<#
  tl-setup.ps1 — CÀI ĐẶT 1 LẦN cho tra-luat + gws trên Claude Code (Windows),
  và SINH lệnh dán cho Claude Cowork. Đổi token dễ, không cần nhớ gì.

  Chạy:  bấm đúp  tl-setup.cmd
     hoặc:  powershell -ExecutionPolicy Bypass -File tl-setup.ps1

  Menu: [1] Setup lần đầu  [2] Đổi token GAS  [3] Kiểm tra  [4] In lệnh Cowork  [0] Thoát
#>
param([string]$SkillDir, [int]$Action = 0)
$ErrorActionPreference = "Stop"
$GWS_VER = "0.22.5"

function Resolve-Skill {
  $cands = @()
  if ($SkillDir) { $cands += $SkillDir }
  $cands += (Join-Path $env:USERPROFILE "Downloads\tra-luat")
  $cands += $PSScriptRoot
  foreach ($d in $cands) {
    if ($d -and (Test-Path (Join-Path $d "scripts\tl.py"))) { return (Resolve-Path $d).Path }
  }
  while ($true) {
    $p = Read-Host "Duong dan thu muc tra-luat (chua scripts\tl.py)"
    if (Test-Path (Join-Path $p "scripts\tl.py")) { return (Resolve-Path $p).Path }
    Write-Host "  Khong thay scripts\tl.py, thu lai." -ForegroundColor Yellow
  }
}

function TL { param($skill, [string[]]$cmd) & python (Join-Path $skill "scripts\tl.py") @cmd }

function Ensure-Gws {
  try { $v = (& gws --version 2>$null | Select-Object -First 1) } catch { $v = "" }
  if ("$v" -notmatch [regex]::Escape($GWS_VER)) {
    Write-Host "-> Cai gws $GWS_VER ..." -ForegroundColor Cyan
    & npm i -g "@googleworkspace/cli@$GWS_VER"
  } else { Write-Host "OK gws: $v" -ForegroundColor Green }
}

function Ensure-Auth {
  $am = "none"
  try { $am = (& gws auth status 2>$null | ConvertFrom-Json).auth_method } catch {}
  if (-not $am -or $am -eq "none") {
    Write-Host "-> Dang nhap gws (mo trinh duyet, chon tai khoan Google)..." -ForegroundColor Cyan
    & gws auth login
  } else { Write-Host "OK gws auth: $am" -ForegroundColor Green }
}

function Get-MasterKey {
  $k = [Environment]::GetEnvironmentVariable("TL_MASTER_KEY", "User")
  if (-not $k) {
    $b = New-Object byte[] 24
    [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($b)
    $k = ([Convert]::ToBase64String($b)) -replace '[+/=]', 'x'
    & setx TL_MASTER_KEY "$k" | Out-Null
    Write-Host "OK Da tao & luu TL_MASTER_KEY (vinh vien, may nay)." -ForegroundColor Green
  } else { Write-Host "OK TL_MASTER_KEY da co (giu nguyen)." -ForegroundColor Green }
  $env:TL_MASTER_KEY = $k
  return $k
}

function Do-Stage { param($skill)
  Write-Host "-> Goi + ma hoa secrets (config + gws cred) -> Drive..." -ForegroundColor Cyan
  $out = TL $skill @("secrets-stage") 2>&1
  $out | ForEach-Object { Write-Host $_ }
  $m = [regex]::Match(($out -join "`n"), 'id=([A-Za-z0-9_\-]+)')
  if ($m.Success) {
    $fid = $m.Groups[1].Value
    & setx TL_SECRETS_FILEID "$fid" | Out-Null
    $env:TL_SECRETS_FILEID = $fid
    Write-Host "OK SECRETS fileId = $fid (da luu TL_SECRETS_FILEID)." -ForegroundColor Green
    return $fid
  }
  return $null
}

function Show-Cowork { param($skill, $key, $fid)
  $block = @"
# ===== DAN KHOI NAY CHO CLAUDE COWORK (moi phien moi) =====
export TL_MASTER_KEY='$key'
export TL_SECRETS_FILEID='$fid'
# Bao Claude: tai fileId $fid tu Drive qua Drive MCP -> luu /tmp/s.enc, roi:
python scripts/tl.py bootstrap --env cowork --secrets-file /tmp/s.enc
python scripts/tl.py gws-ping --env cowork
"@
  $f = Join-Path $skill "COWORK-paste.txt"
  $block | Out-File -FilePath $f -Encoding utf8
  Write-Host "`n$block`n" -ForegroundColor Yellow
  Write-Host "OK Da luu khoi tren vao: $f" -ForegroundColor Green
}

function Change-Token { param($skill)
  $t = Read-Host "Nhap GAS webapp token MOI"
  if (-not $t) { Write-Host "Bo qua."; return }
  $cfg = Join-Path $env:USERPROFILE ".tra_luat_config.json"
  $env:TL_NEWTOK = $t
  & python -c "import json,os; p=os.path.expanduser('~/.tra_luat_config.json'); d=json.load(open(p,encoding='utf-8')) if os.path.exists(p) else {}; d['token']=os.environ['TL_NEWTOK']; json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False); print('local config token: updated')"
  Remove-Item Env:\TL_NEWTOK -ErrorAction SilentlyContinue
  TL $skill @("secrets-set", "--gas-token", $t) | ForEach-Object { Write-Host $_ }
  Write-Host "OK Doi token xong (local config + bundle Drive)." -ForegroundColor Green
}

function Do-Setup { param($skill)
  Ensure-Gws; Ensure-Auth
  $key = Get-MasterKey
  $fid = Do-Stage $skill
  if (-not $fid) { Write-Host "X Stage that bai - kiem tra config/token (~/.tra_luat_config.json)." -ForegroundColor Red; return }
  Write-Host "`n=== KIEM TRA ===" -ForegroundColor Cyan
  TL $skill @("ping") | ForEach-Object { Write-Host $_ }
  TL $skill @("gws-ping") | ForEach-Object { Write-Host $_ }
  Show-Cowork $skill $key $fid
  Write-Host "XONG. Code: dung binh thuong. Cowork: dan khoi tren (COWORK-paste.txt)." -ForegroundColor Green
}

# ===== main =====
$skill = Resolve-Skill
Write-Host "Skill: $skill" -ForegroundColor Gray
if ($Action -eq 0) {
  Write-Host "`n=== tra-luat setup ==="
  Write-Host " [1] Setup lan dau (cai gws + auth + ma hoa secrets)"
  Write-Host " [2] Doi token GAS"
  Write-Host " [3] Kiem tra (ping + gws-ping)"
  Write-Host " [4] In lai lenh Cowork"
  Write-Host " [0] Thoat"
  $Action = [int](Read-Host "Chon")
}
switch ($Action) {
  1 { Do-Setup $skill }
  2 { Change-Token $skill }
  3 { TL $skill @("ping") | ForEach-Object { Write-Host $_ }; TL $skill @("gws-ping") | ForEach-Object { Write-Host $_ } }
  4 { $k = [Environment]::GetEnvironmentVariable("TL_MASTER_KEY", "User"); $f = [Environment]::GetEnvironmentVariable("TL_SECRETS_FILEID", "User"); Show-Cowork $skill $k $f }
  default { Write-Host "Thoat." }
}
