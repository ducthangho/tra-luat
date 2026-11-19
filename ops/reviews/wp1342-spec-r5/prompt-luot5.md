# Review độc lập ĐẶC TẢ — packet #1342 WP1174-WINDOWS-BACKEND r5 (bậc r1d-a1-ii), lượt 5

Bạn là reviewer độc lập, CHỈ ĐỌC; không sửa tệp, không commit, không gọi mạng. Giữ đầu ra gọn và LUÔN kết thúc bằng thông điệp cuối có dòng KET_LUAN.

- Cây làm việc = worktree tách rời của `origin/master` `4eda94e9effc6cfe7fcc0b3e3fb4151ad437ecbd`. Tệp chưa commit: `ops/specs/WP1174-WINDOWS-BACKEND-r5.md` (bản 5, sha256 627e4c8a71dab21e7a4aacb455be9ed9a0368df181d6f4c341522d3a24980911) và `ops/specs/WP1174-WINDOWS-BACKEND-r5-ban4.md` (bản bạn review lượt 4) để `diff -u`.
- Nguồn: r4 trên `origin/ops/wp1342-r4-spec`; hạ tầng test r4 `.claude/dev/packet_loop_test.py` 18560–18934 (`_wp1342a1_goi` 18702: với `viec=None` luồng quan sát trả ngay), `_module1174` 10647; sản phẩm `.claude/dev/packet_loop.py` 6830–6912.

Finding lượt 4 (của bạn) cần kiểm đã đóng: A1 P2 đường đo J4 thiếu thứ tự toàn phần; A2 P2 ngân sách thời gian chưa đủ cho hai lời gọi J4 và chuỗi chấm J12; A3 P3 nơi chạy a1@J12 ghi hai kiểu.

## Việc (đo bằng lệnh, ghi lệnh + rc)

1. Bảng trạng thái A1–A3.
2. Delta (§4 M1 đoạn "Ngân sách theo ca", M2 đường đo, N7, §11) có tạo lỗ mới hoặc mâu thuẫn nội tại không; kiểm số học ngân sách (J4: `het = now+75`, hai lời gọi `han=10`, ngưỡng 50/25; J5 `min(20, het-now-45)`; J12 dự phòng 25, ngưỡng chấm 20/15) bằng phép tính.
3. Chỉ P0–P2 chặn approve; P3 ghi kèm.

Nếu một hướng thử cần nội dung dạng đường dẫn thoát khỏi cây thư mục, MÔ TẢ BẰNG LỜI.

## Đầu ra

Tiếng Việt, gọn. DÒNG CUỐI CÙNG đúng một trong hai:
KET_LUAN: approve
KET_LUAN: request_changes
