Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 3, cho đặc tả `ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1.md` (Issue #646). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Worktree master 641108c. `ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1-ban2.md` là bản bạn review lượt 2 (request_changes: P2 N5 đọc YAML text-mode bỏ lọt CRLF; P2 N5 chấp nhận mệnh đề sai vị trí/trong khối mã; P3 N4 thiếu mẫu dương). `ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1.md` là bản sửa; §9 liệt kê thay đổi.

Việc: (1) `diff` hai bản, kiểm ba finding lượt 2 đã đóng thật: CHẠY script N5 trên bản sao — base đỏ; một H thử chứa bảy mệnh đề đúng vùng §4 xanh; các đột biến (CRLF một byte, toàn tệp CRLF, dời đoạn ra cuối/trong khối mã/trước §5, bọc rào, thụt lề, ba đảo nghĩa, đổi byte YAML) đỏ; số hit N4 mới trên base đúng; (2) rà nhanh L1–L7 có gì mới vỡ; tìm cách khác làm script N5 xanh giả.

Đầu ra stdout: bảng finding (đóng/chưa), finding mới P0–P3. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
