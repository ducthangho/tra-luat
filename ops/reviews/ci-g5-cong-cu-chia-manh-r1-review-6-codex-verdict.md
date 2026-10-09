# Cross-review độc lập — packet #668 r1 g1 — lượt 6

Trạng thái lúc mở: dang_review; kết luận hoàn tất ở cuối.
reviewed_sha: b6e05980f4a9cc13e2e565129637f784de0d8bd0

Các kết quả dưới đây được ghi dần từ phép đo độc lập. Không sửa cây sản phẩm; đột biến chỉ chạy trên bản sao /tmp.

HƯỚNG 1: Neo ứng viên và môi trường
  giả thuyết : Cây được giao đúng SHA, SPEC và write set.
  lệnh       : git -C cay-kho rev-parse HEAD HEAD^{tree}; git -C cay-kho status --short; sha256sum SPEC.md; cat numstat.txt
  output     : HEAD b6e05980f4a9cc13e2e565129637f784de0d8bd0; tree 23f7252c15a0af32c180811a4e6756ebcb18c1ff; status rỗng; SPEC dd2ada1b8511bec1c6c30ffdd7a94a3c34f4024836761878caf73ce339516b15; 5 tệp +1174/-31.
  kết luận   : KHÔNG PHẢI LỖI. Trần ~1.400 và quyền tiếp tục lượt 6 lấy từ chỉ thị hiện tại. Harness ghim commit.gpgsign=false/core.abbrev=7 cho cả git con; không tái dùng kết quả cũ.

HƯỚNG 2: Workflow F1/F3/F10/F14 — chạy phản chứng có sẵn và gỡ chốt
  giả thuyết : Chốt mới từ chối shell vắng, hai hàng rào F3/F10 vẫn có răng độc lập.
  lệnh       : python evidence/env.py python -u evidence/workflow.py; registry-head.log / registry-base.log
  output     : control F1=20/20, F3=28/28, F10=7/7, F14=5/5 đỏ đúng. Gỡ F14 ⇒ 5/5 F14 lọt. Gỡ F10 ⇒ 7/7 F10 lọt. Chỉ trả splitlines ⇒ không F3 lọt; gỡ F10 + splitlines ⇒ 27/28 F3 lọt. Registry head: 1025/1025, TỔNG ĐẠT.
  kết luận   : KHÔNG PHẢI LỖI với các biểu hiện trên. F14 ĐÃ VÁ THẬT; F3 được hai hàng rào độc lập chặn. Mọi payload dùng nguyên ca có sẵn trong cây.

HƯỚNG 3: Hồi quy công cụ và các ca lân cận
  giả thuyết : Không có delta ngoài lớp main/gom.
  lệnh       : python evidence/env.py python -u evidence/regression.py; registry trên /tmp/review668-r6-base và /tmp/review668-r6
  output     : head/base t152 PASS; lease t24/t31/t35/t161/t162 PASS; actionlint rc=0; probe công cụ rc=0. Ruff F rc=1 cả hai: cùng 6 F841 (5 launcher, 1 cong_cu_test), cùng đường/tên/thông điệp, delta=0. Registry baseline=938/938, head=1025/1025; cả hai TỔNG ĐẠT.
  kết luận   : KHÔNG PHẢI LỖI. Bare Ruff không xanh tuyệt đối; tiêu chí delta được đáp ứng. Không chạy --chay toàn bộ suites đăng ký.

HƯỚNG 4: MỚI — nhiều lỗi đồng thời trong main
  giả thuyết : Kịch bản mỗi nguồn một lỗi có thể bỏ lọt phép biến đổi điều kiện truthy thành == 1.
  lệnh       : python evidence/env.py python -u evidence/main_new.py; python evidence/env.py python evidence/wiring_new.py
  output     : writer_eq_one và final_db_eq_one đều sống 56/56, không trạng thái ngoài qua. Wiring: writer trả 2 lỗi ⇒ control rc=1, mutant rc=0; hai kết quả bán kính mỗi kết quả lỗi=1 ⇒ control rc=1, mutant rc=0, stdout vẫn ghi lỗi đột biến=2.
  kết luận   : LỖI (P2), F15 nối lớp F2/F5/F6/F7/F12. Giàn giáo mới đã có hai kết quả nhưng không có hai kết quả cùng lỗi, và writer chỉ trả 0/1. Đây là thiếu răng M4; không khẳng định main chưa đột biến đang xanh sai.

  Phản chứng loại trừ: final_gate_eq_one chỉ tương đương trên miền đầu ra thật của _cong_tren_cay_that (luôn 0 hoặc 1). Wiring giả trả 2 nằm ngoài hợp đồng helper nên KHÔNG được dùng làm finding.

