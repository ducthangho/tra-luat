verdict: changes_requested
reviewed_sha: 47b873a2e977e2a9485c550d141708fd5814af96
spec_sha256: 2fb1b2633ae09e4b737f97d601186389fd801cc294a5217ea07b3e761c3bf13b
Ket qua: 0 P0, 0 P1, 2 P2, 0 P3.

PR #1097 / packet #1078, r1/g1, lease `wp1078-r1-g1-claude`, sensitive, lượt Codex 1/2.
Reviewer: Codex/OpenAI (provider openai_codex); bề mặt API có công cụ shell, transport machine/local. Không đủ chứng thực để khai codex_cli hay codex_desktop; GitHub submitter: null.
Không có công cụ chứng thực model phục vụ nên model/effort chính xác: KHONG DO DUOC.
Session review độc lập với executor Claude; không đăng verdict, push hay gọi dịch vụ mạng.
Tree: `ba8e3c2bab162ba14d950e62354c6c21794e5cb2`; base thật: `90c101b8d1f8895b66607de8582a18c5e72d834c`.
`sha256sum SPEC.md` khớp hash trên. Diff Git khớp byte với `diff.patch`, SHA256
`30dbfcbfd15cbe90995419b19734554834aef4727757fa142e55deb602bbc13e`;
numstat: test +64/-5, shell +10/-7; đúng hai tệp trong write set.

Kết luận: chưa thấy lỗi hành vi sản phẩm trong phạm vi M1–M3; yêu cầu sửa hai khoảng trống
test đo được dưới đây. Ngưỡng sensitive chưa cho phép bỏ qua P2. CI/Windows chưa xác minh vì cấm mạng.

Các lệnh dưới đây chạy từ `cay-kho/`. Ký hiệu P/T/V/L tương ứng các lệnh đầy đủ:

```bash
P() { PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/probe_selection.py; }
T() { PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/probe_tests.py; }
V() { PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/validate_hint.py; }
L() { PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/compare_legacy_mutation.py; }
```

P chép nguyên văn 32 dòng đầu của shell tại HEAD vào sân tạm, chỉ thêm in mảng PY;
không đo phần installer. T và V chạy các ca trên nguyên shell trong fixture có installer giả.
Mọi đột biến và bản sao đều nằm ngoài `cay-kho/`. Các script trong `evidence/` tái dựng được sân tạm;
đường `/tmp/...` trong log là đường của lượt đã chạy, không phải phụ thuộc cố định.

## BANG NGHIEM THU

