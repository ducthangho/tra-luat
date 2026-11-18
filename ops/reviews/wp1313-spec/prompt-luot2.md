Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 2, cho đặc tả `ops/specs/LAUNCHER-5XX-KHONG-PHAI-CHAN-r2.md` (Issue #1313). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử thì chạy trong RAM hoặc bản sao trong /tmp.

Thư mục làm việc: worktree kho tra-luat trên master 13bf69f, có r1 (lượt 1 của bạn ra request_changes với F1–F5 P2) và r2 (bản sửa, mục 9 liệt kê thay đổi).

Việc:
1. Kiểm từng F1–F5 của lượt 1 đã đóng thật trong r2 (đối chiếu mã `.claude/dev/launcher.py`, `.claude/dev/launcher_test.py`).
2. Rà TOÀN BỘ r2 theo L1–L7 của `.claude/skills/soan-spec/SKILL.md`: phần mới (M6, M7, đột biến `r1313_rest_mo_ta_noi_chan`, `r1313_canh_kho_gop_moi_that_bai`, ma trận chéo N1, tập ca đóng N3, vế (g) 600 và (h) 429) có phép đỏ đỏ được không; M7 có khả thi với khuôn giả của `t103`/`t115` không (`gh auth status` thành công trong khi `rest-kho` trả từng trạng thái); M6 có đổi cờ/kết luận nào không; neo đột biến cũ có còn khớp đúng một chỗ không.
3. Còn chỗ thứ ba cùng suy diễn "thất bại ⇒ bị chặn" mà r2 bỏ sót không?

Đầu ra stdout: bảng F1–F5 (đóng/chưa), finding mới P0–P3 (chỗ, vấn đề, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
