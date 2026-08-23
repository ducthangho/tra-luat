# ĐẶC TẢ ĐÓNG BĂNG — `LEASE-DANG-WINDOWS`, **bản sửa đổi 3** (delta)

> **CHỈ ghi phần thay đổi** so với r2 (`d9da7705617c95c8dc394d773de8456712d3cc2a2975e5903e8cb28c934c0d83`).
> r1 (`f555cbe1a368c12040726dd706ce25ed8dd4041bd8a2f840590810a3c3908a26`) và r2
> **KHÔNG bị sửa, KHÔNG bị xoá**.

`packet_id`: `LEASE-DANG-WINDOWS` · `packet_issue`: `#238`

## Vì sao có bản này

Cross-review lượt 1 (`38b4986dac49c0207cd6c6ccf68e169491065552288169a790c0e7ba49589523`, đo trên
`edc1906cf01fcceb15c646e1fdc4fcd8957644ed`) kết luận `can_sua`. `W3′`/`W4`/`W5` **đạt, có bằng
chứng sơ cấp**. `W6`/`W7`/`W8` — ba tiêu chí r2 sinh ra — **không có răng**: cả ba đo **HÀM TRỢ
GIÚP**, không đo **DÂY NỐI**. Hệ quả đo được, hai chiều:

```
P1-1  raise BoQuaNen("hom nay troi mua — khong lien quan runs-on")
      -> 72/72 đạt; đã chạy=72, bỏ qua=1 ; rc=0        <- cửa sau, W7 KHÔNG ĐẠT
P1-2  job = job or {"runs-on": "ubuntu-latest"}        # hằng số trá hình
      -> 72/72 đạt; đã chạy=72, bỏ qua=0 ; rc=0        <- W6 KHÔNG ĐẠT
      (kèm YAML đổi sang matrix[ubuntu,windows]: vẫn rc=0 — đúng phép thử W6 tự khai làm chuẩn)
```

Nghĩa là `Q3′` — **quyết định trung tâm của r2** — hiện **không có cổng nào giữ**: đúng khoảnh
khắc ai đó "dọn gọn" hàm dẫn xuất thành hằng số, không phép đo nào kêu.

Người giữ kho quyết in-session 22-08-2026: **nới trần, vá hai P1**.

## Quyết định MỚI

| # | quyết định | căn cứ |
|---|---|---|
| **Q8** | **BẰNG CHỨNG PHẢI ĐẶT Ở DÂY NỐI.** Một tiêu chí `Wn` chỉ được khai **ĐẠT** khi đột biến làm nó đỏ vẫn còn ít nhất một ca đỏ **SAU KHI gỡ bỏ mọi ca gọi thẳng hàm trợ giúp của tiêu chí ấy**. Chưa thoả ⇒ khai **KHÔNG ĐẠT**, không làm tròn lên. | Đây là chốt **dẫn xuất được**, không phải lời hứa: phép "gỡ ca gọi thẳng rồi chạy lại" là một lệnh chạy được, cho ra số. Nó giết **cả lớp** hình dạng **E** thay vì vá từng biểu hiện — bốn biểu hiện trong một diff 90 dòng là bằng chứng rằng vá lẻ không đủ. |
| **Q9** | **Lý do bỏ qua phải được `main()` ĐO LẠI, không được nhận lời khai của ca.** `BoQuaNen` mang theo mỏ neo `(tệp workflow, tên job)`; `main()` tự gọi phép dẫn xuất trên mỏ neo ấy. Dẫn xuất trả rỗng ⇒ ca xếp vào **hỏng**, KHÔNG phải bỏ qua. | Đóng P1-1 tại gốc: cửa sau tồn tại vì `main()` tin chuỗi lý do do ca tự khai. Ca không còn khai được lý do thì không còn cửa sau nào để khoá bằng danh sách. |
| **Q10** | **Phép dẫn xuất phải chịu được HẰNG SỐ TRÁ HÌNH: ca đo phải TỰ SINH chuỗi `runs-on` lúc chạy** rồi đòi **chính chuỗi ấy** xuất hiện trong lý do, kèm đối chứng một nhãn không ubuntu-only phải trả rỗng. | Đóng P1-2 tại gốc. Hằng số ghi trong mã **không thể** đoán trước chuỗi mà ca vừa sinh ⇒ mọi bản "dọn gọn" thành hằng số đều đỏ, không cần liệt kê trước các dạng hằng số. |
| **Q11** | Ngân sách nới **90 → 120 dòng thêm** so với `ba82b06f`. Phạm vi lượt này **CHỈ** hai P1. **KHÔNG** có P2 nào trong phạm vi. | Con số của reviewer: P1-1 ≈ 19, P1-2 ≈ 10 ⇒ ~29. Trần 120 để lại đúng 1 dòng dư — cố ý chật, để không ai lấy chỗ thừa làm cớ nới phạm vi. Bốn P2 và ba P3 thành packet kế tiếp có tên. |

