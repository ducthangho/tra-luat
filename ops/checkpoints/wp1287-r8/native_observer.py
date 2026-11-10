"""Bounded Windows observer, called in an owned subprocess. Raw records stay native."""
import ctypes as C
from ctypes import wintypes as W
import os,time,json,sys,hashlib,datetime
from pathlib import Path
from contract import same_identity,module_state,presence,bridge
K=C.WinDLL('kernel32',use_last_error=True)
for name,args,ret in [('CreateToolhelp32Snapshot',[W.DWORD,W.DWORD],W.HANDLE),('OpenProcess',[W.DWORD,W.BOOL,W.DWORD],W.HANDLE),('CloseHandle',[W.HANDLE],W.BOOL),('QueryFullProcessImageNameW',[W.HANDLE,W.DWORD,W.LPWSTR,C.POINTER(W.DWORD)],W.BOOL),('GetProcessTimes',[W.HANDLE]+[C.POINTER(W.FILETIME)]*4,W.BOOL),('GetExitCodeProcess',[W.HANDLE,C.POINTER(W.DWORD)],W.BOOL)]:
    f=getattr(K,name);f.argtypes=args;f.restype=ret
INVALID=C.c_void_p(-1).value
class PE(C.Structure):
    _fields_=[('size',W.DWORD),('usage',W.DWORD),('pid',W.DWORD),('heap',C.c_size_t),('module',W.DWORD),('threads',W.DWORD),('parent',W.DWORD),('priority',W.LONG),('flags',W.DWORD),('exe',W.WCHAR*260)]
class ME(C.Structure):
    _fields_=[('size',W.DWORD),('moduleid',W.DWORD),('pid',W.DWORD),('globaluses',W.DWORD),('processuses',W.DWORD),('base',C.c_void_p),('bytes',W.DWORD),('handle',W.HMODULE),('name',W.WCHAR*256),('path',W.WCHAR*260)]
class TE(C.Structure):
    _fields_=[('size',W.DWORD),('usage',W.DWORD),('tid',W.DWORD),('pid',W.DWORD),('priority',W.LONG),('delta',W.LONG),('flags',W.DWORD)]
for name,typ in [('Process32FirstW',PE),('Process32NextW',PE),('Module32FirstW',ME),('Module32NextW',ME),('Thread32First',TE),('Thread32Next',TE)]:
    getattr(K,name).argtypes=[W.HANDLE,C.POINTER(typ)];getattr(K,name).restype=W.BOOL
