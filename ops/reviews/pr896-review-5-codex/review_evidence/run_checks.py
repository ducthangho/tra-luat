import concurrent.futures
import json
import os
from pathlib import Path
import subprocess

base = Path(__file__).resolve().parent
root = base.parent / 'cay-kho'
commands = {
    't26': ['python3', 'ops/lease_publish_test.py', '--chi-ca=t26_'],
    't27': ['python3', 'ops/lease_publish_test.py', '--chi-ca=t27_'],
    't138': ['python3', 'ops/lease_publish_test.py', '--chi-ca=t138_'],
    'bien_nhan_v2': ['python3', 'ops/bien_nhan_v2.py', '--root', '.'],
    'land_evidence_nguon': ['python3', 'ops/land_evidence_nguon.py', '--root', '.'],
    'doctrine': ['python3', '.claude/dev/packet_loop.py', 'doctrine-scan', '--root', '.'],
    'doc_claims': ['python3', 'scripts/tl.py', 'doc-claims-check', '--json'],
}

def run(item):
    name, cmd = item
    r = subprocess.run(cmd, cwd=root, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}, capture_output=True, text=True)
    (base / (name + '.stdout')).write_text(r.stdout)
    (base / (name + '.stderr')).write_text(r.stderr)
    (base / (name + '.rc')).write_text(str(r.returncode) + '\n')
    result = {'name': name, 'command': cmd, 'rc': r.returncode, 'tail': r.stdout.splitlines()[-4:], 'stderr_tail': r.stderr.splitlines()[-2:]}
    if name == 'doc_claims':
        result['ok'] = json.loads(r.stdout).get('ok')
    print(json.dumps(result, ensure_ascii=False), flush=True)
    with (base.parent / 'VERDICT.md').open('a') as f:
        f.write('\n- Phép đo tại `cay-kho/`: `' + ' '.join(cmd) + '` ⇒ rc=' + str(r.returncode) + '; ' + (('JSON ok=' + str(result['ok'])) if name == 'doc_claims' else ' / '.join(result['tail'])) + '. Log: `review_evidence/' + name + '.stdout` và `.stderr`.\n')
    return result

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, commands.items()))
(base / 'checks.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
