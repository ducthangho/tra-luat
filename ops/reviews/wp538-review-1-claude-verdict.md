---
verdict: changes_requested
reviewed_sha: f2aa1f9fd0dc0d7914c2f5ce34563f60fdec3f72
so_p1: 0
so_p2: 1
so_p3: 1
so_the_hien: 2
---

# Cross-review WP538 — claude review codex (`cross_approved`)

TỆP NÀY GHI TĂNG DẦN, tạo TRƯỚC phép đo đầu tiên. Nếu lượt chết giữa chừng, phần đã ghi vẫn đọc được.

## XUNG ĐỘT LỢI ÍCH — khai TRƯỚC khi đo gì

Reviewer là **phiên claude đang điều phối**, không phải một tiến trình claude riêng. Lý do đo được,
không phải tiện tay:

- `launcher.py doctor` ⇒ `rc=12`, `CHUA_XAC_THUC claude — khong co ~/.claude/.credentials.json va
  khong co bien`.
- Không có `ANTHROPIC_API_KEY`, không có `ANTHROPIC_AUTH_TOKEN`.
- Phép đo THẬT, không đọc cấu hình: gọi `claude --print --output-format json` ⇒ `rc=1` và
  **`duration_api_ms: 0`** — CLI chạy nhưng **không gọi API lần nào**.

⇒ KHÔNG phóng được phiên claude độc lập trong container này.

**Cái này ĐỘC LẬP:** diff WP538 do **codex** viết. Reviewer là **claude**. Khác provider thật, đúng
`§8` dòng 507 (*"`cross_approved`: Claude review Codex"*). Context reviewer KHÔNG fork từ executor —
hai nền khác nhau, hai phiên khác nhau.

**Cái này KHÔNG độc lập, và tôi khai thẳng:** chính phiên này soạn `spec r3` và ghi hộ `lease g3`.
Hai thứ ấy đổi **đúng hai trường** (`Reviewer`, `Assurance target`) và **không** đổi tiêu chí nghiệm
thu của mã WP538 — tiêu chí ấy do r2 đặt và r3 giữ nguyên. Nhưng người đọc phải biết để tự trừ hao.

**Checkout riêng:** mirror bare 428 ref (`is-shallow=false`, `core.abbrev 7`) + cây detached tại
`f2aa1f9f`, `status --porcelain` rỗng. Tập ref hai nguồn: `comm -23` **rỗng** ⇒ không mù.

## PHẠM VI ĐO

`immutable_acceptance_baseline` = `c66415aa` (từ lease). Delta: **11 tệp, +1248 −64**.

## ỨNG VIÊN ĐÃ TAN KHI ĐO — ghi ra để không tố oan

`ops/specs/wp538-skill-preflight-review-land-r1.md` (+143) KHÔNG có trong `write_set` của lease
**r2/g2** ⇒ thoạt nhìn là đường ngoài phạm vi. Đo tiếp: nó **CÓ** trong `write_set` của lease
**r1/g1**, và được tạo ở commit `fb9c784` — chính `start_from_sha` của r1/g1. Tức nó được viết dưới
một lease hợp lệ **tại thời điểm ấy**. **KHÔNG phải vi phạm.**

## CỔNG — chạy trên chính cây ứng viên, `rc` đọc TRỰC TIẾP

| cổng | rc | bằng chứng DƯƠNG |
|---|---:|---|
| `doctrine-scan` | **0** | — |
| `adr-song` | **0** | 48 ADR trên đĩa / 48 dòng §20, khớp 1–1 |
| `doc-claims-check --strict` | **0** | `core.abbrev=7` |
| `bien_nhan_v2` | **0** | TỔNG: ĐẠT |
| `git diff --check` | **0** | — |
| `release-verify --strict` | **0** | `ok=true`, `expected == checked == 180` |

## BẢNG SĂN — sáu hướng, mỗi hướng có lệnh + kết quả thật

