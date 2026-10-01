<!-- executor: luot 11 BI CAT boi bo loc noi dung (23:51Z, khi reviewer soan script dot bien phan hoach partition_rotation/partition_reverse_source). Lan chay 1 truoc do bi ngat do container bi thu hoi (~20:30Z). Khong co ket luan cuoi; noi dung duoi day la NGUYEN VAN phan da ghi. -->

verdict: dang_review
reviewed_sha: e4b7bdb2214fa6351c5ff58c686e871d6291beb2

Cross-review độc lập lượt 11. Chỉ đột biến trên bản sao /tmp; không sửa mã sản phẩm. Kết quả được đo lại trong lượt này.

HƯỚNG 1: Neo vật liệu và phạm vi
  giả thuyết : đúng head, SPEC, write set và trần đã cấp.
  lệnh       : git -C cay-kho rev-parse HEAD HEAD^{tree}; sha256sum SPEC.md; git diff baseline HEAD --numstat; python evidence/snapshot.py initial
  output     : HEAD=e4b7bdb2214fa6351c5ff58c686e871d6291beb2; tree=68d691afe3cd2d1643fe679224c4ae34bf18cc25; SPEC=dd2ada1b8511bec1c6c30ffdd7a94a3c34f4024836761878caf73ce339516b15; 5 tệp +1540/-49; status sạch. 339 đột biến/56 CA, baseline 212/53, không mất tên cũ.
  kết luận   : KHÔNG PHẢI LỖI. Áp trần ~1600 theo chỉ thị trực tiếp. Các bản sao /tmp đã tồn tại khi clone thử; đã xác minh exact SHA, tracked diff sạch trước khi dùng. Không dùng kết quả cũ: evidence/ chỉ nhận script .py; mọi JSON/log kết quả sinh mới.

Môi trường: OpenAI Codex qua công cụ shell của phiên này; không có biên nhận độc lập để tự chứng nhận model/effort thực tế hoặc human_audited. Không GitHub CI, push, comment, land. PYTHONDONTWRITEBYTECODE=1, Git abbrev=7, signing=false qua evidence/env.py. Snapshot băm toàn bộ tệp ngoài .git của cây ứng viên, cùng HEAD/tree/status gồm ignored; chỉ chứng minh bất biến giữa hai mốc. Bản sao baseline/head dùng để chạy test, không sửa cây ứng viên.

HƯỚNG 2: Workflow F1/F3/F10/F14 — chạy payload sẵn có, đột biến chốt
  giả thuyết : lớp workflow còn đóng; phân biệt chốt có bảo vệ chồng với chốt không có răng.
  lệnh       : python evidence/env.py python -u evidence/workflow.py; python evidence/env.py python -u evidence/workflow_ablation_extra.py
  output     : control F1=20/20, F3=28/28, F10=7/7, F14=5/5 chặn. Gỡ F10: 7 F10 lọt. Chỉ splitlines(): 0 lọt. Gỡ F10 + splitlines(): 27 F3 và 7 F10 lọt. Gỡ execution guard: 13 F1 lọt. Gỡ execution + shell guard: 18 F1, 7 F10, 5 F14 lọt.
  kết luận   : KHÔNG PHẢI LỖI trong miền đã đo. Chỉ chạy phan_chung có sẵn; không dựng payload điều khiển/ẩn. Log evidence/workflow-*.log và workflow-summary.json.

HƯỚNG 3 (MỚI): Cửa CLI không đối số dưới env HỢP LỆ — miền bù của F26
  giả thuyết : phép CLI của t54 chỉ đo cấu hình lỗi nên không bảo vệ việc đi vào main/truyền rc khi cấu hình hợp lệ.
  lệnh       : python evidence/env.py python -u evidence/novel_entry.py; python evidence/env.py python evidence/entry_valid.py
  output     : entry_requires_config, entry_gate_shortcut, entry_full_rc: mỗi phép đủ 56/56 trạng thái qua, không ca bị giết. Wiring CLI thật (chỉ thay thân main bằng marker + rc để đo dispatcher rẻ): control vào main ở du/gate/manh và truyền rc 0/1. entry_requires_config ở du rc=0, entered=false; entry_gate_shortcut ở gate rc=0, entered=false; entry_full_rc ở du main_rc=1 nhưng CLI rc=0, entered=true.
  kết luận   : LỖI (P2), F28 nối F26/F13/F25. Bản vá đã giết hai mutant vô điều kiện F26 nhưng chưa đóng lớp CLI mặc định: đường dương không được quan sát. Đây là thiếu răng; không khẳng định head chưa đột biến đang bỏ main. Phản chứng đủ 56 CA ở novel-entry-*.json, cặp neo/thay ở novel-entry-mutations.json, wiring ở entry-valid.json. Cần quan sát cả vào main lẫn chuyển rc trên miền hợp lệ du/gate/manh, có đối chứng lỗi, và giữ bán kính t54 độc lập t52/t53.

