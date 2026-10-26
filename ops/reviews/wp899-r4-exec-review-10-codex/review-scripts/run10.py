import datetime, hashlib, json, os, pathlib, subprocess, sys, time
R=pathlib.Path(__file__).resolve().parent
label=sys.argv[1];cmd=sys.argv[2:];start=time.time()
p=subprocess.run(cmd,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(R/'tmp')))
for kind,data in [('stdout',p.stdout),('stderr',p.stderr)]: (R/f'{label}.{kind}.txt').write_bytes(data)
r={'command':cmd,'cwd':str(R.parent),'rc':p.returncode,'started_utc':datetime.datetime.fromtimestamp(start,datetime.timezone.utc).isoformat(),'seconds':time.time()-start,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest(),'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr)}
(R/f'{label}.receipt.json').write_text(json.dumps(r,indent=2));print(json.dumps(r));print(p.stdout.decode(errors='replace')[-1600:]);print(p.stderr.decode(errors='replace')[-1000:]);sys.exit(p.returncode)
