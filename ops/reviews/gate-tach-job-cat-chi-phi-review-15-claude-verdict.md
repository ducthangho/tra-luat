# VERDICT — #463 lượt 15 (revision23 / generation4) — REVIEWER CLAUDE độc lập

verdict: changes_requested
reviewed_sha: e5e8e2390db1c4a68ad0ee6febdf7d6ed0a39582

> Trạng thái: **HOÀN TẤT** — hai dòng trên là canonical và ĐÃ CHỐT tại mục "KẾT LUẬN CUỐI".
> (Đầu lượt hai dòng ấy là placeholder `changes_requested` đúng quy trình; kết luận cuối trùng giá trị
> placeholder nên không đổi chữ nào — xác nhận MỘT lần khi đóng, không xoá nhật ký. P1=0 · P2=1 · P3=2.)

---

## Nhật ký đo

### Đ0 — Trạng thái clone (đo lúc mở phiên)
```
$ git rev-parse HEAD            → e5e8e2390db1c4a68ad0ee6febdf7d6ed0a39582   (KHỚP exact reviewed_sha)
$ git rev-parse "HEAD^{tree}"   → 2046f927fe8375c0bd98f2dc2d6a23fab1c14da9   (KHỚP exact tree)
$ git status --porcelain        → (rỗng — sạch)
$ git log --oneline -6          → e5e8e23 / 86b0feb / 664aaf3 / f4005d2 / 3bbc6b4 / dcd7039
```
Kết luận: clone đúng SHA/tree, detached, sạch tại thời điểm đọc.

### Đ1 — Baseline: A8, byte-identity, suite, Ruff, actionlint, spec hash (đo trên clone)
```
$ git diff --numstat bb7013c..HEAD → 746+92 (.claude/dev/ci_dang_ky_test.py) · 126+6 (.github/workflows/ci.yml)
  ⇒ additions 746+126 = 872 ≤ 1000, ĐÚNG 2 path (KHỚP khai 872/1000, đúng 2 paths)
$ git rev-parse HEAD:.github/workflows/ci.yml == 3bbc6b4:.github/workflows/ci.yml
  → cb025a5a704a8f73319fee4ddded0010678e8f02 CẢ HAI ⇒ workflow BYTE-IDENTICAL với 3bbc6b4 ✓ (khớp khai)
$ C:/Python313/python.exe -X utf8 -B .claude/dev/ci_dang_ky_test.py → rc=0
  ĐĂNG KÝ: 21/21 · LAUNCHER WINDOWS: 4/4 · RUFF CI: 3/3 · PHẢN CHỨNG: 423/423 đỏ đúng · TỔNG: ĐẠT
  (đếm dòng "ĐỘT BIẾN" = 423 — hai số dương BẰNG NHAU, không tin rc trần)
$ diff (freeze minus dòng chú thích rc) vs (tự chạy) → IDENTICAL; freeze ≡ sandbox-registry.txt IDENTICAL
$ ruff check --no-cache --select F .claude/dev/ci_dang_ky_test.py → All checks passed, rc=0
$ actionlint .github/workflows/ci.yml → rc=0, 0 chẩn đoán
$ sha256(SPEC-r23.md) = 7089ad0d7c4322ffe5677f100cd31f44115fb15af1f7efe4087b7b267e7de482 — KHỚP spec_hash lease r23
```
Kết luận: mọi lời khai baseline của executor TỰ TÁI LẬP trên exact SHA. A1/A5/CI vẫn not_run theo chỉ thị — KHÔNG đọc thành passed.

### Đ2 — XÁC MINH VÁ R14 (V-pass, không tính vào N hướng mới)
**V1 — P2 `opaque-structural-grammar`: 6 ca addendum + thành viên SÓT + 2 biên** (`scratch/v1_r14_p2_6ca.py`,
import module từ clone, carrier opaque giữa pin/probe đúng và registry đúng trong MỘT job gate):
```
'echo hi ||'            errors=2  KPT trace='thiếu vế phải toán tử'
'echo hi |'             errors=2  KPT trace='thiếu vế phải toán tử'
'echo hi ;;;'           errors=2  KPT trace='toán tử ngoài miền'
'echo hi && || echo hi' errors=2  KPT trace='thiếu lệnh'
'echo hi >'             errors=2  KPT trace='redirect thiếu đích'
'V=${x'                 errors=2  KPT trace='parameter expansion ngoài miền hoặc chưa đóng'
'echo "${x"'            errors=2  KPT trace='parameter expansion …'   ← thành viên SÓT (R14-D2), có fixture syntax-parameter-double
'echo hi ||| echo ok'   errors=2  KPT trace='toán tử ngoài miền'      ← biên op-list addendum đòi
'echo hi > | wc'        errors=2  KPT trace='redirect thiếu đích'     ← biên redirect-đích addendum đòi
```
Cả 6 ca gốc ĐỎ với trace TỪNG LUẬT đúng khuôn addendum-D; thành viên sót trong nháy kép ĐỎ và CÓ fixture
(`syntax-parameter-double`); mutant nới-danh-sách (`syntax-operator-widen` thêm `;;`) có trong bộ 33.
⇒ **P2 `ruff-khuon-chua-chung-minh-provisioning`/opaque-structural-grammar: ĐÃ VÁ THẬT (hành vi, tự đo).**
Trạng thái răng (mutant/fixture) kiểm ở Đ4.

