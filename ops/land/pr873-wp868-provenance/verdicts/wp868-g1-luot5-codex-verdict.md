verdict: approve
reviewed_head: f07f88c75cabbef691c86ac8746317a6c0705162
reviewed_sha: f07f88c75cabbef691c86ac8746317a6c0705162
reviewed_tree: 694e9b94c9625fee6df6322b40bc70c80169b7e7
review_class: sensitive
provider: openai_codex
model: gpt-6.1-sol
model_family: openai
reasoning_effort: xhigh
execution_surface: codex_cli
transport: machine
review_round: 5/5

## Kết luận

**approve trên exact head ở header. F868-02 ĐÓNG; không còn finding P0/P1/P2/P3 mở trong phạm vi bản vá đã đo.** F868-01/03/04/05/06 vẫn đóng, không phát hiện lỗi mới của packet. Đối chiếu lượt 4 đã hoàn tất trước khi săn mới. Không còn yêu cầu sửa sản phẩm hoặc test theo các finding đã báo.

Đây là kết luận review nội dung, không xác nhận đủ điều kiện merge/land/deploy. Launcher đầy đủ còn 13 lỗi môi trường và 10 skip giống hệt nền ở cả hai chế độ auth; **không ghi chúng thành N/N xanh**. CI và Windows thật chưa xác minh do chỉ thị cấm mạng/GitHub. Không suy M-2/M-3 hoặc trạng thái lifecycle `cross_approved` từ verdict này.

## Neo và môi trường

- Base/merge-base `origin/master`: `9e9a74b2a396ef458d25c51a5563efafbb45ba0c`; base tree `9fc05c9986f711d1961e040dc7345850d0133294`. Head/tree đúng header; `core.abbrev=7` repo-local ở cả hai nguồn. Hai cây sạch đầu và cuối; băm nội dung toàn bộ tracked files được đối chiếu lại, không đổi. [Audit thật](out/evidence/scope-audit.json).
- Spec SHA-256 tự đo `0d950c2b98b9e024bf1cc43a77c5d3351b5f4c21e6307b2e36ba9cdeca7b3f69`; verdict lượt 4 `bf0dd45fa0d29e8d9a63c9897914113c5481070c97488a61201db13d2712d5d5`; `prompt.snapshot` bằng byte với `PROMPT.md`. [Spec](out/evidence/spec.md), [lease](out/evidence/lease.yaml), [lượt 4](out/verdict-luot4.md). Đã đọc lịch sử lượt 1–3, #858 lượt 4–5 và [handoff Q4](out/evidence/handoff.md).
- Lease offline generation 1, sensitive, executor Claude, reviewer OpenAI, hết hạn `2026-10-24T06:52:00Z`. Không suy heartbeat/authority live từ bản sao lease. Ngưỡng áp dụng trong lượt này: không để lại P0/P1/P2/P3 mở.
- Run `684d95a7b1164a41bbfb5c7ddd499f13`, CLI `0.163.0`, header công bố model/effort như trên. Đây là bằng chứng cấu hình CLI; không tự chứng thực model backend từng request. [Header cục bộ](out/evidence/model-header.txt).
- Linux x86_64; Bash 5.2.21, Python 3.13.16, Git 2.43.0, Ruff 0.16.9, actionlint thật 1.7.7. `/tmp/.git` là mount rỗng read-only mode555; sandbox không cho ghi `/var/tmp`. Không tháo mount hay xoá marker để làm xanh ca. [Môi trường](out/evidence/runtime.txt).
- `PYTHONDONTWRITEBYTECODE=1 python3 -B out/review.py setup` dựng head, base, base-cross **trong một lệnh** bằng bản sao thường, không hardlink; base-cross là nền + `launcher_test.py` của head. Chỉ chạy trong `out/`; không sửa `cay-kho/`/`nen/`, không viết patch sản phẩm, không gọi mạng/GitHub. Env chung `PYTHONDONTWRITEBYTECODE=1`, `PIP_NO_INDEX=1`, `PIP_DISABLE_PIP_VERSION_CHECK=1`, TMPDIR riêng từng job dưới `out/tmp/`; gỡ auth thật trước child, auth giả là `review-fixture-not-a-credential`. Commit signing được tắt ở command scope. Core.abbrev cuối cùng dùng repo-local, xem lỗi driver được sửa ở bảng cổng.
- Theo `CLAUDE.md` mục Quy trình sửa code §5, agent read-only `tl_auditor` đọc các log dài và kiểm độc lập delta; agent không sửa tệp hoặc chạy gate. Reviewer chính kiểm kết quả và viết verdict. [Tiến độ đã lưu trước kết luận](out/VERDICT-progress.md).

## Đối chiếu lượt 4 và bảng finding

Lệnh đã chạy **trước săn mới**: `PYTHONDONTWRITEBYTECODE=1 python3 -B out/review.py prior`. [Log](out/prior-r5.log), [phép thay và từng kết quả](out/evidence/prior-r5.json).

