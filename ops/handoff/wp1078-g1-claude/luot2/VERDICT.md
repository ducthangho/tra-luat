verdict: changes_requested
reviewed_sha: 0311db45d5786c3d4a1c05fec1375aec9e727249
spec_sha256: 2fb1b2633ae09e4b737f97d601186389fd801cc294a5217ea07b3e761c3bf13b

Ket qua: 0 P0, 0 P1, 1 P2, 0 P3.

Kết luận nội dung: F01 đã vá thật. Bản vá F02 đo được chốt dùng lại ở môi trường sạch,
nhưng fixture mới kế thừa thuộc tính export/allexport nên có thể đi sai nhánh và đỏ oan;
F02 được phân loại VÁ SINH LỖI MỚI, còn mở P2. Không tìm thấy lỗi runtime M1/M2 của shell HEAD.
Đề nghị sửa chỉ TEST trong HINT.patch đã được đo trên bản sao. Đây là lời gọi2/2 cuối;
còn P2 thì dừng tại checkpoint chủ kho, không tự gọi lượt review thứ ba.

Preflight: HEAD đúng SHA trên; tree `740ca2f9380fdbcffcc4d11ad03293283d576f37`;
base `90c101b8d1f8895b66607de8582a18c5e72d834c`. Git status ban đầu rỗng.
`sha256sum SPEC.md` khớp hash đóng băng. `cmp diff.patch evidence/git-diff.patch`: rc0.
Numstat: test +98/-5, shell +10/-7; chỉ hai tệp được giao.
`ls -ld /tmp/.git`: tồn tại, read-only; sẽ đối chiếu lỗi môi trường với base.
Launcher đã chạy trọn ở hai vế; nhật ký và output ở `evidence/launcher-head.*`, `launcher-base.*`.

## ĐỐI CHIẾU LƯỢT TRƯỚC — kết quả đã đo

`PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/probe_tests.py` (từ `cay-kho/`):
HEAD 6/6 ca mục tiêu PASS. Mọi mutant ở bản sao tạm ngoài cây.

- F01 `no-function-invocation-assertion`: ĐÓNG. Mutant `wp1078_goi_ham_python_thua`
  làm chính ca M3 ném `TinHieuChotCa: linux: ham python ke thua da bi goi`.
- F02 `reused-py-guard-unmeasured`: VÁ SINH LỖI MỚI. Trong môi trường sạch, mutant
  `wp1078_chot_chi_nhanh_chon_moi` làm đúng ca ném `TinHieuChotCa`, rc3 thay4.
  Nhưng ca mới không bảo đảm marker không export: hai lần chạy HEAD với SHELLOPTS=allexport
  hoặc marker môi trường đều đỏ0/1, trong khi script đúng đang chọn nhánh mới. Chi tiết finding dưới đây.
- M4: command-v giết đúng4/4; bỏ guard giết shape1/1; kết hợp cả hai giết cả3
  ca hành vi. Base `086f1b7` và `90c101b` đều làm hai ca HINT đỏ bằng assertion của ca,
  rc1, GITHUB_PATH rỗng. Chi tiết: `evidence/targets.json`, `evidence/targets.log`.

## Phạm vi và cách chạy lại

PR #1097 / packet #1078 r1/g1, lease `wp1078-r1-g1-claude`, sensitive, lượt Codex 2/2 cuối.
Reviewer: Codex/OpenAI, provider `openai_codex`; bề mặt API có shell cục bộ, transport machine/local.
Context độc lập với executor Claude. Model/effort phục vụ thực tế: KHONG DO DUOC — các trường quan sát
trong `runs/9f526f63/run.json` hiện null. Không suy danh tính model từ actor vận chuyển; chưa publish,
GitHub submitter=null. Windows: `required` vì diff chạm `.sh` và `.claude/dev/**`; thực thi native còn chưa đo.

Môi trường: Linux, Bash 5.2.21, Python 3.13.16, Ruff 0.17.1. Không gọi mạng, push hoặc dùng credential thật.
Script đo/đột biến và clone base đều ngoài `cay-kho/`. Shell/test nguồn không được vá.
Các lệnh dưới đây chạy từ `cay-kho/`, tại exact HEAD nêu trên. Định nghĩa viết tắt chạy được:

```bash
export PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0
P() { python3 ../evidence/probe_selection.py; }
T() { python3 ../evidence/probe_tests.py; }
L() { python3 ../evidence/compare_legacy.py; }
H() { python3 ../evidence/probe_hint.py; }
S() { python3 ../evidence/summarize.py; }
```

P lấy nguyên khối đầu shell đến trước `# wp858`, chỉ thêm `declare -p PY` và `SELECTION_OK`;
đây là đo bộ chọn, không phải đo installer. T chạy ca thật của HEAD trên bản sao NGUYÊN shell,
fixture dùng venv thật thiếu PyYAML và installer giả. Nhãn linux/macos trong T là `CONG_CU_NEN`,
đều chạy bằng Bash Linux. Bản sao được dựng lại mỗi lần, không phụ thuộc tên `/tmp` cũ trong log.
`<san>` trong các bảng là phần đường tạm ngẫu nhiên; JSON/log giữ đường thật.

Các lượt dài chạy qua `../evidence/run_gate.py <nhãn> <cwd> <giới-hạn-giây> <lệnh...>` để ghi output,
thời lượng, timeout và mã thoát. Mọi rc dưới đây là rc TIẾN TRÌNH ĐÍCH trong JSON, không phải rc script gom log.
Launcher có thêm `--nhat-ky` để lưu từng ca; vẫn chạy trọn bộ mặc định.

## BANG NGHIEM THU

| Tiêu chí | Lệnh | Output thật | Đạt? |
|---|---|---|---|
| M1: chỉ giải tệp bằng type-P, thứ tự và args | P; T ca r886 | `order_all` chọn `<san>/all/python`; `order_python3` chọn python3; `order_py` giữ `[1]="-3"`; cùng rc0. `function_only_no_file` rc4, không gọi hàm. r886 PASS. | Đạt trên Bash Linux; py.exe/Git Bash native KHONG DO DUOC. |
| M2: đường tuyệt đối kể cả PY dùng lại | P; T ca dùng lại | `reuse_python`, `reuse_._python` rc4, stdout rỗng, một dòng stderr; `/usr/bin/python3 -I` dùng lại rc0 với PATH không Python. PATH `rel`, rỗng, `.` đều rc4. | Đạt. |
| M3: hai ca HINT và hàm echo không bị gọi | T; launcher HEAD | Cả ba PASS. Mutant gọi thừa khiến cả ba ném TinHieuChotCa `ham python ke thua da bi goi`; không dùng exception vơ càn. | Đạt; F01 đã vá thật. |
| M4: từng đột biến giết đúng ca | `python3 .claude/dev/launcher_test.py --dot-bien`; T | Native: command-v4/4; gọi thừa1/1; chỉ chốt chọn mới1/1; bỏ guard1/1. T: kết hợp command-v+bỏ guard giết3/3 ca hành vi; mỗi lỗi là assertion của chính ca. | Đạt. Biến thể kết hợp được đo riêng, không giả thành mục native thứ năm. |
| A1: launcher Linux và delta môi trường; mutation mới đúng đích | `python3 .claude/dev/launcher_test.py --nhat-ky ../evidence/launcher-head.journal`; cùng lệnh trên clone base; `--dot-bien`; L; S; H | HEAD315/328 đã chạy, tổng330, skip2, đỏ13, rc1. Base310/323, tổng325, skip2, đỏ13, rc1. Tập ca đỏ trùng ở môi trường mặc định;5 ca mới PASS. Mutation521/522,4 KHONG DO DUOC; mục sống cũ sống cả2vế. Riêng ca reuse dưới hai môi trường kế thừa mới đều0/1. | Delta0 mặc định; độ tin cậy fixture chưa đạt vì F02 P2. Không khai toàn suite xanh hoặc skip là pass. |
| A2: phản chứng spec-base086f1b7 | T | Hai HINT trên086f1b7 đều assertion đỏ: rc1, GITHUB_PATH rỗng. Đo cả base thật90c101b cùng kết quả. | Đạt. |
| A3: cong_cu không đổi; cài rg rc0 | `python3 ops/cong_cu_test.py` trên HEAD/base; `bash ops/cai_cong_cu.sh rg` trên hai vế | Cả hai60/60 ca đã chạy, tổng61, cùng skip1 INDEX. Phần bán kính490 đột biến chưa hoàn tất. Cài rg hai vế cùng rc1, `sudo: PERM_SUDOERS: setresuid(-1, 1, -1): Invalid argument`. | Nền test delta0; cả suite490 và kết quả cài rc0 KHONG DO DUOC, không gán lỗi sudo cho PR. |
| A4: Ruff delta, whitespace, doctrine, cú pháp, CI/Windows | `python3 -m ruff check --no-cache --select F --output-format json .claude/dev/launcher_test.py scripts/tl.py`; `git diff --check 90c101b8d1f8895b66607de8582a18c5e72d834c HEAD`; `python3 .claude/dev/packet_loop.py doctrine-scan --root .`; `bash -n ops/cai_cong_cu.sh`; S | Ruff17/17 cảnh báo giống nhau ở hai vế (test5F841 + tl.py12F821), delta0, rc1. Diff rc0; doctrine rc0,10 tệp/0 vi phạm; bash-n rc0. | Cục bộ đạt theo delta. CI PR, workflow_dispatch windows-only và Windows local KHONG DO DUOC: cấm mạng, không runner/receipt native trong bundle; không miễn gate đó. |

