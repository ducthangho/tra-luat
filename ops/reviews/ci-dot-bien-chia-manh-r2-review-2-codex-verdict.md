verdict: changes_requested
reviewed_sha: 2a8af3a8bd7e4ffeb3212bc7d0d6a66daf73a637
nguong_ap: sensitive + chỉ thị chủ kho "đến hết P1, P2, P3"

Có **2 lớp finding mới còn mở: 1 P2 và 1 P3** (4 biểu hiện). Hai finding P2 lượt trước đã được chặn trong các phép tái kiểm. Không đủ điều kiện approved. Đã đo 50/237 mục tự đột biến chọn lọc, tất cả giết đúng; 10/10 mutant công cụ cũng giết đúng. Các mục chưa đo trọn được ghi rõ bên dưới.

## ĐỊNH DANH VÀ PHẠM VI

- HEAD như trên; tree `902bf7dd2917341a9d3e05aca2fc8b2ff60f9957`; base `5618f61c6ac2fa14aab52b0f5ce3d065aee8e022`. Diff đúng W1–W3. `ci.yml` không đổi; W1–W3 cũng không đổi giữa base spec `518faca` và base lease `5618f61`.
- SHA-256 của `spec-r2.md` và blob tại `b6380bf:ops/specs/CI-DOT-BIEN-CHIA-MANH-r2.md` cùng là `9a2ab4fe746330f87ef86cc9b9a2bef6da8edde6e198a1989d415827c9fb2783`. Lease `1efa6cf40c06e9413cd942a2260aed7b12fb8095`: revision 2 / generation 1, đúng base và write set, hết hạn 28-09-2026 15:22Z. Không xác thực người ký qua GitHub.
- Reviewer: `provider: openai_codex`, `execution_surface: codex_cli`, `transport: machine/local`. Header launcher báo Codex 0.157.1, `gpt-6-astra`, effort `xhigh`, session `01a0e3aa-3cad-7f60-8631-f38e9717d1e1` (`evidence/reviewer-header.txt`). Header chứng minh cấu hình được CLI công bố; không chứng thực độc lập model/effort mọi request. Không dùng subagent, không kế thừa context Executor.
- Linux; Python **3.12.3**, actionlint **1.7.7**, Ruff **0.15.8**. Dùng `PYTHONDONTWRITEBYTECODE=1`, Ruff `--no-cache`, Git global config riêng `sandbox/git-measure.config` tắt ký commit và ghim abbrev=7. Không sửa config cây được review. Origin của clone là mirror nội bộ được giao, không gọi mạng.
- Mỗi phép đo có command, rc thật, thời gian trong `evidence/<tên>.json`; output nguyên bản trong `.log`. `do/run_measure.py` là wrapper lưu kết quả: mã thoát **của tiến trình con** phải đọc từ JSON, không lấy rc của wrapper làm rc bộ test. Thời gian các probe chạy đồng thời không dùng để suy thời gian runner CI.
- Snapshot đầu `evidence/checkout-before.json`; lịch sử ghi tăng dần trước khi hợp nhất bảng ở `evidence/review-progress.md`. Cây `cay-kho` chỉ đọc theo kỷ luật phiên; sandbox thực tế cho phép ghi workspace, không phải mount read-only.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: `VERDICT-luot-1.md`, SHA `70d1698ad2867d8e6e6721d416e80b1f3ebb9704`.

| Finding cũ | Phân loại | Tự đo trên HEAD này |
|---|---|---|
| `workflow-matrix-type-confusion` [P2] | **ĐÃ VÁ THẬT** trong phạm vi đã đo | Matrix `[false,true,2,3]` / float bị `loi_workflow_dot_bien_du` chặn; workflow đúng được nhận. Bản sao chỉ đổi matrix bool: actionlint vẫn rc=0 nhưng registry thật rc=1, báo lệch job mảnh (`registry-matrix-bool-final.log`). Tháo `_bang_kieu` ⇒ 4 ca kiểu LỌT, 934/938; số 5 Executor khai sai được ghi lớp mới F02, không coi là workflow còn lọt. |
| `shard-json-schema` [P2] | **ĐÃ VÁ THẬT** với probe cũ và đột biến tháo chốt | CLI `--gop` từ chối phiên bản bool/float, `so_manh` float ở từng vị trí tệp, object thay mảng. Dựng đúng phản chứng cũ: cả hai trường trong cả 4 tệp là object `{tên: false}` ⇒ rc=1, `giet/tk_giet phai la mang` (`gop-old-exact-object.log`). N=1 bị chặn; N=2..8 đúng đều xanh. 36 mutant mảnh/gộp đều giết đúng, gồm chốt kiểu/miền mới và chốt cũ đã sửa neo (`new-mutants.log`). Không thấy đường xanh mới do vá schema. |

