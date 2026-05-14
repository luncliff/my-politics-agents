# Architecture

```
Copilot CLI / VS Code Chat / Codex CLI / Claude Code CLI
                    │
        agents/*  +  skills/*  +  commands/*
                    │
            MCP servers (legalize-kr, notebooklm)
                    │
    보관함/다운로드 → 보관함/결과 → notebooks/<slug> → NotebookLM
```

## Directory Map

| Path | Responsibility |
| --- | --- |
| `.github/agents/` | Domain personas (Copilot). |
| `.codex/agents/` | Domain personas (Codex CLI). |
| `.claude/agents/` | Domain personas (Claude Code subagents). |
| `.agents/skills/` | Single-purpose reusable tasks (all channels). |
| `.github/prompts/` | Prompt templates (Copilot). |
| `.claude/commands/` | Slash commands (Claude Code). |
| `.github/hooks/` | Copilot CLI policy · logging. |
| `.claude/settings.json` | Claude Code hooks · env · plugins. |
| `.codex/config.toml` | Codex CLI MCP · model config. |
| `.vscode/` | IDE settings · tasks · MCP · toolsets. |
| `scripts/` | Setup · auth purge · hook scripts. |
| `adapters/` | Per-site collectors (JS/Py). |
| `archive/` | Originals + processed. |
| `notebooks/` | NotebookLM bundles. |
| `회고/` | Cumulative session retros. |
| `data/{legalize,precedent,admrule,ordinance}-kr/` | Shallow clones of legal data. |

## Stack

- **Node 24 LTS**
- **Python 3.12+ (uv)**
- JVM 11+ only when using `opendataloader-pdf`

## Agents (all channels)

| Name | Role | Copilot | Codex | Claude Code |
| --- | --- | --- | --- | --- |
| assembly-minutes | 회의록 정리 (사실/표결/쟁점 분리) | ✅ | ✅ | `minutes` |
| civic-persona-panel | 합성 시민 패널 시뮬레이션 | ✅ | ✅ | `persona-panel` |
| lawyer-agent | 법령·판례·행정규칙 검토 | ✅ | ✅ | `lawyer` |
| ordinance-processor | 조례 수집·분류 | ✅ | ✅ | `ordinance` |
| ordinance-reviewer | 조례 브리핑 작성 | ✅ | ✅ | `ordinance` |
| party-advisor | 정당 플랫폼 정합성 검토 | ✅ | ✅ | — |
| researcher-kr-website | 정부·공공 웹사이트 조사 | ✅ | ✅ | `researcher` |

## Skills (all channels)

| Skill | Purpose |
| --- | --- |
| diagnose-prompts | Prompt/agent/tool configuration audit |
| local-budget-tracker | Municipal budget tracking by 編成目 |
| local-fund-manager | Memory-driven fund portfolio tracking (기금) |
| local-ordinance-processor | Ordinance 3-tier validation + semantic categorization |
| local-timeline-manager | Annual admin/legislative timeline |
| local-transport-tracker | Bus transit data aggregation |
| party-alignment-review | Party platform consistency check |
| persona-perspective-review | Synthetic citizen panel simulation |
| pii-mask | Korean PII anonymization |
| retrospective-writer | Session post-work documentation |
| review-feedback | Retrospective pattern analysis → harness improvement |
| search-night-care | Night-time hospital accessibility research |
| track-goals | Session goal declaration and progress tracking |
| vscode-task-author | VS Code task entry creation |
