verdict: changes_requested
reviewed_sha: 5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456
spec_sha256: e4fd84e1f079d0ac4841a145d078473576af3a3e4e2f593e4f3e40c5de7200e0
Ket qua: 0 P0, 1 P1, 1 P2, 0 P3.

Review độc lập PR #823, packet wp802 r1/g1, trên exact HEAD đã merge được giao. Có hai finding: F1 chặn nhầm wrapper chạy được từ Bash; F2 lệnh đo handoff thiếu phạm vi. Các giới hạn Windows/mạng và bẫy `/tmp/.git` được tách khỏi finding.

Reviewer: Codex, họ GPT theo chỉ thị runtime; provider `openai_codex`, execution surface `codex_service`, transport `machine` qua công cụ shell. Không suy model từ tài khoản GitHub. Không có receipt hoặc model ID có chữ ký để tự xác thực model cụ thể. Executor Claude theo packet; không dùng lại context executor, không đọc nội dung verdict cũ.

Tree: `78773e6b62eea2c879ac3aa5948dca3d3db94a9a`; Python `3.13.16`, Linux x86_64; `core.abbrev=7`, kho không shallow. Base đối chiếu là `fb490a7c3fa2992c6f4635ed091dafa813df2fe7`. Chỉ đọc `cay-kho/`; không push, không gọi GitHub/Internet, không dùng credential thật. Fixture nhạy cảm có sẵn chỉ được chạy qua bộ test, không tự soạn payload mới.

Lệnh trong các bảng dưới chạy từ `cay-kho/`. Các script reviewer ở `../runs/a34aff65/review_evidence/`; lệnh thực tế được bọc bởi `run_offline.py` để bỏ biến secret kế thừa, chặn socket Internet cho toàn bộ cây tiến trình và không sinh bytecode. Khi cần tái chạy cùng điều kiện: `python3 ../runs/a34aff65/review_evidence/run_offline.py <ten-log-moi> <lenh>`. Log của wrapper ở thư mục evidence, ngoài cây được review.

## BANG NGHIEM THU

| Tiêu chí | Lệnh/phép đo đã chạy | Output thật | Đạt? |
|---|---|---|---|
| N1 rg đầu PATH hỏng, bản sau tốt | `python3 ../runs/a34aff65/review_evidence/doctor_probes.py`; full suite ca `r802_doctor_rg_tran_hong_la_BI_CHE` | `ORDER rg rc=12 co=True state=BI_CHE`; có hai đường dẫn/cách chữa; ca `qua`; hai mutant bỏ BI_CHE/bỏ thiếu đều chết assertion | ĐẠT ca yêu cầu; F1 là trường hợp shell khác bị bỏ sót |
| N2 chỉ bản tốt | Cùng driver; `r802_doctor_rg_chi_ban_tot_khong_BI_CHE` | `ONLY_GOOD 0 None True`; mutant luôn BI_CHE chết đúng assertion | ĐẠT |
| N3 git như rg | Cùng driver; `r802_doctor_git_tran_hong_la_BI_CHE` | `ORDER git rc=12 co=True state=BI_CHE`; bỏ git khỏi tập áp dụng chết đúng ca | ĐẠT |
| N4 bash ngoài phạm vi | Cùng driver; `r802_doctor_bash_ngoai_pham_vi_BI_CHE` | `ORDER bash rc=0 co=True state=None`; Python cũng rc=0; mutant áp mọi công cụ chết | ĐẠT |
| N5 Windows rg.exe 0 byte phải QUA | Full suite có ca N1; đọc `_wp802_rg_that` tại HEAD | Linux ca N1 `qua`; nhánh `write_bytes(b"" if LA_WINDOWS ...)` có trong mã, nhưng không có Windows thật | KHÔNG ĐO ĐƯỢC yêu cầu native Windows; không khai pass từ Linux |
| N6 đối chiếu ba bảng và PyYAML vắng phải đỏ | Full suite `r802_bang_cai_rg_khop_cong_cu_yaml`; `claim_inventory.py`; strict mutants launcher/hook | Ca `qua`; PyYAML vắng → `TinHieuChotCa KHONG DO DUOC: thieu PyYAML...`, không skip; đổi một bảng giết đúng ca | ĐẠT |
| N7 Linux apt giả thành công không chữa thì cargo phải được gọi | `python3 ../runs/a34aff65/review_evidence/hook_recipe_probes.py`; mutant `wp802_hook_co_thay_co_chay` | `HOOK_LINUX rc=0 calls=['APT-GET install -y -qq ripgrep', 'CARGO install ripgrep']`; mutant thiếu cargo bị assertion bắt | ĐẠT |
| N8 uname Windows, không installer, in đúng lệnh YAML | Cùng driver; `r802_hook_windows_khong_cai_in_dung_lenh` | MINGW/MSYS/CYGWIN tốt/hỏng đều `calls=['RG']`; bản hỏng in đúng lệnh, bản tốt stdout rỗng; các mutant rơi vào apt/probe hai lần bị bắt | ĐẠT phép mô phỏng được spec yêu cầu |
| N9 cai_cong_cu.sh rg xanh trên windows-latest | Driver công thức YAML thật trên Linux + installer/cygpath giả; `git diff abc16de 9b45585 -- ops/cong_cu.yaml` | Các ca hợp lệ `rc=0 DAT=true`; cả installer hỏng rc=1; không thư mục tốt rc=2; commit mutant đổi hai tên package thật sự tồn tại | KHÔNG ĐO ĐƯỢC job Windows 39101164840/39101166158 hoặc lượt exact HEAD |
| N10 Linux toàn suite N/N, dispatch Windows, mutation đúng assertion | `python3 .claude/dev/launcher_test.py --nhat-ky ../runs/a34aff65/review_evidence/launcher-cases.log`; `--dot-bien`; strict driver | `212/224`, tổng 234, skip 10, hỏng 12 (bẫy môi trường); 11/11 ca mới qua; `272/272` mutant, 4 không đo; 22/22 mutant mới xác minh riêng, 9/9 mutant bổ sung | KHÔNG ĐO ĐƯỢC toàn tiêu chí: Linux không N/N trong sandbox này; chưa đo Windows. Không quy 12 lỗi thành hồi quy |
| N11 cổng tĩnh | `python3 ../runs/a34aff65/review_evidence/static_gates.py` | Ruff F head=5/base=5/new=0; `bash -n` rc=0; `bash_nen.py quet` ĐẠT rc=0; `doctrine-scan` sạch rc=0; diff --check rc=0 | ĐẠT |
| N12 release-verify WORKER trên PR | Driver cổng tĩnh chạy `release-manifest --out` ngoài cây rồi `release-verify --strict --json` | rc=0, `errors=[]`, `package_hash_match=true`; changelog fragment hiện diện | ĐẠT mô phỏng cục bộ; KHÔNG ĐO ĐƯỢC trạng thái lane PR GitHub |
| Write set / trần được cho phép | `git diff --numstat fb490a7c3fa2992c6f4635ed091dafa813df2fe7 5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456` | 6 tệp; 482 thêm/22 xóa, khớp nguyên văn `diff.patch`/`numstat.txt` | ĐẠT theo chỉ thị riêng cho phép vượt trần; không mở lại quyết định |
| M1–M8 ngoài tên ca cụ thể | Hai driver doctor/hook, full suite, inventory, đọc changelog/handoff | M2–M7 có hành vi/bằng chứng tương ứng ở N1–N8; M1 có F1; M8 có F2 và phần lịch sử không đo được | M1/M8 CHƯA ĐẠT; phần còn lại như các dòng trên |

