verdict: dang_lam
reviewed_sha: 51ae5c095972611d2c6045bd81786a4fc7e9ca62
spec_sha256: 5caec680395ae3dbe673091153e917feb4262a69142f36e54c63a2260d48bdad

Đã tái hiện một finding P1 (F03 tái mở qua hàm Python kế thừa); đang đợi bộ cong_cu hoàn tất trước khi chốt.

## BANG NGHIEM THU

Các lệnh sản phẩm dưới đây chạy từ `cay-kho/`; script reviewer chạy từ thư mục chứa `VERDICT.md`. Các phép chạy bổ sung đặt `PYTHONDONTWRITEBYTECODE=1 PIP_NO_INDEX=1`. “macOS” trong fixture là công thức YAML macOS với brew giả trong Bash Linux, không thay phép đo macOS native.

| Tiêu chí | Lệnh chạy được | Output thật | Đạt? |
|---|---|---|---|
| N1: Linux nguyên công thức, rg đầu PATH hỏng, dương/âm | `python3 .claude/dev/launcher_test.py --lap-ca r831_cai_rg_linux_chon_ban_chay_duoc --lan 1`; đã chạy ca trong full suite và mutation; bổ sung `python3 evidence/edge_probes.py candidates` | Ca r831 không nằm trong 12 ca đỏ; fixture riêng 21/21 tổ hợp Linux đúng; bỏ ứng viên usrbin → TinHieuChotCa rc2 | Đạt các ca đóng băng |
| N2: macOS công thức/brew stub | `python3 .claude/dev/launcher_test.py --lap-ca r831_cai_rg_macos_chon_ban_chay_duoc --lan 1`; cùng phép đo như N1 | 21/21 tổ hợp công thức macOS đúng; bỏ ứng viên brew → TinHieuChotCa rc2 | Đạt fixture, native KHÔNG ĐO ĐƯỢC |
| N3: checker chính thức, tiền tố install giữ nguyên | `python3 evidence/probes.py docs`; `python3 evidence/probes.py mutations`; `python3 evidence/edge_probes.py candidates` | Parity r802 PASS; 5 mutant wp831 và mutant neo wp802 bị giết; mã cài Linux/macOS đúng base; output rác/rc0 không được chọn | Đạt |
| N4: bảng doctor theo nền, thiếu/xác thực sai/BI_CHE; hai cổng docs | `python3 evidence/probes.py docs`; `python3 scripts/tl.py doc-claims-check --strict`; `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 6 ca r802 PASS; tập bắt buộc khớp bảng; `ok=true`, 0 blocking; doctrine sạch10 tệp | Đạt |
| N5: manifest cuối | `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | rc0, ok=true, expected=checked=189; extra/failed rỗng; hash khớp | Đạt |
| N6: selftest/ratchet, delta nền | `python3 scripts/tl.py --selftest`; cùng lệnh trên clone nền; `python3 evidence/ratchets.py`; `python3 evidence/git_environment.py` | Raw head=nền1729/1731, chỉ r226/r268 đỏ do signing=true; trích hai ca signing=false đều qua; ratchet6/6 đúng kỳ vọng. HEAD cô lập signing: **1731/1731**, rc0 (`evidence/selftest-signing-off.log`) | Đạt với cô lập signing; raw môi trường đỏ |
| N7: venv thật thiếu yaml, ghim interpreter, đơn | `python3 evidence/edge_probes.py entries`; `python3 evidence/probes.py mutations`; `python3 evidence/function_regression.py` | 84/84 bố cục thường; bỏ ghim → đúng hai r831 TinHieuChotCa rc2. Hàm python kế thừa → hai ca mới đỏ; sửa riêng bản sao → cả hai PASS | Ca đóng băng đạt, bất biến ghim còn lỗi F03 tái mở |
| N8: --bat-buoc rg→bash thật, không chọn lại Python | `python3 evidence/probes.py runtime`; `python3 evidence/edge_probes.py inherited` | 24/24 và72/72; cả rg/bash DAT; bỏ dùng lại/bỏ dấu → hai ca r831 đỏ rc3 thiếu yaml; không thêm mutation shell vào DOT_BIEN_HOOK | Đạt ca đóng băng; đường hàm kế thừa vẫn lỗi |
| Trần/phạm vi r4 | `python3 evidence/probes.py claims`; `git diff --numstat 6b641ca2a2b889c9f43eec58bae47a00a80373cd 51ae5c095972611d2c6045bd81786a4fc7e9ca62` | 8 tệp, +380/−18; đúng write set; sửa selftest chỉ ratchet/chú thích, shell chỉ ghim/dùng lại/chú thích | Đạt |
| Cổng launcher / đột biến / ruff / bash-n | Các lệnh trong BANG TEST; `bash -n ops/cai_cong_cu.sh` | Launcher 214/226 +12 môi trường; mutation277/277 +4 không đo; ruff delta0; bash-n rc0 | Không đọc 12 lỗi môi trường thành hồi quy; các ca liên quan packet qua |
| Cổng có/không credential giả | Full suite mặc định đã chạy; không tự soạn CODEX_AUTH_JSON | Chỉ có vế mặc định. Vế có credential giả không tự dựng theo mục5 của prompt; credential nghiệp vụ còn bị /tmp/.git chặn | KHÔNG ĐO ĐƯỢC đầy đủ |
| CI, Windows trên exact HEAD; một lần push/budget/authority | Không gọi mạng; kiểm được refs/commit offline bằng Git, không kiểm được check run/Issue | Không có phép đo GitHub/Windows native; không suy từ handoff hay merge rằng CI đã xanh | KHÔNG ĐO ĐƯỢC |

