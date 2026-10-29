Verdict: request_changes
Reviewed commit: 71c19c937442ae38875717989654ee93f387d04e
Spec sha256: 9df36da1ef2be23c7519934bf6aee0dfecb6d2082cb8e485c7a6819c8a6154f3; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

**Kết luận lượt 3: còn 1 lớp P2, giữ slug `r813-mutation-evidence-incomplete`; lớp `ci-reopen-run-context-unbound` đã đóng. Không phát hiện P0/P1 hoặc lớp P3 mới.** Candidate xử lý đúng những đầu vào đã đo; P2 còn lại là thiếu phản chứng bảo vệ việc thay quyền `mo_lai_tu` theo I6. Ngưỡng approve của assignment là hết P0/P1/P2. Theo prompt, slug cũ còn mở nên packet dừng để chủ kho quyết định tiếp; verdict này không cấp quyền vá thêm, push, merge hoặc land.

| slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| `r813-mutation-evidence-incomplete` | **P2, còn mở** | `.claude/dev/packet_loop_test.py:8932` chỉ kiểm state/bộ đếm sau connector đến sau CI; thiếu kiểm quyền thay thế. Điểm đột biến sản phẩm: `.claude/dev/packet_loop.py:2984`. | Mutant riêng giữ `mo_lai_tu` cũ sống **104/104 ca r813+r834**. A/B chuỗi CI → connector → checkpoint vá: candidate rc0/0/0, mutant rc0/0/8 với `state hỏng (mo-lai)`. Ca reviewer kiểm tuple quyền giết đúng bằng AssertionError; ca sẵn có vẫn xanh. | Bổ sung oracle đầy đủ `(nguyên nhân, generation, sha)` ngay sau CI → connector và bước dùng checkpoint vá; khai mutant giữ quyền cũ, yêu cầu chết đúng oracle, giữ đối chứng dương. |

Reviewer độc lập Codex/OpenAI, họ openai; executor theo lease bản chép là Claude, họ claude. Packet #813 revision 2 generation 1, review_class sensitive, assurance_target cross_approved. Thực thi qua shell công cụ Linux, transport machine; serving model/effort và attestation launcher `codex_cli` không được đo độc lập, không suy từ tên công cụ hoặc actor đăng GitHub. Không tạo receipt assurance. Đã đọc toàn bộ `runs/58e835d1/prompt.snapshot`; mọi đường dẫn tương đối tính từ gốc rv3 theo chỉ thị trực tiếp. Không kế thừa context executor, không mạng/GitHub, không sửa mã nguồn SRC; mọi phép thử và artifact ở OUT.

**Đối chiếu lượt trước.** Lượt 2 review `79bbbdc16bd873f319ab70885039413735ee2fb3` còn hai lớp P2. Lượt 3 do chủ kho cho vá thêm và nâng trần lên 10 theo prompt (không xác minh comment online). Đã review toàn bộ diff base `a268bcc0e956f010eb4e06633676aafe1f386c37` → candidate, không chỉ diff vá `79bbbdc` → candidate. Hai diff lưu ở `FULL.diff`, `FIX.diff`.

| slug lượt 2 | phân loại | bằng chứng độc lập lượt này |
|---|---|---|
| `ci-reopen-run-context-unbound` | **ĐÃ VÁ THẬT** | Chính phản chứng lượt 2: check-run đỏ sai head hoặc head rỗng đều rc12, state nguyên byte; head null/số cũng bị schema chặn rc12. Baseline đỏ đúng head rc0. Mutant bỏ riêng so head bị `r813_ci_do_check_head_khac` giết bằng AssertionError đòi12/được0. Run mới xanh + run cũ rerun đỏ, check khác kho, check mới thiếu app đều bị từ chối/nguyên byte. |
| `r813-mutation-evidence-incomplete` | **VÁ HỜ ở cấp lớp: hai biểu hiện lượt 2 đã vá thật, còn biểu hiện cùng nguyên nhân** | Hai mutant cũ bỏ kiểu `repository.full_name` và giữ `checkpoint_day` cũ nay bị đúng ca mới bắt. A/B độc lập vẫn cho candidate rc12/nguyên byte với full_name số, và quyền checkpoint khớp hash thực tính của hiện vật thứ hai. Tuy nhiên mutant giữ quyền `mo_lai_tu` cũ sống 104/104, nên chưa đóng lớp độ phủ I6. |

