verdict: changes_requested
reviewed_sha: 79b75cdb6cf2737c3bd911ee7313969c2cfce62e

> Trạng thái: **HOÀN TẤT** — hai dòng trên là canonical và ĐÃ CHỐT tại mục "KẾT LUẬN CUỐI".
> (Placeholder đầu lượt cũng là `changes_requested` đúng quy trình; kết luận cuối trùng giá trị nên
> không đổi chữ nào — xác nhận MỘT lần khi đóng. P1=0 · P2=0 · P3=1.)
> Reviewer: CLAUDE độc lập — provider **anthropic_claude** · model **claude-fable-5** · effort **max**
> · surface **claude_code** · transport **machine/local**. #463 lượt 18, revision 24 / generation 5, sensitive.
> base_sha bb7013c7669da19304a8769e5b25f8c1f8951e9c · expected tree 41b49168ba2fc322d7bc42fbe9e0a11013049df7.

## Trạng thái đo
- [x] Đọc cross-review-SKILL.md · CONTEXT · CLAUDE.md (mục liên quan) · PROTOCOL §8+§13 · SPEC-r24 · LEASE-r24 · g5-resume-authority/g5-lease-record/r18-fence · PRIOR_HUNT_INDEX (R7–R17) · prior-review-16-original · prior-review-17-PERMISSION-INVALID (chỉ như lịch sử săn) · TOÀN delta (diff.patch ≡ tự sinh) và vùng tương tác (kiem/chay_moi/bang_chung_xanh/main)
- [x] Đ0/Đ6: HEAD/tree/status khớp exact ĐẦU và CUỐI lượt; base là ancestor; root commit khớp
- [x] Đ1: A8 **949/1000**, đúng **2 path**; ci.yml blob `cb025a5a70…` @HEAD = @ff146f16 = @3bbc6b46 (freeze) — workflow BYTE-IDENTICAL
- [x] Đ2: registry **671/671** · 21/21 · 4/4 · 3/3 · rc=0 — tự chạy trên clone, KHÔNG `--chay`; output ≡ r17-freeze-registry.txt (677=677 dòng sau chuẩn hoá newline); Ruff 0.15.15 F rc=0; actionlint 1.7.7 rc=0 (shellcheck 0.9.0 CÓ MẶT)
- [x] Đ3: TÁI LẬP TRỌN **87/87 mutant GIẾT** (phương pháp EXECUTOR_MUTATION_METHOD nguyên văn, chỉ đổi neo R→clone, artifact scratch); per-mutant (killed/semantic/separate/rc/tập-fixture-LỌT) KHỚP executor **0 lệch**; đúng 1 fixture_run_separate (powershell-known-subset)
- [x] ĐỐI CHIẾU R16: F-A **ĐÃ VÁ THẬT** · F-B **ĐÃ VÁ THẬT** (tự đo, không nhận lời khai; R17 invalid không dùng làm căn cứ)
- [x] BẢNG SĂN **6 hướng MỚI độc lập** (lớp 1: H1·H2 · lớp 2: H3·H4 · lớp 3: H5·H6) — **1 LỖI (F-18A, P3)** · 5 KHÔNG PHẢI LỖI
- [x] Chuỗi định danh: sha256(PROMPT.md)=e0ce4404… ≡ --expected-prompt-sha256 ≡ prompt.snapshot; sha256(SPEC-r24)=79ba77c3… ≡ spec_sha256/spec_hash LEASE-r24; permission_denials RỖNG trong cả lượt (không tool nào bị deny)

## Nhật ký đo

### Đ0 — Identity clone (đo lúc mở phiên)
```
$ git rev-parse HEAD          → 79b75cdb6cf2737c3bd911ee7313969c2cfce62e  (KHỚP exact)
$ git rev-parse "HEAD^{tree}" → 41b49168ba2fc322d7bc42fbe9e0a11013049df7  (KHỚP exact)
$ git status --porcelain      → 0 dòng · merge-base --is-ancestor bb7013c7 HEAD → rc=0
$ git rev-list --max-parents=0 HEAD → 394e93468fc8d84ec20938e6df8fb7ab72b2cc37 (KHỚP expected-root)
```