**V2 — P3 `bien-nguong-C0`:** tuple fixture C0 nay là `("\r","\f","\v","\0") + chr(1..31 trừ 9,10,11,12,13)`
= **30 ký tự** (đủ cả biên trên U+001F và nửa trên U+000E–U+001E — đúng hướng sửa R14 và đúng chỉ thị
"C0 30 ký tự trừ TAB/NL", dòng 1120). Bốn ID cũ `c0-0..c0-3` GIỮ NGUYÊN (4 ký tự cũ đứng đầu tuple).
Hai mutant ngưỡng `<32→<14` (`c0-threshold-plain/escape`) nằm trong bộ 33 của executor — tái lập độc lập ở Đ3.
Đếm fixture khớp cấu trúc: 245 (r14) + 27 (syntax-op 9×3) + 47 (syntax-*) + 104 (26 ký tự C0 mới ×4) = **423** ✓.

### Đ3 — TÁI LẬP 33 MUTANT CỦA EXECUTOR (phương pháp EXECUTOR_MUTATION_METHOD, ROOT ghim CLONE)
`scratch/mutants/run_mutation.py` — chép nguyên case-list 33 mutant, mỗi mutant một TÊN TỆP RIÊNG (bài học
`.pyc`), chạy `-B`, cwd=clone, KHÔNG đụng đường dẫn nguồn ngoài sandbox. Kết quả (`mutation-rv.json`):
```
KILLED 33/33 — TỪNG mutant: semantic_changed=True AND >=1 fixture LỌT AND rc=1 AND "TỔNG: ĐỎ"
(mẫu tập LỌT khớp mutation-r15.json từng tên: c0-threshold-plain → c0-12..29-tran (18 LỌT) ·
 syntax-operator-widen → syntax-op-;;-giua/cuoi (2) · syntax-structure-consumer → 16 LỌT · …)
```
⇒ Lời khai executor **"33/33 semantic_changed AND fixture LỌT AND main rc1" TỰ TÁI LẬP ĐỘC LẬP** trên clone.
Hai mutant ngưỡng C0 của P3-R14 nay BỊ GIẾT (18 fixture LỌT mỗi cái) ⇒ **P3 `bien-nguong-C0`: ĐÃ VÁ THẬT.**

### Đ4 — MUTANT RIÊNG CỦA REVIEWER: săn cửa-không-răng (14 mutant tự dựng, cùng rig Đ3)
`scratch/mutants/run_mutation.py` (12) + `run_mutation2.py` (2). Đối chứng phương-pháp-có-răng:
`rv-unclosed-eof-off` BỊ GIẾT (3 fixture LỌT) · `rv-op-widen-pipeamp` BỊ GIẾT (2 LỌT) — rig không hiền.
**CHÍN mutant KHÔNG TƯƠNG ĐƯƠNG mà SỐNG 423/423 (rc=0, TỔNG: ĐẠT):**
```
mutant (gỡ/thu hẹp)                       witness (bash -n rc=2 trừ khi ghi khác)     HEAD    mutant
rv2-header-thieu-lenh-off  (dòng 197)     '{ ; echo hi; }' · '{ && echo hi; }'        2 lỗi → 0 lỗi KHONG
rv-inline-header-off       (dòng 198)     'if true; then if false; fi'                2 lỗi → 0 lỗi KHONG
rv-khung-shell-gate-off    (dòng 195-196) 'do echo hi\n'                              2 lỗi → 0 lỗi KHONG
rv-cond-compound-off       (dòng 181)     'if true\nif false; then echo a; fi\nthen echo b; fi'
                                          (bash -n rc=0 — POSIX-VALID, chiều CHẶN)    2 lỗi → 0 lỗi
rv-redirect-drop-newline   ("\n;|&<>#"→bỏ \n)  'echo hi >\nwc'                        2 lỗi → 0 lỗi KHONG
rv-redirect-drop-pipe      (bỏ |)         'echo hi > | wc'  ← ĐÍCH DANH addendum R14  2 lỗi → 0 lỗi KHONG
rv-redirect-drop-amp       (bỏ &)         'echo hi > & echo ok'                       2 lỗi → 0 lỗi KHONG
rv-redirect-drop-ltgt      (bỏ <>)        'echo hi > > f'                             2 lỗi → 0 lỗi KHONG
rv2-op-widen-3pipe         (thêm "|||")   'echo hi ||| echo ok' ← ĐÍCH DANH addendum  2 lỗi → 0 lỗi KHONG
(+ rv-redirect-narrow-max ";#" cũng sống — bản gộp của 4 mutant drop)
```
`rv-orphan-close-off` chết bằng **IndexError** (lỗi VÔ CAN thoát khỏi `except ValueError`) — KHÔNG tính giết
thật theo doctrine tín-dụng-giả; guard vẫn chịu tải (mutant làm suite sập), chỉ ghi nhận trạng thái.
HEAD từ chối ĐÚNG mọi witness (cột HEAD) ⇒ lỗ nằm ở LƯỚI FIXTURE, không ở hành vi cổng — xem Finding F1/F2.

