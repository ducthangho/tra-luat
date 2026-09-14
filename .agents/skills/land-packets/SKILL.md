---
name: land-packets
description: Adapter chuẩn bị land khi người dùng giao việc trên Codex CLI. Authority, trigger và tiêu chí hoàn tất nằm trong docs/PROTOCOL_DA_PHIEN.md; cung cấp cú pháp PowerShell và con trỏ.
---

# Adapter `land-packets` — Codex CLI / PowerShell

Đọc [protocol](../../../docs/PROTOCOL_DA_PHIEN.md) §13/§13.1–§13.2 (trigger/quyền, fence,
ruleset), §4 (hạn lease), §5.1 (ref delta), §7 (receipt), §8 (assurance) và §10.2 (CI/trạng thái).
Nguồn Bash/Python: [.claude adapter](../../../.claude/skills/land-packets/SKILL.md).
Nền này là `openai_codex / codex_cli / machine`; không coi frontmatter của Claude là
cơ chế chặn tự kích hoạt trên Codex. Điều kiện gọi skill nằm ở §13.

Admission trước heavy gate dùng nhánh Linux/WSL hoặc handoff của
[work-packet](../work-packet/SKILL.md), theo §10.2.1; native Git xanh không chứng minh
admission native chạy được. Diff/numstat đọc từ scratch của đúng run bằng cú pháp
[cross-review](../cross-review/SKILL.md), giữ `$ReviewRoot` và `$Scratch` tường minh.

## Đọc trạng thái và full fence

`$Scratch`, `$MergeOid` và các ID lấy từ assignment; scratch ngoài checkout.

```powershell
gh issue view 54 --json labels,title
gh pr list --state open --json number,headRefName,headRefOid,statusCheckRollup
$RemoteRefs = @(git ls-remote origin)
$RefsRc = $LASTEXITCODE
if ($RefsRc -ne 0 -or $RemoteRefs.Count -eq 0) { throw "refs not_measured rc=$RefsRc" }
$RefFile = Join-Path $Scratch 'refs-new.raw'
[IO.File]::WriteAllText($RefFile, ($RemoteRefs -join "`n") + "`n", [Text.UTF8Encoding]::new($false))
git show -s --format='%H %P %T' $MergeOid
```

Khối Python “Full ref fence và merge evidence” ở nguồn in đủ name/old/new và hash; lưu
ngoài checkout rồi gọi `& $Py $RefScript $OldRefFile $RefFile`, lấy `$LASTEXITCODE` ngay.
Script không loại `refs/pull`; phân loại/refence theo §5.1/§13.1. Số Issue ví dụ thay bằng
assignment; CI chưa đo lấy disposition theo §10.2, không suy từ `statusCheckRollup` rỗng.

## Ruleset và readback

```powershell
gh api "repos/ducthangho/tra-luat/rulesets/$RulesetId"
$RulesetReadRc = $LASTEXITCODE
```

Lưu raw JSON bằng `subprocess` capture nếu cần bảo toàn bytes. Python “Ruleset snapshot và
payload ngoài checkout” ở nguồn chỉ dựng writable projection trên snapshot; dùng lại với
`& $Py $ProjectionScript $SnapshotFile $PayloadFile`. Quyền thay đổi, read-before-write,
integration ID, readback và giới hạn race ở §13.2. Không có lệnh mutation ruleset trong ví dụ.
Comment/readback dùng [work-packet](../work-packet/SKILL.md); provenance CI dùng
[cross-review](../cross-review/SKILL.md). Báo merged/landed/Packet complete/Mission complete
theo §10.2.4; adapter không tự tạo authorization hoặc receipt của thao tác chưa chạy.
