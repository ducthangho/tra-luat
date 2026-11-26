from pathlib import Path
import os,sys,time,subprocess,json,shutil
w=Path(__file__).resolve().parent;os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
while not (w/'measure-done').exists():time.sleep(5)
rows=[]
for name in ['probes.py','excess_probe.py','trace_v2.py','guard_witnesses.py','data_domain_probe.py','b02_targeted.py','distinct_target.py']:
 shutil.copy(w.parent/'lich_su/luot3'/name,w/name)
subprocess.run(['git','clone','-q',str(w/'head'),str(w/'mut')],check=True)
for name,cmd in [('table',[sys.executable,'-B',str(w/'bang_toan_tu.py'),'--goc',str(w/'head'),'--ra',str(w/'table'),'--song-song','3']),*[(n,[sys.executable,'-B',str(w/n)]) for n in ['repro_R3.py','probes.py','excess_probe.py','trace_v2.py','guard_witnesses.py','data_domain_probe.py','b02_targeted.py','distinct_target.py','ast_review.py','domain_review4.py','cache_review4.py','tool_review4.py']]]:
 print('START',name,flush=True)
 with (w/(name+'.log')).open('w') as f:q=subprocess.run(cmd,cwd=w,stdout=f,stderr=subprocess.STDOUT)
 rows.append(dict(name=name,command=cmd,rc=q.returncode));(w/'queue.json').write_text(json.dumps(rows,indent=2));print(rows[-1],flush=True)
(w/'queue-done').write_text('done')
