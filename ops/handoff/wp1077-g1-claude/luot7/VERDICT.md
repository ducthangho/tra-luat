verdict: changes_requested
reviewed_sha: c4af7260a2b6d95b6a0623eeca566a2225912fde
spec_sha256: eabbb725650addad531429d48801667f2ef05a6090c00123d1d4146c7b89c3f3
Ket qua: 0 P0, 1 P1, 0 P2, 0 P3.

PR #1080, packet #1077 DOCTOR-ENOEXEC-BI-CHE r1/g1, sensitive, lease theo assignment `wp1077-r1-g4-claude`, Codex lượt 7/10. **F4-phan-giai-PATH chưa đóng:** commit hiện tại sửa thật các lỗi errno và chuỗi ứng viên được báo lượt 6, nhưng sinh hồi quy với PATH chứa byte ngoài UTF-8 và vẫn đổi `$0` của tệp shebang hợp lệ qua phần tử PATH rỗng. Một lớp P1, hai biểu hiện; không đếm lại các đường chủ kho đã chuyển #1083.

Kết luận cuối: **changes_requested, 1 P1 thuộc lớp F4**. Full suite offline có cùng delta 0 so base; mutation cô lập RUST_LOG đạt 516/516. CI exact-head vẫn chưa đo được.

## NEO, PHAM VI VA DANH TINH

- Base Git OID: `086f1b7343fc1d778e50797e6c9ca0964b11a755`.
- HEAD/tree: `c4af7260a2b6d95b6a0623eeca566a2225912fde` / `2e92bdff4ace9b99d93ed73368de41e12f8ead0b`.
- `sha256sum ../SPEC.md` tự đo đúng hash ở dòng 3. `git diff BASE HEAD` khớp nguyên byte `../diff.patch`; numstat khớp `../numstat.txt`.
- Hai tệp đổi: launcher **+54/-9**, launcher_test **+274/-11**, tổng **+328/-20**. Đếm dòng thêm, không dùng net +308; trong trần 330 đã được chủ kho nâng.
- Vai Reviewer, khác context Executor Claude. `runs/763c03a5/run.json` khai `openai_codex / codex_cli / machine`, run ID `763c03a558ad4143a3d326b50fbcc0d8`. Metadata chưa có evidence `model_phuc_vu`/`effort_phuc_vu` cho lượt đang chạy; không suy model, effort hoặc assurance từ actor GitHub. Reviewer chính tự đo và kết luận. Agent `tl_auditor` chỉ đọc ba log dài theo CLAUDE.md bước 5, không viết source hoặc verdict.
- Linux x86_64, Python **3.13.16**, glibc **2.39**, Bash **5.2.21**, `/bin/sh` là dash. Ma trận glibc dùng chương trình C gọi **execvp thật**, không mô phỏng libc bằng Python.
- Không fetch/push/đăng review, không gọi công cụ mạng hoặc sử dụng credential thật. Các fixture CLI bổ sung chạy trong HOME/env riêng; `kiem_song=True` chỉ gọi llm giả in `ok`. HTTP và git network trong phép đo caller được thay bằng stub. Hai lượt full suite đầu chạy nguyên lệnh yêu cầu; fixture pip không dựng được venv và bỏ qua. Lượt đối chứng offline đặt thêm `PIP_NO_INDEX=1 UV_OFFLINE=1`, không biến skip pip thành pass.
- Source tracked được đối xử read-only. Có quan sát tác dụng phụ của bộ test/hook ở ignored `.claude/.packet_state/session-start.ran` và Git metadata `.git/.tl_reqs_97733a880d95f8a9_894d731f`; xem mục toàn vẹn cuối. Không sửa launcher/test thật hoặc áp HINT vào `cay-kho/`.

## LENH TAI LAP VA HIEN VAT

