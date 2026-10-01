# Cross-review độc lập packet #668 — lượt 12

verdict: changes_requested
reviewed_sha: 0b22f55d36f2090db9900328354ec821f6128727

Mọi phép đột biến được thực hiện trên bản sao trong `/tmp`; không sửa mã sản phẩm trong `cay-kho/`.

HƯỚNG 1: Neo vật liệu và môi trường
  giả thuyết : đúng SHA, SPEC, phạm vi và trần được chủ kho nâng.
  lệnh       : git -C cay-kho rev-parse HEAD HEAD^{tree}; sha256sum SPEC.md; python evidence/snapshot.py initial
  output     : HEAD=0b22f55d36f2090db9900328354ec821f6128727; tree=b41597a3de2babd1a740179023c7c2c31b60259e; SPEC=dd2ada1b8511bec1c6c30ffdd7a94a3c34f4024836761878caf73ce339516b15; snapshot 2350 tệp, status gồm ignored rỗng; 5 tệp +1577/-49.
  kết luận   : KHÔNG PHẢI LỖI. Áp trần ~1600 và quyền review tại chỗ theo chỉ thị lượt này. Không thực hiện ghi/land theo executor lease.

Môi trường: OpenAI Codex, công cụ shell trực tiếp của phiên API này, transport machine; không có receipt độc lập chứng nhận model/effort thực tế hay human audit. Không gọi CI/GitHub, push, đăng comment, land. Origin của clone được giao là mirror cục bộ `/home/user/tra-luat`, không shallow, detached; baseline là ancestor của head. Không xác minh remote GitHub trực tiếp hoặc đổi origin. Bản sao head `/tmp/review668-r12`, baseline `/tmp/review668-r12-base`; runner cũ được chép vào `evidence/` và đổi đường r11/r10 thành r12 (các thích nghi khác được ghi bên dưới). Kết quả JSON cũ đã xoá trước phép đo, chỉ giữ bảng mutations làm checklist. Dùng `evidence/env.py` để đặt bytecode-off, signing=false, abbrev=7. Snapshot kiểm nội dung ngoài `.git`, HEAD/tree/status; giới hạn là hai mốc, không chứng minh lịch sử giữa hai mốc.

HƯỚNG 2: Workflow F1/F3/F10/F14, chạy các ca có sẵn và gỡ chốt
  giả thuyết : lớp đã đóng vẫn chặn phản chứng, các chốt thật sự có răng.
  lệnh       : python evidence/env.py python evidence/workflow.py; python evidence/env.py python evidence/workflow_ablation_extra.py
  output     : control chặn F1 20/20, F3 28/28, F10 7/7, F14 5/5. Gỡ F10: 7 F10 lọt. Chỉ đổi splitlines: không lọt. Gỡ F10 kèm splitlines: 27 F3 và 7 F10 lọt. Gỡ execution: 13 F1 lọt; gỡ shell: 5 F14 lọt; gỡ cả execution + shell: 18 F1, 7 F10, 5 F14 lọt.
  kết luận   : KHÔNG PHẢI LỖI trong miền control đã đo; splitlines đơn lẻ được chốt F10 bảo vệ chồng. Không tự dựng chuỗi điều khiển/ẩn.

HƯỚNG 3: ĐỐI CHIẾU LƯỢT TRƯỚC — F28, miền CLI hợp lệ
  giả thuyết : bản vá phải giết đủ ba phản chứng lượt 11, đúng t54, giữ 55 ca còn lại xanh.
  lệnh       : python evidence/env.py python -u evidence/novel_entry.py; python evidence/env.py python evidence/entry_valid.py
  output     : entry_requires_config, entry_gate_shortcut, entry_full_rc đều bị t54 giết thật, 1/56. Thông điệp t54 lần lượt chỉ rõ không gọi main ở du, không gọi main ở gate, và nuốt mã 1/2 ở du. JSON evidence/novel-entry_*.json ghi từng trạng thái.
  kết luận   : KHÔNG PHẢI LỖI — F28 ĐÃ VÁ THẬT. Phép đo dùng chính ba cặp neo/thay cũ trên head mới, không nhận kết quả executor.

  Bổ sung: patch_radius.py đo 15 mutation chính thức thuộc f7_cau_hinh_nuot, f13, f25, f27, f28: 15/15 lỗi=0, đúng 1/56 theo đích khai báo. Bốn f28_* đều chỉ giết t54; f13/f25 chỉ giết t52. Kết quả riêng được đóng băng tại evidence/patch-radius/ để vòng bán kính khác không ghi đè bằng chứng này.

