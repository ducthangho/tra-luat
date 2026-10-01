# Cross-review độc lập — packet #668 r1 g1 — lượt 10

verdict: changes_requested
reviewed_sha: 0acd3a943e6ffc3fb0bfc88f98e757a978549d3a

Mọi đột biến thực hiện trên bản sao trong /tmp. Không sửa mã sản phẩm. Các ca ký tự đặc biệt chỉ được chạy từ bộ có sẵn.

HƯỚNG 1: Neo vật liệu và môi trường
  giả thuyết : Head, spec, write set khớp nhiệm vụ.
  lệnh       : git -C cay-kho rev-parse HEAD HEAD^{tree}; git -C cay-kho status --short; sha256sum SPEC.md; git -C cay-kho diff f8a7829 --numstat
  output     : HEAD 0acd3a943e6ffc3fb0bfc88f98e757a978549d3a; tree 061dbc3ba25e62e89c51c0329707126d21f38d7e; status rỗng; SPEC dd2ada1b8511bec1c6c30ffdd7a94a3c34f4024836761878caf73ce339516b15; 5 tệp +1505/-49.
  kết luận   : KHÔNG PHẢI LỖI. Trần ~1600 và quyền lượt 10 theo chỉ thị người dùng. Bản sao /tmp/review668-r10; baseline /tmp/review668-r10-base.

Reviewer: OpenAI Codex, họ GPT-6 theo cấu hình phiên; terminal qua API, transport machine/local. Exact model ID/effort không có phép đo độc lập. Không cấp human_audited hoặc quyền land. Môi trường fixture ghim core.abbrev=7, commit.gpgsign=false; bytecode tắt (evidence/env.py). Chỉ tái dùng script lượt trước, mọi kết quả bên dưới đo mới.

HƯỚNG 2: Workflow F1/F3/F10/F14 — chạy ca có sẵn, tháo chốt
  giả thuyết : Lớp workflow đã đóng vẫn chặn phản chứng và có răng.
  lệnh       : python evidence/env.py python -u evidence/workflow.py; python evidence/env.py python evidence/workflow_ablation_extra.py
  output     : Control chặn F1=20/20, F3=28/28, F10=7/7, F14=5/5. Bỏ F10: 7/7 F10 lọt. Chỉ splitlines: 0 F3 lọt; splitlines + bỏ F10: 27/28 F3 lọt. Bỏ execution guard: 13/20 F1 và 7/7 F10 lọt. Bỏ F14: 5/5 F14 lọt.
  kết luận   : KHÔNG PHẢI LỖI trong phạm vi đo. Hai hàng rào che chồng nhau, nên splitlines đơn lẻ sống không chứng minh lớp mất răng. Không tự dựng payload ký tự điều khiển/ẩn hoặc lệnh giấu trong chú thích.

HƯỚNG 3: Hồi quy nhanh và delta baseline
  giả thuyết : Registry, t152, ca lease lân cận, actionlint và Ruff F không hồi quy.
  lệnh       : python evidence/env.py python -u evidence/regression.py; python .claude/dev/ci_dang_ky_test.py trên hai bản sao (qua evidence/env.py)
  output     : Head registry 1025/1025, TỔNG: ĐẠT. t152 và t24/t31/t35/t161/t162 của lease: head/base rc=0. Actionlint head/base rc=0. Probe G5 head/base rc=0. Ruff head/base cùng 6 F841, cùng tệp/message, delta=0.
  kết luận   : KHÔNG PHẢI LỖI. Đây là registry tự kiểm, không phải --chay mọi suite của kho; Ruff nền không phải 0 tuyệt đối.

HƯỚNG 4: Miền chế độ và gom dữ liệu sai trên head nguyên bản
  giả thuyết : Không có đường xanh trên bộ sai do grammar, kiểu, phân hoạch hoặc kết quả đo.
  lệnh       : evidence/env.py + mode_domain.py, gom_current_data.py, partition_roundtrip.py, schema_io.py, cli_mode_collision.py
  output     : Lưới 10.816 cặp k/N: nhận 135, từ chối 10.681; thêm 11 dạng ASCII sai; mismatch=[]. Gom valid 332 dòng/lỗi=0; survives, target_skipped, false_credit, wide_radius, measurement_error: mỗi bộ lỗi=1; unknown_case/wrong_target bị G-ban-ghi. N=2..16 đều phủ 332 tên rời nhau, bảng đúng thứ tự dù đảo tên tệp và trộn thứ tự bản ghi. CLI tên thư mục trùng cửa: rc=1/G-rong, cửa sau --gop: rc=2/G-doi-so, không chạy tự kiểm.
  kết luận   : KHÔNG PHẢI LỖI trên các bộ đã đo. Bản ghi ở đây là fixture tổng hợp, không phải A1 hoặc 332 phép đo thật.

