# Independent review — WP748 r23/g23, PR #882, round 3

Review Class: sensitive. Review complete; incrementally recorded below. Content verdict: approve.

Reviewer identity: OpenAI Codex, as identified by the session instructions. The session describes the agent as based on GPT-6, but exposes no independently verifiable served-model receipt, exact model version, or model-family attestation. The launcher invocation is stated by the requester; its execution receipt has not yet been independently checked. Tool/product names do not establish reviewer model family (`khong_do_duoc` unless measured runtime evidence is found).

Identity gate passed: `src/` HEAD is detached at `bab8702692f1d723ac1a84b865660597aa6291e6`; tree `8568aa04e0dfa1dbd014e7b4a3ebd215cb40b522`. Base: `747f983ccbcaf29a8e5228d09fd05b5a5ab6e479`.

Scope: read-only inspection of the requested delta and provenance; no source edits, commits, pushes, GitHub comments, credentials, or network access. Scratch and this verdict are the only intended writes.

Initial commands: `git -C src rev-parse --verify HEAD`, `git -C src rev-parse 'HEAD^{tree}'`: rc 0, exact identity match. `git -C src symbolic-ref -q HEAD`: rc 1, confirming detached HEAD (wrapper rc 0).

Findings and checks: completed in the checkpoints and final disposition below.

UTC start: 2026-10-23T01:54:49Z.
Scratch: `review-r3.67osjs5a`.

## Checkpoint 1 — frozen scope and mechanical checks

- Local `master` spec lookup: rc 128. Local `origin/ops/wp748-r23-g23-lease` fallback: rc 0. Frozen spec SHA-256 matches `6190ebbb943f1d017de32d9f316f85623906fded49379f4ce2540d957bee9584` (1/1). No fetch/network.
- Four commits since the supplied base. The round-3 delta changes only the reopening paragraphs in the two permitted records.
- `git archive` of reviewed SHA and extraction into `review-r3.67osjs5a/archive`: rc 0 / 0.
- From the archive: `python3 ops/land_evidence_nguon.py --root .`: rc 0; 21/21 checked records pass; 28/28 cutover exemptions match; 49/49 accounted for; zero violations or unknown. Log: `review-r3.67osjs5a/land-validator.log`. This checker does not prove factual truth or reviewer assurance.
- `sha256sum -c SHA256SUMS` in r22 provenance: rc 0, 30/30 OK. In pr846 provenance: rc 0, 36/36 OK.
- F01's common prerequisite now explicitly covers both `do_may` and `khai_co_audit`; detailed negative-case review and F02–F04 regression verification follow below.

## Checkpoint 2 — independent factual audit

- `python3 review-r3.67osjs5a/audit.py`: final rc 0; detailed comparisons in `audit.log`. All 33/33 changed paths are allowed; 32 additions. Both head/merge trees (4/4) and parent lists (2/2) match Git and PR snapshots. Manifest inventories are complete and unique (30/30 and 36/36).
- r22 CI has 69/69 jobs: attempts 1 and 2 each 20 success + 3 failure; attempt 3 is 23/23 success. Mutant CI has 20/20 jobs: each attempt 9 success + 1 failed `dot-bien-gop`. All eight failed job objects have runner ID 0 and zero steps. All 89/89 job/check-run identities match; head snapshot retains 91 checks. pr846 has 14/14 PR, 1/1 admission and 14/14 merge successes, with 29/29 job/check matches.
- r22 final prompt SHA-256 matches its receipt (1/1); final verdict SHA-256 matches the retained PR comment (1/1). All five r22 terminal receipts match the five review heads/verdicts. All ten retained receipts across the two packets lack a model key (recursive inspection); final durations are 883.85 s and 431.001 s.
- r22 patches `9e9a74b..b9318cc` and `7400df4^1..7400df4` are byte-identical, SHA-256 `bf5ffcf04ad41c25feb7922af8ec1c97ce78878c82ba4ec126290d73674edb83`, one file +537/-11. Spec and write-set hashes match. pr846 spec hashes, five verdict hashes and shortened lease match their retained/Git anchors.
- pr846 changes exactly two YAML value paths: `trang_thai_packet.landed` and `trang_thai_packet.landed_dieu_kien`. The historical measured conditions (1)–(4) remain an identical prefix; the old true-state/owner-instruction claim is retained explicitly as history. The first audit-script attempt incorrectly compared the entire old paragraph, including the superseded true-state conclusion, and exited 1; corrected to compare the measured prefix, then passed. Initial output retained in `audit-initial.log`.
- `python3 review-r3.67osjs5a/scan.py`: rc 0; 33/33 changed files (32/32 added) free of lone CR and matches for eight credential/private-key pattern families. 21/21 added JSON files parse and have no nonempty credential-key fields. Static pattern coverage is not proof against arbitrary secret encodings.
- Plain `git diff --check BASE HEAD`: rc 2, 13 Markdown hard-break/trailing-space lines in unchanged historical verdict bytes. Round-3-only `git diff --check 682c888... bab8702...`: rc 0. No provenance bytes were rewritten.