## BẢNG LỚP

| Slug | ID / biểu hiện | Mức còn mở | Nguồn | Cách đóng |
|---|---|---|---|---|
| `invalid-shard-no-execution-unobserved` | F01: gọi T1..T8 trước parse vẫn qua toàn bộ tự kiểm | P2 | Lượt 2 / HEAD đang review | Spy đủ bộ chạy trong r549; mutant chạy trước xác thực phải đỏ đúng r549; đối chứng không đột biến và mutant cũ vẫn đúng. |
| `executor-quantitative-claims` | F02a: khai 5 ca LỌT / 933; F02b: W1 khai +325; F02c: nền spec khai 185 | P3 | Lượt 2 / commit HEAD, PROMPT #3/#4, spec §1 | Sửa hồ sơ bằng output 4 ca / 934, W1 +323, nền 5c79fa2 có 200 mục. Ba biểu hiện cùng lớp số liệu không tái lập; số trong spec đóng băng cần điều phối xử lý hồ sơ, reviewer không tự sửa spec. |

## BẢNG ĐỐI CHIẾU SPEC

| Mục | Kết quả | Bằng chứng chạy được / giới hạn |
|---|---|---|
| M1 | Hành vi đã thử **đạt**; lỗ kiểm thử F01 | `contracts.log`: 13 chuỗi k/N sai trả rc=2 trước CASE/TU_KIEM; r549 còn thử RA vắng/rỗng và chỉ có RA. `inventory.log`: N=2..8 phủ đúng/rời nhau, bảng trùng tên bị chặn. r551/r552 đo truyền đúng tập, output, băm và chỉ ghi khi đạt. `child-env.log`: 242 lần gọi run không có biến mảnh, thiếu kết quả ⇒ rc=1, không JSON. Chưa chạy bốn mảnh đầy đủ. |
| M2 | **Đạt trong phạm vi kiểm gộp** | 86 tình huống CLI (`gop-boundaries.log`) + phản chứng object toàn bộ cũ: đúng N=2..8 xanh; sai kiểu/schema/tập tên/băm/số tệp/JSON đều đỏ. Đảo thứ tự tên vẫn giữ tập được nhận là không đổi tính phủ. Receipt tự dựng đủ tên/băm được nhận theo thiết kế, không phải bằng chứng đã chạy mutant. |
| M3 | **Lệch P2 F01** | 52 TU_KIEM, 52 nhóm bắt buộc, SAN_NHOM=52, 237 neo duy nhất; 36 mutant mảnh/gộp giết đúng `(36,0,0)`. Mutant bổ sung `probe-invalid-runs-ca` sống qua toàn bộ 52 ca; thêm spy vào r549 mới giết đúng. |
| M4 | **Đạt ở đường CLI** | `m4.log`: biến đúng cho bộ mục tiêu nhẹ qua 5 tình huống diff, cả hai bộ kia giữ nguyên; 6 giá trị lạ CLI `--chay` đều rc=2 trước kế hoạch. `contracts.log`: vắng/rỗng hợp lệ. Gọi thẳng hàm lập kế hoạch bỏ qua parser không phải đường vào runtime. |
| M5 | **Đạt trong phạm vi đã đo** | Workflow thật hợp lệ; matrix bool/float/thiếu/trùng/thừa, thiếu job/needs, if/continue-on-error/defaults, permissions/env lệch đều bị chặn. `registry-no-pinned-jobs.log`: tháo chốt job ⇒ 10 ca LỌT, 928/938, rc=1. Chốt equality theo kiểu ⇒ 4 ca LỌT khi tháo. |
| M6 | **Đạt tĩnh/local** | `w3.log`: hai job khớp cấu trúc ghim; upload/download, N=4, needs đúng. `actionlint.log`: rc=0. Chưa chạy Actions/artifact thật. |
| M7 | **Đạt qua phép đo yêu cầu** | r543 mã gốc 0/300; dưới rút-lại 0/300; trả generator cũ 11/300. 13 mục liên quan qua runner thật `(13,0,0)`, mục rút-lại đỏ đúng `{r527,r528}`. Không đổi bảng đích/phân hạng. |
| A1 | **Chưa đo đủ, không ghi pass** | Số lượng phân hoạch đúng `[3,3,2,2]` và `[60,59,59,59]`; tổng 10/237. CLI gộp fixture đúng phát đủ 3 dòng. Không tự chạy 4 mảnh trọn trên HEAD nên chưa xác minh rc và thời gian ~1900 s/mảnh Executor khai. |
| A2 | **Đạt** | Thiếu/thừa tệp, chuyển/xoá/trùng tên, sha-test/sha-tool, số mảnh, JSON hỏng đều rc=1. Bộ `new` đủ 36 mục giết đúng; không chốt cũ nào trong bộ này bị vá schema làm mất răng. |
| A3 | Hành vi HEAD đã thử đạt; **lệch phần tự kiểm P2 F01** | CLI sai dừng sớm, phân hoạch đúng; nhưng mutant chạy CA trước parse vẫn `52/52`, nên r549 chưa đo đủ điều "không chạy gì". |
| A4 | **not_run trọn bộ** | Đã đo nhẹ 8/8, TU_KIEM 52/52, DOT_BIEN thật `(10,0,0)`, 50/237 DOT_BIEN_TU_KIEM chọn lọc. Không đồng nhất chúng với lượt không mảnh đầy đủ 237 mục. Prompt cho phép bỏ lượt ~1 giờ. |
| A5 | **Đạt** | Registry HEAD rc=0, 938/938; các phản chứng A5 đều nằm trong output. `contracts.log`: biến mảnh ở bước ci.yml bị env guard chặn; ở job/workflow bị băm gate-registry chặn. |
| A6 | **Đạt local trong phạm vi W1/W2/W3** | Registry base 916/916 và HEAD 938/938; các phản chứng cũ không hụt. Ruff F cùng 0.15.8 trên base/HEAD đều 0, delta=0. actionlint rc=0. Chưa chạy bare Ruff đúng pin CI 0.15.15 hoặc các bộ khác full/Windows. |
| A7 | **not_run, ngoài cổng land** | Không GitHub/network/CI theo chỉ thị. Chưa xác minh thời gian thực, upload/download artifact trên runner hoặc mốc 22–25 phút. |
| A8 | **Đạt qua phép đo local** | Ba lượt 300 gọi trực tiếp như M7; 12 mutant nhắm r543 và mục rút-lại đều giết đúng qua bộ phân hạng thật. Không cần suy A8 từ A4 chưa chạy. |

