# WP748 r28 round 2 — independent review

Review complete. No P0–P3 code findings; approval is blocked by the unverified required live remote-provenance check. Local measurements and limits are recorded below.

- Reviewer: OpenAI Codex; runtime instructions identify the agent as based on GPT-6. Exact serving-model revision and the outer launcher execution receipt are not independently exposed here.
- UTC started: 2026-10-27T03:17:53.661584+00:00
- Review class: sensitive. User-declared Codex call 2 of 10; round 1 blocked on fixture provenance. Call ledger not independently exposed.
- Reviewed SHA: `7f89b21867e0c62aea21947e6f9da91ca0750742`.
- Reviewed tree: `9182b0f519852d588cf0053763945499ab514c52`.
- Single parent and local origin/master: `f577ab5b467510f3fa7ed27107dc2eab539d3bef`. Full clone (`--is-shallow-repository`: false), detached HEAD, initially clean worktree, no local branch refs. Local origin remote URL: `https://github.com/ducthangho/tra-luat`. Only origin/master and origin/ops/wp748-r28-l7-lease remote-tracking refs exist.
- Frozen spec SHA-256 verified: `07e058391eb9b592d384c8eb7a8136f7ff49fed6dbc9847a1588d02e6c0814a3`.
- Owner approval reference supplied: #748 issuecomment-6432555871. I cannot read/verify the GitHub issue comment in this review and will not use credentials.
- No writes to src/, commits, pushes, or GitHub comments authorized. Test bytecode writes will be disabled. Scratch and this report only.

## Initial commands

- `git -C src rev-parse HEAD HEAD^{tree}` — rc 0, exact requested identity.
- `git -C src status --porcelain=v1` — rc 0, empty.
- `git -C src symbolic-ref -q HEAD` — rc 1, detached as required.
- `git -C src rev-list --parents -n 1 HEAD` — rc 0, single required parent.
- `git -C src rev-parse origin/master` — rc 0, required base.
- `git -C src rev-parse --is-shallow-repository` — rc 0, false.
- `git -C src for-each-ref` — rc 0; no candidate remote-tracking ref or local branch.
- `git -C src config --get remote.origin.url` — rc 0, GitHub URL above.
- `git show` frozen spec + Python SHA-256 assertion — rc 0.

## Remote identity check

Credential helpers, global/system Git config, extra Authorization headers, and interactive prompts disabled for `git -C src ls-remote origin` (command includes `-c credential.helper= -c http.extraHeader=`). rc 128. Advertised refs: 0. Candidate SHA matches: [].

```text
fatal: unable to access 'https://github.com/ducthangho/tra-luat/': Could not resolve host: github.com
```
A failed remote query is not proof that the candidate is absent.

## Review scope and code evidence

- Runtime surface: direct machine tool execution in a Linux cloud container; provider `openai_codex`, model family GPT-6 as runtime-described. The exact CLI/service entry transport and completed outer `launcher.py run` receipt are not exposed. `launcher.out` was initially empty. No new Codex invocation/subagent was started.
- `ls -d /tmp/.git` — rc 0. `ls -la /tmp/.git` — rc 0: existing empty read-only directory. It is left untouched.
- `python3 --version` — rc 0: Python 3.13.16 (Linux). This is not the workflow's Ubuntu Python 3.11 or Windows Python 3.13 runner.
- `git -C src diff origin/master HEAD --numstat` — rc 0: exactly 1 file, 3 additions, 0 deletions, `.claude/dev/launcher_test.py`; within ≤1 file/≤20 added.
- Source case lines 11572–11592: return is the final statement of the existing non-Linux branch, after child rc=0, effort values/status, and sandbox `KHONG_DO_DUOC` assertions. No existing assertion is bypassed. `San.__exit__` still runs on return.
- Exhaustive loaded `DOT_BIEN` inventory: 430 mutants total. Exactly two target this case: `r27_lenh_run_khong_lay_mau` (line 11679) and `r27_lenh_run_khong_ghi_so` (lines 11680–11681); each has this case as its sole target and no platform exclusion. No other mutant target lists include it.
- Selected prefix inventory: 25 r25 + 99 r26 + 42 r27 + 2 r952 = 168 distinct mutants. Target-level kill count is reported separately; the requested 178 is not the number of distinct mutants.
- `chay_dot_bien` lines 13489–13515 treats a string return as skipped, subtracts skipped targets from measurable targets, and emits `KHONG DO DUOC tren nen nay` when none remain. A `TinHieuChotCa` before the return remains a kill. The production DOT_BIEN runner also counts other exceptions; this review's harness deliberately does not give them kill credit.
- Scratch evidence: `review-r28.WcdBo9/`; independent measurement harness `measure.py`, inventory `inventory.json`. Bytecode writes are disabled via `PYTHONDONTWRITEBYTECODE=1`; mutant edits are confined to scratch copies. Full suite, target, and strict mutant measurements started.

