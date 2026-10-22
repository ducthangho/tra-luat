verdict: changes_requested
reviewed_head: ac4a6cb78a136b5e7f55abfac90b75ddd3cd080d
reviewed_sha: ac4a6cb78a136b5e7f55abfac90b75ddd3cd080d
reviewed_tree: e7ca9a3b5bc1f00c103f97b2bb9563ba2d9216a4
review_class: sensitive
provider: openai_codex
model: gpt-6.1-sol
model_family: openai
reasoning_effort: xhigh
execution_surface: codex_cli
transport: machine
review_round: 2/5

## Kết luận

**changes_requested — F868-01/02/03 ĐÓNG, F868-04 mới P2 và F868-05 mới P3 là khoảng trống test.** Head nguyên vẹn xử lý đúng các fault mới đã đo. Hai mutant nuốt lỗi ghi payload và một mutant nhận payload hỏng vẫn sống qua bộ ca liên quan lẫn toàn launcher suite, không có ca đỏ/bỏ qua mới so control. F868-04 cần bổ sung chốt hành vi trước khi approve. Không phát hiện P0/P1 hoặc lỗi runtime mới trên head nguyên vẹn trong phạm vi đã đo.

Selftest head đạt **1731/1731**, release strict **ok=true, expected=checked=191**. Các lỗi launcher chung nền/head được giữ nguyên trạng thái failed; không tính là hồi quy. Không cấp quyền merge/land/deploy, không gọi mạng/GitHub, không viết patch sản phẩm.

## Neo và môi trường

