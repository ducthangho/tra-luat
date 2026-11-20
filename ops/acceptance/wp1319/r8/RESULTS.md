# WP1319 r8 — Đường mạng ASUS → VM và tên endpoint cho U11 (đo chỉ đọc)

**Căn cứ:** đặc tả `ops/specs/wp1319-r8.md` (sha256 `63201732…`), lease `ops/leases/wp1319-r8-g1-operator.yaml`. Chủ kho bảo ngày 20/11: *"Thử dùng máy ASUS đi"*. Không xác thực, không gọi HTTP; chỉ TCP connect, không gửi byte nào.

## Lượt chạy (mỗi máy 1 lượt, cả hai đạt)
| Máy | Script | Kết quả |
|---|---|---|
| VM `f7281f27` | `R8VM.ps1` `677ccfb8…`, parse 0 lỗi | `OK=True`, JSON `464e3eb0…` (01:07:03Z) |
| ASUS `7404cfba` | `R8ASUS.ps1` `9c55a00f…`, parse 0 lỗi, `-VmIp '10.70.0.2'` (lấy từ JSON của VM) | `OK=True`, JSON `af345e0b…` (01:08:38Z) |

## Kết quả
- **VM:**
  - IPv4 `10.70.0.2/24` trên card `Ethernet`, gateway mặc định `10.70.0.1`.
  - Không có tệp `*.pssc`/`*.psrc` nào dưới `C:\ProgramData\TraLuatCommander` (độ sâu ≤ 6).
  - Không đọc được khoá registry plugin WSMan: `SecurityException`, tài khoản `tlcommander` không phải admin.
  - Tên endpoint vì vậy **vẫn chưa biết**.
- **ASUS:**
  - Không có card nào thuộc `10.70.0.0/24`. ASUS có Wi-Fi `10.86.15.11/20`, `vEthernet (WSL …)` `172.18.32.1/20`, `vEthernet (Default Switch)` `172.29.48.1/20` và các địa chỉ link-local `169.254.x`.
  - Tệp `hosts` không có dòng nào chứa `tra-luat`.
  - Bảng hàng xóm IPv4 không có `10.70.0.x`.
  - `Get-VM` bị từ chối (`VirtualizationException`, thiếu quyền), nên **không đo được** VM có chạy trên Hyper-V của ASUS hay không.
  - TCP tới `10.70.0.2` cổng `5985` và `5986`: **không mở**. Cả hai lần `Wait(3000)` hết hạn, không có `connect_error`.

## Ghi nhận
- **Từ ASUS, hiện không có đường mạng tới cổng WinRM của VM.**
  - Đã đo: ASUS không cùng mạng `10.70.0.0/24`, và TCP tới `10.70.0.2:5985/5986` hết hạn.
  - Chưa đo: VM có chạy trên ASUS không, và có VPN hay jump host nào không (ngoài phạm vi phép đo).
- U11 giữ `not_evidenced`. Lượt xác thực qua ASUS **chưa chạy được**.
- Để chạy được, chủ kho cần cho biết đường mạng tới VM (VPN, tunnel, jump host hay máy nào cùng mạng `10.70.0.0/24`) và tên endpoint. Không tự đổi mạng, hosts hay TrustedHosts.