HƯỚNG 4: Hồi quy gate và kiểm tra hai vế
  giả thuyết : gate giữ toàn bộ công việc trước bán kính, các công cụ chung không thêm lỗi.
  lệnh       : python evidence/env.py python -u evidence/run_regression.py
  output     : gate rc=0, 227.0s, ca=56, lỗi đột biến=0, tiền kiểm bỏ qua=0, cổng cây thật=ĐẠT, thông báo GIAO 343 đột biến. Registry head 1025/1025, baseline 938/938, cả hai rc=0/TỔNG ĐẠT. t152 và lease t24/t31/t35/t161/t162 rc=0 hai vế. actionlint riêng ci.yml rc=0 hai vế; toàn workflow rc=1 hai vế, output giống hệt (SC1003 ở ops-don-ref.yml:117). Ruff F rc=1 hai vế, cùng 6 F841 theo tệp/mã/message, delta=0. Probe cong_cu.py kiem-tra --json rc=0 hai vế. Python 3.11.15; actionlint 1.7.7; Ruff 0.15.15.
  kết luận   : KHÔNG PHẢI LỖI hồi quy ở các kiểm tra trên. Bare Ruff và actionlint toàn kho vẫn đỏ nền; không gọi là xanh tuyệt đối. Workflow dùng Python 3.12; nền cục bộ này là 3.11.15.

HƯỚNG 5: Miền cấu hình, phân hoạch và dữ liệu sai kết quả
  giả thuyết : gom chặn dữ liệu đúng cấu trúc nhưng sai kết quả; tên tệp và thứ tự bản ghi không thay danh tính phép đo.
  lệnh       : mode_domain.py; partition_roundtrip.py; gom_current_data.py; novel_files.py; cli_mode_collision.py; cli_collision_workflow.py (qua evidence/env.py)
  output     : lưới 10816 cặp nhận 135, từ chối 10681, thêm 11 hình dạng sai, mismatch=[]. N=2..16: phủ 343, rời nhau, gom_errors=0, đúng thứ tự bảng. Bộ lành 343 ok; các bộ đích sống/bỏ qua/tín dụng giả/bán kính rộng/lỗi đo đều bị từ chối. CLI trùng tên cửa được giữ là đối số thư mục; workflow thêm cờ bị validator từ chối.
  kết luận   : KHÔNG PHẢI LỖI trong miền đo. Đây là dữ liệu tổng hợp kiểm consumer, không phải A1 hay bán kính thật.

HƯỚNG 6 (MỚI): Phân biệt biến vắng với biến rỗng khi phối hợp cấu hình
  giả thuyết : bảng t53 chỉ có gate rỗng đứng riêng, thiếu các ô rỗng ở nhánh mảnh/ra lẻ, nên đổi kiểm hiện diện sang truthiness có thể sống.
  lệnh       : python evidence/env.py python -u evidence/measure.py evidence/r12-mutations.json; phép đối chứng lưu evidence/mode-empty-probe.json
  output     : mode_empty_both, mode_empty_orphan, mode_empty_shard đều sống đủ 56/56. Đối chứng: control báo C-ca-hai với BK rỗng + MANH=0/8 + RA=x, mutant nhận manh; control C-ra-le với RA rỗng đứng riêng, mutant nhận du; control C-hinh-dang với MANH rỗng đứng riêng, mutant nhận du.
  kết luận   : LỖI (P2), F29 — thiếu răng miền hiện diện/rỗng, M4 yêu cầu mỗi chốt M1/M2 có tự kiểm. Head nguyên bản từ chối đúng; lỗi nằm ở tự kiểm không phát hiện chốt bị gỡ. Không quy thành P1 của head chưa đột biến.

  Bổ sung: lưới hiện diện 27 ô (mỗi BK/MANH/RA là vắng, rỗng, hợp lệ): control 27/27 đúng, nhận đúng 3 ô. mode_empty_both nhận sai 1 ô; mode_empty_orphan và mode_empty_shard nhận sai 2 ô mỗi phép, gồm đường rơi về gate khi BK=manh. evidence/mode-presence-grid.json. Hướng sửa: đo bảng này qua cửa t53/TEP_TEST, xác nhận từ chối trước CA, giữ bán kính từng mutant đúng t53 và không giết oan t54.

