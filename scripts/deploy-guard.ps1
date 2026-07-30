<#
.SYNOPSIS
  Chốt CHỐNG THỤT LÙI khi đẩy Package — bản PowerShell của bước 4 trong scripts/deploy-package.sh.
  CLAUDE.md §Quy ước deploy mục 3.

.DESCRIPTION
  Package là MỘT fileId duy nhất; `tl drive-push` GHI ĐÈ nội dung và giữ fileId, KHÔNG có LockService
  như registry ⇒ last-writer-wins IM LẶNG. Sự cố 30-07-2026: hai phiên đẩy cùng fileId trong ~20 phút.
  Lần đó vô hại vì phiên sau build từ master mới nhất, nhưng ngược chiều thì Package THỤT LÙI âm thầm
  và mọi phiên Cowork mới bootstrap bản cũ.

  Đường Linux đã cưỡng chế từ v1.35.79. Tệp này port sang PowerShell để `upload-skill-to-Package.ps1`
  (ngoài repo, D:\Quốc hội\) không còn là đường ghi KHÔNG có chốt.

.PARAMETER Version
  Version SẮP ĐẨY (vd '1.35.79'). Thường lấy từ (Get-Content VERSION).Trim().

.PARAMETER ForceOlder
  Cố ý ghi đè dù Drive đang bản MỚI HƠN hoặc CÙNG SỐ. Chỉ dùng khi đã đọc CLAUDE.md §Quy ước deploy.

.PARAMETER FileId
  fileId của Package. Mặc định = SKILL_FILEID trong scripts/tl.py.

.PARAMETER DriveNameOverride
  CHỈ để TEST — bơm thẳng tên file "như thể đọc từ Drive", bỏ qua việc gọi gws.
  Đường sản xuất KHÔNG dùng tham số này.

.EXAMPLE
  # Cách nối vào upload-skill-to-Package.ps1 — THÊM ĐÚNG 1 DÒNG, ngay TRƯỚC lệnh drive-push:
  & "$PSScriptRoot\deploy-guard.ps1" -Version $ver; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  # (nếu script của bạn đặt ở thư mục khác repo, trỏ đường dẫn tới scripts\deploy-guard.ps1)

.EXAMPLE
  # Chạy tay để kiểm trước khi đẩy:
  .\scripts\deploy-guard.ps1 -Version (Get-Content VERSION).Trim()

.OUTPUTS
  exit 0 = KHÔNG thụt lùi, đẩy được (hoặc đã -ForceOlder, hoặc không rút được version ⇒ WARN)
  exit 3 = CHẶN THỤT LÙI (khớp rc=3 của deploy-package.sh)
  exit 4 = không đọc được Drive (gws chết/thiếu quyền) — fail-closed, KHÔNG đoán là an toàn
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)][string]$Version,
  [switch]$ForceOlder,
  [string]$FileId = '1H5kAt3SRVP7_xmLMIzcqyFtFc4VSDH0P',
  [string]$DriveNameOverride
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-Ok   { param($m) Write-Host "  [OK]   $m"   -ForegroundColor Green }
function Write-Bad  { param($m) Write-Host "  [FAIL] $m"   -ForegroundColor Red }
function Write-Warn { param($m) Write-Host "  [WARN] $m"   -ForegroundColor Yellow }

# ── 1. Lấy tên file Package đang có trên Drive ──
$driveName = $null
if ($PSBoundParameters.ContainsKey('DriveNameOverride')) {
  $driveName = $DriveNameOverride
} else {
  $params = '{"fileId":"' + $FileId + '","fields":"name,size,md5Checksum"}'
  try {
    $raw = & gws drive files get --params $params 2>&1 | Out-String
  } catch {
    Write-Bad "không gọi được gws: $($_.Exception.Message)"
    exit 4
  }
  if ($LASTEXITCODE -ne 0) {
    Write-Bad "gws trả rc=$LASTEXITCODE khi đọc Package — cần ``gws auth login``. KHÔNG đoán là an toàn."
    Write-Host ($raw -split "`n" | Select-Object -First 5 | ForEach-Object { "        $_" }) -ForegroundColor DarkGray
    exit 4
  }
  # gws trả JSON; đọc bằng ConvertFrom-Json chứ không regex mò cả khối
  try {
    $driveName = ($raw | ConvertFrom-Json).name
  } catch {
    Write-Bad "không parse được JSON từ gws — KHÔNG kiểm được thụt lùi, fail-closed."
    exit 4
  }
}

if ([string]::IsNullOrWhiteSpace($driveName)) {
  Write-Bad 'Drive không trả tên file — fail-closed.'
  exit 4
}
Write-Host "  Package HIỆN TẠI: $driveName"

# ── 2. Rút version từ tên (khuôn: tra-luat-skill-v<VER>-gws3env.zip) ──
# Không rút được ⇒ WARN và ĐI TIẾP, KHÔNG chặn oan: tên file có thể do người đặt tay.
# Đây là điểm KHÁC hẳn lỗi đọc Drive ở trên (fail-closed) — ở đây ta ĐÃ biết trạng thái Drive,
# chỉ là không suy ra được số hiệu.
$m = [regex]::Match($driveName, '-v(?<v>\d+(?:\.\d+)+)-')
if (-not $m.Success) {
  Write-Warn "không rút được version từ tên Package ('$driveName') — KHÔNG kiểm được thụt lùi, tự chịu trách nhiệm"
  exit 0
}
$driveVer = $m.Groups['v'].Value

# ── 3. So sánh ──
# Dùng [version] (so theo TỪNG THÀNH PHẦN SỐ) — KHÔNG so chuỗi: '1.35.9' -gt '1.35.78' là ĐÚNG khi so
# chuỗi nhưng SAI về nghĩa. Cạm bẫy này chính là lý do bản sh dùng `sort -V` chứ không `[ \> ]`.
try {
  $vLocal = [version]$Version
  $vDrive = [version]$driveVer
} catch {
  Write-Warn "version không phải dạng số thuần (local='$Version' drive='$driveVer') — bỏ qua chốt"
  exit 0
}

if ($vDrive -ge $vLocal) {
  $rel = if ($vDrive -eq $vLocal) { '=' } else { '>' }
  if ($ForceOlder) {
    Write-Warn "Drive đang v$driveVer $rel v$Version sắp đẩy — GHI ĐÈ vì có -ForceOlder"
    exit 0
  }
  Write-Bad "CHẶN THỤT LÙI: Drive đang v$driveVer, bản sắp đẩy v$Version — phiên khác vừa đẩy (hoặc cây này tụt sau)."
  Write-Host '        Chữa: git fetch origin master && (merge/rebase) -> chạy lại gate -> deploy lại.' -ForegroundColor Red
  Write-Host '        Cố ý ghi đè bản mới hơn/cùng số: thêm -ForceOlder (đọc CLAUDE.md §Quy ước deploy trước).' -ForegroundColor Red
  exit 3
}

Write-Ok "Drive đang v$driveVer < v$Version sắp đẩy — không thụt lùi"
exit 0
