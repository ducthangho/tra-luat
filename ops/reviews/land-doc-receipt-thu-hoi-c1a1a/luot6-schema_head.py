# Same F36 schema_control.py measurement, directly on HEAD as instructed: no stale patch anchor.
import audit as A
import json
T=A.T; orig=T._CON_TINH
row=('R6','benign comment','comment',T._DAU,T._DAU+'  # harmless','tinh',None)
reports=[('valid',None),('bad_ev',{'ev':None,'trang_thai':True,'tat_dinh':True}),('bad_bool',{'ev':[],'trang_thai':1,'tat_dinh':1}),('ev_int',{'ev':[1],'trang_thai':True,'tat_dinh':True}),('false_state',{'ev':[],'trang_thai':False,'tat_dinh':True}),('false_determinism',{'ev':[],'trang_thai':True,'tat_dinh':False}),('event',{'ev':['open'],'trang_thai':True,'tat_dinh':True})]
try:
 for case,report in reports:
  T._CON_TINH=orig+('' if report is None else '\nprint('+repr(json.dumps(report))+')\n')
  try:T.ca_tinh('tinh',A.M);oracle='pass'
  except Exception as e:oracle=type(e).__name__+': '+str(e)
  A.emit(case=case,oracle=oracle,disposition=T.chay_dot_bien(A.SRC,row))
finally:T._CON_TINH=orig
for ident in ('M1s6','M1s7','M1s8','M1s9'):
 r=next(r for r in T.DB if r[0]==ident);A.emit(id=ident,disposition=T.chay_dot_bien(A.SRC,r))