HƯỚNG 5: MỚI — gom phải kết luận dữ liệu đo, không chỉ kiểm cấu trúc
  giả thuyết : Bộ tự kiểm gom chỉ làm sai cấu trúc/header/phân hoạch, có thể chưa đo bản ghi hợp lệ nhưng đột biến sống.
  lệnh       : python evidence/env.py python -u evidence/cli_new.py; python evidence/env.py python -u evidence/cli_semantic_wiring.py; gom_semantics.py
  output     : gop_eq_one (đổi loi += l thành loi = l trong vòng kết luận gom) sống 56/56. CLI thật trên 8 tệp fixture đủ 289 bản ghi, hai đích qua thay vì giet_that: control rc=1, 2 dòng ĐỎ, lỗi đột biến=2; mutant rc=0, vẫn 2 dòng ĐỎ nhưng lỗi đột biến=0. Các mutant bỏ kết luận/cắt bảng đang đo đủ CA; CLI đã xác nhận chúng nhận xanh cùng bộ sai.
  kết luận   : LỖI (P2), F16: thiếu răng ở chốt phân loại và tích luỹ của _gom_manh. M3/M4 đòi cùng _ket_luan_ban_ghi với đường song song; việc helper đúng không bảo vệ dây gọi từ gom. Đây là bộ dữ liệu giả cho phản chứng, KHÔNG phải A1 đo 289 mutant thật.

HƯỚNG 6: CLI F13 và miền mã lỗi lớn hơn một
  giả thuyết : Hai đường âm mới của CLI đều trả lỗi 1 hoặc lỗi đối số 2 trước khi gom; chưa đo số lỗi gom >1.
  lệnh       : python evidence/env.py python -u evidence/cli_new.py; python evidence/env.py python -u evidence/cli_semantic_wiring.py
  output     : cli_eq_one đổi riêng return 1 if loi else 0 thành return 1 if loi == 1 else 0 trong _main_gop, sống 56/56. CLI thật trên bộ 8 mảnh có hai mutant sống: control rc=1, mutant rc=0; cả hai in lỗi đột biến=2. Bộ dương không đột biến: rc=0, 289 dòng ok, GOM MẢNH 8/8; thiếu/thừa đối số rc=2.
  kết luận   : LỖI (P2), F17 nối lớp F8/F13. Biểu hiện bỏ dispatcher cũ được vá; chưa đóng toàn lớp chuyển phán quyết gom qua CLI. Không lấy rc=2 do đối số sai làm kiểm chứng trường hợp gom trả 2 lỗi.

HƯỚNG 7: Gate trọn chế độ giao mảnh và miền phân hoạch gom
  giả thuyết : Head chạy đủ phần gate; gom nhận phân hoạch hợp lệ và fail-closed với lỗi filesystem.
  lệnh       : python evidence/env.py bash -c 'cd /tmp/review668-r6 && CONG_CU_TEST_BAN_KINH=manh python ops/cong_cu_test.py'; python evidence/env.py python evidence/new_paths.py
  output     : Gate rc=0; cong_cu_test: 56/56 đạt, bỏ qua=0, tiền kiểm bỏ qua=0; cổng cây thật=ĐẠT; SỐ LIỆU: ca=56 · đột biến=289 (giao mảnh) · lỗi đột biến=0. 15/15 N=2..16 nhận đủ 289 bản ghi fixture khi đảo thứ tự và đổi tên tệp; symlink trả [G-tep], thư mục ở đích writer ném IsADirectoryError.
  kết luận   : KHÔNG PHẢI LỖI với phạm vi đã đo. Đây là gate M1 đầy đủ; không gọi phép này là A1 hoặc CLI mặc định đo trọn 289 mutant. Bộ fake có mọi ca ngoài đích bo_qua vẫn được nhận như lượt 5; đây là giới hạn chính sách kế thừa, không báo finding mới.

  Bổ sung F15: main_real_writer.py dùng bộ nhận và _ket_thuc_manh THẬT, chỉ giả CA/transport để cô lập dây nối. Hai đột biến sống trong mảnh ⇒ writer báo [M-loi]: 2 lỗi, xoá tệp cũ ở cả hai bên; control main rc=1, mutant writer_eq_one rc=0. Job upload vẫn có thể bắt thiếu tệp, nên finding giữ P2 thiếu răng, không khai đây là P1 của workflow hiện tại.

  Bổ sung F16: gop_drop_judgment (bỏ _ket_luan_ban_ghi) và gop_no_error_sum (bỏ cộng lỗi) đã sống 56/56. CLI thật trên cùng bộ sai lần lượt rc=0 với 0 dòng kết luận / rc=0 với 2 dòng ĐỎ. Đây là lỗ ở phép kiểm dây kết luận của gom, độc lập với hình dạng tệp.

