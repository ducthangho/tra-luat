verdict: changes_requested
reviewed_sha: 4fa47209b79b28a29e65a42ed08665b2e945c74d
spec_sha256: eabbb725650addad531429d48801667f2ef05a6090c00123d1d4146c7b89c3f3
Ket qua: 0 P0, 1 P1, 0 P2, 0 P3.

PR #1080, packet #1077 r1/g1, sensitive; lease theo chỉ thị `wp1077-r1-g4-claude`, Codex lượt 5/10. **Đề nghị changes_requested: F4 chưa đóng cả lớp phân giải PATH.** Hai biến thể cũ, PATH rỗng và symlink/.., đã sửa thật. Còn hai hậu quả của việc đổi đường tương đối thành tuyệt đối, cùng một hồi quy khi interpreter của bản đầu PATH bị thiếu. F1 về lời khai phạm vi đã đóng. Không tính `_git` và `_do_codex_song` đã chuyển #1083 thành finding runtime của packet này.

Base `086f1b7343fc1d778e50797e6c9ca0964b11a755`; HEAD tree `56420e34b969030fd0d3c51dddf3e228239d8171`. Băm lại SPEC khớp chỉ định; `diff.patch` khớp byte với Git. Numstat thật: launcher **+61/-9**, test **+240/-15**, tổng **+301/-24**, hai tệp, đạt trần **330 dòng thêm**. Không lấy net +277 thay số dòng thêm. Kiểm tra cuối giữ nguyên HEAD và nội dung worktree sạch.

Danh tính trong `runs/016195d4/run.json`: provider `openai_codex`, execution_surface `codex_cli`, transport `machine`, run_id `016195d4bb3c4086a397e551296cc7ff`. Reviewer họ OpenAI/Codex, độc lập context executor Claude theo phân công. Run.json không attest chính xác model/effort phục vụ; không suy chúng từ Co-Authored-By, tên công cụ hay tài khoản GitHub. Không đăng review, fetch, push hoặc gọi công cụ mạng. Mọi phép đo bổ sung dùng CLI giả, HOME/config riêng và môi trường loại credential thừa kế; các lệnh “live” bên dưới chỉ chạy fixture cục bộ.

Môi trường: Linux x86_64, Python 3.13.16, glibc 2.39, Bash 5.2.21, `/bin/sh` là dash. `getconf PATH_MAX .` in **4096**. `/tmp/.git` tồn tại, rỗng; không xóa nó để làm xanh test. `/var/tmp` chỉ đọc. Runner ghim `PIP_NO_INDEX=1`, `PIP_DISABLE_PIP_VERSION_CHECK=1`, `UV_OFFLINE=1`, `PYTHONDONTWRITEBYTECODE=1`. PATH sạch là `/usr/local/bin:/usr/bin:/bin`; t53 vì vậy còn báo thiếu CLI claude/codex, đã đo cùng điều kiện trên base.

## LENH VA HIEN VAT

Các lệnh sau chạy từ `cay-kho/`. Script, log, bản sao base, đột biến và HINT đều ở ngoài cây review. Runner giữ rc thật của tiến trình test trong JSON, không lấy rc0 của wrapper làm pass.

```sh
python3 ../evidence/run_suite.py head .
python3 ../evidence/run_suite.py base ../evidence/base-copy
python3 ../evidence/run_suite.py mutation . --dot-bien
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/checks.py
cc ../evidence/execvp.c -o ../evidence/execvp-glibc
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/semantics.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/edge_cases.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/doctor_edges.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/m1_cases.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/paths.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/audit.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/environment_probe.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/verify_hint.py
```

Tên lệnh rút gọn trong bảng: **P** = checks.py; **S** = semantics.py; **E** = edge_cases.py; **D** = doctor_edges.py; **M** = m1_cases.py; **X** = paths.py; **I** = audit.py; **N** = environment_probe.py; **H** = verify_hint.py. Mỗi tên dẫn tới lệnh nguyên văn ở trên và JSON/log cùng tên trong `evidence/`.

Full runner thực sự gọi `.claude/dev/launcher_test.py` không đối số và với `--dot-bien` bằng Python3. `base-copy` được xuất từ Git object đúng OID bằng `git archive`; không checkout/sửa nhánh executor. Agent `tl_auditor` chỉ đọc ba log dài theo CLAUDE.md bước 5; reviewer chính kiểm lại kết quả và tự thực hiện các phản chứng.

## DOI CHIEU TUNG FINDING CU

