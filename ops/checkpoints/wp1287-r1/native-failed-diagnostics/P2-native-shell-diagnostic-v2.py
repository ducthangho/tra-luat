import pathlib,ctypes,msvcrt,os,sys,json,datetime,subprocess,threading,time,hashlib,csv,zipfile,base64,traceback,shutil
I=pathlib.Path(r'C:\tl-win\wp1287-inputs');M=json.loads((I/'shell-diagnostic-v2-manifest.json').read_text());W=pathlib.Path(M['root']);SID='wp1287-'+M['candidate'][:12];LOCK=pathlib.Path(r'C:\tl-win\KHOA.txt');stop=threading.Event();held=None;taken=False;start=datetime.datetime.now(datetime.timezone.utc);mu=threading.Lock();rc=2
PS=r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe';PY=r'C:\tl-win\wp1271-tools\python-3.12.10\python.exe'
def now():return datetime.datetime.now(datetime.timezone.utc)
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(p,v):pathlib.Path(p).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
def owns():return LOCK.read_text(encoding='utf-8-sig').split('\t')[0]==SID
def write(t):
 with mu:held.seek(0);held.write(t);held.truncate();held.flush();os.fsync(held.fileno())
def beat():
 assert owns();n=now();assert n<start+datetime.timedelta(hours=1);write('\t'.join([SID,start.isoformat(),(start+datetime.timedelta(hours=1)).isoformat(),'P2 pinned CLI controlled fixture',n.isoformat()])+'\n')
 with (W/'heartbeats.jsonl').open('a') as f:f.write(json.dumps({'at':n.isoformat(),'readback':LOCK.read_text(encoding='utf-8-sig')})+'\n')
def heart():
 while not stop.wait(30):
  try:beat()
  except Exception:stop.set();return

