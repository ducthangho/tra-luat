Đã đo xong. Cây review sạch, `HEAD` không đổi (`7f91ea1c…`), mọi đột biến chạy trên bản sao tạm trong `/tmp`.

```
KET_LUAN: dat
reviewed_sha: 7f91ea1cffe17af391362a91b83907c32b16f3b2
```

## 0. Kiểm băm nguồn — 3/3 khớp

`-r4.md` `11972e8c…` · verdict lượt 2 `e5dd9584…` · `-r3.md` `130b6d29…`. Tệp mã: `sha256 = c378e6b0f934aa0236086c58002bfcc01a9db16cf1bc2c3a0938f1009609f061` — khớp tiền tố anh khai.

## 1. Kiểm lại anh — 6/6 khớp, không con số nào lệch

| anh khai | tôi đo | |
|---|---|---|
| write-set `ba82b06f..7f91ea1` = 2 tệp, +124/−20 | y hệt | ✔ |
| trần 125, dư 1 | và `ba82b06f..b0c8fb3` = **+116/−20** ⇒ delta đúng **8** | ✔ |
| `ops/lease_publish.py` không đổi một byte | vắng khỏi `b0c8fb3..7f91ea1` | ✔ |
| nguyên vẹn 73/73, chạy=73, bỏ qua=0, rc=0 | y hệt (cả trong cây review lẫn bản sao `/tmp`) | ✔ |
| +X1 → 64/65, chạy=65, bỏ qua=8, rc=1, ĐỎ `t73` | y hệt | ✔ |
| X1 không kèm bản vá → 64/64, bỏ qua=8, rc=0 XANH | y hệt | ✔ |

