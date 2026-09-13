verdict: approve
reviewed_sha: 664aaf326f5b084cf51a5005c48a7dbb72699bd8

# VERDICT — packet #463 lượt 13 (reviewer Claude độc lập, class=sensitive)

- tree kỳ vọng: 4fbf9f5b8385c946e39431bb3982d0b40c97f405
- base: bb7013c7669da19304a8769e5b25f8c1f8951e9c
- P1: 0 · P2: 0 · P3: 1 (CUỐI CÙNG — `ruff-ham-chet-khong-caller`, lớp 3, không chặn)
- Trạng thái: HOÀN TẤT. Verdict cuối: **approve** — lớp 1 approve · lớp 2 approve · lớp 3 approve.
  (Dòng placeholder ban đầu ghi changes_requested/0-0-0 theo đúng quy trình; nhật ký dưới giữ nguyên, không xoá.)

## Nhật ký phép đo (append-only)

### Neo (không tính N)
- `git rev-parse HEAD` = `664aaf326f5b084cf51a5005c48a7dbb72699bd8` — KHỚP reviewed_sha.
- `git rev-parse HEAD^{tree}` = `4fbf9f5b8385c946e39431bb3982d0b40c97f405` — KHỚP tree kỳ vọng.
- `git status --porcelain` rỗng lúc mở lượt.
- Đã đọc: prompt.snapshot, SPEC-r23.md (trọn), LEASE-r23.yaml, g4-resume-authority-response.json, frozen-r13.json, diff.patch (trọn 959 dòng), PRIOR_HUNT_INDEX.md, prior-review-11.md (3 finding + giới hạn).

### Phép đo nền (không tính N)
- `git diff --numstat bb7013c7..664aaf3` ⇒ `621+92` (test) · `126+6` (ci.yml) ⇒ **747 additions, đúng 2 path** — khớp A8 ≤ 1000, khớp lời khai 747.
- `git rev-parse 3bbc6b4:.github/workflows/ci.yml` = `HEAD:.github/workflows/ci.yml` = `cb025a5a70…` ⇒ **ci.yml BYTE-IDENTICAL với 3bbc6b4** — các phép đo workflow-layer của R10/R11 (A3 bộ ba job, prefix9, on/concurrency, A4 timeout, actionlint-delta) chuyển giao nguyên vẹn cho blob này.
- Registry test (KHÔNG `--chay`), `C:/Python313/python.exe -X utf8 -B` trong clone: **rc=0, ĐĂNG KÝ 21/21 · LAUNCHER 4/4 · RUFF CI 3/3 · PHẢN CHỨNG 214/214 · TỔNG: ĐẠT**. Output của tôi ≡ `sandbox-registry.txt` (diff chỉ lệch dòng header `rc=0` của log executor) và `baseline-registry.txt ≡ sandbox-registry.txt` — lời khai 214/214 ĐƯỢC XÁC NHẬN ĐỘC LẬP.
- `ruff check --select F` (ruff 0.15.15): rc=0. `actionlint` 1.7.7: rc=0 trên ci.yml. Khớp `r12-freeze-*`.
- Sau các phép đo nền: `git status` clone vẫn rỗng.
- Ghi chú đọc mã (sẽ phân hạng ở cuối): `_cham_ruff` (dòng 262), `_loai_mot_dong` (383), `_probe_sau_ghim` (391), `_la_registry` (395) mỗi tên xuất hiện ĐÚNG 1 lần toàn kho (rg) — hàm chết, không caller; `_phan_loai_cai_ruff` còn 1 caller thật (dòng 914, bảng `nhan-*`). Ruff F không bắt hàm chết mức module.
- `mutation-r12.json`: 12 mutant, tất cả khai killed, có danh sách fixture LỌT từng mutant — KHÔNG kèm diff mutant ⇒ phải tự dựng mutant tương đương để kiểm độc lập.

