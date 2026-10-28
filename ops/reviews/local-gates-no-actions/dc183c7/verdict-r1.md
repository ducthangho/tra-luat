# Independent Code Review — PR #1003 (`local_gate*` & `LOCAL_GATE.md`)

## 1. Preflight, Identity, and Governance Limitations

```yaml
review_type: advisory_independent_code_review
repository: ducthangho/tra-luat
pr_number: 1003
reviewed_sha: c0b7711850ecee2e7165564df2f84cb92afe5fa0
base_sha: ef34d88838bc125727670f494b15213b6c6f0c8d
reviewed_tree: 5d0b903a6b044c665db9685600e3200f037b51e6 # orchestrator-measured; not independently verified via git CLI
verdict: changes_requested
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
    - "git rev-parse / git diff / git status preflight commands (denied by CLI)"
    - "python -B .claude/dev/local_gate_checks.py (not_run: command execution denied by CLI)"
    - "All finding reproduction scripts F01..F06 below (not_run: command execution denied by CLI; provided as concrete scripts for Executor to run in /workspace/argon-review-evidence/scratch)"
```

### Mandatory Disclosures & Limitations
1. **Command Execution Denied by CLI (`not_run`)**: Every call to `run_command` in this review session was canceled by the CLI (`Tool execution was canceled`). Per owner instruction, no further command tool calls or bypasses were attempted, and `/workspace/argon-review-1003` was treated strictly as read-only via `read_file`.
2. **Git OID Verification Source**: Because `git` CLI execution was denied, `reviewed_sha` (`c0b7711850ecee2e7165564df2f84cb92afe5fa0`) and `base_sha` (`ef34d88838bc125727670f494b15213b6c6f0c8d`) were cross-checked via `read_file` against [`.git/HEAD`](file:///workspace/argon-review-1003/.git/HEAD#L1), [`.git/logs/HEAD`](file:///workspace/argon-review-1003/.git/logs/HEAD#L1-L2), [`.git/refs/heads/work`](file:///workspace/argon-review-1003/.git/refs/heads/work#L1), and [`.git/packed-refs`](file:///workspace/argon-review-1003/.git/packed-refs#L1-L2). However, the tree OID (`5d0b903a6b044c665db9685600e3200f037b51e6`), object graph integrity, and working-tree cleanliness were **provided by the orchestrator** rather than independently computed by `git rev-parse HEAD^{tree}` or `git status`.
3. **Governance Limitation (No Frozen Packet/Lease)**: PR #1003 introduces five new files outside any frozen Packet Spec or active lease under [`docs/PROTOCOL_DA_PHIEN.md` §4–§5](file:///workspace/argon-review-1003/docs/PROTOCOL_DA_PHIEN.md#L121-L265). Under [`AGENTS.md` §1–§2](file:///workspace/argon-review-1003/AGENTS.md#L25-L41), this review is conducted under direct owner authorization as an **advisory independent code review** (`advisory_review`). It does **not** grant `cross_approved`, `same_provider_approved`, or merge/land authority.
4. **Runtime vs. Self-Report Distinction**: `session_id` (`5560112b-091f-4d31-a888-4fd5267a8376`), `execution_surface` (`antigravity`), and `runtime_metadata_model` (`Gemini 4 Argon (High)`) are reported from host-injected environment blocks (`<user_information>` and `<USER_SETTINGS_CHANGE>`). Per `ADR-0050` and [`docs/PROTOCOL_DA_PHIEN.md` §8](file:///workspace/argon-review-1003/docs/PROTOCOL_DA_PHIEN.md#L486-L526), model self-report is not independent cryptographic proof of model identity.

---

## 2. Review Scope & Two-Axis Evaluation Summary

### Files Reviewed (100% of Lines Read via `read_file`)
1. [`.claude/dev/LOCAL_GATE.md`](file:///workspace/argon-review-1003/.claude/dev/LOCAL_GATE.md#L1-L67) (67 lines)
2. [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L1-L200) (200 lines)
3. [`.claude/dev/local_gate_plan.json`](file:///workspace/argon-review-1003/.claude/dev/local_gate_plan.json#L1-L25) (25 lines)
4. [`.claude/dev/local_gate_linux_suites.json`](file:///workspace/argon-review-1003/.claude/dev/local_gate_linux_suites.json#L1-L31) (31 lines)
5. [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate_checks.py#L1-L112) (112 lines)

### Axis 1: Spec & Owner Intent Alignment
* **What aligns well**:
  * Explicitly documents and stamps `"approval": false` and `"full_ci_equivalence": false` in [`execute()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L84-L98) and [`LOCAL_GATE.md`](file:///workspace/argon-review-1003/.claude/dev/LOCAL_GATE.md#L3-L6), matching owner intent that local Linux evidence while GitHub Actions is disabled for billing is not approval, merge authority, or full multi-OS CI equivalence.
  * Rejects `--out` paths located inside `--root` via `root in (out, *out.parents)` in [`execute()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L75).
  * Requires explicit positive regex matches (`positive`) and rejects negative regex matches (`negative`) so neither exit code `0` alone nor `skipped`/`not_run` counts as pass in [`execute()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L132-L135) and [`verify()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L170-L176).
* **Where Spec/Evidence reliability breaks down**:
  * [`verify()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L153-L177) fails to verify that `"approval": false`, `"full_ci_equivalence": false`, valid `"tree"` OID, and `row["positive_matches"]` are preserved in `receipt.json`, and checks `type(r['checkout_unchanged'])` via truthiness (`if not r['checkout_unchanged']` passes on non-empty string `"false"`!) (**F01**).
  * [`identity()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L29-L43) runs `git status --porcelain --untracked-files=all` **without** `--ignored=matching` (or `--ignored=traditional`), violating [`docs/PROTOCOL_DA_PHIEN.md` §8.2](file:///workspace/argon-review-1003/docs/PROTOCOL_DA_PHIEN.md#L790-L793) and allowing steps that write to `.gitignore`d paths inside `--root` (e.g., `.claude/.packet_state`, `.codex/`, `dist/`) to be certified as `checkout_unchanged: true` (**F02**).
  * [`local_gate_linux_suites.json`](file:///workspace/argon-review-1003/.claude/dev/local_gate_linux_suites.json#L13-L17) runs `python -B .claude/dev/ci_dang_ky_test.py --chay` with a stripped environment ([`local_gate.py:100`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L100)) that drops `CI_DANG_KY_WORKERS` and `CI_DANG_KY_DOT_BIEN_MANH`, forcing single-worker serial execution of all full mutation suites (including `ops/nhanh_don_duoc_test.py`), and omits preflight tool probes required by [`docs/PROTOCOL_DA_PHIEN.md` §10.2.1](file:///workspace/argon-review-1003/docs/PROTOCOL_DA_PHIEN.md#L943-L946) (**F04**).

### Axis 2: Standards, Code Correctness & Security
* **Process & Signal Lifecycle**: [`execute()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L116-L129) only kills `proc.pid`'s immediate process group (`os.killpg(proc.pid, signal.SIGKILL)`), leaking grandchildren spawned with `start_new_session=True` by [`ci_dang_ky_test.py`](file:///workspace/argon-review-1003/.claude/dev/ci_dang_ky_test.py#L1028) when a step times out; it also lacks a `SIGTERM` handler, leaves `receipt.json` stuck at `state: "running"` on `SIGINT`/`SIGTERM`, and omits `stdin=subprocess.DEVNULL` (**F03**).
* **Test Registry & Self-Test Integration**: [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate_checks.py#L1-L112) uses the suffix `_checks.py` instead of `_test.py`, so [`ci_dang_ky_test.py`](file:///workspace/argon-review-1003/.claude/dev/ci_dang_ky_test.py#L112) (`root.rglob("*_test.py")`) never discovers or enforces registry rules on it, and neither JSON plan executes it (**F05**).
* **Atomic Receipt Durability**: [`write_receipt()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L66-L69) writes to a fixed `receipt.tmp` path without `os.fsync` or symlink checks (**F06**).

---

## 3. Bảng lớp của lượt review (Review Class Table)

Per [`docs/PROTOCOL_DA_PHIEN.md` §8.3](file:///workspace/argon-review-1003/docs/PROTOCOL_DA_PHIEN.md#L565-L579):

| Class slug | Phiên bản mẫu được kiểm | Vùng cùng lớp đã quét | Trạng thái |
| :--- | :--- | :--- | :--- |
| `verify-bo-sot-rang-buoc-bien-nhan-va-symlink` | [`verify()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L153-L177), [`load_plan()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L45-L63) | [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L45-L177), [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate_checks.py#L51-L108) | **Có lỗi (`F01` — P1)** |
| `identity-mu-tep-ignored-va-bien-git-moi-truong` | [`git()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L29-L32), [`identity()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L35-L43) | [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L29-L43), [`.claude/dev/chay-cong-windows.ps1`](file:///workspace/argon-review-1003/.claude/dev/chay-cong-windows.ps1#L140-L195) | **Có lỗi (`F02` — P1)** |
| `ro-hau-due-setsid-va-mat-bien-nhan-khi-bi-tin-hieu` | [`execute()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L114-L150), [`main()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L180-L196) | [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L106-L196), [`.claude/dev/gate_lifecycle.py`](file:///workspace/argon-review-1003/.claude/dev/gate_lifecycle.py#L388-L431), [`.claude/dev/ci_dang_ky_test.py`](file:///workspace/argon-review-1003/.claude/dev/ci_dang_ky_test.py#L1002-L1048) | **Có lỗi (`F03` — P1)** |
| `linux-suites-buoc-chay-tuan-tu-dot-bien-du-va-thieu-probe-cong-cu` | [`local_gate_linux_suites.json`](file:///workspace/argon-review-1003/.claude/dev/local_gate_linux_suites.json#L1-L31), [`execute()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L100-L104) | [`.claude/dev/local_gate_linux_suites.json`](file:///workspace/argon-review-1003/.claude/dev/local_gate_linux_suites.json#L1-L31), [`.claude/dev/local_gate_plan.json`](file:///workspace/argon-review-1003/.claude/dev/local_gate_plan.json#L1-L25), [`.claude/dev/ci_dang_ky_test.py`](file:///workspace/argon-review-1003/.claude/dev/ci_dang_ky_test.py#L830-L999) | **Có lỗi (`F04` — P2)** |
| `kiem-tra-runner-nam-ngoai-so-dang-ky-va-ke-hoach-gate` | [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate_checks.py#L1-L112) | [`.claude/dev/ci_dang_ky_test.py`](file:///workspace/argon-review-1003/.claude/dev/ci_dang_ky_test.py#L108-L165), [`.claude/dev/local_gate_plan.json`](file:///workspace/argon-review-1003/.claude/dev/local_gate_plan.json#L1-L25) | **Có lỗi (`F05` — P2)** |
| `write-receipt-khong-fsync-va-dung-ten-tam-co-dinh` | [`write_receipt()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L66-L69) | [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L66-L69), [`.claude/dev/gate_lifecycle.py`](file:///workspace/argon-review-1003/.claude/dev/gate_lifecycle.py#L91-L103) | **Có lỗi (`F06` — P3)** |

---

## 4. Detailed Actionable Findings

### Finding `F01` — `P1` | Class: `verify-bo-sot-rang-buoc-bien-nhan-va-symlink`
* **Location**: [`.claude/dev/local_gate.py#L153-L177`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L153-L177) (`verify()`) and [`.claude/dev/local_gate_checks.py#L51-L108`](file:///workspace/argon-review-1003/.claude/dev/local_gate_checks.py#L51-L108)
* **Technical Explanation**:
  [`verify()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L153-L177) is the sole cryptographic/schema gate certifying an evidence directory as `VERIFIED`. However, lines 157–176 omit several critical boundary checks:
  1. **Unchecked governance flags (`approval`, `full_ci_equivalence`)**: [`execute()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L87-L88) writes `"approval": False` and `"full_ci_equivalence": False`, and [`LOCAL_GATE.md`](file:///workspace/argon-review-1003/.claude/dev/LOCAL_GATE.md#L58) states `verify` checks receipt schema, but [`verify()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L161-L165) never inspects `r.get("approval")` or `r.get("full_ci_equivalence")`. A receipt edited to `"approval": true, "full_ci_equivalence": true` passes `verify()` with exit code `0` (`VERIFIED`).
  2. **Non-boolean truthiness on `checkout_unchanged` and `timed_out`**: Line 162 checks `and r['checkout_unchanged']` (truthiness) instead of `r.get('checkout_unchanged') is True`, and line 174 checks `and not row['timed_out']` instead of `row.get('timed_out') is False`. In Python, a string `"false"` or `"0"` in JSON (`"checkout_unchanged": "false"`) is truthy (`bool("false") is True`), bypassing the check!
  3. **Unchecked `tree`, `started_at`, and `positive_matches` fields**: `verify()` never validates that `r.get('tree')` is a valid 40/64-hex Git tree OID, that `r.get('started_at')` is a non-empty string, or that `row.get('positive_matches') == [True] * len(s['positive'])` and `row.get('negative_matches') == [False] * len(s['negative'])`.
  4. **Symlink check only on `log`, not on `out`, `receipt.json`, `plan.json`, or `runner.py`**: Line 172 checks `not log.is_symlink()`, and [`execute()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L76) rejects symlinked `out` at run time, but [`verify()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L154-L160) does not check `not out.is_symlink()` or `not (out / name).is_symlink()` for `receipt.json`, `plan.json`, or `runner.py`.

* **Reproducible Test Script (`status: not_run` — CLI command execution denied; for Executor to run in `/workspace/argon-review-evidence/scratch/repro_f01.py`)**:
  ```python
  # status: not_run (CLI command execution denied in Reviewer session)
  # Run from /workspace/argon-review-evidence/scratch:
  #   python -B /workspace/argon-review-evidence/scratch/repro_f01.py
  import json, subprocess, sys, tempfile
  from pathlib import Path

  GATE = Path("/workspace/argon-review-1003/.claude/dev/local_gate.py")

  with tempfile.TemporaryDirectory() as tmp:
      base = Path(tmp)
      repo = base / "repo"
      out = base / "out"
      plan = base / "plan.json"
      repo.mkdir()
      subprocess.run(["git", "init", str(repo)], check=True, capture_output=True)
      subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@example.com"], check=True)
      subprocess.run(["git", "-C", str(repo), "config", "user.name", "t"], check=True)
      (repo / "a.txt").write_text("ok\n", encoding="utf-8")
      subprocess.run(["git", "-C", str(repo), "add", "a.txt"], check=True)
      subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"], check=True, capture_output=True)
      head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()

      plan.write_text(json.dumps({
          "schema_version": 1,
          "steps": [{"id": "s1", "argv": [sys.executable, "-c", "print('PASS_OK')"], "timeout": 10, "positive": ["PASS_OK"]}]
      }), encoding="utf-8")

      subprocess.run([sys.executable, "-B", str(GATE), "run", "--root", str(repo), "--out", str(out), "--plan", str(plan), "--expected-head", head], check=True)

      # Tamper receipt: flip approval/full_ci_equivalence to True, set checkout_unchanged to truthy string "false", corrupt tree
      receipt_path = out / "receipt.json"
      data = json.loads(receipt_path.read_text(encoding="utf-8"))
      data["approval"] = True
      data["full_ci_equivalence"] = True
      data["checkout_unchanged"] = "false"
      data["tree"] = "not-a-tree-oid"
      data["steps"][0]["positive_matches"] = [False]
      receipt_path.write_text(json.dumps(data), encoding="utf-8")

      res = subprocess.run([sys.executable, "-B", str(GATE), "verify", "--out", str(out), "--plan", str(plan), "--expected-head", head], capture_output=True, text=True)
      print("rc=", res.returncode, "stdout=", res.stdout.strip(), "stderr=", res.stderr.strip())
      assert res.returncode != 0, "BUG REPRODUCED: verify() accepted tampered approval=True, checkout_unchanged='false', invalid tree!"
  ```

* **Four Mandatory Remediation Parts**:
  1. **Vá ở đâu**: [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L153-L177) inside [`verify()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L153-L177), and [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate_checks.py#L51-L108) inside [`LocalGateChecks`](file:///workspace/argon-review-1003/.claude/dev/local_gate_checks.py#L22-L108).
  2. **Vá thế nào**:
     * In [`verify()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L153-L177), before reading files in `out`, assert `not out.is_symlink()` and for each artifact (`receipt.json`, `plan.json`, `runner.py`), assert `p.is_file() and not p.is_symlink()`.
     * Enforce strict type and value checks on top-level receipt keys:
       * `r.get('schema_version') == 1 and type(r.get('schema_version')) is int` (note: in Python `isinstance(True, int)` is `True`, so check `type(x) is int` or `not isinstance(x, bool)` in both `load_plan()` and `verify()`)
       * `r.get('kind') == 'local_test_evidence'`
       * `r.get('approval') is False and r.get('full_ci_equivalence') is False`
       * `r.get('head') == expected`
       * `bool(re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', str(r.get('tree', ''))))`
       * `r.get('checkout_unchanged') is True`
       * `isinstance(r.get('started_at'), str) and bool(r['started_at']) and isinstance(r.get('finished_at'), str) and bool(r['finished_at'])`
     * For each step row `row` and plan step `s`, verify:
       * `row.get('state') == 'passed' and type(row.get('rc')) is int and row.get('rc') == 0 and row.get('timed_out') is False`
       * `row.get('positive_matches') == [True] * len(s['positive'])`
       * `row.get('negative_matches') == [False] * len(s['negative'])`
     * Also tighten [`load_plan()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L48-L59) so `type(data.get('schema_version')) is int` and `type(step.get('timeout')) is int` (rejecting booleans `True`/`False`, since `isinstance(True, int)` is `True` in Python).
  3. **Ca test khoá nó**: Add unit tests in [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate_checks.py) asserting `verify` exits `2` (`VERIFY_FAIL`) when: (a) `approval` or `full_ci_equivalence` is `True`; (b) `checkout_unchanged` is `"false"` or `False`; (c) `tree` is not a valid hex OID; (d) `positive_matches` or `negative_matches` in `receipt.json` is mutated; (e) `receipt.json`, `plan.json`, or `runner.py` is replaced with a symlink; (f) `timeout: true` is passed in `plan.json`.
  4. **Bản vá này có thể đẻ ra gì**: Checking `type(x) is int` is safe for JSON-decoded integers in standard library `json.loads`. Ensure `verify()` does not require `--root` (since `verify()` is designed to validate an evidence bundle using `--out`, `--plan`, and `--expected-head`), so validate `r['tree']` format (`40` or `64` lowercase hex chars) without requiring a live git query unless `--expected-tree` is optionally passed.

---

### Finding `F02` — `P1` | Class: `identity-mu-tep-ignored-va-bien-git-moi-truong`
* **Location**: [`.claude/dev/local_gate.py#L29-L43`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L29-L43) (`git()`, `identity()`) and [`.claude/dev/local_gate.py#L140-L143`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L140-L143)
* **Technical Explanation**:
  [`identity(root)`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L35-L43) is used before step execution (line 79) and after step execution (line 141) to certify that `--root` is clean and `checkout_unchanged` is `True`. It has three defects:
  1. **Blind to `.gitignore`d files (`--ignored` omitted)**: Line 40 runs `git(root, 'status', '--porcelain', '--untracked-files=all')`. Because `--ignored=matching` (or `--ignored=traditional`) is omitted, any step that creates or modifies gitignored files/directories inside `--root` (such as `.claude/.packet_state`, `.codex/`, `__pycache__/`, `.ruff_cache/`, `dist/`, `.venv/`) produces empty output from `git status --porcelain --untracked-files=all`. Thus `identity(root) == measured` evaluates to `True` (`checkout_unchanged: true`), directly violating [`docs/PROTOCOL_DA_PHIEN.md` §8.2](file:///workspace/argon-review-1003/docs/PROTOCOL_DA_PHIEN.md#L790-L793) (*"kiểm cả tracked, untracked và ignored"*).
  2. **Inherited `GIT_*` environment variables and index lock mutation**: [`git(root, *args)`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L29-L32) calls `subprocess.run(['git', '-C', str(root), *args], ...)` without stripping `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_COMMON_DIR`, `GIT_OBJECT_DIRECTORY`, or `GIT_ALTERNATE_OBJECT_DIRECTORIES` from `os.environ` (compare [`.claude/dev/chay-cong-windows.ps1#L147-L156`](file:///workspace/argon-review-1003/.claude/dev/chay-cong-windows.ps1#L147-L156), which explicitly deletes those variables) and without `--no-optional-locks`. If the caller environment has `GIT_INDEX_FILE` or `GIT_DIR` set, `identity(root)` queries a different git state than the child step (which runs under the stripped `env` at line 100). Moreover, running `git status` without `--no-optional-locks` allows `git` itself to write `.git/index.lock` / refresh `.git/index` inside the read-only checkout.
  3. **Linked worktree not rejected**: [`LOCAL_GATE.md#L8`](file:///workspace/argon-review-1003/.claude/dev/LOCAL_GATE.md#L8) states *"Use a standalone clean clone for `--root`; do not use a linked git worktree because `packet_loop_test.py` checks standalone `.git` metadata."* However, `identity(root)` only checks `git rev-parse --show-toplevel == str(root)`; it does not check `(root / '.git').is_dir() and not (root / '.git').is_symlink()` or compare `--git-dir` vs `--git-common-dir`. Running against a linked worktree proceeds into the suite and fails partway with `MA_WORKTREE` (`rc=14`).

* **Reproducible Test Script (`status: not_run` — CLI command execution denied; for Executor to run in `/workspace/argon-review-evidence/scratch/repro_f02.py`)**:
  ```python
  # status: not_run (CLI command execution denied in Reviewer session)
  # Run from /workspace/argon-review-evidence/scratch:
  #   python -B /workspace/argon-review-evidence/scratch/repro_f02.py
  import json, subprocess, sys, tempfile
  from pathlib import Path

  GATE = Path("/workspace/argon-review-1003/.claude/dev/local_gate.py")

  with tempfile.TemporaryDirectory() as tmp:
      base = Path(tmp)
      repo = base / "repo"
      out = base / "out"
      plan = base / "plan.json"
      repo.mkdir()
      subprocess.run(["git", "init", str(repo)], check=True, capture_output=True)
      subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@example.com"], check=True)
      subprocess.run(["git", "-C", str(repo), "config", "user.name", "t"], check=True)
      (repo / ".gitignore").write_text(".codex/\n", encoding="utf-8")
      subprocess.run(["git", "-C", str(repo), "add", ".gitignore"], check=True)
      subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"], check=True, capture_output=True)
      head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()

      # Step mutates checkout by writing an ignored file inside repo/.codex/polluted.txt
      plan.write_text(json.dumps({
          "schema_version": 1,
          "steps": [{
              "id": "pollute-ignored",
              "argv": [sys.executable, "-c", "from pathlib import Path; Path('.codex').mkdir(exist_ok=True); Path('.codex/polluted.txt').write_text('dirty'); print('OK')"],
              "timeout": 10,
              "positive": ["OK"]
          }]
      }), encoding="utf-8")

      res = subprocess.run([sys.executable, "-B", str(GATE), "run", "--root", str(repo), "--out", str(out), "--plan", str(plan), "--expected-head", head], capture_output=True, text=True)
      receipt = json.loads((out / "receipt.json").read_text(encoding="utf-8"))
      print("rc=", res.returncode, "checkout_unchanged=", receipt["checkout_unchanged"], "exists=", (repo / ".codex/polluted.txt").exists())
      assert res.returncode != 0 and not receipt["checkout_unchanged"], (
          "BUG REPRODUCED: step created .codex/polluted.txt inside --root but local_gate certified checkout_unchanged=True!"
      )
  ```

* **Four Mandatory Remediation Parts**:
  1. **Vá ở đâu**: [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L29-L43) in [`git()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L29-L32), [`identity()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L35-L43), and [`execute()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L79-L143).
  2. **Vá thế nào**:
     * In [`git(root, *args)`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L29-L32), pass `--no-optional-locks` to `git` (`['git', '--no-optional-locks', '-C', str(root), *args]`) and run with a sanitized environment stripping all `GIT_*` variables (`{k: v for k, v in os.environ.items() if not k.startswith('GIT_')}`).
     * In [`identity(root)`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L35-L43), require `(root / '.git').is_dir() and not (root / '.git').is_symlink()` (rejecting linked worktrees and symlinked `.git` up front with `PRECONDITION_FAIL: root must be a standalone git clone, not a linked worktree`).
     * Change the status check at line 40 to `git(root, 'status', '--porcelain=v1', '--untracked-files=all', '--ignored=matching')` so any ignored file or directory created before or during a step fails `PRECONDITION_FAIL` / `CHECKOUT_MODIFIED`.
  3. **Ca test khoá nó**: Add two tests in [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate_checks.py): (a) a step that writes a `.gitignore`d file inside `--root` must fail with `CHECKOUT_MODIFIED` (`rc=2`) and record `checkout_unchanged: False`; (b) invoking `local_gate.py` when `GIT_INDEX_FILE=/nonexistent` is set in the caller environment or against a linked worktree (`.git` file) is handled deterministically without false pass.
  4. **Bản vá này có thể đẻ ra gì**: Using `--ignored=matching` means a developer checkout that already contains `.venv/`, `.pytest_cache/`, or `.ruff_cache/` inside `--root` will be rejected at preflight with `PRECONDITION_FAIL: dirty checkout`. This matches [`LOCAL_GATE.md#L8`](file:///workspace/argon-review-1003/.claude/dev/LOCAL_GATE.md#L8) (*"Use a standalone clean clone for `--root`"*); document in `LOCAL_GATE.md` that any virtual environment or tool installation must reside outside `--root`.

---

### Finding `F03` — `P1` | Class: `ro-hau-due-setsid-va-mat-bien-nhan-khi-bi-tin-hieu`
* **Location**: [`.claude/dev/local_gate.py#L100-L150`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L100-L150) (`execute()`) and [`.claude/dev/local_gate.py#L194-L196`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L194-L196) (`main()`)
* **Technical Explanation**:
  [`execute()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L114-L150) manages long-running step subprocesses (`registry-suites` up to 9000s, `packet-loop` up to 1800s) with three process-lifecycle and evidence-integrity bugs:
  1. **Orphaned `setsid` descendants on step timeout**: Line 116 spawns `proc` with `start_new_session=True`, and lines 125–129 clean up via `os.killpg(proc.pid, signal.SIGKILL)`. However, the suites run by `local_gate_linux_suites.json`—specifically [`.claude/dev/ci_dang_ky_test.py#L1028`](file:///workspace/argon-review-1003/.claude/dev/ci_dang_ky_test.py#L1028)—themselves spawn child test processes with `start_new_session=True`! When `proc.wait(timeout=step['timeout'])` times out in `local_gate.py` (or if `ci_dang_ky_test.py` is killed by `SIGKILL` before its own `finally` handler can run), `os.killpg(proc.pid, signal.SIGKILL)` only kills `ci_dang_ky_test.py`'s immediate process group (`pgid == proc.pid`). All grandchild test processes in their own sessions survive as orphans running inside `root` while `local_gate.py` immediately calls `identity(root)`. Both [`.claude/dev/gate_lifecycle.py#L388-L431`](file:///workspace/argon-review-1003/.claude/dev/gate_lifecycle.py#L388-L431) and [`.claude/dev/ci_dang_ky_test.py#L1002-L1048`](file:///workspace/argon-review-1003/.claude/dev/ci_dang_ky_test.py#L1002-L1048) solved this in the same folder by injecting a unique token env var into the child tree and scanning `/proc/<pid>/environ` on Linux (or sending `SIGTERM` first with a grace window so the child runner's cleanup handler can reap its own `start_new_session` children, followed by `/proc` token sweep with `SIGKILL`).
  2. **Receipt left permanently in `state: "running"` on `SIGINT`/`SIGTERM`**: At lines 107–113, `execute()` writes `receipt.json` with `row['state'] = 'running'`. If `SIGINT` (`KeyboardInterrupt`) arrives during `proc.wait()`, the `finally` block (lines 124–129) kills `proc.pid`'s group and re-raises `KeyboardInterrupt` **without** updating `row['state']`, `receipt['finished_at']`, or calling `write_receipt(out, receipt)`. Even worse, no `signal.SIGTERM` or `signal.SIGHUP` handler is installed (unlike `BiKetThuc` in [`gate_lifecycle.py#L51-L64`](file:///workspace/argon-review-1003/.claude/dev/gate_lifecycle.py#L51-L64)), so `SIGTERM` kills `local_gate.py` immediately without running `finally` at all—leaving both the child process tree alive and `receipt.json` stuck at `state: "running"`.
  3. **Missing `stdin=subprocess.DEVNULL`**: Line 116 calls `subprocess.Popen(..., stdout=handle, stderr=subprocess.STDOUT, start_new_session=True)` without `stdin=subprocess.DEVNULL`, violating [`CLAUDE.md#L736-L743`](file:///workspace/argon-review-1003/CLAUDE.md#L736-L743) (preventing child processes from hanging on inherited stdin).

* **Reproducible Test Script (`status: not_run` — CLI command execution denied; for Executor to run in `/workspace/argon-review-evidence/scratch/repro_f03.py`)**:
  ```python
  # status: not_run (CLI command execution denied in Reviewer session)
  # Run from /workspace/argon-review-evidence/scratch:
  #   python -B /workspace/argon-review-evidence/scratch/repro_f03.py
  import json, os, signal, subprocess, sys, tempfile, time
  from pathlib import Path

  GATE = Path("/workspace/argon-review-1003/.claude/dev/local_gate.py")

  with tempfile.TemporaryDirectory() as tmp:
      base = Path(tmp)
      repo = base / "repo"
      out = base / "out"
      plan = base / "plan.json"
      pid_file = base / "grandchild.pid"
      repo.mkdir()
      subprocess.run(["git", "init", str(repo)], check=True, capture_output=True)
      subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@example.com"], check=True)
      subprocess.run(["git", "-C", str(repo), "config", "user.name", "t"], check=True)
      (repo / "a.txt").write_text("ok\n", encoding="utf-8")
      subprocess.run(["git", "-C", str(repo), "add", "a.txt"], check=True)
      subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"], check=True, capture_output=True)
      head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()

      # Step spawns a grandchild with start_new_session=True (just like ci_dang_ky_test.py does) and sleeps past timeout=1
      child_code = (
          "import subprocess, sys, time; "
          f"p = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'], start_new_session=True); "
          f"open({str(pid_file)!r}, 'w').write(str(p.pid)); "
          "time.sleep(30)"
      )
      plan.write_text(json.dumps({
          "schema_version": 1,
          "steps": [{"id": "timeout-grandchild", "argv": [sys.executable, "-c", child_code], "timeout": 1, "positive": ["NEVER"]}]
      }), encoding="utf-8")

      subprocess.run([sys.executable, "-B", str(GATE), "run", "--root", str(repo), "--out", str(out), "--plan", str(plan), "--expected-head", head], capture_output=True, text=True)
      gpid = int(pid_file.read_text().strip())
      alive = True
      try:
          os.kill(gpid, 0)
      except ProcessLookupError:
          alive = False
      finally:
          try:
              os.killpg(gpid, signal.SIGKILL)
          except ProcessLookupError:
              pass
      print("grandchild_pid=", gpid, "still_alive_after_local_gate_exit=", alive)
      assert not alive, "BUG REPRODUCED: start_new_session grandchild leaked alive after step timeout!"
  ```

* **Four Mandatory Remediation Parts**:
  1. **Vá ở đâu**: [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L100-L150) (`execute()`) and [`main()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L180-L196).
  2. **Vá thế nào**:
     * Pass `stdin=subprocess.DEVNULL` to `subprocess.Popen` at line 116.
     * Stamp a unique per-step token into the child `env` (e.g., `env['LOCAL_GATE_STEP_TOKEN'] = token = f"{os.getpid()}_{step['id']}_{time.monotonic_ns()}"`).
     * In the `finally` cleanup block of `execute()`, first send `SIGTERM` to `proc.pid`'s process group and wait briefly (e.g. up to `1.0s`) so intermediate runners like `ci_dang_ky_test.py` can run their own `finally` cleanup, then `os.killpg(proc.pid, signal.SIGKILL)`, and finally scan `/proc/[0-9]*/environ` (matching `_quet_proc_token` in [`.claude/dev/ci_dang_ky_test.py#L1002-L1018`](file:///workspace/argon-review-1003/.claude/dev/ci_dang_ky_test.py#L1002-L1018)) to `SIGKILL` any surviving descendant carrying `LOCAL_GATE_STEP_TOKEN=token`.
     * Install a signal handler for `SIGTERM` (and `SIGHUP` where available) during `execute()` that raises a dedicated `_Terminated` exception (or `KeyboardInterrupt`), and in `execute()`'s `except BaseException:` block ensure `row['state'] = 'aborted'`, `row['finished_at'] = now()`, `receipt['finished_at'] = now()`, and `write_receipt(out, receipt)` are written before exiting with non-zero code (`2`).
  3. **Ca test khoá nó**: Add two tests in [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate_checks.py): (a) a timed-out step that spawns a grandchild with `start_new_session=True` leaves zero surviving grandchild processes after `local_gate.py` returns; (b) sending `SIGTERM` to `local_gate.py` while a step is running kills the child process and updates `receipt.json` out of `state: "running"` with a non-null `finished_at`.
  4. **Bản vá này có thể đẻ ra gì**: Scanning `/proc` can raise `PermissionError` or `FileNotFoundError` as processes exit concurrently; wrap each `/proc/<pid>/environ` read in `try ... except OSError: continue` and never kill `os.getpid()`. Restore previous signal handlers in a `finally` block so unit tests calling `execute()` in-process do not leak global signal handlers.

---

### Finding `F04` — `P2` | Class: `linux-suites-buoc-chay-tuan-tu-dot-bien-du-va-thieu-probe-cong-cu`
* **Location**: [`.claude/dev/local_gate_linux_suites.json#L1-L31`](file:///workspace/argon-review-1003/.claude/dev/local_gate_linux_suites.json#L1-L31), [`.claude/dev/local_gate_plan.json#L1-L25`](file:///workspace/argon-review-1003/.claude/dev/local_gate_plan.json#L1-L25), and [`.claude/dev/local_gate.py#L100-L104`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L100-L104)
* **Technical Explanation**:
  1. **Forced single-worker (`N=1`) full mutation run in `local_gate_linux_suites.json`**:
     In [`local_gate.py#L100`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L100), `execute()` strips all environment variables except `PATH`, `HOME`, `LANG`, `LC_ALL`, and `TMPDIR`. When step `registry-suites` in [`local_gate_linux_suites.json#L13-L17`](file:///workspace/argon-review-1003/.claude/dev/local_gate_linux_suites.json#L13-L17) runs `["python", "-B", ".claude/dev/ci_dang_ky_test.py", "--chay"]`:
     * `CI_DANG_KY_WORKERS` is stripped, so [`ci_dang_ky_test.py#L996`](file:///workspace/argon-review-1003/.claude/dev/ci_dang_ky_test.py#L996) falls back to `N=1` (strictly serial execution).
     * `CI_DANG_KY_DOT_BIEN_MANH` and `CI_DANG_KY_SU_KIEN` are stripped, so [`ke_hoach()`](file:///workspace/argon-review-1003/.claude/dev/ci_dang_ky_test.py#L859-L870) schedules **every** suite in `MOI`—including `ops/nhanh_don_duoc_test.py`, `.claude/hooks/pretooluse_guard_test.py`, and `.claude/hooks/subagent_ghi_detect_test.py`—in `DAY_DU` (full mutation mode) on 1 worker. As documented in [`ci_dang_ky_test.py#L758-L765`](file:///workspace/argon-review-1003/.claude/dev/ci_dang_ky_test.py#L758-L765) and `#L979`, CI never runs `nhanh_don_duoc_test.py` full mutations serially inside `gate-registry` (it uses `CI_DANG_KY_WORKERS=2` and shards `ops/nhanh_don_duoc_test.py` across 8 shards in `ci-dot-bien-du.yml`) because unsharded single-worker mutation testing risks exceeding the `5400s` per-suite / `9000s` step timeout.
  2. **Missing tool preflight step despite `scope` claim**:
     [`local_gate_linux_suites.json#L4`](file:///workspace/argon-review-1003/.claude/dev/local_gate_linux_suites.json#L4) states `"Install pinned tools from repository manifest first"`, and [`docs/PROTOCOL_DA_PHIEN.md` §10.2.1](file:///workspace/argon-review-1003/docs/PROTOCOL_DA_PHIEN.md#L943-L946) requires probing `ruff --version`, `actionlint --version`, and `python ops/cong_cu.py kiem-tra --json` before heavy suites. However, `local_gate_linux_suites.json` jumps straight into `registry-preflight` and `registry-suites` without a tool preflight step, so missing pinned tools (`actionlint`, `gitleaks`, `zizmor`, `shellcheck`, `ruff`) only fail deep inside `ci_dang_ky_test.py --chay`.
  3. **Shared `TMPDIR` across steps**:
     Unlike [`ci_dang_ky_test.py#L1021`](file:///workspace/argon-review-1003/.claude/dev/ci_dang_ky_test.py#L1021) (which creates an isolated `tempfile.TemporaryDirectory(prefix="ci_dang_ky_")` per child and sets `TMPDIR`/`TEMP`/`TMP`), [`local_gate.py#L100`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L100) passes the host `TMPDIR` directly to every step without per-step isolation or cleanup, risking `/tmp/.git` ceiling-directory pollution across steps ([`CLAUDE.md#L920-L926`](file:///workspace/argon-review-1003/CLAUDE.md#L920-L926)).

* **Reproducible Test Script (`status: not_run` — CLI command execution denied; for Executor to run in `/workspace/argon-review-evidence/scratch/repro_f04.py`)**:
  ```python
  # status: not_run (CLI command execution denied in Reviewer session)
  # Run from /workspace/argon-review-evidence/scratch:
  #   CI_DANG_KY_WORKERS=4 python -B /workspace/argon-review-evidence/scratch/repro_f04.py
  import json, os, subprocess, sys, tempfile
  from pathlib import Path

  GATE = Path("/workspace/argon-review-1003/.claude/dev/local_gate.py")

  with tempfile.TemporaryDirectory() as tmp:
      base = Path(tmp)
      repo = base / "repo"
      out = base / "out"
      plan = base / "plan.json"
      repo.mkdir()
      subprocess.run(["git", "init", str(repo)], check=True, capture_output=True)
      subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@example.com"], check=True)
      subprocess.run(["git", "-C", str(repo), "config", "user.name", "t"], check=True)
      (repo / "a.txt").write_text("ok\n", encoding="utf-8")
      subprocess.run(["git", "-C", str(repo), "add", "a.txt"], check=True)
      subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"], check=True, capture_output=True)
      head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()

      plan.write_text(json.dumps({
          "schema_version": 1,
          "steps": [{
              "id": "check-env",
              "argv": [sys.executable, "-c", "import os; print('WORKERS=' + str(os.environ.get('CI_DANG_KY_WORKERS')))"],
              "timeout": 10,
              "positive": ["WORKERS=4"]
          }]
      }), encoding="utf-8")

      env = dict(os.environ, CI_DANG_KY_WORKERS="4")
      res = subprocess.run([sys.executable, "-B", str(GATE), "run", "--root", str(repo), "--out", str(out), "--plan", str(plan), "--expected-head", head], env=env, capture_output=True, text=True)
      print("rc=", res.returncode, "log=", (out / "check-env.log").read_text(encoding="utf-8").strip())
      assert res.returncode == 0, "BUG REPRODUCED: local_gate.py stripped CI_DANG_KY_WORKERS and provides no plan env support!"
  ```

* **Four Mandatory Remediation Parts**:
  1. **Vá ở đâu**: [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L45-L63) (`load_plan()`), [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L100-L120) (`execute()`), and [`.claude/dev/local_gate_linux_suites.json`](file:///workspace/argon-review-1003/.claude/dev/local_gate_linux_suites.json#L1-L31).
  2. **Vá thế nào**:
     * In [`execute()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L114-L130), create a dedicated `tempfile.TemporaryDirectory(prefix=f"local_gate_{step['id']}_")` per step and set `step_env['TMPDIR'] = step_env['TEMP'] = step_env['TMP'] = tmp_step_dir` so temporary files are isolated per step and automatically cleaned up after each step.
     * Support an optional validated `env` object in step definitions in `load_plan()` (allowing safe non-secret tuning keys such as `CI_DANG_KY_WORKERS`, or pass `CI_DANG_KY_WORKERS` from host environment when valid `1..8`), and configure `CI_DANG_KY_WORKERS: "2"` (or appropriate sharding/worker count) in `local_gate_linux_suites.json`.
     * Add an initial `tool-preflight` step in [`local_gate_linux_suites.json`](file:///workspace/argon-review-1003/.claude/dev/local_gate_linux_suites.json) running `["python", "-B", "ops/cong_cu.py", "kiem-tra", "--json"]` with positive pattern `"\"ok\":\\s*true"` (or equivalent positive marker from `ops/cong_cu.py`) so missing pinned binaries fail fast in `<5s` instead of mid-suite.
  3. **Ca test khoá nó**: Add a test in [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate_checks.py) verifying that each step gets an isolated `TMPDIR` that is cleaned up after the step completes, and that `local_gate_linux_suites.json` loads cleanly via `load_plan()`.
  4. **Bản vá này có thể đẻ ra gì**: If `step["env"]` is allowed in `load_plan()`, forbid overriding security-critical variables (`PATH`, `PYTHONHOME`, `PYTHONPATH`, `LD_PRELOAD`, `GIT_*`) inside `step["env"]` so a plan cannot hijack interpreter resolution.

---

### Finding `F05` — `P2` | Class: `kiem-tra-runner-nam-ngoai-so-dang-ky-va-ke-hoach-gate`
* **Location**: [`.claude/dev/local_gate_checks.py#L1-L112`](file:///workspace/argon-review-1003/.claude/dev/local_gate_checks.py#L1-L112), [`.claude/dev/local_gate_plan.json#L1-L25`](file:///workspace/argon-review-1003/.claude/dev/local_gate_plan.json#L1-L25), and [`.claude/dev/local_gate_linux_suites.json#L1-L31`](file:///workspace/argon-review-1003/.claude/dev/local_gate_linux_suites.json#L1-L31)
* **Technical Explanation**:
  1. **Bypassed test registry via `*_checks.py` naming**: In this repository, [`.claude/dev/ci_dang_ky_test.py#L112`](file:///workspace/argon-review-1003/.claude/dev/ci_dang_ky_test.py#L112) discovers live tests in `.claude/dev` via `root.rglob("*_test.py")` and requires every test file to be registered in `DANG_KY` (`CLAUDE.md:57-59`). Naming the test suite `.claude/dev/local_gate_checks.py` bypasses `tim()` in `ci_dang_ky_test.py`, so `ci_dang_ky_test.py --kiem-tra` and `ci_dang_ky_test.py --chay` never run it!
  2. **Omitted from both `local_gate_plan.json` and `local_gate_linux_suites.json`**: Neither [`.claude/dev/local_gate_plan.json`](file:///workspace/argon-review-1003/.claude/dev/local_gate_plan.json#L5-L23) nor [`.claude/dev/local_gate_linux_suites.json`](file:///workspace/argon-review-1003/.claude/dev/local_gate_linux_suites.json#L6-L30) includes a step executing `.claude/dev/local_gate_checks.py`. Thus, running either local gate plan produces a `VERIFIED` receipt without ever testing `local_gate.py` itself!
  3. **No `N/N` positive evidence output**: [`local_gate_checks.py#L111`](file:///workspace/argon-review-1003/.claude/dev/local_gate_checks.py#L111) calls bare `unittest.main()`. Under [`CLAUDE.md#L46-L47`](file:///workspace/argon-review-1003/CLAUDE.md#L46-L47), test files in this repository emit an explicit `N/N` positive pass summary (e.g. `PASS: K/K local_gate_checks`) so gate runners can match a deterministic positive regex alongside unittest's `Ran N tests` / `OK`.

* **Reproducible Test Script (`status: not_run` — CLI command execution denied; for Executor to run in `/workspace/argon-review-evidence/scratch/repro_f05.py`)**:
  ```python
  # status: not_run (CLI command execution denied in Reviewer session)
  # Run from /workspace/argon-review-evidence/scratch:
  #   python -B /workspace/argon-review-evidence/scratch/repro_f05.py
  import json
  from pathlib import Path

  root = Path("/workspace/argon-review-1003")
  plan1 = json.loads((root / ".claude/dev/local_gate_plan.json").read_text(encoding="utf-8"))
  plan2 = json.loads((root / ".claude/dev/local_gate_linux_suites.json").read_text(encoding="utf-8"))
  all_argvs = [ s["argv"] for p in (plan1, plan2) for s in p["steps"] ]
  mentions = [ argv for argv in all_argvs if any("local_gate_checks" in tok or "local_gate_test" in tok for tok in argv) ]
  print("steps_running_local_gate_self_tests=", mentions)
  assert mentions, "BUG REPRODUCED: neither local_gate_plan.json nor local_gate_linux_suites.json runs local_gate_checks.py!"
  ```

* **Four Mandatory Remediation Parts**:
  1. **Vá ở đâu**: [`.claude/dev/local_gate_plan.json`](file:///workspace/argon-review-1003/.claude/dev/local_gate_plan.json#L5-L23), [`.claude/dev/local_gate_linux_suites.json`](file:///workspace/argon-review-1003/.claude/dev/local_gate_linux_suites.json#L6-L30), and [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate_checks.py#L109-L112) (plus [`.claude/dev/LOCAL_GATE.md`](file:///workspace/argon-review-1003/.claude/dev/LOCAL_GATE.md#L33-L45)).
  2. **Vá thế nào**:
     * Add a `local-gate-self-check` step (`["python", "-B", ".claude/dev/local_gate_checks.py", "-v"]`) to both [`.claude/dev/local_gate_plan.json`](file:///workspace/argon-review-1003/.claude/dev/local_gate_plan.json) and [`.claude/dev/local_gate_linux_suites.json`](file:///workspace/argon-review-1003/.claude/dev/local_gate_linux_suites.json) with a deterministic positive marker (e.g. `"^LOCAL_GATE_CHECKS_PASS [1-9][0-9]*/[1-9][0-9]*$"` and `"^OK\\b"`).
     * In [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate_checks.py#L109-L112), run `unittest.TextTestRunner(verbosity=2).run(suite)` in `__main__`, check `result.wasSuccessful() and result.testsRun > 0 and not result.skipped`, and print `f"LOCAL_GATE_CHECKS_PASS {result.testsRun}/{result.testsRun}"` before `sys.exit(0)`.
     * *(Governance note on `ci_dang_ky_test.py`)*: If write scope is strictly restricted to `.claude/dev/local_gate*` and `.claude/dev/LOCAL_GATE.md`, keeping the filename `local_gate_checks.py` avoids touching `.claude/dev/ci_dang_ky_test.py`, which makes including `local-gate-self-check` explicitly inside both `local_gate_plan.json` and `local_gate_linux_suites.json` even more critical so it is never unexecuted.
  3. **Ca test khoá nó**: Add a test in [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate_checks.py) that loads both `.claude/dev/local_gate_plan.json` and `.claude/dev/local_gate_linux_suites.json` via `local_gate.load_plan()` and asserts that both plans contain a step invoking `.claude/dev/local_gate_checks.py` with non-empty `positive` patterns.
  4. **Bản vá này có thể đẻ ra gì**: When `local_gate_checks.py` is invoked as a step inside `local_gate.py run`, `local_gate_checks.py` itself spawns nested `local_gate.py` subprocesses inside `tempfile.TemporaryDirectory()`. Ensure `local_gate_checks.py` creates all temporary repos/outputs in `tempfile.TemporaryDirectory()` (outside `--root`) so the outer `identity(root)` check remains completely clean.

---

### Finding `F06` — `P3` | Class: `write-receipt-khong-fsync-va-dung-ten-tam-co-dinh`
* **Location**: [`.claude/dev/local_gate.py#L66-L69`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L66-L69) (`write_receipt()`)
* **Technical Explanation**:
  [`write_receipt(out: Path, receipt: dict)`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L66-L69) writes to a fixed path `temp = out / 'receipt.tmp'` using `temp.write_text(...)` and `temp.replace(out / 'receipt.json')`:
  * It does not reject symlinks on `temp` or `out / 'receipt.json'`.
  * It does not call `os.fsync()` on the temporary file descriptor before `os.replace()` or `fsync` on the parent directory (contrary to [`CLAUDE.md#L868-L882`](file:///workspace/argon-review-1003/CLAUDE.md#L868-L882) and `_atomic_json` in [`.claude/dev/gate_lifecycle.py#L91-L103`](file:///workspace/argon-review-1003/.claude/dev/gate_lifecycle.py#L91-L103)).

* **Reproducible Test Script (`status: not_run` — CLI command execution denied; for Executor to run in `/workspace/argon-review-evidence/scratch/repro_f06.py`)**:
  ```python
  # status: not_run (CLI command execution denied in Reviewer session)
  # Run from /workspace/argon-review-evidence/scratch:
  #   python -B /workspace/argon-review-evidence/scratch/repro_f06.py
  import ast
  from pathlib import Path

  src = Path("/workspace/argon-review-1003/.claude/dev/local_gate.py").read_text(encoding="utf-8")
  tree = ast.parse(src)
  fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "write_receipt")
  calls = [ast.unparse(c.func) for c in ast.walk(fn) if isinstance(c, ast.Call)]
  print("write_receipt calls:", calls)
  assert any("fsync" in c for c in calls), "BUG REPRODUCED: write_receipt() does not call os.fsync() before replace!"
  ```

* **Four Mandatory Remediation Parts**:
  1. **Vá ở đâu**: [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L66-L69) in [`write_receipt()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L66-L69).
  2. **Vá thế nào**: Use `tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=out, prefix='receipt.', suffix='.tmp', delete=False)` (or verify `not temp.is_symlink()`), write the JSON payload, call `f.flush()` and `os.fsync(f.fileno())`, close the file, `os.replace(temp, out / 'receipt.json')`, and remove `temp` in an `except` cleanup block if `replace` fails.
  3. **Ca test khoá nó**: Add a test in [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate_checks.py) asserting `write_receipt()` leaves no leftover `*.tmp` files in `out` and produces a valid UTF-8 `receipt.json`.
  4. **Bản vá này có thể đẻ ra gì**: If `write_receipt` fails mid-write, a `NamedTemporaryFile` with `delete=False` could leave a `.tmp` file unless wrapped in `try ... except BaseException: os.unlink(tmp_name); raise`. Adding that `try/except` prevents orphan `.tmp` files in `out`.

---

## 5. Final Verdict

* **Verdict**: **`changes_requested`**
* **Reviewed HEAD SHA**: `c0b7711850ecee2e7165564df2f84cb92afe5fa0`
* **Base SHA**: `ef34d88838bc125727670f494b15213b6c6f0c8d`
* **Orchestrator-Measured Tree SHA**: `5d0b903a6b044c665db9685600e3200f037b51e6` (unverified via `git` CLI due to CLI command denial)
* **Blocking Findings Requiring Remediation Before Approval**:
  * **`F01` (`P1`)**: Harden [`verify()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L153-L177) and [`load_plan()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L45-L63) to validate `approval is False`, `full_ci_equivalence is False`, strict boolean `checkout_unchanged is True` and `timed_out is False`, valid hex `tree`, `positive_matches`/`negative_matches`, `not isinstance(..., bool)` on integer fields, and `not is_symlink()` on `out`, `receipt.json`, `plan.json`, and `runner.py`.
  * **`F02` (`P1`)**: Harden [`git()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L29-L32) and [`identity()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L35-L43) to pass `--no-optional-locks`, strip `GIT_*` environment variables, reject linked worktrees (`.git` not a directory), and include `--ignored=matching` in `git status --porcelain`.
  * **`F03` (`P1`)**: Harden [`execute()`](file:///workspace/argon-review-1003/.claude/dev/local_gate.py#L114-L150) to set `stdin=subprocess.DEVNULL`, reap `start_new_session` grandchildren via per-step token / `/proc` sweep on timeout/termination, and handle `SIGINT`/`SIGTERM` so `receipt.json` is never left stuck in `state: "running"`.
  * **`F04` (`P2`) & `F05` (`P2`)**: Isolate per-step `TMPDIR`, configure bounded worker/tool preflight in [`local_gate_linux_suites.json`](file:///workspace/argon-review-1003/.claude/dev/local_gate_linux_suites.json), and include [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003/.claude/dev/local_gate_checks.py) with a deterministic `N/N` pass marker in both JSON plans.
