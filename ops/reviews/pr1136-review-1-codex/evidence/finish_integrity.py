from pathlib import Path
import os,subprocess,hashlib,json
S=Path(__file__).resolve().parent;R=S/'cay-kho';E=S/'evidence';os.environ['GIT_CONFIG_GLOBAL']=str(S/'audit.gitconfig');os.environ['GIT_CONFIG_NOSYSTEM']='1';os.environ['GIT_OPTIONAL_LOCKS']='0';os.environ['PYTHONDONTWRITEBYTECODE']='1'
old=json.loads((E/'original-before.json').read_text());new={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in R.rglob('*') if p.is_file() and '.git' not in p.relative_to(R).parts}
out={'files_before':len(old),'files_after':len(new),'added':sorted(set(new)-set(old)),'removed':sorted(set(old)-set(new)),'modified':[p for p in old.keys()&new.keys() if old[p]!=new[p]],'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'status':subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=all'],cwd=R).decode()}
(E/'final-integrity.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False))
with (S/'VERDICT.md').open('a') as f:f.write('\nKiểm tra cuối — `python3 finish_integrity.py`:\n```json\n'+json.dumps(out,ensure_ascii=False,indent=2)+'\n```\n')
