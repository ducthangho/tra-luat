# ĐỀ BÀI — vòng lặp TRI THỨC của kho `tra-luat`: nên tất định hoá tới đâu?

Bạn thẩm định độc lập. Kho ở `./kho` (chỉ đọc). Trả lời bằng PHÉP ĐO khi đo được, và khai
thẳng khi chỉ là suy luận.

## Câu hỏi của người giữ kho
"Kế hoạch có tính năng nào để lưu log/kiến thức/bài học trong quá trình build không? Một số
bài học rút ra dẫn tới cần thay đổi CẢ KẾ HOẠCH — có nên chuẩn hoá, TẤT ĐỊNH HOÁ, biến nó
thành một tính năng bắt buộc của Kế hoạch không?"

## Phép đo phiên điều phối đã chạy (kiểm lại được, đừng tin suông)

BẢY chỗ đựng tri thức, KHÔNG chỗ nào bị cổng máy đòi:
  CLAUDE.md §"Bài học đắt giá"     161 dòng
  ops/NO_KY_THUAT.md (sổ nợ)       481 dòng · 8 mục
  docs/adr/                        45 ADR
  ops/reviews/*.receipt.yaml       24 biên nhận (có khoá `verdict_usage_caveats` — khuôn
                                   BÀI HỌC CÓ CẤU TRÚC tốt nhất kho đang có)
  ops/reviews/*verdict.md          24
  ops/TONG_HOP_*                   1
  CHANGELOG.md                     7 648 dòng
  + thông điệp commit

  `grep 'bai_hoc' ops/lease_publish.py .claude/dev/packet_loop.py` → **0**

ĐƯỜNG SỬA KẾ HOẠCH ĐÃ CÓ: Mission Change Request, `docs/PROTOCOL_DA_PHIEN.md §3.1.1`, và
`:747` ghi "Packet Spec hoặc Mission Plan sai thì phải đi qua Packet revision hoặc MCR".
⇒ Con đường TỒN TẠI. Thứ thiếu là CÁI CÒ: không dòng nào định nghĩa KHI NÀO một bài học
buộc phải sinh MCR.

`hinh_dang_lap` (bộ đếm HÌNH DẠNG LỖI — cơ chế gần nhất với cò "bài học ⇒ đổi cách làm"):
  xuất hiện trong ĐÚNG 2 tệp văn bản, **0 dòng mã** nào đọc nó.
  Hệ quả đo được: `hinh_dang_lap: 3` của packet X4 KHÔNG chặn được packet X5 vì bộ đếm
  RESET Ở BIÊN PACKET.

## Ba dữ kiện tái phát, đo trong MỘT ngày (đây là bằng chứng bất lợi cho "viết thêm tài liệu")
1. Bẫy `$?` sau pipeline tái phát BA lần trong một ngày, với BA bên **đều đã đọc** bài học ấy.
2. Phiên điều phối lặp lại bài học về manifest/ratchet **đã được viết sẵn cách vài chục dòng
   TRONG CHÍNH TỆP đang sửa** (`scripts/tl_selftest.py`, khối "ĐÃ TRẢ GIÁ").
3. Bản hợp nhất kế hoạch (~3 giờ máy của ba bên) bị thực tế vượt qua trong vài giờ vì nó nằm
   trên một PR CHƯA MERGE — phiên khác không có cách nào đọc.

## Đề xuất hiện thời của phiên điều phối (hãy TẤN CÔNG nó)
Ba cạnh máy, nằm gọn trong gói `D` (`ops/lease_publish.py`) đã lên lịch:
  (1) `hinh_dang_lap` phải KẾ THỪA xuyên packet + có cổng ĐỌC nó; `dem >= 3` mà thiếu khối
      `quyet_dinh_kien_truc` ⇒ đỏ.
  (2) Biên nhận thêm `doi_ke_hoach: {can: bool, mcr: <id>|null}`; cổng từ chối packet kế
      nhiệm trên CÙNG SEAM nếu biên nhận tiền nhiệm nói `can: true` mà không trích MCR.
  (3) Mỗi bài học phải trỏ được một ca `rXX_`, HOẶC tự khai `chi_la_chu: true` — không ép ai
      viết test, chỉ CẤM IM LẶNG.
Một thay đổi KHÔNG cần máy: đánh chỉ mục bài học theo **CÒ** (`khi:gộp-master`, `khi:đọc-rc`,
`khi:thêm-tệp-docs`, `khi:dựng-sandbox-review`…) thay vì theo chủ đề, rồi hook phiên in ĐÚNG
nhóm liên quan.

## Trả lời sáu câu

**C1.** "Kho bài học" có phải KHUNG ĐÚNG không? Hay vấn đề là TRUY XUẤT chứ không phải LƯU?
Nếu là truy xuất thì tất định hoá việc LƯU có giải quyết được gì không?

**C2.** Trong ba cạnh máy, cạnh nào THỰC SỰ hoàn vốn? Tấn công từng cạnh: nêu một cách lách
rẻ tiền, hoặc một ca nó sẽ báo động giả và làm người ta học cách bỏ qua cổng.

**C3.** Cạnh (2) — "bài học ⇒ MCR" — có tất định hoá được không, hay "kế hoạch sai" vốn là
phán đoán nên KHÔNG gate được? Nếu không gate được thì nói thẳng, đừng vẽ một cổng giả.

**C4.** Đánh chỉ mục theo CÒ: với agent (thứ đi grep chứ không đọc tuần tự) nó có tác dụng
thật không, hay chỉ là một lớp văn xuôi nữa? Có cách đo được hiệu quả của nó không?

**C5.** RẺ NHẤT: thứ gì — MỘT thứ thôi — nếu đã tồn tại thì sẽ chặn được NHIỀU NHẤT trong ba
ca tái phát ở trên? Trả lời bằng cách chiếu từng ca vào đề xuất của bạn.

**C6.** Bạn sẽ KHÔNG xây gì? Kho đã có 7 chỗ đựng; chi phí lớn nhất của ngày hôm nay là
QUẢN TRỊ (4 lần gộp master, 3 lần chết bằng chứng CI), không phải mã.

## Định dạng
Markdown, tiếng Việt, NGẮN và dứt khoát. `C1`…`C6`, rồi `TOI_KY` (đề xuất cuối bạn ký, danh
sách đánh số, mỗi mục kèm cưỡng chế máy hoặc chữ "CHỈ LÀ CHỮ"), rồi `TOI_KHONG_KY`.
Giữ nhãn ĐO ĐƯỢC / ĐỌC ĐƯỢC / SUY LUẬN.
