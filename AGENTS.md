# AGENTS.md

Common rules for **GitHub Copilot CLI** and **VS Code Copilot Chat** in this repo.
A narrower scope wins: `applyTo` `.instructions.md` > `agents/` > this file.

## Mission

Build a trusted information pipeline for Korean local politics:
**collect → process → publish**, with citations attached at every step.

## Core Rules

### Workspace-local

- MUST keep all settings, credentials, and caches inside this repo folder.
- MUST ask before any global change (`npm i -g`, `git config --global`, edits to `~/.copilot/*`, etc.).
- NEVER touch `~/.aws`, `~/.ssh`, OS keychains. Tell the user to do it.

### Citation

- MUST include **source URL · collected_at (ISO-8601 KST) · SHA-256** in every artifact derived from external data.
- MUST preserve originals under `archive/raw/<host>/` (immutable).
- MUST use `gov-archive` MCP `archive_cite` to generate citation metadata.
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

- NEVER use `Bypass Approvals`, `Autopilot`, `/yolo`, or `chat.tools.global.autoApprove`.
- New tools or domains MUST be approved explicitly before being added to auto-approve lists.
- Destructive commands (`rm -rf`, `git push --force`, `mkfs`, `dd`, `curl|bash`) MUST require human confirmation.
- MUST honor `robots.txt` and rate limits (max 1 req/sec per host).
- If a site's ToS forbids scraping, STOP and ask the user.

## Workflow

### Session start

1. Copilot CLI hooks print the policy banner.
2. Summarize intent in one line and list affected directories.
3. Confirm risk · scope · expected artifacts with the user.

### During the session

- For any new site or format, MUST call `archive_fetch` first to preserve the original.
- If the same task happens twice, log it as a **skill candidate** in the retro.
- If a domain persona appears twice, log it as an **agent candidate**.

### Session end (mandatory retro)

Call `retrospective-writer` skill. Save to `retrospectives/YYYY-MM-DD-<slug>.md`:

- What was tried · what worked · what blocked.
- New sites · formats · policies discovered.
- Automation candidates (skill / agent / task / hook).
- Any missing citations or PII leaks — fix immediately.

## Output Formats

### File naming

- MUST use **Korean filenames** for user-facing generated Korean documents under `archive/processed/`, `data/processed/`, `notebooks/`, `retrospectives/`, and similar artifact folders.
- MUST use `<YYYY-MM> <한글 파일명>.md` as the default filename shape for processed Korean Markdown unless a narrower instruction explicitly overrides it. (ex. `2026-04 경기도 환승센터 교통사업 프로세스.md`, `2026-04 경기도 성남시 초등교육 및 아동지원 예산결산 분석.md`)
- Use Korean filename for human readers and reviewers. But use English for machine files(code, metadata, logs, tool configurations, etc.) to avoid encoding issues.

### File organization

- MUST keep `archive/processed/` **flat**. Store generated files directly under `archive/processed/` and do **not** create topic subfolders such as `archive/processed/transport/`.
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

### NotebookLM bundle

`notebooks/<slug>/manifest.yml` — schema in [notebooks/README.md](notebooks/README.md).

### Retrospective

`retrospectives/YYYY-MM-DD-<slug>.md` — template from `retrospective-writer`.

## Tool Priority

1. Workspace-local MCP servers (`mcp-servers/*`) — unified citation · hash · logging.
2. Skill commands — pass safety guards.
3. VS Code built-ins (`#fetch`, `#problems`, `#codebase`).
4. Terminal — only patterns in `chat.tools.terminal.autoApprove` may run unattended.

When approaching the 128-tool limit, group via `Tool Sets` (`.vscode/toolsets.jsonc`).

## Architecture (one diagram)

```
Copilot CLI / VS Code Chat
        │
   agents/*  +  skills/*
        │
   MCP servers (mcp-servers/*)
        │
archive/raw → archive/processed → notebooks/<slug> → NotebookLM
```

| Path | Responsibility |
| --- | --- |
| `agents/` | Domain personas. |
| `.agents/skills/` | Single-purpose reusable tasks. |
| `.github/prompts/` | Prompt templates. |
| `.github/hooks/` | Copilot CLI policy · logging. |
| `.vscode/` | IDE settings · tasks · MCP · toolsets. |
| `scripts/` | Setup · auth purge. |
| `mcp-servers/` | Workspace-local MCP servers. |
| `adapters/` | Per-site collectors (JS/Py). |
| `archive/` | Originals + processed. |
| `notebooks/` | NotebookLM bundles. |
| `retrospectives/` | Cumulative session retros. |
| `data/{legalize,precedent,admrule,ordinance}-kr/` | Shallow clones of legal data. |

Stack: **Node 24 LTS**, **Python 3.12+ (uv)**. JVM 11+ only when using `opendataloader-pdf`.

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
