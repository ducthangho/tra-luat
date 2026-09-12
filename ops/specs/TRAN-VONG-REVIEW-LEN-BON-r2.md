# Đặc tả packet — TRAN-VONG-REVIEW-LEN-BON (revision 2)

- `packet_id`: **TRAN-VONG-REVIEW-LEN-BON**; ID bền `wp<packet_issue>`.
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp)**
- `revision`: **2** · `generation`: 1 · soạn **08:0xZ 12-09-2026**
- `thay_the_cho`: **revision 1** (soạn 11:5xZ 11-09-2026, trần **BỐN**) — r1 CHƯA từng được cấp packet
  hay lease, nên đây không phải sửa một hợp đồng đang chạy; r1 giữ nguyên trên đĩa làm hồ sơ.
- `depends_on`: **`[]`**
- `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive** (đổi một ADR đang hiệu lực về THẨM QUYỀN)

## `nguon_cap_viec`

Chỉ thị chủ kho **12-09-2026**: *"trần nâng lên thành 10 vòng đi"*. Chỉ thị **11-09-2026** trước đó là
*"Nâng trần lên 4"*, và r1 của đặc tả này viết theo con số ấy.

`ADR-0043` (Accepted 2026-08-21, chủ kho phê duyệt Q5) đang khai trần canon trục VÒNG là **HAI**.
`ADR-0034` đòi **Mission Change Request** cho thay đổi material; packet này là đường thi hành của MCR
ấy, **không** phải một phiên tự nâng trần.

## VÌ SAO 10, KHÔNG PHẢI 4 — số biện hộ đo được, không phải sở thích

Trần chỉ có ích khi nó bắt được ca bất thường. Hai chuỗi review THẬT của kho, đo 12-09-2026:

| PR | số vòng cross-review đã dùng | trần 2 | trần 4 | trần 10 |
|---|---:|---|---|---|
| `#508` (`#513`) | **13** | vượt từ vòng 3 | vượt từ vòng 5 | vượt từ vòng 11 |
| `#512` (`#504`) | **4** | vượt từ vòng 3 | **chạm đúng ở vòng 4** | còn chỗ |
| `#517` | 3 | vượt từ vòng 3 | trong trần | trong trần |
| `#520` | 3 | vượt từ vòng 3 | trong trần | trong trần |

Trần **4** đã bị chạm bởi một packet đang chạy (`#512`) **ngay trong ngày r1 được soạn**, và `#508`
vượt nó gấp ba. Một trần mà thực tiễn thường xuyên vượt thì mỗi lần vượt lại đòi một khối `nang_tran`,
và khi việc khai ngoại lệ thành THƯỜNG LỆ thì ngoại lệ không còn là tín hiệu — đúng khuyết tật
*"cổng đỏ thường trực"* mà kho đã ghi. Trần **10** giữ cho `nang_tran` là chuyện hiếm và do đó ĐÁNG ĐỌC.

**Nói thẳng giới hạn của lý lẽ này:** nó biện hộ cho việc trần phải CAO HƠN 4, không chứng minh đúng
con số 10. Con số 10 là quyết định của chủ kho; phần đo được chỉ là *"4 quá thấp so với thực tiễn đã
đo"*. Đừng khai mạnh hơn thế.

## VẤN ĐỀ ĐO ĐƯỢC — con số này sống ở NHIỀU chỗ (giữ nguyên từ r1)

`grep -rn 'ADR-0043'` (đo 11:5xZ 11-09-2026, bỏ `ops/reviews/`), kiểm lại 12-09-2026 vẫn đúng:

| tệp | dòng | nội dung |
|---|---:|---|
| `docs/adr/0043-tran-vong-review-canon-la-hai.md` | 1 | ADR gốc |
| `docs/adr/0037-review-rescue-va-tach-stable-slice.md` | 6 | trỏ `ADR-0043`, **không** chép số ✔ |
| `docs/PROTOCOL_DA_PHIEN.md` | 807 | trỏ `ADR-0043`, **không** chép số ✔ |
| `docs/PROTOCOL_DA_PHIEN.md` | 1145 | bảng §20 — **chép chữ "HAI"** vào tiêu đề |
| `ops/specs/BO-CONG-DUYET-KHAC-DANH-TINH.md` | 185 | **chép số** |
| `ops/specs/CI-CAI-JSONSCHEMA-r2.md` | 184 | **chép số** |
| `ops/specs/CI-CAI-JSONSCHEMA-r3.md` | 208 | **chép số** |
| `ops/specs/TAT-DINH-VOID-HA-TANG-r2.md` | 113 | **chép số** |