### Đ1 — A8 + freeze workflow + delta
```
$ git diff --numstat bb7013c7..HEAD → 823+92 ci_dang_ky_test.py · 126+6 ci.yml ⇒ 949 additions ≤ 1000, ĐÚNG 2 path
$ ls-tree ci.yml @HEAD = @ff146f16 = @3bbc6b46 = cb025a5a704a8f73319fee4ddded0010678e8f02 (BYTE-IDENTICAL freeze)
$ git diff bb7013c7..HEAD tự sinh ≡ diff.patch được giao (73393 = 73393 byte, identical)
```

### Đ2 — Baseline suite + Ruff + actionlint (clone, KHÔNG --chay, KHÔNG CI, KHÔNG thực thi fixture/installer)
```
$ C:\Python313\python.exe -X utf8 -B .claude/dev/ci_dang_ky_test.py (cwd=clone) → rc=0
  ĐĂNG KÝ: 21/21 · LAUNCHER WINDOWS: 4/4 · RUFF CI: 3/3 · PHẢN CHỨNG: 671/671 đỏ đúng · TỔNG: ĐẠT
  đếm "ĐỘT BIẾN " = 671 · "LỌT" = 0 — hai số dương bằng nhau, không tin rc trần
$ output ≡ r17-freeze-registry.txt (bỏ dòng rc, chuẩn hoá newline): IDENTICAL, 677 = 677 dòng
$ ruff 0.15.15 check --no-cache --select F → All checks passed, rc=0 (khớp r17-freeze-ruff.txt)
$ actionlint 1.7.7 ci.yml → rc=0, 0 chẩn đoán; shellcheck 0.9.0 CÓ MẶT (khớp r17-freeze-actionlint.txt)
```

### Đ3 — TÁI LẬP 87 MUTANT (EXECUTOR_MUTATION_METHOD.py.txt nguyên văn, chỉ thay MỘT dòng neo:
R = clone cay-kho; mọi artifact vào scratch/rv18/mutants; KHÔNG ghi clone)
```
KILLED 87/87 — từng mutant: semantic_changed AND ≥1 fixture LỌT AND rc=1 AND "TỔNG: ĐỎ"
So mutation-r17.json executor: tập tên = nhau (87=87); (killed, semantic_changed, fixture_run_separate,
rc, tập-fixture-LỌT) khớp TỪNG MUTANT — mảng diffs RỖNG. Đúng 1 separate: powershell-known-subset.
Hiện vật: scratch/rv18/mutants/ (87×.py + 87×.txt + baseline + mutation-r17.json) · compare_mutation.py
```

### Đ4 — Cấu trúc workflow thật (V-baseline, không tính N)
```
jobs @HEAD = {gate, gate-registry, gate-packet-loop}; bộ ba (if=None, matrix.os chuẩn hoá, timeout=60)
CẢ BA BẰNG NHAU; env parity ✓; 0 timeout-minutes mức bước; on:/concurrency == base (kể cả khoá YAML True
— không so hai None); tập (name,if,run,shell,with,env) 40 bước base ⊆ 58 bước head, chỉ THÊM 18 bản sao
9 bước thiết lập; 2 bước dời ("test registry", "packet-loop selftest") GIỮ NGUYÊN dict từng trường
(base_n=1, head_n=1, equal=true — if giữ nguyên/null); tiền tố 9 bước khớp THEO TÊN+THỨ TỰ đúng câu A3;
byte-level chỉ lệch CHÚ THÍCH trong scalar run của bước 0 (r226 rút gọn thành con trỏ "xem job gate") —
đúng ghi chú độ mịn đã có từ R15-H5, không phải finding mới. Hiện vật: scratch/rv18/a3_struct.py
```

### Đ6 — Bất biến cuối lượt (đo SAU toàn bộ phép đo, trước khi chốt verdict)
```
$ git rev-parse HEAD          → 79b75cdb6cf2737c3bd911ee7313969c2cfce62e  (KHÔNG đổi)
$ git rev-parse "HEAD^{tree}" → 41b49168ba2fc322d7bc42fbe9e0a11013049df7  (KHÔNG đổi)
$ git status --porcelain      → 0 dòng (sạch — trạng thái chỉ là phép đọc tại thời điểm đó)
Clone không bị ghi trong cả lượt: mọi mutant/probe chạy trên BẢN SAO trong scratch/rv18, ROOT ghim clone
chỉ để ĐỌC; python -B; PowerShell/Bash KHÔNG được thực thi (chỉ phân tích tĩnh qua consumer).
```

