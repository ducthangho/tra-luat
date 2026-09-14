verdict: changes_requested
reviewed_sha: ff146f16f26f1eb59d7a3839d5cc48811b13daac

> Trạng thái: **HOÀN TẤT** — hai dòng trên là canonical và ĐÃ CHỐT tại mục "KẾT LUẬN CUỐI".
> (Đầu lượt hai dòng ấy là placeholder `changes_requested` đúng quy trình; kết luận cuối trùng giá trị
> placeholder nên không đổi chữ nào — xác nhận MỘT lần khi đóng, không xoá nhật ký. P1=0 · P2=0 · P3=2.)

## Trạng thái đo
- [x] Xác minh SHA/tree/base của clone cay-kho — Đ0
- [x] Đọc SPEC-r23 / LEASE-r23 / authority / prompt / cross-review-SKILL / protocol §8+§13 / PRIOR_HUNT_INDEX / prior-review-15 (main + addendum-FAILED) / delta-r15.patch / toàn bộ delta mã
- [x] Đối chiếu finding R15 (F1/F2/F3): CẢ BA **ĐÃ VÁ THẬT** — bảng ĐỐI CHIẾU LƯỢT TRƯỚC
- [x] Gate targeted: registry 531/531 · 21/21 · launcher 4/4 · Ruff 3/3 · ruff F rc0 — Đ2 · actionlint rc0 (kèm shellcheck) — Đ2b
- [x] A8 933/1000 đúng 2 paths — Đ1
- [x] 54/54 semantic mutants — Đ3 (ROOT ghim clone, artifact scratch, đúng 1 fixture_run_separate)
- [x] Bảng săn 7 hướng MỚI độc lập (lớp 1: 2 · lớp 2: 3 · lớp 3: 2) — 2 LỖI (F-A·F-B) · 5 KHÔNG PHẢI LỖI
- [x] Kiểm cuối HEAD/tree/status — Đ6

## Nhật ký đo

### Đ0 — Trạng thái clone (đo lúc mở phiên)
```
$ git -C cay-kho rev-parse HEAD          → ff146f16f26f1eb59d7a3839d5cc48811b13daac  (KHỚP exact reviewed_sha)
$ git -C cay-kho rev-parse "HEAD^{tree}" → f405a78c241100fe14a0d824e1483a78bdb69357  (KHỚP exact tree)
$ git -C cay-kho status --porcelain      → (rỗng — sạch)
$ git -C cay-kho cat-file -t bb7013c7…   → commit (base tồn tại)
```

### Đ1 — A8 + freeze workflow
```
$ git diff --numstat bb7013c7..HEAD → 807+92 (.claude/dev/ci_dang_ky_test.py) · 126+6 (.github/workflows/ci.yml)
  ⇒ additions 807+126 = 933 ≤ 1000, ĐÚNG 2 path (KHỚP khai 933/1000)
$ ls-tree ci.yml @3bbc6b46 = cb025a5a704a8f73319fee4ddded0010678e8f02 = @HEAD ⇒ workflow BYTE-IDENTICAL với freeze ✓
$ git diff --numstat 3bbc6b46..HEAD → CHỈ ci_dang_ky_test.py (620+191) — sau freeze chỉ Python đổi ✓
```

### Đ2 — Baseline suite + Ruff (đo trên clone, KHÔNG --chay)
```
$ python -X utf8 -B .claude/dev/ci_dang_ky_test.py (cwd=clone) → rc=0
  ĐĂNG KÝ: 21/21 · LAUNCHER WINDOWS: 4/4 · RUFF CI: 3/3 · PHẢN CHỨNG: 531/531 đỏ đúng · TỔNG: ĐẠT
  grep -c "ĐỘT BIẾN" = 531 — hai số dương BẰNG NHAU, không tin rc trần.
$ diff (r16-freeze-registry.txt trừ dòng "rc=0") vs (tự chạy) → IDENTICAL; freeze ≡ sandbox-registry.txt IDENTICAL
$ ruff check --no-cache --select F ci_dang_ky_test.py → All checks passed, rc=0
```

