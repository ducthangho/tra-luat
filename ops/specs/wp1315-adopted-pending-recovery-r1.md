# WP1315 — adopted-pending recovery design note (r5/g5 re-integration)

This is the worker design note that travels with the candidate. It is not the
Packet Spec and grants nothing. The authority input stays in controller
metadata outside this candidate: Packet1315 revision 5, generation 5, spec
`wp1315 r5 — readmission SOURCE sau WP1325`, SHA256
`6f3098f7f2c8aaabf7e7d98bc3931e630b37656599822d71c261d63da4cc84be`, under
Mission1172 r56.

- Canonical base `C`: `9c1661f76d5f4ef811aa349df102989cc2e2d53d`.
- Immutable acceptance baseline: `c0b8e11d7099f756e65db8bd9a81493cde789a6f`.
- Historical input: `669af5f9f58dfd72324d1f5b6aaefd15745592b1` (H669). Its
  audit and reviews are history on H669 only. They are not an audit, review or
  approval of this candidate.

Author: Claude (`claude-fable-5-2`, requested), Claude Code cloud Linux shell,
transport machine. Actual serving model/effort: not attested by this note. No
reviewer, connector, owner or human verdict is represented here, and nothing in
this note is `delegated_audited` or `human_audited` evidence.

## Re-integration result

At `C` the two Python paths are byte-identical to the immutable baseline, so the
question for this generation was semantic, not textual: do the canonical
changes landed since the baseline (lease publisher UTF-8 subprocess handling,
receipt reader, Windows gate script and unrelated packets) change what the
recovery logic must do? Every product hunk was re-read against the current
callers (`_load`, `_reader_state`, `_verify_lease_ref`, `_1174_state`,
`_1174_adopt_payload`, `_1174_ordinary`, `_1174_record_lease`,
`_1174_postimage`, `_1174_lifecycle_records`) and then measured. No hunk needed
to change. The resulting product and test bytes equal the H669 bytes:

- Product `.claude/dev/packet_loop.py`:
  `1db4e5536c20a139c58f485a85987e4801fcf80572e26e2e371977776bc256a1`.
- Tests `.claude/dev/packet_loop_test.py`:
  `d985a1092081e91ff2855255ec7c5b456339a49f431460062da83c2394b2f2e9`.

Equal bytes do not transfer H669's audit. The canonical modules these paths
load at run time (`ops/lease_publish.py` through the canonical validator copy)
differ from the baseline, which is why the measurements below were taken again
on `C`. No unrelated canonical change was reverted: the write set is exactly
these three paths.

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

Under the approved r39 option A, this recovery also requires every predecessor
call reservation to be consumed. A valid but unused old reservation rejects
recovery before any probe, synchronization or write. The check runs in actual
pending recovery, so diagnostic reads and immutable adoption evidence remain
valid. It does not retire, consume or delete a reservation, alter cumulative
counts, or change general scoped review and existing lease-rebind behavior.
A predecessor with an unused reservation needs further authority to resolve;
this path cannot make it recoverable by changing that evidence.

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
unchanged adoption snapshot. Exactly one history event,
`record_lease_pending_recovery`, is appended. It binds the recovery to the
adoption ID, source digest, predecessor/target generation, old pending head,
new lease ID/OID and comment digest. Counters, all limits, attempt anchor,
consumed call IDs/heads, reviews, findings, posts, key and enrollment identity
are preserved exactly. Earlier history entries, the adoption record and the
witness history are unchanged; the usual ordinary commit advances the state and
witness revisions and the high-water digest, and nothing else.

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

## Diagnostic reader (state_path)

The local unflagged reader includes the resolved state-file path in its
diagnostic enrollment and resolves the containing journal directory for relative
invocations. The strict canonical-path equality in pending-projection validation
is unchanged. Inactive-policy adopted pending and recovered leased images are
readable with `status` and `next-comment` using absolute or relative paths. The
diagnostic allowlist still excludes keys, history and source snapshots. Copied
images reject wherever the pending-recovery binding applies. The historical
pending/human diagnostic lane retains its existing behavior, including
diagnostic reads of copies; those reads create no authority.

