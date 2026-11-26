from pathlib import Path
import hashlib,json,subprocess
w=Path(__file__).resolve().parent;r=w.parent/'repo'
before=json.loads((w/'snapshot-start.json').read_text());after={str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for p in r.rglob('*') if p.is_file() and '.git' not in p.relative_to(r).parts}
delta=[x for x in sorted(set(before)|set(after)) if before.get(x)!=after.get(x)]
cmds=[]
for cmd in [['git','rev-parse','HEAD','HEAD^{tree}'],['git','status','--porcelain=v1','--untracked-files=all','--ignored=matching'],['git','diff','--binary'],['git','diff','--cached','--binary']]:
 q=subprocess.run(cmd,cwd=r,capture_output=True,text=True);cmds.append(dict(command=cmd,rc=q.returncode,stdout=q.stdout,stderr=q.stderr))
out=dict(files_before=len(before),files_after=len(after),delta=delta,commands=cmds,limit='Hai mốc quan sát; không chứng minh lịch sử không từng ghi rồi khôi phục. Repo nguồn ngoài checkout được giao không nằm trong phạm vi quan sát.')
(w/'snapshot-final.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False))
