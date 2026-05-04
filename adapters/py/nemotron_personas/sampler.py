"""Stratified sampling of Nemotron-Personas-Korea into civic panel card libraries.

Outputs JSONL (one persona per line, demographic + persona text fields)
and a human-readable Markdown summary with footer citation.

Usage:
    uv run python -m nemotron_personas.sampler \\
        --panel national --size 300 --seed 20260504
    uv run python -m nemotron_personas.sampler \\
        --panel local --district 분당구 --size 100 --seed 20260504
"""

from __future__ import annotations
import argparse
import datetime as dt
import json
import pathlib
import random
import sys
from collections import defaultdict
from typing import Iterable

from .config import (
    DATASET_REPO,
    DEFAULT_FIELDS,
    HF_RESOLVE_BASE,
    LICENSE,
    PROCESSED_DIR,
    RAW_DIR,
    REPO_ROOT,
)

AGE_BUCKETS = [
    ("19-29", 19, 29),
    ("30-39", 30, 39),
    ("40-49", 40, 49),
    ("50-59", 50, 59),
    ("60-69", 60, 69),
    ("70-79", 70, 79),
    ("80+", 80, 200),
]

PROVINCE_SUFFIXES = (
    "특별자치도",
    "특별자치시",
    "특별시",
    "광역시",
    "자치도",
    "자치시",
    "도",
    "시",
)


def _age_bucket(age: int | None) -> str:
    if age is None:
        return "unknown"
    for label, lo, hi in AGE_BUCKETS:
        if lo <= age <= hi:
            return label
    return "unknown"


def _normalize_province(value: str | None) -> str | None:
    if not value:
        return value
    province = value.strip()
    for suffix in PROVINCE_SUFFIXES:
        if province.endswith(suffix):
            return province[: -len(suffix)]
    return province


def _iter_records(
    parquet_files: list[pathlib.Path], fields: list[str]
) -> Iterable[dict]:
    import pyarrow.parquet as pq  # lazy import

    for fp in parquet_files:
        pf = pq.ParquetFile(str(fp))
        present = [c for c in fields if c in pf.schema_arrow.names]
        for batch in pf.iter_batches(batch_size=8192, columns=present):
            cols = {name: batch.column(name).to_pylist() for name in present}
            n = len(next(iter(cols.values())))
            for i in range(n):
                yield {name: cols[name][i] for name in present}


def _stratify_key(rec: dict, mode: str) -> tuple:
    sex = rec.get("sex") or "?"
    age_b = _age_bucket(rec.get("age"))
    if mode == "national":
        return (rec.get("province") or "?", sex, age_b)
    return (rec.get("district") or "?", sex, age_b)


def _sample_stratified(
    pool: list[dict],
    size: int,
    mode: str,
    rng: random.Random,
) -> list[dict]:
    buckets: dict[tuple, list[dict]] = defaultdict(list)
    for rec in pool:
        buckets[_stratify_key(rec, mode)].append(rec)

    if not buckets:
        return []

    # Floor: at least 1 per non-empty bucket, then proportional fill.
    floor = {k: 1 for k in buckets}
    remaining = max(0, size - sum(floor.values()))
    total = sum(len(v) for v in buckets.values())
    proportional = {
        k: max(0, round(len(v) / total * remaining)) for k, v in buckets.items()
    }
    quota = {k: floor[k] + proportional.get(k, 0) for k in buckets}
    # Adjust to hit `size` exactly.
    diff = size - sum(quota.values())
    keys_by_pool = sorted(buckets.keys(), key=lambda k: -len(buckets[k]))
    i = 0
    while diff != 0 and keys_by_pool:
        k = keys_by_pool[i % len(keys_by_pool)]
        if diff > 0 and quota[k] < len(buckets[k]):
            quota[k] += 1
            diff -= 1
        elif diff < 0 and quota[k] > 1:
            quota[k] -= 1
            diff += 1
        i += 1
        if i > 10 * len(keys_by_pool) and diff != 0:
            break

    out: list[dict] = []
    for k, recs in buckets.items():
        n = min(quota[k], len(recs))
        out.extend(rng.sample(recs, n))
    rng.shuffle(out)
    return out


def _md_card(rec: dict) -> str:
    lines = [
        f"### {rec.get('uuid', '?')[:8]} · {rec.get('sex', '?')}/{rec.get('age', '?')} · "
        f"{rec.get('province', '?')} {rec.get('district', '')}".strip(),
        f"- 학력: {rec.get('education_level', '?')} · 직업: {rec.get('occupation', '?')} "
        f"· 가구: {rec.get('household_type', '?')} · 혼인: {rec.get('marital_status', '?')}",
    ]
    concise = rec.get("concise_persona") or rec.get("professional_persona")
    if concise:
        lines.append(f"- {concise.strip()}")
    hobbies = rec.get("hobbies_and_interests")
    if hobbies:
        lines.append(f"- 관심사: {str(hobbies).strip()}")
    goals = rec.get("goals_and_ambitions")
    if goals:
        lines.append(f"- 목표: {str(goals).strip()}")
    return "\n".join(lines)


