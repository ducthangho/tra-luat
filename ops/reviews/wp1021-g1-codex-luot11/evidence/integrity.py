from pathlib import Path
import hashlib
import json
import re
import subprocess
from record import REPO, ROOT, ENV, record

def git(*a):
    return subprocess.check_output(['git','-C',str(REPO),*a],env=ENV).decode().strip()
paths = subprocess.check_output(['git','-C',str(REPO),'ls-files','-z','--cached','--others'],env=ENV).split(b'\0')
snap = {}
for raw in paths:
    if not raw:
        continue
    rel = raw.decode()
    p = REPO/rel
    snap[rel] = {'mode':oct(p.lstat().st_mode),
                 'sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'not-file'}
after = {'HEAD':git('rev-parse','HEAD'), 'tree':git('rev-parse','HEAD^{tree}'),
         'status':git('status','--porcelain=v1','--untracked-files=all','--ignored'),
         'index_tree':git('ls-files','--stage'), 'files':snap}
before = json.loads((ROOT/'evidence/snapshot-before.json').read_text())
(ROOT/'evidence/snapshot-after.json').write_text(json.dumps(after,ensure_ascii=False,sort_keys=True,indent=2))
assert after == before
suite = (ROOT/'evidence/h02.log').read_text()
header = re.search(r'^bien_nhan_v2_test — (\d+) ca$',suite,re.M)
summary = re.search(r'^bien_nhan_v2_test: (\d+)/(\d+) ca đạt · (\d+)/(\d+) đột biến thường CÓ RĂNG · (\d+)/(\d+) ca TỰ KIỂM đạt · (\d+)/(\d+) đột biến thường khai đối chứng$',suite,re.M)
assert summary and header
nums = list(map(int,summary.groups()))
assert nums[0] == nums[1] == int(header[1]) == 98
assert nums[2] == nums[3] == 153 and nums[4] == nums[5] == 2
assert nums[6:] == [135,153]
positive_cases = re.findall(r'^  ĐẠT   (\w+)$',suite,re.M)
assert len(positive_cases) == 98
assert 'TỔNG: ĐẠT\n' in suite and '[exit_code=0;' in suite
assert 'Codex home is inside a repository' not in suite
assert not re.search(r'^  (ĐỎ|KHÔNG ĐO ĐƯỢC)',suite,re.M)
lines = [f'HEAD={after["HEAD"]}',f'tree={after["tree"]}',
         f'snapshot_files_before={len(before["files"])}; after={len(snap)}',
         'all_file_contents_and_modes_equal=True',
         'index_entries_equal=True', 'tracked_untracked_ignored_status='+repr(after['status']),
         'full_snapshot_equal=True',summary[0],
         'positive_case_lines=98; header_denominator=98; equal=True',
         '135/153 là số mutant KHAI đối chứng, không phải tỉ lệ đạt.',
         'Codex home is inside a repository: absent',
         'Không có ca bỏ khỏi mẫu số; không có dòng ca thường ĐỎ/KHÔNG ĐO ĐƯỢC.']
for prefix in ('c14_','c40_','c76_','c88_','c89_','c98_','c99_','c100_','c101_'):
    name = next(n for n in positive_cases if n.startswith(prefix))
    lines.append('suite ĐẠT '+name)
for rel in ('ops/bien_nhan_v2.py','ops/bien_nhan_v2_test.py'):
    lines.append(rel+' sha256='+snap[rel]['sha256'])
record('h15','Kiểm toàn vẹn đầu/cuối và phân số dương của suite',
       'PYTHONDONTWRITEBYTECODE=1 python3 evidence/integrity.py', '\n'.join(lines))