### Đ3 — TÁI LẬP 54 MUTANT (phương pháp EXECUTOR_MUTATION_METHOD.py.txt nguyên văn, chỉ thay neo:
ROOT ghim CLONE cay-kho, artifact scratch/mutants-r16; KHÔNG chạy path executor)
```
KILLED 54/54 — từng mutant: semantic_changed AND ≥1 fixture LỌT AND rc=1 AND "TỔNG: ĐỎ"
fixture_run_separate: đúng 1 — powershell-known-subset (main short-circuit vì ci.yml thật đỏ; phan_chung gọi riêng)
So với mutation-r16.json của executor: tập tên = nhau; (killed, tập-fixture-LỌT) từng mutant KHỚP TOÀN BỘ.
10 mutant SỐNG của R15 nay CHẾT, leak đúng fixture cô lập (disjoint theo mệnh đề):
  header-command → guard-header-group-{semicolon,and} · inline-header → guard-inline-header-isolated
  condition-compound → guard-condition-compound-isolated · unsupported-keyword → 14 guard-unsupported-keyword-*
  operator-3pipe → syntax-op-|||-{giua,cuoi} · redirect-drop-{newline,pipe,amp,ltgt} → đúng phần tử biên tương ứng
  (narrow-max → hợp của 5) — thoả yêu cầu "mỗi mệnh đề MỘT fixture mà CHỈ nó chặn".
```

### Đ2b — actionlint (điều kiện đo khai kèm)
```
$ actionlint cay-kho/.github/workflows/ci.yml → rc=0, 0 chẩn đoán
  actionlint 1.7.7 · shellcheck 0.9.0 CÓ MẶT (nền đo MẠNH — luật shellcheck đang bật, không phải rc=0 vì thiếu công cụ)
$ r16-freeze-actionlint.txt = "rc=0" · r16-freeze-ruff.txt = "rc=0\nAll checks passed!" — khớp tự đo
```

### Đ4 — Chuỗi định danh + không-kế-thừa-addendum-lỗi-model
```
$ sha256(PROMPT.md) = 3d78a7b2… KHỚP --expected-prompt-sha256 của launch-request.json; PROMPT.md ≡ prompt.snapshot
$ sha256(SPEC-r23.md) = 7089ad0d… KHỚP spec_hash/spec_sha256 của LEASE-r23.yaml
$ frozen-r16.json: head/tree/base/additions 933/fixtures 531/mutants 54 — TẤT CẢ khớp phép đo độc lập ở Đ0–Đ3
$ prior-review-15-addendum-IDENTITY-FAILED: KHÔNG dùng làm căn cứ; mọi phán quyết expansion tự tái lập ở Đ5/H2
$ delta-r15.patch ≡ git diff e5e8e23..HEAD (tự sinh, byte-equal) — delta lượt này CHỈ Python, khớp khai
```

### Đ5 — Tái đo expansion-acceptance-r16.json (V-pass, KHÔNG tính vào N hướng săn)
```
14/14 dòng: số lỗi + nội dung errors + kind KHỚP artifact executor; bash --noprofile --norc -n -c (ground truth
parse-only) KHỚP cột bash_n_rc từng dòng (6 reject/2-lỗi · 8 accept/0-lỗi; 'echo $'"'"'ok'"'"'' và 'echo $"ok"'
bash rc=0 mà consumer TỪ CHỐI — đúng chiều CHẶN đã công bố "không hỗ trợ ANSI-C/locale").
Hiện vật: scratch/hunt-rv.json khoá V_expansion_acceptance.
```

### Đ6 — Bất biến cuối lượt (đo SAU khi viết xong thân verdict)
```
$ git -C cay-kho rev-parse HEAD          → ff146f16f26f1eb59d7a3839d5cc48811b13daac  (KHÔNG đổi)
$ git -C cay-kho rev-parse "HEAD^{tree}" → f405a78c241100fe14a0d824e1483a78bdb69357  (KHÔNG đổi)
$ git -C cay-kho status --porcelain | wc -l → 0  (sạch — trạng thái chỉ là phép đọc tại thời điểm đo)
Clone không bị ghi trong cả lượt: mọi mutant/probe chạy trên BẢN SAO trong scratch/, ROOT ghim về clone chỉ để ĐỌC.
```

---

## ĐỐI CHIẾU LƯỢT TRƯỚC (R15 main — verdict hiệu lực; addendum FAILED-IDENTITY không phải verdict)

