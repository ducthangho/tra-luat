# Cross-review độc lập — packet #668, lượt 8

Trạng thái lúc mở: dang_review. Các hướng được ghi dần; kết luận hoàn tất ở cuối tệp.
reviewed_sha: 320475292649a9bf985edccf8e9e35f78243c2e4

Mọi đột biến thực hiện trên bản sao trong /tmp; không sửa mã sản phẩm.

HƯỚNG 1: Neo vật liệu và quyền đo
  giả thuyết : Head/SPEC/write set đúng chỉ thị.
  lệnh       : git -C cay-kho rev-parse HEAD HEAD^{tree}; git status --porcelain --ignored; sha256sum SPEC.md; cat numstat.txt
  output     : HEAD=320475292649a9bf985edccf8e9e35f78243c2e4; tree=44037d1bc3f8a4a5aa6bc2abb439f55d612abda9; status rỗng; SPEC=dd2ada1b8511bec1c6c30ffdd7a94a3c34f4024836761878caf73ce339516b15; 5 tệp +1419/-31.
  kết luận   : KHÔNG PHẢI LỖI. Trần ~1.600 và lượt review tiếp lấy từ chỉ thị chủ kho. Cây đo /tmp/review668-r8, baseline /tmp/review668-r8-base; git fixture ghim core.abbrev=7, commit.gpgsign=false; bytecode tắt. Harness lượt 7 được chép và chỉ đổi đường cây; chưa chép kết quả cũ.

Reviewer: OpenAI Codex, họ GPT-6 theo cấu hình phiên; công cụ terminal qua dịch vụ/API (`codex_service`, machine/local), không tự khai CLI hay exact model ID/effort đã đo được. Verdict này không cấp human_audited/quyền land.

HƯỚNG 2: Workflow F1/F3/F10/F14 và đột biến hàng rào
  giả thuyết : Bản vá lượt 8 không mở lại lớp thực thi workflow.
  lệnh       : python evidence/env.py python -u evidence/workflow.py; python evidence/env.py python -u evidence/workflow_ablation_extra.py
  output     : Control: F1=20/20, F3=28/28, F10=7/7, F14=5/5 chặn đúng. Bỏ F10: 7/7 F10 lọt. Chỉ splitlines: 0 F3 lọt; splitlines + bỏ F10: 27/28 F3 lọt. Bỏ F14: 5/5 F14 lọt. Bỏ thực thi+Bash: 18/20 F1, 7/7 F10, 5/5 F14 lọt.
  kết luận   : KHÔNG PHẢI LỖI trong phạm vi đo. Hai ca F1 cấp workflow vẫn được chốt riêng giữ. Chỉ chạy payload đã có trong phan_chung; không soạn payload ký tự ẩn/điều khiển mới.

HƯỚNG 3: Các cổng lân cận
  giả thuyết : t152, lease, actionlint, probe và Ruff không hồi quy.
  lệnh       : python evidence/env.py python -u evidence/regression.py
  output     : Head/base: t152 rc=0; lease t24/t31/t35/t161/t162 rc=0; actionlint rc=0; probe rc=0. Ruff F --no-cache: cùng 6 F841, delta=0, rc=1 cả hai.
  kết luận   : KHÔNG PHẢI LỖI. Ruff còn nợ nền, không gọi là xanh tuyệt đối. Log chi tiết trong evidence/head-*.log và base-*.log.

HƯỚNG 4: Miền cấu hình và gom bộ sai trên head nguyên bản
  giả thuyết : Phải phân biệt lỗ test đột biến với đường xanh sai của mã chưa đột biến.
  lệnh       : python evidence/env.py python evidence/mode_domain.py; gom_current_data.py; partition_roundtrip.py
  output     : Lưới 10.816 k/N: nhận 135, từ chối 10.681, 0 mismatch; thêm 11 dạng ASCII sai bị chặn. Bộ đủ 320 bản ghi gom lỗi=0. Các bộ đích sống/bỏ qua/tín dụng giả/bán kính 2/lỗi đo đều lỗi=1; đủ 320 hàng. Sai tên ca/đích bị G-ban-ghi. Mọi N=2..16: phân hoạch phủ 320, rời nhau; đảo thứ tự tệp và BKCON vẫn gom lỗi=0, bảng đúng thứ tự DOT_BIEN.
  kết luận   : KHÔNG PHẢI LỖI trên đầu vào đã đo. Đây là dữ liệu fixture, không thay A1 chạy tám mảnh thật.

Bổ sung HƯỚNG 3: registry head 1025/1025, baseline 938/938; TỔNG ĐẠT cả hai (evidence/registry-head.log, registry-base.log). Không chạy toàn bộ suites --chay của registry.

