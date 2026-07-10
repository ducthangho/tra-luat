<#
  install-patch.ps1 — đặt bản vá tra-luat vào D:\Quốc hội\tra-luat (CÓ BACKUP).

  CÁCH CHẠY
    1) Tải 3 file về CÙNG một thư mục (vd Downloads):
         install-patch.ps1
         tl_gws.patched.py
         refresh-tokens.patched.ps1
    2) Mở PowerShell tại thư mục đó, chạy:
         .\install-patch.ps1
       (nếu bị chặn policy:  powershell -ExecutionPolicy Bypass -File .\install-patch.ps1 )

  THAM SỐ
    -Repo   "D:\Quốc hội\tra-luat"   # mặc định
    -SrcDir "<thư mục chứa file .patched>"   # mặc định = thư mục chứa script này
    -Verify   # sau khi copy: chạy py_compile + tl.py --selftest (nếu có python/py)
#>
[CmdletBinding()]
param(
  [string]$Repo   = "D:\Quốc hội\tra-luat",
  [string]$SrcDir = $PSScriptRoot,
  [switch]$Verify
)
$ErrorActionPreference = "Stop"
if (-not $SrcDir) { $SrcDir = (Get-Location).Path }
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"

function Install-One {
  param([string]$Src, [string]$Dst)
  if (-not (Test-Path -LiteralPath $Src)) { throw "Không thấy file nguồn: $Src" }
  $dstDir = Split-Path -Parent $Dst
  if (-not (Test-Path -LiteralPath $dstDir)) { throw "Không thấy thư mục đích: $dstDir (kiểm -Repo)" }
  if (Test-Path -LiteralPath $Dst) {
    $bak = "$Dst.bak.$stamp"
    Copy-Item -LiteralPath $Dst -Destination $bak -Force
    Write-Host "  backup: $bak" -ForegroundColor DarkGray
  } else {
    Write-Host "  (đích chưa tồn tại — tạo mới)" -ForegroundColor DarkYellow
  }
  # Copy-Item giữ NGUYÊN BYTES (UTF-8 không đổi encoding)
  Copy-Item -LiteralPath $Src -Destination $Dst -Force
  Write-Host "  OK ghi: $Dst" -ForegroundColor Green
}

Write-Host "== install-patch . repo=$Repo ==" -ForegroundColor Cyan
if (-not (Test-Path -LiteralPath $Repo)) { throw "Không thấy repo: $Repo — truyền -Repo cho đúng." }

# [1/2] scripts\tl_gws.py
$srcPy = Join-Path $SrcDir "tl_gws.patched.py"
$dstPy = Join-Path $Repo   "scripts\tl_gws.py"
Write-Host "[1/2] scripts\tl_gws.py"
Install-One -Src $srcPy -Dst $dstPy

# [2/2] refresh-tokens.ps1 — tự dò vị trí THẬT trong repo (tránh đặt nhầm chỗ)
$srcPs = Join-Path $SrcDir "refresh-tokens.patched.ps1"
$found = @(Get-ChildItem -Path $Repo -Filter "refresh-tokens.ps1" -Recurse -File -ErrorAction SilentlyContinue)
if ($found.Count -eq 1) {
  $dstPs = $found[0].FullName
} elseif ($found.Count -gt 1) {
  Write-Host "  CANH BAO: tìm thấy NHIỀU refresh-tokens.ps1:" -ForegroundColor Yellow
  $found | ForEach-Object { Write-Host "     $($_.FullName)" }
  throw "Nhiều bản — chỉ định tay đích rồi copy, hoặc dọn bớt."
} else {
  $dstPs = Join-Path $Repo "refresh-tokens.ps1"
}
Write-Host "[2/2] $dstPs"
Install-One -Src $srcPs -Dst $dstPs

# [3] verify tuỳ chọn
if ($Verify) {
  Write-Host "== verify ==" -ForegroundColor Cyan
  $pyCmd = (Get-Command python -ErrorAction SilentlyContinue)
  if (-not $pyCmd) { $pyCmd = (Get-Command py -ErrorAction SilentlyContinue) }
  if ($pyCmd) {
    $py = $pyCmd.Source
    Push-Location $Repo
    try {
      & $py -m py_compile "scripts\tl_gws.py"
      if ($LASTEXITCODE -eq 0) { Write-Host "  OK py_compile" -ForegroundColor Green }
      else { Write-Host "  FAIL py_compile" -ForegroundColor Red }
      Write-Host "  selftest (dòng cuối):" -ForegroundColor DarkGray
      & $py "scripts\tl.py" --selftest 2>&1 | Select-Object -Last 1
    } finally { Pop-Location }
  } else {
    Write-Host "  CANH BAO: không thấy python/py trên PATH — bỏ verify." -ForegroundColor DarkYellow
  }
}

Write-Host ""
Write-Host "== XONG ==" -ForegroundColor Green
Write-Host "Khôi phục: đổi tên các file *.bak.$stamp về tên gốc." -ForegroundColor DarkGray
Write-Host "LƯU Ý: tl_gws.py đã thay TRỰC TIẾP. Muốn version-pin vào package, chạy thêm:" -ForegroundColor DarkGray
Write-Host "  tl edit-skill scripts/tl_gws.py --patch  ->  release-check  ->  bump VERSION" -ForegroundColor DarkGray
