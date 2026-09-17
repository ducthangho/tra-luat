# ĐẶC TẢ PACKET — `CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND` **revision 2**

**Mọi con số trong tệp này đo lúc `16:46Z 17-09-2026`** trên `origin/master` `a612c70cbc56` và head
`6d46e6fc16ca`, trừ chỗ ghi thời điểm khác. Luật L5: **đo lại trước mỗi bước công bố** (đóng băng,
cấp lease, merge) — đừng chép lại số ở đây.

| | |
|---|---|
| `packet_id` | `CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND` |
| `packet_issue` | #548 · PR #550 |
| `revision` | **2** — `thay_the_cho`: revision 1 (`sha256 56cb4bdc07052e7653aad41fb91b5c0f2291e748f553a83ce60d05f0f516e7e1`) |
| `generation` dự kiến | **2** (lease gen 1 mất hiệu lực theo §3.2) |
| `executor` · `reviewer` | `antigravity` · `claude` |
| `review_class` | **`sensitive`** — không đổi |

## `nguon_cap_viec`

Packet khắc phục **chính revision 1 của nó**. Căn cứ: cross-review lượt 4,
`ops/reviews/ci-windows-review-4-claude-verdict.md`
(`sha256 e112e404ffd9cef528ff3a40f1744cc33a5f983fab939e3d2368db9ee664f9a8`), verdict **`blocked`**,
theo §3.2 *"finding cho thấy chính spec thiếu thì verdict là `blocked` và đi qua revision mới"*.

**Công việc `M1`–`M7` ĐÃ THI CÔNG XONG** ở head `6d46e6fc16ca`; bốn finding của ba lượt trước đã
đóng. r2 **chủ yếu phát biểu lại `nghiem_thu`** và nới `write_set` cho đủ kham.

## Vì sao r1 không thi hành được — hai khiếm khuyết ĐO ĐƯỢC

### Đ1 — `A1` của r1 đòi GIỮ chính con bug

r1 dòng 104: *"`grep -c 'os: ${{ fromJSON'` trên `ci.yml` = **1** … số khác 1 ⇒ ĐỎ"*.

Đo tại `6d46e6fc16ca`: **0**.

Không vá được, vì `A1` chỉ đạt khi `ci.yml` chứa nguyên văn `os: ${{ fromJSON` tại `chuan-bi.outputs`
— mà đó **chính là** lỗi `P1`: giá trị `outputs` của một job **phải là chuỗi**, `fromJSON('[...]')`
trả **mảng**, GitHub từ chối cả template (*"A sequence was not expected"*, `ci.yml` dòng 40, job
`105282976101`), kéo ba job `gate` · `gate-registry` · `gate-packet-loop` thành **`skipped`**.

Bất biến mà `A1` sinh ra để canh — *một nguồn duy nhất cho ma trận `os`* — **vẫn được giữ**, và `t161`
đo nó đúng. Hỏng là **cách phát biểu**: `A1` đo **CHÍNH TẢ** của một tên hàm, không đo **THẨM QUYỀN**.

### Đ2 — `M5` tất yếu làm `r291` ĐỎ, mà tệp phải sửa NẰM NGOÀI write set

| phép đo (`16:46Z 17-09`) | |
|---|---|
| `docs/**/*.md` trên `a612c70cbc56` | **73 tệp** |
| trên `6d46e6fc16ca` | **74 tệp** (thêm `docs/adr/0049-*.md` của `M5`) |
| `scripts/tl_selftest.py:21300` | `len(paths) + 73 == 253` — **đấm cứng số 73** |
| `scripts/tl_selftest.py:21303` | `len(tren_dia) == 73` |
| hậu quả đo được | `gate (ubuntu-latest)` **FAILURE**, job `105289776267`, bước 26 `tl selftest` |

`scripts/tl_selftest.py` **không** có trong `write_set` của r1 ⇒ vi phạm luật **L2**: đặc tả hứa thứ
write set không kham được. Và tệp ấy **nằm trong** `RELEASE_MANIFEST.json` (đo: `True`;
`file_count` **180**) nên sửa nó kéo theo phải tái sinh manifest — **đường thứ sáu**.

Tiền lệ y hệt: packet #522 gặp đúng chuyện này và phải đi qua **revision 3**.

## `write_set` — ĐÚNG SÁU đường, liệt kê tường minh

```
.github/workflows/ci.yml
ops/lease_publish_test.py
docs/adr/0049-cong-hai-nen-truoc-phat-hanh-khong-phai-moi-lan-land.md
docs/PROTOCOL_DA_PHIEN.md
scripts/tl_selftest.py
RELEASE_MANIFEST.json
```

