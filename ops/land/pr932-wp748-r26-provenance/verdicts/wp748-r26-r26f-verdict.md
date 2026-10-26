# Independent review — WP748 r26, round 6

Reviewer: OpenAI Codex (identity supplied by the agent runtime). Exact backend model and `launcher.py run` execution receipt have not yet been independently verified. No GitHub access or credentials will be used; authority issue #748, issuecomment-6394503720 cannot be verified here.

Reviewed HEAD: `d5166b2b4d5f2427a7e29d3ab28005f90b52beab`; tree: `4690c6a649224b6e146031963f9802f644fd9df2`. Review class: sensitive.

## Identity gate

Command: `git -C src rev-parse --is-shallow-repository HEAD HEAD^{tree}` — rc 0:

```text
false
d5166b2b4d5f2427a7e29d3ab28005f90b52beab
4690c6a649224b6e146031963f9802f644fd9df2
```

`git -C src symbolic-ref -q HEAD` produced no output (detached); `git -C src status --short` produced no output (clean). The recorded parent chain is HEAD → 55a0afa → 0fe659e → 97bb4c5 → 143d43f → b306e15, matching the request. Identity gate passed. These commands are read-only; no source edits performed.

Review completed; the final disposition and complete evidence appear below.
2026-10-25T10:58:29Z

## Context and size (measured)

The spec was absent at local `master` (git-show rc 128); fallback at `origin/ops/wp748-r25-g25-lease` succeeded (rc 0). `sha256sum review-r26f-e3QSTmt4/spec.md` returned `f20615ae559f377150cfd6a9cfd0bce4478bf28ae3d562a674588a9c6f9d4bdb`. Lease read rc 0; it explicitly permits offline review of subsequent local fix heads until zero P0–P3. Source reviewer instructions read; the user's explicit round-six instructions control over generic review-budget/gate instructions. Cloud runtime skill read; no environment-status tool available. No network work performed.

`git -C src log --oneline 113e0d1..b306e15a96a4d9d05d2ba4191cbd071fa7820ee7 -- .claude/dev/launcher.py .claude/dev/launcher_test.py` — rc 0, empty. The two files are unchanged by those intervening master commits.

Size commands (`git -C src diff --numstat <base> <head> -- .claude/dev/launcher.py .claude/dev/launcher_test.py`) all rc 0:

| Range | launcher.py +/− | launcher_test.py +/− | Additions |
|---|---:|---:|---:|
| e739ac1 → reviewed HEAD (cumulative, merged part included) | 252/4 | 908/0 | **1,160** |
| b306e15 → reviewed HEAD (entire new fix delta) | 183/68 | 581/35 | **764** |
| b306e15 → 0fe659e (requested round-four comparison) | 182/68 | 458/35 | **640** |
| 55a0afa → reviewed HEAD (round six only) | 0/0 | 47/0 | **47** |

The fix changes exactly the two allowed files. The cumulative two-file addition count exceeds v2's 550-line ceiling by 610. This is reported to the owner as requested, **not a code finding**. An unrestricted diff from e739ac1 also includes unrelated intervening master changes; the ceiling calculation above counts the packet's two files.

Local refs `agent/wp748-r26-claude` and `origin/agent/wp748-r26-claude` point to HEAD. The local `origin/*` ref does not prove GitHub push status; local/unpushed status is requester-reported, not independently attested.

Scratch: `review-r26f-e3QSTmt4/`. Every test subprocess receives a minimal explicit environment, isolated test home/temp and an absent Codex home, without inherited authentication variables. `PYTHONDONTWRITEBYTECODE=1` prevents source-tree bytecode writes. Mutation copies include byte-identical companion modules. Exact commands, return codes, stdout/stderr and timings are retained in `commands.jsonl` and individual `logs/*.json`.

## Required current-head executions

