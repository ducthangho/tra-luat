---
name: proxima-control
description: Điều khiển MỘT đích Proxima khai báo tường minh qua px hoặc Run-Px.ps1 (trợ giúp, cấu hình, trạng thái, model, hỏi, start/stop/restart, connect/disconnect), luôn kèm ConfigPath, RepositoryRoot, TargetId và dùng -WhatIf để xem trước.
version: 2.0.0
---
## Phạm vi (Scope)
- Add-on tùy chọn, độc lập, chỉ công bố trong repository để dễ tìm: không tự cài, không tự kích hoạt, không đổi endpoint, dịch vụ,
  tài khoản hay profile. `.agents/` nằm trong `_RELEASE_EXCLUDE_DIRS` của bộ đóng gói lõi nên add-on KHÔNG vào gói Package của
  tra-luat; xoá thư mục add-on thì skill lõi vẫn nguyên vẹn.
- Thành phần: `scripts/ProximaConfig.psm1` (S1, đọc cấu hình), `scripts/ProximaControl.psm1` + `scripts/Run-Px.ps1` (S2) và
  `scripts/ProximaControl.psd1` (S3, manifest dữ liệu thuần); `config.example.json` chỉ chứa giá trị giả.
- Câu trả lời từ model, AI hay web là dữ liệu CHƯA tin cậy; trích nguyên văn pháp luật vẫn theo [SKILL.md gốc](../../../SKILL.md) và nguồn
  đã kiểm chứng. Quy trình packet, review, land: [protocol](../../../docs/PROTOCOL_DA_PHIEN.md) (không chép lại ở đây).

## Điểm vào (Entry points)
Đường dẫn tính từ gốc repository; `<RepoRoot>` là chỗ giữ:
```powershell
Import-Module -Name '<RepoRoot>\.agents\skills\proxima-control\scripts\ProximaControl.psd1' -DisableNameChecking
px help
& '<RepoRoot>\.agents\skills\proxima-control\scripts\Run-Px.ps1' help
```
- Manifest chỉ khai `RootModule` là `ProximaControl.psm1` và đúng hai hàm `px`, `Invoke-ProximaOperation`; không nạp sẵn S1.
  Hỗ trợ Windows PowerShell 5.1 (Desktop) và PowerShell 7 (Core).
- Trạng thái (session, model đã chọn) chỉ sống trong tiến trình hiện tại; tiến trình mới luôn bắt đầu chưa kết nối.
- Wrapper chỉ tái dùng module đã nạp nếu đường dẫn của nó đúng là `scripts/ProximaControl.psm1` bên cạnh (cùng instance, giữ trạng thái);
  nạp từ chỗ khác, hoặc runtime báo đường dẫn khác, thì dừng với `ProximaControl.ModuleConflict`, không reset, không nạp đè.
- Đừng `Import-Module -Force` lần nữa (mất session và lựa chọn). Gỡ bằng `Remove-Module ProximaControl`: đóng session do module
  sở hữu và mất toàn bộ trạng thái.

## Mục tiêu (Target)
Mọi hành động trừ `help` cần đủ `-ConfigPath`, `-RepositoryRoot`, `-TargetId` (khớp Ordinal với tệp cấu hình). Không đích mặc định,
không dò môi trường hay thư mục hiện hành, không tự kết nối. Giá trị trong `<...>` là chỗ giữ:
```powershell
px config -ConfigPath '<ConfigPath>' -RepositoryRoot '<RepoRoot>' -TargetId '<TargetId>'
px models '<provider>' -ConfigPath '<ConfigPath>' -RepositoryRoot '<RepoRoot>' -TargetId '<TargetId>'
px use '<provider>' '<provider>/<model>' -ConfigPath '<ConfigPath>' -RepositoryRoot '<RepoRoot>' -TargetId '<TargetId>'
px ask '<provider>' 'Nội dung câu hỏi' -ConfigPath '<ConfigPath>' -RepositoryRoot '<RepoRoot>' -TargetId '<TargetId>'
px connect -ConfigPath '<ConfigPath>' -RepositoryRoot '<RepoRoot>' -TargetId '<TargetId>' -Credential (Get-Credential)
```
- Chỉ `connect` nhận `-Credential` (PSCredential); hành động khác không hỏi và không đọc thông tin đăng nhập.
- Không suy diễn: `ask` khi chưa `use` (và không có `-Model`) báo `NoModelSelected`; model không được quảng bá báo
  `ModelNotAdvertised`. Không fallback sang model hay đích khác, không tự thử lại.

## Xem trước (WhatIf)
`px` gọi ShouldProcess TRƯỚC mọi tác động, kể cả truy vấn `status`/`models`; mọi hành động có `-WhatIf` và `-Confirm`, wrapper chuyển
tiếp đúng hai cờ ấy. `-Force` chỉ vượt chốt "còn yêu cầu đang chờ" của `stop`/`restart`, KHÔNG BAO GIỜ vượt `-WhatIf`:
```powershell
px restart -ConfigPath '<ConfigPath>' -RepositoryRoot '<RepoRoot>' -TargetId '<TargetId>' -Force -WhatIf
& '<RepoRoot>\.agents\skills\proxima-control\scripts\Run-Px.ps1' stop -ConfigPath '<ConfigPath>' -RepositoryRoot '<RepoRoot>' -TargetId '<TargetId>' -WhatIf
```

## Phiên bản (Versions)
Ba miền danh tính tách biệt, không suy miền này từ miền kia:
1. Add-on trong repository: `ModuleVersion` 2.0.0 của manifest, cộng commit và tree Git chứa nó. Major 2 tách khỏi module 1.0.1
   đã thấy ở P0; không khẳng định module trên máy chủ đã được cập nhật.
2. Module điều khiển đã cài trên endpoint: cặp băm `moduleSha256` + `configModuleSha256` do handshake trả về khi `connect`.
3. Gateway runtime: `FileVersion` của `Proxima.exe` là NOT_MEASURED ở S2/S3; đo nó thuộc quan sát P4, không lén thêm vào S2.
   `status`/`models` không xác lập phiên bản runtime, quota, xác thực hay danh tính model upstream.

## Giới hạn (Limits)
- Kiểm listener là ảnh chụp và kiểm băm rồi mới import cũng vậy: đổi tiến trình/cổng/tệp chen giữa là race đã khai. Xác thực WinRM
  thật chưa được đo; băm chỉ ràng tương thích mã, không chứng thực máy chủ; dịch vụ bọc (kiểu NSSM) bị từ chối.
- Kiểm thử: `tests/ProximaManifest.Tests.ps1` (manifest, tài liệu), `tests/ProximaControl.Tests.ps1` (S2), `tests/ProximaConfig.Tests.ps1`
  (S1). Một lượt xanh không chứng minh bản đã triển khai trên máy nào.
