You are the INDEPENDENT SPEC REVIEWER (Codex) for packet wp1494 of Mission #1172, repo ducthangho/tra-luat. Read-only: do not edit/commit/push, no GitHub writes, no workflow dispatch; scratch only under /tmp plus the output file below. Read CLAUDE.md, docs/PROTOCOL_DA_PHIEN.md and docs/adr/0060-* as needed.
Object (exact): ops/specs/wp1494-r1/SPEC.md at commit 8c68b39153a62ff26a982dc72add5f079277e051 (branch ops/wp1494-r1), sha256 22d6a09277509c5462c955278da03696c6931ea8aa9fbcfe349df73c9e451740. It is a frozen-spec candidate for a packet of plan r4: `git show origin/ops/wp1172-plan-r4:ops/specs/wp1172-source-plan-r4/KE_HOACH_NGUON_R4.md` (sha256 0f287ce4…; installed at Mission r83). Owner decisions: mission-r84.json; authority and budgets: mission-r85.json (same dir on that branch). Sibling specs may exist on branches ops/wp1460-r1 (B1), ops/wp1461-r1 (B3), ops/wp1462-r1 (B4).
Check adversarially: fidelity to plan r4 (no reintroduced removed mechanisms; owner decisions respected), internal consistency, feasibility against the CURRENT code on origin/master (read the files it touches; measure, run cheap probes), completeness and measurability of acceptance (two-direction cases, three states, dedicated mutants per check classified by the case's own exception class, A/B where behaviour must not change), write set correctness and overlap with live leases (python3 ops/lease_publish.py ai-dang-giu <path> after fetching all refs), budget/process consistency with r85, and anything that would make the executor build the wrong thing. Report ALL issues P0–P3 (the owner wants zero before approval).
Follow docs/PROTOCOL_DA_PHIEN.md §7 (reviewer evidence), §8, §8.1–§8.3 and .claude/skills/cross-review/SKILL.md (VERDICT layout) LITERALLY:
- Generalize every manifestation into a CAUSE CLASS and scan the whole candidate for all manifestations before reporting (§8.3, ADR-0060 M2); never report isolated instances.
- Each finding: id, class_slug (stable across rounds; reuse prior slugs for the same cause; split/merge only with a mapping table), severity, location, claim, evidence (command + observed output), and suggested_fix with the FOUR parts of §7: where (file+function/case and why there), how (direction only for product code; runnable for tests/mutants/measurement scripts), locking test (which test gives teeth and which mutant must die), and what the fix may spawn.
- "class_table": per class: slug, finding ids/manifestations, highest open severity, source round/SHA, common fix or reason for per-instance fix, closing check (command, result, what is unmeasured). Count classes and manifestations.
- From round 2: "prior_findings_check" (ĐỐI CHIẾU LƯỢT TRƯỚC): for EVERY finding of the immediately previous round, a label from exactly {ĐÃ VÁ THẬT, VÁ HỜ, VÁ SINH LỖI MỚI, CHƯA VÁ} with your own measured evidence; then "prior_class_status" per class (a class is ĐÃ VÁ THẬT only if all in-scope manifestations are closed, no same-mechanism regressions, nothing left to measure).
- "hunt_table" (BẢNG SĂN): >= 6 INDEPENDENT directions, each with hypothesis, command, real output, conclusion LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC; and "measure_table" (BẢNG ĐO) for quantitative claims.
- Evidence fields (§7): schema_version 1, packet_id, generation, provider "codex", role "reviewer", model_family "openai", execution_surface, transport, session_id, model_reviewer_identity, github_submitter_identity null, reviewed_sha, independent_from_executor_session true, review_axes ["spec","standards_security"], tests, findings, verdict, assurance (state what you can attest; never claim beyond evidence), evidence_url null.
Write JSON to $REVIEW_OUT and print it: {"schema_version":1,...,"verdict":"approve"|"changes_requested"|"blocked","reviewed_sha":"8c68b39153a62ff26a982dc72add5f079277e051","reviewed_file_sha256":"22d6a09277509c5462c955278da03696c6931ea8aa9fbcfe349df73c9e451740","findings":[...],"class_table":[...],"prior_findings_check":[...],"prior_class_status":[...],"hunt_table":[...],"measure_table":[...],"tests":[...],"notes":"..."}. Approve only with zero findings.

ROUND 5 NOTE (coordinator): Object unchanged from round 4 (same commit, same sha256). Round 4 returned "blocked" with ZERO findings solely because the reviewer sandbox could not fetch all refs, so every `ai-dang-giu` probe returned rc 12 (KHÔNG_XÁC_ĐỊNH). This workspace has now been fully fetched BEFORE your run (`git fetch origin '+refs/heads/*:refs/remotes/origin/*'`; set-compare of `git ls-remote --heads origin` vs `for-each-ref refs/remotes/origin` gave 0 missing; local master = origin/master). Run the probes yourself first (`python3 ops/lease_publish.py ai-dang-giu <path>` for each of the four write-set files) from this workspace; do NOT re-fetch (network may be blocked in your sandbox) — if a probe still returns rc 12, record it as KHÔNG ĐO ĐƯỢC in the hunt table and compare with the coordinator-run outputs below (taken from this same workspace minutes before your run), stating which you rely on. Expected, and NOT a spec defect: `.claude/dev/ci_dang_ky_test.py` is held by live lease wp1236-a-r12-g1-claude-20261121 until 2026-11-23T13:45Z — the spec is a frozen candidate; implementation starts only after that lease releases and a B2 lease is issued (writer-slot sequencing is the coordinator's job, not a spec finding unless the spec itself mis-states it).
Coordinator-run probe output:
== .github/workflows/canh-tuoi-audit.yml
PHẠM_VI: quét refs/heads/*; nhánh cục bộ tụt sau origin/<cùng tên> sẽ bị CHẶN
NGƯỜI_GIỮ 0: không có
rc=0
== ops/canh_tuoi_audit.py
PHẠM_VI: quét refs/heads/*; nhánh cục bộ tụt sau origin/<cùng tên> sẽ bị CHẶN
NGƯỜI_GIỮ 0: không có
rc=0
== ops/canh_tuoi_audit_test.py
PHẠM_VI: quét refs/heads/*; nhánh cục bộ tụt sau origin/<cùng tên> sẽ bị CHẶN
NGƯỜI_GIỮ 0: không có
rc=0
== .claude/dev/ci_dang_ky_test.py
HẾT_HẠN	wp1343-r1-g1-claude	refs/remotes/origin/ops/wp1343-r1-g1-lease:ops/leases/wp1343-r1-g1-claude.yaml
HẾT_HẠN	wp1343-r2-g1-claude	refs/remotes/origin/ops/wp1343-r1-g1-lease:ops/leases/wp1343-r2-g1-claude.yaml
HẾT_HẠN	wp1343-r3-g1-claude	refs/remotes/origin/ops/wp1343-r1-g1-lease:ops/leases/wp1343-r3-g1-claude.yaml
HẾT_HẠN	wp923-r2-g2-claude	refs/remotes/origin/ops/wp923-r2-g2-lease:ops/leases/wp923-r2-g2-claude.yaml
HẾT_HẠN	wp923-r3-g3-claude	refs/remotes/origin/ops/wp923-r3-g3-lease:ops/leases/wp923-r3-g3-claude.yaml
NGƯỜI_GIỮ 1: wp1236-a-r12-g1-claude-20261121
rc=0
Round-4 verdict for prior_findings_check: file wp1494-spec-review-4.json had 0 findings; prior_findings_check for round 5 is therefore empty, but carry prior_class_status from round 4 forward with your own re-measurement.
