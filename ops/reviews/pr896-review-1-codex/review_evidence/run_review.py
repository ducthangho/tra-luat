#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import shlex
import subprocess

p = argparse.ArgumentParser()
p.add_argument('number')
p.add_argument('title')
p.add_argument('hypothesis')
p.add_argument('conclusion')
p.add_argument('command', nargs=argparse.REMAINDER)
a = p.parse_args()
root = Path(__file__).resolve().parent.parent
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
print('$ ' + shlex.join(a.command), flush=True)
r = subprocess.run(a.command, cwd=root / 'cay-kho', env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
out = r.stdout
log = root / 'review_evidence' / f'{a.number}.log'
log.write_text('$ ' + shlex.join(a.command) + '\n' + out + f'\nrc={r.returncode}\n', encoding='utf-8')
with (root / 'VERDICT.md').open('a', encoding='utf-8') as f:
    f.write(f'\nHƯỚNG {a.number}: {a.title}\n\n')
    f.write(f'  giả thuyết : {a.hypothesis}\n\n')
    f.write(f'  lệnh       : `cd cay-kho && {shlex.join(a.command)}` (PYTHONDONTWRITEBYTECODE=1)\n\n')
    f.write('  output     :\n\n```text\n' + out.rstrip() + f'\nrc={r.returncode}\n```\n\n')
    f.write(f'  kết luận   : {a.conclusion}\n')
print(out, end='')
print(f'rc={r.returncode}')
