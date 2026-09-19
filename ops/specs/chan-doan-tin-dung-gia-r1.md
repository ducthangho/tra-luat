# `CHAN-DOAN-TIN-DUNG-GIA` — revision 1

| trường | giá trị |
|---|---|
| `packet_id` | `CHAN-DOAN-TIN-DUNG-GIA` |
| `packet_issue` | #568 |
| `revision` | 1 |
| `executor` | **chưa gán** — xem `chua_do_duoc` `C1` |
| `assurance_target` | **chưa chốt** — xem `chua_do_duoc` `C1` |
| `review_class` | `sensitive` — chạm bộ phân hạng đột biến, tức chạm CHÍNH cổng đo răng |
| `base` | `dc85dd0a34188238aa6537ce843ff3688e488fd3` |

## `nguon_cap_viec`

Nợ #568, mở theo chỉ thị chủ kho *"Mở nợ ngay"* sau khi `gate-registry (ubuntu-latest)` ĐỎ trên
head `57f85a1` của PR #567 với `DELTA = 0` so nền.

## Vấn đề — nói ĐÚNG phạm vi, vì có HAI thứ và chỉ MỘT cái packet này chữa

### (A) `r506` chết vì lỗi VÔ CAN trên runner — **KHÔNG TÁI HIỆN ĐƯỢC**, ngoài phạm vi packet này

Đo 19-09-2026 trên container này, bằng phản chứng chạy riêng một đột biến:

| điều kiện | số lượt | nhãn |
|---|---|---|
| tải thường, 2,4s/lượt | 4 | `GIET_THAT` 4/4 |
| ép tải gấp đôi số nhân (4 nhân · 8 tiến trình quay vòng), 4,1–6,4s/lượt | 6 | `GIET_THAT` 6/6 |

**10/10 `GIET_THAT`.** Thời gian giãn 2,7 lần mà nhãn không đổi ⇒ giả thuyết "nhạy tải" **chưa có
bằng chứng**, và cũng chưa bị bác. Trạng thái: **`KHÔNG TÁI HIỆN ĐƯỢC ở nền Linux container`**.

Packet này **KHÔNG** hứa chữa (A). Hứa như thế là khai rộng hơn phép đo.

### (B) Khi (A) xảy ra, log CI KHÔNG ĐỦ để biết nó chết vì gì — **ĐÂY** là thứ packet này chữa

`ops/nhanh_don_duoc_test.py:2607`:

```python
do_khac = set(re.findall(r"^TU KIEM (r\d+): DO_KHAC", p.stdout, re.M))
```

Bắt **chỉ tên ca**. Tiến trình con *có* in đủ chẩn đoán (dòng 2645):

```python
print(f"TU KIEM {ten}: DO_KHAC — {type(exc).__name__}: {exc}")
```

Cha giữ `p.stdout` trong tay, rồi in ra đúng một dòng **không** mang kiểu ngoại lệ lẫn thông điệp:

```
DOT BIEN TU KIEM cham-doc-stdout-vo-dieu-kien | r512 | TIN DUNG GIA: ca chet vi loi VO CAN ['r506']
```

Hệ quả đo được: từ log CI của run `35438656966` **không cách nào** biết `r506` ném
`AssertionError` (git thất bại — `run(check=True)` ném lớp ấy TRẦN), `TypeError`, `OSError` hay
`TimeoutExpired`. Bốn nguyên nhân ấy cần bốn cách xử khác nhau, mà log không phân biệt nổi cái nào.

Đúng họ bài học *"cổng không nói dối — nó VẮNG MẶT"*: chẩn đoán **có tồn tại**, đi qua đúng một
hàm, rồi biến mất ở lớp cuối.

## `write_set` — MỘT đường

```
ops/nhanh_don_duoc_test.py
```

Đo 19-09-2026 `11:4xZ`: `ai-dang-giu ops/nhanh_don_duoc_test.py` ⇒ **`NGƯỜI_GIỮ 0`** (5 lease
`HẾT_HẠN`, 0 `CÒN_HẠN`). Không giao với packet nào đang mở.

