# Đánh giá quy trình theo pattern và delta-only

| Nội dung | Hiện hành (protocol8/8.3/12) | Pilot theo yêu cầu mới |
|---|---|---|
| Phân loại | Đã có stable ID/lớp nguyên nhân | Giữ lớp, bổ sung danh mục mọi dạng cú pháp/điểm gọi trước khi vá |
| Neo finding | Có anchors/evidence | Finding mới bắt buộc file + start_line/end_line ở exact SHA; validator từ chối thiếu |
| Lượt sau | Đối chiếu lượt trước, quét lớp trên candidate | Discovery chỉ H2→H mới; đọc ngữ cảnh để hiểu hunk, regression xác minh lỗi cũ |
| Lỗi cũ | Đối chiếu trạng thái | Giữ trong bảng trạng thái ID cũ; validator cấm lặp ID/slug cũ trong findings[] |
| Không hội tụ | Checkpoint sau ba lượt/trần riêng | Giữ checkpoint; đợt này đã xét lại trước lời gọi reviewer vì phép thử mở rộng bắt dạng còn sót |

Số đo nguồn cuối: B→H401 dòng thêm/ba tệp; H2→H46 thêm+22 xoá=68 dòng thay đổi/một tệp. Phạm vi discovery giảm83,04% theo số dòng (68/401). Đây không phải tỷ lệ tiết kiệm token hoặc thời gian.

Bash Linux35/35 kiểm tra trên nguồn cuối; native PowerShell5.1/7 dùng lại70/70 kiểm tra, với cả năm block byte-identical và hash riêng chứng minh. Không gọi70 ca này là vừa chạy trên toàn tệp mới. Core selftest1777/1777 cũng được dùng lại cho byte nguồn core không đổi. Những số component gồm ca dương/âm, config và mutant; không phải105 ca browser.

Phép thử mở rộng phát hiện hai Setup Bash version-query rc17 còn bị nhận thành công (33/35). Đã sửa chung bằng gán kết quả trước rồi mới so sánh; 35/35 sau vá. Lỗi này thuộc PREFLIGHT-001 cũ, không tạo ID/finding mới. R19 bị dừng trong snapshot trước model-child: giữ terminal và bằng chứng, shared vẫn6 trước reviewer thực. Đây là bằng chứng mẫu cho lợi ích quét toàn lớp và cũng là giới hạn của bộ test đầu tiên.

Đã thử validator bằng năm đối chứng: verdict hợp lệ, ID/slug cũ bị báo mới, thiếu line, sai delta scope và thiếu bảng trạng thái lớp cũ. Đối chứng đạt5/5. Validator kiểm hợp đồng/schema; không chứng minh reviewer thực sự đã đọc đúng phạm vi hoặc đủ ngữ nghĩa.

Đánh giá tạm: giảm phần đọc lại và tránh đếm lại lỗi cũ; quét nhiều dạng cú pháp bắt thêm lỗi cùng gốc. Chi phí ban đầu tăng do lập ledger/test/receipt. Chưa có A/B model hay số liệu token nên chưa chứng minh nhanh hơn hoặc rẻ hơn tổng thể. Delta-only có nguy cơ bỏ lỗi nền/cắt ngang; full review r18, regression lớp cũ, đọc phụ thuộc cần thiết và nghĩa vụ OP-F01/U10/assurance giữ lại giúp giới hạn rủi ro. Kết quả independent delta review sẽ được cập nhật sau, không tự đóng acceptance từ các số kiểm tra trên.