class WL(C.Structure):_fields_=[('name',W.WCHAR*128),('timeout',C.c_longlong),('alertable',W.BOOL)]
class WT(C.Structure):_fields_=[('pid',W.DWORD),('tid',W.DWORD),('WaitTime',W.DWORD),('ContextSwitches',W.DWORD)]
class WU(C.Union):_fields_=[('lock',WL),('thread',WT)]
class WN(C.Structure):_fields_=[('type',C.c_int),('status',C.c_int),('info',WU)]
A=C.WinDLL('advapi32',use_last_error=True)
A.OpenThreadWaitChainSession.argtypes=[W.DWORD,C.c_void_p];A.OpenThreadWaitChainSession.restype=W.HANDLE
A.GetThreadWaitChain.argtypes=[W.HANDLE,C.c_size_t,W.DWORD,W.DWORD,C.POINTER(W.DWORD),C.POINTER(WN),C.POINTER(W.BOOL)]
A.CloseThreadWaitChainSession.argtypes=[W.HANDLE]
def stamp():return {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mono_ns':time.monotonic_ns()}
def checked(f,*args):
    C.set_last_error(0);v=f(*args);err=C.get_last_error() if not v else None;return v,err

def identity(pid,handle=None):
    h=handle or K.OpenProcess(0x1000,False,pid)
    if not h:return None
    try:
        times=[W.FILETIME() for _ in range(4)];b=C.create_unicode_buffer(32768);n=W.DWORD(len(b))
        if not K.GetProcessTimes(h,*[C.byref(t) for t in times]) or not K.QueryFullProcessImageNameW(h,0,b,C.byref(n)):return None
        value=lambda t:(t.dwHighDateTime<<32)|t.dwLowDateTime
        code=W.DWORD();ok=K.GetExitCodeProcess(h,C.byref(code))
        return {'pid':pid,'birth':value(times[0]),'exit_time':value(times[1]),'image':b.value.lower(),'alive':ok and code.value==259}
    finally:
        if handle is None:K.CloseHandle(h)
def census():
    h=K.CreateToolhelp32Snapshot(2,0)
    if h==INVALID:raise OSError(C.get_last_error(),'process snapshot')
    rows=[];p=PE();p.size=C.sizeof(p)
    try:
        ok,err=checked(K.Process32FirstW,h,C.byref(p))
        if not ok:raise OSError(err,'process first')
        while ok:
            rows.append({'pid':p.pid,'parent':p.parent,'exe':p.exe})
            ok,err=checked(K.Process32NextW,h,C.byref(p))
        if err!=18:raise OSError(err,'partial process census')
    finally:K.CloseHandle(h)
    return rows

def shared_read(path):
    import msvcrt
    K.CreateFileW.argtypes=[W.LPCWSTR,W.DWORD,W.DWORD,C.c_void_p,W.DWORD,W.DWORD,W.HANDLE];K.CreateFileW.restype=W.HANDLE
    h=K.CreateFileW(path,0x80000000,7,None,3,0x80,None)
    if h==INVALID:raise C.WinError(C.get_last_error())
    try:fd=msvcrt.open_osfhandle(h,os.O_RDONLY|os.O_BINARY)
    except BaseException:K.CloseHandle(h);raise
    return os.fdopen(fd,'rb')

def file_bridge(path):
    # Same observed path, read-only handle with FILE_SHARE_READ|WRITE|DELETE; Windows file index via fstat.
    try:
        with shared_read(path) as f:
            a=os.fstat(f.fileno());before={'path':os.path.realpath(path),'device':a.st_dev,'file_id':a.st_ino,'bytes':a.st_size,'mtime_ns':a.st_mtime_ns}
            if a.st_size>16*1024*1024:return {'state':'not_hashed_size_bound','identity':before}
            digest=hashlib.file_digest(f,'sha256').hexdigest();b=os.fstat(f.fileno());c=os.stat(path)
            after={'path':os.path.realpath(path),'device':b.st_dev,'file_id':b.st_ino,'bytes':b.st_size,'mtime_ns':b.st_mtime_ns}
            state=bridge(before,after,os.path.realpath(path)) if (c.st_dev,c.st_ino,c.st_size,c.st_mtime_ns)==(b.st_dev,b.st_ino,b.st_size,b.st_mtime_ns) else 'UNKNOWN'
            return {'state':state,'identity':before,'sha256':digest,'at':stamp(),'scope':'observed_disk_file_not_memory'}
    except OSError as e:return {'state':'UNKNOWN','error':e.winerror}

def probe(expected):
    h=K.OpenProcess(0x1000,False,expected['pid']);before=identity(expected['pid'],h) if h else None
    out={'start':stamp(),'identity_before':before,'modules':[],'snapshot_attempts':[],'flags':24,'bitness':C.sizeof(C.c_void_p)*8,'ME_bytes':C.sizeof(ME),'WN_bytes':C.sizeof(WN)}
    if not same_identity(expected,before) or not before['alive']:
        if h:K.CloseHandle(h)
        out['state']='inconsistent';return out
    try:
        sh=INVALID
        for attempt in range(2):
            C.set_last_error(0);sh=K.CreateToolhelp32Snapshot(24,expected['pid']);err=C.get_last_error() if sh==INVALID else None
            out['snapshot_attempts'].append({'ok':sh!=INVALID,'error':err,'at':stamp()})
            if sh!=INVALID or err!=24:break
        first_ok=False;first_error=None;next_error=None
        if sh!=INVALID:
            try:
                e=ME();e.size=C.sizeof(e);first_ok,first_error=checked(K.Module32FirstW,sh,C.byref(e));ok=first_ok
                while ok:
                    out['modules'].append({'name':e.name,'path':e.path,'base':e.base,'bytes':e.bytes})
                    ok,next_error=checked(K.Module32NextW,sh,C.byref(e))
            finally:K.CloseHandle(sh)
        out.update(first_ok=bool(first_ok),first_error=first_error,next_error=next_error)
        after=identity(expected['pid'],h);main=any(x['path'].lower()==before['image'] for x in out['modules'])
        out['identity_after']=after;out['state']=module_state(sh!=INVALID,first_ok,first_error,next_error,out['modules'],same_identity(before,after),main)
        out['chrome_dll']=presence(out['state'],[x['name'] for x in out['modules']],'chrome.dll')
        # Bridge only selected small files actually observed, never filename search elsewhere.
        for row in out['modules']:
            if row['name'].lower() in ('chrome.exe','chrome_elf.dll','uvh64.dll'):row['file_bridge']=file_bridge(row['path'])
        tids=[];sh=K.CreateToolhelp32Snapshot(4,0);out['threads']=[]
        if sh!=INVALID:
            try:
                e=TE();e.size=C.sizeof(e);ok,err=checked(K.Thread32First,sh,C.byref(e))
                while ok:
                    if e.pid==expected['pid']:tids.append(e.tid)
                    ok,err=checked(K.Thread32Next,sh,C.byref(e))
                out['thread_walk_end_error']=err
            finally:K.CloseHandle(sh)
        else:out['thread_snapshot_error']=C.get_last_error()
        out.update(thread_count=len(tids),threads_truncated=len(tids)>64,wct_flags=0,max_nodes=16)
        session=A.OpenThreadWaitChainSession(0,None)
        if not session:out['wct_session_error']=C.get_last_error()
        else:
            try:
                for tid in tids[:64]:
                    nodes=(WN*16)();count=W.DWORD(16);cycle=W.BOOL();ok,err=checked(A.GetThreadWaitChain,session,0,0,tid,C.byref(count),nodes,C.byref(cycle));row={'tid':tid,'ok':bool(ok),'error':err,'cycle':bool(cycle.value),'returned_count':count.value,'nodes':[]}
                    if ok:
                        for n in nodes[:min(16,count.value)]:
                            value={'type':n.type,'status':n.status}
                            if n.type==8:value.update(owned_process=n.info.thread.pid==expected['pid'],WaitTime=n.info.thread.WaitTime,ContextSwitches=n.info.thread.ContextSwitches)
                            row['nodes'].append(value)
                    out['threads'].append(row)
            finally:A.CloseThreadWaitChainSession(session)
        out['end']=stamp();return out
    finally:K.CloseHandle(h)
if __name__=='__main__':
    if sys.argv[1]=='selfcheck':
        x=probe(identity(os.getpid()));assert x['bitness']==64 and x['ME_bytes']==1080 and x['WN_bytes']==280 and x['state']=='complete_walk' and len(x['modules'])>0
        print(json.dumps({'passed':True,'bitness':64,'ME_bytes':1080,'WN_bytes':280,'module_count':len(x['modules']),'thread_count':x['thread_count'],'wct_session_error':x.get('wct_session_error'),'no_browser':True}))
    else:
        expected=json.loads(Path(sys.argv[1]).read_text());Path(sys.argv[2]).write_text(json.dumps(probe(expected),indent=2),encoding='utf-8')
