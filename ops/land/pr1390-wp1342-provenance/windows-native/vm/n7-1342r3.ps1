param([string]$Pha)
# N7 #1342 r3: BootId truoc/sau MOT lan khoi dong lai VM. Pha 'truoc' ghi khoa + do + goi shutdown /r; pha 'sau' do lai + nha khoa.
$ErrorActionPreference = 'Continue'
$SID = 'session_015GtxrZk6gmfQKo7g4BfMBS'
$H = '972089eb4acd5e83f7b58b757f02a69590b26e4b'
$W = "C:\tl-win\$SID"
$OUT = Join-Path $W 'wp1342r3-n7-out'
$SRC = Join-Path $W 'wp1361-n2-src'
$khoa = 'C:\tl-win\KHOA.txt'
$fmt = 'yyyy-MM-ddTHH:mm:ssZ'
New-Item -ItemType Directory -Force $OUT | Out-Null
$log = Join-Path $OUT "n7-$Pha.txt"
$lenh = "import sys,json,datetime;sys.path.insert(0,'.claude/dev');import packet_loop as m;v1=m._1174_win_boot_id();v2=m._1174_win_boot_id();print('N7_BOOTID '+json.dumps({'v1':v1,'v2':v2,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))"
function Do-N7 {
  $r = @()
  $r += "pha=$Pha utc=" + (Get-Date).ToUniversalTime().ToString('o') + ' LastBootUpTime=' + (Get-CimInstance Win32_OperatingSystem).LastBootUpTime.ToUniversalTime().ToString('o')
  $r += 'HEAD=' + (git -C $SRC rev-parse HEAD) + ' tree=' + (git -C $SRC rev-parse 'HEAD^{tree}') + ' sach=[' + ((git -C $SRC status --porcelain) -join ';') + ']'
  Push-Location $SRC
  $o = & python -X utf8 -B -c $lenh 2>&1
  $r += "python_rc=$LASTEXITCODE"
  $r += ($o | ForEach-Object { "$_" })
  Pop-Location
  $r += 'reg=' + ((reg query 'HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters' /v BootId 2>&1) -join ' | ')
  return $r
}
if ($Pha -eq 'truoc') {
  [string]$k = Get-Content -Raw $khoa
  if ($null -eq $k) { $k = '' }
  if ($k.Trim() -ne '') { "KHOA BAN: $k" | Out-File -Encoding utf8 $log; exit 3 }
  $bd = (Get-Date).ToUniversalTime()
  ($SID, $bd.ToString($fmt), $bd.AddMinutes(45).ToString($fmt), 'N7 #1342 r3 BootId: KHOI DONG LAI VM mot lan (chu kho duyet 17-11)', $bd.ToString($fmt)) -join "`t" | Set-Content -Encoding utf8 -NoNewline -Path $khoa
  $env:PYTHONDONTWRITEBYTECODE = '1'
  git -C $SRC fetch -q origin agent/wp1342-r3-g1-claude 2>&1 | Out-File -Encoding utf8 (Join-Path $OUT 'fetch.log')
  git -C $SRC config core.abbrev 7
  git -C $SRC -c advice.detachedHead=false checkout -q --detach $H
  $r = Do-N7
  $r += 'shutdown_goi_utc=' + (Get-Date).ToUniversalTime().ToString('o')
  $s = & shutdown.exe /r /t 20 /d p:0:0 /c "tra-luat N7 #1342 r3 BootId (mot lan)" 2>&1
  $rc = $LASTEXITCODE
  $r += "shutdown_rc=$rc out=" + ($s -join ' ')
  $r | Out-File -Encoding utf8 $log
  if ($rc -ne 0) { Clear-Content -Path $khoa; 'KHOA DA NHA (shutdown that bai)' | Out-File -Append -Encoding utf8 $log }
} else {
  $env:PYTHONDONTWRITEBYTECODE = '1'
  try { $r = Do-N7; $r | Out-File -Encoding utf8 $log }
  finally {
    [string]$k = Get-Content -Raw $khoa
    if ($null -ne $k -and $k.StartsWith($SID)) { Clear-Content -Path $khoa; 'KHOA DA NHA' | Out-File -Append -Encoding utf8 $log }
    else { "KHOA KHONG PHAI CUA TA, KHONG DUNG: [$k]" | Out-File -Append -Encoding utf8 $log }
  }
}
