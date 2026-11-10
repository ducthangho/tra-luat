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

ROOT = Path(r'C:\tl-win\wp1287-r6-loader-20261110')
OLD = Path(r'C:\tl-win\wp1287-H1-native-recovery2')
NODE = r'C:\Program Files\nodejs\node.exe'
INSTALL = OLD / 'installation'
CACHE = OLD / 'browser-cache'
CLI = INSTALL / 'node_modules/@playwright/cli/playwright-cli.js'
CHROME = CACHE / 'chromium-1252/chrome-win64/chrome.exe'
NONCE = 'tl-pw-r6-loader-20261110'
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


# Read only loader and wait-chain metadata for the owned browser. No dump or privilege change.
class ME(C.Structure):
    _fields_=[('size',W.DWORD),('moduleid',W.DWORD),('pid',W.DWORD),('globaluses',W.DWORD),('processuses',W.DWORD),('base',C.c_void_p),('bytes',W.DWORD),('handle',W.HMODULE),('name',W.WCHAR*256),('path',W.WCHAR*260)]
class TE(C.Structure):
    _fields_=[('size',W.DWORD),('usage',W.DWORD),('tid',W.DWORD),('pid',W.DWORD),('basepriority',W.LONG),('delta',W.LONG),('flags',W.DWORD)]
class WL(C.Structure):
    _fields_=[('name',W.WCHAR*128),('timeout',C.c_longlong),('alertable',W.BOOL)]
class WT(C.Structure):
    _fields_=[('pid',W.DWORD),('tid',W.DWORD),('wait_ms',W.DWORD),('switches',W.DWORD)]
class WU(C.Union):
    _fields_=[('lock',WL),('thread',WT)]
class WN(C.Structure):
    _fields_=[('type',C.c_int),('status',C.c_int),('info',WU)]
K.Module32FirstW.argtypes=[W.HANDLE,C.POINTER(ME)]
K.Module32NextW.argtypes=[W.HANDLE,C.POINTER(ME)]
K.Thread32First.argtypes=[W.HANDLE,C.POINTER(TE)]
K.Thread32Next.argtypes=[W.HANDLE,C.POINTER(TE)]
A=C.WinDLL('advapi32',use_last_error=True)
A.OpenThreadWaitChainSession.argtypes=[W.DWORD,C.c_void_p];A.OpenThreadWaitChainSession.restype=W.HANDLE
A.GetThreadWaitChain.argtypes=[W.HANDLE,C.c_size_t,W.DWORD,W.DWORD,C.POINTER(W.DWORD),C.POINTER(WN),C.POINTER(W.BOOL)]
A.CloseThreadWaitChainSession.argtypes=[W.HANDLE]
def probe(pid):
    result={'at':utc(),'pid':pid,'modules':[],'threads':[],'no_memory_dump':True,'no_privilege_changes':True}
    h=K.CreateToolhelp32Snapshot(8|16,pid)
    if h==C.c_void_p(-1).value:result['module_error']=C.get_last_error()
    else:
        try:
            e=ME();e.size=C.sizeof(e);ok=K.Module32FirstW(h,C.byref(e))
            while ok:
                path=e.path;scope='owned_cache' if path.lower().startswith(str(CACHE).lower()) else 'windows' if path.lower().startswith(os.environ.get('SystemRoot',r'C:\Windows').lower()) else 'other'
                result['modules'].append({'name':e.name,'bytes':e.bytes,'scope':scope})
                ok=K.Module32NextW(h,C.byref(e))
        finally:K.CloseHandle(h)
    tids=[];h=K.CreateToolhelp32Snapshot(4,0)
    try:
        e=TE();e.size=C.sizeof(e);ok=K.Thread32First(h,C.byref(e))
        while ok:
            if e.pid==pid:tids.append(e.tid)
            ok=K.Thread32Next(h,C.byref(e))
    finally:K.CloseHandle(h)
    session=A.OpenThreadWaitChainSession(0,None)
    if not session:result['wct_session_error']=C.get_last_error();return result
    try:
        for tid in tids[:64]:
            nodes=(WN*16)();count=W.DWORD(16);cycle=W.BOOL(False);C.set_last_error(0)
            ok=A.GetThreadWaitChain(session,0,0,tid,C.byref(count),nodes,C.byref(cycle))
            row={'tid':tid,'ok':bool(ok),'cycle':bool(cycle.value),'nodes':[]}
            if not ok:row['error']=C.get_last_error()
            else:
                for i in range(min(count.value,16)):
                    n=nodes[i];v={'type':n.type,'status':n.status}
                    if n.type==8:v.update(owned_process=(n.info.thread.pid==pid),wait_ms=n.info.thread.wait_ms,context_switches=n.info.thread.switches)
                    row['nodes'].append(v)
            result['threads'].append(row)
    finally:A.CloseThreadWaitChainSession(session)
    return result
if '--probe-selfcheck' in sys.argv:
    x=probe(os.getpid());print(json.dumps({'wn_bytes':C.sizeof(WN),'me_bytes':C.sizeof(ME),'module_count':len(x['modules']),'thread_count':len(x['threads']),'wct_session_error':x.get('wct_session_error'),'no_browser':True}));sys.exit(0)

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
lockline='\t'.join([NONCE,start.isoformat(),deadline.isoformat(),'WP1287 r6 one loader/wait-chain diagnostic',start.isoformat()])
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
        owned={launch.pid};t0=time.monotonic();until=t0+100;probe_marks=set();loader_probes=[]
        while time.monotonic()<until:
            rows=processes();live=[]
            for pid,parent,exe in rows:
                if pid in owned or parent in owned or exe.lower()=='chrome.exe' and (image(pid) or '').lower().startswith(str(CACHE).lower()):
                    owned.add(pid);path=image(pid);live.append({'pid':pid,'parent':parent,'exe':path,'at':utc()})
                    if pid not in seen:
                        seen[pid]=live[-1];h=K.OpenProcess(0x1000,False,pid)
                        if h:handles[pid]=h
            elapsed=time.monotonic()-t0
            for mark in [5,15,25]:
                if elapsed>=mark and mark not in probe_marks:
                    probe_marks.add(mark)
                    for row in live:
                        if row['exe'] and row['exe'].lower()==str(CHROME).lower():loader_probes.append({'scheduled_second':mark,'probe':probe(row['pid'])})
                    save('loader-probes.json',loader_probes)
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
