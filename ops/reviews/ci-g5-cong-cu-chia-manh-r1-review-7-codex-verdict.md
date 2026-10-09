# Cross-review độc lập — packet #668, lượt 7

Trạng thái lúc mở: dang_review; kết luận hoàn tất ở cuối.
reviewed_sha: 2bb11df16f0b35d611e8650f384d3c5b421295e5

Đang đo độc lập; không sửa mã sản phẩm. Đột biến chỉ trên bản sao trong /tmp. Không tự dựng payload ký tự điều khiển/ẩn.

HƯỚNG 1: Neo head, phạm vi và môi trường
  giả thuyết : Vật liệu đúng ứng viên, SPEC và write set được giao.
  lệnh       : git -C cay-kho rev-parse HEAD HEAD^{tree}; git -C cay-kho status --porcelain --ignored; sha256sum SPEC.md; cat numstat.txt
  output     : HEAD=2bb11df16f0b35d611e8650f384d3c5b421295e5; tree=78f9beafa77a3e807696309bc2959c77c25f6d83; status rỗng; SPEC=dd2ada1b8511bec1c6c30ffdd7a94a3c34f4024836761878caf73ce339516b15; 5 tệp +1322/-31 theo numstat thật (khác +1325 trong prompt).
  kết luận   : KHÔNG PHẢI LỖI sản phẩm. Trần ~1.400 và quyền tiếp tục lấy từ chỉ thị lượt này. Bản sao /tmp/review668-r7 và /tmp/review668-r7-base; bytecode tắt, git fixture ghim core.abbrev=7/commit.gpgsign=false. Không dùng kết quả lượt trước thay phép đo mới.

Đã tìm thấy script/ma trận lượt 6 trong ../rv6/evidence; sao chép harness vào evidence, đổi đường cây đo sang r7 và mở bộ mutant chính thức thêm f15/f16/f17. Mọi kết quả r7 được chạy lại.

HƯỚNG 2: Workflow F1/F3/F10/F14 và răng hai hàng rào
  giả thuyết : Bản vá F15–F17 không mở lại lớp workflow đã đóng.
  lệnh       : python evidence/env.py python -u evidence/workflow.py; python evidence/env.py python -u evidence/workflow_ablation_extra.py
  output     : Control F1=20/20, F3=28/28, F10=7/7, F14=5/5 đỏ đúng. Gỡ F10 ⇒ 7/7 F10 lọt; chỉ splitlines ⇒ 0 F3 lọt; splitlines + gỡ F10 ⇒ 27/28 F3 lọt. Gỡ F14 ⇒ 5/5 F14 lọt. Gỡ chốt thực thi + Bash ⇒ 18/20 F1, 7/7 F10, 5/5 F14 lọt; hai F1 cấp workflow vẫn bị chốt độc lập bắt.
  kết luận   : KHÔNG PHẢI LỖI trong phạm vi đo. Chạy nguyên các phản chứng sẵn có; không soạn payload ký tự đặc biệt. Chưa có biến thể mới đủ căn cứ để báo bằng lời.

HƯỚNG 3: Hồi quy registry, t152, lease, actionlint và bare Ruff
  giả thuyết : Không có delta trên các cổng lân cận.
  lệnh       : python evidence/env.py python -u evidence/regression.py; python evidence/env.py python /tmp/review668-r7/.claude/dev/ci_dang_ky_test.py; cùng lệnh trên /tmp/review668-r7-base
  output     : Registry head 1025/1025; base 938/938; TỔNG ĐẠT, rc=0 cả hai. t152 và lease t24/t31/t35/t161/t162 PASS cả hai. actionlint ci.yml rc=0; probe cong_cu rc=0 cả hai. Bare Ruff --no-cache --select F trên W1/W3/W4 rc=1 cả hai, cùng 6 F841; delta=0.
  kết luận   : KHÔNG PHẢI LỖI. Bare Ruff có nợ nền, không gọi là lint xanh tuyệt đối. Không chạy toàn bộ suites --chay của registry.

HƯỚNG 4: MỚI — lỗi đơn sau khi giàn giáo chuyển sang giá trị ≥2
  giả thuyết : Vá `==1` bằng việc chỉ kích lỗi ≥2 có thể bỏ hẳn miền đúng một lỗi thật.
  lệnh       : python evidence/env.py python -u evidence/main_extra.py; python evidence/env.py python evidence/main_wiring_r7.py
  output     : writer_gt_one và final_db_gt_one đều sống 56/56 (mọi trạng thái qua). Wiring mảnh dùng receiver/writer THẬT và đúng một mutant sống: control rc=1, mutant rc=0; cả hai không ghi tệp và in [M-loi]: 1 lỗi. Wiring đủ, helper phân hạng trả 1: control rc=1, mutant rc=0, stdout vẫn ghi lỗi đột biến=1.
  kết luận   : LỖI (P2), F18 nối lớp main F2/F5/F6/F7/F12/F15. Đây là thiếu răng M4, không phải head nguyên bản tự gom xanh sai. Job upload vẫn có thể bắt tệp thiếu, nên không nâng thành P1.

