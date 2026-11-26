from pathlib import Path
import importlib.util,json,os,sys,hashlib
from unittest import mock
w=Path(__file__).resolve().parent;r=w/'head'
os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
def load(p,n,src=None):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp)
 if src is None:sp.loader.exec_module(m)
 else:exec(compile(src,str(p),'exec'),m.__dict__)
 return m
b=load(r/'ops/land_evidence_nguon_test.py','b');a=load(r/'ops/gate_output_doi_chieu_test.py','a')
rows=[];loops=[];outer=''
def profile(frame,event,arg):
 if event=='c_call' and getattr(arg,'__name__','')=='append' and frame.f_code.co_name=='<lambda>' and 'o' in frame.f_code.co_freevars and loops:
  loops[-1]['actual_counter_calls']+=1
 if event=='return' and frame.f_code.co_name=='chay_ca':
  rows.append(dict(outer=outer,case=frame.f_locals.get('ten'),rc=arg[0],output=arg[1],file=frame.f_code.co_filename))
line=next(i for i,s in enumerate((r/'ops/land_evidence_nguon_test.py').read_text().splitlines(),1) if 'ky8(json.dumps({"gate_output": f"measured — {ten}"})' in s)
def trace(frame,event,arg):
 if frame.f_code.co_name=='c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong':
  if event=='call':loops.append({'iterations':0,'actual_counter_calls':0})
  if event=='line' and frame.f_lineno==line:loops[-1]['iterations']+=1
 return trace
for m,c in [(b,'c39_c37_do_khi_bo_sinh_lech_mien'),(b,'c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o'),(a,'a136_a135_do_khi_bo_sinh_lech_mien'),(b,'c38_c36_do_khi_bang_cua_dot_a_mat_ca')]:
 outer=c;sys.setprofile(profile)
 if c.startswith('c39'):sys.settrace(trace)
 out=m.chay_ca(c);sys.settrace(None);sys.setprofile(None)
 print(c,out,flush=True)
(w/'trace-v2.json').write_text(json.dumps({'calls':rows,'c39_loops':loops},ensure_ascii=False,indent=2))
# In-memory exact control has same code/constants/globals except import metadata; compare code by marshal.
import marshal
needle='("nhan", "", dung),'
same=b.nap_sua('land_evidence_nguon_test.py',needle,needle)
mut=b.nap_sua('land_evidence_nguon_test.py',needle,'')
eq={n:marshal.dumps(b.CA[n].__code__)==marshal.dumps(same.CA[n].__code__) for n in b.CA}
checks={'same_case_inventory':list(b.CA)==list(same.CA),'all_case_code_equal':all(eq.values()),'case_code_equal':eq,'same_A_CA':b.A_CA==same.A_CA,'same_LOAI':b.LOAI==same.LOAI,'same_paths':all(getattr(b,k)==getattr(same,k) for k in ['HERE','ROOT_THAT','MA']),'mutation_changes_c37_code':marshal.dumps(b.CA['c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong'].__code__)!=marshal.dumps(mut.CA['c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong'].__code__)}
for label,needle in [('absent','NEEDLE_REVIEW_ABSENT'),('multiple','import ')]:
 try:b.nap_sua('land_evidence_nguon_test.py',needle,'');res='unexpected pass'
 except b.TinHieuChotCa as e:res=str(e)
 checks[label]=res
(w/'nap-sua.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
print('nap_sua',checks,flush=True)