- `python3 -B review-r26f-e3QSTmt4/review.py targeted` — rc **0**, **33/33** requested cases (15 `r925_*`, 18 `r926_*`), each invoked separately as `python3 src/.claude/dev/launcher_test.py --lap-ca <full-name> --lan 1` (absolute paths in ledger). Every case emitted `1/1 qua, 0 bo qua, 0 hong`.
- `python3 -B review-r26f-e3QSTmt4/review.py mutants` — rc **0**, **95/95** supplied r25/r26 mutants compiled and had uniquely matching replacement anchors. All **105/105** designated target executions raised **TinHieuChotCa with the named target in its traceback**. The independent wrapper uses rc **42** for that signal; unrelated exceptions use 44, wrong-origin signals 43, skips 45, and survivors 0. No unrelated exception or skip was credited.
- `python3 -B review-r26f-e3QSTmt4/review.py neutral` — rc **0**, **33/33** cases pass using an unchanged temporary launcher and the same companion layout as the mutants.
- `python3 -B review-r26f-e3QSTmt4/regression.py` — rc **1** because its strict all-selected counter includes a platform skip: **12 passed, 1 skipped, 0 failed** across 13 selected cases. `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125` explicitly skips on POSIX; it is not reported as passed. The POSIX timeout/tree-kill cases, Windows mocks, and persisted-log hash case passed.
- `python3 -B review-r26f-e3QSTmt4/extra.py` — rc **0**, **165/165** supplemental executions completed: three additional mutants survive all 33 cases; two are killed by one existing target each.
- `python3 -B review-r26f-e3QSTmt4/more.py` — rc **0**, **132/132** supplemental executions completed: one additional mutant survives all 33 cases; three are killed by existing targets (four target signals).

Thus **4/9 additional independent guard mutations survive all 33 required cases (132/132 passes)**; the other five have **6 target-origin signals** across 165 runs. These are nine supplemental audit variants (eight distinct omitted safeguards), not registered DOT_BIEN entries. All mutate only temporary launcher copies and reuse existing fixtures. No new exploit payload was authored.

## Finding — remaining independent guard coverage

**R26-TEST-15 — P3 — `.claude/dev/launcher_test.py:10779` (`DOT_BIEN`), guarding `.claude/dev/launcher.py:1607`, `:1608`, `:1624`, `:1742`.** Class: **unguarded-filter-invariants**, continuing the earlier test-coverage class. Round-six fixes close the specifically listed R26-TEST-14 omissions, but the claim that every filter guard has its own effective mutant remains false. The remaining omissions are in the regex grammar and the separate streaming normalization path; an inventory of only explicit Python `if` expressions misses them.

| Independent omitted guard | Supplemental mutant | Current measured result |
|---|---|---|
| Required TRACE severity, line 1607 | `frame_trace_level`: replace only `TRACE` with a non-whitespace-level matcher | **33/33 survive**. No supplied mutation removes this provenance check; target/receive-position mutations leave it intact. |
| Whole-frame end anchor, line 1608 | `frame_end_anchor`: remove only the trailing whitespace/end assertion | **33/33 survive**. The physical-LF and single-chunk mutants do not remove rejection of extra content after a parsed frame on a complete line. |
| Captured top-level JSON-object shape, line 1608 | `frame_json_object`: broaden only the brace-delimited capture to arbitrary content | **33/33 survive**. This grammar guard is also the premise used to justify removal of `isinstance(ev, dict)`. |
| ANSI normalization for streaming candidate detection, line 1742 | `streaming_ansi`: remove only ANSI cleanup from `duoi + doan`, retaining whitespace compaction | **33/33 survive**. `r25_bo_go_ansi` changes line 1698 (complete-line/prefix parsing), not this path. |
| Timestamp shape at the receive-header start, line 1607 | `frame_timestamp`: broaden only the timestamp token; supplemental variant `frame_start_anchor`: permit a prefix before the timestamp | Both variants independently trigger the existing cut sweep at cap **444**: `byte_bo=632`, no loss, wrong DO_DUOC. Each passes 32 other cases. These are two variants of one header-shape safeguard, not two additional Python dispatch predicates. |
| Literal first `type` key for prefix confirmation, line 1624 | `prefix_literal_type`: broaden only that key matcher | Existing unknown-header case fails at `khoa_escape`: **687 dropped bytes**, no unknown count, wrong DO_DUOC. 32 other cases pass. |
| No undecoded escapes in prefix type, line 1624 | `prefix_no_escape`: allow backslashes in the captured type | Same target fails at `gia_tri_escape`: **688 dropped bytes**, no unknown count, wrong DO_DUOC. 32 other cases pass. |
| Closed prefix type string, line 1624 | `prefix_closed_type`: remove only the closing quote requirement | Unknown-header target fails at `gia_tri_escape`; prefix-cap target also fails at cap **150** (`byte_bo=484`, expected unknown count 1 missing). 31 other cases pass. |