Một trong hai lớp cũ đóng: **1/2 = 50%**. Không đổi slug, không reset lịch sử. Không gọi việc sửa đúng hai biểu hiện đã chỉ ra là đóng toàn lớp khi còn phản chứng cùng cơ chế trong phạm vi I6/M2.

**P2 còn mở — phạm vi và cách tái hiện.** Đây không phải khẳng định mã candidate giữ sai quyền. Candidate thay quyền đúng; suite hiện không bảo vệ hành vi ấy. `r813_connector_sau_ci` chạy CI rồi connector, kết thúc ở kiểm `state=cho_chu_kho` và hai bộ đếm, không kiểm `mo_lai_tu`, không đọc lại bằng `status` và không đi tiếp qua checkpoint. Các ca checkpoint khác bắt đầu từ connector trực tiếp nên chưa có quyền cũ để thay.

Mutant ở bản sao OUT chỉ thêm phép giữ quyền hiện có vào phép gán quyền của `cmd_mo_lai`; cặp tìm/thay nguyên văn nằm trong `extra_reopen_keep_old/mutation.json`, mã đã chạy ở `extra_reopen_keep_old/packet_loop.py`. Nó có đúng một mỏ neo, không sửa fixture hoặc code SRC. Toàn bộ 104 ca #813+#834 vẫn xanh, không skipped hoặc traceback. Bảng sau trích `probes/results.json`; SHA được so trong từng fixture, không dùng tên nhánh làm định danh.

| bước | candidate | mutant giữ quyền cũ |
|---|---|---|
| `mo-lai ci-do` | rc0, running, quyền `(ci-do,1,H)` | rc0, cùng kết quả |
| `mo-lai connector` trên cùng H | rc0, cho_chu_kho, quyền **`(connector,1,H)`** | rc0, cho_chu_kho, quyền vẫn **`(ci-do,1,H)`** |
| `chu-kho-duyet` với checkpoint cho_phep_va hợp lệ trên master fixture | rc0, running, quyền được tiêu thụ thành None | rc8, `state hỏng (mo-lai)`, state nguyên byte; quyền cũ khiến trạng thái vừa ghi không đọc lại được |

Ca bổ sung `reviewer_i6_reopen_replaces_permission` trong `lock_reopen_probe.py` dùng baseline thật và so toàn bộ dict quyền sau hai lệnh. Candidate PASS; mutant bị GIẾT bằng `AssertionError: r813: nội dung quyền sai`, không phải CLI sập. Trên cùng mutant, ca gốc `r813_connector_sau_ci` và 3 đối chứng khác họ vẫn PASS. Kết quả đầy đủ ở `lock_reopen_probe/results.json` và `logs/lock_reopen_probe.log`.

**Hướng vá đủ bốn phần:** sửa test tại ca `r813_connector_sau_ci` hoặc thêm ca chuỗi riêng, vì nơi thiếu quan sát là hậu điều quyền sau chuyển nguyên nhân, không phải predicate sản phẩm hiện đang đúng. So `mo_lai_tu` với tuple nguồn độc lập; nối checkpoint cho_phep_va để kiểm quyền đọc lại và tiêu thụ được. Thêm mutant giữ quyền cũ vừa đo, và yêu cầu chết tại oracle tuple trong khi baseline cùng các đối chứng vẫn xanh. Rủi ro khi vá test: chỉ kiểm state/bộ đếm hoặc chỉ so hai trường cùng sinh từ code sẽ tiếp tục bỏ sót quyền cũ; đợi tới một CLI sau sập rồi tính đó là tín dụng cũng không chứng minh đúng chốt. Có thể gộp thêm oracle vào ca sẵn có để giữ diff dưới 450 dòng; không cần đổi mã sản phẩm đang đúng cho biểu hiện này.

