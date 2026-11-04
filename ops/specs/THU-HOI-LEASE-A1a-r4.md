# THU-HOI-LEASE-A1a - revision 4

## Authority and scope

This revision supersedes revision 3 only for execution and review routing. The owner authorized Codex to act as executor and as an independent reviewer, with a human audit before merge, on 2026-11-02. It does not activate the revocation ledger, enlarge the write set, or waive any technical acceptance criterion.

The authoritative technical contract remains `ops/specs/THU-HOI-LEASE-A1a-r3.md`, blob `401804bacea92ae5305bb5c3a36cc3821f973227`, SHA-256 `ac7e0129b281b517c69e9a2512a05b47d55ad99f0ac964462c061ea511f70bc1`. All objectives M1-M14, tests A1-A22, measurement scripts and hashes, limits, negative controls, and stop conditions in that exact blob are incorporated into this revision without change. The parent slice A1 in `ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` r9 is incorporated for technical scope; its `executor: claude` and `assurance_target: cross_approved` are superseded by the routing below.

## Packet

```yaml
packet_id: THU-HOI-LEASE-A1a
packet_issue: 564
mission_issue: null
revision: 4
generation: 1
objective: Implement the A1a code slice of ADR-0047 under the immutable r3 technical contract.
depends_on:
  - 579
executor: codex
environment: local
risk: sensitive
review_class: sensitive
write_set:
  - type: exact
    path: ops/lease_publish.py
  - type: exact
    path: ops/lease_publish_test.py
  - type: exact
    path: .github/workflows/ops-thu-hoi-admission.yml
```

The lease may additionally list a handoff path outside the product PR diff. No other product path is authorized. The executor must remeasure all baseline-dependent facts at the lease base and stop when any r3 invariant or hash does not hold.

## Review and land gates

1. A fresh Codex session reviews the exact candidate head independently of the executor session. It records model family, execution surface, transport, run receipt, findings by cause class, and explicit P0/P1/P2/P3 counts. Same-provider review is recorded as `same_provider_approved`; it is never labeled `cross_approved`.
2. Every P0/P1/P2/P3 finding must be resolved with evidence on the final head. If the head changes, repeat review and affected gates. The GitHub connector must complete on that same head, and every thread must be resolved or explicitly dispositioned under the protocol.
3. Run the full r3 local acceptance suite and required CI on the exact head. Run the ADR-0060 M3 Windows comparison if classified `required`; record test IDs and baseline/candidate delta. A skipped or unavailable required test is not success. Preserve positive markers, commands, return codes, runner identity, and artifacts in the evidence.
4. After findings are closed and required CI and Windows evidence are green, request a human audit by the owner on the exact head. The owner's verdict and approval are separate from the Codex review and must be read back before merge. No merge on this revision without that human audit.
5. Merge by merge commit only after the human audit and all current-head gates pass. Then collect four-milestone post-merge CI provenance, complete bookkeeping, and release the lease. A merge alone is not `landed`.

## Admission

Before granting generation 1, the dispatcher must verify the exact r3 blob and SHA-256 above, confirm #579 landed, reconcile the complete remote-head ref set, and run `ai-dang-giu` on each of the three product paths. Each must return `NGƯỜI_GIỮ 0` with a directly observed return code. An uncertain or occupied path blocks the lease. A later material change requires a new revision and generation.

