verdict: approve
reviewed_sha: 7f8be85a7cf9077400fc1747aa6e23128f087677
spec_sha256: 2fb1b2633ae09e4b737f97d601186389fd801cc294a5217ea07b3e761c3bf13b
Ket qua: 0 P0, 0 P1, 0 P2, 0 P3.

PR ducthangho/tra-luat#1097, packet #1078 r1, lease `wp1078-r1-g2-claude`, sensitive, Codex lượt 3/3 theo chỉ thị nâng trần trong prompt.snapshot. Không dùng trần 2 cũ trong SPEC để tự hủy lượt đã được chủ kho cho phép.

Reviewer: Codex, provider `openai_codex`, execution_surface `codex_service`, transport `machine` (công cụ shell trong sandbox; không phải review Web do người chép). Không có attestation từng response để chứng thực model/effort/session identity: KHONG DO DUOC; không tự tạo receipt/required check hay quyền land. Không dùng context executor.

HEAD tree `148cc49af9ebcb347f6b527a0fb7379ec80e6355`; base thật `90c101b8d1f8895b66607de8582a18c5e72d834c`. `sha256sum SPEC.md` khớp hash dòng 3. `git diff BASE HEAD` byte-match `diff.patch`, diff `0311db4..HEAD` byte-match `diff-tu-luot2.patch`; 2 tệp, +113/-12 (test +103/-5, shell +10/-7), trong write set, không sửa runtime khác. Spec soạn tại `086f1b7`; shell ở hai base 086f1b7 và 90c101b có cùng SHA-256 `16b43f985ba5c22e5ad1cd938e5ef9f8f4236f72963a0ca854b8b1b4b42709ad`.

Môi trường đo: Linux, Bash 5.2.21, Python 3.13.16; HEAD và clone base đều có `core.abbrev=7` trước lượt offline dùng để kết luận. `/tmp/.git` tồn tại và rỗng (`ls -d /tmp/.git`; `ls -la /tmp/.git`), không xóa/sửa để làm suite xanh. Không dùng Web/GitHub hoặc credential thật, không sửa `cay-kho/`. Bản base và mutant đều ngoài cây được review. Có `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0` cho các suite.

Phát hiện trong khi đo: fixture cũ `_r345_venv` gọi `pip install pypdf==3.17.4` mà không tự đặt no-index. Lượt suite đầu chưa ép no-index, nên không dùng lượt ấy làm bằng chứng tuân thủ offline; khác biệt skip ở nhóm r345 có thể phụ thuộc cache/khả năng cài gói. Đã chạy lại launcher HEAD/base và mutation với `PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1`; bảng kết luận cuối lấy lượt offline này. Các gói không có cục bộ được ghi KHONG DO DUOC, không tải thêm để làm xanh. Không khẳng định lượt đầu không hề thử kết nối chỉ vì sandbox chặn mạng.

Công cụ environment_status không có trong tập tools phiên này; không suy môi trường hoặc credential ready từ sự vắng mặt đó.

Các lệnh có thể chạy lại từ `cay-kho/` (đặt `PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1` khi chạy suite đầy đủ):