## BANG DO

Cách tìm khẳng định: đối chiếu byte toàn `diff.patch` với `git diff` đúng hai OID; phân tích hunk và kiểm kê **380 dòng thêm**, đọc cả phần bỏ/ngữ cảnh. `evidence/diff-lines.json` và `evidence/claim-inventory.md` giữ từng tệp/dòng/text, gắn các nhóm Dxx dưới đây. Quét số, SHA 7–40/64 ký tự, tên ca, N/M, từ điều kiện (“chỉ”, “đầu tiên”, “không”, “cả hai”, “nguyên văn”, “tuyệt đối”), rồi đối chiếu lệnh/runtime thay vì chỉ grep. `evidence/sha-inventory.json` tách commit, spec hash, kích thước manifest, run/comment ID; không coi số thập phân là Git OID. Các nhóm lịch sử không có bằng chứng offline được đánh KHÔNG ĐO ĐƯỢC, không mặc định khớp. Không đọc verdict cũ của PR này.

| ID / Khẳng định | Diff khai | Đo được bằng lệnh/artifact | Khớp? |
|---|---|---|---|
| D01 ứng viên Linux/macOS/thứ tự | usrbin→command-v; brew/bin→command-v; bản đầu hỏng không được chọn | `edge_probes.py candidates` 42/42, có cả hai bản tốt để đo ưu tiên và ứng viên xấu để đo fallback | Có trong fixture |
| D02 cần tồn tại/thực thi/checker DAT | -f/-x và checker kiem-tra --chi rg; rc0 rỗng/token rác không đủ | candidates42; mutation YAML theo mã thoát/loại-x bị giết bằng assertion; đối chiếu đúng câu lệnh YAML | Có |
| D03 không ứng viên thì fail | rc≠0, không ghi GITHUB_PATH | Mọi tổ hợp âm candidates; r831 và mutation CLI | Có |
| D04 GITHUB_PATH có điều kiện | Chỉ ghi khi bare rg chưa DAT; không ghi khi bare tốt | Các ca r831; mutant ghi vô điều kiện chết với rc0 nhưng path không rỗng | Có; CI phiên bản Python lịch sử xem D16 |
| D05 ghim PY[0] tuyệt đối, giữ py -3 | Python không đổi khi PATH đổi | entries84 thường qua, py shim kiểm -3; `python-resolution.log`: command-v=python khi là hàm; function-regression hai ca đỏ | **Không — finding F03 tái mở** |
| D06 source batch dùng lại mảng | Dấu cùng $$ không export; giữ interpreter cha | runtime24, entries84, inherited72; mutant A/B chết rc3 | Có ở đầu vào đã đo, còn điều kiện D05 |
| D07 môi trường kế thừa/exec | Dấu export bị loại; PY vô hướng không được dùng | inherited72 qua; D bỏ loại export khiến installer thấy PID; E sống ở ca cũ nhưng array_invariant bản sao đỏ đúng | Có cho biến môi trường thông thường |
| D08 allexport | Gán rồi declare+x; con ABSENT | 3 chế độ runtime/inherited, source+set-a entries; G bỏ declare+x → thiếu yaml/rc3 | Có |
| D09 F05 giữ mọi installer trong fixture | Symlink bash, kiểm trước wrapper, sudo gọi apt tuyệt đối, đếm1/2 | H và I giết đúng ca; sudo_absolute đổi PATH chỉ giữa hai stub, nguyên bảnPASS/mutantTinHieuChotCa | Có; không tuyên bố biết installer thật đã chạy trong lịch sử |
| D10 manifest/số khe | 187→189, thêm wp802/wp831, còn10 khe | claims: hai path thêm đúng; 189 mục size/hash đúng; strict release189/189; 200−190=10 kể manifest | Có |
| D11 doctor theo nền/rc12 | git/python/rg/bash luôn; claude/codex trừCI; gh máy người dùng; BI_CHE chỉ git/rg | `_bat_buoc` cho user/remote/CI/GitHub/CI+remote; 6 ca doctor/parity thực chạy; doc_claims/doctrine | Có với giá trị dấu nền “true” của mã |
| D12 tên ca/đột biến/anchor | 2 r831; 5 wp831; neo wp802 chỉ1 chỗ | AST/claims/6 anchor đều1; mutations6 YAML giết đúng ca | Có |
| D13 các SHA/spec/base/merge | r1 92d179bc, r2 3ab3aac4, r3 dd8f0fab, r4 5caec680; dfe5437, 1e69d2a, các head lịch sử | SHA256 4 spec; `git rev-parse --verify <sha>^{commit}`; 15 token commit trong diff resolve; `git merge-base --is-ancestor` cho base/merge source | Spec/commit có thật; nhánh không thay OID làm chuẩn |
| D14 số ca lịch sử | nền232/232, head234/234 (có auth); không auth231/232,233/234; riêng t8610/10 | AST tại1e69d2a=234 đăng ký,720ee87=236; mẫu số có thể loại BO QUA. Không mở log/verdict review cũ theo chỉ thị | N/M/chế độ auth và10/10 lịch sử KHÔNG ĐO ĐƯỢC; không bác chỉ từ AST |
| D15 mutation/Windows lịch sử | @720ee87:281 đo+4 không đo; bỏ9 còn5 để197/281≈70.1% | AST @720 tổng285 (262+16+7), HEAD281 (262+12+7); phép tính197/285≈69.1%,197/281≈70.1%; nativeWindows chưa chạy | Tổng và phép tính khớp;197 native/lượt CI KHÔNG ĐO ĐƯỢC |
| D16 số run/JSONSchema/Python/rc/duration/authority cũ | CI39115659366,39115887003,lease runs39113916942/39128676976;3.12.3,4.10.3/4.26.0; các issuecomment; số giây review | Không mạng, không receipt runtime hay output CI trong packet được đo; không suy từ Git commit tác giả | KHÔNG ĐO ĐƯỢC, không phải finding suy đoán |
| D17 N6/ratchet/handoff1731 | selftest1731, hai ratchet189 | raw head=nền1729/1731; signingtrue→false đóng đúng hai fail ở cả hai; ratchets6/6 đúng; HEAD cô lập signing: **1731/1731**, rc0 (`evidence/selftest-signing-off.log`) | Delta0, các ratchet có răng |
| D18 sửa sau lượt6 | 9385ad2 chỉ fixture F05,51ae5c0 chỉ handoff | `git show --stat`/diff:13+/3− test;10+ handoff; H/I/sudo probes như D09 | Có |
| D19 trạng thái review cũ/F01–F04, ma trận12/24/48/216/576 và E/F | Handoff nói các lớp đã đóng, E sống có chủ ý; lịch sử review1…6 | Không đọc verdict cũ. Đo lại lớp hiện tại bằng runtime24+entries84+inherited72+candidates42; F01/marker/allexport qua, hàm interpreter làm F03 tái mở. E được cô lập thử riêng | Phép đo hiện tại cụ thể khớp; các tổng lịch sử KHÔNG ĐO ĐƯỢC; câu đóng toàn lớp cần thu hẹp |
| D20 nợ/ngoài phạm vi | git/python/shellcheck/bash dirname; bash prepend có thể làm rg đỏ; t86 song song; fixedtemp selftest; Windows/bash_nen warning; signing | Xem nguyên công thức và source; không tự tái chạy installer thật/can thiệp credential; signing đã đo thực nghiệm; F05 giữ bash ở stub để kiểm test | Giữ nguyên các quyết định ngoài phạm vi, không mở finding cho nợ ấy |

