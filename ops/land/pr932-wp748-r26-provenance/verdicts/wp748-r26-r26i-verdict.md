# WP748 r26 round 9 independent read-only review

**Disposition: approve. Open: 0 P0, 0 P1, 0 P2, 0 P3.**

Reviewer: OpenAI Codex, as identified by this session's developer/runtime instructions. The exact serving model build, launcher execution receipt, and remote authority are not independently verified. No GitHub access or credentials will be used. Review Class: sensitive.

Reviewed SHA: `3877d463c0d9b7a0757d051d547c824814601370`. Tree: `71493dad49d8b61bb52317cb399cc569f94099a1`. Detached, full (non-shallow), initially clean clone; all eight parent links through master `b306e15a96a4d9d05d2ba4191cbd071fa7820ee7` match. Local branch `agent/wp748-r26-claude` exists; no claim of remote push state is independently verified.

Identity commands: `git -C src rev-parse HEAD HEAD^{tree}` (rc 0, exact values above); `git -C src symbolic-ref -q HEAD` (rc 1, detached); `git -C src rev-parse --is-shallow-repository` (rc 0, `false`); `git -C src status --short` (rc 0, empty); `git -C src log -9 --format='%H %P'` (rc 0, supplied chain confirmed).

Scope/size commands (rc 0): `git -C src diff --numstat b306e15a96a4d9d05d2ba4191cbd071fa7820ee7 HEAD`: launcher.py +183/-68; launcher_test.py +1007/-35, exactly these two files; **1190 added lines**, within supplied 1300 cap. From `e739ac1b74024a20949425c447fb6cf025317c0e`, same files: +252/-4 and +1334/-0 = **1586 cumulative added lines**. Round 9 only: launcher_test.py +67/-8. `git -C src log --oneline 113e0d1..b306e15a96a4d9d05d2ba4191cbd071fa7820ee7 -- .claude/dev/launcher.py .claude/dev/launcher_test.py` is empty.

Authority comments #748 issuecomment-6394503720, -6396160332 and -6399648861 are user-supplied; GitHub cannot be consulted within this review.

Started UTC: 2026-10-25T15:43:52.475068+00:00

Spec/lease: local master lookup rc 128 (master absent); prescribed origin/ops fallback rc 0, SHA-256 `f20615ae559f377150cfd6a9cfd0bce4478bf28ae3d562a674588a9c6f9d4bdb` matches. Lease permits later local heads and offline review before push/gates; expires 2026-10-26T06:48:19Z. Supplied latest owner cap and ninth-call authority supersede earlier numeric limits for this review; remote comments remain unverified.

Execution evidence is being retained in `review-r26i-AgFeVkSE/`. Final test subprocesses receive an explicit minimal environment, a verified absent root-level fixture HOME, no credential variables, disabled global/system Git config and no bytecode writes. Fake children and disposable fixture repositories are outside src.

Initial execution setup failed: private empty HOME was below an enclosing repository; the pre-existing credential-store guard rejected that location before fake Codex ran (30/38 CLI cases passed; 26/134 mutant executions did not produce target signals). No credential was supplied or used. This reviewer fixture error is corrected by using a fresh `/tmp` empty home outside repositories. First-attempt results are preserved under `first-attempt/`; none count toward final measurements.

Setup follow-up: `/tmp` itself has a `.git` marker, so moving the empty home within `/tmp` was insufficient. The second run reproduced the same prefilter setup failures (preserved under `second-attempt/`). The final fixture HOME now names a verified nonexistent root-level path, so the guard reaches FileNotFoundError before any repository/credential location. No real credential path is read; root filesystem is not modified.

## Measured execution results

Final clean-environment run: `python3 -B review-r26i-AgFeVkSE/review.py targeted` rc **0**, invokes every required `python3 src/.claude/dev/launcher_test.py --lap-ca <name> --lan 1`: **38/38 pass**, each 1/1 with zero skips. `... review.py neutral` rc **0**, **38/38** unchanged temporary-copy controls pass.

`... review.py mutants` rc **0**: **124/124** registered r25/r26 replacements match uniquely, compile and are killed; **134/134** designated executions return wrapper rc **42**, exclusively for `TinHieuChotCa` with the designated case in the traceback. No wrong-origin signals, unrelated errors, skips, survivors or timeouts are credited. Exact replacements and target assertions are retained in mutation-inventory.json, mutants.json and mutation-reasons.md.

