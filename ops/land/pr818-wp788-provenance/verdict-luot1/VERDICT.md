verdict: blocked

Đã nhận chỉ thị review wp788; đang xác minh preflight.

Preflight: HEAD `e995730464da03223cf636e49ad32e220c6ec720`, tree `a0729f20a384f197a2b3a9590d4348714e455dee`; spec r1 sha256 `82dc170446c3a4431739a3effbec8cb55adadc13d69f5c510f8782a2b45eb54e` khớp. Checkout detached; trước review chỉ có `.review/` untracked do người giao cung cấp. Provider `openai_codex`, execution_surface `codex_cli`, transport `machine`; model được khai trong session là GPT-6, không có selector cụ thể hơn được đo. Review Class `sensitive`.

Suite nền đã khởi chạy `2026-10-17T18:02:07.699673+00:00`: `PYTHONDONTWRITEBYTECODE=1 python -B .claude/dev/packet_loop_test.py > .review/suite.out 2>&1`; wrapper PID `4` lưu rc thật vào `.review/suite.rc`. Trạng thái hiện tại **not_run/pending completion**, chưa tính pass.

Scratch ngoài kho: `/tmp/wp788-review-8ixnugpw`. Mọi bản sao đột biến đặt tại đây. Chỉ ghi artifact do prompt cho phép trong `.review/`; cây tracked read-only.

Kiểm diff hoàn tất: `git diff --numstat d8b15cb0730c85e7019aee627c3bfa645a6d3eaf HEAD` rc=0: `41 10 .claude/dev/packet_loop.py`, `197 16 .claude/dev/packet_loop_test.py`; **2 tệp / 238 dòng thêm**, trong write set và trần ≤3/≤300. Đã đọc toàn bộ diff hai tệp. Raw diff/preflight ở scratch.

Đính chính trạng thái suite: lần khởi chạy bằng detached wrapper chưa tạo `suite.out`, không có completion evidence và KHÔNG được tính pass. Đã khởi chạy lại bằng shell background + `wait` trong exec session `15243` để giữ tiến trình; vẫn **pending**, rc thật sẽ nằm `.review/suite.rc`. Lần chạy bảng đột biến đầu thiếu thư mục output: setup_failed (rc của shell không chứng minh audit); tạo thư mục rồi đã chạy lại TOÀN BỘ bảng trong một lượt, kết quả đang phân loại.

Audit TOÀN BỘ `kg_*` đã chạy xong trong một lượt: `bash .review/mut_all.sh "$PWD/.claude/dev" kg_ /tmp/wp788-review-8ixnugpw/mutants > .review/mut_all.out 2>&1`, rc shell=0 (không dùng riêng rc này làm bằng chứng). Đã parse và đọc từng thông điệp chết: **34 đột biến / 82 ô ca đích; 0 sống; 0 thông điệp chứa Traceback**. Mỗi ô đổi rc hoặc đúng assertion tính chất (cảnh báo/help/suite output). N1 đổi rc=2→12 vẫn là bắt đúng hợp đồng mã lỗi đối số; không nhận rc=12 như pass. Giữ riêng từng ô dưới đây để không suy từ tổng.