HƯỚNG 8: Main — danh sách nhiều phần tử và báo cáo tổng hợp còn mất quan sát
  giả thuyết : So tên CA và ba dòng marker không tương đương so toàn bộ dữ liệu/đầu ra của main.
  lệnh       : main_new.py; python evidence/env.py python evidence/multi_fault_wiring.py
  output     : baseline_first, precheck_first, full_line_first, writer_line_first, gate_print_drop, baseline_print_drop, summary_errors_zero sống 56/56. Wiring hai CA đỏ: control truyền 2 tên nền vào bán kính, mutant chỉ 1; hai tiền kiểm bỏ qua: control ghi 2, mutant ghi 1. Một lỗi bán kính: summary_errors_zero vẫn rc=1 nhưng in lỗi đột biến=0.
  kết luận   : LỖI (P2), cùng F15. Chưa đóng lớp main: từng nguồn lỗi được kích hoạt đơn lẻ và collector chỉ giữ một dòng đếm + ba số marker, không đo tập nền nhiều phần tử hoặc dòng SỐ LIỆU. Không nâng các lỗi báo cáo riêng lẻ thành P1.

Bảng kiểm độc lập: quyết định / dữ liệu của main (không lấy danh sách DOT_BIEN làm trần)

| Đơn vị main quyết định/truyền đi | Phép đổi đã gửi đo đủ 56 CA | Điểm quan sát cần có |
|---|---|---|
| Đọc env, chọn du/gate/manh; cấu hình sai trả 2 trước mọi CA | config_ignore, shard_never, gate_run_full | rc, nhật ký tiền kiểm/CA/nhánh |
| Gọi đúng hai tiền kiểm, giữ mọi kết quả bỏ qua | batch_skip, alias_skip, precheck_ignore, precheck_first | danh tính, số kết quả và rc, kể cả cả hai bỏ qua |
| CA: đủ tên/thứ tự, gọi đúng một lần, phân biệt ba loại exception | ca_skip, ca_duplicate_middle, ca_reverse, assert_ignore, exception_ignore, skip_as_red | tên từng CA, hong/bo_qua/qua |
| Đếm đạt/bỏ qua và công khai CA/tiền kiểm đỏ | pass_counter, skip_counter, precheck_print_drop, skip_print_drop, failure_print_drop | dòng đếm lẫn chẩn đoán; không chỉ tổng lời gọi |
| Mảnh: lấy k/N/ra, phân hoạch đúng | shard_k/n/ra, partition | đối số thật tới transport/writer |
| Nền đỏ hoặc tiền kiểm bỏ qua: dọn tệp và trả lỗi | base_red_ignore, precheck_ignore, no_cleanup, cleanup_fp, bad_base_rc | writer được gọi với None/lý do/vân tay, rc≠0 |
| Phóng con bằng đúng tên/nền rỗng/số worker | launch_names/baseline/workers, launch_skip_last_group | đủ nhóm được tiêu thụ |
| Nhận từng nhóm: nhóm/rc/stdout/nền rỗng | receiver_group/rc/output/baseline, receiver_ca_baseline, receiver_skip_call | dữ liệu hợp lệ và từ chối riêng rc sai/stdout sai |
| Giữ lý do đầu tiên, không mất nhóm/giá trị | no_reason, break_on_error, reason_last, drop_group, drop_values | tập và giá trị; lý do đầu tiên khi nhiều nhóm lỗi |
| Writer: k/N/ra/tên/ket/ly/vân tay và rc | writer_k/n/ra/names/ket/reason/fp, writer_skip/rc, writer_eq_one, writer_negative_error | toàn bộ đối số; số lỗi 0, 1, >1 |
| In mọi dòng writer | print_writer_drop, writer_line_first | cả bảng lẫn dòng ghi tệp/lý do |
| Cổng cây thật đúng GOC, giữ kết quả và chẩn đoán | gate_skip, gate_root, gate_print_drop, final_gate | rc helper, dòng bằng chứng dương/âm |
| Tự kiểm phân hạng/giàn giáo/song song và cộng lỗi | classifier_skip, scaffold_skip/reset, parallel_skip/arg/reset | thứ tự, do_o_nen, không xoá lỗi trước |
| Tập mọi tên nền đỏ, báo cáo nền và cộng lỗi | baseline_empty/report_arg/errors/reset, baseline_first, baseline_print_drop | tập nhiều tên; lỗi nền + báo cáo |
| Gate công khai giao bán kính; du truyền mọi tên/nền/worker | gate_run_full, gate_notice_drop, full_names/base/workers | đúng nhánh, tham số và thông báo M1 |
| Du đọc mọi kết quả, mọi dòng, tích luỹ mọi lỗi | full_errors/reset/first_only/repeat_result, print_full_drop, full_line_first, final_db_eq_one | lỗi đầu/cuối/cùng lúc; kết quả nhiều dòng |
| Dòng tổng hợp: mode, số CA/mutant/lỗi/precheck/cổng | summary_errors_zero, summary_gate_pass | không in số lỗi 0 hoặc cổng ĐẠT khi đã đỏ |
| Mã thoát cuối từ hong/loi_db/precheck/cổng | final_hong/db/precheck/gate, final_db_eq_one | mọi nguồn lỗi đơn lẻ và lỗi tổng >1 |

