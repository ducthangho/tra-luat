#requires -Version 7.0
# WP710: refresh -> real notebook canary -> stage, serialized on this host. Never prints child output.
# Exit codes: 0 staged; 2 refresh/canary rc != 0 (auth_failure, network_failure or inconclusive);
# 3 timeout; 4 inconclusive (canary body or preflight); 5 inconclusive/lock_busy/tree_quarantine; 6 stage_failure.
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
    [int]$MaxCycles = 1,
    # Bounded exit for an operation record whose process tree cannot be proven gone (see Get-RecordVerdict).
    [int]$UnconfirmedQuarantineSeconds = 900
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

# A child that outlives a killed wrapper keeps running after the OS mutex is released. The wrapper
# records each operation here BEFORE spawning it (marker, then pid + start time) and a new owner waits
# until that operation is gone. Every child gets TRA_LUAT_NLM_OP=<marker> in its environment; descendants
# inherit it, so on Linux the whole tree is found again even after the direct child exited.
$OperationRecord = Join-Path ([IO.Path]::GetTempPath()) 'tra_luat_nlm_credential_refresh.operation.json'
$MarkerName = 'TRA_LUAT_NLM_OP'
$Evidence = [ordered]@{ cycle = 0; profile_fingerprint = ''; cli_version = ''; takeover = 'none'; takeover_reason = '';
    steps = [ordered]@{} }

# WP714 round 3: the ONE place that decides whether this platform can enumerate the operation's process
# tree. Only Linux can (/proc). Everywhere else every "no descendant found" is NOT MEASURED, never "none".
$TreeMeasurable = [bool]$IsLinux
$ProcRoot = '/proc'   # where the operation tree is enumerated (the wrapper's own entry is always /proc/$PID)
$Subreaper = $false
$OwnUid = $null
$OwnerStartJiffies = $null

function Read-ProcStat([string]$dir) {
    # /proc/<pid>/stat -> @{State; Ppid; Start}; $null when the process is gone. Throws when it exists but
    # cannot be read, so the caller counts it as unknown instead of absent.
    try { $text = [IO.File]::ReadAllText("$dir/stat") }
    catch { if ([IO.Directory]::Exists($dir)) { throw } else { return $null } }
    $fields = $text.Substring($text.LastIndexOf(')') + 2).Split(' ')
    # flags & PF_KTHREAD (0x00200000): a kernel thread is never a descendant of a user process.
    return @{ State = $fields[0]; Ppid = [int]$fields[1]; Start = [uint64]$fields[19]
        Kernel = (([uint64]$fields[6] -band 0x00200000) -ne 0) }
}

function Read-ProcUid([string]$dir) {
    try { $text = [IO.File]::ReadAllText("$dir/status") }
    catch { if ([IO.Directory]::Exists($dir)) { throw } else { return $null } }
    $match = [regex]::Match($text, '(?m)^Uid:\s+(\d+)')
    if (-not $match.Success) { throw 'status without Uid' }
    return [int64]$match.Groups[1].Value
}

if ($TreeMeasurable) {
    # A child subreaper adopts every orphan of this wrapper's subtree (a daemon that double-forked, cleared its
    # environment or made itself non-dumpable), so while this wrapper lives its descendants are found by
    # parent links, not only by the inherited marker. Failure leaves the marker scan, with unknowns blocking.
    try {
        Add-Type -Namespace TraLuatWp710 -Name NativeLinux -MemberDefinition '[DllImport("libc", SetLastError = true)] public static extern int prctl(int option, ulong arg2, ulong arg3, ulong arg4, ulong arg5);'
        $Subreaper = ([TraLuatWp710.NativeLinux]::prctl(36, 1, 0, 0, 0) -eq 0)
    } catch { $Subreaper = $false }
    try {
        $OwnUid = Read-ProcUid "/proc/$PID"
        $OwnerStartJiffies = (Read-ProcStat "/proc/$PID").Start
    } catch { $OwnUid = $null; $OwnerStartJiffies = $null }
}

