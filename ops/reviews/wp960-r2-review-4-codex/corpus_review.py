import types,subprocess,yaml
import replay_probe_recheck as h
b=h.b;root=h.ROOT/'cay-kho'
src=subprocess.check_output(['git','-C',str(root),'show','934a5b063670acfbed410487d8244cd17d586d6e:ops/bien_nhan_v2.py'],text=True)
old=types.ModuleType('previous');old.__file__=str(h.COPY/'ops/bien_nhan_v2.py');exec(compile(src,old.__file__,'exec'),old.__dict__)
receipts={};tokens=[]
for p in sorted((root/b.THU_MUC).glob('*.receipt.yaml')):
 s=p.read_text();d=yaml.safe_load(s);receipts[p.name]=(d,s)
 for path,node,_ in b._duyet_scalar(yaml.compose(s,Loader=yaml.SafeLoader)):
  for sentence in b._cac_cau(node.value):
   if b._RE_ANCESTRY.search(b._bo_dau(sentence)):tokens.extend(m.group(0) for m in b._RE_OID.finditer(sentence))
def resolve(mod,x):
 try:return mod._commit_cua(root,x)
 except Exception as ex:return type(ex).__name__+':'+str(ex)
rows=[dict(token=x,old=resolve(old,x),new=resolve(b,x)) for x in sorted(set(tokens))];h.log(appearances=len(tokens),distinct=len(rows),changes=[r for r in rows if r['old']!=r['new']])
vp,chua,sf=b._kiem_cau_lich_su(root,receipts);h.log(receipts=len(receipts),violation_keys=len(vp),debt_keys=len(b.NO_CAU_LICH_SU),equal_debt=set(vp)==set(b.NO_CAU_LICH_SU),unknown=chua,surface_not_applied=sf)
loi,tk=b.kiem(root,no_cau_lich_su=frozenset());h.log(empty_debt_rc=b._ma_thoat(loi,tk),law_errors=sum(s.startswith('[L-') for s in loi),other_errors=sum(not s.startswith('[L-') for s in loi),unknown=tk['chua_do'])
