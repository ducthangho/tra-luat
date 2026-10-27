# WP748 r28 round 3 — independent read-only review

Review complete: approve the exact candidate SHA. P0=0, P1=0, P2=0, P3=0. Environment and native-Windows limits are recorded below.

Reviewer: OpenAI Codex, based on GPT-6 as runtime instructions report. Provider: openai_codex. Execution surface: direct machine tools in this Linux container. The user states invocation through launcher.py run; the exact serving-model revision, outer transport/receipt, and call ledger are not independently exposed. launcher.out was empty at initial inspection. This is user-declared Codex call 3 of 10 (calls 1–2 blocked); no nested Codex calls or agents started.

Review class: sensitive. UTC started: 2026-10-27T03:32:38.498593+00:00.

Reviewed SHA: `7f89b21867e0c62aea21947e6f9da91ca0750742`; tree: `9182b0f519852d588cf0053763945499ab514c52`. Full, non-shallow clone, detached HEAD, clean status, single parent `f577ab5b467510f3fa7ed27107dc2eab539d3bef` = origin/master. No local branches. Remote-tracking refs are exactly origin/master and origin/ops/wp748-r28-l7-lease. The executor's branch name is provenance only, not the candidate identifier.

Frozen spec SHA-256 verified: `07e058391eb9b592d384c8eb7a8136f7ff49fed6dbc9847a1588d02e6c0814a3`. Lease read from the named local ops branch. Owner approval #748 issuecomment-6432555871 cannot be read or verified here; no GitHub access attempted. REMOTE_CHECK.txt is an executor claim dated 2026-10-27T03:30:32Z. The supplied ls-remote.txt contains 1397 advertised-ref lines and zero exact candidate-SHA matches, independently counted locally; its provenance/freshness and the live remote were not re-measured. Per this round's instruction this is not a blocker. Round 1's local tracking-ref fixture error is not evidence of a push; round 2's network-only blocker is not repeated.

Read-only boundary: no source edits, commits, pushes, comments, credentials, or network access. Bytecode writes will be disabled. Scratch evidence: `review-r28c.3cs6KP/`.

Initial environment: `/tmp/.git` exists, empty and read-only. It is left untouched. Candidate diff: 1 file (.claude/dev/launcher_test.py), 3 additions, 0 deletions, within ≤1 file/≤20 added.

## Identity commands and return codes

```text
$ git -C src rev-parse HEAD 'HEAD^{tree}'
rc=0
7f89b21867e0c62aea21947e6f9da91ca0750742
9182b0f519852d588cf0053763945499ab514c52
```

```text
$ git -C src rev-list --parents -n 1 HEAD
rc=0
7f89b21867e0c62aea21947e6f9da91ca0750742 f577ab5b467510f3fa7ed27107dc2eab539d3bef
```

```text
$ git -C src symbolic-ref -q HEAD
rc=1
```

```text
$ git -C src rev-parse --is-shallow-repository
rc=0
false
```

```text
$ git -C src status --porcelain=v1
rc=0
```

```text
$ git -C src for-each-ref '--format=%(refname) %(objectname)' refs/heads refs/remotes
rc=0
refs/remotes/origin/master f577ab5b467510f3fa7ed27107dc2eab539d3bef
refs/remotes/origin/ops/wp748-r28-l7-lease d4b267a228d77305cbf564925ce0cfd4f7dbfdcc
```

```text
$ git -C src config --get remote.origin.url
rc=0
https://github.com/ducthangho/tra-luat
```

```text
$ ls -d /tmp/.git
rc=0
/tmp/.git
```

```text
$ ls -la /tmp/.git
rc=0
total 264
dr-xr-xr-x    2 root root     40 Oct 27 03:32 .
drwxrwxrwt 6246 root root 266240 Oct 27 03:32 ..
```

```text
$ python3 --version
rc=0
Python 3.13.16
```

```text
$ git -C src diff origin/master HEAD --numstat
rc=0
3	0	.claude/dev/launcher_test.py
```

`git -C src show origin/ops/wp748-r28-l7-lease:ops/specs/wp748-r28-windows-dot-bien-khong-do-duoc.md` — rc 0; SHA-256 assertion and local advertised-ref file count — rc 0. Full command output: review-r28c.3cs6KP/identity.json.

## Review and measurement progress

