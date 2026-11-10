# Quy trình vá và review theo lớp lỗi — pilot WP1287

1. Đóng băng SHA cũ, SHA mới và ledger. Prompt/spec phải giữ nguyên byte UTF-8 canonical: dùng binary writer và kiểm hash ở máy nhận với hash từ control; không tính lại hash sau khi writer tự đổi newline rồi coi là khớp. Dùng helper/đối chứng `../wp1287-r21/freeze_packet.py` và `test_freeze_packet.py`; mismatch dừng trước model. Bootstrap phải thử đúng đường tool và mọi native capability cần cho delta, giữ sandbox/read-only/never. Một lớp nguyên nhân có stable slug/ID; các biểu hiện có file:line riêng. Chốt tất cả vị trí tương tự trong write set trước khi sửa.
2. Vá cả lớp, chạy đối chứng dương/âm và mutant khôi phục từng cơ chế cũ. Ghi đúng shell/nền đã chạy, không dùng tổng suite để thay bằng chứng đóng lớp.
3. Lượt đầu đọc full diff. Từ lượt sau, discovery chỉ đọc diff SHA đã review → SHA mới, đọc ngữ cảnh cần thiết để hiểu thay đổi. Kiểm lỗi cũ bằng regression và bảng trạng thái ID cũ; không phát hành lại thành finding mới.
4. Finding mới bắt buộc: ID, pattern, severity, file, dòng đầu/cuối tại exact SHA, trigger/evidence, hướng vá chung, test khóa và rủi ro. Lỗi cũ chưa sửa tiếp tục chặn theo ID cũ; lỗi do patch sinh ra dùng ID mới chỉ khi cơ chế mới.
5. Hết ba chu kỳ mà chưa hội tụ: dừng vá nối tiếp, xét lại thiết kế/phạm vi/phép thử. Trần riêng chặt hơn vẫn thắng. Không reset lịch sử vì đổi revision.
6. Đánh giá bằng phạm vi diff, độ phủ biểu hiện, duplicate count, lớp đóng/mới/tái mở, thời gian và call thực. Không suy tiết kiệm token/thời gian từ số dòng đơn thuần.

Phạm vi: pilot của Packet1287 theo chỉ thị chủ kho; không tự sửa protocol chung, nới assurance hoặc đóng acceptance thiếu phép đo. Người vá không tự nhận là reviewer độc lập.
