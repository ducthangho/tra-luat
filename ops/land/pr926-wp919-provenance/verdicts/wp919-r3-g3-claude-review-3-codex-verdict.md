# Independent read-only review — wp919 (ADR-0055), round 3

**Approve: 0 P0, 0 P1, 0 P2, 0 P3.** All prior findings are closed on the exact reviewed SHA. Local documentation gates pass; remote CI/authority and the enclosing execution receipt remain independently unverified.

Reviewer: OpenAI Codex, described by runtime instructions as based on GPT-6; provider `openai_codex`, model family `openai` as declared by the runtime role. Observed execution surface is tool-mediated local subprocess execution; transport is machine/tool-mediated. Invocation through `launcher.py run` is supplied by the user. Exact serving model/effort, launcher session ID, final execution receipt and CLI-versus-service identity are not independently visible; `launcher.out` is empty. No Executor conversation was supplied. Runtime instructions are not a serving-model attestation.

Reviewed SHA: `4e4d482e46cccc6b5e7e6c4f8cf4af636b63e070`.
Tree: `b20fb04d7612bfa5ed4451c0a45c7e8b36fdc248`.
Review base: `0dbb4c22aaaaf801e6c392e235391a35c1a6a268`.
Review Class: **sensitive**. Identity matched: full non-shallow clone, detached HEAD, clean tree, expected merge-base. Review is anchored to this local SHA; publication status is the user's statement, not a remote observation.

Revision 3 spec SHA-256: `7d0eb91dd35a36a547348dbc0370366975071c6b3ac3468c2bab7351edbf2987`, verified from the local `origin/ops/wp919-r1-g1-lease` object. Authority comments supplied: #919 `issuecomment-6393799783` (r1), `issuecomment-6394493260` (r2), `issuecomment-6396165849` (r3). **I cannot read GitHub in this review; comment contents/authors, current authority, ref freshness and exact-head CI are not independently verified.** No network or credential use is authorized or performed.

All writes are limited to this verdict and reviewer scratch outside `src/`. Scripts use `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0` and `GIT_TERMINAL_PROMPT=0`. No source edit, commit, push or GitHub comment is permitted. The cloud-runtime skill was read for environment guidance; its environment-status tool is unavailable. No credential discovery was attempted.

## Initial execution evidence

Command: `python3 -B review-wp919-r3.XaCvO7/preflight.py`, rc=0. The following output and the full per-command records in `review-wp919-r3.XaCvO7/receipts.jsonl` are locally executed evidence:

```text
$ git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/w919c/src rev-parse --is-inside-work-tree [rc=0]
true
$ git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/w919c/src rev-parse --is-shallow-repository [rc=0]
false
$ git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/w919c/src rev-parse HEAD [rc=0]
4e4d482e46cccc6b5e7e6c4f8cf4af636b63e070
$ git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/w919c/src rev-parse 'HEAD^{tree}' [rc=0]
b20fb04d7612bfa5ed4451c0a45c7e8b36fdc248
$ git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/w919c/src symbolic-ref -q HEAD [rc=1]
(empty stdout)
$ git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/w919c/src merge-base HEAD origin/master [rc=0]
0dbb4c22aaaaf801e6c392e235391a35c1a6a268
$ git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/w919c/src status --porcelain=v1 --untracked-files=all --ignored [rc=0]
(empty stdout)
$ git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/w919c/src config --get-regexp 'extensions\.partialclone|remote\..*\.promisor|remote\..*\.partialclonefilter' [rc=1]
(empty stdout)
$ git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/w919c/src config --get core.abbrev [rc=1]
(empty stdout)
$ git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/w919c/src rev-parse origin/master [rc=0]
b168290226d4ae9829f7cc45badf2bce4ba8457c
$ git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/w919c/src diff --name-status 0dbb4c22aaaaf801e6c392e235391a35c1a6a268 4e4d482e46cccc6b5e7e6c4f8cf4af636b63e070 [rc=0]
M	docs/PROTOCOL_DA_PHIEN.md
A	docs/adr/0055-tran-loi-goi-codex-len-muoi.md
$ git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/w919c/src diff --numstat 0dbb4c22aaaaf801e6c392e235391a35c1a6a268 4e4d482e46cccc6b5e7e6c4f8cf4af636b63e070 [rc=0]
2	1	docs/PROTOCOL_DA_PHIEN.md
135	0	docs/adr/0055-tran-loi-goi-codex-len-muoi.md
$ git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/w919c/src diff --check 0dbb4c22aaaaf801e6c392e235391a35c1a6a268 4e4d482e46cccc6b5e7e6c4f8cf4af636b63e070 [rc=0]
(empty stdout)
Runtime: Linux-6.18.44-fc-v153-x86_64-with-glibc2.39; Python 3.13.16
UTC: 2026-10-25T11:38:43.040191+00:00
launcher.out bytes=0
spec source master: rc=128
spec source origin/master: rc=128
spec source origin/ops/wp919-r1-g1-lease: rc=0
spec sha256=7d0eb91dd35a36a547348dbc0370366975071c6b3ac3468c2bab7351edbf2987
lease wp919-r1-g1-claude-remote-20261025.yaml copied from local ref
lease wp919-r2-g2-claude-remote-20261025.yaml copied from local ref
lease wp919-r3-g3-claude-remote-20261025.yaml copied from local ref

```