Commands and exact before/after strings are in `extra-inventory.json` / `more-inventory.json`; every supplemental anchor is unique and every copy compiles. `extras.json` / `more.json` contain all 297 executions, including real target messages/tracebacks. **This is a testing/acceptance defect, not a demonstrated production credential leak or production false-positive measurement on HEAD.** No severity is inferred from an unexecuted attack direction.

Fix at `DOT_BIEN` and the corresponding r925/r926 cases: register focused mutations for these distinct guards; bind the five already-detected mutation variants to the existing targets named above. For the four survivors, the executor should add independent benign fixtures that exercise non-TRACE provenance, content after a closed JSON frame, non-object JSON at the receive position, and ANSI within a candidate token across the streaming path. Include a valid prior model when testing completeness so lack of all positive evidence cannot mask the loss defect. The reviewer supplies directions only for those new payloads. Keep neutral controls, and require the target's own TinHieuChotCa. Risks: changing several grammar rules in one mutant hides which guard is tested; a generic filter error or incidental fixture exception is insufficient evidence of the intended classification. No production rewrite is required by this finding.

## Current predicate inventory

The production lines below were re-read on this HEAD and the explicit `if`/conditional-expression/while/exception nodes were enumerated with Python AST. Each constituent of a compound evidence predicate is listed separately. Supplied mutations below were all executed in the 105-target run; exact replacements and target names are in `mutation-inventory.json`. A guard's reject action can be disabled instead of negating its condition when that removes exactly the same observable safeguard; shared grammar guards are distinguished from their Python dispatch predicates. The regex/normalization omissions above are additional to this table.

