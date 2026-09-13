verdict: changes_requested
reviewed_sha: e5e8e2390db1c4a68ad0ee6febdf7d6ed0a39582

# VERDICT-ADDENDUM — làm rõ readback acceptance-r15 (cùng review 15, cùng SHA, KHÔNG phải lượt mới)

- Cùng reviewer session `14967d80-0caf-4723-997b-d543fb7396ab` của review 15, độc lập executor; không dùng
  context executor. Hạn tuyệt đối CŨ `2026-09-13T20:47:43Z`, KHÔNG reset 90 phút.
- Phạm vi: đúng hai tệp readback — `expansion-acceptance-r15.json` (14 ca, đọc bytes, tự tái lập trên clone)
  và `shell-carrier-acceptance-r15.json` — KHÔNG săn 6 hướng mới; giữ nguyên bảng săn chính + lịch sử. Chỉ
  parser offline, KHÔNG thực thi fixture/shell/`--chay`, không mạng/CI/commit.
- **VERDICT.md gốc BẤT BIẾN** — tự đo sha256 = `36f700a3c08e1d2b3bb53db4bdc8f4f015abdb7c66cfabbf0245788edc6229e0`
  **KHỚP neo** (đo ở Đ0 dưới). Verdict gốc giữ nguyên; addendum này KHÔNG đổi verdict (đã là `changes_requested`).
- Trạng thái: **HOÀN TẤT** — hai dòng đầu canonical, chốt tại "KẾT LUẬN HIỆU LỰC".

## Nhật ký phép đo (append-only)

### Đ0 — Neo bất biến
```
sha256(VERDICT.md)      = 36f700a3c08e1d2b3bb53db4bdc8f4f015abdb7c66cfabbf0245788edc6229e0  (KHỚP neo prompt)
clone HEAD              = e5e8e2390db1c4a68ad0ee6febdf7d6ed0a39582   tree 2046f927fe8375c0bd98f2dc2d6a23fab1c14da9
```

### Đ1 — Tái lập 14 ca `expansion-acceptance-r15.json` trên CLONE (`scratch/adden_expansion.py`)
Carrier đúng mô tả: job pin+probe đúng · run opaque (ca) · registry `--chay` đúng; gọi `loi_ruff_ci` qua
`yaml.safe_dump`; `bash --noprofile --norc -n` của TÔI đối chiếu (không thay kết quả consumer).
**Cả 14 ca khớp executor từng ca** (kind, errors, bash_n_rc). Phân loại POSIX (XCU 2.6.2/2.2.2) + phán quyết:

| # | input | bash -n | scanner argv/kind | POSIX | phán quyết |
|---|---|---|---|---|---|
| 1 | `echo $[1+2` | rc=2 | `['echo','$[1+2']` KHONG | `$[` **unspecified** (non-POSIX) | **GAP** expansion-grammar |
| 2 | `X=$[` | rc=2 | `['X=$[']` KHONG | unspecified | **GAP** |
| 3 | `echo "$[1+2"` | rc=2 | `['echo','$[1+2']` KHONG | unspecified | **GAP** |
| 4 | `echo $'\'` | rc=2 | `['echo','$\']` KHONG | **VALID** (`$` + SQ `\` = `$\`) | accepted-domain (xem dưới) |
| 5 | `echo $'ok'` | rc=0 | KHONG | valid | accepted (opaque) |
| 6 | `echo $"ok"` | rc=0 | KHONG | valid | accepted |
| 7 | `echo '$[1+2'` | rc=0 | KHONG | valid (SQ data) | accepted |
| 8 | `echo \$[1+2` | rc=0 | KHONG | valid (escaped `$`) | accepted |
| 9 | `echo "$"` | rc=0 | KHONG | valid (literal `$`) | accepted |
| 10 | `echo $` | rc=0 | KHONG | valid | accepted |
| 11 | `echo $X` | rc=0 | KHONG | valid expansion | accepted → **F3** (docstring rộng) |
| 12 | `echo $$` | rc=0 | KHONG | valid special-param | accepted → **F3** |
| 13 | `echo ${X}` | rc=0 | KHONG | valid | accepted — docstring `${TEN}` in-domain |
| 14 | `echo "${X:-OK}"` | rc=0 | KHONG | valid | accepted — docstring `${TEN:-literal}` in-domain |

### Đ2 — Tokenize 4 ca "cú pháp hỏng" + THỬ KHAI THÁC (`scratch/adden_expansion.py` mục B/C)
```
echo $[1+2    -> [(['echo','$[1+2'], bad=True, related=False, KHONG)]   ($ rơi vào else generic, chỉ set bad)
X=$[          -> [(['X=$['], bad=True, KHONG)]
echo "$[1+2"  -> [(['echo','$[1+2'], bad=True, KHONG)]
echo $'\'     -> [(['echo','$\'], bad=True, KHONG)]   ← trùng KHỚP tokenize POSIX (`$\`)
```
KHAI THÁC (giấu installer liên quan qua divergence — **KHÔNG ca nào giấu được**):
```
echo $[pip install ruff==9.9.9        -> 1 token echo, related=False (pip nằm TRONG word, bash cũng vậy)
echo $[1] ; pip install ruff==9.9.9   -> pip TÁCH ra, related=True KHONG_GHIM — bị THẤY, không giấu
pip install ruff==9.9.9 $[1+2         -> 1 lệnh, KPT (bad+related)
echo $'\' ; pip install ruff==9.9.9 ' -> RAISE "trích dẫn chưa đóng" = KPT (fail-close!)  [3 biến thể $' đều KPT]
echo "$[1+2 ; pip ..."                -> 1 token echo (`;`/pip trong nháy kép), bash cũng rc=2
```
⇒ Divergence `$[`/`$'` **không mở đường giấu installer**: hoặc scanner nuốt vào cùng một word như bash-word,
hoặc `;` tách khiến pip **bị thấy**, hoặc chuỗi smuggle **RAISE KPT** (scanner CHẶT hơn bash — chiều fail-close).

### Đ3 — `$((` modern arithmetic + real ci.yml (`scratch/adden_expansion2.py` mục E + grep)
```
echo $((1+2      -> KPT "command substitution chưa đóng"    (bắt qua đường $( )
echo $((1+2))    -> KPT "ngoặc trần ngoài miền lệnh đơn"     (bắt qua bare-paren)
X=$((            -> KPT
```
⇒ `$((` (và cả họ `$(`) ĐÃ được closure-guard; **chỉ RIÊNG `$[` (dấu ngoặc vuông, arithmetic legacy) hở.**
`grep -E '\$\[|\$\(\(|\$'\''' ci.yml` (real) ⇒ **0 hit** — `$[`/`$'` KHÔNG có trong ci.yml thật (bare `$`/`${`
= 46 hit). Nên tighten `$[` → KPT **không** đụng workflow thật.

### Đ4 — shell-carrier (`scratch/adden_expansion2.py` mục F/G) — pwsh + POSIX-if body
`_shell_trong_mien` nhận `bash/sh/pwsh/powershell` (dòng 464) + docstring dòng 487 khai cả bốn in-domain;
`_dong_logic` CHỈ có grammar POSIX. Đo:
```
consumer: shell=pwsh   run='if true; then echo hi; fi' -> errors=0 (KHONG)
PowerShell 7.6.6:      cùng chuỗi              -> MissingOpenParenthesisInIfStatement (executor đo)
KHAI THÁC giấu installer trên pwsh (job phụ):
  pip install ruff==9.9.9                    -> BAT (2 lỗi)     ← pip tokenize y hệt mọi shell
  if ($true) { pip install ruff==9.9.9 }     -> BAT (3 lỗi)     ← `(`/`{` bare-paren/khung → KPT
  & pip install ruff==9.9.9                  -> BAT (3 lỗi)
  Start-Process pip -Args 'install','ruff'   -> BAT (2 lỗi)     ← Start-Process unknown → KPT
  pwsh run='Write-Host hi'                   -> consumer 1 lỗi  (KPT — idiom PowerShell fail-close)
```
⇒ Grammar POSIX áp lên thân pwsh **không giấu được installer** (pip cross-shell; idiom PowerShell fail-close).
Divergence chỉ theo hai chiều VÔ HẠI: (a) thân POSIX-hợp-lệ-nhưng-pwsh-vô-nghĩa → KHONG nhưng runtime pwsh
sẽ ĐỎ (ồn ào, không im); (b) thân PowerShell-hợp-lệ → thường KPT (false-positive, fail-close).

---

## PHÁN QUYẾT TỪNG CA (trả lời "thuộc miền được nhận nào, hay vi phạm")

- **Ca 1-3 (`$[…` legacy arithmetic, bash rc=2):** VI PHẠM nhẹ — sub-class **`expansion-grammar`** thuộc
  `opaque-structural-grammar`, GIỮ stable slug `ruff-khuon-chua-chung-minh-provisioning`. Lý do: `$[` là
  expansion **non-POSIX/unspecified** nên KHÔNG phải "quoting POSIX hợp lệ"; scanner để `$` rơi vào else
  generic (chỉ set `bad`) trong khi `${`/`$(`/`$((` đều được closure-check ⇒ đúng lớp "opaque không được
  miễn cú pháp" (R13/R14-addendum). **P3, không P2:** (i) đo được KHÔNG khai thác được (Đ2 — không giấu được
  installer); (ii) `$[` là *unspecified* chứ không *invalid* dứt khoát như `||`/`>`/`${x` của R14-addendum
  (vốn P2); (iii) `$[` vắng mặt trong ci.yml thật. Đây là hở fail-close/nhất-quán, không phá bảo đảm cổng.
- **Ca 4 (`$'\'` ANSI-C, bash rc=2):** **KHÔNG vi phạm — accepted-domain.** Scanner cho `['echo','$\']`, **trùng
  khớp POSIX** (`$` literal + SQ `\` = `$\`); bash rc=2 CHỈ vì extension ANSI-C (`$'…'`) — ngoài POSIX. Miền
  công bố là POSIX ⇒ KHONG là ĐÚNG theo hợp đồng. Divergence lexer vs bash đi chiều fail-close (Đ2: mọi
  smuggle RAISE KPT); "không viện shell sẽ chết" không áp ngược để BẮT một chuỗi POSIX-hợp-lệ. Ghi rõ đây là
  ca runtime(bash) CHẶT hơn miền POSIX công bố, không phải cổng nhận sai.
- **Ca 5-10:** accepted-domain đúng (opaque/data/escaped/literal `$`, đều POSIX-valid, bash rc=0).
- **Ca 11-12 (`$X`, `$$`):** accepted-domain (POSIX-valid) nhưng KHỚP **F3** của VERDICT gốc — docstring
  "các expansion khác ngoài miền" RỘNG HƠN hành vi (nhận). Không nhân đôi: **hợp nhất vào F3**, không finding mới.
- **Ca 13-14 (`${X}`, `"${X:-OK}"`):** accepted-domain, **đúng nguyên văn** docstring (`${TEN}`/`${TEN:-literal}`).

## FINDING (cộng vào VERDICT gốc — KHÔNG nhân đôi slug)

### F4 — `ruff-khuon-chua-chung-minh-provisioning` [P3] (sub-class MỚI **expansion-grammar** trong opaque-structural-grammar; GIỮ slug, không reset lịch sử)
`$[…]` arithmetic legacy không được closure-check nên chuỗi bash-invalid được cấp KHONG.
TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py` — `_dong_logic` xử lý `$` chỉ đóng `${` (dòng 237-240) và `$(`
(242-249); `$[` rơi vào else generic dòng 297 (`if c in "$\`()<>*?[]{}": bad = True`) ⇒ `$` thành literal, `[`
set bad, không đòi `]`. (Đối chứng: `$((` được bắt qua đường `$(`+bare-paren — Đ3.)
COUNTEREXAMPLE (ĐÃ CHẠY, Đ1/Đ2): `echo $[1+2` · `X=$[` · `echo "$[1+2"` — bash rc=2, scanner KHONG errors=0.
KHÔNG khai thác được (Đ2): không giấu được installer liên quan.
HƯỚNG SỬA CẤP LỚP (bằng lời, KHÔNG patch — gate sensitive §8): mở rộng nhánh `$` trong `_dong_logic` để nhận
diện `$[` như một expansion NGOÀI MIỀN — `raise ValueError("arithmetic expansion ngoài miền")` khi gặp `$[`
(giống cách `${` đòi `}` và `$(` đòi `)`); vì `$[` là dạng legacy/non-POSIX vắng mặt ci.yml thật, từ chối
thẳng (KPT) là an toàn. Cân nhắc gộp cùng một điểm với luật `${` cho một mặt "expansion đóng".
FIXTURE/MUTANT KHOÁ: âm `syntax-dollar-bracket-eof` `echo $[1+2` (want 1) · `X=$[` (want 1) ·
`echo "$[1+2"` (want 1); dương giữ màu `echo '$[1+2'` (want 0, SQ data) · `echo \$[1+2` (want 0, escaped) ·
`echo $((1+2))`-đã-KPT giữ nguyên. MUTANT: gỡ guard `$[` ⇒ ba ca âm phải LỌT (đối chứng bắt buộc); và mutant
NỚI guard sang bắt cả `$((` ĐÃ-KPT không được đổi ba ca dương.
NGUY CƠ HỒI QUY: ≈0 — ci.yml thật 0 `$[` (Đ3); ca dương xanh sẵn trên HEAD. Ước +~5 fixture + ~2-3 dòng lexer
⇒ 872 → <885 ≤ 1000, giữ đúng 2 path.
ĐÃ THỬ VÁ: không (write set packet + authority sensitive). ĐỘ TIN: cao — A/B scanner↔bash + POSIX XCU 2.6.2.

### F5 — `ruff-shell-carrier-grammar-mismatch` [P3] (trục Spec/scope lớp 3 — chưa executor tự gán)
Miền shell công bố (`bash/sh/pwsh/powershell`) RỘNG HƠN grammar được cài (POSIX-only) ⇒ thân pwsh/powershell
được chấm bằng POSIX.
TỆP/DÒNG: `_shell_trong_mien` dòng 464 (`scope["shell"] in ("bash","sh","pwsh","powershell")`) + docstring
dòng 487; `_dong_logic` chỉ POSIX. COUNTEREXAMPLE (ĐÃ CHẠY, Đ4): `shell:pwsh` + `if true; then echo hi; fi`
⇒ consumer KHONG/[], PowerShell 7.6.6 ⇒ `MissingOpenParenthesisInIfStatement`.
XÁC ĐỊNH (trả lời scope_question): **carrier KHÔNG khớp grammar, và là giới hạn CHƯA được công bố** — docstring
nhận pwsh/powershell mà KHÔNG nói "thân được chấm bằng tokenize POSIX". KHÔNG khai thác được (Đ4: pip cross-shell
vẫn BẮT; idiom PowerShell fail-close) ⇒ P3, không phá cổng.
HƯỚNG SỬA (ƯU TIÊN THU HẸP HỢP ĐỒNG, KHÔNG thêm engine — theo chỉ thị): hoặc (a) `_shell_trong_mien` chỉ nhận
`bash/sh` (POSIX shell) ⇒ pwsh/powershell → KPT (sạch nhất, khớp spec "quoting POSIX"); hoặc (b) khai THẲNG
trong docstring rằng pwsh/powershell chỉ được nhận cho phát hiện-cài SHELL-AGNOSTIC qua tokenize POSIX (giới
hạn ĐƯỢC CÔNG BỐ), giữ nguyên fixture. KHÔNG viết parser PowerShell tổng quát.
FIXTURE/MUTANT KHOÁ: nếu (a) — `shell-vo-can-hop-le-pwsh/powershell` lật want→1, thêm mutant re-add pwsh vào
`_shell_trong_mien` phải làm ca pwsh-POSIX-body LỌT; nếu (b) — một fixture ghim câu giới hạn (pwsh + thân POSIX
= KHONG có chủ đích, ghi rõ). NGUY CƠ HỒI QUY: (a) đổi hành vi 2 fixture hiện có (phải cân nhắc) · (b) ≈0.
ĐỘ TIN: cao — đo consumer + đối chiếu PowerShell parser executor + battery khai thác.

## KẾT LUẬN HIỆU LỰC (chốt — thay placeholder; hai dòng đầu tệp canonical)
- verdict hiệu lực: **changes_requested** · reviewed_sha `e5e8e2390db1c4a68ad0ee6febdf7d6ed0a39582`
  (tree `2046f927fe8375c0bd98f2dc2d6a23fab1c14da9`). VERDICT.md gốc BẤT BIẾN — verdict KHÔNG đổi bởi addendum.
- **Ba lớp (hợp nhất với VERDICT gốc):** Lớp 1 **approve** (14 ca không đụng nhận dạng installer) · Lớp 2
  **approve** (hành vi; ca 4 accepted-domain POSIX-đúng; F3 docstring giữ P3) · Lớp 3 **changes_requested**
  (F1 P2 giữ nguyên + thêm F4 `$[` P3 + F5 shell-carrier P3).
- **Count hiệu lực:** P1=0 · **P2=1** (F1 `cua-khuon-khong-rang`, VERDICT gốc — KHÔNG đổi) · **P3=4**
  (F2 bien-bang-chu-cai-redirect-va-op · F3 docstring-parameter · **F4 expansion-grammar `$[`** ·
  **F5 shell-carrier-grammar-mismatch**). Approve tổng vẫn đòi cả ba lớp ⇒ **changes_requested**.
- **Bao phủ & hợp nhất slug (không nhân đôi):** F4 dùng CHUNG slug `ruff-khuon-chua-chung-minh-provisioning`
  với F1, chỉ khác sub-class (`expansion-grammar` vs `cua-khuon-khong-rang`) — đúng khuôn R11→R14 một-slug-
  nhiều-subtype. Ca 11-12 (`$X`/`$$`) HỢP NHẤT vào F3 gốc, không finding mới. Ca 4 KHÔNG thành finding.
- **Readback:** phán quyết acceptance — 4 ca bash-invalid gồm **3 vi phạm (`$[`, → F4)** + **1 accepted-domain
  (`$'\'`, POSIX-đúng)**; 10 ca còn lại accepted-domain (2 khớp F3). Verdict chấp nhận của executor **KHÔNG
  được xác nhận** ở đúng 3 ca `$[`; đây là cùng lớp opaque-structural-grammar mà R14-addendum đã phân xử.
- A1/A5/CI/A2-conclusions/A6-readback/A9-live: **not_run/KHÔNG ĐO ĐƯỢC** theo chỉ thị — không đọc thành passed.
  Tích hợp master mới `c16bd329`: **not_measured**, không dùng ngoại lệ merge §5.1. Không mang quyền merge/land.
- Identity: provider **anthropic_claude** · model **claude-fable-5** · effort **max** · execution_surface
  **claude_code** · transport **machine/local** — cùng session review 15, không phiên executor; validator so
  `modelUsage` thô sau run.
- Hiện vật addendum: `scratch/adden_expansion.py` · `scratch/adden_expansion2.py` (NGOÀI clone).
- Bất biến cuối lượt (ĐO SAU khi viết xong thân — ghi ở dòng dưới cùng): clone HEAD/tree/porcelain + sha VERDICT gốc.

### ĐO CUỐI LƯỢT
```
clone HEAD  = e5e8e2390db1c4a68ad0ee6febdf7d6ed0a39582   (KHỚP, không đổi)
clone tree  = 2046f927fe8375c0bd98f2dc2d6a23fab1c14da9   (KHỚP)
porcelain   = 0 dòng (sạch — chỉ đo tại thời điểm này, không tự chứng minh lịch sử cả lượt)
sha256(VERDICT.md gốc) = 36f700a3c08e1d2b3bb53db4bdc8f4f015abdb7c66cfabbf0245788edc6229e0  (BẤT BIẾN, khớp neo)
```
