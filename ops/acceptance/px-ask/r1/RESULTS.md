# PX-ASK-SONG r1 — kết quả: cả ba máy `blocked`, 0 lời gọi model

**Căn cứ:** đặc tả `ops/specs/px-ask-r1.md` (sha256 `97e6d617…`), lease `ops/leases/px-ask-r1-g1-operator.yaml`, Issue #1446.

## 1. Tóm tắt
| máy | Pha A | kết luận | điều kiện §0 thiếu |
|---|---|---|---|
| Desktop `a5f7076e` | 1 lượt, rc 0 | `blocked` | không có Proxima: không tiến trình, không dịch vụ, không thư mục cài |
| VM `f7281f27` | 1 lượt, rc 0 (+ 1 truy vấn chỉ đọc bổ sung, mục 3.2) | `blocked` | đường dẫn exe của tiến trình gateway không đọc được dưới tài khoản chạy `px` (không phải admin) |
| ASUS `7404cfba` | 1 lượt, rc 0 | `blocked` | không có Proxima: như Desktop |

- **Pha B không chạy trên máy nào.** Không chép module, không ghi cấu hình px, không gọi `px`, **0 lời gọi inference**.
- Không đổi gì trên host ngoài việc tạo thư mục làm việc `…\tl-work\px-ask-r1\`, chứa script dò và JSON đầu ra.

## 2. Script và cách chạy
- Script Pha A: `PXA.ps1`, sha256 `8260538509892ba7835756ea5f9be799135a08edac2f78649be788ff8b0b5e50`, 41 dòng. Mỗi máy in lại băm này
  trước khi chạy, và băm khớp ở cả ba máy.
- Lệnh trên mỗi máy (PowerShell 7, qua Desktop Commander): `pwsh -NoProfile -File <dir>\PXA.ps1 -Out <dir>\pha-a-<máy>.json`.
  Nội dung đúng như đặc tả §1: đọc CIM `Win32_Process`/`Win32_Service`, `Get-NetTCPConnection -State Listen`, đọc `rest-port.json`, tìm
  `ProximaControl.psd1`. Không gửi HTTP.
- JSON thô **không** vào kho (kho public, có đường dẫn hồ sơ người dùng). Băm do host in:

| máy | tệp | sha256 | lúc (UTC) | PowerShell |
|---|---|---|---|---|
| Desktop | `pha-a-desktop.json` | `9b83ef1749a90c4c3f3c5a062d124100e446f3c18b301dd9cd68d1df0f6cf3e7` | 2026-11-20T05:46:49Z | 7.6.10 Core |
| VM | `pha-a-vm.json` | `1e5cb7d4f449d1e0b96d55f78b3f0a9e6e509dd9a722993900a7ecbcc9ee8d2e` | 2026-11-20T05:48:15Z | 7.6.9 Core |
| ASUS | `pha-a-asus.json` | `2b92f7dd4b70ef2c9edfff74d2df3db0c67c029417a3ca83392e0aad52a4d266` | 2026-11-20T05:48:22Z | 7.6.10 Core |

## 3. Dữ kiện (đã lược)
### 3.1 Desktop, ASUS
Giống nhau trên hai máy: `is_admin` false, session 1, `proxima_procs` rỗng, `services` rỗng; base `C:\ProgramData\TraLuatCommander` và
`%LOCALAPPDATA%\Programs\Proxima` đều không tồn tại; không listener; `PROXIMA_API_KEY` không đặt; không tìm thấy `ProximaControl.psd1`
trong `PSModulePath`. `errs` rỗng. Giải thích hợp lý nhất: Proxima per-user đã được gỡ ở các lượt nghiệm thu NSIS (#1405) — đây là
suy luận, chưa đối chiếu nhật ký gỡ.

### 3.2 VM
- Tài khoản chạy script: `is_admin` false, session **0**.
- `rest-port.json` ở base `C:\Users\<tài khoản dịch vụ>\ProximaGateway`: `pid` 436, `port` 3210. Có `runtime\Proxima.exe`.
- 12 tiến trình `Proxima.exe`, tất cả ở session 0. Tám tiến trình đọc được `ExecutablePath`, và đều là `<base>\runtime\Proxima.exe`.
  Bốn tiến trình trả rỗng, trong đó có **PID 436**.
- Listener: `127.0.0.1:3210` và `127.0.0.1:19222`, cả hai thuộc PID 436.
- `Win32_Service`: `Access denied` (ghi trong `errs`), nên không biết dịch vụ nào bọc gateway.
- Module đã cài: chỉ `ProximaControl` **1.0.1** dưới `Documents\PowerShell\Modules` của hồ sơ dịch vụ (psd1 `3f2ac59e…`, psm1 `ef4821cc…`),
  khớp số liệu r7 của #1319.
- **Truy vấn bổ sung, chỉ đọc**, chạy sau Pha A để giải thích PID 436; ngoài script, ghi ở đây cho minh bạch:
  ```text
  {"pid":436,"name":"Proxima.exe","cim_exe":null,"cmdline_len":0,"gp_path":null,"owner_rv":2,"owner_user":null}
  {"pid":5268,"name":"ProximaGateway.exe","cim_exe":null,"cmdline_len":0,"gp_path":null,"owner_rv":2,"owner_user":null}
  ```
  PID 436 là con của `ProximaGateway.exe` (PID 5268). `Win32_Process.GetOwner` trả 2 (access denied) cho cả hai, tức hai tiến trình chạy
  dưới danh tính khác tài khoản đang gọi. `Get-Process` cũng không đọc được `Path`.

## 4. Vì sao VM `blocked`
- Module 2.0.0 đọc `ExecutablePath` của PID trong `rest-port.json` qua CIM `Win32_Process`, cùng nguồn với Pha A
  (`$script:Prim.GetProcess`). Đường dẫn rỗng ⇒ `throw 'unreadable'` ⇒ `RuntimeUnverified`, trước mọi HTTP
  (`ProximaControl.psm1`, `Get-PxcGateway`).
- Gateway được bọc bởi `ProximaGateway.exe`. Skill khai *"dịch vụ bọc (kiểu NSSM) bị từ chối"* (`SKILL.md`, mục Giới hạn), nhưng chốt
  ấy (`Assert-PxcService`) chỉ nằm trên đường `start`/`stop`/`restart`. Đường `ask` không gọi nó; với `ask`, chỗ chặn là đường dẫn exe.
- Vì vậy chạy `px ask` dưới tài khoản này sẽ dừng an toàn mà không gọi model. Theo đặc tả §2, máy không thỏa §0 thì dừng ở Pha A, nên
  `px` **không** được gọi để tái hiện điều này: đó là suy ra từ mã, chưa chạy.

## 5. Muốn `px ask` chạy thật thì cần gì (chủ kho quyết; mỗi lựa chọn là thay đổi LIVE khác loại, ngoài r1)
1. **VM, chạy `px` dưới tài khoản đọc được tiến trình gateway** (admin, hoặc chính danh tính của dịch vụ). Khi đó đường `ask` chỉ còn
   phải đo: đường dẫn exe của PID 436 có đúng `<base>\runtime\Proxima.exe` không, và `/v1/models` có quảng bá model không. Còn
   `start`/`stop`/`restart` sẽ vướng thêm chốt "dịch vụ bọc".
2. **VM, đổi cách chạy gateway** thành dịch vụ `ProximaGateway` trỏ thẳng `<base>\runtime\Proxima.exe`, đúng mẫu module nhận. Việc này
   đổi dịch vụ LIVE.
3. **Desktop hoặc ASUS: cài Proxima dạng dịch vụ session 0.** Bản per-user không bao giờ thỏa §0, vì nó chạy ở session của người dùng.
4. **Sửa module** để nhận gateway bọc hoặc per-user. Đây là đổi mã của skill, cần packet có review riêng.

## 6. Ngân sách đã dùng
| máy | Pha A | `px status`/`models` | `ask -WhatIf` | `ask` thật |
|---|---|---|---|---|
| Desktop | 1/2 | 0 | 0 | 0/1 |
| VM | 1/2 (+1 truy vấn bổ sung) | 0 | 0 | 0/1 |
| ASUS | 1/2 | 0 | 0 | 0/1 |
