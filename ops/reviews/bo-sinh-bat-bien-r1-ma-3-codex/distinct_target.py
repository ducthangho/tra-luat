from pathlib import Path
import importlib.util,json,os
from unittest import mock
w=Path(__file__).resolve().parent;r=w/'head';os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'));A=r/'ops/gate_output_doi_chieu_test.py';B=r/'ops/land_evidence_nguon_test.py';src=B.read_text();asrc=A.read_text();guard='bang(len(van_tay) == mong - lap,';assert src.count(guard)==1
rows=[]
def load(p,n,s):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);exec(compile(s,str(p),'exec'),m.__dict__);return m
for tt,cu,moi in [('a126','        do(URL, DONG.replace("ubuntu-latest", "ubuntu-latest,win7"), [])\n','        do(URL, DONG, [])\n'),('a129','    kiem(dau + " [khong khop]" + duoi, ten_goc + " [khong khop]")\n','    kiem(dong, ten_goc)\n')]:
 assert asrc.count(cu)==1
 for label,s in [('guard-present',src),('guard-removed',src.replace(guard,'bang(True,'))]:
  b=load(B,'b',s);a=load(A,'a',asrc.replace(cu,moi));old=b.nap_a
  with mock.patch.dict(b.__dict__,{'A_CA':{tt:b.A_CA[tt]},'nap_a':lambda n:a if n==A.name else old(n)}):out=b.chay_ca('c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a')
  rows.append(dict(case=tt,guard=label,rc=out[0],output=out[1]));print(rows[-1],flush=True)
(w/'distinct-target.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
