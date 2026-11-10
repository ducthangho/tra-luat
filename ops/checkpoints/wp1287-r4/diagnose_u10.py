"""One bounded operator measurement; never product code or a compatibility gate."""
import base64
import ctypes as C
from ctypes import wintypes as W
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback

ROOT = Path(r'C:\tl-win\wp1287-r4-u10-20261110')
OLD = Path(r'C:\tl-win\wp1287-H1-native-recovery2')
NODE = r'C:\Program Files\nodejs\node.exe'
INSTALL = OLD / 'installation'
CACHE = OLD / 'browser-cache'
CLI = INSTALL / 'node_modules/@playwright/cli/playwright-cli.js'
CHROME = CACHE / 'chromium-1252/chrome-win64/chrome.exe'
NONCE = 'tl-pw-r4-u10-20261110'
H2 = '2a5803e17b7ca4910c7188bfcc2276190e2d0b4b'
LOCK = Path(r'C:\tl-win\KHOA.txt')
K = C.WinDLL('kernel32', use_last_error=True)
K.CreateToolhelp32Snapshot.restype = W.HANDLE
K.OpenProcess.restype = W.HANDLE
K.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
K.CloseHandle.argtypes = [W.HANDLE]
K.QueryFullProcessImageNameW.argtypes = [W.HANDLE, W.DWORD, W.LPWSTR, C.POINTER(W.DWORD)]
K.GetExitCodeProcess.argtypes = [W.HANDLE, C.POINTER(W.DWORD)]

class PE(C.Structure):
    _fields_ = [('size',W.DWORD),('usage',W.DWORD),('pid',W.DWORD),('heap',C.c_size_t),('module',W.DWORD),('threads',W.DWORD),('parent',W.DWORD),('priority',W.LONG),('flags',W.DWORD),('exe',W.WCHAR*260)]

K.Process32FirstW.argtypes=[W.HANDLE,C.POINTER(PE)]
K.Process32NextW.argtypes=[W.HANDLE,C.POINTER(PE)]

class MEM(C.Structure):
    _fields_=[('length',W.DWORD),('load',W.DWORD)]+[(n,C.c_ulonglong) for n in ['total','free','commit_limit','commit_free','virtual_total','virtual_free','extended_free']]