## `nghiem_thu` — thay `W6`/`W7`, thêm `W9`

Giữ `W1`, `W2`, `W4`, `W5` (r1) và `W3′` (r2). **`W8` giữ nguyên văn nhưng nay chịu Q8** — nếu ca
duy nhất giữ nó là ca tự dựng chuỗi rồi khẳng định về chuỗi mình vừa dựng thì `W8` khai **KHÔNG
ĐẠT** (reviewer đã đo: bỏ vòng in ⇒ 8 ca biến mất im lặng, rc=0).

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| **W6′** | Phép dẫn xuất đọc **TỆP THẬT**, và không hằng số nào giả được nó. | Ca tự sinh YAML tạm với `runs-on` là một chuỗi **do chính ca dựng lúc chạy** (không xuất hiện ở bất cứ đâu trong mã sản phẩm) ⇒ lý do phải chứa **đúng chuỗi ấy**. Thay lời đọc YAML bằng bất kỳ hằng số nào ⇒ **ĐỎ**. Đối chứng: nhãn không ubuntu-only ⇒ lý do **rỗng**. |
| **W7′** | Không ca nào bỏ qua được vì lý do **không dẫn xuất được từ `runs-on`**. | Bơm một `BoQuaNen` với mỏ neo trỏ tới một job **không** ubuntu-only (hoặc không có mỏ neo) ⇒ ca ấy phải bị xếp **hỏng** và suite **ĐỎ**. Đây là ca meta bắt buộc; thiếu nó thì `W7′` KHÔNG ĐẠT. |
| **W9** | **Chốt Q8, đo được:** với mỗi tiêu chí trong `{W6′, W7′, W8}`, gỡ bỏ khỏi suite mọi ca **gọi thẳng** hàm trợ giúp của tiêu chí ấy rồi chạy lại **dưới đúng đột biến của tiêu chí** ⇒ vẫn phải còn **≥ 1 ca đỏ**. | Chạy đúng phép trên. Báo cáo phải là bảng: `tiêu chí · đột biến · ca đã gỡ · ca còn đỏ · N/N`. Không còn ca đỏ nào ⇒ tiêu chí ấy **KHÔNG ĐẠT** — khai thẳng, đừng đổi phép đo cho vừa. |

## Điều kiện DỪNG (bổ sung, giữ nguyên các điều kiện đã đăng ký)

- **Nếu đóng trọn hai P1 ở mức DÂY NỐI không lọt 120 dòng thêm:** **DỪNG**, báo **số dòng đo được**
  cần thiết và chỗ vượt. **KHÔNG** thu nhỏ phép đo cho vừa ngân sách — đó chính là cách `W6`/`W7`
  ra đời ở lượt trước.
- **Nếu `W9` không đỏ được cho một tiêu chí:** khai `KHÔNG ĐẠT` cho tiêu chí ấy và **DỪNG** ở đó;
  không thay bằng một phép đo dễ hơn.

## `hinh_dang_ke_thua`

**E** (*khoá phần LIỆT KÊ ĐƯỢC thay vì phần THẬT SỰ CHẶN*) tăng **2 → 3**, do reviewer lượt 1 tuyên
với bốn biểu hiện độc lập trong một diff 90 dòng (P1-1, P1-2, P2-1, P2-4). Bộ đếm khác giữ nguyên:
**A** = 7 · **B** = 2 · **C** = 1 · **D** = 3 · **F** = 2.

Ghi thêm cho hồ sơ: **cả bốn biểu hiện đều do ĐẶC TẢ r2 gây ra**, không do bản vá — `W6`/`W7`/`W8`
được viết bằng cách mô tả *thứ cần đúng*, mà không viết *đột biến nào phải làm nó đỏ ở đâu*. Q8 là
lần đầu đặc tả này khai vị trí của bằng chứng, chứ không chỉ khai nội dung của nó.

## `chua_do_duoc`

Giữ r2. Thêm: **P2-2 (dẫn xuất MỘT CHIỀU — workflow windows-only vẫn chạy trên Linux)** là lỗi
**đúng thật, đã đo**, và **CỐ Ý để ngoài phạm vi** lượt này vì ngân sách. Nó phải vào packet kế
tiếp có tên. Nói thẳng ở đây thay vì để nó nằm trong prompt: **chỗ đó là nơi các ca đi chết.**
