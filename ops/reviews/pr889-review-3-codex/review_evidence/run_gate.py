import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
repo = root / 'cay-kho'
mode = sys.argv[1]
commands = {
    'doctrine': ['python3', '.claude/dev/packet_loop.py', 'doctrine-scan', '--root', '.'],
    'doc-claims': ['python3', 'scripts/tl.py', 'doc-claims-check', '--json'],
}
cmd = commands[mode]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
p = subprocess.run(cmd, cwd=repo, env=env, capture_output=True, text=True)
log = root / 'review-evidence' / (mode + '.log')
log.write_text(p.stdout + p.stderr, encoding='utf-8')
print('command:', ' '.join(cmd))
print('rc:', p.returncode)
print(p.stdout[-6000:])
if p.stderr:
    print('stderr:', p.stderr[-1000:])
(root / 'review-evidence' / (mode + '.rc')).write_text(str(p.returncode) + '\n')
