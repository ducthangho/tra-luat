Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 6, cho đặc tả `ops/specs/WP1174-WINDOWS-BACKEND-r4.md` (Issue #1342, bậc r1d-a1-i). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Clone master e2c3b82 (cộng chưa commit: đặc tả r1–r4, các bản trước `ops/specs/WP1174-WINDOWS-BACKEND-r4-ban1.md` … `-ban5.md`, review `ops/reviews/wp1342-spec-r1..r3/` và `ops/reviews/wp1342-spec-r4/luot1..5.verdict.txt`).

Ràng buộc đã chốt (§9, không tranh luận): phạm vi r1d-a1-i; J4/J5/J12 sang a1-ii; transport sang a2; nợ `wp1342-pre-assign-orphan` (gồm hai biến thể constructor `Popen` và thiếu `_handle`) đã được chủ kho chấp nhận; trần nâng ≤ 2 tệp / ≤ 550 dòng thêm, CƯỠNG CHẾ trên numstat thật lúc thi công (§7), không trên đầu cao của ước lượng tĩnh (quyết định điều phối). Chỉ nêu finding về ngân sách nếu ước lượng hợp lý của bạn có ĐIỂM GIỮA > 550.

Việc:
1. `diff` bản 5 (`-ban5.md`) với bản hiện tại; với từng finding lượt 5 (`luot5.verdict.txt`, R5-1–R5-8), kiểm đã đóng thật (trích chỗ) hay chưa.
2. Tìm đường MỚI ở các chỗ vừa sửa: ghi chú bằng mã bước qua `BaseException.add_note` gọi thẳng (chạy thử trong RAM hai phản chứng S4: lỗi ghi đè `add_note`, ngoại lệ dọn có metaclass ghi đè `__getattribute__`); dấu hiệu a1/k2 bằng `cleanup:xac_nhan`; bàn giao handle khi join hết hạn; giao thức tệp `tha_*` của J2/J3/J6/J9/J10/J10b; d0 `proc.wait()`; vector d1 `now+10**6`; N2(ii) đếm sau khi loại khối chèn hợp lệ và N2(iv) cấm walrus/Global/Store-Del tên cũ trên toàn cây phần chèn — CHẠY lại trong RAM trên `packet_loop_test.py` của base: base xanh bốn vế; các phản chứng cũ và hai phản chứng walrus mới đỏ; khối hợp lệ mô phỏng (hai def mới, một gán mới, `CASES += [("id", _native1342("id", fn))]`) xanh.
3. Mỗi đột biến §4b (15 ID): khớp đúng một chỗ trong mã dự kiến, đúng dấu hiệu đã ghi, dấu hiệu không đột biến nào khác gây ra.
4. N1–N8 theo L1–L7 `.claude/skills/soan-spec/SKILL.md`.

Đầu ra stdout: bảng finding lượt 5 (đóng/chưa, kèm chỗ), finding mới P0–P3. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
