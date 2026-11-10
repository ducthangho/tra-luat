"""Operator-only one-open fullflow. No product parser, process-wide changes or retries."""
import os,sys,json,time,hashlib,subprocess,threading,http.server,re,struct,datetime,traceback
from pathlib import Path
# Embedded Python uses an isolated sys.path; add only this frozen operator directory.
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from contract import same_identity,readiness,cleanup,terminal,load_module_probes
from native_observer import K,identity,census,stamp,memory_sample
ROOT=Path(r'C:\tl-win\wp1287-r12-ps-literal-20261110');INSTALL=ROOT/'installation';E=ROOT/'evidence'
CACHE=Path(r'C:\tl-win\wp1287-H1-native-recovery2\browser-cache')
NODE=r'C:\Program Files\nodejs\node.exe';NPM=r'C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js'
CLI=INSTALL/'node_modules/@playwright/cli/playwright-cli.js';CHROME=CACHE/'chromium-1252/chrome-win64/chrome.exe'
LOCK=Path(r'C:\tl-win\KHOA.txt');NONCE='tl-pw-128709101110';H2='2a5803e17b7ca4910c7188bfcc2276190e2d0b4b'
EXPECTED={'@playwright/cli':'0.1.23','playwright':'1.65.0-alpha-2026-10-30','playwright-core':'1.65.0-alpha-2026-10-30'}
BODY=('<!doctype html><html><head><meta charset="utf-8"><title>WP1287 candidate</title></head><body><p>controlled-source-wp1287-candidate '+NONCE+'</p></body></html>').encode()
def save(p,v):Path(p).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def utc():return datetime.datetime.now(datetime.timezone.utc)
ENV=os.environ.copy()
for key in list(ENV):
    if key.startswith('TL_') or any(x in key.upper() for x in ['TOKEN','SECRET','PASSWORD','API_KEY','MASTER_KEY']):ENV.pop(key,None)
assert not any(k.startswith(('PLAYWRIGHT_MCP_','PWTEST_')) for k in ENV)
ENV.update(PLAYWRIGHT_BROWSERS_PATH=str(CACHE),PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD='1',NO_UPDATE_NOTIFIER='1',NPM_CONFIG_USERCONFIG=str(ROOT/'npm-user-empty.conf'),NPM_CONFIG_GLOBALCONFIG=str(ROOT/'npm-global-empty.conf'),NPM_CONFIG_CACHE=str(ROOT/'npm-cache'))
ENV['PATH']=str(Path(NODE).parent)+os.pathsep+ENV.get('PATH','')
MEMORY=[];CENSUS_TIMES=[]
ROWS=[];OWN={};HANDLES={};GAPS=[];PROBES=[];WORKER=None;QUEUE=[];MARKS=set();T0=None;ACTIVE=None;lockline=None;deadline=None

def acquire(label,minutes):
    global lockline,deadline
    assert os.name=='nt' and os.environ.get('COMPUTERNAME')=='DESKTOP-T9R33P2'
    assert not LOCK.read_text(encoding='utf-8-sig').strip(),'HOST_BUSY'
    start=utc();deadline=start+datetime.timedelta(minutes=minutes)
    lockline='\t'.join([NONCE,start.isoformat(),deadline.isoformat(),label,start.isoformat()]);LOCK.write_text(lockline,encoding='utf-8')
    assert LOCK.read_text(encoding='utf-8')==lockline

def release():
    assert LOCK.read_text(encoding='utf-8')==lockline,'LOCK_OWNER_CHANGED';LOCK.write_bytes(b'')

