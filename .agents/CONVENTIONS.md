# Agent & Skill Naming Conventions

## Skills (`.agents/skills/<verb-noun>/SKILL.md`)

이름은 **verb-noun** 형식을 강제한다. `local-` 접두는 `location.txt`로 지역이 결정되므로 사용하지 않는다.

| 형식 | 예시 |
|---|---|
| `verb-noun` | `track-budget`, `track-funds`, `track-timeline`, `track-transit`, `collect-ordinance`, `review-persona`, `review-party-alignment`, `mask-pii`, `write-retro`, `find-night-clinic`, `add-vscode-task`, `improve-harness`, `track-goals`, `diagnose-prompts` |

## Agents

에이전트 식별자는 모든 채널에서 **동일한 짧은 noun 또는 noun-noun**을 쓴다. `-agent` 접미는 폐지한다(파일명·frontmatter `name`·호출자 모두).

| 채널 | 위치 | 파일명 패턴 |
|---|---|---|
| Claude Code | `.claude/agents/<noun>.md` | `lawyer.md`, `minutes.md`, `ordinance.md`, `persona-panel.md`, `gov-researcher.md`, `party-advisor.md` |
| GitHub Copilot | `.github/agents/<noun>.agent.md` | `lawyer.agent.md`, `minutes.agent.md`, `ordinance.agent.md`, `persona-panel.agent.md`, `gov-researcher.agent.md`, `party-advisor.agent.md` |
| Codex CLI | `.codex/agents/<noun>.toml` | `lawyer.toml`, `minutes.toml`, `ordinance.toml`, `persona-panel.toml`, `gov-researcher.toml`, `party-advisor.toml` |

채널 간 베이스명은 일치해야 한다. 동일 도메인은 단일 에이전트로 통합하고, 모드는 인자로 분기한다(예: `ordinance collect|brief`).

## Prompts / Commands

세 채널 모두 동일한 8개 명령 세트를 유지한다.

| 명령 | Copilot | Claude | Codex |
|---|---|---|---|
| `collect` | `.github/prompts/collect.prompt.md` | `.claude/commands/collect.md` | `.codex/prompts/collect.md` |
| `brief` | `.github/prompts/brief.prompt.md` | `.claude/commands/brief.md` | `.codex/prompts/brief.md` |
| `retro` | `.github/prompts/retro.prompt.md` | `.claude/commands/retro.md` | `.codex/prompts/retro.md` |
| `persona-review` | `.github/prompts/persona-review.prompt.md` | `.claude/commands/persona-review.md` | `.codex/prompts/persona-review.md` |
| `diagnose-prompts` | `.github/prompts/diagnose-prompts.prompt.md` | `.claude/commands/diagnose-prompts.md` | `.codex/prompts/diagnose-prompts.md` |
| `improve-harness` | `.github/prompts/improve-harness.prompt.md` | `.claude/commands/improve-harness.md` | `.codex/prompts/improve-harness.md` |
| `track-goals` | `.github/prompts/track-goals.prompt.md` | `.claude/commands/track-goals.md` | `.codex/prompts/track-goals.md` |
| `health` | — (생략) | `.claude/commands/health.md` | `.codex/prompts/health.md` |

채널별 best practice는 frontmatter / 본문 구조에서만 분기한다.

- `.claude/`: Claude Code subagents 가이드 — frontmatter 최소(`name`, `description`), 본문은 절차적 지시.
- `.codex/`: ChatGPT prompting guide + Codex CLI prompting guide — `developer_instructions`(또는 prompt 본문)에 **Role / Context / Procedure / Output** 섹션 표준화, 짧은 명령형.
- `.github/`: Copilot — frontmatter `tools`, `model`, `argument-hint`를 정확히 채우고, prompt 본문은 "스킬 참조 + 호출 인자" 패턴.

## Channel-Specific Files

채널별 설정/정의 파일은 각 채널 폴더에서만 관리한다.

| 채널 | 설정 위치 |
|---|---|
| Claude Code | `.claude/` |
| GitHub Copilot | `.github/` |
| Codex CLI | `.codex/` |
| VS Code | `.vscode/` |

공통 skill은 `.agents/skills/`에 두고, 채널별 파일에서 참조한다.

## SKILL.md 규약 (Anthropic skills 형식)

- YAML frontmatter `name` / `description` 필수.
- `description` 첫 문장은 동사로 시작한다.
- `Use when:` 절을 description 또는 본문 상단에 둔다.
- 재사용 템플릿은 `references/`에 두고, 산출물은 `보관함/양식/` 또는 `보관함/결과/`에 저장한다.