## Progress — measured scope and gates

The full base-to-head diff is exactly **2 files, +137/-1**: protocol **+2/-1**, ADR **+135/-0**. `measure_docs.py` confirms **2/2** byte-scope checks: the protocol before §20 is identical, and removing its ADR-0052/0055 routing rows makes the entire old/new protocol identical. All **6/6** forbidden historical ADRs remain byte-identical. The round-3 delta replaces only the invariant paragraph in ADR-0055.

The r3 lease's spec commit `289d1f29ace72edf60a4cb7633b02657a05612dd` yields the same hash-verified spec. Frozen r1/r2 blobs still match their recorded hashes and spec commits. Local lease replacement links are reciprocal g1→g2→g3; g3 is not marked superseded and expires `2026-10-26T11:35:17Z`. The lease's older base `937162894e703dec9aa7c30163d913e2f83d276c` is an ancestor of the requested review base (`merge-base --is-ancestor`, rc=0). Its note expressly anchors this review to local head `4e4d482`. Current remote holder status is not independently observable.

`core.abbrev` was **unset** (read rc=1). For gate subprocesses it was set to **7** using `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.abbrev GIT_CONFIG_VALUE_0=7`, then read back as `7` (rc=0); no Git configuration file was changed. `PYTHONDONTWRITEBYTECODE=1` prevents bytecode writes.

| Executed command | cwd | rc | Positive evidence |
| --- | --- | ---: | --- |
| `python3 src/.claude/dev/packet_loop.py adr-song --root src` | Review directory | 0 | **54 ADRs / 54 §20 rows**, 1:1; existing ADR-0016 status exemption disclosed |
| `python3 src/.claude/dev/packet_loop.py doctrine-scan --root src` | Review directory | 0 | **10/10** target files scanned; zero hits |
| `python3 scripts/tl.py doc-claims-check --path docs/adr/0055-tran-loi-goi-codex-len-muoi.md --json` | `src/` | 0 | `ok: true`, **1/1** file, zero flags/advisories |
| `python3 scripts/tl.py doc-claims-check --path docs/PROTOCOL_DA_PHIEN.md --json` | `src/` | 0 | `ok: true`, **1/1** file, zero flags/advisories |
| `git -C src diff --check 0dbb4c22aaaaf801e6c392e235391a35c1a6a268 4e4d482e46cccc6b5e7e6c4f8cf4af636b63e070` | Review directory | 0 | Empty output |

Both doc-claims scans explicitly skip L9 because these narrow inputs lack `SKILL.md` plus a references file. Syntax/claim scanners do not establish semantic correctness, CI, authority, or reviewer model identity. Full output is in `review-wp919-r3.XaCvO7/gates.out` and per-command receipts.

## Revision-3 invariant measurements

Command: `python3 -B review-wp919-r3.XaCvO7/probe_logic.py`, rc=0. The current table and iff sentence agree in **11,900/11,900** enumerated contexts; no-0055 selection agrees with the old rule in **2,925/2,925**. The **154,700** append-one-line edges include **58,330** invalid/duplicating 0055 additions and **3,380** additions to an already selected 8/10 cap: **zero increases** in either protected category. There are **392** increases from two, all caused by valid opt-in lines. All **30/30** named cases (including every round-1 case), **9/9** raw cases and **4/4** arithmetic cases passed.

