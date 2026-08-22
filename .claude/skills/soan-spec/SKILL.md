---
name: soan-spec
description: Chất vấn người giữ kho tới khi hết chỗ giả định, rồi xuất ra ĐẶC TẢ PACKET đóng băng ở ops/specs/<packet-id>.md kèm sha256 để lease neo vào. Dùng khi sắp mở một packet mới, khi một packet bị chặn vì đặc tả tự mâu thuẫn, hoặc khi người dùng nói "soạn spec", "chốt đặc tả", "grill trước khi code".
---

Cơ chế hỏi ở mục 1 mượn từ skill `grilling` của `mattpocock/skills` (MIT) — đã vendor nguyên
văn tại `.claude/skills/grilling/`. Mục 2–5 là phần của kho này; đừng trộn hai phần khi sửa.

Skill này KHÔNG nhắc lại luật của protocol. Luật ở `docs/PROTOCOL_DA_PHIEN.md`; từ vựng ở
`CONTEXT.md`. Chỗ nào skill này lệch protocol thì SKILL NÀY sai.

## 1. Cách hỏi — theo vòng, theo biên giới

Dựng cây quyết định: mỗi quyết định rẽ ra những quyết định treo vào nó. **Biên giới** là mọi
quyết định đã đủ tiền đề — tức những câu hỏi được ngay bây giờ mà không phải đoán câu trả lời
chưa nghe. Hỏi TRỌN biên giới trong một vòng, đánh số, mỗi câu kèm một câu trả lời khuyến nghị.
Rồi ĐỢI.

```
❓ **Q1** — **<tiêu đề>**: <thân câu hỏi, có thể nhiều đoạn, có thể kèm lựa chọn>

➡️ <câu trả lời tôi khuyến nghị>
```

Câu nào phụ thuộc một câu **đang mở trong cùng vòng** thì thuộc vòng SAU, không phải vòng này.

**Tra dữ kiện là việc của tôi, không bao giờ là việc của người dùng.** Câu hỏi nào cần một
sự thật của môi trường (tệp, lịch sử git, số đo CI, trạng thái PR) thì tôi đi đo hoặc phái
subagent đi đo. Không chặn cả vòng vì nó: một phép đo đang chạy là một tiền đề chưa xong, nên
chỉ các câu nằm dưới nó phải đợi — phần còn lại của biên giới hỏi ngay. **Quyết định** thì
luôn là của người dùng.

Xong khi biên giới RỖNG: mọi nhánh đã đi qua, không còn gì được giả định trong im lặng.
**Không hành động cho tới khi người dùng xác nhận đã hiểu giống nhau.**

## 2. Bốn luật riêng của kho — chúng sinh ra từ những lần đã trả giá

**L1 — Mọi con số "N thứ phải xử" phải khai N ĐẾM GÌ.** Một đặc tả từng viết một con số mà
người viết đếm phản chứng còn người đọc đếm finding; lượt thi hành đốt hơn 170 nghìn token và
54 lượt gọi để cho ra 0 dòng mã, rồi dừng vì đặc tả tự mâu thuẫn. Con số nào cũng phải đi kèm
đơn vị của nó.

**L2 — Mỗi mục phải chiếu được vào MỘT đường dẫn trong write set.** Mục nào cần sửa một tệp
ngoài write set thì đó là phát hiện của lượt soạn spec, phải xử NGAY tại đây — mở rộng write
set, hay cắt mục đó ra — chứ không để phiên thi hành gặp rồi tự xoay. Đặc tả hứa thứ mà write
set không kham được là lỗi của đặc tả.

**L3 — Mỗi tiêu chí nghiệm thu phải nói được phép đo nào làm nó ĐỎ.** "Có ca test" không phải
tiêu chí; "ca `rXX_` này, và đột biến ĐỔI MÀU nó" mới là. Tiêu chí không thể đỏ thì không phải
tiêu chí — ghi thẳng là chưa có cách đo, đừng làm tròn thành đã có.

**L4 — Packet khắc phục phải chép số đếm HÌNH DẠNG LỖI từ hồ sơ tiền nhiệm.** Bộ đếm ấy sống
trong biên nhận của packet trước; packet mới bắt đầu từ 0 nếu không ai chép sang, và chốt "lặp
ba lần thì hỏi có nên làm nữa không" mất tác dụng đúng lúc cần nhất.