## BANG DO

Cách tìm: đọc TOÀN `diff.patch`, đối chiếu byte với `git diff BASE HEAD`, đọc nguyên
`git log --format=%B 90c101b8d1f8895b66607de8582a18c5e72d834c..HEAD` (lưu
`evidence/commit-messages.txt`), rồi đo từng khẳng định hành vi/comment bên dưới.
Không dùng tìm từ khóa làm trần phạm vi review. Các khẳng định lịch sử về nguyên phiên #832
chỉ tái hiện được cơ chế trên base/HINT; không giả đã truy cập issue hoặc log máy gốc.

| Khẳng định / nơi | Diff khai | Đo được (lệnh, cách tìm) | Khớp? |
|---|---|---|---|
| Shell21–25: command-v nhận hàm/in tên trần; type-P giải tệp | Ba nhánh type-P thay command-v | P `exported_echo_function`: `declare -F` có python, command-v in `python`, type-P/PY in `<san>/all/python`; không FUNCTION_CALLED. T: hai base đỏ. | Khớp. `type-P` không chứng thực nội dung interpreter; giới hạn ở BANG SAN. |
| Shell23–25, commit882cb50: python→python3→py -3, giữ args | Chọn thẳng đường tệp, py thêm -3 | P `order_all/order_python3/order_py`, reuse absolute; T r886 so toàn bộ tuple TEN_PYTHON. | Khớp. Native Windows chưa đo. |
| Shell28–32 / commit882cb50: PATH đổi không làm rời interpreter đã chọn, PY không tuyệt đối thoát4 kể cả lượt cha | Guard chung sau hai nhánh | P các reuse/PATH; T ba ca batch venv; ca reuse checker giả. | Khớp hành vi, kể cả args còn lại. |
| Test9641: copy bản ĐANG THỬ | CAI_SH_DANG_DUNG thay nguồn cố định | T mutant command-v làm ba ca hành vi đỏ rc4 bằng assertion, không phải import/fixture error. | Khớp. |
| Comment9790–9791, hai hàm9819/9824: nhận hai HINT #832 | Helper chung với hàm export và venv/batch | T HEAD cả hai PASS; hai base cả hai đỏ, rc1/gp rỗng; đối chiếu HINT-review-832.patch. | Khớp cơ chế; macOS là nền giả trên Linux. |
| Test9798–9815, docstring9830, commit0311db4 F01: hàm không bao giờ được gọi, ghi log mỗi lời gọi | Hàm export ghi R1078_HAM_LOG; assertion file không tồn tại; finally khôi phục seam | T HEAD3/3 PASS; `function_called_all_platform_fixtures`3/3 assertion `ham...da bi goi`; native mục gọi thừa1/1. | Khớp. Đòi file không tồn tại mạnh hơn chỉ đòi file rỗng; trong fixture file chỉ được tạo khi gọi hàm. |
| Ca9835: hình dạng chạy cả Windows, type-P và guard fail-close | Pure Python đọc/regex văn bản | T shape PASS; command-v và bỏ guard giết đúng shape. Đọc ca không gọi Bash; ba ca hàm và reuse có skip POSIX trên Windows. | Khớp tính khả chuyển cấu trúc; Windows execution KHONG DO DUOC. |
| Test9847–9867 / commit0311db4 F02: source nhánh dùng lại tên trần/tương đối phải rc4 trước checker | Marker=$$, mảng PY, checker giả SystemExit23 | T môi trường sạch PASS; native fresh-only và mutant chỉ nhận `./python` chết đúng ca. H và hai CLI env thực: HEAD có allexport/marker export đều assertion đỏ rc3, do marker bị script bỏ và chọn mới. | Phạm vi phép đo chưa kín: F02 P2. Không mở đường installer thật nhưng môi trường có thể đổi nhánh fixture. |
| Test10205–10209: r886 đọc đúng thứ tự và args | Regex mới cho type-P | T HEAD r886 PASS; nạp mã test882cb50 cùng fixture thì assertion `sh=[]`, TEN_PYTHON ba tuple đúng thứ tự. | Khớp. |
| Comment13744 và bảng13745–13759: command-v, bỏ guard, bỏ cả hai; hai mục mới F01/F02 | Native bốn mục wp1078; kết hợp là phản chứng riêng/base | T và native log bốn mục; T cả hai kết hợp3/3 đỏ. | Khớp hiệu lực M4; bảng native có4 mục, không có mục kết hợp riêng. |
| Commit882cb50: trên base90 cả4 ca đỏ, M3 có rc0 mà gp rỗng | Bằng chứng A2 lịch sử | T trên90 và086: hai HINT rc1, M3 rc0/gp rỗng, shape assertion đỏ. Blob shell hai base trùng (đo Git/hash). | Khớp lượt đo này; không nâng rc0 của hàm echo thành bất biến mọi lần chạy. |
| Commit47b873: trên882cb50 r886 đỏ, mutation chỉ giết1/4 do copy tệp thật | Sửa regex và fixture | T `history882_HEAD`: r886 TinHieuChotCa `sh=[]`; `history882_command_v`: ba hành vi PASS, shape assertion đỏ → đúng1/4. | Khớp cơ chế. |
| Commit47b873: sau đổi fixture ba ca đỏ rc4; tổng lịch sử326/327 và519/520 | Chọn đúng mutant | T command-v: ba ca rc4 với assertion của ca. Lượt hiện tại đầy đủ315/328 và521/522. | Cơ chế khớp. Hai tổng lịch sử KHONG DO DUOC trên nguyên rig cũ; không dùng khác biệt môi trường để kết tội claim lịch sử. |
| Commit0311db4: áp HINT F01/F02 của lượt1 vào TEST | Chỉ +34 dòng test so47b873a | `git diff 47b873a HEAD` khớp `diff-tu-luot1.patch`; T hai mutation mới chết đúng chốt, HEAD6/6 PASS ở môi trường sạch. H đo thêm môi trường kế thừa. | Khớp việc áp hint; không đủ để đóng F02 vì fixture sinh lỗi môi trường mới. |

