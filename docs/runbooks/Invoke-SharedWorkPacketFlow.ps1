<#
.SYNOPSIS
Runs the D0 shared-work-packet workflow with explicit permission gates.

.DESCRIPTION
Preview measures the canonical source and generates the packet body without
creating a GitHub Issue. CreateExecutor creates one real Issue only when
-ConfirmCreateIssue is present, fills the Codex executor prompt, and normally
copies that prompt to the clipboard. PrepareReviewer fills the SHA-pinned
Claude reviewer prompt, fetches the packet branch, and creates and verifies a
clean detached review worktree.

The controller never pushes, opens or merges a pull request, posts a review
verdict, bumps a version, deploys, or imports LIVE data.

.EXAMPLE
./docs/runbooks/Invoke-SharedWorkPacketFlow.ps1 -Action Preview -CanonicalRepoPath 'D:\Quốc hội\tra-luat'

Measures live state and emits a dry-run JSON result. No Issue is created.

.EXAMPLE
./docs/runbooks/Invoke-SharedWorkPacketFlow.ps1 -Action CreateExecutor -CanonicalRepoPath 'D:\Quốc hội\tra-luat' -ConfirmCreateIssue

Creates the Issue after an explicit permission flag, fills the executor prompt,
and copies the prompt to the clipboard when Set-Clipboard is available.

.EXAMPLE
./docs/runbooks/Invoke-SharedWorkPacketFlow.ps1 -Action PrepareReviewer -CanonicalRepoPath 'D:\Quốc hội\tra-luat' -IssueNumber 123 -BaseSha '<40-hex-base>' -HeadSha '<40-hex-head>' -Branch 'agent/wp123-g1-codex'

Fills the reviewer prompt and prepares a verified detached review worktree.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateSet('Preview', 'CreateExecutor', 'PrepareReviewer')]
    [string]$Action,

    [string]$CanonicalRepoPath,

    [string]$SnapshotPath,

    [string]$BodyOutputPath,

    [ValidateRange(1, [int]::MaxValue)]
    [int]$IssueNumber,

    [string]$BaseSha,

    [string]$HeadSha,

    [string]$IssueUrl,

    [ValidateRange(1, [int]::MaxValue)]
    [int]$Generation = 1,

    [string]$Branch,

    [string]$ExecutorWorktree,

    [string]$ReviewWorktree,

    [string]$PromptOutputPath,

    [string]$GitCommand = 'git',

    [string]$GhCommand = 'gh',

    [switch]$ConfirmCreateIssue,

    [switch]$NoClipboard
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$OutputEncoding = $Utf8NoBom
[Console]::OutputEncoding = $Utf8NoBom

function ConvertTo-AsciiSafeJson {
    param(
        [Parameter(Mandatory)]
        [object]$Value
    )

    $Json = $Value | ConvertTo-Json -Depth 8 -Compress
    return [regex]::Replace(
        $Json,
        '[^\x00-\x7F]',
        { param($Match) '\u{0:x4}' -f [int][char]$Match.Value[0] }
    )
}

function Invoke-PowerShellJsonScript {
    param(
        [Parameter(Mandatory)]
        [string]$ScriptPath,

        [Parameter(Mandatory)]
        [System.Collections.IDictionary]$Arguments,

        [Parameter(Mandatory)]
        [string]$Name
    )

    $PowerShellPath = (Get-Process -Id $PID).Path
    $ArgumentList = [System.Collections.Generic.List[string]]::new()
    [void]$ArgumentList.Add('-NoProfile')
    [void]$ArgumentList.Add('-File')
    [void]$ArgumentList.Add($ScriptPath)
    foreach ($Key in $Arguments.Keys) {
        $Value = $Arguments[$Key]
        if ($Value -is [bool] -or $Value -is [System.Management.Automation.SwitchParameter]) {
            if ([bool]$Value) {
                [void]$ArgumentList.Add("-$Key")
            }
            continue
        }
        if ($null -eq $Value) {
            continue
        }
        [void]$ArgumentList.Add("-$Key")
        [void]$ArgumentList.Add([string]$Value)
    }

    $Text = ((& $PowerShellPath @ArgumentList 2>&1) | Out-String).Trim()
    $ExitCode = $LASTEXITCODE
    if ($ExitCode -ne 0) {
        throw "$Name failed with exit code ${ExitCode}: $Text"
    }
    if ([string]::IsNullOrWhiteSpace($Text)) {
        throw "$Name không trả JSON."
    }
    try {
        return $Text | ConvertFrom-Json
    }
    catch {
        throw "$Name trả output không phải một JSON object: $Text"
    }
}

