$ErrorActionPreference = 'Stop'
$root = Join-Path ([IO.Path]::GetTempPath()) ('wp710-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $root | Out-Null
$script = Join-Path $PSScriptRoot 'nlm-credential-refresh.ps1'
$cases = 0
try {
    $source = @'
import json, os, sys, time
op = sys.argv[1] if len(sys.argv) > 1 else "stage"
if op == "--version":
    print("fake-nlm 1.0")
    sys.exit(0)
with open(os.environ["WP710_LOG"], "a", encoding="utf-8") as log:
    log.write(f"start:{op}:{os.getpid()}\n")
time.sleep(int(os.environ.get("WP710_DELAY", "0")) / 1000)
mode = os.environ.get("WP710_MODE", "ok")
if mode == "timeout" and op == "auth":
    time.sleep(5)
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
    else:
        print(json.dumps({"id": "WRONG12345" if mode == "wrong" else sys.argv[3], "title": "Test"}))
with open(os.environ["WP710_LOG"], "a", encoding="utf-8") as log:
    log.write(f"end:{op}:{os.getpid()}\n")
'@
    $fake = Join-Path $root 'fake.py'
    Set-Content -LiteralPath $fake -Value $source -Encoding utf8
    $python = (Get-Command python).Source
    $profile = Join-Path $root 'profile'
    New-Item -ItemType Directory -Path $profile | Out-Null
    $config = Join-Path $root 'config.json'
    @{notebook_id='NOTEBOOK12345';browser_profile_path=$profile} | ConvertTo-Json | Set-Content -LiteralPath $config
    $env:WP710_LOG = Join-Path $root 'calls.log'
    foreach ($mode in @('ok','auth','network','timeout','wrong','empty','stage')) {
        $env:WP710_MODE = $mode
        Remove-Item -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue
        $args = @('-NoProfile','-File',$script,'-ConfigPath',$config,'-NlmCommand',$python,
                  '-NlmArgumentsPrefix',$fake,'-StageCommand',$python,
                  '-StageArguments',$fake,'-TimeoutSeconds','1')
        $output = & pwsh @args
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
    $one = Start-Process -FilePath $powershell -ArgumentList $argline -PassThru -WindowStyle Hidden -RedirectStandardOutput (Join-Path $root 'one.out')
    $two = Start-Process -FilePath $powershell -ArgumentList $argline -PassThru -WindowStyle Hidden -RedirectStandardOutput (Join-Path $root 'two.out')
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
    $owner = Start-Process -FilePath $powershell -ArgumentList ('-NoProfile -File "' + $ownerScript + '" -Name "' + $lockName + '" -Ready "' + $ready + '"') -PassThru -WindowStyle Hidden
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
    "passed=$cases failed=0"
} finally {
    Remove-Item -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue
}
