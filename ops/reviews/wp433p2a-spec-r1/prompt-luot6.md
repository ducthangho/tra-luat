Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 6, cho đặc tả `ops/specs/GWS-CRED-DICH-NGOAI-KHO-A-r1.md` (packet P2a, Issue #433, phạm vi POSIX). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp (nếu /tmp chỉ đọc, mô phỏng trong RAM và ghi rõ).

Clone master 3b647461db7c8ded1bddd9aafc5c6aa5eead223f, cộng chưa commit: đặc tả cần review; `ops/specs/GWS-CRED-DICH-NGOAI-KHO-A-r1-ban6.md` là bản bạn review lượt 5 (sha256 0560b8bf…); verdict lượt 1–4 ở `ops/reviews/wp433p2a-spec/luot{1,2,3,4,5}.verdict.txt`.

Quyết định chủ kho là RÀNG BUỘC, không nêu lại: §2/§9 (P2b, P2c, Q2, Q4 đã quyết), Q1 trần riêng ≤ 3 tệp / ≤ 550 dòng thêm. Q3 chặn lease không chặn review — không nêu.

Việc:
1. Diff với `-ban6.md`. Hai finding lượt 5 (P2 `pc_probe_quyen` thiếu `winerror`, P3 §8 năm/sáu): đã đóng THẬT chưa — dựng lại đúng bộ phân loại sai bạn đã dùng (mọi `OSError` có `winerror`) và đo phản chứng mới có đỏ không.
2. Sửa có làm vỡ chỗ khác không (đẳng thức N9(c), tổng §4b, nhãn, thứ tự lượt).
3. Chỉ nêu finding MỚI nếu nó là lỗ đo hoặc tự mâu thuẫn có bằng chứng; không nêu lại finding đã đóng.

Đầu ra stdout: bảng finding lượt 5 (đóng / chưa), finding mới P0–P3 (chỗ, vấn đề, bằng chứng, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
