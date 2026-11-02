verdict: changes_requested
reviewed_sha: 057abc816169688e894f64bbe637ea63d6bd9791
Kết quả: 0 P0, 1 P1, 0 P2, 0 P3.

Hai finding lượt6 đã đóng bằng đúng v1/v2/v3 và witness. Một finding M6 còn mở: hai cận cửa sổ surface đúng trên product HEAD nhưng chưa được test khóa; nới riêng mỗi cận vẫn qua93/93 ca, trong khi fixture ngoài biên cho kết quả sai. Phân P1 theo yêu cầu “chốt không răng” của nhiệm vụ. Suite gốc93/93,135/135;corpus và mô phỏng PR merge rc0/nợ1/60/0. HINT chỉ sửa test,đã kiểm trên scratch93/93,137/137;không áp vào cây review.

## BẢNG ĐO

Các phép đo dùng Python 3.13.17, Git 2.43.0, Ruff 0.16.9 (đọc bằng `--version`). Không gọi mạng/push; mã và fixture đột biến ở `/tmp/wp960-r7-review/` hoặc scratch của helper test. Có một lần Ruff tạo cache ngoài ý định rồi được chuyển ra ngoài, ghi rõ trong nhật ký; không sửa byte mã nguồn. Không tự gán tên execution surface/model/effort chưa đo được.

| Tiêu chí | Lệnh (từ thư mục chứa PROMPT.md, trừ khi ghi khác) | Output thật / kết luận |
|---|---|---|
| SHA/tree/spec | `python3 -B review_checks.py checks` | HEAD `057abc816169688e894f64bbe637ea63d6bd9791`; tree `936b717ecf0afb264b0801fb0a969c9e97bf93bc`; spec sha256 `9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca`; lease r2/g2 đúng. |
| Phạm vi vá lượt6 | `git -C cay-kho diff --numstat 78c138f HEAD -- ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py` | Chỉ test +17/−1; blob product bằng `6dca85f` và `78c138f`: `83ba1d37a902b7064f95e2efb2a2d0f197a81733`. |
| Suite gốc B7 | `PYTHONDONTWRITEBYTECODE=1 python3 -B -u /tmp/wp960-r7-review/head/ops/bien_nhan_v2_test.py` | **rc0,93/93 ca,135/135 đột biến thường CÓ RĂNG,2/2 tự kiểm,117/135 khai đối chứng,TỔNG: ĐẠT** (`evidence/suite.log`). |
| M1/B1 bỏ mốc | `python3 -B review_cases.py acceptance`; AST ở `evidence/m1-static.log` | c86 cả hai luật rc1; không literal `dung_tai`, không hàm `_moc_*`/`_commit_them_cau`/`_co_cau`; m94 bị c86 giết. |
| M2/B2 một biên lỗi | `python3 -B review_cases.py closure`; `python3 -B review_probes.py surface-errors` |11/11 ca closure qua; c91 có17 nguồn×2 trạng thái nợ; JSON bổ sung10/10 rc2; không traceback/NỢ CHẾT. |
| M3/B3 OID theo ngữ cảnh | `python3 -B review_cases.py acceptance`; `python3 -B review_mutants.py v3 --all` | c87 bốn ngữ cảnh thiếu→2; token thường→0; c78 OID thuần thật→1. v3 đúng c87 đỏ tại `tron-so-chu-rieng`,92/93. |
| M4/B4 lời tự khai | `python3 -B review_cases.py acceptance` | c73/c79/c83/c88 qua; HEAD đúng provider/citation/cửa sổ/mọi khai báo trên dòng/caveat. **Thiếu răng ở biên ngoài cửa sổ, finding mới bên dưới.** |
| M5/B5 corpus HEAD | `python3 -B review_checks.py corpus` | **rc0,244 v2+11 legacy+42 nợ=297;0 lỗi/0 unknown;nợ1/60/0**. |
| B5 corpus base | `python3 -B review_topology.py base-recheck` | HEAD code trên corpus/ref base4488444:rc0/nợ1/60/0; code gốc base:rc0/nợ1/60/3. |
| B5 nợ rỗng/bánh cóc | `python3 -B review_topology.py debt` | **rc1/61 lỗi ba luật/0 lỗi khác/0 unknown**; tập khóa đúng61 mục đóng băng; mọi tệp có thật; subset test=true. |
| B6 literal/folded | acceptance c72; suite m78 | c72 qua,m78 giết đúng literal `khoi_lit`; folded là hồi quy và docstring khai giới hạn rõ. |
| B7 Ruff F delta | `python3 -B review_checks.py ruff` (lượt cuối có `--no-cache`) | Cả base/head đúng1 F541 ở test:1677:19;delta0. **Bare lint hai tệp packet**, không suy thành toàn kho hoặc Ruff pin/probe contract. |
| B7 doctrine | `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` tại cay-kho | rc0,sạch,quét10 tệp/0 chỗ chép doctrine. |
| B7 whitespace/size | `git -C cay-kho diff --check 44884446f71c89e25f9a72ac58e4f597db63c1ba HEAD`; `... diff --numstat ... -- ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py` | diff-check rc0/rỗng;product+297/−193,test+699/−104,tổng1.293 dòng. Disclosure ADR-0044 trên PR online **KHÔNG ĐO ĐƯỢC**, cấm mạng. |
| B8 nền tái dựng | `python3 -B review_misc.py baseline` dùng test HEAD/module base4488444 | c86/c89/c87/c88 đỏ đúng các thiếu sót nền; không phải finding HEAD. Không chứng kiến thời điểm executor bắt đầu. |
| CI PR merge mô phỏng | `python3 -B review_topology.py ci` | merge2 parent/tree candidate,full history,không origin/HEAD,origin/master79dbaf4 ⇒**rc0,nợ1/60/0**. Không thay check run GitHub thật. |
| M6 răng lượt6 | `python3 -B review_mutants.py v1 --all`; tương tự v2/v3; `python3 -B review_probes.py r6-witness` | v1/v2/v3 mỗi bản92/93,chỉ c94/c94/c87 đỏ đúng lý do; witness HEAD2/2→mutant1/0,0/1,0/1. |
| M6 mutant reviewer mới | `python3 -B review_mutants.py <n1,n2,n3,n5,n7>`; `... n4-provider-next-boundary --all`; `... n8-provider-prev-boundary --all` |5 mutant mới bị đúng ca giết/c18 nghiêm qua; n4/n8 mỗi bản sống **93/93,red=[]**, có witness sai0→1 và1→0. **M6 chưa đạt.** |
| HINT.patch | `python3 -B review_hint.py` | `patch --dry-run --fuzz=0 -p0`rc0/không offset; chỉ test; c88 sau áp qua, hai mutant nới cửa sổ bị giết đúng vi/vii,c18 qua. **Fullsuite hint rc0,93/93 ca,137/137 đột biến thường,2/2 tự kiểm** (`evidence/hint-suite.log`). |
| CI/PR/authority online | Không gọi mạng theo nhiệm vụ | Check run trên057abc8,PR disclosure/merge status/authority online **not_measured**; không suy từ CI78c138f. |

