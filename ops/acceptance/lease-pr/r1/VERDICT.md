# LEASE-KIEM-NGHIEM-MOI-DUONG r1 — review độc lập Codex offline (2/2 lời gọi): approve

**Căn cứ:** đặc tả `ops/specs/lease-pr-r1.md` §4, lease `ops/leases/lease-pr-r1-g1-claude.yaml` (`review_calls_limit: 2`), Issue #1445.

## Các lượt
| lượt | run (`launcher.py run`) | head review | kết luận | sandbox | model phục vụ |
|---|---|---|---|---|---|
| 1 | `f5763a4a`, 09:44:28Z → 09:46:54Z, `ma_thoat` 0 | `529f8b53f23f714c715e70a1a9953c99976f490a` | **request_changes**: 2 P2, 1 P3 | `DO_DUOC` | `gpt-6-astra` (`DO_DUOC`) |
| 2 | `c795bbcc`, 09:48:48Z → 09:50:33Z, `ma_thoat` 0 | `33874ad797bd88c71a7103ca852018a159750d05` (delta) | **approve**: 0 P0–P2, 1 P3 (3 đột biến sống) | `DO_DUOC` | `gpt-6-astra` (`DO_DUOC`) |

Lệnh, cả hai lượt: `python3 .claude/dev/launcher.py run --workspace <clone tại head> --expected-repo ducthangho/tra-luat
--expected-root-commit e13f74bb… --expected-head <head> --prompt-file <p> --expected-prompt-sha256 <sha> -- /opt/node22/bin/codex exec
-m gpt-6-astra --sandbox workspace-write --skip-git-repo-check -C <thư mục review> "…{PROMPT_FILE}…"`. `effort` không ghi (null).

## Xử lý finding
| finding | xử lý | bằng chứng |
|---|---|---|
| L1 F1 P2: selftest thừa kế `GITHUB_ACTOR`, PR của người ngoài danh sách đỏ dù không đụng lease | cô lập `GITHUB_ACTOR` trong ca cây thật; thêm `ca_actor_la` | `33874ad`; lượt 2 tái hiện với `GITHUB_ACTOR=outside-contributor` ⇒ rc 0 |
| L1 F2 P2: symlink treo ở đường dẫn lease bị coi như đã xoá ⇒ xanh | wrapper: `lexists` sai ⇒ xoá; symlink/thư mục/mục lạ ⇒ LỖI; thêm `ca_muc_khong_phai_tep_thuong` + đột biến `symlink_coi_la_xoa` | `33874ad`; lượt 2 tái hiện ba dạng ⇒ rc 1 |
| L1 F3 P3: `if: false` lọt khoá cấu trúc | cấm SỰ CÓ MẶT của khoá `if`/`continue-on-error` ở job và MỌI bước; đột biến `if_false_buoc_kiem`, `coe_selftest` | `33874ad`; lượt 2 xác nhận |
| L1 đột biến sống (lọc hai gạch, `.yml`, …) | ca `.yml` + thư mục con; đột biến `loc_hai_gach` | `33874ad`; lượt 2 đo: đã giết |
| L2 P3: 3 đột biến sống (tiền tố `ops/leases` thiếu `/`; `paths:` lọc trigger; CLI luôn thoát 0) | ca `ops/leases-extra/a.yaml` không là lease; khoá `pull_request` không bộ lọc; `ca_cli_that` chạy đúng điểm vào CLI; 3 đột biến tương ứng | commit sau `33874ad` (chỉ đổi `ops/kiem_lease_pr_test.py`): **11/11 ca, 11/11 đột biến giết đúng ca**, cả với `GITHUB_ACTOR=outside-contributor`. Phần đổi này chỉ là test, không qua lời gọi review thứ ba (trần 2); connector Codex review head cuối. |

## Đính chính đặc tả (không sửa tệp đóng băng)
§2 của `ops/specs/lease-pr-r1.md` ghi chốt `GITHUB_ACTOR` áp cho lease **còn hạn**. Đúng ra nó áp cho **cả lease hết hạn**:
`kiem(bo_qua_han=True)` vẫn kiểm thẩm quyền (`ops/lease_publish.py` dòng ~1086). Hai lượt review cùng chỉ ra. Ca `ca_actor_la` khoá hành vi này:
actor lạ sửa lease đã hết hạn ⇒ `CHAN [4]`.

## Giới hạn còn lại (đã nêu, không chặn)
- Check `kiem-lease-pr` chưa chặn merge cho tới khi chủ kho thêm nó vào ruleset.
- Đuôi viết hoa (`.YAML`) nằm ngoài vị từ, nhất quán với `ci_duong_nhanh.kiem_lease` và bộ quét bia mộ.
- Hệ thống tệp không phân biệt hoa thường và Windows: chưa chạy. Workflow chỉ chạy trên Ubuntu.

## Chạy thật trên GitHub
Run `44713185482` (head `529f8b5`): job `kiem-lease-pr` success. Selftest `TONG: DAT`; bước kiểm in
`KIEM_LEASE_PR: DAT (1 lease doi trong 6 tep doi, 0 loi)`, tức lease của chính PR này đã được kiểm.