def observe():
    rows=census();now=time.monotonic_ns();live=[]
    CENSUS_TIMES.append(now)
    if not MEMORY or now-MEMORY[-1]['at']['mono_ns']>=500000000:MEMORY.append(memory_sample(WORKER[0].pid if WORKER else None))
    # Scan repeatedly so a child may precede its parent in the snapshot.
    for _ in range(4):
        changed=False
        for row in rows:
            if row['pid'] in OWN:continue
            parent=OWN.get(row['parent'])
            if not parent:continue
            parent_now=identity(row['parent'],HANDLES[row['parent']]);child=identity(row['pid'])
            if not child or not parent_now:continue
            if child['birth']<parent['birth'] or parent_now['exit_time'] and child['birth']>parent_now['exit_time']:continue
            h=K.OpenProcess(0x1000,False,row['pid'])
            if h and same_identity(child,identity(row['pid'],h)):
                OWN[row['pid']]={**child,'parent':row['parent'],'observed_mono_ns':now};HANDLES[row['pid']]=h;changed=True
            elif h:K.CloseHandle(h)
        if not changed:break
    for pid,old in OWN.items():
        current=identity(pid,HANDLES[pid])
        if current and current['alive']:
            if same_identity(old,current):live.append(current)
            else:GAPS.append({'at':stamp(),'reason':'identity_changed','pid':pid})
    # Cache is an admission/unknown detector only, never an ownership or kill rule.
    for row in rows:
        if row['exe'].lower()=='chrome.exe' and row['pid'] not in OWN:
            x=identity(row['pid'])
            if x and x['image']==str(CHROME).lower():GAPS.append({'at':stamp(),'reason':'unattributed_target_browser','pid':row['pid']})
    return live

def observer_tick(post=False):
    global WORKER
    now=time.monotonic_ns()
    if T0 is None:return
    live=observe()
    for mark in [5,15,25]:
        if now-T0>=mark*10**9 and mark not in MARKS:
            MARKS.add(mark);browsers=[x for x in live if x['image']==str(CHROME).lower()]
            if not browsers:PROBES.append({'scheduled_offset_ns':mark*10**9,'state':'not_run_process_exited_or_not_observed','at':stamp()})
            for x in browsers:QUEUE.append((mark*10**9,x,False))
    if post:
        browsers=[x for x in live if x['image']==str(CHROME).lower()]
        if not browsers:PROBES.append({'scheduled_offset_ns':now-T0,'post_open':True,'state':'not_run_process_exited_or_not_observed','at':stamp()})
        for x in browsers:QUEUE.append((now-T0,x,True))
    if WORKER:
        p,start,record=WORKER
        if p.poll() is not None:record.update(worker_rc=p.returncode,end=stamp());PROBES.append(record);WORKER=None
        elif time.monotonic()-start>=3:
            p.terminate();p.wait(timeout=3);record.update(state='deadline_exhausted',end=stamp());PROBES.append(record);WORKER=None
    if WORKER is None and QUEUE:
        scheduled,x,ispost=QUEUE.pop(0);index=len(PROBES);ip=E/f'probe-{index}-identity.json';op=E/f'probe-{index}.json';save(ip,x)
        rec={'post_open':ispost,'scheduled_offset_ns':scheduled,'actual_start':stamp(),'lag_ns':time.monotonic_ns()-T0-scheduled,'pid':x['pid'],'output':op.name}
        p=subprocess.Popen([sys.executable,str(ROOT/'native_observer.py'),str(ip),str(op)],env=ENV,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,cwd=ROOT)
        WORKER=(p,time.monotonic(),rec)
    save(E/'probe-schedule.json',PROBES)

def command(label,args,timeout=90,track=True):
    global ACTIVE
    assert utc()<deadline,'RUN_DEADLINE'
    out=E/(label+'.stdout');err=E/(label+'.stderr');assert not out.exists() and not err.exists()
    row={'label':label,'argv':args,'start':stamp(),'timeout_seconds':timeout};ROWS.append(row);save(E/'commands.json',ROWS)
    with out.open('xb') as so,err.open('xb') as se:
        p=subprocess.Popen(args,cwd=ROOT,env=ENV,stdout=so,stderr=se);ACTIVE=p
        x=identity(p.pid)
        if track:
            assert x,'CLI_IDENTITY_UNKNOWN';h=K.OpenProcess(0x1000,False,p.pid);assert h and same_identity(x,identity(p.pid,h));OWN[p.pid]=x;HANDLES[p.pid]=h
        started=time.monotonic();last=None
        while p.poll() is None:
            now=time.monotonic_ns()
            if track:
                if last and now-last>1500000000:GAPS.append({'at':stamp(),'reason':'census_gap','ns':now-last})
                observe();observer_tick();last=now
            if time.monotonic()-started>timeout or utc()>=deadline:
                # Only this Popen process is stopped; no PID lookup or browser/global kill.
                p.terminate();p.wait(timeout=5);row.update(timed_out=True);break
            time.sleep(.1)
        row.update(rc=p.returncode,end=stamp(),stdout_sha256=sha(out),stderr_sha256=sha(err));save(E/'commands.json',ROWS);ACTIVE=None
    print(json.dumps({'command':label,'rc':p.returncode,'timed_out':row.get('timed_out',False)}),flush=True)
    return {'rc':p.returncode,'stdout':out.read_bytes(),'stderr':err.read_bytes(),'timed_out':row.get('timed_out',False)}

