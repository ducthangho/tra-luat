# HANDOFF — `DOCTRINE-SCAN-DAO-SANG-DANH-SACH-CHO-PHEP` (#543), revision 1, generation 1 (Vá Review Lượt 2)

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
head_sha: 020b0b0ada848929451e4613451dde8aabcfe107
tree_oid: 8b3753f0b14eea930a8c2c1bf4e713eb2246b761
branch: agy/doctrine-scan-r1-g1
status: ready_for_review
summary: >-
  Giải quyết trọn vẹn các finding trong verdict lượt 1 và lượt 2 của Reviewer Claude (PR #545).
  Fail-close 4 cửa đọc protocol; bỏ fallback ngoài --root; chuẩn hoá _repo_gia với nguồn trung tính;
  sửa ca test §12 sang 30 từ văn xuôi thuần; mutant bo_kiem_chep_protocol giết cả 3 ca; hiệu chỉnh số
  đếm ngưỡng 10 thành 11 hits; và dời hiện vật handoff trở lại thư mục con ops/reviews/doctrine-scan/
  để tuân thủ nghiêm ngặt write_set của lease r1/g1.
changed_paths:
  - .claude/dev/packet_loop.py
  - .claude/dev/packet_loop_test.py
  - ops/reviews/doctrine-scan/handoff-doctrine-scan-r1-g1-antigravity.md
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

## 1. Đối chiếu và giải quyết các lớp finding (Lượt 1 & Lượt 2)

| Lớp | Loại | Lượt 1 | Lượt 2 | Trạng thái vá hiện tại |
|---|---|---|---|---|
| **Lớp 1** | P1 | Fail-open 4 cửa đọc protocol | Đã vá (bằng fail-close) | **ĐẠT** (`_die(RC_ARG, "KHÔNG ĐO ĐƯỢC: ...")` cả 4 cửa) |
| **Lớp 2** | P1 | Fallback ngoài `--root` | Đã vá | **ĐẠT** (bỏ hẳn fallback; `_repo_gia` dựng `docs/` dưới `--root`) |
| **Lớp 3** | P2 | Ca `chep_12` không có răng | Đã vá thật | **ĐẠT** (đổi sang 30 từ văn xuôi §12 không dính 28 cụm; mutant giết cả 3 ca) |
| **Lớp 4** | P3 | Ngưỡng 15 không giải thích | Trôi số hạng: 10 hits -> 11 hits | **ĐÃ HIỆU CHỈNH** (sửa thành 11 hits, khớp phép đo bằng `_phang_ca_tep`) |
| **Lớp 5** | P3 | `head_sha`/`tree_oid` phantom | Đã vá thật | **ĐẠT** (neo commit và tree OID thật của sản phẩm) |
| **Lớp 6** | P2 (Mới) | Ghi ngoài write set (tệp ở tầng đầu) | Thay đổi phạm vi | **ĐÃ DỜI VỀ** `ops/reviews/doctrine-scan/` đúng `write_set` của lease r1/g1 |

### Chi tiết hiệu chỉnh Lớp 4 (P3 — Hiệu chỉnh số hạng trôi):
- Đo lại bằng chính `_phang_ca_tep` của mã sản phẩm trên `CLAUDE.md`:
  - Ngưỡng 10: **11** hits.
  - Ngưỡng 11..15: 7 / 4 / 2 / 0 / 0 hits (khớp hoàn toàn).
- Đã sửa số `10` thành `11` trong phần chú thích của `.claude/dev/packet_loop.py` và trong hồ sơ handoff.

### Chi tiết hiệu chỉnh Lớp 6 (P2 — Giữ vững ranh giới write set):
- `write_set` của lease r1/g1 quy định: `ops/reviews/doctrine-scan/`.
- Thực hiện dời tệp handoff trở lại đúng thư mục con: `ops/reviews/doctrine-scan/handoff-doctrine-scan-r1-g1-antigravity.md`.
- Rút tệp ở tầng đầu về, bảo toàn bất biến: *Executor chỉ ghi trong effective write set; không mở rộng phạm vi ngoài lease*.

## 2. Số liệu tự khai của bộ kiểm thử (`packet_loop_test.py`)

```
SỐ LIỆU (đếm bằng máy — chép vào hồ sơ TỪ ĐÂY, đừng gõ tay):
  ca               : 292
  đột biến         : 88
  lớp lách         : 78
  ca bắt-oan       : 35
  ngoại lệ AC 18   : 0
```
- 291/291 ca đạt (loại trừ 1 ca Windows-only skip hợp lệ), 0 hồi quy so với nền.
- 13/13 ca doctrine-scan đạt.
- Cả hai đột biến `bo_kiem_chep_protocol` (giết 3 ca) và `nang_nguong_chep_protocol_len_50` (giết 1 ca) hoạt động chính xác.