- F: `PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/focused.py` — 6 ca HEAD, test HEAD trên hai shell base, 4 mutation wp1078, mutation kết hợp và lời gọi hàm thừa; chỉ `TinHieuChotCa` tính là giết. `focused.json`/`.log` ghi từng case và thông điệp.
- P: `python3 ../evidence/probes.py` — Bash thật, từng tình huống độc lập; ghi `probes.json`/`.log`. Phép đo bộ chọn dùng nguyên 32 dòng đầu shell HEAD trong bản sao tạm rồi in `declare -p PY`; không lấy kết quả bộ chọn cô lập làm bằng chứng installer đã DAT. Hàng `full-CDPATH-checker-reached` dùng nguyên script và checker giả.
- H: `PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/history.py` — mã test lấy bằng `git show` từ commit cũ, nạp dưới đường dẫn fixture HEAD để giữ dữ liệu phụ thuộc; không checkout/sửa HEAD. Kiểm cơ chế hỏng ở 882cb50 và chạy CLI ca reuse HEAD trong 3 môi trường cha.
- O: `PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/original_hint.py` — lấy đúng các dòng thêm từ `HINT-review-832.patch`, chạy hai hàm HINT nguyên gốc trên HEAD và cả hai base.
- L: `PIP_NO_INDEX=1 PYTHONDONTWRITEBYTECODE=1 python3 ../evidence/legacy_mutant.py` — mục mutation cũ còn sống, kiểm neutral/mutant ở cả HEAD và base; lưu `legacy-mutant.json`.
- G: đọc `../evidence/gates.json`, `ruff-{head,base}.stdout`, `*-{head,base}.stderr` cho rc/stdout/stderr các gate; lệnh cụ thể ở bảng dưới.

Mọi script đo đọc đường dẫn theo `__file__` nên cũng chạy được từ thư mục chứa VERDICT. Wrapper `evidence/run_suite.py` lưu lệnh, rc, thời gian và trạng thái timeout riêng trong JSON, log đầy đủ ra tệp. Có thể chạy trực tiếp những lệnh suite dưới đây tại HEAD; base là clone local ngoài `cay-kho/`, checkout đúng OID, không dùng archive thiếu `.git` làm baseline.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding nguồn | Trạng thái ở HEAD | Bằng chứng tự đo | Lỗ mới? |
|---|---|---|---|
| F01-no-function-invocation-assertion, P2 lượt 1 | ĐÃ VÁ THẬT | F: HEAD 3 ca hàm PASS; `extra-function-call-all` làm cả 3 đỏ bởi `ham python ke thua da bi goi`; mutation native `wp1078_goi_ham_python_thua` giết 1/1 ca M3. | Không thấy. Nhật ký do chính hàm tạo; `not ham_log.exists()` đủ khóa mọi lời gọi trong fixture. |
| F02-reused-py-guard-unmeasured, P2 lượt 1; lỗi fixture export ở lượt 2 | ĐÃ VÁ THẬT | F: reuse PASS 4 chế độ × 2 giá trị. H: CLI HEAD clean/allexport/marker-export đều `1/1 qua, 0 bo qua, 0 hong`, rc0. Mutant `wp1078_chot_chi_nhanh_chon_moi` đỏ đúng assertion của ca; bỏ riêng `declare +x` trong BẢN SAO TEST đỏ tại nhãn `bash-a`, rc3 thay vì4. | Không tái hiện lỗi mới. Dòng 9865 gán rồi bỏ export trước `source`, đúng thứ tự cần thiết dưới allexport. |

Không đổi ID hoặc chia biểu hiện để xóa lịch sử F02. Lượt này đã tự đo bản sửa, không chỉ nhận kết luận của executor hoặc verdict cũ.

## BANG NGHIEM THU

