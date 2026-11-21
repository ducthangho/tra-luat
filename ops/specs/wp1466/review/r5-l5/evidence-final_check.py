from pathlib import Path
import hashlib,json,subprocess,os,datetime
O=Path(__file__).resolve().parent;R=O.parent/'cay-kho';before=json.loads((O/'source-snapshot.json').read_text());after={}
for p in R.rglob('*'):
 if p.is_file() and '.git' not in p.relative_to(R).parts:after[str(p.relative_to(R))]=[p.stat().st_size,p.stat().st_mtime_ns,hashlib.sha256(p.read_bytes()).hexdigest()]
print('AT',datetime.datetime.now(datetime.timezone.utc).isoformat());print('FILES_BEFORE_AFTER',len(before),len(after));print('ADDED',sorted(set(after)-set(before)));print('REMOVED',sorted(set(before)-set(after)));print('CONTENT_OR_STAT_CHANGED',[k for k in before.keys()&after.keys() if before[k]!=after[k]])
for args in [['status','--porcelain=v1','--untracked-files=all'],['rev-parse','HEAD','HEAD^{tree}'],['diff','--binary'],['diff','--cached','--binary']]:
 r=subprocess.run(['git','-C',str(R),*args],capture_output=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'));print('GIT',args,'RC',r.returncode,'BYTES',len(r.stdout),'SHA256',hashlib.sha256(r.stdout).hexdigest());
 if args[0]=='rev-parse':print(r.stdout.decode().strip())
print('SPEC_SHA256',hashlib.sha256((R/'ops/specs/wp1466.md').read_bytes()).hexdigest())