| Đột biến | Ca đích | Phân loại | Output thật |
|---|---|---|---|
| `kg_bo_status_rieng` | `kg_m3_in_progress_success` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_conclusion_rieng` | `kg_m3_ket_luan_skipped` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_conclusion_rieng` | `kg_m3_ket_luan_neutral` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_conclusion_rieng` | `kg_m3_ket_luan_failure` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_conclusion_rieng` | `kg_m3_ket_luan_timed_out` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_conclusion_rieng` | `kg_m3_ket_luan_action_required` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_conclusion_rieng` | `kg_m3_ket_luan_stale` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_conclusion_rieng` | `kg_m3_ket_luan_None` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_khoa_trung` | `kg_m2_khoa_trung_id_False` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_khoa_trung` | `kg_m2_khoa_trung_id_True` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_khoa_trung` | `kg_m2_khoa_trung_name_False` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_khoa_trung` | `kg_m2_khoa_trung_name_True` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_khoa_trung` | `kg_m2_khoa_trung_head_sha_False` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_khoa_trung` | `kg_m2_khoa_trung_head_sha_True` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_khoa_trung` | `kg_m2_khoa_trung_status_False` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_khoa_trung` | `kg_m2_khoa_trung_status_True` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_khoa_trung` | `kg_m2_khoa_trung_conclusion_False` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_khoa_trung` | `kg_m2_khoa_trung_conclusion_True` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_khoa_trung` | `kg_m2_khoa_trung_check_suite_False` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_khoa_trung` | `kg_m2_khoa_trung_check_suite_True` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_khoa_trung` | `kg_m2_khoa_trung_check_runs` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_khoa_trung` | `kg_m2_khoa_trung_total_count` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_hang_ngoai_json` | `kg_m2_hang_ngoai_json_NaN_False` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_hang_ngoai_json` | `kg_m2_hang_ngoai_json_NaN_True` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_hang_ngoai_json` | `kg_m2_hang_ngoai_json_Infinity_False` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_hang_ngoai_json` | `kg_m2_hang_ngoai_json_Infinity_True` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_hang_ngoai_json` | `kg_m2_hang_ngoai_json_-Infinity_False` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_hook_hang_ngoai_json` | `kg_m2_hang_ngoai_json_-Infinity_True` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_sha_re` | `kg_m1_head_7_ky_tu` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=2, được rc=0; stderr='' |
| `kg_bo_kiem_ten_rong` | `kg_m1_bat_buoc_rong` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=2, được rc=12; stderr="ĐỎ  '': VẮNG — không check-run nào mang đúng tên này trong suite 1\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" |
| `kg_bo_qua_phan_tu_thieu_truong` | `kg_m2_thieu_conclusion` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bool_la_int` | `kg_m2_id_bool` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_kiem_thieu_trang` | `kg_m2_thieu_trang` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_kiem_thieu_trang` | `kg_n5_khai_3_co_2` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_kiem_thieu_trang` | `kg_n5_khai_1_co_2` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_kiem_thieu_trang` | `kg_n5_khong_voi_mot_run` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_kiem_vang` | `kg_m3_vang` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_kiem_vang` | `kg_m3_ten_tuyet_doi` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_chon_success_bat_ky` | `kg_m3_huy_moi_nhat` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_chon_luot_cu_nhat` | `kg_m3_chay_lai_xanh` | GIẾT ĐÚNG CHỐT | AssertionError: gate phải XANH: đòi rc=0, được rc=12; stderr="ĐỎ  'gate' id=1: status='completed' conclusion='cancelled' head_sha='abababababababababababababababababababab'\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" |
| `kg_chon_luot_cu_nhat` | `kg_m2_list_nhieu_trang` | GIẾT ĐÚNG CHỐT | AssertionError: gate phải XANH: đòi rc=0, được rc=12; stderr="ĐỎ  'gate' id=1: status='completed' conclusion='cancelled' head_sha='abababababababababababababababababababab'\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" |
| `kg_chon_luot_cu_nhat` | `kg_n3_chay_lai` | GIẾT ĐÚNG CHỐT | AssertionError: gate phải XANH: đòi rc=0, được rc=12; stderr="ĐỎ  'gate' id=1: status='completed' conclusion='cancelled' head_sha='abababababababababababababababababababab'\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" |
| `kg_chon_luot_cu_nhat` | `kg_n3_chay_lai_suite_khac_cu_hon` | GIẾT ĐÚNG CHỐT | AssertionError: gate phải XANH: đòi rc=0, được rc=12; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\n  ĐỎ  'gate' id=2: status='completed' conclusion='cancelled' head_sha='abababababababababababababababababababab'\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" |
| `kg_trung_id_chon_mot` | `kg_m3_trung_id_moi_ban_phai_xanh` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_danh_sach_cam` | `kg_m3_ket_luan_skipped` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_danh_sach_cam` | `kg_m3_ket_luan_neutral` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_danh_sach_cam` | `kg_m3_ket_luan_timed_out` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_danh_sach_cam` | `kg_m3_ket_luan_action_required` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_danh_sach_cam` | `kg_m3_ket_luan_stale` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_danh_sach_cam` | `kg_m3_ket_luan_None` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_danh_sach_cam` | `kg_m3_in_progress` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_bo_so_head` | `kg_m3_head_khac` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_khop_tien_to` | `kg_m3_ten_tuyet_doi` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_xet_moi_check` | `kg_m3_ngoai_bo_qua` | GIẾT ĐÚNG CHỐT | AssertionError: gate phải XANH: đòi rc=0, được rc=12; stderr="ĐỎ  'gate' id=2: status='completed' conclusion='cancelled' head_sha='abababababababababababababababababababab'\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" |
| `kg_rc_gate_thanh_8` | `kg_m4_rc_gate_12` | GIẾT ĐÚNG CHỐT | AssertionError: gate đỏ phải trả ĐÚNG 12: đòi rc=12, được rc=8; stderr="ĐỎ  'gate' id=1: status='completed' conclusion='cancelled' head_sha='abababababababababababababababababababab'\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" |
| `kg_n1_bo_kiem_dang` | `kg_n1_check_suite_abc` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=2, được rc=12; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\n  ĐỎ  'gate': VẮNG — không check-run nào mang đúng tên này trong suite None\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" |
| `kg_n1_bo_kiem_dang` | `kg_n1_check_suite_am` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=2, được rc=12; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\n  ĐỎ  'gate': VẮNG — không check-run nào mang đúng tên này trong suite None\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" |
| `kg_n1_bo_kiem_dang` | `kg_n1_check_suite_0` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=2, được rc=12; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\n  ĐỎ  'gate': VẮNG — không check-run nào mang đúng tên này trong suite None\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" |
| `kg_n1_bo_kiem_dang` | `kg_n1_check_suite_012` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=2, được rc=12; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\n  ĐỎ  'gate': VẮNG — không check-run nào mang đúng tên này trong suite None\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" |
| `kg_n1_bo_kiem_dang` | `kg_n1_check_suite_cong` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=2, được rc=12; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\n  ĐỎ  'gate': VẮNG — không check-run nào mang đúng tên này trong suite None\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" |
| `kg_n1_bo_kiem_dang` | `kg_n1_check_suite_cach` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=2, được rc=12; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\n  ĐỎ  'gate': VẮNG — không check-run nào mang đúng tên này trong suite None\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" |
| `kg_n1_bo_kiem_dang` | `kg_n1_check_suite_unicode` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=2, được rc=12; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\n  ĐỎ  'gate': VẮNG — không check-run nào mang đúng tên này trong suite None\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" |
| `kg_n1_cho_so_0_dau` | `kg_n1_check_suite_0` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=2, được rc=12; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\n  ĐỎ  'gate': VẮNG — không check-run nào mang đúng tên này trong suite 0\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" |
| `kg_n1_cho_so_0_dau` | `kg_n1_check_suite_012` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=2, được rc=12; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\n  ĐỎ  'gate': VẮNG — không check-run nào mang đúng tên này trong suite 12\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" |
| `kg_n1_chu_so_unicode` | `kg_n1_check_suite_unicode` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=2, được rc=12; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\n  ĐỎ  'gate': VẮNG — không check-run nào mang đúng tên này trong suite 11\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" |
| `kg_n2_chi_kiem_bat_buoc` | `kg_n2_run_khong_bat_buoc_thieu_suite` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_n2_bool_la_int` | `kg_n2_suite_id_bool` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_n3_bo_loc_suite` | `kg_n3_producer` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (2) — bỏ qua" |
| `kg_n3_bo_loc_suite` | `kg_n3_vang` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua" |
| `kg_n3_bo_loc_suite` | `kg_n7_that_suite_thu_hoi` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr="CẢNH BÁO: 'chuan-bi' có 2 run ở suite khác (116911938097, 116968288225) — bỏ qua\nCẢNH BÁO: 'gate (ubuntu-latest)' có 2 run ở suite khác (116912043094, 116968376214) — bỏ qua\nCẢNH BÁO: 'gate-registry (ubuntu-latest)' có 2 run ở suite khác (116912043092, 116968376237) — bỏ qua\nCẢNH BÁO: 'gate-ops (ubuntu-latest)' có 2 run ở suite khác (116912042979, 1169683763… (đầy đủ trong mut_all.out) |
| `kg_n3_suite_cua_run_dau` | `kg_n3_chay_lai_suite_khac_cu_hon` | GIẾT ĐÚNG CHỐT | AssertionError: gate phải XANH: đòi rc=0, được rc=12; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\n  ĐỎ  'gate' id=1: status='completed' conclusion='failure' head_sha='abababababababababababababababababababab'\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" |
| `kg_n4_bo_canh_bao` | `kg_n4_canh_bao` | GIẾT ĐÚNG CHỐT | AssertionError: đòi đúng MỘT dòng cảnh báo cho 'gate': [] |
| `kg_n4_canh_bao_moi_ten` | `kg_n4_canh_bao` | GIẾT ĐÚNG CHỐT | AssertionError: tên không bắt buộc không được cảnh báo: ["CẢNH BÁO: 'khac' có 1 run ở suite khác (2) — bỏ qua"] |
| `kg_n5_quay_ve_nho_hon` | `kg_n5_khai_1_co_2` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_n5_quay_ve_nho_hon` | `kg_n5_khong_voi_mot_run` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_n5_bo_doi_co_mat` | `kg_n5_thieu` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_n5_trang_sau_thua_huong` | `kg_n5_thieu_o_trang_sau` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_n5_bo_so_giua_trang` | `kg_n5_lech_trang` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_n5_bool_la_int` | `kg_n5_bool` | GIẾT ĐÚNG CHỐT | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' |
| `kg_n6_xoa_help` | `kg_n6_help` | GIẾT ĐÚNG CHỐT | AssertionError: --help của kiem-gate thiếu '--check-suite': 'usage: packet_loop.py kiem-gate [-h] --head HEAD --check-runs CHECK_RUNS                                 --bat-buoc BAT_BUOC  options:   -h, --help            show this help message and exit   --head HEAD           SHA 40 ký tự của head cần kiểm   --check-runs CHECK_RUNS                         tệp JSON: object có `check_runs`, hoặc list trang              … (đầy đủ trong mut_all.out) |
| `kg_n6_dong_xanh_khong_suite` | `kg_m2_object_mot_trang` | GIẾT ĐÚNG CHỐT | AssertionError: dòng xanh thiếu suite 1: 'gate XANH trên abababababababababababababababababababab : gate id=1' |
| `kg_n6_dong_xanh_khong_suite` | `kg_n7_that_suite_ci` | GIẾT ĐÚNG CHỐT | AssertionError: dòng xanh thiếu suite 105371250078: 'gate XANH trên bb8c0c41d37ea5d7eddef254ea9079518e114890 : chuan-bi id=116968288225 · gate (ubuntu-latest) id=116968376214 · gate-registry (ubuntu-latest) id=116968376237 · gate-ops (ubuntu-latest) id=116968376391 · gate-packet-loop (ubuntu-latest) id=116968376298 · gate-cong-cu-gop (ubuntu-latest) id=116979365158 · gate-cong-cu (ubuntu-latest, 0) id=116968376242 · … (đầy đủ trong mut_all.out) |

Runtime identity đo từ HEADER KHỞI TẠO của đúng `runs/7e93895a/stderr.log` (không lấy từ prompt): Codex v0.163.0; model `gpt-6.1-sol`; effort `xhigh`; provider `openai`; approval `never`; sandbox `workspace-write [workdir, /tmp, $TMPDIR]`; session `01a14b06-aa9f-74f0-91d2-7b50e21ceb12`. `run.json`: run_id `7e93895a065d4545aaca0d31fd7bca35`, provider `openai_codex`, execution_surface `codex_cli`, transport `machine`. Header chỉ chứng minh CLI công bố model/effort, không chứng minh mọi request; executor identity là routing trong spec, chưa có runtime receipt executor trong phạm vi offline.

