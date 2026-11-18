# Ma tran phan chung PowerShell cho buoc don du luong daemon cua playwright-browser SKILL.md (packet #1389).
# Chay TREN BYTE CUA SKILL: trich NOI DUNG giua cap dong danh dau (khong gom dong danh dau), lan xuat hien THU HAI
# (khoi PowerShell) cua moi cap: "du-luong-daemon" (Cleanup) va "du-luong-daemon-truoc-open" (Capture). SOURCE/frag
# bam tren byte goc (LF, khong BOM); ban chay cho PS 5.1 la tep wrapper rieng co BOM.
# Moi ca chay trong TIEN TRINH CON cua chinh shell dang do ($Shell), LOCALAPPDATA tro vao scratch, CWD = <ca>\home.
# Khong goi CLI, khong mang, khong trinh duyet.
# Dung: <shell> -NoProfile -File residue_matrix.ps1 -Skill <SKILL.md> -Scratch <thu muc rong> -Shell <pwsh.exe|powershell.exe>
# PowerShell 5.1 goi tu pwsh 7 phai mang PSModulePath = gia tri Machine, neu khong se thieu Get-FileHash (do r3 #1319).
param([Parameter(Mandatory)][string]$Skill, [Parameter(Mandatory)][string]$Scratch, [Parameter(Mandatory)][string]$Shell)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Skill -PathType Leaf)) { throw 'SKILL.md?' }
if (-not (Test-Path -LiteralPath $Scratch -PathType Container) -or @(Get-ChildItem -Force -LiteralPath $Scratch).Count) { throw 'Scratch phai rong' }
$Scratch = (Resolve-Path -LiteralPath $Scratch).ProviderPath
$utf8 = New-Object System.Text.UTF8Encoding($false); $bom = New-Object System.Text.UTF8Encoding($true)
$raw = [IO.File]::ReadAllBytes($Skill); if ($raw -contains 13) { throw 'SKILL.md co CR: can byte LF goc' }
$lines = [Text.Encoding]::UTF8.GetString($raw) -split "`n"
function Extract([string]$Name) {
  $b = '  # --- ' + $Name + ': bat dau'; $e = '  # --- ' + $Name + ': het'; $pairs = @(); $open = -1
  for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -ceq $b) { if ($open -ge 0) { throw "danh dau long nhau: $Name" }; $open = $i }
    elseif ($lines[$i] -ceq $e) { if ($open -lt 0) { throw "het khong cap: $Name" }; $pairs += , @($open, $i); $open = -1 } }
  if ($open -ge 0 -or $pairs.Count -ne 2) { throw "can 2 cap danh dau $Name, thay $($pairs.Count)" }
  $p = $pairs[1]; if ($p[1] - $p[0] -lt 2) { throw "doan rong: $Name" }
  (($lines[($p[0] + 1)..($p[1] - 1)]) -join "`n") + "`n" }
