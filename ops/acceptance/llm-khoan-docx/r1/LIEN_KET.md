# Cách đọc liên kết trong các VERDICT.md của packet #1525

Reviewer ghi `VERDICT.md` trong thư mục `.review/` của bản sao rời. Liên kết trong bản gốc tính từ chỗ ấy:

| Dạng trong VERDICT | Trỏ tới | Ở thư mục lưu này |
| --- | --- | --- |
| `../scripts/…`, `../docs/…`, `../ops/…` | gốc kho tại `reviewed_sha` | thêm `../../../../` phía trước (gốc kho cách 5 cấp) |
| `../../run/<id>/run.json` | hồ sơ launcher | `run.json` cùng thư mục |
| `../../run/<id>/prompt.snapshot` | prompt đã băm | `PROMPT.md` cùng thư mục |
| `/tmp/…` | nhật ký trong scratch của reviewer | KHÔNG lưu kèm (băm nhật ký nếu có ghi ngay trong verdict) |

Từ lượt 41 (r43), liên kết được viết lại theo bảng trên NGAY khi lưu, và đường dẫn tuyệt đối vào scratch đổi thành
neo `#nhat-ky-scratch` có ghi chú. Các lượt trước giữ nguyên chữ của reviewer (không biên nhận nào neo byte
các tệp ấy); đọc chúng theo bảng này. Nội dung đánh giá không đổi; chỉ đích liên kết đổi.
