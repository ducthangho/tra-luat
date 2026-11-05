#!/usr/bin/env bash
# Source this file from ~/.bashrc or an interactive Bash shell:
#   source /path/to/tra-luat/ops/environment/login-linux.sh
# It only prepends existing user CLI directories to PATH and sets TL_REPO for this shell.
# It never installs software, edits profiles, logs in, or reads/stores TL_MASTER_KEY.
if [ -z "${BASH_VERSION:-}" ]; then
  echo 'login-linux.sh requires Bash; source it from ~/.bashrc, not from a POSIX sh profile.' >&2
  # shellcheck disable=SC2317  # exit is reached only when this file was executed by sh, not sourced
  return 2 2>/dev/null || exit 2
fi
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  echo 'login-linux.sh must be sourced, not executed: source ops/environment/login-linux.sh' >&2
  exit 2
fi
_tl_env_repo="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)" || {
  echo 'login-linux.sh: cannot resolve repository root' >&2; unset _tl_env_repo; return 2; }
for _tl_env_dir in "$HOME/.local/bin" "$HOME/.local/share/tra-luat-tools/venv/bin"; do
  if [[ -d "$_tl_env_dir" && ":$PATH:" != *":$_tl_env_dir:"* ]]; then PATH="$_tl_env_dir:$PATH"; fi
done
export PATH
export TL_REPO="$_tl_env_repo"
printf 'tra-luat session: %s\n' "$TL_REPO"
printf 'Check: bash ops/environment/update-linux.sh --repo .\n'
printf 'Health: python scripts/tl.py doctor --offline\n'
unset _tl_env_repo _tl_env_dir
