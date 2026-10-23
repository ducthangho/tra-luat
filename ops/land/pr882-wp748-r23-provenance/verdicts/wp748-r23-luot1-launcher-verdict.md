# WP748 r23/g23 — PR #882 — independent review, round 1

Review status: complete; changes requested. Review class: sensitive.

Reviewer identity: this session identifies the assistant as OpenAI Codex, based on GPT-6 (runtime instruction). Provider self-identification: OpenAI. System-reported interface: API; observed execution surface/transport: machine access to local shell through `functions.exec` / `exec_command`. The enclosing `launcher.py run` / `codex_cli` invocation is supplied by the user, not independently attested by an accessible receipt in this session. No independently verifiable served-model identifier or launcher execution receipt for this reviewer has yet been exposed; the actual served model/family cannot be independently measured here. This statement is not assurance inferred from a tool name.

UTC start: 2026-10-23 01:31:54 UTC.

Identity verified before substantive review:
- HEAD: `8f12e02856eb130160c40188470f7e5911ab1687`.
- Tree: `7c3a033f68dedb3178ca85614aeaa1ffddc60cf6`.
- Detached HEAD: `git symbolic-ref -q HEAD` returned 1 (expected).
- Base: `747f983ccbcaf29a8e5228d09fd05b5a5ab6e479`.

Constraints: local, read-only review of `src/`; no credentials, network retrieval, commits, pushes, or GitHub comments. Scratch artifacts and this report only.

## Execution log (incremental)

- `git -C src rev-parse HEAD HEAD^{tree}`: rc 0; both identifiers matched (2/2).
- `git -C src symbolic-ref -q HEAD`: rc 1; detached as required.

## Findings

Final findings are recorded below; checkpoints retain the incremental execution history.

## Checkpoint 1 — identity, scope and mechanical checks

- Frozen spec found via local `origin/ops/wp748-r23-g23-lease` after `master` lookup failed (rc 128). Spec SHA-256 matches `6190ebbb943f1d017de32d9f316f85623906fded49379f4ce2540d957bee9584` (1/1). No fetch/network used.
- Delta is exactly two commits and 33 paths, all within the three permitted write-set entries; source status initially clean.
- Created scratch `review-scratch.4iOCXt/`; `git archive` of reviewed HEAD and extraction: rc 0.
- From the archive: `python3 ops/land_evidence_nguon.py --root .`: rc 0; 21/21 checked records pass, 28/28 cutover exemptions match, 49/49 accounted for, 0 violations, 0 unknown. This checks source existence/schema, not factual truth or assurance.
- From `src/ops/land/pr869-wp748-r22-provenance`: `sha256sum -c SHA256SUMS`: rc 0, 30/30 OK.
- Independent JSON aggregation: CI 39766018386 has 69/69 listed jobs, attempts 1/2 each 20 success + 3 failure; attempt 3 is 23/23 success. Each earlier failure has runner_id 0 and 0 steps. Run 39768193731 has 20/20 jobs; each attempt 9 success + 1 failed `dot-bien-gop`, runner_id 0, 0 steps. These numerical claims match.
- Round-5 prompt SHA-256 matches receipt `run-76825653.json` (1/1): `3842bc9cc5159f1e76ad32c0faf2b838a900a34b322174c5e41ce797e86604b0`.
- `run-964888d9.json` has 35 top-level keys; no model key. All five r22 receipts also lack a model key. The assurance demotion is justified; provider/surface labels alone do not establish served-model family.

Audit continues: semantic claims, reopening conditions, historical facts, peer records, secrets/EOL, and final source identity.

## Checkpoint 2 — semantic audit

