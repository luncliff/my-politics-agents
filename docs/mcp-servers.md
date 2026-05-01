---
description: 워크스페이스 MCP 서버 가이드
---
# MCP 서버

이 저장소는 **워크스페이스 로컬 MCP 서버**를 권장합니다.
`.vscode/mcp.json`에 정의된 서버는 VS Code Chat과 Copilot CLI **양쪽**에서 동일하게 사용됩니다.

## 현재 등록된 서버

| 서버 | 위치 | 상태 | 트랜스폿 |
| --- | --- | --- | --- |
| `gov-archive` | `mcp-servers/gov-archive/` | **동작** | stdio |
| `hwp-toolkit` | `mcp-servers/hwp-toolkit/` | placeholder | (후속) |
| `pdf-loader` | `mcp-servers/pdf-loader/` | placeholder | (후속) |
| `notebooklm-bridge` | `mcp-servers/notebooklm-bridge/` | placeholder | (후속) |

## gov-archive 도구 표면

| 도구 | 입력 | 동작 | 어노테이션 |
| --- | --- | --- | --- |
| `archive_fetch` | `url`, `note?` | URL 본문을 `archive/raw/<host>/`에 저장하고 SHA-256 산출 | `readOnlyHint: true` (외부 read) |
| `archive_search` | `query`, `scope?` | 로컬 archive에서 텍스트 grep | `readOnlyHint: true` |
| `archive_cite` | `path` | 원본 URL·수집 시각·해시로 인용 메타 Markdown 생성 | `readOnlyHint: true` |

- 파일명에는 수집 날짜를 자동 접두어로 붙이지 않습니다.
- 저장 시 URL의 basename을 우선 사용하고, 시간순 추적은 `.meta.json`의 `collected_at`을 기준으로 합니다.

> 모든 쓰기는 워크스페이스 루트의 `archive/raw/` 안으로만 제한됩니다(경로 트래버설 차단).

## 추가·디버그

- 새 서버: `mcp-servers/<name>/`을 만들고 `.vscode/mcp.json`에 등록.
- 핫 리로드·디버그: `.vscode/mcp.json`의 `dev.watch` / `dev.debug` 사용.
  - 서버 정의에서 코드 렌즈로 Start/Stop/Restart 가능.
- 상태 점검: `Tasks: Run Task` → `civic: mcp doctor`.
- 도구 출력 로그: `MCP: List Servers` → 서버 선택 → `Show Output`.

## 작성 시 권장사항

- **로깅은 stderr** (`stdout`에 쓰면 JSON-RPC가 깨집니다).
- read-only 도구는 `readOnlyHint`로 명시 — VS Code가 confirm을 생략합니다.
- 쓰기 도구는 `chat.tools.eligibleForAutoApproval: false`로 두는 것을 권장.
- 자격증명은 항상 환경변수에서 읽고, 도구 인자/로그에는 마스킹.
- 워크스페이스 외부 경로 쓰기 금지(MCP `roots` 검증).

## 참고

- VS Code MCP 가이드: <https://code.visualstudio.com/api/extension-guides/ai/mcp>
- MCP 서버 빌드: <https://modelcontextprotocol.io/docs/develop/build-server>
