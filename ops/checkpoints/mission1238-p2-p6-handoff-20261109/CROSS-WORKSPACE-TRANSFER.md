# Chuyển tệp giữa hai workspace — sửa đường nhận gói

Chủ kho báo phiên mới không có ZIP ở đường /workspace của phiên cũ và yêu cầu phiên cũ tìm/gửi gói cho phiên mới. Dispatcher kế nhiệm đã ghi nhận tiếp quản tại Mission1238 comment6738948800. Phiên cũ chỉ làm **hỗ trợ vận chuyển bàn giao**, không nhận lại dispatcher hay chạy product work song song.

Nguyên gói ZIP3605236bytes, SHA2566ac46ac05b2cf1bc8393914e340848a6a2a331af4a04e97356bc47e73abbb8bc được lưu tại artifacts/mission1238-P2-P6-handoff-20261109.zip trên controlref này. Đây là artifact dữ liệu để chuyển cùng candidate/evidence giữa workspace; không tạo productbranch/PR, không tạo codeapproval/M5pass/Ready, không cấp lease hoặc reset cap. H2 trong bundle vẫn là candidate chưa formalreview/nativeU10pass, productpushP2 vẫn0/1; clone/import vào ref local riêng và giữ preflight/lease/gates trước execution.

Ghi chú này thay riêng cách chuyển tệp local-only trong handoff9f7d365; byte ZIP và nội dung còn lại giữ nguyên. Không dùng metadata artifactref để lách điều kiện review trước primary productpush. Quyền vận chuyển đến từ yêu cầu trực tiếp hiện tại của chủ kho, không phải từ tên tài khoản đăng comment. ZIP không có credential/loginprofile được lựa chọn để chuyển.