## BANG TEST

Mã thoát trong `evidence/*.rc` là rc tiến trình test, không phải rc của shell `tail`/ghi log. Giữ nguyên headline raw; “KHÔNG ĐO ĐƯỢC” tách riêng với PASS/FAIL.

| Bộ / lệnh | N/M thực tế | Bỏ qua / giới hạn |
|---|---|---|
| `python3 .claude/dev/launcher_test.py` | **214/226** đã chạy qua; tổng236; HỎNG12; rc1 | BO QUA10. Cả12 đỏ là môi trường credential, baseline12/12 tái hiện; không coi chúng PASS |
| `python3 ops/cong_cu_test.py` | ĐANG CHẠY: 60/60 ca đã chạy qua, tổng61; bán kính470 chưa trả kết quả cuối | 1 ca t47 không dựng được INDEX chưa hòa giải (stage={0}); không coi là PASS |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | **189/189**, rc0, ok=true | Không bỏ qua; links15, pointers326, bare tools278 không fail; advisory không phải blocking |
| `python3 .claude/dev/launcher_test.py --dot-bien` | **277/277**, tổng281; rc0 |4 không đo được do nền |
| `python3 scripts/tl.py --selftest` HEAD / nền | **1729/1731** ở cả hai, rc1; delta ca đỏ0 | Không có skip headline;2 đỏ r226/r268 do Git signing; không đánh PASS raw |
| HEAD selftest với `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false` | HEAD cô lập signing: **1731/1731**, rc0 (`evidence/selftest-signing-off.log`) | Không đổi config hay source của cây |
| `python3 evidence/ratchets.py` |6/6 kết quả đúng kỳ vọng | Hai [FAIL] là mutant đích, không phải baseline fail |
| `python3 evidence/probes.py mutations` |13/15 mutant bị giết đúng;20/24 lần gọi ca TinHieuChotCa;rc0 harness | E/J sống, đo bổ sung tách lớp bằng array_invariant/sudo_absolute; không báo15/15 giết ở ca cũ |
| `python3 evidence/edge_probes.py candidates` / `entries` / `inherited` |42/42 ·84/84 ·72/72 | Chỉ POSIX Linux với công thức hai nền, py là shim kiểm -3 |
| `python3 evidence/probes.py runtime` / `docs` |24/24 ·6 ca doctor/parity PASS | Tập bắt buộc cũng đo trực tiếp |
| `python3 evidence/function_regression.py` |HEAD **0/2**; scratch giải executable **2/2** | Chính TinHieuChotCa của hai ca mới; `HINT.patch` test-only, dry-run -p0 ngoài cây rc0 |
| `doc-claims-check --strict` / `doctrine-scan --root .` |ok=true,113 tệp/0 blocking · sạch10 tệp/0 chỗ chép;rc0 |381 advisory trong doc-claims |
| `ruff check --select F` hai tệp Python đổi |Head=nền4397: F8415,F8214391,F4011; delta0 |rc1 cả hai; không dùng rc1 làm lỗi packet |
| `bash -n ops/cai_cong_cu.sh` |rc0 |Chỉ kiểm cú pháp, không thay runtime |