## Final finding disposition

**Open in-scope findings: P0 0, P1 0, P2 0, P3 0.** Applied threshold: zero P0/P1/P2, as explicitly requested. The result is a content verdict on this frozen packet; it does not attest this reviewer's served model family or authorize land.

### WP748-R23-F01 — P2 — CLOSED / ĐÃ VÁ THẬT

Class: `cross-family-assurance-contract`. Locations: `ops/land/pr846-wp845-land-evidence.yaml:96` and `ops/land/pr869-wp748-r22-land-evidence.yaml:99`.

**Previous scenario:** An exact-head independent reviewer served by the same Claude family as the Executor, with a named auditor confirming its identity and a weaker-evidence disclosure, could satisfy the standalone `khai_co_audit` alternative despite not supplying `cross_approved`.

**Fix verified:** Both records now place a completed independent exact-SHA approval and a different served reviewer family under the common prerequisite for (A) `cross_approved`. Machine measurement and audited declaration are only alternative strengths of evidence for that same approving run. Both explicitly reject same-family assurance even with an auditor. `khai_co_audit` retains named durable auditor confirmation and the weaker-than-`do_may` disclosure. (B) separately retains the full §8 human-audit contract: independent auditor, durable identity, personal spec/diff review, durable evidence/verdict on the exact head. pr846's stray item `(7)` is corrected to `(5)`.

**Manual semantic checks against both texts, 6/6:** (1) same-family measurement rejected; (2) same-family audited declaration rejected; (3) evidence for another run/SHA rejected; (4) owner-only declaration without auditor rejected; (5) a completed independent exact-head different-family approval with properly audited identity remains permitted; (6) a full independent exact-head human audit remains permitted. These are textual counterexample checks, not tests purporting to prove actual model identity. A future launcher upgrade still cannot retroactively measure an old run. This meets `docs/PROTOCOL_DA_PHIEN.md:611`, `:612`, and `:764` for the reopening instructions. No remaining same-mechanism bypass found in either changed paragraph.

### Prior findings F02–F04 — all remain CLOSED / ĐÃ VÁ THẬT