HƯỚNG 5: MỚI — main bị đóng cứng N=8 dù helper hỗ trợ N=2..16
  giả thuyết : Một mẫu 3/8 trong giàn giáo main không phân biệt truyền tham số với hằng số 8.
  lệnh       : main_extra.py (shard_n_fixed_eight, partition_fixed_eight); main_wiring_r7.py với cấu hình 1/3
  output     : Cả hai phép đổi sống 56/56. Control 1/3 phóng 102/307 tên, header N=3, rc=0. Gán n=8 phóng 39 tên, header N=8, rc=0. Chỉ cố định `_phan_manh(k,8)` phóng 39 tên nhưng header vẫn N=3, rc=0.
  kết luận   : LỖI (P2), gộp F18 cùng điểm mù dữ liệu main. Không báo P1: gom nguyên bản sẽ từ chối phân hoạch thiếu hoặc N không đủ. Cần nhiều cấu hình k/N ở cửa main, không chỉ ở `_doc_che_do`/`_phan_manh`.

HƯỚNG 6: Gate M1 đầy đủ, miền cấu hình và gom trên dữ liệu sai
  giả thuyết : Survivor là lỗ phép kiểm; không được suy thành lỗi chức năng của head chưa đột biến.
  lệnh       : python evidence/env.py bash -c 'cd /tmp/review668-r7 && CONG_CU_TEST_BAN_KINH=manh python -u ops/cong_cu_test.py'; mode_domain.py; gom_current_data.py
  output     : Gate 56/56, bỏ qua=0, tiền kiểm bỏ qua=0; cổng cây thật ĐẠT; tự kiểm phân hạng/giàn giáo và N126 ĐẠT; giao 307 mutant, lỗi đột biến=0. Lưới 10.816 cặp k/N nhận 135, từ chối 10.681, 0 mismatch; thêm 11 dạng ASCII sai bị từ chối. Gom bộ đủ 307 bản ghi đạt lỗi=0; đích sống/bỏ qua/tín dụng giả/bán kính 2/lỗi đo đều lỗi=1 và đủ 307 hàng; sai tập ca/đích bị G-ban-ghi.
  kết luận   : KHÔNG PHẢI LỖI trên dữ liệu đã thử. Đây là gate M1 và bộ bản ghi fixture, không phải A1 tám mảnh thật hoặc CLI mặc định đo trọn 307 mutant.

HƯỚNG 7: MỚI — danh tính và thứ tự bảng gom bị nén thành số đếm
  giả thuyết : `bang_kq` chỉ đếm số ok/ĐỎ, nên đủ số dòng không chứng minh đủ tên hoặc đúng thứ tự DOT_BIEN.
  lệnh       : python evidence/env.py python -u evidence/gom_extra.py; python evidence/env.py python evidence/gom_wiring_r7.py
  output     : gom_reverse, gom_same_status_repeated và gom_details_drop đều sống 56/56. CLI thật với bộ đủ 307 bản ghi: control rc=0, 307 tên phân biệt đúng thứ tự; gom_reverse rc=0 nhưng thứ tự ngược; gom_same_status_repeated rc=0, 307 hàng ok nhưng CHỈ 1 tên phân biệt. Bộ 3 lỗi vẫn rc=1 ở cả control/mutant, nên không chứng minh gom xanh trên bộ sai.
  kết luận   : LỖI (P2), F19 nối lớp F16. Bản vá phán quyết/tổng lỗi có răng mới, nhưng hợp đồng bảng chưa được kiểm theo danh tính/thứ tự. Đối chứng bổ sung đặt tín dụng giả/bán kính 2: gom_details_drop làm mất cả 3 dòng lý do (control 3 → mutant 0); gộp cùng F19, không tách finding.

HƯỚNG 8: CLI thật cũng bỏ lọt việc đảo toàn bảng
  giả thuyết : Đường CLI mới kiểm số dòng và hai đầu ra tổng hợp, chưa kiểm việc chuyển nguyên bảng qua stdout.
  lệnh       : gom_extra.py (cli_reverse_table); gom_wiring_r7.py
  output     : cli_reverse_table sống 56/56. CLI control trên bộ đạt rc=0, 307 tên đúng thứ tự; đổi RIÊNG `_main_gop` để in ngược phần bảng vẫn rc=0, số dòng/đầu/cuối giữ nguyên nhưng thứ tự sai. Bộ 3 lỗi control/mutant đều rc=1.
  kết luận   : LỖI (P2), F20 nối lớp F8/F13/F17. F17 về rc khi >1 lỗi đã có phép thử; phần stdout của lớp CLI chưa đóng. F19 và F20 dùng chung quan sát `bang_kq`, nhưng hai chỗ gây sai độc lập (_gom_manh tạo bảng / _main_gop in bảng), cần đo cả hai.