HƯỚNG 5: Gate M1 trọn vẹn
  giả thuyết : Hồi quy F22 không được che bằng chỉ chạy ba ca mới.
  lệnh       : python evidence/env.py bash -c 'cd /tmp/review668-r8 && CONG_CU_TEST_BAN_KINH=manh python -u ops/cong_cu_test.py'
  output     : rc=0; cong_cu_test: 56/56 đạt; tổng=56, bỏ qua=0, tiền kiểm bỏ qua=0. Cổng cây thật ĐẠT; tự kiểm phân hạng/giàn giáo/song song N126 ĐẠT; giao 320 đột biến; lỗi đột biến=0.
  kết luận   : KHÔNG PHẢI LỖI ở gate M1. F22 thuộc vòng bán kính riêng, đang đo đủ 320; không lấy gate này thay vòng ấy.

HƯỚNG 6: MỚI — kiểu từng trường header và loại tệp
  giả thuyết : Một fixture bool cho trường manh không chứng minh chốt kiểu của phien_ban/so_manh; thư mục giả không chứng minh chốt symlink.
  lệnh       : python evidence/env.py python -u evidence/new_mutations.py; python evidence/env.py python -u evidence/schema_io.py
  output     : header_type_phien_ban, header_type_so_manh, header_accept_symlink: mỗi phép 56/56 qua; header_type_manh bị t52 giết. Trên bộ đủ 320 bản ghi: phien_ban=True hoặc 1.0, control lỗi=1 G-dau; bỏ riêng kiểm kiểu phien_ban ⇒ lỗi=0, GOM MẢNH 3/3. Tệp 0.txt là symlink tới tệp thường hợp lệ: control lỗi=1 G-tep; bỏ riêng is_symlink ⇒ lỗi=0. Bỏ kiểm kiểu so_manh chưa thấy xanh sai: ví dụ 3.0 ném TypeError.
  kết luận   : LỖI (P2), F24 — chốt cấu trúc gom thiếu răng. Head nguyên bản fail-closed; không báo P1 từ kết quả của mutant. Hai survivor có hậu quả quan sát được (kiểu phiên bản và symlink) cùng lớp schema/loại tệp, không nhân thành hai finding. so_manh sống nhưng vẫn fail-closed trong các mẫu, ghi riêng giới hạn.

HƯỚNG 7: Đo lại I/O và tệp đầu ra cũ (đã có hướng này ở lượt 3/6)
  giả thuyết : Dọn mảnh hỏng hoặc ghi thất bại có thể để lại dữ liệu cũ được gom nhầm.
  lệnh       : python evidence/env.py python -u evidence/schema_io.py
  output     : Header cụt ⇒ lỗi=1 G-dau. Writer nhận ket=None với output là symlink: lỗi=1, symlink bị xoá, đích giữ nguyên KEEP. Output là thư mục ⇒ IsADirectoryError, thư mục còn nguyên; không trả xanh. Tiêm OSError tại Path.write_bytes sau tệp STALE: OSError, tệp cũ không còn.
  kết luận   : KHÔNG PHẢI LỖI xanh sai trên head trong các phép đo này. Một số I/O lỗi đi bằng exception, chưa có chẩn đoán gắn thẻ; đó không phải bằng chứng fail-open. Không mô phỏng runner upload/download thật.

HƯỚNG 8: Main — nhiều ca bỏ qua và bảo toàn chẩn đoán
  giả thuyết : Kỳ vọng stdout nguyên văn vẫn thiếu răng nếu giàn giáo chỉ kích một ca bỏ qua và nén lý do receiver thành rc.
  lệnh       : python evidence/env.py python -u evidence/main_skip.py; main_skip_wiring.py; main_reason.py; new_mutations.py (main_no_error_tail đã sửa cú pháp rồi chạy riêng lại).
  output     : skip_first_diagnostic và skip_boolean_count đều 56/56 qua. Wiring hai ca bỏ qua: control rc=0, hai dòng BỎ QUA và 54/54 đạt, bỏ qua=2; mutant cắt danh sách chỉ in một dòng; mutant ép số đếm bool in 54/55 đạt, bỏ qua=1. main_no_error_tail cũng 56/56 qua. Wiring reason_message_lost với receiver/writer thật: control rc=1, nêu danh sách kết quả thiếu; mutant rc=1 nhưng chỉ còn (rc=0).
  kết luận   : LỖI (P2), F23 nối nguyên lớp F2/F5/F6/F7/F12/F15/F18. Phần lớn miền F18 đã được mở rộng nhưng vẫn chưa bảo toàn mọi số đếm/chẩn đoán mà main quyết định. Không báo P1: các mutant này chưa cho bộ đo sai thành xanh; hệ quả là mất danh tính ca bỏ qua, báo cáo số đo sai và mất nguyên nhân lỗi con.

Ghi chú harness: bản đầu main_no_error_tail dùng dấu nháy lồng không hợp lệ với Python 3.11, tạo SyntaxError/tin_dung_gia; giữ tại evidence/invalid-syntax-main_no_error_tail.json, loại khỏi số đếm kết quả. Đã sửa cặp neo/thay, chạy lại đủ 56 ca (evidence/new-main_no_error_tail.json). main_skip.py lúc dựng có assert nhầm số lần neo vì tính cả chú thích; sửa trước khi chạy phép đo. Không tính các lỗi harness này thành răng hay lỗi sản phẩm.

