import datetime as dt, hashlib, json, os, pathlib, subprocess, sys, time
BASE=pathlib.Path(__file__).resolve().parents[1]; OUT=BASE/'do-review8'
name=sys.argv[1]; cmd=sys.argv[2:]
env=dict(os.environ,PATH='/usr/local/bin:'+os.environ['PATH'],PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(OUT/'tmp'),GIT_ALLOW_PROTOCOL='file')
start=dt.datetime.now(dt.timezone.utc).isoformat(); t=time.monotonic()
r=subprocess.run(cmd,cwd=BASE/'cay-kho',env=env,capture_output=True)
for suf,data in [('stdout',r.stdout),('stderr',r.stderr)]: (OUT/(name+'.'+suf)).write_bytes(data)
info=dict(name=name,command=cmd,start_utc=start,end_utc=dt.datetime.now(dt.timezone.utc).isoformat(),seconds=time.monotonic()-t,rc=r.returncode,stdout_bytes=len(r.stdout),stdout_sha256=hashlib.sha256(r.stdout).hexdigest(),stderr_bytes=len(r.stderr))
(OUT/(name+'.json')).write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(info,ensure_ascii=False)); print(r.stdout[-800:].decode(errors='replace')); print(r.stderr[-800:].decode(errors='replace'))
