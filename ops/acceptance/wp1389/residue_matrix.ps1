# Ma tran phan chung PowerShell cho buoc don du luong daemon cua playwright-browser SKILL.md (packet #1389).
# Chay TREN BYTE CUA SKILL: trich doan giua hai dong danh dau trong khoi Cleanup PowerShell va doan kiem truoc
# `open` trong khoi Capture PowerShell. Moi ca chay trong TIEN TRINH CON cua chinh shell dang do ($Shell), voi
# LOCALAPPDATA tro vao scratch. Khong goi CLI, khong mang, khong trinh duyet.
# Dung: <shell> -NoProfile -File residue_matrix.ps1 -Skill <SKILL.md> -Scratch <thu muc rong> -Shell <pwsh.exe|powershell.exe>
# PowerShell 5.1 goi tu pwsh 7 phai mang PSModulePath = gia tri Machine, neu khong se thieu Get-FileHash (do r3 #1319).
param([Parameter(Mandatory)][string]$Skill, [Parameter(Mandatory)][string]$Scratch, [Parameter(Mandatory)][string]$Shell)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Skill -PathType Leaf)) { throw 'SKILL.md?' }
if (-not (Test-Path -LiteralPath $Scratch -PathType Container) -or @(Get-ChildItem -Force -LiteralPath $Scratch).Count) { throw 'Scratch phai rong' }
$Scratch = (Resolve-Path -LiteralPath $Scratch).ProviderPath
$utf8 = New-Object System.Text.UTF8Encoding($true)
$src = [IO.File]::ReadAllText($Skill, [Text.Encoding]::UTF8) -replace "`r`n", "`n"
$lines = $src -split "`n"
$begin = @(); $end = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
  if ($lines[$i] -ceq '  # --- du-luong-daemon: bat dau') { $begin += $i }
  if ($lines[$i] -ceq '  # --- du-luong-daemon: het') { $end += $i } }
if ($begin.Count -ne 2 -or $end.Count -ne 2) { throw "can 2 cap danh dau, thay $($begin.Count)/$($end.Count)" }
$frag = ($lines[$begin[1]..$end[1]] -join "`n") + "`n"
if (-not $frag.Contains('$hits = @(Get-ChildItem')) { throw 'khong trich duoc doan PowerShell' }
$pi = @(); for ($i = 0; $i -lt $lines.Count; $i++) { if ($lines[$i].StartsWith('  $daemonDir = "$cacheRoot\ms-playwright\daemon"   # ')) { $pi += $i } }
if ($pi.Count -ne 1) { throw "doan kiem truoc open: thay $($pi.Count)" }
$pre = ($lines[($pi[0] - 1)..($pi[0] + 2)] -join "`n") + "`n"
if (-not ($lines[$pi[0] - 1].StartsWith('  $cacheRoot = ') -and $lines[$pi[0] + 1].StartsWith('  Need (-not (Test-Path -LiteralPath $daemonDir)'))) { throw 'doan kiem truoc open sai dang' }
[IO.File]::WriteAllText("$Scratch\frag_cleanup.ps1", $frag, $utf8); [IO.File]::WriteAllText("$Scratch\frag_pre.ps1", $pre, $utf8)
function Sha([string]$p) { (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLower() }
"SOURCE $(Sha $Skill) cleanup_frag $(Sha "$Scratch\frag_cleanup.ps1") pre_frag $(Sha "$Scratch\frag_pre.ps1") shell $Shell"
$prelude = @'
param([string]$Body)
$ErrorActionPreference = 'Stop'
function Need($Ok, $Msg) { if (-not $Ok) { throw "STOP[PLAYWRIGHT_ADDON_UNAVAILABLE]: $Msg" } }
$session = $env:TL_PW_SESSION
& { $ErrorActionPreference = 'Stop'
  . ([scriptblock]::Create([IO.File]::ReadAllText($Body, [Text.Encoding]::UTF8)))
  'RESIDUE_OK' }
'@
[IO.File]::WriteAllText("$Scratch\runner.ps1", $prelude, $utf8)
$NONCE = 'tl-pw-0123456789ab'; $OTHER = 'tl-pw-ba9876543210'; $H = 'aaaaaaaaaaaaaaaa'; $H2 = 'bbbbbbbbbbbbbbbb'
$script:PASS = 0; $script:FAIL = 0; $script:SKIP = 0; $script:C = $null
function New-Case([string]$Name) {
  $script:C = "$Scratch\case-$Name"; $d = "$script:C\cache\ms-playwright\daemon"
  New-Item -ItemType Directory -Force -Path "$d\$H", "$d\$H2", "$script:C\run" | Out-Null
  [IO.File]::WriteAllText("$d\$H\$NONCE.err", "own stderr $Name`n")
  [IO.File]::WriteAllText("$d\$H\$OTHER.err", "other`n"); [IO.File]::WriteAllText("$d\$H\$OTHER.session", "{}`n")
  [IO.File]::WriteAllText("$d\$H2\tl-pw-111111111111.err", "legacy`n") }
function Own { "$script:C\cache\ms-playwright\daemon\$H\$NONCE.err" }
function Decoys {
  $rows = Get-ChildItem -Force -Recurse -File -LiteralPath "$script:C\cache" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notlike "*$NONCE*" } | Sort-Object FullName |
    ForEach-Object { "$($_.FullName)|$($_.Length)|$($_.LastWriteTimeUtc.Ticks)|$(Sha $_.FullName)" }
  ($rows -join "`n") }