function Invoke-GitChecked {
    param(
        [Parameter(Mandatory)]
        [string[]]$GitArguments,

        [Parameter(Mandatory)]
        [string]$Description
    )

    $OriginalErrorActionPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = 'Continue'
        $GitOutput = ((& $GitCommand @GitArguments 2>&1) | Out-String).Trim()
        $GitExitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $OriginalErrorActionPreference
    }
    if ($GitExitCode -ne 0) {
        throw "$Description failed with exit code ${GitExitCode}: $GitOutput"
    }
    return $GitOutput
}

$ToolRepoPath = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
if ([string]::IsNullOrWhiteSpace($CanonicalRepoPath)) {
    $CanonicalRepoPath = $ToolRepoPath
}
else {
    $CanonicalRepoPath = [System.IO.Path]::GetFullPath($CanonicalRepoPath)
}

$NewPacketScript = Join-Path $PSScriptRoot 'New-SharedWorkPacket.ps1'
$FillerScript = Join-Path $PSScriptRoot 'Fill-SharedWorkPacketPrompt.ps1'
foreach ($RequiredScript in @($NewPacketScript, $FillerScript)) {
    if (-not (Test-Path -LiteralPath $RequiredScript -PathType Leaf)) {
        throw "Thiếu runbook bắt buộc: $RequiredScript"
    }
}

