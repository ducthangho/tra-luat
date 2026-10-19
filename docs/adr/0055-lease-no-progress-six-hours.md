# ADR-0055 — Ngưỡng thu hồi lease vì không tiến triển nâng lên SÁU giờ (360 phút)

- **Trạng thái:** Accepted (2026-10-19, chỉ thị chủ kho `ducthangho`; thi hành bằng packet `wp835`
  revision 1, Issue #835 — không phải một phiên tự nới ngưỡng) · **CHƯA KÍCH HOẠT VẬN HÀNH**: chờ
  controller ngoài được đồng bộ và xác minh, xem mục *Hiệu lực*. Tới lúc ấy mọi lease vẫn chịu ngưỡng
  đã đóng dấu trong chính nó.

Lease không có tiến triển trong **6 giờ (360 phút)** thì dispatcher thu hồi, tăng generation rồi mới
reroute. ADR này thay **đúng một câu** của `ADR-0017` — câu *"Sau 30 phút không có tiến triển"* — và
không thay gì khác. Khi `review_sla` thiếu, không parse được hoặc cơ sở giờ mơ hồ, đồng hồ dự phòng
fail-closed cũng là 6 giờ này, không phải một con số riêng.

## Những gì KHÔNG đổi

- `lease_until` vẫn là timestamp tuyệt đối: hết `lease_until` thì lease hết, kể cả khi chưa đủ 6 giờ
  không tiến triển. Ngưỡng 6 giờ chỉ là cửa thu hồi SỚM, không gia hạn lease.
- Fencing theo generation, bia mộ hai chiều (`thay_the_cho` · `da_bi_thay_the`) và vô hiệu theo exact
  head giữ nguyên.
- `review_sla` mặc định (vào `reviewing` + 2 giờ) và chế độ *treo theo review* giữ nguyên.
- Verdict `changes_requested` đổ về thì executor vẫn phải heartbeat trong **15 phút**.
- `ADR-0017` vẫn hiệu lực ở mọi phần còn lại.

## Không hồi tố

Ngưỡng mới chỉ áp cho lease **mới cấp sau khi kích hoạt**, và lease ấy khai
`heartbeat_required_minutes: 360`. Lease đã cấp — kể cả WP748 g19 — giữ nguyên byte và giữ
`heartbeat_required_minutes` đã đóng dấu. Muốn một packet đang chạy hưởng 360 phút thì phải có lease
kế nhiệm được cấp quyền riêng sau khi ADR này kích hoạt; không sửa lease cũ tại chỗ.

## Hiệu lực

Đo tại base `6842a625`: không có controller nào **trong kho** mang hằng 30 phút cho việc thu hồi;
ngưỡng ấy sống trong văn bản protocol và trong trường `heartbeat_required_minutes` của từng lease.
Controller ngoài (dispatcher) **chưa đo được** từ phiên này. Nên ADR này chưa được khai là đã kích hoạt
vận hành: chưa xác minh được controller đã đồng bộ thì không cấp lease 360 phút.

`.github/coordination/change-impact.v1.json` (`ADR-0032`) vắng mặt ở base. Write set hai tệp của
packet này là một ngoại lệ đóng tay một-packet do chủ kho duyệt trên Issue #835, không phải một
closure tính từ policy.

## Vì sao sáu giờ

Đây là **quyết định của chủ kho**, không phải phép tối ưu. Ba mươi phút thu hồi cả những phiên đang
làm việc thật nhưng chưa ghi heartbeat kịp — một gate dài hoặc một lượt review chéo là đủ để vượt
ngưỡng — và mỗi lần thu hồi nhầm là một generation mới cộng một lượt handoff. Cái giá của sáu giờ là
một worker chết thật giữ write set lâu hơn; `lease_until` tuyệt đối vẫn chặn trên cái giá ấy.
