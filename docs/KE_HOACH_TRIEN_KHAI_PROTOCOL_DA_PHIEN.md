# Kế hoạch triển khai Protocol đa phiên Claude–Codex

- **Trạng thái:** Kế hoạch thi công chi tiết
- **Ngày chốt:** 2026-08-03
- **Nguồn chuẩn:** `docs/PROTOCOL_DA_PHIEN.md`, ADR-0017–ADR-0033
- **Mục tiêu:** từ repo hiện tại đi tới hai executor Claude/Codex chạy song song an toàn, tự bàn giao,
  tiếp tục qua Windows/cloud/Android và land có phê duyệt.

Tài liệu này là kế hoạch thi công, không thay thế protocol. Ký hiệu
`planned:<repo-relative-path>` chỉ tệp/thư mục sẽ tạo trong pha tương ứng, chưa khẳng định nó đang tồn tại.

## 1. Kết quả cuối cùng cần đạt

1. Mỗi mission có Issue, integration branch và draft land PR riêng.
2. Mỗi packet có spec hash, effective write set, executor, environment và lease generation duy nhất.
3. Codex và Claude chỉ ghi trên worktree/branch của packet mình; không hai lease giao nhau.
4. Test mới nằm trong fragment packet-owned; version, changelog hợp nhất, bundled test module và manifest
   chỉ do land gate sinh.
5. Command/handoff vào durable inbox; reconciler single-writer không làm rơi event hay sinh packet trùng.
6. Hết token/quota chuyển `paused` hoặc review fallback có nhãn, không đổi provider âm thầm.
7. Windows tắt không làm mất packet; cloud tiếp tục, packet local chờ controller trở lại.
8. Android đọc prompt/state và gọi cùng operation `land apply` cho exact head SHA.
9. Worker không có credential LIVE; deploy là cổng phê duyệt riêng.

## 2. Trạng thái xuất phát và các blocker

Kiểm tại 2026-08-03:

- local `master` ở `e8134a2`, sau `origin/master=ac63cd7` chín commit;
- worktree canonical đang bẩn và có nhiều worktree/phiên khác; không được stage hàng loạt từ cây này;
- Codex CLI `0.146.0` chạy được;
- Claude Code: npm từng trỏ binary không hợp lệ cho Windows và đã gỡ trong preflight; **đo lại 03-08
  ~09:45: native `2.1.220` tại `C:\Users\admin\.local\bin\claude.exe` CHẠY ĐƯỢC, `where.exe claude`
  chỉ một đường** ⇒ T0-01 chỉ còn `claude doctor` + login/workspace trust;
- `.gitattributes` vẫn `* -text`; `CLAUDE.md` vẫn bắt mọi phiên bump release metadata;
- chưa có fragment harness, change-impact policy, Issue Forms, adapters, dispatcher, reconciler, local controller
  hay `land apply` operation;
- **ĐÃ ĐO 03-08 (~09:40): cổng tài liệu KHÔNG còn là blocker** — `doc-claims-check --strict` trên worktree
  sạch tách từ `origin/master` + trọn bộ D0 (kể cả kế hoạch này) = `ok:true`, 0 blocking; advisory đều thuộc
  tài liệu cũ có sẵn (chi tiết phụ lục §13);
- PR #22 (r327/v1.36.59 — vá phép dò auth `gws`) MỞ lúc đo ~09:45 nhưng **ĐÃ MERGE trước ~10:15**:
  `origin/master` nay = r327/v1.36.59, số trống kế tiếp **r328/v1.36.60**, 0 PR mở ⇒ cửa sổ
  zero-open-PR ĐANG MỞ — đo lại `gh pr list --state open` ngay trước khi dùng.

Hệ quả: chưa được chạy hai **writer code** theo protocol ngay. Trước activation, chỉ cho phép hai phiên
read-only hoặc pilot thủ công với write set do người giữ đối chiếu.

## 3. Nguyên tắc chia việc và commit

- Mỗi work packet cho ra một kết quả tự đủ, một PR và một rollback point.
- Không gộp migration EOL, dispatcher, provider adapter và land automation trong một PR.
- PR hạ tầng nhạy cảm phải cross-review hoặc human review; không dùng `review_deferred`.
- Trước activation, foundation PR được land tuần tự theo quy trình release cũ; không chạy song song
  hai PR cùng chạm `scripts/tl.py`, `scripts/tl_selftest.py`, release policy hoặc metadata.