| ID / prior severity / class | Location | Scenario, fix and independently rechecked evidence |
| --- | --- | --- |
| WP748-R23-F02 / P2 / `ci-provenance-substitution` | `ops/land/pr869-wp748-r22-land-evidence.yaml:95` | Equal product code alone must not replace the cancelled merge gate. The text still requires successful exact-merge CI with run, checkout, workflow-definition and output provenance. A successor requires explicit SHA/run/attempt authorization, ancestry/scope comparison, required contexts and disposition of the original cancellation. Equal code with an unproven workflow or missing required context remains insufficient. `readback-run-39882625690.json:12` remains `cancelled`; `readback-check-runs-7400df4-all.json:2` remains zero. No regression. |
| WP748-R23-F03 / P3 / `event-time-label` | `ops/land/pr869-wp748-r22-land-evidence.yaml:31` and `:42` | Ready-for-review matches `readback-events-869.json:30`, `01:10:26Z`. Connector comment creation matches `readback-comments-869.json:485`, `01:10:37Z`; completion matches its body at `:487`, `01:12:41.879488Z` (record displays whole seconds). Internal trigger time remains `not_measured`; creation is not mislabeled as execution start. Completion remains after merge at `01:11:56Z`. No regression. |
| WP748-R23-F04 / P3 / `observed-vs-inferred-cause` | `ops/land/pr869-wp748-r22-land-evidence.yaml:45` | Observed cancellation must not become a measured causal attribution. API conclusion/updated time remain `cancelled` / `01:15:23Z` (`readback-run-39882625690.json:12`, `:22`). Cause and cancelling actor remain `not_measured`. Git successor `fdaad3f78ab8355495f40fdd91d330b3416c0887` is timestamped `2026-10-23T08:15:18+07:00` = `01:15:18Z`; the record explicitly treats this as correlation only. No regression. |

Four prior finding classes, four prior findings, zero open in this packet. Historical P2 debts declared in the r22 record are not asserted fixed by this bookkeeping change.

## Factual claims, labels and land conditions

No remaining false count, timestamp, hash or Git identity was found in the two records. The independent aggregation above was checked against the actual cited files, rather than relying on the source-existence validator or prior verdicts.

| Claim group | Result / evidence boundary |
| --- | --- |
| Merge and patch history | Both records' full head/tree and merge/tree identities and both parent lists match Git. r22 correctly distinguishes snapshot PR base `9e9a74b` from merge first parent `807859b`. Its two patches are byte-identical, +537/-11. pr846's write-set files are unchanged between `7a39463` and `974859d`. |
| CI facts and chronology | r22's 23/23-success attempt was updated `01:10:31Z`, before merge `01:11:56Z`. Earlier attempts have three failed jobs each, not four; mutant aggregation failed in both attempts with no runner/steps. The frozen spec's stale description of jobs still failing at merge is not repeated as a current measured claim in the record. Merge push remains cancelled; the successor snapshot has pending main CI and a successful separate workflow, not a proven replacement gate. pr846's 14/14, 1/1 and 14/14 results and reported times match snapshots. API results do not independently supply missing checkout/workflow/log provenance. |
| Reviews and labels | Five r22 receipt heads and terminal states agree with their verdict files: four `changes_requested`, then `approve`. Final reported 8/8, 56/56, 22/22 and 78/78 totals match the retained round-5 verdict; these are correctly `thuat_lai`, not tests rerun in this review. Windows native remains unmeasured. Both packets have empty review/review-comment arrays. Product/tool names in review-entry titles do not confer assurance; the operative text explicitly denies that inference. |
| Prompt / verdict binding | r22 prompt SHA-256 is `3842bc9cc5159f1e76ad32c0faf2b838a900a34b322174c5e41ce797e86604b0`, equal to receipt `prompt_sha256`; final verdict hash is `6a60f9c7cfb16a7292995c1d1325de32f0f94d3bf8166eb5505046ce0c4ba99b`, equal to the retained PR comment. Manifest hashes prove retained-byte integrity, not independent authenticity of historical runtime execution. |
| Lease, spec, authority | r22 spec matches Git `e0f91d0`; canonical compact-JSON write-set hash, expiry `19:00:08Z`, heartbeat `07:00:08Z` and head commit time `10:49:41Z` match. pr846 specs at `9d401ef` / `12e1885`, five verdict hashes and shortened lease at `41a72cb` match. Holder-scan files retain 548/548 and 530/530 inventory summaries and zero-holder results; no live inventory was fetched. Recorded owner instructions are supported as anchored declarations. REST identifies accounts, not the human or credential operator. r22 retains the absence of durable exact-head land approval. |
| pr846 history | Only the two YAML value paths reported above change. Measured conditions (1)–(4), all other fields, and prior verdict/provenance bytes remain intact; the superseded `landed: true` conclusion is expressly historical. Issue #845 is closed/completed at `2026-10-19T09:28:18Z` in its snapshot. The fifth review began `09:38:39Z`, after the `08:55:29Z` merge; inherited `pre_merge_checks` organization is not evidence that it ran before merge. This demotion does not rewrite chronology. |