HƯỚNG 5: MỚI — dispatcher không đối số có thực sự gọi main và giữ rc?
  giả thuyết : t54 gọi main trực tiếp qua cửa tự kiểm nên có thể không đo dây cuối __main__ mà CI dùng.
  lệnh       : python evidence/env.py python -u evidence/extra_r10.py; python evidence/env.py python evidence/extra_wiring.py
  output     : entry_drop và entry_rc đều sống: 56 trạng thái qua, không bỏ qua/tín dụng giả. CLI không đối số với CONG_CU_TEST_BAN_KINH=hong: control rc=2/[C-ban-kinh]; entry_drop rc=0/stdout rỗng; entry_rc rc=0 nhưng stdout vẫn báo cấu hình ĐỎ.
  kết luận   : LỖI (P2), F26. Thay duy nhất `sys.exit(main())` bằng `sys.exit(0)` hoặc `main(); sys.exit(0)` không ca nào bắt. Chốt dispatcher --gop đã đo, chốt default vẫn không có răng. Không gọi đây là head nguyên bản bỏ main hoặc P1 CI xanh: job upload còn bắt thiếu artifact khi bỏ main hoàn toàn.

HƯỚNG 6: MỚI — giá trị 0 của chỉ số mảnh qua dây main → phân hoạch → bộ ghi
  giả thuyết : Giàn giáo main chỉ thử k=3,5,1, nên truthiness fallback ở k=0 không được phân biệt.
  lệnh       : extra_r10.py (shard_zero); python evidence/env.py python evidence/shard_zero_wiring.py
  output     : Wiring dùng bộ nhận/bộ ghi/gom THẬT, chỉ giả CA và dữ liệu transport: control main rc=0, artifact có, GOM MẢNH 8/8 lỗi=0; `_phan_manh(k or 1,n)` ở main: main rc=0, artifact có, gom lỗi=1/G-ban-ghi: mảnh 0 chứa t2_go_canary ngoài nhóm.
  kết luận   : KHÔNG ĐO ĐƯỢC kết luận răng lúc ghi khối này: đột biến 56 CA đang chạy. Gom nguyên bản vẫn chặn nên không phải P1. Sẽ chốt bên dưới.

HƯỚNG 7: Main — giữ lỗi đã có khi vào nhánh đủ
  giả thuyết : Các nguồn tự kiểm lỗi chỉ được bật trong gate; reset loi_db ngay đầu else có thể thoát phép đo dù loop cộng lỗi tự nó đúng.
  lệnh       : extra_r10.py (full_clear); python evidence/env.py python evidence/extra_wiring.py
  output     : Wiring tự kiểm phân hạng lỗi=1, mọi kết quả bán kính lành: control rc=1/lỗi đột biến=1; thêm `loi_db=0` ngay đầu nhánh đủ ⇒ rc=0/lỗi đột biến=0.
  kết luận   : KHÔNG ĐO ĐƯỢC kết luận răng lúc ghi khối này: đột biến 56 CA đang chạy. Phản chứng wiring là phép cô lập bằng helper giả, không phải gate thật.

  Chốt HƯỚNG 6: shard_zero sống đủ 56/56 qua, không bỏ qua/tín dụng giả (evidence/extra-r10-shard_zero.json). Kết luận: LỖI (P2), F27, lớp main chưa đóng ở miền k=0. Main trả thành công và ghi mảnh sai; gom sau đó bắt được.
  Chốt HƯỚNG 7: full_clear bị t54 giết đúng, 55 ca khác qua. Kết luận: KHÔNG PHẢI LỖI; kịch bản du có nền đỏ đã quan sát tổng lỗi và bắt reset. Wiring chứng minh hậu quả của mutant, nhưng không chứng minh thiếu răng.

HƯỚNG 8: Gate trọn M1 và tự kiểm bán kính
  giả thuyết : Gate vẫn chạy đủ CA, cổng cây thật, tự kiểm phân hạng/giàn giáo/song song; không đo bán kính trong chế độ giao mảnh.
  lệnh       : python evidence/env.py bash -c 'cd /tmp/review668-r10 && CONG_CU_TEST_BAN_KINH=manh python ops/cong_cu_test.py'
  output     : rc=0; cong_cu_test: 56/56 đạt; tổng=56, bỏ qua=0, tiền kiểm bỏ qua=0; CỔNG TRÊN CÂY THẬT: ĐẠT; TỰ KIỂM SONG SONG (N126): ĐẠT; 332 đột biến GIAO mảnh; SỐ LIỆU lỗi đột biến=0.
  kết luận   : KHÔNG PHẢI LỖI. Không gọi gate M1 là CLI mặc định đo trọn bán kính.

