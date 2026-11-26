from pathlib import Path
import importlib.util,json,subprocess,sys
from unittest.mock import patch
w=Path(__file__).resolve().parent;r=w/'tool-copy';p=r/'ops/land_evidence_nguon_test.py';src=p.read_text();rows=[]
def load(path,s,n):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);exec(compile(s,str(path),'exec'),m.__dict__);return m
b=load(p,src.replace('if tru is not None:','if True:'),'b_branch')
with patch.dict(b.__dict__,{'A_CA':{'a131':b.A_CA['a131']}}):out=b.chay_ca('c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a')
rows.append(dict(probe='branch-always-true-a131',rc=out[0],output=out[1]));print(rows[-1],flush=True)
out=b.chay_ca('c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o');rows.append(dict(probe='branch-always-true-c40',rc=out[0],output=out[1]));print(rows[-1],flush=True)
spec=importlib.util.spec_from_file_location('table',w/'bang_toan_tu.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
old='bang((rc, dong) == ((0, "") if dau is None else (3, f"DO:{c36}:{dau}")),';assert src.count(old)==1
try:
 p.write_text(src.replace(old,'bang(True,'))
 out=t.mot(r,t.B,t.C40,'bang(not thieu,','bang(True,');rows.append(dict(probe='dev-table-with-c40-own-assert-removed',**out));print(rows[-1],flush=True)
finally:p.write_text(src)
(w/'exclusions-probe.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