---

## BẢNG SĂN — 6 hướng MỚI độc lập (lớp 1: H3-H4 · lớp 2: H1-H2 · lớp 3: H5-H6)
Đối chiếu `PRIOR_HUNT_INDEX.md`: không hướng nào trùng đầu vào R7–R14 (bare-`$`-opaque, khuôn-generator,
static-pin-qua-wrapper, aux-job-tĩnh, prefix9-granularity, guard-teeth-mutation đều 0 hit trong index;
wrapper/prefix cũ của R7-R13 đo bằng đối số ĐỘNG `"$PACKAGE"` — hướng H3 đo chiều ĐÚC CHỨNG CHỈ với pin TĨNH).
Script: `scratch/hunt_h1_h6.py` · `scratch/mutants/run_mutation*.py`. Replay V1/V2/Đ3 KHÔNG tính vào N.

### H1 [LỚP 2] — họ bare-`$` expansion trên carrier opaque so câu docstring MỚI r15 — **LỖI (P3, F3)**
Giả thuyết: câu docstring mới "Parameter chỉ nhận ${TEN} hoặc ${TEN:-literal}…; các expansion khác ngoài
miền" (dòng 482-483) rộng hơn hành vi. Đo 12 dạng: `echo $X` · `echo "$X"` · `echo $@` · `echo "$@"` ·
`echo $1` · `echo $*` · `echo $?` · `echo $$` · `echo $!` · `echo $-` · `V=$X` · `echo $X#tail` ⇒ **TẤT CẢ
KHONG** (nhận, cờ bad chỉ đánh related). Đối chứng related: `pip install $X` · `pip install ruff==$V` ⇒ KPT ✓.
POSIX XCU 2.5.2/2.6.2: mọi dạng trên LÀ parameter expansion ⇒ theo câu công bố phải "ngoài miền" mà đo được
là NHẬN. Chứng chỉ KHÔNG sai (input POSIX-valid + unrelated), nhưng CÂU CÔNG BỐ sai/mơ hồ — và không thể sửa
MÃ theo câu: `ci.yml` THẬT dùng `$VAR`/`$$`/`"$(...)"` khắp nơi (`test -n "$PR_HEAD_SHA"` · `echo $$ >
"$RIENG/cgroup.procs"`) — siết là làm đỏ workflow thật (RUFF CI đang 3/3). ⇒ lỗi ở CÂU DOCSTRING.

### H2 [LỚP 2] — sweep soundness bash -n với GENERATOR MỚI quanh khuôn if/{}/redirect/param/heredoc — KHÔNG PHẢI LỖI
503 candidate (9 seed trái × 9 seed phải × 6 op + 20 ca ghép tay khuôn-lồng/redirect-trong-khuôn/param),
parser nhận **146**, cả 146 qua `bash --noprofile --norc -n` ⇒ **0 accepted-invalid**. Bao phủ đúng vùng
generator của executor KHÔNG chạm (executor: cặp toán tử + đuôi redirect; tôi: tổ hợp khuôn + thân lồng).
Cộng đối chứng accept-side H6-mini: `if true & then echo a; fi` · `{ echo a; } &` · `if…fi | wc -l` ·
hai câu if nối newline — đều KHONG đúng POSIX; `fi() { echo x; }` KPT đúng công bố (ngoặc trần).

