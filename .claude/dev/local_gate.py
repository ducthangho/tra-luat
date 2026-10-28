#!/usr/bin/env python3
"""Run an explicit local test plan; receipts are evidence, never merge approval.

No network calls or GitHub credentials are needed. Logs stay outside the checkout.
An interrupted attempt remains not_run and can be retried into a NEW directory.
"""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import signal
import subprocess
import sys
import time
import tempfile
from datetime import datetime, timezone


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def git(root, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    return subprocess.check_output(['git', '--no-optional-locks', '-C', str(root), *args],
                                   env=env, text=True).strip()


def identity(root):
    if Path(git(root, 'rev-parse', '--show-toplevel')).resolve() != root.resolve():
        raise ValueError('root must be the repository toplevel')
    # Reject index flags that can hide edits from git status.
    flags = git(root, 'ls-files', '-v').splitlines()
    if any(s and (s[0].islower() or s[0] == 'S') for s in flags):
        raise ValueError('assume-unchanged/skip-worktree entries are not supported')
    if git(root, 'status', '--porcelain', '--untracked-files=all', '--ignored=matching'):
        raise ValueError('checkout must be clean, including untracked and ignored files')
    return {'head': git(root, 'rev-parse', 'HEAD'),
            'tree': git(root, 'rev-parse', 'HEAD^{tree}')}


def read_plan(path):
    plan = json.loads(path.read_text(encoding='utf-8'))
    if type(plan['schema_version']) is not int or plan['schema_version'] != 1 or not plan['steps']:
        raise ValueError('unsupported or empty plan')
    ids = set()
    for s in plan['steps']:
        if not re.fullmatch('[a-z0-9-]+', s['id']) or s['id'] in ids:
            raise ValueError('invalid/duplicate step id')
        ids.add(s['id'])
        if not isinstance(s['argv'], list) or not s['argv'] or not all(isinstance(a, str) for a in s['argv']):
            raise ValueError('argv must be a nonempty string list')
        if type(s['timeout_seconds']) is not int or not 1 <= s['timeout_seconds'] <= 9000:
            raise ValueError('timeout must be 1..9000 seconds')
        if not isinstance(s['positive'], list) or not s['positive'] or not all(isinstance(p, str) and p for p in s['positive']):
            raise ValueError('positive output patterns are required')
        tuning = s.get('env', {})
        if (not isinstance(tuning, dict) or set(tuning) - {'CI_DANG_KY_WORKERS'}
                or any(not isinstance(v, str) or not re.fullmatch('[1-8]', v) for v in tuning.values())):
            raise ValueError('only CI_DANG_KY_WORKERS=1..8 is allowed in step env')
        for pattern in s['positive']:
            re.compile(pattern)
    return plan


def write_receipt(out, receipt, filename='receipt.json'):
    fd, name = tempfile.mkstemp(prefix='receipt.', suffix='.tmp', dir=out)
    temp = Path(name)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            stream.write(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
            stream.flush()
            os.fsync(stream.fileno())
        temp.replace(out / filename)
        directory = os.open(out, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        temp.unlink(missing_ok=True)


class Interrupted(BaseException):
    pass


def interrupted(signum, frame):
    raise Interrupted(signum)


def supervise(status, timeout, argv):
    """A dedicated Linux subreaper; ECHILD, not a process snapshot, proves reaping.

    Only trusted tests: this is lifecycle management, not a security sandbox.
    SIGKILL of this supervisor or host death cannot run its cleanup handlers.
    """
    result = {'rc': None, 'state': 'not_measured', 'cleanup_complete': False,
              'containment': 'not_started'}
    proc = None
    old = {}
    try:
        if ctypes.CDLL(None, use_errno=True).prctl(36, 1, 0, 0, 0) != 0:
            raise OSError('PR_SET_CHILD_SUBREAPER unavailable')
        result['containment'] = 'linux_subreaper'
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            old[sig] = signal.signal(sig, interrupted)
        blocked = signal.pthread_sigmask(signal.SIG_BLOCK, set(old))
        try:
            proc = subprocess.Popen(argv, stdin=subprocess.DEVNULL, start_new_session=True,
                                    preexec_fn=lambda: signal.pthread_sigmask(signal.SIG_SETMASK, blocked))
        finally:
            signal.pthread_sigmask(signal.SIG_SETMASK, blocked)
        try:
            rc = proc.wait(timeout=timeout)
            result.update(rc=rc, state='passed' if rc == 0 else 'failed')
        except subprocess.TimeoutExpired:
            result['reason'] = 'timeout'
        except Interrupted:
            result['reason'] = 'interrupted'
    except Interrupted:
        result.update(rc=None, state='not_measured', reason='interrupted')
    except (OSError, ValueError) as e:
        result['reason'] = type(e).__name__ + ': ' + str(e)
    finally:
        # Do not let a second termination interrupt cleanup and status persistence.
        for sig in old:
            signal.signal(sig, signal.SIG_IGN)
        deadline = time.monotonic() + 5
        while proc is not None:
            try:
                pid, _ = os.waitpid(-1, os.WNOHANG)
            except ChildProcessError:
                result['cleanup_complete'] = True
                break
            if pid:
                continue
            if time.monotonic() >= deadline:
                result.update(state='not_measured', reason='child cleanup deadline exceeded')
                break
            # Reap only OUR direct children. A child cannot have its PID reused
            # before we reap it; no unrelated process is selected by a stale PID.
            for entry in Path('/proc').glob('[0-9]*/stat'):
                try:
                    fields = entry.read_text().rsplit(')', 1)[1].split()
                    if int(fields[1]) == os.getpid():
                        os.kill(int(entry.parent.name), signal.SIGKILL)
                except (OSError, ValueError, IndexError):
                    continue
            time.sleep(0.01)
        if proc is None:
            result['cleanup_complete'] = True
        write_receipt(status.parent, result, status.name)
        for sig, handler in old.items():
            signal.signal(sig, handler)
    return 0 if result['cleanup_complete'] else 1


def execute(root, out, plan_path, expected, only=None):
    if platform.system() != 'Linux':
        raise ValueError('this runner requires Linux; use chay-cong-windows.ps1 on Windows')
    plan = read_plan(plan_path)
    measured = identity(root)
    if measured['head'] != expected:
        raise ValueError('HEAD differs from --expected-head')
    if out == root or root in out.parents:
        raise ValueError('output must be outside the checkout')
    selected = set(only.split(',')) if only else {s['id'] for s in plan['steps']}
    if not selected or selected - {s['id'] for s in plan['steps']}:
        raise ValueError('unknown/empty selection')
    out.mkdir(parents=True, exist_ok=False)
    # Preserve exact plan and runner for later content inspection, not just their names.
    (out / 'plan.json').write_bytes(plan_path.read_bytes())
    (out / 'runner.py').write_bytes(Path(__file__).read_bytes())
    receipt = {'schema_version': 1, 'kind': 'local_test_evidence', **measured,
               'started_at': datetime.now(timezone.utc).isoformat(),
               'system': platform.platform(), 'python': sys.version,
               'python_executable': sys.executable, 'git_version': git(root, '--version'),
               'plan_sha256': digest(out / 'plan.json'),
               'runner_sha256': digest(out / 'runner.py'),
               'full_ci_equivalence': False, 'approval': False,
               'checkout_unchanged': False, 'steps': []}
    for s in plan['steps']:
        receipt['steps'].append({'id': s['id'], 'state': 'not_run'})
    write_receipt(out, receipt)
    # Do not inherit credentials or test-mode switches into candidate code.
    env = {k: os.environ[k] for k in ('PATH', 'HOME', 'LANG', 'LC_ALL', 'TMPDIR') if k in os.environ}
    env.update(PYTHONUTF8='1', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1',
               GIT_CONFIG_COUNT='3', GIT_CONFIG_KEY_0='core.abbrev', GIT_CONFIG_VALUE_0='7',
               GIT_CONFIG_KEY_1='core.autocrlf', GIT_CONFIG_VALUE_1='false',
               GIT_CONFIG_KEY_2='core.eol', GIT_CONFIG_VALUE_2='lf')
    for s, row in zip(plan['steps'], receipt['steps']):
        if s['id'] not in selected:
            continue
        argv = [sys.executable if a == '{python}' else a for a in s['argv']]
        row.update(argv=argv, env=s.get('env', {}), timeout_seconds=s['timeout_seconds'], state='running')
        write_receipt(out, receipt)
        log = out / (s['id'] + '.log')
        start = time.monotonic()
        supervisor = None
        status = out / (s['id'] + '.process.json')
        old = {sig: signal.signal(sig, interrupted)
               for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)}
        try:
            with tempfile.TemporaryDirectory(prefix=s['id'] + '-', dir=out) as scratch:
                step_env = dict(env, **s.get('env', {}), TMPDIR=scratch, TEMP=scratch, TMP=scratch,
                                RUFF_CACHE_DIR=str(out / 'ruff-cache'))
                with log.open('wb') as f:
                    supervisor = subprocess.Popen(
                        [sys.executable, '-B', str(out / 'runner.py'), '_supervise',
                         str(status), str(s['timeout_seconds']), *argv],
                        cwd=root, env=step_env, stdin=subprocess.DEVNULL,
                        stdout=f, stderr=subprocess.STDOUT, start_new_session=True)
                    try:
                        supervisor.wait(timeout=s['timeout_seconds'] + 10)
                    except (Interrupted, subprocess.TimeoutExpired):
                        for sig in old:
                            signal.signal(sig, signal.SIG_IGN)
                        supervisor.terminate()
                        try:
                            supervisor.wait(timeout=8)
                        except subprocess.TimeoutExpired:
                            supervisor.kill()
                            supervisor.wait(timeout=2)
                        row.update(rc=None, state='not_measured', reason='interrupted or supervisor timeout')
                if status.is_file():
                    process = json.loads(status.read_text(encoding='utf-8'))
                    if row['state'] == 'running':
                        row.update(process)
                    else:
                        row['cleanup_complete'] = process['cleanup_complete']
                else:
                    row.update(rc=None, state='not_measured', cleanup_complete=False,
                               reason='supervisor status missing')
        except OSError as e:
            row.update(rc=None, state='not_measured', cleanup_complete=False, reason=type(e).__name__)
        finally:
            for sig, handler in old.items():
                signal.signal(sig, handler)
        row['seconds'] = round(time.monotonic() - start, 3)
        row['log'] = log.name
        row['log_sha256'] = digest(log)
        if row['state'] == 'passed':
            body = log.read_text(encoding='utf-8', errors='replace')
            row['positive_matches'] = [bool(re.search(p, body, re.M)) for p in s['positive']]
            if not all(row['positive_matches']):
                row.update(state='failed', reason='missing positive evidence')
        try:
            receipt['checkout_unchanged'] = identity(root) == measured
        except (ValueError, subprocess.SubprocessError):
            receipt['checkout_unchanged'] = False
        write_receipt(out, receipt)
        print(s['id'], row['state'], 'rc=' + str(row['rc']), flush=True)
        if not receipt['checkout_unchanged'] or row['state'] == 'not_measured':
            break
    receipt['finished_at'] = datetime.now(timezone.utc).isoformat()
    write_receipt(out, receipt)
    return 0 if receipt['checkout_unchanged'] and all(r['state'] == 'passed' for r in receipt['steps']) else 1


def verify(out, expected, trusted_plan):
    def require(condition):
        if not condition:
            raise ValueError("receipt verification failed")
    for name in ('receipt.json', 'plan.json', 'runner.py'):
        require((out / name).is_file() and not (out / name).is_symlink())
    r = json.loads((out / 'receipt.json').read_text(encoding='utf-8'))
    plan = read_plan(out / 'plan.json')
    require(digest(out / 'plan.json') == digest(trusted_plan))
    require(digest(out / 'runner.py') == digest(Path(__file__)))
    require(type(r['schema_version']) is int and r['schema_version'] == 1 and r['kind'] == 'local_test_evidence')
    require(r['head'] == expected and r['checkout_unchanged'] is True and isinstance(r.get('finished_at'), str) and r['finished_at'])
    require(r.get('approval') is False and r.get('full_ci_equivalence') is False)
    require(isinstance(r.get('tree'), str) and re.fullmatch('[0-9a-f]{40}|[0-9a-f]{64}', r['tree']))
    require(isinstance(r.get('started_at'), str) and r['started_at'])
    require(digest(out / 'plan.json') == r['plan_sha256'])
    require(digest(out / 'runner.py') == r['runner_sha256'])
    require([s['id'] for s in plan['steps']] == [s['id'] for s in r['steps']])
    for s, row in zip(plan['steps'], r['steps']):
        require(row['state'] == 'passed' and type(row['rc']) is int and row['rc'] == 0)
        require(row.get('cleanup_complete') is True and row.get('containment') == 'linux_subreaper')
        matches = row.get('positive_matches')
        require(isinstance(matches, list) and len(matches) == len(s['positive'])
                and all(match is True for match in matches))
        require(row.get('env') == s.get('env', {}))
        require(type(row['timeout_seconds']) is int and row['timeout_seconds'] == s['timeout_seconds'])
        require(row['argv'] == [r['python_executable'] if a == '{python}' else a for a in s['argv']])
        require(row['log'] == s['id'] + '.log')
        log = out / row['log']
        require(not log.is_symlink() and digest(log) == row['log_sha256'])
        body = log.read_text(encoding='utf-8', errors='replace')
        require(all(re.search(p, body, re.M) for p in s['positive']))
    print('VERIFIED:', len(r['steps']), 'steps;', expected)
    print('Content integrity only; not independent attestation or merge approval.')
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['run', 'verify'])
    p.add_argument('--root', type=Path, default=Path.cwd())
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--plan', type=Path, default=Path(__file__).with_name('local_gate_plan.json'))
    p.add_argument('--expected-head', required=True)
    p.add_argument('--only', help='comma-separated step IDs; omitted steps remain not_run')
    a = p.parse_args()
    try:
        if not re.fullmatch('[0-9a-f]{40}|[0-9a-f]{64}', a.expected_head):
            raise ValueError('expected-head must be a full Git OID')
        return (verify(a.out.resolve(), a.expected_head, a.plan.resolve()) if a.action == 'verify' else
                execute(a.root.resolve(), a.out.resolve(), a.plan.resolve(), a.expected_head, a.only))
    except (OSError, ValueError, KeyError, AssertionError, subprocess.SubprocessError) as e:
        print('NOT VERIFIED:', type(e).__name__, str(e), file=sys.stderr)
        return 2


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '_supervise':
        raise SystemExit(supervise(Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4:]))
    raise SystemExit(main())