Các lệnh dưới chạy từ `cay-kho/`, output và mọi bản sao/đột biến nằm ngoài kho được review:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/launcher_test.py
PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/launcher_test.py --dot-bien
PIP_NO_INDEX=1 UV_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/launcher_test.py
RUST_LOG=warn PIP_NO_INDEX=1 UV_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/launcher_test.py --dot-bien
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/packet_checks.py
cc -Wall -Wextra ../evidence/execvp.c -o ../evidence/execvp-glibc
cc -Wall -Wextra ../evidence/argv0.c -o ../evidence/argv0-native
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/semantics.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/contracts.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/merged_guards.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/new_guards.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/shebang_guard.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/callers.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/environment_checks.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/audit.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/build_hint.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/final_snapshot.py
```

Base được xuất bằng `git archive` đúng OID vào `../evidence/base-copy/`; chạy cùng lệnh suite tại đó. Không checkout, đổi branch, config hay Git index của executor.

Ký hiệu dùng trong các bảng: **P** = `packet_checks.py`; **S** = `semantics.py`; **C** = `contracts.py`; **G** = `merged_guards.py`; **U** = `new_guards.py`; **Z** = `shebang_guard.py`; **K** = `callers.py`; **E** = `environment_checks.py`; **I** = `audit.py`. Mỗi ký hiệu là đúng lệnh ở trên, có `.log`/`.json` tương ứng trong evidence; riêng P dùng tên `packet-checks`, G `merged-guards`, U `new-guards`, Z `shebang-guard`, E `environment-checks`. Không dùng output kỳ vọng thay output thật.

## DOI CHIEU LUOT TRUOC VA TUNG FINDING CU

| Finding | Tự đo lại tại HEAD | Disposition |
|---|---|---|
| F1: thiếu probe CLI / lời khai “mọi probe” | I lập mọi call site bằng AST toàn launcher; K chạy version, auth, codex status, llm version/keys/prompt, gh auth/api, MCP và agy bằng CLI giả không shebang; P test cấu trúc 7 hàm; helper :2931–2932, test :9382+, comment DOT_BIEN đều ghi ngoại lệ | **ĐÃ VÁ THẬT phần được giao và lời khai.** `_git` / `_do_codex_song` giữ disposition ngoài packet theo #1083, không nhận là runtime đã vá |
| F2: đồng nhất Bash và `/bin/sh` | S: bashism Bash 0/BASH_ONLY, glibc/helper 127; ELF sai kiến trúc Bash 126, glibc/helper 2; helper :2926 và comment test khai khác biệt | **ĐÃ VÁ THẬT lời khai.** M1 chủ ý chọn `/bin/sh`; các khác biệt đặc trưng Bash không tự mở lại F2 |
| F3: không khóa argv/env | P ca retry argv/env xanh; mutant mất argv chết TinHieuChotCa; C 11 neutral và 20 mutant kiểm kwargs/rc/timeout/guard | **ĐÃ VÁ THẬT**, có răng đúng assertion |
| F4: bỏ wrapper đầu, PATH rỗng, abspath/symlink, cwd dài, interpreter thiếu | S/P/G: absolute, empty, `link/..`, cwd >4200, interpreter ENOENT đều đúng; 9 đột biến riêng làm từng tính chất của ca gộp đỏ | Các biểu hiện này **ĐÃ VÁ THẬT**; không chỉ dựa vào pass đầu tiên của ca gộp |
| F4 lượt 6: ETXTBSY/ELOOP/ENAMETOOLONG, errno cuối, `$0` no-shebang rỗng và `/` cuối | S: ETXTBSY=26, ELOOP=40, component256=36 đều dừng như glibc; EACCES rồi ELOOP trả40; ENOENT/ENOTDIR trả lỗi cuối; no-shebang `$0=cli`, `bin/llm`, `bin//llm` được giữ. G chọc riêng ETXTBSY, empty, bin, bin/ đều đỏ đúng assertion | **ĐÃ VÁ THẬT các biểu hiện lượt 6; cả lớp VÁ SINH LỖI MỚI / CHƯA ĐÓNG**, U/Z dưới đây |
| F5: commit dcfb011 khai +228 sai | I: BASE..dcfb011 launcher +48/-9, test +188/-10 = **+236/-19**; BASE..e6bf386 +56/-9 và +211/-15 = **+267/-24**, đúng đính chính tại e6 | **ĐÃ ĐÍNH CHÍNH** theo cơ chế chủ kho chấp nhận. Handoff tương lai không có trong bundle: **KHÔNG ĐO ĐƯỢC** đã ghi ở handoff; không gán số tại e6 cho HEAD |
| F6: t103 không so tên lệnh | I: AST t103/t111/t113 tại HEAD bằng BASE; t103 có so `cmd[:2] == ["gh", "api"]`, hai nhánh cùng Rc(0). Message1027f85 đính chính đúng; t115 chỉ bỏ qua thêm khóa executable | **ĐÃ ĐÍNH CHÍNH / ĐÃ VÁ THẬT** phần đồ giả, không thấy hồi quy ở các caller K |

Lớp còn mở giữ stable slug **F4-phan-giai-PATH**, nối lịch sử tên F4 qua các lượt 2–6. Không tách hai biểu hiện ở lượt này thành hai finding để làm sai số hội tụ. U lượt 6 = {F4}; cả lớp chưa được xác minh đóng ⇒ **0/1 = 0%**. Owner đã cấp lượt 7/10 và thu hẹp/nâng trần như prompt; đây không phải quyền tự cấp lượt tiếp hoặc xóa lịch sử checkpoint.

## BANG NGHIEM THU

