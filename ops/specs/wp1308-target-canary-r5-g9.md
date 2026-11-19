# wp1308 r5 — Desktop g9 accept-after-1393 continuation and canary completion, Mission65
packet_id: wp1308
revision: 5
generation: 9
mission_issue: 1172
mission_revision: 65
mission_plan_sha256: 4ffa95ce252faa793883ea6f8956d6ce27d0443d6e37368d720e4c4c48158215
contract_id: WP1308-r5-g9-desktop-accept-after-1393
immutable_acceptance_baseline: d39313eceb71c185deca65878383a94284be3f54
admission_ref: refs/heads/ops/wp1308-target-r5-g9@6804e047069606c3188ab7f46902cc0d89cf6e3f
admission_path: ops/admissions/wp1308-r5-g9.json
admission_sha256: aa6c7db7b2096d332542931de0f3e42f39a01eb01ffcb21cfe5b64536bd67056
executor: codex
environment: local
risk: sensitive
review_class: sensitive
effective_review_class: sensitive
assurance_target: human_audited

## Authority and history
Owner decision r63: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6975912237 (open #1393, then g9). Owner decision on g9 limits: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6978536145 (attempts/review/Codex 4 -> 6; owner audits canary exact H personally). Installed Mission64: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6979218857 ; corrected by Installed Mission65 (Packet1308 registration row only): https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6979844522 .
G8 (r62/r63, lease wp1308-r5-g8-codex) ended approved_pending at rev8 (sha cea8bf86) with H 6886ebe reviewed, owner-audited, CI-green and connector-clean; accept failed because publication receipts were compared on raw_snapshot_sha256 and page counts. Its allowance ended 2026-11-18T10:45:00Z. Closure: https://github.com/ducthangho/tra-luat/issues/1308#issuecomment-6979228525 . #1393 fixed the comparison (PR #1397, merged d39313e). History, counters (attempts 4/4, review 4/4, Codex calls 4/4), findings, costs and failures are preserved; nothing is replayed or refunded.
Canonical product: master d39313e (packet_loop.py sha256 bd10b4df320d3278485063067a035a3a800c550db9dae37e7d697da6a5f21698).
Same WSL boot as g8 (2f7fa68a), keeper still holding. g9 adopts the g8 state through canonical adopt-state (pending recovery) into journals-g9 with the same enrollment id and binding. Root/mount/magic/seed fingerprint unchanged; no seed creation/copy/export, reset, delete or fresh init.

## Effective write set
- ops/admissions/wp1308-r5-g9.json
- ops/specs/wp1308-target-canary-r5-g9.md
- ops/prompts/wp1308-target-canary-r5-g9.txt
- ops/leases/wp1308-r5-g9-codex.yaml
- ops/canary/wp1308-target-canary.md

## Envelope
Hard expiry 2026-11-18T18:59:00Z (allowance end; earliest of allowance/lease/installation/MCR-1172-C1 governs). A boot keeper holds the WSL boot; any boot/identity/ref mismatch stops at a checkpoint.
Lifecycle: adopt-state (initial; pending recovery of the approved_pending predecessor); canonical nang-tran on attempts, vong_review and codex_review_calls to 6 each (bounded by the admission allowance, citing the owner decision); record-rescue only if the state is blocked; record-lease rebind; begin-attempt; canary H (adds only ops/canary/wp1308-target-canary.md); record-post; transition reviewing; record-codex-call; one offline Codex service review (requested xhigh) scoped to the packet's five-path diff against the baseline; record-review. Each mutator through the stock launcher with expected revisions and receipts; never replayed.
Owner performs and posts the actual-human exact-H audit (human_exact_head_audit.v1) before H publication; the coordinator never signs or substitutes it. Then exact-H Ubuntu PR CI, one genuine connector, canonical K0-K7, accept (Repository Activity collector; receipt comparison per #1393) with paired state/witness readback. The human-remote-run input is the earliest workflow run on H across all same-head runs.
No WP1179 log cleanup, Windows CI, full M9, source changes, executor model calls, target G5/enrollment, installation, LIVE, PR0-PR8 or Mission closure. Preserve failures, UNKNOWN usage and billing.
