[CmdletBinding()]
param(
    [ValidateSet('ready', 'paused', 'prereq', 'create', 'prompts', 'all')]
    [string]$Case = 'all'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptPath = [System.IO.Path]::GetFullPath(
    (Join-Path $PSScriptRoot '..\New-SharedWorkPacket.ps1')
)
$PowerShellPath = (Get-Process -Id $PID).Path

function Assert-Contains {
    param(
        [Parameter(Mandatory)]
        [string]$Text,

        [Parameter(Mandatory)]
        [string]$Expected
    )

    if ($Text.IndexOf($Expected, [System.StringComparison]::Ordinal) -lt 0) {
        throw "Expected generated packet to contain: $Expected"
    }
}

function Invoke-SnapshotPreview {
    param(
        [Parameter(Mandatory)]
        [System.Collections.IDictionary]$Snapshot,

        [Parameter(Mandatory)]
        [string]$Name
    )

    $Suffix = [Guid]::NewGuid().ToString('N')
    $SnapshotPath = Join-Path ([System.IO.Path]::GetTempPath()) "wp-$Name-$Suffix.json"
    $BodyPath = Join-Path ([System.IO.Path]::GetTempPath()) "wp-$Name-$Suffix.md"
    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    $SnapshotJson = $Snapshot | ConvertTo-Json -Depth 5
    [System.IO.File]::WriteAllText($SnapshotPath, $SnapshotJson, $Utf8NoBom)

    try {
        $Output = ((& $PowerShellPath -NoProfile -File $ScriptPath `
            -SnapshotPath $SnapshotPath `
            -DryRun `
            -BodyOutputPath $BodyPath) | Out-String).Trim()
        $ExitCode = $LASTEXITCODE

        if ($ExitCode -ne 0) {
            throw "Packet CLI failed with exit code $ExitCode. Output: $Output"
        }
        if (-not (Test-Path -LiteralPath $BodyPath -PathType Leaf)) {
            throw 'Packet CLI did not create the requested Markdown body file.'
        }

        return [System.IO.File]::ReadAllText($BodyPath)
    }
    finally {
        Remove-Item -LiteralPath $SnapshotPath -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath $BodyPath -Force -ErrorAction SilentlyContinue
    }
}

function Invoke-ReadyPacketTest {
    $Body = Invoke-SnapshotPreview -Name 'ready' -Snapshot ([ordered]@{
        repo_slug   = 'example/tra-luat'
        base_sha    = '0123456789abcdef0123456789abcdef01234567'
        version     = '1.36.59'
        observed_at = '2026-08-03T12:00:00+07:00'
        open_prs    = @()
    })

    Assert-Contains -Text $Body -Expected '# Work packet: wp-d0-protocol-constitution'
    Assert-Contains -Text $Body -Expected '- Status: ready_for_claim'
    Assert-Contains -Text $Body -Expected '- Planned executor: codex'
    Assert-Contains -Text $Body -Expected '- Cross-provider reviewer: claude'
    Assert-Contains -Text $Body -Expected '- base_sha: 0123456789abcdef0123456789abcdef01234567'
    Assert-Contains -Text $Body -Expected '- Không có PR mở tại thời điểm quan sát.'
    Assert-Contains -Text $Body -Expected 'docs/prompts/CODEX_EXECUTOR_D0.md'
    Assert-Contains -Text $Body -Expected 'Không sửa `VERSION` hoặc cấp số `rNNN`/version mới.'
    Assert-Contains -Text $Body -Expected 'packet protocol-v1 lease/start'
    Assert-Contains -Text $Body -Expected 'text file thuộc policy đang mang CRLF'
    Assert-Contains -Text $Body -Expected 'REVIEW_READY'
    Assert-Contains -Text $Body -Expected '`cross_approved`'
    Assert-Contains -Text $Body -Expected '`review_deferred`'
}

function Invoke-PausedPacketTest {
    $Body = Invoke-SnapshotPreview -Name 'paused' -Snapshot ([ordered]@{
        repo_slug   = 'example/tra-luat'
        base_sha    = 'fedcba9876543210fedcba9876543210fedcba98'
        version     = '1.36.60'
        observed_at = '2026-08-03T12:30:00+07:00'
        open_prs    = @(
            [ordered]@{
                number      = 42
                title       = 'Concurrent writer'
                headRefName = 'agent/wp42-g1-claude'
                url         = 'https://github.com/example/tra-luat/pull/42'
            }
        )
    })

    Assert-Contains -Text $Body -Expected '- Status: PAUSE_OPEN_PR'
    Assert-Contains -Text $Body -Expected '- open_pr_count: 1'
    Assert-Contains -Text $Body -Expected '#42 — Concurrent writer — branch: agent/wp42-g1-claude'
    Assert-Contains -Text $Body -Expected 'https://github.com/example/tra-luat/pull/42'
}

function Invoke-PromptContractTest {
    $PromptRoot = [System.IO.Path]::GetFullPath(
        (Join-Path $PSScriptRoot '..\..\prompts')
    )
    $CodexPromptPath = Join-Path $PromptRoot 'CODEX_EXECUTOR_D0.md'
    $ClaudePromptPath = Join-Path $PromptRoot 'CLAUDE_REVIEWER_D0.md'

    if (-not (Test-Path -LiteralPath $CodexPromptPath -PathType Leaf)) {
        throw "Missing Codex prompt: $CodexPromptPath"
    }
    if (-not (Test-Path -LiteralPath $ClaudePromptPath -PathType Leaf)) {
        throw "Missing Claude prompt: $ClaudePromptPath"
    }

    $CodexPrompt = [System.IO.File]::ReadAllText($CodexPromptPath)
    $ClaudePrompt = [System.IO.File]::ReadAllText($ClaudePromptPath)

    Assert-Contains -Text $CodexPrompt -Expected '{{ISSUE_URL}}'
    Assert-Contains -Text $CodexPrompt -Expected '{{BASE_SHA}}'
    Assert-Contains -Text $CodexPrompt -Expected 'executor duy nhất'
    Assert-Contains -Text $CodexPrompt -Expected 'REVIEW_READY'
    Assert-Contains -Text $CodexPrompt -Expected 'Không merge hoặc deploy'

    Assert-Contains -Text $ClaudePrompt -Expected '{{ISSUE_URL}}'
    Assert-Contains -Text $ClaudePrompt -Expected '{{BASE_SHA}}'
    Assert-Contains -Text $ClaudePrompt -Expected '{{HEAD_SHA}}'
    Assert-Contains -Text $ClaudePrompt -Expected 'read-only'
    Assert-Contains -Text $ClaudePrompt -Expected 'Không Edit/Write/commit/push/merge/deploy'
    Assert-Contains -Text $ClaudePrompt -Expected 'cross_approved'
    Assert-Contains -Text $ClaudePrompt -Expected 'review_deferred'
}

function Invoke-MissingToolTest {
    $RepoRoot = [System.IO.Path]::GetFullPath(
        (Join-Path $PSScriptRoot '..\..\..')
    )
    $BodyPath = Join-Path ([System.IO.Path]::GetTempPath()) (
        'wp-missing-tool-' + [Guid]::NewGuid().ToString('N') + '.md'
    )
    $OriginalPath = $env:PATH
    $OriginalErrorActionPreference = $ErrorActionPreference

    try {
        $env:PATH = ''
        $ErrorActionPreference = 'Continue'
        $Output = ((& $PowerShellPath -NoProfile -File $ScriptPath `
            -RepoPath $RepoRoot `
            -DryRun `
            -BodyOutputPath $BodyPath 2>&1) | Out-String).Trim()
        $ExitCode = $LASTEXITCODE

        if ($ExitCode -eq 0) {
            throw 'Live preflight unexpectedly succeeded without git or gh in PATH.'
        }
        Assert-Contains -Text $Output -Expected 'git'
        Assert-Contains -Text $Output -Expected 'PATH'
        if (Test-Path -LiteralPath $BodyPath) {
            throw 'Failed preflight must not leave a generated packet body.'
        }
    }
    finally {
        $env:PATH = $OriginalPath
        $ErrorActionPreference = $OriginalErrorActionPreference
        Remove-Item -LiteralPath $BodyPath -Force -ErrorAction SilentlyContinue
    }
}

function Invoke-IssueCreationTest {
    $RepoRoot = [System.IO.Path]::GetFullPath(
        (Join-Path $PSScriptRoot '..\..\..')
    )
    $Suffix = [Guid]::NewGuid().ToString('N')
    $ShimRoot = Join-Path ([System.IO.Path]::GetTempPath()) "wp-shims-$Suffix"
    $GitShim = Join-Path $ShimRoot 'git.cmd'
    $GhShim = Join-Path $ShimRoot 'gh.cmd'
    $GhLogPath = Join-Path $ShimRoot 'gh-calls.log'
    $WrapperPath = Join-Path $ShimRoot 'invoke-with-clipboard-guard.ps1'
    $BodyPath = Join-Path ([System.IO.Path]::GetTempPath()) "wp-create-$Suffix.md"
    $OriginalPath = $env:PATH
    $OriginalGhLog = $env:WP_GH_LOG
    $OriginalScriptUnderTest = $env:WP_SCRIPT_UNDER_TEST
    $OriginalRepoUnderTest = $env:WP_REPO_UNDER_TEST
    $OriginalBodyUnderTest = $env:WP_BODY_UNDER_TEST
    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

    [void](New-Item -ItemType Directory -Path $ShimRoot)
    $GitShimBody = @(
        '@echo off',
        'if "%~3"=="rev-parse" if "%~4"=="--show-toplevel" (echo D:\repo& exit /b 0)',
        'if "%~3"=="fetch" exit /b 0',
        'if "%~3"=="rev-parse" if "%~4"=="origin/master" (echo 1111111111111111111111111111111111111111& exit /b 0)',
        'if "%~3"=="show" (echo 1.36.59& exit /b 0)',
        'exit /b 9'
    ) -join [Environment]::NewLine
    $GhShimBody = @(
        '@echo off',
        'echo %*>>"%WP_GH_LOG%"',
        'if "%~1"=="auth" exit /b 0',
        'if "%~1"=="repo" (echo {"nameWithOwner":"example/tra-luat"}& exit /b 0)',
        'if "%~1"=="pr" (echo []& exit /b 0)',
        'if "%~1"=="issue" (echo https://github.com/example/tra-luat/issues/77& exit /b 0)',
        'exit /b 9'
    ) -join [Environment]::NewLine
    [System.IO.File]::WriteAllText($GitShim, $GitShimBody, $Utf8NoBom)
    [System.IO.File]::WriteAllText($GhShim, $GhShimBody, $Utf8NoBom)
    $WrapperBody = @(
        '$ErrorActionPreference = ''Stop''',
        'function Set-Clipboard { throw ''CLIPBOARD_CALLED'' }',
        '& $env:WP_SCRIPT_UNDER_TEST -RepoPath $env:WP_REPO_UNDER_TEST -BodyOutputPath $env:WP_BODY_UNDER_TEST -NoClipboard'
    ) -join [Environment]::NewLine
    [System.IO.File]::WriteAllText($WrapperPath, $WrapperBody, $Utf8NoBom)

    try {
        $env:PATH = "$ShimRoot;$env:SystemRoot\System32"
        $env:WP_GH_LOG = $GhLogPath
        $env:WP_SCRIPT_UNDER_TEST = $ScriptPath
        $env:WP_REPO_UNDER_TEST = $RepoRoot
        $env:WP_BODY_UNDER_TEST = $BodyPath
        $Output = ((& $PowerShellPath -NoProfile -File $WrapperPath 2>&1) | Out-String).Trim()
        $ExitCode = $LASTEXITCODE

        if ($ExitCode -ne 0) {
            throw "Issue creation flow failed with exit code $ExitCode. Output: $Output"
        }

        $Summary = $Output | ConvertFrom-Json
        if ($Summary.issue_url -ne 'https://github.com/example/tra-luat/issues/77') {
            throw "Unexpected issue URL: $($Summary.issue_url)"
        }
        if ($Summary.status -ne 'ready_for_claim' -or $Summary.dry_run) {
            throw "Unexpected creation summary: $Output"
        }
        if (-not (Test-Path -LiteralPath $BodyPath -PathType Leaf)) {
            throw 'Successful issue creation must retain the exact submitted body.'
        }

        if (-not (Test-Path -LiteralPath $GhLogPath -PathType Leaf)) {
            throw 'The gh boundary did not produce an invocation log.'
        }
        $IssueCalls = @(
            [System.IO.File]::ReadAllLines($GhLogPath) |
            Where-Object { $_.StartsWith('issue create ', [System.StringComparison]::Ordinal) }
        )
        if ($IssueCalls.Count -ne 1) {
            throw "Expected exactly one gh issue create call, observed $($IssueCalls.Count)."
        }
        Assert-Contains -Text $IssueCalls[0] -Expected '--repo example/tra-luat'
        Assert-Contains -Text $IssueCalls[0] -Expected '--title'
        Assert-Contains -Text $IssueCalls[0] -Expected '[WP D0] Land'
        Assert-Contains -Text $IssueCalls[0] -Expected "--body-file $BodyPath"
    }
    finally {
        $env:PATH = $OriginalPath
        $env:WP_GH_LOG = $OriginalGhLog
        $env:WP_SCRIPT_UNDER_TEST = $OriginalScriptUnderTest
        $env:WP_REPO_UNDER_TEST = $OriginalRepoUnderTest
        $env:WP_BODY_UNDER_TEST = $OriginalBodyUnderTest
        Remove-Item -LiteralPath $BodyPath -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath $GitShim -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath $GhShim -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath $GhLogPath -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath $WrapperPath -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath $ShimRoot -Force -ErrorAction SilentlyContinue
    }
}

$PassedCases = [System.Collections.Generic.List[string]]::new()

if ($Case -in @('ready', 'all')) {
    Invoke-ReadyPacketTest
    Write-Output 'PASS: zero open PR generates a ready work packet'
    [void]$PassedCases.Add('ready')
}

if ($Case -in @('paused', 'all')) {
    Invoke-PausedPacketTest
    Write-Output 'PASS: open PR generates a paused work packet'
    [void]$PassedCases.Add('paused')
}

if ($Case -in @('prereq', 'all')) {
    Invoke-MissingToolTest
    Write-Output 'PASS: live preflight fails closed when required tools are missing'
    [void]$PassedCases.Add('prereq')
}

if ($Case -in @('create', 'all')) {
    Invoke-IssueCreationTest
    Write-Output 'PASS: live flow creates one Issue through the external CLI boundary'
    [void]$PassedCases.Add('create')
}

if ($Case -in @('prompts', 'all')) {
    Invoke-PromptContractTest
    Write-Output 'PASS: prompt pair preserves exclusive executor and SHA-bound review'
    [void]$PassedCases.Add('prompts')
}

$Total = $PassedCases.Count
$ExpectedTotal = if ($Case -eq 'all') { 5 } else { 1 }
if ($Total -ne $ExpectedTotal) {
    throw "Expected $ExpectedTotal test cases for -Case $Case, observed $Total."
}
Write-Output "RESULT: $Total/$ExpectedTotal"
[ordered]@{
    ok     = $true
    passed = $Total
    total  = $ExpectedTotal
    cases  = @($PassedCases)
} | ConvertTo-Json -Compress
