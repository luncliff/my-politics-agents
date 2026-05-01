"""Tool implementations for gov-archive."""

from __future__ import annotations
import hashlib
import json
import pathlib
import re
from typing import Any
from urllib.parse import urlparse

import httpx

from .citation import cite
from .paths import (
    archive_processed_root,
    archive_raw_root,
    ensure_within,
    log,
    utc_now_iso,
)

USER_AGENT = "my-politics-agents/0.1 (+https://github.com/luncliff/my-politics-agents)"
TIMEOUT_SEC = 30.0


def _read_sidecar_meta(path: pathlib.Path) -> dict[str, Any]:
    sidecar = path.with_suffix(path.suffix + ".meta.json")
    if not sidecar.exists():
        return {}
    try:
        return json.loads(sidecar.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _charset_from_meta(path: pathlib.Path) -> str | None:
    meta = _read_sidecar_meta(path)
    content_type = str(meta.get("content_type", ""))
    match = re.search(
        r"charset\s*=\s*['\"]?([A-Za-z0-9._-]+)", content_type, re.IGNORECASE
    )
    if not match:
        return None
    return match.group(1)


def _read_searchable_text(path: pathlib.Path) -> str:
    encodings: list[str] = []
    detected = _charset_from_meta(path)
    if detected:
        encodings.append(detected)
    encodings.extend(["utf-8", "utf-8-sig", "cp949", "euc-kr"])

    seen: set[str] = set()
    for encoding in encodings:
        key = encoding.lower()
        if key in seen:
            continue
        seen.add(key)
        try:
            return path.read_text(encoding=encoding)
        except (LookupError, OSError, UnicodeDecodeError):
            continue

    return path.read_text(encoding="utf-8", errors="ignore")


def _safe_basename(url: str) -> str:
    p = urlparse(url)
    name = pathlib.PurePosixPath(p.path).name or "index.html"
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
    return name[:160] or "index.html"


def archive_fetch(url: str, note: str | None = None) -> dict[str, Any]:
    """Fetch URL and store under archive/raw/<host>/<basename>.

    Returns metadata: {path, sha256, status, bytes, source_url, collected_at, changed}
    """
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"unsupported scheme: {parsed.scheme}")
    host = parsed.netloc.lower()
    if not host:
        raise ValueError("missing host")

    raw_root = archive_raw_root()
    target_dir = raw_root / host
    target_dir.mkdir(parents=True, exist_ok=True)
    target_dir = ensure_within(raw_root, target_dir)

    target = target_dir / _safe_basename(url)
    target = ensure_within(raw_root, target)

    log(f"fetch {url} → {target}")
    with httpx.Client(
        timeout=TIMEOUT_SEC, follow_redirects=True, headers={"User-Agent": USER_AGENT}
    ) as client:
        resp = client.get(url)
        resp.raise_for_status()
        body = resp.content

    digest = hashlib.sha256(body).hexdigest()

    changed = True
    if target.exists():
        existing_digest = hashlib.sha256(target.read_bytes()).hexdigest()
        changed = existing_digest != digest

    if changed:
        target.write_bytes(body)

    meta = {
        "source_url": url,
        "collected_at": utc_now_iso(),
        "sha256": digest,
        "bytes": len(body),
        "status": resp.status_code,
        "content_type": resp.headers.get("content-type", ""),
        "note": note or "",
    }
    sidecar = target.with_suffix(target.suffix + ".meta.json")
    sidecar.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "path": str(target.relative_to(raw_root.parent.parent)),
        "changed": changed,
        **meta,
    }


def archive_search(
    query: str, scope: str = "all", limit: int = 50
) -> list[dict[str, Any]]:
    """Plain-text search across archive directories. Returns up to `limit` hits."""
    if not query:
        raise ValueError("query is required")

    roots: list[pathlib.Path] = []
    if scope in ("raw", "all"):
        roots.append(archive_raw_root())
    if scope in ("processed", "all"):
        roots.append(archive_processed_root())
    if not roots:
        raise ValueError("scope must be one of: raw, processed, all")

    pattern = re.compile(re.escape(query), re.IGNORECASE)
    hits: list[dict[str, Any]] = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if not p.is_file() or p.suffix in (".meta.json",):
                continue
            try:
                text = _read_searchable_text(p)
            except OSError:
                continue
            for i, line in enumerate(text.splitlines(), start=1):
                if pattern.search(line):
                    hits.append(
                        {
                            "path": str(p),
                            "line": i,
                            "preview": line.strip()[:240],
                        }
                    )
                    if len(hits) >= limit:
                        return hits
    return hits


def archive_cite(path: str) -> str:
    """Return Markdown citation block for the given archived file path."""
    return cite(path)
