from pathlib import Path
import os,sys,subprocess,shutil,json
R=Path(__file__).resolve().parent
assert (R/'suite.stdout.txt').exists()
for n in (1,2):shutil.copy2(R/'suite.stdout.txt',R/f'prior{n}/suite.stdout.txt')
rows=[]
for n in (1,2):
 d=R/f'prior{n}'
 for name in ('run_old.py','registry_check.py'):
  cmd=[sys.executable,'-B',str(d/name)];p=subprocess.run(cmd,capture_output=True)
  rows.append({'label':f'prior{n}-{name}','command':cmd,'rc':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()})
 p=d/'old2/composite_current.py'
 if p.exists():
  cmd=[sys.executable,'-B',str(p)];q=subprocess.run(cmd,capture_output=True)
  rows.append({'label':f'prior{n}-composite-current','command':cmd,'rc':q.returncode,'stdout':q.stdout.decode(),'stderr':q.stderr.decode()})
 (R/'legacy-final-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print('round',n,[(r['label'],r['rc']) for r in rows],flush=True)
