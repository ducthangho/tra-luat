verdict: changes_requested
reviewed_sha: 457e413bff72480004687636ffd02ef2c2b02bb2
spec_sha256: eabbb725650addad531429d48801667f2ef05a6090c00123d1d4146c7b89c3f3
Ket qua: 0 P0, 1 P1, 0 P2, 0 P3.

PR #1080 · packet #1077 r1 · lease wp1077-r1-g5-claude · sensitive · lượt Codex9/10.

**changes_requested.** F7 đã sửa đúng bằng assertion. F4 đã sửa chọn tệp cho script không shebang qua PATH dài, nhưng còn biến thể **shebang + phần tử PATH quá dài KHÔNG RỖNG**: helper đổi `$0`, khiến doctor kết luận CHUA_XAC_THUC trong khi glibc execvp thực tế cho CO_CREDENTIAL. W-1077-1 chỉ miễn đầu vào có phần tử PATH rỗng; không tự mở rộng miễn trừ sang đầu vào dài không rỗng.

Base: `086f1b7343fc1d778e50797e6c9ca0964b11a755`; reviewed tree: `29044d8e4860f9a3d2460b7a80b030645ea29071`. Detached checkout phục vụ review; Git origin khớp kho được giao. `SPEC.md` tự băm khớp hash yêu cầu. Diff tự dựng bằng Git khớp byte `diff.patch`; numstat launcher +56/-9, test +283/-11 = **+339/-20**, trong trần345 theo g5. Không tính trần300/330 cũ như điều kiện còn hiệu lực.

Reviewer: Codex/OpenAI, làm việc trực tiếp qua API/tool shell; không dùng context executor hay agent phụ. Không có attestation độc lập để xác minh model/session/transport từ footer commit. Review là nội dung exact SHA, không phải biên nhận CI hay quyền merge.

Mọi script/log ở `evidence/`, ngoài `cay-kho/`. Bản BASE lấy từ `git archive BASE`, mutant và bản thử hint nằm trong thư mục tạm ngoài cây review. Full suite dùng môi trường tối thiểu, không kế thừa credential; `PIP_NO_INDEX=1`, `PYTHONDONTWRITEBYTECODE=1`, cấu hình Git global rỗng, cùng điều kiện ở HEAD/base. CLI, REST và Git trong phép đo caller là fixture; không gọi mạng, LIVE hoặc credential thật. Các lệnh `python3 -B ../evidence/<tên>.py` dưới đây chạy được từ `cay-kho/`.

## BANG NGHIEM THU