## BẢNG ĐÓNG FINDING LƯỢT 6

| Slug | Trạng thái | Lệnh | Output thật |
|---|---|---|---|
| chot-oid-va-loai-batch-check-chua-co-rang | **ĐÓNG** hai guard đã nêu | `python3 -B review_mutants.py v1 --all`; `... v2 --all`; `python3 -B review_probes.py r6-witness` | Mỗi mutant92/93,chỉ c94 `giet_that` tại `batch-check-sai-oid`/`batch-check-sai-loai`;m137/m138 chính thức CÓ RĂNG. HEAD2/2→mutant1/0 và0/1; đối chứng nghiêm qua. |
| ngu-canh-tron-so-chu-chua-co-rang-rieng | **ĐÓNG** guard mixed riêng | `python3 -B review_mutants.py v3 --all`; cùng r6-witness |92/93,chỉ c87 `giet_that` tại `tron-so-chu-rieng`;m139 chính thức CÓ RĂNG. `12ab34c` thiếu thật,HEAD2/2→mutant0/1; đối chứng nghiêm qua. |

Hai finding cũ đóng ở phản chứng cụ thể. Không tuyên bố toàn lớp `bo-chon-ung-vien` đã đóng: một thiếu răng khác của M4 được tìm thấy ở lượt này.

## BẢNG SĂN

