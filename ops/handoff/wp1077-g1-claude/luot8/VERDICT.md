verdict: changes_requested
reviewed_sha: 7879902ac11f14c5f67708ee058f6cb0e7916b55
spec_sha256: eabbb725650addad531429d48801667f2ef05a6090c00123d1d4146c7b89c3f3
Ket qua: 0 P0, 1 P1, 1 P2, 0 P3.

PR #1080 · packet #1077 DOCTOR-ENOEXEC-BI-CHE r1 · lease `wp1077-r1-g5-claude` · review_class `sensitive` · Codex lượt 8/10.

**Đề nghị changes_requested.** Lớp F4 còn chọn khác executable của glibc khi một phần tử PATH quá dài đứng trước dấu `:`; đã đo ảnh hưởng tới nhãn credential. Bản vá UTF-8 chạy đúng, nhưng chốt đột biến mới chưa chết bằng assertion theo yêu cầu lượt review. Hai finding được phân biệt: hành vi phân giải PATH (P1) và cách kiểm chứng trong test (P2).

## NEO VA DIEU KIEN DO

- BASE: `086f1b7343fc1d778e50797e6c9ca0964b11a755`.
- HEAD: `7879902ac11f14c5f67708ee058f6cb0e7916b55`; tree: `c1333b3207b6c65d9f63ceb35734d393631e6b8a`.
- `sha256sum ../SPEC.md` tự đo đúng hash dòng 3. `git diff BASE HEAD` khớp byte `diff.patch`; `git diff --numstat BASE HEAD` khớp `numstat.txt`.
- Hai tệp: `.claude/dev/launcher.py` **+54/-9**; `.claude/dev/launcher_test.py` **+280/-11**; tổng **+334/-20**, trong trần **345** tại `LEASE-g5.yaml:nang_tran_lan_4`. Không dùng net +314 thay số dòng thêm.
- Runtime đã đo: Python **3.13.16**, Linux x86_64, **glibc 2.39**, **Bash 5.2.21**, Ruff **0.17.1**. Không suy parity native Windows từ mock.
- `runs/c491c7bb/run.json` ghi provider `openai_codex`, execution_surface `codex_cli`, transport `machine`, run ID `c491c7bb6dfe405093d0c454af2c498a`. Đây là metadata được giao, không phải phép đo độc lập exact model/effort đã phục vụ. Không suy reviewer identity từ coauthor hay tài khoản GitHub, không tự tạo receipt/assurance hoặc quyền merge.
- Review độc lập context executor; không sửa source/branch `cay-kho/`, không push, không gọi mạng hoặc dùng credential thật. Fixture CLI, Git/HTTP giả và các bản đột biến đều ngoài cây review. CLI `llm prompt` trong phép đo là tệp giả cục bộ, không gọi API.
- `cloud-environment-runtime` đã đọc; công cụ `environment_status` không có trong tool catalog. Không dùng kết quả credential/network readiness giả định.

Bằng chứng ở `evidence/`. Lệnh script trong bảng chạy được từ `cay-kho/`, ví dụ `PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/matrix.py`. Script tự xác định thư mục từ `__file__`. Các log và JSON giữ output thật, tên ca, exception và return code; không chỉ lưu kết luận.

Full suite được chạy bởi `python3 ../evidence/run_suites.py`. Nó gọi `python3 -u .claude/dev/launcher_test.py` và cùng lệnh thêm `--dot-bien` tại HEAD; `-u` chỉ để flush log. Base được xuất từ Git object BASE vào `evidence/base-copy/`, có `.git` riêng để không kích hoạt skip bản sao rời. Môi trường chung chỉ có PATH/LANG/LC_ALL/TMPDIR nếu có, thêm `PYTHONDONTWRITEBYTECODE=1`, `CLAUDE_CODE_REMOTE=false`, `CLAUDE_PROJECT_DIR=<evidence/hook-workspace>`. Không mang credential hay RUST_LOG của phiên vào lượt suite. Hai thử khởi động trước đã dừng; kết quả nghiệm thu chỉ lấy lượt cô lập hoàn tất. Hook t152 được chuyển nơi ghi dấu vết ra ngoài cây review.

`/tmp/.git` có thật và chỉ đọc (`ls -ld /tmp/.git`). Giữ nguyên để đối chiếu base cùng điều kiện, không xóa để làm suite xanh. Không có mạng. Hai điều kiện này làm một số phép đo môi trường không thực hiện được; không ghi chúng thành hồi quy packet.

## BANG NGHIEM THU