Bảng kiểm độc lập: quyết định / dữ liệu của main (không lấy danh sách DOT_BIEN làm trần)

| Đơn vị main quyết định/truyền đi | Phép đổi đã đo đủ 56 CA ở r7 | Điểm quan sát cần có |
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


Bổ sung lượt 7: miền một lỗi (`writer_gt_one`, `final_db_gt_one`); N cố định (`shard_n_fixed_eight`, `partition_fixed_eight`); bảo toàn nguyên lý do (`reason_message_lost`); cộng qua nhiều nguồn (`scaffold_max`, `parallel_max`, `baseline_max`, `full_max`); số CA tổng hợp (`summary_ca_zero`); tên/lý do ở dây dọn mảnh (`cleanup_names_lost`, `cleanup_reason_lost`). Mọi cặp neo/thay lưu trong evidence/main-extra-mutations.json; 12/12 đã chạy đủ 56 CA, 8 sống và 4 bị t54 giết. Cặp neo/thay 68 + 19 cũ đã đối chiếu trùng với JSON lượt 6. Bảng kết quả từng phép đã chốt trong evidence/main-matrix.md sau khi các lượt dài kết thúc.

HƯỚNG 9: MỚI — bộ ghi mảnh chỉ được thử lỗi vận chuyển, thiếu lỗi kết quả đo
  giả thuyết : Phần ghi của t52 chỉ đưa bản ghi loại `loi` vào đường âm; không thử bản ghi loại `do` đúng cấu trúc nhưng đích sống, và lỗi chỉ ở bản ghi đầu.
  lệnh       : python evidence/env.py python -u evidence/writer_extra.py; python evidence/env.py python evidence/writer_wiring_r7.py
  output     : writer_only_transport_errors sống 56/56. Writer thật control với một đích sống trả lỗi=1, xoá tệp; mutant chỉ cộng lỗi khi loại bản ghi là `loi` trả lỗi=0, ghi tệp mang kết quả sai (đặt lỗi ở đầu hoặc cuối đều lọt). Gom nguyên bản đọc bộ ấy vẫn trả lỗi=1. writer_error_overwrite đã bị t52 giết; writer_first_record cũng sống 56/56: lỗi chỉ ở cuối ⇒ writer lỗi=0, vẫn ghi tệp; control lỗi=1, không tệp.
  kết luận   : LỖI (P2), F21 — lớp mới ở phía producer `_ket_thuc_manh`, không phải mở lại P1 workflow. Bản ghi sai được ghi ra nhưng lớp gom còn bắt; thiếu răng ở M2/M4 là lỗi độc lập với dây main và phán quyết phía gom.

Gợi ý cách vá (chỉ mô tả, không sửa mã sản phẩm):

- F18: sửa giàn giáo `_in_tu_kiem_main` và kỳ vọng t54. Giữ cả 0/1/>1; nhiều nguồn lỗi cùng lúc; nhiều cấu hình k/N; mỗi danh sách đầu ra có ít nhất hai dòng có nghĩa; quan sát nguyên lý do receiver, tên và giá trị truyền đi. Ca khoá phải giết `>1`, N=8 cố định, max thay cộng, cắt bảng/cổng/nền, đồng thời control xanh. Rủi ro: so đầu ra helper quá rộng sẽ giết oan mutant cũ; giới hạn ở hợp đồng main và đo lại bán kính 1/56.
- F19: sửa `bang_kq`/t52 để giữ chuỗi danh tính của từng hàng, đúng thứ tự DOT_BIEN và đúng kết quả từng vị trí. Đếm 307 dòng không chứng minh 307 mutant. Ca khoá phải giết đảo thứ tự và lặp cùng một hàng trong `_gom_manh`. Rủi ro: tự sinh kỳ vọng từ chính phần mã đang đột biến sẽ tái tạo điểm mù; không đổi bộ phân hạng chung chỉ để làm phép thử xanh.
- F20: ở đường CLI thật, đối chiếu bảng stdout có danh tính và thứ tự với hợp đồng gom, giữ cả bộ đạt và bộ sai. Ca khoá phải giết đảo bảng ở RIÊNG `_main_gop`. Có thể dùng chung bộ quan sát với F19, nhưng phải thử cả nguồn tạo bảng lẫn dây in qua CLI; một phép riêng không thay phép còn lại. Rủi ro: chuẩn hoá quá tay làm mất lỗi, hoặc kéo vân tay t53 vào t52 lần nữa.
- F21: mở các fixture ghi trong `_in_tu_kiem_gom`: loại `do` đúng schema nhưng sai kết quả (đích sống/tín dụng giả/bán kính >1), đặt đầu/giữa/cuối và nhiều lỗi; kiểm số lỗi, không tệp mới và xoá tệp cũ. Ca khoá phải giết writer chỉ cộng lỗi vận chuyển và writer chỉ xét bản ghi đầu. Rủi ro: phải đưa dữ liệu sai TRƯỚC lời gọi writer; sửa sau writer chỉ thử lại phía gom như F16.

