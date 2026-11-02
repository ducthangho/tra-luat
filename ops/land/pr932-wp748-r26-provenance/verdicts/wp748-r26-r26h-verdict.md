# Independent read-only review — WP748 r26, round 8

**Disposition: changes requested. Open: 0 P0, 0 P1, 0 P2, 1 P3 (R26-TEST-17, continuing the R26-TEST-16 coverage class).** All 37 required cases pass and all 124 registered mutants are killed, but four claimed regex equivalents are distinguishable, two missing range-boundary mutants survive the entire suite, and generator emission can omit a whole family without failing.

Reviewer: OpenAI Codex, as identified by runtime instructions (GPT-6-based agent). Observed surface: tool-mediated local shell, managed Linux x86_64, Python 3.13.16; transport machine. Exact serving model/build, provider attestation and the enclosing launcher execution receipt are not independently visible. User-reported launcher invocation is not receipt verification. No credentials, GitHub access, source edits, source commits, pushes or comments are authorized or used.

Review class: sensitive. Reviewed SHA `41ada5f7e0a0bf34fbd4488c6ec412ff81fe5fff`; tree `b734e3c4f68d9879eb09184941c34b2f5e03f5cf`.

Started UTC: 2026-10-25T14:47:50.860518+00:00

## Identity and scope

Identity gate passed: HEAD/tree exact, detached (`symbolic-ref -q HEAD`: rc 1, no output), full clone (`--is-shallow-repository`: rc 0, false), clean (`status --porcelain=v1`: rc 0, no output). `git -C src log -8 --format='%H %P'` confirms the complete requested chain through b306e15. Command outputs and rc are in `review-r26h-b2Mfroo2/preflight.json`.

Local master spec lookup: rc 128, master absent. Required origin/ops fallback: rc 0, SHA-256 `f20615ae559f377150cfd6a9cfd0bce4478bf28ae3d562a674588a9c6f9d4bdb`, matches. Lease read rc 0; local later-head offline review is permitted. GitHub authority comments #748 issuecomment-6394503720 and issuecomment-6396160332 cannot be read here. Owner's latest ≤1200-added-line/new-delta cap and final review authorization are taken from the explicit user instruction; durable cap comment is pending as disclosed. Publication/unpushed status cannot be independently established offline.

Round eight changes launcher_test.py only. Entire fix touches exactly launcher.py and launcher_test.py. Master-history check `git -C src log --oneline 113e0d1..b306e15a96a4d9d05d2ba4191cbd071fa7820ee7 -- .claude/dev/launcher.py .claude/dev/launcher_test.py`: rc 0, empty.

`git -C src diff --numstat b306e15a96a4d9d05d2ba4191cbd071fa7820ee7 HEAD -- <two files>`: rc 0, +183/-68 launcher.py, +948/-35 launcher_test.py; **1131 added lines**, 69 below 1200. Cumulative from e739ac1: +252/-4 and +1275/-0; **1527 added lines** (reference only). Round eight: **284 added lines**.

## Review procedure

This file was written incrementally. Required cases, all registered mutations, generator equivalence/operator audit and security/regression checks have completed. Scratch artifacts are outside src. No previous-round execution is counted as current evidence.

## Architecture audit — initial confirmed result

Two `_R26_TUONG_DUONG` claims are false (`launcher_test.py:7167`, `:7169`): replacing trailing `\s*` with `\s` or `\s?` is distinguishable on a complete benign frame with two spaces before LF (also tab+space+CRLF). `python3 -B review-r26h-b2Mfroo2/review.py exec equivalence review-r26h-b2Mfroo2/architecture.py equivalence`: rc 0. HEAD retains r0+r1, DO_DUOC, mat=0; each exempt mutant retains only r0, KHONG_DO_DUOC, mat=1. Plain LF/CRLF controls pass. No attack payload was created. All ten exempt variants were applied separately to temporary launcher copies; details are in equivalence-observations.json and logs/equivalence.json. This is an acceptance/test defect, not a demonstrated production leak on HEAD. Final finding and completeness audit follow.

## Current executions

`python3 -B review-r26h-b2Mfroo2/review.py targeted` invokes **every** `python3 src/.claude/dev/launcher_test.py --lap-ca <r925/r926 name> --lan 1`: rc 0, **37/37 pass**, each 1/1, no skips/failures. Generator case: 108.768 s. `... review.py neutral`: rc 0, **37/37** unchanged temporary-copy controls pass. Environment is explicitly rebuilt with a private empty HOME, absent root-level CODEX_HOME, no authentication variables, no global Git config/hooks and no bytecode writes. Only fake children are executed; disposable test repositories/fixture commits are outside src.

