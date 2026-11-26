from pathlib import Path
import os,sys,json,subprocess,time,hashlib
w=Path(__file__).resolve().parent;r=w/'head';dest=w/'floor'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
subprocess.run(['git','-c','advice.detachedHead=false','clone','--quiet','--local','--no-hardlinks',str(r),str(dest)],check=True,env=env)
subprocess.run(['git','-C',str(dest),'config','core.abbrev','7'],check=True,env=env)
p=dest/'ops/land_evidence_nguon_test.py';s=p.read_text();cu='bang(rc == 0 and dem[0] - truoc == mong,';moi='bang(rc == 0 and dem[0] - truoc >= mong,';assert s.count(cu)==1;p.write_text(s.replace(cu,moi))
cmd=[sys.executable,'-B','ops/land_evidence_nguon_test.py'];t=time.monotonic()
with (w/'floor-full-B.log').open('w') as f:out=subprocess.run(cmd,cwd=dest,env=env,stdout=f,stderr=subprocess.STDOUT)
row=dict(command=cmd,cwd=str(dest),rc=out.returncode,seconds=time.monotonic()-t,mutant={'cu':cu,'moi':moi},stdout_sha256=hashlib.sha256((w/'floor-full-B.log').read_bytes()).hexdigest())
(w/'floor-full-B.json').write_text(json.dumps(row,ensure_ascii=False,indent=2));print(row,flush=True)
