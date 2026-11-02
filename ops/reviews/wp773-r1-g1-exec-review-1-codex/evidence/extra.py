exec(open('/tmp/rv773-review/probes.py').read().split('cases=')[0])
m=t.nap();m.MIEN_TRU_CUTOVER={}
rc,ra=t.kiem(m,pathlib.Path('/home/user/rv773'));pathlib.Path('/tmp/rv773-review/no-exempt.log').write_text(ra);print('NO_EXEMPT rc',rc,ra.splitlines()[-2:]); print('L1',ra.count('\n  L1 '),'L2',ra.count('\n  L2 '),'L3',ra.count('\n  L3 '))
# Compare frozen independent digest to Git blobs, not the runtime dictionary.
import hashlib
names=subprocess.check_output(['git','-C','/home/user/rv773','ls-tree','-r','--name-only','c73af7b','ops/land']).decode().splitlines()
ds=[]
for name in names:
 if name.endswith('-land-evidence.yaml') and name.count('/')==2:
  blob=subprocess.check_output(['git','-C','/home/user/rv773','show','c73af7b:'+name]);ds.append((pathlib.Path(name).name,hashlib.sha256(blob).hexdigest()))
print('GIT_SNAPSHOT',len(ds),hashlib.sha256(json.dumps(sorted(ds)).encode()).hexdigest())
# Demonstrate the identical timestamp key is checked within a list, skipped in a mapping.
for hs in ["pre_merge_checks:\n  - {'2026-10-16T02:59:00Z': ok}\n", "pre_merge_checks:\n  gate: {luc: '2026-10-16T02:59:00Z'}\n"]:
 print('DICT_CONTROL',t.chay(hs,pv))
with t.cay("x: 'measured — a.json'\n",{'real.json':'{}'}) as root:
 (root/'ops/land'/t.PROV/'a.json').symlink_to('real.json');print('SYMLINK_INTERNAL',t.kiem(t.nap(),root))
with t.cay("pre_merge_checks: ['2026-99-16T02:59:00Z']\n",pv) as root:
 r=subprocess.run(['python3.13','-B','/home/user/rv773/ops/land_evidence_nguon.py','--root',str(root)],capture_output=True,text=True)
 print('INVALID_DATE_CLI',r.returncode,r.stdout,r.stderr)
# Surviving weakening mutation of mapping support.
source=pathlib.Path('/home/user/rv773/ops/land_evidence_nguon.py').read_text()
a='list(pmc.values()) if isinstance(pmc, dict)';b='[] if isinstance(pmc, dict)'
p=pathlib.Path('/tmp/rv773-review/dict_walk.py');p.write_text(source.replace(a,b))
for ca in t.CA:
 rc,out=t.chay_con(ca,p)
 print('DICT_MUT_ALL',ca,rc,out.strip())