HƯỚNG 7 (MỚI): Tín hiệu thất bại và định dạng đầu ra của nguồn HEAD
  giả thuyết : t53 chỉ đổi nội dung tệp/commit và kho không git, chưa tách mã thoát Git khỏi stdout có hình dạng hợp lệ.
  lệnh       : measure.py với fingerprint_rc/fingerprint_format trong r12-mutations.json; đối chứng evidence/fingerprint-probe.json và fingerprint-consumer.json
  output     : fingerprint_rc và fingerprint_format đều sống đủ 56/56. Đối chứng control trả head=None khi Git rc=1/stdout=40 ký tự hex, hoặc rc=0/stdout=not-a-head. Hai mutant nhận các giá trị này; bộ ghi tổng hợp trả [0,0], gom GOM MẢNH 2/2, 343 đột biến, lỗi=0.
  kết luận   : LỖI (P2), F30 nối F9 — nguồn HEAD thiếu răng ở hai chốt trạng thái/định dạng. Head nguyên bản từ chối đúng. Bản ghi tổng hợp chỉ chứng minh consumer tin vân tay sai nếu chốt nguồn bị gỡ, không phải bán kính thật hoặc một đường lọt của head nguyên bản.

  Bổ sung: lưới rc=0/1/2 × stdout hợp lệ 40/64 hex, rỗng, sai định dạng: control 12/12 đúng; bỏ kiểm rc chỉ 8/12 đúng; bỏ kiểm định dạng 11/12 đúng. evidence/fingerprint-grid.json. Hướng sửa: phép tự kiểm nguồn vân tay cần tách trạng thái tiến trình và stdout, gồm hai chiều nhận đúng/từ chối đúng; đối chứng đi qua chính bản TEP_TEST đột biến. Không dùng riêng kho không git để chứng minh cả hai chốt, vì stdout không hợp lệ và rc khác 0 cùng có mặt che lẫn nhau.

HƯỚNG 8: Bán kính đầy đủ và nhiễu t5
  giả thuyết : mọi đột biến chính thức giết đúng ca đích, không lan sang t52/t53/t54.
  lệnh       : radii.py all; sample_run.py; freeze_radius.py (qua evidence/env.py)
  output     : chốt mẫu lớn 249/343 tên, mỗi tên đủ 56 trạng thái, gồm 169 cũ + 80 mới. Mẫu chọn trước 121 tên đã hoàn tất sạch: mọi tên mới đích ngoài t54, toàn bộ f23/f24/f25/f26/f27/f28/f13, mọi mutant cũ TEP_TEST, 12 tên đầu nền, t21 và đại diện f2/f5/f6/f7/f12/f15/f18; thêm 128 tên đã hoàn tất từ vòng quét đầu. 248/249 đạt ngay; t30_go_fail_close_bo_giai thêm t5 rc=141 ở lần đầu, chạy lại nguyên 56 ca đạt đúng 1/56. Sau retry: 249 giet_that đúng đích + 13682 qua + 13 bo_qua ngoài đích, 0 tin_dung_gia, 0 lỗi bán kính. Trên 169 mutant cũ, t52/t53/t54 qua 507/507.
  kết luận   : KHÔNG PHẢI LỖI hồi quy packet được chứng minh trong mẫu chốt. KHÔNG ĐO ĐƯỢC trọn 343 tại thời điểm đóng băng; không ngoại suy 94 tên còn lại. Dùng quyền chọn mẫu lớn của nhiệm vụ: vòng đầy đủ chưa xong sau hơn 35 phút cùng checklist, nên kết luận chỉ neo bộ bất biến evidence/audited-radius/selection.json. Kết quả phát sinh thêm từ vòng quét không thuộc verdict này. SIGPIPE đã được chủ kho tách packet; không sửa installer hoặc làm tròn lỗi đầu thành xanh.

  Đối chứng nhiễu: retry_radius.py t30_go_fail_close_bo_giai chạy lại nguyên 56 ca, errors=0, đúng t30 1/56. recheck_noise.py: t5 baseline 8/8 và head 8/8 qua. noise_sources.py: AST t5 cùng bytes cai_cong_cu.sh, cai_actionlint.sh, cong_cu.py, bash_nen.py, lease_publish_test.py giống baseline. Không xóa kết quả thô hoặc tính lần đầu là sạch.

  Gặp lại cùng triệu chứng ở checklist main-new/baseline_print_drop: t54 giết đúng, thêm t5 rc=141. Bản đầu được giữ tại evidence/raw-first/main-new-baseline_print_drop.json; chạy lại nguyên 56 ca chỉ t54 bị giết (retry-main-baseline-print.log). Không sửa installer.