- Target command: `python3 src/.claude/dev/launcher_test.py --lap-ca r927_lenh_run_ghi_effort_va_sandbox_vao_run_json --lan 1` — rc 0, 1/1 passed, 0 skipped, 0 broken, 1.58 seconds. See `review-r28c.3cs6KP/target.{json,log}`.
- Full candidate suite is running. Both CLI runs disable bytecode and pip index/version access (`PYTHONDONTWRITEBYTECODE=1`, `PIP_NO_INDEX=1`, `PIP_CONFIG_FILE=/dev/null`, `PIP_DISABLE_PIP_VERSION_CHECK=1`); credential-bearing environment variables are removed by name, not inspected. `CLAUDE_PROJECT_DIR` points to scratch so incidental hook markers stay outside src/. These controls are disclosed, not treated as a pristine CI environment.
- `PYTHONDONTWRITEBYTECODE=1 python3 review-r28c.3cs6KP/measure.py inventory` — rc 0. Loaded all 430 DOT_BIEN entries: exactly two list the changed target, `r27_lenh_run_khong_lay_mau` and `r27_lenh_run_khong_ghi_so`. Each has that single target, without a platform exclusion. Full inventory saved, not merely a search restricted to r27.
- Selected groups: r25=25, r26=99, r27=42, r952=2; 168 distinct mutants / 178 named-target executions. The strict harness uses a separate temporary launcher file per mutant, validates anchors and compilation, calls only named targets under `_co_lap_toan_cuc`, and requires TinHieuChotCa with the named target on the traceback for kill credit. Other exceptions are errors. RUST_LOG is removed for this measurement because round 2 identified inherited-value sensitivity; it is not silently counted as an r28 regression.
- The added return at `.claude/dev/launcher_test.py:11592` follows child exit/effort assertions (11579–11580) and non-Linux sandbox assertion (11589). There is no subsequent check to bypass; context-manager cleanup still runs. The Linux branch is byte-for-byte unchanged.
- `chay_dot_bien` classifies string returns as skipped targets (13491–13492), subtracts their count (13501), and reports KHONG DO DUOC when no measurable targets remain (13502–13507). A preceding TinHieuChotCa remains a kill. The production runner also counts unrelated exceptions as kills; the independent strict harness does not.

Measurement interruption: initial full-suite and strict-mutant attempts overlapped full-tree exports that exhausted scratch disk space (Errno 28). The initial suite rc=1 reported 190/307 executed passes, 2 skips, 117 failures; that run is invalid for regression attribution. Export and mutant harnesses exited 1. Logs retained as `disk-full-*`. Only reviewer-created export directories were removed; src/ was untouched. Reruns use narrowly exported relevant tracked paths to stay within scratch capacity.

## Off-Linux countercheck and simulation audit

`PYTHONDONTWRITEBYTECODE=1 python3 review-r28c.3cs6KP/simulate.py` — rc 0. Fresh narrow exports (`git archive <exact-SHA> .claude .github requirements.txt` and tar extraction, both rc 0) include the relevant tracked sources and fixtures. Before each measurement, launcher/test bytes were compared to `git show <exact-SHA>:<path>`. The two branch replacements each matched exactly once. Scratch sources were restored afterward.

| Off-Linux experiment | Candidate 7f89b218 | Master f577ab5 |
| --- | --- | --- |
| Neutral target | String skip, after existing checks | Pass |
| Remove sandbox.bat_dau() | String skip | Pass: mutant survives |
| Remove sandbox.ghi_so() | TinHieuChotCa kill | TinHieuChotCa kill |
| Actual chay_dot_bien, remove bat_dau | KHONG DO DUOC tren nen nay | SAI giet 0/1 |
| Actual chay_dot_bien, remove ghi_so | OK giet 1/1 | OK giet 1/1 |

The actual runner was invoked with its mutation list restricted to the two affected entries, with unrelated hook/harness tables empty; its `(failures, unmeasurable)` results were `(0,1)` on the candidate and `(1,0)` on master. Direct target runs independently established strict TinHieuChotCa kills, preventing the production runner's broad exception handling from supplying false credit. Evidence: `simulation.{json,log}` and `simulate.py`.

`r27_lenh_run_khong_ghi_so` has no alternate target: its sole target is this case (launcher_test.py:11680–11681). Removing `sandbox.ghi_so` leaves `sandbox_trang_thai` missing, so `.get(...) == "KHONG_DO_DUOC"` fails at line 11589, before line 11592. The only changed classification among all 430 DOT_BIEN entries is therefore the non-measurable `r27_lenh_run_khong_lay_mau`; no other mutant loses a real Windows measurement. A string return marks the entire neutral case as skipped for reporting even though its earlier checks executed; an assertion failure there still fails the case.

The executor's `sim2.py` was read critically. Its two replacements faithfully model the relevant sampler contract: non-Linux constructs `luong=None` (launcher.py:2027), `bat_dau` immediately returns (2042–2043), `ket_thuc` does not join (2125), and `ghi_so` sets KHONG_DO_DUOC (2131–2132). But sim2 runs only `--lap-ca`, whose rc=0 alone cannot distinguish pass from skip; it prints the child rc but does not propagate it as the script exit status, does not run the actual mutation classifier, and leaves scratch copies behind. The independent harness above checks explicit outcomes and the actual classifier instead.