## BANG TEST

| Bộ | N/M và rc thật | Bỏ qua / giới hạn |
|---|---|---|
| Launcher HEAD | 315/328 ca chạy qua; tổng330, đỏ13, rc1;427.780s, không timeout | 2 skip: t62 Windows và r484_g4 native SID. 13 ca môi trường không coi là pass. |
| Launcher base90 | 310/323 ca chạy qua; tổng325, đỏ13, rc1;414.886s, không timeout | Cùng2 skip, cùng13 ca đỏ.5 ca mới HEAD đều PASS. |
| Launcher --dot-bien HEAD | 521/522 đạt, tổng526, rc1;369.508s | 4 KHONG DO DUOC: SID2, share-delete1, t62 Windows1. SAI duy nhất `r26_rv5_codex_env_guard`. |
| Native mới wp1078 | 4/4 mục đạt,7/7 assertion đích | Không skip Linux. T xác nhận toàn bộ đều TinHieuChotCa. |
| T mục tiêu HEAD | 6/6 PASS | Ba ca hàm, shape, reuse, r886. Không cộng vào tổng launcher lần nữa. |
| T phản chứng mới/kết hợp | 7/7 native;3/3 kết hợp;3/3 gọi thừa ở ba fixture;1/1 chỉ lọt đường tương đối | Tất cả giết bằng assertion của chính ca, không ERROR/SKIP. |
| T base90/base086 | Mỗi base4/4 ca mục tiêu assertion đỏ | A2 hai HINT đều đỏ đúng lý do. Đây là chạy test mới trên shell cũ, không phải toàn suite cũ. |
| T lịch sử882 | r8861/1 đỏ; mutant chỉ1/4 đỏ | Tái hiện đúng regex cũ và fixture copy tệp thật. |
| L đối chiếu mutant cũ sống | Neutral2/2 PASS; mutant2/2 vẫn PASS (HEAD/base) | Không chạy toàn bảng mutation base; không gán sống sót này cho PR1078. |
| cong_cu HEAD/base | Mỗi bên60/60 ca đã chạy, tổng61, skip1; N126 ĐẠT ở cả2vế | Cả2bị giới hạn420s và SIGINT khi đang bán kính490: rc tiến trình=-2 (tương đương shell130), timed_out=true. Phần490 KHONG DO DUOC; không gọi cả suite xanh từ headline60/60. |
| H / CLI kiểm môi trường kế thừa | HEAD sạch1/1 PASS; allexport0/1, marker-export0/1, cả2rc1 | Lỗi assertion của ca reuse, checker giả trả về nhánh rc3; F02. |
| HINT kiểm riêng |6/6 ca mục tiêu PASS; ba môi trường outer3/3 PASS; bốn mutant cũ7/7 giết đúng ca | Bên trong ca reuse kiểm4chế độ ×2đường; mutant bỏ declare+x đỏ đúng ca tại nhãn bash-a. Patch-p0 rc0, byte-match. Không chạy toàn suite với HINT. |
| Bash syntax / whitespace / doctrine | rc0/0/0; doctrine10tệp/0vi phạm | Doctrine base cũng rc0,10/0. |
| Ruff bare lint | HEAD/base17/17 cảnh báo trùng; rc1/1; delta0 |5F841 test +12F821 tl.py. Đã dùng --no-cache. |
| Ruff pin/probe contract | `loi_ruff_ci()` → `RUFF_CONTRACT 3 []`, rc0 | Consumer hiện có, khác phạm vi bare lint. |
| Cài rg thật | HEAD/base cùng rc1; không timeout | Cùng lỗi sudo trước apt-get; rc0 KHONG DO DUOC. |
| CI / workflow_dispatch Windows / Windows local | KHONG DO DUOC | Không mạng, không native runner, không receipt làm chứng; gate tương ứng vẫn cần bên có năng lực xác minh. |

