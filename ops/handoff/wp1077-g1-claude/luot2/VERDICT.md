verdict: changes_requested
reviewed_sha: dcfb0115cef9defa0af35c7aca0537d75b87dd17
spec_sha256: eabbb725650addad531429d48801667f2ef05a6090c00123d1d4146c7b89c3f3
Ket qua: 0 P0, 3 P1, 0 P2, 0 P3.

PR #1080, packet #1077 DOCTOR-ENOEXEC-BI-CHE r1/g1, lease `wp1077-r1-g1-claude`, sensitive, lượt Codex **2/2 cuối**. Hai finding hành vi P1: F1 cũ còn mở và F4 mới về chọn sai executable trong PATH. F5 là khẳng định số dòng sai đo được; xếp P1 theo quy ước riêng của prompt, không coi nó là lỗi runtime. F2 và F3 lượt trước đã vá thật.

Base `086f1b7343fc1d778e50797e6c9ca0964b11a755`; tree HEAD `ac662cbe687d6fcdfd639f5e2578e111ce05a85c`. HEAD detached đúng OID. Git diff khớp byte `diff.patch`; numstat khớp `numstat.txt`: launcher 48/9, test 188/10; 2 tệp, **236 dòng thêm, 19 dòng bớt**. Không có đổi `_AP_DUNG_BI_CHE`, danh sách ứng viên hoặc logic ngân sách/quá hạn trong diff.

Danh tính theo `runs/bc1b29d6/run.json`: provider `openai_codex`, execution_surface `codex_cli`, transport `machine`, run_id `bc1b29d6c305427fa0cd9befcfe917a4`; họ model OpenAI theo phiên hiện tại. Không suy model thực phục vụ, danh tính executor hoặc tính độc lập bằng Co-Authored-By; phân công reviewer khác họ/context executor được nhận từ prompt. Không đăng GitHub, push/fetch, gọi dịch vụ mạng hoặc dùng credential thật. Mọi đường REST/MCP remote được stub; CLI giả chạy cục bộ. Không nhận thành công của CLI giả là bằng chứng credential thật còn sống.

Môi trường: Linux x86_64, Python 3.13.16, bash 5.2.21, glibc 2.39, uid=0, `/bin/sh -> dash`; `/tmp/.git` tồn tại và chỉ đọc; `/var/tmp` không ghi được. Skill runtime đã đọc; không có tool `environment_status` callable. Windows native, CI remote và môi trường thật vắng `/bin/sh` không đo được. Sandbox thực tế là workspace-write, không phải filesystem read-only.

## LENH TAI LAP VA PHAM VI BANG CHUNG

Các lệnh ngắn dưới chạy từ `cay-kho/`, đọc HEAD và ghi bằng chứng/bản sao ngoài cây review. Tên S/R/B/I/P/F/A/C/V/Q dùng trong các bảng bên dưới.

```sh
# S: bash thật, glibc execvp thật, argv/$0, empty/BOM/ELF, timeout
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/semantics.py
# R: 8 ca packet trên HEAD/base; replay nghiêm ngặt 9 mutant mới
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/replay.py
# B: các probe khả dụng, guard/kwargs và mutant bổ sung
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/behavior.py
# I: call graph AST toàn launcher, không chỉ các tên trong diff
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/inventory.py
# P: hai executable cùng tên; thử sửa và đảo sửa ngoài kho
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/path_shadow.py
# F: đối chứng sửa/đột biến các đường Git và Codex delegate
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/finding_controls.py
# A: từng rg/git doctor trên HEAD/base và launcher lịch sử 2bcd8f3
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/acceptance.py
# C: cách trích khẳng định + số dòng + commit message
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/claims.py
# V: dry-run/áp HINT trên bản sao tạm, chạy test và mutant
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/validate_hint.py
# Q: so tập lỗi/bỏ qua và hash tracked đầu/cuối
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/summary.py
```

Bộ đầy đủ được chạy thực sự, với subprocess cwd trỏ đúng cây tương ứng:

```sh
# Từ thư mục chứa VERDICT.md:
python3 evidence/run_suite.py head cay-kho
python3 evidence/run_suite.py mutation cay-kho --dot-bien
python3 evidence/run_suite.py base evidence/base-copy
```

Wrapper chạy đúng `python3 .claude/dev/launcher_test.py` và `python3 .claude/dev/launcher_test.py --dot-bien`; mã thoát của lệnh con nằm trong `head.json`, `base.json`, `mutation.json`. Nó dùng môi trường tối thiểu, HOME cô lập, Git config rỗng, `PYTHONDONTWRITEBYTECODE=1` và `PIP_NO_INDEX=1`. Base được giải nén từ `git archive BASE` ngoài kho, không checkout hoặc sửa cây review. Log đầy đủ giữ ở `evidence/`.

Danh sách dưới đây không được dùng làm trần review: `claims.py` ánh xạ mọi dòng sửa sang hàm/docstring bằng AST; reviewer đọc toàn diff, phần DOT_BIEN ngoài hàm và toàn commit riêng. Cách này không tự hiểu ngữ nghĩa bình luận, lambda, chuỗi động hoặc lịch sử bên ngoài kho. Vì vậy tôi còn dựng call graph độc lập I, lần theo bảng CONG_CU/KHA_NANG và delegation, rồi tạo phản chứng hành vi. Mục bị bộ trích bỏ sót vẫn được tính finding. Không xác minh được nguồn người viết/Issue từ mạng thì ghi giới hạn, không chuyển thành pass.

## DOI CHIEU LUOT TRUOC

