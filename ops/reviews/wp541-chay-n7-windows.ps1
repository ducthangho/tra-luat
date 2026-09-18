# WP541 — MOT script: dung clone do, lay script do, kiem toan ven, chay, luu log.
# Chay trong PowerShell 7:   .\wp541-chay-n7-windows.ps1
# Doc rc o cuoi. 0 = moi chot dat | 1 = co chot truot | 3 = KHONG_DO_DUOC.

param(
    [string]$Base   = 'D:\Quốc hội',
    [string]$Nguon  = '',      # kho san co, dung lam nguon clone. Mac dinh: <Base>\tl546
    [string]$Kho    = '',      # clone RIENG de do.               Mac dinh: <Base>\tl541-do
    [string]$Py     = ''       # duong dan python, neu muon chi dinh
)
$ErrorActionPreference = 'Stop'
try { chcp 65001 > $null } catch {}
try { [Console]::OutputEncoding = [Text.Encoding]::UTF8 } catch {}

if (-not $Nguon) { $Nguon = Join-Path $Base 'tl546' }
if (-not $Kho)   { $Kho   = Join-Path $Base 'tl541-do' }
$Url       = 'https://github.com/ducthangho/tra-luat'
$ShaVa     = '2f70869'                          # HEAD mong cua ban va
$NhanhRv   = 'claude/review-541-luot3-20260918' # nhanh mang script do
$DuongPy   = 'ops/reviews/wp541-do-n7-windows.py'
$BlobMong  = 'f13264075dcb9190057a1b13cd56e27613300082'   # git blob OID cua script
$Log       = Join-Path $Base ('wp541-n7-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '.log')

function Dung($ly_do) {
    Write-Host ''
    Write-Host "KHONG_DO_DUOC: $ly_do" -ForegroundColor Red
    Write-Host 'Khong chay phep do. Khong ket luan gi.' -ForegroundColor Red
    exit 3
}
function G {
    # Chay git, doc rc TRUC TIEP. Khong qua pipe.
    $out = & git @args 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host ($out | Out-String)
        Dung "git $($args -join ' ') => rc=$LASTEXITCODE"
    }
    return $out
}

Write-Host '=============================================================='
Write-Host 'WP541 — do N7 tren Windows that'
Write-Host '=============================================================='

# ---- 0. Cong cu ----
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Dung 'khong co git trong PATH' }
$pyCmd = if ($Py) { Get-Command $Py -ErrorAction SilentlyContinue } else { $null }
if (-not $pyCmd) { $pyCmd = Get-Command py -ErrorAction SilentlyContinue }
if (-not $pyCmd) { $pyCmd = Get-Command python -ErrorAction SilentlyContinue }
if (-not $pyCmd) { $pyCmd = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $pyCmd) { Dung 'khong co py / python / python3 trong PATH' }
Write-Host "git : $((Get-Command git).Source)"
Write-Host "py  : $($pyCmd.Source)"
if (-not (Test-Path $Nguon)) { Dung "khong thay kho nguon: $Nguon" }

# ---- 1. Clone RIENG (khong dung worktree: worktree lam lech ket qua do) ----
if (Test-Path (Join-Path $Kho '.git')) {
    Write-Host "clone do da co: $Kho"
} else {
    Write-Host "dung clone do tu $Nguon ..."
    G clone --no-single-branch --quiet -- "$Nguon" "$Kho" | Out-Null
    G -C "$Kho" remote set-url origin "$Url" | Out-Null
}
G -C "$Kho" config core.abbrev 7 | Out-Null
G -C "$Kho" config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*' | Out-Null

# ---- 2. Lay ban va + nhanh review ----
Write-Host 'fetch fix_issue_541 va nhanh review ...'
G -C "$Kho" fetch --quiet origin fix_issue_541 | Out-Null
G -C "$Kho" fetch --quiet origin ("+refs/heads/{0}:refs/remotes/origin/{0}" -f $NhanhRv) | Out-Null
G -C "$Kho" checkout --quiet -B fix_issue_541 FETCH_HEAD 2>&1 | Out-Null
G -C "$Kho" fetch --quiet origin fix_issue_541 | Out-Null
G -C "$Kho" reset --hard --quiet FETCH_HEAD | Out-Null

$head = (G -C "$Kho" rev-parse --short HEAD) | Select-Object -First 1
Write-Host "HEAD clone do : $head  (mong $ShaVa)"
if ("$head" -notlike "$ShaVa*") { Dung "HEAD=$head khac $ShaVa" }

# ---- 3. Lay script do, kiem TOAN VEN bang blob OID ----
$blob = (G -C "$Kho" rev-parse ("origin/{0}:{1}" -f $NhanhRv, $DuongPy)) | Select-Object -First 1
Write-Host "blob script   : $blob"
Write-Host "blob mong     : $BlobMong"
if ("$blob".Trim() -ne $BlobMong) { Dung "blob script lech — script khac ban reviewer soan" }

$Script = Join-Path $Base 'do_win_541.py'
$bytes  = & git -C "$Kho" cat-file blob "$blob"
if ($LASTEXITCODE -ne 0) { Dung 'khong doc duoc blob script' }
[System.IO.File]::WriteAllLines($Script, $bytes, (New-Object Text.UTF8Encoding($false)))
Write-Host "script -> $Script"

# ---- 4. Chay. Doc rc TRUC TIEP. ----
Write-Host ''
Write-Host 'Chay phep do (bo test chay HAI lan — tinh 20-40 phut) ...'
Write-Host "log -> $Log"
Write-Host '--------------------------------------------------------------'
& $pyCmd $Script $Kho $ShaVa 2>&1 | Tee-Object -FilePath $Log
$rc = $LASTEXITCODE
Write-Host '--------------------------------------------------------------'
Write-Host "rc = $rc"
switch ($rc) {
    0 { Write-Host 'MOI CHOT DAT'            -ForegroundColor Green }
    1 { Write-Host 'CO CHOT TRUOT'           -ForegroundColor Yellow }
    3 { Write-Host 'KHONG_DO_DUOC'           -ForegroundColor Red }
    default { Write-Host "rc la $rc"         -ForegroundColor Red }
}
Write-Host ''
Write-Host "Gui ve cho reviewer: noi dung $Log"
exit $rc