### H3 [LỚP 1] — pin TĨNH qua wrapper/prefix: có đường nào ĐÚC GHIM xuyên wrapper không — KHÔNG PHẢI LỖI
`sudo/env/command/nice/time pip install ruff==0.15.15` · `pip3.12 install…` · `py -m pip install…` ·
`pip download ruff==0.15.15` ⇒ **đều KPT, probe=False** (không GHIM xuyên wrapper — fail-close đúng);
`\p\i\p install ruff==0.15.15` ⇒ GHIM và `pip "install" ruff==0.15.15` ⇒ GHIM — **ĐÚNG POSIX-tương-đương**
(escape/quote removal cho argv y hệt pip nhận thật, cùng lớp fixture `noi-giua-token`); `pip install
ruff==0.15.15 # ghi chú` ⇒ GHIM ✓; `pip install "ruff == 0.15.15"` (PEP508 có space) ⇒ KHONG_GHIM — CHẶN
oan-có-công-bố (pin literal `==0.15.15`), fail-close, khai để người viết workflow biết phải viết liền.

### H4 [LỚP 1] — nghĩa vụ pin/probe cho job PHỤ cài TĨNH (fixtures sẵn có chỉ phủ aux-job ĐỘNG) — KHÔNG PHẢI LỖI
Job `phu` cài `ruff==0.15.15` tĩnh KHÔNG probe ⇒ 1 lỗi "CI không in probe (job: ['phu'])" ✓; thêm probe ⇒ 0 ✓;
cài `ruff==0.15.14` ⇒ 2 lỗi (ghim + probe) ✓. Phân hoạch per-job giữ nguyên nghĩa vụ ở job phụ.

### H5 [LỚP 3] — A3/A4 đo trực tiếp trên ci.yml thật + độ mịn prefix9 — KHÔNG PHẢI LỖI (kèm ghi chú độ mịn)
3 job `gate`/`gate-registry`/`gate-packet-loop`: `timeout-minutes` 60/60/60 · job-`if` None×3 · 0 step-timeout ·
`matrix.os` CÙNG CHUỖI cả 3 · `fail-fast` False×3 · concurrency/`on:` như R10-14 (tệp byte-identical 3bbc6b4).
Prefix9 so theo (name/uses/run/shell/with/env): **run của bước 1 KHÁC BYTE** giữa gate và 2 job mới — chỉ khác
DÒNG COMMENT trong script (`# r226 — NGƯỠNG L2…` dài ↔ `# r226 — vì sao ghim…: xem chú thích cùng bước ở job
gate`), ba lệnh `git config` y hệt. SPEC-r23:328 đòi prefix9 **"theo tên, theo thứ tự"** ⇒ ĐẠT theo đúng đơn vị
đo của spec; ghi chú độ mịn để người sau không đọc "prefix9 bằng nhau" thành "bằng nhau từng byte".
Bước sau prefix9: đúng 1 bước/job mới (`test registry` · `packet-loop selftest`) ✓ A7 4 fixture + 2 phản chứng
trong 423 ✓. A2/A6/A1/A5: cần lượt chạy CI ⇒ not_run/KHÔNG ĐO ĐƯỢC theo chỉ thị — không đọc thành passed.

### H6 [LỚP 3] — răng của TỪNG mệnh đề chốt mới (mutation tự dựng, 14 mutant) — **LỖI (P2 F1 + P3 F2)**
Chi tiết phép đo ở Đ4; phân tích ở Finding. Đối chứng dương: 2 mutant tự dựng BỊ GIẾT chứng minh rig có răng.

---

## FINDING

