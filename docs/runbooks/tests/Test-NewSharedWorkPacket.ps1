[CmdletBinding()]
param(
    [ValidateSet('ready', 'paused', 'bootstrap', 'inventory', 'prereq', 'create', 'prompts', 'fill_executor', 'fill_reviewer', 'fill_leftover', 'all')]
    [string]$Case = 'all'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptPath = [System.IO.Path]::GetFullPath(
    (Join-Path $PSScriptRoot '..\New-SharedWorkPacket.ps1')
)
$PromptFillerPath = [System.IO.Path]::GetFullPath(
    (Join-Path $PSScriptRoot '..\Fill-SharedWorkPacketPrompt.ps1')
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

function Assert-NotContains {
    param(
        [Parameter(Mandatory)]
        [string]$Text,

        [Parameter(Mandatory)]
        [string]$Unexpected
    )

    if ($Text.IndexOf($Unexpected, [System.StringComparison]::Ordinal) -ge 0) {
        throw "Expected content not to contain: $Unexpected"
    }
}

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

function Get-D0SourceStatus {
    return @(Get-D0SourceFiles | ForEach-Object { "?? $_" })
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
        source_files = @(Get-D0SourceFiles)
        source_status = @(Get-D0SourceStatus)
        bootstrap_ready = $true
        bootstrap_missing = @()
    })

    Assert-Contains -Text $Body -Expected '# Work Packet — wp{{ISSUE_NUMBER}} (alias: wp-d0-protocol-constitution)'
    Assert-Contains -Text $Body -Expected '- Status: ready_for_claim'
    Assert-Contains -Text $Body -Expected '- Planned executor: codex'
    Assert-Contains -Text $Body -Expected '- Cross-provider reviewer: claude'
    Assert-Contains -Text $Body -Expected '- base_sha_observed: 0123456789abcdef0123456789abcdef01234567'
    Assert-Contains -Text $Body -Expected '- Không có PR mở tại observed_at; vẫn phải đo lại lúc claim.'
    Assert-Contains -Text $Body -Expected 'docs/prompts/CODEX_EXECUTOR_D0.md'
    Assert-Contains -Text $Body -Expected 'docs/runbooks/Fill-SharedWorkPacketPrompt.ps1'
    Assert-Contains -Text $Body -Expected '## 4. Write-set (ĐÍCH DANH, 23 đường)'
    Assert-Contains -Text $Body -Expected '`docs/adr/0033-durable-inbox-va-reconciler.md`'
    Assert-Contains -Text $Body -Expected '`docs/research/2026-08-03-phan-bien-protocol-da-phien.md`'
    Assert-Contains -Text $Body -Expected 'COPY BYTE NGUYÊN VẸN'
    Assert-Contains -Text $Body -Expected 'Cây canonical đang bẩn chỉ là nguồn đọc'
    Assert-NotContains -Text $Body -Unexpected 'cùng ba bootstrap artifact của packet này'
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
        source_files = @(Get-D0SourceFiles)
        source_status = @(Get-D0SourceStatus)
        bootstrap_ready = $true
        bootstrap_missing = @()
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

function Invoke-BootstrapNotLandedTest {
    $Body = Invoke-SnapshotPreview -Name 'bootstrap' -Snapshot ([ordered]@{
        repo_slug        = 'example/tra-luat'
        base_sha         = '0123456789abcdef0123456789abcdef01234567'
        version          = '1.36.59'
        observed_at      = '2026-08-03T12:00:00Z'
        open_prs         = @()
        source_files     = @(Get-D0SourceFiles)
        source_status    = @(Get-D0SourceStatus)
        bootstrap_ready  = $false
        bootstrap_missing = @('docs/runbooks/Fill-SharedWorkPacketPrompt.ps1')
    })

    Assert-Contains -Text $Body -Expected '- Status: PAUSE_BOOTSTRAP_NOT_LANDED'
    Assert-Contains -Text $Body -Expected 'bootstrap_on_base: false'
    Assert-Contains -Text $Body -Expected '`docs/runbooks/Fill-SharedWorkPacketPrompt.ps1`'
    Assert-Contains -Text $Body -Expected 'Không tạo Issue thật trước khi bootstrap đã land'
}

function Invoke-DirtyInventoryTest {
    $Suffix = [Guid]::NewGuid().ToString('N')
    $SnapshotPath = Join-Path ([System.IO.Path]::GetTempPath()) "wp-inventory-$Suffix.json"
    $BodyPath = Join-Path ([System.IO.Path]::GetTempPath()) "wp-inventory-$Suffix.md"
    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    $Snapshot = [ordered]@{
        repo_slug     = 'example/tra-luat'
        base_sha      = '0123456789abcdef0123456789abcdef01234567'
        version       = '1.36.59'
        observed_at   = '2026-08-03T12:00:00Z'
        open_prs      = @()
        source_files  = @(Get-D0SourceFiles)
        source_status = @(Get-D0SourceStatus | Select-Object -First 22)
        bootstrap_ready = $true
        bootstrap_missing = @()
    }
    [System.IO.File]::WriteAllText(
        $SnapshotPath,
        ($Snapshot | ConvertTo-Json -Depth 5),
        $Utf8NoBom
    )

    $OriginalErrorActionPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = 'Continue'
        $Output = ((& $PowerShellPath -NoProfile -File $ScriptPath `
            -SnapshotPath $SnapshotPath `
            -DryRun `
            -BodyOutputPath $BodyPath 2>&1) | Out-String).Trim()
        $ExitCode = $LASTEXITCODE

        if ($ExitCode -eq 0) {
            throw 'Snapshot with one clean/missing D0 source unexpectedly passed.'
        }
        Assert-Contains -Text $Output -Expected 'source_status'
        if (Test-Path -LiteralPath $BodyPath) {
            throw 'Failed dirty-source validation must not generate a packet body.'
        }
    }
    finally {
        $ErrorActionPreference = $OriginalErrorActionPreference
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
    Assert-Contains -Text $CodexPrompt -Expected '{{ISSUE_NUMBER}}'
    Assert-Contains -Text $CodexPrompt -Expected '{{BASE_SHA}}'
    Assert-Contains -Text $CodexPrompt -Expected 'executor duy nhất'
    Assert-Contains -Text $CodexPrompt -Expected 'REVIEW_READY'
    Assert-Contains -Text $CodexPrompt -Expected 'Không merge hoặc deploy'
    Assert-Contains -Text $CodexPrompt -Expected 'COPY BYTE NGUYÊN VẸN'
    Assert-Contains -Text $CodexPrompt -Expected 'Không `git add -A`/`-u`'
    Assert-Contains -Text $CodexPrompt -Expected '5 cổng JSON'
    Assert-Contains -Text $CodexPrompt -Expected 'marker `[FAIL]`'
    Assert-Contains -Text $CodexPrompt -Expected 'Issue thắng prompt'
    Assert-Contains -Text $CodexPrompt -Expected "git diff --name-status '{{BASE_SHA}}'"
    Assert-Contains -Text $CodexPrompt -Expected "git diff --name-status '{{BASE_SHA}}..HEAD'"
    Assert-Contains -Text $CodexPrompt -Expected 'Nếu worktree đã tồn tại'
    Assert-Contains -Text $CodexPrompt -Expected 'planned:docs/PROTOCOL_DA_PHIEN.md'
    Assert-Contains -Text $CodexPrompt -Expected '$env:GIT_CONFIG_KEY_0 = ''core.abbrev'''
    Assert-Contains -Text $CodexPrompt -Expected 'reviewer_fill_command:'
    Assert-Contains -Text $CodexPrompt -Expected 'Fill-SharedWorkPacketPrompt.ps1'' -Role reviewer'
    Assert-Contains -Text $CodexPrompt -Expected '{{REPO_PATH_PS}}'
    Assert-NotContains -Text $CodexPrompt -Unexpected 'git config core.abbrev 7'
    Assert-NotContains -Text $CodexPrompt -Unexpected 'baseline ~314'

    Assert-Contains -Text $ClaudePrompt -Expected '{{ISSUE_URL}}'
    Assert-Contains -Text $ClaudePrompt -Expected '{{ISSUE_NUMBER}}'
    Assert-Contains -Text $ClaudePrompt -Expected '{{BASE_SHA}}'
    Assert-Contains -Text $ClaudePrompt -Expected '{{HEAD_SHA}}'
    Assert-Contains -Text $ClaudePrompt -Expected 'read-only'
    Assert-Contains -Text $ClaudePrompt -Expected 'Không Edit/Write/commit/push/merge/deploy'
    Assert-Contains -Text $ClaudePrompt -Expected 'cross_approved'
    Assert-Contains -Text $ClaudePrompt -Expected 'review_deferred'
    Assert-Contains -Text $ClaudePrompt -Expected 'Issue thắng mọi danh sách tĩnh trong prompt'
    Assert-Contains -Text $ClaudePrompt -Expected 'blocking: true|false'
    Assert-Contains -Text $ClaudePrompt -Expected 'bản nháp comment GitHub đầy đủ'
    Assert-Contains -Text $ClaudePrompt -Expected 'chỉ đăng sau khi người dùng phê duyệt'
    Assert-Contains -Text $ClaudePrompt -Expected 'Giai đoạn 1 — cơ học'
    Assert-Contains -Text $ClaudePrompt -Expected 'planned:docs/PROTOCOL_DA_PHIEN.md'
    Assert-Contains -Text $ClaudePrompt -Expected 'export GIT_CONFIG_KEY_0=core.abbrev'
    Assert-Contains -Text $ClaudePrompt -Expected 'Các tham chiếu ADR-0001 còn lại trong `SKILL.md`'
    Assert-Contains -Text $ClaudePrompt -Expected 'không phải finding ở D0'
    Assert-NotContains -Text $ClaudePrompt -Unexpected 'worktree add'
    Assert-NotContains -Text $ClaudePrompt -Unexpected 'fetch origin'
    Assert-NotContains -Text $ClaudePrompt -Unexpected 'config core.abbrev'
    Assert-NotContains -Text $ClaudePrompt -Unexpected 'baseline ~314'
    Assert-NotContains -Text $ClaudePrompt -Unexpected 'D:\Quốc hội\_docs_lam_viec'
}

function Invoke-FillExecutorPromptTest {
    $OutputPath = Join-Path ([System.IO.Path]::GetTempPath()) (
        'wp77-executor-' + [Guid]::NewGuid().ToString('N') + '.md'
    )
    $BaseSha = '0123456789abcdef0123456789abcdef01234567'
    $ExecutorWorktree = 'D:\Quốc hội\tra-luat-wt\wp77-codex'
    $RepoPath = "D:\O'Brien\tra-luat"

    try {
        $Output = ((& $PowerShellPath -NoProfile -File $PromptFillerPath `
            -Role executor `
            -IssueNumber 77 `
            -IssueUrl 'https://github.com/example/tra-luat/issues/77' `
            -BaseSha $BaseSha `
            -Generation 2 `
            -Branch 'agent/wp77-g2-codex' `
            -RepoPath $RepoPath `
            -Worktree $ExecutorWorktree `
            -OutputPath $OutputPath `
            -NoClipboard 2>&1) | Out-String).Trim()
        $ExitCode = $LASTEXITCODE
        if ($ExitCode -ne 0) {
            throw "Executor prompt filler failed with exit code $ExitCode. Output: $Output"
        }

        $Summary = $Output | ConvertFrom-Json
        if (-not $Summary.ok -or $Summary.role -ne 'executor') {
            throw "Unexpected executor filler summary: $Output"
        }
        if ($Summary.prompt_output_path -ne $OutputPath) {
            throw "Unexpected filled prompt path: $($Summary.prompt_output_path)"
        }
        if ($Summary.clipboard -ne 'disabled') {
            throw "-NoClipboard was not honored: $Output"
        }

        $Filled = [System.IO.File]::ReadAllText($OutputPath)
        Assert-NotContains -Text $Filled -Unexpected '{{'
        Assert-Contains -Text $Filled -Expected 'work packet `wp77`, generation'
        Assert-Contains -Text $Filled -Expected '`2`, tại `https://github.com/example/tra-luat/issues/77`'
        Assert-Contains -Text $Filled -Expected 'branch là `agent/wp77-g2-codex`'
        Assert-Contains -Text $Filled -Expected $ExecutorWorktree
        Assert-Contains -Text $Filled `
            -Expected "& 'D:\O''Brien\tra-luat\docs\runbooks\Fill-SharedWorkPacketPrompt.ps1'"
        Assert-Contains -Text $Filled -Expected "-RepoPath 'D:\O''Brien\tra-luat'"
    }
    finally {
        Remove-Item -LiteralPath $OutputPath -Force -ErrorAction SilentlyContinue
    }
}

function Invoke-FillReviewerPromptTest {
    $OutputPath = Join-Path ([System.IO.Path]::GetTempPath()) (
        'wp77-reviewer-' + [Guid]::NewGuid().ToString('N') + '.md'
    )
    $BaseSha = '0123456789abcdef0123456789abcdef01234567'
    $HeadSha = 'fedcba9876543210fedcba9876543210fedcba98'
    $RepoPath = 'D:\Quốc hội\tra-luat'
    $ReviewWorktree = 'D:\Quốc hội\tra-luat-review-wp77'
    $InvalidBranchOutputPath = Join-Path ([System.IO.Path]::GetTempPath()) (
        'wp77-invalid-branch-' + [Guid]::NewGuid().ToString('N') + '.md'
    )

    try {
        $Output = ((& $PowerShellPath -NoProfile -File $PromptFillerPath `
            -Role reviewer `
            -IssueNumber 77 `
            -IssueUrl 'https://github.com/example/tra-luat/issues/77' `
            -BaseSha $BaseSha `
            -HeadSha $HeadSha `
            -Generation 2 `
            -Branch 'agent/wp77-g2-codex' `
            -RepoPath $RepoPath `
            -Worktree $ReviewWorktree `
            -OutputPath $OutputPath `
            -NoClipboard 2>&1) | Out-String).Trim()
        $ExitCode = $LASTEXITCODE
        if ($ExitCode -ne 0) {
            throw "Reviewer prompt filler failed with exit code $ExitCode. Output: $Output"
        }

        $Summary = $Output | ConvertFrom-Json
        if (-not $Summary.ok -or $Summary.role -ne 'reviewer') {
            throw "Unexpected reviewer filler summary: $Output"
        }
        if (@($Summary.review_setup_commands).Count -ne 2) {
            throw "Reviewer filler must return exactly two user setup commands: $Output"
        }
        Assert-Contains -Text $Summary.review_setup_commands[0] `
            -Expected "git -C 'D:\Quốc hội\tra-luat' fetch origin 'agent/wp77-g2-codex'"
        Assert-Contains -Text $Summary.review_setup_commands[1] `
            -Expected "worktree add --detach 'D:\Quốc hội\tra-luat-review-wp77' '$HeadSha'"

        $Filled = [System.IO.File]::ReadAllText($OutputPath)
        Assert-NotContains -Text $Filled -Unexpected '{{'
        Assert-Contains -Text $Filled -Expected 'D:/Quốc hội/tra-luat-review-wp77'
        Assert-Contains -Text $Filled -Expected $HeadSha

        $OriginalErrorActionPreference = $ErrorActionPreference
        try {
            $ErrorActionPreference = 'Continue'
            $InvalidBranchResult = ((& $PowerShellPath -NoProfile -File $PromptFillerPath `
                -Role reviewer `
                -IssueNumber 77 `
                -BaseSha $BaseSha `
                -HeadSha $HeadSha `
                -Generation 2 `
                -Branch '--upload-pack=evil' `
                -OutputPath $InvalidBranchOutputPath `
                -NoClipboard 2>&1) | Out-String).Trim()
            if ($LASTEXITCODE -eq 0) {
                throw 'Prompt filler accepted a branch that Git could parse as an option.'
            }
            Assert-Contains -Text $InvalidBranchResult `
                -Expected 'INVALID_BRANCH'
            if (Test-Path -LiteralPath $InvalidBranchOutputPath) {
                throw 'Invalid branch validation must not create a filled prompt.'
            }
        }
        finally {
            $ErrorActionPreference = $OriginalErrorActionPreference
        }
    }
    finally {
        Remove-Item -LiteralPath $OutputPath -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath $InvalidBranchOutputPath -Force -ErrorAction SilentlyContinue
    }
}

function Invoke-FillPromptLeftoverTest {
    $Suffix = [Guid]::NewGuid().ToString('N')
    $TemplateRoot = Join-Path ([System.IO.Path]::GetTempPath()) "wp-fill-template-$Suffix"
    $TemplatePath = Join-Path $TemplateRoot 'CODEX_EXECUTOR_D0.md'
    $OutputPath = Join-Path ([System.IO.Path]::GetTempPath()) "wp-fill-leftover-$Suffix.md"
    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [void](New-Item -ItemType Directory -Path $TemplateRoot)
    [System.IO.File]::WriteAllText(
        $TemplatePath,
        'packet={{PACKET_ID}} unknown={{unknown_token}} mixed={{Issue_Number}} blank={{ }}',
        $Utf8NoBom
    )

    $OriginalErrorActionPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = 'Continue'
        $Output = ((& $PowerShellPath -NoProfile -File $PromptFillerPath `
            -Role executor `
            -IssueNumber 77 `
            -BaseSha '0123456789abcdef0123456789abcdef01234567' `
            -TemplateRoot $TemplateRoot `
            -OutputPath $OutputPath `
            -NoClipboard 2>&1) | Out-String).Trim()
        $ExitCode = $LASTEXITCODE
        if ($ExitCode -eq 0) {
            throw 'Prompt filler unexpectedly accepted an unresolved placeholder.'
        }
        Assert-Contains -Text $Output -Expected '{{unknown_token}}'
        Assert-Contains -Text $Output -Expected '{{Issue_Number}}'
        Assert-Contains -Text $Output -Expected '{{ }}'
        if (Test-Path -LiteralPath $OutputPath) {
            throw 'Failed placeholder validation must not create a filled prompt.'
        }
    }
    finally {
        $ErrorActionPreference = $OriginalErrorActionPreference
        Remove-Item -LiteralPath $OutputPath -Force -ErrorAction SilentlyContinue
        if (Test-Path -LiteralPath $TemplateRoot -PathType Container) {
            $ResolvedTemplateRoot = (Resolve-Path -LiteralPath $TemplateRoot).Path
            $ResolvedTempRoot = [System.IO.Path]::GetFullPath(
                [System.IO.Path]::GetTempPath()
            ).TrimEnd('\') + '\'
            if (-not $ResolvedTemplateRoot.StartsWith(
                    $ResolvedTempRoot,
                    [System.StringComparison]::OrdinalIgnoreCase
                )) {
                throw "Refusing to remove test directory outside temp: $ResolvedTemplateRoot"
            }
            Remove-Item -LiteralPath $ResolvedTemplateRoot -Recurse -Force
        }
    }
}

function Invoke-MissingToolTest {
    $RepoRoot = [System.IO.Path]::GetFullPath(
        (Join-Path $PSScriptRoot '..\..\..')
    )
    $BodyPath = Join-Path ([System.IO.Path]::GetTempPath()) (
        'wp-missing-tool-' + [Guid]::NewGuid().ToString('N') + '.md'
    )
    $OriginalErrorActionPreference = $ErrorActionPreference

    try {
        $ErrorActionPreference = 'Continue'
        $Output = ((& $PowerShellPath -NoProfile -File $ScriptPath `
            -RepoPath $RepoRoot `
            -GitCommand '__wp_missing_git__' `
            -GhCommand '__wp_missing_gh__' `
            -DryRun `
            -BodyOutputPath $BodyPath 2>&1) | Out-String).Trim()
        $ExitCode = $LASTEXITCODE

        if ($ExitCode -eq 0) {
            throw 'Live preflight unexpectedly succeeded without git or gh in PATH.'
        }
        Assert-Contains -Text $Output -Expected 'git'
        Assert-Contains -Text $Output -Expected '__wp_missing_git__'
        if (Test-Path -LiteralPath $BodyPath) {
            throw 'Failed preflight must not leave a generated packet body.'
        }
    }
    finally {
        $ErrorActionPreference = $OriginalErrorActionPreference
        Remove-Item -LiteralPath $BodyPath -Force -ErrorAction SilentlyContinue
    }
}

