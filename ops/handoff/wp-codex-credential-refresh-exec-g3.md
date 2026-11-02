# WP484 r3/g3 execution checkpoint — not final approval

Owner authority: https://github.com/ducthangho/tra-luat/issues/484#issuecomment-5612165878
Admission/grant: https://github.com/ducthangho/tra-luat/issues/484#issuecomment-5612244207
Provider OpenAI Codex desktop/service, Windows local, machine/local. Reviewer independent Anthropic Claude Code, source read-only. Sensitive class. No runtime patch hint used.

Entry candidate3dcbfd7567a6c92be2d1182db95b84a4e738dbc1/tree8d6381d4920acceffb38b7015e0ed550c8b76bd8. Original product basec0a5cbe89a90588115262e1a2c3ac84cbd98be9e. This commit changes only authorized g3 spec/lease/handoff metadata. Exact resulting head/tree will be bound in the external review-start receipt after commit (not a self-referential hash).

G2 content1 plus g3 current1 = global2/3. State-dir g3 enforces at most2 remaining-generation attempts; g2 journal remains historical. Five prior Claude calls and two prior Codex calls retained; two additional Claude calls authorized,20minutes each. A2/A3 generated content and timed out without verdict, not refunded. Their metadata/diagnostics are local, no raw transcripts in GitHub.

A1 approved e7459bd326640500871d7cc9df5ccc92b6e9db38 only (0P1/P2,3P3). Runtime bytes have not changed since A1; later launcher_test.py modifications corrected two mutant anchors, copied the missing codex_cred companion, and exercised explicit resolved executable paths. Earlier two-mutant green claims were invalid false kills; corrected controls now pass on Windows and Linux: neutral t133 1/1 and two intended mutants2/2 killed. Full independent review on new g3 candidate remains required; do not transfer old approval.

Runtime evidence retained in g2 checkpoint and local artifacts: Windows/POSIX storage controls, recovery rollback, schema, raw environment boundary, checkpoint anchors and timeout-after-output. codex_cred14cases+14mutants each OS passed; related regressions Windows11passed/3POSIXskipped, Linux15passed/0skipped. New mutants Windows5kills;Linux4kills+1Windows-only not measured. Temporary manifest verification180/180 passed at runtime-identical g2 candidate; not a hosted full gate claim.

Current preflight: fresh Windows repository doctor rc0, no missing or unmeasured mandatory tools. Native codex/openai-llm authentication not established; executor is this desktop service, reviewer Claude. No live credential probe requested or performed.

Review recovery: prepare fresh scratch and existing harness before review; explicit available tools Bash/Read/Glob/Grep, default permissions, no source Write/Edit, no recursive cleanup. User-level supervision guard remains unchanged; known merge-base false positive disclosed, never bypassed. Source clone remains read-only and final status/tree must match. Final JSON/modelUsage and exact-SHA verdict required.

Required remaining work: independent current-head verdict and validated publication, final hosted CI with required Windows checks not skipped, final handoff. No full CI/full worker oracle yet; no push/successor PR/merge/land/deploy/LIVE. Master bookkeeping differences not merged automatically. Old g1/g2 lease/handoff files are historical and untouched.
