import base64,csv,ctypes,datetime,hashlib,json,os,pathlib,shutil,subprocess,sys,threading,time,traceback,zipfile,msvcrt
I=pathlib.Path(r'C:\tl-win\wp1285-r2-g2-inputs');M=json.loads((I/'S3-native-manifest-recovery4.json').read_text());W=pathlib.Path(r'C:\tl-win\wp1285-r2-g2\F01-H1-native');LOCK=pathlib.Path(r'C:\tl-win\KHOA.txt');SID='wp1285-r2-'+M['candidate'][:12]+'-F01H1'
GIT=r'C:\tl-win\wp1271-tools\mingit-2.56.0.4\cmd\git.exe';PS51=r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe';PS7=r'C:\Program Files\PowerShell\7\pwsh.exe'
REL='.agents/skills/proxima-control/scripts/ProximaControl.psm1';TEST='.agents/skills/proxima-control/tests/ProximaControl.Tests.ps1';MT='.agents/skills/proxima-control/tests/ProximaManifest.Tests.ps1'
stop=threading.Event();taken=False;start=None;thread=None;results=[];phases={};lockfile=None;mu=threading.Lock()
def now():return datetime.datetime.now(datetime.timezone.utc)
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=True)+'\n',encoding='utf-8')
def say(v):print(json.dumps(v,ensure_ascii=True),flush=True)
def own():return LOCK.exists() and LOCK.read_text(encoding='utf-8-sig').split('\t')[0]==SID
# Share READ only: competing writers cannot overwrite a live lock. Writes/heartbeat use this held handle.
def lockwrite(text):
 with mu:
  lockfile.seek(0)
  if text:lockfile.write(text)
  lockfile.truncate();lockfile.flush();os.fsync(lockfile.fileno())
