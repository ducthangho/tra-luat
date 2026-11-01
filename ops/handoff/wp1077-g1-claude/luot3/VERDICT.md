verdict: changes_requested
reviewed_sha: 57e2d4ad9c1e7881c4e4af6776b476abf5c861f7
spec_sha256: eabbb725650addad531429d48801667f2ef05a6090c00123d1d4146c7b89c3f3
Ket qua: 0 P0, 2 P1, 0 P2, 0 P3.

PR #1080, packet #1077 r1/g1, sensitive, lease `wp1077-r1-g2-claude`, lượt Codex 3/4. F4 còn một biến thể PATH rỗng làm đo nhầm executable. F6 là lời khai sai đo được trong commit cuối; không có tác động runtime. Xếp F6 P1 theo rubric riêng của prompt, giống F5 lượt trước.

Base `086f1b7343fc1d778e50797e6c9ca0964b11a755`; tree HEAD `420787eb9f33f0663c6ded28abc216ba20e87b35`. Git diff khớp byte `diff.patch`; numstat khớp `numstat.txt`: launcher +56/-9, test +213/-15; tổng +269/-24, net +245, hai tệp, chưa tính HINT.

Danh tính theo `runs/ceb22db5/run.json`: provider `openai_codex`, execution_surface `codex_cli`, transport `machine`, run_id `ceb22db5cc524d8f901d95cd0b7abc0d`. Reviewer Codex theo phân công, context độc lập executor Claude; không suy model từ Co-Authored-By. Run.json không attest tên model phục vụ. Không push/fetch, đăng GitHub hay dùng credential thật. Các CLI trong phép đo bổ sung đều là fixture; REST/MCP remote được stub.

Môi trường: Linux x86_64, Python 3.13.16, Bash 5.2.21, glibc 2.39, uid0, `/bin/sh -> dash`. Đã kiểm `/tmp/.git` tồn tại, `/var/tmp` chỉ đọc; không xóa để làm xanh test. Skill runtime đã được đọc; không có tool environment_status callable. Không có receipt CI remote trên exact HEAD.

Quyết định chủ kho ngày 31-10-2026 trong prompt thắng phạm vi rộng cũ: `_git` và `_do_codex_song` chuyển #1083. KHÔNG tính hai đường đó thành finding mở của packet này. Vẫn kiểm riêng các lời khai phạm vi mới.

## LENH VA PHAM VI BANG CHUNG

Các lệnh dưới chạy từ `cay-kho/`, đọc HEAD và ghi hiện vật ngoài cây review:

```sh
# S: shell/libc thật, argv/$0, BOM/rỗng/ELF, timeout, doctor rg/git
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/semantics.py
# P: ca r1077, phản chứng base, replay mutant nghiêm ngặt và F4
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/checks.py
# I: AST toàn launcher, Git objects, commit, numstat, ruff, t111 lịch sử
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/audit.py
# X: các nhánh capability bằng CLI giả, không gọi dịch vụ thật
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/paths.py
# E: env=None/{} và PATH, nguồn lỗi lịch sử, policy AST không đổi
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/extra_claims.py
# L: trace phép so sánh trong t103, chỉ sửa bản hàm trong bộ nhớ
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/claim_trace.py
```

S/P/I/X/E/L trong các bảng là chính những lệnh này. Output chi tiết lưu ở `evidence/*.json` và log cùng tên. Bash oracle dùng `"$@"`; libc oracle dùng `ctypes.CDLL(None).execvp`, không dùng `os.execvp` của Python làm đại diện glibc. Mutant và bản sao chẩn đoán nằm ngoài `cay-kho/`.

Bộ đầy đủ thực sự đã chạy bằng `python3 .claude/dev/launcher_test.py` và `python3 .claude/dev/launcher_test.py --dot-bien`, qua runner lưu rc thật của test. Tái lập từ `cay-kho/`:

```sh
python3 ../evidence/run_suite.py head .
python3 ../evidence/run_suite.py mutation . --dot-bien
python3 ../evidence/run_suite.py base /tmp/cr1077-3-base
python3 ../evidence/run_suite.py e6 /tmp/cr1077-3-e6 --dot-bien
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/replay_environment.py head
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/replay_environment.py base
```

