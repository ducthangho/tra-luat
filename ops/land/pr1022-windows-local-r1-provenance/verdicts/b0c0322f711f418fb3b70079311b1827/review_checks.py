import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

SANDBOX = Path(__file__).resolve().parent
REPO = SANDBOX / 'cay-kho'
EVIDENCE = SANDBOX / 'evidence'
EVIDENCE.mkdir(exist_ok=True)
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1',
           PYTHONIOENCODING='utf-8', GIT_OPTIONAL_LOCKS='0',
           TL_CACHE_DIR=str(EVIDENCE / 'tl-cache'),
           XDG_CACHE_HOME=str(EVIDENCE / 'cache'))

def snapshot(label):
    commands = [
        ['git', 'rev-parse', 'HEAD', 'HEAD^{tree}'],
        ['git', 'status', '--porcelain=v1', '--untracked-files=all', '--ignored'],
        ['git', 'diff', '--binary', 'HEAD'],
        ['git', 'diff', '--cached', '--binary'],
        ['git', 'ls-files', '--stage'],
        ['git', 'ls-files', '--others', '--exclude-standard', '-z'],
        ['git', 'ls-files', '--others', '--ignored', '--exclude-standard', '-z'],
    ]
    result = []
    for command in commands:
        p = subprocess.run(command, cwd=REPO, env=ENV, capture_output=True)
        assert p.returncode == 0, (command, p.stderr)
        result.append({'command': command, 'rc': p.returncode,
                       'stdout': p.stdout.decode('utf-8'),
                       'stderr': p.stderr.decode('utf-8')})
    (EVIDENCE / f'snapshot-{label}.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return result

if __name__ == '__main__':
    before = snapshot('before')
    records = []
    checks = [
        ('adr-song', ['python3', '.claude/dev/packet_loop.py', 'adr-song', '--root', '.']),
        ('doctrine-scan', ['python3', '.claude/dev/packet_loop.py', 'doctrine-scan', '--root', '.']),
        ('doc-claims-check', ['python3', 'scripts/tl.py', 'doc-claims-check', '--json']),
    ]
    for name, command in checks:
        start = time.monotonic()
        p = subprocess.run(command, cwd=REPO, env=ENV, capture_output=True)
        stdout = EVIDENCE / (name + '.stdout')
        stderr = EVIDENCE / (name + '.stderr')
        stdout.write_bytes(p.stdout)
        stderr.write_bytes(p.stderr)
        record = {'name': name, 'command': command, 'cwd': str(REPO),
                  'rc': p.returncode, 'elapsed_s': round(time.monotonic() - start, 3),
                  'stdout_sha256': hashlib.sha256(p.stdout).hexdigest(),
                  'stderr_sha256': hashlib.sha256(p.stderr).hexdigest()}
        if name == 'doc-claims-check':
            out = json.loads(p.stdout)
            record['summary'] = {k: out[k] for k in (
                'ok', 'files_scanned', 'claims_flagged', 'advisory_count', 'layers_skipped')}
        else:
            record['stdout'] = p.stdout.decode('utf-8').strip()
        records.append(record)
        print(json.dumps(record, ensure_ascii=False), flush=True)
        (EVIDENCE / 'checks.json').write_text(
            json.dumps(records, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    after = snapshot('after')
    print(json.dumps({'snapshot_unchanged': before == after}), flush=True)
