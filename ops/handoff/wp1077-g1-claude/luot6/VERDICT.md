verdict: changes_requested
reviewed_sha: 01b973469c6cd321b9afc723adc29865164256ac
spec_sha256: eabbb725650addad531429d48801667f2ef05a6090c00123d1d4146c7b89c3f3
Ket qua: 0 P0, 1 P1, 0 P2, 0 P3.

PR #1080, packet #1077 r1/g1, review_class `sensitive`, lease theo chỉ thị `wp1077-r1-g4-claude`, lượt Codex 6/10. **F4 chưa đóng cả lớp phân giải PATH.** Thiết kế mới sửa thật ba biểu hiện ở lượt 5, nhưng còn bỏ qua lỗi exec phải dừng và thay chuỗi `$0`. Có phản chứng doctor báo `DUNG_DUOC`/0 cho executable phía sau khi bash/glibc dừng với `ETXTBSY`. Đây là một lớp P1 kế thừa F4, không tách thành nhiều finding để tăng số lượng.

Base: `086f1b7343fc1d778e50797e6c9ca0964b11a755`; HEAD tree: `940e3c18dc5bac88eb1f4ef004112 ca2b2dfc0ef`. `sha256sum ../SPEC.md` khớp băm trên; diff Git khớp nguyên byte `diff.patch`. Numstat thật: launcher **+58/-9**, test **+268/-11**, tổng **+326/-20**, hai tệp, trong trần **330 dòng thêm** được chủ kho nâng. Không lấy net +306 thay số dòng thêm.

Danh tính: `runs/287b2a60/run.json` khai provider `openai_codex`, execution_surface `codex_cli`, transport `machine`, run_id `287b2a60d309476f92c2fbf69f00ae2e`. Reviewer họ OpenAI/Codex, context review riêng với executor Claude theo phân công. Metadata này không attest chính xác model/effort phục vụ; không suy chúng từ tài khoản đăng hoặc commit. Agent phụ `tl_auditor` chỉ đọc log, theo yêu cầu cụ thể tại CLAUDE.md bước 5; reviewer chính tự đo phản chứng và đối chiếu kết luận.

Không gọi công cụ mạng, fetch/push, đăng review hay dùng credential thật. CLI fixture chỉ in dữ liệu kiểm thử cục bộ; ca doctor có `kiem_song=True` bên dưới chạy **llm giả**, không gọi dịch vụ hoặc quota. Môi trường test được dựng từ danh sách biến cho phép, HOME/config riêng, `PIP_NO_INDEX=1`, `UV_OFFLINE=1`, `PYTHONDONTWRITEBYTECODE=1`; không truyền môi trường chứa credential thừa kế. Linux x86_64, Python **3.13.16**, glibc **2.39**, Bash **5.2.21**, `/bin/sh` của container là dash, PATH_MAX **4096**. Ruff bare lint **0.16.8**, cache tắt.

## LENH VA BANG CHUNG

Các lệnh dưới chạy được từ `cay-kho/`; script tự neo đường dẫn source HEAD trong thư mục review này. Log/JSON/bản sao/đột biến đều nằm trong `../evidence/`. Runner full test thực sự chạy Python3 với cwd đúng cây tương ứng, ghi rc thật vào JSON và journal từng ca; không lấy rc của lệnh bọc làm pass.

```sh
python3 ../evidence/run_suite.py head .
python3 ../evidence/run_suite.py base ../evidence/base-copy
python3 ../evidence/run_suite.py mutation . --dot-bien
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/checks.py
cc ../evidence/execvp.c -o ../evidence/execvp-glibc
cc ../evidence/argv0.c -o ../evidence/argv0-native
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/semantics.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/contracts.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/mutate_contracts.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/platform_edges.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/new_guards.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/doctor_edges.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/claims_dynamic.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/audit.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/historical_master.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/environment_probe.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/snapshot_final.py
```

Trong các bảng: **P** = `checks.py`; **S** = `semantics.py`; **C** = `contracts.py`; **CM** = `mutate_contracts.py`; **E** = `platform_edges.py`; **G** = `new_guards.py`; **D** = `doctor_edges.py`; **Q** = `claims_dynamic.py`; **I** = `audit.py`. Mỗi ký hiệu là lệnh đầy đủ ở trên và file `.log`/`.json` cùng gốc tên trong evidence. `claims_inventory.md`, `call-sites.json`, `ruff-summary.json`, `head/base/mutation.{log,json}` và các journal giữ chứng cứ chi tiết. Bản base xuất bằng `git archive` từ đúng OID, không checkout hoặc sửa nhánh executor.

## DOI CHIEU TUNG FINDING CU

