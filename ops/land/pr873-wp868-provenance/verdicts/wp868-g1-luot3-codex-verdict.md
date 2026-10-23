verdict: changes_requested
reviewed_head: 93d33b406d596b7245c69aa0a1fe80cf7e49748e
reviewed_sha: 93d33b406d596b7245c69aa0a1fe80cf7e49748e
reviewed_tree: a57adffacfb3666c2953dff6331c4a68905cc542
review_class: sensitive
provider: openai_codex
model: gpt-6.1-sol
model_family: openai
reasoning_effort: xhigh
execution_surface: codex_cli
transport: machine
review_round: 3/5

## Kết luận

**changes_requested — F868-01/02/03/04/05 ĐÓNG; còn F868-06 mới P3 về độ phủ allexport. Không có P0/P1/P2 mở được xác nhận.** Head runtime nguyên vẹn xử lý đúng các fault đã đo; không yêu cầu vá runtime theo finding mới này.

**P3 có chặn approve ở lượt này theo M-1:** lease yêu cầu P2/P3 còn mở phải có quyết định chủ kho có link. Dữ liệu offline được giao chưa có quyết định cho F868-06, nên chưa approve. Có thể đóng bằng test/mutation hoặc quyết định chấp nhận rõ finding này; không cần tự động mở thêm vòng chỉ vì một P3, và không chuyển quyết định chấp nhận nợ #858 sang F868-06.

Head selftest **1731/1731**; release strict **ok=true, expected=checked=191**; congcu theo chế độ CI **61/61**, không bỏ qua. Launcher có **0 ca đỏ mới** trên cả hai chế độ auth; 13 lỗi/10 bỏ qua chung nền và head vẫn ghi failed/skipped. Không gọi mạng/GitHub, không ghi cây nguồn, không viết patch sản phẩm và không cấp quyền merge/land/deploy.

## Neo và môi trường

- HEAD/tree đúng header; base và merge-base với origin/master `9e9a74b2a396ef458d25c51a5563efafbb45ba0c`, base tree `9fc05c9986f711d1961e040dc7345850d0133294`. Hai cây nguồn sạch khi bắt đầu; fingerprint mọi tệp/symlink, gồm Git metadata/ignored/untracked, không đổi cuối lượt: `cay-kho=[]`, `nen=[]`. [Integrity](out/evidence/source-integrity.json), [neo cuối](out/evidence/final-anchors.json).
- Snapshot bằng byte với PROMPT.md. Spec đọc offline từ ref được giao, SHA-256 **0d950c2b98b9e024bf1cc43a77c5d3351b5f4c21e6307b2e36ba9cdeca7b3f69**; verdict lượt2 **667af2a30eafeb57fb29ff594c578f46ca8f275e7deca1dc718f7195d55207d8**; handoff **ea1c692b74a442390696002dfac83a7abeb02a454f3060f864211a1fd3f48fa6**, đều khớp. Đã đọc verdict lượt1 và #858 lượt4/5. [Spec](out/spec.md), [lease M-1…M-5](out/lease.md), [prior2](out/prior2.md), [handoff](out/handoff.md).
- Lease offline hết hạn 2026-10-24T06:52:00Z, generation1, sensitive; không xác nhận heartbeat/authority live. Diff so lượt2 chỉ `.claude/dev/launcher_test.py`; shell/YAML runtime không đổi.
- Run `1f61bfda29944082a1e2a14082930171`: CLI công bố Codex **0.163.0**, model **gpt-6.1-sol**, effort **xhigh**, sandbox workspace-write, approval never. Đây là cấu hình CLI công bố, không chứng thực model phục vụ từng request. [Header](out/evidence/model-header.txt).
- Linux/Bash **5.2.21**, Python **3.13.16**, Git **2.43.0**; `core.abbrev=7` local ở các bản sao. `python -m ruff` **0.17.1** dùng cho bare lint; actionlint thật **1.7.7**. [Runtime](out/evidence/runtime.stdout), [tool audit](out/evidence/scope-audit.json).
- `PYTHONDONTWRITEBYTECODE=1 python3 -B out/review.py setup` dựng **cả head/base trong MỘT lệnh**, sao chép thường, không hardlink; dựng base-cross bằng cách chép test head vào nền. Chỉ chạy trên bản sao/fixture/mutant trong `out/`. Env dùng `PIP_NO_INDEX=1`, `TMPDIR=out/tmp`, signing command-config=false; không dùng auth thật. Hai vế fake dùng chuỗi giả `review-fixture-not-a-credential`.
- `/tmp/.git` rỗng là tmpfs **ro mode555**; `/var/tmp` trả EROFS trong sandbox. Không xoá marker/mount. `t86`, `r858_goc_tam` và 11 `r484_*` lỗi cả nền/head; không tính là hồi quy. Mỗi subprocess có argv/cwd/env override/rc trong `out/evidence/<tên>.json` và stdout/stderr tương ứng.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đã làm **trước săn mới**. Sao chép witness/driver của lượt2 vào out/, dùng head hiện tại; không sử dụng kết quả lượt2 như kết quả chạy mới. [Toàn lệnh/output](out/prior-rerun.log), [assertion trực tiếp](out/evidence/prior-check.json), [witness cũ](out/evidence/extra-witnesses.json).

