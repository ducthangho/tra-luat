import concurrent.futures,ctypes,importlib.util,json,os,pathlib,subprocess,sys,time
root=pathlib.Path(__file__).resolve().parents[1]
def stat(pid):
 try:
  parts=pathlib.Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
  return dict(state=parts[0],ppid=int(parts[1]),pgrp=int(parts[2]))
 except FileNotFoundError: return dict(state='gone')
def worker(count):
 sys.path.insert(0,str(root/'work/head/ops'))
 spec=importlib.util.spec_from_file_location('m',root/'work/head/ops/cloud_agent_creds.py')
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 assert ctypes.CDLL(None).prctl(36,1,0,0,0)==0
 m._SUBREAPER=False
 rows=[]
 for i in range(count):
  p=subprocess.Popen(['sh','-c','sleep 30 & echo $!; sleep 30'],stdout=subprocess.PIPE,start_new_session=True)
  time.sleep(.3)
  da,ra=m._giet_nhom(p)
  ts=time.monotonic();g=int(ra.split()[0]);states=[stat(g)]
  while states[-1]['state'] not in ('Z','gone') and time.monotonic()-ts<5:
   states.append(stat(g))
  elapsed=time.monotonic()-ts
  if len(states)>1:
   rows.append(dict(round=i,pid=g,da=da,after_return=states[0],final=states[-1],seconds=elapsed,reads=len(states)))
  # Cleanup only after observing the unassisted transition.
  try: os.killpg(p.pid,9)
  except ProcessLookupError: pass
  for _ in range(20):
   try:
    while os.waitpid(-p.pid,os.WNOHANG)[0]>0: pass
   except ChildProcessError: break
   time.sleep(.001)
 print(json.dumps(dict(total=count,transitions=rows)),flush=True)
if len(sys.argv)>1 and sys.argv[1]=='worker': worker(int(sys.argv[2]))
else:
 def run(i):
  r=subprocess.run(['python3','-B',__file__,'worker','100'],capture_output=True,text=True,timeout=100)
  assert r.returncode==0,(r.stdout,r.stderr)
  return json.loads(r.stdout)
 with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool: rows=list(pool.map(run,range(12)))
 out=dict(total=sum(r['total'] for r in rows),transitions=[x for r in rows for x in r['transitions']])
 (root/'evidence/mechanism.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(out,ensure_ascii=False),flush=True)
