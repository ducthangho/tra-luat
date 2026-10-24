Independent read-only review — WP748 r24/g24, PR #894, round 1. Review Class: sensitive.

Reviewed SHA: `d42713cc621cbd78d324a8b212749ff5c6199d1e`.
Reviewed tree: `e545a9f95b2c945aa1588a21bd3038f9fb86f618`.
Base: `1d7e642092fb3dda15967be44d095f37bb22ac5f`.
Review started 2026-10-23T13:25Z; completed UTC: 2026-10-23T13:38:09.306505+00:00.

Reviewer identity: OpenAI Codex. Runtime instructions describe this agent as GPT-6-based; that is an instruction-level identity claim, not a machine measurement of the model serving individual requests. Exact served model, effort, and provider-side routing are not exposed for independent verification. Observed execution: this API/tool session can invoke a local Bash/Python/Git executor. `launcher.py run` invocation is stated by the user; the enclosing launcher's final run.json/child rc is not available inside this review. Do not infer `cross_approved` from this verdict or the Codex tool name alone. No executor context or subagents were used.

Identity passed at entry and exit: exact SHA/tree, detached HEAD (`symbolic-ref -q HEAD` rc 1), clean index/worktree. Spec lookup on `master` failed because that local ref is absent (rc 128). The specified fallback ref supplied spec bytes with SHA-256 `b139d8972f9f5ba6fcd3be35686de552f441b79cdb0267c1016ea83ce286fda2`, exactly the required identifier. Lease r24/g24 has the same spec hash and base and the stated 18-path write set. The user's explicit pr621/pr696/pr721 deferral governs this review. No credentials, network access, GitHub writes, commits, pushes, or source edits were used.

Disposition: changes requested. In-scope findings: P0 0, P1 0, P2 1, P3 3. All 15 demotions themselves are justified by the stored evidence; no wrongly demoted record was found. The blocker is an incorrect new historical review-outcome assertion, not the decision to set landed false.

**F01 — P2 — `ops/land/pr836-wp812-land-evidence.yaml:146`: a failed launcher attempt is described as a completed changes_requested review.**

Scenario: the new `ly_do` says the launcher rounds “deu changes_requested”. Round 6 is included in the six cited run receipts, but `ops/land/pr836-wp812-provenance/verdict/wp812-r2-g3-exec-review-6-codex/run.json:14` records `ma_thoat: 1`, and that directory has no VERDICT.md. The unchanged record explicitly says “KHONG verdict” at :117 and :132. Thus the appended correction misstates the execution evidence and contradicts the retained facts. Protocol §8.1 distinguishes an execution failure/no verdict from a completed review. This matters in a packet whose deliverable is a truthful assurance ledger, even though both outcomes fail to supply approval.

Fix: change only the appended explanation to say that completed offline reviews requested changes, round 6 failed without a verdict, and the final exact-head approval came from the connector with unmeasured served-model family. Preserve landed false. Executed counterexample: rc 0, 2/2 assertions (`ma_thoat == 1`, VERDICT.md absent); saved in `review-scratch.39EBEQ/F01-counterexample.json`. The underlying historical launcher rc is 1, not 0.

**F02 — P3 — `ops/land/pr672-wp574-land-evidence.yaml:176` and `ops/land/pr679-wp678-land-evidence.yaml:569`: incomplete line anchors.**

Scenario: pr672's new :56 citation selects only `- pr: 672`; the actual authorized/merged head is at :58. The same wrong :56 appears inside the new :172 explanation. Its human audit's reviewed SHA is most directly supported by :63. For pr679, receipt :50–57 ends on the `KHONG_do_duoc: >-` key; the actual served-model limitation is at :58.

Fix: use pr672 :58 (and :63 for the human-audit claim); extend pr679's receipt range through :58. All 48 citation occurrences / 32 unique targets were inspected at post-edit line numbers. The other references point to the claimed content; these two unique targets need precision fixes. The underlying demotion evidence exists immediately nearby.

**F03 — P3 — `ops/land/pr672-wp574-land-evidence.yaml:179`: distinguish audit approval from land authorization.**

Scenario: the extra-gap text says “SHA duoc duyet (76f199e) khac merged head (a602a38)”. That is correct for the human audit, but misleading as a statement about the final land authorization: :71 records amendment 5 authorizing merge specifically on a602a38, and :58/:88 agree. The gap is the old human-reviewed SHA and absent full audit body, not evidence that the final merge ignored its authorized head.

Fix: explicitly call 76f199e the human-audited/reviewed head and acknowledge that a602a38 is the final recorded authorized land head. Reopening should require adequate exact-head review; it should not demand repairing a nonexistent difference between the final recorded land authorization and the merge.

