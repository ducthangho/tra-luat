import csv
import hashlib
import json
from pathlib import Path
import re
import statistics
import subprocess
import yaml

B = Path(__file__).resolve().parents[1]
R = B / 'cay-kho'
O = B / 'do-review10'

def git(*args):
    return subprocess.check_output(['git', '-C', str(R), *args])

def section(s, a, b):
    return s[s.index(a):s.index(b)]

g = (R / 'ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md').read_text()
g3 = git('show', '0bc6e56:ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md').decode()
lo = (R / 'ops/specs/LO-319-LINUX-BANG-CHUNG-XANH.md').read_text()
lo3 = git('show', '0bc6e56:ops/specs/LO-319-LINUX-BANG-CHUNG-XANH.md').decode()
lease_path = R / 'ops/leases/gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906.yaml'
lease_raw = lease_path.read_text()
lease = yaml.safe_load(lease_raw)
order = next(line for line in g.splitlines() if line.startswith('| số đo của GATE'))
report = dict(a2_r3_r4_byte_identical=section(g3, '**A2 (M2)', '**A3 (M3)') == section(g, '**A2 (M2)', '**A3 (M3)'),
    ordering_row=order, ordering_denies_old_baseline='chỉ còn là đối chiếu lịch sử cho A1/A5' in order,
    A1_unchanged='**≤ 25,00 phút**' in g and '**≤ 25,00 phút**' in g3,
    A5_unchanged='**≤ 135,00**' in g and '**≤ 135,00**' in g3,
    H_python_blocks_unchanged=re.findall(r'```python\n(.*?)\n```', lo, re.S) == re.findall(r'```python\n(.*?)\n```', lo3, re.S),
    H_python_blocks=len(re.findall(r'```python\n(.*?)\n```', lo, re.S)),
    H_conditions_unchanged=re.findall(r'^\| Đ[1-5] \|.*$', lo, re.M) == re.findall(r'^\| Đ[1-5] \|.*$', lo3, re.M),
    H_conditions=len(re.findall(r'^\| Đ[1-5] \|.*$', lo, re.M)),
    H_explicit_old_denials_remaining=[phrase for phrase in ['**chưa được chọn**', '**ứng viên — chưa chọn**', '**không khai `§12` đã xong**'] if phrase in lo],
    H_preamble_history='Các bản lượt 4–7\n**không tự khai' in lo,
    H_preamble_current='CHỌN lựa chọn (1) — tiếp H**' in lo,
    H_table_current='**chủ kho CHỌN 07-09-2026 — lựa chọn 1** (mục §12; thi công chưa bắt đầu)' in lo,
    lease_current_noise=[s for s in lease['viec_trong_lease'] if 'nhiễu' in s])
assert report['a2_r3_r4_byte_identical'] and report['ordering_denies_old_baseline']
assert all(report[k] for k in ['A1_unchanged', 'A5_unchanged', 'H_python_blocks_unchanged', 'H_conditions_unchanged', 'H_preamble_history', 'H_preamble_current', 'H_table_current'])
assert not report['H_explicit_old_denials_remaining']

S = R / 'ops/reviews/pr468-hoso-4-packet-review-6-codex/nen-a1-a5'
steps = list(csv.DictReader((S / 'buoc.tsv').open(), delimiter='\t'))
jobs = list(csv.DictReader((S / 'job.tsv').open(), delimiter='\t'))
def triples(h):
    return {(r['step_name'], 'windows' if 'windows' in r['job_name'] else 'ubuntu', r['step_conclusion']) for r in steps if r['head7'] == h}
left, right = triples('426bfc0'), triples('1b3caa1')
report['same_tree_different_lane'] = dict(same_tree=git('rev-parse', '426bfc0^{tree}') == git('rev-parse', '1b3caa1^{tree}'),
    diff_paths=git('diff', '--name-only', '426bfc0', '1b3caa1').decode().splitlines(),
    before=len(left), after=len(right), added=sorted(right-left), removed=sorted(left-right),
    jobs=[{k: r[k] for k in ['run_id', 'head7', 'head_branch', 'event', 'job_name', 'started_at', 'completed_at']} for r in jobs if r['head7'] in ['426bfc0','1b3caa1']])
import datetime as dt
def minutes(r):
    return (dt.datetime.fromisoformat(r['completed_at']) - dt.datetime.fromisoformat(r['started_at'])).total_seconds() / 60
durations = {h: {('windows' if 'windows' in r['job_name'] else 'ubuntu'): minutes(r) for r in jobs if r['head7']==h} for h in ['426bfc0','1b3caa1']}
report['two_run_minutes'] = durations
report['two_run_job_deltas'] = {platform: abs(durations['426bfc0'][platform] - durations['1b3caa1'][platform]) for platform in ['windows','ubuntu']}
sample_heads = re.findall(r'^\| `([a-f0-9]{7})` \|', section(g, '### ĐO LẠI 2026-09-07', '#### Nền TRÔI'), re.M)
sample = [r for r in jobs if r['head7'] in sample_heads and 'windows' in r['job_name']]
values = [minutes(r) for r in sample]
report['sample11'] = dict(n=len(sample), master_push=sum(r['head_branch']=='master' and r['event']=='push' for r in sample),
    other_branch=sum(r['head_branch']!='master' for r in sample),
    min=min(values), max=max(values), range=max(values)-min(values), median=statistics.median(values), mean=statistics.mean(values),
    yaml_step_counts={h: len(yaml.safe_load(git('show', h+':.github/workflows/ci.yml'))['jobs']['gate']['steps']) for h in sample_heads})

# A text-only remedy, never an edit to a live lease or workflow.
old = '(lượt master 34048685345 = 111,08 để đối chiếu nhiễu)'
new = '(lượt master 34048685345 = 111,08 để đối chiếu lịch sử; cùng tree, khác event/lane, chưa tách được phần runner)'
assert lease_raw.count(old) == 1
fixed = lease_raw.replace(old, new)
fixed_lease = yaml.safe_load(fixed)
changed = [k for k in lease if lease[k] != fixed_lease[k]]
assert changed == ['viec_trong_lease']
assert len(lease['viec_trong_lease']) == len(fixed_lease['viec_trong_lease'])
changes = sum(a != b for a,b in zip(lease['viec_trong_lease'], fixed_lease['viec_trong_lease']))
assert changes == 1 and not any('đối chiếu nhiễu' in s for s in fixed_lease['viec_trong_lease'])
report['lease_remedy_model'] = dict(anchor_count=1, changed_keys=changed, changed_list_items=changes,
    authority_hashes_times_unchanged=all(lease[k]==fixed_lease[k] for k in ['lease_id','spec_hash','spec_sha256','granted_on_instruction','leased_at_utc','lease_expires_at_utc','write_set_hash','thay_the_cho']),
    A5_unchanged='≤ 135,00' in fixed)
(O / 'prose-experiment').mkdir(exist_ok=True)
(O / 'prose-experiment/lease-r4.yaml.txt').write_text(fixed)
(O / 'prose-experiment/README.md').write_text('chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit\n\nThử nghiệm văn bản ở bản sao reviewer; không phải lease đã được cấp lại.\n')
(O / 'prose-checks.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
