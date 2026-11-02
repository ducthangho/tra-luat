# WP748 r23/g23 — PR #882 — independent review, round 2

Review class: sensitive. Status: complete; changes requested for the remaining part of F01.

Reviewer identity: runtime instructions identify this assistant as OpenAI Codex, based on GPT-6; the system reports an API interface. Observed execution surface/transport: local shell through `functions.exec` / `exec_command`. The user reports invocation through `launcher.py run`; no enclosing receipt or independently verifiable served-model identifier has been exposed to this session. Actual served model/family therefore remains `khong_do_duoc` for independent assurance; the tool name is not identity evidence.

UTC start: 2026-10-23 01:44:39 UTC.

Identity verified before substantive review:

- Reviewed SHA: `682c8880e493e9b4019e599482a33081fa35576f`.
- Tree: `15e043161156b5be9e9d496aab71ec10b3a7f3ae`.
- Base: `747f983ccbcaf29a8e5228d09fd05b5a5ab6e479`.
- Prior reviewed SHA: `8f12e02856eb130160c40188470f7e5911ab1687`.
- `git -C src rev-parse HEAD HEAD^{tree}`: rc 0, 2/2 expected identifiers.
- `git -C src symbolic-ref -q HEAD`: rc 1, detached as required.
- `git -C src status --short`: rc 0, clean.

Constraints: `src/` is read-only; no credentials, network retrieval, GitHub comments, commits or pushes. Scratch and this report only. Prior findings F01–F04 will each receive an explicit disposition with evidence.

## Incremental review log

Identity matches. Reading the frozen spec, protocol, both records and the round-2 delta; factual checks and required archive validation are pending.

Checkpoint 1:

- `master` spec lookup: rc 128 (`master` absent). Local `origin/ops/wp748-r23-g23-lease` fallback: rc 0. SHA-256 is exactly `6190ebbb943f1d017de32d9f316f85623906fded49379f4ce2540d957bee9584` (1/1); no fetch.
- Three commits since base; round-2 delta changes only the two land records. Historical provenance is unchanged since round 1.
- Scratch created with `mktemp -d ./review-r2.XXXXXX`: `review-r2.nu3SVu/`.
- `git -C src archive --format=tar 682c8880e493e9b4019e599482a33081fa35576f --output=<scratch>/reviewed.tar`: rc 0; `tar -xf ... -C <scratch>/archive`: rc 0.
- From that archive, `python3 ops/land_evidence_nguon.py --root .`: rc 0; 21/21 checked records pass, 28/28 exemptions match, 49/49 accounted for, zero violations/unknown. Log: `review-r2.nu3SVu/land-validator.log`. This validates source/schema conditions, not truth or assurance.
- `sha256sum -c SHA256SUMS` in r22 provenance: rc 0, 30/30 OK. In pr846 provenance: rc 0, 36/36 OK.

Semantic review and independent JSON/Git aggregation remain in progress.

Checkpoint 2:

- `python3 review-r2.nu3SVu/audit.py`: rc 0; log retained in `review-r2.nu3SVu/audit.log`. All 33/33 changed paths are allowed. Both head/tree and merge/tree identities (4/4), both merge parent lists (2/2), and PR snapshot identities match Git.
- r22 CI: 69/69 jobs accounted for; attempts 1 and 2 each have 20 successes and 3 failures, attempt 3 has 23/23 successes. The six earlier failed jobs have runner ID 0 and no steps. Mutant CI: 20/20 jobs, each attempt has 9 successes and one failed `dot-bien-gop`, also runner ID 0/no steps. All 89/89 jobs match their check-run name, conclusion and head; 91/91 unique check-run objects retained.
- pr846: PR CI 14/14 success, admission 1/1 success, merge CI 14/14 success. Reported API timestamps match. Final receipt has 35 keys and no model field; all five r22 receipts have 36 keys and no model field.
- r22 round-5 prompt matches its receipt SHA-256 (1/1): `3842bc9cc5159f1e76ad32c0faf2b838a900a34b322174c5e41ce797e86604b0`. Verdict hash matches the retained PR comment (1/1): `6a60f9c7cfb16a7292995c1d1325de32f0f94d3bf8166eb5505046ce0c4ba99b`.
- The two r22 patches are byte-identical, SHA-256 `bf5ffcf04ad41c25feb7922af8ec1c97ce78878c82ba4ec126290d73674edb83`: one file, +537/-11. Lease/spec hash matches Git object `e0f91d0`.
- pr846's YAML has exactly two changed value paths: `trang_thai_packet.landed` and `trang_thai_packet.landed_dieu_kien`. The prior measured conditions are an identical prefix; no historical measured values were rewritten. All five retained pr846 verdict hashes match their saved measurement files (5/5).
- `python3 review-r2.nu3SVu/scan.py`: rc 0. All 33/33 changed files, including 32/32 added files, have no lone CR and no matches across eight credential/private-key pattern families; 21/21 added JSON files parse and contain no nonempty secret-key fields. This is a static scan, not a proof against every possible secret encoding.
- `git -C src diff --check BASE HEAD`: rc 2, solely 13 Markdown hard-break/trailing-space lines in copied historical verdicts; no lone CR. Historical bytes were preserved.
- F02's equivalent-code shortcut is removed; F03's event times now match their exact sources; F04 now separates measured cancellation from unmeasured cause/actor. F01's machine-measured and human-audit alternatives are substantially repaired, but its standalone `khai_co_audit` alternative still omits the different-family requirement. Final disposition follows after remaining evidence/peer checks.

