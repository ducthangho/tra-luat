import contextlib, importlib.util, io, json, os, shutil, subprocess, sys, tempfile, time, zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
COPY=Path('/tmp/wp960-r3-recheck-copy')
spec=importlib.util.spec_from_file_location('tests_r3',COPY/'ops/bien_nhan_v2_test.py')
t=importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
b=t.bnv2
KEY=('r.receipt.yaml','anchor.mo_ta',b.LUAT_ANCESTRY)
def log(**x): print(json.dumps(x,ensure_ascii=False),flush=True)
def git(p,*args,inp=None,env=None):
    r=subprocess.run(['git','-C',str(p),*args],input=inp,text=True,capture_output=True,env={**os.environ,**b._ENV_GIT,**(env or {})})
    return dict(rc=r.returncode,out=r.stdout.strip(),err=r.stderr.strip())
def raw(p,al,no=(),co=(),env=None):
    code='import importlib.util,sys; from pathlib import Path; s=importlib.util.spec_from_file_location("b",sys.argv[1]); b=importlib.util.module_from_spec(s); s.loader.exec_module(b); b.ALLOWLIST_CUTOVER='+repr(al)+'; b.NO_DA_DO={}; b.NO_CAU_LICH_SU=frozenset('+repr(list(no))+'); sys.exit(b.main(["--root",sys.argv[2]]+sys.argv[3:]))'
    r=subprocess.run([sys.executable,'-B','-c',code,str(b.__file__),str(p),*co],text=True,capture_output=True,env={**os.environ,**(env or {})})
    return dict(rc=r.returncode,out=r.stdout.strip(),err=r.stderr.strip(),traceback='Traceback' in r.stderr,dead='NỢ CHẾT' in r.stderr)
def anc(p,which='M',pure=False):
    k=t._kho_cau(p)
    sha=t._commit_tien_to_so(p,k,str.isalpha,'chu',30000) if pure else k[which]
    if pure:k['g']('merge','-q','--no-ff',sha,'-m','merge')
    al=t._ghi_bn_cau(p,k,{'r.receipt.yaml':t._bn_cau(1,f'anchor:\n    mo_ta: Ban {sha[:7]} chua vao master.\n')})
    return k,sha,al

def matrix():
    orig=t._chay_cli
    n=[0]
    def trace(*a,**kw):
        r=orig(*a,**kw);n[0]+=1;log(call=n[0],flags=kw.get('co',[]),rc=r[0],stderr=r[1]);return r
    t._chay_cli=trace
    for fn in [t.c91_B2_MA_TRAN_nguon_hong_qua_CLI_co_va_khong_no,t.c92_B2_co_SINH_NO_cung_bien_voi_cong,t.c93_ung_vien_CHI_TINH_COMMIT_blob_chung_tien_to_khong_mo_ho,t.c94_giao_thuc_git_DANG_LA_la_KHONG_DO_DUOC]:
        log(case=fn.__name__,result=t._chay_1(fn))

def objects():
    for name in ['empty','zlib','valid-zlib-wrong-hash','missing','replace','graft','branch-prefix','trace','config-warning']:
        with tempfile.TemporaryDirectory(prefix='r3-obj-') as d:
            p=Path(d); k,sha,al=anc(p,which='B0' if name in ('valid-zlib-wrong-hash','replace','graft') else 'M',pure=name in ('empty','zlib'))
            before=raw(p,al);log(name=name,phase='before',sha=sha,result=before)
            if name in ('empty','zlib','missing'):
                f=p/'.git/objects'/sha[:2]/sha[2:]
                f.chmod(0o644)
                if name=='missing': f.unlink()
                else:f.write_bytes(b'' if name=='empty' else b'garbage')
            if name=='valid-zlib-wrong-hash':
                target=k['M'];f=p/'.git/objects'/target[:2]/target[2:]
                content=bytes.fromhex('')+zlib.decompress(f.read_bytes()).split(b'\0',1)[1]
                changed=content.replace(b'parent '+k['B0'].encode()+b'\n',b'')
                assert changed!=content
                f.chmod(0o644); f.write_bytes(zlib.compress(b'commit '+str(len(changed)).encode()+b'\0'+changed))
                log(name=name,fsck=git(p,'fsck','--full'))
            if name=='replace': log(name=name,replace=git(p,'replace',k['M'],k['X']))
            if name=='graft':(p/'.git/info/grafts').write_text(k['M']+'\n')
            if name=='branch-prefix':
                k['g']('update-ref','refs/remotes/origin/master',k['M']);k['g']('branch','-m','main');k['g']('branch','master/topic')
            if name=='config-warning':
                k['g']('config','core.fsyncObjectFiles','true')
            env={'GIT_TRACE':'1'} if name=='trace' else {}
            log(name=name,health=git(p,'rev-parse','--is-shallow-repository',env=env),candidates=git(p,'rev-parse','--disambiguate='+sha[:7],env=env),kind=git(p,'cat-file','--batch-check=%(objectname) %(objecttype)',inp=sha+'\n',env=env),refs=git(p,'for-each-ref','--format=%(refname) %(objectname) %(objecttype)',*b._REF_MAC_DINH,env=env),ancestor=git(p,'merge-base','--is-ancestor',sha,'refs/heads/master' if name!='branch-prefix' else 'refs/remotes/origin/master',env=env))
            for no in ((),(KEY,)):
                log(name=name,phase='after',debt=bool(no),result=raw(p,al,no,env=env))

def partial():
    with tempfile.TemporaryDirectory(prefix='r3-partial-') as d:
        p=Path(d);src=p/'source';src.mkdir();k,sha,al=anc(src)
        k['g']('config','uploadpack.allowFilter','true')
        dst=p/'partial'
        r=subprocess.run(['git','clone','-q','--no-checkout','--no-local','--filter=blob:none',src.as_uri(),str(dst)],text=True,capture_output=True)
        log(clone_rc=r.returncode,stderr=r.stderr)
        log(config=git(dst,'config','--local','--list'),missing=git(dst,'rev-list','--objects','--all','--missing=print'),promisor_files=[x.name for x in (dst/'.git/objects/pack').glob('*.promisor')])
        try: out=b._kho_lanh(dst);log(health='accepted',result=out)
        except Exception as ex:log(health='rejected',exception=str(ex))
        shutil.copytree(src/'ops',dst/'ops')
        log(gate=raw(dst,al),candidate=git(dst,'rev-parse','--disambiguate='+sha[:7]))

def yaml_cli():
    for name,content in [('timestamp','date: 2026-99-99\n'),('deep','a: '+'['*1200+']'*1200+'\n'),('utf8',b'x: \xff\n'),('dir',None),('good','x: 1\n')]:
        with tempfile.TemporaryDirectory(prefix='r3-yaml-') as d:
            p=Path(d);k,sha,al=anc(p);f=p/b.THU_MUC/'hong.receipt.yaml'
            if content is None:f.mkdir()
            elif isinstance(content,bytes):f.write_bytes(content)
            else:f.write_text(content)
            for co in ((),('--sinh-no',),('--sinh-no-cau-lich-su',)):
                log(name=name,flags=co,result=raw(p,al,co=co))

if __name__=='__main__': globals()[sys.argv[1]]()