## BANG DO

Cách tìm lời khai: đọc trọn diff sáu tệp; `git diff --unified=0 BASE HEAD` lấy mọi dòng thêm; regex riêng cho SHA, số, tên ca; AST/decorator và các bảng mutation; đọc riêng comment, changelog, handoff. Driver `claim_inventory.py` ghi danh sách token vào `claim_tokens.json`. Danh sách tự lập không bảo đảm vét cạn mọi mệnh đề ngôn ngữ; bảng này nêu rõ cả điều đo được và điều bị giới hạn, không coi việc có token là bằng chứng đúng.

| Khẳng định | Diff khai | Đo được (lệnh/log) | Khớp? |
|---|---|---|---|
| Artifact và danh tính | HEAD/spec được giao | `git rev-parse HEAD`, `sha256sum ../SPEC.md`; static driver `PATCH_MATCH True`, `NUMSTAT_MATCH True` | Có |
| Phạm vi | Sáu đường dẫn, 482 dòng thêm | Numstat đúng base: 64+374+13+9+7+15=482; xóa22 | Có |
| rg/git trước bản sửa bỏ bản hỏng rồi xanh | Comment/changelog/handoff | `doctor_probes.py`: `LEGACY_BAD_FIRST rg/git 0 None`, chọn bản tốt; HEAD tương ứng12/BI_CHE | Có trong phạm vi probe cô lập |
| Bản tên trần giải theo PATH, mục rỗng=cwd, đo trước | Resolver/changelog/M1 | Full suite `r802_doctor_ten_tran_tu_muc_PATH_rong` qua; ba mutant bỏ mục rỗng/không đặt đầu/ghi đè bản hỏng chết đúng assertion | Có với các dạng đã thử |
| Khả năng chạy như shell | “the way the shell does”; bản tên trần hỏng | `doctor_probes_final.log`: cả rg/git `shell_rc=0`, `base_rc=0`, `head_rc=12`, ENOEXEC | KHÔNG, F1 |
| BI_CHE có trạng thái, hai bản, remedy, co=True, thiếu bắt buộc12 | Code/JSON/bản chữ/changelog | Driver doctor; strict mutations; extra mutations bỏ riêng từng trường/bản chữ/kết luận đều chết assertion | Có ở ca hỏng thật |
| Chỉ rg/git; loại bash/python | Q3/comment | Driver thật bốn công cụ: rg/git=12, bash/python=0; mutant áp mọi công cụ bị bắt | Có |
| Timeout hoặc không giải ra tên trần không phải BI_CHE | Handoff dòng5/comment | `TIMEOUT_NOT_BROKEN 0 None True`; `ABSENT 12 False None`; `extra_mutations.py` có đối chứng và mutant timeout | Có |
| PATHEXT mặc định, thứ tự CMD so shim, tên có đuôi vẫn nối | Resolver/native, comment “CPython 3.13” | Ca `r802_cac_duong_dan_chi_trong_PATH_va_theo_PATHEXT` qua; bốn mutant tương ứng chết; đọc `inspect.getsource(shutil.which)` trên Python3.13.16, mặc định `.COM;.EXE;.BAT;.CMD;.VBS;.JS;.WS;.MSC` | Khớp thuật toán đã đối chiếu/mô phỏng; CreateProcess Windows thật chưa đo |
| Tên ca, 0 byte, qua trên Windows | N1/N5/docstring helper | Mã ghi bytes rỗng khi LA_WINDOWS, ca không tự return skip; thực chạy Linux không đi nhánh Windows | Chỉ xác nhận cấu trúc; chưa xác nhận native pass |
| Ba bảng lệnh Windows/Linux khớp | CONG_CU/hook/YAML | N6 qua; lệnh Windows trong stdout hook đủ ba cờ accept-source/accept-package/disable-interactivity và fallback choco | Có; không mở lại công thức Linux/macOS đã chốt |
| Launcher không thêm phụ thuộc YAML runtime | Q5 | `launcher.py` không có import yaml; YAML được đọc trong helper test; driver vắng PyYAML đỏ đúng ca | Có |
| Hook Windows không cài rg, probe đúng một lần | Hook/comments/handoff | Sáu ca MINGW/MSYS/CYGWIN tốt/hỏng: một `RG`, không installer; mutant probe hai lần cho `RG1,RG2,APT-GET,...` và đỏ đúng assertion | Có cho khối rg; không suy toàn hook không chạy installer khác |
| Linux dùng co_chay trước cargo | Hook/M3 | Apt giả thành công không sửa rg vẫn gọi `CARGO install ripgrep`; đổi về co giết ca | Có |
| WinGet Links → choco/bin → command-v; checker thật quyết định | YAML/comment/M2/M5 | Ca mới chạy công thức thật với phiên bản hợp lệ/rỗng/rác/stderr/header; driver thêm installer thất bại/thư mục có khoảng trắng | Có trong mô phỏng Linux; không xác minh CLI Windows thật |
| GITHUB_PATH truyền thư mục đã chọn; vắng vẫn chạy | YAML/changelog | Driver ghi đúng Links hoặc choco; `no-github-path rc=0 DAT=true`; mutant bỏ ghi bị assertion bắt | Có trong mô phỏng; đổi đường dẫn cygpath Windows chưa đo |
| 11 r802; 22 wp802 =13 launcher+4 hook+3 YAML+2 harness | Handoff M6 | `claim_inventory.py`: `COUNTS r802=11 product=13 hook=4 yaml=3 harness=2`; tổng suite mutant 276 | Có |
| t106 giữ fallback/thứ tự, đổi BI_CHE/12; bốn neo cũ cập nhật | Handoff/M6 | Full suite t106 qua; inventory chỉ ra bốn entry doctor_luon_xanh/bo_qua_auth/chi_thu_binary_dau/text_gop_CHUA_DO; suite mutation qua | Có |
| Hook/YAML chỉ TinHieuChotCa mới được tính giết | Comment/bảng runner mới | Đọc catch mới tách Exception; strict log có đúng assertion ca đích cho cả7; lỗi thiếu launcher của giàn reviewer được loại, sửa rồi kiểm lại | Có cho 22 mutant mới; không dùng headline để khẳng định mọi mutant cũ không có tín dụng giả |
| Spec hash tại lease và HEAD | Handoff f6159dc4, e4fd84e1…00e0 | `git show <sha>:ops/specs/wp802.md` rồi SHA256, tại cả HEAD và f6159dc4 đều đúng hash đầy đủ | Có |
| Các SHA lịch sử tồn tại | f6159dc4/db1ed4d/509dfa8/a0de1f9/3d65c95/db56075/9b45585/abc16de/de82ef74/fb490a7 | `claim_inventory.py` dùng `git show -s --format=%H`; ghi đủ OID ở log | Có về object; không đọc lại verdict ở db56075 |
| N9 có mutant làm hỏng công thức | 9b45585, đối chứng abc16de | `git diff abc16de 9b45585 -- ops/cong_cu.yaml` đúng đổi hai package sang tên không tồn tại; abc16de là tổ tiên HEAD, 9b45585 không phải tổ tiên | Có về nội dung Git, chưa đo kết quả workflow |
| Lệnh de82ef74 cho 482/6 | Handoff dòng11 | `scope_probe.log`: không lọc→28 tệp/1107 thêm/32 xóa; lọc write set→ 6/482/22; base review→ 6/482/22 | Thiếu điều kiện phạm vi, F2 |
| Preflight success, lease độc quyền6/6, ref596↔596 | Handoff dòng3; runs39092181024/39092090057 | Ref bundle hiện có 658; object lease và spec tồn tại; không có snapshot ls-remote lịch sử được tự đo | KHÔNG ĐO ĐƯỢC phép so máy chủ và trạng thái job; 658 không bác lời khai lịch sử596 |
| CI Windows/15.2.0 và trạng thái exact HEAD | YAML39093706610; handoff39101164840/39101166158/39095054115; PR comment | Không gọi mạng, không có runner Windows hoặc log server được đo trực tiếp | KHÔNG ĐO ĐƯỢC; không dùng làm pass |
| F1–F6 của các lượt cũ, ngân sách +1, comment6246303988/6247229964 | Handoff dòng9/11 | Chỉ kiểm object commit và hiệu ứng code hiện tại; không đọc verdict cũ hoặc gọi GitHub | KHÔNG ĐO ĐƯỢC lịch sử; quyền vượt trần đã có trong chỉ thị lượt này |
| Windows t23/t49/t217, 251/252, delta0; PowerShell5.1 không nhận toán tử OR | Handoff dòng14/15 | Không có môi trường Windows/PowerShell5.1; hai lỗi Windows và manifest/docs đã được chủ kho xử lý theo prompt | KHÔNG ĐO ĐƯỢC; không mở finding mới |