| Tiêu chí | Lệnh | Output thật / bằng chứng | Đạt? |
|---|---|---|---|
| M1: type -P, thứ tự python/python3/py -3 | P; T | `order_python`, `order_python3`, `order_py_minus3` rc=0, mảng lần lượt chọn đúng tên; py giữ `[1]="-3"`; r886 PASS. | Đạt trên Bash Linux; py thật Windows KHONG DO DUOC. |
| M2: chặn cả PY chọn mới và dùng lại không tuyệt đối | P; V | `reuse_bare_name_rejected`, `reuse_relative_name_rejected`, PATH tương đối/rỗng đều rc=4, stdout rỗng, một dòng stderr nêu đường sai; absolute PY giữ đối số. Ca HINT dùng nguyên script cũng PASS. | Hành vi đạt; test hiện có thiếu răng cho nhánh dùng lại: F02. |
| M3: hai ca HINT + hàm không phải Python | T | HEAD cả ba ca hành vi PASS; base cả ba chết bằng TinHieuChotCa. | Ca có mặt và hành vi đạt; khẳng định “không bao giờ được gọi” chưa được test khóa: F01. |
| M4: ba phản chứng đúng ca | `python3 .claude/dev/launcher_test.py --dot-bien`; T | Hai mutation tự động `wp1078_chon_bang_command_v` giết 4/4, `wp1078_bo_chot_tuyet_doi` giết 1/1. Kết hợp command-v + bỏ guard trong T làm ca M3 chết bằng assertion, không phải exception vơ càn. | Đạt phép đo yêu cầu; biến thể kết hợp hiện chỉ có bằng chứng thủ công, không có mục riêng trong bảng tự động. |
| A1: launcher Linux, delta so base; mutation mới đúng đích | `python3 .claude/dev/launcher_test.py --nhat-ky ../evidence/launcher.journal`; `--dot-bien`; L | HEAD 312/325, tổng 329, bỏ qua 4, hỏng 13; 4 ca mới PASS. Mutation 519/520, 4 KHONG DO DUOC; 2 mutation mới đạt. L xác nhận mutation cũ thất bại như nhau trên base/HEAD. Đối chiếu base: 302/315, tổng 325, bỏ qua 10, hỏng 13, rc1. | Không khai toàn bộ xanh; KNDO do sandbox ở các ca liệt kê dưới. |
| A2: phản chứng trên base đặc tả 086f1b7 | T | Hai ca HINT đều TinHieuChotCa: rc=1, GITHUB_PATH rỗng. Đo cả base thật 90c101b cũng cùng kết quả. | Đạt; không nhầm số dòng/spec-base với base thật. |
| A3: cong_cu_test không đổi; cài rg rc=0 | `python3 ops/cong_cu_test.py`; `bash ops/cai_cong_cu.sh rg` | HEAD và base đều 60/60 ca đã chạy (tổng 61, cùng bỏ qua 1 ca INDEX), tự kiểm song song N126 ĐẠT; phần 490 đột biến bị dừng bằng Ctrl-C, tool rc130, KHONG DO DUOC kết quả toàn suite. Lệnh rg thực tế rc=1: `sudo: PERM_SUDOERS: setresuid(-1, 1, -1): Invalid argument`; chưa đến apt-get. | rg rc=0 KHONG DO DUOC do sudo của sandbox; không tính regression PR. |
| A4: Ruff delta0, diff, doctrine, cú pháp, CI và Windows | `python3 -m ruff check --no-cache --select F .claude/dev/launcher_test.py scripts/tl.py`; `git diff --check BASE HEAD`; `python3 .claude/dev/packet_loop.py doctrine-scan --root .`; `bash -n ops/cai_cong_cu.sh` | Ruff hai vế cùng 5 F841 ở test +12 F821 ở tl.py, delta0; diff rc0; doctrine rc0, 10 tệp, 0 vi phạm; bash-n rc0. | Gate cục bộ đạt theo delta; CI PR và workflow_dispatch windows-only KHONG DO DUOC: không mạng, không runner Windows/receipt đi kèm. |

## BANG DO