### XÁC MINH VÁ R11 (không tính N) — phần 1: hành vi trên HEAD
Lệnh: `probe_r11fix.py` (import module từ clone, read-only). Output nguyên văn (rút gọn):
- `V1a` — phản ví dụ R11 NGUYÊN VĂN (`shell: python` + thân `x=__import__('os')...`): **2 lỗi**, kèm `ngoài miền cú pháp: ['gate/bước 2']` ⇒ **ĐÃ VÁ** (lượt 11: 0 lỗi XANH).
- `V1b` thân RỖNG · `V1c` thân opaque (`python setup.py`) dưới `shell: python`: **đều 2 lỗi** ⇒ chốt shell chạy TRƯỚC phân tích thân, bất kể hình dạng thân — đúng yêu cầu «kể cả thân nhìn như assignment/opaque/rỗng».
- `V1d` đối chứng `shell: bash` + `x=1`: **0 lỗi** — không chặn oan.
- `V1e` `defaults.run.shell: python` mức WORKFLOW: **3/3 lỗi** ⇒ nhánh workflow-defaults nay có hiệu lực hành vi.
- `V1f`/`V1g` thông điệp KPT: `ngoài miền cú pháp: ['gate/bước 2']` — vị trí job/bước + phân loại nguyên nhân, không dump argv ⇒ P3 lượt 11 đã xử lý (ghi chú: trace chi tiết như «shell ngoài miền» vs «heredoc chưa đóng» vẫn không in ra — chấp nhận được, xem Nhận xét cuối).

### XÁC MINH VÁ R11 — phần 2: mutant ĐỘC LẬP (tự dựng, không dùng diff executor; không tính N)
Lệnh: `mutant_runner.py` — 5 mutant trên BẢN SAO trong `scratch/mutants/` (mỗi mutant một tên tệp riêng, ROOT ghim về clone, `-X utf8 -B`), chạy TRỌN suite:
| mutant tự dựng | rc | tally | fixture LỌT | khớp mutation-r12.json? |
|---|---|---|---|---|
| mA gỡ mệnh đề −1-poison (dòng 466) | 1 | 211/214 | `registry-ngoai-hop-dong-job-phu-{0,1,2}` | khớp `registry-poison` từng tên |
| mB gỡ scope workflow-defaults (dòng 406) | 1 | 211/214 | `workflow-shell-{ngoai-mien,null}`, `workflow-run-sai-kieu` | khớp `workflow-shell-default` từng tên |
| mC gỡ chốt shell-trước-thân (dòng 418) | 1 | 187/214 | 27 fixture (đúng bộ shell-*) | khớp `shell-before-body` từng tên + tally |
| mD gỡ `reason` vị trí (dòng 472) | 1 | 212/214 | `nguyen-nhan-{lexer,shell}` | khớp `outside-diagnostic` |
| mE bỏ điều kiện `pinned` của probe nội-run (dòng 372) | 1 | 212/214 | `probe-truoc-cai`, `probe-chi-buoc-truoc` | khớp `probe-order` |
⇒ **Hai mutant SỐNG ở R11 (m1 poison, m2 workflow-defaults) nay CHẾT có răng riêng**; chốt shell mới và thông điệp cũng có răng. 5/12 dòng của mutation-r12.json được tái lập độc lập, khớp từng tên fixture và từng tally — 7 dòng còn lại nhận ở mức lời khai có cấu trúc nhất quán (không phát hiện mâu thuẫn).
⇒ KẾT LUẬN XÁC MINH VÁ R11: **cả ba finding R11 ĐÃ VÁ THẬT** (P2-1 hành vi + fixture; P2-2 hai răng mới; P3 thông điệp).

