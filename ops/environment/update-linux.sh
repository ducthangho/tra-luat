#!/usr/bin/env bash
# Shared baseline with Windows: ops/cong_cu.yaml and ops/cai_cong_cu.sh.
# Usage: bash ops/environment/update-linux.sh --repo /path/to/tra-luat [--apply [--user-only] [--persist-path]
#          [--latest [--tools claude,codex,agy,nlm,gws]]]
# Without --apply it only reports versions and the checker result (exit code = checker exit code).
# It reports only whether TL_* variables are set; it never prints their values or reads credential files.
set -euo pipefail
repo='' apply=0 latest=0 persist_path=0 user_only=0 selected='claude,codex,agy,nlm,gws'
while (($#)); do
  case "$1" in
    --repo) repo="${2:?missing repository}"; shift 2 ;;
    --apply) apply=1; shift ;;
    --latest) latest=1; shift ;;
    --persist-path) persist_path=1; shift ;;
    --user-only) user_only=1; shift ;;
    --tools) selected="${2:?missing tool list}"; shift 2 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done
if (( (latest || persist_path) && ! apply )); then
  echo '--latest and --persist-path require --apply' >&2; exit 2
fi
[[ -n "$repo" ]] || { echo '--repo is required' >&2; exit 2; }
# Validate the tool list before any mutation, not after earlier installs already ran.
IFS=, read -r -a requested_tools <<< "$selected"
for requested_tool in "${requested_tools[@]}"; do
  case "$requested_tool" in
    claude|codex|agy|nlm|gws|git|python|rg|shellcheck|gh|node|npm|pwsh|uv) : ;;
    *) echo "unknown tool: $requested_tool" >&2; exit 2 ;;
  esac
done
repo="$(cd -- "$repo" && pwd -P)"
for f in ops/cong_cu.yaml ops/cong_cu.py ops/cai_cong_cu.sh; do
  [[ -f "$repo/$f" ]] || { echo "missing $repo/$f" >&2; exit 2; }
