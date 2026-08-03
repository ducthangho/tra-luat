[CmdletBinding()]
param(
    [string]$RepoPath,

    [string]$SnapshotPath,

    [string]$BodyOutputPath,

    [string]$GitCommand = 'git',

    [string]$GhCommand = 'gh',

    [switch]$DryRun,

    [switch]$NoClipboard
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ExpectedD0SourceFiles = @(
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

function Assert-D0SourceInventory {
    param(
        [Parameter(Mandatory)]
        [string[]]$SourceFiles,

        [string]$SourceRoot
    )

    $Normalized = @($SourceFiles | ForEach-Object { $_.Replace('\', '/') })
    if ($Normalized.Count -ne 23) {
        throw "Đếm nguồn D0 = $($Normalized.Count), kỳ vọng đúng 23 — DỪNG trước khi tạo Issue."
    }
    if (@($Normalized | Select-Object -Unique).Count -ne $Normalized.Count) {
        throw 'Write-set D0 có đường dẫn trùng — DỪNG trước khi tạo Issue.'
    }

    $ExpectedSorted = @($ExpectedD0SourceFiles | Sort-Object)
    $ActualSorted = @($Normalized | Sort-Object)
    if (($ExpectedSorted -join "`n") -ne ($ActualSorted -join "`n")) {
        $MissingExpected = @($ExpectedSorted | Where-Object { $_ -notin $ActualSorted })
        $Unexpected = @($ActualSorted | Where-Object { $_ -notin $ExpectedSorted })
        throw "Write-set D0 lệch allowlist. Thiếu: $($MissingExpected -join ', '). Ngoài dự kiến: $($Unexpected -join ', ')."
    }

    if (-not [string]::IsNullOrWhiteSpace($SourceRoot)) {
        $MissingOnDisk = @(
            $Normalized | Where-Object {
                -not (Test-Path -LiteralPath (Join-Path $SourceRoot $_) -PathType Leaf)
            }
        )
        if ($MissingOnDisk.Count -gt 0) {
            throw "Thiếu nguồn D0 trong cây canonical: $($MissingOnDisk -join ', ')"
        }
    }

    return $Normalized
}

function Assert-D0SourceStatus {
    param(
        [Parameter(Mandatory)]
        [string[]]$StatusLines,

        [Parameter(Mandatory)]
        [string[]]$SourceFiles
    )

    if ($StatusLines.Count -ne $SourceFiles.Count) {
        throw "source_status có $($StatusLines.Count) đường bẩn, kỳ vọng $($SourceFiles.Count); mọi nguồn D0 phải là M hoặc ??."
    }

    $DirtyPaths = [System.Collections.Generic.List[string]]::new()
    $NormalizedStatus = [System.Collections.Generic.List[string]]::new()
    foreach ($Line in $StatusLines) {
        if ([string]::IsNullOrWhiteSpace($Line) -or $Line.Length -lt 4) {
            throw "source_status không hợp lệ: $Line"
        }
        $Code = $Line.Substring(0, 2)
        if ($Code -notin @('??', ' M', 'M ', 'MM')) {
            throw "source_status chỉ chấp nhận modified/untracked, nhận '$Code': $Line"
        }
        $RelativePath = $Line.Substring(3).Replace('\', '/')
        if ($RelativePath.Contains(' -> ')) {
            throw "source_status không chấp nhận rename: $Line"
        }
        [void]$DirtyPaths.Add($RelativePath)
        [void]$NormalizedStatus.Add("$Code $RelativePath")
    }

    $ExpectedSorted = @($SourceFiles | Sort-Object)
    $DirtySorted = @($DirtyPaths | Sort-Object)
    if (($ExpectedSorted -join "`n") -ne ($DirtySorted -join "`n")) {
        throw 'source_status không phủ đúng toàn bộ 23 đường D0; có nguồn sạch, thiếu hoặc ngoài allowlist.'
    }

    return @($NormalizedStatus)
}

if ([string]::IsNullOrWhiteSpace($RepoPath)) {
    $RepoPath = [System.IO.Path]::GetFullPath(
        (Join-Path $PSScriptRoot '..\..')
    )
}

if ([string]::IsNullOrWhiteSpace($BodyOutputPath)) {
    $BodyOutputPath = Join-Path ([System.IO.Path]::GetTempPath()) (
        'wp-d0-' + [Guid]::NewGuid().ToString('N') + '.md'
    )
}
$BodyOutputPath = [System.IO.Path]::GetFullPath($BodyOutputPath)
if (Test-Path -LiteralPath $BodyOutputPath) {
    throw "Body output already exists: $BodyOutputPath"
}
$BodyParent = Split-Path -Parent $BodyOutputPath
if (-not (Test-Path -LiteralPath $BodyParent -PathType Container)) {
    throw "Body output directory does not exist: $BodyParent"
}

if (-not [string]::IsNullOrWhiteSpace($SnapshotPath)) {
    if (-not $DryRun) {
        throw 'Snapshot mode is preview-only and requires -DryRun.'
    }
    if (-not (Test-Path -LiteralPath $SnapshotPath -PathType Leaf)) {
        throw "Snapshot file does not exist: $SnapshotPath"
    }
    $Snapshot = Get-Content -LiteralPath $SnapshotPath -Raw | ConvertFrom-Json
    if (-not ($Snapshot.PSObject.Properties.Name -contains 'source_files')) {
        throw 'Snapshot thiếu source_files; không thể xác minh write-set D0.'
    }
    $SourceFiles = @(Assert-D0SourceInventory -SourceFiles @($Snapshot.source_files))
    if (-not ($Snapshot.PSObject.Properties.Name -contains 'source_status')) {
        throw 'Snapshot thiếu source_status; không thể chứng minh 23 nguồn canonical đều đang M/untracked.'
    }
    $SourceStatus = @(
        Assert-D0SourceStatus -StatusLines @($Snapshot.source_status) -SourceFiles $SourceFiles
    )
}
else {
    if (-not (Get-Command $GitCommand -ErrorAction SilentlyContinue)) {
        throw "Không tìm thấy git command: $GitCommand"
    }
    if (-not (Get-Command $GhCommand -ErrorAction SilentlyContinue)) {
        throw "Không tìm thấy GitHub CLI command: $GhCommand"
    }
    if (-not (Test-Path -LiteralPath $RepoPath -PathType Container)) {
        throw "Repository directory does not exist: $RepoPath"
    }
    $RepoPath = (Resolve-Path -LiteralPath $RepoPath).Path

    $GitTop = ((& $GitCommand -C $RepoPath rev-parse --show-toplevel 2>&1) | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "Not a Git repository: $RepoPath`n$GitTop"
    }
    $CanonicalTop = [System.IO.Path]::GetFullPath($GitTop).TrimEnd([char]'\', [char]'/')
    $ResolvedRepoPath = [System.IO.Path]::GetFullPath($RepoPath).TrimEnd([char]'\', [char]'/')
    if (-not $CanonicalTop.Equals(
            $ResolvedRepoPath,
            [System.StringComparison]::OrdinalIgnoreCase
        )) {
        throw "RepoPath phải là đúng root của cây canonical, nhận: $RepoPath; git top: $GitTop"
    }

    $AuthOutput = ((& $GhCommand auth status 2>&1) | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "GitHub CLI chưa đăng nhập. Hãy chạy: gh auth login`n$AuthOutput"
    }

    $FetchOutput = ((& $GitCommand -C $RepoPath fetch origin --prune 2>&1) | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "Không fetch được origin; không dùng ref cũ để tạo packet.`n$FetchOutput"
    }

    $BaseSha = ((& $GitCommand -C $RepoPath rev-parse origin/master 2>&1) | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($BaseSha)) {
        throw 'Không lấy được SHA của origin/master.'
    }

    $Version = ((& $GitCommand -C $RepoPath show 'origin/master:VERSION' 2>&1) | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($Version)) {
        throw 'Không đọc được VERSION từ origin/master.'
    }

    Push-Location -LiteralPath $RepoPath
    try {
        $RepoInfoJson = ((& $GhCommand repo view --json nameWithOwner 2>&1) | Out-String).Trim()
        $RepoInfoExitCode = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }
    if ($RepoInfoExitCode -ne 0) {
        throw "Không xác định được GitHub repository.`n$RepoInfoJson"
    }
    $RepoSlug = ($RepoInfoJson | ConvertFrom-Json).nameWithOwner

    $OpenPrJson = ((& $GhCommand pr list --repo $RepoSlug --state open --limit 100 `
        --json number,title,headRefName,url 2>&1) | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "Không kiểm được danh sách PR đang mở.`n$OpenPrJson"
    }

    if ($OpenPrJson.Trim() -eq '[]') {
        $LiveOpenPrs = @()
    }
    else {
        $LiveOpenPrs = @($OpenPrJson | ConvertFrom-Json)
    }

    $SourceFiles = @(
        Assert-D0SourceInventory -SourceFiles $ExpectedD0SourceFiles -SourceRoot $RepoPath
    )
    $StatusArgs = @(
        '-C', $RepoPath, 'status', '--porcelain=v1', '--untracked-files=all', '--'
    ) + $SourceFiles
    $RawSourceStatus = @(& $GitCommand @StatusArgs 2>&1)
    if ($LASTEXITCODE -ne 0) {
        throw "Không đo được source_status của 23 nguồn D0: $($RawSourceStatus -join "`n")"
    }
    $SourceStatus = @(
        Assert-D0SourceStatus -StatusLines $RawSourceStatus -SourceFiles $SourceFiles
    )
    $Snapshot = [pscustomobject]@{
        repo_slug    = $RepoSlug
        base_sha     = $BaseSha
        version      = $Version
        observed_at  = [DateTime]::UtcNow.ToString("yyyy-MM-dd'T'HH:mm:ss'Z'")
        open_prs     = $LiveOpenPrs
        source_files = $SourceFiles
        source_status = $SourceStatus
    }
}

$OpenPrs = @($Snapshot.open_prs)

if ($OpenPrs.Count -eq 0) {
    $PacketStatus = 'ready_for_claim'
    $OpenPrLines = @('- Không có PR mở tại observed_at; vẫn phải đo lại lúc claim.')
}
else {
    $PacketStatus = 'PAUSE_OPEN_PR'
    $OpenPrLines = @(
        $OpenPrs | ForEach-Object {
            "- #$($_.number) — $($_.title) — branch: $($_.headRefName) — $($_.url)"
        }
    )
}

$IssueNumberToken = '{{ISSUE_NUMBER}}'
$PacketId = "wp$IssueNumberToken"
$Branch = "agent/wp$IssueNumberToken-g1-codex"
$SourceStatusByPath = @{}
foreach ($StatusLine in $SourceStatus) {
    $SourceStatusByPath[$StatusLine.Substring(3)] = $StatusLine.Substring(0, 2)
}
$FileLines = @(
    $SourceFiles | Sort-Object | ForEach-Object {
        '- `' + $_ + '` — source_status: `' + $SourceStatusByPath[$_] + '`'
    }
)

$BodyLines = @(
    "# Work Packet — $PacketId (alias: wp-d0-protocol-constitution)",
    '',
    '## 1. Định danh',
    '',
    '- Mission: protocol-da-phien',
    '- Generation: 1',
    '- Planned executor: codex',
    '- Cross-provider reviewer: claude',
    "- Status: $PacketStatus",
    "- Repository: $($Snapshot.repo_slug)",
    ("- Executor branch: ``$Branch``"),
    '',
    '## 2. Snapshot khi tạo packet — không phải chân lý lâu dài',
    '',
    "- observed_at: $($Snapshot.observed_at)",
    '- base_ref: origin/master',
    "- base_sha_observed: $($Snapshot.base_sha)",
    "- VERSION tại base: $($Snapshot.version)",
    "- open_pr_count: $($OpenPrs.Count)",
    ''
)
$BodyLines += $OpenPrLines
$BodyLines += @(
    '',
    'Mọi dữ liệu trong mục này phải được kiểm lại khi claim và ngay trước khi mở PR/land.',
    'Base/quyền sở hữu lệch snapshot thì `PAUSE`; không âm thầm rebase hoặc giả định cửa sổ 0-PR còn mở.',
    '',
    '## 3. Mục tiêu',
    '',
    'Land D0 — bộ hiến pháp docs-only của protocol đa phiên theo:',
    '',
    '- `docs/PROTOCOL_DA_PHIEN.md`;',
    '- `docs/KE_HOACH_TRIEN_KHAI_PROTOCOL_DA_PHIEN.md`;',
    '- ADR-0026 v3;',
    '- ADR-0017 đến ADR-0033.',
    '',
    'D0 làm rõ ADR-0001 đã bị ADR-0017 thay thế nhưng chưa kích hoạt runtime protocol mới.',
    'Một PR vào `master`; KHÔNG version, KHÔNG rNNN, KHÔNG manifest.',
    '',
    'Prompt dùng chung:',
    '',
    '- Executor: `docs/prompts/CODEX_EXECUTOR_D0.md`;',
    '- Reviewer: `docs/prompts/CLAUDE_REVIEWER_D0.md`.',
    '',
    '## 3A. Nguồn nội dung',
    '',
    'Các tệp D0 hiện là tệp untracked/M trong cây canonical. Cây canonical đang bẩn chỉ là nguồn đọc;',
    'executor phải COPY BYTE NGUYÊN VẸN đúng từng tệp vào worktree sạch rồi mới áp chỉnh sửa cuối.',
    'Không stage từ cây canonical và không mang tệp bẩn của phiên khác.',
    '',
    '## 4. Write-set (ĐÍCH DANH, 23 đường)',
    ''
)
$BodyLines += $FileLines
$BodyLines += @(
    '',
    'Issue này thắng prompt nếu danh sách tĩnh trong prompt lệch. Sai đúng 23 đường hoặc thiếu nguồn',
    'thì `PAUSE`; không tự mở rộng write-set. Các bootstrap artifact đã land trước D0 là chỉ dẫn,',
    'không thuộc write-set D0.',
    '',
    'Trước lần sửa đầu tiên, executor comment `CLAIM` gồm packet, generation, executor,',
    'base SHA, worktree, branch, write-set đã khai triển, thời điểm claim và lease expiry.',
    '',
    'Tệp ngoài write-set bị cấm, kể cả tệp đã bẩn từ phiên khác.',
    '',
    '## 5. Ngoài phạm vi',
    '',
    '- Không sửa `VERSION` hoặc cấp số `rNNN`/version mới.',
    '- Không sửa `CHANGELOG.md`, `SKILL.md`, manifest hoặc runtime.',
    '- Không sinh release metadata.',
    '- Không merge, deploy hoặc re-import.',
    '- Không mang tệp bẩn ngoài write-set vào commit.',
    '- Không `git add -A`/`-u`; chỉ stage đích danh 23 đường.',
    '- Không formatter hoặc đổi EOL ngoài chỉnh sửa nội dung cần thiết.',
    '- Không cấp credential Drive/GAS/LIVE cho worker hay CI.',
    '- Reviewer không sửa branch của executor.',
    '',
    '## 6. Năm chỉnh sửa cuối',
    '',
    'a. Mọi số liệu tức thời mang `observed_at` và lệnh đo lại.',
    'b. Rollback F4 chỉ hợp lệ khi chưa packet v1 nào lease/start VÀ chưa durable event hậu cutover.',
    'c. Tuyên bố CRLF/EOL phải gắn mốc đo và chỉ áp dụng cho text file thuộc policy hiện hành.',
    'd. Deploy/re-import Capabilities cần phê duyệt LIVE tường minh theo ADR-0022.',
    'e. T0 có nghiệm thu Claude Remote Control từ Android đến host Windows end-to-end.',
    '',
    'Sau a–e, rà chéo activation nguyên tử F4; integration-head base; credential boundary ADR-0020;',
    'one-executor ADR-0017; journal/inbox ADR-0025/0033; required-check ADR-0031; ratchet ADR-0032.',
    '',
    '## 7. Acceptance criteria',
    '',
    '1. ADR-0001 được đánh dấu `Superseded by ADR-0017` nhất quán.',
    '',
    '2. ADR-0017–0033, PROTOCOL và Kế hoạch không mâu thuẫn về trạng thái hoặc thứ tự',
    '   `D0 → T0 → F1 → F2 → F3 → F4`.',
    '',
    '3. PR, SHA, số worktree và số phát hành chỉ là snapshot có `observed_at`.',
    '',
    '4. Số `rNNN`/version chỉ được chọn phút chót sau khi quét open PR và branch live/unmerged.',
    '',
    '5. Rollback F4 chỉ được phép khi chưa có packet protocol-v1 lease/start và chưa có',
    '   durable-inbox event hậu cutover; nếu đã có thì `PAUSE` và fix-forward.',
    '',
    '6. Phát biểu EOL chỉ áp dụng cho text file thuộc policy đang mang CRLF.',
    '',
    '7. Deploy/re-import là hành động LIVE cần phê duyệt rõ ràng; worker và CI không có',
    '   credential Drive/GAS/LIVE.',
    '',
    '8. T0 nghiệm thu Claude Remote Control Windows → Android end-to-end, gồm login, kết nối,',
    '   ngắt mạng và reconnect.',
    '',
    '9. Required check bundled module chỉ bật nguyên tử tại F4.',
    '',
    '10. Packet sau khi mission tồn tại bắt đầu từ integration head.',
    '',
    '11. D0 là docs-only và không bump VERSION/r/manifest.',
    '',
    '12. 5 cổng JSON offline đều `ok:true`; selftest có marker `[FAIL]` = 0 trên đúng worktree push;',
    '    `git diff --check`, EOL, trailing whitespace và final newline đều đạt.',
    '',
    '## 8. Quy tắc executor',
    '',
    '- Một packet chỉ có một executor ghi.',
    '- Làm trong worktree sạch; không tự mở rộng write-set.',
    '- Base thay đổi trước khi bắt đầu thì cập nhật packet và generation; không âm thầm rebase.',
    '- Có PR mở hoặc write-set conflict thì chuyển `PAUSE`.',
    '- Không merge hoặc deploy.',
    '',
    'Khi xong, executor comment `REVIEW_READY` gồm base/head SHA, branch, commit, changed files,',
    'diffstat, lệnh và kết quả kiểm tra, cùng residual risks.',
    '',
    '## 9. Quy tắc reviewer',
    '',
    '- Claude review read-only đúng head SHA trong `REVIEW_READY`.',
    '- Không Edit/Write/commit/push/merge/deploy.',
    '- Approval cũ hết hiệu lực khi head SHA thay đổi.',
    '- Có lỗi thì trả `changes_requested`.',
    '- Chỉ trả `cross_approved` khi không còn blocking finding.',
    '- Thiếu quyền, quota/token hoặc bằng chứng thì trả `review_deferred`.',
    '',
    '## 10. Khi gần hết token/context',
    '',
    'Ghi `HANDOFF_REQUIRED` gồm role, packet, generation, base/head SHA, việc đã làm, việc còn',
    'lại, lệnh tiếp tục, blocker và evidence. Sau đó `PAUSE`; không tự nhận hoàn thành.',
    '',
    '## 11. Điều kiện được land',
    '',
    '- Đúng write-set và các gate bắt buộc đạt.',
    '- Không còn blocking finding.',
    '- `cross_approved` gắn với đúng head SHA.',
    '- Preflight phút chót xác nhận lại GitHub.',
    '- Integrator có thẩm quyền chủ động land.'
)

$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$Body = ($BodyLines -join "`n") + "`n"
[System.IO.File]::WriteAllText($BodyOutputPath, $Body, $Utf8NoBom)

$IssueUrl = $null
$IssueNumber = $null
if (-not $DryRun) {
    $IssueTitle = '[WP D0] Land hiến pháp docs-only cho protocol đa phiên'
    $IssueOutput = ((& $GhCommand issue create --repo $Snapshot.repo_slug --title $IssueTitle `
        --body-file $BodyOutputPath 2>&1) | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "Không tạo được GitHub Issue. Packet body còn tại: $BodyOutputPath`n$IssueOutput"
    }

    $IssueUrl = @(
        $IssueOutput -split '\s+' |
        Where-Object { $_ -match '^https://github\.com/.+/issues/\d+$' }
    ) | Select-Object -Last 1
    if ([string]::IsNullOrWhiteSpace($IssueUrl) -or $IssueUrl -notmatch '/issues/(\d+)$') {
        throw "GitHub trả thành công nhưng không tìm thấy Issue URL/số Issue. Output: $IssueOutput"
    }

    $IssueNumber = [int]$Matches[1]
    $PacketId = "wp$IssueNumber"
    $Branch = "agent/wp$IssueNumber-g1-codex"
    $FinalBody = $Body.Replace('{{ISSUE_NUMBER}}', [string]$IssueNumber)
    [System.IO.File]::WriteAllText($BodyOutputPath, $FinalBody, $Utf8NoBom)

    $EditOutput = ((& $GhCommand issue edit $IssueNumber --repo $Snapshot.repo_slug `
        --body-file $BodyOutputPath 2>&1) | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "Issue đã tạo tại $IssueUrl nhưng chưa gắn được packet_id thật. Body phục hồi: $BodyOutputPath`n$EditOutput"
    }

    if (-not $NoClipboard -and (Get-Command Set-Clipboard -ErrorAction SilentlyContinue)) {
        Set-Clipboard -Value $IssueUrl
    }
}

[ordered]@{
    ok               = $true
    dry_run          = [bool]$DryRun
    status           = $PacketStatus
    body_output_path = [System.IO.Path]::GetFullPath($BodyOutputPath)
    issue_url         = $IssueUrl
    issue_number      = $IssueNumber
    packet_id         = $PacketId
    branch            = $Branch
    base_sha          = $Snapshot.base_sha
    observed_at       = $Snapshot.observed_at
} | ConvertTo-Json -Compress