## BANG TEST

| Bộ/lệnh thực thi | N/M thật | Bỏ qua / không đo | Mã thoát |
|---|---|---|---|
| `python3 .claude/dev/launcher_test.py --nhat-ky ../runs/a34aff65/review_evidence/launcher-cases.log` | 212/224 đã chạy qua; tổng 234, hỏng 12; đủ 234 cặp vào/ra | 10 BO QUA (liệt kê dưới); 12 lỗi bị chặn bởi môi trường home/repository | 1 |
| 11 ca mới r802 trong chính lượt trên | 11/11 | 0 | Từng ca `qua` |
| `python3 ops/cong_cu_test.py` mặc định | 55/55 đã chạy qua; tổng 56 | 1 ca t47; tiền kiểm 0; vòng bán kính 470 chưa hoàn tất | Ngắt 130 ở vòng bán kính, không khai rc=0 |
| `CONG_CU_TEST_BAN_KINH=manh python3 ops/cong_cu_test.py` | cong_cu_test: 55/55 đạt; tổng=56, bỏ qua=1, tiền kiểm bỏ qua=0 | Bán kính giao mảnh theo chế độ gate; chi tiết cuối bên dưới | 0 |
| `python3 .claude/dev/launcher_test.py --dot-bien` | 272/272 đo được; tổng 276 | 4 không đo được, liệt kê dưới | 0 |
| `strict_mutations.py` + `strict_mutations.py --harness-only` | 22/22 mutant mới, 25 assertion ca đích được xác minh | Lượt giàn đầu thiếu launcher.py ở 2 mutant harness: loại tín dụng, sau sửa giàn → 2/2 assertion đúng | Lượt đầu1 do giàn reviewer; lượt harness sửa0 |
| `extra_mutations.py` | 9/9 mutant bổ sung bị giết; hai ca trung tính qua | 0 | 0 |
| `doctor_probes.py` | Các ca PATH/scope/timeout/bản chữ đúng; phản chứng F1 tái lập cho cả rg/git | Bộ đo xác nhận tuple lỗi F1, rc=0 của script không có nghĩa sản phẩm hết lỗi | 0 |
| `hook_recipe_probes.py` | 6 ca hook Windows mô phỏng +1 Linux +6 công thức YAML | Không thực thi installer hay Windows thật | 0 |
| Static/release WORKER cục bộ | Ruff F delta0; bash syntax/scan, doctrine, diff-check, manifest/verify đều đạt | Ruff mỗi cây rc=1 vì cùng 5 lỗi nền | Driver0 |