| Finding / nguồn | Đo lại ở HEAD | Kết luận |
|---|---|---|
| F1 — probe còn bỏ sót / lời khai “mọi probe”, lượt 1/2/4 | I liệt kê mọi spawn và caller; P kiểm 7 hàm CLI; docstring :2936–2938, test :9370+, comment mutant :12393 đều nói phạm vi thu hẹp | Phần CLI được giao và lời khai đã sửa. `_git` / `_do_codex_song` vẫn chưa vá runtime, **chuyển #1083 theo chủ kho**, không gọi là đã vá hoặc finding mở packet này |
| F2 — đồng nhất bash với `/bin/sh`, lượt 1 | S: bashism Bash 0/`x`, glibc/helper 2; ELF sai kiến trúc Bash 126, glibc/helper 2. Docstring hiện nêu rõ bash dùng chính bash | Đã sửa lời khai, không mở lại khác biệt được SPEC M1 chủ ý chọn |
| F3 — thiếu chốt argv/env, lượt 1 | P ca retry giữ đối số có khoảng trắng + env xanh; mutant mất đối số chết đúng TinHieuChotCa. C/CM giữ toàn bộ kwargs, một retry, rc gốc | Đã vá phần được giao và có chốt thật |
| F4 — chọn sai tệp / đổi ngữ nghĩa PATH, lượt 2–5 | P: 3 ca mới hiện xanh và đều đỏ đúng assertion trên `4fa4720` (cwd dài, `$0` tương đối, interpreter thiếu). S/G/D có phản chứng còn lại | Ba biểu hiện lượt 5 đã sửa thật; **cả lớp chưa đóng**, P1 dưới đây |
| F5 — khai +228 sai, lượt 2 | I: BASE..dcfb011 +48/-9 và +188/-10 ⇒ **+236/-19**; BASE..e6bf386 +56/-9 và +211/-15 ⇒ **+267/-24** | Đính chính của e6bf386 đúng ở head đó. Handoff dự kiến không có trong bundle: **không đo được việc ghi đính chính vào handoff**, không suy đã hoàn thành |
| F6 — nói t103 không so tên lệnh, lượt 3 | I/đọc source: t103 vẫn có `cmd[:2] == ["gh", "api"]`, hai nhánh đều Rc(0); message1027f85 đã đính chính. t103/t111/t113 AST HEAD bằng BASE; mutation github cũ vẫn bị giết đúng t111 | Đã đính chính lời khai; các sửa đồ giả lượt 2 được gỡ như message HEAD nói. t115 chỉ bỏ qua thêm khóa `executable` |

Bảng lớp: giữ slug lượt 5 **`F4-phan-giai-PATH`**, nối các tên lịch sử `F4-ten-tran-bo-qua-wrapper-dau` → `F4-PATH-rong-van-bo-qua-wrapper-dau` → `F4-chon-sai-executable`. Một lớp còn mở, sáu biểu hiện đo được ở lượt này: ETXTBSY, ELOOP, ENAMETOOLONG ở một component PATH, errno cuối bị ưu tiên sai, `$0` với phần tử rỗng, `$0` với dấu `/` cuối. Chúng cùng thuộc hợp đồng tái hiện execvp, không phải sáu lớp mới. U lượt 5 có một lớp; F đóng toàn lớp ở lượt 6 bằng0 ⇒ **0/1 =0%**; không xóa lịch sử lặp vì đã đổi thiết kế. Chủ kho đã cấp lượt 6/10 sau checkpoint trước đó; lượt này ghi bằng chứng, không tự cấp lượt7 hoặc đổi phạm vi.

## BANG NGHIEM THU

| Tiêu chí | Lệnh | Output thật | Đạt? |
|---|---|---|---|
| M1 — helper chung, guard ENOEXEC/POSIX/sh-file, một retry, cùng tham số | C, CM, P, S, G, D | C 14/14; CM 14/14 mutant chết đúng assertion. Đường có `/` giữ nguyên exception khác ENOEXEC và chỉ spawn một lần; retry giữ argv/kwargs/rc. Tên trần vẫn chọn sai tệp hoặc đổi `$0`; D cho doctor 0 đo nhầm bản sau | **Không đạt toàn bộ hợp đồng được yêu cầu đối chiếu execvp**, F4. Cơ chế retry trực tiếp đạt |
| M2 — hai classifier dùng helper, đủ caller trong phạm vi | I, P | `_phien_ban`:2991 và `_xac_thuc_kem_dau_ra`:3043 gọi helper; codex/llm/gh/claude MCP cũng nối helper | **Đạt phạm vi đã thu hẹp** |
| M3(a) — rg/git wrapper tốt đầu PATH | P | Cả rg và git: doctor 0, co=True, version có `khong-shebang`, không bi_che | **Đạt** |
| M3(b) — wrapper exit 1 vẫn BI_CHE | P | doctor 12, trạng thái BI_CHE | **Đạt** |
| M3(c) — shebang hợp lệ, thiếu bit x | P, C | 0644 → EACCES; version=False, qua_han=False, một spawn; mutant mọi OSError chết đúng ca(c) | **Đạt** |
| M3(d) — auth wrapper in một dòng, rc 0 | P | HEAD True/Logged in; BASE False/OSError; mutant bỏ helper chết đúng ca(d) | **Đạt** |
| M4 — bốn mutant bắt buộc giết đúng ca | P, full mutation | Bỏ retry 2/2; mọi OSError 1/1; auth bỏ helper 1/1; bỏ rc 1/1. Cả 5 cặp TinHieuChotCa; toàn 12 mutant wp1077 có 18/18 cặp đúng assertion | **Đạt** |
| A1 — suite, ngoại lệ môi trường có delta 0, mutant mới | Runner HEAD/BASE/mutation, P | HEAD 292/316 (326 tổng, bỏ 10, lỗi 24); BASE 280/304 (314 tổng, bỏ 10, lỗi 24); cùng ID lỗi+bỏ qua. Cả 12 ca thêm xanh. Mutation 514/514, bỏ 4 | **Đạt phần delta 0 theo ngoại lệ SPEC**; không gọi full suite xanh hoặc coi 24 ca lỗi là passed |
| A2 — (a),(d) đỏ trên BASE | P, nhóm BASE-counterexample | 2/2 TinHieuChotCa: rg 12/BI_CHE; auth False/OSError | **Đạt**, đúng assertion của chính ca |
| A3 — tái hiện Issue tại chỗ | P, ca(a) gọi lenh_doctor thật | HEAD rg/git: 0/co=True/FIRST/không bi_che; BASE rg: 12. Fixture chỉ giữ công cụ cần đo và tắt KHA_NANG ngoài ca | **Đạt tái hiện tập trung**; không khai doctor toàn máy xanh |
| A4 — Ruff F delta 0 | Bare Ruff dưới đây; ruff-summary.json | launcher 0 F; test 5 F841; tl.py 12 F821, giống nhau ở HEAD/BASE. 17→17, delta 0; rc 1 cả hai | **Đạt delta**, không khai Ruff tuyệt đối xanh |
| A4 — diff check, doctrine | `git diff --check BASE HEAD`; `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py doctrine-scan --root .` | Diff check rc 0; doctrine rc 0, sạch, quét 10 tệp, 0 chỗ chép doctrine | **Đạt hai check cục bộ** |
| A4 — CI xanh trên exact HEAD | Không gọi mạng theo chỉ thị; không có receipt/log CI trong bundle | **KHÔNG ĐO ĐƯỢC** | **A4 tổng thể chưa đủ chứng cứ**, không coi CI xanh hoặc là hồi quy |

