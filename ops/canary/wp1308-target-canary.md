# Packet1308 r5/g9 — Desktop canary evidence checkpoint

Mission65 (r64 with the Packet1308 registration row corrected); genuine draft PR #1399; immutable baseline d39313eceb71c185deca65878383a94284be3f54.
This candidate (rework H, second attempt of g9) records the executed g9 adoption (pending recovery of g8 approved_pending), lease rebind, canonical limit raises, the first attempt and its independent review, the owner erratum, and the rework attempt reservation. It does not claim approval of this H, human audit, H CI, connector completion or final acceptance.

## Erratum (owner decision)

The frozen spec `ops/specs/wp1308-target-canary-r5-g9.md` (Lifecycle) and prompt `ops/prompts/wp1308-target-canary-r5-g9.txt` (line 3) order nang-tran before record-lease. That order is wrong: canonical pending recovery (`_1315_pending_projection`) keeps the adopted projection exact until record-lease, so the only valid g9 order is adopt-state -> record-lease -> nang-tran (attempts, vong_review, codex_review_calls to 6) -> begin-attempt. Those spec/prompt bytes are pinned by spec_hash in the target state since record-lease and are kept unchanged. The owner recorded this erratum, which supersedes that sentence for g9: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6982222196 . No step ever succeeded in the wrong order; the two pre-rebind nang-tran attempts are recorded below as failures. The independent review of the first H (0563bdb3dedfae347cba90dee7772b33e84c29ff) raised exactly this as finding pending-recovery-raises-before-lease-rebind.

## History carried into g9

g8 (Mission62/63) ended approved_pending at state revision 8 (sha cea8bf86) with H 6886ebe offline-approved, owner-audited, CI-green and connector-clean, but canonical accept failed because publication receipts were compared on raw_snapshot_sha256 and cursor page counts; its allowance ended 2026-11-18T10:45:00Z. #1393 changed the comparison to the immutable receipt fields (merged d39313e). All g8 counters (attempts 4, review rounds 4, Codex calls 4), findings and failures are preserved. Closure: https://github.com/ducthangho/tra-luat/issues/1308#issuecomment-6979228525 .

## Executed checks