**Q13 (chép nguyên văn) đo trên thứ ĐÃ ĐẾN, không trên thứ đã gửi:** khối ```python duy nhất của r4 (`sha256` khối `c96483ba7baf95ff…`) nằm trong tệp **đúng từng byte**, xuất hiện đúng **1** lần, và phần giữa nó với `def main()` là đúng `'\n\n'`.

**W3′ — tôi không nhận lời khai, tôi đi lấy log.** `actions_get` run `32567293842`: `head_sha=7f91ea1cffe17af391362a91b83907c32b16f3b2`, `run_attempt=1`, `event=workflow_dispatch`, `conclusion=success`, 2 job đều success. Tải blob log và grep:
- `windows-latest`: đúng **8** dòng `BỎ QUA`, đúng 8 ca `_chay_buoc_dang`, mỗi dòng in `runs-on đã đọc được: 'ubuntu-latest'` → `lease_publish: 65/65 đạt; đã chạy=65, bỏ qua=8`
- `ubuntu-latest`: `73/73 đạt; đã chạy=73, bỏ qua=0`

`t73` không nằm trong 8 dòng bỏ qua ⇒ nó **chạy thật và xanh** trên chân Windows.

## 2. Tôi đã tấn công `t73` bằng những gì — 14 đột biến, mọi bản qua `ast.parse` trước

| đột biến | số đo | ai bắt |
|---|---|---|
| **X1** bỏ mệnh đề nền | 64/65 rc=1 | **CHỈ `t73`** |
| **X2** đảo `!= "nt"` | 63/65 rc=1 | `t72`+`t73` |
| **X3** `os.name` → hằng `"nt"` | 64/65 rc=1 | **CHỈ `t73`** |
| **X13** `main()` luôn dẫn xuất với `nen="nt"` | 72/73 rc=1 | **CHỈ `t73`** |
| **Q8/W10**: gỡ `@ca` của `t70` (ca DUY NHẤT gọi thẳng helper) + X1 | 63/64 rc=1 | `t73` vẫn đỏ ⇒ **W10 thoả Q8** (chưa ai chạy phép này) |
| X4 bỏ tham số `nen` (chỉ `os.name`) | 73/73 rc=0 | không ai |
| X5 `_chay_main_meta` bỏ qua tham số nền | 72/73 rc=1 | `t72` (`t73` xanh) |
| X9 `if ly_do:` → `if False:` | 72/73 rc=1 | `t72` (`t73` xanh vô nghĩa) |
| X8 đổi tên workflow · X7 = X8+X1 | 62/73 rc=1, **11 ĐỎ** | 11 ca khác (`t73` xanh vô nghĩa) |
| X11b `runs-on`→windows · X11 = +X1 | 73/73 rc=0 | không ai |
| X17/X18 phân biệt theo **TÊN TỆP** thay vì theo NỀN | 73/73 rc=0 | không ai trên chân Ubuntu |

**Hướng 1 (xanh mà không đo gì).** Vì `_chay_main_meta` đặt `CA[:] = [fn]`, ba mệnh đề `rc==1` · `"ĐỎ" in out` · `"bỏ qua=0"` **suy sập thành ĐÚNG MỘT BIT**: ca duy nhất rơi vào `hong`. Ba nguyên nhân cho bit ấy: (a) posix chặn — đúng ý; (b) `except Exception` nuốt lỗi (P2-5); (c) `main()` không bao giờ bỏ qua nữa. Tôi dựng cả (b) và (c): (b) kéo theo **11 ca ĐỎ**, (c) kéo `t72` ĐỎ. **Không có trạng thái nào `t73` xanh giả mà suite còn xanh.**

**Hướng 3 (chuỗi `"ĐỎ"`).** `ĐỎ` chỉ được IN ở đúng một chỗ (`main`, dòng 2676) và `CA` chỉ còn một phần tử ⇒ `"ĐỎ" in out` tương đương với "ca ấy hỏng". Không phải họ `t64 đếm chuỗi`: ở đó chuỗi đếm trên tập nhiều ca, ở đây tập có lực lượng 1 và ba mệnh đề khoá chéo nhau (bỏ qua ⇒ `rc=0` **và** `bỏ qua=1`).

**Hướng 2 (đỏ sai lý do).** Không dựng được. Mọi cách làm `_chay_main_meta` hỏng qua tệp/đường dẫn (X7/X8) đẩy `t73` về **XANH**, không về đỏ. `t73` không có chế độ đỏ giả — nó chỉ có chế độ xanh rỗng, và mọi chế độ ấy đều bị ca khác bắt ồn ào.

**Hướng 4 (X1 có phải đột biến duy nhất?).** Không — `t73` là **ca duy nhất** giết X1, X3 **và** X13. Đó là ba đột biến, không phải một, và hai trong ba (`os.name`→hằng; `main` giả định nền) là đúng hình dạng "hằng số trá hình" mà `Q10` sinh ra để chặn. Ca này mạnh hơn mức đặc tả đòi.

## 3. Phát hiện (không có P1/P2)

**P3-1 · Trục phân biệt không được `t73` khoá; chỉ chân Windows khoá, mà chân Windows không chạy cho PR thường.**
Phép đã chạy: X17 (`tep.name != "ops-publish-lease.yml"` thay cho mệnh đề nền) và X18 (giữ `nt` nhưng loại trừ chính tệp thật) ⇒ **73/73, rc=0** — toàn bộ chân Ubuntu, `t73` gồm trong đó, không thấy gì. Hai đột biến ấy làm 8 ca **CHẠY** thay vì bỏ qua trên Windows, tức chân Windows sẽ đỏ; nhưng `ci.yml` chỉ chạy `ubuntu` cho PR thường. Vì sao quan trọng: `t73` chứng minh *"nền posix thì tuple (tệp thật, job dang) không được bỏ qua"* — nó **không** chứng minh quyết định ấy tra theo NỀN. Cái tách hai thứ đó là 8 dòng `BỎ QUA` trên chân Windows, và chân đó phải gọi tay. Ngoài phạm vi `Q15` (r4 chỉ đòi đóng P1-3, và P1-3 **đã đóng**); ghi cho packet kế.
*Nếu người giữ muốn đóng ngay:* thêm mệnh đề `nen="nt"` phải cho lý do KHÁC RỖNG trên cùng tuple = **2 dòng `git diff --numstat`** — **vượt trần 125 đúng 1 dòng**, nên tôi **không** đề xuất làm trong lượt này.

**P3-2 · X4 sống sót (`nen` thành tham số chết) — thuộc `t70`, không thuộc lượt 4.** Đo: 73/73 rc=0. `t70` là ca duy nhất bơm `nen`, mà kỳ vọng của nó là chiều ÂM (`not ly_do`), nên nó xanh cả khi điểm bơm bị vô hiệu. Không đổi hành vi sản phẩm (đường sản xuất không truyền `nen`). Ghi lại vì lượt 4 **không** làm nặng thêm chỗ này.

## 4. Hai câu hỏi anh đặt riêng

**Nặng thêm ngoài phạm vi?** Không. P2-5 nay đỡ một phần bit của `t73` (X7/X8 cho thấy `t73` xanh vì nuốt lỗi chứ không vì posix) — nhưng đo được là trạng thái ấy **luôn** kèm 11 ca ĐỎ, nên rủi ro không tăng; nó chỉ thêm một lý do nữa để vá P2-5 ở packet kế. Không tính là phát hiện mới. Bảy mục P2/P3 lượt 1: không mục nào bị chạm.

**Handoff nằm trong reviewed commit?** Chỉ là nếp, không có hệ quả. Lease exec-4 khai `handoff_bat_buoc.path` đúng tệp ấy, và `ngan_sach_kich_thuoc.don_vi` ghi rõ *"trên write_set"* — `ops/handoff/**` không thuộc write_set (3 đường: `.yml`, `lease_publish.py`, `lease_publish_test.py`) ⇒ 9 dòng handoff không vào 124. Đo hai chiều: `2ab3560a..HEAD` = 4 tệp `+760/−21`; `ba82b06f..HEAD` **trên write_set** = 2 tệp `+124/−20`. Hạt sạn có sẵn (không do lượt 4): dòng `gate_bat_buoc` viết `git diff --numstat ba82b06f..HEAD -> <= 3 tệp` mà không nhắc write_set — đọc nguyên văn thì range đó ra **58 tệp**, vì `ba82b06f` là tổ tiên xa và mọi việc master chen giữa đều nằm trong. Chỉ `don_vi` cứu câu ấy; nên sửa câu, không phải sửa số.

*Ngoài phạm vi, xác nhận lại chứ không báo mới:* `actionlint` toàn kho `rc=1` (SC1003 ở `ops-don-ref.yml`) — verdict lượt 2 đã báo; tệp ấy khớp `origin/master` từng byte ⇒ **delta = 0**. Kèm một chỗ trôi: `CLAUDE.md` còn ghi *"actionlint trên cả 5 workflow của kho → rc=0"*, nay sai. Không gate nào đỏ vì `don_ref_chot_test.sh` gọi `-shellcheck=`.

## 5. `chua_do_duoc`

- **"codex chép đúng bản `claude` đã chạy"** — tôi đo được sha256 tệp khớp con số anh khai, nhưng cây review lượt 2 không có trong kho, nên mắt xích *"bản ấy đã CHẠY ở đó"* là suy từ một chuỗi băm, không đo độc lập được. (Không đổi kết luận: tôi đã chạy lại cả ba số của `W10` từ đầu.)
- `shellcheck` có/vắng trên runner `windows-latest` — vẫn không đo được từ log.
- X17/X18 trên chân Windows THẬT (suy: 8 ca chạy thay vì bỏ qua ⇒ đỏ; chưa chạy — không dựng lại lượt Windows theo yêu cầu).
- Nguyên nhân gốc vì sao 8 ca `_chay_buoc_dang` phải bỏ qua trên Windows: vẫn né, chưa ai đo.

## 6. `hinh_dang_ke_thua` sau lượt này

**A**=7 · **B**=2 · **C**=1 · **D**=3 · **E**=**4** · **F**=2 — **không đổi**. Lượt 4 không mô tả phép dẫn xuất mới nào (r4 cố ý chỉ chép), nên không có biểu hiện **E** thứ năm. Không có bộ đếm nào chạm ngưỡng DỪNG.

**Vì sao `dat` dù đây là mã của nhà cung cấp tôi:** `t73` là ca duy nhất giết ba đột biến độc lập (X1, X3, X13), giữ nguyên răng sau khi gỡ ca gọi thẳng (Q8), chép đúng từng byte, lọt trần với 1 dòng dư, và có bằng chứng chạy thật trên cả hai chân CI ở đúng exact head. Thứ nó không khoá (P3-1) nằm ngoài `Q15` và không đóng được trong 1 dòng còn lại.