def cli(label,args,timeout=90,allowed=(0,)):
    r=command(label,[NODE,str(CLI),'-s='+NONCE,*args,'--json'],timeout)
    assert r['rc'] in allowed and not r['timed_out'],(label,'CLI_FAILED',r['rc'])
    v=json.loads(r['stdout']);assert not v.get('isError') and not v.get('error'),(label,'CLI_ERROR');return v

def runtime():
    assert not (Path.home()/'.playwright/cli.config.json').exists()
    assert subprocess.check_output([NODE,'--version'],env=ENV).strip()==b'v26.13.0'
    assert subprocess.check_output([NODE,NPM,'--version'],env=ENV).strip()==b'11.20.0'
    assert {n:json.loads((INSTALL/'node_modules'/n/'package.json').read_text())['version'] for n in EXPECTED}==EXPECTED
    b=next(x for x in json.loads((INSTALL/'node_modules/playwright-core/browsers.json').read_text())['browsers'] if x['name']=='chromium');assert b['revision']=='1252' and b['browserVersion']=='157.0.8103.15'
    assert sha(CHROME)=='7ca0cf1b2cba9b9ec812a8e3df2cb92a5ddbea8c7013b8d71d589a43589fad21'
    source=json.loads((ROOT/'source-manifest.json').read_text())
    for name,digest in source['files'].items():assert sha(INSTALL/name)==digest
    return b

