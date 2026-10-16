import audit as A
import json,sys,time,statistics,tempfile,pathlib
T=A.T
A.emit(kind='environment',version=sys.version,exe=sys.executable,int_max_str_digits=sys.get_int_max_str_digits(),recursionlimit=sys.getrecursionlimit())
for depth in (1000,5000,10000,100000):
 raw=b'['*depth+b']'*depth
 durations=[]; outcomes=[]
 for i in range(20):
  st=time.perf_counter()
  try:json.loads(raw); outcome='parsed'
  except Exception as e: outcome=type(e).__name__+': '+str(e)
  durations.append(time.perf_counter()-st);outcomes.append(outcome)
 A.emit(kind='parser_depth',depth=depth,repeats=20,median_ms=1000*statistics.median(durations),max_ms=1000*max(durations),outcomes=sorted(set(outcomes)))
for ident in ('M2b3','M2c3','M2d',"M2e'",'M6d','M2j','M2k'):
 row=next(r for r in T.DB if r[0]==ident)
 with tempfile.TemporaryDirectory() as d:
  p=pathlib.Path(d)/'m.py';p.write_text(A.edit(row[3],row[4]));m=A.load(p,'ver_mutant')
  st=time.perf_counter();disp=T.chay_dot_bien(A.SRC,row)
  A.emit(kind='exception_identity',id=ident,disposition=disp,elapsed=time.perf_counter()-st,baseline=A.target(A.M,A.DEV/'doc_receipt_thu_hoi.py',row[5]),guard=A.target(m,p,'duong_fixture'),target=A.target(m,p,row[5]))
