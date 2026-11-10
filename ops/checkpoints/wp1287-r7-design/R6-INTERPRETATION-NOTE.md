# Ghi chú diễn giải bổ sung cho R4–R6

Ghi chú này bổ sung lịch sử; không đổi byte/hash của result, helper, log hay biên nhận R4–R6.

Advisory độc lập đã hoàn tất, được neo bằng [advisory-completion.json](../wp1287-r6/advisory-completion.json). Nó chỉ phân tích năm đầu vào được duyệt, không kiểm native raw và không phải formal approval.

1. Cụm “loader stage before chrome.dll” trong R6 phải được đọc như một giả thuyết. Helper chưa tách đầy đủ lỗi First/Next khỏi walk kết thúc bình thường. Không thấy entry không chứng minh DLL thực sự vắng mặt hoặc loader bị kẹt.
2. Các mốc5/15/25 là lịch dự kiến, không phải timestamp chính xác của toàn bộ snapshot. Có thêm tiến trình sau probe cuối; không kéo dài kết luận của mẫu25s tới toàn lượt chạy.
3. Chưa có exact loaded-path/file-identity/hash bridge cho uvh64.dll. Không quy lỗi cho UltraViewer/injection từ basename hoặc hash của tệp tìm riêng trên đĩa.
4. WCT thread nodes và không có cycle chưa xác định điểm chờ gây lỗi. Giá trị WaitTime không được tự gán đơn vị ms từ tên field helper cũ.
5. R6 openCLIrc0 khác với operatorrc2 do close timeout. Empty snapshot không xác nhận URL/readiness; startup, readiness và cleanup phải được báo riêng. Recovery thành công không xóa failure ban đầu.
6. RAM/commit là số đo tương quan. R4/R6 không phải cặp A/B có kiểm soát; không kết luận OOM hoặc loại trừ memory pressure chỉ từ commit còn trống.

OP-R6-LOCK-01 vẫn là lỗi vận hành của helper: nhả lock trong finally khi còn process chưa được cleanup. Helper kế nhiệm phải giữ khóa/handoff theo ownership và deadline cho tới khi cleanup được xác minh; không gán lỗi này cho sản phẩm H2.

Counter hiện hành sau advisory: shared3/8, design-advisory1/1, formal0/2, author3/3, productpush0/1, reservations0. Các số trong những đầu vào advisory là snapshot lịch sử, không phải reset counter hiện tại.

U10 và OP-F01 formal vẫn OPEN. [Thiết kế kế nhiệm](MEASUREMENT-DESIGN.md) giải quyết các khoảng trống đo; chưa có helper mới, native run, allowance hoặc lease mới được kích hoạt.