The task's unqualified “no added line can raise the ceiling” cannot be confirmed: first valid opt-in must permit 2→10 or 2→8. R3 explicitly replaces that property. The tested guarantees are precisely r3 Hợp đồng 2(a–c), implemented at ADR lines 54–59, with the valid-opt-in exception at 61–64. The three round-2 counterexamples are now intended behavior, not contradictions. The tests model the written policy using synthetic land predicates; they do not claim a production declaration parser exists or that ADR-0055 has landed.

## ĐỐI CHIẾU LƯỢT TRƯỚC — every prior finding

The supplied round-1 verdict has seven findings (3 P2, 4 P3); round 2 carries the first class forward as WP919-R2-01. All are **ĐÃ VÁ THẬT — closed** on this SHA. R1-01 and R2-01 are one historical class, not two independent open defects. Locations below refer to the current candidate.

| Finding / original severity / class | Status and current location | Measured closure evidence |
| --- | --- | --- |
| WP919-R1-01 / P2 / `arbitration-invalid-raises-cap` | **Closed**, ADR:31–68,109–111 | `python3 -B review-wp919-r3.XaCvO7/probe_logic.py`, rc=0: **30/30** selection cases, **9/9** raw cases, **11,900/11,900** iff/table checks. Both valid gives **8**; append duplicate 0052 gives **2**, never the old erroneous **10**. Invalid/duplicate/unmeasurable input with a 0055 declaration fails closed. Initialization now requires the full selection rule. The replacement-invariant defect is closed as detailed in R2-01 below. |
| WP919-R1-02 / P2 / `frozen-counter-contract-conflict` | **Closed against r3**, ADR:86–118; protocol:1521,1524 | `python3 -B review-wp919-r3.XaCvO7/measure_docs.py`, rc=0: r3 SHA-256 matches the supplied identifier, lease and `spec_commit`; C4 explicitly requires the existing counter plus absent declaration reader, and C5 permits the old gate-cell correction. C4–C5 are byte-identical between r2/r3. At spec base, review base and reviewed head, whole-word line counts (lease_publish / packet_loop) are **0/8** for `codex_review_calls_used`, **0/8** for `nang_tran`, **0/0** for `tran_loi_goi_codex`. Current `rg -n -w` reruns return rc=1 for zero matches and rc=0 for eight lines. `git grep -n -w tran_loi_goi_codex <head> -- '*.py'` returns rc=1, zero hits. Counter behavior **16/16** below. No restoration of the false zero-counter claim. Remote authorization remains unverified. |
| WP919-R1-03 / P2 / `pr909-cause-not-measured` | **Closed**, ADR:112–115 | `python3 -B review-wp919-r3.XaCvO7/measure_incident.py`, rc=0: **5/5** ledger rows, **4/4** launcher records (2 unfinished / 2 completed), **4/4** prompt hashes, **1/1** connector readback. Ledger structured call-accounting keys **0**; **35** provenance files, **0** with tested counter markers. These absences do not prove counter non-use. ADR expressly labels use `KHÔNG ĐO ĐƯỢC` and the executor assertion as unrecorded; it no longer asserts zero block events. The original PR909 spec is now positively read from both local sources, hash-matches the ledger and has **0** call declarations. |
| WP919-R1-04 / P3 / `counter-history-date` | **Closed**, ADR:88–93 | `measure_docs.py`, rc=0; `git show -s --format=%H%n%aI%n%cI%n%P%n%s <rev>` each rc=0: ADR-0052 land `8ab1007` is **2026-10-17 07:45:01Z**; counter merge `d8b15cb` is **2026-10-17 16:55:49Z**; implementation commit `97291ab` is **2026-10-16 14:58:33Z**. `git show <rev>:.claude/dev/packet_loop.py` each rc=0: matching whole-word lines at `8ab1007`, `d8b15cb^1`, `d8b15cb` are **0, 0, 8**. Text correctly separates branch authorship from next-day mainline availability. |
| WP919-R1-05 / P3 / `mixed-reviewer-quantifier` | **Closed**, ADR:76–84 | `probe_logic.py`, rc=0: **4/4** arithmetic cases. `(calls, Codex rounds, other rounds)` = `(10,10,0)` reaches both; `(10,8,0)` reaches calls only; `(1,1,9)` reaches total rounds only; `(10,9,1)` reaches both. The before-or-together assertion is expressly restricted to a PR with **only** Codex reviewers; mixed review counts total rounds separately. |
| WP919-R1-06 / P3 / `state-limit-entry-exclusive` | **Closed**, ADR:103–115 | `python3 -B review-wp919-r3.XaCvO7/probe_counter.py`, rc=0: **16/16** assertions. Default init selects **2**, explicit init selects **10** (both rc=0). The third call returns **rc=3**, used remains **2**, state becomes `blocked`. Rescue before raise returns **rc=8**. `nang-tran --tran-moi 10` returns rc=0, installs **10** while staying blocked; `record-rescue --quyet-dinh nang_tran` returns rc=0 and resumes `running` with used still **2**. Text accurately describes both entry paths and separate authority. These are synthetic scratch fixtures, not real calls or authenticated approval. |
| WP919-R1-07 / P3 / `cap-pointer-count` | **Closed**, ADR:127–131 | `measure_docs.py`, rc=0: exactly **5** body references to ADR-0052, at protocol lines **702,722,737,1139,1145**. Context classification is **4 ceiling + 1 unchanged eligibility** (737); §8 has 3 total and §12 has 2. Text matches those measurements; protocol body is byte-identical to base. |
| WP919-R2-01 / P2 / carried `arbitration-invalid-raises-cap` | **Closed**, ADR:52–64 | `measure_docs.py`, rc=0, extracts the r3 C2 invariant and current ADR text side by side. C2(a) matches ADR:54–55 (invalid 0055 additions), C2(b) matches 56–57 (already 8/10), C2(c) matches 58–59 (no-0055 exact old behavior); C2's valid-opt-in exception matches 61–64. `probe_logic.py`, rc=0: **58,330/58,330**, **3,380/3,380**, **2,925/2,925** respective checks. All three prior counterexamples now agree with the explicit exception: empty+valid55 **2→10**, empty+valid52 **2→8**, malformed52+first exact valid52 without55 **2→8**. Restoring the old blanket sentence fails **3/3** mutation counterexamples; restoring r1's remaining-valid-line rule fails the duplicate52 case. |

