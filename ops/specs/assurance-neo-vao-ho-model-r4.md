# ĐẶC TẢ PACKET — `ASSURANCE-NEO-VAO-HO-MODEL` revision 4

| | |
|---|---|
| `packet_id` | `ASSURANCE-NEO-VAO-HO-MODEL` |
| `packet_issue` | **#551** |
| `revision` / `generation` | **4** / 4 |
| `thay_the_cho` | **revision 3** (`sha256 fbe599fb21dcb567e8028b0142f6391fecbaa50002e6914a6aa0a76f3e53737c`, 14 361 B) — r3 **giữ nguyên trên đĩa** làm hồ sơ |
| `review_class` | **`sensitive`** (KHÔNG đổi — xem `Đ4`) |
| `base_sha` | **`2aaf49f402ccfdaa8d6d608e3a5482ed54dc6e1b`** (`origin/master`, đo `18:2xZ 18-09-2026`) |
| `start_from_sha` | **`6bcf26637ca94fd29039665e34b3f07732b57490`** — bản vá r3/g3 của agy ĐÃ CÓ, không bỏ |
| `executor` | **`claude`** ← ĐỔI (r3: `antigravity`) |
| `reviewer` | **KHÔNG CÓ provider khác họ model** — xem `Đ2` |
| `assurance_target` | **`human_audited`** ← ĐỔI (r3: `cross_approved` có điều kiện) |

## `nguon_cap_viec`

Chỉ thị chủ kho, phiên điều phối `18-09-2026` `~18:20Z`, **nguyên văn**:

> agy đã hết quota, hãy rà soát, scan xem agy đã vá #551 tới đâu và kế thừa từ đây. Hãy chuyển thành
> executor và vá nốt từ đây.

và, cùng phiên:

> Không chạy CI, full CI cho đến khi merge

Hai quyết định bổ sung của chủ kho, hỏi và trả lời trong cùng phiên (ghi vì chúng đổi `assurance_target`
và mở `S1`/`S2` cho r4):

1. **Mức assurance** → *"`human_audited` — anh tự audit khi land"*.
2. **`S1`/`S2`** → *"r4 xử luôn cả `S1` và `S2`"*.

