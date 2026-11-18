Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 4, cho đặc tả `ops/specs/WP1174-WINDOWS-BACKEND-r4.md` (Issue #1342, bậc r1d-a1-i). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Clone master e2c3b82 (cộng chưa commit: đặc tả r1–r4, các bản trước `ops/specs/WP1174-WINDOWS-BACKEND-r4-ban1.md` … `-ban3.md`, review `ops/reviews/wp1342-spec-r1..r3/` và `ops/reviews/wp1342-spec-r4/luot1..3.verdict.txt`).

Ràng buộc đã chốt (§9, không tranh luận): phạm vi r1d-a1-i; J4/J5/J12 sang a1-ii; transport sang a2; nợ `wp1342-pre-assign-orphan` (gồm hai biến thể constructor `Popen` và thiếu `_handle`) đã được chủ kho chấp nhận; trần nâng ≤ 2 tệp / ≤ 550 dòng thêm, CƯỠNG CHẾ trên numstat thật lúc thi công (§7), không trên đầu cao của ước lượng tĩnh (quyết định điều phối). Chỉ nêu finding về ngân sách nếu ước lượng hợp lý của bạn có ĐIỂM GIỮA > 550.

Việc:
1. `diff` bản 3 (`-ban3.md`) với bản hiện tại; với từng finding lượt 3 (`luot3.verdict.txt`), kiểm đã đóng thật (trích chỗ) hay chưa.
2. Tìm đường MỚI ở các chỗ vừa sửa: `_1174_win_cleanup` chỉ bắt `Exception`; M4(9) quyết định lỗi thắng và `add_note` an toàn; hợp đồng "trả rc ⇔ đã xác nhận"; trần deadline `now + 86400` và chờ theo lát; J9 gán bằng handle gốc; ô kết quả luồng quan sát; tệp `giu` của trợ giúp; J6 nhãn (i)/(ii); N2 đếm điểm bind ở phạm vi module (CHẠY thử trong RAM trên `packet_loop_test.py` của base với các phản chứng: chèn `return` vào thân `_native1342`, `def _native1342` trùng cuối tệp, decorator tiêm trước `def _native1342`, `if True: _native1342 = None` — và kiểm base tự nó xanh, kể cả các tên bị gán lại hợp lệ ở base như `MUTANTS_NHAM_TEST`).
3. Mỗi đột biến §4b (15 ID): khớp đúng một chỗ trong mã dự kiến, đúng dấu hiệu đã ghi, dấu hiệu không đột biến nào khác gây ra.
4. N1–N8 theo L1–L7 `.claude/skills/soan-spec/SKILL.md`.

Đầu ra stdout: bảng finding lượt 3 (đóng/chưa, kèm chỗ), finding mới P0–P3. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
