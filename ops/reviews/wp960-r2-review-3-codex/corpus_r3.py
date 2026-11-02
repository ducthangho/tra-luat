import importlib.util,json,os,subprocess,time,types
from pathlib import Path
import yaml
import probe_r3 as h
ROOT=h.ROOT/'cay-kho'; b=h.b
src=subprocess.run(['git','-C',str(ROOT),'show','ae0d06c23fb777545fd7547a07d9f368e4122f49:ops/bien_nhan_v2.py'],capture_output=True,text=True,check=True).stdout
old=types.ModuleType('old_gate');old.__file__=str(h.COPY/'ops/bien_nhan_v2.py');exec(compile(src,old.__file__,'exec'),old.__dict__)
tokens=[];receipts={}
for p in sorted((ROOT/b.THU_MUC).glob('*.receipt.yaml')):
 s=p.read_text();d=yaml.safe_load(s);receipts[p.name]=(d,s)
 if not isinstance(d,dict):continue
 for path,node,_ in b._duyet_scalar(yaml.compose(s,Loader=yaml.SafeLoader)):
  for sentence in b._cac_cau(node.value):
   if b._RE_ANCESTRY.search(b._bo_dau(sentence)):
    tokens.extend((p.name,path,mo.group(0)) for mo in b._RE_OID.finditer(sentence))
def result(mod,tok):
 try:return mod._commit_cua(ROOT,tok)
 except Exception as ex:return type(ex).__name__+':'+str(ex)
rows=[{'token':x,'old':result(old,x),'new':result(b,x)} for x in sorted({x for _,_,x in tokens})]
h.log(appearances=len(tokens),distinct=len(rows),changes=[r for r in rows if r['old']!=r['new']],rows=rows)
# Surface/corpus facts, calculated without trusting debt count output.
vp,chua,sf=b._kiem_cau_lich_su(ROOT,receipts)
h.log(receipts=len(receipts),historical_keys=len(vp),debt_keys=len(b.NO_CAU_LICH_SU),equal_debt=set(vp)==set(b.NO_CAU_LICH_SU),unknown=chua,surface_not_applied=sf)
with_debt=b.kiem(ROOT);empty=b.kiem(ROOT,no_cau_lich_su=frozenset())
h.log(with_debt_rc=b._ma_thoat(*with_debt),empty_rc=b._ma_thoat(*empty),empty_law_errors=sum(s.startswith('[L-') for s in empty[0]),empty_other_errors=sum(not s.startswith('[L-') for s in empty[0]),empty_unknown=empty[1]['chua_do'])
real=subprocess.run
for i in range(3):
 for name,mod in [('old',old),('head',b)] if i%2==0 else [('head',b),('old',old)]:
  calls=[0]
  def run(*a,**kw):
   if a and isinstance(a[0],list) and a[0] and a[0][0]=='git':calls[0]+=1
   return real(*a,**kw)
  subprocess.run=run;start=time.perf_counter()
  try:loi,tk=mod.kiem(ROOT)
  finally:subprocess.run=real
  h.log(benchmark=name,iteration=i+1,seconds=round(time.perf_counter()-start,4),git_calls=calls[0],rc=mod._ma_thoat(loi,tk),unknown=len(tk['chua_do']))