| Tiêu chí | Lệnh từ cay-kho/ | Output thật / bằng chứng | Đạt? |
|---|---|---|---|
| M1: ENOEXEC, POSIX, sh là file, đúng một retry; giữ argv/env/stdin/timeout/encoding và rc | `python3 -B ../evidence/contracts.py`; `python3 -B ../evidence/extra_mutations.py`; `python3 -B ../evidence/matrix.py` | Contract 6/6; 20/20 mutant riêng chết TinHieuChotCa; 6 errno của đường có slash giữ nguyên object, không retry; lỗi retry không sinh spawn thứ ba | **Đạt cơ chế M1**; lời khai chọn tệp theo glibc của toàn helper chưa đạt, F4 |
| M2: version/auth cùng helper và đủ probe trong phạm vi đã thu hẹp | `python3 -B ../evidence/audit.py`; `python3 -B ../evidence/callers.py`; `python3 -B ../evidence/targeted.py` | Hai call site 2987/3039 và các caller KHA_NANG đã nối helper; 8 caller × 2 mode shebang/no-shebang cùng kết quả; ca cấu trúc xanh | **Đạt phạm vi được giao**; `_git`/`_do_codex_song` chuyển #1083 |
| M3(a): rg/git no-shebang đứng đầu, bản tốt phía sau | `python3 -B ../evidence/targeted.py` | Ca(a) PASS; cả rg/git `doctor rc=0`, `co=True`, version khong-shebang, không bi_che | **Đạt** |
| M3(b): đầu PATH exit1 vẫn BI_CHE | Cùng lệnh | Ca(b) PASS: doctor 12/BI_CHE; bỏ rc → TinHieuChotCa đúng ca | **Đạt** |
| M3(c): shebang nhưng 0644 không retry | Cùng lệnh; contracts.py | Ca(c) PASS; phiên bản False, qua_han False; mutant mọi OSError chết đúng assertion | **Đạt** |
| M3(d): auth no-shebang một dòng rc0 | Cùng lệnh | Ca(d) PASS: True, ok, Logged in; mutant auth spawn thẳng chết đúng assertion | **Đạt** |
| M4: 4 mutant bắt buộc giết đúng ca | Cùng lệnh | Bỏ retry 2/2; mọi OSError 1/1; auth bỏ helper 1/1; bỏ rc 1/1 — **5/5 cặp TinHieuChotCa** | **Đạt**; không gộp lỗi mutant UTF-8 khác vào bốn mutant M4 |
| A1: full Linux suite, cho phép lỗi môi trường cùng delta 0 | `python3 -B ../evidence/run_suites.py` | HEAD 302/315 đã chạy, tổng 325/skip 10/lỗi 13; BASE291/304, tổng 314/skip 10/lỗi 13; đúng cùng ID lỗi và skip; +11 pass, delta lỗi 0 | **Đạt phần suite theo ngoại lệ SPEC**, không khai toàn suite xanh |
| A1: mọi mutant mới đúng ca và đúng lý do theo chỉ thị review | `python3 -B ../evidence/targeted.py`; `python3 -B ../evidence/merged_guards.py` | 15 mutant wp1077,21 cặp;20 assertion kill,1 UnicodeEncodeError trước assertion. 9/10 tính chất ca gộp chết đúng assertion, UTF-8 không đạt điều kiện này | **Chưa đạt yêu cầu assertion của chốt mới**, F7 P2 |
| A2: base(a),(d) đỏ đúng bệnh | `python3 -B ../evidence/targeted.py` | HEAD tests + BASE launcher:2/2 TinHieuChotCa; rg12/BI_CHE, authFalse/OSError | **Đạt** |
| A3: tái hiện Issue tại chỗ | Ca(a) trong targeted.py gọi lenh_doctor thật, CLI giả | rg/git rc0, không bi_che, co=True; BASE cùng fixture rc12 | **Đạt fixture tập trung**, không khai doctor toàn máy xanh |
| A4: Ruff F delta 0 | `python3 -m ruff check --no-cache --select F .claude/dev/launcher.py .claude/dev/launcher_test.py`; tương tự `scripts/tl.py`, và tại base-copy | HEAD/BASE đều launcher0 + test5 F841 + tl12 F821; rc1 hai bên, delta 0; cùng diagnostic/message/function, không chỉ so tổng | **Đạt delta**. Goc_run đổi RHS nên raw source fingerprint khác, diagnostic cũ vẫn cùng function |
| A4: diff check | `git diff --check 086f1b7343fc1d778e50797e6c9ca0964b11a755 HEAD` | rc0, output rỗng | **Đạt** |
| A4: doctrine | `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | rc0; `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` | **Đạt phần scanner**, không suy scanner chứng minh đúng nghĩa mọi câu |
| A4: CI PR xanh exact HEAD cuối | Không gọi mạng; quét artifact exact SHA trong bundle | Chỉ có prompt/run/checkpoint; không có check-run receipt/log exact-head để xác minh | **KHÔNG ĐO ĐƯỢC**; A4 tổng thể chưa đủ bằng chứng, không tự khai CI xanh |

## BANG DO

**Cách tìm khẳng định:** đọc toàn `diff.patch` và `diff-tu-luot7.patch`; tự dựng diff từ Git và so byte. `audit.py` theo hunk thu mọi dòng thêm, tokenize mọi comment thêm, AST toàn hàm/docstring giao dòng thêm và lưu cả thân hàm vào `claims-inventory.json`. Đọc toàn helper mới, mọi caller đổi, mọi test và tuple DOT_BIEN wp1077; đọc nguyên `git log -1 --format=%B HEAD` và các message e6bf386/57e2d4a/1027f85/c4af726/2320f27. Rà AST toàn launcher cùng delegate, không lấy whitelist 7 hàm của test làm trần tìm. Bảng dưới nhóm theo nghĩa; bộ lọc trích xuất không được dùng để loại khẳng định khác khỏi review.

| Khẳng định | Diff khai | Đo được (lệnh / artifact) | Khớp? |
|---|---|---|---|
| No-shebang gây ENOEXEC; subprocess có slash ném, bare có thể thử bản sau | Helper2924–2926 | matrix.py và targeted.py: trực tiếp base rg/auth OSError8; BASE doctor rg12/BI_CHE; helper fallback FIRST | Có |
| Hợp đồng glibc `/bin/sh`; Bash có thể khác | Helper2926; comment test 9237 | matrix.py bash-syntax: Bash 0/BASH_ONLY, helper và glibc127; wrong-arch Bash 126, helper/glibc 2 | Có; không coi Bash và glibc là một oracle |
| Chuỗi `<entry>/<name>`, giữ slash cuối, relative, `..`, symlink | Helper2927–2928/2943 | matrix.py: bin/cli, bin//cli; link/.. đúng inode FIRST; merged_guards.py có mutant riêng từng property | Có dạng đã đo |
| Entry rỗng logical `<name>`; syscall `./<name>` | Helper2928–2931/2948 | matrix.py: no-shebang `$0=cli`; native argv0=cli; shebang helper `$0=./cli`, glibc cli | Mô tả đúng; phần shebang **MIỄN TRỪ W-1077-1**, không finding |
| Bỏ phần tử PATH dài mà vẫn chọn như execvpe glibc | Helper2922/2928/2942–2943 | long_entry.py: long-first/long-middle glibc+coreutils CWD, helper LATER; credential-label-contrast CO_CREDENTIAL vs CHUA_XAC_THUC | **Không**, F4; không được mở rộng waiver |
| env=None kế thừa; explicit env thiếu PATH dùng defpath | Helper2941 | matrix.py: None+PATH FIRST; env thiếu PATH / None khi PATH vắng đều chạy true rc0 | Có |
| Byte ngoài UTF-8 dùng fsencode thay encode strict | Hai dòng diff lượt7;2320f27 message | matrix.py raw-byte hiện hữu và vắng trước bản sau đều rc0; targeted neutral PASS; khôi phục strict gây UnicodeEncodeError | **Bản vá hành vi đúng**; chốt assertion còn F7 |
| Chỉ 6 errno tìm kiếm đi tiếp, lỗi khác dừng | Helper2929–2930/2944/2952 | matrix.py EACCES/ENOENT/ENOTDIR vật lý, ETXTBSY26/ELOOP40 dừng; contracts.py lỗi đường có slash giữ nguyên object | Đạt dạng đo thật; ESTALE/ENODEV/ETIMEDOUT chưa dựng filesystem thật, chỉ thấy đúng tập trong source |
| Hết search ưu tiên EACCES, còn lại lỗi cuối | Helper2930/2954–2955 | matrix.py: EACCES+ENOENT→13; EACCES+ENOTDIR→13; ENOENT+ENOTDIR→20; đảo→2; EACCES+ELOOP→40 ngay | Có các thứ tự đo thật. All-long-only libc có thể trả errno0; helper ENOENT, chưa chứng minh hậu quả nhãn ở trường hợp chỉ-fail này |
| Retry cùng tệp, argv/env/stdin/timeout/encoding/rc | Helper2950–2951, M1 | contracts.py ghi cả2 argv/kwargs; extra_mutations.py20/20; matrix native argv0 và `a b`; targeted argv/env | Có nhánh retry |
| sh vắng không retry; Windows giữ nguyên | Helper2935/2950 | contracts.py mock2 guard: mỗi bên1 spawn/đúng exception; mutant bỏ guard đỏ. Chroot thật rc125 Operation not permitted | Đạt mock; native Windows và sh-vắng thật **KHÔNG ĐO ĐƯỢC** |
| llm wrapper utf8/replace, DEVNULL/capture/timeout | Helper2958–2963 | contracts.py exact kwargs; callers.py3 lệnh llm bằng CLI giả, marker FIRST | Có thuộc tính được nêu; không suy API wrapper mới có mọi tham số tùy chọn stdin/cwd của wrapper cũ |
| Đổi callee, giữ phân loại thường và negative | 9 call site cũ + wrapper llm mới | callers.py8 × 2 mode parity; contracts.py empty/rc1/BOM/timeout; targeted ca(b)/(c) | Có trong fixture; F4 xảy ra trước classifier do chọn tệp khác |
| M3(a–d), argv/env, Codex status và llm tên trần được khóa | Test9240+ / DOT_BIEN12393+ | targeted.py11/11 neutral;5/5 cặp M4 đúng assertion; ca Codex status/version cùng CO_CREDENTIAL | Có |
| Ca gộp giữ đủ tính chất sau nén | Test9402–9468 và messagec4 | merged_guards.py9 tính chất cũ mỗi tính chất một mutant, đúng assertion; property UTF-8 mới OTHER_EXCEPTION | **Không trọn vẹn**, F7 |
| Ca mới UTF-8 đỏ khi dùng encode strict | Test9465–9468; mutant 12420; message 2320 | targeted.py: UnicodeEncodeError; log full in `OK giet1/1 ... (UnicodeEncodeError)` | Đỏ theo nghĩa phát sinh exception; **không đạt điều kiện bang/TinHieuChotCa**. Không gọi exception này là lỗi vô can, cũng không đổi nó thành assertion trong báo cáo |
| Không tuyên bố phủ mọi probe, trừ2 đường #1083 | Helper2931–2932; structural9382+; commentDOT_BIEN12401 | audit.py full call graph; docstrings và comment đều nêu scope đã thu hẹp | Có; F1 lời khai đã đóng |
| Gỡ đổi stub lượt2, argv0 tên trần | Diff t115/t121; message01b | AST t103/t111/t113 bằng BASE; t115 chỉ lọc thêm executable; native argv0=cli. `final-checks.json` | Có |
| t103 có so tên nhưng hai nhánh cùngRc0; t113 không so | Message 1027f85 đính chính57e2d4a | AST/source t103 lồng chay_kho có so cmd[:2]; không thay stub trong diff hiện tại | Đính chính đúng, F6 đóng |
| HEAD docstring neo đúng W-1077-1 | `git log -1 --format=%B HEAD`; helper2931 | Đọc LEASE-g5:mien_tru và diff-tu-luot7; matrix shebang-empty-waiver | Khớp quyền miễn trừ đã được giao; chỉ áp shebang/empty PATH |
| Số dòng tại2320 và head cuối +334/-20; c4 +328/-20 | Message2320 và Git numstat từng object | audit.json:2320 +54/-9,+280/-11;7879902 cùng số; c4 +54/-9,+274/-11 | Có; trần330 cũ bị vượt4 nhưng g5 đã nâng345 |
| F5: dcfb+236/-19, e6+267/-24 | Message e6 | audit.json Git object exact BASE..dcfb/e6 | Đính chính đúng. Handoff không trong bundle2-file này nên việc ghi vào handoff **chưa đo được** |

## KIEM KE CAC DUONG PROBE VA SPAWN

`evidence/call-sites.json` lưu caller/line/call từ AST; `call-graph.json` lưu graph toàn launcher. Tìm từ cả CONG_CU, KHA_NANG, `lenh_doctor`/preflight, các đường Git và tất cả `subprocess.run/Popen`, rồi đọc delegate `codex_cred.py`. Không chỉ kiểm danh sách trong ca cấu trúc.

| Đường quyết định nhãn | Spawn cuối / nội dung | Phạm vi và kết quả |
|---|---|---|
| Mọi CONG_CU --version | `_phien_ban:2987` → helper2948/2951 | Trong packet; no-shebang tốt/hỏng, empty, BOM, binary, timeout đã đo |
| CONG_CU auth và agy models | `_xac_thuc_kem_dau_ra:3039` → helper; `_xac_thuc` chỉ bọc; `_do_antigravity` dùng cache hoặc cùng auth/version helper | Trong packet; auth/agy CLI giả no-shebang xanh, không chạy probe thừa |
| Codex login status | `_do_codex:3934` → helper | Trong packet; CO_CREDENTIAL với CLI giả |
| Codex --kiem-song | `_do_codex_song:3856` → runpy codex_cred `_kiem_song` → subprocess tại codex_cred.py | **Ngoài packet theo chủ kho**, #1083; chưa phủ ENOEXEC; không gọi live/credential thật |
| Snapshot preflight doctor/run/chuan-bi | `_chuan_bi_va_bo_snapshot:3219` → credential helper → `_probe_snapshot:3616` → codex_cred delegate | Credential preflight ngoài scope CLI được giao; cùng hạn chế delegate; không suy mọi spawn doctor đã phủ |
| llm version, keys list, prompt --no-log | `_do_openai_llm:4040/4048/4062` → `_chay_probe_llm` → helper | Trong packet;8 × 2 caller matrix có 3 lệnh llm; F4 ảnh hưởng chọn tệp |
| gh auth status, gh api repos/... | `_do_github:4571/4632` → helper | Trong packet; CLI giả và REST/Git stub; DUNG_DUOC dựa gh-kho, không đi mạng |
| claude mcp get | `_suc_khoe_mcp_github:4373` → helper | Trong packet; Status Connected → khoe; đúng argv và env chuẩn hóa |
| git ls-remote/remote get-url, tìm workspace, đọc hook/launcher master | `_git:286` dùng subprocess.run thẳng; caller `_do_github`, `_do_hook_cu`, `_do_launcher_cu` và đường run dùng chung | **Ngoài packet theo chủ kho**, #1083; ghi nhận chưa nhận ENOEXEC; không tính finding mới |
| Claude credential, hook-da-chay, locale/path/module Python | Đọc file/env/hash/importlib/find_spec, không exec CLI thêm | Không có spawn ENOEXEC trong lớp này |
| GitHub REST/MCP endpoint | urllib HTTP, không exec tệp | Ngoài cơ chế ENOEXEC; phép đo dùng stub, không gọi mạng |
| `_probe_spawn`/run | `_chay_van_ban_an_toan:319`; Popen2299 sinh lệnh người dùng | Ngoài phạm vi SPEC; không đổi helper dùng chung đường run |
| `_chay_json_chat_che:333` | subprocess riêng; không có caller trong graph doctor | Không phải probe quyết định nhãn doctor được giao |
| ps371/455/508/706, taskkill883, process tree | Hỏi/quản lý tiến trình | Ngoài probe khả dụng công cụ và packet; không thiếu một caller doctor trong write set |

Không phát hiện đường CLI trong phạm vi còn dùng spawn trần ngoài helper. Hai nhóm `_git` và codex_cred vẫn có spawn trần, đã khai đúng giới hạn và được chuyển #1083; không mở lại F1 runtime của packet này.

## DOI CHIEU LUOT TRUOC VA LICH SU FINDING

| ID / biểu hiện lịch sử | Phân loại tại HEAD | Tự đo và giới hạn |
|---|---|---|
| F4 lượt7 — PATH chứa byte ngoài UTF-8 | **ĐÃ VÁ THẬT về hành vi** | matrix raw-byte hiện hữu/vắng đều chạy; ca neutral xanh; os.fsencode ở cả hai độ dài. Chốt assertion mới còn F7 riêng |
| F4 lượt7 — shebang qua entry rỗng đổi $0 | **CHƯA VÁ, ĐƯỢC MIỄN TRỪ**, không gọi là vá thật | helper ./cli, glibc cli; quyền W-1077-1 trong lease g5 khớp đúng biểu hiện; không tính finding |
| F4 toàn lớp qua lượt2–6 | **CHƯA ĐÓNG LỚP** | absolute/empty/relative/symlink/.., cwd dài, thiếu interpreter, ETXTBSY/ELOOP/error order đều đã đo lại; phát hiện long-entry-before-colon khác glibc, P1 còn mở. Không gán biến thể mới cho commit2320 — nó có từ thiết kế c4af726 |
| F1 runtime probe bỏ sót | **Đã sửa các caller được giao; phần2 đường CHUYỂN PHẠM VI**, không gọi tất cả đã vá | callers8 × 2, AST structural; `_git`/`_do_codex_song` còn ở #1083 theo chủ kho |
| F1 lời khai “mọi probe” | **ĐÃ VÁ THẬT** | Helper, structural docstring và comment bảng mutant đều nêu ngoại lệ/phạm vi hẹp; không thấy lời khai phủ toàn doctor mới trong diff/HEAD message |
| F2 Bash = sh/glibc | **ĐÃ VÁ THẬT về lời khai** | Bash-only syntax Bash 0, glibc/helper127; binary sai kiến trúc Bash 126 vs2. Diff đã nói rõ hợp đồng glibc và Bash khác |
| F3 mất đối số không bị test bắt | **ĐÃ VÁ THẬT** | targeted argv/env neutral PASS; mutant mất argv chết TinHieuChotCa; own kwargs mutants20/20 |
| F5 số dòng+228 sai | **Đã đính chính đo đúng** | Git dcfb 236 và e6 267; không đo được handoff ngoài bundle, không tái cáo buộc câu lịch sử đã đính chính |
| F6 t103 không so tên | **ĐÃ VÁ THẬT về đính chính** | Message 1027 nói đúng phép so/hai Rc0; AST stub hiện tại bằng BASE |

Sổ lớp còn mở: **2 lớp / 2 biểu hiện tính finding**: `F4-phan-giai-PATH` (P1; long entry trước colon) và `F7-dot-bien-UTF8-khong-toi-assertion` (P2; thiếu assertion khi rollback strict encoding). Waiver và successor giữ nguyên nguồn lịch sử, không dùng để xóa F4 khỏi sổ.

## BANG TEST

| Bộ / lệnh | N/M và exit code | Bỏ qua / giới hạn |
|---|---|---|
| HEAD `python3 -u .claude/dev/launcher_test.py` | **302/315** đã chạy;325 tổng;13 lỗi;rc1 |10 skip, danh sách dưới |
| BASE cùng suite/môi trường | **291/304** đã chạy;314 tổng;13 lỗi;rc1 | Cùng10 skip và13 ID lỗi;delta lỗi 0 |
| HEAD `python3 -u .claude/dev/launcher_test.py --dot-bien` | Harness báo **517/517**,rc0 |4 KHÔNG ĐO ĐƯỢC nền; con số517 bao gồm tín dụng exception UTF-8, không coi là toàn bộ assertion kills |
| targeted.py | **11/11** neutral;15 mutant/21 cặp: **20/21 assertion kill**,1 OTHER_EXCEPTION;BASE2/2 assertion kill | Không skip; không nhận exception khác làm TinHieuChotCa |
| contracts.py | **6/6**,rc0 | Windows/sh absent là mock;5 fixture classifier gồm timeout thật |
| extra_mutations.py | **20/20** mutant chết assertion đúng test;rc0 | Bản sao tạm, không sửa launcher thật |
| merged_guards.py | **9/10** property kill đúng assertion,1 UnicodeEncodeError | Từng property độc lập; không lấy đỏ sớm của ca gộp để chứng minh property sau |
| matrix.py |47 trường hợp helper/glibc/Bash, thêm1 ghi nhận chroot không đo được | Không tự gọi47/47 pass: có 2 sai khác helper/glibc,1 là waiver,1 là F4; test uid65534 ban đầu bị setup errno22, thay bằng permission_probe đo thực tế |
| permission_probe.py |2 dạng permission ×3 oracle khớp | Cả mode 000/mode 0111 listdir thật đều EACCES 13; mode 000 chọn later, 0111 chạy unreadable |
| callers.py |8 caller ×2 mode = **16 kết quả parity** | Mọi CLI/REST/Git là fixture, không chứng minh credential thật hoặc live mạng |
| hint_validate.py / HINT.patch | NeutralUTF8 và neutral glibc **2/2**; head-vs-guard và strict-mutant **2/2 assertion đỏ** | Patch TEST thuần đã dry-run/apply-p0 trên bản sao; không chạy lên cây thật |

Các 4 mutation bị bỏ qua theo nền được in nguyên lý do trong `head-mutations.log`; không cộng vào mẫu số 517. Các 10 ca skip full suite và 13 ca lỗi đối chiếu được lưu tên nguyên vẹn trong `suite-comparison.json`.

Danh sách **13 lỗi cùng tồn tại trên HEAD/BASE** (KHÔNG ĐO ĐƯỢC trong môi trường này, không phải13 finding):

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

Các lỗi này có message `Codex home is inside a repository` hoặc không thấy lời gọi sau materializer; `/tmp/.git` là nguyên nhân môi trường đã được chỉ thị nêu trước. Delta0 được so bằng ID, không chỉ tổng13.

Danh sách **10 skip giống nhau**:

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

## BANG SAN

Mỗi hướng có lệnh và output thực tế. JSON/log giữ đủ các kết quả; chỉ sai khác có hậu quả được tính finding.

| Hướng độc lập | Lệnh từ cay-kho/ | Output thật | Phán định |
|---|---|---|---|
| PATH, `$0`, argv0 | `python3 -B ../evidence/matrix.py` | Absolute, relative, dotdot, symlink-dotdot và tên có slash giữ FIRST; `bin/` giữ `bin//cli`; native argv0=cli, đối số `a b` giữ nguyên; env=None/defpath rc0 | **KHÔNG PHẢI LỖI** ở các dạng này; shebang qua PATH rỗng thuộc waiver |
| PATH quá dài, có executable trong cwd | `python3 -B ../evidence/long_entry.py` | C glibc và coreutils chọn llm-CWD; Bash/helper chọn llm-LATER. HEAD trả CO_CREDENTIAL, cùng caller qua glibc trả CHUA_XAC_THUC | **LỖI F4 P1**, ngoài W-1077-1 |
| Lỗi exec và thứ tự lỗi cuối | `python3 -B ../evidence/matrix.py` | EACCES ưu tiên errno13; lỗi cuối ENOTDIR20/ENOENT2; ELOOP40 và ETXTBSY26 dừng; thiếu interpreter thì sang LATER | **KHÔNG PHẢI LỖI** trên errno vật lý đã đo; ba errno hiếm chưa tái hiện filesystem thật |
| Quyền thư mục và tệp thiếu bit x | `python3 -B ../evidence/permission_probe.py`; targeted.py ca(c) | listdir trả EACCES 13 cho cả mode 000 và 0111; mode 000 chọn later, 0111 vẫn exec được; tệp 0644 probe False, không quá hạn | **KHÔNG PHẢI LỖI**. Thử setuid/capsh bị sandbox chặn, đã thay bằng phép đo mode thực tế |
| Empty, BOM, ELF sai kiến trúc, cú pháp Bash | `python3 -B ../evidence/matrix.py`; contracts.py | Empty rc0 nhưng probe False vì thiếu output; BOM 127; ELF sai kiến trúc helper/glibc 2, Bash 126; cú pháp Bash helper/glibc 127, Bash 0 | **KHÔNG PHẢI LỖI** của hợp đồng glibc; không nâng empty/ELF thành phiên bản tốt |
| Retry, kwargs, số lượt, timeout | `python3 -B ../evidence/contracts.py`; extra_mutations.py | 6/6 contract; 20/20 mutant chết assertion; timeout 0.1s cho version/auth đều False, qua_han True, tổng khoảng 0.203s | **KHÔNG PHẢI LỖI**; giữ cùng timeout theo SPEC |
| Byte ngoài UTF-8 và chốt mới | `python3 -B ../evidence/targeted.py`; merged_guards.py | Neutral 11/11; strict mutant OTHER_EXCEPTION/UnicodeEncodeError trước bang; harness vẫn in OK 1/1 | **LỖI F7 P2 về assertion**; bản vá fsencode chạy đúng |
| Phạm vi caller và negative classifier | `python3 -B ../evidence/audit.py`; callers.py; targeted.py | 7 hàm trong phạm vi không spawn thẳng; 16 kết quả caller có parity; doctor ca(a) rc0, ca(b) rc12/BI_CHE | **KHÔNG PHẢI LỖI** của nối caller; hai delegate chuyển #1083 |
| Môi trường, lint, doctrine, số dòng | `python3 -B ../evidence/run_suites.py`; audit.py | 302/315 so 291/304, cùng 13 lỗi/10 skip; 517/517 harness; Ruff 17 so 17; diff check 0; doctrine 0; 334 dòng thêm | **KHÔNG PHẢI HỒI QUY** đối với 13 lỗi môi trường; phần tính mutation có F7 |
| Windows, sh vắng thật, CI exact HEAD | contracts.py; `chroot <empty-root> /bin/sh`; quét artifact theo SHA | Mock guard chỉ 1 spawn; chroot 125/Operation not permitted; không có Windows runtime hoặc CI receipt | **KHÔNG ĐO ĐƯỢC** ba điều kiện thật; không suy pass |