| Finding / mức / slug giữ nguyên | Trạng thái và bằng chứng lượt3 |
|---|---|
| F868-01 / P2 / `stdout-installer-bi-nhan-lam-ket-qua-chon` | **ĐÓNG — ĐÃ VÁ THẬT.** `probes.py io-readback`: control rc0/DAT, DICH=ứng viên; cat rc74 trên kênh → rc7, không DAT, không probe thư mục stdout, tmp_left=[]. `prior_check.py`: mutant reader `&&`→`;` bị **TinHieuChotCa**, rc0/xau_goi=True. |
| F868-02 / P2 / `fixture-khong-khoa-don-kenh-khi-thoat-loi` | **ĐÓNG — ĐÃ VÁ THẬT.** Control ca cleanup pass; mutant cũ tắt trap EXIT bị **TinHieuChotCa**: installer rc29, còn thư mục kênh. Ca mới batch và mutant bỏ rm tường minh cũng có kill thật trong strict hook audit. |
| F868-03 / P3 / `fixture-fallback-khong-khoa-crlf` | **ĐÓNG — ĐÃ VÁ THẬT.** Control fallback LF/CRLF pass; mutant cũ bỏ cắt CR bị **TinHieuChotCa**, `duong lui dong cuoi khong cat CR: rc=2`. |
| F868-04 / P2 / `fixture-khong-khoa-loi-ghi-payload-kenh` | **ĐÓNG — ĐÃ VÁ THẬT.** Cả hai mutant cũ return1→return0 của GIU_PATH/DICH bị `r868_ghi_kenh_hong_thi_dung` giết bằng **TinHieuChotCa**. Output thật: `GIU_PATH/DICH: ghi kenh hong ma van chay tiep: rc=0 xau_goi=True`, stderr có fault printf. Witness head khi fault rc1/không DAT/không probe stdout. Control CLI ca mới **2/2**, mutant CLI **0/1** từng nhánh. |
| F868-05 / P3 / `fixture-khong-khoa-tu-choi-payload-kenh-hong` | **ĐÓNG — ĐÃ VÁ THẬT.** Witness BAD_CHANNEL: head rc7, mutant exit0 cho rc0/không DAT. Ca mới có biến thể rac: control **2/2**, mutant **0/1**, message `kenh rac ma van chay tiep: rc=0 xau_goi=False`. Strict audit xác nhận **TinHieuChotCa**. |

Không thay slug/ID để xoá lịch sử. Lớp F868-01 giữ liên hệ F858-03 ở nhánh reader lỗi; F868-06 dưới đây là thiếu phép đo môi trường allexport, không phải chứng minh lỗi reader/runtime F868-01 tái phát.

## Finding

| ID / mức / slug lớp | Vị trí | Bằng chứng | Hướng xử lý bằng lời |
|---|---|---|---|
| **F868-06 / P3 / `fixture-kenh-rieng-chua-khoa-allexport`** — một lớp, hai biểu hiện KENH_KQ và TAM_CAI | `.claude/dev/launcher_test.py:8756` (ca N1), `:8933` (shape); tính chất runtime được bảo vệ ở `ops/cai_cong_cu.sh:123` và `:126` | Hai mutant ngoài bảng, mỗi bản chỉ thêm phép gán lại một biến sau declare+x. Cả hai sống qua **28 ca liên quan pass + 1 lỗi setup môi trường**, không TinHieuChotCa. Mutant KENH_KQ sống cả **toàn launcher 229/242, failed13/skipped10**, delta lỗi/bỏ qua so control head=0. Witness riêng: normal control/mutant pass; **bash -a và SHELLOPTS=allexport** cho control ABSENT/ABSENT, nhưng mỗi mutant lộ đúng biến và bị witness **TinHieuChotCa**. Head nguyên vẹn vẫn riêng ở cả ba chế độ. | Mở rộng ca N1 để đo cả normal, bash-a và SHELLOPTS, xác nhận installer không thấy **cả hai biến**; thêm hai mutant gán lại sau declare+x và yêu cầu kill bằng TinHieuChotCa. Giữ đối chứng không fault cùng sân. Không cần vá runtime theo bằng chứng hiện có. Rủi ro sửa test: đừng bật allexport cho toàn harness hoặc che lỗi setup; bảo đảm phép gán không bị môi trường fixture lọc đi. Giữ P3 vì chỉ thiếu độ phủ, chưa có lỗi runtime head. |

