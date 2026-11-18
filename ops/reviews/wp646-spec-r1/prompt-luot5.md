Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 5, cho đặc tả `ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1.md` (Issue #646). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Worktree master 641108c. `ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1-ban4.md` là bản bạn review lượt 4 (request_changes: P2 N5 xanh khi bảy mệnh đề nằm trong blockquote chứa rào hoặc trong một code span hai backtick giữa dòng; P3 điểm chờ E2 ở §6 thiếu mức đã dùng, quyền còn thiếu, mục đích). `ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1.md` là bản sửa; §9 liệt kê thay đổi.

Việc: (1) `diff` hai bản, kiểm hai finding lượt 4 đã đóng bằng cách CHẠY script N5 (trích từ chính đặc tả) trên bản sao: blockquote chứa rào, code span hai backtick giữa dòng phải đỏ; H gốc và H ngắt 60 cột phải xanh; chạy lại các đột biến lượt 2–4 vẫn đỏ. (2) Tìm cách khác làm N5 xanh giả (vd thẻ HTML giữa dòng ngoài comment, setext heading, bảng, tham chiếu link) hoặc đỏ oan với H hợp lệ. (3) Kiểm điểm chờ E2 §6 đủ dữ liệu theo L7/ADR-0067. (4) Rà nhanh L1–L7.

Đầu ra stdout: bảng finding (đóng/chưa), finding mới P0–P3. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
