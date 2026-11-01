verdict: approve
reviewed_sha: ee3dc6d20d47becd0ab9379c22583bc5587c64b2
spec_sha256: eabbb725650addad531429d48801667f2ef05a6090c00123d1d4146c7b89c3f3
Ket qua: 0 P0, 0 P1, 0 P2, 0 P3.

PR #1080 · packet #1077 DOCTOR-ENOEXEC-BI-CHE r1 · lease `wp1077-r1-g6-claude` · sensitive · Codex lượt **10/10, cuối**.

**Approve về nội dung trong phạm vi chủ kho đã chốt.** Không còn finding phải sửa trong phạm vi này. F4 vẫn có hành vi đổi `$0` đã đo được, nhưng hai dạng ứng viên cwd từ PATH rỗng/quá dài đều thuộc W-1077-1 của lease g6; đây là **miễn trừ, không phải đã vá**. `_git` và probe sống được delegate sang `codex_cred.py` vẫn chưa nhận fallback, thuộc nợ #1083 theo quyết định phạm vi. Không dùng các ngoại lệ này để nhận là đã phủ toàn doctor.

**Chưa đủ bằng chứng nghiệm thu/merge:** CI PR xanh trên exact HEAD không đo được trong bundle offline. A4 tổng thể chưa xác nhận; verdict nội dung này không xác nhận CI xanh, không tạo quyền merge/land. Điều kiện M-2 của lease vẫn phải được người giữ kho/executor xác minh riêng.

## NEO VA CACH DO

Base `086f1b7343fc1d778e50797e6c9ca0964b11a755`; tree HEAD `cbf4031615070801ead1989feb3411f3ef3eb8b9`. `sha256sum ../SPEC.md` tự đo khớp `eabbb725650addad531429d48801667f2ef05a6090c00123d1d4146c7b89c3f3`. Diff dựng lại bằng Git khớp byte `diff.patch`; numstat **launcher +57/-9, test +283/-11 = +340/-20**, hai tệp, trong trần 345 theo lease g6. Không lấy net 320 làm số dòng thêm. HEAD so với 457e413 chỉ đổi docstring: AST bỏ docstring bằng nhau (`history-final.json`), đúng lời commit “không đổi hành vi”.

Reviewer là Codex/OpenAI theo assignment. `runs/5cfca6a9/run.json` khai provider `openai_codex`, surface `codex_cli`, transport `machine`, run ID `5cfca6a99b7b411bbb7b9cc89bed47a6`. Tôi trực tiếp đọc/đo bằng shell tools trong phiên reviewer độc lập; không dùng context executor hoặc gọi agent khác. Không có attestation độc lập về model/effort thực phục vụ; không suy chúng từ footer commit hay actor GitHub.

Tất cả script, log, bản BASE, mutant ở `../evidence/`, ngoài `cay-kho/`. Các lệnh bảng dưới chạy được từ `cay-kho/`. `run_suites.py` chạy chính `python3 -u .claude/dev/launcher_test.py` ở HEAD/BASE và `python3 -u .claude/dev/launcher_test.py --dot-bien` ở HEAD. Môi trường liệt kê trong `clean_env()`: HOME riêng, PATH hệ thống, không credential thừa kế, `PIP_NO_INDEX=1`, bytecode tắt, Git global/system config tắt. Không dùng web/API tools để lấy dữ liệu, không fetch/push/LIVE hoặc dùng credential thật. Các phép đo riêng dùng fixture offline. Bộ test hiện hữu có probe Git/REST/MCP; trong lượt chạy này chúng không cung cấp bằng chứng mạng thành công (JSON t53 ghi URLError khi POST initialize). Vì vậy không dùng những probe nền đó để xác nhận CI hay khả dụng dịch vụ. Các lệnh llm/gh/codex/claude/agy trong phép đo riêng là fixture cục bộ; “llm-live-fixture” chỉ chạy script giả.

Môi trường: Linux x86_64, Python3.13.16, glibc2.39, `/bin/sh` → dash. `matrix.py` gọi **glibc execvp thật bằng ctypes trong child** và **Bash thật `/bin/bash --noprofile --norc`**, không dùng mô hình giả của execvp làm oracle. Phép đo quyền thực tế không cần setuid; hai lần thử setuid trước đó bị sandbox từ chối được ghi riêng, không nhận thành kết quả sản phẩm.

