# F2-D — kiểm kê writer trước khi mở lại

## Kết luận

**Verdict: `blocked`. Writer VẪN phải giữ trạng thái đóng băng.**

Quan sát `2026-08-10T08:17:49Z`. Canonical `b044f8b14e9ea3ad5d91a7fb4f0d29a3fe8415eb`.
Commit EOL chuẩn `1880346d2be3c0be9a93de7624ee108d99b6c88c`.

Blocker **cưỡng chế** đã ĐÓNG (#52 land, merge `578724e5` — xem §5). Blocker **kiểm kê** còn MỞ:

- 73 remote branches chưa chứa commit EOL: **70 `close` · 2 `rebase` · 1 `finish rồi rebase`**.
- **43/73 branches có `owner=unknown`** — không có bằng chứng owner trực tiếp từ PR. Không suy owner
  từ namespace, tên nhánh hay tác giả commit.
- 3 branches mang nội dung CHƯA land, đã đo đích danh (§4.3). Chúng không được `close`.
- **Kiểm kê worktree KHÔNG đo được trong môi trường phiên này** (§2). Đây là blocker đo lường thật,
  không phải "0 worktree".

Artifact này CHỈ là inventory/decision record. F2-D **không** xoá remote branch, không prune/remove
worktree, không rebase, không force-push, không sửa dữ liệu dirty, không mở writer, không sửa hook/CI.

Mọi mục `close` chỉ được THỰC THI sau khi owner được xác nhận. Với 43 mục `owner=unknown`, quyết định
`close` là **đề xuất có căn cứ**, chưa phải uỷ quyền xoá.

## 1. Nguồn điều phối

- Mission: [#48](https://github.com/ducthangho/tra-luat/issues/48), revision 2 ·
  plan hash `340b15a934cc27f2aa5d542973e12c268ab4db4307b390a77e66bc9d6a060d11`.
- Human MCR: [MCR-48-01](https://github.com/ducthangho/tra-luat/issues/48#issuecomment-5227303367).
- Packet: [#63](https://github.com/ducthangho/tra-luat/issues/63), revision 1 / generation 1 ·
  spec hash `de63e124ed39a94108f87770c2bec9ec39a25119795ce9f6534d7084fd4d0fea`.
- Parent drain packet: [#49](https://github.com/ducthangho/tra-luat/issues/49) — `state:landed`.
- Enforcement packet: [#52](https://github.com/ducthangho/tra-luat/issues/52) — `state:landed`.
- Reconcile gần nhất: [#63 comment 5237539078](https://github.com/ducthangho/tra-luat/issues/63#issuecomment-5237539078).
- Artifact tiền nhiệm: PR [#64](https://github.com/ducthangho/tra-luat/pull/64), head
  `86dc0705c796d4436df00d7accc47e219282c858` (Draft, chưa merge). Xem §6 — sai lệch đã sửa.

Readback fail-closed, rc đọc trực tiếp:

```
git merge-base --is-ancestor 1880346d… b044f8b1…   → rc=0   EOL base là ancestor của canonical
git merge-base --is-ancestor 91d5e8dc… b044f8b1…   → rc=0   base lúc mint là ancestor
git merge-base --is-ancestor 578724e5… b044f8b1…   → rc=0   merge #52 là ancestor
```

## 2. Phạm vi đo — GIỚI HẠN PHẢI ĐỌC TRƯỚC

Packet ghi `environment: local (Windows)`, `executor: codex`. Phiên thực thi này chạy trên
**container Linux từ xa** (`uname -s -r` → `Linux 6.18.5-fc-v20`, cwd `/home/user/tra-luat`),
executor `claude`. Hệ quả **không thể lách**:

| Hạng mục | Đo được ở đây? | Lý do |
|---|---|---|
| Remote branches (`git branch -r`) | **CÓ** — đầy đủ 73/73 | ref từ `origin`, độc lập máy |
| Local worktrees | **KHÔNG** | `git worktree list` chỉ thấy worktree của CHÍNH bản sao này |

Đo thật trong môi trường này:

```
git worktree list --porcelain      → rc=0, ĐÚNG 1 worktree: /home/user/tra-luat (canonical, clean)
git worktree prune --dry-run -v    → rc=0, 0 prunable
```

**Con số `1` này KHÔNG được đọc là "chỉ còn 1 worktree".** 58 worktrees mà artifact tiền nhiệm đo
nằm trên máy Windows của chủ kho (`D:\Quốc hội\…`, `C:\Users\admin\.codex\worktrees\…`) — chúng
không tồn tại trong container này và **không bị bác bỏ** bởi phép đo trên. §4.5 giữ chúng ở dạng
**KẾ THỪA, CHƯA ĐO LẠI**, gắn nhãn rõ ràng. Kiểm kê worktree phải được chạy lại trên chính máy
Windows đó thì acceptance của #63 mới đóng được.

## 3. Phương pháp

```text
git fetch origin --prune
git branch -r --no-contains 1880346d2be3c0be9a93de7624ee108d99b6c88c
git merge-base --is-ancestor <tip> b044f8b1…            # bằng chứng "đã nằm trong canonical"
git diff --name-status --diff-filter=A <canonical> <ref> # tệp CHỈ có trên nhánh
git grep -q '<rNNN>' <canonical> -- CHANGELOG.md         # bằng chứng fix đã land
git cat-file -e <canonical>:<path>                       # tệp có/không trên canonical
git worktree list --porcelain ; git worktree prune --dry-run --verbose
```

| Phép đo | rc | Kết quả |
|---|---:|---|
| `git fetch origin --prune` | 0 | 4 nhánh mới + 1 tag; base không drift |
| `git branch -r` (tổng, trừ `origin/HEAD`) | 0 | **92** |
| `git branch -r --no-contains <EOL>` | 0 | **73** |
| `git branch -r --contains <EOL>` | 0 | **19** |
| `git worktree list --porcelain` | 0 | **1** (giới hạn môi trường — §2) |
| `git worktree prune --dry-run --verbose` | 0 | 0 prunable |
| `merge-base --is-ancestor <tip> canonical` ×73 | 0 cho 26; 1 cho 47 | 26 đã nằm trong canonical |
| `diff --diff-filter=A canonical <ref>` ×73 | 0 cho 73/73 | chỉ **3** nhánh có tệp riêng |
| PR mapping (`list_pull_requests`, state=all) | 0 | 49 PR; **30** nhánh có PR, **43** không |

### 3.1 Lệch số so với mốc reconcile — ghi cả hai

Reconcile (`2026-08-10T08:03:39Z`) đo **93** remote heads; ở đây **92**. Chênh **1**.
Tập legacy thì **BẰNG NHAU TUYỆT ĐỐI**: 73 = 73, và cả 73 tip khớp từng ký tự với artifact tiền
nhiệm (0 mismatch trên 73 dòng).

Số học khớp với giả thiết `origin/HEAD`: ở đây `git branch -r | grep -c '^origin/HEAD'` → **0**
(bản sao này không tạo ref đó), và `73 + 19 = 92`. Nếu phía reconcile có `origin/HEAD` thì nó rơi
vào nhóm *chứa* EOL (trỏ `origin/master`), cho `73 + 20 = 93`. Đây là **suy luận số học, không phải
phép đo trên máy kia** — ghi ra để phiên sau khỏi coi 92 là "mất một nhánh". Điểm cần nhớ: đại lượng
mà acceptance quan tâm — tập 73 legacy — **không đổi**.

## 4. Remote branches chưa chứa EOL (73)

### 4.1 Quy ước bằng chứng

Bốn lớp bằng chứng, xếp theo độ mạnh. Mỗi dòng dùng lớp MẠNH NHẤT nó có:

1. **Ancestry** — `merge-base --is-ancestor <tip> canonical` rc=0. Chứng minh tuyệt đối.
2. **Merged PR** — PR đã merge; nội dung land qua squash/rebase.
3. **CHANGELOG** — số `rNNN` của nhánh có trong `CHANGELOG.md` canonical.
4. **Không tệp riêng** — `diff --diff-filter=A` rỗng: không tệp nào chỉ tồn tại trên nhánh.

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

### 4.3 Ba nhánh mang nội dung CHƯA land — đo đích danh

| Nhánh | Bằng chứng (rc trực tiếp) | Decision |
|---|---|---|
| `origin/claude/ras-17-data-pr13-windows-bjovq2` | `git grep -q 'rasoat-anchor' <branch> -- scripts/` rc=**0**; trên canonical rc=**1** ⇒ tính năng `tl rasoat-anchor` VẮNG ở canonical | `rebase` |
| `origin/claude/nlm-registry-sheet-dup-s22fk7` | 2 tệp chỉ có trên nhánh; `git cat-file -e b044f8b1:rasoat/KETQUA_R281_V1_V2_V3_2026-07-31.md` rc=**128** | `rebase` |
| `origin/claude/audit-errors-patch-plan-56x4rq` | 1 tệp chỉ có trên nhánh; `git cat-file -e b044f8b1:docs/AUDIT_XAC_MINH_VA_KE_HOACH_VA_2026-07-31.md` rc=**128** | `finish rồi rebase` |

Kiểm chéo âm tính: 30 nhánh nhóm CHANGELOG và 4 nhánh nhóm merged-PR đều có
`diff --diff-filter=A` **rỗng (0/30, 0/4)** — không có nội dung nấp sau một dòng changelog.

Đối chiếu: `70 close + 2 rebase + 1 finish rồi rebase = 73`.
Phân lớp bằng chứng: `26 ancestry + 4 merged-PR + 30 CHANGELOG + 10 không-tệp-riêng + 3 chưa-land = 73`.

### 4.4 Bảng kiểm kê

| # | Remote branch | Tip | Commit date | Owner / bằng chứng | Decision | Basis (lệnh + rc) |
|---:|---|---|---|---|---|---|
| 1 | `origin/claude/audit-errors-patch-plan-56x4rq` | `4c0332f05252` | `2026-07-31T16:01:11+00:00` | `unknown` | `finish rồi rebase` | 1 tệp chỉ có trên nhánh: `docs/AUDIT_XAC_MINH_VA_KE_HOACH_VA_2026-07-31.md`; cần owner triage trước |
| 2 | `origin/claude/baotri-kho-bhxh-luot2` | `fcf9053537cb` | `2026-08-02T21:32:25+07:00` | `ducthangho` — tác giả PR #16 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 3 | `origin/claude/bhxh-41-2024-maintenance-jncsle` | `c0cbc96bbbee` | `2026-08-02T12:11:23+00:00` | `ducthangho` — tác giả PR #13 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 4 | `origin/claude/codex-exclude-dir` | `1050c17fb96b` | `2026-08-04T00:52:22+07:00` | `ducthangho` — tác giả PR #30 | `close` | `merge-base --is-ancestor <tip> canonical` rc=0 — nội dung ĐÃ nằm trong canonical |
| 5 | `origin/claude/corpus-audit-write-2026-07-31-3twkfb` | `3500f1fde2b7` | `2026-07-31T04:34:33+00:00` | `unknown` | `close` | 0 tệp chỉ có trên nhánh (`diff --diff-filter=A` rỗng) — bị canonical thay thế |
| 6 | `origin/claude/cuu-viec-treo-2026-08-03` | `6c148d331e5d` | `2026-08-04T00:21:52+07:00` | `unknown` | `close` | 0 tệp chỉ có trên nhánh (`diff --diff-filter=A` rỗng) — bị canonical thay thế |
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
| 49 | `origin/claude/ras-17-data-pr13-windows-bjovq2` | `411b3f3fb749` | `2026-08-02T13:36:58+00:00` | `unknown` | `rebase` | `rasoat-anchor` CÓ trên nhánh (grep rc=0), VẮNG trên canonical (rc=1) — tính năng chưa land |
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

### 4.5 Worktrees — KẾ THỪA, CHƯA ĐO LẠI

**Không dòng nào dưới đây được đo trong phiên này.** Toàn bộ là bản sao từ artifact tiền nhiệm
(PR #64, head `86dc0705`, đo `2026-08-09T00:48:42+07:00` trên máy Windows của chủ kho). Giữ lại vì
xoá đi sẽ khiến phiên sau tưởng kiểm kê worktree đã sạch — nó chưa hề được chạy lại.

Tổng kế thừa: **58 worktrees live, 0 prunable · 8 chứa EOL / 50 legacy · 55 clean / 3 dirty ·
57/58 `owner=unknown`**. Phân bổ decision kế thừa: `39 close + 11 rebase + 8 finish rồi rebase`.

Ba worktrees **dirty** cần owner xử lý tại chỗ trước mọi thao tác:

1. `D:/Quốc hội/tra-luat` (`master`) — 6 mục untracked.
2. `…/.claude/worktrees/wp51-g1-f1-01-fix-codex` — modified `scripts/tl_selftest.py`.
3. `D:/Quốc hội/tra-luat-wt/wp41-f1-01-codex` — modified `scripts/tl_selftest.py`, untracked
   `scripts/tl_core/test_fragments.py`.

Bốn detached legacy worktrees có commit riêng/không được ref tới, phải bảo toàn trước khi rebase:
`…/.codex/worktrees/03aa`, `18db`, `4411`, `b26f` (đường dẫn đầy đủ trong PR #64).

Điều kiện đóng hạng mục này: chạy lại `git worktree list --porcelain`,
`git worktree prune --dry-run --verbose`, `merge-base --is-ancestor` và `status --short` **trên
chính máy Windows đó**, rồi thay bảng kế thừa bằng số đo mới.

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

1. **Hook chỉ phủ máy đã cấu hình `core.hooksPath`.** Đo ngay tại container này:
   `git config core.hooksPath` → **rc=1 (chưa đặt)**. Tức chính bản sao đang chạy kiểm kê này KHÔNG
   được hook bảo vệ. Máy chưa cấu hình, hoặc `--no-verify`, đều đi vòng qua được. Hook là hàng rào
   phía client, không phải cưỡng chế phía server.
2. **Không hồi tố.** 73 nhánh legacy đã nằm sẵn trên `origin` TRƯỚC khi cơ chế land — chúng không bị
   chặn hồi tố, chỉ bị chặn ở **lần push kế tiếp**. Đừng đọc "#52 đã land" thành "73 nhánh đã an toàn".
3. **Không có cưỡng chế phía server.** `master` hiện `protected: false` (đọc qua GitHub API,
   `list_branches`). Required status checks không bật.

**Về branch protection / ruleset:** artifact tiền nhiệm ghi API trả HTTP 403 kèm
`Upgrade to GitHub Pro or make this repository public to enable this feature`. Phiên này **không
tái kiểm được** khẳng định đó: `curl` tới `api.github.com/…/protection` và `…/rulesets` đều trả
**HTTP 403 nhưng với thông điệp KHÁC** — `GitHub access is not enabled for this session` — tức
403 của **proxy phiên**, không phải 403 **theo gói của repo**. Hai cái này khác nhau và không được
gộp. Vì vậy: **không khai required checks / branch protection / ruleset là khả dụng**, đồng thời
**không khẳng định** đã tự tay xác minh nguyên nhân 403 là do private plan free. Điều đo được chắc
chắn trong phiên này chỉ là `protected: false` trên `master`.

## 6. Sai lệch đã sửa so với artifact tiền nhiệm (PR #64)

Ghi ra để không ai chép lại lỗi này.

PR #64 ghi basis **`ancestor master`** cho khoảng 44 dòng `close`. Basis đó **không tái lập được**:

```
git merge-base --is-ancestor origin/claude/r210-rasoat-dot2 91d5e8dc…  → rc=1
git merge-base --is-ancestor origin/claude/r210-rasoat-dot2 b044f8b1…  → rc=1
```

Chỉ **26/73** nhánh là ancestor của master — đo ở CẢ base cũ `91d5e8dc` lẫn canonical `b044f8b1`,
cùng ra 26. Vì `91d5e8dc` là ancestor của `b044f8b1` (rc=0), ancestry có tính bắc cầu, nên con số
không thể khác nhau giữa hai mốc: basis cũ sai tại thời điểm nó được ghi, không phải do trôi base.

Hệ quả: **tập quyết định không đổi** (vẫn 70/2/1, cùng 3 nhánh ngoại lệ), nhưng **căn cứ đã được
thay bằng bằng chứng chạy lại được** (§4.1). Một dòng `close` dựa trên basis sai vẫn là rủi ro xoá
nhầm, kể cả khi kết luận tình cờ đúng.

## 7. Điều kiện gỡ blocker

Không đổi verdict và không mở lại writer cho tới khi đủ bằng chứng dương:

1. **Kiểm kê worktree chạy lại trên máy Windows** — thay §4.5 bằng số đo thật (§2).
2. 3 nhánh §4.3 đã rebase lên tip chứa EOL, hoặc owner quyết định bỏ có ghi nhận.
3. 43 mục `owner=unknown` có owner, hoặc có quyết định human rõ ràng cho từng mục.
4. 3 worktrees dirty được owner xử lý và kiểm lại.
5. Mọi mục `close` được owner xác nhận trước khi xoá; không mất dirty hay commit riêng.
6. Chạy lại kiểm kê trên canonical mới, kết quả không còn residual writer trái chính sách.

Cho tới lúc đó: giữ **#63, #49, #48 MỞ**. Không tuyên bố F2-D hoàn tất vận hành.