`python3 -B review-r26h-b2Mfroo2/review.py mutants`: rc 0, **124/124** unique registered r25/r26 replacements compile and **134/134** designated executions raise the exact target-origin TinHieuChotCa (wrapper rc 42). Wrong-origin signal, unrelated exception, skip, survivor and timeout are separate codes and none occurred. Exact replacements, output, rc, timing and tracebacks are in mutation-inventory.json, mutants.json and logs/. Actual assertion text is retained in mutation-reasons.md.

`... review.py regression`: process rc 0; **10 passed, 1 Windows-only skipped, 0 failed**. This is not 11 passes: the ordinary runner returns 0 on skip. The skipped case is t62 (Windows whole-tree 125). POSIX 125 is measured independently below.

`... review.py exec generated-survey .../architecture.py survey`: completed **151/151** variants across 7 literals, **141 target-origin kills, 10 survivors**, **1011** individual target executions, 0 unrelated exceptions, 0 skips. Reproduced inventory: ANSI 18, header 49, frame 15, candidate 23, whitespace 5, prefix 39, JSON-header 2. All survivors exactly match the supplied exemption keys. Correction to requester claim: the new grammar contract itself kills **118**, with the remaining **23** killed by other existing r925/r926 cases (total remains 141).

Supplemental `python3 -B review-r26h-b2Mfroo2/extra.py`: rc 0, **74/74** executions pass. Independently changing ANSI final range `[@-~]` to `[A-~]` or `[@-}]` survives **37/37 each, including the generator**. These are absent from both generated and registered mutation inventories. Benign ANSI boundary observations distinguish each from HEAD: at its removed endpoint HEAD retains 1 model/no loss; the respective mutant retains 0 and counts mat=1. No attack input was authored.

Generator controls (`... review.py exec <label> .../architecture.py teeth <mode>`): removing the existing tab-separator contract subcase gives rc **42**, two new header survivors; adding a bogus exemption gives rc **42**, stale entry. Disabling **all 18 ANSI variants** gives rc **0**, `GENERATOR_PASSED remove_ansi_family`: 133 variants still exceed the loose threshold, and literal count is incremented before variants are produced. This establishes partial vacuity; it does not claim a wholly empty generator passes.

## Finding — R26-TEST-17 (P3): generated coverage still permits meaningful grammar regressions

**Class:** continuing `unguarded-filter-invariants` / R26-TEST-16. **Locations:** `.claude/dev/launcher_test.py:7165`, `:7166`, `:7167`, and `:7169` (false equivalences), `:7124` and `:7129` (operator coverage), `:7204` and `:7226` (coverage accounting). Affected production grammar is `.claude/dev/launcher.py:1606` and `:1608`.

**Scenario and impact:** the generator passes on HEAD while exempting four distinguishable frame-grammar mutants. A normal complete response frame followed by two spaces and LF is accepted on HEAD; either exempt mutant loses it. The assertion that physical lines end in LF does not imply that the entire suffix after `}` contains at most one whitespace byte. The two closing-brace exemptions also differ: a form-feed or vertical-tab suffix is accepted by production `\s*` outside the JSON capture, but the broader greedy capture consumes it and `json.loads` rejects it. Regex backtracking is not retried in response to a later JSON parsing failure. Independently, changing either endpoint of the ANSI final-byte range survives the complete required suite, including the generator, despite dropping a benign frame at that endpoint. Thus a future grammar regression can remain green under the architecture intended to close this class. This is a test/acceptance defect; it is not a demonstrated credential leak or false positive measurement in current production code.

Evidence, all on temporary launcher copies:

```text
$ python3 -B review-r26h-b2Mfroo2/review.py exec equivalence review-r26h-b2Mfroo2/architecture.py equivalence
HEAD + two_spaces_LF: r0,r1; DO_DUOC; mat=0
_RE_KHUNG trailing \\s: r0 only; KHONG_DO_DUOC; mat=1
_RE_KHUNG trailing \\s?: r0 only; KHONG_DO_DUOC; mat=1
rc=0 (all diagnostic measurements completed)

$ python3 -B review-r26h-b2Mfroo2/extra.py
SUMMARY ansi_final_lower_bound {'0': 37}
SUMMARY ansi_final_upper_bound {'0': 37}
rc=0 (37/37 cases survive for EACH non-equivalent mutant)

$ python3 -B review-r26h-b2Mfroo2/review.py exec teeth-remove-ansi review-r26h-b2Mfroo2/architecture.py teeth remove_ansi_family
GENERATOR_PASSED remove_ansi_family
rc=0
```

The endpoint mutations are exactly `[@-~]` → `[A-~]` and `[@-~]` → `[@-}]`, separately. The generator treats a range as a single class member; it can delete/broaden that member but cannot move either boundary. `observations.json` records HEAD accepting the corresponding benign CSI-prefixed frame (one model, no loss), while the pertinent mutant records zero models and `mat=1`. Both still discard all trace bytes. Their existing-suite results are genuine passes, not crashes or skipped cases.