| Tiêu chí | Lệnh | Output thật / giới hạn | Đạt? |
|---|---|---|---|
| M1: `type -P`, thứ tự python → python3 → py -3, giữ args | P (`order-python`, `order-python3`, `order-py-minus3`), F ca r886; `sed -n '19,32p' ops/cai_cong_cu.sh` | `declare -a PY=([0]="<san>/all/python")`; lần lượt thiếu tên trước thì `.../py3/python3`, `.../py/py [1]="-3"`; đều rc0. Hàm export cho cả 3 tên bị bỏ qua. | ĐẠT trên Bash Linux; Git Bash/py.exe native KHONG DO DUOC. |
| M2: không tuyệt đối phải rc4, stderr một dòng, cả nhánh chọn mới/reuse | P PATH rỗng/tương đối và reuse; F ca reuse nguyên script | `python`, `./python`, `rel/python` đều rc4 và một dòng `PY[0] khong phai duong dan tuyet doi`; stdout rỗng. Reuse absolute giữ `-3` ở cả 3 chế độ kế thừa. | ĐẠT cho các đường của spec đã đo. |
| M3: 2 HINT + hàm echo không phải Python không được gọi | F + O | HEAD 3/3 ca hành vi PASS; HINT nguyên gốc 2/2 PASS. Gọi hàm thừa làm cả 3 assertion đỏ đúng thông điệp nhật ký. | ĐẠT; `macos` là giả nền công thức trên Linux, không phải máy macOS. |
| M4: chọn command-v; bỏ M2; kết hợp; đúng ca | F; `python3 .claude/dev/launcher_test.py --dot-bien` | 4 mutation wp1078 riêng giết 7/7 lượt ca đích; kết hợp command-v + bỏ guard giết 4/4, trong đó M3 rc0 nhưng GITHUB_PATH rỗng nên assertion đỏ. Bỏ riêng guard giết shape bằng `thieu chot PY[0] tuyet doi`. | ĐẠT tập mới; kết hợp có phép đo riêng, không khai là một mục riêng trong bảng native. |
| A1: launcher Linux, delta môi trường 0, mutation mới đúng đích | `PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1 python3 .claude/dev/launcher_test.py --nhat-ky ../evidence/launcher-offline-head.journal`; tương ứng trên clone base; cùng env với `--dot-bien` | Offline HEAD 307/320 ca đã chạy qua; tổng 330, skip 10, đỏ 13; rc1, 375.572s. Base 302/315 ca đã chạy qua; tổng 325, skip 10, đỏ 13; rc1, 374.935s. Cùng 13 ca đỏ và cùng 10 skip, 0 ca đỏ mới. Mutation offline 521/522 đạt, 4 KHONG DO DUOC, rc1; 4 mục wp1078 đều đạt. | ĐẠT delta 0 của các ca đo được và mọi mutation mới. Toàn suite không xanh: các phần bị môi trường chặn KHONG DO DUOC, không tính skip là pass. |
| A2: HINT đỏ trên spec-base 086f1b7 | O và F | O hai HINT đều ASSERT trên 086 và 90: rc1/GITHUB_PATH rỗng. HEAD đều PASS. F xác nhận thêm M3 và shape đỏ trên cả 2 base. | ĐẠT. |
| A3: cong_cu không đổi so base; cài rg rc0 | `python3 ops/cong_cu_test.py` trên hai vế; `bash ops/cai_cong_cu.sh rg` trên hai vế | Phần ca thường mỗi vế 60/60, tổng61/skip1, delta0. HEAD N126 ĐẠT; base N126 và toàn bộ bán kính490 KHONG DO DUOC (giới hạn600s/180s, SIGINT rc=-2). Cài rg HEAD/base đều rc1, cùng `sudo: PERM_SUDOERS: setresuid(-1, 1, -1): Invalid argument`, chưa tới apt-get. | Kết quả cài rc0 KHONG DO DUOC do sandbox, không gán thành regression PR. |
| A4: Ruff F delta 0, whitespace, doctrine, bash-n, CI/Windows | `python3 -m ruff check --no-cache --select F --output-format json .claude/dev/launcher_test.py scripts/tl.py`; `git diff --check 90c101b8d1f8895b66607de8582a18c5e72d834c HEAD`; `python3 .claude/dev/packet_loop.py doctrine-scan --root .`; `bash -n ops/cai_cong_cu.sh` | Ruff 17/17 cảnh báo cũ (test 5 F841, tl.py 12 F821), cùng thông điệp, delta 0; rc1 cả 2 vế. Diff rc0, doctrine rc0 (`10 tệp, 0 chỗ`), bash-n rc0. | Các gate cục bộ đạt theo delta. CI PR và workflow_dispatch windows-only KHONG DO DUOC: cấm mạng, không runner/receipt native trong bundle. Không coi là xanh hoặc miễn gate. |

## BANG DO

