# Hậu kiểm connector trên PR #652 — sáu finding sau merge, xử lý và bằng chứng

**Định danh là BĂM, không phải tên nhánh.** Đặc tả đóng băng: `ops/specs/THU-HOI-LEASE-A1a-r2.md`,
sha256 `9bc0fe282fbebc02791f47a30e4ff187b1182a2e5e357ee2e66c04d4f7dac7cd`, blob
`9c65f4e29ae8f361d09d45f1f7b91776789efef9`, land ở merge commit `67802bf9a1b9adba6d8b13c63ee46744d74655b5`.
Tệp này **không** sửa đặc tả và **không** sửa `ops/lease_publish*.py`.

## Chuyện gì đã xảy ra

PR #652 rời draft lúc `01:26:00Z` 27-09-2026. Việc đó **tự kích** connector `chatgpt-codex-connector[bot]`
(review bắt đầu `01:26:07Z`). Phiên soạn merge lúc `~01:26:3xZ`, sau khi kiểm CI 8/8 và human audit, nhưng
**không chờ** lượt connector đang chạy. Connector đăng review `5328420840` lúc `01:34:18Z` trên `d71f77e`:
**4 P1 · 2 P2**, không finding nào nhắm vào tệp đặc tả.

Đây là mặt thứ tư của bài học CLAUDE.md *"Gate xanh KHÔNG phải đã được review"*: rời draft là một cò
review, nên phải chờ nó xong rồi mới merge.

## Sáu finding