Mutant nguyên văn `clear-exit-trap-after-recipe` thêm `trap - EXIT` ngay sau `( set +e; eval "$LENH" ) > "$TAM_CAI/stdout"`. Control: cả ba ca reader/cleanup/shape PASS. Mutant: ca reader ném **TinHieuChotCa** với output `kenh 'loi': thu muc kenh con sau khi thoat: rc=7 con=['cai_cong_cu.kqqeJE']`; ca shape ném **TinHieuChotCa** `trap EXIT don kenh phai la DUY NHAT, khong bi go/ghi de`. Ca installer-failure vẫn pass trên mutant, đúng lý do finding lượt 4 đã mở.

Sau đó đo riêng **cả hai** nhánh, không để assertion nhánh đọc-lỗi che nhánh payload-rác: `python3 -B out/hunts.py exits`. Control: read-error rc7/tmp_left=[], BAD_CHANNEL rc7/tmp_left=[]; mutant: cùng rc7 nhưng mỗi nhánh còn một thư mục, witness cleanup đều **TinHieuChotCa**. Cat giả ghi đường kênh thật và fault xảy ra sau khi installer đã thành công. [Witness độc lập](out/evidence/hunt-exits.json).

| ID / mức / slug ổn định | Trạng thái, vị trí | Bằng chứng mới và hướng xử lý bằng lời |
|---|---|---|
| F868-01 / P2 / `stdout-installer-bi-nhan-lam-ket-qua-chon` | **ĐÓNG**, reader `ops/cai_cong_cu.sh:136`; test `.claude/dev/launcher_test.py:8840` | Head lỗi cat rc7, không DAT; mutant reader `&&`→`;` bị ca hành vi và shape giết bằng TinHieuChotCa. Giữ lỗi đọc tách khỏi kênh rỗng/fallback; không cần sửa thêm. |
| F868-02 / P2 / `fixture-khong-khoa-don-kenh-khi-thoat-loi` | **ĐÓNG thật ở lượt 5**, `.claude/dev/launcher_test.py:8853`, `:8969`, `:11276`; runtime trap `ops/cai_cong_cu.sh:126` | Mutant lượt 4 bị ca reader mới và shape giết thật; hai witness độc lập xác nhận cả exit7. Các nhánh installer-error, success và batch vẫn sạch. Giữ TMPDIR riêng, bằng chứng kênh từng tồn tại và mutant sau eval; không cần vá runtime. |
| F868-03 / P3 / `fixture-fallback-khong-khoa-crlf` | **ĐÓNG**, `.claude/dev/launcher_test.py:8830` | Fallback LF/CRLF head/nền DAT; bỏ cắt CR bị ca hành vi và shape giết. Giữ cắt CR ở biên dòng cuối, không strip toàn đường. |
| F868-04 / P2 / `fixture-khong-khoa-loi-ghi-payload-kenh` | **ĐÓNG**, `.claude/dev/launcher_test.py:8876` | Hai mutant nuốt lỗi printf GIU_PATH/DICH đều bị ca ghi-kênh và shape giết bằng TinHieuChotCa. Giữ return lỗi tường minh và hai nhánh fault. |
| F868-05 / P3 / `fixture-khong-khoa-tu-choi-payload-kenh-hong` | **ĐÓNG**, `.claude/dev/launcher_test.py:8840` | BAD_CHANNEL head rc7, sạch; mutant exit7→exit0 bị ca hành vi và shape giết. Giữ đối chứng payload hợp lệ/rỗng và không DAT khi hỏng. |
| F868-06 / P3 / `fixture-kenh-rieng-chua-khoa-allexport` | **ĐÓNG**, `.claude/dev/launcher_test.py:8794` | Normal, bash-a và SHELLOPTS đều installer `ABSENT ABSENT`; hai mutant gán lại sau declare+x bị ca hành vi và shape giết thật. Giữ cả TAM_CAI/KENH_KQ, cả hai cách bật allexport. |

Không có finding mới cần hướng vá, owner hoặc quyết định chấp nhận nợ. Bằng chứng 44 mutant / 84 checks đều TinHieuChotCa nằm ở [strict audit](out/evidence/strict-hook-mutations.json); không dùng exception dựng sân làm kill.

## Từng tiêu chí N1–N7

Chạy CLI thật từng ca trong bốn nhóm bằng `--lap-ca TEN --lan 1` trên **head và base-cross**, không thay bằng gọi import: `PYTHONDONTWRITEBYTECODE=1 python3 -B out/review.py targeted head` và `… targeted base-cross`. Mỗi JSON ca ghi argv/cwd/rc/thời gian, kèm stdout/stderr. 29 ca: head **28 pass + 1 lỗi môi trường**; nền **21 pass + 8 đỏ**, trong đó cùng 1 lỗi môi trường. [Head](out/evidence/targeted-head.json), [nền + test head](out/evidence/targeted-base-cross.json).

