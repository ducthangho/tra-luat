# Independent read-only review — WP748 r26, round 7

Reviewer: OpenAI Codex, as identified by this session's runtime instructions. No external provider attestation, launcher receipt identity, or hidden serving-model identifier has yet been independently verified. Review class: sensitive.

Reviewed commit: `be15ad5187c2f501a8682366804363e54860590e`

Reviewed tree: `ab5a981c05978bf4ae97288a8a027fde2437bd92`

UTC started: 2026-10-25T12:37:45.828918+00:00

## Identity gate — passed

Commands and actual output:
```text
$ git -C src rev-parse --verify HEAD
be15ad5187c2f501a8682366804363e54860590e
rc=0
$ git -C src rev-parse HEAD^{tree}
ab5a981c05978bf4ae97288a8a027fde2437bd92
rc=0
$ git -C src symbolic-ref -q HEAD
(no output; detached)
rc=1
$ git -C src rev-parse --is-shallow-repository
false
rc=0
$ git -C src status --porcelain=v1
(no output)
rc=0
```

`git -C src log -8 --format='%H %P'` (rc=0) confirms the exact parent chain be15ad5 → d5166b2 → 55a0afa → 0fe659e → 97bb4c5 → 143d43f → b306e15. The commit hash, not a branch label, identifies this review. Local and remote publication status cannot be independently established without network access; no network or credentials will be used. GitHub authority comments #748 issuecomment-6394503720 and issuecomment-6396160332 cannot be read here; their authority and raised ≤1000-added-line cap are supplied by the review request.

## Review procedure

Source edits, commits, pushes, GitHub comments and credential use are prohibited. Only this verdict and scratch artifacts will be written.

## Scope and specification

Local `master` is absent (git-show rc=128). Fallback spec read rc=0, SHA-256 `f20615ae559f377150cfd6a9cfd0bce4478bf28ae3d562a674588a9c6f9d4bdb`, matching the required v2 identifier. Lease read rc=0; offline later-head review is explicitly permitted. GitHub authority and publication remain unverified. Cloud runtime skill was read; no environment-status tool is available. No network work.

The entire new delta changes exactly the two allowed files. `git log --oneline 113e0d1..b306e15 -- <two files>` returns rc=0 and no output. Round seven changes only launcher_test.py.

Size commands and real outputs are retained in `review-r26g-5lBjpFda/size.json`: all rc=0. New fix delta: launcher.py +183/-68, launcher_test.py +664/-35, **847 added lines**, below the supplied raised cap of 1000 by **153**. Cumulative from e739ac1: **1243 additions** (252 + 991); requested round-four comparison: **640 additions**; round seven alone: **83 additions**. The cumulative number is reference only under the owner’s new-delta counting instruction.

## Execution setup

Scratch `review-r26g-5lBjpFda/` contains drivers, exact replacement inventory, command ledger, stdout/stderr/rc/durations and temporary launcher copies. Tests receive an explicit minimal environment without authentication variables, `PYTHONDONTWRITEBYTECODE=1`, a private /tmp HOME and an absent CODEX_HOME. The initial setup put CODEX_HOME beneath a repository ancestor: 27/34 cases passed, 7 fake-child cases were stopped by pre-existing rc=13 credential-home validation. This is a reviewer setup failure, not a source defect or mutation kill. Those results are preserved in targeted-setup-failed.json and logs-setup-failed/. Corrected runs follow. No actual credential is read or used.

Setup follow-up: the sandbox exposes `/tmp/.git`, so the first /tmp-home correction still hit the same existing guard (27/34 cases; 105/129 mutation target signals, 24 unrelated setup errors). These runs are retained under `*-setup2-failed.json` and `logs-setup2-failed/`, and **none is used as the final mutation evidence**. Selecting the verified absent root-level `/__r26g_absent_codex_home__` gives `exists=False`, `_dang_cho_snapshot=False`, without creating or reading credentials. The third required-case run is rc=0, **34/34 passed** (15 r925, 19 r926), each printing `1/1 qua, 0 bo qua, 0 hong`. Exact commands: `python3 src/.claude/dev/launcher_test.py --lap-ca <name> --lan 1`, invoked by `python3 -B review-r26g-5lBjpFda/review.py targeted`.

Selected regression driver: `python3 -B review-r26g-5lBjpFda/review.py regression`, rc=1 because its all-selected denominator includes a platform skip: **13 passed, 1 skipped, 0 failed**. Windows-only t62 reports a skip; it is not counted as passed. Details remain in regression.json.

## Registered mutations and controls — current head