10 ca BO QUA launcher, nguyên tên: `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125` (Windows); `r345_chan_socket_that_ma_than_hook_van_chay_dung`, `r345_cac_phep_do_cuc_bo_van_dung`, `r345_lop_tham_import_van_co_rang`, `r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO`, `r347_tham_import_van_song_tren_python_truoc_310`, `r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO`, `r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia`, `r348_dot_bien_bo_isidentifier_lam_ca_dich_DO` (8 ca không dựng được venv/pip, không mạng); `r484_g4_windows_sid_alias_identity` (SID native Windows).

4 mutant launcher KHÔNG ĐO ĐƯỢC: `g4_windows_sid_alias_not_normalized`, `g4_windows_LA_not_current_owner` (SID native), `g2_windows_directory_pin_access` (Windows share-delete pin), `124_khi_chau_con_song` (ca t62 chỉ Windows).

## BANG SAN

Mười hướng độc lập, mỗi hướng có lệnh và output thật, được ghi tăng dần ở nhật ký bên dưới: manifest; doctor/docs; batch/allexport; bộ chọn ứng viên; write set/SHA; interpreter/entry modes; F05/đột biến phòng thủ; ratchet; hàm Python kế thừa; môi trường nền. Kết luận lần lượt: KHÔNG PHẢI LỖI cho1–8 trong phạm vi đo, **LỖI** cho9, KHÔNG PHẢI LỖI của packet cho10. Phần native Windows/macOS, mạng/GitHub và lịch sử không có log: **KHÔNG ĐO ĐƯỢC**, ghi cụ thể ở bảng trên.



## Nhật ký đo — preflight