Cặp neo/thay chính xác và 56 trạng thái mỗi phép nằm trong evidence/main-mutations.json, main-new-mutations.json và các JSON main-*. Bảng từng phép được sinh ở evidence/main-matrix.md. Miền không có tên mảnh là nhánh phòng thủ: với 289 DOT_BIEN và N≤16, mọi mảnh hợp lệ đều không rỗng. Không dùng dữ liệu ngoài hợp đồng helper để báo lỗi tương đương; không coi phép đổi thuần văn phong là chốt độc lập.

Gợi ý khắc phục cho executor (mô tả, không phải patch hay quyền sửa):

- **F15 — vá tại t54/_in_tu_kiem_main.** Dùng kịch bản nhiều CA đỏ, hai tiền kiểm cùng bỏ qua, hai nhóm con cùng lỗi, writer trả số lỗi >1 và hai kết quả bán kính cùng lỗi. So tập nền đầy đủ, lý do đầu tiên, toàn bộ các dòng có ý nghĩa hợp đồng (bảng, chẩn đoán, giao mảnh, SỐ LIỆU), không chỉ một dòng đếm và marker. Ca khoá phải giết writer_eq_one/final_db_eq_one/baseline_first và các phép xoá/cắt/sửa đầu ra; giữ control xanh. Nguy cơ: so quá rộng vào văn phong hoặc helper sẽ làm ca giết oan mutant cũ; giới hạn t54 vào dây main và kiểm lại bán kính 1/56.
- **F16 — vá tại t52/_in_tu_kiem_gom, chốt gọi kết luận trong _gom_manh.** Sau khi dựng bộ mảnh hợp lệ, sửa trạng thái đích của một hoặc nhiều bản ghi thành qua/bo_qua/tin_dung_gia mà vẫn giữ đúng schema/tập tên. Đặt lỗi ở đầu, giữa, cuối và ở nhiều tệp; yêu cầu rc≠0, đúng số lỗi, đủ bảng đúng thứ tự. Ca khoá phải giết bỏ _ket_luan_ban_ghi, bỏ cộng lỗi, gán đè lỗi và cắt vòng còn một bản ghi. Nguy cơ: writer cố ý không ghi bộ lỗi; phải sửa dữ liệu SAU writer để phép thử đi tới chốt gom, tránh chết sớm ở schema hoặc biến thành phép thử writer lần hai.
- **F17 — vá tại t52 và đường CLI thật.** Đưa bộ đủ cấu trúc nhưng có ≥2 lỗi kết luận qua CHÍNH `python ops/cong_cu_test.py --gop ...`, cùng bộ đạt; đòi rc chuẩn hoá 0/1 và bảng/SỐ LIỆU đủ. Ca khoá phải giết cli_eq_one/cli_output_first và vẫn giết f13_dispatcher_nuot. Có thể dựng kho git tạm từ chính TEP_TEST đang đột biến và lấy vân tay thật tại đó; không cần coi đường dương dưới mutation là bất khả thi. Nguy cơ: dùng HEAD/hash của cây đối chứng sẽ gây đỏ oan mọi mutant hoặc giết thêm t53; vân tay fixture phải khớp đúng tiến trình CLI được đo.