| Production line / safeguard | Current independent supplied coverage |
|---|---|
| 1642 optional counter initialization / retain caller's dict | `r26_rv5_optional_counter_init`; `r26_rv5_retain_caller_counter` |
| 1645–1649 filter error handling: record / drain / bounded read / count drain | `r25_bo_loc_hong_khong_ghi_loi`; `r25_bo_loc_hong_khong_xa_ong`; `r25_xa_ong_khong_tran`; `r26_xa_khong_dem` |
| 1656 missing frame match | `r26_rv5_frame_match_guard` |
| 1659 strict UTF-8 / 1660 parse-error handling | `r26_utf8_thay_the`; `r26_rv5_exception_valueerror` |
| 1607 target identity / immediate receive-message position | `r26_rv5_target_only`; `r26_rv5_receive_position_only` (legacy `r25_khung_moi_target` removes both) |
| 1663 eligible event | `r25_moi_su_kien` |
| 1666 response object | `r26_response_khong_kiem_object` |
| 1667 id string / stripped id nonempty | `r26_id_khong_kiem_chuoi`; `r26_id_khong_strip` |
| 1667 model string / stripped model nonempty | `r26_model_khong_kiem_chuoi`; `r26_model_khong_strip` (legacy `r25_nhan_id_model_rong` weakens multiple terms) |
| 1684 retry short writes / 1686 require progress | `r26_ghi_khong_lap`; `r26_ghi_bo_chot_0_byte`; independent first failures are `ngan_roi_du` and `tra_0` |
| 1689 closed-sink discarded suffix / 1691 other failure suffix | `r26_tep_dong_khong_dem`; `r26_ghi_loi_khong_dem`; `r26_ghi_dem_ca_doan` |
| 1698 ANSI removal before complete parsing and prefix confirmation | `r25_bo_go_ansi`; separate streaming removal at 1742 remains missing, above |
| 1699 single chunk / complete physical line | `r26_mot_doan_bo_dieu_kien_so_doan`; `r25_parse_khong_can_ca_dong` |
| 1701 parsed model non-None | `r26_rv5_parsed_model_guard` |
| 1702 whole dedup / response-id equality / model equality | `r26_rv5_dedup_whole`; `r26_rv5_dedup_response_id`; `r25_gop_theo_id` |
| 1704 parsed bad candidate / raw candidate | `r26_phan_loai_theo_token`; `r26_doc_tron_bo_token`; action removal `r25_bo_dem_mat` |
| 1706 no parsed event / JSON header / whole fallback | `r26_doc_tron_khong_ro_ca_su_kien_khac`; `r26_doc_tron_khong_ro_khong_doi_json`; `r26_doc_tron_khong_parse_bo_qua` |
| 1709 multi-chunk/EOF candidate loss | `r26_bo_dem_mat_nhieu_doan`; its targets explicitly require `mat`, so a downgrade via `khong_ro` alone is insufficient |
| 1713 prefix regex match | `r26_rv5_prefix_match_guard`; grammar inside that regex has the omissions above |
| 1715–1717 strict decoded prefix type | `r26_loai_khong_utf8_thay_the` |
| 1720 decoded type non-None / type not candidate / other-event return | `r26_rv5_prefix_decoded`; `r26_tien_to_ung_vien_tha`; `r26_bo_xac_nhan_su_kien_khac` |
| 1722 JSON header / unknown counter | `r26_khong_ro_moi_dong_dai`; `r26_khong_ro_khong_dem`; shared opening-brace grammar has `r26_khong_ro_khong_doi_json` |
| 1729 bounded readline | `r25_doc_khong_tran`; EOF sentinel is standard bytes-stream EOF, not a separate policy predicate |
| 1730 reset on new physical line | `r26_khong_dat_lai_moi_dong` |
| 1732 actual LF | `r26_rv5_lf_detection` |
| 1734 first chunk / exact raw membership / exact CRLF forms | `r25_cho_phep_ca_dong_cut`; `r25_ghi_moi_dong_tron`, `r25_cho_phep_theo_tien_to`; `r26_cho_phep_cat_moi_CRLF` |
| 1738 capture first chunk versus continuation | `r26_rv5_first_chunk_capture` |
| 1741 append / bounded prefix / nonnegative remainder | `r26_dau_dong_khong_noi`; `r26_tien_to_khong_tran`; `r26_tien_to_bo_max` |
| 1742 whitespace compaction / 1744 cross-chunk tail | `r26_khong_bo_khoang_trang`; `r26_bo_duoi_vat` |
| 1743 sticky candidate / new candidate search | `r26_token_khong_dinh`; `r26_rv5_candidate_search` |
| 1745 classify only at LF / 1747 classify final incomplete line | `r26_rv5_classify_only_at_lf`; `r26_bo_dong_cut_EOF` |
| 1754 reader errors / 1756 unfinished reader | `r25_DO_DUOC_khi_loc_hong`; `r25_DO_DUOC_khi_ong_con_mo` |
| 1758 loss / 1760 unknown / 1763 positive frame required | `r25_DO_DUOC_khi_mat`; `r26_DO_DUOC_khi_khong_ro`; `r25_DO_DUOC_khong_khung` |
| 1787 start failure catch / record error / close pipe | `r26_luong_hong_lot_ra`; `r26_luong_hong_khong_ghi_loi`; `r26_luong_hong_khong_dong_ong` |
| 1795 only join started thread | `r26_cho_luong_chua_chay` |
| 1796 bounded join / 1797 latch / 1798 close ordering and close action | `r25_doc_ong_khong_han`; `r25_bo_chot_luong`; `r26_dong_tep_truoc_chot`, `r26_ket_thuc_khong_dong_tep` |
| 1803 unlatched defaults incomplete / no late liveness resample | `r26_mac_dinh_chua_chot_la_xong`; `r26_lay_mau_lai_luong_muon` |
| 1805 error / loss / unknown handoff | `r25_so_khong_chuyen_loi`; `r25_so_khong_chuyen_mat`; `r26_so_khong_chuyen_khong_ro` |
| 1808 negative-status reason | `r26_rv5_reason_guard` |
| 1934 Codex-only routing, both directions | `r26_rv5_codex_mode_disabled`; `r25_loc_ca_luot_khong_phai_codex` |
| 1937–1938 binary FileIO contract, unbuffered write guarantee | `r26_tep_stderr_co_dem` removes buffering=0; target observes actual FileIO; Codex/non-Codex selection follows the shared routing flag |
| 1941 environment application / exact RUST_LOG replacement / 1946 override recording | `r26_rv5_codex_env_guard`; `r25_khong_bat_trace`, `r25_noi_rust_log_thua_ke`; `r26_rv5_rust_override_record` |
| 1956 pipe route / 1958 start reader | `r26_rv5_codex_pipe_guard`; `r26_rv5_codex_reader_guard` |
| 2025 finalize filter / ordering | `r26_rv5_finish_object_guard`; `r26_san_xuat_dong_tep_truoc`, `r26_rv5_old_late_production_latch` |
| 2030 serialize filter evidence | `r26_khong_ghi_so` |