| Tiêu chí | Lệnh | Output thật | Đạt? |
|---|---|---|---|
| M1: helper, ENOEXEC/POSIX/sh-file, đúng một retry và cùng tham số | C, S, U, Z | C 11/11 neutral; 20/20 mutant chết TinHieuChotCa; kwargs/argv/rc giữ nguyên, lỗi ngoài ENOEXEC của đường có `/` giữ nguyên object; retry lỗi dừng ở spawn 2. U/Z có hồi quy tên trần không cần ENOEXEC | **Cơ chế retry đạt; toàn helper KHÔNG ĐẠT**, F4 |
| M2: version và auth đều qua helper, đủ caller trong phạm vi thu hẹp | I, P, K | `_phien_ban`:2987, `_xac_thuc_kem_dau_ra`:3039 đều nối helper; 7 hàm CLI có đủ, không spawn trần; K 8 trạng thái ×2 mode | **ĐẠT phạm vi đã được giao** |
| M3(a): rg/git không shebang tốt trước bản tốt có shebang | P | rg/git doctor 0, co=True, version có `khong-shebang`, không bi_che | **ĐẠT** |
| M3(b): wrapper đầu exit1 vẫn BI_CHE | P, C | doctor 12/BI_CHE; mutant bỏ rc chết đúng ca(b) | **ĐẠT** |
| M3(c): thiếu bit x không retry | P, C, S | 0644 → EACCES; version=False/qua_han=False; đường trực tiếp chỉ1 spawn; mọi-OSError mutant chết ca(c) | **ĐẠT** |
| M3(d): auth no-shebang in một dòng, rc0 | P | HEAD True/Logged in; BASE False/OSError; mutant auth spawn trần chết đúng ca(d) | **ĐẠT** |
| M4: bốn mutant bắt buộc giết đúng ca | P/full mutation | Bỏ retry2/2; mọi OSError1/1; auth bỏ helper1/1; bỏ rc1/1. Cả5 cặp TinHieuChotCa, không nhận OSError/SyntaxError làm kill | **ĐẠT** |
| A1: full suite Linux, ngoại lệ môi trường delta0; mutant mới | Log HEAD/BASE, P | HEAD 302/315 (tổng 325, skip 10, lỗi 13); BASE 291/304 (tổng 314, skip 10, lỗi 13), cùng ID lỗi/skip; +11 pass. 14 mutant wp1077,20/20 target đúng assertion | **ĐẠT phần local theo ngoại lệ SPEC**; không khai cả suite xanh tuyệt đối |
| A2: base(a),(d) đỏ | P | Hai ca chạy HEAD test với BASE launcher: 2/2 TinHieuChotCa; rg12/BI_CHE, authFalse/OSError | **ĐẠT**, đúng bệnh |
| A3: tái hiện Issue tại chỗ | P ca(a) chạy lenh_doctor thật | rg/git wrapper đầu không shebang ⇒ 0/co=True/FIRST/không bi_che | **ĐẠT fixture tập trung**; không khai doctor toàn máy xanh |
| A4: Ruff F delta0 | I | Ruff0.17.1, `--no-cache --select F` trên launcher/test/tl.py: HEAD17, BASE17 (0+5 F841+12 F821), rc1 cả hai, delta0 | **ĐẠT delta**, không khai lint tuyệt đối xanh |
| A4: diff và doctrine | I: `git diff --check BASE HEAD`; `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | Diff rc0; doctrine rc0, sạch,10 tệp/0 chỗ chép doctrine | **ĐẠT local** |
| A4: CI exact-head cuối | Không gọi mạng, bundle không có CI receipt/log đã xác minh trên c4af726 | **KHÔNG ĐO ĐƯỢC** | A4 tổng thể **CHƯA ĐỦ BẰNG CHỨNG**, không gán CI xanh hoặc lỗi runtime |

Ruff **pin/probe contract** đo riêng với `runpy.run_path(".claude/dev/ci_dang_ky_test.py")["loi_ruff_ci"]()`: **3, []**, rc0. Đây là kiểm cấu trúc workflow; không thay bare lint và không chứng nhận CI đã cài/chạy đúng pin ở một run thật.

## BANG DO

**Cách tìm:** I đọc nguyên byte toàn diff BASE..HEAD, đánh dấu mọi dòng thêm bằng hunk Git, tokenize **mọi COMMENT giao dòng thêm**, AST **mọi docstring/hàm giao dòng thêm**, rồi đọc toàn thân hai helper mới, từng caller đổi, toàn test thêm và từng tuple DOT_BIEN liên quan. Đọc nguyên `git log -1 --format=%B HEAD` và message e6bf386/57e2d4a/1027f85 để kiểm đính chính. `claims-inventory.json` lưu source/comment/docstring cùng tọa độ, `head-commit.txt` lưu message. Song song quét call graph toàn launcher, không dùng danh sách 7 hàm trong test làm trần tìm kiếm. Đây là cách nhóm khẳng định theo nghĩa, không chỉ grep vài từ “mọi probe”.

| Khẳng định | Diff khai | Đo được (lệnh) | Khớp? |
|---|---|---|---|
| No-shebang ⇒ ENOEXEC; subprocess trực tiếp khác shell | Helper2924–2926 | S: path có `/` raw subprocess OSError8; bare raw subprocess chạy LATER, glibc/Bash/helper FIRST | **Có** |
| Hợp đồng `/bin/sh` của glibc, Bash có thể khác | 2926; comment test | S: bashism Bash0, glibc/helper127; ELF Bash126, glibc/helper2 | **Có**, không đồng nhất hai oracle |
| Chuỗi `<entry>/<name>`, giữ trailing slash, tương đối/..,symlink | 2927–2928,2943; messageHEAD | S: no-shebang `first/` ⇒ glibc/helper `first//cli`, Bash `first/cli`; `link/..` đúng inode/marker FIRST; G riêng từng property | **Có cho các dạng đã đo; PATH byte còn F4** |
| Empty entry logical `<name>`, syscall qua `./<name>` | 2928–2929,2948 | S: fallback `$0=cli`, native argv0=cli; Z: shebang `$0=./llm`, mất CO_CREDENTIAL | **Mô tả chính xác nhưng GIỚI HẠN CÓ HẬU QUẢ**, F4; công bố không đồng nghĩa waiver |
| PATH lấy từ env của probe; None kế thừa, thiếu PATH dùng defpath | 2941 | S: env={} và env=None thiếu PATH đều chạy true từ default; env None/explicit có PATH chọn FIRST | **Có ở env string bình thường**; .encode strict làm hỏng môi trường POSIX hợp lệ U |
| Bỏ entry vượt ngưỡng PATH, không đồng nhất với component256 | 2928,2942–2943; messageHEAD | S: entry4200 rồi good ⇒ LATER; component256 rồi good ⇒ glibc/helper errno36, Bash LATER | **Có dạng đã đo**. Tất cả entry đều dài: glibc driver giữ errno0, helper tổng hợp ENOENT; cả hai không chạy CLI, chưa thấy sai nhãn nên không thêm finding |
| Chỉ tập6 errno đi tiếp; ETXTBSY/ELOOP dừng | 2929–2930,2944,2952 | S: EACCES/ENOENT/ENOTDIR đo vật lý, ETXTBSY26/ELOOP40 dừng. ESTALE/ENODEV/ETIMEDOUT chỉ xác minh tập trong source, không có filesystem tái hiện vật lý | **Đạt phần đo được; 3 errno hiếm KHÔNG ĐO ĐƯỢC vật lý**, không khai đầy đủ |
| Ưu tiên EACCES nếu hết search, còn lại lỗi cuối | 2930,2954–2955 | S: EACCES+ENOENT ⇒13; ENOENT+ENOTDIR ⇒20; đảo ⇒2; EACCES+ELOOP ⇒40 ngay | **Có dạng thật đã đo** |
| Retry đúng tệp, một lần, kwargs/argv/rc giữ | 2950–2951; M1 | C: spawn 2, retry error object nguyên,7 kwargs/argv riêng mutant; S native argv0 và đối số `a b`; P argv/env | **Có nhánh ENOEXEC** |
| Không retry Windows / sh không phải file | 2935,2950 | C mock nt/no-sh mỗi ca1 spawn; hai mutant guard chết assertion; E chroot PermissionError1 | **Đo mock đạt**; Windows và `/bin/sh` vắng thật KHÔNG ĐO ĐƯỢC |
| llm wrapper utf8/replace, stdinDEVNULL, capture, timeout30 | 2957–2963 | Đối source `_chay_van_ban_an_toan`, C giữ kwargs, K trace version/keys/prompt cùng marker | **Có thuộc tính được nêu**; không suy helper hỗ trợ mọi tham số cwd của wrapper cũ |
| Các caller CLI dùng helper nhưng classifier vẫn cũ | 9 call site cũ đổi callee + helper llm mới | I diff chỉ đổi callee; K status/llm live giả/gh api/MCP/agy đều đúng8/8×2; C empty/rc1/timeout không thành có | **Có fixture thường**; U/Z là hồi quy phân giải trước classifier |
| Test M3(a–d), argv/env, Codexstatus, llm tên trần có răng | Test9237+; DOT_BIEN12381+ | P11/11 neutral; 14 mutant20/20 target đúng TinHieuChotCa | **Có** |
| Test cấu trúc không phải mọi probe, trừ2 đường #1083 | Test9382+; comment DOT_BIEN | I kiểm graph toàn module; helper/test/comment đều nói đúng ngoại lệ | **Có**, F1 lời khai đóng |
| Ca gộp vẫn đo từng tính chất | MessageHEAD; PATH tests9402+ | G9/9 mutant riêng: absolute,empty,symlink,interpreter,empty$0,bin$0,bin/$0,ETXTBSY,cwd dài | **Có**, từng assertion/variant được ghi trong merged-guards.json |
| Ca hợp đồng mới đỏ trên01b9734 | MessageHEAD | P: r1077_PATH_hop_dong_glibc đỏ TinHieuChotCa ngay `$0` PATH rỗng; hai ca PATH/cwd khác xanh như kỳ vọng | **Có**; không lấy lần đỏ sớm làm bằng chứng các nhánh sau, đã đo G độc lập |
| Gỡ đồ giả lượt2, argv0 là tên trần | Message01b và diff cuối | I: AST t103/t111/t113=BASE; t115 chỉ lọc thêm executable; S native argv0=cli | **Có** |
| Lượt6 changes_requested1P1, F4 | MessageHEAD | Đọc VERDICT-luot6 dòng1–4 và finding F4 | **Khớp artifact được giao**, không suy attestation model |
| +54/-9,+274/-11,tổng+328/-20,trần330 | MessageHEAD | I git diff --numstat exact BASE..HEAD | **Có**, không nhầm số head trước |
| e6 đính chính dcfb và số tại chính e6 | Messagee6, chỉ thịF5 | I Git objectnumstat:236/-19 và267/-24 | **Có**; handoff chưa có nên chưa đo việc ghi ở đó |