Cách tìm khẳng định: đọc TOÀN BỘ `diff.patch` và diff Git từ BASE tới HEAD, HINT và hai verdict cũ; bản có thêm ngữ cảnh được lưu ở `evidence/diff-context40.patch`; đọc `git log --format=%B BASE..HEAD` (lưu `evidence/commit-messages.txt`). Kiểm từng dòng mới, comment/docstring và commit body, không dùng danh sách từ khóa làm trần review. Bảng nhóm các phát biểu cùng phép đo; số dòng neo HEAD.

| Khẳng định | Diff khai / nơi neo | Đo được bằng lệnh | Khớp? |
|---|---|---|---|
| Bỏ hàm/alias/builtin; giữ thứ tự 3 tên và đối số py | Shell 21–25; commit 882cb50 M1 | P: 3 thứ tự, hàm export mỗi tên, alias off/on, builtin; F: r886 | Khớp hợp đồng dùng `type -P`. Không phải xác thực nội dung file hoặc chống startup code/hash tùy ý. |
| command-v nhận hàm, in tên trần; ghim cũ không ngăn đổi interpreter | Shell 21–22; test 9790–9791; commit 882cb50 | P: `command-v=python type-P=<san>/all/python`; O/F: HEAD qua, base đỏ, GITHUB_PATH rỗng | Khớp cơ chế. Issue/log #832 bên ngoài KHONG DO DUOC offline; không giả đã mở nguồn ấy. |
| Chốt absolute áp dụng cả nhánh reuse, giữ đối số mảng | Shell 29–32; commit 882cb50 M2 | P: bare/relative/PATH rỗng, reuse absolute; F: nguyên script | Khớp. Guard sau cả hai nhánh. Không hứa khóa inode hoặc nội dung symlink. |
| Fixture chép đúng shell đang thử, nhìn thấy mutant | Test 9641; commit 47b873 | F: command-v giết 3 ca hành vi, rc4; H: mã test 882cb50 trước sửa khiến cả 3 ca vẫn PASS với cùng mutant, chỉ shape đỏ | Khớp; có phản chứng cơ chế 1/4 cũ. Không sửa tệp thật. |
| Nhận hai HINT và thêm ca hàm echo | Test 9792–9831; commit 882cb50 M3 | Đọc `HINT-review-832.patch`; O/F | Khớp nội dung: HINT nguyên gốc 2/2 PASS tại HEAD, 2/2 đỏ trên mỗi base; ca echo bổ sung M3. Đường `ops/specs/wp1078.md` ghi trong comment không có trong Git HEAD (cat-file rc128); nguồn authority để review là SPEC.md đóng băng ở ngoài kho theo prompt, không giả đã đọc file đó ở HEAD. |
| Hàm không bao giờ được gọi; nhật ký phát hiện mỗi lần | Test 9798–9815, 9830; commit 0311db4 F01 | F: `extra-function-call-all`, 3/3 ASSERT `ham python ke thua da bi goi` | Khớp. `finally` phục hồi seam môi trường; chốt không chỉ dựa vào DAT/rc0. |
| Ca hình dạng dùng được trên Windows, khóa fail-close4 | Test 9835–9843 | F: shape PASS; command-v/bỏ guard đều shape ASSERT; đọc ca thuần Python, không gọi Bash | Khớp cấu trúc có thể chạy trên Windows. Thực thi Windows KHONG DO DUOC; ca hành vi POSIX có skip rõ. |
| Reuse đúng nhánh cha, checker chặn installer; chịu allexport/marker export | Test 9847–9872; commit 0311db4 và 7f8be85 | F: 8 tình huống PASS; H: 3 outer env PASS; bỏ `declare +x` đỏ tại `bash-a`; native fresh-only đỏ | Khớp bản 7f8be85. Checker `SystemExit(23)` chặn trước installer. F02 ở 0311db4 đã đóng. |
| r886 đối chiếu tập, tên, thứ tự, args với TEN_PYTHON | Test 10209–10215; commit 47b873 | F: r886 PASS; P: py giữ -3; H: ca r886 ở 882cb50 ASSERT `sh=[]` | Khớp. Regex mới không xanh nhờ tập rỗng. |
| M4: command-v, bỏ guard, kết hợp; thêm mutation F01/F02 | Bảng 13749–13762; commit 882cb50/0311db4 | F/native: 4 mục wp1078 giết 7/7 lượt ca; F: kết hợp 4/4 đỏ | Khớp. Native có 4 mục; kết hợp là phản chứng riêng/base, không khai có mục thứ 5. |
| Base90 cả 4 ca đỏ; M3 có rc0 mà gp rỗng | Commit 882cb50 A2 | F: mỗi base 4/4 ASSERT; O: hai HINT trên mỗi base ASSERT | Khớp lượt đo này. Không nâng rc0 của hàm echo thành bất biến mọi môi trường. |
| Lịch sử 326/327 và 519/520 trên 882cb50; sau 47b873 ba ca đỏ rc4 | Commit 47b873 body | H: r886 hỏng, mutant chỉ giết shape; F: mutant làm ba ca hành vi đỏ rc4 | Cơ chế khớp. Hai tổng lịch sử KHONG DO DUOC trên đúng rig gốc; không dùng tổng hiện tại để kết tội số lịch sử. |
| Lượt1 có 2P2, lượt2 có 1P2 fixture; áp HINT từ hai lượt | Commit 0311db4 và 7f8be85 | Đọc hai verdict cũ; `git diff 47b873a 0311db4`; `git diff 0311db4 HEAD`; F/H | Khớp số finding, nội dung fix; diff lượt2 byte-match. Không dùng số finding để suy suite xanh. |
| Ca reuse qua ba điều kiện kế thừa; fresh-only chết bởi assertion | Commit 7f8be85 đoạn Đo | H: 3 CLI, mỗi `1/1 qua`, rc0; F: fresh-only ASSERT của chính ca reuse | Khớp. Mỗi CLI tự kiểm 4 chế độ × 2 giá trị, không chỉ tình huống outer. |
| Attribution/session trong commit trailer | `Co-Authored-By`, `Claude-Session` ở 4 commit | `git log --format=%B BASE..HEAD` | Có metadata đúng trong Git; danh tính model, người hoặc nội dung session từ URL KHONG DO DUOC offline. Không dùng trailer làm attestation. |

