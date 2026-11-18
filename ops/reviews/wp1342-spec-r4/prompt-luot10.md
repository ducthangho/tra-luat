Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 10 (lượt CUỐI trong trần), cho đặc tả `ops/specs/WP1174-WINDOWS-BACKEND-r4.md` (Issue #1342, bậc r1d-a1-i). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Clone master e2c3b82 (cộng chưa commit: đặc tả r1–r4, các bản trước `ops/specs/WP1174-WINDOWS-BACKEND-r4-ban1.md` … `-ban9.md`, review `ops/reviews/wp1342-spec-r1..r3/` và `ops/reviews/wp1342-spec-r4/luot1..9.verdict.txt`).

Ràng buộc đã chốt (§9, không tranh luận): phạm vi r1d-a1-i; J4/J5/J12 sang a1-ii; transport sang a2; nợ `wp1342-pre-assign-orphan` (gồm hai biến thể constructor `Popen` và thiếu `_handle`) đã được chủ kho chấp nhận; trần nâng ≤ 2 tệp / ≤ 550 dòng thêm, CƯỠNG CHẾ trên numstat thật lúc thi công (§7), không trên đầu cao của ước lượng tĩnh (quyết định điều phối). Chỉ nêu finding về ngân sách nếu ước lượng hợp lý của bạn có ĐIỂM GIỮA > 550.

Việc:
1. `diff` bản 9 (`-ban9.md`) với bản hiện tại; với finding lượt 9 (`luot9.verdict.txt`, R9-1), kiểm đã đóng thật (trích chỗ) hay chưa.
2. Tìm đường MỚI ở chỗ vừa sửa: ràng buộc đăng ký `CASES += [...]` (ID hằng có tiền tố, mới, duy nhất, rời base; vị trí sau câu lệnh base cuối cùng đọc/biến đổi `CASES` — trên base kết thúc ở dòng 18557 — và trước `if __name__` ở 18560). CHẠY lại N2 trong RAM: base xanh; mọi phản chứng cũ và đăng ký trùng `wp1174_writer_accept` đỏ; khối hợp lệ có tiền tố, ID mới, đặt ở cửa sổ 18558–18559 xanh. Rà lần cuối toàn bộ đặc tả xem còn P0–P2 nào.
3. Mỗi đột biến §4b (15 ID): khớp đúng một chỗ trong mã dự kiến, đúng dấu hiệu đã ghi, dấu hiệu không đột biến nào khác gây ra.
4. N1–N8 theo L1–L7 `.claude/skills/soan-spec/SKILL.md`.

Đầu ra stdout: bảng finding lượt 9 (đóng/chưa, kèm chỗ), finding mới P0–P3. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