**Checkpoint H3:** đã đo cùng một ID có hai `check_suite.id` khác nhau, một bản đỏ, lệnh vẫn `rc=0` + `gate XANH`; đồng thời đo cùng ID đáp ứng hai tên bắt buộc với `total_count=1`. Ghi finding `check-run-id-identity-conflict` (P1, trục Standards/Security, lớp H3 `bang-chung-dau-vao-tin-qua-muc`). H3 kế thừa **3→4**, kích hoạt `review_rescue_checkpoint` của spec. Không tự approve, vá cây sản phẩm, gọi thêm reviewer hoặc tiếp tục vòng vá; hoàn tất ghi evidence và thu kết quả suite đã chạy.

`python -B /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.claude/dev/packet_loop.py kiem-gate --head abababababababababababababababababababab --check-suite 1 --bat-buoc gate --check-runs /tmp/wp788-review-8ixnugpw/identity-control.json`

```text
rc=0
gate XANH trên abababababababababababababababababababab (suite 1): gate id=1
```

`python -B /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.claude/dev/packet_loop.py kiem-gate --head abababababababababababababababababababab --check-suite 1 --bat-buoc gate --check-runs /tmp/wp788-review-8ixnugpw/identity-name-conflict.json`

```text
rc=0
gate XANH trên abababababababababababababababababababab (suite 1): gate id=1
```

`python -B /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.claude/dev/packet_loop.py kiem-gate --head abababababababababababababababababababab --check-suite 1 --bat-buoc gate --check-runs /tmp/wp788-review-8ixnugpw/identity-suite-conflict.json`

```text
rc=0
gate XANH trên abababababababababababababababababababab (suite 1): gate id=1
CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua
```

`python -B /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.claude/dev/packet_loop.py kiem-gate --head abababababababababababababababababababab --check-suite 1 --bat-buoc gate --check-runs /tmp/wp788-review-8ixnugpw/identity-head-conflict.json`

```text
rc=12
  ĐỎ  'gate' id=1: status='completed' conclusion='success' head_sha='cdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcd'
gate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ
```

`python -B /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.claude/dev/packet_loop.py kiem-gate --head abababababababababababababababababababab --check-suite 1 --bat-buoc gate --check-runs /tmp/wp788-review-8ixnugpw/identity-name-suite-pages.json`

```text
rc=0
gate XANH trên abababababababababababababababababababab (suite 1): gate id=1
```

`python -B /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.claude/dev/packet_loop.py kiem-gate --head abababababababababababababababababababab --check-suite 1 --bat-buoc gate --check-runs /tmp/wp788-review-8ixnugpw/identity-two-required.json --bat-buoc gate2`

```text
rc=0
gate XANH trên abababababababababababababababababababab (suite 1): gate id=1 · gate2 id=1
```

Các gate nhanh đã đo (Ruff v0.15.15; Python 3.13.16; Linux x86_64). Base được xuất từ đúng OID bằng `git archive`, cả hai vế dùng cùng executable/config, không tạo cache:

| Scope | Command | rc thật | Bằng chứng dương / lỗi nền |
|---|---|---:|---|
| base | `python -B -m ruff check --no-cache --select F /tmp/wp788-review-8ixnugpw/base/.claude/dev/packet_loop.py` | 1 | F841 Local variable `n` is assigned to but never used |
| base | `python -B /tmp/wp788-review-8ixnugpw/base/.claude/dev/packet_loop.py doctrine-scan --root /tmp/wp788-review-8ixnugpw/base` | 0 | doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine |
| base | `python -B /tmp/wp788-review-8ixnugpw/base/.claude/dev/packet_loop.py adr-song --root /tmp/wp788-review-8ixnugpw/base` | 0 | adr-song: sạch — 53 ADR trên đĩa, 53 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016']) |
| head | `python -B -m ruff check --no-cache --select F /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.claude/dev/packet_loop.py` | 1 | F841 Local variable `n` is assigned to but never used |
| head | `python -B /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.claude/dev/packet_loop.py doctrine-scan --root /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1` | 0 | doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine |
| head | `python -B /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.claude/dev/packet_loop.py adr-song --root /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1` | 0 | adr-song: sạch — 53 ADR trên đĩa, 53 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016']) |

Bare Ruff **failed** ở cả base/head: cùng 1 F841 `n` tại dòng 1804, **DELTA=0** ⇒ tiêu chí `ruff` của spec **ĐẠT**, không khai bare lint sạch. `doctrine-scan` và `adr-song` cùng rc=0 ở cả hai vế, output lần lượt `10 tệp, 0 chỗ chép doctrine` và `53 ADR / 53 dòng`; tiêu chí giữ màu **ĐẠT**. Ruff pin/probe contract không thuộc thay đổi này: **not_run**; không suy từ bare lint.

Component command: `PYTHONDONTWRITEBYTECODE=1 python -B -W ignore /tmp/wp788-review-8ixnugpw/targeted.py "$PWD"` rc=0, output **`TARGETED 88 / 88`** (86 ca `kg_*` + `stdout_cp1252`, `stdout_cp1258`). Catalog base/head được import trong các tiến trình riêng: **352→388 ca; kg 50→86; removed_kg=[]; hai ca stdout còn nguyên**. Cả 50 ca kg cũ còn mặt. Output từng tên ở `.review/targeted.out`; chưa dùng component thay kết quả full suite.

HINT TEST thuần đã được tạo ngoài kho: `/tmp/wp788-review-8ixnugpw/HINT-check-run-id-identity-conflict.patch`. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Chỉ chạy test bản sao với sản phẩm HEAD không sửa: `PYTHONDONTWRITEBYTECODE=1 python -B -W ignore /tmp/wp788-review-8ixnugpw/hint_checks.py "$PWD"` rc harness=0 (harness in dữ liệu, không phải gate pass). Output `HINT_TARGETS 5 RED 4 GREEN 1`: bốn ca mâu thuẫn chết trực tiếp `đòi rc=12, được rc=0`, một đối chứng trùng ID nhất quán xanh. Đây là bằng chứng tái hiện lỗi, KHÔNG phải bằng chứng đã vá.

```text
{
  "kg_h3_same_id_other_suite": "AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr=\"CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\"",
  "kg_h3_same_id_other_name": "AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr=''",
  "kg_h3_same_id_two_required": "AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr=''",
  "kg_h3_same_id_conflict_pages": "AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr=\"CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\"",
  "kg_h3_same_id_consistent_pages": null
}
HINT_TARGETS 5 RED 4 GREEN 1
```

## Quét toàn lớp H3 — toàn bộ đường vào và phép so

Lệnh sinh/chạy 126 probe: `PYTHONDONTWRITEBYTECODE=1 python -B /tmp/wp788-review-8ixnugpw/probe_h3.py "$PWD" > .review/probes.out 2>&1` rc=0. **120 probe có oracle trước chạy đều đúng oracle; 6 probe thăm dò không được gộp thành pass** (CLI dài và 5 ca ID bất thường). Script và `probes.json` giữ argv/rc/stdout/stderr từng lần. Lần đầu rig vô tình dùng `None` như mặc định thay vì JSON null ở `count_null`; đã sửa fixture thành object tường minh và chạy lại trọn bộ, kết quả null thật rc=12. Không ghi đó thành lỗi sản phẩm.

