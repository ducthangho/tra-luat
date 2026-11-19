# WP1319 r6 — Vị trí cache trình duyệt của add-on Playwright trên ASUS (đo chỉ đọc)

**Căn cứ:** đặc tả `ops/specs/wp1319-r6.md` (sha256 `cfecbe61…`). Lease `ops/leases/wp1319-r6-g1-operator.yaml` (đã thu hồi) và `ops/leases/wp1319-r6-g2-operator.yaml`. Hàng U9 sau PR #1426 ghi nơi add-on thật sự đặt cache là **chưa kiểm**.

**Máy:** ASUS-LAPTOP (`7404cfba`), PS 7.6.9, tài khoản Desktop Commander. Thư mục làm việc `C:\Users\admin\tl-work\r6-session_015GtxrapMSm976JLC7Fp1HM\`. Không lấy khoá host vì không có thao tác ghi nào trên host.

## Các lượt chạy
| Lượt | Lease | Kết quả |
|---|---|---|
| 1 | g1 | **Hỏng do lỗi dựng.** Chạy bằng Windows PowerShell 5.1: phiên ấy không nạp được `Get-FileHash`, và script ném lỗi khi gán `errors`. Không có JSON. |
| 2 | g1 | **Hỏng do lỗi dựng.** Chạy bằng pwsh 7.6.9: biến vòng lặp `$r` ghi đè biến kết quả `$R`, vì tên biến PowerShell không phân biệt hoa thường; lỗi `The property 'caches' cannot be found`. Không có JSON. |
| — | — | Hết 2/2 lượt của g1. Đã sửa (đổi `$r` thành `$scanRoot`; soát lại tên biến không phân biệt hoa thường: không còn trùng). Chủ kho cấp thêm 1 lượt (g2). |
| 3 | g2 | **Đạt.** Script sha256 `30dd27702d74e86f559db5d2e9d5b13a048bf759f58dc9a65ef2faa1fd3707b1` (chép nguyên văn ở mục *Script đo* bên dưới), băm khớp giữa container và ASUS, parser PS 7 cho 0 lỗi. Lệnh chạy và trạng thái thoát ở mục *Lệnh chạy lượt 3*. JSON 21:18:52Z, `errors` rỗng. |

Cả ba lượt chỉ ghi vào thư mục làm việc của phiên.

## Kết quả (lượt 3)
- `TL_PW_ROOT` và `PLAYWRIGHT_BROWSERS_PATH`: **chưa đặt** ở cả ba phạm vi Process (tiến trình Desktop Commander), User và Machine.
- **Hai cache add-on hiện có đều nằm trên ổ C**, là hai add-on của P3:
  - `C:\Users\admin\tl-work\mission1238-asus-20261112-P3\addon-ps51\browsers`: 315 tệp, 467 067 094 byte;
  - `C:\Users\admin\tl-work\mission1238-asus-20261112-P3\addon-ps7\browsers`: 315 tệp, 467 067 093 byte;
  - mỗi cache có một thư mục con `0.1.0`; `install\0.1.0\package-lock.json` của cả hai có sha256 `0da56e1e…`, khớp lock P3 đã ghi.
- **Không có** thư mục `browsers` hay `ms-playwright` nào dưới `D:\tl-win` (độ sâu ≤ 4).
- Thư mục mặc định `C:\Users\admin\AppData\Local\ms-playwright`: 18 tệp, 7 759 byte, thư mục con `b` và `daemon`. Đây là dư lượng `daemon` mà P3 đã ghi (F1), không phải cache trình duyệt.
- Không có tiến trình `node.exe` hay `chrome.exe` nào chạy từ các thư mục trên.
- Dung lượng trống: C 21 092 708 352 byte; D 2 100 563 968 byte.

## Ghi nhận
- U9: cache trình duyệt của các add-on hiện có **đã nằm trên ổ C**, đúng với lựa chọn của chủ kho. Không chuyển hay cài gì.
- **Sửa lời khai của hàng U9 bản PR #1426.** Câu *"P3 ghi mỗi add-on trên ASUS có cache riêng dưới `D:\tl-win\…`"* là sai. P3 (`RAW-P3-VERDICT-claude-xhigh.md` §11 #5 và F4) chỉ ghi **nguồn seed** của cache nằm trên D (nay không còn). Hai cache thật nằm trên C như đo ở trên.
- Mẫu `TL_PW_ROOT` trong `.agents/skills/playwright-browser/SKILL.md` vẫn ghi ổ D. Vì vậy lượt cài kế tiếp phải đặt `TL_PW_ROOT` trên C một cách tường minh.

## Giới hạn
- Trường `installation_complete` chỉ kiểm **một cấp** dưới `browsers` (tức `browsers\0.1.0`), trong khi `INSTALLATION_COMPLETE` nằm sâu hơn một cấp (`browsers\0.1.0\chromium-*`). Danh sách rỗng ở đây **không** chứng minh cache cài dở. P3 đã ghi tệp ấy có mặt.
- Biến môi trường của các lượt khởi chạy add-on về sau được đặt trong tiến trình, nên không đo trước được.
- Chỉ quét `D:\tl-win` và `C:\Users\admin\tl-work` tới độ sâu 4, cộng thư mục mặc định. Cache đặt ở nơi khác không nằm trong phép đo.
- Tiến trình chỉ lọc theo đường dẫn thực thi của `node.exe`/`chrome.exe`.

## Lệnh chạy lượt 3
Chạy qua Desktop Commander, shell `pwsh` (PS 7.6.9), một dòng:

```powershell
$d='C:\Users\admin\tl-work\r6-session_015GtxrapMSm976JLC7Fp1HM'; Remove-Variable -Name e -ErrorAction SilentlyContinue; & "$d\R6.ps1" -Out "$d\r6-asus-g2.json" *> "$d\r6-run3.log"; 'OK=' + $?; Get-Content "$d\r6-run3.log"
```

Đầu ra nguyên văn:

```text
OK=True
SHA256=6dcdbafcd1eb80b22411443244f5ad87bed9bad3e2d3b752f5d6d056f8af74b2
```

Trạng thái thoát: `$?` = `True` sau lời gọi script. Script là `.ps1` gọi trong cùng tiến trình nên **không** đặt `$LASTEXITCODE`; với `$ErrorActionPreference = 'Stop'`, một lỗi kết thúc sẽ làm `$?` = `False` (như lượt 2 đã cho `OK=False`). Dòng `SHA256=` là dòng cuối của script, chỉ chạy sau khi JSON đã ghi xong. Tiến trình Desktop Commander kết thúc bình thường.

Kiểm trước lượt chạy (cùng phiên pwsh, lệnh riêng): `SCRIPT=30dd2770…`, `PARSE_ERRORS=0`.

## Script đo (`R6.ps1`, sha256 `30dd27702d74e86f559db5d2e9d5b13a048bf759f58dc9a65ef2faa1fd3707b1`)
Tệp trên host dùng LF. Nội dung khối dưới, cộng LF ở cuối dòng cuối, ra đúng băm trên; đã kiểm trong container.

```powershell
# WP1319 r6 (ops/specs/wp1319-r6.md): do CHI DOC vi tri cache trinh duyet cua add-on Playwright tren ASUS.
param([Parameter(Mandatory)][string]$Out)
$ErrorActionPreference = 'Stop'
$R = [ordered]@{ schema = 'wp1319_r6_probe.v1'; utc = (Get-Date).ToUniversalTime().ToString('o'); host = $env:COMPUTERNAME; errors = @() }
$R.env = [ordered]@{}
foreach ($n in 'TL_PW_ROOT', 'PLAYWRIGHT_BROWSERS_PATH') {
  $R.env[$n] = [ordered]@{ process = [Environment]::GetEnvironmentVariable($n, 'Process'); user = [Environment]::GetEnvironmentVariable($n, 'User'); machine = [Environment]::GetEnvironmentVariable($n, 'Machine') }
}
$roots = @('D:\tl-win', 'C:\Users\admin\tl-work')
$found = New-Object System.Collections.Generic.List[string]
foreach ($scanRoot in $roots) {
  if (-not (Test-Path -LiteralPath $scanRoot)) { $R.errors += "root_missing: $scanRoot"; continue }
  try {
    @(Get-ChildItem -LiteralPath $scanRoot -Directory -Recurse -Depth 4 -Force -ErrorAction SilentlyContinue | Where-Object { $_.Name -in 'browsers', 'ms-playwright' }) | ForEach-Object { $found.Add($_.FullName) }
  } catch { $R.errors += "scan ${scanRoot}: $($_.Exception.Message)" }
}
$def = 'C:\Users\admin\AppData\Local\ms-playwright'
if (Test-Path -LiteralPath $def) { $found.Add($def) }
$R.caches = @(foreach ($d in ($found | Select-Object -Unique)) {
    $x = [ordered]@{ path = $d; drive = $d.Substring(0, 1) }
    try {
      $files = @(Get-ChildItem -LiteralPath $d -Recurse -Force -File -ErrorAction SilentlyContinue)
      $sum = 0L; foreach ($f in $files) { $sum += $f.Length }
      $x.files = $files.Count; $x.bytes = $sum
      $subs = @(Get-ChildItem -LiteralPath $d -Directory -Force -ErrorAction SilentlyContinue)
      $x.children = @($subs | ForEach-Object { $_.Name })
      $x.installation_complete = @($subs | Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'INSTALLATION_COMPLETE') } | ForEach-Object { $_.Name })
      $root = Split-Path -Parent $d
      $lock = Join-Path $root 'install\0.1.0\package-lock.json'
      $x.addon_root = $root
      $x.lock_present = (Test-Path -LiteralPath $lock)
      if ($x.lock_present) { $x.lock_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $lock).Hash.ToLowerInvariant() }
    } catch { $R.errors += "cache ${d}: $($_.Exception.Message)" }
    $x })