`PYTHONDONTWRITEBYTECODE=1 python3 -B review-r26g-5lBjpFda/review.py mutants` — rc=0, **119/119** registered r25/r26 mutants compiled with unique replacement anchors; **129/129** designated target executions raised `TinHieuChotCa` with the named target in its traceback. Wrapper rc=42 means this exact signal; 43 wrong-origin, 44 unrelated exception, 45 skip and 0 survivor are never credited. All **24/24** round-seven r26_rv6 entries have intended signals.

`PYTHONDONTWRITEBYTECODE=1 python3 -B review-r26g-5lBjpFda/review.py neutral` — rc=0, **34/34** cases pass against an unchanged temporary launcher with byte-identical codex_cred.py and codex_env_policy.py companions. Replacements and hashes are in mutation-inventory.json; all 129 real assertion messages are in mutation-reasons.md. The legacy target-only/position and id/model aggregate mutants weaken multiple terms; the current registry also supplies separate mutants for those terms. The round-seven colon-whitespace mutant still changes two terms together, discussed below.

`python3 -B review-r26g-5lBjpFda/review.py exec observations review-r26g-5lBjpFda/observations.py` — rc=0, `OBSERVATIONS PASS`. Native unbuffered FileIO under a 10-byte file-size ceiling measured **43 input = 10 stored + 33 dropped**, OSError recorded. Fake-Codex run directory contains exactly run.json/stderr.log/stdout.log; stored stderr=receipt **39 bytes**, stored SHA-256=receipt **1aa26269eb1cc57f86b235a03cda53c004edb5b1e9fc99d4da4f00843293d721**, **186** trace bytes dropped. Popen failure with absent executable and explicit probe-bypass reason returns **2**, receipt hong, null ma_thoat, no model/drop keys. Production reader-start failure returns child **120**, KHONG_DO_DUOC/RuntimeError, stored/dropped **0/0** (no bytes read). After a real successful kill, withholding whole-tree confirmation produces launcher=receipt **125**, giet_tron_ven=false, one model retained. No fixture process intentionally remains alive.

`python3 -B review-r26g-5lBjpFda/review.py exec order-audit review-r26g-5lBjpFda/order_audit.py` — rc=0, **3/3** diagnostic expectations. The two late production-order mutants first trigger their target’s close-observation assertion (a second close overwrites its observation). Non-stopping diagnostic assertion capture additionally shows both fail the final receipt assertion with **DO_DUOC / None**, while neutral passes all three and records **KHONG_DO_DUOC / open pipe**. This distinguishes the intended evidence regression from the incidental first assertion. Ordinary target signals remain the mutation-kill evidence.

The short-write-loop mutant fails `ngan_roi_du`; the separate zero-progress mutant fails `tra_0`. Closed-sink and general-write-failure counter mutations fail their own byte-accounting assertions. Unrestricted-writing integration first fails model status, but its separate exact-list target directly observes forbidden sample bytes. Type-check and grammar mutations that raise inside the filter are killed by explicit target assertions about correct classification/no error, not credited merely for throwing an unrelated exception.

## New finding — R26-TEST-16 (P3)

**Location:** `.claude/dev/launcher_test.py:11018`, especially `:11047`, and the `DOT_BIEN` inventory at `:10813`; guards in `.claude/dev/launcher.py:1606`, `:1607`, `:1608`, `:1621`, `:1624`, `:1782`, `:1804`, `:1937`.

**Class:** `unguarded-filter-invariants`, continuing the prior test-coverage findings. The specific R26-TEST-15 omissions are fixed, but the claimed complete guard inventory is still incomplete. This is a test/acceptance defect, **not a demonstrated production credential leak or false DO_DUOC on this head**.

The clearest example is `r26_rv6_d_khoang_hai_cham`: it removes both `\s*` expressions around the prefix's colon. Its target fails because whitespace **after** the colon is needed. Removing only whitespace **before** the colon survives every required case. Thus the aggregate kill does not establish independent coverage of both components. Similar independently mutable rules and evidence-copy operations are absent from the registry.

The reviewer applied only temporary source mutations and reused every current r925/r926 fixture. No new attack payload was authored. Four audit drivers returned rc=0, meaning all measurements completed, **not** that surviving mutants were killed:

```text
$ PYTHONDONTWRITEBYTECODE=1 python3 -B review-r26g-5lBjpFda/extra.py
header_after_trace_separator pass 34 target_signal 0 other 0
candidate_literal_type_key pass 33 target_signal 1 other 0
candidate_closed_value pass 34 target_signal 0 other 0
prefix_space_before_colon pass 34 target_signal 0 other 0
prefix_space_after_colon pass 32 target_signal 2 other 0
rc=0
$ PYTHONDONTWRITEBYTECODE=1 python3 -B review-r26g-5lBjpFda/more.py
ansi_requires_escape_introducer pass 31 target_signal 3 other 0
header_requires_received_verb pass 34 target_signal 0 other 0
prefix_excludes_embedded_quote pass 33 target_signal 1 other 0
rc=0
$ PYTHONDONTWRITEBYTECODE=1 python3 -B review-r26g-5lBjpFda/state_audit.py
ansi_optional_escape pass 34 target_signal 0 other 0
snapshot_model_list pass 34 target_signal 0 other 0
snapshot_error_list pass 34 target_signal 0 other 0
snapshot_counters pass 34 target_signal 0 other 0
reader_daemon pass 0 target_signal 1 other 0
rc=0
$ PYTHONDONTWRITEBYTECODE=1 python3 -B review-r26g-5lBjpFda/trailing.py
frame_trailing_whitespace pass 34 target_signal 0 other 0
rc=0
```

**443/443 supplemental executions completed:** 435 passes, 8 target-origin signals, no unrelated exceptions or skips. Nine of fourteen temporary variants survive all 34 cases (**306/306** surviving executions). Two variants examine the same ANSI introducer rule. The additional binary-sink audit below brings the total to fourteen omitted independent rule/copy-operation groups, not fifteen new production bugs.

| Guard and scenario | Independent measurement / gap |
|---|---|
| 1606 ANSI CSI introducer must contain ESC | Making ESC optional survives 34/34. Deleting ESC outright is killed by 3 targets because it leaves the original escape byte unnormalized; that separate variant does **not** establish rejection of ordinary text resembling ANSI. Neither variant has its own registered entry. |
| 1607 whitespace between TRACE and target | Changing only this `\s+` to `\s*` survives 34/34. The new before-TRACE mutation covers the other separator. |
| 1607 literal Received verb | Broadening only Received to a non-whitespace word survives 34/34. Immediate-position coverage does not remove this literal provenance constraint. |
| 1608 permitted whitespace after the JSON object | Removing only trailing `\s*` survives 34/34. A separate benign CRLF observation below shows this breaks actual supported framing. Removing the end anchor is a different rule. |
| 1621 exact candidate key | Broadening only the quoted `type` key is killed by the unknown-header case: its existing complete escaped-key/invalid-UTF-8 fixture becomes `mat=1` instead of `khong_ro=1` (329 dropped bytes). The registered prefix-key mutant changes `_RE_LOAI_DAU`, not this detector. |
| 1621 candidate value must end at its closing quote | Removing only that quote survives 34/34. The registered prefix closing-quote mutant changes another regex. |
| 1624 whitespace before colon | Removing only the first `\s*` survives 34/34; masked by the combined registered mutation. |
| 1624 whitespace after colon | Independent removal is killed by the known-other all-cap case (cap 187, 382 bytes, wrong unknown count) and prefix-cap case (cap 4096, 484 bytes). It currently shares the aggregate mutant with the preceding rule. |
| 1624 prefix capture must stop at a quote | Removing quote exclusion while keeping backslash exclusion is killed by the direct candidate-prefix case, which observes the missing unknown count. Closing-quote and no-backslash mutations retain this exclusion. |
| 1782 reader must be a daemon | Setting daemon=False independently kills the inherited-pipe target at **40.521 s**. Join(timeout=10) still executes; process shutdown waits for the non-daemon reader. No registered mutation changes this setting. |
| 1804 model-list snapshot | Removing only list(self.ket) survives 34/34. A late append changes the returned record under the mutant; current head retains its snapshot. |
| 1804 error-list snapshot | Removing only list(self.loi) survives 34/34. A reader error arriving after snapshot acquisition changes the selected reason under the mutant. |
| 1804 counter snapshot | Removing only dict(self.dem) survives 34/34. A reader update during conclusion changes serialized counters under the mutant. |
| 1937 Codex binary sink mode | Removing only the binary-mode selection is killed by the fake-Codex integration target, with its own rc assertion. No registered mutation changes this mode; changing buffering and disabling the whole Codex path are separate operations. |

`python3 -B review-r26g-5lBjpFda/review.py exec snapshot-observation review-r26g-5lBjpFda/snapshot_observation.py` — rc=0, **4/4 snapshot diagnostic expectations and 2/2 CRLF diagnostic expectations**. This uses benign supplied frame construction and deterministic simulated reader progress, not new attack content. With a latched live reader, head retains one model, open-pipe reason and counters 1/10. The respective isolated copy-removal variants expose two models, RuntimeError reason, or counters 2/20. All remain KHONG_DO_DUOC; the difference concerns the specified single-snapshot contract. A valid CRLF frame is accepted on head (one model, 187 discarded trace bytes, no loss); the trailing-whitespace mutant loses it (no model, mat=1). These establish that the relevant survivors are not merely equivalent code transformations.