## BẢNG SĂN — 8 hướng MỚI độc lập (N=8; lớp 1: H1-H2 · lớp 2: H3-H5 · lớp 3: H6-H8)
Đối chiếu PRIOR_HUNT_INDEX (lượt 7..11): các hướng dưới đây chọn NHÁNH NGỮ NGHĨA chưa đo — không trùng
với pip-grammar đã đo (fixture `nhan-*` 39 ca), opaque-family đã đo (executable-path/exe, installer-la,
trinh-dong, prefix-env/assignment/command/sudo), POSIX-carrier đã đo (shell fixtures), malformed đã đo
(quote-chua-dong, and-thieu-trai/phai cùng-dòng, backtick, heredoc), probe-order đã đo (4 fixture),
consumer-mutant đã đo (mutation-r22/r12), hay workflow-constraint đã đo (A3/A4/prefix9/on/concurrency).

### H1 [LỚP 1] — pip requirement/option grammar: 15 biên chưa đo
GIẢ THUYẾT: còn dạng đối số install được cấp `KHONG`/`GHIM` trong khi ngữ nghĩa pip khác lời chứng.
LỆNH: `hunt_L1.py` phần H1 (gọi `_doc_run_ruff` trên sản phẩm HEAD, import từ clone).
OUTPUT (nguyên văn, rút cột): `ruff == 0.15.15`→KPT · lặp ruff 2 lần→KPT · `ruff[]==…`→KPT ·
`ruff===0.15.15`→KHONG_GHIM · `.post1`/`+cpu`→KHONG_GHIM · `--`→KPT · `install` trơ/chỉ-flag→KPT ·
`pip` trần→KPT · `pip download`→KPT · ruff+gói khác→KPT · `ruff.==…`→KHONG_GHIM · marker sau `;` trong
nháy→KHONG_GHIM · `ruff-lsp`→KHONG.
KẾT LUẬN: **KHÔNG PHẢI LỖI** — mọi biên fail-close hoặc từ-chối-an-toàn (KHONG_GHIM ⇒ đỏ qua bad_pin);
`===0.15.15` bị chặn oan (pip hiểu là pin đúng bản) — chiều an toàn, chấp nhận. Giới hạn khai thẳng:
`pip install ruff-lsp` (KHONG) có thể KÉO ruff bản khác theo dependency — provenance runtime, chủ kho đã
loại khỏi phạm vi M7, KHÔNG tính lỗi.

### H2 [LỚP 1] — họ wrapper/prefix quanh installer: 15 biến thể chưa đo
GIẢ THUYẾT: một wrapper (time/exec/builtin/nohup/sudo -u/command -p/`\pip`/`py`/`python -m pip._internal`…)
có thể làm installer thoát nhận dạng thành `KHONG`.
LỆNH: `hunt_L1.py` phần H2. OUTPUT: 14/15 → **KPT** (fail-close); riêng `\pip install ruff==0.15.15` → **GHIM**.
KẾT LUẬN: **KHÔNG PHẢI LỖI** — `\pip` là đúng ngữ nghĩa POSIX (quote-removal: `\p`→`p`, chạy chính `pip`),
chấp nhận GHIM là ĐÚNG chứ không phải lọt; mọi wrapper còn lại đổ về KPT nhờ luật «ngoài whitelist không
được suy KHONG», kể cả `python -m pip._internal` (module chỉ khớp literal `pip`).