Other platform behavior is not emulated: fake executable naming/chmod (`LA_WINDOWS`, launcher_test.py:6422), process creation flags (launcher.py:2293), Windows Job Object setup (745,2327), process identity via Win32 APIs (354), Windows run-record field (2329), path normalization/probe differences, and the platform name interpolated into the sandbox reason (2132, still Linux in this simulation). The sandbox status does not depend on that reason text; the target does not assert it. These omissions limit the experiment to the relevant off-Linux branch/classifier behavior. They do not establish native Windows process behavior or a passing full Windows job. Native Windows §3 acceptance remains not_run here.

An AST comparison also passed: removing only the candidate's added final non-Linux Return makes the entire target function AST identical to master's, proving existing statements and cleanup structure are preserved.

## Strict mutation results and environment control

`PYTHONDONTWRITEBYTECODE=1 python3 review-r28c.3cs6KP/measure.py mutants` — rc 0 on the valid rerun: **168/168 distinct mutants killed; 178/178 named-target TinHieuChotCa kills; 0 survived, 0 skipped, 0 other exceptions.** All r25/r26/r27/r952 entries were executed. Evidence: `mutants.json`, `mutants.log`, mutation sources in `mutants/`. The earlier disk-full attempt was not credited.

`PYTHONDONTWRITEBYTECODE=1 python3 review-r28c.3cs6KP/baseline.py` — rc 0 for the measurement/assertion harness. It freshly executes the prior round's 13 failing cases and all 10 skipped cases on exact master source, rather than adopting the earlier counts. Two hook cases initially stopped at a missing `ops/bash_nen.py` in the narrow scratch export; those initial outcomes are not valid attribution and are retained in `baseline-incomplete-fixture.json`. The exact master dependency was subsequently exported and those two cases rerun separately by `baseline_hook.py`.

The same baseline harness also measures `r26_rv5_codex_env_guard` on both exact source versions, with inherited and absent RUST_LOG. Neutral passes in all four combinations. The mutant survives with the inherited value and dies by TinHieuChotCa when RUST_LOG is absent on both master and candidate. This reproduces the pre-existing environment sensitivity and justifies the explicitly controlled strict run; it is not introduced by the three-line change. Evidence: `env-control.json`.

## Final measurements and master attribution

`python3 src/.claude/dev/launcher_test.py`, under the disclosed offline/read-only environment controls — **rc 1**, 357.55 seconds: **286/299 executed cases passed; 10 skipped; 13 failed; 309 total**. The expected clean-environment 307/307 with two skips was **not** obtained here. No failure or skip is counted as a pass.

The exact master countercheck reproduces **all 13 failures with the same reasons** (normalizing only generated /var/tmp names) and **all 10 skip names/reasons**. `baseline_hook.py` — rc 0; its two corrected hook-fixture measurements fail by TinHieuChotCa for the same post-materializer assertion as the candidate. `finalize.py` comparison assertions — rc 0; full evidence in `comparison.json` and `baseline.json`. These are targeted baseline reruns, not a claim that the full master suite passed.

| Candidate case (same result on master) | Observed failure / attribution |
| --- | --- |
| `r858_goc_tam_tranh_to_tien_co_git` | Read-only /var/tmp; Errno 30. |
| `t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac` | Read-only /var/tmp; Errno 30. |
| `r484_g2_doctor_doc_dung_home_da_materialize` | doctor ignored the credential in CODEX_HOME |
| `r484_g2_schema_truoc_freshness_va_home_materialize` | freshness hid invalid schema |
| `r484_g2_child_khong_nhan_snapshot_va_rac_chan_truoc_probe` | inert launcher child failed: CHAN [13]: Không chuẩn bị được Codex credential; chưa chạy child |
| `r484_g2_storage_kernel_guardrails` | OSError: Codex home is inside a repository |
| `r484_g2_recovery_probe_rollback_va_snapshot_moi` | OSError: Codex home is inside a repository |
| `r484_g2_probe_isolated_marker_va_refresh` | OSError: Codex home is inside a repository |
| `r484_g2_hook_shell_scrub_truoc_probe` | No call after materializer; blocked by repository-ancestor credential-storage guard. |
| `r484_g8_hook_scrub_kin_voi_bash_env` | No call after materializer; blocked by repository-ancestor credential-storage guard. |
| `r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do` | OSError: Codex home is inside a repository |
| `r484_g7_tu_choi_ghi_dung_ban_da_probe` | OSError: Codex home is inside a repository |
| `r484_g7_auth_doi_truoc_khi_thay_thi_giu_ban_moi` | OSError: Codex home is inside a repository |