`ls -ld /tmp/.git` đã chạy trước khi kết luận. 11 ca `r484_*` bị chặn trực tiếp hoặc dây chuyền bởi
`Codex home is inside a repository`; hai ca `r858_goc_tam_tranh_to_tien_co_git` và
`t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac` gặp `/var/tmp` read-only.
S đối chiếu tên ca đỏ:13 chung,0 mới,0 mất; lý do gốc cùng điều kiện. Giữ là KHONG DO DUOC đối với
hành vi mục tiêu bị sandbox chặn. Danh sách và thông báo thật đầy đủ ở `evidence/summary.json` cùng hai log launcher.

## BANG SAN

| Hướng độc lập / lớp đường vào | Lệnh | Output thật | Kết luận |
|---|---|---|---|
| Hàm python export, chuyển interpreter khi prepend PATH | P `exported_echo_function/function_only_no_file`; T hai HINT trên HEAD và hai base | command-v=`python`, type-P=`<san>/all/python`; HEAD PASS, base HINT rc1/gp rỗng. Không file thì rc4, không FUNCTION_CALLED. | KHONG PHAI LOI còn mở. |
| Hàm echo không phải Python; gọi thừa vẫn chạy checker đúng | T `function_called_all_platform_fixtures` | HEAD3/3 PASS; mutant3/3 TinHieuChotCa `ham python ke thua da bi goi`. | KHONG PHAI LOI; F01 ĐÃ VÁ THẬT. |
| Nhánh dùng lại PY tên trần/tương đối và thuộc tính marker của fixture | P reuse; T; H; hai CLI env trong finding | Product bare/relative rc4; hai mutant chết đúng ca ở môi trường sạch. Fixture HEAD kế thừa allexport/marker export lại đỏ0/1 với product nguyên vẹn; HINT3/3 môi trường PASS. | LOI TEST P2 F02: fixture chưa cố định đúng nhánh đang đo. |
| Alias không tương tác, cả khi bật expand_aliases | P `alias_default_noninteractive/alias_enabled` | Mặc định `expand_aliases off`, type thấy file; bật thì type thấy alias, PY vẫn `<san>/all/python`, rc0, không ALIAS_CALLED. | KHONG PHAI LOI. Alias không tự export qua bash mới. |
| Builtin | P `builtin_class` | `printf is a shell builtin`; command-v=`printf`, type-P=`<san>/tools/printf`; `builtin python`, python3, py đều `not a shell builtin`; chọn file rc0. | KHONG PHAI LOI với builtin chuẩn. Builtin tự nạp tên Python KHONG DO DUOC/ngoài phạm vi. |
| py -3 / thứ tự tên trên Windows-Git Bash | P `order_all/order_python3/order_py`; T r886 | Bash Linux chọn đúng ba nhánh, py giữ `[1]="-3"`, r886 PASS. | KHONG DO DUOC py.exe/Git Bash native. Không coi symlink fixture Linux là Windows. |
| Marker/PY từ môi trường, exec giữ PID, marker thiếu/sai | P `exec_exported_marker_scalar/reuse_no_marker/reuse_wrong_pid` | Marker export+PY scalar qua exec bị loại, chọn file thật; mảng không marker hoặc sai PID không được dùng lại; cùng rc0. | KHONG PHAI LOI. |
| bash -a và SHELLOPTS=allexport | P `reuse_bash_a/reuse_SHELLOPTS/reuse_bare_bash_a/reuse_bare_SHELLOPTS`; H | Absolute array giữ args với PATH không Python, rc0; bare array có marker đã gỡ export bị chặn rc4 trong cả hai chế độ. H đo fixture mới thiếu bước gỡ export. | Product KHONG PHAI LOI; khoảng trống fixture là F02 ở hàng trên. |
| hash -p trong shell source / qua exec | P `hash_in_source/hash_not_inherited_exec` | Shell source với hash chủ động chọn `/bin/echo`, rc0; qua exec mới chọn `<san>/all/python`, rc0. | KHONG PHAI LOI trong spec: hash do caller cài chủ động ngoài phạm vi; không tuyên bố type-P chống can thiệp shell tùy ý. |
| PATH có phần tử tương đối/rỗng/. | P `path_relative/path_empty/path_dot/path_missing_relative_then_absolute` | type-P lần lượt `rel/python`, `./python`, `./python`; guard rc4 với một dòng stderr. Relative miss rồi absolute tốt thì rc0. | KHONG PHAI LOI: fail-close đúng M2, không đổi sang ưu tiên thấp hơn để lách guard. |
| BASH_ENV | P `BASH_ENV_hash/BASH_ENV_explicit_source` | Chỉ đặt env: không thấy `STARTUP_READ`, chọn file PATH rc0. Source tường minh cùng tệp: có `STARTUP_READ`, hash/type-P/PY=`/bin/echo`, rc0. | KHONG DO DUOC activation tự động BASH_ENV trong sandbox này. Startup code tùy ý ngoài spec, không tính finding; không suy lượt env không kích hoạt thành đã bảo vệ. |
| CDPATH | P `CDPATH` | rc0, chỉ declare PY và SELECTION_OK, không stdout CDPATH xen đường. | KHONG PHAI LOI; cd dùng đường tuyệt đối. |
| Tệp mang tên python nhưng thực chất echo; PY absolute do caller cấp | P `file_named_python_is_echo/absolute_nonpython_reuse` | `-c PROBE_NONPYTHON`; PY là tệp absolute mang tên python hoặc `/bin/echo -n`, selection rc0. | KHONG PHAI LOI trong spec: M1 giải tệp, M2 kiểm hình dạng đường; không có mục chứng thực nội dung binary. Thay nội dung/symlink sau chọn cũng ngoài hợp đồng này. |
| Harness hoặc môi trường tạo tín dụng giả | T phân biệt TinHieuChotCa/ERROR; L; S; `ls -ld /tmp/.git` | Các mutation mới không ERROR; mutant cũ sống ở cả2vế;13 lỗi môi trường trùng base/HEAD. | KHONG PHAI LOI mới do diff; phần bị chặn ghi KHONG DO DUOC. |

