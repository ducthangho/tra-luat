$ErrorActionPreference = 'Stop'
$S = 'session_015GtxraXfMD1t2FJLzzGDr4'
$G = "D:\tl-win\$S"
New-Item -ItemType Directory -Force $G | Out-Null
$now = (Get-Date).ToUniversalTime()
$t0 = $now.ToString('yyyy-MM-ddTHH:mm:ssZ')
$han = $now.AddHours(2).ToString('yyyy-MM-ddTHH:mm:ssZ')
"== kiem tai (ADR-0057 §4) $t0"
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | ForEach-Object { "python pid=$($_.ProcessId) cmd=$($_.CommandLine)" }
[string]$old = Get-Content -Raw 'D:\tl-win\KHOA.txt'
if ($null -eq $old) { $old = '' }
$old = $old.Trim()
"khoa cu: $old"
$U8 = New-Object System.Text.UTF8Encoding($false)
# dong tiep nhan khoa da ghi o luot truoc (08:31:14Z), khong ghi lai
[IO.File]::WriteAllText('D:\tl-win\KHOA.txt', "$S`t$t0`t$han`twp1038 M1 LIVE agent-creds-exec --gemini", $U8)
"khoa moi: $(Get-Content -Raw 'D:\tl-win\KHOA.txt')"

$env:PYTHONUTF8 = '1'; $env:PYTHONIOENCODING = 'utf-8'; $env:PYTHONDONTWRITEBYTECODE = '1'
$R = "$G\tra-luat"
if (-not (Test-Path "$R\.git")) { git clone -q --depth 1 https://github.com/ducthangho/tra-luat.git $R }
git -C $R fetch -q --depth 1 origin master
git -C $R checkout -q --detach FETCH_HEAD
git -C $R config core.abbrev 7
$sha = git -C $R rev-parse HEAD
"== kho do: $sha"

# Tien trinh do: xoa hai bien khoi moi truong CUA CHINH NO; TL_MASTER_KEY lay tu bien User
Remove-Item Env:GEMINI_API_KEY -ErrorAction SilentlyContinue
Remove-Item Env:CLAUDE_CODE_OAUTH_TOKEN -ErrorAction SilentlyContinue
$env:TL_MASTER_KEY = [Environment]::GetEnvironmentVariable('TL_MASTER_KEY', 'User')
"GEMINI_API_KEY trong tien trinh do: $([bool]$env:GEMINI_API_KEY) · CLAUDE_CODE_OAUTH_TOKEN: $([bool]$env:CLAUDE_CODE_OAUTH_TOKEN) · TL_MASTER_KEY dai: $($env:TL_MASTER_KEY.Length)"

[string]$k = [Environment]::GetEnvironmentVariable('GEMINI_API_KEY', 'User')
$sh = [System.Security.Cryptography.SHA256]::Create()
$kyvong = -join ($sh.ComputeHash([Text.Encoding]::UTF8.GetBytes($k)) | ForEach-Object { $_.ToString('x2') })
$rong = -join ($sh.ComputeHash([byte[]]@()) | ForEach-Object { $_.ToString('x2') })
$k = $null
$con = "$G\m1-con.py"
[IO.File]::WriteAllText($con, "import os, hashlib`nprint(hashlib.sha256(os.environ.get('GEMINI_API_KEY', '').encode()).hexdigest())`n", $U8)

$ErrorActionPreference = 'Continue'
"== (i) agent-creds-exec --gemini -- <con>"
$out1 = & python "$R\scripts\tl.py" agent-creds-exec --gemini -- python $con 2>&1
$rc1 = $LASTEXITCODE
$h1 = ($out1 | ForEach-Object { "$_" } | Where-Object { $_ -match '^[0-9a-f]{64}$' } | Select-Object -Last 1)
$out1 | ForEach-Object { "$_" } | Where-Object { $_ -notmatch '^[0-9a-f]{64}$' } | ForEach-Object { "   | $_" }
"rc=$rc1 · bam_con == kyvong: $($h1 -eq $kyvong) · bam_con == rong: $($h1 -eq $rong) · kyvong == rong: $($kyvong -eq $rong)"

"== (ii) doi chung: <con> truc tiep"
$out2 = & python $con 2>&1
$rc2 = $LASTEXITCODE
$h2 = ($out2 | ForEach-Object { "$_" } | Select-Object -Last 1)
"rc=$rc2 · bam_con == rong: $($h2 -eq $rong) · bam_con == kyvong: $($h2 -eq $kyvong)"

$t1 = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
$dat = ($rc1 -eq 0) -and ($h1 -eq $kyvong) -and ($kyvong -ne $rong) -and ($rc2 -eq 0) -and ($h2 -eq $rong)
[IO.File]::AppendAllText('D:\tl-win\do-luong.csv', "$t1,$S,1038-M1,$sha,M1-agent-creds-exec,$([int]$dat),1,$([int](-not $dat)),,phien-dieu-phoi,,,""may=ASUS-LAPTOP; (i) rc=$rc1 khop=$($h1 -eq $kyvong); (ii) rc=$rc2 rong=$($h2 -eq $rong)""`r`n", $U8)
[IO.File]::WriteAllText('D:\tl-win\KHOA.txt', '', $U8)
"== M1 $(if ($dat) {'DAT'} else {'DO'}) · khoa da xoa · $t1"
