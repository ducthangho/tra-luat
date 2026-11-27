# Cách đọc liên kết trong các VERDICT.md của packet #1525

Reviewer ghi `VERDICT.md` trong thư mục `.review/` của bản sao rời. Liên kết trong bản gốc tính từ chỗ ấy:

| Dạng trong VERDICT | Trỏ tới | Ở thư mục lưu này |
| --- | --- | --- |
| `../scripts/…`, `../docs/…`, `../ops/…` | gốc kho tại `reviewed_sha` | thêm `../../../../` phía trước (gốc kho cách 5 cấp) |
| `../../run/<id>/run.json` | hồ sơ launcher | `run.json` cùng thư mục |
| `../../run/<id>/prompt.snapshot` | prompt đã băm | `PROMPT.md` cùng thư mục |
| `/tmp/…` | nhật ký trong scratch của reviewer | KHÔNG lưu kèm (băm nhật ký nếu có ghi ngay trong verdict) |

Từ lượt 41 (r44), liên kết được viết lại NGAY khi lưu: mã và tài liệu (`scripts/`, `docs/`) ghim vào blob tại
`reviewed_sha` (`https://github.com/ducthangho/tra-luat/blob/<reviewed_sha>/<đường dẫn>#L<n>` — dòng đúng như reviewer đọc,
không trôi theo checkout); hồ sơ `ops/` giữ đường dẫn tương đối trong kho; `run.json`/`PROMPT.md` cùng thư mục; mọi đích scratch
hay ngoài kho trỏ neo `#nhat-ky-scratch` — mục cuối mỗi verdict liệt kê các đích ấy. Đã đọc ngược từng liên kết của lượt
41–44 (lượt 44 viết lại ở r46 theo P3 lượt 45; lượt 45 không có liên kết): blob tồn tại tại SHA, số dòng nằm trong tệp, tệp đồng gói có mặt, neo có thật. Các lượt trước giữ nguyên chữ của reviewer (không biên nhận nào neo byte
các tệp ấy); đọc chúng theo bảng này. Nội dung đánh giá không đổi; chỉ đích liên kết đổi.
Liên kết blob chỉ mở được trên GitHub khi commit ấy đã được push; trước đó đọc bằng `git show <reviewed_sha>:<đường dẫn>`.