| Tiêu chí | Kết quả thật, phản chứng và đột biến |
|---|---|
| N1 kênh riêng | N1 CLI head 1/1, nền 0/1. Phép độc lập dùng **nguyên recipe YAML qua cai_cong_cu.sh**: (a) writer muộn nền rc2/DO, head rc0/DAT; (b) stdout không LF nền rc2/DO, head rc0/DAT; (c) dòng cuối installer nền/head rc0/DAT. Writer marker thật ở cả hai; head chọn đúng ứng viên, installer không thấy hai biến. Producer/reader/export/allexport và lỗi đọc có kill TinHieuChotCa. [Dữ liệu](out/evidence/hunt-channel.json). |
| N2 không chờ EOF stdout | CLI head 1/1; nền 0/1, khoảng20 giây/rc2. Writer giữ stdout3 giây: head shell và capture đều0.266s/rc0/DAT. Mutant chuyển lại `$(eval)` bị ca hành vi và shape giết. Giữ stderr được tách ở hướng4 bên dưới. |
| N3 không helper | Fallback LF/CRLF/empty-output head và nền đều rc0/DAT; `r868_khong_bo_chon_doc_dong_cuoi` cả hai1/1. Mutant bỏ fallback/bỏ CR bị TinHieuChotCa. `ops/cong_cu_test.py` **61/61**, không skip/precheck-skip, cây thật ĐẠT; PyYAML/jsonschema/actionlint giữ recipe cũ, hai tệp cong_cu_test/cai_actionlint không đổi byte. [Fallback](out/evidence/hunt-fallback.json). |
| N4 rg dùng helper chung | r802 bảng cài, r802 Windows, r831 Linux/macOS pass cả hai phía; 15/15 tiền tố installer trước ` && ` đầu tiên giữ nguyên. YAML chỉ `rg.cai` đổi. Mutant quay selector riêng và bỏ ứng viên WinGet/usrbin/brew đều có kill thật. Không tái thêm lọc rg.exe; tên trần đã DAT giữ PATH/GITHUB_PATH. |
| N5 vòng duyệt | `r868_vong_duyet_ung_vien` head/nền1/1. Hai mutant chỉ duyệt2/bỏ break bị **chính ca hành vi** giết bằng TinHieuChotCa, ngoài shape. Ca buộc ứng viên tốt đầu tiên ở vị trí3; vị trí4 tốt nhưng không được checker gọi. |
| N6 hồi quy858 | Mọi ca r858 head xanh, trừ r858_goc_tam OSError EROFS giống nền. `r858_bat_buoc_bash_khong_dua_rg_hong_len_dau` cả hai xanh. Batch 18 tổ hợp riêng không rò thư mục; mutant Q4 đổi neo có kill thật. Không xoá ca/hàm. |
| N7 release/selftest | Head **selftest 1731/1731 rc0** sau sửa env driver; nền cũng1731/1731. Release strict head **ok=true, expected=checked=191**, nền 190/190. Witness manifest sửa một sha256: rc2/ok=false, chỉ rõ .gitattributes mismatch; acceptance witness ném TinHieuChotCa. Đây là phép validator trực tiếp, không giả nhận một ca r868 shell là kiểm N7. [Mutant manifest](out/evidence/release-mutation-witness.json). |

Nền đỏ ở fault kênh vì không có kênh mới để fault, và shape nền `ValueError: substring not found`. Ghi lỗi thực, **không đếm chúng là kill**. Ca N1 dừng sớm ở (a) trên nền nên phép (b) được đo riêng; đã chứng minh đúng yêu cầu hai vế đỏ độc lập.

Lệnh cho từng dòng sau: cwd `out/<phía>`, `PYTHONDONTWRITEBYTECODE=1 python3 -B .claude/dev/launcher_test.py --lap-ca <TEN> --lan 1`.

