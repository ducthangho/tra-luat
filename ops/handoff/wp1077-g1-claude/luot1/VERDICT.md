verdict: changes_requested
reviewed_sha: e61def425e0656be4fd75a5fa5410972638ad395
spec_sha256: eabbb725650addad531429d48801667f2ef05a6090c00123d1d4146c7b89c3f3
Ket qua: 0 P0, 2 P1, 1 P2, 0 P3.

Review PR #1080, packet #1077 r1/g1, sensitive, lượt Codex 1/2. Helper thực hiện đúng hợp đồng `/bin/sh` hẹp của M1 và sửa được phản chứng POSIX ban đầu. Chưa approve vì còn probe khả dụng trong phạm vi doctor mắc cùng lỗi ENOEXEC, lời khai về bash sai đo được, và test mới chưa khóa việc giữ đối số.

Base: `086f1b7343fc1d778e50797e6c9ca0964b11a755`. Tree HEAD: `6b19ee1da02f3a32a3c44a8db2763eccf3ae1042`. HEAD checkout dạng detached; diff Git khớp byte với `diff.patch`, numstat đúng 22/2 và 79/0, chỉ hai tệp đã nêu. Không sửa `cay-kho/`: so hash trước/sau của 9.125 tệp được Git theo dõi, không đổi; `git status --short` rỗng. Bản sao base, mutant và thử hint nằm ngoài cây review.

Danh tính theo metadata chạy cục bộ `runs/0957f9a3/run.json`: provider `openai_codex`, execution_surface `codex_cli`, transport `machine`, run_id `0957f9a38dd54e86a0942c39f248c030`. Reviewer là Codex, độc lập với context executor Claude theo phân công; không suy model tác giả từ Co-Authored-By hoặc Claude-Session. Không đăng GitHub, không push/fetch, không dùng credential thật. Các phép đo bổ sung dùng công cụ giả và stub offline; không kiểm sống agent/API thật. Tool environment_status của skill runtime không có trong danh sách callable; môi trường thực tế được đo bằng các lệnh cục bộ.

Môi trường: Linux x86_64, Python 3.13.16, bash 5.2.21, glibc 2.39, uid=0, `/bin/sh -> dash`; `/tmp/.git` tồn tại. Windows native, CI remote, và bash/libc thật khi `/bin/sh` vắng mặt được ghi riêng là KHÔNG ĐO ĐƯỢC.

## LENH TAI LAP

Các lệnh dưới chạy khi đứng trong `cay-kho/`, đọc mã HEAD đã neo. Script review và output được giữ tại `../evidence/`.

```sh
# S: shell thật, libc execvp thật, hai probe, và doctor với PATH fixture
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/semantics.py
# P: guard/kwargs/timeout, mutant bổ sung, mutant chính thức và phản chứng base
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/probes_mutants.py
# F: ca phản chứng finding, sửa chẩn đoán và mutant trên bản sao tạm
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/finding_cases.py
# I: kiểm kê AST toàn tệp, không chỉ tìm tên hai hàm trong diff
python3 ../evidence/coverage.py
# X: các probe khả dụng còn lại với CLI giả, mọi REST/MCP remote được stub
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/extra_paths.py
# C: SHA/hash, kết quả suite/base, lịch sử 2bcd8f3 và Windows skip mô phỏng
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/final_checks.py
```

Bộ đầy đủ thực sự đã chạy bằng `python3 .claude/dev/launcher_test.py` và `python3 .claude/dev/launcher_test.py --dot-bien`, qua wrapper `evidence/run_suite.py` đặt cwd, môi trường không mang credential và lưu mã thoát. Lệnh từ thư mục chứa verdict:

```sh
python3 evidence/run_suite.py head cay-kho
python3 evidence/run_suite.py mutation cay-kho --dot-bien
# Bản base tạo bằng git archive, không checkout/sửa cây đang review:
mkdir -p /tmp/review1077-base
git -C cay-kho archive 086f1b7343fc1d778e50797e6c9ca0964b11a755 | tar -x -C /tmp/review1077-base
python3 evidence/run_suite.py base /tmp/review1077-base
```

## BANG NGHIEM THU

