verdict: changes_requested
reviewed_sha: 27f0d3054ee02e0584d00d750888737eac40585a

# VERDICT — #463 lượt review 19 (revision24/generation5, sensitive) — REVIEWER CLAUDE độc lập

reviewer: anthropic_claude / claude-fable-5 / max / claude_code / machine-local — context/clone mới, độc lập executor
packet: GATE-TACH-JOB-CAT-CHI-PHI (#463), mission #467 · base `bb7013c7669da19304a8769e5b25f8c1f8951e9c`
tree (mong đợi = đo): `43a566b03470bd9a706cd0241c6cbde2df12d370` — KHỚP · clone detached, porcelain 0 dòng (đo đầu VÀ cuối lượt)
CI/A1/A5: **not_run** theo chỉ thị chủ kho · integration với master `c16bd329…`: **not_measured** · không mạng/GitHub/dispatch/merge
Công cụ: Python 3.13 (`C:\Python313`) · ruff 0.15.15 (`D:\chocolatey\bin\ruff.exe`) · actionlint 1.7.7 + shellcheck 0.9.0 CÓ MẶT · git · bash chỉ `-n` (parse-only) · mọi đột biến/bản sao nằm `scratch/rv19/`, clone READ-ONLY

## Nhật ký đo

### Đ0 — Identity clone
`rev-parse HEAD` = `27f0d305…` (đầu + cuối lượt) · `HEAD^{tree}` = `43a566b0…` · `status --porcelain` rỗng cả hai lần · `HEAD~1` = `79b75cdb…` (đúng head R18).

### Đ1 — A8 + delta + freeze workflow (tự đo, không nhận artifact)
- `git diff --numstat base..head`: `.claude/dev/ci_dang_ky_test.py` **827**, `.github/workflows/ci.yml` **126** ⇒ additions **953 ≤ 1000**, đúng **2 path** (khớp numstat.txt).
- `delta-r18.patch` ≡ tự sinh `git diff HEAD~1 HEAD`: sha256 `0e7d78bd…` **BYTE-IDENTICAL**. Delta = **đúng 4 dòng fixture dữ liệu** chèn vào danh sách `_FX` trong `phan_chung()` — **0** thay đổi mã guard/lexer/harness/workflow.
- `diff.patch` ≡ tự sinh `git diff base..head`: sha256 `a78b35b4…`, 73 636 byte, **BYTE-IDENTICAL**.
- Workflow byte-identical: blob `ci.yml` = `cb025a5a70…` tại **cả bốn** mốc HEAD / `79b75cdb`(r18) / `ff146f16`(r16) / `3bbc6b46`(freeze).

### Đ2 — Baseline suite + Ruff + actionlint (clone, KHÔNG `--chay`, KHÔNG CI, KHÔNG thực thi fixture/installer)
Bản sao ghim `ROOT`→clone, chạy `python -X utf8 -B`: **rc=0 · ĐĂNG KÝ 21/21 · LAUNCHER WINDOWS 4/4 · RUFF CI 3/3 · PHẢN CHỨNG 675/675 · TỔNG: ĐẠT** (1,6 s) · **675 tên phân biệt, 0 trùng** · đủ 4 fixture mới (`ruff-ci-syntax-{command-substitution-depth-limit, escape-eof, second-heredoc, heredoc-unclosed}`).
Output của tôi ≡ `r19-targeted-registry.txt` **từng dòng (681=681)**, chỉ khác dòng `rc=0` cuối của executor.
Ruff `check --no-cache --select F` trên tệp Python đổi: **All checks passed, rc=0** (0.15.15). actionlint trên `ci.yml`: **rc=0, 0 chẩn đoán** — đo với shellcheck 0.9.0 CÓ MẶT (điều kiện đo khai kèm).

### Đ3 — TÁI LẬP 4 DOOR-MUTANT (EXECUTOR_DOOR_MUTATION_METHOD, neo TỰ ĐẶT trên clone; kèm đo thêm của tôi)
| mutant | rc | fixture LỌT | cô lập? | witness A/B (HEAD→mutant) |
|---|---|---|---|---|
| drop-depth-guard | 1 | đúng `…depth-limit` | **CÓ** (duy nhất) | `$(echo…)`×17: **2→0** (fail-open flip) |
| drop-heredoc-unclosed | 1 | đúng `…heredoc-unclosed` | **CÓ** | `cat <<'E'\nx\n`: **2→0** |
| drop-second-heredoc | 1 | đúng `…second-heredoc` | **CÓ** | `cat <<'A' <<'B'…`: **2→0** |
| drop-escape-eof | 1 | (không dòng LỌT) | — | `echo hi\`: **2→IndexError** |

**Failure-mode escape-EOF (nghĩa vụ riêng của lượt):** mutant chết bằng **IndexError tại `_dong_logic` dòng 232**, quy kết bằng patch `__globals__`: **479** lời gọi `loi_ruff_ci` sạch rồi crash đúng tại nguồn chứa `run: echo hi\` — tức **chính fixture `escape-eof` kích crash tại đúng site bị gỡ** (không phải tín dụng giả từ ca vô can). Giá của crash: traceback nuốt **toàn bộ** bảng PHẢN CHỨNG (0 dòng fixture in ra) — đúng phân tích F-18A: cửa `:231` là thứ đổi crash thành đỏ-có-kiểm-soát. Executor khai trung thực (`fixture_lot: false`, `expected_crash_caught: true` trong r19-door-mutants.json) — khớp phép đo của tôi từng mutant.

### Đ4 — MONOTONICITY BỘ 87 CŨ: chạy ĐỦ, không chỉ lập luận
Delta chỉ thêm dữ liệu fixture ⇒ về lý thuyết kill cũ bảo toàn; **vẫn chạy trọn** `EXECUTOR_MUTATION_METHOD.py.txt` nguyên văn (chỉ thay MỘT dòng neo E/R về scratch/clone) trên head r19: **KILLED 87/87, rc=0**; so per-mutant với `mutation-r17.json` của executor: killed **87/87 cả hai bên**, tập fixture-LỌT **BẰNG TỪNG TÊN 87/87**, đúng 1 ca `fixture_run_separate` (`powershell-known-subset`). Hệ quả kép: 4 fixture mới **không leak** dưới bất kỳ mutant cũ nào (cô lập hoàn toàn), và không mutant cũ nào mất kill.

### Đ5 — Chuỗi định danh + artifacts
sha256(`SPEC-r24.md`) = `79ba77c3…` **khớp** `spec_sha256`/`spec_hash` lease r24 và fence r19 · `PROMPT.md` ≡ `launcher/3bc4acc4/prompt.snapshot` (sha256 `c01627f4…`) · frozen-r19/fence khớp head/tree/base/master/953/2-path/675/4-door đối chiếu với phép đo của tôi · lease exec-6 thay exec-5 hai chiều (`thay_the_cho` + lý do thu hồi), authority comment 5657673695 của OWNER · A9/refset live: reviewer bị cấm mạng ⇒ **KHÔNG ĐO ĐƯỢC tại chỗ**, chỉ ghi nhận hiện vật (`unique_exec6_both`, 374 heads, comm rỗng) — đúng phạm vi.

### Đ6 — Bất biến cuối lượt
Sau toàn bộ phép đo: `status --porcelain` **rỗng**, HEAD/tree **không đổi** (đo lại sau khi viết xong thân verdict — xem BẢNG ĐO).

## ĐỐI CHIẾU LƯỢT TRƯỚC (R18 — verdict hợp lệ: changes_requested P1=0/P2=0/P3=1)

| finding R18 | trạng thái | bằng chứng TỰ ĐO (không nhận lời khai) |
|---|---|---|
| **F-18A** `ruff-fixture-thieu-rang-chot-moi`/cua-heredoc-va-do-sau-khong-rang [P3] — 4 cửa fail-close (`:208` depth>16 · `:231` escape-EOF · `:269` heredoc thứ hai · `:298` heredoc chưa đóng) 0-phủ fixture, mutant gỡ cửa sống 671/671 | **ĐÃ VÁ THẬT** | Đ1: delta đúng 4 fixture cô lập, một-cửa-một-fixture như hướng sửa R18 chỉ định (`$()`×17 thuần opaque · thân kết thúc `\` trần · hai heredoc một dòng · heredoc quoted không đóng), +4 dòng ≤ ước +8–14 của R18; Đ3: **4/4 mutant gỡ-cửa nay BỊ GIẾT**, 3 leak cô lập đúng tên + escape-EOF chết bằng crash quy kết được về đúng fixture; witness flip 2→0 tái lập cho cả 3 cửa fail-open; bộ door-mutant được giao dạng method chạy được (EXECUTOR_DOOR_MUTATION_METHOD) đúng yêu cầu "kèm 3–4 mutant cho lượt sau". KHÔNG phát hiện VÁ SINH LỖI MỚI trong phạm vi 4 cửa: 87/87 mutant cũ giữ nguyên kill + leak-set (Đ4), suite 675/675, witness HEAD vẫn đỏ đúng. *(Nhánh m-None còn lại của CÙNG dòng `:269` là lỗ RIÊNG chưa từng nêu trong F-18A — H5/F-19A dưới, không phải VÁ HỜ của F-18A vì F-18A chỉ định fixture theo THÔNG ĐIỆP cửa và mutant (c) của R18 nhắm đúng nhánh here-not-None.)* |

## BẢNG SĂN — 6 hướng MỚI độc lập (lớp 1: H1·H2 · lớp 2: H3·H4 · lớp 3: H5·H6)

Đối chiếu PRIOR_HUNT_INDEX R7–R18: không hướng nào trùng — H1 đo RỬA CHỨNG CHỈ qua 4 thân cửa MỚI trong job đầy đủ nghĩa vụ (R18-H6 đo vector quy kết của 8 họ CŨ); H2 đo kênh DỮ LIỆU heredoc vào màng membership `kiem()` (R18-H1 dùng `kiem()` làm backstop cho lookalike — câu hỏi ngược); H3 là sweep related-installer THEO TỪNG depth 1..17 (R18-H3 đo parity boundary↔inner, không sweep depth); H4 là tổ hợp TRẠNG THÁI-PENDING heredoc + quy kết cửa (R14-H5 đo biên NHẬN toán tử heredoc); H5 là răng THEO NHÁNH của cửa ghép `:269` (R18-H5 đo phủ theo THÔNG ĐIỆP — nhánh là tầng dưới thông điệp); H6 là răng NGƯỠNG hai chiều của cửa depth quanh fixture mới (R14-H6 là ngưỡng C0, mã khác cửa khác). Replay Đ2/Đ3/Đ4 không tính N. Script + JSON: `scratch/rv19/{rig_*.py, rv19-hunts.json, rv19-door-mutants-reviewer.json, m87/}`.

HƯỚNG H1 [LỚP 1]: cửa mới không rửa được chứng chỉ trong job đầy đủ nghĩa vụ
  giả thuyết : nếu một bước mang thân cửa (depth17/escape-EOF/second-heredoc/heredoc-unclosed) đứng cạnh bộ pin+probe+registry hợp lệ mà job vẫn xanh ở BẤT KỲ vị trí nào (trước pin/giữa/sau registry/cùng bước pin/job phụ) thì KPT bị rửa
  lệnh       : loi_ruff_ci trên 4 thân × 5 bố cục = 20 ca (rig_hunts.py H1)
  output     : 20/20 ĐỎ (2–3 lỗi); mọi ca đều đỏ CẢ pin-check (`không chứng minh ghim … ngoài miền cú pháp`) LẪN registry-check (`không provision`); `any_wrong_green: false`
  kết luận   : KHÔNG PHẢI LỖI — KPT thống trị ở mọi vị trí, -1 poison tiêu thụ đúng, không đường rửa chứng chỉ

HƯỚNG H2 [LỚP 1]: kênh DỮ LIỆU heredoc vs màng membership `kiem()`
  giả thuyết : nếu chuỗi lời gọi canonical nằm THUẦN trong thân heredoc (dữ liệu) mà thoả membership của `kiem()` thì check ấy data-blind; nếu đồng thời M7 xanh thì có wrong-green tổng
  lệnh       : kiem(workflows=heredoc-DOC chứa đủ 13 chuỗi DA_NOI) + loi_ruff_ci trên YAML chỉ có registry-line trong DOC (rig_h2fix_identity.py)
  output     : kiem missing = **[] — 13/13 thoả bằng dòng dữ liệu thuần**; nhưng loi_ruff_ci: `CI không provision Ruff trước test registry … KHÔNG CÓ` (đỏ); composite_red = true
  kết luận   : KHÔNG PHẢI LỖI cho packet — membership `kiem()` đúng là data-blind (substring trên mọi dòng kể cả thân heredoc) nhưng đó là hành vi NỀN có sẵn, ngoài write set, và cổng M7 fail-close độc lập nên không mở wrong-green tổng; GHI NHẬN cho sổ nợ nền (không tính finding packet)

HƯỚNG H3 [LỚP 2]: related-installer theo TỪNG depth 1..17
  giả thuyết : nếu tồn tại depth d ≤ 16 mà `pip install ruff` ở tầng trong cùng của `$(…)` lồng d tầng được KHONG-hoá thì đệ quy rửa nghĩa vụ installer ở tầng ấy
  lệnh       : loi_ruff_ci trên 17 thân `X=$(echo …$(pip install ruff)…)` d=1..17 + đối chứng thuần opaque d=16/17 (rig_hunts.py H3)
  output     : 17/17 ĐỎ (2 lỗi mỗi ca); opaque-16 = **0 lỗi** (nhận), opaque-17 = **2 lỗi** với quy kết đúng `ngoài miền cú pháp: ['gate/bước 2']`
  kết luận   : KHÔNG PHẢI LỖI — mệnh đề "related bị chặn ở mọi tầng đệ quy" mà F-18A tựa vào nay có phép đo đủ 17 điểm; biên 16/17 hành xử đúng công bố fail-close

HƯỚNG H4 [LỚP 2]: tổ hợp heredoc-pending + quy kết cửa
  giả thuyết : nếu một tổ hợp trạng thái-pending (hai heredoc hai lệnh một dòng; pending gặp EOF/escape-EOF; heredoc trong `$()`; delimiter biến/rỗng; đóng tại EOF; tab-đóng) làm HEAD crash hoặc nhận thân ngoài miền thì lexer hở ở lớp trạng thái
  lệnh       : loi_ruff_ci trên 8 probe + bash -n (parse-only) đối chứng 3 ca then chốt (rig_hunts.py H4)
  output     : 6/8 ĐỎ có kiểm soát (2 lỗi, KPT đúng bước); 2/8 NHẬN đúng (`cat <<'E'\nx\nE` đóng tại EOF và `<<-` tab-đóng — bash -n rc=0 cả hai); hai ca over-block (`cat <<'A'; cat <<'B'` tuần tự và `cat <<$X` delimiter biến) bash -n rc=0 nhưng consumer đỏ — chiều CHẶN
  kết luận   : KHÔNG PHẢI LỖI — không crash, không wrong-green trên HEAD; các divergence đều chiều chặn-oan an toàn đã công bố (heredoc động/tĩnh), chấp nhận đúng chỗ bash chấp nhận ở 2 ca dương

HƯỚNG H5 [LỚP 3]: răng THEO NHÁNH của cửa ghép `:269` — **LỖI (F-19A, P3)**
  giả thuyết : nếu không fixture nào đi qua nhánh `m is None` của `if m is None or here is not None: raise …` thì mutant thu hẹp cửa còn nhánh `here` sống trọn suite — đúng lớp "fixture bắt được mất chốt"
  lệnh       : mutant `if here is not None: raise …` (gỡ nhánh m-None), chạy TRỌN suite trên clone + witness A/B `cat <<$X\nx\n$X\n` qua chính loi_ruff_ci (rig_hunts.py H5)
  output     : mutant **SỐNG: rc=0, PHẢN CHỨNG 675/675, TỔNG ĐẠT, 0 LỌT**; witness: HEAD **2 lỗi có kiểm soát** (ValueError `heredoc ngoài miền`) → mutant **AttributeError: 'NoneType' object has no attribute 'end'** (crash không được bắt — `_doc_run_ruff` chỉ bắt ValueError)
  kết luận   : **LỖI** — nửa cửa m-None 0-phủ; mutant KHÔNG-tương-đương (failure-mode flip controlled→crash, cùng lớp với cửa escape-EOF trước r19) sống trọn lưới 675; chi tiết ở F-19A

HƯỚNG H6 [LỚP 3]: răng NGƯỠNG hai chiều của cửa depth quanh fixture mới
  giả thuyết : nếu widen (`>16`→`>17`) sống thì fixture depth-17 không neo đúng điểm từ chối tối thiểu; nếu narrow (`>1`/`>0`) sống thì phía NHẬN không có neo và siết lặng lẽ không ai thấy
  lệnh       : 3 mutant ngưỡng chạy trọn suite + witness depth-2 opaque A/B (rig_hunts.py H6)
  output     : widen-17 **BỊ GIẾT** (leak đúng duy nhất fixture depth-limit — fixture nằm ĐÚNG điểm 17 tối thiểu); narrow-1 **SỐNG** (675/675; witness depth-2 opaque: HEAD 0 → mutant 2 — chỉ đổi chiều CHẶN-OAN, đỏ ồn ào, không im lặng); narrow-0 **BỊ GIẾT bởi hợp đồng ci.yml THẬT** (RUFF CI 1/3 — `$()` depth-1 có thật trong workflow)
  kết luận   : KHÔNG PHẢI LỖI — chiều fail-open có răng tại điểm tối thiểu, chiều fail-close tự phơi bằng đỏ thật trên workflow thật; GHI NHẬN trục Spec: trần `16` không xuất hiện trong docstring công bố (chỉ ở chính dòng `:208`) — không nâng thành finding vì R18-H3 đã đo biên 16/17 và kết luận khớp câu "chỉ lệnh opaque được phân tích đệ quy" theo chiều CHẶN; ghi để lượt sau khỏi đo lại

## FINDING

### F-19A — `ruff-fixture-thieu-rang-chot-moi`  [P3]  (GIỮ stable slug R11/R15/R16/R18; sub-class MỚI: nua-cua-heredoc-m-None-khong-rang)
Nhánh `m is None` của cửa ghép heredoc `:269` không có răng fixture — mutant thu hẹp cửa còn nhánh `here` sống trọn 675/675, failure-mode đổi controlled→crash.
TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py:269` — `if m is None or here is not None: raise ValueError("heredoc ngoài miền")`. Một dòng, HAI ngữ nghĩa: (a) toán tử heredoc có delimiter NGOÀI grammar tag tĩnh (`m is None`), (b) heredoc THỨ HAI khi đang pending (`here is not None`).
VẤN ĐỀ + COUNTEREXAMPLE (đều ĐÃ CHẠY — H5): fixture mới `second-heredoc` (r19) chỉ đi qua nhánh (b); đo trọn suite dưới mutant giữ-nhánh-here: **675/675 xanh, rc=0** ⇒ không fixture nào đi qua nhánh (a). Mutant KHÔNG tương đương: witness `cat <<$X\nx\n$X\n` (bash -n rc=0 — bash nhận delimiter biến) trên HEAD bị từ chối CÓ KIỂM SOÁT (ValueError → KPT, 2 lỗi); dưới mutant thành **AttributeError crash không được bắt** tại `m.end()` — cùng lớp hỏng mà F-18A đã đếm cho cửa escape-EOF (không fail-open, nhưng đổi failure-mode thành traceback nuốt trọn bảng PHẢN CHỨNG như đã đo ở Đ3). Bộ door-mutant r19 của executor cũng không phủ: mutant `drop-second-heredoc` của họ thu hẹp về nhánh (a) — đúng chiều NGƯỢC LẠI, nên hai bên bù nhau vẫn hở nhánh (a).
VÌ SAO P3 (không phải P2): trên HEAD mọi witness bị từ chối đúng; khi nới cũng không mở đường cài ẩn (m-None crash ồn ào thay vì nhận); lỗ CHỈ ở độ mịn lưới cho hồi quy tương lai — đúng phép phân hạng R14/R15/R16/R18 đã dùng cho lớp này.
HƯỚNG SỬA CẤP LỚP (bằng lời, không patch — sensitive): một fixture âm mà CHỈ nhánh m-None chặn — thân có toán tử heredoc với delimiter hỏng grammar tag tĩnh (ví dụ lớp: ký tự mở đầu ngoài `[A-Za-z_]`), đặt trên bước shell mặc định như họ `syntax-*` hiện có; kèm một mutant dạng thu-hẹp-cửa-còn-nhánh-here vào bộ door-mutant lượt sau (mutant ấy đồng thời chốt failure-mode controlled-thay-vì-crash, như ca escape-EOF). Ước +1–2 dòng Python ⇒ 953→≤955 ≤ 1000, giữ đúng 2 path.
TEST/MUTANT GIỮ CHỐT: `scratch/rv19/hunt_door269_keep_here_branch.py` + `hunt_door269.txt` (suite trọn) + witness A/B trong `rv19-hunts.json` (khoá H5).
NGUY CƠ HỒI QUY: ≈0 — không đổi mã sản phẩm; HEAD đỏ đúng witness; fixture bổ sung sẽ xanh ngay trên HEAD.
ĐÃ THỬ VÁ: không — write set packet + sensitive (§8 loại trừ patch-as-hint cho bề mặt này).
ĐỘ TIN: cao — mutant sống đo bằng suite trọn, witness hai chiều, phương pháp trùng rig đã giết 87/87 + 4/4 (đối chứng rig không hiền).

## BẢNG ĐO — lời khai executor ↔ đo được (độc lập)

| khẳng định executor | đo được (reviewer) | khớp? |
|---|---|---|
| exact head/tree/base `27f0d305…`/`43a566b0…`/`bb7013c7…` | rev-parse đầu VÀ cuối lượt, porcelain 0 cả hai lần | Có |
| A8 953/1000, đúng 2 path | numstat 827+126=953, đúng 2 path | Có |
| delta r19 = 4 fixture cô lập | delta-r18.patch ≡ tự sinh (BYTE-IDENTICAL); đúng 4 dòng dữ liệu trong `_FX`, 0 đổi mã | Có |
| workflow byte-identical freeze `3bbc6b46` | blob `cb025a5a70…` tại cả 4 mốc | Có |
| registry 675/675 · 21/21 · 4/4 · 3/3 · rc=0 | tự chạy KHÔNG `--chay`: y hệt; output ≡ r19-targeted-registry.txt (681=681, modulo dòng `rc=0`) | Có |
| Ruff F rc=0 · actionlint rc=0 | All checks passed (ruff 0.15.15) · rc=0, 0 chẩn đoán (actionlint 1.7.7, shellcheck 0.9.0 CÓ MẶT) | Có |
| 4/4 door mutants killed (r19-door-mutants.json) | tái lập 4/4 với neo tự đặt; 3 leak cô lập đúng tên + TỔNG ĐỎ; escape-EOF chết bằng IndexError quy kết đúng fixture (479 lời gọi sạch trước crash) — khai `expected_crash_caught` trung thực | Có |
| bộ 87 cũ vẫn đứng (khai kế thừa) | chạy ĐỦ 87 theo method nguyên văn (chỉ thay neo): **87/87 killed**, leak-set **bằng từng tên** với mutation-r17.json, đúng 1 separate; 4 fixture mới không leak dưới mutant cũ nào | Có |
| "răng theo TỪNG cửa" (tiêu chí lớp 3 các lượt đặt ra) | **KHÔNG khớp trọn** — nhánh m-None của `:269` 0-phủ, mutant giữ-nhánh-here sống 675/675 với witness đã chạy (F-19A) | **KHÔNG — F-19A** |
| spec/prompt sha256 | SPEC-r24.md = `79ba77c3…` khớp lease+fence; PROMPT.md ≡ prompt.snapshot (`c01627f4…`) | Có |
| A1/A5/A2-conclusions/A6-readback/CI · integration master | not_run / not_measured theo chỉ thị — KHÔNG đọc thành passed/failed; không ngoại lệ merge | Đúng trạng thái |
| A9 live / refset (`unique_exec6_both`, fence audit=passed) | reviewer bị cấm mạng ⇒ KHÔNG ĐO ĐƯỢC tại chỗ; chỉ ghi nhận hiện vật lease/fence | Đúng phạm vi |
| cây review nguyên trạng | mọi đột biến/bản sao ở `scratch/rv19/*` tên riêng, ROOT ghim clone; porcelain 0 + HEAD/tree không đổi đo lại cuối lượt | Có |

## KẾT LUẬN THEO LỚP (trục Spec + Standards/Security cho từng lớp)

| lớp | verdict | căn cứ |
|---|---|---|
| 1. Installer/domain/invocation + job phụ | **approve** | Delta không đụng lớp nhận dạng (đo bằng diff, không nhận lời khai); H1: 20/20 bố cục cửa-mới × vị trí đều đỏ CẢ pin LẪN registry — không rửa chứng chỉ, không KHONG-hoá; H2: kênh dữ liệu heredoc không mở wrong-green tổng (M7 fail-close độc lập); Spec khớp Miền công khai M7; Security fail-close đủ |
| 2. Lexer/structure/expansion/order/shell carrier | **approve** | Delta 0 dòng mã lexer; H3: related-installer đỏ ở TRỌN 17 depth, biên 16/17 đúng công bố; H4: 8 tổ hợp pending-heredoc — không crash, không wrong-green, 2 ca nhận khớp bash -n, over-block đều chiều CHẶN đã công bố; witness mọi cửa trên HEAD đỏ có kiểm soát |
| 3. Consumer/spec/workflow/fixtures | **changes_requested** | Tiêu chí lớp ("fixture bắt được mất chốt") đo ra **F-19A [P3]**: nhánh m-None của cửa ghép `:269` 0-phủ, mutant thu hẹp KHÔNG-tương-đương (failure-mode controlled→crash) sống trọn 675/675 với witness đã chạy; phần còn lại SẠCH: F-18A ĐÃ VÁ THẬT (4/4 door-mutant giết, leak cô lập, failure-mode escape-EOF quy kết đúng), 87/87 mutant cũ tái lập leak-set bằng từng tên, H6 ngưỡng depth có răng chiều fail-open, A8/byte-identity/Ruff/actionlint/đếm-675 khớp trọn |

## KẾT LUẬN CUỐI (hai dòng đầu tệp là canonical và ĐÃ CHỐT — không còn là placeholder)

**verdict: changes_requested** · reviewed_sha `27f0d3054ee02e0584d00d750888737eac40585a` · **P1=0 · P2=0 · P3=1** (F-19A, stable slug `ruff-fixture-thieu-rang-chot-moi`, sub-class mới `nua-cua-heredoc-m-None-khong-rang`).
Tổng approve đòi CẢ BA lớp approve — lớp 3 chưa đạt. Điều kiện dừng của spec đòi approve tường minh; theo chuỗi R15→R16→R18, khuôn FIXTURE/MUTANT-KHOÁ đã áp tới cửa thứ tư và chỉ còn nửa-nhánh này trong họ cửa POSIX-lexer mà bản đồ nhánh của tôi thấy. Không merge/land; integration master not_measured; CI/A1/A5 not_run theo chỉ thị.
