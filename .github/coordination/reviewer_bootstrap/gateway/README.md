# RA-03 GitHub capability gateway — WP122

This candidate exposes exactly two additive capabilities: an active-lease heartbeat and an
exact-head Reviewer verdict. It validates a sealed Dispatcher authority snapshot outside the
candidate checkout, then checks exact repository, issue/PR lane, reviewed SHA, Packet revision,
generation, attempt, schema revision and `reconcile_key` before the integrated RA-01 fake store can
write anything.

The offline implementation has no credential, network client, raw `gh`, REST/GraphQL proxy, token,
header, arbitrary method/path, command, metadata mutation, label/state change, approval,
mark-ready, ref/workflow operation, merge, deploy or LIVE surface. Candidate and Reviewer tests
must use `FakeGatewayGitHub`; operational promotion from an exact canonical SHA remains outside
this Packet and requires a fresh pin/readback plus the mandatory human audit.

Run the complete positive/negative matrix, including optimized Python boundary controls:

```text
python .github/coordination/reviewer_bootstrap/gateway/selftest.py
python -O .github/coordination/reviewer_bootstrap/gateway/selftest.py
```

The suite emits a machine-readable final report with scheduled, executed, passed, failed, skipped
and not-run counts. Any nonzero failed/skipped/not-run count is red.