### H3 [LỚP 2] — whitespace shlex ⊃ POSIX-IFS: `\r` `\f` `\v` trong thân lệnh
GIẢ THUYẾT: `shlex.split` tách từ tại `\r` còn bash thì KHÔNG ⇒ có chuỗi được cấp GHIM/probe mà bash chạy
ra hành vi khác (lớp «misparse trong miền» — họ hàng đúng với P2-1 lượt 11 nhưng ở tầng TOKEN, chưa ai đo).
LỆNH: `hunt_L2.py` phần H3. OUTPUT: `pip\rinstall …`→**GHIM** · `…==0.15.15\rX`→KPT · CR cuối dòng→GHIM ·
`ruff\r--version`→KHONG · `\f`/`\v` trong requirement→KHONG_GHIM · CRLF tách lệnh→GHIM+probe.
KẾT LUẬN: **KHÔNG PHẢI LỖI SẢN PHẨM** — divergence CÓ THẬT nhưng mọi ca lệch chiều NHẬN đều tương ứng một
runtime CHẾT ỒN ÀO: bash coi `pip\rinstall` là MỘT từ ⇒ command-not-found ⇒ mọi shell trong miền chạy `-e`
⇒ bước ĐỎ ⇒ gate không thể XANH bằng bước ấy — bất biến «gate xanh ⇒ đã ghim» đứng vững (thoả rỗng). Thêm
hai lớp chặn thực tế: YAML parser chuẩn hoá `\r\n`→`\n` trong block scalar, và kho có cổng EOL (§9). Ghi
nhận là GIỚI HẠN TÀI LIỆU HOÁ: «quoting POSIX hợp lệ» của docstring rộng hơn shlex một bậc tại `\r` —
không đòi vá; nếu muốn khoá hẳn: từ chối token chứa ký tự điều khiển C0 trong `_dong_logic` (≤3 dòng).

### H4 [LỚP 2] — biên toán tử/nối dòng: `&&`-vắt-dòng, `;;`, subshell, redirect, `\$(`, `#` trong `$()`
GIẢ THUYẾT: các tổ hợp toán tử chưa đo có nhánh nhận sai hoặc ném lọt.
LỆNH: `hunt_L2.py` phần H4. OUTPUT: `pin && #cmt\nprobe`→GHIM+probe ✓ (khớp bash: sau `&&` được xuống
dòng) · `pin &&\nprobe`→GHIM+probe ✓ · `pin &&\n<EOF>`→KPT+registry=-1 ✓ («thiếu vế phải» bắt cả biến
thể ĐA DÒNG — trước chỉ đo cùng-dòng) · `;;`→KPT · subshell/redirect/`&>`→KPT · `echo \$(pip…)`→KHONG
(bash: lỗi cú pháp `(` ⇒ bước chết ồn) · `V=$(echo hi # )`→KHONG (bash: `#` nuốt `)` ⇒ lỗi cú pháp ồn).
KẾT LUẬN: **KHÔNG PHẢI LỖI** — hai ca cuối lệch parser-vs-bash nhưng chiều lệch là «nhận thứ bash sẽ chết
ồn» ⇒ thoả rỗng như H3; phần còn lại fail-close/nhận-đúng.

### H5 [LỚP 2] — kiểu dữ liệu lạ tại 3 scope shell (mở rộng bộ null đã đo sang list/str/bool/int/case)
GIẢ THUYẾT: một kiểu không-chuỗi ở scope nào đó làm `_shell_trong_mien` ném hoặc tha nhầm.
LỆNH: `hunt_L2.py` phần H5. OUTPUT: job-defaults là list → 3 lỗi · defaults.run là str → 3 lỗi ·
shell=True/1/"BASH" → 3 lỗi · workflow `defaults.run: {}` → **0 lỗi** (đúng: không khai shell) ·
step khai `bash` nhưng job-defaults là list → 3 lỗi (chặn oan có chủ đích — YAML đó GitHub cũng từ chối).
KẾT LUẬN: **KHÔNG PHẢI LỖI** — không ngoại lệ nào thoát ra ngoài, mọi kiểu lạ fail-close, không tha nhầm.

