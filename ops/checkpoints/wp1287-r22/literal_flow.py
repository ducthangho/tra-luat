"""Operator only: bind documented inputs and execute exact source shell fragments."""
import pathlib,sys,os,json,re,hashlib,subprocess,threading,http.server,struct,datetime,base64,shutil,time
ROOT=pathlib.Path(sys.argv[1]);kind=sys.argv[2];WIN=os.name=='nt';SRC=ROOT/'source';skill=(SRC/'SKILL.md').read_text(encoding='utf-8-sig');language='powershell' if WIN else 'bash';b=re.findall('```'+language+r'\n(.*?)\n```',skill,re.S)
assert len(b)==5;E=ROOT/('flow-'+kind);E.mkdir(exist_ok=False);ADDON=ROOT/('addon-'+kind);NODE=r'C:\Program Files\nodejs\node.exe' if WIN else '/opt/codex/runtimes/codex-primary-runtime/dependencies/node/bin/node';NPM=r'C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js' if WIN else '/opt/codex/runtimes/codex-primary-runtime/dependencies/node/lib/node_modules/npm/bin/npm-cli.js';CLI=ADDON/'install/0.1.0/node_modules/@playwright/cli/playwright-cli.js';CACHE=ADDON/'browsers/0.1.0';ROWS=[];STATE=E/'state.json';M=None
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(p,v):pathlib.Path(p).write_bytes((json.dumps(v,indent=2)+'\n').encode())
env={k:v for k,v in os.environ.items() if not k.startswith(('TL_','GIT_','PLAYWRIGHT_','PWTEST_')) and not any(x in k.upper() for x in ['TOKEN','SECRET','PASSWORD','API_KEY','MASTER_KEY'])};env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1',NO_UPDATE_NOTIFIER='1');globalconf=E/'npm-global-empty.conf';globalconf.write_bytes(b'');env['NPM_CONFIG_GLOBALCONFIG']=str(globalconf)
SHELL=(r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' if kind=='ps51' else r'C:\Program Files\PowerShell\7\pwsh.exe') if WIN else 'bash'
if WIN:
 sys.path.insert(0,str(ROOT));import native_flow as M
 M.ROOT=E;M.E=E;M.INSTALL=ADDON/'install/0.1.0';M.CACHE=CACHE;M.CHROME=CACHE/'chromium-1252/chrome-win64/chrome.exe';M.NODE=NODE;M.CLI=CLI;M.NONCE='wp1287-r22-'+kind;M.ENV=env;M.acquire('H4 literal acceptance '+kind,90)
 env['PSModulePath']=(r'C:\Windows\System32\WindowsPowerShell\v1.0\Modules' if kind=='ps51' else r'C:\Program Files\PowerShell\7\Modules')+r';C:\Program Files\WindowsPowerShell\Modules'
 # Seed only this owned cache from the immutable prior pinned CFT revision.
 prior=pathlib.Path(r'C:\tl-win\wp1287-H1-native-recovery2\browser-cache');CACHE.mkdir(parents=True)
 for p in prior.iterdir():
  if p.is_dir() and p.name.startswith(('chromium-1252','ffmpeg-','winldd-')):shutil.copytree(p,CACHE/p.name)
 save(E/'cache-provenance.json',{'prior_verified_cache':str(prior),'seeded_chrome_sha256':sha(M.CHROME),'official_installer_still_required':True})
def execute(label,code,timeout=180):
 path=E/(label+('.ps1' if WIN else '.bash'));path.write_bytes((('\ufeff' if WIN else '')+code).encode());out=E/(label+'.stdout');err=E/(label+'.stderr')
 if WIN:
  stub="$ErrorActionPreference='Stop'; & ([scriptblock]::Create([IO.File]::ReadAllText('"+str(path)+"',[Text.Encoding]::UTF8)))";args=[SHELL,'-NoProfile','-NonInteractive','-EncodedCommand',base64.b64encode(stub.encode('utf-16le')).decode()];row=M.command(label,args,timeout,True);rc=row['rc'];raw=row['stdout']
 else:
  with out.open('xb') as so,err.open('xb') as se:cp=subprocess.run([SHELL,'--noprofile','--norc',str(path)],env=env,stdout=so,stderr=se,timeout=timeout)
  rc=cp.returncode;raw=out.read_bytes()
 ROWS.append({'label':label,'rc':rc,'bound_script_sha256':sha(path),'stdout_sha256':sha(out),'stderr_sha256':sha(err)});save(E/'literal-steps.json',ROWS);assert rc==0,(label,rc);return raw
body=('<!doctype html><html><head><meta charset="utf-8"><title>WP1287 H4 fixture</title></head><body><p>controlled-source-wp1287-H4-'+kind+'</p></body></html>').encode()
class Fixture(http.server.BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_GET(self):
  if self.path=='/redirect':self.send_response(302);self.send_header('Location','/source.html');self.end_headers()
  elif self.path=='/source.html':self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
  else:self.send_error(404)
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Fixture);threading.Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_port}/redirect';final=url.replace('/redirect','/source.html');ok=False;run=None;cleanup_attempted=False
try:
 setup=b[0]
 if WIN:
  for old,new in [('<TargetId>','DESKTOP-T9R33P2'),('<D:\\abs\\ngoai-git\\tl-playwright>',str(ADDON)),('<D:\\abs\\node-v26.13.0-win-x64\\node.exe>',NODE),('<D:\\abs\\node-v26.13.0-win-x64\\node_modules\\npm\\bin\\npm-cli.js>',NPM),('<D:\\abs\\checkout-tra-luat>\\.agents\\skills\\playwright-browser',str(SRC))]:setup=setup.replace(old,new)
 else:
  for old,new in [('<TargetId>','codex-cloud-linux'),('</abs/ngoai-git/tl-playwright>',str(ADDON)),('</abs/node-v24.19.0-linux-x64/bin/node>',NODE),('</abs/node-v24.19.0-linux-x64/lib/node_modules/npm/bin/npm-cli.js>',NPM),('</abs/checkout-tra-luat>/.agents/skills/playwright-browser',str(SRC))]:setup=setup.replace(old,new)
 # Persist only already-bound documented inputs across source fragment invocations.
 if WIN:prefix=setup[:setup.index('& { $ErrorActionPreference')];defs=setup[setup.index('function Need'):setup.index('& { $ErrorActionPreference')]
 else:prefix=setup[:setup.index('( set -')];defs=''
 execute('01-setup',setup,600)
 cap=b[2];cut=cap.index('# Chạy khối');pre=cap[:cut].replace('<https://nguon-cong-khai/duong-dan>',url);rest=cap[cut:]
 if WIN:
  state="[IO.File]::WriteAllText('"+str(STATE)+"',(@{run=$env:TL_PW_RUN;session=$env:TL_PW_SESSION}|ConvertTo-Json))\n";pin=b[1]+" *>&1 | Tee-Object -FilePath \"$env:TL_PW_RUN\\00-pins.log\"\n"
 else:state="printf '%s\\n%s\\n' \"$TL_PW_RUN\" \"$TL_PW_SESSION\" > '"+str(STATE)+"'\n";pin=b[1]+" 2>&1 | tee \"$TL_PW_RUN/00-pins.log\"\n"
 execute('02-capture-init',prefix+pre+state+pin+rest,180)
 state_data=json.loads(STATE.read_text(encoding='utf-8-sig')) if WIN else dict(zip(['run','session'],STATE.read_text().splitlines()));run=pathlib.Path(state_data['run']);session=state_data['session'];requests=json.loads((run/'04-requests.json').read_text(encoding='utf-8-sig'))['result'];tabs=json.loads((run/'03-tab-list.json').read_text(encoding='utf-8-sig'))['result'];assert tabs.count('(current)')==1 and final in tabs
 matches=[line for line in requests.splitlines() if final in line and '[GET]' in line and '[200]' in line];assert len(matches)==1 and any(url in line and '[302]' in line for line in requests.splitlines());m=re.match(r'^(\d+)\. \[GET\]',matches[0]);assert m
 helper=cap[cap.index('function Invoke-PwGhi' if WIN else 'chay_ghi()'):cut]
 if WIN:restore=prefix+"$env:TL_PW_RUN='"+str(run)+"'; $env:TL_PW_SESSION='"+session+"'\n"+helper+'\n'
 else:restore=prefix+"export TL_PW_RUN='"+str(run)+"' TL_PW_SESSION='"+session+"'\n"+helper+'\n'
 execute('03-capture-files',restore+b[3].replace('<N đọc từ 04-requests.json>',m[1]),120)
 assert (run/'source.body').read_bytes()==body;png=(run/'page.png').read_bytes();assert png[:8]==b'\x89PNG\r\n\x1a\n';dimensions=struct.unpack('>II',png[16:24]);assert min(dimensions)>0
 if WIN:
  wheel=pathlib.Path(r'C:\tl-win\wp1287-H1-native-recovery2\inputs\pypdf-6.10.0-py3-none-any.whl');assert sha(wheel)=='90005e959e1596c6e6c84c8b0ad383285b3e17011751cedd17f2ce8fcdfc86de';sys.path.insert(0,str(wheel))
 import pypdf
 pdf='\n'.join(p.extract_text() or '' for p in pypdf.PdfReader(str(run/'page.pdf')).pages);assert 'controlled-source-wp1287-H4-'+kind in pdf
 cleanup_attempted=True;execute('04-cleanup',restore+b[4],90)
 observed=[]
 if WIN:
  until=time.monotonic()+5
  while True:
   observed=M.observe()
   if not observed or time.monotonic()>=until:break
   time.sleep(.1)
  assert not observed and not M.GAPS,('OWNERSHIP_OR_LIVE_CHILD',observed,M.GAPS)
 else:
  daemon=subprocess.run([NODE,str(CLI),'--session='+session,'tab-list','--json'],env=dict(env,PLAYWRIGHT_BROWSERS_PATH=str(CACHE)),capture_output=True,timeout=20);assert daemon.returncode==1
 save(E/'captures.json',{'requested_url':url,'final_url':final,'response_index':int(m[1]),'body_exact':True,'PNG_dimensions':dimensions,'PDF_fixture_text':True,'files':{n:{'bytes':(run/n).stat().st_size,'sha256':sha(run/n)} for n in ['source.body','page.png','page.pdf']}});ok=True