`... review.py exec generated-survey review-r26i-AgFeVkSE/architecture.py survey` rc **0**: independent AST census agrees with textual discovery, **7/7 literals**, **207 variants**, **1030 target invocations**, **200 target-origin kills / 7 survivors**. Survivors exactly equal the seven listed equivalents. The grammar-contract case kills **175**, other cases kill **25**; no claim that the contract alone kills all 200.

Generator teeth, each real rc **42** from its own generator assertion: omit all ANSI emission → per-literal count mismatch; add bogus equivalent → stale exemption; remove the tab-separator contract subcase → two unlisted surviving variants. Commands: `... review.py exec teeth-omit-ansi .../architecture.py teeth omit-_RE_ANSI_B`; same form for `teeth-bogus-equivalent`/`bogus-equivalent` and `teeth-drop-subcase`/`drop-contract-subcase`. **3/3 controls turn red for the intended reason.** These controls alter only scratch/in-memory test code.

`... review.py regression` rc **0**, **9 passed / 1 Windows-only skipped / 0 failed** (10 selected cases; t62 is the skip, not a pass). `... review.py exec observations .../observations.py` rc **0**, `OBSERVATIONS PASS`: native unbuffered accounting, exact line endings, old cut positions, stored-log hashes, Popen failure, actual run with reader-start failure, and POSIX 125 measured. Detailed observations follow in the final audit.

## Round-8 closure and generator audit

**R26-TEST-17 P3 is closed on this SHA.** The four former false equivalents are no longer exempt. The generated variants removing/replacing the closing brace fail at `form_feed`; the two trailing-quantifier variants fail at `hai_cach_LF`. Independently narrowing the ANSI final range at either end fails at `ansi_ket_at` or `ansi_ket_nga`. Optionalizing ESC fails because the existing benign model `ga[1m` is changed to `ga`. **7/7 specific variants produce target-origin signals**, all in `r926_hop_dong_ngu_phap_bo_loc_theo_hanh_vi`; exact variants/messages are in `round8-closure.json`. No new exploit input was authored.

The generator's finite operation inventory was read independently: token deletion; class/escape/punctuation widening to dot; whitespace escape to literal space; literal-word widening to `\S+`; quantifier removal and `*`/`+`/`?` changes; class-member deletion and negation removal; independent inward range-endpoint shifts; optionalization of mandatory atoms (grouping literal words); atom-plus-quantifier deletion; and independent alternation-branch deletion. The current seven literals are all discovered; an independent AST constant census agrees 7/7. No current literal is hidden by the line-based discovery. Per-literal expected counts are ANSI **29**, header **67**, frame **19**, candidate **33**, whitespace **6**, prefix **50**, JSON header **3**. The count-table equality prevents any current family from being silently omitted. This is an audit of the current grammar and stated finite operators, not a claim to enumerate every possible regex edit.

`python3 -B review-r26i-AgFeVkSE/review.py exec operator-audit review-r26i-AgFeVkSE/operator_audit.py`: rc **0**. Removing each of the generator-layer case's **19** expected emissions independently causes that case's own `TinHieuChotCa` (**19/19**); the unchanged control passes. The full generator's measured runtime was **141.391 s** in the CLI run; timing reflects this Linux environment and concurrent independent review measurements.

All seven equivalence claims were separately instantiated in the survey and survived the available target cases. Their supporting proofs concern reachable production calls:

| Equivalent | Reason |
|---|---|
| Header without leading `^` | Every derived header regex is used with `.match(sach)`, without a nonzero starting position. Removing `^` cannot admit a later header. |
| Frame trailing `\s+` replacing `\s*` | The parser is entered only for a complete single-chunk physical line. That line includes LF; ANSI removal cannot consume LF, and the captured object ends before it. At least one suffix whitespace byte is therefore always available. EOF-cut input never enters this parser. |
| Whitespace `\s` | Empty replacement of every individual whitespace byte equals deletion of each whitespace run. |
| Whitespace `\s*` | Removes the same nonempty runs; additional empty matches replace nothing with nothing. |
| Whitespace `\s?` | Removes individual whitespace bytes; empty matches have no effect. |
| Prefix opening brace replaced by dot | With an opening brace, behavior is unchanged. Without it, candidate evidence has already been handled; an extra noncandidate-prefix match may return early, but the original falls through to a JSON-header check that also rejects the absent brace. Neither path stores a model or adds loss/unknown. |
| Prefix opening brace optional | The same proof applies: existing-brace matches are unchanged; absent-brace matches cannot change the final classification because the independent JSON-header check requires the brace. |