HƯỚNG 9: F24 và ranh giới I/O bộ ghi
  giả thuyết : Kiểu từng trường header và loại tệp được canh riêng; hỏng I/O không để lại artifact xanh giả.
  lệnh       : python evidence/env.py python -u evidence/schema_io.py; new_mutations.py
  output     : phien_ban/manh/so_manh qua 6 kiểu mỗi trường: control từ chối mọi dạng sai đã thử; gỡ từng kiểm kiểu đều bị t52 giết. Symlink trỏ mảnh hợp lệ: control G-tep, gỡ is_symlink nhận GOM MẢNH 3/3, mutant bị t52 giết. Header cắt dở G-dau. Writer gặp symlink cũ: xoá link, target KEEP còn nguyên; đường ra directory ném IsADirectoryError; OSError tại write: tệp cũ không còn.
  kết luận   : KHÔNG PHẢI LỖI trong phạm vi đo. Symlink được nền này hỗ trợ. F24 ĐÃ VÁ THẬT. Không gọi ngoại lệ I/O fail-closed là xanh.

HƯỚNG 10: Main — đường ra và số worker là dữ liệu, không phải hằng của giàn giáo
  giả thuyết : Tất cả kịch bản t54 dùng ra='x' và cùng cấu hình worker; thay tham số bằng hằng đó có thể sống.
  lệnh       : python evidence/env.py python -u evidence/main_inputs.py; python evidence/env.py python evidence/main_inputs_wiring.py
  output     : fixed_path và fixed_workers đều sống 56/56 qua. receiver_known_baseline và config_message đều bị đúng t54 giết. Wiring mảnh với bộ ghi/bộ nhận thật: control ghi requested.txt, không x; mutant `ra="x"` rc=0, không requested.txt, có x. Wiring đủ với CONG_CU_TEST_TIEN_TRINH=3: control truyền 3 tới vòng bán kính; mutant truyền 2, cùng rc=0.
  kết luận   : LỖI (P2), cùng F27: miền tham số trong giàn giáo main chưa đủ phân biệt chuyển tiếp với hằng. Worker là thiếu răng phụ thuộc cấu hình phép đo (env=2); không khẳng định nó sống nếu chạy suite với env=3. Đường ra cố định và k=0 không có caveat đó.

Gợi ý F26 (dispatcher default): vá phép đo tại t54/cửa CLI thật của cong_cu_test.py, vì đường thiếu quan sát nằm SAU helper main. Một lệnh CLI không đối số với env cấu hình sai phải trả đúng rc=2 và thông điệp cấu hình; nó rẻ, không cần chạy đệ quy cả suite. Khoá bằng hai mutant entry_drop và entry_rc (phải chết đúng một ca), kèm đối chứng CLI không đối số đi vào main. Tránh dựng fixture phụ thuộc cong_cu.py nếu cửa import không cần nó; nguy cơ lặp F22 hoặc giết oan t52 phải được đo trên cả năm cây mutant cũ.

Gợi ý F27 (miền đầu vào main): vá giàn giáo _in_tu_kiem_main và kỳ vọng t54, không đổi thuật toán sản phẩm đang đúng. Bổ sung k=0, ít nhất hai đường ra khác nhau (một đường có thư mục con/khoảng trắng bình thường), và ít nhất hai giá trị worker; kiểm tham số giao cho từng helper từ dữ liệu của kịch bản thay vì một hằng chung. shard_zero/fixed_path/fixed_workers phải chết đúng t54, chạy lại toàn ma trận và mẫu cũ. Rủi ro: dùng chung chính biểu thức sai để tạo cả kỳ vọng lẫn thực tế sẽ tiếp tục cho xanh; thay env phải phục hồi, không làm rò sang kịch bản hoặc ca sau.

  Bổ sung HƯỚNG 10: worker_domain.py đo riêng t54 trên chính mutant fixed_workers: worker=1/3/4 ⇒ giet_that; worker=2 ⇒ qua. Đây là thiếu biến thiên trong cấu hình giàn giáo, không phải mutant bất tử trên mọi máy.

HƯỚNG 11: Bán kính hồi quy — mẫu có chủ đích thay vòng 332
  giả thuyết : Bản vá mới không làm lệch bán kính, đặc biệt không giết oan ba ca mới trên mutant cũ.
  lệnh       : python evidence/env.py python -u evidence/radii.py all (dừng sau phần đã hoàn tất); python evidence/env.py python -u evidence/radius_sample.py
  output     : Inventory baseline 212 mutant/53 CA; head 332/56; không mất mutant cũ, thêm 120. Mẫu chốt 110 tên (69 mới + 41 cũ), liệt kê trong sample-names.json. Chọn tất cả mutant mới có đích ngoài t54; tất cả f23_/f24_/f25_/f26_; tất cả mutant cũ TEP_TEST; 12 mutant đầu nền; t21; đại diện f2/f5/f6/f7/f12/f15/f18. Các JSON đã hoàn tất trong lượt 332 ban đầu được giữ, không tính lại hai lần.
  kết luận   : KHÔNG ĐO ĐƯỢC trọn 332 trong lượt này. Phần còn lại của mẫu đang chạy, số cuối sẽ chốt bên dưới. Lựa chọn mẫu theo quyền người dùng cho phép; tốc độ ban đầu ~116–123 giây/mutant với nhiều phép đo đồng thời. Không nhận lời khai 332/332 của executor làm kết quả độc lập.

