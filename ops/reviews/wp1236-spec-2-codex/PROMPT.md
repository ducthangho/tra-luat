# Cross-review ĐẶC TẢ wp1236 r2 — vòng 2 — reviewer độc lập

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã). Kho: ducthangho/tra-luat.

## Quyền
- CHỈ ĐỌC. Không sửa, không commit, không push bất kỳ tệp nào trong `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r2b-codex/repo`. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r2b-codex/work/`.
- Không tìm kết luận của reviewer khác. Bạn có VERDICT vòng 1 CỦA CHÍNH BẠN (`/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r2b-codex/VERDICT_VONG1_CUA_BAN.md`); bảng *Phản biện r1 → r2* cuối đặc tả
  tóm tắt cách soạn giả xử lý finding của cả hai reviewer — đó là một phần của đặc tả, không phải kết luận vòng 2 của ai.
- Hướng thử nào đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI, đừng dựng.

## Đầu vào
- Đặc tả: `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r2b-codex/SPEC.md`, sha256 `570b10851be95875662da56df3dcb6d6f028429f4cb2e2f1291c3604eb618a0c`. Kiểm sha256 trước tiên; lệch thì dừng và báo.
- Kho ở `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r2b-codex/repo`, commit `308a14ac2c944e0209eb410d6cdf52de57ec9f0d` = origin/master `3163f4d` + đúng một tệp `ops/specs/wp1236-r2.md`. Lịch sử master đầy đủ, KHÔNG nông.
  (Các nhánh khác như `ops/wp1240-r1-g1-lease` không có trong clone; mục *Nợ kế thừa* trỏ tới chúng — đánh giá dựa trên những gì đặc tả ghi, và ghi rõ chỗ không kiểm được.)
- Thân Issue #1236 + comment bổ sung: `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r2b-codex/ISSUE.md`.
- Đọc thêm trong kho: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` (§8.1, §10.2.2, §10.2.3, §20) · `.claude/skills/soan-spec/SKILL.md` (L1–L6) ·
  `ops/land_evidence_nguon.py` (+ test) · `ops/kiem_ho_so_land.py` (+ test) · `.claude/dev/packet_loop.py` (`cmd_kiem_dong_wp`, `_canon`) · `ops/ci_provenance.py` ·
  `ops/land/pr1127-wp1120-provenance/ci/tom_gate_output.py` · `ops/land/pr1231-wp1105-provenance/danh_gia_gate.py` · `ops/land/`.

## Việc phải làm (theo thứ tự ưu tiên)
1. **Từng finding P0–P2 trong VERDICT vòng 1 của bạn**: đã đóng thật chưa trong r2? Ghi ĐÓNG / CÒN MỞ (kèm lý do) cho từng id.
2. **ĐO LẠI các con số MỚI hoặc ĐỔI của r2** (28 hồ sơ/34 tệp provenance; bảng tên khoá và dạng giá trị; 46/44/61/22/22/9/35; bảng L8 35 dòng; 49/49 L-7 = 32+17; nền ruff). Số lệch là finding.
3. **Lỗ thiết kế MỚI do r2 đưa vào**: sổ phiên bản LUAT, bốn loại dấu hiệu, K1–K9 (đặc biệt K7 so tên bước với `ten_du_kien`), định nghĩa lời khai fail-closed, *Neo run* (tìm `run_id` gần nhất ở tổ tiên — có chọn nhầm run không?), `owner_waived`, D2b nạp module từ origin/master, `nang_tran` đợt A, N1/N2.
4. Luật soan-spec L1–L6 cho mọi tiêu chí mới: có phép đo làm nó ĐỎ không; đột biến có răng không (đo nếu được).
5. Q1–Q9: chỉ nêu nếu khuyến nghị dựa trên số đo sai hoặc thiếu hệ quả.

## Đầu ra — in ra ĐÚNG khối sau làm phần cuối câu trả lời (Markdown)
```
# VERDICT wp1236 r2 vòng 2
spec_sha256: <sha256 bạn đo được>
## Finding vòng 1 của tôi
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
Quy tắc: `approve` CHỈ khi không còn finding P0, P1 hay P2 (kể cả finding vòng 1 CÒN MỞ). P3 không chặn. Dòng `KET_LUAN:` là dòng cuối cùng.