function Emit([string]$status, [string]$step, [int]$rc, [double]$elapsed) {
    # Never emit child stdout/stderr: either stream can include cookies.
    [ordered]@{
        status = $status; step = $step; rc = $rc; elapsed_seconds = $elapsed; cycle = $Evidence.cycle
        profile_fingerprint = $Evidence.profile_fingerprint
        profile_fingerprint_basis = 'sha256 of the lower-cased full browser_profile_path declared in config (first 16 hex)'
        profile_bound_to_cli = $false
        cli_version = $Evidence.cli_version
        tree_measurement = $(if (-not $TreeMeasurable) { 'not_measurable' } elseif ($Subreaper) { 'linux_subreaper_and_marker' } else { 'linux_marker' })
        takeover = $Evidence.takeover; takeover_reason = $Evidence.takeover_reason
        steps = $Evidence.steps
    } | ConvertTo-Json -Compress -Depth 5
}

function Write-Step([string]$name, $result) {
    $Evidence.steps[$name] = [ordered]@{ rc = $result.rc; elapsed_seconds = $result.elapsed
        timeout = $result.timeout; child_confirmed_exited = $result.exited; descendants_stopped = $result.reaped
        tree_state = $result.tree }
}

function Get-StartTicks($process) {
    try { return $process.StartTime.ToUniversalTime().Ticks } catch { return $null }
}

function Get-OperationTree([string]$marker, $floor, [bool]$inRun) {
    # Ids: live processes of the operation (marker in the inherited environment, plus - while this wrapper
    # runs - every descendant by parent link). Unknown: processes that COULD belong to it but whose
    # environment cannot be read (non-dumpable, or a vanished /proc entry that still exists), counted only
    # when they started after $floor and run under this user. Measured=$false: nothing was enumerated.
    $tree = [pscustomobject]@{ Measured = $false; Ids = @(); Unknown = 0 }
    if (-not $TreeMeasurable) { return $tree }
    $haveMarker = $marker -match '^[0-9a-f]{32}$'
    $needle = "`0$MarkerName=$marker`0"
    $children = @{}
    $found = [Collections.Generic.HashSet[int]]::new()
    $unreadable = [Collections.Generic.List[int]]::new()
    foreach ($dir in [IO.Directory]::GetDirectories($ProcRoot)) {
        $name = [IO.Path]::GetFileName($dir)
        if ($name -notmatch '^\d+$' -or [int]$name -eq $PID) { continue }
        $id = [int]$name
        try { $stat = Read-ProcStat $dir } catch { $unreadable.Add($id); continue }
        if ($null -eq $stat -or $stat.State -in @('Z', 'X')) { continue }   # zombies are dead
        if (-not $children.ContainsKey($stat.Ppid)) { $children[$stat.Ppid] = [Collections.Generic.List[int]]::new() }
        $children[$stat.Ppid].Add($id)
        # Init (pid 1) is the ancestor of every process and kernel threads are not user processes: neither can
        # belong to an operation, and both have environments root cannot always read.
        if (-not $haveMarker -or $id -eq 1 -or $stat.Kernel) { continue }
        if ($null -ne $floor -and $stat.Start -lt [uint64]$floor) { continue }   # older than the owner: not ours
        if ($OwnUid -ne 0) {
            try { $uid = Read-ProcUid $dir } catch { $unreadable.Add($id); continue }
            if ($null -eq $uid) { continue }
            if ($null -ne $OwnUid -and $uid -ne $OwnUid) { continue }
        }
        try {
            $environ = "`0" + [Text.Encoding]::Latin1.GetString([IO.File]::ReadAllBytes("$dir/environ"))
            if ($environ.Contains($needle)) { [void]$found.Add($id) }
        } catch {
            if ([IO.Directory]::Exists($dir)) { $unreadable.Add($id) }   # exists but unreadable: UNKNOWN
        }
    }
    if ($inRun) {
        $queue = [Collections.Generic.Queue[int]]::new()
        $queue.Enqueue($PID)
        while ($queue.Count -gt 0) {
            $parent = $queue.Dequeue()
            if (-not $children.ContainsKey($parent)) { continue }
            foreach ($child in $children[$parent]) { [void]$found.Add($child); $queue.Enqueue($child) }
        }
    }
    $tree.Measured = $true
    $tree.Ids = @($found)
    # With the subreaper active every descendant is adopted, so parent links are complete in-run.
    $tree.Unknown = if ($inRun -and $Subreaper) { 0 } else { @($unreadable | Where-Object { -not $found.Contains($_) }).Count }
    return $tree
}

