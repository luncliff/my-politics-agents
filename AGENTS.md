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
- MUST preserve originals under `보관함/다운로드/<host>/` (immutable).
- Machine-derived source path segments such as hostnames or upstream dataset identifiers MAY remain in their original language/script under `보관함/다운로드/`.
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
- Originals stay in `보관함/다운로드/` for personal review only — NEVER share.

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

- For any new site or format, preserve the original in `보관함/다운로드/` first.
- If the same task happens twice, log it as a **skill candidate** in the retro.
- If a domain persona appears twice, log it as an **agent candidate**.

### Session end (mandatory retro)

Call the `retrospective-writer` skill (Copilot/Codex) or `/retro` command (Claude Code).
Save to `회고/YYYY-MM-DD <slug>.md`:

- What was tried · what worked · what blocked.
- New sites · formats · policies discovered.
- Automation candidates (skill / agent / task / hook).
- Any missing citations or PII leaks — fix immediately.

## Output Formats

### File naming

- MUST use **Korean filenames** for user-facing generated Korean documents under `보관함/결과/`, `보관함/양식/`, `data/processed/`, `notebooks/`, `회고/`, and similar artifact folders.
- MUST use `<YYYY-MM> <한글 파일명>.md` as the default filename shape for processed Korean Markdown unless a narrower instruction explicitly overrides it.
- Use Korean filename for human readers. Use English for machine files (code, metadata, logs, tool configurations).
- Source-derived machine path segments under `보관함/다운로드/` are exempt from the Korean filename rule.

### File organization

- MUST keep default user-facing reports in `보관함/결과/` **flat** (no topic subfolders).
- MAY use subfolders under `보관함/결과/` only when an existing repo rule or skill explicitly requires structured machine-readable grouping (for example dataset, panel, legal-review, or timeline paths).
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

## Forbidden

- NEVER modify or delete files in `보관함/다운로드/`.
- NEVER include credentials or tokens in chat · logs · commits · artifacts.
- NEVER violate `robots.txt` or ignore rate limits.
- NEVER make assertions without a citation.

## Disputes · takedowns

- Process deletion requests within 24 hours and restrict access to the matching `보관함/다운로드/` entry.
- Record only facts in `회고/`.

## See also

- [docs/dev/architecture.md](docs/dev/architecture.md) — directory map, agents/skills lists, stack.
- [docs/dev/channels.md](docs/dev/channels.md) — channel-specific configuration (Copilot / Codex / Claude Code).
- [docs/dev/security.md](docs/dev/security.md) — security model · credentials.
- [docs/references/](docs/references/) — LLM-friendly reference documents.
- [.agents/CONVENTIONS.md](.agents/CONVENTIONS.md) — naming rules (verb-noun skills, noun agents).
