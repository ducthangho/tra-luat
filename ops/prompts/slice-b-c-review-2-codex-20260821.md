# PROMPT REVIEWER — `SLICE-B-C` (#215 / PR "#216"), **lượt 2/2**. Neo exact head `175e95bd`.

Reviewer khác nền (codex) cho packet do `claude` vá. **Read-only.** Kho ở `./kho`; tệp bạn tạo
phải nằm NGOÀI cây ấy. Chốt: `git -C kho status --short` RỖNG ở cuối lượt, HEAD vẫn
`175e95bd68556d38a7dde517ce858cb27e821097` (đủ 40 ký tự ở dòng cuối tệp này).

**ĐÂY LÀ LƯỢT CUỐI TRONG NGÂN SÁCH.** `changes_requested` hoặc `blocked` ⇒ human checkpoint,
không có lượt ba.

## Lượt 1 của bạn ra `changes_requested` với ba finding P2 — cả ba đã được vá

Verdict lượt 1 đọc lại được ở `kho/ops/reviews/` nếu có; nếu không có trong bản sao này thì
bỏ qua, đừng đi tìm. Tóm tắt để bạn khỏi phải nhớ:

- **F1** — `t42` chưa neo lời khai vào HÀNH VI. Bạn tìm được đột biến thứ tư: nới
  `_CHAY_BO_TEST` nhận thêm cờ đơn ⇒ phép đo đổi (`bắt 3/8 lọt 5/8` → `4/8 · 4/8`) mà suite
  vẫn `42/42`.
- **F2** — con số *"8 ca đỏ"* trong `ops/NO_KY_THUAT.md` §9 không đo được; chạy thật cho **1**.
- **F3** — tiêu chí `2 = 2` chỉ là ảnh chụp: thêm marker thứ ba mà mọi cổng vẫn xanh.

## Việc — đo BA bản vá, đừng đọc lời khai về chúng

**1. F1 đã đóng THẬT chưa.** Phiên vá thêm bảng `_DANG_CANONICAL_BI_BAT` (3 dạng PHẢI bị bắt)
và cho `t42` **sinh** tỷ lệ từ hai tập thay vì tìm chuỗi. **Chạy lại chính đột biến M4 của
bạn** và khẳng định nó nay giết `t42`. Rồi tìm đột biến **thứ năm**: có cách nào đổi hành vi
của `_CHAY_BO_TEST` mà `t42` vẫn xanh không? Gợi ý hướng, không phải danh sách đầy đủ — siết
regex thay vì nới; đổi một dạng trong bảng thành dạng vừa-bắt-vừa-lọt; thay đổi làm hai tập
đổi **cùng lúc** nên tỷ lệ giữ nguyên.

**2. F3 đã đóng THẬT chưa, và `t43` có BÁO ĐỘNG GIẢ không.** Phiên vá khai `t43` ĐỎ ngay lượt
chạy đầu vì kiểm cả hai chiều, rồi **hạ xuống MỘT chiều** (`marker ⊆ sổ nợ`) với lý lẽ: nợ tồn
tại được mà không cần marker trong mã. **Tấn công quyết định ấy**: hạ một chiều có làm mất một
bất biến thật không? Marker bị **gỡ** khỏi `ci.yml` mà mục nợ vẫn còn — ai bắt? Và hai mẫu
`_MARKER_NO` / `_MUC_SO_NO` có bó đúng hình dạng không, hay một câu văn xuôi có chữ `NỢ CÓ TÊN`
vẫn đếm nhầm?

**3. F2 đã đóng THẬT chưa.** §9 nay khai *"đúng một ca đỏ, suite `41/42`"*. **Tự chạy lại** với
`PATH` không có `actionlint`. Và kiểm chỗ khó hơn: câu mới có nói QUÁ không? Nó khẳng định
*"tám lỗi cùng chết vì thiếu một dependency không phải tám lớp bảo vệ độc lập"* — câu ấy có
được đo, hay lại là một suy luận nữa thay chỗ suy luận cũ?

**4. Bản vá có mở lỗ mới không.** `t43` đọc hai tệp ngoài write set của packet
(`.github/workflows/ci.yml`). Nó có nhánh "không thấy tệp thì bỏ qua" — nhánh ấy có chốt đúng
không, hay lại là một ca **CÓ MẶT mà KHÔNG ĐO** (bệnh `t24` của kho)?

## Bốn chốt của kho
1. Bằng chứng DƯƠNG: `N/N` hai số bằng nhau. **Và đừng nhận một `N/N` khi đột biến có thể chưa
   áp được** — phiên vá vừa mắc đúng lỗi này ở lượt trước, khai thẳng trong commit.
2. Đột biến chạy trên **BẢN SAO CẢ CÂY**, không ghi vào tệp thật.
3. Ba trạng thái: `có` · `không` · **`KHÔNG ĐO ĐƯỢC`** — cái thứ ba phải được KHAI.
4. Khai thẳng thứ bạn không đo được.

## Đầu ra
Mỗi finding: bằng chứng chạy được · mức (P0..P3) · bất biến bị cắt · gợi ý vá.
Kết thúc bằng đúng hai dòng, mỗi dòng ĐÚNG MỘT LẦN:

```
VERDICT: approve | changes_requested | blocked
Reviewed commit: 175e95bd68556d38a7dde517ce858cb27e821097
```
