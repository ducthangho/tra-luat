# WP748 r26 round 5 independent read-only review

Disposition: **changes requested — 0 P0, 0 P1, 0 P2, 1 P3 open (R26-TEST-14, continuing mutation-coverage class).** The two predicates reported in round 4 are fixed.

Started 2026-10-25 10:34:58 UTC. Review class: **sensitive**.

Reviewer: OpenAI Codex, as identified by the session runtime instructions (GPT-6 based agent). This interface does not expose an independently verifiable backend model ID or launcher execution receipt; those cannot be attested. No credentials or GitHub access will be used. Authority issue #748 / issuecomment-6394503720 cannot be read under this review's constraints.

Identity verified before review: `src` is non-shallow (`git rev-parse --is-shallow-repository` → `false`), detached HEAD (`git symbolic-ref -q HEAD` → no output), SHA `55a0afa796c1012c5551cd620bbdb5ab505dec3f`, tree `38e733989566d80b668cf0c68b6fff372647f551`. Initial `git status --porcelain=v1` is empty. `git show -s --format='%H %P'` confirms the exact chain 55a0afa → 0fe659e → 97bb4c5 → 143d43f → b306e15. The initial command batch returned rc 0; individual detached-ref rc will also be recorded. Local/unpushed status and the named owner branch cannot establish remote absence without contacting GitHub, which is prohibited.

Scope: combined implementation through HEAD, round-5 delta against 0fe659e, earlier findings, all r925/r926 cases and r25/r26 mutants, exact stderr allow-list and evidence integrity, compatibility, and size accounting. Only this verdict and temporary scratch artifacts may be written; `src/` will remain unchanged.

## Verified context and size

`python3 -B review-r26e-g564iDKA/review.py integrity` rc 0. Per-command records: `review-r26e-g564iDKA/logs/` and `commands.jsonl`. Individual detached-ref rc=1, empty output, as expected. Local `master` spec lookup rc=128 (`fatal: invalid object name 'master'.`); prescribed fallback rc=0, SHA-256 **f20615ae559f377150cfd6a9cfd0bce4478bf28ae3d562a674588a9c6f9d4bdb**, exact match. Lease read rc=0; its local-head rereview provision covers the supplied head. Intervening master log for the two files is empty, rc=0.

`git -C src diff --numstat <base> HEAD -- .claude/dev/launcher.py .claude/dev/launcher_test.py`, each rc=0:

| Base | launcher +/− | tests +/− | Total additions/deletions |
|---|---:|---:|---:|
| e739ac1b74024a20949425c447fb6cf025317c0e, cumulative including merged part | 252/4 | 861/0 | **1,113/4** |
| b306e15a96a4d9d05d2ba4191cbd071fa7820ee7, fix delta only | 183/68 | 534/35 | **717/103** |
| 0fe659e30e151f4ce3dce13789fa6622ca6c6b47, round 5 only | 6/5 | 84/8 | **90/13** |

Exactly two changed files. The cumulative additions exceed the v2 ceiling of 550 by **563**. This is an informational owner item, not a code finding, per the explicit review request. Owner escalation is requester-reported.

Tests use an explicit minimal environment, bytecode disabled, isolated scratch HOME/TMPDIR, and the nonexistent `/nonexistent-wp748-r26e-fixture-codex-home` selector. No inherited authentication variables or real credential files are used. Supplied test helpers create seed Git repositories/commits only in disposable fixtures; no commit is made in `src`. Mutants each use a uniquely named temporary launcher with unchanged companion files. Independent wrapper rc=1 requires `TinHieuChotCa` with the named target in the traceback; unrelated exceptions, skips, or wrong-target signals receive no kill credit.

## Required executions completed

- `python3 -B review-r26e-g564iDKA/review.py targeted`: rc **0**, **33/33** requested cases (**15 r925 + 18 r926**), each invoked as `python3 src/.claude/dev/launcher_test.py --lap-ca <name> --lan 1` with absolute paths in the command ledger. Every case reports `1/1 qua, 0 bo qua, 0 hong`.
- `python3 -B review-r26e-g564iDKA/review.py mutants`: rc **0**, **72/72** supplied r25/r26 mutants uniquely matched and compiled, **82/82** designated target executions killed by target-origin `TinHieuChotCa`, each rc **1**. No ordinary exception or skip credited.
- `python3 -B review-r26e-g564iDKA/review.py regression`: rc **0**, **13/13** selected timeout/tree-kill, Windows-mock, and persisted-log hash cases passed; no skips.

