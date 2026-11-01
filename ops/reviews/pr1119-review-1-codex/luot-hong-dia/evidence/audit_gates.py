import concurrent.futures as cf
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
REPO = ROOT / 'cay-kho'
OUT = ROOT / 'evidence'
BASE = 'f4b513da5802d439aedbe58ae4a5cd38ff47d6ab'
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')

def snapshot():
    files = {}
    for p in REPO.rglob('*'):
        if '.git' not in p.relative_to(REPO).parts and p.is_file():
            files[p.relative_to(REPO).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    for cmd in [('status', '--porcelain=v1', '--untracked-files=all', '--ignored'), ('rev-parse', 'HEAD', 'HEAD^{tree}'), ('diff',), ('diff', '--cached')]:
        files['GIT ' + ' '.join(cmd)] = subprocess.check_output(['git', *cmd], cwd=REPO, env=ENV).decode()
    return files

def run(label, name, cmd, cwd):
    start = time.monotonic()
    p = subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True)
    (OUT / f'{label}-{name}.stdout').write_bytes(p.stdout)
    (OUT / f'{label}-{name}.stderr').write_bytes(p.stderr)
    result = dict(label=label, name=name, cmd=cmd, cwd=str(cwd), rc=p.returncode, seconds=round(time.monotonic()-start,3), stdout_bytes=len(p.stdout), stderr_bytes=len(p.stderr))
    print(json.dumps(result), flush=True)
    return result

if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    (OUT / 'original-snapshot.json').write_text(json.dumps(snapshot(), indent=2))
    base = ROOT / 'work/base'
    if not base.exists():
        shutil.copytree(REPO, base, symlinks=True)
        subprocess.run(['git','checkout','--detach',BASE], cwd=base, env=ENV, check=True, capture_output=True)
    direct = "import importlib.util; s=importlib.util.spec_from_file_location('lease_tests','ops/lease_publish_test.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); fs=[f for f in m.CA if f.__name__.startswith(('t26_','t27_'))]; assert len(fs)==3; [(f(),print(f.__name__+' PASS')) for f in fs]"
    commands = [('bien-nhan',['python3','ops/bien_nhan_v2.py','--root','.']), ('land-evidence',['python3','ops/land_evidence_nguon.py','--root','.']), ('t26-t27',['python3','-c',direct]), ('doctrine',['python3','.claude/dev/packet_loop.py','doctrine-scan','--root','.']), ('diff-check',['git','diff','--check',BASE,'HEAD'])]
    with cf.ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(run,label,name,cmd,cwd) for label,cwd in [('base',base),('head',REPO)] for name,cmd in commands]
        results = [f.result() for f in futures]
    (OUT / 'gate-results.json').write_text(json.dumps(results,indent=2))
