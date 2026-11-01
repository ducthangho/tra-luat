import datetime
import importlib.util
import re
import sys
import yaml
from audit_common import *

d = yaml.safe_load((REPO / RECEIPT).read_text())
v = (SOURCE / 'VERDICT.md').read_bytes()
vt = v.decode()
r = json.loads((SOURCE / 'runs/71490d5a/run.json').read_text())
m = d['model_reviewer_identity']
checks = []

def check(name, actual, expected):
    checks.append(dict(name=name, actual=actual, expected=expected, ok=actual == expected))

def g(*args):
    return git(*args).decode().strip()

check('verdict', d['verdict'], vt.splitlines()[0].split(': ', 1)[1])
check('reviewed_sha/verdict', d['reviewed_sha'], vt.splitlines()[1].split(': ', 1)[1])
check('reviewed_sha/run', d['reviewed_sha'], r['head'])
check('reviewed_tree/git', d['reviewed_tree'], g('rev-parse', d['reviewed_sha'] + '^{tree}'))
check('verdict_sha256/source', d['verdict_sha256'], sha(v))
check('verdict_bytes/source', d['verdict_bytes'], len(v))
check('verdict_path/byte_source', (REPO / d['verdict_path']).read_bytes() == v, True)
check('receipt_id/suffix', d['receipt_id'], 'pr1075-review-1-codex-' + sha(v)[:8])
check('target_pr', d['target_pull_request'], 1075)
check('round', d['luot'], 1)
matches = re.findall(r'^- \[(P[0-3])\]\s+([^:]+):', vt, re.M)
counts = [sum(s == f'P{i}' for s, slug in matches) for i in range(4)]
for i, count in enumerate(counts):
    check(f'finding_count/P{i}', d[f'so_p{i}'], count)
    check(f'finding_summary/P{i}', f'{count} P{i}' in vt.splitlines()[3], True)
check('findings_ids', d['findings_ids'], [slug for s, slug in matches])
check('verdict_line4', 'approve — 0 P0, 0 P1, 0 P2, 0 P3' in vt.splitlines()[3], True)
parents = g('rev-list', '--parents', '-n', '1', d['land_merge_commit']).split()[1:]
check('land/two_parents', len(parents), 2)
check('land/second_parent', parents[1], d['reviewed_sha'])
check('land/ancestor_master', run(['git', 'merge-base', '--is-ancestor', d['land_merge_commit'], 'origin/master']).returncode, 0)
check('land/ancestor_HEAD', run(['git', 'merge-base', '--is-ancestor', d['land_merge_commit'], 'HEAD']).returncode, 0)
check('base/merge_base_with_first_parent', d['base_sha'], g('merge-base', d['reviewed_sha'], parents[0]))
check('source_DIFF.patch/git', git('diff', d['base_sha'], d['reviewed_sha']) == (SOURCE / 'DIFF.patch').read_bytes(), True)
urlmatch = re.fullmatch(r'https://github.com/ducthangho/tra-luat/blob/([0-9a-f]{40})/(.+)', d['evidence_url'])
check('evidence_url/form', bool(urlmatch), True)
anchor, blobpath = urlmatch.groups()
check('evidence_url/path', blobpath, d['verdict_path'])
check('evidence_url/ancestor_HEAD', run(['git', 'merge-base', '--is-ancestor', anchor, 'HEAD']).returncode, 0)
check('evidence_url/ancestor_receipt_commit', run(['git', 'merge-base', '--is-ancestor', anchor, '6af4c9a']).returncode, 0)
blob = git('show', anchor + ':' + blobpath)
check('evidence_url/blob_sha256', sha(blob), d['verdict_sha256'])
check('evidence_url/blob_bytes', len(blob), d['verdict_bytes'])
check('evidence_url/blob_equals_source', blob == v, True)
check('session_run_id', m['session_run_id'], r['run_id'])
check('run_json/path', json.loads((REPO / m['run_json']).read_text()), r)
check('launcher/run_json', json.loads((SOURCE / 'launcher.json').read_text()), r)
check('run/ma_thoat', r['ma_thoat'], 0)
check('run/trang_thai', r['trang_thai'], 'xong')
check('run/thoi_luong_giay', r['thoi_luong_giay'], 412.567)
delta = (datetime.datetime.fromisoformat(r['ket_thuc_utc']) - datetime.datetime.fromisoformat(r['bat_dau_utc'])).total_seconds()
check('run/duration_rounded', round(delta, 3), r['thoi_luong_giay'])
check('run/clean', r['worktree_sach'], True)
check('run/dirty_items', r['so_muc_ban'], 0)
check('run/provider', m['provider'], r['provider'])
check('run/historical_surface', m['surface'], r['execution_surface'])
check('run/transport', m['transport'], r['transport'])
check('run/prompt_hash', r['prompt_sha256'], sha((SOURCE / 'PROMPT.md').read_bytes()))
check('run/prompt_prefix_in_note', r['prompt_sha256'][:12] in m['run_json_ghi_chu'], True)
check('run/sandbox_status', r['sandbox_trang_thai'], 'DO_DUOC')
check('run/sandbox_observations_present', bool(r['sandbox_quan_sat']), True)
check('run/sandbox_sampling_limit_present', 'KHONG chung minh moi lenh' in r['sandbox_gioi_han'], True)
check('run/model_status', r['model_phuc_vu_trang_thai'], 'DO_DUOC')
events = r['model_phuc_vu']
models = sorted({x['model'] for x in events})
check('run/model_events', len(events), 19)
check('run/model_unique_response_ids', len({x['response_id'] for x in events}), 19)
check('run/model_event_types', sorted({x['su_kien'] for x in events}), ['response.created'])
for field in ['model', 'model_da_chay']:
    check('run/' + field, models, [m[field]])
