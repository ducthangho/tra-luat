#requires -Version 7.0
$ErrorActionPreference = 'Stop'
# -WindowStyle exists only on Windows; splat it so the same file runs unchanged on Linux pwsh.
$hidden = @{}
if ($IsWindows) { $hidden['WindowStyle'] = 'Hidden' }
$root = Join-Path ([IO.Path]::GetTempPath()) ('wp710-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $root | Out-Null
$script = Join-Path $PSScriptRoot 'nlm-credential-refresh.ps1'
$cases = 0
try {
    $source = @'
import json, os, subprocess, sys, time
op = sys.argv[1] if len(sys.argv) > 1 else "stage"
if op == "--version":
    print("fake-nlm 1.0")
    sys.exit(0)
tag = os.environ.get("WP710_TAG", "")
def note(kind):
    with open(os.environ["WP710_LOG"], "a", encoding="utf-8") as log:
        log.write(f"{kind}:{op}:{os.getpid()}:{tag}\n")
    if os.environ.get("WP710_TIMELOG"):
        with open(os.environ["WP710_TIMELOG"], "a", encoding="utf-8") as tlog:
            tlog.write(f"{kind} {op} {time.time()}\n")
note("start")
if op == "stage" and os.environ.get("WP710_ENVLOG"):
    with open(os.environ["WP710_ENVLOG"], "w", encoding="utf-8") as elog:
        elog.write(os.environ.get("TL_NOTEBOOK_ID", "<absent>"))
mode = os.environ.get("WP710_MODE", "ok")
if mode == "leak_all":
    print("SECRET_SENTINEL", file=sys.stderr)
    if op != "notebook":
        print("SECRET_SENTINEL")
if mode == "beat":
    for _ in range(int(os.environ.get("WP710_DELAY", "0")) // 100):
        note("beat")
        time.sleep(0.1)
else:
    time.sleep(int(os.environ.get("WP710_DELAY", "0")) / 1000)
if mode == "timeout" and op == "auth":
    time.sleep(5)
if mode == "timeout_canary" and op == "notebook":
    time.sleep(5)
if mode == "linger" and op == "auth":
    subprocess.Popen([sys.executable, "-c", "import time; time.sleep(20)"])
    sys.exit(0)
if mode == "err_conn_reset" and op == "auth":
    print("Error running `nlm auth refresh`: connection reset by peer", file=sys.stderr)
    sys.exit(1)
if mode == "err_login_hint" and op == "auth":
    print("network unreachable; if this persists run `nlm login`", file=sys.stderr)
    sys.exit(1)
if mode == "err_traceback" and op == "auth":
    print('Traceback (most recent call last):\n  File "/x/nlm/auth/refresh.py", line 9\nValueError: boom', file=sys.stderr)
    sys.exit(1)
if mode == "err_line401" and op == "auth":
    print('Traceback (most recent call last):\n  File "/x/nlm/auth/refresh.py", line 401\nKeyError: cookies', file=sys.stderr)
    sys.exit(1)
if mode == "err_mixed" and op == "auth":
    print("Authentication expired after connection reset by peer", file=sys.stderr)
    sys.exit(1)
if mode == "err_http401" and op == "auth":
    print("HTTP 401 Unauthorized", file=sys.stderr)
    sys.exit(1)
if mode == "err_503" and op == "auth":
    print("503 Service Unavailable", file=sys.stderr)
    sys.exit(1)
if mode == "auth_second" and op == "auth":
    counter = os.path.join(os.path.dirname(os.environ["WP710_LOG"]), "auth-count.txt")
    seen = int(open(counter).read()) if os.path.exists(counter) else 0
    open(counter, "w").write(str(seen + 1))
    if seen >= 1:
        print("Authentication expired", file=sys.stderr)
        sys.exit(7)
if mode == "auth" and op == "auth":
    print("auth expired SECRET_SENTINEL", file=sys.stderr)
    sys.exit(7)
if mode == "network" and op == "notebook":
    print("network failure SECRET_SENTINEL", file=sys.stderr)
    sys.exit(8)
if mode == "stage" and op == "stage":
    print("SECRET_SENTINEL", file=sys.stderr)
    sys.exit(9)
if op == "notebook":
    if mode == "empty":
        print("{}")
    elif mode == "wrongcase":
        print(json.dumps({"id": sys.argv[3].lower(), "title": "Test"}))
    elif mode == "noname":
        print(json.dumps({"id": sys.argv[3]}))
    else:
        body = {"id": "WRONG12345" if mode == "wrong" else sys.argv[3], "title": "Test"}
        if mode == "leak_all":
            body["note"] = "SECRET_SENTINEL"
        print(json.dumps(body))
note("end")
'@
    $fake = Join-Path $root 'fake.py'
    Set-Content -LiteralPath $fake -Value $source -Encoding utf8
    $python = (Get-Command python).Source
    $browserProfile = Join-Path $root 'profile'
    New-Item -ItemType Directory -Path $browserProfile | Out-Null
    $config = Join-Path $root 'config.json'
    @{notebook_id='NOTEBOOK12345';browser_profile_path=$browserProfile} | ConvertTo-Json | Set-Content -LiteralPath $config
    $env:WP710_LOG = Join-Path $root 'calls.log'
    # [HINT reviewer - CHUA chay tren cay that; executor tu ap, tu do, tu chiu trach nhiem] lop: khoa-va-timeout-khong-rang-buoc-cay-tien-trinh-con
    function Invoke-Wrapper([string]$mode, [string[]]$extra = @(), [string]$cfg = $config, [string]$tag = '') {
        $env:WP710_MODE = $mode; $env:WP710_TAG = $tag
        Remove-Item -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue
        $wargs = @('-NoProfile','-File',$script,'-ConfigPath',$cfg,'-NlmCommand',$python,'-NlmArgumentsPrefix',$fake,
                   '-StageCommand',$python,'-StageArguments',$fake) + $extra
        $sw = [Diagnostics.Stopwatch]::StartNew()
        $out = & pwsh @wargs 2>&1
        $rc = $LASTEXITCODE
        $sw.Stop()
        $strings = @($out | Where-Object { $_ -is [string] })
        [pscustomobject]@{
            Rc = $rc; Seconds = $sw.Elapsed.TotalSeconds
            Text = (($out | ForEach-Object { "$_" }) -join "`n")
            Json = $(if ($strings.Count) { $strings[-1] | ConvertFrom-Json } else { $null })
            Calls = @(Get-Content -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue)
        }
    }
    foreach ($mode in @('ok','auth','network','timeout','wrong','empty','stage')) {
        $env:WP710_MODE = $mode
        Remove-Item -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue
        # $args is an automatic variable inside PowerShell functions; never reuse that name.
        $loopArgs = @('-NoProfile','-File',$script,'-ConfigPath',$config,'-NlmCommand',$python,
                  '-NlmArgumentsPrefix',$fake,'-StageCommand',$python,
                  '-StageArguments',$fake,'-TimeoutSeconds',$(if ($mode -eq 'timeout') { '1' } else { '5' }))
        $output = & pwsh @loopArgs
        $rc = $LASTEXITCODE
        $result = $output | Select-Object -Last 1 | ConvertFrom-Json
        $calls = @(Get-Content -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue)
        $stageCalls = @($calls | Where-Object { $_ -like 'start:stage:*' }).Count
        $expected = @{ok='staged';auth='auth_failure';network='network_failure';
                      timeout='timeout';wrong='inconclusive';empty='inconclusive';stage='stage_failure'}[$mode]
        if ($result.status -ne $expected -or $output -match 'SECRET_SENTINEL' -or
            $stageCalls -ne [int]($mode -in @('ok','stage')) -or
            (($mode -eq 'ok') -ne ($rc -eq 0))) {
            throw "case $mode failed: status=$($result.status) rc=$rc stageCalls=$stageCalls"
        }
        $cases++
    }
    # [HINT reviewer - CHUA chay tren cay that; executor tu ap, tu do, tu chiu trach nhiem] lop: phan-loai-loi-doan-bang-chuoi-tu-do
    # <<case:c
    # (c) nhan trang thai KHONG duoc suy tu tu khoa tran (`auth`/`login`/`cookie`) vi chinh ten lenh (`nlm auth refresh`) va goi y
    #     (`nlm login`) nam trong stderr. Nhan mong doi la cach doc cua reviewer; executor co the doi kem ly do, nhung moi
    #     dau vao duoi day PHAI cho cung mot nhan on dinh va KHONG duoc stage.
    # WP710 r4/g3: anchored phrases only; command names, hints and paths are stripped; mixed signals are inconclusive.
    foreach ($case in @(@('err_conn_reset','network_failure'), @('err_login_hint','network_failure'), @('err_traceback','inconclusive'),
                        @('err_line401','inconclusive'), @('err_mixed','inconclusive'), @('err_http401','auth_failure'),
                        @('err_503','network_failure'), @('auth','auth_failure'))) {
        $r = Invoke-Wrapper $case[0] @('-TimeoutSeconds','5')
        if ($r.Json.status -ne $case[1] -or @($r.Calls | Where-Object { $_ -like 'start:stage:*' }).Count -ne 0) {
            throw ('free-text classification wrong for ' + $case[0] + ': got ' + $r.Json.status + ', expected ' + $case[1])
        }
    }
    $cases++
    # >>case:c
    # Explicit keepalive is bounded; default made just one cycle above.
    $env:WP710_MODE = 'ok'
    Remove-Item -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue
    $output = & pwsh -NoProfile -File $script -ConfigPath $config -NlmCommand $python `
        -NlmArgumentsPrefix $fake -StageCommand $python -StageArguments $fake `
        -EnableKeepalive -MaxCycles 2 -IntervalSeconds 1
    if ($LASTEXITCODE -ne 0 -or @($output).Count -ne 2) { throw 'keepalive cycle count' }
    $cases++
    # The OS mutex must serialize two native processes. Each holds the lock through stage.
    $env:WP710_DELAY = '200'
    Remove-Item -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue
    $powershell = (Get-Command pwsh).Source
    $argline = '-NoProfile -File "' + $script + '" -ConfigPath "' + $config + '" -NlmCommand "' + $python + '" -NlmArgumentsPrefix "' + $fake + '" -StageCommand "' + $python + '" -StageArguments "' + $fake + '"'
    $one = Start-Process -FilePath $powershell -ArgumentList $argline -PassThru @hidden -RedirectStandardOutput (Join-Path $root 'one.out')
    $two = Start-Process -FilePath $powershell -ArgumentList $argline -PassThru @hidden -RedirectStandardOutput (Join-Path $root 'two.out')
    $one.WaitForExit(); $two.WaitForExit()
    if ($one.ExitCode -ne 0 -or $two.ExitCode -ne 0) { throw 'concurrent process failed' }
    $lines = @(Get-Content -LiteralPath $env:WP710_LOG)
    $depth = 0
    foreach ($line in $lines) {
        if ($line -like 'start:*') { $depth++ } else { $depth-- }
        if ($depth -gt 1 -or $depth -lt 0) { throw 'concurrent critical sections overlap' }
    }
    if (@($lines | Where-Object { $_ -like 'start:stage:*' }).Count -ne 2) { throw 'missing concurrent stage' }
    $cases++
    # [HINT reviewer - CHUA chay tren cay that; executor tu ap, tu do, tu chiu trach nhiem] lop: test-ps1-thieu-rang
    # <<case:d
    # (d) ho so goc thieu / notebook_id sai / than canary khong co title|name => inconclusive, 0 thao tac con (Spec r4 #1, #2)
    $cfgNoProfile = Join-Path $root 'config-noprofile.json'
    @{notebook_id='NOTEBOOK12345';browser_profile_path=(Join-Path $root 'no-such-profile')} | ConvertTo-Json | Set-Content -LiteralPath $cfgNoProfile
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5') $cfgNoProfile
    if ($r.Json.status -ne 'inconclusive' -or $r.Rc -eq 0 -or $r.Calls.Count -ne 0) { throw 'missing original profile must be inconclusive with zero operations' }
    $cfgBadId = Join-Path $root 'config-badid.json'
    @{notebook_id='bad id!';browser_profile_path=$browserProfile} | ConvertTo-Json | Set-Content -LiteralPath $cfgBadId
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5') $cfgBadId
    if ($r.Json.status -ne 'inconclusive' -or $r.Rc -eq 0 -or $r.Calls.Count -ne 0) { throw 'invalid notebook_id must be inconclusive with zero operations' }
    $r = Invoke-Wrapper 'noname' @('-TimeoutSeconds','5')
    if ($r.Json.status -ne 'inconclusive' -or @($r.Calls | Where-Object { $_ -like 'start:stage:*' }).Count -ne 0) { throw 'canary body without title/name must not stage' }
    $r = Invoke-Wrapper 'wrongcase' @('-TimeoutSeconds','5')
    if ($r.Json.status -ne 'inconclusive' -or @($r.Calls | Where-Object { $_ -like 'start:stage:*' }).Count -ne 0) { throw 'notebook id must match case-sensitively' }
    $cases++
    # >>case:d
    # <<case:e
    # (e) thu tu refresh -> canary -> stage, dung 1 lan moi buoc, va bang chung ghi lai (Spec r4 #1, #4)
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5')
    $order = (@($r.Calls | Where-Object { $_ -like 'start:*' } | ForEach-Object { ($_ -split ':')[1] }) -join ',')
    if ($order -ne 'auth,notebook,stage') { throw ('operation order must be auth,notebook,stage; got ' + $order) }
    if ($r.Json.status -ne 'staged' -or $r.Json.cli_version -ne '1.0' -or $r.Json.profile_fingerprint -notmatch '^[0-9A-Fa-f]{16}$' -or $r.Json.rc -ne 0 -or $r.Json.elapsed_seconds -le 0) {
        throw 'emitted evidence fields (cli_version/profile_fingerprint/rc/elapsed_seconds) missing or wrong'
    }
    $cases++
    # >>case:e
    # <<case:f
    # (f) -MaxCycles/-IntervalSeconds KHONG tu bat keepalive: thieu -EnableKeepalive thi dung MOT chu ky (Spec r4 #6)
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-MaxCycles','3','-IntervalSeconds','1')
    if ($r.Rc -ne 0 -or @($r.Calls | Where-Object { $_ -like 'start:stage:*' }).Count -ne 1) { throw '-MaxCycles without -EnableKeepalive must run exactly one cycle' }
    $cases++
    # >>case:f
    # <<case:g
    # (g) sentinel khong lot ra stdout LAN stderr, ke ca duong THANH CONG (`leak_all` in sentinel o stdout+stderr cua MOI thao tac) (Spec r4 #4)
    foreach ($m in @('leak_all','auth','network','stage')) {
        $r = Invoke-Wrapper $m @('-TimeoutSeconds','5')
        if ($r.Text -match 'SECRET_SENTINEL') { throw ('sentinel leaked to stdout/stderr in mode ' + $m) }
    }
    $r = Invoke-Wrapper 'leak_all' @('-TimeoutSeconds','5')
    if ($r.Json.status -ne 'staged') { throw 'leak_all control must still stage' }
    $cases++
    # >>case:g
    # <<case:h
    # (h) het han cho khoa => fail-closed, KHONG chay thao tac nao; ten khoa lay TU SCRIPT (khong cung) (Spec r4 #6)
    $lockFromScript = [regex]::Match((Get-Content -LiteralPath $script -Raw), 'Mutex\]::new\(\$false,\s*''([^'']+)''\)').Groups[1].Value
    if (-not $lockFromScript -or -not (Select-String -LiteralPath $PSCommandPath -SimpleMatch $lockFromScript -Quiet)) { throw 'script lock name not found, or the abandoned-owner case no longer holds that exact name' }
    $holdScript = Join-Path $root 'hold.ps1'
    @'
param([string]$Name, [string]$Ready, [int]$Seconds)
$m = [Threading.Mutex]::new($false, $Name)
[void]$m.WaitOne()
Set-Content -LiteralPath $Ready -Value 'held'
Start-Sleep -Seconds $Seconds
$m.ReleaseMutex()
'@ | Set-Content -LiteralPath $holdScript
    $readyHold = Join-Path $root 'ready-hold'
    $holder = Start-Process -FilePath $powershell -ArgumentList ('-NoProfile -File "' + $holdScript + '" -Name "' + $lockFromScript + '" -Ready "' + $readyHold + '" -Seconds 8') -PassThru @hidden
    for ($i=0; $i -lt 100 -and -not (Test-Path -LiteralPath $readyHold); $i++) { Start-Sleep -Milliseconds 100 }
    if (-not (Test-Path -LiteralPath $readyHold)) { throw 'lock holder did not start' }
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
    if ($r.Rc -eq 0 -or $r.Json.status -ne 'inconclusive' -or $r.Calls.Count -ne 0) { throw 'lock-wait timeout must fail closed without running any operation' }
    $holder.WaitForExit()
    $cases++
    # >>case:h
    # <<case:i
    # (i) MOT khoa cho ca refresh -> canary -> stage cua MOI tien trinh (khong phai khoa tung thao tac) (Spec r4 #4)
    $env:WP710_MODE = 'ok'; $env:WP710_DELAY = '200'
    Remove-Item -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue
    $argT = '-NoProfile -File "' + $script + '" -ConfigPath "' + $config + '" -NlmCommand "' + $python + '" -NlmArgumentsPrefix "' + $fake + '" -StageCommand "' + $python + '" -StageArguments "' + $fake + '"'
    $env:WP710_TAG = 'one'; $t1 = Start-Process -FilePath $powershell -ArgumentList $argT -PassThru @hidden -RedirectStandardOutput (Join-Path $root 't1.out')
    $env:WP710_TAG = 'two'; $t2 = Start-Process -FilePath $powershell -ArgumentList $argT -PassThru @hidden -RedirectStandardOutput (Join-Path $root 't2.out')
    $t1.WaitForExit(); $t2.WaitForExit()
    if ($t1.ExitCode -ne 0 -or $t2.ExitCode -ne 0) { throw 'tagged concurrent wrappers failed' }
    $groups = @()
    foreach ($ln in @(Get-Content -LiteralPath $env:WP710_LOG | Where-Object { $_ -like 'start:*' })) {
        $tg = ($ln -split ':')[3]
        if ($groups.Count -eq 0 -or $groups[-1] -ne $tg) { $groups += $tg }
    }
    if ($groups.Count -ne 2) { throw ('refresh -> canary -> stage must be one critical section per process; tag sequence: ' + ($groups -join ',')) }
    $env:WP710_DELAY = '0'
    $cases++
    # >>case:i
    # <<case:j
    # (j) qua han => con BI GIET (khong de chay tiep), va nhan `timeout` cung ap cho buoc canary (Spec r4 #1, #5)
    $r = Invoke-Wrapper 'timeout' @('-TimeoutSeconds','1')
    Start-Sleep -Seconds 5
    if (@(Get-Content -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue | Where-Object { $_ -like 'end:auth:*' }).Count -ne 0) { throw 'timed-out child must be killed, not left to finish' }
    $r = Invoke-Wrapper 'timeout_canary' @('-TimeoutSeconds','1')
    if ($r.Json.status -ne 'timeout' -or @($r.Calls | Where-Object { $_ -like 'start:stage:*' }).Count -ne 0) { throw 'canary timeout must report status timeout and not stage' }
    $env:WP710_MODE = 'ok'; $env:WP710_TAG = ''; $env:WP710_DELAY = '200'
    $cases++
    # >>case:j
    # A killed owner leaves an abandoned OS mutex; takeover is then permitted.
    $lockName = 'Global\tra_luat_nlm_credential_refresh'
    $ownerScript = Join-Path $root 'owner.ps1'
    @'
param([string]$Name, [string]$Ready)
$m = [Threading.Mutex]::new($false, $Name)
[void]$m.WaitOne()
Set-Content -LiteralPath $Ready -Value 'held'
Start-Sleep -Seconds 30
'@ | Set-Content -LiteralPath $ownerScript
    $ready = Join-Path $root 'ready'
    $owner = Start-Process -FilePath $powershell -ArgumentList ('-NoProfile -File "' + $ownerScript + '" -Name "' + $lockName + '" -Ready "' + $ready + '"') -PassThru @hidden
    for ($i=0; $i -lt 50 -and -not (Test-Path -LiteralPath $ready); $i++) { Start-Sleep -Milliseconds 100 }
    if (-not (Test-Path -LiteralPath $ready)) { throw 'owner did not acquire lock' }
    Stop-Process -Id $owner.Id -Force
    $owner.WaitForExit()
    $env:WP710_DELAY = '0'
    $output = & pwsh -NoProfile -File $script -ConfigPath $config -NlmCommand $python `
        -NlmArgumentsPrefix $fake -StageCommand $python -StageArguments $fake
    if ($LASTEXITCODE -ne 0 -or ($output | Select-Object -Last 1 | ConvertFrom-Json).status -ne 'staged') {
        throw 'abandoned mutex takeover failed'
    }
    $cases++
    $env:WP710_DELAY = '0'
    # <<case:a
    # (a) mot hau due (trinh duyet/daemon) giu pipe stdout/stderr sau khi CLI thoat rc 0 khong duoc keo dai qua -TimeoutSeconds
    $r = Invoke-Wrapper 'linger' @('-TimeoutSeconds','2')
    if ($r.Seconds -gt 12) { throw ('wrapper exceeded its own timeout budget: ' + [int]$r.Seconds + 's with -TimeoutSeconds 2 (a descendant held the redirected pipes)') }
    $cases++
    # >>case:a
    # <<case:b
    # (b) chu khoa bi giet khi thao tac con dang chay: wrapper ke tiep KHONG duoc chay thao tac chong len thao tac con cua chu cu
    $env:WP710_MODE = 'beat'; $env:WP710_DELAY = '4000'; $env:WP710_TAG = 'A'
    Remove-Item -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue
    $argA = '-NoProfile -File "' + $script + '" -ConfigPath "' + $config + '" -NlmCommand "' + $python + '" -NlmArgumentsPrefix "' + $fake + '" -StageCommand "' + $python + '" -StageArguments "' + $fake + '"'
    $wa = Start-Process -FilePath $powershell -ArgumentList $argA -PassThru @hidden
    for ($i=0; $i -lt 100 -and -not (Test-Path -LiteralPath $env:WP710_LOG -PathType Leaf -ErrorAction SilentlyContinue); $i++) { Start-Sleep -Milliseconds 100 }
    for ($i=0; $i -lt 100 -and -not (@(Get-Content -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue) -like 'beat:auth:*:A'); $i++) { Start-Sleep -Milliseconds 100 }
    if (-not (@(Get-Content -LiteralPath $env:WP710_LOG) -like 'beat:auth:*:A')) { throw 'wrapper A never started its child' }
    Stop-Process -Id $wa.Id -Force
    $wa.WaitForExit()
    $env:WP710_MODE = 'ok'; $env:WP710_DELAY = '0'; $env:WP710_TAG = 'B'
    & pwsh -NoProfile -File $script -ConfigPath $config -NlmCommand $python -NlmArgumentsPrefix $fake -StageCommand $python -StageArguments $fake -LockWaitSeconds 20 2>&1 | Out-Null
    Start-Sleep -Seconds 5
    $lines = @(Get-Content -LiteralPath $env:WP710_LOG)
    $firstB = -1
    for ($i=0; $i -lt $lines.Count; $i++) { if ($lines[$i] -like 'start:*:B') { $firstB = $i; break } }
    if ($firstB -ge 0 -and @($lines[$firstB..($lines.Count-1)] | Where-Object { $_ -like 'beat:*:A' }).Count -gt 0) {
        throw 'operations overlapped: wrapper B started while the dead wrapper A child was still running'
    }
    $cases++
    # >>case:b
    $env:WP710_DELAY = '0'
    # <<case:k
    # (k) WP710 r4/g3 Spec #1 evidence: rc/elapsed of EVERY step (not just stage), honest profile binding,
    #     and the stage child receives the trusted notebook so both canaries probe the same notebook.
    $env:WP710_ENVLOG = Join-Path $root 'stage-env.txt'
    Remove-Item -LiteralPath $env:WP710_ENVLOG -ErrorAction SilentlyContinue
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5')
    $s = $r.Json.steps
    if ($r.Json.status -ne 'staged' -or $r.Json.cycle -ne 1 -or $r.Json.profile_bound_to_cli -ne $false -or
        $s.version.rc -ne 0 -or $s.refresh.rc -ne 0 -or $s.refresh.elapsed_seconds -le 0 -or $s.refresh.timeout -ne $false -or
        $s.canary.rc -ne 0 -or $s.canary.elapsed_seconds -le 0 -or $s.stage.rc -ne 0 -or $s.stage.elapsed_seconds -le 0) {
        throw ('per-step evidence missing or wrong: ' + ($r.Json | ConvertTo-Json -Compress -Depth 5))
    }
    if ((Get-Content -LiteralPath $env:WP710_ENVLOG -Raw) -cne 'NOTEBOOK12345') { throw 'stage child did not receive TL_NOTEBOOK_ID of the trusted config' }
    $r = Invoke-Wrapper 'auth' @('-TimeoutSeconds','5')
    if ($r.Json.steps.refresh.rc -ne 7 -or $null -ne $r.Json.steps.canary -or $null -ne $r.Json.steps.stage) {
        throw 'refresh failure evidence must carry the real refresh rc and no later step'
    }
    Remove-Item Env:WP710_ENVLOG
    # A later keepalive cycle must not carry the previous cycle's canary/stage evidence.
    Remove-Item -LiteralPath (Join-Path $root 'auth-count.txt') -ErrorAction SilentlyContinue
    $r = Invoke-Wrapper 'auth_second' @('-TimeoutSeconds','5','-EnableKeepalive','-MaxCycles','2','-IntervalSeconds','1')
    if ($r.Rc -ne 2 -or $r.Json.cycle -ne 2 -or $r.Json.status -ne 'auth_failure' -or $r.Json.steps.refresh.rc -ne 7 -or
        $null -ne $r.Json.steps.canary -or $null -ne $r.Json.steps.stage) {
        throw ('cycle 2 evidence carries stale steps from cycle 1: ' + ($r.Json | ConvertTo-Json -Compress -Depth 5))
    }
    $cases++
    # >>case:k
    # <<case:l
    # (l) keepalive keeps its interval: cycle 2 refresh starts no earlier than IntervalSeconds after cycle 1 stage ended.
    $env:WP710_TIMELOG = Join-Path $root 'times.log'
    Remove-Item -LiteralPath $env:WP710_TIMELOG -ErrorAction SilentlyContinue
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-EnableKeepalive','-MaxCycles','2','-IntervalSeconds','2')
    $times = @(Get-Content -LiteralPath $env:WP710_TIMELOG)
    $endStage = @($times | Where-Object { $_ -like 'end stage *' })
    $startAuth = @($times | Where-Object { $_ -like 'start auth *' })
    if ($r.Rc -ne 0 -or $endStage.Count -ne 2 -or $startAuth.Count -ne 2) { throw 'keepalive did not run two full cycles' }
    $gap = [double]($startAuth[1] -split ' ')[2] - [double]($endStage[0] -split ' ')[2]
    if ($gap -lt 1.8) { throw ('keepalive interval not honoured: gap ' + $gap + 's for -IntervalSeconds 2') }
    Remove-Item Env:WP710_TIMELOG
    $cases++
    # >>case:l
    # <<case:m
    # (m) operation record: a live recorded child blocks a new owner (fail closed, zero operations); a dead pid,
    #     a reused pid (different start time) do not; an unreadable record fails closed. Path is read from the script.
    $recName = [regex]::Match((Get-Content -LiteralPath $script -Raw), "GetTempPath\(\)\)\s+'([^']+)'").Groups[1].Value
    if (-not $recName) { throw 'operation record name not found in script' }
    $recPath = Join-Path ([IO.Path]::GetTempPath()) $recName
    $sleeper = Start-Process -FilePath $python -ArgumentList '-c "import time; time.sleep(60)"' -PassThru @hidden
    try {
        $ticks = $sleeper.StartTime.ToUniversalTime().Ticks
        @{pid=$sleeper.Id; start_ticks=$ticks} | ConvertTo-Json -Compress | Set-Content -LiteralPath $recPath
        $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
        if ($r.Rc -ne 5 -or $r.Json.step -ne 'lock_busy' -or $r.Calls.Count -ne 0) { throw 'live recorded child must block the new owner with zero operations' }
        @{pid=$sleeper.Id; start_ticks=($ticks - 36000000000)} | ConvertTo-Json -Compress | Set-Content -LiteralPath $recPath
        $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
        if ($r.Rc -ne 0 -or $r.Json.status -ne 'staged') { throw 'a reused pid with another start time must not block' }
    } finally { Stop-Process -Id $sleeper.Id -Force -ErrorAction SilentlyContinue }
    $sleeper.WaitForExit()
    @{pid=$sleeper.Id; start_ticks=$ticks} | ConvertTo-Json -Compress | Set-Content -LiteralPath $recPath
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
    if ($r.Rc -ne 0 -or $r.Json.status -ne 'staged' -or (Test-Path -LiteralPath $recPath)) { throw 'a dead recorded pid must not block, and a finished run leaves no record' }
    Set-Content -LiteralPath $recPath -Value 'not json'
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
    Remove-Item -LiteralPath $recPath -ErrorAction SilentlyContinue
    if ($r.Rc -ne 5 -or $r.Calls.Count -ne 0) { throw 'an unreadable operation record must fail closed' }
    $cases++
    # >>case:m
    "passed=$cases failed=0"
} finally {
    Remove-Item -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue
}