Base và e6 được xuất đầy đủ bằng `git archive` từ object cục bộ ra hai thư mục `/tmp/cr1077-3-*`, không checkout hay sửa branch review. Runner lọc môi trường không mang credential và ghim `PIP_NO_INDEX=1`, `PIP_DISABLE_PIP_VERSION_CHECK=1`, `UV_OFFLINE=1`. JSON runner chứa rc của bộ test; rc wrapper không được dùng thay rc test.

Giới hạn phép chạy: lượt full suite đầu chưa ghim PIP_NO_INDEX; fixture `_r345_venv` có lời gọi `pip install` nên có thể thử mạng trước khi thất bại trong sandbox offline. Đây là thiếu sót của reviewer đối với ràng buộc không gọi mạng; không dùng lượt đầu để chứng minh tuân thủ offline. Đã chạy lại HEAD/base/mutation với runner offline, cùng kết quả headline. Hai lượt đầu dùng chung tên log nên raw `head.log`/`base.log` có đoạn ghi đè xen nhau; không dùng số dòng trong chúng làm bộ đếm. Đã replay riêng đủ 23 ca lỗi/bỏ qua với log và JSON riêng, xác nhận chính xác tên/status. Không có phép đo từ dịch vụ bên ngoài hoặc credential thật trong kết luận.

## DOI CHIEU TUNG FINDING CU

| Finding | Đo lại | Trạng thái |
|---|---|---|
| F1: bỏ probe capability | I/X/P: Codex status, ba lệnh llm, hai lệnh gh, Claude MCP đều đi helper. Git/delegate live vẫn lỗi khi thiếu shebang, xanh khi thêm shebang. Helper :2939–2942 và test :9376–9380 nêu rõ ngoại lệ | Phần trong phạm vi đã sửa. Hai đường còn lại chuyển #1083, KHÔNG giữ F1 mở hoặc đếm lại thành finding mới |
| F2: đồng nhất Bash và sh | S: bashism Bash0, glibc/helper127. Docstring :2927–2930 và comment :9238 khai đúng giới hạn sh | ĐÓNG lời khai cũ; khác biệt Bash vẫn có thật nhưng đã được công bố đúng hợp đồng M1 |
| F3: thiếu chốt argv | P: ca argv/env xanh; mutant bỏ đối số chết đúng TinHieuChotCa/lost arguments | ĐÓNG |
| F4: bỏ wrapper đầu | S/P/X: PATH tuyệt đối đã sửa; PATH `:<later>` vẫn which=`cli`, Bash/glibc FIRST, helper LATER, llm sai credential | CHƯA ĐÓNG, giữ ID F4 |
| F5: +228 dòng sai | I: BASE..dcfb +236/-19 đúng lời đính chính; BASE..e6 +56/-9 và +211/-15 = +267/-24, đúng tại e6; HEAD thêm2 dòng thành +269/-24 | ĐÓNG theo cơ chế đính chính đã được chấp nhận. Handoff tương lai không nằm trong bundle nên chưa xác nhận đã ghi ở đó |

## BANG NGHIEM THU

