"""Run byte-for-byte repository scripts in their required original layout.

Use this wrapper alone, with no repository-copying test running concurrently.
Only temporary symlinks are created in cay-kho/ops/reviews, then removed.
"""
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys

BASE=pathlib.Path(__file__).resolve().parents[1]
ROOT=BASE/'cay-kho'
PKG=ROOT/'ops/reviews/pr468-hoso-4-packet-review-6-codex'
OUT=BASE/'do-review7'
REPLAY=OUT/'replay'
REPLAY.mkdir(exist_ok=True)
for name in ['real-results.json','nhanh-rerun.json']:
    shutil.copyfile(PKG/name,REPLAY/name)
shutil.copytree(PKG/'outputs',REPLAY/'outputs',dirs_exist_ok=True)
links={'tai-lieu':BASE/'tai-lieu','cay-kho':ROOT,'do-review':REPLAY}
created=[]
result=[]
try:
    for name,dest in links.items():
        p=PKG.parent/name
        p.symlink_to(dest,target_is_directory=True)
        created.append(p)
    for script in (sys.argv[1:] or ['harness.py','attack_h.py','extra_checks.py']):
        assert script in ['harness.py','attack_h.py','extra_checks.py']
        r=subprocess.run([sys.executable,'-B',str(PKG/script)],cwd=BASE,capture_output=True,text=True,
                         env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_ALLOW_PROTOCOL='file'))
        (OUT/(script+'.rerun.log')).write_text(r.stdout+r.stderr)
        result.append(dict(script=str(PKG/script),rc=r.returncode,source_sha256=hashlib.sha256((PKG/script).read_bytes()).hexdigest()))
        if r.returncode: raise RuntimeError(r.stderr)
finally:
    for p in reversed(created): p.unlink()
(OUT/'package-rerun.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
