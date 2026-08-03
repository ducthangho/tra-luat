[CmdletBinding()]
param(
    [ValidateSet('preview', 'create_guard', 'create', 'reviewer', 'all')]
    [string]$Case = 'all'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ControllerPath = [System.IO.Path]::GetFullPath(
    (Join-Path $PSScriptRoot '..\Invoke-SharedWorkPacketFlow.ps1')
)
$PowerShellPath = (Get-Process -Id $PID).Path
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Get-D0SourceFiles {
    return @(
        'CONTEXT.md',
        'docs/PROTOCOL_DA_PHIEN.md',
        'docs/KE_HOACH_TRIEN_KHAI_PROTOCOL_DA_PHIEN.md',
        'docs/adr/0001-canonical-only-versioning-bundle-protocol.md',
        'docs/adr/0017-pr-github-la-ban-giao-va-dieu-phoi-chinh.md',
        'docs/adr/0018-eol-canonical-theo-loai-tep.md',
        'docs/adr/0019-ba-skill-adapter-hai-agent-mot-protocol.md',
        'docs/adr/0020-ranh-gioi-an-ninh-worker-cloud.md',
        'docs/adr/0021-local-controller-headless-tren-windows.md',
        'docs/adr/0022-hai-cong-land-va-deploy.md',
        'docs/adr/0023-tham-quyen-lenh-dieu-phoi.md',
        'docs/adr/0024-review-phan-tang-khi-het-quota.md',
        'docs/adr/0025-issue-contract-va-state-machine.md',
        'docs/adr/0026-rollout-theo-promotion-gate.md',
        'docs/adr/0027-mission-integration-branch.md',
        'docs/adr/0028-stale-generation-va-retention.md',
        'docs/adr/0029-budget-guard-cho-agent.md',
        'docs/adr/0030-definition-of-done-cua-mission.md',
        'docs/adr/0031-test-fragment-thay-khoa-toan-cuc-selftest.md',
        'docs/adr/0032-change-impact-rule-co-huong.md',
        'docs/adr/0033-durable-inbox-va-reconciler.md',
        'docs/research/2026-08-03-danh-gia-gop-y-adr-0017-0032-cuoi.md',
        'docs/research/2026-08-03-phan-bien-protocol-da-phien.md'
    )
}

function Invoke-PreviewTest {
    $HelpText = (Get-Help $ControllerPath -Examples | Out-String)
    if ($HelpText.IndexOf('D:\Quốc hội\tra-luat', [System.StringComparison]::Ordinal) -lt 0) {
        throw 'Controller help did not preserve the Vietnamese canonical path.'
    }

    $Suffix = [Guid]::NewGuid().ToString('N')
    $TestRoot = Join-Path ([System.IO.Path]::GetTempPath()) "wp-flow-preview-Quốc hội-$Suffix"
    $RepoRoot = Join-Path $TestRoot 'repo'
    $GitShim = Join-Path $TestRoot 'git.cmd'
    $GhShim = Join-Path $TestRoot 'gh.cmd'
    $GitStatusPath = Join-Path $TestRoot 'git-status.txt'
    $GitLogPath = Join-Path $TestRoot 'git-calls.log'
    $GhLogPath = Join-Path $TestRoot 'gh-calls.log'
    $SnapshotPath = Join-Path $TestRoot 'forbidden-snapshot.json'
    $SnapshotBodyPath = Join-Path $TestRoot 'forbidden-snapshot.md'
    $BodyPath = Join-Path $TestRoot 'packet.md'
    $SourceFiles = @(Get-D0SourceFiles)
    $OriginalGitLog = $env:WP_FLOW_PREVIEW_GIT_LOG
    $OriginalGhLog = $env:WP_FLOW_PREVIEW_GH_LOG
    $OriginalGitStatus = $env:WP_FLOW_PREVIEW_GIT_STATUS
    $OriginalRepo = $env:WP_FLOW_PREVIEW_REPO
    $Snapshot = [ordered]@{
        repo_slug        = 'example/tra-luat'
        base_sha         = '0123456789abcdef0123456789abcdef01234567'
        version          = '1.36.59'
        observed_at      = '2026-08-04T00:00:00Z'
        open_prs         = @()
        source_files     = $SourceFiles
        source_status    = @($SourceFiles | ForEach-Object { "?? $_" })
        bootstrap_ready  = $true
        bootstrap_missing = @()
    }

    [void](New-Item -ItemType Directory -Path $RepoRoot -Force)
    foreach ($RelativePath in $SourceFiles) {
        $SourcePath = Join-Path $RepoRoot $RelativePath
        [void](New-Item -ItemType Directory -Path (Split-Path -Parent $SourcePath) -Force)
        [System.IO.File]::WriteAllText($SourcePath, "fixture`n", $Utf8NoBom)
    }
    [System.IO.File]::WriteAllText(
        $SnapshotPath,
        ($Snapshot | ConvertTo-Json -Depth 5),
        $Utf8NoBom
    )
    $GitShimBody = @(
        '@echo off',
        'echo %*>>"%WP_FLOW_PREVIEW_GIT_LOG%"',
        'if "%~3"=="rev-parse" if "%~4"=="--show-toplevel" (echo %WP_FLOW_PREVIEW_REPO%& exit /b 0)',
        'if "%~3"=="fetch" exit /b 0',
        'if "%~3"=="rev-parse" if "%~4"=="origin/master" (echo 1111111111111111111111111111111111111111& exit /b 0)',
        'if "%~3"=="show" (echo 1.36.59& exit /b 0)',
        'if "%~3"=="cat-file" exit /b 0',
        'if "%~3"=="status" (type "%WP_FLOW_PREVIEW_GIT_STATUS%"& exit /b 0)',
        'exit /b 9'
    ) -join [Environment]::NewLine
    $GhShimBody = @(
        '@echo off',
        'echo %*>>"%WP_FLOW_PREVIEW_GH_LOG%"',
        'if "%~1"=="auth" exit /b 0',
        'if "%~1"=="repo" (echo {"nameWithOwner":"example/tra-luat"}& exit /b 0)',
        'if "%~1"=="pr" (echo []& exit /b 0)',
        'exit /b 9'
    ) -join [Environment]::NewLine
    [System.IO.File]::WriteAllText($GitShim, $GitShimBody, $Utf8NoBom)
    [System.IO.File]::WriteAllLines(
        $GitStatusPath,
        @($SourceFiles | ForEach-Object { "?? $_" }),
        $Utf8NoBom
    )
    [System.IO.File]::WriteAllText($GhShim, $GhShimBody, $Utf8NoBom)

    try {
        $env:WP_FLOW_PREVIEW_GIT_LOG = $GitLogPath
        $env:WP_FLOW_PREVIEW_GH_LOG = $GhLogPath
        $env:WP_FLOW_PREVIEW_GIT_STATUS = $GitStatusPath
        $env:WP_FLOW_PREVIEW_REPO = $RepoRoot

        $OriginalErrorActionPreference = $ErrorActionPreference
        try {
            $ErrorActionPreference = 'Continue'
            $SnapshotOutput = ((& $PowerShellPath -NoProfile -File $ControllerPath `
                -Action Preview `
                -CanonicalRepoPath $RepoRoot `
                -SnapshotPath $SnapshotPath `
                -BodyOutputPath $SnapshotBodyPath `
                -NoClipboard 2>&1) | Out-String).Trim()
            $SnapshotExitCode = $LASTEXITCODE
        }
        finally {
            $ErrorActionPreference = $OriginalErrorActionPreference
        }
        if ($SnapshotExitCode -eq 0) {
            throw 'Public Preview unexpectedly accepted a snapshot that bypasses live measurement.'
        }
        if ($SnapshotOutput.IndexOf('SnapshotPath', [System.StringComparison]::Ordinal) -lt 0) {
            throw "Snapshot bypass rejection did not identify SnapshotPath. Output: $SnapshotOutput"
        }
        if (Test-Path -LiteralPath $SnapshotBodyPath) {
            throw 'Rejected snapshot bypass must not create a packet body.'
        }

        $Output = ((& $PowerShellPath -NoProfile -File $ControllerPath `
            -Action Preview `
            -CanonicalRepoPath $RepoRoot `
            -BodyOutputPath $BodyPath `
            -GitCommand $GitShim `
            -GhCommand $GhShim `
            -NoClipboard) | Out-String).Trim()
        if ($LASTEXITCODE -ne 0) {
            throw "Preview failed with exit code $LASTEXITCODE. Output: $Output"
        }

        $Result = $Output | ConvertFrom-Json
        if (-not [bool]$Result.ok) {
            throw 'Preview did not report ok=true.'
        }
        if ($Result.action -cne 'Preview') {
            throw "Expected action Preview, got: $($Result.action)"
        }
        if (-not [bool]$Result.dry_run -or $null -ne $Result.issue_number) {
            throw 'Preview must remain dry-run and must not create an Issue.'
        }
        if ($Result.status -cne 'ready_for_claim') {
            throw "Unexpected preview status: $($Result.status)"
        }
        if (-not (Test-Path -LiteralPath $BodyPath -PathType Leaf)) {
            throw 'Preview did not create the requested packet body.'
        }

        $GitCalls = [System.IO.File]::ReadAllLines($GitLogPath) -join "`n"
        if ($GitCalls.IndexOf('fetch origin --prune', [System.StringComparison]::Ordinal) -lt 0) {
            throw 'Preview did not fetch origin --prune.'
        }
        if ($GitCalls.IndexOf('status --porcelain=v1 --untracked-files=all --', [System.StringComparison]::Ordinal) -lt 0) {
            throw 'Preview did not measure the canonical D0 source status.'
        }
        $GhCalls = [System.IO.File]::ReadAllLines($GhLogPath) -join "`n"
        foreach ($ExpectedCall in @('auth status', 'repo view', 'pr list')) {
            if ($GhCalls.IndexOf($ExpectedCall, [System.StringComparison]::Ordinal) -lt 0) {
                throw "Preview did not run gh $ExpectedCall."
            }
        }
        if ($GhCalls.IndexOf('issue ', [System.StringComparison]::Ordinal) -ge 0) {
            throw 'Preview must not call the GitHub Issue API.'
        }
    }
    finally {
        $env:WP_FLOW_PREVIEW_GIT_LOG = $OriginalGitLog
        $env:WP_FLOW_PREVIEW_GH_LOG = $OriginalGhLog
        $env:WP_FLOW_PREVIEW_GIT_STATUS = $OriginalGitStatus
        $env:WP_FLOW_PREVIEW_REPO = $OriginalRepo
        if (Test-Path -LiteralPath $TestRoot -PathType Container) {
            $ResolvedTestRoot = (Resolve-Path -LiteralPath $TestRoot).Path
            $ResolvedTempRoot = [System.IO.Path]::GetFullPath(
                [System.IO.Path]::GetTempPath()
            ).TrimEnd('\') + '\'
            if (-not $ResolvedTestRoot.StartsWith(
                    $ResolvedTempRoot,
                    [System.StringComparison]::OrdinalIgnoreCase
                )) {
                throw "Refusing to remove test directory outside temp: $ResolvedTestRoot"
            }
            Remove-Item -LiteralPath $ResolvedTestRoot -Recurse -Force
        }
    }
}

function Invoke-CreateGuardTest {
    $OriginalErrorActionPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = 'Continue'
        $Output = ((& $PowerShellPath -NoProfile -File $ControllerPath `
            -Action CreateExecutor `
            -NoClipboard 2>&1) | Out-String).Trim()
        $ExitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $OriginalErrorActionPreference
    }

    if ($ExitCode -eq 0) {
        throw 'CreateExecutor unexpectedly ran without -ConfirmCreateIssue.'
    }
    if ($Output.IndexOf('-ConfirmCreateIssue', [System.StringComparison]::Ordinal) -lt 0) {
        throw "CreateExecutor did not explain its permission gate. Output: $Output"
    }
}

function Invoke-CreateExecutorTest {
    $Suffix = [Guid]::NewGuid().ToString('N')
    $TestRoot = Join-Path ([System.IO.Path]::GetTempPath()) "wp-flow-create-Quốc hội-$Suffix"
    $RepoRoot = Join-Path $TestRoot 'repo'
    $GitShim = Join-Path $TestRoot 'git.cmd'
    $GhShim = Join-Path $TestRoot 'gh.cmd'
    $GitStatusPath = Join-Path $TestRoot 'git-status.txt'
    $GhLogPath = Join-Path $TestRoot 'gh-calls.log'
    $BodyPath = Join-Path $TestRoot 'packet.md'
    $PromptPath = Join-Path $TestRoot 'codex-prompt.md'
    $ExecutorWorktree = Join-Path $TestRoot 'executor-worktree'
    $OriginalGhLog = $env:WP_FLOW_GH_LOG
    $OriginalGitStatus = $env:WP_FLOW_GIT_STATUS
    $OriginalRepo = $env:WP_FLOW_REPO

    [void](New-Item -ItemType Directory -Path $RepoRoot -Force)
    foreach ($RelativePath in Get-D0SourceFiles) {
        $SourcePath = Join-Path $RepoRoot $RelativePath
        [void](New-Item -ItemType Directory -Path (Split-Path -Parent $SourcePath) -Force)
        [System.IO.File]::WriteAllText($SourcePath, "fixture`n", $Utf8NoBom)
    }

    $GitShimBody = @(
        '@echo off',
        'if "%~3"=="rev-parse" if "%~4"=="--show-toplevel" (echo %WP_FLOW_REPO%& exit /b 0)',
        'if "%~3"=="fetch" exit /b 0',
        'if "%~3"=="rev-parse" if "%~4"=="origin/master" (echo 1111111111111111111111111111111111111111& exit /b 0)',
        'if "%~3"=="show" (echo 1.36.59& exit /b 0)',
        'if "%~3"=="cat-file" exit /b 0',
        'if "%~3"=="status" (type "%WP_FLOW_GIT_STATUS%"& exit /b 0)',
        'exit /b 9'
    ) -join [Environment]::NewLine
    $GhShimBody = @(
        '@echo off',
        'echo %*>>"%WP_FLOW_GH_LOG%"',
        'if "%~1"=="auth" exit /b 0',
        'if "%~1"=="repo" (echo {"nameWithOwner":"example/tra-luat"}& exit /b 0)',
        'if "%~1"=="pr" (echo []& exit /b 0)',
        'if "%~1"=="issue" (echo https://github.com/example/tra-luat/issues/77& exit /b 0)',
        'exit /b 9'
    ) -join [Environment]::NewLine
    [System.IO.File]::WriteAllText($GitShim, $GitShimBody, $Utf8NoBom)
    [System.IO.File]::WriteAllLines(
        $GitStatusPath,
        @(Get-D0SourceFiles | ForEach-Object { "?? $_" }),
        $Utf8NoBom
    )
    [System.IO.File]::WriteAllText($GhShim, $GhShimBody, $Utf8NoBom)

    try {
        $env:WP_FLOW_GH_LOG = $GhLogPath
        $env:WP_FLOW_GIT_STATUS = $GitStatusPath
        $env:WP_FLOW_REPO = $RepoRoot
        $Output = ((& $PowerShellPath -NoProfile -File $ControllerPath `
            -Action CreateExecutor `
            -CanonicalRepoPath $RepoRoot `
            -BodyOutputPath $BodyPath `
            -PromptOutputPath $PromptPath `
            -ExecutorWorktree $ExecutorWorktree `
            -GitCommand $GitShim `
            -GhCommand $GhShim `
            -ConfirmCreateIssue `
            -NoClipboard 2>&1) | Out-String).Trim()
        if ($LASTEXITCODE -ne 0) {
            throw "CreateExecutor failed with exit code $LASTEXITCODE. Output: $Output"
        }

        $Result = $Output | ConvertFrom-Json
        if (-not [bool]$Result.ok -or $Result.action -cne 'CreateExecutor') {
            throw "Unexpected CreateExecutor result: $Output"
        }
        if ($Result.issue_number -ne 77 -or $Result.packet_id -cne 'wp77') {
            throw "Issue identity was not propagated: $Output"
        }
        if ($Result.branch -cne 'agent/wp77-g1-codex') {
            throw "Unexpected executor branch: $($Result.branch)"
        }
        if ($Result.executor_prompt_path -cne [System.IO.Path]::GetFullPath($PromptPath)) {
            throw "Unexpected executor prompt path: $($Result.executor_prompt_path)"
        }
        $Prompt = [System.IO.File]::ReadAllText($PromptPath)
        if ([regex]::IsMatch($Prompt, '\{\{[^{}]*\}\}')) {
            throw 'CreateExecutor left an unresolved prompt placeholder.'
        }
        if ($Prompt.IndexOf('agent/wp77-g1-codex', [System.StringComparison]::Ordinal) -lt 0) {
            throw 'Filled executor prompt does not contain the exact packet branch.'
        }

        $IssueCreateCalls = @(
            [System.IO.File]::ReadAllLines($GhLogPath) |
            Where-Object { $_.StartsWith('issue create ', [System.StringComparison]::Ordinal) }
        )
        if ($IssueCreateCalls.Count -ne 1) {
            throw "Expected exactly one Issue creation call, got $($IssueCreateCalls.Count)."
        }
    }
    finally {
        $env:WP_FLOW_GH_LOG = $OriginalGhLog
        $env:WP_FLOW_GIT_STATUS = $OriginalGitStatus
        $env:WP_FLOW_REPO = $OriginalRepo
        if (Test-Path -LiteralPath $TestRoot -PathType Container) {
            $ResolvedTestRoot = (Resolve-Path -LiteralPath $TestRoot).Path
            $ResolvedTempRoot = [System.IO.Path]::GetFullPath(
                [System.IO.Path]::GetTempPath()
            ).TrimEnd('\') + '\'
            if (-not $ResolvedTestRoot.StartsWith(
                    $ResolvedTempRoot,
                    [System.StringComparison]::OrdinalIgnoreCase
                )) {
                throw "Refusing to remove test directory outside temp: $ResolvedTestRoot"
            }
            Remove-Item -LiteralPath $ResolvedTestRoot -Recurse -Force
        }
    }
}

function Invoke-PrepareReviewerTest {
    $Suffix = [Guid]::NewGuid().ToString('N')
    $TestRoot = Join-Path ([System.IO.Path]::GetTempPath()) "wp-flow-review-Quốc hội-$Suffix"
    $RepoRoot = Join-Path $TestRoot 'repo'
    $OriginRoot = Join-Path $TestRoot 'origin.git'
    $ReviewWorktree = Join-Path $TestRoot "reviewer's worktree"
    $StaleReviewWorktree = Join-Path $TestRoot 'stale-review-worktree'
    $PromptPath = Join-Path $TestRoot 'claude-prompt.md'
    $StalePromptPath = Join-Path $TestRoot 'stale-claude-prompt.md'
    $GitPath = (Get-Command git -ErrorAction Stop).Source
    $PacketBranch = 'agent/wp77-g1-codex'

    function Invoke-TestGit {
        param([Parameter(Mandatory)][string[]]$GitArguments)

        $OriginalErrorActionPreference = $ErrorActionPreference
        try {
            $ErrorActionPreference = 'Continue'
            $GitOutput = ((& $GitPath @GitArguments 2>&1) | Out-String).Trim()
            $GitExitCode = $LASTEXITCODE
        }
        finally {
            $ErrorActionPreference = $OriginalErrorActionPreference
        }
        if ($GitExitCode -ne 0) {
            throw "Test git failed: git $($GitArguments -join ' ')`n$GitOutput"
        }
        return $GitOutput
    }

    [void](New-Item -ItemType Directory -Path $TestRoot -Force)
    try {
        [void](Invoke-TestGit -GitArguments @('init', $RepoRoot))
        [void](Invoke-TestGit -GitArguments @('-C', $RepoRoot, 'config', 'user.name', 'Flow Test'))
        [void](Invoke-TestGit -GitArguments @('-C', $RepoRoot, 'config', 'user.email', 'flow-test@example.invalid'))
        [void](Invoke-TestGit -GitArguments @('-C', $RepoRoot, 'config', 'core.autocrlf', 'false'))
        [System.IO.File]::WriteAllText((Join-Path $RepoRoot 'fixture.txt'), "base`n", $Utf8NoBom)
        [void](Invoke-TestGit -GitArguments @('-C', $RepoRoot, 'add', 'fixture.txt'))
        [void](Invoke-TestGit -GitArguments @('-C', $RepoRoot, 'commit', '-m', 'base'))
        $Base = Invoke-TestGit -GitArguments @('-C', $RepoRoot, 'rev-parse', 'HEAD')

        [void](Invoke-TestGit -GitArguments @('init', '--bare', $OriginRoot))
        [void](Invoke-TestGit -GitArguments @('-C', $RepoRoot, 'remote', 'add', 'origin', $OriginRoot))
        [void](Invoke-TestGit -GitArguments @('-C', $RepoRoot, 'push', '-u', 'origin', 'HEAD:master'))
        [void](Invoke-TestGit -GitArguments @('-C', $RepoRoot, 'checkout', '-b', $PacketBranch))
        [System.IO.File]::WriteAllText((Join-Path $RepoRoot 'fixture.txt'), "head`n", $Utf8NoBom)
        [void](Invoke-TestGit -GitArguments @('-C', $RepoRoot, 'add', 'fixture.txt'))
        [void](Invoke-TestGit -GitArguments @('-C', $RepoRoot, 'commit', '-m', 'head'))
        $Head = Invoke-TestGit -GitArguments @('-C', $RepoRoot, 'rev-parse', 'HEAD')
        [void](Invoke-TestGit -GitArguments @('-C', $RepoRoot, 'push', '-u', 'origin', $PacketBranch))

        $OriginalErrorActionPreference = $ErrorActionPreference
        try {
            $ErrorActionPreference = 'Continue'
            $StaleOutput = ((& $PowerShellPath -NoProfile -File $ControllerPath `
                -Action PrepareReviewer `
                -CanonicalRepoPath $RepoRoot `
                -IssueNumber 77 `
                -BaseSha $Base `
                -HeadSha $Base `
                -Branch $PacketBranch `
                -ReviewWorktree $StaleReviewWorktree `
                -PromptOutputPath $StalePromptPath `
                -GitCommand $GitPath `
                -NoClipboard 2>&1) | Out-String).Trim()
            $StaleExitCode = $LASTEXITCODE
        }
        finally {
            $ErrorActionPreference = $OriginalErrorActionPreference
        }
        if ($StaleExitCode -eq 0) {
            throw 'PrepareReviewer accepted a stale head after the remote packet branch moved.'
        }
        if ($StaleOutput.IndexOf('FETCH_HEAD', [System.StringComparison]::Ordinal) -lt 0) {
            throw "Stale reviewer failure did not identify the fetched branch head. Output: $StaleOutput"
        }
        if (Test-Path -LiteralPath $StaleReviewWorktree) {
            throw 'Stale reviewer preparation must fail before creating a worktree.'
        }

        $Output = ((& $PowerShellPath -NoProfile -File $ControllerPath `
            -Action PrepareReviewer `
            -CanonicalRepoPath $RepoRoot `
            -IssueNumber 77 `
            -BaseSha $Base `
            -HeadSha $Head `
            -Branch $PacketBranch `
            -ReviewWorktree $ReviewWorktree `
            -PromptOutputPath $PromptPath `
            -GitCommand $GitPath `
            -NoClipboard 2>&1) | Out-String).Trim()
        if ($LASTEXITCODE -ne 0) {
            throw "PrepareReviewer failed with exit code $LASTEXITCODE. Output: $Output"
        }

        $Result = $Output | ConvertFrom-Json
        if (-not [bool]$Result.ok -or $Result.action -cne 'PrepareReviewer') {
            throw "Unexpected PrepareReviewer result: $Output"
        }
        if (-not [bool]$Result.setup_completed) {
            throw 'PrepareReviewer did not report completed detached-worktree setup.'
        }
        if (@($Result.review_setup_commands).Count -ne 2) {
            throw 'Reviewer result must retain exactly two auditable setup commands.'
        }
        $MeasuredHead = Invoke-TestGit -GitArguments @('-C', $ReviewWorktree, 'rev-parse', 'HEAD')
        if ($MeasuredHead -cne $Head) {
            throw "Detached review worktree is at $MeasuredHead, expected $Head."
        }
        $MeasuredBranch = Invoke-TestGit -GitArguments @('-C', $ReviewWorktree, 'branch', '--show-current')
        if (-not [string]::IsNullOrWhiteSpace($MeasuredBranch)) {
            throw "Review worktree is not detached: $MeasuredBranch"
        }
        $MeasuredStatus = Invoke-TestGit -GitArguments @('-C', $ReviewWorktree, 'status', '--short')
        if (-not [string]::IsNullOrWhiteSpace($MeasuredStatus)) {
            throw "Review worktree is dirty: $MeasuredStatus"
        }
        $Prompt = [System.IO.File]::ReadAllText($PromptPath)
        if ([regex]::IsMatch($Prompt, '\{\{[^{}]*\}\}')) {
            throw 'PrepareReviewer left an unresolved prompt placeholder.'
        }
        if ($Prompt.IndexOf($Head, [System.StringComparison]::Ordinal) -lt 0) {
            throw 'Filled reviewer prompt does not pin the exact head SHA.'
        }
    }
    finally {
        if (Test-Path -LiteralPath $TestRoot -PathType Container) {
            $ResolvedTestRoot = (Resolve-Path -LiteralPath $TestRoot).Path
            $ResolvedTempRoot = [System.IO.Path]::GetFullPath(
                [System.IO.Path]::GetTempPath()
            ).TrimEnd('\') + '\'
            if (-not $ResolvedTestRoot.StartsWith(
                    $ResolvedTempRoot,
                    [System.StringComparison]::OrdinalIgnoreCase
                )) {
                throw "Refusing to remove test directory outside temp: $ResolvedTestRoot"
            }
            Remove-Item -LiteralPath $ResolvedTestRoot -Recurse -Force
        }
    }
}

$PassedCount = 0

if ($Case -in @('preview', 'all')) {
    Invoke-PreviewTest
    Write-Output 'PASS: preview'
    $PassedCount += 1
}

if ($Case -in @('create_guard', 'all')) {
    Invoke-CreateGuardTest
    Write-Output 'PASS: create_guard'
    $PassedCount += 1
}

if ($Case -in @('create', 'all')) {
    Invoke-CreateExecutorTest
    Write-Output 'PASS: create'
    $PassedCount += 1
}

if ($Case -in @('reviewer', 'all')) {
    Invoke-PrepareReviewerTest
    Write-Output 'PASS: reviewer'
    $PassedCount += 1
}

$ExpectedCount = if ($Case -eq 'all') { 4 } else { 1 }
if ($PassedCount -ne $ExpectedCount) {
    throw "Expected $ExpectedCount selected flow tests, observed $PassedCount."
}
Write-Output "RESULT: $PassedCount/$ExpectedCount"
