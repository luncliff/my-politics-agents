#!/usr/bin/env bash
# scripts/setup.sh — my-politics-agents 환경 설정 (macOS / Linux)
set -eu

DRY_RUN=0
ASSUME_YES=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --yes|-y)  ASSUME_YES=1 ;;
    *) echo "unknown arg: $arg"; exit 2 ;;
  esac
done
export DRY_RUN ASSUME_YES

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "$SCRIPT_DIR/lib/common.sh"

cd "$(repo_root)"
info "repo: $(pwd)"

# 1) detect
declare -a TOOLS=(git node gh copilot uv java)
echo
info "현재 도구 상태:"
for t in "${TOOLS[@]}"; do
  if have "$t"; then ok "$t"; else warn "miss: $t"; fi
done

# installer
INSTALLER=""
if is_macos; then
  if have brew; then INSTALLER="brew"; fi
elif is_linux; then
  if have apt-get; then INSTALLER="apt"; fi
fi

# 2) plan
echo
PLAN=()
have node    || PLAN+=("Node.js LTS")
have gh      || PLAN+=("GitHub CLI")
have uv      || PLAN+=("uv (Astral)")
have copilot || PLAN+=("Copilot CLI (npm i -g @github/copilot)")

if [ "${#PLAN[@]}" -eq 0 ]; then
  ok "추가 설치가 필요한 도구가 없습니다."
else
  info "다음 항목을 설치하려고 합니다:"
  for p in "${PLAN[@]}"; do echo "  - $p"; done
  if [ -z "$INSTALLER" ]; then
    warn "패키지 매니저(brew/apt-get)를 찾지 못했습니다. 위 항목을 수동으로 설치하세요."
  fi
fi

step() {
  local desc="$1"; shift
  if confirm "실행할까요? $desc"; then
    "$@" && ok "$desc"
  else
    warn "skip: $desc"
  fi
}

if [ -n "$INSTALLER" ] && ! have node; then
  if [ "$INSTALLER" = "brew" ]; then
    step "Node.js LTS 설치 (brew)" brew install node
  else
    step "Node.js LTS 설치 (apt)" sudo apt-get install -y nodejs npm
  fi
fi
if [ -n "$INSTALLER" ] && ! have gh; then
  if [ "$INSTALLER" = "brew" ]; then
    step "GitHub CLI 설치 (brew)" brew install gh
  else
    step "GitHub CLI 설치 (apt)" sudo apt-get install -y gh
  fi
fi
if [ -n "$INSTALLER" ] && ! have uv; then
  if [ "$INSTALLER" = "brew" ]; then
    step "uv 설치 (brew)" brew install uv
  else
    step "uv 설치 (curl|sh — 사용자 홈에만)" sh -c 'curl -LsSf https://astral.sh/uv/install.sh | sh'
  fi
fi
if ! have copilot; then
  step "Copilot CLI 전역 설치 (npm i -g @github/copilot)" npm install -g '@github/copilot'
fi

# 3) workspace
step "git submodule update --init --recursive" git submodule update --init --recursive

if [ -f "mcp-servers/gov-archive/pyproject.toml" ]; then
  step "uv sync (mcp-servers/gov-archive)" sh -c "cd mcp-servers/gov-archive && uv sync"
fi

if [ ! -f ".env" ]; then
  step ".env.example → .env 복사 (값은 직접 채우세요)" cp .env.example .env
fi

# 4) verify
echo
info "검증:"
for k in git node gh uv copilot; do
  if have "$k"; then ok "$k OK"; else warn "$k 누락"; fi
done

echo
ok "setup 완료. 다음 단계:"
echo "  1) gh auth login"
echo "  2) Tasks: Run Task → 'civic: copilot session'"