## Whole-diff review against r3

Every **6/6 Hợp đồng clause** and **5/5 Chấp nhận bullet** was assessed over the entire base→head delta, including unchanged-since-r2 content. Measured script outputs are in the adjacent scratch directory; local results do not certify remote CI or authority.

| Requirement | Evidence and conclusion |
| --- | --- |
| C1 — change call ceiling only; retain output-based counting, later-call eligibility, two-call reservation, rounds/attempts and rescue | ADR:6–11 expressly inherits the other ADR-0052 rules, which retain output/timeout/schema counting and exclude pre-output failures. ADR:66–68 preserves frozen policies and separate owner raise; 76–84 separates axes; 117–118 preserves pre-call budget checks. ADR-0041 still reserves two; ADR-0043/0048 preserve distinct counters. No exemption, count reset, new reservation or second budget is added. **Conforms.** |
| C2 — raw declaration grammar, three land checks, iff/table, conservative selection, invariant, no retroactivity and old-only parity | ADR:25–72 implements all terms. Raw bytes are measured without trimming CR, BOM, spaces or case. All named and enumerated tests pass, and r3's three scoped guarantees agree with the opt-in exception. All three local land predicates were executed separately; failure/unmeasurability scenarios are represented in the model. **Conforms**, with ref freshness unverified as explicitly disclosed. |
| C3 — correct equal numerical ceilings and exhaustion order | ADR:74–84; **4/4** arithmetic cases establish Codex-only before-or-together and mixed total-round behavior. No ten-plus-ten reading. **Conforms.** |
| C4 — accurate existing counter versus absent declaration reader, bounded incident claims | ADR:86–118; three revisions × six whole-word counts; history **0→8**; real CLI **16/16** checks; incident evidence and explicit unmeasured-counter-use label. **Conforms.** |
| C5 — new number lives in ADR; §20 adds new row and updates old status/gate cell, no copied ten-call ceiling | Exactly the two §20 rows at protocol:1521,1524 changed, with the old status pointing to ADR-0055 and preserving old-only selection. No ten-call number is copied into either changed row. Both gate cells distinguish manual state from no automatic declaration reader. **Conforms.** |
| C6 — historical ADRs/frozen specs untouched | Exact authorized two-file diff, **6/6** forbidden old ADRs byte-equal; frozen r1/r2/r3 hashes and spec commits match local authority branch. **Conforms.** |
| A1 — adr-song | **Passed**, rc=0, **54/54**. |
| A2 — doctrine-scan | **Passed**, rc=0, **10/10** files, zero hits. |
| A3 — exactly two files within ADR-0053 | **Passed locally**: **2 files ≤6**, **137 added lines ≤450**. Spec's 0053 land selector passes stored-history checks. Even the old 3-file/300-line cap would contain this delta. |
| A4 — whitespace and final-head CI | Whitespace **passed**, rc=0. CI **not_run / not_measured**: local-only offline review precedes publication under the supplied instruction. No green-CI claim is made. |
| A5 — launcher review, zero findings, model receipt if measurable, exact-SHA owner approval before merge | This exact-SHA independent substantive review has **0 P0, 0 P1, 0 P2, 0 P3**. Enclosing launcher receipt/serving-model evidence and owner exact-SHA approval are **not independently verified here**; they remain downstream evidence requirements before merge. |

