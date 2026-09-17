# WP552 WINDOWS-T150-TRACEBACK-RO — spec r2 (packet revision 1 / generation 1)

> ĐẶC TẢ ĐÓNG BĂNG. KHÔNG phải lease, KHÔNG cấp việc.
>
> **`r2` thay `r1`** (`34aa11fabecf59cfe29734d0588f171d6f32b79379a0877786ee10bff884c8bf`, nhánh
> `claude/spec-552-r1-20260917`). `r1` khai `review_class: routine`; **cổng đăng lease BÁC** — xem
> §D7. Đổi đúng một thứ: lớp review và trần ADR-0044 đi kèm. Mục tiêu, write set, nghiệm thu,
> `ngoai_pham_vi` **không đổi**. `r1` giữ nguyên làm dấu vết, không sửa đè (§5 skill `soan-spec`).
>
> `revision`/`generation` của **packet** vẫn **1 / 1**: chưa lease nào từng cấp, và §3.2 chỉ buộc
> revision mới khi đổi objective / acceptance / write set / dependency / executor / environment —
> không thứ nào trong số đó đổi. `r1`→`r2` là revision của TỆP spec.
>
> **Đây là packet ĐO, không phải packet VÁ.** Sản phẩm là một biên bản đo có số, không phải một
> bản vá. Nguyên nhân gốc chưa xác định được từ Linux, và lượt soạn spec này đã **bác** giả thuyết
> gọn gàng nhất (xem `hien_trang_da_do` §D5). Vá lúc chưa biết nguyên nhân là vá theo phỏng đoán.
>
> Mọi con số kèm ĐƠN VỊ (L1) và THỜI ĐIỂM ĐO (L5).

## packet_id · packet_issue

| trường | giá trị |
|---|---|
| `packet_id` | `WP552-WINDOWS-T150-TRACEBACK-RO` |
| `packet_issue` | **552** (`open`, 0 comment, tạo 17-09-2026) |
| `revision` / `generation` | 1 / 1 |
| `mission_issue` | `KHONG_CO` |
| `base_sha` | `a612c70cbc56d0e3a8c580f4759eddf215af82fb` |
| `depends_on` | `[]` — **không phụ thuộc #541**, xem `write_set` |

## nguon_cap_viec

Issue **#552**, mở theo chỉ thị chủ kho (*"mở packet riêng cho t150"*), tách khỏi **#541** vì phép đo
cho thấy nguyên nhân khác. Issue #541 (thân issue, 15-09-2026) đã yêu cầu sẵn điều này:

> *"Preserve distinct case diagnoses, including t150, rather than declaring every failure solved by
> that hypothesis."*

Không có dòng kế hoạch nào cho packet này.

## review_class