function Stop-OperationTree([string]$marker, [bool]$inRun) {
    # Kill the operation's processes and confirm. State: gone | alive | unknown | not_measurable.
    # Only 'gone' is a proof; the other three keep the operation record.
    $tree = Get-OperationTree $marker $OwnerStartJiffies $inRun
    if (-not $tree.Measured) { return @{ State = 'not_measurable'; Stopped = 0 } }
    $stopped = [Collections.Generic.HashSet[int]]::new()
    $watch = [Diagnostics.Stopwatch]::StartNew()
    while ($tree.Ids.Count -gt 0) {
        foreach ($id in $tree.Ids) { [void]$stopped.Add($id); Stop-Process -Id $id -Force -ErrorAction SilentlyContinue }
        if ($watch.ElapsedMilliseconds -gt 5000) { return @{ State = 'alive'; Stopped = $stopped.Count } }
        Start-Sleep -Milliseconds 50
        $tree = Get-OperationTree $marker $OwnerStartJiffies $inRun
    }
    if ($tree.Unknown -gt 0) { return @{ State = 'unknown'; Stopped = $stopped.Count } }
    return @{ State = 'gone'; Stopped = $stopped.Count }
}

function Write-OperationRecord($marker, $process, [bool]$unconfirmed) {
    $data = [ordered]@{ marker = $marker; pid = $null; start_ticks = $null; tree_unconfirmed = $unconfirmed
        owner_start_jiffies = $OwnerStartJiffies }
    if ($process) { $data.pid = $process.Id; $data.start_ticks = (Get-StartTicks $process) }
    Set-Content -LiteralPath $OperationRecord -Value ($data | ConvertTo-Json -Compress) -Encoding utf8
}