**Both `landed: false` values are correctly justified.** The approving receipts contain no served-model field: 35 top-level keys for `run-964888d9.json`, 36 for `run-76825653.json`; recursive inspection finds no model keys. They do not establish the required reviewer-family assurance under §8/§8.1. The r22 record also explicitly leaves the cancelled merge gate, unexecuted mutant aggregation, and absent durable exact-head authorization unresolved.

The reopening conditions now cover those outstanding requirements: qualifying exact-head cross-family or human-audit assurance for both records; additionally r22 requires the merge gate (or a specifically authorized substitute with complete provenance), owner approval on `b9318cc`, and successful `dot-bien-gop` on that head. These are future obligations, not evidence already obtained. Nothing in the operative diff certifies assurance from “Codex”, `codex_cli` or `launcher.py` alone. The raw lease's requested reviewer-family configuration is historical configuration, not a measurement.

## Same-evidence records still `landed: true` — report only

The packet fixes exactly its frozen write set; it does not make assurance treatment uniform across the whole tree. The following records retain the same reviewer-identity gap without a qualifying replacement audit identified in the inspected justification. They warrant separate authorized follow-up; these are not additional in-scope findings or requests to expand this PR.

| Record under `ops/land/` | `landed: true` line | Evidence of the gap |
| --- | ---: | --- |
| `pr679-wp678-land-evidence.yaml` | 67 | `:174` claims `cross_approved`; `:177` expressly denies a human-audit verdict. `ops/reviews/wp678-spec-review-6-codex-verdict.receipt.yaml:53` says launcher evidence is only reported, and `:57` leaves the served model unmeasured. |
| `pr779-wp775-land-evidence.yaml` | 94 | `:153`; final `verdict-luot17/run.json` has 35 keys, no model key, and head `f9d84d7`. |
| `pr792-wp484-land-evidence.yaml` | 91 | `:145` explicitly says served model unmeasured; `:121` also discloses later head changes. |
| `pr818-wp788-land-evidence.yaml` | 86 | `:133` distinguishes CLI header from per-request measurement; `:141` declares the gap. Exact-head `verdict-luot5/run.json` has 34 keys, no model key. |
| `pr823-wp802-land-evidence.yaml` | 85 | `:126` declares actual model unmeasured. |
| `pr832-wp831-land-evidence.yaml` | 86 | `:124`; exact-head `verdict-luot7/run.json` has 35 keys, no model key. |
| `pr836-wp812-land-evidence.yaml` | 86 | `:131` declares actual model unmeasured. |
| `pr848-wp744-land-evidence.yaml` | 80 | `:112`; exact-head `verdicts/run-f65e544e.json` has 35 keys, no model key. |
| `pr849-wp748-land-evidence.yaml` | 90 | `:113`–`:114` distinguish CLI-requested identity; `:129` leaves actual served model unmeasured. |
| `pr862-wp748-r21-land-evidence.yaml` | 92 | `:112` and `:123` leave actual served model unmeasured; this is the r21 source of the packet's rationale. |
| `pr864-wp858-land-evidence.yaml` | 88 | `:100` and `:112`; final receipt has 36 keys, no model key, head `521efeb`. |

Additional screening candidates: `pr791-wp782-land-evidence.yaml:106`, `pr793-wp784-land-evidence.yaml:103`, `pr800-wp794-land-evidence.yaml:56`, `pr801-wp795-land-evidence.yaml:56`; their review sections at `:135`, `:131`, `:66`, `:70` respectively disclaim retained offline review receipts. This is not a full re-review of those packets. `pr765` and `pr778` have separate retained exact-head human-audit declarations (comments 6207001889 and 6245464876) and were not grouped solely on unknown model identity.

## Additional gate and final verification

