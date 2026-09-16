# WP540 WINDOWS-R523-CROSS-DRIVE — revision2 / generation2

Authority (r2): https://github.com/ducthangho/tra-luat/issues/540#issuecomment-5694699451
Authority (r1, still the source for everything r2 does not change): https://github.com/ducthangho/tra-luat/issues/540#issuecomment-5675140912
Owner ducthangho; recorder for r1 codex_desktop, for r2 a claude session, neither a dispatcher. User expressly granted a separate r523 repair packet and sufficient authority. Related blocker #538; independent from proposed optimization packet #466. No inherited WP523/WP473 debt closed.

## Identity and anchors
- Canonical base / immutable acceptance baseline / initial start: 19de56693d06813e6743a30113d0fb87bff3e196.
- Base tree: 89f21ef96592e97b45ccbd33648ed93bf2b3a7ff.
- Branch codex/wp540-r1-g1, exclusive; target master.
- Executor openai_codex / codex_cli / machine, gpt-6-astra/high, Windows local / PowerShell.
- Reviewer **anthropic_claude / claude_code / machine-local — CHANGED AT r2**, fresh session/context/real-remote checkout, read-only source, scratch outside source. No executor context fork. Verify actual runtime identity and rc. The r1 condition "same model, xhigh > high" NO LONGER APPLIES: that was a raise in EFFORT, and r2 makes it a change of PROVIDER. The owner same-provider exception is not withdrawn and the r1 reviewer plan is not called wrong; it is simply no longer the target. Manual journal, no packet_loop state fabrication.
- Review class sensitive conservatively; computed dispatcher closure unavailable, #473 remains disclosed debt.

## Objective and exact effective write set
Repair Windows r523 fixture setup when cwd and the supplied/default temp root are on different drives. The test must still exercise valid relative input against the real chay_mot_mutant path handling and compare it with absolute input. Do not substitute absolute paths for relative input or suppress the test/error.

Product: `ops/nhanh_don_duoc_test.py` only, scoped to r523 fixture and directly necessary regression/assertions in the same file.
Coordination: `ops/specs/wp540-windows-r523-r1.md`, `ops/leases/wp540-r1-g1-codex-windows.yaml`, `ops/specs/wp540-windows-r523-r2.md`, `ops/leases/wp540-r2-g2-claude-review.yaml`, `ops/reviews/wp540/` only. The r1 spec and the g1 lease STAY ON DISK as the record; r2 supersedes them, it does not delete them.
No changes to runtime implementation, workflow, other tests, manifest, golden, CHANGELOG, credential/hooks or WP538 seven product files. Preserve concurrent work. Scratch/code probes live outside source. Canonical master drift must be classified; no stale review reuse for a changed candidate.

## Acceptance and negative controls
A1. Reproduce actual baseline r523 ValueError with cwd on D: and supplied temp on C:, and baseline success on same drive. Record commands, true rc, complete diagnostics and exact file hash.
A2. Fixed r523 passes both same-drive and cross-drive native Windows arrangements. Observe that the argument under the relative branch is actually relative, and resolves to the same real fixture as absolute input. Do not catch-and-ignore ValueError or skip Windows.
A3. Process cwd before/after is identical, including failure paths; temporary fixture is cleaned. Use scoped temporary context on a suitable drive if needed; do not mutate global cwd/temp policy or persist test files in checkout.
A4. Demonstrate failure of semantic mutations: removing relative path normalization from the tested child launcher still makes the test red; converting the fixture to absolute-only must be rejected by a meaningful assertion/probe. Negative controls are executed in external copies, not source edits. No unrelated mutant counts invented.
A5. Run relevant native full nhanh_don_duoc suite with selfchecks/mutants actually enabled; verify counts and positive execution, not rc alone. Targeted Linux r523 plus appropriate syntax checks; no repeated broad all-repo/full-CI until ready. Distinguish skipped/not_run/not_measured.
A6. Independent exact-SHA review covers Standards/Spec and class root cause, no P1/P2 (or approve), separate runtime identity and source-preservation evidence. Record body/hash readback on publication. **CHANGED AT r2 — the assurance target is `cross_approved`, not `same_provider_approved`.** A review that is not cross-provider does not satisfy A6 at this revision, whatever its effort level. The verdict and its v2 receipt are committed under `ops/reviews/wp540/`; a GitHub comment is a mirror, not the source.
A7. Before PR/CI: canonical admission at current S/H/T, dependency/event/ruleset check. Windows+Ubuntu required gates on final candidate/integration checkout; final canonical post-merge gates and bookkeeping before landed. Existing unrelated failure is not waived; report it.

