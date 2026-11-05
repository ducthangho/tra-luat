#!/usr/bin/env bash
# Shared baseline with Windows: ops/cong_cu.yaml and ops/cai_cong_cu.sh.
# Usage: bash ops/environment/update-linux.sh --repo /path/to/tra-luat [--apply [--user-only] [--persist-path]
#          [--latest [--tools claude,codex,agy,nlm,gws]]]
# Without --apply it only reports versions and the checker result (exit code = checker exit code).
# It reports only whether TL_* variables are set; it never prints their values or reads credential files.
set -euo pipefail
# Developer regression mode: real entrypoint, isolated Ubuntu fixtures, no installers/network.
if [[ "${1:-}" == --selftest ]]; then
  shift
  PYTHONDONTWRITEBYTECODE=1 python3 -B - "$0" "$@" <<'UPDATER_SELFTEST'
import hashlib, io, json, os, pathlib, shutil, subprocess, sys, tarfile, tempfile, time

source = pathlib.Path(sys.argv[1]).resolve()
args = sys.argv[2:]
if args:
    if len(args) != 2 or args[0] != '--against':
        raise SystemExit('selftest accepts only --against SCRIPT')
    source = pathlib.Path(args[1]).resolve()
text = source.read_text()
if pathlib.Path('/etc/os-release').read_text().find('ID=ubuntu\n') < 0:
    raise SystemExit('selftest requires real Ubuntu (fixture installers only)')
real_python, real_bash = sys.executable, shutil.which('bash')
real_pgrep = shutil.which('pgrep')
assert real_pgrep and real_bash, 'fixture dependency missing'
print('RUNTIME', sys.version.split()[0], pathlib.Path('/etc/os-release').read_text().splitlines()[0], flush=True)
results = []
def suite_ok(records):
    return bool(records) and all(ok for _, ok in records)