**F04 — P3 — `ops/land/pr779-wp775-land-evidence.yaml:171` (same wording in seven other records): key-count scope is unstated.**

Scenario: the advertised 34/35/36/37 counts are correct for top-level keys, but are not recursive totals. Counting every mapping-key occurrence through nested objects/lists yields the totals below, always 12 higher. Crucially, the claim of zero model-bearing keys remains true at every depth in all 17 receipts; there is no hidden model evidence that rescues these records.

Fix: label the numbers “top-level keys” and explicitly say the model-key search is recursive, or report the recursive totals. Other locations: pr792 :166, pr818 :160, pr832 :143, pr836 :150, pr848 :130, pr864 :130, pr873 :134. Update duplicated counts in `ly_do` consistently. This is a measurement-scope clarification, not a claim that the existing top-level arithmetic is wrong.

The per-record evidence assessment follows. Every head in this table matches the actual Git merge's second parent (15/15); primary stored PR readbacks also match wherever available (13/13). This verifies the selected merged-head anchor, not that every old authorization has independently adequate human provenance.

| Record | Full authorized/merged head in new block | Demotion and extra-gap assessment |
|---|---|---|
| pr672 | `a602a380a5d6bee8771876fd7066bddf15e0be67` | Justified: human audit is on 76f199e, not this head; full comment absent. Final land authorization already names a602a38; see F02/F03. |
| pr679 | `03a7219c9f3df4e6304f499b79df968aa7d386cb` | Justified: receipt explicitly limits model identity to requested/header claims; no raw run/stderr retained. Stored authorization says a separate human audit was not posted. |
| pr779 | `f9d84d70fb46540bbecfae963c9afb4a2b48984d` | Justified: final launcher receipt and connector do not establish served family; final receipt head matches. |
| pr791 | `1bcbaa0b564612b3072c7c6e8e884e18782a0745` | Justified: connector evidence has no model; CLI rounds only narrated, receipts absent. Extra missing-receipt claim matches :137. |
| pr792 | `288ad3ea79ef94e061b649effe7bee2c7e2a0a9b` | Justified: receipt has no model and reviews 907214d. Extra unreviewed delta is real: launcher_test.py +18/-3 at merged head, matching :133–136. |
| pr793 | `1b375dbab5f4fe2694c7e12bbf159dd1c7c53828` | Justified: connector evidence has no model; CLI receipts absent as recorded at :133. |
| pr800 | `c679d645cafe5e4e0fbf4e782cfb0f3547759bca` | Justified: stored review is connector-only; no CLI receipt found. The extra-gap statement does not prove that a CLI review ever occurred. |
| pr801 | `76014ce0e76df70d8d3655b8f130747ae4d2cc14` | Justified: stored review is connector-only; no CLI receipt found. Same limitation as pr800. |
| pr818 | `984032f375aa0c8fe6039dfd35f6842acd49c926` | Justified: five receipts have no model keys; final receipt matches head. :135/:143 explicitly limit CLI-header identity. |
| pr823 | `5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456` | Justified: launcher run b3d8a108 is narrated, raw run.json absent; connector index supplies no served family. Exact merge dfe5437 gate is failure; green 6842a62 is a descendant. |
| pr832 | `51ae5c095972611d2c6045bd81786a4fc7e9ca62` | Justified: final receipt has no model and matches head. Connector at 6376cd3 is stale; :42 explicitly records that distinction. |
| pr836 | `d7b42d26f09dad0599dc0434dfad25b3897f3e51` | Justified: final connector approval has no served family. Exact merge f1979a5 gate is failure; green 6842a62/062292b are descendants. Correct failed round 6 per F01. |
| pr848 | `23bc189f28ea60f04ca1634b6fe66d02babf12ed` | Justified: final receipt has no model and matches head; connector provides no independent served-family evidence. |
| pr864 | `521efebab226fe3a92b2ccce4a59c27dd638edff` | Justified: receipt has no model and matches head. Final verdict is changes_requested, with owner-disposed P2s, exactly as extra-gap text says; disposition is not a new approve verdict. |
| pr873 | `f07f88c75cabbef691c86ac8746317a6c0705162` | Justified: final receipt has no model and matches head; no sufficient alternative human audit was found in stored evidence. |

All nine `do_duoc` fields were checked: eight records cite run JSONs, and pr679 cites the stored v2 receipt. pr679's limitation and missing raw-run claim are supported. Recursive counts and heads for the 17 JSON receipts are below; full paths and full heads are in `review-scratch.39EBEQ/runs.json`. “Model keys” means case-insensitive substring `model` in any key at any depth, counting key occurrences rather than unique names.