Ghi rõ: `f26_*` là tên bốn mutant do executor bổ sung từ script dở dang lượt 9; **F26 trong verdict này** là finding mới về dispatcher default, không đồng nhất với tên mutant ấy.

HƯỚNG 12: F22 — cây tạm thiếu phụ thuộc của cả năm mutant cũ
  giả thuyết : Bản vá fixture không còn đòi cong_cu.py ở các cây TEP_TEST cũ.
  lệnh       : radius_sample.py; đọc radius-t31_tien_kiem_nuot_moi_loi.json, radius-t32_bo_nhan_dong_ho_nhay.json, radius-t32_noi_ra_moi_timeout.json, radius-bn_ban_kinh_giau_ly_do.json, radius-bn_ban_kinh_gia_ve_som.json
  output     : 5/5 mutant đủ 56 trạng thái, errors=0; t52/t53/t54 đều qua (15/15), không tín dụng giả.
  kết luận   : KHÔNG PHẢI LỖI. F22 ĐÃ VÁ THẬT trong đúng tập năm mutant từng gây hồi quy, không dựa riêng vào một mẫu tên thuận lợi.

HƯỚNG 13: Main — phân biệt lỗi nền với lỗi tự kiểm ở nhánh đủ
  giả thuyết : Reset toàn bộ về 0 bị ca nền đỏ bắt, nhưng reset về loi_nen giữ nguyên nền và xoá lỗi phân hạng/giàn giáo/song song chỉ ở du có thể lọt.
  lệnh       : python evidence/env.py python -u evidence/main_seed.py; python evidence/env.py python evidence/seed_wiring.py
  output     : Chèn `loi_db = loi_nen` ngay đầu else đo đủ: full_seed sống 56/56 qua. Wiring giữ 56 CA giả lành, tự kiểm phân hạng trả 1, mọi kết quả bán kính lành: control rc=1/lỗi đột biến=1; mutant rc=0/lỗi đột biến=0.
  kết luận   : LỖI (P2), cùng F27: miền kịch bản main chưa có lỗi tự kiểm ở nhánh đủ. Đây là biến thể phân biệt được với full_clear đã bị giết ở HƯỚNG 7; không dùng kết quả của mutant chết để suy mutant này cũng chết. Chưa chứng minh head nguyên bản xoá lỗi.

Bổ sung gợi ý F27: thêm kịch bản du có lỗi phân hạng/giàn giáo/song song và có lỗi nền xen kẽ kết quả bán kính. Quan sát tổng lỗi/rc theo nguồn độc lập, không chỉ đặt lỗi tự kiểm ở gate. full_seed phải chết đúng t54. Rủi ro: chỉ thêm một tổng lỗi mà các nguồn luôn cùng giá trị vẫn không phân biệt việc bỏ/gán đè từng nguồn.

HƯỚNG 14: Phân biệt nhiễu t5 với hồi quy packet
  giả thuyết : Một bán kính 2/56 trong mẫu có thể do lỗi gián đoạn ở ca cũ, không phải chốt mới kéo thêm ca.
  lệnh       : retry_radius.py g668_che_do_rong_la_vang; recheck_noise.py; noise_sources.py (đều qua env.py khi chạy test)
  output     : Lần đầu mutant giết đúng t53 nhưng thêm t5: cai_cong_cu.sh rc=141, không stdout/stderr. Đo lại NGUYÊN 56 CA trên cùng mutant: errors=0, đúng t53, 55 qua. t5 lặp baseline 8/8 qua, head 8/8 qua. AST t5 và bytes cai_cong_cu.sh/cai_actionlint.sh/cong_cu.py/bash_nen.py/lease_publish_test.py giống baseline.
  kết luận   : KHÔNG PHẢI LỖI packet được chứng minh. rc=141 gợi ý SIGPIPE ở pipeline installer nhưng chưa truy vết syscall để khẳng định nguyên nhân. Giữ nguyên radius-g668_che_do_rong_la_vang.json có lỗi và retry-g668_che_do_rong_la_vang.json đạt; không ghi đè log, không khai cả vòng đầu sạch. Số cuối sẽ tách trước/sau đo lại.