## FINDINGS

### F4-phan-giai-PATH [P1] Bỏ phần tử PATH quá dài làm chọn khác executable của glibc

**TEP/DONG:** `.claude/dev/launcher.py:2942` và `:2943` lọc phần tử trước vòng exec; lời khai tại `:2922`, `:2928`. Caller trong phạm vi là `_do_openai_llm:4040/4048`, rồi kết luận KHA_NANG của doctor. Đây không phải `$0` của shebang qua PATH rỗng được miễn trừ.

**VAN DE:** Helper bỏ hẳn entry dài khi dựng danh sách. Trên glibc 2.39 thật, nếu entry quá dài có dấu `:` theo sau, execvp còn thử tên công cụ trong cwd trước khi sang entry kế tiếp. Fixture đặt `llm` không shebang trong cwd và bản khác trong thư mục `later`; không có empty entry viết trong PATH. Với PATH=`'a'*4200 + ':' + later`, C execvp và coreutils `/usr/bin/env` đều chạy `llm-CWD`; helper chạy `llm-LATER`. Bash cũng chạy LATER, nên Bash không chứng minh parity glibc cho ca này.

Hậu quả đã đo: CLI trong cwd không có credential (`keys list` rc1), CLI phía sau in `openai`. HEAD `_do_openai_llm` trả **CO_CREDENTIAL / llm-LATER**; cùng caller qua C execvp thật trả **CHUA_XAC_THUC / llm-CWD**. Doctor fixture cũng ghi phiên bản LATER do helper chọn. Sai khác ảnh hưởng tới nhãn khả dụng, không chỉ text báo lỗi. W-1077-1 chỉ miễn trường hợp shebang qua entry rỗng; không miễn tất cả khác biệt với glibc hoặc mọi đường có cwd.