**Bốn đường đầu**: giữ nguyên từ r1. **Hai đường cuối**: mới, và chúng là hệ quả **bắt buộc** của
`Đ2`, không phải mở rộng tuỳ tiện.

### `ngoai_le_adr_0044` — khai tường minh

| trường | giá trị |
|---|---|
| `tran_goc` | **3 tệp** cho class `sensitive` |
| `tran_da_duyet_cho_r1` | **4 tệp** |
| `tran_xin_cho_r2` | **6 tệp** |
| `tran_dong_them` | **300** — **GIỮ NGUYÊN**, không xin nới |
| `ai_nang` | `ducthangho` |
| `can_cu` | `Đ2` ở trên: `M5` thêm một tệp `docs/**/*.md` ⇒ `r291_docs_ngoai_goi` ĐỎ ⇒ cần `scripts/tl_selftest.py`; tệp ấy ở trong manifest ⇒ cần `RELEASE_MANIFEST.json` |

**Đo tại `16:46Z 17-09-2026`**: `numstat` so `a612c70cbc56` = **4 tệp, +257 / −24**. Phần kê khai slot
(`M8`) và tái sinh manifest (`M9`) thêm vài dòng ⇒ dự kiến vẫn dưới 300. **Con số này chống đỡ một câu
về THẨM QUYỀN — đo lại ngay trước khi đẩy, không chép lại.**

### `write_set_da_quet_toan_kho`

Đo `16:46Z 17-09-2026`, sau khi chữa hai nhánh cục bộ tụt sau (cổng `ai-dang-giu` fail-close đúng luật
và in sẵn lệnh chữa):

| đường dẫn | `ai-dang-giu` |
|---|---|
| `scripts/tl_selftest.py` | `rc=0` · **NGƯỜI_GIỮ 0** |
| `RELEASE_MANIFEST.json` | `rc=0` · **NGƯỜI_GIỮ 0** |

Bốn đường cũ đã do lease gen 1 giữ; gen 1 mất hiệu lực khi r2 được đóng băng (§3.2). **Quét lại cả
sáu đường ngay trước khi cấp lease gen 2** — con số trên sẽ trôi.

## `ngoai_pham_vi` — CỐ Ý không làm

1. **Không chữa nợ `WP541`** (`ops/lease_publish.py:1106` ghi cứng PATH `/usr/bin:/bin`). Nó có phiên
   riêng. `ops/lease_publish.py` **không** trong write set.
2. **Không sửa `ops-don-ref.yml`** để dập finding `SC1003:info` — đỏ sẵn trên cả bốn vế, không phải
   việc của packet này. `A6` phát biểu theo delta chính vì thế.
3. **Không khai `types: [labeled]`** cho `pull_request` trong `ci.yml`. Nó đổi hành vi CI ngoài ý định
   packet; đã ghi thành nợ ở `ADR-0049` (độ phủ Windows cho `ops/`, `scripts/`, `.github/` về 0).
4. **Không viết cổng đo "outputs phải là chuỗi" cho mọi cách sinh mảng.** Chốt hiện tại bắt
   `fromJson(`; hai đường khác **đã đo là LỌT** — xem `chua_do_duoc` C3.
5. **Không chạy CI tay.** `manual_ci_budget: 0`; cấm `workflow_dispatch`, cấm gọi lane `windows`, cấm
   full CI tay.