## BẢNG SĂN

Các lệnh Python dưới được bọc bằng `python3 do/run_measure.py <tên-log> ...` để lưu env, rc và log. Tất cả bản đột biến nằm ngoài `cay-kho`.

| Hướng | Giả thuyết / lệnh chính | Output thật | Kết luận |
|---|---|---|---|
| 1 | Probe cũ matrix: `python3.12 do/probe_contracts_r2.py`; registry `sandbox/workflow-bool/...` | Validator từ chối; actionlint bool rc=0; registry rc=1 | **KHÔNG PHẢI LỖI** trên HEAD; lỗi cũ được vá |
| 2 | Schema cũ: `python3.12 do/probe_gop_r2.py`; `--gop sandbox/gop-probes/object-both-all` | Sai kiểu toàn bộ/ở từng vị trí đều rc=1; đúng N=2..8 rc=0 | **KHÔNG PHẢI LỖI** trong phạm vi probe |
| 3 | Thiếu/trùng/chuyển tên, thiếu/thừa JSON, băm lệch, rác JSON/UTF-8 | Đều rc=1; dict trong mảng làm TypeError rc=1 | **KHÔNG PHẢI LỖI** cho việc fail-closed; phần tử sai kiểu chưa có chẩn đoán GOP chuẩn |
| 4 | Tệp tự dựng với đúng băm/tên | rc=0, GOP 4/4 + 10/10 + 237/237 | **KHÔNG PHẢI LỖI** so M2; hash không xác thực nguồn gốc/lịch sử thực thi |
| 5 | `doc_manh`, phân hoạch, tên trùng: contracts + inventory | Chuỗi sai rc=2; trùng hai bảng ValueError; N=2..8 phủ đủ/rời nhau | **KHÔNG PHẢI LỖI** |
| 6 | Chạy con còn biến mảnh: `python3.12 do/probe_env_children.py` | 242 run, LEAKS=[], cha đã pop; kết quả thiếu bị main từ chối rc=1, không receipt | **KHÔNG PHẢI LỖI**; probe cố ý cắt việc, không phải A1 |
| 7 | M4 cho phép giá trị lạ / làm nhẹ bộ khác: `python3.12 do/probe_m4.py` | 6 chuỗi lạ CLI rc=2, không kế hoạch; 5 diff với biến đúng không đổi hai bộ kia | **KHÔNG PHẢI LỖI** đường CLI; giá trị không phải str trong dict giả không đại diện os.environ |
| 8 | Biến mảnh ở ci.yml: contracts | Bước bị env guard chặn; workflow/job bị hash guard chặn | **KHÔNG PHẢI LỖI** trong đường registry thật |
| 9 | Tháo allowlist hai job / so kiểu: registry no-pinned-jobs / weak-types | 928/938 (10 LỌT) / 934/938 (4 LỌT), rc=1 | Chốt có răng; **LỖI F02a** ở số 5 Executor khai |
| 10 | Tín dụng giả: `python3.12 do/probe_credit_r2.py` | TypeError → DO_KHAC/TIN DUNG GIA; no-op → child rc=0/TIN DUNG GIA; `(0,2,0)` | **KHÔNG PHẢI LỖI**, không cấp GIẾT sai |
| 11 | A8: `do/do_r543.py <W1> 0 300`, `1 300`; bộ sinh cũ `1 300` | 0/300, 0/300, 11/300; target runner `(13,0,0)` | **KHÔNG PHẢI LỖI** ở r543 |
| 12 | Đột biến mọi chốt mới: `do/tk_muc.py <W1> 0/1 new`; mục `ghi-so-gop` | `(36,0,0)`; ghi-so-gop `(1,0,0)` | **KHÔNG PHẢI LỖI** trên các mutant đã đăng ký; F01 là mutant bổ sung còn sống |
| 13 | Thêm `chay_ca(None)` trước parse; `do/probe_invalid_runner.py <W1>` | Cả 52 ca xanh; input 4/4 vẫn chạy T1..T8 rồi rc=2; mutant `(0,1,0)` | **LỖI F01** |
| 14 | Thử spy r549: `do/probe_invalid_fix.py`; runner trên `sandbox/invalid-fix-head` | HEAD+spy 52/52; mutant đỏ đúng r549, `(1,0,0)` | Hướng vá có đối chứng dương/âm |
| 15 | Đếm diff: `git diff --numstat base..HEAD` | W1 +323/−7; W2 +81/−10; W3 +46/−0 | **LỖI F02b** ở số +325; tổng +450/−17 đúng |
| 16 | Thời gian A1, A4 trọn bộ, A7 runner/artifact, hướng cần thoát đường dẫn | Không có phép đo thực tế trong lượt này; không soạn/chạy nội dung thoát đường dẫn | **KHÔNG ĐO ĐƯỢC / not_run**, không gán pass |