| Tiêu chí | Lệnh | Output thật | Đạt? |
|---|---|---|---|
| M1: chỉ ENOEXEC/POSIX/có sh mới retry; đúng một lần; giữ argv, env, stdin, timeout, encoding; lỗi/rc/rỗng phân loại như cũ | P; S | 8 ca kiểm bổ sung xanh; 12/12 mutant chết bởi TinHieuChotCa. PermissionError giữ nguyên; lỗi lần hai không tạo spawn thứ ba; retry timeout mang cờ True; empty/rc1 đều False | ĐẠT hợp đồng `/bin/sh`; native Windows chỉ mô phỏng. Khẳng định tương đương bash không đạt, xem F2 |
| M2: `_phien_ban` và `_xac_thuc_kem_dau_ra` cùng dùng helper | I; P | AST :2962 và :3014 đều gọi helper; mutant bỏ helper ở auth chết đúng ca (d) | ĐẠT hai điểm nối được yêu cầu; lời khai “hai đường probe của doctor” không đầy đủ, xem F1 |
| M3(a–d) | F; P | 4/4 ca r1077 gốc xanh trên HEAD; (a) chạy cả rg/git, (b) hỏng vẫn BI_CHE, (c) thiếu x vẫn hỏng, (d) auth không shebang xanh | ĐẠT bốn ca đặc tả; thiếu chốt argv của M1, F3 |
| M4 | `python3 .claude/dev/launcher_test.py --dot-bien`; P | Bốn mutant wp1077 OK; lần lượt 2/2, 1/1, 1/1, 1/1 ca đích chết. Replay nghiêm ngặt xác nhận cả 5 cặp đều chết bởi chính `bang(...)`, không phải lỗi vô can | ĐẠT |
| A1 | Hai suite HEAD/base và suite đột biến; C | HEAD rc1: 295/308, tổng318, bỏ10, hỏng13. Base rc1: 291/304, tổng314, bỏ10, hỏng13. Tập tên lỗi và bỏ qua giống hệt; delta lỗi cũ=0; thêm4 ca đều qua. Mutation rc0:506/506, không đo4 | ĐẠT delta hồi quy và mutant mới; 13 ca môi trường và 8 ca cần venv/pip KHÔNG ĐO ĐƯỢC, không nhận là suite xanh trọn vẹn |
| A2 | P, chạy ca HEAD với launcher base | Ca (a): TinHieuChotCa, doctor rc12 BI_CHE; ca (d): TinHieuChotCa, ok=False/OSError. S còn đo riêng git để tránh vòng lặp (a) dừng sớm ở rg | ĐẠT |
| A3 | S, `doctor_rg` và `doctor_git` | Cùng PATH fixture không shebang đầu/bản tốt sau: base rc12 BI_CHE; HEAD rc0, co=true, chọn wrapper đầu, không bi_che | ĐẠT tái hiện có kiểm soát qua lenh_doctor; không gọi toàn bộ năng lực remote thật |
| A4 | `ruff check --select F --output-format json --no-cache .claude/dev/launcher.py .claude/dev/launcher_test.py` trên HEAD/base; `git diff --check BASE HEAD`; `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | Ruff0.16.8: cả hai rc1 với cùng5 F841 cũ, delta0; diff-check rc0; doctrine rc0, quét10 tệp,0 vi phạm. Không có receipt CI exact-head trong dữ liệu cục bộ | ĐẠT ba phép đo cục bộ; CI trên head cuối KHÔNG ĐO ĐƯỢC do offline, không suy là pass hoặc chưa chạy |

## BANG DO

Cách lập danh sách khẳng định: đọc toàn bộ `git diff BASE HEAD` (kể cả comment/docstring/test/DOT_BIEN), đọc `git log -1 --format=%B HEAD` lưu ở `evidence/commit-message.txt`, lập nhóm mệnh đề hành vi/định lượng, rồi kiểm kê AST toàn launcher và truy ngược CONG_CU/KHA_NANG/delegation. Không giả định danh sách tự đọc trong diff là đầy đủ. Danh sách nguồn gọi thô ở `evidence/inventory.log`, phép đo ở các JSON/log cùng tên script.

| Khẳng định | Diff/commit khai | Đo được (lệnh) | Khớp? |
|---|---|---|---|
| Wrapper thực thi không shebang gây ENOEXEC ở bản cũ | Docstring :2924–2927; commit đoạn đầu | C trích Git object master2bcd8f3: rg/git `_phien_ban` False, Errno8; S đo base doctor rc12 BI_CHE | Có đối với fixture POSIX đã nêu |
| Bash và glibc execvp cùng chạy lại bằng `/bin/sh` | :2925; test comment :9237; commit “nhu bash/execvp” | S: bashism bash rc0/in version; libc execvp thật rc127; helper rc127; doctor rc12 BI_CHE. `/bin/sh` là dash | KHÔNG, F2 |
| Helper chỉ thêm nhánh ENOEXEC | :2934–2938, commit gạch1 | P: EACCES không retry/giữ cùng exception; isfile=False và os.name=nt chỉ gọi1 lần | Có; hai guard cuối được đo bằng mock |
| Chạy lại đúng một lần | Docstring/commit gạch1 | P: lần1 ENOEXEC, lần2 OSError; đúng2 spawn và giữ lỗi lần2; mutant spawn lần3 chết đúng assertion | Có, tính theo mỗi lần gọi helper, không nhầm với retry timeout có sẵn của doctor |
| Cùng env/stdin/timeout/mã hóa và đối số | Hai caller truyền cùng kwargs qua helper; M1 | P: so argv/kwargs và danh tính env; S: `$0`, argc2, `--version`, `two words`, env=from-env khớp bash/libc/helper | Có về code; test PR chưa khóa đối số, F3 |
| Kết quả retry được phân loại như lượt thường | :2929–2930; commit gạch1 | S empty: rc0 nhưng cả hai probe False; exit1: rc1/cả hai False; P mutant ép rc0 chết đúng ca (b) | Có |
| Hai đường probe của doctor là version/auth chung | Comment M2, commit gạch2 | I liệt kê thêm `_do_codex`, `_do_openai_llm`, `_do_github`, MCP và delegate live; F/X tái hiện lỗi ở các nhánh này | KHÔNG nếu hiểu là liệt kê đủ doctor, F1; đúng việc nối hai hàm được nêu |
| `_wp1077_tep` tạo tệp executable mặc định, mode có thể đổi | Test helper :9238–9242 | S/F tạo tệp thật, chạy thật; no_x=0644 cho errno13 khi uid0 | Có |
| Fixture doctor đặt wrapper đầu PATH và bản có shebang sau | :9245–9253 | S JSON ghi hai đường dẫn và bản được chọn trên base/HEAD, cả rg/git | Có |
| M3(a): rg/git không BI_CHE và nhận version wrapper | :9257–9265 | 4/4 ca mới qua; S từng công cụ rc0, co=true, phien_ban có no-shebang, không bi_che | Có cho script POSIX fixture, không chứng minh mọi script bash |
| M3(b): wrapper exit1 vẫn BI_CHE/12 | :9269–9275 | Ca gốc xanh; mutant bỏ qua rc chết TinHieuChotCa tại chính ca này; S exit1 hỏng | Có |
| M3(c): thiếu x không được retry, kể cả root | :9279–9288 | S: uid0, mode0644, errno13; version False/qua_han=False; mutant mọi OSError chết đúng ca (c) | Có |
| M3(d): auth không shebang có output/rc0 thì ok | :9292–9301 | HEAD ca (d) qua; base đỏ OSError; mutant bỏ helper auth chết đúng assertion | Có |
| Windows: bốn ca trả BO QUA shell POSIX | Bốn nhánh LA_WINDOWS | C mô phỏng LA_WINDOWS=True: 4 chuỗi đúng; P mô phỏng nt không fallback | Có ở mức logic; CreateProcessW/native Windows KHÔNG ĐO ĐƯỢC và ngoài phạm vi |
| 4 ca mới và4 mutant mới, đúng đích | Commit gạch3, DOT_BIEN | AST/harness đếm4/4; mutation log 4 OK; replay5/5 cặp mutant-ca là TinHieuChotCa | Có |
| launcher_test316/316, bỏ2 Windows; mutation506/506, không đo4 | Commit “Do:” | Suite ở đây 295/308, bỏ10/hỏng13; base291/304, cùng tập lỗi/bỏ; mutation506/506, không đo4 | Mutation khớp; headline316 không tái lập trên sandbox này, KHÔNG coi khác môi trường là lời khai sai/hồi quy |
| Base(a),(d) đỏ; doctor base12/head0; Ruff F delta0 | Commit “Do:” | P/S/C: đúng; ruff JSON5F841 cả hai, delta rỗng | Có trong điều kiện fixture đã công bố |
| Nguồn review #823 F1 và identity Co-Authored-By/Claude-Session | Docstring, commit metadata | Object2bcd8f3 có và lỗi tái lập. Đường artifact review-doc-lap-a-5c6c7a8 nêu trong SPEC không có trong checkout; metadata Git không chứng minh model/session thực phục vụ | Lỗi lịch sử đã đo; phần provenance/model không xác minh độc lập được, không dùng nâng assurance |

## KIEM KE TOAN BO DUONG PROBE

Lệnh I xuất mọi `subprocess.run`/`Popen`, các wrapper và call-site vào `evidence/inventory.log`/`.json`; sau đó đọc dispatcher, bảng CONG_CU/KHA_NANG và delegate. Phân biệt phép đo công cụ với lời gọi nghiệp vụ/process-control để không đưa ngoài phạm vi thành finding.

| Đường | Spawn thực tế / vị trí | Trạng thái phạm vi |
|---|---|---|
| Mọi mục CONG_CU: git, python3/python/py, claude, codex, rg, bash, gh, npm, node, llm, agy, actionlint, shellcheck | lenh_doctor:5023/version và :5040/retry → `_phien_ban`:2962 → helper | Đã sửa; `_AP_DUNG_BI_CHE` vẫn chỉ rg/git |
| Auth trong CONG_CU: claude auth status; agy models | :5074 và :5085 → `_xac_thuc_kem_dau_ra`:3014 → helper; cache `_XAC_THUC_DA_DO` | Đã sửa |
| `_xac_thuc` convenience API | :2983 → `_xac_thuc_kem_dau_ra` | Đã hưởng helper; doctor không gọi wrapper này trực tiếp |
| Khả dụng Antigravity | :4080/models qua auth helper hoặc cache; :4098/version qua helper | Đã sửa; X: không shebang vẫn DUNG_DUOC với output model giả |
| Khả dụng Codex | `_do_codex`:3909 chạy `[duong_codex,login,status]` bằng subprocess.run thô | Bỏ sót trong doctor, F1; version xanh/status OSError |
| Codex kiểm sống | :3962/:3970 → `_do_codex_song`:3831 → `codex_cred.py::_kiem_song`:197 chạy đường dẫn codex exec thô | Vẫn thiếu fallback ở delegate. Chỉ kiểm bằng fixture/mô tả call graph; không gọi API hay dùng credential thật. Không bị mục “Ngoài phạm vi” loại khỏi doctor |
| Khả dụng OpenAI llm | :4015/version, :4023/keys list, :4037/prompt → `_chay_van_ban_an_toan`:319 → subprocess.run thô | Bỏ sót cùng lớp F1; X: version ném errno8 trước khi phân loại, doctor bắt thành KHONG_DO_DUOC. Không đề nghị đổi utility chung mù vì utility còn dùng cho run |
| Khả dụng GitHub qua git | :4538/ls-remote, :4574/remote get-url → `_git`:286, spawn thô | Bỏ sót cùng lớp F1; X dùng git giả chỉ in output, không thực ls-remote mạng |
| Khả dụng GitHub qua gh | :4546/auth status, :4607/api → subprocess.run thô; tên trần được OS phân giải PATH | Bỏ sót cùng lớp F1; X dùng gh giả, mọi REST được stub |
| Trạng thái MCP GitHub phía Claude | :4348/claude mcp get → subprocess.run thô | Cùng thiếu fallback; X: khong_do_duoc/OSError ↔ khoe khi thêm shebang. Trạng thái này chỉ chẩn đoán MCP, không tự cấp DUNG_DUOC cho GitHub |
| Kiểm launcher/hook cũ trong doctor | :4783 và :4735 git show → `_git`:286 | Cùng spawn git thô; phép kiểm doctor về launcher cần xem cùng F1. Không gom việc thực thi hook phiên vào phạm vi vá |
| Các nhánh doctor không spawn công cụ | `_do_claude`: which + tệp/biến; `_do_hook_da_chay`: đọc marker; module Python/find_spec; UTF8/path; REST/MCP HTTP | Không có chỗ subprocess để thay; phép remote thật không chạy |
| `_probe_spawn`, `_chay_json_chat_che`, `_git` dùng cho check/run, Popen child trong lenh_run | :1144 → :319; :333; :1228/:1248/:1348; :2299 | run và lời gọi nghiệp vụ, không phải probe doctor trong phạm vi; ghi nhận, KHÔNG tính finding riêng |
| ps/taskkill | :371,:455,:508,:706,:883 | Process-control/Windows, không phân loại công cụ DUNG_DUOC/THIEU/BI_CHE; ngoài phép vá |
| Hook phiên thực thi và ops/cai_cong_cu.sh | Không nằm trong diff; chỉ test có sẵn chạy fixture | SPEC loại rõ; không tính finding cho các spawn thô tại đây |

## BANG TEST

| Bộ | N/M thực đo, mã thoát | Bỏ qua / giới hạn |
|---|---|---|
| HEAD `python3 .claude/dev/launcher_test.py` | 295/308 đã chạy qua; tổng318;13 hỏng; rc1 | 10 bỏ qua:2 native Windows,8 cần venv/pip |
| Base cùng lệnh/cùng môi trường | 291/304 đã chạy qua; tổng314;13 hỏng; rc1 | Cùng10 tên bỏ qua và13 tên lỗi; delta0 |
| HEAD `--dot-bien` | 506/506; rc0 | 4 không đo được:3 native Windows và1 ca t62 chỉ dành Windows |
| Bốn ca r1077 trên HEAD | 4/4 | 0 bỏ qua trên Linux |
| Bốn mutant wp1077 replay nghiêm ngặt | 4/4 mutant,5/5 cặp mutant/ca chết đúng TinHieuChotCa | Không nhận lỗi ngoại lai làm kill |
| Mutant bổ sung M1/ngữ nghĩa | 12/12, tám ca neutral xanh trước khi phá | Bản sao tạm; guard nt/sh-vắng là mock có ghi rõ |
| Phản chứng base mới | 2/2 ca (a),(d) ĐỎ đúng assertion | Chạy ca HEAD với source base; git còn được đo riêng bằng S |
| Ca F1 và F3 | F1: HEAD đỏ → bản sao dùng helper xanh → revert mutant đỏ. F3: HEAD xanh → mutant mất argv đỏ;4/4 ca PR gốc vẫn xanh trên mutant đó | Không có sửa sản phẩm nào trong cây review |
| HINT.patch | dry-run/apply `patch -p0` rc0; Ruff5F841 (delta0); t117 và ca argv/env qua; ca Codex mới đỏ đúng F1 | Chỉ thử trên bản sao. Hint là test + comment giới hạn, chưa phải bản vá đầy đủ F1/F2 |

## BANG SAN

Các hướng dưới độc lập về tiền đề lỗi; lệnh S/P/F/X/C được định nghĩa ở trên, output chi tiết giữ nguyên trong evidence.

| Hướng / lệnh | Output thật | Phân loại |
|---|---|---|
| Wrapper POSIX không shebang đầu PATH, rg và git; S | base rc12 BI_CHE; HEAD rc0/co=true/không bi_che | KHÔNG PHẢI LỖI: tái hiện gốc đã đóng |
| Wrapper hỏng có output và exit1; S/P | helper rc1; version/auth False; mutant ép rc0 bị ca(b) giết | KHÔNG PHẢI LỖI |
| Tệp shebang hợp lệ,0644 khi uid0; S/C | errno13/PermissionError; version False, qua_han=False | KHÔNG PHẢI LỖI |
| `$0`, đối số có khoảng trắng, env; S/P | bash/libc/helper cùng `$0` là đường dẫn script; argc2,one=--version,two=two words,env=from-env; mock giữ mọi kwargs | KHÔNG PHẢI LỖI ở code HEAD |
| Tệp rỗng và chỉ BOM; S | empty: bash/libc/helper rc0 nhưng hai probe False do không output. BOM: cả ba rc127, hai probe False | KHÔNG PHẢI LỖI; chính sách đòi output vẫn giữ |
| ELF có x, đổi e_machine của /bin/true sang AArch64; S | bash rc126/cannot execute binary; libc/helper rc2/Syntax error; version/auth False | KHÔNG PHẢI LỖI phân loại trong mẫu này; mã thoát/parser không tương đương bash |
| Timeout của chính lượt /bin/sh retry; S/P | timeout=.15s: version `(False,timeout...,True)` khoảng.159s; auth cờ True khoảng.151s; mutant nuốt cờ bị bang giết | KHÔNG PHẢI LỖI |
| OSError ở lượt retry; P | exactly2 spawn, trả lại cùng lỗi lần2; mutant chạy lần3 chết TinHieuChotCa | KHÔNG PHẢI LỖI |
| sh vắng; P và `python3 ../evidence/no_sh.py`, `chroot-limit.json` | isfile=False: đúng1 spawn và rethrow ENOEXEC. Thử môi trường thật bằng chroot bị PermissionError errno1 | KHÔNG ĐO ĐƯỢC bash/libc thật trong hệ không có sh; guard helper đã đo bằng mock, không tính hồi quy |
| Windows; P/C | guard nt không retry;4 test trả BO QUA shell POSIX khi mô phỏng LA_WINDOWS=True | KHÔNG ĐO ĐƯỢC native Windows; ngoài phạm vi, không gắn pass native |
| Probe khả dụng sau bảng version; F/X | Codex version xanh/status KHONG_DO_DUOC; llm errno8; Github CHUA_XAC_THUC ↔ DUNG_DUOC khi thêm shebang; MCP khong_do_duoc ↔ khoe | LỖI F1 |
| Parser bash thật đối chiếu glibc thật; S | wrapper `[[ ... ]]`: bash rc0/in phiên bản, glibc/helper rc127, doctor BI_CHE rc12 | LỖI F2: lời khai/bash equivalence sai có hậu quả |
| Bỏ đối số trong retry, không làm hỏng source; F | 4/4 ca r1077 hiện có vẫn PASS; ca mới HEAD PASS, mutant TinHieuChotCa với `lost arguments`/rc6 | LỖI F3: chốt thiếu răng |
| Đối chiếu lỗi sandbox; C | Cùng13 lỗi và10 bỏ qua trên HEAD/base; không có tên lỗi/bỏ qua mới | KHÔNG ĐO ĐƯỢC các ca đó; không tính13 lỗi thành finding |

## FINDINGS

### F1-probe-kha-dung-con-bo-sot [P1] Hai điểm nối không phủ đủ probe của doctor

TEP/DONG: `.claude/dev/launcher.py:2962,3014` (điểm nối trong diff); `:3909` (Codex status bỏ sót); các spawn tương tự đã liệt kê trong bảng kiểm kê, đặc biệt `:319,:4015,:4023,:4037,:4546,:4607,:286`. Commit gạch2 gọi chúng là “hai duong probe cua doctor”.

VAN DE: Doctor còn tầng KHA_NANG chạy CLI riêng sau CONG_CU. Với cùng wrapper Codex POSIX không shebang, `_phien_ban` xanh nhưng `_do_codex` ném ENOEXEC tại subprocess.run thô, trả KHONG_DO_DUOC; chỉ thêm shebang thì thành CO_CREDENTIAL. X còn cho thấy cùng lớp lỗi ở llm và git/gh. Các đường này là doctor, không phải `launcher run`, hook thực thi hay trình cài đã bị SPEC loại. Đây là thiếu sót được kế thừa từ base, không khai là hồi quy do diff; nó vẫn thuộc yêu cầu kiểm kê/đóng các probe trong lượt review này. Hai hàm M2 đích danh đã nối đúng, nhưng không được suy chúng là toàn bộ probe doctor.

DA THU NGHIEM: `python3 ../evidence/finding_cases.py`: ca `r1077_doctor_codex_status_khong_shebang` HEAD đỏ bởi bang của chính ca, thông báo version xanh/capability KHONG_DO_DUOC. Bản sao tạm đổi riêng probe status qua helper làm ca xanh; revert mutant lại đỏ cùng assertion. `extra_paths.py` cho llm errno8 và GitHub CHUA_XAC_THUC thay cho DUNG_DUOC trong fixture tương đương có shebang. Mọi prerequisite credential/REST được stub; không có gọi mạng. CO_CREDENTIAL của fixture không được dùng chứng minh credential thật còn sống.

DO TIN: Cao về bỏ sót và kết quả phân loại; không suy bất kỳ kết quả live/native nào từ mock.

GỢI Ý: Vá tại các caller probe khả dụng trong launcher và điểm delegate cần thiết, dùng cùng chính sách ENOEXEC; giữ nguyên thông số env/stdin/timeout/encoding và logic auth/rc hiện có. Không đổi `_chay_van_ban_an_toan` hoặc `_git` toàn cục một cách mù vì chúng phục vụ cả run/việc nghiệp vụ ngoài phạm vi. Nếu không thể hoàn tất delegate trong write set đóng băng, phải ghi rõ phần thiếu và xử lý revision/successor, không khai đã phủ toàn doctor. Ca khóa tối thiểu là test Codex mới trong HINT; bổ sung tương tự cho llm và đường GitHub độc lập, mỗi ca cần mutant bỏ helper. Nguy cơ khi vá: mở hành vi retry cho lệnh ngoài phạm vi hoặc vô tình biến “có credential” thành “đã kiểm sống”; giữ nguyên ranh giới phân loại. HINT chỉ mang test phản chứng, chưa tự vá hết nhóm này.

### F2-bash-khong-phai-bin-sh [P1] Lời khai bash/execvp đồng nghĩa là sai, doctor vẫn BI_CHE oan cho wrapper bash

TEP/DONG: `.claude/dev/launcher.py:2925–2927,2938`; `.claude/dev/launcher_test.py:9237`; commit đoạn đầu và gạch mô tả “nhu bash/execvp”.

VAN DE: Bash không đồng nhất với glibc execvp ở fallback ENOEXEC. Trong container thật, bash chấp nhận script không shebang và dùng cú pháp bash; glibc execvp dùng `/bin/sh` (dash). Wrapper có điều kiện `[[ ... ]]` in phiên bản và rc0 trong bash, nhưng helper nhận rc127, doctor quay lại chọn bản tốt sau và gắn BI_CHE/12 — đúng loại báo oan mà packet tuyên bố loại bỏ. M1 yêu cầu `/bin/sh` nên code làm đúng hợp đồng hẹp; finding là mệnh đề đo được sai trong diff/commit và phạm vi kết luận rộng hơn hợp đồng đó, không ghi sai rằng argv M1 được triển khai sai.

DA THU NGHIEM: S dùng `/bin/bash --noprofile --norc` và `ctypes.CDLL(None).execvp` thật trong child (không dùng os.execvp của Python làm oracle libc). `bashism`: bash0/in `ripgrep 14.1.0-bash`; libc127; helper127; `doctor_bashism`: rc12/trang_thai BI_CHE. ELF sai kiến trúc cũng cho bash126/libc2 nhưng cả hai vẫn hỏng; không đếm thêm finding cho khác rc đó. Không đo được trường hợp thiếu sh thật do chroot bị sandbox từ chối.

DO TIN: Cao; không dựa vào mô phỏng parser hoặc tài liệu nhớ lại.

GỢI Ý: Cách hẹp là sửa comment/docstring/khẳng định commit để nói rõ chỉ theo glibc execvp và `/bin/sh`, giới hạn script POSIX tương thích, công bố wrapper bash vẫn có thể khác. HINT có gợi ý lời văn này. Nếu mục tiêu bắt buộc là khớp bash thật thì cần chốt lại đặc tả, vì tự đổi `/bin/sh` thành `/bin/bash` sẽ vi phạm M1 đóng băng. Ca khóa hiện có ở reviewer `gioi_han_bash_khac_sh` xanh theo M1 và mutant dùng bash thay sh làm đúng bang đỏ; phép đo bash/libc/doctor thật phải được giữ để không tái khai đồng nghĩa. Nguy cơ của đổi interpreter là đổi cú pháp và chính sách nhận/từ chối binary; không thể coi đó là sửa diễn đạt đơn thuần.

### F3-test-khong-khoa-doi-so [P2] Bỏ toàn bộ đối số của lượt chạy lại vẫn qua cả bốn ca mới

TEP/DONG: `.claude/dev/launcher_test.py:9262,9273,9285,9298–9300`; bảng mutant wp1077 bắt đầu `:12220`. M1 yêu cầu `[/bin/sh,duong_dan,*doi_so]`, code HEAD tại launcher.py:2938 hiện đúng.

VAN DE: Fixture thành công chỉ echo hằng, fixture hỏng exit1 vô điều kiện; không ca nào cần `--version` hay `status` để thành công. Đột biến hợp lệ thay fallback bằng `[/bin/sh,lenh[0]]` vứt hết đối số, nhưng4/4 ca r1077 vẫn xanh. Do đó bốn mutant M4 đúng đích chưa chứng minh đủ hợp đồng đối số mới của M1. Đây là thiếu độ nhạy của test, không phải bug argv hiện có trong helper.

DA THU NGHIEM: F tạo mutant ngoài cay-kho, chạy4 ca gốc: cả4 PASS. Ca mới `r1077_retry_giu_argv_env` dùng script kiểm `$1`, `$#`, đối số `two words` và biến MEASURE: HEAD PASS; mutant đỏ TinHieuChotCa với version False/`lost arguments`, auth rc6. P còn kiểm kwargs/biên đối số bằng spy và mutant giữ sai kwargs chết đúng assertion.

