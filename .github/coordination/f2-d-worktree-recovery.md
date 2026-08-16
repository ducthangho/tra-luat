# F2-D dirty-worktree recovery ledger — wp88 r3/g3

This ledger records only the recovery authorized by
[Mission #48 revision 5](https://github.com/ducthangho/tra-luat/issues/48) and
[Packet #88 revision 3](https://github.com/ducthangho/tra-luat/issues/88).
The Executor used lease `wp88-r3-g3-codex-20260812T030134Z`, exact base
`d866eba152063427c00a8fbdc6934747fe764aad`, and the eight-path write set.
No source worktree was checked out, staged, stashed, reset, cleaned, committed,
written, or deleted.

## Source-status fence

The hash is SHA-256 of the raw bytes from
`git status --porcelain=v1 -z --untracked-files=all`. The preflight measurement
preceded the work-start heartbeat. The recovery readback was taken at
`2026-08-12T03:19:54.3938478Z`.

| Row | Entries | Preflight status hash | Recovery-readback status hash | Result |
|---:|---:|---|---|---|
| 1 | 23 | `4a2e04ddca6c15937ceeac2045714b1c551a3cc464773de68d0112f58f506592` | `4a2e04ddca6c15937ceeac2045714b1c551a3cc464773de68d0112f58f506592` | unchanged |
| 12 | 2 | `3e5ff125563f5060b52112020450203a83b4b51b52b5eac585a1a58d9e03f420` | `3e5ff125563f5060b52112020450203a83b4b51b52b5eac585a1a58d9e03f420` | unchanged |
| 46 | 1 | `8771d638ba60e83273ba5d56e0cad0328823878f539dd38143530d48b4508d5a` | `8771d638ba60e83273ba5d56e0cad0328823878f539dd38143530d48b4508d5a` | unchanged |
| 86 | 10 | `6d3f046ad064805183ab96dc1d4367cf9d547b08bc1eaeb7cad19eea3ad910dc` | `6d3f046ad064805183ab96dc1d4367cf9d547b08bc1eaeb7cad19eea3ad910dc` | unchanged |
| 90 | 2 | `a8bacdf297f1c3321d65bb102332bc1edddafc300b12514b7fc9e1abbc43b36f` | `a8bacdf297f1c3321d65bb102332bc1edddafc300b12514b7fc9e1abbc43b36f` | unchanged |

## Row 1 — recovered

- Outcome: `recovered`.
- Source worktree: `D:/Quốc hội/tra-luat`, branch
  `codex/f3-02-impact-policy`, observed HEAD
  `a55efcdfe18f8e924335e1d2d030e8fd65f6c077`.
- Nested repositories, worktrees, caches, ZIP files, and scratch fixtures:
  `preserved_external`; none was copied or deleted.
- Three targets are byte-identical to their sources. The subscription and
  orchestrator documents each had one blank line at EOF that
  `git diff --check` rejects for a new file; their targets remove only that
  blank line and retain one final LF.

| Path | Source SHA-256 / Git blob | Target SHA-256 / Git blob |
|---|---|---|
| `docs/research/2026-08-04-kiem-chung-auth-fail-close-codex-claude.md` | `9db028636b77d6e93c82ccc27ddcec12cb9e8c9d51b4f0f0691313697e1b969d` / `83a735f9d19a0acc4550f0e3e041b53b40f40c25` | same SHA-256 / `83a735f9d19a0acc4550f0e3e041b53b40f40c25` |
| `docs/research/2026-08-04-kiem-chung-phuong-an-subscription-codex-claude.md` | `37f2f46755b7a0b66cb14717c2a4db23b6ab4fb20d1277943a35650e94ddb2af` / `b14e908eb8f35f5f37395ee8a385f600a0eea891` | `90bc4509ee829157bae5612c6c470c1369a700ad9b98ef1841eefe89ca559f6f` / `871c314d3313ac3f979effaadfd50baae5a44614` |
| `docs/research/2026-08-04-lua-chon-orchestrator-da-model-codex-claude.md` | `2f23f761504b4d77f9ffb703660ab43526a227c21a126c5babca35177b8142dc` / `c917cfc05009a493684cabb33257c17a730eef57` | `0d92c0ba751e54be1357a9709ee4bff7463086290e229b1f837c99675a2a7eec` / `57b99abe9019de841fd28a5f7a5e2e96f87656f4` |
| `docs/research/2026-08-04-so-sanh-gh-aw-bernstein-agent-orchestrator-metaswarm.md` | `9c1a3bd4bf826991d8a220f1356b940bdc13fa8db0f88df7c474f1273b70062b` / `738945c7cff8fc27b2448c98f610a8a849010fd8` | same SHA-256 / `738945c7cff8fc27b2448c98f610a8a849010fd8` |
| `docs/research/2026-08-05-kiem-chung-claude-bare-va-auth-gate.md` | `d782436174b01e3dc5843a335cf6e2539107f9ef4c2c0c10a21371b8cfdc5d22` / `bbe6f61e3062bbe697b93896e8cdcec562e02cac` | same SHA-256 / `bbe6f61e3062bbe697b93896e8cdcec562e02cac` |

Positive evidence: direct execution of
`scripts/test_fragments/wp88_worktree_recovery.py` returned
`rc=0; wp88_worktree_recovery=True`; the fragment verifies all five target
SHA-256 values.

## Row 12 — deferred

- Outcome: `deferred`.
- Owner packet: [wp68 / Mission #54](https://github.com/ducthangho/tra-luat/issues/68).
  This is a durable pointer, not a dependency of wp88.
- Source worktree:
  `C:/Users/admin/.codex/visualizations/2026/08/09/019fe86a-b6f5-7d40-bd90-4a09003d8c40/mission54-wp68-g7-codex`;
  branch `codex/wp68-g7-release-nested`; HEAD
  `578724e5fd046f3bc57024c601da7c2262ad2027`.
- `scripts/tl_core/release.py`: source SHA-256
  `b2eb3f3409f2fe23e1bd309b744b7b6730ca03f8d07c5e8ff2e90ac30a0d846a`,
  Git blob `1fb925fc020069e16b33c4fb843626b87980e95f`.
- `scripts/test_fragments/wp68_release_exclude_nested_repo.py`: source
  SHA-256 `72f865dea83f47c1e259f43b5cfa457e3375a8d19aa3a3a635ad071f68e405e8`,
  Git blob `fc6158fbfb7aa0090073f415043e689027b169f4`.
- No target path exists in wp88 and neither source file was copied. Positive
  preservation evidence is the identical two-entry status hash before/after.
  Row 12 is not `recovered` or `superseded`, and remains unresolved for F2-D.

## Row 46 — superseded

- Outcome: `superseded`.
- Source worktree:
  `D:/Quốc hội/tra-luat/.claude/worktrees/wp51-g1-f1-01-fix-codex`;
  branch `codex/wp51-g1-f1-01-fix`; HEAD
  `1880346d2be3c0be9a93de7624ee108d99b6c88c`.
- Source `scripts/tl_selftest.py`: SHA-256
  `688219e1a991be80a40d741008f8445b371a60e32ea3bb31bc3b9bce1348d4c8`,
  Git blob `e7320410286e13c3f294331b699fe7746c41ef69`.
- The sole dirty behavior is the resolved-path mismatch fixture for a
  diagnosable `FRAGMENT_READ`. Exact canonical evidence is
  `d866eba152063427c00a8fbdc6934747fe764aad:scripts/tl_selftest.py`,
  blob `b73bd540ded637874d82037bae2ec9c6658f32e9`, which contains the same
  fail-loud junction/symlink behavior under
  `wp41_fragment_read_error_diagnosable`.
- Positive behavioral evidence: the wp88 fragment independently constructs a
  lexical/physical path mismatch, blocks `Path.read_text`, and observes
  `FragmentError.code == "FRAGMENT_READ"`
  (`rc=0; wp88_worktree_recovery=True`). The exact-head full selftest also
  executes `wp41_fragment_read_error_diagnosable`.

## Row 90 — superseded

- Outcome: `superseded`.
- Source worktree: `D:/Quốc hội/tra-luat-wt/wp41-f1-01-codex`; branch
  `codex/wp41-g1-f1-01`; HEAD
  `c5e8a9d42d6cf80ed14084a05056f5880941dd4c`.
- Dirty `scripts/tl_selftest.py`: SHA-256
  `652f8a0260a30db5ffa8e1f52fbd75063afb24e75b6ee6e2ab0ca0c189be7bbd`,
  Git blob `b6794c228dc4a598b4c658fbe53544943a91fde8`.
- Untracked `scripts/tl_core/test_fragments.py`: SHA-256
  `1115f1abdbbe0154e0e03aa364986bcf8cf6c663f1f13050f44366d0533c12da`,
  Git blob `49eef04bc2e7f3f588bfc7e96462398f6937273f`.
- Exact canonical evidence at `d866eba152063427c00a8fbdc6934747fe764aad`:
  `scripts/tl_selftest.py` blob
  `b73bd540ded637874d82037bae2ec9c6658f32e9` contains every initial wp41
  loader test ID plus later hardening; `scripts/tl_core/test_fragments.py`
  blob `27fbf2a8e9c86ee042c181ce446944745e45d09e` is the landed superset with
  metadata indexing, bundled-module generation/runtime, read/execution guards,
  and deterministic topology selection.
- Positive behavioral evidence: the wp88 fragment requires all 15 relevant
  canonical wp41 test IDs, loads two packet fragments in deterministic order,
  executes both, and separately exercises the row-46 read-error path
  (`rc=0; wp88_worktree_recovery=True`). The exact-head full selftest executes
  those registered wp41 cases.

## Row 86 — abandoned by owner

- Outcome: `abandoned_by_owner`.
- `content_abandon_authorized: true`
- `filesystem_delete_authorized: false`
- Source worktree:
  `D:/Quốc hội/tra-luat-wt/review-wp68-03f9919`.
- No content was copied, no filesystem entry was removed, and its ten-entry
  status hash remained unchanged.

## Land-only obligations

Pre-commit worker evidence was positive: direct wp88 fragment
`rc=0; wp88_worktree_recovery=True`; full selftest
`rc=0; 1697/1697`; EOL policy `rc=0; ok=true; violations=[]`; and
strict doc claims `rc=0; ok=true; flags=[]`. The durable Executor handoff
records the final exact-head reruns.

The Executor did not edit `scripts/tl_test_fragments_bundled.py` or
`RELEASE_MANIFEST.json`. After independent review, the Land Operator/control
plane must generate the bundled module deterministically from the reviewed
fragment and regenerate the canonical manifest on the frozen land candidate,
then run the required Windows/Ubuntu land gates on that exact candidate.