def beat():
 if not own():raise RuntimeError('machine-lock ownership lost')
 n=now()
 if n>start+datetime.timedelta(hours=1):raise RuntimeError('machine-lock deadline exceeded')
 lockwrite('\t'.join([SID,start.isoformat(),(start+datetime.timedelta(hours=1)).isoformat(),'wp1285 focused native PS51/7',n.isoformat()])+'\n')
 with (W/'heartbeat-readbacks.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps({'at':n.isoformat(),'readback':LOCK.read_text(encoding='utf-8-sig')})+'\n')
def heart():
 while not stop.wait(30):
  try:beat()
  except Exception as e:say({'heartbeat_error':str(e)});stop.set();return

def run(args,label,env=None,cwd=None,timeout=1200,check=True):
 if stop.is_set() or (start and now()>start+datetime.timedelta(hours=2)):raise RuntimeError('ownership/deadline lost')
 say({'start':label});t=time.monotonic();p=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env,cwd=cwd)
 try:out,_=p.communicate(timeout=timeout)
 except subprocess.TimeoutExpired:
  subprocess.run(['taskkill','/PID',str(p.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);out,_=p.communicate();(W/'logs'/f'{label}.log').write_bytes(out);raise RuntimeError('owned test timeout '+label)
 log=W/'logs'/f'{label}.log';log.write_bytes(out);row={'label':label,'command':args,'rc':p.returncode,'seconds':round(time.monotonic()-t,3),'log_sha256':sha(log)};results.append(row)
 with (W/'command-receipts.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(row)+'\n')
 say({'finished':label,'rc':p.returncode,'seconds':row['seconds']})
 if check and p.returncode:raise RuntimeError(label+' failed rc='+str(p.returncode))
 return p.returncode,out.decode('utf-8',errors='replace').strip()
def git(repo,*args,label):return run([GIT,'-C',str(repo),*args],label)[1]
def ledger(label,rep,rc,seconds):
 p=pathlib.Path(r'C:\tl-win\do-luong.csv');exists=p.exists() and p.stat().st_size>0
 with p.open('a',encoding='utf-8',newline='') as f:
  w=csv.writer(f)
  if not exists:w.writerow(['thoi_diem','session','packet','sha','bo_test','dat','tong','ca_do','thoi_luong_s','phat_hien_boi','loi_that','da_va','ghi_chu'])
  w.writerow([now().isoformat(),SID,'wp1285',M['baseline'] if label.startswith('baseline') else (M['old_h3'] if label.startswith('old-h3') else M['candidate']),label,rep.get('passed',0),rep.get('total',0),'|'.join(rep.get('failed_ids',[])),seconds,'focused-local','not_classified','no',f'may=DESKTOP-T9R33P2;device=a5f7076e-a491-4f84-829b-8d1fbcc1c767;ngat=khong;rc={rc}'])
def files(repo):return {str(p.relative_to(repo)).replace(chr(92),'/'):sha(p) for p in repo.rglob('*') if p.is_file() and '.git' not in p.relative_to(repo).parts}

def acquire():
 global lockfile,taken
 k=ctypes.WinDLL('kernel32',use_last_error=True);k.CreateFileW.restype=ctypes.c_void_p;k.CreateFileW.argtypes=[ctypes.c_wchar_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p]
 h=k.CreateFileW(str(LOCK),0x80000000|0x40000000,1,None,4,0x80,None)
 if h==ctypes.c_void_p(-1).value:raise OSError(ctypes.get_last_error(),'native lock busy/unavailable')
 fd=msvcrt.open_osfhandle(h,os.O_RDWR|os.O_BINARY);lockfile=os.fdopen(fd,'r+',encoding='utf-8-sig',newline='');before=lockfile.read();assert not before.strip(),'foreign machine-lock owner';taken=True;lockwrite(SID+'\tBOOTSTRAP\n');return before

def main():
 global start,thread
 assert os.name=='nt' and not W.exists();W.mkdir(parents=True)
 for n in ['logs','reports','scratch','harness']:(W/n).mkdir()
 start=now();before=acquire();save(W/'lock-acquisition.json',{'session':SID,'before':before,'at':start.isoformat()});beat();thread=threading.Thread(target=heart,daemon=True);thread.start()
 src=pathlib.Path(r'C:\tl-win\wp1285-r2-g2\H4196fbaaeb13-recovery4\candidate');assert git(src,'rev-parse','HEAD',label='source-head')==M['candidate'];original=files(src);shutil.copytree(src/'.agents/skills/proxima-control',W/'mutated-addon');manifest=W/'mutated-addon/scripts/ProximaControl.psd1';old=manifest.read_text(encoding='utf-8-sig');new="end {\n"+old+"\n}\nclean { 'PM01_CLEAN_PROBE' }\n";manifest.write_text(new,encoding='utf-8');harness=W/'harness/ProximaManifest.Tests.ps1';shutil.copyfile(src/MT,harness);save(W/'mutation.json',{'finding':'WP1285-R1-F01','original_sha256':hashlib.sha256(old.encode()).hexdigest(),'mutated_sha256':sha(manifest),'shape':'end { unchanged hashtable } clean { harmless literal only }','arbitrary_side_effect':False,'harness_sha256':sha(harness)})
 env=os.environ.copy();env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1');observed={}
 for psid,exe in [('ps51',PS51),('ps7',PS7)]:
  d=W/'scratch'/psid;d.mkdir();rp=W/'reports'/(psid+'.json');pe=env.copy();pe['PSModulePath']=str(pathlib.Path(exe).parent/'Modules')+r';C:\Program Files\WindowsPowerShell\Modules';pe['TMP']=pe['TEMP']=str(d);pe['PSModuleAnalysisCachePath']=str(d/'ModuleAnalysisCache');args=[exe,'-NoProfile','-NonInteractive','-ExecutionPolicy','RemoteSigned','-File',str(harness),'-AddonRoot',str(W/'mutated-addon'),'-ScratchRoot',str(d),'-ReportPath',str(rp)];rc,_=run(args,'F01-H1-'+psid,env=pe,check=False);r=json.loads(rp.read_text(encoding='utf-8-sig'));case=next(c for c in r['cases'] if c['id']=='PM01');observed[psid]={'actual_rc':rc,'PM01':case,'runtime_children':r['runtime_children'],'setup_error':r['setup_error'],'before_import_rejected':case['outcome']=='failed' and r['runtime_children']==0,'report_sha256':sha(rp)};phases[psid]={'rc':rc,'report':r};ledger('F01-H1-'+psid,r,rc,0)
 assert files(src)==original;save(W/'probe-result.json',{'finding':'WP1285-R1-F01','H':M['candidate'],'observed':observed,'reproduced':not observed['ps7']['before_import_rejected'],'original_source_unchanged':True});return 0 if not observed['ps7']['before_import_rejected'] and observed['ps51']['before_import_rejected'] else 1

rc=2
try:rc=main()
except BaseException as e:
 if W.exists():save(W/'operator-failure.json',{'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),'commands':results,'phases':phases,'at':now().isoformat()})
 say({'operator_error':str(e)});rc=2
finally:
 stop.set()
 if thread:thread.join(timeout=5)
 if taken:
  try:
   assert own();lockwrite('');save(W/'lock-release.json',{'session':SID,'released':True,'at':now().isoformat(),'after':LOCK.read_text(encoding='utf-8-sig')})
  except Exception as e:
   if W.exists():save(W/'lock-release-error.json',{'error':str(e)});rc=2
 if lockfile:lockfile.close()
 if W.exists():
  save(W/'terminal.json',{'rc':rc,'at':now().isoformat(),'candidate':M['candidate'],'phase_count':len(phases)})
  # Archive only declared operator/evidence/retained fixture inputs; sparse cloned source bytes are small and retained, .git excluded.
  manifest={str(p.relative_to(W)).replace('\\','/'):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(W.rglob('*')) if p.is_file() and '.git' not in p.relative_to(W).parts and p.name!='source-byte-manifest.json'};save(W/'source-byte-manifest.json',manifest);z=W.parent/(W.name+'-evidence.zip')
  with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as zz:
   for p in sorted(W.rglob('*')):
    if p.is_file() and '.git' not in p.relative_to(W).parts:zz.write(p,str(p.relative_to(W)).replace('\\','/'))
  raw=base64.b64encode(z.read_bytes()).decode();b64=z.with_suffix(z.suffix+'.b64');b64.write_text('\n'.join(raw[i:i+4096] for i in range(0,len(raw),4096)),encoding='ascii')
  save(W.parent/(W.name+'-archive.json'),{'zip':str(z),'bytes':z.stat().st_size,'sha256':sha(z),'b64':str(b64),'base64_bytes':len(raw),'source_files':len(manifest),'rc':rc});say({'terminal_rc':rc,'archive':str(z),'sha256':sha(z),'source_files':len(manifest)})
sys.exit(rc)