The former allow-list `het_dong` predicate is redundant because **every** exact allowed wire form ends in LF. The removed `isinstance(ev, dict)` is redundant under the intact object-delimited capture and standard `json.loads` with no custom hooks: a successful parse of that capture yields a dict. Neither is being excused merely because its mutant survives.

## Current non-regex predicate inventory

Fresh AST extraction is in `predicate-ast.json`; nested AST entries are not counted as independent policy rules. The following maps each policy decision/component to focused registered mutations. The complete replacement/target mapping is in `mutation-inventory.json`; every listed registered target was measured on this head. Legacy aggregate mutations remain, but separate constituent mutations supply the independent evidence.

| Production line / decision | Focused mutant(s) |
|---|---|
| 1642 optional counter initialization / caller counter preservation | `r26_rv5_optional_counter_init`, `r26_rv5_retain_caller_counter` |
| 1645–1649 reader error record / bounded drain / drain accounting | `r25_bo_loc_hong_khong_ghi_loi`, `r25_bo_loc_hong_khong_xa_ong`, `r25_xa_ong_khong_tran`, `r26_xa_khong_dem` |
| 1656 regex match required; 1659 strict decode; 1660 parse-error fallback | `r26_rv5_frame_match_guard`, `r26_utf8_thay_the`, `r26_rv5_exception_valueerror` |
| 1663 accepted event set | `r25_moi_su_kien`, `r26_rv6_l_su_kien_bo_completed` |
| 1666 response object; 1667 id/model string and nonblank checks | `r26_response_khong_kiem_object`, `r26_id_khong_kiem_chuoi`, `r26_id_khong_strip`, `r26_model_khong_kiem_chuoi`, `r26_model_khong_strip` |
| 1684 repeat short writes; 1686 zero-progress guard | `r26_ghi_khong_lap`, `r26_ghi_bo_chot_0_byte` |
| 1689 closed sink; 1691 generic failure and unwritten suffix | `r26_tep_dong_khong_dem`, `r26_ghi_loi_khong_dem`, `r26_ghi_dem_ca_doan` |
| 1699 one chunk AND complete physical line | `r26_mot_doan_bo_dieu_kien_so_doan`, `r25_parse_khong_can_ca_dong` |
| 1701 parsed model exists | `r26_rv5_parsed_model_guard` |
| 1702 dedup whole rule / response-id / model constituents | `r26_rv5_dedup_whole`, `r26_rv5_dedup_response_id`, `r25_gop_theo_id` |
| 1704 parsed bad candidate / raw candidate / loss action | `r26_phan_loai_theo_token`, `r26_doc_tron_bo_token`, `r25_bo_dem_mat` |
| 1706 no parsed event / JSON header / unknown fallback | `r26_doc_tron_khong_ro_ca_su_kien_khac`, `r26_doc_tron_khong_ro_khong_doi_json`, `r26_doc_tron_khong_parse_bo_qua` |
| 1709 multichunk/EOF candidate loss | `r26_bo_dem_mat_nhieu_doan` |
| 1713 prefix match; 1716 strict prefix decode | `r26_rv5_prefix_match_guard`, `r26_loai_khong_utf8_thay_the` |
| 1720 decoded prefix / noncandidate prefix / early return | `r26_rv5_prefix_decoded`, `r26_tien_to_ung_vien_tha`, `r26_bo_xac_nhan_su_kien_khac` |
| 1722 JSON header / unknown increment | `r26_khong_ro_moi_dong_dai`, `r26_khong_ro_khong_dem`, `r26_khong_ro_khong_doi_json` |
| 1729 bounded read; 1730 new-line reset; 1732 actual LF | `r25_doc_khong_tran`, `r26_khong_dat_lai_moi_dong`, `r26_rv5_lf_detection` |
| 1734 first chunk / raw exact allow-list / exact CRLF forms | `r25_cho_phep_ca_dong_cut`, `r25_ghi_moi_dong_tron`, `r25_cho_phep_theo_tien_to`, `r26_cho_phep_cat_moi_CRLF`, `r26_rv6_j_bo_CRLF` |
| 1738 first-chunk capture | `r26_rv5_first_chunk_capture` |
| 1741 prefix append / upper bound / nonnegative remainder | `r26_dau_dong_khong_noi`, `r26_tien_to_khong_tran`, `r26_tien_to_bo_max`, `r26_rv6_i_tran_dau_nho` |
| 1742 whitespace/ANSI normalization; 1744 cross-boundary carry | `r26_khong_bo_khoang_trang`, `r26_rv6_f_chi_dau_cach`, `r26_rv6_h_luong_khong_ansi`, `r26_bo_duoi_vat`, `r26_rv6_g_duoi_ngan` |
| 1743 sticky candidate / new candidate search | `r26_token_khong_dinh`, `r26_rv5_candidate_search` |
| 1745 classify at LF; 1747 classify incomplete EOF | `r26_rv5_classify_only_at_lf`, `r26_bo_dong_cut_EOF` |
| 1754 error / 1756 reader incomplete / 1758 loss / 1760 unknown / 1763 no positive frame | `r25_DO_DUOC_khi_loc_hong`, `r25_DO_DUOC_khi_ong_con_mo`, `r25_DO_DUOC_khi_mat`, `r26_DO_DUOC_khi_khong_ro`, `r25_DO_DUOC_khong_khung` |
| 1782 daemon; 1787 start failure catch / error / pipe close | `r26_rv7_luong_doc_khong_daemon`, `r26_luong_hong_lot_ra`, `r26_luong_hong_khong_ghi_loi`, `r26_luong_hong_khong_dong_ong` |
| 1795 join only started thread; 1796 bounded join; 1797 latch; 1798 close/order | `r26_cho_luong_chua_chay`, `r25_doc_ong_khong_han`, `r25_bo_chot_luong`, `r26_dong_tep_truoc_chot`, `r26_ket_thuc_khong_dong_tep` |
| 1803 unlatched incomplete / no late resampling | `r26_mac_dinh_chua_chot_la_xong`, `r26_lay_mau_lai_luong_muon` |
| 1804 three snapshot copies | `r26_rv7_khong_chup_ket`, `r26_rv7_khong_chup_loi`, `r26_rv7_khong_chup_dem` |
| 1805 error/loss/unknown handoff; 1808 reason | `r25_so_khong_chuyen_loi`, `r25_so_khong_chuyen_mat`, `r26_so_khong_chuyen_khong_ro`, `r26_rv5_reason_guard` |
| 1934 Codex routing in both directions; 1937 binary/unbuffered sink | `r26_rv5_codex_mode_disabled`, `r25_loc_ca_luot_khong_phai_codex`, `r26_rv7_tep_stderr_van_ban`, `r26_tep_stderr_co_dem` |
| 1941 scoped env; 1945 exact RUST_LOG replacement; 1946 override record | `r26_rv5_codex_env_guard`, `r25_khong_bat_trace`, `r25_noi_rust_log_thua_ke`, `r26_rv5_rust_override_record` |
| 1956 pipe routing; 1958 start reader | `r26_rv5_codex_pipe_guard`, `r26_rv5_codex_reader_guard` |
| 2025 finalize / production order; 2030 serialize evidence | `r26_rv5_finish_object_guard`, `r26_san_xuat_dong_tep_truoc`, `r26_rv5_old_late_production_latch`, `r26_khong_ghi_so` |

