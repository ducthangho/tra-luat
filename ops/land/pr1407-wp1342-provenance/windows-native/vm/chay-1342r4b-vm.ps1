$ErrorActionPreference = 'Continue'
$SID = 'session_015GtxrZk6gmfQKo7g4BfMBS'
$H = '46d39071989fd77582ef8d1d61a7ab7de90a12ba'
$HT = 'a8bc50284bc9fffc0759e81d5b723d66e51701ce'
$W = "C:\tl-win\$SID"
$OUT = Join-Path $W 'wp1342r4b-vm-out'
$SRC = Join-Path $W 'wp1361-n2-src'
$khoa = 'C:\tl-win\KHOA.txt'
$fmt = 'yyyy-MM-ddTHH:mm:ssZ'
$TT = Join-Path $OUT 'TOM-TAT.txt'
New-Item -ItemType Directory -Force $OUT | Out-Null
[string]$k = Get-Content -Raw $khoa
if ($null -eq $k) { $k = '' }
if ($k.Trim() -ne '') { "KHOA BAN: $k" | Out-File -Encoding utf8 $TT; exit 3 }
if ((Get-PSDrive C).Free -lt 1GB) { "DUNG: o C con < 1 GB" | Out-File -Encoding utf8 $TT; exit 4 }
$bd = (Get-Date).ToUniversalTime()
function Ghi-Khoa { $n = (Get-Date).ToUniversalTime(); ($SID, $bd.ToString($fmt), $n.AddHours(1).ToString($fmt), 'native VM #1342 r4 (46d3907) N6 J3/J9/J10', $n.ToString($fmt)) -join "`t" | Set-Content -Encoding utf8 -NoNewline -Path $khoa }
function Ghi($s) { $s | Out-File -Append -Encoding utf8 $TT }
Ghi-Khoa
try {
  Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue
  $env:PYTHONDONTWRITEBYTECODE = '1'
  $tmp = Join-Path $W 'tmp1342r4'; New-Item -ItemType Directory -Force $tmp | Out-Null
  $env:TMP = $tmp; $env:TEMP = $tmp; $env:TMPDIR = $tmp
  Ghi ('bat_dau=' + $bd.ToString($fmt) + ' python=' + (python --version 2>&1) + ' os=' + [Environment]::OSVersion.VersionString + ' ptr=' + [IntPtr]::Size + ' C_free_GB=' + [math]::Round((Get-PSDrive C).Free/1GB,2))
  git -C $SRC fetch -q origin agent/wp1342-r4-g1-claude 2>&1 | Out-File -Append -Encoding utf8 (Join-Path $OUT 'clone.log')
  git -C $SRC config core.abbrev 7
  git -C $SRC -c advice.detachedHead=false checkout -q --detach $H 2>&1 | Out-File -Append -Encoding utf8 (Join-Path $OUT 'clone.log')
  $h = (git -C $SRC rev-parse HEAD); $t = (git -C $SRC rev-parse 'HEAD^{tree}'); $s = ((git -C $SRC status --porcelain) -join ';')
  Ghi "CHOT sha=$h tree=$t sach=[$s]"
  if ($h -ne $H -or $t -ne $HT -or $s -ne '') { throw 'head/tree/cay khong khop' }
  $ids = @('wp1342_native_job_mo_coi','wp1342_native_job_mo_coi','wp1342_native_job_mo_coi','wp1342_native_job_loi_sau_gan','wp1342_native_job_loi_sau_gan','wp1342_native_job_loi_sau_gan','wp1342_native_job_cha_chet_sau_gan','wp1342_native_job_cha_chet_sau_gan','wp1342_native_job_cha_chet_sau_gan')
  $a = @('-X','utf8','-B',(Join-Path $W 'do_r4.py'),$SRC,'VM',$OUT,'ds') + $ids
  $p = Start-Process -FilePath python -ArgumentList $a -NoNewWindow -PassThru -Wait -RedirectStandardOutput (Join-Path $OUT 'VM.stdout.txt') -RedirectStandardError (Join-Path $OUT 'VM.stderr.txt')
  Ghi "VM exit=$($p.ExitCode)"
  Get-Content (Join-Path $OUT 'VM.stdout.txt') | ForEach-Object { Ghi "  $_" }
  Ghi ("sach_sau=[" + ((git -C $SRC status --porcelain) -join ';') + ']')
  (& python -c "import hashlib,sys;[print(hashlib.sha256(open(p,'rb').read()).hexdigest(),p) for p in sys.argv[1:]]" (Join-Path $W 'do_r4.py') (Join-Path $W 'chay-1342r4b-vm.ps1') 2>&1) | ForEach-Object { Ghi "$_" }
} catch { Ghi "LOI: $_" }
finally {
  Ghi ("TONG " + [math]::Round(((Get-Date).ToUniversalTime() - $bd).TotalSeconds,1) + "s")
  Clear-Content -Path $khoa
  Ghi 'XONG (khoa da nha)'
}