## BẢNG LỚP VÀ QUYẾT ĐỊNH FINDING

| Slug lớp nguồn | Finding / nguồn | Trạng thái trên0311db4 | Phép đóng lớp |
|---|---|---|---|
| no-function-invocation-assertion | F01 P2, lượt1/47b873a | ĐÃ VÁ THẬT;0biểu hiện mở | Nhật ký trong helper chung cho cả3ca; neutral đều PASS, gọi thừa đều chết đúng assertion. |
| reused-py-guard-unmeasured | F02 P2, lượt1/47b873a; biểu hiện từ bản sửa0311db4 | VÁ SINH LỖI MỚI;1biểu hiện mở với2đường vào môi trường | Môi trường sạch đã bắt mutant fresh-only; fixture mới vẫn thiếu cố định thuộc tính export của marker. H tái hiện2đường và kiểm hint. |

Đã quét cùng cơ chế ở fixture linux/macos, hàm echo, shape, reuse và bảng mutation.
Hai lớp nguồn đóng1/2, F02 giữ nguyên slug và có biểu hiện fixture mới; không tách slug để xóa lịch sử.
Những giới hạn ngoài spec hoặc thiếu runner không được chuyển thành finding sản phẩm.

### F02-reused-py-guard-unmeasured [P2] Fixture dùng lại PY không cố định thuộc tính export của marker

