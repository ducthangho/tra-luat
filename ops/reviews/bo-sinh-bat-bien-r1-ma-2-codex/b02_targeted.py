from pathlib import Path
import importlib.util,json,os
from unittest import mock
w=Path(__file__).resolve().parent;r=w/'head';os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
def load(p,n,src=None):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s)
 if src is None:s.loader.exec_module(m)
 else:exec(compile(src,str(p),'exec'),m.__dict__)
 return m
rows=[]
for mut in json.loads((w.parent/'lich_su/wp1236-b-luot4-outside-mutants.json').read_text()):
 p=r/mut['target'];src=p.read_text();assert src.count(mut['raw_cu'])==1
 a=load(p,'a_mut',src.replace(mut['raw_cu'],mut['raw_moi']));b=load(r/'ops/land_evidence_nguon_test.py','b');old=b.nap_a
 for name in ['c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a']+(['c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong'] if mut['id']=='omit-category-Mn' else []):
  with mock.patch.dict(b.__dict__,{'nap_a':lambda t:a if t=='gate_output_doi_chieu_test.py' else old(t)}):out=b.chay_ca(name)
  rows.append(dict(mutant=mut['id'],case=name,rc=out[0],output=out[1]));print(rows[-1],flush=True)
(w/'b02-targeted.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