| Tiêu chí | Lệnh | Output thật | Đạt? |
|---|---|---|---|
| M1: helper dùng chung, ENOEXEC/POSIX/có sh, retry đúng1 lần, giữ argv/env/stdin/timeout/mã hóa, không nới lỗi | `python3 -B ../evidence/contracts.py`; `targeted.py`; `matrix.py` |5 contract neutral PASS;4 ca vật lý PASS;12 mutant bổ sung đỏ TinHieuChotCa; version/auth timeout0.1s đều False/qua_han=True; rc1 và đầu ra rỗng đều False | **Đạt hợp đồng retry M1**. Lời khai mở rộng chọn tệp theo glibc chưa đạt toàn bộ: F4 |
| M2: hai probe đích và các caller trong scope dùng helper | `python3 -B ../evidence/audit.py`; `callers.py` | Hai điểm nối2989/3041; AST toàn launcher có38 call site cần kiểm;8 nhóm caller ×2 trạng thái có16/16 parity shebang/no-shebang | **Đạt điểm nối**, không suy phủ2 delegate ngoài scope |
| M3(a): rg/git no-shebang tốt đầu PATH | `python3 -B ../evidence/targeted.py` | Mỗi mục doctor rc0/co=True/phien_ban=1.0.0-khong-shebang, không bi_che | **Đạt** |
| M3(b): rg no-shebang exit1, bản tốt sau | Cùng targeted.py | Ca PASS: doctor rc12/trang_thai=BI_CHE | **Đạt**, không nới rc lỗi |
| M3(c): shebang0644 | Cùng targeted.py; matrix.py | Ca PASS: chay_duoc=False/qua_han=False; EACCES13, không retry | **Đạt** |
| M3(d): auth no-shebang có đầu ra, rc0 | Cùng targeted.py | Ca PASS: True/ok/False/Logged in | **Đạt** |
| M4: bốn mutant bắt buộc chết đúng ca | Cùng targeted.py | Bỏ retry2/2, retry mọi OSError1/1, auth bỏ helper1/1, bỏ rc1/1; **5/5 cặp TinHieuChotCa** | **Đạt** |
| A1: full suite Linux, ngoại lệ môi trường phải delta0 | `python3 -B ../evidence/run_suites.py` → hai lệnh `python3 -u .claude/dev/launcher_test.py` ở HEAD/base | HEAD302/315 đã chạy (tổng325,skip10,lỗi13); BASE291/304 (tổng314,skip10,lỗi13); đúng cùng13 ID lỗi và10 ID skip | **Đạt theo ngoại lệ môi trường A1**: sau loại13 ngoại lệ, HEAD302/302 so BASE291/291; delta lỗi0, thêm11 pass; vẫn ghi riêng10skip, không khai toàn suite xanh |
| A1: mutation mới đúng ca/đúng lý do | `python3 -u .claude/dev/launcher_test.py --dot-bien` qua run_suites.py; `targeted.py`; `merged_guards.py` | Harness **518/518**,rc0;4 nền không đo được; riêng wp1077 **16 mutant/22 cặp,22/22 TinHieuChotCa**;9/9 property của ca gộp chết ở đúng assertion | **Đạt răng của các mutant mới**; không suy suite xanh nghĩa là không có F4 |
| A2: base(a),(d) đỏ | `python3 -B ../evidence/targeted.py` dùng HEAD test + BASE launcher | **2/2 TinHieuChotCa**; doctor rg12/BI_CHE, authFalse/OSError | **Đạt** |
| A3: tái hiện Issue tại chỗ | Cùng targeted.py, gọi lenh_doctor thật với CLI giả | rg/git rc0, co=True, không bi_che; full JSON trong targeted.json | **Đạt fixture Issue**, không khai doctor toàn máy xanh |
| A4: Ruff F delta0 | `python3 -m ruff check --no-cache --select F --output-format json .claude/dev/launcher.py .claude/dev/launcher_test.py scripts/tl.py` trên HEAD và base-copy, audit.py lưu output | Ruff0.17.1; cả hai17 diagnostic: launcher0, test5F841, tl12F821; Counter(code,file,message) delta0, rc1 hai bên | **Đạt delta**, không khai0 tuyệt đối hoặc suy kết quả Ruff pin CI |
| A4: diff check | `git diff --check 086f1b7343fc1d778e50797e6c9ca0964b11a755 HEAD` | rc0, output rỗng | **Đạt** |
| A4: doctrine | `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | rc0: `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` | **Đạt scanner** |
| A4: CI PR xanh trên exact HEAD | Không gọi mạng theo chỉ thị; kiểm bundle/runs và artifact cục bộ | Không có receipt/check-run exact457e413; runs chỉ có prompt/checkpoint/run/stdout/stderr | **KHÔNG ĐO ĐƯỢC**, A4 tổng thể chưa đủ bằng chứng |

## BANG DO

**Cách tìm khẳng định:** tự dựng diffBASE..HEAD và so byte; đọc toàn diff, helper, caller, test mới, các tuple DOT_BIEN và toàn HEAD message `git log -1 --format=%B HEAD`. `audit.py` ghi339 dòng thêm theo hunk, mọi comment thêm bằng tokenize, mọi hàm/docstring giao dòng thêm bằng AST vào `claims-inventory.json`. Đọc thêm các message e6bf386/57e2d4a/1027f85 để xác minh F5/F6 và lịch sử thay thiết kế. Từ graph của toàn launcher truy ngược CONG_CU/KHA_NANG/lenh_doctor và đọc delegate, không lấy danh sách7 hàm trong test cấu trúc làm giới hạn tìm. Bảng nhóm các khẳng định theo nghĩa; thao tác trích xuất tự động không thay phép đo hành vi.

| Khẳng định | Diff khai | Đo được (lệnh/artifact) | Khớp? |
|---|---|---|---|
| Kernel ENOEXEC; subprocess có slash ném, bare có thể chạy bản sau | launcher2924–2926 | targeted BASE(a)/(d) đỏ đúng lỗi; matrix absolute/relative no-shebang chạy FIRST với helper/glibc | Có |
| Hợp đồng glibc/bin/sh; Bash có thể khác | launcher2926; test9237 | matrix bash-syntax: Bash0/BASH_ONLY, helper/glibc127; wrong-arch Bash126, helper/glibc2; /bin/sh thực tế là dash | Có; không đồng nhất Bash với glibc |
| Candidate giữ `<entry>/<name>`, tương đối, `..`, symlink, slash cuối | launcher2927–2930/2945 | matrix và extra_matrix: a/cli, a//cli, link/../cli, native argv0=native, argc2/arg1=two words | Có ở các dạng này |
| Empty candidate exec qua `./name`, fallback ENOEXEC nhận logical `name` | launcher2928–2931/2950–2953 | matrix no-shebang empty `$0=cli`, shebang empty `$0=./cli` so glibc cli; merged guard empty đỏ đúng assertion khi phá fallback | Cơ chế mô tả đúng; **shebang/empty input thuộc W-1077-1** |
| Phần tử quá dài không cuối như empty, cuối bỏ; “chọn tệp theo execvpe glibc” | launcher2922/2928/2943–2950; HEAD message F4 | matrix long-first/middle/twice/no-cwd chọn đúng như glibc với no-shebang; extra_matrix + doctor_long: **PATH dài không rỗng, shebang $0 khác, CHUA_XAC_THUC vs CO_CREDENTIAL** | **Chưa trọn vẹn, F4**. Không tự mở rộng W-1077-1 |
| env=None dùng env tiến trình; explicit env thiếu PATH dùng os.defpath | launcher2941–2942 | matrix env-none, env-missing-PATH, none-missing-PATH: rc0; raw-byte hiện hữu/vắng và ở cuối đều chạy đúng | Có |
| fsencode xử lý surrogateescape, không encode strict | launcher2942/2944; HEAD message F7 | matrix raw-byte-first/last/missing đều rc0; targeted strict mutant đỏ **TinHieuChotCa**, message chứa UnicodeEncodeError như dữ liệu | Có, F7 đã đóng |
| Chỉ6 errno tiếp; ETXTBSY/ELOOP dừng | launcher2929–2930/2946/2954 | matrix: EACCES/ENOENT/ENOTDIR vật lý, ETXTBSY26/ELOOP40 dừng; thiếu interpreter chuyển LATER. Source có đúng6 errno | Có phần đã đo thật; **ESTALE/ENODEV/ETIMEDOUT filesystem thật chưa dựng được**, không nhận source là bằng chứng thực thi chúng |
| Hết search ưu tiên EACCES, còn lại errno cuối | launcher2930/2956–2957 | matrix EACCES+ENOENT→13, EACCES+ENOTDIR→13; ENOENT+ENOTDIR→20, đảo→2 | Có các thứ tự đo. Toàn PATH quá dài: glibc thất bại/errno0, helperENOENT2; cả hai không chạy công cụ/không có bằng chứng nhãn sai, ghi nhận khác diagnostic, không thêm finding |
| Retry đúng argv/env/stdin/timeout/encoding/errors và giữ kết quả lỗi | launcher2953; hai caller2989/3041 | contracts5 neutral,4 physical,12 mutant đúng assertion; targeted argv/env; timeout retry khoảng0.204s cho2 phép đo0.1s | Có; cùng timeout mỗi lượt theo M1, không tuyên bố deadline tổng mới |
| Windows giữ nguyên; không retry khi sh không phải file; không lượt thứ3 | launcher2935–2936/2952 | contracts mock guard đều1spawn/giữ exception; retry-error2spawn; chroot thật125/Operation not permitted | Đạt mock; native Windows/sh-vắng thật **KHÔNG ĐO ĐƯỢC** |
| `_chay_probe_llm`: utf8/replace, DEVNULL/capture, timeout, chỉ probe llm | launcher2959–2965; thay3 caller | callers16/16 parity; contracts exact kwargs; AST không đổi wrapper run cũ | Có thuộc tính nêu rõ; không suy wrapper mới hỗ trợ mọi tùy chọn cwd/stdin của wrapper cũ |
| Nối các probe CLI; giữ phân loại rc/rỗng/auth và --no-log | 9 call site cũ, wrapper llm; t115/t121 | callers8nhóm ×2trạng thái; M3(b)/(c); physical empty/rc1/timeout; llm-live-fixture chỉ script, giữ --no-log qua test hiện có | Có điểm nối. F4 ở chọn/đặt filename trước classifier |
| M3(a–d), argv/env, Codex status, llm tên trần, AST scope | test9240–9400; DOT_BIEN12387+ | targeted11/11 neutral;22/22 mutant assertion; gh/MCP/agy caller độc lập | Có ca đã khai, không suy ca AST bao trùm toàn graph |
| Ca gộp khóa từng property, không chết sớm vì setup | test9402–9470 | merged_guards9/9: symlink-only, long-entry, missing-interpreter, long-cwd, empty$0, relative$0, trailing-slash, ETXTBSY, UTF8 đều đúng marker assertion | Có9 tính chất đã có; **thiếu kết hợp PATH dài + shebang/$0**, HINT chứng minh F4 |
| Scope trừ `_git`/`_do_codex_song`, không “mọi probe” | helper2931–2932; structural9377+; comment DOT_BIEN | audit call graph + đọc codex_cred; lời khai3 nơi đều nêu ngoại lệ | Có, F1 lời khai đã đóng |
| Stub cũ đã gỡ đổi, argv0 lại tên trần | diff t115/t121, các tuple codex/MCP; message01b | history_check.py: AST t103/t111/t113 bằng BASE; t115 chỉ bỏ executable khỏi kwargs so; native argv0=native | Có |
| t103 có so tên với2 nhánh cùngRc0, t113 không so | Đính chính1027f85 đối với57e2d4a | history_check.json ghi `cmd[:2] == ['gh','api']`; đọc thân hai nhánh; AST bằng BASE | Đính chính đúng, F6 đóng |
| F5: dcfb +236/-19; e6 +267/-24 | messagee6bf386 | audit.json tự đo Git từng object:48+188=236;56+211=267 | Đúng; ghi handoff ngoài bundle **chưa đo được**, không tái cáo buộc câu đã đính chính |
| HEAD: lượt8 có1P1+1P2; mutant UTF8 nay bang; +56/-9,+283/-11=339<=345 | HEAD message nguyên văn trong audit.json | VERDICT-luot8 dòng1–4; targeted strict assertion; Git numstat hiện tại | Các con số và assertion **đúng**. Câu sửa F4 chưa đủ đóng lớp theo phản chứng mới |

## KIEM KE PROBE DOCTOR VA SPAWN KHAC

`call-sites.json` lưu38 call site/caller/line, `call-graph.json` lưu graph toàn launcher. Đã rà cả các đường gián tiếp, bảng KHA_NANG và các spawn ngoài doctor.

| Đường quyết định nhãn | Spawn cuối | Phạm vi/kết quả |
|---|---|---|
| CONG_CU --version cho mọi ứng viên | `_phien_ban:2989` → helper2950/2953 | Trong scope, M3(a)/(b)/(c) đạt |
| CONG_CU auth, `_xac_thuc` wrapper, agy models | `_xac_thuc_kem_dau_ra:3041` → helper | Trong scope; agy dùng cache auth nếu đã đo, fallback version cũng cùng helper |
| Codex login status | `_do_codex:3936` → helper | Trong scope; CLI giả nhận no-shebang, có cả negative |
| llm --version/keys list/prompt --no-log | `_do_openai_llm:4042/4050/4064` → `_chay_probe_llm` | Trong scope;16paircaller có parity, F4 vẫn ảnh hưởng đây |
| gh auth status và gh api repos/slug | `_do_github:4573/4634` → helper | Trong scope; Git/REST/MCP stub, gh-kho mới quyết định làm được việc |
| claude mcp get | `_suc_khoe_mcp_github:4375` → helper | Trong scope; env chuẩn hóa; positive khoe, negative hong như shebang |
| Codex --kiem-song | `_do_codex_song:3858` → runpy codex_cred `_kiem_song` → subprocess197 | **Ngoài packet theo chủ kho, #1083**; còn spawn trần, không tính finding; không gọi live |
| Credential preflight doctor | `_chuan_bi_va_bo_snapshot:3221` → materializer → `_probe_snapshot` → codex_cred | Cùng giới hạn delegate chuyển #1083; fixture không có snapshot thật |
| Git ls-remote/remote get-url; tìm workspace; đọc hook/master launcher | `_git:286` dùng subprocess.run trần; `_git_mot_dong` bọc nó | **Ngoài packet theo chủ kho, #1083**, dùng chung run; ghi nhận chưa phủ ENOEXEC |
| Claude credential, dấu vết hook, locale/PATH và Python modules | Đọc file/env/hash/find_spec/import | Không thêm CLI spawn thuộc ENOEXEC |
| GitHub REST và MCP endpoint | urllib HTTP | Không exec CLI; chỉ dùng stub offline trong phép đo |
| `_probe_spawn:1144`, runnerPopen2299 | `_chay_van_ban_an_toan:319` / subprocess.Popen | **Ngoài scope SPEC: launcher run**, không đổi |
| `_chay_json_chat_che:333` | subprocess.run riêng | Không có cạnh gọi trong graph doctor; ngoài probe được giao |
| ps371/455/508/706, taskkill883, cây tiến trình | subprocess.run riêng | Hỏi/quản lý tiến trình, ngoài phân loại khả dụng công cụ của packet |

Không thấy probe CLI **trong phạm vi đã giao** còn spawn trần ngoài helper. Không gọi việc chuyển2 delegate sang #1083 là “đã vá toàn doctor”.

## DOI CHIEU TUNG FINDING CU

| Finding/lịch sử | Trạng thái tại457e413 | Bằng chứng/giới hạn |
|---|---|---|
| F1: sót Codex status, llm, gh/MCP | Đã nối các caller trong scope;2 delegate **chuyển phạm vi** | callers16/16; AST + đọc delegate; `_git`/codex_cred chưa sửa theo quyền chủ kho |
| F1: docstring/comment khai “mọi probe” | **Đã sửa thật** | helper, structural và comment bảng mutant cùng nêu giới hạn |
| F2: Bash đồng nghĩa glibc/sh | **Đã sửa lời khai** | Bashism0/127 và binary126/2 còn khác như công bố; không đổi interpreter trái M1 |
| F3: mất argv vẫn qua test | **Đã sửa thật** | r1077_retry_giu_argv_env PASS; mutant bỏ argv đỏ chính TinHieuChotCa;12 own mutant contract |
| F4 lượt2–6: chọn bản sau/empty/abspath/..symlink/cwd dài/interpreter vắng/ETXTBSY,ELOOP/trailing slash | **Đã vá các biểu hiện ấy** | matrix, permission, extra_matrix, merged_guards; không dùng một assertion chết sớm để nhận tín dụng property sau |
| F4 lượt7: byte ngoàiUTF8 | **Đã vá thật về runtime** | fsencode, raw-byte đầu/cuối/không tồn tại đều đúng |
| F4 lượt7: shebang qua phần tử PATH rỗng | **Chưa vá, miễn W-1077-1** | helper ./cli vs glibc cli; không tính finding cho đầu vào empty |
| F4 lượt8: bỏ entry dài làm chọn LATER thay cwd | **Đã vá no-shebang; lớp còn mở** | long-first/middle/multiple/no-cwd khớp; **shebang qua entry dài KHÔNG rỗng** vẫn đổi$0, finding bên dưới |
| F5: khai sai số dòng dcfb | **Đã đính chính đúng** | Git236/19 và e6 267/24; handoff không có trong2-file bundle |
| F6: phủ nhận t103 so tên | **Đã đính chính đúng** | AST so tên thật, cả2 nhánh Rc0; t103/t111/t113 hiện bằng BASE |
| F7: mutant UTF8 chết bằng exception ngoài assertion | **Đã vá thật** |22/22 cặp đúng TinHieuChotCa; strict mutant mang UnicodeError thành dữ liệu rồi bang; mergedUTF8 marker đúng |

Sổ còn mở: **1 lớp F4 / 1 biểu hiện tính finding**. Không mở lại F1 ngoài phạm vi, F7, hoặc đầu vào empty được miễn trừ.

## BANG TEST

| Bộ/lệnh | N/M và mã thoát | Bỏ qua/giới hạn |
|---|---|---|
| HEAD `python3 -u .claude/dev/launcher_test.py` | **302/315**, rc1; tổng325/lỗi13 | 10skip;13ca không đo được trong môi trường này, đối chiếuBASE bên dưới |
| BASE cùng lệnh/môi trường | **291/304**, rc1; tổng314/lỗi13 | Cùng10skip/cùng13IDlỗi,delta0 |
| HEAD `python3 -u .claude/dev/launcher_test.py --dot-bien` | **518/518**, rc0; tổng522 mutant | 4không đo được theo nền; tên/lý do ngay dưới |
| targeted.py |11/11 neutral;16mutant/22cặp:22/22 assertion kill;BASE2/2 assertion kill | Không skip, không nhận OTHER_EXCEPTION làm pass |
| contracts.py |5/5 mock contract +4/4 ca vật lý;12/12 own mutant assertion kill | Windows/sh-vắng chỉ mock; timeout thật0.1s mỗi version/auth |
| merged_guards.py |9/9 mutant đúng property và TinHieuChotCa | Mutant symlink chỉ phá path có`..`; mutant slash chỉ chết ở bin/; không nhận kill sớm property khác |
| matrix.py |41 so sánh helper/glibc/Bash |2 khác: shebang/empty miễn; all-long errno0/2 đều-fail không có hậu quả nhãn.2 phép setuid khởi tạo bị EPERM, không nhận như lỗi sản phẩm; đã thay bằng permission_probe |
| permission_probe.py |2mode×3oracle khớp | mode000 và0111 đều listdirEACCES13; mode000 chọnlater,0111 chạyfirst; không cần setuid |
| extra_matrix.py |7 so sánh thêm;2 kết quả capability;1 phép thử chroot |7comparison gồm shebang-explicit-empty và shebang-long; long không rỗng là F4; nativeargv0/name-space/name-dash/cwd>4200 đều khớp. Chroot125/EPERM |
| callers.py |16/16 parity positive/negative,8 nhóm |32 lần chạy CLI giả, gồm llm-live-fixture; không gọi API |
| doctor_long.py |HEAD và glibc cùng doctor JSON,2 phép đo |HEAD CHUA_XAC_THUC vs glibcCO_CREDENTIAL; default cả2rc0, không tự khai rc khác |
| hint_validate.py |glibcneutral1/1 PASS;HEAD + mutant-prefix2/2 đúng assertion;patchdry-run/apply2/2rc0 |Test thuần +3 dòng; chưa áp trên cây review; không tuyên bố HEAD xanh sau hint |

**13 lỗi HEAD/BASE cùng ID, không tính là finding:**

- `r858_goc_tam_tranh_to_tien_co_git`: OSError30: /var/tmp read-only; chỉ tên thư mục tạm khác giữa2lượt.
- `t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac`: OSError30: /var/tmp read-only; chỉ tên thư mục tạm khác giữa2lượt.
- `r484_g2_doctor_doc_dung_home_da_materialize`: doctor ignored the credential in CODEX_HOME
- `r484_g2_schema_truoc_freshness_va_home_materialize`: freshness hid invalid schema
- `r484_g2_child_khong_nhan_snapshot_va_rac_chan_truoc_probe`: inert launcher child failed: CHAN [13]: Không chuẩn bị được Codex credential; chưa chạy child
- `r484_g2_storage_kernel_guardrails`: OSError: Codex home is inside a repository
- `r484_g2_recovery_probe_rollback_va_snapshot_moi`: OSError: Codex home is inside a repository
- `r484_g2_probe_isolated_marker_va_refresh`: OSError: Codex home is inside a repository
- `r484_g2_hook_shell_scrub_truoc_probe`: Không đo được child SAU materializer; cùng lý do trênBASE.
- `r484_g8_hook_scrub_kin_voi_bash_env`: Không đo được child SAU materializer; cùng lý do trênBASE.
- `r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do`: OSError: Codex home is inside a repository
- `r484_g7_tu_choi_ghi_dung_ban_da_probe`: OSError: Codex home is inside a repository
- `r484_g7_auth_doi_truoc_khi_thay_thi_giu_ban_moi`: OSError: Codex home is inside a repository

`ls -ld /tmp/.git` xác nhận thư mục tồn tại (`dr-xr-xr-x`). Hai lỗi /var/tmp là hạn chế filesystem;11lỗi còn lại do preflight/materializer trong cùng điều kiện. Không xóa /tmp/.git, không sửa test hoặc gọi đây là hồi quy. Các message HEAD/BASE giống nhau trừ2tên thư mục tạm /var/tmp; so tên lỗi có delta0. Chi tiết đầy đủ ở suite-comparison.json.

**10skip giống nhau, ghi riêng:**

- `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125`: fixture nay danh cho Windows; ban POSIX la t63 (chay duoc, khong bo qua)
- `r345_chan_socket_that_ma_than_hook_van_chay_dung`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r345_cac_phep_do_cuc_bo_van_dung`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r345_lop_tham_import_van_co_rang`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r347_tham_import_van_song_tren_python_truoc_310`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r348_dot_bien_bo_isidentifier_lam_ca_dich_DO`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r484_g4_windows_sid_alias_identity`: BO QUA native Windows SID conversion