TEP/DONG: `.claude/dev/launcher_test.py:9857`, `:9860` (ca
`r1078_py_dung_lai_khong_tuyet_doi_phai_thoat_4`). Mã sản phẩm liên quan để giải thích là
`ops/cai_cong_cu.sh:19–20`, không đề nghị vá mã sản phẩm.

VAN DE: chỉ gán `CAI_CONG_CU_PY_CUA=$$` không bảo đảm marker là biến shell KHÔNG export.
Nếu môi trường cha đã export marker thì phép gán giữ thuộc tính export; nếu Bash kế thừa
`SHELLOPTS=allexport` thì chính phép gán tự export marker. `_wp802_bash_env()` không gỡ hai
đường này. Shell sản phẩm cố ý bỏ marker export ở dòng19 để tránh nhận marker từ môi trường.
Vì thế fixture chuyển sang nhánh CHỌN MỚI, thay mảng PY tên trần bằng interpreter thật;
checker giả làm `cai-lenh` thất bại và script trả3. Assertion báo không chặn PY dùng lại,
nhưng lần chạy ấy chưa hề đi qua nhánh dùng lại. Đây là khoảng trống cô lập phép đo của F02
và gây đỏ oan ở môi trường Bash được mã sản phẩm hỗ trợ. Phân loại P2 cho fixture/chốt đo;
không quy thành lỗi runtime của M2.

DA THU NGHIEM: chạy nguyên HEAD, không đột biến mã sản phẩm:

```bash
PYTHONDONTWRITEBYTECODE=1 env SHELLOPTS=allexport python3 .claude/dev/launcher_test.py \
  --lap-ca r1078_py_dung_lai_khong_tuyet_doi_phai_thoat_4 --lan 1
PYTHONDONTWRITEBYTECODE=1 env CAI_CONG_CU_PY_CUA=ambient python3 .claude/dev/launcher_test.py \
  --lap-ca r1078_py_dung_lai_khong_tuyet_doi_phai_thoat_4 --lan 1
```

Cả hai rc1, output thật: `LAP r1078_py_dung_lai_khong_tuyet_doi_phai_thoat_4: 0/1 qua, 0 bo qua, 1 hong`;
assertion `PY dung lai 'python' phai thoat 4 truoc checker: rc=3 out=''` và stderr
`cai_cong_cu: 'rg' khong co cong thuc cai tu dong cho nen nay`.
Log: `evidence/reuse-allexport.log`, `evidence/reuse-exported-marker.log`.
Đối chứng P với marker gán rồi gỡ export: absolute array được dùng lại rc0;
bare array bị chặn rc4 dưới cả bash-a lẫn SHELLOPTS. Do đó đây không phải lỗi sản phẩm.

DO TIN: cao. H chạy lại ba môi trường với HEAD: sạch PASS, hai môi trường kế thừa đều
TinHieuChotCa. HINT trên cùng shell chưa sửa: cả ba PASS, sáu ca mục tiêu6/6 PASS;
các bốn mutant wp1078 vẫn giết7/7 ca đích. Ca reuse trong HINT chủ động kiểm bốn chế độ
(thường, bash-a, SHELLOPTS, marker export), mỗi chế độ cả `python` và `./python`.