**Bốn đặc tả đã ĐÓNG BĂNG chép con số `HAI` vào thân.** Sửa chúng là sửa hợp đồng đã đóng băng —
`§3.2` cấm. Không sửa thì chúng mâu thuẫn ADR mới.

**Lối ra: trần có HIỆU LỰC THEO THỜI ĐIỂM ĐÓNG BĂNG, không hồi tố.** `§3.2` đã có sẵn cơ chế:
*"Policy đổi làm closure thay đổi thì packet phải tạo revision và generation mới trước khi chạy tiếp."*
Nên bốn đặc tả kia **giữ trần 2** cho packet của chúng, và đó **không** phải mâu thuẫn — đó là lời khai
đúng về trần **tại thời điểm chúng đóng băng**. Packet nào muốn trần mới thì **tạo revision mới** sau
ngày ADR mới được chấp nhận. Điều này phải viết **vào chính ADR mới**, kẻo lần đọc kế tiếp thấy
*"ADR nói 10, bốn đặc tả nói 2"* mà không có gì phân xử.

## `review_class` và ngưỡng

`sensitive` ⇒ `ADR-0044`: **≤ 3 tệp, ≤ 300 dòng thêm**. Packet này **2 tệp**.

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `docs/adr/0048-tran-vong-review-len-muoi.md` | ADR mới, thay số của `ADR-0043` |
| 2 | `docs/PROTOCOL_DA_PHIEN.md` | dòng §20 cho ADR mới + dòng `1145` của `ADR-0043` đổi trạng thái |

Không ký tự đại diện. **KHÔNG** đụng bốn đặc tả đã đóng băng ở bảng trên. **KHÔNG** đụng
`docs/adr/0043-*.md` — ADR cũ giữ nguyên làm hồ sơ; ADR mới **trỏ tới** nó. **KHÔNG** đụng
`ops/specs/TRAN-VONG-REVIEW-LEN-BON.md` (r1) — nó là hồ sơ đã đóng băng của một con số khác.

## `ngoai_pham_vi`

1. **KHÔNG sửa bốn đặc tả đã đóng băng.**
2. **KHÔNG viết cổng `so-canon`** — packet riêng; nợ #1 dưới.
3. **KHÔNG đổi `codex_review_calls_used`** (trần LỜI GỌI = 2). `ADR-0043` tách ba trục
   (VÒNG · LỜI GỌI · ATTEMPT); packet này chỉ đụng trục **VÒNG**. Nâng nhầm trục kia là nâng CHI PHÍ
   chứ không nâng kỷ luật.
4. **KHÔNG đổi định nghĩa vòng review canon** (`PROTOCOL:814` — vòng chỉ tính khi có biên nhận). Nâng
   trần mà nới định nghĩa là nâng hai thứ cùng lúc rồi không biết cái nào có tác dụng.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | ADR mới khai trần canon trục VÒNG là **MƯỜI**, trỏ `ADR-0043` là tiền nhiệm, giữ nguyên hai trục kia. | #1 |
| M2 | ADR mới khai **luật hiệu lực theo thời điểm đóng băng**: packet có `spec_hash` đóng băng TRƯỚC ngày ADR được chấp nhận giữ trần cũ; muốn trần mới thì tạo revision. | #1 |
| M3 | `§20` có **đúng một dòng** cho ADR mới; dòng của `ADR-0043` đổi sang trạng thái *đã bị thay số*, **không xoá**. | #2 |
| M4 | Khối `nang_tran` vẫn bắt buộc khi vượt trần MỚI — nâng trần không bỏ cơ chế vượt trần. | #1 |
| M5 | ADR mới ghi **số biện hộ** (bảng bốn PR ở trên) và ghi thẳng rằng phần đo được chỉ biện hộ *"cao hơn 4"*, con số 10 là quyết định của chủ kho. | #1 |

