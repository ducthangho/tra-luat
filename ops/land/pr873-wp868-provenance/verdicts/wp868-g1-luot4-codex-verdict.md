verdict: changes_requested
reviewed_head: 0bfc73d6f7a810dc3716bb40f0193eae9cd3f888
reviewed_sha: 0bfc73d6f7a810dc3716bb40f0193eae9cd3f888
reviewed_tree: 557f41fb730953c68b7f964802822d59ba09b2f2
review_class: sensitive
provider: openai_codex
model: gpt-6.1-sol
model_family: openai
reasoning_effort: xhigh
execution_surface: codex_cli
transport: machine
review_round: 4/5

## Kết luận

**changes_requested — F868-06 ĐÓNG; F868-02 MỞ LẠI về độ phủ cleanup khi reader lỗi sau khi công thức cài đã thành công.** Giữ ID/slug cũ vì cùng lớp cleanup khi thoát lỗi; không tạo F868-07 cho cùng hình dạng. F868-01/03/04/05 giữ trạng thái đóng. Runtime head nguyên vẹn dọn sạch ở mọi fault đã đo; finding này yêu cầu khóa hồi quy bằng test, không yêu cầu sửa runtime.

Đã hoàn tất các cổng có thể chạy offline; mọi failure/skip nền và giới hạn CI/Windows được tách riêng bên dưới.

M-1 của lease yêu cầu P2/P3 mở có quyết định chủ kho kèm link; dữ liệu offline chưa có quyết định cho nhánh tái mở này. Verdict không cấp quyền merge/land/deploy. Không gọi mạng/GitHub, không sửa hai cây nguồn, không viết patch sản phẩm.

## Neo và môi trường

- Base/merge-base với `origin/master`: `9e9a74b2a396ef458d25c51a5563efafbb45ba0c`; base tree `9fc05c9986f711d1961e040dc7345850d0133294`. Head/tree đúng header, `core.abbrev=7`, hai cây sạch lúc đầu. [Neo thật](out/evidence/anchors.stdout).
- Spec SHA-256 `0d950c2b98b9e024bf1cc43a77c5d3351b5f4c21e6307b2e36ba9cdeca7b3f69`; verdict lượt 3 SHA-256 `d327dacae9d32651b7f213421e4c4ac910bc642b3fda504f26d0c131b7734e36`: đã tự băm, khớp. `prompt.snapshot` bằng byte với `PROMPT.md`. Đã đọc spec, lease, handoff Q4, các verdict lượt 1–3 và #858 lượt 4–5. [Spec](out/evidence/spec.md), [lease](out/evidence/lease.yaml), [lượt 3](out/evidence/round3.md), [handoff](out/evidence/handoff.stdout).
- Lease offline generation 1, sensitive, hạn `2026-10-24T06:52:00Z`; không suy authority/heartbeat/CI live từ bản lease. Cổng M-2/M-3 phía GitHub chưa được xác minh.
- Run `6427f21387dc49b6ac9b53e385707b69`, CLI 0.163.0 công bố model/effort như header; không chứng thực model phục vụ từng request. [Header CLI](out/evidence/model-header.txt).
- Linux x86_64, Bash 5.2.21, Python 3.13.16, Git 2.43.0, ruff 0.17.1; actionlint thật 1.7.7. [Môi trường](out/evidence/runtime.stdout), [audit](out/evidence/scope-audit.json).
- `PYTHONDONTWRITEBYTECODE=1 python3 -B out/review.py setup` dựng **cả head và base trong MỘT lệnh**, bản sao thường không hardlink, thêm base-cross bằng cách chép test head vào nền. Chỉ chạy ca/fixture/mutant trong `out/`. Env chung: `PYTHONDONTWRITEBYTECODE=1`, `PIP_NO_INDEX=1`, `PIP_DISABLE_PIP_VERSION_CHECK=1`, `TMPDIR=$R/out/tmp`, tắt Git commit signing bằng command config. Auth thật bị gỡ khỏi tiến trình test; hai lượt fake dùng chuỗi giả `review-fixture-not-a-credential`.
- `/tmp/.git` là tmpfs rỗng **ro mode555**; `/var/tmp` không ghi được trong sandbox. `t86`, `r858_goc_tam` và 11 `r484_*` đỏ ở cả nền/head: ghi failed, không tính thành hồi quy. 8 ca venv/pip bị bỏ qua do offline cùng 2 ca riêng Windows. Không tháo mount/xoá marker để làm xanh cổng.