Gợi ý vá ở CHÍNH fixture ca dùng lại, ngay sau phép gán marker: gỡ thuộc tính export trước
khi source, như nhánh batch của sản phẩm đang làm ở dòng117. Mở vòng fixture để chủ động
thử cả hai nguồn kế thừa và bash-a; không thay helper môi trường chung của toàn bộ suite.
`HINT.patch` chứa đúng hướng này và chỉ sửa `.claude/dev/launcher_test.py`.

Chốt mới có phản chứng độc lập: H lấy bản test đề xuất trên bản sao, bỏ duy nhất
`declare +x CAI_CONG_CU_PY_CUA; ` khỏi chuỗi Bash của fixture. Ca dùng lại ném
TinHieuChotCa `PY dung lai 'python' (bash-a)...rc=3` sau khi lượt thường đã qua.
Đó là assertion của chính ca, không phải lỗi import/cú pháp/fixture thiếu. Phản chứng này
được đo riêng trong H, không giả là mục native đã thêm vào HEAD.

Rủi ro của hướng vá: phải gán TRƯỚC rồi gỡ export; không gán lại marker sau đó trong allexport.
Chỉ cố định marker cho fixture mô phỏng lượt source đáng tin, không nới sản phẩm để tin marker môi trường.
Giữ checker giả và finally/isolation để mutant không chạy installer thật hoặc làm nhiễu ca khác.

`HINT.patch`: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.
`patch --batch -p0 --input <HINT.patch>` đã áp thành công trên bản sao tạm ngoài kho,
rc0 và byte-match với candidate đã compile/chạy. SHA256:
`69be15d022c2c30d3c72e7da47cefe8ae03defd306a063f5464871c145a33ec8`.
Không khẳng định toàn launcher suite hoặc490đột biến đã chạy trên HINT.
Ruff bare lint trên candidate test có đúng5F841 cũ, delta0 so test HEAD (rc1), không thêm cảnh báo.

## Giới hạn gate và vệ sinh cây review

Không dùng các giới hạn sudo, /tmp/.git, /var/tmp, Windows hay CI để miễn gate hoặc tạo thêm
finding code. Review còn F02 P2 nên chưa đủ approval; hết lời gọi2/2 thì checkpoint chủ kho.
Không có hành động publish/state/merge nào được thực hiện trong lượt này.

Snapshot nội dung ban đầu có9912tệp. Sau các phép đo, xuất hiện đúng một tệp dấu do hook
`session-start.sh` tạo: `.claude/.packet_state/session-start.ran`,28byte. Đã xóa đúng hiện vật
phát sinh sau khi kiểm nó không có trong snapshot đầu và hash vẫn khớp snapshot sau;
đồng thời bỏ thư mục rỗng `.packet_state` có birth-time trùng lượt hook. Không sửa nội dung nguồn.
Có ghi tạm của hook trong lượt chạy; không khai chưa từng có ghi vào cây.
Giới hạn snapshot: chỉ chứng minh trạng thái ở hai mốc, không chứng minh toàn bộ lịch sử thao tác.
Chi tiết cleanup/snapshot được lưu trong `evidence/generated-marker-cleanup.json`,
`evidence/snapshot-final-comparison.json`; bước readback Git cuối được ghi sau khi dọn.

Readback cuối:9912/9912tệp khớp byte/hash,0added/0removed/0changed. Git status kể cả ignored,
working diff và cached diff đều0byte. HEAD/tree vẫn `0311db45d5786c3d4a1c05fec1375aec9e727249` /
`740ca2f9380fdbcffcc4d11ad03293283d576f37`. Hai tệp reviewed khớp blob HEAD:
shell `f54d486013fa8adc75cde41f4ec5abb939e66ebc`, test `65a04cac449cdab1e7c71c0acae61ba5a17e32ad`.

Nguồn kiểm tra: [selection.log](evidence/selection.log), [selection.json](evidence/selection.json),
[targets.log](evidence/targets.log), [targets.json](evidence/targets.json),
[legacy.log](evidence/legacy.log), [summary.json](evidence/summary.json),
[commit-messages.txt](evidence/commit-messages.txt), [hint-validation.log](evidence/hint-validation.log),
[hint-validation.json](evidence/hint-validation.json), các `*-head/base.log` và `*.json` tương ứng.
