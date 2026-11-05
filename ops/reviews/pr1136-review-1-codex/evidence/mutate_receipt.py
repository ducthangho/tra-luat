from pathlib import Path
import subprocess,os,json
S=Path(__file__).resolve().parent;R=S/'work/mutant';E=S/'evidence';os.environ['PYTHONDONTWRITEBYTECODE']='1';os.environ['GIT_CONFIG_GLOBAL']=str(S/'audit.gitconfig');os.environ['GIT_CONFIG_NOSYSTEM']='1'
p=R/'ops/reviews/pr1131-review-1-codex-verdict.receipt.yaml';original=p.read_bytes();old=b'verdict_sha256: c6011123';new=b'verdict_sha256: d6011123';assert original.count(old)==1;p.write_bytes(original.replace(old,new))
out=[]
try:
 for name,cmd in [('bien-nhan',['python3','ops/bien_nhan_v2.py','--root','.']),('direct',['python3',str(S/'direct_gates.py'),'.'])]:
  r=subprocess.run(cmd,cwd=R,capture_output=True);(E/f'mutant-{name}.stdout').write_bytes(r.stdout);(E/f'mutant-{name}.stderr').write_bytes(r.stderr)
  text=r.stdout.decode(errors='replace');lines=text.splitlines();errors=[x for x in lines if ('VI PHẠM' in x or 'FAIL' in x or 'pr1131-review' in x)]
  out.append({'name':name,'command':cmd,'rc':r.returncode,'errors':errors,'tail':lines[-4:]});print(json.dumps(out[-1],ensure_ascii=False),flush=True)
finally:p.write_bytes(original)
(E/'mutation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
with (S/'VERDICT.md').open('a') as f:f.write('\nĐột biến — `python3 mutate_receipt.py` đổi riêng ký tự đầu verdict_sha256 của biên nhận mới trên work/mutant, rồi hồi nguyên:\n```json\n'+json.dumps(out,ensure_ascii=False,indent=2)+'\n```\n')
print('mutant status',subprocess.check_output(['git','status','--porcelain=v1'],cwd=R).decode())
