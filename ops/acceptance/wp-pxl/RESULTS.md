# WP-PXL r1 — LIVE promote 2 module mới lên Desktop rồi VM (#1413)

**Căn cứ:**
- Chủ kho 19/11 khoảng 06:03Z: "Live Promote thì đẩy bản lên desktop và cả VM đi".
- Xác nhận thao tác cụ thể: **"Chỉ 2 module mới"**.

**Artifact:**
- `ProximaActivation.psm1` (`bb96cd58…`, 29 276 byte);
- `ProximaInstall.psm1` (`81c1164b…`, 39 070 byte);
- lấy từ commit `9cdfeaf5b`; `artifact_sha256` = `194de266…`.

**Driver:** `PXL.ps1`, sha256 `91faef1c46d60212bbef104712749d5f0c6199e6613e3e3d2ca1dbcf4f5a83c1`. Trước khi chạy, driver đã được kiểm cú pháp bằng parser của PS 5.1 và PS 7 trên **cả hai** máy, và sha khớp trên cả hai.

## Hàng rào: Desktop → VM
| Máy | Thời gian | P1 hàng rào | P2 cài | P3 kiểm khói | P4 hậu kiểm | Receipt |
|---|---|---|---|---|---|---|
| DESKTOP-T9R33P2 | 06:27:47–06:27:52Z | `ALLOWED` (máy đầu, chưa cần receipt) | 2 tệp, băm khớp | PS 7 (nạp theo tên) và PS 5.1 (nạp theo đường dẫn): export đúng; `WhatIf` → `NOTHING_TO_DO`, 0 hành động; hàng rào `ALLOWED` | chỉ thêm `ProximaActivation`, `ProximaInstall` | `passed=true`, sha `fb230706…` |
| TRA-LUAT-WIN (gateway LIVE) | 06:34:19–06:34:37Z | `ALLOWED` dựa trên receipt Desktop `fb230706…` (chuyển nguyên byte, kiểm sha hai đầu) | 4 tệp (2 module × 2 thư mục Modules), băm khớp | Đạt ở cả 4 tổ hợp: thư mục `tlcommander` (PS 7/5.1, theo đường dẫn) và thư mục commander (PS 7 theo tên, PS 5.1 theo đường dẫn) | **`gateway_unchanged=True`**: 14 tiến trình `ProximaGateway`/`Proxima.exe` giữ nguyên PID và thời điểm khởi động; 4 tệp `ProximaControl` 1.0.1 giữ nguyên băm; tác vụ `TraLuat*` giữ nguyên trạng thái. Mỗi thư mục chỉ thêm đúng 2 thư mục | `passed=true` |

**Thư mục đích:**
- Desktop: `C:\Users\ThangHD\OneDrive\Documents\PowerShell\Modules\{ProximaActivation,ProximaInstall}`.
- VM:
  - `C:\Users\tlcommander\Documents\PowerShell\Modules\{ProximaActivation,ProximaInstall}`;
  - `C:\ProgramData\TraLuatCommander\profile\Documents\PowerShell\Modules\{ProximaActivation,ProximaInstall}`.

**Lệch so với đặc tả (ghi rõ):** trên Desktop, thư mục Modules của người dùng **chưa tồn tại**. Driver chạy với `-CreateRoot` và đã tạo `C:\Users\ThangHD\OneDrive\Documents\PowerShell` cùng `…\Modules` (P2a; rollback sẽ xoá nếu rỗng). Đây là đường dẫn module chuẩn của PS 7 cho người dùng không có quyền admin. Vì nằm trong OneDrive, 2 tệp `.psm1` (mã công khai của kho) sẽ được đồng bộ lên OneDrive của chủ kho.

**Bằng chứng (đóng băng, quét secret rc 0):**
- Desktop: `F:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\pxl\freeze-desktop\wp-pxl-desktop-evidence.zip`, sha256 `2021e18376d60f90bc394bac0d32f5c0a95c0890ffa6ca80ffe1d79940e2036e`, 8 tệp, MANIFEST `9280a6d4…`.
- VM: `C:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\pxl\freeze-vm\wp-pxl-vm-evidence.zip`, sha256 `df30ce64ac6175c9998752ce8836927fa5983abf8f227d401774aadbb0b51d57`, 9 tệp, MANIFEST `8d3a5310…`.

**Không làm:**
- không đụng `ProximaControl` 1.0.1, gateway hay runtime Proxima;
- không restart gì;
- không đổi service, tác vụ, tài khoản hay endpoint;
- không inference.

Các module mới **chưa được luồng nào trên VM gọi tới**. Chúng sẵn sàng để `Import-Module` khi cần, nhưng không thay đổi hành vi nào đang chạy.

**Rollback**, mỗi máy: xoá đúng 2 thư mục module mới (và trên Desktop, thư mục gốc vừa tạo nếu rỗng).
