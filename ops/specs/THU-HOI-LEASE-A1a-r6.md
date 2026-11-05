# THU-HOI-LEASE-A1a - revision 6 (draft)

## Reason and authority

Revision 5 raised the A1a-only addition ceiling to 800 but retained the original A16 comparison against the generation 1 baseline. That is insufficient after independent canonical commits: the `thu-hoi` admission workflow requires the current PR base S to be an ancestor of candidate H, while `git diff B0..H` necessarily includes upstream spec files when H incorporates S. This revision changes only the A16 attribution rule for verified upstream-only drift. It preserves r5's 800-line/three-product-file ceiling, all other r3 M1-M14 and A1-A22 requirements, r4 role routing, and owner human audit.

The incorporated contracts are r5 at blob `94f3c7d4ddfa988d0b44fb8e83695891589e4b03` (SHA-256 `42a1bb7dcc37b530799b6705c966c58e075dba6fcaaadead526b879f5f53fa42`), r4 at blob `6cb435619fc85f3fe295ec2c399735012e28aad9`, and the r3 technical contract at blob `401804bacea92ae5305bb5c3a36cc3821f973227`. This revision does not activate the revocation ledger or permit a fourth authored product path.

## Baselines and A16 attribution

- `B0 = 7f65476afdac57023be1b83ddec0df36a5e8d4b8` remains the immutable historical acceptance baseline of generation 1. The complete `B0..H` diff and all generation 1 findings remain in evidence; they are not erased or relabeled as passed by a rebase.
- `S` is the exact canonical `master` commit used as `base.sha` for the final implementation PR admission run. The dispatcher records S, its tree, and the complete path/numstat diff `B0..S` before a continuation. S must descend from B0. Every path in `B0..S` must be outside the three A1a write-set paths and correspond to a separately merged canonical change. If any A1a write-set path changed upstream, this rule does not apply and the packet stops for a further decision.
- The generation 2 executor constructs candidate H from S with only the three A1a product paths changed. `git merge-base --is-ancestor S H` must return 0; the canonical `thu-hoi` admission run must independently confirm S/H. For every upstream-only path in `B0..S`, tree(H) must contain exactly the same blob and mode as tree(S). No upstream change is credited as executor work.
- **A16 for generation 2:** `git diff --numstat S..H` must touch exactly `ops/lease_publish.py`, `ops/lease_publish_test.py`, and `.github/workflows/ops-thu-hoi-admission.yml`; total added lines across those paths must be at most 800. The executor also publishes the full `git diff --numstat B0..H` and the exact `B0..S` subtraction so the original baseline and upstream provenance remain visible. A fourth authored path or any unexplained upstream byte change is red.
- If canonical master advances after H is reviewed, the candidate and any CI/review/human authorization for H are stale for the admission check. Incorporating a new S requires a new H, fresh affected gates and exact-head review, and a push checkpoint under the applicable budget. It does not silently move B0 or treat the old verdict as valid.

## Continuation and gates

```yaml
packet_id: THU-HOI-LEASE-A1a
packet_issue: 564
mission_issue: null
revision: 6
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

The generation 1 lease is fenced before generation 2 is granted. A durable generation 1 handoff must name its committed head/tree and any uncommitted P2 patch by hash; the new lease names the exact continuation OID and source, B0, current S, r6 spec hash, new branch ownership, and owner decision. The dispatcher reconciles all remote refs and checks holders on each of the three paths before publishing the successor lease. A self-issued lease or overlapping active holder is invalid.

Generation 2 follows r5's two-stage push order: independent read-only Codex review and required local gates, including Windows local if classified required, on exact local H; then one authorized push of that H and a draft PR; then connector review, PR CI, canonical `thu-hoi` admission, and owner human audit on the same H before merge. Reuse of generation 1 evidence is limited to unchanged code and unchanged test selection and must be labeled with its tested SHA. Any required skipped or unavailable gate is red. Merge, post-merge CI/provenance, bookkeeping, and lease release follow r4; a merge alone is not landed.
