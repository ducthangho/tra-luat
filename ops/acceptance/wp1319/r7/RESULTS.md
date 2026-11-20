# WP1319 r7 — Ghi quyết định của chủ kho 19/11 và tiền kiểm chỉ đọc cho U11

**Căn cứ:** đặc tả `ops/specs/wp1319-r7.md` (sha256 `3f44db51…`), lease `ops/leases/wp1319-r7-g1-operator.yaml`.

## 1. Quyết định của chủ kho (ghi vào MATRIX mục I)
Chủ kho trả lời trong phiên điều phối ngày 19/11 (AskUserQuestion). Đây là lời khai của phiên điều phối; không có bản ghi trên GitHub.
| Mục | Lựa chọn của chủ kho | Ghi vào MATRIX |
|---|---|---|
| U5/U12 | "Chấp nhận theo digest" | `accepted_risk`; dữ kiện `NotSigned`, không provenance giữ nguyên |
| U11, §11 #2 | "Cấp đo chỉ đọc trên f728" | r7 tiền kiểm (mục 2); lượt xác thực thật cần đặc tả riêng |
| §11 #10 | "Chấp nhận mức fixture" | `owner_waived` ở mức fixture; dữ kiện `partial` giữ nguyên |
| Đóng WP con | "Đóng kèm miễn trừ" | Đã đóng 19/11 21:42Z; biên bản M8 trên từng Issue |

**Đóng 5 WP con:** mỗi WP có một biên bản M8 dạng YAML trên Issue. Cả 5 đều land cùng merge `96b6a33d` của PR #1378. `kiem-dong-wp` cho `ĐÓNG ĐƯỢC WP` với lease cuối của từng WP. Phản chứng: đổi các hàng `owner_waived` thành `partial` thì cổng chặn ở D2. Biên bản được đọc lại qua REST và khớp từng byte với tệp gốc.
| WP | Issue comment | sha256 khối YAML |
|---|---|---|
| WP-PXA #1401 | `issuecomment-7022988362` | `232764cbd2b14ddf…` |
| WP-NSIS #1405 | `issuecomment-7022997734` | `e0b8286d65fac1ec…` |
| WP-PXU #1409 | `issuecomment-7023002175` | `b3952176630c7ea4…` |
| WP-U8 #1410 | `issuecomment-7023006731` | `dc87287758ffb6cc…` |
| WP-PXL #1413 | `issuecomment-7023011613` | `4cfcd91f71436868…` |

Các hàng `owner_waived` giữ nguyên kết quả đo. Lý do của từng hàng ghi trong `mien_tru_chi_tiet` của biên bản; không hàng nào được nâng mức.

## 2. Tiền kiểm chỉ đọc cho U11
Không xác thực, không `New-PSSession`, không `Get-Credential`, không gọi Proxima. Không ghi gì ngoài thư mục làm việc của phiên.

### Các lượt chạy
| Máy | Lượt | Script | Kết quả |
|---|---|---|---|
| VM `f7281f27` (`tra-luat-win`) | 1 | `R7VM.ps1` `ab9c4d4f…` | **Đạt.** `OK=True`, JSON `cc6d50d7…` (23:25:18Z) |
| ASUS `7404cfba` | 1 | `R7CTL.ps1` bản 1 `bf391101…` | **Hỏng do lỗi dựng** sau 433 s: `Argument types do not match`, không có JSON. Dòng gây lỗi **không đo được**: pwsh in dạng gọn, không có số dòng. Thử riêng trên ASUS hai biểu thức bị nghi (`$h.keys = …` trên `[ordered]` và `[Uri]::TryCreate` với `[ref]$null`): cả hai đều chạy êm, nên nghi vấn bị bác |
| ASUS | 2 (lượt dựng lại duy nhất) | `R7CTL.ps1` bản 2 `92f5c141…` | **Đạt.** `OK=True`, `errs` rỗng, JSON `818ed2c5…` (23:36:22Z), 197 s |
| Desktop `a5f7076e` | 1 | bản 1 `bf391101…` | **Hỏng do lỗi dựng**, cùng thông báo, sau 1 348 s. Không có JSON |
| Desktop | 2 (lượt dựng lại duy nhất) | bản 2 `92f5c141…` | **Đạt.** `OK=True`, `errs` rỗng, JSON `61ca9ec1…` (23:58:01Z), 1 158 s |

