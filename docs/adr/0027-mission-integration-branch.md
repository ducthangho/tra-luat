# ADR-0027 — Mission integration branch

- **Trạng thái:** Accepted (2026-08-03, phiên grilling)

Mỗi mission có nhánh `mission/<issue>/integration` tạo từ một base SHA cố định. Packet tạo branch/worktree riêng
từ head integration hiện tại và mở PR vào integration, không PR thẳng vào canonical. Dispatcher là bên duy nhất
merge tuần tự packet đã qua worker gate và review policy; lifecycle có thêm trạng thái `integrated` giữa
`accepted` và `landed`.

Packet có dependency chỉ chạy sau khi predecessor đã integrated, tránh stacked PR. Packet độc lập được phép
chạy song song từ cùng base nhưng phải rebase lên head integration mới và chạy lại write-set/worker gate trước
khi merge. Effective-write-set exclusion sau change-impact closure là toàn repo, kể cả giữa hai mission. Vì vậy
conflict và coupling ẩn được phát hiện ở từng packet nhỏ thay vì dồn vào canonical.

Mỗi mission chỉ có một draft land PR từ integration vào canonical. Phiên land xử lý lần rebase/integration cuối,
version, changelog và manifest; dispatcher không có quyền merge canonical. Mô hình này thêm một nhánh trung gian
nhưng đổi lại dependency rõ, ít stacked PR và một điểm hội tụ tuần tự có audit.