Round-4 **R26-TEST-13 P3 is closed for both reported predicates**: `r26_mot_doan_bo_dieu_kien_so_doan` removes only the single-read qualifier and is killed by the oversized-frame target (`byte_bo=470`, an oversized model wrongly accepted); `r26_doc_tron_khong_ro_ca_su_kien_khac` removes only `loai is None` and is killed at cap 196 (`byte_bo=382`, `khong_ro=1`, known-other event wrongly downgrades the status). These are the expected target assertions.

The subsequent predicate audit below disproves the broader claim that EVERY predicate has its own mutant. Additional focused removals use only existing fixture bytes. An initial supplemental driver failed after its first target execution because the reviewer's `dict()` call repeated the keyword `name`; rc=1, retained in `extra-initial-driver-error.txt`. This scratch-only bookkeeping error was corrected; it is not a source finding or a mutation kill.

## New finding (continuing mutation-coverage class)

**R26-TEST-14 — P3 — `.claude/dev/launcher_test.py:10779` (`DOT_BIEN`; production predicates detailed below).** Class: **unguarded-filter-invariants**, continuing R25-TEST-03 → R26-TEST-12 → R26-TEST-13. The two specifically reported round-4 omissions are fixed, but the new claim of individual coverage for every remaining predicate is false. Existing tests already distinguish the additional removals; the missing artifacts are focused registered mutations, not newly demonstrated production defects.

Measured particularly consequential omissions:

- `.claude/dev/launcher.py:1720`: removing only `loai is not None` leaves `None not in _SU_KIEN_KHUNG` true after the existing invalid-UTF-8 type fixture. The mutant incorrectly returns early and reports **DO_DUOC**, `byte_bo=683`, no `khong_ro`. Its named target raises TinHieuChotCa at `loai_khong_utf8`. `r26_loai_khong_utf8_thay_the` changes the decoder, while `r26_tien_to_ung_vien_tha` removes the OTHER conjunct; neither removes this predicate.
- `:1702`: removing only the response-ID equality deduplicates different responses sharing a model. Existing fake-child target retains only resp_1 and resp_2, losing resp_3, and raises TinHieuChotCa. `r25_gop_theo_id` removes only the model equality, the opposite conjunct. Disabling deduplication altogether is also independently detected by the same target (four records instead of three) but has no registered mutation.
- `:1738`: forcing the first-chunk assignment on subsequent chunks overwrites the physical-line prefix. Existing escaped-key fixture then yields **DO_DUOC**, `byte_bo=687`, no unknown count. This differs from `r26_dau_dong_khong_noi`, which preserves the first chunk but stops appending to it.
- `:1745`: classifying before physical LF falsely marks the existing confirmed-other event unknown at cap 187 (`byte_bo=382`, `khong_ro=1`). The reset guard at :1730 and EOF guard at :1747 have mutants; this separate LF guard does not.
- `:1642`: replacing the caller's counter dictionary discards the loss count before `ghi_so`, producing **DO_DUOC**, zero recorded drops, and one retained model in the existing production loss test. The opposite optional-counter initialization branch also has a reachable four-argument caller in the supplied tests; it is not dead code.

Additional missing individual checks, including nullable regex/model guards, candidate-token discovery, reason/override recording and parse-error classification, are enumerated in the audit matrix below. Focused provenance removals also distinguish target identity from receive-message position; the current `r25_khung_moi_target` relaxes BOTH together.

Commands: `python3 -B review-r26e-g564iDKA/extra.py` rc **0**, **14/14** target signals (11 additional checks plus the three prior surviving mutants); `python3 -B review-r26e-g564iDKA/more.py` rc **0**, **5/5** target signals. Every replacement uniquely matches and compiles; exact pairs, target names, rc, assertion text and traceback are retained in `extras.json`, `more.json`, and their command logs. All use existing test inputs; no new exploit payload was authored.

Fix direction: complete a finite predicate inventory in `DOT_BIEN`, add focused r26 entries pointing to the already effective targets, and keep current mutations that exercise distinct behaviors. The executable scratch pairs are review evidence, not a production patch. Prove any claimed equivalence from reachable states; an existing test that passes on head does not replace a mutation. Re-run the target with the neutral copy and demand its own TinHieuChotCa, not a generic harness exception. Main risks are compound mutations concealing which guard failed and incidental fixture assertions earning false confidence. No production behavior change is required to close these coverage omissions.

