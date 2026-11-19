# Packet1308 r5/g7 — Desktop canary evidence checkpoint

Mission60; genuine draft PR #1364; immutable baseline 14f7dd3a593fc1ef225e5067e73569a702153871.
This candidate records the executed g7 adoption, limit raises to 4/4/4, rescue exit, lease rebind and attempt reservation. It does not claim review, human audit, H CI, connector completion or final acceptance.

## History carried into g7

g6 (Mission59) ended blocked rescue_required (codex_review_calls) at state revision 11 (sha 6da87c0e) after an offline Codex review returned blocked with one P2 finding, inherited-raw-hmac-literals-in-reviewed-tree, about baseline-identical WP1179 test logs outside the packet diff; the g6 review prompt over-scoped to the whole tree. That finding and all g6 counters (attempts 2, review rounds 2, Codex calls 2) are preserved. Closure: https://github.com/ducthangho/tra-luat/issues/1308#issuecomment-6940650122 .

## Executed checks

| Check | Actual outcome | State revision / witness revision |
|---|---|---|
| adopt-state g6 -> g7 (initial) | rc0 completed_no_dispatch; blocked rescue_required carried by canonical adoption | 2 / 26 |
| nang-tran attempts 2 -> 4 | rc0 completed_no_dispatch | 3 / 27 |
| nang-tran vong_review 2 -> 4 | rc0 completed_no_dispatch | 4 / 28 |
| nang-tran codex_review_calls 2 -> 4 | rc0 completed_no_dispatch | 5 / 29 |
| record-rescue --quyet-dinh nang_tran | rc0; blocked -> running | 6 / 30 |
| record-lease rebind -> wp1308-r5-g7-codex, tries 1 and 2 | rc8 UNKNOWN: resolver fresh clone timed out after 480s; no state/witness write (reconciled by digest) | 6 / 30 |
| record-lease rebind, try 3 | rc0 completed_no_dispatch | 7 / 31 |
| begin-attempt (fresh doctor --json, clean) | rc0 reserved_for_dispatch=true; running; attempts 3/4; reviews 2/4; offline Codex calls 2/4 | 8 / 32 |

Every command used the stock canonical launcher (`--require-clean`, `--expected-head 14f7dd3`, 20-minute deadline) and the packet_loop scoped entrypoint with expected revisions, fresh authority resolves and actual paired state/witness high_water readback. No hand-written state/witness/HMAC, serialized proof reuse or counter reset. Limits were raised only through canonical nang-tran bounded by the g7 admission allowance 4/4/4, with owner instruction https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6940706317 as can_cu. The doctor image for begin-attempt was taken through agent-creds-exec with an owner-provisioned key file that was deleted immediately after doctor.

## Evidence integrity

Raw operational logs and private lineage stay outside this candidate. These SHA256 values identify actual private receipts; they do not independently grant authority or prove a future gate.

- adopt-state: finished 2026-11-17T06:51:32.917466+00:00; receipt SHA256 8c4491fcc0f3eb29e98333e125d93ff9d9b8c1831a9f14503bdac9c961100907.
- nang-tran attempts: finished 2026-11-17T06:55:13.241952+00:00; receipt SHA256 44334e56360da794fa8dc00414a61bbfc4dd1250d767467818e7259802808ebf.
- nang-tran vong_review: finished 2026-11-17T06:59:19.177755+00:00; receipt SHA256 e6a994585eba463d2240760d406094dcb062112b84e0bab0b5e20ea2c6c91b9d.
- nang-tran codex_review_calls: finished 2026-11-17T07:07:07.321926+00:00; receipt SHA256 5c061a8ccc8c2b238839ddd124034f061167e13fbce40c9522154618516b8737.
- record-rescue: finished 2026-11-17T07:09:14.868660+00:00; receipt SHA256 c173b2c34225452a205409fa6d3d532c82d45fa5d82d83fad13aed37461be606.
- record-lease try 1 (rc8): finished 2026-11-17T07:17:17.539390+00:00; receipt SHA256 4e95be417ff51d02e2425e878ab06ddfebad5ae963225ac414c24058b1de897c.
- record-lease try 2 (rc8): finished 2026-11-17T07:30:07.848355+00:00; receipt SHA256 81812d76fedf98d8cc4e9d19874d047c45557d22233905d95fe1e7906deaca16.
- record-lease: finished 2026-11-17T07:51:50.987498+00:00; receipt SHA256 10ef25b6531e444737b7b83bf369b5b2d2bec5d72eb3023aa6675bc3025d2635.
- begin-attempt: finished 2026-11-17T07:54:54.880834+00:00; receipt SHA256 7988fe1a546fc676a01c4b47361b9b0ee0907d974771948ce7f2e76a4c3bd9d3; doctor image SHA256 0ab456d88ca78d6c43d48c874b59107792d19755472965cfeeb3b804a4e80a55.

Observed running state SHA256 d721d76320cc014cbcd0e987ea28a41ae6054b03cf73dd45c995bf406e25d256; witness SHA256 3a457dd8ef83269c0f2b37250d6e27deab0726ff63246307417852be40895014; witness high_water matches generation7/state_revision8/state digest.

## Authority, limits and remaining gates

Owner decision r60 https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6940706317; Installed60 https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6940711831; Packet grant https://github.com/ducthangho/tra-luat/issues/1308#issuecomment-6940753723. Boot 932e5ec5 held by a keeper process; root/device/inode/mount/magic/seed fingerprint unchanged; same enrollment id/binding kept for canonical adoption.
Frozen allowance 2026-11-17T06:36:00Z to 2026-11-17T12:36:00Z, bounded by MCR-1172-C1 2026-11-24T18:53:00Z; earliest deadline governs. No pause/reset/automatic extension or successor.
Remaining in g7 after this reservation: one more attempt, two review rounds and two offline Codex calls, plus one genuine exact-H connector. The offline review of this H is scoped to the packet's five-path diff. No WP1179 cleanup, source/Windows/fullM9/LIVE/security/account/ACL edits or paid credit purchase.
Independent review, actual-human exact-H/tree/spec/generation/PR audit by the owner, controlled H publication, applicable exact-H Ubuntu CI, genuine exact-H connector completion and positive canonical accept/readback remain mandatory. H must remain local until the actual-human audit; P results never substitute for H evidence.
This five-path metadata/canary diff does not change product, CI or protocol. No PR0-PR8 dispatch or Mission completion is authorized by this checkpoint.