Ma trận S còn đo tên có khoảng trắng/Unicode/dấu gạch đầu (đều chạy0), tên dài256 (glibc/helper errno36), đường chỉ thư mục (EACCES) và đường có slash không tồn tại (ENOENT). Tên lệnh rỗng cho helper ValueError trong khi glibc ENOENT; không caller doctor nào nhận tên rỗng từ bảng công cụ, nên không có hậu quả nhãn trong phạm vi và không tính finding. Không suy mọi giá trị tùy ý của API Python đều đồng nhất libc.

## KIEM KE HET DUONG PROBE VA SPAWN

`evidence/call-sites.json` lưu mỗi call site cùng caller/line/source từ AST **toàn launcher**. Tôi lần từ cả `CONG_CU`, `KHA_NANG`, các hàm chẩn đoán khác và preflight tới wrapper/delegate, rồi phân loại mọi spawn trực tiếp; không chỉ tìm chuỗi `subprocess.run` trong doctor.

| Đường / nguồn | Spawn cuối / ý nghĩa | Phạm vi và kết quả |
|---|---|---|
| CONG_CU mọi `--version` | `_phien_ban`2987 → helper2948/2951 | Trong phạm vi; P/K/S đo |
| CONG_CU `xac_thuc` + cached evidence agy | `_xac_thuc_kem_dau_ra`3039 → helper; `_xac_thuc` chỉ bọc; `_do_antigravity` dùng lại `_XAC_THUC_DA_DO` hoặc auth/version helper | Trong phạm vi; K auth/agy không shebang xanh |
| Codex status | `_do_codex`3934 → helper | Trong phạm vi; P/K CO_CREDENTIAL |
| Codex live | `_do_codex_song`3878 → runpy codex_cred `_kiem_song` → spawn bên ngoài write set | **Ngoài packet theo quyết định chủ kho, #1083**. Không gọi live/credential thật; không tính finding này |
| Snapshot preflight doctor/run/chuan-bi | `_chuan_bi_va_bo_snapshot` → `chuan_bi_xac_thuc` → `_probe_snapshot`3626 → cùng delegate codex_cred | Credential materializer/preflight, không phải probe nhãn CONG_CU/KHA_NANG được giao; delegate ngoài write set. Ghi nhận cùng giới hạn; không tuyên bố mọi spawn doctor đã phủ |
| llm version / keys list / prompt --no-log | `_do_openai_llm`4040/4048/4062 → `_chay_probe_llm` → helper | Trong phạm vi; K3CLI giả; U/Z lỗi F4 |
| gh auth status / gh api repos/... | `_do_github`4571/4632 → helper | Trong phạm vi; K gh-cliOK,gh-khoOK,DUNG_DUOC bằng gh-kho; HTTP/git network stub |
| Claude MCP get | `_suc_khoe_mcp_github`4373 → helper | Trong phạm vi; K `khoe`, nguyên args/server và chuẩn env |
| Git ls-remote, remote get-url, show hook/launcher master, tìm workspace | `_git`286; cả `_do_github`, `_do_hook_cu`, `_do_launcher_cu` và đường run dùng chung | **Ngoài packet theo chủ kho, #1083**, không đếm F1 runtime; source vẫn subprocess.run thô |
| Claude capability, hook-da-chay, locale, module Python, paths | Đọc file/env/hash/`find_spec`/import, không spawn công cụ mới | Không có call subprocess bị bỏ sót trong lớp ENOEXEC |
| REST GitHub / MCP endpoint | urllib HTTP, không exec file | Ngoài cơ chế ENOEXEC; không gọi mạng trong phép đo này |
| `_probe_spawn` | `_chay_van_ban_an_toan`319, caller đường run tự chọn command | Ngoài phạm vi SPEC |
| `_chay_json_chat_che` | subprocess333, không có caller trong doctor graph | Không là đường probe doctor; không phát hiện lỗ hổng nối helper bị bỏ sót ở đây |
| ps lstart/stat/process-tree; taskkill; Popen lenh_run | subprocess371/455/508/706/883; Popen2299 | Giám sát/kill-tree hoặc chạy lệnh người dùng; ngoài packet, không quyết định nhãn khả dụng công cụ doctor |