| Finding | Đo lại | Trạng thái |
|---|---|---|
| F1 — probe bỏ sót và lời khai phạm vi | P/I/X: các đường CLI được giao nối helper. Helper :2944–2947, test :9376–9379, comment DOT_BIEN :12361 đều nêu `_git`/`_do_codex_song`, #1083 | **Đã đóng phần được giao và lời khai.** Hai đường chuyển #1083 vẫn chưa vá runtime; không tính thành finding packet này |
| F2 — đồng nhất Bash với sh | S: bashism → Bash0/BASH_ONLY, glibc/helper127; docstring và comment nói rõ giới hạn | **Đã đóng lời khai cũ**, không mở lại khác biệt đã công bố đúng M1 |
| F3 — thiếu chốt argv/env | P: ca retry giữ đối số có khoảng trắng và env xanh; mutant bỏ đối số chết TinHieuChotCa. M kiểm từng kwarg | **Đã đóng** |
| F4 — phân giải PATH đổi lệnh/ngữ nghĩa | P: ca hiện tại đỏ ở57e2d4a vì PATH rỗng, đỏ ở1027f85 vì symlink/.., xanh ởHEAD. E/D/H có phản chứng mới | **Hai biến thể cũ đã vá; lớp F4 còn mở**, một P1 dưới đây |
| F5 — khai +228 dòng sai | I: BASE..dcfb011 +236/-19; BASE..e6bf386 +267/-24; HEAD +301/-24 | **Đính chính đúng tại từng head.** Handoff tương lai không có trong bundle để xác nhận đã ghi ở đó |
| F6 — khai t103 không so tên lệnh | I: t103 có `cmd[:2] == ['gh','api']` tại :3577; t113 không so cmd. D trace hai return đều rc0. Message1027f85 đã đính chính | **Đã đóng lời khai cũ.** t111 hiện giết mutant đúng assertion; tại e6bf386 mutant còn sống như message57e2d4a đã khai |

## BANG NGHIEM THU

| Tiêu chí | Lệnh | Output thật | Đạt? |
|---|---|---|---|
| M1 — guard, một retry, giữ argv/kwargs và lỗi khác | M/S/E/D | M10/10 neutral;20/20 mutant TinHieuChotCa. Lỗi direct EACCES/ENOENT/EISDIR giữ cùng đối tượng,1 spawn; retry lỗi2 spawn; mock Windows/sh-vắng1 spawn. Nhưng E cwd4321→errno36; D base DUNG_DUOC/0→HEADKHONG_DO_DUOC/13 | Đạt cơ chế retry; **không đạt bảo toàn lời gọi công cụ**, F4 |
| M2 — version/auth dùng helper | I/P | `_phien_ban`:2994; `_xac_thuc_kem_dau_ra`:3046; mutant auth bỏ helper chết đúng ca(d) | **Đạt trong phạm vi thu hẹp** |
| M3(a) — rg/git tốt không shebang đầu PATH | P/X | HEAD0/co=True/FIRST/không bi_che, cả rg và git. Khi wrapper là bản duy nhất cũng0/co=True | **Đạt fixture POSIX yêu cầu**, không suy mọi PATH đều đúng |
| M3(b) — wrapper lỗi vẫn BI_CHE | P/S | doctor12/BI_CHE; hai probeFalse dù có output rồi exit1 | **Đạt** |
| M3(c) — thiếu bit x không retry | P/M/S | 0644→EACCES13 kể cả uid0; versionFalse/qua_hanFalse. Mutant mọiOSError chết đúng ca(c) | **Đạt** |
| M3(d) — auth không shebang có output,rc0 | P | HEADTrue/Logged in; baseFalse/OSError; mutant bỏ helper chết đúng ca(d) | **Đạt** |
| M4 — bốn mutant bắt buộc đúng ca đích | P/full mutation | Bỏ retry2/2; mọiOSError1/1; auth bỏ helper1/1; bỏ rc1/1. Cả5 cặp đúng TinHieuChotCa. Toàn11 mutant wp1077:15/15 cặp đúng assertion | **Đạt** |
| A1 — full suite, delta môi trường0, mutant mới | Full/N/P | HEAD290/314, tổng324/bỏ10/hỏng24,rc1; base280/304, tổng314/bỏ10/hỏng24,rc1. Cùng24 ID lỗi và10 skip, thêm0/bớt0. Mutation513/513,4 không đo được,rc0 | **Delta0 và mutant mới đạt**; không gọi full suite xanh hoặc 24 lỗi là pass |
| A2 — base làm(a),(d) đỏ | P/X | Hai ca trên sourceBASE đều TinHieuChotCa: rg12/BI_CHE, authFalse/OSError. X đo riêng git:base12/HEAD0 | **Đạt** |
| A3 — tái hiện Issue tại chỗ | X | rg/git:base12, LATER/BI_CHE hoặc coFalse khi chỉ có một wrapper; HEAD0/coTrue/FIRST/không bi_che | **Đạt tái hiện cô lập qua lenh_doctor thật**; lọc CONG_CU, tắt khả năng ngoài ca |
| A4 — Ruff F delta0, diff-check, doctrine, CI exact head | I | Ruff0.17.1: HEAD/base cùng5 F841 hai tệp launcher, cùng12 F821 scripts/tl.py. diff-check0; doctrine0/10 tệp/0 vi phạm | **Các phép cục bộ đạt delta0. CI KHÔNG ĐO ĐƯỢC**: offline, thiếu receipt/workflow run đầy đủ đúng4fa4720 |

Lệnh trực tiếp trong I: `git diff --check BASE HEAD`; `python3 -m ruff check --no-cache --select F --output-format json .claude/dev/launcher.py .claude/dev/launcher_test.py` trên HEAD/base; tương tự cho `scripts/tl.py`; `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .`. Ruff vẫn rc1 vì lỗi sẵn có; delta0 không phải lint0.

## BANG DO

