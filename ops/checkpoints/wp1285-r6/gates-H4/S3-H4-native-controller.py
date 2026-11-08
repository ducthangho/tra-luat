import base64,csv,ctypes,datetime,hashlib,json,os,pathlib,shutil,subprocess,sys,threading,time,traceback,zipfile,msvcrt
I=pathlib.Path(r'C:\tl-win\wp1285-H4-inputs');M=json.loads((I/'S3-H4-native-manifest.json').read_text());W=pathlib.Path(M['native_root']);LOCK=pathlib.Path(r'C:\tl-win\KHOA.txt');SID='wp1285-r6-'+M['candidate'][:12]+'-g7-H4'
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
 assert os.name=='nt' and not W.exists(),'wrong OS or existing evidence (do not relaunch)'
 W.mkdir(parents=True,exist_ok=False)
 for n in ['logs','reports','scratch','harness','evidence','operator-inputs']:(W/n).mkdir()
 start=now();before=acquire();save(W/'lock-acquisition.json',{'session':SID,'before':before,'at':start.isoformat(),'lock_write_sharing':'READonly heldhandle'});beat();thread=threading.Thread(target=heart,daemon=True);thread.start()
 for p in I.iterdir():
  if p.is_file():shutil.copyfile(p,W/'operator-inputs'/p.name)
 env=os.environ.copy()
 for key in list(env):
  if key.startswith('TL_') or key in ['GH_TOKEN','GITHUB_TOKEN','GITHUB_PAT','CODEX_AUTH_JSON','CLAUDE_CODE_OAUTH_TOKEN','OPENAI_API_KEY','ANTHROPIC_API_KEY','PROXIMA_API_KEY']:env.pop(key,None)
 env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1',POWERSHELL_TELEMETRY_OPTOUT='1');env['PATH']=str(pathlib.Path(GIT).parent)+';'+str(pathlib.Path(PS7).parent)+';'+env.get('PATH','')
 pre="$ErrorActionPreference='Stop';$ProgressPreference='SilentlyContinue';$env:PSModulePath=(Join-Path $PSHOME 'Modules')+';C:\\Program Files\\WindowsPowerShell\\Modules'; "
 probe=pre+"[pscustomobject]@{host=$env:COMPUTERNAME;service=@(Get-CimInstance Win32_Service -Filter \"Name='ProximaGateway'\" -ErrorAction Stop).Count;process=@(Get-CimInstance Win32_Process -Filter \"Name='Proxima.exe'\" -ErrorAction Stop).Count;python=@(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" -ErrorAction Stop|Select-Object ProcessId,CreationDate,CommandLine);policy=@(Get-ExecutionPolicy -List);memory=@(Get-CimInstance Win32_OperatingSystem|Select-Object FreePhysicalMemory,TotalVisibleMemorySize,FreeVirtualMemory,TotalVirtualMemorySize)}|ConvertTo-Json -Depth 5 -Compress"
 _,out=run([PS51,'-NoProfile','-NonInteractive','-Command',probe],'host-before',env=env);host=json.loads(out);host['GetACP']=ctypes.windll.kernel32.GetACP();save(W/'host-before.json',host);assert host['host']=='DESKTOP-T9R33P2' and host['service']==host['process']==0;assert all(str(p['ExecutionPolicy']) in ['5','Undefined'] for p in host['policy'] if str(p['Scope']) in ['4','3','MachinePolicy','UserPolicy'])
 bundle=W/'candidate.bundle';bundle.write_bytes(base64.b64decode((I/'S3-H4-native.bundle.b64').read_text()));assert sha(bundle)==M['bundle_sha256'];source=pathlib.Path(M['Windows_source_repo']);assert source.is_dir(),'prior verified source repo unavailable; no fallback clone'
 base=W/'baseline';cand=W/'candidate'
 run([GIT,'clone','--no-hardlinks','--no-checkout',str(source),str(base)],'clone-base');git(base,'bundle','verify',str(bundle),label='bundle-verify');git(base,'fetch',str(bundle),M['bundle_ref']+':refs/heads/wp1285-import-H4',label='import-bundle');run([GIT,'clone','--no-hardlinks','--no-checkout',str(base),str(cand)],'clone-H')
 for name,repo in [('baseline',base),('candidate',cand)]:
  for k,v in [('core.autocrlf','false'),('core.eol','lf'),('core.abbrev','7')]:git(repo,'config',k,v,label=name+'-'+k)
  git(repo,'sparse-checkout','set','--no-cone','/.gitattributes','/SKILL.md','/docs/PROTOCOL_DA_PHIEN.md','/.agents/skills/proxima-control/',label=name+'-sparse');git(repo,'checkout','--detach',M[name],label=name+'-checkout')
 ids={}
 for name,repo in [('baseline',base),('candidate',cand)]:
  x={'sha':git(repo,'rev-parse','HEAD',label=name+'-sha'),'tree':git(repo,'rev-parse','HEAD^{tree}',label=name+'-tree'),'parents':git(repo,'show','-s','--format=%P','HEAD',label=name+'-parents').split()};ids[name]=x;assert x=={'sha':M[name],'tree':M['baseline_tree' if name=='baseline' else 'tree'],'parents':M['baseline_parents' if name=='baseline' else 'parents']}
  for p,h in M['baseline_file_sha256' if name=='baseline' else 'file_sha256'].items():assert sha(repo/p)==h,(name,p)
 save(W/'identity.json',{'manifest':M,'actual':ids,'host':host['host'],'lock_session':SID});common=W/'harness'/'ProximaManifest.Tests.ps1';shutil.copyfile(cand/MT,common);legacy=W/'harness'/'ProximaControl.Tests.ps1';shutil.copyfile(cand/TEST,legacy);beforefiles={'baseline':files(base),'candidate':files(cand)};save(W/'before-file-hashes.json',beforefiles)
 def measure(name,repo,exe,psid,cx=False,old=False):
  label=name+'-'+psid+('-CX' if cx else '');sc=W/'scratch'/label;sc.mkdir();rp=W/'reports'/(label+'.json');ev=W/'evidence'/label;ev.mkdir();pe=env.copy();pe['PSModulePath']=str(pathlib.Path(exe).parent/'Modules')+r';C:\Program Files\WindowsPowerShell\Modules';pe['TEMP']=pe['TMP']=str(sc);pe['PSModuleAnalysisCachePath']=str(sc/'ModuleAnalysisCache')
  if old:args=[exe,'-NoProfile','-NonInteractive','-ExecutionPolicy','RemoteSigned','-File',str(legacy),'-ModulePath',str(repo/REL),'-ScratchRoot',str(sc),'-ReportPath',str(rp),'-EvidenceRoot',str(ev),'-TestCulture','en-US']
  else:args=[exe,'-NoProfile','-NonInteractive','-ExecutionPolicy','RemoteSigned','-File',str(common),'-AddonRoot',str(repo/'.agents/skills/proxima-control'),'-ScratchRoot',str(sc),'-ReportPath',str(rp)]
  if cx:args+=['-Counterexamples']
  t=time.monotonic();rc,_=run(args,label,env=pe,timeout=min(1200,max(1,int((start+datetime.timedelta(hours=1)-now()).total_seconds()))),check=False);rep=json.loads(rp.read_text(encoding='utf-8-sig')) if rp.exists() else {'setup_error':'REPORT_ABSENT','passed':0,'total':0,'cases':[]};phases[label]={'rc':rc,'report':rep,'report_path':str(rp),'report_sha256':sha(rp) if rp.exists() else None,'kind':'legacyS2normal' if old else ('S3CX' if cx else 'S3normal')};ledger(label,rep,rc,round(time.monotonic()-t,3));save(W/'phase-progress.json',{'phases':phases,'commands':results});return phases[label]
 normal=True;expected=set(M['normal_ids'])
 for psid,exe in [('ps51',PS51),('ps7',PS7)]:
  b=measure('baseline',base,exe,psid);h=measure('candidate',cand,exe,psid)
  normal &= b['rc']==1 and b['report'].get('total')==7 and b['report'].get('passed')==0 and not b['report'].get('setup_error') and {c['id'] for c in b['report']['cases']}==expected and all(c['outcome']=='failed' and ('MANIFEST_ABSENT' in str(c.get('reason')) or 'SKILL_ABSENT' in str(c.get('reason'))) for c in b['report']['cases'])
  normal &= h['rc']==0 and h['report'].get('total')==h['report'].get('passed')==7 and not h['report'].get('setup_error') and {c['id'] for c in h['report']['cases']}==expected
 cxok=False
 if normal:
  cxok=True
  for psid,exe in [('ps51',PS51),('ps7',PS7)]:
   x=measure('candidate',cand,exe,psid,cx=True);rr=x['report'];cxok &= x['rc']==0 and rr.get('passed')==rr.get('total')==12 and len(rr.get('counterexamples',[]))==5 and all(q.get('credited') is True for q in rr.get('counterexamples',[]) if q['id']!='CX00')
 oldok=True
 for psid,exe in [('ps51',PS51),('ps7',PS7)]:
  q=measure('legacy-S2',cand,exe,psid,old=True);oldok &= q['rc']==0 and q['report'].get('total')==q['report'].get('passed')==26 and not q['report'].get('setup_error')

 # Extra finding-class closure probes, preserving all original normal/CX/legacy phases and counts.
 closure=[]
 for shape in ['named-end','end-clean','background']:
  for psid,exe in [('ps51',PS51),('ps7',PS7)]:
   label='F01-'+shape+'-'+psid;d=W/'scratch'/label;d.mkdir();add=d/'addon';shutil.copytree(cand/'.agents/skills/proxima-control',add);mf=add/'scripts/ProximaControl.psd1';original=mf.read_text(encoding='utf-8-sig');changed=(original.rstrip()+' &\n') if shape=='background' else ('end {\n'+original+'\n}\n'+("clean { 'PM01_CLEAN_PROBE' }\n" if shape=='end-clean' else ''));mf.write_text(changed,encoding='utf-8');rp=W/'reports'/(label+'.json');pe=env.copy();pe['PSModulePath']=str(pathlib.Path(exe).parent/'Modules')+r';C:\Program Files\WindowsPowerShell\Modules';pe['TMP']=pe['TEMP']=str(d);pe['PSModuleAnalysisCachePath']=str(d/'ModuleAnalysisCache');args=[exe,'-NoProfile','-NonInteractive','-ExecutionPolicy','RemoteSigned','-File',str(common),'-AddonRoot',str(add),'-ScratchRoot',str(d),'-ReportPath',str(rp)];rc,_=run(args,label,env=pe,check=False);rr=json.loads(rp.read_text(encoding='utf-8-sig'));pm=next(c for c in rr['cases'] if c['id']=='PM01');pm04=next(c for c in rr['cases'] if c['id']=='PM04');safe=rc==1 and rr['setup_error'] is None and pm['outcome']=='failed' and rr['runtime_children']==0 and pm04['reason'].startswith('NOT_EXECUTED:') and (pm['reason'].startswith('EXECUTABLE_STATEMENT:') or (psid=='ps51' and shape in ['end-clean','background'] and pm['reason'].startswith('PARSE_ERROR:')));assert safe,(label,pm,rr['runtime_children']);phases[label]={'rc':rc,'report':rr,'report_path':str(rp),'report_sha256':sha(rp),'kind':'F01closure'};closure.append({'label':label,'shape':shape,'PM01':pm,'runtime_children':rr['runtime_children'],'before_import_rejection':safe,'manifest_sha256':sha(mf),'replacement':changed,'report':str(rp)});ledger(label,rr,rc,0)

 # Roll back ONLY the newly added background rejection, preserving all other H3 checks.
 oldh=W/'harness'/'rollback-background-only-ProximaManifest.Tests.ps1';text=common.read_text(encoding='utf-8-sig')
 anchor="if ($pr.Name -ceq 'Background') { if ($v) { Stop-Case 'EXECUTABLE_STATEMENT: background pipeline' }; continue }"
 replacement="if ($pr.Name -ceq 'Background') { continue }"
 assert text.count(anchor)==1;oldh.write_text(text.replace(anchor,replacement),encoding='utf-8');save(W/'background-only-mutation.json',{'source_harness_sha256':sha(common),'mutant_harness_sha256':sha(oldh),'anchor':anchor,'replacement':replacement,'count':1})
 d=W/'scratch'/'F01-background-ps7';rp=W/'reports'/'F01-rollback-background-only-ps7.json';pe=env.copy();pe['PSModulePath']=str(pathlib.Path(PS7).parent/'Modules')+r';C:\Program Files\WindowsPowerShell\Modules';pe['TMP']=pe['TEMP']=str(d);pe['PSModuleAnalysisCachePath']=str(d/'ModuleAnalysisCache-rollback');args=[PS7,'-NoProfile','-NonInteractive','-ExecutionPolicy','RemoteSigned','-File',str(oldh),'-AddonRoot',str(d/'addon'),'-ScratchRoot',str(d),'-ReportPath',str(rp)];rc,_=run(args,'F01-rollback-background-only-ps7',env=pe,check=False);rr=json.loads(rp.read_text(encoding='utf-8-sig'));pm=next(c for c in rr['cases'] if c['id']=='PM01');assert rc==1 and rr['setup_error'] is None and pm['outcome']=='passed' and rr['runtime_children']==2;phases['F01-rollback-background-only-ps7']={'rc':rc,'report':rr,'report_path':str(rp),'report_sha256':sha(rp),'kind':'F01rollbackMutant'};save(W/'F01-closure.json',{'finding':'WP1285-R1-F01','candidate':M['candidate'],'positive_control':'original7of7/12of12both mandatory','negatives':closure,'rollback_mutant':{'mutant_harness_sha256':sha(oldh),'PM01':pm,'runtime_children':rr['runtime_children'],'actual_rc':rc,'new_beforeimport_property_failed':True,'not_arbitrary_code_execution_claim':True}})

 afterfiles={'baseline':files(base),'candidate':files(cand)};save(W/'after-file-hashes.json',afterfiles);assert beforefiles==afterfiles,'fixture/source checkout bytes changed';dirty={n:git(r,'status','--porcelain',label=n+'-status') for n,r in [('baseline',base),('candidate',cand)]};assert not any(dirty.values());_,out=run([PS51,'-NoProfile','-NonInteractive','-Command',probe],'host-after',env=env);after=json.loads(out);save(W/'host-after.json',after);assert after['service']==after['process']==0
 final={'candidate':M['candidate'],'baseline':M['baseline'],'normal_comparison_passed':bool(normal),'counterexamples_passed':bool(cxok),'legacy_S2_normal_passed':bool(oldok),'CX_not_run_reason':None if normal else 'normal comparison failed; no killcredit','phases':phases,'identities':ids,'dirty':dirty,'commands':results,'finished_at':now().isoformat()};save(W/'measurement.json',final);return 0 if normal and cxok and oldok else 1
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
