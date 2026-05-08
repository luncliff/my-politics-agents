#!/usr/bin/env bash
# scripts/fetch_legalize_kr.sh — Shallow clone legalize-kr to data/legalize-kr
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
. "$SCRIPT_DIR/lib/common.sh"

cd "$(repo_root)"

REPO_URL="https://github.com/legalize-kr/legalize-kr.git"
DATA_DIR="data"
TARGET_DIR="$DATA_DIR/legalize-kr"

if [ "$DRY_RUN" = "1" ]; then
  info "(dry-run) would shallow clone $REPO_URL into $TARGET_DIR"
  exit 0
fi

mkdir -p "$DATA_DIR"

if [ -d "$TARGET_DIR/.git" ]; then
  warn "already exists: $TARGET_DIR"
  exit 0
fi

if [ -e "$TARGET_DIR" ]; then
  warn "target exists (not a git repo): $TARGET_DIR"
  exit 0
fi

git clone --depth 1 "$REPO_URL" "$TARGET_DIR"

ok "legalize-kr ready at $TARGET_DIR"
