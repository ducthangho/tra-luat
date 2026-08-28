# `BIA-MO-MOT-CHIEU` — bia mộ lease chỉ được cưỡng chế MỘT chiều, và đó là chiều KHÔNG gỡ khoá

Issue #372. Mở sau khi phiên điều phối 28-08-2026 dựng được phản chứng chạy được.

## Phép đo mở packet — chạy trên clone sandbox, tái lập được

```
NEN                                             SAU khi noi DUNG MOT dong vao cuoi tep lease
                                                `da_bi_thay_the: khong-he-ton-tai-lease-nay-bao-gio`

CÒN_HẠN  w1-p1-…-20260828  <- dang giu           CÒN_HẠN · ĐÃ_BỊ_THAY_THẾ  w1-p1-…-20260828
NGƯỜI_GIỮ 1                                      NGƯỜI_GIỮ 0: không có
rc = 11                                          rc = 0
```

Cái tên được trỏ tới **không tồn tại ở bất kỳ ref nào trong kho**. Cổng vẫn nhận.

`rc=0` + `NGƯỜI_GIỮ 0` là đúng cặp tín hiệu mà một phiên sắp ghi đọc thành *"đường trống, ghi
được"*. Write-set exclusion là **cơ chế duy nhất** chặn hai writer trên một tệp.

## Vì sao lỗ tồn tại — bất đối xứng có thật trong mã

`da_bi_thay_the` xuất hiện đúng **bốn** chỗ trong `ops/lease_publish.py`:

| dòng | vai trò |
|---|---|
| 565, 571 | trong `_kiem_bia_mo` — kiểm chiều **MỚI → CŨ**, chỉ chạy lúc `publish` |
| 930 | `da_chet = bool(lease.get("da_bi_thay_the")) and trang_thai == "CÒN_HẠN"` — **ĐỌC để loại khỏi phép đếm** |
| 947 | `con-tro-treo` **bỏ qua** lease mang khoá này |

Không dòng nào xác nhận **cái tên nó trỏ tới**. Chiều **CŨ → MỚI** — chiều duy nhất có tác dụng
**gỡ khoá** — không ai kiểm, và không đi qua `publish` lần nào.

## Đây KHÔNG phải chuyện kẻ gian, và spec này không được viết như thể là

Mọi phiên trong kho chạy bằng credential của chủ kho. "Sửa tệp lease của người khác" không đòi
đặc quyền gì. Nên mô hình đe doạ đúng là **TAI NẠN**, và tai nạn đã xảy ra:

> Lease `mcp-doc-phan-tich-exec-1r3-codex-20260828` (#359) bị thu hồi bằng một `da_bi_thay_the`
> **một chiều**, viết từ tệp lease của packet **KHÁC** (#368). Lần ấy **đúng** — #359 đã land
> thật. Không cơ chế nào kiểm điều đó. Nó đúng vì người viết cẩn thận, không vì cổng bắt phải đúng.

## Việc của packet

### 1. Vị từ đối xứng, chạy trong PHÉP QUÉT chứ không chỉ lúc đăng
Lease mang `da_bi_thay_the: X` chỉ được coi là đã chết khi **cả hai** đúng:
- `X` **tồn tại** ở một ref nào đó trong kho (cùng phạm vi quét mà `ai-dang-giu` đang dùng), **và**
- `X` mang `thay_the_cho` **chứa** lease này.

Chạy lúc đăng là **không đủ**: tai nạn nằm ở lease **CŨ** bị sửa sau lưng, mà lease cũ không đi
qua `publish` lần nào nữa.

### 2. Không thoả ⇒ `KHÔNG_XÁC_ĐỊNH`, KHÔNG phải "hết hạn", KHÔNG phải "vẫn giữ"
Doctrine `None ≠ False`: bia mộ không đối chứng được là thứ ta **không biết**. Mã thoát phải là
`RC_KHONG_XAC_DINH` (`rc=12`), cùng đường với các ca không đo được đã có. Đọc nó thành ĐẠT là tái
tạo đúng lỗ; đọc thành "vẫn giữ" là chặn oan hàng loạt lease đã thu hồi hợp lệ.

### 3. `thay_the_cho` phải nhận DANH SÁCH
`_kiem_bia_mo` đọc `str(lease.get("thay_the_cho"))` ⇒ một lease thay thế được **đúng một** lease.
Phiên W1-P1 cần thu hồi **hai** lease xác chết nên buộc phải viết một cái đúng cách và một cái một
chiều — tức schema **ép** người ta dùng sai. Nhận cả chuỗi (tương thích ngược) lẫn danh sách.

### 4. ĐẾM TRƯỚC KHI SIẾT — và con số ấy là đầu ra bắt buộc
Trước khi cổng siết, phải đếm được: **bao nhiêu lease trong toàn kho đang mang `da_bi_thay_the`
không đối chứng được**. Siết mà không đếm trước thì một loạt lease cũ hoá `rc=12` cùng lúc và
không ai phân biệt được "cổng mới bắt đúng" với "cổng mới hỏng". Con số này đi vào thân PR.

Nếu số ấy **lớn**, packet **DỪNG và BÁO** — cách chữa khi ấy là một đường **thu hồi tử tế**
(việc 5), không phải siết cổng rồi đi dọn hậu quả.

### 5. Đường THU HỒI lease — chỉ khi việc 4 cho thấy cần
Nợ `AG-T0-01B-thu-hoi-lease-chua-co-duong` (đo 21-08: **5** quyền ghi còn sống sau khi packet đã
land) là **lý do người ta mượn `da_bi_thay_the` làm đường thu hồi**. Chừng nào chưa có lệnh
`thu-hoi` thì việc 1 chỉ đóng cửa mà không mở cửa nào.

Việc này **có thể tách packet riêng** — quyết định theo con số ở việc 4, và ghi rõ đã quyết thế nào.

## Phản chứng bắt buộc (mỗi cái là một ca `tNN_`, không phải một câu trong tài liệu)

Kho có bài học: *"NGHĨ RA được phép thử mà KHÔNG CHẠY nó thì phép thử ấy KHÔNG TỒN TẠI."*

| ca | phải |
|---|---|
| `da_bi_thay_the` trỏ tên **không tồn tại** | `rc=12`, KHÔNG phải `rc=0` |
| `da_bi_thay_the` trỏ lease **có thật** nhưng lease ấy **không** trỏ ngược lại | `rc=12` |
| bia mộ **hai chiều đầy đủ** | vẫn được coi là đã chết, `NGƯỜI_GIỮ` giảm đúng như hôm nay |
| `thay_the_cho` là **danh sách 2 phần tử**, cả hai có bia mộ trỏ ngược | ĐẠT |
| `thay_the_cho` là danh sách, **một** phần tử thiếu bia mộ | CHẶN |
| hai lease trỏ **vòng** vào nhau (`A→B`, `B→A`) | phải có kết quả XÁC ĐỊNH, không treo, không đệ quy vô hạn |

Và **đột biến canh chính bản vá**: nới vị từ mới thành `if False` phải làm ca đích ĐỎ. Không có
đột biến ấy thì không biết ca đang đo luật mới hay đo thứ khác.

## write set

- `ops/lease_publish.py`
- `ops/lease_publish_test.py`

Đo lúc 2026-08-28T07:2xZ sau khi so hai nguồn ref bằng TẬP TÊN: **cả hai `NGƯỜI_GIỮ 0`**.

## Ràng buộc

- **KHÔNG bỏ hành vi gỡ.** `t91_A2c_da_bi_thay_the_van_in_nhung_khong_giu` khoá đúng hành vi ấy có
  chủ đích, kèm đột biến canh. Thứ thiếu là **đối chứng cho lời khai gỡ**, không phải hành vi gỡ.
- **KHÔNG dựng danh sách CẤM.** Kho đã trả giá 7 lần cho hình dạng *"danh sách cấm đội lốt
  allow-list"* trong riêng packet #348. Vị từ ở đây phải là phép **so bằng nhau** trên tên lease,
  không phải phép dò chuỗi.
- Phép quét lease phải giữ nguyên chốt hai-nguồn-ref hiện có; **không fetch được ref nào ⇒ ĐỎ**.
  "Không đo được" không phải "không có".

## KHÔNG ĐO ĐƯỢC — khai thẳng, đừng biến thành lời khai

- Số lease đang mang bia mộ không đối chứng được: **chưa đếm** (đó là việc 4).
- Hành vi khi bia mộ trỏ vòng: **chưa dựng**.