No additional unguarded filter policy decision was established. Standard bytes-stream EOF iteration is loop mechanics; bounded reads and unfinished physical-line handling have independent mutations. Unchanged platform/probe/kill predicates are regression scope, not new filter predicates.

Right-reason qualifications: unrestricted writing first fails model status in its integration target, but the exact-list target directly observes forbidden sample bytes. Type-guard removals can cause errors *inside the filter*; their target assertions reject that incorrect classification instead of crediting an escaped setup exception. Text-sink mutation directly conflicts with `buffering=0`, causing `ValueError: can't have unbuffered text I/O`; its target asserts the failed launcher exit, and the neutral run succeeds. The short-write and zero-progress mutations fail independently at `ngan_roi_du` and `tra_0`.

`... review.py exec order-audit .../order_audit.py`, rc **0**, **3/3** diagnostic expectations: the two late-production-order mutants initially fail the close-observation assertion because their second close overwrites the observation. Non-stopping diagnostic assertion capture also reaches their final receipt assertion: both incorrectly produce **DO_DUOC / None**, while head produces **KHONG_DO_DUOC / open pipe**. The ordinary target signals remain the mutation-kill evidence; this diagnostic verifies the underlying evidence regression.

## Earlier findings on 3877d463c0d9b7a0757d051d547c824814601370

