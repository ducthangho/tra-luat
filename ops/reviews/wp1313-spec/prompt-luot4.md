Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 4, cho đặc tả `ops/specs/LAUNCHER-5XX-KHONG-PHAI-CHAN-r3.md` (Issue #1313). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao trong /tmp.

Thư mục làm việc: worktree master 3d6bfa5. `ops/specs/LAUNCHER-5XX-KHONG-PHAI-CHAN-r3-ban1.md` là bản bạn review lượt 3 (request_changes: P2 M9/N6 thiếu biên 500/499/600 và cụm `HTTP <mã>`; P2 lệnh quét §6 dùng rg trần bỏ `.claude/`; P3 `t06` phụ thuộc KeyError fixture; P3 mốc giờ §0, §9 thiếu, docstring). `ops/specs/LAUNCHER-5XX-KHONG-PHAI-CHAN-r3.md` là bản sửa; mục 9 dòng cuối liệt kê thay đổi.

Việc: (1) `diff` hai bản, kiểm từng finding lượt 3 đã đóng thật; (2) thử trong RAM: các biến thể sai (`500 <`, bỏ `< 600`, mã rời) giờ có làm đỏ ca M9 như N6 nói không; lệnh `git grep` mới ở §6 có trả các hit cần thấy (launcher.py, mcp_github_doc.py) không; `t06` với fixture 202 có xanh trên base và đỏ đúng thông điệp khi gỡ guard `bo_header_github` không; (3) rà nhanh phần còn lại theo L1–L7, có gì mới vỡ không.

Đầu ra stdout: bảng finding lượt 3 (đóng/chưa), finding mới P0–P3. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
