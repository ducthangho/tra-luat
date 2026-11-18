$ErrorActionPreference = 'Continue'
$SID = 'session_015GtxrZk6gmfQKo7g4BfMBS'
$H = 'c10d0710735e3532035a5219d469704d8a7592bb'
$B = '641108cb997872b0ef2a277ea9c8faf8b82532bb'
$W = "F:\tl-win\$SID"
$OUT = Join-Path $W 'wp1342r2c-out'
$SRC = Join-Path $W 'wp1342-src'
$khoa = 'F:\tl-win\KHOA.txt'
$fmt = 'yyyy-MM-ddTHH:mm:ssZ'
New-Item -ItemType Directory -Force $OUT | Out-Null
[string]$k = Get-Content -Raw $khoa
if ($null -eq $k) { $k = '' }
if ($k.Trim() -ne '') { "KHOA BAN: $k" | Out-File -Encoding utf8 (Join-Path $OUT 'TOM-TAT.txt'); exit 3 }
$bd = (Get-Date).ToUniversalTime()
function Ghi-Khoa { $n = (Get-Date).ToUniversalTime(); ($SID, $bd.ToString($fmt), $n.AddHours(2).ToString($fmt), 'native #1342 r2 (c10d071) N4W/N5/N6/N7', $n.ToString($fmt)) -join "`t" | Set-Content -Encoding utf8 -NoNewline -Path $khoa }
Ghi-Khoa
try {
Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue
$env:PYTHONDONTWRITEBYTECODE = '1'
$tmp = Join-Path $W 'tmp1342r2'; New-Item -ItemType Directory -Force $tmp | Out-Null
$env:TMP = $tmp; $env:TEMP = $tmp; $env:TMPDIR = $tmp
$tom = @()
git -C $SRC fetch -q origin agent/wp1342-r2-g1-claude master 2>&1 | Out-File -Append -Encoding utf8 (Join-Path $OUT 'clone.log')
git -C $SRC config core.abbrev 7
git -C $SRC config core.longpaths true
$tom += 'python=' + (python --version 2>&1) + ' os=' + [Environment]::OSVersion.VersionString + ' fs=' + (fsutil fsinfo volumeinfo F: | Select-String 'File System Name').Line + ' bd=' + $bd.ToString($fmt)
$lenh = "import sys,tempfile,pathlib,json;sys.path.insert(0,'.claude/dev');import packet_loop_test as T;k=T.chay_suite(T.CANONICAL,pathlib.Path(tempfile.mkdtemp()),{sys.argv[1]});print('KQ_JSON '+json.dumps({n:(None if v is None else [type(v).__name__,str(v)[:600]]) for n,v in k.items()}));sys.exit(0 if list(k.values())==[None] else 1)"
$both = @('admission_valid','admission_wrong_scope','witness_valid','witness_keyset','witness_int_bool','witness_json_bytes','witness_fresh_reserved','witness_import_retry','witness_suspended','witness_active_pending','lifecycle_legacy_unchanged','status_closed') | ForEach-Object { "wp1174_$_" }
$n4 = @('wp1174_windows_claim_rejected') + $both
$cu = @('wp1342_native_read','wp1342_native_volume_junction','wp1342_native_swap_ancestor','wp1342_native_metadata_drift','wp1342_native_noinherit','wp1342_native_symlink_file')
$thuan = @('wp1342_pure_platform_path','wp1342_additive_byte_preserved','wp1342_pure_lock_persist_refuse')
$moi = @('lock_exclusive','lock_noinherit','lock_names','persist_create','persist_update','persist_update_refuse','persist_update_symlink','persist_update_held','persist_bindings') | ForEach-Object { "wp1342_native_$_" }
foreach ($ve in @(@('BASE',$B,($n4 + $cu)), @('HEAD',$H,($n4 + $cu + $thuan + $moi)))) {
  $nhan = $ve[0]; $sha = $ve[1]; $ds = $ve[2]
  git -C $SRC -c advice.detachedHead=false checkout -q --detach $sha 2>&1 | Out-File -Append -Encoding utf8 (Join-Path $OUT 'clone.log')
  $tom += "$nhan HEAD=" + (git -C $SRC rev-parse HEAD) + ' tree=' + (git -C $SRC rev-parse 'HEAD^{tree}') + ' sach_truoc=[' + ((git -C $SRC status --porcelain) -join ';') + ']'
  Push-Location $SRC
  foreach ($c in $ds) {
    Ghi-Khoa
    $t0 = Get-Date
    $o = & python -X utf8 -B -c $lenh $c 2>&1
    $rc = $LASTEXITCODE
    $o | Out-File -Encoding utf8 (Join-Path $OUT "$nhan-$c.txt")
    $kq = ($o | Select-String '^KQ_JSON ' | Select-Object -Last 1).Line
    $nat = ($o | Select-String '^WP1342_NATIVE_V1 ' | Select-Object -Last 1).Line
    $tom += "$nhan $c rc=$rc $([math]::Round(((Get-Date)-$t0).TotalSeconds,1))s :: $kq"
    if ($nat) { $tom += "  $nhan $nat" }
    $tom | Out-File -Encoding utf8 (Join-Path $OUT 'TOM-TAT.txt')
  }
  $tom += "$nhan sach_sau=[" + ((git status --porcelain) -join ';') + ']'
  Pop-Location
}
Ghi-Khoa
git -C $SRC -c advice.detachedHead=false checkout -q --detach $H
$env:MUT_GOC = Join-Path $W 'm3'
New-Item -ItemType Directory -Force $env:MUT_GOC | Out-Null
$t0 = Get-Date
$p = Start-Process -FilePath python -ArgumentList @('-X','utf8','-B',(Join-Path $W 'dot-bien-1342r2.py'),$SRC,(Join-Path $OUT 'dot-bien')) -NoNewWindow -PassThru -RedirectStandardOutput (Join-Path $OUT 'dot-bien.stdout.txt') -RedirectStandardError (Join-Path $OUT 'dot-bien.stderr.txt')
while (-not $p.WaitForExit(600000)) { Ghi-Khoa }
$tom += "DOT_BIEN rc=$($p.ExitCode) $([math]::Round(((Get-Date)-$t0).TotalSeconds,1))s"
$tom += (Get-Content (Join-Path $OUT 'dot-bien.stdout.txt') | ForEach-Object { "  $_" })
$tom += (& python -c "import hashlib,sys;[print(hashlib.sha256(open(p,'rb').read()).hexdigest(),p) for p in sys.argv[1:]]" (Join-Path $W 'dot-bien-1342r2.py') (Join-Path $W 'chay-1342r2.ps1') 2>&1)
$tg = [math]::Round(((Get-Date).ToUniversalTime() - $bd).TotalSeconds,1)
$tom += "TONG ${tg}s"
$tom | Out-File -Encoding utf8 (Join-Path $OUT 'TOM-TAT.txt')
} finally {
  Clear-Content -Path $khoa
  'XONG (khoa da nha)' | Out-File -Append -Encoding utf8 (Join-Path $OUT 'TOM-TAT.txt')
}
