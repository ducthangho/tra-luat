# HANDOFF — `DOCTRINE-SCAN-DAO-SANG-DANH-SACH-CHO-PHEP` (#543), revision 1, generation 1 (Vá Review Lượt 1)

## 0. Khối bàn giao schema-v1 (protocol §7)

```yaml
schema_version: 1
packet_id: DOCTRINE-SCAN-DAO-SANG-DANH-SACH-CHO-PHEP        # Issue #543
generation: 1
revision: 1
lease_id: doctrine-scan-r1-g1-antigravity
spec_hash: 60dbefa1f617be36ecd4ac93743d9def0ddc063f06ae09e7af0e002c7c80b0cf
provider: google_antigravity
role: executor
execution_surface: antigravity
transport: machine/local
base_sha: dd274415408bd1c6b4279c8e2cf9671057520f23
head_sha: a7431897fb82acd6f1e02bb15e71cc87655804e0
tree_oid: 2b1c2be6d4c7139a6f6df92b4e79c8e912e8e090
branch: agy/doctrine-scan-r1-g1
status: ready_for_review
summary: >-
  Giải quyết trọn vẹn 5 lớp finding trong verdict lượt 1 của Reviewer Claude (PR #545).
  Fail-close toàn bộ 4 cửa đọc protocol nguồn; bỏ fallback ngoài --root; chuẩn hoá
  _repo_gia với protocol trung tính; sửa ca test §12 sang đoạn văn xuôi thuần không
  dính 28 cụm cấm; cập nhật mutant bo_kiem_chep_protocol giết cả 3 ca; bổ sung giải trình
  số liệu ngưỡng 15 cho CLAUDE.md; chuyển handoff note ra tầng đầu ops/reviews/ theo r374.
changed_paths:
  - .claude/dev/packet_loop.py
  - .claude/dev/packet_loop_test.py
  - ops/reviews/doctrine-scan-handoff-r1-g1-antigravity.md
tests:
  - name: doctrine-scan trên toàn kho (10 tệp)
    command: python .claude/dev/packet_loop.py doctrine-scan --root .
    exit_code: 0
    status: passed
    evidence: 'sạch — đã quét 10 tệp, 0 chỗ chép doctrine'
  - name: adr-song
    command: python .claude/dev/packet_loop.py adr-song --root .
    exit_code: 0
    status: passed
    evidence: 'sạch — 48 ADR trên đĩa, 48 dòng trong §20, khớp 1–1'
  - name: git diff --check
    command: git diff --check
    exit_code: 0
    status: passed
    evidence: 'sạch'
  - name: doc-claims-check --strict
    command: python scripts/tl.py doc-claims-check --strict
    exit_code: 0
    status: passed
    evidence: '0 lỗi vi phạm (by_layer all 0)'
  - name: release-verify --strict
    command: python scripts/tl.py release-verify --strict RELEASE_MANIFEST.json
    exit_code: 0
    status: passed
    evidence: 'package_hash_match: true, errors: []'
  - name: 13 ca test doctrine-scan (bao gồm 4 ca fail-close mới)
    command: python packet_loop_test.py (chạy độc lập qua Ctx)
    exit_code: 0
    status: passed
    evidence: '13/13 ca ĐẠT: sach_xanh, bom_cum, THAT, repo_that, chep_5_1 (rc=6), chep_5_1_ngan (rc=6), chep_12 (rc=6), fail_close_thieu (rc=2), fail_close_utf8 (rc=2), fail_close_ngan (rc=2), fail_close_fence (rc=2), adr_48 (rc=0), con_tro (rc=0)'
  - name: 2 đột biến doctrine-scan (bo_kiem_chep_protocol, nang_nguong_chep_protocol_len_50)
    command: mutant runner trong test suite
    exit_code: 0
    status: passed
    evidence: 'bo_kiem_chep_protocol giết đủ 3 ca đích (chep_5_1, chep_5_1_ngan, chep_12); nang_nguong giết chep_5_1_ngan; đối chứng khác họ sống'
```

## 1. Giải quyết 5 lớp finding của Reviewer Claude (Lượt 1)

### Lớp 1 (P1 — Fail-open khi đọc protocol nguồn):
- `_doc_nguon_protocol` trong `.claude/dev/packet_loop.py` chuyển sang **fail-close** tuyệt đối: gọi `_die(RC_ARG, "KHÔNG ĐO ĐƯỢC: ...")` cho cả 4 cửa:
  1. Thiếu tệp `docs/PROTOCOL_DA_PHIEN.md` dưới `--root`.
  2. Lỗi đọc tệp / giải mã UTF-8.
  3. Tệp nguồn quá ngắn (< 200 từ).
  4. Tệp nguồn rỗng hoặc quá ngắn (< 200 từ) sau khi bóc tách code fence.
