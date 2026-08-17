# ADR-0037 — Review Rescue Checkpoint và tách Stable Slice

- **Trạng thái:** Accepted (2026-08-17, phiên `grill-with-docs`; chủ kho phê duyệt)

Một PR phải vào Review Rescue Checkpoint khi đã dùng hết hai lượt Codex hoặc đã qua ba vòng code/review tổng
cộng mà chưa approve. Phần đã ổn chỉ được tách thành Stable Slice khi hữu ích độc lập, có acceptance và evidence
riêng, không phụ thuộc phần còn lỗi và không làm yếu security/gate; nó phải được dựng thành Packet/PR sạch rồi
review exact head mới. Phần chưa ổn thành Remediation Slice kế nhiệm, giữ finding IDs và lịch sử. Nếu finding cắt
ngang bất biến lõi thì không tách mà revision Packet/Mission hoặc xem lại thiết kế; hình dạng lỗi xuất hiện lần
thứ ba bắt buộc xét lại việc có nên tiếp tục cách làm đó. Quyết định này đổi thêm chi phí chia PR lấy khả năng
land giá trị đã chứng minh mà không kéo theo phần chưa hội tụ hoặc giữ một vấn đề mắc kẹt vô hạn.

Rework không preempt writer đang chạy. Khi slot kế tiếp mở, cùng priority thì rework đi trước Packet
chưa mở; khác priority thì Packet P cao hơn đi trước rework P thấp hơn. Quy tắc này cho phần đã có
evidence quay lại sớm mà không biến checkpoint thành quyền cướp slot.
