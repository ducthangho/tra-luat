# Independent Code Review (Round 3) — PR #1003 (`local_gate*` & `LOCAL_GATE.md`)

## 1. Preflight, Identity, Review History, and Governance Limitations

```yaml
review_type: advisory_independent_code_review
review_round: 3
review_history_preserved:
  - round: 1
    reviewed_sha: c0b7711850ecee2e7165564df2f84cb92afe5fa0
    verdict: changes_requested
  - round: 2
    reviewed_sha: dc183c7ceb0c8efda6c648e4bcddb8f16ab18064
    verdict: approve # superseded after runtime-selftest exposed F07 (GIT_CONFIG_* override & ignored fixture writes)
  - round: 3
    reviewed_sha: a07b0487635118f1d66487691e70e6e837261289
    verdict: approve
repository: ducthangho/tra-luat
pr_number: 1003
reviewed_sha: a07b0487635118f1d66487691e70e6e837261289
base_sha: ef34d88838bc125727670f494b15213b6c6f0c8d
reviewed_tree: 81f18cdb34196d3c04edbea73b9156b436cea0b1 # orchestrator-measured; not independently verified via git CLI
verdict: approve
assurance_state: advisory_review # NOT cross_approved, NOT same_provider_approved, NOT governance completion
packet_id: null # No frozen Packet Spec, spec_hash, or lease exists for PR #1003
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
    - "python -B .claude/dev/local_gate_checks.py (not_run by Reviewer; 22/22 pass on a07b0487... and prior-SHA failure reproduction on dc183c7c... are executor-reported)"
    - "runtime-selftest on a07b0487635118f1d66487691e70e6e837261289 (not_run by Reviewer; still running in executor environment — NOT claimed as passed)"
    - "packet-loop suite on a07b0487635118f1d66487691e70e6e837261289 (not_run on new SHA; prior 981/981 + 1342 mutation pass on dc183c7c... is old-SHA evidence)"
```