BẢNG KIỂM MAIN — liệt kê theo thân main() ở head, không lấy DOT_BIEN làm trần

| Quyết định / dữ liệu main sở hữu | Đột biến độc lập đối chiếu | Quan sát / giới hạn |
|---|---|---|
| Truyền os.environ, đọc chế độ trước CA, ValueError in lý do và rc=2 | config_ignore, main_environment_empty | Nhật ký rỗng trước lỗi; stdout và rc |
| Hai tiền kiểm đúng danh tính/thứ tự, giữ mọi kết quả khác None | batch_skip, alias_skip, precheck_first | Cả batch, alias, cả hai cùng bỏ qua |
| Chạy đủ CA theo thứ tự, đúng một lần | ca_skip, ca_duplicate_middle, ca_reverse | Tên từng CA trong nhật ký |
| Phân biệt BoQuaMoiTruong/AssertionError/Exception; lưu tên và lý do, tăng qua | assert_ignore, exception_ignore, skip_as_red, pass_counter, skip_counter | Đạt, bỏ qua, đỏ assertion và lỗi runtime |
| In mọi chẩn đoán tiền kiểm, CA bỏ qua, CA đỏ | precheck_print_drop, skip_print_drop, failure_print_drop, skip_first_diagnostic | Hai tiền kiểm/hai CA đỏ có thử; hai CA bỏ qua thiếu ⇒ F23 |
| Tổng qua, mẫu số bỏ qua, tổng CA, số bỏ qua/tiền kiểm | skip_boolean_count, pass_counter, summary_ca_zero | Hai CA bỏ qua bị nén thành một mà chưa bị bắt ⇒ F23 |
| Chọn mảnh hay nhánh đủ/gate | shard_never, gate_run_full | Cả ba mode và đường cấu hình sai |
| Mảnh lấy k/N/ra, truyền đúng phân hoạch | shard_k/n/ra, partition, shard_n_fixed_eight, partition_fixed_eight | Hiện thử 3/8, 5/16, 1/2 |
| Nền đỏ/tiền kiểm bỏ qua: không phóng con, gọi dọn đúng đường, trả lỗi | base_red_ignore, precheck_ignore, no_cleanup, cleanup_fp/names_lost/reason_lost, main_cleanup_path, bad_base_rc | Dữ liệu ket=None và lý do; một số tham số dọn không ảnh hưởng hàm thật khi ket=None |
| Thông báo số mảnh/tổng tên/số worker | T54 so toàn dòng mảnh; các phép shard/partition/workers ở trên | Kích thước và tham số đổi làm kỳ vọng lệch |
| Phóng con đúng tên/nền rỗng/worker, tiêu thụ mọi nhóm | launch_names/baseline/workers, launch_skip_last_group | Hai nhóm; trường hợp ten rỗng không tới được với 320 mutant và N≤16 |
| Receiver nhận đúng nhom/rc/stdout/nền rỗng | receiver_group/rc/output/baseline/ca_baseline/skip_call | Có rc≠0 với stdout đủ, rc=0 stdout thiếu |
| Nhận lỗi đầu tiên, giữ lý do/rc/đuôi stdout; không mất nhóm/giá trị | no_reason, reason_last, reason_message_lost, main_no_error_tail/rc, main_initial_error_ignored, break_on_error, drop_group, drop_values | Lý do nguyên/đuôi stdout còn bị nén mất ⇒ F23 |
| Writer nhận k/N/ra/tên/ket hoặc None/lý do/vân tay | writer_k/n/ra/names/ket/reason/fp, writer_skip | Băm toàn ket quan sát giá trị và tập |
| In mọi dòng writer, chuyển lỗi 0/1/>1 sang rc | print_writer_drop, writer_line_first, writer_rc/eq_one/gt_one/negative_error | Hai dòng và ba miền số lỗi |
| Cổng cây thật đúng GOC, giữ rc và mọi dòng | gate_skip/root/print_drop, final_gate, summary_gate_pass | Cổng thật trả 0/1; không dựng miền 2 để gọi mutant tương đương là lỗi |
| Tự kiểm phân hạng/giàn giáo, báo cáo nền, song song đúng thứ tự và cộng lỗi | classifier_skip, scaffold_skip/reset/max, parallel_skip/arg/reset/max, baseline_errors/reset/max | Kịch bản đồng thời cho tổng loi_db=5 |
| Tập mọi tên nền đỏ; báo cáo đúng tập và mọi dòng; truyền tới tự kiểm/bán kính | baseline_empty/report_arg/first/print_drop, main_no_sorted_baseline, full_base | Helper thật tự sắp xếp/tập hoá, nên bỏ sort tại main không đổi kết quả quan sát |
| Gate thông báo giao đo; đủ gọi vòng bán kính đúng mọi tên/nền/worker | gate_run_full, gate_notice_drop, full_names/base/workers | So đủ nhật ký và thông báo |
| Nhánh đủ tiêu thụ mọi kết quả, mọi dòng, cộng mọi lỗi | full_errors/reset/first_only/repeat_result/max, print_full_drop, full_line_first | Hai kết quả; lỗi đầu/cuối/cả hai; mỗi kết quả hai dòng |
| Tổng hợp mode/số CA/số mutant/lỗi/tiền kiểm/cổng | summary_errors_zero, summary_gate_pass, summary_ca_zero, main_gate_summary_mode | Nguyên các dòng có nghĩa; giàn giáo cố ý bỏ dòng trống |
| Rc cuối từ hong, loi_db, tien_kiem_bo_qua, loi_cong | final_hong/db/precheck/gate, final_db_eq_one/gt_one | hong có loi_nen bảo vệ; không gán survivor tương đương thành finding |