The 11 r484 failures share the pre-existing empty, read-only `/tmp/.git` ancestor. The unchanged `_KhoCodex` guard rejects credential homes inside a repository (launcher.py:3258–3262). The other two failures use `_goc_tam_khong_git` (launcher_test.py:2349–2355), which selects /var/tmp as the first Git-free fallback without checking writability. Both mechanisms and failure messages reproduce on master. No changes to these paths or the sandbox mounts were made.

Skipped cases, each freshly reproduced on master:

- `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125` — fixture nay danh cho Windows; ban POSIX la t63 (chay duoc, khong bo qua)
- `r345_chan_socket_that_ma_than_hook_van_chay_dung` — KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r345_cac_phep_do_cuc_bo_van_dung` — KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r345_lop_tham_import_van_co_rang` — KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO` — KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r347_tham_import_van_song_tren_python_truoc_310` — KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO` — KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia` — KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r348_dot_bien_bo_isidentifier_lam_ca_dich_DO` — KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r484_g4_windows_sid_alias_identity` — BO QUA native Windows SID conversion

Eight skips are the r345/r347/r348 venv/pip fixtures, which cannot obtain their pypdf dependency offline. Two are native Windows-only cases. The candidate's changed target itself passes on Linux. The tests use disposable fixture repositories/commits and inert credential records; the review made no commits in src/ and used no real credentials.

## Final identity, size, budget, and decision

Source, index, and tracked/untracked/ignored working-tree status are clean after all tests. No hook marker or bytecode was left in src/. The partial-clone/promisor configuration query returned rc 1 with no matches (expected negative result); `--is-shallow-repository` was false. Final commands:

- `git -C src rev-parse HEAD 'HEAD^{tree}'` — rc 0; 7f89b21867e0c62aea21947e6f9da91ca0750742; 9182b0f519852d588cf0053763945499ab514c52
- `git -C src rev-list --parents -n 1 HEAD` — rc 0; 7f89b21867e0c62aea21947e6f9da91ca0750742 f577ab5b467510f3fa7ed27107dc2eab539d3bef
- `git -C src symbolic-ref -q HEAD` — rc 1; empty output.
- `git -C src diff --exit-code HEAD --` — rc 0; empty output.
- `git -C src diff --cached --exit-code` — rc 0; empty output.
- `git -C src status --porcelain=v1 --untracked-files=all --ignored` — rc 0; empty output.
- `git -C src for-each-ref '--format=%(refname) %(objectname)' refs/heads refs/remotes` — rc 0; refs/remotes/origin/master f577ab5b467510f3fa7ed27107dc2eab539d3bef; refs/remotes/origin/ops/wp748-r28-l7-lease d4b267a228d77305cbf564925ce0cfd4f7dbfdcc
- `git -C src diff --numstat origin/master HEAD` — rc 0; 3	0	.claude/dev/launcher_test.py
- `git -C src diff --check origin/master HEAD` — rc 0; empty output.

Evidence file hashes: `review-r28c.3cs6KP/evidence-sha256.json`. Ancillary source/spec/lease/instruction reads and scratch writes completed locally; no network query was run. The cloud-runtime skill was read, but no environment-status tool was available. No authentication/bootstrap doctor command was run because this review explicitly prohibits credential/network use.

Size: **PASS — 1 file, 3 added lines, 0 deleted**, against ≤1 file/≤20 added. Codex budget: **call 3 of 10**, as supplied; calls 1–2 are the blocked prior rounds. No additional agent/reviewer invocation was made; the outer call ledger and completed execution receipt remain outside this review's visibility.

**Findings: P0=0, P1=0, P2=0, P3=0.** Finding ID / severity / file:line / scenario / fix: none. Spec §2 is implemented exactly: all meaningful non-Linux checks remain before the string return, Linux behavior is unchanged, and no other DOT_BIEN target loses a measurement. The 178 strict mutation signals provide positive Linux evidence. The off-Linux countercheck reproduces master's reported failure and the candidate's corrected classification while retaining the ghi_so kill.

This is approval of the reviewed code at the exact SHA above. It does not claim a green full Linux suite in this sandbox, native Windows §3 workflow acceptance, verified GitHub owner approval, live remote absence, or merge/land authorization. Those limits are disclosed; the supplied remote-absence claim and known baseline-reproduced sandbox behavior are not treated as code defects or blockers in this round.

UTC completed: 2026-10-27T03:42:50.124558+00:00

VERDICT: approve