Các hướng mới của lượt 6 là (1) miền số lượng lỗi/danh sách nhiều phần tử ở main; (2) kết luận gom trên bản ghi đúng cấu trúc nhưng đột biến sống. CLI với số lỗi >1 là hướng bổ sung, khác lỗi bỏ dispatcher đã báo ở lượt 5. Không dựng biến thể payload ẩn/điều khiển mới; sau chốt toàn thân run + Bash tường minh, không có biến thể mới thuộc loại đó đủ căn cứ để báo bằng lời.

HƯỚNG 9: Hồi quy bán kính mẫu cũ, và trạng thái phép đo dài
  giả thuyết : Ba ca mới không giết lan mutant cũ.
  lệnh       : python evidence/env.py python -u evidence/radii.py old; python evidence/summary.py
  output     : TOTAL 9 ERRORS 0; 27/27 trạng thái t52/t53/t54 đều qua. Toàn mẫu: 484 qua, 9 giet_that đúng đích, 11 bo_qua ngoài ba ca mới; không tin_dung_gia. 19 phép mới main: 3 bị t54 giết, 16 sống; 4 gom_semantic đều sống; CLI/helper bổ sung: 3 sống, dispatcher_exit_normalized bị t52 giết.
  kết luận   : KHÔNG PHẢI LỖI hồi quy lan sang ca mới trên mẫu đã đo. Không suy từ mẫu này sang toàn bộ 212 mutant cũ. Các survivor có hậu quả thuộc F15/F16/F17; final_gate_eq_one nằm ngoài miền lỗi >1 của helper và không phải lỗi. Các lượt 68/77 tiếp tục chạy, kết quả cuối sẽ chốt riêng.

  Răng workflow bổ sung: gỡ đồng thời _loi_thuc_thi_g5 và chốt Bash mới ⇒ 18/20 F1 + 7/7 F10 + 5/5 F14 lọt. Hai F1 cấp workflow vẫn bị chốt defaults/env độc lập bắt. Chỉ gỡ _loi_thuc_thi_g5 ⇒ 13/20 F1 lọt vì chốt Bash mới còn đứng; không phải năm phản chứng mất răng.

HƯỚNG 10: Đối chứng mã chưa đột biến — chế độ và dữ liệu gom sai
  giả thuyết : Các survivor chứng minh thiếu răng, không tự chứng minh head nguyên bản xanh sai.
  lệnh       : python evidence/env.py python evidence/mode_domain.py; python evidence/env.py python evidence/gom_current_data.py
  output     : Lưới 10.816 cặp k/N nhận đúng 135 cặp hợp lệ, từ chối 10.681 cặp còn lại, 0 mismatch; 11 dạng ASCII sai bị từ chối. Các env rỗng/lạ/orphan/thiếu đầu ra/cả hai chế độ trả đúng thẻ. Gom head: valid lỗi=0 với 289 dòng; survives/target_skipped/false_credit/wide_radius/measurement_error mỗi bộ lỗi=1 và đủ 289 dòng; unknown_case/wrong_target bị [G-ban-ghi].
  kết luận   : KHÔNG PHẢI LỖI chức năng trên đầu vào đã thử. F15/F16/F17 là P2 về chốt thiếu răng; không đánh tráo kết quả mutant thành P1 của head chưa đột biến.


Chốt đầy đủ các phép đo bắt buộc (chỉ ghi sau khi tất cả tiến trình kết thúc):

