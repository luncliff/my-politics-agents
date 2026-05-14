# Agent & Skill Naming Conventions

## Skills (`.agents/skills/<name>/SKILL.md`)

이름은 **verb-noun** 형식을 사용한다.

| 형식 | 예시 |
|---|---|
| `verb-noun` | `track-goals`, `review-feedback`, `search-night-care`, `pii-mask` |
| `verb-noun-qualifier` | `local-budget-tracker` → 향후 `track-local-budget` 으로 별칭 가능 |

기존 skill 중 이 규칙 이전에 만들어진 것들(예: `local-budget-tracker`, `retrospective-writer`)은 그대로 유지한다. 새로 만드는 skill은 반드시 verb-noun을 따른다.

## Agents

에이전트 정의의 이름은 **역할 noun**을 사용한다.

| 채널 | 위치 | 예시 |
|---|---|---|
| Claude Code | `.claude/agents/<noun>.md` | `lawyer`, `researcher`, `ordinance` |
| GitHub Copilot | `.github/agents/<noun>.agent.md` | `lawyer-agent`, `party-advisor` |
| Codex CLI | `.codex/agents/<noun>.toml` | `lawyer-agent`, `civic-persona-panel` |

에이전트 이름에 `-agent` 접미사는 Copilot/Codex 채널에서 관례적으로 사용. Claude Code는 접미사 없이 순수 noun.

## Channel-Specific Files

채널별 설정/정의 파일은 각 채널 폴더에서만 관리한다:

| 채널 | 설정 위치 |
|---|---|
| Claude Code | `.claude/` |
| GitHub Copilot | `.github/` |
| Codex CLI | `.codex/` |
| VS Code | `.vscode/` |

공통 skill은 `.agents/skills/`에 두고, 채널별 파일에서 참조한다.
