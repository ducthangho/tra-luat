from pathlib import Path
import subprocess,sys,os,json,time,concurrent.futures
R=Path(__file__).resolve().parent
jobs=[]
for n in (1,2):
 d=R/f'prior{n}'
 for name in ('preflight.py','calendar_cases.py','new_probes_r4.py','classifier_negative.py','q1_time_detail.py','run_old.py'):
  jobs.append((f'prior{n}-{name}',[sys.executable,'-B',str(d/name)]))
 for sub in ('old1','old2'):
  for name in ('probes.py','r4_compare.py','r4_compare_current.py','extra_mutants.py'):
   if (d/sub/name).exists():jobs.append((f'prior{n}-{sub}-{name}',[sys.executable,'-B',str(d/sub/name)]))
  if sub=='old2':
   for name in ('boundary_case.py','boundary_current.py','composite_case.py','composite_current.py','new_probes.py','new_probes_current.py'):
    if (d/sub/name).exists():jobs.append((f'prior{n}-{sub}-{name}',[sys.executable,'-B',str(d/sub/name)]))
 # legacy shape and mutation drivers will be run sequentially, after these probes
rows=[]
def run(job):
 label,cmd=job;t=time.time();p=subprocess.run(cmd,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(R/'tmp'),TMP=str(R/'tmp'),TEMP=str(R/'tmp')),timeout=600)
 out=R/'prior-results';out.mkdir(exist_ok=True)
 (out/(label+'.stdout')).write_bytes(p.stdout);(out/(label+'.stderr')).write_bytes(p.stderr)
 return {'label':label,'command':cmd,'rc':p.returncode,'seconds':time.time()-t,'stdout_tail':p.stdout.decode('utf8','replace')[-1000:],'stderr_tail':p.stderr.decode('utf8','replace')[-500:]}
with concurrent.futures.ThreadPoolExecutor(4) as ex:
 for v in ex.map(run,jobs):
  rows.append(v);(R/'prior-reruns.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)); print(v['label'],v['rc'],flush=True)
