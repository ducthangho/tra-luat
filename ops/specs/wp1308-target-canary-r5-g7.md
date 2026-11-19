# wp1308 r5 — Desktop g7 double-limits continuation and canary completion, Mission60
packet_id: wp1308
revision: 5
generation: 7
mission_issue: 1172
mission_revision: 60
mission_plan_sha256: 9987115c4dbb36538e3dbe710d557a8eff41429cb9a8119e98628b99d0900f0a
contract_id: WP1308-r5-g7-desktop-double-limits
immutable_acceptance_baseline: 14f7dd3a593fc1ef225e5067e73569a702153871
admission_ref: refs/heads/ops/wp1308-target-r5-g7@d8e4356ebc6295947a78ba1301ca93627f78dd3a
admission_path: ops/admissions/wp1308-r5-g7.json
admission_sha256: ba768469266048099004798dbfc673a8c222f9e83922c4559696a9988e3a2527
executor: codex
environment: local
risk: sensitive
review_class: sensitive
effective_review_class: sensitive
assurance_target: human_audited

## Authority and history
Owner decision r60: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6940706317 (double limits to 4/4/4; review scope limited to the packet diff; owner audits canary exact H personally). Installed Mission60: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6940711831 .
G6 (r59, lease wp1308-r5-g6-codex) ended blocked rescue_required (codex_review_calls) at rev11 (sha 6da87c0e) after an offline review whose only finding, inherited-raw-hmac-literals-in-reviewed-tree, concerned baseline-identical WP1179 test logs outside the packet diff; the g6 review prompt over-scoped to the whole tree. Closure: https://github.com/ducthangho/tra-luat/issues/1308#issuecomment-6940650122 . History, counters, findings, costs and failures are preserved; nothing is replayed or refunded.
Canonical product: master 14f7dd3 (packet_loop.py sha256 47ad08ef11359f81040e136ad83e77d393e332f1c960679b3547bb59c97f52b8).
WSL boot changed after the g6 keeper stopped (d72dd346 -> 932e5ec5). g7 adopts the g6 state through canonical adopt-state into journals-g7 with the same enrollment id and binding and the newly measured boot/coordinator. Root/mount/magic/seed fingerprint unchanged; no seed creation/copy/export, reset, delete or fresh init.

## Effective write set
- ops/admissions/wp1308-r5-g7.json
- ops/specs/wp1308-target-canary-r5-g7.md
- ops/prompts/wp1308-target-canary-r5-g7.txt
- ops/leases/wp1308-r5-g7-codex.yaml
- ops/canary/wp1308-target-canary.md

## Envelope
Hard expiry 2026-11-17T12:36:00Z (allowance end; earliest of allowance/lease/installation/MCR-1172-C1 governs). A boot keeper holds the WSL boot; any boot/identity/ref mismatch stops at a checkpoint.
Lifecycle: adopt-state (initial); nang-tran attempts, vong_review and codex_review_calls 2 -> 4 with the owner instruction URL as can_cu, bounded by admission allowance 4/4/4; record-rescue --quyet-dinh nang_tran; record-lease rebind; begin-attempt; canary H (adds only ops/canary/wp1308-target-canary.md); record-post; transition reviewing; record-codex-call; one offline Codex service review (requested xhigh) whose scope is the packet's five-path diff against the baseline; record-review. Each mutator through the stock launcher with expected revisions and receipts; never replayed.
Owner performs and posts the actual-human exact-H audit (human_exact_head_audit.v1) before H publication; the coordinator never signs or substitutes it. Then exact-H Ubuntu PR CI, one genuine connector, canonical K0-K7, accept with paired state/witness readback.
No WP1179 log cleanup, Windows CI, full M9, source changes, executor model calls, target G5/enrollment, installation, LIVE, PR0-PR8 or Mission closure. Preserve failures, UNKNOWN usage and billing.
