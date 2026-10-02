#!/usr/bin/env bash
set -euo pipefail

target="codex"
custom_path=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --target) target="${2:?}"; shift 2 ;;
    --path) custom_path="${2:?}"; shift 2 ;;
    -h|--help) echo "Usage: ./uninstall.sh [--target codex|claude|agents|gemini|openclaw|portable|custom|all] [--path DIR]"; exit 0 ;;
    *) echo "ERROR: unknown argument: $1" >&2; exit 2 ;;
  esac
done

case "${target}" in codex|claude|agents|gemini|openclaw|portable|custom|all) ;; *) echo "ERROR: invalid target" >&2; exit 2 ;; esac
if [ "${target}" = "custom" ] && [ -z "${custom_path}" ]; then
  echo "ERROR: --target custom requires --path" >&2
  exit 2
fi
base_home="${ANTI_SLOP_BRAIN_INSTALL_HOME:-${HOME}}"

target_dir() {
  case "$1" in
    codex) echo "${base_home}/.codex/skills/anti-slop-brain" ;;
    claude) echo "${base_home}/.claude/skills/anti-slop-brain" ;;
    agents) echo "${base_home}/.agents/skills/anti-slop-brain" ;;
    openclaw) echo "${base_home}/.openclaw/skills/anti-slop-brain" ;;
    portable) echo "${base_home}/.agent-skills/anti-slop-brain" ;;
    custom) echo "${custom_path%/}/anti-slop-brain" ;;
  esac
}

remove_one() {
  local dir="$1"
  if [ -d "${dir}" ]; then
    rm -rf "${dir}"
    echo "Removed ${dir}"
  else
    echo "Anti-Slop Brain is not installed at ${dir}"
  fi
}

# The Gemini loader cleanup is the only step that needs an interpreter, so
# resolve one lazily rather than at startup: --help must still work on a machine
# with no Python at all. Prefer python3. macOS has not shipped a bare `python`
# since Monterey removed the Python 2 stub, so hardcoding it fails with 127,
# which would strand the loader block in GEMINI.md after an uninstall.
resolve_python() {
  if [ -n "${PYTHON:-}" ]; then
    return
  fi
  local candidate
  for candidate in python3 python; do
    if command -v "${candidate}" >/dev/null 2>&1 &&
       "${candidate}" -c 'import sys; sys.exit(0 if sys.version_info[0] == 3 else 1)' >/dev/null 2>&1; then
      PYTHON="${candidate}"
      return
    fi
  done
  echo "ERROR: no Python 3 interpreter on PATH. Looked for python3, then python." >&2
  exit 1
}

remove_gemini() {
  local dir="${base_home}/.gemini/anti-slop-brain"
  local loader="${base_home}/.gemini/GEMINI.md"
  remove_one "${dir}"
  if [ -f "${loader}" ]; then
    resolve_python
    "${PYTHON}" - "${loader}" <<'PY'
from __future__ import annotations

import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
start = "<!-- anti-slop-brain-install:start -->"
end = "<!-- anti-slop-brain-install:end -->"
text = path.read_text(encoding="utf-8")
pattern = f"\n*{re.escape(start)}.*?{re.escape(end)}\n*"
new_text = re.sub(pattern, "\n", text, flags=re.S).strip()
if new_text:
    path.write_text(new_text + "\n", encoding="utf-8")
else:
    path.unlink()
PY
    echo "Anti-Slop Brain Gemini loader cleaned at ${loader}"
  fi
}

if [ "${target}" = "all" ]; then
  for name in codex claude agents openclaw portable; do
    remove_one "$(target_dir "${name}")"
  done
  remove_gemini
elif [ "${target}" = "gemini" ]; then
  remove_gemini
else
  remove_one "$(target_dir "${target}")"
fi
