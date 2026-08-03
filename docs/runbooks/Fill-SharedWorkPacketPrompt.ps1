[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateSet('executor', 'reviewer')]
    [string]$Role,

    [Parameter(Mandatory)]
    [ValidateRange(1, [int]::MaxValue)]
    [int]$IssueNumber,

    [Parameter(Mandatory)]
    [string]$BaseSha,

    [string]$HeadSha,

    [string]$IssueUrl,

    [ValidateRange(1, [int]::MaxValue)]
    [int]$Generation = 1,

    [string]$Branch,

    [string]$Worktree,

    [string]$RepoPath,

    [string]$TemplateRoot,

    [string]$OutputPath,

    [switch]$NoClipboard
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$OutputEncoding = $Utf8NoBom
[Console]::OutputEncoding = $Utf8NoBom

function Assert-FullSha {
    param(
        [Parameter(Mandatory)]
        [string]$Name,

        [Parameter(Mandatory)]
        [string]$Value
    )

    if ($Value -notmatch '^[0-9a-fA-F]{40}$') {
        throw "$Name phải là SHA đủ 40 ký tự hex: $Value"
    }
    return $Value.ToLowerInvariant()
}

function ConvertTo-PowerShellSingleQuotedLiteral {
    param(
        [Parameter(Mandatory)]
        [string]$Value
    )

    return "'" + $Value.Replace("'", "''") + "'"
}

function ConvertTo-AsciiSafeJson {
    param(
        [Parameter(Mandatory)]
        [string]$Json
    )

    return [regex]::Replace(
        $Json,
        '[^\x00-\x7F]',
        { param($Match) '\u{0:x4}' -f [int][char]$Match.Value[0] }
    )
}

$BaseSha = Assert-FullSha -Name 'BaseSha' -Value $BaseSha
if ($Role -eq 'reviewer') {
    if ([string]::IsNullOrWhiteSpace($HeadSha)) {
        throw 'Reviewer bắt buộc có -HeadSha từ REVIEW_READY mới nhất.'
    }
    $HeadSha = Assert-FullSha -Name 'HeadSha' -Value $HeadSha
}

if ([string]::IsNullOrWhiteSpace($IssueUrl)) {
    $IssueUrl = "https://github.com/ducthangho/tra-luat/issues/$IssueNumber"
}
if ($IssueUrl -notmatch "/issues/$IssueNumber/?$") {
    throw "IssueUrl không khớp IssueNumber ${IssueNumber}: $IssueUrl"
}

if ([string]::IsNullOrWhiteSpace($TemplateRoot)) {
    $TemplateRoot = [System.IO.Path]::GetFullPath(
        (Join-Path $PSScriptRoot '..\prompts')
    )
}
if (-not (Test-Path -LiteralPath $TemplateRoot -PathType Container)) {
    throw "Không thấy thư mục template: $TemplateRoot"
}

if ([string]::IsNullOrWhiteSpace($RepoPath)) {
    $RepoPath = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
}
else {
    $RepoPath = [System.IO.Path]::GetFullPath($RepoPath)
}

$ExpectedBranch = "agent/wp$IssueNumber-g$Generation-codex"
if ([string]::IsNullOrWhiteSpace($Branch)) {
    $Branch = $ExpectedBranch
}
elseif ($Branch -cne $ExpectedBranch) {
    throw "INVALID_BRANCH: Branch phải khớp protocol packet: $ExpectedBranch"
}