## VERDICT lượt 1 (nguyên văn, sha256 `eb840e34ec169ec5…`)
Review: packet #1445 r1/g1, sensitive; read-only, offline.

Reviewed SHA: `529f8b53f23f714c715e70a1a9953c99976f490a`; base: `00ee83998487d289324566f230b67b5923a9a9d9`.
Tree: `e229a6f02285c2e48287cd5ff4c03f56f4a1c0d1`.
Identity: OpenAI Codex, machine transport; exact model id: `KHONG_do_duoc`.

| Check | Result and evidence |
|---|---|
| Frozen scope | Spec SHA-256 matches lease: `d78198f6ee899c14fa372c87381b77c08654d9e127d4cc3425a28d2946bdc5b2`. All six changed files belong to `ops/leases/lease-pr-r1-g1-claude.yaml:23` write_set. |
| Diff fail-closed | `ops/kiem_lease_pr.py:46` rejects `None`. `ops/ci_duong_nhanh.py:166` unions three-dot, merge-tree and actual merge-ref differences; rejects bad SHAs, git failures, ambiguous merge bases and malformed output. Empty sets succeed intentionally. No file-count cap; large output is captured, resource exhaustion cannot yield an ordinary successful completion. |
| Path coverage | `ops/ci_duong_nhanh.py:700` includes nested lowercase `.yaml`/`.yml`; matching is case-sensitive, consistent with tombstone scanning (`ops/lease_publish.py:757`). Uppercase extensions escape checking. `--no-renames` preserves source/destination coverage. Delete/re-add is checked if final content differs; identical restoration has no net change. Symlink gap: F2. |
| Workflow | `.github/workflows/lease-pr.yml:9` uses default PR activities: opened, synchronize, reopened; labeled/edited do not trigger it. Default checkout tests the merge commit, matching `_MERGE` at line 36. No identified stale-activity trigger. Env interpolation contains SHAs/event name, not executable shell text. Read-only token, hosted runner and ordinary pull_request avoid privileged fork execution; this is not a tamper-proof gate against PR edits to its own code. |
| Tombstones | Checkout depth 0 (`.github/workflows/lease-pr.yml:23`) conventionally fetches all origin branches, matching `gate-ops` (`.github/workflows/ci.yml:716`). Thus another origin branch is not inherently invisible to `ops/lease_publish.py:544`. Fork-only branches are not all fetched. Live ref availability was not measured offline; no evidence of universal tombstone failure. |
| Behaviour | Lease validation is shared, but the whole job is not equivalent to `kiem-re`, which also checks modes, YAML and other evidence (`ops/ci_duong_nhanh.py:781`). Expired leases intentionally bypass expiry only. Actor enforcement applies to expired leases too (`ops/lease_publish.py:1086`), so spec §2 is incomplete. No-lease PR regression: F1. |
| Tests/registry | `python3 -B ops/kiem_lease_pr_test.py`: rc 0, 8/8 cases, 4/4 required mutants killed. Direct registry `kiem()` returned `([], 30, 30)`; registration at `.claude/dev/ci_dang_ky_test.py:84` matches workflow run-line discovery at line 685. Actionlint, t24 and live Actions: not_run. |

Findings:

- **F1 — P2: selftest rejects unrelated contributors’ PRs.** `.github/workflows/lease-pr.yml:29` always runs `ops/kiem_lease_pr_test.py:103`, whose real expired “good” fixture inherits `GITHUB_ACTOR`. `kiem(bo_qua_han=True)` still checks actor authority. Reproduction: `GITHUB_ACTOR=outside-contributor python3 -B ops/kiem_lease_pr_test.py` returned rc 1, 7/8 cases, `CHAN [4]`. A README-only PR from that actor therefore fails before its actual diff is inspected. Isolate actor environment for fixture subprocesses and add an unapproved-actor/no-lease workflow regression; preserve production authority checks. Correct the expired-lease consequence in `ops/specs/lease-pr-r1.md:37`.

- **F2 — P2: added dangling symlink passes as deletion.** `ops/kiem_lease_pr.py:54` delegates without a file-mode guard; `ops/ci_duong_nhanh.py:702` skips anything failing `is_file()`. Scratch reproduction with changed `ops/leases/broken.yaml -> missing` returned rc 0 and `DAT (1 lease doi ... 0 loi)`. The added entry cannot undergo strict YAML validation, yet receives green. Directory-target symlinks likewise skip; regular-target symlinks follow the target. Distinguish actual deletions from present nonregular entries, preferably using Git modes, and add regression cases. This guard can live in the new wrapper without modifying leased files.

- **F3 — P3: structural test accepts a disabled validation step.** `ops/kiem_lease_pr_test.py:159` uses truthiness: YAML `if: false` becomes Python `False`, satisfying `not cuoi.get("if")`. A measured single-line insertion on the final step survived every case while disabling validation. Reject presence of `if`, or validate its semantics explicitly.

