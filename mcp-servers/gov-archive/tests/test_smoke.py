"""Smoke tests — no network."""
from __future__ import annotations
import pathlib

from gov_archive.paths import (
    archive_raw_root,
    ensure_within,
    workspace_root,
)
from gov_archive.server import describe


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
