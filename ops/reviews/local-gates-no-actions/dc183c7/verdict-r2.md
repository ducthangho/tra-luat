# Independent Code Review (Round 2) — PR #1003 (`local_gate*` & `LOCAL_GATE.md`)

## 1. Preflight, Identity, and Governance Limitations

```yaml
review_type: advisory_independent_code_review
review_round: 2
repository: ducthangho/tra-luat
pr_number: 1003
reviewed_sha: dc183c7ceb0c8efda6c648e4bcddb8f16ab18064
previous_reviewed_sha: c0b7711850ecee2e7165564df2f84cb92afe5fa0
base_sha: ef34d88838bc125727670f494b15213b6c6f0c8d
reviewed_tree: 7aba374f0d962f3512a6d0341e057600a752fb04 # orchestrator-measured; not independently verified via git CLI
verdict: approve
assurance_state: advisory_review # NOT cross_approved, NOT same_provider_approved, NOT governance completion
packet_id: null # No frozen Packet Spec or lease exists for PR #1003
provider: google_antigravity
model_family: gemini
runtime_metadata_model: "Gemini 4 Argon (High)" # observed via harness <USER_SETTINGS_CHANGE> notification
model_self_report_caveat: "Model weights/endpoint cannot be independently verified from inside model inference (ADR-0050); identity relies on harness-supplied metadata."
execution_surface: antigravity
transport: machine/local
session_id: "5560112b-091f-4d31-a888-4fd5267a8376" # observed via harness <user_information> Conversation ID
independently_run: false
tests_status:
  passed: []
  failed: []
  skipped: []
  not_run:
    - "git rev-parse / git diff / git status preflight commands (not_run: CLI command tools denied)"
    - "python -B .claude/dev/local_gate_checks.py (not_run by Reviewer; 20/20 pass is executor-reported)"
    - "python -B .claude/dev/local_gate.py run/verify on local_gate_plan.json (not_run by Reviewer; 4/4 pass and verifier rc=0 are executor-reported)"
```