function Run-Frag([string]$Body, [hashtable]$ExtraEnv) {
  $psi = New-Object Diagnostics.ProcessStartInfo
  $psi.FileName = $Shell; $psi.UseShellExecute = $false; $psi.RedirectStandardOutput = $true; $psi.RedirectStandardError = $true
  $psi.Arguments = "-NoProfile -NonInteractive -ExecutionPolicy Bypass -File `"$Scratch\runner.ps1`" -Body `"$Body`""
  $psi.EnvironmentVariables['LOCALAPPDATA'] = "$script:C\cache"; $psi.EnvironmentVariables['TL_PW_SESSION'] = $NONCE
  $psi.EnvironmentVariables['TL_PW_RUN'] = "$script:C\run"
  if ($psi.EnvironmentVariables.ContainsKey('PWTEST_DAEMON_SESSION_DIR')) { $psi.EnvironmentVariables.Remove('PWTEST_DAEMON_SESSION_DIR') }
  if ($ExtraEnv) { foreach ($k in $ExtraEnv.Keys) { $psi.EnvironmentVariables[$k] = $ExtraEnv[$k] } }
  $p = [Diagnostics.Process]::Start($psi); $o = $p.StandardOutput.ReadToEndAsync(); $e = $p.StandardError.ReadToEnd(); $p.WaitForExit()
  [IO.File]::WriteAllText("$script:C\out", $o.Result + $e, $utf8)
  @{ rc = $p.ExitCode; ok = (($o.Result -split "`r?`n") -ccontains 'RESIDUE_OK'); stop = ($o.Result + $e).Contains('STOP') } }
function Rec([bool]$Ok, [string]$Name, $R) {
  if ($Ok) { $script:PASS++; "PASS $Name rc=$($R.rc)" } else { $script:FAIL++; "FAIL $Name rc=$($R.rc)"; Get-Content -LiteralPath "$script:C\out" | ForEach-Object { "    $_" } } }
function Expect([string]$Name, [string]$Want, $R, [bool]$OwnRemains, [string]$D0) {
  $ok = ($D0 -ceq (Decoys))
  if ($Want -eq 'ok') { $ok = $ok -and $R.rc -eq 0 -and $R.ok } else { $ok = $ok -and $R.rc -ne 0 -and -not $R.ok -and $R.stop }
  if ($OwnRemains) { $ok = $ok -and (Test-Path -LiteralPath (Own)) }
  Rec $ok $Name $R }
function Try-Link([string]$Type, [string]$Path, [string]$Target) {
  try { New-Item -ItemType $Type -Path $Path -Target $Target -ErrorAction Stop | Out-Null; $true } catch { $false } }
$F = "$Scratch\frag_cleanup.ps1"

New-Case P1; $d0 = Decoys; $ownSha = Sha (Own); $r = Run-Frag $F; Expect P1-positive ok $r $false $d0
$okA = -not (Test-Path -LiteralPath (Own)) -and (Sha "$script:C\run\11-daemon.err") -eq $ownSha -and
  ([IO.File]::ReadAllText("$script:C\run\11-daemon-path.txt")) -ceq "$(Own)`n"