## BẢNG ĐO

| Khẳng định | Executor khai | Reviewer đo được | Khớp? |
|---|---|---|---|
| #1 A1 bốn mảnh + gộp, rc=0, ~1900 s/mảnh | 3/60, 3/59, 2/59, 2/59; tổng 10/237 | Phân hoạch đếm đúng; gộp fixture đúng. Chưa chạy bốn mảnh trọn, không có receipt/log nguyên gốc để xác minh ~1900 s | **Chưa xác minh trọn** |
| #2 registry W2 | HEAD 938/938, base 916/916 | Đúng hai con số, cùng Python 3.12.3/config không ký; rc=0 | **Khớp** |
| #3 `_bang_kieu` → `==` | 5 ca LỌT, 933/938 | **4** ca LỌT, **934/938**, rc=1, tái lập hai lần. Python-version float vẫn đỏ | **Sai — F02a** |
| #4 diff | +450/−17; W1 +325, W2 +81, W3 +46 | Tổng +450/−17; W1 **+323**/−7, W2 +81/−10, W3 +46/−0 | **Sai chi tiết W1 — F02b**; S5 không vượt |
| #5 inventory | 237 mục, neo duy nhất; 52 TU_KIEM; SAN_NHOM 52 | 237/237 neo duy nhất ngoài bảng; 52 ca, 52 nhóm, SAN=52 | **Khớp** |
| #6 W3 giản lược hai job | Bỏ Force LF và fetch-depth:0; gom không env | Đúng cả W3 và `_job_manh_gop`; ci.yml/băm gate không đổi | **Khớp tĩnh**; lý do đủ trên runner chưa đo A7 |
| #7 actionlint/Ruff F | rc=0, F sạch | actionlint 1.7.7 rc=0; Ruff 0.15.8 base/HEAD cùng 0 | **Khớp phiên bản local đã nêu**; không suy bare lint pin 0.15.15 |
| #8 A4 HEAD | Chưa có; đang chạy trên lượt 1 | Reviewer cũng không chạy A4 trọn HEAD; không có evidence run khác trong bundle | **Không phản chứng**; trạng thái thực thi bên Executor không quan sát được |
| Spec §1: nền tại 5c79fa2 | 185 DOT_BIEN_TU_KIEM | Git blob `5c79fa2c94b328ae3bbbef52a4cfa820fc40bc4a` có **200**; `68b552d` cũng 200 | **Sai — F02c**; không dùng ví dụ 185 làm kỳ vọng cứng khi A1 quy định N hiện tại |
| Commit 70d1698: +33 mục, 200→233; 48→52 | Theo message commit đầu | Dùng bảng Git: base 200, lượt 1 233, HEAD 237; TU_KIEM/SAN 48→52 | **Khớp**, AST từ đúng Git blobs (`history-counts.log`) |
| Commit HEAD: 5 p*, 4 kịch bản r552, 6 mutant riêng | Theo message commit vá | 5 phản chứng, 4 entry r552. Theo tên mutant: thêm **5**, bỏ **1**, net +4; sửa neo 4 mục cũ. Sáu chốt kiểu/miền/giá trị phiên bản đều có mục được đo | **Khớp khi phân biệt cách đếm**; không diễn giải thành +6 mục mới hay 5 ca đo phép so kiểu |

