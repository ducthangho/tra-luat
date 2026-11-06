# Human audit comment URL identity - Packet #1254

- Status: proposed normative addendum; effective only after this addendum and its consumer land on canonical master.
- Source: HUMAN-AUDIT-URL-IDENTITY r2; separate from frozen Packet #1187 and PR #1253.
- This bounded addendum amends only the audit-source URL comparison described by ADR-0063.

## Decision

For `human_exact_head_audit.v1` only, `/pull/N#issuecomment-ID` and `/issues/N#issuecomment-ID`
are exact aliases of one comment when the scheme is HTTPS, host is github.com, repository is
the canonical repository, and both the positive integer number and raw comment ID match.
No other path, query, encoding, host, repository, number or fragment is accepted by this rule.
The current raw API `html_url` may use either exact alias. The raw API `issue_url`, owner login,
GitHub User type and OWNER association remain mandatory and unchanged.

The consumer normalizes only a parsed copy of `audit_source` to the canonical pull URL for
comparison. It does not edit raw JSON, comment body, timestamps or evidence history, and does
not follow a redirect to infer authority. Closed schema, exact field types, H/tree/spec,
Packet/revision/generation/PR, both review axes, findings and earliest-run timing remain intact.
A genuine edit after the earliest workflow still fails M5/M12. This is not a post-push audit
exception and does not extend URL equivalence to authorization or historical transition records.

## Compatibility and evidence

Frozen historical spec bytes and Accepted ADR-0063 remain untouched; they are not rewritten
to claim prior implementation of this rule. The same unchanged historical raw comment may be
evaluated by the amended canonical consumer after rollout, without changing its original
H/tree/spec or timing. A proposed local consumer passing is not a production gate.

Existing long-test receipts remain evidence for their exact original identities. This addendum
does not waive CI, M9, admission, independent review, land authority or integration checks.