**L5 — Mọi con số phải kèm THỜI ĐIỂM ĐO, và phải ĐO LẠI trước khi công bố.** Cùng họ với L1:
L1 hỏi *con số ĐẾM GÌ*, L5 hỏi *con số đo LÚC NÀO, trên head/ref nào*. Một con số không có mốc
không sai lúc viết — nó **chết lặng** ở lần đẩy kế tiếp, và im lặng là toàn bộ vấn đề: không cổng
nào đỏ, không ai cảnh báo, câu văn vẫn đọc trôi chảy.

Đo được ở `PLAT-X8`, cùng một packet, **bốn lần**: `265 → 313 → 328` dòng thêm và `82/82 → 85/85 →
87/87` ca test. Mỗi con số đúng ở commit sinh ra nó và sai ở commit kế. Lần tệ nhất, ô "trần
`ADR-0044`" khai một cổng **ĐẠT** trong khi số thật đã vượt trần và cần ngoại lệ người giữ kho —
tức một lời khai sai về THẨM QUYỀN, không chỉ sai một chữ số.

Hai hệ quả bắt buộc:
1. Mỗi con số trong đặc tả ghi kèm mốc (`đo trên <head/ref>, <ngày>`). Không có mốc thì không được
   viết ra.
2. Trước khi công bố bất kỳ bản nào, **đo lại** mọi con số, đừng chép từ bản trước hay từ thân PR.
   Chép là cách con số sống lâu hơn sự thật của nó.

Cách chữa cấu trúc, khi có thể: đừng ghi GIÁ TRỊ, hãy ghi **QUAN HỆ BẤT BIẾN + lệnh đo** (`N ≥ sàn`
kèm lệnh sinh ra `N`). Quan hệ sống qua commit; giá trị thì không.

## 3. Đo trước khi hỏi

Trước vòng 1, tự đo và ĐƯA SỐ vào câu hỏi, đừng bắt người dùng nhớ hộ:

- kích thước dự kiến (`git diff --numstat` trên phạm vi tương đương gần nhất) — đối chiếu
  ngưỡng ở `docs/adr/0044-nguong-kich-thuoc-packet-theo-do-luong.md`;
- write set dự kiến có giao với packet nào đang mở không;
- base dự kiến có phải tổ tiên của nhánh mặc định không;
- lớp review theo đường dẫn bị chạm (`docs/PROTOCOL_DA_PHIEN.md` §8), fail-closed khi không rõ.

Một câu hỏi mang sẵn số đo tốn của người dùng một chữ; cùng câu hỏi ấy không có số đo tốn họ
một buổi.

## 4. Thứ phải xuất ra

`ops/specs/<packet-id>.md`, các mục dưới đây đủ cả, mục nào rỗng thì ghi rõ **RỖNG VÌ SAO**:

| mục | nội dung |
|---|---|
| `packet_id` · `packet_issue` | định danh |
| `nguon_cap_viec` | trỏ một dòng kế hoạch `tệp:dòng`, HOẶC biên nhận/packet cha nếu là khắc phục |
| `review_class` | theo đường dẫn bị chạm; không rõ ⇒ mức chặt nhất |
| `write_set` | liệt kê từng đường dẫn, không dùng ký tự đại diện |
| `ngoai_pham_vi` | thứ CỐ Ý không làm, kèm lý do |
| `muc_tieu` | mỗi mục một dòng, đánh số, mỗi dòng chiếu vào một đường dẫn ở `write_set` (L2) |
| `nghiem_thu` | mỗi mục tiêu ≥1 tiêu chí, mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3) |
| `hinh_dang_ke_thua` | chép từ biên nhận tiền nhiệm; không phải packet khắc phục thì ghi `khong_ap_dung` (L4) |
| `chua_do_duoc` | thứ không kiểm được từ phiên này — ghi thẳng, đừng giấu sau chữ "có thể" |

Xong thì in băm để đưa vào lease:

```
sha256sum ops/specs/<packet-id>.md
```

Băm ấy là giá trị của `spec_sha256` trong lease. Đặc tả sống trong kho và có băm thì nó diff
được, review được, và không đổi sau lưng ai — khác hẳn một đặc tả nằm trong thân Issue.

## 5. Skill này KHÔNG làm gì

Nó **không** cấp việc. Đặc tả không phải lease, và một cây quyết định đã chốt cũng không phải
lease. Sau khi đóng băng vẫn phải có Issue và lease còn hiệu lực theo `docs/PROTOCOL_DA_PHIEN.md`
§3.2 và §4 thì mới được bắt tay. Phiên nào đọc spec rồi tự làm là tự cấp việc cho mình.

Nó cũng **không** tự sửa đặc tả đã đóng băng. Đặc tả đã có băm mà cần đổi thì đi qua bản sửa
đổi mới; sửa đè là làm băm trong lease trỏ vào một thứ không còn tồn tại.