**Fix location and approach:** extend `_r26_bien_the` with independent range-boundary changes and mandatory-atom optionalization; make emission/accounting explicit per literal and per applicable operator so an omitted family cannot hide behind global minima. Add benign trailing-whitespace (including form-feed/vertical-tab) and ANSI-endpoint observations to the behavioral contract. Remove the four false exemption entries once the new observations kill them; retain stale-entry rejection. Parse/discover the source literals in a way that does not silently omit supported literal forms when the block evolves. Keep production behavior unchanged unless a separate production defect is established.

**Tests to lock it:** valid frames with two spaces before LF and tab+space before CRLF must retain the second model without loss; separately mutate each trailing quantifier and closing-brace capture requirement. Form-feed/vertical-tab suffix controls must remain outside the captured JSON. Independently narrow each ANSI range endpoint and require its own target-origin signal. Disabling emission for any current regex family must turn the generator red. Continue both existing controls: deleting the tab contract subcase and adding a bogus equivalence must fail. Test operator coverage at the generator layer with known input/output variants, as well as behavior at the filter layer.

**Patch risks:** additional operators can produce invalid or genuinely equivalent regexes and increase run time. Distinguish invalid compilation from a kill, justify each remaining equivalent by reachable call-site behavior, and retain neutral controls and wrong-exception rejection. The current generator takes about 109 seconds in the required-case run; account for added cost explicitly. No further Codex call is requested or assumed.

## All ten equivalence claims

The following audit concerns reachable filter behavior, not the private parser called arbitrarily outside its production preconditions. Every listed variant was instantiated separately; expanded benign LF/CRLF/whitespace measurements (66 observations: HEAD plus ten variants, six suffixes each) are in `equivalence-observations.json`.

| Entry | Assessment and proof / distinguishing scenario |
|---|---|
| `_DAU_NHAN`, remove `^` | **Equivalent at current call sites.** `_RE_KHUNG`, `_RE_LOAI_DAU`, and `_RE_DAU_JSON` all use `.match`, which already starts at byte zero. No nonzero-offset match becomes reachable. |
| `_RE_KHUNG`, remove closing `\}` requirement | **Not equivalent.** With a complete valid object followed by form feed or vertical tab and LF, HEAD excludes the suffix from its capture and accepts the model. The mutant greedily captures the non-JSON whitespace, so parsing fails and mat becomes 1. Measured independently. |
| `_RE_KHUNG`, replace closing `\}` with `.` | **Not equivalent.** The same benign suffix distinguishes it: the final dot can consume that byte and leave it inside the JSON capture. The successful regex match does not backtrack after json.loads rejects the captured bytes. |
| `_RE_KHUNG`, trailing `\s` | **Not equivalent.** Two spaces before the terminating LF distinguish it, as measured. |
| `_RE_KHUNG`, trailing `\s+` | **Equivalent on the complete-line production path.** That path requires an actual LF; ANSI removal cannot consume LF. Every accepted line therefore supplies at least one whitespace byte after the object's closing brace, even when `$` can match before the final LF. EOF-cut lines do not enter this parser. |
| `_RE_KHUNG`, trailing `\s?` | **Not equivalent.** Two spaces before LF, or tab+space before CRLF, distinguish it. |
| `_RE_KHOANG_TRANG_B`, `\s` | **Equivalent.** Global substitution with empty bytes removes each whitespace byte, yielding the same result as removing runs. |
| `_RE_KHOANG_TRANG_B`, `\s*` | **Equivalent.** The same nonempty runs are removed; extra zero-length matches replace empty bytes with empty bytes. |
| `_RE_KHOANG_TRANG_B`, `\s?` | **Equivalent.** Global deletion removes the same individual whitespace bytes; empty matches change nothing. |
| `_RE_LOAI_DAU`, opening `\{` → `.` | **Equivalent at current classification call sites.** For `{`, behavior is unchanged. Without `{`, candidate evidence was already handled before this branch; a recognized other prefix may return early, while the original falls through to `_RE_DAU_JSON`, which rejects the missing brace. Neither path stores a model or adds loss/unknown. |

Expanded command: `python3 -B review-r26h-b2Mfroo2/review.py exec equivalence-expanded review-r26h-b2Mfroo2/architecture.py equivalence`, rc **0**; 66/66 observations completed. HEAD accepts all six suffixes; four distinct exempt variants fail their distinguishing suffixes. Result: **6 supported equivalence claims; 4 refuted**. The earlier removed allow-list `het_dong` check is also genuinely redundant: every member of `_STDERR_CHO_PHEP_DONG` ends in LF. The removed top-level `isinstance(ev, dict)` check is redundant under the intact brace-delimited capture and standard `json.loads` without hooks.

## Operator coverage and non-vacuity

All seven current regex literals are discovered, with exactly the 151 variants reported above. The generator rejects uncaught exceptions via `khac`, rejects unknown survivors, and rejects stale exemptions. Fresh instrumentation checked each of its 141 actual kills for the named target in the traceback. There were no wrong-origin or unrelated-error kills. The three excluded slow cases address timeout/reader shutdown; the generator itself is excluded to prevent recursion. The other 33 cases were available to each generated variant, with 0 skips in the measured survey.

