Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 3, cho đặc tả `ops/specs/WP1174-WINDOWS-BACKEND-r4.md` (Issue #1342). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Clone master e2c3b82 (cộng chưa commit: đặc tả r1–r4, các bản trước `ops/specs/WP1174-WINDOWS-BACKEND-r4-ban1.md`, `-ban2.md`, và review `ops/reviews/wp1342-spec-r1..r3/`, `ops/reviews/wp1342-spec-r4/luot1.verdict.txt`, `luot2.verdict.txt`).

PHẠM VI (quyết định chủ kho, §9): r4 nay là **r1d-a1-i** = lõi vòng đời tiến trình trong Job Object, không pipe. Đã chuyển đi và KHÔNG được nêu lại thành finding của r4 (chỉ kiểm §2 có ghi): sang r1d-a1-ii — breakaway tường minh/ngầm (J4/J5 cũ, e1/e2), job lồng (J12 cũ); sang r1d-a2 — transport hai pipe, `on_bytes`, trần byte, M3/P1–P4/(d)(f)(g)/N4(f)(g) cũ. Chủ kho đã NÂNG TRẦN kích thước cho riêng revision này lên ≤ 2 tệp / ≤ 550 dòng thêm (Q5, dòng khai đầu tệp) — dùng 550, không dùng 450. Ranh giới "tiến trình gọi chết giữa Popen và gán job ⇒ con treo bị bỏ lại" là nợ có tên đã được chủ kho chấp nhận (Q2, §2) — chỉ nêu finding nếu lời khai về ranh giới ấy SAI hoặc J10b không đo đúng nó.

Việc:
1. `diff` bản 2 với bản hiện tại; với từng finding lượt 2 (`luot2.verdict.txt`) thuộc a1-i, kiểm đã đóng thật (trích chỗ) hay chưa.
2. Tìm đường MỚI chưa có trong §4b để tiến trình sống ngoài vòng đời lời gọi hoặc hàm trả thành công sai; đặc biệt các chỗ mới: `_1174_win_cleanup` bắt `BaseException`, thứ tự bước dọn và điều kiện `da_gan`, đăng ký dọn ngay sau `Popen` trước kiểm `_handle`, ưu tiên lỗi + `add_note`, xác minh creation time, luồng quan sát, giao thức trợ giúp J10/J10b, J9 thành viên thứ hai (gán tiến trình phụ vào job trong `between` có được không — tiến trình phụ có thể đã ở job khác?).
3. Mỗi đột biến §4b: khớp đúng một chỗ trong mã dự kiến, cho ĐÚNG dấu hiệu đã ghi, và dấu hiệu ấy không đột biến nào khác gây ra (kiểm riêng phần "Phân biệt" a1/k2/a2/c/b).
4. N1–N8 theo L1–L7 `.claude/skills/soan-spec/SKILL.md`; N2 (AST + cấm trùng tên) có thật sự đỏ với hai phản chứng đã nêu — hãy CHẠY thử trong RAM trên `packet_loop_test.py` của base.
5. Ngân sách §8 (428–536) có hợp lý với trần 550 không.

Đầu ra stdout: bảng finding lượt 2 thuộc a1-i (đóng/chưa, kèm chỗ), finding mới P0–P3. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