`PYTHONDONTWRITEBYTECODE=1 python3 -B review-r26g-5lBjpFda/sink_mode.py` — rc=0, **1/1** target-origin signal. Selecting text mode independently conflicts with the unbuffered binary contract; the target explicitly detects failed execution. Together the five supplemental drivers complete **444/444** executions across **15** variants: **435 passes, 9 intended signals, 0 other errors/skips**. Nine variants still survive all 34 cases.

**Fix:** finish the independent inventory, register focused mutations for these missing rules and each snapshot operation, and split the colon-whitespace mutant. Bind already-detected variants to their demonstrated targets. Add small benign cases for each survivor: distinguish literal header/ANSI/candidate syntax, cover a CRLF model frame, and simulate reader progress after snapshot acquisition. For rejection cases, include prior valid model evidence so absence of all evidence cannot conceal a completeness error. Keep mutations independent; an incidental exception, an aggregate kill, or an unexecuted test direction is insufficient. No production rewrite is required by this finding.

Exact replacements, temporary paths and all outputs: `extra-inventory.json`/`extras.json`, `more-inventory.json`/`more.json`, `state-inventory.json`/`state.json`, `trailing-inventory.json`/`trailing.json`, and `sink-mode-inventory.json`/`sink-mode.json` under the scratch directory. Each source anchor matched once and every temporary file compiled.

## Current guard inventory

The filter was re-read on the exact current head; `predicate-ast.json` records **59** AST condition/exception/boolean/comparison nodes. The table groups related nodes but names each constituent's independent mutation. A reject action may be disabled instead of negating its condition when that removes the same safeguard. The regex/copy/daemon omissions above are additional to the explicit Python predicates, not ignored because they lack an `if` statement.