## Predicate-by-predicate audit

All line numbers below refer to the reviewed `launcher.py`. “Missing → X” means no independent supplied mutation for that check, and supplemental mutant X uniquely removes/changes it and is killed by its existing target. Exact supplemental pairs and target traceback locations are in `extras.json`, `more.json`, and `integration-mutants.json`. They are part of R26-TEST-14, not additional production findings. Rows marked covered identify the supplied entry; all such designated targets were executed above.

| Line / predicate or guard | Audit result |
|---|---|
| 1642 `dem is None`, initialize optional counters | Missing → `optional_counter_init`; existing four-argument caller gets AttributeError instead of its expected RuntimeError classification. This path is reachable in the supplied helper test. |
| 1642 preserve supplied counter object | Missing → `retain_caller_counter`; production loss case incorrectly DO_DUOC, drop counts zero. |
| 1645 filter exception recording; 1648 bounded error drain | Covered: `r25_bo_loc_hong_khong_ghi_loi`, `r25_bo_loc_hong_khong_xa_ong`, `r25_xa_ong_khong_tran`, `r26_xa_khong_dem`. |
| 1656 reject absent frame regex match (`not k`) | Missing → `frame_match_guard`; existing wrong-source frame aborts parsing and loses the valid following models. |
| 1659 strict UTF-8 | Covered: `r26_utf8_thay_the`. |
| 1660 parse-error classification (`except ValueError`) | Missing → `exception_valueerror`; existing invalid-UTF-8 candidate becomes a filter error instead of one counted loss. Target raises TinHieuChotCa, not an escaped decoder exception. |
| 1607/1655 target identity and immediate receive-message position | Compound supplied mutation `r25_khung_moi_target` removes both. Missing independent removals → `target_only` and `receive_position_only`; existing x1/x2 controls separately enter the accepted list. |
| 1663 eligible event membership | Covered: `r25_moi_su_kien`. |
| 1666 response is dict | Covered: `r26_response_khong_kiem_object`, target fails at `response_chuoi`. |
| 1667 id is str | Covered: `r26_id_khong_kiem_chuoi`. First failure is id=None from the `response_chuoi` row; the resulting AttributeError is caught by the filter and the target correctly rejects the erroneous error/loss classification. It is not an unrelated harness exception. |
| 1667 stripped id nonempty | Covered: `r26_id_khong_strip`, target fails at `id_trang`. |
| 1667 model is str | Covered: `r26_model_khong_kiem_chuoi`, target fails at `model_so`. |
| 1667 stripped model nonempty | Covered: `r26_model_khong_strip`, target fails at `model_trang`. Legacy `r25_nhan_id_model_rong` weakens two checks together; these individual entries supply separation. |
| 1684 continue until all bytes written | Covered behavior: `r26_ghi_khong_lap`, failure at `ngan_roi_du`. This replacement changes progress handling and also removes the zero check; the separate next row is required. |
| 1686 zero/None progress | Covered independently: `r26_ghi_bo_chot_0_byte`, failure specifically at `tra_0`. |
| 1689 closed sink; 1691 generic write failure accounting | Covered: `r26_tep_dong_khong_dem`, `r26_ghi_loi_khong_dem`, `r26_ghi_dem_ca_doan`; only unwritten suffix counted. |
| 1699 `so_doan == 1` | Covered, round-4 finding fixed: `r26_mot_doan_bo_dieu_kien_so_doan`. |
| 1699 `tron` | Covered: `r25_parse_khong_can_ca_dong`. |
| 1701 parsed model is non-None | Missing → `parsed_model_guard`; existing wrong-source input puts None in accepted list, caught by the target. |
| 1702 suppress duplicate id/model pair (`not any`) | Missing → `dedup_whole`; four rows instead of three. |
| 1702 id equality | Missing → `dedup_response_id`; distinct resp_3 wrongly removed. |
| 1702 model equality | Covered: `r25_gop_theo_id`. |
| 1704 parsed bad candidate (`loai == "ung_vien_hong"`) | Covered: `r26_phan_loai_theo_token`; escaped-key/empty-id fixture loses its loss count. |
| 1704 raw candidate token (`or ung_vien`) | Covered: `r26_doc_tron_bo_token`. |
| 1706 `loai is None` | Covered, round-4 finding fixed: `r26_doc_tron_khong_ro_ca_su_kien_khac`. |
| 1706 complete-line JSON-header requirement | Covered independently: `r26_doc_tron_khong_ro_khong_doi_json`; complete Ping control wrongly becomes unknown. Whole fallback removal: `r26_doc_tron_khong_parse_bo_qua`. |
| 1709 multi-read/EOF candidate branch | Covered loss action: `r26_bo_dem_mat_nhieu_doan`; every-cut assertion now demands `mat`, so unknown is not accepted as equivalent. |
| 1713 prefix regex matched (`k`) | Missing → `prefix_match_guard`; escaped-key input records AttributeError instead of unknown. |
| 1715 strict prefix UTF-8 | Covered: `r26_loai_khong_utf8_thay_the`. |
| 1720 decoded type is non-None | Missing → `prefix_decoded`; existing invalid-UTF-8 type wrongly produces DO_DUOC. |
| 1720 decoded type is outside candidate set | Covered: `r26_tien_to_ung_vien_tha`; dedicated direct-helper target. No equivalence exemption is needed for this branch. |
| 1720 confirmed-other early return | Covered: `r26_bo_xac_nhan_su_kien_khac`. |
| 1722 multi-read JSON-header requirement | Covered: `r26_khong_ro_moi_dong_dai`, and shared-regex `r26_khong_ro_khong_doi_json`; unknown count itself has `r26_khong_ro_khong_dem`. |
| 1729 bounded normal reads | Covered: `r25_doc_khong_tran`. EOF sentinel is the standard BytesIO/FileIO bytes contract; input consumes the same bounded loop in all fixtures. |
| 1730 reset state only on a new physical line | Covered: `r26_khong_dat_lai_moi_dong`. |
| 1732 actual LF detection | Missing → `lf_detection`; existing EOF-cut frame is wrongly accepted when every read is called complete. |
| 1734 first chunk of physical line | Covered: `r25_cho_phep_ca_dong_cut`. |
| 1734 exact raw allow-list membership | Covered: `r25_ghi_moi_dong_tron`, `r25_cho_phep_theo_tien_to`, `r26_cho_phep_cat_moi_CRLF`. Raw comparison precedes all normalization. |
| 1738 first-chunk assignment versus continuation | Missing → `first_chunk_capture`; prefix overwritten, known unknown JSON disappears from completeness evidence. |
| 1741 prefix bound and nonnegative slice | Covered individually: `r26_tien_to_khong_tran`, `r26_tien_to_bo_max`; append behavior also has `r26_dau_dong_khong_noi`. |
| 1742 whitespace compaction / 1744 cross-read tail | Covered: `r26_khong_bo_khoang_trang`, `r26_bo_duoi_vat`. ANSI cleanup for complete-line parsing has `r25_bo_go_ansi`; no claim is made that it independently mutates the separate streaming ANSI normalization. |
| 1743 preserve previously seen candidate | Covered: `r26_token_khong_dinh`. |
| 1743 discover a candidate in current compacted bytes | Missing → `candidate_search`; existing cut sweep has no `mat` at cap 60. |
| 1745 classify at physical LF only | Missing → `classify_only_at_lf`; known-other event wrongly becomes unknown before its line completes. |
| 1747 classify EOF fragment | Covered: `r26_bo_dong_cut_EOF`. |
| 1754 reader errors | Covered: `r25_DO_DUOC_khi_loc_hong`; passing errors into status also has `r25_so_khong_chuyen_loi`. |
| 1756 unfinished reader | Covered: `r25_DO_DUOC_khi_ong_con_mo`. |
| 1758 any candidate loss | Covered: `r25_DO_DUOC_khi_mat`, `r25_so_khong_chuyen_mat`. |
| 1760 any unknown JSON receive line | Covered: `r26_DO_DUOC_khi_khong_ro`, `r26_so_khong_chuyen_khong_ro`. |
| 1763 at least one positive frame | Covered: `r25_DO_DUOC_khong_khung`. |
| 1787 start-failure handler and pipe close | Covered: `r26_luong_hong_lot_ra`, `r26_luong_hong_khong_dong_ong`, `r26_luong_hong_khong_ghi_loi`. |
| 1795 only join a started thread | Covered: `r26_cho_luong_chua_chay`. |
| 1796 wait bound / 1797 latch / 1798 close | Covered: `r25_doc_ong_khong_han`, `r25_bo_chot_luong`, `r26_dong_tep_truoc_chot`, `r26_san_xuat_dong_tep_truoc`, `r26_ket_thuc_khong_dong_tep`. |
| 1803 unlatched defaults to incomplete / no late resampling | Covered: `r26_mac_dinh_chua_chot_la_xong`, `r26_lay_mau_lai_luong_muon`. |
| 1808 write negative-status reason | Missing → `reason_guard`; existing actual-reader failure retains KHONG_DO_DUOC but omits its required reason. |
| 1934 Codex routing, positive side | Missing → `codex_mode_disabled`; required fake-child case loses model metadata. Opposite non-Codex side has `r25_loc_ca_luot_khong_phai_codex`. |
| 1937–1938 binary/unbuffered output contract | `r26_tep_stderr_co_dem` specifically removes unbuffering; target observes real FileIO. The shared Codex/non-Codex selector is included in routing checks. |
| 1941 apply Codex environment / 1946 record inherited override | Missing → `codex_env_guard`, `rust_override_record`. Existing value-specific mutations `r25_khong_bat_trace` and `r25_noi_rust_log_thua_ke` do not remove these predicates. |
| 1956 pipe routing / 1958 reader startup | Missing → `codex_pipe_guard`, `codex_reader_guard`; target status fails for the corresponding broken integration, with no unrelated exception credit. |
| 2025 finalize existing filter object | Missing → `finish_object_guard`; no latch, so positive fake-child measurement becomes KHONG_DO_DUOC. |
| 2030 write filter evidence | Covered: `r26_khong_ghi_so`. |