### Mandatory Disclosures & Caveats
1. **Static Review Only (`tests_status: not_run`)**: CLI command execution tools are denied in this environment; no `run_command` or permission calls were made. All five target files and `.git` ref files in `/workspace/argon-review-1003-r2` were inspected directly via `read_file`. Candidate test results (`local_gate_checks.py` 20/20, foundation plan 4/4, verifier `rc=0`) and prior-SHA bug reproductions are **executor/orchestrator-reported**, not reviewer-executed.
2. **Git OID Verification Source**: [`.git/HEAD`](file:///workspace/argon-review-1003-r2/.git/HEAD#L1), [`.git/refs/heads/agent/local-gates-argon-fixes`](file:///workspace/argon-review-1003-r2/.git/refs/heads/agent/local-gates-argon-fixes#L1), [`.git/logs/HEAD`](file:///workspace/argon-review-1003-r2/.git/logs/HEAD#L1), and [`.git/packed-refs`](file:///workspace/argon-review-1003-r2/.git/packed-refs#L1-L3) were read via `read_file` and match `dc183c7ceb0c8efda6c648e4bcddb8f16ab18064` (HEAD) and `ef34d88838bc125727670f494b15213b6c6f0c8d` (`origin/work` base). The tree OID `7aba374f0d962f3512a6d0341e057600a752fb04` and worktree cleanliness rely on orchestrator measurement rather than independent `git` CLI execution.
3. **Governance Limitation**: No frozen Packet Spec or lease exists for PR #1003. Under [`AGENTS.md` §1–§4](file:///workspace/argon-review-1003-r2/AGENTS.md#L1-L108) and [`docs/PROTOCOL_DA_PHIEN.md`](file:///workspace/argon-review-1003-r2/docs/PROTOCOL_DA_PHIEN.md), this verdict is an owner-authorized **advisory independent code review** (`advisory_review`), **not** `cross_approved`, **not** `same_provider_approved`, and **not** merge/land authorization.
4. **Correction of Round 1 Reviewer Naming Inaccuracies**:
   * In Round 1 (`c0b7711850ecee2e7165564df2f84cb92afe5fa0`), the Reviewer note inaccurately referred to `load_plan` (actual function name in [`local_gate.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L46) is [`read_plan()`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L50)), referred to nonexistent receipt fields `negative_matches` and `timed_out`, and used `"timeout"` instead of `"timeout_seconds"` in the text reproduction snippets.
   * Round 1 `F02` also misattributed a linked-worktree prohibition to `LOCAL_GATE.md`; [`LOCAL_GATE.md#L32`](file:///workspace/argon-review-1003-r2/.claude/dev/LOCAL_GATE.md#L32) explicitly clarifies that linked worktrees remain supported by `local_gate.py` (`Linked worktree vẫn được hỗ trợ; kiểm tra này không coi worktree là standalone clone`).

---

## 2. Re-Evaluation of Prior Findings (`F01`–`F06`) on `dc183c7ceb0c8efda6c648e4bcddb8f16ab18064`

All five changed files in `/workspace/argon-review-1003-r2` were read in full:
* [`.claude/dev/LOCAL_GATE.md`](file:///workspace/argon-review-1003-r2/.claude/dev/LOCAL_GATE.md#L1-L92) (92 lines)
* [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L1-L328) (328 lines)
* [`.claude/dev/local_gate_plan.json`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_plan.json#L1-L64) (64 lines)
* [`.claude/dev/local_gate_linux_suites.json`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_linux_suites.json#L1-L100) (100 lines)
* [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_checks.py#L1-L248) (248 lines)

| Prior Finding | Class Slug | Status in `dc183c7c...` | Verification in Current Code |
| :--- | :--- | :--- | :--- |
| **`F01` (`P1`)** | `verify-bo-sot-rang-buoc-bien-nhan-va-symlink` | **Resolved** | [`verify()`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L269-L303) now rejects symlinks on `receipt.json`, `plan.json`, `runner.py` (lines 273–274) and step logs (line 298); enforces `type(r['schema_version']) is int` (line 279), `r['checkout_unchanged'] is True` (line 280), `r.get('approval') is False and r.get('full_ci_equivalence') is False` (line 281), 40/64-hex `r['tree']` (line 282), non-empty `started_at` and `finished_at` strings (lines 280, 283), `row.get('cleanup_complete') is True and row.get('containment') == 'linux_subreaper'` (line 289), `positive_matches` list of `True` booleans matching `len(s['positive'])` (lines 290–292), `row.get('env') == s.get('env', {})` (line 293), and `type(row['timeout_seconds']) is int` (line 294). [`read_plan()`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L50-L71) uses `type(...) is not int` for `schema_version` and `timeout_seconds` (lines 52, 61) and validates `isinstance(s['argv'], list)` and `isinstance(s['positive'], list)`. Locked by [`test_receipt_invariants_rejected`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_checks.py#L113-L132) and [`test_symlinked_artifacts_rejected`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_checks.py#L134-L145). |
| **`F02` (`P1`)** | `identity-mu-tep-ignored-va-bien-git-moi-truong` | **Resolved** | [`git()`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L31-L34) strips all `GIT_*` variables from `os.environ` and passes `--no-optional-locks`. [`identity()`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L44-L45) passes `--ignored=matching` to `git status --porcelain --untracked-files=all`. Locked by [`test_ignored_writes_invalidate_checkout`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_checks.py#L147-L156) and [`test_caller_git_override_is_not_inherited`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_checks.py#L158-L161). |
| **`F03` (`P1`)** | `ro-hau-due-setsid-va-mat-bien-nhan-khi-bi-tin-hieu` | **Resolved** | [`supervise()`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L100-L164) runs each step in a dedicated Linux supervisor process with `prctl(PR_SET_CHILD_SUBREAPER, 1)` (line 111), `stdin=subprocess.DEVNULL` (line 118), and signal-mask synchronization (`pthread_sigmask` at lines 116–121). In `finally` (lines 133–164), it ignores `SIGINT`/`SIGTERM`/`SIGHUP`, kills direct children via `/proc/[0-9]*/stat` `ppid == os.getpid()`, and loops `os.waitpid(-1, os.WNOHANG)` until kernel `ECHILD` (`ChildProcessError`) proves all reparented descendants across all sessions are reaped (`cleanup_complete: True`). [`execute()`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L210-L265) forwards termination signals to the supervisor, records `state: 'not_measured'`, stops remaining steps (`not_run`), and persists `finished_at`. Locked by [`test_timeout_reaps_detached_grandchild`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_checks.py#L167-L184) and [`test_sigterm_records_interruption_and_reaps_child`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_checks.py#L185-L212). |
| **`F04` (`P2`)** | `linux-suites-buoc-chay-tuan-tu-dot-bien-du-va-thieu-probe-cong-cu` | **Resolved** | [`local_gate_linux_suites.json`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_linux_suites.json#L6-L32) adds preflight steps `tools` (`ops/cong_cu.py kiem-tra --json`) and `ruff-version` (`ruff 0.15.15`), and pins `"env": {"CI_DANG_KY_WORKERS": "2"}` on `registry-suites` (lines 70–72). [`read_plan()`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L65-L68) restricts `step['env']` strictly to `CI_DANG_KY_WORKERS` in `'1'..'8'`. [`execute()`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L213-L215) isolates per-step `TMPDIR`/`TEMP`/`TMP` and `RUFF_CACHE_DIR` outside `--root`. Locked by [`test_explicit_worker_tuning_and_isolated_temp`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_checks.py#L213-L225). |
| **`F05` (`P2`)** | `kiem-tra-runner-nam-ngoai-so-dang-ky-va-ke-hoach-gate` | **Resolved** | Both [`local_gate_plan.json#L7-L17`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_plan.json#L7-L17) and [`local_gate_linux_suites.json#L34-L44`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_linux_suites.json#L34-L44) now execute `runner-checks` (`.claude/dev/local_gate_checks.py`) and require `^LOCAL_GATE_CHECKS_PASS ([1-9][0-9]*)/\1$`, emitted by [`local_gate_checks.py#L243-L248`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_checks.py#L243-L248) only when `testsRun > 0` and `skipped == 0`. Locked by [`test_both_plans_run_behavior_checks`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_checks.py#L236-L240). |
| **`F06` (`P3`)** | `write-receipt-khong-fsync-va-dung-ten-tam-co-dinh` | **Resolved** | [`write_receipt()`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L74-L90) uses `tempfile.mkstemp(prefix='receipt.', suffix='.tmp', dir=out)`, `os.fsync` on the file descriptor, atomic `Path.replace()`, `os.fsync` on the directory fd, and `temp.unlink(missing_ok=True)` in `finally`. Locked by [`test_receipt_temp_symlink_is_not_followed`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_checks.py#L226-L234). |

---

## 3. Bảng lớp của lượt review (Round 2 Review Class Table)

| Class slug | Phiên bản mẫu được kiểm | Vùng cùng lớp đã quét | Trạng thái |
| :--- | :--- | :--- | :--- |
| `verify-bo-sot-rang-buoc-bien-nhan-va-symlink` | [`verify()`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L269-L303), [`read_plan()`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L50-L71) | [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L50-L71), [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_checks.py#L113-L145) | **Sạch (Đã đóng `F01`)** |
| `identity-mu-tep-ignored-va-bien-git-moi-truong` | [`git()`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L31-L34), [`identity()`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L37-L47) | [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L31-L47), [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_checks.py#L147-L161) | **Sạch (Đã đóng `F02`)** |
| `ro-hau-due-setsid-va-mat-bien-nhan-khi-bi-tin-hieu` | [`supervise()`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L100-L164), [`execute()`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L167-L266) | [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L92-L266), [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_checks.py#L163-L212) | **Sạch (Đã đóng `F03`)** |
| `linux-suites-buoc-chay-tuan-tu-dot-bien-du-va-thieu-probe-cong-cu` | [`local_gate_linux_suites.json`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_linux_suites.json#L1-L100), [`execute()`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L195-L216) | [`.claude/dev/local_gate_linux_suites.json`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_linux_suites.json#L1-L100), [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_checks.py#L213-L225) | **Sạch (Đã đóng `F04`)** |
| `kiem-tra-runner-nam-ngoai-so-dang-ky-va-ke-hoach-gate` | [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_checks.py#L236-L248) | [`.claude/dev/local_gate_plan.json`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_plan.json#L1-L64), [`.claude/dev/local_gate_linux_suites.json`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_linux_suites.json#L1-L100) | **Sạch (Đã đóng `F05`)** |
| `write-receipt-khong-fsync-va-dung-ten-tam-co-dinh` | [`write_receipt()`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L74-L90) | [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L74-L90), [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_checks.py#L226-L234) | **Sạch (Đã đóng `F06`)** |

---

## 4. Remaining Actionable Findings

**None (`0` findings).** All six Round 1 findings (`F01`–`F06`) have been cleanly resolved in [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py), [`.claude/dev/local_gate_plan.json`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_plan.json), [`.claude/dev/local_gate_linux_suites.json`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_linux_suites.json), [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate_checks.py), and [`.claude/dev/LOCAL_GATE.md`](file:///workspace/argon-review-1003-r2/.claude/dev/LOCAL_GATE.md), and the new `PR_SET_CHILD_SUBREAPER` lifecycle, signal handling, receipt verification, and documentation boundaries are internally consistent and well-scoped.

---

## 5. Final Verdict

* **Verdict**: **`approve`** (advisory independent code review; `assurance_state: advisory_review`, **not** `cross_approved` or `same_provider_approved`)
* **Reviewed HEAD SHA**: `dc183c7ceb0c8efda6c648e4bcddb8f16ab18064`
* **Base SHA**: `ef34d88838bc125727670f494b15213b6c6f0c8d`
* **Orchestrator-Measured Tree SHA**: `7aba374f0d962f3512a6d0341e057600a752fb04`
* **Limitations**:
  1. Static review only (`independently_run: false`, all tests `not_run` by Reviewer due to CLI command tool denial).
  2. No frozen Packet Spec or lease exists for PR #1003; this review does not substitute for governance admission, Windows gate execution, or merge/land authority.
