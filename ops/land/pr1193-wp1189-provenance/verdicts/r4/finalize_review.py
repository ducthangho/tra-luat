"""Finish the offline report only after all measured requirements pass."""
import hashlib
import json
from pathlib import Path

import review_checks as r


def main():
    state = r.state()
    ids = {p['id']: p for p in state['phep_do']}
    required = ['snapshot-initial', 'static', 'python-tools', 'A1', 'A3-shellcheck',
                'A3-actionlint-version', 'A3', 'A5-diff-check', 'doctrine-scan',
                'doc-claims-check', 'spec-effects', 'master-ancestor', 'A4-numstat',
                'A2', 'A2-positive-evidence', 'snapshot-final']
    for key in required:
        assert key in ids and ids[key]['rc'] == 0 and ids[key]['trang_thai'] == 'passed', key
    assert r.git('rev-parse', 'HEAD').stdout.decode().strip() == r.HEAD
    assert not ids['snapshot-final']['ket_qua']['changed_sections']
    assert not any(p.get('status') != 'closed' for p in state['findings'])
    assert state['findings_moi'] == []
    positive = json.loads((r.EVIDENCE / 'A2-positive-evidence.json').read_text())
    state['verdict'] = 'approve'
    state.pop('tong_hop_tam', None)
    state['moi_truong'].update(python='3.12.3', PyYAML='6.0.3', actionlint='1.7.7', shellcheck='0.9.0')
    for label, desc in [
        ('A5-selftest', 'Không chạy python scripts/tl.py --selftest: không thuộc danh sách phải chạy lại của prompt.snapshot lượt 4; không nhận là pass.'),
        ('A6', 'Không chạy LIVE GitHub Actions sau land; thuộc phiên điều phối, ngoài phạm vi offline và user cấm gọi GitHub.'),
        ('Windows', 'not_run trong review offline này. Bộ phân loại thực của ADR-0060 M3 trả required do diff chạm workflow; không tuyên bố not_required hoặc đã đạt Windows.'),
        ('kiem-merge-full', 'Không chạy toàn lệnh vì K0 gọi git ls-remote; chỉ đo K1 cô lập bằng chính hàm thật/real local Git. Không kết luận K0/K2–K7 đạt.'),
    ]:
        state['phep_do'].append(dict(id=label, rc=None, trang_thai='not_run', ket_qua=desc))
    state['gioi_han'] = [
        'Đây là approve nội dung trong phạm vi review OFFLINE lượt 4 trên exact SHA; không phải quyền push/merge/land hoặc bằng chứng required CI/connector.',
        'A5 selftest tl.py, Windows và A6 LIVE không chạy trong lượt này; không biến not_run thành passed. Windows classifier thực trả required; điều kiện đó thuộc quy trình merge ngoài lượt offline.',
        'Không fetch hoặc gọi GitHub. OID master 358451e80b573d148807717bece3fd973915fbad do prompt cung cấp đã được đo ancestry/tree cục bộ; chưa xác minh master hiện tại trên remote.',
        'doctrine-scan mặc định quét 10 adapter/CLAUDE.md, không quét ops/specs. doc-claims-check mặc định quét 123 tệp từ 6 gốc, không quét ops/specs. Không diễn giải hai kết quả đó thành chứng minh mọi nội dung đặc tả đúng ngữ nghĩa.',
        'Model family GPT-6 theo runtime; không đo độc lập model ID/effort, session hoặc launcher bên ngoài. Không tự tạo receipt assurance.',
        'Snapshot toàn bộ path/hash/mode/symlink/thư mục gồm tracked/untracked/ignored và .git tại đầu/cuối không đổi. Đây là so hai mốc, không chứng minh chưa từng ghi rồi hoàn nguyên. Sandbox thực tế workspace-write; reviewer đối xử cay-kho read-only.',
    ]
    state['tong_hop'] = dict(
        P0_mo=0, P1_mo=0, P2_mo=0, P3_mo=0, P3_dong=1,
        F1='closed; ĐÃ VÁ THẬT; không tái diễn',
        ancestry='master 358451e là tổ tiên của reviewed_sha; rc=0',
        merge='Sạch về nội dung: tree dựng từ master + workflow đã approve bằng tree ccf7790; 109 path thay đổi đều khớp master, 107 thêm/2 sửa trong ops/land/.',
        spec='6121 byte/78 dòng; SHA-256 8f4f89a1414fd009f5a16be358925332c6c576a132710f5819e5cce7e778f5ce; bằng byte SPEC.md',
        A1='DAT; rc=0', A2=positive,
        A3='actionlint rc=0; version 1.7.7; ShellCheck 0.9.0 có mặt',
        A4='Đúng 2 tệp theo chỉ thị lượt 4: workflow +8/-0, đặc tả +78/-0; patch workflow bằng byte lượt 2/3',
        A5='git diff --check rc=0; selftest tl.py not_run',
        other_gates='doctrine-scan rc=0 (10 tệp/0 hit); doc-claims strict rc=0, ok=true, flags=[], 123 tệp, 0 lớp skipped; K1 cô lập rc12→0; CI day_du; đặc tả không vào release',
        Windows='required theo classifier; not_run trong phạm vi offline này',
        A6='not_run; LIVE sau land thuộc điều phối',
        checkout_cuoi='11443 tệp và 920 thư mục không đổi; HEAD/tree/status/index/worktree/.git không đổi tại hai mốc',
    )
    state['ket_luan'] = (
        'Approve nội dung exact SHA 275869169e134758bb145565d28f0b0897a92f87 theo chỉ thị review OFFLINE lượt 4. '
        'Đủ bằng chứng dương cho mọi phép đo bắt buộc của lượt này; bản vá workflow không đổi so với lượt đã approve, '
        'merge chỉ đưa đúng nội dung master vào, đặc tả được chép đúng byte/hash và không làm đỏ các chốt liên quan đã đo. '
        'Không có finding P0/P1/P2/P3 mới hoặc còn mở. Không sửa cay-kho/, không push, không gọi GitHub. '
        'Verdict này không thay điều kiện Windows, CI/connector, A6 hoặc approval merge/land.'
    )
    state['hoan_tat_utc'] = r.now()
    r.write_state(state)
    paths = [p for p in r.EVIDENCE.iterdir() if p.is_file() and p.name != 'artifact-hashes.json']
    paths += [r.ROOT / x for x in ['VERDICT.md', 'SPEC.md', 'a1_check.py', 'VERDICT_luot3.md',
                                  'review_checks.py', 'review_spec_effects.py', 'finalize_review.py']]
    manifest = {p.relative_to(r.ROOT).as_posix(): {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                for p in sorted(paths)}
    r.dump(r.EVIDENCE / 'artifact-hashes.json', manifest)
    check = r.state()
    assert check['verdict'] == 'approve' and check['reviewed_sha'] == r.HEAD
    print(json.dumps({'verdict': check['verdict'], 'reviewed_sha': r.HEAD,
                      'A2': positive['tong_ket'], 'report': str(r.ROOT / 'VERDICT.md'),
                      'report_sha256': manifest['VERDICT.md']['sha256']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
