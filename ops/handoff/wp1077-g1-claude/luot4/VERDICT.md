verdict: changes_requested
reviewed_sha: 1027f8550014b798504eaa8c8c7035a3040b931f
spec_sha256: eabbb725650addad531429d48801667f2ef05a6090c00123d1d4146c7b89c3f3
Ket qua: 0 P0, 1 P1, 1 P2, 0 P3.

PR #1080, packet #1077 r1/g1, sensitive, lease `wp1077-r1-g2-claude`, Codex lượt 4/4. F4: bản sửa PATH rỗng sinh lỗi chọn executable khác khi PATH chứa symlink rồi `..`. F1 chỉ còn lời khai phạm vi quá rộng trong comment bảng đột biến, xếp P2 theo rubric “khai rộng hơn phép đo”. KHÔNG tính hành vi `_git` hay `_do_codex_song` đã chuyển #1083 thành lỗi runtime của packet này.

Base `086f1b7343fc1d778e50797e6c9ca0964b11a755`; tree HEAD `caa73f0282f514caf9512973ba120d31637cd396`. SPEC được băm lại bằng SHA-256; `diff.patch` khớp byte với Git. Numstat thực: launcher +60/-9, test +235/-15, tổng **+295/-24**, 2 tệp, đạt trần 300 dòng thêm; không dùng net +271 để xét trần. Bằng chứng: `evidence/metadata.json`.

Danh tính theo `runs/46882d3c/run.json`: provider `openai_codex`, execution_surface `codex_cli`, transport `machine`, run_id `46882d3c4101482c8dd4fe3d1b9db994`. Context reviewer độc lập executor Claude theo phân công; không suy model từ Co-Authored-By hoặc tài khoản GitHub. Run.json không attest model/effort phục vụ: phần này KHÔNG ĐO ĐƯỢC độc lập. Không đăng review, push, fetch hoặc gọi dịch vụ ngoài; không dùng credential thật. Các phép đo bổ sung dùng môi trường sạch, CLI giả và stub HTTP/MCP. “llm prompt”/Codex live bên dưới chỉ chạy fixture cục bộ.

Môi trường: Linux x86_64, Python 3.13.16, glibc 2.39, Bash 5.2.21; `/bin/sh` là dash. `/tmp/.git` tồn tại; `/var/tmp` chỉ đọc. Không xóa `/tmp/.git` để làm xanh test. HOME thử nghiệm nằm ngoài cây review, dưới `evidence/`, không kế thừa credential phiên. Pip được ghim `PIP_NO_INDEX=1`, `PIP_DISABLE_PIP_VERSION_CHECK=1`, `UV_OFFLINE=1` ngay từ đầu.

## LENH VA HIEN VAT

Các lệnh sau chạy từ `cay-kho/`. Script/output reviewer đều nằm ngoài cây này. Mã lệnh trong bảng dẫn tới chính lệnh nguyên văn dưới đây; JSON/log cùng tên lưu output thật.

```sh
# P: 10 ca packet, base counterexample, strict mutants, F4 cũ, t111 lịch sử
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/checks.py
# S: Bash/glibc thật, argv/$0, ELF, BOM, rỗng, EACCES, timeout
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/semantics.py
# M: guard/kwargs và 15 mutant bổ sung, chỉ nhận TinHieuChotCa
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/m1_cases.py
# I: AST toàn launcher, Git objects/messages, số dòng, Ruff, doctrine
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/audit.py
# X: doctor rg/git, capability CLI giả, lỗi lịch sử, trace t103
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/paths.py
# F: F4 trước/HEAD/sửa/đảo sửa, PATH tuyệt đối và tương đối
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/f4_symlink.py
# C: lời khai phạm vi và Codex delegate, fixture không có credential
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/scope_claim.py
# E: nguyên nhân môi trường và bản sao chẩn đoán riêng
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/environment_probe.py
# H: tạo HINT, patch -p0 dry-run/apply, đo trên bản sao ngoài kho
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/build_hint.py
```

Các script cuối đều rc0. Lượt nháp đầu P bị lỗi unpack bảng mutant; một mutant nháp M gây IndexError. Đã sửa script và chạy lại; không nhận hai lỗi ngoại lai ấy làm tín dụng giết đột biến. Kết quả dưới dùng JSON/log cuối với loại ngoại lệ của từng ca.

Full suite thực sự gọi `python3 .claude/dev/launcher_test.py` và `python3 .claude/dev/launcher_test.py --dot-bien`. Runner giữ rc thật của tiến trình test trong JSON, không lấy rc0 của wrapper làm pass. Lệnh tái lập:

```sh
python3 ../evidence/run_suite.py head .
python3 ../evidence/run_suite.py mutation . --dot-bien
python3 ../evidence/run_suite.py base ../evidence/base-copy
```

`base-copy`, `e6-copy`, `head-copy` được xuất bằng `git archive` từ object cục bộ tương ứng, không checkout/sửa branch executor. Các mutant/HINT nằm ngoài `cay-kho/`. Không nhận diện “đã chạy Windows” từ mock hoặc ca bỏ qua.

