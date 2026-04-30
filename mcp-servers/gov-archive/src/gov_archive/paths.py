"""Filesystem layout helpers and the archive root resolver."""
from __future__ import annotations
import os
import pathlib
import sys
from datetime import datetime, timezone


def workspace_root() -> pathlib.Path:
    """Resolve the workspace root.

    Priority: env CIVIC_REPO_ROOT > nearest ancestor with `.git` > cwd.
    """
    env = os.environ.get("CIVIC_REPO_ROOT")
    if env:
        return pathlib.Path(env).resolve()
    here = pathlib.Path.cwd().resolve()
    for p in [here, *here.parents]:
        if (p / ".git").exists() or (p / "AGENTS.md").exists():
            return p
    return here


def archive_raw_root() -> pathlib.Path:
    return workspace_root() / "archive" / "raw"


def archive_processed_root() -> pathlib.Path:
    return workspace_root() / "archive" / "processed"


def ensure_within(root: pathlib.Path, candidate: pathlib.Path) -> pathlib.Path:
    """Reject path traversal outside `root`. Returns resolved path."""
    resolved = candidate.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as e:
        raise ValueError(f"path escapes archive root: {candidate}") from e
    return resolved


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today_dir() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def log(msg: str) -> None:
    """stderr-only logger (stdout is JSON-RPC)."""
    print(f"[gov-archive] {msg}", file=sys.stderr, flush=True)