- Merge/head tree and parents match local Git for both records (4/4 commit identities). r22's two claimed diffs are byte-identical, SHA-256 `bf5ffcf04ad41c25feb7922af8ec1c97ce78878c82ba4ec126290d73674edb83`, one file, +537/-11.
- r22 final verdict SHA-256 `6a60f9c7cfb16a7292995c1d1325de32f0f94d3bf8166eb5505046ce0c4ba99b` matches the retained PR comment. Its reported 8/8, 56/56, 22/22 and 78/78 are correctly attributed as `thuat_lai`, not rerun by this review.
- r846's PR CI is 14/14 success, admission is 1/1 success, and exact-merge CI is 14/14 success. Run timestamps, issue closure, verdict hashes, lease shortening, and frozen spec hash match retained evidence/local Git.
- `git diff --check BASE HEAD`: rc 2, 13 Markdown hard-break/trailing-space lines in the copied historical verdicts. These are retained provenance bytes, not lone CR; do not silently rewrite them to satisfy whitespace style.
- Static scan of all 32 added files: 32/32 free of lone CR; 32/32 without matches for eight credential/private-key pattern families (no matched secret values printed). JSON and text references to credential variable names are not credential values.
- Confirmed precision issues: r22 record line 31 says ready-for-review at 01:10:27Z, but the retained event is 01:10:26Z. Line 42's claimed connector trigger at 01:10:34Z is not present in its cited readback; the retained comment was created at 01:10:37Z and completed at 01:12:41.879488Z (after merge).
- r22 line 45 correctly reports cancelled status/updated_at and zero check runs, but states a cancellation cause as measured. The retained API response gives no cancellation reason/actor. Git shows a subsequent master merge at 01:15:18Z; that is temporal correlation, not proof of the cause.

Reopening conditions and report-only peer assurance gaps are being finalized.

## Final findings

Threshold applied: zero P0/P1/P2 for approval. **P0: 0; P1: 0; P2: 2; P3: 2.** Findings concern the new record/reopening instructions, not a request to alter historical provenance.

### WP748-R23-F01 — P2 — Require resulting assurance, not merely a recorded model

**Locations:** `ops/land/pr846-wp845-land-evidence.yaml:96`; `ops/land/pr869-wp748-r22-land-evidence.yaml:96` (continues on line 97).

**Scenario / impact:** The reopening alternatives say that the launcher measures the served model, or the owner records `khai_co_audit`, or there is `human_audited`. The first alternative does not require the measured family to differ from the Executor's family or bind the measurement to the review that supplies the approval. A newly instrumented launcher, or a measured same-family reviewer, satisfies that wording without curing either historical review's missing cross-family assurance. The owner-confirmation alternative also omits the auditor's confirmation required by the definition of `khai_co_audit`. The words naming evidence levels cannot substitute for those checks. These are incomplete instructions for reopening a sensitive land record.

**Evidence / rule:** `docs/PROTOCOL_DA_PHIEN.md:611` requires two independently served model families for `cross_approved` and defines `khai_co_audit` as a declaration accompanied by auditor confirmation. Lines 764–772 require the actual Executor–Reviewer pair and per-run evidence. Line 612 defines `human_audited` as an independent, durably identified auditor who reads the spec/diff and anchors audit evidence and verdict to the exact SHA. Current receipts prove neither historical served reviewer model. The frozen r23 spec uses the same shorthand; that shorthand does not override these protocol definitions.

**Fix:** Tighten these two reopening paragraphs, within the existing write set: require a completed independent approval on the exact authorized SHA, with evidence for the actual Executor–Reviewer pair establishing different served families; bind machine evidence to that approving run. For `khai_co_audit`, retain the weaker-than-`do_may` disclosure and require a named auditor's durable confirmation of the declaration. Alternatively require the full exact-SHA `human_audited` contract. Do not claim that an upgrade to the launcher retroactively measured old runs.

**Verification / regression risk:** Review the rewritten checklist against three negative cases: a measured same-family run, a model measurement from a different run/SHA, and an owner declaration without auditor confirmation. All must remain insufficient. No runtime test is required for this prose-only fix; the current source validator does not enforce these semantics. Avoid rewriting the historical receipts or treating these instructions as new land authorization.

### WP748-R23-F02 — P2 — Code equivalence alone cannot replace post-merge gate evidence

**Location:** `ops/land/pr869-wp748-r22-land-evidence.yaml:95`.

