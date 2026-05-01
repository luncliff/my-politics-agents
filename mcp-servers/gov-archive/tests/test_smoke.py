"""Smoke tests — no network."""

from __future__ import annotations
import json
import pathlib
import re

from gov_archive.paths import (
    archive_raw_root,
    ensure_within,
    workspace_root,
)
from gov_archive.server import describe
from gov_archive.tools import archive_fetch, archive_search


def test_describe_runs():
    msg = describe()
    assert "gov-archive" in msg


def test_workspace_root_is_path():
    assert isinstance(workspace_root(), pathlib.Path)


def test_ensure_within_blocks_traversal(tmp_path):
    root = tmp_path
    (root / "ok.txt").write_text("ok", encoding="utf-8")
    ensure_within(root, root / "ok.txt")  # should not raise

    try:
        ensure_within(root, root / ".." / "outside.txt")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for traversal")


def test_archive_root_has_archive_segment():
    assert "archive" in str(archive_raw_root())


def test_archive_search_finds_korean_text_in_utf8_source(monkeypatch, tmp_path):
    monkeypatch.setenv("CIVIC_REPO_ROOT", str(tmp_path))

    host_dir = tmp_path / "archive" / "raw" / "example.go.kr"
    host_dir.mkdir(parents=True)
    source = host_dir / "2026-05-02 utf8.txt"
    source.write_text("한글 UTF-8 검색", encoding="utf-8")

    hits = archive_search("UTF-8", scope="raw")

    assert len(hits) == 1
    assert hits[0]["preview"] == "한글 UTF-8 검색"


def test_archive_search_finds_korean_text_in_cp949_source(monkeypatch, tmp_path):
    monkeypatch.setenv("CIVIC_REPO_ROOT", str(tmp_path))

    host_dir = tmp_path / "archive" / "raw" / "example.go.kr"
    host_dir.mkdir(parents=True)
    source = host_dir / "2026-05-02 sample.txt"
    source.write_bytes("한글 원문 검색".encode("cp949"))

    meta = {
        "source_url": "https://example.go.kr/sample.txt",
        "collected_at": "2026-05-02T00:00:00Z",
        "sha256": "dummy",
        "content_type": "text/plain; charset=cp949",
    }
    source.with_suffix(source.suffix + ".meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    hits = archive_search("한글", scope="raw")

    assert len(hits) == 1
    assert hits[0]["preview"] == "한글 원문 검색"


def test_archive_fetch_does_not_prepend_collection_date(monkeypatch, tmp_path):
    monkeypatch.setenv("CIVIC_REPO_ROOT", str(tmp_path))

    class FakeResponse:
        status_code = 200
        headers = {"content-type": "application/pdf"}
        content = b"pdf-bytes"

        def raise_for_status(self):
            return None

    class FakeClient:
        def __init__(self, **_kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def get(self, _url):
            return FakeResponse()

    monkeypatch.setattr("gov_archive.tools.httpx.Client", FakeClient)

    result = archive_fetch("https://example.go.kr/20250423_report.pdf")
    rel_path = pathlib.Path(result["path"])
    basename = rel_path.name

    assert not re.match(r"^\d{4}-\d{2}-\d{2}\s", basename)
    assert basename == "20250423_report.pdf"
    assert (tmp_path / rel_path).exists()
    assert (tmp_path / rel_path).with_suffix(".pdf.meta.json").exists()