| Record / receipt round | Top-level keys | Recursive keys | Model keys | run.json head |
|---|---:|---:|---:|---|
| pr779 / verdict-luot17 | 35 | 47 | 0 | `f9d84d70fb46540bbecfae963c9afb4a2b48984d` |
| pr792 / verdict-luot5 | 36 | 48 | 0 | `907214d2cd0b67ff444b3adf734811eab39bfc71` |
| pr818 / verdict-luot1 | 34 | 46 | 0 | `e995730464da03223cf636e49ad32e220c6ec720` |
| pr818 / verdict-luot2 | 34 | 46 | 0 | `4ffae005eb1c434d660cbfb713ad21ed92115a8a` |
| pr818 / verdict-luot3 | 34 | 46 | 0 | `8264089a14f79867091da2629edbf45a22854c39` |
| pr818 / verdict-luot4 | 34 | 46 | 0 | `47591ebc51af917523e67191b2e96939506b78fe` |
| pr818 / verdict-luot5 | 34 | 46 | 0 | `984032f375aa0c8fe6039dfd35f6842acd49c926` |
| pr832 / verdict-luot7 | 35 | 47 | 0 | `51ae5c095972611d2c6045bd81786a4fc7e9ca62` |
| pr836 / wp812-r2-g3-exec-review-2-codex | 36 | 48 | 0 | `97f3bc18a937c251f9ee639279e2ca818bce9a58` |
| pr836 / wp812-r2-g3-exec-review-3-codex | 36 | 48 | 0 | `468667238e53e77580e4be62e0b8ed5753a75cd9` |
| pr836 / wp812-r2-g3-exec-review-4-codex | 36 | 48 | 0 | `4504b80e67e4c3c8e967be92212842eb835c6e85` |
| pr836 / wp812-r2-g3-exec-review-5-codex | 36 | 48 | 0 | `77393f6b5d9b04070567ec999e0137b9024b04f1` |
| pr836 / wp812-r2-g3-exec-review-6-codex | 37 | 49 | 0 | `e93dad700a7d2274dbcca5a0f5069b4a358639dc` |
| pr836 / wp812-r2-g3-exec-review-7-codex | 36 | 48 | 0 | `91c6d8c31190f5f9ea08e4da42ecafd898ee8935` |
| pr848 / run-f65e544e.json | 35 | 47 | 0 | `23bc189f28ea60f04ca1634b6fe66d02babf12ed` |
| pr864 / wp858-g1-luot5-run.json | 36 | 48 | 0 | `521efebab226fe3a92b2ccce4a59c27dd638edff` |
| pr873 / wp868-g1-luot5-run.json | 35 | 47 | 0 | `f07f88c75cabbef691c86ac8746317a6c0705162` |

Reopening wording: 15/15 require an independent completed approval on the exact head and a different served family for that same run, established by `do_may` or a named auditor's durable `khai_co_audit` explicitly weaker than measurement; same-family evidence is expressly insufficient. Branch B requires the full §8 item 2 audit, with the owner's pre-merge/self-read/full-copy ruling. This matches §8 and the pr846/pr882 precedent. All ten records listing extra gaps append a mandatory requirement for separate positive closure evidence; the red exact-merge gates in pr823/pr836 therefore remain blockers under either A or B. Existing descendant green gates do not close them. pr792 still requires coverage of its merged-head delta; pr864 cannot reuse its changes_requested verdict as an approval. Correct pr672's description of its gap as noted in F03. These are necessary assurance reopening conditions, not a blanket certification of every historical CI/authority claim.

Change containment: for each file, removing the two inserted header lines and appended block and reverting the one landed boolean reconstructs the base bytes exactly (15/15). No previously measured fact or unrelated line was edited. All old landed conclusions are visibly superseded by the header and the appended correction; I found no additional material state contradiction beyond the findings above. In particular, old narrative `landed_ly_do`, `landed_hieu_luc_tu`, and authorization.assurance fields are retained history, not renewed approval by this review.

Lease coverage: all 15 non-deferred paths were demoted. The only untouched lease paths are pr621/pr696/pr721, exactly the user's owner-authorized deferrals. There is no fourth omission. The final tree has 14 records with structured landed true: those three plus the 11 explicitly excluded by the spec.

