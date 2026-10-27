Verdict: request_changes
Reviewed commit: 79bbbdc16bd873f319ab70885039413735ee2fb3
Spec sha256: 9df36da1ef2be23c7519934bf6aee0dfecb6d2082cb8e485c7a6819c8a6154f3; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

**Kết luận lượt 2: 2 lớp P2 còn mở; 2 lớp P2 lượt 1 đã đóng. Không có P0/P1/P3 mới.** Giữ nguyên slug theo nguyên nhân. Ngưỡng approve là hết P0/P1/P2. Verdict chỉ neo exact commit trên, không cấp quyền push/merge/land.

Reviewer độc lập Codex/OpenAI, họ openai; executor theo lease bản chép là Claude, họ claude. Packet #813 revision 2 generation 1, review_class sensitive, assurance_target cross_approved. Thực thi qua shell công cụ Linux, transport machine; không suy serving model/effort/session hoặc attestation launcher codex_cli từ tên công cụ. Không tạo receipt assurance. Đã đọc toàn bộ `runs/df129e3b/prompt.snapshot`, dùng gốc rv2 cho SRC/OUT/tham-chieu theo chỉ thị trực tiếp. Không dùng context executor, mạng hay GitHub; không sửa nguồn packet.

| slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| `ci-reopen-run-context-unbound` | **P2, còn mở** | `.claude/dev/packet_loop.py:2880–2884` | `probes.py`: check-run đỏ sai/rỗng `head_sha` vẫn rc0, state running, quyền ci-do được ghi. Cùng lỗi head ở accept → rc12/nguyên byte. | Kiểm head của check-run đã nối với job/suite trước khi cấp quyền đỏ; khóa bằng ca đổi đúng một trường và mutant bỏ so head. |
| `r813-mutation-evidence-incomplete` | **P2, còn mở** | `.claude/dev/packet_loop_test.py:8947–8949`, `:8961`, `:8967–8969` | Hai mutant riêng đều sống toàn bộ 101 ca r813+r834: bỏ kiểu repository.full_name; không thay checkpoint_day cũ. A/B chứng minh cả hai khác hành vi đúng. | Thêm ca M5 full_name sai kiểu và hai checkpoint hợp lệ khác hash; oracle đối chiếu quyền với hash hiện vật mới nhất; mỗi ca có mutant đúng predicate. |

## Đối chiếu lượt trước

Lý do lượt 2: lượt 1 trên `d7893933b0e02d6cebd1d7f5e17df05ea2a8de04` trả bốn lớp P2; head mới sửa `_kiem_ci` dùng chung với accept nên review lại **toàn bộ** `git diff f577ab5 79bbbdc`, không chỉ phần vá `git diff d789393 79bbbdc`. Hai diff lưu ở `FULL.diff`, `FIX.diff`.

| slug lượt 1 | phân loại | bằng chứng tự đo trên head mới |
|---|---|---|
| `ci-reopen-run-context-unbound` | **VÁ SINH LỖI MỚI**, chưa đóng lớp | Run 101 xanh, run 100 rerun sau có check ID lớn hơn: rc12; workflow khác cùng job: rc12; check mới mất app/url: rc12. Tất cả nguyên byte. Bản vá bỏ đường kiem-gate cho nhánh đỏ và mất phép so head check-run, phản chứng mới rc0. |
| `checkpoint-spec-context-unbound` | **ĐÃ VÁ THẬT** | Cả cho_phep_va và cho_phep_day: hash đúng rc0; thiếu hash rc7/sai lược đồ; hash sai rc7/['spec_hash']; các lần từ chối nguyên byte. Mutant bỏ so hash bị giết đúng rc7→0. |
| `checkpoint-nested-scope-unvalidated` | **ĐÃ VÁ THẬT** | List/object lồng trong pham_vi ở cả hai phạm vi: rc7/sai lược đồ, không traceback, state nguyên byte. Checkpoint đúng vẫn rc0. |
| `r813-mutation-evidence-incomplete` | **VÁ HỜ ở cấp lớp: các biểu hiện cũ đã vá, còn lỗ cùng nguyên nhân** | Mutant slug cũ được thay bằng r812_bo_slug_trong_bang, chết đúng rc11→0 và baseline CI hợp lệ vẫn xanh. Đã có mutant hai nguyên nhân; bỏ ghi quyền đẩy, bỏ generation, bỏ refs duy nhất và bỏ kiểu path đều bị giết. Tuy nhiên hai mutant bổ sung dưới đây sống 101/101, nên chưa đóng lớp độ phủ. |

