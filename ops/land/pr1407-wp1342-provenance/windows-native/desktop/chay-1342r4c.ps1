$ErrorActionPreference = 'Continue'
$SID = 'session_015GtxrZk6gmfQKo7g4BfMBS'
$M = 'a2c7d759866502e7da318e4f83e17d5f77491eb5'
$MT = '24094d95f6e1e40a506befe5aab3abd81478f254'
$W = "F:\tl-win\$SID"
$OUT = Join-Path $W 'wp1342r4c-out'
$SRC = Join-Path $W 'wp1342-src'
$khoa = 'F:\tl-win\KHOA.txt'
$fmt = 'yyyy-MM-ddTHH:mm:ssZ'
$TT = Join-Path $OUT 'TOM-TAT.txt'
New-Item -ItemType Directory -Force $OUT | Out-Null
[string]$k = Get-Content -Raw $khoa
if ($null -eq $k) { $k = '' }
if ($k.Trim() -ne '') { "KHOA BAN: $k" | Out-File -Encoding utf8 $TT; exit 3 }
$bd = (Get-Date).ToUniversalTime()
function Ghi-Khoa { $n = (Get-Date).ToUniversalTime(); ($SID, $bd.ToString($fmt), $n.AddHours(1).ToString($fmt), 'native #1342 r4 cay merge a2c7d75: bang ca + J3/J9 x3 + phan chung N5', $n.ToString($fmt)) -join "`t" | Set-Content -Encoding utf8 -NoNewline -Path $khoa }
function Ghi($s) { $s | Out-File -Append -Encoding utf8 $TT }
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
  git -C $SRC fetch -q origin master 2>&1 | Out-File -Append -Encoding utf8 (Join-Path $OUT 'clone.log')
  git -C $SRC config core.abbrev 7
  git -C $SRC -c advice.detachedHead=false checkout -q --detach $M 2>&1 | Out-File -Append -Encoding utf8 (Join-Path $OUT 'clone.log')
  $h = (git -C $SRC rev-parse HEAD); $t = (git -C $SRC rev-parse 'HEAD^{tree}'); $s = ((git -C $SRC status --porcelain) -join ';')
  Ghi "CHOT sha=$h tree=$t sach=[$s]"
  if ($h -ne $M -or $t -ne $MT -or $s -ne '') { throw 'merge/tree/cay khong khop' }
  Chay 'MERGE' 'tap' @()
  Chay 'LAP-J3' 'lap' @('wp1342_native_job_mo_coi','3')
  Chay 'LAP-J9' 'lap' @('wp1342_native_job_loi_sau_gan','3')
  Ghi-Khoa
  $p = Start-Process -FilePath python -ArgumentList @('-X','utf8','-B',(Join-Path $W 'n5_phan_chung_1407.py'),(Join-Path $SRC '.claude\dev')) -NoNewWindow -PassThru -Wait -RedirectStandardOutput (Join-Path $OUT 'n5-phan-chung.stdout.txt') -RedirectStandardError (Join-Path $OUT 'n5-phan-chung.stderr.txt')
  Ghi "N5_PHAN_CHUNG exit=$($p.ExitCode)"; Get-Content (Join-Path $OUT 'n5-phan-chung.stdout.txt') | ForEach-Object { Ghi "  $_" }
  Ghi ("sach_sau=[" + ((git -C $SRC status --porcelain) -join ';') + ']')
  (& python -c "import hashlib,sys;[print(hashlib.sha256(open(p,'rb').read()).hexdigest(),p) for p in sys.argv[1:]]" (Join-Path $W 'do_r4.py') (Join-Path $W 'n5_phan_chung_1407.py') (Join-Path $W 'chay-1342r4c.ps1') 2>&1) | ForEach-Object { Ghi "$_" }
} catch { Ghi "LOI: $_" }
finally {
  $tg = [math]::Round(((Get-Date).ToUniversalTime() - $bd).TotalSeconds,1)
  Ghi "TONG ${tg}s"
  Clear-Content -Path $khoa
  Ghi 'XONG (khoa da nha)'
}