### H6 [LỚP 3] — liên từ registry: hai bước registry cùng job, tổ hợp `if` từng bước
GIẢ THUYẾT: `registry[jn].index(1)` neo bước ĐẦU ⇒ có tổ hợp hai-bước làm chốt tha/chặn sai.
LỆNH: `hunt_L3.py` phần H6. OUTPUT: 2 bước registry không điều kiện → 0 lỗi (pin đứng trước CẢ HAI —
đúng hợp đồng M7, vẫn MỘT job registry) · bước-1 có `if`/bước-2 không → 1 lỗi (chặn oan — neo bước đầu;
chiều an toàn) · bước-2 có `if` → 0 lỗi (pin trước cả hai ✓) · 0 install + 0 registry → 3/3 lỗi ·
lệnh lạ trong job registry → đỏ qua check-1 (job vào `installs` vì có KPT) dù registry-flag=0.
KẾT LUẬN: **KHÔNG PHẢI LỖI** — không tổ hợp nào tha nhầm; một ca chặn oan fail-close, ghi nhận.

### H7 [LỚP 3] — parity job-level NGOÀI bộ ba A3: strategy.fail-fast · env · defaults · permissions · needs · container · services · concurrency · outputs · environment
GIẢ THUYẾT: A3(1) chỉ so (if, matrix.os, timeout) ⇒ job mới có thể lệch gate ở khoá NGOÀI bộ ba (fail-fast
đổi hành vi huỷ ma trận; env thiếu biến mà bước dời cần) mà mọi phép đo trước vẫn xanh.
LỆNH: `hunt_L3.py` phần H7 (yaml.safe_load ci.yml tại HEAD, so 10 khoá × 2 job mới với `gate`).
OUTPUT: **20/20 BẰNG** — cả `strategy` (kể `fail-fast: false`) lẫn `env` (đủ 3 biến PYTHONIOENCODING/
PYTHONUTF8/PYTHONDONTWRITEBYTECODE) và 8 khoá còn lại đều `None==None` hoặc bằng sâu.
KẾT LUẬN: **KHÔNG PHẢI LỖI** — điểm mù của bộ ba A3 RỖNG trên blob này; hai bước dời không mất biến env nào.

### H8 [LỚP 3] — răng của chốt trùng-tên trong harness `_them`
GIẢ THUYẾT: chốt `any(t == ten for t, _ in KQ)` có thể không đủ răng (F02-họ: bảng tên câm lặng nuốt ca).
LỆNH: `hunt_L3b.py` — mutant mF đổi tên fixture `probe-buoc-sau`→`probe-hai-phia` (tạo trùng tên).
OUTPUT: `rc=1`, `AssertionError: trung ten ca phan chung: ruff-ci-probe-hai-phia`, KHÔNG in `TỔNG`.
Kèm phép đếm trên baseline: 214 tên phân biệt / 214 dòng, 0 trùng (uniq -d rỗng), 214 «ĐỎ đúng»,
đủ 4 fixture đặc tả A7 (`chua-tach…`, `da-tach-dung`, `da-tach-thieu-ruff`, `da-tach-ruff-sau-registry`).
KẾT LUẬN: **KHÔNG PHẢI LỖI** — harness chết ỒN khi tên trùng, không im lặng; lớp F02 đóng theo cấu trúc.