Additional full-diff measurements: **12/12** explicit local ADR/source/evidence targets resolve (including ADR-0055 itself), and protocol §3.2 exists. The current counter source files are byte-identical from the spec's older base through the reviewed head (`git diff --exit-code 9371628 HEAD -- ops/lease_publish.py .claude/dev/packet_loop.py`, rc=0). The bounded `ops/reviews/*.receipt.yaml` inventory parses **285/285** files: **5** textual mentions of `codex_review_calls_used`, **0** files with that structured key. This does not prove absence in every possible historical artifact; the ADR appropriately presents ten as an owner choice, not a measured optimum. PR #892 is recorded at `CLAUDE.md:573–580`. The ADR status line retains the original r1 approval provenance; the current review contract/lease is r3/g3 as verified above.

No new P0–P3 finding was established. Accordingly there is no new finding ID/severity/location/scenario/fix entry; no finding has been deferred to reach zero.

## Selection cases — executable output and limits

The following is output of `probe_logic.py` (rc=0). `valid55` uses a hypothetical future land OID with all land predicates true; this is not the current unlanded head. The finite enumeration uses 13 representative raw line types, ordered blobs of length 0–3, and five full/shallow/unmeasurable/per-side-failure contexts. Appending preserves existing lines and measurements. An independent raw-regex oracle supplies the legacy comparison. These tests are a model of written rules, not tests of a production parser or a proof over arbitrary byte strings.

