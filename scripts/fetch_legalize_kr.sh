#!/usr/bin/env bash
# scripts/fetch_legalize_kr.sh — Shallow clone legalize-kr repos to 보관함/
set -eu

DRY_RUN=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    *) echo "unknown arg: $arg"; exit 2 ;;
  esac
done
export DRY_RUN

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "$SCRIPT_DIR/common.sh"

cd "$(repo_root)"

DATA_DIR="보관함"
REPOS=(
  "legalize-kr|https://github.com/legalize-kr/legalize-kr.git"
  "precedent-kr|https://github.com/legalize-kr/precedent-kr.git"
  "admrule-kr|https://github.com/legalize-kr/admrule-kr.git"
  "ordinance-kr|https://github.com/legalize-kr/ordinance-kr.git"
)

if [ "$DRY_RUN" = "1" ]; then
  for repo in "${REPOS[@]}"; do
    name="${repo%%|*}"
    url="${repo##*|}"
    info "(dry-run) would shallow clone $url into $DATA_DIR/$name"
  done
  exit 0
fi

mkdir -p "$DATA_DIR"

for repo in "${REPOS[@]}"; do
  name="${repo%%|*}"
  url="${repo##*|}"
  target="$DATA_DIR/$name"

  if [ -d "$target/.git" ]; then
    warn "already exists: $target"
    continue
  fi

  if [ -e "$target" ]; then
    warn "target exists (not a git repo): $target"
    continue
  fi

  git clone --depth 1 "$url" "$target"
  ok "ready: $target"
done