## BANG TEST

| Bộ | N/M / rc | Bỏ qua / giới hạn |
|---|---|---|
| Launcher HEAD | 307/320 ca đã chạy qua; tổng 330, skip 10, đỏ 13; rc1, 375.572s | 10 skip: 2 nền Windows và 8 fixture venv/pip không có gói offline; cùng base. |
| Launcher base90 | 302/315 ca đã chạy qua; tổng 325, skip 10, đỏ 13; rc1, 374.935s | Cùng sandbox, clone local thật ngoài kho. |
| Launcher mutation HEAD | 521/522 đạt, tổng 526, rc1, 328.342s; wp1078 4/4 mục đạt | 4 mục KHONG DO DUOC; xem các dòng native/ca đích skip trong mutation-offline-head.log. Mục SAI duy nhất sống cả trên base (L). Không chạy toàn bộ mutation base; chỉ đo riêng mục sống. |
| Tập mới F / O | F HEAD 6/6 PASS; O HEAD 2/2 PASS; F mỗi base 4/4 ASSERT, O mỗi base 2/2 ASSERT | Không skip, không ERROR. Test mới chạy trên shell cũ, không gọi là toàn suite base. |
| Native wp1078 theo F | 4 mục đạt, 7/7 lượt ca ASSERT | command-v 4/4; gọi hàm thừa 1/1; fresh-only 1/1; bỏ guard 1/1. |
| Mutation thêm F | Kết hợp 4/4 ASSERT; gọi hàm thừa 3/3 ASSERT; bỏ `declare +x` trong fixture 1/1 ASSERT | Mọi mutant ở bản sao ngoài kho; không nhận ngoại lệ vô can làm tín dụng. |
| H / CLI kế thừa | clean/allexport/marker-export: mỗi `1/1 qua, 0 skip, 0 hỏng`, rc0 | Ca reuse tự kiểm 8 nhánh. |
| cong_cu HEAD/base | Mỗi vế 60/60 ca đã chạy qua, tổng61, skip1; HEAD N126 ĐẠT; cả hai tiến trình rc=-2 do timeout có chủ đích | 1 skip INDEX ở cả hai vế. HEAD bị SIGINT ở 600s khi đang bán kính 490; base ở 180s khi chưa xong N126. Phần 490 và N126 base KHONG DO DUOC; không gọi cả suite xanh. |
| Ruff/diff/doctrine/bash-n | Ruff 17/17, delta 0; ba gate sau rc0 | Không khai Ruff tuyệt đối 0. |
| Cài rg thật | HEAD/base cùng rc1 | Lỗi sudo sandbox, rc0 KHONG DO DUOC, không tới installer mạng. |
| CI, Windows native, macOS native | KHONG DO DUOC | Không mạng/runner/receipt. Không coi nền giả hoặc skip là pass native. |