DO TIN: Cao; không có SyntaxError/OSError ngoại lai được nhận làm tín dụng kill.

GỢI Ý: Thêm ca giữ argv/env và mutant `wp1077_retry_mat_doi_so` như HINT.patch; đặt ở nhóm r1077 vì đây là chốt hợp đồng helper mới, không cần sửa các test unrelated. Đã kiểm hint trên bản sao: t117 mỏ neo xanh, ca mới xanh; mutant mất argv đỏ bằng ca đó trong F. Nguy cơ test mới là vô tình kiểm phụ thuộc shell ngoài POSIX hoặc environment máy; fixture chỉ dùng builtin POSIX, env tối thiểu và trả BO QUA shell POSIX trên Windows.

## HINT VA GIOI HAN

`HINT.patch` là gợi ý reviewer, áp bằng `patch -p0 < ../HINT.patch` khi đứng trong một BẢN SAO của cay-kho. Đã dry-run và áp thật trên bản sao tạm, chưa áp trên cây review. Nó bổ sung hai ca, một mutant argv và sửa lời văn về phạm vi bash; cố ý giữ ca Codex mới ĐỎ trên sản phẩm hiện tại để executor tự sửa và đo lại. Không coi hint là bản vá đầy đủ hoặc bằng chứng CI. `evidence/hint.log` ghi cả kết quả xanh lẫn đỏ dự kiến.

