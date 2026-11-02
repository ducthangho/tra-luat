from pathlib import Path
import os,subprocess,json,re
S=Path(__file__).resolve().parent;R=S/'work/head';E=S/'evidence'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_CONFIG_GLOBAL=str(S/'audit.gitconfig'),GIT_CONFIG_NOSYSTEM='1',GIT_OPTIONAL_LOCKS='0')
results=[]
for n in (1,2):
 p=R/f'ops/reviews/pr1119-review-{n}-codex-verdict.receipt.yaml';orig=p.read_bytes()
 old=re.search(rb'^verdict_sha256: ([a-f0-9]{64})$',orig,re.M)[1]
 replacement=(b'0' if old[:1]!=b'0' else b'1')+old[1:]
 try:
  p.write_bytes(orig.replace(b'verdict_sha256: '+old,b'verdict_sha256: '+replacement,1))
  for name,cmd in [('bien-nhan',['python3','ops/bien_nhan_v2.py','--root','.']),('direct',['python3',str(S/'direct_tests.py'),'.'])]:
   cp=subprocess.run(cmd,cwd=R,env=env,capture_output=True,text=True)
   label=f'mutant-{n}-{name}'
   (E/(label+'.stdout')).write_text(cp.stdout);(E/(label+'.stderr')).write_text(cp.stderr)
   text=cp.stdout+cp.stderr
   names=set(re.findall(r'pr1119-review-\d+-codex-verdict\.receipt\.yaml',text))
   r=dict(round=n,cmd=cmd,changed_field='verdict_sha256',before=old.decode(),after=replacement.decode(),rc=cp.returncode,reported=sorted(names),only_expected=names=={p.name},stdout=cp.stdout,stderr=cp.stderr)
   results.append(r)
   print(label,'rc',cp.returncode,'only_expected',r['only_expected'],text[:1300],flush=True)
 finally:p.write_bytes(orig)
(E/'mutations.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
status=subprocess.check_output(['git','status','--porcelain'],cwd=R,env=env).decode()
print('restored status',repr(status))
with (S/'VERDICT.md').open('a') as f:
 f.write('\nĐột biến: `PYTHONDONTWRITEBYTECODE=1 python3 mutate_receipts.py`; đổi đúng 1 ký tự verdict_sha256 của từng biên nhận, hồi nguyên trong finally.\n')
 for r in results:f.write(f"- Lượt {r['round']} {r['cmd'][1]}: rc={r['rc']}, chỉ nêu đúng tệp={r['only_expected']}; output ở `evidence/mutations.json`.\n")
 f.write(f'- Status bản sao sau hồi nguyên: {status!r}.\n')