Two removed checks are actually unreachable/redundant on production constants: (1) every `_STDERR_CHO_PHEP_DONG` member ends in LF, so membership implies `het_dong`; (2) the intact `_RE_KHUNG` captures a complete brace-delimited top-level JSON object, and successful standard `json.loads` without hooks returns a dict. Non-object success cannot occur with this production regex. The second proof remains valid on HEAD, but its premise deserves independent regression coverage (the `frame_json_object` survivor above). The literal leading `^` in `_DAU_NHAN` is also redundant under current call sites: all three derived regexes are used only with `.match(sach)`, which already requires position zero. Removing only `^` cannot make a nonzero-offset match reachable. The supplemental `frame_start_anchor` variant deliberately adds a leading wildcard, so it tests the header-shape safeguard and is not evidence that deleting `^` alone changes behavior. No survivor of an actual safeguard removal is excused as equivalent. The `max(0, limit-len(prefix))` rewrite avoids negative slicing while preserving an already-large first chunk; both independent bound mutations fail the existing prefix-cap case.

## Earlier-finding status on this exact HEAD

| Earlier finding | Status and fresh measured evidence |
|---|---|
| R25-SEC-01 P1 | **Closed for the reported stderr write path.** Exact-list and synthetic-secret run-directory cases pass. Unrestricted, prefix, continuation and RUST_LOG mutations die; the direct exact-list target observes forbidden output under the unrestricted-write mutant. |
| R25-MEAS-02 P2 | **Reported production defect stays closed.** Source/position/event, strict UTF-8, metadata types/nonblank values and multi-model tests pass. New residual grammar mutation coverage is R26-TEST-15 P3, not a demonstrated head provenance bypass. |
| R25-TEST-03 P2 | **All previously identified surviving removals stay closed.** Generic write-count removal fails at `ngan_roi_nem`; default-unlatched removal produces wrong DO_DUOC; old late-production-latch removal is killed and independently diagnosed below. Strict UTF-8 and error/loss handoff removals also die. Broader every-guard class continues at P3. |
| R25-ROBUST-04 P2 | **Closed for unbounded normal/error-drain reads.** Both named bounded-read cases pass and both unbounded-read mutants die. Production cap is 4 MiB. |
| R25-EVID-05 P2 | **Closed for all reported paths and fixtures.** All-cut/whitespace sweeps require actual loss counts; malformed complete receive lines require unknown counts. Complete-fallback removal fails at the existing 329-byte invalid-UTF-8/escaped-key fixture; no model loss is silently certified on head in those cases. |
| R25-RACE-06 P2 | **Closed.** Latch-before-copy and late-resample cases pass; corresponding removals die. Status and serialized evidence use the same copies after the latch. |
| R25-CONTRACT-07 P2 | **Closed under superseding v2.** Loss of non-allow-listed Codex diagnostics is the authorized policy. Non-Codex stderr remains unchanged and its case passes. |
| R26-ALLOW-08 P3 | **Closed.** LF stores 39/39, CRLF 40/40, CR-CR-LF 0/41; the exact corresponding mutation fails at `CR_CRLF`. Continuation equal to an allowed line stores 0/78 bytes. |
| R26-COUNT-09 P3 | **Closed under native unbuffered contract.** Real FileIO/file-size-limit probe: 43 input = 10 stored + 33 dropped, OSError recorded. Drain, closed-sink, short-write, suffix-accounting and unbuffered mutants die. |
| R26-EOF-10 P3 | **Closed for finish-during-close.** Real 10-second join integration passes; object and production order mutations die. Additional diagnostic confirms wrong final DO_DUOC in both late-close-order variants. |
| R26-CLASSIFY-11 P3 | **Closed for reported other-event fixtures.** Every-cap controls pass; Binary/Ping controls remain complete with no loss/unknown. No new payload-dependent production claim made. |
| R26-TEST-12 P3 | **Closed.** Zero-progress mutant dies at `tra_0` (incorrectly 39 bytes written, no OSError, only 4 dropped); short-write-loop mutant separately dies at `ngan_roi_du`. |
| R26-TEST-13 P3 | **Closed for both reported predicates.** Single-chunk and complete-other-event-condition removals fail their intended targets. |
| R26-TEST-14 P3 | **Closed for its listed omissions.** All 23 newly registered `r26_rv5_*` entries match uniquely, compile, and die at their designated targets; the two previously duplicated omissions remain covered. The continuing coverage class is now R26-TEST-15. |
| Unreachable `bo_loc is None` failed-start note | **No false-positive evidence path.** Actual absent-executable attempt returns rc 2, receipt `hong`, null child exit, no model/drop keys. Popen failure exits before final filter evidence serialization. |

