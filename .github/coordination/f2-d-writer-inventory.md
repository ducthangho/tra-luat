# F2-D — kiểm kê writer trước khi mở lại

## Kết luận

**Verdict: `blocked`. Writer vẫn phải giữ trạng thái đóng băng.**

Tại thời điểm quan sát `2026-08-09T00:48:42+07:00`, `origin/master` và base của packet cùng ở `91d5e8dc0133b1d9942d5868032aacf2ea9d2ff9`. Commit EOL chuẩn là `1880346d2be3c0be9a93de7624ee108d99b6c88c`.

Các điều kiện để mở lại chưa đạt:

- 73 remote branches chưa chứa commit EOL: 70 `close`, 2 `rebase`, 1 `finish rồi rebase`.
- 58 worktrees đều live/non-prunable; 50 chưa chứa commit EOL và 8 đã chứa. Trong 50 legacy worktrees: 36 `close`, 9 `rebase`, 5 `finish rồi rebase`.
- 3 worktrees đang dirty; không được tự ý sửa, rebase hoặc đóng.
- 43/73 remote branches không có bằng chứng owner trực tiếp từ PR. `owner=unknown` được giữ nguyên, không suy từ namespace hay tác giả commit.
- 57/58 worktrees có `owner=unknown`; tên branch/path chỉ được giữ làm routing hint. Worktree F2-D hiện tại là ngoại lệ duy nhất vì có lease #63 cho Codex.
- Không có cơ chế tự động cưỡng chế branch ancestry. Issue [#52](https://github.com/ducthangho/tra-luat/issues/52) vẫn chưa triển khai và revision hiện tại của issue đó cũng chỉ gate ref đích `master`, không gate mọi writer branch.

Artifact này chỉ là inventory/decision record. F2-D **không** xóa remote branch, prune/remove worktree, rebase, sửa dữ liệu dirty, mở writer, hoặc sửa hook/CI.

## Nguồn điều phối và phương pháp

- Mission: [#48](https://github.com/ducthangho/tra-luat/issues/48), revision 2.
- Human MCR approval: [MCR-48-01](https://github.com/ducthangho/tra-luat/issues/48#issuecomment-5227303367).
- Packet: [#63](https://github.com/ducthangho/tra-luat/issues/63), revision 1, generation 1.
- Parent drain packet: [#49](https://github.com/ducthangho/tra-luat/issues/49).
- Plan hash: `340b15a934cc27f2aa5d542973e12c268ab4db4307b390a77e66bc9d6a060d11`.
- Packet spec hash: `de63e124ed39a94108f87770c2bec9ec39a25119795ce9f6534d7084fd4d0fea`.

Kiểm kê dùng các phép đo đọc-chỉ:

```text
git fetch --prune origin
git branch -r --no-contains 1880346d2be3c0be9a93de7624ee108d99b6c88c
git worktree list --porcelain
git worktree prune --dry-run --verbose
git -C <worktree> merge-base --is-ancestor 1880346d2be3c0be9a93de7624ee108d99b6c88c HEAD
git -C <worktree> status --short --untracked-files=all
gh pr list --state all --head <branch> --json number,author,state,mergedAt
```

| Phép đo | rc | Kết quả đọc lại |
|---|---:|---|
| `git fetch --prune origin` | 0 | fetch hoàn tất; base quan sát không drift |
| `git branch -r --no-contains <EOL_SHA>` | 0 | 73 remote branches |
| `git worktree list --porcelain` | 0 | 58 worktrees live |
| `git worktree prune --dry-run --verbose` | 0 | 0 worktree prunable |
| `git -C <worktree> merge-base --is-ancestor <EOL_SHA> HEAD` (58 lần) | 0 cho 8; 1 cho 50; không rc>1 | 8 chứa EOL, 50 chưa chứa; rc=1 là kết quả ancestry âm dự kiến |
| `git -C <worktree> status --short --untracked-files=all` (58 lần) | 0 cho 58/58 | 55 clean, 3 dirty |
| `gh pr list ... --head <branch>` (73 lần) | 0 cho 73/73 | 30 branches có direct PR evidence; 43 không có |

Kết quả kiểm đếm được đối chiếu độc lập: remote `73 = 70 close + 2 rebase + 1 finish rồi rebase`; worktree `58 = 39 close + 11 rebase + 8 finish rồi rebase`, `8 EOL + 50 legacy`, `55 clean + 3 dirty`, `0 prunable`.

Quy ước quyết định:

- `close`: tip đã land/được supersede, hoặc worktree review/đã hoàn tất; chỉ thực thi sau khi owner được xác nhận nếu owner đang unknown.
- `rebase`: còn giá trị cần tiếp tục và phải cập nhật lên accepted base mới nhất. Với tip legacy, base mới phải chứa commit EOL; với tip đã có EOL, quyết định này là freshness update sau khi upstream tiến thêm.
- `finish rồi rebase`: còn dữ liệu/commit cần triage hoặc worktree đang làm dở; hoàn tất/bảo toàn trước, sau đó mới cập nhật lên accepted base mới nhất có EOL. Đây là nhãn workflow inventory, không cho phép rewrite canonical `master`: riêng worktree `R` phải xử lý dữ liệu dirty rồi fast-forward/reconcile an toàn thay vì rebase lịch sử `master`.

Quy ước owner:

- `D#N` = **candidate owner** `ducthangho`, bằng chứng trực tiếp là author của PR #N; đây không phải suy đoán từ commit author.
- `Codex branch/path hint` và `Claude branch/path hint` chỉ là routing hint từ tên branch/path, **không** phải owner evidence; trường owner của các dòng đó vẫn là `unknown`.
- `U` = `owner=unknown`; không suy owner từ namespace hoặc tác giả commit.

## Remote branches chưa chứa EOL (73)

| # | Remote branch | Tip | Commit date | Owner/evidence | Decision | Basis |
|---:|---|---|---|---|---|---|
| 1 | `origin/claude/audit-errors-patch-plan-56x4rq` | `4c0332f05252` | `2026-07-31T16:01:11Z` | U | `finish rồi rebase` | 3 docs-only commits độc nhất, không PR; cần owner triage |
| 2 | `origin/claude/baotri-kho-bhxh-luot2` | `fcf9053537cb` | `2026-08-02T21:32:25+07:00` | D#16 | `close` | ancestor master; PR merged |
| 3 | `origin/claude/bhxh-41-2024-maintenance-jncsle` | `c0cbc96bbbee` | `2026-08-02T12:11:23Z` | D#13 | `close` | ancestor master; PR merged |
| 4 | `origin/claude/codex-exclude-dir` | `1050c17fb96b` | `2026-08-04T00:52:22+07:00` | D#30 | `close` | ancestor master; PR merged |
| 5 | `origin/claude/corpus-audit-write-2026-07-31-3twkfb` | `3500f1fde2b7` | `2026-07-31T04:34:33Z` | U | `close` | ancestor master |
| 6 | `origin/claude/cuu-viec-treo-2026-08-03` | `6c148d331e5d` | `2026-08-04T00:21:52+07:00` | U | `close` | payload land/supersede bởi `dcab765`/PR #33 |
| 7 | `origin/claude/deploy-v1-35-61-ci-5f7wdw` | `e094512a37ca` | `2026-07-29T02:48:58Z` | D#1,#2 | `close` | ancestor master; PRs merged |
| 8 | `origin/claude/gate-04-05-t0f-hi76xl` | `eb9132f3aa2b` | `2026-08-02T09:45:41Z` | D#8,#9,#12 | `close` | ancestor master; PRs merged |
| 9 | `origin/claude/legal-doc-review-architecture-2al46n` | `f39f98398d7b` | `2026-07-26T08:06:51+07:00` | U | `close` | ancestor master |
| 10 | `origin/claude/luat-bhxh-30-07-fyc9tq` | `3e9a90c77f69` | `2026-07-30T09:12:32Z` | D#5 | `close` | ancestor master; PR merged |
| 11 | `origin/claude/nifty-diffie-63b72e` | `45513c5b4358` | `2026-08-03T09:51:42+07:00` | D#22 | `close` | ancestor master; PR merged |
| 12 | `origin/claude/nlm-queue-vbqppl-56qz82` | `e234bd38e24b` | `2026-07-31T02:53:10Z` | U | `close` | ancestor master |
| 13 | `origin/claude/nlm-registry-sheet-dup-s22fk7` | `0bb60d215c02` | `2026-07-31T06:25:47Z` | U | `rebase` | 3 commits độc nhất; helper/detector còn vắng trên master |
| 14 | `origin/claude/p15-review-tra-luat-osp5td` | `cc20b71e855e` | `2026-07-30T20:37:05Z` | U | `close` | ancestor master |
| 15 | `origin/claude/prompt-phien-ke-sau-rc-21og1d` | `fa255e827eef` | `2026-07-25T09:31:40Z` | U | `close` | ancestor master |
| 16 | `origin/claude/r210-rasoat-dot2` | `d82ef707fb26` | `2026-07-26T07:15:50+07:00` | U | `close` | ancestor master |
| 17 | `origin/claude/r211-rasoat-dot3` | `386c8ccffdc7` | `2026-07-26T08:06:00+07:00` | U | `close` | ancestor master |
| 18 | `origin/claude/r212-guard-bind-path` | `c226ae165193` | `2026-07-26T08:53:42+07:00` | U | `close` | ancestor master |
| 19 | `origin/claude/r213-rasoat-dot5` | `e9fea2d7a1d6` | `2026-07-26T11:44:27+07:00` | U | `close` | ancestor master |
| 20 | `origin/claude/r215-khoi-dau-van-ban` | `b77306ec6cac` | `2026-07-27T11:06:09+08:00` | U | `close` | ancestor master |
| 21 | `origin/claude/r216-rasoat-merge-cong-trung` | `23ab5f297654` | `2026-07-27T22:44:27+08:00` | U | `close` | ancestor master |
| 22 | `origin/claude/r217-doc-patch-loc-congbao` | `e777cd294d9f` | `2026-07-28T00:23:26+08:00` | U | `close` | ancestor master |
| 23 | `origin/claude/r219-doc-claims-l8-l9-gotchas` | `e8f2f85b010f` | `2026-07-28T03:19:26+08:00` | U | `close` | ancestor master |
| 24 | `origin/claude/r221-verify-deep-t1-sohieu` | `036b63f68db6` | `2026-07-28T09:50:52+08:00` | U | `close` | ancestor master |
| 25 | `origin/claude/r255-bare-vbhn-rasoat-chongcheo` | `264f562dbd89` | `2026-07-30T09:36:27Z` | U | `close` | ancestor master |
| 26 | `origin/claude/r256-rasoat-loop-dry-rounds` | `008ce8259e0f` | `2026-07-30T09:37:57Z` | U | `close` | ancestor master |
| 27 | `origin/claude/r257-sweep-corpus-predicate` | `4c75c591ba0c` | `2026-07-30T09:39:19Z` | U | `close` | ancestor master |
| 28 | `origin/claude/r258-vbhn-goc-map-corpus-rule` | `433ec06e85a6` | `2026-07-30T09:40:38Z` | U | `close` | ancestor master |
| 29 | `origin/claude/r259-dong-bo-so-r-trong-chu-thich` | `c833677518dc` | `2026-07-30T09:48:23Z` | U | `close` | ancestor master |
| 30 | `origin/claude/r260-test-r255-r258-vao-selftest` | `c51319e45d07` | `2026-07-30T11:42:25Z` | U | `close` | ancestor master |
| 31 | `origin/claude/r261-monkeypatch-dung-cua-stub` | `d63fec4cd18c` | `2026-07-30T12:04:38Z` | U | `close` | ancestor master |
| 32 | `origin/claude/r262-selftest-hermetic-chan-mang` | `d82f3b311d29` | `2026-07-30T12:46:14Z` | U | `close` | ancestor master |
| 33 | `origin/claude/r263-merge-legal-doc-review-architecture` | `cf6ae53ae6e9` | `2026-07-30T13:19:13Z` | U | `close` | ancestor master |
| 34 | `origin/claude/r264-doc-claims-phu-docs` | `320952a64185` | `2026-07-30T13:39:28Z` | U | `close` | ancestor master |
| 35 | `origin/claude/r266-doc-text-sanitize-u1` | `3e440eff0c19` | `2026-07-30T19:25:38Z` | U | `close` | ancestor master |
| 36 | `origin/claude/r267-parity-4-reader-cache-u1` | `a4ebf7442c33` | `2026-07-30T20:27:05Z` | U | `close` | ancestor master |
| 37 | `origin/claude/r268-r264-sha-may-phu-thuoc` | `cc20b71e855e` | `2026-07-30T20:37:05Z` | U | `close` | ancestor master |
| 38 | `origin/claude/r269-dedup-status-active-alias` | `955965832168` | `2026-07-31T05:23:47+08:00` | U | `close` | ancestor master |
| 39 | `origin/claude/r270-vbhn-for-goc-boundary` | `eed79ed24315` | `2026-07-31T05:31:03+08:00` | U | `close` | ancestor master |
| 40 | `origin/claude/r271-hieuluc-negation-first` | `ae89d6fb35bb` | `2026-07-31T05:37:26+08:00` | U | `close` | ancestor master |
| 41 | `origin/claude/r272-classify-ref-canonical-chon` | `49de1bb5c4e0` | `2026-07-31T05:55:32+08:00` | U | `close` | ancestor master |
| 42 | `origin/claude/r273-vbhn-gate-cutoff-dong` | `ef3f64f5c7a8` | `2026-07-31T06:09:31+08:00` | U | `close` | ancestor master |
| 43 | `origin/claude/r274-fixture-vbhn-nam` | `2fe439230ae8` | `2026-07-31T06:18:30+08:00` | U | `close` | ancestor master |
| 44 | `origin/claude/r275-vbhn-base-key-tie-break` | `9c8e5b27eca8` | `2026-07-31T06:47:28+08:00` | U | `close` | ancestor master |
| 45 | `origin/claude/r276-sohieu-khong-nam-detector` | `44da73864caa` | `2026-07-31T06:59:52+08:00` | U | `close` | ancestor master |
| 46 | `origin/claude/r323-tach-duoi-vbhn` | `9775d867eeaa` | `2026-08-03T00:38:04+07:00` | D#18 | `close` | ancestor master; PR merged |
| 47 | `origin/claude/r325-noi-lai-duoi-vbhn` | `1bdc16c73421` | `2026-08-03T02:04:23+07:00` | D#20 | `close` | ancestor master; PR merged |
| 48 | `origin/claude/ras-01-ras-14-metadata-cli-bi25ke` | `93a7dab7a4d4` | `2026-08-02T07:14:58Z` | D#10 | `close` | ancestor master; PR merged |
| 49 | `origin/claude/ras-17-data-pr13-windows-bjovq2` | `411b3f3fb749` | `2026-08-02T13:36:58Z` | U | `rebase` | 1 commit độc nhất; `rasoat-anchor` vắng trên master |
| 50 | `origin/claude/ras17-merge-gate-anchor` | `d8a3acee53b3` | `2026-08-02T20:42:11+07:00` | D#15 | `close` | ancestor master; PR merged |
| 51 | `origin/claude/ras18-doc-patch-hash-vo-hieu` | `cbe21dc88274` | `2026-08-02T23:22:04+07:00` | D#17 | `close` | ancestor master; PR merged |
| 52 | `origin/claude/rasoat-luat-bhxh-pending-svev2v` | `296e5c078e6d` | `2026-07-30T07:16:05Z` | U | `close` | ancestor master |
| 53 | `origin/claude/rasoat-luot19-kho-nen` | `a99463361cd4` | `2026-07-31T05:21:27+08:00` | U | `close` | ancestor master |
| 54 | `origin/claude/recursing-nightingale-76526b` | `1f22c7da9302` | `2026-08-03T02:37:32+07:00` | D#21 | `close` | ancestor master; PR merged |
| 55 | `origin/claude/refresh-token-gws-nlm-k4mt2m` | `14d1e354ebe5` | `2026-07-30T04:00:45Z` | D#4 | `close` | ancestor master; PR merged |
| 56 | `origin/claude/rel05-nlm08` | `aada9647e053` | `2026-08-03T01:38:31+07:00` | D#19 | `close` | ancestor master; PR merged |
| 57 | `origin/claude/reverent-torvalds-6a0ab8` | `103b43a47e0c` | `2026-08-03T23:43:07+07:00` | D#28 | `close` | ancestor master; PR merged |
| 58 | `origin/claude/review-bhxh-law-profile-2m08hz` | `b5b7831c21ec` | `2026-07-29T14:07:31Z` | U | `close` | ancestor master |
| 59 | `origin/claude/review-tra-luat-plan-qto0bb` | `2a2b890ee803` | `2026-07-23T09:19:31Z` | U | `close` | ancestor master |
| 60 | `origin/claude/sad-clarke-fdf8f0` | `615915958389` | `2026-08-03T22:22:53+07:00` | D#24 | `close` | ancestor master; PR merged |
| 61 | `origin/claude/selftest-r218-r219-bundle-k69xeh` | `f27684bdb706` | `2026-07-29T04:47:45Z` | D#3 | `close` | ancestor master; PR merged |
| 62 | `origin/claude/t0f-doc01-ras17-ing09-pdfvkn` | `9be57d6006fb` | `2026-08-02T08:26:16Z` | D#11 | `close` | ancestor master; PR merged |
| 63 | `origin/claude/t2-pro03-pro09-pro05-ing04-ing06` | `cd2d93418022` | `2026-08-02T13:02:34Z` | D#14 | `close` | ancestor master; PR merged |
| 64 | `origin/claude/tra-luat-r300-handoff-wpicyt` | `ccee68cd2236` | `2026-08-02T02:11:57Z` | D#7 | `close` | ancestor master; PR merged |
| 65 | `origin/claude/va-t1-gate-nlvoj9` | `88c41e312c5d` | `2026-08-01T15:38:37Z` | D#6 | `close` | ancestor master; PR merged |
| 66 | `origin/codex/d0-bootstrap-quote-fix` | `76435d6f4a51` | `2026-08-03T23:49:52+07:00` | D#29 | `close` | ancestor master; PR merged |
| 67 | `origin/codex/d0-constitution-rescue` | `dcab765acbdf` | `2026-08-04T02:38:55+07:00` | D#33 | `close` | ancestor master; PR merged |
| 68 | `origin/codex/d0-preview-already-landed` | `6f54fc0d02d0` | `2026-08-04T07:07:52+07:00` | D#34 | `close` | ancestor master; PR merged |
| 69 | `origin/codex/d0-workflow-controller` | `ac3fe25c17de` | `2026-08-04T01:02:39+07:00` | D#31 | `close` | ancestor master; PR merged |
| 70 | `origin/codex/f2-a-eol-policy` | `070cee76a63c` | `2026-08-07T18:49:25+07:00` | D#50 | `close` | ancestor master; PR merged |
| 71 | `origin/codex/release-v1.36.64` | `bd11532d2468` | `2026-08-04T01:38:43+07:00` | D#32 | `close` | ancestor master; PR merged |
| 72 | `origin/codex/work-packet-bootstrap` | `cefdb73d2c42` | `2026-08-03T22:58:58+07:00` | D#25 | `close` | ancestor master; PR merged |
| 73 | `origin/codex/work-packet-bootstrap-2` | `8876c3a4d426` | `2026-08-03T23:28:44+07:00` | D#26 | `close` | ancestor master; PR merged |

## Worktrees (58 live, 0 prunable)

Path aliases: `R=D:/Quốc hội/tra-luat`, `A=C:/Users/admin/.codex/worktrees`, `C=D:/Quốc hội/tra-luat/.claude/worktrees`, `X=D:/Quốc hội/tra-luat/.codex/worktrees`, `W=D:/Quốc hội/tra-luat-wt`.

| # | Path | Branch/detached | Tip | Date | EOL | Dirty | Owner / routing hint | Decision |
|---:|---|---|---|---|---|---|---|---|
| 1 | `R` | `master` | `91d5e8dc0133` | `2026-08-09T00:07:42+07:00` | yes | 6 untracked | unknown | `finish rồi rebase` |
| 2 | `A/03aa/tra-luat` | detached | `828ec8ff4aa6` | `2026-08-07T16:11:00+07:00` | no | clean | unknown; Codex path hint | `finish rồi rebase` |
| 3 | `A/18db/tra-luat` | detached | `ac00d0ee3505` | `2026-08-07T16:32:20+07:00` | no | clean | unknown; Codex path hint | `finish rồi rebase` |
| 4 | `A/1b4b/tra-luat` | detached | `fc50a5416d8d` | `2026-08-07T01:15:54+07:00` | no | clean | unknown; Codex path hint | `close` |
| 5 | `A/431a/tra-luat` | detached | `31602843cc7f` | `2026-08-06T15:10:13+07:00` | no | clean | unknown; Codex path hint | `close` |
| 6 | `A/4411/tra-luat` | detached | `377f4d130c0e` | `2026-08-07T18:49:25+07:00` | no | clean | unknown; Codex path hint | `finish rồi rebase` |
| 7 | `A/537d/tra-luat` | `codex/f2-a-eol-policy-r3` | `def2bd46770b` | `2026-08-07T16:14:12+07:00` | no | clean | unknown; Codex branch hint | `rebase` |
| 8 | `A/68e8/tra-luat` | detached | `0844c0bc2439` | `2026-08-08T06:54:13+07:00` | yes | clean | unknown; Codex path hint | `close` |
| 9 | `A/b26f/tra-luat` | detached | `2cc9576fcadf` | `2026-08-07T13:00:32+07:00` | no | clean | unknown; Codex path hint | `finish rồi rebase` |
| 10 | `A/cf7e/tra-luat` | `codex/f2-a-eol-policy` | `070cee76a63c` | `2026-08-07T18:49:25+07:00` | no | clean | unknown; Codex branch hint | `close` |
| 11 | `D:/Quốc hội/luot3_wt` | `claude/r325-noi-lai-duoi-vbhn` | `1bdc16c73421` | `2026-08-03T02:04:23+07:00` | no | clean | unknown; Claude branch hint | `close` |
| 12 | `D:/Quốc hội/p16_wt` | `claude/r299-bridge-scope-va-chunks-apply` | `7469d8c96df8` | `2026-08-01T17:03:25+07:00` | no | clean | unknown; Claude branch hint | `close` |
| 13 | `D:/Quốc hội/rasoat_docs_wt` | `claude/legal-doc-review-architecture-2al46n` | `f39f98398d7b` | `2026-07-26T08:06:51+07:00` | no | clean | unknown; Claude branch hint | `close` |
| 14 | `D:/Quốc hội/rel05_wt` | `claude/rel05-nlm08` | `e9bea049f341` | `2026-08-03T01:00:01+07:00` | no | clean | unknown; Claude branch hint | `rebase` |
| 15 | `C/nifty-diffie-63b72e` | `claude/nifty-diffie-63b72e` | `39e860c725ff` | `2026-08-03T10:43:50+07:00` | no | clean | unknown; Claude branch hint | `close` |
| 16 | `C/recursing-nightingale-76526b` | detached | `1f22c7da9302` | `2026-08-03T02:37:32+07:00` | no | clean | unknown; Claude path hint | `close` |
| 17 | `C/reverent-torvalds-6a0ab8` | `claude/codex-exclude-dir` | `1050c17fb96b` | `2026-08-04T00:52:22+07:00` | no | clean | unknown; Claude branch hint | `close` |
| 18 | `C/sad-clarke-fdf8f0` | `claude/sad-clarke-fdf8f0` | `615915958389` | `2026-08-03T22:22:53+07:00` | no | clean | unknown; Claude branch hint | `close` |
| 19 | `C/wp51-g1-f1-01-fix-codex` | `codex/wp51-g1-f1-01-fix` | `1880346d2be3` | `2026-08-08T01:03:44+07:00` | yes | `M scripts/tl_selftest.py` | unknown; Codex branch hint | `finish rồi rebase` |
| 20 | `C/wp51-g2-f1-01-fix-codex` | `codex/wp51-g2-f1-01-fix` | `3c8df84bfdf7` | `2026-08-08T01:55:02+07:00` | yes | clean | unknown; Codex branch hint | `close` |
| 21 | `C/wp55-f3-03-claude` | `claude/wp55-f3-03` | `a3e39573a269` | `2026-08-08T10:25:33+07:00` | yes | clean | unknown; Claude branch hint | `rebase` |
| 22 | `C/wp57-g2-f3-00-governance-codex` | `codex/wp57-g2-f3-00-governance` | `d2bc8e0de88c` | `2026-08-08T12:02:33+07:00` | yes | clean | unknown; Codex branch hint | `close` |
| 23 | `C/wp60-g1-f3-01-claude` | `claude/wp60-g1-f3-01-github-schema` | `b5cc5d688a75` | `2026-08-08T21:47:19+07:00` | yes | clean | unknown; Claude branch hint | `rebase` |
| 24 | `X/d0-bootstrap-hardening` | `codex/d0-bootstrap-hardening` | `768b160511f0` | `2026-08-03T23:32:00+07:00` | no | clean | unknown; Codex branch hint | `rebase` |
| 25 | `X/d0-bootstrap-quote-fix` | `codex/d0-bootstrap-quote-fix` | `76435d6f4a51` | `2026-08-03T23:49:52+07:00` | no | clean | unknown; Codex branch hint | `close` |
| 26 | `X/d0-constitution-rescue` | `codex/d0-constitution-rescue` | `d1016d24647e` | `2026-08-04T02:57:37+07:00` | no | clean | unknown; Codex branch hint | `close` |
| 27 | `X/d0-preview-already-landed` | `codex/d0-preview-already-landed` | `c5e8a9d42d6c` | `2026-08-04T08:49:24+07:00` | no | clean | unknown; Codex branch hint | `close` |
| 28 | `X/d0-workflow-controller` | `codex/d0-workflow-controller` | `ac3fe25c17de` | `2026-08-04T01:02:39+07:00` | no | clean | unknown; Codex branch hint | `close` |
| 29 | `X/release-v1-36-64` | `codex/release-v1.36.64` | `fd3d0e5e2e35` | `2026-08-04T01:47:26+07:00` | no | clean | unknown; Codex branch hint | `close` |
| 30 | `X/review-wp37-g2` | detached | `c5e8a9d42d6c` | `2026-08-04T08:49:24+07:00` | no | clean | unknown; Codex path hint | `close` |
| 31 | `X/reviewer-cross-platform` | `codex/reviewer-cross-platform` | `65f5e4944709` | `2026-08-04T16:23:04+08:00` | no | clean | unknown; Codex branch hint | `rebase` |
| 32 | `X/wp-bootstrap` | `codex/work-packet-bootstrap` | `c50700675ae5` | `2026-08-03T23:22:42+07:00` | no | clean | unknown; Codex branch hint | `rebase` |
| 33 | `X/wp46-f1-docs` | `codex/wp46-f1-docs` | `004bb98e0009` | `2026-08-06T23:58:09+07:00` | no | clean | unknown; Codex branch hint | `close` |
| 34 | `X/wp47-f1-staleness` | `codex/wp47-f1-staleness` | `6f24f9008ad1` | `2026-08-07T01:05:56+07:00` | no | clean | unknown; Codex branch hint | `close` |
| 35 | `R/work/f2-d-reopen-writer` | `codex/f2-d-reopen-writer` | `91d5e8dc0133` | `2026-08-09T00:07:42+07:00` | yes | clean | Codex; packet #63 lease | `finish rồi rebase` |
| 36 | `W/f1-40-integration` | `codex/f1-40-integration` | `b303a734b9af` | `2026-08-06T21:19:54+07:00` | no | clean | unknown; Codex branch hint | `close` |
| 37 | `W/f1-40-land` | `codex/f1-40-land` | `8be3398d60b8` | `2026-08-06T23:20:56+07:00` | no | clean | unknown; Codex branch hint | `close` |
| 38 | `W/f1-40-land-review-8be3398` | detached | `8be3398d60b8` | `2026-08-06T23:20:56+07:00` | no | clean | U | `close` |
| 39 | `W/followups-46-47-land-review-fc50a54` | detached | `fc50a5416d8d` | `2026-08-07T01:15:54+07:00` | no | clean | U | `close` |
| 40 | `W/review-wp41-g2` | detached | `cad2e32df83a` | `2026-08-05T08:28:16+07:00` | no | clean | U | `close` |
| 41 | `W/review-wp41-g3` | detached | `8bd09894f2e3` | `2026-08-05T16:06:06+07:00` | no | clean | U | `close` |
| 42 | `W/review-wp41-g4` | detached | `06df58f64297` | `2026-08-05T18:11:51+07:00` | no | clean | U | `close` |
| 43 | `W/review-wp42-g1` | detached | `ac78b7c493ab` | `2026-08-05T22:51:12+07:00` | no | clean | U | `close` |
| 44 | `W/review-wp42-g2` | detached | `8074ec9a1a93` | `2026-08-06T02:42:09+07:00` | no | clean | U | `close` |
| 45 | `W/review-wp42-g3` | detached | `98e91f280915` | `2026-08-06T06:48:27+07:00` | no | clean | U | `close` |
| 46 | `W/review-wp43-g1` | detached | `d30e46aa6c6a` | `2026-08-06T09:37:45+07:00` | no | clean | U | `close` |
| 47 | `W/review-wp44-g1` | detached | `31602843cc7f` | `2026-08-06T15:10:13+07:00` | no | clean | U | `close` |
| 48 | `W/review-wp45-g1` | detached | `b303a734b9af` | `2026-08-06T21:19:54+07:00` | no | clean | U | `close` |
| 49 | `W/wp41-f1-01-codex` | `codex/wp41-g1-f1-01` | `c5e8a9d42d6c` | `2026-08-04T08:49:24+07:00` | no | `M tl_selftest.py; ?? test_fragments.py` | unknown; Codex branch hint | `finish rồi rebase` |
| 50 | `W/wp41-g2-f1-01-codex` | `codex/wp41-g2-f1-01` | `cad2e32df83a` | `2026-08-05T08:28:16+07:00` | no | clean | unknown; Codex branch hint | `rebase` |
| 51 | `W/wp41-g3-f1-01-codex` | `codex/wp41-g3-f1-01` | `8bd09894f2e3` | `2026-08-05T16:06:06+07:00` | no | clean | unknown; Codex branch hint | `rebase` |
| 52 | `W/wp41-g4-f1-01-codex` | `codex/wp41-g4-f1-01` | `06df58f64297` | `2026-08-05T18:11:51+07:00` | no | clean | unknown; Codex branch hint | `close` |
| 53 | `W/wp42-g1-f1-02-codex` | `codex/wp42-g1-f1-02` | `ac78b7c493ab` | `2026-08-05T22:51:12+07:00` | no | clean | unknown; Codex branch hint | `rebase` |
| 54 | `W/wp42-g2-f1-02-codex` | `codex/wp42-g2-f1-02` | `8074ec9a1a93` | `2026-08-06T02:42:09+07:00` | no | clean | unknown; Codex branch hint | `rebase` |
| 55 | `W/wp42-g3-f1-02-codex` | `codex/wp42-g3-f1-02` | `98e91f280915` | `2026-08-06T06:48:27+07:00` | no | clean | unknown; Codex branch hint | `close` |
| 56 | `W/wp43-g1-f1-03-codex` | `codex/wp43-g1-f1-03` | `d30e46aa6c6a` | `2026-08-06T09:37:45+07:00` | no | clean | unknown; Codex branch hint | `close` |
| 57 | `W/wp44-g1-f1-04-codex` | `codex/wp44-g1-f1-04` | `31602843cc7f` | `2026-08-06T15:10:13+07:00` | no | clean | unknown; Codex branch hint | `close` |
| 58 | `W/wp45-g1-f1-05-codex` | `codex/wp45-g1-f1-05` | `b303a734b9af` | `2026-08-06T21:19:54+07:00` | no | clean | unknown; Codex branch hint | `close` |

Ba worktrees dirty cần owner xử lý tại chỗ trước mọi thao tác:

1. `R`: 6 untracked entries (5 research files và `work/`).
2. `C/wp51-g1-f1-01-fix-codex`: modified `scripts/tl_selftest.py`.
3. `W/wp41-f1-01-codex`: modified `scripts/tl_selftest.py`, untracked `scripts/tl_core/test_fragments.py`.

Bốn detached legacy worktrees có unique/unreferenced commits cần bảo toàn và triage trước rebase: `A/03aa/tra-luat`, `A/18db/tra-luat`, `A/4411/tra-luat`, `A/b26f/tra-luat`.

## Enforcement inventory

Tại `master@91d5e8d`:

- `.githooks/pre-push` và `.githooks/pre_push_test.py` không tồn tại (`git cat-file -e` trả rc=128).
- Không có kiểm tra `1880346`/`git merge-base --is-ancestor` trong `.githooks` hoặc `.github/workflows` (`git grep` trả rc=1).
- `.githooks/pre-commit` chỉ gọi `eol_policy.py --staged`. Nó kiểm byte EOL của staged blobs, có thể bị bỏ qua bằng `--no-verify`, và không kiểm ancestry.
- CI chạy kiểm EOL trên PR merge result và push `master`, nhưng không kiểm ancestry của PR head/writer tip.
- `master` hiện `protected:false`; required status checks có enforcement level `off` và không có required contexts.
- API branch protection và rulesets đều trả HTTP 403 với thông báo: `Upgrade to GitHub Pro or make this repository public to enable this feature.` Repository đang private trên plan hiện tại, nên không được tuyên bố required checks/rulesets đang hoạt động.

Issue #52 revision 1 dự kiến thêm pre-push gate cho push có ref đích `master`, đồng thời acceptance cho phép các ref đích khác đi qua. Vì vậy ngay cả khi triển khai nguyên revision đó, nó vẫn chưa cưỡng chế rằng mọi writer branch chứa commit EOL. Sửa `.githooks/pre-push`, test và `ci.yml` thuộc exact write-set của #52, ngoài write-set F2-D; cần revision được phê duyệt của #52 hoặc packet mới.

Cơ chế khả thi cho packet tiếp theo:

- pre-push đọc từng stdin row và fail closed nếu `git merge-base --is-ancestor 1880346d2be3c0be9a93de7624ee108d99b6c88c "$local_sha"` không trả 0 (trừ deletion SHA toàn số 0);
- PR CI fetch và kiểm `${{ github.event.pull_request.head.sha }}`; không kiểm `GITHUB_SHA` của synthetic merge ref vì base parent có thể tạo false assurance. Xem [GitHub pull_request semantics](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request).

## Điều kiện gỡ blocker

Không đổi verdict sang `ready_for_rereview` và không mở lại writer cho tới khi có đủ bằng chứng:

1. Mọi branch/worktree được tiếp tục đã rebase lên tip chứa commit EOL.
2. Mọi mục `close` có owner xác nhận và đã được đóng/prune an toàn; không mất dirty hoặc unique commit.
3. Ba worktrees dirty đã được owner xử lý và kiểm tra lại.
4. Các mục `owner=unknown` đã có owner hoặc có quyết định human rõ ràng.
5. #52 được sửa/triển khai, hoặc packet mới cung cấp enforcement ancestry thực; gates chứng minh cơ chế hoạt động.
6. Re-run cùng inventory trên `origin/master` mới cho kết quả không còn residual writer trái chính sách.

Cho tới lúc đó, giữ #63, #49 và #48 mở; không tuyên bố F2-D hoàn tất vận hành.