HƯỚNG 9: Hai phép đổi phân hoạch lượt 11
  giả thuyết : dịch modulo và đảo nguồn là mutant có hậu quả thật hay chỉ đổi nhãn mảnh?
  lệnh       : python evidence/env.py python evidence/partition_identity.py; partition_roundtrip.py
  output     : partition_rotation và partition_reverse_source đều 56/56 qua. Đo thêm producer/consumer cùng phép đổi trên N=2..16: control 15/15, rotation 15/15, reverse 15/15; mỗi bộ count=unique=343, phủ đủ, gom_errors=0, ok_rows=343 (evidence/partition-variants.json).
  kết luận   : KHÔNG PHẢI LỖI bán kính bị bỏ đo hoặc gom xanh sai. Hai phía cùng thay thuật toán vẫn đo mỗi tên đúng một lần. Không khẳng định dữ liệu sinh bởi hai phiên bản khác nhau có thể trộn: vân tay test khác và gom từ chối. Công thức i % N của SPEC là lựa chọn cố định trong code hiện tại; các phép đổi này không chứng minh chốt an toàn thiếu.

HƯỚNG 10: Kiểm kê thân main và toàn checklist cũ
  giả thuyết : F2…F27 phải được kiểm theo mọi quyết định/tham số/đầu ra, không chỉ các tên executor bổ sung.
  lệnh       : run_checklists.py; fields_full.py; novel_entry.py; patch_radius.py; các runner wiring cũ; danh sách độc lập tại evidence/main-inventory.md
  output     : TOÀN BỘ 138/138 phép checklist lượt 5–10 đã chạy lại qua đủ 56 ca: 132 bị đúng ca đích giết, 6 survivor an toàn cũ. Thêm 17/17 phép trường lượt 11 và 3/3 entry đều bị đúng t54 giết; 2 phép phân hoạch sống tương đương. Bảy phép mới: 5 sống có hệ quả thuộc F29/F30, 1 sống tương đương, 1 bị t54 giết. Tổng 167/167 phép, 153 giết đúng đích + 14 sống; không bỏ qua/tín dụng giả trong ma trận cuối. Một lần đầu nhiễu t5 được giữ riêng và retry như HƯỚNG 8.
  kết luận   : KHÔNG PHẢI LỖI mới của dây nối main/dispatcher trong miền đã kiểm kê. Sáu survivor cũ: receiver_baseline chứa tên ngoài CA nên không đổi nền; break_on_error vẫn trả đỏ sau lỗi đầu và không ghi mảnh; final_hong được lỗi nền bảo vệ; final_gate_eq_one tương đương miền 0/1 của cổng; main_no_sorted_baseline được helper sắp xếp; writer_drop_missing vẫn KeyError và không có file. main_receiver_baseline_hong mới tương đương vì nhánh này chỉ tới khi hong rỗng. Các helper chế độ/vân tay vẫn mở bởi F29/F30, không dùng kết luận wiring để đóng thay chúng.

  Thích nghi runner cũ: extra_r10.py dừng ở assertion neo entry_drop không còn duy nhất vì bảng F28 mới chứa cùng đoạn chữ. Đã thêm LF cuối vào neo/thay để nhắm đúng dòng dispatcher thực thi (như runner novel_entry đã làm), rồi chạy lại; không đổi ý nghĩa phép đột biến. Các nhóm độc lập được chạy sớm song song; cache chỉ dùng JSON 56 trạng thái do chính lượt này sinh trên head cố định, không dùng kết quả cũ.