## `muc_tieu` — mỗi mục chiếu vào MỘT đường trong write set (L2)

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M1** | Job `chuan-bi` (ubuntu, không checkout mã sản phẩm) tính **một lần** danh sách nền, xuất qua `outputs.os`. Bỏ `github.ref == 'refs/heads/master'`; giữ `workflow_dispatch` và nhãn `windows` | `ci.yml` |
| **M2** | Ba job `gate` · `gate-registry` · `gate-packet-loop` đọc `needs.chuan-bi.outputs.os`; xoá cả ba biểu thức chép | `ci.yml` |
| **M2b** | **MỚI (từ `P1`)** — giá trị `chuan-bi.outputs.os` là **CHUỖI JSON**, KHÔNG bọc `fromJSON`/`fromJson`. Việc phân giải nằm ở **consumer** | `ci.yml` |
| **M3** | Chốt **NGUỒN DUY NHẤT**: quét `ci.yml`, ĐỎ khi bất kỳ job nào khai `os:` riêng ngoài `needs.chuan-bi.outputs.os` | `ops/lease_publish_test.py` |
| **M3b** | **MỚI (từ `P1`)** — chốt **OUTPUTS KHÔNG BỌC `fromJson`**: quét **mọi** job, không phân biệt hoa thường | `ops/lease_publish_test.py` |
| **M4** | **Evaluator TỐI GIẢN** cho đúng hình biểu thức của `chuan-bi`, **fail-close** (`KHÔNG ĐO ĐƯỢC` ⇒ ĐỎ) khi gặp hình khác; bảng ca `push master` · `PR thường` · `PR nhãn windows` · `workflow_dispatch` | `ops/lease_publish_test.py` |
| **M5** | `ADR-0049` ghi đổi tiêu chuẩn gate; kèm phần **mất mát**, và **ghi trạng thái đo được tại thời điểm land** của lane Windows bị gỡ | `docs/adr/0049-*.md` |
| **M6** | `ADR-0049` khai rõ *"land không còn chạy Windows"* **không** đúng tuyệt đối — diff chạm `.claude/dev/**` vẫn sinh Windows qua `launcher-windows.yml` | `docs/adr/0049-*.md` |
| **M7** | Một hàng mới cho `ADR-0049` trong bảng `§20`, **đúng một dòng** | `docs/PROTOCOL_DA_PHIEN.md` |
| **M8** | **MỚI (từ `Đ2`)** — kê khai slot `r291_docs_ngoai_goi`: `73 → 74` và `253 → 254`, theo đúng NẾP của khối chú thích tệp ấy (nêu đúng tệp được thêm) | `scripts/tl_selftest.py` |
| **M9** | **MỚI (từ `Đ2`)** — tái sinh `RELEASE_MANIFEST.json` sau `M8`; diff của manifest **chỉ** chứa `scripts/tl_selftest.py`, `file_count` **giữ 180** | `RELEASE_MANIFEST.json` |

## `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3)