## Security and regression boundaries

`python3 -B review-r26f-e3QSTmt4/review.py exec observations-fixed review-r26f-e3QSTmt4/observations.py` — rc **0**, `OBSERVATIONS PASS`. First scratch observation attempt returned rc 1 (reviewer omitted the required reason argument to `--bo-qua-probe`, then tried to read a nonexistent receipt). That harness mistake was corrected in scratch; it is not a source failure or mutation kill. Both command records are retained.

| Boundary | Evidence and limits |
|---|---|
| Stderr disk writes | The only filter write receives a raw exact allow-list member, only at the beginning of a physical line. Comparison precedes normalization. Partial lines, suffix/prefix variants, repeated CR, oversized continuations, invalid bytes and sample-secret fixtures pass. A short write can persist only a prefix of an allowed constant. No raw fallback or trace spool was found. |
| Four physical-line classification paths | Complete single-chunk records use strict parsing; bad candidate metadata or raw candidate signal counts loss; otherwise an unparseable JSON receive header counts unknown. Multi-chunk/EOF-cut records classify once at physical LF/EOF: sticky candidate → loss; confirmed other prefix → no loss/unknown; unconfirmed JSON header → unknown. All existing path/cut tests pass. |
| Cross-boundary detection | Whitespace compaction plus 64-byte carry preserves candidate tokens across the supplied cuts, and the sticky flag preserves earlier matches. Streaming ANSI normalization lacks an effective independent test, as reported above. Existing fixtures do not prove every encoding/framing combination. |
| Further payload-dependent directions (not executed) | Executor-authored tests should examine ANSI sequences split at normalization boundaries, escaped or duplicate event-type fields in oversized records, and parsed noncandidate events containing nested candidate-like material. These are directions only; this review authored no new exploit input and claims no new head production bypass from them. |
| Positive evidence and counters | DO_DUOC requires a retained model, no reader error, latched completion, no loss and no unknown count. All explicit conditions and evidence handoffs have effective supplied mutants. Counters count successfully read/discarded chunks, not unread bytes that never reached the reader. |
| Error drain / closed output | Drain remains bounded and counted. Error text is reduced to exception class names. Closed-output writes count the unwritten allowed suffix; no alternative sink receives raw data. An unfinished reader is already latched incomplete, preventing late work from certifying completion. |
| Write accounting | Native FileIO probe with RLIMIT_FSIZE=10 measured input 43, persisted 10, dropped 33, `OSError`. This substantiates the documented unbuffered contract. No claim is made for arbitrary buffered/custom streams outside that contract. |
| 10-second join and late reader | Head's inherited-pipe case and finish-during-close case pass. Unbounded-join mutant takes **40.474 s** and fails the intended elapsed-time assertion. `ket_thuc(10)` joins, samples liveness, then closes. An already-latched live reader cannot become complete later. No independent EOF timestamp measures a sub-scheduling-window deadline between join return and liveness sampling. |
| Run directory and stderr hashes | Fake-child run retains exactly `run.json`, `stderr.log`, `stdout.log`; stored stderr=receipt `stderr_byte`=39, SHA-256=`1aa26269eb1cc57f86b235a03cda53c004edb5b1e9fc99d4da4f00843293d721`, equal to receipt; 186 trace bytes counted dropped. `r14_run_json_bam_lai_dung_hai_log` passes. |
| Other sinks | Selected response id/model/event metadata are intentionally persisted by v2. Existing stdout/prompt-snapshot sinks and child-owned files are outside this stderr filter. No authenticated live Codex execution or universal all-process no-disk guarantee is claimed. |
| Timeout / kill 124 and 125 | Required fake-Codex timeout case passes and asserts 124 with the prior model retained. Selected POSIX tree-kill regressions pass. Independent actual-kill probe deliberately withholds complete confirmation after the real kill succeeds: launcher=receipt **125**, `giet_tron_ven=false`; no child deliberately left alive. Windows-only t62 is skipped, explicitly. |
| Windows | Job Object/process mocks pass; creationflags and Job Object production paths are unchanged. `codex`, `codex.exe`, `codex.cmd`, `CODEX.CMD` identify true, Python false. Exact CRLF storage measured. Native Windows launch/Job Object/handle inheritance/`.cmd` execution and the Windows CI lane are **not_run/unverified**. |
| Non-Codex | Required unchanged-stderr/no-extra-model-or-drop-fields case and persisted-log hash case pass. Codex RUST_LOG override is scoped to Codex. |
| Popen failure | Public bypass-reason fixture with absent executable returns **2**, receipt `hong`, null `ma_thoat`, no model/drop keys. |
| Reader-start failure | Actual lenh_run with Thread.start forced to raise RuntimeError closes the pipe and completes; fake Python child's broken-stderr rc **120** is preserved. Receipt is **KHONG_DO_DUOC**, reason RuntimeError, stored/dropped bytes **0/0** because no reader consumed them. No deadlock or positive measurement. |