- `git -C cay-kho rev-parse HEAD` → `51ae5c095972611d2c6045bd81786a4fc7e9ca62`; tree `a59ccc5a870d2ab6f250e6a3f3ca9aa07d8729fa`; `git status --short` rỗng.
- `sha256sum SPEC.md` → `5caec680395ae3dbe673091153e917feb4262a69142f36e54c63a2260d48bdad`.
- `git diff 6b641ca2a2b889c9f43eec58bae47a00a80373cd 51ae5c095972611d2c6045bd81786a4fc7e9ca62 | sha256sum` → `9d2adf985c29c805f3cf707ce9cf027d568ed3af97a4990732dea04fa922dfc2`, khớp `diff.patch`.
- Đặc tả kế thừa lấy bằng `git show refs/remotes/origin/ops/wp831-r4-g4-lease:ops/specs/wp831{,-r2,-r3,-r4}.md` (từng tên riêng). Băm r1 `92d179bca46c3523f1ce21e3a65bd06d6074237ffa79b8bf293cba3179659888`, r2 `3ab3aac4c68a7bbe87daf5dfee75c649ff46110697b2cd5b00b29586e4c253e7`, r3 `dd8f0fab5e3592975e4cde2f180fe0d052fc66e67fae15194e71970cb02f65e6`; r4 khớp SPEC. Lưu bản đọc tại `evidence/wp831*.md`; không mở verdict cũ.
- `/tmp/.git` có mặt, là thư mục bảo vệ rỗng. Các lỗi credential do home nằm trong repository sẽ ghi KHÔNG ĐO ĐƯỢC, không coi hồi quy.
- Đang chạy ba lệnh bắt buộc, đặt `PYTHONDONTWRITEBYTECODE=1` để tránh bytecode trong cây đọc. Log và rc ở `evidence/{launcher,cong_cu,release}.{log,rc}`.
- Danh tính theo phiên hiện tại: Codex/OpenAI, thực thi shell qua tool của môi trường API, transport machine; không có phép đo runtime cho model ID chi tiết, không suy từ GitHub actor; chưa đăng ra ngoài.

### Hướng 1: tính toàn vẹn manifest — KHÔNG PHẢI LỖI
`PYTHONDONTWRITEBYTECODE=1 python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` tại `cay-kho/`: rc 0, `ok=true`, `expected_file_count=checked_file_count=189`, `failed=[]`, `extra_files=[]`, package hash `1f2f6d8c6d6d1590ec3e6e522170b5dba291b6fb72d93dccd3c56a0c72bf6d05` khớp. Output đầy đủ: `evidence/release.log`.

### Không gian đầu vào Python, liệt kê trước khi đo
1. Lệnh mới chạy `bash script rg` hoặc `bash script --bat-buoc`, môi trường không dấu, dấu rỗng/sai/khớp PID; `PY` vô hướng trống/tên/tuyệt đối.
2. Cha dùng `exec` giữ PID; phân biệt dấu export đến từ ngoài với dấu shell không export do vòng batch tạo.
3. `source` cùng shell; thứ tự `rg→bash` và `bash→rg`; source trong subshell (phân biệt $$ với BASHPID); nguồn BASH_ENV/ENV và hàm shell export cũng là đầu vào của Bash, cần phân biệt với môi trường biến thông thường.
4. `allexport`: tắt, `bash -a`, `SHELLOPTS=allexport`, `set -a` trước source; kết hợp dấu/PY kế thừa.
5. Cách tìm interpreter: python, chỉ python3, chỉ py -3; đường có dấu cách/Unicode; PATH tương đối; hàm/alias shell; giữ đối số của mảng.
6. Đường PATH đổi: công thức rg trong command substitution, lượt source tiếp theo, checker cuối; thư mục ứng viên có venv thật không PyYAML; công thức bash thêm lại thư mục của chính nó.
Đây là danh sách tìm hướng thử, chưa phải tuyên bố tất cả đã đo. Hướng liên quan credential/thoát cây chỉ mô tả bằng lời, không tự dựng tải trọng.

### Hướng 2: bảng doctor và cổng tài liệu — KHÔNG PHẢI LỖI
- `PYTHONDONTWRITEBYTECODE=1 PIP_NO_INDEX=1 python3 evidence/probes.py docs`: `_bat_buoc` đo máy người dùng = git/python/claude/codex/rg/gh/bash; remote bỏ gh; CI và CI+remote bỏ claude/codex/gh; `_AP_DUNG_BI_CHE=['git','rg']`, rc thiếu = 12. Sáu ca r802 liên quan doctor/parity đều PASS (`evidence/docs.log`).
- `python3 scripts/tl.py doc-claims-check --strict` rc 0, `ok=true`, 113 tệp, 0 lỗi blocking (381 advisory); `python3 .claude/dev/packet_loop.py doctrine-scan --root .` rc 0, sạch 10 tệp, 0 chỗ chép (`evidence/doc_claims.log`, `evidence/doctrine.log`).
- Ruff: head và nền diff đều F841=5, F821=4391, F401=1 (4397 tổng); delta=0, không đọc rc=1 thành hồi quy (`evidence/lint-comparison.json`). `bash -n ops/cai_cong_cu.sh` rc 0.