## BANG NGHIEM THU

| Tiêu chí | Lệnh từ cay-kho/ | Output thật | Đạt? |
|---|---|---|---|
| M1: ENOEXEC/POSIX/sh-file, retry một lần, giữ tham số/kết quả/lỗi khác | `python3 -B ../evidence/contracts.py`; `matrix.py` | 8/8 neutral, 8/8 mutant chết TinHieuChotCa;7 contract giữ số spawn/exception/argv/kwargs/rc và 1 contract llm; timeout0.1 s cho cả version/auth trả False/qua_han=True | **Đạt hợp đồng M1**. Windows/sh vắng: guard mock, chưa phải native |
| M2: hai probe dùng helper, rà đủ caller | `python3 -B ../evidence/audit.py`; `callers.py` | `_phien_ban:2990`, `_xac_thuc_kem_dau_ra:3042`; AST toàn launcher +36 call site khớp bộ tìm;16/16 parity caller | **Đạt trong scope đã thu hẹp**, không nhận đã sửa 2 delegate #1083 |
| M3(a): rg/git không shebang tốt đầu PATH | `python3 -B ../evidence/targeted.py` | 2 mục doctor rc0/co=True, version 1.0.0-khong-shebang, không bi_che | **Đạt** |
| M3(b): rg không shebang exit1, bản tốt sau | Cùng targeted.py | Ca `r1077_doctor_khong_shebang_hong_van_BI_CHE` PASS: rc12/BI_CHE | **Đạt**, không nới bản hỏng |
| M3(c): shebang0644 | Cùng targeted.py; contracts.py | ca PASS, chay_duoc=False/qua_han=False; direct EACCES giữ nguyên lỗi,1 spawn | **Đạt** |
| M3(d): auth không shebang có dòng/rc0 | Cùng targeted.py | ca PASS, `(True,ok,False,Logged in)` | **Đạt** |
| M4:4 mutant bắt buộc chết đúng assertion ca đích | Cùng targeted.py | bỏ retry2/2, retry mọi OSError1/1, auth bỏ helper1/1, bỏ rc1/1; **5/5 cặp TinHieuChotCa** | **Đạt** |
| A1: full suite Linux, loại đúng ngoại lệ có đối chứng BASE | `python3 -B ../evidence/run_suites.py` | HEAD **291/315**, tổng325/skip10/lỗi24; BASE **280/304**, tổng314/skip10/lỗi24; cùng24 ID lỗi, cùng 10 ID skip, delta lỗi0 | **Đạt theo ngoại lệ môi trường**, thêm11 ca xanh. Không khai toàn suite xanh; danh sách đầy đủ bên dưới |
| A1: mutation mới có răng đúng lý do | Cùng run_suites.py; targeted.py | Harness: **DOT BIEN: 518/518 dat  (4 khong do duoc tren nen nay)**, rc0; riêng wp1077 **16 mutant/22 cặp,22/22 TinHieuChotCa**;9/9 thuộc tính ca gộp chết riêng đúng assertion | **Đạt cho các mutant mới**; không lấy tổng harness thay bằng chứng đúng ca |
| A2: base(a),(d) đỏ | `python3 -B ../evidence/targeted.py` dùng HEAD test + launcher BASE | **2/2 TinHieuChotCa**; doctor(a) không nhận wrapper, auth(d) không chạy được | **Đạt** |
| A3: tái hiện Issue tại chỗ | Cùng targeted.py | doctor fixture rg/git rc0,co=True,không bi_che; JSON ở targeted.json | **Đạt**, không nhận toàn máy đủ công cụ |
| A4: Ruff F delta0 | `python3 -B ../evidence/audit.py` chạy Ruff thật HEAD/BASE | Ruff0.17.1; cả2rc1,17 diagnostic: `{'F841': 5, 'F821': 12}`; Counter(file,code,message) bằng nhau; launcher0 | **Đạt delta**, không khai lint0 tuyệt đối hoặc pin CI đã kiểm |
| A4: diff check | `git diff --check 086f1b7343fc1d778e50797e6c9ca0964b11a755 HEAD` | rc0, output rỗng | **Đạt** |
| A4: doctrine | `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | rc0: sạch,10 tệp,0 chỗ chép doctrine | **Đạt scanner** |
| A4: CI PR trên exact HEAD | Kiểm artifact cục bộ; không gọi mạng theo chỉ thị | Không có check-run/receipt xác minh xanh cho ee3dc6d trong packet; run metadata của reviewer không phải CI | **KHÔNG ĐO ĐƯỢC; A4 tổng thể chưa đủ** |

## BANG DO

**Cách tìm khẳng định:** tự dựng và đọc toàn diffBASE..HEAD; `audit.py` bám dòng thêm theo hunk rồi trích comment bằng tokenize, hàm/docstring giao hunk bằng AST vào `claims-inventory.json` (**35 mục**, gồm cả thân hàm chứa phần sửa). Đọc tiếp các tuple DOT_BIEN đã đổi, `git log -1 --format=%B HEAD`, các message e6bf386/57 e2d4a/1027 f85 và lịch sử thay thiết kế. Dựng graph từ **toàn bộ** launcher, không lấy danh sách7 hàm trong test cấu trúc làm trần kiểm kê. Bảng gộp các khẳng định theo nghĩa; trích xuất tĩnh là cách tìm, không phải bằng chứng hành vi.

| Khẳng định | Diff khai | Đo được (lệnh/artifact) | Khớp? |
|---|---|---|---|
| No-shebang gây ENOEXEC; subprocess direct ném, bare có thể chạy bản sau | launcher2924–2926 | `extra_matrix.py`: raw subprocess0/LATER, helper/glibc0/FIRST; BASE(a)/(d) đỏ | Có |
| Hợp đồng glibc/bin/sh; Bash có thể khác | launcher2926; test9237 | matrix bash-syntax: Bash0/BASH_ONLY, helper/glibc127; wrong-arch: Bash126, helper/glibc2 | Có; không đồng nhất Bash với sh |
| Giữ candidate `<entry>/<name>`, trailing slash, relative/../symlink | launcher2927–2930/2945 | matrix/extra: first/cli,first//cli,link/../cli;9 property mutant riêng xác minh từng tính chất | Có các dạng đã đo |
| Empty candidate exec qua ./name, ENOEXEC dùng logical name | launcher2928–2930/2951–2954 | empty no-shebang `$0=cli`; mutant thêm ./ vào fallback giết chính assertion empty-$0 | Có; không mở rộng miễn trừ sang ENOEXEC |
| Entry quá dài không cuối như empty, cuối bỏ | launcher2928/2944–2946 | long-first/middle/multiple/last/boundary4095/4096; helper/glibc cùng chọn cwd/LATER hoặc cùng lỗi | Có về chọn executable; all-long errno0 vs2 khác diagnostic, cả 2 không chạy gì |
| Shebang qua cwd từ empty/overlong thấy ./name | launcher2931; HEAD message; lease g6 | extra_matrix WAIVER_CLASSIFIER: helper CHUA_XAC_THUC,glibc CO_CREDENTIAL cho **cả2 đầu vào**; matrix `$0=./cli`/`cli` | **Đúng mô tả, hành vi chưa vá, miễn W-1077-1**; không tính finding |
| env=None kế thừa, env thiếu PATH dùng defpath | launcher2942–2943 | contracts: ENV_NONE INHERITED; env={} true rc0; matrix PATH vắng true0 | Có |
| fsencode giữ PATH có byte ngoài UTF8 | launcher2943/2945; test9465 | raw-byte đầu/cuối/nonexistent đều chạy; strict mutant chết TinHieuChotCa mang UnicodeError thành dữ liệu | Có, F7 đóng đúng assertion |
| Chỉ 6 errno tiếp; lỗi khác dừng; ưu tiên EACCES rồi lỗi cuối | launcher2929–2930/2947/2955–2958 | matrix EACCES/ENOENT/ENOTDIR thực; ETXTBSY26/ELOOP40 dừng; EACCES→ELOOP40; ENOENT↔ENOTDIR ra20/2 | Có với lỗi thực đã đo; ESTALE/ENODEV/ETIMEDOUT filesystem thật **chưa dựng được**, không lấy đọc source làm đo thật 3 lỗi này |
| kwargs/argv/stdin/timeout/encoding/rc giữ nguyên | launcher2954; hai probe và wrapper llm | contracts8 neutral/8 mutant; physical stdin EOF,UTF8 replace,rc1/rỗng False,timeout True; target argv/env PASS | Có; không hứa deadline tổng mới |
| Windows nguyên trạng; no-sh không retry; không lượt3 | launcher2936–2937/2953 | contract guard1 spawn,second-error2 spawn; mutant chết đúng chốt; chroot125/EPERM | Mock đạt; native Windows/sh vắng thật **chưa đo được** |
| llm wrapper cùng các thuộc tính nêu trong docstring, chỉ3probe llm | launcher2960–2966;3 call site | contracts exact kwargs + stdin/UTF8 thật; callers llm default/live fixture parity; `_chay_van_ban_an_toan` cũ giữ nguyên | Có trong hợp đồng nêu rõ; wrapper mới không khai hỗ trợ mọi tùy chọn cwd/stdin của wrapper cũ |
| Caller đổi runner, giữ classifier và --no-log | 9 điểm nối cũ + wrapper; t115/t121 | callers8 nhóm × 2 trạng thái=16 parity;8 mutant raw helper chết chốt riêng; target M3b/c/d; test t121 hiện hữu | Có trong scope; không suy mọi classifier yêu cầu đầu ra giống nhau |
| Cấu trúc test/comment nêu rõ scope ngoại lệ | helper2933–2934; structural9381+; comment DOT_BIEN | audit graph,đọc3 nơi,đọc delegate codex_cred:197 | Có; không còn khai “mọi probe” mà giấu 2 đường #1083 |
| t115 chỉ bỏ executable; t121 stub đổi sang wrapper probe; t103/t111/t113 gỡ đổi | diff và lịch sử 01b9734 | AST 3 hàm bằng BASE; source t115;16 caller parity và full suite delta0 | Có |
| F5: dcfb236/19, e6 267/24; số tại 2320/457 | message e6 và các commit | audit Git object: 236/19,267/24,334/20,339/20; HEAD340/20 | Có; lời hứa ghi handoff **chưa đo được** vì handoff không trong bundle |
| F6: t103 có so tên nhưng2 nhánh Rc0, t113 không so | message 1027 f85 đính chính 57 e2d4a | source 3573–3575 và AST bằng BASE | Đính chính đúng |
| HEAD: lượt 9 có1 P1, mở rộng W, không đổi hành vi | `git log -1 --format=%B HEAD` | VERDICT-luot9 dòng1–4; lease g6 mien_tru/mo_rong; diff HEAD^..HEAD chỉ docstring, AST không doc bằng nhau | Có; không suy footer là attestation tác giả/model |

## KIEM KE HET PROBE DOCTOR VA SPAWN KHAC

| Đường quyết định nhãn | Spawn cuối tại HEAD | Phạm vi/kết quả |
|---|---|---|
| CONG_CU mọi candidate: git; python3/python/py; claude; codex; rg; bash; gh; npm; node; llm; agy; actionlint; shellcheck | `_phien_ban:2990 → helper2951/2954` | Trong scope; version rc/rỗng/timeout giữ classifier |
| CONG_CU auth (`claude auth status`, `agy models`); `_xac_thuc` bọc auth | `_xac_thuc_kem_dau_ra:3042 → helper` | Trong scope; doctor dùng bộ4 để cache đầu ra |
| Codex login status | `_do_codex:3937 → helper` | Trong scope; no-shebang positive CO_CREDENTIAL/negative CHUA_XAC_THUC |
| llm --version,keys list,prompt --no-log | `_do_openai_llm:4043/4051/4065 → _chay_probe_llm` | Trong scope; fixture không gọi API |
| gh auth status,gh api repos/slug | `_do_github:4574/4635 → helper` | Trong scope; classifier giữ nhãn; REST/Git khác dùng stub offline |
| claude mcp get | `_suc_khoe_mcp_github:4376 → helper` | Trong scope; positive khoe/negative hong |
| agy models; lùi --version; cache auth | `_do_antigravity:4108/4126 → auth/version helper` | Trong scope; DUNG_DUOC/CO_MAT như shebang |
| Codex --kiem-song | `_do_codex_song:3859 → runpy(codex_cred)._kiem_song → subprocess.run:197` | **Còn spawn trần; chuyển #1083 theo chủ kho**, không tính finding |
| Preflight snapshot của doctor nếu có CODEX_AUTH_JSON | `_chuan_bi_va_bo_snapshot:3222 → chuan_bi_xac_thuc → _probe_snapshot:3619 → cùng delegate codex_cred:197` | Ghi rõ thêm đường gián tiếp tới module ngoài write set, chưa phủ ENOEXEC; cùng giới hạn delegate, không nhận đã vá/toàn doctor. Không dùng snapshot thật |
| Git tìm workspace/rev-parse,ls-remote,remote get-url,git show hook/launcher master | `_git:286 → subprocess.run`; `_git_mot_dong` bọc | **Còn spawn trần; chuyển #1083 theo quyết định phạm vi**, dùng chung run |
| Claude credential,dấu vết hook,locale/PATH,module Python | Đọc file/env/hash/find_spec/import | Không thêm CLI spawn cần fallback |
| REST GitHub/MCP endpoint | urllib HTTP | Không exec CLI; phép đo caller riêng dùng stub. Probe nền trong full suite không xác minh được mạng |
| `_probe_spawn:1144`,runner Popen2299,`_chay_van_ban_an_toan:319` | subprocess run/Popen | Ngoài SPEC: `launcher run` |
| `_chay_json_chat_che:333` | subprocess run riêng | Không cạnh từ doctor trong graph đã rà |
| ps371/455/508/706,taskkill883,cây tiến trình | subprocess run riêng | Quản lý tiến trình, ngoài phân loại công cụ của packet |

Không tìm thấy đường CLI **trong phạm vi chủ kho giữ lại** còn gọi subprocess.run trần ngoài helper. Hai cơ chế thô Git/delegate vẫn được liệt kê, không xóa khỏi kiểm kê vì chúng đã được chuyển scope.

## DOI CHIEU TUNG FINDING CU VA BANG LOP

| Finding/lịch sử | Kết quả tại HEAD | Bằng chứng/giới hạn |
|---|---|---|
| F1: Codex status/llm/gh/MCP bỏ sót | **ĐÃ VÁ THẬT phần trong scope** | 16 caller parity;8 raw helper mutant đúng assertion;graph |
| F1: Git/Codex delegate | **CHUYỂN PHẠM VI, CHƯA VÁ** | #1083 theo quyết định chủ kho, không tính finding packet |
| F1: helper/ca cấu trúc/comment DOT_BIEN khai “mọi probe” | **ĐÃ SỬA THẬT lời khai** | Cả3 nơi đều nêu ngoại lệ; không chỉ sửa docstring mà bỏ comment |
| F2: đồng nhất Bash và glibc/bin/sh | **ĐÃ SỬA THẬT lời khai** | Bashism0/127,binary126/2; khác như công bố/hợp đồng M1 |
| F3: mất argv/env vẫn qua ca | **ĐÃ VÁ THẬT chốt** | target argv/env PASS;mutant mất argv chết đúng ca;contract argv/kwargs riêng |
| F4 lượt 2–6: bản sau,empty,abspath/symlink..,cwd dài,missing interpreter,errno/trailing slash | **ĐÃ VÁ các biểu hiện trong scope đã đo** | matrix/extra/permission,9 mutant riêng cho9 property; không nhận một kill sớm thay cho property sau |
| F4 lượt 7: byte ngoài UTF8 | **ĐÃ VÁ THẬT runtime** | raw byte nonfinal/final/vắng đều chạy |
| F4 lượt 7/9: shebang qua cwd từ empty/overlong PATH | **MIỄN W-1077-1 g6, CHƯA VÁ** | `$0` ./cli≠cli vẫn có hậu quả classifier,2 dạng đã tái hiện. Không dùng miễn trừ cho ENOEXEC hoặc dạng khác |
| F4 lượt 8: bỏ entry dài làm chọn LATER thay cwd | **ĐÃ VÁ THẬT chọn tệp** | long-first/middle/multiple/last/boundary; mutant drop-entry chết đúng assertion |
| F5: khai +228 ở dcfb | **ĐÃ ĐÍNH CHÍNH ĐÚNG** | Git236/19 và e6 267/24; việc ghi handoff chưa đo được |
| F6: phủ nhận t103 so tên | **ĐÃ ĐÍNH CHÍNH ĐÚNG** | Hai nhánh Rc0;AST t103/t111/t113 bằng BASE |
| F7: strict UTF8 chết bằng exception bên ngoài assertion | **ĐÃ VÁ THẬT chốt** | strict mutant TinHieuChotCa của chính r1077_PATH_hop_dong_glibc;UnicodeError thành dữ liệu |

Giữ slug lớp lịch sử **F4-phan-giai-PATH**; không tách2 miễn trừ thành findingmới hoặc nhận là sửa toàn lớp. Sổ finding cần sửa trong packet hiện tại: **0 lớp/0 biểu hiện** sau quyết định phạm vi/miễn trừ. Phần chưa vá chuyển#1083 và W vẫn tồn tại như đã ghi. Không reset lịch sử hoặc xin lượt 11.

## BANG TEST

| Bộ | N/M và rc | Bỏ qua/giới hạn |
|---|---|---|
| HEAD full | 291/315,rc1,tổng325,lỗi24 | 10 skip;đối chứngBASE cùng24 ID |
| BASE full | 280/304,rc1,tổng314,lỗi24 | Cùng10 skip;delta0;HEAD thêm11 pass |
| HEAD --dot-bien | DOT BIEN: 518/518 dat  (4 khong do duoc tren nen nay),rc0 | Khai riêng các mutant không đo được bên dưới; không nhận exception ngoài assertion thành kill wp1077 |
| targeted.py | 11/11 neutral;22/22 cặp mutant wp1077 đúng TinHieuChotCa;BASE2/2 đỏđúng assertion | Không skip;16 mutant mới |
| Propertymutant trong targeted.py | 9/9 đúng assertion riêng | symlink,longentry,interpreter,cwd,empty$0,relative$0,trailing slash,ETXTBSY,UTF8 |
| contracts.py | 8/8 neutral,8/8 mutant đúng assertion;6 physical probe | Windows/no-sh chỉmock;chroot125/EPERM |
| callers.py | 16/16 parity,8/8 raw helper mutant đúng assertion | 8 nhóm × 2 trạng thái;CLI giả |
| matrix.py | 58 dòng quan sát;56 so sánh chạyđược,51 khớprc/stdout | 2 thử setuidkhông đo được;5 khác biệt=2 W+3 diagnosticđều-fail. Không khai58/58 pass |
| extra_matrix.py | 20 quan sát gồm nativeargv0,rawcontrol,slash,errno,waiverclassifier,raw byte | Không network;chi tiếtJSON |
| permissions.py | 2 mode × 3 oracle khớp,2 listdirEACCES | UID0khôngbypassquyền trong sandbox;không setuid |

**24 lỗi HEAD/BASE cùng ID, không tính là hồi quy:**

- `t53_doctor_bao_du_khi_du`
- `r858_goc_tam_tranh_to_tien_co_git`
- `t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac`
- `r15_moi_provider_chi_mot_transport_va_hai_luot_on_dinh`
- `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat`
- `r926_lenh_run_khung_mat_thi_run_json_KHONG_DO_DUOC`
- `r926_dot_bien_tu_sinh_moi_thanh_phan_regex`
- `r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC`
- `r925_rust_log_thua_ke_bi_GHI_DE_khong_noi`
- `r925_codex_khong_co_khung_thi_KHONG_DO_DUOC_khong_suy_tu_m`
- `r925_codex_qua_han_van_124_va_giu_khung_da_den`
- `r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC`
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
- `r927_lenh_run_ghi_effort_va_sandbox_vao_run_json`

`t53`: JSON nêu thiếu claude/codex trong PATH sạch, rc12; không phải kết quả no-shebang bị gắnBI_CHE. `r858`/`t86`: `/var/tmp` read-only, errno30. Các ca storage/materializer r484: `/tmp/.git` tồn tại (`ls -d /tmp/.git` đã chạy), “Codex home is inside a repository” và các hậu quả trước khi child được gọi. `r15`/r925/r926/r927: fixturecodex bị chặn trước spawn, “CHỜ snapshot Codex mới”, hoặc không có thư mục runs; cùng điều kiện/cùng ID trênBASE. Đây là phép đo **không đạt trong môi trường này**, không tuyên bố từng ca ấy xanh hay lỗi chỉ có đúng một nguyên nhân. `suite-comparison.json`: head_only=[],base_only=[],same_skips=true. Không xóa `/tmp/.git`, không sửa credentialpreflight để làm suitexanh.

**10 ca bỏ qua giống nhau, không cộng vào tử số:**

- BO QUA t62_qua_han_ma_khong_giet_het_cay_phai_tra_125: fixture nay danh cho Windows; ban POSIX la t63 (chay duoc, khong bo qua)
- BO QUA r345_chan_socket_that_ma_than_hook_van_chay_dung: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- BO QUA r345_cac_phep_do_cuc_bo_van_dung: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- BO QUA r345_lop_tham_import_van_co_rang: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- BO QUA r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- BO QUA r347_tham_import_van_song_tren_python_truoc_310: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- BO QUA r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- BO QUA r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- BO QUA r348_dot_bien_bo_isidentifier_lam_ca_dich_DO: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- BO QUA r484_g4_windows_sid_alias_identity: BO QUA native Windows SID conversion

**Mutant không đo được theo harness, ghi riêng:**

- g4_windows_sid_alias_not_normalized KHONG DO DUOC tren nen nay (native SID conversion)
- g4_windows_LA_not_current_owner KHONG DO DUOC tren nen nay (native SID conversion)
- g2_windows_directory_pin_access KHONG DO DUOC tren nen nay (native Windows share-delete pin)
- 124_khi_chau_con_song        KHONG DO DUOC tren nen nay (ca dich bo qua: t62_qua_han_ma_khong_giet_het_cay_phai_tra_125)

## BANG SAN

| Hướng độc lập | Lệnh từ cay-kho/ | Output thật | Phán định |
|---|---|---|---|
| 1. Các dạng PATH/tên/argv0: rỗng, tương đối, .., symlink, slash, PATH vắng, env=None, cwd>4200, tên có space/dash/Unicode | `python3 -B ../evidence/matrix.py`; `python3 -B ../evidence/extra_matrix.py`; `python3 -B ../evidence/contracts.py` | Chọn FIRST đúng inode; giữ first//cli; native argv0=native, 2 đối số, đối số cuối=two words; env=None in INHERITED; env={} chạy true rc0; cwd dài helper/glibc rc0 | **KHÔNG PHẢI LỖI** ở các dạng trong scope; các khác biệt được phân loại riêng |
| 2. Trật tự errno và interpreter thiếu | `python3 -B ../evidence/matrix.py`; `python3 -B ../evidence/extra_matrix.py` | EACCES+ENOENT→13; ENOENT→ENOTDIR ra20, đảo thứ tự ra2; ETXTBSY26/ELOOP40 dừng; thiếu interpreter thì chọn LATER | **KHÔNG PHẢI LỖI** với lỗi thực đã đo; ESTALE/ENODEV/ETIMEDOUT trên filesystem thật chưa đo được |
| 3. Quyền thư mục và thiếu bit x | `python3 -B ../evidence/permissions.py`; `python3 -B ../evidence/targeted.py` | listdir EACCES13 ở cả000/0111; mode000 chọn LATER, mode0111 chạy FIRST ở cả3oracle; shebang0644 probeFalse | **KHÔNG PHẢI LỖI**. Hai phép thử setuid ban đầu bị EPERM; phép đo cuối không dùng setuid |
| 4. Binary sai kiến trúc, empty, BOM, cú pháp Bash | `python3 -B ../evidence/matrix.py`; `python3 -B ../evidence/contracts.py` | ELF: helper/glibc2, Bash126; empty raw rc0 nhưng version/authFalse; BOM127; cú pháp Bash: Bash0, helper/glibc127 | **KHÔNG PHẢI LỖI** theo hợp đồng glibc/bin/sh. Không gắn khả dụng cho tệp rỗng |
| 5. Đối số/env/stdin/mã hóa/timeout/rc và điều kiện retry | `python3 -B ../evidence/contracts.py`; `python3 -B ../evidence/targeted.py` | 8/8 neutral,8/8 mutant assertion; stdinEOF/UTF8replace; timeout trả False/qua_han=True; rc1/rỗngFalse; lỗi lượt2 dừng ở2spawn | **KHÔNG PHẢI LỖI** M1 |
| 6. Byte filesystem ngoài UTF8 và độ nhạy ca gộp | `python3 -B ../evidence/targeted.py`; `python3 -B ../evidence/extra_matrix.py` | Strict UTF8 mutant chết TinHieuChotCa; raw-byte cuối/không cuối rc0/RAW_FIRST;9 property mutant chết đúng chốt | **KHÔNG PHẢI LỖI**, F7 đã đóng đúng assertion |
| 7. Graph caller và classifier | `python3 -B ../evidence/audit.py`; `python3 -B ../evidence/callers.py` | 16/16 parity;8/8 mutant raw-helper đúng assertion; Git/delegate thô vẫn được liệt kê | **KHÔNG PHẢI LỖI** trong scope giữ lại; hai cơ chế thô thuộc #1083 |
| 8. Shebang kiểm $0 qua cwd do PATH rỗng/quá dài | `python3 -B ../evidence/extra_matrix.py`; `python3 -B ../evidence/matrix.py` | Cả2dạng: helper CHUA_XAC_THUC/$0=./cli, glibc CO_CREDENTIAL/$0=cli | **KHÔNG TÍNH FINDING** theo W-1077-1 g6; hành vi chưa vá |
| 9. Khẳng định định lượng, lịch sử và gate | `python3 -B ../evidence/audit.py`; `python3 -B ../evidence/run_suites.py` | +340/-20; dcfb236/e6267; Ruff17/17 delta0; doctrine10/0; full suite cùng24ID lỗi. history-final.json: AST bỏ docstring bằng parent | **KHÔNG PHẢI LỖI** với các số đã đo; CI chưa đo được |
| 10. Native Windows, sh vắng, CI và các diagnostic đều thất bại | `python3 -B ../evidence/contracts.py`; `python3 -B ../evidence/matrix.py` | Windows guard mock1spawn; chroot125/Operation not permitted; all-long errno0/2, filename dài errno2/36 nhưng đều không chạy được công cụ; bundle không có CI receipt | Native/CI: **KHÔNG ĐO ĐƯỢC**. Khác diagnostic khi đều thất bại chưa có bằng chứng đổi nhãn khả dụng, không tự nâng thành finding |

## HINT VA TINH TOAN VEN

Không có finding cần vá trong scope; `HINT.patch` rỗng, không đề xuất sửa runtime hoặc mở rộng miễn trừ. Không áp patch lên `cay-kho/`.

HEAD/tree cuối khớp đầu, tracked diff/index diff rỗng. Snapshot hash nội dung ngoài Git tại mốc audit và cuối: `{'added': [], 'removed': [], 'changed': []}`. Mốc audit được lấy sau khi full suite đã bắt đầu, nên không dùng nó để khẳng định mọi ignored file chưa từng thay đổi trong cả lượt. Ở mốc audit đã thấy ignored `.claude/.packet_state/session-start.ran` do hook/test cục bộ; giữ lại và ghi nhận, không nhận Git status rỗng là chứng minh không phát sinh runtime artifact. Không chỉnh sửa tệp nguồn hoặc ref executor. Chi tiết ở `integrity-final.json`; không có nguồn repo thứ hai được cấp để snapshot.

**Kết luận exact HEAD: approve nội dung; 0 finding trong phạm vi đã cấp.** CI/A4 chưa đo được phải được xác minh trước khi báo đủ điều kiện merge. Kết thúc lượt 10/10 tại đây, không tự cấp lượt mới hoặc thực hiện merge/push.
