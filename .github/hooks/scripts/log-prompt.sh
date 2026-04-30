#!/usr/bin/env bash
# log-prompt.sh — userPromptSubmitted 로그 (메타데이터만, 본문 저장 안 함)
set -eu

LOG_DIR=".github/hooks/logs"
mkdir -p "$LOG_DIR"
ts="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
cwd="$(pwd)"

# 본문은 기록하지 않는다. 길이만 기록.
read -r len <<<"${COPILOT_PROMPT_LENGTH:-0}"

printf '{"ts":"%s","cwd":"%s","prompt_len":%s}\n' "$ts" "$cwd" "${len:-0}" \
  >> "$LOG_DIR/audit.jsonl"

exit 0
