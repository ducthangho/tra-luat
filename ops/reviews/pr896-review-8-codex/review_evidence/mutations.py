import json, os, re, subprocess
from pathlib import Path
from measure import BASE,OUT,SHA,record
repo=Path((OUT/'copy-path.txt').read_text()); assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==SHA
readme=repo/'ops/reviews/README.md'; receipt=repo/'ops/reviews/pr896-review-7-codex-verdict.receipt.yaml'
originals={p:p.read_bytes() for p in [readme,receipt]}; text=readme.read_text(); rt=receipt.read_text()
index=[s for s in text.splitlines(keepends=True) if s.startswith('| [`pr896-review-7-codex-verdict.md`]')]; assert len(index)==1
row=[s for s in text.splitlines(keepends=True) if s.startswith('| `pr896-review-7-codex-verdict.md` | `LAN-CHAY-DAU-CHET-VI-MAY-CHU-QUA-TAI`')]; assert len(row)==1
caveat=re.search(r'  - id: LAN-CHAY-DAU-CHET-VI-MAY-CHU-QUA-TAI\n.*?(?=  - id:)',rt,re.S); assert caveat
cases=[('delete-new-index-row',readme,index[0]),('delete-new-caveat-readme-row',readme,row[0]),('delete-new-receipt-caveat',receipt,caveat[0])]
results=[]; lines=[f'copy={repo}',f'HEAD={SHA}']
for label,p,old in cases:
 try:
  assert p.read_text().count(old)==1; p.write_text(p.read_text().replace(old,'')); lines.append(f'{label} removed_bytes={len(old.encode())}')
  for t in ['t26','t27','t138']:
   cmd=['python3','ops/lease_publish_test.py','--chi-ca='+t+'_']; r=subprocess.run(cmd,cwd=repo,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
   (OUT/f'{label}-{t}.log').write_text(r.stdout+r.stderr); summary='\n'.join(s for s in r.stdout.splitlines() if s.startswith(('lease_publish:','!!!','  !!!')) or 'KHÔNG' in s)
   lines.append(f'{t} rc={r.returncode} {summary}'); results.append(dict(case=label,test=t,rc=r.returncode,summary=summary))
 finally:
  for p,b in originals.items():p.write_bytes(b)
status=subprocess.check_output(['git','status','--porcelain=v1'],cwd=repo,text=True); lines.append(f'status_after_restore={status!r}');(OUT/'mutations.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
record(5,'Đột biến hàng README và caveat mới trên clone','Ba ca có sẵn phải thật sự phát hiện mất hàng/caveat mới.','git clone --no-hardlinks --no-checkout mirror.git <copy>; git checkout --detach '+SHA+'; python3 review_evidence/mutations.py',lines,'KHÔNG PHẢI LỖI hiện hành trong hai lớp săn; t27 có răng với hàng mục lục/cảnh báo README. t26 và t138 không có răng với các hàng đó; cả ba không có răng khi xóa caveat khỏi receipt. Không quy chốt kiểm hình thức thành chốt nội dung')
