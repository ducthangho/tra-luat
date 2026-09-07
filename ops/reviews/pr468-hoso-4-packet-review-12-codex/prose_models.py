import json
from pathlib import Path
import re
import subprocess

import yaml

from measure import B, R, O, git, note, save

# Experiments in memory only. No patched lease/receipt/authority file is emitted.
checks = {}
p = R / 'ops/reviews/pr468-hoso-4-packet-review-10-codex-verdict.receipt.yaml'
raw = p.read_text()
session = re.search(r'^Claude-Session:\s*(\S+)', git('show', '-s', '--format=%B', '17c6901').decode(), re.M).group(1)
anchor = 'verdict/gói: phiên khác (commit 17c6901, không rõ session URL)'
time_anchor = 'lượt này chạy 11:35–11:50Z, trước mốc ấy;'
assert raw.count(anchor) == raw.count(time_anchor) == 1
repaired = raw.replace(anchor, 'verdict/gói: session URL tự khai trong trailer Claude-Session của commit 17c6901: ' + session)
repaired = repaired.replace(time_anchor, 'gói lượt 10 lưu log bắt đầu 11:24:25Z và final-check 11:47:28.896723Z; thời lượng launcher chính xác KHÔNG ĐO ĐƯỢC; cả hai mốc trước hạn;')
old, new = yaml.safe_load(raw), yaml.safe_load(repaired)
changed = [k for k in old if old[k] != new[k]]
assert set(changed) == {'github_submitter_identity', 'KHONG_do_duoc'}
assert old['model_reviewer_identity'] == new['model_reviewer_identity']
assert old['assurance'] == new['assurance'] == 'review_deferred'
assert old['verdict'] == new['verdict'] == 'changes_requested'
checks['receipt10'] = {'session_anchor_count': raw.count(anchor), 'time_anchor_count': raw.count(time_anchor),
                       'changed_top_level_fields': changed, 'reviewer_identity_unchanged': True,
                       'verdict_hash_and_anchor_unchanged': all(old[k] == new[k] for k in ['verdict', 'verdict_path', 'verdict_sha256', 'verdict_bytes', 'reviewed_sha', 'evidence_url', 'anchor']),
                       'assurance_unchanged': True, 'source_session': session}
p = R / 'ops/reviews/pr468-hoso-4-packet-review-11-codex-verdict.receipt.yaml'
raw = p.read_text()
header = '# gói lượt 9 thiếu 19 tệp rig/ đã phục dựng) vá ở commit chứa verdict này.'
desc = '(commit chứa verdict lượt 11 + bản vá 2 P2)'
assert raw.count(header) == raw.count(desc) == 1
repaired = raw.replace(header, '# gói lượt 9 thiếu 19 tệp rig/ đã phục dựng): 19 tệp đã được bổ sung ở 17c6901; commit chứa verdict11 sửa câu billing và kiểm lại gói 69/69.')
repaired = repaired.replace(desc, '(commit chứa verdict lượt 11 + bản sửa billing; gói 19 tệp đã sửa ở 17c6901)')
old, new = yaml.safe_load(raw), yaml.safe_load(repaired)
changed = [k for k in old if old[k] != new[k]]
assert changed == ['evidence_url_ghi_chu']
checks['receipt11'] = {'header_anchor_count': 1, 'description_anchor_count': 1,
                       'changed_top_level_fields': changed, 'identity_assurance_verdict_unchanged': True}
p = R / 'ops/reviews/GHI-NHAN-CROSS-REVIEW-LUOT5-KHONG-HOAN-TAT.md'
raw = p.read_text()
anchors = ['khi vận chuyển vì lượt 10 kia đã lên nhánh trước 5 giây (`DOC-MANIFEST.md` trong gói ghi rõ).',
           'phỏng). Hai P2 vá ngay trong commit chứa verdict lượt 11.']
assert all(raw.count(x) == 1 for x in anchors)
checks['incident_note'] = {'unique_anchors': len(anchors),
                           'correction_direction': 'Ghi thứ tự commit đã đo, bỏ độ chênh push chưa có log; tách 19 tệp tại17c6901 và billing tại4c18cb2; giữ mô tả hai phiên độc lập.'}
save('prose-models.json', checks)
print(json.dumps(checks, ensure_ascii=False, indent=2))
note('Thử sửa hồ sơ trong bộ nhớ rc=0: receipt10 có 2 mỏ neo duy nhất; chỉ thay github_submitter_identity (phần prose nguồn vận chuyển) và KHONG_do_duoc (khung giờ), giữ nguyên model reviewer/assurance/verdict/băm/neo. Receipt11 có 2 mỏ neo duy nhất, chỉ 1 trường YAML ghi chú đổi; identity/assurance/verdict nguyên. GHI-NHAN có 2 mỏ neo duy nhất để sửa hướng. Không xuất bản vá authority/receipt; đây là phản chứng dữ liệu, executor tự tái dẫn xuất. Kết quả `do-review12/prose-models.json`.')

coverage = {}
for name in ['cay-kho', 'kho.git']:
    path = B / name
    raw = subprocess.check_output(['git', '-C', str(path), 'for-each-ref', '--format=%(refname)%09%(objectname)%09%(symref)'])
    (O / (name.replace('.', '-') + '-refs.tsv')).write_bytes(raw)
    head_refs = []
    remote_names = []
    for line in raw.decode().splitlines():
        ref, oid, sym = line.split('\t')
        if ref.startswith('refs/heads/') and not ref.endswith('/HEAD'):
            head_refs.append(ref.removeprefix('refs/heads/'))
        if ref.startswith('refs/remotes/origin/') and not ref.endswith('/HEAD'):
            remote_names.append(ref.removeprefix('refs/remotes/origin/'))
    coverage[name] = {'head_names': head_refs, 'remote_names': remote_names}
historical = json.loads((R / 'ops/reviews/pr468-hoso-4-packet-review-10-codex/do-review10/leases.json').read_text())
old_names = set(historical['old456_branches']) - {'HEAD'}
provided_names = set(coverage['kho.git']['head_names'])
coverage['historical_reference_only'] = {'round10_measurement_utc': historical['measured_at_utc'],
                                        'historical_old_blob_branch_count': len(old_names),
                                        'historical_old_blob_names_missing_now': sorted(old_names - provided_names),
                                        'caveat': 'Không gọi tên lịch sử là nhánh máy chủ hiện hành; chỉ chứng minh gói lịch sử biết tên mà mirror hiện tại không có.'}
save('ref-coverage.json', coverage)
print(json.dumps(coverage, ensure_ascii=False, indent=2))
