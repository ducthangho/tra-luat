# THU-HOI-LEASE-A1a - revision 5 (draft)

## Authority and scope

This revision succeeds `ops/specs/THU-HOI-LEASE-A1a-r4.md` solely to raise the A1a addition ceiling and to document continuation after the generation 1 capacity stop. The r4 file at blob `6cb435619fc85f3fe295ec2c399735012e28aad9`, SHA-256 `62a51da2a9c5d44cab1fd831ac50c12c18545d810e25b51ea958fffafa91bf97`, and its incorporated r3 technical contract remain authoritative except for the two clauses explicitly replaced below. Objectives M1-M14, acceptance A1-A22, measurement script hashes, three-path write set, Codex executor, independent Codex reviewer, and owner human audit before merge are unchanged. No revocation ledger is activated by this revision.

## Capacity decision

The A1a-only exception to ADR-0044 in r3 section 8.1 is raised from at most 663 to at most **800 added lines**, still at most **three changed product files**, measured by `git diff --numstat <immutable_baseline>..<reviewed_head>` and summing the added-line column across the three exact paths. This is a ceiling, not an acceptance target. The generation 1 candidate was reported at 696 added lines before two P2 fixes were committed; 800 allows at most 104 more added lines from that reported measurement. The executor must record the actual final numstat and stop if it exceeds 800 or touches a fourth product path. No technical test or review gate is waived.

## Git identity and continuation

- **Immutable acceptance baseline:** `7f65476afdac57023be1b83ddec0df36a5e8d4b8`, the `base_sha` of generation 1. It remains the left side of A16 and of every capacity measurement for this packet, including generation 2. The independent advance of `master` to `6c9079c2e6ef51bc2be27f1588958937e11cc261` changed only a spec outside the A1a write set; it does not move this baseline or require rebase.
- **Continuation base:** the exact committed generation 1 candidate recorded in a durable handoff. The local candidate reported before the two P2 fixes was `e6772d84def91d664d38ba8a3df59652a404008d`. This is an observation, not a substitute for the final handoff OID or authorization to push it. The generation 2 lease must name the actual continuation OID and the handoff/patch identity; any uncommitted fixes must be transferred with a measured patch outside the product diff and applied only under the new lease.
- **Reviewed candidate:** the final generation 2 head and tree after all fixes. A16 compares this head with the immutable baseline above. The branch-behind/default-branch check remains separate. Any merge with a newer master uses GitHub's merge commit after exact-head review and gates; it does not rewrite the candidate's baseline.

## Packet and gates

```yaml
packet_id: THU-HOI-LEASE-A1a
packet_issue: 564
mission_issue: null
revision: 5
generation: 2
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

Generation 1 must be fenced and handed off before generation 2 is granted. The dispatcher must recheck the full remote ref set and the three write-set holders at grant time, then publish one successor lease with the exact r5 hash, immutable baseline, continuation base, owner decision, and new branch ownership. Existing valid test evidence may be cited only for unchanged code and unchanged test selection; all affected tests, independent review, connector review, CI, required Windows comparison, and owner human audit must be tied to the final exact head. P0/P1/P2/P3 findings must be resolved before asking the owner to audit. A skipped required gate is not success.

The single implementation push has two distinct stages. First, while H is still local, a separate read-only Codex session must approve the exact H and all local gates required before push must pass on H, including the local Windows comparison if classified required; the executor records H, tree(H), review receipt, tests, and the immutable-baseline numstat in a durable handoff. Only then may the executor push that same H once and open a draft PR. Second, the connector review and PR CI run on the pushed exact H; the reviewer verifies that the Windows evidence, if required, still names that same H. The owner then human-audits H. Connector and PR CI are post-push merge gates, never claimed as prerequisites already passed before the push. Any new commit after push invalidates the exact-head evidence and requires a separate owner checkpoint under the applicable push budget; it is not silently folded into the one authorized push. No merge until all post-push gates pass and the owner audits H.
