# tools/AGENTS.md — Tools, adapters, MCP servers

Scope: `tools/` 하위. 공통 규약은 [/AGENTS.md](../AGENTS.md).

## 구성

- `tools/js/` — Node/TypeScript 어댑터.
- `tools/nemotron_personas/` — 합성 시민 페르소나 샘플러 (Python).
- `tools/eslint.config.js`, `tools/.prettierrc`, `tools/.prettierignore` — JS/TS lint·format 설정.

## 추가 기준 — 새 도구·도메인이 필요할 때

1. 공급자 / 주소 / 필요한 권한을 사용자에게 알리고 승인을 받는다.
2. `.vscode/settings.json` 자동 승인 항목은 PR로 추가한다.
3. 새 어댑터·MCP는 `tools/` 적절한 하위에 정의하고, lint·테스트가 CI에서 돌도록 등록한다.

## 검증

- JS/TS: `npm run lint`, `npm run format:check` (워크스페이스 루트에서).
- Python MCP: 각 서버 폴더에서 `uv run pytest -q tests`.

## 보안

- 토큰 / 자격증명은 코드·로그·산출물에 절대 포함하지 않는다.
- 외부 호출은 root [/AGENTS.md](../AGENTS.md) 의 `robots.txt` · 율 제한 규정을 따른다.
