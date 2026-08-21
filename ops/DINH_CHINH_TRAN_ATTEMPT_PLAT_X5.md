# ĐÍNH CHÍNH — trần attempt của `PLAT-X5` (#206)

**Loại:** append-only. **KHÔNG tệp lease nào bị sửa.** Hai lease dưới đây giữ nguyên từng byte;
tệp này là bản ghi *thêm vào*, không phải bản vá đè.

## 1. Sự việc — đo được
| tệp | dòng | giá trị |
|---|---|---|
| `ops/leases/plat-x5-exec-1-codex-20260820.yaml` | 76 | `attempts_limit: 3` |
| `ops/leases/plat-x5-exec-1r2-codex-20260820.yaml` | 102 | `attempts_limit: 2` |
| `ops/leases/plat-x5-exec-1r2-codex-20260820.yaml` | 1 | tiêu đề vẫn ghi **"lượt 1/3"** |

Lease r2 **không** có khối `nang_tran` hay `ha_tran`, **không** có dòng lý do, và
`granted_on_instruction` của nó chỉ nói về write set ("Thêm file vào write set #206") — không một
chữ nào về việc siết trần. Tức một trường trần **đổi giá trị giữa hai revision mà không để lại vết**,
và tự mâu thuẫn với tiêu đề của chính tệp mang nó.

Mặc định của protocol là **3**: `docs/PROTOCOL_DA_PHIEN.md:729` và `:73`
(`max_attempts_per_packet: 3`).

## 2. Quyết định của người giữ kho — 21-08-2026
> "Không phải chỉ đạo của tôi. Và để `attempts_limit` là 3."

**Trần đúng của `PLAT-X5` là 3.** Lần hạ 3→2 là **sai sổ**, không phải một quyết định ngân sách.

## 3. Đây KHÔNG phải nới trần hồi tố — và khác biệt là đo được
Nới hồi tố sẽ là: ghi `attempts_limit: 3` **đè lên** lease r2 rồi chạy tiếp — viết lại một con số
sau khi đã biết kết quả, đúng thứ `ADR-0034` cấm. Việc làm ở đây ngược lại: **không đụng lease cũ**,
ghi một bản đính chính nêu đủ ba số (`3` · `2` · tiêu đề "1/3"), người quyết, và căn cứ canon.

## 4. Đính chính này KHÔNG cấp thêm attempt nào cho nhánh hiện tại
`PLAT-X5` đã được chủ kho quyết là **`superseded`** (quyết định Q2 cùng ngày). Attempt được khôi
phục **không** được tiêu trên `e071e0aa`: nhánh ấy sẽ không land, và mọi việc làm trên nó sẽ mất
hiệu lực review khi base đổi. Packet kế nhiệm dựng từ base canonical bắt đầu với trần **mặc định
của protocol**, không phải với một con số ai đó chọn hôm nay khi đã biết kết quả.

## 5. Chốt máy phải sinh ra từ ca này
`ops/lease_publish.py check`: một trường `*_limit` đổi giá trị so với revision **trước** của cùng
lease series mà thiếu khối `doi_tran{tu, ve, ai, can_cu}` ⇒ **rc≠0**.
**Fixture đỏ có sẵn, không phải dựng:** chính cặp `plat-x5-exec-1` / `plat-x5-exec-1r2`.
Kèm đột biến: nới điều kiện để chấp nhận đúng cặp ấy ⇒ ca đích phải ĐỎ. Thuộc gói `V4`.

## 6. Vì sao ghi thành một tệp riêng
Chủ kho đo được rằng lần siết **không được ghi**; không ai đo được rằng nó **không được nói** — nên
câu trả lời phải đến từ người, và phải nằm ở một chỗ tra lại được. Một dòng chat không phải chỗ đó.