## Lệnh
VM (pwsh 7.6.9), thư mục `C:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\r7`:
```powershell
$d='C:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\r7'; 'SCRIPT=' + (Get-FileHash -Algorithm SHA256 "$d\R8VM.ps1").Hash.ToLowerInvariant(); $pe=$null; $tk=$null; [void][Management.Automation.Language.Parser]::ParseFile("$d\R8VM.ps1",[ref]$tk,[ref]$pe); 'PARSE_ERRORS=' + @($pe).Count; & "$d\R8VM.ps1" -Out "$d\r8-vm.json" *> "$d\r8-vm.log"; 'OK=' + $?; Get-Content "$d\r8-vm.log"; Get-Content "$d\r8-vm.json"
```
ASUS (pwsh 7.6.10), thư mục `C:\Users\admin\tl-work\r7-session_015GtxrapMSm976JLC7Fp1HM`:
```powershell
$d='C:\Users\admin\tl-work\r7-session_015GtxrapMSm976JLC7Fp1HM'; 'SCRIPT=' + (Get-FileHash -Algorithm SHA256 "$d\R8ASUS.ps1").Hash.ToLowerInvariant(); $pe=$null; $tk=$null; [void][Management.Automation.Language.Parser]::ParseFile("$d\R8ASUS.ps1",[ref]$tk,[ref]$pe); 'PARSE_ERRORS=' + @($pe).Count; & "$d\R8ASUS.ps1" -Out "$d\r8-asus.json" -VmIp '10.70.0.2' *> "$d\r8-asus.log"; 'OK=' + $?; Get-Content "$d\r8-asus.log"; Get-Content "$d\r8-asus.json"
```
Đầu ra:
- VM: `SCRIPT=677ccfb8…`, `PARSE_ERRORS=0`, `OK=True`, `SHA256=464e3eb0969e5d46f0366bf59b7e381fcbb5e725214ee4959b7ce3d0fa2ffc16`.
- ASUS: `SCRIPT=9c55a00f…`, `PARSE_ERRORS=0`, `OK=True`, `SHA256=af345e0b56f158b38376a06dcd7d634aa941384393e65da9b715020c35bd646e`.

Trạng thái thoát: script gọi trong cùng tiến trình nên không có `$LASTEXITCODE`. Bằng chứng là `$?` = `True`, cùng dòng `SHA256=`, dòng cuối của script, chỉ in ra sau khi JSON đã ghi xong.

## Giới hạn
- VM: tài khoản không admin. Tên endpoint còn có thể nằm ở registry hay cấu hình WinRM mà tài khoản này không đọc được.
- ASUS: chỉ thử đúng một IP mà VM tự báo. Không dò IP công khai, NAT hay VPN.
- Bảng hàng xóm là ảnh chụp tại lúc đo.

## Bằng chứng nguyên văn
`r8-vm.json` (sha256 `464e3eb0…`) và `r8-asus.json` (sha256 `af345e0b…`): CRLF giữa các dòng, một LF ở cuối. Đổi mỗi LF trong khối thành CRLF rồi thêm LF ở cuối sẽ ra đúng băm; đã kiểm trong container.
```json
{
  "schema": "wp1319_r8_vm.v1",
  "utc": "2026-11-20T01:07:03.3436198Z",
  "host": "TRA-LUAT-WIN",
  "ps": "7.6.9",
  "errs": [
    "wsman_plugins L29: System.Security.SecurityException: Requested registry access is not allowed."
  ],
  "ipv4": [
    {
      "ip": "10.70.0.2",
      "prefix": 24,
      "if": "Ethernet"
    }
  ],
  "gateways": [
    {
      "next_hop": "10.70.0.1",
      "if": "Ethernet"
    }
  ],
  "endpoint_files": []
}
```
```json
{
  "schema": "wp1319_r8_asus.v1",
  "utc": "2026-11-20T01:08:38.0874022Z",
  "host": "ASUS-LAPTOP",
  "ps": "7.6.10",
  "vm_ip_input": [
    "10.70.0.2"
  ],
  "errs": [
    "hyperv L15: Microsoft.HyperV.PowerShell.VirtualizationException: You do not have the required permission to complete this task. Contact the administrator of the authorization policy for the computer 'ASUS-LAPTOP'."
  ],
  "ipv4": [
    {
      "ip": "172.18.32.1",
      "prefix": 20,
      "if": "vEthernet (WSL (Hyper-V firewall))"
    },
    {
      "ip": "172.29.48.1",
      "prefix": 20,
      "if": "vEthernet (Default Switch)"
    },
    {
      "ip": "169.254.227.239",
      "prefix": 16,
      "if": "Local Area Connection* 2"
    },
    {
      "ip": "169.254.126.59",
      "prefix": 16,
      "if": "Bluetooth Network Connection"
    },
    {
      "ip": "169.254.5.72",
      "prefix": 16,
      "if": "Local Area Connection* 1"
    },
    {
      "ip": "169.254.113.16",
      "prefix": 16,
      "if": "Ethernet"
    },
    {
      "ip": "10.86.15.11",
      "prefix": 20,
      "if": "Wi-Fi"
    }
  ],
  "hosts_lines": [],
  "neighbors": [
    {
      "ip": "172.18.47.255",
      "state": "Permanent",
      "if": "vEthernet (WSL (Hyper-V firewall))"
    },
    {
      "ip": "172.18.35.122",
      "state": "Stale",
      "if": "vEthernet (WSL (Hyper-V firewall))"
    },
    {
      "ip": "172.29.63.255",
      "state": "Permanent",
      "if": "vEthernet (Default Switch)"
    },
    {
      "ip": "10.86.14.103",
      "state": "Reachable",
      "if": "Wi-Fi"
    },
    {
      "ip": "10.86.0.1",
      "state": "Reachable",
      "if": "Wi-Fi"
    }
  ],
  "tcp": [
    {
      "ip": "10.70.0.2",
      "port": 5985,
      "open": false
    },
    {
      "ip": "10.70.0.2",
      "port": 5986,
      "open": false
    }
  ]
}
```

