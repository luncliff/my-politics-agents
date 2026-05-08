# Security Policy

## Supported Versions

This repository contains documentation, scripts, and agent configuration — not a versioned software library.
Security fixes are applied to the `main` branch only.

| Branch | Supported |
| --- | --- |
| `main` | ✅ |
| any other | ❌ |

## Reporting a Vulnerability

**Do not open a public issue for security vulnerabilities.**

Report privately via [GitHub Security Advisories](https://github.com/luncliff/my-politics-agents/security/advisories/new) or email the repository owner (see profile).

Include:
- Description of the vulnerability and affected component.
- Steps to reproduce or a proof-of-concept.
- Potential impact (credential leak, data exposure, prompt injection, etc.).

You will receive an acknowledgement within **72 hours** and a resolution or mitigation plan within **7 days**.
Deletion requests for accidentally exposed personal data are processed within **24 hours**.

## Threat Model

| Threat | Mitigation |
| --- | --- |
| Credential / token leak | `.env`, `*.token`, `.copilot/credentials*` in `.gitignore`; [gitleaks](https://github.com/gitleaks/gitleaks) scans every push and PR (`.github/workflows/gitleaks.yml`) |
| Prompt injection from external pages | `*.go.kr/*` URLs: request auto-approved, **response requires human review** (`approveResponse: false` in `chat.tools.urls.autoApprove`) |
| Unintended global system changes | `scripts/setup.*` and Copilot CLI hooks gate every global change behind explicit consent |
| Unattended destructive commands | `Bypass Approvals` / `Autopilot` / `/yolo` disabled; `preToolUse` hook blocks known destructive patterns |
| Arbitrary external domain calls | `chat.agent.networkFilter` domain whitelist + explicit approval flow for new domains |
| PII in artifacts | `pii-mask` skill is mandatory before any artifact is saved or shared |
| Dependency vulnerabilities | Dependabot alerts enabled; `pyproject.toml` + `package.json` dependency graph monitored |

## Workspace-local Principle

All settings, credentials, and caches MUST stay inside this repository folder.

| Asset | Location | Global? |
| --- | --- | --- |
| Copilot CLI config | `.copilot/` (workspace) | `~/.copilot/` used only with consent |
| MCP server definitions | `.vscode/mcp.json` | Global `mcp.json` MUST NOT be modified |
| Prompts / skills / agents | `.github/prompts/`, `.agents/skills/`, `agents/` | User prompts folder is opt-in only |
| Node packages | repo `node_modules/` | `npm install -g` only in setup, with consent |
| Python environment | `.venv/` (uv) | `uv tool install --global` is opt-in |
| Git config | `.git/config` | `git config --global` only with consent |

## GitHub Actions Security

### Active workflows

| Workflow | Trigger | Purpose |
| --- | --- | --- |
| `gitleaks.yml` | push to `main`, PRs | Scans entire git history for leaked secrets |
| `lint.yml` | push to `main`, PRs | Validates YAML frontmatter and JSON syntax in agent/skill/prompt files |

### Hardening practices applied

- `actions/checkout@v4` with `fetch-depth: 0` for full-history secret scanning.
- `GITHUB_TOKEN` is the only secret injected into workflows; no long-lived personal access tokens.
- No `pull_request_target` triggers (prevents fork-based privilege escalation).
- No `workflow_dispatch` with unvalidated inputs.
- Third-party Actions pinned to major version tags (`@v4`, `@v5`); review before bumping.

### Recommended additions (not yet active)

- **CodeQL default setup** — enable under *Settings → Advanced Security → CodeQL analysis* for JavaScript/TypeScript and Python scanning.
- **Dependabot version updates** — add `.github/dependabot.yml` to keep `actions/` and `pip`/`uv` dependencies current.
- **Secret scanning push protection** — enable under *Settings → Advanced Security → Secret Protection* to block commits containing known secret patterns.
- **Branch protection on `main`** — require PR review + passing `gitleaks` and `lint` checks before merge.

## URL Auto-approval Policy

Defined in `.vscode/settings.json` under `chat.tools.urls.autoApprove`:

- `*.go.kr/*` (government portals): **request auto-approved, response always reviewed by a human** — defends against user-generated content prompt injection.
- `docs.github.com`, `code.visualstudio.com`, `modelcontextprotocol.io`: both directions auto-approved (trusted OSS documentation).
- `pastebin.com`, `*.ngrok.io`, and similar: explicitly blocked (`false`).

Reset all approvals: `Ctrl+Shift+P` → `Chat: Reset Tool Confirmations`.
Review individual approvals: `Chat: Manage Tool Approval`.

## Credential Cleanup

Run interactively (non-interactive mode is intentionally disabled):

```pwsh
# Windows
pwsh -File scripts/auth-purge.ps1
```

```zsh
# macOS
zsh scripts/auth-purge.sh
```

Covers: `gh auth logout`, `.copilot/credentials*`, shell profile environment variable audit, Windows Credential Manager, macOS Keychain, NotebookLM MCP token/session files.

## Copilot CLI Hooks

`.github/hooks/copilot-cli-policy.json` registers:

| Hook | Action |
| --- | --- |
| `sessionStart` | Prints the policy banner |
| `userPromptSubmitted` | Logs timestamp + cwd to `.github/hooks/logs/audit.jsonl` (gitignored) |
| `preToolUse` | Blocks/warns on destructive patterns; demo deny via `COPILOT_HOOKS_DENY_DEMO` |

Default policy is **logging-first**. Harden deny patterns in `pre-tool-policy.{sh,ps1}` incrementally for production use.

## Code Scanning Alerts

This repository uses [gitleaks](https://github.com/gitleaks/gitleaks) for secret scanning on every push and PR.
If CodeQL default setup is enabled, alerts will appear in *Security → Code scanning alerts*.

Alert severity mapping (CodeQL):

| Security severity | CVSS range | Action |
| --- | --- | --- |
| Critical | 9.0–10.0 | Block PR merge; fix immediately |
| High | 7.0–8.9 | Fix before next release |
| Medium | 4.0–6.9 | Triage within 7 days |
| Low | 0.1–3.9 | Address in backlog |

Alerts labeled **Test** or **Library** may be dismissed after review. Alerts labeled **Generated** require human judgment.

## Forbidden (always)

- NEVER commit credentials, tokens, or API keys to any branch.
- NEVER use `git push --force` on `main`.
- NEVER disable `gitleaks` or `lint` workflows without a documented reason.
- NEVER process PII outside the `pii-mask` skill boundary.
- NEVER store masking keys on disk.