| Finding lượt 1 trên e61def425e0656be4fd75a5fa5410972638ad395 | Phân loại | Tự đo tại HEAD | Kết luận |
|---|---|---|---|
| F1-probe-kha-dung-con-bo-sot, P1 | **VÁ HỜ** | R: Codex status và llm mới xanh. B: llm ba lệnh, gh auth/api, MCP đều nhận script POSIX không shebang khi nó là bản executable duy nhất. I/B/F: `_git` và delegate Codex vẫn thô; P: tên trần còn bỏ qua wrapper đầu PATH | Các điểm vá có tác dụng nhưng lớp chưa đóng. Việc tự ghi hai đường là “ngoài phạm vi” không sửa được SPEC. F4 là biểu hiện khác cần test PATH hai bản |
| F2-bash-khong-phai-bin-sh, P1 | **ĐÃ VÁ THẬT** | S: bashism chạy bash rc0; glibc/helper rc127. Docstring hiện công bố đúng khác biệt đó; commit mới nhận rõ lời khai cũ sai | Không yêu cầu đổi interpreter trái M1; giới hạn hiện đã nói rõ |
| F3-test-khong-khoa-doi-so, P2 | **ĐÃ VÁ THẬT** | R: `r1077_retry_giu_argv_env` xanh; mutant bỏ đối số chết bởi chính TinHieuChotCa, version/auth đều không đạt | Test kiểm số đối số, `two words`, biến MEASURE và kết quả hai caller |

Không gọi F4 là hồi quy runtime so với base: raw subprocess ở base cũng có hành vi chọn bản sau. Đây là phần mục tiêu còn chưa được sửa và lời khai mới về helper không đúng trong trường hợp đã đo.

## BANG NGHIEM THU

