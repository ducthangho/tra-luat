# ĐẶC TẢ ĐÓNG BĂNG — `MCP-DOC-PHAN-TICH`

> Đặc tả này **không cấp việc**. Phải có Issue + lease còn hiệu lực (`docs/PROTOCOL_DA_PHIEN.md`
> §3.2, §4) mới được bắt tay. Phiên nào đọc rồi tự làm là tự cấp việc cho mình.
>
> Sửa đặc tả đã có băm ⇒ đi qua **bản sửa đổi mới**.

`packet_id`: `MCP-DOC-PHAN-TICH`
`packet_issue`: `359`
`revision`: `3` · `generation`: `1`
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

## `write_set` — MỞ RỘNG ở bản sửa đổi 3

```yaml
- type: exact
  path: .claude/dev/mcp_github_doc.py
- type: exact
  path: .claude/dev/mcp_github_doc_test.py
- type: exact
  path: .claude/dev/launcher.py
- type: exact
  path: .claude/dev/launcher_test.py
```

`launcher.py` **VÀO** write set. `S3` của bản 2 được **gỡ**, và chỉ gỡ bằng thẩm quyền chủ kho.

Đo trước khi mở: `ai-dang-giu` trên `.claude/dev/launcher.py` và `launcher_test.py` ⇒
**`NGƯỜI_GIỮ 0`** cả hai. Master drift `693d68f..fe6152b` (5 tệp) **không chạm** hai tệp ấy.

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


---

# BẢN SỬA ĐỔI 3 — mở `launcher.py`, vì vá vòng ngoài đã thua HAI lần

## Vì sao phải sửa đặc tả thay vì vá tiếp

Bản 2 cấm đụng `launcher.py` (`S3`). Dưới lệnh cấm ấy, packet chọn **tái sử dụng một phần**
`_doc_mcp_json` — và chính lựa chọn đó đẻ ra một lớp hỏng mới, đo được qua hai vòng review:

| vòng | finding | trạng thái |
|---|---|---|
| 1 | URL và `headers` đến từ **hai ảnh chụp** ⇒ có thể gửi token của B tới A | vá bằng so băm trước/sau |
| 2 | **ABA đánh bại so băm**: A → B (trong lúc launcher đọc) → A. Hai băm khớp, launcher trả URL của B, client đọc headers của A | **bản vá THUA** |

Đây là **mâu thuẫn kiến trúc**, không phải cẩu thả:

| hướng | được | mất |
|---|---|---|
| ủy quyền `_doc_mcp_json` | giết lớp "hai công cụ bất đồng" | buộc **hai lần đọc** ⇒ đua |
| tự phân tích | một ảnh, hết đua | **tái sinh** lớp trôi lệch mà packet sinh ra để giết |

Không có đường thứ ba **trong** ràng buộc của bản 2. Chủ kho gỡ `S3` in-session `2026-08-27`.

## `objective` (bản 3)

`_doc_mcp_json` trả về **cả `headers`** (hoặc một biến thể trả đủ), để client lấy URL và
`headers` từ **MỘT lời gọi, MỘT ảnh chụp**. Khi ấy đua biến mất **theo cấu trúc**, không phải
bị canh — và lớp trôi lệch vẫn chết vì client vẫn không tự phân tích.

## `acceptance_criteria` (bản 3) — cộng vào bản 2, không thay thế

10. `_doc_cau_hinh` gọi **đúng MỘT** lần vào tầng phân tích và nhận đủ URL + `headers`.
    Phản chứng **ABA** (A → B → A quanh lời gọi) phải **không còn ghép nhầm được**, và ca
    test phải dựng đúng chuỗi ấy.
11. **Không phá caller cũ của `_doc_mcp_json`.** Nó đang được `doctor` dùng qua hợp đồng
    bốn giá trị. Giữ hợp đồng cũ dùng được, hoặc **chuyển caller một cách tường minh** và
    chứng minh `doctor` không hồi quy. Đo, đừng khai.
12. `launcher_test.py` phải có ca cho phần mới. **`t117` vẫn phải xanh** — mỗi mẫu đột biến
    khớp ĐÚNG MỘT chỗ trong `launcher.py`; thêm mã có thể phá tính duy nhất ấy. Đo, đừng đoán.
13. **Bộ phân hạng mutant không được bị lừa bởi việc ĐỔI KIỂU NGOẠI LỆ.** Đo được ở vòng 2:
    `except Exception: raise AssertionError(...)` trong `mcp_github_doc_test.py:143` biến một
    `AttributeError` vô can thành `AssertionError`, nên `_phan_hang_dot_bien` đếm là GIẾT THẬT.
    Ý định của dòng ấy đúng, cách làm thì tự phá thước đo.
    ⇒ Tín hiệu "assertion của ca đích" phải là thứ **mã triển khai không giả được** — ví dụ
    một lớp ngoại lệ riêng, hoặc một dấu hiệu do chính khung ca sinh ra — chứ không phải cái
    tên `AssertionError` mà bất kỳ `except` nào cũng dựng lên được.
    **Chốt ngược:** sau khi sửa, một mutant chết vì `AttributeError` phải rơi vào hạng
    **TÍN DỤNG GIẢ**, kể cả khi trên đường đi có một `except` đổi kiểu.
14. `read_bytes()` (và mọi lời gọi hệ tệp sau pha phân tích) ném `OSError` phải được chuyển
    thành `Hong`; `_main` không được để lọt traceback thay cho `KHONG_DO_DUOC/CHAN`.

## Ngân sách (bản 3)

`≤6` tệp / `≤1000` dòng thêm+xoá từ `base_sha`. Hiện dùng **256**. Mở write set **KHÔNG** nới
trần kích thước.

## Điều kiện dừng (bản 3)

`S1` `S2` `S5` giữ nguyên. **`S3` GỠ** (được sửa `launcher.py`). `S4` giữ nguyên: không được
xoá khác biệt PHẠM VI hợp lệ. Thêm:

- `S6` sửa `_doc_mcp_json` làm `doctor` hoặc `launcher_test.py` hồi quy ⇒ DỪNG, trình phép đo.
- `S7` phải đụng đường dẫn thứ năm ngoài write set ⇒ DỪNG.