### `R8VM.ps1` (sha256 `677ccfb84d0795c43134bf4264179a44c69926bd237f363751ce426daff4b1dd`, LF; khối cộng LF ở cuối ra đúng băm)
```powershell
# WP1319 r8 (ops/specs/wp1319-r8.md) muc 1, VM: dia chi IPv4, tep endpoint TraLuatCommander, plugin WSMan. Chi doc.
param([Parameter(Mandatory)][string]$Out)
$ErrorActionPreference = 'Stop'
$Res = [ordered]@{ schema = 'wp1319_r8_vm.v1'; utc = (Get-Date).ToUniversalTime().ToString('o'); host = $env:COMPUTERNAME; ps = "$($PSVersionTable.PSVersion)"; errs = [Collections.Generic.List[string]]::new() }
function Add-Err([string]$Step, $Er) { $Res['errs'].Add("${Step} L$($Er.InvocationInfo.ScriptLineNumber): $($Er.Exception.GetType().FullName): $($Er.Exception.Message)") }
try {
  $Res['ipv4'] = @(Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -ne '127.0.0.1' } | ForEach-Object { $a = [ordered]@{}; $a['ip'] = [string]$_.IPAddress; $a['prefix'] = [int]$_.PrefixLength; $a['if'] = [string]$_.InterfaceAlias; $a })
} catch { Add-Err 'ipv4' $_ }
try {
  $Res['gateways'] = @(Get-NetRoute -AddressFamily IPv4 -DestinationPrefix '0.0.0.0/0' | ForEach-Object { $g = [ordered]@{}; $g['next_hop'] = [string]$_.NextHop; $g['if'] = [string]$_.InterfaceAlias; $g })
} catch { Add-Err 'gateways' $_ }
$pat = '^\s*(SessionType|RunAsVirtualAccount|RoleDefinitions|VisibleFunctions|ModulesToImport)\b'
$found = [Collections.Generic.List[object]]::new()
try {
  $root = 'C:\ProgramData\TraLuatCommander'
  if (Test-Path -LiteralPath $root) {
    foreach ($fi in @(Get-ChildItem -LiteralPath $root -Recurse -Depth 6 -File -Include '*.pssc', '*.psrc' -ErrorAction SilentlyContinue)) {
      try {
        $e = [ordered]@{}
        $e['path'] = [string]$fi.FullName
        $e['sha256'] = (Get-FileHash -Algorithm SHA256 -LiteralPath $fi.FullName).Hash.ToLowerInvariant()
        $e['lines'] = @(Get-Content -LiteralPath $fi.FullName | Where-Object { $_ -match $pat } | ForEach-Object { $_.Trim() })
        $found.Add($e)
      } catch { Add-Err "file $($fi.FullName)" $_ }
    }
  } else { $Res['errs'].Add('root_missing: C:\ProgramData\TraLuatCommander') }
} catch { Add-Err 'endpoint_files' $_ }
$Res['endpoint_files'] = @($found)
try { $Res['wsman_plugins'] = @(Get-ChildItem -LiteralPath 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WSMAN\Plugin' -ErrorAction Stop | ForEach-Object { [string]$_.PSChildName }) } catch { Add-Err 'wsman_plugins' $_ }
$Res['errs'] = @($Res['errs'])
$json = $Res | ConvertTo-Json -Depth 6
[IO.File]::WriteAllText($Out, $json + "`n", [Text.UTF8Encoding]::new($false))
'SHA256=' + (Get-FileHash -Algorithm SHA256 -LiteralPath $Out).Hash.ToLowerInvariant()
```

### `R8ASUS.ps1` (sha256 `9c55a00f8716bb624bd66c34679d7460161f453b965838386ff60ecddea2e8ad`, LF; khối cộng LF ở cuối ra đúng băm)
```powershell
# WP1319 r8 (ops/specs/wp1319-r8.md) muc 1, ASUS: card mang, hosts, hang xom, Hyper-V, TCP toi IP cua VM. Chi doc, khong xac thuc.
param([Parameter(Mandatory)][string]$Out, [string[]]$VmIp = @())
$ErrorActionPreference = 'Stop'
$Res = [ordered]@{ schema = 'wp1319_r8_asus.v1'; utc = (Get-Date).ToUniversalTime().ToString('o'); host = $env:COMPUTERNAME; ps = "$($PSVersionTable.PSVersion)"; vm_ip_input = @($VmIp); errs = [Collections.Generic.List[string]]::new() }
function Add-Err([string]$Step, $Er) { $Res['errs'].Add("${Step} L$($Er.InvocationInfo.ScriptLineNumber): $($Er.Exception.GetType().FullName): $($Er.Exception.Message)") }
try {
  $Res['ipv4'] = @(Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -ne '127.0.0.1' } | ForEach-Object { $a = [ordered]@{}; $a['ip'] = [string]$_.IPAddress; $a['prefix'] = [int]$_.PrefixLength; $a['if'] = [string]$_.InterfaceAlias; $a })
} catch { Add-Err 'ipv4' $_ }
try { $Res['hosts_lines'] = @(Get-Content -LiteralPath 'C:\Windows\System32\drivers\etc\hosts' | Where-Object { $_ -match '(?i)tra-?luat' } | ForEach-Object { $_.Trim() }) } catch { Add-Err 'hosts' $_ }
try {
  $Res['neighbors'] = @(Get-NetNeighbor -AddressFamily IPv4 | Where-Object { "$($_.State)" -in 'Reachable', 'Stale', 'Permanent' -and $_.IPAddress -notmatch '^(224\.|239\.|255\.)' -and $_.IPAddress -ne '255.255.255.255' } | ForEach-Object { $n = [ordered]@{}; $n['ip'] = [string]$_.IPAddress; $n['state'] = [string]$_.State; $n['if'] = [string]$_.InterfaceAlias; $n })
} catch { Add-Err 'neighbors' $_ }
try {
  if (Get-Command -Name Get-VM -ErrorAction SilentlyContinue) {
    $Res['hyperv'] = @(Get-VM -ErrorAction Stop | ForEach-Object { $v = [ordered]@{}; $v['name'] = [string]$_.Name; $v['state'] = [string]$_.State; $v['ips'] = @($_.NetworkAdapters | ForEach-Object { $_.IPAddresses } | ForEach-Object { [string]$_ }); $v })
  } else { $Res['hyperv'] = 'get_vm_not_available' }
} catch { Add-Err 'hyperv' $_ }
$tcpList = [Collections.Generic.List[object]]::new()
foreach ($ip in @($VmIp)) {
  foreach ($port in 5985, 5986) {
    $t = [ordered]@{}; $t['ip'] = [string]$ip; $t['port'] = [int]$port
    try {
      $c = [Net.Sockets.TcpClient]::new()
      try { $ok = $c.ConnectAsync([string]$ip, [int]$port).Wait(3000); $t['open'] = [bool]($ok -and $c.Connected) } finally { $c.Dispose() }
    } catch { $t['open'] = $false; $t['connect_error'] = $_.Exception.GetBaseException().GetType().Name }
    $tcpList.Add($t)
  }
}
$Res['tcp'] = @($tcpList)
$Res['errs'] = @($Res['errs'])
$json = $Res | ConvertTo-Json -Depth 6
[IO.File]::WriteAllText($Out, $json + "`n", [Text.UTF8Encoding]::new($false))
'SHA256=' + (Get-FileHash -Algorithm SHA256 -LiteralPath $Out).Hash.ToLowerInvariant()
```
