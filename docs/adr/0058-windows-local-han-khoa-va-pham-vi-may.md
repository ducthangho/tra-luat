# ADR-0058 — Máy Windows local: phạm vi theo `list_devices`, khoá theo từng máy và hạn khoá 2 giờ

- **Trạng thái:** Accepted (2026-10-30, chủ kho `ducthangho` duyệt `spec_hash` `4c92ecbf…7c2b` của đặc tả
  `ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r2.md` ở PR #1025 issuecomment-6514073214 mục 1; thi hành bằng packet
  `WINDOWS-LOCAL-MAY-CHU-KHO` revision 2 · generation 1, mission #748 — không phải một phiên tự đặt quy ước)

ADR này sửa **đúng hai điểm** của `ADR-0057`: §1 *Phạm vi* và §3 *Khoá*. Mọi điểm khác của `ADR-0057` giữ
nguyên hiệu lực, theo cùng cách `ADR-0056` thay đúng một câu của `ADR-0017`. Tệp `ADR-0057` không bị sửa.

## Vì sao — số đo 29-10-2026

`ADR-0057` có hiệu lực từ 29-10-2026. Ngay trong ngày đó đã đo được hai lỗ mà nó không phủ (chép từ §1 của đặc tả):

| # | sự kiện | số đo | bài học |
|---|---|---|---|
| D7 | khoá bỏ rơi | Phiên `session_015GtxrYjGJtmjF3eT1nCSG9` ghi khoá `D:\tl-win\KHOA.txt` lúc 09:24:55Z. Laptop mất kết nối khoảng 10:00Z, offline tới ~11:37Z. Khoá nằm đó khoảng 2 giờ 15 phút trong khi máy không chạy test nào (`session_015GtxrbUPS7zGdffB8Sfo8Y` kiểm lúc ~11:40Z: chỉ có 2 tiến trình python của MCP browser-use). Phiên giữ khoá không xoá được từ xa nên tự tuyên bố khoá hết hiệu lực qua `send_message`. | §3 của `ADR-0057` chỉ có "xoá khi xong", không có hạn. Máy tắt khi đang giữ khoá thì khoá kẹt mãi, và mọi phiên khác phải đợi |
| D8 | máy thứ hai | VM GCE `tra-luat-win` ở trạng thái RUNNING (đo bằng `gcloud` trên laptop, ~11:40Z) nhưng không có trong `list_devices` của Desktop Commander (chỉ có ASUS-LAPTOP). `gcloud` trong container cloud không có credential. | §1 của `ADR-0057` chỉ nêu ASUS-LAPTOP. Máy Windows thứ hai chưa có luật, và khoá một-tệp không nói khoá thuộc máy nào |
| D9 | chu trình đủ đầu tiên | `t27`: master `9666771` cho 0/1 ĐỎ, #1007 head `10446ff` cho 2/2 QUA, đo local trên ASUS-LAPTOP lúc 11:39:56Z–11:40:20Z. #1022 head `f4d15ed`: 3/3 ĐẠT local. | quy trình chạy được trọn vòng; lỗ ở D7 và D8 là lỗ thật, không phải giả định |

## Quyết định

1. **Phạm vi (thay §1 của `ADR-0057`).** Phạm vi là mọi máy Windows của chủ kho đang có mặt trong `list_devices`
   của Desktop Commander với trạng thái `Online`. Hiện có ASUS-LAPTOP; VM `tra-luat-win` chỉ thuộc phạm vi khi nó
   xuất hiện trong `list_devices`. Máy không có trong `list_devices` thì không dùng, và không tìm đường khác
   (ví dụ `gcloud`, RDP) để vào máy đó.
2. **Khoá và sổ đo theo máy.** Mỗi máy có khoá và sổ đo riêng ở thư mục gốc `tl-win` của chính máy đó: `D:\tl-win\`,
   hoặc `C:\tl-win\` nếu máy không có ổ `D:`. Mọi đường dẫn `D:\tl-win\…` trong `ADR-0057` được đọc theo nghĩa
   này. Kết quả đo ghi thêm tên máy vào cột `ghi_chu`, dạng `may=<tên trong list_devices>`.
3. **Hạn khoá (bổ sung cho §3 của `ADR-0057`).**
   - Dòng khoá có thêm trường hạn: `<session_id>\t<UTC bắt đầu>\t<UTC hạn>\t<việc>`. Hạn không quá **2 giờ** sau
     lúc bắt đầu.
   - Hết hạn mà phiên giữ khoá vẫn cần máy thì phải ghi lại dòng với hạn mới (gia hạn).
   - Khoá được coi là **hết hiệu lực** khi:
     (a) quá hạn ghi trong dòng; hoặc
     (b) dòng theo dạng cũ của `ADR-0057` (không có trường hạn) đã quá 2 giờ kể từ UTC bắt đầu; hoặc
     (c) phiên giữ khoá đã tuyên bố bỏ khoá. Trường hợp (c) phải có bằng chứng: tin nhắn của chính phiên đó hoặc
     comment trên PR của nó.
   - Phiên tiếp nhận khoá hết hiệu lực làm theo thứ tự: chạy bước kiểm tải (§4 của `ADR-0057`); ghi một dòng vào
     sổ đo với `ghi_chu` nêu khoá cũ (session, UTC) và lý do (a)/(b)/(c); thay nội dung khoá bằng dòng của mình.
     Dù có tiếp nhận khoá, vẫn không được dừng tiến trình của phiên khác.

## Những gì KHÔNG đổi

- §2 và §4–§10 của `ADR-0057` giữ nguyên: điều kiện merge cộng thêm, kiểm tải, cô lập, môi trường, tiến độ,
  cột sổ đo, bằng chứng và mốc xem xét lại.
- Mục *Những gì KHÔNG đổi* của `ADR-0057` giữ nguyên: check bắt buộc CI, branch protection và điều kiện merge theo
  review class (§8) không đổi; local chỉ cộng thêm.
- Khoá vẫn là tệp văn bản không nguyên tử như `ADR-0057` đã khai. Hạn khoá không làm nó nguyên tử: hai phiên đọc
  cùng lúc thấy khoá hết hiệu lực vẫn có thể cùng tiếp nhận.
- Không có quyền dừng tiến trình của phiên khác, kể cả khi tiếp nhận khoá. Dọn máy là việc của chủ kho.

## Không cổng nào cưỡng chế ADR này

**0 cổng**, như `ADR-0057`. Không gì trong kho đọc `KHOA.txt`, đọc trường hạn, so giờ hạn với giờ hiện tại, đọc
sổ đo, hay kiểm `list_devices`. `adr-song` chỉ canh ADR này có dòng trong §20 và có dòng `Trạng thái`; nó không
đọc nội dung. Toàn bộ ADR là **kỷ luật executor**. Viết công cụ khoá nguyên tử hay bộ đọc sổ đo nằm ngoài packet
này. Cấp credential `gcloud` cho container và cài Desktop Commander lên VM là việc của chủ kho.

## Phương án bị loại

- **Khoá không hạn, chờ phiên giữ khoá tự xoá:** D7 đo được khoá kẹt khoảng 2 giờ 15 phút khi máy offline; phiên giữ
  khoá không xoá được từ xa.
- **Dùng mọi máy Windows của chủ kho, kể cả máy ngoài `list_devices`:** D8 cho thấy đường vào VM qua `gcloud` không
  có credential trong container; tự tìm đường vào máy là vượt quyền đã cấp.
- **Một khoá chung cho mọi máy:** khoá chung chặn máy rảnh vì máy khác đang bận, và không nói khoá thuộc máy nào.
