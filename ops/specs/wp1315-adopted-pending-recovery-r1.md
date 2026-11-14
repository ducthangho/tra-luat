# WP1315 r1/g1 — private adopted-pending recovery design

This is the worker design note for Mission1172 r37 private preparation. The
immutable authority input remains outside this candidate: metadata commit
`55541d2a643bb4b2046163de4954fd813c8df730`, path
`ops/specs/wp1315-readmission-private-prepare-r1.md`, SHA256
`37abb5c3d38913d62195c59a555995434196051c5e55107b6ad07bc4c69ffaa8`.
The exact acceptance/continuation baseline is
`c0b8e11d7099f756e65db8bd9a81493cde789a6f`.

Executor: Codex, cloud Linux shell. Requested effort: high. Actual serving
model/effort: UNKNOWN. No reviewer/model/connector call or assurance verdict is
represented by the synthetic records below.

## Behavior and guards

The existing scoped `record-lease` path can recover one finalized adopted
`approved_pending` projection to `leased`, without granting dispatch. It requires
the original canonical v3 predecessor snapshot, its admission-bound digest and
generation, a closed scoped approval for its pending/reviewing head, a closed
attempt, and no prior human acceptance. The live pending image must match the
immutable adoption projection exactly, apart from its state revision and adoption
wrapper. This intentionally grants no new recovery privilege to legacy v2 input
without a scoped predecessor approval.
An old owner-scoped `same_provider_approved` record without a current owner
policy remains unsupported. The targeted predecessor uses `advisory_review`;
this change does not relax the owner-scoped historical assurance validator.

The normal TargetProof, current admission/allowance, expected revision,
state/witness pair, complete source tombstone chain and canonical I2 checks run
first. Recovery additionally requires finalized `adopted` with cutover intent,
a distinct current-generation lease, matching executor/reviewer identities,
matching current lease reference/OID/path, API comment bytes/hash, and a context
derived from the verified canonical lease. The live lease must pass the existing
lease schema/authority/expiry validator. There is no override or new CLI flag.

The inactive-policy reproduction also exposed a validation blocker before lease
rebind: the adopted pending image retains its predecessor lease generation, so
ordinary current-generation pending-lane validation rejects it. The new fallback
recognizes only the exact admission-bound immutable pending projection during
full-state validation. Internal source bytes supplied during adoption must match
the immutable source digest and deterministic projection. Prepared, intent and
aborted images remain valid representations for the existing adoption recovery
machinery; the ordinary state/witness pair still rejects them. This fallback does
not change `_pending_human_lane` or `CHUYEN_HOP_LE`, and it does not authorize any
lifecycle operation.

Recovery clears `reviewing_head_sha` and removes the stale optional live fields
`pending_sha`, `bien_nhan_approve`, `mo_lai_tu`, `checkpoint_day`, `moc_connector`
and `quyet_dinh_p3`. The original pending/scoped-review evidence remains in the
unchanged adoption snapshot. One history event binds the recovery to the
adoption ID, source digest, predecessor/target generation, old pending head,
new lease ID/OID and comment digest. Counters, all limits, attempt anchor,
consumed call IDs/heads, reviews, findings, posts, key and enrollment identity
are preserved exactly. Adoption and witness history remain unchanged; the usual
ordinary commit advances the state/witness revisions and high-water digest.

Postimage validation reconstructs this exact guarded recovery from verified I2
facts and compares the entire result before permitting the bounded additional
field changes. The global command whitelists retain their original entries.
Other `record-lease` cases cannot clear pending fields or change a review head.
Existing leased/running/reviewing rebind behavior is preserved.

A separate fresh reservation consumes the next cumulative attempt. Recovery
neither raises a limit nor reserves a call. An exhausted cumulative allowance
remains exhausted; an expired current allowance rejects recovery. Old approval
cannot directly authorize acceptance after recovery. Any necessary cumulative
limit increase must use the existing explicitly authorized path after recovery.

## Focused algorithmic evidence

Tests call the real `main(argv)` parser/router, reducers, canonical I2 against an
isolated local bare Git remote, state serialization and durable journal/witness
writers. Authority/API/native-runtime transport seams are synthetic. The two
advisory-record cycles, consumed calls and historical finding in each fixture are
synthetic data, not actual model/reviewer workloads. No Desktop target journal,
operational seed or HMAC was read or copied.

The baseline inactive-policy reproduction fails at full-state `adr0054`
validation. A separate valid historical-policy predecessor reaches baseline
`record-lease` and fails at `scoped lease rebind requires adopted predecessor
lease` (CLI rc8, no dispatch). Both red-before results are retained privately.

Final new regression selection: eight groups passed through
`chay_suite(script, tmp, chi_chay=ids)` with outer rc0. Product/test SHA256 values
were captured before and after that run and remained equal:

- Product: `ebfbd964f80101106a16d1e100e462b071a06511363fe9f9cf57e6ca107e67ca`.
- Tests: `26a4f4074da5dbd987b1f1b8f64b187b79972af9189d59de8b42f292a82bb01b`.

| Exact selected ID | Main property |
| --- | --- |
| `wp1315_adopted_pending_valid` | Inactive-policy recovery, exact preservation, replay rejection, separate cumulative reservation |
| `wp1315_adopted_pending_historical` | Historical-policy valid predecessor and the same preservation controls |
| `wp1315_adopted_pending_rejections` | Nonadopted/nonfinalized/aborted input; wrong source digest/generation/projection, current context/lease, witness, tombstone, expiry and generic transitions |
| `wp1315_pending_intermediate_no_dispatch` | Prepared and intent images cannot recover, reserve attempts/calls or record review |
| `wp1315_pending_postimage_exact` | Extra core/optional mutations reject before durable effects; 15 reach the exact postimage check and one fails earlier shape validation |
| `wp1315_pending_exhausted_budget` | Recovery preserves exhausted cumulative limits; a separate attempt is refused without dispatch |
| `wp1315_ordinary_record_lease_whitelist` | Ordinary lease acquisition cannot gain the recovery-only field permissions |
| `wp1315_pending_target_proof` | Synthetic same-family target recovery and missing/mismatched/expired TargetProof rejection |

The final twelve existing focused controls passed with outer rc0 in 335.93s,
capturing the same product/test hashes before and after the run. They cover
unchanged adoption/witness behavior,
scoped and legacy lifecycles, current target identity pairs and the K3 connector
parser. Exact commands, hashes, returned results and retained failures are in the
private evidence directory `/workspace/wp1315-private-evidence`; they are not
added to the candidate. Earlier red runs include one canonical serialization
postimage mismatch, negative-message assertion corrections, a malformed test
`accept` invocation, a baseline-copy import failure, and two synthetic target
lease setup rejections. None receives acceptance credit. The first controls run
passed but did not capture starting hashes and overlapped new test additions; a
single repeat on frozen product/test bytes records the final provenance.

AST parsing and diff whitespace checks passed. Ruff F-rule diagnostics match the
baseline message multiset exactly (both rc1: F841=3, F401=8, F541=2, F811=3).
The pre-existing test-file invalid-escape SyntaxWarning remains unchanged.

## Remaining validation and authority

These are private synthetic Linux algorithm checks. Enrolled native runtime and
mount/boot/seed behavior, Windows, full M9, GitHub CI, independent review,
publication, readmission and real target recovery are not_run in this phase.
The current K3 parser and human/first-publication/CI checks are unchanged.
No source push/PR, public candidate, target mutation, g5, merge, activation,
formal acceptance, complete-corrective delivery or canary PASS is claimed.