Kết luận gate công cụ cuối: `SỐ LIỆU: ca=56 · đột biến=470 (giao mảnh) · lỗi đột biến=0 · tiền kiểm bỏ qua=0 · cổng cây thật=ĐẠT`. Các ca bỏ qua/không đo không được cộng vào tử số hoặc dùng làm bằng chứng xanh đầy đủ.

10 ca BO QUA của launcher:

1. `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125`: fixture native Windows; POSIX có t63.
2. `r345_chan_socket_that_ma_than_hook_van_chay_dung`.
3. `r345_cac_phep_do_cuc_bo_van_dung`.
4. `r345_lop_tham_import_van_co_rang`.
5. `r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO`.
6. `r347_tham_import_van_song_tren_python_truoc_310`.
7. `r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO`.
8. `r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia`.
9. `r348_dot_bien_bo_isidentifier_lam_ca_dich_DO`.
10. `r484_g4_windows_sid_alias_identity`: native Windows SID.

Các mục2–9 cùng lý do `KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)`. Không cài gói qua mạng để đổi kết quả.

12 ca lỗi launcher thuộc t86/r484 home/materializer, tên cụ thể trong `launcher.log` và `launcher-cases.log`. `/tmp/.git` hiện diện từ preflight; nhiều ca báo nguyên văn `OSError: Codex home is inside a repository`. Blob `.claude/dev/codex_cred.py` ở base và HEAD giống nhau: `61d826dc0b253194c15dec3632aadc9df7f95a02`. Vì bẫy đã được chỉ thị nêu trước, ghi KHÔNG ĐO ĐƯỢC các hậu điều credential trong sandbox, không phát sinh finding hồi quy từ 12 ca này; cũng không tự đổi chúng thành pass.

