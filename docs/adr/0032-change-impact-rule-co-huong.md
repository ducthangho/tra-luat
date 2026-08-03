# ADR-0032 — Change-impact rule có hướng

- **Trạng thái:** Accepted (2026-08-03, phiên grilling)

Write set khai tay không biểu diễn được coupling ẩn như thay `SKILL.md` làm số đo trong
`references/GOTCHAS.md` và check r219 cần được xác minh lại. Hệ thống dùng change-impact policy canonical có
hướng `trigger path → write closure + required checks`; dispatcher tính closure bắc cầu trước khi cấp lease và
CI tính lại từ diff. Lease, exclusion và `write_set_hash` dùng effective write set cùng policy SHA, nên hai packet
không thể âm thầm chia đôi một coupling; policy đổi làm packet liên quan phải re-evaluate và tăng generation nếu
closure đổi.

Write closure chỉ cấp phạm vi có thể cần sửa, còn required checks chứng minh invariant; không ép companion phải
đổi khi giá trị vẫn đúng. Land-only obligation thuộc land gate, không được kéo vào quyền worker. Quyết định này
không dùng nhóm file đối xứng vì quan hệ tác động thường một chiều. Coupling số byte hiện tại được khai như rule
tạm để phản ánh repo thật, nhưng foundation phải đánh giá việc sinh/bỏ pin đó; khi invariant biến mất, policy
phải thu hẹp thay vì biến số đo động thành coupling vĩnh viễn.

Policy chuẩn đặt tại `.github/coordination/change-impact.v1.json`, schema tại
`.github/coordination/schemas/change-impact.v1.schema.json`; JSON có `schema_version` để validator Python stdlib
đọc tất định, không thêm YAML dependency. Mỗi rule có `rule_id`, `trigger`, `write_closure`, `required_checks`,
`land_obligations`, `evidence`, `owner` và trường hết hạn cho rule tạm; policy/schema/validator/CODEOWNERS thuộc
security paths.
Seed ban đầu là báo cáo read-only rút ứng viên từ input/rule của `doc-claims-check`, golden và release gate, sau
đó human review từng rule; tool không tự promote coupling suy đoán vào canonical.

Áp dụng **change-impact ratchet** chỉ khi một check phát machine-readable `impact_hint` chỉ ra trigger/companion
ngoài closure. Generation hiện tại bị chặn và finding phải kết thúc có audit bằng một trong bốn cách: thêm/sửa
rule; chuyển thành land obligation; sinh/gỡ invariant động; hoặc ngoại lệ có `owner`, `reason`, `expires_at` và
human approval. Mọi thay đổi policy đi qua packet nhạy cảm; sau khi integrate resolution mới tính closure và cấp
generation nội dung mới. Gate không tự sửa policy và test failure thường không được suy diễn thành coupling.
Rule/exception hết hạn phải fail gate tới khi được thu hẹp, xóa hoặc gia hạn có review.
