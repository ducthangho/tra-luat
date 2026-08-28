# ĐẶC TẢ ĐÓNG BĂNG — `MCP-DOC-PHAN-TICH`

> Đặc tả này **không cấp việc**. Phải có Issue + lease còn hiệu lực (`docs/PROTOCOL_DA_PHIEN.md`
> §3.2, §4) mới được bắt tay. Phiên nào đọc rồi tự làm là tự cấp việc cho mình.
>
> Sửa đặc tả đã có băm ⇒ đi qua **bản sửa đổi mới**.

`packet_id`: `MCP-DOC-PHAN-TICH`
`packet_issue`: `359`
`revision`: `2` · `generation`: `1`
`review_class`: **`sensitive`** — tệp chuyển `${GITHUB_PAT}` tới một endpoint ngoài.
`risk`: `normal` — trần ADR-0044 `≤3 tệp/≤300 dòng` gắn với packet **chạm authority**;
`.claude/dev/**` là dev-side, NGOÀI gói phát hành, không cổng nào đọc.

## Vì sao đặc tả này tồn tại — và một phép đo đáng ghi

Lease `revision 1` được đăng **thiếu `spec_hash`**, và executor `codex` DỪNG hai lượt liên
tiếp vì đúng chỗ đó (`§3.2` liệt `spec_hash` trong schema tối thiểu; *"Khi vào `ready`, spec
được đóng băng bằng `spec_hash`"*). Nó từ chối tự suy giá trị, và nó **đúng**.

Phiên điều phối đo lại toàn kho:

```text
tong lease tren origin/master : 74
co truong spec_hash           :  2
```

Tức **protocol đòi, thực tế 3% làm**. Lease `r1` của packet này theo thói quen của 72 cái
kia. Đây không phải lỗi của executor, cũng không phải một mình phiên này — nhưng packet nào
bị chặn thì packet đó trả, nên đặc tả này ra đời. Con số `2/74` là **nợ khai**, không thuộc
phạm vi packet này chữa.

## `nguon_cap_viec`

Nợ khai lúc land **PR #357** (packet #355). Ba finding P2 của connector để MỞ có chủ đích,
thành Issue #359. Chủ kho chốt in-session `2026-08-27`: *"cấp lease và làm như các lần"*.

## `objective`

Thôi TỰ phân tích `.mcp.json` trong `.claude/dev/mcp_github_doc.py`; giao phần phân tích và
chọn cho bộ chuẩn `launcher.py::_doc_mcp_json`, để lớp *"hai công cụ bất đồng về cùng một
tệp"* chết theo **kiến trúc** chứ không theo bản vá.

### Vì sao đổi kiến trúc chứ không vá lẻ

| hình dạng | số lần trong #355 |
|---|---|
| đầu vào méo được chấp nhận | **3** — `isError` · `mcpServers` hỏng · `headers` falsy |
| lệch bộ phân tích chuẩn | **2** — chọn khoá · tìm gốc dự án |

Số finding **tăng** theo vòng (`1 → 1 → 3`). Ngưỡng CLAUDE.md là ba. Tiền lệ: **BẢY** phát
hiện cùng một đường ở bộ gỡ `shell_environment_policy`, chữa bằng đổi kiến trúc.

## `write_set`

```yaml
- type: exact
  path: .claude/dev/mcp_github_doc.py
- type: exact
  path: .claude/dev/mcp_github_doc_test.py
```

`launcher.py` **NGOÀI** write set. Mở rộng hợp đồng của nó là điều kiện dừng `S3`.

## `acceptance_criteria`

1. `_doc_cau_hinh` dùng `launcher._doc_mcp_json` cho: kiểm lược đồ, chọn khoá theo **CÓ MẶT**,
   khớp `github` bằng `casefold()`, từ chối khi nhiều tên khớp, lấy tên và URL.
2. **Tìm gốc** neo theo vị trí tệp như `launcher` (`__file__.parents[2]`), `TL_GOC` ghi đè.
3. `headers`: **vắng mặt** ⇒ mặc định `{}`; `null` `[]` `""` `0` `false` ⇒ **từ chối trước khi
   ra mạng**. Quyết định về `null` phải viết ra, không để lửng lơ.
4. **SSE**: nối các trường `data` TRONG cùng một event, giữ ranh giới event, và chọn event là
   **response JSON-RPC** (`id` + `result`/`error`) — không lấy mù event cuối.
5. **URL và `headers` phải đến từ MỘT ảnh chụp.** Đọc hai lần rồi ghép là đường rò rỉ
   credential: cấu hình đổi giữa hai lần đọc ⇒ gửi token của endpoint B tới endpoint A.
   Phát hiện-rồi-fail-close là ĐẠT; **cấm khai "đã loại bỏ race"** — cửa sổ vẫn còn, chỉ là
   không còn ghép nhầm âm thầm.
6. **Bộ đo mutant không được cấp tín dụng giả.** "Bị giết" CHỈ KHI ca đích đỏ bằng
   `AssertionError` của chính nó. Chết vì lỗi vô can ⇒ **hạng thứ ba**, báo riêng.
7. Mỗi chốt có **đột biến riêng** làm ca đích ĐỎ. Không test nào gọi mạng thật; đồ giả mô
   phỏng **TRẠNG THÁI**.
8. Khác biệt **PHẠM VI** hợp lệ phải được **khai**, không được "thống nhất" bằng cách xoá:
   `launcher` chấp nhận khai kiểu `stdio` không URL là "có khai"; client HTTP từ chối vì thiếu
   URL. Xoá khác biệt này là điều kiện dừng `S4`.
9. `launcher.py doctor` không hồi quy. Bốn chốt của #355 (`.port`, `isError`, chọn khoá theo
   có mặt, khớp tên `casefold`) không hồi quy.

## `dieu_kien_dung`

- `S1` cần đường dẫn thứ ba ngoài write set
- `S2` vượt `1000` dòng thêm+xoá tính từ `base_sha`
- `S3` phương án gọn nhất đòi sửa `launcher.py`
- `S4` tái sử dụng làm mất một khác biệt phạm vi hợp lệ
- `S5` `origin/master` đã đi tiếp so `base_sha` mà chưa đo lại

## Ngoài phạm vi

- Sửa `launcher.py` dưới mọi hình thức.
- Chữa nợ `spec_hash 2/74` cho các lease khác.
- Thêm đường ghi thứ ba vào registry/Drive.
