from pathlib import Path
import subprocess,sys,os,json,time,concurrent.futures
R=Path(__file__).resolve().parent
jobs=[]
for n in (1,2):
 d=R/f'prior{n}'
 for name in ('preflight.py','calendar_cases.py','new_probes_r4.py','classifier_negative.py','q1_time_detail.py','run_old.py','finish_probes.py','trace_c44_current.py','verify_new_cases.py','registry_check.py','shape_audit.py','reviewer_cases_r4.py'):
  if (d/name).exists(): jobs.append((f'prior{n}-{name}',[sys.executable,'-B',str(d/name)]))
 for sub in ('old1','old2'):
  for name in ('probes.py','r4_compare_current.py','extra_mutants.py','new_probes_current.py','boundary_current.py','composite_current.py'):
   if (d/sub/name).exists():jobs.append((f'prior{n}-{sub}-{name}',[sys.executable,'-B',str(d/sub/name)]))
rows=[]
def one(x):
 label,cmd=x;t=time.time();q=subprocess.run(cmd,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),timeout=900)
 d=R/'legacy6';d.mkdir(exist_ok=True);(d/(label+'.stdout')).write_bytes(q.stdout);(d/(label+'.stderr')).write_bytes(q.stderr)
 return {'label':label,'command':cmd,'rc':q.returncode,'seconds':time.time()-t,'stdout_tail':q.stdout.decode('utf8','replace')[-1500:],'stderr_tail':q.stderr.decode('utf8','replace')[-1000:]}
with concurrent.futures.ThreadPoolExecutor(3) as ex:
 for v in ex.map(one,jobs):
  rows.append(v);(R/'legacy6-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(v['label'],v['rc'],flush=True)
