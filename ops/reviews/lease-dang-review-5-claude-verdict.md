Đo xong. Cây review sạch, `HEAD` không đổi (`ba82b06f…`), mọi đột biến chạy trên bản sao `/tmp/rv5.tVw8/`.

```
KET_LUAN: dung_lai
reviewed_sha: ba82b06f9df81fc2f13786fec590ec2110d046b7
```

**Băm đã kiểm** — spec r7 `623b2355…0cb4` ✓ · verdict lượt 4 `0655b9d0…614f` ✓ · handoff `08b61f52…`. `numstat cfaccff9..HEAD` = 3 tệp `+645/−19` ✓; delta lượt 7 = `ops/lease_publish_test.py` `+30/−18` ✓ (YAML **không** đổi lượt này: 310 dòng ở cả hai head). Nền `68/68` rc=0.

---

## P1 — `bao_chan` KHÔNG phải dấu hiệu bắt buộc của nhánh chặn; Q32 vẫn khoá theo CÁCH VIẾT ⇒ **E lần 2**

Dựng bốn nhánh chặn **thật** trong thân bước `đăng` (bản sao tạm), chạy suite đầy đủ:

```
[E1-BI_CHAN-thang] rc=0 lease_publish: 68/68 đạt ĐỎ=[]
[E2-exit1-thang]   rc=0 lease_publish: 68/68 đạt ĐỎ=[]
[E3-im-lang-rc6]   rc=0 lease_publish: 68/68 đạt ĐỎ=[]
[E4-doi-ten-ham]   rc=1 lease_publish: 65/68 đạt ĐỎ=['t64…','t66…','t67…']
```

- **E1** — chèn một guard thật (`python3 -c "…yaml.safe_load…"` + `rc=$?`) rồi chặn bằng `echo ::error…; BI_CHAN=1; echo "::endgroup::"; continue`, **không gọi `bao_chan`**. `actionlint` rc=0 (t33 xanh), `t64` xanh vì đếm `bao_chan` vẫn = 9. Đây **đúng hình dạng D3/D4** mà `r7` tuyên đã đóng — chỉ đổi cách viết.
- **E2** — `exit 1` thẳng trong vòng lặp: phá luôn bất biến cô lập lease mà `t51` sinh ra để giữ (lease sau không được xử lý), **không ca nào kêu**.
- **E3** — nguy nhất, và là **fail-open thật**: chèn `if [ "$rc" = "6" ]; then echo "::endgroup::"; continue; fi` ngay trước guard `check`. `RC_NEO = 6` (`ops/lease_publish.py:43`, ném ở 7 chỗ — lệch băm neo prompt). Sau đột biến, lease **lệch băm neo bị bỏ qua IM LẶNG và bước XANH** thay vì `BI_CHAN=1`. Đồ giả chỉ sinh rc ∈ {0, 8, 9} nên không ca nào chạm rc=6. `68/68`.
- **E4** (đổi tên hàm) là **cái duy nhất** bị bắt — vì nó phá phép **đếm chuỗi**, không phải vì cổng hiểu "chặn".

Nói cho công bằng: lời khai của executor về **thân hiện tại** là ĐÚNG, tôi đo lại độc lập và khớp — `bao_chan` = 9 · `continue` = 13 (9 nhánh chặn + 2 bộ lọc đầu vào + 2 đường `rc=9`) · `exit` = 1 (nằm **ngoài** vòng lặp) · `BI_CHAN=` = 2 (khởi tạo + trong `bao_chan`). Cái sai không nằm ở lời khai mà ở **suy luận từ nó sang thiết kế cổng**: Q32 biến một mô tả về thân hôm nay thành một giả định về mọi thân mai sau, và cổng không cưỡng chế giả định ấy. `bao_chan` là **một cách viết** của "chặn"; `BI_CHAN=1`, `exit 1`, `continue` im lặng là những cách viết khác. Nguyên văn verdict lượt trước: *"distinguishes spelling, not authority"* — câu ấy vẫn đúng nguyên si sau khi đảo danh sách.

Chuẩn bằng chứng của chính packet này cho hình dạng E/D là **dựng** (P2-2 lượt 6 cũng dựng `if ! cmd` chứ không tìm thấy sẵn trong thân). Theo đúng chuẩn ấy: **E lần 2**, và chốt `r7` viết thẳng *"E lần 2 ⇒ DỪNG, không vá"*.

