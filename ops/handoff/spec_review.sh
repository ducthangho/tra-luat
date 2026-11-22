#!/bin/bash
# usage: spec_review.sh PKT(wp1460) BRANCH HEAD SPECSHA ROUND [EXTRA_NOTE_FILE]
S=/tmp/claude-0/-home-user-tra-luat/0ed29fd3-d596-56bc-a105-f1c27f1c8301/scratchpad; R=$S/rvspec
P=$1; B=$2; H=$3; SH=$4; N=$5; X=${6:-}
C=$R/$P-clone; [ -d $C ] || git clone -q --no-local /home/user/tra-luat $C
git -C $C fetch -q origin "$B" ops/wp1172-plan-r4 ops/wp1448-r1 master 2>/dev/null || git -C $C fetch -q /home/user/tra-luat
git -C $C fetch -q https://github.com/ducthangho/tra-luat.git "+refs/heads/$B:refs/remotes/origin/$B" "+refs/heads/ops/wp1172-plan-r4:refs/remotes/origin/ops/wp1172-plan-r4" "+refs/heads/ops/wp1448-r1:refs/remotes/origin/ops/wp1448-r1" "+refs/heads/master:refs/remotes/origin/master"
git -C $C remote set-url origin https://github.com/ducthangho/tra-luat.git
git -C $C checkout -q -B "$B" "$H"
git -C $C config core.abbrev 7
git -C $C fetch -q origin "+refs/heads/*:refs/remotes/origin/*" 2>/dev/null; git -C $C branch -f master origin/master 2>/dev/null
PR=$R/$P-spec-review-$N-PROMPT.md
cat > $PR <<EOT
You are the INDEPENDENT SPEC REVIEWER (Codex) for packet $P of Mission #1172, repo ducthangho/tra-luat. Read-only: do not edit/commit/push, no GitHub writes, no workflow dispatch; scratch only under /tmp plus the output file below. Read CLAUDE.md, docs/PROTOCOL_DA_PHIEN.md and docs/adr/0060-* as needed.
Object (exact): ops/specs/${P}-r1/SPEC.md at commit $H (branch $B), sha256 $SH. It is a frozen-spec candidate for a packet of plan r4: \`git show origin/ops/wp1172-plan-r4:ops/specs/wp1172-source-plan-r4/KE_HOACH_NGUON_R4.md\` (sha256 0f287ce4…; installed at Mission r83). Owner decisions: mission-r84.json; authority and budgets: mission-r85.json (same dir on that branch). Sibling specs may exist on branches ops/wp1460-r1 (B1), ops/wp1461-r1 (B3), ops/wp1462-r1 (B4).
Check adversarially: fidelity to plan r4 (no reintroduced removed mechanisms; owner decisions respected), internal consistency, feasibility against the CURRENT code on origin/master (read the files it touches; measure, run cheap probes), completeness and measurability of acceptance (two-direction cases, three states, dedicated mutants per check classified by the case's own exception class, A/B where behaviour must not change), write set correctness and overlap with live leases (python3 ops/lease_publish.py ai-dang-giu <path> after fetching all refs), budget/process consistency with r85, and anything that would make the executor build the wrong thing. Report ALL issues P0–P3 (the owner wants zero before approval).
Follow docs/PROTOCOL_DA_PHIEN.md §7 (reviewer evidence), §8, §8.1–§8.3 and .claude/skills/cross-review/SKILL.md (VERDICT layout) LITERALLY:
- Generalize every manifestation into a CAUSE CLASS and scan the whole candidate for all manifestations before reporting (§8.3, ADR-0060 M2); never report isolated instances.
- Each finding: id, class_slug (stable across rounds; reuse prior slugs for the same cause; split/merge only with a mapping table), severity, location, claim, evidence (command + observed output), and suggested_fix with the FOUR parts of §7: where (file+function/case and why there), how (direction only for product code; runnable for tests/mutants/measurement scripts), locking test (which test gives teeth and which mutant must die), and what the fix may spawn.
- "class_table": per class: slug, finding ids/manifestations, highest open severity, source round/SHA, common fix or reason for per-instance fix, closing check (command, result, what is unmeasured). Count classes and manifestations.
- From round 2: "prior_findings_check" (ĐỐI CHIẾU LƯỢT TRƯỚC): for EVERY finding of the immediately previous round, a label from exactly {ĐÃ VÁ THẬT, VÁ HỜ, VÁ SINH LỖI MỚI, CHƯA VÁ} with your own measured evidence; then "prior_class_status" per class (a class is ĐÃ VÁ THẬT only if all in-scope manifestations are closed, no same-mechanism regressions, nothing left to measure).
- "hunt_table" (BẢNG SĂN): >= 6 INDEPENDENT directions, each with hypothesis, command, real output, conclusion LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC; and "measure_table" (BẢNG ĐO) for quantitative claims.
- Evidence fields (§7): schema_version 1, packet_id, generation, provider "codex", role "reviewer", model_family "openai", execution_surface, transport, session_id, model_reviewer_identity, github_submitter_identity null, reviewed_sha, independent_from_executor_session true, review_axes ["spec","standards_security"], tests, findings, verdict, assurance (state what you can attest; never claim beyond evidence), evidence_url null.
Write JSON to \$REVIEW_OUT and print it: {"schema_version":1,...,"verdict":"approve"|"changes_requested"|"blocked","reviewed_sha":"$H","reviewed_file_sha256":"$SH","findings":[...],"class_table":[...],"prior_findings_check":[...],"prior_class_status":[...],"hunt_table":[...],"measure_table":[...],"tests":[...],"notes":"..."}. Approve only with zero findings.
EOT
[ -n "$X" ] && cat "$X" >> $PR
PS=$(sha256sum $PR|cut -d' ' -f1)
cd /home/user/tra-luat && REVIEW_OUT=$R/$P-spec-review-$N.json python3 .claude/dev/launcher.py run --workspace $C --expected-head $H --require-clean --prompt-file $PR --expected-prompt-sha256 $PS --run-root $R/runs --name $P-spec-review-$N -- $(which codex) exec -m gpt-6-astra -c model_reasoning_effort=xhigh -s workspace-write --skip-git-repo-check -o $R/$P-last-$N.txt "$(cat $PR)" > $R/$P-launcher-$N.log 2>&1
echo rc=$? >> $R/$P-launcher-$N.log
python3 $R/kiem_verdict_lop.py $R/$P-spec-review-$N.json --vong $N > $R/$P-spec-review-$N.kiem83.txt 2>&1; echo "kiem83 rc=$?" >> $R/$P-spec-review-$N.kiem83.txt
sha256sum $R/$P-spec-review-$N.json > $R/$P-spec-review-$N.json.sha256