| Check | Actual outcome | State revision / witness revision |
|---|---|---|
| adopt-state g8 -> g9 under the first (Mission64) admission, two tries | clean UNKNOWN, no write: canonical I2 verification rc=7, then Mission registered Packet (r64 graph row still g8) | - / 45 |
| adopt-state g8 -> g9 (initial; pending recovery of approved_pending) under the reissued Mission65 admission | rc0 completed_no_dispatch; approved_pending projected into g9 | 2 / 48 |
| nang-tran attempts before record-lease, two tries | clean UNKNOWN, no write: pending recovery exact adopted projection required | 2 / 48 |
| record-lease rebind -> wp1308-r5-g9-codex | rc0 completed_no_dispatch; state leased, stale pending fields dropped | 3 / 49 |
| nang-tran attempts 4 -> 6 | rc0 completed_no_dispatch | 4 / 50 |
| nang-tran vong_review 4 -> 6 | rc0 completed_no_dispatch | 5 / 51 |
| nang-tran codex_review_calls 4 -> 6 | rc0 completed_no_dispatch | 6 / 52 |
| begin-attempt (fresh doctor --json, no missing required tools) | rc0 reserved_for_dispatch=true; running; attempts 5/6; reviews 4/6; offline Codex calls 4/6 | 7 / 53 |
| record-post (first H 0563bdb, comment https://github.com/ducthangho/tra-luat/pull/1399#issuecomment-6981749091) | rc0 completed_no_dispatch | 8 / 54 |
| transition reviewing (head 0563bdb) | rc0 completed_no_dispatch | 9 / 55 |
| record-codex-call (run 02883089b299420cb9f2dc1738941382) | rc0 reserved_for_dispatch; offline Codex calls 5/6 | 10 / 56 |
| independent Codex service review of 0563bdb | changes_requested, one P2 finding pending-recovery-raises-before-lease-rebind (see Erratum) | - |
| record-review changes_requested, first six tries | six clean UNKNOWN with no write: git clone timeout (twice), noncanonical JSON bytes of the coordinator-written receipt (three times), local master behind origin during the temporary clone (once); the coordinator corrected the receipt bytes | 10 / 56 |
| record-review changes_requested (canonical receipt) | rc0 completed_no_dispatch; running; reviews 5/6 | 11 / 57 |
| begin-attempt rework (fresh doctor --json, no missing required tools) | rc0 reserved_for_dispatch=true; running; attempts 6/6; reviews 5/6; offline Codex calls 5/6 | 12 / 58 |

Every command used the stock canonical launcher (`--require-clean`, `--expected-head d39313e`, 20-minute deadline) and the packet_loop scoped entrypoint with expected revisions, fresh authority resolves and actual paired state/witness high_water readback. No hand-written state/witness/HMAC, serialized proof reuse or counter reset. Each limit raise went through canonical nang-tran citing the owner decision https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6978536145 and stays within the admission allowance. The doctor image for begin-attempt was taken through agent-creds-exec with an owner-provisioned key file that was deleted immediately after doctor.

## Evidence integrity

Raw operational logs and private lineage stay outside this candidate. These SHA256 values identify actual private receipts; they do not independently grant authority or prove a future gate.

- adopt-state (r64 admission) clean UNKNOWN receipts: cd664754ec9bc81416826f0e628e2dc5845b43556b4e5fc49d78625025aea3f6, 3bfd34b4178cea0445937a33f8d1dbbc51ef6674560fecb185048ea142d70144.
- adopt-state: finished 2026-11-18T13:37:17.936316+00:00; receipt SHA256 2a5095b0038cf6d766da2c6f8b0f2d45e355e05eef2d48107120085b74246dea.
- nang-tran-attempts clean UNKNOWN receipts: f8c5c47610949348b83b26f5805fd79a917c1f576c1434d6d068e435ab3581fd, 76936d1d9ee4c0f885e32cd6819e6674d3b97436034f7a213d3a9ed7c3e4d767.
- record-lease: finished 2026-11-18T14:07:31.858133+00:00; receipt SHA256 33bb9835be5a26f4cdabf424388b35ff1f765277dc4267c5599c32380f78bde3.
- nang-tran-attempts: finished 2026-11-18T14:10:49.103998+00:00; receipt SHA256 0ea0a820cb8b293f4a42c69cb90fa68cadedb86f89c2ddf2206c3a9f3e970403.
- nang-tran-vong_review: finished 2026-11-18T14:13:40.904240+00:00; receipt SHA256 c25635a8d7f1d8d2aca18b01325987cfd4c10776686062abb63b944f5c754f75.
- nang-tran-codex_review_calls: finished 2026-11-18T14:17:15.771125+00:00; receipt SHA256 ed8c4bdab1abcb21c3d9a2d338d88a22e54c9d917ef82022282a949cc78c88a2.
- begin-attempt: finished 2026-11-18T14:22:05.348781+00:00; receipt SHA256 d7fc6bfac32cac4c01043d3e69c5c0a3aeb7df71c2e7a3a890a67874fccaea81; doctor image SHA256 8cfa4abbdb7456a38a5671b528994aa379abdfdd8a89f9707c6618b18cafa22f.
- record-post: finished 2026-11-18T14:42:43.752837+00:00; receipt SHA256 09854ef636b0d700d2897011e652ad9d0c4fecf9d3a66ab911e1b4a1f2ff5f63.
- transition reviewing: finished 2026-11-18T14:45:37.598933+00:00; receipt SHA256 7e45ababf0854faf67c409a3e825a024c5bbc5c181721874857d215701375db5.
- record-codex-call: finished 2026-11-18T14:47:45.937665+00:00; receipt SHA256 ae51182e9b9a4fc289ed66fdb64780901193a088ca4051067a44f09efcbed188.
- record-review clean UNKNOWN receipts: a433d12f6cce6073fca714835428fe4b411cd21fc2d7401fce665d94c6acc6e1, fcce961f5c94cfee461db387a7cfeb7fb8c662bd0e1e3f9231d25a0c46a9f1a2, 7779b56784d8f00291b0473199c745aa7d23fe47534e000690c6ba27f5ffced1, de55d9f92a23aad15b248cea87f03cd4c9dbafae74d34269a37531c54aafc334, f8fd914e89177984655405003d445a275792d23b22707e8cfd8140de7a9c1af4, aed0ddc4b305e63f4806b961d4ebbde37e357abf8d71ea8fecac3ee1ebe249c2.
- record-review: finished 2026-11-18T15:34:33.379794+00:00; receipt SHA256 02b8ea59f67ee7a3dcfa1c3eae31230d00c8c91c5dfc44ea8a7f2238b948e73b; advisory receipt SHA256 080c642c8baeec54fc5553f587bd97ab8808d2df6f68335abba4cdf68fd9b9a1.
- begin-attempt rework: finished 2026-11-18T15:36:43.794169+00:00; receipt SHA256 fc82932b49765428a70c4304d3cecca7673665df606608d580a88bd49cf2bb4e; doctor image SHA256 2732cea9dee20614ec2094d732af7b27845d6f860e1e92f200f7b117ea537ce0.

Observed running state SHA256 82dc8e11c5dbd4edba51106b7536ea75faf2b1e9bc941f224d4a479ec4b3f448; witness SHA256 6f68b508c2f7271aabfdf323620cfaca213fdc80d807fbcbf785e9f367f485bc; witness high_water matches generation9/state_revision12/state digest.

## Authority, limits and remaining gates

Owner decisions https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6975912237 , https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6978536145 and erratum https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6982222196 ; Installed64 https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6979218857; Installed65 https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6979844522; Packet grant https://github.com/ducthangho/tra-luat/issues/1308#issuecomment-6979255125 and reissue note https://github.com/ducthangho/tra-luat/issues/1308#issuecomment-6979862026. Boot 2f7fa68a held by a keeper process; root/device/inode/mount/magic/seed fingerprint unchanged; same enrollment id/binding kept for canonical adoption.
Frozen allowance 2026-11-18T12:59:00Z to 2026-11-18T18:59:00Z, bounded by MCR-1172-C1 2026-11-24T18:53:00Z; earliest deadline governs. No pause/reset/automatic extension or successor.
Remaining in g9 after this reservation: no further attempt, one review round and one offline Codex call, plus one genuine exact-H connector. The offline review of this H is scoped to the packet's five-path diff. No WP1179 cleanup, source/Windows/fullM9/LIVE/security/account/ACL edits or paid credit purchase.
Independent review, actual-human exact-H/tree/spec/generation/PR audit by the owner, controlled H publication, applicable exact-H Ubuntu CI, genuine exact-H connector completion and positive canonical accept (receipt comparison per #1393) with readback remain mandatory. H must remain local until the actual-human audit; P results never substitute for H evidence.
This five-path metadata/canary diff does not change product, CI or protocol. No PR0-PR8 dispatch or Mission completion is authorized by this checkpoint.
