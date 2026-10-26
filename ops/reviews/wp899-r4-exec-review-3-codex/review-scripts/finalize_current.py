from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parent
# All test writers have finished. Inventory stable evidence, excluding its own hash and expendable temporary/cache files.
rows={}
for p in sorted(R.rglob('*')):
 if not p.is_file() or p.name=='evidence-manifest.json' or any(x in ('tmp','cache') for x in p.relative_to(R).parts):continue
 b=p.read_bytes();rows[str(p.relative_to(R))]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(R/'evidence-manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
# Read back every stabilized artifact; no assertion from an earlier run substitutes for this check.
for name,rec in rows.items():
 b=(R/name).read_bytes();assert len(b)==rec['bytes'] and hashlib.sha256(b).hexdigest()==rec['sha256']
v=(R/'VERDICT.md').read_text();assert v.startswith('verdict: changes_requested\n');assert 'Reviewed commit: 27997a73c6b01e577ed655ea94e73d56adf697da' in v
for i in range(1,28):assert '| A'+str(i)+' |' in v
for i in range(1,12):assert '| F'+str(i).zfill(2)+' `' in v
for cmd in [['git','status','--short'],['git','diff','--check'],['git','rev-parse','HEAD','HEAD^{tree}']]:
 q=subprocess.run(cmd,capture_output=True);assert q.returncode==0;print('command',cmd,'rc',q.returncode,q.stdout.decode().strip())
print('VERDICT',rows['VERDICT.md']);print('stable artifacts verified',len(rows))
