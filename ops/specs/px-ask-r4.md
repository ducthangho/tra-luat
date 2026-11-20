# PX-ASK-SONG r4 — một lời gọi `px ask` thật trên VM với module 2.1.0 (đặc tả đóng băng)

- **Packet:** #1446. Revision 4, generation 1. Role `operator`. Review Class `sensitive`.
- **Căn cứ:**
  - r2 (`ops/acceptance/px-ask/r2/RESULTS.md`): dưới quyền admin, VM thông tới gateway, nhưng module 2.0.0 không nhận id model thật.
  - r3 (PR #1450, `ops/acceptance/px-ask/r3/`): module 2.1.0 nhận `<provider>` và `<provider>:<variant>`. Test Windows đạt, review Codex 2/2 approve.
  - Chủ kho 20/11 đã cho phép đúng 1 lời gọi thật trên VM (Issue #1446, *"Đồng ý làm đi"*). Cách chạy bằng một lệnh admin do chủ kho
    tự chạy, đã chọn ở r2.
- **Máy đích:** chỉ VM `f7281f27` (`tra-luat-win`).

## 1. Phiên chuẩn bị (Desktop Commander, tài khoản không admin)
Thư mục làm việc `D` = `C:\ProgramData\TraLuatCommander\profile\tl-work\px-ask-r4\`.
1. `git init` + `git -c core.autocrlf=false fetch --depth 1 https://github.com/ducthangho/tra-luat.git ac9a06d442000417e37487e271c646aa6162e3c3`, rồi
   `checkout FETCH_HEAD` vào `D\repo`. Băm `ProximaControl.psd1`, `ProximaControl.psm1`, `ProximaConfig.psm1`, `Run-Px.ps1` phải khớp
   blob tại SHA ấy; lệch thì dừng.
2. Cấu hình px `D\px-ask-r4-vm.json`: như r2, đổi `targetId` thành `px-ask-r4-vm`.
3. Script `D\R4.ps1`: giống `R2.ps1` của r2, khác ở hai điểm:
   - **Chọn model**: id đầu tiên trong `px models` có dạng `<provider>:<variant>`; nếu không có thì lấy id dạng `<provider>` đầu tiên,
     bỏ qua `auto`. Provider = phần trước `:`, hoặc chính id. Thứ tự giữ nguyên như `px models` trả về; không thử model khác khi lỗi.
   - Tệp đánh dấu riêng `D\ask-that-da-goi.marker`, chặn lời gọi thật thứ hai.

## 2. `R4.ps1` làm gì
`identity` → `gateway_exe` → `import` (phải là 2.1.0) → `px config` → `px status` → `px models` → chọn model → `px ask … -WhatIf` →
**đúng 1** `px ask` thật với câu `Reply with exactly one word: OK`. Ghi mọi kết quả vào `D\r4-vm.json` và in sha256 của tệp ấy.

## 3. Ranh giới (cứng)
Như r2 §3:
- không dịch vụ, không start/stop, không `connect`;
- không đổi tài khoản, ACL hay firewall; không đọc profile, cookie, credential; không in `PROXIMA_API_KEY`;
- nhật ký `px.active.v1` dưới `<basePath>\results\px-active\` là ghi duy nhất được phép dưới `basePath`;
- phiên không chạy lệnh admin thay chủ kho.

Câu trả lời của model là dữ liệu không tin cậy. RESULTS ghi nguyên văn câu trả lời, gắn nhãn không tin cậy.

## 4. Kết luận và ngân sách
- Kết luận: `ask_ok` (outcome `ok`, HTTP 200), `ask_failed` (đã gọi, kèm `outcome` và `httpStatus`), hoặc `blocked` (dừng trước ask, kèm mã).
- `R4.ps1` chạy 1 lần; chạy lại 1 lần chỉ khi dừng **trước** bước ask thật vì lỗi dựng của phiên. Lời gọi model thật: **tối đa 1**.
- Review: connector Codex trên PR; không gọi Codex offline (không đổi mã).

## 5. Write set (không glob)
- `ops/specs/px-ask-r4.md`
- `ops/leases/px-ask-r4-g1-operator.yaml`
- `ops/leases/px-ask-r3-g1-claude.yaml`
- `ops/acceptance/px-ask/r4/RESULTS.md`
