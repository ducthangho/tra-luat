# Cross-review ĐẶC TẢ wp1236 r7 — vòng 7 (vòng CUỐI, chủ kho cho thêm) — reviewer độc lập

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã). Kho: ducthangho/tra-luat.

## Quyền
- CHỈ ĐỌC. Không sửa, không commit, không push bất kỳ tệp nào trong `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r7-claude/repo`. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r7-claude/work/`.
- Không tìm kết luận của reviewer khác. Bạn có VERDICT vòng 6 CỦA CHÍNH BẠN (`/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r7-claude/VERDICT_VONG6_CUA_BAN.md`); bảng *Phản biện* cuối đặc tả
  tóm tắt cách soạn giả xử lý finding của cả hai reviewer — đó là một phần của đặc tả, không phải kết luận vòng 2 của ai.
- Hướng thử nào đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI, đừng dựng.

## Đầu vào
- Đặc tả: `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r7-claude/SPEC.md`, sha256 `31415a8a840c63c3b3a16eefe83dc90739698c3d10afb2348b5e7c5011ae26ba`. Kiểm sha256 trước tiên; lệch thì dừng và báo.
- Kho ở `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r7-claude/repo`, commit `500592da5fd26c6c96a8e6cc2b6fc08f083ae460` = origin/master `b796259` (merge PR #1253; trước đó PR #1255 = #1254, PR #1249 = #1240) + đúng một tệp `ops/specs/wp1236-r7.md`. Lịch sử master đầy đủ, KHÔNG nông.
  (Các nhánh khác như `ops/wp1240-r1-g1-lease` không có trong clone; mục *Nợ kế thừa* trỏ tới chúng — đánh giá dựa trên những gì đặc tả ghi, và ghi rõ chỗ không kiểm được.)
- Thân Issue #1236 + comment bổ sung: `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r7-claude/ISSUE.md`.
- Đọc thêm trong kho: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` (§8.1, §10.2.2, §10.2.3, §20) · `.claude/skills/soan-spec/SKILL.md` (L1–L6) ·
  `ops/land_evidence_nguon.py` (+ test) · `ops/kiem_ho_so_land.py` (+ test) · `.claude/dev/packet_loop.py` (`cmd_kiem_dong_wp`, `_canon`) · `ops/ci_provenance.py` ·
  `ops/land/pr1127-wp1120-provenance/ci/tom_gate_output.py` · `ops/land/pr1231-wp1105-provenance/danh_gia_gate.py` · `ops/land/`.

## Việc phải làm (theo thứ tự ưu tiên)
1. **Từng finding P0–P2 trong VERDICT vòng 6 của bạn**: đã đóng thật chưa trong r7? (Gồm cả P3 — chủ kho giao r7 sửa đủ P3.) Ghi ĐÓNG / CÒN MỞ (kèm lý do) cho từng id.
2. **ĐO LẠI các con số MỚI hoặc ĐỔI của r7**: 22 tên `JOB_BAT_BUOC` và lời khai "ở cả 29 tệp provenance `ci.yml` `push`, J có đúng 22 job và đúng 22 tên này"; J = 14 và tám mảnh `gate-cong-cu` vắng trên run 41397205258; base `b796259` (`51d6509..b796259` không đổi `ops/`, `.github/`; số dòng `packet_loop.py`); `ai-dang-giu` 04:00–04:05Z nếu đo được; Q7 sáu hồ sơ; ước A1 720–900 và `tran_moi` ≤ 950. Số lệch là finding.
3. **Lỗ thiết kế MỚI do r7 đưa vào** (theo QUYẾT ĐỊNH chủ kho ở `QUYET_DINH_CHU_KHO.md`, phần cuối — không tranh luận lại hướng đã chọn, chỉ kiểm cách thi hành): chốt đủ job K3 (`thieu_job_bat_buoc` / `job_trung_ten` / `job_ngoai_luat`) và kiểm sổ; ranh giới của nó với K5/K6/K9; `F-ok` 23 job dựng từ provenance thật + `ci.yml@fe84620` nguyên văn; ca A3j/j′/j″, A3k (`F-41397205258`) và các đột biến m-A3d…g, m-A3k có răng không; A16b/c; A22 danh sách cho phép (`.py`/`.pyc` dưới gốc cây A22, đối chứng (5), (6), m-A22); `nang_tran`. Bản r6 ở `SPEC_R6.md` để so.
4. Luật soan-spec L1–L6 cho mọi tiêu chí mới: có phép đo làm nó ĐỎ không; đột biến có răng không (đo nếu được).
5. Q1–Q10: chỉ nêu nếu khuyến nghị dựa trên số đo sai hoặc thiếu hệ quả.

## Đầu ra — in ra ĐÚNG khối sau làm phần cuối câu trả lời (Markdown)
```
# VERDICT wp1236 r7 vòng 7
spec_sha256: <sha256 bạn đo được>
## Finding vòng 6 của tôi
- F0x: ĐÓNG | CÒN MỞ — <một câu>
## Findings mới
- id: G01
  severity: P0|P1|P2|P3
  vi_tri: <mục/dòng trong SPEC.md>
  van_de: <một câu>
  bang_chung: <lệnh đã chạy + output rút gọn, hoặc trích dẫn>
  de_xuat: <sửa thế nào>
## Đã đo lại, khớp
- <liệt kê ngắn>
KET_LUAN: approve | changes_requested
```
Quy tắc: `approve` CHỈ khi không còn finding P0, P1 hay P2 (kể cả finding vòng 6 CÒN MỞ). P3 không chặn. Dòng `KET_LUAN:` là dòng cuối cùng.