- **68/68 checklist lượt 5 đã chạy lại trên head này**, cặp neo/thay đối chiếu bằng nhau với 62+6 phép của lượt 5. 64 bị giết; 4 sống 56/56: receiver_baseline, break_on_error, baseline_errors, final_hong. Không bo_qua/tin_dung_gia. Toàn bộ từng ca nằm trong JSON và evidence/main-matrix.md.
- **19/19 phép main bổ sung** đã chạy đủ 56 ca: 3 bị t54 giết, 16 sống. Danh sách và phân loại nằm ở evidence/summary.json; hậu quả có ý nghĩa đã tái hiện trong main-real-writer.log, multi-fault-wiring.log và wiring-new.log. final_gate_eq_one tương đương trên miền thật 0/1; không dùng wiring giả giá trị 2 để báo finding.
- **77/77 mutant chính thức mới** (`g668_*`, `f2_*`, `f5_*`, `f6_*`, `f7_*`, `f8_*`, `f9_*`, `f12_*`, `f13_*`) giết đúng ca đích, bán kính **1/56**, lỗi bán kính=0: **4.235 qua + 77 giet_that**, không bo_qua/tin_dung_gia. Không cần phép đo bù t47 như lượt 5; đây là các lượt đã ghim môi trường từ đầu.
- **F12/F13 mới thêm: 7 f12_* + 1 f13_*** có răng thật; F13 bỏ `sys.exit(_main_gop())` bị đúng t52 bắt. Tuyên bố đóng từng mutant được xác nhận; không suy nó thành đóng cả lớp.
- **9 mutant cũ**: lỗi bán kính=0, đúng đích; 27/27 trạng thái t52/t53/t54 qua. 484 qua + 9 giet_that + 11 bo_qua ngoài ba ca mới. Không mở rộng kết luận sang 212 mutant cũ.
- **8 phép gom/CLI bổ sung**: 7 sống 56/56; đổi dispatcher chuẩn hoá mọi mã thoát thành tối đa 1 bị đúng t52 bắt. 5 survivor gắn F16 (bỏ kết luận, bỏ cộng, gán đè, cắt vòng, xoá bảng); 2 survivor gắn F17 (==1 và cắt stdout).
- **Workflow**: F1 20/20, F3 28/28, F10 7/7, F14 5/5; registry head 1025/1025, baseline 938/938, rc=0. Ablation và giới hạn hai hàng rào ghi ở HƯỚNG 2/9.
- **Gate M1 trọn** rc=0, 56/56, bỏ qua=0, tiền kiểm bỏ qua=0, cổng cây thật ĐẠT, N126 ĐẠT, lỗi đột biến=0, giao 289 mutant. **t152**, nhóm lease t24/t31/t35/t161/t162, actionlint và probe công cụ đều qua trên cả head/base. **Ruff F delta=0** (bare lint rc=1 cả hai, cùng 6 F841).

Phân loại survivor checklist cũ: receiver_baseline dùng tên không có trong CA nên không đổi tập thực; final_hong được loi_nen bảo vệ và không đổi kết quả; break_on_error vẫn đỏ và không ghi tệp nên không có bằng chứng xanh sai (đổi phạm vi thu chẩn đoán ở đường đã lỗi). baseline_errors vẫn đỏ nhờ hong nhưng làm khác số lỗi trong SỐ LIỆU; phần không được quan sát này nối điểm mù đầu ra F15, không phải chứng minh rc sai.

Giới hạn và thông tin phiên:

- Reviewer OpenAI Codex, họ GPT-6 theo cấu hình phiên; bề mặt dịch vụ/API + terminal tools (`codex_service`), transport machine/local. Không có bằng chứng độc lập về exact model ID/effort đã phục vụ, không tự nhận Codex CLI gpt-6-astra hay human_audited. Verdict không cấp quyền land.
- Linux, Python 3.11.15; actionlint 1.7.7; Ruff 0.15.15. Git fixture ghim commit.gpgsign=false/core.abbrev=7 qua evidence/env.py. Các lỗi harness (neo CLI trùng chuỗi khai báo mutant lúc đầu) đã được sửa trước khi chạy; log cuối và JSON là phép đo hoàn tất, không tính lỗi thiết lập thành mutant chết.
- Không sửa/commit/push cây ứng viên, không GitHub CI, không đăng verdict ra ngoài. HEAD/tree cuối khớp neo đầu; diff/index và status cuối (tracked/untracked/ignored) rỗng. Status đầu dùng --short; không có snapshot ignored trước phép đo đầu tiên, các lần kiểm đầy đủ về sau đều rỗng. Snapshot không chứng minh lịch sử mọi lần ghi; sandbox thực tế workspace-write, checkout được đối xử read-only theo vai trò.
- **Chưa đo:** A1 tám mảnh thật đủ 289 mutant trên head này; CLI mặc định chạy trọn 289; Windows/Actions runner, upload/download artifact thật, ruleset và A9. Fixture 8 mảnh chỉ kiểm gom/CLI, không thay A1. Lời executor về A1 trên ef01112 không được dùng để nghiệm thu b6e05980.
- Ma trận là tập biến đổi hữu hạn, không phải chứng minh toán học mọi chương trình đột biến. Không xác nhận mọi con số lịch sử trong SPEC/handoff. Tất cả số được dùng cho kết luận lượt này có log/JSON tự đo trong evidence/.

Bảng lớp finding — giữ slug lịch sử:

| Slug lớp | Nguồn và chuỗi finding | Trạng thái lượt 6 | Cách đóng/đối chiếu |
|---|---|---|---|
| g5-main-thieu-ca-chon-vong-ban-kinh | F2@c8f52b6 → F5@c454ee9 → F6@2b501ef → F7@971e14c → F12@ef011126 → F15@b6e05980 | Chưa đóng, P2 | Các mutant cũ đã được đo lại; miền nhiều lỗi/nhiều tên/đầu ra vẫn thiếu quan sát. Cần F15 |
| g5-gom-cli-thieu-rang | F8@971e14c → F13@ef011126 → F17@b6e05980 | Chưa đóng, P2 | Bỏ dispatcher bị bắt; số lỗi gom >1 và toàn bảng CLI vẫn chưa được gác. Cần F17 |
| g5-gom-phan-quyet-thieu-rang | F16@b6e05980 (lớp mới, khác schema và CLI) | Chưa đóng, P2 | Gom phải gọi đủ bộ kết luận, tích luỹ lỗi và công khai đủ mọi bản ghi. Cần F16 |
| g5-shell-bo-qua-thuc-thi | F1@c8f52b6 → F3@c454ee9 → F10@971e14c → F14@ef011126 | Đóng trong phạm vi đo | 60 ca F1/F3/F10/F14 chặn đúng; ablation chứng minh răng; chưa phát hiện biến thể mới |
| g5-nguon-van-tay-thieu-rang | F9@971e14c | Đóng | Hai f9_* đúng đích t53; test thật bytes/HEAD/no-Git qua |
| g5-chu-thich-dem-cu | F11@971e14c | Đóng | t152 head/base PASS; số thật và chú thích cùng 5 |

Có 6 lớp theo dõi: 3 mở, 3 đóng trong phạm vi review; 3 finding mới P2, không có P1/P3 mới. F16 tách thành lớp mới vì lỗi nằm ở bước quyết định trên bản ghi bên trong gom; F17 ở chuyển kết quả/đầu ra sang CLI; sửa chỉ một nơi không đóng nơi kia. Nhiều mutant cùng một cơ chế được gộp dưới một finding, không đếm thành nhiều lỗi.

| F<n> | mức | tệp:dòng | mô tả | phản chứng |
|---|---|---|---|---|
| F15 | P2 | ops/cong_cu_test.py:6545, :7253, :7336; main :7452, :7465, :7483, :7488 | Giàn giáo main chỉ kích lỗi đơn lẻ, quan sát stdout chưa đầy đủ; số lỗi >1, tập nền nhiều tên và báo cáo sai còn sống | main-new-writer_eq_one.json / main-new-final_db_eq_one.json: 56/56 qua; main-real-writer.log, wiring-new.log control=1/mutant=0; multi-fault-wiring.log chứng minh mất tên/báo cáo sai |
| F16 | P2 | ops/cong_cu_test.py:6490, :7139; chốt :7113 | t52 thiếu bộ đúng cấu trúc nhưng sai kết quả đo; bỏ kết luận/cộng lỗi, ghi đè lỗi hoặc chỉ xét bản ghi đầu vẫn sống | gom-semantic-*.json và cli-new-gop_eq_one.json: mỗi phép 56/56 qua; cli-semantic-wiring.log: control rc=1; bốn phép đổi quyết định trả rc=0 trên hai mutant sống, phép xoá bảng giữ rc=1 nhưng mất bảng |
| F17 | P2 | ops/cong_cu_test.py:6513, :7221; chốt :7129 | CLI chưa đo phán quyết gom >1 lỗi hoặc đủ dòng kết quả; sửa truthy thành ==1 và cắt stdout còn sống | cli-new-cli_eq_one.json / cli-new-cli_output_first.json: 56/56 qua; CLI thật control rc=1 → mutant=0 với lỗi đột biến=2; mutant cắt output mất toàn bảng |