- Bổ sung 4 ca test fail-close tương ứng trong `.claude/dev/packet_loop_test.py`:
  - `case_doctrine_scan_fail_close_thieu_protocol`
  - `case_doctrine_scan_fail_close_khong_phai_utf8`
  - `case_doctrine_scan_fail_close_protocol_ngan`
  - `case_doctrine_scan_fail_close_chi_co_fence`
  Cả 4 ca đều xác nhận nhận đúng `rc=2` và in ra `"KHÔNG ĐO ĐƯỢC"`.

### Lớp 2 (P1 — Đọc ngoài `--root` làm mất kiểm soát cơ sở so sánh):
- Gỡ bỏ hoàn toàn đường fallback `parents[2]` trong `_doc_nguon_protocol`. Phép đo chỉ so sánh duy nhất với protocol dưới `--root`.
- `_repo_gia` trong `packet_loop_test.py` nay tự tạo `docs/PROTOCOL_DA_PHIEN.md` với `_PROTO_TRUNG_TINH` mặc định (đủ dài > 200 từ, không trùng câu chữ của protocol hay adapter mẫu, tránh làm đỏ 36 ca đối chứng khác họ). Ca nào đo hành vi chép thì truyền `protocol=raw` tường minh.

### Lớp 3 (P2 — Ca có mặt khác ca có đo):
- `case_doctrine_scan_chep_12_bi_chan` trước đây chép trọn §12 (vốn dính cụm cấm cũ như `"người có thẩm quyền"`), làm ca này không đo được cơ chế n-gram mới.
- Đã sửa ca này sang trích xuất 30 từ văn xuôi thuần ở vị trí 45 của §12:
  `"Các trần độc lập và trần chạm trước thắng: 20 packet là guard cấu trúc, không hứa đủ invocation cho 20 × 3 attempt cùng reviewer. Trước khi cấp lease/review,"`
  Đoạn này hoàn toàn không dính 28 cụm cấm cũ. Khi bật n-gram => `rc=6`; khi tắt n-gram (`if False:`) => `rc=0`.
- Cập nhật mutant `bo_kiem_chep_protocol` trong `MUTANTS` để `phai_chet` bao gồm cả 3 ca:
  `["doctrine_scan_chep_tron_5_1_bi_chan", "doctrine_scan_chep_doan_ngan_5_1_bi_chan", "doctrine_scan_chep_12_bi_chan"]`.
  Thực nghiệm xác nhận mutant giết trọn vẹn cả 3 ca.

### Lớp 4 (P3 — Ngưỡng 15 của `CLAUDE.md` cần giải trình bằng số liệu đo):
- Đã đo thực tế trên `master`: `CLAUDE.md` có trích dẫn câu bài học nguyên văn dài 13 từ từ protocol (*"cùng họ cổng vắng mặt trông giống cổng xanh, đổi đối tượng: một"*).
- Đo trên `master`: ngưỡng 10: 10 hits; 11: 7 hits; 12: 4 hits; 13: 2 hits; 14: 0 hits; 15: 0 hits.
- Ngưỡng 15 là cận an toàn tối thiểu để không bắt oan câu dẫn giải bài học trong `CLAUDE.md`, trong khi vẫn chặn đứng việc sao chép đoạn dài ( >= 15 từ). Các adapter khác giữ nguyên ngưỡng nghiêm ngặt 10 từ.
- Đã đưa số liệu thực tế này vào chú thích giải trình ngay trên dòng gán `threshold` trong `.claude/dev/packet_loop.py`.

### Lớp 5 (P3 — Hiện vật handoff nằm ngoài tầm ba cổng):
- Theo caveat `r374` (`HIEN-VAT-TRONG-THU-MUC-CON-NAM-NGOAI-TAM-BA-CONG`), các cổng `bien_nhan_v2`, `t26`, `t27` chỉ glob tầng đầu `ops/reviews/*.md`.
- Đã chuyển hiện vật handoff từ thư mục con ra tầng đầu: `ops/reviews/doctrine-scan-handoff-r1-g1-antigravity.md` và dọn dẹp thư mục con cũ.

## 2. Số liệu tự khai của bộ kiểm thử (`packet_loop_test.py`)

```
SỐ LIỆU (đếm bằng máy — chép vào hồ sơ TỪ ĐÂY, đừng gõ tay):
  ca               : 292
  đột biến         : 88
  lớp lách         : 78
  ca bắt-oan       : 35
  ngoại lệ AC 18   : 0
```
- Số ca tăng từ 288 lên 292 (+4 ca fail-close: thiếu protocol, lỗi UTF-8, quá ngắn, chỉ có fence).
- Đột biến `bo_kiem_chep_protocol`: giết đủ 3 ca đích (`chep_5_1`, `chep_5_1_ngan`, `chep_12`).
- Đột biến `nang_nguong_chep_protocol_len_50`: giết đúng ca đích `chep_5_1_ngan`.
