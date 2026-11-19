param([string]$Buoc, [string]$Tdir = '')
$W = 'F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS'
$H = Join-Path $W 'c433c1-20261119T151704Z'
$TMP = Join-Path $W 'tmp433c1-20261119T151704Z'
$OUT = Join-Path $W 'wp433c1-out-20261119T151704Z'
[string]$k = Get-Content -Raw 'F:\tl-win\KHOA.txt'
if ($null -eq $k) { $k = '' }
if ($k.Trim() -ne '' -and -not $k.Contains('D10')) { "KHOA BAN: $k"; exit 3 }
$now = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
Set-Content -Path 'F:\tl-win\KHOA.txt' -Value ("session_015GtxrZk6gmfQKo7g4BfMBS`t$now`t" + (Get-Date).ToUniversalTime().AddHours(1).ToString('yyyy-MM-ddTHH:mm:ssZ') + "`tnative #433 C1 PR #1425: D10 $Buoc`t$now") -Encoding utf8
$env:TEMP = $TMP; $env:TMP = $TMP; $env:PYTHONIOENCODING = 'utf-8'; $env:PYTHONDONTWRITEBYTECODE = '1'
Set-Location $H
$Argv = @('-B', (Join-Path $TMP 'wp433c1_rig.py'), $Buoc)
if ($Tdir -ne '') { $Argv += $Tdir }
"== D10 $Buoc bat_dau=$now" | Out-File -Append -Encoding utf8 (Join-Path $OUT "D10-$Buoc.txt")
& python @Argv 2>&1 | Tee-Object -Append -FilePath (Join-Path $OUT "D10-$Buoc.txt")
"rc=$LASTEXITCODE ket_thuc=" + (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ') | Tee-Object -Append -FilePath (Join-Path $OUT "D10-$Buoc.txt")
if ($Buoc -eq 'd10c') { Set-Content -Path 'F:\tl-win\KHOA.txt' -Value '' -Encoding utf8 }