| finding R15 | trạng thái | bằng chứng TỰ ĐO (không nhận lời khai executor) |
|---|---|---|
| F1 `ruff-fixture-thieu-rang-chot-moi`/cua-khuon-khong-rang [P2] — 4 mệnh đề `_kiem_khuon_shell` gỡ nguyên mà suite xanh | **ĐÃ VÁ THẬT** | Đ3: 4 mutant (header-command · inline-header · condition-compound · unsupported-keyword) BỊ GIẾT, leak ĐÚNG fixture cô lập mới, tập leak rời nhau theo mệnh đề; 14 fixture keyword phủ cả 12 keyword còn lại + `"fi"` (quote) + `\f\i` (escape) đúng hướng sửa R15; suite HEAD 531/531 xanh |
| F2 cùng slug/bien-bang-chu-cai-redirect-va-op [P3] — 6 mutant biên sống | **ĐÃ VÁ THẬT** | Đ3: cả 6 (redirect-drop-newline/pipe/amp/ltgt/narrow-max + operator-3pipe) BỊ GIẾT; 7 fixture guard-redirect-boundary phủ TRỌN bảng chữ cái `\n ; | & < > #`; `\|\|\|` vào op-fixture 3 vị trí; hai phần tử addendum nêu đích danh (`> \| wc` · `\|\|\|`) nay có fixture riêng |
| F3 `ruff-docstring-parameter-rong-hon-hanh-vi` [P3] — câu docstring rộng hơn hành vi | **ĐÃ VÁ THẬT** | Docstring viết lại đúng hướng "giới hạn vào dạng có kiểm + $ là literal ngoài tiền tố"; 33 fixture parameter-bare (11 dạng × 3 ngữ cảnh) làm neo dương; Đ5 14/14 khớp bash; H2 đo thêm heredoc/midword/continuation đều khớp câu mới. KHÔNG phát hiện VÁ SINH LỖI MỚI trong phạm vi câu parameter. (Câu MỚI về pwsh có vấn đề RIÊNG — F-B dưới, bề mặt khác, không phải hồi quy của F3.) |

---

## BẢNG SĂN — 7 hướng MỚI độc lập (lớp 1: H3·H4 · lớp 2: H1·H2·H6 · lớp 3: H5·H7)

Đối chiếu PRIOR_HUNT_INDEX.md: các bề mặt săn chính (grammar carrier pwsh `_shell_trong_mien` nhánh mới,
charset argv ASCII, splitlines-vs-PS-newline, tương tác dollar-guard mới, installer-qua-carrier) đều thuộc MÃ MỚI
của r16 (delta e5e8e23..HEAD) nên không tồn tại trong R7–R15; grep index các từ khoá liên quan chỉ trúng các mục
shell-before-body/≥0x7F cũ đo trên bề mặt POSIX-lexer, khác đầu vào. Replay Đ2/Đ3/Đ5 KHÔNG tính vào N.
Script + JSON: `scratch/hunt_rv.py` · `scratch/hunt-rv.json` · `scratch/ps_probe.ps1` · `scratch/ps_probe_out_{51,7}.json` · `scratch/mutants-carrier/`.

### H1 [LỚP 2] — carrier pwsh: splitlines của Python vs luật newline của PowerShell (C0 + NEL/LS/PS + CRLF) — **LỖI một phần (F-B, P3)**
Giả thuyết: `splitlines()` cắt trên \x0b \x0c \x1c-\x1e \x85 U+2028 U+2029 mà PowerShell không coi là newline ⇒ có
thân được "duyệt theo dòng Python" nhưng chạy theo luật khác. Đo end-to-end `loi_ruff_ci` (cả pwsh lẫn powershell):
```
\x0b/\x0c/\x1c giữa 2 lệnh → 2 lỗi (C0-guard POSIX chặn) · \r\n → 2 lỗi (\r là C0) — fail-close ✓
\x85 · U+2028 · U+2029 giữa "echo hi" và "echo ok" → 0 lỗi — ĐƯỢC NHẬN
"echo hi\x85pip install ruff==0.15.14" (cả U+2028/U+2029) → 0 lỗi — ĐƯỢC NHẬN
```
Ground truth PS parser (ParseInput, PS 5.1.26100.9278 VÀ pwsh 7.6.6, parse-only): cả bốn thân NEL/LS/PS đều là
**MỘT PipelineAst duy nhất** — PowerShell KHÔNG cắt statement tại các byte ấy ⇒ `pip install…` KHÔNG bao giờ chạy
thành lệnh riêng (nó là đối số/đuôi token của `echo`). Chứng chỉ 0-lỗi vì vậy VẪN ĐÚNG về hành vi (không có install
ẩn); phép thử pin-smuggle `"pip install ruff==0.15.15\x85echo hi"` → 1 lỗi (token dính làm pin lệch ⇒ KHONG_GHIM) —
nghĩa vụ installer không xuyên thủng. Phần LỖI còn lại thuần công bố-miền: thân chứa byte NGOÀI ASCII được nhận
trong khi câu công bố nói "từ ASCII" và mô hình "line" của câu là splitlines chứ không phải CR/LF của chính shell
được nêu tên ⇒ **F-B [P3] trục Spec**. Kết luận: hành vi KHÔNG PHẢI LỖI (đo 2 phiên bản PS bắt buộc); công bố LỖI P3.