Outside-write-set observations, report only: pr714 is a clear same-class gap: `ops/land/pr714-wp710-land-evidence.yaml:176` and :194 record the human audit after merge; stored comment 6080353250 was posted 2026-10-09T11:55:41Z, versus merge 11:08:09Z, and states it was not an independent search. This fails the owner's pre-merge audit rule. pr666 (:55–87) and pr680 (:56–68) retain human-audit summaries without a full stored comment body in the checked tree, so the full-copy requirement is not demonstrated. They are already assigned to the spec's later-packet group. pr732's comment has an audit checklist and named auditor but no explicit self-read sentence; keep it for the planned owner assessment rather than treat its model label as proof. Conversely, pr765/pr778 have full stored owner comments with exact candidate heads and explicit “tôi đã đọc diff” statements posted before merge (02:56:39 < 02:58:26 and 04:04:02 < 04:15:03 respectively); their unmeasured model receipts alone do not justify a same-class demotion under the owner's ruling. pr689/pr701/pr703/pr707/pr718 remain untouched per the explicit owner ruling. No out-of-scope source edits are proposed for this PR.

Command receipts and limits:

| Command / measurement | rc | Result |
|---|---:|---|
| `git -C src rev-parse HEAD HEAD^{tree}` at entry/exit | 0 | 2/2 identity values match |
| `git -C src symbolic-ref -q HEAD` | 1 | Expected: detached HEAD |
| `git -C src show master:ops/specs/wp748-r24-don-so-assurance-81-lo2.md` | 128 | Local master absent; prescribed fallback used |
| `git -C src show origin/ops/wp748-r24-g24-lease:ops/specs/wp748-r24-don-so-assurance-81-lo2.md` plus SHA-256 | 0 | 1/1 required hash matches |
| Read fallback lease; compare changed paths | 0 | 15/15 inside 18-path lease; 3 exact deferrals |
| `git -C src diff --numstat BASE HEAD` | 0 | 15 files, +332/-15; ceilings 15/18 files and 332/450 additions |
| `git -C src diff --check BASE HEAD` | 0 | No whitespace errors |
| `PYTHONDONTWRITEBYTECODE=1 python3 review-scratch.39EBEQ/audit.py` | 0 | 15/15 exact allowed edits, head-parent checks, archive created |
| `git -C src archive --format=tar --output=.../head.tar HEAD` | 0 | Exact committed HEAD extracted only to scratch |
| From archive: `python3 ops/land_evidence_nguon.py --root .` | 0 | 25/25 checked pass; 26/28 exempt; 51 total; 0 violations; 0 KHÔNG ĐO ĐƯỢC |
| Recursive JSON measurement | 0 | 17/17 parsed; 0 model keys; every stated head matches; numeric scope in F04 |
| Post-edit citation inspection | 0 | 48 occurrences / 32 unique targets inspected; defects in F02 |
| `PYTHONDONTWRITEBYTECODE=1 python3 review-scratch.39EBEQ/semantic_audit.py` | 0 | Stored comment/review search across all 15 provenance scopes; declared lease reviewer families are configuration, not execution evidence |
| F01 counterexample on archive | 0 | 2/2 assertions; historical launcher failed rc 1, no verdict |
| `python3 .../archive/scripts/pkg_secret_scan.py .../changed-files` | 0 | 15/15 changed files scanned; 0 hits; supplemental GitHub/OpenAI/AWS/credential-assignment patterns also 0 hits |
| `PYTHONDONTWRITEBYTECODE=1 python3 review-scratch.39EBEQ/final_checks.py` | 0 | Archive: 15/15 strict YAML, no duplicate keys, landed false, no lone CR, byte parity with src |
| Source file-content snapshot comparison | 0 | 5049/5049 files unchanged, including tracked/untracked/ignored outside .git |
| `git -C src status --porcelain=v1 --untracked-files=all --ignored`; worktree and cached `diff --exit-code` | 0 each | Empty; SHA/tree unchanged |

An initial exploratory comment-search helper raised AttributeError on a string-form user field; it was corrected to handle both representations and nested/indexed comments, then rerun successfully as semantic_audit.py. No failed helper result was treated as a passing check. Full repository CI and live GitHub state were not measured; this was an offline review of the frozen Git objects and stored evidence. The source-content snapshots establish no observed beginning/end delta, not an independently attested history of every filesystem write. Secret scanning establishes zero matches for the documented patterns in changed files, not universal proof of absence of every possible secret format. The source gate checks source presence and selected invariants; its green result does not validate every historical assertion.

Evidence artifacts remain in `review-scratch.39EBEQ/`: `spec.md`, `lease.yaml`, `full.diff`, `audit.log`, `records.json`, `runs.json`, `citations.json`, `reopen-checks.json`, `semantic-audit.log`, `land-evidence-gate.log`, `land-evidence-gate.rc`, `secret-scan.log`, `F01-counterexample.json`, and `final-checks.log`. VERDICT.md was created early and updated incrementally before this completed report.

VERDICT: changes_requested
