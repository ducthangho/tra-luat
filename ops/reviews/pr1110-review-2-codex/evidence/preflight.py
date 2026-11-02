import os, subprocess, json, hashlib
from pathlib import Path
os.environ['PYTHONDONTWRITEBYTECODE']='1'
S=Path(__file__).resolve().parent; R=S/'cay-kho'; E=S/'evidence'; W=S/'work'
B='fb74c6eca742205acc0af9bb7ea89da94f15aa21'; H='3a3aac561ba359c08dfe92d95584b56494fc12d4'
def git(*a): return subprocess.check_output(['git',*a],cwd=R)
def sha(b): return hashlib.sha256(b).hexdigest()
paths=git('diff','--name-only',B,H).decode().splitlines()
r={'head':git('rev-parse','HEAD').decode().strip(),'tree':git('rev-parse','HEAD^{tree}').decode().strip(),'base':B,'merge_base_origin_master':git('merge-base','HEAD','origin/master').decode().strip(),'status':git('status','--porcelain=v1','--untracked-files=all','--ignored').decode(),'abbrev':git('config','core.abbrev').decode().strip(),'changed_count':len(paths),'outside_reviews':[p for p in paths if not p.startswith('ops/reviews/')],'diff_equal':git('diff',B,H)==(S/'DIFF.patch').read_bytes(),'diff_sha256':sha(git('diff',B,H)),'round1_ops_delta_bytes':len(git('diff','e137f8c',H,'--','ops/reviews')),'round1_patch_equal':git('diff','e137f8c',H,'--','ops/reviews')==(S/'DIFF-OPS-REVIEWS-TU-LUOT1.patch').read_bytes()}
r['commits']=git('log','--format=%H %P %s',B+'..'+H).decode().splitlines()
(E/'changed-paths.txt').write_text('\n'.join(paths)+'\n'); (E/'preflight.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(r,ensure_ascii=False,indent=2))
assert r['head']==H and r['merge_base_origin_master']==B and not r['status'] and not r['outside_reviews'] and r['diff_equal'] and r['round1_ops_delta_bytes']==0 and r['round1_patch_equal']
W.mkdir(exist_ok=True)
for name,ref in [('head',H),('base',B)]:
 d=W/name
 subprocess.run(['git','clone','--shared','--no-checkout','--quiet',str(R),str(d)],check=True)
 subprocess.run(['git','-C',str(d),'config','core.abbrev','7'],check=True)
 subprocess.run(['git','-C',str(d),'checkout','--detach','--quiet',ref],check=True)
 print('COPY_READY',name,ref,flush=True)
