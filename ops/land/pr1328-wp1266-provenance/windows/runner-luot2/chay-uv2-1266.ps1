# Luot Windows native tap trung 2 — packet #1266 (dac ta B r13 muc 6 buoc 3 + B17) — phien dieu phoi session_015GtxrbDu3ubjAHY6UebEUe.
$ErrorActionPreference = 'Continue'
$SID = 'session_015GtxrbDu3ubjAHY6UebEUe'
$BASE = '997b383f824ca63d7cee4a659bb6f9cf19bc439f'
$H = '2acd5c7cd6ccdac99011e408217ca34081ee4fb6'
$TREE_H = 'b76a912d76e911b697de235934f0362e49750d56'
$GOC = "C:\tl-win\$SID"
$R = "$GOC\runner1266b"
$NGUON = "$GOC\wp1266-nguon"
$TT = "$GOC\wp1266-tt2"
$B17KHO = "$GOC\wp1266-b17kho2"
$OUT = "$GOC\wp1266-uv2-out"
$KHOA = 'C:\tl-win\KHOA.txt'
$VIEC = '#1266 luot Windows tap trung 2 (runner + B17) tren H2 2acd5c7'
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
New-Item -ItemType Directory -Force -Path $OUT, "$GOC\tmp" | Out-Null
$LOG = "$OUT\tien-do.log"
function Log($m) { "$(UtcNow) $m" | Tee-Object -FilePath $LOG -Append }

$py = Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select-Object ProcessId, CreationDate
Log "kiem tai python.exe truoc khi do: $(@($py).Count) tien trinh"
$py | ForEach-Object { Log "  PID $($_.ProcessId) tao $($_.CreationDate)" }
GhiKhoa
Log "da ghi khoa: $(Get-Content -Raw $KHOA)"
try {
  if (Test-Path $NGUON) { Remove-Item -Recurse -Force $NGUON }
  git -c core.autocrlf=false clone --quiet https://github.com/ducthangho/tra-luat.git $NGUON 2>&1 | ForEach-Object { Log "clone: $_" }
  git -C $NGUON fetch --quiet origin "refs/heads/agent/wp1266-g1-claude:refs/heads/agent/wp1266-g1-claude" 2>&1 | ForEach-Object { Log "fetch: $_" }
  $hH = (git -C $NGUON rev-parse "agent/wp1266-g1-claude").Trim()
  $tH = (git -C $NGUON rev-parse "$H^{tree}").Trim()
  $pH = (git -C $NGUON rev-list --parents -n 1 $H).Trim()
  Log "M4: nhanh=$hH tree=$tH cha=[$pH] shallow=$(git -C $NGUON rev-parse --is-shallow-repository)"
  if ($hH -ne $H -or $tH -ne $TREE_H -or $pH -ne "$H 802a5665df9ae512d5b2df125b8e219f496fa9f9") { throw "M4 LECH: H/tree/cha khong khop" }
  Log "M4 KHOP"
  GhiKhoa
  Log ">>> runner_tap_trung"
  $t0 = Get-Date
  & python "$R\runner_tap_trung.py" $NGUON $BASE $H $TT *> "$OUT\runner-tap-trung.txt"
  $rc1 = $LASTEXITCODE
  Log "<<< runner_tap_trung rc=$rc1 $([Math]::Round(((Get-Date)-$t0).TotalSeconds,1))s :: $((Get-Content "$OUT\runner-tap-trung.txt" -Tail 2) -join ' | ')"
  if (Test-Path "$TT\tap-trung-Windows.json") { Copy-Item "$TT\tap-trung-Windows.json" $OUT }
  GhiKhoa
  if (Test-Path $B17KHO) { Remove-Item -Recurse -Force $B17KHO }
  git -c core.autocrlf=false clone --quiet --no-hardlinks $NGUON $B17KHO 2>&1 | ForEach-Object { Log "clone b17kho: $_" }
  Log ">>> b17_runner N 10 50 100 500"
  $t0 = Get-Date
  & python "$R\b17_runner.py" $B17KHO "$TT\ung_vien\ops\lease_publish.py" "$OUT\b17" 10 50 100 500 *> "$OUT\b17-runner.txt"
  $rc2 = $LASTEXITCODE
  Log "<<< b17_runner rc=$rc2 $([Math]::Round(((Get-Date)-$t0).TotalSeconds,1))s :: $((Get-Content "$OUT\b17-runner.txt" -Tail 6) -join ' | ')"
  "$(UtcNow),$SID,wp1266,$H,runner_tap_trung,,,,,,,,may=tra-luat-win; luot tap trung 2; rc=$rc1" | Add-Content C:\tl-win\do-luong.csv
  "$(UtcNow),$SID,wp1266,$H,b17_runner N10/50/100/500,,,,,,,,may=tra-luat-win; luot tap trung 2; rc=$rc2" | Add-Content C:\tl-win\do-luong.csv
  Log "XONG rc_runner=$rc1 rc_b17=$rc2"
} catch {
  Log "LOI: $_"
} finally {
  [string]$cur = '' + (Get-Content -Raw $KHOA -ErrorAction SilentlyContinue)
  if ($cur.StartsWith($SID)) { [IO.File]::WriteAllText($KHOA, ''); Log "da nha khoa" } else { Log "KHONG nha khoa: dong hien co khong phai cua phien nay: $cur" }
}