## Đối chiếu lượt trước — đã làm trước săn mới

Lệnh thật: `PYTHONDONTWRITEBYTECODE=1 python3 -B out/prior_r4.py`. Driver lấy đúng hai phép thay của lượt 3, không thay bằng kết quả cũ. [Lệnh và output](out/prior-r4.log), [JSON](out/evidence/prior-r4.json).

| Finding / mức / slug ổn định | Kết quả lượt 4 |
|---|---|
| F868-01 / P2 / `stdout-installer-bi-nhan-lam-ket-qua-chon` | **ĐÓNG.** Control I/O reader DAT; cat rc74 làm head rc7, không DAT, không probe thư mục stdout, tmp_left=[]. Mutant `&&`→`;` bị ca hành vi và shape giết bằng TinHieuChotCa. |
| F868-02 / P2 / `fixture-khong-khoa-don-kenh-khi-thoat-loi` | Mutant cũ tắt trap trước installer vẫn bị giết thật; batch bỏ rm cũng bị giết. **MỞ LẠI cùng lớp**, theo mutant tắt trap sau eval ở finding bên dưới. |
| F868-03 / P3 / `fixture-fallback-khong-khoa-crlf` | **ĐÓNG.** Head/nền fallback LF/CRLF pass; mutant bỏ cắt CR bị đúng ca hành vi và shape giết. |
| F868-04 / P2 / `fixture-khong-khoa-loi-ghi-payload-kenh` | **ĐÓNG.** Hai mutant nuốt lỗi ghi `GIU_PATH`/`DICH` đều bị `r868_ghi_kenh_hong_thi_dung` giết bằng TinHieuChotCa; control ca mới pass. |
| F868-05 / P3 / `fixture-khong-khoa-tu-choi-payload-kenh-hong` | **ĐÓNG.** Head nhận BAD_CHANNEL → rc7, không DAT, tmp_left=[]. Mutant exit7→exit0 bị ca hành vi và shape giết thật. |
| F868-06 / P3 / `fixture-kenh-rieng-chua-khoa-allexport` | **ĐÓNG.** Control hai ca pass. Cả mutant KENH và TAM nguyên văn lượt 3 đều bị **ca hành vi và shape** giết. Output ca hành vi: `allexport=co: trinh cai thay kenh: '/…/kq ABSENT\n'` hoặc `'ABSENT /…/cai_cong_cu.…\n'`. Head riêng normal/bash-a/SHELLOPTS đều rc0/DAT và installer `ABSENT ABSENT`. |

## Finding

| ID / mức / slug | Vị trí | Bằng chứng | Hướng xử lý bằng lời |
|---|---|---|---|
| **F868-02 / P2 / `fixture-khong-khoa-don-kenh-khi-thoat-loi` — MỞ LẠI** | `.claude/dev/launcher_test.py:8898` chỉ fault installer; `:8840` fault reader nhưng không chốt cleanup. Runtime được bảo vệ: `ops/cai_cong_cu.sh:124`–reader. | Bản sao chỉ thêm `trap - EXIT` **sau** dòng eval thành công. Giữ trap ban đầu, rm đường thành công, mọi chuỗi shape. Targeted: control và mutant đều 28 pass + 1 OSError môi trường, không TinHieuChotCa. Toàn launcher mutant rc=1, 229/242 ca DA CHAY QUA (tong 252, bo qua 10, hong 13) - KHONG DU: 10 ca BO QUA, chua do gi; delta lỗi/bỏ qua với control head = 0. Witness: control read-error/bad-payload rc7, tmp_left=[]; mutant cùng rc7 nhưng mỗi nhánh còn **một thư mục cai_cong_cu.***, witness ném **TinHieuChotCa**. Success của cả hai rc0/DAT, tmp_left=[]. | **Vá test** `r868_don_kenh_khi_loi` hoặc `r868_doc_kenh_hong_thi_dung`: dùng TMPDIR fixture riêng, cho installer thành công rồi fault cat đọc kênh và payload sai; chứng minh kênh từng được tạo và thư mục bị dọn cả khi rc7. Đăng ký mutant tắt trap sau eval, đòi TinHieuChotCa; giữ installer-failure/batch và đối chứng thành công. **Rủi ro:** đừng biến lỗi dựng sân thành kill, đừng đếm thư mục trước khi tiến trình kết thúc; giữ trần 450 dòng thêm. Không sửa runtime theo finding này. |