| TEN | Head rc | Nền + test head rc |
|---|---:|---:|
| `r858_goc_tam_tranh_to_tien_co_git` | [1](out/evidence/target-head-r858_goc_tam_tranh_to_tien_co_git.stdout) | [1](out/evidence/target-base-cross-r858_goc_tam_tranh_to_tien_co_git.stdout) |
| `r802_doctor_rg_tran_hong_la_BI_CHE` | [0](out/evidence/target-head-r802_doctor_rg_tran_hong_la_BI_CHE.stdout) | [0](out/evidence/target-base-cross-r802_doctor_rg_tran_hong_la_BI_CHE.stdout) |
| `r802_doctor_rg_chi_ban_tot_khong_BI_CHE` | [0](out/evidence/target-head-r802_doctor_rg_chi_ban_tot_khong_BI_CHE.stdout) | [0](out/evidence/target-base-cross-r802_doctor_rg_chi_ban_tot_khong_BI_CHE.stdout) |
| `r802_doctor_git_tran_hong_la_BI_CHE` | [0](out/evidence/target-head-r802_doctor_git_tran_hong_la_BI_CHE.stdout) | [0](out/evidence/target-base-cross-r802_doctor_git_tran_hong_la_BI_CHE.stdout) |
| `r802_doctor_bash_ngoai_pham_vi_BI_CHE` | [0](out/evidence/target-head-r802_doctor_bash_ngoai_pham_vi_BI_CHE.stdout) | [0](out/evidence/target-base-cross-r802_doctor_bash_ngoai_pham_vi_BI_CHE.stdout) |
| `r802_doctor_ten_tran_tu_muc_PATH_rong` | [0](out/evidence/target-head-r802_doctor_ten_tran_tu_muc_PATH_rong.stdout) | [0](out/evidence/target-base-cross-r802_doctor_ten_tran_tu_muc_PATH_rong.stdout) |
| `r802_cai_rg_windows_chon_ban_chay_duoc` | [0](out/evidence/target-head-r802_cai_rg_windows_chon_ban_chay_duoc.stdout) | [0](out/evidence/target-base-cross-r802_cai_rg_windows_chon_ban_chay_duoc.stdout) |
| `r802_cac_duong_dan_chi_trong_PATH_va_theo_PATHEXT` | [0](out/evidence/target-head-r802_cac_duong_dan_chi_trong_PATH_va_theo_PATHEXT.stdout) | [0](out/evidence/target-base-cross-r802_cac_duong_dan_chi_trong_PATH_va_theo_PATHEXT.stdout) |
| `r802_runner_tra_lai_con_tro_nguoi_goi` | [0](out/evidence/target-head-r802_runner_tra_lai_con_tro_nguoi_goi.stdout) | [0](out/evidence/target-base-cross-r802_runner_tra_lai_con_tro_nguoi_goi.stdout) |
| `r802_bang_cai_rg_khop_cong_cu_yaml` | [0](out/evidence/target-head-r802_bang_cai_rg_khop_cong_cu_yaml.stdout) | [0](out/evidence/target-base-cross-r802_bang_cai_rg_khop_cong_cu_yaml.stdout) |
| `r802_hook_linux_rg_hong_van_thu_cargo` | [0](out/evidence/target-head-r802_hook_linux_rg_hong_van_thu_cargo.stdout) | [0](out/evidence/target-base-cross-r802_hook_linux_rg_hong_van_thu_cargo.stdout) |
| `r802_hook_windows_khong_cai_in_dung_lenh` | [0](out/evidence/target-head-r802_hook_windows_khong_cai_in_dung_lenh.stdout) | [0](out/evidence/target-base-cross-r802_hook_windows_khong_cai_in_dung_lenh.stdout) |
| `r831_cai_rg_linux_chon_ban_chay_duoc` | [0](out/evidence/target-head-r831_cai_rg_linux_chon_ban_chay_duoc.stdout) | [0](out/evidence/target-base-cross-r831_cai_rg_linux_chon_ban_chay_duoc.stdout) |
| `r831_cai_rg_macos_chon_ban_chay_duoc` | [0](out/evidence/target-head-r831_cai_rg_macos_chon_ban_chay_duoc.stdout) | [0](out/evidence/target-base-cross-r831_cai_rg_macos_chon_ban_chay_duoc.stdout) |
| `r858_cai_linux_chon_ban_chay_duoc` | [0](out/evidence/target-head-r858_cai_linux_chon_ban_chay_duoc.stdout) | [0](out/evidence/target-base-cross-r858_cai_linux_chon_ban_chay_duoc.stdout) |
| `r858_cai_macos_chon_ban_chay_duoc` | [0](out/evidence/target-head-r858_cai_macos_chon_ban_chay_duoc.stdout) | [0](out/evidence/target-base-cross-r858_cai_macos_chon_ban_chay_duoc.stdout) |
| `r858_cai_windows_chon_ban_chay_duoc` | [0](out/evidence/target-head-r858_cai_windows_chon_ban_chay_duoc.stdout) | [0](out/evidence/target-base-cross-r858_cai_windows_chon_ban_chay_duoc.stdout) |
| `r858_cai_python_khong_in_thu_muc_ban_hong` | [0](out/evidence/target-head-r858_cai_python_khong_in_thu_muc_ban_hong.stdout) | [0](out/evidence/target-base-cross-r858_cai_python_khong_in_thu_muc_ban_hong.stdout) |
| `r858_bat_buoc_bash_khong_dua_rg_hong_len_dau` | [0](out/evidence/target-head-r858_bat_buoc_bash_khong_dua_rg_hong_len_dau.stdout) | [0](out/evidence/target-base-cross-r858_bat_buoc_bash_khong_dua_rg_hong_len_dau.stdout) |
| `r858_hinh_dang_cong_thuc_cai` | [0](out/evidence/target-head-r858_hinh_dang_cong_thuc_cai.stdout) | [1](out/evidence/target-base-cross-r858_hinh_dang_cong_thuc_cai.stdout) |
| `r858_selftest_editskill_thu_muc_rieng` | [0](out/evidence/target-head-r858_selftest_editskill_thu_muc_rieng.stdout) | [0](out/evidence/target-base-cross-r858_selftest_editskill_thu_muc_rieng.stdout) |
| `r868_kenh_rieng_khong_doc_stdout_trinh_cai` | [0](out/evidence/target-head-r868_kenh_rieng_khong_doc_stdout_trinh_cai.stdout) | [1](out/evidence/target-base-cross-r868_kenh_rieng_khong_doc_stdout_trinh_cai.stdout) |
| `r868_writer_muon_khong_lam_treo` | [0](out/evidence/target-head-r868_writer_muon_khong_lam_treo.stdout) | [1](out/evidence/target-base-cross-r868_writer_muon_khong_lam_treo.stdout) |
| `r868_khong_bo_chon_doc_dong_cuoi` | [0](out/evidence/target-head-r868_khong_bo_chon_doc_dong_cuoi.stdout) | [0](out/evidence/target-base-cross-r868_khong_bo_chon_doc_dong_cuoi.stdout) |
| `r868_doc_kenh_hong_thi_dung` | [0](out/evidence/target-head-r868_doc_kenh_hong_thi_dung.stdout) | [1](out/evidence/target-base-cross-r868_doc_kenh_hong_thi_dung.stdout) |
| `r868_ghi_kenh_hong_thi_dung` | [0](out/evidence/target-head-r868_ghi_kenh_hong_thi_dung.stdout) | [1](out/evidence/target-base-cross-r868_ghi_kenh_hong_thi_dung.stdout) |
| `r868_don_kenh_khi_loi` | [0](out/evidence/target-head-r868_don_kenh_khi_loi.stdout) | [1](out/evidence/target-base-cross-r868_don_kenh_khi_loi.stdout) |
| `r868_vong_duyet_ung_vien` | [0](out/evidence/target-head-r868_vong_duyet_ung_vien.stdout) | [0](out/evidence/target-base-cross-r868_vong_duyet_ung_vien.stdout) |
| `r868_hinh_dang_kenh_ket_qua` | [0](out/evidence/target-head-r868_hinh_dang_kenh_ket_qua.stdout) | [1](out/evidence/target-base-cross-r868_hinh_dang_kenh_ket_qua.stdout) |

