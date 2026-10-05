param(
    [Parameter(Mandatory=$true)][string]$ConfigPath,
    [string]$NlmCommand = 'nlm',
    [string[]]$NlmArgumentsPrefix = @(),
    [string]$StageCommand = 'python',
    [string[]]$StageArguments = @('scripts/tl.py', 'nlm-auth-stage'),
    [int]$TimeoutSeconds = 120,
    [int]$LockWaitSeconds = 10,
    [switch]$EnableKeepalive,
    [int]$IntervalSeconds = 3600,
    [int]$MaxCycles = 1
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

function Emit([string]$status, [string]$step, [int]$rc, [double]$elapsed, [string]$profileHash, [string]$version) {
    # Never emit child stdout/stderr: either stream can include cookies.
    [pscustomobject]@{status=$status; step=$step; rc=$rc; elapsed_seconds=$elapsed;
        profile_fingerprint=$profileHash; cli_version=$version} | ConvertTo-Json -Compress
}

function Invoke-Bounded([string]$file, [string[]]$arguments, [int]$seconds) {
    $info = [System.Diagnostics.ProcessStartInfo]::new()
    $info.FileName = $file
    $info.UseShellExecute = $false
    $info.RedirectStandardOutput = $true
    $info.RedirectStandardError = $true
    foreach ($arg in $arguments) { [void]$info.ArgumentList.Add($arg) }
    $process = [System.Diagnostics.Process]::new()
    $process.StartInfo = $info
    $watch = [System.Diagnostics.Stopwatch]::StartNew()
    try {
        [void]$process.Start()
        $stdout = $process.StandardOutput.ReadToEndAsync()
        $stderr = $process.StandardError.ReadToEndAsync()
        if (-not $process.WaitForExit($seconds * 1000)) {
            $process.Kill($true)
            $process.WaitForExit()
            return @{timeout=$true; rc=-1; out=''; err=''; elapsed=$watch.Elapsed.TotalSeconds}
        }
        return @{timeout=$false; rc=$process.ExitCode; out=$stdout.GetAwaiter().GetResult();
            err=$stderr.GetAwaiter().GetResult(); elapsed=$watch.Elapsed.TotalSeconds}
    } finally { $process.Dispose() }
}

function Classify([string]$message) {
    if ($message -match '(?i)auth|expired|unauthori[sz]ed|forbidden|login|cookie') { return 'auth_failure' }
    if ($message -match '(?i)network|connection|dns|socket|reach|offline|503|502') { return 'network_failure' }
    return 'inconclusive'
}

$mutex = $null
$held = $false
try {
    if ($TimeoutSeconds -lt 1 -or $LockWaitSeconds -lt 0 -or $IntervalSeconds -lt 1 -or $MaxCycles -lt 1) {
        throw 'invalid bounded timing parameters'
    }
    $configFull = [IO.Path]::GetFullPath($ConfigPath)
    $config = Get-Content -LiteralPath $configFull -Raw | ConvertFrom-Json
    $notebook = [string]$config.notebook_id
    $profile = [string]$config.browser_profile_path
    if ($notebook -notmatch '^[A-Za-z0-9_-]{8,128}$') { throw 'trusted config lacks valid notebook_id' }
    if (-not $profile -or -not (Test-Path -LiteralPath $profile -PathType Container)) { throw 'original browser profile missing' }
    $profileFull = [IO.Path]::GetFullPath($profile)
    $digest = [Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes($profileFull.ToLowerInvariant()))
    $profileHash = [Convert]::ToHexString($digest).Substring(0, 16)
    # One lock for every config on this interactive host, including distinct config paths.
    $mutex = [Threading.Mutex]::new($false, 'Global\tra_luat_nlm_credential_refresh')
    try { $held = $mutex.WaitOne([TimeSpan]::FromSeconds($LockWaitSeconds)) }
    catch [Threading.AbandonedMutexException] { $held = $true } # OS proves prior owner process ended.
    if (-not $held) { Emit 'inconclusive' 'lock_busy' -1 0 $profileHash '' ; exit 5 }
    $versionResult = Invoke-Bounded $NlmCommand ($NlmArgumentsPrefix + @('--version')) $TimeoutSeconds
    $versionMatch = [regex]::Match($versionResult.out, '\b\d+\.\d+(?:\.\d+)?\b')
    $version = if ($versionResult.rc -eq 0 -and -not $versionResult.timeout -and $versionMatch.Success) {
        $versionMatch.Value
    } else { 'unavailable' }
    for ($cycle=0; $cycle -lt $MaxCycles; $cycle++) {
        if ($cycle -gt 0) { Start-Sleep -Seconds $IntervalSeconds }
        $refresh = Invoke-Bounded $NlmCommand ($NlmArgumentsPrefix + @('auth','refresh')) $TimeoutSeconds
        if ($refresh.timeout) { Emit 'timeout' 'refresh' -1 $refresh.elapsed $profileHash $version; exit 3 }
        if ($refresh.rc -ne 0) {
            Emit (Classify ($refresh.err + ' ' + $refresh.out)) 'refresh' $refresh.rc $refresh.elapsed $profileHash $version
            exit 2
        }
        $canary = Invoke-Bounded $NlmCommand ($NlmArgumentsPrefix + @('notebook','get',$notebook,'-j')) $TimeoutSeconds
        if ($canary.timeout) { Emit 'timeout' 'canary' -1 $canary.elapsed $profileHash $version; exit 3 }
        if ($canary.rc -ne 0) {
            Emit (Classify ($canary.err + ' ' + $canary.out)) 'canary' $canary.rc $canary.elapsed $profileHash $version
            exit 2
        }
        try {
            $body = $canary.out | ConvertFrom-Json
            if ($body -is [array]) { if ($body.Count -ne 1) { throw 'ambiguous array' }; $body = $body[0] }
            if ($body.data) { $body = $body.data }
            if ([string]$body.id -ne $notebook -and [string]$body.notebook_id -ne $notebook) { throw 'id mismatch' }
            if (-not $body.title -and -not $body.name) { throw 'missing notebook body' }
        } catch {
            Emit 'inconclusive' 'canary' $canary.rc $canary.elapsed $profileHash $version
            exit 4
        }
        try { $stage = Invoke-Bounded $StageCommand $StageArguments $TimeoutSeconds }
        catch { Emit 'stage_failure' 'stage' -1 0 $profileHash $version; exit 6 }
        if ($stage.timeout -or $stage.rc -ne 0) {
            Emit 'stage_failure' 'stage' $stage.rc $stage.elapsed $profileHash $version
            exit 6
        }
        Emit 'staged' 'stage' $stage.rc $stage.elapsed $profileHash $version
        if (-not $EnableKeepalive) { break }
    }
} catch {
    Emit 'inconclusive' 'preflight' -1 0 '' ''
    exit 4
} finally {
    if ($held) { $mutex.ReleaseMutex() }
    if ($mutex) { $mutex.Dispose() }
}
