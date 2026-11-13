# WP1309 r1/g1 — bounded canonical snapshot timeout480
packet_id: wp1309
packet_issue: 1309
revision: 1
generation: 1
immutable_acceptance_baseline: 6f32aad6fe9db93867fc87456541740f80bf79a4
executor: codex
executor_surface: codex_cli
executor_requested_effort: high
review_class: sensitive
assurance_target: cross_approved
authority_url: https://github.com/ducthangho/tra-luat/issues/1309#issuecomment-6822313718
hard_expiry_utc: 2026-11-13T05:01:05Z

## Assignment
Owner directly instructed timeout480seconds and normal land, with standing delegation for routine leases/caps/bookkeeping. Dispatcher administers this finite new correction envelope, not a reuse/reset of closed1174/1303 or expired1308. No new paid purchase/credential/account/profile/LIVE/security grant. Stale1288 retired under ADR0056; candidatebc620/PR1310 preserved. Ownership before source lease measured0.

## Product write set and delta
Only `.claude/dev/packet_loop.py`: in `_1174_git_snapshot`, change subprocess.run full upstream clone timeout120 to480seconds. Exactly one line added/one removed. Keep endpoint allowlist, full clone flags, Git env filtering, canonical rollout check, fullrefs/DAG and immutable admission/spec/lease guards. No API/collector/launcher timeout changes, no tests or unrelated source edits, no fixture/mirror/shallow/cache workaround. If another edit is necessary, stop with evidence instead of expanding scope.

## Roles, envelope and history
One fresh CodexCLI Executor requested high, maximum30minutes. One fresh independent Codex review requested xhigh, read-only/advisory, maximum30minutes; one actual native ClaudeCode Opus/max read-only formal review of public source/diff/normative/authority payload, maximum30minutes. Existing accounts only, no authentication changes. Record actual provider/surface/serving identity honestly; do not manufacture human audit or transfer old-head approvals. If any call fails, preserve cost and stop; no implicit extra call. New correction cap: author1, Codexadvisory1, Claudeformal1, sourcepush1, no Windows/M9 dispatch; automatic required LinuxCI remains. Four-hour absolute operational window includes waits; old costs/failures/unknowns preserved separately and not refunded. This is a scoped operational allowance under standing owner routine-cap delegation, not a new Mission target grant.

## Validation and review
Read AGENTS/CONTEXT/protocol/CLAUDE/provider rules and relevant working method. Verify lease/spec ref/path/hash/current head/ownership before sourcewrite and review. Run through pinned trusted launcher with secret-free project children. Small patch: syntax and exact diff, focused canonical affected tests/error-path validation, required CI and actual review/gates. Do not add tests merely asserting a literal. Each new finding file:line and pattern; scan analogous sites but do not bulk-change other deadlines. First review this exact diff and direct dependencies, later delta-only with no duplicate findings. Reassess after3unfinished rounds within the stricter finite budget.

## Publication/land
No source publication until prepublication requirements for this sensitive Packet pass. No WindowsCI/fullWindowsmutantCI; no full M9 new dispatch in this operational envelope. If applicable canonical land gate requires additional run/assurance not available here, checkpoint, never relabel UNKNOWN/skipped as pass or waive it. Normal expected-H merge, actual postmerge checks/readback/bookkeeping and lease closure only after current exact-H authority/gates. Root is Dispatcher/Land Operator, not source Reviewer.

## Target
No target init/canary from this lease. Target1308 sole Dispatcher stays unchanged. After source land, its admission/spec/Mission registration/lease must be reconciled to newcanonical H and fresh runtime; oldwindow expired. Actual-human target outcome acceptance remains separate. No PR0–PR8 dispatch from this correction.