```text
R1 no declaration: cap=2; expected=2; iff10=False
R1 only valid 0052: cap=8; expected=8; iff10=False
R1 only valid 0055: cap=10; expected=10; iff10=True
R1 both valid: cap=8; expected=8; iff10=False
R1 0052 duplicated + valid 0055: cap=2; expected=2; iff10=False
R1 0055 duplicated + valid 0052: cap=2; expected=2; iff10=False
R1 only 0052 duplicated: cap=2; expected=2; iff10=False
R1 only 0055 duplicated: cap=2; expected=2; iff10=False
R1 both duplicated: cap=2; expected=2; iff10=False
R1 0052 wrong OID + valid 0055: cap=2; expected=2; iff10=False
R1 0055 wrong OID + valid 0052: cap=2; expected=2; iff10=False
R1 only invalid 0055: cap=2; expected=2; iff10=False
R1 shallow: cap=2; expected=2; iff10=False
R1 globally unmeasurable: cap=2; expected=2; iff10=False
R1 only 0052 unmeasurable + valid 0055: cap=2; expected=2; iff10=False
NEW only 0055 unmeasurable + valid 0052: cap=2; expected=2; iff10=False
NEW valid55 + malformed52: cap=2; expected=2; iff10=False
NEW valid55 + valid52 + malformed52: cap=2; expected=2; iff10=False
NEW valid55 + malformed55: cap=2; expected=2; iff10=False
NEW valid52 + malformed55: cap=2; expected=2; iff10=False
NEW no55: valid52 + malformed52: cap=8; expected=8; iff10=False
NEW no55: only malformed52: cap=2; expected=2; iff10=False
NEW no55: valid52 + prose mention: cap=8; expected=8; iff10=False
NEW valid55 + comment-prefixed52: cap=10; expected=10; iff10=True
NEW invalid52 only: cap=2; expected=2; iff10=False
NEW invalid55 + invalid52: cap=2; expected=2; iff10=False
NEW valid52 + CRLF52, no55: cap=8; expected=8; iff10=False
NEW valid55 + CRLF52: cap=2; expected=2; iff10=False
NEW valid52 + BOM55: cap=8; expected=8; iff10=False
NEW valid55 + unrelated ADR declaration: cap=10; expected=10; iff10=True
Explicit cases: 30/30; all 15 round-1 cases covered
Raw LF: cap=10; expected=10
Raw no terminal LF: cap=10; expected=10
Raw CRLF: cap=2; expected=2
Raw BOM: cap=2; expected=2
Raw trailing space: cap=2; expected=2
Raw uppercase OID: cap=2; expected=2
Raw duplicate: cap=2; expected=2
Raw comment prefix: cap=2; expected=2
Raw good plus malformed: cap=2; expected=2
Raw-byte cases: 9/9
Enumeration counts: {"append": 154700, "iff": 11900, "invalid55": 58330, "legacy": 2925, "raises": 392, "selected_high": 3380}
Violations: iff=0; invalid55 increases=0; increases from 8/10=0; no55 legacy differences=0; raises without valid opt-in=0
R2 counterexample now expressly allowed: first valid55: 2 -> 10
R2 counterexample now expressly allowed: first valid52: 2 -> 8
R2 counterexample now expressly allowed: malformed52 then first exact valid52: 2 -> 8
Land-predicate failure 52 / ADR absent at L: cap=2
Land-predicate failure 52 / ADR present at L parent: cap=2
Land-predicate failure 52 / L off first-parent chain: cap=2
Land-predicate failure 52 / unmeasurable history: cap=2
Land-predicate failure 55 / ADR absent at L: cap=2
Land-predicate failure 55 / ADR present at L parent: cap=2
Land-predicate failure 55 / L off first-parent chain: cap=2
Land-predicate failure 55 / unmeasurable history: cap=2
Land-predicate negative cases: 8/8 (simulated predicates, separate from real Git checks)
Round arithmetic: calls=10; Codex rounds=10; other=0; total=10; call-cap=True; round-cap=True
Round arithmetic: calls=10; Codex rounds=8; other=0; total=8; call-cap=True; round-cap=False
Round arithmetic: calls=1; Codex rounds=1; other=9; total=10; call-cap=False; round-cap=True
Round arithmetic: calls=10; Codex rounds=9; other=1; total=10; call-cap=True; round-cap=True
Arithmetic cases: 4/4
Mutation checks: old blanket invariant rejected by 3/3 opt-in cases; r1 both-valid+duplicate52 promotion rejected (10 != 2).
```

The structural argument extends beyond the bounded sample: once any 0055 declaration exists, a second or invalid 0055 forces two; an absent 0052 side can only keep ten or reduce it when a declaration is added. Starting at eight, a valid52 is already present, so adding 0055 cannot satisfy the no52 condition for ten. With no 0055 declaration, the first table row explicitly delegates to the untouched old raw-match rule. A two-call result can increase only by adding a valid first opt-in; malformed old-only lines remain governed by the old exact-match predicate. Unrelated prose and nonmatching prefixes do not become declarations.

## Real land-predicate and incident measurements

`measure_docs.py` executed `git cat-file -e <L>:<ADR>`, `git cat-file -e <L>^1:<ADR>` and membership in `git rev-list --first-parent origin/master`. All rev-list commands returned rc=0. Parent rc=128 below means the path is absent in an existing parent, an expected negative result.

| OID / ADR | Present rc | Parent present rc | In stored first-parent chain | Meaning |
| --- | ---: | ---: | --- | --- |
| `8ab100793df9831505f495543a74044b91c2c9ab` / 0052 | 0 | 128 | yes | Local land tests pass; wp919 itself retains the eight-call selection in its spec |
| Same OID / 0053 | 0 | 128 | yes | Local size-selector land tests pass |
| `3868e923a5f20f34e5a8223932b27b25ac5b4001` / 0055 | 0 | 128 | no | R1 author commit is not a land OID |
| `0a5c5e59af4c416e2524e1c349d50ac73bdde2a5` / 0055 | 0 | 0 | no | R2 head is not an introduction or land OID |
| `4e4d482e46cccc6b5e7e6c4f8cf4af636b63e070` / 0055 | 0 | 0 | no | Reviewed r3 head is not an introduction or land OID |

