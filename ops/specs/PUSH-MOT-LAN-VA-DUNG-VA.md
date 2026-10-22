# Đặc tả packet — PUSH-MOT-LAN-VA-DUNG-VA (revision 1)

- `packet_id`: **PUSH-MOT-LAN-VA-DUNG-VA**; ID bền `wp<packet_issue>`.
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp)**
- `revision`: **1** · `generation`: 1 · soạn **17:1xZ 16-10-2026**
- `depends_on`: **packet #782** (`TRAN-CODEX-VA-SENSITIVE`) — cùng sửa `docs/PROTOCOL_DA_PHIEN.md`; packet này
  chỉ được cấp lease và mọc trên `master` SAU khi #782 land.
- `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive** (đổi luật review, điều kiện dừng vá và đường push —
  tức review/land authority)

## `nguon_cap_viec`

Chỉ thị chủ kho `ducthangho` **16-10-2026**, trong phiên `session_01XaeBSkW4R49AEWj6x4uqff`, nguyên văn:

> "Ngoài ra tôi muốn bổ sung một số yêu cầu trong packet loop. Theo đó là sẽ không được push vào cho đến khi
> đủ điều kiện để merge. Làm sao để mỗi packet hoặc là WP thì chỉ push vào GitHub duy nhất một lần.
> Điều kiện để dừng vá là khi hết P1 và P2. Tùy trường hợp, bạn có thể vá thêm một vài vòng nếu thấy có khả
> năng làm giảm sâu số P3 còn lại, hoặc xóa hoặc giải quyết hết được các P3.
> cross review thì luôn tìm theo phân lớp, không tìm theo các lỗi riêng lẻ. Nếu những yêu cầu nào mà đã có
> sẵn thì hãy bỏ qua."

Sau đó chủ kho trả lời *"Đồng ý với các khuyến nghị"* cho Q1–Q8 dưới đây.

## Đối chiếu với thứ đã có (đo 17:1xZ 16-10-2026, trên `origin/master` @ `653fef3f`)

| yêu cầu | đã có ở đâu | phần còn thiếu |
|---|---|---|
| R1 — push một lần, khi đủ điều kiện merge | **Không có.** Gần nhất: `docs/PROTOCOL_DA_PHIEN.md:1085` (*"khi owner yêu cầu đợi tới đủ điều kiện merge, không chạy CI/fullCI giữa vòng vá"*), có điều kiện. Ngược lại `:713` cho Codex review *"trên exact PR head"*, tức giả định đã push | toàn bộ |
| R2 — dừng vá khi hết P1 và P2; vá thêm vì P3 tuỳ trường hợp | **Một phần.** Bảng `:619-622`: `systemic` đã đòi hết P2; `routine` cho giữ P2 kèm nợ; `sensitive` chỉ đòi hết P0 kèm quyết định từng finding. Không có luật vòng vá thêm vì P3 | siết `routine`/`sensitive`; luật vòng thêm |
| R3 — review tìm theo lớp | **Gần như đủ.** §8.3 (`:784-811`): mỗi finding một slug lớp, bảng lớp mỗi lượt, chỉ tính *đã vá* khi đóng cả lớp; `:537` gợi ý vá phải *"đóng lớp"* | một câu chỉ thị CÁCH TÌM: khái quát thành lớp rồi quét mọi biểu hiện cùng lớp trước khi báo |

## Quyết định đã chốt với chủ kho (16-10-2026)

| # | câu hỏi | quyết định |
|---|---|---|
| Q1 | "Push một lần" tính cho nhánh nào | **Chỉ nhánh code của packet.** Nhánh `ops/**` (lease, biên nhận), PR đặc tả là sổ sách, push như hiện nay |
| Q2 | CI đỏ sau lần push duy nhất | Trước push bắt buộc chạy đủ cổng tại chỗ (skill `gate`) trên đúng commit sẽ push. CI vẫn đỏ thì **được push vá chỉ để sửa CI**, mỗi lần ghi vào biên nhận kèm nguyên nhân; không dùng lần push ấy để vá thêm finding review |
| Q3 | Review ở đâu khi chưa push | Mọi vòng review chạy **offline** trên bundle/mirror (cơ chế đã có, `:655`, `:747`), neo **SHA commit cục bộ**; push đúng commit ấy nên *"exact head"* vẫn đúng mà không phải review lại. Connector Codex trên PR GitHub không dùng cho các vòng vá |
| Q4 | "Hết P1 và P2 mới dừng" áp class nào | **Mọi class.** `routine` không còn được giữ P2 dạng nợ; `sensitive` vẫn giữ thêm yêu cầu approval tường minh đúng assurance. P0 vẫn chặn ở mọi class |
| Q5 | Giới hạn vòng vá thêm vì P3 | Executor tự quyết, **tối đa 2 vòng thêm**, vẫn tính vào trần lời gọi Codex (`ADR-0052`) và trần vòng (`ADR-0048`). Dừng ngay nếu một vòng không giảm số **lớp** P3. P3 còn lại ghi sổ nợ như nay |
| Q6 | Thêm câu "quét theo lớp" | **Một câu** vào §8.3; không làm gì thêm |
| Q7 | Tài liệu hay mã | **Chỉ tài liệu** (ADR + protocol). Cổng mã đếm số lần push là packet riêng sau |
| Q8 | Gộp với #782 hay tách | **Tách**, làm sau khi #782 land |

## Số ADR

`0051` bị chiếm trên nhánh `claude/human-audited-khai-ai-dang-r1`; `0052`, `0053` thuộc packet #782. Quét mọi
`refs/remotes/origin/*` (đo 17:1xZ 16-10-2026): **không** nhánh nào có `docs/adr/0054-*`. Dùng **`0054`**. Đo lại
trước khi commit ADR; số đã bị chiếm thì DỪNG hỏi.

## `review_class` và ngưỡng

`sensitive`. Đặc tả này đóng băng **sau** mốc `ADR-0053` (2026-10-16) nên chịu trần **mới**: ≤ 6 tệp, ≤ 450 dòng
thêm. Nếu #782 chưa land khi cấp lease thì `ADR-0053` chưa có trên `master` — khi ấy DỪNG, không cấp lease
(xem `depends_on`). Write set **2** tệp, ước lượng ~150–220 dòng thêm.

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `docs/adr/0054-push-mot-lan-dung-va-theo-hang-va-review-theo-lop.md` | ADR mới — R1, R2, R3 |
| 2 | `docs/PROTOCOL_DA_PHIEN.md` | bảng ngưỡng §8 (Q4); câu `:713` về review trên PR head (Q3); §8.3 thêm một câu (Q6); §12 luật vòng thêm (Q5) và push (Q1, Q2); §20 thêm dòng `0054` |

Không ký tự đại diện. Đo `ai-dang-giu` cho cả hai đường dẫn TRƯỚC khi cấp lease (lúc soạn, `docs/PROTOCOL_DA_PHIEN.md`
đang bị lease của #782 giữ — đúng lý do của `depends_on`).

## `ngoai_pham_vi`

1. **KHÔNG cổng mã** đếm số lần push hay cưỡng chế điều kiện dừng (Q7). Ghi nợ có tên.
2. **KHÔNG sửa adapter** (`.claude/skills/*`, `.agents/skills/*`): adapter TRỎ protocol, không chép luật;
   `doctrine-scan` chặn chép. Nếu đo ra một adapter MÔ TẢ push giữa vòng vá thì đó là phát hiện — DỪNG hỏi, đừng
   tự mở rộng write set. Đo lúc soạn: `rg -n -i "push|rereview" .claude/skills/{work-packet,cross-review,land-packets}/SKILL.md .agents/skills/*/SKILL.md AGENTS.md`
   ⇒ chỉ hai dòng liệt kê thao tác CẤM (`AGENTS.md:95`, `work-packet/SKILL.md:193`), không dòng nào mô tả push giữa vòng.
3. **KHÔNG đổi** trần lời gọi (`ADR-0052`), trần vòng (`ADR-0048`), trần kích thước (`ADR-0053`).
4. **KHÔNG hồi tố**: neo `spec_hash` đóng băng, như `ADR-0048`/`0052`/`0053`.
5. **KHÔNG sửa** `ADR-0037`/`0038`/`0041` hay đặc tả đóng băng nào.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | `ADR-0054` khai luật push một lần cho nhánh code packet (Q1), điều kiện trước push (Q2), ngoại lệ push chỉ-vá-CI có ghi biên nhận (Q2) | #1 |
| M2 | `ADR-0054` khai review offline neo SHA cục bộ, push đúng SHA đã review (Q3) | #1 |
| M3 | `ADR-0054` khai điều kiện dừng vá: hết P0/P1/P2 ở mọi class (Q4); luật tối đa 2 vòng thêm vì P3 và điều kiện dừng sớm (Q5) | #1 |
| M4 | Protocol: bảng ngưỡng §8 khớp Q4; câu `:713` không còn giả định review trên PR head đã push; §8.3 có câu quét theo lớp (Q6); §20 có dòng `0054` | #2 |
| M5 | `ADR-0054` khai không hồi tố và **không cổng nào cưỡng chế** (Q7) | #1 |

## `nghiem_thu`

**A1 (M4) — `adr-song` xanh**, số ADR trên đĩa bằng số dòng §20. **Đỏ khi:** bỏ dòng `0054` ở §20.

**A2 (M3, M4) — bảng ngưỡng không còn cho giữ P2.** `rg -n "P2/P3 còn lại phải có nợ" docs/PROTOCOL_DA_PHIEN.md`
⇒ **0** dòng. **Đỏ khi:** dòng `routine` cũ còn nguyên.

**A3 (M2, M4) — không còn câu giả định review trên PR đã push.** Đọc §8 quanh câu *"Reviewer read-only trên exact
PR head"*: phải nói review trên SHA cục bộ trước push. **Đỏ khi:** còn *"exact PR head"* làm điều kiện cho vòng vá.

**A4 (M1) — luật push đọc ra đúng MỘT câu trả lời** cho bốn ca: (a) đẩy nhánh code lần đầu khi đủ điều kiện ⇒ được;
(b) đẩy nhánh code giữa vòng vá ⇒ không; (c) CI đỏ sau lần đẩy, vá CI ⇒ được, phải ghi biên nhận; (d) đẩy nhánh
`ops/**` lease ⇒ ngoài luật. **Đỏ khi:** một ca có hai cách đọc.

**A5 (M3) — luật vòng P3 có điểm dừng đo được.** ADR nêu trần 2 vòng thêm VÀ điều kiện *"không giảm số lớp P3 ⇒
dừng"*. **Đỏ khi:** thiếu một trong hai (vòng thêm thành không giới hạn).

**A6 (M5) — lời khai cưỡng chế đúng mức.** ADR nói rõ không cổng nào đếm push hay canh điều kiện dừng. **Đỏ khi:**
ADR khai một cổng mà `rg` không tìm ra.

**A7 — trần `ADR-0053`.** `git diff --numstat` ⇒ đúng **2** đường dẫn, tổng thêm ≤ **450**.

**A8 — `doctrine-scan` xanh.**

**Điều kiện dừng:** `sensitive` ⇒ cross-review khác nền `approve` tường minh (hoặc `human_audited`). Chính packet
này áp luật của nó theo tinh thần (push một lần) dù luật chưa có hiệu lực khi đặc tả đóng băng.

## `hinh_dang_ke_thua`

`khong_ap_dung` — không phải packet khắc phục.

## `chua_do_duoc`

1. **Không đo được** số lần push của một nhánh từ trong kho: GitHub không giữ lịch sử push theo nhánh ở dạng
   phiên này đọc được qua MCP; reflog là cục bộ. Đây là lý do Q7 chọn tài liệu trước.
2. **Không đo được** việc review offline có bắt được mọi thứ CI bắt không — Q2 thừa nhận bằng ngoại lệ vá CI.
3. Tác động lên tốc độ hội tụ của bỏ đường *"review trên PR head"*: chưa có số đo.
