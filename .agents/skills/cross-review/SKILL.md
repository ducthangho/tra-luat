---
name: cross-review
description: Adapter review packet trên Codex CLI với checkout/context được cấp riêng. Assurance và hợp đồng evidence lấy từ docs/PROTOCOL_DA_PHIEN.md; cung cấp cú pháp PowerShell.
---

# Adapter `cross-review` — Codex CLI / PowerShell

Đọc [protocol](../../../docs/PROTOCOL_DA_PHIEN.md) §7 (receipt), §8/§8.1–§8.3
(assurance, bootstrap, runtime, cache, Ruff, lịch sử lớp), §10.2.1–§10.2.3 (CI) và §13.
Nguồn cú pháp và ghi chép provider: [.claude adapter](../../../.claude/skills/cross-review/SKILL.md).
Các mục model selector Claude ở nguồn chỉ dành cho lane Claude; không dùng bảng đó chọn Codex.
Nhận dạng nền này là `openai_codex / codex_cli / machine`; model/effort và sandbox đọc từ run.

## Bootstrap và snapshot

Biến `$Remote`, `$ReviewRoot`, `$Branch`, `$ReviewedSha`, `$Scratch` lấy từ assignment.
Lệnh clone/config/checkout thuộc bootstrap trước bàn giao (§8.1):

```powershell
git -c core.longpaths=true clone --no-checkout $Remote $ReviewRoot
git -C $ReviewRoot remote get-url origin
git -C $ReviewRoot config core.abbrev 7
git -C $ReviewRoot config core.longpaths true
git -C $ReviewRoot fetch origin $Branch
git -C $ReviewRoot checkout --detach $ReviewedSha
git -C $ReviewRoot rev-parse HEAD 'HEAD^{tree}'
git -C $ReviewRoot status --porcelain=v1 --untracked-files=all --ignored=matching
git -C $ReviewRoot diff --binary
git -C $ReviewRoot diff --cached --binary
git -C $ReviewRoot ls-files --others --exclude-standard
git -C $ReviewRoot ls-files --others --ignored --exclude-standard
```

Ghi rc của từng command ngay sau chạy; snapshot bytes/hash và giới hạn quan sát ở §8.2.
Trust path/capability theo §8.1; không có lệnh tự chấp nhận trust trong adapter này.

Ví dụ diff/numstat giữ raw bytes trong scratch của run, với `$BaseSha` từ assignment:

```powershell
$Py = (Get-Command python -ErrorAction Stop).Source
& $Py -B -c 'import pathlib,subprocess,sys; r,b,h,o=sys.argv[1:]; p=subprocess.run(["git","-C",r,"diff",b,h],check=True,capture_output=True); (pathlib.Path(o)/"diff.patch").write_bytes(p.stdout); p=subprocess.run(["git","-C",r,"diff","--numstat",b,h],check=True,capture_output=True); (pathlib.Path(o)/"numstat.txt").write_bytes(p.stdout)' $ReviewRoot $BaseSha $ReviewedSha $Scratch
$DiffArtifactsRc = $LASTEXITCODE
```

`$ReviewRoot`/`$Scratch` là đường dẫn tuyệt đối. Khi đọc `modelUsage` lane Claude qua nguồn,
truyền `$ReviewRoot` vào đối số SOURCE và JSON đúng `$Scratch/reviewer.json`; producer và
consumer cùng run theo §8.1. Không đọc JSON trùng tên ở cwd.

## Runtime và Ruff

```powershell
$Py = (Get-Command python -ErrorAction Stop).Source
codex --version
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONPYCACHEPREFIX = Join-Path $Scratch 'pycache'
& $Py -B -c 'import pathlib,runpy,sys; m=runpy.run_path(str(pathlib.Path(sys.argv[1])/".claude/dev/ci_dang_ky_test.py")); errors,count=m["loi_ruff_ci"](); print("RUFF_CONTRACT",count,errors); sys.exit(bool(errors) or count == 0)' $ReviewRoot
$RuffContractRc = $LASTEXITCODE
& $Py -m ruff check --no-cache --select F (Join-Path $ReviewRoot 'scripts/tl.py')
$RuffLintRc = $LASTEXITCODE
```

Hai lệnh Ruff trỏ checkout được giao, không phụ thuộc cwd. Pin/probe và bare lint là hai scope của §8.2;
tiêu chí A7/mutant riêng xem §10.2.3. Cú pháp `launcher.py run --prompt-file` và mẫu Codex
ở nguồn, mục “Reviewer là codex”; schema đầy đủ ở `docs/GOI_AGENT_DA_NEN.md`.
`$Run = Get-Content -Raw -LiteralPath $RunJson | ConvertFrom-Json` đọc rc con/trạng thái; parse được chưa là
completion evidence. Model/effort/sandbox lấy từ `$Run.model_phuc_vu`, `$Run.effort_phuc_vu`, `$Run.sandbox_quan_sat`,
chỉ đo được khi `model_phuc_vu_trang_thai`/`effort_phuc_vu_trang_thai`/`sandbox_trang_thai` là `DO_DUOC`
(khác thì đọc `*_ly_do`); đối chiếu với prompt/receipt theo §8.1. Header `model:`/`reasoning effort:` trong
`$StderrLog`, nếu có, chỉ là lời khai phụ; vắng header không phải chưa đo được. Không lấy model từ actor GitHub.

## Provenance và vận chuyển

Lưu khối GraphQL “Provenance CI” của .claude adapter vào `$QueryFile` ngoài checkout:

```powershell
gh api graphql -F "query=@$QueryFile" -f "id=$RunNodeId"
$ProvenanceRc = $LASTEXITCODE
gh api --paginate --slurp "repos/ducthangho/tra-luat/actions/runs/$RunId/attempts/$Attempt/jobs?per_page=100"
$JobsRc = $LASTEXITCODE
git -C $ReviewRoot cat-file blob "${DefinitionOid}:$WorkflowPath"
```

Khối `cat-file` minh họa đọc; để lưu bytes/hash dùng Python `subprocess` như work-packet.
Nguồn URL/OID, nullable `file`, 403, skipped/waiver và đủ attempt/context theo §10.2.2–§10.2.3.
Receipt body-file dùng Python ở [work-packet nguồn](../../../.claude/skills/work-packet/SKILL.md),
mục “Body file và exact readback”. Bảng verdict/lịch sử lớp ở nguồn; không đổi contract khi
đổi shell. Không dispatch reviewer từ ví dụ đọc evidence này.