No fetch occurred. Stored `origin/master` is `b168290226d4ae9829f7cc45badf2bce4ba8457c`; the reviewed merge-base remains the requested `0dbb4c2…`. The freshly-fetched prerequisite is **not certified**. This review does not grant ten calls to this packet or retroactively to PR909.

PR909's original spec now resolves with **rc=0** at both `1c879c0:ops/specs/wp748-r25-launcher-model-phuc-vu.md` and `origin/ops/wp748-r25-g25-lease:ops/specs/wp748-r25-launcher-model-phuc-vu.md`. Both raw blobs hash to `5f85d350bc78a28693b1cb095bfa2fa62353975c3ba0e714a2a59c6e8e4dafa3`, matching the committed ledger, and contain **zero** `tran_loi_goi_codex:` declarations, selecting **two** under ADR-0052. This is stronger local evidence than the prior verdict's failed lookups. The interruption causes and emitted-output byte counts are still ledger-level reports: unfinished launcher records alone do not independently prove those causes. Counter non-use remains expressly unmeasured.

## Execution receipts and probe corrections

Reproducible scripts and captured outputs are in `review-wp919-r3.XaCvO7/`; `receipts.jsonl` contains substantive command/cwd/UTC/rc/stdout/stderr records. `run_probe.py` captures top-level probe rc as well as subcommand receipts. Final runs of `measure_docs.py`, `probe_logic.py`, `probe_counter.py` and `measure_incident.py` each returned **rc=0**. Required gate outputs are in `gates.out`.

Expected negative return codes are not counted as successful positive lookups: detached `symbolic-ref` rc=1; unset configuration/no grep matches rc=1; absent spec sources on master/origin-master rc=128; missing ADR at existing parent rc=128; over-budget counter rc=3; premature rescue rc=8.

Two reviewer scratch probes were corrected before relying on their results. The initial write-set hash check raised `AssertionError` (Python rc=1) because it omitted the lease's expressly declared NFC/casefold normalization; applying that normalization yields the exact lease hash `0dddc70e2ac7a55db20f1bb9af2f4a26848f2caad15bf6f4897310ea20d6bef0` (final probe rc=0). An initial incident-spec lookup wrongly included the ledger's parenthetical annotation in the path (rc=128); extracting the real `.md` path produced the successful, hash-matched reads above. Those failed exploratory lookups are not evidence of absent source. No candidate edit was made to repair either probe.

Full selftest, Ruff, remote GitHub/API reads, live CI, extra model invocation, push, merge, land and deployment were **not run**. They are not claimed as passed. The required documentation gates and focused independent semantic/counter/claim probes were executed. The execution receipt must be completed by the enclosing launcher, not fabricated here.

## Final read-only verification

Command: `python3 -B review-wp919-r3.XaCvO7/final_checks.py`, rc=0.

```text
$ git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/w919c/src rev-parse HEAD 'HEAD^{tree}' [rc=0]
4e4d482e46cccc6b5e7e6c4f8cf4af636b63e070
b20fb04d7612bfa5ed4451c0a45c7e8b36fdc248
$ git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/w919c/src status --porcelain=v1 --untracked-files=all --ignored [rc=0]
(empty stdout)
$ git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/w919c/src diff --exit-code --no-ext-diff [rc=0]
(empty stdout)
$ git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/w919c/src diff --cached --exit-code --no-ext-diff [rc=0]
(empty stdout)
$ git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/w919c/src diff --check 0dbb4c22aaaaf801e6c392e235391a35c1a6a268 HEAD [rc=0]
(empty stdout)
$ git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/w919c/src config --get core.abbrev [rc=1]
(empty stdout)
Source unchanged: expected HEAD/tree, clean tracked/index/untracked/ignored state; core.abbrev remains unset on disk.
UTC completed: 2026-10-25T11:47:54.677959+00:00
```

The requested identity still matches; tracked and index diffs are empty, with no untracked or ignored files in `src/`. No source edit, commit, push, GitHub comment, remote call or credential use was performed. Intentional writes were this verdict and reviewer scratch outside `src/`. Read-only treatment was procedural; the runtime does not provide an independently attested read-only mount or a proof that no transient write ever occurred.

**Approve this exact-SHA substantive review: zero open P0, P1, P2 or P3.** All seven round-1 findings and WP919-R2-01 are closed against hash-verified revision 3. This verdict is not merge authorization or a certification of unobserved CI, owner comments, remote freshness or the enclosing launcher/model receipt.

VERDICT: approve