HƯỚNG 10: Checklist main cũ — đầu ra nhiều dòng vẫn chưa được kích thích
  giả thuyết : So stdout nguyên văn không đủ khi các helper giả trả rỗng hoặc chỉ một dòng.
  lệnh       : main_new.py; main_wiring_r7.py; main_cross_sources.py; main_baseline_cross.py
  output     : full_line_first, writer_line_first, gate_print_drop và baseline_print_drop đã sống đủ 56/56. Wiring: cắt writer từ 44 xuống 5 dòng stdout; cắt vòng bán kính mất RADIUS-LAST; xoá vòng cổng mất GATE-FIRST/GATE-LAST. scaffold_max và parallel_max sống 56/56, ba nguồn lỗi thật thuộc miền 0/1 làm control báo 3, mutant báo 2. baseline_max sống 56/56; lỗi nền + ba helper làm control báo 4, mutant báo 3.
  kết luận   : LỖI (P2), cùng F18. F15 chưa đóng ngay trên checklist cũ; không phải chỉ do reviewer mở thêm phạm vi mới. Phép `final_gate_eq_one` sống nhưng tương đương trên miền helper cổng 0/1, không dùng làm finding.

Bổ sung HƯỚNG 6: `partition_roundtrip.py` chạy mọi N=2..16, dựng tệp theo thứ tự ngược và trộn thứ tự BKCON trong từng tệp. 15/15 phân hoạch rời nhau phủ 307 tên, gom lỗi=0 và trả bảng đúng thứ tự DOT_BIEN. Đây vẫn là fixture, không thay phép đo thật A1.

Bổ sung F18: main_reason.py dùng receiver/writer thật, con rc=0 nhưng stdout rỗng. Control giữ lý do thiếu các tên; mutant reason_message_lost chỉ còn `(rc=0)`. Cả hai vẫn rc=1; đây là mất chẩn đoán, không phải cổng xanh sai.

HƯỚNG 11: Chốt 87 phép main và 8 phép gom/CLI kế thừa
  giả thuyết : Đối chiếu lại TOÀN BỘ phép đổi lượt 5/6, không chỉ mutant executor chọn đưa vào DOT_BIEN.
  lệnh       : main_matrix.py (68); main_new.py (19); cli_new.py (4); gom_semantics.py (4); progress.py
  output     : 68/68 chạy đủ 56 CA: 65 bị giết, 3 sống (receiver_baseline, break_on_error, final_hong). 19/19 chạy đủ: 14 bị giết, 5 sống (final_gate_eq_one, full_line_first, writer_line_first, gate_print_drop, baseline_print_drop). 8/8 gom/CLI đều bị đúng t52 giết. Cặp neo/thay 68+19 trùng JSON lượt 6; JSON từng trạng thái và bảng từng phép tại evidence/main-matrix.md.
  kết luận   : LỖI (P2) ở bốn survivor đầu ra thuộc F18. F16/F17 vá THẬT các phép phán quyết/CLI cụ thể lượt 6, nhưng chưa đóng đầu ra theo F19/F20.

Bốn survivor không được coi là lỗi mới: receiver_baseline truyền tên không có trong CA, nên phép hiệu tập không đổi; final_hong được loi_nen bảo vệ; final_gate_eq_one tương đương vì helper thật chỉ trả 0/1; break_on_error xảy ra sau khi `_phong_con` đã phóng và đợi HẾT các con, vẫn giữ lỗi đầu/rc đỏ/không tệp, nên không có thay đổi nghiệm thu quan sát được. Không dựng miền helper giả ngoài hợp đồng để buộc chúng thành finding.

