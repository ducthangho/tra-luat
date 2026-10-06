# WP710 — NLM credential refresh, Packet Spec revision 4 (proposal)

## Identity and authority

- Packet Issue: https://github.com/ducthangho/tra-luat/issues/710; mission Issue: 710.
- Revision 4, proposed generation 2, proposed Executor `codex` / `openai_codex` / `codex_cli` on local Windows/PowerShell; proposed branch `agent/wp710-g2-codex`. This revision supersedes r3/g1 for new execution only after a separate owner GitHub grant and lease. Existing r3/g1 candidate remains historical evidence, not r4 authority.
- Canonical base `refs/heads/master` at exact SHA `8c98afacb9285aa71e5200739236284f7a190d4f`, tree `93a49ac374a8e182821e10861033f9eac2a0fd6f`. Recheck remote before lease. r3/g1 candidate head `c1266494a36af5723bc11df0d5097e6d1a871116`, tree `7331b18f3fbdb3131d888f08983af1449b1a7364`, is the proposed starting point for g2; no old admission/review/gate result transfers to a new head.
- Risk and Review Class: **sensitive**; effective Review Class proposed **sensitive**. Require a fresh independent cross-provider reviewer with valid model/session evidence, or human audit, on exact new head. A self-review or invalid automated verdict does not suffice.
- r3 owner grant: https://github.com/ducthangho/tra-luat/issues/710#issuecomment-6000071313 ; r3 WSL validation grant: https://github.com/ducthangho/tra-luat/issues/710#issuecomment-6010599805 . Neither grants r4/g2. r3/g1 lease: `ops/leases/wp710-r3-g1-codex.yaml`, expires 2026-10-06T17:58:41Z.

## Objective and write set

Refresh NotebookLM credentials with `nlm auth refresh` only on the host carrying the original browser profile; require a positive real notebook canary before any Drive credential stage. Auth failure, network failure, timeout and inconclusive results must not stage. Add a Windows keepalive that is off by default, explicitly enabled, bounded, stoppable and serialized across processes. Update RUNBOOK and behavioral tests. Preserve untracked `scripts/nlm-auth.ps1` untouched and unstaged.

The proposed product write set is the same six exact paths as r3/g1, with a **narrow additional permitted change inside `scripts/tl_selftest.py`**. No directory prefix or glob:

| Path | Permitted change |
|---|---|
| `scripts/nlm-credential-refresh.ps1` | Host refresh/canary/stage wrapper and opt-in serialized keepalive. |
| `scripts/nlm-credential-refresh.Tests.ps1` | Hermetic PowerShell behavior and concurrent-process tests. |
| `scripts/tl_gws.py` | `nlm-auth-stage` must upload only after live canary is positively `True`, including `--force`. |
| `scripts/tl_selftest.py` | Command-level NLM stage upload-count regression; additionally, change only `r209_cay_that_va_phan_chung` so its eight existing assertions read the worker candidate's temporary release manifest from the existing `_build_release_manifest(root)` helper rather than the committed land-only `RELEASE_MANIFEST.json`. Preserve all eight assertions and the negative pointer probe. |
| `references/RUNBOOK.md` | Host prerequisites, real canary evidence, outcome meanings, keepalive controls and recovery. |
| `changelog.d/wp-710.md` | Packet changelog fragment, no version bump. |

`RELEASE_MANIFEST.json`, VERSION, golden and workflow files remain land-only/out of the Executor write set. Do not obscure the RUNBOOK path to silence the pointer guard. Existing shell wrappers call `tl nlm-auth-stage`; its own guard must protect them without editing their files.

## Why revision and generation change

