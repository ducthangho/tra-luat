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
- review đã approve trên chính SHA ấy, với đúng assurance mà Review Class và đặc tả packet đòi theo §8 của
  protocol (mục 2). ADR này **không** nâng yêu cầu assurance: packet được phép `same_provider_approved` hay
  `human_audited` theo §8 vẫn được phép như cũ.

Lý do đo được: packet #782 đẩy lần đầu sau ba cổng tài liệu xanh nhưng **không** chạy selftest, và CI đỏ
`1730/1731` ở ca `r291_docs_ngoai_goi` (run `38945289558`). Một lần đẩy hỏng kéo theo revision đặc tả, lease
mới và vòng review mới.

**Ngoại lệ duy nhất: CI đỏ sau lần đẩy.** Executor được đẩy thêm **chỉ để sửa CI**. Commit vá đổi `head_sha`,
nên mọi verdict của SHA cũ hết hiệu lực (§7 của protocol): **trước khi đẩy**, commit vá phải qua review offline
trên chính SHA mới (lượt xác minh lại bản vá theo `ADR-0052`) và chạy lại đủ cổng tại chỗ của mục này. Mỗi lần
như vậy **ghi vào biên nhận** của packet: SHA trước/sau, check đỏ, nguyên nhân, vì sao cổng tại chỗ không bắt
được, verdict của SHA mới. Lần đẩy vá CI không được mang thêm bản vá cho finding review; finding mới phát hiện
thì đi mục 2.

**Phạm vi.** Luật chỉ áp cho nhánh code của packet (`agent/wp<issue>-g<generation>-<executor>`). Nhánh
`ops/**` (lease, bia mộ, biên nhận) và nhánh đặc tả là sổ sách, đẩy như trước, ngoài luật này.

Bốn ca, mỗi ca một câu trả lời:

| ca | được đẩy? |
|---|---|
| nhánh code, lần đầu, khi đã đủ điều kiện | được |
| nhánh code, giữa các vòng vá | không |
| nhánh code, CI đỏ sau lần đẩy, bản vá chỉ sửa CI | được, sau khi SHA mới được approve; ghi vào biên nhận |
| nhánh `ops/**` hoặc nhánh đặc tả | ngoài luật này |

## 2. Review offline, neo SHA commit cục bộ

Vì nhánh code chưa đẩy trong lúc vá, mọi vòng review chạy **offline** trên bundle/mirror dựng từ commit cục bộ
(cơ chế đã có ở §8 của protocol), neo SHA commit cục bộ. Verdict nêu SHA ấy và `spec_sha256` của đặc tả. Lần
đẩy duy nhất đẩy **đúng** SHA đã được approve, nên điều kiện *"exact SHA"* vẫn đúng mà không phải review lại.

**Ánh xạ các bước protocol vốn giả định đã có PR.** Với packet áp ADR này, trước lần đẩy chưa có nhánh từ xa
và chưa có PR. Bốn chỗ của protocol đọc như sau, và mỗi chỗ có con trỏ về đây:

| chỗ trong protocol | đọc trước lần đẩy |
|---|---|
| §7: handoff/evidence lên Packet Issue **và PR** | chỉ lên Packet Issue |
| §7: reconciler đọc lại **PR head** rồi so các trường | đọc SHA ứng viên cục bộ ghi trong handoff và bundle; so đủ các trường như cũ (spec hash, generation, lease, `head_sha`, `tested_sha`, changed paths, gate policy) |
| §13 `work-packet`: worker gate → **PR** → handoff | worker gate → handoff → review → đẩy → PR |
| §13 `cross-review`: trigger khi **PR** vào `reviewing`; hoàn tất khi verdict ghi **vào PR** | trigger khi Packet vào `reviewing` với SHA ứng viên; verdict ghi vào biên nhận và Packet Issue, chép sang PR sau lần đẩy |

Không bước nào bị bỏ: mỏ neo đổi từ PR head sang SHA ứng viên, mọi phép so giữ nguyên. Executor vẫn không tự
tạo review có thẩm quyền. Sau lần đẩy, PR head phải **bằng** SHA đã được approve; khác SHA thì verdict cũ hết
hiệu lực như quy tắc commit mới của §7.