## Final finding

Threshold: zero P0/P1/P2. **Open findings: P0 0, P1 0, P2 1, P3 0.**

### WP748-R23-F01 — P2 — Still open: audited identity is not itself cross-family assurance

**Locations:** `ops/land/pr846-wp845-land-evidence.yaml:99`; `ops/land/pr869-wp748-r22-land-evidence.yaml:102`. The governing “one of three” alternatives start at lines 96 and 99 respectively.

**Scenario:** The new branch (ii) accepts a declaration of the approving review's model family on the exact head, a named auditor's durable confirmation, and a weaker-than-`do_may` disclosure. Consider a completed independent review on that head whose served family is **Claude**, with an auditor durably confirming that truthful declaration. It satisfies the stated branch (ii), although the executor is also Claude. It cannot supply the required `cross_approved` assurance. The auditor has confirmed identity, not necessarily performed the independent spec/diff audit required for `human_audited`.

**Evidence / rule:** `docs/PROTOCOL_DA_PHIEN.md:611` defines `khai_co_audit` as a strength of model-family evidence, not a third approval class; different served families are required for `cross_approved`. Both revised records put that comparison and completed-independent-review requirement explicitly inside branch (i), then introduce branch (ii) as a separate sufficient alternative. The general reference to §8 leaves this operational checklist internally incomplete. This is a residual of F01, not a new finding against the fixed machine-evidence branch. Current `landed: false` remains correct.

**Fix:** Make completed independent approval on the exact authorized SHA, with the actual executor/reviewer served families established as different for that approving run, a shared prerequisite of **both** `do_may` and `khai_co_audit`. Keep the named auditor's durable confirmation and weaker-evidence disclosure in the latter. Keep full exact-SHA `human_audited` as the separate alternative. Also remove the stray “(7)” in pr846's reopening sentence, which actually reopens its item (5). Do not rewrite historical receipts or interpret future launcher instrumentation as a retroactive measurement.

**Verification / regression:** Manual counterexample against both literal branch-(ii) texts: same-family declaration + exact head + named durable auditor + weaker-evidence disclosure meets the listed predicates but fails §8. After revision, reject this case, an audited declaration for another run/SHA, and an owner-only declaration. Accept an audited *different-family* pair only with the completed independent exact-SHA approval. No executable product test is warranted for this prose correction; `land_evidence_nguon` does not enforce assurance semantics. Preserve the valid audited-evidence path rather than accidentally requiring machine evidence for every review.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding | Round-2 disposition | Independently checked evidence |
| --- | --- | --- |
| F01 P2 | **Still open — VÁ HỜ (partial repair)** | Machine evidence is now bound to the approving run/exact head, different served family and independent completed approval; later instrumentation cannot repair past runs. Named audit confirmation and the full human-audit contract were added. The standalone audited-declaration alternative still lacks the resulting cross-family requirement, as detailed above. |
| F02 P2 | **Closed — ĐÃ VÁ THẬT** | `ops/land/pr869-wp748-r22-land-evidence.yaml:95` now requires a successful exact-merge gate and all four CI provenance dimensions. Code/tree equality is explicitly insufficient. A successor requires specific authorization, SHA/run/attempt, ancestry/scope, required contexts and disposition of the original cancellation. An equal-code run with a different/unproven workflow or missing required context no longer qualifies. Original run `39882625690` remains cancelled; zero merge checks remain recorded. |
| F03 P3 | **Closed — ĐÃ VÁ THẬT** | Record line 31 now matches `readback-events-869.json:30`: ready-for-review `01:10:26Z`. Line 42 separately identifies comment creation `01:10:37Z` and completion `01:12:41Z` (source precision `01:12:41.879488Z`); internal trigger time is `not_measured`. Both match the retained connector comment; completion remains after the `01:11:56Z` merge. |
| F04 P3 | **Closed — ĐÃ VÁ THẬT** | Record line 45 retains the API conclusion `cancelled`, `updated_at=01:15:23Z`, and zero checks, while explicitly marking cause/actor `not_measured`. Git commit `fdaad3f78ab8355495f40fdd91d330b3416c0887` has committer time `2026-10-23T08:15:18+07:00` = `01:15:18Z`; the text now labels this only temporal correlation. |

