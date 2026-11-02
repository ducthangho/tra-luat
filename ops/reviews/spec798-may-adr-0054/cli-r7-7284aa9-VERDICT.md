VERDICT: changes_requested
P0=0 P1=0 P2=2 P3=0

## Lớp ca-nghiem-thu-khong-phan-biet-dung-sai — P2

- biểu hiện: ops/specs/wp796-r7.md:A1 — Luật chung vẫn đòi từ chối `--finding-id` trùng, trong khi A7 yêu cầu giữ đường cũ và các ca cũ yêu cầu nhận ID trùng, đếm một lần.
- biểu hiện: ops/specs/wp797-r7.md:A3 — Ca “quyền cũ” xóa `checkpoint_day` rồi đòi bắt được đột biến bỏ so generation tại M3; thiếu checkpoint vẫn chặn cả bản đúng lẫn bản đột biến.
- vì sao là lỗi theo (a)/(b)/(c): **(b)** Hai tiêu chí đầu mâu thuẫn trên cùng đầu vào; probe hàm hiện hành trong bộ nhớ trả `rc=0`, bộ đếm bằng 1. Tiêu chí sau không phân biệt được chốt generation: ngay cả khi các điều kiện khác đầy đủ, checkpoint vắng vẫn khiến cả hai phiên bản từ chối.
- hướng sửa ở mức lớp: Giới hạn luật trùng vào đúng giao diện mới `--finding <id>=<slug>`, giữ ca legacy. Tách phép đo xóa quyền khi chuyển generation khỏi phép đo cửa đọc: dựng baseline hợp lệ, chỉ đổi generation của checkpoint; bỏ riêng phép so ấy phải làm ca đỏ.

## Lớp ep-cross-review-cho-moi-assurance — P2

- biểu hiện: ops/specs/wp796-r7.md:M2 — Mọi packet áp ADR-0054 đều bị buộc reviewer khác họ model, kể cả lease cho phép `same_provider_approved` hoặc `human_audited`.
- biểu hiện: ops/specs/wp797-r7.md:M1 — Dùng lại `_du_dieu_kien_approve` nên kế thừa việc từ chối các mức assurance hợp lệ ấy.
- vì sao là lỗi theo (a)/(b)/(c): **(b)** Một packet routine được cấp fallback độc lập cùng họ model, có receipt approve đúng SHA/spec và bảng lớp rỗng, vẫn bị M2 từ chối. Human audit cũng không thể đáp ứng yêu cầu họ model. ADR-0054 §1 nói rõ không nâng assurance; protocol §8 cho phép hai đường này. Probe validator danh tính lease hiện hành nhận cả hai trường hợp.
- hướng sửa ở mức lớp: Kiểm assurance theo chính sách của lease và Review Class; chỉ buộc khác họ model khi yêu cầu `cross_approved`. Thêm ca dương cho same-provider độc lập và human audit, kèm ca âm sai assurance; giữ yêu cầu cross-review của hai packet sensitive đang giao.