Một tệp, nằm gọn trong trần `ADR-0044:5` cho class `sensitive` (≤3 tệp, ≤300 dòng thêm). **Không
xin ngoại lệ nào.**

## `ngoai_pham_vi` — CỐ Ý không làm

| thứ | vì sao |
|---|---|
| Chữa nguyên nhân của (A) | Chưa tái hiện được. Vá một thứ chưa dựng được phản chứng là ĐOÁN — `CLAUDE.md` gọi thẳng đó là cách người ta ở lại quá lâu trong một cái hố |
| Nới bộ phân hạng để `r506` chết vô can vẫn được tính GIẾT | Đó là dựng lại đúng lỗ `#355`/`#359` vừa bịt. Cấm tuyệt đối |
| Thêm `timeout` / `retry` cho `r506` | Là một bản vá cho (A), và lại là ĐOÁN. Thêm retry còn che mất tín hiệu |
| Đổi `run(check=True)` sang ném `TinHieuChotCa` | Sẽ biến một hỏng hạ tầng thành "chốt của ca" — ĐẢO NGƯỢC đúng phân biệt mà `#355` trả giá để có |
| Chạm `ops/nhanh_don_duoc.py` | Sản phẩm không sai; bộ ĐO mới thiếu |

## `muc_tieu`

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M1** | `chay_dot_bien_tu_kiem` in **NGUYÊN** dòng chẩn đoán của con cho mỗi ca `DO_KHAC`: tên ca **và** kiểu ngoại lệ **và** thông điệp — không cắt ở tên | `ops/nhanh_don_duoc_test.py` |
| **M2** | Cùng thế cho nhánh `p.returncode != 1`: in kèm `stderr` của con (cắt trần độ dài), vì ca ấy thường là con chết trước khi in được gì | `ops/nhanh_don_duoc_test.py` |
| **M3** | Chẩn đoán in ra phải **không** đổi phép PHÂN HẠNG: cùng đầu vào ⇒ cùng `giet`/`hong` như trước bản vá | `ops/nhanh_don_duoc_test.py` |
| **M4** | Thông điệp của con có thể **nhiều dòng** (một `AssertionError` của `run()` mang cả `stdout` lẫn `stderr` của git). Phải in được phần sau dòng đầu, hoặc khai rõ đã cắt và cắt ở đâu — im lặng nuốt là tái lập đúng (B) | `ops/nhanh_don_duoc_test.py` |
| **M5** | Ca `rXX_` mới khoá M1–M4, nằm trong `TU_KIEM`, và có **đột biến riêng** trong `DOT_BIEN_TU_KIEM` — `NHOM_BAT_BUOC` đòi thế | `ops/nhanh_don_duoc_test.py` |

