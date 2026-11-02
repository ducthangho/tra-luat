from pathlib import Path
import difflib,subprocess,os,json
root=Path.cwd(); repo=root/'cay-kho'; out=Path('/tmp/pr896-r2-audit-b3269a02'); copy=out/'copy'; env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0'); logs=[]
message='Verdict dong 7 tu khai `execution_surface: codex_service` va phu nhan di qua `codex exec`, nhung run.json 9f946d71 dong 47 ghi execution_surface=codex_cli, lenh.chuong_trinh=codex; run/stderr-header.txt ghi OpenAI Codex v0.163.0. Dinh chinh be mat thanh codex_cli; giu nguyen byte verdict lich su. Dinh chinh nay KHONG chung thuc model/effort da phuc vu va KHONG doi assurance cross_reviewed.'
files=['ops/reviews/pr889-review-1-codex-verdict.receipt.yaml','ops/reviews/README.md']; originals={p:(repo/p).read_bytes() for p in files}; modified={}
s=originals[files[0]].decode(); anchor='verdict_usage_caveats:\n'; assert s.count(anchor)==1; modified[files[0]]=s.replace(anchor,anchor+'  - id: VERDICT-KHAI-SAI-EXECUTION-SURFACE\n    muc: P1\n    mo_ta: >-\n      '+message+'\n',1)
s=originals[files[1]].decode(); lines=s.splitlines(True); idx=next(i for i,l in enumerate(lines) if l.startswith('| `pr889-review-1-codex-verdict.md` |')); lines.insert(idx,'| `pr889-review-1-codex-verdict.md` | `VERDICT-KHAI-SAI-EXECUTION-SURFACE` | '+message+' |\n'); modified[files[1]]=''.join(lines)
patch=''.join(''.join(difflib.unified_diff(originals[p].decode().splitlines(True),modified[p].splitlines(True),fromfile=p,tofile=p)) for p in files); (root/'HINT.patch').write_text(patch)
for p in files: assert (copy/p).read_bytes()==originals[p]
def run(cmd):
 z=subprocess.run(cmd,cwd=copy,env=env,text=True,capture_output=True,timeout=120); return z
z=run(['patch','--dry-run','-p0','--fuzz=0','-i',str(root/'HINT.patch')]); logs.append('patch --dry-run -p0 --fuzz=0: rc='+str(z.returncode)+'; '+repr(z.stdout)); assert z.returncode==0
try:
 z=run(['patch','-p0','--fuzz=0','-i',str(root/'HINT.patch')]); logs.append('patch -p0 --fuzz=0: rc='+str(z.returncode)+'; '+repr(z.stdout)); assert z.returncode==0
 for selector in ['t26_','t27_','t138_']:
  z=run(['python3','ops/lease_publish_test.py','--chi-ca='+selector]); summary=[l for l in z.stdout.splitlines() if l.startswith(('lease_publish:','  ĐỎ'))]; logs.append('patched '+selector+': rc='+str(z.returncode)+'; '+' | '.join(summary)); assert z.returncode==0 and 'lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0' in z.stdout
 z=run(['python3','ops/bien_nhan_v2.py','--root','.']); logs.append('patched bien_nhan_v2: rc='+str(z.returncode)+'; '+repr(z.stdout.strip())); assert z.returncode==0
 readme=copy/files[1]; saved=readme.read_bytes(); readme.write_text(''.join(l for l in saved.decode().splitlines(True) if not ('pr889-review-1-codex-verdict.md' in l and 'VERDICT-KHAI-SAI-EXECUTION-SURFACE' in l)))
 z=run(['python3','ops/lease_publish_test.py','--chi-ca=t27_']); summary=[l for l in z.stdout.splitlines() if l.startswith(('lease_publish:','  ĐỎ'))]; logs.append('patched, remove_new_README_row t27_: rc='+str(z.returncode)+'; '+' | '.join(summary)); assert z.returncode==1 and 'lease_publish: 0/1 đạt' in z.stdout; readme.write_bytes(saved)
 git=subprocess.run(['git','diff','--name-only'],cwd=copy,env=env,text=True,capture_output=True); logs.append('copy changed_files='+repr(git.stdout.splitlines())); assert set(git.stdout.splitlines())==set(files)
 for slug in ['pr889-review-1-codex']:
  for path in ['ops/reviews/'+slug+'-verdict.md','ops/reviews/'+slug+'/VERDICT.md','ops/reviews/'+slug+'/SHA256SUMS']:
   logs.append('preserved '+path+'='+str((copy/path).read_bytes()==(repo/path).read_bytes())); assert (copy/path).read_bytes()==(repo/path).read_bytes()
finally:
 for p,b in originals.items(): (copy/p).write_bytes(b)
s='\n'.join(logs)+'\n'; (out/'hint-validation.log').write_text(s); print(s)
with (root/'VERDICT.md').open('a') as f: f.write('\n### HƯỚNG 18: Kiểm HINT.patch trên bản sao và phản chứng cảnh báo mới\n\nGiả thuyết: hint không áp bằng patch -p0, phá hash hoặc thêm caveat chưa được t27 bảo vệ.\n\nLệnh: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr896-r2-audit-b3269a02/build_hint.py`. Hint chỉ sửa sidecar + một hàng README.\n\nOutput thật:\n```text\n'+s+'```\n\nKết luận: KHÔNG PHẢI LỖI của hint. Đã thử trên bản sao, CHƯA áp trên cây thật; executor phải tự áp/tự đo. Tệp verdict lịch sử, băm, manifest và assurance giữ nguyên.\n')