4 mutant launcher không đo được: `g4_windows_sid_alias_not_normalized`, `g4_windows_LA_not_current_owner` (native SID), `g2_windows_directory_pin_access` (native share-delete pin), `124_khi_chau_con_song` (ca đích t62 tự bỏ qua).

## BANG SAN

Nhật ký được ghi tăng dần ngay từ đầu; giữ lại dưới đây với chín hướng độc lập, lệnh và output thật. Các phần từng ghi “đang chạy” là thời điểm ghi nhật ký; bảng test phía trên là trạng thái chốt cuối.


- `sha256sum SPEC.md` → `e4fd84e1f079d0ac4841a145d078473576af3a3e4e2f593e4f3e40c5de7200e0`.
- `git -C cay-kho rev-parse HEAD` → `5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456`; `status --short` rỗng, `core.abbrev=7`, `--is-shallow-repository=false`.
- `ls -ld /tmp/.git` → `dr-xr-xr-x … /tmp/.git`; đã ghi nhận bẫy Codex home. Không xóa/sửa thư mục đó.
- Chỉ thị riêng của lượt review cho phép 482 dòng thêm, 6 tệp; không coi vượt 450 dòng là finding. Các quyết định packet #831 và Windows t23/t49/t217 cũng không mở lại.

### Hướng 1 — neo phiên bản và phạm vi (KHÔNG PHẢI LỖI)

`git -C cay-kho diff --numstat fb490a7c3fa2992c6f4635ed091dafa813df2fe7 5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456` → lần lượt `64/7`, `374/11`, `13/3`, `9/0`, `7/1`, `15/0`: tổng 482 thêm, 22 xóa, đúng 6 đường dẫn trong spec. `git rev-parse HEAD^{tree}` → `78773e6b62eea2c879ac3aa5948dca3d3db94a9a`.

Ba lệnh test đã được khởi chạy; output và rc ghi ở `runs/a34aff65/review_evidence/`. Wrapper `run_offline.py` chặn tạo socket IPv4/IPv6/packet bằng seccomp cho cả cây tiến trình, bỏ biến credential kế thừa và đặt `PYTHONDONTWRITEBYTECODE=1`. Không đổi HOME, không chạy hook toàn phần khôi phục xác thực. `unshare -n true` → rc=1, `Operation not permitted`; vì vậy dùng seccomp thay cho network namespace.

### Hướng 2 — doctor qua PATH thật và đối chứng (KHÔNG PHẢI LỖI ở ca danh định)

Lệnh: `python3 runs/a34aff65/review_evidence/run_offline.py doctor_probes python3 ../runs/a34aff65/review_evidence/doctor_probes.py` (cwd wrapper là thư mục review; subprocess chạy trong `cay-kho/`). Output thật: `ORDER rg rc=12 co=True state=BI_CHE`, `ORDER git rc=12 co=True state=BI_CHE`, `ORDER bash rc=0 state=None`, `ORDER python rc=0 state=None`; `ONLY_GOOD 0 None True`; `ABSENT 12 False None`; `NONEXEC_SKIPPED 0 None`; `DEDUP` có đúng 2 ứng viên; `TIMEOUT_NOT_BROKEN 0 None True`. Bản chữ in đủ bản hỏng, bản tốt, `TRUOC trong PATH`, và kết luận `THIEU rg (BI_CHE: co cai, ban ten tran hong)`. Log: `runs/a34aff65/review_evidence/doctor_probes.log`.

### Hướng 3 — ngữ nghĩa gọi từ shell (LỖI, F1 tạm xếp P1)

Cũng lệnh trên, hai dòng `TEXT_WRAPPER rg` và `TEXT_WRAPPER git`: Bash thực chạy tên trần `shell_rc=0` và in phiên bản; base `fb490a7…` có `base_rc=0`; HEAD có `head_rc=12`, `head_state=BI_CHE`, lý do `[Errno 8] Exec format error`. Fixture là script chữ vô hại có quyền thực thi, không có shebang; Bash tự thực thi dạng script khi exec trả ENOEXEC. Đã đo bằng tiến trình `/bin/bash --noprofile --norc` thật, PATH thật và probe sản phẩm thật; chỉ cô lập bảng công cụ/module/năng lực để lỗi không lẫn với môi trường. Không phải bẫy `/tmp/.git`.

### Hướng 4 — hook Windows/Linux (KHÔNG PHẢI LỖI trong phép mô phỏng)

Lệnh: `python3 runs/a34aff65/review_evidence/run_offline.py hook_recipe_probes python3 ../runs/a34aff65/review_evidence/hook_recipe_probes.py` → rc=0. Mỗi `MINGW64_NT-10.0`, `MSYS_NT-10.0`, `CYGWIN_NT-10.0`, cả `rg` tốt/hỏng: `calls=[RG]`, rc=0; bản hỏng in đúng công thức Windows, bản tốt stdout rỗng. Linux: `calls=[APT-GET install -y -qq ripgrep, CARGO install ripgrep]`, chứng minh apt giả thành công không làm mất fallback cargo. Chạy riêng khối rg lấy từ hook tại HEAD; mọi installer đều stub, không chạy phần credential. Log `hook_recipe_probes.log`.