**Đối chiếu từng ca bắt buộc trong `nghiem_thu`.** Mỗi ca dưới đây PASS trên candidate. Cột mutant ghi ngoại lệ thực đo của đúng ca; tất cả đều là AssertionError đúng hành vi, không dùng riêng mã thoát runner để kết luận.

| yêu cầu | ca | mutant khai báo | lỗi của đúng ca trên mutant / đánh giá |
|---|---|---|---|
| Chạm trần qua mo-lai → blocked | `r813_cham_tran_mo_lai` | `r813_mo_lai_khong_xet` | AssertionError: r813 bước 1: đòi rc=3, được rc=0; stderr='' — đúng chốt đã khai |
| Cùng nguyên nhân dưới hai comment ID → chung bộ đếm | `r813_cung_slug_hai_id` | `r813_dem_theo_id` | AssertionError: r813 bước 4: đòi rc=3, được rc=0; stderr='' — đúng chốt đã khai |
| Hai nguyên nhân độc lập đếm riêng | `r813_hai_slug_doc_lap` | `r813_gop_nguyen_nhan` | AssertionError: r813 bước 4: đòi rc=0, được rc=3; stderr='cùng finding-id lặp tới trần (gop×2; trần 2) — packet về blocked. Lặp lại nghĩa là bản vá không trúng gốc; ghi failure evidence + handoff rồi dừng.' — đúng chốt đã khai |
| Slug ngoài H → từ chối | `r813_slug_ngoai_bien_nhan` | `r812_bo_slug_trong_bang` | AssertionError: r813 bước 0: đòi rc=11, được rc=0; stderr='' — đúng chốt đã khai |
| begin-attempt khi đã chạm trần | `r813_begin_attempt_cham` | `r813_begin_khong_xet` | AssertionError: r813 bước 2: đòi rc=3, được rc=0; stderr='' — đúng chốt đã khai |
| Cửa khép lượt không bị chặn | `r813_cua_khep_khong_chan` | `r813_chan_cua_khep` | AssertionError: r813 bước 3: đòi rc=0, được rc=3; stderr='cùng finding-id lặp tới trần (ci-gate×1; trần 1) — packet về blocked. Lặp lại nghĩa là bản vá không trúng gốc; ghi failure evidence + handoff rồi dừng.' — đúng chốt đã khai |
| mo-lai không finding → từ chối | `r813_khong_finding` | `r813_bo_tap_rong` | AssertionError: r813 bước 0: đòi rc=2, được rc=0; stderr='' — đúng chốt đã khai |
| Connector chỉ phủ tập con P0–P2 | `r813_connector_tap_con` | `r813_tap_con_lot` | AssertionError: r813 bước 0: đòi rc=11, được rc=0; stderr='' — đúng chốt đã khai |
| CI đỏ và connector P1 cùng head | `r813_ci_va_p1_cung_head` | `r813_bo_ci_do` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' — đúng chốt đã khai |
| Connector đến sau CI: điều kiện vào | `r813_connector_sau_ci` | `r813_chi_tu_approved` | AssertionError: r813 bước 1: đòi rc=0, được rc=8; stderr="mo-lai connector không chạy từ 'running' (đòi approved_pending của packet áp ADR-0054, hoặc running mở lại bằng ci-do cùng generation)" — đúng chốt đã khai |
| Connector đến sau CI: không đòi đã xong lúc CI đỏ | `r813_connector_sau_ci` | `r813_ci_do_doi_connector_xong` | AssertionError: r813 bước 0: đòi rc=0, được rc=12; stderr='connector chưa xong trên 6c9c5b8c25a48a890f6cd6d2f859fe37036360a0: không review hoàn tất/kết luận nào của chatgpt-codex-connector[bot]' — đúng chốt đã khai |
| Checkpoint chỉ trên nhánh khác | `r813_checkpoint_nhanh_khac` | `r813_checkpoint_ref_tuy_y` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' — đúng chốt đã khai |
| Checkpoint của packet khác | `r813_checkpoint_packet_khac` | `r813_bo_packet_checkpoint` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' — đúng chốt đã khai |
| Không dùng cho_phep_va làm quyền đẩy | `r813_va_lam_quyen_day` | `r813_moi_pham_vi_la_du` | AssertionError: r813 bước 0: đòi rc=7, được rc=0; stderr='' — đúng chốt đã khai |
| M5 run mới in_progress thiếu repository | `r813_m5_run_moi_thieu_repository` | `r813_m5_bo_repository` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' — đúng chốt đã khai |
| M5 path sai kiểu | `r813_m5_run_path_sai_kieu` | `r813_m5_bo_path` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' — đúng chốt đã khai |
| M5 head_sha sai kiểu | `r813_m5_run_head_sai_kieu` | `r813_m5_bo_head_sha` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' — đúng chốt đã khai |
| M5 full_name sai kiểu, bổ sung đóng biểu hiện lượt 2 | `r813_m5_run_full_name_sai_kieu` | `r813_m5_bo_full_name` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' — đúng chốt đã khai |

