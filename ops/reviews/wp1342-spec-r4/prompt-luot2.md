Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 2, cho đặc tả `ops/specs/WP1174-WINDOWS-BACKEND-r4.md` (Issue #1342). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Clone master e2c3b82 (cộng chưa commit: đặc tả r1–r4 và review cũ `ops/reviews/wp1342-spec-r1..r3/`). `ops/specs/WP1174-WINDOWS-BACKEND-r4-ban1.md` là bản bạn review lượt 1; verdict lượt 1 ở `ops/reviews/wp1342-spec-r4/luot1.verdict.txt` (request_changes: 2 P1, 7 P2, 1 P3).

PHẠM VI ĐÃ THU HẸP (quyết định chủ kho sau lượt 1, ghi §9 Q1): r4 nay là **r1d-a1** = vòng đời tiến trình trong Job Object, KHÔNG pipe (stdin/stdout/stderr đều DEVNULL). Transport hai pipe chuyển sang r1d-a2. Vì vậy các finding lượt 1 sau đây KHÔNG còn thuộc r4 và không được nêu lại là finding của r4 (chỉ kiểm rằng §2 đã ghi chúng sang a2): P1 "hai reader / trần byte / cleanup I/O", phần `on_bytes`/callback của P2 "callback và handle", N4 (f)(g) cũ, M3 cũ, P1–P4 cũ, đột biến (d)(f)(g) cũ.

Các finding lượt 1 THUỘC a1 phải được ĐÓNG THẬT trong bản này: P1 sở hữu cleanup trước/sau gán; P2 chứng cứ bắt đầu treo + thứ tự gán + nhánh Toolhelp/ResumeThread + ABI; P2 job rỗng (query lỗi, terminate lỗi, giữ handle đúng đối tượng, bắt tay, tách a1/a2); P2 breakaway/job lồng/handle kế thừa (allowlist mã lỗi, job ngoài che mutant, silent breakaway, allowlist cờ); phần handle của P2 "callback và handle" (ma trận lối ra theo mốc sở hữu); P2 N1–N8; P2 dự toán; P3 văn bản. §9 Q1–Q4 là quyết định chủ kho, không tranh luận.

Việc:
1. `diff` bản 1 với bản hiện tại; với từng finding thuộc a1 ở trên, kiểm đã đóng thật (trích chỗ đóng) hay chưa.
2. Tìm đường MỚI chưa có trong bảng §4b để tiến trình/cháu sống ngoài vòng đời lời gọi, hoặc để hàm trả thành công sai (kể cả do chính thiết kế mới: `truoc_gan`/`between` có thành seam bỏ qua mã runtime không; `_1174_win_cleanup` thứ tự bước; ưu tiên lỗi; `proc.kill()` trên tiến trình đã gán job; `Popen._handle`; `GetProcessIdOfThread`; job lồng; tiến trình trợ giúp J10/J12; tái dùng PID trong bắt tay).
3. Mỗi đột biến §4b có thật sự khớp đúng một chỗ trong mã dự kiến và cho ĐÚNG dấu hiệu đỏ đã ghi, khác mọi đột biến khác không (vd a1 có thể đỏ ở J3 bằng "job not empty" nhưng cũng làm J9/J12 đỏ — chấp nhận được nếu dấu hiệu ghi cho a1 là duy nhất của nó; nêu chỗ hai đột biến không phân biệt được). Ca native J1–J12 có thật sự đo được trên Windows thật, có tự lừa không.
4. N1–N8 theo L1–L7 `.claude/skills/soan-spec/SKILL.md`: mỗi N có phép đỏ đỏ được.
5. Ngân sách 355–435 dòng có hợp lý không (trần 450).

Đầu ra stdout: bảng finding lượt 1 thuộc a1 (đóng/chưa, kèm chỗ), finding mới P0–P3. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