**M-1 chặn approve khi P3 này còn mở và chưa có quyết định chủ kho có link.** Không có P0/P1/P2 mở; không nâng thiếu test này thành lỗi runtime. Quyết định chấp nhận của packet khác không áp dụng tự động.

[Ba cặp neo/thay nguyên văn](out/evidence/new-mutations.json), [116 kết quả targeted](out/evidence/new-targeted.json), [14 witness/control](out/evidence/new-witnesses.json), [toàn suite mutant](out/evidence/new-full-channel.stdout), [delta suite](out/evidence/suite-delta-r3.json). Witness dùng `bang()` của chính module để đếm TinHieuChotCa; lỗi môi trường không được tính kill.

## N1–N7

Mỗi ca chạy CLI thật ở **cả** out/head và out/base-cross: `python3 -B .claude/dev/launcher_test.py --lap-ca TEN --lan 1`, cùng env. `out/review.py targeted {head,base-cross}` lưu riêng lệnh/rc/output mỗi ca. Test head có **29 ca** trong bốn nhóm r868/r858/r831/r802; head **28 qua, 1 lỗi môi trường**; nền với test head **21 qua, 8 đỏ**, gồm các ca không dựng được khi nền chưa có kiến trúc kênh.

| Tiêu chí | Phản chứng nền/head và mutation |
|---|---|
| N1 kênh riêng | `r868_kenh_rieng_khong_doc_stdout_trinh_cai` head1/1, nền0/1. Phép riêng `probes.py channel` chạy (a)(b)(c) độc lập: **(a) writer muộn nền rc2/DO, head rc0/DAT; (b) không LF nền rc2/DO, head rc0/DAT; (c) dòng cuối nền/head rc0/DAT**. Writer đã ghi marker; head nhận đúng ứng viên. Các mutant producer/reader/export/read-error có TinHieuChotCa; F868-06 chỉ giới hạn độ phủ allexport. |
| N2 không treo stdout | `r868_writer_muon_khong_lam_treo`: head1/1, nền0/1 với **20.3s/rc2**. Mutant `wp868_sh_cho_eof_stdout` bị ca hành vi và shape giết. Phép giữ stderr không làm shell chờ nhưng caller capture stderr còn đợi EOF, xem hướng5. |
| N3 không gọi helper | `r868_khong_bo_chon_doc_dong_cuoi` cả hai1/1, gồm LF/CRLF. congcu-ci61/61, không sửa cong_cu_test/actionlint script. Mutant bỏ fallback/bỏ cắt CR bị đúng ca hành vi và shape giết. |
| N4 rg chung helper | r802_bang_cai_rg_khop_cong_cu_yaml và các ca chọn rg r802/r831 qua cả hai. YAML chỉ đổi rg.cai, giữ tiền tố cài của cả15 recipe. Mutant rg quay bộ chọn riêng và các mutant ứng viên usrbin/brew/winget bị TinHieuChotCa. |
| N5 vòng duyệt | r868_vong_duyet_ung_vien qua cả hai; tốt ở vị trí3, vị trí4 không được probe. Hai mutant chỉ duyệt2/bỏ break bị **chính ca hành vi** giết, không chỉ shape. |
| N6 hồi quy858 | Mọi ca hành vi r858 qua head trừ r858_goc_tam EROFS chung nền. r858_bat_buoc_bash_khong_dua_rg_hong_len_dau qua cả hai; các mutant GIU_PATH/đọc stdout lại bị ca N4 này giết. Không đánh đồng lỗi EROFS nền với hồi quy. |
| N7 release/selftest | Head selftest **1731/1731, rc0**; release strict **ok=true, expected_file_count=checked_file_count=191**, package hash khớp. Không lấy mutation shell làm bằng chứng release; N7 đo trực tiếp bằng hai gate này. |

Bảng toàn bộ ca (rc1 ở nền không mặc nhiên là mutation kill):