`python3 -B review-r26e-g564iDKA/integration_mutants.py`: rc **0**, **6/6** additional target signals. Combined supplemental executions: **25/25** (22 additional focused removals, 3 historical removals). “Missing” rows sometimes describe two sides of one predicate or constituent/aggregate checks; these are **one P3 finding in one continuing class**, not 22 distinct findings.

The two removed redundant checks are valid simplifications:

1. `_STDERR_CHO_PHEP_DONG` is constructed exclusively from constants ending in LF or CRLF. Every member therefore ends in LF. Since `het_dong` is exactly `doan.endswith(b"\n")`, membership implies the removed `het_dong` conjunct. A member with `het_dong=False` is unreachable with the production constants.
2. `_RE_KHUNG` captures a string beginning `{` and ending `}`; strict `json.loads` is called without a custom decoder or object hook. Successful parsing of that top-level object yields a dict; scalar/array/extra-value inputs cannot reach a successful non-dict result. Parsing failures leave through the error path. The removed `isinstance(ev, dict)` rejection is unreachable after successful parsing.

The prefix rewrite is also equivalent under the nonnegative production limit: if the retained prefix already reaches/exceeds the limit, the new slice length is zero; otherwise it appends only the remaining capacity. It preserves an already-large first chunk needed for complete-line parsing. This is verified by the cap/append tests, with separate negative-slice and no-cap mutants.