| Đường vào / phép so | Phép đo trên candidate | Kết luận H3 |
|---|---|---|
| `--head`: required + `SHA_RE.fullmatch` ASCII hex thường 40 ký tự | thiếu, 7 ký tự, uppercase, head khác, newline cuối | không cấp xanh |
| `--check-suite`: required + fullmatch `[1-9][0-9]*` + `int` | thiếu/abc/âm/0/012/+1/space/newline/Unicode/exponent; số 4301 chữ số | dạng sai rc=2; số dài traceback rc=1, finding P3 riêng, không phải xanh giả |
| `--bat-buoc`: parser required append; `dict.fromkeys`; `strip()` chống rỗng | thiếu, rỗng, whitespace, trùng tên; `gate` so `Gate`/suffix/newline | không vacuous pass; trùng tên đúng một lần; khớp tuyệt đối |
| `--check-runs`: Path/read_text UTF-8 + decoder; OSError/Unicode/ValueError/RecursionError | tệp vắng, JSON hỏng, root null/scalar/list rỗng, sâu 1200 cấp | rc=12 KHÔNG ĐO ĐƯỢC |
| `--help`; `--run-id` không được hỗ trợ | help; unknown flag | help có thông tin N6; unknown rc=2, không gọi gate |
| Global `--state-dir` | đọc main: chỉ chuyển `Path(a.state_dir)`, `_doc_check_runs`/`cmd_kiem_gate` không đọc state_dir | không có đường đọc state để cấp xanh; không suy quyền từ state |
| JSON object keys mọi tầng: `_cam_khoa_trung`; hằng phi JSON: `parse_constant` | khóa trùng trường run, page, `check_suite.id`; NaN/Infinity trong extra; object/list paginated | từ chối rc=12 trước lọc, không mất nhánh mâu thuẫn |
| root/page `check_runs`: list; từng item phải dict | null/string/object, phần tử thiếu trường | rc=12; không skip phần tử hỏng |
| page `total_count`: tồn tại, `type is int`, `>=0` | thiếu/null/bool/float/string/âm, zero với run | rc=12; kiểu chặt không nhận bool |
| `total_count` mọi trang bằng trang đầu (`any(t != tong_khai)`) | 2/3; trang sau thiếu; số id đúng trang đầu nhưng trang sau khác | rc=12; chốt giữa trang độc lập với chốt đếm |
| run `id`: `type is int`, đếm `len(set(id)) == total_count` | bool/string/float; trang trùng ID không bù trang thiếu; dư/thiếu; trùng nhất quán | kiểu sai/đếm sai rc=12; **chưa kiểm quan hệ ID→identity**, F01 |
| run `name`: `type is str`; so `== ten` | tên suffix, khác case, whitespace/newline; run ngoài danh sách thiếu trường | exact match đúng; **lọc tên xóa bản ghi cùng ID khác tên**, F01 |
| run `check_suite`: dict; `.id` int không bool; so `== suite` | thiếu/null/list/thiếu id/bool/string/float; suite khác id lớn/nhỏ | schema và producer độc lập đúng; **lọc suite xóa bản ghi cùng ID khác suite**, F01 |
| cảnh báo: so tên `==`, suite `!=`, sort `id`, đếm run | producer khác đỏ/xanh, tên không bắt buộc, tên bắt buộc lặp | đúng một dòng mỗi tên, không đổi rc; F01 vẫn được cấp xanh kèm cảnh báo |
| chọn newest: `max(id)` trong tập đã lọc | success cũ/cancelled mới; cancelled cũ/success mới; thứ tự đảo | đúng màu theo id lớn nhất; không chọn success tùy ý |
| duplicate newest: `id == id_max`, mọi bản ghi trong tập lọc phải xanh | conflict cùng ID/cùng tên/suite ở cả hai thứ tự; head khác | rc=12; **phạm vi lọc khiến invariant trùng ID chỉ được kiểm cục bộ**, F01 |
| run `status`: str, `== "completed"` | queued/in_progress/pending/uppercase/space; riêng in_progress+success | tất cả rc=12 |
| run `conclusion`: str hoặc null, `== "success"` | null/failure/cancelled/skipped/neutral/stale/timed_out/action_required/uppercase/space | tất cả rc=12 |
| run `head_sha`: str, `== a.head` | khác/thiếu/ngắn/uppercase/newline, kể cả duplicate id | không cấp xanh cho bản ghi được xét |
| danh sách `do` khác rỗng ⇒ 12; parser bảo đảm ≥1 tên bắt buộc | một tên đỏ giữa nhiều tên; fixture thật sai suite 14 tên vắng | không cấp xanh nếu một tên được xét đỏ/vắng |
| `app`, timestamps, metadata khác | không dùng trong hai hàm; xem phạm vi nguồn | không chứng minh producer bằng app. Không xác thực nguồn API/workflow: ngoài phạm vi theo spec |

ID 0/âm đơn lẻ được chấp nhận (probe có output), nhưng schema spec chỉ đòi int, không đòi dương; **không ghi finding cho thay đổi hợp đồng chưa được yêu cầu**. F01 dựa trên quan hệ mâu thuẫn giữa CÁC bản ghi cùng ID và suy diễn “hai check từ một ID”, không dựa vào đòi gọi API/xác thực tệp thật. Không mở rộng scope sang app, run-id, land hay provenance workflow.

## Các hướng săn độc lập

```text
HƯỚNG 1: Decoder xóa mâu thuẫn ở tầng lồng
  giả thuyết : nếu khóa id trong check_suite lặp được decoder chọn vế cuối thì producer khác có thể biến thành suite neo
  lệnh       : /usr/bin/python -B /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.claude/dev/packet_loop.py kiem-gate --head abababababababababababababababababababab --check-suite 1 --bat-buoc gate --check-runs /tmp/wp788-review-8ixnugpw/inputs/duplicate_suite_id.json
  output     : rc=12
               KHÔNG ĐO ĐƯỢC: /tmp/wp788-review-8ixnugpw/inputs/duplicate_suite_id.json: không đọc được như JSON (ValueError: khoá trùng 'id' — bằng chứng mâu thuẫn)
  kết luận   : KHÔNG PHẢI LỖI
```

```text
HƯỚNG 2: Phần tử không được chọn làm rỗng schema
  giả thuyết : nếu run không bắt buộc thiếu status bị bỏ qua thì file bằng chứng hỏng vẫn xanh
  lệnh       : /usr/bin/python -B /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.claude/dev/packet_loop.py kiem-gate --head abababababababababababababababababababab --check-suite 1 --bat-buoc gate --check-runs /tmp/wp788-review-8ixnugpw/inputs/nonrequired_missing_status.json
  output     : rc=12
               KHÔNG ĐO ĐƯỢC: /tmp/wp788-review-8ixnugpw/inputs/nonrequired_missing_status.json: trang 0 check_runs[1] thiếu/sai kiểu trường ['status']
  kết luận   : KHÔNG PHẢI LỖI
```

```text
HƯỚNG 3: Trang lặp giả đủ số run
  giả thuyết : nếu lặp cùng ID được cộng hai lần thì trang mất có thể bị che
  lệnh       : /usr/bin/python -B /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.claude/dev/packet_loop.py kiem-gate --head abababababababababababababababababababab --check-suite 1 --bat-buoc gate --check-runs /tmp/wp788-review-8ixnugpw/inputs/pages_duplicated_id_hides_missing.json
  output     : rc=12
               KHÔNG ĐO ĐƯỢC: /tmp/wp788-review-8ixnugpw/inputs/pages_duplicated_id_hides_missing.json: `total_count` khai 2 mà có 1 id — thiếu trang (`--paginate --slurp`)
  kết luận   : KHÔNG PHẢI LỖI
```

```text
HƯỚNG 4: Đổi producer bằng id lớn hơn
  giả thuyết : nếu run success suite khác có quyền hơn run failure suite neo thì xanh sai
  lệnh       : /usr/bin/python -B /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.claude/dev/packet_loop.py kiem-gate --head abababababababababababababababababababab --check-suite 1 --bat-buoc gate --check-runs /tmp/wp788-review-8ixnugpw/inputs/producer_red_own.json
  output     : rc=12
               CẢNH BÁO: 'gate' có 1 run ở suite khác (2) — bỏ qua
                 ĐỎ  'gate' id=1: status='completed' conclusion='failure' head_sha='abababababababababababababababababababab'
               gate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ
  kết luận   : KHÔNG PHẢI LỖI
```

```text
HƯỚNG 5: Thứ tự bản ghi trùng ID
  giả thuyết : nếu chọn bản ghi thuận lợi đầu tiên thì đảo thứ tự conflict thay màu gate
  lệnh       : /usr/bin/python -B /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.claude/dev/packet_loop.py kiem-gate --head abababababababababababababababababababab --check-suite 1 --bat-buoc gate --check-runs /tmp/wp788-review-8ixnugpw/inputs/same_id_conflict_reversed.json
  output     : rc=12
                 ĐỎ  'gate' id=1: status='completed' conclusion='failure' head_sha='abababababababababababababababababababab'
               gate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ
  kết luận   : KHÔNG PHẢI LỖI
```

