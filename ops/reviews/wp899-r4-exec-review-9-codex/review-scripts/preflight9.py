import hashlib, json, pathlib, platform, subprocess, sys
R=pathlib.Path(__file__).resolve().parent; root=R.parent
commands=[['git','remote','get-url','origin'],['git','branch','--show-current'],['git','rev-parse','HEAD','HEAD^{tree}','HEAD^'],
 ['git','cat-file','-t','ba222ffd1615f0d74b59985b9612f725211b62f5'],
 ['git','merge-base','--is-ancestor','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD'],
 ['git','status','--porcelain=v1','--untracked-files=all'],['git','config','--get','core.abbrev'],
 ['git','diff','--numstat','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD'],
 ['git','diff','--name-status','431681270298ffab8edcd316bdf26670157b4b4e','HEAD'],
 ['git','diff','--check','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD'], ['git','diff','--exit-code'],['git','diff','--cached','--exit-code'],
 [sys.executable,'--version']]
rows=[]
for cmd in commands:
 p=subprocess.run(cmd,capture_output=True); rows.append({'command':cmd,'rc':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()})
spec=root/'.review-input/wp899-r4.md'; h=hashlib.sha256(spec.read_bytes()).hexdigest()
files={}
for p in root.rglob('*'):
 if not p.is_file() or '.review' in p.relative_to(root).parts or '.git' in p.relative_to(root).parts:continue
 files[str(p.relative_to(root))]={'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
out={'commands':rows,'spec_sha256':h,'platform':platform.platform(),'executable':sys.executable,'files':files}
suffix=sys.argv[1] if len(sys.argv)>1 else 'start'
(R/f'snapshot-{suffix}.json').write_text(json.dumps(out,ensure_ascii=False,indent=1))
print(json.dumps({k:v for k,v in out.items() if k!='files'},ensure_ascii=False,indent=2));print('FILES',len(files))
assert rows[2]['stdout'].splitlines()[0]=='d2cca1580ed23dbbc532fb21481d0fac1e6ad8ac'
assert h=='be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45'
