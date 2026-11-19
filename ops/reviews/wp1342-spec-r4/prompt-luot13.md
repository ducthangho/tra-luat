Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 13 — LƯỢT XÁC NHẬN DUY NHẤT (chủ kho cấp đúng một lời gọi, §9 Q9) — cho đặc tả `ops/specs/WP1174-WINDOWS-BACKEND-r4.md` (Issue #1342, bậc r1d-a1-i). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Clone master e2c3b82 (cộng chưa commit): bản 12 tại `ops/specs/WP1174-WINDOWS-BACKEND-r4-ban12.md` (sha256 7d73c43f…); bản mới là `ops/specs/WP1174-WINDOWS-BACKEND-r4.md`; verdict lượt 12 ở `ops/reviews/wp1342-spec-r4/luot12.verdict.txt`; phần test của head PR thi công (#1407, `728eccab`) ở `ops/reviews/wp1342-spec-r4/head_packet_loop_test.py` (để đối chiếu thứ tự kiểm J9, không review mã).

Phạm vi CHỈ là:
1. `diff` bản 12 → bản mới: liệt kê mọi thay đổi; xác nhận chỉ chạm câu J9 ở M7, §9 Q9 và §11 nhật ký.
2. Finding P2 lượt 12 đã ĐÓNG: câu J9 mới đọc và lưu `ActiveProcesses` ngay sau khi hàm ném, chấm nhãn k2 ("phụ chưa signaled trong 5 s VÀ thiếu cleanup:xac_nhan") trước, rồi con, sau cùng mới assert kết quả đã lưu; dưới k2 ca đỏ ĐÚNG nhãn k2 (không phải nhãn job chưa rỗng); dưới a1 ca vẫn phân biệt với k2 (có `cleanup:xac_nhan`); đường sạch vẫn đạt (job rỗng khi hàm trả được kiểm bằng giá trị đã lưu). Đối chiếu thứ tự với mã head.
3. §4b/N7 không còn câu nào mô tả thứ tự kiểm J9 mâu thuẫn với câu mới; không hồi quy ở phần không đổi.

Đầu ra stdout: danh sách thay đổi của diff, đánh giá (2)(3), finding nếu có (P0–P3). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
