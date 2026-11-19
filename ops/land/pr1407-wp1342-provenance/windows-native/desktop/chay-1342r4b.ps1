$ErrorActionPreference = 'Continue'
$SID = 'session_015GtxrZk6gmfQKo7g4BfMBS'
$H = '46d39071989fd77582ef8d1d61a7ab7de90a12ba'
$HT = 'a8bc50284bc9fffc0759e81d5b723d66e51701ce'
$B = 'e2c3b82f818bd1739d31261e8129d3ef44915acf'
$W = "F:\tl-win\$SID"
$OUT = Join-Path $W 'wp1342r4b-out'
$SRC = Join-Path $W 'wp1342-src'
$khoa = 'F:\tl-win\KHOA.txt'
$fmt = 'yyyy-MM-ddTHH:mm:ssZ'
$TT = Join-Path $OUT 'TOM-TAT.txt'
New-Item -ItemType Directory -Force $OUT | Out-Null
[string]$k = Get-Content -Raw $khoa
if ($null -eq $k) { $k = '' }
if ($k.Trim() -ne '') { "KHOA BAN: $k" | Out-File -Encoding utf8 $TT; exit 3 }
$bd = (Get-Date).ToUniversalTime()
function Ghi-Khoa { $n = (Get-Date).ToUniversalTime(); ($SID, $bd.ToString($fmt), $n.AddHours(3).ToString($fmt), 'native #1342 r4 (46d3907) N4W/N5/N6/N7', $n.ToString($fmt)) -join "`t" | Set-Content -Encoding utf8 -NoNewline -Path $khoa }
function Ghi($s) { $s | Out-File -Append -Encoding utf8 $TT }
function Chot($sha, $tree) {
  git -C $SRC -c advice.detachedHead=false checkout -q --detach $sha 2>&1 | Out-File -Append -Encoding utf8 (Join-Path $OUT 'clone.log')
  $h = (git -C $SRC rev-parse HEAD); $t = (git -C $SRC rev-parse 'HEAD^{tree}'); $s = ((git -C $SRC status --porcelain) -join ';')
  Ghi "CHOT sha=$h tree=$t sach=[$s]"
  if ($h -ne $sha -or $s -ne '' -or ($tree -and $t -ne $tree)) { Ghi "CHOT_HONG"; return $false }
  return $true
}
function Chay($nhan, $mode, $rest) {
  Ghi-Khoa
  $a = @('-X','utf8','-B',(Join-Path $W 'do_r4.py'),$SRC,$nhan,$OUT,$mode) + $rest
  $p = Start-Process -FilePath python -ArgumentList $a -NoNewWindow -PassThru -Wait -RedirectStandardOutput (Join-Path $OUT "$nhan.stdout.txt") -RedirectStandardError (Join-Path $OUT "$nhan.stderr.txt")
  Ghi "$nhan exit=$($p.ExitCode)"
  Get-Content (Join-Path $OUT "$nhan.stdout.txt") | ForEach-Object { Ghi "  $_" }
}
Ghi-Khoa
try {
  Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue
  $env:PYTHONDONTWRITEBYTECODE = '1'
  $tmp = Join-Path $W 'tmp1342r4'; New-Item -ItemType Directory -Force $tmp | Out-Null
  $env:TMP = $tmp; $env:TEMP = $tmp; $env:TMPDIR = $tmp
  Ghi ('bat_dau=' + $bd.ToString($fmt) + ' python=' + (python --version 2>&1) + ' os=' + [Environment]::OSVersion.VersionString + ' ptr=' + [IntPtr]::Size)
  git -C $SRC fetch -q origin agent/wp1342-r4-g1-claude master 2>&1 | Out-File -Append -Encoding utf8 (Join-Path $OUT 'clone.log')
  git -C $SRC config core.abbrev 7
  if (-not (Chot $H $HT)) { throw 'head khong khop' }
  Chay 'GATE' 'ds' @('wp1342_native_job_abi','wp1342_native_job_thuan','wp1342_native_job_query_loi')
  $gate = Get-Content (Join-Path $OUT 'GATE.jsonl') | ForEach-Object { $_ | ConvertFrom-Json }
  if (($gate | Where-Object { $_.rc -ne 0 }).Count -gt 0) { Ghi 'GATE HONG -> DUNG'; throw 'gate' }
  Chay 'HEAD' 'tap' @()
  if (-not (Chot $B $null)) { throw 'base khong khop' }
  Chay 'BASE' 'tap' @()
  if (-not (Chot $H $HT)) { throw 'head khong khop lan 2' }
  Chay 'LAP-J3' 'lap' @('wp1342_native_job_mo_coi','10')
  Chay 'LAP-J9' 'lap' @('wp1342_native_job_loi_sau_gan','10')
  Ghi-Khoa
  $dev = Join-Path $SRC '.claude\dev'
  $p = Start-Process -FilePath python -ArgumentList @('-X','utf8','-B',(Join-Path $W 'dot_bien_r4_ban2.py'),$dev,'--kiem-neo') -NoNewWindow -PassThru -Wait -RedirectStandardOutput (Join-Path $OUT 'neo.stdout.txt') -RedirectStandardError (Join-Path $OUT 'neo.stderr.txt')
  Ghi "NEO exit=$($p.ExitCode)"; Get-Content (Join-Path $OUT 'neo.stdout.txt') | ForEach-Object { Ghi "  $_" }
  $t0 = Get-Date
  $p = Start-Process -FilePath python -ArgumentList @('-X','utf8','-B',(Join-Path $W 'dot_bien_r4_ban2.py'),$dev) -NoNewWindow -PassThru -RedirectStandardOutput (Join-Path $OUT 'dot-bien.stdout.txt') -RedirectStandardError (Join-Path $OUT 'dot-bien.stderr.txt')
  while (-not $p.WaitForExit(300000)) { Ghi-Khoa }
  Ghi "DOT_BIEN exit=$($p.ExitCode) $([math]::Round(((Get-Date)-$t0).TotalSeconds,1))s"
  Get-Content (Join-Path $OUT 'dot-bien.stdout.txt') | ForEach-Object { Ghi "  $_" }
  Ghi ("sach_sau=[" + ((git -C $SRC status --porcelain) -join ';') + ']')
  (& python -c "import hashlib,sys;[print(hashlib.sha256(open(p,'rb').read()).hexdigest(),p) for p in sys.argv[1:]]" (Join-Path $W 'do_r4.py') (Join-Path $W 'dot_bien_r4_ban2.py') (Join-Path $W 'chay-1342r4b.ps1') 2>&1) | ForEach-Object { Ghi "$_" }
} catch { Ghi "LOI: $_" }
finally {
  $tg = [math]::Round(((Get-Date).ToUniversalTime() - $bd).TotalSeconds,1)
  Ghi "TONG ${tg}s"
  Clear-Content -Path $khoa
  Ghi 'XONG (khoa da nha)'
}
