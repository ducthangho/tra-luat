from pathlib import Path
import importlib.util,json,os
from unittest import mock
w=Path(__file__).resolve().parent;r=w/'head';os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
p=r/'ops/land_evidence_nguon_test.py';src=p.read_text();name='c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong'
def load(s):
 sp=importlib.util.spec_from_file_location('b',p);m=importlib.util.module_from_spec(sp);exec(compile(s,str(p),'exec'),m.__dict__);return m
needle='("nhan", "", dung),';assert src.count(needle)==1
rows=[]
for label,s in [('original',src),('missing-cell',src.replace(needle,'')),('missing-cell-no-648',src.replace(needle,'').replace('bang(len(o) == 648,','bang(True,'))]:
 m=load(s);calls=[0];old=m.ky8
 def spy(*a,**k):calls[0]+=1;return old(*a,**k)
 m.ky8=spy;out=m.chay_ca(name);rows.append(dict(label=label,rc=out[0],output=out[1],actual_cells=calls[0]));print(rows[-1],flush=True)
for label,s in [('duplicate-extra-nonBMP',src),('duplicate-extra-no-total',src.replace('bang(len(vu_tru) == 158 and len(set(vu_tru)) == 158 and not lech,','bang(len(set(vu_tru)) == 158 and not lech,'))]:
 m=load(s);a=m.nap_a('gate_output_doi_chieu_test.py');old=a._mau_loai_unicode
 a._mau_loai_unicode=lambda *x:(*old(*x),old(*x)[-1])
 with mock.patch.dict(m.__dict__,{'nap_a':lambda _:a}):out=m.chay_ca(name)
 rows.append(dict(label=label,rc=out[0],output=out[1]));print(rows[-1],flush=True)
(w/'guard-witnesses.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