HƯỚNG 11: Gom, CLI và bộ ghi — schema, danh tính, thứ tự và I/O
  giả thuyết : các chốt F16/F17/F19–F21/F24–F25 còn đo đúng tầng, không để file cũ tạo xanh giả.
  lệnh       : các nhóm gom_semantics/cli_new/gom_extra/writer_extra trong checklists.py; schema_io.py; schema_cli.py; gom_wiring_r7.py; writer_wiring_r7.py; survivor_equivalence.py
  output     : wiring gom/writer cũ rc=0. Một lượt wiring schema ban đầu chưa chạy vì thiếu bảng new-mutations.json/skip-mutations.json (bảng do runner trước sinh); đã dựng lại bảng từ head hiện tại và chạy lại, cả bốn runner rc=0. Schema: 18 giá trị sai kiểu trên ba trường đều bị control chặn; symlink G-tep; header cắt dở G-dau. Symlink output cũ bị xoá, target KEEP nguyên; directory ném IsADirectoryError; lỗi write ném OSError, file cũ không còn. Bỏ xử lý bản ghi thiếu trong writer vẫn KeyError, không có file, nên là fail-closed tương đương chứ không finding.
  kết luận   : KHÔNG PHẢI LỖI trong miền đo. 15/15 phép gom/CLI/writer kế thừa bị đúng t52 giết, 825 trạng thái qua + 15 giet_that. Các phép gỡ kiểu từng trường/symlink và đảo bảng writer trong new_mutations cũng bị t52 giết. F16/F17/F19/F20/F21/F24/F25 đã vá thật, F28 không làm hồi quy chúng. Phản chứng schema CLI là hậu quả của mutant, không phải head gốc lọt.

Bảng lớp finding — 10 lớp lịch sử, 2 lớp còn mở; mỗi finding mới thuộc đúng một lớp. Nguồn các lớp cũ giữ theo VERDICT lượt 1–10; F28 từ lượt 11/SHA e4b7bdb. Mọi phép kiểm đóng/mở trong bảng này đo trên head 0b22f55d36f2090db9900328354ec821f6128727.

| Slug lớp | Chuỗi finding | Mức còn mở / trạng thái | Phép kiểm đóng lớp hoặc hướng sửa chung |
|---|---|---|---|
| g5-shell-bo-qua-thuc-thi | F1/F3/F10/F14 | Đóng trong miền đo | 60 fixture và ablation toàn thân run/shell/execution; registry 1025/1025. |
| g5-main-thieu-ca-chon-vong-ban-kinh | F2/F5/F6/F7/F12/F15/F18/F23/F27 | Đóng trong miền wiring đã kiểm kê | Toàn checklist main cũ + 17 trường; k=0, đường ra, worker, nhiều nguồn lỗi, lý do và stdout đều có răng; survivor an toàn đã đối chứng. |
| g5-gom-cli-thieu-rang | F8/F13/F17/F20/F25/F26/F28 | Đóng trong miền đo | CLI gom dương/âm, đối số/dispatcher; ba mutant F28 cũ và 15 mutation chính thức lân cận đúng đích. |
| g5-nguon-van-tay-thieu-rang | F9 → F30 | P2 — mở lại ở rc/định dạng Git | F9 hash/HEAD hằng đã vá thật; bổ sung miền độc lập rc × stdout của nguồn HEAD, giết riêng hai mutant F30 bằng t53. |
| g5-gom-phan-quyet-thieu-rang | F16/F19 | Đóng trong miền đo | Bản ghi đúng schema/sai kết quả; bỏ/cắt/đảo bảng và phép cộng đều bị t52 bắt. |
| g5-manh-phan-quyet-thieu-rang | F21 | Đóng trong miền đo | Writer kiểm kết quả đầu/cuối/nhiều lỗi, giữ bảng và xoá output cũ; mutant đúng đích t52. |
| g5-cli-gian-giao-thieu-phu-thuoc | F22 | Đóng trong mẫu | Năm tên từng thiếu dependency đạt 5/5, ca mới 15/15 qua; toàn 169 mutant cũ ca mới 507/507 qua. |
| g5-gom-cau-truc-thieu-rang | F24 | Đóng trong miền đo | Kiểu từng trường/symlink và CLI đối chứng; gỡ chốt bị t52 bắt. |
| g5-chu-thich-dem-cu | F11 | Đóng | Diff hook chỉ đổi chú thích 4→5; t152 hai vế qua, 5 AL_VER khớp. |
| g5-che-do-hien-dien-rong-thieu-rang | F29 — mới | P2 — chưa đóng | Miền vắng/rỗng/hợp lệ của ba biến; đo bảng 27 ô qua TEP_TEST, giết ba phép truthiness riêng ở t53. Khác dây nối main: parser là nơi tự quyết định hợp lệ. |

