# ============================================================================
#  gas-deploy.ps1 — 1-lenh: sync + push + version + deploy Apps Script webapp
#  qua clasp (THAY browser editor tay). Giu NGUYEN deployment production hien
#  tai (KHONG tao deployment moi -> URL /exec KHONG doi).
#
#  Nguon-chan-ly: gas-project/Code.gs (clasp-managed). Sau deploy thanh cong,
#  TU DONG dong bo NGUOC ve references/Code.2.21.2i.gs (tai lieu doc, tranh
#  tai dien su co 2026-07-02: tinh nang viet vao references/ nhung quen deploy).
#
#  Cach dung:
#    .\gas-deploy.ps1 -Message "mo ta thay doi"              # push+version+deploy that
#    .\gas-deploy.ps1 -Message "..." -DryRun                 # chi xem diff, KHONG push/deploy
#    .\gas-deploy.ps1 -Message "..." -SourceFile <path.gs>   # doi file nguon (mac dinh gas-project/Code.gs)
# ============================================================================
param(
  [Parameter(Mandatory = $true)][string]$Message,
  [switch]$DryRun,
  [string]$SourceFile = ""
)
$ErrorActionPreference = "Stop"

$Root = $PSScriptRoot
$GasDir = Join-Path $Root "gas-project"
$GasFile = if ($SourceFile) { $SourceFile } else { Join-Path $GasDir "Code.gs" }
$RefFile = Join-Path $Root "references\Code.2.21.2i.gs"
# Deployment PRODUCTION hien hanh (khop webappUrl trong tra_luat_config.v2.json) — GIU NGUYEN, KHONG doi.
$DeploymentId = "AKfycbzNrsxGYjFkzT-Gq8NB_AiUS4zTOua8NwQtXqa_Dj51GEWOpUZ2Zq7PVBOu2YpAIeAU"

if (-not (Test-Path $GasFile)) { Write-Host "[LOI] khong thay: $GasFile" -ForegroundColor Red; exit 1 }
if (-not (Test-Path (Join-Path $GasDir ".clasp.json"))) { Write-Host "[LOI] gas-project/ chua clasp clone (.clasp.json thieu)" -ForegroundColor Red; exit 1 }

Write-Host "== gas-deploy: $Message ==" -ForegroundColor Cyan

# 1) DIFF trước khi làm gì — luôn hiện rõ CÁI GÌ sắp lên production (bài học 2026-07-02: đừng deploy mù).
if (Test-Path $RefFile) {
  $diff = Compare-Object (Get-Content $RefFile) (Get-Content $GasFile)
  if ($diff) {
    Write-Host "[diff] references/Code.2.21.2i.gs (tài liệu) khác $GasFile (nguồn deploy):" -ForegroundColor Yellow
    $diff | Select-Object -First 40 | Format-Table -AutoSize
    if ($diff.Count -gt 40) { Write-Host "  ... còn $($diff.Count - 40) dòng khác nữa" -ForegroundColor Yellow }
  } else {
    Write-Host "[diff] không đổi (references/ đã khớp gas-project/Code.gs)" -ForegroundColor Green
  }
} else {
  Write-Host "[diff] references/Code.2.21.2i.gs không tồn tại — bỏ qua so sánh" -ForegroundColor Yellow
}

if ($DryRun) {
  Write-Host "[dry-run] DỪNG ở đây — không push/version/deploy." -ForegroundColor Yellow
  exit 0
}

Push-Location $GasDir
try {
  Write-Host "[1/3] clasp push..." -ForegroundColor Cyan
  clasp push -f
  if ($LASTEXITCODE -ne 0) { throw "clasp push thất bại (rc=$LASTEXITCODE)" }

  Write-Host "[2/3] clasp version..." -ForegroundColor Cyan
  $versionOutput = (clasp version "$Message" 2>&1 | Out-String)
  Write-Host $versionOutput
  if ($LASTEXITCODE -ne 0) { throw "clasp version thất bại (rc=$LASTEXITCODE)" }
  if ($versionOutput -notmatch "Created version (\d+)") { throw "không đọc được số version từ output: $versionOutput" }
  $VersionNum = $Matches[1]

  Write-Host "[3/3] clasp deploy -> PRODUCTION ($DeploymentId, giữ nguyên /exec)..." -ForegroundColor Cyan
  clasp deploy -i $DeploymentId -V $VersionNum -d "$Message"
  if ($LASTEXITCODE -ne 0) { throw "clasp deploy thất bại (rc=$LASTEXITCODE)" }
}
finally {
  Pop-Location
}

# 2) Đồng bộ NGƯỢC gas-project/Code.gs (vừa deploy) → references/ (tài liệu luôn khớp LIVE thật, không trôi).
Copy-Item -Force $GasFile $RefFile
Write-Host "== XONG: version $VersionNum LIVE tại /exec hiện tại. references/Code.2.21.2i.gs đã đồng bộ. ==" -ForegroundColor Green
Write-Host "Verify: cd scripts; python tl.py --config <config> ping"