PR https://github.com/ducthangho/tra-luat/pull/711 at r3/g1 head failed `gate (ubuntu-latest)` on `r209_cay_that_va_phan_chung`: 1714/1715 full selftests passed. The candidate RUNBOOK points to `scripts/nlm-credential-refresh.ps1`, absent from the **committed** release manifest. Read-only A/B measurement isolated that single pointer failure to the RUNBOOK addition. The worker candidate's temporary manifest contains 183 files, including the new script and RUNBOOK; with that manifest all eight r209 assertions pass, pointer failures zero, advisory 107 and baseline 3. Protocol §10.2.4 makes the worker manifest temporary and the canonical manifest land-only. The new r209 test behavior extends the r3 acceptance for `scripts/tl_selftest.py`; protocol §5 requires a new revision, generation and lease even though the path set stays six files.

## Effective write set and pre-lease checks

At the measured base, `.github/coordination/change-impact.v1.json` and schema were absent. The r3 owner granted a **bounded manual six-path exception** under policy debt #473; no computed closure was claimed. For r4/g2, the owner must expressly renew that bounded exception for these same six paths and the r209 test scope. Dispatcher must recheck exact base, Spec bytes/SHA-256, current branch refs and live-lease overlaps before a g2 lease; record effective paths/hash, required checks and land obligations as measurable or `not_measured`. No overlap or missing authority may be inferred from old receipts.

## Acceptance and evidence

1. `nlm auth refresh` runs on the original browser-profile host with bounded timeout; record CLI version, real rc, elapsed time and non-secret profile fingerprint. Nonzero, timeout or missing profile makes zero stage calls.
2. A specified real notebook is read through `nlm notebook get` or existing `_nlm_auth_alive`; trusted local notebook ID must match the response. CLI rc 0, `nlm login --check` or notebook count alone is insufficient. Wrong ID, absent body, parser failure, auth/network error and timeout yield zero stage calls.
3. Actual `tl nlm-auth-stage` uploads exactly once after positive `True`, zero after `False`, `None`, auth/network error or timeout, including `--force`. A `None`-allows-upload mutant must turn the test red.
4. Windows wrapper enforces `refresh -> canary -> stage` under one inter-process lock. Hermetic fake CLI proves order and upload counts, stage failure reporting and secret-sentinel suppression.
5. Machine-readable `auth_failure`, `network_failure`, `timeout`, `inconclusive` and `stage_failure` statuses remain distinct; the first four make zero stage calls.
6. Keepalive schedules nothing by default; explicit opt-in is bounded/stoppable. Two native Windows processes never overlap operations; abandoned-owner takeover proves owner death first. No Scheduled Task installation or auto-start.
7. `r209_cay_that_va_phan_chung` uses the candidate temporary manifest and keeps all eight assertions plus negative probe effective. Exact candidate probe must show 183 or current measured file count, new script included and zero pointer failures. Mutating the RUNBOOK pointer to a nonexistent path must fail the guard. Committed `RELEASE_MANIFEST.json` remains unchanged by Executor.
8. Record native Windows targeted tests, Python targeted tests, full repository gates, admission and independent sensitive review separately with exact head/tree, command, rc and positive evidence. Distinguish `passed`, `failed`, `skipped`, `not_run`, `not_measured`. On head change, repeat admission/review/gates as required. LIVE refresh and Drive stage are owner-controlled operations outside this Executor lease; no mock counts as LIVE evidence.

## Limits and handoff

- No dispatcher or Executor LIVE refresh, Drive stage, credential read/write, deployment, self-review, approval, merge or land. No worker/test job receives LIVE credentials.
- The new lease should permit only code/tests/docs and PR on r4/g2, with local WSL Ubuntu-Clean restricted to offline admission/checks using checker bytes at canonical base and scratch outside the product checkout. It does not turn WSL into a credential host.
- Before executing g2, reverify capability, current base/Spec hash, no overlapping live lease and branch ownership. Preserve dirty canonical checkout and the untracked `scripts/nlm-auth.ps1`.
- Executor handoff must identify exact full head SHA/tree, six changed paths, commands/rc/positive evidence, provider/surface/transport, limits and all unmeasured items. A reviewer must use fresh independent context and read-only source; a review that claims unrun tests or writes the checkout is invalid.