HƯỚNG 15: Rà mọi trường đầu ra và tham số dọn mảnh của main
  giả thuyết : Checklist không được chỉ đo lời gọi mà quên các trường chính main in ra hoặc đường dọn mảnh riêng.
  lệnh       : python evidence/env.py python -u evidence/field_probes.py
  output     : 13/13 bị t54 giết: cleanup_k/n; header_k/n/count/total/workers; full_total; gate_total; summary_total/precheck; exception_type; case_total.
  kết luận   : KHÔNG PHẢI LỖI ở 13 trường này. Đây là phép đo t54 mục tiêu, không khai là 13 vòng đủ 56 CA. Chúng bổ sung 138 vòng đầy đủ; cặp neo/thay và trạng thái ở field-probes.json, inventory lời gọi AST ở main-calls.json.

HƯỚNG 16: Chốt TOÀN BỘ ma trận main lượt 5–8 và phép đổi mới
  giả thuyết : Các bản vá riêng không được coi là đóng lớp nếu dây hoặc miền chưa đo còn sống.
  lệnh       : checklists.py; new_mutations.py; main_skip.py; extra_r10.py; main_inputs.py; main_seed.py; final_summary.py (test chạy qua env.py)
  output     : 138/138 phép độc lập, mỗi phép đủ 56 trạng thái: 126 bị giết đúng ca đích, 12 sống. Toàn checklist main lượt 5–7: 99/99, 95 bị đúng t54 giết, bốn survivor an toàn: receiver_baseline, break_on_error, final_hong, final_gate_eq_one. 15 phép lượt 8 cũng chạy đủ (bao gồm hai skip). Chín phép mới: ba bị t54 giết, sáu sống thuộc F26/F27.
  kết luận   : LỖI (P2), F26/F27. Không có bỏ qua/tín dụng giả trong ma trận độc lập. Bốn survivor cũ không chứng minh xanh sai; hai survivor an toàn nữa ở lượt 8 là main_no_sorted_baseline và writer_drop_missing. Hai entrypoint và bốn miền kịch bản mới có hậu quả thật trong wiring/CLI. Toàn bảng từng phép ở evidence/mutation-matrix.md; không suy từ số lượng mutant chính thức sang đóng lớp.

HƯỚNG 17: Chốt lớp gom/CLI/bộ ghi theo checklist lượt 6–8
  giả thuyết : Bộ sai cấu trúc/kết quả, nhiều lỗi, mất danh tính bảng và dây CLI đã được đo đúng tầng.
  lệnh       : checklists.py (gom_semantics, cli_new, gom_extra, writer_extra); new_mutations.py; schema_io.py; cli_mode_collision.py
  output     : 15/15 phép gom/CLI/writer kế thừa đều bị đúng t52 giết, 825 trạng thái qua + 15 giet_that. Gỡ phán quyết, bỏ/gán đè tổng lỗi, chỉ bản ghi đầu, mất/đảo/lặp/cắt bảng, CLI ==1/cắt stdout và writer chỉ tính lỗi transport đều chết. Kiểu từng header/symlink và đảo bảng writer cũng có răng. Dispatcher --gop nhận đúng thư mục tên trùng cửa và từ chối cờ sau --gop.
  kết luận   : KHÔNG PHẢI LỖI ở các chốt gom/CLI --gop/bộ ghi đã đo; F16/F19/F20/F21/F24 đã vá thật trong phạm vi này. Lớp dispatcher rộng hơn vẫn mở do F26 ở đường không đối số, không đánh đồng nó với lỗi --gop cũ.

HƯỚNG 18: Chốt mẫu bán kính chính thức và bốn phép từ lượt 9
  giả thuyết : Những mutant đã đăng ký phải giết riêng ca đích, không tạo hồi quy quanh bản vá mới.
  lệnh       : radius_sample.py; retry_radius.py g668_che_do_rong_la_vang; final_summary.py
  output     : Mẫu đủ 110/110 tên, mỗi tên đủ 56 ca. 109 đạt ngay, một tên vướng t5 rc=141 rồi đo lại NGUYÊN 56 ca đạt. Kết quả đã kiểm lại: 110 giet_that đúng đích + 6039 qua + 11 bo_qua ngoài đích của mutant cũ; 0 tin_dung_gia, 0 lỗi bán kính. 41 mutant cũ: t52/t53/t54 qua 123/123. Đủ 12 mutant f23/f24/f25/f26: riêng đúng t52/t53/t54 theo khai báo; bốn f26_* đều chỉ giết t54.
  kết luận   : KHÔNG PHẢI LỖI hồi quy packet được chứng minh trong mẫu. Không gọi đây là 332/332 hoặc một vòng đầu sạch; log lỗi đầu và retry được giữ riêng. Các ca bỏ qua ngoài đích không được đổi thành qua.

