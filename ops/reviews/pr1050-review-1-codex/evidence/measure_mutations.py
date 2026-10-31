from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import os, subprocess, json
root=Path('review-copy').resolve();out=Path('evidence').resolve()
commands={
 'bien_nhan_v2':['python3','ops/bien_nhan_v2.py','--root','.'],
 'land_evidence_nguon':['python3','ops/land_evidence_nguon.py','--root','.'],
 'doctrine_scan':['python3','.claude/dev/packet_loop.py','doctrine-scan','--root','.'],
 't26':['python3','ops/lease_publish_test.py','--chi-ca=t26_'],
 't27':['python3','ops/lease_publish_test.py','--chi-ca=t27_'],
 't138':['python3','ops/lease_publish_test.py','--chi-ca=t138_']}
verdict=root/'ops/reviews/wp1037-g1-codex-luot2-verdict.md'
readme=root/'ops/reviews/README.md'
receipt=root/'ops/reviews/wp1037-g1-codex-luot2-verdict.receipt.yaml'
def remove_row(b,kind):
 lines=b.splitlines(keepends=True)
 selected=[l for l in lines if (l.startswith(b'| [`wp1037-g1-codex-luot2-verdict.md`]') if kind=='toc' else l.startswith(b'| `wp1037-g1-codex-luot2-verdict.md` | `CHECKOUT-REVIEW'))]
 assert len(selected)==1,len(selected)
 return b.replace(selected[0],b'',1)
mutations=[('verdict-one-byte',verdict,lambda b:b'v'+b[1:]),('readme-delete-toc',readme,lambda b:remove_row(b,'toc')),('receipt-so-p1',receipt,lambda b:b.replace(b'so_p1: 0\n',b'so_p1: 1\n',1)),('readme-delete-caveat',readme,lambda b:remove_row(b,'caveat'))]
all_results=[]
for label,path,mut in mutations:
 original=path.read_bytes(); changed=mut(original);assert original!=changed
 path.write_bytes(changed)
 try:
  def run(item):
   name,cmd=item
   r=subprocess.run(cmd,cwd=root,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   (out/f'mutant-{label}-{name}.log').write_bytes(r.stdout)
   (out/f'mutant-{label}-{name}.rc').write_text(str(r.returncode)+'\n')
   relevant=[line for line in r.stdout.decode(errors='replace').splitlines() if any(t in line for t in ['TỔNG:','lease_publish:','doctrine-scan:','LỆCH BĂM','KHÔNG có trong','KHÔNG nằm ở','KHÔNG ĐẠT','ĐỎ ','SO_P'])]
   return {'gate':name,'rc':r.returncode,'output':relevant}
  with ThreadPoolExecutor(max_workers=6) as pool: result=list(pool.map(run,commands.items()))
  print(label,json.dumps(result,ensure_ascii=False),flush=True)
  all_results.append({'mutant':label,'path':str(path.relative_to(root)),'results':result})
 finally:path.write_bytes(original)
(out/'mutations.json').write_text(json.dumps(all_results,ensure_ascii=False,indent=2)+'\n')
