# ADR-0054 — Đẩy nhánh code một lần, dừng vá theo hạng, review tìm theo lớp

- **Trạng thái:** Accepted (2026-10-16, chỉ thị chủ kho `ducthangho`; thi hành bằng packet `wp784`
  `PUSH-MOT-LAN-VA-DUNG-VA`, Issue #784 — không phải một phiên tự đặt luật)

Ba luật, một chỉ thị. Chủ kho nói: *"sẽ không được push vào cho đến khi đủ điều kiện để merge"*, *"điều kiện
để dừng vá là khi hết P1 và P2"*, và *"cross review thì luôn tìm theo phân lớp, không tìm theo các lỗi riêng
lẻ"*. Phần đã có sẵn thì không lặp lại: lịch sử lớp và bảng lớp mỗi lượt đã nằm ở §8.3 của protocol.

## 1. Đẩy nhánh code của packet đúng một lần

Executor **đẩy nhánh code của packet đúng một lần**, khi ứng viên đã đủ điều kiện merge theo mọi phép đo làm
được tại chỗ. Trước lần đẩy ấy, trên **đúng commit sẽ đẩy**, executor chạy đủ cổng tại chỗ, tối thiểu:

- `python scripts/tl.py --selftest` ⇒ `N/N` với hai số bằng nhau;
- các cổng mà đặc tả packet liệt kê (vd `adr-song`, `doctrine-scan`, `release-verify --strict`, `git diff --check`);
- review khác nền đã approve trên chính SHA ấy (mục 2).

Lý do đo được: packet #782 đẩy lần đầu sau ba cổng tài liệu xanh nhưng **không** chạy selftest, và CI đỏ
`1730/1731` ở ca `r291_docs_ngoai_goi` (run `38945289558`). Một lần đẩy hỏng kéo theo revision đặc tả, lease
mới và vòng review mới.

**Ngoại lệ duy nhất: CI đỏ sau lần đẩy.** Executor được đẩy thêm **chỉ để sửa CI**, và mỗi lần như vậy
**ghi vào biên nhận** của packet: SHA trước/sau, check đỏ, nguyên nhân, vì sao cổng tại chỗ không bắt được.
Lần đẩy vá CI không được mang thêm bản vá cho finding review; finding mới phát hiện thì đi mục 2.

**Phạm vi.** Luật chỉ áp cho nhánh code của packet (`agent/wp<issue>-g<generation>-<executor>`). Nhánh
`ops/**` (lease, bia mộ, biên nhận) và nhánh đặc tả là sổ sách, đẩy như trước, ngoài luật này.

Bốn ca, mỗi ca một câu trả lời:

| ca | được đẩy? |
|---|---|
| nhánh code, lần đầu, khi đã đủ điều kiện | được |
| nhánh code, giữa các vòng vá | không |
| nhánh code, CI đỏ sau lần đẩy, bản vá chỉ sửa CI | được, ghi vào biên nhận |
| nhánh `ops/**` hoặc nhánh đặc tả | ngoài luật này |

## 2. Review offline, neo SHA commit cục bộ

Vì nhánh code chưa đẩy trong lúc vá, mọi vòng review chạy **offline** trên bundle/mirror dựng từ commit cục bộ
(cơ chế đã có ở §8 của protocol), neo SHA commit cục bộ. Verdict nêu SHA ấy và `spec_sha256` của đặc tả. Lần
đẩy duy nhất đẩy **đúng** SHA đã được approve, nên điều kiện *"exact SHA"* vẫn đúng mà không phải review lại.

Connector review trên PR GitHub chạy sau lần đẩy. Nó **không** mở vòng vá tự động: nếu nó báo P0/P1/P2 trên
head đã đẩy, executor DỪNG và đưa checkpoint cho chủ kho kèm phép đo. Đẩy thêm để vá finding ấy là quyết định
của chủ kho, không phải ngoại lệ vá CI.

## 3. Dừng vá theo hạng, ở mọi class

Điều kiện dừng vá: **Không còn P0/P1/P2** theo bảng lớp của lượt review mới nhất, ở **mọi** Review Class.
`routine` không còn được giữ P2 dạng nợ; `sensitive` giữ thêm yêu cầu approval tường minh đúng assurance và quyết
định có căn cứ cho từng finding P3 còn mở. P0 chặn ở mọi class như trước.

**Vòng vá thêm vì P3.** Khi đã hết P0/P1/P2, executor được tự quyết vá thêm để giảm P3,
**tối đa hai vòng vá thêm**. Dừng ngay nếu một vòng **không giảm số lớp P3** so với lượt trước (đếm lớp, không đếm biểu hiện, đúng
cách đếm của §8.3). Mỗi vòng thêm vẫn tính vào trần lời gọi Codex (`ADR-0052`) và trần vòng (`ADR-0048`), và
lượt Codex cho nó phải có lý do theo `ADR-0052` (cần xác minh lại bản vá). P3 còn lại ghi sổ nợ như nay.

## 4. Review tìm theo lớp

Reviewer khái quát mỗi biểu hiện thành một lớp nguyên nhân, rồi **quét mọi biểu hiện cùng lớp** trên candidate
trước khi báo; không báo từng lỗi riêng lẻ. Đây là CÁCH TÌM; cách GHI (slug, bảng lớp, tỷ lệ đóng lớp) đã có
ở §8.3 và không đổi.

## Hiệu lực — không hồi tố

Cùng luật land-OID của `ADR-0052`. Luật của ADR này áp cho một packet **khi và chỉ khi** blob đặc tả mà
`spec_hash` của lease trỏ tới có **đúng một** dòng khớp `^luat_push_va_dung_va: ADR-0054@([0-9a-f]{40})$`, và
OID `<L>` bắt được thoả ba phép đo của `ADR-0052` thay đường dẫn bằng
`docs/adr/0054-push-mot-lan-dung-va-theo-hang-va-review-theo-lop.md`. Thiếu dòng, hai dòng, phép đo sai hoặc
không đo được ⇒ luật cũ, fail-closed. Dạng dòng khai cần trích: `luat_push_va_dung_va: ADR-0054@<oid40>`.

Chính packet thi hành ADR này không có dòng khai (OID land chưa tồn tại khi đặc tả đóng băng), nên về hiệu lực
nó chịu luật cũ. Đặc tả của nó tự nhận áp dụng mục 1–3 theo tinh thần; đó là lựa chọn của packet, không phải
hiệu lực của luật này.

## Cưỡng chế

Ba luật trên: **không cổng nào cưỡng chế**. Không bộ đếm số lần đẩy (GitHub không giữ lịch sử đẩy theo nhánh ở
dạng một phiên đọc được qua MCP; reflog là cục bộ), không cổng đọc điều kiện dừng, và `luat_push_va_dung_va`
có **0** dòng trong `ops/lease_publish.py` và `.claude/dev/packet_loop.py` (đo 17-10-2026, `rg -cw`). Luật được
canh bằng kỷ luật đọc và bằng biên nhận. Cùng họ nợ `SO-CANON-CHUA-TON-TAI`.

## Protocol trỏ, không chép

`docs/PROTOCOL_DA_PHIEN.md` sửa ba dòng class của bảng ngưỡng §8, câu reviewer ở §8, thêm một câu vào §8.3, một
con trỏ ở §12 và dòng §20. Con số và cụm luật (một lần, hai vòng) chỉ ở **tệp này**.

ADR này **không** sửa `ADR-0037`, `ADR-0038`, `ADR-0041`, `ADR-0048`, `ADR-0052`, `ADR-0053` hay đặc tả đóng
băng nào.

## Nợ

- **`CONG-DEM-PUSH`** — cổng mã đếm số lần đẩy nhánh code và đọc biên nhận vá CI. Packet riêng (Q7 của đặc tả).
- **`R291-DAM-SO-CUNG`** — packet này là lần thứ **5** phải kê khai slot vì ratchet đếm cứng `docs/*.md`.
- Chưa có số đo tác động lên tốc độ hội tụ khi bỏ đường *"review trên PR head"*.
