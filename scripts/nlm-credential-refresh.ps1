#requires -Version 7.0
# WP710: refresh -> real notebook canary -> stage, serialized on this host. Never prints child output.
# Exit codes: 0 staged; 2 refresh/canary rc != 0 (auth_failure, network_failure or inconclusive);
# 3 timeout; 4 inconclusive (canary body or preflight); 5 inconclusive/lock_busy; 6 stage_failure.
param(
    [Parameter(Mandatory=$true)][string]$ConfigPath,
    [string]$NlmCommand = 'nlm',
    [string[]]$NlmArgumentsPrefix = @(),
    [string]$StageCommand = 'python',
    [string[]]$StageArguments = @((Join-Path $PSScriptRoot 'tl.py'), 'nlm-auth-stage'),
    [int]$TimeoutSeconds = 120,
    [int]$LockWaitSeconds = 10,
    [switch]$EnableKeepalive,
    [int]$IntervalSeconds = 3600,
    [int]$MaxCycles = 1
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

# A child that outlives a killed wrapper keeps running after the OS mutex is released. The wrapper
# records each running child (pid + start time) here and a new owner waits until that child is gone.
$OperationRecord = Join-Path ([IO.Path]::GetTempPath()) 'tra_luat_nlm_credential_refresh.operation.json'
$Evidence = [ordered]@{ cycle = 0; profile_fingerprint = ''; cli_version = ''; steps = [ordered]@{} }

function Emit([string]$status, [string]$step, [int]$rc, [double]$elapsed) {
    # Never emit child stdout/stderr: either stream can include cookies.
    [ordered]@{
        status = $status; step = $step; rc = $rc; elapsed_seconds = $elapsed; cycle = $Evidence.cycle
        profile_fingerprint = $Evidence.profile_fingerprint
        profile_fingerprint_basis = 'sha256 of the lower-cased full browser_profile_path declared in config (first 16 hex)'
        profile_bound_to_cli = $false
        cli_version = $Evidence.cli_version
        steps = $Evidence.steps
    } | ConvertTo-Json -Compress -Depth 5
}

function Write-Step([string]$name, $result) {
    $Evidence.steps[$name] = [ordered]@{ rc = $result.rc; elapsed_seconds = $result.elapsed
        timeout = $result.timeout; child_confirmed_exited = $result.exited }
}

function Get-StartTicks($process) {
    try { return $process.StartTime.ToUniversalTime().Ticks } catch { return $null }
}

function Test-RecordedChildAlive {
    if (-not (Test-Path -LiteralPath $OperationRecord -PathType Leaf)) { return $false }
    # An unreadable record fails closed: an operator must confirm no child is left, then delete it.
    try { $record = [string](Get-Content -LiteralPath $OperationRecord -Raw) | ConvertFrom-Json } catch { return $true }
    if ($null -eq $record -or $null -eq $record.pid -or $null -eq $record.start_ticks) { return $true }
    $process = Get-Process -Id ([int]$record.pid) -ErrorAction SilentlyContinue
    if (-not $process) { return $false }
    $ticks = Get-StartTicks $process
    if ($null -eq $ticks) { return $true }
    # A different start time is pid reuse, not the recorded child.
    if ([math]::Abs([int64]$ticks - [int64]$record.start_ticks) -gt 10000000) { return $false }
    if ($IsLinux) {
        try { if ([IO.File]::ReadAllText("/proc/$([int]$record.pid)/stat") -match '\)\s+Z\s') { return $false } } catch { }
    }
    return $true
}

function Invoke-Bounded([string]$file, [string[]]$arguments, [int]$seconds, [hashtable]$environment = @{}) {
    $info = [System.Diagnostics.ProcessStartInfo]::new()
    $info.FileName = $file
    $info.UseShellExecute = $false
    $info.RedirectStandardOutput = $true
    $info.RedirectStandardError = $true
    foreach ($arg in $arguments) { [void]$info.ArgumentList.Add($arg) }
    foreach ($key in $environment.Keys) { $info.Environment[$key] = [string]$environment[$key] }
    $process = [System.Diagnostics.Process]::new()
    $process.StartInfo = $info
    $budget = [int64]$seconds * 1000
    $watch = [System.Diagnostics.Stopwatch]::StartNew()
    $started = $false
    $exited = $false
    try {
        [void]$process.Start()
        $started = $true
        $record = [ordered]@{ pid = $process.Id; start_ticks = (Get-StartTicks $process) } | ConvertTo-Json -Compress
        Set-Content -LiteralPath $OperationRecord -Value $record -Encoding utf8
        $stdout = $process.StandardOutput.ReadToEndAsync()
        $stderr = $process.StandardError.ReadToEndAsync()
        $done = $process.WaitForExit([int][Math]::Max(0, $budget - $watch.ElapsedMilliseconds))
        # A descendant can keep the redirected pipes open after the CLI exits; the budget covers both.
        if ($done) {
            $done = [Threading.Tasks.Task]::WaitAll([Threading.Tasks.Task[]]@($stdout, $stderr),
                [int][Math]::Max(0, $budget - $watch.ElapsedMilliseconds))
        }
        if (-not $done) {
            try { if (-not $process.HasExited) { $process.Kill($true) } } catch { }
            # Asking to kill is not proof of death: confirm, or keep the record so the next owner waits.
            try { $exited = $process.WaitForExit(5000) } catch { $exited = $false }
            return @{timeout=$true; rc=-1; out=''; err=''; elapsed=$watch.Elapsed.TotalSeconds; exited=$exited}
        }
        $exited = $true
        return @{timeout=$false; rc=$process.ExitCode; out=$stdout.Result; err=$stderr.Result;
            elapsed=$watch.Elapsed.TotalSeconds; exited=$true}
    } finally {
        if ($started -and $exited) { Remove-Item -LiteralPath $OperationRecord -ErrorAction SilentlyContinue }
        $process.Dispose()
    }
}

function Classify([string]$message) {
    # Bare words are not evidence: `nlm auth refresh`, `nlm login` and .../nlm/auth/refresh.py all
    # contain auth words. Only anchored failure phrases count (allow-list); a mixed or unknown signal
    # stays inconclusive. Any non-zero rc still makes zero stage calls whatever the label.
    $auth = $message -match '(?i)\bauth(?:entication)?\s+(?:has\s+)?(?:expired|failed|required|invalid)\b|\bunauthori[sz]ed\b|\bHTTP\s*40[13]\b|\b40[13]\s+(?:Unauthorized|Forbidden)\b|\bClientAuthenticationError\b|\b(?:session|cookies?)\s+(?:has\s+|have\s+)?(?:expired|invalid)\b'
    $network = $message -match '(?i)\bnetwork\s+(?:failure|error|(?:is\s+)?unreachable)\b|\bconnection\s+(?:reset|refused|aborted|timed\s+out)\b|\bname\s+resolution\b|\bgetaddrinfo\b|\bno\s+route\s+to\s+host\b|\bHTTP\s*50[234]\b|\b50[234]\s+(?:Bad\s+Gateway|Service\s+Unavailable|Gateway\s+Time-?out)\b|\bConnectionError\b'
    if ($auth -and -not $network) { return 'auth_failure' }
    if ($network -and -not $auth) { return 'network_failure' }
    return 'inconclusive'
}

$mutex = $null
$held = $false
try {
    if ($TimeoutSeconds -lt 1 -or $LockWaitSeconds -lt 0 -or $IntervalSeconds -lt 1 -or $MaxCycles -lt 1) {
        throw 'invalid bounded timing parameters'
    }
    $configFull = [IO.Path]::GetFullPath($ConfigPath)
    $config = [string](Get-Content -LiteralPath $configFull -Raw) | ConvertFrom-Json
    $notebook = [string]$config.notebook_id
    $browserProfile = [string]$config.browser_profile_path
    if ($notebook -cnotmatch '^[A-Za-z0-9_-]{8,128}$') { throw 'trusted config lacks valid notebook_id' }
    if (-not $browserProfile -or -not (Test-Path -LiteralPath $browserProfile -PathType Container)) { throw 'original browser profile missing' }
    $profileFull = [IO.Path]::GetFullPath($browserProfile)
    $digest = [Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes($profileFull.ToLowerInvariant()))
    $Evidence.profile_fingerprint = [Convert]::ToHexString($digest).Substring(0, 16)
    # Resolve to a real application path: a bare name does not find a .cmd shim through Process.Start.
    $nlmPath = (Get-Command -Name $NlmCommand -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source
    $stagePath = (Get-Command -Name $StageCommand -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source
    $deadline = [DateTime]::UtcNow.AddSeconds($LockWaitSeconds)
    # One lock for every config on this interactive host, including distinct config paths.
    $mutex = [Threading.Mutex]::new($false, 'Global\tra_luat_nlm_credential_refresh')
    try { $held = $mutex.WaitOne([TimeSpan]::FromSeconds($LockWaitSeconds)) }
    catch [Threading.AbandonedMutexException] { $held = $true } # The OS reports the prior owner process ended.
    if (-not $held) { Emit 'inconclusive' 'lock_busy' -1 0; exit 5 }
    # The owner process ending does not end its child: wait for a recorded child first.
    while (Test-RecordedChildAlive) {
        if ([DateTime]::UtcNow -ge $deadline) { Emit 'inconclusive' 'lock_busy' -1 0; exit 5 }
        Start-Sleep -Milliseconds 200
    }
    Remove-Item -LiteralPath $OperationRecord -ErrorAction SilentlyContinue
    $versionResult = Invoke-Bounded $nlmPath ($NlmArgumentsPrefix + @('--version')) $TimeoutSeconds
    Write-Step 'version' $versionResult
    $versionMatch = [regex]::Match($versionResult.out, '\b\d+\.\d+(?:\.\d+)?\b')
    $Evidence.cli_version = if ($versionResult.rc -eq 0 -and -not $versionResult.timeout -and $versionMatch.Success) {
        $versionMatch.Value
    } else { 'unavailable' }
    for ($cycle=0; $cycle -lt $MaxCycles; $cycle++) {
        # The lock is held through the keepalive interval as well: a manual run then sees lock_busy.
        if ($cycle -gt 0) { Start-Sleep -Seconds $IntervalSeconds }
        $Evidence.cycle = $cycle + 1
        foreach ($name in @('refresh', 'canary', 'stage')) { [void]$Evidence.steps.Remove($name) }
        $refresh = Invoke-Bounded $nlmPath ($NlmArgumentsPrefix + @('auth','refresh')) $TimeoutSeconds
        Write-Step 'refresh' $refresh
        if ($refresh.timeout) { Emit 'timeout' 'refresh' -1 $refresh.elapsed; exit 3 }
        if ($refresh.rc -ne 0) {
            Emit (Classify ($refresh.err + ' ' + $refresh.out)) 'refresh' $refresh.rc $refresh.elapsed
            exit 2
        }
        $canary = Invoke-Bounded $nlmPath ($NlmArgumentsPrefix + @('notebook','get',$notebook,'-j')) $TimeoutSeconds
        Write-Step 'canary' $canary
        if ($canary.timeout) { Emit 'timeout' 'canary' -1 $canary.elapsed; exit 3 }
        if ($canary.rc -ne 0) {
            Emit (Classify ($canary.err + ' ' + $canary.out)) 'canary' $canary.rc $canary.elapsed
            exit 2
        }
        try {
            $body = $canary.out | ConvertFrom-Json
            if ($body -is [array]) { if ($body.Count -ne 1) { throw 'ambiguous array' }; $body = $body[0] }
            if ($body.data) { $body = $body.data }
            if ([string]$body.id -cne $notebook -and [string]$body.notebook_id -cne $notebook) { throw 'id mismatch' }
            if (-not $body.title -and -not $body.name) { throw 'missing notebook body' }
        } catch {
            Emit 'inconclusive' 'canary' $canary.rc $canary.elapsed
            exit 4
        }
        # The stage command repeats its own canary; give it the same trusted notebook.
        try { $stage = Invoke-Bounded $stagePath $StageArguments $TimeoutSeconds @{ TL_NOTEBOOK_ID = $notebook } }
        catch { Emit 'stage_failure' 'stage' -1 0; exit 6 }
        Write-Step 'stage' $stage
        if ($stage.timeout -or $stage.rc -ne 0) {
            Emit 'stage_failure' 'stage' $stage.rc $stage.elapsed
            exit 6
        }
        Emit 'staged' 'stage' $stage.rc $stage.elapsed
        if (-not $EnableKeepalive) { break }
    }
} catch {
    Emit 'inconclusive' 'preflight' -1 0
    exit 4
} finally {
    if ($held) { $mutex.ReleaseMutex() }
    if ($mutex) { $mutex.Dispose() }
}
