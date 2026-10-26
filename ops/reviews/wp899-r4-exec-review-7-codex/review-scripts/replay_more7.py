from pathlib import Path
import subprocess,sys,os,json,time
R=Path(__file__).resolve().parent
jobs=[('historical-targets','replay_targets6.py',[]),('operators','operators6.py',[]),('operator-errors','operator_errors6.py',[]),('normalization','replay_norm6.py',[]),('frontier5','frontier5_current.py',[]),('signatures','signature6.py',[]),('reanchors','reanchor6.py',[]),('legacy-cli','repair6.py',[]),('legacy-remaining','remaining5.py',[]),('after-suite','after_suite6.py',[]),('a10-details','a10checks6.py',[])]
rows=[]
for label,name,args in jobs:
 p=subprocess.run([sys.executable,'-B',str(R/'run.py'),label,sys.executable,'-B',str(R/name),*args],capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 rows.append({'label':label,'driver_rc':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()});(R/'replay-more7-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(label,p.returncode,flush=True)