Bare lint thực sự dùng Ruff 0.16.8, từ mỗi cwd HEAD/base tương ứng:

```sh
/root/.local/bin/ruff check --no-cache --select F --output-format json .claude/dev/launcher.py .claude/dev/launcher_test.py scripts/tl.py
```

So diagnostic bằng `(tệp,code,message,count)`, bỏ tọa độ dòng dịch do thêm code; mọi nhóm trùng. Đây là **bare lint**, không phải kiểm hợp đồng pin/version của workflow; contract pin không chạy, không lấy lint thay chứng nhận CI.

## BANG DO

Cách tìm khẳng định: I phân tích **toàn bộ** dòng thêm `git diff BASE HEAD`, tokenize mọi COMMENT giao dòng thêm, AST mọi docstring giao dòng thêm; đọc toàn bộ thân hai hàm mới, caller đổi, các test và tuple DOT_BIEN; đọc nguyên message `git log -1 --format=%B HEAD` và các message e6bf386/57e2d4a/1027f85 để đối chiếu đính chính. Danh mục nguyên văn ở `claims_inventory.md`; bảng sau nhóm theo đơn vị nghĩa, không coi vài từ khóa grep là đủ.

| Khẳng định | Diff khai / vị trí | Đo được (lệnh) | Khớp? |
|---|---|---|---|
| Helper “CHỌN TỆP như execvp glibc” | launcher:2922; message HEAD tiêu đề/thiết kế | S ETXTBSY/ELOOP/ENAMETOOLONG và G/D | **Không**, F4 |
| Subprocess có `/` ném ENOEXEC; tên trần có thể bỏ wrapper và chạy bản sau | :2924–2926 | Q: absolute errno 8; bare rc 0/`LATER` | Có |
| glibc fallback `/bin/sh`; bash dùng chính bash | :2927; comment test wp1077 | S bashism 0/`x` so helper/glibc 2; binary Bash 126 so sh 2 hoặc 127 | Có giới hạn đã công bố |
| Duyệt `os.get_exec_path(env)` theo thứ tự | :2929,:2946; message HEAD | S PATH tuyệt đối/tương đối/thiếu PATH/env None,first/later | Có thứ tự; không đủ chứng minh parity toàn bộ |
| “giữ nguyên dạng” ứng viên | :2929–2930; message HEAD | S `first/` helper`first/probe`,glibc`first//probe`; G wrapper phụ thuộc chuỗi trả CHUA_XAC_THUC | **Không đầy đủ**, F4 |
| Phần tử rỗng là `./tên` và không đổi ngữ nghĩa glibc | :2930,:2946 | S PATH='' helper`$0=./probe`,glibc/bash`probe`; G version/auth False so positive True | Code tạo`./` đúng như mô tả, **suy parity sai**, F4 |
| Không ghép cwd/không abspath, giữ symlink/.. | :2930; message HEAD | S symlink_dotdot FIRST; cwd 4311 chạy được; P ba ca lượt 5 đỏ trên 4fa, xanh HEAD | Có với các dạng đã đo |
| `executable=` giữ argv[0] | :2931; message HEAD; gỡ sửa đồ giả | S native C: helper/glibc/bash đều `argv0=native argc=2 arg1=two words`; I AST t103/t111/t113 bằng BASE | Có; khác vấn đề `$0` của script fallback |
| ENOENT/ENOTDIR/EACCES/interpreter thiếu chuyển ứng viên sau | :2931–2932; message HEAD | S các ca tương ứng đều helper/glibc 0/LATER; interpreter thiếu Bash 127 dừng | Có theo glibc; **bash khác** ở interpreter thiếu, không khai hai cái đồng nhất |
| Mọi errno còn lại được xem như lỗi tìm kiếm | Thân :2954–2958 dù lời khai chỉ nêu ví dụ “…” | S ETXTBSY helper 0/LATER,glibc errno 26/Bash 126; ELOOP errno 40; component 256 errno 36 | **Sai với glibc**, có hậu quả caller thật trong D |
| Hết ứng viên ném lỗi đầu khác ENOENT/ENOTDIR theo CPython | :2933,:2957–2959 | S EACCES→ENOENT/đảo thứ tự đều 13; ENOTDIR→ENOENT cuối 2; EACCES→ELOOP helper 13/glibc 40 | **Đúng mô tả quy tắc CPython**, nhưng không đúng lời hứa parity glibc của helper |
| ENOEXEC dừng ở đúng file, không sang bản tốt sau | :2932,:2952–2955 | P/S FIRST thắng LATER; rc 1 vẫn lỗi; mutant bỏ helper/resolution chết đúng assertion | Có cho các trường hợp tương ứng |
| Chỉ ENOEXEC retry; sh phải là file | :2952 | C/CM 14/14; mock sh-vắng: 1 spawn, giữ ENOEXEC. E thử chroot thật bị EPERM | Đạt guard/mutation; **chưa đo sh-vắng thật** |
| Cùng env/stdin/timeout/mã hóa/argv, chỉ một lượt retry | M1 và `**kw`; helper llm:2961–2967 | C exact kwargs/args/rc; P env và khoảng trắng; Q UTF-8 lỗi thành U+FFFD, stdin DEVNULL EOF; S timeout thật | Có; CM giết 14/14 đúng assertion |
| Kết quả retry phân loại y như thường | :2934; probe:2991/3043 | C: rc 0 rỗng False,output + rc 1 False,rc 0 output True,BOM False,timeout True. P b/d+mutant | Có ở hai classifier, không chữa được chọn sai executable |
| Windows giữ nguyên | :2941–2942 | C/CM mock nt: 1 spawn, giữ exception; native Windows không có | Đạt guard bằng mock+mutation; **không suy native Windows pass** |
| Phạm vi CONG_CU/KHA_NANG trừ `_git`/`_do_codex_song` | :2936–2938; test cấu trúc; comment DOT_BIEN | I liệt kê 30 call-sites, xem bảng probe dưới; P AST 7 hàm không spawn trần | Khớp phạm vi đã thu hẹp; không tính hai khoản #1083 thành finding |
| `_chay_probe_llm` như text-safe về utf8/replace,DEVNULL,timeout | :2961–2967; caller llm 3 lượt | Q kwargs hiệu lực bằng nhau; hàm cũ truyền cwd=None, mới bỏ khóa cwd với cùng mặc định; P: llm wrapper xanh | Có về hợp đồng caller hiện tại |
| M3(a–d) và codex status/llm thật, test structural chỉ khóa danh sách nêu rõ | test mới,docstring từng ca | P: 12/12 neutral và 18/18 target kills; hai phản chứng BASE | Có trong phạm vi ca; không suy cả lớp PATH đã khóa |
| Các ca PATH đủ rỗng/tương đối/dotdot và3 ca HINT lượt 5 | test:9400+; message HEAD | P/S/G: ca hiện có xanh; 3 ca HINT đỏ đúng assertion ở 4fa; G tìm thêm 3 guard đỏ HEAD | Mô tả từng ca khớp; không bao phủ mọi `$0`/errno |
| Mutant đổi theo helper mới, thêm dừng ở lỗi tìm kiếm | DOT_BIEN:12380–12411; message HEAD | P: 12 mutant, 18 targets,compile được,anchor duy nhất,đúng TinHieuChotCa | Có; mutant “dừng mọi lỗi” không khóa chiều ngược lại “nuốt lỗi cứng” |
| T115 chỉ bỏ qua thêm `executable`, t121 đổi stub sang helper llm | diff test:3766,4222+ | Đọc toàn diff; full suite các ca đó xanh,mutation đúng t111/t121; I t103/t111/t113 không đổi AST | Có; không lấy đồ giả này thay phép đo executable thật |
| Số dòng HEAD / lịch sử e6 / đính chính dcfb | Message HEAD/I; trần SPEC đã được chủ kho sửa | HEAD +326/-20; e6 +267/-24; dcfb +236/-19 | Có; handoff chưa có để đo |

