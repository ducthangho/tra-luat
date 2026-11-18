Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 2, cho đặc tả `ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1.md` (Issue #646). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Worktree master 641108c. `ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1-ban1.md` là bản bạn review lượt 1 (request_changes: P2 N5 phép đếm token lọt câu đảo nghĩa; P2 N4 grep -F khớp nhầm; P2 M2 thiếu phạm vi hạn; P2 N2 thiếu phản chứng định danh; P3 M1 phạm vi grep/ADR-0056; P3 M3 đủ nhánh K4). `ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1.md` là bản sửa; §9 liệt kê thay đổi. Bản sửa nay ghi nguyên văn bảy mệnh đề ở §3 và có script N5 chạy được.

Việc: (1) `diff` hai bản, kiểm từng finding lượt 1 đã đóng thật; (2) CHẠY script N5 trong đặc tả trên bản sao (base phải đỏ; dựng một bản H thử chứa bảy mệnh đề sau khối YAML phải xanh; ba đột biến đảo nghĩa và đổi một byte YAML phải đỏ); kiểm số hit N4 trên base; (3) bảy mệnh đề §3 có đúng sự thật với mã không (từng mệnh đề); (4) rà nhanh L1–L7 có gì mới vỡ.

Đầu ra stdout: bảng finding lượt 1 (đóng/chưa), finding mới P0–P3. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