Mức P2 giữ theo finding gốc cùng lớp; đây là **thiếu khóa test**, không phải chứng minh runtime head đang rò. Nhánh cụ thể đã vá ở lượt trước vẫn có kill thật. [Phép thay mutant](out/evidence/additional-mutations.json), [targeted](out/evidence/additional-targeted.json), [witness](out/evidence/additional-witnesses.json), [suite/delta](out/evidence/suite-delta-r4.json).

## Từng tiêu chí N1–N7

Mỗi ca hiện có trong bốn nhóm `r868_*`, `r858_*`, `r831_*`, `r802_*` được chạy CLI ở **head và base-cross**: cwd `out/head` hoặc `out/base-cross`, `python3 -B .claude/dev/launcher_test.py --lap-ca TEN --lan 1`. Lệnh gom: `PYTHONDONTWRITEBYTECODE=1 python3 -B out/review.py targeted head` rồi `… targeted base-cross`. 29 ca mỗi phía: head **28 pass/1 lỗi môi trường**, nền **21 pass/8 đỏ**. [Toàn argv, rc và đuôi output](out/evidence/targeted-comparison.json).

| Tiêu chí | Kết quả thật và đột biến |
|---|---|
| N1 kênh riêng | `r868_kenh_rieng_khong_doc_stdout_trinh_cai` head1/1, nền0/1. Witness chạy nguyên recipe YAML qua script: **(a) writer muộn nền rc2/DO, head rc0/DAT; (b) không LF nền rc2/DO, head rc0/DAT; (c) dòng cuối cả hai rc0/DAT**. Marker writer_done=true; head chọn đúng ứng viên, installer không thấy hai biến. Producer/reader/export/allexport có kill thật. Cleanup còn F868-02. |
| N2 không chờ EOF stdout | `r868_writer_muon_khong_lam_treo` head1/1, nền0/1 với **20.4s/rc2**. Mutant chờ EOF stdout bị ca hành vi và shape giết. Phép giữ stdout riêng: head shell0.609s/rc0; giữ stderr: shell0.641s nhưng communicate3.212s. |
| N3 fallback công thức không helper | `r868_khong_bo_chon_doc_dong_cuoi` head/nền1/1, có LF/CRLF; mutant bỏ fallback/bỏ CR đều bị TinHieuChotCa. `congcu-ci` **61/61**, skip/precheck-skip0, cây thật ĐẠT. PyYAML/jsonschema/actionlint vẫn recipe cũ; `ops/cong_cu_test.py` và `ops/cai_actionlint.sh` không đổi. |
| N4 rg dùng helper chung | `r802_bang_cai_rg_khop_cong_cu_yaml` và r802/r831 liên quan pass cả hai. Audit chỉ rg thay YAML; tiền tố cài trước && đầu tiên giữ nguyên cả15 recipe. Mutant quay bộ chọn riêng và bỏ ứng viên winget/usrbin/brew bị giết thật. |
| N5 khóa vòng duyệt | `r868_vong_duyet_ung_vien` head/nền1/1. Tốt đầu tiên ở vị trí3; ứng viên4 cũng tốt nhưng marker không được ghi. Hai mutant chỉ duyệt2/bỏ break đều bị **chính ca hành vi** giết, không chỉ shape. |
| N6 hồi quy858 | Tất cả r858 hành vi head pass, trừ `r858_goc_tam` OSError EROFS giống nền. `r858_bat_buoc_bash_khong_dua_rg_hong_len_dau` pass cả hai; batch12 tổ hợp không rò temp. Những mutant chốt cũ chuyển neo đều có kill thật. |
| N7 selftest/release | Head **selftest1731/1731 rc0**, release strict **ok=true, expected=checked=191**. N7 đo trực tiếp bằng hai gate; không nhận mutant shell làm bằng chứng kiểm release. |