Không đổi slug F9 khi mở miền mới thành F30; không gộp F29 vào main để xoá lịch sử của lớp wiring. Hai lớp cần fixture khác nhau (môi trường cấu hình và kết quả tiến trình Git), cùng phải giữ bán kính 1.

Bảng finding:

| F<n> | mức | tệp:dòng | mô tả | phản chứng |
|---|---|---|---|---|
| F29 | P2 | ops/cong_cu_test.py:6684, :7249, :7250, :7257, :7741 | Tự kiểm chế độ thiếu miền hiện diện/rỗng khi phối hợp biến. Ba phép đổi kiểm hiện diện thành truthiness sống dù nhận cấu hình phải từ chối. | `mode_empty_both`, `mode_empty_orphan`, `mode_empty_shard`: mỗi phép 56/56 qua. Lưới 27 ô: control đúng 27, mutant nhận sai 1/2/2 ô. Main với helper ghi lời gọi: control rc=2, chưa chạy gì; mutant đi vào tiền kiểm/CA. `r12-mutations.json`, `measure-mode_*.json`, `mode-presence-grid.json`, `main-empty-wiring.json`. |
| F30 | P2 | ops/cong_cu_test.py:6684, :7281, :7285, :7741 | Lớp nguồn vân tay F9 chưa đóng ở hai chốt rc Git/định dạng HEAD: kho không Git làm cả rc và stdout sai nên chưa tách được răng từng chốt. | `fingerprint_rc`, `fingerprint_format`: mỗi phép 56/56 qua. Lưới rc/stdout: control 12/12, mutant 8/12 và 11/12. Với vân tay lỗi được mutant nhận, writer/gom tổng hợp xanh 343 dòng; control trả head=None và chặn. `measure-fingerprint_*.json`, `fingerprint-grid.json`, `fingerprint-consumer.json`. |

Hai finding đều là thiếu răng tự kiểm; chưa có phản chứng P1 rằng head nguyên bản cho CI/gom xanh sai. Hướng sửa và ranh giới phép đo nằm ở HƯỚNG 6–7. Không cung cấp patch sản phẩm hoặc quyền land.

Bảng trạng thái F1–F28 (không có F4):