## BẢNG ĐO — mọi con số đã đo, kể cả cái khớp
| khẳng định | khai / hợp đồng | đo được | khớp? |
|---|---|---|---|
| Exact head | 664aaf326f5b084cf51a5005c48a7dbb72699bd8 | rev-parse đầu VÀ cuối lượt khớp; porcelain rỗng cả hai lần | Có |
| Tree | 4fbf9f5b8385c946e39431bb3982d0b40c97f405 | khớp | Có |
| Base | bb7013c7669da19304a8769e5b25f8c1f8951e9c | dùng đúng cho numstat | Có |
| A8 additions / path | 747 ≤ 1000, đúng 2 path | 621+126=747, 2 path | Có |
| ci.yml giữ byte so 3bbc6b4 | tuyên bố nhiệm vụ | blob `cb025a5a70…` ở CẢ HAI commit | Có |
| Registry (KHÔNG --chay) | 214/214, rc=0 | tự chạy: 21/21 · 4/4 · 3/3 · **214/214** · TỔNG ĐẠT · rc=0; ≡ sandbox ≡ baseline | Có |
| Ruff F | rc=0 | All checks passed, ruff 0.15.15 | Có |
| actionlint ci.yml | rc=0 | rc=0, actionlint **1.7.7** (đúng AL_VER ci.yml ghim) | Có |
| spec_hash lease r23 | 7089ad0d7c4322ff… | SPEC-r23.md chuẩn hoá LF ⇒ **7089ad0d7c4322ff…** (bản sandbox bị CRLF-hoá 726 dòng — tạo tác chép Windows, không phải lệch nội dung) | Có |
| Spec trong cây HEAD | — | `49844d77…` (bản r21-era; write_set không chứa spec nên bản trong nhánh đứng yên — ĐÚNG thiết kế, authority là bản neo lease) | Ghi nhận |
| 12 mutant mutation-r12.json | 12/12 killed | tự dựng 5 mutant ĐỘC LẬP (mA..mE) nhắm 5 chốt tương ứng: 5/5 chết, tập fixture LỌT + tally khớp TỪNG TÊN với 5 dòng tương ứng (`registry-poison`, `workflow-shell-default`, `shell-before-body`, `outside-diagnostic`, `probe-order`) | Có (mẫu 5/12; 7 dòng còn lại: lời khai nhất quán, chưa tái lập riêng) |
| Răng chốt trùng-tên harness | — | mutant mF: rc=1, AssertionError đúng tên, không TỔNG | Có |
| 214 tên fixture | phân biệt | 214 distinct, 0 dup, 4 fixture A7 đủ mặt | Có |
| A3 blind-spot (fail-fast/env/8 khoá) | không lệch | 20/20 BẰNG giữa gate và 2 job mới | Có |
| A1 / A5 / A2-conclusion / A6-readback / CI | not_run theo chủ kho | không chạy CI, không dispatch, không mạng — **KHÔNG ĐO ĐƯỢC, không đọc thành passed** | Đúng trạng thái |
| A9 (lease không chồng) | lease khai đã đo lúc cấp (371 heads, holders 0) | offline không mạng ⇒ không tái đo được ref-set remote — nhận ở mức hiện vật lease | KHÔNG ĐO ĐƯỢC (đúng phạm vi) |
| Cây review nguyên trạng | không sửa/commit | mọi đột biến ở `scratch/mutants/*`, ROOT ghim về clone; status rỗng + HEAD/tree không đổi đo lại cuối lượt (bảng dưới) | Có |

## Hai trục bổ sung
- **Spec (M1–M7, A7, A8):** M1 hai bước nặng sang 2 job riêng cùng ma trận ✓ (diff + parse). M3/M4 bộ ba
  (if=None, matrix.os cùng chuỗi, timeout=60×3) kế thừa từ R11 trên blob BYTE-IDENTICAL + H7 mở rộng 10 khoá ✓.
  M7 consumer đọc MỌI job, đòi pin CÙNG job TRƯỚC registry, không job nào có bước ⇒ lỗi ✓ (fixture
  `khong-job-nao-chay-registry`, `da-tach-*`, real ci.yml 3/3). A7 bốn fixture đúng màu trong 214 ✓. A8 747/1000,
  2 path ✓. M2/M5/M6 cần CI/ruleset ⇒ not_run theo chỉ thị — KHÔNG suy thành đạt. Phạm vi M7 đúng chốt chủ kho:
  chỉ lệnh khai trực tiếp trong YAML; script/`python -c` opaque — fixture đối chứng dương giữ đúng ranh ấy ✓.
- **Standards/Security:** không thực thi nội dung fixture nào (chỉ parser offline) ✓; `yaml.safe_load` ✓;
  không đường ghi mới, không network trong sản phẩm ✓; thông điệp lỗi không dump argv (mD có răng) ✓;
  comment tiếng Việt đúng idiom kho, một dòng khai phạm vi/quyết định chủ kho tại chỗ ✓. MỘT tì vết standards:
  4 hàm chết (finding P3 dưới). Console cp1258: tệp tự reconfigure UTF-8 ✓ (chạy thật không UnicodeEncodeError).

