import difflib
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo=Path.cwd()
root=repo.parent
original=(repo/'CLAUDE.md').read_text()
before='''  · hành vi ấy được khoá bằng `t162_M4_evaluator_toi_gian_chuan_bi` trong `ops/lease_publish_test.py`
  (đánh giá biểu thức thật bằng `_danh_gia_bieu_thuc_chuan_bi` cho push / PR thường / PR nhãn `windows` /
  từng `runner_set`) — đổi ma trận mà quên ca ấy thì gate ĐỎ, nên đọc ca ấy là đọc ma trận HIỆN HÀNH.
'''
after='''  · riêng hành vi của output `os` được khoá bằng `t162_M4_evaluator_toi_gian_chuan_bi` trong `ops/lease_publish_test.py`
  (đánh giá biểu thức thật bằng `_danh_gia_bieu_thuc_chuan_bi` cho push / PR thường / PR nhãn `windows` /
  từng `runner_set`). Ca này không đọc `exclude:` hay `if:` mức job, nên vẫn phải đọc chúng trong `ci.yml`;
  phần mảnh/gom của `gate-cong-cu*` có chốt riêng ở `loi_g5_workflow` trong `.claude/dev/ci_dang_ky_test.py`.
'''
assert original.count(before)==1
updated=original.replace(before,after)
patch=''.join(difflib.unified_diff(original.splitlines(True),updated.splitlines(True),fromfile='CLAUDE.md',tofile='CLAUDE.md'))
(root/'HINT.patch').write_text('# chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit\n'+patch)
with tempfile.TemporaryDirectory(prefix='pr896-hint-') as td:
    target=Path(td)
    (target/'CLAUDE.md').write_text(original)
    for args in (['patch','-p0','--dry-run','-i',str(root/'HINT.patch')],['patch','-p0','-i',str(root/'HINT.patch')]):
        r=subprocess.run(args,cwd=target,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        print('$ '+' '.join(args));print(r.stdout,end='');print('rc='+str(r.returncode))
        assert r.returncode==0
    assert (target/'CLAUDE.md').read_text()==updated
print('patched scratch content matches intended wording; source CLAUDE.md unchanged:',(repo/'CLAUDE.md').read_text()==original)
print('HINT.patch only changes CLAUDE.md; no workflow/test/runtime hunks.')