function Invoke-IssueCreationTest {
    $Suffix = [Guid]::NewGuid().ToString('N')
    $ShimRoot = Join-Path ([System.IO.Path]::GetTempPath()) "wp-shims-$Suffix"
    $RepoRoot = Join-Path $ShimRoot 'repo'
    $GitShim = Join-Path $ShimRoot 'git.cmd'
    $GitStatusPath = Join-Path $ShimRoot 'git-status.txt'
    $GhShim = Join-Path $ShimRoot 'gh.cmd'
    $GhLogPath = Join-Path $ShimRoot 'gh-calls.log'
    $WrapperPath = Join-Path $ShimRoot 'invoke-with-clipboard-guard.ps1'
    $BodyPath = Join-Path ([System.IO.Path]::GetTempPath()) "wp-create-$Suffix.md"
    $OriginalGhLog = $env:WP_GH_LOG
    $OriginalGitStatus = $env:WP_GIT_STATUS
    $OriginalGitShim = $env:WP_GIT_SHIM
    $OriginalGhShim = $env:WP_GH_SHIM
    $OriginalScriptUnderTest = $env:WP_SCRIPT_UNDER_TEST
    $OriginalRepoUnderTest = $env:WP_REPO_UNDER_TEST
    $OriginalBodyUnderTest = $env:WP_BODY_UNDER_TEST
    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

    [void](New-Item -ItemType Directory -Path $RepoRoot)
    foreach ($RelativePath in Get-D0SourceFiles) {
        $SourcePath = Join-Path $RepoRoot $RelativePath
        [void](New-Item -ItemType Directory -Path (Split-Path -Parent $SourcePath) -Force)
        [System.IO.File]::WriteAllText($SourcePath, "fixture`n", $Utf8NoBom)
    }
    $GitShimBody = @(
        '@echo off',
        'if "%~3"=="rev-parse" if "%~4"=="--show-toplevel" (echo %WP_REPO_UNDER_TEST%& exit /b 0)',
        'if "%~3"=="fetch" exit /b 0',
        'if "%~3"=="rev-parse" if "%~4"=="origin/master" (echo 1111111111111111111111111111111111111111& exit /b 0)',
        'if "%~3"=="show" (echo 1.36.59& exit /b 0)',
        'if "%~3"=="cat-file" exit /b 0',
        'if "%~3"=="status" (type "%WP_GIT_STATUS%"& exit /b 0)',
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
    [System.IO.File]::WriteAllLines($GitStatusPath, @(Get-D0SourceStatus), $Utf8NoBom)
    [System.IO.File]::WriteAllText($GhShim, $GhShimBody, $Utf8NoBom)
    $WrapperBody = @(
        '$ErrorActionPreference = ''Stop''',
        'function Set-Clipboard { throw ''CLIPBOARD_CALLED'' }',
        '& $env:WP_SCRIPT_UNDER_TEST -RepoPath $env:WP_REPO_UNDER_TEST -BodyOutputPath $env:WP_BODY_UNDER_TEST -GitCommand $env:WP_GIT_SHIM -GhCommand $env:WP_GH_SHIM -NoClipboard'
    ) -join [Environment]::NewLine
    [System.IO.File]::WriteAllText($WrapperPath, $WrapperBody, $Utf8NoBom)

    try {
        $env:WP_GH_LOG = $GhLogPath
        $env:WP_GIT_STATUS = $GitStatusPath
        $env:WP_GIT_SHIM = $GitShim
        $env:WP_GH_SHIM = $GhShim
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
        if ($Summary.issue_number -ne 77 -or $Summary.packet_id -ne 'wp77') {
            throw "Issue number was not promoted into packet identity: $Output"
        }
        if ($Summary.branch -ne 'agent/wp77-g1-codex') {
            throw "Unexpected executor branch: $($Summary.branch)"
        }
        Assert-Contains -Text $Summary.fill_executor_command `
            -Expected 'Fill-SharedWorkPacketPrompt.ps1'
        Assert-Contains -Text $Summary.fill_executor_command `
            -Expected '-Role executor -IssueNumber 77'
        Assert-Contains -Text $Summary.fill_executor_command `
            -Expected '-BaseSha 1111111111111111111111111111111111111111'
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
        $EditCalls = @(
            [System.IO.File]::ReadAllLines($GhLogPath) |
            Where-Object { $_.StartsWith('issue edit 77 ', [System.StringComparison]::Ordinal) }
        )
        if ($EditCalls.Count -ne 1) {
            throw "Expected exactly one gh issue edit call, observed $($EditCalls.Count)."
        }
        Assert-Contains -Text $EditCalls[0] -Expected "--body-file $BodyPath"

        $FinalBody = [System.IO.File]::ReadAllText($BodyPath)
        Assert-Contains -Text $FinalBody -Expected '# Work Packet — wp77 (alias: wp-d0-protocol-constitution)'
        Assert-Contains -Text $FinalBody -Expected '- Executor branch: `agent/wp77-g1-codex`'
    }
    finally {
        $env:WP_GH_LOG = $OriginalGhLog
        $env:WP_GIT_STATUS = $OriginalGitStatus
        $env:WP_GIT_SHIM = $OriginalGitShim
        $env:WP_GH_SHIM = $OriginalGhShim
        $env:WP_SCRIPT_UNDER_TEST = $OriginalScriptUnderTest
        $env:WP_REPO_UNDER_TEST = $OriginalRepoUnderTest
        $env:WP_BODY_UNDER_TEST = $OriginalBodyUnderTest
        Remove-Item -LiteralPath $BodyPath -Force -ErrorAction SilentlyContinue
        if (Test-Path -LiteralPath $ShimRoot -PathType Container) {
            $ResolvedShimRoot = (Resolve-Path -LiteralPath $ShimRoot).Path
            $ResolvedTempRoot = [System.IO.Path]::GetFullPath(
                [System.IO.Path]::GetTempPath()
            ).TrimEnd('\') + '\'
            if (-not $ResolvedShimRoot.StartsWith(
                    $ResolvedTempRoot,
                    [System.StringComparison]::OrdinalIgnoreCase
                )) {
                throw "Refusing to remove test directory outside temp: $ResolvedShimRoot"
            }
            Remove-Item -LiteralPath $ResolvedShimRoot -Recurse -Force
        }
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

if ($Case -in @('bootstrap', 'all')) {
    Invoke-BootstrapNotLandedTest
    Write-Output 'PASS: missing bootstrap on base pauses packet creation for Android safety'
    [void]$PassedCases.Add('bootstrap')
}

if ($Case -in @('inventory', 'all')) {
    Invoke-DirtyInventoryTest
    Write-Output 'PASS: packet generation rejects a clean or missing D0 source'
    [void]$PassedCases.Add('inventory')
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

if ($Case -in @('fill_executor', 'all')) {
    Invoke-FillExecutorPromptTest
    Write-Output 'PASS: executor prompt filler resolves all late-bound values'
    [void]$PassedCases.Add('fill_executor')
}

if ($Case -in @('fill_reviewer', 'all')) {
    Invoke-FillReviewerPromptTest
    Write-Output 'PASS: reviewer prompt filler emits detached worktree setup for the user'
    [void]$PassedCases.Add('fill_reviewer')
}

if ($Case -in @('fill_leftover', 'all')) {
    Invoke-FillPromptLeftoverTest
    Write-Output 'PASS: prompt filler fails closed when any placeholder remains'
    [void]$PassedCases.Add('fill_leftover')
}

$Total = $PassedCases.Count
$ExpectedTotal = if ($Case -eq 'all') { 10 } else { 1 }
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