## Findings carried from the first independent review of the old head

- F1 (reader `state_path`): the diagnostic-enrollment repair above.
- F2 (predecessor closure): the predecessor table covers open attempt, prior
  accepted SHA or human acceptance, scoped verdict/head, latest review
  verdict/head, pending versus reviewing head, predecessor generation,
  lease-context generation and lease ID, and owner-scoped assurance without a
  current owner policy. An actual historical v2 reducer output is adopted through
  the real router and rejected by recovery.
- F3 (unused reservation): option A, as described above.

Hint provenance: these were re-derived and measured by the earlier executor on
the old head; this generation re-read and re-measured them on `C`. No reviewer
patch was applied as executable proof.

## Focused evidence on `C` (this generation)

Scope: private synthetic Linux algorithm checks, Python 3.13.18, `python -B`.
Tests call the real `main(argv)` parser/router, reducers, canonical I2 against
an isolated local bare Git remote, state serialization and the durable
journal/witness writers. Authority/API/native-runtime transport seams are
synthetic. The advisory-record cycles, consumed calls and the historical finding
in each fixture are synthetic data, not model or reviewer workloads. No target
journal, operational seed or HMAC key was read or copied.

`packet_loop_test.py` has no case-selection flag: its `main()` ignores
arguments and starts the whole harness. Selection therefore used the module's
own `chay_suite(script, tmp, chi_chay={id})`, one required ID per call, after
checking that each ID occurs exactly once in `CASES`. Product and test hashes
were equal before and after every run.

- Eleven WP1315 groups: 11 passed, 0 failed, 0 skipped, 0 not_run; executed ID
  set equals the required set.
- Thirteen healthy controls: 13 passed, 0 failed, 0 skipped, 0 not_run; executed
  ID set equals the required set. Per-ID results and timings are in the author
  handoff.
- Four targeted mutants, each applied to a temporary copy of the product with a
  unique anchor:
  - `m1315_reader_state_path` kills `wp1315_pending_unflagged_readers` at the
    inactive-policy `status` assertion (rc8, `KeyError: 'state_path'` surfaced
    as a full-state validation rejection); controls
    `wp1315_adopted_pending_valid` and `wp1315_adopted_pending_historical` pass
    on the same mutated bytes.
  - `m1315_predecessor_attempt_open` and `m1315_predecessor_latest_verdict` each
    kill `wp1315_pending_predecessor_closure`: the mutated product completes a
    forbidden recovery with rc0 where the case requires rejection; control
    `wp1315_adopted_pending_valid` passes.
  - `m1315_unused_predecessor_call` kills `wp1315_pending_unused_reservation`
    the same way; control `wp1315_adopted_pending_valid` passes.
- Ruff F rules (ruff 0.16.9): 16 messages on the candidate and 16 on `C`
  (F401=8, F541=2, F811=3, F841=3), identical multiset after removing line
  numbers; delta 0. Both invocations exit 1 because of those pre-existing
  messages. `python -m ruff` is not installed in this environment; the
  standalone binary was used.
- AST parse of both Python files and `git diff --check` pass. The pre-existing
  invalid-escape `SyntaxWarning` in the test file is unchanged.

## Historical evidence (old head only)

The r37/r39 measurements, private evidence directories and hashes recorded for
`f97107bd99133a6a295385ba846884beac3a36a7` and H669 belong to those heads. They
are kept in the history of the superseded branch and receive no acceptance
credit here.

## Not measured by this author

Full self-test, the main harness, full M9, Windows, enrolled native runtime and
mount/boot/seed behavior, GitHub CI, the connector, publication, readmission and
real target recovery are `not_run`. The independent source review and the exact
head audit required before publication are outstanding. No source push, PR,
target mutation, G5 action, merge, activation or acceptance is claimed.