Không thấy thêm `subprocess.run` trần nào trong probe CLI mà owner giữ lại. F4 nằm ở logic phân giải mới, không phải một call site trong phạm vi chưa được nối.

## BANG TEST

| Bộ / lệnh đã chạy | N/M thật | Bỏ qua / giới hạn |
|---|---|---|
| `python3 .claude/dev/launcher_test.py`, HEAD | **302/315**, rc1; tổng 325,lỗi 13 | 10 skip riêng dưới đây |
| Cùng lệnh tại base-copy | **291/304**, rc1; tổng 314,lỗi 13 | Cùng10 skip/cùng13 ID lỗi; delta0 |
| `python3 .claude/dev/launcher_test.py --dot-bien` | **515/516**, rc1;597/598 cặp target | 4 không đo; mutant cũ RUST_LOG sống sót, E đối chiếu HEAD/base |
| Mutation với `RUST_LOG=warn`, offline | **516/516**, rc0; **598/598** cặp target | 4 không đo; log `head-mutants-rust-warn.log` |
| Full suite HEAD/BASE có PIP_NO_INDEX/UV_OFFLINE | **302/315 / 291/304**, rc1/1 | Cùng 13 failure, 10 skip; trùng lượt đầu; `head-suite-offline.log`, `base-suite-offline.log` |
| P: neutral mới | **11/11** | 0 skip |
| P:14 mutant wp1077 | **20/20** target chết TinHieuChotCa | Cả5 cặp M4 đúng ca; không tín dụng exception vô can |
| P:BASE(a),(d) | **2/2 đỏ TinHieuChotCa** | Phản chứng có chủ ý, không phải suitefail mới |
| C:kwargs,guards,classifier,timeout | **11/11 neutral;20/20 mutant assertion** | Mocknt/no-sh không thay nền thật |
| G:chốt từng tính chất trong ca gộp | **9/9 mutant riêng đúng assertion** | Message/nguồn assertion của từng variant được giữ |
| S:glibc C/Bash/raw subprocess/helper | **54 dạng ×4 engine** | Bảng đo, không phải “54/54 pass”; có lệch được phân loại |
| K:8 caller status ×2shebang modes | **16/16** | CLI giả; git/HTTP được stub, không chứng minh dịch vụ thật |
| U:PATHbyte | HEAD đỏ,BASE xanh,đối chứngxanh;**2/2 mutant TinHieuChotCa** | Đo cả CLI trong tên byte và entry byte không chứa CLI |
| Z:shebang `$0` | HEAD đỏ,BASE xanh,đối chứng biệt lậpxanh,đảo lạiđỏ TinHieuChotCa | Đối chứng chỉ chứng minh fixture, không là thiết kế production đã được duyệt |
| HINT | dry-run/áp `--fuzz=0 -p0` trên bản sao đều rc0 | Hai test HINT đỏ HEAD/xanh BASE đúng assertion; không áp kho thật |

