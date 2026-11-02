import concurrent.futures
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = '3574cb07dba8a8f7f32384ee3d1d3dfbf3a4f70e'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
commands = {
    'bien-nhan': ['python3', 'ops/bien_nhan_v2.py', '--root', '.'],
    'land': ['python3', 'ops/land_evidence_nguon.py', '--root', '.'],
    'direct': ['python3', str(HERE / 'direct_checks.py'), '.'],
    'doctrine': ['python3', '.claude/dev/packet_loop.py', 'doctrine-scan', '--root', '.'],
    'diff-check': ['git', 'diff', '--check', BASE, 'HEAD'],
}

def run_tree(label):
    root = HERE / 'work' / label
    results = {}
    for name, command in commands.items():
        start = time.monotonic()
        p = subprocess.run(command, cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = HERE / 'evidence' / f'{label}-{name}.log'
        log.write_bytes(p.stdout)
        results[name] = {'command': command, 'cwd': str(root), 'rc': p.returncode,
                         'seconds': round(time.monotonic()-start, 3), 'log': str(log.relative_to(HERE))}
        print(label, name, p.returncode, p.stdout.decode(errors='replace').splitlines()[-3:], flush=True)
    (HERE / 'evidence' / f'{label}-gates.json').write_text(json.dumps(results, indent=2, ensure_ascii=False)+'\n')
    return results

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        all_results = list(pool.map(run_tree, sys.argv[1:] or ['head', 'base']))
    sys.exit(int(any(v['rc'] for r in all_results for v in r.values())))