Các lỗi môi trường được đối chiếu theo tên ca, không chỉ theo tổng. `summary.json` ghi `new_failures=[]`, `lost_failures=[]`. Hai ca `r858_goc_tam_tranh_to_tien_co_git` và `t86_...` bị `/var/tmp` read-only; 11 ca r484 liên quan chốt “Codex home is inside a repository” hoặc bị chặn trước bước materializer. `/tmp/.git` rỗng có mặt ở cả hai vế. Không dùng credential thật để vượt chốt. Tập 13 ca đỏ chung:

- `r484_g2_child_khong_nhan_snapshot_va_rac_chan_truoc_probe`
- `r484_g2_doctor_doc_dung_home_da_materialize`
- `r484_g2_hook_shell_scrub_truoc_probe`
- `r484_g2_probe_isolated_marker_va_refresh`
- `r484_g2_recovery_probe_rollback_va_snapshot_moi`
- `r484_g2_schema_truoc_freshness_va_home_materialize`
- `r484_g2_storage_kernel_guardrails`
- `r484_g7_auth_doi_truoc_khi_thay_thi_giu_ban_moi`
- `r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do`
- `r484_g7_tu_choi_ghi_dung_ban_da_probe`
- `r484_g8_hook_scrub_kin_voi_bash_env`
- `r858_goc_tam_tranh_to_tien_co_git`
- `t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac`

Cùng 10 ca skip ở hai lượt offline (skip KHÔNG phải pass):

- `r345_cac_phep_do_cuc_bo_van_dung`
- `r345_chan_socket_that_ma_than_hook_van_chay_dung`
- `r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO`
- `r345_lop_tham_import_van_co_rang`
- `r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO`
- `r347_tham_import_van_song_tren_python_truoc_310`
- `r348_dot_bien_bo_isidentifier_lam_ca_dich_DO`
- `r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia`
- `r484_g4_windows_sid_alias_identity`
- `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125`

Tám fixture venv/pip bị skip dùng định nghĩa giống hệt HEAD/base (`legacy-fixture-equality.json`, 10 định nghĩa helper/ca bằng nhau); không quy skip này cho PR. Lượt đầu chưa ép offline có HEAD315/328 (2 skip), base302/315 (10 skip), cùng13đỏ; không dùng chênh lệch ấy làm kết luận delta cho phần chưa đo. Lượt ép offline mới là A/B chính.

Mutation cũ `r26_rv5_codex_env_guard` sống ở cả HEAD và base; L có cả neutral và mutant đều PASS, không ERROR. Không tuyên bố toàn mutation base đã được chạy. Bốn mục wp1078 trong CLI offline:

```text
wp1078_chon_bang_command_v   OK  giet 4/4: r831_cai_rg_linux_python_ham_ke_thua, r831_cai_rg_macos_python_ham_ke_thua, r1078_ham_python_khong_phai_python_khong_duoc_goi, r1078_hinh_dang_chon_python_bang_type_P
wp1078_goi_ham_python_thua   OK  giet 1/1: r1078_ham_python_khong_phai_python_khong_duoc_goi
wp1078_chot_chi_nhanh_chon_moi OK  giet 1/1: r1078_py_dung_lai_khong_tuyet_doi_phai_thoat_4
wp1078_bo_chot_tuyet_doi     OK  giet 1/1: r1078_hinh_dang_chon_python_bang_type_P
```


## BANG SAN

Mỗi hàng là một hướng độc lập. P/F/H/O ở trên dùng Bash/subprocess thật. `<san>` chỉ thay đường dẫn thư mục tạm có suffix ngẫu nhiên; log/JSON giữ đường dẫn đầy đủ. Không coi bộ chọn cô lập là đã chạy installer.

| Hướng | Lệnh / tình huống | Output thật | Phân loại |
|---|---|---|---|
| Hàm export làm đổi interpreter sau prepend PATH | P `exported-function`; F/O HEAD và base | `command-v=python type-P=<san>/all/python`; HEAD 3 ca PASS; base HINT rc1/gp rỗng | KHONG PHAI LOI còn mở. |
| Hàm không phải Python bị gọi thừa ngoài checker | F `extra-function-call-all` | Cả 3 ASSERT `ham python ke thua da bi goi` | KHONG PHAI LOI; F01 đã vá. |
| Hàm export ở fallback python3/py; không có file | P `exported-python3-function`, `exported-py-function`, `function-only-no-file` | Chọn `.../python3` hoặc `.../py` với -3, rc0; không file: rc4 `khong tim thay python, python3 hay py`, không `FUNCTION_CALLED` | KHONG PHAI LOI; fallback cũng bỏ hàm. |
| Alias trong script không tương tác | P `alias-noninteractive`, `alias-expand-explicit` | `expand_aliases off`, chọn file. Bật rõ ràng thì có `python is aliased to...` nhưng type-P/PY vẫn là file, rc0, không `ALIAS_CALLED` | KHONG PHAI LOI. Đã kiểm alias mặc định không kích hoạt. |
| Builtin | P `builtin-class` | `builtin`; `command-v=printf type-P=<san>/all/printf`; python/python3/py đều `not a shell builtin` | KHONG PHAI LOI với builtin chuẩn. Builtin tự nạp tên Python KHONG DO DUOC/ngoài phạm vi. |
| py -3 / Windows-Git Bash | P `order-py-minus3`; F r886 | `declare -a PY=([0]="<san>/py/py" [1]="-3")`, rc0; r886 PASS | KHONG PHAI LOI về thứ tự/args trên Linux; py.exe/Git Bash native KHONG DO DUOC. |
| Reuse array cha absolute/bare/relative | P `reuse-absolute/reuse-bare/reuse-relative`; F fresh-only | Absolute giữ -3 rc0; bare/relative rc4, một dòng stderr; mutant fresh-only ASSERT rc3 | KHONG PHAI LOI; F02 đã có ca hành vi đủ sức giết. |
| Marker export, PY vô hướng, exec giữ PID | P `exported-marker-array`, `scalar-matching-marker`, `exec-exported-marker-scalar` | Đều chọn lại file PATH, không giữ `/bin/echo`; exec in `declare -ax PY=([0]="<san>/all/python")`, rc0 | KHONG PHAI LOI; không dùng PID đơn độc để tin môi trường. |
| bash -a, SHELLOPTS, marker cha export | P: 9 hàng reuse; F/H | Absolute + args rc0; bare/relative rc4; H: 3 outer env PASS; bỏ `declare +x` trong fixture ASSERT tại `bash-a` | KHONG PHAI LOI; đã đo lại đúng biểu hiện lượt2. |
| PATH có phần tử rỗng/tương đối/dot | P `PATH-empty/PATH-relative/PATH-dot` | rc4; stderr lần lượt `'./python'`, `'rel/python'`, `'./python'`; stdout rỗng | KHONG PHAI LOI: M2 cố ý fail-close, không canonical hóa hoặc thử tiếp tên khác. |
| Hash table Bash bị ghi tường minh | P `hash-absolute`: `hash -p /bin/echo python; type -P python` | `/bin/echo`; PY[0]=`/bin/echo`, rc0 ở prefix | NGOÀI PHẠM VI, KHONG PHAI LOI của diff. `type -P` theo spec vẫn đọc hash; không khai đường này đã bị chặn. |
| BASH_ENV | P `BASH_ENV-automatic/BASH_ENV-explicit` | Automatic in `STARTUP_READ`, chọn `/bin/echo`; source tường minh in marker hai lần | NGOÀI PHẠM VI, KHONG PHAI LOI của diff: startup code có thể sửa hash/chạy code. Lượt này kích hoạt tự động đo được; không kéo lại kết quả khác ở môi trường lượt2. |
| CDPATH / lấy gốc kho | P `CDPATH/full-CDPATH-checker-reached` | Prefix rc0, không có stdout do CDPATH; nguyên script rc3 từ checker23: `'rg' khong co cong thuc cai tu dong...` | KHONG PHAI LOI: cd đến absolute path không bị CDPATH làm bẩn kết quả; không chạy installer. |
| File tên Python không chứa Python / symlink có thể đổi | P: prefix với symlink tới `/usr/bin/true`; đọc 32 dòng bộ chọn | Nhận file absolute, rc0; không xác minh magic/import | NGOÀI PHẠM VI: spec chọn file theo tên và chặn nonabsolute, không xác thực code/inode. Không khai đã chống TOCTOU/symlink mutable. |
| Harness hoặc môi trường tạo tín dụng giả | F phân biệt ASSERT/ERROR; suites HEAD/base; `ls -d /tmp/.git` | Các mutant wp1078 không ERROR; empty git marker hiện diện; offline hai vế cùng 13 ca đỏ, cùng 10 skip; L neutral/mutant cả hai vế đều PASS | KHONG DO DUOC các hành vi bị chặn; không có regression do diff qua tập ca chạy được. |