```text
HƯỚNG 6: Chuẩn hóa chuỗi trạng thái quá rộng
  giả thuyết : nếu completed có whitespace được strip thành completed thì bằng chứng khác whitelist được nhận
  lệnh       : /usr/bin/python -B /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.claude/dev/packet_loop.py kiem-gate --head abababababababababababababababababababab --check-suite 1 --bat-buoc gate --check-runs /tmp/wp788-review-8ixnugpw/inputs/predicate_status_4.json
  output     : rc=12
                 ĐỎ  'gate' id=1: status='completed ' conclusion='success' head_sha='abababababababababababababababababababab'
               gate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ
  kết luận   : KHÔNG PHẢI LỖI
```

```text
HƯỚNG 7: Số Unicode trong đối số neo
  giả thuyết : nếu regex hoặc int chấp nhận chữ số ngoài ASCII thì neo khác dạng yêu cầu vẫn được dùng
  lệnh       : /usr/bin/python -B /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.claude/dev/packet_loop.py kiem-gate --head abababababababababababababababababababab --check-suite '1١' --bat-buoc gate --check-runs /tmp/wp788-review-8ixnugpw/inputs/control_green.json
  output     : rc=2
               --check-suite phải là số nguyên dương thập phân (không dấu, không số 0 đầu), được '1١'
  kết luận   : KHÔNG PHẢI LỖI
```

```text
HƯỚNG 8: Tràn bộ chuyển số nguyên của runtime
  giả thuyết : nếu chuỗi decimal đúng dạng vượt giới hạn int thì CLI thoát ngoài hợp đồng 0/2/12
  lệnh       : PYTHONDONTWRITEBYTECODE=1 python -B /tmp/wp788-review-8ixnugpw/probe_h3.py "$PWD" > .review/probes.out 2>&1  # probe arg_suite_long_decimal; argv thật lưu trong probes.json
  output     : rc=1
               Traceback (most recent call last):
                 File "/tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/s
               …
               v1/.claude/dev/packet_loop.py", line 2573, in main
                   return a.fn(a, Path(a.state_dir))
                          ~~~~^^^^^^^^^^^^^^^^^^^^^^
                 File "/tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.claude/dev/packet_loop.py", line 2323, in cmd_kiem_gate
                   suite = int(a.check_suite) if re.fullmatch(r"[1-9][0-9]*", a.check_suite) else None
                           ~~~^^^^^^^^^^^^^^^
               ValueError: Exceeds the limit (4300 digits) for integer string conversion: value has 4301 digits; use sys.set_int_max_str_digits() to increase the limit
  kết luận   : LỖI
```

```text
HƯỚNG 9: Một ID tự nhận hai identity
  giả thuyết : nếu lọc suite/tên trước kiểm tính nhất quán của ID thì bằng chứng mâu thuẫn được lọc thành xanh
  lệnh       : /usr/bin/python -B /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.claude/dev/packet_loop.py kiem-gate --head abababababababababababababababababababab --check-suite 1 --bat-buoc gate --bat-buoc second --check-runs /tmp/wp788-review-8ixnugpw/inputs/duplicate_id_two_names.json
  output     : rc=0
               gate XANH trên abababababababababababababababababababab (suite 1): gate id=1 · second id=1
  kết luận   : LỖI
```

## Finding F01 — `check-run-id-identity-conflict`

- Severity: **P1**; trục **Standards/Security**; lớp **H3**, slug lớp `bang-chung-dau-vao-tin-qua-muc`.
- Tệp:dòng: `.claude/dev/packet_loop.py:2312` (`_doc_check_runs` chỉ đếm ID), `.claude/dev/packet_loop.py:2340`–2341 (lọc tên/suite trước kiểm duplicate).
- Bằng chứng: `identity-suite-conflict.json`, `identity-name-conflict.json`, `identity-name-suite-pages.json`, `identity-two-required.json`; argv/rc/output đầy đủ ở phần checkpoint phía trên. `total_count=1`, hai bản ghi cùng ID=1 nhưng suite 1 và 9 (bản suite 9 `failure`) ⇒ **rc=0, gate XANH**, chỉ có cảnh báo. Cùng một ID mang hai tên bắt buộc ⇒ **rc=0**, output `gate id=1 · gate2 id=1`. Đối chứng ID trùng nhất quán ⇒ rc=0; conflict cùng tên/suite/head ⇒ rc=12. Bốn test HINT mới đều chết `đòi rc=12, được rc=0`, không phải traceback/setup.
- Tác động: file ghép từ snapshots không nhất quán hoặc chứa identity mâu thuẫn được coi là đủ evidence, chỉ nhờ một phép đếm ID đúng. Một ID không chứng minh hai check độc lập; cùng ID không đồng thời thuộc hai suite. Chốt duplicate hiện có chỉ giữ được tính fail-closed khi name/suite chưa thay đổi. Đây là kiểm consistency nội bộ, không đòi xác thực nguồn API, app hay suite thuộc workflow nào.
- Nguồn/lịch sử: finding mới lượt 1 trên `e995730464da03223cf636e49ad32e220c6ec720`; nối lớp H3 kế thừa của wp770, **3→4**, bắt buộc checkpoint. Một lớp, bốn biểu hiện; không tách bốn finding để đổi bộ đếm.
- HINT — vá ở đâu: `_doc_check_runs`, trước trả danh sách và trước mọi lọc name/suite; đây là chỗ có toàn bộ bản ghi của mọi trang. Vá ở vòng từng tên sẽ lặp lại đúng lỗ lọc mất evidence.
- HINT — vá thế nào: dựng ràng buộc identity chung theo `id`; khi cùng ID có `name`, `check_suite.id` hoặc `head_sha` không nhất quán, từ chối **KHÔNG ĐO ĐƯỢC + 12**, không tự chọn một bản. Giữ luật hiện hành cho duplicate nhất quán và conflict `status`/`conclusion` (không vô tình làm rerun hợp lệ đỏ). Hướng rẻ nhất là một kiểm chung trước lọc; không cần mạng hay mở write set. Không đính code sản phẩm cho sensitive gate, theo protocol §8.
- HINT test — diff gợi ý nằm dưới và tại `/tmp/wp788-review-8ixnugpw/HINT-check-run-id-identity-conflict.patch`; **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Đã chạy test bản sao trên sản phẩm HEAD: 4 đỏ / 1 xanh như trên. Sau sửa phải bổ sung mutant bỏ kiểm identity; nó phải làm đúng bốn ca mâu thuẫn xanh (test đỏ), trong khi ca duplicate nhất quán và fixture CI thật vẫn xanh. Chưa áp bản vá sản phẩm, chưa chứng minh mutant hậu sửa.
- Rủi ro bản vá: cấm mọi duplicate sẽ chặn oan trang lặp nhất quán; so toàn bộ metadata/timestamps sẽ bắt nhầm trạng thái có thể đổi; chỉ kiểm sau lọc sẽ bỏ sót cùng lớp. Đo cả object một trang, nhiều trang, hai thứ tự, multi-name và đối chứng duplicate nhất quán.

```diff
--- a/.claude/dev/packet_loop_test.py
+++ b/.claude/dev/packet_loop_test.py
@@ -5441,6 +5441,25 @@
     _KG_CA[f"kg_n5_{_ten}"] = _kg_ca({"total_count": _tc, "check_runs": [_kg_run(1)]}, chua="≥ 0")
 
 
+# HINT check-run-id-identity-conflict — chỉ là test phản chứng, không sửa gate.
+_KG_CA["kg_h3_same_id_other_suite"] = _kg_ca(
+    {"total_count": 1, "check_runs": [_kg_run(1), _kg_run(1, suite=9, conclusion="failure")]},
+    dem=False, chua="KHÔNG ĐO ĐƯỢC")
+_KG_CA["kg_h3_same_id_other_name"] = _kg_ca(
+    {"total_count": 1, "check_runs": [_kg_run(1), _kg_run(1, name="khac", conclusion="failure")]},
+    dem=False, chua="KHÔNG ĐO ĐƯỢC")
+_KG_CA["kg_h3_same_id_two_required"] = _kg_ca(
+    {"total_count": 1, "check_runs": [_kg_run(1), _kg_run(1, name="gate2")]},
+    bat_buoc=("gate", "gate2"), dem=False, chua="KHÔNG ĐO ĐƯỢC")
+_KG_CA["kg_h3_same_id_conflict_pages"] = _kg_ca(
+    [{"total_count": 1, "check_runs": [_kg_run(1)]},
+     {"total_count": 1, "check_runs": [_kg_run(1, suite=9, conclusion="failure")]}],
+    dem=False, chua="KHÔNG ĐO ĐƯỢC")
+_KG_CA["kg_h3_same_id_consistent_pages"] = _kg_ca(
+    [{"total_count": 1, "check_runs": [_kg_run(1)]},
+     {"total_count": 1, "check_runs": [_kg_run(1)]}], dem=False, expect=0)
+
+
 def case_kg_n4_canh_bao(c: Ctx):
     """N4: đúng MỘT dòng mỗi tên bắt buộc có run ở suite khác; 0 dòng cho tên không bắt buộc;
     mã thoát do luật xanh quyết, cảnh báo không đổi nó. Kiểm NGAY sau từng lệnh."""
```

