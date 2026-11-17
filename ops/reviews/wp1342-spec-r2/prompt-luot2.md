Bạn là reviewer ĐỘC LẬP (họ OpenAI) cho một ĐẶC TẢ packet, chưa có mã. CHỈ ĐỌC; không ghi tệp nào trong thư mục làm việc; không gọi mạng.

Thư mục làm việc: git worktree kho tra-luat trên base master 39ce682 cộng tệp đặc tả `ops/specs/WP1174-WINDOWS-BACKEND-r2.md` (bản sửa sau review lượt 1). Kết quả review lượt 1 của bạn nằm ở `ops/specs/.luot1-review.txt` (đọc phần báo cáo cuối: bảy finding F1–F7).

Việc:
1. Với từng finding F1–F7 của lượt 1: bản sửa có đóng được nó không? Đo lại bằng mã nơi có thể (ví dụ: dựng trong bộ nhớ một helper đúng mô tả M7 từ `_new1342` và kiểm base/base, thêm hàm hợp lệ, sửa byte hàm r1; kiểm hàm `_1174_win_lock` không decorator trả context manager từ generator nội bộ có được `_new1342` nhận và `_wired1342` không báo).
2. Bản sửa có sinh lỗi MỚI không: mâu thuẫn giữa M1 (sáu API) và M2/M3/B1; đột biến B1 (xoá `GetHandleInformation`) có thật sự chỉ làm B1 đỏ hay làm L2 đỏ trước (L2 dùng `GetHandleInformation`); M3 vòng đời tên tạm và P6; N2 phản chứng thứ ba (thêm decorator) có làm helper M7 khác `[]` đúng không.
3. Kiểm lại L1–L7 cho các ô đã đổi; L7: mọi câu hỏi/báo/chờ chủ kho có mã E.

Đầu ra stdout: (1) bảng F1–F7: đóng/chưa đóng kèm bằng chứng; (2) finding MỚI P0–P3 (chỗ, vấn đề, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
