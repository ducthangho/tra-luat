# Review readiness correction

The original request repeatedly authorized independent review. The old process treated a machine-local full Git clone plus review package as an expanded private payload, then asked again without first checking provenance/minimizing input. This caused unnecessary friction.

Correct this preparation: verify whether source is already public with anonymous access, prove each evidence origin/hash, and construct a fresh public-only source workspace. Do not copy an entire machine-local .git containing unrelated unpublished refs/loose objects. Reuse the user's review authorization for unchanged purpose/provider; do not ask repeated general permission. Preserve actual automatic rejections and obey them: a safer alternative must materially change exposure and be validated, not rename or reroute the rejected payload.

Here the GitHub API says public and anonymous pinned downloads verify H2 bundle +14spec/evidence files. R15 uses only those public inputs and a new anonymous GitHub clone; R13/R14 old private-local scope is not executed. Formal review, source SHA, budgets, independence/read-only constraints and sensitive assurance are not weakened. User feedback is applied to workflow preparation, not used to forge a verdict or override a guard.