## Finding F02 — `check-suite-decimal-conversion-limit`

- Severity: **P3**; trục **Spec**; lớp khác: `cli-decimal-conversion-unhandled` (không phải H3: không cấp xanh).
- Tệp:dòng: `.claude/dev/packet_loop.py:2323`, `cmd_kiem_gate`.
- Bằng chứng: HƯỚNG 8; Python 3.13.16 giới hạn mặc định 4300 chữ số, `--check-suite` gồm 4301 ký tự `1` khớp dạng N1 nhưng `int()` ném `ValueError`; rc thật **1**, stderr chứa **Traceback**. Với fixture suite 1, giá trị neo khác đúng dạng phải kết luận không có run trong suite ấy bằng rc=12, hoặc một lỗi đối số có giới hạn được quy định rõ, thay vì crash. Không có giới hạn chiều dài trong spec và help hiện tại.
- HINT — vá ở đâu/thế nào: đường chuyển đổi CLI trước đọc evidence. Có thể giữ suite ở dạng decimal canonical và so với biểu diễn canonical của ID đã validate, hoặc có xử lý giới hạn chuyển đổi rõ ràng; đừng tắt giới hạn int toàn tiến trình. Nếu chọn thêm trần ID thì cần chốt lại giới hạn trong spec/help, không tự coi chuỗi đúng regex là sai dạng.
- Test khóa: thêm `_kg_ca(_KG_1, suite="1" * 4301, chua="VẮNG")`, kỳ vọng rc=12 và không traceback; suite 1 vẫn xanh, abc/012/Unicode vẫn rc=2. Mutant khôi phục đường int không bảo vệ phải làm ca này đỏ trên runtime có limit.
- Nguy cơ sửa: so chuỗi mà cho phép leading zero/Unicode làm đổi nghĩa neo; catch ValueError quá rộng có thể che lỗi đọc evidence. Phải giữ validate dạng ASCII trước so. Owner/hướng xử lý đề nghị: executor wp788, sau checkpoint của owner; đây là đề xuất xử lý, chưa là quyết định hay quyền rework.

## Bảng lớp của lượt này

| Slug lớp | Finding / biểu hiện | Hạng cao nhất | Nguồn | Đóng lớp / giới hạn |
|---|---|---|---|---|
| `bang-chung-dau-vao-tin-qua-muc` (H3) | F01: cùng ID khác suite; khác tên; nhiều tên bắt buộc; mâu thuẫn xuyên trang | P1 | kế thừa 3 finding + lượt 1, exact SHA hiện hành | kiểm identity trước mọi lọc + test âm/dương + mutant; chưa vá; H3=4 ⇒ checkpoint |
| `cli-decimal-conversion-unhandled` | F02: decimal vượt int limit | P3 | lượt 1, exact SHA hiện hành | xử lý số dài có kiểm soát + ca không traceback; chưa vá |

Đếm riêng: **2 lớp có finding trong lượt (1 lớp kế thừa tái diễn + 1 lớp mới); 2 finding; 5 biểu hiện** (4 của F01, 1 của F02). H3 là lớp kế thừa tái diễn, không phải lớp nguyên nhân mới. Không có lượt review liền trước của chính packet wp788 để tính tỷ lệ F/U: **N/A**. Không tính suite xanh là đóng hai lớp này.

HINT test F02 (test thuần, chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit):

```diff
--- a/.claude/dev/packet_loop_test.py
+++ b/.claude/dev/packet_loop_test.py
@@ -5441,6 +5441,9 @@
     _KG_CA[f"kg_n5_{_ten}"] = _kg_ca({"total_count": _tc, "check_runs": [_kg_run(1)]}, chua="≥ 0")
 
 
+_KG_CA["kg_n1_suite_decimal_long"] = _kg_ca(_KG_1, suite="1" * 4301, chua="VẮNG")
+
+
 def case_kg_n4_canh_bao(c: Ctx):
     """N4: đúng MỘT dòng mỗi tên bắt buộc có run ở suite khác; 0 dòng cho tên không bắt buộc;
     mã thoát do luật xanh quyết, cảnh báo không đổi nó. Kiểm NGAY sau từng lệnh."""
```

Đã chạy phản chứng ngoài kho trên sản phẩm không sửa: test đỏ `đòi rc=12, được rc=1`, stderr chứa ValueError/Traceback đúng lỗi chuyển đổi đang báo; KHÔNG đưa tín dụng này vào bảng mutation “giết đúng chốt”. F01 mới là lỗi cấp xanh, F02 là lỗi mã thoát/robustness.

Kiểm whitespace: `git diff --check d8b15cb0730c85e7019aee627c3bfa645a6d3eaf HEAD` rc=0, stdout/stderr rỗng. Đây là kiểm read-only, không thay bằng chứng test.

Full suite đã ra dòng dương `nền: 387/387 đạt · BỎ QUA: 1`; ca bị skip là `luong_canonical_chay_that: chỉ đo lệnh pwsh trên Windows`. **Chưa có TỔNG/rc cuối ⇒ chưa khai full suite passed**. Windows thực là `not_run/skipped`, không được đọc `387/387` thành 388 ca hay Windows parity.

## Đối chiếu từng ô “Phép đo làm ĐỎ”

Các ô ghi rõ đột biến trong spec đều có đột biến cụ thể, đã chạy cả bảng trong một lượt và kiểm đúng assertion. Các tiêu chí metadata/gate trực tiếp giữ command/oracle riêng; không đổi chúng thành lời khai “đã mutation test” khi chỉ có phép đo Git hoặc lint.

