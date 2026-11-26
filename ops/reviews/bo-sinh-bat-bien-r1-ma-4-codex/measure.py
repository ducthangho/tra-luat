from pathlib import Path
import subprocess,sys,time,os,json
w=Path(__file__).resolve().parent
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
rows=[]
def run(label,side,cmd,**meta):
 print('START',label,flush=True);t=time.monotonic()
 with (w/(label+'.log')).open('w') as f:p=subprocess.run(cmd,cwd=w/side,env=env,stdout=f,stderr=subprocess.STDOUT)
 row=dict(label=label,side=side,command=cmd,cwd=str(w/side),rc=p.returncode,seconds=time.monotonic()-t,**meta);rows.append(row)
 (w/'measure.json').write_text(json.dumps(rows,indent=2));print(row,flush=True)
for kind,script,n in [('A','ops/gate_output_doi_chieu_test.py',3),('B','ops/land_evidence_nguon_test.py',2)]:
 for sample in range(1,n+1):
  for side in (['base','head'] if sample%2 else ['head','base']):run(f'{side}-{kind}-{sample}',side,[sys.executable,'-B',script],kind=kind,sample=sample)
for side in ['base','head']:
 for case in ['a135','a136','c40']:
  script='ops/'+('gate_output_doi_chieu_test.py' if case[0]=='a' else 'land_evidence_nguon_test.py')
  # exact case names only exist at head; base records absence, then combined current cases measured separately
  import ast
  names=[x.name for x in ast.parse((w/side/script).read_text()).body if isinstance(x,ast.FunctionDef) and x.name.startswith(case+'_')]
  if not names:
   rows.append(dict(label=f'{side}-{case}',status='absent_at_base',seconds=None));continue
  for i in range(3):run(f'{side}-{case}-{i}',side,[sys.executable,'-B',script,'--mot-ca',names[0]])
for label,side,cmd in [('head-land','head',[sys.executable,'-B','ops/land_evidence_nguon.py','--root','.']),('head-ci','head',[sys.executable,'-B','.claude/dev/ci_dang_ky_test.py']),*[(s+'-selftest',s,[sys.executable,'-B','scripts/tl.py','--selftest']) for s in ['base','head']],*[(s+'-ruff',s,[sys.executable,'-m','ruff','check','--no-cache','--select','F','ops/land_evidence_nguon_test.py','ops/gate_output_doi_chieu_test.py']) for s in ['base','head']]]:run(label,side,cmd)
(w/'measure-done').write_text('done')