Rec $okA 'P1-artefacts' $r
New-Case P2; [IO.File]::WriteAllText((Own), ''); $d0 = Decoys; $r = Run-Frag $F; Expect P2-empty-err ok $r $false $d0
New-Case N1; Remove-Item -LiteralPath (Own); $d0 = Decoys; $r = Run-Frag $F; Expect N1-zero-match stop $r $false $d0
New-Case N2; [IO.File]::WriteAllText("$script:C\cache\ms-playwright\daemon\$H2\$NONCE.err", "dup`n"); $d0 = Decoys
$r = Run-Frag $F; Expect N2-two-hash-dirs stop $r $true $d0
Rec (Test-Path -LiteralPath "$script:C\cache\ms-playwright\daemon\$H2\$NONCE.err") 'N2-dup-kept' $r
New-Case N3; [IO.File]::WriteAllText("$script:C\cache\ms-playwright\daemon\$H\$NONCE.session", "{}`n"); $d0 = Decoys
$r = Run-Frag $F; Expect N3-session-left stop $r $true $d0
New-Case N4; New-Item -ItemType Directory -Path "$script:C\cache\ms-playwright\daemon\$H\ud-$NONCE-chromium" | Out-Null; $d0 = Decoys
$r = Run-Frag $F; Expect N4-userdata-left stop $r $true $d0
New-Case N5; Remove-Item -LiteralPath (Own)
if (Try-Link SymbolicLink (Own) "$script:C\cache\ms-playwright\daemon\$H\$OTHER.err") {
  $d0 = Decoys; $r = Run-Frag $F; Expect N5-err-symlink stop $r $true $d0
} else { $script:SKIP++; 'SKIP N5-err-symlink: khong tao duoc symlink tep (thieu quyen SeCreateSymbolicLink / Developer Mode) — KHONG DO DUOC, khong tinh dat' }
New-Case N6; New-Item -ItemType Directory -Path "$script:C\elsewhere" | Out-Null; Move-Item -LiteralPath (Own) -Destination "$script:C\elsewhere\"
if (Try-Link Junction "$script:C\cache\ms-playwright\daemon\cccccccccccccccc" "$script:C\elsewhere") {
  $d0 = Decoys; $r = Run-Frag $F; Expect N6-hashdir-junction stop $r $false $d0
  Rec (Test-Path -LiteralPath "$script:C\elsewhere\$NONCE.err") 'N6-target-kept' $r
} else { $script:FAIL++; 'FAIL N6: khong tao duoc junction' }
New-Case N7; Move-Item -LiteralPath "$script:C\cache\ms-playwright\daemon" -Destination "$script:C\real-daemon"
if (Try-Link Junction "$script:C\cache\ms-playwright\daemon" "$script:C\real-daemon") {
  $d0 = Decoys; $r = Run-Frag $F; Expect N7-daemon-junction stop $r $false $d0
  Rec (Test-Path -LiteralPath "$script:C\real-daemon\$H\$NONCE.err") 'N7-target-kept' $r
} else { $script:FAIL++; 'FAIL N7: khong tao duoc junction' }
New-Case N8; [IO.File]::WriteAllText("$script:C\run\11-daemon.err", "old`n"); $d0 = Decoys
$r = Run-Frag $F; Expect N8-stale-output stop $r $true $d0
Rec ([IO.File]::ReadAllText("$script:C\run\11-daemon.err") -ceq "old`n") 'N8-old-kept' $r
New-Case N9; New-Item -ItemType Directory -Path "$script:C\cache\ms-playwright\daemon\not-a-hash" | Out-Null
Move-Item -LiteralPath (Own) -Destination "$script:C\cache\ms-playwright\daemon\not-a-hash\"; $d0 = Decoys
$r = Run-Frag $F; Expect N9-bad-hash-name stop $r $false $d0
Rec (Test-Path -LiteralPath "$script:C\cache\ms-playwright\daemon\not-a-hash\$NONCE.err") 'N9-kept' $r
New-Case N10; $d0 = Decoys; $r = Run-Frag $F @{ PWTEST_DAEMON_SESSION_DIR = "$script:C\x" }; Expect N10-pwtest-hook stop $r $true $d0
New-Case N11; Remove-Item -LiteralPath (Own); New-Item -ItemType Directory -Path (Own) | Out-Null; $d0 = Decoys
$r = Run-Frag $F; Expect N11-err-is-dir stop $r $true $d0
New-Case N12; Remove-Item -LiteralPath "$script:C\cache\ms-playwright\daemon" -Recurse -Force; $d0 = Decoys
$r = Run-Frag $F; Expect N12-no-registry stop $r $false $d0
New-Case N13; [IO.File]::WriteAllText("$script:C\cache\ms-playwright\daemon\$H2\$($NONCE.ToUpper()).ERR", "case`n")
# NTFS khong phan biet hoa thuong: ban viet hoa o thu muc hash khac la muc thu hai => phai dung
$d0 = Decoys; $r = Run-Frag $F; Expect N13-case-variant stop $r $true $d0
$P = "$Scratch\frag_pre.ps1"
New-Case C1; Remove-Item -LiteralPath (Own); $d0 = Decoys; $r = Run-Frag $P; Expect C1-pre-clean ok $r $false $d0
New-Case C2; $d0 = Decoys; $r = Run-Frag $P; Expect C2-pre-nonce-present stop $r $true $d0
New-Case C3; Remove-Item -LiteralPath "$script:C\cache\ms-playwright" -Recurse -Force; $d0 = Decoys; $r = Run-Frag $P; Expect C3-pre-no-registry ok $r $false $d0

