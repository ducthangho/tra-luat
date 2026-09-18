# Verdict lượt 2 — Packet #551 `ASSURANCE-NEO-VAO-HO-MODEL` (r3/g3)

- **Kết luận:** `changes_requested` — **1 P1 · 1 P2** còn mở với bản vá, **cộng 2 khuyết tật của CHÍNH ĐẶC TẢ/LEASE** cần chủ kho quyết
- **Neo `reviewed_sha`:** `d8ef235a312533515f2c73f2ea73de714f67a78e`
- **PR:** [#557](https://github.com/ducthangho/tra-luat/pull/557) · nhánh `claude/assurance-ho-model-r2-g2`
- **Đặc tả:** `ops/specs/assurance-neo-vao-ho-model-r3.md`, `sha256 fbe599fb21dcb567e8028b0142f6391fecbaa50002e6914a6aa0a76f3e53737c`
- **Lease:** `assurance-ho-model-r3-g3-antigravity` · executor `agy` · reviewer `claude`
- **Thời điểm đo:** `2026-09-18T13:13Z` (phép đo chạy `13:04Z`–`13:13Z`)

## 0. Giới hạn của lượt này — đọc trước mọi phát hiện

**Lượt này KHÔNG phải `cross_approved`, và lý do khác lượt 1.** Bản vá (`d8ef235`) do executor
`agy` viết, nên phần đối chiếu **triển khai** là độc lập thật — khác hẳn lượt 1. Nhưng:

1. Phiên này **soạn cả ba đặc tả** (r1, r2, r3) và **ghi cả ba lease**. Đối chiếu tiêu chí vẫn là
   tự chấm bài mình ra đề. Mục 3 dưới đây là hệ quả trực tiếp: **hai trong bốn phát hiện là lỗi của
   ĐẶC TẢ, không phải của executor.**
2. Họ model thật của `agy` ở lượt chạy này **KHÔNG ĐO ĐƯỢC** — đúng cái mà `M16` sinh ra để đóng,
   và `M16` chưa đóng được (xem `S1`). Nên cặp `claude`↔`agy` chưa xác lập là khác họ.

Mức cao nhất lượt này mua được: **`advisory_review`**.

## 1. Bảng đo — kê CẢ cái khớp

Rig: hai vế dựng trong **MỘT** lệnh (`cong551_l2.py`), clone thật, `checkout --detach`,
`core.abbrev 7`, `status --porcelain` rỗng. `rc` đọc TRỰC TIẾP từ `returncode`.

| cổng | nền `eb15657` | ứng viên `d8ef235` | delta |
|---|---|---|---|
| `ops/bien_nhan_v2.py` | rc=0 · `125 ĐẠT v2 · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 178` | rc=0 · **cùng số từng chữ** | **0** |
| `ops/bien_nhan_v2_test.py` | rc=0 · `48/48 ca · 63/63 CÓ RĂNG` | rc=0 · `58/58 ca · 71/71 CÓ RĂNG` | +10 ca, +8 đột biến |
| `doctrine-scan` | rc=0 | rc=0 | 0 |
| `adr-song` | rc=0 · 49/49 | rc=0 · **50/50** khớp 1–1 | +1 |
| `doc-claims-check --strict` | rc=0 | rc=0 | 0 |
| `git diff --check` | rc=0 | rc=0 | 0 |
| `release-verify --strict --json` | rc=0 | rc=0 | 0 |

`A9`: **đúng 6 tệp**, **+227 / −18** — dưới trần 250. Ước lượng của đặc tả r3 là 245–285; số thật
**227**, tức ước lượng ấy **cao hơn thực tế**, không phải thấp hơn. Ghi ra để lần sau đừng xin nới
trần dựa trên một ước lượng chưa ai kiểm.

**`M14` ĐẠT, và đạt ở mức chặt nhất.** Tám đột biến `m62`–`m69`, mỗi cái giết một ca **KHÁC NHAU**
(`c49` `c50` `c52` `c53` `c54` `c55` `c56` `c57`), **tất cả `giet_that`**, không cái nào
`tin_dung_gia`, không hai cái nào trùng ca đích. Đây đúng là thứ `M14` đòi: không phải bộ tương
đương. Đây là chỗ bản vá làm tốt nhất và phải nói ra.

**Bốn lớp ĐÓNG THẬT, đo bằng ca đối chứng biết trước đáp án:**

```
[doi chung] claude review codex          -> QUA    (rig song)
[doi chung] claude review claude         -> CHAN   (rig song)
P1-1  executor_provider VANG             -> CHAN   "khong xac dinh duoc ho model cua executor"
P1-2  agy KHONG khai model               -> CHAN   (bang mac dinh da BO google_antigravity)
      agy KHAI gemini                    -> QUA
      agy KHAI claude                    -> CHAN   "hai ben cung ho model claude"
P2-1  grok-4/grok-3, llama-*, deepseek-* -> deu tra '' => CHAN
P3-1  yi-o1, o1_preview, mistral-o3x     -> deu tra '' (khop chuoi con da bi siet)
```

`P2-2` đóng: §20 dòng `ADR-0050` nay ghi `ops/bien_nhan_v2.py (_NEO_LUAT_CHEP_TAY + chốt tách họ
model)` thay cho `**0 cổng**`.

`P2-3` đóng, và đóng **tốt hơn tôi yêu cầu**: ADR-0050 nay neo URL chỉ thị, sửa ngày `2026-09-17` →
`2026-09-18`, **và** tự khai đúng nguồn — *"quyết định kiến trúc do Đặc tả r2 đề xuất, chủ kho
`ducthangho` phê duyệt tại …"* — thay vì gán việc khởi xướng cho chủ kho. Đó là sửa đúng bản chất
lời khai về thẩm quyền, không chỉ dán một URL vào.

## 2. Phát hiện với BẢN VÁ

### P1-MỚI — Bất đối xứng: khai đè model của **reviewer** đòi bằng chứng, của **executor** thì KHÔNG

`ops/bien_nhan_v2.py`, khối `if khai == "cross_approved":`. Đo, không lọc thông điệp:

| ca | kết quả |
|---|---|
| reviewer khai đè `model`, **không** mức bằng chứng | **CHẶN** — *"khai đè model cho `cross_approved` mà thiếu mức bằng chứng model"* |
| executor khai đè `executor_model: gpt-5`, **không** mức bằng chứng | **QUA** |
| `agy` khai `executor_model: gemini-3`, **không** bằng chứng | **QUA** |
| `agy` khai `executor_model: gemini-3` **+ mức `khong_do_duoc`** | **CHẶN** |

Biến `override_rev` chỉ nhìn bốn trường của `model_reviewer_identity`; không có `override_exec`
tương ứng.

**Vì sao đây là P1 chứ không phải chi tiết:** `M16` của lease gen 3 đặt toàn bộ tính chính đáng của
`cross_approved` cho packet này lên việc `agy` khai `executor_model`. Bản vá cho lời khai ấy đi qua
**không cần một mẩu bằng chứng nào**. Cơ chế sinh ra để biến một **mặc định** thành một **phép đo**
lại biến nó thành một **lời tự khai không ai kiểm** — của đúng bên đang bị nghi ngờ về tính độc lập.

Tệ hơn, dòng cuối bảng cho thấy **đường TRUNG THỰC bị phạt**: `agy` khai thật *"tôi không đo được"*
⇒ CHẶN; `agy` chỉ viết `executor_model: gemini-3` và bỏ trống mức bằng chứng ⇒ QUA. Đây **cùng
hình dạng** với `P1-3` của lượt 1 (thang bằng chứng lật ngược) — hình dạng ấy nay **tái phát lần
thứ hai trong cùng một packet**, nên nó là lỗi LỚP, không phải lỗi chỗ.

**Đề xuất:** dựng `override_exec` đối xứng, và cho `do_may`/`khai_co_audit` của executor cùng đòi
hỏi như reviewer (`model_evidence_ref` / người audit). Kèm một ca **và một đột biến riêng** — gỡ
chốt đối xứng phải làm đúng một ca ĐỎ.

### P2-MỚI — `HO_MODEL_CHO_PHEP` là hằng số CHẾT, và docstring khẳng định sai về chính nó

`ops/bien_nhan_v2.py:152` khai `HO_MODEL_CHO_PHEP = frozenset({"claude","gpt","gemini"})`. Nó chỉ
xuất hiện thêm ở **docstring** dòng 641 và ở một bảng liệt kê trong tệp test. **Không dòng logic
nào đọc nó** — ba họ vẫn đấm cứng trong chuỗi `if`.

Đột biến tại chỗ, phản chứng chạy được:

```
truoc = _ho_model_cua_ten("gemini-2.5")  -> 'gemini'
HO_MODEL_CHO_PHEP = frozenset()          # xoa SACH bang cho phep
sau   = _ho_model_cua_ten("gemini-2.5")  -> 'gemini'     KHONG DOI
```

Thêm một họ vào bảng ⇒ không có gì đổi. Bớt một họ ⇒ cũng không. Đây là **một danh sách cho phép
không tồn tại đúng lúc nó cần tồn tại**, và docstring *"chuẩn hoá … trong `HO_MODEL_CHO_PHEP`"* là
một chú thích khẳng định về tệp mình đang nằm trong mà không đúng — kho đã trả giá cho đúng hình
dạng này.

**Đề xuất:** hoặc cho `_ho_model_cua_ten` thật sự kiểm kết quả qua `HO_MODEL_CHO_PHEP` (rồi thêm
đột biến: xoá một phần tử phải làm một ca ĐỎ), hoặc **xoá hằng số và sửa docstring**. Giữ nguyên là
để lại một cái bẫy cho người sau.

## 3. Phát hiện với ĐẶC TẢ và LEASE — lỗi của TÔI, không của executor

### S1 — `M16` giao nghĩa vụ cho một hiện vật KHÔNG TỒN TẠI

Lease gen 3 viết: *"Biên nhận **của executor** PHẢI khai `executor_model`"*. Đo trên kho:

```
kind tren 177 bien nhan trong ops/reviews/: {'review_delivery_receipt': 174, '<khong khai>': 3}
=> 0 bien nhan EXECUTOR, chua tung co
```

Và `_giai_ho_model_executor(d)` đọc `d.get("executor_model")` với `d` là **biên nhận của
REVIEWER**. Cộng thêm: `ops/reviews/**` **không** nằm trong write set của lease, nên `agy` cũng
**không có đường ghi** một biên nhận nào.

Nên `M16` không thể thi hành như đã viết, và cơ chế thật là: **reviewer khai hộ model của
executor**. Ghép với `P1-MỚI` thì thành ra `cross_approved` của packet này sẽ đứng trên việc
**reviewer đoán model của agy**, không ai kiểm. Đó không phải thứ `M16` định làm.

**Cần chủ kho quyết:** (a) đổi `M16` thành nghĩa vụ của **reviewer**, kèm đòi hỏi bằng chứng đối
xứng (`P1-MỚI`); hoặc (b) mở đường cho executor ghi biên nhận (thêm `ops/reviews/**` vào write set
⇒ **revision 4** theo §3.2); hoặc (c) chấp nhận `advisory_review` cho packet này và tách việc
attest model của agy sang nợ `AGY-CHUA-ATTEST-MODEL-TUNG-LUOT`.

### S2 — `A14` và `A3` của đặc tả r3 LOẠI TRỪ NHAU

`A14` đòi: mức bằng chứng **RỖNG ⇒ CHẶN**. `A3` đòi: số `ĐẠT v2`/`tổng` **KHÔNG ĐỔI** giữa nền và
ứng viên. Đo:

```
bien nhan khai cross_approved: 50
phan bo muc bang chung:        {'<RONG>': 50}
=> RONG bi CHAN thi 50/50 bien nhan THAT ro cong => A3 bat kha thi
```

**Executor chọn `A3` và bỏ vế RỖNG của `A14`. Đó là lựa chọn ĐÚNG** — `A3` bảo vệ một bất biến
thật (luật mới không hồi tố), còn `A14` viết quá tay. Nhưng nghĩa là **`A14` chưa đạt theo đúng
chữ của nó**, và đặc tả r3 tự mâu thuẫn.

Đây đúng cái §3.2 gọi tên: *"finding cho thấy chính spec thiếu thì verdict là `blocked` và đi qua
revision mới"*. Tôi **không** tự sửa đặc tả đã đóng băng; chủ kho quyết giữa: viết lại `A14` ở
**revision 4**, hay khai một miễn trừ có tên cho vế RỖNG.

**Ghi thêm cho trung thực:** khuyết tật này là của tôi, và nó thuộc đúng lớp mà kho đã trả giá —
`TIEU-CHI-THEO-GIA-TRI-TUYET-DOI`. Tôi viết `A14` bằng cách liệt kê các giá trị phải bị chặn mà
không đo xem dữ liệu thật đang ở giá trị nào. Hình dạng ấy nay ở mức **BỐN**.

## 4. Soát lại chính verdict lượt 1 (PR #558)

Đo lại bằng máy trên nhánh `claude/review-551-luot1-20260918` @ `673e054`:

| lời khai | đo lại | |
|---|---|---|
| `verdict_sha256` | `e039649c…` | **KHỚP** |
| `verdict_bytes` | 14 780 | **KHỚP** |
| `evidence_url` → blob `7d7f1224` | băm blob == băm verdict | **KHỚP** |
| `reviewed_sha` `f4684e45` | tra được | **KHỚP** |
| `findings_ids` = 7 vs `so_p1+p2+p3` = 7 | | **KHỚP** |

**Bảy phát hiện của lượt 1 đều đúng** — sáu cái đã được vá thật và đo được là đã đóng; cái thứ bảy
(`P1-3`) đóng một phần, phần còn lại là do `A14` của tôi viết sai chứ không phải executor bỏ sót.

Một khuyết tật của biên nhận lượt 1, phát hiện khi soát chéo: **`so_lop_mo` không có định nghĩa ở
bất kỳ tệp nào trong kho**, và đang được dùng với hai nghĩa — `wp541-review-1` đếm `P1+P2` (loại
P3), còn `doctrine-scan-review-2` (đã land) và lượt 1 của #551 đếm cả P3. Không cổng nào đọc
trường ấy. Đúng `L1`: *"mọi con số 'N thứ phải xử' phải khai N ĐẾM GÌ"*. Việc này không thuộc
packet #551 — nêu ra để chủ kho quyết mở nợ riêng.

## 5. Một lỗi của chính lượt đo này, ghi lại vì nó suýt thành phát hiện giả

Vòng đo đầu lọc thông điệp của `_thieu()` theo bốn cụm (`họ model` · `người audit` ·
`bằng chứng model` · `đo lường`). Thông điệp của nhánh `khong_do_duoc` viết *"mức bằng chứng"* —
**không** chứa cụm nào trong bốn cụm ấy. Kết quả: rig báo `khong_do_duoc ⇒ QUA`, và tôi suýt viết
thành một P1 rằng chốt ấy không có răng. Đo lại **không lọc** ⇒ nó **CHẶN**, đúng như bản vá khai.

Chỉ lộ ra vì tôi dừng lại hỏi *"bộ lọc của mình có mù không"* trước khi viết. Đây đúng bài học
*"bộ quét NHÁP của chính mình là thứ dễ tin nhất, nên nguy nhất"* — và lần này nạn nhân suýt là
executor.

## 6. Chưa đo được

- **`gate (windows-latest)`** — `manual_ci_budget: 0` theo chỉ thị chủ kho. **KHÔNG DÙNG PHƯƠNG
  TIỆN**, không phải *"đã đo và xanh"*.
- **Họ model thật của `agy`** ở lượt chạy sinh ra `d8ef235` — không có bằng chứng máy. Đây chính là
  `C4` của đặc tả r3, và `S1` giải thích vì sao nó vẫn chưa đóng được.
- **Lượt CI tự động trên `d8ef235`** — chưa đọc ở thời điểm viết; verdict này neo vào cây, không
  neo vào kết quả CI.

---

**Nguồn có thẩm quyền là tệp có băm trong kho; mọi bản đăng lên GitHub chỉ là bản chiếu.**
