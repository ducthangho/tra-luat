from pathlib import Path
import json,subprocess,sys,os,time,shutil
R=Path(__file__).resolve().parent
start=time.monotonic()
while not (R/'suite.stdout.txt').exists():
 if time.monotonic()-start>3600:raise TimeoutError('suite not finished')
 time.sleep(2)
text=(R/'suite.stdout.txt').read_text();assert all(s in text for s in ('CA: 49/49 dat','DOT BIEN: 231/231 bi giet dung ly do','TONG: DAT'))
for n in (1,2):
 shutil.copy2(R/'suite.stdout.txt',R/f'prior{n}/suite.stdout.txt')
 p=R/f'prior{n}/old2/composite_current.py';s=p.read_text().replace('.review/prior2/old2/composite/runner-step.sh',f'.review/prior{n}/old2/composite/runner-step.sh');p.write_text(s)
 # Keep actual measured current stdout for the custom-shell replay, no fabricated marker.
(R/'emit.py').write_text("from pathlib import Path\nimport sys\nsys.stdout.buffer.write((Path('.review')/'suite.stdout.txt').read_bytes())\n")
rows=[]
for n in (1,2):
 for name in ('old2/composite_current.py','run_old.py','registry_check.py'):
  cmd=[sys.executable,'-B',str(R/f'prior{n}'/name)];q=subprocess.run(cmd,capture_output=True,timeout=600)
  rows.append({'label':f'prior{n}-{name}','command':cmd,'rc':q.returncode,'stdout':q.stdout.decode(),'stderr':q.stderr.decode()});print(rows[-1]['label'],q.returncode,flush=True)
(R/'legacy-after-suite6-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
assert all(r['rc']==0 for r in rows)
print('legacy composites + registry + old cases DAT')