function Test-RecordedRootAlive($record) {
    # $true alive (or not decidable), $false gone or pid reused, $null no pid was ever recorded.
    if ($null -eq $record.pid -or $null -eq $record.start_ticks) { return $null }
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

function Get-RecordVerdict {
    # clear: no record, or Linux proved the old tree gone. alive: the old root or a marked process lives, or
    # the record cannot be read (fail closed; an operator deletes it). quarantine / released: the root is
    # not alive but the tree cannot be proven gone (not Linux, no marker, or unreadable environments). That
    # state is BOUNDED: the first owner that sees it stamps the record, and once -UnconfirmedQuarantineSeconds
    # have passed a takeover is released with takeover=quarantine_elapsed in the evidence. It is not a proof.
    if (-not (Test-Path -LiteralPath $OperationRecord -PathType Leaf)) { return @{ State = 'clear'; Reason = '' } }
    try { $record = [string](Get-Content -LiteralPath $OperationRecord -Raw) | ConvertFrom-Json } catch { $record = $null }
    if ($null -eq $record -or $record -isnot [pscustomobject]) { return @{ State = 'alive'; Reason = 'record_unreadable' } }
    if ((Test-RecordedRootAlive $record) -eq $true) { return @{ State = 'alive'; Reason = 'root_alive' } }
    $reason = 'tree_not_measurable'
    $marker = [string]$record.marker
    if ($marker -match '^[0-9a-f]{32}$') {
        $floor = $null
        if ($record.owner_start_jiffies -is [long] -or $record.owner_start_jiffies -is [int]) { $floor = [uint64]$record.owner_start_jiffies }
        $tree = Get-OperationTree $marker $floor $false
        if ($tree.Measured) {
            if ($tree.Ids.Count -gt 0) { return @{ State = 'alive'; Reason = 'marked_alive' } }
            if ($tree.Unknown -eq 0) { return @{ State = 'clear'; Reason = '' } }
            $reason = 'tree_unknown'
        }
    }
    $now = [DateTime]::UtcNow.Ticks
    $seen = $record.root_dead_seen_utc_ticks
    if ($null -eq $seen) {
        $record | Add-Member -NotePropertyName root_dead_seen_utc_ticks -NotePropertyValue $now -Force
        Set-Content -LiteralPath $OperationRecord -Value ($record | ConvertTo-Json -Compress) -Encoding utf8
        $seen = $now
    }
    if (-not ($seen -is [long] -or $seen -is [int])) { return @{ State = 'alive'; Reason = 'record_unreadable' } }
    $age = $now - [int64]$seen
    if ($age -lt 0) { return @{ State = 'alive'; Reason = 'record_clock' } }
    if ($age -ge [int64]$UnconfirmedQuarantineSeconds * 10000000) { return @{ State = 'released'; Reason = $reason } }
    return @{ State = 'quarantine'; Reason = $reason }
}

function Invoke-Bounded([string]$file, [string[]]$arguments, [int]$seconds, [hashtable]$environment = @{}) {
    $marker = [guid]::NewGuid().ToString('N')
    $info = [System.Diagnostics.ProcessStartInfo]::new()
    $info.FileName = $file
    $info.UseShellExecute = $false
    $info.RedirectStandardOutput = $true
    $info.RedirectStandardError = $true
    foreach ($arg in $arguments) { [void]$info.ArgumentList.Add($arg) }
    foreach ($key in $environment.Keys) { $info.Environment[$key] = [string]$environment[$key] }
    $info.Environment[$MarkerName] = $marker
    $process = [System.Diagnostics.Process]::new()
    $process.StartInfo = $info
    $budget = [int64]$seconds * 1000
    $watch = [System.Diagnostics.Stopwatch]::StartNew()
    $started = $false
    $confirmed = $false
    # Record BEFORE spawning: a wrapper killed between Start() and the pid write leaves the marker behind
    # (Linux finds the tree by marker; elsewhere a record without pid goes to the bounded quarantine).
    Write-OperationRecord $marker $null $false
    try {
        [void]$process.Start()
        $started = $true
        Write-OperationRecord $marker $process $false
        $stdout = $process.StandardOutput.ReadToEndAsync()
        $stderr = $process.StandardError.ReadToEndAsync()
        $done = $process.WaitForExit([int][Math]::Max(0, $budget - $watch.ElapsedMilliseconds))
        # A descendant can keep the redirected pipes open after the CLI exits; the budget covers both.
        if ($done) {
            $done = [Threading.Tasks.Task]::WaitAll([Threading.Tasks.Task[]]@($stdout, $stderr),
                [int][Math]::Max(0, $budget - $watch.ElapsedMilliseconds))
        }
        if (-not $done) {
            # The direct child may have exited while a descendant still holds the pipes: Kill($true) cannot
            # reach an orphan, so the tree sweep does. Asking to kill is not proof of death: confirm the
            # child, the tree and that every pipe writer is gone, or keep the record. A tree that cannot be
            # enumerated (not Linux) or has unreadable members is NOT confirmed.
            try { if (-not $process.HasExited) { $process.Kill($true) } } catch { }
            $rootGone = $false
            try { $rootGone = $process.WaitForExit(5000) } catch { $rootGone = $false }
            $tree = Stop-OperationTree $marker $true
            $pipesClosed = $false
            try { $pipesClosed = [Threading.Tasks.Task]::WaitAll([Threading.Tasks.Task[]]@($stdout, $stderr), 5000) } catch { $pipesClosed = $false }
            $confirmed = $rootGone -and $pipesClosed -and $tree.State -eq 'gone'
            if (-not $confirmed) { Write-OperationRecord $marker $process $true }
            return @{timeout=$true; rc=-1; out=''; err=''; elapsed=$watch.Elapsed.TotalSeconds; exited=$confirmed;
                reaped=$tree.Stopped; tree=$tree.State}
        }
        # Success path: a descendant that dropped the pipes may still run; it is part of this operation and
        # must not overlap the next step, so it is stopped and confirmed first (Linux). Off Linux nothing can
        # be enumerated: the step proceeds and its evidence says tree_state=not_measurable.
        $tree = Stop-OperationTree $marker $true
        if ($tree.State -in @('alive', 'unknown')) {
            Write-OperationRecord $marker $process $true
            return @{timeout=$true; rc=-1; out=''; err=''; elapsed=$watch.Elapsed.TotalSeconds; exited=$false;
                reaped=$tree.Stopped; tree=$tree.State}
        }
        $confirmed = $true
        return @{timeout=$false; rc=$process.ExitCode; out=$stdout.Result; err=$stderr.Result;
            elapsed=$watch.Elapsed.TotalSeconds; exited=$true; reaped=$tree.Stopped; tree=$tree.State}
    } finally {
        if (-not $started -or $confirmed) { Remove-Item -LiteralPath $OperationRecord -ErrorAction SilentlyContinue }
        $process.Dispose()
    }
}

$CanaryKnownKeys = @('id', 'notebook_id', 'title', 'name', 'data', 'ok', 'error')

function Get-CanaryLevel($element) {
    # One object level as an ordinal (case-sensitive) map, or $null: duplicate key, a known key in another
    # case, `ok` present but not true, or `error` present and not null/false/"" make the answer ambiguous.
    if ($element.ValueKind -ne [Text.Json.JsonValueKind]::Object) { return $null }
    $props = [Collections.Generic.Dictionary[string, Text.Json.JsonElement]]::new([StringComparer]::Ordinal)
    foreach ($property in $element.EnumerateObject()) {
        if ($props.ContainsKey($property.Name)) { return $null }
        if ($CanaryKnownKeys -contains $property.Name -and $CanaryKnownKeys -cnotcontains $property.Name) { return $null }
        $props[$property.Name] = $property.Value
    }
    if ($props.ContainsKey('ok') -and $props['ok'].ValueKind -ne [Text.Json.JsonValueKind]::True) { return $null }
    if ($props.ContainsKey('error')) {
        $e = $props['error']
        $empty = $e.ValueKind -in @([Text.Json.JsonValueKind]::Null, [Text.Json.JsonValueKind]::False) -or
            ($e.ValueKind -eq [Text.Json.JsonValueKind]::String -and $e.GetString() -eq '')
        if (-not $empty) { return $null }
    }
    return ,$props
}

function Test-JsonStrictTree($root) {
    # WP714 round 3: the same document contract as tl_gws._nlm_canary_json_strict, over the WHOLE tree, not
    # only the levels the notebook rule reads. Parse already rejects NaN/Infinity, comments, trailing commas,
    # raw control characters, a leading BOM in the string and nesting deeper than 64 (measured, pwsh 7.4.6).
    # It does NOT reject: a duplicate key in nested metadata, a lone escaped surrogate (only reading the
    # string throws) or a number that overflows double (TryGetDouble returns true with +/-Infinity).
    $stack = [Collections.Generic.Stack[Text.Json.JsonElement]]::new()
    $stack.Push($root)
    while ($stack.Count -gt 0) {
        $element = $stack.Pop()
        switch ($element.ValueKind) {
            ([Text.Json.JsonValueKind]::Object) {
                $seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
                foreach ($property in $element.EnumerateObject()) {
                    if (-not $seen.Add($property.Name)) { return $false }
                    $stack.Push($property.Value)
                }
            }
            ([Text.Json.JsonValueKind]::Array) { foreach ($item in $element.EnumerateArray()) { $stack.Push($item) } }
            ([Text.Json.JsonValueKind]::String) { [void]$element.GetString() }
            ([Text.Json.JsonValueKind]::Number) {
                $number = 0.0
                if (-not $element.TryGetDouble([ref]$number) -or -not [double]::IsFinite($number)) { return $false }
            }
        }
    }
    return $true
}

function Test-CanaryBody([string]$text, [string]$notebook) {
    # Allow-list, same rules as tl_gws._nlm_canary_body_ok: exactly ONE notebook object; every id key
    # present is a string equal to the trusted id; every title/name present is a non-blank string.
    # System.Text.Json keeps JSON types and sees duplicate keys (ConvertFrom-Json keeps the last one silently
    # and turns date-like strings into DateTime). Any exception while reading (a lone surrogate in a property
    # name or string throws) is a negative answer, never a positive one.
    try { $doc = [Text.Json.JsonDocument]::Parse($text) } catch { return $false }
    try {
        if (-not (Test-JsonStrictTree $doc.RootElement)) { return $false }
        $node = $doc.RootElement
        if ($node.ValueKind -eq [Text.Json.JsonValueKind]::Array) {
            if ($node.GetArrayLength() -ne 1) { return $false }
            $node = $node[0]
        }
        $props = Get-CanaryLevel $node
        if ($null -eq $props) { return $false }
        if (-not $props.ContainsKey('id') -and -not $props.ContainsKey('notebook_id') -and $props.ContainsKey('data')) {
            $props = Get-CanaryLevel $props['data']
            if ($null -eq $props) { return $false }
        }
        $ids = @(@('id', 'notebook_id') | Where-Object { $props.ContainsKey($_) })
        if ($ids.Count -eq 0) { return $false }
        foreach ($key in $ids) {
            $value = $props[$key]
            if ($value.ValueKind -ne [Text.Json.JsonValueKind]::String -or $value.GetString() -cne $notebook) { return $false }
        }
        $titles = @(@('title', 'name') | Where-Object { $props.ContainsKey($_) })
        if ($titles.Count -eq 0) { return $false }
        foreach ($key in $titles) {
            $value = $props[$key]
            if ($value.ValueKind -ne [Text.Json.JsonValueKind]::String -or [string]::IsNullOrWhiteSpace($value.GetString())) { return $false }
        }
        return $true
    } catch { return $false } finally { $doc.Dispose() }
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
    if ($TimeoutSeconds -lt 1 -or $LockWaitSeconds -lt 0 -or $IntervalSeconds -lt 1 -or $MaxCycles -lt 1 -or
        $UnconfirmedQuarantineSeconds -lt 1) {
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
    # The owner process ending does not end its child: wait for a recorded operation first.
    while ($true) {
        $verdict = Get-RecordVerdict
        if ($verdict.State -eq 'clear') { break }
        if ($verdict.State -eq 'released') {
            $Evidence.takeover = 'quarantine_elapsed'; $Evidence.takeover_reason = $verdict.Reason
            break
        }
        if ([DateTime]::UtcNow -ge $deadline) {
            $Evidence.takeover_reason = $verdict.Reason
            Emit 'inconclusive' $(if ($verdict.State -eq 'quarantine') { 'tree_quarantine' } else { 'lock_busy' }) -1 0
            exit 5
        }
        Start-Sleep -Milliseconds 200
    }
    Remove-Item -LiteralPath $OperationRecord -ErrorAction SilentlyContinue
    $versionResult = Invoke-Bounded $nlmPath ($NlmArgumentsPrefix + @('--version')) $TimeoutSeconds
    Write-Step 'version' $versionResult
    # WP714 round 3: the version probe is an operation like any other. A tree it left unconfirmed keeps the
    # record; starting the refresh would overwrite that record and overlap the old tree.
    if ($versionResult.timeout -and -not $versionResult.exited) { Emit 'timeout' 'version' -1 $versionResult.elapsed; exit 3 }
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
        if (-not (Test-CanaryBody $canary.out $notebook)) {
            Emit 'inconclusive' 'canary' $canary.rc $canary.elapsed
            exit 4
        }
        # The stage command repeats its own canary; give it the same trusted notebook. TL_CANARY_NOTEBOOK_ID
        # is the pin: a profile config loaded by the stage command rewrites TL_NOTEBOOK_ID, never this one.
        $pin = @{ TL_NOTEBOOK_ID = $notebook; TL_CANARY_NOTEBOOK_ID = $notebook }
        try { $stage = Invoke-Bounded $stagePath $StageArguments $TimeoutSeconds $pin }
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
