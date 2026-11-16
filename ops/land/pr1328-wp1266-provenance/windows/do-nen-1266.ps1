# Do nen Windows packet #1266 (dac ta B r13 muc 6 buoc 1) tren base 997b383 — phien dieu phoi session_015GtxrbDu3ubjAHY6UebEUe.
# Khoa theo ADR-0057/0058/0059: <session_id>\t<UTC bat dau>\t<UTC han>\t<viec>\t<UTC nhip tim>.
$ErrorActionPreference = 'Continue'
$SID = 'session_015GtxrbDu3ubjAHY6UebEUe'
$BASE = '997b383f824ca63d7cee4a659bb6f9cf19bc439f'
$GOC = "C:\tl-win\$SID"
$DIR = "$GOC\wp1266-nen-997b383"
$OUT = "$GOC\wp1266-nen-out"
$KHOA = 'C:\tl-win\KHOA.txt'
$VIEC = '#1266 do nen Windows muc 6 buoc 1 (base 997b383)'
$env:PYTHONUTF8 = '1'; $env:PYTHONIOENCODING = 'utf-8'; $env:PYTHONDONTWRITEBYTECODE = '1'
$env:TMP = "$GOC\tmp"; $env:TEMP = "$GOC\tmp"
function UtcNow { (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ') }
$BATDAU = UtcNow
function GhiKhoa {
  [string]$cur = '' + (Get-Content -Raw $KHOA -ErrorAction SilentlyContinue)
  if ($cur.Trim() -ne '' -and -not $cur.StartsWith($SID)) { throw "KHOA dang do phien khac giu: $cur" }
  $han = (Get-Date).ToUniversalTime().AddHours(2).ToString('yyyy-MM-ddTHH:mm:ssZ')
  [IO.File]::WriteAllText($KHOA, "$SID`t$BATDAU`t$han`t$VIEC`t$(UtcNow)")
}
New-Item -ItemType Directory -Force -Path $GOC, $OUT, "$GOC\tmp" | Out-Null
$LOG = "$OUT\tien-do.log"
function Log($m) { "$(UtcNow) $m" | Tee-Object -FilePath $LOG -Append }

# kiem tai truoc khi do (ADR-0057 muc 4)
$py = Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select-Object ProcessId, CommandLine
Log "kiem tai python.exe truoc khi do: $(@($py).Count) tien trinh"
$py | ForEach-Object { Log "  PID $($_.ProcessId): $($_.CommandLine)" }

GhiKhoa
Log "da ghi khoa: $(Get-Content -Raw $KHOA)"
try {
  if (-not (Test-Path "$DIR\.git")) {
    git clone --quiet https://github.com/ducthangho/tra-luat.git $DIR 2>&1 | ForEach-Object { Log "clone: $_" }
  }
  git -C $DIR fetch --quiet origin master 2>&1 | ForEach-Object { Log "fetch: $_" }
  git -C $DIR checkout --quiet --detach $BASE 2>&1 | ForEach-Object { Log "checkout: $_" }
  git -C $DIR config core.abbrev 7
  Log "HEAD=$(git -C $DIR rev-parse HEAD) status=[$(git -C $DIR status --porcelain | Out-String)]"
  $ketqua = @()
  $buoc = @(
    @{ten='doc_receipt_thu_hoi_test (toan bo)'; args=@('-u', '.claude/dev/doc_receipt_thu_hoi_test.py')},
    @{ten='lease_publish_test t129'; args=@('-u', 'ops/lease_publish_test.py', '--chi-ca=t129_')},
    @{ten='lease_publish_test t133'; args=@('-u', 'ops/lease_publish_test.py', '--chi-ca=t133_')},
    @{ten='lease_publish_test t137'; args=@('-u', 'ops/lease_publish_test.py', '--chi-ca=t137_')},
    @{ten='lease_publish_test t151'; args=@('-u', 'ops/lease_publish_test.py', '--chi-ca=t151_')}
  )
  $i = 0
  foreach ($b in $buoc) {
    $i++
    GhiKhoa
    $f = "$OUT\buoc$i.txt"
    Log ">>> $($b.ten): python $($b.args -join ' ')"
    $t0 = Get-Date
    Push-Location $DIR
    & python @($b.args) *> $f
    $rc = $LASTEXITCODE
    Pop-Location
    $s = [Math]::Round(((Get-Date) - $t0).TotalSeconds, 1)
    $tail = (Get-Content $f -Tail 4) -join ' | '
    Log "<<< $($b.ten): rc=$rc ${s}s :: $tail"
    $ketqua += [pscustomobject]@{buoc=$b.ten; rc=$rc; giay=$s; tail=$tail}
    "$(UtcNow),$SID,wp1266,$BASE,$($b.ten),,,,$s,,,,may=tra-luat-win; do nen muc 6 buoc 1; rc=$rc" | Add-Content C:\tl-win\do-luong.csv
  }
  $ketqua | ConvertTo-Json | Set-Content "$OUT\ket-qua.json" -Encoding utf8
  Log "XONG"
} finally {
  [string]$cur = '' + (Get-Content -Raw $KHOA -ErrorAction SilentlyContinue)
  if ($cur.StartsWith($SID)) { [IO.File]::WriteAllText($KHOA, ''); Log "da nha khoa" } else { Log "KHONG nha khoa: dong hien co khong phai cua phien nay: $cur" }
}