| Current source lines / condition | Independent registered coverage |
|---|---|
| 1642 optional counter / retain supplied counter | r26_rv5_optional_counter_init; r26_rv5_retain_caller_counter |
| 1645–1649 filter exception / error latch / bounded drain / drain accounting | r25_bo_loc_hong_khong_ghi_loi; r25_bo_loc_hong_khong_xa_ong; r25_xa_ong_khong_tran; r26_xa_khong_dem |
| 1656 frame-match dispatch | r26_rv5_frame_match_guard |
| 1659–1660 strict UTF-8 and ValueError handling | r26_utf8_thay_the; r26_rv5_exception_valueerror |
| 1663 eligible event / 1666 response object | r25_moi_su_kien; r26_response_khong_kiem_object |
| 1667 id type, id nonblank, model type, model nonblank | r26_id_khong_kiem_chuoi; r26_id_khong_strip; r26_model_khong_kiem_chuoi; r26_model_khong_strip |
| 1684 short-write loop / 1686 zero progress | r26_ghi_khong_lap; r26_ghi_bo_chot_0_byte |
| 1689 closed sink / 1691 generic failure and unwritten suffix | r26_tep_dong_khong_dem; r26_ghi_loi_khong_dem; r26_ghi_dem_ca_doan |
| 1699 single chunk and complete physical line | r26_mot_doan_bo_dieu_kien_so_doan; r25_parse_khong_can_ca_dong |
| 1701 parsed model non-None | r26_rv5_parsed_model_guard |
| 1702 dedup whole / id equality / model equality | r26_rv5_dedup_whole; r26_rv5_dedup_response_id; r25_gop_theo_id |
| 1704 parsed bad candidate / raw candidate / loss action | r26_phan_loai_theo_token; r26_doc_tron_bo_token; r25_bo_dem_mat |
| 1706 no parsed event / JSON header / complete fallback | r26_doc_tron_khong_ro_ca_su_kien_khac; r26_doc_tron_khong_ro_khong_doi_json; r26_doc_tron_khong_parse_bo_qua |
| 1709 multi-chunk or EOF candidate loss | r26_bo_dem_mat_nhieu_doan |
| 1713 prefix-match dispatch / 1715 strict prefix decode | r26_rv5_prefix_match_guard; r26_loai_khong_utf8_thay_the |
| 1720 decoded type present / not candidate / return for other event | r26_rv5_prefix_decoded; r26_tien_to_ung_vien_tha; r26_bo_xac_nhan_su_kien_khac |
| 1722 JSON-header condition / unknown action | r26_khong_ro_moi_dong_dai; r26_khong_ro_khong_dem; shared grammar r26_khong_ro_khong_doi_json |
| 1729 bounded read / 1730 new-line reset / 1732 LF detection | r25_doc_khong_tran; r26_khong_dat_lai_moi_dong; r26_rv5_lf_detection |
| 1734 first chunk / raw exact membership | r25_cho_phep_ca_dong_cut; r25_ghi_moi_dong_tron; r25_cho_phep_theo_tien_to |
| 1738 first-chunk capture | r26_rv5_first_chunk_capture |
| 1741 prefix append / upper bound / nonnegative remaining space | r26_dau_dong_khong_noi; r26_tien_to_khong_tran; r26_tien_to_bo_max |
| 1743 sticky candidate / detector search | r26_token_khong_dinh; r26_rv5_candidate_search |
| 1745 classify only at LF / 1747 EOF-cut classification | r26_rv5_classify_only_at_lf; r26_bo_dong_cut_EOF |
| 1754 error / 1756 unfinished reader / 1758 loss / 1760 unknown / 1763 no model | r25_DO_DUOC_khi_loc_hong; r25_DO_DUOC_khi_ong_con_mo; r25_DO_DUOC_khi_mat; r26_DO_DUOC_khi_khong_ro; r25_DO_DUOC_khong_khung |
| 1787 startup exception handling / error latch / pipe close | r26_luong_hong_lot_ra; r26_luong_hong_khong_ghi_loi; r26_luong_hong_khong_dong_ong |
| 1795 started-thread condition / 1796 bounded join / 1797 latch / 1798 close | r26_cho_luong_chua_chay; r25_doc_ong_khong_han; r25_bo_chot_luong; r26_ket_thuc_khong_dong_tep; order r26_dong_tep_truoc_chot |
| 1803 never latched defaults negative / no late resampling | r26_mac_dinh_chua_chot_la_xong; r26_lay_mau_lai_luong_muon |
| 1805 error, loss, unknown evidence handoffs / 1808 reason | r25_so_khong_chuyen_loi; r25_so_khong_chuyen_mat; r26_so_khong_chuyen_khong_ro; r26_rv5_reason_guard |
| 1934 Codex versus other run / 1938 unbuffered sink; 1937 binary selection has the new gap | r26_rv5_codex_mode_disabled; r25_loc_ca_luot_khong_phai_codex; r26_tep_stderr_co_dem |
| 1941 environment application / 1945 exact override / 1946 override record | r26_rv5_codex_env_guard; r25_khong_bat_trace; r25_noi_rust_log_thua_ke; r26_rv5_rust_override_record |
| 1956 pipe route / 1958 reader construction | r26_rv5_codex_pipe_guard; r26_rv5_codex_reader_guard |
| 2025 finish / ordering / 2030 serialization | r26_rv5_finish_object_guard; r26_san_xuat_dong_tep_truoc; r26_rv5_old_late_production_latch; r26_khong_ghi_so |

Regex/normalization inventory:

| Component | Current coverage / disposition |
|---|---|
| Exact allow-list and LF/one-CRLF construction | exact/prefix/continuation mutations, r26_cho_phep_cat_moi_CRLF and r26_rv6_j_bo_CRLF |
| ANSI introducer; parameters; intermediate bytes; final byte | introducer gap R26-TEST-16; other three have r26_rv6_a_* |
| Header anchored timestamp; required TRACE; separator before TRACE; separator after TRACE | r26_rv6_b_bo_neo_dau / b_moc_thoi_gian; b_muc_TRACE; b_khoang_truoc_TRACE; after-TRACE gap |
| Exact target; immediate receive position; literal Received; final message separator | r26_rv5_target_only; r26_rv5_receive_position_only; literal-verb gap; r26_rv6_b_dau_cach_sau_message |
| Whole JSON object capture; end anchor; trailing whitespace | r26_rv6_c_doi_tuong_json; c_neo_cuoi; trailing-whitespace gap |
| Candidate key; response dot; event alternatives; closing quote | candidate-key gap; r26_rv6_e_cham_bat_ky; e_bo_completed plus candidate-search/cut cases; closing-quote gap |
| Whitespace compaction; carry size/use; ANSI cleanup in streaming path | r26_khong_bo_khoang_trang / r26_rv6_f_chi_dau_cach; r26_bo_duoi_vat / r26_rv6_g_duoi_ngan; r26_rv6_h_luong_khong_ansi |
| ANSI cleanup for complete parsing/prefix classification | r25_bo_go_ansi |
| Prefix leading object; post-brace whitespace; quoted key; two colon whitespace expressions | object/fallback observation below; r26_rv6_d_khoang_sau_ngoac; d_khoa_type; combined mutant leaves independent gaps |
| Prefix quoted string closure; excludes escape; excludes quote | r26_rv6_d_dong_nhay; d_khong_escape; independent quote-exclusion gap |
| JSON-header opening brace; prefix cap; read cap; eligible-event constant | r26_khong_ro_khong_doi_json (rv6_m is an exact duplicate); r26_rv6_i_tran_dau_nho plus bound mutations; both bounded-read mutations; r26_rv6_l_su_kien_bo_completed / r25_moi_su_kien |

