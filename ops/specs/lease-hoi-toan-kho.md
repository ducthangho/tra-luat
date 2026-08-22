# ĐẶC TẢ PACKET — `LEASE-HOI-TOAN-KHO`

```yaml
packet_id: LEASE-HOI-TOAN-KHO
packet_issue: 244
revision: 1
review_class: sensitive          # ops/lease_publish.py = lease/publish authority (protocol §8), fail-closed
executor: claude
reviewer: codex
assurance_target: cross_approved
base_sha: 08bb4ecd6dbdb87267cb8179f52ac28c151eb4b9
```

## `nguon_cap_viec`

**KHÔNG có dòng kế hoạch nào cấp việc này** — đã tìm trong `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md`
và `ops/HANG_DOI_PACKET.md`, cả hai đều không nhắc. Packet sinh từ phép đo của phiên `tra-luat-3a`
ngày 22-08-2026, nên nguồn là **sổ nợ + Issue**, ghi thẳng chứ không bịa một dòng kế hoạch:

- `ops/NO_KY_THUAT.md:1004` — nợ mục 18 `CHOT-CHONG-DANG-TRUNG-DOC-DAU-THEO-NHANH`
- nợ có tên `SO-LEASE-KHONG-NAM-MOT-CHO` (`CLAUDE.md`, mục *"SỔ LEASE KHÔNG NẰM MỘT CHỖ"*)
- Issue `#244`

## `write_set`

```
ops/lease_publish.py
ops/lease_publish_test.py
```

Hai đường dẫn, liệt kê đủ, không ký tự đại diện.

**Write set này ĐANG BỊ GIỮ lúc đóng băng đặc tả.** Đo 16:5xZ 22-08-2026 trên 164 ref
(`yaml.safe_load`, fail-close): `plat-x8-exec-2`, `-2r2`, `-2r3` khai đúng hai đường dẫn này, hết hạn
`2026-08-23T14:10:00Z`, và `PLAT-X8` đang chạy thật (PR `#248`, +265/−1 trên đúng hai tệp).
**Lease cho packet này chỉ được cấp SAU khi `PLAT-X8` nhả** — land hoặc rút. Đặc tả không phải lease
(protocol §7), nên đóng băng trước là hợp lệ; bắt tay trước thì không.

Cùng lúc còn **9** lease `CÒN_HẠN` khác giao write set, thuộc `LEASE-DANG-*` — packet ấy **đã land**
(`#238` qua PR `#246`) nên chúng là quyền ghi **đã tiêu**, không phải vật cản. Chúng không tự khai điều
đó; xem `chua_do_duoc`.

## `ngoai_pham_vi`

| thứ | vì sao KHÔNG làm ở đây |
|---|---|
| Cổng `t33` đòi `shellcheck` | Packet riêng `T33-DOI-SHELLCHECK`. Chạm tệp khác (`ops/cai_actionlint.sh`), và **không dùng** năng lực "hỏi toàn kho" — gộp vào chỉ làm packet này vượt trần ADR-0044 |
| Đường **thu hồi** lease đã tiêu | Nợ `AG-T0-01B-thu-hoi-lease-chua-co-duong`. Packet này chỉ **ĐỌC ĐÚNG** trạng thái, không chế cơ chế huỷ. Cho một packet thu hồi lease của packet khác là dựng đường huỷ đơn phương |
| Sửa dữ liệu 6 lượt đăng thừa đã có | Là **hiện vật lịch sử**. Sửa hậu kỳ làm mất bằng chứng của chính nợ này |
| Đoán quan hệ `thay_the_lease` / `tiep_tuc_lease` | Hai trường ấy trỏ **NGƯỢC**; đọc xuôi không suy ra được. Sửa hướng con trỏ là đổi lược đồ lease — việc khác, packet khác |

## `muc_tieu`

Mỗi mục chiếu vào **một** đường dẫn trong `write_set` (L2).

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M1** | Lệnh `ai-dang-giu <đường-dẫn>`: quét **mọi ref**, trả **ba** trạng thái `CÒN_HẠN` / `HẾT_HẠN` / `KHÔNG_XÁC_ĐỊNH`, dùng bộ phân tích cấu trúc (`yaml.safe_load`), **fail-close** | `ops/lease_publish.py` |
| **M2** | Trước khi quét, `ai-dang-giu` **so hai nguồn** — `git ls-remote --heads` (máy chủ) với `git for-each-ref` (đệm) — **so bằng TẬP TÊN**, loại ref tượng trưng; thiếu ở phía cục bộ ⇒ `KHÔNG_XÁC_ĐỊNH` | `ops/lease_publish.py` |
| **M3** | Chốt chống đăng trùng (`:236-241`) đọc dấu **TOÀN KHO** thay vì từ bản lease trong cây đang chạy | `ops/lease_publish.py` |
| **M4** | Ca `rXX_` + đột biến cho M1–M3 | `ops/lease_publish_test.py` |

**Đơn vị của mọi con số trong đặc tả này (L1):** "lease" = **cặp (blob, đường dẫn) duy nhất** trên toàn
bộ ref, trừ khi ghi khác. Đếm theo **đường dẫn** cho số khác — đo 22-08: 117 cặp / 100 đường dẫn, chênh
10 là **phiên bản thừa**, không phải 10 tệp. Con số nào cũng phải đi kèm đơn vị.