### Hướng 3: batch, allexport và exec — KHÔNG PHẢI LỖI trong phạm vi đã đo
`PYTHONDONTWRITEBYTECODE=1 PIP_NO_INDEX=1 python3 evidence/probes.py runtime` → 24/24: 2 công thức nền × 3 chế độ allexport × 2 có/không dấu/PY kế thừa qua exec × 2 thứ tự batch. Mọi lượt rc 0, rg/bash DAT, hai installer thấy ABSENT, GITHUB_PATH đúng ứng viên. Đây là shell Linux chạy công thức macOS với brew giả, chưa phải macOS native. Output `evidence/runtime.log`, `evidence/runtime.json`.

### Hướng 4: bộ chọn ứng viên độc lập — KHÔNG PHẢI LỖI
`PYTHONDONTWRITEBYTECODE=1 PIP_NO_INDEX=1 python3 evidence/edge_probes.py candidates` → 42/42. Fixture riêng không dùng helper r831: 2 nền × 7 dạng ứng viên (tốt, tốt+kêu stderr, exit1, rc0 rỗng, token rác, thiếu, không thực thi) × 3 bản đầu PATH (tốt/hỏng/thiếu). Đo thứ tự ưu tiên ứng viên rồi fallback, không ứng viên thì rc≠0/GITHUB_PATH rỗng. Installer chỉ là stub; log `evidence/candidates.log`/json.

### Hướng 5: write set, SHA và băm — KHÔNG PHẢI LỖI
`python3 evidence/probes.py claims` → 8 tệp, 380 dòng thêm/18 bỏ, trong trần 8/450. Manifest nền 187 → head189, chỉ thêm `changelog.d/wp-802.md`, `changelog.d/wp-831.md`; kiểm độc lập 189 mục size/SHA không có mục sai; số khe theo cách kho đếm cả manifest: 200−(189+1)=10. Sáu anchor YAML liên quan đều count=1. OID các commit được resolve đầy đủ trong `evidence/claims.log`; riêng commit `9385ad2c200c4859a30160967e5fa39d55ce5f7c` chỉ sửa test, `51ae5c095972611d2c6045bd81786a4fc7e9ca62` chỉ sửa handoff.
Số ca đăng ký tại `1e69d2a`=234, `720ee87`=236, head=236 (khác số ĐÃ CHẠY vì skip); bảng mutation tại `720ee87` tổng285, head281. Không suy lại các N/N lịch sử từ số ca đăng ký.

### Hướng 6: wrapper/interpreter độc lập — KHÔNG PHẢI LỖI ở 84 bố cục thông thường
`python3 evidence/edge_probes.py entries` → 84/84: 2 nền × 3 lựa chọn python/python3/py -3 × 2 thứ tự × 7 đường gọi (script, exec, source, source+set-a, source trong subshell, bash-a, SHELLOPTS). Đường fixture có dấu cách và Unicode; venv ứng viên thật thiếu yaml; hai installer chỉ thấy ABSENT. `py` shim đòi đối số đầu đúng -3. Output `evidence/entries.log`/json.
`python3 evidence/edge_probes.py inherited` → 72/72: 2 nền × đơn/batch × dấu khớp PID/sai/rỗng × PY rỗng/venv × 3 allexport. Output `evidence/inherited.log`/json.

### Hướng 7: F05 và lớp phòng thủ — KHÔNG PHẢI LỖI
- `python3 evidence/probes.py mutations`: 15 đột biến trên cây sao ở `evidence/mutation-copies/`; 13 bị giết, 2 sống. 20/24 lần gọi ca bị giết bởi chính `TinHieuChotCa`, 4 lần sống là E/J, không có lỗi vô can. Sáu YAML mutations bị giết đúng; A bỏ dùng lại/B bỏ dấu → rc3 thiếu yaml ở bash; C bỏ ghim → rc2; D bỏ loại export → installer thấy PID; G bỏ declare+x → allexport rc3. H bỏ symlink → hai ca đỏ `fixture ro: bash ten tran la '/usr/bin/bash'...` TRƯỚC wrapper. I bỏ nhật ký stub → rc0 và cả hai DAT nhưng ca đỏ vì `installer thay []`, xác nhận assertion đếm thật có răng. `evidence/mutations.log`/json.
- E bỏ array guard sống ở r831 sẵn có, đúng phòng thủ chiều sâu được handoff nêu. `python3 evidence/guard_probes.py array_invariant`: tạo dấu không export + PY vô hướng trong CÙNG shell (không phải biến môi trường kế thừa). Bản nguyên PASS rc0; bỏ guard trên bản sao → chính assertion `TinHieuChotCa`, rc3 thiếu yaml. Đây là phép đo riêng bất biến, không nhận nó là phản chứng tấn công qua môi trường ngoài.
- J bỏ đường tuyệt đối trong sudo stub sống ở r831 vì symlink đã giữ PATH đúng. `python3 evidence/guard_probes.py sudo_absolute`: gọi đúng stub với PATH chỉ chứa apt-get GIẢ KHÁC; nguyên bản gọi fixture một lần, bỏ đường tuyệt đối → chính assertion `TinHieuChotCa: ...fixture=[], alternative=True`. Cả hai chỉ gọi stub vô hại, không gọi installer thật. Hai lớp F05 nay có phép đo tách riêng.
- `git show 9385ad2` và `git show 51ae5c0`: commit thứ nhất đúng 13 thêm/3 bỏ chỉ trong test; thứ hai 10 thêm chỉ handoff. Không thay sản phẩm sau sửa F05.