### Hướng 5 — công thức YAML và truyền PATH giữa bước (KHÔNG PHẢI LỖI trong phép mô phỏng)

Cũng lệnh trên, chạy nguyên `cai_cong_cu.sh rg` với công thức YAML thật và installer giả, mọi đường dẫn fixture có dấu cách: `winget-links rc=0 installers=[WINGET] DAT=true`, `winget-fails-choco rc=0 installers=[WINGET,CHOCO] DAT=true`; `both-installers-fail rc=1`, `no-valid-folder rc=2`; `empty-version rc=0` chọn choco, không nhận bản rỗng; `no-github-path rc=0 DAT=true` không cần GITHUB_PATH. Khi có GITHUB_PATH, nội dung đúng thư mục được chọn. Đây là Bash Linux mô phỏng nền Windows, không phải kết quả CreateProcess/winget/cygpath Windows thật.

### Hướng 6 — cổng tĩnh và lane WORKER cục bộ (KHÔNG PHẢI LỖI)

Lệnh: `python3 runs/a34aff65/review_evidence/run_offline.py static_gates python3 ../runs/a34aff65/review_evidence/static_gates.py`. Output thật: `RUFF_F head=5 base=5 new=0 delta={}` (ruff riêng từng cây rc=1 vì cùng 5 lỗi có sẵn); `bash_syntax rc=0`; `bash_scan rc=0 DAT: không có lời gọi trần mới`; `doctrine rc=0 sạch — đã quét 10 tệp, 0 chỗ chép doctrine`; `diff_check rc=0`; `release_manifest rc=0`; `release_verify rc=0 errors=[] package_hash_match=true`; `PATCH_MATCH True`, `NUMSTAT_MATCH True`. Bản nền ruff là đúng base `fb490a7…`, không lấy master hiện nay. Manifest tạm ở ngoài cây. Đây không chứng minh job GitHub N12 đã xanh.

### Hướng 7 — đột biến với phân loại assertion chặt (KHÔNG PHẢI LỖI ở 22 đột biến mới)

`python3 .claude/dev/launcher_test.py --dot-bien` qua wrapper → rc=0, `DOT BIEN: 272/272 dat (4 khong do duoc tren nen nay)`. Bộ chấm độc lập `strict_mutations.py` xác nhận 20 mutant launcher/hook/YAML mới đều chết bằng `TinHieuChotCa`, có message và stack của ca đích trong `strict_mutations.log`. Hai mutant harness lúc đầu không đo được vì giàn reviewer thiếu bản sao launcher.py (FileNotFoundError, không cấp tín dụng giết). Đã sửa riêng giàn reviewer và chạy `strict_mutations.py --harness-only`: rc=0, `STRICT_MUTATIONS 2 mutants; failures=0`, cả hai có `ASSERTION r802_runner_tra_lai_con_tro_nguoi_goi ... bang:161`. Không sửa cây thật. Bốn mutant ngoài nền được ghi riêng khi tổng hợp.

### Hướng 8 — chạy hết launcher và tách bẫy môi trường (KHÔNG ĐO ĐƯỢC N10 đầy đủ)

`python3 .claude/dev/launcher_test.py --nhat-ky ../runs/a34aff65/review_evidence/launcher-cases.log` qua wrapper → rc=1 sau 410,70 giây: `212/224 ca DA CHAY QUA (tong 234, bo qua 10, hong 12)`. Nhật ký `# XONG TRON VEN`, đủ 234 cặp vào/ra. Các lỗi thuộc t86/r484 credential/home/materializer; lỗi trực tiếp có `OSError: Codex home is inside a repository`, khớp `/tmp/.git` đã tồn tại trước lượt đo. KHÔNG coi đây là hồi quy wp802. Các ca BO QUA được liệt kê riêng ở bảng test cuối.

Cả 11 ca mới r802 đều `qua` trong lượt đầy đủ:
```
<<< ra  216 r802_doctor_rg_tran_hong_la_BI_CHE -> qua
<<< ra  217 r802_doctor_rg_chi_ban_tot_khong_BI_CHE -> qua
<<< ra  218 r802_doctor_git_tran_hong_la_BI_CHE -> qua
<<< ra  219 r802_doctor_bash_ngoai_pham_vi_BI_CHE -> qua
<<< ra  220 r802_doctor_ten_tran_tu_muc_PATH_rong -> qua
<<< ra  221 r802_cai_rg_windows_chon_ban_chay_duoc -> qua
<<< ra  222 r802_cac_duong_dan_chi_trong_PATH_va_theo_PATHEXT -> qua
<<< ra  223 r802_runner_tra_lai_con_tro_nguoi_goi -> qua
<<< ra  224 r802_bang_cai_rg_khop_cong_cu_yaml -> qua
<<< ra  225 r802_hook_linux_rg_hong_van_thu_cargo -> qua
<<< ra  226 r802_hook_windows_khong_cai_in_dung_lenh -> qua
```