| F<n> | Trạng thái | Lý do / đối chiếu |
|---|---|---|
| F1 | đóng | Execution guard chặn fixture; gỡ chốt mở đúng nhóm. |
| F2 | đóng | Nhánh đủ/gate/mảnh có răng trong ma trận; không còn survivor có hậu quả của wiring. |
| F3 | đóng | 28 fixture bị chặn; ablation kép mở 27 đường cũ. |
| F5 | đóng | Truyền/nhận rc và kết quả con có răng. |
| F6 | đóng | Giá trị, vân tay trao writer, tiền kiểm và worker có răng; nguồn vân tay tách ở F30. |
| F7 | đóng | Checklist đầy đủ chạy lại; cấu hình lỗi và từng đường gọi main được quan sát. |
| F8 | đóng | Helper/CLI gom dương, âm và truyền mã đúng tầng. |
| F9 | chưa đóng | Biểu hiện cũ ĐÃ VÁ THẬT; lớp nguồn vân tay còn F30 ở rc/định dạng. |
| F10 | đóng | 7 fixture chặn; gỡ guard mở cả 7. |
| F11 | đóng | Chú thích 5 và t152 khớp. |
| F12 | đóng | Danh tính ca, nhiều kết quả, đầy đủ stdout được t54 kiểm. |
| F13 | đóng | Mutation dispatcher --gop giết riêng t52; cửa mặc định F28 cũng đã vá. |
| F14 | đóng | 5 fixture vắng shell bị chặn, gỡ chốt mở cả 5. |
| F15 | đóng | Giá trị lỗi 0/1/>1, nhiều ca/nhiều nguồn được đo. |
| F16 | đóng | Bộ đúng cấu trúc/sai kết quả không gom xanh. |
| F17 | đóng | CLI thật với nhiều lỗi, rc/stdout có răng; không tái sinh F22. |
| F18 | đóng | N khác 8, nhiều dòng/nhiều nguồn; miền k=0/ra/worker bổ sung cũng đạt. |
| F19 | đóng | Bảng nguyên văn, danh tính/thứ tự/chi tiết có răng. |
| F20 | đóng | Đảo/cắt bảng CLI bị t52 giết. |
| F21 | đóng | Writer kiểm đủ kết quả và lỗi muộn, không để file cũ. |
| F22 | đóng | Trong mẫu: năm mutant cũ đều đúng bán kính; 169 mutant cũ không giết oan ca mới. |
| F23 | đóng | Nhiều ca bỏ qua và lý do nguyên được bảo toàn/đo. |
| F24 | đóng | Kiểu từng trường, symlink và đường CLI đã đo hai chiều. |
| F25 | đóng | Chỉ chọn cửa từ argv[1]; tên thư mục trùng cờ không chiếm dispatcher. |
| F26 | đóng | Hai phép entry_drop/entry_rc cũ đều bị t54 giết trên head mới. |
| F27 | đóng | shard_zero/fixed_path/fixed_workers/full_seed bị giết; worker=1/2/3/4 đều bắt hằng 2. |
| F28 | đóng | ĐÃ VÁ THẬT: cả ba phản chứng lượt 11 giết đúng t54 1/56, thêm bốn f28_* chính thức cũng đúng đích. |

Giới hạn nghiệm thu: không chạy lại A1 đủ tám mảnh thật trên head này; roundtrip tổng hợp không thay A1 và không nhận A1 của e4b7bdb làm bằng chứng của 0b22f55. Không chạy CLI mặc định nguyên bản hết 343 mutation/A5, Windows, GitHub runner, upload/download thật hoặc latency A9. Gate M1 thật, ma trận và mẫu bán kính là ba phép đo riêng. Không gọi registry tự kiểm là `--chay` mọi suite của kho.

Kiểm cuối: SHA/tree vẫn 0b22f55d36f2090db9900328354ec821f6128727 / b41597a3de2babd1a740179023c7c2c31b60259e; snapshot 2350 tệp và status gồm ignored giống đầu lượt (`UNCHANGED`), diff worktree/index đều rỗng. Tệp bằng chứng kết luận: `evidence/mutation-matrix.md`, `evidence/review-summary.json`, `evidence/audited-radius/selection.json`, hai snapshot và các JSON/log liên kết. Không sửa mã sản phẩm.

Ngưỡng yêu cầu là 0 P1/P2/P3: còn 2 P2 (F29, F30), không có P1/P3 mới được chứng minh. Main/dispatcher và workflow đóng trong miền checklist; M4 chưa đạt ở hai lớp helper trên. Đây là verdict kỹ thuật, không tự cấp human_audited hoặc authority land.

verdict: changes_requested
reviewed_sha: 0b22f55d36f2090db9900328354ec821f6128727
