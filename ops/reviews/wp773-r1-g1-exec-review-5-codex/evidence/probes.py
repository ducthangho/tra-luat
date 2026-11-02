import sys,importlib.util,subprocess,os,tempfile,json
from pathlib import Path
K=Path('/home/user/rv773'); O=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('t',K/'ops/land_evidence_nguon_test.py'); t=importlib.util.module_from_spec(s); s.loader.exec_module(t)
m=t.nap(); import yaml
rows=[]
def cli(label,hs,prov):
 with t.cay(hs,prov) as root:
  r=subprocess.run([sys.executable,'-B',str(t.MA),'--root',str(root)],capture_output=True,text=True)
 rows.append(dict(label=label,rc=r.returncode,stdout=r.stdout,stderr=r.stderr))
for hs in ["x: {<<: {a: 'measured — khong nguon', a: ok}}\n", "x: {<<: {null: 'measured — khong', null: ok}}\n",'x: 2026-02-30\n','pre_merge_checks: [2026-99-16T02:00:00Z]\n']:
 cli('regression '+hs,hs,{'a.json':'{}'})
for hs in ["x: 'measured — a.json'\n", "x: 'measured — trich/*.txt'\n", "x: 'measured — trich/'\n",'positive: 123\nnguon_positive: a.json\n',"pre_merge_checks: {'2026-10-16T02:59:00Z': ok}\n", "pre_merge_checks: ['2026-10-16T02:58:26.1Z']\n", "pre_merge_checks: ['2026-10-16T03:59:00+01:00']\n"]:
 cli('boundary '+hs,hs,{'a.json':'{}','trich/a.txt':'1/1','readback-pr-9001.json':t.RB_PR})
with t.cay("x: 'measured — a.json'\n",{'a.json':'{}'}) as root:
 p=root/'ops/land'/t.PROV
 (p/'inside.json').symlink_to(p/'a.json')
 (root/'ops/land'/t.TEN).write_text("x: 'measured — inside.json'\n")
 r=subprocess.run([sys.executable,'-B',str(t.MA),'--root',str(root)],capture_output=True,text=True)
 rows.append(dict(label='internal symlink',rc=r.returncode,stdout=r.stdout,stderr=r.stderr))
 # Ordinary CLI combination advertised in --tep help; no traversal token.
 r=subprocess.run([sys.executable,'-B',str(t.MA),'--root','.', '--tep',str(root/'ops/land'/t.TEN)],cwd=root,capture_output=True,text=True)
 rows.append(dict(label='relative root absolute file',rc=r.returncode,stdout=r.stdout,stderr=r.stderr))
for n in [100,300,450,480,490,495,500,600,1000]:
 hs=('x: '+'['*n+']'*n+'\n').encode()
 try: obj=m.nap_yaml(yaml,hs)
 except Exception as e: rows.append(dict(label='depth '+str(n),stage='loader',error=type(e).__name__)); continue
 try: list(m.duyet(obj)); rows.append(dict(label='depth '+str(n),stage='both pass'))
 except Exception as e: rows.append(dict(label='depth '+str(n),stage='traversal',error=type(e).__name__))
# Extra mutation: remove L2 content check, not merely its token-boundary check.
source=t.MA.read_text(); old='if not any(mau.search(nd) for nd in noi_dung):'; assert source.count(old)==1
mut=Path('/tmp/rv773-r4-l2-content.py'); mut.write_text(source.replace(old,'if False:'))
ca='c05_l2_luot2_positive_phai_co_nguon_chua_nguyen_van'
r=subprocess.run([sys.executable,'-B',str(K/'ops/land_evidence_nguon_test.py'),'--mot-ca',ca],env=dict(os.environ,LAND_EVIDENCE_NGUON_MA=str(mut)),capture_output=True,text=True)
rows.append(dict(label='extra mutation L2 content',rc=r.returncode,stdout=r.stdout,stderr=r.stderr))
(O/'probes.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
for row in rows: print(json.dumps(row,ensure_ascii=False))