### Hướng 9 — kiểm lời khai, SHA, số đếm (LỖI P2 ở lệnh đo thiếu phạm vi; phần còn lại nêu giới hạn)

`claim_inventory.py` qua wrapper rc=0: `COUNTS r802=11 product=13 hook=4 yaml=3 harness=2`, `MUTATION_TOTAL 276`; cả spec trong HEAD và f6159dc4 băm đúng `e4fd84e1…00e0`; mọi SHA được nhắc trong handoff đều giải ra commit thật. Đã mô phỏng vắng PyYAML: `TinHieuChotCa KHONG DO DUOC: thieu PyYAML de doc ops/cong_cu.yaml`, không BO QUA. Không đọc verdict cũ; với SHA review chỉ xem metadata commit. Ref hiện có 658, không đủ để kiểm lời khai lịch sử 596↔596 ở máy chủ. Không có mạng nên các run GitHub, comment quyết định, số 15.2.0 lịch sử và 251/252 Windows không đo lại được; không suy pass.

Phép đếm lệnh ở handoff dòng 11 cho output thật:
```
handoff-command: files=28 added=1107 deleted=32 rc=0
handoff-with-write-set: files=6 added=482 deleted=22 rc=0
review-base: files=6 added=482 deleted=22 rc=0
```
Cặp 482/6 đúng với diff review, nhưng lệnh nguyên văn `git diff --numstat de82ef74` thiếu bộ lọc write set (hoặc sai base nếu dùng để tái lập diff hiện tại). Đây là thiếu điều kiện của bằng chứng, không phải mở lại quyền vượt trần đã được chủ kho chốt.

Bổ sung 9 đột biến do reviewer tự lập (chỉ trên bản sao tạm): `extra_mutations.py` → rc=0, `EXTRA_MUTATIONS 9 failures=0`; các chốt top-level state, nested detail, co=True, hai đường dẫn, cách chữa, bản chữ, kết luận chữ và timeout đều chết bằng assertion đúng ca. Hai đối chứng độc lập `summary_contract`, `timeout_contract` đều `NEUTRAL_PASS`.

### Cập nhật suite công cụ

Lượt mặc định `python3 ops/cong_cu_test.py` đã kết thúc toàn bộ 56 ca đăng ký: `cong_cu_test: 55/55 đạt; tổng=56, bỏ qua=1, tiền kiểm bỏ qua=0`, `CỔNG TRÊN CÂY THẬT: ĐẠT`, tự kiểm phân hạng/giàn giáo/song song đều đạt. Ca bỏ qua: `t47_INDEX_phai_duoc_doc_TRUNG_THUC_va_nguon_py_nhan_du_moi_cach_viet`, không dựng được INDEX chưa hòa giải (`stage={0}`). Sau đó lệnh mặc định tự chạy bán kính 470 đột biến (4 tiến trình), ngoài write set. Đã ngắt phần bán kính bằng Ctrl-C, tool trả exit_code=130; KHÔNG khai toàn lệnh mặc định rc=0 hoặc 470/470.

Đang chạy lại chính suite ở chế độ gate mà code hỗ trợ: `CONG_CU_TEST_BAN_KINH=manh python3 ops/cong_cu_test.py` (không phải chế độ mảnh; dòng cuối chương trình ghi bán kính giao mảnh). Giữ output riêng `cong_cu_gate.log`.

### Chốt lượt gate công cụ

`CONG_CU_TEST_BAN_KINH=manh PYTHONUNBUFFERED=1 python3 ops/cong_cu_test.py` qua wrapper hoàn tất sau 451,80 giây, rc=0: `cong_cu_test: 55/55 đạt; tổng=56, bỏ qua=1, tiền kiểm bỏ qua=0`; `TỰ KIỂM SONG SONG (N126): ĐẠT`; `SỐ LIỆU: ca=56 · đột biến=470 (giao mảnh) · lỗi đột biến=0 · tiền kiểm bỏ qua=0 · cổng cây thật=ĐẠT`. Số 470 là giao mảnh, không phải 470 mutant đã chạy. Log `cong_cu_gate.log`, rc trong `cong_cu_gate.rc`.

QA cuối: đủ N1–N12, chín hướng săn, 11 link evidence tồn tại; HEAD và spec không đổi; `git status --porcelain`, diff worktree và diff index đều rỗng.


### F1-shell-enoexec [P1] Không gán BI_CHE cho wrapper Bash vẫn thực thi được

TEP/DONG: `.claude/dev/launcher.py:4431` (ghi `hong_dau` từ lỗi probe native), nhánh mới tại 4435 và điều kiện thiếu bắt buộc 4517; liên quan probe `_phien_ban` tại 2344 và changelog dòng1–4.