| Hướng độc lập | Lệnh | OUTPUT THẬT / kết luận |
|---|---|---|
| Bỏ nguồn gốc câu/mốc | `python3 -B review_cases.py acceptance` c86;AST | review/ancestry có dung_tai vẫn1;không còn hàm/literal mốc. |
| OID thật/thiếu và ngữ cảnh | acceptance c71/c78/c87; `python3 -B review_probes.py r6-witness` | thuần thật1;40/backtick/commit/mixed thiếu2;deadbeef/run0;v3 bắt đúng mixed riêng. |
| I/O/YAML/JSON và biên sinh nợ | `python3 -B review_cases.py closure`; `python3 -B review_probes.py surface-errors` |11/11 qua,JSON10/10 rc2,không NỢ CHẾT/Traceback;hai cờ sinh nợ giữ biên lỗi. |
| Ref/object/clone hỏng có diagnostic | closure c91/c93/c94 |tree/ref hỏng/symref gãy/empty object/mơ hồ/shallow/partial ⇒2/2;blob chung tiền tố không làm commit mơ hồ. |
| Stderr và mã thoát bất thường | `python3 -B review_probes.py stderr`; closure c96 |same-error,health-error,healthrc3 đều2/2;probe cũ đã bỏ1/0. |
| Môi trường hợp lệ/object pool/worktree | `python3 -B review_topology.py config`; closure c95 |false/no/off1/0,true/yes/on2/2;alternates env/file và linked worktree fsck0/gate1/0;GIT_DIR/trace/replace cô lập. |
| Giao thức batch-check từng vế | `python3 -B review_mutants.py v1 --all`;v2; r6-witness |92/93,mỗi lượt chỉ c94 đỏ;HEAD2/2→mutant1/0 hoặc0/1. Hai guard cũ đóng. |
| Cửa sổ surface chính xác và ngoài biên | `python3 -B review_mutants.py n4-provider-next-boundary --all`; `python3 -B review_probes.py window-fixture` |**93/93red=[]**;provider cách hai dòng khiến mutant0→1;HEAD đúng. Finding thiếu răng M6. |
| Citation ngoài cửa sổ | `python3 -B review_misc.py citation-window` |Fixture c88 có citation cách hai dòng:HEAD qua;mutant trái/phải đỏ viii/ix (đòi1,được0). Cùng lớp cửa sổ. |
| Nợ thật/bánh cóc trên corpus/base | `python3 -B review_topology.py debt`; `... base-recheck` |nợ rỗng1/61luật/0 unknown;keys bằng đóng băng;HEAD-code/base-corpus0/nợ1/60/0. |
| Checkout PR merge đầy đủ | `python3 -B review_topology.py ci` |hai parent,tree candidate,shallowfalse,không origin/HEAD ⇒0/nợ1/60/0. |
| Đột biến mới có đối chứng | `python3 -B review_mutants.py <n1,n2,n3,n5,n7>` |c88/c87/c69/c88/c88 `giet_that` đúng assertion;c18 nghiêm qua5/5. |

## NHẬT KÝ ĐO TĂNG DẦN

### Hướng 1 — neo SHA, đặc tả và phạm vi vá

Lệnh tại `cay-kho/`: `git rev-parse HEAD HEAD^{tree}`; `git status --porcelain=v1`; `git rev-parse --is-shallow-repository`; `sha256sum ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md`; `git diff 6dca85f HEAD -- ops/bien_nhan_v2.py`; `git diff --numstat 44884446f71c89e25f9a72ac58e4f597db63c1ba HEAD -- ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py`.

Output: HEAD `057abc816169688e894f64bbe637ea63d6bd9791`; tree `936b717ecf0afb264b0801fb0a969c9e97bf93bc`; status rỗng; shallow `false`; đặc tả sha256 `9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca` khớp. Diff product so `6dca85f` rỗng. Hai tệp packet so base: `297/193` và `699/104` dòng thêm/xóa (1.293 dòng cộng). Lease r2/g2 ghi đúng spec/hash/base/write set. Các commit merge giữa base và head có tệp khác; review giới hạn hai tệp packet và hành vi trên cây HEAD.

### Hướng 2 — kiểm tĩnh và không phá nền

