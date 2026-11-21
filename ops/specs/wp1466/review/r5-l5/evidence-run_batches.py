from pathlib import Path
import subprocess,os,concurrent.futures,json,time
O=Path(__file__).resolve().parent
os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(O/'tmp'),GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='commit.gpgsign',GIT_CONFIG_VALUE_0='false')
(O/'tmp').mkdir(exist_ok=True)
jobs={k:['python3','-B',str(O/'sc/chay5.py'),str(O/'prototype'),str(O/'tmp/suite'),k] for k in ['ca','adr','moi','cu']}
jobs.update({k:['python3','-B',str(O/'sc/thu_pv5.py'),str(O),k[3:],'2'] for k in ['pv_ma','pv_test']})
jobs['preflight19']=['python3','-B',str(O/'sc/fx_tien_kiem.py'),str(O),str(O/'base/ops/lease_publish.py')]
jobs['registry']=['python3','-B',str(O/'sc/so_dang_ky.py'),str(O/'base'),str(O/'prototype')]
def run(item):
 k,cmd=item;t=time.time()
 with (O/(k+'.log')).open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
 result=dict(job=k,rc=r.returncode,seconds=round(time.time()-t,1));print(json.dumps(result),flush=True);return result
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:results=list(ex.map(run,jobs.items()))
(O/'batches.json').write_text(json.dumps(results,indent=2))