**4 đột biến không đo được trong full mutation suite (không cộng vào mẫu số518):**

- `g4_windows_sid_alias_not_normalized KHONG DO DUOC tren nen nay (native SID conversion)`
- `g4_windows_LA_not_current_owner KHONG DO DUOC tren nen nay (native SID conversion)`
- `g2_windows_directory_pin_access KHONG DO DUOC tren nen nay (native Windows share-delete pin)`
- `124_khi_chau_con_song        KHONG DO DUOC tren nen nay (ca dich bo qua: t62_qua_han_ma_khong_giet_het_cay_phai_tra_125)`

## BANG SAN

| Hướng độc lập | Lệnh từ cay-kho/ | Output thật | Phán định |
|---|---|---|---|
| PATH/filename/argv0: absolute, relative, empty,`..`,symlink,slash cuối,tên có slash,space/dash,PATH vắng/envNone | `python3 -B ../evidence/matrix.py`; `extra_matrix.py` |FIRST/CWD đúng;bin//cli giữ slash;nativeargv0=native/argc2/arg1=two words;env thiếuPATH chạytrue0;cwd>4200 cảshebang/no-shebangrc0 | **KHÔNG PHẢI LỖI** các dạng thường; empty-shebang miễnW |
| PATH dài + script có shebang kiểm$0 | `python3 -B ../evidence/extra_matrix.py`; `doctor_long.py`; `hint_validate.py` |Input không entryrỗng;helperrc42/glibcrc0;doctorCHUA_XAC_THUC/CO_CREDENTIAL;HEAD và mutantprefix đỏ đúng assertion | **LỖI F4 P1**, ngoài đầu vào empty được miễn |
| Trật tự lỗi exec và interpreter không tồn tại | `python3 -B ../evidence/matrix.py` |EACCES13 ưu tiên;ENOENT/ENOTDIR cuối2/20;ETXTBSY26/ELOOP40 dừng;thiếuinterpreter chuyểnLATER | **KHÔNG PHẢI LỖI** errno thực đã đo;3 errno hiếm filesystem chưa đo |
| Quyền thư mục và thiếu bitx | `python3 -B ../evidence/permission_probe.py`; targeted.py ca(c) |listdirEACCES13 cả000/0111;execute qua0111 được;0644False khôngretry | **KHÔNG PHẢI LỖI**;setuid EPERM là môi trường, không hồi quy |
| Binary sai kiến trúc, empty0byte,BOM-only,cú phápBash | `python3 -B ../evidence/matrix.py`; contracts.py |wrong-arch helper/glibc2,Bash126;emptyrc0 nhưng probeFalse;BOM127;Bashsyntax Bash0,helper/glibc127 | **KHÔNG PHẢI LỖI** theo hợp đồng glibc;khácbinaryrc không tạo nhãn tốt |
| Retry/argv/env/stdin/mã hóa,timeout,rc/rỗng | `python3 -B ../evidence/contracts.py`; targeted.py |9/9neutral;12/12mutantassertion;stdinEOFTrue;timeoutFalse/qua_hanTrue;rc1/rỗngFalse | **KHÔNG PHẢI LỖI** trong hợp đồngM1 |
| Byte ngoàiUTF8 và độ nhạy chốt | `python3 -B ../evidence/targeted.py`; merged_guards.py |strictUTF8mutantTinHieuChotCa,không exception ngoài;22/22pairs;9/9properties | **KHÔNG PHẢI LỖI**,F7 đã đóng |
| Toàn graph caller và classifier | `python3 -B ../evidence/audit.py`; callers.py |38callsite,7hàmstructural;16paircallerparity;2delegate #1083 còn trần | **KHÔNG PHẢI LỖI** scope giữ lại;không nâng scope miễn trừ |
| Suite/gate/số dòng/khẳng định lịch sử | `python3 -B ../evidence/run_suites.py`; audit.py; history_check.py |HEAD302/315,BASE291/304,cùng13lỗi/10skip;ruff17/17delta0;diffcheck0;doctrine10/0;+339 | **KHÔNG PHẢI HỒI QUY** các lỗi cùngBASE;F4 vẫn tồn tại ngoài các case đang xanh |
| NativeWindows,/bin/sh thật vắng,CIexactHEAD | contracts.py;extra_matrix.py;kiểmartifact |Windowsguardmock1spawn;chroot125/EPERM;khôngCIreceipt | **KHÔNG ĐO ĐƯỢC**,không bịa pass hoặc finding |