def _read_location(repo_root: pathlib.Path) -> str:
    loc = repo_root / "location.txt"
    if not loc.exists():
        return ""
    return loc.read_text(encoding="utf-8").strip()


def _meta_for_sources(parquet_files: list[pathlib.Path]) -> list[dict]:
    items = []
    for fp in parquet_files:
        meta_path = fp.with_suffix(fp.suffix + ".meta.json")
        if meta_path.exists():
            items.append(json.loads(meta_path.read_text(encoding="utf-8")))
    return items


def _footer(meta_items: list[dict]) -> str:
    today = dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    bullets = []
    for m in meta_items:
        bullets.append(
            f"- {m.get('repo_path', '?')} · sha256:{(m.get('sha256') or '')[:12]} · "
            f"수집 {m.get('collected_at', '?')}"
        )
    src_block = "\n".join(bullets) if bullets else "- (no sidecar found)"
    return (
        "\n---\n"
        f"출처: {HF_RESOLVE_BASE} · 라이선스: {LICENSE} · 추출 {today}\n"
        f"속성: {DATASET_REPO} (NVIDIA, CC BY 4.0)\n\n"
        f"원본 shard:\n{src_block}\n\n"
        "본 카드의 페르소나는 합성 데이터로, 실존 인물과의 어떠한 유사성도 우연입니다.\n"
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Sample Nemotron-Personas-Korea into a civic panel"
    )
    ap.add_argument("--panel", choices=["national", "local"], required=True)
    ap.add_argument(
        "--size", type=int, default=None, help="Target panel size (default: 300/100)"
    )
    ap.add_argument("--district", default=None, help="Filter district (local panel)")
    ap.add_argument("--province", default=None, help="Filter province (local panel)")
    ap.add_argument("--seed", type=int, default=20260504)
    ap.add_argument("--out-jsonl", type=pathlib.Path, default=None)
    ap.add_argument("--out-md", type=pathlib.Path, default=None)
    args = ap.parse_args(argv)

    parquet_files = sorted(RAW_DIR.glob("*.parquet"))
    if not parquet_files:
        # check nested layout from huggingface_hub.snapshot_download
        parquet_files = sorted(RAW_DIR.rglob("*.parquet"))
    if not parquet_files:
        print(
            f"No parquet files in {RAW_DIR}. Run `python -m nemotron_personas.fetch` first.",
            file=sys.stderr,
        )
        return 1

    repo_root = REPO_ROOT
    if args.panel == "local" and not (args.district or args.province):
        loc = _read_location(repo_root)
        # Heuristic: parse trailing tokens like "성남시 분당구"
        tokens = loc.split()
        if len(tokens) >= 2:
            args.province = _normalize_province(tokens[-3] if len(tokens) >= 3 else None)
            args.district = " ".join(tokens[-2:]) if len(tokens) >= 3 else tokens[-1]
            print(
                f"location.txt -> province={args.province} district={args.district}"
            )

    size = args.size or (300 if args.panel == "national" else 100)
    rng = random.Random(args.seed)

    print(f"Loading {len(parquet_files)} parquet shard(s) from {RAW_DIR}")
    pool: list[dict] = []
    for rec in _iter_records(parquet_files, DEFAULT_FIELDS):
        if args.panel == "local":
            if args.district and args.district not in (rec.get("district") or ""):
                continue
            if args.province and args.province not in (rec.get("province") or ""):
                continue
        pool.append(rec)
    print(f"pool size: {len(pool):,}")
    if not pool:
        print("Empty pool after filters", file=sys.stderr)
        return 2

    sampled = _sample_stratified(pool, size, args.panel, rng)
    print(f"sampled: {len(sampled)}")

    out_dir = PROCESSED_DIR / "panels"
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = args.panel if args.panel == "national" else (args.district or "local")
    jsonl_path = args.out_jsonl or out_dir / f"{slug}-{len(sampled)}.jsonl"
    md_path = args.out_md or out_dir / f"{slug}-{len(sampled)}.md"

    with jsonl_path.open("w", encoding="utf-8") as f:
        for rec in sampled:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"wrote {jsonl_path}")

    meta_items = _meta_for_sources(parquet_files)
    header = (
        f"# Nemotron-Personas-Korea — {args.panel} 패널 ({len(sampled)}명)\n\n"
        f"- 시드: {args.seed}\n"
        f"- 필터: panel={args.panel}, province={args.province or '-'}, district={args.district or '-'}\n"
        f"- 필드: {', '.join(DEFAULT_FIELDS)}\n\n"
    )
    body = "\n\n".join(_md_card(r) for r in sampled)
    md_path.write_text(header + body + _footer(meta_items), encoding="utf-8")
    print(f"wrote {md_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