### Hướng 8: ratchet — KHÔNG PHẢI LỖI
`python3 evidence/ratchets.py`: trích NGUYÊN hai hàm `_c291_docs_ngoai_goi`/`_c357_agents_ngoai_goi` bằng AST từ bản sao ngoài cây, chạy với release helper và manifest HEAD thật. Baseline OK/OK; đổi riêng r291 về187 → FAIL/OK; đổi riêng r357 → OK/FAIL; 6/6 kết quả đúng kỳ vọng (`evidence/ratchets.log`). Không coi phép đo trích hàm này thay cho full selftest; full head đã chạy 1729/1731, hai fail r226/r268 đang đối chiếu nền.

### Hướng 9: Python hàm kế thừa — LỖI
`PYTHONDONTWRITEBYTECODE=1 PIP_NO_INDEX=1 python3 evidence/guard_probes.py python_function` (output `evidence/python-functions-ab.log`): trên đúng script HEAD, 4/4 ca hàm python ủy quyền bằng `command python` bị rc2 (2 nền × đơn/batch), dù Python ban đầu có yaml, rg tốt, venv ứng viên thiếu yaml. Cùng fixture không hàm hoặc hàm gọi Python tuyệt đối: 8/8 đạt. Trên bản sao chỉ thay phép giải executable bằng `type -P`: 12/12 đạt. Đây là phản chứng cho lời “ghim thành đường dẫn tuyệt đối”, không phải lỗi allexport/dấu cũ.

### f03-exported-python-function-reselects  [P1]  Hàm Python kế thừa khiến dòng ghim vẫn giữ tên trần
TEP/DONG: `ops/cai_cong_cu.sh:29` (chọn tên tại 20–23); khẳng định liên quan `changelog.d/wp-831.md:14` và `ops/handoff/wp831-g1-claude.md:21`.

VAN DE: F03 tái mở theo đường hàm interpreter kế thừa; không phải tái mở F04 đối với dấu biến shell thông thường. Bash nhận hàm python được export từ shell cha. Với hàm ủy quyền thông thường `python() { command python "$@"; }`, `command -v python` trả `python`, không trả đường dẫn executable. Vì vậy PY[0] vẫn là tên trần. Trong công thức rg, PATH ứng viên được prepend rồi hàm gọi `command python` vào venv thiếu PyYAML; rg tốt bị loại, wrapper rc2/GITHUB_PATH rỗng. Việc gọi độc lập vẫn tái chọn interpreter theo PATH, trái mục ghim của r3/N7 và lời tuyên bố trong diff. Không cần dấu giả hay credential; đầu vào là hàm shell kế thừa hợp lệ. Các phép thử r831 gỡ BASH_FUNC_* khỏi môi trường nên hiện không thấy đường này.

DA THU NGHIEM: ma trận A/B 24 lần gọi ở `evidence/python-functions-ab.log`: HEAD thường 8/8 đạt, hàm ủy quyền 0/4; bản sao với giải executable 12/12. Hai nền là công thức Linux/macOS chạy trong Bash Linux với installer giả, không tuyên bố đo macOS native. Có ca test gợi ý ở `HINT.patch`; chỉ là TEST, áp -p0 từ gốc cây. Bản sao hồi quy được chạy bởi `python3 evidence/function_regression.py`.

DO TIN: cao về tái hiện và cơ chế. Mức P1 theo phân loại của prompt (sai hành vi đo được), không suy rằng mọi máy có hàm python. Ảnh hưởng chỉ khi tên interpreter được giải thành hàm ủy quyền theo PATH.

