from pathlib import Path
import json, os, re, subprocess, tempfile
BASE=Path(__file__).resolve().parent.parent
OUT=BASE/'evidence'
CLONE=Path(tempfile.mkdtemp(prefix='pr896-r3-mutants-',dir='/tmp'))/'repo'
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
def call(cmd,**kwargs):
 return subprocess.run(cmd,env=ENV,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,**kwargs)
p=call(['git','clone','--no-hardlinks','--no-checkout',str(BASE/'mirror.git'),str(CLONE)])
(OUT/'clone.log').write_text(p.stdout);assert p.returncode==0,p.stdout
p=call(['git','checkout','--detach','82359c4deec90edebbaebf9ab9d094902120b567'],cwd=CLONE)
with (OUT/'clone.log').open('a') as f:f.write(p.stdout)
assert p.returncode==0,p.stdout
assert call(['git','rev-parse','HEAD'],cwd=CLONE).stdout.strip()=='82359c4deec90edebbaebf9ab9d094902120b567'
(OUT/'clone-path.txt').write_text(str(CLONE)+'\n')
readme=CLONE/'ops/reviews/README.md';receipt=CLONE/'ops/reviews/pr889-review-1-codex-verdict.receipt.yaml'
originals={readme:readme.read_bytes(),receipt:receipt.read_bytes()}
rows=[]
for mutation in ['delete_README_row','delete_receipt_caveat']:
 for p,b in originals.items():p.write_bytes(b)
 if mutation=='delete_README_row':
  s=readme.read_text();lines=s.splitlines(keepends=True);chosen=[l for l in lines if 'pr889-review-1-codex-verdict.md' in l and 'VERDICT-KHAI-SAI-EXECUTION-SURFACE' in l];assert len(chosen)==1
  readme.write_text(s.replace(chosen[0],''))
 else:
  s=receipt.read_text();s2,n=re.subn(r'(?m)^  - id: VERDICT-KHAI-SAI-EXECUTION-SURFACE\n.*?(?=^  - id:)', '',s, count=1,flags=re.S);assert n==1
  receipt.write_text(s2)
 diff=call(['git','diff','--stat'],cwd=CLONE);(OUT/(mutation+'-diff.log')).write_text(diff.stdout)
 for sel in ['t26_','t27_','t138_']:
  cmd=['python3','ops/lease_publish_test.py','--chi-ca='+sel]
  p=call(cmd,cwd=CLONE);(OUT/(mutation+'-'+sel+'.log')).write_text(p.stdout)
  summary=[l for l in p.stdout.splitlines() if l.startswith('lease_publish:')]
  row={'mutation':mutation,'selector':sel,'rc':p.returncode,'summary':summary}
  rows.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
 with (BASE/'VERDICT.md').open('a') as f:
  f.write('\n### HƯỚNG '+('7' if mutation=='delete_README_row' else '8')+': '+mutation+' trên bản sao exact SHA\n')
  f.write('- giả thuyết: bỏ '+('hàng README mới' if mutation=='delete_README_row' else 'caveat receipt mới')+' sẽ làm cả ba ca đỏ.\n')
  f.write('- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/mutations.py` (clone cục bộ từ `mirror.git`, checkout `82359c4`; chỉ đổi tài liệu/receipt).\n- output thật:\n```text\n')
  for row in rows[-3:]:f.write(json.dumps(row,ensure_ascii=False)+'\n')
  f.write('```\n- kết luận: '+('KHÔNG PHẢI LỖI. t27 có răng với hàng README khi caveat còn; t26/t138 không có răng với hàng này.\n' if mutation=='delete_README_row' else 'KHÔNG PHẢI LỖI của lời khai đã giới hạn; cả t26/t27/t138 không có răng với việc bỏ caveat. Không dùng nền xanh để suy phát hiện đủ mâu thuẫn surface.\n'))
for p,b in originals.items():p.write_bytes(b)
(OUT/'mutation-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
assert not call(['git','status','--porcelain=v1'],cwd=CLONE).stdout