| # | tiêu chí | cái gì làm nó ĐỎ |
|---|---|---|
| **A1** *(viết lại — `M1`,`M2`,`M3`)* | `t161_M3_chot_nguon_duy_nhat_ma_tran_ci` ⇒ `1/1 đạt`, `rc=0` | thêm một job khai `os:` riêng ⇒ ĐỎ. **Đột biến**: gỡ ruột `_kiem_tra_nguon_duy_nhat_os_ci` (cho luôn trả `[]`) ⇒ ca ĐỎ. **Đo `A1` theo THẨM QUYỀN, KHÔNG theo chính tả** — `fromJson`/`fromJSON` đều hợp lệ. Con số *"giảm từ 3 xuống 1"* là **ghi chú lịch sử**, không phải tiêu chí |
| **A2** *(giữ)* | Ca dựng `ci.yml` giả có **một** job lén khai `os:` riêng ⇒ chốt bắt được; bản không lén ⇒ `rc=0` | chốt không phân biệt hai bản ⇒ ĐỎ |
| **A3** *(giữ)* | Bảng bốn ca của evaluator: `push master` ⇒ `["ubuntu-latest"]` · `PR thường` ⇒ `["ubuntu-latest"]` · `PR nhãn windows` ⇒ hai nền · `workflow_dispatch` ⇒ hai nền | sai một ca ⇒ ĐỎ. **Đột biến**: đưa `github.ref == 'refs/heads/master'` trở lại ⇒ ca `push master` ĐỎ |
| **A4** *(viết lại — `M4`)* | Fail-close: biểu thức **hình khác** (kể cả **bọc `fromJSON` ngoài**) ⇒ in `KHÔNG ĐO ĐƯỢC` và raise | **Đột biến do REVIEWER bơm vào HÀM THẬT trên bản sao** — đổi nhánh fail-close thành `return ["ubuntu-latest"]` ⇒ ca đích phải ĐỎ; verdict ghi **câu khẳng định nào đã giết** nó. **CẤM mã hoá đột biến thành một hàm cục bộ trong tệp test** — đó chính là cách tautology ra đời ở lượt 1 |
| **A5** *(giữ)* | `packet_loop.py adr-song --root .` ⇒ số ADR **bằng** số dòng `§20`, khớp 1–1 | thiếu dòng `§20` ⇒ `rc=9` |
| **A6** *(viết lại — toàn packet)* | `actionlint` trên **cả 6** workflow: **số finding trên head BẰNG số trên `base_sha`** ⇒ **delta = 0**. `rc` chỉ ghi để đối chiếu, **không** là tiêu chí. **Khai nền đo có `shellcheck` hay không.** Thiếu `actionlint` ⇒ **ĐỎ** | delta finding ≠ 0 ⇒ ĐỎ. **Không được phát biểu theo `rc=0` tuyệt đối** — đo `16:46Z 17-09`: `rc=1`, **1** finding (`ops-don-ref.yml SC1003:info`) trên **cả bốn** vế (`f27a28f`, `d1258fe`, `6d46e6f`, `a612c70`) ⇒ `rc=0` là thứ **không bao giờ đạt được** |
| **A7** *(giữ — nó ĐÃ LÀM ĐÚNG VIỆC)* | `ops/lease_publish_test.py` chạy trọn **N/N** (hai số BẰNG NHAU), `rc=0`; và `doctrine-scan` · `adr-song` · `doc-claims-check --strict` · `git diff --check` · **`tl.py --selftest`** · `release-verify --strict` đều `rc=0` | bất kỳ cổng nào khác 0, hoặc `N/M` hai số khác nhau ⇒ ĐỎ. **Chính `A7` bắt được `Đ2`** — `tl selftest` ĐỎ ở bước 26 của job `105289776267` |
| **A8** *(giữ, số đổi)* | `git diff --numstat` so `base_sha`: **≤ 6 tệp** và **≤ 300 dòng thêm** | vượt ⇒ **DỪNG**, xin ngoại lệ **TRƯỚC** khi đẩy. Con số này chống đỡ một câu về **THẨM QUYỀN** — đo lại ngay trước khi đăng |
| **A9** *(giữ)* | Sau merge: đếm job Windows sinh bởi push `master` đầu tiên, bằng `actions_list` lọc `head_sha` ⇒ phải là **0** từ `ci.yml`. Job từ `launcher-windows.yml` **không tính** nếu diff chạm `.claude/dev/**` | > 0 job Windows từ `ci.yml` ⇒ packet **chưa đạt**, dù A1–A8 xanh |
| **A10** *(MỚI — `M2b`,`M3b`)* | Trên head cuối: `chuan-bi` ⇒ **`success`**, VÀ ba job `gate` · `gate-registry` · `gate-packet-loop` ⇒ **CÓ CHẠY**. Đo bằng `pull_request_read get_check_runs` trên đúng `head_sha` | `chuan-bi` khác `success` ⇒ ĐỎ. **`skipped` ở bất kỳ job nào trong ba ⇒ `KHÔNG ĐO ĐƯỢC`, KHÔNG phải đạt.** Đột biến: bọc lại `fromJSON` quanh `outputs.os` ⇒ `chuan-bi` FAILURE và ba job `skipped` |
| **A11** *(MỚI — `M8`,`M9`)* | `docs/**/*.md` đếm được **74**; `r291_docs_ngoai_goi` **ĐẠT**; `git diff -- RELEASE_MANIFEST.json` chỉ chứa `scripts/tl_selftest.py`; `file_count` **giữ 180** | `tl.py --selftest` ĐỎ ⇒ chưa đạt. Manifest đổi thêm tệp khác ⇒ ĐỎ (dấu hiệu chạm ngoài write set) |

**`A10` là tiêu chí DUY NHẤT có răng với lớp lỗi `P1`.** Ở lượt 3, `t161`/`t162` xanh, `A1` = 1,
`actionlint` delta 0, `adr-song` `rc=0` — **tất cả đều đúng**, và workflow vẫn chết. Mọi cổng tại chỗ
mù với hợp đồng kiểu của `outputs`; chỉ lượt CI thật thấy.

**`A9` và `A10` chỉ đo được sau khi có lượt CI** — `A9` sau merge, `A10` trên PR. Đó là điều kiện của
bài toán dưới `manual_ci_budget: 0`, không phải thiếu sót.

## `hinh_dang_ke_thua` (L4)

**KHÔNG phải `khong_ap_dung`** — r2 là bản khắc phục của r1, nên phải chép bộ đếm hình dạng lỗi sang.

| hình dạng | số lần đã xảy ra | ở đâu |
|---|---|---|
| **`TIEU-CHI-THEO-GIA-TRI-TUYET-DOI`** — tiêu chí phát biểu theo giá trị **tuyệt đối** của một phép đo bề mặt thay vì theo **DELTA** hoặc theo **BẤT BIẾN** | **2** | `A1` (`grep` = 1) · `A6` (`actionlint rc=0`) |
| **`DOT-BIEN-TAUTOLOGY`** — "đột biến" là một hàm cục bộ khẳng định chính thứ nó vừa được viết để trả, không thể ĐỎ | **2** | `t161` `chot_bi_go` · `t162` `evaluator_doan_bua` (cross-review lượt 1, đã đóng ở lượt 2) |

