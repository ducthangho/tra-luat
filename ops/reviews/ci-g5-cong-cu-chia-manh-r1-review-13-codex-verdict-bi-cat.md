<!-- executor: luot 13 BI CAT boi bo loc noi dung (05:24Z) sau HUONG 9; khong co ket luan cuoi. Hai P2 da ghi: F31 (khoang trang gia tri gate), F32 (ngu phap HEAD: do dai / bang chu). Noi dung duoi la NGUYEN VAN. -->

verdict: dang_review
reviewed_sha: 19c0e3043357d7058727e92c90e4fb41e750be3e

Reviewer: Codex / OpenAI, công cụ shell trực tiếp trong sandbox workspace-write; không tự chứng nhận model/effort hay human_audited từ yêu cầu trong SPEC. Không gọi CI, đăng GitHub, commit hoặc sửa cây ứng viên. Chỉ thị lượt 13 cho phép review tiếp và trần ~1.600 dòng được dùng thay ngưỡng cũ trong SPEC/LEASE.

HƯỚNG 1: Neo hiện vật và phạm vi
  giả thuyết : vật liệu đúng exact head, SPEC và write set trước khi đo.
  lệnh       : git -C cay-kho rev-parse HEAD HEAD^{tree}; sha256sum SPEC.md; python evidence/snapshot.py initial; đọc diff-vong-13.patch, CLAUDE.md, AGENTS.md và protocol §8.
  output     : HEAD=19c0e3043357d7058727e92c90e4fb41e750be3e; tree=fbe99288f89c6fdb0ce113c06e92cb6e34848d76; SPEC=dd2ada1b8511bec1c6c30ffdd7a94a3c34f4024836761878caf73ce339516b15; 2350 tệp, status kể cả ignored rỗng. Diff +1602/-49 đúng 5 đường; lượt 13 chỉ đổi ops/cong_cu_test.py cho F29/F30.
  kết luận   : KHÔNG PHẢI LỖI. Chạm trần xấp xỉ chủ kho đã cấp, không tự coi ngưỡng cũ ~600 là blocker của review read-only này.

Phép đo đang chạy: runner kế thừa chép riêng vào evidence/, thay đường cây thành /tmp/review668-r13; không sao chép JSON kết quả cũ. Cây baseline /tmp/review668-r13-base được checkout exact f8a7829. Lượt bootstrap đầu gọi checkout trước khi copy xong báo rc=128; đã hoàn tất copy và checkout lại thành công. Regression khởi động sớm có thể đọc baseline trước checkout nên phải chạy lại trước kết luận, không dùng lần đó làm bằng chứng delta.

HƯỚNG 2: Workflow lịch sử và răng từng lớp bản vá
  giả thuyết : F1/F3/F10/F14 còn bị chặn; bỏ bản vá phải mở đúng fixture kế thừa.
  lệnh       : python evidence/env.py python evidence/workflow.py; workflow_ablation_extra.py.
  output     : control chặn 20 F1 + 28 F3 + 7 F10 + 5 F14. no_f10 mở 7/7 F10; splitlines đơn lẻ không mở ca vì guard toàn thân còn đứng; no_f10_splitlines mở 27/28 F3 và 7/7 F10. Bỏ execution guard mở 13/20 F1; bỏ đồng thời execution và shell mở 18/20 F1. Bỏ shell guard mở 5/5 F14. Log và JSON từng fixture ở evidence/workflow-*.
  kết luận   : KHÔNG PHẢI LỖI. Lớp workflow vẫn đóng trong miền kiểm. Không tự dựng payload điều khiển/ẩn mới; toàn bộ phản chứng loại đó lấy nguyên từ phan_chung của cây.

HƯỚNG 3: F29/F30 — đo lại phản chứng đã báo
  giả thuyết : năm mutant sống lượt 12 nay phải bị đúng t53 giết, ngoài đích vẫn qua.
  lệnh       : python evidence/env.py python evidence/measure.py evidence/r12-mutations.json; python evidence/env.py python evidence/probe.py.
  output     : mode_empty_both/orphan/shard, fingerprint_rc/format: mỗi phép đủ 56 ca, đúng t53 giet_that, 55 qua. Bảng 27 ô control nhận đúng 3 ô; mutant truthiness nhận sai thêm 1/2/2 ô. Bảng nguồn HEAD 33 ô (rc 0/1/2 × 11 stdout) control khớp oracle; các mutant bỏ rc/format lệch 6/7 ô. main_receiver_baseline_hong vẫn tương đương vì hong rỗng ở đường nhận; main_worker_header_one bị t54 giết.
  kết luận   : KHÔNG PHẢI LỖI ở năm biểu hiện cũ — ĐÃ VÁ THẬT. Việc đóng cả lớp còn phụ thuộc biên mới tại HƯỚNG 4–5.

HƯỚNG 4: Biên khoảng trắng và hoa/thường của chế độ
  giả thuyết : tự kiểm có MANH nhưng chưa có giá trị manh thừa khoảng trắng ASCII; chuẩn hoá không được âm thầm biến cấu hình sai thành gate.
  lệnh       : measure.py evidence/r13-mutations.json; probe.py; cặp neo/thay mode_trim_gate và mode_fold_gate nằm trong JSON.
  output     : mode_trim_gate sống 56/56 qua; control từ chối ba chuỗi ' manh', 'manh ', ' manh ', mutant nhận cả ba thành gate. mode_fold_gate bị đúng t53 giết nhờ fixture MANH.
  kết luận   : LỖI (P2), F31 nối lớp F29 — thiếu răng ở giá trị gate cần khớp đúng, không phải lỗi head nguyên bản tự nhận sai. Cắt khoảng trắng biến job có cấu hình sai thành nhánh không đo bán kính; M1/M4 đòi từ chối và tự kiểm chốt.