### H2 [LỚP 2] — tương tác dollar-guard mới: nối dòng/heredoc/mid-word/DQ (bash -n ground truth) — KHÔNG PHẢI LỖI
12 ca đo (scratch/hunt-rv.json H2): `X=$\⏎(pip install ruff==0.15.14)` → 2 lỗi (chuẩn hoá nối dòng KHÔNG che được
command-substitution liên quan — inner vẫn bị phân tích đệ quy) · `echo $\⏎(echo hi)` → 0 · `echo "$\⏎[1+2"` → 2 ·
`echo $\⏎X` → 0 · nối dòng KÉP `$\⏎\⏎[` → 2 · `$\⏎$X` → 0 · heredoc quoted/unquoted chứa `$[1+2]` → 0 (đúng câu
"dữ liệu heredoc giữ nguyên") · `echo hi#$[1+2]` → 2 và `echo a$'b'` → 2 (bash -n rc=0 — chiều CHẶN, đã công bố
"$[ bị từ chối"/"không hỗ trợ ANSI-C") · `echo "x$"[1+2]` → 0 (đúng POSIX: $ trước nháy đóng là literal) ·
`pip install ruff==0.15.15$` → 1 lỗi (pin lệch ⇒ fail-close, không đúc GHIM). Mọi ca khớp bash -n hoặc lệch đúng
CHIỀU CHẶN đã công bố. Không đường nào biến related thành KHONG.

### H3 [LỚP 1] — nhận dạng họ installer XUYÊN carrier pwsh mới — KHÔNG PHẢI LỖI
```
job gate TOÀN pwsh (pin+probe / registry) → 0 lỗi  — carrier đủ chỗ cho trọn hợp đồng M7
pwsh 'pip install ruff==0.15.14' → 1 lỗi (KHONG_GHIM)      pwsh 'python -m pip install ruff==0.15.14' → 1 lỗi
pwsh 'pip.exe install ruff==0.15.14' → 1 lỗi (KPT — installer lạ KHÔNG biến thành KHONG; bash cùng kết quả)
pwsh 'Pip install ruff==0.15.14' → 1 lỗi (KPT — PS case-insensitive nhưng phân loại POSIX case-sensitive ⇒ fail-close)
pwsh 'uv pip install ruff==0.15.15' + probe → 0 lỗi
```
Đúng chỉ thị lease "ngoài miền không được biến thành KHONG": mọi dạng lạ đều ĐỎ, không dạng nào đúc được GHIM.

### H4 [LỚP 1] — nghĩa vụ pin/probe ở JOB PHỤ qua carrier pwsh + defaults job/workflow — KHÔNG PHẢI LỖI
`phu` pwsh pin-không-probe → 1 lỗi (probe, đúng job) · `phu` pwsh sai pin → 2 lỗi · `phu` pwsh pin+probe → 0 ·
defaults job-level pwsh + `echo hi` → 0 (mặt NHẬN của defaults hoạt động) · defaults pwsh + thân POSIX → 3 lỗi.
Phân hoạch per-job giữ nguyên nghĩa vụ khi shell khai ở mức defaults — khớp 4 ca `_them` shell-carrier-{job,workflow}.

### H5 [LỚP 3] — răng lưới cho BẢNG CHỮ CÁI của carrier (mutant nới charset tự dựng) — **LỖI (F-A, P3)**
5 mutant nới từng lớp ký tự bị loại của grammar `_shell_trong_mien` (mỗi mutant MỘT tệp riêng trong
scratch/mutants-carrier/, ROOT ghim clone, chạy TRỌN suite): **CẢ 5 SỐNG 531/531 (rc=0, 0 LỌT)** trong khi mỗi cái
KHÔNG-tương-đương NHÌN THẤY ĐƯỢC qua chính loi_ruff_ci (witness 2 lỗi → 0 lỗi, đã chạy):
```
widen-arg-dollar    ($ vào arg-class)   witness pwsh 'echo $X'      HEAD 2 → mutant 0   SỐNG
widen-arg-dquote    (\x22 vào arg)      witness pwsh 'echo "ok"'    HEAD 2 → mutant 0   SỐNG
widen-arg-semicolon (; vào arg)         witness pwsh 'echo hi; wc'  HEAD 2 → mutant 0   SỐNG
widen-arg-brace     ({} vào arg)        witness pwsh 'echo {x}'     HEAD 2 → mutant 0   SỐNG
widen-first-digit   (digit mở đầu từ 1) witness pwsh '2fa.sh x'     HEAD 2 → mutant 0   SỐNG (đo bổ sung, không suy)
```
Đối chứng rig có răng: 4 mutant carrier của executor (powershell-words/keywords/nonempty/known-subset) đều BỊ GIẾT
trong cùng rig (Đ3) — không phải rig hiền. Phân tích ở Finding F-A.

