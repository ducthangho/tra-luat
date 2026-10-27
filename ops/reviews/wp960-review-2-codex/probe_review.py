#!/usr/bin/env python3
"""Ngoại tuyến: gọi ca/builder sẵn có, chỉ đổi fixture trong thư mục tạm."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import hashlib
import yaml
ROOT=Path(os.environ.get('WP960_REPO','/tmp/wp960-r2-Dt2G8H/repo'))
spec=importlib.util.spec_from_file_location('bt', ROOT/'ops/bien_nhan_v2_test.py')
t=importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
b=t.bnv2

def out(label, **kw): print(label, json.dumps(kw,ensure_ascii=False),flush=True)
def result(label,tmp,al,no=frozenset()):
 try:
  rc,loi,tk=t._kiem_cau(tmp,al,no)
  out(label,rc=rc,loi=loi,chua_do=tk.get('chua_do'),surface_chua_do=tk.get('surface_chua_do'))
 except Exception as e: out(label,exception=type(e).__name__,error=str(e))
def al_now(tmp):return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (tmp/b.THU_MUC).glob('*.receipt.yaml')}
def sentence(k):return f"Commit {k['M'][:7]} chua vao master."
def anchors():
 for style in ['plain','folded','literal','list']:
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);k=t._kho_cau(p);c=sentence(k)
   def body(sp=False):
    s=c.replace('chua vao','chua  vao') if sp else c
    if style=='plain': return f'anchor:\n    mo_ta: {s}\n'
    if style=='folded':return f'anchor:\n    mo_ta: >-\n        {s.replace("vao master",chr(10)+"        vao master")}\n'
    if style=='literal':return f'anchor:\n    mo_ta: |\n        {s.replace("vao master",chr(10)+"        vao master")}\n'
    return f'anchor:\n    mo_ta:\n        - {s}\n'
   al=t._ghi_bn_cau(p,k,{'r.receipt.yaml':t._bn_cau(1,body())});first=k['g']('rev-parse','HEAD')
   (p/'b.txt').write_text('b');k['g']('add','-A');k['g']('commit','-qm','B');later=k['g']('rev-parse','HEAD')
   for tag,sp in [('anchor-only',False),('reformat',True)]:
    (p/b.THU_MUC/'r.receipt.yaml').write_text(t._bn_cau(1,body(sp)+f'    dung_tai: {later}\n'))
    result(style+'-'+tag,p,al_now(p))
   k['g']('add','-A');k['g']('commit','-qm','format');result(style+'-committed',p,al_now(p))
   out(style+'-identity',first=first,later=later)
 # Đổi tên tệp sau khi câu đã tồn tại; chỉ đổi fixture.
 with tempfile.TemporaryDirectory() as td:
  p=Path(td);k=t._kho_cau(p);c=sentence(k)
  t._ghi_bn_cau(p,k,{'old.receipt.yaml':t._bn_cau(1,f'anchor:\n    mo_ta: {c}\n')});first=k['g']('rev-parse','HEAD')
  (p/'b.txt').write_text('b');k['g']('add','-A');k['g']('commit','-qm','B');later=k['g']('rev-parse','HEAD')
  old=p/b.THU_MUC/'old.receipt.yaml';new=p/b.THU_MUC/'new.receipt.yaml'
  old.rename(new);new.write_text(t._bn_cau(1,f'anchor:\n    mo_ta: {c}\n    dung_tai: {later}\n'))
  k['g']('add','-A');k['g']('commit','-qm','rename with late anchor')
  result('rename-late-anchor',p,al_now(p));out('rename-history',first=first,later=later,log=k['g']('log','--format=%H','--reverse','--',str(new.relative_to(p))))
def historical():
 for bad in ['yaml-invalid','alias-cycle','missing-blob','utf8']:
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);k=t._kho_cau(p);c=sentence(k);rel=f'{b.THU_MUC}/r.receipt.yaml'
   raw=t._bn_cau(1,f'anchor:\n    mo_ta: {c}\n')
   text=('cycle: &self [*self]\n' if bad=='alias-cycle' else '')+raw+('oops: [\n' if bad=='yaml-invalid' else '')
   t._ghi_bn_cau(p,k,{'r.receipt.yaml':text});
   if bad=='utf8':
    (p/rel).write_bytes(b'x: \xff\n');k['g']('add','-A');k['g']('commit','-qm','bad utf8')
   first=k['g']('rev-parse','HEAD');blob=k['g']('rev-parse',f'HEAD:{rel}')
   (p/'b.txt').write_text('b');k['g']('add','-A');k['g']('commit','-qm','B');later=k['g']('rev-parse','HEAD')
   al=t._ghi_bn_cau(p,k,{'r.receipt.yaml':raw+f'    dung_tai: {later}\n'})
   if bad=='missing-blob': (p/'.git/objects'/blob[:2]/blob[2:]).unlink()
   result('history-'+bad,p,al)
   import contextlib,io
   stdout,stderr=io.StringIO(),io.StringIO()
   saved=b.ALLOWLIST_CUTOVER,b.NO_DA_DO,b.NO_CAU_LICH_SU
   b.ALLOWLIST_CUTOVER,b.NO_DA_DO,b.NO_CAU_LICH_SU=al,{},frozenset()
   try:
    with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
     try: rc=b.main(['--root',str(p)])
     except Exception as e: rc=type(e).__name__+': '+str(e)
    out('history-'+bad+'-main-fixture-injected',rc=rc,stdout=stdout.getvalue()[-700:],stderr=stderr.getvalue()[-500:])
   finally: b.ALLOWLIST_CUTOVER,b.NO_DA_DO,b.NO_CAU_LICH_SU=saved
   code=("import importlib.util,sys; s=importlib.util.spec_from_file_location('gate',"+repr(str(ROOT/'ops/bien_nhan_v2.py'))+"); b=importlib.util.module_from_spec(s); s.loader.exec_module(b); b.ALLOWLIST_CUTOVER="+repr(al)+"; b.NO_DA_DO={}; b.NO_CAU_LICH_SU=frozenset(); sys.exit(b.main(['--root',"+repr(str(p))+"]))")
   cp=subprocess.run([sys.executable,'-c',code],capture_output=True,text=True)
   out('history-'+bad+'-process-fixture-injected',rc=cp.returncode,stdout=cp.stdout[-500:],stderr=cp.stderr[-500:])

def candidates():
 for x in ['1234abc','deadbeef','1111111','a'*40,'1'*40]:
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);k=t._kho_cau(p)
   al=t._ghi_bn_cau(p,k,{'r.receipt.yaml':t._bn_cau(1,f'anchor:\n    mo_ta: Commit `{x}` chua vao master.\n')})
   out('resolve-'+x,commit=b._commit_cua(p,x));result('candidate-'+x,p,al)
def surfaces():
 lines=[('mismatch','execution_surface: codex_service'),('two-fields','execution_surface: codex_cli; execution_surface: codex_service'),('quoted','ops/land/other/verdict.md:6: execution_surface: codex_service'),('reference-before-self','Tham chieu docs/PROTOCOL_DA_PHIEN.md:8; execution_surface: codex_service'),('line-prefix-self','VERDICT.md:2: execution_surface: codex_service')]
 for name,line in lines:
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);d,_=t._bn_surface('ops/reviews/v/run.json','');al=t._kho_surface(p,d,json.dumps({'execution_surface':'codex_cli'}),line+'\n');result('surface-'+name,p,al)
 for name,rj in [('json-error','{'),('list','[]'),('missing-field','{}'),('bad-surface',json.dumps({'execution_surface':'gibberish'}))]:
  for debt in [False,True]:
   with tempfile.TemporaryDirectory() as td:
    p=Path(td);d,_=t._bn_surface('ops/reviews/v/run.json','');al=t._kho_surface(p,d,rj,'execution_surface: codex_service\n');no=frozenset({('r.receipt.yaml','verdict_path',b.LUAT_SURFACE)}) if debt else frozenset();result(f'source-{name}-debt={debt}',p,al,no)
def old():
 for i in [69,70,71,72,73,74,75,77,78,79,80,81,82,83,84,85]:
  fn=next(f for f in t.CA if f.__name__.startswith(f'c{i}_'))
  out('case',name=fn.__name__,result=t._chay_1(fn))
def a3():
 old=b._cac_cau
 b._cac_cau=lambda van:[c for dong in van.splitlines() for c in b._RE_CAU.split(dong) if c]
 orig=t._kiem_cau
 def obs(*args,**kwargs):
  r=orig(*args,**kwargs);out('m78-fields',fields=[x.split('`')[1] for x in r[1]],rc=r[0]);return r
 t._kiem_cau=obs
 fn=next(f for f in t.CA if f.__name__.startswith('c72_'));out('m78-c72',result=t._chay_1(fn))
 b._cac_cau=old
if __name__=='__main__': globals()[sys.argv[1]]()

def debt():
 base=Path('/tmp/wp960-r2-Dt2G8H/base')
 sets={}
 for name,root in [('head',ROOT),('base',base)]:
  for tag,no in [('frozen',None),('empty',frozenset())]:
   loi,tk=b.kiem(root,no_cau_lich_su=no)
   vp=set(tk['vi_pham_cau']);sets[name]=vp
   out(name+'-'+tag,rc=b._ma_thoat(loi,tk),n_errors=len(loi),unknown=tk['chua_do'],counts=tk['no_cau'],n_violations=len(vp),equals_frozen=vp==b.NO_CAU_LICH_SU,extra=sorted(vp-b.NO_CAU_LICH_SU),missing=sorted(b.NO_CAU_LICH_SU-vp))
 out('base-head-parity',equal=sets['base']==sets['head'])
 # A7 đo byte ở base trước thi công.
 text=(base/'ops/bien_nhan_v2.py').read_text();tests=(base/'ops/bien_nhan_v2_test.py').read_text()
 out('A7',new_law_exists='_kiem_cau_lich_su' in text,new_debt_exists='NO_CAU_LICH_SU' in text,new_A1_exists='def c69_' in tests)

def measurement():
 for name in ['git-fails','merge-base-fails','branch-missing','moc-missing','current-alias','unreadable-receipt']:
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);k=t._kho_cau(p);c=sentence(k)
   extra=f'    dung_tai: {"abc1234"*5+"abc12"}\n' if name=='moc-missing' else ''
   al=t._ghi_bn_cau(p,k,{'r.receipt.yaml':t._bn_cau(1,f'anchor:\n    mo_ta: {c}\n'+extra)+('cycle: &self [*self]\n' if name=='current-alias' else '')})
   oldgit=b._git;oldbam=b._bam
   if name=='git-fails':b._git=lambda *a,**kw:(127,'')
   if name=='merge-base-fails':b._git=lambda *a,**kw:(127,'') if a[1]=='merge-base' else oldgit(*a,**kw)
   if name=='branch-missing':k['g']('update-ref','-d','refs/heads/master')
   if name=='unreadable-receipt':
    rp=p/b.THU_MUC/'r.receipt.yaml';rp.unlink();rp.symlink_to('source-missing.yaml')
    r=subprocess.run(['python3',str(ROOT/'ops/bien_nhan_v2.py'),'--root',str(p)],capture_output=True,text=True)
    out('unreadable-receipt-CLI',rc=r.returncode,stdout=r.stdout,stderr=r.stderr[-800:])
   try:result(name,p,al)
   finally:
    b._git=oldgit;b._bam=oldbam


def acceptance():
 old=t._kho_surface
 def watch(tmp,*args,**kw):
  al=old(tmp,*args,**kw)
  r=subprocess.run(['git','-C',str(tmp),'rev-parse','--verify','HEAD'],capture_output=True,text=True)
  tree=subprocess.run(['git','-C',str(tmp),'ls-tree','-r','--name-only','HEAD','--','ops/reviews'],capture_output=True,text=True)
  out('A4-fixture-git',git_rc=r.returncode,head=r.stdout.strip(),files=tree.stdout.splitlines())
  return al
 t._kho_surface=watch
 fn=next(f for f in t.CA if f.__name__.startswith('c73_'));out('A4-case',result=t._chay_1(fn))
 for i in range(2):
  with tempfile.TemporaryDirectory() as td:
   k=t._kho_cau(Path(td));out('fixture-dates',iteration=i,B0=k['B0'],X=k['X'],M=k['M'])

def debt_surface_context():
 be_mat=frozenset().union(*(v['be_mat'] for v in b.PROVIDER_HOP_DONG.values()))
 for file,field,law in sorted(b.NO_CAU_LICH_SU):
  if law!=b.LUAT_SURFACE:continue
  d=yaml.safe_load((ROOT/b.THU_MUC/file).read_text());lines=(ROOT/d['verdict_path']).read_text().splitlines();run=json.loads((ROOT/d['model_reviewer_identity']['run_json']).read_text())
  matches=[]
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);fixture,_=t._bn_surface('ops/reviews/v/run.json','');t._kho_surface(p,fixture,json.dumps({'execution_surface':run['execution_surface']}),'x\n')
   for i,line in enumerate(lines,1):
    if not b._RE_DONG_SURFACE.search(line):continue
    (p/'ops/reviews/v.md').write_text(line+'\n')
    mismatch=b._surface_cua_verdict(p,fixture,run['execution_surface'],be_mat)
    if mismatch:matches.append({'line':i,'text':line,'mismatch':sorted(mismatch)})
  out('debt-surface-matches',receipt=file,run_surface=run['execution_surface'],verdict=d['verdict_path'],matches=matches)
 # Ca c73 chỉ đổi verdict thành câu TRÍCH lời của verdict khác, không có trích dẫn tệp:N cùng dòng.
 for name,text in [
  ('finding-prose','VAN DE: Verdict #khac tu khai `execution surface codex_service`. Run cua no ghi codex_cli.\n'),
  ('previous-line-path','ops/land/khac/verdict.md:6\nSELF: execution_surface: codex_service\n')]:
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);d,_=t._bn_surface('ops/reviews/v/run.json','');al=t._kho_surface(p,d,json.dumps({'execution_surface':'codex_cli'}),text);result('quoted-other-'+name,p,al)