## FINDINGS

### F4-phan-giai-PATH [P1] Phần tử PATH quá dài không rỗng làm đổi `$0` của shebang và sai nhãn doctor

**TEP/DONG:** `.claude/dev/launcher.py:2944` biến phần tử dài thành `""`, `:2945` thành tên trần, `:2950` bắt exec bằng `./<tên>`; lời khai chọn như glibc tại`:2922`/`:2928`. Hậu quả ở `_do_openai_llm:4042`/`:4050` và KHA_NANG của doctor. Ca hiện tại`:9414` chỉ dựng script **không shebang**, chưa khóa kết hợp này.

**VAN DE:** Bản vá sửa đúng việc glibc thử cwd khi bỏ qua phần tử PATH quá dài trước dấu`:`, nhưng tái sử dụng nhánh `executable='./llm'`. Kernel nhận script có shebang qua tên`./llm`, nên interpreter thấy `$0=./llm`; glibc execvp thật gọi filename`llm` và interpreter thấy `$0=llm`. Wrapper kiểm `$0` trả42 qua helper, thành công qua glibc. Trong fixture không có empty entry ở đầu vào: PATH=`('x'*4200)+':'+later`, cả2 phần tử đều không rỗng.

**Ranh giới miễn trừ:** W-1077-1 của LEASE-g5 miễn script shebang tìm qua **phần tử PATH RỖNG**, kèm câu “CHI truong hop tren… Moi lech glibc khac van la finding”; prompt lặp lại ranh giới này. Reviewer giữ nguyên miễn trừ cho `PATH=':'+later` và không tính ca ấy. Việc implementation tự đổi phần tử dài thành empty candidate không biến đầu vào không rỗng thành trường hợp đã được chủ kho miễn. Sai khác mới có cùng cơ chế`./`, nhưng thuộc biến thể PATH dài được thêm trong457e413; không có authority mở rộng W sang biến thể đó. Nếu chủ kho chủ ý chấp nhận cả biến thể này thì cần quyết định miễn trừ ghi rõ đầu vào dài, reviewer không tự cấp.

