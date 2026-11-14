# wp1315 r3 — Bounded review remediation and second source review
packet_id: wp1315
revision: 3
generation: 3
mission_issue: 1172
mission_revision: 39
mission_plan_sha256: f4ad9b9b50600c574409a3ab3445e6a2385ebaf7efb451ec9cf7778d668b4e4a
immutable_acceptance_baseline: c0b8e11d7099f756e65db8bd9a81493cde789a6f
continuation_base: f97107bd99133a6a295385ba846884beac3a36a7
executor: codex
environment: cloud
risk: sensitive
review_class: sensitive
effective_review_class: sensitive
assurance_target: cross_approved
source_instruction: https://github.com/ducthangho/tra-luat/issues/1315#issuecomment-6877126546
mission_installation: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6877126339

## Effective write set
- .claude/dev/packet_loop.py
- .claude/dev/packet_loop_test.py
- ops/specs/wp1315-adopted-pending-recovery-r1.md

The source authority spec/prompt/lease are controller-only metadata outside the product write set. Implement only the approved F1/F2/F3 remediation; no actual target journal/seed/HMAC is provided to worker fixtures.

## F1 diagnostic reader
Add the actual resolved state file path to the local read-only diagnostic enrollment. Retain strict canonical-path matching; no .get() workaround or guard removal. Test unflagged status and next-comment before and after recovery, inactive and historical controls, relative/absolute invocation, allowlisted output/no secret leak/no file writes; the new recovery binding must reject a noncanonical copied file. Preserve unrelated diagnostic and historical semantics; report a real scope contradiction rather than broadening policy.

## F2 predecessor closure coverage
Add executable negative cases for genuine historical-v2 predecessor, owner-scoped same_provider_approved without current owner policy, open attempt, acceptance fields, scoped/latest review verdict and head mismatch, pending/reviewing head mismatch, source-generation and lease/context mismatches. Assert rejection/no dispatch/probe/write/sync and byte-unchanged pair/source. Reuse synthetic canonical reducer/adoption/I2 fixtures. Targeted mutants only with positive distinguishing controls; do not weaken guards or fabricate kill credit where redundant checks keep a mutant safely rejected.

## F3 explicit policy decision
Choose fail-closed option A: this new adopted-pending recovery requires every predecessor call already consumed. If any old reservation is unconsumed, reject recovery before writes. Never mark it used/retire it/reset counts to make recovery pass. Do not broaden general scoped review/rebind code. Test an extra valid reservation before predecessor approve through the actual synthetic reducers and an all-consumed healthy control. Preserve cumulative counts/call identities/history.

## Envelope and handoff
One fresh Codex service context requested high <=45min, one fresh independent Claude Code second review requested high <=30min, private stage150 continuous minutes including all setup/tests/artifacts/stop. Before each invocation verify current authority/lease/I2, exact checkout/scope, readiness and remaining fit. Prior source implementation1 and source review1 remain consumed; known g4 offline workload1 remains historical. Older history/billing UNKNOWN is not zero. No journal initialization/edit or counter refund is required or authorized for the private code task; actual invocation reservations are kept in the controller's stage/Mission ledger, preserving old source and target journals unchanged.

After implementation, freeze exact private output head/tree/diff/test byte hashes. Dispatcher binds the generated head through a durable metadata registration and current lease before the second review; this is only the already approved three-path output, no new scope. Keep immutable acceptance baseline unchanged. A new finding after review2 means checkpoint; no third review or extra author context.

Do not run fullM9/main harness, Windows, CI, code push, source PR, merge, target mutation or G5 in this private stage. Run meaningful bounded focused Linux fixtures/counterexamples and preserve all failed/interrupted/not_run results. Close stage lease after handoff; no active writer/model/validation clock during subsequent actual-human source audit wait. Planned generation4/720min validation remains inactive until actual-human exact-head audit/publication decision and all readiness/ownership/I2/finite-fit conditions. No automatic pause/refund/reset/extension or target admission.