| Ca | Head rc | Nền + test head rc | Phân loại nếu đỏ |
|---|---:|---:|---|
| `r858_goc_tam_tranh_to_tien_co_git` | [1](out/evidence/target-head-r858_goc_tam_tranh_to_tien_co_git.stdout) | [1](out/evidence/target-base-cross-r858_goc_tam_tranh_to_tien_co_git.stdout) | EROFS môi trường cả hai; không pass/kill |
| `r802_doctor_rg_tran_hong_la_BI_CHE` | [0](out/evidence/target-head-r802_doctor_rg_tran_hong_la_BI_CHE.stdout) | [0](out/evidence/target-base-cross-r802_doctor_rg_tran_hong_la_BI_CHE.stdout) |  |
| `r802_doctor_rg_chi_ban_tot_khong_BI_CHE` | [0](out/evidence/target-head-r802_doctor_rg_chi_ban_tot_khong_BI_CHE.stdout) | [0](out/evidence/target-base-cross-r802_doctor_rg_chi_ban_tot_khong_BI_CHE.stdout) |  |
| `r802_doctor_git_tran_hong_la_BI_CHE` | [0](out/evidence/target-head-r802_doctor_git_tran_hong_la_BI_CHE.stdout) | [0](out/evidence/target-base-cross-r802_doctor_git_tran_hong_la_BI_CHE.stdout) |  |
| `r802_doctor_bash_ngoai_pham_vi_BI_CHE` | [0](out/evidence/target-head-r802_doctor_bash_ngoai_pham_vi_BI_CHE.stdout) | [0](out/evidence/target-base-cross-r802_doctor_bash_ngoai_pham_vi_BI_CHE.stdout) |  |
| `r802_doctor_ten_tran_tu_muc_PATH_rong` | [0](out/evidence/target-head-r802_doctor_ten_tran_tu_muc_PATH_rong.stdout) | [0](out/evidence/target-base-cross-r802_doctor_ten_tran_tu_muc_PATH_rong.stdout) |  |
| `r802_cai_rg_windows_chon_ban_chay_duoc` | [0](out/evidence/target-head-r802_cai_rg_windows_chon_ban_chay_duoc.stdout) | [0](out/evidence/target-base-cross-r802_cai_rg_windows_chon_ban_chay_duoc.stdout) |  |
| `r802_cac_duong_dan_chi_trong_PATH_va_theo_PATHEXT` | [0](out/evidence/target-head-r802_cac_duong_dan_chi_trong_PATH_va_theo_PATHEXT.stdout) | [0](out/evidence/target-base-cross-r802_cac_duong_dan_chi_trong_PATH_va_theo_PATHEXT.stdout) |  |
| `r802_runner_tra_lai_con_tro_nguoi_goi` | [0](out/evidence/target-head-r802_runner_tra_lai_con_tro_nguoi_goi.stdout) | [0](out/evidence/target-base-cross-r802_runner_tra_lai_con_tro_nguoi_goi.stdout) |  |
| `r802_bang_cai_rg_khop_cong_cu_yaml` | [0](out/evidence/target-head-r802_bang_cai_rg_khop_cong_cu_yaml.stdout) | [0](out/evidence/target-base-cross-r802_bang_cai_rg_khop_cong_cu_yaml.stdout) |  |
| `r802_hook_linux_rg_hong_van_thu_cargo` | [0](out/evidence/target-head-r802_hook_linux_rg_hong_van_thu_cargo.stdout) | [0](out/evidence/target-base-cross-r802_hook_linux_rg_hong_van_thu_cargo.stdout) |  |
| `r802_hook_windows_khong_cai_in_dung_lenh` | [0](out/evidence/target-head-r802_hook_windows_khong_cai_in_dung_lenh.stdout) | [0](out/evidence/target-base-cross-r802_hook_windows_khong_cai_in_dung_lenh.stdout) |  |
| `r831_cai_rg_linux_chon_ban_chay_duoc` | [0](out/evidence/target-head-r831_cai_rg_linux_chon_ban_chay_duoc.stdout) | [0](out/evidence/target-base-cross-r831_cai_rg_linux_chon_ban_chay_duoc.stdout) |  |
| `r831_cai_rg_macos_chon_ban_chay_duoc` | [0](out/evidence/target-head-r831_cai_rg_macos_chon_ban_chay_duoc.stdout) | [0](out/evidence/target-base-cross-r831_cai_rg_macos_chon_ban_chay_duoc.stdout) |  |
| `r858_cai_linux_chon_ban_chay_duoc` | [0](out/evidence/target-head-r858_cai_linux_chon_ban_chay_duoc.stdout) | [0](out/evidence/target-base-cross-r858_cai_linux_chon_ban_chay_duoc.stdout) |  |
| `r858_cai_macos_chon_ban_chay_duoc` | [0](out/evidence/target-head-r858_cai_macos_chon_ban_chay_duoc.stdout) | [0](out/evidence/target-base-cross-r858_cai_macos_chon_ban_chay_duoc.stdout) |  |
| `r858_cai_windows_chon_ban_chay_duoc` | [0](out/evidence/target-head-r858_cai_windows_chon_ban_chay_duoc.stdout) | [0](out/evidence/target-base-cross-r858_cai_windows_chon_ban_chay_duoc.stdout) |  |
| `r858_cai_python_khong_in_thu_muc_ban_hong` | [0](out/evidence/target-head-r858_cai_python_khong_in_thu_muc_ban_hong.stdout) | [0](out/evidence/target-base-cross-r858_cai_python_khong_in_thu_muc_ban_hong.stdout) |  |
| `r858_bat_buoc_bash_khong_dua_rg_hong_len_dau` | [0](out/evidence/target-head-r858_bat_buoc_bash_khong_dua_rg_hong_len_dau.stdout) | [0](out/evidence/target-base-cross-r858_bat_buoc_bash_khong_dua_rg_hong_len_dau.stdout) |  |
| `r858_hinh_dang_cong_thuc_cai` | [0](out/evidence/target-head-r858_hinh_dang_cong_thuc_cai.stdout) | [1](out/evidence/target-base-cross-r858_hinh_dang_cong_thuc_cai.stdout) | phản chứng/hợp đồng mới đỏ nền; xem log |
| `r858_selftest_editskill_thu_muc_rieng` | [0](out/evidence/target-head-r858_selftest_editskill_thu_muc_rieng.stdout) | [0](out/evidence/target-base-cross-r858_selftest_editskill_thu_muc_rieng.stdout) |  |
| `r868_kenh_rieng_khong_doc_stdout_trinh_cai` | [0](out/evidence/target-head-r868_kenh_rieng_khong_doc_stdout_trinh_cai.stdout) | [1](out/evidence/target-base-cross-r868_kenh_rieng_khong_doc_stdout_trinh_cai.stdout) | phản chứng/hợp đồng mới đỏ nền; xem log |
| `r868_writer_muon_khong_lam_treo` | [0](out/evidence/target-head-r868_writer_muon_khong_lam_treo.stdout) | [1](out/evidence/target-base-cross-r868_writer_muon_khong_lam_treo.stdout) | phản chứng/hợp đồng mới đỏ nền; xem log |
| `r868_khong_bo_chon_doc_dong_cuoi` | [0](out/evidence/target-head-r868_khong_bo_chon_doc_dong_cuoi.stdout) | [0](out/evidence/target-base-cross-r868_khong_bo_chon_doc_dong_cuoi.stdout) |  |
| `r868_doc_kenh_hong_thi_dung` | [0](out/evidence/target-head-r868_doc_kenh_hong_thi_dung.stdout) | [1](out/evidence/target-base-cross-r868_doc_kenh_hong_thi_dung.stdout) | phản chứng/hợp đồng mới đỏ nền; xem log |
| `r868_ghi_kenh_hong_thi_dung` | [0](out/evidence/target-head-r868_ghi_kenh_hong_thi_dung.stdout) | [1](out/evidence/target-base-cross-r868_ghi_kenh_hong_thi_dung.stdout) | nền không ghi payload nên fault printf không chạy; không đo producer nền |
| `r868_don_kenh_khi_loi` | [0](out/evidence/target-head-r868_don_kenh_khi_loi.stdout) | [1](out/evidence/target-base-cross-r868_don_kenh_khi_loi.stdout) | nền không tạo kênh để đo cleanup; không kill |
| `r868_vong_duyet_ung_vien` | [0](out/evidence/target-head-r868_vong_duyet_ung_vien.stdout) | [0](out/evidence/target-base-cross-r868_vong_duyet_ung_vien.stdout) |  |
| `r868_hinh_dang_kenh_ket_qua` | [0](out/evidence/target-head-r868_hinh_dang_kenh_ket_qua.stdout) | [1](out/evidence/target-base-cross-r868_hinh_dang_kenh_ket_qua.stdout) | ValueError vì nền chưa có kiến trúc; không kill |