**Scenario / impact:** The reopening condition permits the gate on `7400df4` to be satisfied by inherited evidence of equivalent code (`hoac ke thua do bang chung ma tuong duong`). That is weaker than the protocol: an equal product file/tree can be tested by a different workflow, checkout, event, runtime, or required context. A later green run plus a code-equivalence comparison would meet the written alternative while leaving the cancelled merge gate unproven.

**Evidence / rule:** `readback-run-39882625690.json:12` is `cancelled`; `readback-check-runs-7400df4-all.json` contains zero checks. The retained successor CI on `747f983` is still pending. `docs/PROTOCOL_DA_PHIEN.md:946` requires Run, Checkout, Workflow definition and Gate output provenance; lines 954–959 explicitly reject treating tree equality as identity of commit, timing, workflow, test type, or runtime. Section 10.2.4 requires positive post-merge evidence. The r23 spec does not authorize a new code-equivalence exception.

**Fix:** Require a successful applicable post-merge gate on the actual merge, or describe a specifically authorized substitution with the successor SHA/run/attempt, ancestry and relevant scope comparison, all four CI provenance dimensions, positive required contexts and explicit disposition of the original cancelled run. Keep missing evidence `not_measured`; code equivalence alone must not close the item. The cheapest unambiguous wording is to retain the exact-merge gate requirement until an authorized alternative is documented.

**Verification / regression risk:** Check a candidate substitute with equal product bytes but a different workflow blob or missing required context: it must not qualify. This is a manual semantic check, not a claim that the existing validator catches it. Preserve the original `cancelled` result and do not turn an authorized exception into a measured pass.

### WP748-R23-F03 — P3 — Correct the two asserted event times

**Locations:** `ops/land/pr869-wp748-r22-land-evidence.yaml:31` and `:42`.

**Scenario / evidence:** Line 31 labels ready-for-review at `01:10:27Z` as measured, but `readback-events-869.json:30` records `2026-10-23T01:10:26Z`. Line 42 asserts a connector trigger at `01:10:34Z`; the cited comment snapshot contains no such timestamp. It records comment creation at `01:10:37Z`, completion at `01:12:41.879488Z`, and update at `01:12:42Z`. Completion after the `01:11:56Z` merge is correctly stated.

**Fix:** Use the event's `01:10:26Z` for ready-for-review. Remove the unsupported trigger time or label it unmeasured; if useful, report the separately named comment-creation and completion timestamps. Verify each time against its exact field. Do not rename comment creation as execution start, and do not alter immutable raw snapshots. This is a precision issue, not a changed merge-order conclusion.

### WP748-R23-F04 — P3 — Separate observed cancellation from inferred cause

**Location:** `ops/land/pr869-wp748-r22-land-evidence.yaml:45`.

**Scenario / evidence:** The `measured` sentence says the merge run was displaced by the next master push. The cited snapshots establish `cancelled`, `updated_at=01:15:23Z`, and zero checks, but no cancellation reason or cancelling actor. Local Git shows a following master merge `fdaad3f` at `01:15:18Z`; this supports a temporal correlation only. No retained event/log proves that push caused the cancellation.

**Fix:** Preserve the observed fields; describe the cause as an inference with its Git/time anchor, or mark cancellation cause/actor `not_measured`. A direct cancellation annotation/event would support a stronger claim. Verify that the revised wording cannot be read as a measured causal attribution; avoid inferring the cancelling actor from the run's initiating actor. No new test or credential use is needed.

## Coverage and conclusions

**Both `landed: false` values are justified.** Neither approving receipt contains a served-model field. `pr869` additionally has a cancelled merge gate, unexecuted mutant aggregation, and no retained durable exact-head land approval. The changed paragraphs do not currently certify assurance from the name “Codex” or `launcher.py`; F01 concerns the weaker future reopening recipe. A content verdict of `approve` is correctly kept distinct from reviewer assurance.

**`pr846` preserves history.** Parsing base and reviewed YAML yields exactly two changed value paths: `$.trang_thai_packet.landed` and `$.trang_thai_packet.landed_dieu_kien`. The old measured conditions remain an identical prefix; all other data are unchanged. The old `landed: true` claim and its owner-instruction anchor are retained as history. Five historical verdict hashes match the saved measurement file (5/5). The final review was after merge, as the retained timestamps show; this demotion does not rewrite that history into a pre-merge review.