### H6 [LỚP 2] — câu "chỉ nhận ≥1 invocation/line": keyword-statement PowerShell lọt carrier có phá câu không — KHÔNG PHẢI LỖI (end-to-end)
Blocklist từ khoá của carrier = `_KHUNG_SHELL ∪ {return, exit}` (từ POSIX + 2 tên) — theo doctrine kho, danh sách
CẤM kiểu này không đủ với từ khoá RIÊNG của PowerShell: `break` `continue` `throw` `using` `param`… đều qua carrier.
Đo PS parser (cả 5.1 lẫn 7.6.6): `break`/`continue`/`throw`/`throw abc` = Break/Continue/ThrowStatementAst (KHÔNG
phải invocation); `using namespace` = using-statement; `switch abc`/`trap` = parse-error. NHƯNG đo end-to-end
`loi_ruff_ci`: TẤT CẢ các dạng ấy → ≥1 lỗi (phân loại POSIX trả KPT vì argv[0] ngoài _LENH_OPAQUE/mọi whitelist);
ca duy nhất 0 lỗi là `set x y` — mà `set` trong PS là alias Set-Variable, tức MỘT invocation thật. Kết luận: câu
công bố ĐÚNG ở mức hợp đồng loi_ruff_ci (mọi thân pwsh được cấp 0-lỗi chỉ gồm dòng-invocation); lỗ blocklist bị
backstop POSIX bịt kín — sạch, có giá ngang finding vì loại trừ nguyên một hướng tấn công.

### H7 [LỚP 3] — helper chết sau "remove dead helpers" (86b0feb)? — KHÔNG PHẢI LỖI
`_TIEN_TO_CAI` còn 2 tham chiếu: định nghĩa + phản chứng sống `tap-tien-to-khop-ky-vong` (khoá kỳ vọng tập tiền tố
cài) — KHÔNG phải mã chết. Đếm fixture mới khớp cấu trúc delta: 44 guard-* + 33 parameter-bare + 8 shell-carrier +
16 boundary + 4 defaults-carrier + 3 op-||| = 108 = 531 − 423 ✓; 4 fixture A7 (chua-tach/da-tach-*) còn nguyên màu.

---

## FINDING

### F-A — `ruff-fixture-thieu-rang-chot-moi`  [P3]  (GIỮ stable slug R11/R15; sub-class MỚI: bien-charset-pwsh-carrier)
Bảng chữ cái CHO PHÉP của grammar carrier pwsh không có răng theo TỪNG LỚP ký tự bị loại — 5 mutant nới sống trọn suite
TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py:471-473` — regex
`[ \t]*[A-Za-z_][A-Za-z0-9_./-]*(?:[ \t]+[A-Za-z0-9_./:=+-]+)*[ \t]*` trong `_shell_trong_mien`.
VẤN ĐỀ + COUNTEREXAMPLE (đều ĐÃ CHẠY, H5): docstring công bố carrier "không quote/expansion/toán tử/khối",
nhưng lưới fixture chỉ ghim MỖI LỚP ĐÚNG MỘT ĐẠI DIỆN ở phía bị chặn (`'` cho quote — boundary-3; `|` cho toán
tử — boundary-5; `"$X"` cho expansion NHƯNG chết được bằng dấu nháy nên không cô lập `$`; KHỐI: không có ca nào;
ký tự mở đầu từ: không có ca nào). Nới từng lớp (`$` · `\x22` · `;` · `{}` vào arg-class; digit mở đầu first-word)
⇒ CẢ 5 mutant KHÔNG-tương-đương sống 531/531 rc=0, mỗi cái có witness đổi màu 2 lỗi → 0 lỗi qua chính
`loi_ruff_ci` (bảng H5). Đây đúng hình dạng F2-R15 ("bảng chữ cái reject chỉ có răng ở 2/7 phần tử") tái phát
trên bảng chữ cái MỚI mà chính lượt vá này thêm vào — cùng lớp "vá đúng chỗ được chỉ rồi bỏ sót đường kế tiếp
không ai chỉ": khuôn FIXTURE/MUTANT-KHOÁ đã áp đủ cho redirect/op/expansion/4-mệnh-đề nhưng KHÔNG áp cho
charset của carrier vừa sinh.
VÌ SAO P3 (không phải P2): sản phẩm trên HEAD từ chối ĐÚNG mọi witness (cột HEAD); mọi mutant nới đều bị backstop
phân loại POSIX giữ nguyên nghĩa vụ installer (H3/H6: KPT/lỗi, không đúc GHIM, không install ẩn — kể cả khi nới);
lỗ CHỈ ở độ mịn lưới cho hồi quy tương lai — đúng phép phân hạng R14/R15 cho lớp này.
HƯỚNG SỬA CẤP LỚP (bằng lời, không patch — sensitive): mỗi LỚP ký tự bị loại một fixture âm pwsh mà CHỈ lớp ấy
chặn: `$` trần không nháy (vd `echo $X`), nháy kép KHÔNG kèm `$` (vd `echo "ok"`), một toán tử ngoài `|`
(vd `;`), một ký tự khối (`{` hoặc `(`), một first-word ngoài `[A-Za-z_]` (vd `2fa.sh x`); nhân đôi cho
powershell như bộ boundary hiện có. Ước +10–12 fixture ≈ +10–14 dòng, 933→≤950 ≤ 1000, giữ 2 path.
TEST/MUTANT GIỮ CHỐT: 5 mutant trong `scratch/mutants-carrier/` là phản chứng bắt buộc — sau khi thêm fixture,
chạy lại: CẢ 5 phải chuyển SỐNG → GIẾT (fixture mới LỌT, main rc=1); nên đưa dạng nới-charset vào bộ 54 của
EXECUTOR_MUTATION_METHOD cho các lượt sau.
NGUY CƠ HỒI QUY: ≈0 — không đổi mã sản phẩm; HEAD đã ĐỎ sẵn mọi witness; fixture mới xanh ngay trên HEAD.
ĐÃ THỬ VÁ: không — write set packet + authority sensitive (§8 loại trừ patch-as-hint cho bề mặt này); mutant nằm scratch.
ĐỘ TIN: cao — 5 cặp A/B HEAD↔mutant + 5 lượt suite trọn vẹn, tất cả trong hiện vật scratch.