Actual redundancy/unreachability proofs: (1) every allow-list member ends in LF, so membership already implies `het_dong`; the deleted extra condition adds no state. (2) `_RE_KHUNG` captures a whole brace-delimited JSON object, so successful standard json.loads without custom hooks cannot return a non-dict; the removed type check is redundant, with its grammar premise now separately tested. (3) removing only the leading `^` is equivalent at current call sites because all three derived regexes use `.match` at position zero; rv6_b_bo_neo_dau adds a leading wildcard and therefore tests a different, reachable expansion. (4) widening only the prefix opening brace to optional would not change the no-brace path: a candidate was already counted before prefix classification; a noncandidate either returns early or falls through to `_RE_DAU_JSON`, which rejects the missing brace. Prefix recognition alone never stores a model. These proofs do not excuse any of the measured non-equivalent survivors above. Standard bytes-stream EOF sentinels are loop mechanics; bounded read and physical-EOF classification are separately covered.

## Earlier findings on be15ad5187c2f501a8682366804363e54860590e

| Earlier finding | Current disposition and fresh evidence |
|---|---|
| R25-SEC-01 P1 | **Reported production path remains closed.** Exact-list and sample-secret directory-scan cases pass; unrestricted, prefix and continuation mutations fail. No raw stderr fallback exists. |
| R25-MEAS-02 P2 | **Reported source/metadata defect remains closed.** Target/position/event, strict UTF-8, nonblank typed id/model and model-aware dedup tests pass; their independent mutants fail. New gaps are test coverage, not a demonstrated head provenance bypass. |
| R25-TEST-03 P2 | **Its previously reported surviving removals are closed.** Generic write-error count mutant dies at ngan_roi_nem; default-unlatched mutant yields wrong DO_DUOC and dies; late production latch is killed and its wrong receipt independently diagnosed. The broader every-guard acceptance class continues as R26-TEST-16 P3. |
| R25-ROBUST-04 P2 | **Closed for reported unbounded reads.** Normal and drain bounded-read cases pass; both unbounded-read mutants die. Production per-read cap remains 4 MiB. |
| R25-EVID-05 P2 | **All specifically reported paths remain closed.** Cross-boundary/whitespace/EOF sweeps pass and require loss counts. Complete unparseable JSON receive headers require khong_ro; the fallback-removal mutant fails on the existing escaped-key/invalid-UTF-8 fixture. |
| R25-RACE-06 P2 | **Reported latch-order production fix remains closed.** Latch-before-copy and late-resample cases pass and corresponding mutations fail. The three current copies are present and pass independent snapshot diagnostics. Their missing registered removals are part of the new P3 coverage finding. |
| R25-CONTRACT-07 P2 | **Closed under superseding v2.** Dropping non-allow-listed Codex diagnostics is explicitly authorized. The non-Codex test and persisted-log hash regression pass. |
| R26-ALLOW-08 P3 | **Closed.** Exact LF/CRLF test passes; rstrip variant dies at CR_CRLF. The continuation-equal-to-allow-list case also passes and kills its own first-chunk removal. |
| R26-COUNT-09 P3 | **Closed under actual unbuffered contract.** Native 43=10+33 accounting measured; short-write, zero-progress, suffix/error/drain/closed-file and unbuffered-open variants die. |
| R26-EOF-10 P3 | **Closed for finish-during-close.** Actual ten-second integration passes; object and production ordering mutations fail. Diagnostic confirms both late production variants falsely return DO_DUOC. |
| R26-CLASSIFY-11 P3 | **Reported other-event regression remains closed.** All-cap known-other controls, unconfirmed headers, Binary/Ping controls and prefix-decode cases pass; their mutants fail. |
| R26-TEST-12 P3 | **Closed.** Dedicated zero-progress removal fails specifically at tra_0, independently of short-write-loop removal at ngan_roi_du. |
| R26-TEST-13 P3 | **Both listed omissions closed.** Single-chunk and complete-other-event-condition removals die at their designated targets. |
| R26-TEST-14 P3 | **All listed omissions closed.** 23/23 r26_rv5 entries have intended target signals; previously duplicated entries remain covered. |
| R26-TEST-15 P3 | **All specifically listed omissions closed.** Required TRACE dies at muc_DEBUG; whole-frame end anchor at rac_sau_khung; object shape at mang_json; streaming ANSI at dem_truoc_ansi_trong_token (cap 188, 635 dropped bytes, false DO_DUOC in mutant). Timestamp/prefix-key/no-escape/closed-string variants also have effective registered targets. The completeness claim remains false for the separate omissions in R26-TEST-16. |
| Unreachable bo_loc-is-None failed-start note | **Remains resolved.** Actual Popen failure returns before final filter serialization, with rc=2/hong/null child exit and no model/drop fields. Reader-thread start failure is a separate tested negative-evidence path. |

