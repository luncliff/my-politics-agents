"""Citation helpers — read frontmatter/sidecar metadata and emit a Markdown citation block."""
from __future__ import annotations
import hashlib
import json
import pathlib
from typing import Any

from .paths import archive_raw_root, ensure_within


def _read_sidecar(path: pathlib.Path) -> dict[str, Any]:
    sidecar = path.with_suffix(path.suffix + ".meta.json")
    if sidecar.exists():
        return json.loads(sidecar.read_text(encoding="utf-8"))
    return {}


def sha256_of(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(64 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def cite(path_str: str) -> str:
    """Return a Markdown citation block for an archived file."""
    raw_root = archive_raw_root()
    path = ensure_within(raw_root, raw_root / path_str if not pathlib.Path(path_str).is_absolute() else pathlib.Path(path_str))
    if not path.exists():
        raise FileNotFoundError(path)

    meta = _read_sidecar(path)
    digest = meta.get("sha256") or sha256_of(path)
    short = digest[:12]

    url = meta.get("source_url", "(unknown)")
    collected = meta.get("collected_at", "(unknown)")
    license_name = meta.get("license", "공공누리 1유형 (추정)")

    return (
        f"출처: {url} · 수집 {collected} · sha256:{short} · 라이선스: {license_name}\n"
        f"\n"
        f"---\n"
        f"```yaml\n"
        f"source_url: \"{url}\"\n"
        f"collected_at: \"{collected}\"\n"
        f"content_sha256: \"{digest}\"\n"
        f"license: \"{license_name}\"\n"
        f"```\n"
    )
