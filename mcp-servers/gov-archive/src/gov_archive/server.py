"""gov-archive MCP server — stdio, FastMCP based."""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from . import tools as T
from .paths import log, workspace_root

mcp = FastMCP("gov-archive")


@mcp.tool(annotations={"readOnlyHint": True})
def archive_fetch(url: str, note: str = "") -> dict:
    """정부 도메인 등 외부 URL 본문을 archive/raw 아래에 보존하고 SHA-256을 반환합니다.

    Args:
        url: 가져올 URL (http/https).
        note: 수집 의도 한 줄 (선택).
    """
    return T.archive_fetch(url, note=note or None)


@mcp.tool(annotations={"readOnlyHint": True})
def archive_search(query: str, scope: str = "all", limit: int = 50) -> list[dict]:
    """워크스페이스 archive에서 텍스트를 검색합니다.

    Args:
        query: 검색어.
        scope: "raw" | "processed" | "all".
        limit: 최대 결과 수 (기본 50).
    """
    return T.archive_search(query, scope=scope, limit=limit)


@mcp.tool(annotations={"readOnlyHint": True})
def archive_cite(path: str) -> str:
    """archive/raw 아래 파일의 인용 메타(Markdown 블록)를 반환합니다.

    Args:
        path: archive/raw 기준 상대 경로 또는 절대 경로.
    """
    return T.archive_cite(path)


def describe() -> str:
    """Used by `civic: mcp doctor` task to verify the server can be loaded."""
    return f"gov-archive ok @ {workspace_root()}"


def main() -> None:
    log(f"starting gov-archive (root={workspace_root()})")
    mcp.run()


if __name__ == "__main__":
    main()
