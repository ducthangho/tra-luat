# Thẩm định "vòng lặp tri thức" — bản hợp nhất 3 vòng × 3 bên (21-08-2026)

**Câu hỏi của người giữ kho:** kho có tính năng nào lưu log/kiến thức/bài học trong lúc build kế hoạch
không, và có nên chuẩn hoá — tất định hoá nó thành một tính năng của Kế hoạch không?

**Ba bên:** phiên chính (Opus 5) · codex (GPT-5, `model_reasoning_effort=max`) · Fable 5.
**Ba vòng**, mỗi vòng neo prompt theo băm, chạy trên worktree chỉ-đọc tại `origin/master` = `0333948`.

| vòng | đề bài | băm prompt | codex | Fable |
|---|---|---|---|---|
| 1 | `DE_BAI.md` | `8b4690a0…` | run `5f124269`, rc=0 | task vòng 1 |
| 2 | `DE_BAI_V2.md` | `3602eafe…` | run `75644324`, rc=0 | task vòng 2 |
| 3 | `DE_BAI_V3.md` | `23cb6d57…` | run `838809f8`, rc=0 | task vòng 3 |

---

## 1. Câu trả lời cho câu hỏi gốc: KHÔNG nên tất định hoá việc LƯU

Kho hiện có **7 chỗ đựng tri thức** (CLAUDE.md 160 dòng "Bài học đắt giá" · `ops/NO_KY_THUAT.md` 481 dòng ·
45 ADR · 24 receipt · 24 verdict · CHANGELOG 7.648 dòng · `TONG_HOP_*`). Đề xuất ban đầu của phiên chính là
chuẩn hoá việc GHI vào các chỗ ấy. **Cả hai bên độc lập bác bỏ khung đó**, và bác theo cùng một hướng:

> codex: *"nút thắt là kích hoạt đúng phép kiểm tại đúng quyết định"*
> Fable: *"vấn đề không phải LƯU, không phải TRUY XUẤT, mà là DẠNG TỒN TẠI"*

Bằng chứng quyết định là ba ca tái phát có thật của kho:
- **Ca 1** (bẫy `$?` sau pipeline, 3 lần/1 ngày): cả ba bên **đã đọc** bài học ⇒ không phải lỗi lưu, không
  phải lỗi truy xuất.
- **Ca 2** (ratchet/manifest trong `tl_selftest.py`): bài học nằm **cách vài chục dòng trong chính tệp đang
  sửa** ⇒ truy xuất hoàn hảo, vẫn tái phát. Đây là phản chứng chết người cho mọi đề án "đưa bài học tới
  đúng lúc".
- **Ca 3** (kế hoạch nằm trên PR chưa merge): lỗi lớp XUẤT BẢN, không phải lớp bài học.