A wholly empty generator is rejected by its count assertions. A missing family is not: `ten_hang` is updated before emission, so dropping all 18 ANSI variants still leaves seven names and 133 variants. The control measured that this passes. Likewise, mutating a regex to omit an endpoint leaves the remaining mutation family self-consistent; both endpoint variants passed the generator itself. Overall mutation score is therefore not a completeness proof.

Another concrete omitted operation is making a mandatory atom optional. `_r26_bien_the` changes existing quantifiers but does not insert one after the required ESC introducer. The old round-seven optional-ESC survivor is now **behaviorally killed**: applying only that source mutation and running `python3 -B review-r26h-b2Mfroo2/review.py case r926_hop_dong_ngu_phap_bo_loc_theo_hanh_vi review-r26h-b2Mfroo2/launchers/ansi_optional_escape.py` returns **42**, target line 7024: the existing benign `ga[1m` model becomes `ga`. It is nevertheless absent from generated/registered variants. This is an operator-inventory gap, not a surviving behavioral case. Whole literal-token weakening similarly is not proof of every internal literal boundary; no additional payload-based failure is asserted here.

The supplied claim “141/151 killed by the new behavioral contract” overstates that individual case. Fresh execution measures **118/151** killed there, plus **23/151** by other cases, and **10/151** exempt survivors. The overall kill count is reproduced.

## Non-regex guard inventory and right-reason audit

I re-read the current filter and integration, and extracted `predicate-ast.json`: **71** condition/comparison/boolean/exception syntax entries, including nested duplicates and the unchanged Windows branch. This is not a claim of 71 independent policy guards. The table maps constituent decisions to effective registered removals. Actions that remove exactly the safeguard are acceptable equivalents to negating its predicate; broad legacy mutations are not the sole evidence when separate constituent mutations exist.

