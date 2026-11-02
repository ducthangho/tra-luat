import subprocess,os,json,sys,importlib.util
from pathlib import Path
K=Path('/home/user/rv773'); O=Path(__file__).resolve().parent; SP=O.parent.parent
src=(K/'ops/land_evidence_nguon.py').read_text()
fix=Path('/tmp/rv773-r4-root-resolved.py');fix.write_text(src.replace('goc = Path(a.root)','goc = Path(a.root).resolve()'))
rows=[]
for v in ['3.11','3.12','3.13','3.14']:
 for ma in [K/'ops/land_evidence_nguon.py',fix]:
  cmd=['python'+v,'-B',str(O/'regression.py')]
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(SP/('yaml-python'+v)),LAND_EVIDENCE_NGUON_MA=str(ma))
  r=subprocess.run(cmd,capture_output=True,text=True,env=env)
  rows.append(dict(cmd=cmd,ma=str(ma),rc=r.returncode,output=r.stdout+r.stderr))
# Independent renamed-cutover mutation.
mut=Path('/tmp/rv773-r4-rename.py'); mut.write_text(src.replace('plat-x8-land-evidence.yaml','plat-x9-land-evidence.yaml'))
ca='c10_l5_danh_sach_dong_bang'
r=subprocess.run([sys.executable,'-B',str(K/'ops/land_evidence_nguon_test.py'),'--mot-ca',ca],env=dict(os.environ,LAND_EVIDENCE_NGUON_MA=str(mut)),capture_output=True,text=True)
rows.append(dict(label='rename-cutover',rc=r.returncode,output=r.stdout+r.stderr))
# Current guard with no targeted official mutation: conflicting merged_at for generic filenames.
old='if len(gia_tri) > 1:';assert src.count(old)==1
mut=Path('/tmp/rv773-r4-conflict-off.py');mut.write_text(src.replace(old,'if False:'))
s=importlib.util.spec_from_file_location('t',K/'ops/land_evidence_nguon_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
for ca in t.CA:
 r=subprocess.run([sys.executable,'-B',str(K/'ops/land_evidence_nguon_test.py'),'--mot-ca',ca],env=dict(os.environ,LAND_EVIDENCE_NGUON_MA=str(mut)),capture_output=True,text=True)
 rows.append(dict(label='conflict-guard '+ca,rc=r.returncode,output=r.stdout+r.stderr))
(O/'extra.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
for r in rows: print(r)