| Claim group | Independent result |
| --- | --- |
| Both records' head/tree, merge/tree and parents | Match Git; r22 merge first parent is `807859b`, while retained PR base is `9e9a74b`; the record preserves that distinction. |
| r22 patch identity | Both compared patches are byte-identical, +537/-11 in `ops/nhanh_don_duoc_test.py`. |
| r22 CI and mutant attempts | 69/69 and 20/20 job objects accounted for; every one of the 89 jobs matches its check-run name, conclusion and head (89/89). Check-run snapshot contains 91/91 distinct checks including two other suites. |
| Run conclusions/times | r22 PR success updated 01:10:31Z before merge; mutant run failure is aggregation only; merge push cancelled. r846 PR 14/14, admission 1/1, merge push 14/14 success; reported run timestamps match. |
| r22 review history | Five receipts match the stated five heads, terminal status/rc and verdict sequence (5/5). Round 5 duration is 883.85 s; r846 final duration is 431.001 s. No served-model key in either final receipt; r846 has 35 top-level keys. |
| Prompt/verdict integrity | r22 prompt matches `run.json` (1/1), final verdict matches retained PR-comment hash (1/1); provenance manifest matches every non-manifest file (30/30), no omissions or duplicate entries. |
| Specs and leases | r23 spec hash matches; r22 frozen spec at `e0f91d0` matches `f3bb1f…`; r846 spec at `9d401ef` matches `a5a896…`. Lease IDs, write sets/hashes, expiry/shortening and saved holder-scan summaries agree with the records. Remote ref completeness is a retained historical scan claim, not freshly verified here. |
| r22 lease timing | All eight commits in `9e9a74b..b9318cc` have committer times before 19:00:08Z (8/8); final head matches PR snapshot. This establishes committed-history timing, not absence of uncommitted writes or validity of the author's clock. |
| Authority / actual human actor | GitHub snapshots establish account/event, not who operated credentials. Owner instructions and scope narrowing remain anchored declarations. No new exact-head land authorization is inferred from merge. |
| Reported reviewer tests and Windows | Totals match retained verdicts; they are `thuat_lai`, not tests rerun here. Native Windows remains unmeasured. |
| Reviews / comments | Both records' review and review-comment arrays are empty as claimed. Connector SHA/status/findings match retained comments; r22 completion is post-merge. |

Live GitHub state, current PR #882 CI, remote ref inventory, actual historical credential operator, actual served model/effort, and external launcher authenticity were not independently measured. No credentials or network retrieval were used. This report is an independent content review, not a replacement model-family or land-authorization receipt.

## Same-level records still marked landed — report only

These are outside the frozen write set. They should be considered for a separately authorized follow-up; no expansion or edits were made here. Each listed record explicitly declares its reviewer model unmeasured, has `landed: true`, and does not record a qualifying replacement human/model-family audit in its assurance justification:

| Record | `landed: true` line | Unmeasured model line / retained evidence |
| --- | ---: | --- |
| `ops/land/pr779-wp775-land-evidence.yaml` | 94 | 153; `verdict-luot17/run.json` has 35 keys, no model key, matching authorized head. |
| `ops/land/pr792-wp484-land-evidence.yaml` | 91 | 145; final review also predates head changes disclosed at line 121. |
| `ops/land/pr818-wp788-land-evidence.yaml` | 86 | 141; `verdict-luot5/run.json` has 34 keys, no model key, matching authorized head. |
| `ops/land/pr823-wp802-land-evidence.yaml` | 85 | 126; launcher review is reported at line 112. |
| `ops/land/pr832-wp831-land-evidence.yaml` | 86 | 124; `verdict-luot7/run.json` has 35 keys, no model key, matching authorized head. |
| `ops/land/pr836-wp812-land-evidence.yaml` | 86 | 131; no recorded assurance replacement. |
| `ops/land/pr848-wp744-land-evidence.yaml` | 80 | 112; `run-f65e544e.json` has 35 keys, no model key, matching authorized head. |
| `ops/land/pr849-wp748-land-evidence.yaml` | 90 | 113–114 and 129; CLI-requested model is explicitly distinguished from unmeasured served model. |
| `ops/land/pr862-wp748-r21-land-evidence.yaml` | 92 | 112 and 123; notably, the r21 source of the cited assurance issue is still true on this exact tree. |
| `ops/land/pr864-wp858-land-evidence.yaml` | 88 | 100 and 112; final launcher receipt has 36 keys, no model key, matching authorized head. |

