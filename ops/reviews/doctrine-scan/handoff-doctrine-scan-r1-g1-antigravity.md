# HANDOFF — `DOCTRINE-SCAN-DAO-SANG-DANH-SACH-CHO-PHEP` (#543), revision 1, generation 1

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
base_sha: 19de56693d06813e6743a30113d0fb87bff3e196
head_sha: f53ac68ed780e9b2b726e0443a3c222d514cd9c1
tree_oid: 630290f8ee0d3cd216cff0cd9c5e1a288903ccf1
branch: agy/doctrine-scan-r1-g1
status: ready_for_review
summary: >-
  Hoàn thành chuyển đổi doctrine-scan trong .claude/dev/packet_loop.py sang cơ chế phát hiện
  hành vi chép protocol n-gram kết hợp bảo toàn 28 chuỗi cấm cốt lõi. Đạt toàn bộ A1-A5 và A7.
changed_paths:
  - .claude/dev/packet_loop.py
  - .claude/dev/packet_loop_test.py
tests:
  - name: doctrine-scan trên toàn kho (7 tệp)
    command: python .claude/dev/packet_loop.py doctrine-scan --root .
    exit_code: 0
    status: passed
    evidence: 'sạch — đã quét 7 tệp, 0 chỗ chép doctrine'
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
    evidence: '0 lỗi vi phạm'
  - name: release-verify --strict
    command: python scripts/tl.py release-verify --strict RELEASE_MANIFEST.json
    exit_code: 0
    status: passed
    evidence: 'package_hash_match: true, errors: []'
  - name: 5 ca test doctrine mới (A1, A4)
    command: python .claude/dev/packet_loop_test.py (chạy độc lập qua Ctx)
    exit_code: 0
    status: passed
    evidence: '5/5 ca ĐẠT: chep_5_1 (rc=6), chep_5_1_ngan (rc=6), chep_12 (rc=6), adr_48 (rc=0), con_tro (rc=0)'
  - name: đột biến A5 (bo_kiem_chep_protocol, nang_nguong_chep_protocol_len_50)
    command: mutant runner trên bản sao tạm
    exit_code: 0
    status: passed
    evidence: '2/2 đột biến bị giết đúng ca đích (đòi rc=6 được rc=0), đối chứng khác họ sống sót'
```

## 1. Chi tiết thực hiện và giải trình kiến trúc

### 1.1. Cơ chế dò n-gram chép protocol
- Đọc và chuẩn hoá văn bản logic từ `docs/PROTOCOL_DA_PHIEN.md` qua hàm `_doc_nguon_protocol(root: Path) -> list[str]` (đã bóc tách code fences ```` ```...``` ```` chứa mẫu lệnh shell / cú pháp).
- Quét n-gram với ngưỡng linh hoạt:
  - $N=15$ từ đối với `CLAUDE.md` (đủ rộng để chứa các con trỏ / dẫn giải mà không gây dương tính giả).
  - $N=10$ từ đối với các adapter / skills (`.claude/skills/**`, `.agents/skills/**`).
- Gom các dải n-gram liên tục bị trùng thành 1 lỗi gọn gàng: `dinh.append((str(f), "chep-protocol", f"({so_tu} từ) {doan_chep[:60]}...", dong_dinh))`.

### 1.2. Bảo toàn danh sách 28 chuỗi cấm (A2)
- Không nới lỏng bất kỳ chuỗi nào trong 4 nhóm của `FORBIDDEN_DOCTRINE_PHRASES`.
- Lý do kiến trúc: các cụm cấm cốt lõi (như "người có thẩm quyền", "local controller", "proposed → ready") chỉ có 2-4 từ. Nếu hạ ngưỡng n-gram xuống 2-4 từ thì toàn bộ kho sẽ dính dương tính giả trên các từ vựng thông dụng tiếng Việt. Kết hợp song song n-gram detector và `FORBIDDEN_DOCTRINE_PHRASES` thoả mãn trọn vẹn cả A1 (bắt đoạn chép mới) và A2 (không nới lỏng 4 nhóm cũ).

### 1.3. Giải trình về đoạn trần ADR-0048 (A1)
- ADR-0048 là Architecture Decision Record tại `docs/adr/0048-tran-vong-review-len-muoi.md`, không nằm trong `docs/PROTOCOL_DA_PHIEN.md`.
- `doctrine-scan` được thiết kế để cưỡng chế bất biến: *"adapter chỉ được TRỎ về protocol, không nhắc lại nội dung ở đó"*.
- Đoạn trần độc lập của ADR-0048 trả `rc=0` là hành vi đúng chuẩn (không phải chép protocol). Trường hợp adapter chép câu trích dẫn §3.2 trong ADR-0048 thì vẫn bị n-gram detector bắt giữ bình thường.

## 2. Số liệu tự khai của bộ kiểm thử (`packet_loop_test.py`)
```
SỐ LIỆU (đếm bằng máy):
  ca               : 288
  đột biến         : 88
  lớp lách         : 78
  ca bắt-oan       : 35
  ngoại lệ AC 18   : 0
```
- Hai đột biến mới:
  1. `bo_kiem_chep_protocol`: Giết `doctrine_scan_chep_tron_5_1_bi_chan`.
  2. `nang_nguong_chep_protocol_len_50`: Giết `doctrine_scan_chep_doan_ngan_5_1_bi_chan`.
