# ĐẶC TẢ ĐÓNG BĂNG — `LEASE-DANG-DUNG-MOT-LAN`, **bản sửa đổi 6** (delta)

> **CHỈ ghi phần thay đổi** so với r5 (`2c8fb5c6…`), trên nền r4/r3/r2. Bản 1–5 **KHÔNG bị sửa**.

`packet_id`: `LEASE-DANG-DUNG-MOT-LAN` · `packet_issue`: `#227`
`ke_thua`: r5 `2c8fb5c68e45dbdcd3e21c316169623d4dcab33459934b575ae8c626b08cb796`
→ r4 `abe7c292aba05aa772b77c246a570d72c9b8e97220247030ae15af8f750d0fce`
→ r3 `c65d5dbd9d2b398978226f6863cf7cd4e4ddb219a7086be0005e65804a0f47da`
→ r2 `3f310582de59dce7c109717dbab13ef9467b80c67ffeafc0ac8e1484309e0093`

## Vì sao có bản này — `T66` của r5 BẤT KHẢ THI, và đó là lỗi của đặc tả

`T66` đòi **mọi** guard cùng khẳng định *"lease đó không POST"*. Đo trên `b32b4241`, thứ tự thật
của thân bước `đăng`:

```
TRƯỚC POST : kiem-github · check · đọc packet_issue · body · dựng payload
LÀ POST     : ID=$(gh api "repos/$REPO/issues/$ISSUE/comments" …)
SAU POST    : case "$ID" · mark · echo "DA_DOI=1" >> $GITHUB_ENV
```

**Ba trong tám guard nằm SAU lời gọi POST** ⇒ với chúng, POST **đã xảy ra**. Vế ấy bất khả thi.

Executor **DỪNG đúng chốt**, từ chối hai đường lách, và từ chối đúng: (a) fake trả ID thành công
mà không ghi comment ⇒ vi phạm *"đồ giả phải mô phỏng TRẠNG THÁI"*; (b) đổi thứ tự / thêm
rollback ⇒ ngoài đơn hàng. Nó nói thẳng rằng tuyên `T66` đóng sẽ là **hình dạng A lần 7**, rồi
**hoàn nguyên sạch** (remote vẫn `b32b4241`, worktree 0 mục bẩn).

**Phần kiến trúc của r5 thì CHẠY**, đo trên bản thử nghiệm của executor: `M1` (thêm guard vào YAML
mà không đăng ký) ⇒ `65/66` ĐỎ `t64` — **phép thử quyết định ĐẠT**; `M2`, `M3` cùng chết; **cả sáu**
đột biến gỡ guard giết `t66`; hai tập guard bằng nhau, **8** mục; không mutant đa sát. **Ý tưởng
Q25 đúng. Thứ hỏng là VẾ KHẲNG ĐỊNH mà đặc tả áp ĐỒNG LOẠT.**

## Hình dạng **D** — lần thứ BA, trục MỚI

**D lần 3: *đặt cùng một câu kiểm chứng ở SAI PHA THỜI GIAN*** (tên do executor đặt). Bộ đếm **3**,
**cả ba đều do phiên điều phối**: lần 1–2 sai **độ phân giải** (khối vs nhánh), lần 3 sai **pha**.

r5 đăng ký *"D lần 3 ⇒ DỪNG"*. **Chốt ấy KÊU, và executor TÔN TRỌNG nó** — lần thứ hai liên tiếp
một chốt đăng ký trước chạy thật.

**Người giữ kho quyết (2026-08-21): cấp lượt 6.** **Override thứ BA** đối với một chốt đăng ký
trước — ghi nguyên trạng. Căn cứ: ba lần D đều là **đặc tả liệt kê từ bên ngoài**, và lượt 5 đã
chứng minh **đường thoát**: cái gì máy dẫn xuất được từ YAML thì đừng để người liệt kê. r5 mới áp
nguyên tắc ấy cho **danh sách guard**; r6 áp nốt cho **vế khẳng định**.

## Quyết định MỚI — Q28…Q31

| # | quyết định | căn cứ |
|---|---|---|
| **Q28** | **`T66` dạng "bốn vế đồng loạt" BỊ BÃI BỎ.** Thay bằng `T66′`: vế khẳng định **phụ thuộc VỊ TRÍ** của guard so với lời gọi POST. | Ba guard sau POST làm vế "không POST" bất khả thi. |
| **Q29** | **Vị trí (trước/sau POST) phải DẪN XUẤT TỪ YAML**, không phải hằng số trong tệp test. | Ghi cứng vị trí là dời chỗ ghi cứng, không phải bỏ nó — và hình dạng D sẽ tái phát ở đúng chỗ mới. |
| **Q30** | **Đặc tả THÔI liệt kê vế khẳng định.** Nó chỉ nêu **bất biến**: mỗi ca khẳng định thứ **QUAN SÁT ĐƯỢC** tại vị trí guard ấy, và **KHAI** thứ không quan sát được. Executor **dẫn xuất** tập vế từ vị trí. | Ba lần liên tiếp đặc tả liệt kê sai. Đây là cùng một nước đi đã cứu Q25, mở rộng một bậc. |
| **Q31** | Trần **620 → 660**; `attempts` **5 → 6**; `review_rounds` **5 → 6**. | Head `+541`. Bản thử nghiệm lượt 5 đạt 66 ca; `T67` thêm vào. |

