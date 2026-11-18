Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 5, cho đặc tả `ops/specs/LAUNCHER-5XX-KHONG-PHAI-CHAN-r3.md` (Issue #1313). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao trong /tmp.

Worktree master 3d6bfa5. `ops/specs/LAUNCHER-5XX-KHONG-PHAI-CHAN-r3-ban2.md` là bản bạn review lượt 4 (request_changes: P2 M3/M4 chỉ đòi mô tả chứa con số mã, chưa đòi cụm `HTTP <mã>` như M9, M5 chưa cô lập; P3 docstring `_do_rest_github`/`_do_mcp_endpoint` chưa được yêu cầu cập nhật; P3 lượt 3 còn sót: §9 chưa dẫn mốc giờ). `ops/specs/LAUNCHER-5XX-KHONG-PHAI-CHAN-r3.md` là bản sửa; dòng cuối mục 9 liệt kê thay đổi.

Việc: (1) `diff` hai bản, kiểm ba finding trên đã đóng thật (thử trong RAM: mô tả `502 (loi truyen tai)` không tiền tố `HTTP ` giờ có làm đỏ vế (a)–(c) của M3/M4 như N1 nói không); (2) rà nhanh có gì mới vỡ theo L1–L7.

Đầu ra stdout: bảng finding (đóng/chưa), finding mới P0–P3. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
