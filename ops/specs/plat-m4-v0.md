# ĐẶC TẢ — `PLAT-M4` vòng vá V0 (Issue #194, PR "#204")

Đặc tả này ĐÓNG BĂNG bằng băm. Lease neo vào `spec_sha256`. Sửa nội dung ⇒ băm đổi ⇒ lease
trỏ vào thứ không còn tồn tại, phải đi qua bản sửa đổi mới. Soạn bằng skill `soan-spec`.

| khoá | giá trị |
|---|---|
| `packet_id` | `PLAT-M4` |
| `packet_issue` | 194 |
| `nguon_cap_viec` | `ops/reviews/plat-m4-review-1-codex-verdict.md` — finding P2 duy nhất, verdict `changes_requested` neo `5813fc45` |
| `review_class` | `systemic` — chạm `.claude/dev/**`, KHÔNG chạm `.github/workflows/**` và KHÔNG chạm cổng đăng lease |
| `hinh_dang_ke_thua` | `khong_ap_dung` — đây không phải packet khắc phục một hình dạng lỗi lặp; là vòng vá thứ nhất sau một verdict |

## write_set
- `.claude/dev/launcher.py`
- `.claude/dev/launcher_test.py`

Không đường dẫn nào khác. Lease, prompt và đặc tả này nằm trên nhánh `ops/**` RIÊNG, cố ý
không nằm trên nhánh packet — đã trả giá một finding P1 vì chuyện đó ở `#195`.

## ngoai_pham_vi — CỐ Ý không làm
1. **Bốn hàng thiếu trong `ops/reviews/README.md`.** Hai bản thẩm định xếp nó vào V0, nhưng ĐO
   trên master: `python3 ops/lease_publish_test.py` ⇒ **35/35, rc=0**, `t27` XANH. Chỗ đỏ nằm ở
   cây gom bằng chứng của phiên thẩm định, không nằm ở kho. Nó chỉ thành việc thật khi các
   verdict trên nhánh `ops/**` land.
2. **E4/C5 (launcher in biên nông như thể là root).** Write set trùng, nhưng gộp làm packet
   sắp-sạch phình ra. Để riêng.
3. **Mọi thứ thuộc `V1`–`V6`.** Packet này không đụng `ops/lease_publish.py`, không dựng
   integration branch, không xoá `t34`.

## muc_tieu — mỗi dòng chiếu vào một đường dẫn ở `write_set` (L2)
1. `_do_mcp_endpoint` TỪ CHỐI một URL mang `userinfo` (`user:secret@host`) và **không gọi
   `urlopen`** cho nó. → `.claude/dev/launcher.py`
2. Phép nhận URL đổi từ khớp TIỀN TỐ CHUỖI sang PHÂN TÍCH CẤU TRÚC: `urlsplit`, chỉ nhận
   `scheme ∈ {http, https}`, đòi `hostname` hợp lệ, từ chối khi `username` hoặc `password`
   khác `None`. → `.claude/dev/launcher.py`
3. Ca kiểm khẳng định cả hai vế: nhãn trả về là `khong_do_duoc` **và** nhật ký `urlopen` RỖNG.
   → `.claude/dev/launcher_test.py`
4. Các dạng đã chặn được từ trước (`file://`, `ftp://`, `gopher://`, `url` rỗng) KHÔNG ĐỔI
   hành vi. → `.claude/dev/launcher_test.py`

## nghiem_thu — mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3)
| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| A1 | `http://user:secret@127.0.0.1/mcp` ⇒ `khong_do_duoc`, `urlopen_calls == []` | ca mới; gỡ chốt `username`/`password` ⇒ ca ĐỎ |
| A2 | `https://user:secret@example.test/mcp` ⇒ y hệt A1 | như trên, đúng một ca đỏ |
| A3 | bí mật KHÔNG xuất hiện trong bất kỳ chuỗi trả về nào | ca đọc `mo_ta` và khẳng định không chứa chuỗi bí mật; in thẳng `url` vào thông điệp ⇒ ĐỎ |
| A4 | `scheme` lạ vẫn `khong_do_duoc` như cũ | ca cũ giữ nguyên; nhận bừa mọi scheme ⇒ ĐỎ |
| A5 | đường thuận không hỏng: URL sạch vẫn probe được | nền `N/N`; chặn nhầm URL sạch ⇒ ĐỎ |
| A6 | suite đầy đủ `N/N`, hai số BẰNG NHAU, `rc=0` | rc trần không đủ — phải đọc dòng `N/N` |
| A7 | mỗi đột biến giết **đúng một** ca | đột biến giết 0 ca ⇒ ca không có răng; giết nhiều ca ⇒ ca trùng phạm vi |

Đột biến chạy trên **bản sao tạm**, không ghi vào tệp thật.

## chua_do_duoc
- Hành vi Windows của các ca mới: sandbox này là Linux. Bằng chứng Windows phải đến từ lượt CI
  trên đúng head, không từ lời khai.
- `mcp-endpoint` gọi ra mạng thật: ca kiểm dùng `urlopen` giả, nên đo HỢP ĐỒNG chứ không đo
  đường mạng.
