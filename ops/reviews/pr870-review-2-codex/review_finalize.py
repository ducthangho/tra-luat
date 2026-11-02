#!/usr/bin/env python3
"""Format recorded evidence only; never write the reviewed checkout."""
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

OUT = Path(__file__).resolve().parent

def gate_summary():
    raw = (OUT / 'evidence-gates.txt').read_text()
    assert raw.count('\nRC=0\n') == 2 and raw.endswith('rc=0\n')
    print('python3 .claude/dev/packet_loop.py doctrine-scan --root .')
    print((OUT / 'doctrine-scan.stdout').read_text().strip())
    print('rc=0; KẾT LUẬN: passed')
    print('python3 scripts/tl.py doc-claims-check --json')
    data = json.loads((OUT / 'doc-claims-check.stdout').read_text())
    assert data['ok'] is True
    print('Các trường chọn từ JSON stdout gốc:')
    print(json.dumps({k: data[k] for k in ('ok', 'schema', 'files_scanned', 'flags', 'advisory_count', 'layers_skipped', 'strict')}, ensure_ascii=False, indent=2))
    print('rc=0; KẾT LUẬN: passed; ok=true; flags=[]')
    print('stderr_cả_hai=' + repr((OUT / 'doctrine-scan.stderr').read_text() + (OUT / 'doc-claims-check.stderr').read_text()))