GOI Y VA: sửa tại khối chọn/ghim của `ops/cai_cong_cu.sh`, vì chính nơi ấy hứa chọn một executable ổn định trước khi công thức đổi PATH. Phân biệt hàm/alias với đường executable và bảo đảm phần tử đầu thật sự là đường ổn định, giữ mảng và `py -3`; hoặc từ chối rõ loại đầu vào không hỗ trợ trước khi cài. Không đưa workaround vào YAML. Ca khóa: hàm python kế thừa + venv ứng viên thiếu yaml, cả đơn/batch và hai công thức phải DAT; đổi lại phép ghim cũ phải làm đúng ca mới đỏ. Nguy cơ của hướng chỉ chọn executable là bỏ qua wrapper shell được người dùng cố ý chọn; cần chốt chính sách rõ và đo python3/py -3, đường có dấu cách/tương đối. `type -P` trong bản sao chỉ là phép chứng minh nguyên nhân, chưa phải bản vá sản phẩm hoàn chỉnh.

HINT.patch: “chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”. Không có hunk sản phẩm trong hint.

### Hướng 10: tách lỗi môi trường — KHÔNG PHẢI LỖI của packet
- Full launcher HEAD: 214/226 đã chạy qua, tổng236, BO QUA10, HỎNG12, rc1. `ls -ld /tmp/.git` xác nhận thư mục rỗng bảo vệ có thật. Chạy lại đúng 12 ca đỏ trên clone nền `6b641ca...` rồi HEAD → 12/12 cùng lỗi/lớp ngoại lệ, source AST các ca không đổi. Các ca dừng trước materializer/probe có lỗi `Codex home is inside a repository`; KHÔNG ĐO ĐƯỢC nghiệp vụ credential trong sandbox này. Không dùng chúng làm finding; không nhầm t86 ở đây với nợ chạy song song chỉ dựa vào tên ca. `evidence/launcher-environment.json`, `evidence/failing-cases-source-comparison.json`.
- Full selftest HEAD và nền (cùng clone/no-hardlinks, core.abbrev7, bytecode off): đều 1729/1731, chỉ r226/r268 FAIL, delta0. `git config --get commit.gpgsign` → true. `python3 evidence/git_environment.py` chạy NGUYÊN hai hàm này trong từng tiến trình riêng cho từng cây: signing=true → cả hai false, signing=false → cả hai true; 8/8 đúng mẫu (`evidence/git-environment.log`). Không sửa Git config thật. Đang chạy full HEAD với override cấu hình chỉ trong môi trường tiến trình để đo N/N.
- Full launcher mutation `python3 .claude/dev/launcher_test.py --dot-bien`: 277/277 đo được đạt, 4 không đo được, tổng281, rc0. Không đổi headline thành281/281. Log `evidence/launcher-mutation.log`.

Cập nhật selftest cô lập Git: `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false PYTHONDONTWRITEBYTECODE=1 PIP_NO_INDEX=1 python3 scripts/tl.py --selftest` → **1731/1731**, rc0. Không đổi config thật; `evidence/selftest-signing-off.log`.

Bổ sung chốt công thức: `python3 evidence/recipe_guards.py` → 6 baseline PASS, 6 mutant bị giết bằng chính TinHieuChotCa, không lỗi vô can. Hai nền × (`-f` với rg là THƯ MỤC, thứ tự khi cả hai rg đều tốt, bỏ ghi GITHUB_PATH khi bare hỏng). Tất cả chạy công thức đọc lại từ YAML bản sao; log `evidence/recipe-guards.log`. Không mở finding mới cho các khoảng trống mutation đã được chủ kho chốt ngoài phạm vi. Khởi tạo RG_DICH và guard cuối là lớp dư trong chuỗi điều kiện hiện tại; không dùng việc chúng sống dưới ca cũ để suy có lỗi hành vi.

Kiểm tra ranh giới cây: Ruff mặc định và phép import đối chiếu 12 ca đã phát sinh 5 tệp cache bị Git bỏ qua (`.ruff_cache` và một pyc của launcher_test), dù các suite chính đều đặt bytecode off. Tôi ghi metadata/băm ở `evidence/cache-sideeffects.json`, xác minh không được Git theo dõi và thời điểm khớp phép đo, rồi dọn đúng 5 tệp này. Sau dọn: `GIT_OPTIONAL_LOCKS=0 git -C cay-kho status --porcelain=v1 --untracked-files=all` rỗng; không còn hai thư mục cache. Không có tệp nguồn theo dõi nào bị sửa. Đây là tác dụng phụ của phép đo, không phải finding của PR; không che bằng trạng thái Git sạch.

Ca cong_cu t47 đo riêng với override Git signing=false → `['qua', null]`, rc0 (`evidence/t47-signing-off.log`); xác nhận raw skip stage={0} thuộc môi trường Git, tương tự r226/r268. Bán kính toàn bộ vẫn đang đo, chưa lấy tiến độ làm số pass.