$prefixes = @($R.caches | ForEach-Object { $_.addon_root }) + @($def)
$R.procs = @(Get-CimInstance Win32_Process -Filter "Name='node.exe' OR Name='chrome.exe'" | Where-Object { $p = $_.ExecutablePath; $p -and @($prefixes | Where-Object { $p.StartsWith($_, [StringComparison]::OrdinalIgnoreCase) }).Count -gt 0 } | ForEach-Object { [ordered]@{ name = $_.Name; exe = $_.ExecutablePath } })
$R.free = [ordered]@{}
foreach ($l in 'C', 'D') { try { $R.free[$l] = [int64](Get-Volume -DriveLetter $l).SizeRemaining } catch { $R.errors += "free ${l}: $($_.Exception.Message)" } }
$json = $R | ConvertTo-Json -Depth 8
[IO.File]::WriteAllText($Out, $json + "`n", [Text.UTF8Encoding]::new($false))
'SHA256=' + (Get-FileHash -Algorithm SHA256 -LiteralPath $Out).Hash.ToLowerInvariant()
```

## Bằng chứng nguyên văn
`r6-asus-g2.json` trên host, sha256 `6dcdbafcd1eb80b22411443244f5ad87bed9bad3e2d3b752f5d6d056f8af74b2` (in ở host). Tệp trên host dùng CRLF giữa các dòng và một LF ở cuối. Đổi mỗi LF trong khối dưới thành CRLF rồi thêm một LF ở cuối sẽ ra đúng băm trên; đã kiểm trong container.

```json
{
  "schema": "wp1319_r6_probe.v1",
  "utc": "2026-11-19T21:18:52.5240113Z",
  "host": "ASUS-LAPTOP",
  "errors": [],
  "env": {
    "TL_PW_ROOT": {
      "process": null,
      "user": null,
      "machine": null
    },
    "PLAYWRIGHT_BROWSERS_PATH": {
      "process": null,
      "user": null,
      "machine": null
    }
  },
  "caches": [
    {
      "path": "C:\\Users\\admin\\tl-work\\mission1238-asus-20261112-P3\\addon-ps51\\browsers",
      "drive": "C",
      "files": 315,
      "bytes": 467067094,
      "children": [
        "0.1.0"
      ],
      "installation_complete": [],
      "addon_root": "C:\\Users\\admin\\tl-work\\mission1238-asus-20261112-P3\\addon-ps51",
      "lock_present": true,
      "lock_sha256": "0da56e1ee6b81ad9226f000a917f6153b95e861ed41811d5eca7deb01bbb8ede"
    },
    {
      "path": "C:\\Users\\admin\\tl-work\\mission1238-asus-20261112-P3\\addon-ps7\\browsers",
      "drive": "C",
      "files": 315,
      "bytes": 467067093,
      "children": [
        "0.1.0"
      ],
      "installation_complete": [],
      "addon_root": "C:\\Users\\admin\\tl-work\\mission1238-asus-20261112-P3\\addon-ps7",
      "lock_present": true,
      "lock_sha256": "0da56e1ee6b81ad9226f000a917f6153b95e861ed41811d5eca7deb01bbb8ede"
    },
    {
      "path": "C:\\Users\\admin\\AppData\\Local\\ms-playwright",
      "drive": "C",
      "files": 18,
      "bytes": 7759,
      "children": [
        "b",
        "daemon"
      ],
      "installation_complete": [],
      "addon_root": "C:\\Users\\admin\\AppData\\Local",
      "lock_present": false
    }
  ],
  "procs": [],
  "free": {
    "C": 21092708352,
    "D": 2100563968
  }
}
```
