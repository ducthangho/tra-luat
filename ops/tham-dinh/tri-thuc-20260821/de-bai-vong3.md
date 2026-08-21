# VÒNG 3 — MỘT NÚT THẮT DUY NHẤT. Cho cả codex và Fable 5.

Vòng 2 đã HỘI TỤ. Đọc `codex/vong2.md` và `fable/vong2.md` (cùng thư mục). Cả hai bên ĐỘC LẬP:
- BỎ `evidence-preflight` tổng quát làm packet đầu (cả hai ghi rõ "ĐỔI Ý")
- CHỌN **script sandbox reviewer fail-đóng** làm packet #1, đi TRƯỚC mọi cạnh khác
- CHỌN `plan_impact` enum thay cho `mcr: id|null`
- TỪ CHỐI `chi_la_chu: true` như bảo đảm (Fable rút chữ ký vòng 1 của chính mình)
- Xếp "neo tài liệu/spec vào ref bền" làm lát kế tiếp

**Đừng tranh lại bất cứ điều nào trên.** Vòng này chỉ giải ĐÚNG MỘT bất đồng còn lại.

## Phiên chính đã KIỂM 6 khẳng định của vòng 2 — cả 6 ĐÚNG
| khẳng định | bên nêu | đo được |
|---|---|---|
| `t36`–`t40` đã có trong `ops/lease_publish_test.py` | Fable | ĐÚNG — bộ có **41** ca, `t36`..`t40` ở dòng 1562–1839 ⇒ **slice A ĐÃ LAND** |
| `required_checks` = 0 trong `packet_loop.py` và `lease_publish.py` | codex | ĐÚNG (protocol có 3, đều là stub) |
| `chi_la_chu` = 0 occurrence toàn kho | codex | ĐÚNG |
| `record-review` có thật, là ĐÚNG MỘT ĐƯỜNG vào `accepted` | codex | ĐÚNG — `cmd_record_review` ở `packet_loop.py:871`; **và kho ĐÃ trả giá cho một lần vòng qua nó**: finding `review-transition-bypasses-record-review` (cross-review lượt 6) ghi ngay tại dòng 113 |
| workflow đọc `prompt_path` từ **head được đẩy**, không từ master | Fable | ĐÚNG (`ops-publish-lease.yml`, `--root .`, chú thích nói thẳng) ⇒ đòi PROMPT trên ref bền tại lúc cấp là báo động giả cấu trúc; SPEC thì không |
| ADR-0044: `sensitive` ≤3 tệp/300 dòng thêm · thường ≤6 tệp/1.000 dòng thêm+xoá | cả hai | ĐÚNG |

## BẤT ĐỒNG DUY NHẤT: script sandbox nằm Ở ĐÂU, và lệnh cấm có răng ngay từ packet 1 không?

**Fable:** tệp MỚI `ops/dung_sandbox_review.py` + test + adapter. Phân loại `systemic` (≤6 tệp/1.000 dòng)
vì "không đụng authority: không cấp lease, không sửa workflow". Mở được NGAY.
Fable **tự khai giới hạn**: *"lệnh CẤM 'mọi lượt review phải qua script' là **CHỈ LÀ CHỮ** chừng nào chưa
có chốt máy phía sau đòi receipt — không gì ngăn phiên chính vẫn dựng tay."*

**codex:** mở rộng `.claude/dev/packet_loop.py` + test + adapter, và **`record-review` phải TỪ CHỐI mọi
lượt review thiếu receipt hợp lệ**. Phân loại `sensitive` (≤3 tệp/**300 dòng**) vì nó ĐỔI review authority.
codex ghi thẳng vào `TOI_KHONG_KY`: *"script sandbox tuỳ chọn nhưng `record-review` vẫn nhận lượt thủ công."*

Tức là: **bản codex đóng đúng cái lỗ mà Fable tự thừa nhận** — nhưng phải sống trong 300 dòng thay vì 1.000.

## Bốn câu

**E1 — Script này có ĐỤNG review authority không?** Trả lời có/không và neo vào tiêu chí `sensitive` của
ADR-0044, không neo vào cảm tính. Lưu ý dữ kiện: `record-review` là ĐÚNG MỘT ĐƯỜNG vào `accepted`, và kho
ĐÃ có một finding về việc vòng qua nó. Nếu bạn trả lời "không", hãy nói **lượt review dựng tay bị chặn ở
đâu** — nếu câu trả lời là "không ở đâu cả" thì bạn đang ký một cổng CHỈ LÀ CHỮ, và cả hai vòng trước đều
đã từ chối đúng loại đó.

**E2 — 300 dòng có đủ không?** Nếu bản có răng (`record-review` đòi receipt) KHÔNG lọt 300 dòng thêm, hãy
CẮT nó sao cho **lát 1 vẫn có răng**. Ràng buộc cứng: lát 1 không được là "script tuỳ chọn, siết sau" —
cả hai bên đã từ chối hình dạng đó ở vòng 1 và vòng 2. Nêu rõ cái gì ở lát 1, cái gì bị đẩy sang lát 2,
và **vì sao lát 1 một mình đã chặn được ít nhất một trong bốn sự cố**.

**E3 — Bốn check của Fable (neo trích dẫn · đủ bundle · rc trực tiếp · thăm dò GHI) so với sáu điều của
codex.** Gộp thành MỘT danh sách tối thiểu: mỗi mục phải neo vào **một sự cố có thật** trong bốn sự cố, và
mỗi mục phải có **một đột biến làm ca đích ĐỎ**. Mục nào không neo được vào sự cố thật thì BỎ — kho đã trả
giá cho việc thêm check "cho chắc". Danh sách này quyết định số dòng của E2, nên trả lời E3 trước rồi hãy chốt E2.

**E4 — Thứ tự, sau khi biết slice A ĐÃ LAND.** Fable xếp lát 2 (cưỡng chế `spec_path`+`spec_sha256` +
resolve từ ref bền, rc=6) SAU slice A/B vì ADR-0044 nói write set giao nhau. Slice A đã land (đo được ở
bảng trên). Vậy lát 2 nay đi SONG SONG với packet 1 được chưa, hay còn vướng slice B? Nếu song song được,
nói thẳng — người giữ kho cần biết có mở hai packet cùng lúc hay không.

## Định dạng
`E1`..`E4`, rồi `CHOT` (một đoạn: packet 1 là gì, write set, phân loại, trần dòng, lát 2 song song hay
không), rồi `TOI_KHONG_KY`, rồi `KHONG_DO_DUOC`. Nhãn `ĐO ĐƯỢC`/`ĐỌC ĐƯỢC`/`SUY LUẬN` cho mỗi khẳng định.
NGẮN. Vòng này cần một quyết định thi hành được, không cần thêm phân tích.