Bản 2 khác bản 1 ở ba điểm:
- mọi phép gán vào từ điển dùng chỉ mục (`$h['k']`);
- bỏ `[Uri]::TryCreate` với `[ref]`;
- mỗi bước bọc `try` và ghi số dòng lỗi vào `errs`.

Desktop: lần gửi lệnh chạy lại đầu tiên bị đứt do worker khởi động lại. Trước khi gửi lại, tôi kiểm thấy **chưa** có tệp log `r7-desktop-2.log`, mà lệnh chuyển hướng `*>` sẽ tạo tệp này ngay khi script bắt đầu. Vậy chỉ có một lượt chạy lại, không có lượt chạy chồng.

### Kết quả
**VM `f7281f27`:**
- Desktop Commander chạy dưới `TRA-LUAT-WIN\tlcommander`, **không** phải admin.
- Cổng `5985` và `5986` đang nghe trên `::`, PID 4 (System, tức http.sys).
- `Get-Service WinRM` báo *không tìm thấy dịch vụ*. `WSMan:\localhost\Listener` báo *không có đường dẫn*. `Get-PSSessionConfiguration` đòi quyền admin. Với tài khoản không admin, cả ba câu trả lời này **không** chứng minh WinRM vắng hay có.
- Module `ProximaControl` 1.0.1 nằm tại `C:\ProgramData\TraLuatCommander\profile\Documents\PowerShell\Modules\ProximaControl\1.0.1\`:
  - `.psd1` có sha256 `3f2ac59e…`, khớp băm khảo sát P0 ngày 05/11;
  - `.psm1` có sha256 `ef4821cc…`.

**ASUS:**
- 13 tệp có khoá `connectionUri`. Không tệp nào là cấu hình điều khiển thật:
  - 6 bản `config.example.json` (`gateway.example.invalid`);
  - 7 tệp `settings.json` chế độ `Local`, không có host, trong `Documents\Codex\2026-11-02\task-7\verification-temp\`.
- `tra-luat-win`: **không phân giải được** (`MethodInvocationException`), nên TCP tới `5985`/`5986` không mở (`SocketException`).

**Desktop:**
- 399 tệp có khoá `connectionUri`, **tất cả** nằm dưới `C:\tl-win` hoặc `F:\tl-win`; không tệp nào nằm trong hồ sơ người dùng.
- Phân theo host: `gateway.example.invalid` 311 · `127.0.0.1` (cổng test 5986x) 56 · `gw.example.invalid` 28 · không có host 4. Bốn tệp không có host gồm:
  - hai báo cáo probe `wp1271-r9`, không phải cấu hình;
  - hai fixture `x.json` của harness r1 có URI không hợp lệ (`parse_error`).
- **Không có** host nào ngoài các host mẫu và test.
- `tra-luat-win`: **không phân giải được**:
  - `5985`: không mở, không có `connect_error` (`Wait(3000)` hết hạn);
  - `5986`: không mở, `SocketException`.
- JSON Desktop (7 236 dòng) **không** được chuyển về container vì dài. Số liệu trên do lệnh tổng hợp chạy trên chính tệp `r7-desktop-2.json` (sha256 `61ca9ec1…`) tại Desktop, chép nguyên văn ở mục *Lệnh*.

### Hệ quả cho lượt đo xác thực thật (r8)
- Không máy điều khiển nào có cấu hình px thật trỏ tới VM.
- Từ Desktop và ASUS, tên `tra-luat-win` không phân giải được.

Vậy lượt r8 cần chủ kho cung cấp:
1. địa chỉ của VM mà máy điều khiển dùng (`connectionUri`, cổng, HTTP hay HTTPS);
2. `configurationName` của endpoint (r7 không đọc được vì thiếu quyền admin trên VM);
3. tự nhập thông tin đăng nhập vào `Get-Credential` trên máy điều khiển. Phiên điều phối không đọc, không lưu.

Lượt r8 chỉ chạy `px connect`, `px status` (`GET /api/status`, không inference) và `px disconnect`, và cần đặc tả cùng review riêng.

## Lệnh
VM (pwsh 7.6.9):
```powershell
$d='C:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\r7'; 'SCRIPT=' + (Get-FileHash -Algorithm SHA256 "$d\R7VM.ps1").Hash.ToLowerInvariant(); $pe=$null; $tk=$null; [void][Management.Automation.Language.Parser]::ParseFile("$d\R7VM.ps1",[ref]$tk,[ref]$pe); 'PARSE_ERRORS=' + @($pe).Count; & "$d\R7VM.ps1" -Out "$d\r7-vm.json" *> "$d\r7-vm.log"; 'OK=' + $?; Get-Content "$d\r7-vm.log"
```
Đầu ra: `SCRIPT=ab9c4d4f…`, `PARSE_ERRORS=0`, `OK=True`, `SHA256=cc6d50d7372e7e16610e2857b8f92030a3f18b32e15eecd3961047572dc7d25a`.

ASUS lượt 2 và Desktop lượt 2 dùng cùng mẫu lệnh với `R7CTL.ps1`. Thư mục làm việc là `C:\Users\admin\tl-work\r7-session_015GtxrapMSm976JLC7Fp1HM` trên ASUS và `F:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\r7` trên Desktop. Tệp ra là `r7-asus-2.json` và `r7-desktop-2.json`.
- ASUS: `SCRIPT=92f5c141…`, `PARSE_ERRORS=0`, `OK=True`, `SHA256=818ed2c5b2d8fe50482b266b64f8312d51f725b76d5a317a40e1fe5a75236237`.
- Desktop: `SCRIPT=92f5c141…`, `PARSE_ERRORS=0`, `OK=True`, `SHA256=61ca9ec1dc90c677501b53233e25c36d2e08b62e632ff49dffcac169794ce9cd`.

Script `.ps1` gọi trong cùng tiến trình nên không đặt `$LASTEXITCODE`. Bằng chứng thành công là `$?` = `True` (hai lượt hỏng cho `OK=False`), cùng dòng `SHA256=`, dòng cuối của script, chỉ in ra sau khi JSON đã ghi xong.

Lệnh tổng hợp chạy trên Desktop (chỉ đọc tệp JSON của phiên):
```powershell
$j = Get-Content -Raw 'F:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\r7\r7-desktop-2.json' | ConvertFrom-Json; 'ERRS=' + @($j.errs).Count; 'CONFIGS=' + @($j.configs).Count; $j.configs | Group-Object { "$($_.uri_host)|$($_.mode)" } | Sort-Object Count -Descending | ForEach-Object { 'HOST ' + $_.Name + ' = ' + $_.Count }; 'NONFIXTURE:'; $j.configs | Where-Object { $_.uri_host -and $_.uri_host -notin 'gateway.example.invalid','gw.example.invalid','127.0.0.1' } | ForEach-Object { $_.path + ' | ' + $_.uri_host + ':' + $_.uri_port + ' | ' + $_.targetId + ' | ' + $_.configurationName }; 'OUTSIDE_TLWIN:'; $j.configs | Where-Object { $_.path -notlike 'C:\tl-win\*' -and $_.path -notlike 'F:\tl-win\*' } | ForEach-Object { $_.path + ' | ' + $_.uri_host + ' | ' + $_.mode }; 'TCP:'; $j.tcp | ConvertTo-Json -Compress
```
```text
ERRS=0
CONFIGS=399
HOST gateway.example.invalid|Remote = 311
HOST 127.0.0.1|Remote = 56
HOST gw.example.invalid|Remote = 23
HOST gw.example.invalid|Local = 5
HOST | = 2
HOST |Remote = 2
NONFIXTURE:
OUTSIDE_TLWIN:
TCP:
[{"target":"tra-luat-win","port":5985,"resolved":[],"resolve_error":"MethodInvocationException","open":false},{"target":"tra-luat-win","port":5986,"resolved":[],"resolve_error":"MethodInvocationException","open":false,"connect_error":"SocketException"}]
```

## Giới hạn
- VM: tài khoản không admin nên không đọc được listener WinRM, session configuration và trạng thái dịch vụ. Cổng đang nghe **không** chứng minh endpoint nào được cấu hình hay ai được quyền vào.
- Chỉ quét tệp `*.json` dưới 64 KiB trong hồ sơ người dùng và `*:\tl-win` (độ sâu ≤ 6). Cấu hình ở nơi khác, hoặc lưu ở định dạng khác, nằm ngoài phép đo.
- Phân giải tên chỉ thử `tra-luat-win`. Địa chỉ IP hay tên khác của VM chưa thử, vì không có trong cấu hình nào tìm được.
- Lỗi của bản 1 không truy được tới dòng gây lỗi.

## Bằng chứng nguyên văn
`r7-vm.json`: sha256 `cc6d50d7…` (CRLF giữa các dòng, một LF ở cuối; đổi mỗi LF trong khối thành CRLF rồi thêm LF ở cuối sẽ ra đúng băm; đã kiểm trong container).
```json
{
  "schema": "wp1319_r7_vm.v1",
  "utc": "2026-11-19T23:25:18.7728298Z",
  "host": "TRA-LUAT-WIN",
  "ps": "7.6.9",
  "errs": [
    "winrm_service: Cannot find any service with service name 'WinRM'.",
    "wsman_listener: ItemNotFoundException: Cannot find path 'localhost\\Listener' because it does not exist.",
    "session_config: InvalidOperationException: Access is denied. To run this cmdlet, start PowerShell with the \"Run as administrator\" option."
  ],
  "user": "TRA-LUAT-WIN\\tlcommander",
  "is_admin": false,
  "listen_ports": [
    {
      "addr": "::",
      "port": 5986,
      "pid": 4
    },
    {
      "addr": "::",
      "port": 5985,
      "pid": 4
    }
  ],
  "proxima_control": [
    {
      "path": "C:\\ProgramData\\TraLuatCommander\\profile\\Documents\\PowerShell\\Modules\\ProximaControl\\1.0.1\\ProximaControl.psd1",
      "version": "1.0.1",
      "ProximaControl.psd1": "3f2ac59e201128f03d047da69698567b75675917687d75e8312fd7e34f14ee77",
      "ProximaControl.psm1": "ef4821cc14ba7234705c42b470d502ceea93982c379871e292d7e7f830ca1344"
    }
  ]
}
```

`r7-asus-2.json`: sha256 `818ed2c5…`, cùng quy ước CRLF; đã kiểm trong container.
```json
{
  "schema": "wp1319_r7_ctl.v2",
  "utc": "2026-11-19T23:36:22.0280320Z",
  "host": "ASUS-LAPTOP",
  "ps": "7.6.10",
  "errs": [],
  "scan_roots": [
    "C:\\Users\\admin",
    "D:\\tl-win"
  ],
  "configs": [
    {
      "path": "C:\\Users\\admin\\Documents\\Codex\\2026-11-02\\task-7\\verification-temp\\settings.json",
      "sha256": "c52a1fa39fa9ae80d3853cd5a51d7c1e300449c642e04618c00be739f37e6856",
      "top_keys": [
        "mode",
        "basePath",
        "connectionUri",
        "configurationName",
        "defaults"
      ],
      "targetId": "",
      "mode": "Local",
      "configurationName": "Microsoft.PowerShell",
      "uri_host": null
    },
    {
      "path": "C:\\Users\\admin\\Documents\\Codex\\2026-11-02\\task-7\\verification-temp\\3d6f3f8530f44feea6a086721d49fe40\\settings.json",
      "sha256": "c52a1fa39fa9ae80d3853cd5a51d7c1e300449c642e04618c00be739f37e6856",
      "top_keys": [
        "mode",
        "basePath",
        "connectionUri",
        "configurationName",
        "defaults"
      ],
      "targetId": "",
      "mode": "Local",
      "configurationName": "Microsoft.PowerShell",
      "uri_host": null
    },
    {
      "path": "C:\\Users\\admin\\Documents\\Codex\\2026-11-02\\task-7\\verification-temp\\3ec412665a5c4442a071b83c0c035c08\\settings.json",
      "sha256": "c52a1fa39fa9ae80d3853cd5a51d7c1e300449c642e04618c00be739f37e6856",
      "top_keys": [
        "mode",
        "basePath",
        "connectionUri",
        "configurationName",
        "defaults"
      ],
      "targetId": "",
      "mode": "Local",
      "configurationName": "Microsoft.PowerShell",
      "uri_host": null
    },
    {
      "path": "C:\\Users\\admin\\Documents\\Codex\\2026-11-02\\task-7\\verification-temp\\8bc852e65cc043c18eb2eebd740f0af0\\settings.json",
      "sha256": "c52a1fa39fa9ae80d3853cd5a51d7c1e300449c642e04618c00be739f37e6856",
      "top_keys": [
        "mode",
        "basePath",
        "connectionUri",
        "configurationName",
        "defaults"
      ],
      "targetId": "",
      "mode": "Local",
      "configurationName": "Microsoft.PowerShell",
      "uri_host": null
    },
    {
      "path": "C:\\Users\\admin\\Documents\\Codex\\2026-11-02\\task-7\\verification-temp\\9a91d2dce0af4d0e98c08e1ff0fb1840\\settings.json",
      "sha256": "c52a1fa39fa9ae80d3853cd5a51d7c1e300449c642e04618c00be739f37e6856",
      "top_keys": [
        "mode",
        "basePath",
        "connectionUri",
        "configurationName",
        "defaults"
      ],
      "targetId": "",
      "mode": "Local",
      "configurationName": "Microsoft.PowerShell",
      "uri_host": null
    },
    {
      "path": "C:\\Users\\admin\\Documents\\Codex\\2026-11-02\\task-7\\verification-temp\\af16cc27c0f44287be2a10a97f70d52e\\settings.json",
      "sha256": "c52a1fa39fa9ae80d3853cd5a51d7c1e300449c642e04618c00be739f37e6856",
      "top_keys": [
        "mode",
        "basePath",
        "connectionUri",
        "configurationName",
        "defaults"
      ],
      "targetId": "",
      "mode": "Local",
      "configurationName": "Microsoft.PowerShell",
      "uri_host": null
    },
    {
      "path": "C:\\Users\\admin\\Documents\\Codex\\2026-11-02\\task-7\\verification-temp\\fb27462dfb4a4a40bcf0e05f5a4f0fdb\\settings.json",
      "sha256": "c52a1fa39fa9ae80d3853cd5a51d7c1e300449c642e04618c00be739f37e6856",
      "top_keys": [
        "mode",
        "basePath",
        "connectionUri",
        "configurationName",
        "defaults"
      ],
      "targetId": "",
      "mode": "Local",
      "configurationName": "Microsoft.PowerShell",
      "uri_host": null
    },
    {
      "path": "C:\\Users\\admin\\tl-work\\mission1238-asus-20261112-P3\\repo\\.agents\\skills\\proxima-control\\config.example.json",
      "sha256": "ddc7a15c729c579ec0d068912a8880da5ad4c0ed6e9826ba1ba60088abe1fa92",
      "top_keys": [
        "schemaVersion",
        "targetId",
        "mode",
        "basePath",
        "connectionUri",
        "configurationName"
      ],
      "targetId": "example-target",
      "mode": "Remote",
      "configurationName": "Example.Endpoint",
      "uri_host": "gateway.example.invalid",
      "uri_port": 5986,
      "uri_scheme": "https"
    },
    {
      "path": "C:\\Users\\admin\\tl-work\\wp-pxa\\tree\\.agents\\skills\\proxima-control\\config.example.json",
      "sha256": "ddc7a15c729c579ec0d068912a8880da5ad4c0ed6e9826ba1ba60088abe1fa92",
      "top_keys": [
        "schemaVersion",
        "targetId",
        "mode",
        "basePath",
        "connectionUri",
        "configurationName"
      ],
      "targetId": "example-target",
      "mode": "Remote",
      "configurationName": "Example.Endpoint",
      "uri_host": "gateway.example.invalid",
      "uri_port": 5986,
      "uri_scheme": "https"
    },
    {
      "path": "C:\\Users\\admin\\tl-work\\wp-pxa\\tree2\\.agents\\skills\\proxima-control\\config.example.json",
      "sha256": "ddc7a15c729c579ec0d068912a8880da5ad4c0ed6e9826ba1ba60088abe1fa92",
      "top_keys": [
        "schemaVersion",
        "targetId",
        "mode",
        "basePath",
        "connectionUri",
        "configurationName"
      ],
      "targetId": "example-target",
      "mode": "Remote",
      "configurationName": "Example.Endpoint",
      "uri_host": "gateway.example.invalid",
      "uri_port": 5986,
      "uri_scheme": "https"
    },
    {
      "path": "C:\\Users\\admin\\tl-work\\wp1303-asus-748-windows-g7\\.agents\\skills\\proxima-control\\config.example.json",
      "sha256": "ddc7a15c729c579ec0d068912a8880da5ad4c0ed6e9826ba1ba60088abe1fa92",
      "top_keys": [
        "schemaVersion",
        "targetId",
        "mode",
        "basePath",
        "connectionUri",
        "configurationName"
      ],
      "targetId": "example-target",
      "mode": "Remote",
      "configurationName": "Example.Endpoint",
      "uri_host": "gateway.example.invalid",
      "uri_port": 5986,
      "uri_scheme": "https"
    },
    {
      "path": "C:\\Users\\admin\\tl-work\\wp1303-windows-bundle-M\\base\\.agents\\skills\\proxima-control\\config.example.json",
      "sha256": "ddc7a15c729c579ec0d068912a8880da5ad4c0ed6e9826ba1ba60088abe1fa92",
      "top_keys": [
        "schemaVersion",
        "targetId",
        "mode",
        "basePath",
        "connectionUri",
        "configurationName"
      ],
      "targetId": "example-target",
      "mode": "Remote",
      "configurationName": "Example.Endpoint",
      "uri_host": "gateway.example.invalid",
      "uri_port": 5986,
      "uri_scheme": "https"
    },
    {
      "path": "C:\\Users\\admin\\tl-work\\wp1303-windows-bundle-M\\candidate\\.agents\\skills\\proxima-control\\config.example.json",
      "sha256": "ddc7a15c729c579ec0d068912a8880da5ad4c0ed6e9826ba1ba60088abe1fa92",
      "top_keys": [
        "schemaVersion",
        "targetId",
        "mode",
        "basePath",
        "connectionUri",
        "configurationName"
      ],
      "targetId": "example-target",
      "mode": "Remote",
      "configurationName": "Example.Endpoint",
      "uri_host": "gateway.example.invalid",
      "uri_port": 5986,
      "uri_scheme": "https"
    }
  ],
  "tcp": [
    {
      "target": "tra-luat-win",
      "port": 5985,
      "resolved": [],
      "resolve_error": "MethodInvocationException",
      "open": false,
      "connect_error": "SocketException"
    },
    {
      "target": "tra-luat-win",
      "port": 5986,
      "resolved": [],
      "resolve_error": "MethodInvocationException",
      "open": false,
      "connect_error": "SocketException"
    }
  ]
}
```

### Script `R7VM.ps1` (sha256 `ab9c4d4fec3065efe19789b73a3f8c7f3341e9b4df801e527932f2b5389cf437`, LF; khối dưới cộng LF ở cuối ra đúng băm)
```powershell
# WP1319 r7 (ops/specs/wp1319-r7.md) muc 2, VM: tien kiem CHI DOC cho U11. Khong xac thuc, khong goi Proxima.
param([Parameter(Mandatory)][string]$Out)
$ErrorActionPreference = 'Stop'
$Res = [ordered]@{ schema = 'wp1319_r7_vm.v1'; utc = (Get-Date).ToUniversalTime().ToString('o'); host = $env:COMPUTERNAME; ps = "$($PSVersionTable.PSVersion)"; errs = @() }
try {
  $id = [Security.Principal.WindowsIdentity]::GetCurrent()
  $Res.user = $id.Name
  $Res.is_admin = ([Security.Principal.WindowsPrincipal]$id).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
} catch { $Res.errs += "identity: $($_.Exception.Message)" }
try { $svc = Get-Service -Name WinRM; $Res.winrm_service = [ordered]@{ status = "$($svc.Status)"; start_type = "$($svc.StartType)" } } catch { $Res.errs += "winrm_service: $($_.Exception.Message)" }
try { $Res.listen_ports = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in 5985, 5986 } | ForEach-Object { [ordered]@{ addr = "$($_.LocalAddress)"; port = $_.LocalPort; pid = $_.OwningProcess } }) } catch { $Res.errs += "ports: $($_.Exception.Message)" }
try { $Res.wsman_listeners = @(Get-ChildItem -Path WSMan:\localhost\Listener -ErrorAction Stop | ForEach-Object { [ordered]@{ name = $_.Name; keys = @($_.Keys) } }) } catch { $Res.errs += "wsman_listener: $($_.Exception.GetType().Name): $($_.Exception.Message)" }
try { $Res.session_configs = @(Get-PSSessionConfiguration -ErrorAction Stop | ForEach-Object { [ordered]@{ name = $_.Name; permission = "$($_.Permission)"; run_as = "$($_.RunAsUser)" } }) } catch { $Res.errs += "session_config: $($_.Exception.GetType().Name): $($_.Exception.Message)" }
try {
  $Res.proxima_control = @(Get-Module -ListAvailable -Name ProximaControl | ForEach-Object {
      $dir = Split-Path -Parent $_.Path
      $m = [ordered]@{ path = $_.Path; version = "$($_.Version)" }
      foreach ($fn in 'ProximaControl.psd1', 'ProximaControl.psm1') { $fp = Join-Path $dir $fn; if (Test-Path -LiteralPath $fp) { $m[$fn] = (Get-FileHash -Algorithm SHA256 -LiteralPath $fp).Hash.ToLowerInvariant() } }
      $m })
} catch { $Res.errs += "module: $($_.Exception.Message)" }
$json = $Res | ConvertTo-Json -Depth 6
[IO.File]::WriteAllText($Out, $json + "`n", [Text.UTF8Encoding]::new($false))
'SHA256=' + (Get-FileHash -Algorithm SHA256 -LiteralPath $Out).Hash.ToLowerInvariant()
```

### Script `R7CTL.ps1` bản 2 (sha256 `92f5c141d71ebdcb30bf586b99d7685ec5e33d0a328f8874685349bdc5a11027`, LF; khối dưới cộng LF ở cuối ra đúng băm)
```powershell
# WP1319 r7 (ops/specs/wp1319-r7.md) muc 2, may dieu khien: tim cau hinh px va thu TCP toi VM. Khong xac thuc.
# Ban 2: moi buoc boc try va ghi so dong loi; luot 1 ASUS hong "Argument types do not match" khong ro dong.
param([Parameter(Mandatory)][string]$Out)
$ErrorActionPreference = 'Stop'
$Res = [ordered]@{ schema = 'wp1319_r7_ctl.v2'; utc = (Get-Date).ToUniversalTime().ToString('o'); host = $env:COMPUTERNAME; ps = "$($PSVersionTable.PSVersion)"; errs = [Collections.Generic.List[string]]::new() }
function Add-Err([string]$Step, $Er) { $Res['errs'].Add("${Step} L$($Er.InvocationInfo.ScriptLineNumber): $($Er.Exception.GetType().FullName): $($Er.Exception.Message)") }
$scan = @()
try { $scan = @(@($env:USERPROFILE, 'C:\tl-win', 'F:\tl-win', 'D:\tl-win') | Where-Object { $_ -and (Test-Path -LiteralPath $_) }) } catch { Add-Err 'roots' $_ }
$Res['scan_roots'] = $scan
$hits = [Collections.Generic.List[object]]::new()
foreach ($sr in $scan) {
  $files = @()
  try { $files = @(Get-ChildItem -LiteralPath $sr -Recurse -Depth 6 -File -Filter '*.json' -ErrorAction SilentlyContinue | Where-Object { $_.Length -lt 65536 }) } catch { Add-Err "list $sr" $_ }
  foreach ($fi in $files) {
    try {
      $txt = [IO.File]::ReadAllText($fi.FullName)
      if ($txt -notmatch '"connectionUri"') { continue }
      $h = [ordered]@{}
      $h['path'] = [string]$fi.FullName
      $h['sha256'] = (Get-FileHash -Algorithm SHA256 -LiteralPath $fi.FullName).Hash.ToLowerInvariant()
      try {
        $o = $txt | ConvertFrom-Json
        $h['top_keys'] = @($o.PSObject.Properties.Name | ForEach-Object { [string]$_ })
        $h['targetId'] = [string]$o.targetId; $h['mode'] = [string]$o.mode; $h['configurationName'] = [string]$o.configurationName
        $h['uri_host'] = $null
        $cu = [string]$o.connectionUri
        if ($cu) { $uo = [Uri]$cu; $h['uri_host'] = [string]$uo.Host; $h['uri_port'] = [int]$uo.Port; $h['uri_scheme'] = [string]$uo.Scheme }
      } catch { $h['parse_error'] = "L$($_.InvocationInfo.ScriptLineNumber): $($_.Exception.GetType().Name)" }
      $hits.Add($h)
    } catch { Add-Err "read $($fi.FullName)" $_ }
  }
}
$Res['configs'] = @($hits)
$tcpList = [Collections.Generic.List[object]]::new()
foreach ($port in 5985, 5986) {
  $t = [ordered]@{}
  $t['target'] = 'tra-luat-win'; $t['port'] = [int]$port
  try { $t['resolved'] = @([Net.Dns]::GetHostAddresses('tra-luat-win') | ForEach-Object { [string]$_ }) } catch { $t['resolved'] = @(); $t['resolve_error'] = $_.Exception.GetType().Name }
  try {
    $c = [Net.Sockets.TcpClient]::new()
    try { $ok = $c.ConnectAsync('tra-luat-win', [int]$port).Wait(3000); $t['open'] = [bool]($ok -and $c.Connected) } finally { $c.Dispose() }
  } catch { $t['open'] = $false; $t['connect_error'] = $_.Exception.GetBaseException().GetType().Name }
  $tcpList.Add($t)
}
$Res['tcp'] = @($tcpList)
$Res['errs'] = @($Res['errs'])
$json = $Res | ConvertTo-Json -Depth 6
[IO.File]::WriteAllText($Out, $json + "`n", [Text.UTF8Encoding]::new($false))
'SHA256=' + (Get-FileHash -Algorithm SHA256 -LiteralPath $Out).Hash.ToLowerInvariant()
```