Nền đỏ ở `r868_ghi_kenh_hong_thi_dung` và cleanup vì **không có kênh mới để fault**; shape nền `ValueError: substring not found`. Không đếm các lỗi dựng ấy là kill. Test N1 dừng ở biểu hiện a nên witness độc lập bắt buộc đã đo b riêng.

| Ca (`--lap-ca TEN --lan 1`) | Head rc | Nền + test head rc |
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

Các lệnh đều thực thi mới trong lượt4. `out/hunts_r4.py` gọi lần lượt các hàm của `out/probes.py`, đồng thời cập nhật VERDICT sau từng hướng. Mọi subprocess có argv, rc, stdout/stderr trong thư mục fixture. Không soạn payload tấn công đường dẫn/thoát thư mục.

| HƯỚNG | Giả thuyết | Lệnh thật | Output thật rút gọn | Kết luận |
|---|---|---|---|---|
| 1. Kênh/stdout/allexport | Log muộn hoặc allexport làm kết quả bị lẫn/lộ. | `python3 -B out/hunts_r4.py` → `probes.channel()` | Nền a/b rc2/DO; head a/b/c rc0/DAT. Ba chế độ normal/bash-a/SHELLOPTS: `ABSENT ABSENT`, tmp_left=[]. Hai mutant gán lại cũ bị TinHieuChotCa. | **KHÔNG PHẢI LỖI** trên head; F868-06 đóng. [JSON](out/evidence/probe-channel.json). |
| 2. Batch/source/trap | Hai lượt source ghi đè trap, rò/xóa nhầm kênh hoặc dùng kênh lượt trước. | cùng driver → `probes.batch()` | 12 tổ hợp thứ tự rg,bash/bash,rg × thành công/lỗi23 ×3 chế độ. 6 rc0, 6 rc23, **mọi tmp_left=[]**. Có JSON DAT của công cụ trước vẫn không che rc23 batch. | **KHÔNG PHẢI LỖI** trong ma trận. [JSON](out/evidence/probe-batch.json). |
| 3. Errexit/mã thoát | `(set +e;eval)` nuốt failure mới so với `$(eval)` cũ. | driver → `probes.failures()`; `python3 -B out/additional_witnesses.py` | Nền/head installer lỗi rc29, checker lỗi rc1; chuỗi `false; echo ứng_viên` cả hai rc0/DAT. Mutant ép errexit: witness rc1; head rc0. | **KHÔNG PHẢI LỖI** trên recipe hiện hành; semicolon là giả lập tương lai. [JSON](out/evidence/probe-failures.json). |
| 4. Writer giữ stdout/stderr | Tiến trình nền giữ luồng làm script treo. | driver → `probes.streams()` | stdout shell0.609s/communicate0.611s; stderr shell0.641s/communicate3.212s; cả hai shell0.676s/communicate3.217s; đều rc0/DAT. | **KHÔNG PHẢI LỖI N2** (stdout); caller thu stderr vẫn chờ EOF, không hứa khác. [JSON](out/evidence/probe-streams.json). |
| 5. CRLF/fallback | Reader mới làm pip/actionlint mất đường lùi dòng cuối CRLF. | driver → `probes.crlf()`; `out/congcu_r4.py` | LF/CRLF head/nền DAT; congcu61/61, skip0/precheck0. Mutant bỏ CR chết bằng TinHieuChotCa. | **KHÔNG PHẢI LỖI** phần mô phỏng; Git Bash thật **KHÔNG ĐO ĐƯỢC**. [JSON](out/evidence/probe-crlf.json). |
| 6. Windows rg/cygpath/GITHUB_PATH | Bỏ lọc rg.exe hoặc đổi điều kiện GITHUB_PATH chọn bản hỏng/đổi PATH khi tên trần đã DAT. | driver → `probes.windows()` | Links/choco/bare-good/gp-empty/gp-unset rc0/DAT; bad/u-error/w-error rc1. Bare-good GITHUB_PATH rỗng; chọn ứng viên có chuyển cygpath-w. | **KHÔNG PHẢI LỖI** trong stub POSIX; native Windows/PATHEXT/ACL **KHÔNG ĐO ĐƯỢC**. [JSON](out/evidence/probe-windows.json). |
| 7. Reader I/O và stdout fallback | Cat lỗi bị hiểu là kênh rỗng rồi dùng thư mục stdout. | driver → `probes.io_readback()` | control rc0/DAT/DICH=ứng_viên; cat lỗi rc7, DICH không được đọc lại, không DAT, không probe thư mục stdout, tmp_left=[]. | **KHÔNG PHẢI LỖI** trên head; F868-01 đóng. [JSON](out/evidence/probe-io-readback.json). |
| 8. Cleanup sau recipe | Suite chỉ chốt cleanup lúc installer lỗi, bỏ sót lỗi reader sau cài thành công. | `python3 -B out/additional_mutations.py`; `out/additional_witnesses.py`; `out/full_mutant_r4.py` | Tắt trap sau eval sống targeted và toàn suite; witness read-error/rac đều rc7 nhưng còn1 thư mục; control cùng fault sạch. TinHieuChotCa từ assertion cleanup mới. | **LỖI độ phủ F868-02 tái mở**, head runtime đúng. [Witness](out/evidence/additional-witnesses.json). |
| 9. Q4/đổi neo cũ | Bỏ5 mutant YAML có làm mất chốt chọn bản chạy được/ghi GITHUB_PATH. | `python3 -B out/audit.py`; `out/strict_mutations.py` | Không mất ca/hàm; chỉ5 mutant YAML mất neo đã được handoff giải thích. 43 mutant hook/YAML/shell:82 TinHieuChotCa trên82 ca đích;21 control pass,0 lỗi dựng. | **KHÔNG PHẢI LỖI** về chuyển chốt Q4 đã đo. [Audit](out/evidence/scope-audit.json), [kill thật](out/evidence/strict-hook-mutations.json). |

