import importlib.util, subprocess, sys, os, json
from pathlib import Path
K=Path('/home/user/rv773')
s=importlib.util.spec_from_file_location('t',K/'ops/land_evidence_nguon_test.py'); t=importlib.util.module_from_spec(s); s.loader.exec_module(t)
rows=[]
def run(label,args,**kw):
 r=subprocess.run(args,capture_output=True,text=True,**kw); rows.append(dict(label=label,args=args,rc=r.returncode,out=r.stdout+r.stderr)); return r
source=t.MA.read_text()
mut=Path('/tmp/rv773-r5-priority.py'); mut.write_text(source.replace('for nen in (prov, goc / THU_MUC, goc):','for nen in (goc, goc / THU_MUC, prov):'))
for ca in t.CA:
 run('priority mutant '+ca,[sys.executable,'-B',str(K/'ops/land_evidence_nguon_test.py'),'--mot-ca',ca],env=dict(os.environ,LAND_EVIDENCE_NGUON_MA=str(mut)))
with t.cay("positive: '1/1'\nnguon_positive: result.txt\n",{'result.txt':'2/2'}) as root:
 (root/'result.txt').write_text('1/1')
 for ma in (t.MA,mut):
  run('priority A/B '+str(ma),[sys.executable,'-B',str(ma),'--root',str(root)])
with t.cay("x: 'measured — a.json'\n",{'a.json':'{}'}) as root:
 (root/'alias').symlink_to(root/'ops/land',target_is_directory=True)
 (root/'child').mkdir()
 for rt,fp in [('child/..','alias/'+t.TEN),('.',str(root/'alias'/t.TEN))]:
  run('root normalization + internal symlink',[sys.executable,'-B',str(t.MA),'--root',rt,'--tep',fp],cwd=root)
# Independent name-change mutation for fingerprint.
m2=Path('/tmp/rv773-r5-rename.py'); m2.write_text(source.replace('plat-x8-land-evidence.yaml','plat-x9-land-evidence.yaml'))
run('fingerprint rename',[sys.executable,'-B',str(K/'ops/land_evidence_nguon_test.py'),'--mot-ca','c10_l5_danh_sach_dong_bang'],env=dict(os.environ,LAND_EVIDENCE_NGUON_MA=str(m2)))
# Re-run old independent CLI regression on all four runtimes with absolute PYTHONPATH.
sp=Path.cwd().parent
for v in ('3.11','3.12','3.13','3.14'):
 run('old regression '+v,['python'+v,'-B','evidence/regression.py'],env=dict(os.environ,PYTHONPATH=str(sp/('yaml-python'+v)),PYTHONDONTWRITEBYTECODE='1'))
Path('evidence/extra.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
for row in rows: print(row['label'],row['rc'],row['out'][-220:])
