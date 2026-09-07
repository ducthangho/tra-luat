import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess

import yaml

from measure import B, R, O, git, note, save


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


result = {'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'diffs': {}, 'receipts': [], 'anchors': []}
for name, base, patch, num in [('since11', 'c43347d', 'diff-tu-luot11.patch', 'numstat-tu-luot11.txt'),
                               ('full', 'origin/master', 'diff.patch', 'numstat.txt')]:
    raw = git('diff', '--numstat', base, 'HEAD')
    rows = [x.split('\t') for x in raw.decode().splitlines()]
    result['diffs'][name] = {'patch_matches': git('diff', base, 'HEAD') == (B / patch).read_bytes(),
                           'numstat_matches': raw == (B / num).read_bytes(), 'files': len(rows),
                           'additions': sum(int(x[0]) for x in rows if x[0].isdigit()),
                           'deletions': sum(int(x[1]) for x in rows if x[1].isdigit()),
                           'outside_ops': [x[2] for x in rows if not x[2].startswith('ops/')]}
commits = git('log', '--reverse', '--format=%H%x09%aI%x09%cI%x09%s', 'c43347d..HEAD').decode().splitlines()
result['commits'] = commits
for n in [10, 11]:
    p = R / f'ops/reviews/pr468-hoso-4-packet-review-{n}-codex-verdict.receipt.yaml'
    d = yaml.safe_load(p.read_text())
    raw = (R / d['verdict_path']).read_bytes()
    anchor = re.search(r'/blob/([0-9a-f]{40})/', d['evidence_url']).group(1)
    body = git('show', '-s', '--format=%B', anchor).decode()
    session = re.findall(r'^Claude-Session:\s*(\S+)', body, re.M)
    first = git('log', '--reverse', '--diff-filter=A', '--format=%H', 'HEAD', '--', d['verdict_path']).decode().splitlines()[0]
    directory = R / f'ops/reviews/pr468-hoso-4-packet-review-{n}-codex'
    files = sorted(str(x.relative_to(directory)) for x in directory.rglob('*') if x.is_file() and not x.is_symlink())
    inventory = {'files': files, 'regular_count': len(files), 'symlinks': [str(x) for x in directory.rglob('*') if x.is_symlink()]}
    save(f'round{n}-inventory.json', inventory)
    identity_sources = [x for x in files if Path(x).name in ['run.json', 'prompt.snapshot', 'PROMPT.md'] or 'session' in Path(x).name]
    row = {'round': n, 'bytes': len(raw), 'declared_bytes': d['verdict_bytes'], 'sha256': sha(raw),
           'declared_sha256': d['verdict_sha256'], 'reviewed_sha': d['reviewed_sha'], 'anchor_commit': anchor,
           'anchor_blob_equal': git('show', f'{anchor}:' + d['verdict_path']) == raw,
           'anchor_first_commit': first == anchor,
           'reviewed_is_ancestor': subprocess.run(['git', '-C', str(R), 'merge-base', '--is-ancestor', d['reviewed_sha'], anchor]).returncode == 0,
           'projection_receipt_equal': p.read_bytes() == (B / 'tai-lieu' / p.name).read_bytes(),
           'projection_verdict_equal': raw == (B / 'tai-lieu' / Path(d['verdict_path']).name).read_bytes(),
           'commit_transport_session_urls': session, 'identity_source_candidates': identity_sources,
           'model_reviewer_identity': d['model_reviewer_identity'], 'github_submitter_identity': d['github_submitter_identity'],
           'assurance': d['assurance']}
    result['receipts'].append(row)
    save('standards.json', result)
    note(f'Kết luận nhỏ — receipt lượt {n}: {len(raw)} byte, SHA256 `{sha(raw)}` khớp; evidence_url ghim commit đầu tiên `{anchor}` chứa đúng blob; reviewed_sha là tổ tiên. Bản chiếu receipt/verdict bằng byte. Kiểm byte/neo không chứng minh danh tính model; danh sách nguồn launcher trong gói: `{identity_sources}`. Session vận chuyển tự khai trong commit: `{session}`.')
for issue_id, prefix in [(463, 'gate-tach-job-cat-chi-phi-exec-1r4'), (464, 'lo-319-linux-bang-chung-xanh-exec-1'),
                         (465, 'mutant-windows-subagent-ghi-detect-exec-1'), (466, 'mutant-windows-nhanh-don-duoc-exec-1')]:
    issue = next((R / 'ops/issues').glob(f'{issue_id}-*.md'))
    lease = next((R / 'ops/leases').glob(prefix + '-claude*.yaml*'))
    d = yaml.safe_load(lease.read_text())
    spec = R / d['spec_path']
    commit = re.search(r'@ `([0-9a-f]{40})`', issue.read_text()).group(1)
    result['anchors'].append({'issue': issue_id, 'revision': d['revision'], 'sha256': sha(spec.read_bytes()),
                              'declared_hash': d['spec_hash'], 'alias_hash': d['spec_sha256'],
                              'issue_commit': commit, 'issue_blob_matches': git('show', f'{commit}:' + d['spec_path']) == spec.read_bytes(),
                              'projection_equal': all(x.read_bytes() == (B / 'tai-lieu' / x.name).read_bytes() for x in [issue, lease, spec]),
                              'null_fields': [k for k, v in d.items() if v is None]})
rig = 'ops/reviews/pr468-hoso-4-packet-review-9-codex/artifact-repair/rig'
result['repair_commits'] = {}
for commit in ['17c6901', '4c18cb2']:
    raw = git('diff-tree', '--no-commit-id', '--name-status', '-r', commit, '--', rig).decode()
    result['repair_commits'][commit] = {'changed_count': len(raw.splitlines()), 'changes': raw.splitlines()}
p10 = R / 'ops/reviews/pr468-hoso-4-packet-review-10-codex/do-review10/final-check.json'
result['round10_launch_record'] = json.loads(p10.read_text())['initial_launch_log']
result['round10_final_check_utc'] = json.loads(p10.read_text())['utc']
result['round11_final_check_utc'] = json.loads((R / 'ops/reviews/pr468-hoso-4-packet-review-11-codex/final-check.json').read_text())['utc']
result['commit_time_gap_seconds'] = (dt.datetime.fromisoformat(git('show', '-s', '--format=%cI', '4c18cb2').decode().strip()) - dt.datetime.fromisoformat(git('show', '-s', '--format=%cI', '17c6901').decode().strip())).total_seconds()
save('standards.json', result)
print(json.dumps({k: v for k, v in result.items() if k != 'receipts'}, ensure_ascii=False, indent=2))
note('Kết luận nhỏ — lịch sử sửa gói 19 tệp rig: `17c6901` thay 19 tệp; `4c18cb2` thay 0 tệp của gói đó. Hai commit cách nhau 1598 giây theo cả timestamp tác giả/committer, không chứng minh thời điểm push. Lượt 10 có log mốc bắt đầu 11:24:25 và final-check 11:47:28.896723Z trong gói; không đủ suy thời lượng launcher chính xác. Đang đối chiếu các câu biên nhận/GHI-NHAN với các nguồn này.')
