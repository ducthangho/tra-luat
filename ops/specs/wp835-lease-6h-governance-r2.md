# WP835 r2/g2 — six-hour no-progress governance, disjoint master drift

## Authority and exact source

Draft until owner posts a new exact comment on Issue #835. Supersedes r1/g1 only after bilateral tombstone and new lease publication. Acceptance base is remote `master` `062292b2c75be8c316a0cf7347290574efa10861`. The protocol blob at this base is `806df3daa5514acaf37a5be83e9641022effd90e`, identical to g1's base protocol blob. ADR-0055 and `.github/coordination/change-impact.v1.json` are absent at this base. Recheck all facts before lease.

Source patch is the frozen Executor g1 diff in `wp835-g1-executor.diff`, SHA256 `361dbe5fc6d621a352603d28eba94fe39030e85081ac2ed4c2a082aa831ecffd`, from commit `0e9a4f09fdd903e97e0d0730415bdc685f53fce1`, tree `929b163a82341900cff26611e75533239902c8f4`. Independent Codex read-only review of that head found no P1/P2 but stopped approval because master advanced under r1 stop condition. Do not label it approved.

## Objective, roles, write set

Apply exactly the frozen two-file patch to a fresh clean clone at the acceptance base. Executor Claude Code Opus 5.5, local Windows, branch `agent/wp835-g2-claude`; Reviewer fresh independent Codex session, read-only on exact new head; sensitive review class. Exact effective Executor write set:

1. `docs/PROTOCOL_DA_PHIEN.md`
2. `docs/adr/0055-lease-no-progress-six-hours.md`

Use the owner-approved temporary manual closure for these paths because canonical `.github/coordination/change-impact.v1.json` is absent. No other product path or old lease may change. Dispatcher may only publish spec/lease/tombstone coordination files on an ops ref.

## Base movement after lease

Before granting g2 lease, remote master MUST equal the exact acceptance base above; on any difference, stop and renew authority. Once the g2 lease is published and Executor has started from that exact base, later master commits outside the two-file write set do not by themselves stale the Executor head. Before review, PR push, or integration, remeasure remote master and confirm both write-set path blob OIDs still equal the acceptance-base blobs and canonical change-impact policy remains absent. If either path or policy changes, or merge conflicts occur, stop for a new revision/generation. The Executor does not silently rebase or change its head after review. Exact-head CI and review bind the candidate head, not master.

## Acceptance and narrow gates

- Protocol §4 no-progress revocation and ambiguous/missing `review_sla` fallback: 6 hours (360 minutes) for newly issued leases only. `heartbeat_required_minutes: 360` appears in the future-lease example; existing YAML and `lease_until` remain unchanged.
- ADR-0055 supersedes only ADR-0017's 30-minute sentence; §20 rows and disk ADR set match 1:1; no claim of operational activation before external controller verification.
- On new head run `git diff --check`, `python .claude/dev/packet_loop.py adr-song --root .`, and focused phrase/unchanged-rule checks. Credit prior WP748 product CI only as historical context; do not rerun Windows suites. After one product push, required exact-head CI must still pass because the candidate SHA is new.
- Independent exact-head Codex review: zero unresolved P1/P2. Do not push until local gates and review are ready. Do not merge, land, LIVE, use credentials, or declare 360-minute leases operational without separate authorization and controller verification.

## Stop conditions

Changed base before lease, changed write-set blobs or policy after lease, stale/overlapping lease, patch mismatch, write outside write set, changed head after review/CI, required check lacking positive evidence, or controller still enforcing 30 minutes at activation.