**Cách tìm khẳng định:** đọc hết diff.patch, diff-tu-luot4.patch và `git log -1 --format=%B HEAD`; đọc các message e6bf386/57e2d4a/1027f85; rà code/comment/docstring, số lượng, các từ “mọi/toàn”, ngoại lệ phạm vi, fixture/assertion và anchor DOT_BIEN. I dùng AST toàn launcher rồi lần theo delegate codex_cred.py, không chỉ tin whitelist của ca cấu trúc. `inventory.json` giữ call-site; `audit.json` giữ message, numstat, AST và lint. Đối chiếu hành vi bằng các lệnh khác. Danh sách này không được dùng làm trần để bỏ qua lời khai ngoài bảng.

| Khẳng định | Diff/commit khai | Đo được: lệnh/output | Khớp? |
|---|---|---|---|
| Nguồn ENOEXEC trên master2bcd8f3 | Helper2925–2928, attribution review#823 | X lấy source2bcd8f3 từ Git object:rg/gitFalse/Errno8; base doctor12/BI_CHE | Khớp cơ chế/source; attribution chỉ so artifact, không xác thực qua mạng |
| Bash retry bằng chính Bash; hợp đồng là sh | Helper2928–2931; comment9240 | S:[[ ]]→Bash0/BASH_ONLY, glibc/helper127 | Có, giới hạn công bố đúng |
| Chỉ ENOEXEC retry; lỗi khác/Windows/sh không là tệp thì không retry | Guard2959; M1/M3(c) | M:guard đúng identity/count; mocknt/sh-vắng1 spawn; S direct0644errno13 | Có ở direct invocation; nativeWindows/sh-vắng thật chưa đo |
| Một retry, nguyên argv/env/stdin/timeout/mã hóa | 2957–2961; callers | P:argv/env đúng; M:kwargs hai lượt bằng nhau,20 mutant đúng chốt; S:EOF/replacement/timeoutTrue | Có cho cơ chế retry; helper tự đổi đường trước đó gâyF4 |
| rc≠0 hoặc output rỗng không được nhận tốt ở version/auth | Callers và M3(b)/(d) | S:visible+rc1→False;0byte+rc0→False;stderr-only+rc0→True | Có; không khẳng định mọi classifier capability dùng cùng chính sách |
| subprocess có thể chạy bản sau khi bản đầu ENOEXEC | Helper2936–2938 | S:rawLATER, Bash/glibc/helperFIRST ở nhiều dạng PATH | Có trên nền đo |
| Ghép cwd không chuẩn hóa symlink/.. | Helper2938–2942; messageHEAD | S:link/.. tuyệt đối/tương đối đềuFIRST; P old1027f85đỏ/HEADxanh; mutantabspathđỏ | Có, biến thể F4 lượt4 đã vá |
| Ghép cwd vẫn bảo toàn lời gọi đường tương đối | 2953–2954; mô tả chạy chính tệp ấy | E:cwd4321→errno36, Bash/glibc0; `$0=bin/llm` bị đổi→rc42. D:doctor13 | **Không**, F4: bảo toàn inode trong trường hợp thường chưa đủ |
| Helper chỉ cộng ENOEXEC vào subprocess vốn có | Mở đầu docstring2923; M1 | S:first cóx/interpretervắng:raw/glibcLATER0,helperENOENT2. D:base0/DUNG_DUOC→HEAD13/KHONG_DO_DUOC | **Không**, F4; Bash127 được ghi riêng |
| PATH từ đúng env; env={} dùng default, envNone kế thừa | 2951–2953 | M:env_empty lấyos.defpath, mutant mượn PATH cha đỏ; S:PATHvắng/envNone chạyprintenv/value | Có với dạng đã đo |
| `sh TEN` không tự tìm tệp trong PATH | Helper2941 | S:`/bin/sh cli`, cli chỉ trongPATH/cwd trống→rc2/cannot open cli | Có trên dash thật |
| Caller không truyềncwd=, đường tương đối dùng cwd cha | Helper2942–2943 | I:7 call-site trực tiếp helper,0cwd=; S:relativeFIRST | Có về caller; không biện minh đổi `$0` hoặc độ dài |
| Scope CLI có hai ngoại lệ #1083 | Helper2944–2947; test9376; comment12361 | I toàn AST; X:_git không shebang127/Errno8; liveCodexFalse/OSError; thêm shebang thì đều thành công | Có ở cả docstring và comment mới; không khai hai đường đã vá |
| _chay_probe_llm giữ utf8/replace/DEVNULL/env/timeout như utility | 2964–2969; seam t121 | M:caller kwargs đúng; S:FF→replacement/EOF; X đủversion/keys/prompt | Có cho caller/default hiện tại; utility cũ còn APIstdin/cwd riêng |
| Không đổi BI_CHE, ứng viên, timeout/budget | SPEC ngoài phạm vi | I:AST _AP_DUNG_BI_CHE, _cac_duong_dan, _ten_tran_giai_ra, CONG_CU, PROBE_TIMEOUT_GIAY, _tran_doctor bằngBASE | Có ở chính sách gốc; helper mới vẫn gâyF4 |
| Fixture755/644, đầu không shebang/sau có shebang; các assertion M3/argv | Test9241–9433 | P10/10; X doctor/CLItrace; M4strict15cặp; S quyền0644 | Có; không chứng minh mọi dạngPATH |
| Stub nhậnpath=, so argv[0] đã resolve | t103/t111/t113/t115/t121; anchor mutant cũ | X5/5 ca xanh; D2 returnrc0; Pgithub mutant e6sống/HEADchếtTinHieu | Có, không thấy lỗi runtime mới từ sửa stub |
| t103 cóCompare nhưng hai nhánh Rc(0); t113 không so | Message1027f85 sửaF6 | I:t103Comparecmd tại3577; D:auth vàapi đều trả0 với argv0=/usr/bin/gh; t113 khôngComparecmd | Có |
| Ca symlink/.. đỏ1027f85, mutant mới khóaabspath | MessageHEAD; test9413–9433; DOT_BIEN12375 | P:oldfail/llm-LATER;HEADpass; mutant chếtTinHieu đúng ca | Có |
| Lượt4 có1P1+1P2; comment scope đã sửa | MessageHEAD | ĐầuVERDICT-luot4 đúng; comment12361 nêu trừ_git/_do_codex_song,#1083 | Có theo artifact được cấp |
| Numstat từng head và đính chính +228 | MessageHEAD/e6 | I:dcfb+236/-19;e6+267/-24;57e+269/-24;1027f85+295/-24;HEAD+301/-24 | Có tại từng head; handoff sau review chưa đo |
| Model/session executor, Co-Authored-By, CIgreen | Metadata/acceptance | Không có attestation runtime executor/receiptCI đầy đủ đúngHEAD trong bundle | KHÔNG ĐO ĐƯỢC độc lập; không dùng làm pass |