Additionally, `pr791` (line 106), `pr793` (103), `pr800` (56) and `pr801` (56) retain true with offline CLI review receipts explicitly missing; these need the same follow-up assessment rather than assuming their tool names establish assurance. This is a screening result, not a full independent re-review of every historical packet. `pr765` and `pr778` were not grouped solely by their unknown model: they retain separate exact-SHA human-audit declarations in comments `6207001889` and `6245464876`.

## Final command results

All commands ran locally; Python/Git audit entries summarize the inline scripts executed during this review.

| Command / measurement | rc | Positive result / limit |
| --- | ---: | --- |
| `git -C src rev-parse HEAD HEAD^{tree}` | 0 | 2/2 supplied identities match. |
| `git -C src symbolic-ref -q HEAD` | 1 | Expected detached HEAD. |
| `git -C src show master:ops/specs/wp748-r23-don-so-assurance-81.md` | 128 | Absent; required local-ref fallback used. |
| `git -C src show origin/ops/wp748-r23-g23-lease:ops/specs/wp748-r23-don-so-assurance-81.md` + SHA-256 | 0 | 1/1 frozen spec hash matches. |
| `git -C src diff --name-status BASE HEAD` / write-set audit | 0 | 33/33 changed paths allowed; two commits. |
| `git -C src archive --format=tar HEAD --output=../review-scratch.4iOCXt/reviewed.tar` and `tar -xf ... -C review-scratch.4iOCXt/archive` | 0 | Reviewed tree extracted outside `src/`. `HEAD` here is the frozen reviewed OID. |
| `(cd review-scratch.4iOCXt/archive && python3 ops/land_evidence_nguon.py --root .)` | 0 | 21/21 checked pass, 28/28 exemptions match; total 49, violations 0, unknown 0. |
| `(cd src/ops/land/pr869-wp748-r22-provenance && sha256sum -c SHA256SUMS)` | 0 | 30/30 OK; independent coverage audit also 30/30. |
| `(cd src/ops/land/pr846-wp845-provenance && sha256sum -c SHA256SUMS)` | 0 | 36/36 OK; coverage 36/36, no omissions/duplicates. |
| Python JSON/job/check-run, hash and Git comparisons | 0 | Counts and outcomes detailed above; 89/89 job/check-run matches; 21/21 added JSON files parse. |
| Python added-file secret/EOL scan | 0 | 32/32 have no lone CR and no token/private-key pattern matches; 21/21 JSON files contain no nonempty secret-key fields. Scan summary saved at `review-scratch.4iOCXt/secret-eol-summary.json`. |
| `git -C src diff --check BASE HEAD` | 2 | 13 existing Markdown hard-break lines copied in provenance; reported, not rewritten. No lone CR. |

`BASE` = `747f983ccbcaf29a8e5228d09fd05b5a5ab6e479`; reviewed `HEAD` = `8f12e02856eb130160c40188470f7e5911ab1687`.

Final supplementary checks: r22 canonical write-set SHA-256 recomputed, 1/1 match (Python rc 0). Existing pr846 provenance checksums and coverage: 36/36, rc 0.

Final source check: `GIT_OPTIONAL_LOCKS=0 git -C src status --porcelain=v1` rc 0, empty output; HEAD/tree unchanged (2/2), still detached (`symbolic-ref` rc 1). No edits to `src/`, commits, pushes, GitHub comments, or credentials used.

UTC completion: 2026-10-23T01:42:48Z.

VERDICT: changes_requested