| # | mức | tệp | finding | xử lý | bằng chứng |
|---|---|---|---|---|---|
| C1 | P1 | `luot1`–`luot6-HINT.patch` | thiếu nhãn patch-as-hint (protocol §13, ràng buộc 1) | **SỬA**: thêm nhãn nguyên văn ở đầu từng tệp, kèm sha256 bản reviewer sinh ra | bảng H dưới; cả sáu patch `git apply --check` **OK** trước và sau khi thêm nhãn, trên đúng bản nháp gốc |
| C2 | P1 | `luot7-VERDICT.md` | `reviewed_sha 7fc28680` ≠ head `d71f77ec` (connector gọi là `f1dec864`) | **ĐÃ CHẤP NHẬN** trong human audit (#652 `5851587276`: *"neo_commit chi them hien vat review luot 7"*). Lượt 8 neo đúng head chứa nó (mục L8) | `d71f77ec^{tree}` = `45e611fa…`, `7fc28680^{tree}` = `15c0240b…`, khớp mô tả của connector. `f1dec864` **không** có trong kho (`git cat-file -t` lỗi); nhiều khả năng là commit merge tổng hợp của connector. Blob đặc tả bằng nhau ở cả hai commit |
| C3 | P1 | `luot7-VERDICT.md` | verdict không khai `execution_surface` / `transport` | **BỔ SUNG** ở bảng S dưới, lấy từ `run.json` của launcher. **Không** sửa verdict: đó là hiện vật của reviewer | bảng S |
| C4 | P1 | `luot7-PROMPT.md` | `origin` của checkout reviewer là bare mirror cục bộ | **ĐÚNG, và rộng hơn connector nói**: cả **bảy** lượt đều vậy. Chữa bằng lượt 8 với `origin` thật (mục L8) | bảng S, cột `origin cay-kho` |
| C5 | P2 | `do_q6.py` | không dùng `ls-tree -z` ⇒ tên có tab/xuống dòng lọt ra `ngoai_mien` im lặng | **SỬA** trong `do_q6_hk.py` (xem "Vì sao tệp mới") | tự kiểm **35/35** (thêm `ten-co-tab`, `ten-xuong-dong-sau-duoi`; lượt 8 thêm `ten-DEL-sau-duoi`, `ten-byte-sau-duoi`); kết quả thật trên cây mốc **không đổi** |
| C6 | P2 | `mut_q6.py` | bỏ qua mã thoát ⇒ mutant chết không `Traceback` được tính KHOP | **SỬA** trong `mut_q6_hk.py` | ma trận **27/27 DUNG**; phản chứng: gỡ chốt rc ⇒ `chet-im-lang-rc2` thành `SAI KHOP` ⇒ `CO_LECH` |

## Vì sao tệp mới, không sửa tại chỗ

Đặc tả đóng băng trích băm của hai script: `do_q6.py` sha256 `36d8f166…` (dòng 303) và `mut_q6.py` sha256
`272dc1e8…` (dòng 325). Sửa tại chỗ làm tệp ở đúng đường dẫn ấy lệch băm đặc tả khai, tức làm hỏng chính
bằng chứng đóng băng. Nên hai tệp gốc **giữ nguyên từng byte**; bản vá nằm ở `do_q6_hk.py` và `mut_q6_hk.py`.

HINT thì khác: protocol §13 đòi nhãn nằm **trên** patch, nên phải sửa tại chỗ. Băm cũ (trích ở
`luot5-VERDICT.md` và `luot6-VERDICT.md`) vẫn tái lập được: bỏ **3 dòng đầu** (`tail -n +4`) là ra đúng
byte reviewer sinh ra, và dòng nhãn ghi sẵn băm ấy.

Băm bản vá: `do_q6_hk.py` sha256 `0ec537e48b34631eee1e6161be2419bb7ba861a5a446b89afd4937672a974967` ·
`mut_q6_hk.py` sha256 `c4f04f03cf781089ae51faf1e8e63f1d7773bf301d2d61de0919f85a8428bb94`. Log:
`tu-kiem-q6-2026-09-27.log` (35/35) · `mut-q6-2026-09-27.log` (27/27, `TAT_CA_KHOP`). Phản chứng chốt rc
chạy trên bản trước khi đổi tên (khác đúng dòng docstring đầu): gỡ dòng `if rc!=(1 if dich else 0)` cùng
bảy assert tự kiểm ⇒ `SAI  KHOP chet-im-lang-rc2` ⇒ `CO_LECH`.

## Kết quả thật trên cây mốc: không đổi

`do_q6_hk.py . 072181157a27804e69deb35bb792a88c70ac31e3 2026-09-10T04:55:37Z` ⇒ `rc=0`, output **giống
từng byte** `q6-do-2026-09-26.json` (sha256 `1fc99cd9339fb5f085436e60ef39bac3058a79dbc009161597ecc7bc85efbd61`).
Cây mốc có **0** tên chứa ký tự điều khiển dưới `ops/leases`. `BIA_MO_LICH_SU = ()` đứng nguyên.

## Bảng H — nhãn HINT

| tệp | bản nháp gốc | sha256 bản reviewer (trước nhãn) | sha256 sau nhãn |
|---|---|---|---|
| `luot1-HINT.patch` | `f8a37c04` | `6ca984f6d17c641d4f6f5116898d443ecabe2244cd748d91657a55bad7587de8` | `230087e1432cecf2f9da0d9f42c2a6a8274d1846ce50eb0ec8af02d90bf653a9` |
| `luot2-HINT.patch` | `981b9ea1` | `1322a3ca7d942ec97508bb490e84b09757578b1897aa7f5792b8a4d1960fd3cf` | `0ecd3674221ab6ea1603a48543b4e6ea859d3a4572574aa8e90eaffe088ce170` |
| `luot3-HINT.patch` | `79b8ec7b` | `133e91d4d4d0d7368b46bfe6c812266b68e5e3777ac46f8f03a079cbf1f784fe` | `ba75a0914d8f4d8fea8eca1deb0a3b56e034b145ac85cebb971384efac662015` |
| `luot4-HINT.patch` | `33e19c41` | `6acfc8e2874aa46714c2842519a4e65e87f52e8f1507ef6b68f9739d110deb34` | `f571c1b3191aeab4ee03b69202b1424dbfbab3b53ea396151c240d0d6d76f593` |
| `luot5-HINT.patch` | `43a17e1e` | `816f293e6ce767e4debdf233b81fad1651db2d0ec760ce14fd42c987a643d6de` | `7a5c4ec19de5eef3d41d05c246b8463436394645a8fddc74224f209a70e2c3c1` |
| `luot6-HINT.patch` | `635e9a23` | `5e0e89aabfcffe166b980a8ac72fdd7ef53c53f678edb31c1d9a907c4b5e8503` | `c6086b71933f1118fce7dcb4fc92852eb8425fce39da38962d91d3224181ec8a` |

`luot7-HINT.patch` rỗng (0 byte), không cần nhãn.

**Câu hỏi còn mở, khai cho lượt 8 và chủ kho:** protocol §13 ràng buộc 3 chỉ cho patch-as-hint trên packet
`sensitive` với (a) tệp test thuần hoặc (b) tooling không tham gia authority. Sáu HINT trên nhắm `SPEC.md`
(một đặc tả), cùng `do_q6.py`/`mut_q6.py` (lượt 3, 4) là hiện vật review. Đặc tả không thuộc (a) hay (b)
theo chữ. Tôi **không** tự phân loại nó; ghi ra để lượt 8 xét.

## Bảng S — bề mặt thực thi, đo từ `run.json` của `launcher.py run`

Mọi lượt: `provider openai_codex` · `execution_surface codex_cli` · `transport machine` ·
`transport_sha256 5c77b6e983ee…` · header `stderr.log`: `model gpt-6-astra`, `reasoning effort high`,
`provider openai`, `sandbox workspace-write`.

| lượt | run_id | bắt đầu (UTC) | giây | `ma_thoat` | HEAD `cay-kho` | `origin` của `cay-kho` |
|---|---|---|---|---|---|---|
| 1 | `36c0d446` | 26-09 15:59:22 | 991 | 0 | `f8a37c04` | bare mirror cục bộ `…/a1a-l1-*/ws/kho.git` |
| 2 | `b3a1f870` | 26-09 22:55:25 | 1074 | 0 | `981b9ea1` | bare mirror cục bộ |
| 3 | `4d58c283` | 26-09 23:24:53 | 890 | 0 | `79b8ec7b` | bare mirror cục bộ |
| 4 | `e75b86d0` | 26-09 23:47:47 | 643 | 0 | `33e19c41` | bare mirror cục bộ |
| 5 | `8a6561f5` | 27-09 00:26:29 | 557 | 0 | `43a17e1e` | bare mirror cục bộ |
| 6 | `66f348ca` | 27-09 00:38:38 | 381 | 0 | `635e9a23` | bare mirror cục bộ |
| 7 | `afa0ef1f` | 27-09 00:49:29 | 495 | 0 | `7fc28680` | bare mirror cục bộ |

Bare mirror dựng bằng `clone --bare --no-local` từ kho làm việc, rồi nạp `refs/remotes/origin/*`. Đối chiếu
**tập tên nhánh** với `git ls-remote --heads origin` (máy chủ thật) **không** đồng đều giữa các lượt. Bản đầu của
đoạn này viết "trước mỗi lượt … lệch 0, không thì dừng": câu ấy suy từ script dựng **hiện hành**, không từ hồ sơ
từng lượt, và lượt 8 (F17, P1) bác đúng bằng hồ sơ lượt 1. Theo từng lượt:

| lượt | đối chiếu tập tên với máy chủ | nguồn |
|---|---|---|
| 1 | **lệch 1**: mirror 430, máy chủ 429 lúc 15:57Z; thừa `claude/wp523-r15-g17-a6-BAN-TRUNG-LAP-khong-land` (đã xoá trên máy chủ). Lượt vẫn chạy lúc 15:59Z | `luot1-EVIDENCE.md` E7 |
| 2 | 435/435, `comm -3` rỗng lúc 22:54:33Z, sau khi gỡ nhánh thừa trên | `luot2-EVIDENCE.md` E11 |
| 3 | 435/435, `comm -3` rỗng lúc 23:23:57Z | `luot3-EVIDENCE.md` dòng 23 |
| 4 | 437/437, `comm -3` rỗng lúc 23:47:11Z | `luot4-EVIDENCE.md` dòng 16 |
| 5–7 | **KHÔNG ĐO ĐƯỢC độc lập.** EVIDENCE ba lượt này không ghi phép so. Workspace còn `.mirror-info` (438 head lúc 00:25:51Z · 00:38:37Z · 00:49:28Z); script dựng hiện hành chỉ ghi tệp ấy **sau** chốt lệch = 0, nhưng phiên bản script lúc chạy không được lưu | `.mirror-info` trong workspace, ngoài kho |

Ở **mọi** lượt 1–7, phép so chỉ là so **tên**; OID là OID của cache kho làm việc, không phải readback máy chủ.
Còn **danh tính remote** trong checkout reviewer thì không được đối chiếu ở lượt nào: `remote get-url origin`
trả một đường dẫn cục bộ. Đó đúng là điều C4 nói. Lượt 8 là lượt đầu tiên so cả tên **và** OID, và đặt
`origin` về endpoint thật.

## L8 — lượt codex 8/10

Trần 10 (#564 `5851241285`); đã dùng 7. Lượt 8 khác bảy lượt trước ở đúng hai điểm:

1. `cay-kho` được `remote set-url origin https://github.com/ducthangho/tra-luat.git` trước khi giao; sandbox
   không có mạng nên reviewer đọc `refs/remotes/origin/*` đã nạp, cùng phép so tập tên với `ls-remote` do
   phiên điều phối chạy ngay trước đó (ghi trong EVIDENCE lượt 8).
2. Verdict phải khai `execution_surface` và `transport`, và neo `reviewed_sha` vào head của PR tiếp nối.

Kết quả lượt 8 ghi ở `luot8-VERDICT.md`: `changes_requested`, **2 P1 · 0 P2 · 0 P3**, 672 giây, `ma_thoat 0`
(`run.json`: `openai_codex` · `codex_cli` · `machine`; header `stderr.log`: `gpt-6-astra`, effort `high`).

- **F17** (P1, `so-do-khong-khop`): bảng S cũ khai "trước mỗi lượt lệch 0" — hồ sơ lượt 1 bác. **SỬA**: bảng theo
  từng lượt ở trên. Bản vá **không** dùng `luot8-HINT.patch` (viết lại bằng tay, từ chính hồ sơ E7/E11).
- **F18** (P1, `q6-thieu-kiem-id-ten`): đặc tả đóng băng vẫn **bắt** executor chạy `do_q6.py` 31 ca và `mut_q6.py`,
  tức đúng bộ đo đã biết lỗi C5/C6; tên hai bản `_hk` không có trong đặc tả; tiêu chí "có dòng `LECH` thì dừng"
  (dòng 371) cũng va với đối chứng âm `DUNG LECH chet-im-lang-rc2`. Chủ kho duyệt **revision 3 tối thiểu**
  (#564 [`5852159297`](https://github.com/ducthangho/tra-luat/issues/564#issuecomment-5852159297), vòng 5): `ops/specs/THU-HOI-LEASE-A1a-r3.md`
  chỉ đổi chỉ dẫn bộ đo thi công sang `do_q6_hk.py`/`mut_q6_hk.py` ghim băm, kèm tiêu chí dương đọc từ bản in. r2
  và hai script gốc giữ nguyên byte. Chờ lượt 9.
- Hai mutant lượt 8 ghi là **sống** (gỡ riêng nhánh DEL; decode `strict`): nhánh DEL nay có ca `ten-DEL-sau-duoi` và
  mutant `bo-rieng-DEL`; byte không-UTF-8 nay có **chốt riêng** (`ten-tep-khong-phai-utf8`), ca `ten-byte-sau-duoi`,
  mutant `bo-chot-utf8`. Mutant `strict` **không** đưa vào ma trận: nó chết bằng `UnicodeDecodeError`, tức giết
  bằng lỗi vô can — đúng loại tín dụng giả mà bộ phân hạng từ chối.

## Lượt 9/10 — revision 3

`changes_requested`, **0 P1 · 1 P2 · 0 P3** (`run.json` `ef7602b8`, 623 giây, `ma_thoat 0`; `openai_codex` · `codex_cli` ·
`machine`; header `gpt-6-astra` / `high`). F17 và F18 **ĐÓNG**; C5, C6 **ĐÓNG** trong bộ đo thi công r3; C3, C4 giữ
**ĐÓNG-MỘT-PHẦN** (giới hạn xác minh lịch sử, không phải lỗi mới). Reviewer thử từng tiêu chí dương của r3 và cả 14 phép
đổi bản in, băm, `rc` đều làm đúng tiêu chí ấy đỏ; khai thêm một hàng `mong="LECH"` bị chặn bởi tiêu chí "duy nhất đối chứng
âm" lẫn băm.

- **F19** (P2, `so-do-khong-khop`): `luot9-EVIDENCE.md` khai *"thay đúng 7 đoạn"* rồi liệt kê **8** mục. Danh sách đúng,
  con số sai. **Đính chính ở đây, không sửa `luot9-EVIDENCE.md`**: tệp ấy là đầu vào reviewer lượt 9 đã đọc, giữ nguyên
  byte để lời khai và finding cùng tra được. Con số nay **đo được**: script tạo r3 được trích nguyên văn từ transcript
  phiên soạn thành `tao_r3.py` (sha256 `ce56a45aa939e4cdfceef55a820ca8adc4e04f33c74e555c7bfd02e077a5d15b`), có đúng **8**
  lời gọi `rep()`, và chạy trên bản sao r2 cho ra r3 **giống từng byte** (`cmp` rc0, r3 sha256 `ac7e0129…`). Lượt 9 ghi
  *"không có script tạo r3 trong packet"*; nay có. `luot9-HINT.patch` (chỉ nhắm EVIDENCE) **không** áp, vì cách đính chính
  trên giữ được hồ sơ.

## Lượt 10/10 — lượt cuối

**`approve`, 0 P1 · 0 P2 · 0 P3**, `HINT.patch` rỗng (`run.json` `9fbc066d`, 477 giây, `ma_thoat 0`; `openai_codex` ·
`codex_cli` · `machine`; header `gpt-6-astra` / `high`). `reviewed_sha` `8eb076b6d5ff41feafa723829d126e2c34c8ba3b`,
`reviewed_spec_sha256` `ac7e0129b281b517c69e9a2512a05b47d55ad99f0ac964462c061ea511f70bc1`. F19 **ĐÓNG** (reviewer tự
đếm 8 lời gọi `rep()` bằng AST và trace, chạy `tao_r3.py` trên bản sao r2 ra r3 giống từng byte). C3/C4 giữ
**ĐÓNG-MỘT-PHẦN** vì giới hạn xác minh lịch sử ngoài sandbox, không phải finding.

Chuỗi hậu kiểm: lượt 8 `2 P1` → lượt 9 `1 P2` → lượt 10 `0`. Trần 10/10 đã dùng hết. Bước kế: human audit của chủ kho neo
**revision 3**, rồi merge PR #658 bằng merge commit. Commit mang verdict lượt 10 chỉ thêm hiện vật lượt 10 và mục này
(cùng tiền lệ đã được chấp nhận ở audit #652 `5851587276`).