## Hướng săn độc lập

| HƯỚNG | Giả thuyết | Lệnh đã chạy | OUTPUT thật rút gọn | Kết luận |
|---|---|---|---|---|
| 1. Kênh/stdout | Writer muộn, không LF hoặc dòng cuối đường dẫn sẽ ghi đè DICH. | `python3 -B out/probes.py channel` | Nền a/b rc2/DO; head a/b/c rc0/DAT, GITHUB_PATH=ứng viên; writer_done=true. | **KHÔNG PHẢI LỖI** trên head; N1a/b đỏ nền. |
| 2. Export/allexport | Gán trong allexport sẽ làm kênh riêng lộ sang installer. | cùng lệnh `channel`; `new_mutations.py`; `new_witnesses.py`; `new_full.py` | Head normal/bash-a/SHELLOPTS ABSENT ABSENT; hai mutant gán lại sống targeted; mutant KENH sống toàn suite; witness allexport có 4 TinHieuChotCa. | **LỖI độ phủ P3 F868-06**, runtime head đúng trong phạm vi đã đo. |
| 3. Batch/source/trap | Trap lượt sau xoá nhầm/rò temp, hoặc kênh cũ lẫn sang lượt sau. | `python3 -B out/probes.py batch` | 12 tổ hợp rg,bash/bash,rg × bình thường/lỗi ×3 chế độ: 6 rc0 và 6 rc23, **mọi tmp_left=[]**. Lỗi sau tool trước có DAT vẫn là batch rc23. | **KHÔNG PHẢI LỖI** trong ma trận. Mutant bỏ rm tường minh bị ca batch mới giết. |
| 4. Errexit/recipe failure | Subshell set+e làm công thức lỗi trả0 khác nền. | `python3 -B out/probes.py failures`; `new_witnesses.py` | nền/head installer rc29, checker rc1; `false; echo uv` cả hai rc0/DAT (semantics cũ). Mutant bỏ pipefail sống ca hiện có; recipe pipeline tổng hợp head rc1/mutant rc0. | **KHÔNG PHẢI LỖI runtime head**. Mutant pipefail là giới hạn cho recipe tương lai; không có pipeline ấy trong YAML đang giao, không mở finding acceptance mới. |
| 5. Giữ stdout/stderr | Descendant giữ fd khiến shell không thoát theo N2. | `python3 -B out/probes.py streams` | stdout shell/communicate **0.638/0.638s**; stderr **0.884/3.195s**; cả hai **0.757/3.202s**, tất cả rc0/DAT. | **KHÔNG PHẢI LỖI N2 stdout**; caller bắt stderr vẫn chờ EOF stderr. Không khẳng định mọi caller trở về ngay. |
| 6. N3/CRLF/temp | Reader mới làm pip/actionlint/fallback hoặc TMPDIR khoảng trắng hỏng. | `python3 -B out/probes.py crlf`; `out/review.py congcu`; gate ci; `out/space-temp-run.log` | CRLF nền/head rc0/DAT; congcu61/61; TMPDIR `tạm có khoảng trắng` trong 3 mode rc0/DAT, tmp_left=[]. | **KHÔNG PHẢI LỖI** đo trên Linux. CRLF mock không chứng minh Git Bash thật. |
| 7. rg Windows | Bỏ kiểm rg.exe và đổi GITHUB_PATH làm sai chọn/ghi path. | `python3 -B out/probes.py windows`; targeted r802/r858 Windows | 8 fixture: links/choco/bare-good/gp-empty/gp-unset rc0; bad/u-error/w-error rc1. Bare-good không gọi cygpath/không ghi gp, giữ Q3. | **KHÔNG PHẢI LỖI trong mô phỏng**; native Windows/rg.exe/cygpath/mktemp **KHÔNG ĐO ĐƯỢC**. |
| 8. Q4 và chốt cũ | Đổi neo/bỏ mutant YAML làm mất kiểm hành vi. | `python3 -B out/audit.py`; `python3 -B out/strict_mutations.py` | 0 ca/hàm bị xoá; 5 mutant YAML bỏ đúng handoff; các chốt chuyển vào hàm chung đều TinHieuChotCa; **41 mutant hook, 78 kill, 21 control pass**, invalid-credit=0. | **KHÔNG PHẢI LỖI** theo phạm vi đã đo. |