Đo thêm lời khai lịch sử tại docstring: `python3 ../evidence/historical_master.py` xuất source đúng object `2bcd8f3`; cả rg/git wrapper không shebang cho probe phiên bản False/errno 8, bash rc 0 và in phiên bản. Điều này xác nhận cơ chế lỗi trên master cũ; không tái chứng nhận toàn bộ review độc lập #823 từ metadata.

## CAC DUONG PROBE VA SPAWN

I quét AST toàn `launcher.py`, tìm mọi `subprocess.run/Popen` và lời gọi helper/classifier, rồi đọc caller, bảng cấu hình và delegation sang `codex_cred.py`. `call-sites.json` có **30 call-sites**. Không lấy danh sách 7 hàm của test cấu trúc làm giới hạn kiểm tra.

| Đường / công cụ | Lệnh quyết định kết quả | Helper / phạm vi |
|---|---|---|
| CONG_CU: git, python, claude, codex, rg, bash, gh, npm, node, llm, agy, actionlint, shellcheck | `--version`, kể cả retry quá hạn tại :5052/5069 | `_phien_ban`:2991 → helper. Được giao; `_AP_DUNG_BI_CHE` vẫn là `{rg,git}` |
| CONG_CU auth: claude và agy | `claude auth status`, `agy models`, retry và cache tại :5103/5114 | `_xac_thuc_kem_dau_ra`:3043 → helper. `_xac_thuc`:3012 chỉ bọc kết quả, không spawn thêm |
| KHA_NANG codex | `codex login status` bằng đường resolve | :3938 → helper; được giao |
| KHA_NANG openai-llm | `llm --version`, `llm keys list`, `llm prompt … --no-log` | :4044/4052/4066 → `_chay_probe_llm` → helper; được giao |
| KHA_NANG antigravity | `agy models`; version khi gọi độc lập; trong doctor đọc cache auth | :4109/4127 → auth/version → helper; được giao |
| GitHub gh-cli / gh-kho | `gh auth status`, `gh api repos/<slug> --jq .full_name` | :4575/4636 → helper; được giao |
| GitHub MCP CLI | `claude mcp get <tên>` | :4377 → helper; được giao. REST/MCP endpoint dùng HTTP, không phải shell/CLI |
| KHA_NANG claude | Tìm CLI, kiểm file/biến credential | Không spawn thêm; version/auth đã qua helper. Không thực đo credential thật |
| GitHub git transport, workspace/remote, so hook/launcher với master | `_git`:286 → subprocess.run | **Chưa phủ**, dùng chung `run`, đã chuyển #1083 theo chủ kho; không tính finding packet này |
| Codex kiểm sống | `_do_codex_song` → `codex_cred._kiem_song` → subprocess.run tại codex_cred:197 | **Chưa phủ**, ngoài write set, đã chuyển #1083. Đường chuẩn bị `_probe_snapshot`:3620 cũng ủy quyền `_kiem_song`; không thực đo credential thật |
| Hook/launcher cũ, UTF-8, đường dẫn kho, module Python | Đọc file/so source, `find_spec`, hoặc `_git` đã nêu | Không có CLI spawn bổ sung trong phần được giao |
| `_probe_spawn`:1144 | Công cụ do người gọi chọn → text-safe:319 | **Ngoài phạm vi SPEC**, đường `run` |
| text-safe/json-strict:319/333, Popen:2299 | Transport text/JSON hoặc child của `run` | Ngoài phần probe doctor; không đổi helper dùng chung |
| ps:371/455/508/706, taskkill:883 | Định danh PID, nhóm/cây process, dọn child | Điều khiển process/run, không phải probe nhãn công cụ doctor; nhánh Windows ngoài phạm vi |
| codex_cred:133 | Popen device-auth | Luồng đăng nhập ngoài write set; không chạy credential thật |

