verdict: changes_requested
reviewed_sha: f4005d203d2ac457322cef46ad63a694c749269a

# VERDICT — packet #463, lượt 11, reviewer claude (độc lập)

- review_class / effective_review_class: sensitive
- provider: claude · model yêu cầu: claude-fable-5 · effort: max · execution_surface: claude_code_cli · transport: machine
- P1: 0 · P2: 2 · P3: 1  (KẾT LUẬN CUỐI)
- Verdict theo lớp: lớp 1 (miền/installers) approve · lớp 2 (lexer/composition/shell) changes_requested ·
  lớp 3 (consumers/spec/layout) changes_requested ⇒ final: **changes_requested**.
- Findings: `ruff-khuon-chua-chung-minh-provisioning` [P2, stable slug — sub-class mới: shell-ngoài-miền
  thân-parse-vô-can thành KHONG] · `ruff-fixture-thieu-rang-chot-moi` [P2] · `ruff-kpt-thong-diep-khong-neu-nguyen-nhan` [P3].
- Bảng săn: 8 hướng độc lập (L1: H1,H2 · L2: H3,H4,H5 · L3: H6,H7,H8), mỗi lớp ≥2 hướng mới; đối chiếu
  lượt 10: ĐÃ VÁ THẬT toàn bộ phản ví dụ đã nêu, còn sub-class mới cùng lớp.
- A1/A5, CI: not_run theo lệnh chủ kho — KHÔNG khai passed. Verdict này KHÔNG phải GitHub native approval,
  KHÔNG phải quyền merge; executor vận chuyển nguyên văn tới Issue #463.

## Nhật ký hướng săn (append sau MỖI hướng)

### Neo và phép đo nền (không tính N)

```
git rev-parse HEAD                    = f4005d203d2ac457322cef46ad63a694c749269a  (khớp reviewed_sha)
tree                                  = 1a7b17f1f97000eb635820ade4e3f0e7ee1a7a98  (khớp)
parent                                = 3bbc6b46c2fb6066fa64088308ce30fe40f87aa5  (handed-off)
git status --porcelain                = RỖNG
git diff --numstat base..HEAD         = 581/92 ci_dang_ky_test.py + 126/6 ci.yml ⇒ 707 additions / 2 path (A8: 707 ≤ 1000, đúng 2 path) ✔
git diff --numstat 3bbc6b4..HEAD      = CHỈ .claude/dev/ci_dang_ky_test.py (+388/−185)
ci.yml blob SHA @3bbc6b4 = @HEAD      = cb025a5a704a8f73319fee4ddded0010678e8f02 ⇒ workflow GIỮ BYTE so handed-off ✔ (tuyên bố đã kiểm)
C:/Python313/python.exe -X utf8 -B .claude/dev/ci_dang_ky_test.py (KHÔNG --chay)
                                      = ĐĂNG KÝ 21/21 · RUFF CI 3/3 · PHẢN CHỨNG 181/181 đỏ đúng · TỔNG: ĐẠT · rc=0 (khớp freeze-registry.txt)
ruff check --select F                 = All checks passed, rc=0
actionlint .github/workflows/ci.yml   = rc=0, 0 chẩn đoán
```

### ĐỐI CHIẾU LƯỢT TRƯỚC — `ruff-khuon-chua-chung-minh-provisioning` [P2, lượt 10]

Lệnh: `C:/Python313/python.exe -X utf8 -B scratch/doi_chieu_r10.py` (probe gọi thẳng `_doc_run_ruff`/`loi_ruff_ci` của head). Output thật (cắt gọn):

```
H2a python -m Ruff --version        => KPT (fail-close)          [trước: nhận ([],3)]
H2b python -m 'ruff[all]' --version => KPT                        [trước: nhận]
H3a ruff[!]==0.15.15                => KPT                        [trước: GHIM]
H3b ruff[all,]==0.15.15             => KPT                        [trước: GHIM]
H3c ruff[all..x]==0.15.15 (PEP503 hợp lệ) => GHIM                 [đúng: pip nhận, extras bỏ qua]
H4a/H4b nối dòng giữa token         => GHIM + probe=True          [trước: tách token sai]
H5  $'--version' ANSI-C             => KPT «ruff $--version»      [ngoài miền ĐÃ CÔNG BỐ — hết misparse-thành-nhận]
H6  python -m ci_dang_ky_test --chay => registry=1                [trước: không nhận]
H8  probe trước VÀ sau install      => probe=True                 [trước: chỉ nhớ probe đầu]
H10 quote chưa đóng                 => KPT «trích dẫn chưa đóng», registry=-1  [trước: fallback split cấp bằng chứng]
H11a/b --help --version · check --version => probe=False          [trước: nhận làm probe]
H9  echo ruff.toml có điều kiện (vô can) => ([], 3) sạch          [trước: đường conditional dùng regex riêng báo lỗi oan]
r9-tab/-mruff/khoảng-trắng          => vẫn nhận đúng (giữ vá lượt 9)
r9-TOML-config trong probe          => probe=False — grammar r22 THU HẸP có công bố («hậu tố đúng --version»);
                                       probe thật của ci.yml là `ruff --version` trần nên không mất ca thật nào
```