Hai cách đọc, người giữ kho quyết (tiền lệ: bộ đếm D lượt 6):
- **hẹp** — "tìm được trong thân hiện tại": KHÔNG kêu, thân sạch.
- **theo chuẩn đã dùng** — "dựng được nhánh chặn mà cổng không thấy": **kêu**.

**Bản vá nếu người giữ kho chọn đi tiếp thay vì dừng** (con số theo yêu cầu, ngân sách còn **15**):
- Khoá **băm thân bước** — hằng số + một ca: **≈ 9–10 dòng, LỌT**. Băm hiện tại `sha256(run) = 397f64e4c0f01be7b8c54cefe1c017349013cdf70589a3d439512305b71eed1d` (2934 byte). Đây là hình dạng duy nhất **không còn cách viết nào để lách**: nó không mô tả thân, nó từ chối mọi thay đổi chưa qua tay người, buộc đi lại `t64/t66/t67`. Giá phải trả: đỏ cả với sửa mỹ phẩm — đó chính là tính năng.
- Đảo sổ sang **mọi lối ra vòng lặp** (`continue`/`exit`/`break`) + `BI_CHAN=`, 13+1+2 mục: **≈ 13–15 dòng, sát trần**, và vẫn là liệt kê cách viết (nhánh chặn *không* `continue` vẫn lách được).

---

## P2 — hồi quy trong 18 dòng bị xoá: mất bất biến `set +e … rc=$? … set -e`

Bộ trích cũ đòi **mọi** `set +e` phải là một khối đóng. Bộ trích mới chỉ đếm `bao_chan`, bất biến ấy biến mất **không ai khai**. Đo trên **cả hai** head, cùng một đột biến:

```
[truoc/nen]              rc=0 67/67  ĐỎ=[]
[truoc/mat-set-e]        rc=1 66/67  ĐỎ=['t64…']
[truoc/post-mat-set-e]   rc=1 66/67  ĐỎ=['t64…']
[nay/nen]                rc=0 68/68  ĐỎ=[]
[nay/mat-set-e]          rc=0 68/68  ĐỎ=[]      ← SỐNG SÓT
[nay/post-mat-set-e]     rc=0 68/68  ĐỎ=[]      ← SỐNG SÓT
```

Xoá `set -e` sau khối `check` (hoặc sau khối POST) ⇒ `errexit` tắt suốt phần còn lại của bước. Nói cho đúng phạm vi: trong **thân hôm nay** đột biến này gần như tương đương hành vi (mọi lệnh đáng kể đều đã tự kiểm `rc`), nên không ca hành vi nào bắt được — thứ mất là **bất biến cấu trúc**, và nó mất đúng trong 18 dòng mà prompt bảo soi từng dòng. Bảng đột biến của handoff khai `16/16 đỏ` nhưng **không** chạy lại họ D cũ trên head mới, nên chỗ hụt răng này không lộ ra ở đó. Chữa rẻ nhất: giữ thêm một phép đếm `set +e` == số khối đóng (**≈ 3 dòng**) — nhưng nó nằm cùng ngân sách với P1.

---

## Mục 2 — phép đếm CÓ ba trạng thái ✅

```
[M2a-doi-ten-buoc] rc=1 57/68 ĐỎ=[… t64 t65 t66 t67 t68]
[M2b-than-rong]    rc=1 57/68 ĐỎ=[… t64 t66 t67 t68]
[M2c-dem-ra-0]     rc=1 61/68 ĐỎ=[… t64 t66 t67 t68]
```
Không trích được thân (đổi tên bước) · thân rỗng · **đếm ra 0** (`bao_chan "` → `echo "::error::`) — cả ba **ĐỎ**, `t64` đỏ ở cả ba. `bang(bao and …)` chặn đúng ca `0 == 0`. Không có finding.

## Mục 3 — `t68` đo thật cả ba vế, đồ giả GIỮ TRẠNG THÁI ✅