### Mandatory Disclosures, Evidence Boundaries & Policy Alignment
1. **Static Review Only (`independently_run: false`, `tests_status: not_run`)**: CLI command execution tools remain denied in this Reviewer session; no `run_command` or permission calls were attempted. All five target files, `.git` ref files, [`scripts/deploy-package.sh`](file:///workspace/argon-review-1003-r3/scripts/deploy-package.sh#L70-L115), and [`docs/adr/0048-tran-vong-review-len-muoi.md`](file:///workspace/argon-review-1003-r3/docs/adr/0048-tran-vong-review-len-muoi.md#L1-L134) in `/workspace/argon-review-1003-r3` were inspected read-only via `read_file`.
2. **Git OID Verification Source**: [`.git/HEAD`](file:///workspace/argon-review-1003-r3/.git/HEAD#L1), [`.git/refs/heads/agent/local-gates-argon-fixes`](file:///workspace/argon-review-1003-r3/.git/refs/heads/agent/local-gates-argon-fixes#L1), [`.git/logs/HEAD`](file:///workspace/argon-review-1003-r3/.git/logs/HEAD#L1), and [`.git/packed-refs`](file:///workspace/argon-review-1003-r3/.git/packed-refs#L1-L4) were read via `read_file` and match HEAD `a07b0487635118f1d66487691e70e6e837261289` and base `ef34d88838bc125727670f494b15213b6c6f0c8d`. The tree OID `81f18cdb34196d3c04edbea73b9156b436cea0b1` and working-tree cleanliness are orchestrator-measured rather than verified via `git` CLI.
3. **Unfinished & Old-SHA Gate Evidence**:
   * Full `runtime-selftest` on `a07b0487635118f1d66487691e70e6e837261289` is still running and is **not** claimed as passed.
   * Prior `packet-loop` results (`981/981` Linux baseline with `1` Windows skip; `1342` mutation lines with `1` Windows mutation skip) were measured on old SHA `dc183c7ceb0c8efda6c648e4bcddb8f16ab18064` and do not constitute gate evidence for `a07b0487635118f1d66487691e70e6e837261289` ([`AGENTS.md` §6](file:///workspace/argon-review-1003-r3/AGENTS.md#L131-L132)).
4. **Governance & Review-Round Ceiling Policy (`ADR-0048`)**:
   * Per [`docs/adr/0048-tran-vong-review-len-muoi.md`](file:///workspace/argon-review-1003-r3/docs/adr/0048-tran-vong-review-len-muoi.md#L6-L15) and [`docs/PROTOCOL_DA_PHIEN.md` §20](file:///workspace/argon-review-1003-r3/docs/PROTOCOL_DA_PHIEN.md#L1500-L1570), the canonical review-round ceiling for post-`2026-09-12` scope is `10` rounds, superseding the older literal `2` in `ADR-0043` and transitional provider-plan documents.
   * No frozen Packet Spec, `spec_hash`, or lease exists for PR #1003. Review history is preserved without reset (Round 3), conducted under direct owner authorization as an **advisory independent code review** (`advisory_review`), not `cross_approved`, not `same_provider_approved`, and not governance admission.

---

## 2. Evaluation of Round 3 Changes (`F07` Class) and Prior `F01`–`F06`

All five changed files in `/workspace/argon-review-1003-r3` were read in full:
1. [`.claude/dev/LOCAL_GATE.md`](file:///workspace/argon-review-1003-r3/.claude/dev/LOCAL_GATE.md#L1-L100) (100 lines)
2. [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L1-L362) (362 lines)
3. [`.claude/dev/local_gate_plan.json`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate_plan.json#L1-L64) (64 lines)
4. [`.claude/dev/local_gate_linux_suites.json`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate_linux_suites.json#L1-L107) (107 lines)
5. [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate_checks.py#L1-L273) (273 lines)

### Technical Audit of `F07` Remediation (`GIT_CONFIG_*` Removal & `scratch_run` Isolation)

1. **Root Cause in Round 2 (`dc183c7ceb0c8efda6c648e4bcddb8f16ab18064`)**:
   * Round 2 [`execute()`](file:///workspace/argon-review-1003-r2/.claude/dev/local_gate.py#L196-L199) injected `GIT_CONFIG_COUNT='3'` (`core.abbrev=7`, `core.autocrlf=false`, `core.eol=lf`) into child `env`. As documented in [`scripts/deploy-package.sh#L87-L90`](file:///workspace/argon-review-1003-r3/scripts/deploy-package.sh#L87-L90), `GIT_CONFIG_*` environment variables override repo-local `.git/config` in nested child repositories, breaking `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` (`1737/1738` in `scripts/tl.py --selftest`) when that test configured a temporary repo with `core.abbrev=8`.
   * In addition, `scripts/tl.py --selftest` writes ignored fixture/state files inside its working directory, tripping the post-step `--ignored=matching` check on `--root`.

2. **Verification of Round 3 Implementation (`a07b0487635118f1d66487691e70e6e837261289`)**:
   * **No `GIT_CONFIG_*` environment inheritance**: [`execute()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L227-L229) and [`scratch_run()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L185-L187) no longer set `GIT_CONFIG_*` in `env`. Instead, [`scratch_run()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L180-L181) applies `core.abbrev=7`, `core.autocrlf=false`, and `core.eol=lf` via `git config --local` inside the disposable scratch clone, allowing nested fixture repositories created during selftest to set their own repo-local Git config. Locked by [`test_nested_git_config_can_override_abbreviation`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate_checks.py#L242-L249).
   * **Protection Against Tracked/Untracked Mutation & OID Spoofing in `scratch_run()`**:
     * **Pre-clone source verification**: [`scratch_run()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L175) calls `source = identity(root)`, verifying that the source checkout `root` has no `assume-unchanged`/`skip-worktree` entries and is clean across tracked, untracked, and ignored files.
     * **Exact OID clone & precheck**: Lines 176–183 clone `root` with `--no-hardlinks` into `TemporaryDirectory(prefix='local-gate-copy-')` (which resides under the per-step `TMPDIR=scratch` inside `out`, outside `root`), detach `HEAD` at `source['head']`, set repo-local Git config, and assert `identity(copy) == source` before running `argv`.
     * **Post-execution tracked/untracked & OID checks**: Lines 190–194 enforce four conjunctive postchecks after `subprocess.call(argv, cwd=copy, ...)`:
       1. `git(copy, 'rev-parse', 'HEAD') == source['head']` (rejects any commit/reset/checkout in the scratch clone);
       2. `git(copy, 'rev-parse', 'HEAD^{tree}') == source['tree']` (rejects any tree OID drift);
       3. `not git(copy, 'status', '--porcelain', '--untracked-files=all')` (rejects any staged, unstaged, or untracked file modification in `copy`, permitting only `.gitignore`d fixture/state writes inside `copy`);
       4. `identity(root) == source` (verifies the original checkout `root` remains completely untouched across tracked, untracked, and ignored paths, and [`execute()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L288) re-verifies `identity(root) == measured` after the supervisor exits).
     * **Positive log & receipt binding**: Only if all four postchecks succeed does [`scratch_run()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L195-L196) print `SCRATCH_CLONE_TRACKED_UNCHANGED true` and return `rc`. [`local_gate_linux_suites.json#L87-L105`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate_linux_suites.json#L87-L105) requires `execution_scope: "scratch_clone"` and positive matches on `^== tl selftest ([1-9][0-9]*)/\1 ==$`, `^SCRATCH_CLONE_HEAD [0-9a-f]{40,64} TREE [0-9a-f]{40,64}$`, and `^SCRATCH_CLONE_TRACKED_UNCHANGED true$`. [`read_plan()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L65-L66) and [`verify()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L325) validate `execution_scope` against the trusted plan.
     * **Subreaper containment**: Because `_scratch_run` executes inside `supervise()` (`PR_SET_CHILD_SUBREAPER`), any timeout or `SIGINT`/`SIGTERM`/`SIGHUP` reaps both `_scratch_run` and all `tl.py --selftest` descendants until kernel `ECHILD`, while the outer `TemporaryDirectory` in [`execute()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L244) removes the scratch clone directory.

---

## 3. Bảng lớp của lượt review (Round 3 Review Class Table)

| Class slug | Phiên bản mẫu được kiểm | Vùng cùng lớp đã quét | Trạng thái |
| :--- | :--- | :--- | :--- |
| `verify-bo-sot-rang-buoc-bien-nhan-va-symlink` (`F01`) | [`verify()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L300-L335), [`read_plan()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L50-L73) | [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L50-L73), [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate_checks.py#L113-L145) | **Sạch (Giữ nguyên từ R2 + kiểm `execution_scope`)** |
| `identity-mu-tep-ignored-va-bien-git-moi-truong` (`F02`) | [`git()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L31-L34), [`identity()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L37-L47) | [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L31-L47), [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate_checks.py#L147-L161) | **Sạch (Giữ nguyên từ R2)** |
| `ro-hau-due-setsid-va-mat-bien-nhan-khi-bi-tin-hieu` (`F03`) | [`supervise()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L102-L166), [`execute()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L199-L297) | [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L94-L297), [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate_checks.py#L163-L212) | **Sạch (Giữ nguyên từ R2)** |
| `linux-suites-buoc-chay-tuan-tu-dot-bien-du-va-thieu-probe-cong-cu` (`F04`) | [`local_gate_linux_suites.json`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate_linux_suites.json#L1-L107) | [`.claude/dev/local_gate_linux_suites.json`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate_linux_suites.json#L1-L107), [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate_checks.py#L213-L225) | **Sạch (Giữ nguyên từ R2)** |
| `kiem-tra-runner-nam-ngoai-so-dang-ky-va-ke-hoach-gate` (`F05`) | [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate_checks.py#L236-L240) | [`.claude/dev/local_gate_plan.json`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate_plan.json#L1-L64), [`.claude/dev/local_gate_linux_suites.json`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate_linux_suites.json#L1-L107) | **Sạch (Giữ nguyên từ R2)** |
| `write-receipt-khong-fsync-va-dung-ten-tam-co-dinh` (`F06`) | [`write_receipt()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L76-L92) | [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L76-L92), [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate_checks.py#L226-L234) | **Sạch (Giữ nguyên từ R2)** |
| `git-config-env-de-fixture-con-va-selftest-ghi-ignored` (`F07`) | [`scratch_run()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L169-L196), [`execute()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L227-L236) | [`.claude/dev/local_gate.py`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L169-L362), [`.claude/dev/local_gate_linux_suites.json`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate_linux_suites.json#L87-L105), [`.claude/dev/local_gate_checks.py`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate_checks.py#L242-L266), [`.claude/dev/LOCAL_GATE.md`](file:///workspace/argon-review-1003-r3/.claude/dev/LOCAL_GATE.md#L37-L45) | **Sạch (Đã đóng `F07`)** |

---

## 4. Remaining Actionable Findings

**None (`0` findings).** All prior findings (`F01`–`F06`) remain resolved and the Round 3 remediation for `F07` ([`scratch_run()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L169-L196), removal of `GIT_CONFIG_*` environment overrides in [`execute()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L227-L229), `execution_scope` verification in [`verify()`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate.py#L325), and regression tests in [`local_gate_checks.py#L242-L266`](file:///workspace/argon-review-1003-r3/.claude/dev/local_gate_checks.py#L242-L266)) is sound and properly protects both the source checkout and tracked/untracked integrity of the scratch clone.

---

## 5. Final Verdict

* **Verdict**: **`approve`** (advisory independent code review; `assurance_state: advisory_review`, **not** `cross_approved` or `same_provider_approved`)
* **Reviewed HEAD SHA**: `a07b0487635118f1d66487691e70e6e837261289`
* **Base SHA**: `ef34d88838bc125727670f494b15213b6c6f0c8d`
* **Orchestrator-Measured Tree SHA**: `81f18cdb34196d3c04edbea73b9156b436cea0b1`
* **Limitations**:
  1. Static code review only (`independently_run: false`, all tests `not_run` by Reviewer due to CLI command tool denial).
  2. Full `runtime-selftest` and `local_gate_linux_suites.json` execution on `a07b0487635118f1d66487691e70e6e837261289` were still in progress at review time and must complete with `verify` exit code `0` on exact SHA `a07b0487635118f1d66487691e70e6e837261289` before operational reliance on the new-head suite receipt.
  3. No frozen Packet Spec, `spec_hash`, or lease exists for PR #1003; governance admission, Windows gate execution, and merge/land authority remain separate owner decisions.
