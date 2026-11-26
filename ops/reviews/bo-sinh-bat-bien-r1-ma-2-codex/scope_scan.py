from pathlib import Path
import importlib.util,json,os
from unittest import mock
w=Path(__file__).resolve().parent;r=w/'head';os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
def load(p,n,s=None):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp)
 if s is None:sp.loader.exec_module(m)
 else:exec(compile(s,str(p),'exec'),m.__dict__)
 return m
A=r/'ops/gate_output_doi_chieu_test.py';B=r/'ops/land_evidence_nguon_test.py';src=A.read_text();bsrc=B.read_text()
cu='    kiem(dau + " [khong khop]" + duoi, ten_goc + " [khong khop]")\n';assert src.count(cu)==1
rows=[]
for label,moi in [('rename-marker','    kiem(dau + " [khac]" + duoi, ten_goc + " [khac]")\n'),('unique-trailing-space','    kiem(dong + " ", ten_goc)\n'),('R1-02-exact-duplicate','    kiem(dong, ten_goc)\n')]:
 a=load(A,'a_'+label,src.replace(cu,moi));b=load(B,'b_'+label);old=b.nap_a
 ra=a.chay_ca('a129_ten_job_lazy_qua_ho_so')
 with mock.patch.dict(b.__dict__,{'nap_a':lambda t:a if t==A.name else old(t),'A_CA':{'a129':b.A_CA['a129']}}):out=b.chay_ca('c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a')
 rows.append(dict(label=label,cu=cu,moi=moi,A_rc=ra[0],A_output=ra[1],B_rc=out[0],B_output=out[1]))
 print(rows[-1],flush=True)
(w/'scope-scan.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
# Guards for the newly added fingerprint must measure both components and reset by case.
mutants=[('ignore-provenance','van_tay.add((byte, *tep))','van_tay.add((byte,))','a125'),('ignore-profile','van_tay.add((byte, *tep))','van_tay.add(tuple(tep))','a124'),('no-reset','        van_tay.clear()\n','',None)]
more=[]
for label,cu,moi,prefix in mutants:
 assert bsrc.count(cu)==1
 b=load(B,'b_'+label,bsrc.replace(cu,moi))
 if prefix:b.A_CA={prefix:b.A_CA[prefix]}
 else:b.A_CA={k:b.A_CA[k] for k in ['a124','a125']}
 out=b.chay_ca('c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a');more.append(dict(label=label,rc=out[0],output=out[1]))
 print(more[-1],flush=True)
(w/'fingerprint-scan.json').write_text(json.dumps(more,ensure_ascii=False,indent=2))