### F1 — `ruff-fixture-thieu-rang-chot-moi`  [P2]  (GIỮ stable slug R11; sub-class MỚI: cua-khuon-khong-rang)
Bốn mệnh đề chốt MỚI của r15 gỡ NGUYÊN MỆNH ĐỀ mà suite vẫn 423/423 xanh
TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py` — (a) dòng 197 `if key and not tail and op != "\n": raise
ValueError("header thiếu lệnh")`; (b) dòng 198 `if key and tail and tail[0] in _KHUNG_SHELL: raise
ValueError("header lồng inline ngoài miền")`; (c) dòng 195-196 `elif key or argv[0] in _KHUNG_SHELL: raise
ValueError("cấu trúc shell ngoài miền")`; (d) dòng 181 `if stack and stack[-1][1] == "condition": raise
ValueError("compound trong condition ngoài miền")`.
VẤN ĐỀ + COUNTEREXAMPLE (đều ĐÃ CHẠY, Đ4): thay TỪNG mệnh đề bằng `if False:`/`elif False:` cho bốn mutant
KHÔNG TƯƠNG ĐƯƠNG mà CẢ BỐN sống trọn suite (rc=0 · 423/423 · TỔNG: ĐẠT):
· (a) `{ ; echo hi; }` và `{ && echo hi; }` — bash -n rc=2 — mutant cấp **KHONG** (HEAD: 2 lỗi KPT). Với
  header NHÓM `{`, mệnh đề này là chốt DUY NHẤT chịu tải (header `if` đã có phase/nonempty đỡ nên fixture
  `if-empty-cond` không phân biệt được — "ca có MẶT khác ca có ĐO").
· (b) `if true; then if false; fi` — bash -n rc=2 — mutant cấp KHONG. Fixture `syntax-if-inline-header`
  KHÔNG đo mệnh đề này: đầu vào của nó dưới mutant vẫn ĐỎ bằng guard phase khác (đo Đ4: 0 LỌT).
· (c) `do echo hi\n` — bash -n rc=2 — mutant cấp KHONG. KHÔNG một fixture nào cho 12 keyword còn lại của
  `_KHUNG_SHELL` (for/while/until/do/done/case/esac/function/select/coproc/time/!) lẫn keyword bị quote/escape
  — cửa chặn NGUYÊN một họ cấu trúc mà không có ca nào.
· (d) witness đa dòng compound-trong-condition — bash -n rc=0 (POSIX-VALID, đây là chiều CHẶN đã công bố
  trong docstring `_kiem_khuon_shell`) — mutant nhận: câu công bố "không nhận compound trong condition"
  thành lời khai không răng (nhẹ hơn a-c, cùng cửa).
3/4 mệnh đề mở chiều FAIL-OPEN dưới mutant (POSIX-invalid → chứng chỉ KHONG) — đúng hình dạng P2 của R11
("mệnh đề chốt đang sống, không tương đương, fixture không có răng" — chính slug này sinh ra ở R11 với hạng
P2; R14 chỉ hạ P3 cho biến thể THU-HẸP vì "gỡ-cả-luật CHẾT" — ở đây gỡ-cả-mệnh-đề SỐNG). Đây là mã MỚI của
chính packet, cùng lượt với khuôn FIXTURE/MUTANT-KHOÁ mà executor đã áp đúng cho 6 luật operator/redirect/
parameter — bốn cửa này bị bỏ ngoài khuôn ấy. Đối chứng phương pháp: `rv-unclosed-eof-off` và 2 widen-mutant
khác BỊ GIẾT ⇒ không phải rig hiền.
HƯỚNG SỬA CẤP LỚP (bằng lời, không patch): mỗi mệnh đề MỘT fixture âm mà CHỈ nó chặn — `{ ; echo hi; }`
(a) · `if true; then if false; fi` (b) · `do echo hi` + một keyword thứ hai khác họ, vd `while true; do echo
a; done` hoặc `esac` (c) · ca đa dòng if-trong-condition want=1 (d); cân nhắc thêm keyword-bị-quote (`"fi"`)
cho nhánh `argv[0] in _KHUNG_SHELL` của (c). Ước +5-7 fixture ≈ +7-10 dòng, 872→~880 ≤ 1000, vẫn 2 path.
TEST/MUTANT GIỮ CHỐT: bốn mutant `rv-*` trong `scratch/mutants/run_mutation*.py` làm phản chứng bắt buộc —
sau khi thêm fixture, chạy lại: cả bốn phải chuyển SỐNG → GIẾT (fixture mới LỌT, rc=1).
NGUY CƠ HỒI QUY: ≈0 — không đổi mã sản phẩm; HEAD đã ĐỎ sẵn mọi witness (đo Đ4 cột HEAD); fixture mới xanh
ngay trên HEAD.
ĐÃ THỬ VÁ: không — write set packet + authority sensitive (§8 cấm patch-as-hint); mutant nằm trong scratch.
ĐỘ TIN: cao — mọi mệnh đề đều có A/B HEAD↔mutant + bash -n đối chứng.

### F2 — `ruff-fixture-thieu-rang-chot-moi`  [P3]  (cùng slug; sub-class MỚI: bien-bang-chu-cai-redirect-va-op)
Bảng chữ cái reject của redirect và biên op-list chỉ có răng ở 2/7 phần tử — 6 mutant thu-hẹp/nới-biên sống
TỆP/DÒNG: dòng 277 `run[target] in "\n;|&<>#"` (reject-set đích redirect) · dòng 214 tuple toán tử cho phép.
VẤN ĐỀ + COUNTEREXAMPLE (ĐÃ CHẠY, Đ4): bỏ TỪNG ký tự `\n`/`|`/`&`/`<>` khỏi reject-set (4 mutant) + bản gộp
`";#"` + nới op-tuple bằng `"|||"` ⇒ **6 mutant sống 423/423**, mỗi cái KHÔNG tương đương (witness
`echo hi >\nwc` · `> | wc` · `> & echo ok` · `> > f` · `||| echo ok` — bash -n rc=2 TẤT CẢ; HEAD từ chối đúng).
Chỉ `;` (fixture redirect-list) và `#` (redirect-comment) + EOF (len-check, redirect-eof) có răng.
**Aggravation:** `a > | b` và `|||` là hai phần tử BIÊN được R14-addendum nêu ĐÍCH DANH trong mục
FIXTURE/MUTANT KHOÁ ("fixture phải lấy cả phần tử BIÊN của mỗi luật… ví dụ `|||` cho op-list, `a > | b` cho
redirect-đích") — phần dặn này CHƯA THI CÔNG ⇒ phần "phần tử BIÊN" của lock R14: **VÁ HỜ** (lõi 6 ca + 6 mutant
luật + widen-`;;` thì ĐÃ VÁ THẬT — Đ2/Đ3).
VÌ SAO P3 (không phải P2): đúng phép phân hạng R14 — gỡ-CẢ-luật CHẾT (syntax-redirect-target 7 LỌT ·
syntax-operator-alphabet 8 LỌT, đo Đ3), sản phẩm từ chối đúng TOÀN bảng chữ cái trên HEAD (bash-n sweep +
witness); lỗ chỉ ở độ mịn lưới cho hồi quy tương lai.
HƯỚNG SỬA CẤP LỚP: 5 fixture âm — `echo hi >\nwc` · `echo hi > | wc` · `echo hi > & echo ok` · `echo hi > > f`
· `echo hi ||| echo ok` (+5 dòng, dư trần). TEST/MUTANT GIỮ CHỐT: 6 mutant `rv-redirect-*`/`rv2-op-widen-3pipe`
phải chuyển SỐNG → GIẾT. NGUY CƠ HỒI QUY: ≈0 (HEAD đỏ sẵn cả 5 đầu vào). ĐỘ TIN: cao.

### F3 — `ruff-docstring-parameter-rong-hon-hanh-vi`  [P3]  (Spec axis lớp 2 — câu công bố MỚI r15)
TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py:482-483` — "Parameter chỉ nhận ${TEN} hoặc ${TEN:-literal}…;
các expansion khác ngoài miền."
VẤN ĐỀ + COUNTEREXAMPLE (ĐÃ CHẠY, H1): 12 dạng bare-`$` (`$X` `"$X"` `$@` `$1` `$*` `$?` `$$` `$!` `$-`…)
đều LÀ parameter expansion theo POSIX XCU 2.5.2/2.6.2 và đều được NHẬN (KHONG trên carrier opaque, cờ bad
chỉ đánh related — `pip install $X` vẫn KPT ✓), trong khi `${X:?bad}` bị TỪ CHỐI — hai thành viên cùng phạm
trù "expansion khác", một nhận một chối, câu công bố nói CHỐI CẢ. Lời khai hợp đồng RỘNG HƠN phép đo — đúng
lớp lỗi kho này truy, trên đúng bề mặt (docstring = miền công bố, per chỉ thị "Miền cụ thể ở loi_ruff_ci/
_dong_logic/_kiem_khuon_shell").
VÌ SAO KHÔNG SỬA MÃ: `ci.yml` THẬT dùng `$VAR`/`$$`/`$(...)` dày đặc (`test -n "$PR_HEAD_SHA"` · `echo $$ >
"$RIENG/cgroup.procs"` · `MOUNT="$(awk …)"`) — siết theo câu là tự làm đỏ workflow thật (RUFF CI 3/3 hiện
hành). Chứng chỉ hiện KHÔNG sai (input POSIX-valid, unrelated thật) ⇒ lỗi nằm ở CÂU.
HƯỚNG SỬA: MỘT câu docstring — giới hạn mệnh đề "các expansion khác ngoài miền" vào dạng `${…}`, và nói thẳng
bare-`$`/special-param là DỮ LIỆU ĐỘNG mang cờ (opaque giữ KHONG, related thành KPT). Kèm 1-2 fixture dương
(`echo "$X"` want 0 · `pip install $X` đã có `requirement-dong`) để câu mới có neo.
NGUY CƠ HỒI QUY: 0 (chỉ chữ + fixture dương xanh sẵn). ĐỘ TIN: cao.

---

## ĐỐI CHIẾU R14 (original + addendum — verdict hiệu lực changes_requested) — trạng thái TỪNG finding
| finding R14 | trạng thái | bằng chứng TỰ ĐO |
|---|---|---|
| P2 `ruff-khuon-chua-chung-minh-provisioning`/opaque-structural-grammar | **ĐÃ VÁ THẬT** (lõi) | Đ2: 6 ca + thành viên sót `echo "${x"` + 2 biên đều ĐỎ với trace TỪNG LUẬT; Đ3: 6 mutant luật (op-alphabet/missing-lhs/missing-rhs/redirect-target/parameter/parameter-double) + widen-`;;` đều BỊ GIẾT, tập LỌT khớp từng tên | 
| — phần dặn "phần tử BIÊN của mỗi luật" trong FIXTURE/MUTANT KHOÁ của addendum | **VÁ HỜ** | Đ4: `a > | b` và `|||` (nêu ĐÍCH DANH) không có fixture — 2 mutant tương ứng SỐNG ⇒ F2 [P3] |
| P3 `ruff-fixture-thieu-rang-chot-moi`/bien-nguong-C0 | **ĐÃ VÁ THẬT** | Đ2-V2: tuple 30 ký tự (giữ ID c0-0..3); Đ3: `c0-threshold-plain/escape` BỊ GIẾT, 18 fixture LỌT mỗi cái |
| (mới lượt này) cùng slug, sub-class cua-khuon-khong-rang | **F1 [P2]** | Đ4: 4 mệnh đề chốt mới gỡ nguyên mệnh đề vẫn 423/423 xanh; 3/4 fail-open (bash -n rc=2) |

## BẢNG ĐO — lời khai executor ↔ đo được
| khẳng định executor | đo được (reviewer, độc lập) | khớp? |
|---|---|---|
| exact head/tree/base | e5e8e23…/2046f92…/bb7013c… — rev-parse đầu VÀ cuối lượt, porcelain 0 cả hai lần | Có |
| A8 872/1000, đúng 2 path | numstat 746+126=872, đúng 2 path | Có |
| workflow byte-identical 3bbc6b4 | blob `cb025a5a70…` ở CẢ HAI commit | Có |
| registry 423/423 + 21/21 + 4/4 + 3/3, rc=0 | tự chạy KHÔNG `--chay`: y hệt; diff freeze/sandbox: IDENTICAL | Có |
| Ruff F rc=0 · actionlint rc=0 | tự chạy: All checks passed · 0 chẩn đoán | Có |
| 33/33 mutants semantic+fixture-LỌT+rc1 | tái lập TRỌN 33 mutant trên clone: 33/33, tập LỌT khớp | Có |
| syntax-probe 403/21/0 "không phải proof đầy đủ" | sweep RIÊNG (generator khuôn): 503/146/**0** — nhất quán; lời khai giới-hạn TRUNG THỰC | Có |
| spec_hash lease r23 | sha256(SPEC-r23.md) khớp đủ 64 ký tự | Có |
| PROMPT.md ↔ launcher expected-prompt-sha256 | 81305f28… khớp | Có |
| Răng theo TỪNG cửa MỚI (khuôn shell) | **KHÔNG khớp trọn** — 4 mệnh đề `_kiem_khuon_shell`/emit không mutant nào trong 33 phủ, gỡ vẫn xanh (F1) · 5+1 phần tử biên redirect/op không răng (F2) | **KHÔNG — F1/F2** |
| A1/A5/A2/A6/CI | not_run theo chỉ thị — reviewer không mạng/CI ⇒ KHÔNG ĐO ĐƯỢC, không đọc thành passed | Đúng trạng thái |
| metadata_head/refset_sha256 (frozen-r15) | ngoài khả năng đo offline (cấm mạng) — KHÔNG ĐO ĐƯỢC | Đúng phạm vi |
| master c16bd329 ≠ base | tích hợp với master mới: not_measured, KHÔNG dùng ngoại lệ merge §5.1 | Đúng trạng thái |

## KẾT LUẬN THEO LỚP (trục Spec + Standards/Security cho từng lớp)
| lớp | verdict | căn cứ |
|---|---|---|
| 1. Installer/domain | **approve** | H3 (12 wrapper/installer-lạ với pin TĨNH: 0 đường đúc GHIM xuyên wrapper; GHIM chỉ cấp cho dạng POSIX-tương-đương thật) · H4 (job phụ cài tĩnh chịu đủ pin/probe/sai-pin) · partition invocation/opaque/ngoài-miền kín trên mọi probe; Spec: khớp Miền công khai; Security: fail-close đủ |
| 2. Lexer/structure/composition/order/shell | **approve** (hành vi; kèm F3 [P3] trục Spec — câu docstring, không hành vi) | Đ2: 9 ca P2 cũ ĐỎ đúng trace; H2: 146 accepted / 0 POSIX-invalid (generator khuôn mới); H6-mini accept-side khớp POSIX; HEAD từ chối đúng TOÀN BỘ witness của Đ4; F3 chỉ là câu công bố rộng hơn hành vi — một dòng docstring |
| 3. Consumer/spec/workflow/fixtures | **changes_requested** | tiêu chí lớp này ("mutable guards THỰC SỰ bị fixture giết") đo ra F1 [P2]: 4 mệnh đề chốt mới gỡ nguyên mệnh đề mà 423/423 vẫn xanh, 3/4 fail-open dưới mutant + F2 [P3]: 6 mutant biên sống, gồm 2 phần tử addendum nêu đích danh; phần còn lại của lớp SẠCH: A7 4 fixture + 2 phản chứng giữ màu, A8 872/2path, byte-identity, A3/A4 đo trực tiếp (H5), 33/33 mutant executor tái lập |

Approve tổng đòi CẢ BA lớp approve ⇒ **changes_requested** (không hạ assurance, không đổi provider).

## KẾT LUẬN CUỐI (hai dòng đầu tệp là canonical và ĐÃ CHỐT — không còn là placeholder)
- verdict: **changes_requested** · reviewed_sha `e5e8e2390db1c4a68ad0ee6febdf7d6ed0a39582`
  (tree `2046f927fe8375c0bd98f2dc2d6a23fab1c14da9`).
- Findings: **P1=0 · P2=1 · P3=2** — F1 `ruff-fixture-thieu-rang-chot-moi`/cua-khuon-khong-rang [P2] ·
  F2 cùng slug/bien-bang-chu-cai-redirect-va-op [P3] · F3 `ruff-docstring-parameter-rong-hon-hanh-vi` [P3].
  KHÔNG finding hành vi nào trên HEAD: mọi witness đều bị HEAD từ chối đúng — cả ba finding là lưới
  fixture/câu công bố; hướng đóng ≈ +10-12 fixture + 1 câu docstring, ước 872→<900 ≤ 1000, giữ đúng 2 path.
- R14: P2 opaque-structural-grammar **ĐÃ VÁ THẬT** (lõi) · P3 bien-nguong-C0 **ĐÃ VÁ THẬT** · phần dặn
  "phần tử BIÊN" của addendum **VÁ HỜ** (thành F2). Không phát hiện VÁ SINH LỖI MỚI.
- Bảng săn: 6 hướng mới (2/2/2 theo lớp), 14 mutant tự dựng (2 bị giết làm đối chứng rig, 9+1 sống
  không-tương-đương), sweep 503/146/0, 12 probe bare-`$`, 12 probe wrapper, A3/A4 đo trực tiếp.
- A1/A5/CI/A2-conclusions/A6-readback/A9-live: **not_run/KHÔNG ĐO ĐƯỢC** theo chỉ thị chủ kho — verdict này
  KHÔNG thay các phép đo ấy, KHÔNG mang quyền merge/land. Nếu lượt sau approve thì cross_approved CHỈ cho
  code review trên exact SHA. Verdict vận chuyển nguyên văn lên Issue #463, không phải GitHub native approval.
- Identity: provider **anthropic_claude** · model **claude-fable-5** · effort **max** · execution_surface
  **claude_code** · transport **machine/local** — validator so `modelUsage` thô sau run.
- Bất biến cuối lượt (ĐO SAU khi viết xong thân): clone HEAD `e5e8e2390db1c4a68ad0ee6febdf7d6ed0a39582` ·
  tree `2046f927fe8375c0bd98f2dc2d6a23fab1c14da9` · porcelain **0 dòng** — KHỚP, không đổi; trạng thái sạch
  chỉ đo tại thời điểm đọc, không tự chứng minh lịch sử cả lượt. Mọi hiện vật reviewer nằm ở `VERDICT.md` +
  `scratch/` (v1_r14_p2_6ca.py · hunt_h1_h6.py · suite-head.txt · mutants/run_mutation{,2}.py ·
  mutants/mutation-rv.{json,out} · 35 bản mutant tên riêng) — NGOÀI clone.

