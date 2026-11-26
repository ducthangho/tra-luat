from pathlib import Path
import importlib.util,json,os
from unittest import mock
w=Path(__file__).resolve().parent;r=w/'head';os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
A=r/'ops/gate_output_doi_chieu_test.py';B=r/'ops/land_evidence_nguon_test.py'
src=B.read_text();a_src=A.read_text()
cu='bang(rc == 0 and dem[0] - truoc == mong,';moi='bang(rc == 0 and dem[0] - truoc >= mong,';assert src.count(cu)==1
extra='    kiem(dong, ten_goc)\n';assert a_src.count(extra)==1
rows=[]
def load(p,n,s):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);exec(compile(s,str(p),'exec'),m.__dict__);return m
for label,s in [('exact',src),('floor-mutant',src.replace(cu,moi))]:
 b=load(B,'b_'+label,s)
 for typ in ['c40','extra-duplicate-a129','intact-a129']:
  if typ=='c40':out=b.chay_ca('c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o')
  else:
   a=load(A,'a_'+label,a_src.replace(extra,extra*2) if typ.startswith('extra') else a_src);old=b.nap_a
   with mock.patch.dict(b.__dict__,{'nap_a':lambda t:a if t==A.name else old(t),'A_CA':{'a129':b.A_CA['a129']}}):out=b.chay_ca('c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a')
  rows.append(dict(guard=label,probe=typ,rc=out[0],output=out[1]));print(rows[-1],flush=True)
(w/'excess-probe.json').write_text(json.dumps({'guard_mutation':{'path':'ops/land_evidence_nguon_test.py','cu':cu,'moi':moi},'witness':{'path':'ops/gate_output_doi_chieu_test.py','cu':extra,'moi':extra*2},'rows':rows},ensure_ascii=False,indent=2))