| Source / decision | Independent registered coverage |
|---|---|
| 1642 missing counter / supplied counter retained | `r26_rv5_optional_counter_init`; `r26_rv5_retain_caller_counter` |
| 1645 filter error latch; drain; bounded drain; accounting | `r25_bo_loc_hong_khong_ghi_loi`; `r25_bo_loc_hong_khong_xa_ong`; `r25_xa_ong_khong_tran`; `r26_xa_khong_dem` |
| 1656 frame-match dispatch; 1660 parse exception; strict UTF-8 | `r26_rv5_frame_match_guard`; `r26_rv5_exception_valueerror`; `r26_utf8_thay_the` |
| 1663 eligible event; 1666 response object | `r25_moi_su_kien`; `r26_response_khong_kiem_object`; completed-member acceptance additionally `r26_rv6_l_su_kien_bo_completed` |
| 1667 id type/nonblank, model type/nonblank | `r26_id_khong_kiem_chuoi`; `r26_id_khong_strip`; `r26_model_khong_kiem_chuoi`; `r26_model_khong_strip` |
| 1684 retry short writes; 1686 reject zero progress | `r26_ghi_khong_lap`; `r26_ghi_bo_chot_0_byte` |
| 1689 closed sink; 1691 other error; unwritten suffix | `r26_tep_dong_khong_dem`; `r26_ghi_loi_khong_dem`; `r26_ghi_dem_ca_doan` |
| 1699 one chunk AND complete line | `r26_mot_doan_bo_dieu_kien_so_doan`; `r25_parse_khong_can_ca_dong` |
| 1701 parsed model present | `r26_rv5_parsed_model_guard` |
| 1702 dedup entire decision / response id / model | `r26_rv5_dedup_whole`; `r26_rv5_dedup_response_id`; `r25_gop_theo_id` |
| 1704 parsed bad candidate / raw candidate / loss action | `r26_phan_loai_theo_token`; `r26_doc_tron_bo_token`; `r25_bo_dem_mat` |
| 1706 parse-failure condition / JSON header / fallback action | `r26_doc_tron_khong_ro_ca_su_kien_khac`; `r26_doc_tron_khong_ro_khong_doi_json`; `r26_doc_tron_khong_parse_bo_qua` |
| 1709 multi-chunk or EOF candidate loss | `r26_bo_dem_mat_nhieu_doan` |
| 1713 prefix match; 1716 strict decoded prefix | `r26_rv5_prefix_match_guard`; `r26_loai_khong_utf8_thay_the` |
| 1720 decoded type / noncandidate / early return | `r26_rv5_prefix_decoded`; `r26_tien_to_ung_vien_tha`; `r26_bo_xac_nhan_su_kien_khac` |
| 1722 JSON header / unknown action | `r26_khong_ro_moi_dong_dai`; `r26_khong_ro_khong_dem` |
| 1729 bounded read; 1730 reset; 1732 LF | `r25_doc_khong_tran`; `r26_khong_dat_lai_moi_dong`; `r26_rv5_lf_detection` |
| 1734 first chunk / exact raw membership / exact endings | `r25_cho_phep_ca_dong_cut`; `r25_ghi_moi_dong_tron`; `r25_cho_phep_theo_tien_to`; `r26_cho_phep_cat_moi_CRLF`; `r26_rv6_j_bo_CRLF` |
| 1738 first chunk capture | `r26_rv5_first_chunk_capture` |
| 1741 prefix append / bound / nonnegative remainder | `r26_dau_dong_khong_noi`; `r26_tien_to_khong_tran`; `r26_tien_to_bo_max`; constant bound `r26_rv6_i_tran_dau_nho` |
| 1742 whitespace and ANSI normalization / carry | `r26_khong_bo_khoang_trang`; `r26_rv6_h_luong_khong_ansi`; `r26_bo_duoi_vat`; `r26_rv6_g_duoi_ngan`; complete-line ANSI `r25_bo_go_ansi` |
| 1743 sticky candidate / candidate search | `r26_token_khong_dinh`; `r26_rv5_candidate_search` |
| 1745 classify at LF / 1747 EOF-cut | `r26_rv5_classify_only_at_lf`; `r26_bo_dong_cut_EOF` |
| 1754 error; 1756 live reader; 1758 loss; 1760 unknown; 1763 no model | `r25_DO_DUOC_khi_loc_hong`; `r25_DO_DUOC_khi_ong_con_mo`; `r25_DO_DUOC_khi_mat`; `r26_DO_DUOC_khi_khong_ro`; `r25_DO_DUOC_khong_khung` |
| 1782 daemon | `r26_rv7_luong_doc_khong_daemon` |
| 1787 start-failure catch / latch / pipe close | `r26_luong_hong_lot_ra`; `r26_luong_hong_khong_ghi_loi`; `r26_luong_hong_khong_dong_ong` |
| 1795 started thread / 1796 bounded join / latch / close / order | `r26_cho_luong_chua_chay`; `r25_doc_ong_khong_han`; `r25_bo_chot_luong`; `r26_ket_thuc_khong_dong_tep`; `r26_dong_tep_truoc_chot` |
| 1803 unlatched negative / no late sample | `r26_mac_dinh_chua_chot_la_xong`; `r26_lay_mau_lai_luong_muon` |
| 1804 copies of models, errors, counters | `r26_rv7_khong_chup_ket`; `r26_rv7_khong_chup_loi`; `r26_rv7_khong_chup_dem` |
| 1805 error/loss/unknown handoff; 1808 reason | `r25_so_khong_chuyen_loi`; `r25_so_khong_chuyen_mat`; `r26_so_khong_chuyen_khong_ro`; `r26_rv5_reason_guard` |
| 1934 Codex routing both directions | `r26_rv5_codex_mode_disabled`; `r25_loc_ca_luot_khong_phai_codex` |
| 1937 binary selection / 1938 unbuffered | `r26_rv7_tep_stderr_van_ban`; `r26_tep_stderr_co_dem` |
| 1941 environment / exact RUST_LOG override / 1946 record | `r26_rv5_codex_env_guard`; `r25_khong_bat_trace`; `r25_noi_rust_log_thua_ke`; `r26_rv5_rust_override_record` |
| 1956 PIPE / 1958 reader / 2025 finalization / 2030 serialization | `r26_rv5_codex_pipe_guard`; `r26_rv5_codex_reader_guard`; `r26_rv5_finish_object_guard`; `r26_khong_ghi_so` |
| Production close/latch order | `r26_san_xuat_dong_tep_truoc`; `r26_rv5_old_late_production_latch` |

No additional missing **non-regex policy predicate** was established in this scope. Standard bytes-stream EOF iteration is loop mechanics; bounded reads and incomplete-line handling are independently covered. Existing platform/kill/probe predicates outside the new filter are assessed for regression, not newly classified as unregistered filter guards.

All **5/5** `r26_rv7_*` entries make one focused replacement and fail for the corresponding effect. Removing a model copy exposes two records; removing the error copy changes the conclusion; removing the counter copy exposes 99/999 instead of 1/5. Daemon removal takes **41.249 s** including wrapper overhead (case reports 40.6 s), failing its intended <35-second bound. Text mode fails at the directly affected binary/unbuffered open (`ValueError: can't have unbuffered text I/O`), which the designated integration case rejects; no unrelated import/setup error is credited.

Short-write removal fails at `ngan_roi_du`; zero-progress removal independently fails at `tra_0`; missing write-error accounting fails at `ngan_roi_nem` (29 bytes missing from dropped total). UTF-8 replacement fails because a replacement character is retained as model data. The complete-header fallback mutation yields false DO_DUOC on the existing 329-byte invalid-UTF-8/escaped-key fixture and is killed. Streaming ANSI-removal mutation is killed at the existing cap-188 fixture (635 discarded bytes, false DO_DUOC in the mutant).

