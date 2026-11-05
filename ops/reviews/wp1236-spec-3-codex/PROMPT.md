# Cross-review ĐẶC TẢ wp1236 r3 — vòng 3 — reviewer độc lập

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã). Kho: ducthangho/tra-luat.

## Quyền
- CHỈ ĐỌC. Không sửa, không commit, không push bất kỳ tệp nào trong `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r3-codex/repo`. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r3-codex/work/`.
- Không tìm kết luận của reviewer khác. Bạn có VERDICT vòng 2 CỦA CHÍNH BẠN (`/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r3-codex/VERDICT_VONG2_CUA_BAN.md`); bảng *Phản biện* cuối đặc tả
  tóm tắt cách soạn giả xử lý finding của cả hai reviewer — đó là một phần của đặc tả, không phải kết luận vòng 2 của ai.
- Hướng thử nào đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI, đừng dựng.

## Đầu vào
- Đặc tả: `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r3-codex/SPEC.md`, sha256 `e4166c02939f154c1d434b97840655d6184e028085f8ec8fe5b99bed885f5f22`. Kiểm sha256 trước tiên; lệch thì dừng và báo.
- Kho ở `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r3-codex/repo`, commit `cc4162d0e0c61e8c085642ad52362166a0fbd2da` = origin/master `3163f4d` + đúng một tệp `ops/specs/wp1236-r3.md`. Lịch sử master đầy đủ, KHÔNG nông.
  (Các nhánh khác như `ops/wp1240-r1-g1-lease` không có trong clone; mục *Nợ kế thừa* trỏ tới chúng — đánh giá dựa trên những gì đặc tả ghi, và ghi rõ chỗ không kiểm được.)
- Thân Issue #1236 + comment bổ sung: `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r3-codex/ISSUE.md`.
- Đọc thêm trong kho: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` (§8.1, §10.2.2, §10.2.3, §20) · `.claude/skills/soan-spec/SKILL.md` (L1–L6) ·
  `ops/land_evidence_nguon.py` (+ test) · `ops/kiem_ho_so_land.py` (+ test) · `.claude/dev/packet_loop.py` (`cmd_kiem_dong_wp`, `_canon`) · `ops/ci_provenance.py` ·
  `ops/land/pr1127-wp1120-provenance/ci/tom_gate_output.py` · `ops/land/pr1231-wp1105-provenance/danh_gia_gate.py` · `ops/land/`.

## Việc phải làm (theo thứ tự ưu tiên)
1. **Từng finding P0–P2 trong VERDICT vòng 2 của bạn**: đã đóng thật chưa trong r3? Ghi ĐÓNG / CÒN MỞ (kèm lý do) cho từng id.
2. **ĐO LẠI các con số MỚI hoặc ĐỔI của r3** (chuỗi khác = 1, tổng 64; 8/9 hồ sơ còn khớp băm L5; L8 hồi tố 36 kèm hàng pr679; `tu_do` 13/11; 118/123 hồ sơ có `merge_commit` mức gốc; chuẩn hoá tên khoá không thêm khoá mới; nền ruff). Số lệch là finding.
3. **Lỗ thiết kế MỚI do r3 đưa vào**: `MIEN_HIEU_LUC` theo run id; dòng `STEP` + K7 dùng lại `ci_provenance.ghep_buoc`/`chan_buoc`/`doc_wf`/`ghep_job` (có gọi được nguyên trạng không? đọc mã); loại `chuan-bi` khỏi J; *Neo* không thừa kế + nhánh `moc_10_2_2`/`ci_master`; *lời khai land* theo `merge_commit` gốc; `owner_waived` ba điều kiện; `url_hop_le` truyền vào; D2b chép ba tệp, rc 8; tách đợt A1/A2 và `nang_tran`; F-ok/F-that chép tên thật từ `pr1231`. Bản r2 ở `SPEC_R2.md` (cùng thư mục) để so.
4. Luật soan-spec L1–L6 cho mọi tiêu chí mới: có phép đo làm nó ĐỎ không; đột biến có răng không (đo nếu được).
5. Q1–Q9: chỉ nêu nếu khuyến nghị dựa trên số đo sai hoặc thiếu hệ quả.

## Đầu ra — in ra ĐÚNG khối sau làm phần cuối câu trả lời (Markdown)
```
# VERDICT wp1236 r3 vòng 3
spec_sha256: <sha256 bạn đo được>
## Finding vòng 2 của tôi
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
Quy tắc: `approve` CHỈ khi không còn finding P0, P1 hay P2 (kể cả finding vòng 2 CÒN MỞ). P3 không chặn. Dòng `KET_LUAN:` là dòng cuối cùng.
