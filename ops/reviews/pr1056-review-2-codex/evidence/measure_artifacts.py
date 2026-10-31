from pathlib import Path
from collections import Counter
import hashlib,json,subprocess,yaml,re
base=Path(__file__).resolve().parent.parent;root=base/'cay-kho'
def git(*a):return subprocess.check_output(['git','-C',str(root),*a])
def sha(b):return hashlib.sha256(b).hexdigest()
for n in (1,2):
 d=root/f'ops/reviews/pr1050-review-{n}-codex';r=yaml.safe_load((root/f'ops/reviews/pr1050-review-{n}-codex-verdict.receipt.yaml').read_text());run=json.loads((d/'run/run.json').read_bytes());v=(d/'VERDICT.md').read_bytes()
 es=[]
 for line in (d/'SHA256SUMS').read_text().splitlines():
  digest,name=line.split(maxsplit=1);es.append((name.removeprefix('*').removeprefix('./'),digest))
 names=[e[0] for e in es];actual={p.relative_to(d).as_posix() for p in d.rglob('*') if p.is_file() and p.name!='SHA256SUMS'}
 print('ROUND',n,'MANIFEST',len(es),'ACTUAL',len(actual),'MISSING',sorted(actual-set(names)),'EXTRA',sorted(set(names)-actual),'DUPLICATE',len(names)-len(set(names)),'BAD_HASH',[name for name,h in es if sha((d/name).read_bytes())!=h])
 print('FLAT_EQUAL',v==(root/r['verdict_path']).read_bytes(),'BYTES',len(v),'SHA256',sha(v),'HEADER',v.decode().splitlines()[:3])
 print('RUN',json.dumps({k:run.get(k) for k in ['run_id','head','provider','execution_surface','transport','worktree_sach','ma_thoat','trang_thai','bat_dau_utc','ket_thuc_utc','thoi_luong_giay','model_phuc_vu_trang_thai','effort_phuc_vu','effort_phuc_vu_trang_thai']},ensure_ascii=False))
 print('PROMPT_HASH',sha((d/'PROMPT.md').read_bytes()),'RUN_MATCH',sha((d/'PROMPT.md').read_bytes())==run['prompt_sha256'])
 print('MODEL_EVENTS',len(run['model_phuc_vu']),'MODELS',dict(Counter(x['model'] for x in run['model_phuc_vu'])))
 print('TREE',git('rev-parse',r['reviewed_sha']+'^{tree}').decode().strip(),'TREE_MATCH',git('rev-parse',r['reviewed_sha']+'^{tree}').decode().strip()==r['reviewed_tree'])
 for name in ('stdout','stderr'):
  b=(d/f'run/{name}.log').read_bytes();print(name,'BYTES',len(b),'BYTE_MATCH',len(b)==run[name+'_byte'],'HASH_MATCH',sha(b)==run[name+'_sha256'])
 ck=json.loads((d/'run/checkpoint.json').read_bytes());print('CHECKPOINT',ck,'HASH_MATCH',sha((d/'run/checkpoint.json').read_bytes())==run['checkpoint_sha256'])
 raw=git('diff','b29da0b',r['reviewed_sha']);omit=(d/'OMITTED.txt').read_text();print('OMITTED_REGENERATED','BYTES',len(raw),'SHA256',sha(raw),'MATCH',str(len(raw)) in omit and sha(raw) in omit)
 oid,path=r['evidence_url'].split('/blob/',1)[1].split('/',1);print('PINNED_BLOB',oid,path,'EXISTS_EQUAL',git('show',oid+':'+path)==v)
 print('NOT_IN_REPO',[x for x in git('ls-tree','-r','--name-only','HEAD','--',d.relative_to(root).as_posix()).decode().splitlines() if '/mirror.git/' in x or '/review-copy/' in x or '/cay-kho/' in x or x==str(d.relative_to(root))+'/diff.patch'])
d1=root/'ops/reviews/pr1050-review-1-codex';d2=root/'ops/reviews/pr1050-review-2-codex'
for a,b in [('VERDICT.md','luot1-VERDICT.md'),('HINT.patch','luot1-HINT.patch')]:print('OLD_COPY',b,'EQUAL',(d1/a).read_bytes()==(d2/'verdict-cu'/b).read_bytes())
raw=git('diff','c24875d','f37b519');print('ROUND2_PATCH_MATCH',raw==(d2/'diff-tu-luot1.patch').read_bytes(),'BYTES',len(raw))