## `nghiem_thu`

Mỗi tiêu chí nêu phép đo làm nó **ĐỎ** (L3).

**M1** — `A1` Gọi `ai-dang-giu ops/lease_publish.py` trên kho có ≥1 lease còn hạn ⇒ in đúng lease ấy và
thoát **khác 0**. ĐỎ khi: đột biến bỏ một trạng thái khỏi bảng phân loại, hoặc đổi `sys.exit` thành `0`.
`A2` Bơm một tệp lease **YAML hỏng** ⇒ `KHÔNG_XÁC_ĐỊNH` **và** mã thoát khác 0. ĐỎ khi: đột biến thay
`raise`/`exit` bằng `|| echo` — đúng cách hỏng lượt 3 của bộ quét hand-roll (fail-**OPEN** trong chốt viết
ra để fail-**CLOSE**).

**M2** — `A3` Giả một `ls-remote` trả **thừa một nhánh** so với `for-each-ref` ⇒ `KHÔNG_XÁC_ĐỊNH`.
`A4` Giả chiều ngược lại (thừa ở **cục bộ**) ⇒ **KHÔNG** báo động. ĐỎ khi: đột biến đổi phép so tập thành
so `wc -l` — cả A3 lẫn A4 phải đổi màu, vì đếm không phân biệt được hai chiều. `A5` Bơm một ref tượng
trưng kiểu `origin/HEAD` ⇒ **không** báo động. ĐỎ khi: bỏ bước loại ref tượng trưng.

**M3** — `A6` Dựng hai nhánh mang **cùng một** `lease_id`, một bản đã có `posted_comment_id`, bản kia
chưa; chạy cổng trên bản chưa có ⇒ **`RC_DA_DANG` (9)**. ĐỎ khi: đột biến đưa phép đọc dấu về chỉ đọc
tệp cục bộ — tức khôi phục đúng hành vi hiện tại. **Ca này là phản chứng của chính nợ mục 18**: không có
nó thì không biết đang đo cổng hay đo thứ khác.

**M4** — `A7` Mỗi ca trong `A1`–`A6` có **ít nhất một** đột biến khiến nó đổi màu, và bộ chạy đột biến in
ra **cả hai** số (số đột biến chạy · số đột biến bị giết) — hai số **bằng nhau**. ĐỎ khi: một đột biến
sống sót, hoặc hai số lệch. Nhắc `t97`: đột biến có thể **chưa từng chạy** do va chạm `.pyc`; bộ chạy phải
tắt ghi bytecode và dùng tên tệp riêng từng đột biến.

## `hinh_dang_ke_thua`

Chép từ thân Issue `#238` (**chưa** đối chiếu biên nhận — xem `chua_do_duoc`):

| | hình dạng | số |
|---|---|---|
| A | lời khai rộng hơn phép đo | **7** |
| B | mượn tiền lệ mà không đo xem nó áp dụng được không | 2 |
| C | phản chứng bắt buộc còn thiếu | 1 |
| D | đặt câu hỏi kiểm chứng ở sai độ phân giải / sai pha | 3 |
| E | khoá theo thứ liệt kê được thay vì theo thứ thật sự chặn | 2 |
| F | land trên một nền, đo trên nền khác | 2 |

Kế thừa vì packet này nhận một nợ đo được trong lượt `#238`. **A = 7 là cao nhất và đúng chỗ nguy hiểm
của packet này**: cả ba mục tiêu đều là "đọc trạng thái rồi khai", tức đúng loại việc đẻ ra hình dạng A.

## `chua_do_duoc`

1. **Hại thực tế của 6 lượt đăng thừa.** Chưa đếm số comment thật trên PR đích, chưa biết lượt sau có ghi
   đè lượt trước không. REST tới `repos/…` bị proxy chặn 403 từ container này.
2. **Bằng chứng byte thật trên GitHub.** Đọc thân comment/issue qua MCP **bị chuẩn hoá thực thể HTML**
   (đo bởi phiên `#238`). Phép đo *"chỉ khác đúng một dòng `posted_comment_id`"* của packet này **KHÔNG**
   đi qua đường ấy — nó chạy `git cat-file -p` trên blob cục bộ, đã chạy lại và xác nhận — nhưng ai
   đối chiếu lại bằng thân comment sẽ thấy khác, và khác đó là tạo tác của công cụ đọc.
3. **Vì sao chỉ `plat-x5-*` dính** (3/90 lease có nhiều id). Chưa phân định được là do `PLAT-X5` chạy
   nhiều lượt review hơn hay do nhánh của nó fan-out rộng hơn.
4. **Bộ đếm hình dạng kế thừa đọc từ thân Issue `#238`, chưa đối chiếu biên nhận.** Nếu biên nhận có số
   khác thì biên nhận thắng.
5. **9 lease `LEASE-DANG-*` "đã tiêu" không tự khai điều đó.** Kết luận ấy dựng bằng tay từ hiện vật trên
   master (`kiem_github` = 1, bộ test 73 ca). Không trường nào trong tệp lease nói ra, và trạng thái Issue
   cũng không.