| Khẳng định / nơi khai | Diff khai | Đo được, lệnh và cách tìm | Khớp? |
|---|---|---|---|
| Shell 21–25: command-v nhận hàm, type-P chọn tệp | Bỏ chọn/ghim command-v, dùng ba type-P | P exported_function; T trên hai base. Hàm echo không xuất hiện ở output của bộ chọn; chọn file đúng. | Khớp trong shell sạch; xem giới hạn hash/BASH_ENV ở BANG SAN. |
| M1 / commit 882cb50: thứ tự và -3 | python → python3 → py -3 | P ba cấu hình chỉ có các tên tương ứng; T r886 so tuple TEN_PYTHON. | Khớp. |
| Shell 29–32 / commit: không tuyệt đối dừng4, cả lượt cha | Guard sau cả hai nhánh | P đường trần, tương đối, reuse, absolute, exec và allexport; V ca reuse nguyên script. | Hành vi khớp; độ mạnh test bị khai rộng: F02. |
| Comment test 9641: fixture dùng bản đang thử | CAI_SH_DANG_DUNG thay tệp thật | T command_v làm cả ba ca hành vi chết rc4 bằng TinHieuChotCa; không dùng lỗi import/fixture. | Khớp. |
| Test helper 9790–9827 / M3: hai HINT và hàm echo | Có ba ca, venv thiếu yaml, batch giữ interpreter | T HEAD ba PASS; hai base đỏ, Linux/macOS là CONG_CU_NEN giả với Bash Linux. | Khớp phần chống đổi interpreter; không phải đo macOS thật. |
| Docstring 9826: hàm “không bao giờ được gọi” | Dựa vào rc/DAT/GITHUB_PATH | T `function_called_once`: 5/5 ca đích vẫn PASS; V thêm nhật ký thì ca M3 TinHieuChotCa “ham python ke thua da bi goi”. | Khai rộng hơn phép đo: F01 P2, không phải lỗi sản phẩm hiện tại. |
| Ca hình dạng 9831: chạy cả Windows | Pure Python đọc văn bản và regex | T shape PASS; code không gọi Bash trong ca này; ba ca hành vi có nhánh skip Windows. | Khớp tính khả chuyển của cấu trúc; thực thi Windows KHONG DO DUOC. |
| r886 10175–10184 | Parser mới đọc thứ tự + args của type-P | T HEAD PASS; bản test 882cb50 TinHieuChotCa, `sh=[]`; khai báo TEN_PYTHON giữ đúng thứ tự và -3. | Khớp. |
| Bảng mutation 13716: command-v / bỏ guard / “bỏ cả hai” | Comment nêu ba, bảng có hai mục wp1078 | T chạy cả kết hợp; native log hai mục giết đúng4/4 và1/1. | Hiệu lực ba phép đo khớp; tự động hóa chỉ có hai, không đọc comment thành ba mục tự động. |
| Commit 882cb50: A2 cả4 ca đỏ, M3 có rc0 nhưng gp rỗng | Base90 với hàm echo vẫn có thể xanh rc | T shape +3 hành vi đỏ; base-m3-repeat.log: 20/20 assertion đỏ, 18 lượt rc0 và2 lượt rc127; gp luôn rỗng. Blob shell của hai base giống nhau, SHA256 16b43f985ba5c22e5ad1cd938e5ef9f8f4236f72963a0ca854b8b1b4b42709ad. | Đo được rc0 như claim; rc không tất định. Không quy kết lần thấy127 là claim lịch sử sai. |
| Commit47b873: trên882cb50 r886 đỏ do regex | Historical regex chỉ đọc command-v | `history-targets.log`; T old_test_882cb50: TinHieuChotCa `TEN_PYTHON lech... sh=[]`. | Khớp cơ chế. |
| Commit47b873: mutation cũ chỉ giết1/4 do copy file thật | Ba ca hành vi không đọc mutant | Chạy code test từ882cb50, __file__ neo cùng checkout để giữ fixture; history-targets.log: 3 PASS, shape TinHieuChotCa. | Khớp1/4. |
| Commit47b873: sửa fixture làm ba ca hành vi đỏ rc4 | Assertion đúng ca | T command_v: Linux/macOS/M3 đều TinHieuChotCa, rc4, lỗi PY[0] tên trần. | Khớp. |
| Commit47b873: số tổng lịch sử326/327 và519/520 | Kết quả một lượt trước | Cơ chế r886 và1/4 đã tái lập. Tổng lịch sử không thể xác nhận đúng nguyên rig vì sandbox có13 lỗi và nhiều skip; không dùng số519/520 hiện tại làm bằng chứng cùng nguyên nhân. | Tổng số lịch sử KHONG DO DUOC; không tuyên bố sai từ rig khác. |

Nguồn đo: [selection.log](evidence/selection.log), [target-tests.log](evidence/target-tests.log),
[history-targets.log](evidence/history-targets.log), [commit-messages.txt](evidence/commit-messages.txt),
[base-m3-repeat.log](evidence/base-m3-repeat.log), [hint-validation.log](evidence/hint-validation.log).
`git log --format=%B BASE..HEAD` được lưu nguyên; hai commit là882cb50 và47b873a.
Các phát biểu nguồn #832 mang tính lịch sử chỉ được kiểm phần cơ chế tái hiện bằng base/HINT;
không truy cập issue hay giả nhận đã đo lại nguyên phiên #832.