---

## ĐỐI CHIẾU LƯỢT TRƯỚC
R16 là verdict hợp lệ gần nhất (changes_requested, P3=2). R17 raw tự khai approve nhưng **KHÔNG được
chấp nhận** (permission denial — không assurance, không valid round); bằng chứng của nó chỉ dùng làm
lịch sử săn để tránh lặp; MỌI phép đo dưới đây tự tái lập trong rig của tôi.

| finding R16 | trạng thái | bằng chứng TỰ ĐO |
|---|---|---|
| F-A `ruff-fixture-thieu-rang-chot-moi`/bien-charset-pwsh-carrier [P3] — 5 mutant nới charset carrier sống 531/531 | **ĐÃ VÁ THẬT** | Đ3 rig của TÔI: widen-arg-dollar · widen-arg-dquote · widen-arg-semicolon · widen-arg-brace · widen-first-digit đều **BỊ GIẾT** trong 87/87, tập fixture-LỌT khớp executor từng cái; 5 witness trên HEAD (`echo $X` · `echo "ok"` · `echo hi; wc` · `echo {x}` · `2fa.sh x`, shell pwsh) đều 2 lỗi — HEAD từ chối đúng (hunt-rv18.json khoá V_FA_FB) |
| F-B `ruff-docstring-pwsh-carrier-rong-hon-hanh-vi` [P3] — splitlines nhận NEL/LS/PS ngoài ASCII công bố | **ĐÃ VÁ THẬT** | Chiều CHẶN đã thi công: `echo hi\x85echo ok` · U+2028 · U+2029 · CRLF → **2 lỗi** ở CẢ pwsh lẫn powershell trên HEAD; đối chứng dương `echo hi\n` · `echo hi\necho ok\n` → 0 lỗi; mutant `powershell-unicode-splitlines` (revert splitlines) **BỊ GIẾT** trong Đ3; docstring "invocation/dòng LF" khớp hành vi |

Không phát hiện VÁ SINH LỖI MỚI trong phạm vi hai finding cũ (RUFF CI thật 3/3; A7 4 ca + 2 phản chứng
ci.yml thật giữ màu trong 671/671; workflow byte-identical). F-18A dưới đây KHÔNG phải hồi quy của delta
r17 — các cửa liên quan có từ trước và chưa lượt nào đo phủ raise-site.

---

## BẢNG SĂN — 6 hướng MỚI độc lập (lớp 1: H1·H2 · lớp 2: H3·H4 · lớp 3: H5·H6)

Đối chiếu PRIOR_HUNT_INDEX R7–R16 và 8 hướng của output invalid R17: KHÔNG hướng nào dưới đây trùng —
H1 là trục argv/path của lời gọi registry (R13-H6 chỉ đo if/hai-bước); H2 là trục chuẩn hoá TÊN GÓI
(R13-H1 đo grammar option/URL/marker); H3 là parity boundary-scanner↔inner-lexer trên heredoc/function/
depth trong `$()` (R15-H2/R16-H2 đo dollar-guard/nối dòng, R14-H5 đo biên NHẬN heredoc — khác câu hỏi);
H4 là đúc-GHIM qua QUOTE/ESCAPE-normalization (R15-H3 đo wrapper/prefix); H5 là BẢN ĐỒ PHỦ RAISE-SITE
của lưới fixture + mutant closure cho cửa chưa răng (chưa lượt nào chạy phương pháp này); H6 là độ chính
xác QUY KẾT thông điệp lỗi theo họ fixture (ngoài 2 ca nguyen-nhan có sẵn). Replay Đ2/Đ3/Đ4 và V_FA_FB
KHÔNG tính vào N. Script + JSON: scratch/rv18/{hunt_rv18.py, hunt-rv18.json, h5_cover2.py,
h5-cover-rv18.json, h5_mutants.py, h5-mutants/}.

### H1 [LỚP 1] — Đóng/mở nhận dạng lời gọi registry theo argv/path — KHÔNG PHẢI LỖI
giả thuyết : nếu biến thể path/quote/flag của `ci_dang_ky_test.py --chay` đúc được WRONG-GREEN cho chốt
             "Ruff trước registry" (neo vào caller giả) hoặc thoát vị từ -1 thì M7 gãy ở lớp nhận dạng