Không tìm thấy probe CLI còn spawn trần trong **phần được chủ kho giao vá**. Wiring F1 đạt không chứng minh lựa chọn executable của helper đúng; đó là F4.

## BANG TEST

| Bộ | N/M thật | Bỏ qua / giới hạn |
|---|---|---|
| HEAD, suite với `--nhat-ky` | **292/316**, rc 1; tổng 326, lỗi 24 | **10**; không gọi suite xanh |
| BASE, cùng suite/env | **280/304**, rc 1; tổng 314, lỗi 24 | **10**, cùng ID/lý do; delta lỗi 0 |
| HEAD `--dot-bien` | **514/514**, rc 0; tổng 518 | **4 không đo được**. 39 dòng ngoài wp1077 có hậu tố exception; không khai 514 assertion kills |
| P: wp1077 neutral | **12/12** | 0 |
| P: 12 mutant wp1077 | **18/18 cặp target chết TinHieuChotCa** | 0; cả 5 cặp của bốn mutant M4 đúng ca đích |
| P: BASE (a),(d) | **2/2 đỏ đúng TinHieuChotCa** | Đúng bệnh, không phải lỗi setup |
| P: ba ca lượt 5 trên 4fa4720 | **3/3 đỏ đúng TinHieuChotCa** | Cùng ca tại HEAD xanh 3/3 |
| C / CM: hợp đồng bổ sung | **14/14 neutral; 14/14 mutant chết đúng TinHieuChotCa** | nt và sh-vắng là mock có mutation kiểm guard |
| G: ba guard F4 mới | **HEAD đỏ 3/3; đối chứng xanh 3/3; mutant chết đúng target 3/3** | Toàn 15 ca r1077 cũ+mới xanh trên đối chứng; không suy full suite của đối chứng xanh |
| S: ma trận thật | **40 trường hợp**, mỗi trường hợp chạy helper, glibc C, bash | Có lệch thật trong bảng săn; không biến thành 40/40 pass |
| E: quyền directory | **3 dạng × 3 engine**, output thật | 0111 → FIRST; 0444/0000 → LATER. uid 0 nhưng CapEff 0 nên DAC vẫn được thử thật |
| E: `/bin/sh` vắng thật | **KHÔNG ĐO ĐƯỢC** | Chroot EPERM; không sửa `/bin/sh` host |
| Native Windows / CI exact HEAD | **KHÔNG ĐO ĐƯỢC** | Linux và chỉ thị không mạng; mock không thay native |