switch ($Action) {
    'Preview' {
        $PacketArguments = @{
            RepoPath   = $CanonicalRepoPath
            GitCommand = $GitCommand
            GhCommand  = $GhCommand
            DryRun     = $true
            NoClipboard = $true
        }
        if (-not [string]::IsNullOrWhiteSpace($SnapshotPath)) {
            $PacketArguments.SnapshotPath = $SnapshotPath
        }
        if (-not [string]::IsNullOrWhiteSpace($BodyOutputPath)) {
            $PacketArguments.BodyOutputPath = $BodyOutputPath
        }

        $Packet = Invoke-PowerShellJsonScript `
            -Name 'New-SharedWorkPacket.ps1' `
            -ScriptPath $NewPacketScript `
            -Arguments $PacketArguments

        $Result = [ordered]@{
            ok                    = [bool]$Packet.ok
            action                = 'Preview'
            dry_run               = $true
            status                = $Packet.status
            body_output_path      = $Packet.body_output_path
            issue_url             = $Packet.issue_url
            issue_number          = $Packet.issue_number
            packet_id             = $Packet.packet_id
            branch                = $Packet.branch
            base_sha              = $Packet.base_sha
            observed_at           = $Packet.observed_at
            bootstrap_ready       = [bool]$Packet.bootstrap_ready
            bootstrap_missing     = @($Packet.bootstrap_missing)
            next_action           = 'CreateExecutor'
            issue_creation_gated  = $true
        }
        [Console]::WriteLine((ConvertTo-AsciiSafeJson -Value $Result))
    }

    'CreateExecutor' {
        if (-not $ConfirmCreateIssue) {
            throw 'CreateExecutor creates a real GitHub Issue. Re-run only with explicit -ConfirmCreateIssue permission.'
        }
        if (-not [string]::IsNullOrWhiteSpace($SnapshotPath)) {
            throw 'CreateExecutor cannot use -SnapshotPath because snapshots are preview-only.'
        }

        $PacketArguments = @{
            RepoPath    = $CanonicalRepoPath
            GitCommand  = $GitCommand
            GhCommand   = $GhCommand
            NoClipboard = $true
        }
        if (-not [string]::IsNullOrWhiteSpace($BodyOutputPath)) {
            $PacketArguments.BodyOutputPath = $BodyOutputPath
        }
        $Packet = Invoke-PowerShellJsonScript `
            -Name 'New-SharedWorkPacket.ps1' `
            -ScriptPath $NewPacketScript `
            -Arguments $PacketArguments

        $Prompt = $null
        if ($Packet.status -eq 'ready_for_claim') {
            $FillerArguments = @{
                Role          = 'executor'
                IssueNumber   = [int]$Packet.issue_number
                BaseSha       = [string]$Packet.base_sha
                IssueUrl      = [string]$Packet.issue_url
                Generation    = 1
                Branch        = [string]$Packet.branch
                RepoPath      = $CanonicalRepoPath
                NoClipboard   = [bool]$NoClipboard
            }
            if (-not [string]::IsNullOrWhiteSpace($ExecutorWorktree)) {
                $FillerArguments.Worktree = $ExecutorWorktree
            }
            if (-not [string]::IsNullOrWhiteSpace($PromptOutputPath)) {
                $FillerArguments.OutputPath = $PromptOutputPath
            }

            try {
                $Prompt = Invoke-PowerShellJsonScript `
                    -Name 'Fill-SharedWorkPacketPrompt.ps1' `
                    -ScriptPath $FillerScript `
                    -Arguments $FillerArguments
            }
            catch {
                $FillerError = $_.Exception.Message
                throw ("Issue was created at {0}, but the executor prompt failed. Recover with Fill-SharedWorkPacketPrompt.ps1. Filler error: {1}" -f `
                    $Packet.issue_url,
                    $FillerError)
            }
        }

        $Result = [ordered]@{
            ok                    = [bool]$Packet.ok
            action                = 'CreateExecutor'
            dry_run               = $false
            status                = $Packet.status
            body_output_path      = $Packet.body_output_path
            issue_url             = $Packet.issue_url
            issue_number          = $Packet.issue_number
            packet_id             = $Packet.packet_id
            branch                = $Packet.branch
            base_sha              = $Packet.base_sha
            observed_at           = $Packet.observed_at
            executor_worktree     = if ($null -eq $Prompt) { $null } else { $Prompt.worktree }
            executor_prompt_path  = if ($null -eq $Prompt) { $null } else { $Prompt.prompt_output_path }
            clipboard             = if ($null -eq $Prompt) { 'not_filled_packet_paused' } else { $Prompt.clipboard }
            next_action           = if ($null -eq $Prompt) { 'Resolve packet pause before executor claim.' } else { 'Paste the filled prompt into a new Codex task.' }
            issue_creation_gated  = $true
        }
        [Console]::WriteLine((ConvertTo-AsciiSafeJson -Value $Result))
    }

    'PrepareReviewer' {
        if ($IssueNumber -lt 1) {
            throw 'PrepareReviewer requires -IssueNumber.'
        }
        if ([string]::IsNullOrWhiteSpace($BaseSha)) {
            throw 'PrepareReviewer requires -BaseSha.'
        }
        if ([string]::IsNullOrWhiteSpace($HeadSha)) {
            throw 'PrepareReviewer requires -HeadSha from the latest REVIEW_READY.'
        }
        if (-not (Test-Path -LiteralPath $CanonicalRepoPath -PathType Container)) {
            throw "Repository does not exist: $CanonicalRepoPath"
        }
        if (-not (Get-Command $GitCommand -ErrorAction SilentlyContinue)) {
            throw "Git command not found: $GitCommand"
        }

        if ([string]::IsNullOrWhiteSpace($ReviewWorktree)) {
            $RepoParent = Split-Path -Parent $CanonicalRepoPath
            $RepoName = Split-Path -Leaf $CanonicalRepoPath
            $ReviewWorktree = Join-Path $RepoParent "$RepoName-review-wp$IssueNumber"
        }
        $ReviewWorktree = [System.IO.Path]::GetFullPath($ReviewWorktree)
        if (Test-Path -LiteralPath $ReviewWorktree) {
            throw "Review worktree path already exists; refusing to overwrite it: $ReviewWorktree"
        }

        $FillerArguments = @{
            Role          = 'reviewer'
            IssueNumber   = $IssueNumber
            BaseSha       = $BaseSha
            HeadSha       = $HeadSha
            Generation    = $Generation
            Worktree      = $ReviewWorktree
            RepoPath      = $CanonicalRepoPath
            NoClipboard   = $true
        }
        if (-not [string]::IsNullOrWhiteSpace($IssueUrl)) {
            $FillerArguments.IssueUrl = $IssueUrl
        }
        if (-not [string]::IsNullOrWhiteSpace($Branch)) {
            $FillerArguments.Branch = $Branch
        }
        if (-not [string]::IsNullOrWhiteSpace($PromptOutputPath)) {
            $FillerArguments.OutputPath = $PromptOutputPath
        }

        $Prompt = Invoke-PowerShellJsonScript `
            -Name 'Fill-SharedWorkPacketPrompt.ps1' `
            -ScriptPath $FillerScript `
            -Arguments $FillerArguments

        [void](Invoke-GitChecked `
            -Description 'Fetch packet branch' `
            -GitArguments @('-C', $CanonicalRepoPath, 'fetch', 'origin', [string]$Prompt.branch))
        $FetchedHead = Invoke-GitChecked `
            -Description 'Resolve fetched packet branch head' `
            -GitArguments @('-C', $CanonicalRepoPath, 'rev-parse', 'FETCH_HEAD')
        if ($FetchedHead -cne [string]$Prompt.head_sha) {
            throw "FETCH_HEAD moved: REVIEW_READY requested $($Prompt.head_sha), but fetched branch $($Prompt.branch) is $FetchedHead. Obtain the latest REVIEW_READY before review."
        }
        [void](Invoke-GitChecked `
            -Description 'Verify base is an ancestor of review head' `
            -GitArguments @('-C', $CanonicalRepoPath, 'merge-base', '--is-ancestor', [string]$Prompt.base_sha, [string]$Prompt.head_sha))
        [void](Invoke-GitChecked `
            -Description 'Create detached review worktree' `
            -GitArguments @('-C', $CanonicalRepoPath, 'worktree', 'add', '--detach', $ReviewWorktree, [string]$Prompt.head_sha))

        $MeasuredHead = Invoke-GitChecked `
            -Description 'Verify review worktree head' `
            -GitArguments @('-C', $ReviewWorktree, 'rev-parse', 'HEAD')
        if ($MeasuredHead -cne [string]$Prompt.head_sha) {
            throw "Review worktree HEAD mismatch: expected $($Prompt.head_sha), got $MeasuredHead"
        }
        $MeasuredBranch = Invoke-GitChecked `
            -Description 'Verify detached review worktree' `
            -GitArguments @('-C', $ReviewWorktree, 'branch', '--show-current')
        if (-not [string]::IsNullOrWhiteSpace($MeasuredBranch)) {
            throw "Review worktree is not detached: $MeasuredBranch"
        }
        $MeasuredStatus = Invoke-GitChecked `
            -Description 'Verify clean review worktree' `
            -GitArguments @('-C', $ReviewWorktree, 'status', '--short')
        if (-not [string]::IsNullOrWhiteSpace($MeasuredStatus)) {
            throw "Review worktree is dirty: $MeasuredStatus"
        }

        $ClipboardStatus = 'disabled'
        if (-not $NoClipboard) {
            if (Get-Command Set-Clipboard -ErrorAction SilentlyContinue) {
                try {
                    Set-Clipboard -Value ([System.IO.File]::ReadAllText(
                        [string]$Prompt.prompt_output_path
                    ))
                    $ClipboardStatus = 'copied'
                }
                catch {
                    $ClipboardStatus = 'failed'
                }
            }
            else {
                $ClipboardStatus = 'unavailable'
            }
        }

        $Result = [ordered]@{
            ok                    = $true
            action                = 'PrepareReviewer'
            issue_number          = $Prompt.issue_number
            packet_id             = $Prompt.packet_id
            generation            = $Prompt.generation
            branch                = $Prompt.branch
            base_sha              = $Prompt.base_sha
            head_sha              = $Prompt.head_sha
            review_worktree       = $ReviewWorktree
            reviewer_prompt_path  = $Prompt.prompt_output_path
            clipboard             = $ClipboardStatus
            setup_completed       = $true
            review_setup_commands = @($Prompt.review_setup_commands)
            next_action           = 'Open a fresh Claude Code session and paste the filled reviewer prompt.'
            automatic_merge       = $false
            automatic_deploy      = $false
        }
        [Console]::WriteLine((ConvertTo-AsciiSafeJson -Value $Result))
    }

    default {
        throw "Action $Action chưa được triển khai."
    }
}
