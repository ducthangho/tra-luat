# Log review THÔ — chưa thành bản ghi verdict

**Thư mục này KHÔNG phải `ops/reviews/`.** Không tệp nào ở đây là một bản ghi verdict hợp
lệ: không biên nhận, không `evidence_url`, không hàng mục lục, không `t26`/`t27` canh. Đừng
trích dẫn chúng như verdict đã ghi nhận.

## Vì sao có thư mục này

Bảy lượt review của chuỗi `doctor-github-mcp` (lease `..review-{1,2,3,4,5,7,8}-codex-20260817`)
có **lease trong kho** nhưng **không có biên nhận**. `ops/reviews/README.md` đã khai lớp nợ
này. Đầu ra của chúng chỉ còn sống trong scratchpad của **một container ephemeral**, và
container bị thu hồi theo thời gian chờ — nên chúng đang ở tình trạng "sắp mất hẳn", không
phải "chưa sắp xếp".

Chép vào đây là **bảo toàn**, không phải **công nhận**. Nó biến một mất mát không đảo ngược
thành một việc còn làm được.

## Cơ sở của cách đặt tên — và giới hạn của nó

Tên tệp gắn `review-N` theo trường `ten` mà launcher ghi (`reviewN-mcp`). Lời khai ấy được
**đối chứng bằng nội dung**, không phải tin suông:

| điểm đối chứng | kết quả |
|---|---|
| `review6-mcp` (`runs/8b15e79c`) ↔ `doctor-github-mcp-review-6-codex-verdict.md` đã ghi | **sha256 TRÙNG KHỚP** |
| `review9-mcp` (`runs/20fd83d5`) ↔ `doctor-github-mcp-review-9-codex-verdict.md` đã ghi | **sha256 TRÙNG KHỚP** |

Hai lượt duy nhất có bản đã ghi để so — và **cả hai đều khớp từng byte**. Quy ước
`reviewN-mcp` → lượt N vì thế có bằng chứng, không phải suy đoán từ tên.

**Nhưng chốt mạnh hơn thì KHÔNG khớp, và phải nói ra:** `head` trong `run.json` của các
lượt 2–9 **không bằng** `reviewed_sha_required` của lease nào. Riêng lượt 1 (`52c9c105`)
thì khớp lease 1. Với lượt 6 và 9, `head` của run cũng khác `reviewed_sha` trong biên nhận
**đã ghi** — trong khi nội dung lại trùng từng byte. Nghĩa là `run.json.head` (head của
workspace lúc launcher chạy) **không phải** cùng một đại lượng với SHA reviewer khai đã đọc.
Đó là một chỗ chưa ai giải thích, và nó là **lý do chính** khiến các tệp này chưa được nâng
thành verdict chính thức: nâng lên là phải khai `reviewed_sha`, mà đại lượng ấy đang có hai
nguồn nói khác nhau.

## Muốn nâng thành bản ghi verdict thì phải làm gì

1. **Giải cho xong chuyện `reviewed_sha`.** Đọc `reviewed_sha:` trong THÂN mỗi log (thứ
   reviewer tự khai) rồi đối chiếu với `reviewed_sha_required` của lease. Thân log là nguồn
   có thẩm quyền hơn `run.json.head`; nếu hai thứ vẫn lệch thì khai thẳng thành caveat.
2. Chép nguyên văn sang `ops/reviews/<lease_id>-verdict.md`, đối chiếu `diff -q`.
3. Viết `*.receipt.yaml` + nâng caveat lên `ops/reviews/README.md` (`t27` đỏ nếu thiếu).
4. Theo **hai commit**: verdict đứng riêng trước, rồi biên nhận + mục lục — để
   `evidence_url` neo được vào một commit đã chứa tệp.

Caveat **bắt buộc** cho cả bảy, đã biết trước: dụng cụ đo của chúng nằm trong scratchpad và
**đã mất**, nên mọi con số trong thân log là **lời khai**, không phải phép đo tra lại được.

## Nội dung

Mỗi lượt hai tệp: `*.log` (nguyên văn `stdout`, **không sửa một byte**) và `*.run.json`
(trích tỉnh lược `run.json` của launcher — định danh, thời gian, `ma_thoat`, `head`,
`prompt_sha256`, commit gốc).