Trong lượt đo `main-new-failure_print_drop`, t54 chết đúng đích và t5 có thêm lỗi `cai_cong_cu.sh rc=141`. Giữ nguyên JSON gốc. `recheck_t5.py` chạy lại riêng t5 3 cặp control/mutant: 6/6 qua; phép đổi chỉ nằm trong thân main của TEP_TEST, không đổi mã t5/cài công cụ. Không dùng lỗi phụ này để chứng minh răng của main, và không khẳng định đã định danh nguyên nhân hệ điều hành của nó.

HƯỚNG 12: Toàn bộ 95 mutant chính thức mới trên đúng head
  giả thuyết : Các răng g668_*/f2_*…f17_* đều đúng đích, bán kính 1/56; bản vá f9 không giết lan t52.
  lệnh       : python evidence/env.py python -u evidence/radii.py new; python evidence/env.py python evidence/progress.py
  output     : TOTAL 95 ERRORS 0. 95/95 có đủ 56 trạng thái, chỉ ca đích giet_that và 55 ca khác qua; tổng 5.225 qua + 95 giet_that, không bo_qua/tin_dung_gia. f9_sha_hang và f9_head_hang chỉ giết t53. Nền có 212 mutant/53 CA; head có 307 mutant/56 CA.
  kết luận   : KHÔNG PHẢI LỖI hồi quy bán kính chính thức. Xác nhận răng từng mutant executor khai; không suy thành đóng lớp main/gom/CLI vì những survivor độc lập đã ghi ở trên.

HƯỚNG 13: Hồi quy mẫu cũ — giàn giáo CLI mới thiếu phụ thuộc trong cây mutant
  giả thuyết : F17 đưa thêm yêu cầu tệp vào t52 nhưng không cập nhật mọi khai báo phụ thuộc của mutant cũ.
  lệnh       : radii.py old; old_dependency_probe.py trên /tmp/review668-r7 và /tmp/review668-r7-prev (b6e05980); old_transport.py
  output     : Mẫu cũ 9/9 đã chạy đủ 56 CA, TOTAL 9 ERRORS 2. Hai bn_ban_kinh_giau_ly_do / bn_ban_kinh_gia_ve_som giết t29 đúng đích nhưng t52 thêm tin_dung_gia: FileNotFoundError tại dòng 7364, thiếu ops/cong_cu.py. Đối chiếu b6e05980: t52 qua trên cả hai mutant. Head hiện tại: t52 tin_dung_gia; chỉ thêm phụ thuộc thiếu vào bản sao fixture ⇒ t52 qua cả hai. Đường `_ban_kinh_moi_dot_bien` phóng hai con THẬT cũng trả TOTAL_ERRORS 2.
  kết luận   : LỖI (P1), F22 — hồi quy cổng bán kính, do bản vá F17. Đây là hồi quy khi head chạy chính bộ mutant cũ của kho, không chỉ là phép đổi do reviewer thêm; khác bốn P2 về chốt thiếu răng. Gate M1 xanh và 95 mutant mới 1/56 không phủ được lỗi này. Không có test mới giết thật thêm ở hai mutant này: trạng thái là tín dụng giả, vẫn làm phép đo bán kính ĐỎ.

Mẫu cũ 9 mutant: 482 qua + 9 giet_that + 2 tin_dung_gia + 11 bo_qua. Riêng t52/t53/t54: 25/27 qua, hai t52 tin_dung_gia. Danh sách khai báo TEP_TEST thiếu ops/cong_cu.py có đúng 5 tên: ba t31/t32 và hai bn nói trên; ba tên còn lại ĐÃ chạy đủ 56 ca qua old_extra_radii.py: mỗi tên giết đúng ca đích nhưng thêm t52 tin_dung_gia, lỗi bán kính=1. Cả 5 tên đều đã đo, nằm ở các mảnh 2, 3, 4, 4, 5 (k/8); do đó bốn phân hoạch chứa mutant gây hồi quy, không phải lời khai đã chạy trọn tám mảnh.

Gợi ý F22: sửa hợp đồng phụ thuộc khi dựng cây cho mọi mutant TEP_TEST cũ, hoặc thu gọn giàn giáo CLI để không yêu cầu tệp nó không sử dụng. Không lấy cong_cu.py từ cây ngoài đang đo để che thiếu fixture. Ca khoá phải chạy t52 trên cây của cả 5 mutant thiếu phụ thuộc và cả cổng bán kính/đường con, rồi đo lại 95 mới + mẫu cũ. Rủi ro: bù nguồn từ cây thật sẽ làm mutant mất cô lập, còn chỉ cập nhật `_KEM_TEP_TEST` có thể vẫn bỏ sót các tuple khai phụ thuộc thủ công.