Bảng kiểm độc lập: mọi quyết định/đầu ra có nghĩa của `main()` trên head này. Các phép đổi nằm trong `*-mutations.json`; bảng kết quả từng mutant sẽ nằm ở `mutation-matrix.md`. Đây là tập phép đổi hữu hạn, không phải chứng minh mọi chương trình sai đều bị bắt.

| Quyết định hoặc dữ liệu | Phép đổi / đối chứng |
|---|---|
| Đọc os.environ, chọn chế độ; ValueError dừng trước tiền kiểm/CA, rc=2, thông điệp | main_environment_empty, config_ignore, config_message |
| Gọi hai tiền kiểm đúng hàm/thứ tự; giữ từng tên/lý do, số lượng | batch_skip, alias_skip, precheck_first; f26_tk_ly_dau |
| Gọi đủ CA đúng danh tính/thứ tự và đếm qua | ca_skip, ca_duplicate_middle, ca_reverse, pass_counter |
| Phân biệt BoQuaMoiTruong/AssertionError/Exception; tên, lý do, loại ngoại lệ | skip_as_red, assert_ignore, exception_ignore, skip_counter; f26_bq_ly_ca_dau/f26_do_ly_ca_dau |
| In mọi ca bỏ qua/đỏ, mọi tiền kiểm; mẫu số trừ đúng số ca bỏ qua | skip_first_diagnostic, skip_boolean_count, precheck_first, f23_bq_* |
| Chọn nhánh mảnh; lấy k,N,ra từ cấu hình | shard_never, shard_k/n/ra, shard_n_fixed_eight, fixed_path |
| Phân hoạch theo k,N, bao gồm k=0 | partition, partition_fixed_eight, shard_zero |
| Nền đỏ HOẶC tiền kiểm bỏ qua: dọn tệp, truyền tên/k/N/ra/lý do/None/vân tay, rc=1 | base_red_ignore, precheck_ignore, no_cleanup, cleanup_fp/names_lost/reason_lost, main_cleanup_path, bad_base_rc |
| Thông báo mảnh: k/N, số tên, tổng DOT_BIEN, workers | so stdout nguyên trong t54, kết hợp các phép tham số và đầu ra |
| Phóng đúng tên, nền rỗng, worker; chỉ phóng khi có tên | launch_names/baseline/workers; nhánh tên rỗng không đạt được với 332 mutant và N≤16 |
| Nhận đủ nhóm, giữ rc/stdout/nhóm/nền; gọi bộ nhận thật | receiver_group/rc/output/baseline/skip_call, receiver_known_baseline; f26_con_sau_rc0 |
| Giữ nguyên lý do hỏng đầu, rc và đuôi stdout; không đè mất lỗi qua nhóm lành | no_reason, reason_message_lost, main_no_error_tail/rc, main_initial_error_ignored, break_on_error |
| Hợp nhất mọi tên và nguyên giá trị kết quả | drop_group, drop_values |
| Gọi bộ ghi, truyền đúng k/N/ra/tên/ket hoặc None/lý do/vân tay | writer_skip, writer_k/n/ra/names/ket/reason/fp |
| In mọi dòng writer và quy lỗi 0/1/>1 thành rc | print_writer_drop, writer_line_first, writer_rc/eq_one/gt_one/negative_error |
| Nhánh đủ/gate: cổng cây thật tại GOC, giữ rc, in mọi dòng | gate_skip/root/print_drop, final_gate, summary_gate_pass |
| Tự kiểm phân hạng/giàn giáo, đúng thứ tự và tích luỹ lỗi | classifier_skip, scaffold_skip/reset/max |
| Tập đủ tên nền đỏ, sắp xếp, truyền báo cáo, in mọi dòng, cộng lỗi nền | baseline_empty/report_arg/errors/reset/max/first/print_drop, main_no_sorted_baseline |
| Workers nhánh đủ, tự kiểm song song nhận đúng nền và giữ lỗi trước | full_workers, fixed_workers, parallel_skip/arg/reset/max |
| Gate chỉ in thông báo giao mảnh; đủ đo toàn bộ tên/nền/worker | gate_run_full, gate_notice_drop, full_names/base/workers |
| Đủ: tiêu thụ mọi kết quả, mọi dòng, cộng từng lỗi và giữ lỗi có trước | full_errors/reset/first_only/repeat_result/max/line_first, print_full_drop, full_clear, full_seed |
| SỐ LIỆU: số CA, số mutant, chế độ, tổng lỗi, số tiền kiểm, cổng | summary_ca_zero/errors_zero/gate_pass, main_gate_summary_mode, các phép cộng và đếm |
| Rc đủ/gate là OR của hong/loi_db/tien_kiem_bo_qua/loi_cong | final_hong/db/precheck/gate, final_db_eq_one/gt_one, final_gate_eq_one |
| Dây CLI default thật vào main và truyền mã thoát | entry_drop, entry_rc — ngoài thân main, nhưng là cửa workflow chạy |