**Chấm: ĐÃ VÁ THẬT ở cấp lớp đã nêu** — mọi phản ví dụ H2/H3/H4/H5/H6/H8/H9/H10/H11 của lượt 10 đổi màu đúng
(nhận đúng hoặc fail-close có công bố). Riêng TOML-config-probe: lượt 10 nhận, r22 từ chối — đây là THU HẸP MIỀN
được công bố trong docstring grammar, khai ở đây theo đúng luật «thu hẹp phạm vi phải khai thẳng», không phải vá hờ.
Slug giữ nguyên để xét tiếp bằng bảng săn bên dưới; verdict lớp chấm cuối sau các hướng mới.

Đã đọc prior-review-7/8/9/10.md. Lịch sử hướng đã đi (tránh lặp y nguyên): sentinel fixture, thứ tự/bối cảnh bước dời,
probe/install trong cùng run, PIP_TARGET env (đã RÚT theo chủ kho), kênh kết quả, YAML sai cấu trúc (r7); env tên vô hại/giá trị
xấu, cờ trình -u/-B/-I, probe whitespace/tab/module, ranh giới && ;, tín dụng chốt ghim, registry nhiều lần (r8); TOML nhiều
dòng, # trong nháy, -mruff, precedence env, tab registry, tương tác hai cửa, toán tử được quote làm dữ liệu (r9); biên tên gói,
module≠distribution, extras grammar, backslash-newline giữa token, ANSI-C quote, registry module/tuyệt đối, --chay qua ranh
giới lệnh, nhiều probe, đường conditional regex, fallback split sau lỗi shlex, --version sai chế độ (r10). A1/A5/CI: not_run
theo lệnh chủ kho — KHÔNG khai passed.

## BẢNG SĂN

HƯỚNG 1: Họ installer CHƯA BIẾT + vị trí job PHỤ  [lớp 1 — biến thể mới: gia đình rộng pipx/conda/apt/npm/brew/cargo/uv-tool/easy_install/py-launcher, uninstall giữa run, uvx@pin; đặt trong job phụ]
  giả thuyết : nếu catch-all còn kẽ (một họ installer lạ rơi về KHONG) thì job phụ cài ruff ngoài khuôn mà cổng vẫn xanh
  lệnh       : C:/Python313/python.exe -X utf8 -B scratch/hunt1_installers.py
  output     :
    pipx/conda/apt-get/npm/brew/cargo/'uv tool install'/easy_install/'py -3 -m pip' → kind=KPT, registry=0, probe=False (cả 13/13)
    'pip download' · 'python -m pip download' · 'pip install ruff==0.15.15\npip uninstall -y ruff' → KPT
    'uvx ruff@0.15.15 --version' → KPT (không phải probe, không phải KHONG)
    job phụ [pipx|uv tool|conda] trong workflow đúng chuẩn → («CI không ghim Ruff 0.15.15 (job: ['phu'])», «CI không in probe ... ['phu']») — ĐỎ, nêu đúng job phụ
  kết luận   : KHÔNG PHẢI LỖI — unknown fail-close cả ở job phụ, đúng «ngoài miền không được biến thành KHONG»

