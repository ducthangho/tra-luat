"""Offline r2 review: mutate existing fixtures only; never write reviewed repository."""
import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
import legacy_bridge_recheck as p

t,b,ROOT=p.t,p.b,p.ROOT

def run(root,al,debt=(),flags=(),env=None):
    bootstrap='''import importlib.util,json,sys
sp=importlib.util.spec_from_file_location('gate',sys.argv[1]);b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
c=json.loads(sys.argv[2]);b.ALLOWLIST_CUTOVER=c['allow'];b.NO_DA_DO={};b.NO_CAU_LICH_SU=frozenset(tuple(k) for k in c['debt'])
raise SystemExit(b.main(sys.argv[3:]))
'''
    r=subprocess.run([sys.executable,'-c',bootstrap,str(ROOT/'ops/bien_nhan_v2.py'),json.dumps({'allow':al,'debt':list(debt)}),'--root',str(root),*flags],text=True,capture_output=True,env=env)
    return dict(rc=r.returncode,stdout=r.stdout.strip(),stderr=r.stderr.strip(),traceback='Traceback' in r.stderr,dead='NỢ CHẾT' in r.stderr)

def emit(label,**kw):p.emit(label,**kw)

def yaml_errors():
    for label,text in [('timestamp','date: 2026-99-99\n'),('deep','x: '+('['*1200)+'0'+(']'*1200)+'\n'),('normal','x: 1\n')]:
      with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp);k=t._kho_cau(root)
        al=t._ghi_bn_cau(root,k,{'r.receipt.yaml':t._bn_cau(1,'x: 1\n')})
        (root/b.THU_MUC/'hong.receipt.yaml').write_text(text)
        for flag in ((),('--sinh-no',),('--sinh-no-cau-lich-su',)):
            emit('yaml-'+label,flags=flag,result=run(root,al,flags=flag))

def symlinks():
    for label in ('absent','dangling','self-loop','parent-loop','directory','not-directory','fifo'):
      for debt in (False,True):
        if label=='fifo':continue # a blocking read is not a useful unattended measurement
        with tempfile.TemporaryDirectory() as tmp:
          root=Path(tmp)
          d,_=t._bn_surface('ops/reviews/v/run.json','')
          al=t._kho_surface(root,d,'{"execution_surface":"codex_cli"}','provider: openai_codex\nexecution_surface: codex_service\n')
          rj=root/'ops/reviews/v/run.json';rj.unlink()
          if label=='dangling':rj.symlink_to('missing.json')
          elif label=='self-loop':rj.symlink_to('run.json')
          elif label=='parent-loop':
            rj.parent.rmdir();rj.parent.symlink_to('v')
          elif label=='directory':rj.mkdir()
          elif label=='not-directory':
            rj.parent.rmdir();rj.parent.write_text('file instead of dir')
          key=('r.receipt.yaml','verdict_path',b.LUAT_SURFACE)
          emit('run-path-'+label,debt=debt,result=run(root,al,(key,) if debt else ()))

def refs():
    for label in ('no-origin-HEAD','dangling-symref','corrupt-master','missing-commit','tree','blob'):
      with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp);k=t._kho_cau(root)
        al=t._ghi_bn_cau(root,k,{'r.receipt.yaml':t._bn_cau(1,f'anchor:\n    mo_ta: Commit {k["M"][:7]} chua vao master.\n')})
        k['g']('update-ref','refs/remotes/origin/master',k['M'])
        if label=='dangling-symref':k['g']('symbolic-ref','refs/remotes/origin/HEAD','refs/remotes/origin/missing')
        elif label=='corrupt-master':(root/'.git/refs/remotes/origin/master').write_text('this-is-not-an-oid\n')
        elif label=='missing-commit':(root/'.git/refs/remotes/origin/master').write_text('d'*40+'\n')
        elif label=='tree':k['g']('update-ref','refs/remotes/origin/master',k['g']('rev-parse','HEAD^{tree}'))
        elif label=='blob':k['g']('update-ref','refs/remotes/origin/master',k['g']('rev-parse','HEAD:a.txt'))
        observed=[]
        for ref in ('refs/remotes/origin/HEAD','refs/remotes/origin/master'):
            q=subprocess.run(['git','-C',str(root),'show-ref','--verify','--quiet',ref],capture_output=True,text=True)
            observed.append([ref,q.returncode,q.stdout.strip(),q.stderr.strip()])
        emit('default-ref-'+label,show_ref=observed,result=run(root,al))

