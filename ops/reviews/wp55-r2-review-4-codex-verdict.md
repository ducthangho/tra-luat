# PR #92 review — REQUEST_CHANGES

Reviewed SHA: `cf39109c9e5167516c53f2071e5fa7ec5c6afff5`

Assurance: `cross_approved` target, independent Codex reviewer. Verdict: **REQUEST_CHANGES**.

## Findings

### `lease-authority-spoof` — P1 / blocking

`record-lease` does not enforce that an authorized actor granted the lease; it only rejects the two exact strings `claude` and `codex`. The same caller can choose another label and arbitrary non-empty evidence, reach `leased`, then open an attempt. This moves the original self-grant hole from `init` to `record-lease`.

Executable evidence on the reviewed SHA:

```text
init --packet 9002 ...                                      rc=0
record-lease --granted-by codex-dispatcher --evidence x \
  --expires-utc 2099-01-01T00:00:00Z                       rc=0
begin-attempt --packet 9002 --provider claude               rc=0
```

Additional boundary probes: `cödex`, `co\u0308dex`, `codex-dispatcher`, and `ai-codex-bot` all returned `rc=0`; a real person named exactly `Claude` is rejected (`rc=7`), while arbitrary evidence `x` and an empty `--lease-id` are accepted. The check at `.claude/dev/packet_loop.py:399-423` therefore distinguishes spelling, not authority. Either bind the transition to independently verifiable authority evidence, or explicitly model it as a manual ledger and stop claiming it prevents agent self-grant.

### `legacy-lease-bypass` — P1 / blocking

`begin-attempt` fail-opens when `lease` is missing: expiration is checked only under `if lease and lease.get("expires_utc")`. A state created by the immediately preceding reviewed head (`22d2cc9`) contains `state: leased` but no `lease`, and the new code accepts it without ever passing through `record-lease`.

Executable evidence:

```text
python <(git show 22d2cc9:.claude/dev/packet_loop.py) ... init --packet 9001 ...
  rc=0, state=leased, no lease field
python .claude/dev/packet_loop.py ... begin-attempt --packet 9001 --provider claude
  rc=0, state=running
```

This directly contradicts the adapter claim that `leased` is reachable only through `record-lease`. The guard at `.claude/dev/packet_loop.py:437-450` must reject missing/malformed lease data (or perform an explicit, authorized migration), and the suite needs an old-state upgrade fixture.

### `doctrine-rendering-bypass` — P1 / blocking

`doctrine-scan` still compares a partially normalized source string, so an adapter can render the exact forbidden doctrine while the scanner returns clean. The normalization at `.claude/dev/packet_loop.py:183-194` handles Markdown decoration and whitespace, but not format characters or HTML entities.

Executable evidence:

```text
"merged: PR đã vào nhánh đích"                 rc=6
"mer<U+200B>ged: PR đã vào nhánh đích"         rc=0
"merged&#58; PR đã vào nhánh đích"              rc=0
NBSP-only spacing variant                         rc=6
backtick-decoration variant                       rc=6
```

The first two bypass forms render as the forbidden phrase in Markdown, so acceptance criterion 2's mechanical prohibition is not met. Normalize rendered-equivalent forms (with safe entity handling and Unicode format-character policy) and add both mutations as negative fixtures.

## Gate evidence

- `packet_loop_test.py`: `48/48`; all 7 declared mutation targets killed.
- `doctrine-scan --root .`: `rc=0`, 4 files; merged `CLAUDE.md` against current master also `rc=0`.
- `tl.py --selftest`: initial `1694/1696` because the environment's global commit-signing hook cannot call its localhost MCP inside sandbox; with per-process `commit.gpgsign=false`, `1696/1696`, `rc=0`. No git config was modified.
- `doc-claims-check --strict --json`: `ok=true`, 82 files, `flags=0`.
- `release-verify --strict --json`: `ok=true`, expected `179`, checked `179`, failed `0`, extra `0`.
- `golden-test`: `rc=0`; EOL policy: `rc=0`, violations `0`.
- Deterministic release bundles: current x2 and base all SHA-256 `20c89545566b7682b3ecd2ac2ac0283add5af8a4d6ca377d9acbcde4487f8590`.
- Scope: exactly the 6 declared paths; `git diff --check` `rc=0`; worktree clean. `packet_loop` remains intentionally absent from CI (`rg` `rc=1`).
- Current master during merge check: `438fc3494a2907cfd49889af4a0eef472dc3d56f`, 62 commits ahead of base; among the six paths it changes only `CLAUDE.md`. Read-only merge-tree and `merge-file` returned `rc=0`.

## Delivery status

GitHub MCP reads succeeded, but both attempts to create the mandatory #55 heartbeat returned `user cancelled MCP tool call`; no heartbeat, PR review, or issue evidence was created. The default state path `.claude/.packet_state` has no packet 55 state (`status --packet 55` rc=8); the required `record-review` command was attempted with all three finding IDs and also returned rc=8. No unauthorized `init` was performed.

---

# Issue #55 reviewer evidence (post after the PR review exists)

```yaml
schema_version: 1
packet_id: wp55
generation: 2
provider: codex
role: reviewer
session_id: wp55-r2-review-4-codex-20260814
reviewed_sha: cf39109c9e5167516c53f2071e5fa7ec5c6afff5
independent_from_executor_session: true
review_axes: [spec, standards_security]
tests:
  - packet_loop_test: {result: 48/48, rc: 0, mutations_killed: 7/7}
  - selftest: {result: 1696/1696, rc: 0, environment_override: commit.gpgsign=false}
  - doctrine_scan_branch: {files: 4, findings: 0, rc: 0}
  - doctrine_scan_merged_claude_md: {files: 1, findings: 0, rc: 0}
  - doc_claims_check: {ok: true, files: 82, flags: 0, rc: 0}
  - release_verify: {ok: true, expected: 179, checked: 179, failed: 0, extra: 0, rc: 0}
  - golden_test: {rc: 0}
  - eol_policy: {violations: 0, rc: 0}
  - release_bundle_sha256: 20c89545566b7682b3ecd2ac2ac0283add5af8a4d6ca377d9acbcde4487f8590
findings:
  - {finding_id: lease-authority-spoof, severity: P1, disposition: blocking}
  - {finding_id: legacy-lease-bypass, severity: P1, disposition: blocking}
  - {finding_id: doctrine-rendering-bypass, severity: P1, disposition: blocking}
verdict: changes_requested
assurance: cross_approved
evidence_url: pending-owner-post
```

Manual next action: submit the first section as a `REQUEST_CHANGES` review on PR #92 anchored to `cf39109c…`, then post this evidence on #55 and replace `evidence_url` with the created PR-review URL.
