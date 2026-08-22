# ĐẶC TẢ ĐÓNG BĂNG — `LEASE-DANG-DUNG-MOT-LAN`, **bản sửa đổi 5** (delta)

> **CHỈ ghi phần thay đổi** so với r4 (`abe7c292…`), trên nền r3/r2.
> Bản 1–4 **KHÔNG bị sửa, KHÔNG bị xoá**.

`packet_id`: `LEASE-DANG-DUNG-MOT-LAN` · `packet_issue`: `#227`
`ke_thua`: r4 `abe7c292aba05aa772b77c246a570d72c9b8e97220247030ae15af8f750d0fce`
→ r3 `c65d5dbd9d2b398978226f6863cf7cd4e4ddb219a7086be0005e65804a0f47da`
→ r2 `3f310582de59dce7c109717dbab13ef9467b80c67ffeafc0ac8e1484309e0093`
→ r1 `e1026adb569f5b4732197afac9c0f35cdd5a8945d46301b1d4cb062624e7c72c`

## Vì sao có bản này

Lượt 4 giao **đủ** `T62`/`T63`/`Q23` — đo lại độc lập trên `b32b4241`: suite `63/63` ở **cả hai**
môi trường, `actionlint` `rc=0`, `numstat` 3 tệp `+541/−19`, **D24** ⇒ `62/63` ĐỎ `t62`, **D23** ⇒
`62/63` ĐỎ `t63` (cả hai **sống sót `61/61`** ở head trước).