Mỗi hướng đã ghi vào verdict khi hoàn tất; đây là bảng hợp nhất cuối. [Hunt argv/output](out/hunts-run.log), [probe JSON](out/evidence/), [mutation riêng](out/evidence/new-targeted.json).

## Đột biến và Q4

`python3 -B .claude/dev/launcher_test.py --dot-bien` in **307/307 đạt, 4 không đo được**, rc0. Đây là kết quả danh nghĩa của runner. Không nhận lỗi vô can làm tín dụng: audit riêng **41/41 DOT_BIEN_HOOK** cho **78/78 ca đích TinHieuChotCa**, 21 control xanh, không lỗi khác. Các chốt bản vá shell/YAML đều có kill thật. Mutant harness gốc tạm `wp858_goc_tam_bo_kiem_to_tien` còn control EROFS trên sandbox này nên không nhận dòng OK danh nghĩa ấy là chứng minh kill nghiệp vụ. Bốn mutation nền không hỗ trợ vẫn là không đo được.

Ba mutant tự nghĩ ngoài bảng (chỉ trong out/new-mutants) đều sống qua cùng bộ29 ca: **28 pass, 1 OSError môi trường**, không TinHieuChotCa. Hai phép gán lại biến private là một lớp F868-06; mutant bỏ pipefail đã được chứng minh không tương đương bằng recipe tổng hợp, nhưng không được nâng thành lỗi của recipe thực tế. Chỉ mutant KENH được chạy thêm toàn launcher; không nói hai mutant còn lại đã chạy toàn bộ.