`$0` với đường tuyệt đối ở S giống nhau giữa Bash/glibc/helper, argc2, đối số và env đúng. Với PATH tương đối, E/D đo được hậu quả phân loại thật; không dùng fixture chỉ in `$0` để kết luận chưa thấy ảnh hưởng.

## KIEM KE TOAN BO DUONG PROBE

CONG_CU: git, python(python3/python/py), claude, codex, rg, bash, gh, npm, node, llm, agy, actionlint, shellcheck. KHA_NANG: codex, claude, github, launcher-phien, hook-phien, hook-da-chay, openai-llm, antigravity. I rà mọi spawn trong launcher và đọc delegate, gồm cả đường không cần ENOEXEC.

| Đường | Chuỗi gọi / spawn tại HEAD | Phạm vi/kết quả |
|---|---|---|
| Version mọi ứng viên, retry timeout | doctor5055/5072→_phien_ban2994→helper2957/2961 | Trong packet; nối helper. BI_CHE vẫn chỉrg/git |
| Auth Claude auth status, AG models, retry/cache | doctor5106/5117→_xac_thuc_kem_dau_ra3046→helper | Trong packet. _xac_thuc3015 cũng hưởng helper dù doctor dùng API4 phần tử |
| AG capability | _do_antigravity4112/auth-cache;4130/version | Qua hai probe chung; Xmodelsfixture→DUNG_DUOC/2model |
| Codex login status | _do_codex3941→helper | Trong packet; Pfixture không shebang→CO_CREDENTIAL |
| Codex live, kể cả nhánh token sắp hết hạn | _do_codex3994/4002→_do_codex_song3885/runpy→codex_cred.py:197 subprocess.run | **Còn thô**. X không shebangFalse/OSError; thêm shebangTrue/marker. Ngoài packet theo#1083; không tính runtimefinding |
| llm version/keys/prompt--no-log | 4047/4055/4069→_chay_probe_llm2969→helper | Trong packet; Xtrace đủ 3lệnh; F4 ảnh hưởng ở đây |
| gh auth status, gh api repos/slug | _do_github4578/4639→helper | Trong packet; Xgh-khoOK/DUNG_DUOC, RESTstub |
| Claude MCP get | _suc_khoe_mcp_github4380→helper | Trong packet; XStatus:Connected→khoe |
| Git ls-remote, remote get-url; workspace/root/head/ref | _do_github4570/4606; _git_mot_dong302 và caller khác→_git286/subprocess.run | **Còn thô**, X127/Errno8. Ngoại lệ_git chuyển#1083, không tính finding runtime |
| Hook/launcher cũ so origin/master | _do_hook_cu4767/_do_launcher_cu4815→_git286/gitshow | Cùng ngoại lệ_git; không sửa hook |
| Claude credential, hook-da-chay, modulePython, path/UTF8/env | File/env/marker/importlib và phép đo nội bộ | Không có executable probe riêng cần fallback bị bỏ quên |
| REST/MCPendpoint | urllib/HTTP _do_rest_github/_do_mcp_endpoint | Không phải exec; Xstub hoàn toàn, không chứng nhận dịch vụ thật |
| _probe_spawn; run/check; utility văn bản/JSON | _probe_spawn1144→utility319; JSON333; lenh_run2299/Popen | Ngoài SPEC; utilityJSON không có caller nội bộ khác trong launcher hiện tại |
| Điều khiển/đo tiến trình | ps371/455/508/706, taskkill883 | Không quyết định trạng thái công cụ DUNG_DUOC/THIEU/BI_CHE |
| Hook thực thi, installer, nativeWindows | Ngoài write set hoặc nhánh loại rõ | Không mở finding runtime ngoài phạm vi |

