[CmdletBinding()]
param(
    [ValidateSet('ready', 'paused', 'prereq', 'prompts', 'all')]
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

    if (-not $Text.Contains($Expected, [System.StringComparison]::Ordinal)) {
        throw "Expected generated packet to contain: $Expected"
    }
}

function Invoke-ReadyPacketTest {
    $Suffix = [Guid]::NewGuid().ToString('N')
    $SnapshotPath = Join-Path ([System.IO.Path]::GetTempPath()) "wp-ready-$Suffix.json"
    $BodyPath = Join-Path ([System.IO.Path]::GetTempPath()) "wp-ready-$Suffix.md"

    $Snapshot = [ordered]@{
        repo_slug  = 'example/tra-luat'
        base_sha   = '0123456789abcdef0123456789abcdef01234567'
        version    = '1.36.59'
        observed_at = '2026-08-03T12:00:00+07:00'
        open_prs   = @()
    } | ConvertTo-Json -Depth 5

    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($SnapshotPath, $Snapshot, $Utf8NoBom)

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

        $Body = [System.IO.File]::ReadAllText($BodyPath)
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
    finally {
        Remove-Item -LiteralPath $SnapshotPath -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath $BodyPath -Force -ErrorAction SilentlyContinue
    }
}

function Invoke-PausedPacketTest {
    $Suffix = [Guid]::NewGuid().ToString('N')
    $SnapshotPath = Join-Path ([System.IO.Path]::GetTempPath()) "wp-paused-$Suffix.json"
    $BodyPath = Join-Path ([System.IO.Path]::GetTempPath()) "wp-paused-$Suffix.md"

    $Snapshot = [ordered]@{
        repo_slug   = 'example/tra-luat'
        base_sha    = 'fedcba9876543210fedcba9876543210fedcba98'
        version     = '1.36.60'
        observed_at = '2026-08-03T12:30:00+07:00'
        open_prs    = @(
            [ordered]@{
                number       = 42
                title        = 'Concurrent writer'
                headRefName  = 'agent/wp42-g1-claude'
                url          = 'https://github.com/example/tra-luat/pull/42'
            }
        )
    } | ConvertTo-Json -Depth 5

    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($SnapshotPath, $Snapshot, $Utf8NoBom)

    try {
        $Output = ((& $PowerShellPath -NoProfile -File $ScriptPath `
            -SnapshotPath $SnapshotPath `
            -DryRun `
            -BodyOutputPath $BodyPath) | Out-String).Trim()
        $ExitCode = $LASTEXITCODE

        if ($ExitCode -ne 0) {
            throw "Packet CLI failed with exit code $ExitCode. Output: $Output"
        }

        $Body = [System.IO.File]::ReadAllText($BodyPath)
        Assert-Contains -Text $Body -Expected '- Status: PAUSE_OPEN_PR'
        Assert-Contains -Text $Body -Expected '- open_pr_count: 1'
        Assert-Contains -Text $Body -Expected '#42 — Concurrent writer — branch: agent/wp42-g1-claude'
        Assert-Contains -Text $Body -Expected 'https://github.com/example/tra-luat/pull/42'
    }
    finally {
        Remove-Item -LiteralPath $SnapshotPath -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath $BodyPath -Force -ErrorAction SilentlyContinue
    }
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

    try {
        $env:PATH = ''
        $Output = ((& $PowerShellPath -NoProfile -File $ScriptPath `
            -RepoPath $RepoRoot `
            -DryRun `
            -BodyOutputPath $BodyPath 2>&1) | Out-String).Trim()
        $ExitCode = $LASTEXITCODE

        if ($ExitCode -eq 0) {
            throw 'Live preflight unexpectedly succeeded without git or gh in PATH.'
        }
        Assert-Contains -Text $Output -Expected 'Không tìm thấy git trong PATH.'
        if (Test-Path -LiteralPath $BodyPath) {
            throw 'Failed preflight must not leave a generated packet body.'
        }
    }
    finally {
        $env:PATH = $OriginalPath
        Remove-Item -LiteralPath $BodyPath -Force -ErrorAction SilentlyContinue
    }
}

if ($Case -in @('ready', 'all')) {
    Invoke-ReadyPacketTest
    Write-Output 'PASS: zero open PR generates a ready work packet'
}

if ($Case -in @('paused', 'all')) {
    Invoke-PausedPacketTest
    Write-Output 'PASS: open PR generates a paused work packet'
}

if ($Case -in @('prereq', 'all')) {
    Invoke-MissingToolTest
    Write-Output 'PASS: live preflight fails closed when required tools are missing'
}

if ($Case -in @('prompts', 'all')) {
    Invoke-PromptContractTest
    Write-Output 'PASS: prompt pair preserves exclusive executor and SHA-bound review'
}
