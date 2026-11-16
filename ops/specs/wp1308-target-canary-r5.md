# wp1308 r5 — Desktop adopted readmission and canary completion, Mission57
packet_id: wp1308
revision: 5
generation: 5
mission_issue: 1172
mission_revision: 57
mission_plan_sha256: 058b399f8b370f09df8d7288225ae42aa2a7edbb097b418c105ac2266e82a403
contract_id: WP1308-r5-desktop-adopted-readmission
immutable_acceptance_baseline: e4cce23bcf975bf041d584f9d4b74327b9c03794
admission_ref: refs/heads/ops/wp1308-target-r5-g5@96982a992b19f25b4b7ecf79e901264fbaec5596
admission_path: ops/admissions/wp1308-r5-g5.json
admission_sha256: acd20a4ccf6c3b02d2236a903b0111cde9eb521b1eafd2299d33692bc350809d
executor: codex
environment: local
risk: sensitive
review_class: sensitive
effective_review_class: sensitive
assurance_target: human_audited

## Authority and history
Owner decision r57: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6931505436 (owner audits canary exact H personally). Installed Mission57: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6932329106 . Packet instruction: https://github.com/ducthangho/tra-luat/issues/1308#issuecomment-6932355367 .
G4 (r36, lease wp1308-r4-g4-codex) reached approved_pending rev6/witness7 on Desktop and expired 2026-11-14T01:23:19Z awaiting actual-human exact-H audit. Its history, counters, costs and failures are preserved; nothing is replayed or refunded.
WP1315 landed at aa718cb (adopted approved_pending recovery); canonical product used here is master e4cce23 (packet_loop.py sha256 d571702aa60f47a60b845130ae3f9a8139a8a65cae3a2c655da75936e6bb5fc7).
Desktop rebooted after g4 (boot 7e1ab957 -> 3bdc0002). Same-boot readmission is impossible, so g5 adopts the g4 state through canonical adopt-state into journals-g5 with the same enrollment id and binding (required by canonical adoption) and the newly measured boot/coordinator. binding_sha256 therefore no longer equals the builder hash of current boot facts; this is recorded, not hidden. Root/mount/magic/seed fingerprint unchanged; no seed creation/copy/export, reset, delete or fresh init.

## Effective write set
- ops/admissions/wp1308-r5-g5.json
- ops/specs/wp1308-target-canary-r5.md
- ops/prompts/wp1308-target-canary-r5.txt
- ops/leases/wp1308-r5-g5-codex.yaml
- ops/canary/wp1308-target-canary.md

## Envelope
Hard expiry 2026-11-17T18:50:00Z, before routing exception MCR-1172-C1 (18:53:00Z); earliest applies. Overall cap 360 minutes. A boot keeper holds the WSL boot; any boot/identity/ref mismatch stops at a checkpoint.
Lifecycle: adopt-state (initial) then record-lease via WP1315 recovery, each through stock launcher with expected revisions and receipts; never replayed. Continuing the canary needs a new attempt; exhausted limits are raised only through the canonical nang-tran path with a recorded owner instruction, never by editing state.
Reviewer: one independent Codex review of the canary H. Owner performs and posts the actual-human exact-H audit (human_exact_head_audit.v1) before H publication; the coordinator never signs or substitutes it. Then exact-H Ubuntu PR CI, one genuine connector, canonical K0-K7, accept with paired state/witness readback.
No Windows CI, full M9, source changes, target G5/enrollment, installation, LIVE, PR0-PR8 or Mission closure. Preserve failures, UNKNOWN usage and billing.