| trường | giá trị | căn cứ |
|---|---|---|
| `risk` / `review_class` | **`sensitive`** | **ĐO, không suy** — xem §D7. Cổng đăng lease tự tính `sensitive` và **bác** bản nháp khai `routine` (`rc=10`). `r1` lập luận theo §8 rằng hai tệp MỚI không chạm authority nên là `routine`; lập luận ấy **đúng về văn bản §8 nhưng sai về cổng đang chạy**. Lease theo CỔNG. |
| `effective_review_class` | **`sensitive`** | Cổng đòi `effective_review_class` **bằng** lớp nó tính; lệch ⇒ `rc=10`, không đăng được. |
| `assurance_target` | **`human_audited`** | §8 cho `sensitive`: *"Phải có Codex `cross_approved` hoặc `human_audited`"*. Executor là `antigravity`, và *"antigravity"* xuất hiện **0** lần trong PROTOCOL (đo tại #548) nên chưa phải provider hợp lệ cho `cross_approved`. |
| `effective_review_class` | do dispatcher đặt | §8: *"dispatcher ghi `effective_review_class` bằng mức cao hơn giữa khai báo và classifier"*. **Executor không được hạ lớp.** Nếu classifier hoặc người giữ kho thấy script đo chạm bề mặt authority thì lớp lên theo họ, không tranh. |
| `environment` | **`local` (Windows)** | phép đo chỉ tồn tại trên Windows |
| `prohibited_actions` | `self_review`, `self_approve`, `merge` | §8 |

## write_set

Hai đường dẫn, đều là **tệp MỚI**:

1. `ops/do_t150_windows.py` — script đo, chạy trên Windows
2. `ops/DO_VI_SAO_T150_DO_TREN_WINDOWS_20260917.md` — biên bản đo (khuôn `ops/DO_VI_SAO_LEASE_482_483_CHET_20260909.md`)

**KHÔNG lấy `ops/lease_publish.py`. KHÔNG lấy `ops/lease_publish_test.py`.** Đây là quyết định thiết
kế, không phải sự trùng hợp: cả hai tệp ấy nằm trong vùng tranh chấp của #541/#548, và một packet ĐO
không cần quyền ghi lên thứ nó đang đo. Hệ quả: **#552 chạy SONG SONG #541, không xếp hàng sau.**

Trần ADR-0044 cho **`sensitive`**: **≤ 3 tệp** và **≤ 300 dòng thêm**. Write set này **2** tệp.
`r1` trích trần của `routine` (≤ 6 tệp, ≤ 1.000 dòng) — sai theo §D7, và **rộng hơn** mức thật. Đây
là chỗ duy nhất cái sai của `r1` nới lỏng chứ không siết: nó cho phép một packet tới 6 tệp trong khi
cổng chỉ cho 3. Write set 2 tệp nên kết luận không đổi, nhưng con số thì đổi.

### Trạng thái lease — đo 17:22:35Z 17-09-2026

| đường dẫn | rc | người giữ |
|---|---|---|
| `ops/do_t150_windows.py` | 0 | **0** — rảnh |
| `ops/DO_VI_SAO_T150_DO_TREN_WINDOWS_20260917.md` | 0 | **0** — rảnh |
| *(đối chiếu)* `ops/lease_publish.py` | 0 | 0 |
| *(đối chiếu)* `ops/lease_publish_test.py` | 11 | **1: `ci-windows-r2-g2-antigravity`**, hạn `2026-09-18T17:00:00Z` |

Chốt so hai nguồn ref chạy TRƯỚC (đo 17:21Z): máy chủ **422** tên nhánh, đệm cục bộ **422**,
`comm -23` **rỗng**.

> **Nền đo của lượt soạn spec này TỪNG SAI, và cổng bắt được — chép lại vì nó sẽ tái phát.**
> Lần quét đầu (17:20Z) `ai-dang-giu` trả **rc=12 KHÔNG_XÁC_ĐỊNH** cho MỌI đường, lý do
> *"`claude/spec-541-r1-20260917` có config upstream nhưng không giải được"*. Đồng thời `comm -23`
> cho **3** ref mù (`claude/review-548-luot4-20260917`, `claude/spec-548-r2-20260917`,
> `ops/cap-lease-548-r2`).
> Fetch đủ refspec chữa được cái mù, **nhưng rc=12 vẫn còn**. Nguyên nhân thật: clone dựng bằng
> `git clone --depth 1` nên `remote.origin.fetch` bị siết thành
> `+refs/heads/master:refs/remotes/origin/master`. Với refspec ấy, `git rev-parse '<nhánh>@{upstream}'`
> **thất bại** dù `refs/remotes/origin/<nhánh>` có thật và đúng SHA — và cổng đọc `%(upstream)` qua
> `for-each-ref` nên thấy rỗng rồi fail-close. Chữa bằng
> `git config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'`.
> Đây đúng bài học CLAUDE.md *"`--depth` kéo theo `--single-branch`, và thứ bị siết là REFSPEC"*, ở
> một mặt mà bài học ấy chưa ghi: nó không chỉ làm **thiếu ref**, nó còn làm **hỏng phép giải
> upstream của ref đã có**. Cổng đã làm đúng: từ chối trả lời thay vì đoán.

## hien_trang_da_do

### D1 — Ca nào, ở đâu

`t150_review2_F10_nguon_khong_utf8_la_12_khong_traceback`, `ops/lease_publish_test.py:5663`.
ĐỎ trên `windows-latest`, XANH trên `ubuntu-latest`.

Nguồn: log job `105238582317` (run `35232106589`, bước 18 `lease-publish selftest`), tải qua REST
lúc 17:00Z 17-09-2026 — **296 402** byte, **2 546** dòng. Metadata job: **đúng MỘT** bước đỏ.

Phân loại 15 ca đỏ bằng máy theo mẫu `PATH tối thiểu` / `/usr/bin`: **14 PATH · 1 KHÁC**. Ca KHÁC là
ca này. Hai dòng `!!! do` của nó **không chứa** `PATH tối thiểu`, **không chứa** `/usr/bin`.

### D2 — Vế nào của assertion trượt (suy diễn, không đoán)

```python
chot(rc == 12 and "Traceback" not in e, f"...: {rc} {e[-200:]!r}")
```

Thông điệp in `rc` = **12** ⇒ vế `rc == 12` ĐÚNG. Assertion vẫn trượt ⇒ **`"Traceback" in e` ĐÚNG**.
`rc` đã đúng; phần hỏng là **stderr có Traceback**.

### D3 — Traceback được viết TRONG TIẾN TRÌNH, không phải từ tiến trình con

`_goi_main` (`ops/lease_publish_test.py:4345`) chạy `main()` **in-process** với
`contextlib.redirect_stderr(io.StringIO())`. `GOI_GIT`/`GOI_GH` dùng `capture_output=True` nên
stderr của `git` bị nuốt vào `p.stderr`. **Tiến trình con không có đường ghi vào `e`.** Một hướng bị
loại hẳn.

`main()` (`:1930-1938`) chỉ bắt `Chan`; mọi ngoại lệ khác thoát ra sẽ cho traceback **và rc=1**. Mà
`rc=12` ⇒ ngoại lệ **không** thoát khỏi `main`. Hai điều đó chỉ đứng cạnh nhau được nếu có thứ gì đó
in "Traceback" vào `sys.stderr` mà **không** làm `main` sập. **Chưa biết thứ đó là gì.**

Dấu vết phụ, chưa kết luận: cửa sổ `e[-200:]` bắt đầu bằng `e` + xuống dòng rồi mới tới `CHAN [12]:`
⇒ có nội dung đứng TRƯỚC dòng `CHAN`, và nội dung ấy kết thúc bằng chữ cái `e`.

### D4 — Thông điệp đến từ nhánh nào

`ops/lease_publish.py:1641-1645`. Nhánh chỉ bắn khi
`noi_dung_p is None or _doc_policy_json(noi_dung_p) is None`.
`_doc_policy_json` (`:1648`) trả `None` **chỉ khi** `json.loads` ném **hoặc** kết quả không phải `dict`.
`_doc_blob_text_12` (`:1617`) trả `None` khi `p is None or p.returncode != 0`, và ném
`Chan(12, "… không phải UTF-8")` khi `GOI_GIT` ném `UnicodeDecodeError`.

Ca này đợi nhánh *"không phải UTF-8"* (`:1621`) nhưng nhận nhánh *"vắng hoặc không phải JSON object
(Q13)"* (`:1643`). **Hai nhánh cùng cho `rc=12`**, nên `rc` không phân biệt được chúng.

### D5 — KẾT QUẢ PHỦ ĐỊNH: codepage KHÔNG đủ làm nguyên nhân

Giả thuyết ban đầu (ghi trong Issue #552 mục "chưa đo" số 3): trên Windows `text=True` giải mã bằng
codepage nên không ném, lọt qua `:1621`, rồi hỏng ở JSON. Đo thẳng bộ byte mà ca này ghi ra
`.github/coordination/change-impact.v1.json` là `b'{"a": "\xc3("}'` (đo 17:1xZ 17-09-2026):

| bộ mã | kết quả |
|---|---|
| `utf-8` | **NÉM** `UnicodeDecodeError` ⇒ Linux đi nhánh `:1621`, khớp ca XANH |
| `cp1258` | KHÔNG ném → `'{"a": "Ă("}'` → `json.loads` **QUA**, là `dict` |
| `cp1252` | KHÔNG ném → `'{"a": "Ã("}'` → `json.loads` **QUA**, là `dict` |

Giả thuyết codepage **dự đoán `_doc_policy_json` trả `dict`** ⇒ nhánh Q13 **KHÔNG** bắn. Mà nó đã
bắn. **Giả thuyết bị bác với tư cách nguyên nhân duy nhất.**

Chỗ còn lại theo D4: trên Windows `_doc_blob_text_12` nhiều khả năng trả **`None`**, tức
`GOI_GIT("cat-file","blob", …)` cho `rc ≠ 0`. **Chưa đo.** Đây là câu hỏi thật của packet.

Ghi kết quả phủ định này ra spec vì kho có luật riêng cho nó: *"ghi một nguyên nhân sai vào doctrine
còn tệ hơn không ghi gì"*. Issue #552 cần được đính chính theo mục này.

### D6 — Đối chứng Linux

Đo 17:2xZ 17-09-2026 trên `a612c70cbc56`, `ubuntu-latest`: `ops/lease_publish_test.py` ⇒
`152/155 đạt; đã chạy=155, bỏ qua=0`. Ba ca đỏ đều là `KHÔNG ĐO ĐƯỢC: thiếu actionlint` (fail-close
vì thiếu công cụ) — **không có `t150`** ⇒ hỏng **chỉ trên Windows**.

Khoá luôn một con số từng treo ở spec `#541 r2`: Windows khai `đã chạy=148, bỏ qua=7`; Linux khai
tổng **155**. **148 + 7 = 155** — khớp. Con số `150` từng nêu là do `grep '^def t[0-9]+_'` đếm hụt
**5** ca; số của chính bộ chạy mới đúng.

### D7 — Cổng đăng lease BÁC lớp `routine`, và classifier trả `sensitive` cho MỌI đầu vào

Đo 17:3xZ 17-09-2026, khi soạn bản nháp lease cho packet này.

Bản nháp khai `review_class: routine` theo lập luận của `r1`. `ops/lease_publish.py check` trả:

```
CHAN [10]: effective_review_class='routine' không bằng lớp cổng tính được 'sensitive'
           cho role='executor'
```

Gọi thẳng `_tinh_lop_tu_write_set` (`ops/lease_publish.py:140`) trên năm write set:

| write set thử | lớp cổng tính |
|---|---|
| hai tệp của packet này | `sensitive` |
| **một tệp docs thuần** (`docs/README.md`) | `sensitive` |
| `ops/lease_publish.py` (có trong bảng) | `sensitive` |
| `.github/workflows/ci.yml` (có trong bảng) | `sensitive` |
| `scripts/tl.py` (KHÔNG có trong bảng) | `sensitive` |

Nguyên nhân đọc được từ mã: `_BANG_LOP` (`:59`) có **7** mục (đơn vị: cặp `(tiền tố, lớp)`), và
**cả 7 đều mang giá trị `sensitive`**; phép tra dùng `next(…, "sensitive")` nên tiền tố **không có
trong bảng cũng thành `sensitive`**. Giá trị khởi tạo `ket_qua = "routine"` trong hàm vì thế
**không bao giờ tới được**.

**Hệ quả:** với `role='executor'`, không lease nào trong kho này xuống dưới `sensitive` được, dù §8
mô tả ba tầng `routine`/`systemic`/`sensitive`. Lớp khai của packet chỉ còn tác dụng **nâng lên**,
không bao giờ hạ xuống.

**KHÔNG kết luận đây là khuyết tật.** Nó có thể là fail-close cố ý (bảng liệt kê đúng những đường
nguy hiểm, mọi thứ khác coi như chưa phân loại nên phải chặt nhất), cũng có thể là bảng chưa điền
xong. Phân biệt được hai khả năng ấy cần đọc ý định của người viết, và việc đó **ngoài phạm vi
packet này**. Ghi ra đây để lượt sau không phải phát hiện lại, và để ai đọc §8 rồi khai `routine`
biết trước rằng cổng sẽ bác.

Bản nháp sau khi sửa thành `sensitive`: `check` **rc=0** —
*"lease `t150-do-r1-g1-antigravity` ĐĂNG ĐƯỢC — issue #552, neo `a612c70cbc56`, hết hạn
`2026-09-18T18:00:00Z`, prompt `ops/specs/wp552-t150-traceback-ro-r1.md` khớp băm `34aa11fabecf`"*.

> Băm ấy là của **`r1`**. Bản nháp lease hiện neo `r1`; khi dùng `r2` thì `spec_path`,
> `prompt_path`, `spec_hash`, `prompt_sha256_required`, `spec_bytes` và `spec_ref` phải đổi theo,
> rồi chạy lại `check`. **Không đổi thì lease neo vào một đặc tả đã bị thay.**

`kiem-github` trả **`rc=8 KHÔNG ĐO ĐƯỢC`**: container soạn spec không có `gh`, và chính cổng nói
*"số hiệu trỏ vào PR là một nguyên nhân có thể — đây là phỏng đoán, không phải phép đo"*. Hai điều
nó kiểm đã được đo bằng **đường REST độc lập**: #552 là **ISSUE** (không có khoá `pull_request`), và
**chưa** comment nào mang `lease_id` `t150-do-r1-g1-antigravity` (issue có 1 comment, là bản đính
chính D5). Lớp ấy vẫn sẽ chạy thật trong CI khi đăng.


## muc_tieu

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M1** | Script đo chạy trên Windows: dựng lại fixture của `t150` khối (a) — kho tạm, nhánh `meta-pol-hong`, marker `ops/thu-hoi/_ngoai-le-closure.retired.yaml`, policy `b'{"a": "\xc3("}'` — rồi gọi `ai-dang-giu` qua CÙNG đường `_goi_main` dùng (in-process, `redirect_stderr`), và in **TRỌN** `e` (không cắt `[-200:]`), `rc`, cùng `rc`+`stdout`+`stderr` của TỪNG lời gọi `git` bên trong. Ba trạng thái, fail-close. | `ops/do_t150_windows.py` |
| **M2** | Biên bản đo: chép nguyên văn đầu ra của M1, trả lời DỨT KHOÁT bốn câu ở `nghiem_thu`, và với câu nào không trả lời được thì ghi `KHÔNG ĐO ĐƯỢC` kèm lý do — không suy, không làm tròn. | `ops/DO_VI_SAO_T150_DO_TREN_WINDOWS_20260917.md` |

**M1 KHÔNG được sửa `ops/lease_publish.py` hay `ops/lease_publish_test.py`** để lấy số — kể cả tạm.
Hai tệp ấy ngoài write set; muốn in trọn `e` thì script tự gọi `main()` của module đã nạp, đúng cách
`_goi_main` làm, chứ không vá chỗ cắt chuỗi trong tệp test.

## nghiem_thu

Packet ĐO nghiệm thu bằng **câu trả lời có số**, không bằng mã xanh. Mỗi câu nêu cái làm nó ĐỎ.

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| **N1** | Biên bản trả lời: **chuỗi `"Traceback"` trong `e` đến từ đâu** — dán trọn `e`, chỉ ra dòng đầu của khối traceback và loại ngoại lệ. | Biên bản chỉ nói "có Traceback" mà không dán trọn `e` ⇒ ĐỎ. Đoán nguồn mà không có đầu ra kèm theo ⇒ ĐỎ. |
| **N2** | Biên bản trả lời: **`GOI_GIT("cat-file","blob", …)` trả `rc` bao nhiêu** trên Windows, và `p.stdout`/`p.stderr` là gì. Nếu `rc≠0` thì vì sao. | Không có con số `rc` cho chính lời gọi ấy ⇒ ĐỎ. |
| **N3** | Biên bản phán quyết **D5 đúng hay sai trên Windows thật**: `text=True` ở `GOI_GIT` có ném `UnicodeDecodeError` hay không, và `locale.getpreferredencoding(False)` trên máy đo là gì. | Không nêu bộ mã thật của máy đo ⇒ ĐỎ. Kết luận "do codepage" mà không kèm phép đo ⇒ ĐỎ, vì D5 đã bác nó trên lý thuyết. |
| **N4** | Biên bản trả lời: **khối (b)** của `t150` (*"tên tệp trong sổ không phải UTF-8"*) trên Windows ĐẠT hay TRƯỢT, hay **chưa từng chạy** vì `chot` khối (a) trượt trước. | Bỏ trống ⇒ ĐỎ. |
| **N5** | Fail-close của chính script: nền đo sai (`sys.platform != "win32"`, hoặc `git` không gọi được) ⇒ in `KHÔNG_ĐO_ĐƯỢC`, `rc ≠ 0`, và **không** in một kết luận nào. | Chạy script trên Linux mà nó vẫn in kết luận ⇒ ĐỎ. Đây là ca tự kiểm bắt buộc, chạy được ở đâu cũng được. |
| **N6** | `git diff --numstat` so `a612c70cbc56`: đúng **2** tệp, cả hai là tệp MỚI, không tệp nào thuộc `ops/lease_publish*.py`. | Chạm tệp thứ ba, hoặc chạm hai tệp ấy ⇒ DỪNG, handoff. |

**Packet này KHÔNG có tiêu chí "gate xanh".** Nó không sửa mã sản phẩm, nên không cổng nào đổi màu vì
nó. Đặt một tiêu chí như thế là đặt tiêu chí không đo được điều gì.

## ngoai_pham_vi

| # | cố ý KHÔNG làm | lý do |
|---|---|---|
| 1 | **Không vá `t150`** | nguyên nhân chưa biết; D5 vừa bác giả thuyết gọn nhất. Vá là packet SAU, spec riêng, neo vào số của biên bản này. |
| 2 | Không chạm `ops/lease_publish.py`, `ops/lease_publish_test.py` | vùng tranh chấp #541/#548; và packet ĐO không cần quyền ghi lên thứ nó đo |
| 3 | Không gộp với **#417** (*"`lease_publish.py:74` giải mã bằng codepage ANSI"*) | cùng tệp, cùng họ, nhưng **D5 vừa cho thấy codepage không giải thích được `t150`**. Gộp bây giờ là buộc hai khuyết tật vào một nguyên nhân mà số đo đã bác. Sau khi có N3 thì quyết. |
| 4 | Không chạy CI Windows bằng tay | `manual_ci_budget: 0` |
| 5 | Không đụng 14 ca PATH | thuộc #541 |

## hinh_dang_ke_thua

`khong_ap_dung` — #552 không phải packet khắc phục của packet nào; nó là **anh em tách ra** từ #541
sau một phép đo, không phải hậu quả của một lượt thi công bị bác.

Hai doctrine ĐANG áp:

- *"Ghi một nguyên nhân sai vào doctrine còn tệ hơn không ghi gì"* — vì sao D5 (kết quả phủ định)
  được ghi thành mục riêng thay vì lặng lẽ bỏ giả thuyết.
- *"Nghĩ ra được phép thử mà KHÔNG CHẠY nó thì phép thử ấy KHÔNG TỒN TẠI"* — vì sao N5 (fail-close
  của chính script) là tiêu chí, không phải lời hứa trong docstring.

## chua_do_duoc

1. **Traceback sinh ở đâu.** Chỉ biết nó CÓ trong `e` (D2) và được viết in-process (D3). Nội dung nằm
   ngoài cửa sổ 200 ký tự mà assertion in. Đây là N1.
2. **`rc` của `git cat-file blob` trên Windows.** D4 suy ra `_doc_blob_text_12` nhiều khả năng trả
   `None`, nhưng chưa ai đo. Đây là N2.
3. **`locale.getpreferredencoding(False)` trên runner `windows-latest`.** Không đo được từ đây; máy
   Windows của chủ kho là máy KHÁC, cấu hình KHÁC — nó trả lời cho máy ấy, không cho runner.
4. **Khối (b) của `t150`.** Đây là N4.
5. **Quan hệ thật với #417.** Đây là N3 + quyết định sau đó.
6. **`_BANG_LOP` trả `sensitive` cho mọi đầu vào là CỐ Ý hay THIẾU SÓT.** §D7 đo được HÀNH VI; ý
   định của người viết thì không đo được từ đây. Ngoài phạm vi packet này — nếu muốn theo đuổi thì
   mở nợ riêng, đừng sửa kèm.

## Ràng buộc thi công

- **KHÔNG chạy CI Windows bằng tay** (`manual_ci_budget: 0`). Đường đo là máy Windows của chủ kho.
- **KHÔNG tự merge, tự approve, tự review.**
- **KHÔNG chạm tệp ngoài `write_set`**, kể cả sửa tạm rồi hoàn nguyên.
- **KHÔNG viết dấu bỏ-qua-CI nguyên văn trong thông điệp commit**, kể cả khi trích dẫn.
- **Đọc `rc` TRỰC TIẾP**, đừng qua pipe.
- **Quét lại `ai-dang-giu` cả hai đường ngay trước khi cấp lease**, kèm chốt `comm -23` rỗng. Và
  kiểm `remote.origin.fetch` là `+refs/heads/*:refs/remotes/origin/*` TRƯỚC khi tin kết quả quét —
  xem hộp cảnh báo ở `write_set`.