⇒ **Tất định hoá việc LƯU giải quyết 0/3 ca.** Thứ giải được là biến bài học thành **phép kiểm chạy tại
điểm chuyển trạng thái** — đúng doctrine kho đã tự viết ("nghĩ ra phép thử mà không chạy thì phép thử ấy
không tồn tại"), và đề bài này là bằng chứng kho chưa tuân doctrine của chính mình.

## 2. Ba đề xuất ban đầu của phiên chính — hai bị bác, một sống sót đã đổi hình

| cạnh đề xuất | phán quyết | lý do (cả hai bên độc lập) |
|---|---|---|
| (1) kế thừa `hinh_dang_lap` + cổng `dem>=3` | **BÁC** | số TỰ KHAI; lách bằng cách đặt tên hình dạng khác; cổng chỉ kiểm SỰ CÓ MẶT của khối `quyet_dinh_kien_truc` — đúng lỗi kho đã trả giá 4 lần; thêm một điểm merge |
| (2) `doi_ke_hoach.can` + chặn packet cùng seam | **BÁC** | `seam` = **0/24** receipt, **0/41** lease ⇒ vị từ KHÔNG máy-đọc-được ⇒ cổng GIẢ. Và `can:true` + MCR chờ người ⇒ dạy người ta khai `can:false`, tức dạy IM LẶNG |
| (3) `rXX_` hoặc `chi_la_chu: true` | **ĐỔI HÌNH** | phần schema "cấm im lặng" giữ lại; riêng giá trị `chi_la_chu: true` là **CHỈ LÀ CHỮ** — 0 occurrence toàn kho, không phép đo nào làm nó ĐỎ. Fable **rút chữ ký vòng 1 của chính mình** ở vòng 2 |

Cùng bị bác bởi cả hai bên, cả ba vòng: chỗ đựng tri thức **thứ 8** · knowledge graph/vector DB · bộ phân
loại LLM "cùng hình dạng" · auto-MCR · hook in hàng loạt lời nhắc theo cò.

## 3. PHÉP ĐO QUYẾT ĐỊNH — không vòng nào chạy nó, phiên chính chạy sau vòng 1

Hậu kiểm trên cây hiện tại: 18/41 lease trích tài liệu ngoài `prompt_path`; số trích dẫn **không** resolve
được từ `origin/master` = **0**. Nhìn qua tưởng "không có bệnh". **Sai** — vì đó là đo TRẠNG THÁI CUỐI.

Đo lại tại **thời điểm cấp lease**:

| vật | lên master lúc | lease trích nó cấp lúc | lệch |
|---|---|---|---|
| `ops/specs/plat-m4-v0.md` | `d27337b` **03:58:21Z** | `plat-m4-exec-2-claude` **02:05Z** | **−1h53m** |
| (nt) | (nt) | `plat-m4-review-2-codex` **02:30Z** | **−1h28m** |

⇒ Cổng "tài liệu lease trích phải resolve từ ref bền" **ĐỎ ĐÚNG HAI LẦN NÓ CẦN ĐỎ**; xanh hôm nay chỉ vì
lịch sử đã đuổi kịp. Đây chính là ca đã **làm hỏng một lượt review thật**. Bài học ấy hiện là VĂN XUÔI.

**Hệ quả thiết kế:** cổng phải chạy ở ĐIỂM CHUYỂN TRẠNG THÁI, không phải hậu kiểm trên cây hiện tại. Hậu
kiểm cho 0/0 rồi kết luận "không có bệnh" — đúng lỗi "hỏi chỗ tiện tay thay vì hỏi chỗ kết luận được ghi".

## 4. Thứ THẬT SỰ phải làm trước: hình dạng lỗi thứ tư đã vượt ngưỡng

Trong 3 ngày, **4 lượt review bị hỏng vì cách PHIÊN CHÍNH dựng sandbox/bundle bằng tay** — không lần nào
do reviewer:

| # | sự cố | hậu quả |
|---|---|---|
| 1 | prompt trỏ `ops/specs/plat-m4-v0.md`, cây reviewer không có tệp đó | lượt review chạy trên đề bài thủng |
| 2 | bundle thiếu lease X4 review-2 | codex ra finding A5 SAI — do bundle, không do codex |
| 3 | `\| tail` nuốt mã thoát khi đo cổng | đo sai, lần thứ ba của cùng bẫy trong một ngày |
| 4 | `codex exec -s read-only` ⇒ reviewer không ghi được báo cáo | vòng 1 của chính đợt này, báo cáo phải in vào stdout |

Luật của kho: **cùng hình dạng ≥3 lần ⇒ câu hỏi đúng không còn là "vá thế nào" mà là "có nên làm việc này
nữa không"**. Ngưỡng đã vượt ở 4. **Cả codex lẫn Fable, ở vòng 2, độc lập kết luận: CẤM dựng sandbox
reviewer bằng tay, và việc này đi TRƯỚC mọi cạnh khác.** Cả hai bên đều **ĐỔI Ý** so với vòng 1 để tới đây.

## 5. CHỐT SAU VÒNG 3 — hai bên hội tụ hoàn toàn về thiết kế

**Packet 1 = `packet_loop review-run`, có răng ngay từ lát 1.**

| hạng mục | chốt | ai đổi ý |
|---|---|---|
| có đụng review authority không | **CÓ** — `record-review` là ĐÚNG MỘT ĐƯỜNG vào `accepted` (`packet_loop.py:871`), và kho ĐÃ có finding `review-transition-bypasses-record-review` về việc vòng qua nó | Fable đổi ý theo codex ở vòng 3 |
| phân loại | **`sensitive`** — ≤3 tệp, **≤300 dòng thêm** (ADR-0044) | Fable rút phương án `systemic` của chính mình |
| ở đâu | `.claude/dev/packet_loop.py` + `packet_loop_test.py` (+ `cross-review/SKILL.md` ở lát sau) | Fable rút tệp standalone `ops/dung_sandbox_review.py` |
| răng | `cmd_record_review` **TỪ CHỐI mọi lượt thiếu receipt hợp lệ NGAY TỪ LÁT 1** — không phải "script tuỳ chọn, siết sau" | cả hai cùng ký, cùng đưa "tuỳ chọn" vào `TOI_KHONG_KY` |

**Bốn check, mỗi check neo một sự cố THẬT, mỗi check một đột biến làm ca đích ĐỎ:**

| check | neo sự cố | đột biến |
|---|---|---|
| a. tự sinh diff `base_sha..reviewed_sha`, CẤM nhận bundle ghép tay | #2 thiếu lát X4 | nhận diff truyền vào ⇒ ca `incomplete-bundle-x4` ĐỎ |
| b. neo trích dẫn: mọi `(path, sha256)` phải resolve trong bundle, đúng băm | #1 prompt trỏ tệp không có | bỏ so băm ⇒ ca `missing-cited-spec` ĐỎ |
| c. rc trực tiếp: subprocess argv, đọc `returncode`, cấm pipeline | #3 `\| tail` nuốt rc | ép mã con = 0 ⇒ ca `child-rc-preserved` ĐỎ |
| d. thăm dò GHI đích báo cáo TRƯỚC khi tiêu lời gọi model | #4 `-s read-only` | bỏ probe ⇒ ca `unwritable-output-stops-before-model` ĐỎ |
| **e. receipt gate** ở `record-review` (dây nối, không phải check thứ 5) | vòng-qua-cửa (finding lượt 6) | nới nhận thiếu receipt ⇒ ca `record-review-without-receipt` ĐỎ |

**BỎ, có tên:** "head không đổi sau chạy" (không neo được sự cố nào; `record-review` đã kiểm `reviewed_sha`)
· "prompt resolve từ ref bền tại lúc cấp" — **đã đo là báo động giả CẤU TRÚC**: `ops-publish-lease.yml`
đọc `prompt_path` từ **head được đẩy** (`--root .`), nên đòi prompt trên master là chặn oan. **SPEC thì
khác** — spec phải đóng băng TRƯỚC lease, nên spec-gate là hợp lệ.

**Không lọt +300 ⇒ cắt hai lát, lát 1 vẫn có răng:**
- **Lát 1** (`sensitive`, 2 tệp): check **c + d + e**. Chặn 2/4 sự cố (#3, #4) + đóng lớp vòng-qua-cửa.
  Hai check còn lại khai `KHÔNG ĐO ĐƯỢC` **trong schema receipt ngay từ lát 1** — trạng thái ba có mặt từ
  đầu, không nới sau rồi siết lại.
- **Lát 2** (nối tiếp): check **a + b** + đủ 4 fixture sự cố + adapter `cross-review/SKILL.md`.
- *(Khác biệt còn lại duy nhất giữa hai bên: Fable xếp `a` vào lát 1, codex xếp `d`. Phiên chính chọn theo
  codex — `d` là ~10 dòng, `a` đòi dựng bundle closure; dưới trần cứng +300 thì `d` mua được nhiều hơn.)*

## 6. Thứ tự thi công — cả hai bên đồng ý, và nó ĐO ĐƯỢC

- **Slice A ĐÃ LAND** (`t36`–`t40` có trong `ops/lease_publish_test.py`, bộ 41 ca).
- **Slice B gần xong**: `t25`/`t34`/`t35` đã có; phần còn lại DUY NHẤT là **mục C** (2 mục sổ nợ +
  hạ lời khai `t34` + ca máy đòi docstring).
- **Mục C ghi vào `ops/lease_publish_test.py`** ⇒ **GIAO write set** với gói spec-gate.

⇒ **Mở SONG SONG: Packet 1 (`packet_loop`) ∥ mục C (`lease_publish*`)** — write set rời nhau hoàn toàn.
**Gói spec-gate** (`spec_path` + `spec_sha256` + resolve từ ref bền, `rc=6`) **NỐI TIẾP ngay sau khi C
land** — mở song song với C là tái tạo đúng hình dạng chuỗi `#203→#206` mà ADR-0044 sinh ra để chặn.

## 7. `plan_impact` thay cho `doi_ke_hoach.can` — cả hai bên chốt, thuộc gói V4

```yaml
plan_impact: none | packet_revision | mcr_candidate | new_mission
decision_by: <actor>
decision_ref: <durable-ref>
reason: <text>
impact_ref: <packet-revision | mcr-id | mission-id | null>
```
Máy kiểm được **HẬU QUẢ**, không kiểm phán đoán: `packet_revision` ⇒ revision mới tồn tại + lease cũ bị thu
hồi · `mcr_candidate` ⇒ MCR tồn tại + phần bị pause · `new_mission` ⇒ liên kết supersede · `none` ⇒ đòi
người quyết + lý do + dấu vết. Việc CHỌN giá trị enum là **CHỈ LÀ CHỮ** có người chịu trách nhiệm — khai
thẳng, đừng đặt tên to hơn phạm vi đo được.

## 8. Ba chỗ đề bài của phiên chính SAI, codex sửa, phiên chính đã kiểm và nhận

| đề bài ghi | đúng là |
|---|---|
| khối "Bài học đắt giá" 161 dòng | **160** dòng kể tiêu đề |
| — | `verdict_usage_caveats` chỉ có ở **14/24** receipt |
| "0 cổng máy đòi bất kỳ chỗ đựng nào" | **SAI**. `t26`/`t27` CÓ cưỡng chế receipt↔verdict↔băm và nâng caveat lên mục lục. Câu đúng và hẹp hơn: **0 cổng đòi một BÀI HỌC phải được khai** |

## 9. Việc CÒN LẠI của kế hoạch A–F (đo 21-08-2026)

| | việc | trạng thái |
|---|---|---|
| A | hợp nhất bản thẩm định + hồ sơ `plat-m4` lên master | **XONG** (#210, #212 đã land) |
| B | PLAT-M4 `#194` | **gần xong** — head `825e970`, 0 sau master, gate **xanh cả ubuntu lẫn windows**, 0 bước lỗi; chỉ thiếu **verdict vòng 3** (trần vòng 2→3 người giữ đã duyệt) |
| C | 2 mục sổ nợ + hạ lời khai `t34` + ca docstring | **chưa bắt đầu** — đo: `PLAT-X5-required-status-check` = **0** dòng trong `NO_KY_THUAT.md`, mà `ci.yml` có **2** marker "NỢ CÓ TÊN" |
| D | gói cưỡng chế `lease_publish` | **chưa bắt đầu** — `spec_sha256`/`cross_provider`/`cat-file` = **0** trong `lease_publish.py`. **Nội dung D nay do bản thẩm định này định lại** (mục 5–6) |
| E | script dựng sandbox reviewer | **chưa bắt đầu** — nay là **Packet 1**, và cả hai bên xếp nó ĐI TRƯỚC |
| F | đồng bộ câu "trần vòng" | **chưa bắt đầu** — còn **1** chỗ "ba vòng" ở `docs/PROTOCOL_DA_PHIEN.md:751` |

## 10. Khai thẳng — thứ KHÔNG đo được

- Số dòng thêm THẬT của lát 1 (260–340 là ƯỚC; chỉ `git diff --numstat` lúc thi công mới là phép đo —
  trần cứng `+300` trong spec là chốt THAY cho ước lượng).
- Có cưỡng chế được closed-read scope ở tầng OS không ⇒ receipt phải khai `read_scope_enforced: false`,
  không được tự nâng thành bảo đảm.
- `record-review` đòi receipt từ ngày land có chặn oan lượt review đang DỞ không — phải kiểm state files
  lúc thi công.
- Fetch được `luu-tru/*` lúc chạy check neo không (thuộc gói spec-gate).
- Hiệu quả HÀNH VI của mọi lớp văn xuôi — **không có baseline**, và cả ba vòng đều khai điều này.
- Chi phí giờ-người của 4 lượt review hỏng — chỉ có lời kể, chưa có số.

## 11. Nguồn có thẩm quyền

Tệp này là bản HỢP NHẤT. Sáu báo cáo gốc và ba đề bài neo băm nằm **TRONG KHO**, cạnh nó:

```
ops/tham-dinh/tri-thuc-20260821/
  codex-vong{1,2,3}.md · fable-vong{1,2,3}.md
  de-bai-vong{1,2,3}.md · do-doc-lap-v1.md · BAM.txt
```

Vì sao chúng phải nằm trong kho chứ không ở thư mục phiên — và vì sao bản nháp đầu của chính
tệp này ghi SAI chỗ đó: bài học §3 của tệp này đo được rằng một tài liệu chỉ tồn tại ngoài
ref bền thì con băm trỏ tới nó là **niềm tin viết dưới dạng hex**, không kiểm được. Kho đã trả
giá đúng thế một lần (lease wp55 ghi `prompt_sha256_required` mà không nói băm cái gì ⇒ đứng
im hai ngày). Thư mục phiên bị thu hồi khi container hết hạn; nếu để nguồn ở đó thì mọi băm
trong tệp này thành con trỏ hỏng — đúng cái bệnh mà bản thẩm định này sinh ra để chữa.
`BAM.txt` là bảng băm đo tại chỗ; đối chiếu bằng `sha256sum -c BAM.txt`.