Đối chứng M5: **63/63 ca r834 hiện có PASS**. Với yêu cầu connector đến sau CI, hai mutant khai báo chứng minh điều kiện vào và thời điểm hoàn tất connector; chúng chưa khóa hậu điều thay quyền I6, là finding P2 nêu trên. Các ca `r813_ci_do_running`, `r813_connector_cho_chu_kho`, `r813_checkpoint_pham_vi_long` có mặt và PASS; không suy từ thiếu tên target rằng chúng không giết gián tiếp bất kỳ mutant nào.

**Audit toàn bộ mutant liên quan.** 35 mutant tiền tố `r813_`, 4 mutant dùng chung được nối target #813, và 2 mutant #834 đổi mỏ neo trong diff: **41 mutant / 45 quan hệ mục tiêu GIẾT / 123 đối chứng khác họ PASS**. Mọi mỏ neo tồn tại duy nhất; không thiếu target; không TIN_DUNG_GIA/BO_QUA/SONG ở target. Đã đọc tên ca, lớp ngoại lệ và thông điệp từng kết quả. Hai lỗi kiểm quyền có state đầy đủ trong JSON; bảng rút gọn bên dưới chỉ nêu trường gây đỏ.

| mutant | ca đích | ngoại lệ/thông điệp thực đo |
|---|---|---|
| `r812_bo_slug_trong_bang` | `r812_slug_ngoai_bang_lop` | AssertionError: r812 review ['bn', 'ids', 'lop', 'verdict']: đòi rc=11, được rc=0; stderr='' |
| `r812_bo_slug_trong_bang` | `r813_slug_ngoai_bien_nhan` | AssertionError: r813 bước 0: đòi rc=11, được rc=0; stderr='' |
| `r834_bo_app` | `r834_check_app_khac` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| `r834_bo_app` | `r813_ci_do_app_khac` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' |
| `r834_bo_path_workflow` | `r834_check_workflow_khac` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| `r834_bo_path_workflow` | `r813_ci_do_workflow_khac` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' |
| `r834_bo_attempt_moi_nhat` | `r834_rerun_dang_chay` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| `r834_run_cu_nhat` | `r834_run_moi_nhat_do` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr="CẢNH BÁO: 'gate (ubuntu-latest)' có 1 run ở suite khác (300) — bỏ qua\nCẢNH BÁO: 'gate-cong-cu-gop (ubuntu-latest)' có 1 run ở suite khác (301) — bỏ qua\nCẢNH BÁO: 'gate-ops (ubuntu-latest)' có 1 run ở suite khác (302) — bỏ qua\nCẢNH BÁO: 'gate-packet-loop (ubuntu-latest)' có 1 run ở suite khác (303) — bỏ qua\nCẢNH BÁO: 'gate-registry (ubuntu-latest)' có 1 run ở suite khác (304) — bỏ qua" |
| `r834_run_cu_nhat` | `r813_ci_do_run_moi_xanh` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' |
| `r834_bo_job_xanh` | `r834_job_chua_xanh` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| `r813_bo_ci_do` | `r813_ci_va_p1_cung_head` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' |
| `r813_ci_do_nhan_xanh` | `r813_ci_khong_do` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' |
| `r813_ci_do_bo_check_do` | `r813_ci_do_check_xanh_job_do` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' |
| `r813_ci_do_bo_head_check` | `r813_ci_do_check_head_khac` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' |
| `r813_quyen_day_giu_cu` | `r813_checkpoint_day_thay` | AssertionError: r813: nội dung quyền sai — quyền giữ hash checkpoint thứ nhất, history đã ghi hash thứ hai; toàn bộ state trong JSON. |
| `r813_m5_bo_full_name` | `r813_m5_run_full_name_sai_kieu` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| `r813_gop_nguyen_nhan` | `r813_hai_slug_doc_lap` | AssertionError: r813 bước 4: đòi rc=0, được rc=3; stderr='cùng finding-id lặp tới trần (gop×2; trần 2) — packet về blocked. Lặp lại nghĩa là bản vá không trúng gốc; ghi failure evidence + handoff rồi dừng.' |
| `r813_bo_ghi_quyen_day` | `r813_checkpoint_day` | AssertionError: r813: nội dung quyền sai — thiếu checkpoint_day dù lệnh trả rc0; toàn bộ state trong JSON. |
| `r813_bo_generation_quyen_ci` | `r813_quyen_ci_khac_generation` | AssertionError: r813 bước 2: đòi rc=8, được rc=0; stderr='' |
| `r813_bo_refs_duy_nhat` | `r813_refs_lap` | AssertionError: r813 bước 0: đòi rc=11, được rc=0; stderr='' |
| `r813_bo_spec_hash_checkpoint` | `r813_checkpoint_spec_lech` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' |
| `r813_bo_mien_pham_vi` | `r813_checkpoint_pham_vi_la` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' |
| `r813_m5_bo_path` | `r813_m5_run_path_sai_kieu` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| `r813_bo_tap_rong` | `r813_khong_finding` | AssertionError: r813 bước 0: đòi rc=2, được rc=0; stderr='' |
| `r813_tap_con_lot` | `r813_connector_tap_con` | AssertionError: r813 bước 0: đòi rc=11, được rc=0; stderr='' |
| `r813_chi_tu_approved` | `r813_connector_sau_ci` | AssertionError: r813 bước 1: đòi rc=0, được rc=8; stderr="mo-lai connector không chạy từ 'running' (đòi approved_pending của packet áp ADR-0054, hoặc running mở lại bằng ci-do cùng generation)" |
| `r813_ci_do_doi_connector_xong` | `r813_connector_sau_ci` | AssertionError: r813 bước 0: đòi rc=0, được rc=12; stderr='connector chưa xong trên 6c9c5b8c25a48a890f6cd6d2f859fe37036360a0: không review hoàn tất/kết luận nào của chatgpt-codex-connector[bot]' |
| `r813_dem_theo_id` | `r813_cung_slug_hai_id` | AssertionError: r813 bước 4: đòi rc=3, được rc=0; stderr='' |
| `r813_mo_lai_khong_xet` | `r813_cham_tran_mo_lai` | AssertionError: r813 bước 1: đòi rc=3, được rc=0; stderr='' |
| `r813_begin_khong_xet` | `r813_begin_attempt_cham` | AssertionError: r813 bước 2: đòi rc=3, được rc=0; stderr='' |
| `r813_chu_kho_khong_xet` | `r813_chu_kho_cham_tran` | AssertionError: r813 bước 2: đòi rc=3, được rc=0; stderr='' |
| `r813_chan_cua_khep` | `r813_cua_khep_khong_chan` | AssertionError: r813 bước 3: đòi rc=0, được rc=3; stderr='cùng finding-id lặp tới trần (ci-gate×1; trần 1) — packet về blocked. Lặp lại nghĩa là bản vá không trúng gốc; ghi failure evidence + handoff rồi dừng.' |
| `r813_xet_truoc_dau_vao` | `r813_xet_dung_sau_dau_vao` | AssertionError: r813 bước 2: đòi rc=11, được rc=3; stderr='cùng finding-id lặp tới trần (ci-gate×1; trần 1) — packet về blocked. Lặp lại nghĩa là bản vá không trúng gốc; ghi failure evidence + handoff rồi dừng.' |
| `r813_checkpoint_ref_tuy_y` | `r813_checkpoint_nhanh_khac` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' |
| `r813_bo_packet_checkpoint` | `r813_checkpoint_packet_khac` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' |
| `r813_moi_pham_vi_la_du` | `r813_va_lam_quyen_day` | AssertionError: r813 bước 0: đòi rc=7, được rc=0; stderr='' |
| `r813_checkpoint_dung_lai` | `r813_checkpoint_day_dung_lai` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' |
| `r813_va_ve_running_khong_tieu` | `r813_checkpoint_va` | AssertionError: r813: đòi {'state': 'running', 'mo_lai_tu': None}, được {'state': 'running', 'mo_lai_tu': {'generation': 1, 'nguyen_nhan': 'connector', 'sha': '6c9c5b8c25a48a890f6cd6d2f859fe37036360a0'}} |
| `r813_m5_bo_repository` | `r813_m5_run_moi_thieu_repository` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| `r813_lop_bo_hang` | `r813_connector_lop_p3` | AssertionError: r813 bước 0: đòi rc=11, được rc=0; stderr='' |
| `r813_bo_head_checkpoint` | `r813_checkpoint_head_lech` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' |
| `r813_bo_generation_checkpoint` | `r813_checkpoint_generation` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' |
| `r813_bo_nguoi_quyet` | `r813_checkpoint_nguoi_quyet` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' |
| `r813_cho_chu_kho_khong_quyen` | `r813_state_cho_chu_kho_mat_quyen` | AssertionError: r813 bước 2: đòi rc=8, được rc=0; stderr='' |
| `r813_m5_bo_head_sha` | `r813_m5_run_head_sai_kieu` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |

