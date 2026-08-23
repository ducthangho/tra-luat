Cây review sạch, HEAD không đổi, 27 bản sao đột biến nằm trong `/tmp/h`.

```
KET_LUAN: can_sua
reviewed_sha: b0c8fb368d70f17bce5eb7e3d1fe02d810db8e19
```

## Kiểm lại phiên điều phối — 5/5 khớp, một chỗ cần đính chính về VỊ TRÍ

| phép đo | tôi đo được | kết |
|---|---|---|
| suite trên `b0c8fb3` | `72/72 đạt; đã chạy=72, bỏ qua=0`, rc=0 | khớp |
| P1-2 hằng số trá hình | `70/72`, rc=1, đỏ `t71`+`t72` | khớp |
| write-set `ba82b06f..b0c8fb3` (3 tệp mã) | `+116/-20`, 2 tệp; `lease_publish.py` vắng ⇒ khớp byte | khớp |
| actionlint 5 workflow | master `2ab3560`: **đúng 1** finding `ops-don-ref.yml:106 SC1003:info`; `b0c8fb3`: y hệt ⇒ **DELTA = 0** | khớp |
| băm 5 tệp hồ sơ | 5/5 khớp | khớp |

**P1-1 — con số `72/73` của anh KHÔNG dựng được ở vị trí handoff khai.** `_dong_tong_ket` lấy `da_chay = len(CA) - len(bo_qua)`, mà `len(CA)=72`, nên `đã chạy=73` **chỉ có thể** xảy ra khi đột biến THÊM một ca. Tôi dựng lại cả hai (mọi bản qua `ast.parse` trước):

```
bơm @ca t73 raise BoQuaNen()        -> 72/73 đạt; đã chạy=73, bỏ qua=0 ; rc=1 ; ĐỎ=1   <- bản của anh
thay guard trong _chay_buoc_dang    -> 64/72 đạt; đã chạy=72, bỏ qua=0 ; rc=1 ; ĐỎ=8   <- bản của handoff
```
Kết luận không đổi (cửa sau đã khoá, `bỏ qua=0`, rc=1 cả hai) nhưng bản anh chạm **1** ca, bản handoff chạm **8**. Anh đo bản yếu hơn.

## Q8 — đúng như anh nghi: KHÔNG AI CƯỠNG CHẾ

```
grep -rn "co_names" ops/ .github/   -> 1 dòng DUY NHẤT: lease_publish_test.py:2608 (thân t70, không phải cổng W9)
grep -rln "W9"  ops/*.py .github/workflows/*.yml -> KHÔNG TỆP NÀO
```
Thủ tục `W9` sống trong r3 và trong một bảng của handoff, **không sống trong lượt chạy nào**. Lần sau ai bỏ qua nó, không có gì đỏ. Đây là hình dạng **E** ở tầng đặc tả, đúng như anh tự nghi.

**Nhưng bảng `W9` của handoff là THẬT** — tôi chạy lại đúng thủ tục, ba con số trùng tuyệt đối: W6′ `69/71` rc=1 · W7′ `69/71` rc=1 · W8 `71/72` rc=1.

## Sáu chỗ nghi — trả lời bằng chạy

**#2 `W9` cho `W8` rỗng theo cấu tạo — nhưng `W8` KHÔNG rỗng.** Ba đột biến riêng rẽ, đều ĐỎ (verdict lượt 1 đo cả (a) lẫn (b) đều rc=0):
```
(a) bỏ vòng in lý do          -> 71/72, rc=1, ĐỎ t72
(b) hạ tổng ket ve {qua}/{len(CA)} -> 71/72, rc=1, ĐỎ t72
(c) bỏ riêng phần "bỏ qua=N"  -> 71/72, rc=1, ĐỎ t72
```
`t72` chạm `W8` qua `main()`, không gọi `_dong_tong_ket`. Tập gỡ rỗng ở đây là kết quả ĐÚNG, không phải lỗ hổng. **`W8` ĐẠT.**

**#1 `W9` cho `W7′` gỡ `t70`:** nhãn lỏng (handoff gọi `t70` là "ca gọi thẳng helper dùng chung") nhưng vô hại — `t70` là ca DUY NHẤT gọi thẳng `_ly_do_bo_qua_workflow`, và hai ca còn đỏ (`t71`,`t72`) đều đi qua `main()`. Không phải phát hiện.

**#4 Q10:** hằng số không qua được — chuỗi `"ubuntu-"+tên tạm` không đoán trước được. Q10 giữ.

**#5 Tám ca ĐI QUA dẫn xuất trên tệp THẬT** (`nen=nt` trả `ops-publish-lease.yml:dang … 'ubuntu-latest'`). Ma trận `runs-on` trên workflow thật, chạy trên Linux thật:
```
ubuntu-latest / [ubuntu-latest]  -> rc=0, 72/72        (nt: có lý do · posix: rỗng)
windows-latest / matrix[ub,win]  -> rc=0, 72/72        tám ca VẪN CHẠY trên Linux   [= P2-2, ngoài phạm vi, KHÔNG nặng thêm]
matrix.os thiếu strategy / ${{ env.X }} / rỗng -> rc=1, ĐỎ t33 (actionlint), KHÔNG phải t71/t72
```