def host(label):
 code="$ErrorActionPreference='Stop';$ProgressPreference='SilentlyContinue';$env:PSModulePath=(Join-Path $PSHOME 'Modules')+';C:\\Program Files\\WindowsPowerShell\\Modules';[pscustomobject]@{host=$env:COMPUTERNAME;python=@(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" |Select-Object ProcessId,CreationDate,CommandLine);gateway=@(Get-CimInstance Win32_Service -Filter \"Name='ProximaGateway'\" -ErrorAction Stop).Count;Proxima=@(Get-CimInstance Win32_Process -Filter \"Name='Proxima.exe'\" -ErrorAction Stop).Count;memory=Get-CimInstance Win32_OperatingSystem|Select-Object FreePhysicalMemory,FreeVirtualMemory;policy=@(Get-ExecutionPolicy -List)}|ConvertTo-Json -Depth 6 -Compress"
 r=subprocess.run([PS,'-NoProfile','-NonInteractive','-EncodedCommand',base64.b64encode(code.encode('utf-16-le')).decode()],capture_output=True,timeout=30);(W/(label+'.stdout')).write_bytes(r.stdout);(W/(label+'.stderr')).write_bytes(r.stderr);assert r.returncode==0;v=json.loads(r.stdout.decode('utf-8-sig'));save(W/(label+'.json'),v);assert v['host']=='DESKTOP-T9R33P2' and v['gateway']==v['Proxima']==0;return v
try:
 assert os.name=='nt' and not W.exists();W.mkdir(parents=True);save(W/'manifest.json',M)
 k=ctypes.WinDLL('kernel32',use_last_error=True);k.CreateFileW.restype=ctypes.c_void_p;k.CreateFileW.argtypes=[ctypes.c_wchar_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p];handle=k.CreateFileW(str(LOCK),0xc0000000,1,None,4,0x80,None);assert handle!=ctypes.c_void_p(-1).value,'machine lock held';held=os.fdopen(msvcrt.open_osfhandle(handle,os.O_RDWR|os.O_BINARY),'r+',encoding='utf-8-sig',newline='');before=held.read();assert not before.strip(),'foreign lock owner';taken=True;write(SID+'\tBOOTSTRAP\n');beat();thread=threading.Thread(target=heart,daemon=True);thread.start();host('host-before')
 install=W/'installation';install.mkdir();inputs=W/'inputs';inputs.mkdir()
 for filename,h in M['inputs'].items():
  source=I/filename;assert sha(source)==h,(filename,'input hash mismatch');(inputs/filename).write_bytes(source.read_bytes())
 for name in ['package.json','package-lock.json','SKILL.md']:(install/name).write_bytes((I/name).read_bytes())
 if M.get('reuse_browser_cache'):shutil.copytree(M['reuse_browser_cache'],W/'browser-cache')
 measure={'candidate':M['candidate'],'tree':M['tree'],'TargetId':'DESKTOP-T9R33P2/a5f7076e-a491-4f84-829b-8d1fbcc1c767','input_hash_bridge':M['source_file_sha256'],'node':r'C:\Program Files\nodejs\node.exe','npm_cli':r'C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js','node_version':'26.13.0','npm_version':'11.20.0','install_root':str(install),'browser_cache':str(W/'browser-cache'),'evidence_root':str(W/'browser-evidence'),'pdf_parser_wheel':str(inputs/'pypdf-6.10.0-py3-none-any.whl'),'pdf_parser_sha256':'90005e959e1596c6e6c84c8b0ad383285b3e17011751cedd17f2ce8fcdfc86de'};measure.update(diagnostic_only=True,diagnostic_checkpoint='https://github.com/ducthangho/tra-luat/issues/1287#issuecomment-6724675093');save(W/'measure-manifest.json',measure)
 env=os.environ.copy();env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1');cmd=[PY,'-B',str(inputs/'P2-browser-measure-shell-diagnostic-v2.py'),str(W/'measure-manifest.json')]
 with (W/'operator.stdout').open('wb') as out:
  p=subprocess.Popen(cmd,stdout=out,stderr=subprocess.STDOUT,env=env,cwd=W)
  while p.poll() is None:
   if stop.wait(2) or now()>start+datetime.timedelta(minutes=55):
    subprocess.run(['taskkill','/PID',str(p.pid),'/T','/F'],capture_output=True);raise RuntimeError('owned operator deadline/lock lost; interrupted')
  rc=p.returncode
 save(W/'operator-command.json',{'command':cmd,'actual_rc':rc,'stdout_sha256':sha(W/'operator.stdout')});host('host-after');assert all(sha(install/name)==M['source_file_sha256'][name] for name in ['package.json','package-lock.json','SKILL.md']);assert rc==0,'controlled CLI fixture failed';assert json.loads((W/'browser-evidence/receipt.json').read_text())['passed'] is True
except BaseException as e:save(W/'failure.json',{'type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc()});rc=2
finally:
 stop.set()
 if taken:
  try:assert owns();write('');save(W/'lock-release.json',{'released':True,'after':LOCK.read_text(encoding='utf-8-sig'),'at':now().isoformat()})
  except Exception as e:save(W/'lock-release-error.json',{'error':str(e)});rc=2
 if held:held.close()
 if W.exists():
  save(W/'terminal.json',{'rc':rc,'at':now().isoformat(),'candidate':M['candidate']});ledger=pathlib.Path(r'C:\tl-win\do-luong.csv');exists=ledger.exists() and ledger.stat().st_size>0
  with ledger.open('a',encoding='utf-8',newline='') as f:
   cw=csv.writer(f)
   if not exists:cw.writerow(['thoi_diem','session','packet','sha','bo_test','dat','tong','ca_do','thoi_luong_s','phat_hien_boi','loi_that','da_va','ghi_chu'])
   cw.writerow([now().isoformat(),SID,'wp1287',M['candidate'],'P2 controlled CLI full flow',1 if rc==0 else 0,1,'' if rc==0 else 'operator/fixture-failed',(now()-start).total_seconds(),'focused-local','unclassified','no','may=DESKTOP-T9R33P2;ngat=khong;rc='+str(rc)])
  # Retain all proof/input/config/source bytes; reproducible tool installation/cache remain on host and are identified by manifests, not huge evidence duplicates.
  selected=[p for p in W.rglob('*') if p.is_file() and not p.is_relative_to(W/'installation/node_modules') and not p.is_relative_to(W/'browser-cache') and not p.is_relative_to(W/'browser-evidence/npm-cache')];manifest={str(p.relative_to(W)).replace('\\','/'):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in selected};save(W/'source-byte-manifest.json',manifest);selected.append(W/'source-byte-manifest.json');z=W.with_name(W.name+'-evidence.zip')
  with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as zz:
   for p in selected:zz.write(p,str(p.relative_to(W)).replace('\\','/'))
  raw=base64.b64encode(z.read_bytes()).decode();z.with_suffix('.zip.b64').write_text('\n'.join(raw[i:i+4096] for i in range(0,len(raw),4096)),encoding='ascii');a={'zip':str(z),'bytes':z.stat().st_size,'sha256':sha(z),'source_files':len(manifest),'base64_bytes':len(raw),'rc':rc};save(W.with_name(W.name+'-archive.json'),a);print(json.dumps(a),flush=True)
sys.exit(rc)
