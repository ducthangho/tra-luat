# Đặc tả packet `PLAT-X8b` — trả phép đo cho chuẩn hoá traversal

- **Issue:** #255 · **depends_on:** `PLAT-X8` (#225, đã land `647cfead`)
- **Trạng thái:** đã duyệt · **duyệt bởi:** `ducthangho`, 23-08-2026

## 0. Số nền — đo lúc nào, trên gì

| thứ | giá trị | đo trên |
|---|---|---|
| master | `1ef928db` | 23-08-2026 00:32Z |
| bộ test `ops/lease_publish_test.py` | **87** ca, `87/87` `rc=0` | master `1ef928db` |
| `_BANG_LOP` | **7** mục, **0** mục dưới `sensitive` | master `1ef928db` |

Theo **L5** (`soan-spec/SKILL.md`): mọi con số trên đây kèm mốc, và phải **đo lại** trước mỗi bước
công bố. Sàn nghiệm thu neo bằng **quan hệ**, không bằng giá trị: `N_sau = N_trước + 1`.

## 1. Vấn đề — đo được, không suy luận

Bản vá P1 của `PLAT-X8` xoá 4 mục `systemic` khỏi `_BANG_LOP`. **Đúng về đầu ra.** Nhưng nó xoá luôn
đích DUY NHẤT mà một đường traversal có thể hạ lớp xuống — bảng nay chỉ còn mục `sensitive`. Hệ quả:
bước `posixpath.normpath` trong `_tinh_lop_tu_write_set` **không còn ca nào đo**.

Mã sản phẩm **ĐÚNG**. Thứ mất là **PHÉP ĐO**.

Bốn trạng thái, đo trên cây sạch `git archive`, `rc` đọc trực tiếp (`echo $?` ngay sau lệnh — không
pipeline, không `$( )` cùng chuỗi):

| trạng thái | kết quả |
|---|---|
| nền | `87/87` `rc=0` |
| xoá hẳn `posixpath.normpath`, không ca mới | `87/87` `rc=0` — **0 ca ĐỎ** |
| thêm ca mới, mã nguyên vẹn | `88/88` `rc=0` |
| ca mới + xoá `normpath` | `87/88` `rc=1`, đúng và **CHỈ** ca mới ĐỎ |

`t83` **XANH** ở cả hai lượt đột biến — bằng chứng DƯƠNG TÍNH rằng nó không còn đo normalization,
không phải suy từ đọc mã.

Đây đúng hình dạng `A14` mà chính `PLAT-X8` dựng ra để chống: *"vế DƯƠNG phải sống"*.

## 2. muc_tieu — mỗi mục chiếu vào một đường dẫn trong write set

1. Thêm **một** ca test khoá lại normalization, bằng cách bơm một mục **thấp hơn `sensitive` TẠM**
   vào `_BANG_LOP` trong phạm vi ca (cùng nếp `t77`/`t81`/`A14`), rồi đòi traversal qua đúng mục ấy
   vẫn ra `sensitive` — cho **cả** `""` lẫn `"planned:"`. → `ops/lease_publish_test.py`

## 3. ngoai_pham_vi — CỐ Ý không làm

1. **KHÔNG sửa `ops/lease_publish.py`.** Mã sản phẩm đúng; thiếu là phép đo. Sửa mã ở đây là chữa
   nhầm bệnh.
2. **KHÔNG nới `_BANG_LOP` thật.** Giữ đúng 7 mục theo `§8:572`. Mục thấp hơn chỉ được bơm TRONG ca
   test, không vào bảng seed.
3. **KHÔNG sửa/xoá `t83`.** Ca mới **bổ sung** phép đo, không thay `t83`.

## 4. Tiêu chí nghiệm thu

| mã | tiêu chí | phép đo nào làm nó ĐỎ |
|---|---|---|
| `B1` | suite `N/N`, hai số BẰNG NHAU, `bỏ qua=0`, `rc=0`, và `N = 87 + 1` | số lệch ⇒ ĐỎ |
| `B2` | **đột biến**: xoá dòng `posixpath.normpath(duong)`, giữ nguyên phần còn lại ⇒ ca mới **ĐỎ** | không đột biến thì không biết ca đang đo gì |
| `B3` | **vế DƯƠNG**: ca mới XANH khi mã nguyên vẹn | bắt bản vá quá tay biến cổng thành máy luôn trả `sensitive` |
| `B4` | `t83` XANH ở cả hai chiều | ca mới bổ sung, không thay `t83` |
| `B5` | write set đúng **một** tệp `ops/lease_publish_test.py` | chạm tệp khác ⇒ ĐỎ |
| `B6` | CI trên exact head, đo **THEO JOB**: cả `ubuntu-latest` lẫn `windows-latest` `success` | *"PR xanh"* không đủ — `ci.yml` chỉ chạy `ubuntu` cho PR thường |
| `B7` | trần `ADR-0044`: ≤3 tệp / ≤300 dòng thêm — packet này **thừa sức**, không cần ngoại lệ | vượt ⇒ phải xin, đừng đẩy im lặng |

## 5. Giới hạn — đọc trước khi tin packet này

Packet này mua **PHÉP ĐO** cho một nhánh bảo vệ, không mua tính đúng của nhánh ấy. Nó chứng minh
*"xoá `normpath` thì có ca ĐỎ"*; nó **không** chứng minh `_tinh_lop_tu_write_set` đúng với mọi đầu
vào đối kháng. Và nó **không** dựng cổng cấu trúc chặn ai đó sau này nới `_BANG_LOP` rồi xoá ca —
`t86` đã khai đúng nợ ấy, packet này không đóng.
