# ADR-0026 — Rollout theo promotion gate

- **Trạng thái:** Accepted (2026-08-03, phiên grilling)

Hệ thống không được bật big bang. Bootstrap trước pha 1 là land bộ ADR/protocol/research bằng một PR docs-only
tạo từ worktree sạch trên `origin/master` mới nhất; không stage từ cây canonical đang bẩn. Thứ tự rollout là:
(1) baseline, test-fragment harness trước, rồi operational freeze/drain và maintenance EOL; (2) protocol, ba
skill/adapters, branch protection, security guard, change-impact policy và hai CI lane nhưng chưa có provider secret;
(3) dispatcher shadow với fixture/dry-run; (4) cloud canary một provider, một packet, chưa tự sinh kế nhiệm;
(5) dual provider, review phân tầng và circuit breaker; (6) autonomous mission và lệnh Android; (7) local
controller; (8) land automation đầy đủ.

Deferred numbering và worker gate không được promote riêng lẻ. Chúng tạo một **kích hoạt worker** nguyên tử:
worker gate tạo manifest tạm ngoài repo bằng primitive `release-manifest --out`, kiểm nó bằng `release-verify
--strict`, và không so feature branch với manifest committed; land gate vẫn sở hữu manifest phát hành. Policy,
adapter hoặc workflow có thể land ở trạng thái chưa bật, nhưng dispatcher không cấp packet worker cho tới khi
cả hai vế cùng sẵn sàng. Nhờ vậy không có cửa sổ mà worker đã bị cấm cập nhật release metadata nhưng mọi gate
còn đòi metadata canonical thay đổi.

Cutover không duy trì hai lane v0/v1. Trước activation, inventory mọi PR/branch đang bay; PR kiểu cũ chạm version,
changelog hoặc manifest phải merge/đóng hay chuyển sang packet mới và rebase. Activation chỉ được land khi không
còn PR ghi chưa phân loại nhắm canonical ngoài chính PR activation; ghi `protocol_cutover_sha`, rồi required
checks mới chuyển một lần sang protocol v1. Branch cũ không được nhận lane legacy theo tuổi/label vì ngoại lệ đó
sẽ sống dai và tạo hai nguồn chính sách.

Mỗi nấc có promotion gate đo được, kill switch và đường quay về nấc trước. Không promote khi còn stale lease,
diff ngoài effective write set, state race, handoff sai schema hoặc packet sinh trùng. Không nấc nào tự mở quyền canonical
hay LIVE; ranh giới của ADR-0020 và hai cổng của ADR-0022 giữ nguyên trong mọi pha.

Delivery chia hai chân trời. **Foundation horizon** (pha 1–2) là phạm vi cam kết trước: repo conflict-safe cho
các phiên do người dùng khởi chạy, có EOL/deferred artifacts/test fragments/change-impact policy và worker/land
gate, nhưng chưa được tuyên bố autonomous. **Automation horizon** (pha 3–8) vẫn là mục tiêu ban đầu nhưng mỗi pha
là một epic được promote riêng sau evidence/budget review; không gộp nhiều epic vào một PR/mission. Phase 3
shadow là checkpoint bắt buộc trước mọi provider secret/model call. Hoàn thành foundation không được dùng để
tuyên bố hệ thống đã tự sinh kế nhiệm, chạy khi Windows tắt hay land end-to-end trên Android.
