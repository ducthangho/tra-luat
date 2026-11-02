from pathlib import Path
import subprocess,os,json,hashlib
B=Path(__file__).resolve().parent.parent;R=B/'cay-kho';C=Path((B/'evidence/clone-path.txt').read_text().strip());E=B/'evidence';env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
def call(cmd,repo=C):return subprocess.run(cmd,cwd=repo,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
paths=['ops/reviews/README.md','ops/reviews/pr889-review-1-codex-verdict.receipt.yaml'];saved={p:(C/p).read_bytes() for p in paths}
for p in paths:(C/p).write_bytes(subprocess.check_output(['git','show','578fb4b:'+p],cwd=R))
p=call(['patch','--batch','-p0','--fuzz=0','-i',str(R/'ops/reviews/pr896-review-2-codex/HINT.patch')]);log=p.stdout;print('old_hint_rc=',p.returncode,flush=True);assert p.returncode==0,p.stdout
for path in paths:
 match=(C/path).read_bytes()==saved[path];log+='target_blob_match '+path+' '+str(match)+'\n';print('target_blob_match',path,match,flush=True);assert match
(E/'old-hint-replay.log').write_text(log)
assert not call(['git','status','--porcelain=v1']).stdout
with (B/'VERDICT.md').open('a') as f:f.write('\n### HƯỚNG 11: Tái áp nguyên HINT lượt 2 và so blob\n- giả thuyết: bản vá 82359c4 không phải nguyên HINT như commit khai.\n- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/validate_hint.py` trên clone (hai tệp tài liệu lấy từ cha 578fb4b), `patch --batch -p0 --fuzz=0 -i <HINT-lượt-2>`; so byte với 82359c4.\n- output thật: `old_hint_rc=0`; `target_blob_match ops/reviews/README.md True`; `target_blob_match ops/reviews/pr889-review-1-codex-verdict.receipt.yaml True`.\n- kết luận: KHÔNG PHẢI LỖI; nguyên HINT tạo đúng hai blob của target, không có sửa thêm trong commit 82359c4.\n')
p=call(['patch','--batch','--dry-run','-p0','--fuzz=0','-i',str(B/'HINT.patch')]);(E/'hint-dry-run.log').write_text(p.stdout);print('hint_dry_run_rc=',p.returncode,flush=True);assert p.returncode==0,p.stdout
p=call(['patch','--batch','-p0','--fuzz=0','-i',str(B/'HINT.patch')]);(E/'hint-apply.log').write_text(p.stdout);print('hint_apply_rc=',p.returncode,flush=True);assert p.returncode==0,p.stdout
cmds=[['python3','ops/lease_publish_test.py','--chi-ca='+sel] for sel in ['t26_','t27_','t138_']]+[['python3','ops/bien_nhan_v2.py','--root','.'],['python3','ops/land_evidence_nguon.py','--root','.']]
rows=[]
for i,cmd in enumerate(cmds,1):
 p=call(cmd);(E/f'hint-gate-{i}.log').write_text(p.stdout)
 summary=[l for l in p.stdout.splitlines() if l.startswith(('lease_publish:','bien_nhan_v2:','land_evidence_nguon:','TỔNG:'))]
 row={'cmd':' '.join(cmd),'rc':p.returncode,'summary':summary};rows.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
(E/'hint-gates.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
changed=call(['git','diff','--name-only']).stdout.splitlines();assert all(p.endswith(('.md','.yaml')) for p in changed);assert not any(p.endswith('-verdict.md') for p in changed)
print('hint_changed_files=',len(changed),flush=True)
with (B/'VERDICT.md').open('a') as f:
 f.write('\n### HƯỚNG 12: Kiểm HINT mới trên bản sao\n- giả thuyết: gợi ý vá phá YAML/mục lục/băm verdict hoặc tự đổi lịch sử/assurance.\n- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/validate_hint.py`; dry-run và áp `patch --batch -p0 --fuzz=0 -i HINT.patch`, rồi chạy từng lệnh dưới trên clone.\n- output thật:\n```text\nhint_dry_run_rc=0\nhint_apply_rc=0\n')
 for row in rows:f.write(json.dumps(row,ensure_ascii=False)+'\n')
 f.write('hint_changed_files='+str(len(changed))+'; chi .md/.yaml; khong sua *-verdict.md\n```\n- kết luận: '+('KHÔNG PHẢI LỖI' if all(x['rc']==0 for x in rows) else 'LỖI TRONG HINT, phải sửa trước khi giao')+'. Đây là kiểm gợi ý trên clone, chưa áp lên cây giao review, chưa chứng nhận approval/land.\n')
