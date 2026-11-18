# Packet1308 r5/g8 — Desktop canary evidence checkpoint

Mission62; genuine draft PR #1385; immutable baseline 641108cb997872b0ef2a277ea9c8faf8b82532bb.
This candidate records the executed g8 adoption (pending recovery of g7 approved_pending), lease rebind and attempt reservation. It does not claim review, human audit, H CI, connector completion or final acceptance.

## History carried into g8

g7 (Mission60/61) ended approved_pending at state revision 12 (sha 0f569cd4) with H 226bba5 offline-approved, owner-audited, CI-green and connector-clean, but canonical accept could not run because the Events-API publication collector could not produce evidence; its allowance ended 2026-11-17T12:36:00Z. #1370 replaced the collector with the Repository Activity API (merged 641108c). All g7 counters (attempts 3, review rounds 3, Codex calls 3), findings and failures are preserved. Closure: https://github.com/ducthangho/tra-luat/issues/1308#issuecomment-6969216821 .

## Executed checks

| Check | Actual outcome | State revision / witness revision |
|---|---|---|
| adopt-state g7 -> g8 (initial; pending recovery of approved_pending) | rc0 completed_no_dispatch; approved_pending projected into g8 | 2 / 39 |
| record-lease rebind -> wp1308-r5-g8-codex | rc0 completed_no_dispatch; state leased, stale pending fields dropped | 3 / 40 |
| begin-attempt (fresh doctor --json, no missing required tools) | rc0 reserved_for_dispatch=true; running; attempts 4/4; reviews 3/4; offline Codex calls 3/4 | 4 / 41 |

Every command used the stock canonical launcher (`--require-clean`, `--expected-head 641108c`, 20-minute deadline) and the packet_loop scoped entrypoint with expected revisions, fresh authority resolves and actual paired state/witness high_water readback. No hand-written state/witness/HMAC, serialized proof reuse or counter reset. No limit was raised. The doctor image for begin-attempt was taken through agent-creds-exec with an owner-provisioned key file that was deleted immediately after doctor.

## Evidence integrity

Raw operational logs and private lineage stay outside this candidate. These SHA256 values identify actual private receipts; they do not independently grant authority or prove a future gate.

- adopt-state: finished 2026-11-18T04:56:57.184147+00:00; receipt SHA256 410ac45a489d30467d6ef9b4e3cd923a3ccc28bd39ed152211f5edc3e0181f8e.
- record-lease: finished 2026-11-18T05:01:16.564742+00:00; receipt SHA256 f50eef86820e7d3e14598121e39f8905592ffd52846efeb81f2a7c29886e83a5.
- begin-attempt: finished 2026-11-18T05:12:50.686422+00:00; receipt SHA256 50ea1c850a2b365d7bccb3018c827b2dd91998aeddb58fa74108048301df8747; doctor image SHA256 f37dc0e0ebdb7165364fb377ca6b0fb873d6e3318e1a62e11f8059b65659ee4a.

Observed running state SHA256 b560cc97dfb52387dca76a583133eae586519f956b1f7f510b3b29a7f8cb3090; witness SHA256 e97f4de2cbddb75148bce220ae0479cb23991d4f0216c96f4bc54cb5f53e8b45; witness high_water matches generation8/state_revision4/state digest.

## Authority, limits and remaining gates

Owner decision r62 https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6969055884; Installed62 https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6969082747; Packet grant https://github.com/ducthangho/tra-luat/issues/1308#issuecomment-6969236813. Boot 2f7fa68a held by a keeper process; root/device/inode/mount/magic/seed fingerprint unchanged; same enrollment id/binding kept for canonical adoption.
Frozen allowance 2026-11-18T04:45:00Z to 2026-11-18T10:45:00Z, bounded by MCR-1172-C1 2026-11-24T18:53:00Z; earliest deadline governs. No pause/reset/automatic extension or successor.
Remaining in g8 after this reservation: no further attempt, one review round and one offline Codex call, plus one genuine exact-H connector. The offline review of this H is scoped to the packet's five-path diff. No WP1179 cleanup, source/Windows/fullM9/LIVE/security/account/ACL edits or paid credit purchase.
Independent review, actual-human exact-H/tree/spec/generation/PR audit by the owner, controlled H publication, applicable exact-H Ubuntu CI, genuine exact-H connector completion and positive canonical accept (publication evidence from the Repository Activity collector) with readback remain mandatory. H must remain local until the actual-human audit; P results never substitute for H evidence.
This five-path metadata/canary diff does not change product, CI or protocol. No PR0-PR8 dispatch or Mission completion is authorized by this checkpoint.
