# WP835 r1/g1 — Lease no-progress threshold 360 minutes

## Authority and exact source

Owner requested six-hour inactivity on 2026-10-19 in the WP748 coordination chat; durable preparatory authority is https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6253065468 and draft Issue https://github.com/ducthangho/tra-luat/issues/835. This spec remains proposed until the owner posts the exact Issue #835 authority comment bound to this spec hash and the missing-policy exception below. No Executor lease exists yet.

Remote master acceptance base: `6842a625f457843a21bd3a3b0422f13cb13de911` (remeasure before lease). Proposed patch `proposal-6842.diff` has SHA256 `c4ffe1ebf16d0b025f2727f9e167b0d4640c4e00ca6e5c1a529386295bf66096`, generated from raw remote protocol blob `806df3daa5514acaf37a5be83e9641022effd90e`; protocol old bytes SHA256 `805216bc03de651c0ad91b6256ee2a50b8858b4634176929c5da278eb9512201`. New ADR path does not exist at this base.

## Objective and write set

Change only the inactivity revocation threshold for future leases from 30 to 360 minutes. Keep absolute `lease_until`, generation fencing, bilateral tombstones, exact-head invalidation, review SLA, and the 15-minute post-`changes_requested` heartbeat. Existing leases, including WP748 g19, remain byte-identical and retain their stamped threshold. Applying 360 minutes to WP748 requires a separately authorized successor lease after governance activation.

Executor: Claude Code Opus 5.5, local Windows, branch `agent/wp835-g1-claude` in a fresh isolated clone. Reviewer: fresh independent Codex, exact-head read-only. Sensitive review class. Exact effective write set, subject to the owner-approved temporary manual closure exception below:

1. `docs/PROTOCOL_DA_PHIEN.md`
2. `docs/adr/0055-lease-no-progress-six-hours.md`

The Dispatcher may publish this spec and a lease YAML on an ops ref after authority/preflight; these coordination files are not Executor write-set paths. No writes to WP748 product, old leases, ADR-0017 history, workflow, controller, credentials, LIVE, merge or land.

## Missing canonical policy exception — explicit checkpoint

The protocol and ADR-0032 name `.github/coordination/change-impact.v1.json`, but the file is absent from remote master at the base. Do not silently pretend a policy hash or a computed closure exists. The owner must explicitly authorize, on Issue #835, a one-packet temporary manual closure for the two exact documentation paths and the read-only required checks below, or authorize a broader successor Packet to implement the policy first. If neither authorization is present, no lease is granted. Recheck if the file appears before lease: if so, compute closure from it and stop on a mismatch.

## Acceptance and gates

- Apply the patch on the exact clean base only after lease; preserve LF Git bytes and check `git diff --check`.
- Protocol §4 says 6 hours (360 minutes); ambiguous/missing review_sla fallback uses the same 6 hours. Add new-lease example `heartbeat_required_minutes: 360`.
- ADR-0055 supersedes only the 30-minute statement of ADR-0017, and §20 has one ADR-0055 row and a truthful ADR-0017 note. `python .claude/dev/packet_loop.py adr-song --root <isolated clone>` must return rc0 with positive count.
- Prove `lease_until`, 15-minute post-verdict heartbeat and already issued YAML bytes are unchanged. `rg`/source scan and owner review identify any active external controller with a 30-minute constant; if the controller cannot be synchronized or verified, do not claim operational activation or issue 360-minute leases.
- Independent Codex review on exact head returns zero unresolved P1/P2. Run applicable docs/protocol tests and exact-head CI after the single permitted push. No push until local gates and review are ready; no merge/land without separate authority.

## Stop conditions

Stop on changed base, expired/overlapping lease, missing owner exception, nonempty effective closure outside these paths, active conflicting controller, changed head after review, write outside write set, or missing positive gate evidence. Report `not_run` and `inconclusive` literally.