| Tiêu chí | Lệnh | Output thực đo | Đạt? |
|---|---|---|---|
| M1: helper, guard ENOEXEC/POSIX/sh, một retry, cùng tham số | P/S/E; I | EACCES giữ nguyên lỗi/1 spawn; mock nt/sh-vắng 1 spawn; lỗi retry giữ nguyên/2 spawn; argv/env/stdin/timeout/encoding giữ nguyên; rỗng/rc1 hỏng, timeout retry có cờ True | ĐẠT nhánh retry được giao. Phần giải tên trần thêm trong diff còn F4. Native Windows/sh-vắng không nhận pass |
| M2: version và auth dùng helper | I :2989/:3041; P | Cả hai gọi helper; mutant auth quay lại subprocess chết đúng ca(d) | ĐẠT theo phạm vi đã thu hẹp, không suy thành phủ `_git`/live |
| M3(a–d) | P/S | 4/4 ca đặc tả xanh: rg/git không bi_che, wrapper hỏng vẫn12/BI_CHE, thiếu x False, auth có output True | ĐẠT POSIX; nhánh skip Windows đã đo bằng mô phỏng |
| M4: bốn mutant đúng đích | Full mutation; P | Bốn mutant bắt buộc chết2/2,1/1,1/1,1/1;5/5 cặp là TinHieuChotCa. Cả9 mutant wp1077 chết13/13 cặp đúng bang | ĐẠT, không tín dụng lỗi ngoại lai |
| A1: full suite/base delta0 và mutant mới đúng đích | Full suites; replay môi trường | HEAD 300/313, tổng323/bỏ10/hỏng13; base 291/304, tổng314/bỏ10/hỏng13; cùng tên lỗi/bỏ qua. Mutation511/511, không đo4 | ĐẠT delta theo ngoại lệ môi trường, KHÔNG khai full suite xanh. Chín ca thêm đều qua |
| A2: base làm(a),(d) đỏ | P, ca HEAD chạy source base; S đo git riêng | (a) TinHieuChotCa/doctor12 BI_CHE; (d) TinHieuChotCa/auth False OSError; git riêng base12/HEAD0 | ĐẠT đúng lý do |
| A3: doctor không shebang đầu PATH | S, lenh_doctor thật | rg/git: base12 BI_CHE/chọn LATER; HEAD0/co=True/version FIRST/không bi_che | ĐẠT tái hiện cô lập từng công cụ. Lọc CONG_CU, tắt KHA_NANG remote; không coi là hạ tầng doctor thật đã được chứng nhận |
| A4: Ruff/diff/doctrine/CI | I; Ruff HEAD/base; `git diff --check BASE HEAD`; `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | Ruff0.17.1: cả hai rc1/cùng5 F841/delta0; diff-check rc0; doctrine rc0/10 tệp/0 vi phạm; không có receipt CI exact-head | ĐẠT ba phép cục bộ; CI KHÔNG ĐO ĐƯỢC, không suy xanh hoặc chưa từng chạy |

## BANG DO

Cách tìm: đọc toàn bộ471 dòng diff, diff-tu-luot2, message HEAD và hai commit sửa sau lượt2; rà code/comment/docstring/test/DOT_BIEN/số định lượng. Sau đó kiểm kê AST toàn launcher, truy ngược từ CONG_CU/KHA_NANG qua wrapper tới spawn và delegate runpy. Đối chiếu từng F1–F5, không chỉ dùng danh sách hàm do test cấu trúc tự khai. `inventory.json` lưu call-site; `claims.json` lưu message/numstat/Git object/Ruff. Các giới hạn provenance được ghi riêng, không dùng metadata thay phép đo.

| Khẳng định | Diff/commit khai | Đo được (lệnh/output) | Khớp? |
|---|---|---|---|
| Nguồn lỗi ENOEXEC trên master2bcd8f3 | Helper :2924–2927 | E xuất object2bcd: version rg/git False/Errno8; S base doctor12 BI_CHE | CÓ về lỗi chạy. Attribution review #823 không xác thực qua mạng |
| sh/glibc và Bash có thể khác | :2922/:2927–2930, test :9238 | S: bashism Bash0, glibc/helper127; script POSIX cùng0 | CÓ giới hạn mới, F2 đóng |
| Chỉ ENOEXEC được retry; PermissionError/mất file không retry | :2930–2932/:2954 | P/S:0644 khi root errno13,1 spawn; mock giữ nguyên đối tượng lỗi | CÓ |
| Windows giữ nguyên | :2932–2933 và hai guard nt | P:nt1 spawn; X:8 ca trả BO QUA shell POSIX khi mô phỏng | CÓ logic; native KHÔNG ĐO ĐƯỢC/ngoài phạm vi |
| Retry một lần, cùng tệp/argv/env/stdin/timeout/mã hóa; phân loại như thường | :2933–2934/:2956, hai caller | P/S:2 spawn khi retry lỗi; `$0` và đối số/env đúng; rỗng/rc1 False, timeout True; mutant từng kwarg/argv chết bang | CÓ khi helper nhận đúng tệp; F4 xảy ra trước đó |
| Giải tên TRƯỚC lần đầu để không chạy bản sau | :2936–2938/:2947–2949; e6 F4 | S:absolute PATH raw subprocess LATER, helper/Bash/glibc FIRST. Empty entry: helper LATER, Bash/glibc FIRST | CHƯA ĐÚNG, F4 còn mở |
| PATH lấy từ đúng env, không tìm thấy giữ tên trần | :2948–2949 | E:None dùng `/INERT-PARENT`,{} dùng `/bin:/usr/bin`,child dùng `/INERT-CHILD`; mutant `moi or os.environ` chết bang | CÓ |
| `sh TÊN` không tra PATH | :2938, docstring test llm | S sh_command_file:dash rc2/cannot open khi cli chỉ có trong PATH | CÓ trên sh của container; không suy cho mọi shell/OS |
| Phạm vi CLI được liệt kê, hai ngoại lệ chuyển #1083 | :2939–2942; test :9376–9380; e6 F1 | I/X:7 hàm liệt kê không spawn trần, `_git` và delegate vẫn thô và được khai rõ; mutant cấu trúc chết bang | CÓ phạm vi mới, không lặp lời khai mọi probe |
| Wrapper llm giữ utf8/replace/DEVNULL/env/timeout như utility cũ | :2959–2965; t121 đổi seam | I/P/X:3 lệnh llm đi helper, fixture keys/prompt CO_CREDENTIAL/DUNG_DUOC; kwargs được giữ | CÓ với caller hiện dùng, không khẳng định toàn bộ API utility cũ |
| Helper fixture755/mode644; đầu không shebang, sau shebang | :9239–9255 | P/S tạo và chạy tệp thật;644 EACCES; HEAD nhận FIRST | CÓ |
| Các ca M3 đúng trạng thái | :9259–9304 | P4/4 xanh; base(a)(d) đỏ; mutant permission/auth/rc đúng đích | CÓ với fixture POSIX |
| Ca argv/env khóa đối số có khoảng trắng | :9308–9327 | P neutral xanh/mất argv đỏ; S `$0`,argc2,`two words`,env nguyên vẹn | CÓ, F3 đóng |
| Codex status/llm không shebang chạy được | :9331–9371 | P/X absolute:CO_CREDENTIAL; mutant spawn thô TinHieuChotCa | CÓ cho fixture, không chứng minh hết PATH/F4 |
| Ca mới không bỏ wrapper đầu | :9397–9408, mutant PATH | P test sẵn xanh và mutant không resolve đỏ; S phần tử rỗng vẫn LATER | Ca có răng nhưng chưa khóa F4 còn lại |
| Stub nhận argv[0] resolve/path= | t103/t111/t113/t115; t121 đổi seam; hai mỏ neo mutant cũ cập nhật | Full mutation511/511; P t111 chết đúng assertion. t115 vẫn kiểm tuple argv/kwargs chính xác sau lọc basename | CÓ; không phát hiện mutant cũ sống do nới stub |
| Tại e6 mutation510/511; t111 sống do không khớp tên trần; HEAD sửa rồi chết đúng assertion | HEAD commit | I:e6 t111 SURVIVED0/1; full e6 rc1/510/511, chỉ mutant này SAI; P HEAD TinHieuChotCa; full HEAD511/511 | CÓ, đo lại cả aggregate lịch sử |
| t103/t113 không so tên lệnh | Câu cuối HEAD commit | AST t103 :3577 có Compare `cmd[:2]==['gh','api']`; L trace thực sự so2 lần/đều False. t113 không so | KHÔNG, F6. Hai nhánh t103 cùng Rc(0), không ảnh hưởng hành vi |
| +267/-24 tại e6; đính chính dcfb +236/-19 | Message e6 | I:git numstat đúng từng tệp/từng head; final HEAD+269/-24 | CÓ; F5 đóng, không lấy số e6 gán cho HEAD |
| Không đổi BI_CHE, ứng viên, budget/timeout | Spec giới hạn | E:AST BASE/HEAD của `_AP_DUNG_BI_CHE`,CONG_CU,hai resolver,_tran_doctor,PROBE_TIMEOUT đều bằng nhau | CÓ về chính sách; không suy helper chọn đúng mọi executable |
| Identity Co-Authored-By/Claude-Session, CI và số đo môi trường executor | Git/provenance | Chỉ metadata, không attestation hoặc receipt CI exact-head offline | KHÔNG ĐO ĐƯỢC độc lập; không dùng nâng assurance hoặc pass native |

## KIEM KE HET DUONG PROBE VA SPAWN

| Đường | Call-site HEAD → spawn | Phạm vi/kết quả |
|---|---|---|
| CONG_CU:git,python3/python/py,claude,codex,rg,bash,gh,npm,node,llm,agy,actionlint,shellcheck | doctor5050/5067 → version2989 → helper2952/2956 | Trong packet, đã nối; BI_CHE vẫn chỉ rg/git |
| Auth CONG_CU:Claude auth status,agy models; retry/cache | doctor5101/5112 → auth3041 → helper | Trong packet, đã nối; `_xac_thuc`3010 cũng hưởng helper dù doctor dùng API bốn phần tử |
| Antigravity capability | 4107 auth/cache,4125 version → helper gián tiếp | X absolute DUNG_DUOC; resolver ứng viên vốn bỏ phần tử PATH rỗng không đổi, không gán sai lệch có trước đó thành regression helper |
| Codex status | 3936 → helper | X absolute CO_CREDENTIAL; which có thể trả tên trần khi PATH entry rỗng, vướng F4 |
| Codex live | 3989/3997 → `_do_codex_song`3858 → runpy codex_cred.py `_kiem_song`:197 | CÒN subprocess thô. X thiếu shebang False/OSError, thêm shebang True/marker. Ngoài packet theo #1083, fixture không dùng credential thật |
| llm version/keys/prompt | 4042/4050/4064 → helper llm2964 → helper chung | X absolute xanh; PATH rỗng sai credential F4; prompt là CLI giả |
| GitHub Git và workspace | 4565 ls-remote,4601 remote get-url; tim_workspace1102 → `_git_mot_dong`302 → `_git`286 | CÒN subprocess thô; X không shebang127/Errno8, thêm shebang0. Chuyển #1083, không đếm finding |
| gh auth/api kho | 4573/4634 → helper | X absolute DUNG_DUOC,PATH rỗng CHUA_XAC_THUC; REST/MCP stub offline |
| Claude MCP | 4375 → helper | X absolute khoe/Connected,PATH rỗng khong_do_duoc; chỉ chẩn đoán MCP, không tự chứng minh thao tác kho |
| Doctor kiểm hook/launcher cũ | 4762/4810 git show → `_git`286 | Còn thô, cùng ngoại lệ #1083, không gom thực thi hook vào packet |
| Claude capability,hook-da-chay,module Python,UTF8/path,REST/MCP endpoint | Đọc file/env/marker,importlib hoặc HTTP; không spawn CLI riêng | Không có subprocess ENOEXEC khác để vá; HTTP thật không dùng trong phép đo |
| Check/run và utility | `_probe_spawn`1144 → utility319; JSON utility333; Git remote/root/head/ref/status; Popen2299 | Ngoài phạm vi. JSON utility không có caller nội bộ trong launcher hiện tại |
| Process-control | ps371/455/508/706,taskkill883 | Không phân loại công cụ DUNG_DUOC/THIEU/BI_CHE; không phải probe cần fallback |
| Hook phiên thực thi,installer,Windows | Ngoài hai tệp diff; fixture cũ có chạm tới | Spec loại rõ, không mở finding ở đây |

Sau khi lần theo wrapper/delegate, không thấy spawn trần nào khác trong phạm vi chủ kho giữ lại. F4 là chọn nhầm tệp trước spawn, không phải một call subprocess trần bị bỏ quên.

## BANG TEST

| Bộ | N/M,rc thật | Bỏ qua/giới hạn |
|---|---|---|
| HEAD full | 300/313 đã chạy qua; tổng323;13 hỏng;rc1 | 10 skip, không khai323/323 |
| Base full cùng điều kiện | 291/304; tổng314;13 hỏng;rc1 | Cùng10 skip/cùng13 tên lỗi |
| HEAD --dot-bien | 511/511;rc0;tổng515 | 4 không đo trên Linux |
| e6 --dot-bien | 510/511;rc1;tổng515 | Cùng4 không đo; chỉ github_dem_gh_auth_la_lam_duoc_viec giết0/1 |
| Replay23 ca môi trường HEAD/base | Mỗi bên13fail/10skip/0pass,không lệch tên/status | Không cộng replay vào pass suite |
| Chín ca r1077 sẵn tại HEAD | 9/9 | 0skip Linux |
| Chín mutant wp1077 replay nghiêm ngặt | 9/9 mutant,13/13 cặp TinHieuChotCa | Không nhận lỗi vô can làm kill |
| Mutant t111 tại HEAD | 1/1 cặp TinHieuChotCa | Tại e6 cùng mutant sống0/1 |
| Bổ sung M1 | 7/7 neutral; 13 mutant guard/retry/kwargs từng trường/empty/timeout chết đúng bang; E thêm1neutral/1mutant env={} chết đúng bang | Guard nt/sh-vắng là mock; timeout retry đo thật |
| Ca reviewer F4 | HEAD đỏ bang → bản sao sửa xanh → revert đỏ bang | Không phải lỗi fixture |
| HINT ngoài kho | patch -p0 dry-run/apply rc0;10/10 r1077 xanh;mutant mới chết bang;Ruff vẫn5F841 | Chưa áp cây executor; không thay full gate/CI của executor |

4 mutant không đo trên Linux: `g4_windows_sid_alias_not_normalized`, `g4_windows_LA_not_current_owner`, `g2_windows_directory_pin_access`, `124_khi_chau_con_song` (ca t62 chỉ Windows). Không trộn chúng vào tử511.

## BANG SAN

Mỗi dòng có tiền đề độc lập, lệnh và output thật; S/P/I/X/E/L là các lệnh nguyên văn phía trên.

| Hướng/lệnh | Output thật | Phân loại |
|---|---|---|
| 1. Gốc rg/git không shebang;S/P | HEAD0/co=True/FIRST;base12/BI_CHE/LATER;4 ca M3 xanh | KHÔNG PHẢI LỖI: gốc đã sửa |
| 2. Wrapper có output nhưng rc1;S/P | Shell/libc/helper1;hai probe False;mutant ép0 bị ca(b) giết | KHÔNG PHẢI LỖI |
| 3. Thiếu x khi root;S/P | 0644→errno13/không retry;mutant mọi OSError giết đúng(c) | KHÔNG PHẢI LỖI |
| 4. argv/$0/env/kwargs;S/P/E | Cùng đường script,argc2,`two words`,from-env;từng kwarg giữ nguyên;13+1 mutant chết bang | KHÔNG PHẢI LỖI ở hợp đồng đã đo |
| 5. Empty/BOM;S | Empty ba bên0/rỗng,hai probe False;BOM ba bên127,hai probe False | KHÔNG PHẢI LỖI;giữ chính sách output |
| 6. ELF có x sai kiến trúc;S | e_machine /bin/true đổi AArch64:Bash126/cannot execute,libc/helper2/Syntax error;hai probe False | KHÔNG PHẢI LỖI phân loại;không hứa rc Bash bằng sh |
| 7. Timeout lượt sh/lỗi lượt hai;S/P | timeout0.1→version/auth False/qua_han=True,version khoảng0.1s;lỗi retry giữ nguyên/đúng 2 spawn | KHÔNG PHẢI LỖI |
| 8. /bin/sh vắng;P/chroot.json | Mock1spawn/rethrow;chroot thật rc77/PermissionError errno1/Operation not permitted | KHÔNG ĐO ĐƯỢC shell/libc thật trong hệ vắng sh;guard chỉ mock |
| 9. Windows;P/X | Mock nt1spawn;8 ca trả BO QUA shell POSIX khi mô phỏng | KHÔNG ĐO ĐƯỢC native,ngoài phạm vi |
| 10. First/later và empty PATH;S/P | Absolute helper FIRST;empty entry which=cli,helper LATER,Bash/glibc FIRST | LỖI F4,có hậu quả credential trong fixture |
| 11. Capability/delegate độc lập;X/I | Absolute Codex/llm CO_CREDENTIAL,llm/gh/agy DUNG_DUOC,MCP khoe;empty Codex/llm/gh/MCP sai;Git/live vẫn ENOEXEC | F4 cho tên trần;hai đường #1083 chỉ ghi nhận ngoài phạm vi |
| 12. Lời khai và số định lượng;I/L | e6+267/-24,HEAD+269/-24;e6 t111 sống / HEAD chết;t103 thực sự so2lần | LỖI KHẲNG ĐỊNH F6;F5 cũ đã đính chính |
| 13. Environment/gate;replay/Ruff/doctrine | HEAD/base13fail+10skip cùng tên/status;Ruff cùng5F841;diff0;doctrine10/0 | KHÔNG PHẢI HỒI QUY;CI exact-head KHÔNG ĐO ĐƯỢC |

### F4-PATH-rong-van-bo-qua-wrapper-dau [P1] Resolve vẫn trả tên trần, subprocess chạy nhầm executable

TEP/DONG: `.claude/dev/launcher.py:2947`–`:2952`, đặc biệt :2949; hậu quả ở llm4042/4050,Codex3936,gh4573/4634,MCP4375. Test :9397 chỉ dùng thư mục PATH tuyệt đối.

VAN DE: PATH bắt đầu bằng phần tử rỗng nghĩa là cwd. `shutil.which('cli',path=':<later>')` tìm thấy file ở cwd nhưng trả `cli` không có slash. Gán lại chuỗi này chưa cố định đường dẫn. Subprocess lại tra PATH, gặp ENOEXEC ở cwd rồi chạy bản có shebang phía sau; helper không thấy exception nên không retry wrapper đầu. Đây vẫn là F4 lượt2, dù dạng PATH tuyệt đối đã sửa. Lời khai “chạy đúng tệp ấy” :2936–2938 cũng chưa đúng trong biến thể này.

DA THU NGHIEM: S dựng first/cli không shebang echo FIRST,later/cli shebang echo LATER,chdir first,PATH=`:<later>`:which=cli,Bash0/FIRST,glibc execvp thật0/FIRST,helper0/LATER. Fixture llm ở cwd trả llm-FIRST/keys=openai,bản sau llm-LATER/keys=other;HEAD `_do_openai_llm(...,False)` trả CHUA_XAC_THUC/llm-LATER. Ca `r1077_PATH_rong_khong_bo_qua_wrapper_dau` đỏ bằng chính TinHieuChotCa. Bản sao chuẩn hóa đường which tìm được thành tuyệt đối làm ca xanh,9ca cũ vẫn xanh;mutant bỏ chuẩn hóa lại đỏ cùng assertion. X đo thêm hậu quả gh/MCP/Codex bằng CLI giả.

DO TIN: Cao. Có shell/libc thật,phản chứng và mutant đúng lý do,không cần mạng/credential. HINT.patch gợi ý sửa+ca+mutant. Không cần đổi BI_CHE,thứ tự ứng viên hoặc hai đường #1083. Các caller doctor hiện không truyền cwd;phản chứng dùng cwd thật. Nếu mở rộng API hỗ trợ child cwd thì resolver cũng phải xét cwd ấy.

### F6-commit-khai-t103-khong-so-ten-lenh [P1] Commit phủ nhận phép so vẫn được thực thi

TEP/DONG: `git log -1 --format=%B HEAD`, câu “t103/t113 khong so ten lenh”;đối chứng `.claude/dev/launcher_test.py:3577`,hàm lồng chay_kho trong t103.

VAN DE: t103 vẫn đánh giá `cmd[:2] == ['gh','api']`;t113 không so tương tự. Hai nhánh t103 cùng Rc(0),vì vậy câu đúng để giải thích không cần sửa stub là “t103 có phép so nhưng kết quả không ảnh hưởng giá trị trả về”. Đây là khẳng định sai đo được theo rubric prompt,không phải lỗi runtime/credential. Không phủ nhận hiệu lực bản sửa t111.

DA THU NGHIEM: AST ghi Compare :3577 trong commit-t103.json. L nạp bản hàm t103 trong bộ nhớ,chỉ thêm trace ngay trước biểu thức,không sửa repo:test PASS;trace ghi hai lần so `['/usr/bin/gh','auth']` và `['/usr/bin/gh','api']`,cả hai False. t103-trace.json giữ output. Không suy thực thi từ việc grep comment.

DO TIN: Cao về lời khai/phép so;không có tác động runtime được phát hiện. Đính chính trong commit kế/handoff như F5: t103 có phép so dư với hai nhánh giống nhau,t113 không so. Có thể bỏ phép so dư,nhưng không cần đổi hành vi để sửa lời khai.

## HINT VA GIOI HAN

HINT.patch là gợi ý chưa áp trên cây executor. Nó đổi kết quả which đã tìm được thành đường dẫn tuyệt đối,thêm ca F4 và mutant phá đúng bước đó. Dùng `patch -p0` từ gốc cay-kho;đã dry-run/áp trên bản sao ngoài kho:rc0,10/10 ca r1077 xanh,mutant mới chết TinHieuChotCa,Ruff vẫn5F841. Đây không phải full-suite/CI chứng nhận bản sửa executor;executor tự tái dẫn xuất,đo và ghi provenance nếu dùng.

Native Windows,shell/libc khi sh vắng,hạ tầng credential thật và CI exact-head đều KHÔNG ĐO ĐƯỢC. Không biến chúng thành regression hoặc pass. Không tự soạn nội dung nhạy cảm;các fixture đã dùng chỉ echo/version/status và binary sai kiến trúc vô hại.

## CAC CA MOI TRUONG KHONG DO DUOC

Replay độc lập HEAD/base: cùng13ca lỗi và10ca bỏ qua; delta tên/status=0. Chi tiết đầy đủ ở hai tệp `*-environment.json`.

| Ca | Trạng thái | Lý do / phạm vi không đo được |
|---|---|---|
| t62_qua_han_ma_khong_giet_het_cay_phai_tra_125 | BO QUA | fixture nay danh cho Windows; ban POSIX la t63 (chay duoc, khong bo qua) |
| r858_goc_tam_tranh_to_tien_co_git | KHONG DO DUOC (test đỏ) | /var/tmp chỉ đọc (EROFS), sau khi tránh /tmp/.git |
| t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac | KHONG DO DUOC (test đỏ) | /var/tmp chỉ đọc (EROFS), sau khi tránh /tmp/.git |
| r345_chan_socket_that_ma_than_hook_van_chay_dung | BO QUA | KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang) |
| r345_cac_phep_do_cuc_bo_van_dung | BO QUA | KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang) |
| r345_lop_tham_import_van_co_rang | BO QUA | KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang) |
| r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO | BO QUA | KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang) |
| r347_tham_import_van_song_tren_python_truoc_310 | BO QUA | KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang) |
| r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO | BO QUA | KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang) |
| r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia | BO QUA | KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang) |
| r348_dot_bien_bo_isidentifier_lam_ca_dich_DO | BO QUA | KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang) |
| r484_g2_doctor_doc_dung_home_da_materialize | KHONG DO DUOC (test đỏ) | Guard Codex home trong repository hoặc không tới được bước/child sau materializer; cùng lỗi trên base |
| r484_g2_schema_truoc_freshness_va_home_materialize | KHONG DO DUOC (test đỏ) | Guard Codex home trong repository hoặc không tới được bước/child sau materializer; cùng lỗi trên base |
| r484_g2_child_khong_nhan_snapshot_va_rac_chan_truoc_probe | KHONG DO DUOC (test đỏ) | Guard Codex home trong repository hoặc không tới được bước/child sau materializer; cùng lỗi trên base |
| r484_g2_storage_kernel_guardrails | KHONG DO DUOC (test đỏ) | Guard Codex home trong repository hoặc không tới được bước/child sau materializer; cùng lỗi trên base |
| r484_g2_recovery_probe_rollback_va_snapshot_moi | KHONG DO DUOC (test đỏ) | Guard Codex home trong repository hoặc không tới được bước/child sau materializer; cùng lỗi trên base |
| r484_g2_probe_isolated_marker_va_refresh | KHONG DO DUOC (test đỏ) | Guard Codex home trong repository hoặc không tới được bước/child sau materializer; cùng lỗi trên base |
| r484_g2_hook_shell_scrub_truoc_probe | KHONG DO DUOC (test đỏ) | Guard Codex home trong repository hoặc không tới được bước/child sau materializer; cùng lỗi trên base |
| r484_g8_hook_scrub_kin_voi_bash_env | KHONG DO DUOC (test đỏ) | Guard Codex home trong repository hoặc không tới được bước/child sau materializer; cùng lỗi trên base |
| r484_g4_windows_sid_alias_identity | BO QUA | BO QUA native Windows SID conversion |
| r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do | KHONG DO DUOC (test đỏ) | Guard Codex home trong repository hoặc không tới được bước/child sau materializer; cùng lỗi trên base |
| r484_g7_tu_choi_ghi_dung_ban_da_probe | KHONG DO DUOC (test đỏ) | Guard Codex home trong repository hoặc không tới được bước/child sau materializer; cùng lỗi trên base |
| r484_g7_auth_doi_truoc_khi_thay_thi_giu_ban_moi | KHONG DO DUOC (test đỏ) | Guard Codex home trong repository hoặc không tới được bước/child sau materializer; cùng lỗi trên base |

## TINH TOAN VEN VA KET LUAN

So SHA-256 trước/sau của 9,125 tệp tracked: 0 tệp đổi. `git status --porcelain=v1` rỗng; HEAD vẫn đúng reviewed_sha. Source review không bị sửa. Chi tiết `evidence/integrity.json`.

Tái lập HINT trên bản sao: `PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/verify_hint.py` từ `cay-kho/`; output `evidence/hint-check.json`.

changes_requested: F4 còn sai hành vi chọn executable trong phạm vi; F6 cần đính chính lời khai. F1 phần chuyển #1083 không bị tính lại. F2/F3/F5 đã đóng theo bằng chứng và quyết định phạm vi. CI exact-head vẫn KHÔNG ĐO ĐƯỢC.
