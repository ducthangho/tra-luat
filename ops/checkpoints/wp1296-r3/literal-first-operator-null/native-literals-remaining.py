import base64,csv,ctypes,datetime,hashlib,json,os,pathlib,shutil,subprocess,sys,threading,time,traceback,zipfile,msvcrt
I=pathlib.Path(r'C:\tl-win\wp1296-H2-inputs');M=json.loads((I/'manifest.json').read_text());W=pathlib.Path(r'C:\tl-win\wp1296-H2-literals-remaining');LOCK=pathlib.Path(r'C:\tl-win\KHOA.txt');SID='wp1296-H2-literals-remaining-'+M['candidate'][:12]
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
 lockwrite('\t'.join([SID,start.isoformat(),(start+datetime.timedelta(hours=1)).isoformat(),'wp1296 focused native PS51/7',n.isoformat()])+'\n')
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
  w.writerow([now().isoformat(),SID,'wp1296',M['baseline'] if label.startswith('baseline') else (M['old_h3'] if label.startswith('old-h3') else M['candidate']),label,rep.get('passed',0),rep.get('total',0),'|'.join(rep.get('failed_ids',[])),seconds,'focused-local','not_classified','no',f'may=DESKTOP-T9R33P2;device=a5f7076e-a491-4f84-829b-8d1fbcc1c767;ngat=khong;rc={rc}'])
def files(repo):return {str(p.relative_to(repo)).replace(chr(92),'/'):sha(p) for p in repo.rglob('*') if p.is_file() and '.git' not in p.relative_to(repo).parts}

def acquire():
 global lockfile,taken
 k=ctypes.WinDLL('kernel32',use_last_error=True);k.CreateFileW.restype=ctypes.c_void_p;k.CreateFileW.argtypes=[ctypes.c_wchar_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p]
 h=k.CreateFileW(str(LOCK),0x80000000|0x40000000,1,None,4,0x80,None)
 if h==ctypes.c_void_p(-1).value:raise OSError(ctypes.get_last_error(),'native lock busy/unavailable')
 fd=msvcrt.open_osfhandle(h,os.O_RDWR|os.O_BINARY);lockfile=os.fdopen(fd,'r+',encoding='utf-8-sig',newline='');before=lockfile.read();assert not before.strip(),'foreign machine-lock owner';taken=True;lockwrite(SID+'\tBOOTSTRAP\n');return before


