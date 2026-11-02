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
**Native Windows chưa hỗ trợ admission**: checker giải Git qua `/usr/bin:/bin`.
Phép ancestry native dưới đây chỉ đo đồ thị; không gọi checker bằng `$Py` native sau nó:

```powershell
git -C $Canon merge-base --is-ancestor $S $H
$AncestorRc = $LASTEXITCODE
switch ($AncestorRc) {
    0 { 'ancestor=true' }
    1 { throw 'ancestor=false' }
    default { throw "ancestry not_measured rc=$AncestorRc" }
}
```

Nếu Packet cho phép WSL, bootstrapper chọn `$WslDistro`, clone tại `$CanonWsl` chứa mã
canonical `$S`/object `$H`, scratch `$ScratchWsl` và script `$AdmissionScriptWsl`, tất cả
đường dẫn tuyệt đối theo Linux. Script là nguyên khối Bash mục “Gate” của
[work-packet nguồn](../../../.claude/skills/work-packet/SKILL.md), lưu ngoài checkout.
Không dùng `.git` linked worktree chứa đường dẫn Windows làm object store WSL.

```powershell
wsl --list --quiet
wsl -d $WslDistro --exec bash $AdmissionScriptWsl $CanonWsl $S $H $ScratchWsl
$AdmissionRc = $LASTEXITCODE
if ($AdmissionRc -ne 0) { throw "WSL admission incomplete rc=$AdmissionRc; inspect output" }
wsl -d $WslDistro --exec cat "$ScratchWsl/local-admission.json"
$ReceiptReadRc = $LASTEXITCODE
if ($ReceiptReadRc -ne 0) { throw "receipt not_measured rc=$ReceiptReadRc" }
```

Script probe Python/modules, Git tối thiểu và Bash trong chính WSL, đối chiếu bytes checker
với blob tại `$S`, rồi mới đo ancestry/admission. Đọc marker và receipt S/H/T theo §10.2.1;
WSL rc=0 hoặc đọc được JSON chưa tự đủ bằng chứng. Không có lane được cấp/probe không đạt:
ghi admission `not_measured` và handoff S/H, code hash, lỗi thực, dependency còn thiếu theo
§10.2.1; không thử sửa runtime hoặc dùng kết quả ancestry thay admission.

Probe modules native cho command native bằng `& $Py -B -c 'import yaml'`
và các module của command thực; `Get-Command git, jq, actionlint`, `git --version`,
`jq --version`, `actionlint -version`, `$PSVersionTable.PSVersion` cho tool/shell.
Probe heavy gate nào vẫn phải đủ tools của chính command đó theo §10.2.1; probe admission
ở trên không xác nhận jq/actionlint hay toàn bộ heavy gate.

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

## Ca symlink Windows native

**Đã đo** (WP748 g11, Windows 11, Python 3.13.1, head `0daeb47`, 15-10-2026): 12 ca `t20n`
`t20x` `t20zd` `t20zf` `t20q` `t20zi` `t20zj` `t20zk` `t20zl` `t20zm` `t20zn` `t20zo` của
`ops/ci_duong_nhanh_test.py`, mỗi ca một lệnh `--mot-ca`, cả 12 `rc=0`, không `WinError 1455`.
Đó là bằng chứng TARGETED trên đúng head ấy, không phải full suite.

**Hướng dẫn** (luật đọc, không phải kết quả đo). Mỗi ca một lệnh, lấy rc ngay sau lệnh:

```powershell
& $Py -B -c 'import yaml'   # thiếu PyYAML thì module chết lúc nạp, không phải lỗi ca
& $Py -B ops/ci_duong_nhanh_test.py --mot-ca t20zk_kiem_re_symlink_treo_qua_bi_danh_thu_muc_do
"t20zk rc=$LASTEXITCODE"    # 0 = đạt (không in gì); 3 = DO; 4 = HONG
```

- Fixture dựng symlink THẬT (`Path.symlink_to`, tệp hay thư mục khai bằng `target_is_directory`;
  trên Windows đích đổi `/` thành `\`). Không có nhánh bỏ qua: không tạo được symlink ⇒ `HONG`.
- `WinError 1455` ném từ `subprocess.Popen` lúc fixture chạy `git init`, trước assertion, là lỗi
  MÔI TRƯỜNG: ghi lại, đo bộ nhớ/pagefile, dừng gate nặng song song.
- Targeted không thay full suite (`CA: N/N`, `DOT BIEN: M/M`, `TONG: DAT`) trên đúng head.
- Ngoại lệ named pipe/socket của `t20zo` (FIFO = symlink tới named pipe thật; socket = `os.stat`
  giả cho leaf `sk`, comment 6171400658) đo logic danh sách cho phép, tách khỏi bằng chứng symlink.