Chốt *"cùng một hình dạng lỗi lặp lần thứ BA ⇒ DỪNG, hỏi 'có nên làm việc này không', không hỏi 'vá
thế nào'"* vì thế **bắt đầu từ 2 cho cả hai hình dạng**, không từ 0. Lần sau gặp là **đã chạm trần**.

## `chua_do_duoc` — ghi thẳng, không giấu sau chữ "có thể"

- **C1 — Hành vi thật của ma trận trên CI chỉ đo được bằng lượt CI thật.** `t162` đo một **evaluator
  viết tay** mô phỏng biểu thức Actions. Nó đọc **ngữ nghĩa điều kiện** đúng (bốn ca đều ra kết quả
  đúng) nhưng **không đo hợp đồng kiểu của `outputs`** — đó là lý do `P1` lọt qua toàn bộ cổng tại
  chỗ. `A10` thu hẹp lớp này, **không đóng** nó: evaluator vẫn có thể hiểu khác GitHub ở một mặt khác.
- **C2 — `A9` chỉ đo được SAU merge.** Câu hỏi *"một push `master` sinh mấy job Windows"* không có
  đường đo nào khác khi `manual_ci_budget = 0`.
- **C3 — Chốt `M3b` đo MỘT tên hàm, không đo bất biến nó khai.** Đo `16:4xZ 17-09`:
  `${{ fromJSON('[...]') }}` ⇒ **bắt được**; `${{ github.event.pull_request.labels.*.name }}` (bộ lọc
  trả **mảng**) ⇒ **LỌT**; `${{ needs.chuan-bi.outputs }}` (**đối tượng**) ⇒ **LỌT**. Hai ca lọt làm
  GitHub chết **y hệt** `P1`. Đây là **danh sách CẤM**, và kho đã ghi rằng danh sách cấm *"thua từ
  trong thiết kế"*. r2 **cố ý không** đòi đảo thành danh sách cho phép (xem `ngoai_pham_vi` 4) — ghi
  thành nợ **`OUTPUTS-CHUOI-CHUA-CO-DANH-SACH-CHO-PHEP`**.
- **C4 — Mệnh đề *"8 cổng của `deploy-package.*` thay thế được lane Windows bị gỡ"* đã được ĐO và
  BÁC.** Đo trên cây: 8 cổng là `selftest` `gen_inst` `workflow` `golden` `docclaims` `determinism`
  `relcheck` `relverify` (`deploy-package.sh:113-120`), và `lease_publish_test` đếm **0** lần ở **cả**
  `.sh` lẫn `.ps1`. Nên nó **không** thay thế được; `ADR-0049` đã sửa theo. Ghi ở đây để r2 không tái
  sinh lời khai cũ.
- **C5 — `gate-registry (ubuntu-latest)` trên head `6d46e6fc16ca` vẫn `in_progress` lúc viết tệp này
  (`16:46Z`).** Không đọc thành đạt. Phải đo lại trước khi cấp lease gen 2.

## Ràng buộc

- **KHÔNG CI tay**: `manual_ci_budget = 0`.
- **KHÔNG viết cú pháp biểu thức Actions trong comment của `run`** — một cặp rỗng trong dòng chú thích
  từng làm cả tệp không hợp lệ.
- **KHÔNG viết `[skip` + `ci]` nguyên văn trong thông điệp commit**, kể cả khi trích dẫn.
- **KHÔNG hạ tiêu chuẩn gate mà không khai**: `M5` bắt buộc.
- **Đọc `rc` TRỰC TIẾP, không qua pipe.** Nợ `RC-QUA-PIPE-KHONG-CO-CHOT`: cùng ngày 17-09-2026, cả
  executor lẫn reviewer **độc lập** khai sai `actionlint rc=0` vì `| tail` rồi đọc `$?`.

## Điều kiện dừng

- Vượt **6 tệp** hoặc **300 dòng thêm** ⇒ DỪNG, xin ngoại lệ **TRƯỚC** khi đẩy.
- Cần chạm dòng nào khác của `docs/PROTOCOL_DA_PHIEN.md` ngoài **một hàng `§20`** ⇒ DỪNG, revision mới.
- Một trong hai hình dạng ở `hinh_dang_ke_thua` lặp **lần thứ ba** ⇒ DỪNG, hỏi *"có nên làm việc này
  không"*.
- `A10` cho `skipped` ⇒ **KHÔNG ĐO ĐƯỢC**, không được đọc thành đạt; dừng và báo.
