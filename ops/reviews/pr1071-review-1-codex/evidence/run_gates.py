import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys

sandbox = Path(__file__).resolve().parent
root = Path(sys.argv[1]).resolve()
label = sys.argv[2]
out = sandbox / 'evidence'
out.mkdir(exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
commands = {
    'bien-nhan': ['python3', 'ops/bien_nhan_v2.py', '--root', '.'],
    'land': ['python3', 'ops/land_evidence_nguon.py', '--root', '.'],
    'direct': ['python3', str(sandbox / 'direct_gates.py'), str(root)],
    'doctrine': ['python3', '.claude/dev/packet_loop.py', 'doctrine-scan', '--root', '.'],
    'diff-check': ['git', 'diff', '--check', '97120d3', 'HEAD'],
}
def run(item):
    name, cmd = item
    r = subprocess.run(cmd, cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (out / f'{label}-{name}.log').write_bytes(r.stdout)
    return {'name': name, 'command': cmd, 'cwd': str(root), 'rc': r.returncode,
            'log': f'evidence/{label}-{name}.log', 'output': r.stdout.decode(errors='replace')}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
    rows = list(ex.map(run, commands.items()))
(out / f'{label}-gates.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
for row in rows:
    print(f"{label} {row['name']} rc={row['rc']}: {row['output'].strip()}")