## Measurement sequence

- Target: `PYTHONDONTWRITEBYTECODE=1 python3 src/.claude/dev/launcher_test.py --lap-ca r927_lenh_run_ghi_effort_va_sandbox_vao_run_json --lan 1` — rc 0; 1/1 passed, 0 skipped, 0 broken (1.45 s). Evidence: `review-r28.WcdBo9/target.{json,log}`.
- Strict initial mutant pass: `PYTHONDONTWRITEBYTECODE=1 python3 review-r28.WcdBo9/measure.py mutants` — rc 1; 168 distinct mutants, 167 killed/1 survived; 178 named-target executions, 177 TinHieuChotCa kills/1 survival/0 skip/0 unexpected error. The sole survivor is `r26_rv5_codex_env_guard`, not a user of the changed case. The inherited RUST_LOG already equals the exact target trace value, so disabling its assignment leaves that value unchanged. A controlled remeasurement with RUST_LOG removed from the test environment followed; the initial result is retained, not overwritten.
- `PYTHONDONTWRITEBYTECODE=1 python3 review-r28.WcdBo9/simulate.py` — rc 0. It exports both complete tracked trees using `git archive` (rc 0 each), checks launcher/test bytes against each exact SHA, verifies both branch-replacement anchors are unique, runs the target directly with strict exception classification, then invokes the actual `chay_dot_bien` function restricted to the two affected mutants.

| Simulated off-Linux case | Candidate | Master f577ab5 |
| --- | --- | --- |
| Neutral target | String skip after assertions | Pass |
| Remove sandbox.bat_dau() | String skip | Pass (mutant survives) |
| Remove sandbox.ghi_so() | TinHieuChotCa at non-Linux sandbox assertion | Same kill |
| Actual chay_dot_bien classifier, remove bat_dau | KHONG DO DUOC tren nen nay | SAI giet 0/1 |
| Actual chay_dot_bien classifier, remove ghi_so | OK giet 1/1 | OK giet 1/1 |

`khong_ghi_so` does not rely on a second target: its only target is the changed case. Removing the write leaves sandbox_trang_thai absent; `.get(...) == "KHONG_DO_DUOC"` is false at line 11589, before the new return. Evidence: `simulation.json` and `simulation.log`.

## Simulation limits

`sim2.py` was read, not trusted as a gate. Its two unique replacements correctly reproduce sampler construction (`luong=None`) and the target's non-Linux assertion branch. However, it runs `--lap-ca`, not `chay_dot_bien`, and prints the child rc without returning it as its own process rc. My independent simulation covers both gaps.

Neither script is a Windows runner. `LA_WINDOWS` remains false (fake codex naming/executable mode); `lenh_run` still uses POSIX start_new_session (launcher.py:2293), Linux process identity (354), and no Windows Job Object (750). Windows native process creation, identity/Job Object handling, path/ACL/credential-store branches (`os.name` at 3220), executable resolution/PATHEXT and console encoding are not exercised. The sampler reason text at 2132 still reports the real host Linux. These do not change the string-return classifier or bypass the preceding assertions; actual Windows §3 acceptance remains not_run.

## Observed test side effect / read-only limitation

`git status --porcelain=v1 --ignored` during execution reported `!! .claude/.packet_state/`. The ignored `src/.claude/.packet_state/session-start.ran` file is 28 bytes with mtime 2026-10-27 03:20:24 UTC. The existing suite's t152 executes the real session-start hook (launcher_test.py:6129), whose marker path defaults to the checkout (session-start.sh:42–47). No tracked source was edited. I did not delete this ignored marker because that would be another write in src/. The initial tracked/untracked status was clean; an initial ignored-file content snapshot was not taken, so I cannot claim a complete before/after proof for ignored files.

## Round-1 comparison

B1 from VERDICT_R28A.md concerned local origin/HEAD and origin/agent/wp748-r28-claude refs naming the candidate. On this fixture both refs are absent, there are no local branches, and the only remote-tracking refs are origin/master and origin/ops/wp748-r28-l7-lease. That local fixture defect is corrected. The original B1 was not evidence of a push, and is not carried forward as a code defect. The independent live-GitHub absence check remains unavailable (DNS failure, rc 128).

