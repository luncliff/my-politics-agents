#!/usr/bin/env bash
# scripts/lib/common.sh — POSIX 공용 헬퍼 (bash/zsh)
set -eu

c_reset='\033[0m'; c_bold='\033[1m'; c_yellow='\033[33m'; c_green='\033[32m'; c_red='\033[31m'

log()    { printf "%b\n" "$*"; }
info()   { printf "${c_bold}[info]${c_reset} %s\n" "$*"; }
warn()   { printf "${c_yellow}[warn]${c_reset} %s\n" "$*"; }
error()  { printf "${c_red}[err ]${c_reset} %s\n" "$*" >&2; }
ok()     { printf "${c_green}[ok  ]${c_reset} %s\n" "$*"; }

have() { command -v "$1" >/dev/null 2>&1; }

# confirm "Question?" → 0 if yes, 1 otherwise. Auto-no in DRY_RUN.
confirm() {
  local q="$1"
  if [ "${DRY_RUN:-0}" = "1" ]; then
    info "(dry-run) would ask: $q"
    return 1
  fi
  if [ "${ASSUME_YES:-0}" = "1" ]; then
    info "(--yes) auto-accept: $q"
    return 0
  fi
  printf "%s [y/N] " "$q"
  read -r ans || ans=""
  case "$ans" in y|Y|yes|YES) return 0 ;; *) return 1 ;; esac
}

is_macos() { [ "$(uname -s)" = "Darwin" ]; }
is_linux() { [ "$(uname -s)" = "Linux" ]; }

repo_root() {
  git rev-parse --show-toplevel 2>/dev/null || pwd
}
