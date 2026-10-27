from pathlib import Path
import os,subprocess,re
out=Path('/tmp/pr896-r2-audit-b3269a02'); repo=out/'copy'; verdict=Path.cwd()/'VERDICT.md'; env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0'); id='VERDICT-KHAI-SAI-EXECUTION-SURFACE'; readme=repo/'ops/reviews/README.md'; original_readme=readme.read_bytes(); logs=[]
slugs=['pr870-review-2-codex','pr889-review-2-codex','pr870-review-3-codex','pr889-review-3-codex']
for slug in slugs:
 receipt=repo/'ops/reviews'/(slug+'-verdict.receipt.yaml'); old=receipt.read_bytes()
 for kind in ['delete_README_row','delete_receipt_caveat']:
  label=slug+'__'+kind
  try:
   if kind=='delete_README_row':
    lines=original_readme.decode().splitlines(True); selected=[x for x in lines if slug+'-verdict.md' in x and id in x]; assert len(selected)==1; readme.write_text(''.join(x for x in lines if x not in selected))
   else:
    new,n=re.subn(r'  - id: '+id+r'\n(?:(?!  - id:|\S)[^\n]*\n)*','',old.decode()); assert n==1; receipt.write_text(new)
   logs.append('MUTANT '+label)
   for prefix in ['t26_','t27_','t138_']:
    cmd=['python3','ops/lease_publish_test.py','--chi-ca='+prefix]; p=subprocess.run(cmd,cwd=repo,env=env,text=True,capture_output=True,timeout=60)
    (out/(label+'--'+prefix+'.log')).write_text(p.stdout+p.stderr)
    lines=[x for x in p.stdout.splitlines() if x.startswith(('lease_publish:','  ĐỎ'))]; s=prefix+' rc='+str(p.returncode)+'; '+' | '.join(lines); logs.append(s); print(label+' '+s,flush=True)
  finally: readme.write_bytes(original_readme); receipt.write_bytes(old)
  # Append after each mutation direction rather than waiting for all variants.
  with verdict.open('a') as f:
   f.write('\n### HƯỚNG 14 ('+label+'): Đột biến caveat trên bản sao\n\nGiả thuyết: mất cảnh báo tại một đầu có thể không bị chốt bắt.\n\nLệnh: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr896-r2-audit-b3269a02/caveat_mutations.py`; mỗi phiên bản gọi RIÊNG `python3 ops/lease_publish_test.py --chi-ca=t26_`, `--chi-ca=t27_`, `--chi-ca=t138_` trong `/tmp/pr896-r2-audit-b3269a02/copy`.\n\nOutput thật:\n```text\n'+'\n'.join(logs[-4:])+'\n```\n\nKết luận: '+('KHÔNG PHẢI LỖI của t27: xoá hàng README khiến t27 đỏ 0/1; t26 và t138 không có răng đối với biến thể này.' if kind=='delete_README_row' else 'LỖI của kỳ vọng phủ ngữ nghĩa: xoá caveat khỏi receipt, cả t26/t27/t138 vẫn xanh 1/1. Các chốt không có răng đối với caveat CHƯA ĐƯỢC KHAI; không coi cổng xanh là chứng minh đủ caveat.')+'\n')
(out/'caveat-mutations.log').write_text('\n'.join(logs)+'\n')