def utc(): return dt.datetime.now(dt.timezone.utc).isoformat()
def save(n,v): (ROOT/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def memory():
    m=MEM();m.length=C.sizeof(m);assert K.GlobalMemoryStatusEx(C.byref(m))
    return {n:getattr(m,n) for n,_ in MEM._fields_}
def processes():
    s=K.CreateToolhelp32Snapshot(2,0);p=PE();p.size=C.sizeof(p);out=[]
    try:
        ok=K.Process32FirstW(s,C.byref(p))
        while ok:
            out.append((p.pid,p.parent,p.exe));ok=K.Process32NextW(s,C.byref(p))
    finally:K.CloseHandle(s)
    return out
def image(pid):
    h=K.OpenProcess(0x1000,False,pid)
    if not h:return None
    try:
        b=C.create_unicode_buffer(32768);n=W.DWORD(len(b))
        return b.value if K.QueryFullProcessImageNameW(h,0,b,C.byref(n)) else None
    finally:K.CloseHandle(h)
def ps(code):
    code="$ErrorActionPreference='Stop';$env:PSModulePath=(Join-Path $PSHOME 'Modules')+';C:\\Program Files\\WindowsPowerShell\\Modules';"+code
    return subprocess.run([r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe','-NoProfile','-NonInteractive','-EncodedCommand',base64.b64encode(code.encode('utf-16le')).decode()],capture_output=True,timeout=20)

assert os.name=='nt' and os.environ.get('COMPUTERNAME')=='DESKTOP-T9R33P2'
assert ROOT.exists() and not (ROOT/'terminal.json').exists() and not (ROOT/'reserved.json').exists()
env=os.environ.copy()
for k in list(env):
    if k.startswith('TL_') or any(t in k.upper() for t in ['TOKEN','SECRET','PASSWORD','API_KEY','MASTER_KEY']):env.pop(k,None)
assert not any(k.startswith(('PLAYWRIGHT_MCP_','PWTEST_')) for k in env)
assert not (Path.home()/'.playwright/cli.config.json').exists()
env.update(PLAYWRIGHT_BROWSERS_PATH=str(CACHE),PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD='1',NO_UPDATE_NOTIFIER='1',DEBUG='pw:browser')
env['PATH']=str(Path(NODE).parent)+os.pathsep+env.get('PATH','')
assert subprocess.check_output([NODE,'--version'],env=env).strip()==b'v26.13.0'
expected={'@playwright/cli':'0.1.23','playwright':'1.65.0-alpha-2026-10-30','playwright-core':'1.65.0-alpha-2026-10-30'}
assert {n:json.loads((INSTALL/'node_modules'/n/'package.json').read_text())['version'] for n in expected}==expected
assert digest(CHROME)=='7ca0cf1b2cba9b9ec812a8e3df2cb92a5ddbea8c7013b8d71d589a43589fad21'
assert not [pid for pid,_,exe in processes() if exe.lower()=='chrome.exe' and (image(pid) or '').lower().startswith(str(CACHE).lower())]
assert not LOCK.read_text(encoding='utf-8-sig').strip(),'HOST_BUSY'
# Only publish load categories, never unrelated process command lines.
load=ps("@(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Select-Object ProcessId,CreationDate,CommandLine)|ConvertTo-Json -Compress")
assert load.returncode==0
loaded=json.loads(load.stdout.decode('utf-8-sig')) if load.stdout.strip() else []
if isinstance(loaded,dict):loaded=[loaded]
assert all(x['ProcessId']==os.getpid() or any(t in (x.get('CommandLine') or '').lower() for t in ['mcp','browser-use','proxima_agent']) for x in loaded),'OTHER_PYTHON_WORKLOAD'
start=dt.datetime.now(dt.timezone.utc);deadline=start+dt.timedelta(minutes=5)
lockline='\t'.join([NONCE,start.isoformat(),deadline.isoformat(),'WP1287 r4 one U10 diagnostic',start.isoformat()])
LOCK.write_text(lockline,encoding='utf-8')
assert LOCK.read_text(encoding='utf-8')==lockline
save('reserved.json',{'at':utc(),'used':0,'reserved':1,'limit':1,'candidate':H2,'script_sha256':digest(__file__),'diagnostic_only':True,'other_python_count':len(loaded)-1})
save('browser.json',{'browser':{'browserName':'chromium','isolated':True,'launchOptions':{'channel':'chromium','headless':True,'timeout':30000}},'outputDir':str(ROOT/'artifacts'),'outputMode':'file'})
cmd=[NODE,str(CLI),'-s='+NONCE,'open','about:blank','--config',str(ROOT/'browser.json'),'--json']
save('command.json',{'argv':cmd,'config_sha256':digest(ROOT/'browser.json'),'candidate':H2,'runtime':expected,'browser_sha256':digest(CHROME),'browser_cache':str(CACHE),'environment_changes':{'DEBUG':'pw:browser','PLAYWRIGHT_BROWSERS_PATH':str(CACHE)},'acquired_utc':utc()})
handles={};seen={};samples=[];rc=2;cleanup=[];launch=None
try:
    with (ROOT/'open.stdout').open('wb') as so,(ROOT/'open.stderr').open('wb') as se:
        launch=subprocess.Popen(cmd,stdout=so,stderr=se,cwd=ROOT,env=env)
        owned={launch.pid};until=time.monotonic()+100
        while time.monotonic()<until:
            rows=processes();live=[]
            for pid,parent,exe in rows:
                if pid in owned or parent in owned or exe.lower()=='chrome.exe' and (image(pid) or '').lower().startswith(str(CACHE).lower()):
                    owned.add(pid);path=image(pid);live.append({'pid':pid,'parent':parent,'exe':path,'at':utc()})
                    if pid not in seen:
                        seen[pid]=live[-1];h=K.OpenProcess(0x1000,False,pid)
                        if h:handles[pid]=h
            samples.append({'at':utc(),'memory':memory(),'owned':live,'launcher_rc':launch.poll()})
            save('samples.json',samples)
            if launch.poll() is not None:break
            time.sleep(.5)
        if launch.poll() is None:
            save('operator-timeout.json',{'at':utc(),'seconds':100,'action':'stop owned CLI launcher only; browser outcome unknown'});launch.terminate();launch.wait(timeout=10)
    rc=launch.returncode
    exits={}
    for pid,h in handles.items():
        n=W.DWORD();exits[str(pid)]=n.value if K.GetExitCodeProcess(h,C.byref(n)) else 'UNKNOWN'
    save('process-exits.json',{'codes':exits,'STILL_ACTIVE_value':259,'limitations':'handles only after observed census; missed child exits UNKNOWN','first_seen':seen})
    for action in ['close','delete-data']:
        r=subprocess.run([NODE,str(CLI),'-s='+NONCE,action,'--json'],cwd=ROOT,env=env,capture_output=True,timeout=20)
        (ROOT/(action+'.stdout')).write_bytes(r.stdout);(ROOT/(action+'.stderr')).write_bytes(r.stderr);cleanup.append({'action':action,'rc':r.returncode})
    # Diagnostic ends here even if open passes: no unapproved extra launch/capture.
    save('diagnosis.json',{'open_rc':rc,'at':utc(),'observed_pids':len(seen),'cleanup':cleanup,'U10':'OPEN','compatibility_acceptance':False,'next':'Review raw process/debug evidence; no automatic retry'})
except BaseException:
    save('operator-failure.json',{'at':utc(),'traceback':traceback.format_exc()});rc=2
finally:
    for h in handles.values():K.CloseHandle(h)
    remaining=[pid for pid,_,exe in processes() if exe.lower()=='chrome.exe' and (image(pid) or '').lower().startswith(str(CACHE).lower())]
    save('cleanup.json',{'at':utc(),'actions':cleanup,'remaining_owned_cache_chrome_pids':remaining,'no_global_kill':True})
    if LOCK.read_text(encoding='utf-8-sig').split('\t')[0]==NONCE:LOCK.write_bytes(b'')
    ledger=Path(r'C:\tl-win\do-luong.csv')
    with ledger.open('a',encoding='utf-8',newline='') as f:f.write(f'{utc()},{NONCE},wp1287,{H2},r4-u10-diagnostic,0,0,{rc},{(dt.datetime.now(dt.timezone.utc)-start).total_seconds():.3f},operator,UNKNOWN,no,may=DESKTOP-T9R33P2;diagnostic_only;no_acceptance\n')
    save('terminal.json',{'rc':rc,'at':utc(),'used':1,'reserved':0,'limit':1,'U10':'OPEN','lock_released':not LOCK.read_bytes(),'candidate':H2})
    files={p.name:{'bytes':p.stat().st_size,'sha256':digest(p)} for p in ROOT.iterdir() if p.is_file()}
    save('evidence-manifest.json',files)
print(json.dumps({'operator_rc':rc,'U10':'OPEN','root':str(ROOT),'allowance_used':1,'retry':False}),flush=True)
sys.exit(0 if rc==0 else 2)