**#3+#6 trạng thái thứ ba: VẪN BỊ GỘP, và lượt 3 THÊM một chỗ gộp mới** — xem P2-5.

---

## P1-3 (MỚI, trong phạm vi) · Cửa sau chưa khoá TẠI GỐC — cổng nền không có phản chứng nào

Q9 tự khai *"Ca không còn khai được lý do thì không còn cửa sau nào"*. Đo được là **còn**. Một đột biến MỘT MỆNH ĐỀ, bỏ cổng nền trong `_ly_do_bo_qua_workflow`:

```
-    if (nen or os.name) == "nt" and nhan and all(
+    if nhan and all(
     -> lease_publish: 64/64 đạt; đã chạy=64, bỏ qua=8 ; rc=0     <- XANH
```
Tám ca `_chay_buoc_dang` **biến mất im lặng trên chính chân Ubuntu — chân LUÔN chạy** — và suite vẫn `rc=0`. Đối chứng `X2` (xoá hẳn dây nối) cũng `72/72 rc=0` trên Linux. Cả ba ca mới (`t70`,`t71`,`t72`) đều ép `nen="nt"`; **không ca nào đo nhánh `posix`**, nên nhánh quyết định "có được bỏ qua hay không" không có ai canh. Thứ duy nhất chặn là người đọc dòng `bỏ qua=0` trong log CI — đúng nghĩa hình dạng **E**, lần **4**. Q9 khoá phần LIỆT KÊ ĐƯỢC (chuỗi lý do) chứ không khoá phần THẬT SỰ CHẶN (nền).

**Ca vá đã CHẠY, không phải đề xuất trên giấy — 5 dòng, đặt ở dây nối, tuân Q8 (đi qua `main()`, không gọi thẳng helper):**
```
ban nguyên vẹn -> 73/73, rc=0   (XANH)
dưới X1        -> 64/65, rc=1, ĐỎ t73_nen_posix_khong_duoc_bo_qua_ca_nao
```

## P2-5 (MỚI — làm NẶNG THÊM P2-3, ngoài phạm vi nhưng phải báo)

`except Exception: ly_do = ""` trong `main()` là chỗ gộp MỚI, `edc1906` không có nó. Ba nguyên nhân khác hẳn nhau ra **cùng một câu**:
```
đường dẫn không tồn tại -> ĐỎ "bỏ qua không dẫn xuất được từ runs-on"
YAML hỏng                -> ĐỎ "bỏ qua không dẫn xuất được từ runs-on"
matrix không phân giải   -> ĐỎ "bỏ qua không dẫn xuất được từ runs-on"
```
Fail-close (rc=1, không mất an toàn) nhưng chẩn đoán SAI: hai ca đầu là **KHÔNG ĐO ĐƯỢC**, câu kia nói người đọc đi tìm `runs-on`. Vá ≈ 3 dòng (mang `type(ex).__name__: ex` vào thông điệp).

## Xác nhận phép đo `t33` của anh — ĐÚNG, và tôi đo được thẳng

```
actionlint 5 workflow, CÓ shellcheck    -> rc=1, 1 finding SC1003
actionlint 5 workflow, VẮNG shellcheck  -> rc=0, 0 finding      <- luật nền biến mất SẠCH
```
`t33` chỉ `assert shutil.which("actionlint")`, không hỏi `shellcheck`, và chỉ lint **một** tệp `ops-publish-lease.yml` — trong khi docstring của nó viết *"phải XANH trên MỌI workflow"*. Ngoài phạm vi (có từ #227), không tính là phát hiện lượt này.

## Ngân sách

Đã dùng **116/120**, còn **4**. Đóng P1-3 ở mức dây nối = **5 dòng đã đo** ⇒ **vượt trần đúng 1 dòng**. Thêm P2-5 (≈3) ⇒ **8**, vượt **4**. Đây rơi trúng điều kiện DỪNG của r3 (*"đóng trọn P1 ở mức dây nối không lọt 120 dòng ⇒ DỪNG, báo số dòng đo được"*): **cần nới 120 → 125 cho riêng P1-3, hoặc 120 → 128 nếu gộp P2-5.** Không thu nhỏ phép đo cho vừa trần.

## `chua_do_duoc`

- Windows thật trên `b0c8fb3` (nhận `W3′` của anh, không dựng lại).
- Hành vi của P1-3 trên chân `windows-latest` thật — suy được là `64/64 bỏ qua=8` y hệt bản đúng, tức **không chân CI nào đỏ**, nhưng chưa chạy Windows thật.
- `shellcheck` có/vắng trên runner `windows-latest` — không đo được từ log; đo được là dù thế nào `t33` cũng không cho biết.

## `hinh_dang_ke_thua` sau lượt này

**A**=7 · **B**=2 · **C**=1 · **D**=3 · **E**=**4** · **F**=2

**E chạm 4 ⇒ điều kiện DỪNG đã đăng ký kích hoạt.** Kết `can_sua`, không đề xuất chương trình vá tiếp — chỉ giao lại con số 5 dòng (đã chạy, đã đỏ đúng chỗ) để người giữ kho quyết nới trần hay đóng packet.
