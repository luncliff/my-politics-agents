"""Download Nemotron-Personas-Korea parquet shards into archive/raw with .meta.json sidecars.

Usage:
    uv run python -m nemotron_personas.fetch --dry-run
    uv run python -m nemotron_personas.fetch
"""

from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import pathlib
import sys

from .config import DATASET_REPO, HF_RESOLVE_BASE, LICENSE, ATTRIBUTION, RAW_DIR


def _sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _list_parquet_files() -> list[str]:
    from huggingface_hub import HfApi  # lazy import

    api = HfApi()
    files = api.list_repo_files(repo_id=DATASET_REPO, repo_type="dataset")
    return sorted(p for p in files if p.endswith(".parquet"))


def _write_sidecar(parquet_path: pathlib.Path, rel_repo_path: str) -> dict:
    digest = _sha256(parquet_path)
    sidecar = {
        "source_url": f"{HF_RESOLVE_BASE}/{rel_repo_path}",
        "collected_at": dt.datetime.now(dt.UTC)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
        "sha256": digest,
        "size_bytes": parquet_path.stat().st_size,
        "license": LICENSE,
        "attribution": ATTRIBUTION,
        "dataset": DATASET_REPO,
        "repo_path": rel_repo_path,
    }
    meta_path = parquet_path.with_suffix(parquet_path.suffix + ".meta.json")
    meta_path.write_text(
        json.dumps(sidecar, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return sidecar


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Fetch Nemotron-Personas-Korea parquet shards"
    )
    ap.add_argument(
        "--dry-run", action="store_true", help="List files and target paths only"
    )
    ap.add_argument(
        "--force", action="store_true", help="Re-download even if file exists"
    )
    args = ap.parse_args(argv)

    files = _list_parquet_files()
    if not files:
        print("No parquet files found in repo", file=sys.stderr)
        return 1

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Dataset:     {DATASET_REPO}")
    print(f"License:     {LICENSE}")
    print(f"Target dir:  {RAW_DIR}")
    print(f"Parquet shards: {len(files)}")
    for rel in files:
        print(f"  - {rel}  ->  {HF_RESOLVE_BASE}/{rel}")

    if args.dry_run:
        print("\n[dry-run] no download performed")
        return 0

    from huggingface_hub import hf_hub_download  # lazy import

    for rel in files:
        target = RAW_DIR / pathlib.Path(rel).name
        if target.exists() and not args.force:
            print(f"skip (exists): {target.name}")
            if not target.with_suffix(target.suffix + ".meta.json").exists():
                _write_sidecar(target, rel)
                print(f"  + sidecar written")
            continue
        print(f"download: {rel}")
        local = hf_hub_download(
            repo_id=DATASET_REPO,
            filename=rel,
            repo_type="dataset",
            local_dir=str(RAW_DIR),
        )
        local_path = pathlib.Path(local)
        # huggingface_hub may place the file under a subdir matching repo path.
        # Move / copy meta beside it.
        sidecar = _write_sidecar(local_path, rel)
        print(f"  ok sha256={sidecar['sha256'][:12]}… size={sidecar['size_bytes']:,}B")

    print("\ndone")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
