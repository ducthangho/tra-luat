---
name: proxima-control
description: Điều khiển MỘT đích Proxima khai báo tường minh qua px hoặc Run-Px.ps1 (trợ giúp, cấu hình, trạng thái, model, hỏi, start/stop/restart, connect/disconnect), luôn kèm ConfigPath, RepositoryRoot, TargetId và dùng -WhatIf để xem trước.
version: 2.1.0
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
px use '<provider>' '<model id>' -ConfigPath '<ConfigPath>' -RepositoryRoot '<RepoRoot>' -TargetId '<TargetId>'
px ask '<provider>' 'Nội dung câu hỏi' -ConfigPath '<ConfigPath>' -RepositoryRoot '<RepoRoot>' -TargetId '<TargetId>'
px connect -ConfigPath '<ConfigPath>' -RepositoryRoot '<RepoRoot>' -TargetId '<TargetId>' -Credential (Get-Credential)
```
- Model id lấy đúng nguyên văn từ `px models`. Id thuộc provider `P` khi nó bằng `P`, hoặc bắt đầu bằng `P:` (dạng Proxima quảng bá,
  ví dụ `chatgpt`, `chatgpt:thinking`), hoặc bắt đầu bằng `P/` (dạng cũ). So Ordinal; provider không được chứa `/` hay `:`.
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
1. Add-on trong repository: `ModuleVersion` 2.1.0 của manifest, cộng commit và tree Git chứa nó. Major 2 tách khỏi module 1.0.1
   đã thấy ở P0; không khẳng định module trên máy chủ đã được cập nhật.
2. Module điều khiển đã cài trên endpoint: cặp băm `moduleSha256` + `configModuleSha256` do handshake trả về khi `connect`.
3. Gateway runtime: `FileVersion` của `Proxima.exe` là NOT_MEASURED ở S2/S3; đo nó thuộc quan sát P4, không lén thêm vào S2.
   `status`/`models` không xác lập phiên bản runtime, quota, xác thực hay danh tính model upstream.

## Giới hạn (Limits)
- Kiểm listener là ảnh chụp và kiểm băm rồi mới import cũng vậy: đổi tiến trình/cổng/tệp chen giữa là race đã khai. Xác thực WinRM
  thật chưa được đo; băm chỉ ràng tương thích mã, không chứng thực máy chủ; dịch vụ bọc (kiểu NSSM) bị từ chối.
- Kiểm thử: `tests/ProximaManifest.Tests.ps1` (manifest, tài liệu), `tests/ProximaControl.Tests.ps1` (S2), `tests/ProximaConfig.Tests.ps1`
  (S1). Một lượt xanh không chứng minh bản đã triển khai trên máy nào.

## Kích hoạt (Activation guard)
Nạp riêng `scripts/ProximaActivation.psm1` khi kiểm tra kích hoạt. Mọi đường dẫn truyền vào phải là đường dẫn tuyệt đối đầy đủ;
đường dẫn tương đối, tham số thiếu hoặc sai kiểu đều trả `NOT_MEASURED` chứ không ném lỗi.
- `Test-ProximaArtifactTree` đối chiếu cây tệp với manifest và giá trị ghi đè. Thành công trả `OK`. Lỗi trả
  `REPARSE_POINT`, `DUPLICATE_CASE`, `ARTIFACT_EXTRA`, `ARTIFACT_MISSING` hoặc `ARTIFACT_CHANGED`. Kết quả là ảnh chụp tại
  lúc gọi: chạy ngay trước khi khởi động ứng dụng, vì tệp đổi sau đó thì không được phát hiện. Tên khai là mutable phải có
  trong manifest hoặc giá trị ghi đè, nếu không hàm trả `NOT_MEASURED`.
- `Enter-ProximaProfileGuard` cần thư mục profile đã tồn tại sẵn (hàm không tạo) và không phải liên kết. Hàm trả
  `PROFILE_BUSY` kèm `pid` và `rule` nếu phát hiện Proxima đang dùng profile, `PROFILE_LOCKED` nếu khoá đang được giữ, hoặc
  `ACQUIRED` kèm guard. Giữ guard suốt thời gian ứng dụng chạy rồi gọi `Exit-ProximaProfileGuard` để đóng khoá
  (`RELEASED`). Tệp khoá được giữ lại; tệp khoá có nội dung lạ thì hàm từ chối chứ không ghi đè.
- Giới hạn của chốt profile: tiến trình Proxima chạy quyền cao hơn hoặc của người dùng khác không lộ dòng lệnh, khi đó
  hàm trả `NOT_MEASURED` kèm `pid` chứ không coi là profile rảnh; danh sách tiến trình không chứa chính tiến trình gọi
  cũng vậy. Danh sách tiến trình là ảnh chụp, được lấy lại một lần sau khi giữ khoá; Proxima khởi động sau lần lấy thứ
  hai, hoặc do người tự mở bằng tay không qua guard, vẫn lọt. Đó là race còn lại và chốt chỉ phối hợp những bên gọi guard.
- `Test-ProximaPromotionFence` trả `ALLOWED` nếu được chuyển tiếp theo thứ tự host. Khi bị chặn, hàm trả
  `FENCE_TARGET_UNKNOWN`, `FENCE_PRIOR_MISSING`, `FENCE_RECEIPT_INVALID`, `FENCE_PRIOR_FAILED` hoặc
  `FENCE_ARTIFACT_MISMATCH`. Băm artifact phải đủ 64 ký tự hex và kế hoạch không được lặp host, nếu không hàm trả
  `NOT_MEASURED`.
- Lỗi ngoài dự kiến trả `NOT_MEASURED` kèm thông tin lỗi. Kiểm thử: `tests/ProximaActivation.Tests.ps1`.

## Gỡ cài đặt (Uninstall residue)
Bộ gỡ chính thức của Proxima per-user (phiên bản 5.5, bản vá 0) luôn để lại thư mục rỗng `%LOCALAPPDATA%\Programs\Proxima` và
`%LOCALAPPDATA%\proxima-updater\installer.exe`. Nạp riêng `scripts/ProximaInstall.psm1` (không qua manifest) để dọn hai thứ đó. Hàm
`Remove-ProximaUninstallResidue` không chạy bộ gỡ, không cài, không mở Proxima, chỉ đọc registry, và chỉ xoá đúng hai đích trên.
1. Chạy bộ gỡ của nhà cung cấp: `"<dir>\Uninstall Proxima.exe" /currentuser /S`.
2. Chờ cả các tiến trình `Un_*`/`Au_*` do bộ gỡ tự nhân bản kết thúc; bộ gỡ chạy bất đồng bộ nên lệnh ở bước 1 trả về sớm.
3. Xem trước bằng `-WhatIf`, đọc kết quả, rồi mới dọn:
```powershell
Remove-ProximaUninstallResidue -WhatIf
Remove-ProximaUninstallResidue
```
- Kết quả có `ok`, `code`, `actions` (việc đã làm, hoặc việc sẽ làm khi `-WhatIf`), `before`, `after`, `error`. Thành công:
  `CLEANED` hoặc `NOTHING_TO_DO` (`ok` là true). `-WhatIf` trả `WOULD_REMOVE` (`ok` là false vì chưa dọn gì) hoặc `NOTHING_TO_DO`.
- Luôn trả trước khi xoá bất cứ thứ gì: `UNINSTALL_RUNNING` (còn tiến trình `Proxima`, `Un_*` hoặc `Au_*`), `STILL_INSTALLED` (còn
  khoá gỡ cài đặt có tên bắt đầu bằng `Proxima`, hoặc còn `Proxima.exe`), `BAD_ARGUMENT`, `RESIDUE_UNEXPECTED`.
- `RESIDUE_UNEXPECTED`: có thứ ngoài dự kiến (thư mục cài còn tệp, updater có thêm mục, bộ cài sai kích thước hoặc sai băm, có
  junction/symlink). **Phải có người xem**; không tự xoá tay, không chạy lại với băm khác chỉ để cho qua.
- Có thể trả sau khi đã xoá một phần, khi đó `actions` ghi đúng việc đã làm và cần người xem:
  `RESIDUE_CHANGED` (đích bị đổi giữa lúc kiểm và lúc xoá; updater được trả về tên cũ khi bộ cài chưa bị xoá, nếu không thì `actions`
  ghi đường dẫn `proxima-updater.pxu-<GUID>` còn giữ lại; junction xuất hiện ở thư mục cài thì chỉ gỡ liên kết, không đụng đích),
  `CLEAN_INCOMPLETE` (đã xoá nhưng kiểm kê sau vẫn còn đích) và `NOT_MEASURED` (lỗi ngoài dự kiến, kể cả lỗi I/O giữa chừng; xem `error`).
- Chống đua: mỗi đích được mở bằng handle không chia sẻ quyền xoá, kiểm trên chính handle đó (không phải liên kết, đường dẫn cuối
  của handle khớp vị trí chuẩn nên tổ tiên bị tráo thành junction sẽ lộ, băm bộ cài đọc qua handle), rồi xoá bằng chính handle.
  Khoảng hở còn lại là từ lần kiểm sơ bộ tới lúc mở handle: đổi thay trong khoảng đó được phát hiện và trả `RESIDUE_CHANGED`,
  không bị xoá theo. Danh sách tiến trình và khoá registry vẫn chỉ là ảnh chụp tại lúc gọi.
- Giới hạn: chỉ cho bản cài per-user nói trên với băm bộ cài đã biết; bản khác phải truyền `-InstallerSha256` và `-InstallerBytes`
  tương ứng. Kiểm thử: `tests/ProximaInstall.Tests.ps1`.
