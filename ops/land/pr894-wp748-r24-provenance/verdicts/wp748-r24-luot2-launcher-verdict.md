Independent read-only review — WP748 r24/g24, PR #894, round 2. Review Class: sensitive.

Reviewed SHA: `77ec458d78d302ba89b317bd04a7282d4493c75b`.
Reviewed tree: `da246c100bf31f574bce60b8360b1ad96e622472`.
Base: `1d7e642092fb3dda15967be44d095f37bb22ac5f`.
Round-1 head: `d42713cc621cbd78d324a8b212749ff5c6199d1e`.
Started UTC: 2026-10-23 13:40:39 UTC. Completed UTC: 2026-10-23 13:49:08 UTC.

Reviewer identity: OpenAI Codex, described by the session's runtime instructions as GPT-6-based. This is an instruction-level identity declaration, not independent measurement of the served model. Exact model build, effort, provider-side routing and per-request model telemetry are unavailable. Observed execution surface: API/tool session with local Linux Bash/Python/Git execution; transport: machine tool calls. The user states this review was invoked through `launcher.py run`; the enclosing launcher's final run.json, run ID and child/launcher terminal rc are not available inside this review. I cannot independently attest `codex_cli` or the enclosing execution receipt. No Executor context or subagents were used. This content verdict alone does not establish `cross_approved` or authorize merge/land.

Identity matched at entry and exit: exact SHA/tree, detached HEAD, clean worktree/index. The spec read from local `origin/ops/wp748-r24-g24-lease` has SHA-256 `b139d8972f9f5ba6fcd3be35686de552f441b79cdb0267c1016ea83ce286fda2`; its lease matches r24/g24, base, sensitive class and 18-path write set. The pr621/pr696/pr721 deferrals recorded in the supplied round-1 review are carried forward under the user's “as in round 1” scope; they are the only three untouched lease paths.

Disposition: approve. Remaining findings in the full delta: **P0 0 / P1 0 / P2 0 / P3 0**. F01–F04 are all **closed / ĐÃ VÁ THẬT**. No additional P0–P3 issue was found in the full base-to-head delta.

**F01 — originally P2 — closed.** Location: `ops/land/pr836-wp812-land-evidence.yaml:146` (support added at :149). Scenario: the previous wording classified the failed offline round 6 as a completed changes_requested review. Fix verified: completed offline reviews are now distinguished from round 6's failure/no verdict and the final connector approval. Independently read all seven offline receipts and six surviving verdicts: rounds 1–5 and 7 each have `ma_thoat: 0` and `Verdict: changes_requested`; round 6 has `ma_thoat: 1` at `ops/land/pr836-wp812-provenance/verdict/wp812-r2-g3-exec-review-6-codex/run.json:14`, and its directory has no VERDICT.md. The connector round-10 VERDICT.md names full head `d7b42d26f09dad0599dc0434dfad25b3897f3e51` at :1 and approve at :2, without served-model evidence. The corrected :38/:117/:122 and :112–122 citations agree. Closure measurement rc 0, 7/7 offline outcomes, 1/1 final connector outcome; historical round-6 launcher rc remains 1.

**F02 — originally P3 — closed.** Locations: `ops/land/pr672-wp574-land-evidence.yaml:172`, :176–177 and `ops/land/pr679-wp678-land-evidence.yaml:569`. Scenario: pr672 pointed to a PR list entry instead of its head, and pr679's range stopped before the model limitation text. Fix verified at post-edit lines: pr672 :58 contains the full a602a38 authorized head; :63 explicitly identifies the human-audited 76f199e head. Existing :45/:54 and :20 references remain consistent. pr679 now cites `ops/reviews/wp678-spec-review-6-codex-verdict.receipt.yaml:50–58`: :50/:52 identify requested/header model, :55–56 state that raw launcher artifacts were not retained, and :58 states that the actually served model cannot be measured. No incomplete corrected anchor remains.

**F03 — originally P3 — closed.** Location: `ops/land/pr672-wp574-land-evidence.yaml:180`. Scenario: “approved SHA differs from merged head” conflated the human-audited head with final land authorization. Fix verified: the text explicitly identifies the old HUMAN AUDIT on 76f199e and recognizes a602a38 as the authorized/merged head. Its new :71 anchor records amendment 5 authorizing merge only on a602a38; :58/:83/:88 and the actual merge commit's second parent agree. The remaining gap is stale audit coverage and missing full comment, not a merge contrary to the recorded authorization. No further fix required.