Các cặp neo/thay và kết quả từng ca lưu riêng trong evidence/*mutations.json và JSON từng phép. Bảng này là checklist hữu hạn theo mọi đơn vị quyết định/truyền dữ liệu trong main; không phải chứng minh toán học mọi chương trình đột biến có thể có.

HƯỚNG 9: Hồi quy F22 — đủ cả năm cây mutant thiếu cong_cu.py
  giả thuyết : Giàn giáo t52 đã trở lại đúng hợp đồng phụ thuộc của mọi mutant cũ.
  lệnh       : radii.py all (năm tên dưới); python evidence/env.py python -u evidence/old_transport.py
  output     : t31_tien_kiem_nuot_moi_loi, t32_bo_nhan_dong_ho_nhay, t32_noi_ra_moi_timeout, bn_ban_kinh_giau_ly_do, bn_ban_kinh_gia_ve_som: đủ 56 trạng thái/tên, lỗi bán kính=0, đúng ca đích. t52/t53/t54: 15/15 qua. Cả năm chạy thêm qua _ban_kinh_moi_dot_bien → hai tiến trình --ban-kinh-con THẬT → receiver/kết luận: TOTAL_ERRORS 0.
  kết luận   : KHÔNG PHẢI LỖI; F22 ĐÃ VÁ THẬT. Đây là phép đo độc lập trực tiếp và đường con thật, không dùng lời executor. Vòng 320 vẫn đang chạy để kiểm hồi quy ngoài năm tên đã biết.

HƯỚNG 10: Chốt checklist main lượt 5
  giả thuyết : Không chỉ chạy những mutant executor chọn bổ sung.
  lệnh       : python evidence/env.py python -u evidence/checklists.py (module main_matrix)
  output     : 68/68 phép chạy đủ 56 CA; 65 bị t54 giết, ba sống 56/56: receiver_baseline, break_on_error, final_hong. Cặp neo/thay khớp nguyên JSON lượt 7 và checklist kế thừa lượt 5.
  kết luận   : KHÔNG PHẢI LỖI mới ở ba survivor này. receiver_baseline thêm tên không có trong CA nên tập thực không đổi; break_on_error dừng đọc sau lỗi đầu nhưng _phong_con đã phóng/đợi hết con, writer vẫn nhận None và rc đỏ; final_hong được loi_nen bảo vệ. Các survivor có hậu quả thuộc F23 được ghi riêng.

Bổ sung HƯỚNG 6/F24 — CLI thật: `python evidence/env.py python -u evidence/schema_cli.py` dựng kho git tối thiểu, lấy đúng HEAD/băm nguồn từng bản rồi gọi `python ops/cong_cu_test.py --gop`. Header phien_ban=true: control rc=1 G-dau → mutant bỏ kiểu rc=0, SỐ LIỆU 320/lỗi=0. Tệp symlink: control rc=1 G-tep → mutant bỏ is_symlink rc=0, 320/lỗi=0. Log evidence/schema-cli.log. Không đổi nhãn thành P1 của head: đây vẫn là hậu quả của các đột biến sống 56/56.

HƯỚNG 11: Checklist main lượt 6 — nhiều dòng và miền lỗi
  giả thuyết : Những phép cắt đầu ra sống ở lượt 7 nay phải chết.
  lệnh       : checklists.py (main_new, 19 phép)
  output     : 19/19 đủ 56 CA; 18 bị t54 giết, một sống final_gate_eq_one. full_line_first, writer_line_first, gate_print_drop, baseline_print_drop đều đã bị bắt. Các phép lỗi ==1, cắt tiền kiểm, đổi lý do đầu thành lý do cuối và sửa SỐ LIỆU cũng bị bắt.
  kết luận   : KHÔNG PHẢI LỖI ở final_gate_eq_one vì cổng thật trả 0/1. Bốn lỗ đầu ra nhiều dòng của F18 ĐÃ VÁ THẬT; điểm thiếu còn lại thuộc F23, không phủ nhận các răng đã hoạt động.

HƯỚNG 12: Hoàn tất TOÀN BỘ checklist main lượt 5–7
  giả thuyết : Vá F18 phải giết lại mọi survivor có hậu quả đã được chỉ ra ở lượt 7.
  lệnh       : checklists.py (main_matrix 68 + main_new 19 + main_extra 12); summarize_r8.py
  output     : 99/99 phép đủ 56 CA; 94 bị đúng t54 giết, 5 sống: receiver_baseline, break_on_error, final_hong, final_gate_eq_one, reason_message_lost. Tổng 5.450 qua + 94 giet_that, không bo_qua/tin_dung_gia. 12 phép lượt 7: 11 bị bắt, riêng reason_message_lost sống.
  kết luận   : LỖI (P2) còn lại thuộc F23. Bốn survivor kia có giải thích tương đương/được lớp khác bảo vệ đã ghi ở HƯỚNG 10/11; không báo thêm lỗi giả. F18 đóng thật các phép một lỗi, N=8 cố định, max thay cộng, cắt bảng, số CA; chưa đóng lý do nguyên. Ma trận chi tiết: evidence/mutation-matrix.md; cặp neo/thay: evidence/main*-mutations.json.

HƯỚNG 13: Gom/CLI/bộ ghi — toàn bộ checklist lượt 6–7
  giả thuyết : Các bộ quan sát nguyên bảng phải đóng F16/F17/F19/F20/F21 mà không thay phép quyết định chung.
  lệnh       : checklists.py: gom_semantics (4), cli_new (4), gom_extra (4), writer_extra (3); new_mutations.py: writer_reverse_table
  output     : 15/15 phép kế thừa đủ 56 CA, đều bị ĐÚNG t52 giết: 825 qua + 15 giet_that, không bo_qua/tin_dung_gia. Bỏ kết luận/cộng lỗi, gán đè lỗi, chỉ bản ghi đầu, xoá/đảo/lặp/cắt bảng, ==1 tại CLI, chuẩn hoá mã dispatcher, cắt stdout, writer chỉ tính lỗi transport đều chết. Phép mới đảo bảng writer cũng bị t52 giết.
  kết luận   : KHÔNG PHẢI LỖI còn mở ở các biểu hiện F16/F17/F19/F20/F21 đã đo. Các biểu hiện phán quyết/bảng gom, CLI và bộ ghi đã đóng trong checklist này; trạng thái cả lớp CLI được kiểm tiếp ở HƯỚNG 15 (F25). F24 là chốt cấu trúc đầu vào riêng, không đổi tên lớp cũ để che survivor.

Tổng checklist kế thừa: 114/114 đủ 56 trạng thái/phép; 109 bị giết, năm survivor của main đã phân loại. Các phép mới thêm: 13 new_mutations + hai main_skip, cũng đủ 56/phép. Các survivor mới ngoài F23/F24: main_no_sorted_baseline (helper thật tự sort/tập hoá), writer_drop_missing (writer vẫn ném KeyError khi ghi, không tạo bộ xanh), header_type_so_manh (mẫu sai kiểu còn đỏ/exception) chưa có bằng chứng xanh sai, không gán P1. Không tính JSON lỗi cú pháp harness vào các tổng này.

HƯỚNG 14: Toàn bộ mutant nền — không chỉ mẫu F22
  giả thuyết : Các giàn giáo mới không giết thêm t52/t53/t54 dưới những mutant cũ khác.
  lệnh       : inventory.py; radii.py all; đối chiếu radius JSON theo tập tên từ base-inventory.json
  output     : Baseline 212 mutant/53 CA; head 320 mutant/56 CA, không mất tên cũ, thêm 108 tên. Đã hoàn tất 212/212 mutant cũ: lỗi bán kính=0, đúng ca đích; t52/t53/t54 636/636 qua.
  kết luận   : KHÔNG PHẢI LỖI hồi quy giết lan trên TOÀN BỘ tập cũ. Phạm vi mạnh hơn mẫu 9/12 tên các lượt trước. Không tự đổi các bo_qua ngoài ba ca mới thành qua; tổng trạng thái thật sẽ ghi ở phần chốt 320.

HƯỚNG 15: MỚI — xung đột tên thư mục/đối số CLI với cửa tự kiểm
  giả thuyết : Dispatcher dò cờ bằng membership trên toàn argv trước --gop có thể hiểu nhầm giá trị đối số thành chế độ tự kiểm, rồi trả 0 mà chưa gom.
  lệnh       : python evidence/env.py python -u evidence/cli_mode_collision.py; cli_collision_workflow.py
  output     : Trên HEAD NGUYÊN BẢN, cùng thư mục rỗng tên --tu-kiem-che-do: argv [--gop, ./--tu-kiem-che-do] ⇒ rc=1 G-rong, đã gọi gom; argv [--gop, --tu-kiem-che-do] ⇒ rc=0, chỉ in KQ, KHÔNG gọi gom. [--gop, missing, --tu-kiem-che-do] cũng rc=0 KQ thay vì lỗi đối số. Validator workflow control=[]; thêm cờ tự kiểm vào lệnh gom ghim ⇒ lỗi sai hình dạng G5.
  kết luận   : LỖI (P2), F25 nối lớp CLI F8/F13/F17/F20. Đây là lỗi chức năng của head, không cần đột biến để tạo lỗi. Phạm vi hẹp là phân giải đối số/chế độ CLI; ci.yml hiện ghim --gop manh và validator từ chối cờ thừa, nên chưa chứng minh CI xanh khi bỏ đo. Không nâng thành P1 workflow. Cần parse mode theo vị trí/cấu trúc và từ chối mode xung đột; mọi nhánh tự kiểm không được chiếm giá trị thư mục của --gop.

Đính chính phân loại hướng mới: I/O/tệp dở/symlink đã được đo ở lượt 3/5/6; HƯỚNG 7 là hồi quy, không tính vào yêu cầu ≥2 hướng mới. Hai hướng mới độc lập ở lượt này là (1) bóc riêng chốt kiểu từng trường/loại tệp để đo răng, thay vì chỉ gỡ cả guard; (2) xung đột đối số CLI với dispatcher tự kiểm. Miền nhiều CA bỏ qua là hướng bổ sung mới ở dữ liệu main. Các phép đều chạy trên bản sao; không dựng payload ẩn/điều khiển.

HƯỚNG 16: Chốt đủ 320 bán kính và tính nguyên vẹn
  giả thuyết : Không còn hồi quy bán kính ngoài những điểm đã kiểm riêng; kết quả phải bám đúng head được giao.
  lệnh       : python evidence/env.py python -u evidence/radii.py all; summarize_r8.py; final_snapshot.py
  output     : TOTAL 320 ERRORS 0, tiến trình rc=0. Đúng tập 320 tên của head; mỗi tên đủ 56 trạng thái và CHỈ ca đích giet_that, bán kính 1/56. Tổng 17.584 qua + 320 giet_that + 16 bo_qua, không tin_dung_gia. Tập cũ 212: 11.644 qua + 212 giet_that + 16 bo_qua; t52/t53/t54 636/636 qua. Tập mới 108: 5.940 qua + 108 giet_that, không bỏ qua. f9_sha_hang/f9_head_hang chỉ giết t53; 13 mutant f18–f21 đều đúng đích. HEAD/tree cuối khớp đầu; status tracked/untracked/ignored của cay-kho rỗng; diff/index rỗng; SHA-256 năm tệp ứng viên và SPEC giữ nguyên. Bản sao đo cũng không đổi tracked files, chỉ có marker ignored .claude/.packet_state/.
  kết luận   : KHÔNG PHẢI LỖI hồi quy bán kính trên head này. Đã đo đủ 320, không dùng mẫu thay toàn bộ. Không đổi 16 bo_qua của các ca khác dưới mutant cũ thành qua; theo bộ kết luận hiện hành chúng không làm sai bán kính, không ca đích hay t52/t53/t54 nào bị bỏ qua. Đây là vòng đo riêng, không tự gọi nó là A1 tám CLI mảnh thật hoặc full CI.

Chốt số lượng: 9 lớp theo dõi, 3 lớp còn mở (main, CLI, cấu trúc gom), 6 lớp đóng trong phạm vi đo. Ba finding mới P2: F23–F25; không có P1/P3 mới được chứng minh. Có đủ 114 phép checklist kế thừa + 15 phép đổi mới, mỗi phép 56 CA; các đối chứng dữ liệu/CLI bổ sung lưu riêng. JSON, bảng từng phép và log gốc ở evidence/README.md, evidence/summary.json và evidence/mutation-matrix.md.

Giới hạn và thông tin phiên:

- Linux, Python 3.11.15; actionlint 1.7.7, shellcheck 0.9.0; Ruff dùng `python -m ruff` 0.15.15. Không suy bare binary Ruff trên PATH thành binary của phép đo.
- Không GitHub CI, không commit/push, không sửa mã ứng viên, không đăng verdict ra ngoài. Bản sao trong /tmp có thể nhận marker/cache do test; cây `cay-kho` được đối xử read-only. Filesystem sandbox thực tế là workspace-write, không khai có cưỡng chế read-only cho checkout.
- Chưa đo A1 chạy nguyên tám CLI mảnh thật rồi gom trên head này; chưa chạy CLI mặc định main đủ từ đầu tới cuối. Vòng bán kính riêng, gate M1 và đường con F22 là các phép đo độc lập; không gọi chúng là A1/full CI. Chưa đo Windows, Actions upload/download thật, ruleset, A9 thời gian runner.
- Fixture 320 bản ghi trong phép gom được tổng hợp để kiểm hợp đồng dữ liệu, không phải tự nhận 320 phép đo thật. Kết quả bán kính thật có JSON riêng chứa 56 trạng thái/đột biến.
- Chỉ dùng các payload workflow đã có trong cây; không có biến thể ký tự ẩn/điều khiển mới đủ căn cứ cần mô tả. Hai hướng mới độc lập là ablation riêng từng trường kiểu/loại tệp và xung đột đối số CLI với dispatcher tự kiểm. I/O/tệp cũ là hướng đo lại.
- Snapshot đầu/cuối không chứng minh lịch sử mọi thao tác; các số đo này chỉ neo head được giao. Không xác minh các số lịch sử/CI trong SPEC hay danh tính người ký lease.

BẢNG LỚP FINDING — giữ nguyên lớp lịch sử

| Slug lớp | Chuỗi finding | Trạng thái lượt 8 | Bằng chứng / cách khép |
|---|---|---|---|
| g5-main-thieu-ca-chon-vong-ban-kinh | F2 → F5 → F6 → F7 → F12 → F15 → F18 → F23 | Chưa đóng, P2 | Các răng 0/1/>1, N khác 8, cộng nhiều nguồn, nhiều dòng đã hoạt động; còn nhiều CA bỏ qua và lý do receiver nguyên |
| g5-gom-cli-thieu-rang | F8 → F13 → F17 → F20 → F25 | Chưa đóng, P2 | Checklist CLI cũ và phép đảo bảng bị bắt, nhưng xung đột mode/giá trị argv trên head thật bỏ qua gom |
| g5-gom-phan-quyet-thieu-rang | F16 → F19 | Đóng trong phạm vi đo | Bỏ/gán đè kết luận, cộng lỗi, đảo/lặp/cắt bảng đều bị t52 bắt |
| g5-manh-phan-quyet-thieu-rang | F21 | Đóng trong phạm vi đo | Bản ghi do sai kết quả ở cuối/đầu+cuối; writer chỉ xét lỗi transport hoặc bản ghi đầu bị bắt |
| g5-cli-gian-giao-thieu-phu-thuoc | F22 | Đóng — ĐÃ VÁ THẬT | Năm mutant cũ đúng bán kính; t52/t53/t54 15/15 qua; đường con thật lỗi=0 |
| g5-shell-bo-qua-thuc-thi | F1 → F3 → F10 → F14 | Đóng trong phạm vi đo | 60 phản chứng; ablation các hàng rào làm đúng nhóm ca lọt |
| g5-nguon-van-tay-thieu-rang | F9 | Đóng trong phạm vi đo | f9_sha_hang/f9_head_hang đúng đích t53, không kéo t52 |
| g5-chu-thich-dem-cu | F11 | Đóng | t152 head/base qua; hook/ci đồng bộ 5 vị trí |
| g5-gom-cau-truc-thieu-rang | F24 — mới | Chưa đóng, P2 | Bool/float phien_ban và symlink không có phép gác độc lập. Khác F16/F19 về phán quyết/bảng trên bản ghi đo |

| F<n> | mức | tệp:dòng | mô tả | phản chứng |
|---|---|---|---|---|
| F23 | P2 | ops/cong_cu_test.py:6654, :7519, :7556; dây thật :7669, :7673, :7692 | Main vẫn thiếu quan sát khi có nhiều CA bỏ qua; giàn giáo nén lý do receiver thành rc. So stdout nguyên không bù được dữ liệu/kịch bản đã bỏ mất. | skip_first_diagnostic, skip_boolean_count, main_no_error_tail sống 56/56; main-skip-wiring.log: mất ca thứ hai hoặc 54/54,bỏ qua=2 thành 54/55,bỏ qua=1. main-reason.log: mất danh sách kết quả thiếu, chỉ còn rc=0. |
| F24 | P2 | ops/cong_cu_test.py:7215, :7224, :7382; t52 :6583 | Phản chứng cấu trúc chỉ dùng bool ở manh và một thư mục, nên không có răng riêng cho kiểu phien_ban và symlink. | new-header_type_phien_ban.json, new-header_accept_symlink.json: 56/56 qua; schema-io.log: control G-dau/G-tep lỗi=1, mutant nhận phien_ban=true/1.0 hoặc symlink, gom lỗi=0. |
| F25 | P2 | ops/cong_cu_test.py:7848, :7854; helper :7271 | Dispatcher tìm cờ tự kiểm ở mọi vị trí argv trước --gop, nên chiếm cả tên thư mục hoặc cờ xung đột và thoát 0 mà không gom. | cli-mode-collision.log: cùng thư mục rỗng, --gop ./--tu-kiem-che-do rc=1 G-rong; --gop --tu-kiem-che-do rc=0 KQ, không gom. cli-collision-workflow.log: lệnh ghim hiện tại vẫn được bảo vệ. |

Gợi ý hướng sửa (không viết bản vá sản phẩm):

- F23: thêm nhiều CA bỏ qua cùng lúc; kiểm từng tên, lý do và các số đếm. Giữ nguyên lý do receiver tại điểm ghi nhật ký, không chỉ trích rc. Đột biến cắt danh sách, bool-hoá số đếm, bỏ lý do/đuôi stdout phải bị ca đúng bắt; đo lại bán kính cũ để tránh kéo t52/t53/t54 vào bán kính 2.
- F24: bảng fixture xấu theo từng trường có hợp đồng kiểu, cùng đối chứng tệp thường/symlink. Phép kiểm phải phân biệt chốt đúng từ chối với exception/chốt khác; bóc từng phần của guard phải làm ca đích đỏ. Không thay bộ phân hạng chung để sửa kiểm cấu trúc.
- F25: parse argv một lần theo vị trí/cấu trúc; mode loại trừ nhau; giá trị thư mục không được kích cửa tự kiểm. Thử CLI thật với cùng đường dẫn có/không có `./`, đường dẫn bình thường, và nhiều mode cùng lúc; đối số xung đột phải đỏ trước mọi công việc.

ĐỐI CHIẾU F1–F22 (không có F4)

| Finding | Trạng thái | Đối chiếu độc lập |
|---|---|---|
| F1 | đóng — ĐÃ VÁ THẬT | 20/20 ca; bỏ hai chốt thực thi/Bash cho 18 lọt, hai ca workflow còn chốt riêng |
| F2 | chưa đóng lớp | Chọn mode đã có răng; F23 còn ở main |
| F3 | đóng — ĐÃ VÁ THẬT | 28/28; splitlines + bỏ hàng rào toàn thân làm 27 lọt |
| F5 | chưa đóng lớp | Dây mảnh/rc đã có răng; lý do receiver còn bị nén (F23) |
| F6 | chưa đóng lớp | Giá trị/vân tay/worker đã có răng; bảo toàn chẩn đoán/số đếm còn F23 |
| F7 | chưa đóng lớp | Danh tính CA/nhật ký đã có răng; nhiều ca bỏ qua chưa được quan sát |
| F8 | chưa đóng lớp | Helper/bảng CLI đã vá thật; dispatcher còn xung đột argv F25 |
| F9 | đóng — ĐÃ VÁ THẬT | Hai mutant nguồn chỉ giết t53, không lan |
| F10 | đóng — ĐÃ VÁ THẬT | 7/7; bỏ guard làm 7/7 lọt |
| F11 | đóng — ĐÃ VÁ THẬT | t152 head/base qua, chú thích đúng |
| F12 | chưa đóng lớp | Danh tính CA/chuỗi kết quả đã vá; F23 vẫn thuộc bảo toàn đầu ra main |
| F13 | chưa đóng lớp — biểu hiện cũ ĐÃ VÁ THẬT | Bỏ dispatcher vẫn bị bắt; cửa dispatcher khác còn F25; không hồi quy F22 |
| F14 | đóng — ĐÃ VÁ THẬT | 5/5; bỏ chốt shell tường minh làm 5/5 lọt |
| F15 | chưa đóng lớp | Các phép lỗi ≥2/nhiều nguồn đã bị bắt; miền nhiều CA bỏ qua và lý do nguyên còn F23 |
| F16 | đóng trong phạm vi đo — ĐÃ VÁ THẬT | Bộ đúng schema/sai kết quả không còn lọt các phép cũ; F24 là cấu trúc đầu vào khác lớp phán quyết |
| F17 | chưa đóng lớp — biểu hiện cũ ĐÃ VÁ THẬT | Mã thoát/bảng CLI đã có răng, nhưng phân giải argv còn F25 |
| F18 | chưa đóng lớp — vá thật phần lớn biểu hiện, chưa đủ đóng lớp | 0/1/>1, N khác 8, nhiều dòng/nhiều nguồn đã bị bắt; lý do receiver nguyên vẫn chưa được gác, thêm nhiều CA bỏ qua theo F23 |
| F19 | đóng trong phạm vi đo — ĐÃ VÁ THẬT | Đảo, lặp danh tính, cắt chi tiết bảng gom đều bị t52 bắt |
| F20 | chưa đóng lớp — biểu hiện cũ ĐÃ VÁ THẬT | Đảo bảng riêng tại CLI bị t52 bắt; F25 ở cửa trước gom |
| F21 | đóng trong phạm vi đo — ĐÃ VÁ THẬT | Chỉ cộng lỗi transport, chỉ bản ghi đầu, gán đè lỗi và đảo bảng writer bị t52 bắt |
| F22 | đóng — ĐÃ VÁ THẬT | Năm cây cũ + đường con thật đều lỗi bán kính=0; t52/t53/t54 qua |

Ngưỡng nhiệm vụ là 0 P1/P2/P3. Còn ba P2 (F23/F24/F25), nên yêu cầu sửa; không có P1/P3 mới được chứng minh. Không gọi các răng mới vô hiệu: nhiều biểu hiện đã vá thật, nhưng lớp main và CLI chưa đóng. Quyết định vòng sửa kế tiếp thuộc chủ kho; verdict không tự mở rộng ngân sách hoặc cấp quyền land.

verdict: changes_requested
reviewed_sha: 320475292649a9bf985edccf8e9e35f78243c2e4