**DA THU NGHIEM:** `python3 -B ../evidence/long_entry.py` ghi 6 tình huống trong `long-entry.json`. Long-first/long-middle chọn CWD ở hai oracle độc lập; long-last/all-long-only không chạy cwd; short-before-long giữ MID. Dòng cuối: HEAD `[CO_CREDENTIAL,llm-LATER…]`, cùng caller qua glibc `[CHUA_XAC_THUC,llm-CWD…]`; glibc version rc0/CWD, keys rc1/rỗng. `matrix.py` tái hiện độc lập cùng sai khác ở huge-entry.

`HINT.patch` thêm biến thể 4200 byte vào ca PATH hiện có. `hint_validate.py`: ca chạy với oracle C glibc neutral PASS; với HEAD hiện tại đỏ **TinHieuChotCa** tại assertion chọn FIRST, nhận LATER. Không dùng lỗi setup hoặc exception ngoài assertion làm kill. Không soạn launcher implementation gợi ý cho runtime nhạy cảm.

**DO TIN:** Cao trên Linux/glibc 2.39 đã chạy thật; không khẳng định mọi libc/Bash cùng hành vi. Đây là phần còn mở của lớp F4/lời khai chọn tệp theo glibc, có từ c4af726; không cáo buộc fsencode sinh ra. Muốn chủ ý giữ khác biệt này cần quyết định phạm vi/miễn trừ mới của chủ kho; reviewer không tự cấp.

