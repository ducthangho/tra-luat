# wp1308 r5 — Desktop g8 accept-activity continuation and canary completion, Mission62
packet_id: wp1308
revision: 5
generation: 8
mission_issue: 1172
mission_revision: 62
mission_plan_sha256: d26ee2becd4ae842cc82c3ea6289f4c6c64b1ca9211f29e89019c8d5a3c274e0
contract_id: WP1308-r5-g8-desktop-accept-activity
immutable_acceptance_baseline: 641108cb997872b0ef2a277ea9c8faf8b82532bb
admission_ref: refs/heads/ops/wp1308-target-r5-g8@6193ffa81804aa36a848294b61231a34b1987227
admission_path: ops/admissions/wp1308-r5-g8.json
admission_sha256: d6b83e482bd5510777f1c9a012501e79683837ba95041e095d457cfcea9a5370
executor: codex
environment: local
risk: sensitive
review_class: sensitive
effective_review_class: sensitive
assurance_target: human_audited

## Authority and history
Owner decision r62: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6969055884 (open g8 via pending recovery; owner audits canary exact H personally). Installed Mission62: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6969082747 .
G7 (r60/r61, lease wp1308-r5-g7-codex) ended approved_pending at rev12 (sha 0f569cd4) with H 226bba5 reviewed, owner-audited, CI-green and connector-clean, but accept could not run because the Events-API publication collector could not produce evidence; its allowance ended 2026-11-17T12:36:00Z. Closure: https://github.com/ducthangho/tra-luat/issues/1308#issuecomment-6969216821 . #1370 replaced the collector with the Repository Activity API (merged 641108c). History, counters (attempts 3/4, review 3/4, Codex calls 3/4), findings, costs and failures are preserved; nothing is replayed or refunded.
Canonical product: master 641108c (packet_loop.py sha256 83743ed78450aad879974fc97699e6d508e5f712f54a52f83a2af1e4f1a0cbdb).
WSL boot changed after the g7 keeper stopped (932e5ec5 -> 2f7fa68a). g8 adopts the g7 state through canonical adopt-state (pending recovery) into journals-g8 with the same enrollment id and binding and the newly measured boot/coordinator. Root/mount/magic/seed fingerprint unchanged; no seed creation/copy/export, reset, delete or fresh init.

## Effective write set
- ops/admissions/wp1308-r5-g8.json
- ops/specs/wp1308-target-canary-r5-g8.md
- ops/prompts/wp1308-target-canary-r5-g8.txt
- ops/leases/wp1308-r5-g8-codex.yaml
- ops/canary/wp1308-target-canary.md

## Envelope
Hard expiry 2026-11-18T10:45:00Z (allowance end; earliest of allowance/lease/installation/MCR-1172-C1 governs). A boot keeper holds the WSL boot; any boot/identity/ref mismatch stops at a checkpoint.
Lifecycle: adopt-state (initial; pending recovery of the approved_pending predecessor); record-lease rebind (state leased, stale pending fields dropped); begin-attempt; canary H (adds only ops/canary/wp1308-target-canary.md); record-post; transition reviewing; record-codex-call; one offline Codex service review (requested xhigh) whose scope is the packet's five-path diff against the baseline; record-review. Each mutator through the stock launcher with expected revisions and receipts; never replayed. Limits stay 4/4/4; any raise only via canonical nang-tran bounded by the admission allowance with a recorded owner instruction.
Owner performs and posts the actual-human exact-H audit (human_exact_head_audit.v1) before H publication; the coordinator never signs or substitutes it. Then exact-H Ubuntu PR CI, one genuine connector, canonical K0-K7, accept (publication evidence from the Repository Activity collector) with paired state/witness readback.
No WP1179 log cleanup, Windows CI, full M9, source changes, executor model calls, target G5/enrollment, installation, LIVE, PR0-PR8 or Mission closure. Preserve failures, UNKNOWN usage and billing.
