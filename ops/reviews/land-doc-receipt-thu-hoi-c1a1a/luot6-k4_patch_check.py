import audit as A
import pathlib,tempfile
T=A.T
old='[f"{k} stale, chay lai" for k, v in (("S", base_hien_hanh), ("H", head_hien_hanh)) if v != r[k]]'
changes={
 'r5_english':'[f"{k}: receipt stale, rerun" for k, v in (("S", base_hien_hanh), ("H", head_hien_hanh)) if v != r[k]]',
 'vietnamese_with_colon':'[f"{k}: receipt stale, chạy lại" for k, v in (("S", base_hien_hanh), ("H", head_hien_hanh)) if v != r[k]]',
 'extra_unspaced_contradiction':old+' + (["S fresh, khong can chay lai"] if base_hien_hanh != r["S"] else [])',
 'missing': '[]',
}
for name,new in changes.items():
 with tempfile.TemporaryDirectory() as td:
  p=pathlib.Path(td)/'m.py';p.write_text(A.edit(old,new));m=A.load(p,name)
  if name=='extra_unspaced_contradiction':
   # Keep valid field reason, plus contradictory K4 line without the exact filter spacing.
   src=p.read_text().replace('    ghi("K5",','    ly_do += ["K4:S fresh, khong can chay lai"] if base_hien_hanh != r["S"] else []\n    ghi("K5",')
   # Remove the ordinary extra reason so this isolates the startswith filter.
   src=src.replace(' + (["S fresh, khong can chay lai"] if base_hien_hanh != r["S"] else [])','')
   p.write_text(src);m=A.load(p,name+'_actual')
  A.emit(name=name,raw=m.kiem_json(T.ma(T.FIX),kho=T.KHO,nhanh='master',base_hien_hanh=T.X40,head_hien_hanh=T.X40),controls={c:A.target(m,p,c) for c in ('duong_fixture','k4_base','k4_head','k4_ca_hai','a11_k3_k4','kieu_S','kieu_H')})
# Restore only the RHS sort bug Executor reported, on copied test text.
source=(A.DEV/'doc_receipt_thu_hoi_test.py').read_text();rhs='sorted(k for k in ("S", "H") if r[k] != t[k])';assert source.count(rhs)==1
with tempfile.TemporaryDirectory() as td:
 p=pathlib.Path(td)/'test.py';p.write_text(source.replace(rhs,'[k for k in ("S", "H") if r[k] != t[k]]'));U=A.load(p,'rhs_unsorted')
 for name in ('k4_base','k4_head','k4_ca_hai'):
  c=next(c for c in U.CA if c[0]==name)
  try:U.ca(A.M,*c[:3],**(c[3] if len(c)>3 else {}));res='pass'
  except Exception as e:res=type(e).__name__+': '+str(e)
  A.emit(name='rhs_unsorted_control',case=name,result=res)
