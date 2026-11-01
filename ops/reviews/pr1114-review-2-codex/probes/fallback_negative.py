import concurrent.futures,ctypes,importlib.util,json,os,pathlib,subprocess,sys,time
root=pathlib.Path(__file__).resolve().parents[1]
if len(sys.argv)>1:
 variant=sys.argv[1]
 if variant!='head': os.environ['CAC_MA']=str(root/'work/mutations'/(variant+'.py'))
 spec=importlib.util.spec_from_file_location('t',root/'work/head/ops/cloud_agent_creds_test.py')
 t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
 m=t.nap_mod();assert ctypes.CDLL(None).prctl(36,1,0,0,0)==0
 m._SUBREAPER=False
 p=subprocess.Popen(['sh','-c','sleep 30 & echo $!; sleep 30'],stdout=subprocess.PIPE,start_new_session=True)
 time.sleep(.3);start=time.monotonic();da,ra=m._giet_nhom(p);kill_seconds=time.monotonic()-start
 pid=int(ra.split()[0]);start=time.monotonic();alive=t._song_roi_don([pid]);wait_seconds=time.monotonic()-start
 result=dict(variant=variant,subreaper_flag=m._SUBREAPER,da=da,alive=alive,kill_seconds=round(kill_seconds,6),helper_seconds=round(wait_seconds,6))
 try:os.killpg(p.pid,9)
 except ProcessLookupError:pass
 p.wait()
 for _ in range(100):
  try:
   while os.waitpid(-p.pid,os.WNOHANG)[0]>0:pass
  except ChildProcessError:break
  time.sleep(.002)
 print(json.dumps(result),flush=True)
else:
 def run(v):
  r=subprocess.run(['python3','-B',__file__,v],capture_output=True,text=True,timeout=40)
  assert r.returncode==0,(v,r.stdout,r.stderr)
  return json.loads(r.stdout)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: rows=list(pool.map(run,['head','parent_only','no_kill']))
 (root/'evidence/fallback-negative.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(json.dumps(rows),flush=True)