**DA THU NGHIEM:**

- `python3 -B ../evidence/extra_matrix.py`: `shebang-long-nonempty-PATH` helper`[42,"",""]`, glibc`[0,"",""]`; ca gọi ở đây dùng đối số`two words` để tách việc thực thi khỏi subcommand. CLI giả qua `_do_openai_llm` nhận HEAD`CHUA_XAC_THUC`, glibc`CO_CREDENTIAL/llm-FIRST`.
- `python3 -B ../evidence/doctor_long.py`: cùng`lenh_doctor`/CLI/env, thay duy nhất helper spawn bằng child gọi **ctypes libc execvp thật**. HEAD JSON:`kha_nang[openai-llm].trang_thai=CHUA_XAC_THUC`, `chua_xac_thuc=[openai-llm]`; glibc:`CO_CREDENTIAL`, `chua_xac_thuc=[]`, `chua_chung_minh=[openai-llm]`. Mặc định cảhai`rc0`; finding là nhãn và việc nhận credential sai, không khai sai mã thoát.
- `python3 -B ../evidence/hint_validate.py`: cùng ca hiện hữu sau hint+3 dòng, oracleglibcneutral **PASS**. HEAD đỏ **TinHieuChotCa** tại đúng`bang` với message`PATH dai KHONG rong doi $0 shebang…`. Mutant riêng buộc filename`./llm` **chỉ cho PATH dài** cũng đỏ đúng assertion đó. Các đoạn absolute/empty/symlink/no-shebang-long/missing-interpreter trước nó vẫn qua; không nhận setup exception làm kill.

