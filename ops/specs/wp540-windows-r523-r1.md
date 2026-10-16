# WP540 WINDOWS-R523-CROSS-DRIVE — revision1 / generation1

Authority: https://github.com/ducthangho/tra-luat/issues/540#issuecomment-5675140912
Owner ducthangho; recorder codex_desktop, not dispatcher. User expressly granted a separate r523 repair packet and sufficient authority. Related blocker #538; independent from proposed optimization packet #466. No inherited WP523/WP473 debt closed.

## Identity and anchors
- Canonical base / immutable acceptance baseline / initial start: 19de56693d06813e6743a30113d0fb87bff3e196.
- Base tree: 89f21ef96592e97b45ccbd33648ed93bf2b3a7ff.
- Branch codex/wp540-r1-g1, exclusive; target master.
- Executor openai_codex / codex_cli / machine, gpt-6-astra/high, Windows local / PowerShell.
- Reviewer same model/provider at xhigh; fresh session/context/real-remote checkout, read-only source, scratch outside source. No executor context fork. Verify actual runtime identity and rc. Owner same-provider exception; manual journal, no packet_loop state fabrication.
- Review class sensitive conservatively; computed dispatcher closure unavailable, #473 remains disclosed debt.

## Objective and exact effective write set
Repair Windows r523 fixture setup when cwd and the supplied/default temp root are on different drives. The test must still exercise valid relative input against the real chay_mot_mutant path handling and compare it with absolute input. Do not substitute absolute paths for relative input or suppress the test/error.

Product: `ops/nhanh_don_duoc_test.py` only, scoped to r523 fixture and directly necessary regression/assertions in the same file.
Coordination: `ops/specs/wp540-windows-r523-r1.md`, `ops/leases/wp540-r1-g1-codex-windows.yaml`, `ops/reviews/wp540/` only.
No changes to runtime implementation, workflow, other tests, manifest, golden, CHANGELOG, credential/hooks or WP538 seven product files. Preserve concurrent work. Scratch/code probes live outside source. Canonical master drift must be classified; no stale review reuse for a changed candidate.

## Acceptance and negative controls
A1. Reproduce actual baseline r523 ValueError with cwd on D: and supplied temp on C:, and baseline success on same drive. Record commands, true rc, complete diagnostics and exact file hash.
A2. Fixed r523 passes both same-drive and cross-drive native Windows arrangements. Observe that the argument under the relative branch is actually relative, and resolves to the same real fixture as absolute input. Do not catch-and-ignore ValueError or skip Windows.
A3. Process cwd before/after is identical, including failure paths; temporary fixture is cleaned. Use scoped temporary context on a suitable drive if needed; do not mutate global cwd/temp policy or persist test files in checkout.
A4. Demonstrate failure of semantic mutations: removing relative path normalization from the tested child launcher still makes the test red; converting the fixture to absolute-only must be rejected by a meaningful assertion/probe. Negative controls are executed in external copies, not source edits. No unrelated mutant counts invented.
A5. Run relevant native full nhanh_don_duoc suite with selfchecks/mutants actually enabled; verify counts and positive execution, not rc alone. Targeted Linux r523 plus appropriate syntax checks; no repeated broad all-repo/full-CI until ready. Distinguish skipped/not_run/not_measured.
A6. Independent exact-SHA review covers Standards/Spec and class root cause, no P1/P2 (or approve), separate runtime identity and source-preservation evidence. Record body/hash readback on publication.
A7. Before PR/CI: canonical admission at current S/H/T, dependency/event/ruleset check. Windows+Ubuntu required gates on final candidate/integration checkout; final canonical post-merge gates and bookkeeping before landed. Existing unrelated failure is not waived; report it.

## History, authority and limits
Class r523-cross-drive-fixture has one measured baseline report from WP538 comment5673358418, zero previous repair/review attempts as of grant. WP538 review6 already approved defe7a819f716f9632b9b5f28a139b53eb3eedfb; do not modify or relabel that verdict. #466 optimization/review history remains separate.
Owner granted commit/push/PR and land outcome; executor does not self-review or self-approve. Coordinator records exact candidate conditional land authority before merge, then may act Land Operator. No admin bypass or ruleset mutation. No Windows waiver.
Executor lease24h; runs90min maximum; heartbeat30min; review SLA2h. Class-based owner-directed loop until no P1/P2 or approve; retain failure history and reconsider design at repeated shape. CI runs only after admission/review readiness, use PR event and no redundant dispatch; required post-merge CI allowed. Land authority separate from executor lease, bounded24h at exact-candidate record. No deploy/LIVE/secrets. Final synchronize approved skill changes without overwriting concurrent edits.