Rồi **bảng `Q24` do chính r4 bắt làm đã trả tiền**: executor **TỰ DỪNG** ở chốt `C lần 2` mà r4
đăng ký trước, thay vì vá tiếp. **Chốt đăng ký trước đã CHẠY THẬT** — không phải chữ trong tài
liệu. Ghi ra vì kho này có nguyên một bài học về chuyện ngược lại (*"nghĩ ra được phép thử mà
không chạy nó thì phép thử ấy không tồn tại"*).

Nhưng bảng ấy lộ ra thứ lớn hơn một nhánh: **một LỚP guard thiếu phản chứng.** Các guard `set +e`
thêm ở lượt 2 theo `Q11` phần lớn không có ca riêng. Đo trên `b32b4241`:

```
gỡ guard `mark rc≠0`          ->  63/63 SỐNG SÓT, actionlint rc=0
gỡ guard `body rc≠0`          ->  63/63 SỐNG SÓT
gỡ guard ghi `$GITHUB_ENV`    ->  63/63 SỐNG SÓT
đọc `packet_issue` · dựng payload · `case ID` phi-số   ->  KHÔNG fixture nào chạm tới
```

## HÌNH DẠNG **D** — lần thứ HAI, và người gây ra là phiên điều phối

**D = *đặt câu hỏi kiểm chứng ở SAI ĐỘ PHÂN GIẢI*.** Bộ đếm nay **2**:

| lần | ở đâu | tác giả |
|---|---|---|
| 1 | `r3` hỏi *"phép đo nào ĐỎ nếu gỡ nó?"* ở mức **KHỐI** (`kiem-github`) ⇒ nửa `rc=9` **của cùng khối** lọt | `claude` (phiên điều phối) |
| **2** | `r2`/**Q11** đặt hàng *"bọc `set +e` quanh MỌI lệnh"* ở mức **KHỐI** mà **không** đặt hàng phản chứng cho **từng guard** ⇒ sáu nhánh lọt | `claude` (phiên điều phối) |

**r4 đăng ký: *"D lần 2 ⇒ DỪNG, không vá"*. Chốt ấy KÊU.** Cùng lúc executor tuyên `C lần 2`.
**Hai chốt DỪNG cùng kêu.**

**Người giữ kho quyết (2026-08-21): cấp lượt 5, nhưng ĐỔI CÁCH.** Đây là **override thứ hai** đối
với một chốt đăng ký trước — ghi nguyên trạng, không làm tròn. Căn cứ: bốn lượt qua, thứ hỏng
**không phải bản vá** mà là **cách đặc tả hỏi câu kiểm chứng**. Vá bằng cách **liệt kê nhánh** đã
thất bại **hai lần liên tiếp** — đúng ngưỡng *"cùng một hình dạng ≥ 2–3 lần ⇒ hỏi CÓ NÊN LÀM
KHÔNG, đừng hỏi VÁ THẾ NÀO"*. Nên lượt 5 **không liệt kê nhánh nữa**.

## Quyết định MỚI — Q25…Q27

| # | quyết định | căn cứ |
|---|---|---|
| **Q25** | **Phép đo phải DẪN XUẤT danh sách guard TỪ CHÍNH TỆP YAML, không nhận nó từ đặc tả.** Một ca **meta** trích thân bước `đăng`, tìm **mọi** lệnh được bọc `set +e … rc=$? … set -e`, rồi đối chiếu với một **sổ đăng ký** trong tệp test. Lệch ⇒ **ĐỎ**. | Hình dạng D chết theo **KIẾN TRÚC**, không theo bản vá — đúng tiền lệ Q9 (giết P1-1) và `shell_environment_policy` (bốn lượt vá rồi bỏ cả lớp). Tôi liệt kê thiếu hai lần; máy đọc YAML thì không quên. |
| **Q26** | Mỗi guard trong sổ đăng ký phải trỏ tới một ca **THẬT** làm lệnh ấy hỏng và khẳng định hành vi (lease đó không POST · các lease khác vẫn xử · `BI_CHAN` đúng · mã thoát bước đúng). | Sổ đăng ký trỏ vào hư không thì nó chỉ là một danh sách. |
| **Q27** | Trần **570 → 620**; `attempts` **4 → 5**; `review_rounds` **4 → 5**. | Head `+541`. Ca meta + sáu ca guard. |

## `nghiem_thu` — ca MỚI

Giữ `T43`–`T63`. Đột biến chạy trên **BẢN SAO TẠM**.

| # | tiêu chí | đột biến làm nó ĐỎ |
|---|---|---|
| **T64** | **Ca META.** Tập guard **dẫn xuất từ YAML** phải **BẰNG** tập trong sổ đăng ký. | **M1** — thêm một lệnh được bọc `set +e` vào YAML mà **không** đăng ký ⇒ ĐỎ. **M2** — xoá một mục khỏi sổ đăng ký ⇒ ĐỎ. **Hai hướng ngược nhau, hai đột biến riêng.** |
| **T65** | **T64 fail-close.** Bộ trích trả **rỗng** hoặc **không phân tích được** ⇒ **ĐỎ**, không phải "không có guard nào". | **M3** — làm bộ trích trả `[]` (vd đổi mẫu khớp thành thứ không khớp gì) ⇒ ĐỎ. Ba trạng thái: `N>0` · `không phân tích được` · `N=0` — **hai trạng thái sau đều ĐỎ**. |
| **T66** | Mỗi guard trong sổ có ca làm nó hỏng, khẳng định **bốn** vế: lease đó **không** POST · lease khác **vẫn** được xử · `BI_CHAN` đặt đúng · mã thoát bước đúng. Bao đủ **sáu** nhánh còn hở: `packet_issue` · `body` · payload · `case ID` phi-số · `mark` · ghi `$GITHUB_ENV`. | Gỡ **từng** guard một ⇒ ca **của guard đó** ĐỎ. Sáu đột biến riêng; **gỡ guard `mark`, `body`, `$GITHUB_ENV` hiện SỐNG SÓT `63/63`** — cả ba phải chết. |

Ngoài ba ca: suite `rc=0`, `N/N` bằng nhau, **≥ 66 ca**; đột biến giết nhiều ca phải **KHAI**.

**Đòi hỏi về BỘ TRÍCH (Q25) — đọc kỹ, đây là chỗ ca meta dễ thành đồ trang trí:**
nó phải đọc **thân bước `đăng` trích từ chính tệp YAML** (tiền lệ `t32`/`t51`/`t59`), **không**
đọc một bản chép. `M1` là phép thử quyết định: thêm guard vào **YAML** mà suite vẫn xanh thì bộ
trích đang đọc nhầm chỗ.

## `ngoai_pham_vi` — không đổi

`ops/specs/**` ngoài `write_set` · khe race hai nhánh `ops/**` · nợ nền `chay(env=None)`
(delta = 0) · các finding đã đóng.

**Thêm:** **đừng vá `_doc_gh` / `_kiem_loai_so_hieu` / `_kiem_comment_da_co`** cho những nhánh mà
bảng `Q24` xếp *"một phần"*. Chúng là **hàm Python**, không phải guard shell, nên nằm ngoài đơn
hàng `T64`–`T66`. Thấy nhánh nào đáng lo thì **KHAI vào `chua_do_duoc`**, đừng tự mở phạm vi —
đây đúng chỗ hai lượt trước đã trượt.

## `hinh_dang_ke_thua`

**A** = 6 · **B** = 2 · **C** = 1 (Q20 giữ) · **D** = **2** (ghi ở trên).

**Chốt cho lượt 5 — CHẶT HƠN, vì đã override hai lần:**
**A** lần 7 · **B** lần 3 · **C** lần 2 · **D** lần **3** ⇒ **DỪNG, không vá**, xuất handoff.

**Và một chốt loại khác, đăng ký lần đầu:** nếu ca meta `T64` **tự nó** hoá ra đo sai chỗ (M1
không giết được nó), thì **DỪNG** — vì khi ấy chính bản vá kiến trúc cho D lại mắc D, và câu hỏi
đúng không còn là *"vá thế nào"*.

## `chua_do_duoc` — thêm

Giữ mọi mục r2/r3/r4, thêm:

1. **Bảng `Q24` xếp *"một phần"* cho vài nhánh trong `_doc_gh` · `_kiem_loai_so_hieu` ·
   `_kiem_comment_da_co`** (lỗi gọi vs JSON hỏng · phản hồi thiếu trường · `--slurp` trả dạng lẫn
   kiểu · comment thiếu `body`). **CỐ Ý để ngoài phạm vi** lượt 5 — chúng là hàm Python, không
   phải guard shell. Nói ra để `cross_approved` không bị đọc rộng hơn thực tế.
2. **`t59` chỉ so `argv[0:2]`** — cờ phía sau vô hình với nó (r4 đã khai; nhắc lại vì `T64` không
   đụng tới).
3. **Vẫn chưa có lượt GitHub Actions THẬT nào**, chưa có Windows. Bốn lượt vá, mọi phép đo
   workflow đều là thân bước chạy dưới `bash` tại chỗ. Đây là khoảng trống **lớn nhất còn lại**
   của packet, và nó **không** đóng được từ trong container.
