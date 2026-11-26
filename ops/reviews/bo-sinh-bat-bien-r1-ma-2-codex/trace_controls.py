import importlib.util,sys,json,os,copy
from pathlib import Path
from unittest import mock
w=Path(__file__).resolve().parent;r=w/'head'
os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
b=load(r/'ops/land_evidence_nguon_test.py','b');a=load(r/'ops/gate_output_doi_chieu_test.py','a')
rows=[]
def record(m):
 old=m.chay_ca
 def go(ten):
  out=old(ten);rows.append({'case':ten,'rc':out[0],'output':out[1]});return out
 m.chay_ca=go
record(b);record(a)
# Observe execution of the cell loop in c39's patched c37 without changing its result.
loops=[]
def trace(frame,event,arg):
 if frame.f_code.co_name=='c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong':
  if event=='call':loops.append({'iterations':0})
  if event=='line' and frame.f_lineno==905:loops[-1]['iterations']+=1
 return trace
sys.settrace(trace);b.chay_ca('c39_c37_do_khi_bo_sinh_lech_mien');sys.settrace(None)
b.chay_ca('c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o')
a.chay_ca('a136_a135_do_khi_bo_sinh_lech_mien')
# Supplement the absent positive a129 control, both plain and same deepcopy cache as c40.
import yaml
for cached in [False,True]:
 aa=b.nap_a('gate_output_doi_chieu_test.py');oldnap=b.nap_a
 if cached:
  cache={}
  aa.yaml=mock.Mock(spec=['safe_load','safe_dump'],safe_load=lambda x:copy.deepcopy(cache.get(x) or cache.setdefault(x,yaml.safe_load(x))),safe_dump=yaml.safe_dump)
 with mock.patch.dict(b.__dict__,{'nap_a':lambda t:aa if t=='gate_output_doi_chieu_test.py' else oldnap(t),'A_CA':{'a129':b.A_CA['a129']}}):
  out=b.chay_ca('c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a')
 rows.append({'positive_a129_cached':cached,'rc':out[0],'output':out[1]})
(w/'controls.json').write_text(json.dumps({'calls':rows,'c39_loop_observation':loops},ensure_ascii=False,indent=2))
print(json.dumps({'calls':len(rows),'nonzero':sum(x['rc']!=0 for x in rows),'c39_loop_observation':loops,'a129_controls':rows[-4:]},ensure_ascii=False))
