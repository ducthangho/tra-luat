from pathlib import Path
import json,hashlib,os,subprocess
S=Path(__file__).resolve().parent;R=S/'cay-kho';E=S/'evidence'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_CONFIG_GLOBAL=str(S/'audit.gitconfig'),GIT_CONFIG_NOSYSTEM='1',GIT_OPTIONAL_LOCKS='0')
old=json.loads((E/'original-before.json').read_text());new={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in R.rglob('*') if p.is_file() and '.git' not in p.relative_to(R).parts}
res=dict(before_files=len(old),after_files=len(new),changed=[p for p in old.keys()&new.keys() if old[p]!=new[p]],added=sorted(new.keys()-old.keys()),removed=sorted(old.keys()-new.keys()))
for label,path in [('original',R),('head_copy',S/'work/head')]:
 for key,args in [('head',['rev-parse','HEAD']),('tree',['rev-parse','HEAD^{tree}']),('status',['status','--porcelain=v1','--untracked-files=all'])]:
  cp=subprocess.run(['git',*args],cwd=path,env=env,capture_output=True,text=True);res[label+'_'+key]=dict(cmd=['git',*args],rc=cp.returncode,stdout=cp.stdout.strip(),stderr=cp.stderr)
res['mutated_receipts_restored']=all((R/f'ops/reviews/pr1119-review-{n}-codex-verdict.receipt.yaml').read_bytes()==(S/'work/head'/f'ops/reviews/pr1119-review-{n}-codex-verdict.receipt.yaml').read_bytes() for n in (1,2))
(E/'final-integrity.json').write_text(json.dumps(res,ensure_ascii=False,indent=2));print(json.dumps(res,ensure_ascii=False,indent=2))
assert not any(res[x] for x in ('changed','added','removed'));assert res['mutated_receipts_restored'];assert res['original_status']['stdout']==''
with (S/'VERDICT.md').open('a') as f:f.write(f'\nKiểm cuối: `PYTHONDONTWRITEBYTECODE=1 python3 final_integrity.py`: {len(old)} → {len(new)} tệp, changed/added/removed đều [], original status rỗng, head/tree giữ nguyên; cả hai biên nhận bản sao đã hồi nguyên byte. `evidence/final-integrity.json`.\n')
