# #1124 r4 — amendment routing reviewer và human audit

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

Revision kế nhiệm: 4; generation: 1. Đường dẫn khi công bố:
`ops/specs/ADR-0060-MAC-DINH-r4-reviewer-route.md`.

Trạng thái: DRAFT — chưa duyệt, chưa công bố, chưa dùng cấp lease hoặc nghiệm thu.

## Phạm vi và kế thừa

Kế thừa toàn bộ đặc tả `ops/specs/ADR-0060-MAC-DINH-r3.md`, SHA-256
`f7e8826d11545ce77b4630e4682464f74c6f1a277bc0e98a93ff5fbd459323e0`.
Amendment này chỉ thay routing reviewer và bổ sung human audit trước merge.
A1–A13, write set, budget, Windows required, A10, ADR-0060 M3 và mọi gate khác giữ nguyên nghĩa.
Không miễn lỗi setup, skipped/not_run, không sửa baseline hoặc ngưỡng tuổi bằng chứng.

Ứng viên kế thừa: H4 `c905714f408df0982438b435d7de0871f66eea77`,
tree `1effe33b73ab302f13844cedb4984da83c8b4bd3`,
parent `dc8b6d3b605c24c5a6b57005ad2265b535e476b2`;
base B `340163a3f4f4dccf3c02ab153c843e8f305fdeb2`.
Các SHA này định danh nguồn kế thừa và bằng chứng chẩn đoán hiện tại. Sau khi spec được duyệt và land
qua làn spec, lấy B' là commit master đã chứa artifact spec, ghi exact SHA vào lease kế nhiệm;
rebase phần mã lên B' thành H'. Diff B'..H' vẫn phải đúng năm tệp W1–W5 theo A12.
Không thêm spec thành tệp thứ sáu trong diff mã để né write set. B'/H' phải được review/test đầy đủ;
không dùng kết quả cặp B/H4 hiện tại làm nghiệm thu thay cho cặp B'/H'.
Commit mới làm mất hiệu lực review/tests/authorization của SHA cũ theo protocol.

## Routing thay thế

Codex tiếp tục làm executor. Vì agy hết quota, reviewer có thể là một phiên Codex độc lập,
context/worktree riêng, mặc định read-only, dùng model hoặc reasoning effort cao hơn executor.
Phải ghi cấu hình executor và reviewer thực sự quan sát được trong biên nhận; phần không đo được
phải ghi `khong_do_duoc`, không suy tên model đã phục vụ chỉ từ tên công cụ hoặc cấu hình yêu cầu.
Nếu chưa chứng minh được điều kiện cao hơn thì chưa đạt routing, phải báo chủ kho quyết định.
Executor không tự review hoặc tự approve công việc của mình.

Chỉ khi reviewer trả verdict approve trên đúng H, chứng cứ độc lập và điều kiện routing nêu trên đều đạt,
review cùng nhà cung cấp mới được ghi `same_provider_approved`; không ghi `cross_approved`.
Biên nhận phải neo đúng SHA và ghi cách xử lý từng finding; P0/P1/P2/P3 phải bằng 0 trước merge.
Yêu cầu 0 P1/P2/P3 là chỉ thị trực tiếp của chủ kho trong phiên này
(“điều kiện để mà merge đó là vá và cross review hết P1, P2, P3”), không phải miễn trừ hoặc diễn giải M1.
Review chuyên môn này không phải GitHub PR approval và không tự cho phép submit approval.

## Human audit và authority

Sau khi review và toàn bộ gate bắt buộc đạt, trình chủ kho gói human audit neo đúng H:
spec_hash, H/tree/parent/B, biên nhận reviewer và cấu hình, xử lý findings, Windows B/H,
CI exact HEAD, nghiệm thu A1–A13 (A13 ghi đúng trạng thái hậu land), và các quyết định/waiver hợp lệ nếu có.
Chỉ merge sau khi chủ kho hoàn tất human audit và duyệt đúng H theo ADR-0060 M7.
Đổi H sau audit phải trình lại audit/duyệt cho H mới.

Amendment này là artifact kế nhiệm dạng addendum: r3 bất biến được tham chiếu bằng hash ở trên,
và chính byte của addendum này là spec_path/spec_hash được chủ kho duyệt và lease kế nhiệm tham chiếu.
Nếu ghép hoặc đổi byte thành một artifact khác, artifact đó cần review và duyệt hash riêng trước cấp lease.
Lease revision 4/generation 1 phải trỏ đúng đường dẫn trên và hash của chính artifact đã duyệt.
Trước nghiệm thu K1, blob spec tại HEAD ứng viên phải khớp hash lease. H4 chỉ là nguồn kế thừa;
nếu tích hợp spec làm đổi HEAD, phải review và chạy lại các gate theo HEAD mới, không tái dùng verdict/tests H4.
Chỉ sau khi chủ kho duyệt SHA-256 của addendum này mới được công bố và
cấp lease kế nhiệm thay routing AGY/cross_approved của lease r3; ghi rõ lease bị thay thế,
giữ nguyên ownership/write set và kiểm tra holder hiện hành trước cấp.
Không ghi đè lease đang hoạt động của phiên khác. Việc duyệt amendment không tự xác nhận test,
không miễn M3(a)/(b)/(c), không thay human audit hoặc quyết định merge neo SHA.
Duyệt amendment không chứng minh hoặc miễn yêu cầu reviewer cao hơn executor; thiếu bằng chứng vẫn chặn routing.
