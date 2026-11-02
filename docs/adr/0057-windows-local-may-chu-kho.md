# ADR-0057 — Máy Windows local của chủ kho: dùng khi online, cộng thêm vào điều kiện merge, không thay CI

- **Trạng thái:** Accepted (2026-10-29, chỉ thị chủ kho `ducthangho` trong phiên điều phối
  `session_01V2PEqhkb91vD5PCBM5yXbm`; chủ kho duyệt `spec_hash` `377ecea6…e715` của đặc tả
  `ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r1.md` ở PR #1020 issuecomment-6493571372 mục 3; thi hành bằng packet
  `WINDOWS-LOCAL-MAY-CHU-KHO` revision 1 · generation 1, mission #748 — không phải một phiên tự đặt quy ước)

Khi máy Windows của chủ kho bật và Desktop Commander hoạt động, executor được dùng máy đó để chạy test và vá lỗi
Windows. Đã chạy local thì lỗi local do diff gây ra phải vá trước merge. Local **cộng thêm** vào check bắt buộc của
CI, không thay chúng.

## Vì sao — số đo 29-10-2026

Trước ADR này quy ước chỉ đi tới từng phiên qua `send_message`. Chủ kho yêu cầu đo hiệu quả trước rồi mới đưa vào
protocol. Số đo lấy từ `D:\tl-win\do-luong.csv` trên ASUS-LAPTOP và từ log phiên, chép từ §1 của đặc tả:

| # | sự kiện | số đo | bài học |
|---|---|---|---|
| D1 | chạy song song selftest của `tl.py`, `lease_publish_test`, `packet_loop_test` trên `1cc847d` | `t192_S8` đỏ khi chạy song song; chạy riêng trên `e9967f0` lúc máy rảnh ra 3/3 ĐẠT (8 s) | chạy chồng sinh **đỏ giả** ⇒ cần khoá một-phiên-một-lúc |
| D2 | hai phiên chưa nhận quy ước | PID 17016 (`wp960-win`) và PID 22884 (`tl1014`, PR #1014 đã đóng) chạy `bien_nhan_v2_test` từ 09:06Z và 09:10Z, ngoài khoá, trong lúc phiên #1006 giữ khoá từ 09:24Z | quy ước gửi qua tin nhắn không tới mọi phiên ⇒ phải nằm ở **nơi mọi phiên đọc** |
| D3 | `packet_loop_test` không in tiến độ (stdout đệm) | 65 phút với `pl.out` = 0 byte rồi phải dừng tay | lượt dài trên local phải in tiến độ |
| D4 | độ sẵn sàng | Desktop Commander trả `CONNECT_TIMEOUT` cho `session_015GtxrZ1Tt93F4NLUUhKYQy` lúc ~09:00Z và ~09:23Z; máy offline khoảng 3 giờ trước 07:48Z | local **có lúc có lúc không** ⇒ không làm điều kiện bắt buộc vô điều kiện |
| D5 | lợi ích | selftest của `tl.py` 1738/1738 local trong khoảng 10 phút; Windows CI qua `workflow_dispatch` ~40 phút cộng hàng đợi, hôm đó bị billing chặn nhiều giờ | máy sẵn sàng thì local nhanh hơn CI và không phụ thuộc billing |
| D6 | lỗi phát hiện | trên master: `t27` (Windows-only, packet #1006), `r929` (WinError 5, đã vá #1010), `bien_nhan_v2_test` c91/c93/c96 (#1017) | local tái hiện lỗi Windows thật mà CI Linux không thấy |

Đây là số đo của **một ngày, một máy**. Nó đủ để đặt quy ước, chưa đủ để kết luận local luôn có lợi; mục
*Xem xét lại* ở dưới tồn tại vì vậy.

## Quyết định

1. **Phạm vi.** Máy Windows của chủ kho (hiện là ASUS-LAPTOP) truy cập qua Desktop Commander. Executor chỉ dùng
   máy khi `list_devices` báo `Online`.
2. **Điều kiện merge cộng thêm.** Packet đã chạy test trên Windows local thì mọi lỗi local **do diff gây ra** phải
   được vá trước merge. Lỗi có sẵn trên base phải nêu tên, kèm SHA đo nền. Máy offline thì vế này không áp, và PR
   phải ghi rõ "không đo local". Local **không thay** check bắt buộc của CI, chỉ cộng thêm.
3. **Khoá.** `D:\tl-win\KHOA.txt` có nội dung nghĩa là máy đang bận. Phiên giữ khoá ghi
   `<session_id>\t<UTC>\t<việc>` và xoá nội dung khi xong. Không chạy test nặng khi khoá đang do phiên khác giữ.
4. **Kiểm tải trước khi đo.** Chạy `Get-CimInstance Win32_Process -Filter "Name='python.exe'"`. Có tiến trình không
   thuộc phiên mình thì ghi vào kết quả đo, và **không** tự dừng tiến trình của phiên khác.
5. **Cô lập.** Mỗi phiên làm trong thư mục riêng `D:\tl-win\<session_id>\` (clone từ GitHub, `core.abbrev 7`).
   Không đụng kho làm việc của chủ kho.
6. **Môi trường.** `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8`, `PYTHONDONTWRITEBYTECODE=1`; gọi `python`; đường dẫn
   có dấu thì dùng `git -C`.
7. **Tiến độ.** Lượt chạy quá 5 phút phải in tiến độ (`python -u` hoặc nhật ký từng ca).
8. **Đo lường.** Mỗi lượt ghi một dòng vào `D:\tl-win\do-luong.csv` theo các cột
   `thoi_diem,session,packet,sha,bo_test,dat,tong,ca_do,thoi_luong_s,phat_hien_boi,loi_that,da_va,ghi_chu`.
9. **Bằng chứng.** PR ghi SHA đã đo, lệnh chạy, N/N, và nói rõ đó là "local".
10. **Xem xét lại.** Sau 10 packet có dùng local, hoặc sau 30 ngày, chủ kho xét lại ADR này dựa trên
    `do-luong.csv`.

## Những gì KHÔNG đổi

- Check bắt buộc của CI và branch protection giữ nguyên. Một lượt local xanh không phải check run, không thay
  receipt CI, và không được ghi thành bằng chứng Windows của CI (`docs/PROTOCOL_DA_PHIEN.md` §10.2.2–§10.2.3).
- Điều kiện merge theo review class (§8) giữ nguyên; vế local chỉ thêm vào.
- Executor vẫn chỉ ghi trong effective write set. Thư mục `D:\tl-win\` là máy của chủ kho, không phải kho.
- Không có quyền dừng tiến trình của phiên khác. Dọn máy là việc của chủ kho.

## Không cổng nào cưỡng chế ADR này

**0 cổng.** Không gì trong kho đọc `KHOA.txt`, đọc `do-luong.csv`, kiểm `list_devices`, hay đòi PR khai "local" /
"không đo local". `adr-song` chỉ canh ADR này có dòng trong §20 và có dòng `Trạng thái`; nó không đọc nội dung.
Khoá là tệp văn bản, không nguyên tử: hai phiên đọc cùng lúc thấy rỗng vẫn có thể cùng ghi. Toàn bộ ADR là **kỷ
luật executor**. Viết công cụ tự động cho khoá hoặc sổ đo nằm ngoài packet này; nếu số đo về sau cho thấy cần, đó
là việc của một packet sau.

## Phương án bị loại

- **Bắt buộc chạy local cho mọi packet:** D4 cho thấy máy offline hàng giờ; điều kiện bắt buộc vô điều kiện sẽ
  chặn merge vì một máy tắt, không vì mã sai.
- **Để quy ước ở tin nhắn `send_message`:** D2 đo được hai phiên chưa từng nhận nó và chạy ngoài khoá.
- **Coi local xanh là đủ, bỏ Windows CI:** local là một máy, một môi trường, không có run/attempt GitHub; nó
  không chứng minh runner `windows-latest`.
