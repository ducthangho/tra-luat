Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 5, cho đặc tả `ops/specs/WP1174-WINDOWS-BACKEND-r4.md` (Issue #1342, bậc r1d-a1-i). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Clone master e2c3b82 (cộng chưa commit: đặc tả r1–r4, các bản trước `ops/specs/WP1174-WINDOWS-BACKEND-r4-ban1.md` … `-ban4.md`, review `ops/reviews/wp1342-spec-r1..r3/` và `ops/reviews/wp1342-spec-r4/luot1..4.verdict.txt`).

Ràng buộc đã chốt (§9, không tranh luận): phạm vi r1d-a1-i; J4/J5/J12 sang a1-ii; transport sang a2; nợ `wp1342-pre-assign-orphan` (gồm hai biến thể constructor `Popen` và thiếu `_handle`) đã được chủ kho chấp nhận; trần nâng ≤ 2 tệp / ≤ 550 dòng thêm, CƯỠNG CHẾ trên numstat thật lúc thi công (§7), không trên đầu cao của ước lượng tĩnh (quyết định điều phối). Chỉ nêu finding về ngân sách nếu ước lượng hợp lý của bạn có ĐIỂM GIỮA > 550.

Việc:
1. `diff` bản 4 (`-ban4.md`) với bản hiện tại; với từng finding lượt 4 (`luot4.verdict.txt`, F1–F8), kiểm đã đóng thật (trích chỗ) hay chưa.
2. Tìm đường MỚI ở các chỗ vừa sửa: `_1174_win_note` (chỉ tên kiểu); hợp đồng trả `rc` hai điều kiện; bàn giao handle của luồng quan sát (khoá, cờ `huy`, worker tự đóng khi muộn); tệp mở riêng từng mốc của trợ giúp (J10 giết khi trợ giúp chặn ở bước (8); J10b đứng ở `truoc_gan`); J9 phụ chờ `tha_phu`; `b` chờ đúng tệp marker J6; `d0` cửa sổ 6–11 s; N2 vế (iv) danh sách cho phép phần chèn — CHẠY thử trong RAM trên `packet_loop_test.py` của base: base phải xanh cả bốn vế; các phản chứng (return chèn thân `_native1342`, def trùng cuối tệp, decorator tiêm, `if True:` gán lại, `match`/`case _native1342`, walrus, `del _native1342`) phải đỏ; và một khối chèn HỢP LỆ mô phỏng phần test r4 (vài `def` mới không decorator, một gán tên mới, một `CASES += [...]`) phải xanh. Kiểm thêm: base có chứa sẵn dạng câu lệnh mức module nào mà r4 hợp lệ cần thêm nhưng (iv) cấm không.
3. Mỗi đột biến §4b (15 ID): khớp đúng một chỗ trong mã dự kiến, đúng dấu hiệu đã ghi, dấu hiệu không đột biến nào khác gây ra.
4. N1–N8 theo L1–L7 `.claude/skills/soan-spec/SKILL.md`.

Đầu ra stdout: bảng finding lượt 4 (đóng/chưa, kèm chỗ), finding mới P0–P3. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
