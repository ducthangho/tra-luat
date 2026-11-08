M8 authoritative — wp1271 r10/g10: landed, acceptance and lease retirement

PR [#1276](https://github.com/ducthangho/tra-luat/pull/1276) merged exact approved H8 via normal merge; canonical CI [42424728996](https://github.com/ducthangho/tra-luat/actions/runs/42424728996) SUCCESS23/23Ubuntu, full selftest1777/1777 and four actual source anchors independently audited. Canonical D1–D4 checker rc0; final lease retired actual UTCZ. No open P0–P3 and no finding waiver.

Durable metadata commit `8db50149dcbc4e0b76bcfbe29d3c7159f962dc1d`: [M8 YAML](https://github.com/ducthangho/tra-luat/blob/8db50149dcbc4e0b76bcfbe29d3c7159f962dc1d/ops/land/wp1271-r10-M8.yaml), [retired lease](https://github.com/ducthangho/tra-luat/blob/8db50149dcbc4e0b76bcfbe29d3c7159f962dc1d/ops/leases/wp1271-r10-g10-claude.yaml), [94-source evidence index](https://github.com/ducthangho/tra-luat/blob/8db50149dcbc4e0b76bcfbe29d3c7159f962dc1d/ops/checkpoints/wp1271-r10/canonical-M-final/index.json). Remote branch and exact M8/lease/index bytes read back equal before this publication.

```yaml
packet: wp1271
revision: 10
generation: 10
spec_hash: 313ece86f69081e6a35e6c18c46be65f9ddb45f5611ee991160ad10ef739ff55
head_da_review: d2fecaa1516cbc8c20b70331a45c8c728e59ddce
tree_h: 818cb867ad28eb26e00d1f8d14ea847316205d94
review:
  verdict: approve
  open_findings:
    P0: 0
    P1: 0
    P2: 0
    P3: 0
  verdict_url: https://github.com/ducthangho/tra-luat/issues/1271#issuecomment-6713611050
  receipt: 698f680276946411a71612820aea438583ed3967:ops/reviews/wp1271-r10-review5.receipt.yaml
  executor: actual Claude Code run543dc17c54de467fb356eeb01675fc25
  reviewer: fresh actual Codex CLI run616c0f3dc54a40fd88a2b0a693648b99
  human_audited: false
windows:
  status: passed
  head: d2fecaa1516cbc8c20b70331a45c8c728e59ddce
  native: PS5.1 and PS7
  normal_each: 23/23 en-US
  focused_each: 49/49 tr-TR
  child_records_verified: 52
  archive_sha256: 8de22f58c3e9278c19069fece6427ffdb858cfc720f42cad38feb32a7e1ad1ca
  windows_ci: not_run per owner instruction
ci_pr:
  run_id: 42419093844
  conclusion: success
  jobs: 23/23 Ubuntu
  checkout: 3cc8d776c1241e26f934f3a5726357f0af996bc8
  anchors: source observations and independent log audit14; bounded legacy unknowns preserved
duyet_chu_kho: https://github.com/ducthangho/tra-luat/issues/1271#issuecomment-6714107843
merge_commit: efebadf83409a81e42e6c97f1b7255ede76110f5
merge_parents:
- c6afde62c846f1ef3d6a83c14459966849edf756
- d2fecaa1516cbc8c20b70331a45c8c728e59ddce
tree_m: 818cb867ad28eb26e00d1f8d14ea847316205d94
ci_master:
  run_id: 42424728996
  attempt: 1
  event: push
  conclusion: success
  jobs: 23/23 Ubuntu
  checkout: efebadf83409a81e42e6c97f1b7255ede76110f5
  artifact_id: 13595253034
  artifact_sha256: 0821a2d3313313b74e98d726ebc36eda3e90bea6678dd4a47d8ee5aaf1ea55c6
  selftest: 1777/1777
  runtime: CPython3.12.16/Linux
  auxiliary_audit_receipt_sha256: 96a2df9be386f97e6d837c7c3d714956421f540172852fa915ff480f762a8a30
nghiem_thu:
  M1: passed
  M2: passed
  M3: passed
  A1: passed
  A2: passed
  A3: passed
  A4: passed
  A5: passed
  A6: passed
  A7: passed
lease_cuoi: wp1271-r10-g10-claude
landed: true
moc_10_2_2:
  run: passed
  checkout: passed
  workflow_definition: passed
  gate_output: passed
scope_limits:
- No LIVE/runtime activation
- S1 foundation only; S2/S3/P2 separate
- No universal concurrent ABA interception or repository-wide outward-junction discovery claim; reviewed declared limits
lease_retirement:
  retired_at_utc: '2026-11-08T00:04:21Z'
  lease_sha256: b68746efb153691d66705352f0f15577949e41856c667dfdfc3f7f92576a775a
  reason: exact_H_merged_canonical_CI_23_of_23_passed_no_remaining_executor_work
  authority: https://github.com/ducthangho/tra-luat/issues/1271#issuecomment-6714107843
recorded_at_utc: '2026-11-08T00:04:21Z'
assurance_limits:
- All 23 raw canonical gate-output job observations remain not_measured; the raw workflow-definition slot remains not_measured.
  This source audit supplies a separate derived four-anchor conclusion, not an automated consumer pass.
- Packet-loop skips one named Windows-only case and its associated mutant; skips are not passes or killed mutants.
- Log hashes identify official plugin received UTF-8 decoded text; original remote raw-byte identity is not asserted.
- Lifecycle records quet-cay and a lock path; lock enforcement was not independently tested by this audit.
- Native Windows was not rerun. This is auxiliary canonical CI evidence auditing, not formal code approval.
budget:
  attempts: 9/9 terminal
  shared_codex_calls: 16/16 terminal
  offline_code_review_rounds: 5/5 terminal; round5 approved
  primary_product_pushes: 1/1
acceptance_evidence:
  M1: 'Independent review5 + both connectors: 0 open P0/P1/P2/P3; no finding waiver'
  M2: Original class table review5 closes all historical manifestations; immutable histories preserved
  M3: Paired native C/H8 PS5.1+PS7, normal23/23 and focused49/49,52 children byte-verified; WindowsCI not run per owner
  A1-A7: Native original committed harness full ID projection144 unique pass IDs; source evidence checkpoint35c97ff7e996bd0ec12ddea1857b34a2ebaca062
    ops/checkpoints/wp1271-r10/final-H8
  Linux: ExactH8 full1777/1777; Ruffdelta0; strictmanifest184/184; admission/diffcheckrc0
  postmerge: ExactM23/23Ubuntu, all4sourceanchors,1777/1777 officialartifact, mandatoryreadonlylog audit16
```

This record closes only P1-S1. Mission#1238 remains in_progress for P1-S2/S3, P2 Playwright and later phases. No LIVE/runtime activation; no WindowsCI/fullWindowsmutantCI. Required native focused Windows evidence remains measured on exactH8. Original bounded provenance unknowns/skips stay unchanged; independent source audit supplies the four-anchor conclusion, not a fabricated automated-consumer pass or human audit.