## Hướng săn độc lập

Mỗi hướng sau đã chạy mới ở lượt5, có giả thuyết, lệnh và output thật. `PYTHONDONTWRITEBYTECODE=1` áp dụng mọi lệnh Python; driver [hunts.py](out/hunts.py) ghi argv/fixture/stdout/stderr rồi cập nhật verdict sau từng hướng. Không soạn payload tấn công đường dẫn/thoát thư mục.

| HƯỚNG | Giả thuyết | Lệnh đã chạy | Output thật rút gọn | Kết luận |
|---|---|---|---|---|
| 1. Kênh/stdout/export | Log muộn/không LF hoặc allexport làm lẫn/lộ kênh. | `python3 -B out/hunts.py channel` | Nền a/b rc2/DO; head a/b/c rc0/DAT, đúng ứng viên. Normal/bash-a/SHELLOPTS: `ABSENT ABSENT`, tmp_left=[]. | **KHÔNG PHẢI LỖI** trên head. [JSON](out/evidence/hunt-channel.json). |
| 2. Batch/source/trap | Lượt source sau xoá nhầm/rò kênh, dùng kết quả lượt trước hoặc che installer lỗi. | `python3 -B out/hunts.py batch` | 18 tổ hợp hai thứ tự ×3 chế độ export ×success/first-failure/second-failure: 6 rc0,12 rc23; mọi tmp_left=[]; installer từng lượt thấy ABSENT ABSENT. DAT của lượt trước không che rc23 toàn lệnh. | **KHÔNG PHẢI LỖI**. [JSON](out/evidence/hunt-batch.json). |
| 3. Errexit/rc recipe | Subshell mới nuốt lỗi mà command substitution cũ trả khác0. | `python3 -B out/hunts.py failures` | Installer rc29 cả nền/head; không ứng viên nền rc2/head rc1, đều khác0; `false; echo uv` cả hai rc0/DAT; pipeline-fail cả hai rc1. | **KHÔNG PHẢI LỖI** với recipe hiện hành; semantics được giữ ở phép so. [JSON](out/evidence/hunt-failures.json). |
| 4. Giữ stdout/STDERR | Con giữ descriptor làm shell hoặc caller treo. | `python3 -B out/hunts.py streams` | stdout shell/capture0.266s; stderr shell0.318s nhưng capture3.093s; cả hai shell0.315s/capture3.094s; đều rc0/DAT. | **KHÔNG PHẢI LỖI N2** stdout. Caller capture stderr vẫn chờ EOF, ghi rõ giới hạn. [JSON](out/evidence/hunt-streams.json). |
| 5. Fallback/pip/CRLF | Reader mới mất dòng cuối hoặc không chấp nhận pip im lặng. | `python3 -B out/hunts.py fallback`; `… out/review.py gates other` | LF/CRLF/empty-output cả hai phía rc0/DAT, tmp_left=[]; congcu61/61. | **KHÔNG PHẢI LỖI** mô phỏng; CRLF/Git Bash thật **KHÔNG ĐO ĐƯỢC**. [JSON](out/evidence/hunt-fallback.json). |
| 6. Windows rg/GITHUB_PATH | Bỏ rg.exe hoặc helper chung chọn bản hỏng, mất chuyển cygpath, ghi PATH khi bare-good. | `python3 -B out/hunts.py windows` | Links/choco/bare-good/gp-empty/gp-unset rc0/DAT; u-error/w-error/both-bad rc1. `Local AppData` có khoảng trắng vẫn đúng; -w ra `W:…`; bare-good không ghi GITHUB_PATH. | **KHÔNG PHẢI LỖI** trong POSIX stub; native **KHÔNG ĐO ĐƯỢC**. [JSON](out/evidence/hunt-windows.json). |
| 7. Những đường thoát thứ sáu trở đi | Danh sách executor bỏ sót lỗi sau tạo temp dẫn đến rò. | `python3 -B out/hunts.py exits` | Reader I/O/payload rc7, fallback stdout-read rc74, init-kq/open-stdout rc1, final-probe rc2; head mọi tmp_left=[]. Mutant lượt4 cả hai reader rc7 nhưng còn1 thư mục, witness TinHieuChotCa. | **KHÔNG PHẢI LỖI** runtime; F868-02 đóng. [JSON](out/evidence/hunt-exits.json). |
| 8. Q4 và mất neo cũ | Xoá5 mutant YAML làm mất ý đồ kiểm executable/probe/ghi PATH. | `python3 -B out/audit.py`; `python3 -B out/mutations.py strict` | Không mất hàm/ca; chỉ5 mutant đã giải thích Q4 bị bỏ. Chốt chuyển sang helper, 44 mutant / 84 TinHieuChotCa; cả mutant đổi selector, cygpath, bare-good và ghi PATH đều chết đúng ca. | **KHÔNG PHẢI LỖI** về chuyển chốt đã đo. [Audit](out/evidence/scope-audit.json), [strict](out/evidence/strict-hook-mutations.json). |
| 9. Tìm survivor ngoài bảng | Còn thay đổi không tương đương mà bộ launcher không phân biệt. | `python3 -B out/mutations.py additional`; `… full drop-nounset`; `… full drop-pipefail` | Mỗi mutant28 pass+1 lỗi setup targeted; toàn launcher229/242,failed13/skip10 như control, delta0. Witness recipe giả control rc1, mutant rc0/DAT, ném TinHieuChotCa. | **KHÔNG PHẢI LỖI** bản vá với YAML hiện tại; ghi giới hạn thực, không gọi survivor thành equivalent/killed. [Dữ liệu](out/evidence/additional-mutations.json), [suite delta](out/evidence/suite-delta-r5.json). |