| Tiêu chí | Lệnh | Output thật | Đạt? |
|---|---|---|---|
| M1: helper ENOEXEC, POSIX, có sh; một lần; giữ argv/env/stdin/timeout/encoding; giữ lỗi khác và phân loại rc/rỗng | S; B `contract_*`; R | Guard EACCES/no-sh/Windows chỉ 1 spawn, giữ cùng exception; ENOEXEC 2 spawn; lỗi lần hai không có lần ba; kwargs/env identity giữ nguyên; empty/rc1 không đạt; retry timeout có cờ True. 6 mutant contract chết đúng assertion | **ĐẠT hợp đồng đường dẫn của M1**. Mở rộng tên trần không khớp execvp, F4. Windows/no-sh guard chỉ mô phỏng |
| M2: hai hàm đích dùng helper, kiểm kê đủ đường doctor | I; R; B/F | `_phien_ban:2978`, `_xac_thuc_kem_dau_ra:3030` dùng helper; auth mutant chết đúng ca. Call graph vẫn tới `_git:286`, delegate subprocess tại codex_cred.py:197 | **ĐẠT hai điểm nối đích danh**; không đạt lời khai phủ toàn doctor, F1 |
| M3(a): rg và git không shebang đầu PATH, bản tốt sau | A; R | HEAD cả rg/git rc0, co=true, chọn wrapper đầu, bi_che=null; ca gốc xanh | ĐẠT |
| M3(b): wrapper exit1 vẫn BI_CHE/12 | R; S | Ca `r1077_doctor_khong_shebang_hong_van_BI_CHE` xanh; mutant bỏ qua rc chết chính ca | ĐẠT |
| M3(c): shebang hợp lệ, mode0644 không được retry | S; R | Kernel errno13 kể cả uid0; helper giữ PermissionError; version False/qua_han=False; mutant mọi OSError chết chính ca | ĐẠT |
| M3(d): auth không shebang có dòng, rc0 | R; S | HEAD ok=True; base False/OSError; mutant auth spawn thô chết TinHieuChotCa | ĐẠT |
| M4: bốn mutant bắt buộc giết đúng ca | R; suite --dot-bien | Bốn mutant lần lượt 2/2,1/1,1/1,1/1 ca đích; từng ngoại lệ là TinHieuChotCa, không lấy SyntaxError/OSError ngoại lai làm kill | ĐẠT |
| A1: suite và đột biến, delta lỗi nền=0 | Q; ba lệnh run_suite ở trên | HEAD rc1:289/312, tổng322/bỏ10/hỏng23; base rc1:281/304, tổng314/bỏ10/hỏng23. Tập tên lỗi/bỏ qua trùng nhau. Mutation rc0:511/511; không đo4. Thêm8 ca đều xanh | ĐẠT delta hồi quy và mutant mới; **không phải suite xanh toàn phần**, 23 lỗi nền và10 ca bỏ qua ghi riêng |
| A2: ca (a),(d) đỏ trên base | R; A | (a) TinHieuChotCa/doctor12 BI_CHE; (d) TinHieuChotCa/ok=False. A đo riêng git và rg để tránh vòng lặp (a) dừng sớm ở rg | ĐẠT |
| A3: tái hiện tại chỗ doctor với wrapper đầu PATH | A | HEAD rg/git đều rc0, co=true, version không-shebang; base đều12/BI_CHE | ĐẠT fixture qua lenh_doctor thật. Không gọi full doctor với các probe remote thật |
| A4: bare Ruff F delta0, diff-check0, doctrine0, CI exact-head xanh | `ruff check --select F --output-format json --no-cache .claude/dev/launcher.py .claude/dev/launcher_test.py`; `git diff --check BASE HEAD`; `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | Ruff0.16.8: HEAD/base đều rc1 với cùng5 F841, delta0; diff-check rc0; doctrine rc0,10 tệp/0 vi phạm. `gates.json`, `doctrine.log` | Ba phép cục bộ ĐẠT. **CI exact-head KHÔNG ĐO ĐƯỢC**, offline/không có receipt trong bundle; không nhận A4 toàn phần |

## BANG DO

| Khẳng định | Diff/commit khai | Đo được (lệnh) | Khớp? |
|---|---|---|---|
| Lỗi cũ trên 2bcd8f3 với executable không shebang | Helper docstring | A đọc Git object cục bộ, chạy `_phien_ban` thật trên rg/git: False/Errno8 | Có cho hành vi. Không xác minh lại danh tính reviewer/Issue #823 từ mạng |
| glibc execvp chạy lại script bằng /bin/sh | :2922–2926 | S dùng ctypes gọi **glibc execvp thật trong child**: POSIX rc0, bashism127; helper tương ứng0/127 | Có cho đường dẫn; tên trần hai bản lệch, F4 |
| Bash dùng chính bash, có thể khác /bin/sh | :2927–2929; comment test; commit F2 | S: `[[ ]]` bash0/in version; glibc/helper127; `/bin/sh` là dash | Có. Khác biệt ELF126/2 cũng được ghi, cả hai cùng hỏng |
| Chỉ ENOEXEC/POSIX/có tệp sh mới retry | :2941–2947; commit | S+B: EACCES giữ nguyên; mock nt/isfile=False chỉ một lời gọi; các mutant nới guard chết đúng assertion | Có trong phạm vi đo; không chứng minh Windows native |
| Retry đúng một lần, giữ lỗi lần hai | :2948 | B contract_once:2 lời gọi và giữ exception; mutant lần ba chết TinHieuChotCa | Có |
| Giữ đối số, $0, env, stdin, timeout, capture/text/codec | Helper **kw và hai caller | S: $0/argc/`--version`/`two words`/MEASURE khớp bash/glibc; B so kwargs và env identity; R test argv mới | Có |
| Retry không nới rc!=0 hoặc output rỗng | Docstring; M1; test(b) | S empty:rc0 nhưng version/auth False; rc1 đều False; R mutant ép rc0 chết (b) | Có |
| Mọi probe CONG_CU/KHA_NANG đều qua helper; AST test khóa đủ | :2935–2936; test:9373–9389; commit tiêu đề/F1 | I liệt kê `_git` và delegate; B/F phản chứng 5 đường; test AST hiện vẫn PASS | **Không, F1** |
| Giải tên trần theo PATH của env là đủ để theo execvp | :2934–2945; commit tiêu đề/F1 | P với hai executable: bash FIRST, glibc FIRST, helper LATER; llm/gh/MCP sai nhãn | **Không, F4**. Giải sau khi đã nhận exception là quá muộn |
| /bin/sh nhận tên script như đường dẫn, cần giải tên trước | :2934–2935 | Đã chạy `/bin/sh hello` với script chỉ trong PATH:rc2/cannot open; `/bin/bash hello`:rc0 | Đúng cho dash ở container; không phổ quát cho mọi implementation /bin/sh. Không có thêm hậu quả khác ngoài F4 trong phạm vi đo |
| `_chay_probe_llm` giữ hợp đồng text/UTF-8/replace/DEVNULL và chỉ đổi đường probe | :2951–2957; ba chỗ gọi | I: ba caller chỉ ở `_do_openai_llm`; B: cả version/keys/prompt đi qua fake script; kwargs từ source giữ đúng giá trị | Có về wrapper/caller; vẫn chịu F4 khi có executable sau |
| Codex status dùng đường resolve và helper | :3925; ca Codex mới | R/B: phiên bản + status xanh không shebang; mutant status thô chết hai ca đích | Có cho status; không phủ kiểm sống delegate, F1 |
| gh auth, gh api, claude mcp get nhận fallback | :4364,4562,4623 | B: gh-cli=OK/gh-kho=OK, MCP=khoe; từng mutant bỏ helper chết đúng assertion | Có khi không có executable hợp lệ phía sau; P chỉ ra giới hạn F4 |
| `_git` và `_do_codex_song` được SPEC loại phạm vi | Test docstring và commit F1 | Đọc SPEC mục Ngoài phạm vi; I lần theo doctor, F đối chứng sống cục bộ | **Không, F1**. Spec loại `run`/`_probe_spawn`, hook phiên, installer và Windows; không loại invocation của doctor vì dùng hàm chung hoặc delegate |
| Fixture wrapper đầu, bản shebang tốt sau; mode mặc định có x | `_wp1077_tep`, `_wp1077_doctor` | A lưu chosen path trên HEAD/base; S đo errno13 với0644; R bốn ca gốc | Có |
| Ca argv mới kiểm hai caller và env | Test:9304–9325 | R HEAD PASS; bỏ argv chết chính ca; S đo $0 riêng | Có, đóng F3 cũ |
| Ca llm mới giải tên trần và base đỏ bằng assertion | Test:9352–9368; commit | R: HEAD PASS/base TinHieuChotCa, không OSError ngoại lai. P thêm bản shebang sau làm ca hành vi mới đỏ | Có cho fixture đã viết; fixture chưa khóa trường hợp hai executable |
| t121 đổi stub sang helper llm; hai mỏ neo mutant cũ đã cập nhật | Diff t121, do_codex_spawn_ten_tran, mcp_hoi_ten... | Suite511/511; t117 xanh; V chạy t121/t133/t115 độc lập đều PASS | Có |
| Bốn ca thêm sau lượt1; năm mutant thêm sau lượt1 | Commit | R: argv/Codex/llm/AST bốn ca đều đỏ bằng TinHieuChotCa trên base; tổng9 mutant wp1077=4 cũ+5 mới | Có. AST base đỏ vì thiếu helper mới, không chứng minh phủ call graph |
| `launcher_test 320/320 (2 bỏ qua Windows)` | Commit | Đếm322 đăng ký,2 Windows; số320 hợp với môi trường executor có đủ pip/không vướng tmp. Tại đây289/312,bỏ10,hỏng23, base cùng lỗi | Không tái lập được kết quả xanh của executor trong sandbox này; **không đủ chứng cứ gọi lời khai lịch sử đó sai** |
| Ruff F delta0 | Commit | HEAD/base cùng5 F841, rc1, delta0 | Có; không đổi thành “Ruff lint xanh tuyệt đối” |
| `+228 dong` | Commit đoạn “Do:” | C; git diff --numstat:48+188=**236** dòng thêm, net217; riêng commit cuối142/24, net118 | **Không, F5** |
| Co-Authored-By, Claude-Session và kết quả CI/máy Windows khác | Commit metadata và A4 | Không gọi mạng/không có attestation hoặc receipt exact-head tương ứng | KHÔNG ĐO ĐƯỢC; không suy identity hay pass từ chuỗi metadata |

## KIEM KE TOAN BO DUONG PROBE

I duyệt AST toàn launcher, không chỉ tập bảy hàm trong test mới. Gốc callback KHA_NANG được thêm tường minh vì graph tên hàm đơn thuần bỏ sót lambda/bảng dữ liệu. `evidence/inventory.json` lưu edges/spawns; `probe-roots.json` lưu đủ13 mục công cụ.

| Đường vào | Lệnh/phép đo | Spawn cuối | Phạm vi và kết quả |
|---|---|---|---|
| CONG_CU: git; python(python3/python/py); claude; codex; rg; bash; gh; npm; node; llm; agy; actionlint; shellcheck | Từng ứng viên `--version`, kể cả retry timeout và bản tên trần BI_CHE | `_phien_ban → _chay_probe_nhu_shell` | Trong phạm vi; đường dẫn resolved nhận ENOEXEC đúng |
| Auth của CONG_CU | `claude auth status`, `agy models`; `_xac_thuc` public cũng bọc hàm dưới | `_xac_thuc_kem_dau_ra → helper` | Trong phạm vi; kết quả được cache cho Antigravity, không spawn lại khi đã có evidence |
| KHA_NANG codex | `codex login status` | helper, đường dẫn đã resolve | Status đã vá |
| KHA_NANG codex --kiem-song | `_do_codex_song → runpy(codex_cred.py)._kiem_song → codex exec` | **subprocess.run thô tại codex_cred.py:197** | Invocation này của doctor, không phải launcher run; chưa vá, F1. Module delegate ngoài write set là ràng buộc sửa, không tự thành ngoại lệ scope |
| KHA_NANG openai-llm | `llm --version`, `llm keys list`, `llm prompt ... --no-log` khi đòi kiểm sống | `_chay_probe_llm → helper`, tên trần | Đã nối; F4 khi có bản chạy được phía sau |
| KHA_NANG github | `gh auth status`; `gh api repos/<slug> --jq .full_name` | helper, tên trần | Đã nối; F4 |
| KHA_NANG github/MCP CLI | `claude mcp get <ten>` | helper, tên trần | Đã nối; F4 |
| KHA_NANG github/Git | `git -C ws ls-remote --heads origin HEAD`, `remote get-url origin` | **_git → subprocess.run:286** | Trong phạm vi doctor; chưa vá, F1. Phản chứng dùng Git giả nên không có ls-remote mạng |
| KHA_NANG hook-phien, launcher-phien | `git show origin/master:<hook hoặc launcher>` | **_git → subprocess.run:286** | Đo file/năng lực của doctor, không thực thi hook phiên; chưa vá, F1 |
| doctor tìm workspace | `tim_workspace → chot_workspace → _git_mot_dong → _git`, `git rev-parse --show-toplevel` | **subprocess.run:286** | Trong phạm vi; plain wrapper làm Chan3, shebang/control trả đúng workspace, F1 |
| KHA_NANG antigravity | Cached auth, hoặc `agy models`, rồi `--version` nếu cần | Hai helper đã nêu | Đã phủ; B ca plain xanh, mutant auth thô làm CO_MAT và chết assertion |
| KHA_NANG claude, hook-da-chay; kiểm môi trường/module Python | File/env/mtime, find_spec/import; materializer/chờ snapshot là I/O cục bộ | Không spawn công cụ theo đường dẫn ở các phép đo này | Không có lỗ ENOEXEC thuộc loại đang xét |
| GitHub REST, MCP endpoint | HTTP REST/initialize | Không spawn executable | Trong graph nhưng không phải lỗi ENOEXEC; chỉ stub offline, không đo dịch vụ thật |
| `_probe_spawn`, child Popen của run; hook thực thi; installer; nhánh Windows | Các lệnh ngoài doctor hoặc chính chức năng đã bị SPEC loại | Giữ nguyên | **Ngoài phạm vi**; không tính finding cho việc chúng chưa nhận fallback |
| `_chay_json_chat_che`, các ps/taskkill, helper text dùng nơi khác | Xử lý JSON/tiến trình/run | Có raw spawn ngoài graph probe công cụ của doctor | Không phát hiện thêm invocation phân loại khả dụng trong phạm vi; không yêu cầu đổi toàn cục |

Việc `_git` dùng chung cho run không cho phép loại **mọi caller doctor** của nó. Có thể tách đường probe hoặc truyền runner riêng để giữ nguyên run; không cần sửa toàn cục một cách mù. Tương tự, vị trí spawn trong tệp delegate không đổi tên lệnh mà người dùng đã gọi: `doctor --kiem-song`.

## BANG TEST

| Bộ | N/M, mã thoát | Bỏ qua/không đo |
|---|---|---|
| HEAD `python3 .claude/dev/launcher_test.py` | **289/312**, rc1; tổng322,23 hỏng |10 bỏ qua:2 Windows,8 venv/pip offline |
| Base cùng lệnh/cùng env | **281/304**, rc1; tổng314,23 hỏng |Cùng10 ca, không thêm/bớt tên lỗi |
| HEAD `--dot-bien` | **511/511**, rc0; tổng515 |4 không đo trên Linux, nêu riêng dưới |
| Tám ca r1077 HEAD | **8/8 PASS** |0; mô phỏng Windows:7 ca hành vi trả đúng `BO QUA shell POSIX`, ca AST vẫn chạy; không gọi là Windows native pass |
| Replay wp1077 nghiêm ngặt | **9/9 mutant**, **12/12 cặp mutant/ca đích** chết TinHieuChotCa |0 exception ngoại lai được tính kill |
| Reviewer B | **13/13 cặp mutant/ca đích** chết TinHieuChotCa |Guard/kwargs/retry và từng đường llm/gh/MCP/agy; đối chứng dương đều chạy |
| Reviewer F | **5/5 đối chứng sửa xanh**, đảo sửa **5/5 TinHieuChotCa** |4 đường Git và1 Codex delegate; sửa thử chỉ trên bản sao |
| Reviewer P | HEAD4 ca đỏ; sửa thử4 xanh; gỡ sửa **4/4 TinHieuChotCa** |Helper/llm/gh/MCP; cả bash và glibc thật chọn FIRST |
| HINT test-only trên bản sao tạm |13/15 ca chọn xanh; **2 ca mới đỏ dự kiến bởi chính assertion**. Dry-run/áp patch rc0. Replay9 mutant/12 cặp đều TinHieuChotCa |Hai ca đỏ là phản chứng F1/F4, không báo hint thành gate xanh |

22/22 cặp mutant/ca đích bổ sung của reviewer (B13+F5+P4) chết đúng lý do. Đây là số cặp chạy, không khai là22 phép biến đổi nguồn độc nhất. Mọi sửa thử/đảo sửa ở thư mục tạm ngoài `cay-kho/`; không nhận lỗi setup/compile thành kill.

## BANG SAN

Mỗi hướng có lệnh và output quan sát được; không dùng ý tưởng thử chưa chạy làm bằng chứng.

| Hướng độc lập | Lệnh | Output thật | Phân loại |
|---|---|---|---|
| 1. Toàn graph doctor và delegate | I; B; F | AST test PASS nhưng Git plain:version=True/khả dụng CHUA_XAC_THUC hoặc KHONG_DO_DUOC; Codex plain --kiem-song CHUA_XAC_THUC; shebang/control DUNG_DUOC | **LỖI F1** |
| 2. Nhiều executable cùng tên trong PATH | P | bash=FIRST; glibc=FIRST; helper=[0,LATER]; llm mất CO_CREDENTIAL; gh mất DUNG_DUOC; MCP từ khoe thành hong | **LỖI F4** |
| 3. Đối số, $0 và env | S; R; B | Script POSIX nhận $0 là đường tệp, argc2, `--version`, `two words`, MEASURE=from-env; helper/bash/glibc đồng ý; mutant bỏ argv chết | KHÔNG PHẢI LỖI; F3 cũ đã đóng |
| 4. Bashism khác /bin/sh | S; B | bash0/version; glibc/helper127; mutant đổi interpreter sang bash làm chốt hợp đồng M1 đỏ | KHÔNG PHẢI LỖI mới; giới hạn đã công bố, F2 cũ đóng |
| 5. ELF sai kiến trúc, empty0 byte, BOM-only | S | Kernel đều ENOEXEC; ELF bash126,glibc/helper2; empty rc0 nhưng hai probeFalse; BOM127/hai probeFalse | KHÔNG PHẢI LỖI mới; khác rc ELF không đổi nhãn; không chấp nhận rc0 rỗng |
| 6. EACCES và điều kiện fallback | S; B | no-x errno13/không retry, nt và no-sh mock chỉ1spawn; lỗi lần hai giữ nguyên; mutant nới guard/lần ba chết | KHÔNG PHẢI LỖI; no-sh/Windows native chưa đo |
| 7. Timeout lượt retry | S; B | Script `exec /bin/sleep 2`, timeout0.2:version(False,...,True), auth(False,...,True,empty); kwargs timeout giữ nguyên | KHÔNG PHẢI LỖI; không nhận timeout là chứng cứ wrapper hỏng |
| 8. `/bin/sh` vắng thật và Windows thật | S; R | chroot rc77:EPERM;7 ca POSIX chỉ được mô phỏng skip; không có Windows runtime | **KHÔNG ĐO ĐƯỢC**; không bịa regression |
| 9. Kết quả suite dưới bẫy sandbox | Q; `ls -d /tmp/.git` | `/tmp/.git` có; HEAD/base cùng23 lỗi và10 bỏ qua, delta tên rỗng | KHÔNG ĐO ĐƯỢC các ca nền; không phải hồi quy diff |
| 10. Khẳng định định lượng/commit | C; `git diff --numstat BASE HEAD`; `git show --shortstat --format= HEAD` |236/19 toàn PR,142/24 commit cuối; không ra +228 | **LỖI KHẲNG ĐỊNH F5**, không phải lỗi runtime |
| 11. Gate và hiện vật review | Q; gates.json; doctrine-scan |9125 tracked hash không đổi; Ruff delta0; diff0; doctrine10/0; không có receipt CI exact-head | Cục bộ phù hợp; CI **KHÔNG ĐO ĐƯỢC** |

### F1-probe-kha-dung-con-bo-sot [P1] Doctor vẫn có probe Git và kiểm sống Codex không nhận ENOEXEC

TEP/DONG: `.claude/dev/launcher.py:2935`, `:3850`, `:3880`, `:4557`, `:4593`, `:4754`, `:4802`; raw spawn chung `:286`; `.claude/dev/launcher_test.py:9373` và `:9377`; commit tiêu đề/F1. Delegate thực tế: `.claude/dev/codex_cred.py:197`.

VAN DE: Đây là F1 cũ **chưa đóng**, không phải finding mới chỉ vì đổi vị trí gọi. Với Git executable không shebang, version đã xanh nhưng doctor tìm workspace thất bại, đường GitHub Git báo không dùng được, hook/launcher báo không đo được. Với Codex, status đã xanh nhưng `doctor --kiem-song` vẫn kết luận CHUA_XAC_THUC vì spawn delegate ném ENOEXEC. Cùng fixture chỉ thêm shebang thì các đường này xanh.

SPEC mục Ngoài phạm vi loại `launcher.py run`/`_probe_spawn`, hook phiên, installer và nhánh Windows. Nó không loại việc doctor gọi `_git`, không loại việc doctor đọc hook bằng git show, và không loại kiểm sống Codex. Tệp delegate ngoài write set là giới hạn thi công cần authority phù hợp; lời khai executor không tự sửa phạm vi đóng băng. Test AST chỉ liệt kê bảy tên và không truy callback/delegate, nên vẫn xanh trước các phản chứng này. Mệnh đề “mọi probe” tại docstring/commit vì vậy sai.

DA THU NGHIEM: B ghi5 ca plain đỏ bởi chính bang: workspace Chan3; GitHub CHUA_XAC_THUC; hook/launcher KHONG_DO_DUOC; Codex CHUA_XAC_THUC/OSError. Cả5 biến thể shebang xanh. F đổi primitive spawn trên bản sao thử,5/5 xanh; đảo sửa5/5 TinHieuChotCa. Không thực hiện network, không dùng auth thật: Git/Codex là CLI giả, storage/REST/MCP được stub. Sửa primitive `_git` toàn cục trong đối chứng chỉ để cô lập nguyên nhân, **không phải đề xuất mở hành vi run**.

DO TIN: Cao về các invocation và kết quả phân loại; không suy credential/API thật từ fixture.

GỢI Ý VÁ Ở ĐÂU/VÁ THẾ NÀO: Tách runner/probe dành cho doctor ở đường Git, gồm cả workspace, rồi đưa các caller doctor qua hợp đồng M1; giữ runner cũ của run. Với `_do_codex_song`, đưa chính sách runner vào điểm delegate hoặc làm revision/successor nếu cần đổi ngoài write set; không được khai đã phủ toàn doctor khi còn lỗ. Mở rộng kiểm kê test theo graph thật thay vì chỉ tăng danh sách cấm bảy hàm.

CA KHOÁ: HINT có ca Git fake không mạng còn đỏ tại HEAD; B/F có đủ5 phản chứng và5 đảo sửa chết đúng assertion. Cần giữ cả đối chứng phiên bản xanh để tránh test chỉ chứng minh CLI vắng mặt.

NGUY CƠ CỦA VÁ: Đổi `_git` toàn cục có thể mở fallback cho run ngoài scope; chỉnh delegate không đúng có thể đổi env/cwd/timeout, làm hỏng việc ghi state hoặc tăng nhãn credential chưa được kiểm sống. Giữ nguyên mọi phân loại và thông số đó; nếu cần mở write set thì phải theo authority của packet.

### F4-ten-tran-bo-qua-wrapper-dau [P1] Giải PATH sau exception để subprocess âm thầm chọn executable phía sau

TEP/DONG: `.claude/dev/launcher.py:2939–2945`, `:2956`, `:4031`, `:4039`, `:4053`, `:4364`, `:4562`, `:4623`; `.claude/dev/launcher_test.py:9352` và nhóm mutant wp1077.

VAN DE: Helper gọi `subprocess.run` bằng tên trần trước khi giải PATH. Trên container thực, subprocess thử tiếp executable phía sau khi bản đầu ENOEXEC. Nếu bản sau có shebang/binary hợp lệ, nó trả kết quả bình thường, nên helper không bao giờ vào except để chạy bản đầu bằng sh. Bash và glibc execvp thật dừng ở bản đầu và chạy bản đó. Kết quả là doctor đo **nhầm bản công cụ**, có thể báo sai trạng thái credential hoặc kết nối dù wrapper người dùng gọi được.

DA THU NGHIEM: P dựng first/cli không shebang in FIRST, later/cli có shebang in LATER. Cùng env: bash0/FIRST; ctypes gọi glibc execvp0/FIRST; helper0/LATER. Ba phép đo hậu quả độc lập: llm trả CHUA_XAC_THUC thay vì CO_CREDENTIAL; gh trả CHUA_XAC_THUC thay vì DUNG_DUOC; MCP trả hong/Failed thay vì khoe/Connected. Không CLI nào đi mạng. Trên bản sao, resolve trước spawn đầu làm4/4 ca xanh; gỡ resolve làm4/4 đỏ bằng chính TinHieuChotCa. Tám ca r1077 sẵn có vẫn xanh tại HEAD; ca llm mới chỉ có một executable llm thực sự trong PATH của sandbox nên chưa khóa tình huống này.

DO TIN: Cao; đối chiếu subprocess, bash và glibc thật, không dùng os.execvp của Python làm oracle libc.

GỢI Ý VÁ Ở ĐÂU/VÁ THẾ NÀO: Giải tên theo PATH thực của env **trước lần spawn đầu**, giữ đúng executable đầu tiên mà chính sách shell M1 cần chạy; sau ENOEXEC chỉ fallback chính tệp đó. Giữ nhánh Windows nguyên trạng. Xử lý cả PATH rỗng/tương đối, env thiếu PATH và cwd của child khi làm resolver. Không chỉ vá từng llm/gh/MCP riêng lẻ.

CA KHOÁ: HINT thêm test hai executable cùng tên, hiện đỏ bởi output LATER. P có các ca khả dụng và mutant bỏ resolve trước spawn; cả4 phải đỏ vì chọn sai bản, không vì lỗi fixture. Khi chuyển resolve lên trước, mutant cũ chỉ phá lookup ở fallback có thể trở nên vô tác dụng; cần thay nó bằng mutant phá lookup trước spawn và cập nhật stub/test nhận đường resolve.

NGUY CƠ CỦA VÁ: Resolver dùng PATH/cwd của process cha hoặc tìm bản chạy được phía sau lại tái tạo lỗi; pre-resolve cũng đổi argv[0] trong các đồ giả của test. Đối chứng thử đã làm lộ ảnh hưởng tới stub MCP và mutant fallback cũ, nên HINT cuối chỉ giao test phản chứng; hướng sửa sản phẩm phải được executor tái dẫn xuất và chạy đủ gate.

### F5-khai-so-dong-sai [P1] Commit khai +228 dòng nhưng diff đóng băng thêm236 dòng

TEP/DONG: `git log -1 --format=%B HEAD`, đoạn `Do: ... ruff F delta 0; +228 dong.`; đối chiếu `numstat.txt` và Git object tại exact HEAD/base.

VAN DE: Đây là khẳng định định lượng ổn định và đo lại được. Toàn diff thêm48+188=236, bớt19, net217. Riêng commit HEAD thêm142/bớt24, net118. Không cách hiểu chuẩn nào trong hai phạm vi diff đã được giao cho ra228. Đánh P1 theo rubric “khẳng định sai đo được” của prompt; sai số này không tạo lỗi chạy và236 vẫn dưới trần300 dòng thêm của packet sensitive.

DA THU NGHIEM: C lưu nguyên commit, numstat và shortstat vào `evidence/claims.json`; lệnh Git cục bộ và hai tệp bundle khớp nhau. Không dựa vào số executor cung cấp.

DO TIN: Cao; hai Git OID và diff được neo đầy đủ, không phụ thuộc mạng/máy khác.

GỢI Ý VÁ Ở ĐÂU/VÁ THẾ NÀO: Sửa lời báo cáo trong commit kế hoặc correction/handoff neo exact SHA thành “2 tệp,236 dòng thêm,19 dòng bớt; net217”, nêu rõ phạm vi BASE..HEAD. Không cần đổi mã để đạt một con số. Commit hiện tại là lịch sử nên HINT test-only không giả làm patch sửa được thông điệp đã commit.

CA KHOÁ: Sinh số báo cáo từ `git diff --numstat BASE HEAD` thay cho gõ tay; giữ số liệu cùng exact OID trong evidence. Đây là kiểm chứng báo cáo, không thêm test runtime hoặc nhận một assertion số học tầm thường làm mutant sản phẩm.

NGUY CƠ CỦA VÁ: Amend/rebase đổi HEAD sẽ làm review và gate hiện tại stale; không tự yêu cầu sửa lịch sử chỉ để đính chính số liệu. Bất kỳ head mới nào phải theo budget/authority hiện hành.

## BANG LOP VA LICH SU

| Slug lớp | Finding/biểu hiện | Mức cao nhất còn mở | Nguồn | Cách đóng chung |
|---|---|---|---|---|
| probe-kha-dung-con-bo-sot | F1:workspace/GitHub Git/git show hook/git show launcher/Codex delegate | P1 | Lượt1 e61def4 → lượt2 dcfb011 | Kiểm kê graph và cấp runner M1 cho mọi invocation doctor;5 đối chứng/đảo sửa |
| bash-khong-phai-bin-sh | F2 cũ, diễn đạt đồng nhất bash với sh | Đã đóng | Lượt1 → lượt2 | Giữ lời văn giới hạn và phép đo bash/glibc |
| test-khong-khoa-doi-so | F3 cũ, bỏ argv vẫn qua | Đã đóng | Lượt1 → lượt2 | Test argv/env + mutant đã có và đã giết đúng ca |
| ten-tran-bo-qua-wrapper-dau | F4:helper/llm/gh/MCP | P1 | Lượt2 dcfb011 | Resolve trước spawn, khóa first/later và mutant ở đúng bước |
| khai-so-dong-sai | F5:metric +228 | P1 theo rubric prompt | Commit dcfb011 | Correction số Git đo được, neo đúng phạm vi/OID |

Ba lớp còn mở, hai lớp cũ đóng. Không đổi slug F2/F3 cũ để dùng cho lỗi mới. Tổng ca hoặc tỷ lệ vá không thay việc đóng từng lớp.

## HINT VA GIOI HAN

`HINT.patch` áp bằng `patch -p0 < ../HINT.patch` khi đứng trong **bản sao** cay-kho. Patch cuối chỉ sửa launcher_test.py, thêm hai ca phản chứng F1/F4. Hai ca mới phải đỏ ở HEAD hiện tại; V xác nhận13 ca chọn cũ xanh/2 ca mới đỏ đúng assertion, dry-run và áp thật rc0,9 mutant wp1077 hiện có vẫn giết12/12 ca đích. Patch mang nhãn: **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**.

Theo protocol của kho, packet sensitive không giao patch sản phẩm cho launcher; hướng sửa sản phẩm nêu bằng lời ở từng finding. Các biến thể sản phẩm trong P/F chỉ là đối chứng thí nghiệm trên bản sao ngoài kho, không phải code đã approve. Không áp hint lên cây review. Executor cần tự tái dẫn xuất, khai hint_provenance nếu dùng, giữ write set và tự đo gate.

## CAC CA MOI TRUONG KHONG DO DUOC

HEAD và base có đúng cùng23 tên lỗi sau. Hai ca đầu vướng `/var/tmp` chỉ đọc sau khi tránh tổ tiên `/tmp/.git`; nhóm materializer vướng “Codex home is inside a repository”; nhóm run/khung không tới được child hoặc thiếu runs trong môi trường HOME cô lập. Đây là lỗi setup/nền đã đối chiếu base, không nhận là regression hoặc pass. `summary.json` lưu thông báo cụ thể từng ca.

- r858_goc_tam_tranh_to_tien_co_git
- t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac
- r15_moi_provider_chi_mot_transport_va_hai_luot_on_dinh
- r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat
- r926_lenh_run_khung_mat_thi_run_json_KHONG_DO_DUOC
- r926_dot_bien_tu_sinh_moi_thanh_phan_regex
- r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC
- r925_rust_log_thua_ke_bi_GHI_DE_khong_noi
- r925_codex_khong_co_khung_thi_KHONG_DO_DUOC_khong_suy_tu_m
- r925_codex_qua_han_van_124_va_giu_khung_da_den
- r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC
- r484_g2_doctor_doc_dung_home_da_materialize
- r484_g2_schema_truoc_freshness_va_home_materialize
- r484_g2_child_khong_nhan_snapshot_va_rac_chan_truoc_probe
- r484_g2_storage_kernel_guardrails
- r484_g2_recovery_probe_rollback_va_snapshot_moi
- r484_g2_probe_isolated_marker_va_refresh
- r484_g2_hook_shell_scrub_truoc_probe
- r484_g8_hook_scrub_kin_voi_bash_env
- r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do
- r484_g7_tu_choi_ghi_dung_ban_da_probe
- r484_g7_auth_doi_truoc_khi_thay_thi_giu_ban_moi
- r927_lenh_run_ghi_effort_va_sandbox_vao_run_json

Bỏ qua10 ca, không tính vào tử/mẫu N/M “đã chạy”:

- t62_qua_han_ma_khong_giet_het_cay_phai_tra_125 — fixture Windows.
- r484_g4_windows_sid_alias_identity — native Windows SID conversion.
- r345_chan_socket_that_ma_than_hook_van_chay_dung
- r345_cac_phep_do_cuc_bo_van_dung
- r345_lop_tham_import_van_co_rang
- r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO
- r347_tham_import_van_song_tren_python_truoc_310
- r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO
- r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia
- r348_dot_bien_bo_isidentifier_lam_ca_dich_DO

Tám ca cuối không dựng được venv/pip trong cấu hình offline. Không thử cài qua mạng. Bốn mutant không đo trên Linux: `g4_windows_sid_alias_not_normalized`, `g4_windows_LA_not_current_owner`, `g2_windows_directory_pin_access`, `124_khi_chau_con_song`. Mẫu số511 đã loại4 này.

## TINH TOAN VEN VA DUNG LUOT

Hash9125 tệp tracked đầu/cuối không đổi; HEAD/spec giữ nguyên; cuối cùng `git status --short --ignored` rỗng. Không sửa mã, index, ref hoặc branch review. Một marker ignored `.claude/.packet_state/session-start.ran` được quan sát sau suite, mtime nằm trong lượt đo. Nó đã được lưu ra `evidence/generated-session-start.ran`, metadata/hash trong `test-side-effect.json`, rồi dọn thư mục rỗng phát sinh. Đây là tác dụng phụ quan sát được trong lúc chạy test; không được khai rằng tuyệt đối chưa từng có ghi trong checkout. Snapshot ban đầu đã hash tracked và xem status thường nhưng **chưa chụp riêng ignored**, nên giới hạn này được công bố, không che bằng final status sạch. Hiện không có delta tracked/untracked/ignored quan sát được; không có test còn đang chạy.

CI exact-head/native Windows/no-sh native chưa đo, không dùng đó làm finding sản phẩm. Không soạn payload credential hoặc nội dung nhạy cảm; chỉ dùng ca có sẵn, script echo/đối số vô hại và mô tả hướng sửa.

Đây là lượt Codex cuối2/2. Verdict vẫn changes_requested; **dừng ở đây**, không tự gọi lượt3, không sửa branch executor hoặc mở write set. `next_role: human/coordinator`; bước tiếp theo thuộc chủ kho theo checkpoint/revision/successor của packet, giữ nguyên các stable finding và evidence trên exact SHA này.