## `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| **A1** | M1: cho con in `TU KIEM r506: DO_KHAC — AssertionError: rc=128: git init` ⇒ dòng cha phải chứa **cả** `r506`, `AssertionError` **và** `rc=128` | Đột biến quay `re.findall` về mẫu chỉ-tên (`r"^TU KIEM (r\d+): DO_KHAC"`) ⇒ ca ĐỎ |
| **A2** | M2: con thoát `rc=2` và `stderr` có chuỗi mốc ⇒ dòng cha chứa chuỗi mốc ấy | Đột biến bỏ phần `stderr` khỏi dòng in ⇒ ca ĐỎ |
| **A3** | M3: chạy `chay_dot_bien_tu_kiem` trên bảng đột biến GIẢ có đủ bốn nhãn (`GIET` · `DO_KHAC` · `rc≠1` · `do_chot≠dich`) ⇒ cặp `(giet, hong)` **bằng đúng** cặp của bản trước vá | Đột biến đổi một nhánh phân hạng ⇒ cặp lệch ⇒ ca ĐỎ |
| **A4** | M4: thông điệp con có dòng thứ hai mang chuỗi mốc ⇒ hoặc dòng cha chứa nó, hoặc cha in nhãn cắt tường minh **và** số ký tự đã cắt | Đột biến nuốt lặng phần sau dòng đầu ⇒ ca ĐỎ |
| **A5** | M5: `NHOM_BAT_BUOC` chứa ca mới, và `dot bien giet` = `len(DOT_BIEN_TU_KIEM)` | Bỏ đột biến của ca mới ⇒ `thieu` khác rỗng ⇒ suite ĐỎ |
| **A6** | Toàn bộ `ops/nhanh_don_duoc_test.py` ⇒ `rc=0`, `TU KIEM: N/N` **hai số bằng nhau**, `dot bien giet M/M` **hai số bằng nhau** | Bất kỳ ca nào đỏ |
| **A7** | Delta so nền `dc85dd0a`: nền đã đo `rc=0 · 76/76`; ứng viên phải `rc=0` và `dot bien giet` = `76 + (số đột biến mới)` trên cả hai vế dựng trong **MỘT** lệnh | Hai vế dựng ở hai thời điểm ⇒ phép đo vô hiệu, không phải ĐẠT |

## `hinh_dang_ke_thua`

Chép từ hồ sơ tiền nhiệm `#355`/`#359` (bộ phân hạng tín dụng giả) — packet này là hậu duệ trực tiếp:

| hình dạng | số đã đếm | ghi chú |
|---|---|---|
| `LOI-KHAI-RONG-HON-PHEP-DO` | **3** | Kế thừa từ `#566`. Packet này thêm một cơ hội tái phát: hứa chữa (A) trong khi chỉ chữa (B) |
| `TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO` | **2** | `#355` lượt 1 (`except Exception → AssertionError`), `#359`. Áp vào đây: dòng chẩn đoán in ra **không** được thành thứ mà một ca khác khớp nhầm |
| `VA-DUNG-CHO-DUOC-CHI-ROI-BO-SOT-DUONG-THU-BA` | **1** | `#513` lượt 10→13. Áp vào đây: có **hai** nhánh in `TIN DUNG GIA` (`do_khac` và `rc != 1`) và **một** nhánh `do_chot != dich` — đóng cả ba, đừng đóng mỗi nhánh đầu |

## `chua_do_duoc` — ghi thẳng

| # | thứ không kiểm được từ phiên này | trạng thái |
|---|---|---|
| **C1** | Executor và `assurance_target` | **CHƯA CHỐT.** Class `sensitive`; `codex` hết quota review, `agy` hết quota lúc soạn. Chủ kho quyết tại thời điểm cấp lease |
| **C2** | Nguyên nhân của (A) | **KHÔNG TÁI HIỆN ĐƯỢC** trên Linux container, 10/10 lượt. Không phải "không có" |
| **C3** | (B) đã vá có làm (A) chẩn đoán được thật không | **KHÔNG ĐO ĐƯỢC cho tới lần tái phát sau.** Packet này mua khả năng ĐỌC, không mua một lời giải |
| **C4** | Vá (B) có làm `gate-registry` xanh không | **KHÔNG.** (B) là chẩn đoán, không phải bản vá. Nếu (A) tái phát thì cổng vẫn ĐỎ — chỉ khác là lần sau đọc được lý do |
| **C5** | Ca này đã xảy ra bao nhiêu lần trước đây | **KHÔNG ĐO ĐƯỢC.** Log Actions có hạn lưu, và chưa có sổ nào đếm `TIN DUNG GIA` theo thời gian |

## Điều packet này KHÔNG hứa, nói một lần nữa cho khỏi đọc nhầm

Nó **không** làm PR #567 merge được. `gate-registry` là required status check của ruleset; merge
#567 hiện trả `405 Repository rule violations found`. Packet này chỉ bảo đảm rằng **lần sau** cổng
ấy đỏ theo kiểu này thì log nói ra nguyên nhân thay vì một mã ca trần.
