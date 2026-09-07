import copy
import datetime as dt
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import yaml

sys.dont_write_bytecode = True
B = Path(__file__).resolve().parents[1]
R = B / 'cay-kho'
O = B / 'do-review10'

def git(*args):
    return subprocess.check_output(['git', '-C', str(R), *args])

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def save(name, data):
    (O / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

report = {'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
          'head': git('rev-parse', 'HEAD').decode().strip(),
          'tree': git('rev-parse', 'HEAD^{tree}').decode().strip(),
          'status': git('status', '--porcelain').decode(),
          'abbrev': git('config', 'core.abbrev').decode().strip(),
          'shallow': git('rev-parse', '--is-shallow-repository').decode().strip(),
          'remote': git('remote', 'get-url', 'origin').decode().strip()}
report['diffs'] = {}
for key, base, patch, num in [('since9', '0bc6e56', 'diff-tu-luot9.patch', 'numstat-tu-luot9.txt'),
                             ('full', 'origin/master', 'diff.patch', 'numstat.txt')]:
    nums = git('diff', '--numstat', base, 'HEAD')
    rows = [r.split('\t') for r in nums.decode().splitlines()]
    report['diffs'][key] = dict(patch_matches=git('diff', base, 'HEAD') == (B / patch).read_bytes(),
                               numstat_matches=nums == (B / num).read_bytes(), files=len(rows),
                               additions=sum(int(r[0]) for r in rows if r[0].isdigit()),
                               deletions=sum(int(r[1]) for r in rows if r[1].isdigit()),
                               outside_ops=[r[2] for r in rows if not r[2].startswith('ops/')])

spec = importlib.util.spec_from_file_location('lease_review10', R / 'ops/lease_publish.py')
L = importlib.util.module_from_spec(spec)
spec.loader.exec_module(L)
leases = L._quet_lease_toan_kho(R, doi_chieu_ref=False)
report['snapshot_blob_path_pairs'] = len(leases)
ids = ['mutant-khong-chay-tren-windows-exec-1-claude-20260906'] + [
    f'gate-tach-job-cat-chi-phi-exec-{v}-claude-20260906' for v in ['1', '1r2', '1r3', '1r4']]
local = [yaml.safe_load((R / f'ops/leases/{i}.yaml').read_text()) for i in ids]
report['chain_current_tree'] = []
for d in local:
    report['chain_current_tree'].append(dict(lease_id=d['lease_id'], replaces=d.get('thay_the_cho'),
        tombstone=d.get('da_bi_thay_the'), bidirectional=L._bia_mo_doi_xung(d, [{'lease': x} for x in local])))
for old, new in zip(local, local[1:]):
    assert old['da_bi_thay_the'] == new['lease_id']
    assert old['lease_id'] in L._danh_sach_thay_the_cho(new['thay_the_cho'])
report['chain_snapshot'] = [{k: r[k] for k in ['ref', 'path', 'blob']} | dict(
    lease_id=r['lease']['lease_id'], replaces=r['lease'].get('thay_the_cho'),
    tombstone=r['lease'].get('da_bi_thay_the'), status=L._phan_loai_lease(r['lease']),
    bidirectional=L._bia_mo_doi_xung(r['lease'], leases))
    for r in leases if r['lease'].get('lease_id') in ids]

def holders(rs, when):
    found = {}
    for path in ['.github/workflows/ci.yml', '.claude/dev/ci_dang_ky_test.py']:
        rows = []
        for r in rs:
            d = r['lease']
            if L._lease_cham_duong(d, path) and L._phan_loai_lease(d, dt.datetime.fromisoformat(when)) == 'CÒN_HẠN':
                bm = L._bia_mo_doi_xung(d, rs)
                assert bm is not False
                if bm is None:
                    rows.append({k: r[k] for k in ['ref', 'blob', 'path']} | {'lease_id': d['lease_id']})
        found[path] = dict(count=len({r['lease_id'] for r in rows}), active_blobs=rows)
    return found

report['holders'] = {t: holders(leases, t) for t in [report['utc'],
    '2026-09-07T14:30:06+00:00', '2026-09-07T14:30:07+00:00', '2026-09-07T14:30:08+00:00']}
model = copy.deepcopy(leases)
for r in model:
    if r['lease'].get('lease_id') == ids[0]:
        r['lease']['da_bi_thay_the'] = ids[1]
report['model_all_456_copies_tombstoned'] = holders(model, report['utc'])
report['master_old_blob'] = git('rev-parse', f'origin/master:ops/leases/{ids[0]}.yaml').decode().strip()
save('snapshot.json', report)
print(json.dumps({k: v for k, v in report.items() if k not in ['chain_snapshot', 'holders']}, ensure_ascii=False, indent=2))
print('holders:', {t: {p: d['count'] for p, d in paths.items()} for t, paths in report['holders'].items()})

anchors = []
prefixes = ['gate-tach-job-cat-chi-phi-exec-1r4', 'lo-319-linux-bang-chung-xanh-exec-1',
            'mutant-windows-subagent-ghi-detect-exec-1', 'mutant-windows-nhanh-don-duoc-exec-1']
for issueid, prefix in zip([463, 464, 465, 466], prefixes):
    issue = next((R / 'ops/issues').glob(f'{issueid}-*.md'))
    text = issue.read_text()
    frozen = re.search(r'@ `([0-9a-f]{40})`', text).group(1)
    lp = next((R / 'ops/leases').glob(prefix + '-claude*.yaml*'))
    d = yaml.safe_load(lp.read_text())
    p = R / d['spec_path']
    row = dict(issue=issueid, lease=lp.name, revision=d['revision'], issue_commit=frozen,
        hash_actual=sha(p.read_bytes()), hash_declared=d['spec_hash'], hash_alias=d['spec_sha256'],
        issue_blob_hash=sha(git('show', frozen + ':' + d['spec_path'])), hash_in_issue=d['spec_hash'] in text,
        copies_equal=all(f.read_bytes() == (B / 'tai-lieu' / f.name).read_bytes() for f in [p, lp, issue]),
        null_keys=[k for k, v in d.items() if v is None], grant=d['granted_on_instruction'])
    anchors.append(row)
    if issueid == 463:
        anchors.append(dict(gate_lease_fields={k: d[k] for k in ['leased_at_utc', 'lease_expires_at_utc',
            'heartbeat_at', 'lease_until', 'run_minutes', 'base_sha', 'start_from_sha',
            'reviewed_sha_required', 'write_set', 'write_set_hash', 'thay_the_cho']},
            duration_minutes=(dt.datetime.fromisoformat(d['lease_until']) - dt.datetime.fromisoformat(d['leased_at_utc'])).total_seconds() / 60,
            write_hash_actual=sha(('\n'.join(sorted(d['write_set'])) + '\n').encode())))
receipt_path = R / 'ops/reviews/pr468-hoso-4-packet-review-9-codex-verdict.receipt.yaml'
d = yaml.safe_load(receipt_path.read_text())
raw = (R / d['verdict_path']).read_bytes()
anchor = re.search('/blob/([0-9a-f]{40})/', d['evidence_url']).group(1)
receipt = dict(schema=d['schema_version'], reviewed_sha=d['reviewed_sha'],
    declared_bytes=d['verdict_bytes'], actual_bytes=len(raw), declared_hash=d['verdict_sha256'], actual_hash=sha(raw),
    anchor_commit=anchor, anchor_blob_matches=git('show', anchor + ':' + d['verdict_path']) == raw,
    copy_equal=receipt_path.read_bytes() == (B / 'tai-lieu' / receipt_path.name).read_bytes(),
    identity_fields={k: d[k] for k in ['model_reviewer_identity', 'github_submitter_identity', 'anchor']})
save('anchors.json', dict(specs=anchors, receipt=receipt))
print('anchors:', json.dumps(anchors, ensure_ascii=False, indent=2))
print('receipt:', {k: v for k, v in receipt.items() if k != 'identity_fields'})