```
[M3-ve-rc]                rc=1 63/68 ĐỎ=[… t66 t68]   (BI_CHAN không còn làm bước thoát 1)
[M3-ve-marks]             rc=1 66/68 ĐỎ=['t66','t68'] (giữ bao_chan, bỏ `continue` ⇒ CHỈ marks lật)
[M3-ve-do-gia-dien-kich]  rc=1 66/68 ĐỎ=['t66','t68'] (đồ giả in id số + rc=1 nhưng KHÔNG ghi comment)
```
Vế `marks` có đột biến giết **riêng** nó (không phải trang trí). Vế `posts.count("giua")==1` chết ngay khi đồ giả chuyển từ **giữ trạng thái** sang **diễn kịch bản** — đúng phép đo mà prompt đòi. Không có finding.

## Mục 4 — hồi quy phần còn lại ✅ (ngoài P2)

Đổi khoá sổ từ **lệnh** sang `bao_chan "…"`: `_ve_dan_xuat` so vị trí vẫn đúng vế (`post_rc`, `case_id` nằm sau dòng `ID=$(gh api`), `t66` đổi `" mark " in x` → khoá theo nhãn `loi == "mark"` (bền hơn). `_ve_dan_xuat` tự tìm dòng POST **từ thân** thay vì từ sổ — bắt buộc, vì sổ không còn chứa lệnh POST. Q34 có răng riêng, đo được:
```
[Q34-next-mac-dinh] rc=1 67/68 ĐỎ=['t65…']
[Q34-boc-try]       rc=1 67/68 ĐỎ=['t65…']
```
Q35 (`ghe.exists()` → `is_file()`): không ca nào yếu đi — chỉ `t51`/`t52` đọc `kq["env"]` và cả hai chạy đường bình thường; đường `guard_hong="github_env"` (biến `$GITHUB_ENV` thành thư mục) trước đây ném `IsADirectoryError`, nay trả `""`, `t66` không đọc trường đó. Tách mục #6 thành `post_rc` + `case_id`: **mạnh lên**, hai ca khác nhau, cả hai bị `t66` phủ, `t68` phủ riêng `post_rc`. Sổ 9 mục = 9 lời gọi `bao_chan`, **không `+1`** ✓.

## Mục 5 — bộ đếm hình dạng

**A** = 6 · **B** = 2 · **C** = 1 · **D** = 3 (giữ; P2 ở trên là hồi quy phạm vi đo, không phải đổi độ mịn câu hỏi) · **E** = **2** (P1). Theo chốt `r7`: **DỪNG, không vá, xuất handoff.**

---

**`da_do_gi`** — băm spec/verdict ✓ · `numstat` hai mốc ✓ · nền `68/68` ✓ · 4 đột biến "nhánh chặn không `bao_chan`" (3 lọt, 1 chết) · 3 đột biến ba-trạng-thái của phép đếm (3 đỏ) · 3 đột biến từng vế `t68` + đồ giả diễn kịch bản (3 đỏ) · 6 lượt hồi quy `set ±e` **so hai head** (2 mutant chết→sống) · 2 phản chứng Q34 (2 đỏ) · đếm độc lập `bao_chan`/`continue`/`exit`/`BI_CHAN=` trong thân YAML · đọc từng dòng diff `+30/−18`. Tổng 20 lượt suite, mỗi lượt ~15s, đều trên bản sao tạm.

**`khong_do_duoc`** — **thu hẹp**: không mục nào của `chua_do_duoc` r2–r7 khai hẹp hơn thực tế; mục 1 ("chỉ đột biến, không rà nội dung `lease_publish.py` +105/−7 và YAML +70/−8") đúng và tôi cũng không rà — lượt này vẫn là review **delta**. **Chưa đóng**: Actions THẬT · Windows · `gh` thật (bảy lượt, không đóng được từ trong container) · cửa sổ "POST xong, `mark` hỏng" (cấm vá) · khe race hai nhánh `ops/**` · nợ `chay(env=None)` · nhánh "một phần" trong `_doc_gh`/`_kiem_loai_so_hieu`/`_kiem_comment_da_co` · `t59` chỉ so `argv[0:2]` · ruleset ngoài kho — thứ này vẫn là biên thật của cả đường: chưa đặt ruleset thì "ai push được vào `ops/**` thì đăng được", và không bản vá trong kho nào đổi được điều đó. **Mở thêm sau lượt này**: cổng không ràng buộc nhánh chặn viết bằng cách khác `bao_chan` (P1) và không còn ràng buộc hình dạng khối `set +e` (P2).
