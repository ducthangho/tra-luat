# wp1308 r5 — Desktop g6 continuation and canary completion, Mission59
packet_id: wp1308
revision: 5
generation: 6
mission_issue: 1172
mission_revision: 59
mission_plan_sha256: 9c86e1558915895202a89d27c59c1d15b449ff877eb0e090afb405fa7e1b1e17
contract_id: WP1308-r5-g6-desktop-continuation
immutable_acceptance_baseline: 5f97e1eaaf4d97bbe86d71a7f6e21d1f60fa5a0a
admission_ref: refs/heads/ops/wp1308-target-r5-g6@3fcec62f24fe0450f3f18d1ec2154ca48ef32801
admission_path: ops/admissions/wp1308-r5-g6.json
admission_sha256: ae9b61b7a10fdd6964a52aae091e009f7098ea32a03422f3df8b2270a58139d0
executor: codex
environment: local
risk: sensitive
review_class: sensitive
effective_review_class: sensitive
assurance_target: human_audited

## Authority and history
Owner decision r59: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6937069662 (owner audits canary exact H personally). Installed Mission59: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6937079858 .
G5 (r57, lease wp1308-r5-g5-codex) adopted g4 and recovered to leased rev3 (sha 2030f1bd), witness rev11; closed by owner decision because attempts were exhausted and nang-tran had no attempts axis (https://github.com/ducthangho/tra-luat/issues/1308#issuecomment-6933338994). Its history, counters, costs and failures are preserved; nothing is replayed or refunded.
WP1350 merged at 59b3fb9 (nang-tran attempts axis); canonical product here is master 5f97e1e (packet_loop.py sha256 47ad08ef11359f81040e136ad83e77d393e332f1c960679b3547bb59c97f52b8).
WSL rebooted after g5 (boot 3bdc0002 -> d72dd346). Same-boot continuation is impossible, so g6 adopts the g5 leased state through canonical adopt-state into journals-g6 with the same enrollment id and binding (required by canonical adoption) and the newly measured boot/coordinator, then rebinds the lease through record-lease (adopted predecessor lease). binding_sha256 therefore no longer equals the builder hash of current boot facts; this is recorded, not hidden. Root/mount/magic/seed fingerprint unchanged; no seed creation/copy/export, reset, delete or fresh init.

## Effective write set
- ops/admissions/wp1308-r5-g6.json
- ops/specs/wp1308-target-canary-r5-g6.md
- ops/prompts/wp1308-target-canary-r5-g6.txt
- ops/leases/wp1308-r5-g6-codex.yaml
- ops/canary/wp1308-target-canary.md

## Envelope
Hard expiry 2026-11-17T09:22:00Z (allowance end; earliest of allowance/lease/installation/MCR-1172-C1 governs). A boot keeper holds the WSL boot; any boot/identity/ref mismatch stops at a checkpoint.
Lifecycle: adopt-state (initial) then record-lease rebind, then nang-tran for attempts, vong_review and codex_review_calls 1 -> 2 each with the owner instruction URL as can_cu, bounded by admission allowance 2/2/2; used counters are never reset. Then one begin-attempt, canary H (adds only ops/canary/wp1308-target-canary.md), record-post, one reserved offline Codex service review (requested xhigh, <=10 min), record-review. Each mutator through the stock launcher with expected revisions and receipts; never replayed.
Owner performs and posts the actual-human exact-H audit (human_exact_head_audit.v1) before H publication; the coordinator never signs or substitutes it. Then exact-H Ubuntu PR CI, one genuine connector, canonical K0-K7, accept with paired state/witness readback.
No Windows CI, full M9, source changes, executor model calls, target G5/enrollment, installation, LIVE, PR0-PR8 or Mission closure. Preserve failures, UNKNOWN usage and billing.