function Mut([string]$Name, [string]$Target, [string]$Old, [string]$New) {
  $body = [IO.File]::ReadAllText($F, [Text.Encoding]::UTF8)
  if (-not $body.Contains($Old)) { $script:FAIL++; "FAIL MUT ${Name}: khong tim thay chuoi goc"; return }
  $m = "$Scratch\mut-$Name.ps1"; [IO.File]::WriteAllText($m, $body.Replace($Old, $New), $utf8)
  New-Case "M-$Name"; $extra = $null
  switch ($Target) {
    'N2' { [IO.File]::WriteAllText("$script:C\cache\ms-playwright\daemon\$H2\$NONCE.err", "dup`n") }
    'N3' { [IO.File]::WriteAllText("$script:C\cache\ms-playwright\daemon\$H\$NONCE.session", "{}`n") }
    'N7' { Move-Item -LiteralPath "$script:C\cache\ms-playwright\daemon" -Destination "$script:C\real-daemon"
           if (-not (Try-Link Junction "$script:C\cache\ms-playwright\daemon" "$script:C\real-daemon")) { $script:FAIL++; "FAIL MUT ${Name}: junction"; return } }
    'N8' { [IO.File]::WriteAllText("$script:C\run\11-daemon.err", "old`n") }
    'N9' { New-Item -ItemType Directory -Path "$script:C\cache\ms-playwright\daemon\not-a-hash" | Out-Null
           Move-Item -LiteralPath (Own) -Destination "$script:C\cache\ms-playwright\daemon\not-a-hash\" }
    'N10' { $extra = @{ PWTEST_DAEMON_SESSION_DIR = 'x' } }
  }
  $r = Run-Frag $m $extra
  if ($r.rc -eq 0 -and $r.ok) { $script:PASS++; "PASS MUT $Name -> $Target lot (chot co rang)" }
  else { $script:FAIL++; "FAIL MUT $Name -> $Target van chan (chot khong do duoc)"; Get-Content -LiteralPath "$script:C\out" | ForEach-Object { "    $_" } } }
Mut exact-one N2 '$hits.Count -eq 1 -and' '$hits.Count -ge 1 -and'
Mut name-filter N3 '-Filter "*$session*"' '-Filter "$session.err"'
Mut daemon-reparse N7 '-not ($dd.Attributes -band $reparse)' '$true'
Mut stale-output N8 'Need (-not (Test-Path -LiteralPath "$env:TL_PW_RUN\$ten"))' 'Need $true'
Mut hash-shape N9 "-cmatch '\A[0-9a-f]{16}\z'" "-cmatch '.'"
Mut pwtest-hook N10 'Need (-not (Test-Path -LiteralPath Env:PWTEST_DAEMON_SESSION_DIR))' 'Need $true'
"TONG: $script:PASS dat / $($script:PASS + $script:FAIL) (bo qua khong do duoc: $script:SKIP)"
if ($script:FAIL -ne 0) { exit 1 } else { exit 0 }