## Đột biến ngoài bảng

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -B out/additional_mutations.py`. Ba mutant không tương đương, chỉ ghi bản sao shell trong out/. Mỗi mutant chạy cả29 ca liên quan; lỗi môi trường không được nhận kill. [Phép thay nguyên văn](out/evidence/additional-mutations.json), [output](out/additional-mutations.log), [witness](out/additional-witnesses.log).

| Mutant | Bộ ca hiện có | Witness phân biệt / xử lý |
|---|---|---|
| `clear-exit-trap-after-recipe` | {'INVALID_CREDIT': 1, 'pass': 28} | Head read-error/rac rc7, tmp_left=[]; mutant cùng rc7 còn1 thư mục mỗi nhánh → witness TinHieuChotCa; mở lại F868-02. |
| `force-errexit-inside-recipe` | {'INVALID_CREDIT': 1, 'pass': 28} | Chuỗi semicolon false rồi echo thư mục: control rc0/DAT, mutant rc1 → witness TinHieuChotCa. YAML hiện hành không có kiểu chuỗi ấy; **KHÔNG mở finding**. |
| `drop-pipefail` | {'INVALID_CREDIT': 1, 'pass': 28} | Recipe pipeline giả: control rc1, mutant rc0/DAT → witness TinHieuChotCa. Không recipe hiện hành nào có pipeline shell; đúng chỉ thị lượt4, **KHÔNG mở finding** cho giới hạn tương lai. |

Các fault trong witness không sửa mã test hiện có để làm suite đỏ: witness độc lập gọi `bang()` của module để xác nhận TinHieuChotCa, có control cùng sân và thành công cùng mutant. Thư mục rò được giữ dưới out/ làm bằng chứng. Mutant ép-errexit và pipefail chỉ cho thấy bộ ca không cam kết recipe ngoài YAML hiện tại; không dùng chúng tạo finding mới.

## Bảng lệnh → kết quả thật

Các lệnh có cwd tương ứng trong JSON; `PYTHONDONTWRITEBYTECODE=1` áp dụng cho mọi lệnh Python. Driver rc0 không thay cho mã thoát gate con.

| Lệnh / cwd | Kết quả thật |
|---|---|
| `python3 -B out/review.py setup` / $R | rc0; dựng head/base/base-cross trong một lệnh; nguồn chỉ đọc. [Log](out/setup.log). |
| `python3 -B .claude/dev/launcher_test.py --nhat-ky …` / out/base; auth=none | rc=1; 221/234 ca DA CHAY QUA (tong 244, bo qua 10, hong 13) - KHONG DU: 10 ca BO QUA, chua do gi; 274.361s — [output](out/evidence/launcher-base-none.stdout), [argv/env/cwd/rc](out/evidence/launcher-base-none.json) |
| `python3 -B .claude/dev/launcher_test.py --nhat-ky …` / out/base; auth=fake | rc=1; 221/234 ca DA CHAY QUA (tong 244, bo qua 10, hong 13) - KHONG DU: 10 ca BO QUA, chua do gi; 221.183s — [output](out/evidence/launcher-base-fake.stdout), [argv/env/cwd/rc](out/evidence/launcher-base-fake.json) |
| `python3 -B .claude/dev/launcher_test.py --nhat-ky …` / out/head; auth=none | rc=1; 229/242 ca DA CHAY QUA (tong 252, bo qua 10, hong 13) - KHONG DU: 10 ca BO QUA, chua do gi; 190.337s — [output](out/evidence/launcher-head-none.stdout), [argv/env/cwd/rc](out/evidence/launcher-head-none.json) |
| `python3 -B .claude/dev/launcher_test.py --nhat-ky …` / out/head; auth=fake | rc=1; 229/242 ca DA CHAY QUA (tong 252, bo qua 10, hong 13) - KHONG DU: 10 ca BO QUA, chua do gi; 184.193s — [output](out/evidence/launcher-head-fake.stdout), [argv/env/cwd/rc](out/evidence/launcher-head-fake.json) |
| `python3 -B .claude/dev/launcher_test.py --dot-bien` | rc=0; DOT BIEN: 309/309 dat  (4 khong do duoc tren nen nay); 198.612s — [output](out/evidence/mutation.stdout), [argv/env/cwd/rc](out/evidence/mutation.json) |
| `CONG_CU_TEST_BAN_KINH=manh python3 -B ops/cong_cu_test.py` | rc=0; cong_cu_test: 61/61 đạt; tổng=61, bỏ qua=0, tiền kiểm bỏ qua=0; SỐ LIỆU: ca=61 · đột biến=470 (giao mảnh) · lỗi đột biến=0 · tiền kiểm bỏ qua=0 · cổng cây thật=ĐẠT; 379.091s — [output](out/evidence/congcu-ci.stdout), [argv/env/cwd/rc](out/evidence/congcu-ci.json) |
| `bash -n ops/cai_cong_cu.sh` | rc=0; stdout/stderr rỗng; 0.007s — [output](out/evidence/bash-n.stdout), [argv/env/cwd/rc](out/evidence/bash-n.json) |
| `python3 -B scripts/tl.py --selftest` | rc=0; == tl selftest 1731/1731 ==; 290.038s — [output](out/evidence/selftest.stdout), [argv/env/cwd/rc](out/evidence/selftest.json) |
| `python3 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | rc=0; ok=True, expected=191, checked=191; 3.393s — [output](out/evidence/release.stdout), [argv/env/cwd/rc](out/evidence/release.json) |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | rc=0; doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine; 1.802s — [output](out/evidence/doctrine.stdout), [argv/env/cwd/rc](out/evidence/doctrine.json) |
| `python3 -B scripts/tl.py doc-claims-check --strict --json` | rc=0; ok=True, strict=true; 8.736s — [output](out/evidence/docclaims.stdout), [argv/env/cwd/rc](out/evidence/docclaims.json) |
| `python3 -B .claude/dev/launcher_test.py --nhat-ky … / full-mutant-clear-trap` | rc=1; 229/242 ca DA CHAY QUA (tong 252, bo qua 10, hong 13) - KHONG DU: 10 ca BO QUA, chua do gi; 220.883s — [output](out/evidence/additional-full-clear-trap.stdout), [argv/env/cwd/rc](out/evidence/additional-full-clear-trap.json) |
| `python3 -B -m ruff check --no-cache --select F --output-format json scripts/tl.py scripts/tl_selftest.py .claude/dev/launcher_test.py` / base và head | rc=1; 4409 finding; 0.323s — [output](out/evidence/ruff-base.stdout), [argv/env/cwd/rc](out/evidence/ruff-base.json); head: rc=1; 4409 finding; 0.371s — [output](out/evidence/ruff-head.stdout), [argv/env/cwd/rc](out/evidence/ruff-head.json); multiset finding không tính line dịch chuyển: **new=0, removed=0**. |
| `actionlint` / base và head | base: rc=0; stdout/stderr rỗng; 0.036s — [output](out/evidence/actionlint-base.stdout), [argv/env/cwd/rc](out/evidence/actionlint-base.json); head: rc=0; stdout/stderr rỗng; 0.023s — [output](out/evidence/actionlint-head.stdout), [argv/env/cwd/rc](out/evidence/actionlint-head.json). |
| `python3 -B out/strict_mutations.py` | rc0; 43 mutant, 82/82 ca đích TinHieuChotCa; không nhận exception vô can thành kill. |
| `python3 -B out/audit.py` | rc0; đúng6 tệp,409 dòng thêm/93 xóa,ngoài write set0,handoff trong PR=false; supplied diff khớp git diff. |