**Hướng xử lý bằng lời:** đối chiếu luồng cursor và dấu phân cách khi glibc bỏ segment dài, trước khi dựng candidate. Giữ các tính chất đang đúng: fallback chính candidate, relative/symlink/argv0 và tập errno. Đo cả entry dài ở đầu/giữa/cuối, cwd có/không có tool và nhãn credential phân biệt. Nếu chủ ý giữ hành vi Bash, cần đổi hợp đồng kèm authority tương ứng; sửa docstring đơn lẻ chưa đóng sai khác.

### F7-dot-bien-UTF8-khong-toi-assertion [P2] Mutant UTF-8 mới được ghi OK trước khi tới assertion của ca

**TEP/DONG:** `.claude/dev/launcher_test.py:9360`–`:9361`, `:9467`–`:9468`, tuple mới `:12420`.

**VAN DE:** Ca raw-byte mới gọi `_wp1077_llm`, nhưng helper test chỉ bắt OSError. Mutant đổi fsencode về encode strict gây **UnicodeEncodeError** trong probe. Exception thoát trước khi gán xong `kq`; `bang(kq[0] == CO_CREDENTIAL …)` chưa chạy. Harness DOT_BIEN chung đếm exception này làm kill, in `OK giet1/1 ... r1077_PATH_hop_dong_glibc(UnicodeEncodeError)`.

