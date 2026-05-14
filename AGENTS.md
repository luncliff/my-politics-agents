# AGENTS.md

Common rules for **GitHub Copilot CLI / VS Code Chat**, **OpenAI Codex CLI**, and **Claude Code CLI** in this workspace.
A narrower scope wins: `applyTo` `.instructions.md` > `agents/` > this file.

## Mission

Build a trusted information pipeline for Korean local politics:
**collect → process → publish**, with citations attached at every step.

## Core Rules

### Workspace-local

- MUST keep all settings, credentials, and caches inside this repo folder.
- MUST ask before any global change (`npm i -g`, `git config --global`, edits to `~/.copilot/*`, `~/.claude/*`, etc.).
- NEVER touch `~/.aws`, `~/.ssh`, OS keychains. Tell the user to do it.

### Citation

- MUST include **source URL · collected_at (ISO-8601 KST) · SHA-256** in every artifact derived from external data.
- MUST preserve originals under `archive/raw/<host>/` (immutable).
- Track time order via `.meta.json` `collected_at`. Do NOT prefix filenames with dates.

### Licensing

| Source | Default license | Note |
| --- | --- | --- |
| `law.go.kr` statutes | Public domain | Modify and reuse freely. |
| Bills · minutes (Assembly · councils) | Mostly KOGL Type 1 | Verify per site. |
| Notices · announcements | KOGL Type 1–4 | Type 4 is non-commercial only. |
| Citizen content (blogs · SNS) | Author copyright | Need consent for direct quotes. |

When unsure, MUST treat as **redistribution forbidden** — summarize and analyze only.

### PII

- MUST run `pii-mask` skill before saving or sharing any text that may contain PII (name · phone · RRN · address · email).
- NEVER persist masking keys to disk (memory only).
- Originals stay in `archive/raw/` for personal review only — NEVER share.

### Political neutrality

- MUST split outputs about parties · candidates · individuals into **Facts** (cited primary sources) and **Interpretation** (reasoning).
- Every Facts item MUST carry a source link.

### Safe automation

- NEVER use `Bypass Approvals`, `Autopilot`, `/yolo`, or unattended destructive commands.
- New tools or domains MUST be approved explicitly before being added to auto-approve lists.
- Destructive commands (`rm -rf`, `git push --force`, `mkfs`, `dd`, `curl|bash`) MUST require human confirmation.
- MUST honor `robots.txt` and rate limits (max 1 req/sec per host).
- If a site's ToS forbids scraping, STOP and ask the user.

## Workflow

### Session start

1. Read `location.txt` — determine the current working region.
2. Verify `data/*-kr/.git` exists. If missing, suggest fetch scripts.
3. Summarize intent in one line and list affected directories.
4. Confirm risk · scope · expected artifacts with the user.

Channel-specific startup:
- **Copilot CLI**: hooks print the policy banner.
- **Claude Code**: `SessionStart` hook runs `scripts/session-start.ps1`.

### During the session

- For any new site or format, preserve the original in `archive/raw/` first.
- If the same task happens twice, log it as a **skill candidate** in the retro.
- If a domain persona appears twice, log it as an **agent candidate**.

### Session end (mandatory retro)

Call the `retrospective-writer` skill (Copilot/Codex) or `/retro` command (Claude Code).
Save to `retrospectives/YYYY-MM-DD <slug>.md`:

- What was tried · what worked · what blocked.
- New sites · formats · policies discovered.
- Automation candidates (skill / agent / task / hook).
- Any missing citations or PII leaks — fix immediately.

## Output Formats

### File naming

- MUST use **Korean filenames** for user-facing generated Korean documents under `archive/processed/`, `data/processed/`, `notebooks/`, `retrospectives/`, and similar artifact folders.
- MUST use `<YYYY-MM> <한글 파일명>.md` as the default filename shape for processed Korean Markdown unless a narrower instruction explicitly overrides it.
- Use Korean filename for human readers. Use English for machine files (code, metadata, logs, tool configurations).

### File organization

- MUST keep `archive/processed/` **flat**. Do NOT create topic subfolders.
- MAY use subfolders in other artifact trees only when an existing repo rule explicitly requires them.

### Processed Markdown

```markdown
---
title: "<title>"
source_url: "<original URL>"
collected_at: "<ISO-8601>"
content_sha256: "<hash>"
license: "KOGL Type 1"
pii_masked: true
---
# <title>

body …

---
출처: <original URL> · 수집 <ISO-8601> · sha256:<short hash>
```

## Legal Data Lookup Priority

When searching for statutes, precedents, administrative rules, or local ordinances,
follow this fixed priority order. **Stop at the first tier that returns adequate data.**