The suite is also reporting eight r345/r347/r348 skips because `_r345_venv` cannot prepare its venv/pip fixture. Its setup attempts `pypdf==3.17.4`. These skips are additional to the two platform-specific skips expected by the executor. They must not be counted as passed.

Additional static check: parsed both committed target functions with Python AST; removing only the candidate’s final non-Linux Return yields exact AST equality with master (rc 0). All existing checks and cleanup structure are preserved.

## Final candidate measurement counts

- Full suite: `PYTHONDONTWRITEBYTECODE=1 python3 src/.claude/dev/launcher_test.py` — **rc 1**, 385.92 s; **286/299 executed cases passed, 10 skipped, 13 broken, 309 total**. This does not reproduce the executor's 307/307 + 2 skipped. Eleven broken cases are r484 credential-storage fixtures under the pre-existing `/tmp/.git`; two more fail to create a fallback temporary directory under the read-only `/var/tmp`. Eight additional skips are venv/pip fixture setup failures. These are environment limitations, not silently converted to passes; an exact-master countercheck reproduced every failing case (see below). Evidence: `suite.json`, `suite.log`.
- Controlled strict mutant pass: `PYTHONDONTWRITEBYTECODE=1 python3 review-r28.WcdBo9/measure.py mutants-clean` — **rc 0; 168/168 distinct mutants killed, 178/178 named-target TinHieuChotCa kills, 0 survived, 0 skipped, 0 unexpected exceptions**. It removes inherited RUST_LOG from its test subprocess environment; no source changes. Evidence: `controlled/mutants-summary.json`, `controlled/mutants.jsonl`, `mutants-controlled.log`.
- Both passes run the complete prefix selection: r25/r26/r27/r952, not only the two affected mutants. Kill credit is only for the exception class owned by the loaded candidate harness and thrown during the exact named target. Bare AssertionError, syntax/import/setup exceptions, and string returns do not count as kills.

### Candidate failures (raw counts retained)

