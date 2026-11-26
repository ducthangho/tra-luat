from pathlib import Path
import subprocess,sys,time,os,json
w=Path(__file__).resolve().parent
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
rows=[]
for label,root,cmd in [
 ('head-B',w/'head',[sys.executable,'-B','ops/land_evidence_nguon_test.py']),
 ('head-A',w/'head',[sys.executable,'-B','ops/gate_output_doi_chieu_test.py']),
 ('head-land',w/'head',[sys.executable,'-B','ops/land_evidence_nguon.py','--root','.']),
 ('head-ci',w/'head',[sys.executable,'-B','.claude/dev/ci_dang_ky_test.py']),
 ('head-selftest',w/'head',[sys.executable,'-B','scripts/tl.py','--selftest']),
 *[(v+'-ruff',w/v,[sys.executable,'-m','ruff','check','--no-cache','--select','F','ops/land_evidence_nguon_test.py','ops/gate_output_doi_chieu_test.py']) for v in ['base','head']]]:
 t=time.monotonic()
 with (w/(label+'.log')).open('w') as f: p=subprocess.run(cmd,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT)
 row=dict(label=label,command=cmd,cwd=str(root),rc=p.returncode,seconds=time.monotonic()-t)
 rows.append(row); (w/'gates.json').write_text(json.dumps(rows,indent=2));print(row,flush=True)