## FINDINGS

### invalid-shard-no-execution-unobserved [P2] r549 không quan sát hai bộ chạy mà nó tuyên bố cấm

**TỆP/DÒNG:** `ops/nhanh_don_duoc_test.py:3934`–`:3935` (`_manh_gia`), `:3951`–`:3955` (`r549`).

**VẤN ĐỀ:** M1/A3 đòi k/N sai không chạy gì; M3 đòi tự kiểm có răng cho chốt ấy. `r549` chỉ nhìn `not goi`, trong khi stub `chay_ca` và `chay_tu_kiem` không ghi dấu gọi. Trên bản sao, thêm `chay_ca(None)` ở đầu nhánh có biến mảnh, trước parse, vẫn cho `TU KIEM: 52/52`. CLI sai `4/4` thực sự chạy cả T1..T8 rồi mới báo lỗi. HEAD hiện từ chối sớm đúng; lỗi ở khả năng khoá bất biến của ca mới, không phải kết luận HEAD đang chạy test với đầu vào sai.

**ĐÃ THỬ VÁ:** Trong bản sao của riêng r549, thay hai stub bằng spy ghi `ca=True`/`tu_kiem=True` vào `goi`. HEAD+spy vẫn 52/52; mutant+spy đỏ đúng `{r549}`. Cần thêm mutant riêng "chạy trước xác thực" và giữ các đối chứng giá trị hợp lệ. Không đổi stub chung làm lệch kỳ vọng `goi` của r551 một cách mù quáng.

**ĐÃ THỬ NGHIỆM:**

```sh
python3 do/run_measure.py invalid-runs-self env NHANH_DON_DUOC_CHI_TU_KIEM=1 python3.12 sandbox/invalid-still-runs/nhanh_don_duoc_test.py
python3 do/run_measure.py invalid-runs-cli env NHANH_DON_DUOC_MANH=4/4 NHANH_DON_DUOC_MANH_RA=sandbox/never.json python3.12 sandbox/invalid-still-runs/nhanh_don_duoc_test.py
python3 do/run_measure.py invalid-fix python3.12 do/probe_invalid_fix.py
python3 do/run_measure.py invalid-actual-runner python3.12 do/probe_invalid_runner.py cay-kho/ops/nhanh_don_duoc_test.py
python3 do/run_measure.py invalid-fixed-runner python3.12 do/probe_invalid_runner.py sandbox/invalid-fix-head/nhanh_don_duoc_test.py
```

Output lần lượt: tự kiểm rc=0/52 trên 52; CLI in `CASE T1: DAT` … `CASE T8: DAT` rồi `MANH: LOI`, rc=2; spy phân biệt đúng mã gốc và mutant. Runner thật trước vá `(0,1,0)` (child rc=0), sau vá `(1,0,0)` (r549 1/1). `invalid-fix-self.log` chứng minh 52/52 ở bản thêm spy không đột biến. Không suy bản vá thử đã qua trọn 237 mutant.

