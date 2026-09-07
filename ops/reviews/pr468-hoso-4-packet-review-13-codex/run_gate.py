import datetime as dt
import json
import os
from pathlib import Path
import subprocess
import sys
import time

BASE=Path(__file__).resolve().parent.parent
OUT=BASE/'do-review13'
(OUT/'tmp').mkdir(exist_ok=True)
env=dict(os.environ,TMPDIR=str(OUT/'tmp'),PYTHONDONTWRITEBYTECODE='1',GIT_ALLOW_PROTOCOL='file')
name,*cmd=sys.argv[1:]
start=dt.datetime.now(dt.timezone.utc)
t=time.monotonic()
p=subprocess.run(cmd,cwd=BASE/'cay-kho',env=env,capture_output=True)
(OUT/(name+'.stdout')).write_bytes(p.stdout)
(OUT/(name+'.stderr')).write_bytes(p.stderr)
row={'command':cmd,'cwd':'cay-kho','started_utc':start.isoformat(),'ended_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
     'elapsed_seconds':round(time.monotonic()-t,3),'rc':p.returncode,'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr)}
(OUT/(name+'.json')).write_text(json.dumps(row,indent=2)+'\n')
print(json.dumps(row))
print(p.stdout.decode(errors='replace')[-1300:])
print(p.stderr.decode(errors='replace')[-600:])
