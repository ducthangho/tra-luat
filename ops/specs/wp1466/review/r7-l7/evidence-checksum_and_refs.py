from pathlib import Path
import subprocess,hashlib,datetime,json
O=Path('out');S=Path('cay-kho');print('UTC',datetime.datetime.now(datetime.timezone.utc).isoformat())
for a,b in [('out/hunt.py','cay-kho/ops/specs/wp1466/review/r6-l6/evidence-hunt.py'),('out/followup.py','cay-kho/ops/specs/wp1466/review/r6-l6/evidence-followup.py'),('out/sc/fx_tien_kiem.py','cay-kho/ops/specs/wp1466/tien-kiem-r6/sc/fx_tien_kiem.py')]:print('UNMODIFIED',a,Path(a).read_bytes()==Path(b).read_bytes())
for f in ['0053-tran-kich-thuoc-sensitive-len-sau-tep.md','0055-tran-loi-goi-codex-len-muoi.md']:
 print('ADR',f)
ref=subprocess.check_output(['git','-C',str(S),'for-each-ref','--format=%(objectname) %(refname)','refs/remotes/origin'],text=True).splitlines();print('REF_COUNT',len([l for l in ref if not l.endswith('/HEAD')]))
for f in ['git','python3','ruff']:
 r=subprocess.run([f,'--version'],capture_output=True,text=True);print('VERSION',f,r.returncode,(r.stdout+r.stderr).strip())