HEAD/base có đủ `vao/ra` lần lượt 326/326 và 314/314, đều kết `# XONG TRON VEN`. Không dùng dòng stdout cuối để suy vị trí ca chết.

Mười ca bỏ qua (HEAD và base giống nhau):

| ID | Lý do thật |
|---|---|
| `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125` | fixture nay danh cho Windows; ban POSIX la t63 (chay duoc, khong bo qua) |
| `r345_chan_socket_that_ma_than_hook_van_chay_dung` | KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang) |
| `r345_cac_phep_do_cuc_bo_van_dung` | KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang) |
| `r345_lop_tham_import_van_co_rang` | KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang) |
| `r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO` | KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang) |
| `r347_tham_import_van_song_tren_python_truoc_310` | KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang) |
| `r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO` | KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang) |
| `r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia` | KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang) |
| `r348_dot_bien_bo_isidentifier_lam_ca_dich_DO` | KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang) |
| `r484_g4_windows_sid_alias_identity` | BO QUA native Windows SID conversion |

Bốn mutant không đo được:

| Mutant | Lý do thật |
|---|---|
| `g4_windows_sid_alias_not_normalized` | KHONG DO DUOC tren nen nay (native SID conversion) |
| `g4_windows_LA_not_current_owner` | KHONG DO DUOC tren nen nay (native SID conversion) |
| `g2_windows_directory_pin_access` | KHONG DO DUOC tren nen nay (native Windows share-delete pin) |
| `124_khi_chau_con_song` | KHONG DO DUOC tren nen nay (ca dich bo qua: t62_qua_han_ma_khong_giet_het_cay_phai_tra_125) |

Hai mươi bốn ID lỗi giống hệt giữa HEAD và base (không coi là hồi quy):

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

`ls -d /tmp/.git` đã đo trước kết luận: tồn tại, rỗng; không xóa để làm xanh test. Log thể hiện `Codex home is inside a repository`, `/var/tmp` readonly, credential bị chặn làm không có `runs`; t53 trong PATH sạch thiếu CLI agent. BASE cùng điều kiện có đúng các lỗi đó. Ghi **KHÔNG ĐO ĐƯỢC do môi trường** cho nội dung các ca này; chỉ khẳng định delta0, không coi chúng passed.

## BANG SAN

Mỗi hướng có lệnh tái lập (ký hiệu được định nghĩa ở phần lệnh) và output thật.

| Hướng độc lập | Lệnh | Output thật / kết luận |
|---|---|---|
| 1. ENOEXEC và first/later, wrapper lỗi | P, Q, S | Raw subprocess: absolute errno 8, bare LATER. HEAD doctor rg/git 0/FIRST; wrapper exit 1 → doctor 12/BI_CHE. **KHÔNG PHẢI LỖI ở cơ chế ENOEXEC đã vá** |
| 2. Quyền file/directory | P, C, CM, E | File 0644 → EACCES, version False, không retry. Directory 0111 → FIRST, 0444/0000 → LATER ở cả ba engine. **KHÔNG PHẢI LỖI** |
| 3. PATH absolute/relative/./../symlink | S, P | absolute, first, ./first, first/../first, link/.. đều FIRST; ba ca lượt 5 đỏ ở 4fa, xanh HEAD. **Biểu hiện cũ đã vá** |
| 4. `$0` khi PATH rỗng/trailing slash | S, G | PATH='' → helper ./probe, glibc/bash probe. PATH first/ → helper và bash first/probe, glibc first//probe. G cho probe False hoặc CHUA_XAC_THUC; đối chứng True/CO_CREDENTIAL. **LỖI F4** |
| 5. Errno tìm kiếm / errno cứng | S, D, G | ENOENT/ENOTDIR/EACCES tiếp tục đúng. ETXTBSY: helper 0/LATER, bash 126, glibc errno 26. ELOOP: helper 0, glibc 40. Component dài 256: helper 0, glibc 36. Doctor HEAD 0/DUNG_DUOC, đối chứng 13/KHONG_DO_DUOC. **LỖI F4** |
| 6. Lỗi cuối | S | EACCES→ENOENT và đảo thứ tự đều 13; ENOTDIR→ENOENT cuối 2; EACCES→ELOOP cho helper 13, glibc 40. **LỖI F4 với glibc**, mô tả riêng quy tắc CPython vẫn đúng |
| 7. PATH vắng/env None/Unicode/native argv0 | S | env thiếu PATH vẫn chạy env, có MARK=value; env None → FIRST; đường có dấu cách/Unicode → FIRST. Cả ba engine in `argv0=native argc=2 arg1=two words`. **KHÔNG PHẢI LỖI** |
| 8. Cwd vượt PATH_MAX | S, P | getcwd dài 4311, PATH='' vẫn FIRST ở cả ba; test PATH='.' giết mutant abspath. **Lỗi cwd lượt 5 đã vá**, còn lệch `$0` như hướng 4 |
| 9. Rỗng/BOM/ELF sai kiến trúc/bashism | S, C | Empty rc 0 nhưng probe False vì rỗng; BOM rc 127/False; ELF ARM trên x86_64: helper/glibc 2, bash 126; bashism: helper/glibc 2, bash 0/x. **KHÔNG PHẢI LỖI theo hợp đồng glibc/sh của SPEC** |
| 10. Timeout/stdin/encoding/kwargs | C, CM, Q, S | Retry timeout 0.1 s → qua_han True ở hai probe; DEVNULL cho EOF; UTF-8 lỗi → U+FFFD; kwargs/args/rc giữ đúng, 14 mutant chết đúng assertion. **KHÔNG PHẢI LỖI ở điều kiện đã đo** |
| 11. Caller/probe ẩn | I, P | Bảy hàm CLI qua helper; toàn 30 call-sites được đọc lại; hai khoản #1083 còn spawn trần nhưng đã được chủ kho loại khỏi packet. **KHÔNG TÍNH LỖI ngoài phạm vi** |
| 12. Sh vắng / Windows thật / CI | E, C, CM | Chroot thật EPERM; mock sh-vắng/nt một spawn và mutant đỏ; không có native Windows/CI. **KHÔNG ĐO ĐƯỢC phần thật**, không suy pass |