## `nghiem_thu` — thay `T66`, thêm `T67`

Giữ `T43`–`T65`. Đột biến chạy trên **BẢN SAO TẠM**.

| # | tiêu chí | đột biến làm nó ĐỎ |
|---|---|---|
| **T66′** | Mỗi guard trong sổ có ca **THẬT**. Vế **CHUNG** cho mọi guard: lease khác **vẫn** được xử · `BI_CHAN` đúng · mã thoát bước đúng. Vế **PHỤ THUỘC VỊ TRÍ** — executor dẫn xuất, đặc tả **không** liệt kê. Gợi ý bất biến, **không phải mệnh lệnh**: guard **trước** POST thì *"lease đó chưa gửi lời gọi POST nào"* quan sát được; guard **sau** POST thì thứ quan sát được là **trạng thái ghi ngược** chứ không phải sự vắng mặt của POST. | Gỡ **từng** guard ⇒ ca **của guard đó** ĐỎ (tám đột biến riêng). Gỡ `mark`, `body`, `$GITHUB_ENV` hiện **SỐNG SÓT `63/63`** — cả ba phải chết. |
| **T67** | **Ca khoá cho Q29.** Vị trí guard phải **dẫn xuất từ YAML**: chuyển một guard **trước** POST thành **sau** POST **trong YAML** ⇒ tập vế khẳng định của guard ấy phải **đổi theo**. | **M4** — di chuyển một guard qua bên kia lời gọi POST trong YAML mà **giữ nguyên** tập vế ⇒ **PHẢI ĐỎ**. Không chết ⇒ vị trí đang bị ghi cứng ⇒ **DỪNG** (chốt dưới). |

Ngoài hai ca: suite `rc=0`, `N/N` bằng nhau, **≥ 67 ca**; đột biến giết nhiều ca phải **KHAI**.

## `ngoai_pham_vi` — thêm một mục QUAN TRỌNG

Giữ mọi mục r2–r5. **Thêm:**

**KHÔNG được đổi thứ tự lệnh trong thân bước `đăng`, không thêm rollback, không thêm preflight.**
Cửa sổ *"POST xong rồi `mark` hỏng"* là **thuộc tính của thiết kế hiện hành**, không phải khuyết
tật của phép đo. Vá nó là đổi sản phẩm giữa một packet đang đo sản phẩm ấy. **Khai vào
`chua_do_duoc`** (Q30), đừng vá.

## `hinh_dang_ke_thua`

**A** = 6 · **B** = 2 · **C** = 1 · **D** = **3**.

**Chốt cho lượt 6:** **A** lần 7 · **B** lần 3 · **C** lần 2 · **D** lần **4** ⇒ **DỪNG**.

**Và hai chốt riêng của lượt này:**
- **`M4` không giết được `T67`** ⇒ **DỪNG**. Khi ấy vị trí guard đang bị ghi cứng, tức đã dời chỗ
  ghi cứng chứ không bỏ nó — **D lần 4 dưới lớp áo mới**.
- Thấy một vế khẳng định **bất khả thi** ở guard nào ⇒ **KHAI ra và DỪNG ca đó**, đừng lách bằng
  đồ giả sai trạng thái. Đây chính xác là điều executor đã làm đúng ở lượt 5.

## `chua_do_duoc` — thêm

Giữ mọi mục r2–r5, thêm:

1. **Cửa sổ *"POST thành công, `mark` hỏng"* KHÔNG ĐÓNG.** Comment đã đăng mà `posted_comment_id`
   chưa ghi. Thứ **duy nhất** che nó là `kiem-github` trả `rc=9` ở lượt chạy sau (lớp hỏi comment
   trên issue). **Che, không đóng** — và nếu lượt sau chạy trên một nhánh khác trước khi lượt này
   ghi ngược, khe race hai nhánh `ops/**` vẫn mở như cũ. Nói đúng chữ.
2. **Vẫn chưa có lượt GitHub Actions THẬT nào**, chưa có Windows — sau **năm** lượt vá. Đây là
   khoảng trống **lớn nhất còn lại**, và nó **không đóng được từ trong container**.