10 skip giống hệt giữa HEAD/BASE:

- `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125`: fixture Windows, POSIX là t63.
- `r345_chan_socket_that_ma_than_hook_van_chay_dung`, `r345_cac_phep_do_cuc_bo_van_dung`, `r345_lop_tham_import_van_co_rang`, `r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO`, `r347_tham_import_van_song_tren_python_truoc_310`, `r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO`, `r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia`, `r348_dot_bien_bo_isidentifier_lam_ca_dich_DO`: **KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)**.
- `r484_g4_windows_sid_alias_identity`: BO QUA native Windows SID conversion.

Bốn mutant không đo được: `g4_windows_sid_alias_not_normalized`, `g4_windows_LA_not_current_owner` (native SID conversion), `g2_windows_directory_pin_access` (native Windows share-delete pin), `124_khi_chau_con_song` (targett62bỏqua). Không cộng chúng vào tử số pass.

13 failure chung, không gọi là hồi quy của diff:

```text
r858_goc_tam_tranh_to_tien_co_git
t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac
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
```

Hai failure đầu là `/var/tmp` EROFS/errno30. Nhóm11r484 bị chặn trước phép đo credential/child;6reason nói trực tiếp “Codex home is inside a repository”. `ls -ld /tmp/.git` xác nhận thư mục tồn tại, phù hợp bẫy đã biết. Tôi không xóa/bypass guard hoặc sửa `/tmp/.git`; đối chiếu base cùng điều kiện cho cùng13 failure, nên phần hành vi bên dưới guard **KHÔNG ĐO ĐƯỢC**, không biến thành pass. `suite-comparison.json` giữ từng tên/reason; không có t53 trong failure.

Mutant cũ `r26_rv5_codex_env_guard` sống sót ở lượt nguyên môi trường vì launcher phiên review thừa kế đúng `RUST_LOG=tungstenite::protocol=trace`: xóa khối gán vẫn cho output ca đích mong. E đo8tổhợp: neutralHEAD/BASE đều xanh ở inherited/warn; mutantHEAD/BASE đều xanh inherited, đều đỏ đúng `TinHieuChotCa("con khong duoc bat dung target trace")` ở warn. Đây là điều kiện rig cũ có delta0, không là mutant mới wp1077 sống sót và không phải finding của packet.

## BANG SAN

Mỗi dòng có hướng độc lập, lệnh chạy được và output thật. Không dùng sự có mặt của ca test làm bằng chứng đã đo.