Chốt mẫu cũ mở rộng: 3 mutant bổ sung có {'qua': 162, 'giet_that': 3, 'tin_dung_gia': 3}; cả ba thêm t52 tin_dung_gia. Cộng mẫu 9 thành 12 mutant cũ: 5 lỗi bán kính, 31/36 trạng thái t52/t53/t54 qua và 5/36 tin_dung_gia. Không có trạng thái mới bị bỏ qua trong ba ca t52/t53/t54.

Snapshot cuối: HEAD 2bb11df16f0b35d611e8650f384d3c5b421295e5; tree 78f9beafa77a3e807696309bc2959c77c25f6d83, khớp đầu. Cây ứng viên có status tracked/untracked/ignored rỗng, diff và index rỗng; hash cong_cu_test.py=907a2251277317ad69e882c3d7e5bb933f195aedf7aada4e3117d5da4917b8ff; SPEC giữ nguyên.

Giới hạn và nhận dạng phiên:

- Reviewer OpenAI Codex, họ GPT-6 theo cấu hình phiên; bề mặt API + terminal tools, transport machine/local. Không có phép xác minh độc lập exact model ID/effort thực sự phục vụ; không tự nhận human_audited hay quyền land.
- Linux, Python 3.11.15; actionlint 1.7.7 có shellcheck 0.9.0; bare lint dùng **python -m ruff 0.15.15** (binary `ruff` trên PATH là 0.15.8, không phải binary dùng cho phép delta). Chi tiết trong evidence/tool-versions.log.
- Không sửa, commit, push mã ứng viên; không chạy GitHub CI hay đăng ra ngoài. Mọi mutant, kho git fixture và harness nằm ngoài cay-kho. Sandbox thực tế workspace-write; checkout được đối xử read-only theo vai trò, không khai rằng filesystem tự cưỡng chế read-only.
- Bản sao đo head/base có marker ignored `.claude/.packet_state/session-start.ran` do test tạo; checkout ứng viên được giao vẫn sạch. Snapshot tracked/untracked/ignored đầu/cuối của checkout ứng viên, HEAD/tree, diff/index được đối chiếu; snapshot không chứng minh mọi thao tác trong toàn lịch sử. Không nhận các số lịch sử của executor làm phép đo của mình.
- **Not run:** A1 tám mảnh thật với đủ 307 mutant trên head này; CLI mặc định chạy trọn 307; Windows/Actions runner, upload/download thật, ruleset, A9. Gate M1 đầy đủ, 95 mutant mới và mẫu 9 mutant cũ là các phạm vi độc lập; không đổi tên chúng thành A1/A5 hay full CI. Không suy mẫu 9 thành toàn bộ 212 mutant cũ.
- Harness được tái dùng từ checklist reviewer lượt 6, nhưng mọi trạng thái r7 được chạy lại. Các script cùng lượt dùng JSON đã hoàn tất làm checkpoint, không dùng JSON lượt cũ làm kết quả. Một bản nháp wiring dùng sai namespace từ runpy đã bị dừng (rc=130) trước khi ghi kết luận; sửa namespace và chạy lại đối chứng. Bộ phân tích tên hàng cũng đã sửa để tách tên khỏi ký hiệu mũi tên; log cuối có control đúng thứ tự. Không tính lỗi harness là răng của bản vá.
- Ma trận là tập biến đổi hữu hạn trên mọi đơn vị quyết định/truyền dữ liệu liệt kê ở bảng kiểm, không phải chứng minh toán học mọi chương trình đột biến. Các hướng mới gồm hồi quy hợp đồng phụ thuộc của CLI fixture, cấu hình N khác 8 qua main, miền một lỗi sau thay đổi giàn giáo, danh tính/thứ tự/chi tiết bảng gom–CLI và lỗi kết quả đo phía writer.

Bảng lớp finding — giữ khóa và lịch sử, không reset lớp tái diễn:

| Slug lớp | Nguồn / chuỗi finding | Trạng thái lượt 7, mức còn mở | Cách vá chung / phép kiểm đóng |
|---|---|---|---|
| g5-main-thieu-ca-chon-vong-ban-kinh | F2@c8f52b6 → F5@c454ee9 → F6@2b501ef → F7@971e14c → F12@ef01112 → F15@b6e0598 → F18@2bb11df | Chưa đóng, P2 | Giàn giáo main phải quan sát miền 0/1/>1, nhiều cấu hình, nhiều nguồn lỗi, danh sách nhiều dòng và lý do nguyên; giết các survivor có hậu quả của 87+12 phép |
| g5-gom-cli-thieu-rang | F8@971e14c → F13@ef01112 → F17@b6e0598 → F20@2bb11df | Chưa đóng, P2 | CLI dương/âm thật đã có; mở quan sát stdout theo danh tính/thứ tự. Đột biến ở riêng `_main_gop` phải chết |
| g5-gom-phan-quyet-thieu-rang | F16@b6e0598 → F19@2bb11df | Chưa đóng, P2 | Bộ sai đúng schema nay có răng; thêm quan sát từng hàng và chi tiết. Đảo/lặp/cắt bảng tại `_gom_manh` phải chết |
| g5-manh-phan-quyet-thieu-rang | F21@2bb11df — mới | Chưa đóng, P2 | Đưa lỗi kết quả loại `do` vào writer, ở nhiều vị trí; đòi không để tệp. Đây là phía producer độc lập, không chuyển F16 ra khỏi lớp cũ |
| g5-cli-gian-giao-thieu-phu-thuoc | F22@2bb11df, do bản vá F17 | Chưa đóng, P1 | Bảo toàn hợp đồng cây mutant cũ khi CLI fixture thêm tệp; t52 không được chết vì thiếu fixture, đường con/bán kính phải trở lại đạt |
| g5-shell-bo-qua-thuc-thi | F1@c8f52b6 → F3@c454ee9 → F10@971e14c → F14@ef01112 | Đóng trong phạm vi đo | 60 ca cũ chặn đúng; ablation chứng minh hàng rào toàn thân run và Bash còn răng; chưa có phản chứng mới |
| g5-nguon-van-tay-thieu-rang | F9@971e14c | Đóng trong phạm vi đo | Hai f9_* giết riêng t53, không lan t52; phép bytes/HEAD/no-Git còn chạy |
| g5-chu-thich-dem-cu | F11@971e14c | Đóng | t152 và số AL_VER/chú thích 5 đồng bộ |

Có **8 lớp: 5 mở, 3 đóng trong phạm vi review; 5 finding mới: F22 P1 và F18–F21 P2, 0 P3 mới**. F19/F20 có thể cùng được vá bằng bộ quan sát bảng dùng chung, nhưng vẫn cần hai phép kiểm độc lập ở nơi tạo bảng và nơi in CLI. F21 cần fixture đi vào writer trước khi ghi; sửa fixture sau ghi của F16 không đo được cơ chế này. Không tách/gộp hay đổi tên các lớp lịch sử để xoá lần tái diễn.

| F<n> | mức | tệp:dòng | mô tả | phản chứng |
|---|---|---|---|---|
| F18 | P2 | ops/cong_cu_test.py:6609, :7397, :7431, :7440, :7448, :7452 | Lớp main chưa đóng: lỗi đúng một bị bỏ khỏi miền thử; N chỉ được thử 8; helper giả rỗng/một dòng; chưa cộng lỗi giữa nhiều nguồn hoặc giữ nguyên lý do. Còn survivor từ checklist cũ. | main-extra-writer_gt_one.json, main-extra-final_db_gt_one.json, main-extra-shard_n_fixed_eight.json; main-new-full_line_first.json, main-new-writer_line_first.json, main-new-gate_print_drop.json, main-new-baseline_print_drop.json. Mỗi phép 56/56 qua. main-wiring-r7.log: rc 1→0 khi một lỗi; 1/3 đo 102→39 tên; mất bảng/chẩn đoán. |
| F19 | P2 | ops/cong_cu_test.py:6571, :7208, :7276 | T52 nén bảng gom thành số ok/ĐỎ; không giữ danh tính, thứ tự hoặc chi tiết. Đủ số dòng vẫn có thể chỉ nói về một mutant. | gom-extra-gom_reverse.json / gom-extra-gom_same_status_repeated.json / gom-extra-gom_details_drop.json: 56/56 qua. gom-wiring-r7.log: 307 hàng ok, chỉ 1 tên; hoặc đảo thứ tự; hoặc mất 3 dòng lý do. |
| F20 | P2 | ops/cong_cu_test.py:6577, :7222, :7378 | CLI thật đã thử rc 0/1 trên bộ nhiều lỗi nhưng kiểm stdout bằng số đếm; đảo toàn bảng ở riêng `_main_gop` vẫn qua. | gom-extra-cli_reverse_table.json: 56/56 qua. gom-wire-cli_reverse_table-False.log và gom-wiring-r7.log: rc=0/307 tên nhưng ngược DOT_BIEN; control đúng thứ tự. |
| F21 | P2 | ops/cong_cu_test.py:7115, :7129, :7388 | Phía ghi trong t52 chỉ thử bản ghi loại `loi` ở đầu; chưa thử loại `do` đúng cấu trúc nhưng sai kết quả và lỗi ở cuối. | writer-extra-writer_only_transport_errors.json / writer-extra-writer_first_record.json: 56/56 qua. writer-wiring-r7.log: writer lỗi=0 và ghi tệp sai; control lỗi=1, không tệp. Gom nguyên bản vẫn bắt ⇒ P2, không P1. |
| F22 | P1 | ops/cong_cu_test.py:7363; khai báo phụ thuộc :572, :579, :585, :685, :690 | Giàn giáo CLI mới trong t52 đòi cong_cu.py nhưng 5 mutant TEP_TEST cũ khai phụ thuộc thủ công không mang tệp đó. Cổng bán kính bị hồi quy. | radius-bn_ban_kinh_giau_ly_do.json / radius-bn_ban_kinh_gia_ve_som.json: t29 giet_that + t52 tin_dung_gia, lỗi bán kính=1 mỗi tên; old-transport.log TOTAL_ERRORS 2. old-dependency-prev/head.log: b6e t52 qua → head lỗi → bù dependency trên bản sao qua. old-extra-radii.log xác nhận thêm cả 3 t31/t32, tổng 5 mutant hồi quy. |