def main():
 global start,thread
 assert os.name=='nt' and not W.exists(),'wrongOS or existingevidence; do not repeat'
 W.mkdir(parents=True)
 for n in ['logs','reports','scratch','harness','operator-inputs','evidence']:(W/n).mkdir()
 env=os.environ.copy()
 for k in list(env):
  if k.startswith('TL_') or k in ['GH_TOKEN','GITHUB_TOKEN','GITHUB_PAT','CODEX_AUTH_JSON','CLAUDE_CODE_OAUTH_TOKEN','OPENAI_API_KEY','ANTHROPIC_API_KEY','PROXIMA_API_KEY']:env.pop(k,None)
 env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1',POWERSHELL_TELEMETRY_OPTOUT='1')
 pre="$ErrorActionPreference='Stop';$ProgressPreference='SilentlyContinue';$env:PSModulePath=(Join-Path $PSHOME 'Modules')+';C:\\Program Files\\WindowsPowerShell\\Modules';"
 probe=pre+"[pscustomobject]@{host=$env:COMPUTERNAME;service=@(Get-CimInstance Win32_Service -Filter \"Name='ProximaGateway'\").Count;process=@(Get-CimInstance Win32_Process -Filter \"Name='Proxima.exe'\").Count;python=@(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\"|Select-Object ProcessId,ParentProcessId,CreationDate,ExecutablePath);policy=@(Get-ExecutionPolicy -List)}|ConvertTo-Json -Depth 5 -Compress"
 _,out=run([PS51,'-NoProfile','-NonInteractive','-Command',probe],'host-before',env=env);host=json.loads(out);save(W/'host-before.json',host);assert host['host']=='DESKTOP-T9R33P2' and host['service']==host['process']==0
 assert all(str(p['ExecutionPolicy']) in ['5','Undefined'] for p in host['policy'] if str(p['Scope']) in ['4','3','MachinePolicy','UserPolicy'])
 start=now();before=acquire();save(W/'lock-acquisition.json',{'session':SID,'before':before,'at':start.isoformat()});beat();thread=threading.Thread(target=heart,daemon=True);thread.start()
 base=I/'base';cand=I/'candidate'
 for root,key in [(base,'base_files'),(cand,'candidate_files')]:
  assert files(root)==M[key],('sourceexportmismatch',key)
 shutil.copyfile(__file__,W/'operator-inputs/controller.py');shutil.copyfile(I/'manifest.json',W/'operator-inputs/manifest.json')
 shutil.copytree(base,W/'operator-inputs/base');shutil.copytree(cand,W/'operator-inputs/candidate')
 common=W/'harness/ProximaManifest.Tests.ps1';shutil.copyfile(cand/MT,common);legacy=W/'harness/ProximaControl.Tests.ps1';shutil.copyfile(cand/TEST,legacy)
 rollback=W/'harness/rollback-requirements-only.ps1';text=common.read_text(encoding='utf-8-sig');anchor='    Assert-NoScriptRequirements $ast';assert text.count(anchor)==1;rollback.write_text(text.replace(anchor,'    # operator private rollback: requirements call intentionally removed'),encoding='utf-8')
 save(W/'rollback-only.json',{'source':sha(common),'mutant':sha(rollback),'anchor':anchor,'replacement':'only guard call removed; other AST guards retained'})
 def pq(v):return "'"+str(v).replace("'","''")+"'"
 def phase(label,exe,psid,source,harness=None,prefix='',culture='en-US',shape=None,cx=False,old=False):
  d=W/'scratch'/label;d.mkdir();addon=d/'addon';shutil.copytree(source/'.agents/skills/proxima-control',addon);mf=addon/'scripts/ProximaControl.psd1';orig=mf.read_text(encoding='utf-8-sig')
  assert orig.count("'ProximaControl.psm1'")==1
  changed=orig.replace("'ProximaControl.psm1'","'#REQUIRES -Version 5.1'")
  if shape:changed=orig.rstrip()+' &\n' if shape=='background' else 'end {\n'+orig+'\n}\n'+("clean { 'WP1296_CLEAN_CONTROL' }\n" if shape=='end-clean' else '')
  if True:mf.write_text(changed,encoding='utf-8')
  rp=W/'reports'/(label+'.json');ap=W/'reports'/(label+'-parser.json');pe=env.copy();pe['PSModulePath']=str(pathlib.Path(exe).parent/'Modules')+r';C:\Program Files\WindowsPowerShell\Modules';pe['TEMP']=pe['TMP']=str(d);pe['PSModuleAnalysisCachePath']=str(d/'ModuleAnalysisCache')
  if old:
   ev=W/'evidence'/label;ev.mkdir();args=[exe,'-NoProfile','-NonInteractive','-ExecutionPolicy','RemoteSigned','-File',str(legacy),'-ModulePath',str(addon/'scripts/ProximaControl.psm1'),'-ScratchRoot',str(d),'-ReportPath',str(rp),'-EvidenceRoot',str(ev),'-TestCulture',culture]
  else:
   h=harness or common
   script=pre+"[Threading.Thread]::CurrentThread.CurrentCulture=[Globalization.CultureInfo]::GetCultureInfo("+pq(culture)+");[Threading.Thread]::CurrentThread.CurrentUICulture=[Globalization.CultureInfo]::GetCultureInfo("+pq(culture)+");$tk=$null;$er=$null;$ast=[System.Management.Automation.Language.Parser]::ParseFile("+pq(mf)+",[ref]$tk,[ref]$er);[pscustomobject]@{culture=[Globalization.CultureInfo]::CurrentCulture.Name;PSVersion=$PSVersionTable.PSVersion.ToString();errors=@($er|ForEach-Object{$_.Message});requirements=$ast.ScriptRequirements;api_members=@([System.Management.Automation.Language.ScriptBlockAst].GetProperty('ScriptRequirements').PropertyType.GetProperties([Reflection.BindingFlags]'Public,Instance')|ForEach-Object{$_.Name})}|ConvertTo-Json -Depth 8|Set-Content -LiteralPath "+pq(ap)+" -Encoding UTF8;& "+pq(h)+" -AddonRoot "+pq(addon)+" -ScratchRoot "+pq(d)+" -ReportPath "+pq(rp)+( ' -Counterexamples' if cx else '')+";exit $LASTEXITCODE"
   launch=W/'harness'/(label+'.ps1');launch.write_text(script,encoding='utf-8-sig');args=[exe,'-NoProfile','-NonInteractive','-ExecutionPolicy','RemoteSigned','-File',str(launch)]
  rc,_=run(args,label,env=pe,timeout=180,check=False);assert rp.exists(),('REPORT_ABSENT',label);rr=json.loads(rp.read_text(encoding='utf-8-sig'));assert rr['setup_error'] is None,(label,rr['setup_error'])
  ar=json.loads(ap.read_text(encoding='utf-8-sig')) if ap.exists() else None;row={'rc':rc,'report':rr,'parser':ar,'culture':culture,'shell':psid,'source_harness_sha256':sha(harness or common) if not old else sha(legacy),'manifest_sha256':sha(mf),'prefix':prefix,'shape':shape};phases[label]=row;ledger(label,rr,rc,results[-1]['seconds']);save(W/'phase-progress.json',{'phases':phases,'commands':results});return row
 def pm(row,id):return next(x for x in row['report']['cases'] if x['id']==id)
 def reject(row,semantic=True):
  rr=row['report'];reason=pm(row,'PM01')['reason'];assert row['rc']==1 and pm(row,'PM01')['outcome']=='failed' and rr['runtime_children']==0 and pm(row,'PM04')['reason'].startswith('NOT_EXECUTED:'),(reason,rr)
  assert reason.startswith('EXECUTABLE_STATEMENT:') if semantic else reason.startswith(('EXECUTABLE_STATEMENT:','PARSE_ERROR:'))
 def inert(row):
  ar=row['parser'];rr=row['report'];expected={'RequiredApplicationId','RequiredPSVersion','RequiredPSEditions','RequiredModules','RequiredAssemblies','IsElevationRequired'}
  assert ar['PSVersion']=='7.6.9' and not ar['errors'] and set(ar['api_members'])==expected and set(ar['requirements'])==expected
  assert (ar['requirements'] is None or all(v in [None,False,[], ''] for v in ar['requirements'].values())) and row['rc']==0 and rr['passed']==rr['total']==7 and rr['runtime_children']==2 and pm(row,'PM01')['outcome']==pm(row,'PM02')['outcome']=='passed'
  row['classification']='inert_legacy_control';row['credited_semantic_kill']=False
 def ownedledger(label,expected):
  raw=pathlib.Path(r'C:\tl-win\do-luong.csv').read_bytes();lines=raw.splitlines(keepends=True)
  ids={'wp1296-H2-literals-'+M['candidate'][:12],'wp1296-H2-native-'+M['candidate'][:12],'wp1296-H2-completion-'+M['candidate'][:12],SID}
  selected=[line for line in lines[1:] if next(csv.reader([line.decode('utf-8-sig')]))[1] in ids]
  assert len(selected)==expected,(label,len(selected),expected)
  dest=W/(label+'.csv');dest.write_bytes(lines[0]+b''.join(selected))
  save(W/(label+'.json'),{'source':r'C:\tl-win\do-luong.csv','source_sha256':hashlib.sha256(raw).hexdigest(),'selected_rows':len(selected),'selected_sha256':sha(dest),'session_ids':sorted(ids),'other_rows_not_archived':True})
 save(W/'source-before-filehashes.json',{'base':files(base),'candidate':files(cand)})
 ownedledger('owned-ledger-before',90)
 for psid,exe in [('ps51',PS51),('ps7',PS7)]:
  for culture in ['en-US','tr-TR','az-Latn-AZ']:
   if psid=='ps51' and culture=='en-US':continue
   q=phase('literal-'+culture+'-'+psid,exe,psid,cand,culture=culture)
   ar=q['parser'];rr=q['report']
   assert not ar['errors'] and (ar['requirements'] is None or all(v in [None,False,[], ''] for v in ar['requirements'].values()))
   assert q['rc']==1 and pm(q,'PM01')['outcome']=='passed' and pm(q,'PM02')['outcome']=='failed' and pm(q,'PM02')['reason']=='VALUE[RootModule]'
   assert rr['runtime_children']==0 and pm(q,'PM04')['reason'].startswith('NOT_EXECUTED:')
   q['classification']='literal_data_PM01_positive_strictschema_PM02_negative';q['credited_semantic_kill']=False
 ownedledger('owned-ledger-after',95)
 save(W/'source-after-filehashes.json',{'base':files(base),'candidate':files(cand)})
 assert (W/'source-before-filehashes.json').read_bytes()==(W/'source-after-filehashes.json').read_bytes()
 assert files(base)==M['base_files'] and files(cand)==M['candidate_files'];_,out=run([PS51,'-NoProfile','-NonInteractive','-Command',probe],'host-after',env=env);hostafter=json.loads(out);save(W/'host-after.json',hostafter);assert hostafter['service']==hostafter['process']==0
 save(W/'measurement.json',{'candidate':M['candidate'],'baseline':M['baseline'],'source_export':'Gitcommitted scopedbytes with filehashmanifest; not a nativefullGitcheckout','phases':phases,'commands':results,'originals_unchanged':True,'passed':True,'literal_schema_supplement_only':True,'not_full7_positive_or_semantic_kill':True,'carried_first_run_archive':'a83e932f656b7d54c275704ba947f889f393b89fdea1725a644d1659be4121d1','AUX1_oracle_disposition':'inert_legacy_control','no_network_inference_activation':True,'finished':now().isoformat()});return 0
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
