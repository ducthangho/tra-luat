"""Đối chứng cho F41: chỉ bản sao test ngoài checkout; không phải patch sản phẩm."""
import audit as A
import pathlib,tempfile
T=A.T
source=(A.DEV/'doc_receipt_thu_hoi_test.py').read_text()
old='x) for x in kq["ly_do"] if re.match(r"K4\\b", x)'
new='x.lstrip(" \\t")) for x in kq["ly_do"] if re.match(r"K4\\b", x.lstrip(" \\t"))'
assert source.count(old)==1
with tempfile.TemporaryDirectory() as td:
 p=pathlib.Path(td)/'test.py';p.write_text(source.replace(old,new));U=A.load(p,'normalized_label')
 for prefix in ('',' ','\t'):
  for bad in (False,True):
   anchor='    ghi("K5",'
   if bad: insert='    ly_do += ['+repr(prefix+'K4:S fresh, khong can chay lai')+'] if base_hien_hanh != r["S"] else []\n'
   else:insert='    ly_do[:] = [('+repr(prefix)+' + x) if x.startswith("K4:") else x for x in ly_do]\n'
   mpath=pathlib.Path(td)/'m.py';mpath.write_text(A.edit(anchor,insert+anchor));m=A.load(mpath,'control')
   result={}
   for label,test in [('HEAD',T),('normalized_copy',U)]:
    result[label]={}
    for case in ('duong_fixture','k4_base','k4_ca_hai','a11_k3_k4'):
     try:test.chay_ca(m,mpath,{case});res='pass'
     except Exception as e:res=type(e).__name__+': '+str(e)
     result[label][case]=res
   A.emit(prefix=repr(prefix),bad=bad,results=result)
   assert result['normalized_copy']['duong_fixture']=='pass'
   for c in ('k4_base','k4_ca_hai','a11_k3_k4'):
    assert (result['normalized_copy'][c].startswith('TinHieuChotCa:')) if bad else result['normalized_copy'][c]=='pass'
