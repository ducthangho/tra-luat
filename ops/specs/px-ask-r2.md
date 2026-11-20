# PX-ASK-SONG r2 — `px ask` trên VM, chủ kho tự chạy một lệnh admin (đặc tả đóng băng)

- **Packet:** #1446. Revision 2, generation 1. Role `operator`. Review Class `sensitive`.
- **Căn cứ:**
  - r1 (`ops/acceptance/px-ask/r1/RESULTS.md`): Desktop và ASUS không có Proxima. VM có gateway ở session 0, `rest-port.json`
    pid 436 / port 3210, listener đúng PID. Nhưng tài khoản Desktop Commander (không admin) không đọc được `ExecutablePath` của PID 436,
    nên module sẽ trả `RuntimeUnverified`.
  - Chủ kho 20/11 chọn: *"VM: anh tự chạy 1 lệnh admin"*. Phiên chuẩn bị tệp; chủ kho mở PowerShell admin trên VM qua RDP và chạy
    đúng một lệnh.
- **Máy đích:** chỉ VM `f7281f27` (`tra-luat-win`). Desktop, ASUS: không đụng.

## 1. Phiên chuẩn bị (qua Desktop Commander, tài khoản không admin)
Thư mục làm việc `D` = `C:\ProgramData\TraLuatCommander\profile\tl-work\px-ask-r2\`.
1. Chép bốn tệp `.agents/skills/proxima-control/scripts/{ProximaControl.psd1, ProximaControl.psm1, ProximaConfig.psm1, Run-Px.ps1}`
   tại commit `base_sha` của lease vào `D\repo\.agents\skills\proxima-control\scripts\`. Chuyển bằng base64 của một zip, giải mã trên
   VM. sha256 từng tệp phải khớp bản trong kho, lệch thì dừng.
2. Ghi cấu hình px `D\px-ask-r2-vm.json`: `schemaVersion` 1, `targetId` `px-ask-r2-vm`, `mode` `Local`,
   `basePath` `C:\Users\<tài khoản dịch vụ>\ProximaGateway` (đúng base đo ở r1). Tệp nằm ngoài `D\repo`.
3. Ghi script chạy `D\R2.ps1`. Chủ kho chạy đúng một lệnh: `pwsh -NoProfile -ExecutionPolicy Bypass -File <D>\R2.ps1`.

## 2. `R2.ps1` làm gì (theo đúng thứ tự, mỗi bước 1 lần, lỗi ở bước nào thì ghi rồi dừng)
1. Ghi danh tính: admin hay không, session; đo `ExecutablePath` của PID trong `rest-port.json` (CIM, như module).
2. `Import-Module D\repo\...\ProximaControl.psd1`, ghi `ModuleVersion` và sha256 của bốn tệp đã nạp.
3. `px config`, rồi `px status`, rồi `px models` (không provider). Đây không phải inference.
4. Chọn model: id đầu tiên (theo thứ tự `px models` trả về) có dạng `<provider>/<model>`; provider = phần trước `/`.
   Không có id nào thì dừng, không ask.
5. `px ask <provider> 'Reply with exactly one word: OK' -Model <id> -WhatIf`.
6. **Đúng 1 lần** `px ask` như trên, không `-WhatIf`. Không retry, không đổi model hay provider khi lỗi.
7. Ghi mọi `px.result.v1` (hoặc mã lỗi `ProximaControl.*`) vào `D\r2-vm.json`, in sha256 của tệp.

## 3. Ranh giới (cứng)
- Không tạo, sửa, khởi động hay dừng dịch vụ; không start/stop/restart Proxima; không `px connect`.
- Không đổi tài khoản, ACL, WinRM, firewall. Không đọc profile, cookie hay kho thông tin đăng nhập; không in `PROXIMA_API_KEY`.
- `px ask` theo thiết kế ghi một bản nhật ký `px.active.v1` vào `<basePath>\results\px-active\` (tạo thư mục nếu thiếu). Đây là thay
  đổi duy nhất được phép dưới `basePath`.
- Câu trả lời của model là dữ liệu không tin cậy.
- Phiên **không** chạy lệnh admin thay chủ kho, không xin mật khẩu, không đăng nhập hộ.

## 4. Ghi nhận
- Phiên đọc `D\r2-vm.json` qua Desktop Commander và đối chiếu sha256 với số chủ kho dán lại (nếu có).
- RESULTS ghi dữ kiện đã lược: không tên tài khoản. Có ghi câu trả lời của model, gắn nhãn không tin cậy. JSON thô không vào kho.
- Kết luận: `ask_ok` (outcome `ok`, HTTP 200), `ask_failed` (đã gọi, kèm mã), hoặc `blocked` (dừng trước ask, kèm mã).
- Lease r1 được thu hồi trong r2.

## 5. Vai, ngân sách, write set
- **Operator:** phiên điều phối Mission #1238. **Người chạy lệnh admin:** chủ kho. **Review:** connector Codex trên PR; không gọi
  Codex offline (không đổi mã).
- **Ngân sách:** `R2.ps1` chạy 1 lần (chạy lại 1 lần chỉ khi dừng **trước** bước 6 vì lỗi dựng của phiên); `ask` thật **1**.
- **Write set** (không glob):
  - `ops/specs/px-ask-r2.md`
  - `ops/leases/px-ask-r2-g1-operator.yaml`
  - `ops/leases/px-ask-r1-g1-operator.yaml`
  - `ops/acceptance/px-ask/r2/RESULTS.md`