| ID / earlier severity | Current status and evidence |
|---|---|
| R25-SEC-01 P1 | **Closed.** Exact-list and sample-secret run-directory cases pass; unrestricted, prefix, partial/continuation and RUST_LOG mutations fail. No raw stderr fallback/spool found. |
| R25-MEAS-02 P2 | **Closed.** Source/position/event, strict UTF-8, id/model type/nonblank and dedup cases pass; constituent mutations fail. Format provenance is checked; cryptographic server identity is not claimed. |
| R25-TEST-03 P2 | **Closed.** The three round-2 surviving removals are independently killed: generic failed-write accounting at `ngan_roi_nem`; default-unlatched state at wrong DO_DUOC; late production latch at close ordering and, in the diagnostic, wrong final DO_DUOC. Strict decode and error/loss handoffs also fail their targets when removed. |
| R25-ROBUST-04 P2 | **Closed.** Normal/error-drain reads are bounded at 4 MiB; both unbounded-read mutations fail their own targets. |
| R25-EVID-05 P2 | **Closed for the reported classification/cut paths.** All-cut sweeps pass; caps 256/330/340/350/360 on the old continuation fixture each record `mat=1`, one model and KHONG_DO_DUOC (632 bytes dropped). Complete unparseable JSON-header fixtures count `khong_ro`; removing that fallback incorrectly produces DO_DUOC and is killed. |
| R25-RACE-06 P2 | **Closed.** Latch precedes the three copies; status and serialized evidence use the copies. Latch, resampling and each individual snapshot mutation fail. |
| R25-CONTRACT-07 P2 | **Closed under superseding v2.** Dropping all other Codex diagnostics is authorized policy; non-Codex stderr remains unchanged in the measured case. |
| R26-ALLOW-08 P3 | **Closed.** LF 39/39 and CRLF 40/40 stored; CR-CR-LF 0/41, CR-only EOF 0/39, no-terminator EOF 0/38. A continuation equal to the allowed line is rejected. The repeated-CR mutation fails at `CR_CRLF`. |
| R26-COUNT-09 P3 | **Closed under the documented native unbuffered contract.** Real FileIO + file-size limit gives 43 input = 10 stored + 33 dropped and OSError; short writes, zero progress, suffix accounting, drain, closed sink and buffering changes have independent effective mutations. |
| R26-EOF-10 P3 | **Closed.** Actual 10-second join/finish-during-close case passes. Object and production order mutations fail; diagnostic final status distinguishes head from both late-order variants. |
| R26-CLASSIFY-11 P3 | **Closed for the reported cases.** Other-event sweeps and Binary/Ping controls pass; classification mutations fail without silently substituting loss for unknown. |
| R26-TEST-12 P3 | **Closed.** Zero-progress removal fails at `tra_0`; short-write-loop removal fails separately at `ngan_roi_du`. |
| R26-TEST-13 P3 | **Closed.** One-chunk predicate removal and complete-other-event predicate removal each fail their intended target. |
| R26-TEST-14 P3 | **Closed.** All 23 `r26_rv5_*` entries independently match, compile and produce target-origin failures; the two prior duplicates retain their existing coverage. Fresh predicate census above found no additional non-regex policy omission. |
| R26-TEST-15 P3 | **Closed.** All 24 `r26_rv6_*` entries fail their targets, including each reported grammar/normalization component. Generated coverage supplements their hand-written inventory. |
| R26-TEST-16 P3 | **Closed.** Five `r26_rv7_*` mutations cover daemon, binary sink and three copies; independently generated grammar mutations cover the earlier separator, word, key, quote, colon and trailing-grammar omissions. |
| R26-TEST-17 P3 | **Closed.** Four false equivalents removed and killed; both ANSI range-endpoint variants and optional ESC generated and killed; per-literal omission control fails; generator-layer operation controls fail; all seven retained equivalents have reachable-call-site proofs. Measured kill attribution is 175 contract + 25 other cases. |
| Unreachable `bo_loc is None` failure-path note | **Resolved as nonfinding.** Absent executable returns 2 with `hong`, null child exit and no model/drop keys; it exits before successful final evidence serialization. |

