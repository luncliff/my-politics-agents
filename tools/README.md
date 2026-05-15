# tools/

저장소 루트에서 분리한 실행용 자산을 모아 둔 폴더입니다.

| 경로 | 용도 |
| --- | --- |
| `js/` | Node 기반 사이트별 수집·정규화 코드 |
| `nemotron_personas/` | Python 기반 시민 페르소나 수집·샘플링 코드 |
| `eslint.config.mjs` | 저장소 전역 JS/TS 린트 설정 |
| `.prettierrc` | 저장소 전역 JS/TS 포맷 설정 |
| `.prettierignore` | 포맷 대상 제외 규칙 |

## References

자체개발 MCP를 다시 추가할 때는 아래 순서로 확인합니다.

1. [Model Context Protocol](https://modelcontextprotocol.io/) — 프로토콜 개요, transport, lifecycle, tool/resource/prompt 기본 규약
2. [MCP Specification](https://modelcontextprotocol.io/specification/2025-06-18/) — 메시지 포맷, capability negotiation, server/client 의무사항
3. [MCP Docs: Guides](https://modelcontextprotocol.io/docs) — server 구현, 보안, 인증, 배포, inspector 사용 예시
4. 워크스페이스 설정 파일: `/.mcp.json`, `/.vscode/mcp.json`
5. 저장소 규칙: `/AGENTS.md`, `/tools/AGENTS.md`