HƯỚNG 2: Dạng requirement PIP-tương-đương/hợp lệ quanh pin  [lớp 1 — biến thể mới: ===, PEP440 zero-pad ==0.15.15.0, +local, marker trong nháy, URL-req «ruff @ file://», --index-url, biên chuẩn hoá tên (ruff. / .ruff / r..uff / ruff_ / «ruff [all]»), --dry-run]
  giả thuyết : nếu một dạng pin-tương-đương hoặc gần-pin được cấp GHIM (hoặc rơi về KHONG) thì bằng chứng ghim là giả hoặc install ruff biến hình thoát kiểm
  lệnh       : C:/Python313/python.exe -X utf8 -B scratch/hunt2_pin_equiv.py
  output     :
    ruff===0.15.15 · ==0.15.15.0 · +local · marker-«;»-trong-nháy · «ruff @ file:///tmp/ruff.whl» · ruff. · ruff_ · «ruff [all]» → KHONG_GHIM (đỏ trong ngữ cảnh, không job nào xanh nhờ chúng)
    --index-url … · .ruff==0.15.15 · --dry-run → KPT (fail-close; --dry-run KHÔNG cài thật nên cấp GHIM mới là lỗi — đã từ chối đúng)
    r..uff==0.15.15 → KHONG: PEP503 normalize «r-uff» ≠ ruff — pip cũng coi là gói KHÁC, nhất quán
    ruff-lsp / ruff-lsp==0.0.62 → KHONG — biên miền ĐÃ CÔNG BỐ («package khác chỉ nhận tên/extras + pin literal»); phụ thuộc bắc cầu là ngoài miền tĩnh theo chỉ thị chủ kho
    job chỉ có «===» hoặc «==0.15.15.0» → đủ 3 thông điệp ĐỎ
  kết luận   : KHÔNG PHẢI LỖI — không dạng nào được cấp GHIM ngoài pin đúng nghĩa; không dạng ruff nào rơi về KHONG

HƯỚNG 3: Ma trận escape/quote/continuation so ngữ nghĩa bash  [lớp 2 — biến thể mới: escape TÊN LỆNH (\pip, p\ip), tên lệnh trong nháy, continuation TRONG nháy kép/đơn, backslash cuối EOF, escape = và $, comment chứa lệnh liên quan/$()/backtick, # sau toán tử/giữa token, nối nháy đơn]
  giả thuyết : nếu lexer cho argv KHÁC bash ở một điểm thì hoặc nhận bằng chứng không chạy, hoặc chối lệnh bash chạy y hệt mà không fail-close
  lệnh       : C:/Python313/python.exe -X utf8 -B scratch/hunt3_quote_escape.py
  output     :
    \pip · p\ip · "pip" · 'pip' · escape-= · 'ruff=''=0.15.15' (nối nháy) → GHIM probe=True — bash chạy y hệt ⇒ NHẬN NHẤT QUÁN
    continuation trong nháy KÉP → GHIM (bash cũng bỏ \<nl> trong nháy kép) ✔
    continuation trong nháy ĐƠN → KPT (token chứa newline → tên không parse được — bash cũng lỗi pip runtime) ✔ fail-close
    backslash cuối EOF → KPT «escape chưa đóng» — bash sẽ bỏ \ và cài được ⇒ OVER-REJECT có công bố, chiều an toàn
    escape-$ → KHONG_GHIM (req sai, bash cũng đỏ pip) ✔
    comment: sau pin/sau «;»→GHIM đúng; chứa «pip install»/«$(...)»/backtick → KHONG, KHÔNG nổ ValueError ✔
    #-giữa-token → KHONG_GHIM (bash: literal, pip đỏ runtime) ✔
  kết luận   : KHÔNG PHẢI LỖI — mọi lệch bash↔lexer đều rơi về phía fail-close; không điểm nào nhận-sai

HƯỚNG 4: Ghép toán tử × newline (biên của miền newline/;/&&)  [lớp 2 — biến thể mới: && vắt qua newline hai chiều, ;; · «; ;» · &&& · ; đầu/cuối, redirection 2>&1, «\;» literal]
  giả thuyết : nếu «&& vắt dòng» hoặc «;» rỗng bị xử lý khác bash thì có run bash-hợp-lệ bị nhận sai cấu trúc lệnh (pin/probe ghép nhầm) hoặc run bash-lỗi được cấp bằng chứng
  lệnh       : C:/Python313/python.exe -X utf8 -B scratch/hunt4_operators.py
  output     :
    pin &&<nl>probe (bash hợp lệ) → GHIM probe=True; job ngữ cảnh → ([],3) XANH ✔ nhất quán bash
    pin<nl>&& · «;;» · «; ;» · «&&&» · «;» đầu → KPT (bash cũng lỗi) ✔ · «;» đuôi → GHIM ✔ · pipe → KPT ✔ · «\;» literal → GHIM ✔
    pin && probe && registry MỘT dòng → GHIM probe=True registry=1 ✔ (miền «newline/;/&&» công bố giữ đúng)
    «echo hi 2>&1» (bước VÔ CAN) → KPT: «&» cắt lệnh, sinh token ma «1» → unknown ⇒ job ngữ cảnh ĐỎ
      «CI không ghim Ruff 0.15.15 (job: ['gate'])» — over-reject ĐÚNG CHIỀU fail-close («mọi lệnh ngoài grammar bị
      từ chối» đã công bố; ci.yml thật không có 2>&1 — RUFF CI 3/3 xanh), NHƯNG thông điệp chẩn đoán nói «không
      ghim» trong khi nguyên nhân là «bước ngoài miền» — trace có sẵn trong _doc_run_ruff mà không được in.
  kết luận   : KHÔNG PHẢI LỖI (lớp) — mọi ca lệch đều đỏ đúng chiều; ghi nhận 1 điểm chất lượng chẩn đoán (xem P3 cuối)

HƯỚNG 5: Độ kín của bộ chọn shell — «các shell khác ngoài miền»  [lớp 2 — biến thể mới: thân PARSE-VÔ-CAN dưới shell ngoài miền; defaults mức WORKFLOW; pwsh lệch POSIX ở nối nháy; shell kiểu dữ liệu lạ]
  giả thuyết : nếu phép soi shell chỉ chạy khi parse-POSIX «trông đáng quan tâm» thì một bước shell ngoài miền có thân vô-can-theo-POSIX được tha — trong khi docstring công bố «các shell khác ngoài miền»
  lệnh       : C:/Python313/python.exe -X utf8 -B scratch/hunt5_shell_selector.py
  output     :
    (a)  body «x=__import__('os').system('pip install ruff==0.16.0')» parse POSIX → 1 token khớp regex assignment
         ⇒ kind=KHONG, registry=0, any_probe=False ⇒ điều kiện soi shell (p[0]!=KHONG or p[3] or p[4]) KHÔNG kích hoạt
         ⇒ job [cài đúng + bước shell:python thân-gán + registry] → ([], 3) — CỔNG XANH.
         Runtime thật: GitHub chạy thân bằng python ⇒ os.system cài ruff==0.16.0 SAU pin, TRƯỚC registry;
         phép gán không đổi exit code ⇒ bước xanh ⇒ registry chạy với ruff≠pin, cả ba chốt vẫn xanh. LỖI (fail-open).
    (a2) đối chứng: shell:python thân «print('hi')» → parse KPT ⇒ bị soi shell ⇒ ĐỎ — phép soi CHỈ chạy khi
         misparse-POSIX tình cờ «đáng quan tâm»; tha/chặn phụ thuộc hình dạng POSIX của văn bản KHÔNG-POSIX.
    (b)  defaults.run.shell mức WORKFLOW = python → ĐỎ (đường đọc có thật) — nhưng KHÔNG fixture nào phủ mức này
         (6 fixture shell chỉ phủ step + job-defaults) ⇒ đột biến bỏ nhánh workflow-level sẽ đo ở HƯỚNG 6.
    (c)  pwsh (TRONG miền) + «'ruff==''0.15.15'» → ([],3) XANH; bash-argv: ruff==0.15.15 (đúng pin) nhưng
         pwsh-argv: ruff=='0.15.15 ⇒ pip LỖI TO ở runtime ⇒ lệch «argv chung» có thật nhưng đổ về ĐỎ ỒN ÀO,
         không phải bypass im lặng — ghi nhận, không thành finding riêng.
    (d)  shell kiểu int/list/dict → KPT ĐỎ, không crash ✔ fail-close.
  kết luận   : LỖI (sub-class mới của lớp nhận dạng miền): bước shell-ngoài-miền chỉ bị từ chối KHI thân
               tình-cờ-parse-đáng-quan-tâm; thân vô-can-theo-POSIX biến bước ngoài miền thành KHONG —
               đúng hình «ngoài miền không được biến thành KHONG» mà lease/`viec_dau_tien` cấm.

HƯỚNG 6: Đột biến PHẪU THUẬT từng mệnh đề chốt MỚI r22 + tái kiểm 2 mutant tự khai  [lớp 3 — biến thể mới: 3 mutant chưa ai chạy (chốt -1-poison; defaults.run.shell mức workflow; tín dụng probe xuyên bước); mỗi mutant chạy TRỌN suite bản sao ROOT-ghim]
  giả thuyết : nếu một mệnh đề chốt sống mà không fixture nào chết khi gỡ nó thì chốt ấy không răng — «cửa không có mutant là cửa sẽ âm thầm hở lại»
  lệnh       : C:/Python313/python.exe -X utf8 -B scratch/hunt6_mutants.py ; ... hunt6b_semantic_ab.py
  output     :
    m1-bo-chot-neg1 (bỏ «not any(-1 in flags…)» dòng 460)      → rc=0, PHẢN CHỨNG 181/181, TỔNG ĐẠT — SỐNG
    m2-bo-workflow-shell-default (bỏ nhánh data.defaults dòng 407) → rc=0, 181/181, TỔNG ĐẠT — SỐNG
    m3-bo-probe-xuyen-buoc → rc=1, LỌT đúng {probe-buoc-sau, probe-hai-phia} — răng CÓ ✔
    m4-shell-luon-trong-mien → rc=1, LỌT đúng 5 fixture shell — KHỚP mutation-r22.json «shell-domain» ✔
    m5-unknown-thanh-khong → rc=1, LỌT đúng 9 fixture — KHỚP mutation-r22.json «default-unknown» ✔
    A/B không-tương-đương (hunt6b): registry-runner NGOÀI hợp đồng ở job phụ («python .claude/dev/ci_dang_ky_test.py»
    thiếu --chay · «--chay --mutant …») ⇒ base=«CI không provision Ruff trước test registry…» / m1=[] XANH;
    defaults.run.shell=python mức WORKFLOW ⇒ base=3 lỗi / m2=[] XANH — cả hai chốt SỐNG và KHÔNG tương đương.
  kết luận   : LỖI (lớp 3 — A7 «fixtures có răng»): HAI mệnh đề chốt r22 đang sống, không tương đương,
               mà 181 fixture không có răng cho mệnh đề nào — gỡ chúng là suite vẫn 181/181 + main rc=0.
               (Tái kiểm 2/9 mutant tự khai: khớp từng tên fixture — count tự khai KHÔNG bị thổi phồng.)

HƯỚNG 7: Biên YAML của consumer — khoá job TRÙNG (last-wins), alias, job «uses:», jobs/steps rỗng  [lớp 3 — biến thể mới so r7-H8 (scalar/list): trùng khoá + anchor + reusable-workflow]
  giả thuyết : nếu PyYAML last-wins cho khoá trùng thì một ci.yml «bản tốt đè bản xấu» qua được loi_ruff_ci đơn lẻ — hỏi tầng nào chặn
  lệnh       : C:/Python313/python.exe -X utf8 -B scratch/hunt7_yaml_boundary.py ; actionlint -no-color scratch/dup2.yml
  output     :
    7a dup-good-last → ([],3) XANH đơn lẻ (last-wins thật); dup-bad-last → 3 lỗi ĐỎ
       actionlint (fixture đủ runs-on): «key "gate-registry" is duplicated in "jobs" section … [syntax-check]» rc=1
       ⇒ tầng A3/actionlint (chốt BẮT BUỘC của chính packet, chạy trong CI) chặn; GitHub cũng từ chối file trùng id
    7b steps qua anchor/alias → ([],3) giải đúng ✔
    7c job «uses:» (reusable workflow hợp lệ GitHub) → «CI YAML jobs/steps ngoài miền» ĐỎ — over-reject ỒN ÀO,
       fail-close; bố cục hiện tại không dùng uses: ⇒ không chặn oan hôm nay
    7d jobs rỗng / steps rỗng → ĐỎ «không job nào cài Ruff» — KHÔNG có pass rỗng (vacuous) ✔
  kết luận   : KHÔNG PHẢI LỖI — lỗ last-wins bị lớp actionlint-bắt-buộc + GitHub chặn (phòng thủ tầng có đo);
               các biên còn lại đều fail-close ồn ào

HƯỚNG 8: Tự kiểm HARNESS 181 fixture — «ca có MẶT» phải là «ca có ĐO»  [lớp 3 — biến thể mới so r8-H1 (công cụ nháp): nhắm harness SẢN PHẨM 181 ca]
  giả thuyết : nếu harness dedupe im tên trùng, hoặc không tiêu thụ kỳ vọng, thì 181/181 là số đếm không đo gì
  lệnh       : C:/Python313/python.exe -X utf8 -B scratch/hunt8_harness.py
  output     :
    (1) nhân đôi tên fixture (bản sao) → AssertionError «trung ten ca phan chung: ruff-ci-registry-module», rc=1 — KHÔNG dedupe im ✔
    (2) lật kỳ vọng heredoc-la-du-lieu 0→1 (bản sao) → PHẢN CHỨNG 180/181, LỌT đúng tên, TỔNG ĐỎ, main rc=1 ✔
    (3) bản gốc: 181 dòng ĐỘT BIẾN in ra, 181 tên phân biệt, 181/181, 0 LỌT, rc=0 — số khai là số ĐO ✔
        (suite không tự neo tổng-số-ca; neo ngoài nằm ở freeze-registry.txt ≡ sandbox-registry.txt — đã diff IDENTICAL)
  kết luận   : KHÔNG PHẢI LỖI — harness có răng với tên trùng và kỳ vọng lật; số 181 tự đếm lại được

## BẢNG ĐO — mọi con số đã đo, kể cả cái khớp

| khẳng định | khai / hợp đồng | đo được | khớp? |
|---|---|---|---|
| Exact head | f4005d203d2ac457322cef46ad63a694c749269a | rev-parse đầu + CUỐI lượt: khớp; status rỗng cả hai lần | Có |
| Tree | 1a7b17f1f97000eb635820ade4e3f0e7ee1a7a98 | `git cat-file -p HEAD` khớp | Có |
| Base | bb7013c7669da19304a8769e5b25f8c1f8951e9c | dùng đúng cho numstat | Có |
| A8 additions | 707 ≤ 1000, đúng 2 path | 581+126=707, 2 path; delta lượt 11 CHỈ tệp test (+388/−185) | Có |
| ci.yml giữ byte so 3bbc6b4 | tuyên bố trong nhiệm vụ | blob cb025a5a70… Ở CẢ HAI commit | Có |
| Registry test (KHÔNG --chay) | freeze-registry.txt: 181/181, rc=0 | tự chạy: ĐĂNG KÝ 21/21 · RUFF CI 3/3 · PHẢN CHỨNG 181/181 · TỔNG ĐẠT · rc=0; sandbox≡freeze (diff IDENTICAL) | Có |
| Ruff F | freeze-ruff.txt rc=0 | All checks passed, rc=0 | Có |
| actionlint ci.yml | freeze-actionlint.txt rc=0 | rc=0, 0 chẩn đoán | Có |
| 9 mutant tự khai (mutation-r22.json) | mỗi mutant: semantic đổi + fixture LỌT + main rc=1 | tái kiểm 2/9 (shell-domain · default-unknown): tập fixture LỌT KHỚP TỪNG TÊN, rc=1 | Có (mẫu 2/9) |
| Răng probe xuyên bước | chốt mới dòng 454 | mutant m3 chết đúng {probe-buoc-sau, probe-hai-phia} | Có |
| Răng chốt −1-poison (dòng 460) | A7 đòi «fixtures có răng» | mutant m1 SỐNG 181/181 + A/B đổi hành vi | **KHÔNG** |
| Răng defaults.run.shell mức WORKFLOW (dòng 407) | như trên | mutant m2 SỐNG 181/181 + A/B đổi hành vi | **KHÔNG** |
| «Shell khác ngoài miền» (docstring) | mọi bước shell ngoài miền bị từ chối | thân parse-vô-can dưới shell:python → ([],3) XANH; đối chứng print('hi') → ĐỎ | **KHÔNG** |
| A3(1) bộ ba mức job | (if,matrix,timeout) 3 job bằng nhau | if=None cả 3 · matrix.os cùng chuỗi · timeout=60 cả 3 | Có |
| A3(2b) tiền tố 9 bước | 2 job mới = gate | prefix9 True cả hai | Có |
| A4 | timeout 60 mỗi job, không mức bước | 60/60/60, step-timeout=False cả 3 | Có |
| Ca đổi màu A7 | 4 fixture bố cục giữ màu | có mặt trong 181 (chua-tach/da-tach-dung/thieu-ruff/sau-registry), 181/181 đỏ đúng | Có |
| Miền công bố newline/;/&& | nhận đúng | && vắt dòng nhận; dạng bash-lỗi fail-close (H4) | Có |
| Registry ngoài hợp đồng bị chặn | «đúng --chay» | thiếu --chay / --chay --mutant → before=False, ĐỎ (base) | Có (nhưng không răng — m1) |
| A1/A5, CI, A2-conclusions, A6-readback | not_run theo lệnh chủ kho | không chạy CI, không dispatch, không mạng | **KHÔNG ĐO ĐƯỢC — đúng trạng thái** |
| Cây review nguyên trạng | không sửa/commit vào cay-kho | status rỗng + HEAD không đổi (đầu và cuối lượt); mọi bản sao/đột biến nằm scratch/ | Có |

## Hai trục bổ sung

**Trục Spec:** M7/A7 — consumer đọc bố cục mới (3 job) và tương thích lùi (fixture chua-tach): giữ. Grammar đóng
được CÔNG BỐ tại docstring `loi_ruff_ci` đúng như prompt yêu cầu; đối chiếu docstring↔hành vi: install/probe/
registry/opaque/substitution/heredoc/comment khớp phép đo (H1–H4, H7); MỘT câu docstring («các shell khác ngoài
miền») KHÔNG được thực thi trọn — xem P2-1. A8 707/1000 · 2 path ✔. Không đụng `bang_chung_xanh`/`MOI`/`chay_moi`
ngoài seam đã có (AST-level: chỉ vùng Ruff thay đổi — đối chiếu diff). Không thêm chốt env — đúng quyết định
thu hẹp của chủ kho (không coi là thiếu).

**Trục Standards/Security:** Ruff F=0; actionlint=0; suite THUẦN TĨNH với fixture (không thực thi nội dung
fixture — `_cuoi_thay_lenh`/`_dong_logic` chỉ parse chuỗi; subprocess duy nhất trong phan_chung là green_test.py
tự sinh, hành vi có sẵn từ trước); không đọc/ghi secrets; không đường ghi mới. Idiom comment tiếng Việt + chú
thích «vì sao» giữ đúng nếp tệp. Regex `_TEN_GOI`/lexer tuyến tính theo n, đệ quy substitution có trần depth 16.

## Kết luận theo LỚP

| lớp | verdict | căn cứ |
|---|---|---|
| 1. Nhận dạng miền/installers | **approve** | H1, H2: unknown fail-close mọi chỗ kể cả job phụ; pin-tương-đương không lọt; KHONG chỉ cấp cho miền công bố |
| 2. Lexer/composition/order | **changes_requested** | H3, H4 sạch; H5 = phản ví dụ LỚP: bước shell-ngoài-miền thân parse-vô-can → biến thành KHONG (P2-1) |
| 3. Consumers/spec/layout | **changes_requested** | A2/A3/A4/A8 giữ; harness có răng (H8) NHƯNG hai chốt mới không răng (H6 → P2-2) |

## ĐỐI CHIẾU LƯỢT TRƯỚC — chấm cuối

- `ruff-khuon-chua-chung-minh-provisioning` [P2 lượt 10]: **ĐÃ VÁ THẬT cho toàn bộ phản ví dụ đã nêu** (bảng
  ĐỐI CHIẾU đầu tệp, 18 ca đo lại); grammar đóng + công bố là bước tiến cấu trúc thật. **NHƯNG cùng lớp còn
  MỘT sub-class mới** (H5) ⇒ giữ slug, mô tả triệu chứng riêng bên dưới — KHÔNG reset lịch sử.

### ruff-khuon-chua-chung-minh-provisioning  [P2]  Bước shell-ngoài-miền chỉ bị từ chối khi thân «trông đáng quan tâm» — thân parse-vô-can biến ngoài-miền thành KHONG

TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py:440` (điều kiện `(p[0] != "KHONG" or p[3] or p[4])` đứng TRƯỚC
`_shell_trong_mien`), `:403-410` (`_shell_trong_mien` — đúng nhưng chỉ được hỏi có điều kiện), docstring `:419`
(«các shell khác ngoài miền» — lời công bố rộng hơn thực thi).

VẤN ĐỀ: Phép soi shell chỉ chạy cho bước mà parse-POSIX cho kết quả «đáng quan tâm». Thân viết cho shell
NGOÀI miền (python/cmd/template) được parse bằng luật POSIX — một phép đo vô nghĩa cho ngôn ngữ đó — và nếu
kết quả tình cờ là KHONG thì bước được THA không cần hỏi shell. Phản ví dụ lớp (đo, hunt5):
`shell: python` + run `x=__import__('os').system('pip install ruff==0.16.0')` → parse POSIX = MỘT token khớp
regex assignment ⇒ KHONG ⇒ job đủ pin/probe/registry vẫn `([], 3)` XANH — trong khi runtime GitHub chạy thân
bằng python: cài ruff==0.16.0 SAU pin, TRƯỚC registry, exit 0 ⇒ registry chạy với ruff ≠ pin, cả ba chốt xanh.
Đối chứng cùng shell, thân `print('hi')` → ĐỎ — tha/chặn phụ thuộc HÌNH DẠNG POSIX của văn bản không-POSIX,
tức đúng hình «ngoài miền bị biến thành KHONG» mà lease `viec_dau_tien` cấm và docstring hứa ngược lại.
Ranh giới scope khai thẳng: thân script là opaque theo chỉ thị chủ kho — bản vá KHÔNG được diễn giải thân
python; nhưng quyết định «shell khác ngoài miền» là của CHÍNH grammar này (6 fixture đang khẳng định nó),
và nó phải áp NHẤT QUÁN theo shell ĐÃ GIẢI, không theo may rủi của misparse.

ĐÃ THỬ VÁ: không — mô tả bằng lời: đưa phép giải shell LÊN TRƯỚC parse; bước có `run` mà shell đã-giải nằm
ngoài (None|bash|sh|pwsh|powershell) ⇒ gán thẳng `("KHONG_PHAN_TICH_DUOC", "shell ngoài miền", False, -1, False)`
bất kể thân. ci.yml thật chỉ dùng bash + 1 bước pwsh (đã grep) ⇒ không chặn oan hôm nay; fixture shell-step-uu-tien
vẫn xanh (shell đã-giải = bash). Kèm một fixture thân-vô-can (ví dụ chính ca trên hoặc thân `x=1`) kỳ vọng ≥1.
Ước tăng: ~4-8 dòng, trong biên A8 (707→≤1000).

ĐÃ THỬ NGHIỆM: scratch/hunt5_shell_selector.py — output nguyên văn trong HƯỚNG 5; đối chứng (a2) chứng minh
đường soi shell hoạt động khi parse «đáng quan tâm».

ĐỘ TIN: cao (đo trực tiếp trên hàm sản phẩm tại exact SHA; hành vi runtime của shell:python là hành vi
GitHub Actions đã tài liệu hoá — không cần chạy CI để thấy phép gán không đổi exit code).

### ruff-fixture-thieu-rang-chot-moi  [P2]  Hai mệnh đề chốt r22 đang sống, không tương đương, mà 181 fixture không có răng

TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py:460` (mệnh đề `not any(-1 in flags for flags in registry.values())`)
và `:406-407` (nhánh `data.get("defaults"…)` — defaults.run.shell mức WORKFLOW).

VẤN ĐỀ: A7 đòi «fixtures có răng»; doctrine kho: «cửa không có mutant là cửa sẽ âm thầm hở lại». Đo (hunt6/6b):
· m1 gỡ mệnh đề −1-poison ⇒ PHẢN CHỨNG 181/181 + main rc=0 (SỐNG); A/B: lời gọi registry-runner NGOÀI hợp đồng
  ở job phụ («python .claude/dev/ci_dang_ky_test.py» thiếu --chay; «--chay --mutant …») — base ĐỎ «CI không
  provision Ruff trước test registry», m1 XANH []. Mệnh đề này là đường TỪ CHỐI DUY NHẤT cho lớp «gọi registry
  ngoài hợp đồng nhưng lexer sạch» (kind của nó là KHONG nên không qua bad_pin).
· m2 gỡ nhánh workflow-defaults ⇒ 181/181 + rc=0 (SỐNG); A/B: defaults.run.shell=python mức workflow — base 3
  lỗi, m2 XANH. 6 fixture shell chỉ phủ step-level + job-defaults.
Cả hai đều là chốt MỚI của r22 — không nằm trong 9 mutant tự khai của mutation-r22.json, nên bảng mutant
tự khai «9/9 killed» đúng nhưng KHÔNG phủ hai cửa này.

ĐÃ THỬ VÁ: không — mô tả bằng lời: thêm 2 fixture vào `_FX`: (i) job phụ với run
`python .claude/dev/ci_dang_ky_test.py` (không --chay), kỳ vọng ≥1; (ii) workflow có
`defaults: {run: {shell: python}}` với job cài đúng, kỳ vọng ≥1 (cần cho `_wf` nhận defaults hoặc dựng dict
tay như fixture shell-job hiện có). Ước ~4-6 dòng, trong biên A8.

ĐÃ THỬ NGHIỆM: scratch/hunt6_mutants.py (chạy TRỌN suite bản sao cho từng mutant, ROOT ghim về cay-kho)
+ scratch/hunt6b_semantic_ab.py (A/B chứng minh không-tương-đương). Output nguyên văn ở HƯỚNG 6.

ĐỘ TIN: cao.

### ruff-kpt-thong-diep-khong-neu-nguyen-nhan  [P3]  Thông điệp đỏ nói «không ghim Ruff» cho job mà nguyên nhân thật là «bước ngoài miền»; trace có sẵn nhưng bị vứt

TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py:448` (bad_pin gom mọi kind ≠ KHONG/GHIM), `:466` (thông điệp),
`:360/:369` (trace của KPT đã được tính nhưng không được in).

VẤN ĐỀ: Job có pin/probe/registry ĐÚNG nhưng chứa một bước vô can ngoài grammar (đo H4: `echo hi 2>&1` —
token ma «1» → KPT) nhận thông điệp «CI không ghim Ruff 0.15.15 (job: ['gate'])» — người sửa sẽ soi dòng pin
(đang đúng) thay vì bước ngoài miền. Chiều fail-close ĐÚNG, chỉ chẩn đoán sai chỗ. Vá lời: nối `trace` của
phần tử KPT vào thông điệp (≤2 dòng). Không blocker.

ĐÃ THỬ NGHIỆM: scratch/hunt4_operators.py (job ngữ cảnh cuối output).

ĐỘ TIN: cao.

## Giới hạn & khai báo cuối

- A1/A5 và mọi phép đo cần CI/GitHub: **not_run/KHÔNG ĐO ĐƯỢC theo lệnh chủ kho** — không được đọc thành passed.
  Verdict này là **CODE REVIEW cục bộ trước merge**, không phải quyền merge, không phải GitHub native approval;
  executor vận chuyển nguyên văn tới Issue #463 (no-CI, không mở PR).
- Không mạng, không CI, không --chay, không full gate; không sửa/commit vào cay-kho (status rỗng, HEAD giữ
  f4005d2 — đo đầu và cuối lượt). Mọi đột biến chạy trên BẢN SAO trong scratch/mutants với ROOT ghim về cay-kho.
- Không soạn payload tấn công: mọi phản ví dụ là chuỗi cấu hình tĩnh đi qua parser offline, cùng họ với fixture
  sẵn có trong tệp; không nội dung nào được thực thi.
- provider=claude · model yêu cầu=claude-fable-5 · effort=max · execution_surface=claude_code_cli ·
  transport=machine — danh tính runtime do validator so `modelUsage`, không tự chứng nhận.
- Ghi chú không-phải-finding: (i) thu hẹp miền probe TOML-config đã công bố; (ii) backslash-EOF over-reject;
  (iii) job `uses:` chưa hỗ trợ (over-reject ồn ào — sẽ chặn oan nếu mai này ci.yml dùng reusable workflow);
  (iv) pwsh nối-nháy lệch POSIX đổ về đỏ-ồn-ào runtime (câu «họ shell có argv chung» hơi rộng nhưng hệ quả
  an toàn); (v) probe uvx/uv-run đo một install KHÁC pin về mặt ngữ nghĩa — thuộc runtime provenance, chủ kho
  đã loại khỏi phạm vi, không tính lỗi; (vi) suite không tự neo tổng 181 — neo ngoài ở freeze/verdict.