Exception đúng cơ chế hồi quy encoding; bản vá HEAD đã xử lý byte PATH đúng. Finding P2 là chốt mới **không đáp ứng yêu cầu rõ của lượt review**: mutant phải làm đỏ assertion của chính ca bằng bang/TinHieuChotCa; ca gộp phải khóa từng property. Không khai thành P1 runtime, không nói bốn mutant M4 bắt buộc bị sai, không lấy 517/517 harness thay bằng chứng assertion.

**DA THU NGHIEM:** `python3 -B ../evidence/targeted.py` → 11/11 neutral; 21 cặp wp1077 có 20 ASSERTION_KILL và 1 OTHER_EXCEPTION/UnicodeEncodeError. `merged_guards.py` → 9 property cũ đỏ đúng assertion, property raw-byte thoát bằng exception. `head-mutations.log` có dòng OK nói trên.

Trong bản sao, hint TEST thuần bắt thêm UnicodeError hẹp, chuyển thành dữ liệu kết quả, giữ OSError/errno cũ. `hint_validate.py`: UTF-8 neutral PASS; strict mutant giờ đỏ **TinHieuChotCa**, message `PATH byte ngoai UTF-8 lam mat probe: ('UnicodeEncodeError', …)`. Không bắt Exception tổng quát hoặc sửa harness để làm điểm xanh.