Không tính13 lỗi môi trường hay10 ca bỏ qua thành finding sản phẩm; không tính các đường run/hook/cài công cụ đã loại phạm vi. Không có kết luận pass CI exact-head, native Windows hoặc môi trường thiếu `/bin/sh`. Các hướng liên quan credential nhạy cảm chỉ dùng ca sẵn có, fixture vô hại hoặc mô tả, không soạn payload nhạy cảm.

## CAC CA MOI TRUONG KHONG DO DUOC

Hai suite có cùng tập tên dưới đây (evidence/summary.json); delta lỗi/bỏ qua rỗng. 2 lỗi đầu là /var/tmp chỉ đọc sau khi bộ chọn tránh tổ tiên /tmp/.git; 11 lỗi còn lại là nhóm Codex home/materializer trong cùng điều kiện. Không xóa /tmp/.git hoặc sửa test để lấy xanh.

- `r858_goc_tam_tranh_to_tien_co_git`
- `t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac`
- `r484_g2_doctor_doc_dung_home_da_materialize`
- `r484_g2_schema_truoc_freshness_va_home_materialize`
- `r484_g2_child_khong_nhan_snapshot_va_rac_chan_truoc_probe`
- `r484_g2_storage_kernel_guardrails`
- `r484_g2_recovery_probe_rollback_va_snapshot_moi`
- `r484_g2_probe_isolated_marker_va_refresh`
- `r484_g2_hook_shell_scrub_truoc_probe`
- `r484_g8_hook_scrub_kin_voi_bash_env`
- `r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do`
- `r484_g7_tu_choi_ghi_dung_ban_da_probe`
- `r484_g7_auth_doi_truoc_khi_thay_thi_giu_ban_moi`

Bỏ qua10 ca:2 ca Windows;8 ca trả thông báo không dựng được venv/pip, không được tính là qua.

- `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125`
- `r345_chan_socket_that_ma_than_hook_van_chay_dung`
- `r345_cac_phep_do_cuc_bo_van_dung`
- `r345_lop_tham_import_van_co_rang`
- `r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO`
- `r347_tham_import_van_song_tren_python_truoc_310`
- `r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO`
- `r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia`
- `r348_dot_bien_bo_isidentifier_lam_ca_dich_DO`
- `r484_g4_windows_sid_alias_identity`

Bốn mutant chính thức không đo được trên Linux: `g4_windows_sid_alias_not_normalized`, `g4_windows_LA_not_current_owner`, `g2_windows_directory_pin_access`, `124_khi_chau_con_song`. Mutation headline đã loại chúng khỏi mẫu số506.

Kết quả cuối neo lại HEAD/spec: `e61def425e0656be4fd75a5fa5410972638ad395` / `eabbb725650addad531429d48801667f2ef05a6090c00123d1d4146c7b89c3f3`; worktree sạch và9.125 hash tệp không đổi. Không còn phép đo đang chạy.