Additional measured surviving mutants: drop `.yml` from logging predicate (`ops/kiem_lease_pr.py:38`); change that prefix to `ops/leases`; filter validation input to paths with exactly two slashes (line 54); add selftest-step `continue-on-error: true`. Dropping `.yml` from actual validation, swapping SHA env values, final-step `continue-on-error: true`, and removing selftest were killed.

Fixture premises (`ops/kiem_lease_pr_test.py:88`) check expiry and reviewed-SHA presence, not full validity or environment independence; missing files raise instead of reporting `fixture vo hieu`. `diff_gia` restores its shared module function in `finally` (line 51); no inter-case/mutant leakage found.

KET_LUAN: request_changes

## VERDICT lượt 2 (nguyên văn, sha256 `c8d02d96809f9d0d…`)
Review: packet #1445 r1, call 2 (delta), read-only/offline.
Reviewed HEAD: `33874ad797bd88c71a7103ca852018a159750d05`.
Previous review: `529f8b53f23f714c715e70a1a9953c99976f490a`.
Exact model id: `KHONG_do_duoc`.

| Check | Result and evidence |
|---|---|
| F1 closed | Normal and `GITHUB_ACTOR=outside-contributor python3 -B ops/kiem_lease_pr_test.py` both exit 0: 10/10 cases, 8/8 built-in mutants killed. Fixture actor isolation/restoration is at `ops/kiem_lease_pr_test.py:63,113,121`; line 126 separately verifies outside-actor/no-lease succeeds and outside-actor/expired-lease fails. |
| F2 closed | Independent scratch reproductions: dangling `.yaml` symlink, regular-file `.yml` symlink, and directory at a lease path each return 1 with `khong phai tep thuong`; absent/deleted lease returns 0. Even a successful fake validator cannot override the guard (`ops/kiem_lease_pr.py:57–63`). Tests cover these entries at `ops/kiem_lease_pr_test.py:139`. |
| F3 closed | Inserting final-step `if: false` now fails the structural case. Presence checks cover every step, including selftest (`ops/kiem_lease_pr_test.py:213–215`), and the job (`:205`). |
| Previous surviving mutants | Measured against all ten cases: dropping `.yml` from `la_lease` is killed; filtering validation to exactly two slashes is killed; selftest `continue-on-error: true` is killed. Loosening the prefix still survives; see P3 below. Built-in mutation results also confirm nested-path and disabled-step coverage (`ops/kiem_lease_pr_test.py:232–238`). |
| Scope/freeze | Delta changes only `ops/kiem_lease_pr.py` and its test, both within `ops/leases/lease-pr-r1-g1-claude.yaml:23` write_set. All six files in `HEAD~3..HEAD` are authorized. Frozen spec SHA-256 remains `d78198f6ee899c14fa372c87381b77c08654d9e127d4cc3425a28d2946bdc5b2`. |
| Regressions/coverage | Good expired lease, absent deletion, no-lease PR and nested/current-lease dispatch pass. Current-lease subprocess outcomes are mocked; expired fixtures run real validation. Production actor enforcement remains intact. No additional validation bypass found for present regular lowercase `.yaml`/`.yml` entries on the configured Ubuntu runner (`.github/workflows/lease-pr.yml:17`). Uppercase extensions remain outside the existing case-sensitive predicate (`ops/kiem_lease_pr.py:38`; `ops/ci_duong_nhanh.py:700`). |

Open findings: **P3 — mutation coverage gaps**, no open P0/P1/P2. All ten cases accept these measured single-line mutants:

- `ops/kiem_lease_pr.py:38`: change prefix `ops/leases/` to `ops/leases`. An unrelated `ops/leases-extra/a.yaml` is then counted/guarded as a lease; add a negative-prefix case.
- `.github/workflows/lease-pr.yml:10`: replace `pull_request:` with `pull_request: {paths: ["ops/leases/**"]}`. The gate stops running on every PR; the test checks event keys but not trigger contents (`ops/kiem_lease_pr_test.py:199`).
- `ops/kiem_lease_pr.py:72`: replace `raise SystemExit(chay())` with `raise SystemExit(0)`. CLI validation disappears; imported-function cases never exercise the entrypoint.

Platform limits: Windows and case-insensitive filesystems were not executed. `lexists` follows filesystem case semantics; a case-only rename can resolve the old path to the new entry rather than register deletion. No supported-Ubuntu regression identified. Windows selftests may require symlink privileges (`ops/kiem_lease_pr_test.py:147–148`); the workflow explicitly targets Ubuntu.

Spec clarification: frozen §2 (`ops/specs/lease-pr-r1.md:37`) is incomplete: actor authority also applies to expired leases (`ops/lease_publish.py:1086`). The new test documents this at `ops/kiem_lease_pr_test.py:127–128`; the spec was not edited.

For unchanged portions of `HEAD~3..HEAD`, I rely on call 1’s diff, workflow-security, tombstone and registry review. Together with this delta review, no open P0/P1/P2 remains. Actionlint, t24 and live Actions were not rerun offline.

KET_LUAN: approve