The two late production-order mutants first fail the close-observation assertion because a second close overwrites the observation. To check the actual evidence consequence, `... review.py exec order-audit .../order_audit.py` records assertions without stopping: rc **0**, **3/3** diagnostic expectations. HEAD passes all three and concludes KHONG_DO_DUOC/open pipe; both mutants also fail the final receipt assertion with **DO_DUOC / None**. Ordinary target-origin kills remain the kill evidence; this diagnosis rules out relying only on incidental fixture timing. No source test was edited.

## Earlier-finding status on 41ada5f7e0a0bf34fbd4488c6ec412ff81fe5fff

| Earlier finding | Current disposition and fresh evidence |
|---|---|
| R25-SEC-01 P1 | **Reported production path remains closed.** Exact-list and sample-secret run-directory cases pass; unrestricted, prefix and continuation mutants die. No raw stderr fallback is present. |
| R25-MEAS-02 P2 | **Reported source/metadata defect remains closed.** Target/position/event, strict UTF-8, typed nonblank id/model and model-aware dedup cases pass; independent mutations fail. Remaining grammar coverage is the P3 finding, not a demonstrated provenance bypass on HEAD. |
| R25-TEST-03 P2 | **The specifically reported surviving removals remain closed.** Generic write-count removal fails at ngan_roi_nem; default-unlatched removal yields wrong DO_DUOC; old late-production-latch removal is killed and its wrong final receipt independently diagnosed. The broader guard-coverage class continues at P3. |
| R25-ROBUST-04 P2 | **Closed for reported unbounded reads.** Both normal-read and error-drain limits are tested; both unbounded mutants fail. Production cap is 4 MiB per read. |
| R25-EVID-05 P2 | **All specifically reported paths stay closed.** Every-cut/whitespace/EOF cases require actual loss. Unparseable complete JSON receive headers require unknown counts; removing that fallback fails on the existing 329-byte fixture with false DO_DUOC. |
| R25-RACE-06 P2 | **Reported production defect remains closed.** Join-boundary latch, no late resampling and copy-consistent evidence tests pass. Each of the three snapshot removals is now separately registered and killed. |
| R25-CONTRACT-07 P2 | **Closed under superseding v2.** Dropping non-allow-listed Codex diagnostics is explicitly authorized. Non-Codex stderr and log-hash regressions pass. |
| R26-ALLOW-08 P3 | **Closed.** Exact LF/CRLF case passes; repeated-CR normalization mutant fails at CR_CRLF; continuation equal to an allow-list line cannot be written. |
| R26-COUNT-09 P3 | **Closed under native unbuffered contract.** Fresh real FileIO probe: 43 input = 10 stored + 33 dropped, OSError latched. Short/zero/error/closed-sink/drain/suffix/unbuffered mutations fail. |
| R26-EOF-10 P3 | **Closed for finish-during-close.** Actual 10-second integration passes; object and production-order mutants die, and diagnostic confirms their wrong final DO_DUOC. |
| R26-CLASSIFY-11 P3 | **Reported known-other-event regression remains closed.** All-cap known-other, unknown-header, prefix decode and Binary/Ping controls pass; corresponding mutations fail. |
| R26-TEST-12 P3 | **Closed.** Zero-progress removal fails specifically at tra_0, independently of short-write retry removal at ngan_roi_du. |
| R26-TEST-13 P3 | **Both reported predicates remain closed.** Single-chunk and complete-other-event-condition removals fail their intended targets. |
| R26-TEST-14 P3 | **All listed omissions remain closed.** All 23 r26_rv5 entries have target-origin kills; the previously duplicated omissions are also covered. |
| R26-TEST-15 P3 | **Its specific listed omissions remain covered.** All 24 r26_rv6 entries have intended target signals, including streaming normalization, required TRACE, object shape and end anchor. This does not establish complete regex operator coverage. |
| R26-TEST-16 P3 | **Partially addressed; architecture does not close the class.** Five non-regex additions are individually killed. Independent colon whitespace, candidate-key/quote, literal header and ordinary-text/ANSI cases now have effective observations. Trailing grammar still has four false equivalence exemptions; range-endpoint regressions survive every case; emission can omit a family and pass. Continuing open class is consolidated in R26-TEST-17, not double-counted. |
| Unreachable `bo_loc is None` failed-start note | **Remains resolved.** Real Popen failure returns rc 2/hong/null child exit before filter serialization; no model/drop keys. Reader-start failure is a separate negative-evidence path and is measured. |

“Closed” above refers to the reported defect and measured scenarios. It is not a universal proof over every possible input. No earlier source finding is silently reopened merely because the stronger current coverage claim fails.

## Security and regression assessment

