# gov-archive MCP server

워크스페이스 로컬 MCP 서버. 외부 자료를 받아 `archive/raw/`에 보존하고, 인용 메타와 로컬 검색 도구를 제공합니다.

## 도구

| 도구 | 입력 | 동작 | 어노테이션 |
| --- | --- | --- | --- |
| `archive_fetch` | `url`, `note?` | URL 본문을 `archive/raw/<host>/<YYYY-MM-DD>/`에 저장 + SHA-256 | `readOnlyHint: true` |
| `archive_search` | `query`, `scope?` (`raw`\|`processed`\|`all`) | 로컬 archive grep | `readOnlyHint: true` |
| `archive_cite` | `path` | 인용 메타 Markdown | `readOnlyHint: true` |

## 실행

```pwsh
uv run --directory mcp-servers/gov-archive gov-archive
```

VS Code/Copilot CLI는 `.vscode/mcp.json`을 통해 자동으로 stdio 연결합니다.

## 안전

- 모든 쓰기는 워크스페이스 루트의 `archive/raw/` 안으로 제한 (경로 트래버설 차단).
- robots.txt 준수, 1초당 동일 호스트 1요청.
- 로깅은 `stderr`로만 (stdout은 JSON-RPC 채널).