## FINDING CON MO

### F4-phan-giai-PATH [P1] Helper vẫn không giữ hợp đồng execvp: nuốt lỗi exec và đổi `$0`

**TEP/DONG:** `.claude/dev/launcher.py:2946` (chuỗi ứng viên), `:2954`–`:2959` (tiếp tục trên mọi OSError còn lại/ưu tiên errno), cùng lời khai tại `:2922`, `:2929`–`:2933` và message commit HEAD. Caller có hậu quả: `_do_openai_llm:4044` và đường `lenh_doctor` (vòng KHA_NANG). Test hiện tại `r1077_PATH_*` chỉ chặn một số dạng, chưa khóa chiều “không tiếp tục khi errno cứng”.

**VAN DE:** vòng lặp xem mọi OSError khác ENOEXEC như lỗi tìm kiếm có thể bỏ qua. Kernel trả `ETXTBSY` khi executable đầu PATH đang mở để ghi; glibc execvp và bash dừng ở nó. Helper bỏ qua rồi chạy executable phía sau, đo nhầm công cụ. Với `llm` giả phía sau trả thành công, doctor có thể nâng thành `DUNG_DUOC`/rc 0 dù lệnh người dùng gọi bị chặn ngay ở đầu PATH. ELOOP và ENAMETOOLONG ở component PATH cũng cho thấy helper không theo quy tắc glibc; không mặc định chúng đều giống Bash, vì Bash có cách tìm riêng.

Đây còn là lỗi lời khai đo được: câu bao “CHỌN TỆP như execvp glibc” không đúng. Quy tắc lưu exception kiểu CPython ở cuối được mô tả đúng như CPython, nhưng không thể dùng nó làm bằng chứng parity glibc. Ca EACCES rồi ELOOP cho helper errno 13, glibc errno 40.

Cùng lớp hợp đồng chuỗi ứng viên: `os.path.join(d or '.',name)` đổi phần tử rỗng thành `./name` và bỏ một dấu phân cách khi d đã kết thúc bằng `/`. Native argv[0] được giữ bởi `executable=`, nhưng `$0` của shell fallback là đối số file `tep`. PATH='' cho helper`./rg` trong khi glibc/bash`rg`; PATH='bin/' cho helper`bin/llm`,glibc`bin//llm` (Bash khớp helper ở trường hợp này). Wrapper có kiểm `$0` chuyển từ chạy được sang rc42, hai probe trảFalse hoặc llm báoCHUA_XAC_THUC. Đã đo trên API probe thật; không khai biến thể PATH='' của `_phien_ban("rg")` là một đường doctor bình thường, vì bộ chọn CONG_CU hiện thường đưa đường tuyệt đối và shutil.which(PATH='') cũng có giới hạn riêng. Hậu quả doctor thực tế của finding được chứng minh độc lập bằng ETXTBSY.

**DA THU NGHIEM:**

```sh
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/semantics.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/new_guards.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/doctor_edges.py
```

- S `ETXTBSY_then_good`: helper rc 0/LATER; glibc driver `execvp_errno=26`, rc 126; bash rc 126, “Text file busy”. ELOOP cho helper 0/LATER, glibc errno 40. Component PATH dài 256 cho helper 0/LATER, glibc errno 36. Entry dài 4200 được cả ba bỏ qua để chạy bản sau; không gộp nó với component 256.
- D giữ cùng fixture first/last: **HEAD doctor_rc=0, openai-llm=DUNG_DUOC, detail có llm-LATER**; bản đối chứng tạm trả **13/KHONG_DO_DUOC/OSError**. Probe khác được tắt, HOME/env riêng, prompt fixture chỉ echo nên không có dịch vụ hay credential thật thay đổi giữa A/B.
- G: ba guard mới đỏ trên HEAD bằng **TinHieuChotCa của chính test**, cùng fixture xanh 3/3 trên đối chứng. Đột biến đảo từng tính chất làm ca đích đỏ 3/3. Không nhận OSError/AttributeError/SyntaxError làm kill. Toàn 15 ca r1077 cũ+mới xanh trên đối chứng.
- Guard `$0` chết bởi `(False,rc42)` hoặc `CHUA_XAC_THUC`; guard ETXTBSY chết bởi `CO_CREDENTIAL,llm-LATER`, không phải lỗi thiếu file/setup. JSON giữ kết quả từng variant.