Handoff Q4 khớp diff: r831 chuyển eval trực tiếp sang script vì GIU_PATH thay stdout; harness r858 trực tiếp tự cấp kênh để tránh xanh vô nghĩa; shape từ12→15 recipe; ba sentinel mutant chuyển sang GIU_PATH/DICH; ba neo ứng viên đổi sang đối số helper. Năm mutant YAML bỏ đúng danh sách, được thay bằng chốt helper chung chọn theo checker, lỗi ghi GITHUB_PATH và bare-DAT. Không xoá ca hoặc hàm; test count244→252, hook mutant30→41. [Audit](out/evidence/scope-audit.json), [strict kills](out/evidence/strict-hook-mutations.json).

Diff **6 tệp/391 dòng thêm/93 xoá**, đúng write set và trần450, không ops/handoff; diff --check rc0. YAML chỉ đổi rg.cai.*; tiền tố cài15 recipe giữ nguyên; tl_selftest chỉ ratchet/comment190→191. Handoff còn bản TẠM/head=null nên không coi là handoff freeze cuối.

## Lệnh → kết quả thật

Các lệnh trong bảng dùng env của out/review.py (`PYTHONDONTWRITEBYTECODE=1`, offline pip, auth thật bị bỏ, signing command-config=false), cwd out/head trừ khi ghi khác. Driver rc0 không thay rc con; rc con ở metadata/output.

