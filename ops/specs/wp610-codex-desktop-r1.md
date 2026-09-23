# WP610 — Codex Desktop receipt contract, revision1

Packet610, mission499; sensitive. Executor openai_codex/codex_desktop/machine.
Owner authorized completing r14/#523 and all PRs with class-based independent Codex
review to zeroP1/P2/P3; source https://github.com/ducthangho/tra-luat/issues/523#issuecomment-5791146266
and continuation “Triển khai đi, đã xong chưa”. This bounded dependency discovered
while delivering M11 is recorded at https://github.com/ducthangho/tra-luat/issues/610.
Agent projection is not human audit/independent approval or deployed dispatcher.

Base/acceptance baseline18d42cab74e80fc7635f754323fd13f520ccdcec.
Environment native Windows, offline WSL allowed. Fresh isolated worktree, no edits
to dirty D:/Quốc hội/tra-luat. Branch codex/wp610-g1. Three exact product paths:
1. .claude/dev/launcher.py — only add explicit non-CLI Desktop contract row/comment;
   do not change process launch, command routing, credentials, assurance or parser.
2. ops/bien_nhan_v2_test.py — Desktop contract regression and its counterexamples.
3. ops/KE_HOACH_THI_CONG_DA_PROVIDER.md — Desktop surface row and identity limits.
Limit3productpaths/300additions. No validator implementation change, workflow,
release metadata, old receipts, legal runtime, registry, deploy/LIVE or ruleset edits.
Authority metadata on codex/wp610-authority: ops/specs/wp610-codex-desktop-r1.md and
ops/leases/wp610-codex-desktop-r1-g1.yaml. Spec OID/hash frozen before lease.

## Defect class and acceptance

Class: provider-contract-rejects-truthful-surface. Source canonical receipt validator
reads launcher _TRANSPORT_CONTRACTS/_PROVIDER_NGOAI_CLI as structure; current Codex
set contains only codex_cli. WP523 receipt model surface codex_desktop is truthful
but schema rejects it. Not a defect of advisory review content, nor permission to
label Desktop as CLI. Keep desktop and CLI separate execution surfaces.

A1 Add exact openai_codex/codex_desktop/machine tuple to non-CLI vocabulary and policy
row; no alias and no wildcard. CLI resolver codex command must still return codex_cli.
A2 A Desktop advisory receipt accepted by schema; existing CLI receipt still accepted.
A3 Wrong provider with Desktop, wrong transport, unsupported surface rejected. A
Desktop model must not claim human_audited; same-provider/cross assurance cannot
be obtained solely by adding a surface. Subagent without identity evidence remains
advisory. Test positive and negative controls independently of production table.
A4 Removing Desktop row makes its designated regression fail for correct assertion;
other control observations stay valid. Mutants in external scratch only. Runtime
import must consume edited table, not stale modules/cache. No survivor called killed.
A5 Existing provider contract cases pass targeted on Windows; run relevant contract
suite once and report setup failure separately. No fullCI/fullselftest during repair.
A6 Product diff scope/EOL/size verified, native rc/positive output logged. No new
serving-model identity or OS sandbox claims. Original r14 receipt bytes not changed.
A7 Fresh independent Codex reviewer requested gpt-6-astra/max, no fork, immutable
exact H/tree; classify by defect mechanism; descriptive patch hints on authority
source, runnable counterexample hints allowed. No openP0/P1/P2/P3 before CI readiness.
A8 FullCI/admission plan only after readiness; human exact-SHA audit remains required.
Land separate session/authority; this run does not merge. Review artifact delivery
for this packet uses GitHub raw/readback first; Git receipt requires declared paths
in a later metadata stage, no wildcard. This packet does not close broader566.

Run starts09:37:05Z23Sep2026; deadline11:07:05Z, lease no later. Prior r14 evidence
stage is handed off pending this contract fix; its product head frozen. New packet
is a dependency with different source paths, not a reset of523 review history.
Reserve one independent review initially; owner loop instruction permits repair/
review tozeroP1/P2/P3, one call reserved at a time, with historical counts retained.
Quota, permission, deadline, scope drift still stop; changed acceptance needs revision.
No model/provider substitution to evade budgets. CI expenditure initially0 in this
packet run only, historical account spend unknown. Do not open PR until technically
ready because pull_request auto-runs heavy gates. Follow protocol/AGENTS/CLAUDE.