| # | hướng | kết quả | phán |
|---|---|---|---|
| H1 | hai bản skill `.claude/` và `.agents/` có trôi lệch không | `.claude`=582/236/124 dòng · `.agents`=86/99/52 | **SẠCH** — `.agents` tự khai *"Nguồn cú pháp: [.claude adapter]"*, tức CON TRỎ, không phải bản sao. Chênh độ dài là ĐÚNG THIẾT KẾ |
| H2 | ngưỡng `ADR-0044` | **7 tệp / +772** so trần `≤3 / ≤300` | **LỆCH** — xem `PHÁT HIỆN 1` |
| H3 | bản viết lại protocol có làm MẤT nghĩa vụ nào không | ba dòng §8 bị `-` trong diff | **SẠCH** — đo hai đầu: định nghĩa được VIẾT LẠI MẠNH HƠN (`cross_approved` thêm *"là cặp khác provider"*; `same_provider_approved` thêm điều kiện fallback), dòng khoá *"không thay `cross_approved` cho class `sensitive`"* **SỐNG SÓT** (base:580 → head:640), và câu *"không giả thành cross-review"* sống ở dạng viết lại (head:1058 *"không giả thành cross-provider"*) |
| H4 | `ops/reviews/wp538/` trong write_set có hiện vật không | không tồn tại trên **bất kỳ ref nào** | **LỆCH** — xem `PHÁT HIỆN 2` |
| H5 | skill có thật sự giao `R15` không | `.claude` nhắc `§8` **38** lần, `.agents` **7** lần; `cross_approved`/`same_provider` xuất hiện **0** lần trong cả hai | **SẠCH** — và đây là chỗ tôi SUÝT TỐ OAN: grep đầu của tôi tìm cụm *"khác provider"* ⇒ 0 hit, đọc như thiếu. Đo lại theo KHÁI NIỆM thì adapter **TRỎ §8** thay vì chép lại — đúng thiết kế mà `doctrine-scan` cưỡng chế, và cổng ấy `rc=0`. Adapter chép luật mới là lỗi, không phải adapter trỏ luật |
| H6 | đường nào ngoài write_set | 11 đường đổi, 1 đường không thuộc write_set r2/g2 | **SẠCH** — `…-r1.md` CÓ trong write_set của **r1/g1** và tạo ở `fb9c784` (`start_from_sha` của r1/g1) ⇒ viết dưới lease hợp lệ tại thời điểm ấy |

## PHÁT HIỆN

### 1. `adr-0044-khai-ngoai-le-chi-phu-mot-trong-hai-nguong` — **P2**, 1 thể hiện

`ADR-0044` cho `sensitive`: **≤ 3 tệp VÀ ≤ 300 dòng thêm**. Đo trên
`c66415aa..f2aa1f9f` giới hạn ở tệp sản phẩm: **7 tệp, +772 dòng** ⇒ **vượt CẢ HAI**.

Spec khai ngoại lệ ở dòng 73–77, và nó dùng **toàn bộ khung SỐ TỆP**:

> *"ADR-0044: khai lý do gói **>3 file** — 3 skill và 3 adapter phải đồng bộ cùng nguồn protocol.
> **Phạm vi hữu hạn là 7 file sản phẩm**… ghi riêng **số sản phẩm** và hiện vật."*

Đo: **không một con số dòng nào** xuất hiện trong spec (`grep` cho `772|vượt.*dòng|ngân sách dòng` ⇒ **0**).
`+772` so `≤300` là **2,6×**, và chiều ấy **không được nói tới**.

**Vì sao đây không phải bắt bẻ hình thức:** ngưỡng dòng của `ADR-0044` neo từ dữ liệu của chính kho,
và dữ liệu ấy nói về **số vòng review**:
`PLAT-M4` = 2 tệp, **+351** ⇒ *một vòng, một finding*; `PLAT-X4` = 4 tệp, **+721** ⇒ ***ba vòng, tám
finding***. WP538 ở **+772** — **trên** đúng điểm mà ADR dẫn ra làm bằng chứng "đã quá lớn".

