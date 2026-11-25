import subprocess,os,pathlib,time,json,hashlib
R=pathlib.Path(__file__).resolve().parents[1]/'repo';W=R.parent/'work';E=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(W/'tmp'))
results=[]
for name,script in [('missing','probe_missing.py'),('scope','probe_scope.py')]:
 args=['python3','-B',str(R.parent/'lich_su'/script)];t=time.monotonic();p=subprocess.run(args,cwd=R,env=E,capture_output=True)
 (W/(name+'.stdout.log')).write_bytes(p.stdout);(W/(name+'.stderr.log')).write_bytes(p.stderr)
 d=dict(name=name,command=args,rc=p.returncode,status='passed' if p.returncode==0 else 'failed',seconds=time.monotonic()-t,stdout_sha256=hashlib.sha256(p.stdout).hexdigest(),stdout_log=name+'.stdout.log',stderr_log=name+'.stderr.log',tested_sha='bca55c1cd09c57180d60b05d5ca1813828ae1d10');results.append(d);print(name,p.returncode,flush=True)
(W/'confirm-checks.json').write_text(json.dumps(results,indent=2))