## F1 — thiếu head của check-run trên đường CI đỏ

`_kiem_ci` kiểm head của workflow run và job, nối URL job với check-run, so suite, app, repo và ID mới nhất. Nhánh mới chỉ kiểm status/conclusion của check-run rồi `continue`; phép so `r['head_sha'] == h` nằm trong `cmd_kiem_gate` ở dòng 2374, bị bỏ qua khi `do=True`.

Phép đo `python -B -W ignore out/probes.py` dựng approved_pending qua lease và H thật của fixture; workflow run/job/H/connector đều trên head từ state. Chỉ thay `check_runs[0].head_sha` thành SHA khác: rc0, stdout `mo-lai ci-do ... state running`, bộ đếm ci-gate=1, quyền chứa SHA ứng viên dù bằng chứng check-run thuộc SHA khác. Chuỗi head rỗng cũng rc0. Đây là kiểm nhất quán R theo I7, không đòi máy chứng minh tính chân thực GitHub. `red_valid` rc0 là đối chứng; `accept_check_head_other` rc12, state nguyên byte.

**Vá ở đâu/thế nào:** nối thêm head check-run vào predicate ngữ cảnh dùng cho kết luận đỏ, hoặc gom kiểm ngữ cảnh chung trước khi phân nhánh xanh/đỏ. Không bỏ kiểm default của accept. **Ca khóa:** run/job đúng head, check-run sai head; biến thể rỗng; baseline đỏ đúng head. Mutant bỏ riêng so head phải khiến ca âm đỏ vì rc0, không phải traceback. **Nguy cơ khi vá:** lọc bỏ check sai head rồi rơi về check cũ; phải từ chối readback mâu thuẫn, đồng thời giữ kiểm run/attempt mới nhất và kết luận đỏ cho phép. Không đưa patch sản phẩm trong verdict này.

## F4 — hai chốt chưa được suite bảo vệ

Đây là nợ nghiệm thu #813 tiếp nối lượt 1, không mở lại nợ P3 ngoài phạm vi của #834. Candidate xử lý đúng hai đầu vào bên dưới; lỗi được phân hạng là thiếu bằng chứng phản chứng của suite, không phải nói candidate đang nhận chúng.