The reported earlier production fixes are present and effective on their measured scenarios. No earlier code finding is silently treated as universally proved safe. Exactly one continuing P3 coverage finding is open here.

## Security and regression assessment

| Boundary | Evidence and practical limit |
|---|---|
| Disk allow-list | The sole filter sink receives a raw exact allow-list member at the first chunk of a physical line. Membership is checked before normalization. Supplied ordinary/sample-secret, invalid-byte, prefix/suffix, partial-line, CR-only, repeated-CR and continuation cases pass. A short write can persist only a prefix of an allowed constant. No trace spool or raw fallback was found. |
| Complete single-chunk classification | A strict matching frame with eligible parsed event and valid metadata is retained/deduplicated. Bad parsed candidate or raw candidate signal counts mat. Otherwise an unparseable JSON receive header counts khong_ro. Parsed other events do not produce unknown counts. |
| Multiple chunks / EOF-cut | A physical line is classified once at LF or final EOF. Sticky candidate signal counts loss; without it, a confirmed other prefix is ignored, and an unconfirmed JSON header counts unknown. Incomplete unsupported headers without candidate signal are not evidence that a response existed. |
| Cross-boundary detection | Whitespace compaction, ANSI normalization, 64-byte carry and sticky candidate signal pass the supplied every-cut fixtures, including the three new completed/tab/ANSI fixtures. This is bounded empirical coverage, not proof over every possible encoding or arbitrarily long split ANSI sequence. |
| Complete positive evidence | DO_DUOC requires retained model evidence, no filter error, latched reader completion, zero loss and zero unknown counts. Unlatched state is negative. Current copies keep the serialized evidence stable after the latch; independent diagnostics establish the copy operations' behavior. |
| Error drain and writes after close | Error text is reduced to exception class names. Drain reads remain bounded and discarded bytes are counted. Closed-file ValueError counts the unwritten allowed suffix. A live reader latched at finalization cannot later certify completion. Counts cover bytes actually read; unread child output is not falsely counted as observed. |
| Unbuffered accounting | Actual FileIO probe verifies the documented write contract. This does not claim correctness for arbitrary buffered/custom streams outside that contract. |
| Join and shutdown | Head inherited-pipe target: **10.541 s**, negative measurement. Head finish-during-close target: **10.448 s**, negative measurement. Unbounded-join mutant: **40.571 s**, intended elapsed-time failure. Non-daemon mutation independently takes **40.521 s** and fails. Liveness is sampled after join and before close; no independent EOF timestamp proves an instantaneous wall-clock boundary if the scheduler delays that sample. |
| Run directory and hashes | Sample-secret fixture scan passes. Independent run contains exactly run.json/stdout.log/stderr.log. stderr_byte and stderr_sha256 describe persisted bytes, not raw input volume; 39-byte/hash measurement matches receipt, and r14 passes. |
| Other sinks | Selected response id/model/event metadata are intentionally persisted by v2. Existing stdout, prompt snapshots, user-selected run-root behavior and child-owned files are outside an absolute all-process no-disk assertion. No authenticated Codex run was made. |
| Timeout and kill codes | Supplied Codex timeout retains prior model and returns 124. POSIX timeout/tree-kill regressions pass. Independent actual-kill/withheld-confirmation probe returns 125 in both launcher and receipt, with giet_tron_ven=false. Windows-only t62 is explicitly skipped. |
| Windows | creationflags and Job Object code remain unchanged; three relevant Windows mocks pass. codex/codex.exe/codex.cmd/CODEX.CMD identify as Codex, Python does not. Diagnostic allow-list CRLF and benign model-frame CRLF work on head. Native Windows process launch, Job Object/handle inheritance, `.cmd` execution and Windows CI are **not_run/unverified**. |
| Non-Codex | Required unchanged-stderr/no-extra-fields case passes. Binary/unbuffered opening, PIPE and RUST_LOG override remain scoped to Codex. |
| Popen failure | Real absent executable: rc=2, hong receipt, null child exit, no model/drop keys. No false successful filter evidence. |
| Reader-thread start failure | Real lenh_run with forced Thread.start RuntimeError closes the read pipe and completes; child broken-stderr rc=120 is preserved. KHONG_DO_DUOC/RuntimeError, no deadlock, 0 stored/0 observed discarded bytes. |