`congcu-ci` chạy đầy đủ61 ca + tiền kiểm + cổng cây thật + tự kiểm giàn giáo/chạy song song theo chế độ CI gate. **470 bán kính đột biến cong_cu được giao mảnh, không chạy trong lượt này**; không khai đã đo470/470. Gate launcher mutation:309/309 đo được,4 không đo được riêng Windows, tổng313; không gọi4 skipped là pass.

Suite launcher failed13/skipped10 là kết quả thật, **không phải N/N**. So failed/skipped theo tên ca cho cả hai chế độ auth; [delta](out/evidence/suite-delta-r4.json).

- `delta-none`: `{"new_failures": [], "removed_failures": [], "new_skips": []}`.
- `delta-fake`: `{"new_failures": [], "removed_failures": [], "new_skips": []}`.
- `delta-clear-trap`: `{"new_failures": [], "removed_failures": [], "new_skips": []}`.

## Diff và giới hạn chưa đo

- Diff đúng6 tệp/409 dòng thêm ≤450, đúng write set, không có `ops/handoff/*`. Chỉ rg.cai thay YAML; scripts/tl_selftest chỉ ratchet190→191 và chú thích. Manifest hash/size đúng gate strict. Delta từ lượt3 chỉ `.claude/dev/launcher_test.py`, không đổi runtime shell/YAML.
- Native Windows Git Bash, PowerShell, Windows mktemp/cygpath/PATHEXT/ACL và mutation floor Windows ≥70%: **KHÔNG ĐO ĐƯỢC** tại Linux. Stub/shape không thay workflow thật.
- `ci.yml` và `launcher-windows.yml workflow_dispatch` trên exact head, thread resolve và heartbeat/authority live: **not_run / không xác minh**, do lệnh review cấm mạng/GitHub. Không diễn giải review này thành đã thỏa M-2/M-3.
- 8 ca venv/pip offline +2 ca Windows bị skipped; 13 lỗi nền do /tmp/.git/EROFS được ghi đầy đủ trong output/delta, không sửa lỗi packet khác.
- Nội dung tấn công đường dẫn/thoát thư mục không được tự dựng. Phân tích chỉ ở mô tả: kết quả đường dẫn không được đánh giá lại thành lệnh; xác minh biên chứa/kênh nếu threat model mở rộng phải là packet riêng. Không lấy phần chưa đo làm pass.
- Kiểm cuối sau khi mọi tiến trình xong: fingerprint toàn bộ tệp/symlink (gồm Git metadata) không đổi: **cay-kho=[]; nen=[]**; head/tree và Git status sạch vẫn khớp neo ban đầu. [Integrity](out/evidence/source-integrity.json), [neo cuối](out/evidence/final-anchors.json).