check('run/model_evidence', m['model_evidence'], 'do_may')
check('run/model_evidence_ref', m['model_evidence_ref'], m['run_json'] + '#model_phuc_vu')
check('run/effort', r['effort_phuc_vu'], ['xhigh'])
check('run/effort_status', r['effort_phuc_vu_trang_thai'], 'DO_DUOC')
for token in ['19 su kien', 'gpt-6-astra', 'xhigh', 'DO_DUOC']:
    check('model_note/' + token, token in m['model_evidence_ghi_chu'], True)
for token in ['ma_thoat 0', 'trang_thai xong', '412.567', 'head 907c474', 'worktree_sach true', 'sandbox_trang_thai DO_DUOC']:
    check('run_note/' + token, token in m['run_json_ghi_chu'], True)
for stream in ['stdout', 'stderr']:
    b = (SOURCE / 'runs/71490d5a' / (stream + '.log')).read_bytes()
    check(stream + '/bytes', len(b), r[stream + '_byte'])
    check(stream + '/sha256', sha(b), r[stream + '_sha256'])
checkpoint_bytes = (SOURCE / 'runs/71490d5a/checkpoint.json').read_bytes()
checkpoint = json.loads(checkpoint_bytes)
check('checkpoint/hash', sha(checkpoint_bytes), r['checkpoint_sha256'])
for key, rkey in [('checkpoint_id', 'run_id'), ('head', 'head'), ('prompt_sha256', 'prompt_sha256')]:
    check('checkpoint/' + key, checkpoint[key], r[rkey])
paths = g('diff', '--name-only', d['base_sha'], d['reviewed_sha']).splitlines()
sys.path.insert(0, str(REPO / 'ops'))
spec = importlib.util.spec_from_file_location('independent_lease', REPO / 'ops/lease_publish.py')
lease = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lease)
klass = lease._tinh_lop_tu_write_set(paths)
check('review_class', d['review_class'], klass)
check('effective_review_class', d['effective_review_class'], klass)
check('review_class/path_count', len(paths), 58)
check('review_class/scope', all(p.startswith('ops/reviews/') for p in paths), True)
for token in ['58 tep', '3574cb0..907c474', klass]:
    check('class_note/' + token, token in d['review_class_ghi_chu'], True)
check('review_class/implementation_unchanged_since_reviewed', git('show', d['reviewed_sha'] + ':ops/lease_publish.py'), (REPO / 'ops/lease_publish.py').read_bytes())

# Measure the summary against the archived verdict and its supporting saved results;
# do not claim to rerun the older review for which nested source trees were not supplied.
historical_archive = json.loads((SOURCE / 'evidence/archive.json').read_text())
historical_receipt = json.loads((SOURCE / 'evidence/receipt.json').read_text())
historical_checks = json.loads((SOURCE / 'evidence/receipt-checks.json').read_text())
historical_readme = json.loads((SOURCE / 'evidence/readme-history.json').read_text())
historical_mutation = json.loads((SOURCE / 'evidence/mutation.json').read_text())
summary = {'copied': historical_archive['copied_equal'], 'omitted': len(historical_archive['omitted']),
           'receipt_checks': len(historical_checks), 'readme_added': len(historical_readme['added']),
           'readme_removed': len(historical_readme['removed']),
           'mutation_rc': historical_mutation['bien-nhan']['rc'],
           'mutation_red_receipts': historical_mutation['bien-nhan']['red_receipts']}
for k, expected in [('copied', 53), ('omitted', 2), ('receipt_checks', 75), ('readme_added', 4), ('readme_removed', 0), ('mutation_rc', 1)]:
    check('ket_luan/' + k, summary[k], expected)