**DO TIN:** Cao về sai khác và hậu quả nhãn trên Linux/glibc2.39. Phân loại ngoài miễn trừ dựa vào đầu vào PATH không có entryrỗng và giới hạn nguyên văn được giao; không nói ca empty được miễn đã hết hiệu lực. Không cáo buộc filesystemUTF8 còn lỗi hoặc F7 chưa sửa.

**GỢI Ý VÁ BẰNG LỜI:** Tại lớp dựng và spawn candidate của `_chay_probe_nhu_shell`, giữ filename glibc cho cwd candidate phát sinh từ entry dài, gồm cả script có shebang; chỉ giữ argv[0] bằng`executable=` chưa giữ được`$0` của interpreter. Nếu vẫn giữ hạn chế subprocess buộc thêm`./`, cần chủ kho quyết định rõ việc nới miễn trừ cho đầu vào dài trước khi coi hành vi này được chấp nhận. Không đơn giản bỏ`./` trên mọi candidate: Python subprocess sẽ lại thử bản sau khi no-shebang ENOEXEC, tái mở F4 cũ.

**CA KHÓA VÀ NGUY CƠ:** `HINT.patch` thêm đúng3 dòng vào ca PATH hiện có, trong trần sauhint342/345; không sửa runtime nhạy cảm. Nó bảo vệ script có shebang/$0 trong cwd khi PATH đầu dài không rỗng. Giữ đồng thời chốt no-shebangđầuPATH, logical$0 fallback, relative/..symlink, trailing slash, cwd dài, nativeargv0, ETXTBSY/ELOOP,env/timeout và negativeclassifier. Đổi cơ chế spawn có thể mất pipe/encoding/timeout hoặc đổi thứ tự errno; một bản sửa chỉ normalize/ghép cwd hoặc bỏ`./` rộng sẽ tái sinh các lỗi lượt trước. Hướng production chỉ mô tả bằng lời theo chỉ thị; executor tự tái dẫn xuất và đo trên nhánh của mình.

## HINT VA TINH TOAN VEN

`HINT.patch` là **test thuần, chưa áp trên cây thật**. Đã `patch -p0 --dry-run` và apply trên bản sao tạm; cả2rc0. Từ `cay-kho/`, cách áp của executor là `patch -p0 < ../HINT.patch`. Hint cố ý làm HEAD hiện tại đỏ ở case mới, không phải bằng chứng gate đã xanh. Executor tự áp, đo và chịu trách nhiệm commit; không apply mù.

`final-checks.json`: HEAD/tree không đổi; `git status --porcelain=v1 --untracked-files=all` rỗng. Cả hai source có byte và mode0644 khớp `git show HEAD:<path>`. Spec tự băm vẫn đúng hash dòng3. Tất cả bản sao, mutation, log và HINT ở ngoài cây review.

Không push, merge, land, deploy, sửa credential hoặc gọi mạng. Kết luận exact SHA: **changes_requested —1P1**, lớpF4 còn mở; A4CIexactHEAD **KHÔNG ĐO ĐƯỢC**. Vẫn còn1lượt review sau lượt9 theo chỉ thị, không tự mở thêm lượt.