**ĐỘ TIN:** Cao; một lớp, một biểu hiện. Nhãn hướng vá: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Script/bản sao là dữ liệu review, không là quyền ghi branch.

### executor-quantitative-claims [P3] Ba số liệu khai không khớp phép tái lập

**TỆP/DÒNG:** `PROMPT.md` bảng #3/#4; `spec-r2.md` §1 (DOT_BIEN_TU_KIEM=185 tại 5c79fa2); message commit `2a8af3a8bd7e4ffeb3212bc7d0d6a66daf73a637` phần F01; `.claude/dev/ci_dang_ky_test.py:1925` (ca python-version float).

**VẤN ĐỀ:**

1. Tháo `_bang_kieu` về `return a == b` cho **934/938**, đúng **4** ca LỌT, không phải 933/938 và 5 ca. Ca python-version float vẫn bị `3.12 != "3.12"` phát hiện; nó không chứng minh răng của phép so kiểu mới. Lỗi khai có trong cả bảng giao reviewer lẫn commit HEAD.
2. `git diff --numstat 5618f61..2a8af3a` cho W1 **+323/−7**, không phải +325. Tổng +450/−17 đúng; không kết luận vượt trần S5.
3. Spec §1 gắn số **185** DOT_BIEN_TU_KIEM với mốc `5c79fa2`, nhưng chính blob tại mốc ấy có **200** mục. `68b552d` cũng có 200. Đây là số nền sai, không phải dao động thời gian hay suy luận rằng bảng hiện tại phải giữ 185. Yêu cầu A1 đã cho phép dùng N thực tế, nên không phát sinh finding thứ hai cho ví dụ output M2 còn ghi 185.

**ĐÃ THỬ VÁ:** Thử đúng đột biến `_bang_kieu` trên bản sao; hướng sửa là cập nhật hồ sơ bằng số đo đúng, phân biệt ca đo kiểu mới với ca vốn equality đã bắt. Không cần đổi nghiệp vụ hoặc thêm ca chỉ để đạt số 5. Số nền trong spec cần đính chính nguồn/hồ sơ qua người điều phối; không tự sửa spec đóng băng.

**ĐÃ THỬ NGHIỆM:**

```sh
python3 do/run_measure.py registry-weak-types-final python3.12 sandbox/weak-types/.claude/dev/ci_dang_ky_test.py
git -C cay-kho diff --numstat 5618f61c6ac2fa14aab52b0f5ce3d065aee8e022..2a8af3a8bd7e4ffeb3212bc7d0d6a66daf73a637
```

Registry rc=1, `PHẢN CHỨNG: 934/938 đỏ đúng`. Bốn dòng LỌT: `matrix-bool`, `matrix-float`, `du-fetch-depth-false`, `du-timeout-float`. Kết quả lặp lại cả lần thăm dò và bản sao cố định. Numstat W1/W2/W3: `323 7` / `81 10` / `46 0`. `python3 do/run_measure.py history-counts python3.12 do/history_counts.py` đếm AST từ các Git blobs, ghi 200 tại cả 5c79fa2 và 68b552d (`history-counts.log` / `spec-baseline-counts.log`).

**ĐỘ TIN:** Cao. Một lớp báo cáo số liệu, ba biểu hiện F02a/F02b/F02c. Không khẳng định cơ chế kiểm kiểu HEAD còn lỗi cũ; ngưỡng chủ kho vẫn yêu cầu đóng P3 trước approval.

## GIỚI HẠN VÀ KIỂM READ-ONLY

- Chưa chạy A1 bốn mảnh thật, A4 full không mảnh, A7 Actions/artifact/thời gian, Windows và Ruff pin 0.15.15. Không coi rc của fixture hoặc probe cắt việc là bằng chứng cho các mục ấy.
- Không gửi thông điệp ra ngoài, không GitHub/CI, không commit/push/merge/land. Không soạn payload thoát thư mục/đường dẫn theo chỉ thị.
- Snapshot cuối: 2251/2251 tệp ngoài `.git`, 0 thêm/xoá/đổi; HEAD/tree giữ nguyên, status tracked/untracked/ignored rỗng, diff worktree/index rỗng (`checkout-verification.json`). Phép so hai mốc không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Bare mirror chỉ được đọc bằng Git; không có snapshot băm nội dung mirror từ đầu nên không khẳng định kiểm toàn mirror bằng hai mốc.
- Approval/assurance/land là các quyết định riêng; verdict này là changes_requested trên exact SHA đã ghi.