## Finding còn mở

Không còn finding mở: 0 P0, 0 P1, 0 P2, 0 P3. F01 và F02 đã vá thật; không phát hiện lỗi mới trong toàn diff qua các phép đo nêu trên. Không soạn patch runtime/gate của packet sensitive.

`HINT.patch` rỗng (0 byte): không còn finding cần gợi ý sửa. Không có patch áp vào `cay-kho/`. Các mutant riêng chỉ là dữ liệu đo ngoài kho, không phải patch sản phẩm.

Ngưỡng nội dung áp cho review sensitive của lượt này: không còn P0/P1/P2; không có P3 cần chấp nhận nợ. Kết luận nội dung: approve exact SHA ở dòng 2. Đây không phải lời khai mọi gate đã xanh hoặc quyền merge/land: CI PR, Windows native, cài rg thật và phần suite dài chưa hoàn tất vẫn thiếu bằng chứng như đã khai. Bên có runner/authority cần kiểm các gate ấy trên đúng SHA trước khi land; không tự mở thêm lượt Codex quá trần3/3.

Kiểm cuối: HEAD không đổi; `git status --porcelain=v1` rỗng; cả hai tệp review byte-match blob HEAD. Không sửa `cay-kho/`, không push, không tạo approval trên dịch vụ ngoài. Evidence và verdict ở ngoài cây. Các lệnh kiểm tra, kết quả dương/đỏ/skip/not-run đã tách riêng trong các bảng; không lấy rc0 hoặc N/N phần đầu làm pass cho cả suite.