`python3 -B review-r26f-e3QSTmt4/review.py exec order-audit review-r26f-e3QSTmt4/order_audit.py` — rc **0**, **3/3** diagnostic expectations. Ordinary `r26_san_xuat_dong_tep_truoc` and `r26_rv5_old_late_production_latch` executions first fail their own close-observation assertion (a second close overwrites the fixture's observation). Diagnostic-only interception records all assertions without stopping: both also fail the final receipt assertion with **DO_DUOC / None**, while head passes all three and has **KHONG_DO_DUOC / ong stderr con mo sau 10s**. The ordinary target signals remain the kill evidence; this extra diagnostic establishes the underlying wrong result rather than relying solely on the incidental first assertion. No source test edited.

The omitted-close mutant dies at absence of the close observation itself; the buffered-output mutant dies at the actual FileIO check. Type-check-removal mutants can create exceptions inside the filter, but those are caught and explicitly rejected by their target's classification assertion. The unrestricted-write mutation's integration target first fails status; its separate exact-list target directly detects forbidden sample-secret output. These are kept distinct in the raw records.


Additional boundary observation: `python3 -B review-r26f-e3QSTmt4/review.py exec boundaries review-r26f-e3QSTmt4/boundaries.py` — rc **0**, `BOUNDARIES PASS`. Existing benign frame with CRLF: **187 dropped bytes, one retained model, no loss**; CR-only EOF: **186 dropped, no model, mat=1**. Existing complete invalid-UTF-8/escaped-key and truncated-JSON/escaped-key fixtures: **329/329** and **314/314** dropped bytes respectively, each `khong_ro=1`, one prior model retained, KHONG_DO_DUOC. Existing Binary/Ping controls: **752** dropped, no loss/unknown, DO_DUOC at caps 256 and 4096. This adds no exploit payload.

## Final integrity, execution identity and disposition

`python3 -B review-r26f-e3QSTmt4/final_integrity.py` — rc **0**, `FINAL INTEGRITY PASS`. HEAD/tree remain exact, detached and full; status including tracked, untracked and ignored files is empty. Worktree diff, staged diff, fix-delta whitespace check and `git fsck --connectivity-only --no-dangling` each rc **0**. Partial-clone/promisor config query rc **1**, no matches. Working-file bytes match committed HEAD **2/2**; all **107/107** temporary launcher/companion Python files compile; companions match source **2/2**. `_giet_cay`, `_job_windows`, `_pid_trong_job`, `_la_codex`, `_ghi_so`, and `KetGiet` remain AST-identical to b306e15 **6/6**. All 95 registered temporary replacements were independently reconstructed and checked against their files and all 105 target records.

Source SHA-256:

- `.claude/dev/launcher.py`: `51342501e0126611f81748f614ef2246a7d87069b57ace67e72200a28862a7a1`
- `.claude/dev/launcher_test.py`: `ec0fef9e28e02501e5c347cc3b1f7514b2b22862cf0e39e499e3b6b4399cd5c5`

Runtime observed: Linux x86_64, Python **3.13.16**. Runtime instructions identify the reviewer as **OpenAI Codex, a GPT-6-based agent**; provider **openai_codex**, model family **openai**. Actual observed execution surface is a tool-mediated local shell in this managed Linux workspace; transport **machine**. Exact serving-model/build/effort/session attestation, enclosing CLI-versus-service identity and the outer `launcher.py run` execution receipt are **not independently visible or verified**. User-reported launcher invocation is not silently upgraded into a verified receipt. GitHub authority, live push/merge status and CI are not verified. No GitHub submitter, credential use, source edit, source commit, push or GitHub comment. No subagents used. Supplied tests create their own disposable fixture Git repositories; no commit is made in the reviewed source. Source read-only behavior is a review procedure here, not a separately attested mount constraint.

Full repository-wide Linux gate, bare Ruff lint, native Windows execution/CI and authenticated live Codex acceptance are **not_run**. The measured review scope is the complete requested r925/r926 case and r25/r26 mutation sets plus the documented local regressions and probes. Prior-round reports are not substituted for current execution. The lease/user explicitly calls for offline review before gates/push; this verdict does not grant merge, land or deployment authority.

Evidence index: `review-r26f-e3QSTmt4/commands.jsonl` and `logs/` hold exact child commands, real rc, stdout/stderr and durations. `targeted.json`, `mutations.json`, `neutral.json`, `regression.json`, `extras.json`, `more.json`, `observations.json`, `boundaries.json`, `order-audit.json`, and `final-integrity.json` hold structured evidence. `mutation-inventory.json`, `extra-inventory.json`, `more-inventory.json` preserve exact source replacements. `mutation-reasons.md` records all **105** actual target assertion messages. Drivers and temporary copies are retained for reproduction. The initial scratch observation-driver failure is retained and not credited as a source failure.

Final result: **33/33 requested cases pass; 95/95 supplied mutants killed through 105/105 intended target signals; 33/33 neutral controls pass; 12 additional regressions pass, 1 Windows-only case skipped; 297 supplemental mutation executions complete, exposing four survivors across all 33 cases.** All specifically reported earlier production fixes and round-five registered omissions remain closed on their measured fixtures. One continuing coverage finding remains: **R26-TEST-15 P3**. Open counts: **0 P0, 0 P1, 0 P2, 1 P3**. The zero-P0–P3 criterion is not met. Size is separately **1,160 cumulative additions / 764 entire-fix additions / 47 round-six additions**, not a code finding.

Completed UTC: **2026-10-25T11:13:15.669791+00:00**.

VERDICT: changes_requested