**Bất biến và review không lọc.** Đã đọc toàn bộ hai tệp trong diff, cùng các đường gọi validator, đọc state, begin/review, connector, CI và checkpoint có liên quan. Không thấy mâu thuẫn thiết kế buộc đổi hợp đồng accept. Phần protocol cho_chu_kho/M4 đã tách khỏi r2 theo assignment, không tính hạng.

| bất biến / mục tiêu | kết quả và giới hạn |
|---|---|
| I1 / M2–M3 | mo-lai cần H qua `_du_dieu_kien_approve`; checkpoint dùng Đ: máy fetch master, so ls-remote và đọc blob bằng OID đã đo. R chỉ bổ sung. |
| I2 | Không đổi đường cấp lease; baseline thật dùng H/Đ/R trên bare repo fixture cục bộ.148 ca r812 PASS. Không xác minh authority lease ngoài bundle bằng mạng. |
| I3 | Finding rỗng, refs thiếu/trùng/thừa/sai kiểu bị từ chối. Ba kết luận đỏ failure/timed_out/startup_failure nhận rc0; success/cancelled/skipped/neutral/action_required/unknown bị chặn rc12. |
| I4 | Các ca âm bắt buộc và probe kiểm state nguyên byte. Kết quả hợp lệ chạm trần ghi findings/history rồi blocked. `_save` mã hóa trước mở tệp. Không thấy lỗi làm đổi byte state ở các lần từ chối đã đo. |
| I5 / M1 | Hai cửa mới dùng chung `_xet_dung` sau các bước xác thực H/R/Đ; mutant xét sớm chết vì trả rc3 thay rc11. Cửa begin-attempt chặn cùng finding; cửa record-review khép lượt vẫn chạy. |
| I6 | Candidate thay ci-do bằng connector, checkpoint mới thay checkpoint cũ, và cho_phep_va tiêu thụ mo_lai_tu. Hai hiện vật checkpoint được băm độc lập, quyền khớp hiện vật mới. Thiếu khóa test vế thay **mo_lai_tu**: P2 trên. Tiêu thụ quyền tại cửa đẩy thuộc #816, không đo trong packet này. |
| I7 | H/connector neo head lấy từ state: approved_pending dùng pending_sha; running chỉ nhận connector khi quyền ci-do cùng generation, dùng SHA nguồn trong quyền. Không có CLI chọn head. Readback connector sai repo/PR/head bị chặn. CI chọn run mới nhất trên workflow/repo/head, attempt mới nhất, nối job/check-suite/check-run/app và so head check đỏ. |
| I8 | Tiếp tục dùng chuẩn hóa canon của `_du_dieu_kien_approve`, không thêm chuẩn danh tính riêng. Regression r812 hỗ trợ. |
| I9 | `accept` gọi `_doc_connector` với p0p2 mặc định None: vẫn đòi connector hoàn tất và chặn P0–P2.63 r834 và148 r812 PASS; state cũ vắng hai quyền vẫn đọc được. Hai ca stdout ép cp1252/cp1258 PASS trên Linux. Không suy thành full suite hoặc Windows thật. |
| I10 | Probe H lệch packet/generation/reviewed_sha/spec_hash/verdict đều rc11/nguyên byte. Checkpoint kiểm packet/generation/head/spec_hash và phạm vi; ca schema lồng, người quyết sai, nhánh khác, dùng lại đều PASS theo rc/thông điệp mong đợi. |
| I11 | Slug từ bảng H, finding_counts đối chiếu reviews + history mo_lai. Hai ID chung nguyên nhân chung bộ đếm; hai nguyên nhân độc lập tách bộ đếm. Mutant slug/bộ đếm bị đúng ca bắt. |
| M5 | Mọi run qua kiểm path/head_sha/repository/full_name trước lọc. Ca thêm run mới thiếu repository, sai path/head/full_name đều rc12 với KHÔNG ĐO ĐƯỢC/nguyên byte. Mutant tương ứng đều bị giết đúng; A/B full_name số làm accept lọt dưới mutant. |

