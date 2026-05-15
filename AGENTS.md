# AGENTS.md

Narrower scope wins: `applyTo` `.instructions.md` > sub-folder `AGENTS.md` > this file.

## Mission

Korean local-politics information pipeline: **collect → process → publish**, with citations at every step.

## Repository Map

| Path | AGENTS.md | Purpose |
| --- | --- | --- |
| `.agents/` | [.agents/AGENTS.md](.agents/AGENTS.md) | Skill / agent conventions, retrospective duty |
| `.codex/`, `.claude/` | — | Channel-specific configs (see [문서/channels.md](문서/channels.md)) |
| `tools/` | [tools/AGENTS.md](tools/AGENTS.md) | MCP servers, JS/Python adapters, lint configs |
| `scripts/` | [scripts/AGENTS.md](scripts/AGENTS.md) | Setup, fetch, hooks, lint helpers |
| `문서/` | [문서/AGENTS.md](문서/AGENTS.md) | Flat documentation set |
| `보관함/` | [보관함/AGENTS.md](보관함/AGENTS.md) | Originals, processed results, output formats, legal-data lookup priority |
| `data/`, `notebooks/` | — | Datasets and notebooks (see [문서/architecture.md](문서/architecture.md)) |
| `회고/` | — | Session retrospectives (`YYYY-MM-DD <slug>.md`) |
| `location.txt` | — | Current working region; read at session start |

## Key Rules

### Workspace-local

- MUST keep all settings, credentials, and caches inside this repo folder.
- MUST ask before any global change (`npm i -g`, `git config --global`, edits to `~/.copilot/*`, `~/.claude/*`).
- NEVER touch `~/.aws`, `~/.ssh`, OS keychains.

### Citation

- MUST attach **source URL · `collected_at` (ISO-8601 KST) · SHA-256** to every artifact derived from external data.
- MUST preserve originals under `보관함/다운로드/<host>/` (immutable). Do NOT prefix filenames with dates; track time via `.meta.json`.

### PII

- MUST run `pii-mask` skill before saving or sharing any text that may contain PII.
- NEVER persist masking keys to disk (memory only).
- Originals stay in `보관함/다운로드/` for personal review only — NEVER share.

### Political neutrality

- MUST split outputs about parties · candidates · individuals into **Facts** (cited primary sources) and **Interpretation** (reasoning).
- Every Facts item MUST carry a source link.

### Licensing (defaults; verify per source)

| Source | Default license | Note |
| --- | --- | --- |
| `law.go.kr` statutes | Public domain | Free reuse. |
| Bills · minutes (Assembly · councils) | Mostly KOGL Type 1 | Verify per site. |
| Notices · announcements | KOGL Type 1–4 | Type 4 non-commercial only. |
| Citizen content (blogs · SNS) | Author copyright | Need consent for direct quotes. |

When unsure, treat as **redistribution forbidden** — summarize and analyze only.

### Safe automation

- NEVER use `Bypass Approvals`, `Autopilot`, `/yolo`, or unattended destructive commands.
- New tools / domains MUST be approved before being added to auto-approve lists.
- Destructive commands (`rm -rf`, `git push --force`, `mkfs`, `dd`, `curl|bash`) MUST require human confirmation.
- MUST honor `robots.txt` and rate limits (max 1 req/sec per host). If ToS forbids scraping, STOP and ask.

### Forbidden

- NEVER modify or delete files in `보관함/다운로드/`.
- NEVER include credentials or tokens in chat · logs · commits · artifacts.
- NEVER make assertions without a citation.

## Workflow

### Session start

1. Read `location.txt` — determine current region.
2. Verify `보관함/*-kr/.git` exists; if missing, suggest fetch scripts (see [보관함/AGENTS.md](보관함/AGENTS.md)).
3. Summarize intent in one line; list affected directories.
4. Confirm risk · scope · expected artifacts with the user.

### During the session

- Preserve any new-format original in `보관함/다운로드/` first.
- If the same task recurs, log a **skill candidate** in the retro.
- If a domain persona recurs, log an **agent candidate**.

### Session end (mandatory retro)

Call `retrospective-writer` skill (Copilot/Codex) or `/retro` (Claude Code). Save to `회고/YYYY-MM-DD <slug>.md`:

- Tried / worked / blocked.
- New sites · formats · policies discovered.
- Automation candidates (skill / agent / task / hook).
- Missing citations or PII leaks — fix immediately.

## Disputes · takedowns

- Process deletion requests within 24 hours; restrict access to the matching `보관함/다운로드/` entry.
- Record only facts in `회고/`.

## See also

- [문서/architecture.md](문서/architecture.md) — directory map, agents/skills lists, stack.
- [문서/channels.md](문서/channels.md) — Copilot / Codex / Claude Code channels.
- [문서/security.md](문서/security.md) — security model · credentials.
- [.agents/CONVENTIONS.md](.agents/CONVENTIONS.md) — naming rules.