`python3 -B review-r26h-b2Mfroo2/review.py exec observations review-r26h-b2Mfroo2/observations.py`: rc **0**, `OBSERVATIONS PASS`. The observations script was inadvertently invoked a second time under the label `integrity-interim`; that duplicate also returned 0, is retained in the ledger, and is not counted as an additional independent experiment or an integrity check.

| Boundary | Evidence and limits |
|---|---|
| Trace/credential content to disk | The only filter write receives a raw exact allow-list member at the first chunk of a physical line. Comparison precedes ANSI/whitespace normalization. Existing ordinary/sample-secret, invalid-byte, partial, prefix/suffix, CR-only, repeated-CR and continuation fixtures pass. Only a prefix of an allowed constant can be persisted by a short write. No raw trace spool or fallback write was found. |
| Complete single-chunk classification | Strict complete parsed candidate with valid metadata is retained and deduplicated. Bad parsed candidate or raw candidate signal counts loss; otherwise an unparseable receive header with a JSON opening brace counts unknown. The parsed-other-event condition prevents its incorrect unknown classification. |
| Multiple chunks and EOF-cut | One classification occurs at physical LF or final EOF. Sticky candidate signal counts loss; without it, confirmed other-event prefix is ignored; unconfirmed JSON receive header counts unknown. Supplied tests cover all four documented paths and every cut in their fixtures. |
| Cross-boundary evidence | Whitespace compaction, ANSI cleanup, 64-byte carry and sticky candidate are tested separately, including existing completed/tab/ANSI cut sweeps. No claim is made for every possible escaped/duplicate event-key or arbitrarily split ANSI input. |
| DO_DUOC | Requires positive retained model evidence, no reader error, latched completion, no loss and no unknown count. Unlatched defaults negative. Every explicit condition and evidence handoff has an effective supplied mutant. Selected response metadata is intentionally stored by the spec. |
| Error drain / after close | Drain remains bounded and counted. Only exception class names enter filter error evidence. Closed-output writes count the unwritten allowed suffix. A live reader already latched incomplete cannot later make the result positive. Counters measure bytes actually consumed, not unread child output. |
| Write accounting | Actual unbuffered FileIO with a ten-byte file-size ceiling measures **43 = 10 stored + 33 dropped**, error `OSError`. This substantiates the documented native contract, not arbitrary custom/buffered sinks. |
| Join boundary | `ket_thuc(10)` joins, samples liveness, then closes. Real inherited-pipe and finish-during-close cases pass. Unbounded join takes **40.882 s** including wrapper overhead and fails; daemon removal fails independently. No independent worker EOF timestamp proves a sub-scheduling-window deadline between join return and liveness sampling. |
| Run directory / hashes | Independent benign fake-child run contains exactly run.json/stdout.log/stderr.log. Stored stderr is **39 bytes**, receipt stderr_byte is **39**, SHA-256 is **1aa26269eb1cc57f86b235a03cda53c004edb5b1e9fc99d4da4f00843293d721**, equal to receipt; **186** trace bytes counted dropped. The sample-secret case independently scans all retained files. stderr_byte/hash retain their persisted-byte semantics. |
| Other sinks | Existing stdout, prompt snapshots, child-owned files and selected id/model/event metadata are outside an absolute “no data anywhere on disk” guarantee. This review establishes the stderr allow-list path, not a universal all-process guarantee. No authenticated Codex execution occurred. |
| Timeout / kill | Required fake-Codex timeout returns **124** and retains earlier model evidence. POSIX tree-kill regressions pass. Independent real kill followed by deliberately withheld whole-tree confirmation returns launcher=receipt **125**, giet_tron_ven=false, one model retained; no child intentionally left alive. Windows-only t62 is skipped and not counted as pass. |
| Windows | creationflags and Job Object production logic are unchanged. t79/t80/t81/t83 mocks and decoding regression pass. codex/codex.exe/codex.cmd/CODEX.CMD identify true; Python false. Exact allow-list CRLF and model-frame CRLF work. Native Windows launch, Job Object/handle inheritance, `.cmd` execution and Windows CI remain **not_run/unverified**. |
| Non-Codex | Required unchanged-stderr/no-extra-fields case passes. PIPE, binary/unbuffered sink and RUST_LOG replacement remain Codex-only. r14 log-hash regression passes. |
| Popen failure | Absent executable with explicit probe-bypass reason: rc **2**, receipt hong, null ma_thoat, no model/drop keys. Failed spawn cannot reach positive filter serialization. |
| Reader start failure | Actual lenh_run with Thread.start forced to raise RuntimeError closes the read pipe and completes. Fake Python child's broken-stderr rc **120** is preserved; receipt **KHONG_DO_DUOC / RuntimeError**, **0** stored/**0** observed dropped bytes. No deadlock or positive measurement. |

No new exploit payload was authored. Further payload-dependent directions, stated only in words: examine escaped or duplicate event-type fields in oversized records, unusually long or split ANSI normalization sequences, and nested candidate-like material in parsed noncandidate events. They are not presented as demonstrated production findings.

