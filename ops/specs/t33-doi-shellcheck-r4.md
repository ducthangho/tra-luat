---
kieu: dac_ta_delta
packet: T33-DOI-SHELLCHECK
ban: r4
trang_thai: dang_hieu_luc
thay_the:
  - tep: ops/specs/t33-doi-shellcheck-r2.md
    dong: 232
    sha256_tep_bi_thay: b9620d17b86f503b12d93359fb6d3423d29c034c29ab372f40cc5d7089b40e71
  - tep: ops/specs/t33-doi-shellcheck-r3.md
    dong: 192
    sha256_tep_bi_thay: 78c3ecb40eb8dd7dcf628ef7ea9a372aae5cfbf7a4fcfd25bb4ec7f32fe6ea0d
pham_vi_thay_the: chon_loc      # CHỈ hai dòng trên; mọi phần khác của r2/r3 GIỮ NGUYÊN hiệu lực
ho_so_lap_luan: https://github.com/ducthangho/tra-luat/issues/297
ghi_chu_hinh_dang: >-
  CẤU TRÚC NÀY LÀ TẠM. Chưa cổng nào đọc nó. Packet "cơ chế trạng thái đặc tả" (hướng (2)
  của #297) ĐƯỢC PHÉP đổi hoàn toàn hình dạng. Đây là DỮ LIỆU để packet ấy kế thừa, KHÔNG
  phải giao diện để nó tuân theo.
---

# `t33-doi-shellcheck` — bản delta `r4`

**DELTA, không phải bản viết lại.** Thay **đúng hai dòng**; mọi phần khác của `r2`/`r3` **giữ
nguyên hiệu lực**, và **hai tệp ấy không đổi một byte nào** — ai đang neo băm `r2`/`r3` vẫn neo đúng.

> **Tệp này CHỈ ghi ĐIỀU GÌ đổi. Nó KHÔNG lập luận.**
> Lý lẽ, phép đo, bảng chân trị, thước phân xử và toàn bộ lịch sử quyết định nằm ở **#297**
> (`ho_so_lap_luan` trong khối đầu tệp). Đó là chỗ chúng chịu được tranh luận và sửa lại;
> một đặc tả **đóng băng** thì không. Xem §4 để biết vì sao ranh giới ấy được đặt ở đây.

---

## 1. Hai chỗ được hạ

`r2:232` và `r3:192` là **cùng một câu**, chỉ khác con số ở dòng ngay trên (`88/88` ở `r2`,
`97/97` ở `r3`).

**Đang có trên master:**

```text
    định ấy tra theo NỀN: thay mệnh đề nền bằng phân biệt theo TÊN TỆP vẫn cho 88/88,
    rc=0 trên toàn chân Ubuntu (đo 23-08-2026). Ca này khoá đúng cái trục ấy.
```

**Thay bằng:**

```text
    định ấy tra theo NỀN: thay mệnh đề nền bằng phân biệt theo TÊN TỆP vẫn cho 88/88,
    rc=0 khi chạy cục bộ trên Linux (đo 23-08-2026). Ca này khoá đúng cái trục ấy.
```

(ở `r3`: `88/88` → `97/97`, phần còn lại y hệt.)

**Câu thay thế KHÔNG phải lời khai mới của `r4`.** Nó là bản vá **đã qua review và đã land** ở
`3239279b`, hôm nay vẫn đứng nguyên trong mã — `ops/lease_publish_test.py:3134`. `r4` **chép**
nó, đúng luật `#238/r4/Q13` (*"chép bản vá đã chạy, KHÔNG tự nghĩ lại"*).

**Sai ở đâu:** `"toàn chân Ubuntu"` chỉ một **job/leg của CI**; bằng chứng trong hồ sơ là một lượt
chạy **cục bộ**. Chi tiết ở #297.

---

## 2. `r2:215` — NGOÀI phạm vi

Câu ở `r2:215` (`toàn bộ chân Ubuntu im lặng`) **không** thuộc phạm vi `r4` và **không** được sửa.

Quyết định của chủ kho, in-session `2026-08-26`: **`r2:215` không phải hình dạng `A`.** Nó là suy
luận từ tiền đề nêu tại chỗ, không phải lời khai kết quả một lượt chạy.

**Đây là kết luận của một LẬP LUẬN, không phải của một phép đo** — không cổng nào phân xử được nó.
Lập luận đầy đủ, ba lượt cross-review đã bác và đã sửa nó, nằm ở **#297**. Ai muốn xét lại thì xét
ở đó, không phải ở đây.

Ghi nhận một điều đo được: `r2:215` dùng **cùng cách lượng hoá** với câu sai ở gần đó nhưng
**không cùng byte** — `:215` viết `toàn bộ chân Ubuntu`, `:232` viết `toàn chân Ubuntu`.

---

## 3. `r4` KHÔNG làm gì

- **Không** dựng cơ chế trạng thái máy đọc được (hướng (2) của #297) — packet riêng, chưa có đặc tả.
- **Không** sửa `r2:215`. **Không** đụng `r1`. **Không** đo lại toàn bộ số của `r2`/`r3`.

---

## 4. Vì sao tệp này không lập luận — và nó phải tự khai điều này

Ba lượt cross-review trên chính `r4` ra **sáu** finding, **tất cả là của người viết**, và **tất cả
cùng MỘT hình dạng**: một câu nói rộng hơn thứ phép đo thật sự chứng minh.

| lượt | câu bị bác |
|---|---|
| 1 | *"`r4` chưa từng tồn tại"* — phép quét chỉ hỏi **tip**, không hỏi lịch sử |
| 1 | thước *"bằng chứng hay giải thích"* — không tách được hai câu |
| 2 | *"bị rút không vì nội dung"* — hồ sơ ghi **hai** lý do |
| 2 | *"gỡ mệnh đề nền là no-op"* — mệnh đề đúng ở **ngữ cảnh khác** |
| 3 | *"chưa bao giờ lên master"* — lẫn **tệp trong cây** với **commit trong lịch sử** |
| 3 | một truth table cho **một tuple** → kết luận cho **cả một leg** |

`CLAUDE.md`: *"cùng một hình dạng lỗi lặp ba lần trở lên thì câu hỏi đúng là **có nên làm việc này
không**, không phải **vá thế nào**."*

Việc không nên làm là: **để một đặc tả ĐÓNG BĂNG mang lập luận.** Mỗi câu lý lẽ là một bề mặt mới
để khai rộng hơn đo, và một tệp đóng băng thì **không sửa được** — nó chỉ được thay bằng một delta
nữa. Nên `r4` giữ đúng phần **không thể sai theo cách đó**: hai câu đổi, băm, phạm vi. Lý lẽ chuyển
sang #297, nơi nó **được phép sai và được sửa**.

---

## 5. Những gì `r4` tự khai là CHƯA ĐO ĐƯỢC

- **KHÔNG khai "đã quét hết".** Số đo được là **hai** chỗ hình dạng `A` cộng **một** chỗ đã được
  chủ kho xếp ngoài phạm vi. `"chỉ ba"` là kết luận của **một** phép quét theo cụm từ — một **danh
  sách đoán trước**. Còn lời khai nào cùng hình dạng mà **không** chứa cụm `"chân Ubuntu"` hay
  không: **CHƯA ĐO ĐƯỢC**.
- **Số `r4` là TÁI DÙNG.** Đo được: path **vắng ở base `9044a5d`** và vắng ở mọi **cây kết quả**
  của `master` đã quét; nhưng hai commit `ee545cf5` (thêm) và `e87eae9d` (rút) **reachable từ
  `master`** qua PR #293. Hai sự kiện khác nhau — đừng gộp. Bản cũ cùng mục đích; tra `ee545cf5`.
  **Định danh là BĂM, không phải tên bản.**
- **Băm hai tệp bị thay đo tại chỗ**, ghi ở khối đầu. Băm không khớp ⇒ `r2`/`r3` đã bị động ⇒ `r4`
  phải được xét lại, không được dùng.
