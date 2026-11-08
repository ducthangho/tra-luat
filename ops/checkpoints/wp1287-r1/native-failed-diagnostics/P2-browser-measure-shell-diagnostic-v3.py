# Operator-only cross-platform candidate CLI measurement; never imported by product.
import os,sys,pathlib,json,hashlib,subprocess,datetime,threading,http.server,re,struct,uuid,time,traceback,base64
M=json.loads(pathlib.Path(sys.argv[1]).read_text());D=pathlib.Path(M['evidence_root']);assert not D.exists();D.mkdir(parents=True);INSTALL=pathlib.Path(M['install_root']);NODE=M['node'];NPM=M['npm_cli'];CACHE=pathlib.Path(M['browser_cache']);SESSION='tl-p2-'+uuid.uuid4().hex[:16];rows=[];opened=False
BODY=b'<!doctype html><html><head><title>tra-luat P2 candidate fixture</title></head><body><p id="evidence">controlled-source-wp1287-candidate</p></body></html>'
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(p,v):pathlib.Path(p).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
env=os.environ.copy()
for k in list(env):
 if k.startswith('TL_') or k in ['GH_TOKEN','GITHUB_TOKEN','GITHUB_PAT','CLAUDE_CODE_OAUTH_TOKEN','OPENAI_API_KEY','ANTHROPIC_API_KEY','PROXIMA_API_KEY','NPM_TOKEN','NODE_AUTH_TOKEN']:env.pop(k,None)
env.update(NO_UPDATE_NOTIFIER='1',PLAYWRIGHT_BROWSERS_PATH=str(CACHE),PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD='1',NPM_CONFIG_USERCONFIG=str(D/'npm-user-empty.conf'),NPM_CONFIG_GLOBALCONFIG=str(D/'npm-global-empty.conf'),NPM_CONFIG_CACHE=str(D/'npm-cache'))
for n in ['npm-user-empty.conf','npm-global-empty.conf']:(D/n).write_text('')
# Preserve per-user daemon/cache environment exactly as the published SKILL documents; own nonce only.
env['PATH']=str(pathlib.Path(NODE).parent)+os.pathsep+env.get('PATH','')
if os.name!='nt':
 tmp=pathlib.Path(M.get('temporary_root',str(D/'tmp')));tmp.mkdir(parents=True,exist_ok=False);env['TMPDIR']=env['TMP']=env['TEMP']=str(tmp)
def run(label,args,allowed=(0,),timeout=180):
 t=time.monotonic();print(json.dumps({'start':label,'at':utc()}),flush=True);r=subprocess.run(args,cwd=INSTALL,env=env,capture_output=True,timeout=timeout);o=D/(label+'.stdout');e=D/(label+'.stderr');o.write_bytes(r.stdout);e.write_bytes(r.stderr);row={'label':label,'command':args,'rc':r.returncode,'seconds':round(time.monotonic()-t,3),'stdout_sha256':sha(o),'stderr_sha256':sha(e),'finished_utc':utc()};rows.append(row);save(D/'command-receipts.json',rows);print(json.dumps({'finished':label,'rc':r.returncode}),flush=True);assert r.returncode in allowed,(label,r.returncode,r.stderr.decode(errors='replace')[-1500:]);return r.stdout
cli=INSTALL/'node_modules/@playwright/cli/playwright-cli.js'
def call(label,args):
 b=run(label,[NODE,str(cli),'-s='+SESSION,*args,'--json'],timeout=90);v=json.loads(b);assert not v.get('error'),(label,v);return v
