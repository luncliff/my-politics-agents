#!/usr/bin/env bash
# scripts/auth-purge.sh — 자격증명·세션 정리 (macOS / Linux)
set -eu

DRY_RUN=0
for arg in "$@"; do
  case "$arg" in --dry-run) DRY_RUN=1 ;; esac
done
export DRY_RUN

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "$SCRIPT_DIR/lib/common.sh"

info "my-politics-agents auth-purge"
warn "이 스크립트는 자격증명을 삭제할 수 있습니다. 각 단계는 별도 확인을 받습니다."

if confirm "gh CLI 로그아웃 (github.com)?"; then
  if have gh; then gh auth logout --hostname github.com; else warn "gh 미설치"; fi
fi

if confirm "워크스페이스의 .copilot/credentials* 파일 삭제?"; then
  find .copilot -maxdepth 1 -name 'credentials*' -print -delete 2>/dev/null || true
fi

if confirm "사용자 홈의 ~/.copilot/credentials* 파일 삭제?"; then
  find "$HOME/.copilot" -maxdepth 1 -name 'credentials*' -print -delete 2>/dev/null || true
fi

info "현재 셸의 토큰성 환경변수 (값은 표시하지 않음):"
for v in GH_TOKEN GITHUB_TOKEN OPENAI_API_KEY ANTHROPIC_API_KEY; do
  if [ -n "${!v:-}" ]; then echo "  set: $v"; else echo "  unset: $v"; fi
done

if is_macos && confirm "macOS 키체인의 'github.com' 항목 나열?"; then
  security find-internet-password -s github.com 2>/dev/null || true
  warn "삭제는 'security delete-internet-password -s github.com' 으로 직접 실행하세요."
fi

echo
ok "완료. VS Code에서 'Chat: Reset Tool Confirmations'도 한 번 실행하세요."
