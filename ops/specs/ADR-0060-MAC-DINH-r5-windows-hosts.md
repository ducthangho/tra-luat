# #1124 r5 — bổ sung máy Windows cho A10

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

Revision kế nhiệm: 5; generation: 1. Đường dẫn dự kiến:
`ops/specs/ADR-0060-MAC-DINH-r5-windows-hosts.md`.

Trạng thái: DRAFT — chưa duyệt hash, chưa công bố, chưa dùng cấp lease hoặc nghiệm thu.

## Kế thừa và thay đổi duy nhất

Kế thừa addendum r4 `ops/specs/ADR-0060-MAC-DINH-r4-reviewer-route.md`, SHA-256
`fd64b142defef4edf047b408847312d8c32847523909948ce9de7e3030789154`,
và r3 mà r4 tham chiếu, SHA-256
`f7e8826d11545ce77b4630e4682464f74c6f1a277bc0e98a93ff5fbd459323e0`.

Chỉ mở rộng lựa chọn máy Windows của mục `windows`, Q6 và A10 trong r3:
`tra-luat-win` hoặc `ASUS-LAPTOP`, qua Desktop Commander trên máy chủ kho đã cho phép.
Không đổi A1–A13 ngoài tên máy tại ba vị trí này; giữ write set W1–W5, budget,
routing reviewer, bằng chứng cấu hình được chủ kho chấp nhận, M3/M4/M5 và human audit.

Lý do: VM chưa đủ dung lượng cho full suite; ASUS có thể dùng khi công việc hiện hữu
kết thúc và kiểm tra thực tế đạt. Đây là thay đổi environment theo protocol §3.2.1,
cần revision/spec_hash và lease kế nhiệm, không sửa ngầm lease r4.

## A10 trên máy được chọn

Cả nền B và ứng viên H phải chạy trên CÙNG một máy được chọn trong hai máy trên,
cùng lệnh đầy đủ `python .claude/dev/packet_loop_test.py`, cùng môi trường được ghi nhận.
Giữ clone nền từ GitHub và bundle exact SHA H theo ADR-0060 M4; ghi commit, tree,
parent, hash bundle, inventory Python/Git/Windows, lệnh, thời gian và exit code thực.
H phải đạt N/N hai số bằng nhau, các ca `cong_c_k1_*` đạt; kết quả và dòng Windows mà
`kiem-merge` đọc phải neo đúng H. Giữ nguyên vế đỏ A10.

Giữ nguyên M3(a): full mandatory tests, không coi lỗi setup hay mandatory skipped/not_run là xanh.
Giữ nguyên M3(b): tập FAILED ID trên H nằm trong tập FAILED ID trên B.
Giữ nguyên M3(c): chủ kho quyết định ca đỏ trong write set. Không miễn lỗi fixture nền,
không sửa nguồn B, ngưỡng tuổi bằng chứng hoặc che ID test để đạt nghiệm thu.

Trước khởi chạy phải xác minh Commander roundtrip, máy và ổ thực, tài nguyên,
khóa theo ADR-0057/0058/0059, không có tác vụ xung đột; không dừng test hiện hữu.
Ngưỡng vận hành của bộ chạy đang chuẩn bị là 10 GiB trống trước setup/mỗi phase,
giữ dự phòng 2 GiB khi chạy. Đây là guard chống đầy đĩa, không thay tiêu chí pass.
Ghi đúng đường dẫn khóa và danh tính máy trong evidence; giám sát giữ quyền sở hữu,
heartbeat và kiểm tra descendants trước dọn TEMP riêng hoặc nhả khóa.

## Authority, tích hợp và chứng cứ

Chỉ sau review độc lập và chủ kho duyệt chính SHA-256 của artifact này mới công bố
và cấp lease revision 5/generation 1 kế nhiệm r4. Ghi lease bị thay thế, kiểm tra holder,
không ghi đè lease của phiên khác; giữ nguyên năm đường dẫn code được phép.

Ứng viên nguồn hiện có H8 `ca876c62cb2a4b4d043662ddecda31c8069af40c`,
tree `1eb234252f5283ac67d78991903602288373a135`,
parent `7eaea1f3d9dd4b72c3ca4c20158cc109a5a97054`,
base B′ `6c9079c2e6ef51bc2be27f1588958937e11cc261` chỉ định danh nguồn kế thừa.
Spec đi làn hồ sơ riêng; sau khi land, lấy nền mới chứa artifact và tích hợp code
thành H mới theo quy trình r4, giữ diff code đúng W1–W5. Không thêm spec thành tệp thứ sáu.
Phải review và chạy các gate theo exact SHA mới; kết quả H8 hoặc H4 không tự trở thành
nghiệm thu H mới. Chưa có SHA B/H mới khi bản nháp này được lập.

Human audit và duyệt exact code HEAD vẫn bắt buộc sau khi toàn bộ gate đạt, trước merge.
Duyệt spec không xác nhận tests, không thay audit/duyệt merge, không cấp quyền LIVE/deploy,
thay credentials/access, mua quota hoặc submit GitHub PR approval.
