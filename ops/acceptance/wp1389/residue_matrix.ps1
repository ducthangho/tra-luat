# Ma tran phan chung PowerShell cho buoc don du luong daemon cua playwright-browser SKILL.md (packet #1389).
# Chay TREN BYTE CUA SKILL: trich NOI DUNG giua cap dong danh dau (khong gom dong danh dau), lan xuat hien THU HAI
# (khoi PowerShell) cua moi cap: "du-luong-daemon-truoc-open" (Capture), "du-luong-daemon-dau-cleanup" (truoc close),
# "du-luong-daemon" (sau 10-verify). SOURCE/frag bam tren byte goc (LF, khong BOM); ban chay cho PS 5.1 co BOM.
# Dong `node -e` cua SKILL chay THAT bang node, tren registry.js GIA (FX_*); registry.js that do o luot native.
# Moi ca chay trong TIEN TRINH CON cua chinh shell dang do ($Shell), CWD = <ca>\home. Khong goi CLI/mang/trinh duyet.
# Dung: <shell> -NoProfile -File residue_matrix.ps1 -Skill <SKILL.md> -Scratch <thu muc rong> -Shell <exe> -Node <node.exe>
# PowerShell 5.1 goi tu pwsh 7 phai mang PSModulePath = gia tri Machine, neu khong se thieu Get-FileHash (do r3 #1319).
# Tep nay CHI ASCII: PS 5.1 doc tep khong BOM theo ANSI.
param([Parameter(Mandatory)][string]$Skill, [Parameter(Mandatory)][string]$Scratch, [Parameter(Mandatory)][string]$Shell,
  [Parameter(Mandatory)][string]$Node)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Skill -PathType Leaf)) { throw 'SKILL.md?' }
