# Đặc tả packet — TRAN-VONG-REVIEW-LEN-BON (revision 1)

- `packet_id`: **TRAN-VONG-REVIEW-LEN-BON**; ID bền `wp<packet_issue>`.
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp)**
- `revision`: **1** · `generation`: 1 · soạn **11:5xZ 11-09-2026**
- `depends_on`: **`[]`**
- `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive** (đổi một ADR đang hiệu lực về THẨM QUYỀN)

## `nguon_cap_viec`

Chỉ thị chủ kho **11-09-2026**: *"Nâng trần lên 4"*. `ADR-0043` (Accepted 21-08-2026, chủ kho phê
duyệt Q5) đang khai trần canon là **HAI** vòng review hợp lệ.

`ADR-0034` đòi **Mission Change Request** cho thay đổi material; packet này là đường thi hành của MCR
ấy, **không** phải một phiên tự nâng trần.

## VẤN ĐỀ ĐO ĐƯỢC — con số này sống ở NHIỀU chỗ, và đó chính là bệnh `ADR-0043` sinh ra để chữa

`grep -rn 'ADR-0043'` (đo 11:5xZ 11-09-2026, bỏ `ops/reviews/`):

| tệp | dòng | nội dung |
|---|---:|---|
| `docs/adr/0043-tran-vong-review-canon-la-hai.md` | 1 | ADR gốc |
| `docs/adr/0037-review-rescue-va-tach-stable-slice.md` | 6 | trỏ `ADR-0043`, **không** chép số ✔ |
| `docs/PROTOCOL_DA_PHIEN.md` | 807 | trỏ `ADR-0043`, **không** chép số ✔ |
| `docs/PROTOCOL_DA_PHIEN.md` | 1145 | bảng §20 — **chép chữ "HAI"** vào tiêu đề |
| `ops/specs/BO-CONG-DUYET-KHAC-DANH-TINH.md` | 185 | **chép số**: *"chạm trần HAI vòng review"* |
| `ops/specs/CI-CAI-JSONSCHEMA-r2.md` | 184 | **chép số** |
| `ops/specs/CI-CAI-JSONSCHEMA-r3.md` | 208 | **chép số** |
| `ops/specs/TAT-DINH-VOID-HA-TANG-r2.md` | 113 | **chép số** |

**Bốn đặc tả đã ĐÓNG BĂNG chép con số `HAI` vào thân.** Nâng trần mà sửa chúng là **sửa một hợp đồng
đã đóng băng** — `§3.2` cấm. Không sửa thì chúng mâu thuẫn ADR mới.

**Lối ra: trần có HIỆU LỰC THEO THỜI ĐIỂM ĐÓNG BĂNG, không hồi tố.**
`§3.2` đã có sẵn cơ chế: *"Policy đổi làm closure thay đổi thì packet phải tạo revision và generation
mới trước khi chạy tiếp."* Nên bốn đặc tả kia **giữ trần 2** cho packet của chúng, và đó **không** phải
mâu thuẫn — đó là lời khai đúng về trần **tại thời điểm chúng đóng băng**. Packet nào muốn trần 4 thì
**tạo revision mới** sau ngày ADR mới được chấp nhận.

Điều này phải được viết **vào chính ADR mới**, nếu không lần đọc kế tiếp sẽ thấy *"ADR nói 4, bốn đặc
tả nói 2"* và không có gì phân xử — đúng hình dạng `ADR-0043` đã trả giá (*"con số sống ở bốn chỗ với
hai giá trị và hai luật ưu tiên loại trừ nhau"*).

## `review_class` và ngưỡng

`sensitive` ⇒ `ADR-0044`: **≤ 3 tệp, ≤ 300 dòng thêm**. Packet này **2 tệp**.

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `docs/adr/0048-tran-vong-review-len-bon.md` | ADR mới, thay số của `ADR-0043` |
| 2 | `docs/PROTOCOL_DA_PHIEN.md` | dòng §20 cho ADR mới + dòng `1145` của `ADR-0043` đổi trạng thái |

Không ký tự đại diện. **KHÔNG** đụng bốn đặc tả đã đóng băng ở bảng trên.
**KHÔNG** đụng `docs/adr/0043-*.md` — ADR cũ giữ nguyên làm hồ sơ; ADR mới **trỏ tới** nó.

## `ngoai_pham_vi`

1. **KHÔNG sửa bốn đặc tả đã đóng băng.** Xem lối ra ở trên.
2. **KHÔNG viết cổng `so-canon`** — đó là packet riêng (`nợ` #1 dưới). Packet này chỉ đổi con số và
   luật hiệu lực.
3. **KHÔNG đổi `codex_review_calls_used`** (trần LỜI GỌI = 2) — `ADR-0043` tách ba trục
   (VÒNG · LỜI GỌI · ATTEMPT) và packet này chỉ đụng trục **VÒNG**. Nâng nhầm trục kia là nâng chi phí
   chứ không nâng kỷ luật.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | ADR mới khai trần canon trục VÒNG là **BỐN**, trỏ `ADR-0043` là tiền nhiệm, và giữ nguyên hai trục kia. | #1 |
| M2 | ADR mới khai **luật hiệu lực theo thời điểm đóng băng**: packet có `spec_hash` đóng băng TRƯỚC ngày ADR được chấp nhận giữ trần cũ; muốn trần mới thì tạo revision. | #1 |
| M3 | `§20` có **đúng một dòng** cho ADR mới; dòng của `ADR-0043` đổi sang trạng thái *đã bị thay số*, **không xoá**. | #2 |
| M4 | Khối `nang_tran` vẫn bắt buộc khi vượt trần MỚI — nâng trần không bỏ cơ chế vượt trần. | #1 |

## `nghiem_thu`

**A1 (M1,M3) — `adr-song` xanh.**
`python3 .claude/dev/packet_loop.py adr-song --root .` ⇒ `rc=0`, và số ADR trên đĩa **BẰNG** số dòng
trong §20 (hôm nay `47/47`; sau packet **48/48** — hai số phải **BẰNG NHAU**).
**Phép làm ĐỎ:** thêm ADR mà quên dòng §20 ⇒ `adr-song` ĐỎ (cổng này **đã có răng**, không phải hứa).

**A2 (M1) — con số chỉ có MỘT chỗ ở.**
`grep -rn 'trần.*\(HAI\|BỐN\)\|vòng review canon'` trên `docs/` ⇒ **chỉ** `docs/adr/0048-*.md` mang
con số; `docs/PROTOCOL_DA_PHIEN.md:807` và `docs/adr/0037:6` vẫn **trỏ** chứ không chép.
**Phép làm ĐỎ:** chép số `4` vào `PROTOCOL:807` hoặc `ADR-0037` ⇒ ĐỎ.
**Đây là tiêu chí quan trọng nhất của packet**: `ADR-0043` ra đời vì con số bị chép; nâng nó bằng cách
chép lại là tái tạo đúng khuyết tật.

**A3 (M2) — luật hiệu lực PHÂN BIỆT ĐƯỢC hai trạng thái.**
Ca kiểm bằng lời, trên bốn đặc tả đã đóng băng ở bảng: với mỗi cái, ADR mới phải cho ra câu trả lời
**KHÔNG mơ hồ** về trần của nó. Đòi ADR nêu **mốc** (ngày chấp nhận) và **thứ neo** (`spec_hash` đóng
băng trước hay sau mốc).
**Phép làm ĐỎ:** bỏ mốc, hoặc viết *"áp dụng cho mọi packet"* ⇒ bốn đặc tả kia mâu thuẫn ⇒ ĐỎ.

**A4 (M4) — vượt trần vẫn đòi `nang_tran`.**
ADR mới phải giữ nguyên câu: vượt trần đòi khối `nang_tran` khai `ai_nang` (người có thẩm quyền),
`can_cu`, `tran_cu`, `tran_moi`.
**Phép làm ĐỎ:** ADR mới bỏ câu ấy ⇒ trần 4 thành trần mềm ⇒ ĐỎ.

**A5 (toàn packet) — `ADR-0044`.** `git diff --numstat` ⇒ đúng **2** đường dẫn, `additions` ≤ `300`.

**A6 — `doctrine-scan` xanh.** `python3 .claude/dev/packet_loop.py doctrine-scan --root .` ⇒ `rc=0`.

**Điều kiện dừng:** `sensitive` ⇒ đòi cross-review **`approve`** tường minh.

## `chua_do_duoc`

1. **`so-canon` vẫn KHÔNG tồn tại.** `§20` ghi `ADR-0043` → **`0 cổng`**, và `ADR-0043` tự khai:
   `grep -rln "review_rounds_used" --include=*.py .` ⇒ **0 tệp** — *"không phải 'có bộ đếm mà thiếu
   trần', mà là không có bộ đếm nào"*. Đo lại 11:5xZ 11-09-2026: **vẫn 0 tệp**.
   ⇒ Trần `4` cũng sẽ **không có cổng nào canh**, y như trần `2`. Packet này **không** chữa điều đó và
   **không** được khai là đã chữa. **Nợ có tên: `SO-CANON-CHUA-TON-TAI`.**
2. **Không đo được số vòng review đã dùng của bất kỳ PR nào** — không bộ đếm, không biên nhận bắt buộc.
   Ba lượt review của `#508` **không** sinh biên nhận nào trong `ops/reviews/` (đo 11:4xZ 11-09-2026),
   nên theo đúng `PROTOCOL:814` chúng **chưa** được tính là vòng canon. Đây là lý do trần `2` chưa
   từng bị chạm một cách đo được, và cũng là lý do nâng lên `4` **không đổi gì trên thực tế** cho tới
   khi nợ #1 được đóng.