check('ket_luan/receipt_count_consistent', historical_receipt['check_count'], len(historical_checks))
check('ket_luan/mutation_target', summary['mutation_red_receipts'], ['pr1071-review-1-codex-verdict.receipt.yaml'])
for token in ['0 finding', '53 tep', '2 tep', '75 doi chieu', '4 hang', 'dot bien bam']:
    check('ket_luan/token/' + token, token in d['ket_luan'], True)
for token in ['53 tệp', 'hai tệp', '75 đối chiếu', 'bốn hàng', 'Đột biến băm bị chặn']:
    check('ket_luan/verdict/' + token, token in vt.splitlines()[3], True)

fixed = ['schema_version', 'kind', 'packet_id', 'luot', 'role', 'provider', 'executor_provider',
         'cross_provider', 'review_class', 'effective_review_class', 'assurance', 'verdict',
         'nguon_tep', 'so_p0', 'so_p1', 'so_p2', 'so_p3', 'so_dem_theo', 'findings_ids',
         'independent_from_executor_session', 'review_axes', 'nguon_co_tham_quyen']
old = yaml.safe_load((REPO / 'ops/reviews/pr1071-review-1-codex-verdict.receipt.yaml').read_text())
fixed_differences = {k: {'old': old[k], 'new': d[k]} for k in fixed if old[k] != d[k]}
check('precedent/pr1071_fixed_fields', fixed_differences, {})
check('precedent/anchor_type', d['anchor']['loai'], old['anchor']['loai'])
check('precedent/anchor_strength', d['anchor']['cuong_do'], old['anchor']['cuong_do'])
check('precedent/caveat_ids', [x['id'] for x in d['verdict_usage_caveats']], [x['id'] for x in old['verdict_usage_caveats']])
check('precedent/caveat_severity', [x['muc'] for x in d['verdict_usage_caveats']], [x['muc'] for x in old['verdict_usage_caveats']])
for key in ['provider', 'surface', 'transport', 'model', 'model_da_chay', 'model_evidence']:
    check('precedent/identity/' + key, m[key], old['model_reviewer_identity'][key])
all_changed_fields = sorted(k for k in set(old) | set(d) if old.get(k) != d.get(k))

unmeasured = {
    'github': 'KHÔNG ĐO ĐƯỢC: live PR/CI, URL public serving, actor/credentials, actual API merge_method/expectedHeadSha; local graph only establishes a two-parent merge and its second parent.',
    'cli': 'KHÔNG ĐO ĐƯỢC: binary version 0.164.0, complete historical launcher argv/flags, requested model/effort; run.json records program/argument-count/fingerprint and served telemetry, not full argv.',
    'independence': 'KHÔNG ĐO ĐƯỢC: executor identity/family, owner instruction, absence of context reuse/fork beyond supplied run/prompt/checkpoint. No re-certification of cross_approved.',
    'sandbox': 'KHÔNG ĐO ĐƯỢC: enforcement for every historical command; saved sandbox_gioi_han explicitly limits DO_DUOC to samples.',
    'omitted_directories': 'KHÔNG ĐO ĐƯỢC: contents of original cay-kho/, work/, nguon/ excluded from supplied source; individual files in those directories are not inventoried here.',
}
# Replace very large equality values with their stable fingerprints in evidence.
for row in checks:
    for key in ['actual', 'expected']:
        if isinstance(row[key], bytes):
            row[key] = dict(bytes=len(row[key]), sha256=sha(row[key]))
        elif isinstance(row[key], dict) and len(json.dumps(row[key])) > 3000:
            row[key] = dict(json_sha256=sha(json.dumps(row[key], sort_keys=True).encode()))
errors = [x['name'] for x in checks if not x['ok']]
save('receipt-checks.json', checks)
out = dict(check_count=len(checks), errors=errors, reviewed_sha=d['reviewed_sha'], reviewed_tree=d['reviewed_tree'],
           land_merge_commit=d['land_merge_commit'], land_parents=parents,
           land_commit_date=g('show', '-s', '--format=%cI', d['land_merge_commit']), anchor=anchor,
           verdict_bytes=len(v), verdict_sha256=sha(v), finding_counts=counts,
           run_id=r['run_id'], ma_thoat=r['ma_thoat'], duration=r['thoi_luong_giay'], duration_from_timestamps=delta,
           model_events=len(events), models=models, effort=r['effort_phuc_vu'], prompt_sha256=r['prompt_sha256'],
           sandbox_status=r['sandbox_trang_thai'], review_class=klass, changed_count=len(paths),
           ket_luan_saved_source_counts=summary, precedent_fixed_fields=len(fixed),
           precedent_fixed_differences=fixed_differences, precedent_changed_fields=all_changed_fields,
           unmeasured=unmeasured)
save('receipt.json', out)
print(json.dumps(out, ensure_ascii=False, indent=2))
assert not errors