Mỏ neo bền: bản chiếu chỉ thị tại
[#551 comment `5734378960`](https://github.com/ducthangho/tra-luat/issues/551#issuecomment-5734378960).

Nợ gốc **`PROTOCOL-CHUA-BIET-ANTIGRAVITY`** không đổi; r4 **không** đổi mục tiêu của packet.

## VÌ SAO PHẢI CÓ REVISION 4 — §3.2, bốn căn cứ

### `Đ1` — đổi `executor`, đúng trường §3.2 nêu đích danh

§3.2: *"Đổi objective, acceptance, write set, dependency, **executor** hoặc environment tạo revision
mới và làm lease cũ mất hiệu lực."* Lease `assurance-ho-model-r3-g3-antigravity` khai
`executor: antigravity` và **CÒN_HẠN** tới `2026-09-19T10:30:00Z` — giữ nó mà để `claude` thi công là
tạo đúng cửa sổ hai writer mà write-set exclusion sinh ra để chặn. Bia mộ **HAI CHIỀU**
(`thay_the_cho` ở gen 4 **và** `da_bi_thay_the` ở gen 3 — chốt `_kiem_bia_mo` đòi cả hai).

### `Đ2` — `assurance_target` phải HẠ, vì không còn provider khác họ model

`cross_approved` đòi hai họ model độc lập. Đo được tại `18:2xZ 18-09-2026`:

| provider | trạng thái |
|---|---|
| `codex` | hết quota review — `chatgpt-codex-connector[bot]` đăng `16:41Z` trên #563: *"You have reached your Codex usage limits for code reviews."* Và `launcher.py doctor`: `SAP_HET_HAN`, ảnh chụp cũ 218,5h |
| `antigravity` (agy) | hết quota — chỉ thị chủ kho ở trên |
| `claude` | **là executor của r4** ⇒ không thể đồng thời là reviewer khác họ |

Nên `cross_approved` **KHÔNG ĐẠT ĐƯỢC**, không phải "chưa đo được". §8 cho `sensitive` còn đúng một
đường: **`human_audited`**. Chủ kho đã chọn đường ấy (quyết định 1 ở trên).

**Hệ quả phải khai thẳng:** packet này **không land được** bằng máy. Bước land đòi chủ kho đọc verdict
và diff rồi xác nhận. Không có phép đo nào của executor thay được chữ ký ấy.

### `Đ3` — verdict lượt 3 ra `changes_requested`, và `nghiem_thu` r3 không có tiêu chí nào đóng được

Verdict lượt 3 (`sha256 935a0c3792c5221eba24455188ecd0b873718c6c8e72134031269b8bd6f54dc0`, 9 705 B,
neo `6bcf2663`) mở **0 P1 · 1 P2 · 2 P3**. `A13`–`A15` của r3 đều **ĐẠT** trên `6bcf2663` mà ba lớp ấy
vẫn còn. Đúng ca §3.2 gọi tên: *"finding cho thấy chính spec thiếu thì verdict là `blocked` và đi qua
revision mới"*.

### `Đ4` — `review_class` GIỮ `sensitive`, và đây là quyết định CÓ CHỦ Ý

Packet sửa **chính cổng đọc luật assurance** (`ops/bien_nhan_v2.py`). Hạ lớp review ở đúng packet ấy là
tự nới luật cho mình. Giữ `sensitive` nghĩa là chấp nhận `Đ2` — phải có audit người.

## `write_set` — SÁU đường, KHÔNG ĐỔI so r3

```
docs/PROTOCOL_DA_PHIEN.md
ops/bien_nhan_v2.py
ops/bien_nhan_v2_test.py
docs/adr/0050-assurance-neo-vao-ho-model-khong-phai-hang-cong-cu.md
scripts/tl_selftest.py
RELEASE_MANIFEST.json
```

Cả ba lớp còn mở của verdict lượt 3 chiếu vào **hai** đường đầu (`ops/bien_nhan_v2.py`,
`ops/bien_nhan_v2_test.py`) cộng ADR — **không đường nào mới**. Ngoại lệ ADR-0044
(`ai_nang: ducthangho`, `tran_moi: 6 tệp`, `tran_dong_them: 250`) **mang sang nguyên hiệu lực**, cùng
căn cứ và cùng tập đường; ngoại lệ §5 (`docs/PROTOCOL_DA_PHIEN.md` · `scripts/tl_selftest.py` giao với
packet khác) cũng mang sang.

### `RUI_RO_TRAN_DONG` — khai TRƯỚC

`6bcf2663` đã dùng **223 / 250** dòng thêm so nền (đo lại ở `A9`). Ba lớp còn lại cần: một chốt trong
`_giai_ho_va_bc` · hai ca test + hai đột biến · hai mục khai trong ADR-0050 · sửa lời `A14`. Ước lượng
**35–60** dòng ⇒ tổng **258–283**.

**Gần như CHẮC CHẮN vượt 250.** Khác r3 ở chỗ r3 nói *"có thể vượt"*; r4 nói **sẽ vượt**, nên xin ngay
tại đây thay vì đụng trần rồi mới kêu:

> **Xin nới trần dòng thêm từ 250 lên 300.** Căn cứ: `ADR-0044:5` đặt trần `sensitive` ở **≤ 3 tệp và
> ≤ 300 dòng thêm**; ngoại lệ đã cấp cho packet này nới **số TỆP** lên 6 nhưng lại ghi `tran_dong_them:
> 250`, **chặt hơn** chính ADR. Nới lên 300 là **về đúng trần ADR**, không phải vượt nó.
> Vượt **300** thì DỪNG và xin lại. **Không** gộp chốt để lách trần — gộp là tạo bộ tương đương, đúng
> thứ `M14` cấm.

## `ngoai_pham_vi` — cố ý KHÔNG làm (kế thừa r3, thêm hai mục)

| thứ | vì sao |
|---|---|
| Nới `same_provider_approved` cho `sensitive` | §8 có dòng cứng; bất biến an toàn |
| Đảo `ASSURANCE_CAM_THEO_PROVIDER` sang CHO PHÉP | nợ `DANH-SACH-CAM-THEO-PROVIDER-CHUA-DAO` |
| Nối `bien_nhan_v2` vào CI làm cổng chặn | nợ `CONG-BIEN-NHAN-KHONG-CHAY-TRONG-CI` |
| Đọc lại verdict đã giao của #546/#538/#540 | luật mới **KHÔNG hồi tố** |
| Đóng nợ `R291-DAM-SO-CUNG` | hình dạng ở mức BA, cần packet riêng |
| Vá `m46` / bộ phân hạng đột biến | nợ `PHAN-HANG-DOT-BIEN-PHU-THUOC-MOI-TRUONG` — khác packet |
| *(mới)* Bỏ hẳn `d` khỏi phạm vi tra của vai reviewer | `P3-2` đo được **0/50** biên nhận bị ảnh hưởng ⇒ đổi hành vi là rủi ro **không mua được gì**. r4 chọn **KHAI**, không chọn đổi |
| *(mới)* Đòi khoá audit riêng cho vai executor | `P3-1` — r4 chọn **KHAI** hành vi hiện có, không đổi nó. Đổi là siết một thứ chưa ai đo là có hại |

## `muc_tieu`

`M1`–`M15` **ĐÃ THI CÔNG** ở `f4684e45` + `d8ef235` + `6bcf2663` và **GIỮ NGUYÊN**; r4 không làm lại.
`M16` **RÚT** (xem `M20`). Năm mục mới:

| # | mục tiêu | đóng lớp | chiếu vào |
|---|---|---|---|
| **M17** | Trong khối `model_<vai>_identity`, tra khoá **KHÔNG tiền tố** cho **cả hai** vai (`model_family` · `ho_model` · `canonical_model` · `model`, và `model_evidence` · `bang_chung_model`). Tiền tố `executor_` **chỉ** còn áp khi tra ở mức top-level `d`. Hết bất đối xứng giữa hai khối | `P2` | `ops/bien_nhan_v2.py` |
| **M18** | ADR-0050 **khai thẳng**: một trường audit **không tiền tố** ở top-level (`nguoi_audit` / `audit_actor`) bảo chứng cho **CẢ HAI** vai. Đây là chủ ý — một biên nhận, một người audit — chứ không phải sơ hở | `P3-1` | `docs/adr/0050-…md` |
| **M19** | ADR-0050 **khai thẳng**: khoá `model` / `ho_model` / `model_family` / `canonical_model` ở **top-level** tính là **khai đè của vai reviewer**, nên kéo theo đòi `model_evidence`. Kèm con số đo được: **0/50** biên nhận `cross_approved` hiện có khoá ấy | `P3-2` | `docs/adr/0050-…md` |
| **M20** | **Rút `M16` và `A16`** — và rút CÓ LÝ DO ghi lại, không xoá lặng. `M16` sinh ra để gắn điều kiện cho `cross_approved`; `Đ2` đã bỏ `cross_approved` khỏi packet này ⇒ `M16` **mất đối tượng**. Đây là cách `S1` được đóng: không phải "đã làm được", mà **"tiêu chí ấy không còn áp"** | `S1` | đặc tả (mục này) |
| **M21** | **Sửa lời `A14`**: *"RỖNG ⇒ CHẶN"* là **RỘNG HƠN mã**, và chính chỗ rộng ấy đẻ ra `S2`. Mã chỉ chặn RỖNG **khi có khai đè** (`ov and not bc`). `A14` của r4 nói đúng điều mã làm ⇒ `A14` và `A3` **hết loại trừ nhau** | `S2` | đặc tả (mục này) |

### `M20`/`M21` — vì sao đây là cách đóng ĐÚNG, không phải cách đóng TIỆN

`S1` và `S2` được verdict lượt 2 xếp là **khuyết tật của đặc tả**. Một khuyết tật của đặc tả **không**
đóng được bằng mã; nó đóng bằng sửa đặc tả. `M20` rút một tiêu chí đã mất đối tượng; `M21` sửa một câu
khai rộng hơn phép đo — đúng lớp lỗi mà `CLAUDE.md` gọi là *"lời khai rộng hơn phép đo"*.

**`S2` đã được ĐO trước khi viết mục này**, không suy từ đọc mã. Fixture là biên nhận THẬT
`ops/reviews/r356-fixture-phu-thuoc-nen-review-2-codex-verdict.receipt.yaml` (`cross_approved`,
`model_evidence` là `None`):

```
(a) NGUYEN BAN                               -> QUA    <- DOI CHUNG, biet truoc dap an
(b) them khai de model reviewer, bc VAN RONG -> CHAN
(c) khoa `model` o TOP-LEVEL                 -> CHAN    <- P3-2
(d) model_executor_identity {model: ...}     -> QUA     <- P2: khoa bi BO QUA
(e) model_executor_identity {executor_model} -> CHAN     <- nhan doi tien to thi moi an
```

Ca (a) QUA là bằng chứng dương cho `S2`: biên nhận `cross_approved` có mức bằng chứng **RỖNG** mà
**KHÔNG bị chặn**, vì nó không khai đè. Nên `A3` (delta 0) và `A14` **chưa bao giờ** thật sự loại trừ
nhau — chỉ **câu chữ** của `A14` làm ta tưởng thế.

### Một giả thuyết đã bị phép đo BÁC — ghi lại kẻo lần sau lại nghĩ thế

Lượt soạn r4 đã nghi `P2` thật ra là **P1 fail-open**: nếu khoá `{model: …}` bị bỏ qua thì gate rơi về
bảng mặc định theo provider, và `agy` khai `claude-opus-4-6-thinking` sẽ được tính là `gemini` ⇒
`cross_approved` đội lốt. Đo thẳng ca ấy (reviewer họ `claude`, `executor_provider: google_antigravity`):

```
(1) agy KHONG khai model                          rev=claude exec=<RONG> -> CHAN
(2) agy khai executor_model: claude-*             rev=claude exec=claude -> CHAN
(3) agy khai model_executor_identity{model: claude-*}  rev=claude exec=<RONG> -> CHAN
```

**Cả ba CHẶN** — vì `M11` đã bỏ `google_antigravity` khỏi bảng mặc định. Giả thuyết **sai**; `P2` đúng
là fail-**closed** như verdict lượt 3 xếp. Ghi vào đặc tả vì một giả thuyết nghe hợp lý mà không đo thì
lần sau sẽ được nghĩ lại y hệt.

## `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ

`A1`, `A2`, `A4`, `A5`, `A6`, `A8`, `A10`, `A11` **giữ NGUYÊN VĂN r3/r2/r1**. `A13`, `A15` giữ nguyên.
`A16` **RÚT** (`M20`). `A3`, `A7`, `A9`, `A12` nêu lại theo nền mới. `A14` **sửa lời** (`M21`). Ba tiêu
chí MỚI:

| # | tiêu chí | ĐỎ khi |
|---|---|---|
| **A3** *(nền mới)* | `ops/bien_nhan_v2.py` trên **NỀN** `2aaf49f4` **và** trên ỨNG VIÊN: `0 vi phạm` **và** `0 KHÔNG ĐO ĐƯỢC` ở cả hai, `TỔNG: ĐẠT` cả hai, số `ĐẠT v2`/`tổng` **KHÔNG ĐỔI** giữa hai vế | luật mới từ chối một biên nhận cũ ⇒ hai vế lệch |
| **A7** *(nền mới)* | `adr-song --root .` ⇒ **rc=0**, số ADR = **(nền + 1)**, khớp 1–1 §20. Đo nền NGAY TRƯỚC ứng viên | quên dòng §20 ⇒ `rc=9` |
| **A9** *(nền mới)* | `numstat` vs `base_sha` `2aaf49f4`: **đúng 6 tệp**, **≤ 300 dòng thêm** (trần đã xin ở `RUI_RO_TRAN_DONG`) | tệp thứ bảy, hoặc vượt 300 ⇒ DỪNG, xin |
| **A12** *(nền mới)* | `release-verify … --strict --json` ⇒ `ok=true`, **`expected_file_count` == `checked_file_count` == 180**, `errors=0` | quên tái sinh manifest |
| **A14** *(SỬA LỜI — `M21`)* | Năm ca mức bằng chứng, **tất cả đều kèm khai đè**: `do_may` **không có** `model_evidence_ref` ⇒ CHẶN · `khai_co_audit` thiếu người audit ⇒ CHẶN · `khong_do_duoc` ⇒ CHẶN · RỖNG ⇒ CHẶN · chuỗi **BỊA ĐẶT** ⇒ CHẶN. **Cộng một ca đối chứng: KHÔNG khai đè + bằng chứng RỖNG ⇒ QUA** | bất kỳ ca nào QUA; **hoặc ca đối chứng CHẶN** — ca ấy CHẶN nghĩa là `A3` sắp vỡ |
| **A17** *(MỚI — `M17`)* | `model_executor_identity: {model: …}` ⇒ **nhận diện được** họ model executor (không còn RỖNG). `model_reviewer_identity: {model: …}` **vẫn** nhận diện được. Hai khối **đối xứng** | một trong hai khối cho RỖNG với cùng cách viết |
| **A18** *(MỚI — `M17`+`M14`)* | Một đột biến **gỡ đúng chốt `M17`** (trả `pre` về áp cho cả `sub`) làm **đúng ca `A17` ĐỎ**, phân hạng **`giet_that`**, không `tin_dung_gia` | đột biến không giết ca nào ⇒ chốt không răng; `tin_dung_gia` ⇒ tín dụng giả |
| **A19** *(MỚI — `M18`+`M19`)* | ADR-0050 có **hai mục riêng**, mỗi mục nêu **hành vi đo được** kèm ca đo: (a) trường audit top-level bảo chứng cả hai vai; (b) khoá model top-level tính là khai đè của reviewer, **0/50** biên nhận hiện có bị chạm. `doc-claims-check --strict` ⇒ rc=0 | thiếu một trong hai mục; hoặc mục viết mà không nêu ca đo |

### Nền đo tại lúc đóng băng — `18:2xZ 18-09-2026`, trên `2aaf49f402cc`

```
bien_nhan_v2 : 131 ĐẠT v2 · 11/11 miễn trừ legacy · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 184
adr-song     : sạch — 49 ADR trên đĩa, 49 dòng §20, khớp 1–1
docs/**/*.md : 74
RELEASE_MANIFEST.json file_count : 180
```

**Mọi con số trên là NỀN, không phải tiêu chí.** `A3` và `A7` so **DELTA** với nền **đo lại**, đúng
`L5`. Nhắc riêng: nền `bien_nhan_v2` đã đi `125/178` (lúc đóng băng r3, ba giờ trước) → `131/184` chỉ
vì sáu PR hồ sơ land — đúng thứ `L5` cảnh báo.

## `hinh_dang_ke_thua`

| hình dạng | đếm | nguồn |
|---|---:|---|
| `TIEU-CHI-THEO-GIA-TRI-TUYET-DOI` | **3** | #522 · #548 · #551 `A7` của r1 |
| `R291-DAM-SO-CUNG` | **3** | #522 · #548 · #551 |
| `TIEU-CHI-NEU-TRUONG-CHUA-AI-DO` | **1** | #548 `A7` của r2 |
| `DANH-SACH-CAM-KHONG-DAO-SANG-CHO-PHEP` | **3** | `v1.36.68` (PR #104) · `doctrine-scan` · #551 `P1-3` của r2 |
| `FAIL-OPEN-KHI-THIEU-DU-KIEN` | **3** | `P1-1` · `P1-3` · `P2-1` — đã đảo sang fail-close ở `M10`–`M14`, **không tăng ở r4** |
| **`LOI-KHAI-RONG-HON-PHEP-DO`** | **2** | `S2` (`A14` r3 nói *"RỖNG ⇒ CHẶN"* rộng hơn mã) · lượt soạn r4 nghi `P2` là fail-open rồi bị phép đo bác |
| **`TIEU-CHI-MAT-DOI-TUONG-MA-KHONG-AI-RUT`** | **1** | `S1` (`M16`/`A16` treo trên một hiện vật chưa từng tồn tại) |

**`LOI-KHAI-RONG-HON-PHEP-DO` mới ở mức HAI** — chưa chạm chốt "lần thứ BA thì hỏi có nên làm không",
nhưng ghi vào đây để packet sau kế thừa đúng bộ đếm (`L4`).

## `chua_do_duoc` — ghi thẳng

| # | thứ | vì sao |
|---|---|---|
| **C1** | Packet có gỡ được trần cho #546 không | **KHÔNG BIẾT, nghiêng về KHÔNG** — giữ nguyên văn r1/r2/r3 |
| **C2** | Model nào agy đã chạy ở #546/#538/#540 | không có bằng chứng máy; nợ `AGY-CHUA-ATTEST-MODEL-TUNG-LUOT` |
| **C3** | Có biên nhận cũ nào bị luật mới từ chối không | `A3` là phép đo **tổng**, không phải phép đo từng cái |
| **C4** *(viết lại)* | Họ model thật của `agy` ở lượt sinh `6bcf2663` | **KHÔNG ĐO ĐƯỢC, và nay KHÔNG CÒN CẦN** — `Đ2` đã bỏ `cross_approved`, nên tính chính đáng của packet không còn treo vào con số ấy. Nợ `AGY-CHUA-ATTEST-MODEL-TUNG-LUOT` vẫn mở cho packet khác |
| **C5** *(viết lại)* | Trần 300 dòng có đủ không | ước lượng **258–283**. Sát trần. Vượt ⇒ DỪNG |
| **C6** | `M8` có phải lần cuối phải kê khai slot không | phụ thuộc nợ `R291-DAM-SO-CUNG` |
| **C7** *(viết lại)* | Reviewer có độc lập với đặc tả này không | **KHÔNG CÓ REVIEWER MÁY.** `Đ2`. Phiên này vừa soạn r4 vừa thi công ⇒ **tự chấm bài mình ra đề ở CẢ HAI vế**. Đây là lý do `human_audited` là bắt buộc chứ không phải thủ tục |
| **C8** | Trần vòng review còn bao nhiêu | `ADR-0048` nâng trục VÒNG lên **10**; packet ở **lượt 4**. Không chạm trần |
| **C9** *(mới)* | Lượt CI trên head cuối | **KHÔNG DÙNG PHƯƠNG TIỆN** — chủ kho: *"Không chạy CI, full CI cho đến khi merge"*. Cổng chạy **tại chỗ**; `gate` chỉ bắn ở bước merge. Đây là **chọn không đo**, không phải "đã đo và xanh" |

## Băm để lease neo vào

```
sha256sum ops/specs/assurance-neo-vao-ho-model-r4.md
```