Không gán mutant tương đương thành finding: baseline receiver chứa tên ngoài CA không đổi tập thực; hong được lỗi nền bảo vệ; bỏ sort ở main được helper tự sắp xếp; nhánh nhóm rỗng không phát sinh trong miền cấu hình hiện tại. `break_on_error` làm mất thu thập sau lỗi và phải xem nhật ký t54, không tự suy thành CI xanh. Bộ ghi bỏ lỗi thiếu bản ghi còn KeyError fail-closed; xem survivor-equivalence.log.

Bảng lớp finding (phạm vi packet, không phải bảo đảm mọi đột biến tưởng tượng):

| Lớp | Chuỗi finding | Trạng thái cuối lượt 10 |
|---|---|---|
| Workflow: thực thi, tách dòng, nội suy, shell | F1/F3/F10/F14 | Đóng trong phạm vi đã đo; ca cũ và tháo hàng rào đều có răng |
| main: chọn nhánh, chuyển dữ liệu, tổng hợp và miền kịch bản | F2/F5/F6/F7/F12/F15/F18/F23 → F27 | Chưa đóng; k=0 và đường ra hằng còn sống; worker hằng sống ở cấu hình đo 2; mất lỗi tự kiểm ở du còn sống |
| CLI gom và dispatcher | F8/F13/F17/F20/F25 → F26 | Nhánh --gop đã vá có răng; lớp dispatcher chưa đóng ở cửa default không đối số |
| Nguồn vân tay | F9 | Đóng trong phạm vi đo |
| Bộ gom: cấu trúc và kiểu/loại tệp | F24 | Đóng trong phạm vi đo; từng trường header và symlink hợp lệ đã bị đo riêng |
| Bộ gom: kết luận và bảng | F16/F19 | Đóng trong phạm vi đo; bộ đúng cấu trúc nhưng kết quả sai bị từ chối |
| Bộ ghi mảnh | F21 | Đóng trong phạm vi đo; lỗi kết quả, lỗi muộn, xóa artifact cũ và đầu ra được đo |
| Phụ thuộc fixture mutant cũ | F22 | Đóng trên toàn bộ các tên cũ bị F22 ảnh hưởng trong mẫu; không lan sang t52/t53/t54 |
| Chú thích số AL_VER | F11 | Đóng; t152 và actionlint hai vế đạt |

| F<n> | mức | tệp:dòng | mô tả | phản chứng |
|---|---|---|---|---|
| F26 | P2 | ops/cong_cu_test.py:7924; t54 :6691 | Default dispatcher gọi main và trả rc chưa có răng; tự kiểm main đi qua cửa riêng, CLI t52 chỉ đo --gop/đối số lạ | entry_drop và entry_rc: mỗi mutant 56/56 qua; CLI env hỏng control rc=2 → mutant rc=0 (stdout rỗng hoặc vẫn báo ĐỎ). extra-r10-entry_*.json, extra-wiring.log |
| F27 | P2 | ops/cong_cu_test.py:7624, :7628, :7760, :7761, :7797, :7802; t54 :6704 | Giàn giáo main chưa biến thiên đủ tham số: không k=0, mọi ra='x', một cấu hình worker; không lỗi tự kiểm ở nhánh đủ. Truyền hằng hoặc xoá riêng lỗi tự kiểm vẫn xanh | shard_zero/fixed_path/fixed_workers/full_seed: mỗi mutant 56/56 qua; main ghi sai mảnh/đường dẫn hoặc dùng 2 worker khi yêu cầu 3; full_seed làm mất lỗi tự kiểm (rc 1→0). Gom thật bắt mảnh sai nên không nâng P1. shard-zero-wiring.log, main-inputs-wiring.log, worker-domain.log, seed-wiring.log |

ĐỐI CHIẾU LƯỢT TRƯỚC: lượt 9 bị cắt, không có verdict/findings hoàn chỉnh. Đối chiếu F23–F25 từ lượt 8 và bốn ý định đo lượt 9: **ĐÃ VÁ THẬT** cho các phản chứng được gọi tên (đa ca bỏ qua/lý do nguyên, kiểu từng trường/symlink, vị trí cờ, lý do riêng từng ca/tiền kiểm và nhóm con lỗi muộn). Các f23/f24/f25/f26 được đo độc lập trong mẫu chính thức; bản vá ấy không đóng thay miền kịch bản F27 hoặc default dispatcher F26.

