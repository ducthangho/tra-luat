# Prompt — Codex executor cho D0

Thay các placeholder trước khi gửi prompt:

- `{{ISSUE_URL}}`: URL GitHub Issue của work packet.
- `{{ISSUE_NUMBER}}`: số Issue; packet = `wp{{ISSUE_NUMBER}}`.
- `{{BASE_SHA}}`: SHA cố định ghi trong Issue.
- `{{PACKET_ID}}`: `wp{{ISSUE_NUMBER}}` (alias `wp-d0-protocol-constitution`).
- `{{GENERATION}}`: generation hiện hành.
- `{{BRANCH}}`: mặc định `agent/wp{{ISSUE_NUMBER}}-g1-codex`.
- `{{WORKTREE}}`: worktree sạch của executor.

---

Bạn là executor duy nhất của work packet `{{PACKET_ID}}`, generation
`{{GENERATION}}`, tại `{{ISSUE_URL}}`.

Claude là reviewer read-only. Thứ tự thẩm quyền là: **Issue thắng prompt; prompt
thắng memory**. Nếu Issue khác danh sách/giá trị tĩnh dưới đây, dừng và làm theo
Issue hoặc đặt `PAUSE` nếu mâu thuẫn làm thay đổi phạm vi.

## Nguồn chuẩn

Đọc đầy đủ trước khi sửa:

1. GitHub Issue `{{ISSUE_URL}}`, gồm mọi state/event comment mới nhất.
2. `CONTEXT.md`.
3. `planned:docs/PROTOCOL_DA_PHIEN.md`.
4. `planned:docs/KE_HOACH_TRIEN_KHAI_PROTOCOL_DA_PHIEN.md`.
5. ADR-0026 và ADR-0017–0033.
6. `AGENTS.md` hoặc chỉ dẫn repo tương đương nếu tồn tại.

Tiền tố `planned:` chỉ đánh dấu “chưa có ở base bootstrap”; đường dẫn thật là
phần sau dấu `:` và sẽ tồn tại sau bước copy nguồn D0.

Issue và protocol quyết định phạm vi. Nếu chúng mâu thuẫn, chuyển `PAUSE`, nêu
bằng chứng và không tự chọn một cách hiểu thuận tiện.

## Preflight và claim

Trước lần ghi đầu tiên:

1. Xác nhận trạng thái packet là `ready_for_claim`, không phải `PAUSE`,
   `leased`, `running`, `reviewing` hoặc trạng thái kết thúc.
2. Fetch remote và xác nhận `{{BASE_SHA}}` vẫn là base được Issue chỉ định.
3. Nếu worktree đã tồn tại, xác nhận nó sạch và branch là `{{BRANCH}}`; nếu
   chưa tồn tại, xác nhận path và branch chưa bị worktree/phiên khác sử dụng.
4. Khai triển write-set D0 thành danh sách đường dẫn chính xác.
5. Kiểm không có writer/PR đang giữ write-set giao nhau.
6. Comment `CLAIM` vào Issue với packet, generation, executor, base SHA,
   branch, worktree, write-set, thời điểm và lease expiry.

Nếu không kiểm được GitHub hoặc base/write-set đã đổi, dừng ở `PAUSE`; không
giả định trạng thái cũ vẫn đúng và không âm thầm rebase.

Các lệnh dưới đây dành cho PowerShell trên Windows; ghi lại output thực:

```powershell
$Canonical = 'D:\Quốc hội\tra-luat'
git -C $Canonical fetch origin --prune
$MeasuredBase = (git -C $Canonical rev-parse origin/master).Trim()
gh issue view {{ISSUE_NUMBER}} --repo ducthangho/tra-luat --comments
gh pr list --repo ducthangho/tra-luat --state open
git -C $Canonical worktree list
```

`$MeasuredBase` phải khớp `{{BASE_SHA}}`. Không dùng `git config
core.abbrev`; mọi bằng chứng SHA phải đủ 40 ký tự. PR mở, claim đang sống,
thiếu đúng 23 tệp nguồn hoặc lệch base ⇒ `PAUSE` với bằng chứng.

## Dựng worktree và copy nguồn

Nếu `{{WORKTREE}}` chưa tồn tại, sau khi claim hãy tạo đúng branch từ base đã
đóng băng; nếu đã tồn tại thì chỉ xác minh branch/status:

```powershell
git -C $Canonical worktree add '{{WORKTREE}}' -b '{{BRANCH}}' '{{BASE_SHA}}'
git -C '{{WORKTREE}}' rev-parse HEAD
git -C '{{WORKTREE}}' status --short
```