The complete repository Linux gate/full launcher suite, native Windows lane and authenticated live-Codex acceptance are **not_run**. The requested offline cases/mutations and documented local regressions are measured. Missing external acceptance evidence is not represented as a passing gate; this review grants no merge, land, deployment or further review-call authority.

## Final integrity and evidence index

`python3 -B review-r26h-b2Mfroo2/review.py exec final-integrity review-r26h-b2Mfroo2/integrity.py`: rc **0**, `FINAL INTEGRITY PASS`. Exact HEAD/tree, detached/full/non-bare status retained. Working/staged diff, delta whitespace check and connectivity fsck each rc **0**, empty output. Partial-clone/promisor config query rc **1**, no matches. Working source matches committed blobs **2/2**; unchanged kill/Job Object/name/hash components are AST-identical to b306e15 **6/6**. Registered replacements independently reconstruct **124/124**, designated result inventory matches **134/134**, temporary Python files compile **292/292**, and companions match source **2/2**. Final readback again confirms clean source including ignored files, exact HEAD/tree and empty intervening-master history (all rc 0).

Source SHA-256:

- launcher.py: `51342501e0126611f81748f614ef2246a7d87069b57ace67e72200a28862a7a1`
- launcher_test.py: `81601988c0c21ab56056a2e224b1ce67e9dc1a132f1d40efead061fcee4e34a9`

The historical delta explicitly named in the prompt, b306e15 → 0fe659e, is **640 additions** (+182 launcher.py, +458 launcher_test.py), rc 0. This review includes subsequent fixes through the requested HEAD: **1131 new-delta additions ≤1200** (69 spare); **1527 cumulative additions** from e739ac1 for reference; **284 additions** in round eight alone. All counts concern exactly the two authorized files. Size is not a finding under the latest user-supplied cap.

Fresh execution totals:

| Work | Result |
|---|---|
| Required CLI cases | **37/37 passed**: 15 r925, 22 r926; rc 0 |
| Registered mutations | **124/124 killed**, **134/134** intended target signals; driver rc 0, each target wrapper rc 42 |
| Neutral temporary-copy controls | **37/37 passed**, rc 0 |
| Generated mutation survey | **151/151 measured**, 141 intended signals, 10 exempt survivors; 1011 target executions, 0 other errors/skips; rc 0 |
| Claimed equivalents | **10/10 reviewed**, 66 benign observations; **4 refuted, 6 supported**; diagnostic rc 0 |
| Additional endpoint variants | **2/2 non-equivalent survivors**, **74/74** suite executions pass, including both generator runs; rc 0 |
| Generator negative controls | Removed contract subcase and bogus exemption rejected, rc 42 each; omitted ANSI family incorrectly accepted, rc 0 |
| Additional regression cases | **10 passed, 1 Windows-only skipped, 0 failed**; runner rc 0 |
| Runtime and order diagnostics | Observations rc 0; **3/3** order expectations, rc 0 |
| Integrity | rc 0; source unchanged |

Evidence is retained in [review-r26h-b2Mfroo2/](review-r26h-b2Mfroo2/): `commands.jsonl` contains 303 parsed command records with stdout/stderr/real rc/duration; `targeted.json`, `neutral.json`, `mutants.json`, `mutation-inventory.json` and `mutation-reasons.md` preserve all required case/registered-mutation evidence. `generated.json` retains per-variant source path, target attempts, exact assertion and origin classification; `extra.json`/`extra-inventory.json` retain the two surviving endpoint variants. `equivalence-observations.json`, the `logs/teeth-*.json` controls, `observations.json`, `order-audit.json`, `predicate-ast.json`, `size.json`, `preflight.json`, `final-integrity.json` and `last-readback.json` retain the remaining measurements. All drivers and temporary launchers remain outside src. The separately reported optional-ESC target command and its real rc 42 are recorded above; it is not included in the 303 driver-ledger records.

Runtime instructions identify **OpenAI Codex, GPT-6-based**, provider `openai_codex`, model family `openai`; observed execution is a tool-mediated shell in managed Linux, transport `machine`. Exact serving model/build/effort, session attestation, enclosing CLI-versus-service identity and the outer launcher execution receipt remain **not independently verified**. GitHub authority/publication/CI were not accessed. No credentials, source edits, source commits, pushes or GitHub comments; no subagents. Disposable fixture commits made by the requested tests are outside src. Read-only source handling is a maintained review procedure, not an independently attested mount property.

The architecture improves coverage but does **not** close the continuing class on this HEAD. Earlier reported production fixes remain effective on their measured scenarios. Open counts: **0 P0, 0 P1, 0 P2, 1 P3**. The owner's zero-P0–P3 criterion is not met.

Completed UTC: 2026-10-25T15:07:45.409082+00:00.

VERDICT: changes_requested