class Fixture(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=='/redirect':self.send_response(302);self.send_header('Location','/source.html');self.end_headers()
        elif self.path=='/source.html':
            self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(BODY)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(BODY)
        else:self.send_response(404);self.end_headers()
    def log_message(self,*args):pass

def stage():
    assert not (ROOT/'stage-terminal.json').exists();E.mkdir(exist_ok=False)
    acquire('WP1287 r12 preparation no browser',15);ok=False
    try:
        for n in ['npm-user-empty.conf','npm-global-empty.conf']:(ROOT/n).write_text('')
        before=sha(INSTALL/'package-lock.json')
        for label,args in [('npm-ci',['ci','--ignore-scripts','--no-audit','--no-fund']),('npm-signatures',['audit','signatures','--json'])]:
            # npm must run in own installation; temporarily use explicit --prefix.
            r=command(label,[NODE,NPM,'--prefix',str(INSTALL),*args],300,False);assert r['rc']==0
            if label=='npm-signatures':v=json.loads(r['stdout']);assert v.get('invalid')==[] and v.get('missing')==[]
        assert sha(INSTALL/'package-lock.json')==before;b=runtime()
        r=command('browser-install',[NODE,str(INSTALL/'node_modules/playwright/cli.js'),'install','--no-shell','chromium'],300,False);assert r['rc']==0
        ok=True;save(ROOT/'stage-terminal.json',{'passed':True,'at':stamp(),'candidate':H2,'runtime':EXPECTED,'browser':b,'browser_sha256':sha(CHROME),'no_browser_open':True})
    finally:
        if not ok:save(ROOT/'stage-failure.json',{'traceback':traceback.format_exc(),'at':stamp()})
        release()
    return 0 if ok else 2

def flow():
    global T0,ROWS,WORKER
    assert json.loads((ROOT/'stage-terminal.json').read_text())['passed'];assert not (E/'terminal.json').exists() and not (E/'reserved.json').exists()
    runtime();assert not [x for x in census() if x['exe'].lower()=='chrome.exe' and (identity(x['pid']) or {}).get('image')==str(CHROME).lower()]
    grant=json.loads((ROOT/'execution-grant.json').read_text());assert grant['one_open_limit']==1 and grant['mode']=='candidate_native_fullflow'
    for name,digest in grant['helper_sha256'].items():assert sha(ROOT/name)==digest
    assert utc()<datetime.datetime.fromisoformat(grant['expires_at'])
    acquire('WP1287 r12 one-open candidate fullflow',8);ROWS=[];server=None;attempted=False;rc=2;clean='not_run';full='not_run';ready='not_run';startup='not_run';openrc=None;error=None
    try:
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Fixture);threading.Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_port}/redirect';final=url.replace('/redirect','/source.html')
        cfg={'browser':{'browserName':'chromium','isolated':True,'launchOptions':{'channel':'chromium','headless':True,'timeout':30000}},'timeouts':{'action':10000},'outputDir':str(E/'artifacts'),'outputMode':'file'};save(E/'browser.json',cfg)
        save(E/'fixture.json',{'nonce':NONCE,'requested':url,'expected_final':final,'expected_statuses':[302,200],'body_sha256':hashlib.sha256(BODY).hexdigest(),'body_bytes':len(BODY),'config_sha256':sha(E/'browser.json')})
        save(E/'reserved.json',{'at':stamp(),'used':1,'reserved':0,'limit':1,'mode':grant['mode'],'candidate':H2,'grant_sha256':sha(ROOT/'execution-grant.json')});attempted=True;T0=time.monotonic_ns()
        r=command('open',[NODE,str(CLI),'-s='+NONCE,'open','about:blank','--config',str(E/'browser.json'),'--json'],100);openrc=r['rc'];observer_tick(post=True)
        assert openrc==0 and not r['timed_out'],'OPEN_FAILED';v=json.loads(r['stdout']);assert v.get('session')==NONCE and type(v.get('pid')) is int and not v.get('isError');startup='acknowledged'
        tabs=cli('initial-tabs',['tab-list']);assert isinstance(tabs.get('result'),str) and tabs['result'].count('(current)')==1,'QUERY_UNKNOWN'
        cli('goto',['goto',url]);tabs=cli('tabs',['tab-list']);text=tabs['result'];assert text.count('(current)')==1 and len([l for l in text.splitlines() if '(current)' in l and final in l])==1,'FINAL_URL_UNKNOWN'
        requests=cli('requests',['requests','--static'])['result'];lines=requests.splitlines();red=[l for l in lines if url in l and 'GET' in l and '302' in l];found=[l for l in lines if final in l and 'GET' in l and '200' in l];assert len(red)==len(found)==1,'REDIRECT_UNKNOWN'
        m=re.match(r'^(\d+)\. \[GET\]',found[0]);assert m,'REQUEST_INDEX_UNKNOWN';cli('response-body',['response-body',m[1],'--filename',str(E/'source.html')])
        ready=readiness(startup,final,final,[302,200],(E/'source.html').read_bytes(),BODY);assert ready=='fixture_verified','BODY_MISMATCH'
        cli('screenshot',['screenshot','--filename',str(E/'screen.png'),'--full-page']);png=(E/'screen.png').read_bytes();assert png[:8]==b'\x89PNG\r\n\x1a\n';dimensions=struct.unpack('>II',png[16:24]);assert min(dimensions)>0
        cli('pdf',['pdf','--filename',str(E/'page.pdf')]);wheel=Path(r'C:\tl-win\wp1287-H1-native-recovery2\inputs\pypdf-6.10.0-py3-none-any.whl');assert sha(wheel)=='90005e959e1596c6e6c84c8b0ad383285b3e17011751cedd17f2ce8fcdfc86de';sys.path.insert(0,str(wheel));import pypdf
        assert pypdf.__version__=='6.10.0';pdf='\n'.join(p.extract_text() or '' for p in pypdf.PdfReader(str(E/'page.pdf')).pages);assert NONCE in pdf and 'controlled-source-wp1287-candidate' in pdf
        save(E/'captures.json',{'PNG_dimensions':dimensions,'PDF_nonce_verified':True,'artifacts':{n:{'sha256':sha(E/n),'bytes':(E/n).stat().st_size} for n in ['source.html','screen.png','page.pdf']}});full='passed'
    except BaseException as e:
        error=type(e).__name__+': '+str(e);save(E/'failure.json',{'at':stamp(),'error':error,'traceback':traceback.format_exc()})
        if startup=='not_run' and attempted:startup='failed'
        if ready=='not_run' and startup=='acknowledged':ready='unknown'
        if full=='not_run':full='failed'
    finally:
        cleanrows=[]
        if attempted:
            for label,args in [('close',['close']),('delete-data',['delete-data']),('verify-closed',['tab-list'])]:
                try:cleanrows.append(command(label,[NODE,str(CLI),'-s='+NONCE,*args,'--json'],20))
                except BaseException as e:cleanrows.append({'rc':None,'stdout':b'','stderr':b'','error':str(e)})
            until=time.monotonic()+5
            while time.monotonic()<until:
                live=observe();observer_tick()
                if not live:break
                time.sleep(.1)
            if WORKER:
                p,_,record=WORKER
                if p.poll() is None:p.terminate();p.wait(timeout=3)
                record.update(worker_rc=p.returncode,state='stopped_for_cleanup',end=stamp());PROBES.append(record);WORKER=None
            for scheduled,x,ispost in QUEUE:PROBES.append({'post_open':ispost,'scheduled_offset_ns':scheduled,'pid':x['pid'],'state':'not_run_cleanup_priority'})
            save(E/'probe-schedule.json',PROBES)
            live=observe();clean=cleanup(NONCE,cleanrows,live,bool(GAPS));save(E/'ownership.json',{'identities':list(OWN.values()),'remaining':live,'gaps':GAPS,'at':stamp()})
        if server:server.shutdown();server.server_close()
        rc=0 if full=='passed' and clean=='verified' else 2
        save(E/'observer-overhead.json',{'samples':MEMORY,'census_mono_ns':CENSUS_TIMES,'worker_limit_seconds':3,'workers_serial':True,'limits':'Observer timings and memory observations only, no causal A/B claim'})
        states=[p['state'] for p in load_module_probes(E)]
        quality='complete_walk' if states and all(x=='complete_walk' for x in states) and not any(x.get('state')=='deadline_exhausted' for x in PROBES) else 'partial' if states else 'unavailable'
        result={**terminal(full,clean,rc),'at':stamp(),'observer_quality':quality,'module_walk_states':states,'startup':startup,'open_cli_rc':openrc,'readiness':ready,'fullflow':full,'cleanup':clean,'error':error,'allowance_used':int(attempted),'limit':1,'U10':'OPEN_pending_documented_shell_proofs_and_formal_review','OP-F01':'formal_OPEN','candidate':H2,'no_automatic_retry':True,'action_timeout_ms':10000,'launch_timeout_ms':30000,'cleanup_timeout_seconds':20}
        if clean=='verified':release()
        result['lock_released']=not LOCK.read_bytes();result['paused_handoff']=clean!='verified';result['lock_deadline']=deadline.isoformat();save(E/'terminal.json',result)
        with Path(r'C:\tl-win\do-luong.csv').open('a',encoding='utf-8',newline='') as f:f.write(f'{utc().isoformat()},{NONCE},wp1287,{H2},r12-documented-ps-fullflow,0,0,{rc},0,operator,{clean},no,may=DESKTOP-T9R33P2;startup={startup};readiness={ready};fullflow={full}\n')
        for h in HANDLES.values():K.CloseHandle(h)
        save(E/'manifest.json',{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in E.iterdir() if p.is_file() and p.name!='manifest.json'})
        print(json.dumps(result),flush=True)
    return rc
if __name__=='__main__':sys.exit(stage() if sys.argv[1]=='stage' else flow())