Lý do đã khai (*sáu tệp phải đồng bộ cùng một nguồn protocol*) giải thích **vì sao NHIỀU TỆP**, và nó
là một lý do tốt. Nó **không** giải thích **vì sao 772 DÒNG**. Hai chiều khác nhau; ADR đòi cả hai.

*Bản vá theo lớp:* bổ sung vào spec một đoạn khai **ngân sách DÒNG** — hoặc lý do vì sao 772 dòng là
tối thiểu cho việc đồng bộ ấy, hoặc một phép tách slice. Vì đoạn ấy nằm trong **spec đã đóng băng**,
sửa nó là **revision mới** theo `§3.2`; quyền quyết thuộc chủ kho.

*KHÔNG khẳng định:* tôi **không** nói bản vá này bỏ sót lỗi vì nó dài. Sáu cổng đều `rc=0` và ba
hướng săn khác đều sạch. Thứ tôi nói là **ngưỡng của kho bị vượt ở một chiều không ai khai**.

### 2. `hien-vat-review-wp538-khong-co-trong-kho` — **P3**, 1 thể hiện

`ops/reviews/wp538/` nằm trong `write_set` của **cả hai** lease (r1/g1 và r2/g2), nhưng đo được nó
**không tồn tại trên bất kỳ ref nào** của kho.

Đối chiếu: kho có **166** tệp verdict trong `ops/reviews/` (131 reviewer=codex, 35 reviewer=claude),
và cổng `bien_nhan_v2` chấm chúng. WP538 có **0**. Nên approve của nó — một packet `sensitive` —
hiện chỉ sống trong **issue comment**, thứ mà chính doctrine của kho gọi là *"bản chiếu"*, không phải
nguồn có thẩm quyền. Comment sửa được; blob có băm thì không.

*Bản vá theo lớp:* commit verdict + biên nhận v2 vào `ops/reviews/wp538/` (đường đã có sẵn trong
write_set, nên không cần nới phạm vi).

*Đây là P3 chứ không phải P2:* nội dung review có tồn tại và tra được qua comment; thiếu là **độ bền
và khả năng chấm bằng cổng**, không phải thiếu bản thân lượt review.

## KHÔNG ĐO ĐƯỢC

- **Chất lượng lượt review cùng nền trước đó.** Tôi không đọc được transcript của nó; tôi **không**
  khẳng định nó bỏ sót gì. Hai phát hiện trên là của lượt NÀY, không phải cáo buộc về lượt ấy.
- **Hành vi runtime trên Windows.** PR mang nhãn `windows`; chỉ thị chủ kho là `N = 0` nên tôi
  **không** chạm lane ấy. Mọi kết luận ở đây là về **văn bản và cổng chạy được trong container này**.
- **CI của ứng viên.** Không gọi CI tay lần nào; không đọc được lượt CI nào cho `f2aa1f9f`.

## KẾT LUẬN

**`changes_requested`** — 0 P1 · **1 P2** · **1 P3** · 2 thể hiện.

Phần lớn packet đo được là **tốt**: sáu cổng `rc=0`; bản viết lại `§8` **giữ và siết** đúng những
dòng mà chính lượt này dựa vào; adapter `.agents/` là **con trỏ** đúng thiết kế, không phải bản sao;
không đường nào ngoài phạm vi. **Ba trong sáu hướng săn ra SẠCH, và tôi ghi chúng ra đầy đủ** — một
kết luận sạch có giá ngang một phát hiện.

Không `approve` vì `ADR-0044` bị vượt ở một chiều **không ai khai**, và ngưỡng ấy tồn tại chính vì
kích thước dự báo số finding bỏ sót. Sửa được bằng một đoạn khai trong spec — nhưng spec đã đóng
băng, nên đường sửa đi qua **revision mới**, và đó là quyết định của chủ kho.