lệnh       : loi_ruff_ci trên 13 bố cục (lookalike-only/fake+real cùng-khác job/quoted/escaped/backslash/
             module±cờ trình/mjoined/$(pwd)-path/case-path/double---chay/2 bước thật/pin giữa 2 lời gọi)
             + kiem(workflows=…) làm backstop cho ca lookalike
output     : lookalike-only → loi_ruff_ci 0 lỗi NHƯNG kiem() đỏ "CI không gọi mục đăng ký …/ci_dang_ky_test.py"
             + "CI không gọi nhóm đăng ký mới"; fake-then-pin-then-real → 1 (gi neo caller ĐẦU ⇒ đỏ);
             fake+real hai job → 1 (caller không duy nhất); backslash-path/case-path → 1 (không caller —
             khớp bash: tệp không tồn tại); dynamic-path → 2 (bad ⇒ -1 poison); double---chay → 1 (-1);
             quoted/escaped/--chay, module±cờ, mjoined → 0 (shlex ≡ bash, chỉ neo — kiem() vẫn đòi chuỗi
             canonical); 2 bước thật sau pin → 0; pin giữa 2 lời gọi → 1
kết luận   : KHÔNG PHẢI LỖI — không đường WRONG-GREEN: mọi tổ hợp fake+real đều đỏ (unique-caller/thứ tự),
             mọi dạng động/lệch đều -1 hoặc không-caller (fail-close), spelling không canonical bị kiem() chặn

### H2 [LỚP 1] — Chuẩn hoá tên gói: có spelling nào pip giải về ruff mà thoát GHIM-hoặc-đỏ? — KHÔNG PHẢI LỖI
giả thuyết : nếu một spelling mà pip resolve về project `ruff` được phân loại KHONG (unrelated) thì lệnh cài
             ruff lách được nghĩa vụ pin/probe
lệnh       : _phan_loai_cai_ruff trên 16 spelling (UPPER/mixed/extras-hoa, ruff. / ruff_ / ruff- tail,
             ==0.15.15.0 / +cpu / 0.15.150, r-u-f-f, Ruff.Ruff, .ruff, space-eq, comment-tail, uv tool, pipx)
output     : RUFF/rUfF/RuFf[ALL]==0.15.15 → GHIM (pip case-insensitive — pin thật); ruff./ruff_/ruff- +
             mọi version lệch (kể cả 0.15.15.0 tương đương PEP440) → KHONG_GHIM (đỏ, chặn oan an toàn);
             .ruff/space-eq/uv tool/pipx → KPT (đỏ); r-u-f-f==… và Ruff.Ruff==… → KHONG
kết luận   : KHÔNG PHẢI LỖI — mọi spelling resolve-về-ruff đều GHIM hoặc đỏ, không đường KHONG-hoá;
             `r-u-f-f`/`ruff-ruff` là PROJECT PyPI KHÁC (PEP503), thuộc diện "gói khác cài tĩnh" mà miền
             M7 đã chốt cho phép (như PyYAML) — ghi nhận GIỚI HẠN THEO TÊN của miền, đã cố định bằng
             chỉ thị chủ kho, không phải lỗi của bản vá

### H3 [LỚP 2] — Parity boundary-scanner `$()` ↔ inner-lexer trên heredoc/function/depth/comment — KHÔNG PHẢI LỖI
giả thuyết : nếu `_cuoi_thay_lenh` (không biết heredoc/redirect) và `_dong_logic` đệ quy bất đồng mà rơi
             fail-OPEN (KHONG cho lệnh related) thì `$()` là cửa cài ẩn
lệnh       : _phan_loai_cai_ruff + loi_ruff_ci end-to-end trên 14 ca (heredoc quoted/unquoted trong $(),
             body chứa `)`, f(){…}, lồng 16/17, comment-only, trailing-op, related ở lệnh THỨ HAI,
             `')'` trong nháy, `\)` escape, if/{ } trong $())
