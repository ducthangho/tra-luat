# ADR-0020 — Ranh giới an ninh cho worker cloud

- **Trạng thái:** Accepted (2026-08-03, phiên grilling)

Dispatcher chỉ được bật sau khi có ranh giới an ninh độc lập với lời nhắc và guard trong mã. Worker cloud không
bao giờ nhận credential hay config của Drive, GAS, NLM, registry, deploy hoặc hệ thống LIVE. Workflow gọi agent
lấy định nghĩa cố định từ canonical, không dùng `pull_request_target` để chạy mã chưa tin cậy, và không cho
feature branch thay workflow/policy đang có credential. Action bên thứ ba phải pin commit SHA; canonical có
branch protection và các security paths chỉ được đổi qua packet hạ tầng do người dùng duyệt riêng.

Mỗi job nhận `GITHUB_TOKEN` ngắn hạn với đúng quyền cần thiết. Job gọi Claude/Codex được tách khỏi job checkout
và chạy code/test; job test không có secret. Credential nhà cung cấp là credential riêng, dễ thu hồi và có quota
chi phí cứng. Kiến trúc đích dùng broker xác thực GitHub OIDC rồi gọi nhà cung cấp thay runner, để raw API key
không nằm trong môi trường có agent/shell; GitHub Secret trực tiếp chỉ là bước chuyển tiếp có giới hạn và phải
được xoay vòng.

Guard từ chối lệnh LIVE khi có `CI`/`GITHUB_ACTIONS` vẫn bắt buộc nhưng chỉ là phòng thủ bổ sung vì mã trên
feature branch có thể sửa guard. Ranh giới thật là thiếu credential LIVE, token tối thiểu, workflow tin cậy và
branch protection. Do đó sự cố hoặc prompt injection trên worker chỉ được phép ảnh hưởng feature branch, Issue,
PR và quota agent; không được chạm canonical hay hệ thống LIVE.