## DOI CHIEU TUNG FINDING CU

| Finding / lớp | Kiểm độc lập tại HEAD | Trạng thái |
|---|---|---|
| F1 — phạm vi probe không khớp lời khai | I/X: version/auth, Codex status, llm, gh, Claude MCP đã nối helper. Helper :2943–2946 và test :9376–9379 khai ngoại lệ đúng. Comment test :12358 còn “mọi probe KHA_NANG”; C xác nhận delegate live spawn thô | Phần CLI được giao đã vá. Hai đường chuyển #1083 giữ disposition ngoài phạm vi, không tuyên bố đã vá. Phần lời khai **CHƯA VÁ**, P2 dưới đây |
| F2 — đồng nhất Bash với sh | S: bashism Bash0, glibc/helper 127; docstring helper và comment fixture nói rõ hợp đồng sh | **ĐÃ VÁ THẬT** lời khai cũ; khác biệt Bash đã công bố đúng M1 |
| F3 — thiếu chốt argv/env | P ca argv/env xanh; mutant bỏ đối số chết bằng assertion ca đó. M kiểm từng kwarg và lỗi retry | **ĐÃ VÁ THẬT** |
| F4 — chọn sai executable đầu PATH | P: ca PATH rỗng mới xanh tại HEAD, đỏ tại 57e2d4a/llm-LATER; mutant bỏ abspath chết đúng ca. F: symlink/.. xanh trên 57e2d4a nhưng đỏ trên HEAD | **VÁ SINH LỖI MỚI** cùng lớp F4, không mở ID runtime rời để quên lịch sử |
| F5 — số dòng +228 sai | I: BASE..dcfb011 +236/-19; BASE..e6bf386 +267/-24 đúng đính chính tại head đó; HEAD +295/-24 | Đính chính đã đo khớp. Handoff tương lai không nằm trong bundle, chưa xác nhận đã ghi ở đó; không dùng số e6 thay HEAD |
| F6 — lời khai t103 không so tên lệnh | I: t103 có `cmd[:2] == ['gh','api']`, t113 không có phép so cmd. X trace hai lần gọi chay_kho đều trả0; hai nhánh cùng Rc(0). Message HEAD đã đính chính đúng | **ĐÃ VÁ THẬT** lời khai; không thấy lỗi runtime mới từ sửa t111 |

Hai lớp còn mở: F4/chọn executable (1 biểu hiện mới, P1) và F1/lời khai phạm vi (1 biểu hiện, P2). Việc chuyển #1083 không được tính là sửa runtime hai đường ấy. Nguồn lượt/head cũ giữ theo các VERDICT-luot1/2/3 được cấp và Git objects trong I.

## BANG NGHIEM THU

| Tiêu chí | Lệnh | Output thực đo | Đạt? |
|---|---|---|---|
| M1 — ENOEXEC/POSIX/sh-file, một retry, giữ tham số, lỗi khác nguyên vẹn | M/S/F | 8/8 neutral;15/15 mutant TinHieuChotCa;  EACCES/ENOENT/EISDIR không retry; nt/sh-vắng1 spawn; retry lỗi2 spawn; kwargs nguyên; timeoutTrue. Nhưng abspath đổi executable ở F | ĐẠT cơ chế retry; **KHÔNG ĐẠT toàn helper** vì F4 trước bước chạy |
| M2 — version/auth dùng helper | I/P | _phien_ban2993, _xac_thuc_kem_dau_ra3045 gọi helper; mutant auth quay lại subprocess chết đúng ca(d) | ĐẠT trong phạm vi thu hẹp, không suy phủ _git/live |
| M3(a) — rg/git tốt không shebang đầu PATH | P/X | HEADdoctor 0/co=True/versionFIRST/không bi_che, cả rg/git | ĐẠT POSIX |
| M3(b) — wrapper lỗi vẫn BI_CHE | P/S | Có output rồi exit1 vẫn doctor 12/BI_CHE; hai probeFalse | ĐẠT |
| M3(c) — thiếu x không chạy lại | P/M/S | 0644→errno13 kể cả uid0, versionFalse/qua_han=False; mutant mọi OSError chết đúng ca | ĐẠT |
| M3(d) — auth không shebang có output | P | ok=True; base False / OSError; mutant bỏ helper chết TinHieuChotCa | ĐẠT |
| M4 — 4 mutant bắt buộc đúng đích | P/full mutation | Bỏ retry2/2; mọi OSError1/1; auth bỏ helper 1/1; bỏ rc1/1. Cả5 cặp là TinHieuChotCa của chính ca | ĐẠT; toàn10 mutant wp1077 hiện có giết 14/14 cặp đúng assertion |
| A1 — full suite, base delta 0, mutant mới | Full runners/P/E | HEAD 291/314, tổng 324/bỏ 10/hỏng 23, rc1; base 281/304, tổng 314/bỏ 10/hỏng 23, rc1. Tên 23 lỗi/10 skip khớp hoàn toàn. Mutation 512/512, không đo 4, rc0 | ĐẠT delta 0 theo ngoại lệ môi trường / yêu cầu mutant mới; **KHÔNG gọi full suite xanh**. 23 ca đỏ môi trường/10 skip không nhận pass |
| A2 — base làm(a),(d) đỏ đúng lý do | P/X | Hai ca HEAD trên source base đều TinHieuChotCa:doctor 12/BI_CHE và authFalse. X đo riêng git base12/HEAD 0 | ĐẠT |
| A3 — tái hiện Issue tại chỗ | X | rg/git:HEAD 0/co=True/FIRST/không bi_che; base12/BI_CHE/chọn bản9.9.9sau | ĐẠT tái hiện cô lập qua lenh_doctor thật; lọc CONG_CU/tắt capability ngoài ca, không chứng nhận toàn hạ tầng doctor |
| A4 — Ruff F delta 0, diff-check, doctrine, CI | I | Ruff0.17.1:HEAD/base cùng 5 F841 trong hai tệp, rc1, delta 0; scripts/tl.py cùng 12 F821; diff-check0; doctrine0/10 tệp/0 vi phạm; RUFF_CONTRACT3[]/rc0 là phép riêng | ĐẠT các phép cục bộ. **CI KHÔNG ĐO ĐƯỢC**:offline/không có receipt run/attempt/checkout/workflow-definition/gate output đúng head; không suy xanh |

