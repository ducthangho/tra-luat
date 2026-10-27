# ADR-0056 — Ngưỡng thu hồi lease vì không tiến triển nâng lên SÁU giờ (360 phút)

- **Trạng thái:** Accepted (2026-10-19, chỉ thị chủ kho `ducthangho`; thi hành bằng packet `wp835`
  revision 3 · generation 3 (bản vá r2/g2 port lên base mới, đổi số từ 0055 sang 0056 vì 0055 đã thuộc
  `docs/adr/0055-tran-loi-goi-codex-len-muoi.md`), Issue #835 — không phải một phiên tự nới ngưỡng) ·
  **ĐÃ KÍCH HOẠT VẬN HÀNH** — mốc kích hoạt là merge của PR thi công `wp943` vào `master` (Issue #943).
  Căn cứ: chủ kho xác nhận không có controller ngoài (#835 issuecomment-6407154789) cộng phép quét mã
  của chính mục *Hiệu lực*; thi hành bằng packet `wp943`. Lease cấp trước mốc ấy vẫn chịu ngưỡng đã
  đóng dấu trong chính nó.

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

Đo 19-10-2026 bằng quét mã tĩnh tại acceptance base `062292b2c75be8c316a0cf7347290574efa10861`
của revision 2, đo lại 25-10-2026 tại base `d2e3052d479d140b7e7b91df41ec4914fab7d544` của revision 3:
không có controller nào **trong kho** mang hằng 30 phút cho việc thu hồi;
ngưỡng ấy sống trong văn bản protocol và trong trường `heartbeat_required_minutes` của từng lease.

Mốc 26-10-2026: chủ kho xác nhận **không có controller ngoài** (dispatcher) — *"Không có, phiên điều
phối làm tay"* (#835 issuecomment-6407154789). Thu hồi lease do phiên điều phối làm tay theo protocol,
nên "đồng bộ controller" nghĩa là phiên điều phối áp ngưỡng 360 phút khi xét thu hồi. Luật áp dụng:
chỉ lease cấp SAU mốc kích hoạt (merge của PR thi công `wp943`) khai `heartbeat_required_minutes: 360`;
lease cấp trước mốc ấy giữ nguyên byte và số đã đóng dấu — kể cả lease `wp943-r1-g1-claude` của chính
packet kích hoạt, vẫn khai 30.

`.github/coordination/change-impact.v1.json` (`ADR-0032`) vắng mặt ở cả hai base ấy. Write set của
packet này là một ngoại lệ đóng tay một-packet do chủ kho duyệt trên Issue #835, không phải một closure tính từ
policy. Bản vá chỉ chạm hai tệp: tệp protocol và tệp ADR này. Revision 4 (chủ kho duyệt 25-10-2026) bỏ hai tệp đi
kèm của r3 (`scripts/tl_selftest.py` và `RELEASE_MANIFEST.json`), vì từ packet #794 `r291_docs_ngoai_goi` tính số
tài liệu dưới `docs/` từ cây, không còn ratchet nào để kê khai, và không tệp nào trong gói đổi.

## Vì sao sáu giờ

Đây là **quyết định của chủ kho**, không phải phép tối ưu. Ba mươi phút thu hồi cả những phiên đang
làm việc thật nhưng chưa ghi heartbeat kịp — một gate dài hoặc một lượt review chéo là đủ để vượt
ngưỡng — và mỗi lần thu hồi nhầm là một generation mới cộng một lượt handoff. Cái giá của sáu giờ là
một worker chết thật giữ write set lâu hơn; `lease_until` tuyệt đối vẫn chặn trên cái giá ấy.