done
case "$(uname -s)" in Linux*) : ;; *) echo 'Linux or WSL required' >&2; exit 4 ;; esac
native_command() {
  local p
  p="$(command -v "$1" 2>/dev/null || true)"
  [[ -n "$p" && "$p" != /mnt/* && "$p" != *.exe && "$p" != *.cmd ]]
}
# `python3 -m venv --help` succeeds even without python3-venv on Ubuntu; only ensurepip proves venv creation works.
venv_available() { python3 -c 'import ensurepip, venv' >/dev/null 2>&1; }
agy_version() {
  local output
  output="$(agy --version 2>/dev/null)" || return 1
  # AGY may print a banner and a separate version: line. Reject ambiguous/no version output.
  printf '%s\n' "$output" | "$py" -c 'import re,sys
pattern=r"\s*(?:version:\s*|agy\s+|antigravity\s+)?v?(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?)\s*"
versions=[m.group(1) for line in sys.stdin.read().splitlines() if (m:=re.fullmatch(pattern,line))]
if len(versions)!=1: sys.exit(1)
print(versions[0])'
}
install_agy_verified() {
  local release asset url digest tag archive tmp found
  case "$(uname -m)" in x86_64) asset=agy_cli_linux_x64.tar.gz ;; aarch64) asset=agy_cli_linux_arm64.tar.gz ;;
    *) echo 'Unsupported AGY CPU architecture' >&2; return 5 ;; esac
  release="$("$py" - <<'PY'
import json, urllib.request
req = urllib.request.Request('https://api.github.com/repos/google-antigravity/antigravity-cli/releases/latest', headers={'User-Agent':'tra-luat-env-setup'})
print(json.dumps(json.load(urllib.request.urlopen(req, timeout=30))))
PY
)"
  read -r tag url digest < <(printf '%s' "$release" | "$py" -c 'import json,sys; d=json.load(sys.stdin); a=[x for x in d["assets"] if x["name"]==sys.argv[1]]; assert len(a)==1; print(d["tag_name"],a[0]["browser_download_url"],a[0]["digest"])' "$asset")
  [[ "$digest" =~ ^sha256:[0-9a-f]{64}$ ]] || { echo 'AGY release has no valid SHA256 digest' >&2; return 5; }
  # Already at the release tag: nothing to do. Otherwise always reinstall from the verified asset;
  # `agy update` would bypass the SHA256 check.
  if native_command agy && [[ "$(agy_version || true)" == "${tag#v}" ]]; then return 0; fi
  tmp="$(mktemp -d)"; archive="$tmp/$asset"
  curl --fail --silent --show-error --location --proto '=https' --tlsv1.2 "$url" --output "$archive" ||
    { rm -rf -- "$tmp"; echo 'AGY download failed' >&2; return 5; }
  printf '%s  %s\n' "${digest#sha256:}" "$archive" | sha256sum --check --status || { rm -rf -- "$tmp"; echo 'AGY SHA256 mismatch' >&2; return 5; }
  found="$(tar -tzf "$archive")"
  [[ "$found" == 'antigravity' ]] || { rm -rf -- "$tmp"; echo 'Unexpected AGY archive layout' >&2; return 5; }
  tar -xOf "$archive" antigravity > "$tmp/agy"
  mkdir -p "$HOME/.local/bin"
  install -m 755 "$tmp/agy" "$HOME/.local/bin/agy"
  rm -rf -- "$tmp"
  hash -r
  [[ "$(command -v agy)" == "$HOME/.local/bin/agy" ]] || { echo 'AGY is shadowed on PATH' >&2; return 6; }
  [[ "$(agy_version)" == "${tag#v}" ]] || { echo "AGY did not reach $tag" >&2; return 6; }
}
if grep -qi microsoft /proc/version 2>/dev/null; then echo 'platform: WSL'; else echo 'platform: Linux'; fi
cd -- "$repo"
for name in TL_MASTER_KEY TL_SECRETS_FILEID TL_AGENT_CREDS_FILEID TL_WEBAPP TL_TOKEN TL_PROFILE; do
  if [[ -n "${!name:-}" ]]; then printf '%-23s set\n' "$name"; else printf '%-23s unset\n' "$name"; fi
done
if [[ -n "${TL_SECRETS_FILEID:-}" && -z "${TL_MASTER_KEY:-}" ]]; then
  echo 'Warning: secrets file ID is set but TL_MASTER_KEY is absent.' >&2
fi
if [[ -n "${TL_WEBAPP:-}" && -z "${TL_TOKEN:-}" ]] || [[ -z "${TL_WEBAPP:-}" && -n "${TL_TOKEN:-}" ]]; then
  echo 'Warning: only one of TL_WEBAPP/TL_TOKEN is set; verify config precedence.' >&2
fi
echo 'Secrets are not copied from Windows or written to shell profiles.'
if command -v python >/dev/null 2>&1; then py=python
elif command -v python3 >/dev/null 2>&1; then py=python3
else echo 'Python is required to read the shared tool manifest' >&2; exit 5
fi
for tool in git python bash rg shellcheck actionlint gh node npm pwsh uv claude codex agy nlm gws; do
  if command -v "$tool" >/dev/null 2>&1; then
    case "$tool" in actionlint) arg=-version ;; *) arg=--version ;; esac
    printf '%-12s %s\n' "$tool" "$("$tool" "$arg" 2>/dev/null | head -1 || true)"
  else printf '%-12s %s\n' "$tool" '(missing)'; fi
done
if (( ! apply )); then
  "$py" ops/cong_cu.py kiem-tra --json
  echo 'Check complete. Use --apply after related jobs finish.'
  exit 0
fi
command -v pgrep >/dev/null 2>&1 || { echo 'pgrep (procps) is required to check for active jobs before --apply' >&2; exit 3; }
if pgrep -x -u "$(id -u)" 'claude|codex|agy|nlm|gws|uv|node|python|python3' >/dev/null 2>&1; then
  echo 'Related tool/runtime processes are active; finish their jobs before updating.' >&2
  exit 3
fi
install_node_user() {
  local version file root tmp hash arch
  case "$(uname -m)" in x86_64) arch=x64 ;; aarch64) arch=arm64 ;; *) echo 'Unsupported Node CPU architecture' >&2; return 5 ;; esac
  version="$(python3 - <<'PY'
import json,urllib.request
d=json.load(urllib.request.urlopen('https://nodejs.org/dist/index.json',timeout=30))
print(next(x['version'] for x in d if x.get('lts')))
PY
)"
  file="node-${version}-linux-${arch}.tar.xz"; root="https://nodejs.org/dist/$version"
  tmp="$(mktemp -d)"
  if ! curl -fsSL --proto '=https' --tlsv1.2 "$root/$file" -o "$tmp/$file" ||
     ! curl -fsSL --proto '=https' --tlsv1.2 "$root/SHASUMS256.txt" -o "$tmp/SHASUMS256.txt"; then
    rm -rf -- "$tmp"; echo 'Node download failed' >&2; return 5
  fi
  hash="$(awk -v f="$file" '$2==f {print $1}' "$tmp/SHASUMS256.txt")"
  [[ "$hash" =~ ^[0-9a-f]{64}$ ]] || { rm -rf -- "$tmp"; echo 'Node SHA256 unavailable' >&2; return 5; }
  printf '%s  %s\n' "$hash" "$tmp/$file" | sha256sum --check --status || { rm -rf -- "$tmp"; echo 'Node SHA256 mismatch' >&2; return 5; }
  mkdir -p "$HOME/.local/share/tra-luat-tools/node" "$HOME/.local/bin"
  tar -xJf "$tmp/$file" -C "$HOME/.local/share/tra-luat-tools/node" --strip-components=1
  ln -sfnT "$HOME/.local/share/tra-luat-tools/node/bin/node" "$HOME/.local/bin/node"
  ln -sfnT "$HOME/.local/share/tra-luat-tools/node/bin/npm" "$HOME/.local/bin/npm"
  ln -sfnT "$HOME/.local/share/tra-luat-tools/node/bin/npx" "$HOME/.local/bin/npx"
  rm -rf -- "$tmp"
  hash -r
  if ! native_command node || ! native_command npm; then echo 'Native Node/npm not available after install' >&2; return 6; fi
}
install_gh_user() {
  local release name url digest tag tmp archive entry arch
  case "$(uname -m)" in x86_64) arch=amd64 ;; aarch64) arch=arm64 ;; *) echo 'Unsupported gh CPU architecture' >&2; return 5 ;; esac
  release="$(python3 - <<'PY'
import json,urllib.request
req=urllib.request.Request('https://api.github.com/repos/cli/cli/releases/latest',headers={'User-Agent':'tra-luat-env-setup'})
print(json.dumps(json.load(urllib.request.urlopen(req,timeout=30))))
PY
)"
  read -r tag name url digest < <(printf '%s' "$release" | python3 -c 'import json,sys,re; d=json.load(sys.stdin); arch=sys.argv[1]; a=[x for x in d["assets"] if re.fullmatch(r"gh_[0-9.]+_linux_"+arch+r"\.tar\.gz",x["name"])]; assert len(a)==1; print(d["tag_name"],a[0]["name"],a[0]["browser_download_url"],a[0]["digest"])' "$arch")
  [[ "$digest" =~ ^sha256:[0-9a-f]{64}$ ]] || { echo 'gh release SHA256 unavailable' >&2; return 5; }
  tmp="$(mktemp -d)"; archive="$tmp/$name"
  curl -fsSL --proto '=https' --tlsv1.2 "$url" -o "$archive" || { rm -rf -- "$tmp"; echo 'gh download failed' >&2; return 5; }
  printf '%s  %s\n' "${digest#sha256:}" "$archive" | sha256sum --check --status || { rm -rf -- "$tmp"; echo 'gh SHA256 mismatch' >&2; return 5; }
  entry="${name%.tar.gz}/bin/gh"
  tar -tzf "$archive" | grep -Fxq "$entry" || { rm -rf -- "$tmp"; echo 'gh binary missing from archive' >&2; return 5; }
  mkdir -p "$HOME/.local/bin"
  tar -xOf "$archive" "$entry" > "$tmp/gh"
  install -m 755 "$tmp/gh" "$HOME/.local/bin/gh"
  rm -rf -- "$tmp"; hash -r
  [[ "$(gh --version | awk 'NR==1 {print $3}')" == "${tag#v}" ]] || { echo "gh did not reach $tag" >&2; return 6; }
}
install_gws() {
  local target
  target="$(npm view @googleworkspace/cli version)"
  npm install -g --allow-scripts=@googleworkspace/cli "@googleworkspace/cli@$target" --no-fund --no-audit
  [[ "$(gws --version | awk 'NR==1 {print $NF}')" == "$target" ]] || { echo "gws did not reach $target" >&2; return 6; }
}
# shellcheck source=/dev/null
case "$(. /etc/os-release; echo "$ID")" in
  ubuntu) : ;;
  *) echo 'Automatic supplemental installation currently supports Ubuntu only' >&2; exit 5 ;;
esac
apt=(apt-get)
if (( EUID != 0 )); then apt=(sudo -n apt-get); fi
export PATH="$HOME/.local/bin:$PATH"
if (( user_only )); then
  for prerequisite in git python3 bash rg shellcheck actionlint pwsh; do
    command -v "$prerequisite" >/dev/null 2>&1 || { echo "--user-only requires preinstalled $prerequisite; use system mode to install OS packages" >&2; exit 5; }
  done
  venv_available || { echo '--user-only requires python3-venv (ensurepip); use system mode to install it' >&2; exit 5; }
  if (( latest )); then
    for requested_tool in "${requested_tools[@]}"; do
      case "$requested_tool" in git|python|rg|shellcheck|gh|node|npm|pwsh)
        echo "--user-only cannot upgrade OS package $requested_tool; rerun without --user-only" >&2; exit 5 ;;
      esac
    done
  fi
  { native_command node && native_command npm; } || install_node_user
  native_command gh || install_gh_user
else
need_apt=()
command -v git >/dev/null || need_apt+=(git)
command -v python3 >/dev/null || need_apt+=(python3)
native_command gh || need_apt+=(gh)
native_command node || need_apt+=(nodejs)
native_command npm || need_apt+=(npm)
if ((${#need_apt[@]})); then
  "${apt[@]}" update
  "${apt[@]}" install -y "${need_apt[@]}"
fi
for native in gh node npm; do
  native_command "$native" || { echo "$native resolves outside Linux after apt installation" >&2; exit 5; }
done
fi
if (( ! user_only )) && ! venv_available; then
  "${apt[@]}" update
  "${apt[@]}" install -y python3-venv
fi
tool_venv="$HOME/.local/share/tra-luat-tools/venv"
if [[ ! -x "$tool_venv/bin/python" ]]; then python3 -m venv "$tool_venv"; fi
export PATH="$tool_venv/bin:$HOME/.local/bin:$PATH"
export NPM_CONFIG_PREFIX="$HOME/.local"
if ! native_command uv; then python -m pip install --disable-pip-version-check uv; fi
if (( user_only )); then
  python -m pip install --disable-pip-version-check 'PyYAML==6.0.3'
  jsonschema_pin="$(python - <<'PY'
import re,yaml
d=yaml.safe_load(open('ops/cong_cu.yaml',encoding='utf-8'))['cong_cu']
m=re.search(r'jsonschema==([0-9][0-9A-Za-z.+-]*)',d['jsonschema']['cai']['lenh'])
assert m, 'jsonschema pin missing from manifest'
print(m.group(1))
PY
)"
  python -m pip install --disable-pip-version-check "jsonschema==$jsonschema_pin" -r requirements.txt
  python ops/cong_cu.py kiem-tra --json
else
  if (( EUID == 0 )); then
    # Manifest OS recipes say "sudo apt-get". A root-only, child-scoped adapter
    # handles exactly that command, including on minimal images without sudo.
    # No wrapper file, global sudo function or manifest modification is needed.
    bash -c '
      sudo() {
        if (( EUID != 0 )) || [[ "$#" -lt 1 || "$1" != apt-get ]]; then
          echo "root installer adapter permits only sudo apt-get" >&2
          return 5
        fi
        shift
        command apt-get "$@"
      }
      export -f sudo
      exec bash "$1" --bat-buoc
    ' tra-luat-root-installer "$repo/ops/cai_cong_cu.sh"
  else
    bash ops/cai_cong_cu.sh --bat-buoc
  fi
fi
if (( persist_path )); then
  marker='# tra-luat CLI PATH'
  for profile in "$HOME/.profile" "$HOME/.bashrc"; do
    if ! grep -Fqx "$marker" "$profile" 2>/dev/null; then
      # POSIX sh syntax (~/.profile may be read by sh); guarded so nested shells do not grow PATH.
      cat >> "$profile" <<'PROFILE'

# tra-luat CLI PATH
for _tl_dir in "$HOME/.local/bin" "$HOME/.local/share/tra-luat-tools/venv/bin"; do
  case ":$PATH:" in *":$_tl_dir:"*) ;; *) PATH="$_tl_dir:$PATH" ;; esac
done
unset _tl_dir
export PATH NPM_CONFIG_PREFIX="$HOME/.local"
PROFILE
      echo "Added tra-luat CLI PATH block to $profile"
    fi
  done
fi
if ! native_command codex; then npm install -g @openai/codex --no-fund --no-audit; fi
if ! native_command gws || ! gws --version >/dev/null 2>&1; then install_gws; fi
if ! native_command claude; then npm install -g @anthropic-ai/claude-code --no-fund --no-audit; fi
if ! native_command nlm; then uv tool install notebooklm-mcp-cli; fi
native_command agy || install_agy_verified
if (( ! user_only )) && ! command -v pwsh >/dev/null 2>&1; then
  # shellcheck source=/dev/null
  ubuntu_version="$(. /etc/os-release; echo "$VERSION_ID")"
  microsoft_deb="$(mktemp --suffix=.deb)"
  trap 'rm -f -- "$microsoft_deb"' EXIT
  curl --fail --silent --show-error --location --proto '=https' --tlsv1.2 \
    "https://packages.microsoft.com/config/ubuntu/$ubuntu_version/packages-microsoft-prod.deb" \
    --output "$microsoft_deb"
  if (( EUID == 0 )); then dpkg -i "$microsoft_deb"; else sudo -n dpkg -i "$microsoft_deb"; fi
  "${apt[@]}" update
  "${apt[@]}" install -y powershell
  rm -f -- "$microsoft_deb"
  trap - EXIT
fi
if (( latest )); then
  tools=("${requested_tools[@]}")
  for tool in "${tools[@]}"; do
    case "$tool" in
      codex)
        target="$(npm view @openai/codex version)"
        current="$(codex --version 2>/dev/null || true)"
        [[ "${current##* }" == "$target" ]] || npm install -g "@openai/codex@$target" --no-fund --no-audit
        [[ "$(codex --version | awk '{print $NF}')" == "$target" ]] || { echo "Codex did not reach $target" >&2; exit 6; } ;;
      gws)
        target="$(npm view @googleworkspace/cli version)"
        current="$(gws --version 2>/dev/null | head -1 || true)"
        [[ "${current##* }" == "$target" ]] || install_gws
        [[ "$(gws --version | awk 'NR==1 {print $NF}')" == "$target" ]] || { echo "gws did not reach $target" >&2; exit 6; } ;;
      claude) claude update ;;
      agy) install_agy_verified ;;
      nlm) uv tool upgrade notebooklm-mcp-cli ;;
      git|python|rg|shellcheck|gh|node|npm|pwsh)
        case "$tool" in python) package=python3 ;; rg) package=ripgrep ;; node) package=nodejs ;;
          pwsh) package=powershell ;; *) package="$tool" ;; esac
        "${apt[@]}" update
        "${apt[@]}" install -y --only-upgrade "$package" ;;
      uv) python -m pip install --disable-pip-version-check --upgrade uv ;;
      *) echo "unknown tool: $tool" >&2; exit 2 ;;
    esac
  done
  for tool in "${tools[@]}"; do
    case "$tool" in
      claude)
        target="$(python -c 'import json,urllib.request; print(json.load(urllib.request.urlopen("https://api.github.com/repos/anthropics/claude-code/releases/latest",timeout=20))["tag_name"].lstrip("v"))')"
        [[ "$(claude --version | awk '{print $1}')" == "$target" ]] || { echo "Claude did not reach $target" >&2; exit 6; } ;;
      nlm)
        target="$(python -c 'import json,urllib.request; print(json.load(urllib.request.urlopen("https://pypi.org/pypi/notebooklm-mcp-cli/json",timeout=20))["info"]["version"])')"
        [[ "$(nlm --version | awk 'NR==1 {print $NF}')" == "$target" ]] || { echo "nlm did not reach $target" >&2; exit 6; } ;;
      agy) agy --version >/dev/null ;;
    esac
  done
fi
for tool in git python bash rg shellcheck actionlint gh node npm pwsh uv claude codex agy nlm gws; do
  command -v "$tool" >/dev/null 2>&1 || { echo "required executor/reviewer tool missing: $tool" >&2; exit 5; }
done
for tool in gh node npm uv claude codex gws agy nlm; do
  native_command "$tool" || { echo "required Linux tool resolves to Windows or outside Linux: $tool" >&2; exit 5; }
done
python ops/cong_cu.py kiem-tra --json