## Earlier findings on 55a0afa796c1012c5551cd620bbdb5ab505dec3f

| Finding | Current status | Independently measured evidence |
|---|---|---|
| R25-SEC-01 P1 | Closed for the reported arbitrary-stderr disk-write path; stays closed. | Exact allow-list and sample-secret run-directory tests pass; unrestricted/prefix/continuation mutations fail. Raw allow-list comparison occurs before normalization; no raw fallback or trace spool was found. |
| R25-MEAS-02 P2 | Reported production defect stays closed. | Correct header/position/event, UTF-8, nonblank response metadata, and two-model tests pass. Additional independent provenance/dedup mutation omissions are now recorded under R26-TEST-14 P3. Format validation does not cryptographically attest a server. |
| R25-TEST-03 P2 | Three specific round-2 survivors stay closed, **3/3** killed; broader coverage class remains open at P3. | Reapplied generic-write-count removal loses 29 dropped bytes; default-unlatched removal returns DO_DUOC; late-production-latch removal is killed, and separate diagnosis confirms its final wrong DO_DUOC. |
| R25-ROBUST-04 P2 | Closed for reported unbounded reads; stays closed. | Normal and drain bounded-read targets pass; both unbounded-read mutants fail. Production read limit is 4 MiB. No memory-exhaustion stress claim. |
| R25-EVID-05 P2 | Closed for all reported fixtures, including round-3 whole-line parse failure; stays closed. | Cross-cut/whitespace sweeps now require actual `mat`. Existing complete invalid-UTF-8/escaped-key input: **329/329 bytes** dropped, `khong_ro=1`, one model retained, KHONG_DO_DUOC. Truncated-JSON/escaped-key input: **314/314**, same status. Removing the complete-line fallback restores DO_DUOC and is killed. |
| R25-RACE-06 P2 | Closed for reported snapshot/status inconsistency; stays closed. | Latch-before-copy and late-resampling cases pass and mutants fail. Status and serialized values use the same copied collections after reader latching. |
| R25-CONTRACT-07 P2 | Closed under superseding v2; stays closed. | Exact allow-list behavior is now required; lost non-allow-listed diagnostics are the accepted contract. Non-Codex stderr remains unchanged. |
| R26-ALLOW-08 P3 | Closed; stays closed. | Allowed LF **39/39** stored, CRLF **40/40**, repeated CR **0/41**, EOF fragment **0/38**; exact corresponding mutant fails at CR_CRLF. |
| R26-COUNT-09 P3 | Closed under real unbuffered contract; stays closed. | Native FileIO/RLIMIT_FSIZE probe: **43 input = 10 persisted + 33 dropped**, OSError recorded. Error drain and closed-sink cases pass, and dedicated short/error/count/closed/drain/unbuffered mutants die. |
| R26-EOF-10 P3 | Closed for finish-during-close; stays closed. | Production 10-second join case passes; object order and production order mutations die. Diagnostic confirms final DO_DUOC for both late-order removals, versus head KHONG_DO_DUOC. |
| R26-CLASSIFY-11 P3 | Closed for reported confirmed-other-event overcount; stays closed. | All-cap other-event controls pass. Unknown JSON is separate from known other events; Binary/Ping controls remain DO_DUOC with no loss/unknown counter at caps 256 and 4096. |
| R26-TEST-12 P3 | Closed; stays closed. | Registered zero-progress mutant fails specifically at `tra_0`: 39 bytes wrongly persisted, no OSError, only 4 dropped instead of 43. Short-write-loop mutant independently fails `ngan_roi_du`. |
| R26-TEST-13 P3 | Closed for both reported round-4 predicates, **2/2**. | New single-read-only and complete-other-event-only mutations fail the exact expected target assertions. The broader class is not closed because R26-TEST-14 remains. |
| Prior unreachable `bo_loc is None` failed-start note | No false-positive measurement found; failed-start behavior unchanged. | Popen failure exits before final filter serialization. The old purported failed-start measurement fallback is absent on this head. Actual absent executable: launcher rc **2**, receipt `hong`, null `ma_thoat`, no model/drop fields. It never claims DO_DUOC. |

