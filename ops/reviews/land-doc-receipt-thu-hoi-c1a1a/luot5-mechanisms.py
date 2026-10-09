import audit as A
import json,pathlib,tempfile,contextlib,io
T=A.T
# K4: every existing red path, plus both mismatches and K2+K4 cases.
k4=[c for c in T.CA if 'K4' in c[2] and 'K1' not in c[2]]
for c in k4:
 A.emit(kind='k4_existing',name=c[0],laws=c[2],baseline=A.target(A.M,A.DEV/'doc_receipt_thu_hoi.py',c[0]))
for label,changes,do,params in [
 ('both',{'S':T.X40,'H':T.X40},('K4',),{}),
 ('wrong_type_S',{'S':[]},('K2','K4'),{}),('wrong_type_H',{'H':{}},('K2','K4'),{}),
 ('wrong_type_both',{'S':None,'H':False},('K2','K4'),{}),
 ('fresh_different',{'S':T.X40,'H':T.X40},(),{'base_hien_hanh':T.X40,'head_hien_hanh':T.X40})]:
 try:T.ca(A.M,label,T.doi(**changes),do,**params);v='pass'
 except Exception as e:v=type(e).__name__+': '+str(e)
 A.emit(kind='k4_added_control',name=label,result=v)
# Alternative wording/order: spec M5 prescribes meaning, not a literal ASCII serialization.
old='[f"{k} stale, chay lai" for k, v in (("S", base_hien_hanh), ("H", head_hien_hanh)) if v != r[k]]'
variants={
 'stale_english':'[f"{k}: receipt stale, rerun" for k, v in (("S", base_hien_hanh), ("H", head_hien_hanh)) if v != r[k]]',
 'reverse_order':'[f"{k} stale, chay lai" for k, v in (("H", head_hien_hanh), ("S", base_hien_hanh)) if v != r[k]]',
 'missing':'[]',
 'type_wrong_fresh':'[f"{k} fresh, khong can chay lai" if luat["K2"] == "do" else f"{k} stale, chay lai" for k, v in (("S", base_hien_hanh), ("H", head_hien_hanh)) if v != r[k]]',
}
for label,new in variants.items():
 with tempfile.TemporaryDirectory() as td:
  p=pathlib.Path(td)/'m.py';p.write_text(A.edit(old,new));m=A.load(p,label)
  targets={c[0]:A.target(m,p,c[0]) for c in k4}
  try:T.ca(m,'both',T.doi(S=T.X40,H=T.X40),('K4',));both='pass'
  except Exception as e:both=type(e).__name__+': '+str(e)
  A.emit(kind='k4_mutant',name=label,targets=targets,both=both)
# F31 additional structure checks, single/tuple positive controls.
r=next(r for r in T.DB if r[0]=='M1s7')
for label,cu,moi in [('valid',r[3],r[4]),('tuple_str',r[3],r[4][0]),('str_tuple',r[3][0],r[4]),('list',list(r[3]),list(r[4])),('none',(r[3][0],None),r[4]),('int',r[3],(r[4][0],3))]:
 A.emit(kind='tuple_shape',name=label,disposition=T.chay_dot_bien(A.SRC,(*r[:3],cu,moi,*r[5:])))
# Actual child processes: malformed telemetry vs valid false property.
old_code=T._CON_TINH
real_run=T.subprocess.run; records=[]
def record(*args,**kwargs):
 r=real_run(*args,**kwargs);records.append({'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr});return r
T.subprocess.run=record
benign=('R5','control without side effects','benign_comment',T._DAU,T._DAU+'  # harmless review control','tinh',None)
try:
 for label,report in [('valid',None),('ev_wrong_type',{'ev':None,'trang_thai':True,'tat_dinh':True}),('boolean_as_int',{'ev':[],'trang_thai':1,'tat_dinh':1}),('false_state',{'ev':[],'trang_thai':False,'tat_dinh':True}),('missing_key',{'ev':[],'trang_thai':True}),('not_dict',[]),('bad_json','NOT_JSON')]:
  suffix='' if report is None else '\nprint('+repr(report if report=='NOT_JSON' else json.dumps(report))+')\n'
  T._CON_TINH=old_code+suffix
  target=A.target(A.M,A.DEV/'doc_receipt_thu_hoi.py','tinh');child=records[-1]
  A.emit(kind='purity_schema',name=label,baseline=target,disposition=T.chay_dot_bien(A.SRC,benign),child=child)
finally:T._CON_TINH=old_code;T.subprocess.run=real_run