| Ô của spec | Đột biến / phép phản chứng cụ thể | Ca đích và kết quả thực |
|---|---|---|
| N1 bỏ kiểm dạng | `kg_n1_bo_kiem_dang` | `kg_n1_check_suite_abc`: đòi 2, được 12; 6 ca sai dạng khác cũng đổi mã; không traceback |
| N2 chỉ kiểm run bắt buộc | `kg_n2_chi_kiem_bat_buoc` | `kg_n2_run_khong_bat_buoc_thieu_suite`: đòi 12, được 0 |
| N3-producer bỏ lọc suite | `kg_n3_bo_loc_suite` | `kg_n3_producer`: đòi 12, được 0; warning vẫn còn nên không phải warning bắt hộ |
| N3-vang bỏ lọc suite | `kg_n3_bo_loc_suite` | `kg_n3_vang`: đòi 12, được 0 |
| N3-chay-lai lọc suite của run nhỏ nhất | `kg_n3_suite_cua_run_dau` | `kg_n3_chay_lai_suite_khac_cu_hon`: đòi 0, được 12, conclusion failure; đúng luật producer |
| N4 bỏ warning | `kg_n4_bo_canh_bao` | `kg_n4_canh_bao`: `đòi đúng MỘT dòng cảnh báo cho 'gate': []` |
| N4 warning cả tên không bắt buộc | `kg_n4_canh_bao_moi_ten` | `kg_n4_canh_bao`: `tên không bắt buộc không được cảnh báo`, đúng tên `khac` |
| N5 quay về `<` | `kg_n5_quay_ve_nho_hon` | `kg_n5_khai_1_co_2`, `kg_n5_khong_voi_mot_run`: đòi 12, được 0 |
| N5 bỏ đòi có mặt | `kg_n5_bo_doi_co_mat` | `kg_n5_thieu`: đòi 12, được 0 |
| N5 bỏ so giữa trang | `kg_n5_bo_so_giua_trang` | `kg_n5_lech_trang`: đòi 12, được 0; số ID bằng total trang đầu nên không bị đếm trang bắt hộ |
| N6 xóa help | `kg_n6_xoa_help` | `kg_n6_help`: thiếu `--check-suite`; rc help vẫn 0, đúng assertion nội dung |
| N7-that sai mã suite khác | `kg_n3_bo_loc_suite` | `kg_n7_that_suite_thu_hoi`: đòi 12, được 0 trên fixture thật 14 tên |
| chung-1 màu ca làm nền a/b không bằng | `kg_bo_status_rieng` | ca `kg_m3_in_progress_success` đổi 12→0 ⇒ assertion đỏ; full runner cộng đúng failure của nền, đọc cơ chế `main` và gate full thực phía dưới; không tuyên bố đã chạy full suite trên một mutant riêng lần nữa |
| chung-2 giữ ca cũ | catalog base/head + `removed_kg=[]`; `kg_bo_status_rieng` là chứng cứ đổi màu bị ca cũ bắt | 50/50 tên cũ còn; mọi ca nền candidate xanh, không có ca không-kg đổi nội dung ngoài fixture stdout được đổi hợp lệ |
| kich-thuoc vượt | `git diff --numstat` trực tiếp trên immutable baseline | 2 tệp / 238 dòng thêm, không mutant giả của Git |
| ruff delta>0 | Ruff thật cả base/head | 1 F841 ở cả hai; delta=0, không mutant giả của Ruff |
| doctrine rc đổi | code base/head gọi cả hai scanner trên root tương ứng | 0/0 cho mỗi cổng, output dương; không nhận việc xóa scanner để tạo “mutant” vô can |
| dot-bien ô sống/sai chốt/thiếu | parse và đọc 34 JSON / 82 ô, đối chiếu N1–N6 phía trên | 0 sống / 0 traceback / 0 ô sai chốt trong bảng được cung cấp; H3 mới chưa có mutant hậu sửa, giữ finding mở |
| tu-do sai mã fixture head cuối | chưa được cấp JSON/API của CI cuối | **not_run**; mutant sai suite trên fixture bb8c0c4 không thay JSON head cuối |

## Ma trận từng dòng `nghiem_thu`

`L1` = `PYTHONDONTWRITEBYTECODE=1 python -B .claude/dev/packet_loop_test.py > .review/suite.out 2>&1` (full, kết quả terminal ghi cuối verdict).
`L2` = `PYTHONDONTWRITEBYTECODE=1 python -B -W ignore /tmp/wp788-review-8ixnugpw/targeted.py "$PWD"` (rc=0, 88/88).
`L3` = `bash .review/mut_all.sh "$PWD/.claude/dev" kg_ /tmp/wp788-review-8ixnugpw/mutants` (34 đột biến, 82 thông điệp đích, bảng từng ô phía trên).
`L4` = `PYTHONDONTWRITEBYTECODE=1 python -B /tmp/wp788-review-8ixnugpw/probe_h3.py "$PWD"` (126 probe; argv/output từng probe trong probes.json).

| ID | ĐẠT / KHÔNG ĐẠT | Ca test / lệnh / giới hạn chứng minh |
|---|---|---|
| chung-1 | ĐẠT Linux, 1 skipped | L1 đã terminal: rc=0, `nền: 387/387 đạt · BỎ QUA: 1`, `TỔNG: ĐẠT`; ca pwsh Windows skipped riêng |
| chung-2 | ĐẠT phần quan sát Linux | L1 nền không ca đỏ; L2 88/88; catalog base/head 50→86 kg, removed=[]; 302 ca không-kg giữ nguyên danh sách, chỉ fixture stdout thêm total/suite đúng spec. Không chạy full base lần hai, không tuyên bố Windows parity |
| N1 | ĐẠT bộ ca liệt kê; mục tiêu tổng thể có F02 | L2 `kg_n1_thieu_check_suite`, `kg_n1_check_suite_{abc,am,0,012}` đều đúng 2 + lý do; L3 bỏ kiểm dạng đổi mã. L4 số dài đúng dạng lại rc=1 ⇒ F02 |
| N2 | ĐẠT | L2 `kg_n2_suite_{thieu,null,list,thieu_id,id_bool,id_chuoi}`, `kg_n2_run_khong_bat_buoc_thieu_suite` đều 12 + đúng lý do; L3 required-only/bool mutant xanh ⇒ test đỏ |
| N3-producer | ĐẠT ca cụ thể | L2 `kg_n3_producer`: 12 + failure; L3 bỏ suite đổi 12→0. F01 là thiếu consistency trước lọc, giữ mở riêng |
| N3-vang | ĐẠT | L2 `kg_n3_vang`: 12 VẮNG; L3 bỏ suite đổi 12→0 |
| N3-chay-lai | ĐẠT | L2 `kg_n3_chay_lai`, `kg_n3_chay_lai_suite_khac_cu_hon`: 0; L3 suite-run-đầu làm 0→12 |
| N4 | ĐẠT | L2 `kg_n4_canh_bao` đo đúng một dòng/0 dòng + rc cho cả ca đỏ và xanh; L3 cả hai warning mutant chết đúng assertion |
| N5 | ĐẠT hợp đồng đếm và kiểu | L2 toàn họ `kg_n5_*` cùng ca dương 1/nhiều trang; L3 `<`, thiếu trường, bỏ so trang đều đổi 12→0. Đếm đủ ID không chứng minh ID nhất quán: F01 |
| N6 | ĐẠT | L2 `kg_n6_help`, ca dương có `(suite …)`; L3 `kg_n6_xoa_help`, `kg_n6_dong_xanh_khong_suite` đều đúng assertion |
| N7-that | ĐẠT behavior trên fixture được cấp | L2 `kg_n7_that_suite_ci`:0; `kg_n7_that_suite_thu_hoi`:12 VẮNG; app/check_suite/attempt cancelled giữ trong 32 run, 14 tên. Không xác thực lại provenance API vì cấm mạng |
| kich-thuoc | ĐẠT | `git diff --numstat d8b15cb0730c85e7019aee627c3bfa645a6d3eaf HEAD`: rc=0, 2 tệp / 238 thêm ≤3/≤300 |
| ruff | ĐẠT tiêu chí delta | cùng lệnh `python -B -m ruff check --no-cache --select F …packet_loop.py`: base rc=1/head rc=1; cùng 1 F841 dòng 1804; delta=0 |
| doctrine | ĐẠT | `doctrine-scan --root <root>` và `adr-song --root <root>`: base/head đều rc=0; 10 tệp và 53 ADR khớp |
| dot-bien | ĐẠT các ô luật được chỉ định; không đóng finding mới | L3 34/82, toàn bộ bảng; mọi ô N1–N6 yêu cầu đột biến cụ thể đã có, không tín dụng traceback. Bốn test mới F01 còn đỏ; chưa có bản vá/mutant đóng lớp |
| tu-do | KHÔNG ĐẠT / not_run | không có JSON CI cuối trên SHA e995… được giao, và prompt cấm gọi GitHub/mạng. Không tự thay fixture bb8c0c4 cho head hiện hành |

Merge-1 không đạt (verdict blocked, P1 mở); merge-2 có bảng mục tiêu ở cuối; merge-3/4/4b **not_run/not_measured** trong review offline (không có evidence CI cuối, authorization hay connector completed được cấp). Không suy job completed thành passed, không coi absence là sạch. Không thao tác merge/land/deploy.

Đo tên ca non-kg độc lập bằng import CASES base/head trong hai subprocess `python -B -W ignore`: base_nonkg=302, head_nonkg=302, removed=[], added=[]. Raw tên đầy đủ `/tmp/wp788-review-8ixnugpw/all-case-names.json`; không chỉ so số lượng.

Phản chứng A/B tối thiểu cho F01, scratch tạo bằng `mktemp -d /tmp/wp788-repro.XXXXXX`: chỉ đổi `check_suite.id` của bản ghi failure từ 1→9, giữ cùng id=1, total_count=1, name/head/status/conclusion không đổi.

