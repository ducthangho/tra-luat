---
name: work-packet
description: Adapter thực thi work packet trên Codex CLI. Đọc docs/PROTOCOL_DA_PHIEN.md và Packet được giao; tệp này cung cấp cú pháp PowerShell và con trỏ công cụ.
---

# Adapter `work-packet` — Codex CLI / PowerShell

Nguồn chung: [protocol](../../../docs/PROTOCOL_DA_PHIEN.md) §3.2.1 (spec và ba mốc Git),
§4/§5 (lease/write set), §7 (handoff/comment), §10.2.1–§10.2.4 (preflight/evidence/trạng thái),
§12/§13 (budget và hợp đồng skill).
Nguồn cú pháp Bash/Python: [.claude adapter](../../../.claude/skills/work-packet/SKILL.md).
Adapter này dùng `openai_codex / codex_cli / machine`; model/effort thực tế lấy từ run.

## Đọc spec và mốc checkout

Các biến `$SpecOid`, `$SpecPath`, `$Scratch`, `$Canon`, `$S`, `$H` lấy từ assignment và
bootstrap đã xác minh theo §3.2.1/§8.1. `$Scratch` ở ngoài checkout.

```powershell
$Py = (Get-Command python -ErrorAction Stop).Source
& $Py --version
git rev-parse --show-toplevel HEAD 'HEAD^{tree}'
git branch --show-current
git status --porcelain=v1 --untracked-files=all --ignored=matching
gh issue view 55 --json body --jq .body
& $Py -c 'import hashlib,pathlib,subprocess,sys; b=subprocess.run(["git","show",sys.argv[1]+":"+sys.argv[2]],check=True,capture_output=True).stdout; pathlib.Path(sys.argv[3]).write_bytes(b); print(hashlib.sha256(b).hexdigest())' $SpecOid $SpecPath (Join-Path $Scratch 'spec.md')
```

Python nhận bytes trực tiếp từ Git, tránh PowerShell đổi encoding/newline của blob.
Số Issue 55 chỉ minh họa cú pháp, thay bằng assignment. Nếu `python` không resolve, dùng
executable đã probe (ví dụ `C:/Python313/python.exe` trên host có đường dẫn ấy).

## Local admission và capability

`$Canon` chứa mã ở `$S` và object `$H`; điều kiện dùng/giới hạn receipt ở protocol §10.2.1.
Ví dụ này không fetch hay chạy workflow:

```powershell
git -C $Canon merge-base --is-ancestor $S $H
$AncestorRc = $LASTEXITCODE
switch ($AncestorRc) {
    0 { 'ancestor=true' }
    1 { throw 'ancestor=false' }
    default { throw "ancestry not_measured rc=$AncestorRc" }
}
& $Py -B (Join-Path $Canon 'ops/lease_publish.py') kiem-thu-hoi-github $H --root $Canon --canonical-base $S --nhanh-mac-dinh master --receipt (Join-Path $Scratch 'local-admission.json')
$AdmissionRc = $LASTEXITCODE
if ($AdmissionRc -ne 0) { throw "admission rc=$AdmissionRc" }
```

Đọc marker/receipt, không chỉ rc (§10.2.1). Probe modules bằng `& $Py -B -c 'import yaml'`
và các module của command thực; `Get-Command git, jq, actionlint`, `git --version`,
`jq --version`, `actionlint -version`, `$PSVersionTable.PSVersion` cho tool/shell.
Probe WSL (nếu Packet dùng WSL) phải chạy bên trong distribution đó theo §10.2.1.

## Local checks và evidence

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONPYCACHEPREFIX = Join-Path $Scratch 'pycache'
& $Py -B .claude/dev/packet_loop.py doctrine-scan --root . --path .agents/skills/work-packet/SKILL.md --path .agents/skills/cross-review/SKILL.md --path .agents/skills/land-packets/SKILL.md
$DoctrineRc = $LASTEXITCODE
& $Py -B .claude/dev/packet_loop.py adr-song --root .
$AdrRc = $LASTEXITCODE
& $Py -B scripts/tl.py doc-claims-check --strict
$ClaimsRc = $LASTEXITCODE
git diff --check
$DiffRc = $LASTEXITCODE
```

Chọn check theo Packet/§10.1; không coi danh sách ví dụ là full gate. Với config Git phục vụ
gate, đặt `core.abbrev=7` trong bootstrap (§8.1) hoặc dùng cấu hình riêng từng process.
Ví dụ máy trạng thái, heartbeat, guard và rc nằm trong .claude adapter; PowerShell gọi Python
bằng `& $Py` và lấy `$LASTEXITCODE` ngay sau command. Không dùng cú pháp continuation `\` của Bash.
Receipt đăng comment dùng đúng khối Python “Body file và exact readback” ở nguồn; gọi file
scratch bằng `& $Py $PostScript $IssueNumber $BodyFile $Scratch`. Authority/handoff ở §7/§13.
Full ref delta: adapter [land-packets](../land-packets/SKILL.md). CI query và nullable provenance:
adapter [cross-review](../cross-review/SKILL.md).