def matrix():
    old_cli=t._chay_cli
    for prefix in ('c91','c92'):
        rows=[]
        def spy(root,al,no_cau=frozenset(),co=(),path=None):
            rc,err=old_cli(root,al,no_cau,co,path)
            rows.append(dict(debt=list(no_cau),flags=list(co),path_absent=path is not None,rc=rc,stderr=err.strip()))
            return rc,err
        t._chay_cli=spy
        try:state,detail=t._chay_1(next(fn for fn in t.CA if fn.__name__.startswith(prefix)))
        finally:t._chay_cli=old_cli
        emit('existing-matrix',case=prefix,state=state,detail=detail,calls=rows)
    emit('existing-b6-docstring',doc=t.c72_A3_bien_the_co_dau_khong_dau_xuong_dong_deu_bi_nhan.__doc__)

def multi():
    with tempfile.TemporaryDirectory() as tmp:
      root=Path(tmp);k=t._kho_cau(root)
      al=t._ghi_bn_cau(root,k,{
        'a-hong.receipt.yaml':t._bn_cau(1,f"anchor:\n    mo_ta: Commit {k['X'][:7]} chua vao master.\n"),
        'b-old.receipt.yaml':t._bn_cau(1,f"anchor:\n    mo_ta: Head {k['B0']} chua duoc review lai.\n"),
        'c-new.receipt.yaml':t._bn_cau(2,'x: 1\n',k['B0']),
      })
      emit('multi-control',result=run(root,al))
      obj=root/'.git/objects'/k['X'][:2]/k['X'][2:];obj.unlink();obj.write_bytes(b'not-zlib')
      emit('multi-git-error',result=run(root,al))

def permissions():
    emit('permission-uid',uid=os.geteuid())
    for kind in ('receipt','run-json','verdict','run-parent'):
      for debt in (False,True):
       with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        d,_=t._bn_surface('ops/reviews/v/run.json','')
        al=t._kho_surface(root,d,'{"execution_surface":"codex_cli"}','provider: openai_codex\nexecution_surface: codex_service\n')
        targets={'receipt':root/b.THU_MUC/'r.receipt.yaml','run-json':root/'ops/reviews/v/run.json','verdict':root/'ops/reviews/v.md','run-parent':root/'ops/reviews/v'}
        target=targets[kind];mode=target.stat().st_mode;target.chmod(0)
        try:
         try:target.read_bytes();read_failure=None
         except Exception as ex:read_failure=type(ex).__name__
         key=('r.receipt.yaml','verdict_path',b.LUAT_SURFACE)
         emit('permission-'+kind,debt=debt,read_failure=read_failure,result=run(root,al,(key,) if debt else ()))
        finally:target.chmod(mode)

def gitfail():
    with tempfile.TemporaryDirectory() as tmp:
      root=Path(tmp);k=t._kho_cau(root)
      al=t._ghi_bn_cau(root,k,{'r.receipt.yaml':t._bn_cau(1,f"anchor:\n    mo_ta: Commit {k['M'][:7]} chua vao master.\n")})
      shim=root/'shim';shim.mkdir();g=shim/'git'
      for code in (1,2,127,128):
        g.write_text(f'#!/bin/sh\nexit {code}\n');g.chmod(0o755)
        emit('git-exit',git_rc=code,result=run(root,al,env=dict(os.environ,PATH=str(shim))))
      g.write_bytes(b'#!/bin/sh\nprintf "\377"\n');g.chmod(0o755)
      emit('git-encoding',result=run(root,al,env=dict(os.environ,PATH=str(shim))))

if __name__=='__main__':globals()[sys.argv[1]]()