output     : heredoc-body-paren/unquoted-$( trong body/f()/nest-17/trailing-op/related-thứ-hai → KPT
             (fail-close, e2e ≥1 lỗi); heredoc quoted đóng đúng/nest-16/comment-only/`')'`/`\)`/if/{ } toàn
             opaque → KHONG (an toàn — khớp ngữ nghĩa dữ liệu/bash, không related nào lọt); e2e 4/4 khớp
kết luận   : KHÔNG PHẢI LỖI — mọi bất đồng boundary↔inner đều ValueError→KPT; tập được nhận trong $()
             đúng câu "chỉ lệnh opaque được phân tích đệ quy" (khuôn if/{ } của opaque thuộc grammar công bố)

### H4 [LỚP 2] — Đúc GHIM qua chuẩn hoá quote/escape — KHÔNG PHẢI LỖI
giả thuyết : nếu shlex-view của consumer lệch bash-view trên MỘT spelling thì GHIM đúc được mà bash chạy
             lệnh khác (hoặc pin thật bị trượt trong khi dạng lách được nhận)
lệnh       : _phan_loai_cai_ruff trên 15 spelling ("pip"/pi''p/p\ip/'pip', ruff==0.15.'15', "ruff==0.15.15",
             ruff"=="…, đuôi space-trong-nháy, \r-trong-nháy, $V-trong-nháy-kép, PIP hoa, ~ruff, glob `?`)
output     : 15/15 khớp kỳ vọng — GHIM CHỈ ở các spelling mà bash tokenize Y HỆT (quote-removal thuần);
             mọi ký tự có khả năng phân kỳ (C0/space trong nháy, $, ~, glob) → KHONG_GHIM/KPT (đỏ)
kết luận   : KHÔNG PHẢI LỖI — không đường đúc GHIM lệch bash; các lớp phân kỳ đều bị bad-flag/pin-mismatch
             chặn trước khi tới phân loại

### H5 [LỚP 3] — Bản đồ phủ RAISE-SITE của lưới 671 fixture + mutant closure cửa chưa răng — **LỖI (F-18A, P3)**
giả thuyết : nếu tồn tại cửa fail-close (raise ValueError) mà KHÔNG fixture nào đi qua, thì gỡ cửa ấy
             sống trọn suite — đúng lớp "fixture bắt được mất chốt" mà tiêu chí lớp 3 canh
lệnh       : wrap `_dong_logic` qua __globals__ của bản copy ghim-clone, chạy TRỌN phan_chung(), so tập
             thông điệp ValueError bắt được với 29 literal trong nguồn; rồi dựng 4 mutant gỡ-từng-cửa,
             mỗi cái: witness A/B qua chính loi_ruff_ci + chạy TRỌN suite
output     : 25/29 cửa có fixture đi qua; **4 cửa 0-phủ**: "escape chưa đóng" (:231) · "heredoc ngoài miền"
             (:269) · "heredoc chưa đóng" (:298) · "lồng command substitution ngoài miền" (:208).
             4 mutant gỡ cửa: **CẢ 4 SỐNG 671/671 rc=0, 0 LỌT**; witness:
             drop-depth-guard: lồng 17×`$(echo …)` HEAD 2 → mutant **0** (FAIL-OPEN flip) ·
             drop-heredoc-unclosed: `cat <<'E'\nx\n` HEAD 2 → **0** · drop-second-heredoc:
             `cat <<'A' <<'B'\nx\nB\n` HEAD 2 → **0** · drop-escape-eof: `echo hi\` HEAD 2 →
             **IndexError crash** (fail-crash, không phải fail-open)
kết luận   : **LỖI** — 3 mutant KHÔNG-tương-đương (flip 2→0 nhìn thấy qua chính loi_ruff_ci) sống trọn
             suite + 1 cửa chỉ còn bảo vệ bằng crash; phân tích ở Finding F-18A. Đối chứng rig có răng:
             cùng rig này giết 87/87 mutant executor (Đ3)

### H6 [LỚP 3] — Độ chính xác QUY KẾT lỗi theo họ fixture (ngoài 2 ca nguyen-nhan có sẵn) — KHÔNG PHẢI LỖI
giả thuyết : nếu một họ fixture âm đỏ vì check KHÁC check nó canh (mis-attribution kiểu F02) thì mutant-kill
             của họ ấy đo nhầm cửa
lệnh       : tái dựng 8 bố cục đại diện (da-tach-thieu-ruff / ruff-sau-registry / probe-truoc-cai /
             hai-job-registry / shell-vo-can / guard-syntax-op / alphabet-dollar / registry-if), đọc
             VECTOR 3 thông điệp (ghim/probe/provision) + chuỗi "ngoài miền cú pháp: [job/bước]"
output     : 8/8 khớp vector dự kiến từng họ; các họ cú-pháp/carrier đỏ đúng bằng cặp (pin-check với
             reason nêu ĐÚNG "gate/bước 2") + (registry-check qua -1), không họ nào đỏ nhờ check vô can
kết luận   : KHÔNG PHẢI LỖI — quy kết thông điệp đúng cửa theo từng họ; không thấy mis-attribution còn sót

---

## FINDING

### F-18A — `ruff-fixture-thieu-rang-chot-moi`  [P3]  (GIỮ stable slug R11/R15/R16; sub-class MỚI: cua-heredoc-va-do-sau-khong-rang)
Bốn cửa fail-close của lexer POSIX không có răng fixture — 3 mutant gỡ cửa KHÔNG-tương-đương sống trọn 671/671
TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py:208` (`lồng command substitution ngoài miền`) · `:231`
(`escape chưa đóng`) · `:269` (`heredoc ngoài miền` — nhánh heredoc THỨ HAI trên một dòng) · `:298`
(`heredoc chưa đóng`).
VẤN ĐỀ + COUNTEREXAMPLE (đều ĐÃ CHẠY — H5): bản đồ phủ raise-site đo bằng wrapper trên chính suite cho
thấy 4/29 thông điệp fail-close KHÔNG BAO GIỜ được kích trong 671 fixture. Gỡ từng cửa: (a) gỡ chốt
depth>16 ⇒ `X=$(echo …)` lồng 17 tầng đổi màu 2→0 qua chính `loi_ruff_ci` — thân ngoài miền công bố được
NHẬN (fail-open); (b) gỡ raise heredoc-chưa-đóng ⇒ `cat <<'E'\nx\n` 2→0; (c) thu hẹp cửa :269 còn nhánh
m-None ⇒ heredoc thứ hai `cat <<'A' <<'B'\nx\nB\n` 2→0 (heredoc A bị đè lặng lẽ); (d) gỡ cửa escape-EOF ⇒
`echo hi\` chuyển từ 2 lỗi có kiểm soát thành **IndexError không được bắt** (`_doc_run_ruff` chỉ bắt
ValueError) — không fail-open nhưng đổi failure-mode thành crash. CẢ 4 mutant chạy TRỌN suite: 671/671
"đỏ đúng", rc=0, 0 LỌT ⇒ lưới không bắt được mất chốt. Cùng rig giết 87/87 mutant executor (đối chứng
rig không hiền). Đây đúng hình dạng F1-R15 (khuôn) và F-A-R16 (charset) tái diễn trên HỌ CỬA THỨ BA
(heredoc/độ sâu/escape-EOF): khuôn FIXTURE/MUTANT-KHOÁ đã áp cho khuôn shell, charset carrier, operator,
redirect, expansion, C0 — nhưng chưa áp cho họ cửa này; bộ 87 của executor cũng không có mutant nào cho
4 cửa ấy (soát danh sách case).
VÌ SAO P3 (không phải P2): sản phẩm trên HEAD từ chối ĐÚNG mọi witness (cột HEAD = 2 lỗi); cả khi nới,
không đường cài ẩn mở ra — thân heredoc là DỮ LIỆU cả trong bash lẫn consumer, `$(` trong heredoc động
vẫn bị cửa :297 chặn, related trong `$()` vẫn bị cửa "lệnh liên quan" chặn ở mọi tầng đệ quy; lỗ CHỈ ở độ
mịn lưới cho hồi quy tương lai — đúng phép phân hạng mà R14/R15/R16 đã dùng cho lớp này.
HƯỚNG SỬA CẤP LỚP (bằng lời, không patch — sensitive): mỗi cửa MỘT fixture âm mà CHỈ cửa ấy chặn, trên
bước shell mặc định như họ syntax-* hiện có (một ca lồng `$()` >16 tầng thuần opaque · một ca heredoc
quoted không đóng · một ca hai heredoc trên một dòng · một ca thân kết thúc bằng `\` trần); kèm 3–4 mutant
dạng gỡ-cửa (như scratch/rv18/h5-mutants) vào bộ EXECUTOR_MUTATION_METHOD cho lượt sau — mutant escape-EOF
đồng thời chốt failure-mode (đỏ có kiểm soát thay vì traceback). Ước +8–14 dòng Python ⇒ 949→≤963 ≤ 1000,
giữ đúng 2 path.
TEST/MUTANT GIỮ CHỐT: 4 mutant + 4 witness + 4 log suite trọn trong `scratch/rv18/h5-mutants/`
(h5-mutants.json); bản đồ phủ trong `scratch/rv18/h5-cover-rv18.json`.
NGUY CƠ HỒI QUY: ≈0 — không đổi mã sản phẩm; HEAD đã đỏ sẵn mọi witness; fixture mới xanh ngay trên HEAD.
ĐÃ THỬ VÁ: không — write set packet + sensitive (§8 loại trừ patch-as-hint cho bề mặt này).
ĐỘ TIN: cao — 4 cặp A/B HEAD↔mutant + 4 lượt suite trọn + bản đồ phủ 25/29, tất cả trong hiện vật scratch.

---

## BẢNG ĐO — lời khai executor ↔ đo được (độc lập)
| khẳng định executor | đo được (reviewer) | khớp? |
|---|---|---|
| exact head/tree/base 79b75cdb…/41b49168…/bb7013c7… | rev-parse đầu VÀ cuối lượt, porcelain 0 cả hai lần; root commit khớp | Có |
| A8 949/1000, đúng 2 path | numstat 823+126=949, đúng 2 path | Có |
| workflow unchanged (freeze 3bbc6b46) | blob cb025a5a70… @HEAD = @ff146f16 = @freeze | Có |
| registry 671/671 · 21/21 · 4/4 · 3/3 · rc=0 | tự chạy KHÔNG --chay: y hệt; output ≡ r17-freeze-registry.txt (677=677) | Có |
| Ruff F rc=0 · actionlint rc=0 | All checks passed (ruff 0.15.15) · rc=0, 0 chẩn đoán (actionlint 1.7.7 + shellcheck 0.9.0 CÓ MẶT) | Có |
| 87/87 semantic mutants, đúng 1 separate | tái lập TRỌN 87 trên clone: 87/87; per-mutant khớp 0 lệch; separate = powershell-known-subset | Có |
| 140 fixture mới cô lập từng lớp ký tự carrier | 671−531=140 khớp; F-A/F-B witnesses đỏ đúng trên HEAD | Có |
| "Răng theo TỪNG cửa" (tiêu chí lớp 3 các lượt trước đặt ra) | **KHÔNG khớp trọn** — 4 cửa POSIX-lexer (heredoc×2, depth, escape-EOF) 0-phủ fixture; 3 mutant gỡ cửa sống trọn suite (F-18A) | KHÔNG — F-18A |
| prompt/spec sha256 | tự tính khớp đủ 64 ký tự cả hai; PROMPT ≡ snapshot | Có |
| A1/A5/A2/A6/CI · integration master | not_run / not_measured theo chỉ thị — KHÔNG đọc thành passed/failed; không ngoại lệ merge | Đúng trạng thái |
| A9 live (unique_exec6_both, fence audit=passed) | reviewer bị cấm mạng ⇒ KHÔNG ĐO ĐƯỢC tại chỗ; chỉ ghi nhận fence r18 | Đúng phạm vi |

## KẾT LUẬN THEO LỚP (trục Spec + Standards/Security cho từng lớp)
| lớp | verdict | căn cứ |
|---|---|---|
| 1. Installer/domain/invocation + job phụ | **approve** | H1: không WRONG-GREEN cho chốt registry qua 13 biến thể argv/path, unique-caller + -1 fail-close, kiem() backstop chuỗi canonical; H2: mọi spelling resolve-về-ruff đều GHIM hoặc đỏ, không KHONG-hoá, không đúc GHIM; miền theo-tên đúng chỉ thị chủ kho |
| 2. Lexer/structure/expansion/order/shell carrier | **approve** | Hành vi trên HEAD từ chối đúng MỌI witness của mọi hướng (H3/H4 + V_FA_FB); parity `$()` fail-close trọn; quote/escape-normalization không mở đường; F-B đóng chiều CHẶN, LF-boundary xác nhận cả hai shell; carrier/backstop giữ nghĩa vụ installer ở mọi tầng |
| 3. Consumer/spec/workflow/fixtures | **changes_requested** | tiêu chí lớp ("fixture bắt được mất chốt") đo ra F-18A [P3]: 4 cửa fail-close 0-phủ, 3 mutant gỡ cửa KHÔNG-tương-đương sống 671/671 với witness flip 2→0 đã chạy + 1 cửa chỉ còn crash-protection; phần còn lại SẠCH: 87/87 tái lập khớp từng mutant, A8/byte-identity/freeze/actionlint+shellcheck/ruff khớp, cấu trúc A3/A4 parity đủ (Đ4), quy kết lỗi đúng cửa (H6) |

Approve tổng đòi CẢ BA lớp approve ⇒ **changes_requested** (không hạ assurance, không đổi model/provider).

## KẾT LUẬN CUỐI (hai dòng đầu tệp là canonical và ĐÃ CHỐT — không còn là placeholder)
- verdict: **changes_requested** · reviewed_sha `79b75cdb6cf2737c3bd911ee7313969c2cfce62e`
  (tree `41b49168ba2fc322d7bc42fbe9e0a11013049df7`).
- Findings: **P1=0 · P2=0 · P3=1** — F-18A `ruff-fixture-thieu-rang-chot-moi`/cua-heredoc-va-do-sau-khong-rang
  [P3]. KHÔNG finding hành vi trên HEAD: mọi witness đều bị HEAD từ chối đúng; finding thuần lưới fixture —
  hướng đóng ≈ +4 fixture (+3–4 mutant khoá vào bộ executor), ước 949→≤963 ≤ 1000, giữ đúng 2 path.
- Đối chiếu R16: F-A [P3] **ĐÃ VÁ THẬT** · F-B [P3] **ĐÃ VÁ THẬT** — 5 mutant charset + revert-splitlines
  đều CHẾT trong rig của tôi, witness đỏ đúng trên HEAD; KHÔNG VÁ SINH LỖI MỚI. R17 invalid: không kế thừa
  kết luận nào, mọi số tự đo lại (87/87 per-mutant 0 lệch, suite ≡ freeze).
- Bảng săn: 6 hướng mới (2 lớp-1 · 2 lớp-2 · 2 lớp-3) — 1 LỖI · 5 KHÔNG PHẢI LỖI; 4 mutant gỡ-cửa tự dựng
  (3 chứng minh lưới thiếu răng bằng flip 2→0, 1 chứng minh failure-mode crash), bản đồ phủ 25/29 raise-site,
  13 probe registry-argv, 16 probe tên-gói, 14 probe `$()`-parity, 15 probe quote-forging, 8 phép quy kết.
- A1/A5/A2/A6/CI · A9-live · integration master mới: **not_run / KHÔNG ĐO ĐƯỢC** theo chỉ thị chủ kho —
  verdict này KHÔNG thay các phép đo ấy, KHÔNG phải ngoại lệ merge, KHÔNG mang quyền merge/land/deploy.
  Nếu lượt sau approve thì cross_approved CHỈ cho code review trên exact SHA.
- Identity actual: provider **anthropic_claude** · model **claude-fable-5** · effort **max** · surface
  **claude_code** · transport **machine/local** — validator so `modelUsage`/`permission_denials` thô SAU run;
  trong lượt này KHÔNG tool call nào bị từ chối.
- Bất biến cuối lượt (Đ6): clone HEAD/tree không đổi, porcelain 0 dòng. Hiện vật reviewer: `VERDICT.md` +
  `scratch/rv18/` (run_baseline.py · suite-head-rv18.txt · diff-self.patch · gen_mutation.py · mutants/
  87×2+json · compare_mutation.py · hunt_rv18.py · hunt-rv18.json · consumer_copy_rv18.py · h5_cover.py ·
  h5_cover2.py · h5-cover-rv18.json · h5_mutants.py · h5-mutants/ 4×py+4×suite.txt+json · a3_struct.py) —
  TẤT CẢ NGOÀI clone.