## Kết luận theo LỚP
| lớp | verdict | căn cứ |
|---|---|---|
| 1. Installer/domain | **approve** | R11 đã approve; H1/H2 (30 biên mới): fail-close toàn bộ, `\pip` nhận đúng ngữ nghĩa; không đường nào biến ngoài-miền thành KHONG |
| 2. Lexer/composition/order/shell | **approve** | P2-1 lượt 11 vá thật + răng (V1a-e, mC 27 fixture); H3/H4/H5: mọi divergence còn lại chiều thoả-rỗng (runtime chết ồn dưới `-e`) hoặc fail-close; không phản ví dụ lớp nào còn dựng được |
| 3. Consumer/spec/workflow/fixtures | **approve** | P2-2 vá thật (mA/mB chết); P3 thông điệp vá (mD chết); ba chốt pin/probe/registry + đúng-một-registry-job đo qua H6; A8/byte-identity/A3-blindspot/harness (H7/H8) sạch; 1 finding P3 mới KHÔNG chặn (không đổi hành vi cổng) |

## ĐỐI CHIẾU LƯỢT TRƯỚC — chấm cuối
- `ruff-khuon-chua-chung-minh-provisioning` [P2 lượt 11]: **ĐÃ VÁ THẬT** — chốt shell chạy TRƯỚC phân tích
  mọi thân (V1a/b/c), đối chứng không chặn oan (V1d), mutant gỡ chốt chết 27 fixture (mC). H1-H5 không tìm
  được sub-class mới cùng lớp ⇒ slug ĐÓNG ở lượt này, không reset lịch sử.
- `ruff-fixture-thieu-rang-chot-moi` [P2 lượt 11]: **ĐÃ VÁ THẬT** — hai mutant sống (poison −1, workflow-defaults)
  nay chết bằng fixture riêng, tái lập độc lập (mA: 3 LỌT · mB: 3 LỌT, main rc=1 cả hai).
- `ruff-kpt-thong-diep-khong-neu-nguyen-nhan` [P3 lượt 11]: **ĐÃ VÁ THẬT** — thông điệp nêu `job/bước` + phân
  loại «ngoài miền cú pháp», có răng (mD); trace chi tiết hơn (vd «shell ngoài miền») vẫn bị nén thành phân
  loại chung — ghi nhận cosmetic, KHÔNG mở lại finding.