## BANG TEST

| Bộ | N/M và rc thật | Bỏ qua / chưa đo |
|---|---|---|
| Launcher HEAD | 312/325 đã chạy, tổng329;13 lỗi, rc1 | 4 skip: t62 Windows; r484_g4 SID Windows; hai r348 thiếu venv/pip. |
| Launcher base90 | base 302/315, tổng 325, bỏ qua 10, hỏng 13, rc1 | So tên ca và lý do trong base-launcher.journal/log; không coi lỗi môi trường là pass. |
| Launcher mutation HEAD | 519/520 đạt, tổng524; rc1 | 4 không đo: SID Windows hai ca, share-delete Windows một ca, t62 một ca; duy nhất SAI là r26_rv5_codex_env_guard. |
| Delta mutation cũ L | 1/1 đối chiếu cùng kết quả base/HEAD | Ca r925 PASS trên mutant ở cả hai, nên không phải regression #1078; chưa chạy toàn bảng mutation base. |
| Mutation mới native | 2/2 mục đạt;5/5 assertion đích | Không có skip cho hai mục wp1078 ở Linux. |
| T chọn mục tiêu | HEAD5/5 PASS; base5/5 assertion đỏ mỗi base; command-v5/5 đỏ; bỏ guard shape1/1 đỏ | Đây là ca chọn lọc; không cộng vào số toàn suite. |
| V test hint | HEAD6/6 PASS; mutation cũ5/5 + mutation bổ sung2/2 giết đúng assertion; rc0 | Chỉ trên bản sao tạm; chưa chạy toàn suite với hint. |
| cong_cu HEAD/base | HEAD và base đều 60/60 ca đã chạy (tổng 61, cùng bỏ qua 1 ca INDEX), tự kiểm song song N126 ĐẠT; phần 490 đột biến bị dừng bằng Ctrl-C, tool rc130, KHONG DO DUOC kết quả toàn suite | Phần 490 mutation KHONG DO DUOC; không suy initial 60/60 thành pass của cả suite. Xem cong-cu-interruption.json. |
| Cú pháp/diff/doctrine | rc0/0/0 | Doctrine base cũng rc0,10 tệp,0 vi phạm. |
| Ruff delta | 17/17 cảnh báo trùng base/HEAD; rc1 hai vế | Delta0, không phải tuyệt đối0. Version thực tế0.17.1. |
| Cài rg thực tế | rc1, stderr sudo Invalid argument | Không có bằng chứng rc0; không chạy lại installer để thử mạng. |

`/tmp/.git` tồn tại và read-only, đã đo bằng `ls -d /tmp/.git`.
11 lỗi r484_* bị chặn trực tiếp hoặc dây chuyền bởi “Codex home is inside a repository”.
Hai lỗi r858_goc_tam.../t86 là `/var/tmp` read-only. Đều ghi KHONG DO DUOC đối với hành vi đích,
không tính thành finding của PR. Đối chiếu tên ca: đúng cùng 13 lỗi ở base và HEAD, không có ca cũ mới hỏng. Sáu ca r345/r347 được đo ở HEAD nhưng base bỏ qua vì venv/pip; không tính các skip đó là pass. Bốn ca mới đều qua; chi tiết trong evidence/launcher-comparison.json.

## BANG SAN

