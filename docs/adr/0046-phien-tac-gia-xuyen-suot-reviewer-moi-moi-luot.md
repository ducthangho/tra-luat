# ADR-0046 — Tác giả XUYÊN SUỐT, reviewer MỚI mỗi lượt, cắt phiên ở BIÊN PACKET

- **Trạng thái:** Proposed (2026-08-22)

> **Vì sao PROPOSED chứ không Accepted, dù chủ kho đã duyệt mô hình.** Cross-review lượt 1 của PR #252
> bắt đúng chỗ (`adr-accepted-tren-bang-chung-khong-tai-lap`, P1): phần lớn căn cứ dưới đây — các phép
> đếm và bốn quan sát nhân quả của PR #250 — **chỉ sống trong comment GitHub**, không có biên nhận trong
> `ops/reviews/` (39 biên nhận trên master, **0** cái cho #250). Không thể vừa dùng chúng để `Accepted`
> vừa đòi reviewer *"không nhận lời khai của executor"*. **Điều kiện để promote lên `Accepted`:** đóng
> băng bằng chứng bốn lượt ấy thành biên nhận trong `ops/reviews/`, rồi neo ADR này vào chúng.

Mô hình phiên cho một chu kỳ soạn spec + review:

1. **Phiên tác giả GIỮ XUYÊN SUỐT** hết chu kỳ, không cắt giữa các lượt review.
2. **Reviewer MỚI mỗi lượt** — sandbox riêng, context riêng, không thấy lượt trước trừ verdict được giao.
3. **Cắt phiên ở BIÊN PACKET**, tức khi chuyển từ soạn spec sang thi công. Người thi hành **không** nên là
   phiên đã viết đặc tả.
4. Trong một phiên dài, **ép một lượt ĐO LẠI trước MỖI bước công bố** (đăng băm, cấp lease, merge).

## Vì sao tác giả xuyên suốt

Đo trên PR #250, bốn lượt trong một phiên. Bốn thứ chỉ bắt được nhờ liên tục:

- Reviewer báo `6 lease`; phiên biết nó từng là `9` nên nhận ra **phân rã**, không phải reviewer sai. Phiên
  mới sẽ nhận `6` như sự thật.
- Lỗ `A2c` (lease `CÒN_HẠN` mà đã chết) lộ vì phiên **tự quét lại** một con số mình từng đo. Phiên mới không
  có lý do gì đi đo lại thứ trông đã chốt.
- Hoãn công bố một thế hệ băm — làm được vì phiên biết công bố là đắt (băm chết) và còn lượt nữa. Nhờ hoãn,
  mỗi Issue chỉ phải khai tử một băm thay vì hai.
- Phát hiện thân PR và hai Issue **trôi lệch nhau**. Việc ấy đòi giữ cả ba cùng lúc.

## Vì sao reviewer phải mới

Reviewer mới mỗi lượt là điều kiện của `cross_approved` (§8) và không đổi ở ADR này. Ghi lại để nói rõ mô hình
là **LAI**, không phải "một phiên làm tất": tác giả liên tục, reviewer rời rạc.

## Vì sao phải cắt ở biên packet

Tới biên ấy, context tích luỹ của phiên tác giả **chủ yếu nói đặc tả được VIẾT THẾ NÀO**, không phải nó NÓI GÌ.
Người thi hành cần đọc đặc tả lạnh, y như mọi người sau này sẽ đọc. Giữ tác giả lại làm executor là mang nguyên
khối thiên vị tác giả sang giai đoạn mà thiên vị ấy không còn ai soi.

Bằng chứng thiên vị ấy có thật và đo được: mục `ngoai_pham_vi` của đặc tả `LEASE-HOI-TOAN-KHO` gạt ba trường
lease vào chung một ô với lý do *"trỏ NGƯỢC"* — lý do đúng cho hai trường, sai cho trường thứ ba. Phiên tác giả
thừa hưởng cách diễn đạt ấy từ một comment có sẵn rồi **coi là đã chốt, không tự dẫn lại**; ba lượt review cũng
không tách ra kiểm. Một phiên đọc lạnh có cơ hội hỏi.

## Nợ của mô hình này, nói thẳng

> **Lợi thế của phiên xuyên suốt là XUẤT XỨ; nợ của nó là xuất xứ có cảm giác như BẰNG CHỨNG.**

Mọi con số sai trong đợt #250 đều là con số **từng được đo đúng** rồi thôi không đo lại: `117/100` → `120/110`,
`37` → `39`, `3/90` → `3/100`, `+265` → `+313`. Không cái nào là đoán bừa. Biết *"tôi đã đo lúc 16:5xZ"* là một
**dấu thời gian**, không phải một **bảo chứng**. Khoản 4 ở trên tồn tại chính vì nợ này.

## Cắt phiên KHÔNG miễn phí

Sự cố 15-08-2026 (hook của nhánh packet cũ hơn hook trên master; `docs/GOI_AGENT_DA_NEN.md`) thuần là tai nạn
**biên phiên**. Nhiều biên hơn thì nhiều tai nạn loại ấy hơn. Nên cắt ở chỗ CÓ ÍCH — biên packet — chứ đừng cắt
theo lịch hay theo độ dài context.

## Cổng

**0 cổng VẬN HÀNH** — nói có điều kiện, vì câu tuyệt đối *"0 cổng"* ở bản đầu che mất một cổng đang có
(cross-review PR #252, `khong-phai-khong-cong-tuyet-doi`): `adr-song` **có** canh ADR này — nó đòi ADR được
đăng ký ở §20, đòi trạng thái hai bên khớp, và đòi có dòng `Trạng thái` đọc được. Cái nó **không** canh là
bốn khoản của mô hình. Mô hình phiên chưa đọc được bằng máy từ trong kho: không hiện vật nào khai "phiên này
có phải phiên đã viết spec không". Khoản 1–3 là kỷ luật vận hành. Khoản 4 có thể cưỡng chế một phần trong tương lai (đòi verdict
mang thời điểm đo cho mọi con số) nhưng chưa có cổng nào làm việc ấy hôm nay — nói ra để không ai tưởng đã có.
