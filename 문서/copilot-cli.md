# Copilot CLI / Codex CLI 사용법

## GitHub Copilot CLI

```pwsh
copilot
# 또는 이어서
copilot --continue
```

세션 시작 시 정책 배너가 출력되고, 위험 명령은 차단/경고됩니다. `chat.tools.urls.autoApprove` · `chat.tools.terminal.autoApprove` 화이트리스트는 VS Code와 공유됩니다.

자주 쓰는 호출:

```pwsh
copilot --model=auto --allow-all-urls --add-dir . --prompt "/search-night-care with current location.txt"
```

## Codex CLI

Codex CLI는 같은 워크스페이스의 `agents/`·`.agents/skills/`·`.github/prompts/`·`.vscode/mcp.json`을 그대로 사용합니다.

1. 저장소 루트에서 Codex 세션을 시작합니다(워크스페이스 트러스트 필수).
2. 첫 응답에서 [AGENTS.md](../../AGENTS.md)의 규칙(특히 citation·PII·destructive command 가드)을 따르는지 확인합니다.
3. MCP 서버는 `.vscode/mcp.json` 정의를 그대로 사용하므로 Codex 측 자격증명만 별도로 점검합니다.
4. 세션 종료 직전 `retrospective-writer` 스킬을 호출해 회고를 남깁니다.
