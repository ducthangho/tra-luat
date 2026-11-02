import argparse
import os
from pathlib import Path
import shlex
import subprocess
import time

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT / 'cay-kho'
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1',
           PYTHONIOENCODING='utf-8', RUFF_NO_CACHE='1', GIT_OPTIONAL_LOCKS='0',
           GIT_ALLOW_PROTOCOL='file')

def record(name, title, command, output, rc=0, conclusion='KHÔNG PHẢI LỖI'):
    path = ROOT / 'evidence' / (name + '.log')
    path.write_text(output, encoding='utf-8')
    shown = output
    if len(shown) > 14000:
        shown = shown[:1800] + '\n[… rút gọn; log đầy đủ ở đường dẫn bên dưới …]\n' + shown[-11000:]
    with (ROOT / 'VERDICT.md').open('a', encoding='utf-8') as f:
        f.write(f'\n### {name} — {title}\n\nLỆNH:\n```sh\n{command}\n```\n\nOUTPUT THẬT (rc={rc}):\n```text\n{shown.rstrip()}\n```\n\nLog đầy đủ: [evidence/{name}.log](evidence/{name}.log).\n\nKết luận: **{conclusion}**.\n')
    print(f'{name}: rc={rc}; log={path.relative_to(ROOT)}', flush=True)
    if len(output) > 7000:
        print(output[:500] + '\n[…]\n' + output[-6000:], flush=True)
    else:
        print(output, flush=True)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('name')
    p.add_argument('title')
    p.add_argument('--cwd', default=str(REPO))
    p.add_argument('command', nargs=argparse.REMAINDER)
    a = p.parse_args()
    cmd = a.command[1:] if a.command[:1] == ['--'] else a.command
    start = time.monotonic()
    r = subprocess.run(cmd, cwd=a.cwd, env=ENV, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True, encoding='utf-8')
    out = r.stdout + f'\n[exit_code={r.returncode}; elapsed_seconds={time.monotonic()-start:.3f}]\n'
    command = 'cd cay-kho\nPYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 RUFF_NO_CACHE=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file ' + shlex.join(cmd)
    record(a.name, a.title, command, out, r.returncode,
           'KHÔNG PHẢI LỖI' if r.returncode == 0 else 'CHỜ PHÂN LOẠI')
