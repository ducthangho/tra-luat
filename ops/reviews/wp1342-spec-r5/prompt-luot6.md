# Review độc lập ĐẶC TẢ — packet #1342 WP1174-WINDOWS-BACKEND r5 (bậc r1d-a1-ii), lượt 6

Bạn là reviewer độc lập, CHỈ ĐỌC; không sửa tệp, không commit, không gọi mạng. Giữ đầu ra gọn và LUÔN kết thúc bằng thông điệp cuối có dòng KET_LUAN.

- Cây làm việc = worktree tách rời của `origin/master` `4eda94e9effc6cfe7fcc0b3e3fb4151ad437ecbd`. Tệp chưa commit: `ops/specs/WP1174-WINDOWS-BACKEND-r5.md` (bản 6, sha256 0550af2102ab4616f2639572195bb28bcb01346d35d5be70af62284df53e0791) và `ops/specs/WP1174-WINDOWS-BACKEND-r5-ban5.md` (bản bạn review lượt 5) để `diff -u`.

Finding lượt 5 (của bạn): A2 P2 còn mở ở J4 — đọc/xoá tệp kết quả giữa hai lời gọi có thể vượt 5 s rồi làm lời gọi thứ hai thiếu ngưỡng 25 s; cần hạn GỘP cho đọc/xoá.

## Việc

1. A2 đã đóng chưa (kiểm số học: `het = now+75`; trước lời gọi đầu ≥ 50; mỗi lời gọi `han=10` + `xac_nhan` 5 + `reap` 5; đọc/xoá gộp 5 s; trước lời gọi thứ hai ≥ 25).
2. Delta (chỉ M1 đoạn ngân sách và §11) có tạo mâu thuẫn mới không. Không mở lại các mục lượt 1–5 đã đóng trừ khi delta chạm tới.
3. Chỉ P0–P2 chặn approve; P3 ghi kèm.

## Đầu ra

Tiếng Việt, gọn. DÒNG CUỐI CÙNG đúng một trong hai:
KET_LUAN: approve
KET_LUAN: request_changes