if ([string]::IsNullOrWhiteSpace($Worktree)) {
    $RepoParent = Split-Path -Parent $RepoPath
    $RepoName = Split-Path -Leaf $RepoPath
    if ($Role -eq 'executor') {
        $Worktree = Join-Path $RepoParent "$RepoName-wt\wp$IssueNumber-codex"
    }
    else {
        $Worktree = Join-Path $RepoParent "$RepoName-review-wp$IssueNumber"
    }
}
$Worktree = [System.IO.Path]::GetFullPath($Worktree)
$WorktreeForPrompt = if ($Role -eq 'reviewer') {
    $Worktree.Replace('\', '/')
}
else {
    $Worktree
}

$TemplateName = if ($Role -eq 'executor') {
    'CODEX_EXECUTOR_D0.md'
}
else {
    'CLAUDE_REVIEWER_D0.md'
}
$TemplatePath = Join-Path $TemplateRoot $TemplateName
if (-not (Test-Path -LiteralPath $TemplatePath -PathType Leaf)) {
    throw "Không thấy template: $TemplatePath"
}
$PromptText = [System.IO.File]::ReadAllText($TemplatePath)

$ReplacementMap = [ordered]@{
    '{{ISSUE_URL}}'       = $IssueUrl
    '{{ISSUE_NUMBER}}'    = [string]$IssueNumber
    '{{BASE_SHA}}'        = $BaseSha
    '{{PACKET_ID}}'       = "wp$IssueNumber"
    '{{GENERATION}}'      = [string]$Generation
    '{{BRANCH}}'          = $Branch
    '{{REPO_PATH_PS}}'    = $RepoPath.Replace("'", "''")
    '{{WORKTREE}}'        = $WorktreeForPrompt
    '{{REVIEW_WORKTREE}}' = $WorktreeForPrompt
    '{{HEAD_SHA}}'        = $HeadSha
}
foreach ($Token in $ReplacementMap.Keys) {
    $Value = $ReplacementMap[$Token]
    if (-not [string]::IsNullOrWhiteSpace($Value)) {
        $PromptText = $PromptText.Replace($Token, $Value)
    }
}

$LeftoverTokens = @(
    [regex]::Matches($PromptText, '\{\{[^{}]*\}\}') |
    ForEach-Object { $_.Value } |
    Sort-Object -Unique
)
if ($LeftoverTokens.Count -gt 0) {
    throw "Còn placeholder chưa điền: $($LeftoverTokens -join ', ')"
}

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path ([System.IO.Path]::GetTempPath()) (
        "PROMPT_wp$IssueNumber-$Role-" + [Guid]::NewGuid().ToString('N') + '.md'
    )
}
$OutputPath = [System.IO.Path]::GetFullPath($OutputPath)
if (Test-Path -LiteralPath $OutputPath) {
    throw "Output đã tồn tại, không ghi đè: $OutputPath"
}
$OutputParent = Split-Path -Parent $OutputPath
if (-not (Test-Path -LiteralPath $OutputParent -PathType Container)) {
    throw "Thư mục output không tồn tại: $OutputParent"
}

[System.IO.File]::WriteAllText($OutputPath, $PromptText, $Utf8NoBom)

$ClipboardStatus = 'disabled'
if (-not $NoClipboard) {
    if (Get-Command Set-Clipboard -ErrorAction SilentlyContinue) {
        try {
            Set-Clipboard -Value $PromptText
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

$ReviewSetupCommands = @()
if ($Role -eq 'reviewer') {
    $RepoLiteral = ConvertTo-PowerShellSingleQuotedLiteral -Value $RepoPath
    $BranchLiteral = ConvertTo-PowerShellSingleQuotedLiteral -Value $Branch
    $WorktreeLiteral = ConvertTo-PowerShellSingleQuotedLiteral -Value $Worktree
    $HeadLiteral = ConvertTo-PowerShellSingleQuotedLiteral -Value $HeadSha
    $ReviewSetupCommands = @(
        "git -C $RepoLiteral fetch origin $BranchLiteral",
        "git -C $RepoLiteral worktree add --detach $WorktreeLiteral $HeadLiteral"
    )
}

$Summary = [ordered]@{
    ok                 = $true
    role               = $Role
    issue_number       = $IssueNumber
    packet_id          = "wp$IssueNumber"
    generation         = $Generation
    branch             = $Branch
    base_sha           = $BaseSha
    head_sha           = $HeadSha
    worktree           = $Worktree
    prompt_output_path = $OutputPath
    clipboard          = $ClipboardStatus
    review_setup_commands = $ReviewSetupCommands
}
$Json = $Summary | ConvertTo-Json -Compress
[Console]::WriteLine((ConvertTo-AsciiSafeJson -Json $Json))