### F-B — `ruff-docstring-pwsh-carrier-rong-hon-hanh-vi`  [P3]  (trục Spec lớp 2 — cùng LỚP lỗi với F3-R15, bề mặt MỚI)
Câu công bố carrier pwsh ("từ ASCII", "invocation/line") dùng mô hình "line" của Python splitlines — thân chứa
byte tách dòng NGOÀI ASCII được NHẬN dù câu nói ASCII
TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py:500-502` (docstring: "pwsh/powershell chỉ nhận ít nhất một
invocation/line bằng từ ASCII…") và `:470` (`splitlines()` — nơi mô hình line rộng hơn CR/LF).
VẤN ĐỀ + COUNTEREXAMPLE (ĐÃ CHẠY, H1): `"echo hi\x85echo ok"`, biến thể U+2028/U+2029, và
`"echo hi\x85pip install ruff==0.15.14"` dưới shell pwsh/powershell → **0 lỗi** (được nhận), trong khi thân
CHỨA byte ngoài ASCII và "dòng" chỉ tồn tại theo splitlines của Python — PowerShell (đo ParseInput cả
5.1.26100.9278 lẫn 7.6.6) coi cả thân là MỘT PipelineAst, tức khái niệm dòng của câu công bố không phải của
shell được nêu tên. Lời khai hẹp hơn hành vi ở chiều NHẬN — consumer KHÔNG "tự từ chối ngoài grammar" với lớp
byte này (chỉ thị M7: opaque không miễn cú pháp).
VÌ SAO KHÔNG PHẢI LỖI HÀNH VI (và vì sao P3): đã đo cả hai phiên bản PS bắt buộc — KHÔNG có statement thứ hai
nào được sinh (không install ẩn; `pip…` chỉ là chuỗi đối số của echo); thử pin-smuggle qua byte dính ⇒ 1 lỗi
(H1) — nghĩa vụ pin/probe/registry không xuyên thủng; C0 + \r đã bị chặn sẵn ở POSIX-guard. Chứng chỉ 0-lỗi
cho các thân ấy do đó vẫn ĐÚNG về hậu quả; sai nằm ở CÂU và ở biên miền công bố.
HƯỚNG SỬA CẤP LỚP (bằng lời): đóng theo chiều CHẶN cho khớp câu — carrier chỉ công nhận ranh giới dòng `\n`
(mọi byte tách-dòng khác của splitlines ⇒ ngoài miền), hoặc tương đương: từ chối thân pwsh chứa byte ngoài tập
ASCII in-domain đã công bố; kèm 3 fixture âm (\x85 · U+2028 · U+2029 giữa hai invocation) + 1 mutant gỡ chốt
ranh-giới làm 3 fixture ấy LỌT. Nếu chủ kho chọn giữ hành vi thì câu docstring phải khai tường minh mô hình
line theo splitlines và bỏ chữ "ASCII" — nhưng chiều CHẶN khớp M7 hơn.
NGUY CƠ HỒI QUY: ≈0 với chiều CHẶN (workflow thật chỉ có 1 dòng pwsh thuần ASCII — Đ2 3/3 xanh; YAML chuẩn hoá
line break về \n nên thân thật không chứa các byte ấy).
ĐÃ THỬ VÁ: không (sensitive). ĐỘ TIN: cao — end-to-end 0-lỗi đo trực tiếp + AST hai phiên bản PS trong hiện vật.

---

## BẢNG ĐO — lời khai executor ↔ đo được
| khẳng định executor | đo được (reviewer, độc lập) | khớp? |
|---|---|---|
| exact head/tree/base | ff146f16…/f405a78c…/bb7013c7… — rev-parse đầu VÀ cuối lượt, porcelain 0 cả hai lần | Có |
| A8 933/1000, đúng 2 path | numstat 807+126=933, đúng 2 path | Có |
| workflow byte-identical 3bbc6b46 | blob `cb025a5a70…` ở CẢ HAI commit; delta sau freeze CHỈ Python | Có |
| registry 531/531 + 21/21 + 4/4 + 3/3, rc=0 | tự chạy KHÔNG `--chay`: y hệt; grep đếm 531 = 531; diff freeze/sandbox-registry: IDENTICAL | Có |
| Ruff F rc=0 · actionlint rc=0 | tự chạy: All checks passed · rc=0 0 chẩn đoán (actionlint 1.7.7 + shellcheck 0.9.0 CÓ MẶT) | Có |
| 54/54 mutants semantic+fixture-LỌT+rc1, fixture_run_separate cho ca short-circuit | tái lập TRỌN 54 trên clone: 54/54, (killed, tập LỌT) khớp TỪNG mutant; đúng 1 ca fixture_run_separate (powershell-known-subset) | Có |
| expansion-acceptance-r16 (14 ca) | tự đo 14/14 khớp errors + kind + bash -n | Có |
| portable-parser 219/202/202 hai phiên bản PS | KHÔNG replay bộ mẫu (chỉ là mẫu hữu hạn theo khai); tự dựng probe MỚI bằng ParseInput cùng phương pháp trên 5.1.26100.9278 + 7.6.6 (H1/H6) — nhất quán với khai, và tự tìm được biên mới (F-B) đúng như prompt dự liệu | Nhất quán |
| spec_hash lease r23 · prompt sha256 | sha256 tự tính khớp đủ 64 ký tự cả hai | Có |
| Răng theo TỪNG cửa MỚI | **KHÔNG khớp trọn** — charset carrier pwsh không có răng theo lớp ký tự (F-A); câu công bố ASCII/line lệch hành vi splitlines (F-B) | KHÔNG — F-A/F-B |
| A1/A5/A2/A6/CI · integration master c16bd329 | not_run/not_measured theo chỉ thị — KHÔNG đọc thành passed/failed; không ngoại lệ merge | Đúng trạng thái |
| A9 live · metadata_head/refset_sha256 | reviewer bị cấm mạng ⇒ KHÔNG ĐO ĐƯỢC tại chỗ; chỉ ghi nhận executor khai uniqueexec5both trước run | Đúng phạm vi |

## KẾT LUẬN THEO LỚP (trục Spec + Standards/Security cho từng lớp)
| lớp | verdict | căn cứ |
|---|---|---|
| 1. Installer/domain/invocation + job phụ | **approve** | H3 (installer xuyên carrier: sai pin/installer lạ/case-trap đều ĐỎ, KHÔNG đường đúc GHIM, KHÔNG biến ngoài-miền thành KHONG; job toàn-pwsh vẫn hoàn tất được hợp đồng) · H4 (job phụ + defaults giữ đủ pin/probe per-job); Spec khớp Miền công khai M7; Security fail-close đủ |
| 2. Lexer/structure/expansion/quoting/order/shell carrier | **approve** (hành vi; kèm F-B [P3] trục Spec — câu công bố, không hành vi) | Đ5 14/14 khớp bash; H2 12 ca dollar-guard khớp POSIX hoặc lệch đúng chiều CHẶN đã công bố; H1: C0/CRLF chặn, NEL/LS/PS vô hại (AST 1-statement trên CẢ HAI phiên bản PS bắt buộc, pin-smuggle ĐỎ); H6: mọi keyword-statement lọt carrier đều bị KPT end-to-end, câu "invocation-only" ĐỨNG ở mức hợp đồng loi_ruff_ci |
| 3. Consumer/spec/workflow/fixtures | **changes_requested** | tiêu chí lớp ("fixture bắt được mất chốt") đo ra F-A [P3]: 5 mutant nới charset carrier — bảng chữ cái MỚI của chính lượt vá — sống 531/531 với witness đổi màu đã chạy; phần còn lại SẠCH: 54/54 mutant executor tái lập, 10 mutant R15 chết đúng fixture cô lập, đếm 108 fixture khớp cấu trúc, A7 4+2 giữ màu, A8/byte-identity/actionlint+shellcheck/ruff đều khớp |

Approve tổng đòi CẢ BA lớp approve ⇒ **changes_requested** (không hạ assurance, không đổi model/provider).

## KẾT LUẬN CUỐI (hai dòng đầu tệp là canonical và ĐÃ CHỐT — không còn là placeholder)
- verdict: **changes_requested** · reviewed_sha `ff146f16f26f1eb59d7a3839d5cc48811b13daac`
  (tree `f405a78c241100fe14a0d824e1483a78bdb69357`).
- Findings: **P1=0 · P2=0 · P3=2** — F-A `ruff-fixture-thieu-rang-chot-moi`/bien-charset-pwsh-carrier [P3] ·
  F-B `ruff-docstring-pwsh-carrier-rong-hon-hanh-vi` [P3]. KHÔNG finding hành vi trên HEAD: mọi witness đều bị
  HEAD từ chối đúng hoặc được nhận VÔ HẠI (đã chứng minh bằng AST hai phiên bản PS); hai finding là lưới
  fixture + câu công bố — hướng đóng ≈ +13–15 fixture (+1 chốt ranh giới dòng nếu chọn chiều CHẶN cho F-B),
  ước 933→≤960 ≤ 1000, giữ đúng 2 path.
- Đối chiếu R15: F1 [P2] **ĐÃ VÁ THẬT** · F2 [P3] **ĐÃ VÁ THẬT** · F3 [P3] **ĐÃ VÁ THẬT** — cả 10 mutant sống
  của R15 nay CHẾT với leak cô lập đúng mệnh đề. Không phát hiện VÁ SINH LỖI MỚI trong phạm vi các finding cũ;
  F-A/F-B nằm trên bề mặt MỚI (carrier pwsh) do chính lượt vá thêm.
- Bảng săn: 7 hướng mới (2 lớp-1 · 3 lớp-2 · 2 lớp-3), 5 mutant carrier tự dựng (cả 5 sống → F-A; đối chứng 4
  mutant carrier executor bị giết trong cùng rig), 20 probe separator/keyword qua PS parser 5.1+7.6.6, 12 ca
  dollar-guard với bash -n, 12 probe installer/aux-job, tái đo 14 ca expansion, đếm lại 108 fixture mới.
- A1/A5/CI/A2/A6/A9-live/integration-master-mới: **not_run / KHÔNG ĐO ĐƯỢC** theo chỉ thị chủ kho — verdict này
  KHÔNG thay các phép đo ấy, KHÔNG phải ngoại lệ merge, KHÔNG mang quyền merge/land. Nếu lượt sau approve thì
  cross_approved CHỈ cho code review trên exact SHA. Verdict vận chuyển nguyên văn lên Issue #463 (chưa có PR),
  không phải GitHub native approval.
- Identity actual: provider **anthropic_claude** · model **claude-fable-5** · effort **max** · surface
  **claude_code** · transport **machine/local** — validator so `modelUsage` thô SAU run; R16 utility probe
  fable5-only KHÔNG được đọc thành bằng chứng giữ model cho lượt dài này (đúng chỉ thị prompt).
- Bất biến cuối lượt (ĐO SAU khi viết xong thân — xem Đ6): clone HEAD/tree không đổi, porcelain 0 dòng; trạng
  thái sạch chỉ là phép đọc tại thời điểm đó. Hiện vật reviewer: `VERDICT.md` + `scratch/` (hunt_rv.py ·
  hunt-rv.json · ps_probe.ps1 · ps_probe_input.json · ps_probe_out_{51,7}.json · mutants-carrier/ 5 tệp ·
  mutants-r16/ 54+1 tệp + mutation-r16.json · run_mutation_rv.py · mutation-rv.out · suite-head.txt ·
  delta-check.patch) — TẤT CẢ NGOÀI clone.
