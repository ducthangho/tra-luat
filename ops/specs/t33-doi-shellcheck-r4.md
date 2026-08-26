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

Lý lẽ, phép đo, lịch sử quyết định và hồ sơ cross-review của chính bản delta này nằm ở **#297**
(`ho_so_lap_luan` ở khối đầu tệp).

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

Câu thay thế là bản vá **đã qua review và đã land** ở `3239279b`, hôm nay vẫn đứng nguyên trong mã
tại `ops/lease_publish_test.py:3134`. `r4` **chép** nó, theo `#238/r4/Q13`.

Chỗ sai của câu cũ: `"toàn chân Ubuntu"` chỉ một **job/leg của CI**; bằng chứng trong hồ sơ là một
lượt chạy **cục bộ**.

---

## 2. `r2:215` — NGOÀI phạm vi

Câu ở `r2:215` (`toàn bộ chân Ubuntu im lặng`) **không** thuộc phạm vi `r4` và **không** được sửa.

Quyết định của chủ kho, in-session `2026-08-26`: `r2:215` **không** phải hình dạng `A`.

Đo được: `r2:215` viết `toàn bộ chân Ubuntu`; `r2:232` viết `toàn chân Ubuntu` — **khác byte**.

---

## 3. `r4` KHÔNG làm gì

- **Không** dựng cơ chế trạng thái máy đọc được (hướng (2) của #297) — packet riêng, chưa có đặc tả.
- **Không** sửa `r2:215`. **Không** đụng `r1`. **Không** đo lại toàn bộ số của `r2`/`r3`.

---

## 4. Những gì `r4` tự khai là CHƯA ĐO ĐƯỢC

- **KHÔNG khai "đã quét hết".** Số đo được là **hai** chỗ hình dạng `A` cộng **một** chỗ đã được
  chủ kho xếp ngoài phạm vi. `"chỉ ba"` là kết luận của **một** phép quét theo cụm từ — một **danh
  sách đoán trước**. Còn lời khai nào cùng hình dạng mà **không** chứa cụm `"chân Ubuntu"` hay
  không: **CHƯA ĐO ĐƯỢC**.
- **Số `r4` là TÁI DÙNG.** Đo được: path **vắng ở base `9044a5d`** và vắng ở mọi **cây kết quả**
  của `master` đã quét; **và** hai commit `ee545cf5` (thêm) `e87eae9d` (rút) **reachable từ
  `master`** qua PR #293. Hai sự kiện khác nhau — đừng gộp. Bản cũ cùng mục đích; tra `ee545cf5`.
  **Định danh là BĂM, không phải tên bản.**
- **Băm hai tệp bị thay đo tại chỗ**, ghi ở khối đầu. Băm không khớp ⇒ `r2`/`r3` đã bị động ⇒ `r4`
  phải được xét lại, không được dùng.
- **Cổng không đọc tệp này.** `doc-claims-check --strict` quét sáu root và **không** gồm
  `ops/specs`. Ba cổng xanh không xác nhận một câu nào ở đây.
