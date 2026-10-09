import audit as A
import pathlib,tempfile,json
T=A.T
src=(A.DEV/'doc_receipt_thu_hoi_test.py').read_text()
old='or set(kq) != {"ev", "trang_thai", "tat_dinh"}:'
new='or set(kq) != {"ev", "trang_thai", "tat_dinh"} or type(kq["ev"]) is not list or any(type(e) is not str for e in kq["ev"]) or type(kq["trang_thai"]) is not bool or type(kq["tat_dinh"]) is not bool:'
assert src.count(old)==1
# Test-only scratch counterfactual. No source checkout write.
p=A.OUT/'schema_control_test.py';p.write_text(src.replace(old,new))
U=A.load(p,'schema_control');U.GOC=A.DEV;U.MODUN=A.DEV/'doc_receipt_thu_hoi.py'
for t,label in ((T,'head'),(U,'counterfactual')):
 original=t._CON_TINH
 try:
  for case,report in [('valid',None),('bad_ev',{'ev':None,'trang_thai':True,'tat_dinh':True}),('bad_bool',{'ev':[],'trang_thai':1,'tat_dinh':1})]:
   t._CON_TINH=original+('' if report is None else '\nprint('+repr(json.dumps(report))+')\n')
   try:t.ca_tinh('tinh',A.M);oracle='pass'
   except Exception as e:oracle=type(e).__name__+': '+str(e)
   row=('R5','benign comment','comment',t._DAU,t._DAU+'  # harmless','tinh',None)
   A.emit(version=label,case=case,oracle=oracle,disposition=t.chay_dot_bien(A.SRC,row))
 finally:t._CON_TINH=original
 if t is U:
  for ident in ('M1s6','M1s7','M1s8','M1s9'):
   row=next(r for r in t.DB if r[0]==ident);A.emit(version=label,id=ident,disposition=t.chay_dot_bien(A.SRC,row))
