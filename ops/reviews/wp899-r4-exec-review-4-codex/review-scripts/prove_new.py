from pathlib import Path
import os,sys,subprocess,json,importlib.util
R=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('b',R/'boundary_cases.py');b=importlib.util.module_from_spec(s);s.loader.exec_module(b)
rows=[]
for label in b.LABELS:
 for mut in (None,R/'new-frontier'/(label+'.py')):
  if mut and not mut.exists():continue
  cmd=[sys.executable,'-B',str(R/'boundary_cases.py'),label];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
  if mut:env['CI_PROVENANCE_MA']=str(mut)
  p=subprocess.run(cmd,env=env,capture_output=True);o=(p.stdout+p.stderr).decode()
  rows.append({'label':label,'source':str(mut) if mut else 'HEAD','command':cmd,'rc':p.returncode,'output':o,'rank':'baseline_passed' if p.returncode==0 and not mut else 'GIET' if mut and p.returncode==3 and o.startswith('DO:'+label+':') else 'ERROR'})
  (R/'new-counterexamples.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(label,'mutant' if mut else 'HEAD',p.returncode,flush=True)
