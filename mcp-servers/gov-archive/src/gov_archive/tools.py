"""Tool implementations for gov-archive."""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
from html.parser import HTMLParser
from typing import Any
from urllib.parse import unquote, urljoin, urlparse, urlunparse

import httpx

from .citation import cite
from .converters import SUPPORTED_EXTENSIONS, convert_to_markdown
from .paths import (
    archive_processed_root,
    archive_raw_root,
    ensure_within,
    log,
    utc_now_iso,
    workspace_root,
)

USER_AGENT = "my-politics-agents/0.1 (+https://github.com/luncliff/my-politics-agents)"
TIMEOUT_SEC = 30.0
AUTO_DOWNLOAD_EXTENSIONS = {".hwp", ".hwpx", ".docx", ".pdf"}
HTML_EXTENSIONS = {".html", ".htm"}
MAX_LINKED_DOWNLOADS = 20


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
    # URL-decode percent-encoded sequences (e.g. %ED%95%9C%EA%B8%80 → 한글)
    name = unquote(name, encoding="utf-8", errors="replace")
    # Strip only characters that are actually unsafe on filesystems
    name = re.sub(r'[\x00-\x1F\x7F/\\:*?"<>|]+', "_", name)
    return name[:160] or "index.html"


def _looks_like_html(content_type: str, body: bytes) -> bool:
    ct = content_type.lower()
    if "text/html" in ct or "application/xhtml+xml" in ct:
        return True
    head = body[:256].lstrip().lower()
    return head.startswith(b"<!doctype html") or head.startswith(b"<html")


def _target_basename(url: str, content_type: str, body: bytes) -> str:
    base = _safe_basename(url)
    if _looks_like_html(content_type, body):
        ext = pathlib.Path(base).suffix.lower()
        if ext not in HTML_EXTENSIONS:
            stem = pathlib.Path(base).stem or "index"
            base = f"{stem}.html"
    return base


class _LinkExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        for key, value in attrs:
            if key.lower() == "href" and value:
                self.links.append(value.strip())
                break


def _detect_html_charset(body: bytes, content_type: str = "") -> str:
    """Detect charset from Content-Type header or HTML <meta> tags."""
    match = re.search(r"charset\s*=\s*['\"]?([A-Za-z0-9._-]+)", content_type, re.IGNORECASE)
    if match:
        return match.group(1)
    head = body[:2048]
    match = re.search(rb'<meta[^>]+charset\s*=\s*["\']?([A-Za-z0-9._-]+)', head, re.IGNORECASE)
    if match:
        return match.group(1).decode("ascii", errors="ignore")
    match = re.search(rb'charset\s*=\s*([A-Za-z0-9._-]+)', head, re.IGNORECASE)
    if match:
        return match.group(1).decode("ascii", errors="ignore")
    return "utf-8"


def _extract_document_links(url: str, body: bytes, content_type: str = "") -> list[str]:
    charset = _detect_html_charset(body, content_type)
    try:
        html = body.decode(charset, errors="ignore")
    except LookupError:
        html = body.decode("utf-8", errors="ignore")
    parser = _LinkExtractor()
    parser.feed(html)

    out: list[str] = []
    seen: set[str] = set()
    for href in parser.links:
        abs_url = urljoin(url, href)
        parsed = urlparse(abs_url)
        if parsed.scheme not in ("http", "https"):
            continue
        suffix = pathlib.PurePosixPath(parsed.path).suffix.lower()
        if suffix not in AUTO_DOWNLOAD_EXTENSIONS:
            continue
        normalized = urlunparse(
            (parsed.scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, "")
        )
        if normalized in seen:
            continue
        seen.add(normalized)
        out.append(normalized)
    return out


def _to_workspace_relative(path: pathlib.Path) -> str:
    return str(path.relative_to(workspace_root()))


def _persist_payload(
    *,
    url: str,
    body: bytes,
    status: int,
    content_type: str,
    note: str | None = None,
    auto_convert: bool = True,
) -> dict[str, Any]:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if not host:
        raise ValueError("missing host")

    raw_root = archive_raw_root()
    target_dir = ensure_within(raw_root, raw_root / host)
    target_dir.mkdir(parents=True, exist_ok=True)

    basename = _target_basename(url, content_type, body)
    target = ensure_within(raw_root, target_dir / basename)

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
        "status": status,
        "content_type": content_type,
        "note": note or "",
    }
    sidecar = target.with_suffix(target.suffix + ".meta.json")
    sidecar.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    convert_result = (
        convert_to_markdown(target)
        if auto_convert and changed and target.suffix.lower() in SUPPORTED_EXTENSIONS
        else None
    )

    result = {
        "path": _to_workspace_relative(target),
        "changed": changed,
        **meta,
    }
    if convert_result:
        result["conversion"] = convert_result
    return result


def archive_fetch(
    url: str, note: str | None = None, auto_convert: bool = True
) -> dict[str, Any]:
    """Fetch URL and store under 보관함/다운로드/<host>/<basename>.

    Returns metadata: {path, sha256, status, bytes, source_url, collected_at, changed}
    """
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"unsupported scheme: {parsed.scheme}")
    log(f"fetch {url}")
    with httpx.Client(
        timeout=TIMEOUT_SEC, follow_redirects=True, headers={"User-Agent": USER_AGENT}
    ) as client:
        resp = client.get(url)
        resp.raise_for_status()
        body = resp.content
        content_type = resp.headers.get("content-type", "")

        primary = _persist_payload(
            url=url,
            body=body,
            status=resp.status_code,
            content_type=content_type,
            note=note,
            auto_convert=auto_convert,
        )

        linked_downloads: list[dict[str, Any]] = []
        linked_skipped = 0
        if _looks_like_html(content_type, body):
            links = _extract_document_links(url, body, content_type)
            linked_skipped = max(0, len(links) - MAX_LINKED_DOWNLOADS)
            for link in links[:MAX_LINKED_DOWNLOADS]:
                try:
                    linked = client.get(link)
                    linked.raise_for_status()
                    linked_downloads.append(
                        _persist_payload(
                            url=link,
                            body=linked.content,
                            status=linked.status_code,
                            content_type=linked.headers.get("content-type", ""),
                            note=f"linked_from={url}",
                            auto_convert=auto_convert,
                        )
                    )
                except httpx.HTTPError as exc:
                    linked_downloads.append(
                        {
                            "source_url": link,
                            "error": f"Failed to download linked document: {exc}",
                        }
                    )

    if linked_downloads:
        primary["linked_downloads"] = linked_downloads
    if linked_skipped:
        primary["linked_downloads_skipped"] = linked_skipped
    return primary


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


def archive_convert(path: str) -> dict[str, str | bool]:
    """Convert archived file to Markdown under 보관함/결과."""
    raw_root = archive_raw_root()
    candidate = pathlib.Path(path)
    target = candidate if candidate.is_absolute() else raw_root / candidate
    target = ensure_within(raw_root, target)
    if not target.exists():
        raise FileNotFoundError(target)
    return convert_to_markdown(target)