def browser_processes(label):
 if os.name=='nt':
  root=str(CACHE).replace("'","''")
  code="$ErrorActionPreference='Stop';$ProgressPreference='SilentlyContinue';$env:PSModulePath=(Join-Path $PSHOME 'Modules')+';C:\\Program Files\\WindowsPowerShell\\Modules'; @(Get-CimInstance Win32_Process -Filter \"Name='chrome-headless-shell.exe'\" -ErrorAction Stop | Where-Object {$_.ExecutablePath -and $_.ExecutablePath.StartsWith('"+root+"',[StringComparison]::OrdinalIgnoreCase)} | Select-Object ProcessId,ParentProcessId,ExecutablePath,CommandLine)|ConvertTo-Json -Depth 4 -Compress"
  raw=run(label,[r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe','-NoProfile','-NonInteractive','-EncodedCommand',base64.b64encode(code.encode('utf-16-le')).decode()]);value=json.loads(raw.decode('utf-8-sig')) if raw.strip() else [];return value if isinstance(value,list) else [value]
 found=[]
 for d in pathlib.Path('/proc').iterdir():
  if not d.name.isdigit():continue
  try:
   raw=(d/'cmdline').read_bytes();exe=(d/'exe').resolve()
   if exe.is_relative_to(CACHE):found.append({'pid':int(d.name),'exe':str(exe),'cmdline':raw.decode(errors='replace').replace('\x00',' ')})
  except (OSError,ValueError):pass
 save(D/(label+'.json'),found);return found
class Handler(http.server.BaseHTTPRequestHandler):
 def do_GET(self):
  if self.path=='/redirect':self.send_response(302);self.send_header('Location','/source.html');self.end_headers();return
  self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(BODY)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(BODY)
 def log_message(self,*args):pass
server=None;rc=2
try:
 assert not (pathlib.Path.home()/'.playwright/cli.config.json').exists(),'Existing global CLI config, not overridden';assert not [k for k in env if k.startswith('PLAYWRIGHT_MCP_')],'Existing MCP environment config, no fallback';assert str(INSTALL.resolve())==str(INSTALL) and str(CACHE.resolve())==str(CACHE)
 assert run('node-version',[NODE,'--version']).decode().strip()=='v'+M['node_version'];assert run('npm-version',[NODE,NPM,'--version']).decode().strip()==M['npm_version']
 pkg=json.loads((INSTALL/'package.json').read_text());assert pkg['name']=='tra-luat-playwright-browser' and pkg['version']=='0.1.0' and pkg['private'] is True and not pkg.get('scripts');assert pkg['dependencies']=={'@playwright/cli':'0.1.23'};lock=json.loads((INSTALL/'package-lock.json').read_text());assert lock['lockfileVersion']==3 and lock['name']=='tra-luat-playwright-browser' and lock['version']=='0.1.0' and lock['packages']['']['version']=='0.1.0'
 before=sha(INSTALL/'package-lock.json');run('npm-ci',[NODE,NPM,'ci','--ignore-scripts','--no-audit','--no-fund'],timeout=300);assert sha(INSTALL/'package-lock.json')==before
 audit=json.loads(run('npm-signatures',[NODE,NPM,'audit','signatures','--json'],timeout=300));assert audit.get('invalid')==[] and audit.get('missing')==[]
 actual={n:json.loads((INSTALL/'node_modules'/n/'package.json').read_text())['version'] for n in ['@playwright/cli','playwright','playwright-core']};assert actual=={'@playwright/cli':'0.1.23','playwright':'1.65.0-alpha-2026-10-30','playwright-core':'1.65.0-alpha-2026-10-30'}
 browsers=json.loads((INSTALL/'node_modules/playwright-core/browsers.json').read_text());b=next(x for x in browsers['browsers'] if x['name']=='chromium-headless-shell');assert b['revision']=='1252' and b['browserVersion']=='157.0.8103.15'
 run('browser-install',[NODE,str(INSTALL/'node_modules/playwright/cli.js'),'install','--only-shell','chromium'],timeout=600);assert (CACHE/'chromium_headless_shell-1252').is_dir()
 binary=next(p for p in (CACHE/'chromium_headless_shell-1252').rglob('chrome-headless-shell.exe' if os.name=='nt' else 'chrome-headless-shell') if p.is_file())
 if os.name=='nt':
  q=str(binary).replace("'","''");code="$ErrorActionPreference='Stop';$ProgressPreference='SilentlyContinue';$f=Get-Item -LiteralPath '"+q+"';[pscustomobject]@{path=$f.FullName;FileVersion=$f.VersionInfo.FileVersion;ProductVersion=$f.VersionInfo.ProductVersion}|ConvertTo-Json -Compress";ver=json.loads(run('browser-binary-version',[r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe','-NoProfile','-NonInteractive','-EncodedCommand',base64.b64encode(code.encode('utf-16-le')).decode()]));actual_cli_version=run('browser-supported-version',[str(binary),'--version'],timeout=15).decode().strip();assert actual_cli_version=='Google Chrome for Testing 157.0.8103.15';ver['supported_cli_version']=actual_cli_version;assert ver['FileVersion'] in [None,'','157.0.8103.15']
 else:
  ver=run('browser-binary-version',[str(binary),'--version']).decode().strip();assert '157.0.8103.15' in ver
 save(D/'browser-binary-identity.json',{'path':str(binary),'sha256':sha(binary),'bytes':binary.stat().st_size,'actual_version':ver,'required_browser':b})
 cfg={'browser':{'browserName':'chromium','isolated':True,'launchOptions':{'executablePath':str(binary),'headless':True,'timeout':30000}},'outputDir':str(D/'artifacts'),'outputMode':'file','timeouts':{'action':30000}};save(D/'browser.json',cfg)
 assert browser_processes('browser-processes-before')==[]
 opened=True;op=call('open',['open','about:blank','--config',str(D/'browser.json')]);assert op['session']==SESSION and type(op['pid']) is int and op['pid']>0;procs=browser_processes('browser-processes-live');assert procs;save(D/'session.json',{'owned_browser_processes':procs,'nonce':SESSION,'open':op,'config':cfg,'browser_pins':b})
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_port}/redirect';final=url.replace('/redirect','/source.html');go=call('goto',['goto',url]);tabs=call('tabs',['tab-list']);assert isinstance(tabs['result'],str) and final in tabs['result'] and tabs['result'].count('(current)')==1
 req=call('requests',['requests','--static']);s=req['result'];assert url in s and final in s and '302' in s and '200' in s;lines=[l for l in s.splitlines() if final in l and 'GET' in l and '200' in l];assert len(lines)==1,lines;match=re.search(r'^(\d+)\. \[GET\]',lines[0]);assert match,lines;index=match[1]
 call('response-body',['response-body',index,'--filename',str(D/'source.html')]);assert (D/'source.html').read_bytes()==BODY
 call('screenshot',['screenshot','--filename',str(D/'screen.png'),'--full-page']);png=(D/'screen.png').read_bytes();assert png[:8]==b'\x89PNG\r\n\x1a\n';width,height=struct.unpack('>II',png[16:24]);assert width>0 and height>0
 call('pdf',['pdf','--filename',str(D/'page.pdf')]);assert (D/'page.pdf').read_bytes().startswith(b'%PDF-')
 if M.get('pdf_parser_wheel'):
  wheel=pathlib.Path(M['pdf_parser_wheel']);assert sha(wheel)==M['pdf_parser_sha256'];sys.path.insert(0,str(wheel))
 import pypdf
 assert pypdf.__version__=='6.10.0';text='\n'.join(p.extract_text() for p in pypdf.PdfReader(str(D/'page.pdf')).pages);assert 'controlled-source-wp1287-candidate' in text;(D/'pdf-text.txt').write_text(text,encoding='utf-8')
 close=call('close',['close']);assert close.get('session')==SESSION and close.get('status')=='closed';opened=False;deleted=call('delete-data',['delete-data']);assert deleted.get('session')==SESSION and type(deleted.get('deleted')) is bool;assert browser_processes('browser-processes-after')==[];save(D/'cleanup.json',{'close':close,'delete_data':deleted,'scope':'only exact owned nonce','session':SESSION})
 artifacts={n:{'bytes':(D/n).stat().st_size,'sha256':sha(D/n)} for n in ['source.html','screen.png','page.pdf','pdf-text.txt']};save(D/'receipt.json',{'diagnostic_only':True,'candidate_gate_eligible':False,'passed':True,'candidate':M['candidate'],'tree':M['tree'],'source_manifest':M,'installed_versions':actual,'node':M['node_version'],'npm':M['npm_version'],'browser':b,'session':SESSION,'requested_url':url,'final_url':final,'UTC':utc(),'source_exact':True,'source_sha256':hashlib.sha256(BODY).hexdigest(),'png_dimensions':[width,height],'pdf_fixture_text_verified':True,'artifacts':artifacts,'commands':rows,'no_legal_verification':True,'native_or_linux':os.name,'limits':'controlled fixture only; response body after HTTP decoding, no claim raw TLS bytes or legal authenticity'});rc=0
except BaseException as e:save(D/'failure.json',{'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),'commands':rows,'at':utc()});print(traceback.format_exc(),flush=True)
finally:
 if server:server.shutdown();server.server_close()
 if opened:
  try:call('failure-close',['close']);call('failure-delete-data',['delete-data'])
  except BaseException as e:save(D/'cleanup-failure.json',{'error':str(e),'session':SESSION})
 save(D/'terminal.json',{'rc':rc,'at':utc(),'candidate':M['candidate'],'session':SESSION})
sys.exit(rc)