def main():
    if '--gate-summary' in sys.argv:
        gate_summary()
        return
    spec = importlib.util.spec_from_file_location('review_probe', OUT / 'review_probe.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    current = (OUT / 'VERDICT.md').read_text()
    # Keep the setup failure as a measured limitation of the first harness attempt.
    setup_start = current.index('### HƯỚNG 6:')
    setup_end = current.index('### HƯỚNG 6:', setup_start + 1)
    (OUT / 'evidence-events-setup.md').write_text(current[setup_start:setup_end])
    # Preserve the full report as incrementally recorded before final formatting.
    (OUT / 'VERDICT.incremental.md').write_text(current)
    table = current[current.index('## BẢNG ĐO'):current.index('## BẢNG SĂN')]
    table = table.replace('5 workflow còn lại, toàn bộ 5 job ubuntu-latest', '5 workflow còn lại, toàn bộ 7 định nghĩa job ubuntu-latest')
    table = table.replace('matrix: expression_same_as_9e9a74b=True; ngày commit head = 22-10-2026 | Có', 'matrix: expression_same_as_9e9a74b=True; timestamp base/head cùng ngày 22-10-2026; không có transcript phép đo gốc | Snapshot khớp; ngày chạy gốc KHÔNG ĐO ĐƯỢC')
    # A repeated probe must not produce duplicate claim rows.
    unique = []
    seen = set()
    for line in table.splitlines():
        if line.startswith('| ') and line in seen:
            continue
        seen.add(line)
        unique.append(line)
    table = '\n'.join(unique) + '\n\n'
    # Make every measurement row point to the exact runnable probe mode.
    lines = []
    for line in table.splitlines():
        if line.startswith('| ') and not line.startswith('| khẳng định'):
            parts = line.split(' | ')
            if len(parts) == 4:
                measure = parts[2]
                modes = [name for name in module.META if re.search(r'(?<![\w-])' + re.escape(name) + r'(?![\w-])', measure)]
                if modes:
                    name = min(modes, key=lambda n: measure.index(n))
                    number = module.META[name][0]
                    parts[2] = f'`python3 ../review_probe.py {name}` (HƯỚNG {number}): ' + measure
                    line = ' | '.join(parts)
        lines.append(line)
    table = '\n'.join(lines) + '\n\n'
    # This runs a local summary of the real captured gate stdout; it does not rerun gates.
    summary = subprocess.run([sys.executable, str(OUT / 'review_finalize.py'), '--gate-summary'], text=True, capture_output=True, check=True)
    (OUT / 'evidence-gates-summary.txt').write_text(summary.stdout + 'summary_rc=0\n')
    content = f'''verdict: approve
reviewed_sha: {module.SHA}
Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.

reviewed_tree: 0fa694daf17e10c37fc3e61690531ade4bd528bf
base_sha: 9e9a74b2a396ef458d25c51a5563efafbb45ba0c
reviewer: codex
provider: openai_codex
execution_surface: codex_service (agent có công cụ shell; không phải ChatGPT Web)
transport: machine/tool-mediated
review_class: routine (tài liệu CLAUDE.md, không đổi workflow/runtime)
identity_limit: không có receipt độc lập xác minh model/session; không tự tạo trạng thái cross_approved/landed

Không phát hiện lỗi mới trong diff tại exact SHA. P2 `master-windows-bo-sot-dispatch` của lượt trước **ĐÃ VÁ THẬT** ở cả hai vị trí. Hai cổng bắt buộc passed. Giới hạn bằng chứng lịch sử được ghi riêng bên dưới; `approve` này không xác nhận những dữ kiện đã đánh dấu KHÔNG ĐO ĐƯỢC và không là biên nhận đủ điều kiện land.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| lớp/finding nguồn | SHA lượt trước | vị trí/biểu hiện | tự đo tại SHA lượt này | phân loại |
|---|---|---|---|---|
| master-windows-bo-sot-dispatch [P2] | b38fce83d0e97981012072ca2a2023ac726e5b2e | CLAUDE.md:169, lời khai Windows trên master chỉ từ launcher | HƯỚNG 2/5/11: push/master → Ubuntu; dispatch/master → Ubuntu+Windows; câu mới ghi rõ “tự động khi push master” | ĐÃ VÁ THẬT |
| cùng lớp, biểu hiện hệ quả tuyệt đối | cùng SHA | CLAUDE.md:173–174, “KHÔNG BAO GIỜ” mở rộng ra mọi gate | HƯỚNG 8/11/12: câu mới chỉ nói lượt PR/push ci.yml và ma trận hiện tại; giữ nguyên ngoại lệ dispatch/label và nghĩa vụ hai nền theo protocol | ĐÃ VÁ THẬT |

Một lớp nguồn, hai vị trí; 0 lớp/0 biểu hiện còn mở. Bản verdict lượt 1 được đọc từ object `7a2eecf:ops/reviews/pr870-review-1-codex-verdict.md` chỉ để nhận diện finding lịch sử. Mọi nội dung runtime đang chấm đều lấy từ `{module.SHA}`, không lấy master hoặc workflow tại commit sau làm chuẩn.

'''
    content += table
    content += '''## BẢNG SĂN

13 hướng độc lập/phép kiểm bên dưới giữ command và output thật. Tất cả command chạy với cwd=`cay-kho/`; script đo nằm ở `../review_probe.py`, đọc blob bằng `git show <exact SHA>:<path>`. Không import `ops/lease_publish_test.py`; chỉ trích nguyên hàm qua AST rồi compile hàm ấy. Không gọi mạng, không tạo/rerun Actions, không push, không sửa checkout. Bytecode tắt; cache của cổng đặt ngoài checkout qua `TL_CACHE_DIR=../gate-cache`.

'''
    for name, (number, title, hypothesis, conclusion) in sorted(module.META.items(), key=lambda item: item[1][0]):
        evidence = (OUT / f'evidence-{name}.txt').read_text()
        assert evidence.endswith('rc=0\n'), (name, evidence[-200:])
        content += f'### HƯỚNG {number}: {title}\n\nGiả thuyết: {hypothesis}\n\nLệnh (cwd=`cay-kho/`):\n\n```bash\nPYTHONDONTWRITEBYTECODE=1 python3 ../review_probe.py {name}\n```\n\n'
        if name == 'gates':
            content += '''Hai command thực thi trong probe (rc thật được lưu cùng stdout/stderr):

```bash
python3 .claude/dev/packet_loop.py doctrine-scan --root .
python3 scripts/tl.py doc-claims-check --json
```

Output tóm từ log thật, đo lại bằng lệnh `PYTHONDONTWRITEBYTECODE=1 python3 ../review_finalize.py --gate-summary` (rc=0):

```text
'''
            content += summary.stdout + '```\n\nStdout đầy đủ: [doctrine-scan.stdout](doctrine-scan.stdout), [doc-claims-check.stdout](doc-claims-check.stdout); cả command, rc, stdout/stderr nguyên bản: [evidence-gates.txt](evidence-gates.txt). Có 381 advisory và `flags=[]`; không biến advisory thành failure hoặc suy scanner sạch là đủ mọi kiểm tra ngữ nghĩa.\n\n'
        else:
            content += 'Output thật:\n\n```text\n' + evidence + '```\n\n'
        if name == 'events':
            content += 'Ghi nhận setup: lần dựng thước đầu tiên rc=1 do so sánh chuỗi `if` chưa bỏ wrapper `${{ ... }}`. Đó là lỗi harness của reviewer; sau khi chuẩn hóa wrapper, phép đo trên nguyên blob được chạy lại và rc=0 như trên. Output lỗi ban đầu giữ tại [evidence-events-setup.md](evidence-events-setup.md); không tính nó là lỗi repository. Ngữ nghĩa event mặc định chỉ đối chiếu YAML/lịch sử cục bộ; không kích hoạt server GitHub.\n\n'
        if name == 'history':
            content += 'Các SHA và chuỗi trích dẫn đã đo khớp. Phần chưa đo được trực tiếp là nội dung/actor/severity của comment r4323607674 và liên kết số PR865. Object sửa 4ae43f0 có trước head nhưng không phải ancestor: nó chỉ xác nhận tồn tại một bản sửa, không chứng minh biên bản trong cây review đã được sửa. Câu “sửa ở PR #865” không được đọc thành “PR đó đã merge vào cây này”. Không có phản chứng đủ để tạo finding mới từ việc thiếu readback.\n\n'
        if name == 'historical':
            content += '“Đợt” sáu merge không được định danh thành sáu run trong Git. Lịch sử còn nhiều merge khác cùng ngày, nên không tự đồng nhất “đợt” với cả ngày hoặc kết luận con số sai chỉ bằng số commit. Phạm vi “nay ... không lần nào” được đọc cùng câu hệ quả đã giới hạn vào PR/push của ci.yml; launcher đã nêu riêng cùng điều kiện paths.\n\n'
        if name == 'sandbox_end':
            content += 'Snapshot [trước](review-snapshot-before.json) / [sau](review-snapshot-after.json) bao gồm hash nội dung mọi tệp trong checkout, symlink và HEAD/index/config/packed-refs, cùng diff/index và trạng thái tracked/untracked/ignored. Đây là đối chiếu hai mốc quan sát, không phải chứng minh toàn lịch sử process chưa từng ghi rồi hoàn nguyên; filesystem vẫn là workspace-write theo môi trường được giao.\n\n'
        content += f'Kết luận: **{conclusion}**.\n\n'
    content += '''## FINDING MỚI

Không có finding mới P0/P1/P2/P3 trên diff đang chấm. Không tạo `HINT.patch` vì không có bản vá cần đề xuất. Phần quote finding P2 trong HƯỚNG 11 là lịch sử đã đóng, không phải finding còn mở.

## CỔNG VÀ GIỚI HẠN KẾT LUẬN

- `python3 .claude/dev/packet_loop.py doctrine-scan --root .`: **passed, rc=0**, sạch 10 tệp, 0 chỗ chép doctrine.
- `python3 scripts/tl.py doc-claims-check --json`: **passed, rc=0, "ok": true, flags=[]**, `layers_skipped={}`. Không chạy lại full selftest hoặc gate Windows thật vì diff chỉ là tài liệu và yêu cầu không mạng.
- **KHÔNG ĐO ĐƯỢC độc lập:** raw comment r4323607674/identity/severity, ánh xạ PR865 bằng PR readback, raw finding P2 PR109, ngày tác giả thực sự chạy phép đo 22-10, phạm vi sáu run/nhãn/dispatch và Windows “đầu tiên” ngày 14-08, quan hệ nhân quả giữa doctrine cũ và ý định executor. Các mục này có lệnh tìm kiếm/đối chứng trong bảng; không dùng lời kể thay bằng chứng.
- Phép chạy evaluator chứng minh cấu hình chọn runner, không chứng minh một run Windows đã được tạo, được cấp runner, hoàn tất hoặc passed. Readback run39354156843 chỉ xác nhận dữ liệu cục bộ đã lưu; không đo API hiện tại hay đủ bốn mốc CI provenance để cấp land.
- Checkout giữ nguyên SHA/tree/index/nội dung: **4.843 tệp**, `added=[]`, `removed=[]`, `changed=[]`, trạng thái kể cả ignored rỗng. Báo cáo và evidence chỉ nằm ngoài `cay-kho/`.
'''
    (OUT / 'VERDICT.md').write_text(content)
    print(summary.stdout)
    print('WROTE VERDICT.md: approve; 13 hướng; P2 cũ đã đóng; 0 finding mới.')
    print('HINT.patch exists=' + str((OUT / 'HINT.patch').exists()))

if __name__ == '__main__':
    main()