Lệnh trực tiếp do I thực hiện: `git diff --check 086f1b7 HEAD`; `python3 -m ruff check --no-cache --select F --output-format json .claude/dev/launcher.py .claude/dev/launcher_test.py` trên HEAD/base; `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .`. Ruff contract không thay bare lint. Bare lint đỏ sẵn chỉ được nhận ở đây theo delta 0.

## BANG DO

Cách tìm: đọc hết diff.patch, diff-tu-luot3.patch, message `git log -1 --format=%B HEAD`, log các commit sửa sau lượt2; kiểm từng code/comment/docstring, fixture/assertion và anchor DOT_BIEN, rà lượng từ “mọi/toàn”, số lượng và ngoại lệ. I duyệt AST toàn launcher, không bắt đầu từ whitelist ca cấu trúc; lần wrapper/delegate đến codex_cred.py và mọi subprocess/Popen. `inventory.json` giữ call-site; `claims.json` giữ messages/numstat/chính sách/lint; C kiểm lượng từ còn sót trong comment. Danh sách này không là trần loại finding; metadata không thay thực nghiệm.

| Khẳng định | Diff/commit khai | Đo được (lệnh/output) | Khớp? |
|---|---|---|---|
| Nguồn ENOEXEC ở master2bcd8f3 | Helper2925–2928 | X lấy source từ object2bcd8f3:rg/gitFalse/Errno8; base doctor 12/BI_CHE | Khớp cơ chế; attribution review#823 không xác thực qua mạng |
| Bash khác glibc/sh khi retry | Helper2928–2931; comment fixture9240 | S:bashismBash0/BASH_ONLY, glibc/helper 127/[[:not found | CÓ giới hạn mới, F2đóng |
| Chỉ ENOEXEC retry; lỗi khác nguyên | Helper2931–2934/2958 | M:cùng đối tượng EACCES/ENOENT/EISDIR,1 spawn; retry lỗi giữ đối tượng thứ2,2 spawn | CÓ |
| Windows giữ hành vi | Hai guard nt; M3 skip | M mocknt1 spawn; X9 ca BO QUA shell POSIX | CÓ logic; native KHÔNG ĐO ĐƯỢC/ngoài scope |
| Retry một lần, cùng kwargs/argv | 2956–2960; hai caller | M kwargs hai lần bằng nhau, argv“two words”;15 mutant đúng chốt; S timeout retryTrue | CÓ khi đã chọn đúng tệp |
| rc≠0 hoặc không output không được nhận tốt ở hai probe | Caller/M3(b)/(d) | S rc1,0 byte, BOM, ELF đều version/authFalse; M empty-output có mutant | CÓ |
| subprocess có thể chạy bản sau khi bản đầu ENOEXEC | Helper2936–2938 | S first:later rawLATER, Bash/glibc/helperFIRST | CÓ trên container; không nói mọi PATH có bản sau |
| Giải PATH/tuyệt đối hóa vẫn chạy CHÍNH tệp which trả | 2938–2942/2953; message HEADF4 | P PATH rỗng đã sửa. F symlink/..:which/abspath khác inode; Bash/glibcFIRST, helperWRONG | **KHÔNG**, F4 |
| Đường tương đối dùng cwd cha, caller không truyền cwd | 2941–2942; message HEAD | I7 call-site trực tiếp helper,0cwd=; S PATH thườngFIRST; F PATH tương đối symlink/..sai | Khớp nhận định caller, chưa chứng minh bảo toàn tệp |
| PATH từ đúng env; không resolve giữ tên | 2951–2953 | M env={} dùng os.defpath, không mượn PATH cha; mutant `moi or os.environ` đỏ; S sh-cli không tra PATH | CÓ nhánh env={}; đường resolve cònF4 |
| sh TÊN không tìm tệp trong PATH như execvp | 2940; testllm | S `/bin/sh cli`, cwd khác, cli chỉ trong PATH:rc2/cannot open cli | CÓ trên dash thật |
| Helper/test cấu trúc đã giới hạn hai đường | Helper2943–2946; test 9376–9379 | I/X/C:7 hàm liệt kê nối helper; _git/live còn thô đúng ngoại lệ | CÓ ở hai docstring |
| “mọi probe KHA_NANG” | Comment DOT_BIEN12358 | C:live không shebang → False / OSError, thêm shebang → True/marker; graph không qua helper | **KHAI RỘNG HƠN PHÉP ĐO**, F1/P2; behavior#1083không đếm |
| llm giữ utf8/replace/DEVNULL/env/timeout của utility | 2963–2969; đổi seam t121 | I kwargs; M giữ từng trường; X version/keys/prompt fixtureCO_CREDENTIAL / DUNG_DUOC | CÓ cho caller hiện tại; không khẳng định tương đương toàn API cwd/stdin của utility cũ |
| Fixture755/644, đầu không shebang/sau shebang | Test9241–9257 | P/S:tệp thật, EACCES644, HEADFIRST, wrapperlỗi12 | CÓ |
| M3, argv/env, Codexstatus, llmtên trần, cấu trúc có chốt | Các ca r1077 trong diff | P10/10 neutral;10 mutant/14 cặp TinHieuChotCa; base(a)(d)đỏ | CÓ fixture hiện tại; không chứng minh mọi cấu trúc PATH |
| Ca PATH rỗng đỏ57e/llm-LATER, mutant mới khóa bước này | MessageHEAD; test 9412–9429 | P previousF4đỏ TinHieuChotCa/llm-LATER; HEAD pass; bỏabspathđỏ cùng assertion | CÓ; chưa khóa symlink/.. |
| Stub nhận path= và argv[0] resolve | t103/t111/t113/t115; t121;2anchor mutant cũ | P:t111 mutant HEAD đỏ assertion/e6sống; full512/512; I ASTstub/kwargs | CÓ; tổng mutant không thay strict replay mới |
| t103 có Compare nhưng hai nhánh Rc(0); t113 không so | MessageHEAD sửaF6 | I:t103 3577Compare, t1130 Comparecmd; X2 returns/đều0, các soFalse với path tuyệt đối | CÓ đính chính mới |
| Lượt3changes_requested2P1 | MessageHEAD | VERDICT-luot3firstlines:0P0/2P1/0P2/0P3, reviewed_sha57e2d4a | Khớp artifact cấp; không suy attestation model |
| +267/-24tại e6, đính chính dcfb+236/-19 | Messagee6 | I numstat từng commit khớp;57e+269/-24; HEAD+295/-24 | CÓ tại từng head, F5 không mở lại |
| Không đổi BI_CHE/ứng viên/budget/timeout | Giới hạn SPEC | I AST BASE/HEAD của _AP_DUNG_BI_CHE, CONG_CU, _cac_duong_dan, _ten_tran_giai_ra, _tran_doctor, PROBE_TIMEOUT_GIAY đều bằng nhau | CÓ chính sách; không suy helper chọn đúng tệp |
| Model/sessioncoauthor, số đo môi trường executor, CIgreen | Gitmetadata/tiêu chí | Không remote receipt/runtime attestation executor trong bundle | KHÔNG ĐO ĐƯỢC độc lập, không dùng pass |

`$0`: gọi đường dẫn tuyệt đối thì S đo Bash/glibc/helper cùng `$0`, argc2, đối số/env nguyên vẹn. PATH rỗng/tên trần: Bash in `./cli`, glibc `cli`, helper đường dẫn tuyệt đối. Không tuyên bố đồng nhất chuỗi `$0` cho tên trần; chuẩn hóa tên để tránh subprocess tra PATH lần hai đã được công bố. Không đo thấy sai phân loại từ riêng khác biệt chuỗi này trong fixture; không suy một pass phổ quát. Lỗi bảo toàn executable có hậu quả được ghi F4.

## KIEM KE TOAN BO DUONG PROBE

Line HEAD lấy từ I/inventory.json rồi đối chiếu bằng X/C. CONG_CU:git, python(python3/python/py), claude, codex, rg, bash, gh, npm, node, llm, agy, actionlint, shellcheck. KHA_NANG:codex, claude, github, launcher-phien, hook-phien, hook-da-chay, openai-llm, antigravity.

| Đường | Chuỗi gọi/spawn | Phạm vi/kết quả |
|---|---|---|
| Version mọi ứng viên CONG_CU | doctor 5054/5071→_phien_ban2993→helper 2956/2960 | Trong packet, nối đúng; BI_CHE vẫn chỉ rg/git |
| Auth Claude auth status, AG models, kể cả retry/cache | doctor 5105/5116→auth3045→helper | Trong packet; _xac_thuc3014 cũng hưởng helper dù doctor dùng API4phần tử |
| Antigravity capability | _do_antigravity4111/auth cache,4129/version→hai probe chung | X DUNG_DUOC/2 model fixture; không spawn thô khác |
| Codex login status | _do_codex3940→helper | X CO_CREDENTIAL fixture không shebang; không paid API |
| Codex live | _do_codex3993/4001→_do_codex_song3862→runpy3884/_kiem_song→codex_cred.py:197 subprocess.run | CÒN THÔ; C thiếu shebangFalse/thêmTrue. Ngoài packet theo#1083,**không runtime finding** |
| llm version/keys/prompt | _do_openai_llm4046/4054/4068→_chay_probe_llm2968→helper | X3CLI fixture chạy được; F4ảnh hưởng tên trần trước spawn |
| gh auth status, gh api repos/slug | _do_github4577/4638→helper | X gh-khoOK/DUNG_DUOC; REST/MCPstub |
| Claude MCP get | _suc_khoe_mcp_github4379→helper | X Status:Connected/khoe; không chứng minh việc kho thật |
| GitHub git ls-remote/remote get-url; workspace/root/head/ref | _do_github4569/4605; tim_workspace1102, _git_mot_dong302→_git286/subprocess.run | CÒN THÔ; X không shebang127/Errno8, shebang0/FIRST. Ngoại lệ#1083, không finding runtime |
| Hook/launcher cũ so origin/master | _do_hook_cu4766, _do_launcher_cu4814→_git286/git show | Cùng ngoại lệ_git, không được sửa hook |
| Claudecredential, hook-da-chay, modulePython, path/UTF8/env | File/env/marker/importlib, không CLI riêng | Không fallback ENOEXEC riêng bị bỏ quên |
| RESTGitHub/MCPendpoint | urllib/HTTP _do_rest_github/_do_mcp_endpoint | Không phải exec; bổ sung stub hoàn toàn, không mạng |
| check/run và utility | _probe_spawn1144→utility319; JSONutility333; lenh_runPopen2299 | Ngoài SPEC; JSONutility không caller nội bộ khác trong launcher hiện tại |
| Process-control | ps371/455/508/706, taskkill883 | Không phân loại tool DUNG_DUOC/THIEU/BI_CHE, không probe cần fallback |
| Hookthực thi, installer, Windows | Ngoài write set/nhánh loại rõ | Ngoài phạm vi, không mở runtime finding |

Sau khi lần delegate, không thấy subprocess thô **khác** còn nằm trong phạm vi giữ lại. Test cấu trúc chỉ khóa whitelist7 hàm của nó; không dùng whitelist chứng minh “mọi probe”.

## BANG TEST

| Bộ | N/M, rc thật | Bỏ qua/giới hạn |
|---|---|---|
| HEAD full | 291/314đã chạy qua; tổng 324;23 hỏng; rc1 | 10 skip, không gọi324/324 |
| BASE full cùng điều kiện | 281/304; tổng 314;23 hỏng; rc1 | Cùng23tênlỗi/10 skip, delta 0; HEADthêm10 ca đều qua |
| HEAD --dot-bien | 512/512; rc0; tổng 516 | 4không đo Linux; chỉ kết quả harness, không chứng nhận mọi mutant lịch sử chết đúng tính chất |
| P:mười ca r1077 | 10/10 | 0skipLinux |
| P:mười mutant wp1077 strict | 10/10 mutant;14/14 cặp TinHieuChotCa | Không tín dụng OSError/permission/import/setup ngoại lai |
| P:base(a)/(d) | 2/2đỏ TinHieuChotCa đúng lý do | Không cộng pass suite |
| P:t111 mutant | HEAD1/1TinHieuChotCa; e6cùngmutant sống | Không chạy lại tổng 511 mutant e6 trong lượt này |
| M:hợp đồng bổ sung | 8/8 neutral;15/15 mutant TinHieuChotCa | nt/sh-vắngmock, không native Windows/tháo sh thật |
| S/X:shell/libc, capability | OutputJSONtừngfixture | libc oracle `ctypes.CDLL(None).execvp`, không `os.execvp` của Python |
| F:symlink/.. | Trước2/2xanh; HEAD 2/2đỏ; hint2/2xanh; revert2/2đỏ đúng assertion | PATHtuyệt đối/tương đối, không hai finding |
| C:phạm vi comment | HEAD đỏ→sửa chữxanh→câu rộng đỏ TinHieuChotCa | Ngoài-scope runtime chỉ chứng minh giới hạn lời khai |
| E:3 ca môi trường đại diện | HEAD/basecùngfail; copychẩn đoán3/3pass | Bỏ guard snapshot ở copy chỉ định nguyên nhân,**không acceptance pass/bản vá** |
| HINT cuối | patch-p0dry-run/apply0;10/10r1077xanh;11 mutant/15 cặp TinHieuChotCa; Ruff cùng 5 F841 | evidence/hint-final-copy, chưa full suite/CI executor |

Bốn mutant bỏ qua: `g4_windows_sid_alias_not_normalized`, `g4_windows_LA_not_current_owner`, `g2_windows_directory_pin_access`, `124_khi_chau_con_song` (ca t62Windows). Không cộng vào tử512.

## BANG SAN

Mỗi hướng có lệnh chạy thật (mã nguyên văn ở LENH VA HIEN VAT) và output độc lập, không chỉ ý tưởng thử.

| Hướng/lệnh | Output thật | Phân loại |
|---|---|---|
| 1. Gốc rg/git không shebang, P/X | HEAD 0/FIRST/không bi_che; BASE 12/BI_CHE, cả2tool | KHÔNG PHẢI LỖI: gốc đã vá |
| 2. Output có nhưng exit1, P/S | Bash/libc/helper 1; doctor 12/BI_CHE; mutant ép0bịca(b)bắt | KHÔNG PHẢI LỖI |
| 3. Permission/errno khác, M/S | 0644EACCES/1 spawn; ENOENT/EISDIRgiữ nguyên lỗi; retrymọilỗiđỏbang | KHÔNG PHẢI LỖI |
| 4. Env/stdin/encoding/timeout/argv, M/P/S | 8neutralxanh;15mutantđỏ; argc2/two words/MEASURE=value nguyên | KHÔNG PHẢI LỖI cơ chế retry |
| 5. PATHtuyệt đối/rỗng/dot/tương đối thông thường, S/P | rawLATER; Bash/glibc/helperFIRST; ca PATHrỗng xanh/mutantđỏ | KHÔNG PHẢI LỖI cho cấu trúc đã đo |
| 6. PATHsymlink/.., F | which/abspathkhácinode; Bash/glibcFIRST; HEADWRONG/CHUA_XAC_THUC; trước 57eCO_CREDENTIAL | **LỖI F4 P1**, hồi quy |
| 7. Lời khai so delegate, I/C | 2docstringcó ngoại lệ; comment 12358“mọiprobe”; livefixtureFalse / OSError | **LỖI F1 P2 lời khai**, behavior#1083không đếm |
| 8. Bashism so sh/libc thật, S | Bash0/BASH_ONLY; glibc/helper 127 | KHÔNG PHẢI LỖI M1:đã khai hợp đồngsh |
| 9. Binary sai kiến trúc/có x, S | ELFAArch64/x86_64:kernelENOEXEC; Bash126, glibc/helper 127; hai probeFalse | KHÔNG PHẢI LỖI phân loại, mã shell khác nhưng đều hỏng |
| 10. Tệp0 byte, S/M | Bash/glibc/helper 0/rỗng; hai probeFalse; mutantnhận rỗngđỏbang | KHÔNG PHẢI LỖI |
| 11. Tệp chỉ BOM, S | Bash/glibc/helper 127; hai probeFalse | KHÔNG PHẢI LỖI |
| 12. Sh-vắng/Windows, M/X | Mock1 spawn/giữENOEXEC;9caBOQUAshellPOSIX | Logic KHÔNG PHẢI LỖI; native / sh-vắng thật **KHÔNG ĐO ĐƯỢC**, không sửaOSđể thử |
| 13. Timeout lượt retry, S/M | versionFalse/timeout/True; authFalse/timeout/True/rỗng; mutanttắt cờđỏ | KHÔNG PHẢI LỖI |
| 14. Capability CLI không shebang, X | Codex/llmCO_CREDENTIAL; llmprompt/AG/ghDUNG_DUOC; MCPkhoe | KHÔNG PHẢI LỖI fixturethường; không suy service thật |
| 15. Stub/claimt103/t111, P/I/X | t111 mutant e6sống/HEAD đỏbang; t103Comparecó thật/2return0 | KHÔNG PHẢI LỖI mới; F6 đính chính đúng |
| 16. Trần dòng/chính sách, I | +295/-24,2 tệp;6ASTkhông đổi; diff-check0; doctrine0 | KHÔNG PHẢI LỖI |
| 17. Môi trường, E/fullBASE | KhoCodexném“inside a repository”; waitingTrue;23fail/10skiptrùngBASE;3 ca copychẩn đoánxanh | KHÔNG ĐO ĐƯỢC phần môi trường, không hồi quy |
| 18. CI/native Windows/identityphục vụ | Không receipt đúng head; không gọi mạng; runtime Linux | KHÔNG ĐO ĐƯỢC, không suy pass |

### F4-chon-sai-executable  [P1]  abspath xóa `..` trước khi kernel giải symlink

TEP/DONG: `.claude/dev/launcher.py:2953`; lời khai :2938–2942; test mới :9412–9429.

VAN DE: `shutil.which` trả đúng executable nhưng `os.path.abspath(tim)` chuẩn hóa `..` theo chuỗi. PATH `<d>/link/../tools`, với `link -> <d>/real/child`, được kernel giải tới `<d>/real/tools`. abspath đổi thành `<d>/tools`, có thể là công cụ khác. PATH tuyệt đối và tương đối đều lỗi. Đây là cùng lớp F4, sinh bởi commit 1027f85 khi vá PATH rỗng.

DA THU NGHIEM: F tạo hai executable không shebang: real/tools/llm in llm-FIRST, keys in openai; tools/llm in llm-WRONG, keys in other. Không có credential thật. Bash / glibc execvp thật cùng 0/llm-FIRST; stat cho inode which/abspath khác nhau. 57e2d4a nhận CO_CREDENTIAL/llm-FIRST; HEAD nhận CHUA_XAC_THUC/llm-WRONG. Copy dùng phép nối cwd giữ nguyên `..` xanh; khôi phục abspath đỏ lại bằng TinHieuChotCa của chính ca, không có lỗi setup. evidence/f4.json có 8 bản đo.

DO TIN: Cao: A/B trên source hai exact heads, oracle độc lập Bash/glibc, cùng fixture; không dựa API/model/credential thật.

GOI Y: Tại dòng 2953, tạo đường có slash bằng `os.path.join(os.getcwd(), tim)` khi tìm được tim, không normpath/abspath xóa ngữ nghĩa symlink/.. . Tim tuyệt đối được join giữ nguyên; tên trần cwd được ghép cwd để subprocess không tra PATH tiếp. Mở rộng chính ca PATH rỗng thêm symlink/..; thêm mutant đưa abspath trở lại. HINT đã đo hướng đó. Rủi ro cần giữ giới hạn: caller tương lai truyền cwd= phải xử lý theo cwd ấy; bảy caller hiện không truyền. Không sửa resolver ứng viên vốn có ngoài hunk này.

### F1-loi-khai-pham-vi  [P2]  comment bảng mutant vẫn nói “mọi probe KHA_NANG”

TEP/DONG: `.claude/dev/launcher_test.py:12358`.

VAN DE: Dòng thêm vẫn là `# Codex lượt 1: F3 (đối số) · F1 (mọi probe KHA_NANG + giải tên trần theo PATH).` Không nhắc phạm vi thu hẹp/ngoại lệ #1083. Helper/test cấu trúc đã khai ngoại lệ đúng; ghi chú này khái quát rộng hơn danh sách mutant/phần đã sửa. Theo chỉ thị lượt 4, phải kiểm mọi lời khai còn trong diff, không chỉ hai docstring. Xếp P2 cho lời khai phủ rộng; không mở lại behavior hai đường chủ kho loại.

DA THU NGHIEM: I/C lần graph _do_codex→_do_codex_song→runpy_kiem_song→subprocess.run ở codex_cred.py:197, không helper. C chạy chính delegate với CLI fixture chỉ echo marker cố định:không shebang → False / OSError, thêm shebang → True / rc0, marker. Ca kiểm lời khai đối chiếu graph/comment:HEAD đỏ TinHieuChotCa; sửa comment “probe trong phạm vi; trừ _git/_do_codex_song, #1083” xanh; mutant khôi phục câu rộng đỏ cùng assertion. evidence/scope.json giữ kết quả/graph.

DO TIN: Cao về phạm vi thật/nội dung comment. Chỉ lỗi độ chính xác lời khai, không thêm runtime finding/đòi sửa file ngoài write set.

GOI Y: Sửa đúng comment 12358 để tham chiếu phạm vi/ngoại lệ đã công bố. HINT giữ runtime hai đường ở #1083. Chốt reviewer có mutant đảo câu rộng, không yêu cầu test CLI mới cho phần ngoài scope. Rủi ro:không được viết “đã phủ _git/live” hoặc dùng sửa chữ tuyên bố nợ #1083 đã đóng.

## HINT VA GIOI HAN

`HINT.patch` là gợi ý theo prompt: **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**. Đã tạo/áp trên bản sao reviewer, không áp lên branch executor; không là quyền commit, approval hay land. Executor phải tái dẫn xuất, kiểm anchor và khai hint_provenance nếu dùng.

H chạy `patch --dry-run -p0 -i <absolute-HINT.patch>` rồi `patch -p0 -i <absolute-HINT.patch>` tại `evidence/hint-final-copy`, cả hai rc0. Mười ca r1077 xanh; mutant abspath giết đúng ca symlink/..; mutant bỏ tạo path tuyệt đối vẫn giết ca PATH rỗng. Cả 11 mutant/15 cặp là TinHieuChotCa. Ruff cùng 5 F841. HINT sửa comment F1, một dòng helper và mở rộng ca/mutant; bỏ một comment dư để tổng BASE..hint đúng **+300/-24** (launcher +60/-9, test +240/-15). Đã đo bằng `git diff --no-index --numstat` từng cặp tệp; rc1 của no-index chỉ báo có diff.

Chưa chạy full suite/CI trên nhánh executor cho hint; không coi hint làm SHA đang review được approve. Đây là lượt 4/4 cuối; verdict không cấp quyền tự gọi lượt 5 hoặc tiếp tục sửa branch.

## CAC CA MOI TRUONG KHONG DO DUOC

`environment-comparison.json` so tên từng ca: HEAD/base cùng 23 fail và 10 skip. Hai ca đầu đỏ vì `/var/tmp` chỉ đọc. Mười một ca r484 liên quan storage/materializer/hook gặp tổ tiên `/tmp/.git`. Mười ca inert Codex/run khác bị cùng guard chặn trước khi tạo run-root: HOME sạch nằm dưới `/tmp`, `_KhoCodex` ném OSError và `_dang_cho_snapshot` đổi thành True. E đo trực tiếp chuỗi này; replay r15/r925/r927 trên HEAD/base cùng đỏ, bản sao chẩn đoán vô hiệu đúng guard ấy 3/3 xanh. Kết quả chẩn đoán không thay test HEAD hoặc đề nghị bỏ guard thật.

23 ca đỏ, chi tiết nguyên văn trong head.log/base.log:

```text
r858_goc_tam_tranh_to_tien_co_git
t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac
r15_moi_provider_chi_mot_transport_va_hai_luot_on_dinh
r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat
r926_lenh_run_khung_mat_thi_run_json_KHONG_DO_DUOC
r926_dot_bien_tu_sinh_moi_thanh_phan_regex
r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC
r925_rust_log_thua_ke_bi_GHI_DE_khong_noi
r925_codex_khong_co_khung_thi_KHONG_DO_DUOC_khong_suy_tu_m
r925_codex_qua_han_van_124_va_giu_khung_da_den
r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC
r484_g2_doctor_doc_dung_home_da_materialize
r484_g2_schema_truoc_freshness_va_home_materialize
r484_g2_child_khong_nhan_snapshot_va_rac_chan_truoc_probe
r484_g2_storage_kernel_guardrails
r484_g2_recovery_probe_rollback_va_snapshot_moi
r484_g2_probe_isolated_marker_va_refresh
r484_g2_hook_shell_scrub_truoc_probe
r484_g8_hook_scrub_kin_voi_bash_env
r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do
r484_g7_tu_choi_ghi_dung_ban_da_probe
r484_g7_auth_doi_truoc_khi_thay_thi_giu_ban_moi
r927_lenh_run_ghi_effort_va_sandbox_vao_run_json
```

10 skip:t62_qua_han_ma_khong_giet_het_cay_phai_tra_125 và r484_g4_windows_sid_alias_identity cần Windows; tám ca sau không dựng được venv/pip khi offline:

```text
r345_chan_socket_that_ma_than_hook_van_chay_dung
r345_cac_phep_do_cuc_bo_van_dung
r345_lop_tham_import_van_co_rang
r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO
r347_tham_import_van_song_tren_python_truoc_310
r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO
r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia
r348_dot_bien_bo_isidentifier_lam_ca_dich_DO
```

Hướng cần tự soạn vật liệu nhạy cảm ngoài fixture sẵn có không được soạn trong lượt này; chỉ mô tả. Không dùng credential thật/remote API để bổ khuyết phần chưa đo.

## TINH TOAN VEN VA TAC DUNG PHU CUA TEST

Snapshot đầu có 9125 tệp ngoài `.git`. Kiểm trước dọn phát hiện bộ test tự tạo đúng một marker ignored `.claude/.packet_state/session-start.ran` (28 byte, SHA-256 `61d94aecf26c119070a67b4b06a4c437ce37a371bf619e50713fdb38dab22185`). Đây là tác dụng phụ của hook từ các phép chạy test; **không tuyên bố cả lượt chưa từng ghi vào cay-kho**. Yêu cầu chỉ đọc đã không được giữ tuyệt đối trong lúc test chạy. Đã lưu metadata sự cố rồi xóa đúng marker/thư mục mới tạo để trả trạng thái đầu; không sửa mã nguồn hoặc index.

`test-side-effect.json` và `integrity-before-cleanup.json` giữ quan sát trước dọn. `integrity.json`/snapshot cuối: HEAD/tree nguyên vẹn, staged/unstaged diff rỗng, status gồm ignored/untracked rỗng, 9125/9125 tệp, **0 delta SHA-256 nội dung**. Trạng thái sạch cuối chỉ chứng minh đã khôi phục, không xóa sự kiện ghi marker. Không thao tác branch executor, push hoặc dữ liệu dịch vụ ngoài.

Verdict `changes_requested` trên exact SHA đã neo: F4 còn lỗi hành vi trong phạm vi; F1 còn lời khai quá rộng. F2/F3/F5/F6 đã đối chiếu như trên. CI exact-head, native Windows và các ca môi trường giữ nhãn chưa đo, không biến thành pass.