| Tier | Source | Covers |
| --- | --- | --- |
| 1 — Local clone | `data/legalize-kr/kr/{법령명}/` | Statutes · decrees · enforcement rules |
|  | `data/precedent-kr/{사건종류}/{법원등급}/` | Precedents |
|  | `data/admrule-kr/{기관경로}/{종류}/` | Administrative rules (notices · directives) |
|  | `data/ordinance-kr/{광역}/{기초}/{종류}/` | Local ordinances · regulations |
| 2 — `legalize-kr` MCP | `legalize-kr` MCP tools (`laws_*`, `precedents_*`, `admrules_*`, `ordinances_*`) | Same scope as above, via MCP when configured |
| 3 — Web | `law.go.kr`, `elis.go.kr`, court sites, web search | Official sources when local and MCP are insufficient |

### Bootstrap — missing `data/*-kr/` folders

If any `data/*-kr/.git` directory does not exist:

1. Inform the user that the legal-data clones are missing.
2. Suggest running **one** of the following to set them up:
   - VS Code Task: `civic: fetch legalize-kr repos (shallow clone)`
   - PowerShell: `pwsh -ExecutionPolicy Bypass -File scripts/fetch_legalize_kr.ps1`
   - Bash: `bash scripts/fetch_legalize_kr.sh`
3. While the clone is pending or unavailable, fall back to Tier 2 (MCP) or Tier 3 (Web).

### Ordinance region scope

When querying `data/ordinance-kr/` or `legalize-kr` MCP `ordinances_*`:

- MUST read `location.txt` first to determine the target metropolitan / municipality.
- MUST restrict search paths to `data/ordinance-kr/{광역}/{기초}/` matching the location.
- MUST NOT reference ordinances from regions outside the location unless the user explicitly requests a different region.

## Tool Priority

1. MCP servers (`legalize-kr`, `notebooklm`) — unified citation · hash · data access.
2. Skill commands (`.agents/skills/`) — pass safety guards.
3. IDE built-ins (Copilot: `#fetch`, `#problems`; Claude Code: `WebFetch`, `Glob`, `Grep`).
4. Terminal / Bash — only pre-approved patterns may run unattended.

## Architecture

```
Copilot CLI / VS Code Chat / Codex CLI / Claude Code CLI
                    │
        agents/*  +  skills/*  +  commands/*
                    │
            MCP servers (legalize-kr, notebooklm)
                    │
    archive/raw → archive/processed → notebooks/<slug> → NotebookLM
```

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
| `retrospectives/` | Cumulative session retros. |
| `data/{legalize,precedent,admrule,ordinance}-kr/` | Shallow clones of legal data. |

Stack: **Node 24 LTS**, **Python 3.12+ (uv)**. JVM 11+ only when using `opendataloader-pdf`.

## Channel-Specific Reference

### GitHub Copilot CLI / VS Code Chat

- Agent definitions: `.github/agents/*.agent.md`
- Prompt templates: `.github/prompts/*.prompt.md`
- Hooks: `.github/hooks/copilot-cli-policy.json`
- Tool gating: `.vscode/settings.json` `chat.tools.terminal.autoApprove`
- MCP: `.vscode/mcp.json`
- See also: [.github/copilot-instructions.md](.github/copilot-instructions.md)

### OpenAI Codex CLI

- Agent definitions: `.codex/agents/*.toml`
- MCP config: `.codex/config.toml`

### Claude Code CLI

- Subagents: `.claude/agents/*.md` (lawyer, ordinance, researcher, persona-panel, minutes)
- Slash commands: `.claude/commands/*.md` (/retro, /brief, /persona-review, /collect, /health, /add-skill, /add-agent, /publish-notebook)
- Hooks in `.claude/settings.json`:
  - **SessionStart** → `scripts/session-start.ps1` (region + clone status banner)
  - **Stop** → `scripts/session-stop.ps1` (retro reminder)
  - **PreToolUse(Bash)** → `scripts/pre-tool-bash.ps1` (destructive command blocker)
- MCP: `.mcp.json`
- Env: Bedrock backend, Agent Teams, 10-min timeout

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
| local-budget-tracker | Municipal budget tracking by 編成目 |
| local-fund-manager | Memory-driven fund portfolio tracking (기금) |
| local-ordinance-processor | Ordinance 3-tier validation + semantic categorization |
| local-timeline-manager | Annual admin/legislative timeline |
| local-transport-tracker | Bus transit data aggregation |
| party-alignment-review | Party platform consistency check |
| persona-perspective-review | Synthetic citizen panel simulation |
| pii-mask | Korean PII anonymization |
| retrospective-writer | Session post-work documentation |
| search-night-care | Night-time hospital accessibility research |
| vscode-task-author | VS Code task entry creation |

## Forbidden

- NEVER modify or delete files in `archive/raw/`.
- NEVER include credentials or tokens in chat · logs · commits · artifacts.
- NEVER violate `robots.txt` or ignore rate limits.
- NEVER make assertions without a citation.

## Disputes · takedowns

- Process deletion requests within 24 hours and restrict access to the matching `archive/raw/` entry.
- Record only facts in `retrospectives/`.

## See also

- [.github/copilot-instructions.md](.github/copilot-instructions.md) — VS Code Chat specifics.
- [docs/security.md](docs/security.md) — security model · credentials.
- [docs/references-nemotron-personas.md](docs/references-nemotron-personas.md) — synthetic citizen personas (CC BY 4.0).