`chu-kho-duyet` chỉ cho rời cho_chu_kho khi checkpoint phạm vi cho_phep_va khớp tuple; cho_phep_day là quyền riêng ở approved_pending. Bảng chuyển state không có lối transition thoát cho_chu_kho. Các command cũ đổi state có guard riêng; record-lease/record-review/begin-attempt không mở đường vòng từ state này. Kiểm Đ chạy với remote bare cục bộ; race remote thật không được dựng trong lượt offline.

**Định danh, phạm vi và lệnh đã chạy.** HEAD `71c19c937442ae38875717989654ee93f387d04e`, tree `6c6b72591ee58f5bb0447a0c03881ba3a78841a2`. Base/ref origin/master `a268bcc0e956f010eb4e06633676aafe1f386c37` là tổ tiên (rc0); symbolic-ref rc1 đúng detached; is-shallow-repository=false; `.git` là thư mục; status/worktree/index sạch. Hai SHA-256 dòng 3 tính từ byte và khớp. `IDENTITY.json` giữ lệnh/rc/output.

Diff base → candidate: `.claude/dev/packet_loop.py` +153/-11, `.claude/dev/packet_loop_test.py` +213/-3: **đúng 2 đường dẫn, 366 dòng thêm ≤ 450**, diff --check rc0. `git diff --exit-code a774304 71c19c9 -- <hai tệp>` rc0, output rỗng: merge không đổi hai tệp write set. Base lease f577ab5 là mốc cấp lease lịch sử; base review lần này theo assignment là a268bcc. Lease bản chép cho thêm handoff trên nhánh lease nhưng ghi rõ diff PR chỉ 2 tệp; không dùng đường handoff để mở rộng phạm vi review.