**F04 — originally P3 — closed.** Locations: `ops/land/pr779-wp775-land-evidence.yaml:171`, pr792 :166, pr818 :160, pr832 :143, pr836 :151, pr848 :130, pr864 :130, pr873 :134 (each abbreviated record is the changed `ops/land/prNNN-*-land-evidence.yaml`). Scenario: unqualified key counts could be mistaken for recursive totals. Fix verified in all eight measurement fields and every duplicated count in `ly_do`: counts now explicitly distinguish top-level keys from all-depth mapping-key occurrences, and the zero-model-key claim explicitly covers every depth. Independently parsed 17/17 receipts and recursively traversed dictionaries and lists, matching keys case-insensitively on substring `model`; all have zero such keys.

| Receipt (relative to that record's provenance directory) | Top-level keys | All-depth keys | Model keys | ma_thoat |
|---|---:|---:|---:|---:|
| pr779 `verdict-luot17/run.json` | 35 | 47 | 0 | 0 |
| pr792 `verdict-luot5/run.json` | 36 | 48 | 0 | 0 |
| pr818 `verdict-luot1/run.json` | 34 | 46 | 0 | 0 |
| pr818 `verdict-luot2/run.json` | 34 | 46 | 0 | 0 |
| pr818 `verdict-luot3/run.json` | 34 | 46 | 0 | 0 |
| pr818 `verdict-luot4/run.json` | 34 | 46 | 0 | 0 |
| pr818 `verdict-luot5/run.json` | 34 | 46 | 0 | 0 |
| pr832 `verdict-luot7/run.json` | 35 | 47 | 0 | 0 |
| pr836 `verdict/wp812-r2-g3-exec-review-2-codex/run.json` | 36 | 48 | 0 | 0 |
| pr836 `verdict/wp812-r2-g3-exec-review-3-codex/run.json` | 36 | 48 | 0 | 0 |
| pr836 `verdict/wp812-r2-g3-exec-review-4-codex/run.json` | 36 | 48 | 0 | 0 |
| pr836 `verdict/wp812-r2-g3-exec-review-5-codex/run.json` | 36 | 48 | 0 | 0 |
| pr836 `verdict/wp812-r2-g3-exec-review-6-codex/run.json` | 37 | 49 | 0 | 1 |
| pr836 `verdict/wp812-r2-g3-exec-review-7-codex/run.json` | 36 | 48 | 0 | 0 |
| pr848 `verdicts/run-f65e544e.json` | 35 | 47 | 0 | 0 |
| pr864 `verdicts/wp858-g1-luot5-run.json` | 36 | 48 | 0 | 0 |
| pr873 `verdicts/wp868-g1-luot5-run.json` | 35 | 47 | 0 | 0 |

Full paths and full receipt heads are retained in `review-r2.JR51hv/runs.json`. The additional pr836 round-1 receipt was also checked for F01: rc 0 and zero model-bearing keys. Thus the broader `verdict/*/run.json` wording does not conceal a counterexample outside rounds 2–7.

Containment and regression assessment: the round-2 diff is exactly 10 files, +20/-18; every changed span is strictly inside `dinh_chinh_r24`. All other files are unchanged between the two review heads. Across the full delta, removing precisely the two inserted header lines and appended block and reverting the sole structured landed boolean reconstructs the base bytes exactly **15/15**. All 15 pre-block prefixes also equal round 1 byte-for-byte. Only reason, evidence-list, measurement and extra-gap wording changed in round 2; packet identity, head anchors, landed state, assurance result and reopening conditions are unchanged.

The full-delta review rechecked all 15 demotion reasons and reopening conditions, 54 line-reference occurrences / 37 unique post-edit targets, and 34/34 evidence-list path references. All 15 selected heads match their Git merge's second parent; stored primary PR readbacks agree 13/13 where present. No reversal of round-1 demotion conclusions or weakened reopening requirement was found. Exact-head independent approval and same-run different-family evidence remain required under branch A; named-auditor attestation remains explicitly weaker than measurement; same-family evidence remains insufficient. Branch B retains the full independent exact-head human audit and owner-comment conditions. All ten records with extra gaps require separate positive closure evidence.

The red exact-merge gates in pr823/pr836, pr792's uncovered merged-head delta, pr832's stale connector head and pr864's changes_requested verdict remain acknowledged gaps. For precision, pr823's stored workflow snapshot is still `in_progress`, with no terminal conclusion; its stored job readback positively shows `gate (ubuntu-latest)` failed at `release-verify strict`. That supports the red-gate statement without establishing terminal workflow completion. The retained historical landed narratives are visibly superseded by the headers and appended corrections. The scope/exclusions and round-1 outside-write-set observations are unchanged; none is presented as a newly discovered defect of this delta.

Commands and measurements (all source-code execution used the archive; `S=review-r2.JR51hv`):

| Command / check | rc | Positive result |
|---|---:|---|
| `git -C src rev-parse HEAD HEAD^{tree}` at entry and exit | 0 | 2/2 exact identity values match each time |
| `git -C src symbolic-ref -q HEAD` | 1 | Expected detached state |
| `git -C src show origin/ops/wp748-r24-g24-lease:ops/specs/wp748-r24-don-so-assurance-81-lo2.md` plus SHA-256; read lease | 0 | 1/1 required spec hash; base/r24/g24/class match; 15/15 changed paths authorized |
| `git -C src diff --numstat d42713cc621cbd78d324a8b212749ff5c6199d1e HEAD` | 0 | 10 files, +20/-18 |
| `git -C src diff --numstat 1d7e642092fb3dda15967be44d095f37bb22ac5f HEAD` | 0 | 15 files, +334/-15; 15 ≤ 18 and 334 ≤ 450 under `nang_tran` |
| `PYTHONDONTWRITEBYTECODE=1 python3 "$S/audit.py"` | 0 | 10/10 round-2 containment; 15/15 base reconstruction, strict YAML with duplicate-key rejection, landed false, no lone CR, archive/HEAD/src byte parity |
| `git -C src archive --format=tar --output="$S/head.tar" 77ec458d78d302ba89b317bd04a7282d4493c75b` (absolute output path in helper), extract to scratch | 0 | Frozen committed HEAD archived and extracted successfully |
| From `$S/archive`: `PYTHONDONTWRITEBYTECODE=1 python3 ops/land_evidence_nguon.py --root .` | 0 | 25/25 checked pass; 26/28 exempt; total 51; 0 violations, 0 KHÔNG ĐO ĐƯỢC |
| `PYTHONDONTWRITEBYTECODE=1 python3 "$S/evidence.py"` | 0 | 17/17 receipt measurements, 7/7 pr836 offline outcomes, 15/15 merge-head checks, 13/13 readbacks, 15/15 reopening rules, 10/10 separate extra-gap requirements |
| `PYTHONDONTWRITEBYTECODE=1 python3 "$S/archive/scripts/pkg_secret_scan.py" "$S/changed-files"` | 0 | 15/15 changed files eligible and scanned; 0 hits (coverage independently asserted by evidence.py) |
| Supplemental GitHub/OpenAI/AWS/credential-assignment patterns in evidence.py | 0 | 15/15 files checked, 0 matches |
| Post-edit citation extraction and manual inspection | 0 extraction | 54/54 occurrences, 37/37 unique line targets inspected; 34/34 evidence-list paths resolve |
| Final Python snapshot/identity assertions (inline command, output in final-checks.log) | 0 | 5049/5049 source files unchanged, including tracked/untracked/ignored outside `.git` |
| `git -C src status --porcelain=v1 --untracked-files=all --ignored`; `git -C src diff --exit-code`; `git -C src diff --cached --exit-code` | 0 each | Empty outputs; clean source/index |
| `git -C src diff --check 1d7e642092fb3dda15967be44d095f37bb22ac5f HEAD` | 0 | No whitespace errors |

Limits: no credentials, remote access, GitHub writes, commits, pushes or source edits were used. Scratch and this report are the only review outputs. Sandbox mode is workspace-write; read-only source handling was maintained by command scope, not claimed as an independently enforced source mount. Beginning/end content snapshots prove no observed delta, not the entire write history. Full repository CI and live head-CI status were not measured; the local source gate verifies its documented invariants, not every historical assertion. Secret scans found zero matches for the stated patterns in the full contents of the 15 changed files; they do not prove absence of all possible secret formats. The managed-environment status tool was not available, and no credential discovery was attempted.

Artifacts: `review-r2.JR51hv/spec.md`, `lease.yaml`, `full.diff`, `round2.diff`, both numstat files, `audit.py`, `audit.log`, `records.json`, `citations.json`, `citation-targets.txt`, `evidence.py`, `evidence.log`, `runs.json`, `head-checks.json`, `pr836-outcomes.json`, `land-evidence-gate.log`/`.rc`, `secret-scan.log`/`.rc`, `final-checks.log`, and beginning/end source hashes. `VERDICT.md` was created after the initial identity gate and updated during the review before this final version.

VERDICT: approve
