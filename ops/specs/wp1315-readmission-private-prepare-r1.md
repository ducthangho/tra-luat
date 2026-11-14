# wp1315 r1 — Adopted pending recovery private preparation
packet_id: wp1315
revision: 1
generation: 1
mission_issue: 1172
mission_revision: 37
mission_plan_sha256: 5232110f74e464aee1d41bda4af54d0cbefbf6ebc1f7b3817f83c8843aa7af80
authority: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6872243930
registration: https://github.com/ducthangho/tra-luat/issues/1315#issuecomment-6872272511
executor: codex
environment: cloud
risk: sensitive
review_class: sensitive
effective_review_class: sensitive
assurance_target: cross_approved
immutable_acceptance_baseline: c0b8e11d7099f756e65db8bd9a81493cde789a6f
continuation_base: c0b8e11d7099f756e65db8bd9a81493cde789a6f
depends_on: [1174, 1309]

## Effective write set
- .claude/dev/packet_loop.py
- .claude/dev/packet_loop_test.py
- ops/specs/wp1315-adopted-pending-recovery-r1.md

The immutable authority spec above is controller metadata and is outside the worker write set. The third allowed path is the worker design note. No real target journal, seed, HMAC or private operational snapshot is supplied.
One implementation service worker requested high, <=45 minutes; actual serving model/effort UNKNOWN unless measured. Zero reviewer or connector calls. Max120 continuous minutes including publisher/I2 15, implementation45, focused Linux45, immutable artifact10 and stop5. No automatic successor. No source push/PR, product CI, Windows/fullM9, target change, g5, merge, activation or acceptance.
Claude/claude_code is the planned future independent cross-family reviewer identity only, with zero calls permitted now; this is not an assurance verdict. Later publication and review need separate applicable authority/gates.

## Acceptance for this preparation
Private exact commit/tree/diff and hashes, source contract/readback, focused synthetic Linux regression evidence with actual commands and exit codes, failures preserved and remaining native/CI/Windows/publication/readmission requirements. No claim of complete corrective delivery or canary PASS.

# Readmission recovery — private source preparation proposal

Exact r37 was approved by the user; this is the immutable source contract, not target activation or a claim of a working correction.

Current baseline is `c0b8e11d7099f756e65db8bd9a81493cde789a6f`; product SHA256 `c683ae3dddc8356370398327031234ee4623f2e9215c29892d3e0da417ebb8b2`. Its connector-marker change must remain intact.

The source condition being addressed is narrow: a valid old state has completed an advisory review and is `approved_pending`; its allowance expired before actual-human audit/publication. A genuine generation adoption preserves that state and all counters/history but clears its scoped review. Existing `record-lease` rebind rejects that state, while ordinary transitions cannot leave it. Review requires `reviewing`; accept requires a scoped review. Do not manufacture CI or connector findings to invoke `mo-lai`.

The proposed correction should use an existing authority-checked entry, preferably a narrowly guarded adopted-pending case of scoped `record-lease`. It must verify finalized adoption, the exact immutable predecessor snapshot, predecessor/target generation and fresh current canonical lease/context. It may invalidate stale live pending/review fields and enter a lease-ready state, but must preserve their evidence in immutable adoption/history. It must not grant dispatch. The global transition graph must keep `approved_pending` closed to generic `transition`.

All attempts/reviews/calls used, limits, call IDs and consumption, finding history, key/enrollment identity and source snapshot/tombstone remain unchanged or append-only as appropriate. No implicit limit increase, fresh attempt, review receipt transfer or acceptance. Subsequent new work needs explicit cumulative limits and an actual fresh canonical reservation/review. A stale or exhausted allowance cannot be revived by this correction.

The implementation must constrain any expanded postimage whitelist to exactly this guarded path. Other `record-lease` cases must not gain permission to clear arbitrary state. Current TargetProof, I2, identity, file/mount/boot, seed, expected revision, durability/tripwire, human, first-publication, connector and CI checks remain in place. No new override flag or manual context injection in production.

Focused tests should cover a valid finalized adopted-pending case and rejects for non-adopted state, unfinished/aborted adoption, wrong source digest, wrong generation/context/current lease, mismatched state/witness and replay. Verify no unauthorized write/dispatch and exact preservation of consumed counters/call identity/history. Tests use isolated synthetic algorithmic fixtures only; do not import the actual Desktop journal, seed or HMAC into the worker workspace. Preserve test failures and distinguish algorithmic evidence from native/CI acceptance.

The one private implementation worker may edit only the two product/test files and an Issue-specific design note. No code publication, PR, reviewer/connector, GitHub CI, Windows/full-M9, land/activation or g5 issuance is allowed in the preparation phase. Return an immutable private candidate, precise diff/hash/commands/results and the remaining validation/authority requirements. No complete-corrective or canary-PASS claim is justified by private preparation.