## Đột biến BẢN VÁ và đột biến ngoài bảng

`python3 -B .claude/dev/launcher_test.py --dot-bien` (cwd out/head): **rc0, 310/310 đạt, 4 không đo được**. Output đầy đủ vẫn có 15 dòng OK kèm ngoại lệ từ nhóm launcher cũ (4 AssertionError trần,5 OSError,2 FileNotFoundError,1 JSONDecodeError,2 TypeError,1 AttributeError). **Không nhận tín dụng TinHieuChotCa cho chúng.** Đã chạy classifier nghiêm riêng toàn bộ DOT_BIEN_HOOK hiện tại: **44 mutant,84 checks,84 TinHieuChotCa,0 lỗi vô can/skip/survived**. Trong đó19 mutant wp868; mỗi mutant N1–N6 có ca hành vi và shape như bảng, không chỉ grep. N7 kiểm bằng selftest/release và witness manifest riêng. [Output cổng](out/evidence/mutation.stdout), [cặp neo/thay + kết quả strict](out/evidence/strict-hook-mutations.json).

Đã tự thử hai mutant ngoài bảng trên **hai bản sao đầy đủ** dưới out/, mỗi bản chỉ đổi shell:

| Mutant / phép thay nguyên văn | Bộ ca hiện có | Witness không tương đương / đánh giá phạm vi |
|---|---|---|
| `drop-nounset`: `set -euo pipefail` → `set -eo pipefail` | Targeted 28 pass+1 OSError môi trường; toàn launcher cùng13 failed/10 skip,229/242 pass; không có TinHieuChotCa mới. | Recipe giả `printf %s "$WP868_UNSET_FOR_REVIEW"`, bare-rg tốt: control rc1, mutant rc0/DAT; witness ném TinHieuChotCa. YAML hiện hành không tham chiếu biến giả này; các biến tuỳ chọn của hợp đồng đều guarded, biến Windows LOCALAPPDATA được fixture và môi trường Windows chuẩn cung cấp. Không mở finding runtime cho recipe tương lai. |
| `drop-pipefail`: `set -euo pipefail` → `set -eu` | Cùng kết quả targeted và toàn launcher; không đếm OSError chung là kill. | Recipe giả `false | echo uv`: control rc1, mutant rc0/DAT, witness TinHieuChotCa. Không recipe hiện hành nào có pipeline shell; đây là giới hạn với recipe giả, giữ kết luận lượt4 cho lớp này. |