Không tìm thấy đường spawn CLI thô khác còn nằm trong phạm vi phải nối helper. Điều này không chứng minh helper đúng trên mọi PATH; F4 nằm bên trong đường đã nối.

## BANG TEST

| Bộ | N/M / kết quả | Bỏ qua hoặc không đo được |
|---|---|---|
| HEAD:python3 .claude/dev/launcher_test.py | **290/314**, tổng324, hỏng24, **rc1**,270.976s | 10 ca |
| BASE cùng lệnh/env | **280/304**, tổng314, hỏng24, **rc1**,268.228s | Cùng10 ca; delta ID lỗi thêm0/bớt0 |
| HEAD:--dot-bien | **513/513 đạt**, **rc0**,214.314s | 4 mutant |
| P:10 ca packet | **10/10 xanh** | 0 |
| P:11 mutant wp1077, strict replay | **15/15 cặp TinHieuChotCa** | 0; không nhận Exception khác làm kill |
| P:base(a),(d) | **2/2 đỏ đúng assertion** | Là phản chứng, không gọi là2 test pass |
| M:guard/kwargs/caller | **10/10 neutral**, **20/20 mutant TinHieuChotCa** | Windows/sh-vắng là mock logic, không là nativepass |
| X:5 ca stub sửa | **5/5 xanh** | 0 |
| H:3 ca mới | **3/3 đỏ bằng TinHieuChotCa trênHEAD** | Không cộng vào suiteHEAD |
| H:đối chứng giữ relative | `$0` và cwd dài xanh; mutant khôi phục join/abspath làm từng ca đỏ TinHieu | Chưa sửaENOENT; không là bản vá đầy đủ |
| H:control bỏ prelookup | CaENOENT xanh; mutant khôi phục prelookup làm ca đích đỏ TinHieu | Control làm ca ENOEXECđầu PATH cũ đỏ; không đề xuất làm bản vá |
| H:base ca ENOENT và nửa có shebang của cwd dài | **2/2 xanh** | Chứng minh hồi quy mới |
| H:patch-p0 | dry-run0/apply0 trên bản sao, byte sau áp khớp test dựng từHINT | Chưa áp vào cay-kho |

10 ca BO QUA giống nhau HEAD/base:

- `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125`.
- `r345_chan_socket_that_ma_than_hook_van_chay_dung`.
- `r345_cac_phep_do_cuc_bo_van_dung`.
- `r345_lop_tham_import_van_co_rang`.
- `r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO`.
- `r347_tham_import_van_song_tren_python_truoc_310`.
- `r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO`.
- `r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia`.
- `r348_dot_bien_bo_isidentifier_lam_ca_dich_DO`.
- `r484_g4_windows_sid_alias_identity`.

Các ca r345/r347/r348 trên đây không dùng được venv/pip trong runner offline; t62 chỉ Windows; r484_g4 cần native SID conversion. Lý do nguyên văn từng ca ở `evidence/logs/head.log` và `base.log`.

Bốn mutant không đo được: `g4_windows_sid_alias_not_normalized`, `g4_windows_LA_not_current_owner`, `g2_windows_directory_pin_access`, `124_khi_chau_con_song` (ca đích t62 chỉ Windows). Log mutation không có SAI/lỗi ngoại lai. P vẫn replay strict11 mutant mới vì runner legacy có thể ghi ngoại lệ khác thành kill;15 cặp ở P đều đúng TinHieuChotCa.

24 ID đỏ giống nhau, không tính là pass:

```text
t53_doctor_bao_du_khi_du
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

N đo `_KhoCodex` với home trống: HEAD/base cùng `OSError: Codex home is inside a repository`, `/tmp/.git` vẫn hiện hữu. Hai ca `/var/tmp` cùngerrno30/Read-onlyfile system. Các ca phụ thuộc materializer vì thế bị chặn hoặc không có thư mục runs; r926 còn tự từ chối tín dụng kill do lỗi ngoại lai. t53 ở hai log đều chỉ thiếu `claude,codex` trong PATH sạch. Đây là delta0 cùng điều kiện, không phải bằng chứng các hành vi đó đã được đo đủ.

## MA TRAN PATH / TEN / NOI DUNG

Lệnh S chạy cùng fixture bằng Bash thật, binary C `execvp-glibc` liên kết libc thật, ctypes gọi libc.execvp làm đối chứng thứ hai, subprocess thô và helper. Hai đường glibc cùng kết quả ở mọi hàng đã đo. Khi execvp trả lỗi, wrapper C in errno rồi thoát125: 125 là mã wrapper đo, không phải mã glibc tự quy định.

| Dạng PATH/tên | Bash | glibc execvp | Helper | Nhận xét |
|---|---|---|---|---|
| Tuyệt đối; đầu không shebang/sau shebang | 0/FIRST | 0/FIRST | 0/FIRST | RawPython chạyLATER |
| Phần tử rỗng ởđầu, còn bản sau | 0/CWD | 0/CWD | 0/CWD | RawPython chạyLATER |
| Toàn PATHrỗng hoặc `:` | 0/CWD | 0/CWD | 0/CWD | RawENOEXEC |
| PATHtươngđối first:later | 0/FIRST | 0/FIRST | 0/FIRST | Đúng chọn tệp; `$0` xem dưới |
| `..` thường | 0/FIRST | 0/FIRST | 0/FIRST | Đúng |
| Symlink thư mục/tệp | 0/FIRST | 0/FIRST | 0/FIRST | Đúng |
| Symlink rồi `..`, tuyệt đối và tương đối | 0/FIRST | 0/FIRST | 0/FIRST | Biến thể lượt4 đã đóng |
| Tên có `/`: ./first/cli hoặc đường tuyệt đối | 0/FIRST | 0/FIRST | 0/FIRST | Không tra PATH lại |
| Tên có khoảng trắng | 0/SPACED | 0/SPACED | 0/SPACED | Không tách đối số |
| PATHvắng; envNone+PATHvắng | 0/value | 0/value | 0/value | printenv tìm được trong defaultPATH |
| env=None kế thừa PATHfixture | 0/FIRST | 0/FIRST | 0/FIRST | Đúng |
| Thư mục không đọc/search, uid65534 | KHÔNG ĐO ĐƯỢC | KHÔNG ĐO ĐƯỢC | KHÔNG ĐO ĐƯỢC | Không dropuid được; lỗi trước exec |
| Tệp đầu thiếu bit x, bản sau cóx | 0/LATER | 0/LATER | 0/LATER | Bỏ qua EACCES đúng |
| Đường trực tiếp thiếu bit x | 126 | errno13 | PermissionError13 | Không retry |
| Ứng viên đầu là thư mục hoặc symlink đứt | 0/LATER | 0/LATER | 0/LATER | Đúng |
| Tất cả không tồn tại | 127 | errno2 | FileNotFoundError2 | Không retry |
| Đầu cóx nhưng interpreter shebang vắng | 127 | 0/LATER | FileNotFoundError2 | **F4**, hồi quy so rawPython/base/glibc; ghi đúng khácBash |
| PATHtươngđối, wrapper dùng`$0` chọnmode | 0/FIRST | 0/FIRST | 42/rỗng | **F4**, capabilityCHUA_XAC_THUC |
| cwd dài 4321 byte, PATH `.`, tên ngắn | 0/FIRST | 0/FIRST | errno36 | **F4**, cả tệp có và không shebang |

Đo thêm thành phần PATH dài5000 ký tự: Bash/subprocess/helper chạyLATER; cả hai đường glibc choCWD (fixtureCWD không shebang), lưu trong `semantics.json`. Không suy tương đương toàn execvp từ các hàng xanh, cũng không dùng góc này để yêu cầu chép một hành vi góc của libc. Finding F4 dựa vào ba hậu quả rõ ràng có ca đích ở trên; M1 là bổ sung ENOEXEC, không phải tái tạo toàn bộ nội bộlibc khi PATH vượt giới hạn.

| Nội dung/điều kiện | Output thật của S/M | Đánh giá |
|---|---|---|
| argv status / two words; MEASURE=value; đường tuyệt đối | Bash/glibc/helper0, `$0` cùngđường, argc2, đủ đối số/env | Đúng; relative`$0` có hậu quảF4 |
| ELF cóx, lấy/bin/true đổi e_machine=183(AArch64) | RawENOEXEC8; Bash126; glibc/helper2; version/authFalse | Mã hỏng khác, cùng phân loại hỏng; không finding riêng |
| Tệp0byte | Bash/glibc/helper0/rỗng; version/authFalse | Không nới cho rc0imlặng |
| ChỉBOMUTF8 | Bash/glibc/helper127; hai probeFalse | Không finding |
| Outputvisible rồi exit1 | Cả ba1; hai probeFalse | Không nới rc≠0 |
| Chỉstderr/rc0 | VersionTrue/version-stderr; authTrue/ok | Giữ đọcstdout+stderr |
| Đọcstdin | EOF/rc0; hai probeTrue | DEVNULL được giữ |
| ByteFF không hợp lệUTF8 | U+FFFDversion/rc0; hai probeTrue | errors=replace được giữ |
| Retry /bin/sleep0.25; probe timeout0.1 | VersionFalse/timeout/True; authFalse/timeout/True/rỗng | Timeout áp trên retry |
| sh vắng hoặc làdirectory | Mmock1spawn/giữENOEXEC | Logic đúng; ambientsh-vắng thật chưa đo |
| Windows | Mmocknt1spawn/giữENOEXEC | NativeWindows chưa đo/ngoàiSPEC; mock không thay native |

Không đổi/xóa `/bin/sh` máy chạy. E thử chroot riêng không có sh trong tiến trình con: `os.chroot` bị `PermissionError: [Errno1] Operation not permitted`. N thử drop quyền: setgroups→EPERM1; setgid/setuid65534→EINVAL22. Các hàng thư mục trong S bị lỗi trước phép exec nên chỉ ghi KHÔNG ĐO ĐƯỢC; không nhận làm hồi quy launcher. Mock guard được báo riêng với phép đo thật.

## BANG SAN

Mỗi hướng có lệnh nguyên văn trong khối LENH và output thật trong JSON/log cùng tên. Các biểu hiện lỗi chỉ tính một finding F4.

| Hướng độc lập | Lệnh/output thật | Phân loại |
|---|---|---|
| 1. Đường dài so với tên tương đối ngắn | E/D:cwd4321/PATH_MAX4096; Bash/glibc0; base có shebang: DUNG_DUOC0→HEADerrno36/KHONG_DO_DUOC13 | **LỖI F4 P1** |
| 2. Ngữ nghĩa `$0` | S/E/D:Bash/glibcbin/llm/0; helperabsolute/42; doctorCHUA_XAC_THUC13 | **LỖI F4 P1**, cùng lớp |
| 3. Interpreter đầu PATH vắng | S/D/H:raw/glibcLATER0; base DUNG_DUOC0→HEAD FileNotFoundError/KHONG_DO_DUOC13 | **LỖI F4 P1**, không đồng nhất Bash/glibc |
| 4. Rỗng/relative/../symlink/slash | P/S:đúng các dạng yêu cầu thông thường; old57e/1027đỏ, HEADxanh | **KHÔNG PHẢI LỖI** ở biến thể đã vá |
| 5. Bitx/EACCES và thứ tự ứng viên | S/M:đầu0644→LATER; direct0644→errno13; mutantmọiOSErrorđỏ TinHieu | **KHÔNG PHẢI LỖI** |
| 6. Đồ thịprobe/phạm vi lời khai | I/X:7callshelper; _git127/Errno8; liveCodexFalse/OSError; ngoại lệ đủ 3 chỗ | **KHÔNG PHẢI LỖI MỞ** của packet; runtime#1083 chưa vá |
| 7. Bashism và ELF | S:Bashism0so127;ELFBash126/glibc/helper2; hai probeELFFalse | **KHÔNG PHẢI LỖI** theoM1/giới hạn công bố |
| 8. Empty/BOM/rc1/stderr/UTF8/stdin | S:empty0nhưngFalse;BOM127;rc1False;stderrTrue;replacement;EOF | **KHÔNG PHẢI LỖI** |
| 9. Guard/kwargs/timeout/lỗi retry | M10/10neutral/20strictmutant;S0.1→qua_hanTrue | **KHÔNG PHẢI LỖI** cơ chế retry |
| 10. Tín dụng giết đột biến | P15/15TinHieu;H3caHEADđỏ TinHieu;control chỉ chứng minh phần được nêu | **KHÔNG PHẢI LỖI** tín dụng kill mới |
| 11. Suite/lint/số dòng | N/I:24IDlỗi chung/delta0;5F841+12F821 chung;HEAD+301/-24 | **KHÔNG PHẢI LỖI MỚI**, không gọi suite xanh |
| 12. Quyền thư mục/sh-vắng/nativeWindows | N/E:dropuid/chroot bị chặn; không cóWindows | **KHÔNG ĐO ĐƯỢC** |
| 13. CI và attribution ngoài bundle | I/run.json:thiếu receiptCI/modelattestation đầy đủ đúngHEAD | **KHÔNG ĐO ĐƯỢC**, không suy pass |

### F4-phan-giai-PATH [P1] Pre-resolve làm hỏng lời gọi tương đối và đường tìm kiếm đang chạy được

**TEP/DONG:** `.claude/dev/launcher.py:2953–2954`, `_chay_probe_nhu_shell`; caller chịu ảnh hưởng gồm `_chay_probe_llm` và `_do_openai_llm:4047`. Ca hiện tại `.claude/dev/launcher_test.py:9413` chỉ khóa PATH rỗng và symlink/.., nên vẫn xanh với ba biểu hiện sau.

**VAN DE:** `which` rồi ghép `os.getcwd()` làm nhiều hơn việc ngăn subprocess bỏ qua ENOEXEC. Nó kéo dài tên hợp lệ vượt PATH_MAX, đổi `$0` của wrapper và kết thúc tìm kiếm tại tệp có bit x nhưng interpreter vắng. Với trường hợp cuối, subprocess trước patch và execvp vẫn chạy bản sau khi exec trả ENOENT. Đây là helper/probe llm trong phạm vi đang giao, không thuộc hai ngoại lệ #1083. Giữ ID F4 thay vì đổi ID mỗi lần xuất hiện biến thể mới.

**DA THU NGHIEM:**

1. **Cwd dài:** E tạo cwd dài 4321 byte bằng chdir từng thành phần; PATH `.`, tên `llm` ngắn. Bash/glibc đều rc0/FIRST cho tệp có hoặc không shebang. Helper trả **OSError(errno36/ENAMETOOLONG)** sau khi ghép cwd. Với tệp có shebang, subprocess thô và source BASE vẫn chạy được: đây là hồi quy trực tiếp.
2. **`$0`:** E dùng PATH `bin`, wrapper POSIX phân nhánh theo `$0=bin/llm`. Bash/glibc rc0/FIRST; helper đổi thành đường tuyệt đối, wrapper thoát42, `_do_openai_llm` thành CHUA_XAC_THUC. Không phải mất `$1…`: ca argv cũ vẫn xanh.
3. **Interpreter vắng:** S có tệp đầu với bit x và shebang trỏ interpreter không tồn tại; bản sau có shebang hợp lệ. Raw Python/glibc rc0/LATER; helper trả FileNotFoundError (errno2). Bash rc127 được ghi riêng, không khai mọi shell chạy bản sau. Hồi quy cần tránh là mất một lượt subprocess vốn thành công khi chỉ muốn bổ sung ENOEXEC.
4. **Hậu quả doctor:** D gọi lenh_doctor thật, cô lập capability openai-llm, `doi_kha_dung=True, kiem_song=True`, chỉ chạy CLI giả trả `ok`. Cả cwd dài với shebang và interpreter vắng: **BASE rc0/DUNG_DUOC/ok_kha_dung=True → HEAD rc13/KHONG_DO_DUOC/False**. Case `$0`: HEAD rc13/CHUA_XAC_THUC. Workspace được stub để không trộn lỗi hạ tầng khác; không gọi API thật.
5. **Chốt có răng:** H áp HINT -p0 trên bản sao, dry-run/apply đều rc0. **Ba ca mới đều đỏ bằng TinHieuChotCa**. Ca ENOENT và nửa có shebang của cwd dài xanh trên BASE. Đối chứng giữ đường tương đối làm hai ca `$0`/cwd dài xanh; mutant khôi phục join hoặc abspath làm từng ca đích đỏ bằng TinHieuChotCa. Ca ENOENT xanh ở control tắt prelookup; mutant khôi phục prelookup giết nó bằng chính assertion. Control đó làm ca ENOEXEC đầu PATH cũ đỏ, nên không phải bản vá đề xuất.

**DO TIN:** Cao. Có Bash/libc C thật, ctypes đối chứng, source BASE, JSON doctor thật và ca đích không nhận ngoại lệ ngoài assertion làm kill. Mọi bản sao/fixture ở ngoài `cay-kho/`. Chưa chứng nhận một bản vá sản phẩm đóng đủ các biến thể; không trình bày đối chứng từng phần thành giải pháp hoàn chỉnh.

**Gợi ý vá — ở đâu:** Sửa bước chọn lệnh ngay trong `_chay_probe_nhu_shell`, nơi có tên trần/env/cwd và dùng chung giữa các probe. Không vá riêng llm, đổi BI_CHE hoặc sửa hai đường #1083 để che hậu quả.

**Gợi ý vá — thế nào:** Giữ đường và tên tương đối mà kernel/libc dùng; chỉ ngăn subprocess tự tra PATH tiếp sau ENOEXEC, không ghép toàn bộ cwd hoặc dùng abspath/realpath. Với tên trần, X_OK không chứng minh ứng viên exec được: cần phân biệt lỗi của lượt tìm kiếm với lỗi khi gọi đường dẫn đã chỉ định, tiếp tục đúng lớp lỗi tìm kiếm như ENOENT/ENOTDIR/EACCES, và dừng/chạy lại chính ứng viên khi ENOEXEC. Giữ nguyên quy tắc lỗi khi gọi đường dẫn đã chỉ định, Windows, timeout và kwargs của M1. Giữ relative và chỉ thêm slash cục bộ khi cần là hướng rẻ để đóng `$0`/cwd dài, **nhưng chưa đóng ENOENT**; đóng cả lớp cần đo việc chọn ứng viên bằng lỗi exec thật. Chỉ mô tả hướng sửa sản phẩm vì đây là packet sensitive.

**Gợi ý vá — ca test khóa nó:** `HINT.patch` chỉ thêm ba ca độc lập: `r1077_PATH_tuong_doi_giu_dollar_zero`, `r1077_cwd_dai_khong_keo_dai_duong_da_chay_duoc`, `r1077_PATH_khong_chan_ban_sau_khi_interpreter_dau_bi_thieu`. H giữ kết quả neutral/mutant cho từng chốt. Phải giữ các ca đầu ENOEXEC/PATH rỗng/symlink/.. và thêm DOT_BIEN theo anchor của bản vá thực tế để khóa đủ ba. Không chỉ tắt prelookup: H đã chứng minh cách đó mở lại F4 cũ.

**Gợi ý vá — có thể đẻ ra gì:** Bỏ ghép cwd có thể để which trả tên trần rồi subprocess lại chạy bản sau; normalize có thể phá symlink/..; tự duyệt PATH có thể đổi thứ tự/ưu tiên EACCES, mượn PATH cha khi env={} hoặc nhầm execpath với argv[0]/`$0`. Đo lại ma trận và các chốt errno. HINT thêm **73 dòng test**, là artifact phản chứng: 301+73=374, vượt trần330 trước cả sửa sản phẩm. Executor cần tái dẫn xuất/gọn fixture và comment hiện có hoặc có quyết định ngân sách mới; review này không tự nâng trần.

HINT mang nhãn **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**. Đã áp/chạy thử trên bản sao reviewer; không sửa cây executor, không cấp quyền commit/land. Dùng `patch -p0` từ gốc kho, không `git am` mù. Không có hướng thử nào ở đây cần soạn nội dung pháp luật/nhạy cảm; không tự soạn nội dung ấy.