- `r858_goc_tam_tranh_to_tien_co_git`: OSError: [Errno 30] Read-only file system: '/var/tmp/lt_5alj3d_y'
- `t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac`: OSError: [Errno 30] Read-only file system: '/var/tmp/tmpjhnpyg5k'
- `r484_g2_doctor_doc_dung_home_da_materialize`: doctor ignored the credential in CODEX_HOME
- `r484_g2_schema_truoc_freshness_va_home_materialize`: freshness hid invalid schema
- `r484_g2_child_khong_nhan_snapshot_va_rac_chan_truoc_probe`: inert launcher child failed: CHAN [13]: Không chuẩn bị được Codex credential; chưa chạy child
- `r484_g2_storage_kernel_guardrails`: OSError: Codex home is inside a repository
- `r484_g2_recovery_probe_rollback_va_snapshot_moi`: OSError: Codex home is inside a repository
- `r484_g2_probe_isolated_marker_va_refresh`: OSError: Codex home is inside a repository
- `r484_g2_hook_shell_scrub_truoc_probe`: không đo được lời gọi nào SAU materializer: ['SACH -c ', 'import hashlib, os, secrets', 'khoa = secrets.token_bytes(16)', 'def vt(v): return hashlib.blake2s(v.encode("utf-8","replace"), key=khoa).hexd…
- `r484_g8_hook_scrub_kin_voi_bash_env`: không đo được lời gọi nào SAU materializer: ['SACH -c ', 'import hashlib, os, secrets', 'khoa = secrets.token_bytes(16)', 'def vt(v): return hashlib.blake2s(v.encode("utf-8","replace"), key=khoa).hexd…
- `r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do`: OSError: Codex home is inside a repository
- `r484_g7_tu_choi_ghi_dung_ban_da_probe`: OSError: Codex home is inside a repository
- `r484_g7_auth_doi_truoc_khi_thay_thi_giu_ban_moi`: OSError: Codex home is inside a repository

### Candidate skipped cases

- `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125`: fixture nay danh cho Windows; ban POSIX la t63 (chay duoc, khong bo qua)
- `r345_chan_socket_that_ma_than_hook_van_chay_dung`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r345_cac_phep_do_cuc_bo_van_dung`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r345_lop_tham_import_van_co_rang`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r347_tham_import_van_song_tren_python_truoc_310`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r348_dot_bien_bo_isidentifier_lam_ca_dich_DO`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r484_g4_windows_sid_alias_identity`: BO QUA native Windows SID conversion

## Baseline attribution and final identity

`PYTHONDONTWRITEBYTECODE=1 python3 review-r28.WcdBo9/baseline.py` — rc 0 for the countercheck harness; **all 13 observed candidate failures reproduce on master f577ab5**, not a passing baseline suite. The scratch master snapshot was restored to exact committed launcher.py/launcher_test.py bytes after simulation; no candidate source was used. Evidence: `baseline.json`, `baseline.log`. The /tmp/.git ancestor rejection is launcher.py:3258–3262; the fallback selector at launcher_test.py:2349–2355 picks the first Git-free directory, which is /var/tmp here, without a write probe. This accounts for the two read-only filesystem failures. These are unchanged environment-sensitive paths, not regressions from r28.

Final identity commands (full outputs in `final-identity.json`):

- `git -C src rev-parse HEAD HEAD^{tree}` — rc 0; 7f89b21867e0c62aea21947e6f9da91ca0750742; 9182b0f519852d588cf0053763945499ab514c52.
- `git -C src rev-list --parents -n 1 HEAD` — rc 0; 7f89b21867e0c62aea21947e6f9da91ca0750742 f577ab5b467510f3fa7ed27107dc2eab539d3bef.
- `git -C src symbolic-ref -q HEAD` — rc 1; (no stdout).
- `git -C src diff --exit-code HEAD --` — rc 0; (no stdout).
- `git -C src diff --cached --exit-code` — rc 0; (no stdout).
- `git -C src status --porcelain=v1 --untracked-files=all --ignored` — rc 0; !! .claude/.packet_state/session-start.ran.
- `git -C src diff --numstat origin/master HEAD` — rc 0; 3	0	.claude/dev/launcher_test.py.
- `git -C src for-each-ref --format=%(refname) %(objectname) refs/heads refs/remotes` — rc 0; refs/remotes/origin/master f577ab5b467510f3fa7ed27107dc2eab539d3bef; refs/remotes/origin/ops/wp748-r28-l7-lease d4b267a228d77305cbf564925ce0cfd4f7dbfdcc.

Tracked source and index remain unchanged; sole observed ignored path is the hook marker already disclosed. No review commit, push, GitHub comment, credential lookup, or authenticated remote query was performed. Test fixtures create their own disposable Git repositories/commits and synthetic credential records. Evidence SHA-256 manifest: `review-r28.WcdBo9/evidence-sha256.json`.

## Final findings and review decision

**Code findings: P0=0, P1=0, P2=0, P3=0.** There is no code finding ID/file:line/scenario/fix to report for this three-line diff. Spec §2 is satisfied: all meaningful non-Linux checks execute before the skip; only the unmeasurable `bat_dau` mutation changes classification. No other mutant loses a real measurement. Linux target behavior is unchanged, and all 178 selected named-target kills were remeasured under the disclosed controlled environment.

**B2 — review verification blocked (not a P0–P3 code defect).** Location: the required `git -C src ls-remote origin` identity/provenance check. Scenario: the rebuilt local refs match the requested fixture, but GitHub DNS resolution fails (rc 128), so this reviewer cannot verify the required claim that no remote ref advertises the candidate. Empty stdout from that failure is not a successful negative lookup. Resolution: obtain a successful credential-free remote-ref advertisement tied to this SHA through the authorized review/bootstrap environment. No source fix is indicated. The failed query establishes neither a push nor an identity mismatch.

Other unmeasured completion evidence is explicit: the full Linux suite is not green in this container (13 baseline-reproduced environment failures and 8 extra fixture skips); native Windows §3 acceptance is not_run, as anticipated by the prompt. The simulation supports the classifier repair but cannot certify the Windows workflow. I cannot read the supplied owner-approval GitHub comment or independently validate the completed outer launcher execution receipt/model revision; these are disclosed limits, not asserted code defects. This report does not claim merge/land authorization.

Additional environment control: an inline Python check on the restored exact-master snapshot ran the neutral case and `r26_rv5_codex_env_guard` with inherited RUST_LOG and with RUST_LOG absent (rc 0; `env-control.{json,log}`). Neutral passes in both; the mutant survives only with the inherited expected value and dies by TinHieuChotCa when absent. Thus the initial mutant discrepancy is baseline test-environment sensitivity, not introduced by r28.

`git -C src config --get-regexp '^(extensions.partialClone|remote\..*\.(promisor|partialclonefilter))$'` — rc 1, no partial-clone/promisor configuration found. Other read-only source/spec/lease/instruction inspections and scratch evidence writes completed with rc 0 unless separately recorded. The cloud-runtime status tool and policy snapshot were unavailable; no alternate network route or credential mechanism was attempted.

Size cap: PASS, 1 file / 3 added lines / 0 deleted. Codex budget: user-declared call 2 of 10; no nested Codex calls or agents.

UTC completed: 2026-10-27T03:28:45.092123+00:00

VERDICT: blocked