| Hướng độc lập | Lệnh đã chạy | Output thật | Kết luận |
|---|---|---|---|
| Hàm python export chuyển interpreter | T: hai ca r831; P exported_function | HEAD PASS; hai base rc1, gp rỗng, assertion đỏ; P chọn tệp tuyệt đối. | KHONG PHAI LOI còn mở trong mã HEAD. |
| Hàm echo không phải Python, kiểm không bị gọi | T function_called_once; V | Test hiện tại5/5 PASS; ca hint đỏ “ham python ke thua da bi goi”. | LOI test P2 F01. |
| Nhánh PY array dùng lại | P reuse; T guard_only_fresh; V | HEAD bare/relative rc4, stderr1 dòng; mutant vẫn5/5 PASS với test hiện tại; ca hint rc3 nên assertion đỏ đúng lý do. | LOI test P2 F02; hành vi HEAD đúng. |
| Alias trong shell không tương tác | P alias_inactive_noninteractive/alias_active_via_shell_option | `expand_aliases off`; bật tùy chọn thì type thấy alias nhưng type-P/PY vẫn trỏ tệp. | KHONG PHAI LOI. Alias không tự export qua bash mới. |
| Builtin | P builtin_class | `printf is a shell builtin`; command-v ra printf, type-P ra `<san>/all/printf`; `builtin python: not a shell builtin`. | KHONG PHAI LOI với builtin chuẩn; builtin tự nạp tên python KHONG DO DUOC, ngoài spec. |
| Windows py -3 | P order_py_minus3; T r886 | Bash Linux giữ `[0]=.../py [1]=-3`, thứ tự tuple đúng. | KHONG DO DUOC py.exe/Git Bash thật: không runner Windows; không giả native. |
| Exec giữ PID, marker export, PY scalar môi trường | P exported_marker_and_scalar_exec | exec với marker=$$ và PY=not_python vẫn chọn python thật, rc0; mảng PY mới. | KHONG PHAI LOI. |
| bash -a và SHELLOPTS=allexport | P reuse_allexport/reuse_SHELLOPTS; native r831 | Mảng absolute dùng lại rc0 dù PATH không có Python; không mất marker sau gỡ export. | KHONG PHAI LOI. |
| hash -p | P hash_source/hash_not_inherited_exec | source có hash thủ công chọn `/bin/echo` dù ngoài PATH; exec mới bỏ hash và chọn `<san>/all/python`. | Ngoài phạm vi: shell source bị cài hash từ trước; không tính finding. type-P không phải chứng thực interpreter. |
| PATH tương đối / phần tử rỗng | P relative_path_found/empty_path_found | type-P trả `rel/python` hoặc `./python`; HEAD rc4 và nêu đúng đường. Relative miss rồi absolute tốt vẫn rc0. | KHONG PHAI LOI, fail-close đúng M2; không tự đổi sang Python ưu tiên thấp hơn. |
| BASH_ENV | P BASH_ENV_alias/BASH_ENV_hash | Alias benign không thay chọn; initializer cài hash thì chọn `/bin/echo`, rc0. | Ngoài spec với startup code tùy ý; test hàm hiện gỡ BASH_ENV, không có claim bảo vệ mã khởi động tùy ý. |
| CDPATH | P CDPATH | rc0, chỉ declare PY + SELECTION_OK, không có stdout CDPATH chen vào đường. | KHONG PHAI LOI: cd bằng đường tuyệt đối. |
| Tên tuyệt đối nhưng file không phải Python / PATH thay file | P hash_source; rà M1/M2 | Đường absolute `/bin/echo` qua guard; spec chỉ yêu cầu chọn và chặn hình dạng. | Không suy M1/M2 thành kiểm nội dung binary hoặc chống thay file sau khi chọn; ngoài spec. |
| Lỗi môi trường và sống sót mutation cũ | Launcher head/base; L; `ls -d /tmp/.git` |13 lỗi môi trường ở HEAD; legacy mutant sống cả base vàHEAD. | KHONG DO DUOC hành vi bị chặn; không gán thành bug mới. |

### F01-no-function-invocation-assertion [P2] Ca M3 chưa đo “hàm không bao giờ được gọi”

TEP/DONG: `.claude/dev/launcher_test.py:9800`,`:9806–9809`,`:9825–9827`.

VAN DE: hàm echo được dựng nhưng assertion chỉ xét rc0, chữ DAT và GITHUB_PATH.
Một lần gọi hàm thừa trước khi chạy checker bằng interpreter đúng vẫn lọt; vì vậy tên/docstring M3
khai mạnh hơn phép đo. Đây là khoảng trống test, không khẳng định shell HEAD đang gọi sai hàm.