## `nghiem_thu`

**A1 (M1,M3) — `adr-song` xanh.** `python3 .claude/dev/packet_loop.py adr-song --root .` ⇒ `rc=0`, và
số ADR trên đĩa **BẰNG** số dòng §20 (hôm nay `47/47`; sau packet **48/48**).
**Phép làm ĐỎ:** thêm ADR mà quên dòng §20 ⇒ `adr-song` ĐỎ (cổng này **đã có răng**).

**A2 (M1) — con số chỉ có MỘT chỗ ở.**
`grep -rn 'trần.*\(HAI\|BỐN\|MƯỜI\)\|vòng review canon'` trên `docs/` ⇒ **chỉ** `docs/adr/0048-*.md`
mang con số mới; `docs/PROTOCOL_DA_PHIEN.md:807` và `docs/adr/0037:6` vẫn **trỏ** chứ không chép.
**Phép làm ĐỎ:** chép số `10` vào `PROTOCOL:807` hoặc `ADR-0037` ⇒ ĐỎ.
**Đây là tiêu chí quan trọng nhất:** `ADR-0043` ra đời vì con số bị chép; nâng nó bằng cách chép lại là
tái tạo đúng khuyết tật.

**A3 (M2) — luật hiệu lực PHÂN BIỆT ĐƯỢC hai trạng thái.** Với mỗi đặc tả trong bốn cái đã đóng băng,
ADR mới phải cho câu trả lời **KHÔNG mơ hồ** về trần của nó. Đòi ADR nêu **mốc** (ngày chấp nhận) và
**thứ neo** (`spec_hash` đóng băng trước hay sau mốc).
**Phép làm ĐỎ:** bỏ mốc, hoặc viết *"áp dụng cho mọi packet"* ⇒ bốn đặc tả kia mâu thuẫn ⇒ ĐỎ.

**A4 (M4) — vượt trần vẫn đòi `nang_tran`.** ADR mới giữ nguyên câu: vượt trần đòi khối `nang_tran`
khai `ai_nang` (người có thẩm quyền), `can_cu`, `tran_cu`, `tran_moi`.
**Phép làm ĐỎ:** bỏ câu ấy ⇒ trần 10 thành trần mềm ⇒ ĐỎ.

**A5 (M5) — số biện hộ có mặt VÀ có giới hạn.** ADR phải mang bảng bốn PR, và phải có câu khai rằng
phép đo chỉ biện hộ *"cao hơn 4"*.
**Phép làm ĐỎ:** viết *"đo được rằng 10 là con số đúng"* ⇒ lời khai rộng hơn phép đo ⇒ ĐỎ.

**A6 (toàn packet) — `ADR-0044`.** `git diff --numstat` ⇒ đúng **2** đường dẫn, `additions` ≤ `300`.

**A7 — `doctrine-scan` xanh.** `python3 .claude/dev/packet_loop.py doctrine-scan --root .` ⇒ `rc=0`.

**Điều kiện dừng:** `sensitive` ⇒ đòi cross-review **`approve`** tường minh.

## `chua_do_duoc`

1. **`so-canon` vẫn KHÔNG tồn tại.** `§20` ghi `ADR-0043` → **`0 cổng`**; `grep -rln
   "review_rounds_used" --include=*.py .` ⇒ **0 tệp**, đo lại 12-09-2026 **vẫn 0**. ⇒ Trần `10` cũng
   sẽ **không có cổng nào canh**, y như trần `2`. Packet này **không** chữa điều đó và **không** được
   khai là đã chữa. **Nợ có tên: `SO-CANON-CHUA-TON-TAI`.**
2. **Số vòng ở bảng biện hộ đếm bằng TAY** từ hiện vật phiên (sandbox, verdict, comment PR), không từ
   một bộ đếm trong kho — vì bộ đếm ấy không tồn tại (nợ #1). `#512` có bốn verdict có băm; `#508` lấy
   theo commit doctrine *"chuỗi 13 lượt #513"*. Ai cần con số chắc hơn thì phải đóng nợ #1 trước.
3. **Không đo được trần 10 có đủ hay không** — nó chưa từng bị chạm. Câu duy nhất đo được là trần 4 ĐÃ
   bị chạm.