with tempfile.TemporaryDirectory(prefix='tl-updater-selftest-') as scratch:
    root = pathlib.Path(scratch)
    def executable(path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        path.chmod(0o755)
    # All package/network/profile effects stay inside this disposable fixture.
    driver = root / 'driver'
    executable(driver, '#!' + real_python + '\n' + r'''
import json, os, pathlib, shutil, subprocess, sys
name = pathlib.Path(sys.argv[0]).name
args = sys.argv[1:]
home = pathlib.Path(os.environ['HOME'])
def event(value):
    with open(os.environ['FIX_LOG'], 'a') as out: out.write(value + '\n')
def tool(name, broken=False):
    dest = home / ('.local/share/tra-luat-tools/venv/bin/uv' if name == 'uv' else '.local/bin/' + name)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_symlink(): dest.unlink()
    dest.write_text('#!/bin/bash\n' + ('exit 127\n' if broken else 'echo "' + name + ' 1.2.3"\n'))
    dest.chmod(0o755)
if name == 'pgrep':
    event('selector ' + json.dumps([os.environ['REAL_PGREP'], '-P', os.environ['FIX_PARENT']] + args))
    sys.exit(subprocess.call([os.environ['REAL_PGREP'], '-P', os.environ['FIX_PARENT']] + args))
if name in ('python', 'python3'):
    if args[:2] == ['-m', 'pip']:
        event('pip ' + ' '.join(args))
        if 'uv' in args: tool('uv', os.environ.get('POST_BROKEN') == 'uv')
        sys.exit(0)
    if args[:2] == ['-m', 'venv']:
        event('venv')
        dest = pathlib.Path(args[2]) / 'bin/python'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.symlink_to(sys.argv[0])
        sys.exit(0)
    if args and args[0] == 'ops/cong_cu.py':
        event('checker')
        print(json.dumps({'cong_cu': [{'ten': 'shellcheck', 'trang_thai': 'DAT'}]}))
        sys.exit(0)
    if args == ['-']:
        code = sys.stdin.read()
        if 'api.github.com/repos/google-antigravity' in code:
            print(os.environ['AGY_RELEASE'])
            sys.exit(0)
        sys.exit(subprocess.run([os.environ['REAL_PYTHON']] + args, input=code, text=True).returncode)
    sys.exit(subprocess.call([os.environ['REAL_PYTHON']] + args))
if name in ('apt-get', 'sudo', 'dpkg', 'curl', 'npm', 'uv') and '--version' not in args:
    event(name + ' ' + ' '.join(args))
    if name == 'sudo':
        if args[:2] == ['-n', 'apt-get']: args = args[1:]
        if not args or args[0] != 'apt-get': raise SystemExit('UNEXPECTED fixture sudo')
        sys.exit(subprocess.call([str(pathlib.Path(os.environ['FIX_BIN'], 'apt-get'))] + args[1:]))
    elif name == 'apt-get' and 'install' in args and 'curl' in args:
        pathlib.Path(os.environ['FIX_BIN'], 'curl').symlink_to(os.environ['DRIVER'])
    elif name == 'curl':
        if 'https://fixture.invalid/agy' not in args: raise SystemExit('UNEXPECTED fixture network')
        dest = args[args.index('--output') + 1] if '--output' in args else args[args.index('-o') + 1]
        shutil.copyfile(os.environ['AGY_ARCHIVE'], dest)
    elif name == 'npm' and args[:1] == ['view']:
        print('1.2.3')
    elif name == 'npm' and 'install' in args:
        for package, binary in [('@openai/codex', 'codex'), ('@anthropic-ai/claude-code', 'claude'), ('@googleworkspace/cli', 'gws')]:
            if any(arg.startswith(package) for arg in args): tool(binary, os.environ.get('POST_BROKEN') == binary)
    elif name == 'uv' and 'install' in args:
        tool('nlm', os.environ.get('POST_BROKEN') == 'nlm')
    elif name not in ('apt-get', 'npm'):
        raise SystemExit('UNEXPECTED fixture operation: ' + name)
    sys.exit(0)
print(name + ' 1.2.3')
''')
    def run_case(label, script=text, mode='system', missing=(), broken=None,
                 managed=False, child=None, post=None, agy=None, extra=(), escape=False):
        case = root / str(len(list(root.iterdir())))
        bin_dir, home, repo = case / 'bin', case / 'home', case / 'repo'
        for directory in (bin_dir, home, repo / 'ops'):
            directory.mkdir(parents=True)
        log = case / 'events'
        log.touch()
        (repo / 'ops/cong_cu.yaml').write_text('cong_cu:\n  shellcheck:\n    bat_buoc: true\n  jsonschema:\n    cai:\n      lenh: pip install jsonschema==4.25.1\n    bat_buoc: false\n')
        for file in ('ops/cong_cu.py', 'ops/cai_cong_cu.sh', 'requirements.txt'):
            (repo / file).touch()
        commands = 'git python python3 bash rg shellcheck actionlint gh node npm pwsh uv claude codex agy nlm gws curl apt-get sudo dpkg pgrep'
        for name in commands.split():
            if name not in missing: (bin_dir / name).symlink_to(driver)
        (bin_dir / 'bash').unlink()
        (bin_dir / 'bash').symlink_to(real_bash)
        for name in 'uname id grep head readlink mkdir mktemp rm sha256sum tar gzip install awk ln cat'.split():
            target = shutil.which(name)
            assert target, 'missing fixture utility ' + name
            (bin_dir / name).symlink_to(target)
        venv = home / '.local/share/tra-luat-tools/venv/bin'
        venv.mkdir(parents=True)
        (venv / 'python').symlink_to(driver)
        if broken:
            dest = (venv / broken if broken == 'uv' else home / '.local/bin' / broken) if managed else bin_dir / broken
            if dest.is_symlink(): dest.unlink()
            executable(dest, '#!/bin/bash\nexit 127\n')
            if escape:
                external = case / 'external' / broken
                executable(external, '#!/bin/bash\nexit 127\n')
                dest.unlink()
                dest.symlink_to(external)
        archive = case / 'agy.tar.gz'
        with tarfile.open(archive, 'w:gz') as out:
            payload = b'#!/bin/bash\necho "agy 1.2.3"\n'
            if post == 'agy': payload = b'#!/bin/bash\nexit 127\n'
            info = tarfile.TarInfo('wrong' if agy == 'layout' else 'antigravity')
            info.size = len(payload)
            out.addfile(info, io.BytesIO(payload))
        digest = hashlib.sha256(archive.read_bytes()).hexdigest() if agy != 'digest' else '0' * 64
        release = {'tag_name': 'v1.2.3', 'assets': [{'name': 'agy_cli_linux_x64.tar.gz', 'browser_download_url': 'https://fixture.invalid/agy', 'digest': 'sha256:' + digest}]}
        entry = case / 'updater.sh'
        entry.write_text(script)
        env = {'PATH': str(bin_dir), 'HOME': str(home), 'PYTHONDONTWRITEBYTECODE': '1',
               'FIX_LOG': str(log), 'FIX_BIN': str(bin_dir), 'FIX_PARENT': str(os.getpid()),
               'REAL_PYTHON': real_python, 'REAL_PGREP': real_pgrep, 'DRIVER': str(driver),
               'AGY_RELEASE': json.dumps(release), 'AGY_ARCHIVE': str(archive), 'POST_BROKEN': post or ''}
        def snapshot():
            return [(str(p.relative_to(case)), p.lstat().st_mode, os.readlink(p) if p.is_symlink() else p.read_bytes())
                    for tree in (home, repo) for p in sorted(tree.rglob('*')) if p.is_symlink() or p.is_file()]
        before = snapshot()
        process = None
        try:
            if child:
                executable_name = case / child
                executable_name.symlink_to(real_python)
                process = subprocess.Popen([str(executable_name), '-B', '-c', 'import time; time.sleep(120)'], env=env)
                for _ in range(100):
                    comm = pathlib.Path('/proc', str(process.pid), 'comm').read_text().strip()
                    if comm == child: break
                    time.sleep(.01)
                assert comm == child, 'child did not start with expected native comm'
                print('CHILD', label, process.pid, comm, 'argv=' + json.dumps([str(executable_name), '-B', '-c', 'import time; time.sleep(120)']), flush=True)
            command = [real_bash, str(entry), '--repo', str(repo), '--apply']
            if mode == 'user': command.append('--user-only')
            command.extend(extra)
            result = subprocess.run(command, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
        finally:
            if process:
                process.terminate()
                process.wait(timeout=5)
        events = log.read_text().splitlines()
        mutations = [line for line in events if not line.startswith(('selector ', 'checker'))]
        if snapshot() != before: mutations.append('fixture filesystem changed')
        print('CASE', label, 'rc=' + str(result.returncode), 'events=' + json.dumps(events), flush=True)
        print(result.stdout, end='', flush=True)
        assert not any('UNEXPECTED' in line for line in result.stdout.splitlines()), 'unexpected fixture operation'
        return result.returncode, result.stdout, mutations
    def check(label, value):
        results.append((label, bool(value)))
        print(('PASS ' if value else 'FAIL ') + label, flush=True)
    def rejected(result, message, rc=5):
        code, output, mutations = result
        return code == rc and message in output and not mutations
    for mode in ('system', 'user'):
        result = run_case('curl-' + mode, mode=mode, missing=('curl',) if mode == 'user' else ('curl', 'agy'), extra=('--persist-path',) if mode == 'user' else ())
        check('curl-' + mode, rejected(result, 'requires preinstalled curl') if mode == 'user' else result[0] == 0 and 'apt-get install -y curl' in result[2] and any(e.startswith('curl ') for e in result[2]) and result[2].index('apt-get install -y curl') < next(i for i, e in enumerate(result[2]) if e.startswith('curl ')))
        result = run_case('healthy-' + mode, mode=mode)
        check('healthy-' + mode, result[0] == 0 and not any(e.startswith(('apt-get ', 'sudo ')) for e in result[2]))
        check('python-version-' + mode, rejected(run_case('python-version-' + mode, mode=mode, child='python3.12', extra=('--persist-path',)), 'processes are active', 3))
    check('exact-name-control', run_case('exact-name-control', child='notpython3.12')[0] == 0)
    for tool in ('uv', 'claude', 'codex', 'nlm', 'agy'):
        check('external-broken-' + tool, rejected(run_case('external-broken-' + tool, broken=tool, extra=('--persist-path',)), 'Broken external ' + tool))
        result = run_case('managed-repair-' + tool, broken=tool, managed=True)
        check('managed-repair-' + tool, result[0] == 0 and any(e.startswith(('pip ', 'npm ', 'uv ', 'curl ')) for e in result[2]))
        result = run_case('managed-postcheck-' + tool, broken=tool, managed=True, post=tool)
        check('managed-postcheck-' + tool, result[0] == 6 and ('version probe failed: ' + tool in result[1] or 'AGY did not reach' in result[1]))
    for tool in ('codex', 'uv'):
        check('managed-symlink-escape-' + tool, rejected(run_case('managed-symlink-escape-' + tool, broken=tool, managed=True, escape=True), 'Broken external ' + tool))
    result = run_case('gws-repair', missing=('gws',))
    check('gws-allow-scripts', result[0] == 0 and any('--allow-scripts=@googleworkspace/cli' in e for e in result[2]))
    check('agy-current-external', not run_case('agy-current-external', extra=('--latest', '--tools', 'agy'))[2])
    for fault, message in (('digest', 'AGY SHA256 mismatch'), ('layout', 'Unexpected AGY archive layout')):
        result = run_case('agy-' + fault, missing=('agy',), agy=fault)
        check('agy-' + fault, result[0] == 5 and message in result[1])
    check('npm-user-broken', rejected(run_case('npm-user-broken', mode='user', broken='npm'), 'requires working native npm'))
    check('healthy-external-no-duplicate', not run_case('healthy-external-no-duplicate')[2])
    # Semantic mutants must lose the intended property, with healthy controls green.
    if not args:
        marker = '# END updater developer selftest\n'
        prefix, body = text.split(marker, 1)
        mutants = [
            ('curl-user', 'in curl git python3', 'in git python3', dict(mode='user', missing=('curl',)), 'requires preinstalled curl', 5),
            ('curl-system', 'command -v curl >/dev/null || need_apt+=(curl)', ': # curl provisioning removed', dict(missing=('curl', 'agy')), 'apt-get install -y curl', 0),
            ('python-version', 'python([0-9]+([.][0-9]+)*)?', 'python|python3', dict(child='python3.12'), 'processes are active', 3),
            ('external-probe', '&& ! usable_command "$tool" && ! managed_cli', '&& false && ! managed_cli', dict(broken='codex'), 'Broken external codex', 5),
            ('execution-probe', 'native_command "$1" && "$1" --version >/dev/null 2>&1;', 'native_command "$1";', dict(broken='codex'), 'Broken external codex', 5),
            ('final-probe', 'usable_command "$tool" || { echo "required Linux tool version probe failed: $tool" >&2; exit 6; }', ': # final probe removed', dict(broken='codex', managed=True, post='codex'), 'version probe failed: codex', 6),
        ]
        for label, before, after, options, message, code in mutants:
            assert body.count(before) == 1, 'mutant anchor not unique: ' + label
            mutant = prefix + marker + body.replace(before, after, 1)
            result = run_case('mutant-' + label, script=mutant, **options)
            intended = any(e == message for e in result[2]) if label == 'curl-system' else result[0] == code and message in result[1]
            expected_rc = {'curl-system': 5, 'external-probe': 6}.get(label, 0)
            evidence = 'AGY download failed' in result[1] if label == 'curl-system' else ('version probe failed: codex' in result[1] and any(e.startswith('npm install') for e in result[2]) if label == 'external-probe' else 'cong_cu' in result[1])
            check('mutant-' + label, not intended and result[0] == expected_rc and evidence)
            check('mutant-control-' + label, run_case('mutant-control-' + label, script=mutant)[0] == 0)
        # A crash cannot count as a semantic kill, and a contaminated run cannot pass.
        for label, bad in [('crash', 'echo "Broken external codex"; exit 99\n'), ('import', 'echo "Broken external codex"; python3 -c "import nonexistent_fixture_module"\n'), ('mutation', 'apt-get install -y forbidden; echo "Broken external codex"; exit 5\n')]:
            result = run_case('canary-' + label, script=bad)
            check('harness-' + label, not rejected(result, 'Broken external codex'))
        try:
            run_case('canary-network', script='curl --output "$HOME/unexpected" https://unexpected.invalid\n')
            check('harness-network', False)
        except AssertionError as error:
            check('harness-network', str(error) == 'unexpected fixture operation')
    check('harness-zero-tests', not suite_ok([]))
    check('nonempty-results', len(results) > 0)
passed = sum(ok for _, ok in results)
print('COUNTS', json.dumps({'cases': len(results), 'mutants': sum(label.startswith('mutant-') and not label.startswith('mutant-control-') for label, _ in results), 'mutant_controls': sum(label.startswith('mutant-control-') for label, _ in results)}), flush=True)
print('SELFTEST %d/%d' % (passed, len(results)), flush=True)
raise SystemExit(0 if suite_ok(results) else 1)
UPDATER_SELFTEST
  exit $?
fi
# END updater developer selftest
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
usable_command() { native_command "$1" && "$1" --version >/dev/null 2>&1; }
managed_cli() {
  local found resolved expected
  found="$(command -v "$1" 2>/dev/null || true)"
  case "$1" in uv) expected="$HOME/.local/share/tra-luat-tools/venv/bin/uv" ;;
    *) expected="$HOME/.local/bin/$1" ;;
  esac
  [[ "$found" == "$expected" && -O "$found" ]] || return 1
  resolved="$(readlink -f -- "$found")" || return 1
  [[ "$resolved" == "$HOME/.local/"* && -O "$resolved" ]]
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
  # Keep current releases wherever installed; update only our managed destination.
  # `agy update` would bypass the SHA256 check.
  if native_command agy; then
    if [[ "$(agy_version || true)" == "${tag#v}" ]]; then return 0; fi
    found="$(command -v agy)"
    if [[ "$found" != "$HOME/.local/bin/agy" ]]; then
      printf 'AGY at %s needs repair or update; upgrade that installation with its package manager, or remove it before installing managed AGY at %s.\n' "$found" "$HOME/.local/bin/agy" >&2
      return 5
    fi
  fi
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
if pgrep -x -u "$(id -u)" 'claude|codex|agy|nlm|gws|uv|node|python([0-9]+([.][0-9]+)*)?' >/dev/null 2>&1; then
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
  if ! native_command node || ! native_command npm || ! npm --version >/dev/null 2>&1; then echo 'Native Node/npm not usable after install' >&2; return 6; fi
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
tool_venv="$HOME/.local/share/tra-luat-tools/venv"
export PATH="$tool_venv/bin:$PATH"
# Refuse broken external installations before package, venv or profile changes.
# Repair is limited to our owned destinations, including resolved symlink targets.
for tool in uv claude codex nlm agy; do
  if native_command "$tool" && ! usable_command "$tool" && ! managed_cli "$tool"; then
    printf 'Broken external %s at %s; repair that installation before --apply.\n' "$tool" "$(command -v "$tool")" >&2
    exit 5
  fi
done
if (( user_only )); then
  for prerequisite in curl git python3 bash rg shellcheck actionlint pwsh; do
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
  if native_command node; then
    if ! native_command npm || ! npm --version >/dev/null 2>&1; then
      printf '%s\n' "--user-only requires working native npm for Node at $(command -v node); repair npm using the package manager for that Node installation, then rerun. Node will not be replaced." >&2
      exit 5
    fi
  else
    install_node_user
  fi
  native_command gh || install_gh_user
else
need_apt=()
command -v curl >/dev/null || need_apt+=(curl)
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
if [[ ! -x "$tool_venv/bin/python" ]]; then python3 -m venv "$tool_venv"; fi
export PATH="$tool_venv/bin:$HOME/.local/bin:$PATH"
export NPM_CONFIG_PREFIX="$HOME/.local"
if ! usable_command uv; then python -m pip install --disable-pip-version-check --force-reinstall uv; fi
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
  # The checker imports yaml before probing any tool; bootstrap only if absent.
  if ! python -c 'import yaml' >/dev/null 2>&1; then
    python -m pip install --disable-pip-version-check 'PyYAML==6.0.3'
  fi
  baseline_dat() {
    local result probe_rc=0
    # Missing/broken tools are expected here; do not let errexit abort repair.
    result="$(python ops/cong_cu.py kiem-tra --chi "$1" --json)" || probe_rc=$?
    (( probe_rc == 0 )) || return 1
    printf '%s' "$result" | python -c 'import json,sys
entries=json.load(sys.stdin).get("cong_cu") or []
sys.exit(0 if len(entries)==1 and entries[0].get("ten")==sys.argv[1] and entries[0].get("trang_thai")=="DAT" else 1)' "$1"
  }
  baseline_tools="$(python - <<'PY'
import yaml
tools=yaml.safe_load(open('ops/cong_cu.yaml',encoding='utf-8'))['cong_cu']
names=[name for name,entry in tools.items() if entry['bat_buoc'] or entry.get('chuan_bi')]
# Prepare ShellCheck before actionlint; the final full checker runs its canary.
print('\n'.join(sorted(names,key=lambda name: name != 'shellcheck')))
PY
)"
  [[ -n "$baseline_tools" ]] || { echo 'Shared baseline is empty' >&2; exit 5; }
  while IFS= read -r baseline_tool; do
    if baseline_dat "$baseline_tool"; then continue; fi
    if (( EUID == 0 )); then
      # Manifest OS recipes say "sudo apt-get". Keep this adapter child-scoped.
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
        if [[ "$2" == actionlint ]]; then export AL_DICH="$HOME/.local/bin"; fi
        exec bash "$1" "$2"
      ' tra-luat-root-installer "$repo/ops/cai_cong_cu.sh" "$baseline_tool"
    elif [[ "$baseline_tool" == actionlint ]]; then
      AL_DICH="$HOME/.local/bin" bash ops/cai_cong_cu.sh "$baseline_tool"
    else
      bash ops/cai_cong_cu.sh "$baseline_tool"
    fi
    # Child PATH changes cannot reach this parent. Known install directories
    # are already on PATH; clear cached lookups and require this exact tool DAT.
    hash -r
    baseline_dat "$baseline_tool" || {
      echo "Baseline tool $baseline_tool is not DAT in the parent after repair (check PATH shadowing)" >&2
      exit 6
    }
  done <<< "$baseline_tools"
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
if ! usable_command codex; then npm install -g @openai/codex --no-fund --no-audit; fi
if ! native_command gws || ! gws --version >/dev/null 2>&1; then install_gws; fi
if ! usable_command claude; then npm install -g @anthropic-ai/claude-code --no-fund --no-audit; fi
if ! usable_command nlm; then uv tool install --force notebooklm-mcp-cli; fi
usable_command agy || install_agy_verified
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
  usable_command "$tool" || { echo "required Linux tool version probe failed: $tool" >&2; exit 6; }
done
python ops/cong_cu.py kiem-tra --json