**Hoàn tất `work-packet` và run kế nhiệm.** Với packet áp ADR này, `work-packet` hoàn tất khi SHA đã approve được
đẩy và PR đã mở, không phải khi handoff được nhận. Handoff phải kèm bundle của SHA ứng viên ở nơi lưu evidence bền
(cùng bundle reviewer đã đọc), vì đường phục hồi nguội của §7 phải tự sống được. Run executor kết thúc trước khi
đẩy (hết giờ, chết, hay chỉ giao handoff rồi dừng) thì reconciler giao một **run kế nhiệm cùng generation, cùng
lease**. Run ấy chỉ làm đúng ba việc: kiểm SHA trong bundle bằng SHA đã approve, đẩy SHA ấy, mở PR. Không sửa gì
khác; lệch SHA thì dừng.

**Finding của connector sau lần đẩy.** Connector review trên PR GitHub chạy sau lần đẩy. Nó **không** mở vòng
vá tự động: nếu nó báo P0/P1/P2 trên head đã đẩy, executor DỪNG và đưa checkpoint cho chủ kho kèm phép đo. Lúc ấy
packet đã `accepted` theo verdict offline, mà `accepted` là trạng thái cuối của máy trạng thái (§4 của protocol;
`.claude/dev/packet_loop.py` không có cạnh đi ra). Nếu chủ kho cho vá, đường đi là **generation mới** theo luật
reroute của §12: `accepted` của generation cũ hết hiệu lực; generation mới có nhánh mới, lease mới, vòng review
offline mới, rồi lại đẩy theo mục 1. Đẩy tiếp lên nhánh của generation cũ không phải ngoại lệ vá CI và không được
làm.

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
dạng một phiên đọc được qua MCP; reflog là cục bộ), không cổng đọc điều kiện dừng. Đo 17-10-2026 bằng
`rg -cw 'luat_push_va_dung_va|ADR-0054'` trên đủ sáu vị trí cổng mà §20 của protocol liệt kê
(`ops/lease_publish.py`, `.claude/dev/packet_loop.py`, `.claude/dev/launcher.py`, `.claude/dev/gate_lifecycle.py`,
`.github/workflows/ci.yml`, `.github/workflows/ops-publish-lease.yml`): **0** dòng ở mỗi tệp. Luật được
canh bằng kỷ luật đọc và bằng biên nhận. Cùng họ nợ `SO-CANON-CHUA-TON-TAI`.

## Protocol trỏ, không chép

`docs/PROTOCOL_DA_PHIEN.md` sửa ba dòng class của bảng ngưỡng §8, câu reviewer ở §8, thêm một câu vào §8.3, một
con trỏ ở §12, bốn con trỏ ánh xạ ở §7 và §13, và dòng §20. **Mọi** chỗ ấy nói rõ chỉ áp cho packet áp ADR này;
packet chưa áp giữ nguyên luật cũ, đúng mục *Hiệu lực*. Con số và cụm luật (một lần, hai vòng) chỉ ở **tệp này**.

ADR này **không** sửa `ADR-0037`, `ADR-0038`, `ADR-0041`, `ADR-0048`, `ADR-0052`, `ADR-0053` hay đặc tả đóng
băng nào.

## Nợ

- **`CONG-DEM-PUSH`** — cổng mã đếm số lần đẩy nhánh code và đọc biên nhận vá CI. Packet riêng (Q7 của đặc tả).
- **`R291-DAM-SO-CUNG`** — packet này là lần thứ **5** phải kê khai slot vì ratchet đếm cứng `docs/*.md`.
- **`ACCEPTED-KHONG-CO-DUONG-RA`** — `packet_loop.py` không có lệnh đưa packet `accepted` sang generation mới; đường
  ở mục 2 đi bằng quyết định chủ kho, lease mới và biên nhận, chưa có máy canh.
- Chưa có số đo tác động lên tốc độ hội tụ khi bỏ đường *"review trên PR head"*.