```text
same-id-same-suite rc=12
  ĐỎ  'gate' id=1: status='completed' conclusion='failure' head_sha='abababababababababababababababababababab'
gate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ
```
```text
same-id-other-suite rc=0
gate XANH trên abababababababababababababababababababab (suite 1): gate id=1
CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua
```

Tái lập độc lập từ root của exact reviewed_sha (chỉ ghi JSON ngoài kho):

```bash
scratch_wp788=$(mktemp -d /tmp/wp788-repro.XXXXXX)
python -B - "$scratch_wp788" <<'PROBE'
from pathlib import Path
import json, subprocess, sys
root = Path(sys.argv[1]); head = "ab" * 20
r = dict(id=1, name="gate", head_sha=head, status="completed",
         conclusion="success", check_suite={"id": 1})
for suite in (1, 9):
    d = dict(total_count=1, check_runs=[r, dict(r, conclusion="failure", check_suite={"id": suite})])
    p = root / (str(suite) + ".json"); p.write_text(json.dumps(d))
    q = subprocess.run(["python", "-B", ".claude/dev/packet_loop.py", "kiem-gate",
                        "--head", head, "--check-suite", "1", "--bat-buoc", "gate",
                        "--check-runs", str(p)], capture_output=True, text=True)
    print("other_record_suite=", suite, "rc=", q.returncode)
    print(q.stdout + q.stderr)
PROBE
```

Kết quả đã đo tương đương block trên: suite 1 ⇒ rc=12/failure; đổi đúng trường ấy sang 9 ⇒ rc=0/gate XANH + cảnh báo. Cùng ID chuyển identity không bị phát hiện, nên warning không chữa được thiếu evidence.

## Kết quả terminal của gate đầy đủ

Command đã chạy nền, shell giữ `wait` và thoát bằng đúng mã child:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B .claude/dev/packet_loop_test.py > .review/suite.out 2>&1 &
suite_child=$!
wait "$suite_child"
suite_exit=$?
printf '%s\n' "$suite_exit" > .review/suite.rc
exit "$suite_exit"
```

Exec session `15243` kết thúc **exit_code=0**; `.review/suite.rc` có `0`. Các dòng output thật:

```text
  BỎ QUA  luong_canonical_chay_that: chỉ đo lệnh pwsh trên Windows
nền: 387/387 đạt · BỎ QUA: 1
  ok  78/78 lớp lách đều có ca bắt-oan (33 ca riêng biệt)
  ok  78 lớp lách đều có đột biến giết · 5 đột biến PHỐI HỢP · 0 ngoại lệ
  ca               : 388
  đột biến         : 161
  lớp lách         : 78
  ca bắt-oan       : 35
  ngoại lệ AC 18   : 0
TỔNG: ĐẠT
```

**passed**: full suite trong scope Linux đã chạy; component 88/88; 34 đột biến kg/82 ô được audit; các tiêu chí delta Ruff/doctrine/ADR/kích thước. **failed**: bare lint có F841 nền (delta 0); bốn test phản chứng F01; ca robustness F02. **skipped**: đúng 1 ca pwsh Windows, không tính là pass. **not_run/not_measured**: Windows execution/parity, JSON CI head cuối `tu-do`, connector completed, CI provenance/merge authorization, lease live/refs máy chủ/receipt executor (prompt cấm mạng và chỉ cấp snapshot). Không tạo GitHub state hay assurance approved. Cần đọc đủ những evidence ấy trước mọi merge; chúng không bị thay bằng local green.

## Snapshot và giới hạn bàn giao

Kiểm cuối `2026-10-17T18:14:59.686887+00:00`: `git rev-parse HEAD HEAD^{tree}` rc=0, HEAD/tree giữ nguyên. `git diff --exit-code` và `git diff --cached --exit-code` đều rc=0, output rỗng. Snapshot hash nội dung tracked không nhạy cảm so với đầu review: delta=[]; 2 path có tên nhạy cảm không được đọc lại để làm cleanliness claim. `git status --porcelain=v1 --untracked-files=all --ignored=matching` chỉ có artifact `.review/` được prompt cấp và `.codex/` ignored đã thấy ở snapshot đầu; không có tracked/index delta. Không truy cập kho executor nguồn vì không nằm trong phạm vi được giao. Hai snapshot chỉ chứng minh không có delta quan sát ở hai mốc, không chứng minh toàn lịch sử chưa từng ghi/hoàn nguyên. Sandbox thực là workspace-write, không giả là OS read-only.

| Artifact ổn định | Byte | SHA-256 |
|---|---:|---|
| `.review/suite.out` | 19515 | `14cf76225123cf59a4fcda4c781f280ad00f8051fed2692b5e4e1bfe177193f7` |
| `.review/suite.rc` | 2 | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `.review/mut_all.out` | 16007 | `6f1360188f30563bb2eb47b23e4cfc8789305936a84e1c10408d292ed693eb7b` |
| `.review/targeted.out` | 5076 | `f53fbfb053d3f58deb482f2c8487f09d8abc9f7d130979be133153491d808e68` |
| `.review/probes.out` | 81199 | `6df3191193e17815c636bc7d4ac8a7c8ce72290a18967d552fc481be36a44755` |
| `.review/hint_checks.out` | 601 | `b0b1fd24a4e7f4e2fb383682c983b387d378080fe2a42309b029b9310595b3fc` |
| `.review/SPEC.md` | 15330 | `82dc170446c3a4431739a3effbec8cb55adadc13d69f5c510f8782a2b45eb54e` |

Bản HINT chỉ là test diff được đính trong verdict và ở scratch; không áp lên checkout. Finding F01 cần quyết định owner tại Review Rescue Checkpoint vì **H3=4**; không tự cấp rework/lease, không đổi spec, không gọi thêm Codex, không approve/merge/land/deploy. Công việc được giao ở lượt này hoàn tất ở artifact verdict cục bộ; đăng/readback/state transition thuộc người điều phối theo chỉ thị cấm GitHub của prompt.

reviewed_sha: e995730464da03223cf636e49ad32e220c6ec720
reviewed_tree: a0729f20a384f197a2b3a9590d4348714e455dee
verdict: blocked
counts: P0=0, P1=1, P2=0, P3=1
provider: openai_codex
model_family: openai
model: gpt-6.1-sol (CLI header)
effort: xhigh (CLI header)
execution_surface: codex_cli
transport: machine
assurance: không có approval; chưa chuyển state/receipt

| Mục tiêu | ĐẠT / KHÔNG ĐẠT | Phép đo / phần còn mở |
|---|---|---|
| N1 | KHÔNG ĐẠT đầy đủ | thiếu/sai dạng đều đúng RC_ARG trong 8 ca; L4 decimal 4301 chữ số khớp dạng gây rc=1 + traceback, F02 P3; HINT test đính kèm |
| N2 | ĐẠT schema tường minh | L2: object/id int không bool ở MỌI phần tử; mutant required-only/bool chết đúng chốt. Thiếu consistency ID được báo riêng F01 |
| N3 | ĐẠT luật trên tập đã lọc; chưa đủ cấp approval | L2 rerun/latest/ties/head/suite/missing đều đúng, L3 mutant đổi màu. F01 Standards/Security: lọc mất record cùng ID khác identity còn cấp xanh |
| N4 | ĐẠT | L2 cảnh báo chính xác cả đỏ/xanh/không bắt buộc; hai mutant warning chết đúng assertion |
| N5 | ĐẠT đòi kiểu/đủ số ID | L2/L3 thiếu/thừa/bool/âm/lệch trang đều đúng; duplicate nhất quán được phép. Đếm bằng nhau không đóng F01 |
| N6 | ĐẠT | L2 help có --check-suite, GET actions/runs, check_suite_id, filter=all; dòng xanh nêu suite; hai mutant tài liệu/output đỏ |
| N7 | ĐẠT bộ ca được đặc tả | 50 ca kg cũ còn; 86 kg + 2 stdout component xanh; fixture bb8c0c4 đúng/sai suite 0/12; full suite rc=0, 387/387 + 1 skipped. Chưa có test hồi quy F01/F02 trong candidate; HINT đã đo độc lập |
