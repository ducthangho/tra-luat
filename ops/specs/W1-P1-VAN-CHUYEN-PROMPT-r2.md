# ĐẶC TẢ ĐÓNG BĂNG — `W1-P1-VAN-CHUYEN-PROMPT` — **BẢN SỬA ĐỔI 2**

> Đặc tả này **không cấp việc**. Phải có Issue + lease còn hiệu lực (`docs/PROTOCOL_DA_PHIEN.md`
> §3.2, §4) mới được bắt tay. Phiên nào đọc rồi tự làm là tự cấp việc cho mình.
>
> Sửa đặc tả đã có băm ⇒ đi qua **bản sửa đổi mới**.

`packet_id`: `W1-P1-VAN-CHUYEN-PROMPT`
`revision`: **2**
`thay_the_cho_ban`: `W1-P1-VAN-CHUYEN-PROMPT.md` (r1, sha256 `91c5de58…0199`) — r1 KHÔNG bị xoá, giữ nguyên làm hồ sơ.
`packet_issue`: **368**
`nen_do`: `origin/master` `27fb9de` (Merge PR #362 — packet #359 đã land 04:55:11Z)
`thoi_diem_soan`: 06:31Z 28-08-2026

## VÌ SAO CÓ BẢN SỬA ĐỔI 2 — đúng MỘT thay đổi

`executor` đổi từ `claude` sang **`codex`** (`xhigh`). §3.2 của protocol ghi thẳng: đổi
`executor` **tạo revision mới và làm lease cũ mất hiệu lực** — nên không thể sửa tại chỗ r1.

**Đây là NGOẠI LỆ CÓ CHỦ Ý của người giữ kho đối với ADR-0041, không phải một lượt đọc sai luật.**
Nói thẳng cả hai vế:

- ADR-0041 (`Accepted` 17-08-2026) ghi: *"Codex chỉ nhận Packet `routine`/`systemic` nhỏ, đóng,
  write-set độc lập"*. W1-P1 là **`sensitive`** ⇒ theo luật thường Codex **không** đủ điều kiện
  làm Executor.
- Người giữ kho quyết 28-08-2026, trong phiên, sau khi được trình bày đúng mâu thuẫn này:
  **Codex làm Executor, override ADR-0041.** Thẩm quyền: §2 — `override` thuộc chủ kho.

Ghi lại để lượt sau không đọc nhầm thành tiền lệ: **ngoại lệ này gắn với riêng packet này**, không
nới ADR-0041, và không tự động áp cho packet `sensitive` nào khác.

**Phần ADR-0041 KHÔNG bị override, vẫn phải tuân:** *"PR do Codex code phải được phiên Claude mới
độc lập hoặc human review; Codex không review code mình."* ⇒ `reviewer_provider: claude`, và
phiên Claude làm reviewer phải **KHÁC** phiên điều phối đã soạn đặc tả này.

r1 sai ở chỗ nào: nó khai `executor: claude` vì chép từ bảng §M2 của kế hoạch thi công mà **không
đối chiếu** với chỉ đạo vận hành của người giữ kho (executor codex xhigh) trong cùng lượt giao
việc. Hai nguồn nói ngược nhau và r1 chọn một nguồn trong im lặng — đúng lỗi mà đặc tả phải chặn.

`review_class`: **`sensitive`** — write set chạm `.claude/dev/launcher.py`, đường PHÓNG của mọi
lượt executor/reviewer. Sai một chiều thì mọi lượt sau chạy trên nền vận chuyển đã hỏng.

## `nguon_cap_viec`

`ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md` §M2, dòng `W1-P1` (P0, class `sensitive`). Người giữ kho
duyệt mở 28-08-2026, kèm chỉ đạo **đợi packet #359 land rồi mới ghi** (#359 đã land 04:55:11Z).

**Hai nguồn nói ngược nhau về `executor`, và r2 chọn có tuyên bố:** bảng §M2 ghi `Claude`; chỉ đạo
vận hành của người giữ kho trong lượt giao việc ghi `codex` `xhigh`. Người giữ kho quyết dứt điểm
28-08: **`codex`** — xem §"VÌ SAO CÓ BẢN SỬA ĐỔI 2".

## Phạm vi đã được NGƯỜI GIỮ KHO quyết (28-08-2026, trong phiên)

**Phạm vi write set đang có HAI nguồn nói ngược nhau, và chênh lệch là một tệp.**

| nguồn | ngày | nói gì về schema `review_verdict.v1` |
|---|---|---|
| `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md` §M2 | 23-08-2026 | write set có `planned:.github/coordination/schemas/review_verdict.v1.schema.json` |
| `ops/KE_HOACH_DIEU_CHINH_DA_NEN_TANG.md` §5 "Nhóm C" | 20-08-2026 | `W1-P1` schema `review_verdict.v1` → **hoãn** — *"thư mục schema đang rỗng"* |

Đọc theo hướng cho phép đi tiếp: bản 23-08 **mới hơn**, và chính bản 20-08 tự khai ở đầu tệp
*"Không cấp authority — authority là Packet Spec, GitHub facts và receipt đã verify"*. Cộng
với việc người giữ kho vừa duyệt mở packet, ba dữ kiện ấy nghiêng về **làm trọn ba tệp**.

Nhưng lý do hoãn KHÔNG tự hết hiệu lực chỉ vì tệp kế hoạch mới hơn được chạm lần cuối vào
23-08 — commit `82e5cd4` ấy là việc của `#276` (ảnh doctor nonce+HMAC), **không phải một lượt
xét lại W1-P1**. Không có bản ghi nào cho thấy quyết định hoãn 20-08 đã được thu hồi.

**QUYẾT ĐỊNH Q1 — `(a)` LÀM TRỌN BA TỆP.** Người giữ kho quyết 28-08-2026: quyết định hoãn
20-08 hết hiệu lực vì packet đã được duyệt mở. Lý do hoãn là *"thư mục schema đang rỗng"* — mà
đó chính là thứ packet này sinh ra để sửa, nên nó là lý do **tự huỷ** khi packet mở.

⇒ Write set là **ba** đường dẫn. Mục **M4–M7 ở trạng thái `CHOT`**, có hiệu lực đầy đủ.

**QUYẾT ĐỊNH Q2 — THU HỒI SỚM lease #363.** Người giữ kho duyệt thu hồi
`probe-agent-exec-1-codex-20260828` (packet #363, đã được lệnh DỪNG) bằng cơ chế
`da_bi_thay_the`. Cách thi hành ở §"Thu hồi lease #363" dưới.

## Packet Spec — hợp đồng (§3.2)

```yaml
schema_version: 1
spec_ten: W1-P1-VAN-CHUYEN-PROMPT
revision: 2
packet_issue: 368
executor: codex            # xhigh — NGOAI LE ADR-0041, chu kho duyet 28-08-2026
reviewer_provider: claude  # ADR-0041 (KHONG bi override): codex khong review code cua chinh no
environment: cloud
risk: normal
review_class: sensitive
assurance_target: cross_approved
write_set:
  - type: exact
    path: .claude/dev/launcher.py
  - type: exact
    path: .claude/dev/launcher_test.py
  - type: exact
    path: .github/coordination/schemas/review_verdict.v1.schema.json
depends_on: []
acceptance_criteria:
  - M1 run.json ghi sha256 stdout/stderr, khong chi st_size
  - M2 run.json ghi ten transport, dung MOT gia tri moi provider
  - M3 consumer fixture doc prompt.snapshot va khang dinh byte khop
  - M4 schema tu choi verdict dung shape nhung sai reviewed_sha
  - M5 schema tu choi sai generation
  - M6 schema tu choi sai role
  - M7 schema tu choi sai identity
```

Trường phái sinh (`change_policy_sha`, `effective_write_set`, `required_checks`,
`land_obligations`, `effective_review_class`) **do dispatcher bổ sung** — §3.2 cấm agent tự khai.

## Giới hạn lời khai — bắt buộc giữ nguyên trong MỌI tài liệu của packet

Packet này chứng minh **byte tới consumer adapter**. Nó **KHÔNG** tuyên bố model "đã hiểu",
"đã đọc", hay "đã tuân thủ" nội dung prompt. Mọi câu trong PR body, CHANGELOG, comment và
biên nhận phải giữ đúng biên giới này. Câu kiểu *"đã chứng minh reviewer nhận đúng chỉ thị"*
là vượt biên — thứ đo được chỉ là *"đúng dãy byte ấy đã tới đầu đọc của adapter"*.

## Nền đã ĐO — số kèm thời điểm (luật L5)

Đo trên clone sạch `origin/master` `fe6152b`, container remote Linux, 02:38–02:41Z 28-08-2026.
Rig là **clone**, không phải worktree — `chay_cac_probe()` ném `Chan(MA_WORKTREE)` khi `.git`
là TỆP, nên worktree cho số khác và số ấy là tạo tác của rig.

| phép đo | kết quả | ghi chú |
|---|---|---|
| `launcher_test.py` | `154/154 ca DA CHAY QUA (tong 155, bo qua 1, hong 0)` | 1 ca bỏ qua = `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125` (fixture Windows; bản POSIX là `t63`, chạy được) |
| `ops/lease_publish_test.py` | `116/116 đạt; đã chạy=116, bỏ qua=0` | có `actionlint` 1.7.7 + `shellcheck` 0.10.0 trên PATH |
| `actionlint` toàn workflow | `rc=1`, **1** finding | `ops-don-ref.yml:106 SC1003:info` — **ĐỎ SẴN, delta = 0** |
| `doctor` | `rc=0` `DU CONG CU BAT BUOC` | sau khi cài `codex` 0.150.1 + `chuan-bi` |
| `doctor --kiem-song` codex | `rc=0 (VAN dung duoc)` | ảnh chụp cũ 104.9h, `SAP_HET_HAN` nhưng **gọi thật được** |

**ĐO LẠI trên `27fb9de` sau khi #359 land** (nó sửa ĐÚNG hai tệp write set này: `launcher.py`
+26/−15, `launcher_test.py` +17/−2 — nên nền BẮT BUỘC phải đo lại, không được suy):

| phép đo | trên `fe6152b` | trên `27fb9de` | kết luận |
|---|---|---|---|
| `launcher_test.py` | `154/154` (tổng 155, bỏ qua 1, hỏng 0) | **giống hệt** | nền còn dùng được |
| 10 số dòng trích ở §"ĐÃ CÓ" | — | **từng dòng khớp nguyên văn** | không trôi |

Không trôi vì **cả bốn** hunk của #362 trong `launcher.py` nằm ở `@@ -2850 -2874 -2895 -2941` —
**dưới** mọi dòng trích (cao nhất 1655), trong vùng `_doc_mcp_json`/`_env_da_chuan`, không chạm
vùng vận chuyển prompt. `launcher_test.py` +17/−2 mà tổng ca vẫn **155** ⇒ #359 sửa trong ca sẵn
có, không thêm ca mới.

**TRÔI SỐ ĐÃ BẮT ĐƯỢC — ghi lại vì đúng bệnh luật L5 tố cáo:** bản giao việc cho phiên này khai
`lease_publish_test` = `114/114` khi đủ công cụ. Đo thật **02:40Z 28-08** ⇒ **`116/116`**. Mẫu số
đã trôi `114 → 116`; bất biến *"đủ công cụ thì N/N hai số bằng nhau"* vẫn đúng, nên dòng cũ
**trông như đã kiểm**. Kiểm SỐ HẠNG, đừng kiểm quan hệ.

## Bằng chứng — cái gì ĐÃ CÓ, cái gì THIẾU

Đọc `.claude/dev/launcher.py` `fe6152b` (3998 dòng). **Đừng viết đặc tả cho thứ đã tồn tại.**

### ĐÃ CÓ (không được viết lại, chỉ được mở rộng)

| năng lực | ở đâu | hành vi đo được |
|---|---|---|
| Neo prompt bằng sha256 | `chot_prompt()` d.1228–1250 | đòi **CẢ** `--prompt-file` lẫn `--expected-prompt-sha256`; thiếu một ⇒ `Chan(MA_THAM_SO)` |
| Chặn prompt RỖNG | `chot_prompt()` d.1243 | tệp rỗng có sha256 hợp lệ nhưng vô nghĩa ⇒ `Chan(MA_PROMPT)` riêng |
| Chặn sha sai định dạng | `chot_prompt()` d.1247 | không khớp `SHA256_RE` ⇒ `Chan(MA_THAM_SO)` |
| Chặn prompt lệch | `chot_prompt()` d.1249 | `Chan(MA_PROMPT, "prompt lech: ...")` |
| **Chặn đổi prompt SAU preflight** | `lenh_run` d.1499–1501 | hash LẠI ngay trước khi sinh con ⇒ `Chan(MA_PROMPT, "prompt DOI giua luc kiem va luc chay")` |
| Bản chụp bất biến | `lenh_run` d.1502–1513 | `prompt.snapshot` trong thư mục lượt, `0600` ngay từ `os.open`, thư mục `0700` |
| Thay `{PROMPT_FILE}` | `lenh_run` d.1516–1518 | trỏ vào **bản chụp**, không phải đường gốc; `run_root` `resolve()` bắt buộc |
| **`{PROMPT_FILE}` không có `--prompt-file` ⇒ CHẶN** | `lenh_run` d.1522–1528 | fail-close, `Chan(MA_THAM_SO)`; nếu im lặng thì con nhận chuỗi nguyên văn |
| Sổ ghi có ký | `_ghi_so` + `ky_ban_ghi_luot` d.1368 | `run.json` ký HMAC, neo `nonce`/`attempt` |
| Sổ ghi prompt | `run.json` | `prompt_sha256` · `prompt_ban_chup` · `prompt_kin_hoan_toan` (True/False, **khai thẳng khi lớp 2 không có**) |
| Dọn bản chụp | d.1639–1640 | xoá sau khi con thoát (`prompt_ban_chup_da_xoa`), quét rác >24h ở `_cap_id` |

⇒ **Phần lớn `Acceptance` "`{PROMPT_FILE}` thiếu/sai bị chặn" và phản chứng "đổi prompt sau
preflight" ĐÃ ĐƯỢC THI HÀNH.** Việc của packet là **đo lại cho có phản chứng khoá bằng `rXX_`**,
không phải viết lại.

### THIẾU (đây mới là việc thật)

| thiếu | đo thế nào để thấy nó thiếu | chiếu vào |
|---|---|---|
| **Output SHA** | `run.json` chỉ ghi `stdout_byte`/`stderr_byte` = **`.stat().st_size`** (d.1655–1659). Không dòng nào băm stdout/stderr. `grep -n 'sha256' launcher.py \| grep -i out` ⇒ **0 kết quả** | `launcher.py` |
| **Tên/băm TRANSPORT theo provider** | `grep -nE 'transport\|van_chuyen' launcher.py` ⇒ **0 kết quả**. Có khái niệm `provider`/`surface` trong bảng `CONG_CU` (d.1858, 3466) nhưng **không có sổ ghi "provider này đi bằng transport nào, băm bao nhiêu"** | `launcher.py` |
| **Consumer fixture nhận byte snapshot** | không có fixture nào đọc `prompt.snapshot` rồi khẳng định byte khớp | `launcher_test.py` |
| **Schema verdict semantic identity** | `.github/coordination/schemas/` **không tồn tại** (đo 02:36Z 28-08) | schema (chờ **Q1**) |

## Write set

```
.claude/dev/launcher.py                                       [BỊ GIỮ lúc soạn]
.claude/dev/launcher_test.py                                  [BỊ GIỮ lúc soạn]
.github/coordination/schemas/review_verdict.v1.schema.json    [tự do; CHỜ Q1]
```

Trạng thái lease đo **HAI lần**, cả hai sau khi so TẬP TÊN hai nguồn ref
(`ls-remote --heads` ↔ `for-each-ref`, `comm` hai chiều) ⇒ phép quét KHÔNG mù:

| lúc | ls-remote | for-each-ref | `comm` hai chiều | kết quả lease |
|---|---:|---:|---|---|
| 02:39Z 28-08 | 237 | 237 | rỗng | không đổi |
| 03:08Z 28-08 | 240 | 240 | rỗng | không đổi |

**Số ref là ẢNH CHỤP, không phải bằng chứng bền:** `237 → 240` trong 29 phút, ba nhánh mới. Ghi
cả hai lần đo để người đọc sau không dùng một con số đã chết làm chốt. Thứ neo được là **chiều
lệch** (`comm` rỗng cả hai chiều), không phải con số.

Bảng dưới là kết quả của **cả hai** lần đo — giống hệt nhau:

| đường dẫn | rc | NGƯỜI_GIỮ |
|---|---:|---|
| `.claude/dev/launcher.py` | 11 | 2 |
| `.claude/dev/launcher_test.py` | 11 | 2 |
| `.github/coordination/schemas/review_verdict.v1.schema.json` | 0 | 0 |

Hai lease giữ: `mcp-doc-phan-tich-exec-1r3-codex-20260828` (#359) và
`probe-agent-exec-1-codex-20260828` (#363). **Tính tới 06:31Z 28-08, CẢ HAI đều là XÁC CHẾT** —
#359 đã land `04:55:11Z`, #363 đã được lệnh DỪNG — mà cả hai vẫn còn hiệu lực (tới `17:05:00Z`
và `2026-08-29T02:00:00Z`). Người giữ kho duyệt **thu hồi cả hai** bằng `da_bi_thay_the`
(§"Thu hồi lease").

**Sắc thái đã đo, không được đọc thành quyền đi trước:** PR #362 (nhánh của #359) hiện chỉ đổi
`mcp_github_doc.py` và test của nó — **không chạm `launcher.py`**. Lease giữ RỘNG hơn diff thật.
Điều đó rút ngắn thời gian chờ dự kiến, nhưng `CLAUDE.md` ghi thẳng *"Không tầng nào kiểm diff
có nằm trong write set hay không"* ⇒ #359 vẫn có thể ghi `launcher.py` ở lượt sau. **Chờ, không
đi trước.**

## Mục nghiệm thu — mỗi mục kèm phép đo làm nó ĐỎ (luật L3)

| # | mục | phép đo làm ĐỎ | tệp |
|---|---|---|---|
| **M1** | `run.json` ghi **băm sha256** của stdout và stderr, không chỉ kích thước | ca `rXX_` đọc `run.json` sau một lượt, băm lại `stdout.log` trên đĩa và đòi bằng nhau. **Đột biến:** đổi băm ghi sổ thành băm của chuỗi rỗng ⇒ ca phải ĐỎ | `launcher.py` · `launcher_test.py` |
| **M2** | `run.json` ghi **tên transport** đã dùng cho lượt đó, và nó là **đúng một** giá trị cho mỗi provider | ca `rXX_` chạy hai lượt cùng provider và đòi cùng tên transport. **Đột biến:** cho một provider hai transport ⇒ ĐỎ | `launcher.py` · `launcher_test.py` |
| **M3** | **Consumer fixture** đọc `prompt.snapshot` và khẳng định **byte** khớp tệp nguồn | fixture ghi prompt có ký tự nhiều byte + chuỗi thoát nguyên văn (`cödex`), so `sha256` hai đầu. **Đột biến:** tráo snapshot bằng tệp khác cùng kích thước ⇒ ĐỎ | `launcher_test.py` |
| **M4** | Schema từ chối verdict **đúng shape nhưng sai `reviewed_sha`** | fixture verdict hợp lệ, đổi mỗi `reviewed_sha` ⇒ phải bị từ chối | schema |
| **M5** | Schema từ chối sai **generation** | như trên, đổi mỗi generation | schema |
| **M6** | Schema từ chối sai **role** | như trên, đổi mỗi role | schema |
| **M7** | Schema từ chối sai **identity** | như trên, đổi mỗi identity | schema |

**M4–M7 phải là danh sách CHO PHÉP, không phải danh sách CẤM.** Bài học đã trả giá ở
`v1.36.68`/PR #104: cổng từ chối đúng hai chuỗi `claude`/`codex` nên `codex-dispatcher`,
`ai-codex-bot`, `cödex` lọt sạch — *"phân biệt CÁCH VIẾT, không phân biệt THẨM QUYỀN"*. Kèm
chốt bắt buộc: **đột biến NỚI danh sách cho phép để chứa tên tấn công phải làm ca đích ĐỎ** —
không có đột biến ấy thì không biết ca đang đo danh sách hay đo thứ khác.

## Phản chứng bắt buộc (không được để nằm trong tài liệu — phải thành `rXX_` chạy được)

1. Đổi prompt sau preflight ⇒ ĐỎ. *(chốt đã tồn tại d.1499; packet phải khoá bằng ca test)*
2. Tráo `prompt.snapshot` giữa lúc ghi và lúc con đọc ⇒ ĐỎ.
3. Echo đúng schema nhưng SHA khác ⇒ ĐỎ.
4. `{PROMPT_FILE}` có mặt mà thiếu `--prompt-file` ⇒ ĐỎ. *(chốt đã tồn tại d.1522)*
5. Nới danh sách cho phép để chứa tên tấn công ⇒ ca đích ĐỎ.

**NGHĨ RA được phép thử mà KHÔNG CHẠY nó thì phép thử ấy KHÔNG TỒN TẠI.** Năm dòng trên là
danh sách việc, không phải danh sách trấn an.

## Ngưỡng gate của packet

- `launcher_test.py` phải ≥ `154/154` nền + số ca mới, **hai số bằng nhau**, `hong 0`.
- `actionlint` `rc=1` với **đúng 1** finding `ops-don-ref.yml:106` ⇒ **đỏ sẵn, delta = 0**.
  Số finding tăng ⇒ hồi quy của packet.
- Gate đỏ ⇒ đo lại trên `origin/master` sạch **trong CÙNG một lệnh dựng cả hai vế** rồi so DELTA.
- `git config core.abbrev 7` trước khi chạy gate.

## Thu hồi lease — CẢ HAI, cơ chế và thứ tự

Người giữ kho duyệt thu hồi **cả hai** lease đang giữ write set này, vì **cả hai đã hết việc mà
vẫn còn hiệu lực**:

| lease | packet | vì sao là xác chết | còn hiệu lực tới |
|---|---|---|---|
| `mcp-doc-phan-tich-exec-1r3-codex-20260828` | #359 | **ĐÃ LAND** — PR #362 merge `04:55:11Z` | `2026-08-28T17:05:00Z` |
| `probe-agent-exec-1-codex-20260828` | #363 | đã được lệnh **DỪNG** | `2026-08-29T02:00:00Z` |

Quyết định #363: 28-08 (Q2). Quyết định #359: 28-08, **sau khi #359 land** — lúc được hỏi lần đầu
người giữ kho đã đúng khi từ chối, vì khi ấy #362 còn đang sửa `launcher.py` thật.

**Cơ chế — ĐO trong mã, không suy:**

- `ops/lease_publish.py` d.930/934 (`lenh_ai_dang_giu`): lease `CÒN_HẠN` mà mang
  `da_bi_thay_the` bị dán nhãn `ĐÃ_BỊ_THAY_THẾ` và **loại khỏi `nguoi_giu`**. Đây là đường
  DUY NHẤT tắt được một lease còn hạn.
- `ops/lease_publish.py` d.562–572 (`_kiem_thay_the`): đăng lease mới mang `thay_the_cho: X`
  **đòi lease X đã mang sẵn** `da_bi_thay_the: <lease_id mới>`. Cổng **không tự sửa hồ sơ cũ**
  — nguyên văn: *"cổng không tự sửa hồ sơ cũ"*.

**Tiền lệ trong chính kho này:** lease r3 của #359 thu hồi `mcp-github-doc-exec-1r2-codex-20260827`
đúng bằng cách này, và `thay_the_ly_do_r1` của nó ghi rõ lý do — packet #355 ĐÃ LAND nhưng lease
vẫn còn hạn và vẫn giữ write set, tức đúng nợ `AG-T0-01B`.

**GIỚI HẠN CỦA CƠ CHẾ — đo được, và phải khai vì nó làm hồ sơ bất đối xứng:**
`_kiem_thay_the` đọc `thay_the_cho` bằng `str(lease.get("thay_the_cho") or "").strip()` (d.558)
⇒ **một lease mới chỉ khai thay thế được MỘT lease cũ.** Nhưng phép loại khỏi `NGƯỜI_GIỮ`
(d.930/934) chỉ đọc `da_bi_thay_the` trên lease **cũ**, không đòi lease mới khai ngược lại. Nên
thu hồi hai lease bằng một lease mới là **làm được**, với cái giá: một trong hai bản ghi có con
trỏ MỘT CHIỀU. Khai thẳng ở đây thay vì để nó im lặng.
Đã kiểm không sinh báo động giả: `lenh_con_tro_treo` **bỏ qua** lease mang `da_bi_thay_the`
(d.947), nên bản ghi một chiều không bị đếm là con trỏ treo.

**Thứ tự thi hành — làm LIỀN NHAU, cùng bước cấp lease:**

1. Thêm `da_bi_thay_the: <lease_id W1-P1>` vào **cả hai** tệp:
   · `ops/leases/probe-agent-exec-1-codex-20260828.yaml` trên nhánh `ops/cap-lease-probe-agent-20260828`
   · `ops/leases/mcp-doc-phan-tich-exec-1r3-codex-20260828.yaml` trên nhánh `ops/cap-lease-mcp-github-doc`
2. Đăng lease W1-P1 mang `thay_the_cho: probe-agent-exec-1-codex-20260828` (bản #359 được thu hồi
   bằng trường `da_bi_thay_the` một chiều — xem giới hạn trên).

⚠️ **Nhánh giữ hồ sơ lease KHÔNG phải nhánh bị cấm chạm.** Hồ sơ nằm trên
`ops/cap-lease-probe-agent-20260828`; nhánh bị cấm là `codex/probe-agent-exec-1`. Đã kiểm: hai
nhánh khác nhau, thao tác này không chạm nhánh cấm.

**Vì sao phải LIỀN NHAU:** tách bước 1 khỏi bước 2 mở ra cửa sổ hồ sơ lease không nhất quán —
lease cũ trỏ một `lease_id` chưa tồn tại. Và giữa quét và đăng phải **quét lại**: phiên trước đã
tạo ra tình huống hai writer vì một lease land đúng trong cửa sổ 18 phút giữa hai bước ấy.

## Nợ ghi nhận

`AG-T0-01B-thu-hoi-lease-chua-co-duong` — **lần thứ ba trong hai ngày nợ này chặn việc thật**;
phải vào báo cáo của packet.

**Nói cho ĐÚNG hơn bản giao việc, vì phép đo không khớp lời khai.** Bản giao việc khai *"không
có lệnh thu hồi lease"*. Đo trong mã: **không có LỆNH thu hồi, nhưng CÓ CƠ CHẾ** —
`da_bi_thay_the` (§"Thu hồi lease #363"). Khác biệt quan trọng vì nó đổi hẳn cách chữa: không
phải "chờ hết hạn", mà là "cấp lease thay thế". Cái nợ thật, hẹp hơn và đúng hơn, là:

- cơ chế đòi **một lease MỚI** mới tắt được lease cũ ⇒ không tắt được một lease khi **không có
  việc kế tiếp** để cấp lease cho;
- cổng **không tự sửa hồ sơ cũ**, nên phải sửa tay đúng thứ tự, và sai thứ tự thì cổng chặn;
- không có lệnh nào trả lời *"lease này còn phục vụ packet nào không"* — `_phan_loai_lease` chỉ
  biết HẠN. Đúng nợ `SO-LEASE-KHONG-NAM-MOT-CHO` đã ghi.
