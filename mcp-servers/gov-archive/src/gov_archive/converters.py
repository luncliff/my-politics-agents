"""Document-to-Markdown conversion helpers."""

from __future__ import annotations

import pathlib
import re
import tempfile
import xml.etree.ElementTree as ET
import zipfile
import zlib
from typing import Callable

from .paths import archive_processed_root, ensure_within, workspace_root

SUPPORTED_EXTENSIONS = {".hwp", ".hwpx", ".docx", ".pdf"}


def convert_to_markdown(path: pathlib.Path) -> dict[str, str | bool]:
    """Convert supported documents to Markdown under archive/processed."""
    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        return {"converted": False, "reason": f"unsupported extension: {ext or '(none)'}"}

    extractors: dict[str, Callable[[pathlib.Path], str]] = {
        ".docx": _extract_docx_text,
        ".hwpx": _extract_hwpx_text,
        ".hwp": _extract_hwp_text,
        ".pdf": _extract_pdf_text,
    }

    try:
        text = extractors[ext](path)
    except Exception as exc:  # noqa: BLE001
        return {"converted": False, "reason": str(exc)}

    if not text.strip():
        text = "(추출 텍스트 없음)"

    processed_root = archive_processed_root()
    processed_root.mkdir(parents=True, exist_ok=True)
    relative_parent = path.relative_to(workspace_root() / "archive" / "raw").parent
    output_dir = ensure_within(processed_root, processed_root / relative_parent)
    output_dir.mkdir(parents=True, exist_ok=True)
    output = ensure_within(processed_root, output_dir / f"{path.stem}.md")
    output.write_text(
        f"# {path.name}\n\n"
        f"- source_file: `{path.relative_to(workspace_root())}`\n\n"
        f"{text.strip()}\n",
        encoding="utf-8",
    )
    return {"converted": True, "markdown_path": str(output.relative_to(workspace_root()))}


def _extract_docx_text(path: pathlib.Path) -> str:
    with zipfile.ZipFile(path) as zf:
        xml_bytes = zf.read("word/document.xml")
    return _extract_xml_text(xml_bytes)


def _extract_hwpx_text(path: pathlib.Path) -> str:
    with zipfile.ZipFile(path) as zf:
        names = sorted(
            name
            for name in zf.namelist()
            if name.startswith("Contents/section") and name.endswith(".xml")
        )
        if not names:
            raise ValueError("HWPX section XML not found")
        sections = [_extract_xml_text(zf.read(name)) for name in names]
    return "\n\n".join(section for section in sections if section.strip())


def _extract_hwp_text(path: pathlib.Path) -> str:
    try:
        import olefile  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError("HWP conversion requires olefile package") from exc

    with olefile.OleFileIO(str(path)) as ole:
        section_paths = sorted(
            "/".join(parts)
            for parts in ole.listdir(streams=True, storages=False)
            if len(parts) >= 2 and parts[0] == "BodyText" and parts[1].startswith("Section")
        )

        if not section_paths:
            raise ValueError("HWP BodyText sections not found")

        lines: list[str] = []
        for section_path in section_paths:
            stream = ole.openstream(section_path)
            data = stream.read()
            lines.extend(_extract_hwp_paragraph_text(_maybe_inflate_raw_deflate(data)))
        return "\n".join(line for line in lines if line.strip())


def _extract_hwp_paragraph_text(data: bytes) -> list[str]:
    i = 0
    out: list[str] = []
    while i + 4 <= len(data):
        header = int.from_bytes(data[i : i + 4], "little")
        i += 4
        tag_id = header & 0x3FF
        size = (header >> 20) & 0xFFF
        if size == 0xFFF:
            if i + 4 > len(data):
                break
            size = int.from_bytes(data[i : i + 4], "little")
            i += 4
        if i + size > len(data):
            break
        payload = data[i : i + size]
        i += size
        if tag_id == 67:  # HWPTAG_PARA_TEXT
            text = payload.decode("utf-16le", errors="ignore")
            text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", text).strip()
            if text:
                out.append(text)
    return out


def _maybe_inflate_raw_deflate(data: bytes) -> bytes:
    try:
        return zlib.decompress(data, -15)
    except zlib.error:
        return data


def _extract_pdf_text(path: pathlib.Path) -> str:
    markdown = _extract_pdf_text_with_opendataloader(path)
    if markdown is not None:
        return markdown
    return _extract_pdf_text_with_pypdf(path)


def _extract_pdf_text_with_opendataloader(path: pathlib.Path) -> str | None:
    try:
        import opendataloader_pdf  # type: ignore[import-not-found]
    except ImportError:
        return None

    with tempfile.TemporaryDirectory(prefix="gov-archive-pdf-") as temp_dir:
        output_dir = pathlib.Path(temp_dir)
        opendataloader_pdf.convert(
            input_path=[str(path)],
            output_dir=str(output_dir),
            format="markdown",
        )
        markdown_files = sorted(output_dir.rglob("*.md"))
        if not markdown_files:
            return None
        return markdown_files[0].read_text(encoding="utf-8")


def _extract_pdf_text_with_pypdf(path: pathlib.Path) -> str:
    try:
        from pypdf import PdfReader  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError("PDF conversion requires pypdf package") from exc

    reader = PdfReader(str(path))
    pages = [(page.extract_text() or "").strip() for page in reader.pages]
    return "\n\n".join(text for text in pages if text)


def _extract_xml_text(xml_bytes: bytes) -> str:
    root = ET.fromstring(xml_bytes)
    blocks: list[str] = []
    current: list[str] = []

    for elem in root.iter():
        local = elem.tag.split("}")[-1]
        if elem.text and elem.text.strip():
            current.append(elem.text.strip())
        if local in {"br", "tab"}:
            current.append("\n" if local == "br" else "\t")
        if local in {"p", "paragraph"}:
            text = _normalize_ws(" ".join(current))
            if text:
                blocks.append(text)
            current = []

    tail_text = _normalize_ws(" ".join(current))
    if tail_text:
        blocks.append(tail_text)
    return "\n\n".join(blocks)


def _normalize_ws(text: str) -> str:
    return re.sub(r"[ \t]+", " ", text).strip()