No further new payload-dependent production assertion is made. Executor-authored follow-up directions, not executed attack content: examine unusually long/split ANSI normalization, escaped or duplicate type fields in oversized records, and nested candidate-like material in parsed noncandidate events. Current tests cannot certify those entire input classes.

Full repository-wide Linux gate, full launcher suite, native Windows lane and authenticated live Codex acceptance are **not_run** in this offline review. The measured scope is all requested r925/r926 cases and r25/r26 mutations plus the documented regressions, independent mutations and local probes. Local lease/user instructions require offline review before push/gates; this review is not merge, land or deployment authorization.


## Final integrity, identity and disposition

`PYTHONDONTWRITEBYTECODE=1 python3 -B review-r26g-5lBjpFda/integrity.py` — rc=0, **FINAL INTEGRITY PASS**. HEAD/tree remain exact; detached check rc=1 with no output; non-shallow and non-bare checks rc=0/false. Tracked, untracked and ignored source status is empty. Working and staged diff checks, fix-delta whitespace check, and `git fsck --connectivity-only --no-dangling` each return rc=0 with no output. Partial-clone/promisor config query returns rc=1/no matches. Working source matches HEAD blobs **2/2**. Temporary Python files compile **137/137**, companion modules match **2/2**, registered replacements independently reconstruct **119/119**, and registered targets match inventory **129/129**. `_giet_cay`, `_job_windows`, `_pid_trong_job`, `_la_codex`, `_ghi_so`, and `KetGiet` are AST-identical to master base **6/6**. Production code is unchanged by rounds six and seven.

Source SHA-256:

- launcher.py: `51342501e0126611f81748f614ef2246a7d87069b57ace67e72200a28862a7a1`
- launcher_test.py: `ab0d929c039f6911f39370635f96de86ff7f50f8f844f6c64d98f509ed43103b`

Runtime observed: **Linux x86_64, Python 3.13.16**. Runtime instructions identify this reviewer as **OpenAI Codex, based on GPT-6**; provider `openai_codex`, model family `openai`. Observable execution surface: tool-mediated local shell in this managed workspace; transport `machine`. Exact serving model/build/effort, session independence attestation, enclosing CLI-versus-service identity and the outer `launcher.py run` execution receipt are **not independently visible or verified**. The requester reports launcher invocation; this report does not turn that statement into a verified receipt. GitHub authority comments, live publication/merge status and CI were not accessed. No credentials, source edit, source commit, push or GitHub comment; no subagents. Supplied tests create disposable fixture Git repositories and fixture commits outside src. Read-only source handling is a review procedure, not an independently attested mount property.

Evidence index: [scratch directory](review-r26g-5lBjpFda/), [command ledger](review-r26g-5lBjpFda/commands.jsonl), [required cases](review-r26g-5lBjpFda/targeted.json), [registered target results](review-r26g-5lBjpFda/mutants.json), [actual mutation assertion messages](review-r26g-5lBjpFda/mutation-reasons.md), [neutral controls](review-r26g-5lBjpFda/neutral.json), [regressions](review-r26g-5lBjpFda/regression.json), [runtime probes](review-r26g-5lBjpFda/observations.json), [final integrity](review-r26g-5lBjpFda/final-integrity.json). The ledger contains **855** parsed command records, including the explicitly excluded setup failures. Supplemental inventories/results and diagnostics are named in the finding. Source was never patched to make a test pass.

Final measured result: **34/34 requested cases pass; 119/119 registered mutant entries killed through 129/129 intended target signals; 34/34 neutral controls pass; 13 additional regressions pass and 1 Windows-only case is skipped.** The supplemental audit completed **444/444** executions: nine independently meaningful variants survive all 34 cases; other variants demonstrate further missing individual registry entries. All specifically reported earlier production defects and the particular R26-TEST-15 omissions remain closed on their measured scenarios. One continuing coverage finding remains: **R26-TEST-16 P3**. Open counts: **0 P0, 0 P1, 0 P2, 1 P3**. The owner's zero-P0–P3 criterion is not met.

Size: **847 new-delta additions ≤ 1000**; **1243 cumulative additions** from e739ac1 for reference. Size is within the supplied current authority and is not a finding.

Completed UTC: **2026-10-25T12:59:05.659937+00:00**.

VERDICT: changes_requested
