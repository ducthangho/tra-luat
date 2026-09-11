---
schema_version: 1
kieu: dac_ta_packet
packet_id: wp-codex-credential-refresh
packet_issue: 484
revision: 5
generation: 5
environment: local
platform: windows
executor: codex
risk: sensitive
review_class: sensitive
base_sha: f2fed4834019e50f65bd05f1948e91906a13a6f3
base_tree: 7d9ba5cea8d4515489b4e7e46ceeba195a987f1b
canonical_target: 4b5184e21373eb8f8a36493d0282ebd020bb4458
branch: codex/wp484-g5-integration
---

# WP484 r5/g5 — immutable historical anchors and canonical integration

Authority: https://github.com/ducthangho/tra-luat/issues/484#issuecomment-5629705138. Owner approved proposal SHA256 9b6cdfd7f948e5a66b9433207280ca225ade4f629c2f76765a48ad0bd7ee3fdd. The remeasured canonical target's delta from 07218115 touches none of the nine metadata paths. Product base is c0a5cbe89a90588115262e1a2c3ac84cbd98be9e; G4 runtime acceptance and prior evidence are inherited through the immutable r4 specification, not reimplemented.

## Objective and edit paths

Repair historical prompt-anchor mismatches exposed by G4 CI. Preserve original r2/r3/r4 spec bytes, migrate only spec_path/prompt_path in old leases, retain all historical hashes/authority/base/counters. G4 may additionally carry the authorized G5 supersession marker. Create the G5 lease/handoff and current specification.

- ops/specs/wp-codex-credential-refresh.md
- ops/specs/history/wp-codex-credential-refresh-r2.md
- ops/specs/history/wp-codex-credential-refresh-r3.md
- ops/specs/history/wp-codex-credential-refresh-r4.md
- ops/leases/wp-codex-credential-refresh-exec-g2.yaml
- ops/leases/wp-codex-credential-refresh-exec-g3.yaml
- ops/leases/wp-codex-credential-refresh-exec-g4.yaml
- ops/leases/wp-codex-credential-refresh-exec-g5.yaml
- ops/handoff/wp-codex-credential-refresh-exec-g5.md

Canonical import by ordinary merge is authorized integration, not discretionary edits to imported files. No runtime, workflow, validator, VERSION, CHANGELOG or RELEASE_MANIFEST edits. Metadata-only commits/pushes on G4/G5 may establish two-way succession before content; no G2/G3 branch push or force-push. Keep original G4 head and accepted journal as historical evidence.

## Acceptance

1. Archived r2 from e7459bd326640500871d7cc9df5ccc92b6e9db38 has SHA256 5927e9368fb4ae2aabe356579a8287d7d555fbc3d3ade884c1ac6065122726af; r3 from625ea2a2cbe37626970550c8c2b4800af214b5fb has f21fca32754655d09cd6423af3b66ee906881da45e4e7f6e0685a261ce2b23a8; r4 fromf2fed4834019e50f65bd05f1948e91906a13a6f3 has e86a6a8cb5e2165d368be71d6a41b6a2bbdc0f9b1f653cafd627adf8c69072ef. Compare raw bytes, not normalized text.
2. All historical pointers must resolve to matching spec bytes. Run the existing validator and t23_MOI_lease_THAT_trong_kho_phai_QUA without hash rewriting or exemptions. Old fields remain unchanged except approved pointers/succession.
3. Canonical target must be ancestor of final integration head. Existing canonical admission must pass on its tree; local admission is distinct from hosted workflow receipt. Runtime bytes must match G4 exactly; identify canonical imports separately from the nine edited paths.
4. Fresh ownership, schema/GitHub checks, doctrine, EOL, temporary manifest and targeted Windows/Linux checks before independent review. Freeze exact head/tree, review, then full CI Windows+Ubuntu once on final identity. Skipped/not_run are not passed.
5. Preserve full G4 credential acceptance via immutable r4 spec and reusable runtime evidence. No real credential, device-auth or LIVE tests. No opportunistic P3 runtime changes.

## Provider, budget and land

Executor openai_codex/codex_service/machine-local Windows. Reviewer anthropic_claude/claude_code/machine-local, independent context, read-only source and external scratch, minimum claude-fable-5/max; validate actual modelUsage. Prior global content3 used; exactly one additional attempt, global limit4. Prior Claude7/Codex2 review calls remain historical; exactly one new Claude call, max20minutes, no refund/reset/extra call. Run2026-09-11T04:56:22Z through2026-09-11T06:26:22Z. Lease expires 2026-09-11T08:58:24Z; heartbeat30minutes. Protocol invocation/cloud-minute ceilings remain.

Owner conditionally authorizes merge/land after independent approve, exact-SHA green required gates/admission and durable head binding. Landed requires post-merge gates/bookkeeping; other land paths need ownership/authority. No deploy/LIVE/guard bypass/unapproved scope. Report changed master, conflicts or ownership delta before further writes.
