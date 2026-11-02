"""Run existing repository gates; write only external evidence files."""
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path('/tmp/rv1050-r2-copy')
out = Path(__file__).resolve().parent
label = sys.argv[1]
gates = {
    'bien_nhan_v2': ['python3', 'ops/bien_nhan_v2.py', '--root', '.'],
    'land_evidence_nguon': ['python3', 'ops/land_evidence_nguon.py', '--root', '.'],
    'doctrine_scan': ['python3', '.claude/dev/packet_loop.py', 'doctrine-scan', '--root', '.'],
    't26': ['python3', 'ops/lease_publish_test.py', '--chi-ca=t26_'],
    't27': ['python3', 'ops/lease_publish_test.py', '--chi-ca=t27_'],
    't138': ['python3', 'ops/lease_publish_test.py', '--chi-ca=t138_'],
}
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
summary = {}
for name, cmd in gates.items():
    proc = subprocess.run(cmd, cwd=root, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (out / f'{label}-{name}.log').write_text(proc.stdout)
    (out / f'{label}-{name}.rc').write_text(str(proc.returncode) + '\n')
    lines = proc.stdout.splitlines()
    tail = lines[-6:]
    summary[name] = {'command': cmd, 'rc': proc.returncode, 'tail': tail}
    print(label, name, 'rc=' + str(proc.returncode), '\n' + '\n'.join(tail), flush=True)
(out / f'{label}-gates.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