| Hướng | Lệnh | Output thật | Phân loại |
|---|---|---|---|
| 1.Tên/PATH: rỗng,tương đối,`..`,symlink,slash,absent,envNone,tên space/Unicode | S | 54 dạng, FIRST được giữ với no-shebang; native argv0=cli/argc2/arg1=`a b`; thiếu PATH chạy true0; cwd>4200 hai modeFIRST | KHÔNG PHẢI LỖI ở các dạng thường; hai biến thể F4 tách dưới |
| 2.Errno vật lý/thứ tự tìm | S | ETXTBSY26/ELOOP40/component25636 dừng; EACCES+ENOENT13; ENOENT/ENOTDIR20,đảo2; entry4200quaLATER | KHÔNG PHẢI LỖI các biểu hiện lượt6; ESTALE/ENODEV/ETIMEDOUT vật lý KHÔNG ĐO ĐƯỢC |
| 3.Quyền thư mục và file | S | Dir0111FIRST;0444/0000LATER; file0644đầuPATHLATER, đường cóslashEACCESkhôngretry | KHÔNG PHẢI LỖI; quyền DAC thật, không chỉ mock |
| 4.Filesystemencoding ngoàiUTF8 | S,U | Bash/glibc/raw0/NON_UTF8_OK; helperUnicodeEncodeError; doctor13/KHONG_DO_DUOC trong khi versioncoTrue; BASE xanh | **LỖI F4 P1**, hồi quy |
| 5.Shebang hợp lệ + `$0` qua emptyPATH | S,Z | Glibc0/SHEBANG_OK; Bash42/helper42; BASE CO_CREDENTIAL,HEAD CHUA_XAC_THUC; đảo mutantđỏassertion | **LỖI F4 P1**, hồi quy đã được công bố nhưng chưa được miễn |
| 6.Hợp đồng kwargs,timeout,retry | C,P | C11/11,20/20 mutant; kwargsnguyên/2 spawn; sleep1 vượt.1 trảqua_hanTrue cảversion/auth | KHÔNG PHẢI LỖI |
| 7.Binary sai kiến trúc,tệp0byte,BOM,bashism | S,C | WrongarchBash126/glibc-helper2; emptyrc0nhưng khôngoutput⇒probeFalse; BOM127; bashismBash0/glibc-helper127 | KHÔNG PHẢI LỖI trong hợp đồng `/bin/sh` M1, không nâng empty0 thànhcó |
| 8.Caller capability/auth toàn diện | I,K,P | CodexCO_CREDENTIAL,llmofflineCO_CREDENTIAL,llmfixtureDUNG_DUOC,MCPkhoe,ghDUNG_DUOC,agyDUNG_DUOC; trace có đủargs | KHÔNG PHẢI LỖI caller thường; `_git`/delegate ngoài packet |
| 9.Ca gộp có giết đúng nhánh riêng | G | 9/9 riêngproperty đỏTinHieuChotCa; log nêu đúngPATH/ETXTBSY/cwddài tương ứng | KHÔNG PHẢI LỖI thiếu răng trong9propertyđãđo |
| 10.Windows và `/bin/sh` vắng | C,E | Mock1 spawn/2mutantchết; thửchrootPermissionError1; nềnLinux | **KHÔNG ĐO ĐƯỢC nền thật**, khôngcoimockthaynative |
| 11.Lời khai định lượng/toàn diff | I | Gitdiffbytekhớp;+328/-20;Ruff17→17;doctrine10/0;contract3/[];ASTstub=BASE | KHÔNG PHẢI LỖI mới; giới hạn handoff/CI ghi riêng |
| 12.Môi trường và mutation cũ | E, logsfullHEAD/BASE | FailureIDs13giống,skip 10giống; mutantRUST_LOGnhưnhauởHEAD/base và chết khiwarn | KHÔNG PHẢI HỒI QUY của diff;13casebêndướiguardchưađo |

### F4-phan-giai-PATH [P1] PATH hợp lệ mất khả dụng do mã hóa và đổi `$0` của shebang

**TEP/DONG:** `.claude/dev/launcher.py:2942` và `:2943` (`str.encode()` mặc định strict UTF-8); `:2948` (ép `./` cho empty PATH); caller có hậu quả `_do_openai_llm:4040` và `lenh_doctor:5192` (exception → KHONG_DO_DUOC). Giới hạn shebang đã được mô tả ở `:2931`, không có authority bỏ nó khỏi packet như hai ngoại lệ #1083.

**VAN DE:**

1. Trên POSIX, PATH/tên thư mục có thể chứa byte không hợp lệ theo UTF-8. Python biểu diễn byte ấy bằng surrogateescape trong `os.environ`; `execvp`, Bash và subprocess dùng filesystem encoding và vẫn chạy được. Mã mới dùng `duong.encode()` rồi `d.encode()` trước spawn nên ném UnicodeEncodeError cho toàn bộ probe tên trần. Không cần CLI nằm trong thư mục byte: một entry không chứa công cụ ở trước CLI ASCII cũng đủ gây lỗi. `doctor` có thể nhận versionco=True từ đường đã resolve nhưng lại báo capabilityKHONG_DO_DUOC vì cùng công cụ ở probe tên trần. BASE không mắc lỗi này; đây là hồi quy của commit c4af726, không phải wrapper hỏng hoặc bất thường môi trường không thể thực thi.
2. Khi candidate logical là `llm` từ entry rỗng, `executable="./llm"` thay `$0` của một script **có shebang hợp lệ**. Fixture chỉ dùng POSIX: `#!/bin/sh` và `[ "$0" = llm ] || exit 42`, rồi in version/key như CLI giả. Glibc execvp và BASE truyền `llm` và chạy thành công; HEAD truyền `./llm`, mất version/key và chuyển CO_CREDENTIAL thành CHUA_XAC_THUC. Bash cũng truyền `./llm` ở ca này; vì vậy không khai Bash thành oracle đồng nhất với glibc. Đây là hồi quy của đường thường không cần ENOEXEC so với BASE và là giới hạn có hậu quả thật của hợp đồng glibc được giao. Docstring mô tả đúng giới hạn chỉ sửa lời khai, không tự cho phép chấp nhận thay đổi hành vi ấy.

**DA THU NGHIEM:**

```sh
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/semantics.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/new_guards.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/shebang_guard.py
PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/build_hint.py
```