finally:
 if STATE.exists() and not cleanup_attempted:
  try:
   state_data=json.loads(STATE.read_text(encoding='utf-8-sig')) if WIN else dict(zip(['run','session'],STATE.read_text().splitlines()));run=pathlib.Path(state_data['run']);session=state_data['session'];helper=b[2][b[2].index('function Invoke-PwGhi' if WIN else 'chay_ghi()'):b[2].index('# Chạy khối')];restore=prefix+("$env:TL_PW_RUN='"+str(run)+"';$env:TL_PW_SESSION='"+session+"'\n" if WIN else "export TL_PW_RUN='"+str(run)+"' TL_PW_SESSION='"+session+"'\n")+helper+'\n';execute('failure-cleanup',restore+b[4],90)
  except BaseException as ex:save(E/'failure-cleanup.json',{'error':repr(ex)})
 server.shutdown();server.server_close()
 live=M.observe() if WIN else []
 if WIN and not live:M.release()
 if WIN:
  with pathlib.Path(r'C:\tl-win\do-luong.csv').open('a',encoding='utf-8',newline='') as ledger:ledger.write(f"{datetime.datetime.now(datetime.timezone.utc).isoformat()},wp1287-r22-{kind},wp1287,0bf2a8a7a094d9df0a84eec807c5c5e5d89d87c2,literal-fullflow,{sum(x['rc']==0 for x in ROWS)},{len(ROWS)},{int(not ok)},0,operator,{not ok},no,may=DESKTOP-T9R33P2;no_model\n")
  for handle in M.HANDLES.values():M.K.CloseHandle(handle)
 save(E/'terminal.json',{'passed':ok,'candidate':'0bf2a8a7a094d9df0a84eec807c5c5e5d89d87c2','source_sha256':hashlib.sha256(skill.encode()).hexdigest(),'shell':kind,'steps':ROWS,'owned_live':len(live),'lock_released':not pathlib.Path(r'C:\tl-win\KHOA.txt').read_bytes() if WIN else None,'source_fragments_sha256':[hashlib.sha256(x.encode()).hexdigest() for x in b]});print(json.dumps({'passed':ok,'shell':kind,'steps':[(x['label'],x['rc']) for x in ROWS],'owned_live':len(live)}),flush=True)
