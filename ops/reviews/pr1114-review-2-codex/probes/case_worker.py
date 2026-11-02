import ctypes, json, os, pathlib, signal, subprocess, sys, time
root=pathlib.Path(__file__).resolve().parents[1]
variant,case=sys.argv[1:]
assert ctypes.CDLL(None).prctl(36,1,0,0,0)==0
script=root/'work/head/ops'/('review_a9_default.py' if variant=='a9_default' else 'cloud_agent_creds_test.py')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
if variant in ('parent_only','no_kill'):
 env['CAC_MA']=str(root/'work/mutations'/(variant+'.py'))
cmd=['python3',str(script),'--mot-ca',case]
log=root/'evidence'/f'case-{variant}-{case}.log'
t=time.monotonic()
with log.open('w') as f:
 p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,env=env,start_new_session=True)
 try: rc=p.wait(timeout=160)
 except subprocess.TimeoutExpired:
  os.killpg(p.pid,signal.SIGKILL);rc=p.wait()
elapsed=time.monotonic()-t
# Reap/clean only children belonging to this isolated worker after result has been recorded.
cleanup=[]
for _ in range(100):
 try:
  while os.waitpid(-1,os.WNOHANG)[0]>0: pass
 except ChildProcessError: break
 children=pathlib.Path(f'/proc/{os.getpid()}/task/{os.getpid()}/children').read_text().split()
 for x in children:
  try: os.kill(int(x),9);cleanup.append(int(x))
  except ProcessLookupError: pass
 time.sleep(.02)
row=dict(variant=variant,case=case,command=cmd,cac_ma=env.get('CAC_MA'),rc=rc,seconds=round(elapsed,6),output=log.read_text(),cleanup_pids=sorted(set(cleanup)))
print(json.dumps(row,ensure_ascii=False),flush=True)