if (-not (Test-Path -LiteralPath $Node -PathType Leaf)) { throw 'node?' }
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
$pre = Extract 'du-luong-daemon-truoc-open'; $dau = Extract 'du-luong-daemon-dau-cleanup'; $frag = Extract 'du-luong-daemon'
if (-not ($pre.Contains('$env:TL_PW_NODE') -and $dau.Contains('$hashDir = $so[1]') -and $frag.Contains('[IO.Directory]::GetDirectories('))) { throw 'doan trich khong phai ban PowerShell' }
function ShaText([string]$t) { $h = [Security.Cryptography.SHA256]::Create(); (($h.ComputeHash($utf8.GetBytes($t)) | ForEach-Object { $_.ToString('x2') }) -join '') }
function Sha([string]$p) { (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLower() }
# Ten bien tep KHONG trung ten bien noi dung ($dau/$FileDau la MOT bien: PowerShell khong phan biet hoa thuong).
$FileClean = "$Scratch\frag_dau_cleanup.ps1"; $FileDau = "$Scratch\frag_dau.ps1"; $FilePre = "$Scratch\frag_pre.ps1"
[IO.File]::WriteAllText($FilePre, $pre, $bom); [IO.File]::WriteAllText($FileDau, $dau, $bom); [IO.File]::WriteAllText($FileClean, $dau + $frag, $bom)
"SOURCE $(Sha $Skill) pre_frag $(ShaText $pre) dau_frag $(ShaText $dau) cleanup_frag $(ShaText $frag) shell $Shell node $(& $Node --version)"
$runner = @'
param([string]$Body)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
function Need($Ok, $Msg) { if (-not $Ok) { throw "STOP[PLAYWRIGHT_ADDON_UNAVAILABLE]: $Msg" } }
$session = $env:TL_PW_SESSION
try { & { $ErrorActionPreference = 'Stop'
    . ([scriptblock]::Create([IO.File]::ReadAllText($Body, [Text.Encoding]::UTF8)))
    'RESIDUE_OK' } } catch { "ERR: $($_.Exception.Message)"; exit 1 }
'@
[IO.File]::WriteAllText("$Scratch\runner.ps1", $runner, $bom)
$holder = @'
param([string]$Path, [int]$Seconds, [string]$Ready, [string]$Share)
$fs = [IO.File]::Open($Path, 'Open', 'Read', $Share); [IO.File]::WriteAllText($Ready, 'x'); Start-Sleep -Seconds $Seconds; $fs.Dispose()
'@
[IO.File]::WriteAllText("$Scratch\holder.ps1", $holder, $bom)
$fakeRegistry = 'module.exports={baseDaemonDir:()=>process.env.FX_BASE,createClientInfo:()=>({daemonProfilesDir:process.env.FX_DIR,workspaceDir:process.env.FX_WS||undefined})};'
$KHONG = "KH$([char]0x00D4)NG ch$([char]0x1EA1)y Cleanup"
$NONCE = 'tl-pw-0123456789ab'; $OTHER = 'tl-pw-ba9876543210'; $H = 'aaaaaaaaaaaaaaaa'; $H2 = 'bbbbbbbbbbbbbbbb'
$script:PASS = 0; $script:FAIL = 0; $script:SKIP = 0; $script:C = $null
function Dm { "$script:C\cache\ms-playwright\daemon" }
function Own { "$(Dm)\$H\$NONCE.err" }
function Rec0 { "$script:C\run\00-sophien.txt" }
function New-Case([string]$Name, [switch]$NoRecord) {
  $script:C = "$Scratch\case-$Name"; $d = "$script:C\cache\ms-playwright\daemon"
  New-Item -ItemType Directory -Force -Path "$d\$H", "$d\$H2", "$script:C\run", "$script:C\home", "$script:C\work",
    "$script:C\install\node_modules\playwright-core\lib\tools\cli-client" | Out-Null
  [IO.File]::WriteAllText("$script:C\install\node_modules\playwright-core\lib\tools\cli-client\registry.js", $fakeRegistry, $utf8)
  [IO.File]::WriteAllText("$d\$H\$NONCE.err", "own stderr $Name`n")
  [IO.File]::WriteAllText("$d\$H\$OTHER.err", "other`n"); [IO.File]::WriteAllText("$d\$H\$OTHER.session", "{}`n")
  [IO.File]::WriteAllText("$d\$H2\tl-pw-111111111111.err", "legacy`n")
  if (-not $NoRecord) { [IO.File]::WriteAllText((Rec0), "$d`n$d\$H`n", $utf8) } }
function Decoys { # tung tep KHONG mang nonce (phan biet hoa thuong): duong dan|kich thuoc|mtime|sha256
  $rows = Get-ChildItem -Force -Recurse -File -LiteralPath "$script:C\cache" -ErrorAction SilentlyContinue |
    Where-Object { -not $_.FullName.Contains($NONCE) } | Sort-Object FullName |
    ForEach-Object { "$($_.FullName)|$($_.Length)|$($_.LastWriteTimeUtc.Ticks)|$(Sha $_.FullName)" }
  ($rows -join "`n") }
function Snap([string[]]$Paths) { # chup TRUOC khi chay: ton tai|loai|sha|mtime
  (@($Paths | ForEach-Object { $i = Get-Item -Force -LiteralPath $_ -ErrorAction SilentlyContinue
      if ($i) { "$_|$($i.PSIsContainer)|$(if (-not $i.PSIsContainer) { Sha $_ })|$($i.LastWriteTimeUtc.Ticks)" } else { "$_|MISSING" } }) -join "`n") }
function NoNewOutputs { -not (Test-Path -LiteralPath "$script:C\run\11-daemon.err") -and -not (Test-Path -LiteralPath "$script:C\run\11-daemon-path.txt") }
function Run-Frag([string]$Body, [hashtable]$ExtraEnv) {
  $psi = New-Object Diagnostics.ProcessStartInfo
  $psi.FileName = $Shell; $psi.UseShellExecute = $false; $psi.RedirectStandardOutput = $true; $psi.RedirectStandardError = $true
  $psi.StandardOutputEncoding = $utf8; $psi.StandardErrorEncoding = $utf8; $psi.WorkingDirectory = "$script:C\home"
  $psi.Arguments = "-NoProfile -NonInteractive -ExecutionPolicy Bypass -File `"$Scratch\runner.ps1`" -Body `"$Body`""
  $ev = @{ LOCALAPPDATA = "$script:C\cache"; TL_PW_SESSION = $NONCE; TL_PW_RUN = "$script:C\run"; TL_PW_ROOT = $script:C
    TL_PW_INSTALL = "$script:C\install"; TL_PW_NODE = $Node; FX_BASE = (Dm); FX_DIR = "$(Dm)\$H" }
  foreach ($k in 'PWTEST_DAEMON_SESSION_DIR', 'FX_WS') { if ($psi.EnvironmentVariables.ContainsKey($k)) { $psi.EnvironmentVariables.Remove($k) } }
  foreach ($k in $ev.Keys) { $psi.EnvironmentVariables[$k] = $ev[$k] }
  if ($ExtraEnv) { foreach ($k in $ExtraEnv.Keys) { $psi.EnvironmentVariables[$k] = $ExtraEnv[$k] } }
  $p = [Diagnostics.Process]::Start($psi); $o = $p.StandardOutput.ReadToEndAsync(); $e = $p.StandardError.ReadToEnd(); $p.WaitForExit()
  [IO.File]::WriteAllText("$script:C\out", $o.Result + $e, $utf8)
  @{ rc = $p.ExitCode; ok = (($o.Result -split "`r?`n") -ccontains 'RESIDUE_OK'); text = ($o.Result + $e) } }
function Rec([bool]$Ok, [string]$Name, $R) {
  if ($Ok) { $script:PASS++; "PASS $Name rc=$($R.rc)" } else { $script:FAIL++; "FAIL $Name rc=$($R.rc)"; Get-Content -LiteralPath "$script:C\out" -ErrorAction SilentlyContinue | ForEach-Object { "    $_" } } }
function IsOk($R) { $R.rc -eq 0 -and $R.ok }
function IsStop($R) { $R.rc -ne 0 -and -not $R.ok -and $R.text.Contains('STOP') }
function Expect-Stop([string]$Name, $R, [string]$D0, [string]$S0, [switch]$AllowOutputs) {
  $ok = (IsStop $R) -and ($D0 -ceq (Decoys))
  if ($S0) { $ok = $ok -and ($S0 -ceq (Snap @($S0 -split "`n" | ForEach-Object { ($_ -split '\|')[0] }))) }
  if (-not $AllowOutputs) { $ok = $ok -and (NoNewOutputs) }
  Rec $ok $Name $R }
function Expect-Ok([string]$Name, $R, [string]$D0, [string]$OwnSha) {
  $ok = (IsOk $R) -and ($D0 -ceq (Decoys)) -and -not (Test-Path -LiteralPath (Own)) -and
    ((Sha "$script:C\run\11-daemon.err") -eq $OwnSha) -and ([IO.File]::ReadAllText("$script:C\run\11-daemon-path.txt") -ceq "$(Own)`n")
  Rec $ok $Name $R }
function Pre-Ok([string]$Name, $R) {
  Rec ((IsOk $R) -and (Test-Path -LiteralPath (Rec0)) -and ([IO.File]::ReadAllText((Rec0)) -ceq "$(Dm)`n$(Dm)\$H`n")) $Name $R }
function Pre-Stop([string]$Name, $R) {
  Rec ((IsStop $R) -and $R.text.Contains($KHONG) -and -not (Test-Path -LiteralPath (Rec0))) $Name $R }
function Try-Link([string]$Type, [string]$Path, [string]$Target) {
  try { New-Item -ItemType $Type -Path $Path -Target $Target -ErrorAction Stop | Out-Null; $true } catch { $false } }
function Run-Locked([string]$Body, [int]$Seconds, [string]$Share) {
  $ready = "$script:C\ready"
  $holderProc = Start-Process -FilePath $Shell -PassThru -WindowStyle Hidden -ArgumentList "-NoProfile -NonInteractive -ExecutionPolicy Bypass -File `"$Scratch\holder.ps1`" -Path `"$(Own)`" -Seconds $Seconds -Ready `"$ready`" -Share $Share"
  for ($i = 0; $i -lt 100 -and -not (Test-Path -LiteralPath $ready); $i++) { Start-Sleep -Milliseconds 100 }
  if (-not (Test-Path -LiteralPath $ready)) { throw 'holder khong san sang' }
  $r = Run-Frag $Body; $null = $holderProc.Handle; $holderProc.WaitForExit(); $r }
$me = [Security.Principal.WindowsIdentity]::GetCurrent().User.Value
function Deny-List([string]$Dir) { & icacls $Dir /deny "*${me}:(RD)" | Out-Null; $LASTEXITCODE -eq 0 }
function Undeny([string]$Dir) { & icacls $Dir /remove:d "*$me" | Out-Null }

# ===== Cleanup (dau-cleanup + don du luong) =====
# Bien vong KHONG duoc ten $c: PowerShell khong phan biet hoa thuong nen $c chinh la $script:C ma New-Case ghi de.
foreach ($caseName in 'P1', 'P2') { New-Case $caseName; if ($caseName -eq 'P2') { [IO.File]::WriteAllText((Own), '') }
  $sz = (Get-Item -LiteralPath (Own)).Length; $want = if ($caseName -eq 'P2') { 0 } else { $utf8.GetByteCount("own stderr $caseName`n") }
  Rec ($sz -eq $want) "$caseName-fixture-size=$sz" @{ rc = '-' }
  $d0 = Decoys; $os = Sha (Own); $r = Run-Frag $FileClean; Expect-Ok "$caseName-positive" $r $d0 $os }
New-Case N1; Remove-Item -LiteralPath (Own); $d0 = Decoys; $r = Run-Frag $FileClean; Expect-Stop N1-zero-match $r $d0 ''
New-Case N2; $dup = "$(Dm)\$H2\$NONCE.err"; [IO.File]::WriteAllText($dup, "dup`n"); $d0 = Decoys; $s0 = Snap @((Own), $dup)
$r = Run-Frag $FileClean; Expect-Stop N2-two-hash-dirs $r $d0 $s0
New-Case N3; $s3 = "$(Dm)\$H\$NONCE.session"; [IO.File]::WriteAllText($s3, "{}`n"); $d0 = Decoys; $s0 = Snap @((Own), $s3)
$r = Run-Frag $FileClean; Expect-Stop N3-session-left $r $d0 $s0
New-Case N4; $u4 = "$(Dm)\$H\ud-$NONCE-chromium"; New-Item -ItemType Directory -Path $u4 | Out-Null; [IO.File]::WriteAllText("$u4\Prefs", "x`n")
$d0 = Decoys; $s0 = Snap @((Own), "$u4\Prefs"); $r = Run-Frag $FileClean; Expect-Stop N4-userdata-left $r $d0 $s0
New-Case N5; Remove-Item -LiteralPath (Own)
if (Try-Link SymbolicLink (Own) "$(Dm)\$H\$OTHER.err") { $d0 = Decoys; $r = Run-Frag $FileClean; Expect-Stop N5-err-symlink $r $d0 '' }
else { $script:SKIP++; 'SKIP N5-err-symlink: khong tao duoc symlink tep (thieu quyen SeCreateSymbolicLink / Developer Mode) - KHONG DO DUOC, khong tinh dat' }
New-Case N6; New-Item -ItemType Directory -Path "$script:C\elsewhere" | Out-Null; Move-Item -LiteralPath (Own) -Destination "$script:C\elsewhere\"
if (Try-Link Junction "$(Dm)\cccccccccccccccc" "$script:C\elsewhere") { $d0 = Decoys; $s0 = Snap @("$script:C\elsewhere\$NONCE.err")
  $r = Run-Frag $FileClean; Expect-Stop N6-other-hashdir-junction $r $d0 $s0 } else { $script:FAIL++; 'FAIL N6: khong tao duoc junction' }
New-Case N7; Move-Item -LiteralPath (Dm) -Destination "$script:C\real-daemon"
if (Try-Link Junction (Dm) "$script:C\real-daemon") { $d0 = Decoys; $s0 = Snap @("$script:C\real-daemon\$H\$NONCE.err")
  $r = Run-Frag $FileClean; Expect-Stop N7-daemon-junction $r $d0 $s0 } else { $script:FAIL++; 'FAIL N7: khong tao duoc junction' }
foreach ($pair in @(@('11-daemon.err', '11-daemon-path.txt'), @('11-daemon-path.txt', '11-daemon.err'))) {
  New-Case "N8-$($pair[0])"; [IO.File]::WriteAllText("$script:C\run\$($pair[0])", "old`n"); $d0 = Decoys; $s0 = Snap @((Own), "$script:C\run\$($pair[0])")
  $r = Run-Frag $FileClean; Expect-Stop "N8-stale-$($pair[0])" $r $d0 $s0 -AllowOutputs
  Rec (-not (Test-Path -LiteralPath "$script:C\run\$($pair[1])")) "N8-$($pair[0])-no-$($pair[1])" $r }
New-Case N9; New-Item -ItemType Directory -Path "$(Dm)\not-a-hash" | Out-Null; Move-Item -LiteralPath (Own) -Destination "$(Dm)\not-a-hash\"
$d0 = Decoys; $s0 = Snap @("$(Dm)\not-a-hash\$NONCE.err"); $r = Run-Frag $FileClean; Expect-Stop N9-bad-hash-name $r $d0 $s0
New-Case N10; $d0 = Decoys; $s0 = Snap @((Own)); $r = Run-Frag $FileClean @{ PWTEST_DAEMON_SESSION_DIR = "$script:C\x" }; Expect-Stop N10-pwtest-hook $r $d0 $s0
New-Case N11; Remove-Item -LiteralPath (Own); New-Item -ItemType Directory -Path (Own) | Out-Null; $d0 = Decoys; $r = Run-Frag $FileClean; Expect-Stop N11-err-is-dir $r $d0 ''
New-Case N12; Remove-Item -LiteralPath (Dm) -Recurse -Force; $d0 = Decoys; $r = Run-Frag $FileClean; Expect-Stop N12-no-registry $r $d0 ''
New-Case N13; $up = "$(Dm)\$H2\$($NONCE.ToUpper()).ERR"; [IO.File]::WriteAllText($up, "case`n")
# NTFS khong phan biet hoa thuong: ban viet hoa o thu muc hash khac la muc thu hai => phai dung, ca hai tep nguyen
$d0 = Decoys; $s0 = Snap @((Own), $up); $r = Run-Frag $FileClean; Expect-Stop N13-case-variant $r $d0 $s0
New-Case N14; $w = "$(Dm)\$H\${NONCE}Xerr"; Move-Item -LiteralPath (Own) -Destination $w; $d0 = Decoys; $s0 = Snap @($w)
$r = Run-Frag $FileClean; Expect-Stop N14-wrong-suffix $r $d0 $s0
New-Case N15; $h3 = "$(Dm)\dddddddddddddddd"; New-Item -ItemType Directory -Path $h3 | Out-Null; [IO.File]::WriteAllText("$h3\$NONCE.session", "{}`n")
$s15 = Sha "$h3\$NONCE.session"
if (Deny-List $h3) { $d0 = Decoys; $s0 = Snap @((Own)); $r = Run-Frag $FileClean; Undeny $h3; Expect-Stop N15-scan-denied $r $d0 $s0
  Rec ((Sha "$h3\$NONCE.session") -eq $s15) 'N15-hidden-entry-kept' $r } else { $script:FAIL++; 'FAIL N15: icacls /deny khong dat' }
New-Case N17; $rel = "$script:C\home\rel"; New-Item -ItemType Directory -Path $rel | Out-Null; Copy-Item -LiteralPath "$script:C\cache" -Destination $rel -Recurse
[IO.File]::WriteAllText((Rec0), "rel\cache\ms-playwright\daemon`nrel\cache\ms-playwright\daemon\$H`n", $utf8)
$d0 = Decoys; $s0 = Snap @((Own), "$rel\cache\ms-playwright\daemon\$H\$NONCE.err")
$r = Run-Frag $FileClean @{ FX_BASE = 'rel\cache\ms-playwright\daemon'; FX_DIR = "rel\cache\ms-playwright\daemon\$H" }; Expect-Stop N17-relative-cache $r $d0 $s0
New-Case N18; Move-Item -LiteralPath (Own) -Destination "$(Dm)\$H2\"; $d0 = Decoys; $s0 = Snap @("$(Dm)\$H2\$NONCE.err")
$r = Run-Frag $FileClean; Expect-Stop N18-err-in-other-install-dir $r $d0 $s0
New-Case N19; Move-Item -LiteralPath "$(Dm)\$H" -Destination "$script:C\real-hash"
if (Try-Link Junction "$(Dm)\$H" "$script:C\real-hash") { $d0 = Decoys; $s0 = Snap @("$script:C\real-hash\$NONCE.err")
  $r = Run-Frag $FileClean; Expect-Stop N19-own-hashdir-junction $r $d0 $s0 } else { $script:FAIL++; 'FAIL N19: khong tao duoc junction' }
# L1/L2: tien trinh khac giu .err khong cho DOC (FileShare.None). L3: cho doc nhung khong cho XOA (FileShare.Read).
New-Case L1; $d0 = Decoys; $os = Sha (Own); $r = Run-Locked $FileClean 2 'None'; Expect-Ok L1-read-locked-2s $r $d0 $os
New-Case L2; $d0 = Decoys; $s0 = Snap @((Own)); $r = Run-Locked $FileClean 12 'None'; Expect-Stop L2-read-locked-12s $r $d0 $s0 -AllowOutputs
Rec ([IO.File]::ReadAllText("$script:C\run\11-daemon-path.txt") -ceq "$(Own)`n") 'L2-path-recorded-before-copy (B4)' $r
New-Case L3; $d0 = Decoys; $os = Sha (Own); $r = Run-Locked $FileClean 2 'Read'; Expect-Ok L3-delete-locked-2s $r $d0 $os
# dau-cleanup: dung TRUOC close
New-Case D1 -NoRecord; $d0 = Decoys; $s0 = Snap @((Own)); $r = Run-Frag $FileDau; Expect-Stop D1-no-capture-record $r $d0 $s0
New-Case D2; $d0 = Decoys; $s0 = Snap @((Own)); $r = Run-Frag $FileDau @{ FX_DIR = "$(Dm)\$H2" }; Expect-Stop D2-registry-changed $r $d0 $s0
New-Case D3; $d0 = Decoys; $s0 = Snap @((Own)); $r = Run-Frag $FileDau @{ FX_WS = 'C:\somewhere' }; Expect-Stop D3-cli-workspace-mode $r $d0 $s0
New-Case D4; $r = Run-Frag $FileDau; Rec (IsOk $r) D4-dau-matches $r
# ===== truoc open =====
New-Case C1 -NoRecord; Remove-Item -LiteralPath (Own); $r = Run-Frag $FilePre; Pre-Ok C1-pre-clean $r
New-Case C2 -NoRecord; $s0 = Snap @((Own)); $r = Run-Frag $FilePre; Pre-Stop C2-pre-nonce-present $r; Rec ($s0 -ceq (Snap @((Own)))) C2-own-kept $r
New-Case C3 -NoRecord; Remove-Item -LiteralPath "$script:C\cache\ms-playwright" -Recurse -Force; $r = Run-Frag $FilePre; Pre-Ok C3-pre-no-registry $r
New-Case C4 -NoRecord; Remove-Item -LiteralPath (Own); $r = Run-Frag $FilePre @{ FX_BASE = 'rel\d'; FX_DIR = "rel\d\$H" }; Pre-Stop C4-pre-relative $r
New-Case C5 -NoRecord; Remove-Item -LiteralPath (Own); $r = Run-Frag $FilePre @{ PWTEST_DAEMON_SESSION_DIR = "$script:C\x" }; Pre-Stop C5-pre-pwtest-hook $r
New-Case C6 -NoRecord; Move-Item -LiteralPath (Own) -Destination "$(Dm)\$NONCE.err"; $r = Run-Frag $FilePre; Pre-Ok 'C6-pre-depth1-ignored (nhu CLI va bash)' $r
New-Case C7 -NoRecord; Remove-Item -LiteralPath (Own); $h7 = "$(Dm)\dddddddddddddddd"; New-Item -ItemType Directory -Path $h7 | Out-Null; [IO.File]::WriteAllText("$h7\$NONCE.err", "x`n")
if (Deny-List $h7) { $r = Run-Frag $FilePre; Undeny $h7; Pre-Stop C7-pre-scan-denied $r } else { $script:FAIL++; 'FAIL C7: icacls /deny khong dat' }
New-Case C8 -NoRecord; Remove-Item -LiteralPath (Own); $r = Run-Frag $FilePre @{ FX_WS = 'C:\somewhere' }; Pre-Stop C8-pre-cli-workspace-mode $r
New-Case C9 -NoRecord; Remove-Item -LiteralPath (Own); Move-Item -LiteralPath (Dm) -Destination "$script:C\real-daemon"
if (Try-Link Junction (Dm) "$script:C\real-daemon") { $r = Run-Frag $FilePre; Pre-Stop C9-pre-daemon-junction $r } else { $script:FAIL++; 'FAIL C9: junction' }
New-Case C10 -NoRecord; Remove-Item -LiteralPath (Own); Move-Item -LiteralPath "$(Dm)\$H" -Destination "$script:C\real-hash"
if (Try-Link Junction "$(Dm)\$H" "$script:C\real-hash") { $r = Run-Frag $FilePre; Pre-Stop C10-pre-hashdir-junction $r } else { $script:FAIL++; 'FAIL C10: junction' }
New-Case C11 -NoRecord; Remove-Item -LiteralPath (Own); $r = Run-Frag $FilePre @{ FX_DIR = "$(Dm)\not-a-hash" }; Pre-Stop C11-pre-bad-hash-shape $r
New-Case C12 -NoRecord; Remove-Item -LiteralPath (Own); $r = Run-Frag $FilePre @{ FX_DIR = "$script:C\elsewhere\$H" }; Pre-Stop C12-pre-hash-not-under-base $r
New-Case C13 -NoRecord; Remove-Item -LiteralPath (Own); $r = Run-Frag $FilePre @{ TL_PW_NODE = "$script:C\no-such-node.exe" }; Pre-Stop C13-pre-node-missing $r

# ===== dot bien =====
function Mut([string]$Name, [string]$Target, [string]$Src, [string]$Old, [string]$New) {
  $body = [IO.File]::ReadAllText($Src, [Text.Encoding]::UTF8)
  if (-not $body.Contains($Old)) { $script:FAIL++; "FAIL MUT ${Name}: khong tim thay chuoi goc"; return }
  $m = "$Scratch\mut-$Name.ps1"; [IO.File]::WriteAllText($m, $body.Replace($Old, $New), $bom)
  $preTarget = $Target -like 'C*'
  if ($preTarget -or $Target -eq 'D1') { New-Case "M-$Name" -NoRecord } else { New-Case "M-$Name" }
  if ($preTarget) { Remove-Item -LiteralPath (Own) }
  $extra = $null; $expectStop = $false
  switch ($Target) {
    'N3' { [IO.File]::WriteAllText("$(Dm)\$H\$NONCE.session", "{}`n") }
    'N7' { Move-Item -LiteralPath (Dm) -Destination "$script:C\real-daemon"
           if (-not (Try-Link Junction (Dm) "$script:C\real-daemon")) { $script:FAIL++; "FAIL MUT ${Name}: junction"; return } }
    'N8' { [IO.File]::WriteAllText("$script:C\run\11-daemon.err", "old`n") }
    'N10' { $extra = @{ PWTEST_DAEMON_SESSION_DIR = 'x' } }
    'N14' { Move-Item -LiteralPath (Own) -Destination "$(Dm)\$H\${NONCE}Xerr" }
    'N15' { $h3 = "$(Dm)\dddddddddddddddd"; New-Item -ItemType Directory -Path $h3 | Out-Null; [IO.File]::WriteAllText("$h3\$NONCE.session", "{}`n")
            if (-not (Deny-List $h3)) { $script:FAIL++; "FAIL MUT ${Name}: icacls"; return } }
    'N17' { New-Item -ItemType Directory -Path "$script:C\home\rel" | Out-Null; Copy-Item -LiteralPath "$script:C\cache" -Destination "$script:C\home\rel" -Recurse
            [IO.File]::WriteAllText((Rec0), "rel\cache\ms-playwright\daemon`nrel\cache\ms-playwright\daemon\$H`n", $utf8)
            $extra = @{ FX_BASE = 'rel\cache\ms-playwright\daemon'; FX_DIR = "rel\cache\ms-playwright\daemon\$H" } }
    'N18' { Move-Item -LiteralPath (Own) -Destination "$(Dm)\$H2\" }
    'D2' { $extra = @{ FX_DIR = "$(Dm)\$H2" } }
    'C4' { $extra = @{ FX_BASE = 'rel\d'; FX_DIR = "rel\d\$H" } }
    'C5' { $extra = @{ PWTEST_DAEMON_SESSION_DIR = 'x' } }
    'C7' { $h3 = "$(Dm)\dddddddddddddddd"; New-Item -ItemType Directory -Path $h3 | Out-Null; [IO.File]::WriteAllText("$h3\$NONCE.err", "x`n")
           if (-not (Deny-List $h3)) { $script:FAIL++; "FAIL MUT ${Name}: icacls"; return } }
    'C9' { Move-Item -LiteralPath (Dm) -Destination "$script:C\real-daemon"
           if (-not (Try-Link Junction (Dm) "$script:C\real-daemon")) { $script:FAIL++; "FAIL MUT ${Name}: junction"; return } }
    'C11' { $extra = @{ FX_DIR = "$(Dm)\not-a-hash" } }
    'L1' { $expectStop = $true }
    'L3' { $expectStop = $true }
  }
  if ($Target -eq 'L1') { $r = Run-Locked $m 2 'None' } elseif ($Target -eq 'L3') { $r = Run-Locked $m 2 'Read' } else { $r = Run-Frag $m $extra }
  if ($Target -eq 'N15' -or $Target -eq 'C7') { Undeny "$(Dm)\dddddddddddddddd" }
  $caught = if ($expectStop) { -not (IsOk $r) } else { IsOk $r }
  if ($caught) { $script:PASS++; "PASS MUT $Name -> $Target $(if ($expectStop) { 'do' } else { 'lot' }) (chot co rang)" }
  else { $script:FAIL++; "FAIL MUT $Name -> $Target khong doi (chot khong do duoc)"; Get-Content -LiteralPath "$script:C\out" | ForEach-Object { "    $_" } } }
# exact-one: thu tu liet ke phu thuoc thu muc, nen thu hai thu tu tao tep; co rang neu MOT thu tu lam ca lot
$body1 = [IO.File]::ReadAllText($FileClean, [Text.Encoding]::UTF8)
if ($body1.Contains('$hits.Count -eq 1 -and')) { [IO.File]::WriteAllText("$Scratch\mut-exact-one.ps1", $body1.Replace('$hits.Count -eq 1 -and', '$hits.Count -ge 1 -and'), $bom); $lot = $false
  foreach ($order in 'session-first', 'session-last') { New-Case "M-exact-one-$order"; Remove-Item -LiteralPath (Own); $s1 = "$(Dm)\$H\$NONCE.session"
    if ($order -eq 'session-first') { [IO.File]::WriteAllText($s1, "{}`n"); [IO.File]::WriteAllText((Own), "own`n") } else { [IO.File]::WriteAllText((Own), "own`n"); [IO.File]::WriteAllText($s1, "{}`n") }
    $r = Run-Frag "$Scratch\mut-exact-one.ps1"; if (IsOk $r) { $lot = $true } }
  if ($lot) { $script:PASS++; 'PASS MUT exact-one -> N3 (mot trong hai thu tu) lot (chot co rang)' } else { $script:FAIL++; 'FAIL MUT exact-one -> N3 van chan o ca hai thu tu' }
} else { $script:FAIL++; 'FAIL MUT exact-one: khong tim thay chuoi goc' }
Mut name-filter N3 $FileClean 'GetFileSystemEntries($_, "*$session*")' 'GetFileSystemEntries($_, "$session.err")'
Mut daemon-reparse N7 $FileClean 'foreach ($d in $daemonDir, $hashDir) { Need (Test-Path' 'foreach ($d in @()) { Need (Test-Path'
Mut stale-output N8 $FileClean 'Need (-not (Test-Path -LiteralPath "$env:TL_PW_RUN\$ten"))' 'Need $true'
Mut pwtest-hook N10 $FileClean 'Need (-not (Test-Path -LiteralPath Env:PWTEST_DAEMON_SESSION_DIR))' 'Need $true'
Mut exact-path N14 $FileClean '$f.FullName -ceq "$hashDir\$session.err"' '$f.Name -like "$session*err"'
Mut scan-silent N15 $FileClean '[IO.Directory]::GetFileSystemEntries($_, "*$session*")' '@(Get-ChildItem -Force -LiteralPath $_ -Filter "*$session*" -ErrorAction SilentlyContinue | ForEach-Object FullName)'
# N17 trong PS duoc chan HAI lop: chot tuyet doi, va FullName (Get-Item tra duong dan tuyet doi) khong bao gio bang
# "$hashDir\..." tuong doi. Dot bien go MOT lop khong lam ca lot (do 2875afc), nen dot bien nay go CA HAI.
$preMutRel = "$Scratch\pre-mut-relative.ps1"
[IO.File]::WriteAllText($preMutRel, ([IO.File]::ReadAllText($FileClean, [Text.Encoding]::UTF8)).Replace('$f.FullName -ceq "$hashDir\$session.err"', '$f.Name -ceq "$session.err"'), $bom)
Mut relative-cache-and-path N17 $preMutRel 'Need ($daemonDir -match ''^([A-Za-z]:\\|\\\\)'')' 'Need ($true)'
Mut install-dir-binding N18 $FileClean '$f.FullName -ceq "$hashDir\$session.err"' '$f.Name -ceq "$session.err"'
Mut no-capture-record D1 $FileDau '(Test-Path -LiteralPath $rec -PathType Leaf) -and' '$true -or'
Mut no-registry-compare D2 $FileDau '([IO.File]::ReadAllText($rec) -ceq "$($so[0])`n$($so[1])`n")' '$true'
Mut pre-relative C4 $FilePre '$so[0] -match ''^([A-Za-z]:\\|\\\\[^\\]+\\[^\\]+\\)'' -and' '$true -and'
Mut pre-hook C5 $FilePre 'Need (-not (Test-Path -LiteralPath Env:PWTEST_DAEMON_SESSION_DIR))' 'Need $true'
Mut pre-scan-silent C7 $FilePre '[IO.Directory]::GetFileSystemEntries($_, "*$env:TL_PW_SESSION*")' '@(Get-ChildItem -Force -LiteralPath $_ -Filter "*$env:TL_PW_SESSION*" -ErrorAction SilentlyContinue | ForEach-Object FullName)'
Mut pre-link C9 $FilePre 'Need (-not ((Get-Item -Force -LiteralPath $d).Attributes -band $reparse)) "' 'Need ($true) "'
Mut pre-shape C11 $FilePre '(Split-Path -Leaf $so[1]) -cmatch ''\A[0-9a-f]{16}\z''' '$true'
Mut no-copy-retry L1 $FileClean '$i -lt 5 -and -not $copied' '$i -lt 1 -and -not $copied'
Mut no-delete-retry L3 $FileClean '$i -lt 5 -and (Test-Path -LiteralPath $f.FullName)' '$i -lt 1 -and (Test-Path -LiteralPath $f.FullName)'
"TONG: $script:PASS dat / $($script:PASS + $script:FAIL) (bo qua khong do duoc: $script:SKIP)"
if ($script:FAIL -ne 0) { exit 1 } else { exit 0 }