## History, authority and limits
Class r523-cross-drive-fixture has one measured baseline report from WP538 comment5673358418, zero previous repair/review attempts as of grant. WP538 review6 already approved defe7a819f716f9632b9b5f28a139b53eb3eedfb; do not modify or relabel that verdict. #466 optimization/review history remains separate.
Owner granted commit/push/PR and land outcome; executor does not self-review or self-approve. Coordinator records exact candidate conditional land authority before merge, then may act Land Operator. No admin bypass or ruleset mutation. No Windows waiver.
Executor lease24h; runs90min maximum; heartbeat30min; review SLA2h. Class-based owner-directed loop until no P1/P2 or approve; retain failure history and reconsider design at repeated shape. CI runs only after admission/review readiness, use PR event and no redundant dispatch; required post-merge CI allowed. Land authority separate from executor lease, bounded24h at exact-candidate record. No deploy/LIVE/secrets. Final synchronize approved skill changes without overwriting concurrent edits.

## WHY r2 EXISTS

`docs/PROTOCOL_DA_PHIEN.md` §3.2: changing acceptance creates a new revision and voids the old
lease. Changing `assurance_target` is changing acceptance, so this is r2 + g2 + a re-issued lease,
not an edit to g1.

The substantive reason is §8 line 580: *"`same_provider_approved` vẫn không thay `cross_approved`
cho class `sensitive`."* WP540 declares `review_class: sensitive`. The r1 plan (codex executor
reviewed by codex at xhigh, under the owner's scoped same-provider exception) is **valid** and is
**not retracted** — but by line 580 it does not substitute for `cross_approved` at this class, and
the condition that produced it (the claude side out of quota) no longer holds.

Exactly two decisions change: **who reviews** (codex -> claude) and **what assurance level is
targeted** (`same_provider_approved` -> `cross_approved`). Everything else is inherited verbatim
from r1: the executor is still **codex**, the product write set is still the single file
`ops/nhanh_don_duoc_test.py`, the baseline is still `19de56693d06813e6743a30113d0fb87bff3e196`, and
A1-A5 and A7 are unchanged. **r2 grants no new write authority.**

### One tension, stated rather than silently resolved

The g2 lease sets `manual_ci_budget: 0`, where g1 set `2`. This follows the owner's standing
instruction, quoted verbatim in the r2 authority comment: *"CI Window gặp lỗi đã biết, để đỡ tốn
tiền, không chạy CI Windows"*.

That budget governs **manually dispatched** CI — `workflow_dispatch`, a hand-called full run, a
hand-called `windows` lane. It does **not** govern the required checks that fire automatically on a
push or a PR event, and it does not govern required post-merge CI. So A7 is left **unchanged**:
its demand for Windows+Ubuntu required gates on the final candidate stands, because those are
automatic runs, not spends against the manual budget. Reading `manual_ci_budget: 0` as "A7 is
waived" would be wrong, and no waiver is granted here.

### Measured before this spec was frozen

- `git diff --numstat 19de5669..codex/wp540-r1-g1` returns **exactly two paths**, both coordination
  artifacts (`+76` lease, `+33` spec). **`ops/nhanh_don_duoc_test.py` is untouched** and no PR
  exists. So at the moment r2 is frozen there is **no candidate to review**; r2 sets the assurance
  target ahead of the work rather than after it.
- `ai-dang-giu` over `refs/heads` + `refs/remotes` (389 refs, `comm -23` empty so the ref set is not
  blind) returns **`NGƯỜI_GIỮ 0`** for all four write-set paths. The scanner was calibrated first on
  a case with a known answer (`.claude/skills/cross-review/SKILL.md` -> `NGƯỜI_GIỮ 1:
  wp538-r3-g3-claude-review`), per the repo lesson that a self-written scanner's conclusion line is
  not its measurement.
- Lease g1 expired `2026-09-16T05:17:24Z`. g2 carries the two-way tombstone (`thay_the_cho` on the
  new lease, `da_bi_thay_the` on the old) that `_kiem_bia_mo` requires in both directions.
