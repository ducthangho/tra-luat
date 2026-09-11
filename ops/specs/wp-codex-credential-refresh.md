---
schema_version: 1
kieu: dac_ta_packet
packet_id: wp-codex-credential-refresh
packet_issue: 484
revision: 6
generation: 6
environment: local
platform: windows
executor: codex
risk: sensitive
review_class: sensitive
base_sha: 09da7f213b2ecee562fc333e2ab30985dec96c3c
base_tree: 7c6903611ad59ae195b57d45e74b30c70b8d5bf7
canonical_target: 26e2555d36c48b3c0f625ae50ab2cfb62b6cb858
branch: codex/wp484-g6-integration
---

# WP484 r6/g6 — Windows trust path separators and canonical integration

Owner authority: https://github.com/ducthangho/tra-luat/issues/484#issuecomment-5630819103. Approved proposal SHA256 a8708b10734c0d5687e6515885af8800233312c342fb8674894c63e0c282f0f6. Preserve inherited acceptance through immutable r5 and r4 specs. G5 runtime review never started; G4 evidence remains historical.

## Scope

Fix _probe_trust_claude to accept equivalent Windows path separators for exactly the trusted workspace. False, missing, malformed and contradictory alias records must fail closed. Do not modify user configuration, use broad private workspace or bypass probes. Add direct neutral/adversarial tests and demonstrate intended mutation failures. Preserve non-Windows path semantics.

Archive r5 raw bytes with original SHA256 500a7cf6eb01322e87591d748bab7575d9d4da989fd610b974ccb084ba44c659. G5 lease may change only spec_path/prompt_path and G6 supersession; preserve historical hashes/counters. Create G6 lease/spec/handoff. Approved edit paths:

- .claude/dev/launcher.py
- .claude/dev/launcher_test.py
- ops/specs/wp-codex-credential-refresh.md
- ops/specs/history/wp-codex-credential-refresh-r5.md
- ops/leases/wp-codex-credential-refresh-exec-g5.yaml
- ops/leases/wp-codex-credential-refresh-exec-g6.yaml
- ops/handoff/wp-codex-credential-refresh-exec-g6.md

Canonical import by ordinary merge is separate integration authority. No arbitrary imported-file edits; no VERSION/CHANGELOG/manifest/workflow edits, no G2/G3/G4 push or force-push. Metadata-only ordinary G5/G6 pushes may establish reciprocal succession before content. Stop if ownership conflicts.

## Acceptance and evidence

Targeted native Windows and WSL trust tests, existing trust controls, hash t23, schema/GitHub ownership/admission, EOL/doctrine and temporary strict release manifest before review. Imported canonical target must be ancestor. Freeze exact head/tree; independent Claude Code fable5/max review in bundle-only workspace with separate scratch; validate modelUsage. Full CI Windows+Ubuntu once after approve. Distinguish passed, failed, skipped, not_run. User trust is consent, not proof of probe correctness. No credential/device-auth/LIVE tests.

## Budget and authority

Executor openai_codex/codex_service, Windows machine/local; reviewer anthropic_claude/claude_code, independent read-only context. Content attempt1 maximum for G6, prior4/global limit5. Carry exactly one UNUSED Claude reservation forward, max20minutes; prior Claude7/Codex2 retained. No refund/reset/additional call. Run2026-09-11T07:08:41Z through2026-09-11T08:38:41Z. Lease expiry 2026-09-11T11:10:20Z, heartbeat30minutes. Other protocol ceilings remain.

Publish safe authority/heartbeat/verdict/CI results to issue484 and successor PR. Owner conditionally authorizes exact-head merge/land after independent approve, required gates/admission and durable SHA binding. Post-merge evidence and bookkeeping required for landed; other land paths require ownership/authority. No deploy/LIVE or guard bypass.