HƯỚNG 5: Ngữ pháp HEAD — độ dài và bảng chữ là hai chốt độc lập
  giả thuyết : stdout not-a-head của F30 sai đồng thời độ dài và bảng chữ, nên không chứng minh răng từng phần của regex.
  lệnh       : measure.py evidence/r13-mutations.json; probe.py (grids.json, consequences.json).
  output     : fingerprint_length_range và fingerprint_hex_class đều sống 56/56 qua. Phép thứ nhất đổi hai độ dài 40|64 thành khoảng 40..64, nhận sai 41/63 ký tự hex; phép thứ hai đổi a-f thành a-z, nhận sai 40 chữ g. Bản gốc trả None; mutant đưa vân tay lỗi vào writer/gom tổng hợp ⇒ writer [0,0], gom errors=0, 348 dòng ok.
  kết luận   : LỖI (P2), F32 nối F9/F30. Năm mutant lượt 12 đã chết nhưng lớp nguồn chưa đóng ở ngữ pháp. Không gọi đây là P1 của head chưa đột biến hoặc là bán kính thật: consumer dùng dữ liệu tổng hợp để chứng minh tác động của chốt nguồn bị nới.

HƯỚNG 6 (MỚI): Kho Git SHA-256 thật qua nguồn và consumer
  giả thuyết : hỗ trợ HEAD 64 ký tự trong F30 không chỉ đúng với subprocess giả.
  lệnh       : probe.py dùng git init --object-format=sha256, commit tạm, _van_tay, ghi/gom 2 mảnh tổng hợp.
  output     : HEAD nguồn thật dài 64, bằng git rev-parse HEAD; writer đạt cả hai mảnh, gom errors=0 cho 348 bản ghi. evidence/extra-domains.json.
  kết luận   : KHÔNG PHẢI LỖI. Đây là kiểm nguồn Git và giao thức, dữ liệu đo tổng hợp không thay A1 bán kính thật.

HƯỚNG 7 (MỚI): JSON ngoài miền số hữu hạn và khoá lặp
  giả thuyết : giá trị NaN/Infinity, mảng/object hoặc khoá header lặp có thể làm lọt tập mảnh sai.
  lệnh       : probe.py trên bộ hai mảnh lành; thay từng phien_ban/manh/so_manh/head/sha256_test bằng NaN, +/-Infinity, [], {}; thử so_manh lặp hai thứ tự.
  output     : 25/25 bộ giá trị sai bị chặn; so_manh cuối=1 bị G-so-manh; so_manh đầu=1/cuối=2 được nhận theo json.loads (giá trị cuối thắng), vẫn đủ hai mảnh/348 tên đúng phân hoạch. Khôi phục bộ lành ⇒ errors=0.
  kết luận   : KHÔNG PHẢI LỖI. Khoá lặp không tạo hai giá trị khác nhau giữa validator và consumer vì cùng parse một lần; không có bằng chứng bỏ đo/tập sai được gom xanh. SPEC hiện không cấm riêng duplicate key ở mức văn bản.

HƯỚNG 8: Hồi quy gate, registry, t152, lease, actionlint và Ruff F
  giả thuyết : packet không làm đỏ các gate/contract đã xanh ở baseline.
  lệnh       : run_regression.py; regression.py chạy lại sau checkout baseline hoàn tất; actionlint hai vế; Python/Ruff version probe. Mọi lệnh qua evidence/env.py (no bytecode, core.abbrev=7, chữ ký commit tắt cho kho tạm).
  output     : gate rc=0, 56/56, 0 bỏ qua, tiền kiểm 0, cổng cây thật ĐẠT, tự kiểm phân hạng/giàn giáo/song song đạt, GIAO 348 đột biến. Registry head 1025/1025, base 938/938, rc=0. t152 và lease t24/t31/t35/t161/t162 rc=0 hai vế. actionlint ci.yml rc=0 hai vế; probe cong_cu.py kiem-tra --json rc=0 hai vế. Ruff --select F trên W1/W3/W4 rc=1 hai vế, cùng sáu F841 (tệp/mã/message), delta=0. Python 3.11.15, actionlint 1.7.7, Ruff 0.15.8.
  kết luận   : KHÔNG PHẢI LỖI hồi quy trong các phép trên. Ruff đỏ nền không được gọi là lint xanh. Đây là G5 gate thật và registry tự kiểm, không phải chạy mọi suite qua registry --chay; Python CI ghim 3.12, cục bộ 3.11.15.

HƯỚNG 9: Gom/mảnh và miền cấu hình kế thừa
  giả thuyết : tập sai, dữ liệu đúng cấu trúc nhưng sai kết quả, hoặc thứ tự vật lý thay đổi có thể làm gom xanh sai.
  lệnh       : mode_domain.py; partition_roundtrip.py; gom_current_data.py; novel_files.py; cli_mode_collision.py; cli_collision_workflow.py; worker_domain.py.
  output     : lưới số 10816 ô: nhận 135, từ chối 10681, 11 dạng sai bổ sung, mismatch=[]; N=2..16 phủ đủ/rời nhau 348 tên, bảng đúng thứ tự, gom errors=0. Bộ lành 348 dòng; bộ đích sống/đích bỏ qua/tín dụng giả/bán kính rộng/lỗi đo đều đỏ. Sai danh tính ca/đích bị G-ban-ghi. Tên tệp và thứ tự bản ghi đảo vẫn đúng bảng; hardlink thừa/FIFO/thư mục/file cắt dở/HEAD lệch đều bị chặn. Toàn bộ bảy runner rc=0.
  kết luận   : KHÔNG PHẢI LỖI trong miền consumer đã đo. Các roundtrip này tổng hợp bản ghi, tách biệt A1 thật đang chạy.