Lệnh `python3 -B review_checks.py checks` ⇒ rc=0. `git diff --check 44884446f71c89e25f9a72ac58e4f597db63c1ba 057abc816169688e894f64bbe637ea63d6bd9791` ⇒ rc=0, stdout/stderr rỗng. Doctrine-scan ⇒ rc=0, `sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. Blob product ở `6dca85f`, `78c138f`, HEAD cùng `83ba1d37a902b7064f95e2efb2a2d0f197a81733`. Diff từ lượt 6 chỉ test `17 thêm/1 xóa`.

Lệnh `python3 -B review_checks.py ruff` ⇒ đo `ruff check --select F --output-format json` trên đúng hai tệp lấy bằng `git show` ở base/HEAD: cả hai cùng một `F541` tại `ops/bien_nhan_v2_test.py:1677:19`, `f-string without any placeholders`; delta=0. Log `evidence/checks.log`, `evidence/ruff.log`. Disclosure kích thước PR/CI từ GitHub chưa đo do cấm mạng; không suy chúng đã đạt từ lời executor.

### Hướng 3 — M1–M5/B1/B3/B4/B6 trên fixture Git thật

Lệnh `python3 -B review_cases.py acceptance` ⇒ rc=0, **13/13 ca qua** (`c69,c70,c71,c72,c73,c74,c75,c78,c79,c83,c86,c87,c88`). Nhật ký `evidence/acceptance.log` giữ từng rc, lỗi và mục chưa đo: B1 cả hai luật vẫn rc1 khi có mốc; B3 bốn ngữ cảnh OID thiếu rc2, hai token thuần không ngữ cảnh rc0, ranh giới precommit/backtick mở rc0; OID thuần thật rc1. B4 provider trước/cùng/sau, citation và notprovider đúng các kết quả kỳ vọng. B6 c72 qua; docstring khai folded chỉ hồi quy.

### Hướng 4 — biên lỗi, ref, object, clone và đóng phản chứng cũ

Lệnh `python3 -B review_cases.py closure` ⇒ rc=0, **11/11 ca qua** (`c77,c82,c84,c89,c90,c91,c92,c93,c94,c95,c96`). Có output từng lần gọi CLI/kiem trong `evidence/closure.log`: c91 đo 17 loại nguồn × 2 trạng thái nợ; mọi nguồn lỗi rc2, không Traceback/NỢ CHẾT. Bao gồm ref tree/hỏng/symref gãy, object rỗng có diagnostic, kho nông/partial thật, grafts, UTF8, alias vòng, run.json thư mục/symlink/tên dài, Git vắng. c92 khóa cả hai cờ sinh nợ; c95 khóa replace, GIT_DIR, trace, ref con, promisor tắt, nguồn object phụ; c96 trả rc2 cho rc3/stderr rỗng.

### Hướng 5 — corpus thật ở exact HEAD

Lệnh `python3 -B review_checks.py corpus` chạy `python3 -B ops/bien_nhan_v2.py --root .` trên bản sao nguyên cây HEAD ⇒ **rc0**: `244 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 297`; `nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 0 · L-SURFACE chua_do_duoc 0`; `TỔNG: ĐẠT`. Log `evidence/corpus.log`.

### Răng lượt 6 và kiểm tra giàn giáo

`python3 -B review_mutants.py v1|v2|v3` đã làm đúng c94/c94/c87 `giet_that`, lần lượt nêu `batch-check-sai-oid`, `batch-check-sai-loai`, `tron-so-chu-rieng`; đối chứng nghiêm c18 qua. `python3 -B review_probes.py r6-witness`: fixture Git fsck0, OID toàn chữ `dbffbbc…` và token thiếu thật `12ab34c`; cặp rc không nợ/có nợ HEAD đều **2/2**, mutant v1 **1/0**, v2/v3 **0/1** (có nợ in NỢ CHẾT). Cổng HEAD đóng đúng cả hai finding lượt 6.

Lần chạy toàn 93 ca đầu dùng helper `_dot_bien_tep` của suite; c42 dọn danh sách scratch toàn cục nên xóa chính tệp mutant ngoài. Các lỗi c14/c44/c66/c68 trong `*-rig-initial.log` vì tệp mất là **lỗi giàn giáo reviewer, không phải finding**, không dùng làm răng hoặc mẫu số. Đang chạy lại toàn ca bằng bản sao nguyên cây riêng, ghi đột biến vào product của bản sao và kiểm băm còn nguyên cuối lượt.

### Hướng 6 — JSON hỏng và stderr không được thành sạch

`python3 -B review_probes.py surface-errors` ⇒ **10/10** lượt (JSON lỗi, UTF8 lỗi, mảng, null, surface rỗng × có/không nợ) đều rc2, không Traceback/NỢ CHẾT. `python3 -B review_probes.py stderr` ⇒ same-error-wrong-ancestry, health-error, health-rc3 đều **2/2**; old-probe-only **1/0** vì probe --git-dir cũ không còn. Đây là tiêm lỗi giao thức trên fixture Git thật, không tuyên bố Git tự sinh stdout/stderr giả. Log `evidence/surface-errors.log`, `evidence/stderr.log`.

### Hướng 7 — mô phỏng checkout PR merge

`python3 -B review_topology.py ci` ⇒ bản sao có merge `42e2cc7a68c4c450f5e6640659064f9cd7167211`, hai parent `79dbaf443f90daece751d9ab2537796bbd6084bf` + exact candidate; tree `936b717ecf0afb264b0801fb0a969c9e97bf93bc` bằng candidate. `--is-shallow-repository=false`; `symbolic-ref -q refs/remotes/origin/HEAD` rc1, output rỗng; origin/master ở `79dbaf4`. Gate với `GITHUB_EVENT_NAME=pull_request` ⇒ **rc0, TỔNG: ĐẠT, nợ 1/60/0**. Đây là mô phỏng cục bộ, không phải check run GitHub thật. Log `evidence/ci.log`.

### Sửa thao tác reviewer: cache Ruff

Đo `git status --porcelain=v1 --ignored` phát hiện `!! .ruff_cache/`; bản sao đầu lượt (chép trước khi lint) không có thư mục ấy. Lệnh Ruff đầu đã tạo cache ngoài ý định trong cây review. Tôi đã chuyển đúng cache này ra `/tmp/wp960-r7-review/accidental-ruff-cache`, rồi đo lại với `ruff check --no-cache` và cwd ngoài checkout (`evidence/ruff-no-cache.log`), vẫn cùng F541/delta0. Không sửa nội dung mã nguồn. Không khai rằng cây review chưa từng có ghi tạm; cuối lượt sẽ đo lại HEAD/tree/index/tracked/untracked/ignored.

### Hướng 8 — cấu hình hợp lệ, kho dùng object pool và worktree

`python3 -B review_topology.py config`: `remote.archive.promisor=false/no/off` đều Git fsck0/stderr rỗng, cổng **1/0** (không nợ/có nợ). true/yes/on đều **2/2**. Dời toàn bộ object sang pool ngoài: cung cấp qua biến môi trường hoặc `.git/objects/info/alternates` đều fsck0 và **1/0**; linked worktree bình thường cũng fsck0 và **1/0**. Log `evidence/config.log`. Không lặp finding đối với cảnh báo cấu hình theo tiền đề B2 của chủ kho.

### Hướng 9 — đột biến reviewer mới và ranh giới cửa sổ

`python3 -B review_mutants.py n1-window-before|n2-commit-case|n3-review-round-order|n5-citation-line-digit|n7-citation-current-only` đã đo **5 mutant mới khác m hiện có**, mỗi cái chỉ thay đúng một mẫu: c88 đỏ i-tu-khai; c87 đỏ sau-commit; c69 đỏ co-luot-sau; c88 đỏ ii-trich-dan-ke; c88 đỏ ii-trich-dan-ke. Tất cả `giet_that`, đối chứng nghiêm c18 `(true, "")` (`evidence/new-mutants.log`).

Mutant thứ 6 `n4-provider-next-boundary` nới duy nhất cuối cửa sổ từ `j+2` thành `j+3`; c88 gốc vẫn qua. `python3 -B review_probes.py window-fixture` chỉ đổi fixture iii của c88: thêm dòng trống rồi `provider` sau khai báo hai dòng. HEAD c88 qua (đúng rc0), mutant đỏ tại iii (sai rc1/L-SURFACE). Đang đo toàn93 ca trên bản sao nguyên cây trước khi kết luận thiếu răng M6. Log `evidence/window-fixture.log`.

### Hướng 10 — base lease, nợ rỗng và B8

`python3 -B review_topology.py base-recheck`: checkout đúng `44884446f71c89e25f9a72ac58e4f597db63c1ba`, đặt origin/master và origin/HEAD của bản sao về chính base ấy. Mã HEAD đo corpus base ⇒ **rc0, nợ1/60/0, không lỗi/unknown**. Mã gốc base chạy chính corpus ấy ⇒ rc0, nợ1/60/3 (định nghĩa surface r1). Không nhầm số nợ giữa hai định nghĩa. Log `evidence/base-recheck.log`.

`python3 -B review_topology.py debt`: mã HEAD trên corpus HEAD, nợ câu rỗng ⇒ **rc1, đúng61 vi phạm (60 L-ANCESTRY+1 L-REVIEW), 0 lỗi khác, 0 unknown**; tập khóa bằng NO_CAU_LICH_SU, không mục trỏ tệp mất, tập con bản đóng băng test=true (`evidence/debt.log`). M1 kiểm AST: `forbidden_functions=[]`, `dung_tai_literal_lines=[]` (`evidence/m1-static.log`).

`python3 -B review_misc.py baseline` (`evidence/baseline.log`): chạy nguyên c86/c89/c87/c88 của HEAD với module exact base, lần lượt đỏ vì miễn mốc rc0, receipt-thư-mục IsADirectoryError,40 hex thiếu thành0,citation bị bắt nhầm1. Đây là nền phải đỏ của B1–B4; không phải finding HEAD và không chứng kiến thời điểm executor bắt đầu.

### Hướng 11 — toàn93 ca trên mutant nguyên cây (đã loại lỗi giàn giáo)

`python3 -B review_mutants.py v1 --all`, `v2 --all`, `v3 --all`: mỗi bản sao **92/93**, duy nhất c94/c94/c87 đỏ `giet_that`, đúng lời `batch-check-sai-oid`, `batch-check-sai-loai`, `tron-so-chu-rieng`; kiểm SHA256 cuối lượt chứng minh source mutant không bị dọn hay ghi lại. Vì vậy hai finding lượt6 đóng đúng nghĩa, không lĩnh tín dụng từ lỗi vô can.

`python3 -B review_mutants.py n4-provider-next-boundary --all`: **93/93, red=[]**, c18 đối chứng nghiêm qua, SHA256 mutant cuối lượt `720966c7fe5f87ad78ff64ac353487a1bf2c6c69a8d3cfa9e308295153b73927` khớp đầu lượt. Kết hợp witness ở hướng9 chứng minh một thiếu răng M6 mới.

### bien-ngoai-cua-so-surface-chua-co-rang [P1] Mở rộng cửa sổ M4 vẫn qua toàn93 ca

HÌNH DẠNG: bo-chon-ung-vien

TỆP/DÒNG: `ops/bien_nhan_v2_test.py:2974` (ma trận c88, nhất là dòng2983); `ops/bien_nhan_v2.py:1276` (chốt đúng nhưng chưa được test khóa đủ).

VẤN ĐỀ: M4 giới hạn lời tự khai ở đúng ba dòng {trước, hiện tại, sau}; M6 đòi đột biến cho từng chốt. Các ca hiện hữu chỉ có provider ở trong cửa sổ hoặc vắng hoàn toàn, citation ở trong cửa sổ. Nới cận phải `j+2` thành `j+3` (bắt cả hai dòng sau) HOẶC riêng cận trái `j-1` thành `j-2` đều qua93/93 ca,red=[];c18 nghiêm qua và băm mutant giữ nguyên cuối lượt. Trên fixture c88 chỉ thêm một dòng trống và provider ở dòng thứ hai sau khai báo, HEAD đúng rc0 nhưng mutant sai rc1/L-SURFACE. Đây là thiếu răng M6 theo ngưỡng P1 của nhiệm vụ; chưa thấy product HEAD sai trên witness này.

ĐÃ THỬ NGHIỆM: `python3 -B review_mutants.py n4-provider-next-boundary --all` và `python3 -B review_mutants.py n8-provider-prev-boundary --all` ⇒ mỗi bản93/93,red=[],c18 nghiêm qua,product mutant giữ đúng băm cuối lượt. `python3 -B review_probes.py window-fixture` ⇒ c88 HEAD qua, mutant `giet_that` tại `iii-khong-provider` (đòi0,được1). Hai phép chạy trên bản sao/fixture Git thật, không sửa object,graph hay nguồn Git. Logs `evidence/n4-provider-next-boundary.log`, `evidence/n8-provider-prev-boundary.log`, `evidence/window-fixture.log`. `python3 -B review_misc.py citation-window` còn đo chiều ngược: citation cách hai dòng không miễn lời tự khai ở HEAD (rc1),nhưng mutant trái/phải làm rc0;sau đổi fixture,c88 đỏ đúng viii/ix (`evidence/citation-window-witness.log`).

Gợi ý vá: thêm vào c88 các hàng provider/citation cách khai báo ĐÚNG hai dòng, cả trước và sau, với rc tương ứng0/1; thêm hai mutant nới cận trái/phải và đòi chúng giết đúng c88. Chỉ sửa test. Rủi ro cần khóa: blank line và dòng prefix phải được giữ nguyên để fixture thật sự đặt token ngoài cửa sổ. `HINT.patch` đã dry-run `patch --dry-run --fuzz=0 -p0` sạch trên bản sao exact HEAD; sau áp scratch, c88 qua, hai mutant giết đúng vi/vii, c18 nghiêm đều qua (`evidence/hint-validation.log`). Fullsuite gợi ý trên scratch đã **rc0,93/93 ca,137/137 đột biến thường,2/2 tự kiểm,TỔNG: ĐẠT** (`evidence/hint-suite.log`).

ĐỘ TIN: cao

## BẢNG ĐÓNG PHẢN CHỨNG LƯỢT 1–5

Chỉ đóng các biểu hiện/guard đã nêu, không tuyên bố mọi biểu hiện cùng lớp đều hết. `closure` và `acceptance` là lệnh `python3 -B review_cases.py <nhóm>`; `suite` là lệnh suite nguyên gốc ở BẢNG ĐO. Các m trong bảng có output `CÓ RĂNG … = giet_that` thực tế trong `evidence/suite.log`.

| Nguồn / slug | Trạng thái | Lệnh / output tại HEAD |
|---|---|---|
| 1/git-hong-thanh-token-thuong | ĐÓNG | closure c91/git_vang:2/2,diagnostic không gọi được git;m103 bị bắt. |
| 1/b2-chua-do-du-ma-tran | ĐÓNG | closure c91:17 nguồn×2 trạng thái nợ;surface-errors bổ sung JSON10/10;rc2,không NỢ CHẾT/Traceback. |
| 1/run-json-thu-muc-thanh-khong-ap | ĐÓNG | closure c91/run_json_thu_muc2/2;m106 bị bắt. |
| 1/nhanh-mac-dinh-tree-bi-bo-qua | ĐÓNG | closure c91/nhanh_la_tree2/2,nêu refs/remotes/origin/master;m104 bị bắt. |
| 1/sinh-no-ngoai-bien-doc-receipt | ĐÓNG | closure c92:hai cờ sinh nợ rc2 với nguồn lỗi;m108 bị bắt. |
| 1/bien-utf8-receipt-chua-co-rang | ĐÓNG | closure c91/receipt_utf8:2/2,nêu UnicodeDecodeError;m107 bị bắt. |
| 1/b6-docstring-chua-khai-gioi-han | ĐÓNG | acceptance c72 qua;docstring khai folded chỉ hồi quy;m78 giết literal. |
| 1/bo-chon-moi-chua-khoa-bien | Bốn phản chứng cũ ĐÓNG; lớp còn MỞ | Suite m110–m113 bị đúng c87/c88 giết (precommit/backtick mở/notprovider/provider sau). Biên ngoài cửa sổ chưa khóa, finding mới `bien-ngoai-cua-so-surface-chua-co-rang`. |
| 2/sinh-no-van-thoat-loi-yaml | ĐÓNG | closure c92 qua,timestamp lỗi/lồng sâu đều vào biên;m109 bị bắt. |
| 2/ref-hong-bi-doc-thanh-vang | ĐÓNG | closure c91 loose ref hỏng/symref gãy2/2;m114/m119 bị bắt. |
| 2/peel-rc1-an-loi-object | ĐÓNG | closure c91/object_rong2/2,stderr is empty;không thành token thường. |
| 2/chot-loi-do-moi-chua-co-rang | ĐÓNG các guard cũ | Suite m114–m119 đều CÓ RĂNG (stderr,lstat,stat lỗi,shallow,partial,symref). |
| 2/loc-ung-vien-commit-chua-co-rang | ĐÓNG | closure c93 qua:commit/blob chung tiền tố không mơ hồ;suite m120 bị c93 giết. |
| 3/stderr-rong-van-tin-lich-su-hong | TIỀN ĐỀ B1,không phải vá | Chủ kho loại object sai băm/commit-graph sai parent mà Git im lặng khỏi phạm vi. Không khai gate thay fsck;không lặp finding. |
| 3/replace-graft-lam-sai-quan-he-oid | ĐÓNG | closure c95/replace đúng1/0;c91/graft2/2 dù warning tắt;m127/m130 bị bắt. |
| 3/git-dir-ke-thua-do-nham-kho | ĐÓNG | closure c95/git_dir_khac qua,kho ngoài master=X;suite m136 giết đúng ca. |
| 3/stderr-vo-hai-chan-nham-kho-lanh | Trace ĐÓNG;cấu hình warning là tiền đề B2 | closure c95/GIT_TRACE vẫnrc1;c91/warningrc2 đúng thiết kế. Không coi môi trường ngoài tiền đề thành finding. |
| 3/for-each-ref-nhan-nham-ref-hau-to | ĐÓNG | closure c95/ref_con_tien_to qua (đúngrc1),suite m131 bị bắt. |
| 3/chot-ma-thoat-git-chua-co-rang | ĐÓNG | closure c96 merge-base/healthrc3 stderr rỗng→2;suite m125 bị bắt. |
| 3/ca-partial-chi-bat-cau-hinh-cu | ĐÓNG | closure c91 clone partial file:// thật2/2;suite m129 bị bắt. |
| 4/stderr-nen-nuot-loi-that | ĐÓNG | `python3 -B review_probes.py stderr`:same-error-wrong-ancestry2/2;không phép trừ stderr nền. |
| 4/promisor-false-bi-coi-la-partial | ĐÓNG | `python3 -B review_topology.py config`:false/no/off fsck0,gate1/0;true/yes/on2/2;m132/m134 bị bắt. |
| 4/xoa-alternates-hop-le-lam-mat-object | ĐÓNG | config:object pool env/file fsck0,gate1/0;suite m133 bị bắt. |
| 4/chot-probe-git-chua-co-rang | ĐÓNG | probe --git-dir cũ đã xóa;closure c96/healthrc3 và stderr/healtherror2/2;suite m125 bị bắt. |
| 5/chot-promisor-moi-chua-co-rang | ĐÓNG | c94 giá trị maybe ném đúng KhongDoDuoc,m135 bị bắt;c95 dùng off/no,m134 bị bắt. config chứng minh Git thậtoff/no không bị chặn nhầm. |
| 5/c95-git-dir-khac-khong-phan-biet-kho | ĐÓNG | Fixture c95 hiện chuyển master kho ngoài sangX;closure c95 qua,m136 bị chính git_dir_khac giết. |

## BẢNG LỚP VÀ PHẠM VI KẾT LUẬN

| Lớp / hình dạng | Nguồn | Kết luận lượt này |
|---|---|---|
| loi-do | Các finding r2 lượt1–6 | Các guard/phản chứng cụ thể nêu trên đóng hoặc thuộc tiền đề B1/B2. Chưa tìm thấy lỗi đo mới trên HEAD trong các hướng đã chạy. Không chứng minh phủ mọi lỗi môi trường có thể có. |
| bo-chon-ung-vien | r2 lượt1 `bo-chon-moi-chua-khoa-bien`,lượt2 lọccommit,lượt6 mixed;finding mới lượt7 | Hai guard cũ đã khóa nhưng lớp vẫn **MỞ**,mức cao nhất P1,1finding hiện tại:cửa sổ surface thiếu đối chứng ngoài biên. Sửa chung ở ma trận c88 và hai đột biến cận cửa sổ. |
| nguon-goc-cau | r1 các mốc/lịch sử | Đã bỏ cơ chế;AST âm và c86 dương phù hợp M1. Không finding lượt này. |
| khac | B2 coverage/B6 docstring các lượt cũ | Các biểu hiện đã nêu đóng;không finding mới. |

Finding hiện tại thuộc hình dạng đã có trong `hinh_dang_ke_thua`. Theo Q8 của đặc tả và M-4 của lease, quyết định xử lý tiếp thuộc chủ kho. Lượt này là trần cuối theo nhiệm vụ; verdict/HINT không cấp thêm vòng review hoặc quyền merge/land.


### Hướng 12 — hai cận đối xứng, gợi ý có răng và readback cuối

`python3 -B review_mutants.py n8-provider-prev-boundary --all` ⇒ **93/93,red=[]**, đối chứng nghiêm c18 qua, băm mutant trước/sau giữ `17ff34f130596e47ee1c680ad80d63b5e23cab0e3c50ef3a9658605020bd5340`. Cả hai cận thuộc cùng một finding,không đếm thành hai lỗi. `python3 -B review_misc.py citation-window` ⇒ HEAD qua cả hai chiều;mutant c88 đỏ đúng `viii-trich-dan-truoc-hai-dong` và `ix-trich-dan-sau-hai-dong` (đòi1,được0). Chỉ đổi các fixture c88 có sẵn;không dùng Git/object hỏng làm witness.

`python3 -B review_hint.py` ⇒ dry-run và áp patch trên bản sao exactHEAD đều rc0,không fuzz/offset. Sau áp,c88 qua;mutant cận trái/phải bị giết đúng vi/vii;c18 nghiêm qua. `PYTHONDONTWRITEBYTECODE=1 python3 -B -u /tmp/wp960-r7-review/hint/ops/bien_nhan_v2_test.py` ⇒ **rc0,93/93 ca đạt ·137/137 đột biến thường CÓ RĂNG ·2/2 ca TỰ KIỂM đạt ·119/137 đột biến thường khai đối chứng;TỔNG: ĐẠT**. Các mẫu đột biến m140/m141 trong hint là gợi ý test,chưa phải commit ứng viên. Log `evidence/hint-validation.log`,`evidence/hint-suite.log`.

`python3 -B review_misc.py final-state`: `git status --porcelain=v1 --ignored` cuối lượt stdout rỗng;tracked/index diff đều rc0;HEAD/tree vẫn đúng;origin/HEAD vẫn trỏ candidate,origin/master vẫn `79dbaf443f90daece751d9ab2537796bbd6084bf`. Spec và hai tệp packet byte-identical với bản sao đầu lượt;spec sha256 giữ nguyên. Product sha256 `82a667496adc4ebbe9516f484fc4d9da4e79570ac20006b122a7400d0be539f6`,test sha256 `0b8c885c72c2e4b12e140ba617ddc9ea87cc5c687cfa57da863021b67a5c7dfa`. Log `evidence/final-state.log`. Snapshot cuối sạch không xóa sự kiện cache Ruff đã ghi rồi chuyển ra ngoài,đã khai riêng ở trên.

Kết luận severity: **1 lớp còn mở,1 finding P1 gồm2 cận cửa sổ chưa khóa (4 tình huống provider/citation trước/sau),0P0/0P2/0P3**. M6 chưa đạt nên không approve. Mọi sửa gợi ý chỉ là artifact để chủ kho/executor cân nhắc theo stop condition,trần review và thẩm quyền hiện hành.
