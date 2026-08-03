[CmdletBinding()]
param(
    [string]$RepoPath = [System.IO.Path]::GetFullPath(
        (Join-Path $PSScriptRoot '..\..')
    ),

    [string]$SnapshotPath,

    [string]$BodyOutputPath,

    [switch]$DryRun,

    [switch]$NoClipboard
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

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
}
else {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        throw 'Không tìm thấy git trong PATH.'
    }
    if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
        throw 'Không tìm thấy GitHub CLI (gh) trong PATH.'
    }
    if (-not (Test-Path -LiteralPath $RepoPath -PathType Container)) {
        throw "Repository directory does not exist: $RepoPath"
    }
    $RepoPath = (Resolve-Path -LiteralPath $RepoPath).Path

    $GitTop = ((& git -C $RepoPath rev-parse --show-toplevel 2>&1) | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "Not a Git repository: $RepoPath`n$GitTop"
    }

    $AuthOutput = ((& gh auth status 2>&1) | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "GitHub CLI chưa đăng nhập. Hãy chạy: gh auth login`n$AuthOutput"
    }

    $FetchOutput = ((& git -C $RepoPath fetch origin --prune 2>&1) | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "Không fetch được origin; không dùng ref cũ để tạo packet.`n$FetchOutput"
    }

    $BaseSha = ((& git -C $RepoPath rev-parse origin/master 2>&1) | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($BaseSha)) {
        throw 'Không lấy được SHA của origin/master.'
    }

    $Version = ((& git -C $RepoPath show 'origin/master:VERSION' 2>&1) | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($Version)) {
        throw 'Không đọc được VERSION từ origin/master.'
    }

    Push-Location -LiteralPath $RepoPath
    try {
        $RepoInfoJson = ((& gh repo view --json nameWithOwner 2>&1) | Out-String).Trim()
        $RepoInfoExitCode = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }
    if ($RepoInfoExitCode -ne 0) {
        throw "Không xác định được GitHub repository.`n$RepoInfoJson"
    }
    $RepoSlug = ($RepoInfoJson | ConvertFrom-Json).nameWithOwner

    $OpenPrJson = ((& gh pr list --repo $RepoSlug --state open --limit 100 `
        --json number,title,headRefName,url 2>&1) | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "Không kiểm được danh sách PR đang mở.`n$OpenPrJson"
    }

    $Snapshot = [pscustomobject]@{
        repo_slug   = $RepoSlug
        base_sha    = $BaseSha
        version     = $Version
        observed_at = (Get-Date).ToString('yyyy-MM-ddTHH:mm:sszzz')
        open_prs    = @($OpenPrJson | ConvertFrom-Json)
    }
}

$OpenPrs = @($Snapshot.open_prs)

if ($OpenPrs.Count -eq 0) {
    $PacketStatus = 'ready_for_claim'
    $OpenPrLines = @('- Không có PR mở tại thời điểm quan sát.')
}
else {
    $PacketStatus = 'PAUSE_OPEN_PR'
    $OpenPrLines = @(
        $OpenPrs | ForEach-Object {
            "- #$($_.number) — $($_.title) — branch: $($_.headRefName) — $($_.url)"
        }
    )
}

$BodyLines = @(
    '# Work packet: wp-d0-protocol-constitution',
    '',
    '## 1. Định danh',
    '',
    '- Mission: protocol-da-phien',
    '- Generation: 1',
    '- Planned executor: codex',
    '- Cross-provider reviewer: claude',
    "- Status: $PacketStatus",
    "- Repository: $($Snapshot.repo_slug)",
    '',
    '## 2. Snapshot khi tạo packet — không phải chân lý lâu dài',
    '',
    "- observed_at: $($Snapshot.observed_at)",
    '- base_ref: origin/master',
    "- base_sha: $($Snapshot.base_sha)",
    "- VERSION tại base: $($Snapshot.version)",
    "- open_pr_count: $($OpenPrs.Count)",
    ''
)
$BodyLines += $OpenPrLines
$BodyLines += @(
    '',
    'Mọi dữ liệu trong mục này phải được kiểm lại khi claim và ngay trước khi land.',
    'Không được giả định cửa sổ zero-open-PR vẫn còn mở.',
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
    '',
    'Prompt dùng chung:',
    '',
    '- Executor: `docs/prompts/CODEX_EXECUTOR_D0.md`;',
    '- Reviewer: `docs/prompts/CLAUDE_REVIEWER_D0.md`.',
    '',
    '## 4. Write-set',
    '',
    'Chỉ sửa các đường dẫn D0-01 liệt kê trong `docs/KE_HOACH_TRIEN_KHAI_PROTOCOL_DA_PHIEN.md`,',
    'cùng ba bootstrap artifact của packet này:',
    '',
    '- `docs/runbooks/New-SharedWorkPacket.ps1`;',
    '- `docs/prompts/CODEX_EXECUTOR_D0.md`;',
    '- `docs/prompts/CLAUDE_REVIEWER_D0.md`;',
    '- `docs/runbooks/tests/Test-NewSharedWorkPacket.ps1`.',
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
    '- Reviewer không sửa branch của executor.',
    '',
    '## 6. Acceptance criteria',
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
    '12. Gate tài liệu, LF, trailing whitespace và final newline đều đạt.',
    '',
    '## 7. Quy tắc executor',
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
    '## 8. Quy tắc reviewer',
    '',
    '- Claude review read-only đúng head SHA trong `REVIEW_READY`.',
    '- Không Edit/Write/commit/push/merge/deploy.',
    '- Approval cũ hết hiệu lực khi head SHA thay đổi.',
    '- Có lỗi thì trả `changes_requested`.',
    '- Chỉ trả `cross_approved` khi không còn blocking finding.',
    '- Thiếu quyền, quota/token hoặc bằng chứng thì trả `review_deferred`.',
    '',
    '## 9. Khi gần hết token/context',
    '',
    'Ghi `HANDOFF_REQUIRED` gồm role, packet, generation, base/head SHA, việc đã làm, việc còn',
    'lại, lệnh tiếp tục, blocker và evidence. Sau đó `PAUSE`; không tự nhận hoàn thành.',
    '',
    '## 10. Điều kiện được land',
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
if (-not $DryRun) {
    $IssueTitle = '[WP D0] Land hiến pháp docs-only cho protocol đa phiên'
    $IssueOutput = ((& gh issue create --repo $Snapshot.repo_slug --title $IssueTitle `
        --body-file $BodyOutputPath 2>&1) | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "Không tạo được GitHub Issue. Packet body còn tại: $BodyOutputPath`n$IssueOutput"
    }

    $IssueUrl = @(
        $IssueOutput -split '\s+' |
        Where-Object { $_ -match '^https://github\.com/.+/issues/\d+$' }
    ) | Select-Object -Last 1
    if ([string]::IsNullOrWhiteSpace($IssueUrl)) {
        throw "GitHub trả thành công nhưng không tìm thấy Issue URL. Output: $IssueOutput"
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
} | ConvertTo-Json -Compress
