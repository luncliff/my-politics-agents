"""Tool implementations for gov-archive."""

from __future__ import annotations
import hashlib
import json
import pathlib
import re
from typing import Any
from urllib.parse import unquote, urlparse

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


def _sanitize_filename(name: str) -> str:
    name = re.sub(r"\s+", "_", name.strip())
    name = name.replace("/", "_").replace("\\", "_")
    # allow Hangul for readability on Windows, but strip everything else risky
    name = re.sub(r"[^A-Za-z0-9가-힣._-]+", "_", name)
    name = re.sub(r"_+", "_", name)
    return (name[:160] or "download")


def _safe_basename(url: str) -> str:
    p = urlparse(url)
    name = pathlib.PurePosixPath(p.path).name or "index.html"
    return _sanitize_filename(name)


def _decode_header_filename(value: str) -> str:
    """Best-effort decode for mojibake from latin-1 decoded header values."""
    try:
        raw = value.encode("latin-1")
    except UnicodeEncodeError:
        return value

    for enc in ("utf-8", "cp949"):
        try:
            decoded = raw.decode(enc)
        except UnicodeDecodeError:
            continue
        # prefer a decode that actually yields Hangul characters
        if re.search(r"[가-힣]", decoded):
            return decoded
    # fallback: keep original
    return value


def _filename_from_content_disposition(cd: str) -> str | None:
    if not cd:
        return None

    # Prefer RFC 5987 (filename*)
    for part in cd.split(";"):
        part = part.strip()
        if part.lower().startswith("filename*="):
            v = part.split("=", 1)[1].strip().strip('"')
            # e.g. UTF-8''%ED%95%9C%EA%B8%80.hwpx
            if "''" in v:
                _charset, encoded = v.split("''", 1)
                try:
                    return unquote(encoded)
                except Exception:
                    return encoded
            return v

    for part in cd.split(";"):
        part = part.strip()
        if part.lower().startswith("filename="):
            v = part.split("=", 1)[1].strip().strip('"')
            return _decode_header_filename(v)

    return None


def _append_tag(filename: str, tag: str) -> str:
    p = pathlib.PurePosixPath(filename)
    stem, suffix = p.stem, p.suffix
    candidate = f"{stem}__{tag}{suffix}"
    if len(candidate) <= 160:
        return candidate
    # trim stem to fit
    keep = max(1, 160 - len(tag) - len(suffix) - 2)
    return f"{stem[:keep]}__{tag}{suffix}"


def _url_tag(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]


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

    log(f"fetch {url}")
    with httpx.Client(
        timeout=TIMEOUT_SEC, follow_redirects=True, headers={"User-Agent": USER_AGENT}
    ) as client:
        resp = client.get(url)
        resp.raise_for_status()
        body = resp.content

    digest = hashlib.sha256(body).hexdigest()

    cd = resp.headers.get("content-disposition", "")
    cd_name = _filename_from_content_disposition(cd)
    basename = _sanitize_filename(cd_name) if cd_name else _safe_basename(url)

    # prevent collisions for query-driven endpoints (e.g., FileDown.do?atchFileId=...)
    if parsed.query:
        basename = _append_tag(basename, _url_tag(url))

    target = target_dir / basename
    target = ensure_within(raw_root, target)

    log(f"  → {target}")

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
        "content_disposition": resp.headers.get("content-disposition", ""),
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