**DO TIN:** Cao; đã phân biệt exception type độc lập với bộ đếm harness. P2 cho thiếu kiểm chứng assertion theo hợp đồng review. Đề nghị kiểm qua doctor JSON thật hoặc chuyển lỗi dự kiến thành dữ liệu trước assertion, rồi đo lại strict mutant và các property đã gộp.

## HINT VA TRANG THAI CUOI

`HINT.patch` chỉ chạm `.claude/dev/launcher_test.py`; áp bằng `patch -p0 < ../HINT.patch` từ bản sao cây. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Patch đã thử trên bản sao ngoài cây review: thêm biến thể PATH dài và sửa test seam bắt UnicodeError. Numstat sau hint: test vẫn +280/-11; launcher không đổi +54/-9; tổng vẫn +334/-20, trong trần 345. Phần PATH dài chủ ý làm HEAD hiện tại đỏ; patch là gợi ý test, không phải bản vá production hoặc bằng chứng cổng đã xanh.

Hướng sửa runtime nhạy cảm chỉ mô tả bằng lời ở finding, không soạn hunk launcher. Executor tự tái dẫn xuất và chạy lại trên nhánh của mình; không apply mù. Nếu muốn đổi hợp đồng hoặc scope/waiver, cần quyết định của chủ kho.

`final-checks.json`: HEAD không đổi; git status rỗng; byte cả hai source bằng `git show HEAD:<path>`. Bản đột biến, base copy và dấu vết hook đều ngoài `cay-kho/`. Không push/merge/land/deploy, không dùng credential thật. Kết luận nội dung exact SHA: **changes_requested — 1 P1, 1 P2**. A4 CI exact HEAD còn **KHÔNG ĐO ĐƯỢC**; chưa có căn cứ báo merge-ready.
