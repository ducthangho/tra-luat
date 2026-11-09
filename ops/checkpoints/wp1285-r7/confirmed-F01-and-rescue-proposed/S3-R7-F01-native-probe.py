import base64,csv,ctypes,datetime,hashlib,json,os,pathlib,shutil,subprocess,sys,threading,time,traceback,zipfile,msvcrt
I=pathlib.Path(r'C:\tl-win\wp1285-H4-inputs');M=json.loads((I/'S3-H4-native-manifest.json').read_text());W=pathlib.Path(r'C:\tl-win\wp1285-r7-F01-probe');LOCK=pathlib.Path(r'C:\tl-win\KHOA.txt');SID='wp1285-r7-F01-measure-'+M['candidate'][:12]
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
 assert os.name=='nt' and not W.exists(),'wrong OS or existing evidence; no repeat'
 W.mkdir(parents=True,exist_ok=False)
 for n in ['logs','reports','scratch','harness','operator-inputs']:(W/n).mkdir()
 start=now();before=acquire();save(W/'lock-acquisition.json',{'session':SID,'before':before,'at':start.isoformat()});beat();thread=threading.Thread(target=heart,daemon=True);thread.start();shutil.copyfile(__file__,W/'operator-inputs/controller.py')
 cand=pathlib.Path(r'C:\tl-win\wp1285-H4-native\candidate');assert git(cand,'rev-parse','HEAD',label='head')==M['candidate'];assert not git(cand,'status','--porcelain',label='before-status');sourcebefore=files(cand);save(W/'source-before.json',sourcebefore);assert sha(cand/MT)=='f230c95b1f36b558b2f58439f8ea64cc6f77a876c1d74cc8c9baf1634cc9f864'
 env=os.environ.copy()
 for k in list(env):
  if k.startswith('TL_') or k in ['GH_TOKEN','GITHUB_TOKEN','GITHUB_PAT','CODEX_AUTH_JSON','CLAUDE_CODE_OAUTH_TOKEN','OPENAI_API_KEY','ANTHROPIC_API_KEY','PROXIMA_API_KEY']:env.pop(k,None)
 env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1',POWERSHELL_TELEMETRY_OPTOUT='1')
 pre="$ErrorActionPreference='Stop';$ProgressPreference='SilentlyContinue';$env:PSModulePath=(Join-Path $PSHOME 'Modules')+';C:\Program Files\WindowsPowerShell\Modules';"
 hostprobe=pre+"[pscustomobject]@{host=$env:COMPUTERNAME;service=@(Get-CimInstance Win32_Service -Filter \"Name='ProximaGateway'\").Count;process=@(Get-CimInstance Win32_Process -Filter \"Name='Proxima.exe'\").Count;policy=@(Get-ExecutionPolicy -List)}|ConvertTo-Json -Depth 5 -Compress"
 _,out=run([PS51,'-NoProfile','-NonInteractive','-Command',hostprobe],'host-before',env=env);host=json.loads(out);assert host['host']=='DESKTOP-T9R33P2' and host['service']==host['process']==0;assert all(str(p['ExecutionPolicy']) in ['5','Undefined'] for p in host['policy'] if str(p['Scope']) in ['4','3','MachinePolicy','UserPolicy']);save(W/'host-before.json',host)
 harness=W/'harness/ProximaManifest.Tests.ps1';shutil.copyfile(cand/MT,harness);src=cand/'.agents/skills/proxima-control';manifest=(src/'scripts/ProximaControl.psd1').read_bytes();cases=[('original','en-US',''),('harmless-keyword-prefix','en-US','#requiresX\n'),('harmless-space-comment','en-US','# Requires the S2 hash guard\n'),('genuine-lower','en-US','#requires -Version 5.1\n'),('genuine-upper-tr','tr-TR','#REQUIRES -Version 5.1\n'),('genuine-upper-az','az-Latn-AZ','#REQUIRES -Version 5.1\n')]
 for psid,exe in [('ps51',PS51),('ps7',PS7)]:
  pe=env.copy();pe['PSModulePath']=str(pathlib.Path(exe).parent/'Modules')+r';C:\Program Files\WindowsPowerShell\Modules'
  for name,culture,prefix in cases:
   label=name+'-'+psid;d=W/'scratch'/label;d.mkdir();addon=d/'addon';shutil.copytree(src,addon);mp=addon/'scripts/ProximaControl.psd1';mp.write_bytes(prefix.encode()+manifest);report=W/'reports'/(label+'.json');astreport=W/'reports'/(label+'-ast.json')
   def pq(p):return "'"+str(p).replace("'","''")+"'"
   script=pre+"[Threading.Thread]::CurrentThread.CurrentCulture=[Globalization.CultureInfo]::GetCultureInfo("+pq(culture)+");[Threading.Thread]::CurrentThread.CurrentUICulture=[Globalization.CultureInfo]::GetCultureInfo("+pq(culture)+");$tk=$null;$er=$null;$a=[System.Management.Automation.Language.Parser]::ParseFile("+pq(mp)+",[ref]$tk,[ref]$er);$comments=@($tk|Where-Object{$_.Kind -eq [System.Management.Automation.Language.TokenKind]::Comment});[pscustomobject]@{culture=[Globalization.CultureInfo]::CurrentCulture.Name;PSVersion=$PSVersionTable.PSVersion.ToString();parse_errors=@($er|ForEach-Object{$_.Message});ScriptRequirementsPresent=($null -ne $a.ScriptRequirements);RequiredPSVersion=$(if($a.ScriptRequirements){[string]$a.ScriptRequirements.RequiredPSVersion}else{$null});regex_matches=@($comments|Where-Object{$_.Text -imatch '^#\s*requires'}|ForEach-Object{$_.Text})}|ConvertTo-Json -Depth 6|Set-Content -LiteralPath "+pq(astreport)+" -Encoding UTF8;& "+pq(harness)+" -AddonRoot "+pq(addon)+" -ScratchRoot "+pq(d)+" -ReportPath "+pq(report)+";exit $LASTEXITCODE"
   launcher=W/'harness'/(label+'-launcher.ps1');launcher.write_text(script,encoding='utf-8-sig');pe['TMP']=pe['TEMP']=str(d);pe['PSModuleAnalysisCachePath']=str(d/'ModuleAnalysisCache');rc,_=run([exe,'-NoProfile','-NonInteractive','-ExecutionPolicy','RemoteSigned','-File',str(launcher)],label,env=pe,timeout=120,check=False);rr=json.loads(report.read_text(encoding='utf-8-sig'));ar=json.loads(astreport.read_text(encoding='utf-8-sig'));phases[label]={'name':name,'culture':culture,'shell':psid,'rc':rc,'report':rr,'ast':ar,'report_sha256':sha(report),'manifest_sha256':sha(mp)};ledger(label,rr,rc,results[-1]['seconds'])
 save(W/'measurement.json',{'head':M['candidate'],'harness_sha256':sha(harness),'finding':'WP1285-R7-F01','scope':'Observe unchanged exactH4 harness on owned manifest copies, no remediation/mutation/sourcepatch','phases':phases,'commands':results})
 after=files(cand);save(W/'source-after.json',after);assert after==sourcebefore;assert not git(cand,'status','--porcelain',label='after-status');_,out=run([PS51,'-NoProfile','-NonInteractive','-Command',hostprobe],'host-after',env=env);hostafter=json.loads(out);save(W/'host-after.json',hostafter);assert hostafter['service']==hostafter['process']==0
 assert all(x['report']['setup_error'] is None for x in phases.values());assert all(x['rc']==0 and x['report']['passed']==x['report']['total']==7 for x in phases.values() if x['name']=='original');return 0
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