1. `extra_m5_full_name`: chỉ thay predicate `type(r['repository'].get('full_name')) is str` bằng True, vẫn giữ kiểm repository là dict. Toàn bộ 38 ca #813 + 63 ca #834 xanh. A/B `fullname_candidate` thêm run 101 in_progress với repository.full_name là số: candidate rc12/KHÔNG ĐO ĐƯỢC, nguyên byte; `fullname_mutant` rc0/accepted dựa run 100 xanh. Ca thiếu repository hiện tại không khóa predicate full_name; đây chính là M5.
2. `extra_checkpoint_replace`: giữ `st.get('checkpoint_day')` nếu đã có, chỉ cấp quyền lần đầu. Cũng sống 101/101. A/B cấp hai checkpoint hợp lệ khác byte trên master cục bộ, cùng packet/generation/head/spec và phạm vi cho_phep_day. Candidate rc0 và quyền khớp hash hiện vật thứ hai; mutant rc0, history ghi hiện vật thứ hai nhưng quyền vẫn giữ hash thứ nhất. Không thử tiêu thụ quyền đẩy (#816 ngoài phạm vi). Đây là vế **bị thay bởi sự kiện mới hơn** của I6, nằm ngay trong cửa #813.

**Vá:** thêm ca đổi full_name thành số/thiếu ở run mới hơn; thêm chuỗi hai checkpoint hợp lệ khác hash. So đầy đủ generation/sha/hash thực tính của hiện vật mới, không chỉ chiều dài 64 của hash. Khai hai mutant đúng predicate và đối chứng dương. **Nguy cơ:** mutant chết do ca dựng nền bị hỏng hoặc lược đồ khác; ghi rc/thông điệp và yêu cầu A/B chứng minh đầu vào sai thực sự đi lọt dưới mutant. Bảo toàn trần 450 dòng bằng gộp dữ liệu ca. Cặp neo/thay đã chạy và JSON toàn văn ở `extra_*/mutation.json`, `extra_*/results.json`, `more_probes/results.json`.

## Đối chiếu từng ca bắt buộc của nghiêm thu

Mỗi ca trong bảng dưới PASS trên candidate. Cột cuối là ngoại lệ thực đo của đúng ca trên mutant; tất cả là AssertionError, không có CliSapDo/traceback được tính điểm. Tên mutant dùng chung #812/#834 được giữ nguyên vì chính mục MUTANTS của candidate đã nối thêm ca #813.

| yêu cầu | ca r813 | mutant khai báo | lỗi đo trên mutant / kết luận |
|---|---|---|---|
| Chạm trần qua mo-lai → blocked | `r813_cham_tran_mo_lai` | `r813_mo_lai_khong_xet` | AssertionError: r813 bước 1: đòi rc=3, được rc=0; stderr='' — đúng chốt |
| Cùng nguyên nhân, hai comment ID → chung bộ đếm | `r813_cung_slug_hai_id` | `r813_dem_theo_id` | AssertionError: r813 bước 4: đòi rc=3, được rc=0; stderr='' — đúng chốt |
| Đối chứng: hai nguyên nhân độc lập đếm riêng | `r813_hai_slug_doc_lap` | `r813_gop_nguyen_nhan` | AssertionError: r813 bước 4: đòi rc=0, được rc=3; stderr='cùng finding-id lặp tới trần (gop×2; trần 2) — packet về blocked. Lặp lại nghĩa là bản vá không trúng gốc; ghi failure evidence + handoff rồi dừng.' — đúng chốt |
| Slug không có trong H → từ chối | `r813_slug_ngoai_bien_nhan` | `r812_bo_slug_trong_bang` | AssertionError: r813 bước 0: đòi rc=11, được rc=0; stderr='' — đúng chốt |
| begin-attempt ở trần → từ chối | `r813_begin_attempt_cham` | `r813_begin_khong_xet` | AssertionError: r813 bước 2: đòi rc=3, được rc=0; stderr='' — đúng chốt |
| Cửa khép lượt không bị chặn | `r813_cua_khep_khong_chan` | `r813_chan_cua_khep` | AssertionError: r813 bước 3: đòi rc=0, được rc=3; stderr='cùng finding-id lặp tới trần (ci-gate×1; trần 1) — packet về blocked. Lặp lại nghĩa là bản vá không trúng gốc; ghi failure evidence + handoff rồi dừng.' — đúng chốt |
| mo-lai không finding → từ chối | `r813_khong_finding` | `r813_bo_tap_rong` | AssertionError: r813 bước 0: đòi rc=2, được rc=0; stderr='' — đúng chốt |
| Connector chỉ phủ tập con P0–P2 → từ chối | `r813_connector_tap_con` | `r813_tap_con_lot` | AssertionError: r813 bước 0: đòi rc=11, được rc=0; stderr='' — đúng chốt |
| CI đỏ và connector P1 cùng head | `r813_ci_va_p1_cung_head` | `r813_bo_ci_do` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' — đúng chốt |
| Connector đến sau CI | `r813_connector_sau_ci` | `r813_chi_tu_approved` | AssertionError: r813 bước 1: đòi rc=0, được rc=8; stderr="mo-lai connector không chạy từ 'running' (đòi approved_pending của packet áp ADR-0054, hoặc running mở lại bằng ci-do cùng generation)" — đúng chốt |
| Checkpoint chỉ trên nhánh khác → từ chối | `r813_checkpoint_nhanh_khac` | `r813_checkpoint_ref_tuy_y` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' — đúng chốt |
| Checkpoint của packet khác → từ chối | `r813_checkpoint_packet_khac` | `r813_bo_packet_checkpoint` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' — đúng chốt |
| Dùng cho_phep_va làm quyền đẩy → từ chối | `r813_va_lam_quyen_day` | `r813_moi_pham_vi_la_du` | AssertionError: r813 bước 0: đòi rc=7, được rc=0; stderr='' — đúng chốt |
| M5: run mới in_progress thiếu repository | `r813_m5_run_moi_thieu_repository` | `r813_m5_bo_repository` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' — đúng chốt |
| M5: path sai kiểu | `r813_m5_run_path_sai_kieu` | `r813_m5_bo_path` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' — đúng chốt |
| M5: head_sha sai kiểu | `r813_m5_run_head_sai_kieu` | `r813_m5_bo_head_sha` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' — đúng chốt |

Connector đến sau CI còn có `r813_ci_do_doi_connector_xong`: chết ở bước CI đầu tiên với rc12 thay vì 0 vì đòi connector đã xong. Cả hai vế của yêu cầu được đo. Đối chứng M5 “mọi ca r834 hiện có vẫn đạt”: **63/63 PASS**, không skipped. Bảng đầy đủ 38 ca, kể cả các ca phụ ngoài danh sách nghiêm thu, ở `baseline_r813_r834/results.json`.

## Audit toàn bộ mutant khai báo liên quan #813

**36 mutant, 40 quan hệ mục tiêu, 108 đối chứng khác họ PASS.** Trong đó 32 mutant tên r813_ và 4 mutant dùng chung được nối ca r813. Các mỏ neo đều tồn tại duy nhất. Mỗi ngoại lệ mục tiêu đã được đọc cả tên ca, lớp và lý do. Các ca dương cùng họ bổ sung ghi trong JSON: mutant gộp nguyên nhân làm sai cả bộ đếm dương, mutant đếm ID làm sai ca connector dương; đó là đúng ngữ nghĩa đột biến bộ đếm, không phải CLI sập. Mutant slug mới giữ cả hai đối chứng dương.

| mutant | ca đích | exception/thông điệp thực đo | đánh giá |
|---|---|---|---|
| `r812_bo_slug_trong_bang` | `r812_slug_ngoai_bang_lop` | AssertionError: r812 review ['bn', 'ids', 'lop', 'verdict']: đòi rc=11, được rc=0; stderr='' | Giết đúng chốt |
| `r812_bo_slug_trong_bang` | `r813_slug_ngoai_bien_nhan` | AssertionError: r813 bước 0: đòi rc=11, được rc=0; stderr='' | Giết đúng chốt |
| `r834_bo_app` | `r834_check_app_khac` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' | Giết đúng chốt |
| `r834_bo_app` | `r813_ci_do_app_khac` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' | Giết đúng chốt |
| `r834_bo_path_workflow` | `r834_check_workflow_khac` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' | Giết đúng chốt |
| `r834_bo_path_workflow` | `r813_ci_do_workflow_khac` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' | Giết đúng chốt |
| `r834_run_cu_nhat` | `r834_run_moi_nhat_do` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr="CẢNH BÁO: 'gate (ubuntu-latest)' có 1 run ở suite khác (300) — bỏ qua\nCẢNH BÁO: 'gate-cong-cu-gop (ubuntu-latest)' có 1 run ở suite khác (301) — bỏ qua\nCẢNH BÁO: 'gate-ops (ubuntu-latest)' có 1 run ở suite khác (302) — bỏ qua\nCẢNH BÁO: 'gate-packet-loop (ubuntu-latest)' có 1 run ở suite khác (303) — bỏ qua\nCẢNH BÁO: 'gate-registry (ubuntu-latest)' có 1 run ở suite khác (304) — bỏ qua" | Giết đúng chốt |
| `r834_run_cu_nhat` | `r813_ci_do_run_moi_xanh` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' | Giết đúng chốt |
| `r813_bo_ci_do` | `r813_ci_va_p1_cung_head` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' | Giết đúng chốt |
| `r813_ci_do_nhan_xanh` | `r813_ci_khong_do` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' | Giết đúng chốt |
| `r813_ci_do_bo_check_do` | `r813_ci_do_check_xanh_job_do` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' | Giết đúng chốt |
| `r813_gop_nguyen_nhan` | `r813_hai_slug_doc_lap` | AssertionError: r813 bước 4: đòi rc=0, được rc=3; stderr='cùng finding-id lặp tới trần (gop×2; trần 2) — packet về blocked. Lặp lại nghĩa là bản vá không trúng gốc; ghi failure evidence + handoff rồi dừng.' | Giết đúng chốt |
| `r813_bo_ghi_quyen_day` | `r813_checkpoint_day` | AssertionError: r813: nội dung quyền sai — rc0 nhưng checkpoint_day vắng (toàn bộ state trong JSON). | Giết đúng chốt |
| `r813_bo_generation_quyen_ci` | `r813_quyen_ci_khac_generation` | AssertionError: r813 bước 2: đòi rc=8, được rc=0; stderr='' | Giết đúng chốt |
| `r813_bo_refs_duy_nhat` | `r813_refs_lap` | AssertionError: r813 bước 0: đòi rc=11, được rc=0; stderr='' | Giết đúng chốt |
| `r813_bo_spec_hash_checkpoint` | `r813_checkpoint_spec_lech` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' | Giết đúng chốt |
| `r813_bo_mien_pham_vi` | `r813_checkpoint_pham_vi_la` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' | Giết đúng chốt |
| `r813_m5_bo_path` | `r813_m5_run_path_sai_kieu` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' | Giết đúng chốt |
| `r813_bo_tap_rong` | `r813_khong_finding` | AssertionError: r813 bước 0: đòi rc=2, được rc=0; stderr='' | Giết đúng chốt |
| `r813_tap_con_lot` | `r813_connector_tap_con` | AssertionError: r813 bước 0: đòi rc=11, được rc=0; stderr='' | Giết đúng chốt |
| `r813_chi_tu_approved` | `r813_connector_sau_ci` | AssertionError: r813 bước 1: đòi rc=0, được rc=8; stderr="mo-lai connector không chạy từ 'running' (đòi approved_pending của packet áp ADR-0054, hoặc running mở lại bằng ci-do cùng generation)" | Giết đúng chốt |
| `r813_ci_do_doi_connector_xong` | `r813_connector_sau_ci` | AssertionError: r813 bước 0: đòi rc=0, được rc=12; stderr='connector chưa xong trên 30ef21147f548482ddfad519e79a0734e2870273: không review hoàn tất/kết luận nào của chatgpt-codex-connector[bot]' | Giết đúng chốt |
| `r813_dem_theo_id` | `r813_cung_slug_hai_id` | AssertionError: r813 bước 4: đòi rc=3, được rc=0; stderr='' | Giết đúng chốt |
| `r813_mo_lai_khong_xet` | `r813_cham_tran_mo_lai` | AssertionError: r813 bước 1: đòi rc=3, được rc=0; stderr='' | Giết đúng chốt |
| `r813_begin_khong_xet` | `r813_begin_attempt_cham` | AssertionError: r813 bước 2: đòi rc=3, được rc=0; stderr='' | Giết đúng chốt |
| `r813_chu_kho_khong_xet` | `r813_chu_kho_cham_tran` | AssertionError: r813 bước 2: đòi rc=3, được rc=0; stderr='' | Giết đúng chốt |
| `r813_chan_cua_khep` | `r813_cua_khep_khong_chan` | AssertionError: r813 bước 3: đòi rc=0, được rc=3; stderr='cùng finding-id lặp tới trần (ci-gate×1; trần 1) — packet về blocked. Lặp lại nghĩa là bản vá không trúng gốc; ghi failure evidence + handoff rồi dừng.' | Giết đúng chốt |
| `r813_xet_truoc_dau_vao` | `r813_xet_dung_sau_dau_vao` | AssertionError: r813 bước 2: đòi rc=11, được rc=3; stderr='cùng finding-id lặp tới trần (ci-gate×1; trần 1) — packet về blocked. Lặp lại nghĩa là bản vá không trúng gốc; ghi failure evidence + handoff rồi dừng.' | Giết đúng chốt |
| `r813_checkpoint_ref_tuy_y` | `r813_checkpoint_nhanh_khac` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' | Giết đúng chốt |
| `r813_bo_packet_checkpoint` | `r813_checkpoint_packet_khac` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' | Giết đúng chốt |
| `r813_moi_pham_vi_la_du` | `r813_va_lam_quyen_day` | AssertionError: r813 bước 0: đòi rc=7, được rc=0; stderr='' | Giết đúng chốt |
| `r813_checkpoint_dung_lai` | `r813_checkpoint_day_dung_lai` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' | Giết đúng chốt |
| `r813_va_ve_running_khong_tieu` | `r813_checkpoint_va` | AssertionError: r813: đòi {'state': 'running', 'mo_lai_tu': None}, được {'state': 'running', 'mo_lai_tu': {'generation': 1, 'nguyen_nhan': 'connector', 'sha': '30ef21147f548482ddfad519e79a0734e2870273'}} | Giết đúng chốt |
| `r813_m5_bo_repository` | `r813_m5_run_moi_thieu_repository` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' | Giết đúng chốt |
| `r813_lop_bo_hang` | `r813_connector_lop_p3` | AssertionError: r813 bước 0: đòi rc=11, được rc=0; stderr='' | Giết đúng chốt |
| `r813_bo_head_checkpoint` | `r813_checkpoint_head_lech` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' | Giết đúng chốt |
| `r813_bo_generation_checkpoint` | `r813_checkpoint_generation` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' | Giết đúng chốt |
| `r813_bo_nguoi_quyet` | `r813_checkpoint_nguoi_quyet` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' | Giết đúng chốt |
| `r813_cho_chu_kho_khong_quyen` | `r813_state_cho_chu_kho_mat_quyen` | AssertionError: r813 bước 2: đòi rc=8, được rc=0; stderr='' | Giết đúng chốt |
| `r813_m5_bo_head_sha` | `r813_m5_run_head_sai_kieu` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' | Giết đúng chốt |

Hai mutant #834 có mỏ neo được sửa trong diff (`r834_bo_attempt_moi_nhat`, `r834_bo_job_xanh`) cũng được chạy riêng: mỗi mutant giết đúng ca r834 tương ứng bằng AssertionError rc12→0; 6/6 đối chứng khác họ PASS. Xem `shared_mutants/results.json`.

Ba ca r813 không có tên đích trong MUTANTS: `r813_ci_do_running`, `r813_connector_cho_chu_kho` (đã chạy thêm làm đối chứng dương trong mọi mutant) và `r813_checkpoint_pham_vi_long`. Không suy từ thiếu target rằng chúng hoàn toàn không giết gián tiếp mutant nào. Không tính riêng số tên thiếu thành finding.

## Bất biến và phạm vi review không lọc

| bất biến / mục tiêu | kết quả |
|---|---|
| I1 / M2–M3 | mo-lai dùng H changes_requested qua validator canon; checkpoint dùng Đ: fetch master, ls-remote khớp OID rồi git show đúng OID. R chỉ bổ sung. |
| I2 | Không đổi đường cấp lease; fixture dựng H/Đ/R và regression r812 chạy thật trên bare repo cục bộ. Không xác minh lease online. |
| I3 | Finding rỗng, hạng sai, refs trùng/thiếu/thừa/sai kiểu đều từ chối trong các ca/probe. failure, timed_out, startup_failure được nhận; success/cancelled/skipped/neutral/action_required/unknown bị chặn. |
| I4 | Ca âm bắt buộc và probe kiểm byte state. Lỗi đầu vào đã đo đều nguyên byte; ca hợp lệ chạm trần ghi finding/history rồi blocked. F1 là lỗi nhận sai bằng chứng, không phải lỗi từ chối. |
| I5 / M1 | Hai cửa mới gọi chung _xet_dung sau xác thực; mutant xét sớm bị giết vì rc3 thay rc11. begin-attempt chặn trần; record-review khép lượt vẫn chạy. |
| I6 | Candidate thay mo_lai_tu ci-do bằng connector trên source head; cấp vá tiêu thụ mo_lai_tu. Checkpoint đẩy mới thay checkpoint cũ đúng hash; dùng lại cùng hiện vật/phạm vi bị chặn. Thiếu chốt test vế thay quyền: F4. Tiêu thụ ở cửa đẩy dành #816. |
| I7 | Connector vẫn neo repo/PR/head và đủ trang theo ID phân biệt. Nhánh accept giữ p0p2=None, không nhận P0–P2/connector chưa xong. CI đỏ còn F1. |
| I8 | Dùng đúng _du_dieu_kien_approve và chuẩn hóa canon, không thêm chuẩn danh tính riêng. Regression r812 hỗ trợ. |
| I9 | 63/63 r834 và 148/148 r812 được chọn PASS; state cũ vắng mo_lai_tu/checkpoint_day vẫn đọc được. Không suy ra full suite 977/977. |
| I10 | Probe H lệch packet/generation/SHA/spec_hash/verdict đều rc11/nguyên byte; checkpoint đủ tuple đúng nhận, thiếu/sai hash bị chặn. |
| I11 | Slug từ bảng H, history mo_lai cộng vào findings; hai ID cùng slug chung bộ đếm, hai nguyên nhân độc lập đếm riêng. Mutant đúng predicate của slug hiện giết đúng ca. |
| M5 | Candidate kiểm kiểu mọi run trước lọc. 17 biến thể path/head/repository/full_name của run mới đều rc12/KHÔNG ĐO ĐƯỢC và nguyên byte; thiếu test khóa full_name: F4. |

Điều kiện vào mo-lai lấy head từ state: approved_pending dùng pending_sha; running chỉ nhận connector với quyền ci-do cùng generation và dùng SHA nguồn trong quyền. CLI không có tham số chọn head. H/connector đều đối chiếu nguồn này. Cửa chu-kho-duyet chỉ đọc origin/master sau fetch/ls-remote; không lấy checkpoint ở HEAD tùy ý. Không dựng race remote thật trong phiên offline. Không thấy mâu thuẫn đặc tả–hợp đồng accept cần đổi thiết kế; M4/đồ thị cho_chu_kho đã được loại khỏi r2 theo chỉ thị, không tính hạng.

## Định danh và lệnh đã chạy

`IDENTITY.json`: HEAD đúng 79bbbdc…, tree `b0546491c57c4600a9c4a6cffde42da2abeef68a`, origin/master/base `f577ab5b467510f3fa7ed27107dc2eab539d3bef`. merge-base --is-ancestor rc0; symbolic-ref rc1 đúng detached; is-shallow-repository=false; .git là thư mục; status/worktree/index sạch. Hai hash ở dòng 3 được tính từ bytes và khớp. Diff đúng 2 path: code +153/-11, test +203/-3 = **356 dòng thêm ≤450**. diff --check rc0.

Lease bản chép có thêm đường handoff trong effective_write_set nhưng ghi rõ handoff chỉ trên nhánh lease; diff sản phẩm thực tế chỉ hai đường đặc tả cho phép. Không mở rộng phạm vi theo đường handoff đó.

Tất cả thử nghiệm dùng `out/copy` hoặc mutant riêng dưới OUT; `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=OUT/tmp`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_OPTIONAL_LOCKS=0`, `GIT_ALLOW_PROTOCOL=file`, bản sao core.abbrev=7. Các fetch/push/ls-remote trong fixture chỉ với bare repo cục bộ dưới OUT; không push/fetch repository packet.

Đã đọc chon.py và dotbien.py lượt này trước khi dùng logic: cả hai có sys.exit theo lỗi; dotbien cắt thông điệp. Runner độc lập dùng cùng chay_suite/_phan_loai_dot_bien/_doi_chung_khac_ho/_phan_loai_giet nhưng giữ toàn văn exception, kiểm inventory/neo và thêm đối chứng cùng họ. Không dùng rc0 trần để tính pass.

| lệnh | rc | bằng chứng dương / artifact |
|---|---:|---|
| `python -B -W ignore out/run_review.py baseline_r813_r834 r813_,r834_` | 0 | 101/101 = 38 r813 + 63 r834 PASS; baseline_r813_r834/results.json |
| `python -B -W ignore out/run_review.py baseline_r812 r812_` | 0 | 148/148 PASS; một ca không chạy có chủ ý dưới đây; baseline_r812/results.json |
| `python -B -W ignore out/run_review.py baseline_codepage stdout_cp` | 0 | 2/2 PASS, có chạy mo-lai và chu-kho-duyet dưới cp1252/cp1258; đây là ép encoding trên Linux, không phải chạy Windows |
| `python -B -W ignore out/run_review.py mutants` | 0 | 36 mutant / 40 quan hệ GIẾT đúng / 108 đối chứng khác họ PASS; mutants/results.json |
| Driver heredoc Python dùng hai MUTANTS #834 đã đổi mỏ neo | 0 | 2/2 mục tiêu GIẾT, 6/6 đối chứng PASS; shared_mutants.log và JSON lưu nguyên cặp thay |
| `python -B -W ignore out/run_review.py extra_m5_full_name` | 0 | Mutant **SỐNG 101/101**, không phải pass nghiệm thu; extra_m5_full_name/results.json |
| `python -B -W ignore out/run_review.py extra_checkpoint_replace` | 0 | Mutant **SỐNG 101/101**; extra_checkpoint_replace/results.json |
| `python -B -W ignore out/probes.py` | 0 | 42 phép đo CLI; probes/results.json ghi rc/stdout/stderr/state/byte equality |
| `python -B -W ignore out/more_probes.py` | 0 | 19 phép đo refs/H và A/B; more_probes/results.json |
| `python -B out/copy/.claude/dev/packet_loop.py doctrine-scan --root out/copy` | 0 | 10 tệp, 0 chỗ chép doctrine; GATES.json |
| `python -B out/copy/.claude/dev/packet_loop.py adr-song --root out/copy` | 0 | 55 ADR / 55 dòng §20, khớp 1–1, ngoại lệ 0016 có sẵn; GATES.json |
| `python -B out/finalize.py` | 0 | Inventory/số đo khớp, source không delta byte/mode, final Git checks sạch |

Tổng ca nền chọn lọc: **251/251 PASS** (101+148+2), không failed/skipped trong tập đã chạy. Các nhóm suite có log/stdout, stderr và summary.json; các probe lưu kết quả từng phép trong results.json. rc0 của probe nghĩa chạy xong phép đo, không có nghĩa hành vi sai đã thành đúng.

## Giới hạn, ngoài phạm vi và toàn vẹn

`not_run`: full suite `python .claude/dev/packet_loop_test.py` (977 ca và mọi mutant); CI online, Windows thật, bare Ruff lint, phần còn lại các mutant #812/#834. Ca `r812_r4_own_parent` được loại trước chạy vì tạo nội dung đường dẫn có thành phần cha; không tự soạn hướng thử thoát cây theo mục 5 prompt. Hướng thử chỉ mô tả: checkpoint/receipt có đường dẫn hoặc liên kết dẫn ra ngoài cây cần bị từ chối trước đọc/ghi ngoài phạm vi, state giữ nguyên. Không tạo payload đó. Các symlink hồi quy được chạy trỏ trong cây fixture.

M4/protocol §4/§12, #814, generation kế tiếp #815, ghi đẩy/tiêu thụ quyền ở #816 và kích hoạt ADR-0054 ngoài phạm vi. Nợ P3 #834 required-mutation-coverage-missing về neo head issue comment/kiểu ID trang không được đánh giá lại hay khai đã đóng.

Snapshot nguồn đầu/cuối: **6982 → 6982 tệp thường, 0 delta byte/mode, 0 symlink**, gồm .git, tracked/untracked/ignored. HEAD/tree/ref/status/diff/index kiểm lại; code/test ở bản sao nền vẫn cùng byte với SRC. Xem SOURCE_INITIAL.json, SOURCE_FINAL.json, SOURCE_INTEGRITY.json, FINAL_CHECKS.json. Đây là so hai mốc, không phải giám sát mọi write trong lịch sử. Sandbox thực tế workspace-write; nguồn được đối xử chỉ đọc, mọi artifact/fixture reviewer ghi ở OUT.