VAN DE: Bản tên trần được chọn đúng nhưng phép đo chạy bằng `subprocess.run([duong_dan, '--version'])`, không có ENOEXEC fallback của Bash. Một wrapper chữ executable không có shebang vẫn chạy bình thường khi agent gõ `rg --version` hoặc `git --version` trong Bash. Probe native trả errno8; nhánh mới coi đó là bản shell hỏng, tìm bản dự phòng rồi gán BI_CHE và chặn rc=12. Base cũ rc=0. Đây là hồi quy chặn sai trên POSIX, không cần Windows hay credential, và không phải ca `/tmp/.git`.

DA THU NGHIEM: `python3 ../runs/a34aff65/review_evidence/doctor_probes.py` qua wrapper. Log `doctor_probes_final.log` ghi cho cả rg/git: `shell_rc=0`, shell stdout có đúng đường dẫn wrapper và phiên bản; `base_rc=0`; `head_rc=12`, `head_state='BI_CHE'`, `loi='[Errno 8] Exec format error'`. Mọi tệp và PATH fixture là thật, Bash và `_phien_ban` thật; chỉ cô lập CONG_CU/MODULE_PY/KHA_NANG và nguồn env để không lẫn lỗi khác. Script cố ý assert tuple lỗi nhằm tái lập finding, không phải test xác nhận sản phẩm đạt.

DO TIN: Cao về kết quả Linux và delta base→HEAD; không suy hành vi Windows từ phép đo này.

Gợi ý vá: tại đường probe bản tên trần của `lenh_doctor`, đo theo cùng semantics Bash mà agent dùng; hoặc xử lý ENOEXEC của script POSIX qua một shell đã xác định là dùng được trước khi kết luận `hong_dau`. Giữ argv/đường dẫn cố định, stdin và ngân sách timeout hiện có. Ca khóa cần cả rg/git: wrapper executable không shebang in phiên bản, rc=0, có backup tốt ⇒ không BI_CHE, doctor=0; đối chứng wrapper exit1 ⇒ BI_CHE/12. Đột biến bỏ fallback phải làm chính assertion đối chứng dương đỏ. Nguy cơ của vá: đổi cách chạy có thể kéo script/native Windows vào sai interpreter, thay hạn giờ hoặc làm mất phân biệt timeout với hỏng; nên giới hạn đúng đường POSIX/ENOEXEC và giữ các đối chứng hỏng thật, timeout, N1–N4.

### F2-handoff-scope [P2] Lệnh numstat cần khai rõ bộ lọc write set hoặc đúng base review

TEP/DONG: `ops/handoff/wp802-g1-claude.md:11`.

VAN DE: Dòng này gắn cặp `482 dòng thêm / 6 tệp` với lệnh nguyên văn `git diff --numstat de82ef74`. Tại exact reviewed_sha, lệnh đó bao gồm thay đổi master đã merge vào nhánh và cho 28 tệp/1107 dòng thêm/32 xóa. Cặp 482/6 đúng cho write set hoặc base review fb490a7; điều kiện lọc ấy đang thiếu trong lời khai. Đây là P2 thiếu phạm vi của phép đo; không tranh lại quyết định cho phép 482 dòng hoặc kết luận write set PR vượt 6 tệp.

DA THU NGHIEM: `git diff --numstat de82ef74 5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456` → 28/1107/32; thêm `-- .claude/dev/launcher.py .claude/dev/launcher_test.py .claude/hooks/session-start.sh changelog.d/wp-802.md ops/cong_cu.yaml ops/handoff/wp802-g1-claude.md` → 6/482/22; dùng base `fb490a7c3fa2992c6f4635ed091dafa813df2fe7` không lọc → 6/482/22. Output thực lưu `scope_probe.log`.

DO TIN: Cao, ba lệnh Git cục bộ cùng exact HEAD, không phụ thuộc mạng hoặc runner.

Gợi ý vá: sửa dòng11 thành lệnh có đủ hai OID `git diff --numstat fb490a7c3fa2992c6f4635ed091dafa813df2fe7 5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456`, hoặc khai rõ lọc sáu đường dẫn nếu muốn giữ base de82ef74. Ca khóa là tính tổng ba cột từ output lệnh được ghi và đòi 6/482/22. Khi cập nhật bằng chứng về sau, phải ghim lại base/head của phép đo để không biến số đúng cho write set thành lời khai cho toàn lịch sử nhánh. Không cung cấp HINT.patch vì F1 cần executor chọn cách probe shell; hướng vá cụ thể cho cả hai finding đã nêu ở đây.

Các bằng chứng chính: [doctor](runs/a34aff65/review_evidence/doctor_probes_final.log), [scope](runs/a34aff65/review_evidence/scope_probe.log), [launcher](runs/a34aff65/review_evidence/launcher.log), [công cụ gate](runs/a34aff65/review_evidence/cong_cu_gate.log), [đột biến](runs/a34aff65/review_evidence/mutations.log), [đột biến strict](runs/a34aff65/review_evidence/strict_mutations.log), [harness strict](runs/a34aff65/review_evidence/strict_harness.log), [đột biến bổ sung](runs/a34aff65/review_evidence/extra_mutations.log), [hook/công thức](runs/a34aff65/review_evidence/hook_recipe_probes.log), [cổng tĩnh](runs/a34aff65/review_evidence/static_gates.log), [inventory](runs/a34aff65/review_evidence/claim_inventory.log).