## Security, evidence, and regression boundaries

`python3 -B review-r26e-g564iDKA/review.py exec observations review-r26e-g564iDKA/observations.py`: rc **0**, `OBSERVATIONS PASS`; numeric outputs in `observations.json` and full stdout in `logs/observations.json`.

| Boundary | Result and practical limit |
|---|---|
| Trace/credential content reaching disk | The only stderr write helper receives an exact allowed constant, and only from the first chunk of a physical line. Existing unknown-line, suffix/prefix, invalid-byte, CR, partial-line, continuation and sample-secret fixtures pass. The sample-secret test scans every retained run file. A short write can retain a prefix of the allowed constant, never arbitrary trace. |
| Complete-line classification | Strict valid candidate accepted once per id/model pair; malformed candidate metadata or raw candidate signal counts loss; unparseable JSON receive header with no token counts unknown; parsed noncandidate event does not. Both complete-fallback predicates now have independent supplied mutations. |
| Multiple chunks / EOF-cut | One classification after LF or EOF; full first chunk retained for complete parsing, bounded prefix for continuation recognition, compacted 64-byte carry and sticky candidate flag. Every existing cut/whitespace sweep passes. Truncated candidates count loss; unconfirmed JSON headers count unknown. Prefix-confirmed other events are ignored. Missing individual state/dispatch mutants are the P3 finding, not an observed head failure. |
| Cross-boundary recognition limit | No new attack inputs were authored. The measured corpus does not prove all possible encoding/framing combinations. Further payload-dependent directions would require executor-authored fixtures for escaped or duplicate event-type fields in oversized records and ANSI sequences split across normalization boundaries. No additional production bypass is claimed from unexecuted directions. |
| CRLF and controls | CR-only response: 186 dropped, no model, `mat=1`. CRLF response: 187 dropped, one model. Binary/Ping controls with a valid preceding model: 752 dropped, no loss/unknown, DO_DUOC at both tested caps. |
| Error drain and writes after close | Error messages are reduced to exception class names; no raw input/message is logged by the filter. Drain is bounded and counted. Closed sink counts the unwritten safe bytes; no fallback writes. The latched unfinished-reader state prevents late parsing or swallowed closed-file errors from making a positive completeness claim. |
| Write accounting | `buffering=0` produces native FileIO. Each successful write advances by its returned byte count; subsequent failure counts only the suffix. The real 10-byte file-limit experiment confirms the contract. Drop counts describe successfully read/discarded chunks; they cannot count bytes a child never successfully delivered or the reader never read. |
| Positive evidence | DO_DUOC needs a retained model, no error, completed latched reader, no loss, and no unknown count. All five conditions and counter/error transfer paths have effective supplied mutants. Lists/errors/counters are copied after latching; an active reader can still change later totals, but it cannot change the already-latched negative status. |
| Join boundary | `ket_thuc(10)` joins, samples liveness, then closes. Actual inherited-pipe case passes; unbounded-join mutation takes **40.2 s** and is killed. Finish-during-close remains incomplete. There is no independent EOF timestamp proving a nanosecond deadline across OS descheduling between join return and liveness sampling. |
| Run directory and hashes | Independent fake-child probe retains exactly `run.json`, `stderr.log`, `stdout.log`. Stored stderr **39 bytes**, `stderr_byte=39`, SHA-256 **1aa26269eb1cc57f86b235a03cda53c004edb5b1e9fc99d4da4f00843293d721**, equal to receipt; 186 trace bytes counted dropped. Receipt atomic temp writing receives selected metadata/counters, not raw trace. |
| Other sinks | Selected id/model/event strings are intentionally persisted under v2. Existing stdout and prompt-snapshot sinks and child-owned log stores are outside the stderr filter. No authenticated Codex run or universal all-process no-disk proof is claimed. |
| Timeout / kill 124 and 125 | Nine existing timeout/tree-kill regressions pass; r925 fake-Codex timeout asserts **124** with pre-timeout model retained. Independent real kill followed by deliberately incomplete confirmation returns launcher=receipt **125**, `giet_tron_ven=false`, one model retained. The latter tests the status selector without leaving a descendant alive. |
| Windows | Three existing Job Object/process-tree mocks pass. Creationflags and Job Object paths remain unchanged; codex, codex.exe, codex.cmd and CODEX.CMD identify true, Python false. Exact CRLF handling measured above. Native Windows launch/Job Object/handle inheritance/`.cmd` execution and the Windows CI lane are **not_run/unverified**. |
| Non-Codex | Required case and r14 persisted-log hash case pass. No new model/drop keys; ordinary stderr remains the preexisting direct sink. The filter's new environment is scoped to Codex. |
| Popen failure | Public `--bo-qua-probe` fixture with absent executable named codex returns rc **2**, receipt `hong`, no model/drop fields. Early exception handling and log closure remain intact. |
| Reader-thread start failure | Actual lenh_run with Thread.start forced to raise RuntimeError closes the pipe and finishes. Fake Python child's broken stderr returns **120**, preserved by launcher and receipt; model status KHONG_DO_DUOC with RuntimeError; stored/drop bytes **0/0** because no reader consumed bytes. No deadlock or positive measurement. |