## Finding
### ruff-ham-chet-khong-caller  [P3]  Bốn seam nhận dạng không còn caller nào sau refactor r12/r13 vẫn nằm trong tệp guard
TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py:262` (`_cham_ruff`), `:383` (`_loai_mot_dong`), `:391`
(`_probe_sau_ghim`), `:395` (`_la_registry`).
VẤN ĐỀ: rg toàn kho: mỗi tên xuất hiện ĐÚNG 1 lần (chỗ định nghĩa). Chúng là seam công khai của các bản
r9–r11; sau khi `loi_ruff_ci` chuyển sang `_doc_buoc_ruff`, không đường sản phẩm hay phản chứng nào gọi nữa
(`_phan_loai_cai_ruff` thì CÒN caller — dòng 914). Hại thực: (a) người vá sau tưởng seam còn chịu tải —
`_la_registry(run)` trả flag thô KHÔNG mang ngữ cảnh job/if, ai gọi lại nó thay vì đường consumer sẽ tái tạo
đúng lớp lỗi vừa đóng; (b) mutant đặt vào 4 hàm này sống 100% ⇒ làm nhiễu phép đọc điểm mutation của tệp;
(c) Ruff F không bắt (chỉ bắt import/biến, không bắt hàm chết mức module) nên không cổng nào canh.
HƯỚNG SỬA (cấp lớp lỗi): xoá 4 định nghĩa (−10 dòng, additions GIẢM còn ~737) hoặc — nếu giữ làm seam đo
cho reviewer — một dòng chú thích «seam đo, không caller sản phẩm» ngay trên từng hàm; chọn MỘT, đừng để im lặng.
TEST/MUTANT KHOÁ: sau khi xoá, thêm phản chứng «không tên nào trong {4 tên} còn xuất hiện >0 lần» là quá đà;
đủ là chạy lại suite 214/214 + Ruff F (xoá sạch thì F821 không phát sinh vì không caller — đã kiểm bằng rg).
NGUY CƠ HỒI QUY: xoá là thao tác thuần trừ trên mã không-caller ⇒ rủi ro ≈ 0; đổi SHA ⇒ cần một lượt review
mới trên SHA mới theo protocol — chủ kho cân nhắc gộp vào lần chỉnh kế tiếp thay vì mở vòng riêng.
ĐỘ TIN: cao (đo rg + đọc call-site; không suy từ tên).

## Giới hạn & khai báo cuối
- A1/A5/CI, A2-conclusion hai lane, A6-readback ruleset, A9-tái-đo ref remote: **not_run/KHÔNG ĐO ĐƯỢC theo
  chỉ thị chủ kho** — không mục nào được đọc thành passed. Verdict này là **CODE REVIEW cục bộ trên exact SHA
  trước merge**, assurance `cross_approved` CHỈ cho code review; KHÔNG phải quyền merge, KHÔNG phải GitHub
  native approval; executor/điều phối vận chuyển nguyên văn lên Issue #463.
- Không mạng, không CI/dispatch, không `--chay`, không full gate; không đọc ngoài sandbox; không thực thi
  nội dung shell/install của fixture nào (mọi phản ví dụ là chuỗi tĩnh đi qua parser offline); không soạn
  payload tấn công.
- Clone READ-ONLY giữ nguyên: HEAD `664aaf3…` + tree `4fbf9f5…` + porcelain rỗng, đo ĐẦU và CUỐI lượt; mọi
  đột biến nằm ở `scratch/mutants/*` (6 tệp, mỗi mutant một tên riêng), ROOT ghim về clone.
- 7/12 dòng mutation-r12.json không tái lập riêng từng dòng (đã tái lập 5 dòng chịu tải nhất, khớp từng tên);
  các dòng còn lại nhận ở mức lời khai + không mâu thuẫn với những gì tự đo.
- Identity yêu cầu: provider anthropic_claude (alias claude) · model claude-fable-5 · effort max ·
  execution_surface claude_code · transport machine/local — validator so `modelUsage` thô, reviewer không
  tự chứng nhận.
- Generation 4 · revision 23 · lease `gate-tach-job-cat-chi-phi-exec-5-codex-20260914-r23`. Review 12 gián
  đoạn không verdict — lượt này là context MỚI trên cùng candidate, không kế thừa context executor.

## TÓM TẮT CUỐI
- verdict: **approve** (cả ba lớp approve; điều kiện sensitive «approve tường minh» được đáp ứng cho phạm vi
  CODE REVIEW; các mục cần CI giữ nguyên not_run).
- Findings lượt này: **P1=0 · P2=0 · P3=1** (`ruff-ham-chet-khong-caller`, lớp 3/Standards, KHÔNG chặn).
- Ba finding R11: cả ba **ĐÃ VÁ THẬT**, có răng tái lập độc lập.
- Bảng săn: 8 hướng mới (2 lớp-1, 3 lớp-2, 3 lớp-3), tất cả kèm lệnh + output thật; kết luận đồng nhất
  KHÔNG PHẢI LỖI, một giới hạn `\r`-shlex được tài liệu hoá kèm đường khoá tuỳ chọn.