DA THU NGHIEM: T thêm một lần gọi hàm có sẵn sau `unset _PY_TEP` trên bản sao;
5/5 ca mục tiêu hiện tại xanh, bao gồm ca M3. V trên HEAD6/6 xanh; cùng đột biến làm ca M3 chết
bằng TinHieuChotCa `linux: ham python ke thua da bi goi`. Không tính lỗi cú pháp/import/timeout là giết.

DO TIN: cao; bằng chứng JSON và log lưu đầy đủ. Vá ở helper test `_r1078_python_ham_ke_thua`, nơi
dựng hàm và còn giữ kết quả cuối, bằng nhật ký riêng trong San và assertion không có lần gọi.
Thêm mutation gọi thừa để buộc assertion ấy đỏ. `HINT.patch` chứa đúng test và mutation này.
Rủi ro: nhật ký phải theo từng San, tên biến riêng và khôi phục monkeypatch trong finally để không nhiễu ca khác.

### F02-reused-py-guard-unmeasured [P2] Chốt M2 ở nhánh dùng lại chưa có ca hành vi khóa

TEP/DONG: `.claude/dev/launcher_test.py:9831–9839`; `ops/cai_cong_cu.sh:20`,`:32` là hành vi cần khóa.

VAN DE: regex chỉ chứng minh văn bản guard có mặt, không chứng minh lượt dùng lại đi qua nó.
Bọc guard để chỉ chạy khi chọn mới vẫn giữ nguyên regex; ba ca hàm đều tạo lượt cha với PY tuyệt đối,
nên không đo được thiếu chốt trên PY dùng lại là tên trần. M2 ghi rõ “kể cả nhánh dùng lại”.

DA THU NGHIEM: T `guard_only_fresh` sống5/5 ca đích hiện có. P đo HEAD dùng lại `python`/`./python`
thoát4 đúng. V bổ sung ca source nguyên shell, marker=$$, PY array tên trần/tương đối, checker giả để
không chạm installer: HEAD PASS; cùng mutant cho rc3 thay vì4 và chết bằng TinHieuChotCa của chính ca.

DO TIN: cao. Vá ở test riêng kiểm source với PY không tuyệt đối và marker đúng shell; đòi rc4,
stdout rỗng và một dòng stderr trước checker. Thêm mutation chỉ chốt nhánh chọn mới;
`HINT.patch` có test + mutation. Mã sản phẩm hiện đạt M2 qua phép đo độc lập.
Rủi ro: test mới cần sandbox riêng và checker giả để mutant không chạy cài đặt thật; shell POSIX bỏ qua trên Windows,
còn ca hình dạng vẫn giữ cho Windows. Không chuyển failure của checker thành tín dụng giết mutation.

`HINT.patch`: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.
Chỉ có `.claude/dev/launcher_test.py`; `patch -p0` áp thành công trong `evidence/hint-apply/`,
byte-match với bản hint đã compile. Không viết patch sửa mã sản phẩm/gate của packet sensitive.

Ghi chú vệ sinh: Ruff ban đầu đã sinh cache mặc định trong `cay-kho/.ruff_cache`; đã xóa đúng4 tệp cache
do lượt này tạo cùng thư mục rỗng, và dùng --no-cache cho các lần sau. Có lần ghi cache ngoài dự định;
không khai tuyệt đối chưa từng ghi tạm vào cây. Không sửa nội dung tệp nguồn. Readback cuối: HEAD/tree không đổi, git diff --exit-code rc0 và status rỗng; hai blob nguồn khớp HEAD: shell f54d486013fa8adc75cde41f4ec5abb939e66ebc, test 1e3fdc097722e5541b39fdf0aaea20e94e197b56. Không còn Ruff cache hay pyc trong cây review.

Môi trường đo: Linux x86_64; GNU Bash 5.2.21; Python 3.13.16; Ruff 0.17.1. Các lệnh Python chính đặt PYTHONDONTWRITEBYTECODE=1, kiểm Git đặt GIT_OPTIONAL_LOCKS=0.
