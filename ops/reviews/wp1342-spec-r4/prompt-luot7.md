Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 7, cho đặc tả `ops/specs/WP1174-WINDOWS-BACKEND-r4.md` (Issue #1342, bậc r1d-a1-i). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Clone master e2c3b82 (cộng chưa commit: đặc tả r1–r4, các bản trước `ops/specs/WP1174-WINDOWS-BACKEND-r4-ban1.md` … `-ban6.md`, review `ops/reviews/wp1342-spec-r1..r3/` và `ops/reviews/wp1342-spec-r4/luot1..6.verdict.txt`).

Ràng buộc đã chốt (§9, không tranh luận): phạm vi r1d-a1-i; J4/J5/J12 sang a1-ii; transport sang a2; nợ `wp1342-pre-assign-orphan` (gồm hai biến thể constructor `Popen` và thiếu `_handle`) đã được chủ kho chấp nhận; trần nâng ≤ 2 tệp / ≤ 550 dòng thêm, CƯỠNG CHẾ trên numstat thật lúc thi công (§7), không trên đầu cao của ước lượng tĩnh (quyết định điều phối). Chỉ nêu finding về ngân sách nếu ước lượng hợp lý của bạn có ĐIỂM GIỮA > 550.

Việc:
1. `diff` bản 6 (`-ban6.md`) với bản hiện tại; với từng finding lượt 6 (`luot6.verdict.txt`, R6-1–R6-4), kiểm đã đóng thật (trích chỗ) hay chưa.
2. Tìm đường MỚI ở các chỗ vừa sửa: `_1174_win_note` nuốt mọi ngoại lệ của bước chẩn đoán (chạy thử trong RAM S4 với vector `__getattribute__` ném `KeyboardInterrupt`); vector S4 dạng cặp; N2(iv) miễn đúng nút đích `CASES += [...]`, danh sách cho phép nút ở vị trí đánh giá lúc nạp module, cấm `globals`/`vars`/… — CHẠY lại trong RAM: base xanh bốn vế; mọi phản chứng cũ và `_r4_x = globals().update(_native1342=None)` đỏ; khối hợp lệ mô phỏng xanh; thử tìm đường gán lại tên cũ khác còn lọt; hạn giữ fixture 300 s, tệp `het_han_*`/`tu_ket_thuc`, J2 dưới d0, trợ giúp deadline +300 s.
3. Mỗi đột biến §4b (15 ID): khớp đúng một chỗ trong mã dự kiến, đúng dấu hiệu đã ghi, dấu hiệu không đột biến nào khác gây ra.
4. N1–N8 theo L1–L7 `.claude/skills/soan-spec/SKILL.md`.

Đầu ra stdout: bảng finding lượt 6 (đóng/chưa, kèm chỗ), finding mới P0–P3. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
