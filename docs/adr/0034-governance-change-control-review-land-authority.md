# ADR-0034 — Change-control, review độc lập và thẩm quyền land

- **Trạng thái:** Accepted (2026-08-08, MCR-54-01; chủ kho phê duyệt)

Protocol dùng ba lớp kế hoạch: Mission Plan mô tả outcome và đồ thị Packet; Packet Spec là hợp đồng objective,
acceptance, write set, dependency, executor và environment; Session Plan chỉ là chiến thuật của một phiên. Mission
đổi material phải qua Mission Change Request có impact analysis, human approval và revision/plan hash mới. Packet
đổi contract phải revision + generation mới; việc ngoài spec thành successor Packet. Kết quả đã landed chỉ được
điều chỉnh bằng corrective/revert Packet, không viết lại lịch sử.

Mỗi phiên chỉ giữ một vai trò và một đơn vị công việc, nhưng “một đơn vị” gồm mọi substep cần thiết trong spec,
không phải một micro-step. Executor, Reviewer, Approver và Land Operator là các vai tách biệt. Reviewer phải dùng
phiên read-only độc lập trên exact SHA; same-provider là fallback có assurance thấp hơn, còn phạm vi nhạy cảm cần
cross-provider hoặc human audit. Executor có thể được ủy quyền bền để làm Land Operator cho exact SHA, nhưng không
nhờ đó tự review hay approve code của mình.

Mọi transition quan trọng có evidence trên GitHub: Executor ghi identity/generation/SHA/diff/test/handoff;
Reviewer ghi session độc lập, reviewed SHA, hai trục review, findings và verdict; land ghi Approver,
authorization, operator, merge commit, post-merge gate và bookkeeping. Head đổi làm review, CI và authorization cũ
hết hiệu lực. `merged` chỉ nói PR vào nhánh đích, `integrated` nói Packet vào mission integration, `landed` cần vào
canonical cùng hậu-merge gate và bookkeeping, còn Mission chỉ `complete` sau final readback và không còn việc mở.

Quyết định này tăng số Issue/comment và checkpoint, nhưng đổi lại tránh tự duyệt, scope drift, approval trên SHA
cũ và lịch sử bị viết lại. Các adapter chỉ trỏ về protocol; schema/enforcement thuộc các Packet F3 chuyên trách để
không sinh nhiều bản doctrine lệch nhau.
