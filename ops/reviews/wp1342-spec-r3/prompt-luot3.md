Bạn là reviewer ĐỘC LẬP (họ OpenAI) cho một ĐẶC TẢ packet, chưa có mã. CHỈ ĐỌC; không ghi tệp nào trong thư mục làm việc; không gọi mạng.

Thư mục làm việc: git worktree kho tra-luat trên master 39ce682, cộng `ops/specs/WP1174-WINDOWS-BACKEND-r2.md` (đã đóng băng) và `ops/specs/WP1174-WINDOWS-BACKEND-r3.md` (bản sửa sau review lượt 2). Kết quả lượt 1, 2 của bạn ở `ops/specs/.luot1-review.txt`, `ops/specs/.luot2-review.txt`.

Việc: (1) F5 (lượt 2) đã đóng chưa — B2 nay patch `winreg.OpenKeyEx`/`QueryValueEx` trên đường mặc định, seam `doc=` bị bỏ, thêm đột biến (h); kiểm trong RAM rằng đột biến fallback (h) bị B2 giết và (f) vẫn giết đúng dòng REG_SZ với giá trị chuỗi số; (2) soát toàn đặc tả lần cuối theo L1–L7 của `.claude/skills/soan-spec/SKILL.md`: mâu thuẫn giữa các ô, phép đỏ không thể đỏ, câu hỏi/báo/chờ chủ kho thiếu mã E.

Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