HƯỚNG 4 (MỚI): Topology hiện vật — thứ tự tên tệp/bản ghi, hardlink và mục đặc biệt
  giả thuyết : gom phải dựa vào danh tính trong bản ghi, không dựa vào tên/tứ tự hiện vật; đọc mọi mục phải từ chối mục không thường/trùng.
  lệnh       : python evidence/env.py python evidence/novel_files.py
  output     : control và đổi toàn bộ tên sang tên Unicode + khoảng trắng, đảo thứ tự bản ghi trong mỗi tệp: GOM MẢNH 8/8, 339 dòng ok, lỗi=0. Hardlink thêm của mảnh 0: G-dem; FIFO và thư mục con: G-tep; tệp cắt giữa bản ghi: G-ban-ghi; pha HEAD khác: G-van-tay. Khôi phục bộ lành lại 339 ok.
  kết luận   : KHÔNG PHẢI LỖI. Dữ liệu tổng hợp để thử consumer, KHÔNG khai là bán kính thật/A1. Evidence novel-files.json.

HƯỚNG 5: Miền cấu hình/phân hoạch và gom trên dữ liệu đúng cấu trúc sai kết quả
  giả thuyết : mọi cặp hợp lệ phải phân hoạch rời nhau, và gom không được đổi dữ liệu đo sai thành xanh.
  lệnh       : mode_domain.py; partition_roundtrip.py; gom_current_data.py (đều qua evidence/env.py)
  output     : lưới 10816 cặp k/N: nhận 135, từ chối 10681, mismatch=[]; 11 hình dạng sai thêm đều bị từ chối. N=2..16: phủ 339, rời nhau, gom lỗi=0, bảng đúng thứ tự. Bộ 8 mảnh lành: 339 ok. Đích sống/bỏ qua/tín dụng giả/bán kính rộng/lỗi đo: mỗi bộ lỗi=1. Thừa ca/sai đích: G-ban-ghi.
  kết luận   : KHÔNG PHẢI LỖI trong miền này. Các bộ dữ liệu là tổng hợp, không thay A1 hoặc bán kính thật.

HƯỚNG 6: Hồi quy gate và công cụ hai vế
  giả thuyết : gate trọn vẹn giữ các phép đo trước vòng bán kính; các kiểm tra chung không thêm nợ.
  lệnh       : python evidence/env.py python -u evidence/run_regression.py
  output     : gate rc=0 (232.9s), cong_cu_test 56/56, lỗi đột biến=0, tiền kiểm bỏ qua=0, cổng cây thật ĐẠT, tự kiểm song song ĐẠT; thông báo GIAO mảnh rõ. Registry head/base rc=0/TỔNG ĐẠT. t152 và lease t24/t31/t35/t161/t162 đều PASS hai vế. actionlint ci.yml rc=0 hai vế. Ruff --select F trên W1/W3/W4: rc=1 cả hai, cùng 6 F841, delta=0 (không khai bare lint xanh). Probe cong_cu.py kiem-tra --json rc=0 cả hai.
  kết luận   : KHÔNG PHẢI LỖI. Python cục bộ 3.11.15 (workflow ghim 3.12); actionlint 1.7.7, Ruff 0.15.15. Log riêng head/base, ruff-delta.json. Dòng KHÔNG ĐO ĐƯỢC trong t162 thuộc phản chứng biểu thức lệch của chính ca, không phải một ca bị skip.