The continuing class `unguarded-filter-invariants` (R25-TEST-03 and R26-TEST-12 through -17) is **closed in the reviewed filter scope**. The other earlier classes—stderr disclosure, provenance, unbounded reads, discarded-evidence completeness, snapshot race, superseded contract, nonliteral allow-list, discard accounting, late EOF and noncandidate classification—remain closed on the measurements above. No new or reopened class is established. This disposition does not equate finite mutation coverage with proof of every possible input or code edit.

## Security and regression assessment

The only filtered stderr write receives raw bytes equal to an allowed complete wire form and only as the first chunk of a physical line. Comparison precedes ANSI/whitespace normalization. Partial, repeated-CR, prefixed/suffixed, oversized and continuation bytes are discarded; error draining never sends raw content to another sink. A short write can persist only a prefix of an allowed constant. Error details stored by the filter are exception class names. Existing sample-secret tests scan the run directory and pass.

Complete single-chunk lines require strict header/object parsing; bad candidate metadata or candidate-token evidence increments loss, while otherwise-unparseable JSON receive headers increment unknown. Multichunk/EOF-cut lines classify once at the physical boundary: sticky candidate evidence → loss; confirmed other prefix → no loss/unknown; unconfirmed JSON receive header → unknown. The whitespace-normalized 64-byte carry and sticky flag cover the supplied cross-boundary sweeps, including ANSI and tabs. Positive measurement requires a retained model, no error, latched reader completion, no loss and no unknown count.

`ket_thuc(10)` joins, samples liveness, then closes the output. A reader still live at that boundary cannot later certify completion. The supplied inherited-pipe test passes; removing bounded join or the daemon flag takes about 40 seconds and fails its elapsed-time target. A closed sink counts the allowed-but-unwritten suffix; unbuffered short-write accounting is measured against an actual file. Counters describe consumed/discarded chunks and bytes at snapshot time, not unread future pipe data. The test seam verifies ordering around close; it does not timestamp EOF independently inside the scheduling interval between join return and the liveness sample.

| Regression boundary | Measured result / limit |
|---|---|
| Stored stderr bytes/hash | Fake Codex: rc 0; actual/receipt stderr bytes **39/39**, SHA-256 `1aa26269eb1cc57f86b235a03cda53c004edb5b1e9fc99d4da4f00843293d721` matches; 186 bytes dropped. Directory contains only `run.json`, `stderr.log`, `stdout.log`. Non-Codex `r14` validates both log hashes. |
| Non-Codex | Required unchanged-stderr/no-model-or-drop-fields test passes; reverse routing mutation fails. RUST_LOG override remains scoped to Codex. |
| Timeout 124 | Required fake-Codex timeout retains its prior model and asserts 124. POSIX timeout/descendant-kill regressions pass. |
| Incomplete-kill 125 | Independent probe performs the real successful kill, then deliberately withholds whole-tree confirmation: launcher=receipt **125**, `giet_tron_ven=false`. No process is intentionally left alive. |
| Windows | Job Object/process mocks pass; `_job_windows`, `_pid_trong_job`, `_giet_cay` and `KetGiet` are AST-identical to master. `creationflags` remains unchanged. `codex`, `codex.exe`, `codex.cmd`, `CODEX.CMD` route as Codex; Python does not. CRLF bytes are measured. Native Windows execution, `.cmd` launching, handle inheritance and Windows CI are **not_run/unverified**; Windows-only t62 explicitly skipped. |
| Popen failure | Actual absent executable: launcher **2**, receipt `hong`, null child exit, no model/drop evidence fields. |
| Reader-start failure | Actual `lenh_run` with Thread.start raising RuntimeError: pipe closes, fake child's nonzero **1** is preserved, receipt **KHONG_DO_DUOC**, RuntimeError reason, stored/dropped bytes **0/0** because no reader consumed them. No deadlock. |
| Unchanged components | `_giet_cay`, `_job_windows`, `_pid_trong_job`, `_la_codex`, `_ghi_so`, `KetGiet`: **6/6 AST-identical** to master. Production filter itself has no changes since round 5. |

