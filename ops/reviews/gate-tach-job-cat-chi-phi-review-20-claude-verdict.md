verdict: changes_requested
reviewed_sha: b881c6d1acd481925ef96c05fb9109e95df340fe

# VERDICT — #463 lượt review 20 (revision24/generation5, sensitive) — REVIEWER CLAUDE độc lập

reviewer: anthropic_claude / claude-fable-5 / max / claude_code / machine-local — context/clone mới, độc lập executor
packet: GATE-TACH-JOB-CAT-CHI-PHI (#463), mission #467 · base `bb7013c7669da19304a8769e5b25f8c1f8951e9c`
tree (mong đợi = đo): `6b9724305365eb806dc48e65320435f1e7159064` — KHỚP · clone detached, porcelain 0 dòng (đo đầu VÀ cuối lượt)
CI/A1/A5: **not_run** theo chỉ thị chủ kho · integration với master `c16bd329…`: **not_measured** · không mạng/GitHub/dispatch/merge
Công cụ: Python 3.13.1 (`C:\Python313`) · ruff 0.15.15 (`D:\chocolatey\bin\ruff.exe`) · actionlint 1.7.7 + shellcheck 0.9.0 CÓ MẶT · git · bash CHỈ `-n` (parse-only, `C:\Program Files\Git\bin\bash.exe`) · KHÔNG thực thi fixture/installer · mọi đột biến/bản sao nằm `scratch/rv20/`, clone READ-ONLY

## Nhật ký đo

### Đ0 — Identity clone
`rev-parse HEAD` = `b881c6d1…` (đầu + cuối lượt) · `HEAD^{tree}` = `6b972430…` · `HEAD~1` = `27f0d305…` (đúng head R19) · `status --porcelain` rỗng cả hai lần · detached.

### Đ1 — A8 + delta + freeze workflow (tự đo, không nhận artifact)
- `git diff --numstat base..head`: `.claude/dev/ci_dang_ky_test.py` **828**, `.github/workflows/ci.yml` **126** ⇒ additions **954 ≤ 1000**, đúng **2 path** (khớp frozen-r20).
- `delta-r19.patch` ≡ tự sinh `git -c core.abbrev=7 diff 27f0d305..b881c6d1`: **BYTE-IDENTICAL**; `diff.patch` ≡ tự sinh base..head cùng cách: **BYTE-IDENTICAL**. *(Điều kiện đo khai kèm: clone của tôi `core.abbrev` unset ⇒ dòng `index` 8 ký tự lệch 7; ép `-c core.abbrev=7` — đúng chốt SKILL.md — thì trùng từng byte. Không phải lệch nội dung.)*
- Delta r19→r20 = **đúng 1 dòng dữ liệu fixture**: `("heredoc-dynamic-delimiter", "cat <<$X\nx\n$X\n", 1)` chèn vào họ `syntax-*` trong `_FX`; **0 dòng xoá, 0 đổi mã** guard/lexer/harness/workflow.
- Workflow byte-identical: blob `ci.yml` = `cb025a5a70…` tại **cả bốn** mốc HEAD / `27f0d305`(r19) / `ff146f16`(r16) / `3bbc6b46`(freeze).

### Đ2 — Baseline suite + Ruff + actionlint (clone, KHÔNG `--chay`, KHÔNG CI)
Chạy `python -X utf8 -B .claude/dev/ci_dang_ky_test.py` cwd=clone: **rc=0 · ĐĂNG KÝ 21/21 · LAUNCHER WINDOWS 4/4 · RUFF CI 3/3 · PHẢN CHỨNG 676/676 · TỔNG: ĐẠT** · **676 tên phân biệt, 0 trùng** · fixture mới `ruff-ci-syntax-heredoc-dynamic-delimiter` CÓ MẶT, 0 dòng LỌT.
Output của tôi ≡ `r20-targeted-registry.txt` **từng dòng (682=682)**, executor chỉ thừa đúng một dòng `rc=0` cuối.
Ruff `check --no-cache --select F` trên tệp Python đổi: **All checks passed, rc=0**. actionlint trên `ci.yml`: **rc=0, 0 chẩn đoán** (`-format {{json .}}`; shellcheck 0.9.0 CÓ MẶT — điều kiện đo khai kèm).

### Đ3 — TÁI LẬP 5 DOOR-MUTANT (4 của r19 + keep-here của r20; EXECUTOR_DOOR_MUTATION_METHOD, neo TỰ ĐẶT về clone)
| mutant | rc | fixture LỌT | cô lập? | witness A/B (HEAD→mutant) |
|---|---|---|---|---|
| drop-depth-guard | 1 | đúng `…depth-limit` | CÓ | `$(echo…)`×17: **2→0** |
| drop-heredoc-unclosed | 1 | đúng `…heredoc-unclosed` | CÓ | `cat <<'E'\nx\n`: **2→0** |
| drop-second-heredoc | 1 | đúng `…second-heredoc` | CÓ — fixture MỚI **không** LỌT (nhánh m-None giữ) | `cat <<'A' <<'B'…`: **2→0** |
| drop-escape-eof | 1 | (crash) | — | `echo hi\`: **2→IndexError** |
| **keep-here-r20** | **1** | (crash) | — | `cat <<$X…`: **2→AttributeError `'NoneType' object has no attribute 'end'`** |

**Quy kết crash (nghĩa vụ riêng):** patch `__globals__` đếm lời gọi `loi_ruff_ci` — drop-escape-eof: **479** lời gọi sạch rồi crash đúng nguồn chứa `echo hi\` (y hệt số R19); **keep-here-r20: 481 lời gọi sạch rồi crash đúng nguồn chứa `cat <<$X`** — tức chính fixture MỚI kích crash tại đúng site bị thu hẹp, không phải tín dụng giả từ ca vô can. Khớp `r20-mutant.json` (`rc:1, attribute_error:true, killed:true`). Giá của crash giữ nguyên phân tích F-18A/F-19A: traceback nuốt trọn bảng PHẢN CHỨNG — cửa `m is None` trên HEAD là thứ đổi crash thành đỏ-có-kiểm-soát, và HEAD đỏ đúng witness (2 lỗi ValueError kiểm soát).

### Đ4 — BỘ 87 MUTANT CŨ: chạy ĐỦ, không chỉ monotonicity
`EXECUTOR_MUTATION_METHOD.py.txt` nguyên văn (CHỈ thay một dòng neo E/R về scratch/clone) trên head r20: **KILLED 87/87, rc=0 của runner**; so per-mutant với `mutation-r17.json`: killed **87/87 cả hai bên**, tập fixture-LỌT **BẰNG TỪNG TÊN 87/87, 0 lệch**, đúng 1 ca `fixture_run_separate` (`powershell-known-subset`). Fixture mới **không leak dưới bất kỳ mutant cũ nào** (cô lập hoàn toàn); không mutant cũ nào mất kill.

### Đ5 — Chuỗi định danh + artifacts
sha256(`SPEC-r24.md`) = `79ba77c3…` **khớp** `spec_sha256`/`spec_hash` lease r24 · `PROMPT.md` ≡ `launcher/ca221175/prompt.snapshot` (sha256 `57d35fb9…`) · frozen-r20/fence khớp head/tree/base/954/2-path/676/1-mutant với phép đo của tôi · `cross-review-SKILL.md` gói review là **adapter Codex** trỏ về `.claude/skills/cross-review/SKILL.md` (adapter Claude Code) trong cây — khác nhau THEO THIẾT KẾ, không phải lệch đồng bộ · `evidence_head e7ab8b9b…`/`refset_sha256`/A9 live: reviewer bị cấm mạng ⇒ **KHÔNG ĐO ĐƯỢC tại chỗ**, chỉ ghi nhận hiện vật lease/fence (`unique_exec6_both`, audit=passed) — đúng phạm vi.

### Đ6 — Bất biến cuối lượt
Sau toàn bộ phép đo: `status --porcelain` **rỗng**, HEAD/tree **không đổi** (`b881c6d1…`/`6b972430…` đo lại trước khi chốt verdict). Mọi tệp sinh ra nằm `scratch/rv20/` ngoài clone.

## ĐỐI CHIẾU LƯỢT TRƯỚC (R19 — verdict hợp lệ: changes_requested P1=0/P2=0/P3=1)

| finding R19 | trạng thái | bằng chứng TỰ ĐO (không nhận lời khai) |
|---|---|---|
| **F-19A** `ruff-fixture-thieu-rang-chot-moi`/nua-cua-heredoc-m-None-khong-rang [P3] — nhánh `m is None` của cửa ghép `:269` 0-phủ, mutant giữ-nhánh-here sống 675/675 | **ĐÃ VÁ THẬT** | Đ1: delta đúng 1 fixture đúng hướng sửa R19 chỉ định (delimiter mở đầu `$` ∉ `[A-Za-z_]`, đặt trên bước shell mặc định họ `syntax-*`, +1 dòng ≤ ước +1–2, 954 ≤ 1000); Đ3: mutant thu-hẹp-cửa-còn-nhánh-here **BỊ GIẾT**, crash AttributeError **quy kết đúng fixture mới** (481 lời gọi sạch); H6: mutant NỚI grammar tag nhận `$` bị giết với leak **cô lập đúng duy nhất** fixture mới ⇒ fixture neo ĐÚNG điểm từ chối tối thiểu; Đ4: 87/87 giữ kill + leak-set bằng từng tên, suite 676/676 — KHÔNG VÁ SINH LỖI MỚI trong phạm vi cửa `:269`. |

## BẢNG SĂN — 6 hướng MỚI độc lập (lớp 1: H1·H2 · lớp 2: H3·H4 · lớp 3: H5·H6)

Đối chiếu PRIOR_HUNT_INDEX R7–R19: không hướng nào trùng — H1 đo ĐÚC CHỨNG CHỈ pin/probe từ DÒNG DỮ LIỆU thân heredoc qua chính `loi_ruff_ci` (R19-H2 đo membership `kiem()` + registry-line, không đo phía đúc pin); H2 đo RESUME nghĩa vụ SAU terminator + quy kết caller/poison qua data (chưa lượt nào đo); H3 đo cửa `:297` trước phép NỐI DÒNG `\<newline>` TRONG thân heredoc không quote (R19-H4 đo tổ hợp pending/delimiter, không đo biểu diễn tương đương của nội dung thân); H4 là lưới quote-form × tail của TAG quanh cửa `:270` (R14-H5/R19-H6 đo herestring/tab/ngưỡng depth, không đo lưới này); H5 là bản đồ răng theo TỪNG VẾ DISJUNCT trên mọi điều kiện ghép của lexer (R18-H5 đo theo RAISE-SITE, R19-H5 chỉ tách vế của `:269`); H6 là răng NGƯỠNG GRAMMAR tag hai chiều quanh fixture mới (R19-H6 là ngưỡng depth — cửa khác, trục khác). Replay Đ2/Đ3/Đ4 không tính N. Script + JSON: `scratch/rv20/{rig_*.py, h12.json, h34.json, h56.json, d3-doors.json, m87/}`.

HƯỚNG H1 [LỚP 1]: chứng chỉ pin/probe không được đúc từ THÂN heredoc (dữ liệu)
  giả thuyết : nếu dòng `python -m pip install --quiet ruff==0.15.15` + `ruff --version` nằm THUẦN trong thân heredoc (quoted/unquoted/`<<-`) mà job không có pin thật vẫn xanh thì chứng chỉ được đúc từ dữ liệu
  lệnh       : loi_ruff_ci trên 3 biến thể thân + 1 đối chứng pin-thật-kèm-data (rig_h12.py H1)
  output     : 3/3 ca thân-mang-pin ĐỎ đủ CẢ BA lỗi (`không chứng minh ghim … không job nào cài` · `không in probe` · `không provision`); đối chứng pin thật + data 0.15.15 trong thân: **0 lỗi** — data không đúc, không poison
  kết luận   : KHÔNG PHẢI LỖI — thân heredoc là dữ liệu ở cả ba dạng delimiter, không đường đúc GHIM/probe từ data

HƯỚNG H2 [LỚP 1]: nghĩa vụ RESUME sau terminator + quy kết registry qua data
  giả thuyết : nếu lexer không thoát body-mode đúng tại terminator thì pin/probe/registry đặt SAU heredoc bị mù (over-block) hoặc dòng registry trong thân sinh caller/poison ma (wrong-green/đỏ oan)
  lệnh       : loi_ruff_ci trên 5 bố cục: pin+probe sau terminator · registry CHỈ trong thân · registry trong thân + thật · `ci_dang_ky_test.py` không `--chay` trong thân · terminator lặp (rig_h12.py H2)
  output     : pin+probe sau terminator **0 lỗi** (resume chính xác); registry chỉ-trong-thân ⇒ đúng 1 lỗi `test registry: KHÔNG CÓ` (data không thành bước); registry thân+thật ⇒ **0 lỗi** (không caller ma); dạng không-`--chay` trong thân ⇒ **0 lỗi** (vị từ −1 không bị data kích); ca terminator-lặp: dòng `E` thứ hai được parse như LỆNH unknown ⇒ KPT đỏ — kỳ vọng ban đầu của rig tôi ghi `==0` là SAI (đã đính chính trong h12.json), hành vi sản phẩm ĐÚNG fail-close whitelist và chứng minh thêm resume về command-mode
  kết luận   : KHÔNG PHẢI LỖI — ranh giới data/lệnh đóng cả hai chiều tại terminator

HƯỚNG H3 [LỚP 2]: cửa `:297` dò substring THEO DÒNG — nối dòng `\<newline>` trong thân heredoc KHÔNG quote tái tạo `$(` — **LỖI (F-20A, P2)**
  giả thuyết : nếu `$(`/backtick bị dò theo từng dòng vật lý thì `$\` cuối dòng + `(…)` đầu dòng sau (POSIX join thành `$(…)` khi thân không quote) lách được cửa
  lệnh       : loi_ruff_ci trên job phụ (đúng khuôn fixture `heredoc-dong` want=1) với 6 thân; bash -n đối chứng (rig_h34.py H3)
  output     : unsplit `cat <<END\n$(pip install ruff)\nEND` ⇒ **3 lỗi** (đỏ, đúng fixture); **SPLIT `cat <<END\nx $\⏎(pip install ruff)\nEND` ⇒ 0 lỗi — XANH**; split-kép ⇒ 0 lỗi; `$\⏎((1+1))` ⇒ 0 lỗi; backtick (1 ký tự, không tách được) ⇒ đỏ; thân QUOTED chứa split ⇒ 0 lỗi (đúng — không expansion); bash -n rc=0 mọi ca (phân biệt nằm ở tầng expansion, không ở parse)
  kết luận   : **LỖI** — biểu diễn tương đương POSIX của đúng nội dung mà cửa `:297` + fixture `heredoc-dong` tuyên bố PHẢI ĐỎ được cấp chứng chỉ xanh; chi tiết F-20A

HƯỚNG H4 [LỚP 2]: lưới biên TAG heredoc (quote-form × tail) quanh cửa `:270` so bash -n
  giả thuyết : nếu grammar tag match TIỀN TỐ hoặc nhận nhầm dạng quote thì delimiter thật của bash khác delimiter của consumer ⇒ wrong-green hoặc kết thúc thân sai chỗ
  lệnh       : loi_ruff_ci + bash -n trên 13 ca: `<< E` · `<<-E` · `<<-$X` · `<<1X` · `<<E-F` · `<<'E F'` · `<<\E` · `<<"E"` · `<<E<in` · `<<E >out` · `<<E;wc` · `<<''` · `<<E'x'` (rig_h34.py H4)
  output     : 6 ca NHẬN đều là delimiter tĩnh bash-tương-đương (space-trước-tag, tab-đóng, `"E"` quoted, redirect/`;` sau tag — cửa `:270` cho qua đúng tập ` \t\n;&|<>`); 7 ca ĐỎ đều 3 lỗi KPT đúng bước — gồm `<<-$X` (động, PHẢI đỏ) và 6 ca bash-hợp-lệ nhưng ngoài grammar tag tĩnh công bố (`1X`, `E-F`, `'E F'`, `\E`, `''`, `E'x'`) — toàn bộ chiều CHẶN-OAN; **0 ca nhận thứ bash coi là động/khác-delimiter**
  kết luận   : KHÔNG PHẢI LỖI — không match-tiền-tố (cửa `:270` chặn tail), mọi divergence đúng chiều chặn đã công bố

HƯỚNG H5 [LỚP 3]: bản đồ răng theo TỪNG VẾ DISJUNCT của các cửa lexer — **LỖI (F-20B, P3)**
  giả thuyết : nếu một VẾ của điều kiện ghép (`or`) không có fixture đi qua thì mutant thu-hẹp-còn-vế-kia sống trọn suite — đúng lớp F-19A vừa đóng cho `:269`, hỏi cho MỌI cửa còn lại
  lệnh       : 10 mutant thu hẹp/gỡ theo vế trên `:297`/`:306`/`:241`/`:282`/`:270`, mỗi mutant chạy TRỌN suite + witness A/B (rig_h56.py H5)
  output     : **m297-keep-dollar (gỡ vế backtick) SỐNG 676/676**, witness `cat <<E\n`x`\nE` HEAD 2→mutant **0** (fail-open flip); **m306-keep-quote (gỡ vế here) SỐNG 676/676**, witness `cat <<'E'` (EOF không newline) HEAD 2→mutant **0** (fail-open flip); m297-keep-backtick BỊ GIẾT (leak đúng `heredoc-dong`); m241 cả hai vế BỊ GIẾT (leak đúng họ `guard-expansion-outside`); m282-keep-len BỊ GIẾT (3 fixture boundary), m282-keep-set BỊ GIẾT bằng IndexError; m270-drop BỊ GIẾT (leak đúng `heredoc-delimiter-ghep` — replay bộ 87); m306-keep-here SỐNG nhưng witness KHÔNG flip (2→2: shlex tự ném "No closing quotation" — vế `quote` là áo giáp TRÙNG, mutant TƯƠNG ĐƯƠNG, không phải lỗ); m297-drop-notquoted SỐNG với flip 0→2 chiều CHẶN-OAN (ghi nhận, không finding — đúng tiền lệ narrow-survivor R19-H6)
  kết luận   : **LỖI** — hai vế fail-close 0-phủ còn lại (`:297`-backtick, `:306`-here), cả hai mutant KHÔNG-tương-đương sống trọn lưới với witness fail-open đã chạy; chi tiết F-20B. Kết quả này ĐÍNH CHÍNH câu R19 *"chỉ còn nửa-nhánh `:269` trong họ cửa POSIX-lexer mà bản đồ nhánh của tôi thấy"* — bản đồ ấy chưa xuống tới mức VẾ của `:297`/`:306`

HƯỚNG H6 [LỚP 3]: răng NGƯỠNG GRAMMAR tag hai chiều quanh fixture mới
  giả thuyết : nếu mutant NỚI grammar tag nhận `$` mà sống thì fixture mới không neo điểm từ chối; nếu mutant SIẾT (chỉ HOA) sống thì phía NHẬN không neo và cần biết chiều flip
  lệnh       : 2 mutant regex tag chạy trọn suite + witness + loi_ruff_ci trên ci.yml THẬT (rig_h56.py H6)
  output     : widen-`$` **BỊ GIẾT**, leak **đúng duy nhất** `ruff-ci-syntax-heredoc-dynamic-delimiter` (fixture mới nằm ĐÚNG điểm biên); narrow-HOA **SỐNG 676/676** — witness `cat <<'eof'…` HEAD 0→mutant 2 (chỉ đổi chiều CHẶN-OAN, đỏ ồn ào) và ci.yml THẬT vẫn 0 lỗi (3 heredoc thật của ci.yml đều `<<'PY'` HOA-quoted)
  kết luận   : KHÔNG PHẢI LỖI — chiều fail-open có răng tại điểm tối thiểu nhờ chính fixture mới; chiều siết tự phơi bằng đỏ; GHI NHẬN: phía NHẬN của tag chưa có fixture dương delimiter thường (mọi delimiter fixture hiện là HOA) — cùng dạng ghi nhận R19-H6, không nâng finding

## FINDING

### F-20A — `ruff-khuon-chua-chung-minh-provisioning`  [P2]  (GIỮ stable slug R10/R13/R14/R15 — sub-class MỚI: heredoc-body-continuation-join, không reset lịch sử)
Cửa `:297` dò `$(`/backtick theo TỪNG DÒNG VẬT LÝ của thân heredoc không quote, trong khi POSIX nối `\<newline>` TRƯỚC khi expansion — nội dung mà chính cửa này và fixture `heredoc-la-du-lieu`/`heredoc-dong` tuyên bố phải đỏ được cấp chứng chỉ xanh qua một biểu diễn tương đương.
TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py:296-297` — vòng tiêu thụ thân heredoc: `if not quoted and ("$(" in line or "`" in line): raise ValueError("heredoc có command substitution ngoài miền")`, với `line` là từng dòng vật lý cắt bằng `find("\n")`.
VẤN ĐỀ + COUNTEREXAMPLE (ĐÃ CHẠY — H3): trên job phụ đúng khuôn fixture `heredoc-dong` (gate đủ pin+registry): thân `cat <<END\n$(pip install ruff)\nEND\n` ⇒ **3 lỗi** (đỏ — đúng hợp đồng hiện có); thân `cat <<END\nx $\⏎(pip install ruff)\nEND\n` ⇒ **0 lỗi — cả workflow XANH**. POSIX XCU §2.7.4: thân here-document KHÔNG quote được expansion, backslash hành xử như trong nháy kép ⇒ §2.2.3: `\<newline>` bị loại (nối dòng) ⇒ hai thân trên là MỘT nội dung `$(pip install ruff)` khi CI chạy thật — một lệnh cài RELATED không ghim được thực thi lúc runtime trong khi consumer chứng nhận xanh. Cùng lách được với `$\⏎((…))` (arithmetic chứa `$((`). Backtick KHÔNG lách được (1 ký tự, dò theo dòng vẫn trúng — đối chứng đã chạy); thân QUOTED không expansion nên nhận là ĐÚNG (đối chứng đã chạy); bash -n rc=0 cả hai vế — tầng phân biệt là expansion, không phải parse.
VÌ SAO P2 (không phải P3/P1): đúng tiền lệ phân hạng của chuỗi này (R13-ADD/R14-ADD): **thân ngoài-miền-phải-đỏ được KHONG-hoá trên HEAD** — không phải lỗ lưới mutant mà là hành vi HEAD; SPEC *Miền công khai* đòi "dạng liên quan ngoài miền phải bị từ chối" và đây là dòng khai TRỰC TIẾP trong YAML (không thuộc ngoại lệ script/`python -c`/env). Không phải P1 vì không chứng chỉ GHIM/probe/registry nào bị đúc sai (H1/H2 đo sạch) — lỗ CHỈ mở đường một bước data-carrier được nhận trong khi nội dung sẽ chạy lệnh liên quan; kẻ ghi được YAML vẫn phải qua các cổng khác của kho.
HƯỚNG SỬA CẤP LỚP (bằng lời, không patch — sensitive): quét thân heredoc không quote trên BẢN ĐÃ CHUẨN HOÁ theo đúng luật POSIX của lớp đó (nối `\<newline>` trước khi dò), hoặc đảo sang chiều CHẶN đã dùng ở nơi khác của tệp: dòng thân không-quote kết thúc bằng backslash là ngoài miền (fail-close, chặn-oan có công bố). Kèm fixture âm cho chính cặp split/twin và mutant "quay lại dò theo dòng vật lý" để khoá cửa; ước +2–4 dòng ⇒ 954→≤958 ≤ 1000, giữ đúng 2 path.
TEST/MUTANT GIỮ CHỐT: `scratch/rv20/rig_h34.py` (H3) + `h34.json`; cặp witness split/unsplit ở trên là cặp fixture-âm/đối-chứng chạy được.
NGUY CƠ HỒI QUY của hướng sửa: thấp — chiều chuẩn hoá chỉ THU HẸP tập được nhận (twin của thứ đang đỏ thành đỏ); 3 heredoc thật trong `ci.yml` đều quoted `<<'PY'` nên không đổi màu RUFF CI 3/3 (đã đo dưới mutant siết ở H6).
ĐÃ THỬ VÁ: không — write set packet + sensitive (§8 loại trừ patch-as-hint cho bề mặt này).
ĐỘ TIN: cao — A/B hai chiều trên HEAD, đối chứng backtick/quoted/bash -n đủ, căn cứ POSIX nguyên văn.

### F-20B — `ruff-fixture-thieu-rang-chot-moi`  [P3]  (GIỮ stable slug R11/R15/R16/R18/R19 — sub-class MỚI: nua-cua-297-backtick-va-306-here-khong-rang)
Hai VẾ fail-close còn 0-phủ fixture: vế backtick của cửa `:297` và vế `here` của cửa `:306` — mutant thu-hẹp-còn-vế-kia sống trọn 676/676 với witness fail-open đã chạy.
TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py:297` (`"$(" in line or "`" in line` — vế sau 0-phủ) và `:306` (`if quote or here: raise ValueError("trích dẫn chưa đóng")` — vế `here` 0-phủ).
VẤN ĐỀ + COUNTEREXAMPLE (đều ĐÃ CHẠY — H5): (a) mutant giữ-`$(`-bỏ-backtick: **SỐNG rc=0, 676/676, TỔNG ĐẠT**; witness `cat <<E\n`x`\nE\n` (backtick trần trong thân không quote) HEAD **2 lỗi kiểm soát** → mutant **0 lỗi** — fail-open thật, không phải crash; (b) mutant giữ-`quote`-bỏ-`here`: **SỐNG 676/676**; witness `cat <<'E'` (heredoc treo tại EOF, KHÔNG newline cuối) HEAD **2 lỗi** → mutant **0 lỗi** — cặp đôi của fixture `heredoc-unclosed` (`cat <<'E'\nx\n` — CÓ newline, đi cửa `:298`, đã có răng) nhưng nhánh EOF-không-newline đi cửa `:306` và không fixture nào chạm. Vế `quote` của `:306` NGƯỢC LẠI là áo giáp trùng (shlex tự ném) — mutant bỏ nó TƯƠNG ĐƯƠNG, không cần fixture; khai để lượt sau khỏi đo lại.
VÌ SAO P3 (không phải P2): trên HEAD cả hai witness bị từ chối đúng, có kiểm soát; lỗ CHỈ ở độ mịn lưới cho hồi quy tương lai — đúng phép phân hạng F-18A/F-19A cho lớp này. (Vế backtick là hàng xóm của F-20A nhưng KHÁC lớp: F-20A là hành vi HEAD, F-20B là răng lưới.)
HƯỚNG SỬA CẤP LỚP (bằng lời, không patch — sensitive): mỗi vế một fixture âm trên đúng bước shell mặc định họ `syntax-*` hiện có — một thân heredoc không quote chứa backtick trần, một thân kết thúc bằng heredoc treo không newline cuối; kèm hai mutant dạng thu-hẹp-còn-vế-kia vào bộ door-mutant lượt sau. Nếu thi công CÙNG bản vá F-20A thì fixture vế backtick nhắm bản quét ĐÃ chuẩn hoá. Ước +2 dòng ⇒ trong trần A8, giữ 2 path.
TEST/MUTANT GIỮ CHỐT: `scratch/rv20/rig_h56.py` + `h56.json` + `scratch/rv20/disjunct/*` (suite trọn từng mutant).
NGUY CƠ HỒI QUY: ≈0 — không đổi mã sản phẩm; HEAD đỏ đúng cả hai witness; fixture bổ sung xanh ngay trên HEAD.
ĐÃ THỬ VÁ: không — sensitive.
ĐỘ TIN: cao — mutant sống đo bằng suite trọn, witness hai chiều, cùng rig đã giết 87/87 + 5/5 (đối chứng rig không hiền).

## BẢNG ĐO — lời khai executor ↔ đo được (độc lập)

| khẳng định executor | đo được (reviewer) | khớp? |
|---|---|---|
| exact head/tree/base `b881c6d1…`/`6b972430…`/`bb7013c7…` | rev-parse đầu VÀ cuối lượt, porcelain 0 cả hai lần; HEAD~1 = head R19 | Có |
| A8 954/1000, đúng 2 path | numstat 828+126=954, đúng 2 path | Có |
| delta r20 = 1 fixture heredoc-dynamic-delimiter | delta-r19.patch ≡ tự sinh (BYTE-IDENTICAL với core.abbrev=7); đúng 1 dòng dữ liệu trong `_FX`, 0 đổi mã | Có |
| workflow unchanged (freeze `3bbc6b46`) | blob `cb025a5a70…` tại cả 4 mốc | Có |
| registry 676/676 · 21/21 · 4/4 · 3/3 · rc=0 | tự chạy KHÔNG `--chay`: y hệt; output ≡ r20-targeted-registry.txt (682=682, modulo dòng `rc=0`); 676 tên phân biệt | Có |
| Ruff F rc=0 · actionlint rc=0 | All checks passed (ruff 0.15.15) · rc=0, 0 chẩn đoán (actionlint 1.7.7, shellcheck 0.9.0 CÓ MẶT) | Có |
| mutant keep-here 1/1 killed, `attribute_error:true` (r20-mutant.json) | tái lập: rc=1, AttributeError `m.end()`, quy kết 481 lời gọi sạch → crash đúng fixture mới; 4 door-mutant r19 giữ nguyên kill + leak cô lập | Có |
| bộ 87 cũ vẫn đứng | chạy ĐỦ 87 theo method nguyên văn (chỉ thay neo): **87/87 killed**, leak-set **bằng từng tên 87/87**, đúng 1 separate; fixture mới không leak dưới mutant cũ nào | Có |
| "răng theo TỪNG cửa/TỪNG VẾ" (tiêu chí lớp 3 các lượt đặt ra) | **KHÔNG khớp trọn** — vế backtick `:297` và vế here `:306` 0-phủ, hai mutant thu hẹp KHÔNG-tương-đương sống 676/676 (F-20B) | **KHÔNG — F-20B** |
| miền công khai M7 "dạng liên quan ngoài miền phải bị từ chối" | **KHÔNG khớp trọn** — twin nối-dòng của `$(pip install ruff)` trong thân heredoc không quote được nhận 0 lỗi trên HEAD (F-20A) | **KHÔNG — F-20A** |
| spec/prompt sha256 | SPEC-r24.md = `79ba77c3…` khớp lease r24; PROMPT.md ≡ prompt.snapshot (`57d35fb9…`) | Có |
| A1/A5/A2-conclusions/A6-readback/CI · integration master `c16bd329…` | not_run / not_measured theo chỉ thị — KHÔNG đọc thành passed/failed; không ngoại lệ merge | Đúng trạng thái |
| A9 live / refset / evidence_head (`unique_exec6_both`, fence audit=passed, `e7ab8b9b…`) | reviewer bị cấm mạng ⇒ KHÔNG ĐO ĐƯỢC tại chỗ; chỉ ghi nhận hiện vật lease/fence | Đúng phạm vi |
| cây review nguyên trạng | mọi đột biến/bản sao ở `scratch/rv20/*` tên riêng, ROOT ghim clone; porcelain 0 + HEAD/tree không đổi đo lại cuối lượt | Có |

## KẾT LUẬN THEO LỚP (trục Spec + Standards/Security cho từng lớp)

| lớp | verdict | căn cứ |
|---|---|---|
| 1. Installer/domain/invocation + job phụ | **approve** | Delta không đụng lớp nhận dạng (đo bằng diff); H1: không đường đúc GHIM/probe từ dữ liệu thân heredoc ở cả 3 dạng delimiter, đối chứng dương giữ 0 lỗi; H2: resume nghĩa vụ chính xác tại terminator, data không sinh caller/poison ma, unknown-sau-terminator fail-close đúng whitelist; Spec khớp Miền công khai M7 ở phía chứng chỉ; Security fail-close đủ ở lớp này |
| 2. Lexer/structure/expansion/order/shell carrier | **changes_requested** | **F-20A [P2]**: cửa `:297` dò theo dòng vật lý — twin nối-dòng POSIX của `$(pip install ruff)` trong thân heredoc không quote được nhận 0 lỗi trên HEAD trong khi twin unsplit đỏ 3 lỗi (A/B + đối chứng backtick/quoted/bash -n đã chạy); phần còn lại của lớp SẠCH: H4 lưới 13 ca biên tag — 0 wrong-green, mọi lệch chiều chặn đã công bố, cửa `:270` chặn đúng tail |
| 3. Consumer/spec/workflow/fixtures | **changes_requested** | Tiêu chí lớp ("fixture bắt được mất chốt", nay xuống mức VẾ) đo ra **F-20B [P3]**: hai vế `:297`-backtick · `:306`-here 0-phủ, mutant sống trọn 676/676 với witness fail-open; phần còn lại SẠCH: F-19A ĐÃ VÁ THẬT (mutant keep-here giết + quy kết đúng fixture mới, widen-tag giết với leak cô lập — fixture neo đúng biên), 87/87 + 5/5 door tái lập leak-set bằng từng tên, fixture mới cô lập hoàn toàn, A8/byte-identity/Ruff/actionlint/đếm-676 khớp trọn, m306-vế-quote chứng minh tương đương (không đòi fixture) |

## KẾT LUẬN CUỐI (hai dòng đầu tệp là canonical và ĐÃ CHỐT — không còn là placeholder)

**verdict: changes_requested** · reviewed_sha `b881c6d1acd481925ef96c05fb9109e95df340fe` · **P1=0 · P2=1 · P3=1** (F-20A slug `ruff-khuon-chua-chung-minh-provisioning`/sub-class mới `heredoc-body-continuation-join`; F-20B slug `ruff-fixture-thieu-rang-chot-moi`/sub-class mới `nua-cua-297-backtick-va-306-here-khong-rang`).
Tổng approve đòi CẢ BA lớp approve — lớp 2 và lớp 3 chưa đạt. F-19A của R19 xác nhận ĐÃ VÁ THẬT; hai finding lượt này nằm ở vùng mã cũ CÙNG HỌ heredoc mà fixture mới vừa soi đèn tới, không phải hồi quy do delta. Đính chính có bằng chứng cho câu R19 "chỉ còn nửa-nhánh `:269`": bản đồ VẾ tìm thêm hai cửa. Không merge/land; integration master not_measured; CI/A1/A5 not_run theo chỉ thị. cross_approved (nếu đạt ở lượt sau) chỉ áp cho exact SHA được review, không phải quyền merge.