- Foundation land theo giao thức cũ ⇒ chọn `r`/version **ở phút chót**: quét `gh pr list --state open`
  VÀ VERSION của mọi nhánh remote trước khi chốt số (48h qua đụng số 5 lần; r327/v1.36.59 đã vào master
  qua PR #22 — số trống lúc đo ~10:15 là r328/v1.36.60).
- Sau activation, tối đa hai executor ghi; dispatcher chỉ cấp lease sau khi closure của hai packet không giao.
- Tài liệu, schema, policy và test đi cùng code làm chúng xanh; không tạo PR “code trước, guard sau”.

## 4. Bản đồ rollout

```mermaid
flowchart LR
    D0["D0: Bootstrap tài liệu"] --> T0["T0: Toolchain + baseline"]
    T0 --> F1["F1: Test fragments"]
    F1 --> EOL["F2: EOL migration"]
    EOL --> S1["F3: Protocol + safety"]
    S1 --> CUT["F4: Zero-legacy cutover"]
    CUT --> A3["A3: Dispatcher shadow"]
    A3 --> A4["A4: Cloud canary"]
    A4 --> A5["A5: Dual provider"]
    A5 --> A6["A6: Successor + Android"]
    A6 --> A7["A7: Local controller"]
    A7 --> A8["A8: Land automation"]
```

`Foundation complete` chỉ ở F4. `Mission automation complete` chỉ sau A8.

## 5. Kế hoạch work packet chi tiết

### D0 — Bootstrap tài liệu trên worktree sạch

| Packet | Nội dung | Phụ thuộc | Nghiệm thu |
|---|---|---|---|
| D0-01 | Tạo worktree từ `origin/master`; mang sang CONTEXT, protocol, **ADR-0001 (bản đánh dấu Superseded)**, ADR-0017–0033, research và kế hoạch này; KHÔNG mang tệp M khác của cây bẩn (vd `docs/WORKFLOW_RASOAT_TU_DONG.md` — khác chủ) | không | diff chỉ docs/CONTEXT; không cuốn runtime bẩn |
| D0-02 | Chuẩn hóa liên kết, planned path và con trỏ tài liệu | D0-01 | `doc-claims-check --strict`, link check, `git diff --check` xanh — baseline ĐÃ XANH (đo 03-08, phụ lục §13); đo lại trên đúng cây sẽ commit |
| D0-03 | PR docs-only và review chéo/human | D0-02 | merge vào canonical; ghi base SHA cho foundation |

Kill switch: nếu PR có runtime diff hoặc doc gate đỏ, đóng PR và tạo lại từ worktree sạch; không “dọn”
canonical bằng reset.

D0 **không bump version/r, không regen manifest**: docs-only nằm ngoài gói (tiền lệ PR #16/r321
«ngoài gói»). Ai bump ở D0 là sai giao thức.

### T0 — Toolchain và GitHub baseline

| Packet | Nội dung | Phụ thuộc | Nghiệm thu |
|---|---|---|---|
| T0-01 | ĐÃ ĐO 03-08: native 2.1.220 chạy được, npm đã gỡ, winget KHÔNG có ⇒ chỉ còn xác nhận một-bản-duy-nhất + doctor + login/trust | D0 | `where.exe claude` đúng MỘT đường; `claude doctor`, login và workspace trust qua |
| T0-02 | Kiểm Codex CLI/app, Git, GitHub CLI, Python 3.12, PowerShell 7 (đo 03-08: codex-cli 0.146.0 ✓, `gh auth` ✓); CHẠY THỬ mọi cờ dùng ở runbook §8: `--remote-control`, `--worktree`, `codex exec --output-schema`/`-o`, `codex … review`, `-s`/`-a` | D0 | tất cả `--version` xanh; **cờ chưa kiểm không được vào runbook chuẩn**; không lộ token |
| T0-03 | Chốt nhãn, environment và actor allowlist trên GitHub | D0 | có owner, backup owner và test account không quyền |
| T0-04 | Kiểm kê worktree/PR/branch đang sống | D0 | mỗi writer có owner và quyết định finish/push/close |

T0 không thêm provider secret vào GitHub.

### F1 — Test fragment và bundled topology

Pha này tuần tự vì chạm legacy harness/release. Đích file đã chốt:
`planned:scripts/test_fragments/`, `planned:scripts/tl_core/test_fragments.py` và
`planned:scripts/tl_test_fragments_bundled.py`.

Loader/generator là tệp MỚI + điểm móc tối thiểu vào harness — KHÔNG rewrite monolith CRLF trước F2;
mọi writer ghi UTF-8/LF tường minh (ADR-0031).

| Packet | Write set chính | Kết quả | Nghiệm thu |
|---|---|---|---|
| F1-01 | legacy harness + loader mới | API discover fragment theo tên tất định; từ chối ID/path sai | fixture root tạm: zero/one/many/duplicate/malformed |
| F1-02 | loader + resolver doc/test ID | registry lập chỉ mục cả `rNNN_*` và `wp<issue>_<slug>` | legacy pointer, wp pointer và fake pointer có phản chứng |
| F1-03 | generator + release predicate | sinh bundled module UTF-8/LF; exclude đúng canonical prefix | byte output giống Windows–Linux; basename cùng tên ở chỗ khác không bị loại |
| F1-04 | release required files/topology | dev chạy fragment; bundle chỉ mang bundled module | thiếu bundled module fail đích danh TRÊN FIXTURE; required-check thật chỉ bật ở F4 cùng activation (ADR-0031); bundle dưới trần file |
| F1-05 | một regression test canary | chuyển/thêm một test mới bằng wp ID | legacy selftest và fragment test cùng xanh |

Promotion gate F1: full selftest, release behavior, determinism và parity hai OS xanh; generator và module
không có hai implementation khác nhau.

### F2 — Migration EOL có drain

| Packet/commit | Nội dung | Nghiệm thu |
|---|---|---|
| F2-00 | Freeze writer mới; owner của mọi worktree push/handoff/close | danh sách writer về zero; chốt EOL base SHA |
| F2-A | `.gitattributes`, `.editorconfig`, validator blob-index và hook Python | test file mới, Unicode, space, LF/CRLF; hook không chỉ so với HEAD |
| F2-B | Chỉ `git add --renormalize .` | diff chỉ newline; không thay nội dung logical |
| F2-C | Tái sinh manifest/golden/artifact; SKILL.md đổi cỡ byte sau LF ⇒ tái sinh golden `workflow_audit.json` + sửa TAY claim ở `references/GOTCHAS.md` dòng 16 + cập nhật rule tạm change-impact (nếu đã seed) | Windows–Linux cùng blob/hash và full gate xanh |
| F2-D | Mở lại writer | mọi branch cũ rebase trên EOL base; branch chưa rebase bị chặn |

F2 đổi byte MỌI tệp trong gói ⇒ `package_hash` mới: kết thúc F2 phải deploy bản mới (deploy-guard
đơn điệu) và user re-import Capabilities (SKILL.md đổi byte).

Rollback: chỉ quay lại trước F2-A khi chưa merge. Sau merge, không revert riêng F2-B; pause và sửa
policy/parity bằng maintenance PR mới.

### F3 — Protocol, safety và hai CI lane

Sau F2, có thể chạy tối đa hai packet trong các nhóm ghi không giao. Các tệp mới dưới
`planned:.github/coordination/` và `planned:.agents/skills/` là dev-side, phải bị loại khỏi release bundle.

| Packet | Nhóm ghi | Nội dung | Phụ thuộc |
|---|---|---|---|
| F3-01 | GitHub schema | Issue Forms mission/packet, JSON schema handoff/state/command | F2 |
| F3-02 | Impact policy | policy/schema/stdlib validator, closure có hướng, candidate report read-only | F2 |
| F3-03 | Agent adapters | `work-packet`, `cross-review`, `land-packets`; `CLAUDE.md` và `AGENTS.md` chỉ trỏ protocol | F2 |
| F3-04 | Security | permissions tối thiểu, security paths, CODEOWNERS, cấm LIVE credential trong worker | F2 |
| F3-05 | Derived metadata | `planned:changelog.d/`, worker cấm version/r number, land-owned metadata | F1, F2 |
| F3-06 | Worker gate | manifest tạm ngoài repo, fragment tests, write-set/EOL/security checks, không provider secret | F3-01…05 |
| F3-07 | Land gate | generate bundled/changelog/version/manifest, parity, dry-run `land prepare` | F3-01…06 |
| F3-08 | Adapter parity | test Claude/Codex adapter cùng schema, stop condition và completion contract | F3-03, F3-06 |

Không cho F3-06 và deferred numbering active riêng. Cả hai chỉ bật trong F4.

### F4 — Zero-legacy cutover

1. Inventory mọi PR/branch còn ghi version, changelog hoặc manifest.
2. Merge, đóng hoặc chuyển chúng sang packet v1; không gán lane theo tuổi branch.
3. Chạy worker gate và land gate trên ba fixture: code-only, docs-only, fragment-only.
4. Land activation PR ghi `protocol_version: 1` và `protocol_cutover_sha`.
5. Chuyển required checks một lần; xóa/disable legacy writer path.
6. Cập nhật đoạn «PHÁT HÀNH & NHÁNH (ADR-0001)» ở `SKILL.md` dòng 38 và bảng dòng 306 sang ADR-0017 —
   tệp byte-lock 48.031 B: cân bằng byte hoặc chấp nhận cascade golden/GOTCHAS/manifest; user re-import
   Capabilities sau khi land.
7. Chạy hai packet canary thủ công, write set không giao, một Codex và một Claude.

Foundation gate chỉ xanh khi hai canary cùng qua worker gate, merge tuần tự vào integration và land mà
không ai sửa release metadata trên worker branch.

Rollback F4: revert activation PR (trả required checks về legacy) — CHỈ hợp lệ khi chưa packet wp nào
land; sau packet đầu tiên chỉ fix-forward, không quay lui.

### A3 — Dispatcher shadow, chưa gọi model

Mã orchestration dev-side đặt dưới `planned:.github/coordination/`; workflow chỉ gọi core này. Mỗi module
có contract nhỏ, test bằng fake GitHub store; không mock qua HTTP mạng.

| Packet | Kết quả | Có thể song song với |
|---|---|---|
| A3-01 | pure domain model, state transition, schema/versioning | A3-02 |
| A3-02 | durable inbox fact, projection, event journal và hash-chain checkpoint | A3-01 |
| A3-03 | reconciler sort `(created_at,id)`, idempotency và pagination | không; phụ thuộc 01–02 |
| A3-04 | lease/generation/heartbeat/takeover và stale fencing | A3-05 nếu file không giao |
| A3-05 | path normalization, change-impact closure và global write-set exclusion | A3-04 |
| A3-06 | successor dedupe, budget reservation và circuit-breaker state | sau A3-03 |
| A3-07 | integration branch/PR planner dry-run | sau A3-03–06 |
| A3-08 | shadow workflow: issue trigger chỉ wake; scheduled/manual reconcile | sau 01–07 |
| A3-09 | stress fixtures: burst, reordered wake, retry, edit/delete, overflow, projection loss | sau A3-08 |

Promotion gate A3: zero model call, zero provider secret, zero canonical write. Ba inbox fact burst không mất;
retry cùng ID chỉ apply một lần; chain hỏng chuyển `paused` có audit.

### A4 — Cloud canary một provider

1. A4-01: provider-neutral executor interface và output schema.
2. A4-02: chọn provider canary theo credential có thể scope/quota; không dùng session token cá nhân chép
   vào prompt hay repo.
3. A4-03: OIDC broker là đích; secret provider trực tiếp chỉ là bước chuyển tiếp có owner/expiry.
4. A4-04: một packet offline, `max_parallel_workers=1`, không successor, không security path.
5. A4-05: thu hồi credential và quota test; workflow branch code không nhìn thấy credential.

Nếu tài khoản không có credential automation được hỗ trợ, A4 `paused`; không lách bằng raw cookie/token.

### A5 — Dual provider và review phân tầng

- A5-01: adapter Claude và Codex cùng executor contract.
- A5-02: reviewer read-only, verdict schema `approve|changes_requested|blocked`.
- A5-03: `cross_approved`, `same_provider_approved`, `review_deferred` và các risk không được defer.
- A5-04: rate-limit/quota fingerprint, reset time và circuit breaker; quota failure không tính attempt nội dung.
- A5-05: canary hai packet không giao; Claude review Codex và Codex review Claude.

### A6 — Successor tự động và Android

- A6-01: validate handoff và successor key; retry workflow không sinh Issue trùng.
- A6-02: enforcement `max_packets`, depth, attempt, run minute, invocation và cloud minute.
- A6-03: `used/reserved/limit`, preflight `budget_infeasible` và PAUSE thay vì tiêu hết token.
- A6-04: parser/authorization chung cho comment và typed workflow dispatch.
- A6-05: GitHub Mobile test: start/pause/resume/reroute và `land apply` stale-head negative test.

### A7 — Local controller trên Windows

Controller nằm dưới `planned:.github/coordination/local_controller.py` hoặc wrapper rất mỏng gọi cùng
core; không tạo generic self-hosted runner.

| Packet | Nội dung | Nghiệm thu |
|---|---|---|
| A7-01 | poll packet local, validate lease, tạo worktree/branch | reboot không sinh worktree/branch trùng |
| A7-02 | launcher `codex exec` và `claude -p`, timeout, JSON handoff | process exit/timeout/quota được phân loại |
| A7-03 | heartbeat và stale-generation kill | worker cũ không push/handoff sau takeover |
| A7-04 | Scheduled Task dưới tài khoản ít quyền | log không secret; start-at-boot/recovery test |
| A7-05 | cleanup sau canonical readback | không xóa worktree bẩn/stale còn cần preserve |

### A8 — Land automation và completion

1. `land prepare`: freeze mission, exact integration head, generate derived files, parity/full gate, draft PR.
2. `land apply`: pure operation không model call, không sửa diff; kiểm actor, environment approval, exact SHA.
3. Ba client: local skill, authorized Issue comment và typed `workflow_dispatch`.
4. Neo mission ID + final state hash vào canonical; readback khớp rồi mới `complete`/cleanup.
5. Deploy LIVE vẫn là operation khác, không tự chạy sau merge.

Promotion gate A8: chạy nhiều mission liên tiếp không stale lease, event loss, duplicate packet,
out-of-effective-write-set hay sai derived metadata; stale SHA và actor lạ bị từ chối có audit.

## 6. Ma trận song song theo pha

| Pha | Số writer tối đa | Điều kiện |
|---|---:|---|
| D0–F2 | 1 | canonical bẩn, release metadata/EOL/harness là nút toàn cục |
| F3 trước activation | 2 do người giữ | worktree riêng, write set/closure đối chiếu thủ công |
| F4 canary | 2 | một Claude, một Codex; không giao effective write set |
| A3 shadow | 2 | chỉ fake store/dry-run; zero model/secret/canonical write |
| A4 cloud canary | 1 | một provider, một packet, không successor |
| A5–A8 | 2 mặc định | dispatcher cấp lease; integration/land vẫn single-writer |

## 7. Runbook cài đặt và kiểm tra Windows

### 7.1 Sửa Claude Code trước

> **Đo 03-08 ~09:45: bước này ĐÃ HOÀN THÀNH** — native 2.1.220 tại `C:\Users\admin\.local\bin\claude.exe`,
> `where.exe claude` đúng một đường. Giữ runbook dưới đây để tái lập máy mới; việc còn lại chỉ là
> `claude doctor` + login/workspace trust.

Máy hiện không có Microsoft Desktop App Installer/WinGet, vì vậy dùng native installer chính thức
của Anthropic là đường chuẩn. Chỉ giữ một installation. Thực hiện trong PowerShell 64-bit bình
thường, không cần Administrator:

```powershell
where.exe claude
npm uninstall -g @anthropic-ai/claude-code
irm https://claude.ai/install.ps1 | iex

# Mở PowerShell mới, rồi kiểm:
where.exe claude
claude --version
claude doctor
```

WinGet chỉ là phương án phụ khi `Get-Command winget.exe` trả về lệnh hợp lệ:

```powershell
winget install Anthropic.ClaudeCode
```

Nếu `where.exe claude` còn nhiều bản, dừng và gỡ bản cũ trước khi chạy. Không chép credential
Claude vào repo hay worktree. Chạy `claude` một lần trong repo để login và accept workspace trust.

### 7.2 Kiểm Codex, Git và GitHub

```powershell
codex --version
codex doctor
git --version
gh --version
gh auth status
python --version
pwsh --version
```

Không dùng `--dangerously-bypass-approvals-and-sandbox`. Codex executor dùng `workspace-write`; reviewer dùng
`read-only`. Trên Claude native Windows, protocol/hook/permission phải chặn write cho reviewer vì native Windows
không có sandbox tương đương WSL2.

## 8. Runbook chạy Codex và Claude đồng thời

Runbook này dùng sau F4 activation. Trước F4, chỉ dùng nó như pilot có người giữ claim và không
cho hai agent chạm code/metadata dùng chung.

### 8.1 Tạo mission và hai packet không giao

Ví dụ:

- `wp101`: Codex, chỉ sửa module A và fragment `wp101_*`;
- `wp102`: Claude, chỉ sửa module B và fragment `wp102_*`;
- không packet nào sửa VERSION, `CHANGELOG.md`, manifest, bundled module, security path hay integration branch.

Trên GitHub, tạo mission Issue và hai packet Issue. Đóng băng objective, acceptance, write set, dependency,
executor và environment trước khi claim. Nếu chưa có dispatcher, người giữ phải tự tính closure và xác
nhận hai tập không giao.

### 8.2 Tạo integration branch và hai worktree

```powershell
$Repo = 'D:\Quốc hội\tra-luat'
$WtRoot = 'D:\Quốc hội\tra-luat-wt'
$Mission = 100

New-Item -ItemType Directory -Path $WtRoot -Force | Out-Null
git -C $Repo fetch origin master

git -C $Repo branch "mission/$Mission/integration" origin/master
git -C $Repo push -u origin "mission/$Mission/integration"

# base = head integration hiện tại (ADR-0027); mission mới thì nó trùng origin/master
git -C $Repo worktree add "$WtRoot\wp101-codex" -b "agent/wp101-g1-codex" "mission/$Mission/integration"
git -C $Repo worktree add "$WtRoot\wp102-claude" -b "agent/wp102-g1-claude" "mission/$Mission/integration"
git -C $Repo worktree list
```

Không tạo hai phiên trong cùng thư mục. Không dùng current dirty `master` làm base. Không thêm secret
vào `.worktreeinclude`; nếu packet cần tài nguyên local có credential, dừng và route sang local operation
được thiết kế riêng.

### 8.3 Mở Codex executor

Trong PowerShell thứ nhất:

```powershell
$CodexWt = 'D:\Quốc hội\tra-luat-wt\wp101-codex'
codex -C $CodexWt -s workspace-write -a on-request
```

Prompt ban đầu:

```text
Đọc docs/PROTOCOL_DA_PHIEN.md và AGENTS.md.
Nhận packet wp101, generation 1, executor codex, branch agent/wp101-g1-codex.
Chỉ sửa effective write set ghi trong Issue <URL>.
Không sửa VERSION, CHANGELOG.md, RELEASE_MANIFEST.json, bundled test module, security path hoặc file ngoài set.
Thêm regression test trong fragment wp101_*; chạy worker gate.
Khi xong, commit/push branch, mở PR vào mission/100/integration và xuất handoff đúng schema.
Nếu closure thiếu, generation/spec sai, cần LIVE hoặc gần hết budget: PAUSE, không tự nới quyền.
```

Headless sau A7 dùng cùng packet prompt/schema:

```powershell
$HandoffSchema = 'D:\Quốc hội\tra-luat\.github\coordination\schemas\handoff.v1.schema.json'
$HandoffJson = 'D:\Quốc hội\tra-luat-wt\wp101-codex\.coord\handoff.json'
$PacketPrompt = 'Thực thi packet wp101 từ Issue URL theo Protocol v1.'
codex exec -C $CodexWt -s workspace-write --output-schema $HandoffSchema -o $HandoffJson $PacketPrompt
```

### 8.4 Mở Claude executor

Trong PowerShell thứ hai:

```powershell
$ClaudeWt = 'D:\Quốc hội\tra-luat-wt\wp102-claude'
Set-Location -LiteralPath $ClaudeWt
claude --remote-control 'wp102-claude'
```

Prompt giống Codex nhưng thay packet/executor/branch thành `wp102`, `claude`, `agent/wp102-g1-claude`.
`--remote-control` cho phép theo dõi phiên local trên Android; máy Windows và process Claude vẫn phải thức.
Muốn máy tắt mà việc tiếp tục thì packet phải route `environment: cloud`, không phải Remote Control.

Claude Code cũng có `claude --worktree <name>`, nhưng runbook này tạo worktree bằng Git để branch,
generation và base SHA khớp lease contract, thay vì để client tự đặt tên.

### 8.5 Theo dõi và chặn trùng việc

Người giữ hoặc dispatcher kiểm bốn thứ, không chỉ nhìn label:

1. packet ID/generation/spec hash;
2. branch và worktree path;
3. effective write set + policy SHA;
4. heartbeat/lease expiry.

Mở rộng write set phải pause cả packet, tạo revision/generation mới rồi mới tiếp tục. Không nhắn hai
agent “tự chia nhau file” trong chat.

### 8.6 Review chéo và integrate

- Claude PR do Codex review read-only; Codex PR do Claude/human review read-only.
- Reviewer không checkout và ghi vào executor worktree.
- Mỗi PR rebase trên integration head mới và chạy lại worker gate trước merge.
- Dispatcher/người giữ merge từng PR vào integration, không cho hai executor tự merge.

Codex review thủ công có thể chạy trong checkout reviewer riêng:

```powershell
codex exec -C <review-worktree> -s read-only review --base origin/mission/100/integration `
  'Review theo Spec và Standards/Security; không sửa file; xuất verdict có evidence.'
```

Sau cùng, land worktree duy nhất sinh version/changelog/bundled module/manifest và draft PR vào canonical.

### 8.7 Kết thúc và dọn worktree

Chỉ dọn sau khi PR đã integrated/landed, handoff đã ghi, branch clean và canonical readback khớp:

```powershell
git -C "$WtRoot\wp101-codex" status --short
git -C "$WtRoot\wp102-claude" status --short
git -C $Repo worktree remove "$WtRoot\wp101-codex"
git -C $Repo worktree remove "$WtRoot\wp102-claude"
git -C $Repo worktree prune --dry-run
```

Nếu `status --short` không rỗng, dừng; không `--force`, không xóa thư mục bằng tay.

## 9. Tiếp tục từ Android

Ba bề mặt có vai trò khác nhau:

- **GitHub Mobile:** control plane bền; đọc Issue/PR/check, approve, chạy typed workflow và gọi `land apply`.
- **Claude app/Code tab:** theo dõi cloud session hoặc Remote Control tới host local; local host phải online.
- **ChatGPT Mobile/Remote tab:** tiếp tục Codex task trên host Windows đã pair; host giữ file, shell và credential.

Checklist:

1. Cập nhật app desktop/mobile, pair từng thiết bị với host.
2. Đặt tên task theo `wp<issue>-<executor>` để không chọn nhầm phiên.
3. Trên điện thoại chỉ steer/approve; không dùng chat history làm state chính.
4. Khi host tắt, theo dõi packet cloud qua GitHub; packet local phải ở `paused`/queued.
5. Land từ Android phải nhập/chọn exact `mission_id` và `head_sha`; stale SHA phải bị từ chối.

## 10. Evidence và báo cáo mỗi promotion gate

Mỗi epic lưu một report non-normative gồm:

- base/head SHA, protocol version, policy SHA;
- packet/PR/workflow run IDs;
- gate matrix Windows–Linux;
- budget `used/reserved/limit` và provider error fingerprint;
- race/negative tests đã chạy;
- secret inventory theo **tên** secret, không ghi giá trị;
- kill switch/rollback đã test;
- quyết định promote, pause hay rollback và người duyệt.

## 11. Definition of done của kế hoạch

Kế hoạch chỉ được đánh dấu hoàn tất khi toàn bộ tiêu chí mục 17 của protocol đã có evidence,
không chỉ vì hai terminal cùng chạy. Tối thiểu phải có:

- hai executor song song không giao effective write set;
- stale generation, duplicate successor, out-of-set diff và event loss đều có negative test;
- EOL/bundled output cùng byte trên Windows–Linux;
- không worker job nào có LIVE credential;
- Windows reboot/local recovery và cloud-host-off test;
- Android stale-head/unauthorized-actor test;
- mission chỉ `complete` sau canonical readback; deploy không tự chạy.

## 12. Nguồn khả năng nền tảng

- [Claude Code worktrees](https://code.claude.com/docs/en/worktrees)
- [Claude Code Remote Control](https://code.claude.com/docs/en/remote-control)
- [Claude Code Windows installation](https://code.claude.com/docs/en/installation)
- [Claude Code skills](https://code.claude.com/docs/en/slash-commands)
- [Codex Remote GA trên Windows/mobile](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- [ChatGPT Work và Codex Remote tab](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex)
- [Codex Windows sandbox](https://openai.com/index/building-codex-windows-sandbox/)
- [GitHub Actions concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency)
- [GitHub workflow dispatch](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)

## 13. Phụ lục — số đo nền 2026-08-03 (~09:45, non-normative)

Đo bởi phiên độc lập trên worktree sạch tách từ `origin/master` (`ac63cd7` = r326/v1.36.58);
ADR/Protocol thắng nếu số liệu dưới đây cũ đi.

- **Cổng tài liệu:** HAI lần `doc-claims-check --strict` trên worktree sạch + trọn bộ D0
  (CONTEXT + PROTOCOL + ADR-0001-Superseded + ADR-0017…0033 + research + kế hoạch này, lần 2 gồm cả
  kế hoạch): `ok:true`, rc=0, **0 blocking**; ~314 advisory đều thuộc tài liệu CŨ có sẵn
  (vd `docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md`), không phải bộ D0. Quy ước `planned:` qua cổng
  thật, không cần dạy thêm mã. Lưu ý cơ chế: tài liệu `docs/` thuộc lớp historical ⇒ path-missing
  chỉ là ADVISORY — nghĩa là cổng không chặn, nhưng cũng KHÔNG chứng minh mọi con trỏ trong docs/ sống.
- **Đo lần 3 (~10:15, SAU khi hoàn thiện kế hoạch, trên nền master MỚI r327/v1.36.59):** `ok:true`,
  314 advisory đúng baseline cũ, **0 advisory thuộc bản kế hoạch hoàn thiện**. Vẫn phải đo lại y hệt
  trên đúng cây sẽ commit khi vào PR D0 (D0-02).
- **Toolchain:** `claude` native 2.1.220 (một đường duy nhất, xem §7.1); `codex-cli 0.146.0`;
  winget KHÔNG có; `gh auth` OK (tài khoản ducthangho).
- **Git:** PR #22 (r327/v1.36.59, nhánh `nifty-diffie-63b72e`, vá phép dò auth `gws`) MỞ lúc ~09:45 và
  **ĐÃ MERGE trước ~10:15** — master nay r327/v1.36.59, 0 PR mở, số trống kế tiếp r328/v1.36.60;
  cửa sổ zero-open-PR ĐANG MỞ cho D0. 9 worktree sống (đo ~02:00 cùng ngày): cây chính
  (bẩn ~19 tệp M + bộ ADR untracked) · luot3_wt · p16_wt · rasoat_docs_wt · rebase19_wt (detached) ·
  rel05_wt · wt_r323 · nifty-diffie-63b72e · recursing-nightingale-76526b — đầu vào trực tiếp cho
  T0-04 và F2-00.
- **`.gitattributes` @HEAD:** `* -text` (khoá byte, v1.33.61) + `*.sh text eol=lf` +
  `references/golden/** -text` — khớp tiên đề §2; F2-A thay chính sách này.
- **CLAUDE.md** dòng 74 và 91 vẫn dạy bump VERSION mọi đợt — đích sửa của F3-03.
- **PROTOCOL** có mục 17 thật (dòng 482) — con trỏ ở §11 đúng.
- **Phạm vi doc-claims:** roots = CHANGELOG.md · SKILL.md · CLAUDE.md · CONTEXT.md · references ·
  docs (`scripts/tl_core/workflow.py` dòng 775); lớp mồ côi L9 phủ cả `docs/adr` (dòng 822-824) —
  17 ADR mới KHÔNG nổ L9 trong cả hai lần đo.