No additional trace/credential disk path or false DO_DUOC path was demonstrated in the reviewed implementation. Selected response id/model/event fields are deliberately persisted by v2; existing stdout, prompt and child-owned file behavior is outside this stderr-filter guarantee. No authenticated live Codex run was performed.

Directions that would require new attack content were not executed: split normalization sequences beyond existing fixtures, escaped/duplicate type fields deep in oversized records, and nested candidate-like material in otherwise noncandidate events. These are explicitly unproved exploration directions, not asserted new defects or claimed passing tests.

## Findings, execution identity and limits

**New findings: none. Open findings: 0 P0, 0 P1, 0 P2, 0 P3.** No production/source patch is proposed by this review.

Reviewer identity is **OpenAI Codex, GPT-6-based agent**, as reported by session instructions; provider `openai_codex`, model family `openai`. Observed surface is a tool-mediated local shell in managed Linux x86_64, Python **3.13.16**; transport **machine**. Exact serving model/build/effort/session attestation, enclosing CLI-versus-service identity, and the outer `launcher.py run` execution receipt are **not independently visible or verified**. The user's reported invocation is not upgraded into a verified receipt. There is no GitHub submitter. GitHub authority comments, live pushed/unpushed state and CI are not verified. The cloud-runtime skill was read; its `environment_status` tool is unavailable, and no network/credential setup was performed.

Full repository Linux gates, bare Ruff lint, native Windows/CI and authenticated live Codex acceptance are **not_run**, consistent with the offline review-before-gates/push instruction. The review approves the examined code/test delta, not merge, land, deployment or the unmet external gates. No subagents, credentials, GitHub access, source edits, source commits, pushes or comments were used. Supplied tests create disposable fixture repositories/commits outside src; no commit is made in the reviewed repository. Source read-only behavior is a review procedure supported by the final snapshot, not an independently attested read-only mount or proof about every historical filesystem operation.

## Final integrity and evidence index

`python3 -B review-r26i-AgFeVkSE/review.py exec final-integrity review-r26i-AgFeVkSE/final_integrity.py`: rc **0**, `FINAL INTEGRITY PASS`. HEAD/tree remain exact; clone remains detached/non-shallow; local fix branch points to the reviewed SHA. Tracked, untracked and ignored status is empty. Worktree/index diffs, fix-delta whitespace check and `git fsck --connectivity-only --no-dangling` all rc **0**. Partial-clone/promisor query rc **1**, no matches. Both reviewed source files match committed bytes **2/2**. All **124/124** registered temporary mutations were reconstructed and byte-compared; companions match **2/2**; **335/335** temporary Python files compile. Final count/positive-output audit passed.

Source SHA-256:

- `launcher.py`: `51342501e0126611f81748f614ef2246a7d87069b57ace67e72200a28862a7a1`
- `launcher_test.py`: `bb329cc82b1c2e511088ebf0a59a982aaba35f4f14f066d14e576a5da1c30592`

Evidence under `review-r26i-AgFeVkSE/`: `logs/*.json` contain commands, real rc, stdout/stderr and duration; `targeted.json`, `neutral.json`, `mutants.json`, `mutation-inventory.json`, `mutation-reasons.md`, `generated-survey.json`, `round8-closure.json`, `operator-audit.json`, `predicate-ast.json`, `regression.json`, `observations.json`, `order-audit.json`, `spec-evidence.json` and `final-integrity.json` contain structured/detail evidence. Drivers and temporary source copies are retained. The two discarded setup attempts remain under `first-attempt/` and `second-attempt/`; their errors are not counted as findings or successful mutation kills.

Final measured totals: **38/38 required cases pass; 38/38 neutral controls pass; 124/124 registered mutants killed by 134/134 intended target signals; 207 generated variants = 200 killed + 7 justified equivalents; 19/19 generator-layer omission controls red; 3/3 whole-generator controls red; 9 additional regressions pass and 1 Windows-only regression skips.** Entire fix **1190 added lines**, cap **1300**; cumulative reference **1586**. All earlier reported findings are closed on this exact head.

Completed UTC: **2026-10-25T16:00:10.775072+00:00**.

VERDICT: approve
