# ADR-0024 — Review phân tầng khi hết quota

- **Trạng thái:** Accepted (2026-08-03, phiên grilling)

Cross-review khác nền tảng là mức ưu tiên cao nhất nhưng không phải gate tuyệt đối cho mọi packet. Nếu nền tảng
còn lại hết quota hoặc không khả dụng, dispatcher thử một phiên reviewer độc lập cùng nền tảng; nếu cũng không
có reviewer thì packet mang trạng thái `review_deferred` và vẫn được đi đến draft land PR. Mức bảo đảm phải hiện
rõ là `cross_approved`, `same_provider_approved` hoặc `review_deferred`; fallback không được giả danh cross-review.

Lỗi quota/rate-limit đã phân loại không tính vào attempt triển khai. Dispatcher bật circuit breaker theo nhà
cung cấp và chỉ thử lại sau thời điểm reset, tránh đốt quota trong vòng lặp. Draft land PR liệt kê mức review của
từng packet; operation `land apply` phải yêu cầu người dùng xác nhận riêng nếu còn `review_deferred`, bất kể gọi
qua client local hay GitHub/Android.

Thay đổi workflow, security paths, credential boundary, dispatcher, migration dữ liệu hoặc LIVE adapter không
được hạ xuống review deferred: phải có cross-review khác nền tảng hoặc human review có audit. Reviewer agent chỉ
có quyền đọc code và ghi verdict/comment vào PR; không push branch. Yêu cầu sửa trả về executor và chỉ lỗi nội
dung mới tiêu thụ attempt; phát hiện ngoài effective write set cần cấp lại lease hoặc tạo packet kế nhiệm.
