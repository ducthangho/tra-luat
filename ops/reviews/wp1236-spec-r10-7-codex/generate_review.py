import os,sys,json,hashlib,subprocess,time,concurrent.futures
from pathlib import Path
W=Path(__file__).resolve().parent;R=W.parent/'repo';M=W.parent/'ma_r9_git';Q=R/'ops/reviews/wp1236-r10-soan/quet_dot_bien.py';K=Q.with_name('kho_dot_bien_reviewer_luot6.jsonl');G=M/'ops/gate_output_doi_chieu.py'
(W/'tmp').mkdir(exist_ok=True)
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(W/'tmp'))
def run(name,args):
 cmd=[sys.executable,'-B',str(Q),*map(str,args)];start=time.monotonic();p=subprocess.run(cmd,cwd=W,env=ENV,capture_output=True)
 (W/(name+'.stdout')).write_bytes(p.stdout);(W/(name+'.stderr')).write_bytes(p.stderr)
 r={'command':cmd,'cwd':str(W),'rc':p.returncode,'seconds':time.monotonic()-start,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()};(W/(name+'.receipt.json')).write_text(json.dumps(r,indent=2));return name,r,p.stdout.decode()
if __name__=='__main__':
 jobs=[('sinh1',['sinh',G,'--ra',W/'m1.jsonl']),('sinh2',['sinh',G,'--ra',W/'m2.jsonl']),('hoi_quy',['hoi-quy',K,'-',G,'--ra',W/'h.jsonl'])]
 with concurrent.futures.ThreadPoolExecutor(3) as ex:
  for r in ex.map(lambda t:run(*t),jobs):print(r,flush=True)