Đã đọc `chon.py` và `dotbien.py` trước khi dùng logic. Runner riêng dùng cùng chay_suite/phân loại mutant/đối chứng khác họ, thêm kiểm inventory không rỗng, mỏ neo duy nhất, và giữ toàn văn exception; hai helper gốc dùng thư mục tạm rồi xóa, dotbien cắt thông điệp. Không coi rc0 trần là pass.

Môi trường phép thử: `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=OUT/tmp`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_OPTIONAL_LOCKS=0`, `GIT_ALLOW_PROTOCOL=file`; bản sao `core.abbrev=7`. Fixture tự dựng Git và commit/fetch/push/ls-remote **chỉ với bare repo cục bộ dưới OUT**. Không push/fetch repository packet. SyntaxWarning có sẵn khi import harness trong heredoc đột biến không là lỗi ca hoặc tín dụng giết.

| lệnh / phép chạy | rc | bằng chứng dương / artifact |
|---|---:|---|
| `python -B -W ignore out/run_review.py baseline_r813_r834 r813_,r834_` |0|104/104 PASS  = 41 r813 + 63 r834; results.json, summary.json, logs/baseline_r813_r834.log |
| `python -B -W ignore out/run_review.py baseline_r812 r812_,stdout_cp` |0|150/150 PASS  = 148 r812 + 2 codepage; results.json, excluded.json, summary.json, logs/baseline_r812.log |
| `python -B -W ignore out/run_review.py mutants` |0|41 mutant/45 target GIẾT đúng/123 đối chứng PASS; mutants/results.json, mỗi mutation.json, logs/mutants.log |
| Heredoc Python tạo mutant giữ quyền cũ và gọi suite với tập r813+r834 |0|**SỐNG 104/104**, không phải pass nghiệm thu; extra_reopen_keep_old/mutation.json, packet_loop.py, results.json, summary.json |
| `python -B -W ignore out/probes.py` |0|50 phép đo CLI với rc/stdout/stderr/hash byte state/quyền; probes/results.json, logs/probes.log |
| `python -B -W ignore out/lock_reopen_probe.py` |0|Ca reviewer PASS trên candidate, GIẾT mutant bằng oracle tuple; ca gốc và 3 đối chứng PASS ở cả hai vế; lock_reopen_probe/results.json |
| `python -B out/copy/.claude/dev/packet_loop.py doctrine-scan --root out/copy` |0|10 tệp/0 chỗ chép doctrine; GATES.json |
| `python -B out/copy/.claude/dev/packet_loop.py adr-song --root out/copy` |0|55 ADR/55 dòng §20, khớp 1–1; ngoại lệ 0016 có sẵn; GATES.json |

Tổng ca nền chọn lọc **254/254 PASS**; không failed/skipped trong tập đã chọn. rc0 của probe hoặc runner mutant sống nghĩa là hoàn tất phép đo, không chứng nhận nghiệm thu xanh. Các phép đo bổ sung không được cộng thành N/N toàn repository.

**Giới hạn và ngoài phạm vi.** `not_run`: full suite `python .claude/dev/packet_loop_test.py` cùng mọi mutant (prompt ưu tiên chạy chọn lọc), các mutant #812/#834 ngoài tập nêu trên, CI online, Windows thật, bare Ruff lint và Ruff pin/probe contract. Không nhận kết quả executor chưa đo làm evidence riêng. Ca `r812_r4_own_parent` loại trước chạy do tạo nội dung đường dẫn có thành phần cha, ghi trong excluded.json. Hướng thử đường dẫn thoát cây chỉ mô tả: checkpoint/receipt hoặc liên kết dẫn ra ngoài cây phải bị chặn trước đọc/ghi ngoài phạm vi và giữ state nguyên byte; không tự soạn payload ấy.

M4/protocol §4/§12, vòng P3 #814, generation kế tiếp #815, ghi đẩy và tiêu thụ quyền ở cửa đẩy #816, kích hoạt ADR-0054 đều ngoài phạm vi. Nợ P3 #834 `required-mutation-coverage-missing` về neo issue-comment/kiểu ID trang không được mở lại, nâng hạng hay khai đã đóng; finding ở đây thuộc I6 của #813.

**Toàn vẹn cuối lượt.** Snapshot SOURCE_INITIAL → SOURCE_FINAL: **6984 → 6984 tệp, 0 delta byte/mode, 0 symlink**. Snapshot đầu được ghi sau preflight và trước các probe độc lập; đây là đối chiếu hai mốc, không là giám sát mọi write trong lịch sử. `FINAL_CHECKS.json` xác nhận HEAD/tree/ref không đổi, source và bản sao nền sạch về worktree/index/untracked/ignored; byte code/test/chung bằng blob exact candidate. Sandbox thực tế workspace-write; mã nguồn packet được đối xử chỉ đọc, artifact reviewer nằm dưới OUT. `python -B out/finalize.py` rc0. Manifest `ARTIFACTS.json` băm verdict, script, diff và kết quả cấp OUT; không đưa toàn bộ kho fixture/bản sao vào manifest.