## Factual coverage and assurance

Both records correctly remain `landed: false`. Their approving launcher receipts contain no served-model field. Provider/surface/transport values identify what the receipt reports and cannot establish the reviewer family. No changed paragraph presently certifies assurance merely from “Codex” or `launcher.py`; the remaining problem is the future reopening alternative in F01. The r22 record additionally keeps its cancelled post-merge gate, unexecuted mutant aggregation and missing durable exact-head land approval unresolved. Owner approval and green `dot-bien-gop` remain explicit reopening conditions.

The factual checks found no remaining wrong count, event timestamp, hash or merge identity in the two records. Supporting coverage beyond the incremental log:

| Claim group | Result and evidence limits |
| --- | --- |
| Git identity / merge history | Both records' head/tree, merge/tree and parent lists match Git. r22 correctly distinguishes retained PR base `9e9a74b` from actual merge first parent `807859b`. pr846's merge and head have the same tree; its two write-set files are unchanged between `7a39463` and `974859d` (`git diff --exit-code`, rc 0). |
| CI counts / timing | r22 PR run attempt 3 success was updated `01:10:31Z`, before merge. Each mutant attempt has `dot-bien-du` plus eight successful shards and failed unexecuted aggregation. pr846's 29/29 job objects also match their check runs. Reported run heads/events/conclusions/times agree with the snapshots. These checks do not manufacture missing checkout/workflow/log provenance. |
| Snapshot coverage / checksum inventory | r22 30/30 and pr846 36/36 manifest entries cover every retained provenance file other than `SHA256SUMS`, with no missing or duplicate entries. The r22 successor snapshot has one pending main CI and one successful other workflow; it is not used as a green substitute for the cancelled merge CI. |
| Reviews / attribution | Five r22 receipts match the five stated heads, terminal status/rc and verdict sequence (5/5). Final duration is 883.85 s; pr846 final duration is 431.001 s. r22's 8/8, 56/56, 22/22 and 78/78 totals match the saved final verdict and are correctly `thuat_lai`, not tests rerun by this reviewer. Native Windows remains unmeasured. Both review and review-comment arrays are empty as stated. |
| Spec / lease | r22 spec hash matches Git object `e0f91d0`; its canonical compact-JSON write-set hash matches (1/1). pr846 spec hash matches Git objects `9d401ef` and `12e1885`; its shortened lease snapshot matches `41a72cb` byte-for-byte. r22's expiry/heartbeat values match the retained lease. Historical holder-scan files support the quoted 548/548 and 530/530 counts and zero holders; no live ref inventory was fetched. |
| Authority / bookkeeping | Retained comments support the recorded owner instructions as declarations. REST establishes the account, not the person or credential operator; those limitations are retained. r22's retained comments/events do not supply the missing durable exact-head land approval. pr846 issue snapshot is closed/completed at `2026-10-19T09:28:18Z` by the stated account. |
| Historical preservation | pr846's unchanged measured fields and prior `landed: true` owner-instruction anchor remain available. Its fifth review began at `09:38:39Z`, after the `08:55:29Z` merge; demotion does not turn it into a pre-merge review. The old `pre_merge_checks` grouping is inherited historical organization, not newly verified chronology. |

## Same-evidence records still marked landed — report only

The packet covers exactly its frozen write set, but it does **not** remove this evidence-level inconsistency across the tree. The following retained records still have `landed: true` and identify no qualifying replacement assurance in the reviewed justification. They warrant separately authorized follow-up; no scope expansion or edits were made.