- S `non-UTF8-PATH`: glibc/Bash/raw subprocess **rc0, NON_UTF8_OK**; helper **UnicodeEncodeError**.
- U chạy `lenh_doctor` thật, chỉ giữ llm CONG_CU và openai-llm KHA_NANG, env/HOMEriêng, credentialinert và CLI giả: **HEAD 13/KHONG_DO_DUOC/UnicodeEncodeError**, trong khi mục công cụ `co=True`, phiênbảnllm-BYTES. **BASE 0/DUNG_DUOC**; đối chứng riêng dùng filesystemencoding **0/DUNG_DUOC**, cả2variant chạy qua. Không gọi OpenAI/GitHub hoặc dùng key thật.
- U mutant riêng đảo cách đếm toàn PATH và từng entry: **2/2 TinHieuChotCa của chính ca doctor**, không tín dụng UnicodeEncodeError thoát thô. Loại exception do doctor chuyển thành dữ liệu; chốt đỏ vì nhãn/rc sai.
- Z cùng fixture shebang: **HEAD CHUA_XAC_THUC**, **BASE CO_CREDENTIAL**, đối chứng biệt lập cho shebangxanh, đảo ép./đỏ đúng `TinHieuChotCa("shebang hop le bi doi $0...")`. Đối chứng đọc đầu tệp chỉ là phép chẩn đoán trong scratch; chưa được xác minh như thiết kế sửa tổng thể và **không phải runtime hint đề nghị áp**.
- Hai test thật trong HINT được import và chạy lại từ bản sao đã áp patch: **HEAD 2/2 đỏTinHieuChotCa,BASE 2/2 xanh**, giữ đúng bệnh. `hint-validation.json` lưu output thật.

**DO TIN:** cao cho hai hành vi POSIX đã chạy trên Linux/glibc2.39/Bash5.2.21 và API doctor/helper thật. Không suy lỗi tương tự trên native Windows. Một lớp P1 theo rubric vì sai hành vi đo được; không cộng thêm P2 riêng cho thiếu regressiontest hoặc thêm P1 cho chính lời khai cùng cơ chế.

Hướng sửa bằng lời: dùng encoding filesystem/surrogateescape cho mọi phép đo byte của PATH, bảo toàn tên script/argv0 ở cả shebang và fallback, rồi đo toàn ma trận chứ không chỉ fixture mới. Nếu thiết kế subprocess hiện tại không giữ được `$0` shebang mà vẫn dừng chính xác ở ENOEXEC/errno cứng, cần quyết định thiết kế hoặc miễn trừ hành vi có authority/spec revision; reviewer không tự cấp waiver bằng docstring.

## HINT VA GIOI HAN

`../HINT.patch` **chỉ thêm hai test vào launcher_test.py**, áp `patch --fuzz=0 -p0` từ `cay-kho/`. Nhãn theo protocol: **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**. Đã dry-run/áp trên `evidence/hint-final-copy` rc0, không áp trên repo được review. Ruff F của test sau HINT vẫn chỉ 5 F841 nền, không thêm diagnostic.

Theo [adapter cross-review](cay-kho/.agents/skills/cross-review/SKILL.md) và [protocol §8](cay-kho/docs/PROTOCOL_DA_PHIEN.md), với packet sensitive, “patch-as-hint chỉ đủ điều kiện cho (a) tệp TEST thuần”; launcher runtime bị loại trừ. Vì vậy hướng sửa runtime là mô tả, các bản đối chứng scratch chỉ là evidence, không phải patch production đã được duyệt.

HINT thêm **52 dòng**, cộng nguyên vào HEAD sẽ thành BASE..hint **+380**, vượt trần330. Đây là dữ liệu phản chứng/test gợi ý, **không phải bản sửa sẵn đáp ứng mọi gate**. Executor phải tái dẫn xuất, bố trí lại trong write set/trần được cấp hoặc xin quyết định phạm vi từ owner; không âm thầm giảm chốt để vừa số dòng. Handoff khi dùng hint phải khai hint_provenance theo protocol; chưa có handoff mới nên không tự suy đã vi phạm/đã khai.

## GIOI HAN VA TOAN VEN

CI exact-head, native Windows, `/bin/sh` vắng thật, ba errno filesystem hiếm và phần hành vi nằm sau các guard môi trường giữ trạng thái **KHÔNG ĐO ĐƯỢC**. Không sửa `/bin/sh`, đổi quyền host, xóa `/tmp/.git`, dùng credential thật hoặc mạng để mở các phép đo ấy.

`initial-hashes.json` chụp hash mọi tracked regular file đầu lượt và `initial-status.txt` chụp status. Chưa có snapshot ignored/Git-internal đầu lượt, nên không thể chứng nhận lịch sử không ghi rồi hoàn nguyên. Sau suite quan sát ignored `session-start.ran` (28byte) và Git stamp `.tl_reqs_*` (0byte), mtime15:32; `side-effect-observation.json` lưu metadata. Chúng khớp cơ chế hook được test gọi. Tôi không xóa/hoàn nguyên khi không có bytes ban đầu và không coi `git status` tracked sạch là bằng chứng không có tác dụng phụ.

Snapshot cuối (`evidence/final-snapshot.json`): **9.125/9.125 tracked file hash không đổi**, HEAD/tree/spec/diff khớp đầu lượt; worktree diff và index diff rỗng, không có untracked ngoài ignored packet_state đã khai. `git diff --check` rc0. Các phép đo đã kết thúc; cặp suite offline giống lượt đầu (HEAD 302/315, BASE 291/304, cùng 13 lỗi/10 skip), mutation offline RUST_LOG=warn 516/516, rc0,598/598 target,4 không đo.

Không approve exact SHA này vì F4 còn sai hành vi trong phạm vi. Các đường #1083 không được tính vào finding; không xin thêm quyền hoặc tự tiếp tục một lượt review mới.