## Right-reason qualifications and controls

`python3 -B review-r26e-g564iDKA/neutral.py`: rc **0**, **33/33** required cases also pass using an unmodified temporary launcher and the same companion-module layout as the mutants. Temporary copy layout does not explain the kills.

`python3 -B review-r26e-g564iDKA/review.py exec order-audit review-r26e-g564iDKA/order_audit.py`: rc **0**, **3/3** diagnostic expectations. Both `r26_san_xuat_dong_tep_truoc` and the adapted historical late-production-latch mutation first die at the fixture's close observation because a second close overwrites its first observation. Diagnostic instrumentation records all three target assertions without stopping: both also fail the final receipt assertion with **DO_DUOC None**. Head passes all three and records **KHONG_DO_DUOC / ong stderr con mo sau 10s**. This is diagnostic evidence, not a substitute for the ordinary target-origin signal; reviewed tests were not edited. The supplied object-order mutant independently reaches the wrong-final-status assertion in its ordinary target run.

`r26_ket_thuc_khong_dong_tep` dies because no close observation exists, which is the removed close operation itself. `r26_tep_stderr_co_dem` dies at the native FileIO check. Type-check mutations can cause an exception INSIDE the filter; the filter captures it and the named case explicitly rejects the incorrect classification. No uncaught setup/fixture exception is counted as a kill. The all-lines-write mutation first fails model status in its integration target, while its separate exact-list target directly detects forbidden sample-secret output. These distinctions are retained in the raw target outputs rather than described as interchangeable safety assertions.

