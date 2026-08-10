# F2-D — kiểm kê writer trước khi mở lại

## Kết luận

**Verdict: `blocked`. Writer VẪN phải giữ trạng thái đóng băng.**

Đo lại trên host Windows trong generation 2 tại `2026-08-10T21:14:45+07:00` đến
`2026-08-10T21:16:23+07:00`. Canonical `b044f8b14e9ea3ad5d91a7fb4f0d29a3fe8415eb`.
Commit EOL chuẩn `1880346d2be3c0be9a93de7624ee108d99b6c88c`.

Blocker **cưỡng chế** đã ĐÓNG (#52 land, merge `578724e5` — xem §5). Blocker **kiểm kê** còn MỞ:

- 73 remote branches chưa chứa commit EOL: **69 `close` · 3 `rebase` · 1 `finish rồi rebase`**.
- **43/73 branches có `owner=unknown`** — không có bằng chứng owner trực tiếp từ PR. Không suy owner
  từ namespace, tên nhánh hay tác giả commit.
- 4 branches non-ancestor mang nội dung chưa land/chưa đủ evidence tương đương (§4.3). Chúng không
  được `close`; riêng row 6 đã đổi từ `close` sang `rebase`.
- `blocker_worktree_measurement=closed`: host inventory thật có **99 live, 0 prunable; 49 chứa EOL /
  50 legacy; 94 clean / 5 dirty; 98 owner unknown** (§4.5). Việc đo xong không đồng nghĩa worktrees
  đã được xử lý: 50 legacy, 5 dirty và owner/consent chưa đủ vẫn giữ writer inventory mở.

Artifact này CHỈ là inventory/decision record. F2-D **không** xoá remote branch, không prune/remove
worktree, không rebase, không force-push, không sửa dữ liệu dirty, không mở writer, không sửa hook/CI.

Mọi mục `close` chỉ được THỰC THI sau khi owner được xác nhận. Với 43 mục `owner=unknown`, quyết định
`close` là **đề xuất có căn cứ**, chưa phải uỷ quyền xoá.

## 1. Nguồn điều phối

- Mission: [#48](https://github.com/ducthangho/tra-luat/issues/48), revision 2 ·
  plan hash `340b15a934cc27f2aa5d542973e12c268ab4db4307b390a77e66bc9d6a060d11`.
- Human MCR: [MCR-48-01](https://github.com/ducthangho/tra-luat/issues/48#issuecomment-5227303367).
- Packet: [#63](https://github.com/ducthangho/tra-luat/issues/63), revision 1 / generation 2 ·
  spec hash `de63e124ed39a94108f87770c2bec9ec39a25119795ce9f6534d7084fd4d0fea`.
- Human decision/lease generation 2: [#63 comment 5241393193](https://github.com/ducthangho/tra-luat/issues/63#issuecomment-5241393193) — Codex Executor, local Windows, kế thừa PR #80/head `fe9395ba3f2379e0a2b670ecfb6224103c944d54`.
- Stable review findings: [#63 comment 5241307078](https://github.com/ducthangho/tra-luat/issues/63#issuecomment-5241307078) — `WP63-RV-01/02/03`.
- Parent drain packet: [#49](https://github.com/ducthangho/tra-luat/issues/49) — `state:landed`.
- Enforcement packet: [#52](https://github.com/ducthangho/tra-luat/issues/52) — `state:landed`.
- Reconcile trước authorization: [#63 comment 5241334459](https://github.com/ducthangho/tra-luat/issues/63#issuecomment-5241334459).
- Artifact tiền nhiệm: PR [#64](https://github.com/ducthangho/tra-luat/pull/64), head
  `86dc0705c796d4436df00d7accc47e219282c858` — **ĐÃ ĐÓNG** (không merge) theo chỉ đạo chủ kho, được
  THAY THẾ bởi PR #80 mang chính artifact này. Xem §6 — sai lệch đã sửa. Nhánh
  `codex/f2-d-reopen-writer` không bị xoá; nó CHỨA EOL base nên không nằm trong 73 nhánh legacy.

Readback fail-closed, rc đọc trực tiếp:

```
GET /pulls/80: state=open, draft=false, head=fe9395ba3f2379e0a2b670ecfb6224103c944d54
git ls-remote origin refs/heads/claude/reopen-writer-eol-drain-b1dj5m
→ fe9395ba3f2379e0a2b670ecfb6224103c944d54, rc=0
git merge-base --is-ancestor 1880346d… b044f8b1…   → rc=0   EOL base là ancestor của canonical
git merge-base --is-ancestor 91d5e8dc… b044f8b1…   → rc=0   base lúc mint là ancestor
git merge-base --is-ancestor 578724e5… b044f8b1…   → rc=0   merge #52 là ancestor
```

## 2. Phạm vi đo — host Windows thật

Phiên này khớp frozen packet: `executor=codex`, `environment=local-windows`, chạy trong isolated
worktree `D:/Quốc hội/tra-luat/work/wp63-g2-codex` từ exact inherited head. Shared main worktree
không bị switch hay sửa; mọi worktree khác chỉ được đọc. Isolated Executor worktree là entry thứ
99, giải thích chênh `98 → 99` so với phép đo Reviewer ngay trước authorization.

`git worktree list --porcelain` rc=0; stdout có 99 entry và được chép đủ vào §4.5. SHA-256 của
stdout chuẩn hóa LF là `bdc47ef42ecf13a0fc7736aa92858320ee9c02aca893dffbe6519b4ffce168c7`.
`git worktree prune --dry-run --verbose` rc=0, stdout rỗng: **0 prunable**. Không chạy prune thật,
không remove/rebase và không ghi vào worktree nào khác.

## 3. Phương pháp

```text
git fetch origin --prune
git branch -r --no-contains 1880346d2be3c0be9a93de7624ee108d99b6c88c
git merge-base --is-ancestor <exact-tip> b044f8b1…
git -c safe.directory=<path> -C <path> status --short --untracked-files=all
git merge-base --is-ancestor 1880346d… <worktree-head>
git merge-base --is-ancestor <worktree-head> b044f8b1…
git worktree list --porcelain
git worktree prune --dry-run --verbose
```

| Phép đo | rc | Kết quả |
|---|---:|---|
| `git fetch origin --prune` | 0 | full remote refs refreshed; base không drift |
| `git branch -r` (tổng, trừ `origin/HEAD`) | 0 | **93** |
| `git branch -r --no-contains <EOL>` | 0 | **73** |
| `git branch -r --contains <EOL>` | 0 | **20** |
| Parse bảng exact tips + đối chiếu remote refs | 0 | **73 rows; 0 resolve failure; 0 tip mismatch** |
| Graph completeness | 0 | non-shallow; no replace/graft; canonical/r210 objects present |
| `merge-base --is-ancestor <exact-tip> canonical` ×73 | 0 cho 69; 1 cho 4 | rows 1/6/13/49 non-ancestor |
| `r210` exact tip `d82ef707f…` → canonical | 0 | ancestor |
| `git worktree list --porcelain` | 0 | **99 live** (§4.5) |
| `git worktree prune --dry-run --verbose` | 0 | 0 prunable |
| `status --short` ×99 | 0 cho 99 | **94 clean / 5 dirty** |
| PR mapping (`list_pull_requests`, state=all) | 0 | 49 PR; **30** nhánh có PR, **43** không |

### 3.1 Graph completeness và exact-tip reconstruction

Phép đo full-history không dùng aggregate cũ. Script parse lại 73 dòng của §4.4, resolve từng SHA
thành commit 40 ký tự, đối chiếu `refs/remotes/<branch>`, rồi chạy ancestry trên từng exact tip.

```text
git rev-parse --is-shallow-repository             false, rc=0
git replace -l                                    <empty>, rc=0
.git/info/grafts present                          false
GIT_REPLACE_REF_BASE                              unset
git cat-file -e b044f8b1…^{commit}                rc=0
git cat-file -e d82ef707f…^{commit}                rc=0
parsed_rows=73; tip_ref_mismatches=0
ancestor_rc0=69; non_ancestor_rc1=4; other_rc=0
non_ancestor_rows=1,6,13,49
r210_row=16; r210_rc=0
```

## 4. Remote branches chưa chứa EOL (73)

### 4.1 Quy ước bằng chứng

Ancestry của **exact tip** là basis chính: 69 rows rc=0 được `close`; 4 rows rc=1 phải có evidence
hai chiều hoặc giữ `rebase`/`finish rồi rebase`. CHANGELOG, merged PR và “0 added files” chỉ là
corroboration; chúng không được dùng để tự đóng một non-ancestor row.

Quy ước owner: chỉ ghi owner khi có **tác giả PR** làm bằng chứng trực tiếp. Ngoài ra là `unknown`.
Tên nhánh (`claude/…`, `codex/…`) là **routing hint, KHÔNG phải owner evidence**.

Quy ước decision:

- `close` — nội dung đã land hoặc đã bị canonical thay thế; **thực thi chỉ sau khi owner xác nhận**.
- `rebase` — còn giá trị chưa land, cần cập nhật lên base chứa EOL.
- `finish rồi rebase` — còn dữ liệu cần triage/hoàn tất trước, rồi mới rebase.

### 4.2 Vì sao `git cherry` KHÔNG dùng được ở đây

Đã thử và **bác bỏ**: `git cherry b044f8b1 origin/claude/r276-…` trả **356/356 dấu `+`**, tức "không
có commit nào đã ở upstream" — kết luận đó SAI. Nguyên nhân cấu trúc: `git cherry` so bằng patch-id,
mà migration EOL (F2-B) đã renormalize CRLF→LF hàng loạt, nên **không patch-id nào của commit
tiền-EOL còn khớp** với canonical hậu-EOL. Sau ADR-0018, patch-id equivalence là công cụ MÙ với mọi
nhánh tiền-EOL — đừng dùng nó làm bằng chứng land.

### 4.3 Bốn nhánh non-ancestor — đo đích danh

| Nhánh | Bằng chứng (rc trực tiếp) | Decision |
|---|---|---|
| `origin/claude/cuu-viec-treo-2026-08-03` | 2 commit riêng (`d347129…`, `6c148d3…`), 40 path đổi từ merge-base; so exact tip với canonical: 19 blob giống, **21 blob khác**; 9 test name `r323_/r324_` thêm bởi branch đều `git grep` canonical rc=**1**. Chưa có evidence hành vi hai chiều | `rebase` |
| `origin/claude/ras-17-data-pr13-windows-bjovq2` | Behavioral A/B trên exact tip/canonical, cùng fixture và command dưới đây: tip rc=**0**, lập 1 migration; canonical rc=**2**, CLI bác subcommand. Control trên tip không đủ Điều trả 0 migration + lý do fail-closed ⇒ khác biệt là hành vi, không phải lỗi dựng môi trường | `rebase` |
| `origin/claude/nlm-registry-sheet-dup-s22fk7` | 2 tệp chỉ có trên nhánh; `git cat-file -e b044f8b1:rasoat/KETQUA_R281_V1_V2_V3_2026-07-31.md` rc=**128** | `rebase` |
| `origin/claude/audit-errors-patch-plan-56x4rq` | 1 tệp chỉ có trên nhánh; `git cat-file -e b044f8b1:docs/AUDIT_XAC_MINH_VA_KE_HOACH_VA_2026-07-31.md` rc=**128** | `finish rồi rebase` |

Behavioral evidence row 49 (mỗi tree detached ở đúng SHA; env credential/cache bị bỏ, `HOME` trỏ thư mục
trống; không dùng `GIT_CONFIG_*`):

- Positive fixture: `master/unit.json` có một dep `so_hieu=18/2025/VBHN-VPQH`,
  `text_hash=cache:18-2025-VBHN-VPQH#dieu54`, `dieu=["54"]`; `cache/docs/a.json` khai cùng số hiệu và
  `articles.54="Điều 54. Mức hưởng ..."`. Chạy từ mỗi tree:
  `python scripts\tl.py rasoat-anchor --in ..\wp63-row49-fixtures\positive\master --cache-dir ..\wp63-row49-fixtures\positive\cache --json`.
  Exact tip `411b3f3fb74945934a82c8dc203cd523e0d31cf0`: rc=**0**,
  `che_do=DRY`, `da_ghi=false`, `ke_hoach.di_tru=1`, `locator_trong_hash: 1→0`,
  `findings_sau.san_sang=true`. Canonical `b044f8b14e9ea3ad5d91a7fb4f0d29a3fe8415eb`: rc=**2**,
  `invalid choice: 'rasoat-anchor'`.
- Negative/control fixture: giữ cache trên nhưng dep yêu cầu `dieu=["99"]` và locator `#dieu99`. Cùng
  command với `positive` đổi thành `negative` trên exact tip: rc=**0**, `ke_hoach.di_tru=0`,
  `ke_hoach.bo_qua=1`, `THIEU_DIEU_TRONG_CACHE:99`, `findings_sau.san_sang=false`. Control này chứng minh
  runner/CLI đã dựng đúng và fixture làm thay đổi kết quả theo dữ liệu đầu vào.

Đối chiếu: `69 close + 3 rebase + 1 finish rồi rebase = 73`; phân lớp chính:
`69 ancestor + 4 non-ancestor = 73`.

### 4.4 Bảng kiểm kê

Bảng dưới được tái tạo trong generation 2 từ đúng 73 rows. Cột Tip hiển thị 12 hex để gọn nhưng
mỗi giá trị đã resolve thành commit 40 hex và khớp exact current remote ref (`tip_ref_mismatches=0`).
Với mọi row ngoài 1/6/13/49, basis quyết định chính là exact-tip ancestry rc=0; nội dung cuối dòng
nếu khác chỉ là corroboration lịch sử.

| # | Remote branch | Tip | Commit date | Owner / bằng chứng | Decision | Basis (lệnh + rc) |
|---:|---|---|---|---|---|---|
| 1 | `origin/claude/audit-errors-patch-plan-56x4rq` | `4c0332f05252` | `2026-07-31T16:01:11+00:00` | `unknown` | `finish rồi rebase` | 1 tệp chỉ có trên nhánh: `docs/AUDIT_XAC_MINH_VA_KE_HOACH_VA_2026-07-31.md`; cần owner triage trước |
| 2 | `origin/claude/baotri-kho-bhxh-luot2` | `fcf9053537cb` | `2026-08-02T21:32:25+07:00` | `ducthangho` — tác giả PR #16 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 3 | `origin/claude/bhxh-41-2024-maintenance-jncsle` | `c0cbc96bbbee` | `2026-08-02T12:11:23+00:00` | `ducthangho` — tác giả PR #13 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 4 | `origin/claude/codex-exclude-dir` | `1050c17fb96b` | `2026-08-04T00:52:22+07:00` | `ducthangho` — tác giả PR #30 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 5 | `origin/claude/corpus-audit-write-2026-07-31-3twkfb` | `3500f1fde2b7` | `2026-07-31T04:34:33+00:00` | `unknown` | `close` | 0 tệp chỉ có trên nhánh (`diff --diff-filter=A` rỗng) — bị canonical thay thế |
| 6 | `origin/claude/cuu-viec-treo-2026-08-03` | `6c148d331e5d` | `2026-08-04T00:21:52+07:00` | `unknown` | `rebase` | ancestry rc=1; 2 commit/40 path; 21 blob khác canonical; 9 test name vắng canonical — chưa có evidence hành vi hai chiều |
| 7 | `origin/claude/deploy-v1-35-61-ci-5f7wdw` | `e094512a37ca` | `2026-07-29T02:48:58+00:00` | `ducthangho` — tác giả PR #2, #1 | `close` | PR #2, #1 merged; 0 tệp chỉ có trên nhánh |
| 8 | `origin/claude/gate-04-05-t0f-hi76xl` | `eb9132f3aa2b` | `2026-08-02T09:45:41+00:00` | `ducthangho` — tác giả PR #12, #9, #8 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 9 | `origin/claude/legal-doc-review-architecture-2al46n` | `f39f98398d7b` | `2026-07-26T08:06:51+07:00` | `unknown` | `close` | 0 tệp chỉ có trên nhánh (`diff --diff-filter=A` rỗng) — bị canonical thay thế |
| 10 | `origin/claude/luat-bhxh-30-07-fyc9tq` | `3e9a90c77f69` | `2026-07-30T09:12:32+00:00` | `ducthangho` — tác giả PR #5 | `close` | PR #5 merged; 0 tệp chỉ có trên nhánh |
| 11 | `origin/claude/nifty-diffie-63b72e` | `45513c5b4358` | `2026-08-03T09:51:42+07:00` | `ducthangho` — tác giả PR #22 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 12 | `origin/claude/nlm-queue-vbqppl-56qz82` | `e234bd38e24b` | `2026-07-31T02:53:10+00:00` | `unknown` | `close` | 0 tệp chỉ có trên nhánh (`diff --diff-filter=A` rỗng) — bị canonical thay thế |
| 13 | `origin/claude/nlm-registry-sheet-dup-s22fk7` | `0bb60d215c02` | `2026-07-31T06:25:47+00:00` | `unknown` | `rebase` | 2 tệp chỉ có trên nhánh (`cat-file -e` canonical rc=128): `rasoat/KETQUA_R281_…`, `rasoat/PROMPT_TIEP_…` |
| 14 | `origin/claude/p15-review-tra-luat-osp5td` | `cc20b71e855e` | `2026-07-30T20:37:05+00:00` | `unknown` | `close` | 0 tệp chỉ có trên nhánh (`diff --diff-filter=A` rỗng) — bị canonical thay thế |
| 15 | `origin/claude/prompt-phien-ke-sau-rc-21og1d` | `fa255e827eef` | `2026-07-25T09:31:40+00:00` | `unknown` | `close` | 0 tệp chỉ có trên nhánh (`diff --diff-filter=A` rỗng) — bị canonical thay thế |
| 16 | `origin/claude/r210-rasoat-dot2` | `d82ef707fb26` | `2026-07-26T07:15:50+07:00` | `unknown` | `close` | `r210` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 17 | `origin/claude/r211-rasoat-dot3` | `386c8ccffdc7` | `2026-07-26T08:06:00+07:00` | `unknown` | `close` | `r211` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 18 | `origin/claude/r212-guard-bind-path` | `c226ae165193` | `2026-07-26T08:53:42+07:00` | `unknown` | `close` | `r212` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 19 | `origin/claude/r213-rasoat-dot5` | `e9fea2d7a1d6` | `2026-07-26T11:44:27+07:00` | `unknown` | `close` | `r213` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 20 | `origin/claude/r215-khoi-dau-van-ban` | `b77306ec6cac` | `2026-07-27T11:06:09+08:00` | `unknown` | `close` | `r215` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 21 | `origin/claude/r216-rasoat-merge-cong-trung` | `23ab5f297654` | `2026-07-27T22:44:27+08:00` | `unknown` | `close` | `r216` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 22 | `origin/claude/r217-doc-patch-loc-congbao` | `e777cd294d9f` | `2026-07-28T00:23:26+08:00` | `unknown` | `close` | `r217` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 23 | `origin/claude/r219-doc-claims-l8-l9-gotchas` | `e8f2f85b010f` | `2026-07-28T03:19:26+08:00` | `unknown` | `close` | `r219` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 24 | `origin/claude/r221-verify-deep-t1-sohieu` | `036b63f68db6` | `2026-07-28T09:50:52+08:00` | `unknown` | `close` | `r221` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 25 | `origin/claude/r255-bare-vbhn-rasoat-chongcheo` | `264f562dbd89` | `2026-07-30T09:36:27+00:00` | `unknown` | `close` | `r255` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 26 | `origin/claude/r256-rasoat-loop-dry-rounds` | `008ce8259e0f` | `2026-07-30T09:37:57+00:00` | `unknown` | `close` | `r256` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 27 | `origin/claude/r257-sweep-corpus-predicate` | `4c75c591ba0c` | `2026-07-30T09:39:19+00:00` | `unknown` | `close` | `r257` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 28 | `origin/claude/r258-vbhn-goc-map-corpus-rule` | `433ec06e85a6` | `2026-07-30T09:40:38+00:00` | `unknown` | `close` | `r258` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 29 | `origin/claude/r259-dong-bo-so-r-trong-chu-thich` | `c833677518dc` | `2026-07-30T09:48:23+00:00` | `unknown` | `close` | `r259` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 30 | `origin/claude/r260-test-r255-r258-vao-selftest` | `c51319e45d07` | `2026-07-30T11:42:25+00:00` | `unknown` | `close` | `r260` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 31 | `origin/claude/r261-monkeypatch-dung-cua-stub` | `d63fec4cd18c` | `2026-07-30T12:04:38+00:00` | `unknown` | `close` | `r261` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 32 | `origin/claude/r262-selftest-hermetic-chan-mang` | `d82f3b311d29` | `2026-07-30T12:46:14+00:00` | `unknown` | `close` | `r262` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 33 | `origin/claude/r263-merge-legal-doc-review-architecture` | `cf6ae53ae6e9` | `2026-07-30T13:19:13+00:00` | `unknown` | `close` | `r263` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 34 | `origin/claude/r264-doc-claims-phu-docs` | `320952a64185` | `2026-07-30T13:39:28+00:00` | `unknown` | `close` | `r264` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 35 | `origin/claude/r266-doc-text-sanitize-u1` | `3e440eff0c19` | `2026-07-30T19:25:38+00:00` | `unknown` | `close` | `r266` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 36 | `origin/claude/r267-parity-4-reader-cache-u1` | `a4ebf7442c33` | `2026-07-30T20:27:05+00:00` | `unknown` | `close` | `r267` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 37 | `origin/claude/r268-r264-sha-may-phu-thuoc` | `cc20b71e855e` | `2026-07-30T20:37:05+00:00` | `unknown` | `close` | `r268` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 38 | `origin/claude/r269-dedup-status-active-alias` | `955965832168` | `2026-07-31T05:23:47+08:00` | `unknown` | `close` | `r269` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 39 | `origin/claude/r270-vbhn-for-goc-boundary` | `eed79ed24315` | `2026-07-31T05:31:03+08:00` | `unknown` | `close` | `r270` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 40 | `origin/claude/r271-hieuluc-negation-first` | `ae89d6fb35bb` | `2026-07-31T05:37:26+08:00` | `unknown` | `close` | `r271` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 41 | `origin/claude/r272-classify-ref-canonical-chon` | `49de1bb5c4e0` | `2026-07-31T05:55:32+08:00` | `unknown` | `close` | `r272` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 42 | `origin/claude/r273-vbhn-gate-cutoff-dong` | `ef3f64f5c7a8` | `2026-07-31T06:09:31+08:00` | `unknown` | `close` | `r273` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 43 | `origin/claude/r274-fixture-vbhn-nam` | `2fe439230ae8` | `2026-07-31T06:18:30+08:00` | `unknown` | `close` | `r274` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 44 | `origin/claude/r275-vbhn-base-key-tie-break` | `9c8e5b27eca8` | `2026-07-31T06:47:28+08:00` | `unknown` | `close` | `r275` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 45 | `origin/claude/r276-sohieu-khong-nam-detector` | `44da73864caa` | `2026-07-31T06:59:52+08:00` | `unknown` | `close` | `r276` có trong CHANGELOG canonical; 0 tệp chỉ có trên nhánh |
| 46 | `origin/claude/r323-tach-duoi-vbhn` | `9775d867eeaa` | `2026-08-03T00:38:04+07:00` | `ducthangho` — tác giả PR #18 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 47 | `origin/claude/r325-noi-lai-duoi-vbhn` | `1bdc16c73421` | `2026-08-03T02:04:23+07:00` | `ducthangho` — tác giả PR #20 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 48 | `origin/claude/ras-01-ras-14-metadata-cli-bi25ke` | `93a7dab7a4d4` | `2026-08-02T07:14:58+00:00` | `ducthangho` — tác giả PR #10 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 49 | `origin/claude/ras-17-data-pr13-windows-bjovq2` | `411b3f3fb749` | `2026-08-02T13:36:58+00:00` | `unknown` | `rebase` | Behavioral A/B §4.3: cùng positive fixture, tip rc=0 (`di_tru=1`, `san_sang=true`), canonical rc=2 (`invalid choice: 'rasoat-anchor'`); negative control trên tip rc=0 (`di_tru=0`, `THIEU_DIEU_TRONG_CACHE:99`) |
| 50 | `origin/claude/ras17-merge-gate-anchor` | `d8a3acee53b3` | `2026-08-02T20:42:11+07:00` | `ducthangho` — tác giả PR #15 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 51 | `origin/claude/ras18-doc-patch-hash-vo-hieu` | `cbe21dc88274` | `2026-08-02T23:22:04+07:00` | `ducthangho` — tác giả PR #17 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 52 | `origin/claude/rasoat-luat-bhxh-pending-svev2v` | `296e5c078e6d` | `2026-07-30T07:16:05+00:00` | `unknown` | `close` | 0 tệp chỉ có trên nhánh (`diff --diff-filter=A` rỗng) — bị canonical thay thế |
| 53 | `origin/claude/rasoat-luot19-kho-nen` | `a99463361cd4` | `2026-07-31T05:21:27+08:00` | `unknown` | `close` | 0 tệp chỉ có trên nhánh (`diff --diff-filter=A` rỗng) — bị canonical thay thế |
| 54 | `origin/claude/recursing-nightingale-76526b` | `1f22c7da9302` | `2026-08-03T02:37:32+07:00` | `ducthangho` — tác giả PR #21 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 55 | `origin/claude/refresh-token-gws-nlm-k4mt2m` | `14d1e354ebe5` | `2026-07-30T04:00:45+00:00` | `ducthangho` — tác giả PR #4 | `close` | PR #4 merged; 0 tệp chỉ có trên nhánh |
| 56 | `origin/claude/rel05-nlm08` | `aada9647e053` | `2026-08-03T01:38:31+07:00` | `ducthangho` — tác giả PR #19 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 57 | `origin/claude/reverent-torvalds-6a0ab8` | `103b43a47e0c` | `2026-08-03T23:43:07+07:00` | `ducthangho` — tác giả PR #28 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 58 | `origin/claude/review-bhxh-law-profile-2m08hz` | `b5b7831c21ec` | `2026-07-29T14:07:31+00:00` | `unknown` | `close` | 0 tệp chỉ có trên nhánh (`diff --diff-filter=A` rỗng) — bị canonical thay thế |
| 59 | `origin/claude/review-tra-luat-plan-qto0bb` | `2a2b890ee803` | `2026-07-23T09:19:31+00:00` | `unknown` | `close` | 0 tệp chỉ có trên nhánh (`diff --diff-filter=A` rỗng) — bị canonical thay thế |
| 60 | `origin/claude/sad-clarke-fdf8f0` | `615915958389` | `2026-08-03T22:22:53+07:00` | `ducthangho` — tác giả PR #24 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 61 | `origin/claude/selftest-r218-r219-bundle-k69xeh` | `f27684bdb706` | `2026-07-29T04:47:45+00:00` | `ducthangho` — tác giả PR #3 | `close` | PR #3 merged; 0 tệp chỉ có trên nhánh |
| 62 | `origin/claude/t0f-doc01-ras17-ing09-pdfvkn` | `9be57d6006fb` | `2026-08-02T08:26:16+00:00` | `ducthangho` — tác giả PR #11 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 63 | `origin/claude/t2-pro03-pro09-pro05-ing04-ing06` | `cd2d93418022` | `2026-08-02T13:02:34+00:00` | `ducthangho` — tác giả PR #14 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 64 | `origin/claude/tra-luat-r300-handoff-wpicyt` | `ccee68cd2236` | `2026-08-02T02:11:57+00:00` | `ducthangho` — tác giả PR #7 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 65 | `origin/claude/va-t1-gate-nlvoj9` | `88c41e312c5d` | `2026-08-01T15:38:37+00:00` | `ducthangho` — tác giả PR #6 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 66 | `origin/codex/d0-bootstrap-quote-fix` | `76435d6f4a51` | `2026-08-03T23:49:52+07:00` | `ducthangho` — tác giả PR #29 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 67 | `origin/codex/d0-constitution-rescue` | `dcab765acbdf` | `2026-08-04T02:38:55+07:00` | `ducthangho` — tác giả PR #33 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 68 | `origin/codex/d0-preview-already-landed` | `6f54fc0d02d0` | `2026-08-04T07:07:52+07:00` | `ducthangho` — tác giả PR #34 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 69 | `origin/codex/d0-workflow-controller` | `ac3fe25c17de` | `2026-08-04T01:02:39+07:00` | `ducthangho` — tác giả PR #31 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 70 | `origin/codex/f2-a-eol-policy` | `070cee76a63c` | `2026-08-07T18:49:25+07:00` | `ducthangho` — tác giả PR #50 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 71 | `origin/codex/release-v1.36.64` | `bd11532d2468` | `2026-08-04T01:38:43+07:00` | `ducthangho` — tác giả PR #32 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 72 | `origin/codex/work-packet-bootstrap` | `cefdb73d2c42` | `2026-08-03T22:58:58+07:00` | `ducthangho` — tác giả PR #25 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 73 | `origin/codex/work-packet-bootstrap-2` | `8876c3a4d426` | `2026-08-03T23:28:44+07:00` | `ducthangho` — tác giả PR #26 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |

### 4.5 Worktrees — đo lại trên host Windows

`git worktree list --porcelain` rc=0: **99 live / 0 prunable**. `git worktree prune --dry-run
--verbose` rc=0, stdout rỗng. Từng status dưới đây chạy với `safe.directory` chỉ trong command
(không sửa global config): **94 clean / 5 dirty; 49 chứa EOL / 50 legacy; 98 owner unknown**.

Decision được tính đúng một lần theo thứ tự fail-closed: dirty → `finish rồi rebase`; nếu clean và
HEAD chứa EOL hoặc HEAD đã là ancestor canonical → `close`; nếu clean, legacy, divergent và detached
→ `finish rồi rebase`; còn lại → `rebase`. Tally: **77 close + 9 rebase + 13 finish rồi rebase = 99**.
Mọi `close` chỉ là đề xuất, phải có owner/consent trước khi thực thi.

| # | Path | HEAD · commit date | Branch | Status / EOL | Owner | Decision |
|---:|---|---|---|---|---|---|
| 1 | `D:/Quốc hội/tra-luat` | `a55efcdfe18f8e924335e1d2d030e8fd65f6c077` · `2026-08-09T18:41:43+07:00` | `codex/f3-02-impact-policy` | dirty (11); EOL rc=0 | `unknown` | `finish rồi rebase` |
| 2 | `C:/Users/admin/.codex/visualizations/2026/08/09/019fe86a-b6f5-7d40-bd90-4a09003d8c40/mission54-wp60-g6-codex` | `578724e5fd046f3bc57024c601da7c2262ad2027` · `2026-08-09T11:20:19+07:00` | `codex/wp60-g6-f3-01-github-schema` | clean; EOL rc=0 | `unknown` | `close` |
| 3 | `C:/Users/admin/.codex/visualizations/2026/08/09/019fe86a-b6f5-7d40-bd90-4a09003d8c40/mission54-wp60-g7-codex` | `632401a58cae9452d52bd1548a9233a5a5844184` · `2026-08-10T05:43:27+07:00` | `codex/wp60-g7-f3-01-github-schema` | clean; EOL rc=0 | `unknown` | `close` |
| 4 | `C:/Users/admin/.codex/visualizations/2026/08/09/019fe86a-b6f5-7d40-bd90-4a09003d8c40/mission54-wp60-g7-review-claude` | `632401a58cae9452d52bd1548a9233a5a5844184` · `2026-08-10T05:43:27+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 5 | `C:/Users/admin/.codex/visualizations/2026/08/09/019fe86a-b6f5-7d40-bd90-4a09003d8c40/mission54-wp60-g7-review-claude-r2` | `632401a58cae9452d52bd1548a9233a5a5844184` · `2026-08-10T05:43:27+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 6 | `C:/Users/admin/.codex/visualizations/2026/08/09/019fe86a-b6f5-7d40-bd90-4a09003d8c40/mission54-wp60-g7-review-claude-r3` | `632401a58cae9452d52bd1548a9233a5a5844184` · `2026-08-10T05:43:27+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 7 | `C:/Users/admin/.codex/visualizations/2026/08/09/019fe86a-b6f5-7d40-bd90-4a09003d8c40/mission54-wp60-g7-review-claude-r4` | `632401a58cae9452d52bd1548a9233a5a5844184` · `2026-08-10T05:43:27+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 8 | `C:/Users/admin/.codex/visualizations/2026/08/09/019fe86a-b6f5-7d40-bd90-4a09003d8c40/mission54-wp60-g7-review-claude-r5` | `632401a58cae9452d52bd1548a9233a5a5844184` · `2026-08-10T05:43:27+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 9 | `C:/Users/admin/.codex/visualizations/2026/08/09/019fe86a-b6f5-7d40-bd90-4a09003d8c40/mission54-wp60-g7-review-claude-r6` | `632401a58cae9452d52bd1548a9233a5a5844184` · `2026-08-10T05:43:27+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 10 | `C:/Users/admin/.codex/visualizations/2026/08/09/019fe86a-b6f5-7d40-bd90-4a09003d8c40/mission54-wp60-g7-review-claude-r7` | `632401a58cae9452d52bd1548a9233a5a5844184` · `2026-08-10T05:43:27+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 11 | `C:/Users/admin/.codex/visualizations/2026/08/09/019fe86a-b6f5-7d40-bd90-4a09003d8c40/mission54-wp68-g6-codex` | `578724e5fd046f3bc57024c601da7c2262ad2027` · `2026-08-09T11:20:19+07:00` | `codex/wp68-g6-release-nested` | clean; EOL rc=0 | `unknown` | `close` |
| 12 | `C:/Users/admin/.codex/visualizations/2026/08/09/019fe86a-b6f5-7d40-bd90-4a09003d8c40/mission54-wp68-g7-codex` | `578724e5fd046f3bc57024c601da7c2262ad2027` · `2026-08-09T11:20:19+07:00` | `codex/wp68-g7-release-nested` | dirty (2); EOL rc=0 | `unknown` | `finish rồi rebase` |
| 13 | `C:/Users/admin/.codex/visualizations/2026/08/09/019fe86a-b6f5-7d40-bd90-4a09003d8c40/mission54-wp68-g8-codex` | `2a941f835c70864b2df0b96fd7e7b70ae9ab7c1d` · `2026-08-10T05:49:01+07:00` | `codex/wp68-g8-release-nested` | clean; EOL rc=0 | `unknown` | `close` |
| 14 | `C:/Users/admin/.codex/visualizations/2026/08/09/019fe86a-b6f5-7d40-bd90-4a09003d8c40/mission54-wp68-g8-review-claude-r1` | `2a941f835c70864b2df0b96fd7e7b70ae9ab7c1d` · `2026-08-10T05:49:01+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 15 | `C:/Users/admin/.codex/visualizations/2026/08/09/019fe86a-b6f5-7d40-bd90-4a09003d8c40/mission54-wp68-g8-review-claude-r2` | `2a941f835c70864b2df0b96fd7e7b70ae9ab7c1d` · `2026-08-10T05:49:01+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 16 | `C:/Users/admin/.codex/visualizations/2026/08/09/019fe86a-b6f5-7d40-bd90-4a09003d8c40/mission54-wp68-g8-review-claude-r3` | `2a941f835c70864b2df0b96fd7e7b70ae9ab7c1d` · `2026-08-10T05:49:01+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 17 | `C:/Users/admin/.codex/visualizations/2026/08/09/019fe86a-b6f5-7d40-bd90-4a09003d8c40/mission54-wp68-g8-review-claude-r4` | `2a941f835c70864b2df0b96fd7e7b70ae9ab7c1d` · `2026-08-10T05:49:01+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 18 | `C:/Users/admin/.codex/visualizations/2026/08/09/019fe86a-b6f5-7d40-bd90-4a09003d8c40/mission54-wp68-g8-review-claude-r5` | `2a941f835c70864b2df0b96fd7e7b70ae9ab7c1d` · `2026-08-10T05:49:01+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 19 | `C:/Users/admin/.codex/visualizations/2026/08/09/019fe86a-b6f5-7d40-bd90-4a09003d8c40/mission54-wp68-g8-review-claude-r6` | `2a941f835c70864b2df0b96fd7e7b70ae9ab7c1d` · `2026-08-10T05:49:01+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 20 | `C:/Users/admin/.codex/worktrees/03aa/tra-luat` | `828ec8ff4aa6efd14733849d4e46a85fa4fedcaf` · `2026-08-07T16:11:00+07:00` | `<detached>` | clean; EOL rc=1 | `unknown` | `finish rồi rebase` |
| 21 | `C:/Users/admin/.codex/worktrees/18db/tra-luat` | `ac00d0ee3505b99d9bf12df56fd0173435bd0dc0` · `2026-08-07T16:32:20+07:00` | `<detached>` | clean; EOL rc=1 | `unknown` | `finish rồi rebase` |
| 22 | `C:/Users/admin/.codex/worktrees/1b4b/tra-luat` | `fc50a5416d8d6f4268ff7cb11965b362eee0f9ab` · `2026-08-07T01:15:54+07:00` | `<detached>` | clean; EOL rc=1 | `unknown` | `close` |
| 23 | `C:/Users/admin/.codex/worktrees/305f/tra-luat` | `11feb3a70e77b68bc33545f277327d9727b22979` · `2026-08-09T10:21:36+07:00` | `codex/wp52-g3-ops-01` | clean; EOL rc=0 | `unknown` | `close` |
| 24 | `C:/Users/admin/.codex/worktrees/431a/tra-luat` | `31602843cc7fd3e26b1c32627385573e18133469` · `2026-08-06T15:10:13+07:00` | `<detached>` | clean; EOL rc=1 | `unknown` | `close` |
| 25 | `C:/Users/admin/.codex/worktrees/4411/tra-luat` | `377f4d130c0e4ba9439606d4943c476b93bbda05` · `2026-08-07T18:49:25+07:00` | `<detached>` | clean; EOL rc=1 | `unknown` | `finish rồi rebase` |
| 26 | `C:/Users/admin/.codex/worktrees/537d/tra-luat` | `def2bd46770bb6031b956b5ca6b472a79e8b39cb` · `2026-08-07T16:14:12+07:00` | `codex/f2-a-eol-policy-r3` | clean; EOL rc=1 | `unknown` | `rebase` |
| 27 | `C:/Users/admin/.codex/worktrees/68e8/tra-luat` | `0844c0bc24399fa4b8430750dc69f7388c23eb8b` · `2026-08-08T06:54:13+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 28 | `C:/Users/admin/.codex/worktrees/69be/tra-luat` | `b044f8b14e9ea3ad5d91a7fb4f0d29a3fe8415eb` · `2026-08-09T17:33:19+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 29 | `C:/Users/admin/.codex/worktrees/6bde/tra-luat` | `b5cc5d688a75ad991e6272d62110237c9a06ff41` · `2026-08-08T21:47:19+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 30 | `C:/Users/admin/.codex/worktrees/71e5/mission54-wp60-g5-claude` | `578724e5fd046f3bc57024c601da7c2262ad2027` · `2026-08-09T11:20:19+07:00` | `claude/wp60-g5-f3-01-github-schema` | clean; EOL rc=0 | `unknown` | `close` |
| 31 | `C:/Users/admin/.codex/worktrees/71e5/tra-luat` | `b044f8b14e9ea3ad5d91a7fb4f0d29a3fe8415eb` · `2026-08-09T17:33:19+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 32 | `C:/Users/admin/.codex/worktrees/7563/tra-luat` | `b044f8b14e9ea3ad5d91a7fb4f0d29a3fe8415eb` · `2026-08-09T17:33:19+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 33 | `C:/Users/admin/.codex/worktrees/94ee/tra-luat` | `91d5e8dc0133b1d9942d5868032aacf2ea9d2ff9` · `2026-08-09T00:07:42+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 34 | `C:/Users/admin/.codex/worktrees/b26f/tra-luat` | `2cc9576fcadf5649c532157ebeddb48b5c12472a` · `2026-08-07T13:00:32+07:00` | `<detached>` | clean; EOL rc=1 | `unknown` | `finish rồi rebase` |
| 35 | `C:/Users/admin/.codex/worktrees/bf26/tra-luat` | `91d5e8dc0133b1d9942d5868032aacf2ea9d2ff9` · `2026-08-09T00:07:42+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 36 | `C:/Users/admin/.codex/worktrees/cf7e/tra-luat` | `070cee76a63c4e32a55346c84216c94c09a6dc11` · `2026-08-07T18:49:25+07:00` | `codex/f2-a-eol-policy` | clean; EOL rc=1 | `unknown` | `close` |
| 37 | `C:/Users/admin/.codex/worktrees/fd03/tra-luat` | `b044f8b14e9ea3ad5d91a7fb4f0d29a3fe8415eb` · `2026-08-09T17:33:19+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 38 | `D:/Quốc hội/luot3_wt` | `1bdc16c73421f58545b635a186da172eb1ba8e6a` · `2026-08-03T02:04:23+07:00` | `claude/r325-noi-lai-duoi-vbhn` | clean; EOL rc=1 | `unknown` | `close` |
| 39 | `D:/Quốc hội/p16_wt` | `7469d8c96df8f1db8a4b769fc69c5313fc14e331` · `2026-08-01T17:03:25+07:00` | `claude/r299-bridge-scope-va-chunks-apply` | clean; EOL rc=1 | `unknown` | `close` |
| 40 | `D:/Quốc hội/rasoat_docs_wt` | `f39f98398d7bdb2927281e857f70bd6e5440b20f` · `2026-07-26T08:06:51+07:00` | `claude/legal-doc-review-architecture-2al46n` | clean; EOL rc=1 | `unknown` | `close` |
| 41 | `D:/Quốc hội/rel05_wt` | `e9bea049f3413ff401110a4485757f5c7caa4a20` · `2026-08-03T01:00:01+07:00` | `claude/rel05-nlm08` | clean; EOL rc=1 | `unknown` | `rebase` |
| 42 | `D:/Quốc hội/tra-luat/.claude/worktrees/nifty-diffie-63b72e` | `39e860c725ff54f42f59a77fc5c259e135081683` · `2026-08-03T10:43:50+07:00` | `claude/nifty-diffie-63b72e` | clean; EOL rc=1 | `unknown` | `close` |
| 43 | `D:/Quốc hội/tra-luat/.claude/worktrees/recursing-nightingale-76526b` | `1f22c7da9302d334a8d38a36ad5a0c85de2190d2` · `2026-08-03T02:37:32+07:00` | `<detached>` | clean; EOL rc=1 | `unknown` | `close` |
| 44 | `D:/Quốc hội/tra-luat/.claude/worktrees/reverent-torvalds-6a0ab8` | `1050c17fb96b53ebd53f5487aeb779189a6aabb6` · `2026-08-04T00:52:22+07:00` | `claude/codex-exclude-dir` | clean; EOL rc=1 | `unknown` | `close` |
| 45 | `D:/Quốc hội/tra-luat/.claude/worktrees/sad-clarke-fdf8f0` | `6159159583894e290602dce38ae3db2e31551293` · `2026-08-03T22:22:53+07:00` | `claude/sad-clarke-fdf8f0` | clean; EOL rc=1 | `unknown` | `close` |
| 46 | `D:/Quốc hội/tra-luat/.claude/worktrees/wp51-g1-f1-01-fix-codex` | `1880346d2be3c0be9a93de7624ee108d99b6c88c` · `2026-08-08T01:03:44+07:00` | `codex/wp51-g1-f1-01-fix` | dirty (1); EOL rc=0 | `unknown` | `finish rồi rebase` |
| 47 | `D:/Quốc hội/tra-luat/.claude/worktrees/wp51-g2-f1-01-fix-codex` | `3c8df84bfdf7fd6eed423333b4f4ea0fa66eaabe` · `2026-08-08T01:55:02+07:00` | `codex/wp51-g2-f1-01-fix` | clean; EOL rc=0 | `unknown` | `close` |
| 48 | `D:/Quốc hội/tra-luat/.claude/worktrees/wp55-f3-03-claude` | `a3e39573a269c94bb58ef75a4c1b5bd15dab4d76` · `2026-08-08T10:25:33+07:00` | `claude/wp55-f3-03` | clean; EOL rc=0 | `unknown` | `close` |
| 49 | `D:/Quốc hội/tra-luat/.claude/worktrees/wp57-g2-f3-00-governance-codex` | `d2bc8e0de88c29a95e63959e3bd8f6dcf14246a9` · `2026-08-08T12:02:33+07:00` | `codex/wp57-g2-f3-00-governance` | clean; EOL rc=0 | `unknown` | `close` |
| 50 | `D:/Quốc hội/tra-luat/.claude/worktrees/wp60-g1-claude` | `578724e5fd046f3bc57024c601da7c2262ad2027` · `2026-08-09T11:20:19+07:00` | `agent/wp60-g1-claude` | clean; EOL rc=0 | `unknown` | `close` |
| 51 | `D:/Quốc hội/tra-luat/.claude/worktrees/wp60-g1-f3-01-claude` | `2b1c6805db3527917db7e0df2d1f76a18273c3b3` · `2026-08-09T21:09:01+07:00` | `claude/wp60-g1-f3-01-github-schema` | clean; EOL rc=0 | `unknown` | `close` |
| 52 | `D:/Quốc hội/tra-luat/.claude/worktrees/wp60-g2-f3-01-claude` | `7dd0e60ae9927ef640de70e00e70beeb120188b9` · `2026-08-10T04:17:27+07:00` | `claude/wp60-g2-f3-01-github-schema` | clean; EOL rc=0 | `unknown` | `close` |
| 53 | `D:/Quốc hội/tra-luat/.codex/worktrees/d0-bootstrap-hardening` | `768b160511f0806be79303c79643ce6594ff35ee` · `2026-08-03T23:32:00+07:00` | `codex/d0-bootstrap-hardening` | clean; EOL rc=1 | `unknown` | `rebase` |
| 54 | `D:/Quốc hội/tra-luat/.codex/worktrees/d0-bootstrap-quote-fix` | `76435d6f4a51b6261fd51103089765aa3f3108ab` · `2026-08-03T23:49:52+07:00` | `codex/d0-bootstrap-quote-fix` | clean; EOL rc=1 | `unknown` | `close` |
| 55 | `D:/Quốc hội/tra-luat/.codex/worktrees/d0-constitution-rescue` | `d1016d24647ef656c058788ed144c3bf6884f373` · `2026-08-04T02:57:37+07:00` | `codex/d0-constitution-rescue` | clean; EOL rc=1 | `unknown` | `close` |
| 56 | `D:/Quốc hội/tra-luat/.codex/worktrees/d0-preview-already-landed` | `c5e8a9d42d6cf80ed14084a05056f5880941dd4c` · `2026-08-04T08:49:24+07:00` | `codex/d0-preview-already-landed` | clean; EOL rc=1 | `unknown` | `close` |
| 57 | `D:/Quốc hội/tra-luat/.codex/worktrees/d0-workflow-controller` | `ac3fe25c17debccbab86d8d78b0be2a45e575aa6` · `2026-08-04T01:02:39+07:00` | `codex/d0-workflow-controller` | clean; EOL rc=1 | `unknown` | `close` |
| 58 | `D:/Quốc hội/tra-luat/.codex/worktrees/release-v1-36-64` | `fd3d0e5e2e357c694523ccf9e69db2d6cf0196c7` · `2026-08-04T01:47:26+07:00` | `codex/release-v1.36.64` | clean; EOL rc=1 | `unknown` | `close` |
| 59 | `D:/Quốc hội/tra-luat/.codex/worktrees/review-wp37-g2` | `c5e8a9d42d6cf80ed14084a05056f5880941dd4c` · `2026-08-04T08:49:24+07:00` | `<detached>` | clean; EOL rc=1 | `unknown` | `close` |
| 60 | `D:/Quốc hội/tra-luat/.codex/worktrees/reviewer-cross-platform` | `65f5e4944709e431ad440ca04a63d5b29f8fc2b0` · `2026-08-04T16:23:04+08:00` | `codex/reviewer-cross-platform` | clean; EOL rc=1 | `unknown` | `rebase` |
| 61 | `D:/Quốc hội/tra-luat/.codex/worktrees/wp-bootstrap` | `c50700675ae541cee507126064f573c239e6604c` · `2026-08-03T23:22:42+07:00` | `codex/work-packet-bootstrap` | clean; EOL rc=1 | `unknown` | `rebase` |
| 62 | `D:/Quốc hội/tra-luat/.codex/worktrees/wp46-f1-docs` | `004bb98e0009efaa2f8817b5c98c86863e91cb59` · `2026-08-06T23:58:09+07:00` | `codex/wp46-f1-docs` | clean; EOL rc=1 | `unknown` | `close` |
| 63 | `D:/Quốc hội/tra-luat/.codex/worktrees/wp47-f1-staleness` | `6f24f9008ad12e06d51970bc974178e456b04b8f` · `2026-08-07T01:05:56+07:00` | `codex/wp47-f1-staleness` | clean; EOL rc=1 | `unknown` | `close` |
| 64 | `D:/Quốc hội/tra-luat/.codex/worktrees/wp66-baseline-578724e` | `578724e5fd046f3bc57024c601da7c2262ad2027` · `2026-08-09T11:20:19+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 65 | `D:/Quốc hội/tra-luat/.codex/worktrees/wp66-g1-codex` | `b0448c85e706f1726810acf6f6cbe82369e5499e` · `2026-08-09T15:20:46+07:00` | `agent/wp66-g1-codex` | clean; EOL rc=0 | `unknown` | `close` |
| 66 | `D:/Quốc hội/tra-luat/AUDIT_WP77_AB5B3C2` | `ab5b3c2a193ed2a4b535e1688a3240d10eecbfbd` · `2026-08-10T08:26:51Z` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 67 | `D:/Quốc hội/tra-luat/AUDIT_WP77_C478472` | `c4784728fb67429b927f6837bd175ac6e18154af` · `2026-08-10T07:49:37Z` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 68 | `D:/Quốc hội/tra-luat/AUDIT_WP77_G1_176b402` | `176b402d413ebe1ea18c44430333506d021b2552` · `2026-08-10T05:29:50Z` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 69 | `D:/Quốc hội/tra-luat/AUDIT_WP77_G2_DC0DBF4` | `dc0dbf427740ee284bfa5bc3d03f9a47f1b69d06` · `2026-08-10T06:48:56Z` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 70 | `D:/Quốc hội/tra-luat/work/f2-d-reopen-writer` | `86dc0705c796d4436df00d7accc47e219282c858` · `2026-08-09T01:06:03+07:00` | `codex/f2-d-reopen-writer` | clean; EOL rc=0 | `unknown` | `close` |
| 71 | `D:/Quốc hội/tra-luat/work/wp63-g2-codex` | `fe9395ba3f2379e0a2b670ecfb6224103c944d54` · `2026-08-10T08:42:30Z` | `<detached>` | clean; EOL rc=0 | `codex` (lease g2) | `close` |
| 72 | `D:/Quốc hội/tra-luat-wt/f1-40-integration` | `b303a734b9afc4cbd5f23d179bc041cf1dd37380` · `2026-08-06T21:19:54+07:00` | `codex/f1-40-integration` | clean; EOL rc=1 | `unknown` | `close` |
| 73 | `D:/Quốc hội/tra-luat-wt/f1-40-land` | `8be3398d60b8283615c60b444a96e7dff701aa70` · `2026-08-06T23:20:56+07:00` | `codex/f1-40-land` | clean; EOL rc=1 | `unknown` | `close` |
| 74 | `D:/Quốc hội/tra-luat-wt/f1-40-land-review-8be3398` | `8be3398d60b8283615c60b444a96e7dff701aa70` · `2026-08-06T23:20:56+07:00` | `<detached>` | clean; EOL rc=1 | `unknown` | `close` |
| 75 | `D:/Quốc hội/tra-luat-wt/followups-46-47-land-review-fc50a54` | `fc50a5416d8d6f4268ff7cb11965b362eee0f9ab` · `2026-08-07T01:15:54+07:00` | `<detached>` | clean; EOL rc=1 | `unknown` | `close` |
| 76 | `D:/Quốc hội/tra-luat-wt/review-wp41-g2` | `cad2e32df83aa4959fc30e5a1e4d830c50386d06` · `2026-08-05T08:28:16+07:00` | `<detached>` | clean; EOL rc=1 | `unknown` | `finish rồi rebase` |
| 77 | `D:/Quốc hội/tra-luat-wt/review-wp41-g3` | `8bd09894f2e3a5f858b5bf6330d1b533de73faca` · `2026-08-05T16:06:06+07:00` | `<detached>` | clean; EOL rc=1 | `unknown` | `finish rồi rebase` |
| 78 | `D:/Quốc hội/tra-luat-wt/review-wp41-g4` | `06df58f6429710ae4adb6a60f4480a6773feb16e` · `2026-08-05T18:11:51+07:00` | `<detached>` | clean; EOL rc=1 | `unknown` | `close` |
| 79 | `D:/Quốc hội/tra-luat-wt/review-wp42-g1` | `ac78b7c493ab50336ffd3e229bdcecc6e38fa60b` · `2026-08-05T22:51:12+07:00` | `<detached>` | clean; EOL rc=1 | `unknown` | `finish rồi rebase` |
| 80 | `D:/Quốc hội/tra-luat-wt/review-wp42-g2` | `8074ec9a1a934fdec4468a8825e3452dd3a48446` · `2026-08-06T02:42:09+07:00` | `<detached>` | clean; EOL rc=1 | `unknown` | `finish rồi rebase` |
| 81 | `D:/Quốc hội/tra-luat-wt/review-wp42-g3` | `98e91f280915953c16c623e846de01cf1e4b52ef` · `2026-08-06T06:48:27+07:00` | `<detached>` | clean; EOL rc=1 | `unknown` | `close` |
| 82 | `D:/Quốc hội/tra-luat-wt/review-wp43-g1` | `d30e46aa6c6a6dc28cedca0db0ae0dd8fcad8207` · `2026-08-06T09:37:45+07:00` | `<detached>` | clean; EOL rc=1 | `unknown` | `close` |
| 83 | `D:/Quốc hội/tra-luat-wt/review-wp44-g1` | `31602843cc7fd3e26b1c32627385573e18133469` · `2026-08-06T15:10:13+07:00` | `<detached>` | clean; EOL rc=1 | `unknown` | `close` |
| 84 | `D:/Quốc hội/tra-luat-wt/review-wp45-g1` | `b303a734b9afc4cbd5f23d179bc041cf1dd37380` · `2026-08-06T21:19:54+07:00` | `<detached>` | clean; EOL rc=1 | `unknown` | `close` |
| 85 | `D:/Quốc hội/tra-luat-wt/review-wp66-b0448c8` | `b0448c85e706f1726810acf6f6cbe82369e5499e` · `2026-08-09T15:20:46+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 86 | `D:/Quốc hội/tra-luat-wt/review-wp68-03f9919` | `03f9919266f712820a558548d8fd461b1c82436e` · `2026-08-09T20:02:58+07:00` | `<detached>` | dirty (10); EOL rc=0 | `unknown` | `finish rồi rebase` |
| 87 | `D:/Quốc hội/tra-luat-wt/review-wp68-8b26cfb` | `8b26cfb11376727b6826000144f839fb3385358b` · `2026-08-09T16:50:24+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 88 | `D:/Quốc hội/tra-luat-wt/review-wp68-d7e3bc4` | `d7e3bc4ab39ac2a13eb96a96e55cc5f3f43030b3` · `2026-08-09T23:22:56+07:00` | `<detached>` | clean; EOL rc=0 | `unknown` | `close` |
| 89 | `D:/Quốc hội/tra-luat-wt/wp-f3-03-nested` | `d7e3bc4ab39ac2a13eb96a96e55cc5f3f43030b3` · `2026-08-09T23:22:56+07:00` | `claude/wp-f3-03-release-nested` | clean; EOL rc=0 | `unknown` | `close` |
| 90 | `D:/Quốc hội/tra-luat-wt/wp41-f1-01-codex` | `c5e8a9d42d6cf80ed14084a05056f5880941dd4c` · `2026-08-04T08:49:24+07:00` | `codex/wp41-g1-f1-01` | dirty (2); EOL rc=1 | `unknown` | `finish rồi rebase` |
| 91 | `D:/Quốc hội/tra-luat-wt/wp41-g2-f1-01-codex` | `cad2e32df83aa4959fc30e5a1e4d830c50386d06` · `2026-08-05T08:28:16+07:00` | `codex/wp41-g2-f1-01` | clean; EOL rc=1 | `unknown` | `rebase` |
| 92 | `D:/Quốc hội/tra-luat-wt/wp41-g3-f1-01-codex` | `8bd09894f2e3a5f858b5bf6330d1b533de73faca` · `2026-08-05T16:06:06+07:00` | `codex/wp41-g3-f1-01` | clean; EOL rc=1 | `unknown` | `rebase` |
| 93 | `D:/Quốc hội/tra-luat-wt/wp41-g4-f1-01-codex` | `06df58f6429710ae4adb6a60f4480a6773feb16e` · `2026-08-05T18:11:51+07:00` | `codex/wp41-g4-f1-01` | clean; EOL rc=1 | `unknown` | `close` |
| 94 | `D:/Quốc hội/tra-luat-wt/wp42-g1-f1-02-codex` | `ac78b7c493ab50336ffd3e229bdcecc6e38fa60b` · `2026-08-05T22:51:12+07:00` | `codex/wp42-g1-f1-02` | clean; EOL rc=1 | `unknown` | `rebase` |
| 95 | `D:/Quốc hội/tra-luat-wt/wp42-g2-f1-02-codex` | `8074ec9a1a934fdec4468a8825e3452dd3a48446` · `2026-08-06T02:42:09+07:00` | `codex/wp42-g2-f1-02` | clean; EOL rc=1 | `unknown` | `rebase` |
| 96 | `D:/Quốc hội/tra-luat-wt/wp42-g3-f1-02-codex` | `98e91f280915953c16c623e846de01cf1e4b52ef` · `2026-08-06T06:48:27+07:00` | `codex/wp42-g3-f1-02` | clean; EOL rc=1 | `unknown` | `close` |
| 97 | `D:/Quốc hội/tra-luat-wt/wp43-g1-f1-03-codex` | `d30e46aa6c6a6dc28cedca0db0ae0dd8fcad8207` · `2026-08-06T09:37:45+07:00` | `codex/wp43-g1-f1-03` | clean; EOL rc=1 | `unknown` | `close` |
| 98 | `D:/Quốc hội/tra-luat-wt/wp44-g1-f1-04-codex` | `31602843cc7fd3e26b1c32627385573e18133469` · `2026-08-06T15:10:13+07:00` | `codex/wp44-g1-f1-04` | clean; EOL rc=1 | `unknown` | `close` |
| 99 | `D:/Quốc hội/tra-luat-wt/wp45-g1-f1-05-codex` | `b303a734b9afc4cbd5f23d179bc041cf1dd37380` · `2026-08-06T21:19:54+07:00` | `codex/wp45-g1-f1-05` | clean; EOL rc=1 | `unknown` | `close` |

#### 4.5.1 Dirty status — raw paths phải bảo toàn

- Row 1: 11 untracked entries: bốn `AUDIT_WP77_*` directories, năm
  `docs/research/2026-08-0{4,5}-*.md`, `work/f2-d-reopen-writer/`, và isolated
  `work/wp63-g2-codex/` vừa được tạo. `status` rc=0.
- Row 12: modified `scripts/tl_core/release.py`; untracked
  `scripts/test_fragments/wp68_release_exclude_nested_repo.py`. `status` rc=0.
- Row 46: modified `scripts/tl_selftest.py`. `status` rc=0.
- Row 86: 10 untracked `tmp/review-r2/*` logs/artifact. `status` rc=0.
- Row 90: modified `scripts/tl_selftest.py`; untracked `scripts/tl_core/test_fragments.py`.
  `status` rc=0.

`blocker_worktree_measurement=closed`, nhưng 5 dirty rows, 50 legacy rows và 98 unknown owners vẫn
là positive evidence để giữ `blocker_writer_inventory=open` và `writer_reopened=false`.

## 5. Enforcement inventory — cập nhật sau khi #52 land

Artifact tiền nhiệm ghi `.githooks/pre-push` **không tồn tại**. Điều đó **đã hết đúng**. Đo lại tại
canonical `b044f8b1`:

| Phạm vi PRA-52-01 duyệt | Có trên canonical? | Bằng chứng |
|---|---|---|
| EOL ancestry cho **mọi** writer `refs/heads/*` | **CÓ** | `.githooks/pre-push:349-370` — duyệt từng dòng stdin, bỏ qua ref xoá (SHA toàn `0`), đòi `git merge-base --is-ancestor 1880346d <sha>`; rc≠0 ⇒ `pre-push BLOCKED` nêu đúng tên ref |
| Kiểm ancestry theo **PR head SHA** | **CÓ** | `.github/workflows/ci.yml:53-64`, step `PR head contains required EOL base`, dùng `github.event.pull_request.head.sha` (KHÔNG dùng `GITHUB_SHA` vì trên `pull_request` đó là synthetic merge), `fetch-depth: 0` |

```
git cat-file -e b044f8b1:.githooks/pre-push        → rc=0
git cat-file -e b044f8b1:.githooks/pre_push_test.py → rc=0
git grep -n '1880346d' -- .githooks .github/workflows → rc=0, 3 khớp
```

Hook fail-closed đúng nghĩa: rc>1 (không xác minh được) cũng chặn, không chỉ rc=1.

### 5.1 Lỗ hổng CÒN LẠI — nối thẳng vào #52

Ba giới hạn dưới đây là thuộc tính của cơ chế #52 đã land, KHÔNG phải khiếm khuyết cần vá trong F2-D.
`.githooks/pre-push` và `.github/workflows/ci.yml` là **exact write-set của #52**, nằm NGOÀI write-set
F2-D; artifact này không sửa chúng.

1. **Hook chỉ phủ máy đã cấu hình `core.hooksPath`.** Trên host/clone này,
   `git config core.hooksPath` → `D:\Quốc hội\tra-luat\.githooks`, rc=0. Clone này được phủ, nhưng
   máy/clone chưa cấu hình hoặc push với `--no-verify` vẫn đi vòng qua được. Hook là hàng rào phía
   client, không phải cưỡng chế phía server.
2. **Không hồi tố.** 73 nhánh legacy đã nằm sẵn trên `origin` TRƯỚC khi cơ chế land — chúng không bị
   chặn hồi tố, chỉ bị chặn ở **lần push kế tiếp**. Đừng đọc "#52 đã land" thành "73 nhánh đã an toàn".
3. **Không có cưỡng chế phía server.** `master` hiện `protected: false` (đọc qua GitHub API,
   `list_branches`). Required status checks không bật.

**Về branch protection / ruleset:** generation 2 gọi trực tiếp cả hai API; mỗi lệnh rc=1, HTTP 403,
message đúng `Upgrade to GitHub Pro or make this repository public to enable this feature`.
`GET /branches/master` đồng thời trả `protected:false`, SHA `b044f8b1…`. Vì vậy không khai required
checks/branch protection/ruleset là khả dụng.

## 6. Finding disposition — generation 2

- **WP63-RV-01 — fixed:** graph complete, bảng được parse lại từ 73 exact tips, 0 remote mismatch;
  ancestry **69/4**, r210 rc=0, non-ancestor đúng rows 1/6/13/49. Claim 26/47 và r210 rc=1 cũ đã
  bị loại khỏi artifact.
- **WP63-RV-02 — fixed:** row 6 đổi `close → rebase`; basis ghi 2 commit riêng, 40 path, 21 blob
  khác canonical và 9 test name vắng canonical. Không dùng CHANGELOG/0-added-files để close.
- **WP63-RV-03 — fixed:** §4.5 là phép đo thật trên host Windows, không còn snapshot kế thừa;
  list/prune/status/ancestry rc được ghi và cả 99 entries có path, exact HEAD/date, branch, status,
  owner hoặc unknown, và đúng một decision.

Finding kỹ thuật đã xử lý không tự gỡ operational block: inventory vẫn có residual writers và
thiếu owner/consent. `operational_verdict=blocked` không đổi.

## 7. Điều kiện gỡ blocker

Không đổi verdict và không mở lại writer cho tới khi đủ bằng chứng dương:

1. 4 nhánh §4.3 đã rebase lên tip chứa EOL, hoặc owner quyết định bỏ có ghi nhận.
2. 43 remote branches và 98 worktrees `owner=unknown` có owner, hoặc có quyết định human rõ ràng.
3. 5 worktrees dirty được owner xử lý và kiểm lại; không mất file/commit riêng.
4. 50 legacy worktrees được rebase/retire theo decision và consent; 13 mục `finish rồi rebase` phải
   được bảo toàn trước mọi thao tác.
5. Mọi mục `close` được owner xác nhận trước khi xoá.
6. Chạy lại kiểm kê trên canonical mới, kết quả không còn residual writer trái chính sách.

Cho tới lúc đó: `blocker_enforcement=closed`, `blocker_worktree_measurement=closed`,
`blocker_writer_inventory=open`, `writer_reopened=false`; giữ **#63, #49, #48 MỞ**. Không tuyên
bố F2-D hoàn tất vận hành.

## 8. Generation 2 validation evidence

Các gate dưới đây chạy trong isolated worktree từ inherited PR head
`fe9395ba3f2379e0a2b670ecfb6224103c944d54`, với working tree chỉ sửa artifact này:

| Gate | Kết quả |
|---|---|
| `git diff --check` | rc=0 |
| `python .githooks/eol_policy_test.py` | rc=0; **30/30 pass** |
| `python .githooks/eol_policy.py --all --json` | rc=0; `ok=true`; scanned=299, checked=277, skipped=22, violations=0 |
| `python scripts/tl.py --selftest` | rc=0; **1696/1696 pass** |
| `python scripts/tl.py doc-claims-check --strict --json` | rc=0; `ok=true`; files_scanned=82, claims_flagged=353, flags=0 |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | rc=0; `ok=true`; expected=179, checked=179; failed/extra/missing/required_missing/errors đều 0 |

`release-verify` trả `package_hash_expected = package_hash_current =
package_hash_full_tree = e004956449c30f7176769a6ede69eecd31029aa7dcac54d3daf3bfa28375c400`,
`package_hash_self_match=true`, `package_hash_match=true`.

So với canonical `b044f8b14e9ea3ad5d91a7fb4f0d29a3fe8415eb`, các object ID ở inherited head
giống hệt byte/tree:

- `VERSION`: `8331824f0abcb019eba69092d8b525753cd84230`
- `CHANGELOG.md`: `6d907f9421d8c4b033e04161378d8df4fd27dc98`
- `RELEASE_MANIFEST.json`: `8fc90183877f8f9aa1fdbb4e4a4d42f82479bbcf`
- `SKILL.md`: `2af1e16729ae5e932147a8b7332fef6ea362511a`
- tree `references/golden`: `faa36333e9c75594c9760a270e28afc25c3fdd2f`

`git diff --name-status b044f8b14e9ea3ad5d91a7fb4f0d29a3fe8415eb HEAD` tại inherited
head chỉ có `A .github/coordination/f2-d-writer-inventory.md`; generation 2 tiếp tục giữ exact
write-set một tệp này.
