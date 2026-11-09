# P2 U10 — thiết kế chẩn đoán kế nhiệm, chưa cấp quyền chạy

Phạm vi: Packet #1287 hiện blocked; không đổi H2 cleanup, pin CLI, browser, timeout hoặc máy đích. Đây là đầu vào cho checkpoint r4, không phải một phép thử đã chạy hoặc lease mới.

Nguồn đọc lại: `P2-node24-diagnostic-original/browser-evidence/open.stderr` trong hồ sơ gốc của P2. CLI báo daemon exit1 sau Timeout30000ms. Chrome full CFT đã được tạo PID5108; log kết thúc ở `<launched>`, không có xác nhận kết nối remote-debugging-pipe. Không có bằng chứng trong log này rằng Chrome đã crash, rằng Node24 là nguyên nhân, hoặc rằng tăng timeout giải quyết được lỗi. Phép đo RAM hiện tại của D4 cũng không giải thích được thời điểm lỗi cũ.

Giả thuyết cần phân biệt: tiến trình khởi động nhưng không hoàn tất handshake; tiến trình con thoát mà stderr chưa được thu; tài nguyên hoặc chính sách của host ảnh hưởng khởi động. Mỗi giả thuyết hiện là chưa xác minh. Không gọi các phiên bản CLI đã thất bại là giải pháp.

Thiết kế phép đo có giới hạn cho r4: đúng Desktop, đúng bộ ghim hiện hành, cùng fixture và timeout30000; tối đa một lượt tái hiện có instrumentation. Thu log debug launcher/browser, census PID/parent/creation/executable trong thời gian chạy, mã thoát thật nếu quan sát được, tài nguyên tại thời điểm khởi động và sự kiện hệ thống có cửa sổ thời gian chính xác. Lưu command/config/hash/runtime/culture/session và toàn bộ stderr/stdout. Chỉ theo dõi cây tiến trình sở hữu; không đọc hồ sơ/cookie của người dùng, không đổi policy hoặc tắt sandbox/antivirus để lấy PASS. Không coi `headless_shell` mở được là acceptance của full CFT.

Trước khi chạy cần r4/spec/descriptor/allowance/ownership/lease đã đóng băng theo protocol, ghi tiếp chi phí và ba author đã dùng; không dùng budget #1296. Nếu instrumentation không tạo bằng chứng phân biệt được giả thuyết thì dừng, không thử phiên bản hoặc flag ngẫu nhiên. Mọi sửa sản phẩm hoặc bộ ghim phải trở thành checkpoint cụ thể riêng, chưa được tài liệu này cho phép.

Nếu U10 chưa được đóng, P3 và rollout tiếp tục blocked. Không dùng code gate xanh hoặc canary Linux để thay native acceptance.