| Lệnh | Kết quả thật |
|---|---|
| `python3 -B out/review.py setup` | rc0; dựng cả hai vế và base-cross trong một lệnh; anchors/diff --check rc0. |
| `python3 -B out/review.py targeted head`; `... targeted base-cross` | 29 CLI mỗi vế; head28 pass/1 lỗi môi trường; base21 pass/8 đỏ như bảng N. |
| `python3 -B out/prior_check.py`; `out/probes.py io-readback`; `out/explore.py witnesses` | Control/witness và mutant cũ xác nhận F868-01..05 đóng; chi tiết ở bảng đối chiếu và prior-rerun.log. |
| `python3 -B .claude/dev/launcher_test.py --nhat-ky $R/out/evidence/launcher-base-none.jsonl` (cwd `out/base`, auth none) | rc1; **221/234** đã chạy qua, tổng244, failed13, skipped10; 317.26s. [Output](out/evidence/launcher-base-none.stdout). |
| `python3 -B .claude/dev/launcher_test.py --nhat-ky $R/out/evidence/launcher-base-fake.jsonl` (cwd `out/base`, auth fake) | rc1; **221/234** đã chạy qua, tổng244, failed13, skipped10; 244.861s. [Output](out/evidence/launcher-base-fake.stdout). |
| `python3 -B .claude/dev/launcher_test.py --nhat-ky $R/out/evidence/launcher-head-none.jsonl` (cwd `out/head`, auth none) | rc1; **229/242** đã chạy qua, tổng252, failed13, skipped10; 238.859s. [Output](out/evidence/launcher-head-none.stdout). |
| `python3 -B .claude/dev/launcher_test.py --nhat-ky $R/out/evidence/launcher-head-fake.jsonl` (cwd `out/head`, auth fake) | rc1; **229/242** đã chạy qua, tổng252, failed13, skipped10; 239.056s. [Output](out/evidence/launcher-head-fake.stdout). |
| `python3 -B out/new_full.py (shell mutant)` | rc1; **229/242** đã chạy qua, tổng252, failed13, skipped10; 269.91s. [Output](out/evidence/new-full-channel.stdout). |
| So tập failed/skipped cả4 suite và mutant | **Delta=0**. [Danh sách đầy đủ và delta](out/evidence/suite-delta-r3.json). Không gọi các suite rc1 là N/N. |
| `python3 -B .claude/dev/launcher_test.py --dot-bien` | rc0, nominal307/307, không đo4; caveat EROFS harness ở trên. |
| `python3 -B out/strict_mutations.py` | rc0,41 hook mutant/78 TinHieuChotCa/21 control pass, không invalid-credit. |
| `python3 -B out/new_mutations.py`; `out/new_witnesses.py` | rc0;116 targeted records;14 witness/control,5 TinHieuChotCa (4 private variables +1 pipeline),9 pass; chỉ tính TinHieuChotCa là kill. |
| `python3 -B ops/cong_cu_test.py` mặc định | **Bị dừng rc130** sau61/61 và cổng cây thật ĐẠT, trước khi hoàn tất470-mutant radius; không pass. [Partial](out/evidence/congcu.stdout). |
| `CONG_CU_TEST_BAN_KINH=manh python3 -B ops/cong_cu_test.py` | **rc0,61/61**, bỏ qua0/tiền kiểm bỏ qua0/cổng cây thật ĐẠT;470 mutant giao CI shard, không đo đủ radius trong lệnh này. [Gate](out/evidence/congcu-ci.stdout). |
| `bash -n ops/cai_cong_cu.sh` | rc0,stdout/stderr rỗng. |
| `python3 -B -m ruff check --no-cache --select F --output-format json scripts/tl.py scripts/tl_selftest.py .claude/dev/launcher_test.py` nền/head | Cả hai rc1,4409 finding; delta mới/xoá=[], Ruff0.17.1. Bare lint có nợ nền; không đồng nhất với pin/probe contract CI. |
| `actionlint` nền/head | Cả hai rc0, không thêm finding. |
| `python3 -B scripts/tl.py --selftest` | **rc0,1731/1731**;346.345s. [Output](out/evidence/selftest.stdout). |
| `python3 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | **rc0,ok=true,191=191**, package hashes khớp. [JSON](out/evidence/release.stdout). |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | rc0,đã quét10 tệp/0 chỗ chép doctrine. |
| `python3 -B scripts/tl.py doc-claims-check --strict --json` | rc0,0 hard finding,396 advisory. |
| Source fingerprints và rev-parse đầu/cuối | rc0,delta=[] cho cả2 cây; HEAD/tree không đổi. |

Driver serial suites được dừng rc130 sau khi hoàn tất cả hai baseline, để chạy độc lập hai head mode. Head-none partial được lưu riêng, **không tính pass**; cả4 kết quả trong bảng đều là lượt chạy kết thúc trọn vẹn. Mọi stdout/metadata/fixture/mutant nằm dưới out/, không ghi source.

## Không đo được

- Native Windows/macOS, Git Bash/MSYS/PATHEXT/rg.exe, mktemp/cygpath/installer thật, và sàn mutation Windows≥70%. Windows/macOS fixture chỉ mô phỏng trên Linux, không nhận là native pass.
- Check run ci.yml/launcher-windows.yml trên exact head, M-2 thread resolution, lease heartbeat/authority live và quyết định chủ kho cho F868-06. Assignment cấm mạng/GitHub; không suy cổng local thành M-3 đã đạt.
- 10 launcher skipped (8 venv/pip offline,2 Windows),13 lỗi môi trường chung; không xoá /tmp/.git ro hay đo trạng thái sau phiên Codex. Không biến failed/skipped thành passed.
- 4 mutation launcher không hỗ trợ trên nền này; control gốc tạm EROFS nên không nhận kill harness ấy;470 mutant radius của congcu giao CI mode manh chưa chạy đủ. Default congcu và head-none partial bị dừng đều giữ cancelled/rc130.
- Full launcher chỉ đo thêm mutant KENH; mutant TAM/pipefail chỉ đo bộ29 ca liên quan cùng witness độc lập. Pipeline tổng hợp không phải recipe đang dùng, không dùng nó để tuyên bố regression runtime.
- Các khả năng đòi tự soạn nội dung tấn công đường dẫn/thoát thư mục không được dựng theo assignment; nếu cần kiểm sâu chúng phải được mô tả bằng lời hoặc dùng phản chứng đã được cấp.

Fingerprint bằng nhau chỉ chứng minh không có delta ở hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Không có patch/commit/push/merge/land/deploy. Danh mục băm các artifact review: [SHA256SUMS](out/SHA256SUMS).