D0 là foundation PR vào `master`; quy tắc integration-head chỉ áp dụng sau F4.
Đọc write-set chính xác từ Issue, kỳ vọng 23 đường. Cây canonical đang bẩn là
nguồn nội dung read-only: **COPY BYTE NGUYÊN VẸN** từng đường sang worktree,
tạo thư mục cha khi cần. Sau copy:

- `git status --short` chỉ được liệt kê các đường thuộc write-set;
- không suy diễn số tệp `M`/untracked từ một snapshot cũ;
- thiếu, thừa hoặc có đường ngoài write-set ⇒ dừng, không “sửa cho khớp”;
- Không `git add -A`/`-u`; sau cùng stage đích danh từng đường.

## Phạm vi triển khai

Thực hiện đúng D0 docs-only và acceptance criteria trong Issue.

- Chỉ sửa write-set đã claim.
- Không mang tệp bẩn từ worktree khác.
- Không sửa `VERSION`, `CHANGELOG.md`, `SKILL.md`, manifest hoặc runtime.
- Không cấp số `rNNN`/version và không sinh release metadata.
- Không sửa security path ngoài phạm vi.
- Không merge hoặc deploy.
- Không re-import Capabilities.

Đặc biệt kiểm đủ các điểm:

- ADR-0001 chuyển thành `Superseded by ADR-0017` nhất quán.
- PR/SHA/worktree/version chỉ là snapshot có `observed_at`.
- Rollback F4 bị chặn ngay khi có packet v1 lease/start hoặc durable event hậu
  cutover; sau đó chỉ `PAUSE` và fix-forward.
- EOL chỉ nói về text file thuộc policy đang mang CRLF.
- Deploy/re-import luôn cần phê duyệt LIVE rõ ràng.
- T0 nghiệm thu Claude Remote Control Windows → Android end-to-end.
- Required check chỉ bật nguyên tử tại F4.
- Packet sau khi mission tồn tại lấy base từ integration head.

Áp “năm chỉnh sửa cuối” trong Issue, với các điểm đọc chéo sau:

1. Mọi số tức thời (PR mở, worktree, số phát hành trống, toolchain) có
   `observed_at` ISO-UTC và lệnh đo lại; số liệu research cũ giữ nhãn
   non-normative/snapshot.
2. Mọi câu rollback F4 trong Kế hoạch và PROTOCOL dùng cùng điều kiện:
   **chưa packet v1 nào lease/start VÀ chưa durable event hậu cutover**; nếu
   một vế đã xảy ra thì chỉ fix-forward.
3. Mọi câu CRLF/EOL phân biệt policy đích với hiện trạng đo tại một mốc; không
   khái quát sang binary/golden đang `-text`.
4. Cả F2 và F4 đều ghi deploy/re-import chỉ sau phê duyệt LIVE tường minh.
5. T0 có ca end-to-end Claude Remote Control Android↔Windows, gồm host phải
   thức, mất mạng và reconnect; cờ CLI chưa đo không được đưa vào runbook chuẩn.

Rà nhất quán thêm: ADR-0017 dùng `leased`; ADR-0025↔0033 journal/inbox;
ADR-0031↔F1-04 chỉ bật required check tại F4; ADR-0032 dùng đúng policy path và
ratchet bốn kết cục; §8.2 dùng integration head; không nới credential boundary
ADR-0020 hoặc one-executor-per-packet.

## Kiểm chứng

Chạy trên đúng worktree sẽ push. Đòi **5 cổng JSON** và selftest; không tin exit
code sau pipe:

```powershell
Set-Location '{{WORKTREE}}'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:GIT_CONFIG_COUNT = '1'
$env:GIT_CONFIG_KEY_0 = 'core.abbrev'
$env:GIT_CONFIG_VALUE_0 = '7'
$Evidence = Join-Path $env:TEMP 'wp{{ISSUE_NUMBER}}-evidence'
New-Item -ItemType Directory -Path $Evidence -Force | Out-Null
$Dc = Join-Path $Evidence 'dc.json'
$Rv = Join-Path $Evidence 'rv.json'
$Wa = Join-Path $Evidence 'wa.json'
$Gt = Join-Path $Evidence 'gt.json'
$Da = Join-Path $Evidence 'da.json'
$Selftest = Join-Path $Evidence 'selftest.log'

python scripts/tl.py doc-claims-check --strict --json > $Dc
python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json > $Rv
python scripts/tl.py workflow-audit --strict --json > $Wa
python scripts/tl.py golden-test --json > $Gt
python scripts/tl.py determinism-audit --strict --json > $Da

Get-ChildItem $Evidence -Filter '*.json' | ForEach-Object {
    $Result = Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json
    [pscustomobject]@{ file = $_.Name; ok = $Result.ok }
}

python scripts/tl_selftest.py *> $Selftest
Select-String -Path $Selftest -Pattern '== tl selftest'
(Select-String -Path $Selftest -SimpleMatch '[FAIL]').Count
```