| Record under `ops/land/` | True at line | Evidence of the same assurance gap |
| --- | ---: | --- |
| `pr679-wp678-land-evidence.yaml` | 67 | Lines 174–179 claim `cross_approved` and explicitly deny a human audit. `ops/reviews/wp678-spec-review-6-codex-verdict.receipt.yaml:57` says the served model is unmeasured; lines 53–56 say the launcher evidence is reported rather than retained. Additional report-only candidate found this round. |
| `pr779-wp775-land-evidence.yaml` | 94 | Line 153; exact-head `verdict-luot17/run.json` has 35 keys and no model key. |
| `pr792-wp484-land-evidence.yaml` | 91 | Line 145 explicitly says actual model unmeasured; line 121 also discloses later head changes. |
| `pr818-wp788-land-evidence.yaml` | 86 | Line 141; exact-head `verdict-luot5/run.json` has 34 keys and no model key. |
| `pr823-wp802-land-evidence.yaml` | 85 | Line 126 declares actual model unmeasured. |
| `pr832-wp831-land-evidence.yaml` | 86 | Line 124; exact-head `verdict-luot7/run.json` has 35 keys and no model key. |
| `pr836-wp812-land-evidence.yaml` | 86 | Line 131 declares actual model unmeasured. |
| `pr848-wp744-land-evidence.yaml` | 80 | Line 112; exact-head `run-f65e544e.json` has 35 keys and no model key. |
| `pr849-wp748-land-evidence.yaml` | 90 | Lines 113–114 and 129 distinguish CLI-requested model from unmeasured served model. |
| `pr862-wp748-r21-land-evidence.yaml` | 92 | Lines 112 and 123 explicitly leave the served model unmeasured, including the r21 source of this packet's rationale. |
| `pr864-wp858-land-evidence.yaml` | 88 | Lines 100 and 112; exact-head final receipt has 36 keys and no model key. |

Also still true: `pr791:106`, `pr793:103`, `pr800:56`, `pr801:56`; their review sections (`:135`, `:131`, `:66`, `:70`) explicitly lack retained offline review receipts. These are screening candidates, not full re-reviews of those packets. `pr765` and `pr778` retain separate exact-SHA human-audit declarations and were not grouped solely because their model was unknown.

## Command results and limits

Commands are local. `BASE` and `HEAD` below are the full immutable OIDs specified above.

| Command / measurement | rc | Result |
| --- | ---: | --- |
| `git -C src rev-parse HEAD HEAD^{tree}` | 0 | 2/2 supplied identifiers match. |
| `git -C src symbolic-ref -q HEAD` | 1 | Expected detached state. |
| `git -C src show master:ops/specs/wp748-r23-don-so-assurance-81.md` | 128 | Local `master` absent. |
| Local origin-branch spec fallback + SHA-256 | 0 | 1/1 frozen hash matches. |
| `git -C src archive --format=tar HEAD --output=<scratch>/reviewed.tar`; `tar -xf ... -C <scratch>/archive` | 0 / 0 | Exact reviewed tree extracted outside `src/`. |
| `(cd review-r2.nu3SVu/archive && python3 ops/land_evidence_nguon.py --root .)` | 0 | 21/21 pass; 28/28 exemptions; 49/49 accounted for; zero violations/unknown. |
| `(cd src/ops/land/pr869-wp748-r22-provenance && sha256sum -c SHA256SUMS)` | 0 | 30/30 OK. |
| `(cd src/ops/land/pr846-wp845-provenance && sha256sum -c SHA256SUMS)` | 0 | 36/36 OK. |
| `python3 review-r2.nu3SVu/audit.py` | 0 | 33/33 paths allowed; Git/JSON/hash comparisons recorded above. |
| Supplemental Python/Git comparisons | 0 | pr846 29/29 job/check matches; 5/5 verdict hashes; 2/2 spec hashes; 1/1 r22 write-set hash. The missing pr846 branch lookup (128) was resolved through its retained commit OIDs. The r22 spec commit does not contain its later lease (lookup 128); lease facts use the retained snapshot. |
| `python3 review-r2.nu3SVu/scan.py` | 0 | 33/33 changed files, including 32/32 additions, free of lone CR and scanned secret patterns; 21/21 JSON files parse, no nonempty secret-key fields. |
| `git -C src diff --check BASE HEAD` | 2 | 13 retained Markdown hard-break lines in historical provenance; no source edits made. |

This is a content review of the frozen Git tree and retained evidence. Live GitHub state/current PR #882 CI, remote inventory, actual historical credential operator, actual served model/effort and external launcher authenticity were not independently measured. No credentials or network retrieval were used. This verdict is not a model-family attestation or land authorization.

Final source verification: HEAD/tree unchanged (2/2, rc 0); still detached (`symbolic-ref` rc 1); `GIT_OPTIONAL_LOCKS=0 git -C src status --porcelain=v1` rc 0 with empty output. Round-2-only `git diff --check 8f12e02856eb130160c40188470f7e5911ab1687 682c8880e493e9b4019e599482a33081fa35576f` rc 0. No edits to `src/`, commits, pushes, GitHub comments or credential use.

UTC completion: 2026-10-23 01:52:42 UTC.

VERDICT: changes_requested
