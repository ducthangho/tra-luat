# ĐẶC TẢ ĐÓNG BĂNG — `LEASE-DANG-DUNG-MOT-LAN`, **bản sửa đổi 7** (delta)

> **CHỈ ghi phần thay đổi** so với r6 (`4ee67d54…`), trên nền r5–r2. Bản 1–6 **KHÔNG bị sửa**.

`packet_id`: `LEASE-DANG-DUNG-MOT-LAN` · `packet_issue`: `#227`
`ke_thua`: r6 `4ee67d54b5504c0b303dad3bf8470c912ad754e6bcda42e8cb4a2866475ba181`
→ r5 `2c8fb5c68e45dbdcd3e21c316169623d4dcab33459934b575ae8c626b08cb796`
→ r4 `abe7c292aba05aa772b77c246a570d72c9b8e97220247030ae15af8f750d0fce`
→ r3 `c65d5dbd9d2b398978226f6863cf7cd4e4ddb219a7086be0005e65804a0f47da`
→ r2 `3f310582de59dce7c109717dbab13ef9467b80c67ffeafc0ac8e1484309e0093`

## Phần CỐT LÕI của r6 — ĐẠT

Review lượt 4 (verdict `0655b9d0caea1d49450b4b8013f79cd49af61adc62b261bdce2085b76b17614f`) đo
**tám** hướng tấn công vào chính phép dẫn xuất vị trí: `M4` và chiều **ngược**, đổi tên biến `ID`,
thêm khoảng trắng, tách dòng bằng dấu chéo ngược, thêm lời gọi POST thứ hai, chú thích chứa
nguyên văn dòng POST — **bảy ĐỎ**, cái thứ tám (chú thích chỉ chứa `gh api`) **xanh ĐÚNG**.
Trạng thái *"không phân tích được"* có bằng chứng dương. Bốn đột biến *"guard còn nhưng hành vi
sai"* cũng chết, **không ca nào trống ruột**.

**Bằng chứng mạnh nhất:** `t66` **không** chết dưới `M4` — vì kỳ vọng của nó **trôi theo YAML** —
chỉ `t67` (sổ đăng ký lệch) chết. Nước đi *"đặc tả thôi liệt kê, executor dẫn xuất"* là **thật**.

## Hai lỗ còn lại — CÙNG MỘT GỐC

**Cả hai P2 đều là: khoá theo THỨ TA LIỆT KÊ ĐƯỢC, thay vì theo THỨ THẬT SỰ CHẶN.**

**P2-1** — gỡ đúng **nhánh chặn** của khối POST (giữ nguyên `set +e`/`rc=$?`/`set -e`) ⇒ suite
**`67/67` XANH TRỌN VẸN**, `actionlint` `rc=0`. Không phải equivalent mutant: đồ giả `gh` trả
`rc=1` **nhưng in một id SỐ hợp lệ**, và khi gỡ guard thì lease `giua` **được `mark` bằng id đến
từ một lời gọi hỏng**. Sổ khoá theo **KHỐI** `set +e`, còn thứ được khẳng định là **NHÁNH chặn**;
mục #6 khoá khối POST nhưng **đặt tên `case_id`**, và ca của nó bơm lỗi vào câu `case "$ID"` —
một nhánh **ngoài mọi khối**. Cái tên đã che chỗ hở. `T66′` đạt **7/8**.

**P2-2** — `_guard_dan_xuat` neo vào **đúng một** mẫu. Thêm một guard chặn **thật** (gọi
`bao_chan` + `continue`) kiểu **`if ! cmd`** ⇒ **`67/67` LỌT**; kiểu **`cmd || rc=$?`** ⇒
**`67/67` LỌT**; kiểu chính tắc ⇒ `66/67` ĐỎ `t64`. Đúng hình dạng **"danh sách CẤM không bao giờ
đủ — phải đảo thành danh sách CHO PHÉP"** của `CLAUDE.md`.

Đo nền: **9** lời gọi `bao_chan` vs **8** khối `set +e` — chênh đúng **1**, chính là nhánh
`case "$ID"` của P2-1. **Hai lỗ, một con số.**

## Bộ đếm D — người giữ kho quyết KHÔNG tăng

Reviewer tách câu hỏi làm hai trục và **từ chối tự quyết**: trục **vế** không phải D (`t66` tính
hai boolean độc lập nên tập vế thực tế phân **ba** lớp); trục **đơn vị guard** thì đúng hình dạng
D lần 1–2. Họ nêu thẳng rằng đọc theo **hình dạng** thì đây là **D = 4** và chốt `r6` biến verdict
thành `dung_lai`.

**Quyết định (2026-08-22): KHÔNG tăng. Bộ đếm D giữ 3.** Căn cứ: lựa chọn *"guard = khối `set +e`"*
là của **`r5`/Q25**, đã qua **hai** lượt review mà không ai bắt; nó không phải nước đi mới của
lượt 6. Cái mới chỉ là **một nhánh sót chưa khai**. Ghi nguyên trạng cả hai cách đọc.

## Quyết định MỚI — Q32…Q35