Mọi JSON phải `ok: true`; marker `[FAIL]` phải bằng 0. Không dùng `| tail`,
không đếm chữ `FAIL` trần vì tên test có thể chứa từ đó. Không đóng đinh tổng
advisory cũ: chỉ so delta và điều tra advisory trỏ vào tệp D0.

Trước commit, hygiene phải so working tree (gồm staged + unstaged) với base đóng
băng; không dùng `BASE..HEAD` khi HEAD vẫn còn bằng base:

```powershell
git diff --name-status '{{BASE_SHA}}'
git diff --numstat '{{BASE_SHA}}'
git diff --check '{{BASE_SHA}}'
git diff '{{BASE_SHA}}' -- VERSION CHANGELOG.md SKILL.md RELEASE_MANIFEST.json scripts/ references/
```

Lệnh cuối phải rỗng; đối chứng bằng diff không pathspec để tránh “rỗng giả”.
Numstat phình bất thường là dấu hiệu lật EOL. Kiểm LF/final newline bằng bytes,
và map từng acceptance trong Issue sang bằng chứng trực tiếp.

## Bàn giao review

Khi toàn bộ acceptance criteria đạt:

1. `git add` đích danh đúng 23 đường; kiểm `git diff --cached --name-only`.
2. Tạo một commit docs-only, không bump version/r/manifest.
3. Push `{{BRANCH}}` nếu quyền hiện hành cho phép, rồi mở PR vào `master` có
   link Issue và evidence; không dùng `--force`.
4. Chờ CI của PR và ghi kết quả; gate local không thay thế CI.
5. Không merge hoặc deploy.
6. Comment `REVIEW_READY` vào Issue theo mẫu:

Sau commit, lặp lại hygiene trên commit thật và đòi worktree sạch:

```powershell
git diff --name-status '{{BASE_SHA}}..HEAD'
git diff --numstat '{{BASE_SHA}}..HEAD'
git diff --check '{{BASE_SHA}}..HEAD'
git diff '{{BASE_SHA}}..HEAD' -- VERSION CHANGELOG.md SKILL.md RELEASE_MANIFEST.json scripts/ references/
git status --short
```

```text
REVIEW_READY
packet_id: {{PACKET_ID}}
generation: {{GENERATION}}
executor: codex
base_sha: {{BASE_SHA}}
head_sha: <HEAD_SHA_THỰC>
branch: {{BRANCH}}
reviewer_fill_command: & '{{REPO_PATH_PS}}\docs\runbooks\Fill-SharedWorkPacketPrompt.ps1' -Role reviewer -IssueNumber {{ISSUE_NUMBER}} -BaseSha {{BASE_SHA}} -HeadSha <HEAD_SHA_THỰC> -Generation {{GENERATION}} -Branch '{{BRANCH}}' -RepoPath '{{REPO_PATH_PS}}'
changed_files:
  - <path>
commands_and_results:
  - <command> => <exit/result>
residual_risks:
  - <risk hoặc none>
```

Trong `changed_files`, liệt kê đủ đường thực tế và xác nhận chúng là tập con
của write-set Issue. Ghi 5 cổng JSON, selftest N/N + `[FAIL]`=0, diffstat,
derived diff rỗng và CI. PR phải ghi Claude review read-only; không merge trước
`cross_approved` gắn đúng head SHA.

Thay `<HEAD_SHA_THỰC>` trong `reviewer_fill_command` bằng SHA vừa commit. Người
dùng chạy lệnh đó để nhận prompt Claude đã điền cùng đúng hai lệnh PowerShell
dựng detached review worktree; Claude không tự chạy hai lệnh chuẩn bị này.

Claude chỉ review đúng `head_sha` này. Mọi commit mới làm approval cũ hết hiệu
lực và cần `REVIEW_READY` mới.

## Khi gần hết token/context

Không tự sinh executor thứ hai. Ghi comment `HANDOFF_REQUIRED` gồm packet,
generation, base/head SHA, việc đã làm, việc còn lại, lệnh tiếp tục, blocker và
evidence. Đặt `PAUSE` hoặc `handoff_required`; không nhận là hoàn thành.

Nếu token/quota không đủ cho bước còn lại, ưu tiên lưu evidence và handoff có
thể tiếp tục được; không hạ chuẩn và không tự mở work packet kế tiếp.
