from pathlib import Path
import os,sys,time,subprocess,json
w=Path(__file__).resolve().parent;os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
while not (w/'measure-done').exists():time.sleep(5)
rows=[]
for name in ['domain_review4.py','repro_R4.py']:
 with (w/(name+'.log')).open('w') as f:q=subprocess.run([sys.executable,'-B',str(w/name)],cwd=w,stdout=f,stderr=subprocess.STDOUT)
 rows.append(dict(name=name,rc=q.returncode));(w/'queue-extra.json').write_text(json.dumps(rows));print(rows[-1],flush=True)
(w/'queue-extra-done').write_text('done')