| # | quyết định | căn cứ |
|---|---|---|
| **Q32** | **ĐẢO danh sách CẤM thành danh sách CHO PHÉP.** Đơn vị khoá không còn là *"khối `set +e`"* mà là **NHÁNH CHẶN**, và nhánh chặn có **một** dấu hiệu bắt buộc: nó gọi `bao_chan` (thứ **duy nhất** đặt `BI_CHAN`). Phép đo đếm `bao_chan` và đòi **mọi** lời gọi phải nằm trong tập đã đăng ký. | P2-2. Đây là bài học đã ghi trong `CLAUDE.md` và đã trả giá ở `lease_publish.py` (`granted_by`): *"danh sách CẤM phải đoán trước mọi cách viết của kẻ gian nên thua từ trong thiết kế; danh sách CHO PHÉP chỉ phải liệt kê một tập nhỏ và biết trước."* Reviewer đã **nguyên mẫu và đo**: `if ! cmd` · `cmd \|\| rc=$?` · `set +e` một dòng — **cả ba chuyển sang ĐỎ**. |
| **Q33** | **Đăng ký nhánh `case "$ID"` TƯỜNG MINH**, và đặt lại tên mục #6 cho khớp thứ nó khoá. Sau Q33 **không còn dấu `+1`**: số `bao_chan` phải **BẰNG** số mục trong sổ. | P2-1. Một hằng số `+1` không giải thích được là chỗ lỗ sau sẽ nấp. |
| **Q34** | `_ve_dan_xuat` phải có **phản chứng fail-close riêng**, không sống nhờ `except Exception` của `main()`. | P3. Ai bọc `try` hoặc cho `next(…, mặc_định)` là chốt câm mà không ca nào kêu. |
| **Q35** | Vá hạt sạn `ghe.exists()` → kiểm **tệp**, kẻo `IsADirectoryError` biến một lỗi sản phẩm tương lai thành cú crash khó đọc. | P3. |

**Ngân sách GIỮ NGUYÊN 660** — reviewer đo ba bản vá ≈ **15 dòng**, lọt trần còn **27**
(`+633/660`). **Lần đầu trong packet này không phải nới trần.**

## `nghiem_thu`

Giữ `T43`–`T67`. Đột biến chạy trên **BẢN SAO TẠM**.

| # | tiêu chí | đột biến làm nó ĐỎ |
|---|---|---|
| **T64′** | Tập **nhánh chặn** dẫn xuất từ YAML (đếm theo `bao_chan`) phải **BẰNG** sổ đăng ký — **không dấu `+1`**. | **D2** `set +e` một dòng · **D3** `if ! cmd` · **D4** `cmd \|\| rc=$?` — cả ba hiện **SỐNG SÓT `67/67`**, cả ba phải chết. Cộng `M1`/`M2` cũ vẫn phải chết. |
| **T68** | Gỡ **nhánh chặn của khối POST** ⇒ ĐỎ. Đồ giả trả `rc=1` **kèm id SỐ hợp lệ**; ca khẳng định `rc` bước `=1` · `giua` POST **đúng một lần** · `marks["giua"]` là **False**. | **A5** — gỡ nhánh ấy; hiện **SỐNG SÓT `67/67`**. |
| **T65′** | `_ve_dan_xuat` fail-close **có ca riêng**: thân đã đổi cách viết dòng POST ⇒ nó phải **NÉM**, không trả mặc định. | Bọc `try` quanh `_ve_dan_xuat`, hoặc `next(…, mặc_định)` ⇒ phải ĐỎ. |

Suite `rc=0`, `N/N` bằng nhau, **≥ 68 ca**; đột biến giết nhiều ca phải **KHAI**.

## `ngoai_pham_vi` — giữ nguyên r2–r6

Nhấn lại mục cấm mới nhất: **không đổi thứ tự lệnh trong thân bước `đăng`, không rollback, không
preflight.** Cửa sổ *"POST xong, `mark` hỏng"* là thuộc tính thiết kế — **khai**, đừng vá.

## `hinh_dang_ke_thua`

**A** = 6 · **B** = 2 · **C** = 1 · **D** = **3** (Q32 §trên).

**Hình dạng E — *khoá theo THỨ LIỆT KÊ ĐƯỢC thay vì theo THỨ THẬT SỰ CHẶN*** — bộ đếm **1**
(hai biểu hiện cùng lượt: P2-1 và P2-2, cùng một gốc). Đây là **họ hàng gần** của
*"danh sách CẤM không bao giờ đủ"* đã có trong `CLAUDE.md`, và của D — nhưng khác trục: D là
**độ mịn/pha** của câu hỏi, E là **tiêu chí nhận dạng** đối tượng được hỏi.

**Chốt cho lượt 7:** **A** lần 7 · **B** lần 3 · **C** lần 2 · **D** lần 4 · **E** lần **2** ⇒
**DỪNG, không vá**, xuất handoff.

**E lần 2** = sau khi đảo sang `bao_chan`, lại tìm được một nhánh chặn **không** gọi `bao_chan`.
Nếu vậy thì dấu hiệu nhận dạng vẫn sai, và câu hỏi đúng không còn là *"vá thế nào"*.

## `chua_do_duoc` — thêm

Giữ mọi mục r2–r6, thêm:

1. **Reviewer KHÔNG rà nội dung `ops/lease_publish.py` (+105/−7) và phần YAML (+70/−8)** của các
   lượt trước — chỉ **đột biến** chúng. Ba lượt review đều là review **delta**. Nói ra để
   `cross_approved` không bị đọc thành *"đã rà toàn bộ diff"*.
2. **Mọi lượt đều đi qua đồ giả; chưa đo `gh` thật lần nào.**
3. **Vẫn chưa có lượt GitHub Actions THẬT, chưa có Windows** — sau **bảy** lượt. Không đóng được
   từ trong container.