| Finding cũ | trạng thái | Lý do / đối chiếu |
|---|---|---|
| F1 | đóng | 20 fixture, execution guard có răng; cùng lớp F3/F10/F14 |
| F2 | chưa đóng lớp | Chọn chế độ đã vá thật; miền kịch bản main còn F27 |
| F3 | đóng | 28 fixture; tháo F10 + đổi splitlines mở 27 đường cũ |
| F5 | chưa đóng lớp | Nhận/ghi/truyền lỗi có răng; lớp main còn F27 |
| F6 | chưa đóng lớp | Giá trị, vân tay, tiền kiểm đã có răng; biến thiên đầu vào còn F27 |
| F7 | chưa đóng lớp | Checklist cũ được chạy lại; lớp main còn F27 |
| F8 | chưa đóng lớp CLI | Helper --gop đã có răng; default dispatcher còn F26 |
| F9 | đóng | Kiểm nguồn hash/HEAD, mutant riêng trong mẫu đúng đích |
| F10 | đóng | 7 fixture bị chặn; gỡ guard mở 7/7 |
| F11 | đóng | t152 xác nhận 5 AL_VER; delta baseline không lỗi |
| F12 | chưa đóng lớp | Danh tính ca/nhiều kết quả/stdout đã được bắt; main còn F27 |
| F13 | chưa đóng lớp dispatcher | --gop thật có răng; cửa default còn F26 |
| F14 | đóng | 5 fixture shell, gỡ chốt mở cả 5 |
| F15 | chưa đóng lớp | Miền lỗi 0/1/>1 và đầu ra đã đo; miền kịch bản còn F27 |
| F16 | đóng | Bỏ kết luận/cộng lỗi/cắt vòng trên bộ đúng cấu trúc sai kết quả bị bắt |
| F17 | chưa đóng lớp CLI | Rc và stdout --gop đã vá thật; default dispatcher còn F26; không tái sinh F22 |
| F18 | chưa đóng lớp | N≠8 và lỗi nhiều nguồn/nhiều dòng đã có răng; k=0/ra/worker còn F27 |
| F19 | đóng | Bảng đủ danh tính/thứ tự/chi tiết, mutant riêng bị bắt |
| F20 | chưa đóng lớp CLI | Đảo bảng ở _main_gop bị t52 bắt; F26 nằm ở nhánh default khác |
| F21 | đóng | Bộ ghi đo kết quả sai đúng cấu trúc và lỗi cuối, mutant bị bắt |
| F22 | đóng trong mẫu | Đủ năm mutant cũ từng thiếu dependency, không ca mới bị giết oan |
| F23 | chưa đóng lớp main | Phản chứng đa skip/lý do và bốn biến thể lượt 9 đã vá thật; main còn F27 |
| F24 | đóng | Kiểu riêng từng header/symlink hợp lệ đều có răng |
| F25 | chưa đóng lớp dispatcher | Sai vị trí cờ/đối số lạ đã vá thật; cửa default còn F26 |

Giới hạn và kết luận:

- Ngưỡng áp dụng là 0 P1/P2/P3. Có **2 P2 mới (F26, F27), 0 P1/P3 mới được chứng minh**. Main và dispatcher chưa đóng; workflow giữ trạng thái đóng trong phạm vi đã đo. Không thấy gom nguyên bản xanh trên các bộ sai đã thử.
- Toàn bộ checklist kế thừa 114 + 15 phép lượt 8 + 9 phép mới = 138, đã chạy đủ 56 CA cho từng phép. Mẫu hồi quy 110/332 có chủ đích, không nhận lời khai 332/332 của executor. Bảng dữ liệu đầu/cuối và phép đo lại nằm trong evidence/summary.json.
- Chưa đo A1 tám CLI mảnh thật rồi gom trên head này; chưa chạy CLI mặc định toàn bộ bán kính từ đầu tới cuối; chưa đo Windows, Actions upload/download thật, ruleset hoặc thời gian runner A9. Fixture gom 332 bản ghi là dữ liệu tổng hợp, không phải 332 phép đo thật.
- Không có biến thể ký tự ẩn/điều khiển mới đủ căn cứ để báo bằng lời; chỉ chạy fixture có sẵn. Không GitHub CI, commit/push, sửa sản phẩm hay đăng verdict ra ngoài.
- Linux, Python 3.11.15, actionlint 1.7.7, Ruff 0.15.15. Git fixture ghim signing=false/abbrev=7. Nhiễu t5 đã được tách khỏi kết luận packet, không xoá bằng chứng lỗi đầu.
- Snapshot cuối: head/tree không đổi (0acd3a943e6ffc3fb0bfc88f98e757a978549d3a / 061dbc3ba25e62e89c51c0329707126d21f38d7e), status tracked/untracked/ignored của cay-kho rỗng; SPEC giữ đúng hash được giao. Mọi kết quả gắn head này; không cấp human_audited hoặc quyền land.

verdict: changes_requested
reviewed_sha: 0acd3a943e6ffc3fb0bfc88f98e757a978549d3a
