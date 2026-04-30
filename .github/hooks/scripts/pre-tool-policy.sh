#!/usr/bin/env bash
# pre-tool-policy.sh — preToolUse 정책 (logging-first, 데모 deny 1개)
set -eu

LOG_DIR=".github/hooks/logs"
mkdir -p "$LOG_DIR"
ts="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

tool="${COPILOT_TOOL_NAME:-unknown}"
cmd="${COPILOT_TOOL_COMMAND:-}"

printf '{"ts":"%s","tool":"%s","cmd":%s}\n' \
  "$ts" "$tool" "$(printf '%s' "$cmd" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))' 2>/dev/null || printf '"%s"' "$cmd")" \
  >> "$LOG_DIR/tool-use.jsonl"

# --- 데모 deny: 환경변수로만 활성화 ---
if [ "${COPILOT_HOOKS_DENY_DEMO:-0}" = "1" ]; then
  case "$cmd" in
    *"rm -rf /"*|*"mkfs"*|*"dd if="*)
      echo "[hook] denied by policy: $cmd" >&2
      exit 2
      ;;
  esac
fi

# 기본 정책: 차단 없음. 운영 단계에서 위 case에 deny 패턴을 추가하세요.
exit 0
