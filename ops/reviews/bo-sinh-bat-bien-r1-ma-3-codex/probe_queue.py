from pathlib import Path
import subprocess,os,sys,time,json,concurrent.futures
w=Path(__file__).resolve().parent;env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
while True:
 try:done=json.loads((w/'gates.json').read_text())
 except (FileNotFoundError,json.JSONDecodeError):done=[]
 if any(x['label']=='head-A' for x in done):break
 time.sleep(10)
subprocess.run(['git','clone','-q',str(w/'head'),str(w/'mut')],check=True)
rows=[]
def run(name,args):
 t=time.monotonic()
 with (w/(name+'.log')).open('w') as f:p=subprocess.run([sys.executable,'-B',*args],cwd=w,env=env,stdout=f,stderr=subprocess.STDOUT)
 row=dict(name=name,command=[sys.executable,'-B',*args],rc=p.returncode,seconds=time.monotonic()-t);rows.append(row);(w/'probe-queue.json').write_text(json.dumps(rows,indent=2));print(row,flush=True)
def lane(tasks):
 for name,args in tasks:run(name,args)
lanes=[
 [('table',['bang_toan_tu.py','--goc',str(w/'head'),'--ra',str(w/'table'),'--song-song','3'])],
 [(n,[n+'.py']) for n in ['probes','excess_probe','distinct_target','guard_witnesses','b02_targeted','trace_v2','count_audit']],
 [(n,[n+'.py']) for n in ['tool_audit','independent','cache_review']],
]
with concurrent.futures.ThreadPoolExecutor(3) as ex:list(ex.map(lane,lanes))
(w/'probes-done').write_text('complete\n')