`python3 review-r3.67osjs5a/kiem_re_local.py`: rc 0, `kiem-re DAT (33 tep doi, 0 loi)` — 33/33 paths. This runs the actual cheap gate in the archive with scratch-only Git metadata and read access to source Git objects. It includes the gate's three lease/receipt data cases. Inputs are explicitly a **local simulation**: event `pull_request`, base = reviewed base, head = reviewed SHA, merge-tree input = reviewed SHA. It is not a measurement of GitHub's real PR #882 merge ref or CI. No new commit was made. Log: `review-r3.67osjs5a/kiem-re-local.log`.

The cheap gate uses its documented whitespace policy; therefore the 13 retained Markdown hard-break lines flagged by plain `git diff --check` do not make this gate fail. No historical bytes were modified to silence those warnings.

Command receipt summary (immutable `BASE` and `HEAD` are the full OIDs at the top):

| Command | rc | Result |
| --- | ---: | --- |
| `git -C src rev-parse HEAD 'HEAD^{tree}'` | 0 | 2/2 identity match, initially and finally. |
| `git -C src symbolic-ref -q HEAD` | 1 | Expected detached HEAD, initially and finally. |
| `git -C src show master:<spec>` / local origin-branch fallback | 128 / 0 | Frozen spec hash 1/1 matches. |
| `git -C src archive --format=tar HEAD --output=<scratch>/reviewed.tar`; `tar -xf ...` | 0 / 0 | Exact reviewed tree copied outside `src/`. |
| `(cd review-r3.67osjs5a/archive && python3 ops/land_evidence_nguon.py --root .)` | 0 | 21/21 pass + 28/28 matching exemptions = 49/49 accounted for; zero violations/unknown. |
| `(cd src/ops/land/pr869-wp748-r22-provenance && sha256sum -c SHA256SUMS)` | 0 | 30/30 OK. |
| `(cd src/ops/land/pr846-wp845-provenance && sha256sum -c SHA256SUMS)` | 0 | 36/36 OK. |
| `python3 review-r3.67osjs5a/audit.py` | 0 final; 1 initial | Initial reviewer-script overbroad prefix assertion corrected as documented above; all final comparisons pass. |
| `python3 review-r3.67osjs5a/scan.py` | 0 | 33/33 changed, 32/32 added, 21/21 JSON; no detected secret patterns or lone CR. |
| `python3 review-r3.67osjs5a/kiem_re_local.py` | 0 | Local simulation 33/33 paths, zero errors; three data cases included. |
| `git -C src diff --check BASE HEAD` | 2 | 13 historical Markdown hard-break lines; no lone CR. |
| `git -C src diff --check 682c8880e493e9b4019e599482a33081fa35576f HEAD` | 0 | Round-3 delta clean. |
| `GIT_OPTIONAL_LOCKS=0 git -C src status --porcelain=v1 --untracked-files=all --ignored` | 0 | Empty output; no tracked, untracked or ignored changes observed at final check. |
| `GIT_OPTIONAL_LOCKS=0 git -C src diff --exit-code`; `git -C src diff --cached --exit-code` | 0 / 0 | Working tree and index clean. |

Reviewer identity clarification: runtime instructions identify OpenAI Codex based on GPT-6; the system reports an API interface. Observed execution is local shell via `functions.exec` / `exec_command`. The user reports `launcher.py run`; this session has no independently verified enclosing terminal receipt or served-model/effort attestation. Actual served model family remains `khong_do_duoc` for independent assurance. The current `launcher.err` was empty when inspected; that is not identity evidence.

Limits: live GitHub state, current PR #882 required CI/merge-ref, remote inventory, historical credential operator, actual served models, and external authenticity of copied launcher/API evidence were not independently measured. This review checks retained facts and Git consistency. Final clean snapshots do not prove that no outside process ever wrote and restored a file between snapshots. No credentials, network, GitHub writes, source edits, commits or pushes were used by this review. `src/` remains at the requested SHA/tree.

UTC completion: 2026-10-23T02:03:04Z.

VERDICT: approve
