# `CHAN-DOAN-TIN-DUNG-GIA` — revision 2

| trường | giá trị |
|---|---|
| `packet_id` | `CHAN-DOAN-TIN-DUNG-GIA` |
| `packet_issue` | #568 |
| `revision` | 2 |
| `revision tiền nhiệm` | 1 (spec `e00be7c46d89e2fd…`, đã thi công ở PR #572) |
| `executor` | `claude` |
| `assurance_target` | `human_audited` — không đổi so r1 |
| `review_class` | `sensitive` — vẫn chạm CHÍNH bộ phân hạng đột biến |
| `base` | `eb4a9aba05ecd82d028497d2352615877f6f5ac6` (head PR #572 sau khi hoà base gen 2) |

## `nguon_cap_viec`

Phát hiện khi rà PR #572 trước audit, đăng kèm phản chứng chạy được tại
[#568 issuecomment-5749389651](https://github.com/ducthangho/tra-luat/issues/568#issuecomment-5749389651).
Chỉ thị chủ kho, nguyên văn: **"Cấp r2 đi"**.

## Vì sao đây là REVISION chứ không phải generation

`PROTOCOL_DA_PHIEN.md:300`: *"Mở rộng phạm vi hay đổi closure là revision mới, generation mới và cấp lại lease."*

Đặc tả r1 khai `M2` **đúng cho nhánh `p.returncode != 1`**. Ca dưới đây có `rc == 1`, nên nó **nằm ngoài chữ** của r1 — không phải r1 làm sai, mà r1 không hứa. Gen 2 đã khai thẳng *"KHÔNG mở rộng bất kỳ thứ gì"*. Đóng ca này là **đổi closure** ⇒ revision.

## Bệnh — đã ĐO, có phản chứng chạy được

Con chết vì một ngoại lệ **không bắt được** ⇒ CPython thoát **`rc=1`**, `stdout` **RỖNG** (chết trước khi in được dòng `TU KIEM` nào). Bốn nhánh của `chay_dot_bien_tu_kiem` định tuyến như sau:

| nhánh | |
|---|---|
| `if do_khac:` | rỗng ⇒ bỏ qua |
| `elif p.returncode != 1:` | **rc ĐÚNG BẰNG 1** ⇒ bỏ qua |
| `elif do_chot == set(dich):` | `set()` ≠ `dich` ⇒ bỏ qua |
| `else:` | in `0 — ca do THUC TE: (rong)`, rồi lặp `kh_chot` — **RỖNG** ⇒ không in gì nữa |

`p.stderr` mang nguyên nhân **bị vứt**. Kết quả là **một nhãn trần không nói nguyên nhân** — đúng bệnh (B) mà r1 sinh ra để chữa, sống sót ở một đường đi tới được.

Đường này CÓ THẬT: bất kỳ đột biến nào sinh ra mã chết ở **mức module** (`SyntaxError`, `NameError` ngoài hàm, `ImportError`) đều cho đúng hình dạng `rc=1` + `stdout` rỗng. Bộ đột biến là phép thay chuỗi, nên đó là kết cục hoàn toàn khả dĩ.

**Nói ĐÚNG mức độ:** ca vẫn được đếm là `hong` **chính xác**; cặp `(giet, hong)` không đổi. Lỗ `#355`/`#359` **KHÔNG** bị mở lại. Đây là lỗ **CHẨN ĐOÁN**, không phải lỗ **PHÂN HẠNG**.

## `write_set` — MỘT đường, y như r1

```
ops/nhanh_don_duoc_test.py
```

Đo `20-09-2026 ~17:2xZ`: `ai-dang-giu` ⇒ `NGƯỜI_GIỮ 1: chan-doan-tin-dung-gia-r1-g2-claude` (CÒN_HẠN). Vì **cùng packet** và **cùng write set**, r2 **kế vị** r1-g2 bằng bia mộ hai chiều; cấp chồng mà không kế vị là tự dựng cửa sổ hai writer.

Một tệp, trong trần `ADR-0044:5` cho class `sensitive` (≤3 tệp, ≤300 dòng thêm). **Không xin ngoại lệ nào.**

## `ngoai_pham_vi` — CỐ Ý không làm

| thứ | vì sao |
|---|---|
| Chữa nguyên nhân của (A) — `r506` chết vì lỗi vô can trên runner | Vẫn **KHÔNG TÁI HIỆN ĐƯỢC**. Vá một thứ chưa dựng được phản chứng là ĐOÁN |
| Chữa `CASE T6` | Nợ riêng, **chưa có chủ**. Chưa ai đo được nó cùng gốc với packet này — xem `issuecomment-5744407812` |
| Nới bộ phân hạng | Dựng lại đúng lỗ `#355`/`#359`. **Cấm tuyệt đối** |
| Đổi `run(check=True)` sang ném `TinHieuChotCa` | ĐẢO NGƯỢC phân biệt mà `#355` trả giá để có |
| Thêm `timeout`/`retry` | Vá cho (A), tức ĐOÁN; retry còn che mất tín hiệu |
| Chạm `ops/nhanh_don_duoc.py` | Sản phẩm không sai; bộ ĐO mới thiếu |

## `muc_tieu`

`M1`–`M5` của r1 **đã thi công** (PR #572) và **không mở lại**. r2 thêm đúng một mục tiêu:

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M6** | Khi con thoát `rc=1` mà **không ca nào** báo `DO_KHAC` lẫn `DO_CHOT` (tức chết trước khi in được gì), nhánh thứ ba phải in `stderr` của con qua `_goi_chan_doan` — cùng phép cắt-và-khai như `M2`. Phân hạng **KHÔNG đổi**: ca vẫn là `hong`, `(giet, hong)` y hệt | `ops/nhanh_don_duoc_test.py` |

## `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| **A8** | `rc=1`, `stdout` rỗng, `stderr` mang chuỗi mốc ⇒ dòng cha phải chứa chuỗi mốc ấy | Đột biến bỏ nhánh in `stderr` ⇒ ca ĐỎ |
| **A9** | Phân hạng **không đổi**: trên bảng đầu vào có đủ bốn nhãn, cặp `(giet, hong)` bằng đúng cặp của r1 | Đột biến đổi một nhánh phân hạng ⇒ cặp lệch ⇒ ca ĐỎ |
| **A10** | Ca `rXX_` mới nằm trong `NHOM_BAT_BUOC`, có **đột biến riêng**, `SAN_NHOM` cập nhật | Bỏ đột biến của ca mới ⇒ `thieu` khác rỗng ⇒ suite ĐỎ |
| **A11** | Toàn bộ `ops/nhanh_don_duoc_test.py` ⇒ `rc=0`, `TU KIEM N/N` **hai số bằng nhau**, `dot bien giet M/M` **hai số bằng nhau** | Bất kỳ ca nào đỏ |
| **A12** | Delta so nền `eb4a9ab`: nền đã đo `rc=0 · 80/80 · 24/24`; ứng viên phải `rc=0` và `dot bien giet = 80 + (số đột biến mới)`, hai vế dựng trong **MỘT** lệnh | Hai vế dựng ở hai thời điểm ⇒ phép đo vô hiệu, **không phải** ĐẠT |

## `hinh_dang_ke_thua`

| hình dạng | số | ghi chú |
|---|---|---|
| `LOI-KHAI-RONG-HON-PHEP-DO` | **3** | Không đổi |
| `TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO` | **2** | Không đổi |
| `VA-DUNG-CHO-DUOC-CHI-ROI-BO-SOT-DUONG-THU-BA` | **2** | **NÂNG từ 1.** `#513` lượt 10→13 là lần một; chính r1 là lần hai — nó đóng ba nhánh ở ca THƯỜNG rồi bỏ sót ca SUY BIẾN của nhánh thứ ba |

**Bài học chật hơn, ghi vào đây vì r1 đã trả giá để có:** *đóng một nhánh ở ca thường **không phải** là đóng nhánh ấy.* Mỗi nhánh còn có ca suy biến của nó (tập rỗng, đầu vào rỗng, không ai báo gì) — và ca suy biến mới là chỗ chẩn đoán biến mất.

**Cơ hội tái phát đã biết của r2:** `M6` thêm **đường thứ tư** vào cùng một chỗ. Phải tự liệt kê hết đường TRƯỚC khi vá, và cho mỗi đường một chốt riêng phân biệt được bằng đầu vào — nếu hai chốt không phân biệt được thì chúng là bộ TƯƠNG ĐƯƠNG và ta chỉ đang đo một cái.

## `chua_do_duoc` — ghi thẳng

| # | thứ không đo được | trạng thái |
|---|---|---|
| **D1** | Ca này đã từng xảy ra thật trên runner chưa | **KHÔNG ĐO ĐƯỢC.** Log Actions có hạn lưu, và chính vì khuyết tật này mà log cũ không phân biệt được |
| **D2** | Nguyên nhân của (A) | **KHÔNG TÁI HIỆN ĐƯỢC** trên Linux container. Không phải "không có" |
| **D3** | `gate (windows-latest)` | `manual_ci_budget: 0`. Là **CHỌN KHÔNG ĐO** |
| **D4** | `CASE T6` có cùng gốc với packet này không | **KHÔNG ĐO ĐƯỢC** — thứ phân biệt bị huỷ trước khi được ghi |

## Quan hệ với PR #572 — khai trước cho khỏi cãi sau

PR #572 mang **r1** và đang **chờ audit người** với ba required check XANH trên `eb4a9ab`. r2 **KHÔNG** đụng vào nó: r2 thi công trên nhánh riêng cắt từ `eb4a9ab`, mở PR riêng.

Hệ quả của việc r2 kế vị r1-g2, nói thẳng: sau khi bia mộ có hiệu lực, **r1 không còn quyền ghi**. PR #572 vẫn **audit và merge được bình thường** — mất quyền GHI không phải mất quyền LAND. Nếu audit tìm ra chỗ cần sửa, chỗ sửa ấy đi dưới r2.

## Điều r2 KHÔNG hứa

Nó **không** làm PR #567 merge được. Nó **không** làm `gate-registry` xanh trên master. Nó **không** chữa `CASE T6`. Nó đóng đúng một đường mà r1 để hở, và đường ấy **chưa từng bắn** trong một lượt CI nào đã quan sát được.