**DO TIN:** cao cho Linux/glibc 2.39/bash 5.2.21 đã chạy thật. Một lớp P1 vì chọn sai executable và nâng nhãn sai; không thêm finding riêng cho lời khai cùng cơ chế. Subprocess tên trần ở BASE cũng bỏ qua ETXTBSY: đây là **lỗ hổng còn lại của hợp đồng F4 và lời khai helper mới**, không khai là hồi quy mới chỉ xuất hiện ở 01b9734. Không suy parity trên Windows/BSD hay errno chưa tái hiện vật lý.

Hướng sửa bằng lời: phân biệt errno glibc cho phép tiếp tục với errno phải dừng; giữ riêng chuỗi ứng viên logic cho fallback và đường có `/` để ngăn CPython tìm PATH lần nữa; giữ argv[0]; bảo toàn ưu tiên lỗi cuối đúng hợp đồng đã chọn. Đối chiếu cả PATH kết thúc bằng phần tử rỗng, EACCES, ENOENT/ENOTDIR, ESTALE/ENODEV/ETIMEDOUT, lỗi cứng và `/bin/sh` vắng, thay vì chỉ thêm điều kiện cho ETXTBSY. Không có filesystem phù hợp để đo thật ESTALE/ENODEV/ETIMEDOUT trong container; không khai đã đo chúng. Phải giữ việc interpreter đầu thiếu vẫn sang bản sau theo glibc, không quay về pre-resolve lượt 5.

## HINT VA PHAM VI GHI

`../HINT.patch` **chỉ chứa test**, áp `patch -p0` từ `cay-kho/`. Nhãn theo protocol: **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**. Không có hunk sửa launcher runtime trong HINT vì protocol §8 hạn chế runtime hint cho packet sensitive; hướng sửa runtime ở trên là mô tả bằng lời. Scratch positivecontrol chỉ dùng để chứng minh fixture có thể xanh và mutant có răng; không phải commit/approval hay bản vá được phép chép mù.

Đã `patch --dry-run -p0` rồi áp thật trên `evidence/hint-copy`, và ba guard trong patch đã được chạy bằng cùng source test/fixture qua G. HINT thêm 41 dòng test; nếu cộng nguyên vẹn vào candidate 326 thì thành 367 > 330. **Đây là artifact phản chứng, không phải phương án commit nguyên vẹn trong budget hiện tại**: executor cần tích hợp các assertion vào ca hiện có/tinh gọn bố cục để tổng BASE..HEAD ≤ 330, hoặc có authority mới trước khi tăng budget. Số 367 không phải số dòng của HEAD đang review. Không sửa branch/source để “chuẩn bị sẵn” patch runtime.

## KIEM TRA READ-ONLY VA GIOI HAN

Sandbox thực tế là workspace-write; chỉ thị reviewer read-only không tự biến sandbox thành mount readonly. Hash hai tệp được đo trước test và sau test giống nhau. Cuối lượt HEAD/tree giữ nguyên; `git status --short --ignored` rỗng; 9.125 blob tracked kiểm khớp Git sau chuẩn hóa EOL checkout của ba tệp.cmd (`deploy-package.cmd`,`don-nhanh.cmd`,`tl-setup.cmd`:CRLF↔LF). `snapshot-final.json` không có content/mode mismatch. Toàn inventory thu trong giai đoạn đầu so cuối chỉ khác hiện vật marker được dọn như mô tả dưới; không có full-tree snapshot trước khi test bắt đầu, không dùng ảnh này để chứng minh “chưa từng ghi”.

**Tác dụng phụ đã xảy ra:** test cũ t152 chạy hook canonical mà không đặt CLAUDE_PROJECT_DIR, sinh `.claude/.packet_state/session-start.ran` lúc 14:49:00Z với nội dung `2026-10-31T14:49:00Z cuc_bo`. Auditor xác định test:6128–6129 và hook:42–47. Đã lưu nội dung/băm/nguyên nhân vào `suite-side-effect.json`, chỉ xóa đúng file do lượt này sinh và thư mục rỗng của nó. Không chỉnh code để sửa test trong checkout review. Vì có lần ghi rồi dọn, **không khẳng định tuân thủ read-only tuyệt đối trong toàn lịch sử chạy**; trạng thái cuối sạch và source/branch không đổi. Đây là side effect suite cũ ngoài diff, không tính thành finding packet.

`/tmp/.git` còn nguyên. Những phần chưa đo thật: native Windows,CI exact HEAD,sh-vắng thật do chroot EPERM,các errno filesystem hiếm và handoff chưa được đưa. Các mục này giữ nhãn không đo được; không gọi chúng hồi quy, không coi mock hoặc rc 0 là nghiệm thu thay thế. Không có quyền approve/merge/land được suy ra từ báo cáo này.
