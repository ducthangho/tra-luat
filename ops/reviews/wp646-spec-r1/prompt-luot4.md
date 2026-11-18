Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 4, cho đặc tả `ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1.md` (Issue #646). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Worktree master 641108c. `ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1-ban3.md` là bản bạn review lượt 3 (request_changes: P2 N5 nhận mệnh đề ẩn trong HTML comment mở giữa dòng; P3 N5 chấp nhận menh_de.txt rỗng; P3 N5 xanh khi thêm câu đảo nghĩa). `ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1.md` là bản sửa; §9 liệt kê thay đổi.

Việc: (1) `diff` hai bản, kiểm ba finding lượt 3 đã đóng thật bằng cách CHẠY script N5 (trích từ chính đặc tả) trên bản sao: base đỏ; H thử chứa bảy mệnh đề đúng vùng xanh; mệnh đề trong `Van dan <!-- … -->` đỏ; comment không đóng đỏ; MD rỗng/sửa đỏ; câu thêm nhắc tên trường đỏ; chạy lại các đột biến lượt 2–3 (CRLF, dời vị trí, rào, thụt lề, đảo nghĩa) vẫn đỏ. (2) Tìm cách khác làm N5 xanh giả hoặc đỏ oan với một H hợp lệ (vd ca ghép rào sau comment cùng dòng mà tác giả khai chưa đo). (3) Đánh giá giới hạn đã khai (câu khẳng định thêm không nhắc tên trường vẫn qua, reviewer phải đọc diff) có chấp nhận được không. (4) Rà nhanh L1–L7.

Đầu ra stdout: bảng finding (đóng/chưa), finding mới P0–P3. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
