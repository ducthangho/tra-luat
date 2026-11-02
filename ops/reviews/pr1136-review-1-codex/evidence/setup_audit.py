from pathlib import Path
import os, subprocess, json, hashlib, shutil
S=Path(__file__).resolve().parent
os.environ['PYTHONDONTWRITEBYTECODE']='1'
os.environ['GIT_CONFIG_GLOBAL']=str(S/'audit.gitconfig')
os.environ['GIT_CONFIG_NOSYSTEM']='1'
R=S/'cay-kho'; E=S/'evidence'; E.mkdir(exist_ok=True)
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
files=[p for p in R.rglob('*') if p.is_file() and '.git' not in p.relative_to(R).parts]
snap={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(E/'original-before.json').write_text(json.dumps(snap,sort_keys=True))
base='62e629156fd0729b743f15eed2f32487786b9adc'; head=git('rev-parse','HEAD').decode().strip()
names=git('diff','--name-only',base,'HEAD').decode().splitlines()
patch=git('diff',base,'HEAD')
data={'head':head,'tree':git('rev-parse','HEAD^{tree}').decode().strip(),'status':git('status','--porcelain=v1').decode(),'abbrev':git('config','core.abbrev').decode().strip(),'base':base,'merge_base_origin_master':git('merge-base','HEAD','origin/master').decode().strip(),'changed_count':len(names),'outside_reviews':[p for p in names if not p.startswith('ops/reviews/')],'patch_matches':patch==(S/'DIFF.patch').read_bytes(),'patch_sha256':hashlib.sha256(patch).hexdigest(),'commits':git('log','--format=%H %s',base+'..HEAD').decode()}
(E/'preflight.json').write_text(json.dumps(data,ensure_ascii=False,indent=2));print(json.dumps(data,ensure_ascii=False))
(E/'changed.txt').write_text('\n'.join(names)+'\n')
for name,sha in [('head',head),('base',base),('mutant',head)]:
 dest=S/'work'/name
 if not dest.exists(): subprocess.run(['cp','-a','--reflink=auto',str(R),str(dest)],check=True)
 subprocess.run(['git','config','core.abbrev','7'],cwd=dest,check=True)
 if name=='base':subprocess.run(['git','checkout','--detach',sha],cwd=dest,check=True,stdout=subprocess.DEVNULL)
 print('READY',name,flush=True)
