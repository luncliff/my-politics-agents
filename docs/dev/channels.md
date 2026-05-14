# Channel-Specific Reference

## GitHub Copilot CLI / VS Code Chat

- Agent definitions: `.github/agents/*.agent.md`
- Prompt templates: `.github/prompts/*.prompt.md`
- Hooks: `.github/hooks/copilot-cli-policy.json`
- Tool gating: `.vscode/settings.json` `chat.tools.terminal.autoApprove`
- MCP: `.vscode/mcp.json`
- See also: [.github/copilot-instructions.md](../../.github/copilot-instructions.md)

## OpenAI Codex CLI

- Agent definitions: `.codex/agents/*.toml`
- MCP config: `.codex/config.toml`

## Claude Code CLI

- Subagents: `.claude/agents/*.md` (lawyer, ordinance, researcher, persona-panel, minutes)
- Slash commands: `.claude/commands/*.md` (/retro, /brief, /persona-review, /collect, /health, /diagnose-prompts)
- Hooks in `.claude/settings.json`:
  - **SessionStart** → `scripts/session-start.ps1` (region + clone status + feedback banner)
  - **Stop** → `scripts/session-stop.ps1` (retro reminder)
  - **PreToolUse(Bash)** → `scripts/pre-tool-bash.ps1` (destructive command blocker)
- MCP: `.mcp.json`
- Env: Bedrock backend, Agent Teams, 10-min timeout
