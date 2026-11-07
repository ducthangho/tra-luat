# Cross-review ĐẶC TẢ wp1236 r4 — vòng 4 (vòng CUỐI) — reviewer độc lập

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã). Kho: ducthangho/tra-luat.

## Quyền
- CHỈ ĐỌC. Không sửa, không commit, không push bất kỳ tệp nào trong `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r4-codex/repo`. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r4-codex/work/`.
- Không tìm kết luận của reviewer khác. Bạn có VERDICT vòng 3 CỦA CHÍNH BẠN (`/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r4-codex/VERDICT_VONG3_CUA_BAN.md`); bảng *Phản biện* cuối đặc tả
  tóm tắt cách soạn giả xử lý finding của cả hai reviewer — đó là một phần của đặc tả, không phải kết luận vòng 2 của ai.
- Hướng thử nào đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI, đừng dựng.

## Đầu vào
- Đặc tả: `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r4-codex/SPEC.md`, sha256 `c8e79de93545c6003e36162f03465213c4d97566a32156faf7a1ba69042b519b`. Kiểm sha256 trước tiên; lệch thì dừng và báo.
- Kho ở `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r4-codex/repo`, commit `deacebf4b590e1dc78706d7374090306d66cd9cf` = origin/master `3163f4d` + đúng một tệp `ops/specs/wp1236-r4.md`. Lịch sử master đầy đủ, KHÔNG nông.
  (Các nhánh khác như `ops/wp1240-r1-g1-lease` không có trong clone; mục *Nợ kế thừa* trỏ tới chúng — đánh giá dựa trên những gì đặc tả ghi, và ghi rõ chỗ không kiểm được.)
- Thân Issue #1236 + comment bổ sung: `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r4-codex/ISSUE.md`.
- Đọc thêm trong kho: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` (§8.1, §10.2.2, §10.2.3, §20) · `.claude/skills/soan-spec/SKILL.md` (L1–L6) ·
  `ops/land_evidence_nguon.py` (+ test) · `ops/kiem_ho_so_land.py` (+ test) · `.claude/dev/packet_loop.py` (`cmd_kiem_dong_wp`, `_canon`) · `ops/ci_provenance.py` ·
  `ops/land/pr1127-wp1120-provenance/ci/tom_gate_output.py` · `ops/land/pr1231-wp1105-provenance/danh_gia_gate.py` · `ops/land/`.

## Việc phải làm (theo thứ tự ưu tiên)
1. **Từng finding P0–P2 trong VERDICT vòng 3 của bạn**: đã đóng thật chưa trong r4? Ghi ĐÓNG / CÒN MỞ (kèm lý do) cho từng id.
2. **ĐO LẠI các con số MỚI hoặc ĐỔI của r4** (bảng ba dạng tệp 6/4, 4/4, 13/11; H = `merge_commit` gốc ∪ `prs[*].merge_commit`, hai hồ sơ nhiều PR; pr721/pr732 H rỗng; 30 provenance push = 26 `ci.yml` + 4 `launcher-windows.yml`; J = 22 job ở run pr1231; `CHECK_BAT_BUOC` dòng 2402). Số lệch là finding.
3. **Lỗ thiết kế MỚI do r4 đưa vào**: `chan_k7` (có tái tạo đúng điều kiện của `chan_buoc` trừ `env:` bước không? tập khoá env theo bước có thi công được, và A15 có xanh trên `F-that` không — đo bằng phản thực tế nếu được); `OS_BAT_BUOC`/`ngoai_pham_vi_os` trong K3; *Phạm vi land* (neo + workflow `ci.yml`, run không provenance coi là land); readback cho `owner_waived` và D2b `gate_output_mien`; `tom` chọn phiên bản theo miền, miền rời nhau, `kiem_so_luat`; quy tắc tên tệp `gate-output2-…` và phân giải trong thư mục provenance; workflow đọc tại SHA checkout. Bản r3 ở `SPEC_R3.md` để so.
4. Luật soan-spec L1–L6 cho mọi tiêu chí mới: có phép đo làm nó ĐỎ không; đột biến có răng không (đo nếu được).
5. Q1–Q10: chỉ nêu nếu khuyến nghị dựa trên số đo sai hoặc thiếu hệ quả.

## Đầu ra — in ra ĐÚNG khối sau làm phần cuối câu trả lời (Markdown)
```
# VERDICT wp1236 r4 vòng 4
spec_sha256: <sha256 bạn đo được>
## Finding vòng 3 của tôi
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
Quy tắc: `approve` CHỈ khi không còn finding P0, P1 hay P2 (kể cả finding vòng 3 CÒN MỞ). P3 không chặn. Dòng `KET_LUAN:` là dòng cuối cùng.