Các survivor này **sống thật trong bộ launcher hiện có**, không chứng minh head thiếu nounset/pipefail (head vẫn bật cả hai). Không dùng ngoại lệ vô can để ép kết quả đẹp, không bỏ qua điều kiện hiện hành của spec để mở một finding chỉ đúng với YAML được giả lập. Phép thay, từng targeted exception và witness đều ở [additional-mutations.json](out/evidence/additional-mutations.json). Toàn suite mutant có log/metadata riêng, delta với control được lưu, không lấy số từ lượt trước.

## Bảng lệnh → kết quả thật

Metadata JSON cùng tên với mỗi stdout chứa argv, cwd, auth giả/không auth, TMPDIR, rc và thời gian. Cwd của gate là `out/head` trừ dòng có ghi nền; mọi Python dùng `PYTHONDONTWRITEBYTECODE=1` và `-B`. Driver rc0 không thay cho rc của gate con.

| Lệnh / cwd hoặc driver | Kết quả thật |
|---|---|
| `python3 -B out/review.py setup` / $R | rc0, dựng hai vế và base-cross cùng 1 lệnh; [log](out/setup.log). |
| `python3 -B .claude/dev/launcher_test.py --nhat-ky …` / base; auth=none | rc=1; 221/234 ca DA CHAY QUA (tong 244, bo qua 10, hong 13) - KHONG DU: 10 ca BO QUA, chua do gi; 206.119s. [output](out/evidence/launcher-base-none.stdout). |
| `python3 -B .claude/dev/launcher_test.py --nhat-ky …` / base; auth=fake | rc=1; 221/234 ca DA CHAY QUA (tong 244, bo qua 10, hong 13) - KHONG DU: 10 ca BO QUA, chua do gi; 186.003s. [output](out/evidence/launcher-base-fake.stdout). |
| `python3 -B .claude/dev/launcher_test.py --nhat-ky …` / head; auth=none | rc=1; 229/242 ca DA CHAY QUA (tong 252, bo qua 10, hong 13) - KHONG DU: 10 ca BO QUA, chua do gi; 214.665s. [output](out/evidence/launcher-head-none.stdout). |
| `python3 -B .claude/dev/launcher_test.py --nhat-ky …` / head; auth=fake | rc=1; 229/242 ca DA CHAY QUA (tong 252, bo qua 10, hong 13) - KHONG DU: 10 ca BO QUA, chua do gi; 195.77s. [output](out/evidence/launcher-head-fake.stdout). |
| `python3 -B .claude/dev/launcher_test.py --dot-bien` | rc=0; 310/310 đạt; 4 không đo được; giới hạn exception xem trên; 158.104s. [output](out/evidence/mutation.stdout). |
| `CONG_CU_TEST_BAN_KINH=manh python3 -B ops/cong_cu_test.py` | rc=0; 61/61 đạt,skip0/precheck-skip0; cây thật ĐẠT. 470 mutant radius được giao job mảnh, KHÔNG chạy trong tiến trình này; 289.998s. [output](out/evidence/congcu.stdout). |
| `bash -n ops/cai_cong_cu.sh` | rc=0; syntax hợp lệ; 0.004s. [output](out/evidence/bash-n.stdout). |
| `python3 -B scripts/tl.py --selftest` / head, env đã sửa | rc=0; 1731/1731; 213.424s. [output](out/evidence/selftest-head-corrected-env.stdout). |
| cùng lệnh / base, env đã sửa | rc=0; 1731/1731; 213.512s. [output](out/evidence/selftest-base-corrected-env.stdout). |
| `python3 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | rc=0; ok=true, strict=true, expected=checked=191; failed=[]; 0.868s. [output](out/evidence/release.stdout). |
| cùng lệnh / base | rc=0; ok=true, expected=checked=190; 1.018s. [output](out/evidence/release-base.stdout). |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | rc=0; sạch,10 tệp,0 hit; 0.366s. [output](out/evidence/doctrine.stdout). |
| `python3 -B scripts/tl.py doc-claims-check --strict` | rc=0; ok=true,strict=true,113 tệp,flags=[]; 3.074s. [output](out/evidence/claims.stdout). |
| `actionlint` | rc=0; stdout/stderr rỗng, không thêm finding; 0.016s. [output](out/evidence/actionlint.stdout). |
| `ruff check --select F .claude/dev/launcher_test.py scripts/tl_selftest.py` / base và head | rc1 cả hai,4397 finding; multiset(file,code,message) bằng nhau,thêm0/bớt0 (bỏ line/column dịch chuyển). Launcher_test5 F841; selftest4391 F821+1 F401. [Nền](out/evidence/ruff-delta-base.stdout), [head](out/evidence/ruff-delta-head.stdout). |
| `ruff check --select F .` / base và head | rc1 cả hai,8806 finding; số nền ghi riêng, không coi đỏ tuyệt đối là hồi quy của packet. [Nền](out/evidence/ruff-base.stdout), [head](out/evidence/ruff-head.stdout). |
| `python3 -B out/mutations.py strict` | rc0,44 mutant / 84 TinHieuChotCa; [log](out/strict-mutations.log). |
| `python3 -B out/mutations.py full drop-nounset`; `… full drop-pipefail` | Gate con rc1 mỗi bản,229/242 passed,13 failed/10 skipped; cùng tập nền/head,delta đỏ mới0. [Nounset](out/evidence/launcher-mutant-drop-nounset.stdout), [pipefail](out/evidence/launcher-mutant-drop-pipefail.stdout). |
| `python3 -B out/audit.py` / $R, đầu/cuối | rc0; băm nguồn không đổi,status sạch,6 tệp/421 dòng thêm,write set đúng; [audit](out/evidence/scope-audit.json). |

**Lỗi driver đã đo và sửa:** lượt selftest đầu head/base đều rc1,1730/1731, riêng `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim`. Driver đặt core.abbrev=7 ở command scope, nên fixture `git config core.abbrev 8` không có hiệu lực. Đã bỏ override command-scope đó, giữ repo-local7, rồi chạy lại **toàn selftest cả hai vế** thành1731/1731. Giữ [output head cũ](out/evidence/selftest.stdout), [nền cũ](out/evidence/selftest-base.stdout) và metadata; không che failure hoặc vá nguồn để qua cổng.

**Delta launcher:** cả 4 lượt nền/head×auth-none/fake đều chạy trọn vẹn, cùng13 failed/cùng10 skipped; delta đỏ mới0, cả 8 r868 head đều qua ở cả hai auth. Hai lỗi EROFS là t86 và r858_goc_tam;11 r484 là materializer nhận home bên trong repo vì /tmp/.git của sandbox. [Đối chiếu tên ca và summary](out/evidence/suite-delta-r5.json). Đây là failed môi trường + skipped, không phải pass.

## Diff và write set

- Tự dựng lại `git diff --binary base HEAD` và `git diff --numstat base HEAD`: bằng byte với diff.patch/numstat.txt được cấp. `git diff --check` rc0. Từ lượt4 chỉ `.claude/dev/launcher_test.py` đổi; diff-tu-luot4.patch cũng byte-match.
- **6 tệp,421 dòng thêm/93 xoá ≤450**, đúng6 đường sản phẩm trong spec; không `ops/handoff/*`. Lease write set7 gồm handoff dành cho nhánh lease, không suy thành cho phép thêm nó vào diff PR.
- YAML semantic chỉ rg.cai đổi;15 tiền tố cài giữ nguyên. Selftest AST chỉ ratchet190→191; manifest kiểm strict đúng nội dung. Không mất hàm/ca test;244→252 ca. Bỏ đúng5 mutant YAML mất neo, handoff Q4 giải thích từng nhóm; đã đo chốt ở helper với44 mutant strict. [Numstat, AST và audit](out/evidence/scope-audit.json).

## Không đo được

- **not_run:** check run `ci.yml`, workflow_dispatch `launcher-windows.yml` trên exact head, thread resolve M-2 và heartbeat/authority live. Review cấm mạng/GitHub; không có bằng chứng máy độc lập để ghi chúng xanh. M-3 vẫn cần người có authority kiểm trên head header trước khi báo đủ điều kiện.
- **KHÔNG ĐO ĐƯỢC native Windows/Git Bash/macOS:** cygpath/CRLF/PATHEXT/ACL/mktemp thực và sàn mutation Windows≥70%; chỉ mô phỏng trên Linux hoặc chạy ca shape thuần Python. Không đổi tên mô phỏng thành nghiệm thu đa nền.
- **skipped launcher:**8 ca venv/pip khi không có gói offline,2 ca chỉ Windows; cùng nền/head. **failed môi trường:**13 ca nêu trên; không sửa gốc tạm của packet khác theo Q9. Không nhận output launcher thành252/252.
- **not_run:**470 mutant bán kính congcu giao job mảnh/gom; đã chạy61ca hành vi và kiểm classifier/giàn giáo/cây thật của lệnh manh.4 mutant launcher riêng nền không đo được;15 dòng exception của nhóm cũ không được nhận tín dụng strict kill.
- Writer giữ STDERR: shell thoát sớm nhưng caller capture stderr có thể chờ writer kết thúc; không suy N2 stdout thành hứa không chờ mọi stream. Không chạy installer mạng thật; dùng stub vô hại và checker thật.

Các giới hạn này đã được ghi riêng, không phát hiện P0/P1/P2/P3 mới của bản vá trong những phép đã đo. Verdict chỉ neo exact head/tree ở header.
