import json
import re
from pathlib import Path

from measure import BASE, ROOT, OUT, PREV, SHA, git, note

paths=[
 'ops/reviews/pr468-hoso-4-packet-review-10-codex-verdict.receipt.yaml',
 'ops/reviews/pr468-hoso-4-packet-review-11-codex-verdict.receipt.yaml',
 'ops/reviews/pr468-hoso-4-packet-review-12-codex-verdict.receipt.yaml',
 'ops/reviews/README.md',
 'ops/reviews/GHI-NHAN-CROSS-REVIEW-LUOT5-KHONG-HOAN-TAT.md',
 'ops/reviews/DOC-READBACK-SAU-HAN-456.md',
]
rows=[]
for path in paths:
    lines=git('diff','--unified=0',PREV,SHA,'--',path).decode().splitlines()
    line_no=None
    for line in lines:
        m=re.match(r'@@ -\d+(?:,\d+)? \+(\d+)',line)
        if m:
            line_no=int(m[1]);continue
        if line_no is None: continue
        if line.startswith('+'):
            text=line[1:]
            if re.search(r'\d',text): rows.append({'path':path,'line':line_no,'text':text})
            line_no+=1
        elif line.startswith(' '):line_no+=1
evidence=(BASE/'EVIDENCE.md').read_text()
examples=['178/178','23631','536028','1166.934']
data={'command':'python3 -B do-review13/claims_inventory.py',
 'method':'git diff --unified=0 02b0b86..f77f198 over six edited receipt/README/incident/readback documents; select added lines containing a digit; manual classification afterwards',
 'limits':'Digit filter also matches SHA/date/IDs and misses numbers written as words, unchanged historical prose, omitted raw evidence, and semantics. Historical immutable artifacts are checked by hashes separately. Every omitted issue found by reviewer still counts as a finding.',
 'paths':paths,'candidate_count':len(rows),'candidates':rows,
 'examples_not_listed_in_evidence':{s:s not in evidence for s in examples},
 'evidence_declares_extraction_method':False,
 'evidence_declares_coverage_omissions':False}
(OUT/'claims-inventory.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
assert all(data['examples_not_listed_in_evidence'].values())
hint='''# Gợi ý bổ sung phương pháp cho EVIDENCE — dữ liệu reviewer

chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit

Trích ứng viên bằng `python3 -B do-review13/claims_inventory.py`: sáu tệp hồ sơ vừa đổi,
git diff --unified=0 từ 02b0b86 tới f77f198, lấy dòng thêm có chữ số rồi phân loại thủ công.
Bộ lọc bắt cả SHA/ngày/ID, bỏ sót số viết bằng chữ, câu không đổi và lỗi ngữ nghĩa;
hiện vật lịch sử bất biến được kiểm manifest riêng. Mọi mục bỏ sót mà reviewer phát hiện
vẫn được tính là finding. Executor phải xuất script/lệnh tương đương cùng gói kế tiếp.

Bổ sung bảng số 23631 B và manifest 178/178 (reviewer đã băm lại); 1166.934 s,
536028 B, prompt hash, model 6/6 và hai preflight rc=11 là lời khai vận chuyển;
gói chưa có raw run/session/prompt, KHÔNG ĐO ĐƯỢC độc lập. Không biến manifest/schema
xanh thành xác thực model hoặc quyền merge. Giữ nguyên receipt/verdict lịch sử.
'''
(OUT/'goi-y-evidence.md').write_text(hint)
note('Finding mới mức P3 `evidence-thieu-phuong-phap-trich-va-gioi-han-bao-phu`: EVIDENCE.md:14–20 khai giới hạn suite nhưng thiếu lệnh/cách trích danh sách khẳng định định lượng và phần bộ lọc bỏ sót theo protocol §8. Ví dụ 178/178,23631 B,536028 B,1166.934 s vắng bảng. Đã chạy claims_inventory.py, lưu danh sách ứng viên và thử bổ sung ở goi-y-evidence.md (chỉ scratch, nhãn chưa chạy trên cây thật). Reviewer đã kiểm riêng byte/manifest và ghi phần attestation KHÔNG ĐO ĐƯỢC, nên finding này không giữ P1/P2 mở.')
print(json.dumps({'candidate_count':len(rows),'omitted_examples':examples},ensure_ascii=False))