Full repository-wide Linux suite and bare Ruff lint are **not_run in this round**. Measured scope is all 33 requested cases, 13 selected regressions, all 72 requested mutants/82 targets, 25 supplemental target runs, 33 neutral controls, and the boundary/order probes. Historical full-suite reports are not substituted for a current full-suite pass. Authenticated live Codex acceptance, Windows lane, remote authority/CI, push status, exact serving-model/build/effort/session ID, and outer launcher execution receipt remain unverified. This review does not grant merge or land authority.

## Final integrity, identity limits, and disposition

`python3 -B review-r26e-g564iDKA/final_integrity.py`: rc **0**. HEAD/tree/parent chain remain exact; status including tracked, untracked and ignored files is empty. Working-tree diff, staged diff, delta whitespace check, and `git fsck --connectivity-only --no-dangling` each rc **0**. Partial-clone/promisor config query rc **1**, no matches. Exact changed-path check yields only the two permitted files. Reviewed working-file bytes match `git show HEAD:<path>` **2/2**. All **102/102** scratch Python copies compile (98 launcher copies plus four companion copies); companion byte comparisons **4/4**. `_giet_cay`, `_job_windows`, `_pid_trong_job`, `_la_codex`, `_ghi_so`, and `KetGiet` remain AST-identical to b306e15, **6/6**. The reviewer integrity script emitted a harmless SyntaxWarning for its regex string; all checks completed, and the original output is retained.

Source SHA-256:

- launcher.py: `51342501e0126611f81748f614ef2246a7d87069b57ace67e72200a28862a7a1`
- launcher_test.py: `8ed1946c4741439f15813de1d6e0cffcd677fb11b4a6d3b71f3a3bbdea51bcbb`

Runtime observed: Linux x86_64, Python **3.13.16**. Provider identity reported by session: **OpenAI Codex / openai_codex**, GPT-6 based agent, OpenAI model family. Observed surface: tool-mediated shell in a managed Linux workspace; transport: machine. The enclosing CLI-versus-service identity, exact serving model/build/effort, session identity and outer launcher execution receipt cannot be independently verified here. The launcher invocation and local/unpushed branch status are requester-reported. No GitHub submitter; no GitHub/credential access, source edit, source commit, push, or comment. No sub-agents were used. The environment permits workspace writes; source read-only behavior was maintained by review procedure, not claimed as a separately enforced source mount. Clean snapshots and byte matches establish no observed source delta, not a forensic proof of every intermediate operation.

Evidence index: `review-r26e-g564iDKA/commands.jsonl` contains exact executed child commands, real rc, stdout/stderr and duration; `logs/` has individual command records. `targeted.json`, `mutations.json`, `regression.json`, `extras.json`, `more.json`, `integration-mutants.json`, `neutral.json`, `observations.json`, `order-audit.json`, and `final-integrity.json` retain the structured measurements. Driver output files and scratch source scripts are retained for reproduction. No prior-round run is represented as a current execution.

Final measured results: **33/33 requested cases; 72/72 supplied mutants with 82/82 intended target signals; 25/25 supplemental target signals; 13/13 regressions; 33/33 neutral-copy cases; 3/3 order diagnostics.** Earlier reported production fixes remain effective on their measured inputs. R26-TEST-13 is closed; the continuing every-guard mutation-coverage class remains open as **R26-TEST-14 P3**. The requested zero-P0–P3 criterion is not met. Size is separately reported as **1,113 cumulative additions / 717 fix-delta additions / 90 round-5 additions**, two files, not a code finding.

Completed UTC: **2026-10-25 10:50:25 UTC** (final report timestamp; source integrity measurements immediately precede finalization).

VERDICT: changes_requested