ĐỐI CHIẾU LƯỢT TRƯỚC — F1–F14 (không có F4):

| Finding | Trạng thái | Lý do và phép đo độc lập |
|---|---|---|
| F1 | đóng trong phạm vi đã đo — ĐÃ VÁ THẬT | F1 20/20; F3/F10/F14 cùng lớp đã bị chặn; gỡ hai chốt ngữ nghĩa/Bash làm 18 F1 lọt |
| F2 | chưa đóng lớp — VÁ HỜ ở cấp lớp | Chọn du/gate/manh đã có răng; F15 còn trong cùng lớp main |
| F3 | đóng — ĐÃ VÁ THẬT | 28/28 ca có sẵn bị chặn; gỡ hai hàng rào làm 27 lọt |
| F5 | chưa đóng lớp — VÁ HỜ ở cấp lớp | Dây nhận/ghi/lỗi từng biểu hiện cũ đã vá; writer >1 lỗi còn F15 |
| F6 | chưa đóng lớp — VÁ HỜ ở cấp lớp | Giá trị/vân tay/worker/tiền kiểm riêng đã vá; tập nhiều phần tử/đầu ra còn F15 |
| F7 | chưa đóng lớp — VÁ HỜ ở cấp lớp | Nhật ký đúng danh tính CA mới có răng, nhưng chưa đo đủ mọi dữ liệu main theo F15 |
| F8 | chưa đóng lớp — VÁ HỜ ở cấp lớp | Helper/dispatcher có thêm răng; chuyển số lỗi >1 còn F17 |
| F9 | đóng — ĐÃ VÁ THẬT | Hai mutant nguồn giết đúng t53, không lan |
| F10 | đóng — ĐÃ VÁ THẬT | 7/7 bị chặn, gỡ chốt làm 7/7 lọt |
| F11 | đóng — ĐÃ VÁ THẬT | 5 AL_VER, chú thích đúng 5, t152 PASS |
| F12 | chưa đóng lớp — biểu hiện cũ ĐÃ VÁ THẬT, cấp lớp VÁ HỜ | Danh tính CA, hai kết quả đầu/cuối và marker stdout đã vá; lỗi đồng thời/tập nhiều tên/đầu ra khác vẫn thiếu răng (F15) |
| F13 | đóng biểu hiện dispatcher — ĐÃ VÁ THẬT; lớp CLI chưa đóng | f13_dispatcher_nuot giết đúng t52; dispatcher_exit_normalized cũng bị bắt. Miền số lỗi gom >1 thuộc F17 |
| F14 | đóng — ĐÃ VÁ THẬT | 5/5 ca bỏ shell đỏ đúng; gỡ chốt mới làm cả 5 lọt |

Không gọi các bản vá riêng vô hiệu: những răng mới đã hoạt động. Nhãn VÁ HỜ ở cấp lớp có nghĩa acceptance của cả lớp vẫn chưa đóng, không có nghĩa executor chưa sửa biểu hiện được báo.

Ngưỡng packet là 0 P1/P2/P3. Còn F15/F16/F17 ở mức P2, nên yêu cầu sửa. Lớp main tiếp tục tái diễn; quyền quyết định vòng sửa/review tiếp theo thuộc chủ kho/điều phối theo S3, không do verdict tự mở rộng. Không yêu cầu dừng các phép đo đã được giao trong lượt này.

verdict: changes_requested
reviewed_sha: b6e05980f4a9cc13e2e565129637f784de0d8bd0