$frag = Extract 'du-luong-daemon'; $pre = Extract 'du-luong-daemon-truoc-open'
if (-not $frag.Contains('$hits = @(Get-ChildItem')) { throw 'doan cleanup khong phai ban PowerShell' }
if (-not $pre.Contains('$daemonDir')) { throw 'doan truoc-open khong phai ban PowerShell' }
function ShaText([string]$t) { $h = [Security.Cryptography.SHA256]::Create(); (($h.ComputeHash($utf8.GetBytes($t)) | ForEach-Object { $_.ToString('x2') }) -join '') }
function Sha([string]$p) { (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLower() }
[IO.File]::WriteAllText("$Scratch\frag_cleanup.ps1", $frag, $bom); [IO.File]::WriteAllText("$Scratch\frag_pre.ps1", $pre, $bom)
"SOURCE $(Sha $Skill) cleanup_frag $(ShaText $frag) pre_frag $(ShaText $pre) shell $Shell"
$runner = @'
param([string]$Body)
$ErrorActionPreference = 'Stop'
function Need($Ok, $Msg) { if (-not $Ok) { throw "STOP[PLAYWRIGHT_ADDON_UNAVAILABLE]: $Msg" } }
$session = $env:TL_PW_SESSION
& { $ErrorActionPreference = 'Stop'
  . ([scriptblock]::Create([IO.File]::ReadAllText($Body, [Text.Encoding]::UTF8)))
  'RESIDUE_OK' }
'@
[IO.File]::WriteAllText("$Scratch\runner.ps1", $runner, $bom)
$holder = @'
param([string]$Path, [int]$Seconds, [string]$Ready, [string]$Share)
$fs = [IO.File]::Open($Path, 'Open', 'Read', $Share); [IO.File]::WriteAllText($Ready, 'x'); Start-Sleep -Seconds $Seconds; $fs.Dispose()
'@
[IO.File]::WriteAllText("$Scratch\holder.ps1", $holder, $bom)
$NONCE = 'tl-pw-0123456789ab'; $OTHER = 'tl-pw-ba9876543210'; $H = 'aaaaaaaaaaaaaaaa'; $H2 = 'bbbbbbbbbbbbbbbb'
$script:PASS = 0; $script:FAIL = 0; $script:SKIP = 0; $script:C = $null
function Dm { "$script:C\cache\ms-playwright\daemon" }
function Own { "$(Dm)\$H\$NONCE.err" }
function New-Case([string]$Name) {
  $script:C = "$Scratch\case-$Name"; $d = "$script:C\cache\ms-playwright\daemon"
  New-Item -ItemType Directory -Force -Path "$d\$H", "$d\$H2", "$script:C\run", "$script:C\home" | Out-Null
  [IO.File]::WriteAllText("$d\$H\$NONCE.err", "own stderr $Name`n")
  [IO.File]::WriteAllText("$d\$H\$OTHER.err", "other`n"); [IO.File]::WriteAllText("$d\$H\$OTHER.session", "{}`n")
  [IO.File]::WriteAllText("$d\$H2\tl-pw-111111111111.err", "legacy`n") }
function Decoys { # tung tep KHONG mang nonce (so sanh phan biet hoa thuong): duong dan|kich thuoc|mtime|sha256
  $rows = Get-ChildItem -Force -Recurse -File -LiteralPath "$script:C\cache" -ErrorAction SilentlyContinue |
    Where-Object { -not $_.FullName.Contains($NONCE) } | Sort-Object FullName |
    ForEach-Object { "$($_.FullName)|$($_.Length)|$($_.LastWriteTimeUtc.Ticks)|$(Sha $_.FullName)" }
  ($rows -join "`n") }
function NoNewOutputs { -not (Test-Path -LiteralPath "$script:C\run\11-daemon.err") -and -not (Test-Path -LiteralPath "$script:C\run\11-daemon-path.txt") }
function Run-Frag([string]$Body, [hashtable]$ExtraEnv) {
  $psi = New-Object Diagnostics.ProcessStartInfo
  $psi.FileName = $Shell; $psi.UseShellExecute = $false; $psi.RedirectStandardOutput = $true; $psi.RedirectStandardError = $true
  $psi.WorkingDirectory = "$script:C\home"
  $psi.Arguments = "-NoProfile -NonInteractive -ExecutionPolicy Bypass -File `"$Scratch\runner.ps1`" -Body `"$Body`""
  $psi.EnvironmentVariables['LOCALAPPDATA'] = "$script:C\cache"; $psi.EnvironmentVariables['TL_PW_SESSION'] = $NONCE
  $psi.EnvironmentVariables['TL_PW_RUN'] = "$script:C\run"
  if ($psi.EnvironmentVariables.ContainsKey('PWTEST_DAEMON_SESSION_DIR')) { $psi.EnvironmentVariables.Remove('PWTEST_DAEMON_SESSION_DIR') }
  if ($ExtraEnv) { foreach ($k in $ExtraEnv.Keys) { $psi.EnvironmentVariables[$k] = $ExtraEnv[$k] } }
  $p = [Diagnostics.Process]::Start($psi); $o = $p.StandardOutput.ReadToEndAsync(); $e = $p.StandardError.ReadToEnd(); $p.WaitForExit()
  [IO.File]::WriteAllText("$script:C\out", $o.Result + $e, $utf8)
  @{ rc = $p.ExitCode; ok = (($o.Result -split "`r?`n") -ccontains 'RESIDUE_OK'); stop = ($o.Result + $e).Contains('STOP') } }
function Rec([bool]$Ok, [string]$Name, $R) {
  if ($Ok) { $script:PASS++; "PASS $Name rc=$($R.rc)" } else { $script:FAIL++; "FAIL $Name rc=$($R.rc)"; Get-Content -LiteralPath "$script:C\out" -ErrorAction SilentlyContinue | ForEach-Object { "    $_" } } }
function IsOk($R) { $R.rc -eq 0 -and $R.ok }
function IsStop($R) { $R.rc -ne 0 -and -not $R.ok -and $R.stop }
# Kept: hashtable duong dan -> sha256 phai con nguyen
function Expect-Stop([string]$Name, $R, [string]$D0, [hashtable]$Kept, [switch]$AllowOutputs) {
  $ok = (IsStop $R) -and ($D0 -ceq (Decoys))
  if (-not $AllowOutputs) { $ok = $ok -and (NoNewOutputs) }
  if ($Kept) { foreach ($k in $Kept.Keys) { $ok = $ok -and (Test-Path -LiteralPath $k) -and ((Sha $k) -eq $Kept[$k]) } }
  Rec $ok $Name $R }
function Expect-Ok([string]$Name, $R, [string]$D0, [string]$OwnSha) {
  $ok = (IsOk $R) -and ($D0 -ceq (Decoys)) -and -not (Test-Path -LiteralPath (Own)) -and
    ((Sha "$script:C\run\11-daemon.err") -eq $OwnSha) -and ([IO.File]::ReadAllText("$script:C\run\11-daemon-path.txt") -ceq "$(Own)`n")
  Rec $ok $Name $R }
function Try-Link([string]$Type, [string]$Path, [string]$Target) {
  try { New-Item -ItemType $Type -Path $Path -Target $Target -ErrorAction Stop | Out-Null; $true } catch { $false } }
function Run-Locked([string]$Body, [int]$Seconds, [string]$Share, [hashtable]$ExtraEnv) {
  $ready = "$script:C\ready"
  $h = Start-Process -FilePath $Shell -PassThru -WindowStyle Hidden -ArgumentList "-NoProfile -NonInteractive -ExecutionPolicy Bypass -File `"$Scratch\holder.ps1`" -Path `"$(Own)`" -Seconds $Seconds -Ready `"$ready`" -Share $Share"
  for ($i = 0; $i -lt 100 -and -not (Test-Path -LiteralPath $ready); $i++) { Start-Sleep -Milliseconds 100 }
  if (-not (Test-Path -LiteralPath $ready)) { throw 'holder khong san sang' }
  $r = Run-Frag $Body $ExtraEnv; $null = $h.Handle; $h.WaitForExit(); $r }
$me = [Security.Principal.WindowsIdentity]::GetCurrent().User.Value
function Deny-List([string]$Dir) { & icacls $Dir /deny "*${me}:(RD)" | Out-Null; $LASTEXITCODE -eq 0 }
function Undeny([string]$Dir) { & icacls $Dir /remove:d "*$me" | Out-Null }
$F = "$Scratch\frag_cleanup.ps1"; $P = "$Scratch\frag_pre.ps1"

foreach ($c in 'P1', 'P2') { New-Case $c; if ($c -eq 'P2') { [IO.File]::WriteAllText((Own), '') }
  $d0 = Decoys; $os = Sha (Own); $r = Run-Frag $F; Expect-Ok "$c-positive" $r $d0 $os }
New-Case N1; Remove-Item -LiteralPath (Own); $d0 = Decoys; $r = Run-Frag $F; Expect-Stop N1-zero-match $r $d0
New-Case N2; $dup = "$(Dm)\$H2\$NONCE.err"; [IO.File]::WriteAllText($dup, "dup`n"); $d0 = Decoys
$r = Run-Frag $F; Expect-Stop N2-two-hash-dirs $r $d0 @{ (Own) = (Sha (Own)); $dup = (Sha $dup) }
New-Case N3; $s3 = "$(Dm)\$H\$NONCE.session"; [IO.File]::WriteAllText($s3, "{}`n"); $d0 = Decoys
$r = Run-Frag $F; Expect-Stop N3-session-left $r $d0 @{ (Own) = (Sha (Own)); $s3 = (Sha $s3) }
New-Case N4; $u4 = "$(Dm)\$H\ud-$NONCE-chromium"; New-Item -ItemType Directory -Path $u4 | Out-Null; [IO.File]::WriteAllText("$u4\Prefs", "x`n"); $d0 = Decoys
$r = Run-Frag $F; Expect-Stop N4-userdata-left $r $d0 @{ (Own) = (Sha (Own)); "$u4\Prefs" = (Sha "$u4\Prefs") }
New-Case N5; Remove-Item -LiteralPath (Own)
if (Try-Link SymbolicLink (Own) "$(Dm)\$H\$OTHER.err") { $d0 = Decoys; $r = Run-Frag $F; Expect-Stop N5-err-symlink $r $d0 }
else { $script:SKIP++; 'SKIP N5-err-symlink: khong tao duoc symlink tep (thieu quyen SeCreateSymbolicLink / Developer Mode) - KHONG DO DUOC, khong tinh dat' }
New-Case N6; New-Item -ItemType Directory -Path "$script:C\elsewhere" | Out-Null; Move-Item -LiteralPath (Own) -Destination "$script:C\elsewhere\"
if (Try-Link Junction "$(Dm)\cccccccccccccccc" "$script:C\elsewhere") { $d0 = Decoys; $t = "$script:C\elsewhere\$NONCE.err"
  $r = Run-Frag $F; Expect-Stop N6-hashdir-junction $r $d0 @{ $t = (Sha $t) } } else { $script:FAIL++; 'FAIL N6: khong tao duoc junction' }
New-Case N7; Move-Item -LiteralPath (Dm) -Destination "$script:C\real-daemon"
if (Try-Link Junction (Dm) "$script:C\real-daemon") { $d0 = Decoys; $t = "$script:C\real-daemon\$H\$NONCE.err"
  $r = Run-Frag $F; Expect-Stop N7-daemon-junction $r $d0 @{ $t = (Sha $t) } } else { $script:FAIL++; 'FAIL N7: khong tao duoc junction' }
foreach ($o in '11-daemon.err', '11-daemon-path.txt') { New-Case "N8-$o"; [IO.File]::WriteAllText("$script:C\run\$o", "old`n"); $d0 = Decoys
  $r = Run-Frag $F; Expect-Stop "N8-stale-$o" $r $d0 @{ (Own) = (Sha (Own)); "$script:C\run\$o" = (Sha "$script:C\run\$o") } -AllowOutputs }
New-Case N9; New-Item -ItemType Directory -Path "$(Dm)\not-a-hash" | Out-Null; Move-Item -LiteralPath (Own) -Destination "$(Dm)\not-a-hash\"; $d0 = Decoys
$t = "$(Dm)\not-a-hash\$NONCE.err"; $r = Run-Frag $F; Expect-Stop N9-bad-hash-name $r $d0 @{ $t = (Sha $t) }
New-Case N10; $d0 = Decoys; $r = Run-Frag $F @{ PWTEST_DAEMON_SESSION_DIR = "$script:C\x" }; Expect-Stop N10-pwtest-hook $r $d0 @{ (Own) = (Sha (Own)) }
New-Case N11; Remove-Item -LiteralPath (Own); New-Item -ItemType Directory -Path (Own) | Out-Null; $d0 = Decoys
$r = Run-Frag $F; Expect-Stop N11-err-is-dir $r $d0
New-Case N12; Remove-Item -LiteralPath (Dm) -Recurse -Force; $d0 = Decoys; $r = Run-Frag $F; Expect-Stop N12-no-registry $r $d0
New-Case N13; $up = "$(Dm)\$H2\$($NONCE.ToUpper()).ERR"; [IO.File]::WriteAllText($up, "case`n")
# NTFS khong phan biet hoa thuong: ban viet hoa o thu muc hash khac la muc thu hai => phai dung, ca hai tep nguyen
$d0 = Decoys; $r = Run-Frag $F; Expect-Stop N13-case-variant $r $d0 @{ (Own) = (Sha (Own)); $up = (Sha $up) }
New-Case N14; $w = "$(Dm)\$H\${NONCE}Xerr"; Move-Item -LiteralPath (Own) -Destination $w; $d0 = Decoys
$r = Run-Frag $F; Expect-Stop N14-wrong-suffix $r $d0 @{ $w = (Sha $w) }
New-Case N15; $h3 = "$(Dm)\dddddddddddddddd"; New-Item -ItemType Directory -Path $h3 | Out-Null; [IO.File]::WriteAllText("$h3\$NONCE.session", "{}`n")
if (Deny-List $h3) { $d0 = Decoys; $r = Run-Frag $F; Undeny $h3; Expect-Stop N15-scan-denied $r $d0 @{ (Own) = (Sha (Own)) } }
else { $script:FAIL++; 'FAIL N15: icacls /deny khong dat' }
New-Case N17; $rc17 = "$script:C\home\rel"; New-Item -ItemType Directory -Path $rc17 | Out-Null; Copy-Item -LiteralPath "$script:C\cache" -Destination $rc17 -Recurse
$t = "$rc17\cache\ms-playwright\daemon\$H\$NONCE.err"; $d0 = Decoys
$r = Run-Frag $F @{ LOCALAPPDATA = 'rel\cache' }; Expect-Stop N17-relative-cache $r $d0 @{ (Own) = (Sha (Own)); $t = (Sha $t) }
# L1/L2: tien trinh khac giu .err khong cho DOC (FileShare.None). L3: cho doc nhung khong cho XOA (FileShare.Read).
New-Case L1; $d0 = Decoys; $os = Sha (Own); $r = Run-Locked $F 2 'None'; Expect-Ok L1-read-locked-2s $r $d0 $os
New-Case L2; $d0 = Decoys; $os = Sha (Own); $r = Run-Locked $F 12 'None'; Expect-Stop L2-read-locked-12s $r $d0 @{ (Own) = $os }
New-Case L3; $d0 = Decoys; $os = Sha (Own); $r = Run-Locked $F 2 'Read'; Expect-Ok L3-delete-locked-2s $r $d0 $os
New-Case C1; Remove-Item -LiteralPath (Own); $d0 = Decoys; $r = Run-Frag $P; Rec ((IsOk $r) -and $d0 -ceq (Decoys)) C1-pre-clean $r
New-Case C2; $d0 = Decoys; $r = Run-Frag $P; Expect-Stop C2-pre-nonce-present $r $d0 @{ (Own) = (Sha (Own)) }
New-Case C3; Remove-Item -LiteralPath "$script:C\cache\ms-playwright" -Recurse -Force; $r = Run-Frag $P; Rec (IsOk $r) C3-pre-no-registry $r
New-Case C4; New-Item -ItemType Directory -Path "$script:C\home\rel" | Out-Null; Move-Item -LiteralPath "$script:C\cache" -Destination "$script:C\home\rel\"
$r = Run-Frag $P @{ LOCALAPPDATA = 'rel\cache' }; Rec (IsStop $r) C4-pre-relative-cache $r
New-Case C5; Remove-Item -LiteralPath (Own); $r = Run-Frag $P @{ PWTEST_DAEMON_SESSION_DIR = "$script:C\x" }; Rec (IsStop $r) C5-pre-pwtest-hook $r
New-Case C6; Move-Item -LiteralPath (Own) -Destination "$(Dm)\$NONCE.err"; $r = Run-Frag $P; Rec (IsOk $r) 'C6-pre-depth1-ignored (chi do do sau 2, nhu CLI va bash)' $r

function Mut([string]$Name, [string]$Target, [string]$Src, [string]$Old, [string]$New) {
  $body = [IO.File]::ReadAllText($Src, [Text.Encoding]::UTF8)
  if (-not $body.Contains($Old)) { $script:FAIL++; "FAIL MUT ${Name}: khong tim thay chuoi goc"; return }
  $m = "$Scratch\mut-$Name.ps1"; [IO.File]::WriteAllText($m, $body.Replace($Old, $New), $bom)
  New-Case "M-$Name"; $extra = $null; $expectStop = $false
  switch ($Target) {
    'N2' { [IO.File]::WriteAllText("$(Dm)\$H2\$NONCE.err", "dup`n") }
    'N3' { [IO.File]::WriteAllText("$(Dm)\$H\$NONCE.session", "{}`n") }
    'N7' { Move-Item -LiteralPath (Dm) -Destination "$script:C\real-daemon"
           if (-not (Try-Link Junction (Dm) "$script:C\real-daemon")) { $script:FAIL++; "FAIL MUT ${Name}: junction"; return } }
    'N8' { [IO.File]::WriteAllText("$script:C\run\11-daemon.err", "old`n") }
    'N9' { New-Item -ItemType Directory -Path "$(Dm)\not-a-hash" | Out-Null; Move-Item -LiteralPath (Own) -Destination "$(Dm)\not-a-hash\" }
    'N10' { $extra = @{ PWTEST_DAEMON_SESSION_DIR = 'x' } }
    'N14' { Move-Item -LiteralPath (Own) -Destination "$(Dm)\$H\${NONCE}Xerr" }
    'N15' { $h3 = "$(Dm)\dddddddddddddddd"; New-Item -ItemType Directory -Path $h3 | Out-Null; [IO.File]::WriteAllText("$h3\$NONCE.session", "{}`n")
            if (-not (Deny-List $h3)) { $script:FAIL++; "FAIL MUT ${Name}: icacls"; return } }
    'N17' { New-Item -ItemType Directory -Path "$script:C\home\rel" | Out-Null; Copy-Item -LiteralPath "$script:C\cache" -Destination "$script:C\home\rel" -Recurse
            $extra = @{ LOCALAPPDATA = 'rel\cache' } }
    'C4' { Remove-Item -LiteralPath (Own); New-Item -ItemType Directory -Path "$script:C\home\rel" | Out-Null
           Move-Item -LiteralPath "$script:C\cache" -Destination "$script:C\home\rel\"; $extra = @{ LOCALAPPDATA = 'rel\cache' } }
    'C5' { Remove-Item -LiteralPath (Own); $extra = @{ PWTEST_DAEMON_SESSION_DIR = 'x' } }
    'L1' { $expectStop = $true }
    'L3' { $expectStop = $true }
  }
  if ($Target -eq 'L1') { $r = Run-Locked $m 2 'None' } elseif ($Target -eq 'L3') { $r = Run-Locked $m 2 'Read' } else { $r = Run-Frag $m $extra }
  if ($Target -eq 'N15') { Undeny "$(Dm)\dddddddddddddddd" }
  $caught = if ($expectStop) { -not (IsOk $r) } else { IsOk $r }
  if ($caught) { $script:PASS++; "PASS MUT $Name -> $Target $(if ($expectStop) { 'do' } else { 'lot' }) (chot co rang)" }
  else { $script:FAIL++; "FAIL MUT $Name -> $Target khong doi (chot khong do duoc)"; Get-Content -LiteralPath "$script:C\out" | ForEach-Object { "    $_" } } }
Mut exact-one N2 $F '$hits.Count -eq 1 -and' '$hits.Count -ge 1 -and'
Mut name-filter N3 $F '-Filter "*$session*" -ErrorAction Stop' '-Filter "$session.err" -ErrorAction Stop'
Mut daemon-reparse N7 $F '-not ($dd.Attributes -band $reparse)' '$true'
Mut stale-output N8 $F 'Need (-not (Test-Path -LiteralPath "$env:TL_PW_RUN\$ten"))' 'Need $true'
Mut hash-shape N9 $F "-cmatch '\A[0-9a-f]{16}\z'" "-cmatch '.'"
Mut pwtest-hook N10 $F 'Need (-not (Test-Path -LiteralPath Env:PWTEST_DAEMON_SESSION_DIR))' 'Need $true'
Mut exact-name N14 $F '$f.Name -ceq "$session.err"' '$f.Name -like "$session*err"'
Mut scan-silent N15 $F '-Filter "*$session*" -ErrorAction Stop' '-Filter "*$session*" -ErrorAction SilentlyContinue'
Mut relative-cache N17 $F 'Need ($daemonDir -match ''^([A-Za-z]:\\|\\\\)'')' 'Need ($true)'
Mut pre-relative C4 $P 'Need ($daemonDir -match ''^([A-Za-z]:\\|\\\\)'')' 'Need ($true)'
Mut pre-hook C5 $P 'Need (-not (Test-Path -LiteralPath Env:PWTEST_DAEMON_SESSION_DIR))' 'Need $true'
Mut no-copy-retry L1 $F '$i -lt 5 -and -not $copied' '$i -lt 1 -and -not $copied'
Mut no-delete-retry L3 $F '$i -lt 5 -and (Test-Path -LiteralPath $f.FullName)' '$i -lt 1 -and (Test-Path -LiteralPath $f.FullName)'
"TONG: $script:PASS dat / $($script:PASS + $script:FAIL) (bo qua khong do duoc: $script:SKIP)"
if ($script:FAIL -ne 0) { exit 1 } else { exit 0 }