ĐỐI CHIẾU LƯỢT TRƯỚC — F1–F17, không có F4:

| Finding | Trạng thái | Đối chiếu độc lập / lý do |
|---|---|---|
| F1 | đóng — ĐÃ VÁ THẬT trong phạm vi đo | 20/20 ca; gỡ thực thi+Bash làm 18 lọt, hai ca còn lại được chốt workflow độc lập giữ |
| F2 | chưa đóng lớp — VÁ HỜ ở cấp lớp | Chọn du/gate/manh đã có răng; main còn F18 |
| F3 | đóng — ĐÃ VÁ THẬT | 28/28 ca; trả splitlines + gỡ hàng rào toàn thân làm 27 lọt |
| F5 | chưa đóng lớp — VÁ HỜ ở cấp lớp | Dây receiver/writer cũ bị bắt; miền một lỗi và đầu ra writer còn F18 |
| F6 | chưa đóng lớp — VÁ HỜ ở cấp lớp | Giá trị/vân tay/worker đã có răng; miền cấu hình và chẩn đoán main còn F18 |
| F7 | chưa đóng lớp — VÁ HỜ ở cấp lớp | Ma trận main cũ đã đo đủ; các vòng in nhiều dòng vẫn sống |
| F8 | chưa đóng lớp — VÁ HỜ ở cấp lớp | Helper và CLI có răng; bảng stdout còn F20 |
| F9 | đóng — ĐÃ VÁ THẬT | f9_sha_hang và f9_head_hang đều đúng 1/56, chỉ t53; không còn bán kính 2 do t52 |
| F10 | đóng — ĐÃ VÁ THẬT | 7/7 bị chặn, gỡ chốt làm 7/7 lọt |
| F11 | đóng — ĐÃ VÁ THẬT | t152 PASS cả head/base; head đòi 5 và chú thích cùng 5 |
| F12 | chưa đóng lớp; danh tính CA đã vá thật | Lặp/bỏ/đảo CA bị bắt; cắt nội dung từng kết quả và đầu ra cổng/nền còn F18 |
| F13 | đóng biểu hiện dispatcher; lớp CLI chưa đóng | Bỏ dispatcher bị t52 bắt; cửa CLI thật còn thiếu quan sát bảng theo F20 |
| F14 | đóng — ĐÃ VÁ THẬT | 5/5 ca shell vắng đỏ đúng, gỡ chốt mới làm 5/5 lọt |
| F15 | chưa đóng — VÁ HỜ ở cấp lớp | Các phép ==1/tập nhiều tên/số liệu đã bị bắt, nhưng 4 survivor đầu ra của chính checklist lượt 6 còn sống; thêm miền một lỗi, N=8 cố định và cộng nhiều nguồn ở F18 |
| F16 | chưa đóng lớp; phần phán quyết ĐÃ VÁ THẬT | Bộ đúng cấu trúc sai kết quả và các phép bỏ/cắt/gán đè kết luận cũ đều bị t52 bắt; bảng bị lặp/đảo/mất chi tiết vẫn lọt (F19) |
| F17 | chưa đóng — VÁ SINH LỖI MỚI | Phần rc >1 có răng thật, bảng còn F20; giàn giáo CLI mới gây hồi quy mutant cũ do thiếu cong_cu.py (F22 P1) |

Các răng mới là thật; “VÁ HỜ ở cấp lớp” không có nghĩa mọi bản vá riêng vô hiệu. Ngưỡng packet là 0 P1/P2/P3; còn một P1 và bốn P2 nên yêu cầu sửa. Lớp main tiếp tục tái diễn; verdict không tự cấp quyền mở vòng sửa/review tiếp hay land, quyền quyết định thuộc chủ kho/điều phối.

verdict: changes_requested
reviewed_sha: 2bb11df16f0b35d611e8650f384d3c5b421295e5