- HEAD thực tế `ac4a6cb78a136b5e7f55abfac90b75ddd3cd080d`, tree `e7ca9a3b5bc1f00c103f97b2bb9563ba2d9216a4`; base và merge-base với origin/master đều `9e9a74b2a396ef458d25c51a5563efafbb45ba0c`, base tree `9fc05c9986f711d1961e040dc7345850d0133294`.
- Spec đọc offline bằng `git -C cay-kho show origin/ops/wp868-spec:ops/specs/wp868.md`, SHA-256 **0d950c2b98b9e024bf1cc43a77c5d3351b5f4c21e6307b2e36ba9cdeca7b3f69**. Spec là nguồn tiêu chí; lease offline hạn 2026-10-24T06:52:00Z, M-1…M-5 được đọc nhưng không xác thực live. Handoff tại ref lease được giao **vắng, git show rc128**.
- Prompt snapshot và PROMPT.md cùng SHA-256 **7525b2cc9dfd23b4cd22ec8e8dbad8e5fea73636c25560735385dda1ee519c5b**. Đã đọc hai verdict #858 lượt 4/5 để giữ đúng bối cảnh F858-03 và F858-08.
- Run `d675fb8367d047419b1e6cf9e6be75bb`: header CLI công bố Codex **0.163.0**, model **gpt-6.1-sol**, effort **xhigh**, sandbox workspace-write, approval never. Đây là cấu hình CLI công bố, không phải phép chứng thực độc lập model phục vụ từng request. [Header](out/evidence/model-header.txt), [run metadata chọn trường](out/evidence/run-identity.json).
- Linux, Bash **5.2.21**, Python **3.13.16**, Git **2.43.0**. Ruff dùng cho delta là `python -m ruff` **0.17.1**; executable `ruff` trên PATH báo 0.16.9, chỉ được probe thông tin, không dùng tính delta. Actionlint **1.7.7** là ELF thật; ShellCheck thật vắng.
- `python -B out/review.py setup` dựng **cả head và base trong MỘT lệnh**, rồi dựng base-cross bằng cách chép launcher_test.py của head vào bản sao nền. Không hardlink, core.abbrev=7 trong Git config **local** (không ép qua env). Toàn bộ ca và mutant chạy dưới `out/`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=out/tmp`, `PIP_NO_INDEX=1`; không dùng auth thật. Hai lượt có auth dùng chuỗi giả `review-fixture-not-a-credential`. Selftest chỉ có command-config `commit.gpgsign=false`.
- `/tmp/.git` **rỗng, mount tmpfs ro mode=555**, `/var/tmp` trả EROFS trong sandbox. Không xoá marker/mount. Lỗi 11 ca r484 và hai ca t86/r858_goc_tam xuất hiện trên cả hai vế. Đã đo trường hợp marker rỗng ngay trong sandbox; **không** đo được vế xoá marker khi mount còn ro, hoặc trạng thái sau khi phiên Codex này kết thúc. [Runtime](out/evidence/runtime.stdout), [delta suite](out/evidence/suite-delta.json).

Diff thực tế **6 tệp / 332 dòng thêm / 93 xoá**, đúng write set, không `ops/handoff/*`; diff --check rc0. YAML chỉ đổi `rg.cai.*`; tiền tố cài của 15 công thức giữ nguyên. tl_selftest chỉ đổi ratchet/comment số tệp 190→191. [Audit](out/evidence/scope-audit.json), [neo](out/evidence/anchors.stdout).

## ĐỐI CHIẾU LƯỢT TRƯỚC

Hoàn tất trước khi săn mới. Verdict lượt 1 đọc qua ref lease, SHA-256 **0a2e05421e5f304331ca3eff2786bb2e4c05399d37886fd97db7ab0b4c9889b7** khớp. Witness/driver lượt 1 được chép sang `out/`; chỉ sửa parser readback để chấp nhận shell thoát trước khi in DICH. Không đổi fault cũ.

| Finding / mức / slug giữ nguyên | Trạng thái | Lệnh → output thật |
|---|---|---|
| F868-01 / P2 / `stdout-installer-bi-nhan-lam-ket-qua-chon` (kế thừa F858-03, đường lỗi đọc) | **ĐÓNG — ĐÃ VÁ THẬT** phạm vi reader đã báo | `python -B out/probes.py io-readback`: control rc0/DAT, DICH=ứng viên; cat giả rc74 ⇒ shell **rc7**, không DAT, alternative_probe_called=false, tmp_left=[]; kênh thật trước fault có DICH+LF+ứng viên. `python -B out/prior_check.py`: control pass, mutant `&&`→`;` **TinHieuChotCa**, rc0/xau_goi=True. |
| F868-02 / P2 / `fixture-khong-khoa-don-kenh-khi-thoat-loi` | **ĐÓNG — ĐÃ VÁ THẬT** test | `python -B out/mutations.py witnesses`: installer rc29, control tmp_left=[], mutant tắt EXIT trap còn cai_cong_cu.*. `prior_check.py`: control pass; **chính mutant cũ** tắt trap bị **TinHieuChotCa**, rc29/con=['cai_cong_cu.fqft3t']. Ca mới chứng minh kênh đã được tạo trước khi đòi nó được dọn. |
| F868-03 / P3 / `fixture-fallback-khong-khoa-crlf` | **ĐÓNG — ĐÃ VÁ THẬT** test | `mutations.py witnesses`: CRLF control **rc0/DAT**; chính mutant cũ bỏ cắt CR **rc2/DO**. `prior_check.py`: control pass; mutant bị **TinHieuChotCa**, `duong lui dong cuoi khong cat CR: rc=2`. |

[Readback](out/evidence/probe-io-readback.json), [witness/mutant cũ](out/evidence/custom-mutation-witnesses.json), [chốt từng finding](out/evidence/prior-check.json). **3/3 finding cũ được vá thật trong phạm vi gốc**; finding mới không tính vào tỷ lệ ấy. Cổng selftest lượt 1 chưa xong nay được đo với local core.abbrev: 1731/1731, không tái hiện lỗi driver 1730/1731.

## Finding mới

| ID / mức / slug lớp | Vị trí | Bằng chứng | Hướng xử lý bằng lời |
|---|---|---|---|
| **F868-04 — P2, test**; `fixture-khong-khoa-loi-ghi-payload-kenh` | `.claude/dev/launcher_test.py:8756`, `:8828`, `:8893`; guard phải bảo vệ ở `ops/cai_cong_cu.sh:46`, `:63` | Hai mutant ngoài DOT_BIEN_HOOK chỉ đổi return1→return0 tại lỗi printf ghi **GIU_PATH** hoặc **DICH**. Mỗi bản có cùng 27 ca liên quan PASS + một lỗi môi trường như control, không TinHieuChotCa; toàn launcher có cùng tập lỗi/bỏ qua như control. Witness printf rc74: head rc1, không chạy rg ở thư mục stdout; từng mutant **rc0/DAT**, alternative_probe_called=true. | Thêm hai fault-injection vào đúng payload producer và đối chứng không fault cùng sân. Đòi rc khác 0, không gọi probe của thư mục stdout; đăng ký hai mutant và buộc **TinHieuChotCa**. Bảo vệ cả GIU_PATH và DICH. **Không có bằng chứng cần sửa runtime head**. Rủi ro: stub chặn nhầm printf sentinel hoặc ghi GITHUB_PATH; chỉ fault đúng format payload, giữ N3 và bare-DAT bình thường. |
| **F868-05 — P3, test**; `fixture-khong-khoa-tu-choi-payload-kenh-hong` | `.claude/dev/launcher_test.py:8893`; guard ở `ops/cai_cong_cu.sh:145` | Mutant đổi exit7→exit0 tại nhánh payload hỏng sống qua cùng 27 ca và toàn launcher. Witness cat trả BAD_CHANNEL/rc0 riêng cho kênh, các tệp khác trong suốt: head **rc7**, mutant **rc0 nhưng không DAT/JSON**. | Thêm ca kênh không rỗng nhưng sai giao thức, đòi khác 0 và không chạy checker cuối; đăng ký mutant nhánh lỗi. Giữ đối chứng DICH/GIU_PATH/rỗng để không chặn fallback hợp lệ. **Không cần sửa runtime theo bằng chứng này**. Giữ P3 vì chưa chứng minh helper nguyên vẹn tạo payload hỏng trong vận hành thường. |

F868-04 là lớp **thiếu test ở producer ghi kênh**, phân biệt với lỗi runtime reader F868-01 đã vá và đã chạy lại witness cũ; không đổi tên để tuyên bố runtime F868-01 tái phát. F868-05 là lớp thiếu chốt tín hiệu thất bại cho payload hỏng. Không có quyết định chủ kho chấp nhận F868-04 trong dữ liệu được giao.

Các mutant đều nằm trong bản sao `out/mutants/`, không sửa test để giúp chúng sống. [Cặp neo/thay chính xác](out/evidence/extra-mutations.json), [driver](out/explore.py), [112 kết quả targeted](out/evidence/extra-targeted.json), [12 phép A/B fault/control](out/evidence/extra-witnesses.json), [assertion witness](out/evidence/extra-witness-chots.json). Các witness độc lập cho **9 pass và 3 TinHieuChotCa**; chỉ tính ba tín hiệu này là witness giết mutant. Không tính OSError môi trường là kill.

| Toàn launcher, cùng driver/env | Qua | Đã chạy | Tổng | Failed | Skipped | rc |
|---|---:|---:|---:|---:|---:|---:|
| `launcher-base-none` | 221 | 234 | 244 | 13 | 10 | 1 |
| `launcher-base-fake` | 221 | 234 | 244 | 13 | 10 | 1 |
| `launcher-head-none` | 228 | 241 | 251 | 13 | 10 | 1 |
| `launcher-head-fake` | 228 | 241 | 251 | 13 | 10 | 1 |
| `extra-full-swallow-channel-write` | 228 | 241 | 251 | 13 | 10 | 1 |
| `extra-full-swallow-keep-path-write` | 228 | 241 | 251 | 13 | 10 | 1 |
| `extra-full-accept-malformed-channel` | 228 | 241 | 251 | 13 | 10 | 1 |

**Delta failed mới nền→head = 0**, hai chế độ auth có cùng tập lỗi/bỏ qua. **Delta failed/bỏ qua mỗi mutant→head control = 0**. Đây là bằng chứng sống của mutant, không đổi các suite rc1 thành pass. Tập failed và skipped đầy đủ trong [suite-delta.json](out/evidence/suite-delta.json); stdout và argv/cwd/rc mỗi lượt ở `out/evidence/<tên>.{stdout,stderr,json}`.

## N1–N7: đối chiếu head và nền

Lệnh targeted chính xác cho từng ca: cwd `out/head` hoặc `out/base-cross`, `python -B .claude/dev/launcher_test.py --lap-ca TEN --lan 1`; `review.py targeted {head,base-cross}` chạy tất cả tên có tiền tố r868/r858/r831/r802. Mỗi tên, argv, cwd, rc, stdout/stderr thực được lưu riêng, không suy kết quả từ rc driver.

| Tiêu chí | Head / nền | Mutant và chốt thật |
|---|---|---|
| N1 kênh riêng | `r868_kenh_rieng_khong_doc_stdout_trinh_cai`: head 1/1, nền 0/1. Witness riêng chạy nguyên recipe Linux YAML qua script: (a) writer muộn **nền rc2/DO**, head rc0/DAT; (b) không LF **nền rc2/DO**, head rc0/DAT; (c) dòng cuối nền/head rc0/DAT. Installer không thấy KENH_KQ/TAM_CAI cả thường, bash -a và SHELLOPTS=allexport. | `wp868_sh_ham_in_stdout_thay_kenh`, `doc_stdout_thay_kenh`, `kenh_export`, `doc_kenh_nuot_loi`, `bo_trap_exit` đều có TinHieuChotCa. F868-04/05 bổ sung khoảng trống fault chưa bị bộ ca hiện có giết. |
| N2 không chờ stdout EOF | r868_writer… head 1/1; nền 0/1, giữ stdout **20.5s/rc2**. Phép riêng head shell xong 0.664–0.791s dù giữ stdout/stderr 3s. Bắt stderr bằng communicate còn chờ ~3.2–3.3s; shell đã thoát. | `wp868_sh_cho_eof_stdout` bị đúng ca N2 và shape giết. Không nhận xét này là bảo đảm caller bắt stderr luôn trở về ngay. |
| N3 không dùng helper | r868_khong_bo_chon_doc_dong_cuoi head/nền 1/1, gồm LF và CRLF. cong_cu_test head 61/61, precheck skip=0, không sửa test này. | `wp868_sh_bo_duong_lui_dong_cuoi` và `duong_lui_bo_cat_cr` bị ca hành vi và shape giết. |
| N4 rg chung helper | r802_bang_cai_rg_khop_cong_cu_yaml và các ca r802/r831 liên quan đều qua head/nền. Audit chỉ rg.cai thay đổi, giữ nguyên phần cài trước && đầu tiên của cả 15 công thức. | `wp868_yaml_rg_linux_ve_bo_chon_rieng` bị TinHieuChotCa; các mutant ứng viên winget/usrbin/brew đã đổi neo đều bị giết. |
| N5 khoá vòng duyệt | r868_vong_duyet_ung_vien head/nền 1/1; fixture có ứng viên tốt ở vị trí 3, vị trí 4 cũng tốt nhưng không được gọi. Nền đã có helper đúng hành vi; test mới để bảo vệ code đó. | `wp868_sh_chi_duyet_hai_ung_vien` và `wp868_sh_bo_break` đều bị đúng **r868_vong_duyet_ung_vien/TinHieuChotCa** giết, không chỉ shape. |
| N6 hồi quy #858 | Các ca r858 hành vi qua ở head; r858_goc_tam… đỏ giống nền vì EROFS /var/tmp. r858_bat_buoc_bash_khong_dua_rg_hong_len_dau qua cả hai. Batch độc lập 12 tổ hợp không rò temp. | Những mutant helper #858 giữ lại đều có kill thật trong strict hook audit; các mutant sentinel đổi neo sang GIU_PATH/kênh và vẫn bị ca hành vi giết. |
| N7 phát hành/selftest | Head selftest **1731/1731**, release strict **ok=true, 191=191**; nền selftest/release ghi trong bảng cổng. | Ratchet/manifest đo bằng gate trực tiếp; không biến một mutant shell thành bằng chứng kiểm release. Hai tệp gate này là output thẩm định N7. |

Bảng toàn bộ 28 ca mỗi vế:

| Tên ca (`--lap-ca TEN --lan 1`) | Head rc | Nền với test head rc | Phân loại |
|---|---:|---:|---|
| `r858_goc_tam_tranh_to_tien_co_git` | [1](out/evidence/target-head-r858_goc_tam_tranh_to_tien_co_git.stdout) | [1](out/evidence/target-base-cross-r858_goc_tam_tranh_to_tien_co_git.stdout) | EROFS môi trường cả hai, không pass/không kill |
| `r802_doctor_rg_tran_hong_la_BI_CHE` | [0](out/evidence/target-head-r802_doctor_rg_tran_hong_la_BI_CHE.stdout) | [0](out/evidence/target-base-cross-r802_doctor_rg_tran_hong_la_BI_CHE.stdout) | 1/1 cả hai |
| `r802_doctor_rg_chi_ban_tot_khong_BI_CHE` | [0](out/evidence/target-head-r802_doctor_rg_chi_ban_tot_khong_BI_CHE.stdout) | [0](out/evidence/target-base-cross-r802_doctor_rg_chi_ban_tot_khong_BI_CHE.stdout) | 1/1 cả hai |
| `r802_doctor_git_tran_hong_la_BI_CHE` | [0](out/evidence/target-head-r802_doctor_git_tran_hong_la_BI_CHE.stdout) | [0](out/evidence/target-base-cross-r802_doctor_git_tran_hong_la_BI_CHE.stdout) | 1/1 cả hai |
| `r802_doctor_bash_ngoai_pham_vi_BI_CHE` | [0](out/evidence/target-head-r802_doctor_bash_ngoai_pham_vi_BI_CHE.stdout) | [0](out/evidence/target-base-cross-r802_doctor_bash_ngoai_pham_vi_BI_CHE.stdout) | 1/1 cả hai |
| `r802_doctor_ten_tran_tu_muc_PATH_rong` | [0](out/evidence/target-head-r802_doctor_ten_tran_tu_muc_PATH_rong.stdout) | [0](out/evidence/target-base-cross-r802_doctor_ten_tran_tu_muc_PATH_rong.stdout) | 1/1 cả hai |
| `r802_cai_rg_windows_chon_ban_chay_duoc` | [0](out/evidence/target-head-r802_cai_rg_windows_chon_ban_chay_duoc.stdout) | [0](out/evidence/target-base-cross-r802_cai_rg_windows_chon_ban_chay_duoc.stdout) | 1/1 cả hai |
| `r802_cac_duong_dan_chi_trong_PATH_va_theo_PATHEXT` | [0](out/evidence/target-head-r802_cac_duong_dan_chi_trong_PATH_va_theo_PATHEXT.stdout) | [0](out/evidence/target-base-cross-r802_cac_duong_dan_chi_trong_PATH_va_theo_PATHEXT.stdout) | 1/1 cả hai |
| `r802_runner_tra_lai_con_tro_nguoi_goi` | [0](out/evidence/target-head-r802_runner_tra_lai_con_tro_nguoi_goi.stdout) | [0](out/evidence/target-base-cross-r802_runner_tra_lai_con_tro_nguoi_goi.stdout) | 1/1 cả hai |
| `r802_bang_cai_rg_khop_cong_cu_yaml` | [0](out/evidence/target-head-r802_bang_cai_rg_khop_cong_cu_yaml.stdout) | [0](out/evidence/target-base-cross-r802_bang_cai_rg_khop_cong_cu_yaml.stdout) | 1/1 cả hai |
| `r802_hook_linux_rg_hong_van_thu_cargo` | [0](out/evidence/target-head-r802_hook_linux_rg_hong_van_thu_cargo.stdout) | [0](out/evidence/target-base-cross-r802_hook_linux_rg_hong_van_thu_cargo.stdout) | 1/1 cả hai |
| `r802_hook_windows_khong_cai_in_dung_lenh` | [0](out/evidence/target-head-r802_hook_windows_khong_cai_in_dung_lenh.stdout) | [0](out/evidence/target-base-cross-r802_hook_windows_khong_cai_in_dung_lenh.stdout) | 1/1 cả hai |
| `r831_cai_rg_linux_chon_ban_chay_duoc` | [0](out/evidence/target-head-r831_cai_rg_linux_chon_ban_chay_duoc.stdout) | [0](out/evidence/target-base-cross-r831_cai_rg_linux_chon_ban_chay_duoc.stdout) | 1/1 cả hai |
| `r831_cai_rg_macos_chon_ban_chay_duoc` | [0](out/evidence/target-head-r831_cai_rg_macos_chon_ban_chay_duoc.stdout) | [0](out/evidence/target-base-cross-r831_cai_rg_macos_chon_ban_chay_duoc.stdout) | 1/1 cả hai |
| `r858_cai_linux_chon_ban_chay_duoc` | [0](out/evidence/target-head-r858_cai_linux_chon_ban_chay_duoc.stdout) | [0](out/evidence/target-base-cross-r858_cai_linux_chon_ban_chay_duoc.stdout) | 1/1 cả hai |
| `r858_cai_macos_chon_ban_chay_duoc` | [0](out/evidence/target-head-r858_cai_macos_chon_ban_chay_duoc.stdout) | [0](out/evidence/target-base-cross-r858_cai_macos_chon_ban_chay_duoc.stdout) | 1/1 cả hai |
| `r858_cai_windows_chon_ban_chay_duoc` | [0](out/evidence/target-head-r858_cai_windows_chon_ban_chay_duoc.stdout) | [0](out/evidence/target-base-cross-r858_cai_windows_chon_ban_chay_duoc.stdout) | 1/1 cả hai |
| `r858_cai_python_khong_in_thu_muc_ban_hong` | [0](out/evidence/target-head-r858_cai_python_khong_in_thu_muc_ban_hong.stdout) | [0](out/evidence/target-base-cross-r858_cai_python_khong_in_thu_muc_ban_hong.stdout) | 1/1 cả hai |
| `r858_bat_buoc_bash_khong_dua_rg_hong_len_dau` | [0](out/evidence/target-head-r858_bat_buoc_bash_khong_dua_rg_hong_len_dau.stdout) | [0](out/evidence/target-base-cross-r858_bat_buoc_bash_khong_dua_rg_hong_len_dau.stdout) | 1/1 cả hai |
| `r858_hinh_dang_cong_thuc_cai` | [0](out/evidence/target-head-r858_hinh_dang_cong_thuc_cai.stdout) | [1](out/evidence/target-base-cross-r858_hinh_dang_cong_thuc_cai.stdout) | phản chứng/contract mới đỏ trên nền; xem log |
| `r858_selftest_editskill_thu_muc_rieng` | [0](out/evidence/target-head-r858_selftest_editskill_thu_muc_rieng.stdout) | [0](out/evidence/target-base-cross-r858_selftest_editskill_thu_muc_rieng.stdout) | 1/1 cả hai |
| `r868_kenh_rieng_khong_doc_stdout_trinh_cai` | [0](out/evidence/target-head-r868_kenh_rieng_khong_doc_stdout_trinh_cai.stdout) | [1](out/evidence/target-base-cross-r868_kenh_rieng_khong_doc_stdout_trinh_cai.stdout) | phản chứng/contract mới đỏ trên nền; xem log |
| `r868_writer_muon_khong_lam_treo` | [0](out/evidence/target-head-r868_writer_muon_khong_lam_treo.stdout) | [1](out/evidence/target-base-cross-r868_writer_muon_khong_lam_treo.stdout) | phản chứng/contract mới đỏ trên nền; xem log |
| `r868_khong_bo_chon_doc_dong_cuoi` | [0](out/evidence/target-head-r868_khong_bo_chon_doc_dong_cuoi.stdout) | [0](out/evidence/target-base-cross-r868_khong_bo_chon_doc_dong_cuoi.stdout) | 1/1 cả hai |
| `r868_doc_kenh_hong_thi_dung` | [0](out/evidence/target-head-r868_doc_kenh_hong_thi_dung.stdout) | [1](out/evidence/target-base-cross-r868_doc_kenh_hong_thi_dung.stdout) | phản chứng/contract mới đỏ trên nền; xem log |
| `r868_don_kenh_khi_loi` | [0](out/evidence/target-head-r868_don_kenh_khi_loi.stdout) | [1](out/evidence/target-base-cross-r868_don_kenh_khi_loi.stdout) | nền không có kênh để đo cleanup; không kill |
| `r868_vong_duyet_ung_vien` | [0](out/evidence/target-head-r868_vong_duyet_ung_vien.stdout) | [0](out/evidence/target-base-cross-r868_vong_duyet_ung_vien.stdout) | 1/1 cả hai |
| `r868_hinh_dang_kenh_ket_qua` | [0](out/evidence/target-head-r868_hinh_dang_kenh_ket_qua.stdout) | [1](out/evidence/target-base-cross-r868_hinh_dang_kenh_ket_qua.stdout) | nền ValueError substring not found: thiếu kiến trúc, không kill |

Không tính ValueError của shape nền hoặc ca cleanup không dựng được trên nền là mutation kill. (a)(b) N1 được chạy riêng để ca (a) đỏ không che việc chưa chạy (b).

## Hướng săn độc lập

| Hướng | Giả thuyết | Lệnh đã chạy | Output thật rút gọn | Kết luận |
|---|---|---|---|---|
| 1. Đối chiếu read/cleanup/CRLF | Bản sửa chỉ làm shape xanh, witness cũ vẫn lọt. | `probes.py io-readback`; `mutations.py witnesses`; `prior_check.py` | Fault reader rc7; 3 control pass, 3 mutant cũ TinHieuChotCa; control cleanup tmp_left=[] và CRLF rc0. | **KHÔNG PHẢI LỖI** phạm vi ba finding cũ. |
| 2. Stdout và export | Log muộn/thiếu LF hoặc allexport đổi DICH. | `python -B out/probes.py channel` | Nền (a)(b) rc2, head cả ba kiểu rc0/DAT; ba mode installer thấy ABSENT ABSENT. | **KHÔNG PHẢI LỖI** trên head ở chiều đã đo. |
| 3. Batch/trap | Source chung shell ghi đè trap, rò kênh hay dùng kênh cũ. | `python -B out/probes.py batch` | 12 tổ hợp hai thứ tự rg/bash × thành công/lỗi × thường/bash-a/SHELLOPTS; thành công rc0, lỗi bash rc23, tất cả tmp_left=[], không thấy biến kênh. | **KHÔNG PHẢI LỖI**. |
| 4. Errexit | `(set +e; eval)` nuốt lỗi recipe so với nền. | `python -B out/probes.py failures` | Cả nền/head: installer rc29, checker rc1, `false; echo uv` rc0/DAT (cùng ngữ nghĩa cũ). | **KHÔNG PHẢI LỖI** ở ba chiều, không suy mọi cú pháp shell đều đã đo. |
| 5. Giữ stdout/stderr | Reader hoặc shell còn chờ EOF writer nền. | `python -B out/probes.py streams` | Cả ba shell rc0/DAT, thoát 0.664–0.791s; stdout-only communicate 0.730s; stderr/both communicate 3.200/3.318s. | **KHÔNG PHẢI LỖI N2 của shell**; caller bắt stderr còn chờ. |
| 6. Windows rg/GITHUB_PATH | Bỏ rg.exe filter làm mất chọn đúng hoặc ghi PATH sai. | `python -B out/probes.py windows` | 8 chiều: links/choco DAT; hết ứng viên rc1; bare DAT không ghi GP; GP rỗng/vắng vẫn DAT; -u/-w lỗi rc1. Mô phỏng đổi V:→Unix và -w→W: rõ ràng. | **KHÔNG PHẢI LỖI** trong mô phỏng; native Git Bash/mktemp/cygpath **KHÔNG ĐO ĐƯỢC**. |
| 7. Q4/chốt cũ/phạm vi | Đổi kiến trúc làm mất ca hoặc bỏ mutation hữu ích. | `python -B out/audit.py`; `python -B out/strict_mutations.py` | 0 ca/hàm mất, 5 mutant YAML bỏ, hook tổng30→36; 20 control pass/68 TinHieuChotCa, 0 tín dụng giả. Prefix cài giữ15/15. | **KHÔNG PHẢI LỖI** qua audit và đo hành vi; handoff giải trình Q4 vắng, chưa kiểm được. |
| 8. Lỗi ghi payload | Test không thấy nuốt lỗi producer, kênh rỗng kích hoạt fallback stdout. | `explore.py setup`; `targeted`; `witnesses`; `full swallow-channel-write`; `full swallow-keep-path-write`; `assess_witnesses.py` | Hai mutant chỉ đổi return; suite delta failed/skipped=0; head fault rc1, mutant rc0/DAT/alternative=true; witness mới TinHieuChotCa. | **LỖI test F868-04**; runtime head từ chối đúng. |
| 9. Payload sai giao thức | Nhánh lỗi bị đổi thành rc0 mà suite không nhận. | `explore.py targeted`; `witnesses`; `full accept-malformed-channel`; `assess_witnesses.py` | Mutant sống toàn suite, head BAD_CHANNEL rc7, mutant rc0/không DAT; witness mới TinHieuChotCa. | **LỖI test F868-05**, P3. |
| 10. Marker Git rỗng | Lỗi r484 do head thay vì marker rỗng trong sandbox. | `extra_gates.py` runtime + `review.py suites` | `/tmp/.git` rỗng/ro; 11 r484 + t86/r858_goc_tam đỏ cùng tên ở nền/head, auth giả không đổi. | **KHÔNG PHẢI hồi quy wp868**; không đo được xoá mount/sau khi phiên kết thúc. |

Headline `DOT BIEN: 302/302` (nền296/296) là output thật của công cụ, không tự chứng minh mọi mutant launcher có kill hợp lệ khi control đang đỏ môi trường. Bằng chứng kill được kiểm riêng ở đây là **36 DOT_BIEN_HOOK/68 TinHieuChotCa** thuộc phạm vi patch; không lấy lỗi r484/t86/gốc tạm làm tín dụng.

## Q4: các mutant cũ bị đổi/bỏ

Năm mutant YAML bị bỏ là `wp802_yaml_chon_ung_vien_chi_theo_ma_thoat`, `wp802_yaml_khong_ghi_github_path`, `wp831_yaml_linux_chi_theo_ma_thoat`, `wp831_yaml_macos_bo_kiem_thuc_thi`, `wp831_yaml_linux_ghi_github_path_vo_dieu_kien`. Chức năng kiểm chuẩn/rc, ghi GITHUB_PATH, bare-DAT chuyển sang helper dùng chung; mutant helper tương ứng vẫn bị các ca r858 hành vi giết. Ca r802 Windows và r831 Linux/macOS cũng chạy recipe rg nguyên văn qua script và qua trên head. Guard `-x` được thay bằng checker thực, hợp đồng Q4 bare DAT đo rc0/DAT + GP rỗng, không còn đo stdout thư mục. Những sentinel mutant #858 chuyển sang GIU_PATH/kênh vẫn có kill hành vi, không nhận tên mutant không đổi là bằng chứng tự thân. Chưa xác nhận lời giải thích trong handoff vì ref được cấp thiếu tệp ấy.

## Bảng lệnh → kết quả thật

Mặc định lệnh sản phẩm cwd `out/head`, môi trường như trên. `run` lưu argv/cwd/rc/thời lượng vào JSON; rc0 của driver không thay rc con.

| Lệnh | Kết quả thật |
|---|---|
| `python -B out/review.py setup` | rc0, dựng cả hai vế trong cùng invocation, base-cross dùng test head. |
| `git -C cay-kho diff --numstat 9e9a74b HEAD`; `diff --check` | 6 tệp/332 thêm/93 xoá; check rc0/output rỗng; diff.patch được cấp khớp diff thực. |
| `python -B out/review.py targeted head`; `targeted base-cross` | Head 27/28 rc0; nền21/28 rc0. Kết quả từng tên ở bảng trên; tách lỗi môi trường/setup khỏi phản chứng hành vi. |
| `python -B out/review.py suites` | Bốn suite đã kết thúc; số liệu thật trong bảng launcher. Failed và skipped không coi là pass. |
| `python -B .claude/dev/launcher_test.py --dot-bien`, head | rc0; `DOT BIEN: 302/302 dat  (4 khong do duoc tren nen nay)`. [log](out/evidence/mutation.stdout) |
| `python -B .claude/dev/launcher_test.py --dot-bien`, base | rc0; `DOT BIEN: 296/296 dat  (4 khong do duoc tren nen nay)`. [log](out/evidence/mutation-base.stdout) |
| `python -B out/strict_mutations.py` | 36 hook mutant, 20 control PASS, 68 TinHieuChotCa, 0 invalid-credit/skip/survived. N5 và các mutant F868-01/02/03 có kill đúng ca hành vi. Riêng mutant gốc tạm trong DOT_BIEN thường không được nhận tín dụng khi control lỗi môi trường. |
| `python -B scripts/tl.py --selftest`, head | rc0; `== tl selftest 1731/1731 ==`. [log](out/evidence/selftest.stdout) |
| `python -B scripts/tl.py --selftest`, base | rc0; `== tl selftest 1731/1731 ==`. [log](out/evidence/selftest-base.stdout) |
| `python -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`, head | rc0; ok=true, expected=191, checked=191, errors=[]. [log](out/evidence/release.stdout) |
| `python -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`, base | rc0; ok=true, expected=190, checked=190, errors=[]. [log](out/evidence/release-base.stdout) |
| `CONG_CU_TEST_BAN_KINH=manh python -B ops/cong_cu_test.py` | rc0; cong_cu_test: 61/61 đạt; tổng=61, bỏ qua=0, tiền kiểm bỏ qua=0 / SỐ LIỆU: ca=61 · đột biến=470 (giao mảnh) · lỗi đột biến=0 · tiền kiểm bỏ qua=0 · cổng cây thật=ĐẠT. [log](out/evidence/congcu-gate.stdout) |
| `python -B ops/cong_cu_test.py` mặc định | **cancelled/SIGINT, session rc130**, sau khi in61/61/cổng cây thật ĐẠT, chưa có kết luận cuối; không coi là pass. Dùng cổng CI `BAN_KINH=manh` ở hàng trên để hoàn tất bộ ca và tự kiểm. Không đo 470 bán kính mutant của ops/cong_cu_test; khác bộ launcher --dot-bien đã hoàn tất. |
| `bash -n ops/cai_cong_cu.sh` | rc0/output rỗng. |
| `actionlint`, nền/head | cả hai rc0/output rỗng, không thêm finding; không có ShellCheck thật nên không chứng nhận lớp SC*. |
| `python -B -m ruff check --no-cache --select F --output-format json scripts/tl.py scripts/tl_selftest.py .claude/dev/launcher_test.py`, nền/head | Cả hai rc1, 4409 finding; Counter(path/code/message/column) delta thêm/xoá=0. Không nhận là lint sạch tuyệt đối. |
| `python -B .claude/dev/packet_loop.py doctrine-scan --root .` | rc0, sạch, 10 tệp/0 hit. |
| `python -B scripts/tl.py doc-claims-check --strict --json` | rc0/ok=true; 396 advisory, không lỗi cứng. |
| `python -B out/audit.py` | rc0, đúng scope; ASTfunctions322→330, @ca244→251, bang819→835, assert85→85, không mất ca/hàm. |
| `python -B out/review.py integrity` | rc0; hash tất cả tệp/symlink (gồm Git metadata) của cay-kho/nen bằng mốc setup, delta=[]/[]; các cây nguồn vẫn đúng HEAD/tree. |
| `python -B out/final_report.py` | rc0; kiểm dữ liệu cuối và ghi verdict cùng suite-delta. Không có gate đang chạy được nhận là đã pass. |

## Không đo được

- Native Windows/macOS, Git Bash/MSYS, PATHEXT/rg.exe, mktemp và cygpath thật, installer thật. Tất cả các chiều Windows/macOS trong local fixture chỉ là mô phỏng Linux. Chưa xác nhận sàn mutation Windows ≥70%.
- Check runs ci.yml/launcher-windows.yml, thread resolution M-2, live heartbeat/lease/authorization M-3. Không gọi mạng/GitHub theo assignment. Không suy từ cổng local thành quyền merge/land/deploy.
- 10 ca launcher skipped (8 venv/pip offline, 2 Windows), 13 failed môi trường chung hai vế; danh sách đầy đủ trong suite-delta. Không tính failed/skipped là N/N launcher, không dùng chúng làm finding hồi quy wp868.
- Vế xoá `/tmp/.git` rỗng hoặc đo sau khi chính phiên Codex này kết thúc: marker đang mount ro. Chỉ chứng minh marker rỗng vẫn đi kèm tập lỗi chung; không nhận kết luận của executor là phép A/B của reviewer.
- 4 mutation launcher không đo được trên nền này, 470 bán kính cong_cu_test giao CI theo chế độ gate, ShellCheck thật vắng. Kết quả302/302 của launcher không thay kết quả native Windows hoặc bộ bán kính470.
- Giải trình Q4 và hint provenance trong handoff không đọc được từ ref lease được cấp (rc128); không tự bổ sung hoặc suy lời giải thích đã tồn tại.
- Python theo PATH vẫn là nợ ngoài phạm vi packet; không thay ops/cong_cu.py/cai_actionlint.sh/cong_cu_test.py. Các khả năng cần nội dung tấn công đường dẫn/thoát thư mục không được dựng; chỉ nên mô tả bằng lời theo assignment.

Snapshot toàn vẹn chỉ chứng minh không có delta giữa hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Tất cả sản phẩm review, fixture và mutant đặt dưới out/ hoặc VERDICT.md; không commit/push/merge/land/deploy. Danh mục băm verdict/driver/evidence: [SHA256SUMS](out/SHA256SUMS).
