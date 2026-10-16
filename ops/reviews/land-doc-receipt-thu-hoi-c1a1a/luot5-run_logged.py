import json, os, pathlib, subprocess, sys, time
out=pathlib.Path(__file__).resolve().parent
label, *cmd=sys.argv[1:]
env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='commit.gpgsign', GIT_CONFIG_VALUE_0='false')
start=time.perf_counter()
try:
 p=subprocess.run(cmd,env=env,capture_output=True,timeout=300)
 rc=p.returncode; stdout=p.stdout; stderr=p.stderr; timeout=False
except subprocess.TimeoutExpired as e:
 rc=None; stdout=e.stdout or b''; stderr=e.stderr or b''; timeout=True
(out/(label+'.stdout')).write_bytes(stdout); (out/(label+'.stderr')).write_bytes(stderr)
r=dict(command=cmd,rc=rc,elapsed=round(time.perf_counter()-start,4),timeout=timeout,stdout_bytes=len(stdout),stderr_bytes=len(stderr))
(out/(label+'.json')).write_text(json.dumps(r,indent=2))
print(json.dumps(r)); print(stdout.decode(errors='replace')[-1200:]); print(stderr.decode(errors='replace')[-1200:])
