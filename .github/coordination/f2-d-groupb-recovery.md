# F2-D-B — Group B recovery record (wp82)

## Authority and fence

This record executes Packet `wp82` revision 4 / generation 3 under Mission #48 revision 5.

- Initial lease: `wp82-r4-g3-codex-20260811T172240Z`
- Rework lease: `wp82-r4-g3-codex-20260811T193620Z` (findings `WP82-R4-G3-F01` and `WP82-R4-G3-F02`)
- Executor/environment: `codex` / `local`
- Packet branch: `codex/wp82-g3-f2-d-b`
- EOL base: `fbe5ab9e1ece3b45c065879bfd59dee2554db3e2`
- Mission plan hash: `856a817c15e7bded2357b9f8df13bf65e828254d3c4d26858348f9b6a852cc0c`
- Packet spec hash: `bf832c17f6385af527c9649aaa0f132dc7a314b67791fc4c624b533fd840375b`
- Owner evidence: [Issue #63 comment 5242722857](https://github.com/ducthangho/tra-luat/issues/63#issuecomment-5242722857) assigns the four Group B refs to `ducthangho` and directs that they be kept for recovery.
- Work-start evidence: [Issue #82 comment 5256598820](https://github.com/ducthangho/tra-luat/issues/82#issuecomment-5256598820).
- Reviewer findings: [Issue #82 comment 5257440302](https://github.com/ducthangho/tra-luat/issues/82#issuecomment-5257440302).
- Rework authority: [Issue #82 comment 5257928421](https://github.com/ducthangho/tra-luat/issues/82#issuecomment-5257928421), starting from packet head `87fac15375bf2cdc579125443deafe18347a7740` and ref-3 tip `1924038aaebdd1a099baa0e696524b887b93d68e`.

Fail-closed preflight was completed before any ref write:

| Check | Direct result |
|---|---|
| `git rev-parse --is-shallow-repository` | rc=0, `false` |
| Mission raw readback and plan-hash recomputation | rc=0, exact revision 5 / `856a817c...cc0c` |
| Packet raw readback and spec-hash recomputation | rc=0, exact revision 4 / generation 3 / `bf832c17...375b` |
| `origin/master` and `git ls-remote origin refs/heads/master` | rc=0, both exact EOL base `fbe5ab9...3e2` |
| Target artifact on the EOL base | `git cat-file -e` rc=128 (absent) |
| Remote `codex/wp82*` before work-start | rc=0, count=0 |
| Each old Group B tip as ancestor of the EOL base | rc=1 for all four (all required recovery) |

## Recovery method and result

Each source ref was initially recovered in place with a normal two-parent merge commit created from the
exact old tip using `git -c merge.renormalize=true merge --no-ff <EOL-base>`. Before every push, the remote
tip was raw-read and required to equal the expected old tip. Every push was explicit and non-force:
`git push origin HEAD:refs/heads/<same-source-ref>`.

Reviewer finding `WP82-R4-G3-F01` showed that the initial ref-3 merge had dropped one live `_STUB_MAP`
wiring line. Under the rework lease, ref 3 alone was advanced by the minimal single-parent corrective
commit `eaa753bd331070ee36583e57f5fe2140861486ee` from exact tip
`1924038aaebdd1a099baa0e696524b887b93d68e`. The remote tip was raw-read immediately before the write,
the update was a normal fast-forward (`1924038a -> eaa753bd`), and no other Group B ref moved.

The two required ancestry directions were then measured on the raw remote tip:

1. `git merge-base --is-ancestor <old-tip> <remote-recovered-tip>` — the legacy content is retained.
2. `git merge-base --is-ancestor <EOL-base> <remote-recovered-tip>` — the recovered ref contains the EOL base.

| # | Exact source ref | Old tip | Outcome | Remote recovered tip | Merge rc | Push rc | old -> recovered rc | EOL base -> recovered rc |
|---:|---|---|---|---|---:|---:|---:|---:|
| 1 | `claude/audit-errors-patch-plan-56x4rq` | `4c0332f052521a118da29607d7741da16033a846` | **recovered** | `f3d8d68503b5d0a9ed19eed955698ff201daa964` | 0 | 0 | 0 | 0 |
| 2 | `claude/cuu-viec-treo-2026-08-03` | `6c148d331e5dcdcc32f3b9474e806e6dcad76ac8` | **recovered** | `42d8459b92b10d450e3d7b4e27796dabf30d778c` | 1, conflicts resolved | 0 | 0 | 0 |
| 3 | `claude/nlm-registry-sheet-dup-s22fk7` | `0bb60d215c029377ac08ffb30024f18f301df68f` | **recovered + corrected** | `eaa753bd331070ee36583e57f5fe2140861486ee` | 1, conflicts resolved; corrective FF rc=0 | 0 | 0 | 0 |
| 4 | `claude/ras-17-data-pr13-windows-bjovq2` | `411b3f3fb74945934a82c8dc203cd523e0d31cf0` | **recovered** | `f1d6558aa103e13bcc57b6caf697f4f3515df16d` | 1, conflicts resolved | 0 | 0 | 0 |

All four remote readbacks exactly matched the recovered tips in the table. No source branch was deleted;
no force push, `--no-verify`, master write, LIVE call, writer opening, or ref outside these four source refs
and the packet branch was used.

### 1. Audit plan ref

The renormalized merge completed without conflict. The branch-only document is preserved byte-for-byte:

- `docs/AUDIT_XAC_MINH_VA_KE_HOACH_VA_2026-07-31.md`
- old blob = recovered blob = `71303942648f9628434001054695daa3cfc0ac4c`
- the same path on the EOL base is absent (`git cat-file -e` rc=128)

### 2. Suspended-work ref

The renormalized merge surfaced real conflicts. The evolved canonical protocol, implementation plan, and
ADR-0031 text were selected from the EOL parent; both non-overlapping selftest blocks were retained in
`scripts/tl_selftest.py`. Conflict markers were absent, AST parsing passed, `git diff --check <EOL-base>`
returned rc=0, and the EOL survey returned rc=0.

Two-way content evidence is not based on added-file counting: the operational change in
`scripts/tl_core/lookup_ops.py` remains byte-identical between the old and recovered tips while differing
from the EOL base:

- old blob: `b4d52c93ef2938475f94fa1f9fc4dcfe6b229925`
- recovered blob: `b4d52c93ef2938475f94fa1f9fc4dcfe6b229925`
- EOL-base blob: `de4956aa6471a185cbe8e91f34b4cab9dd2cdb3a`

The recovered source ref's full selftest returned rc=1 with `1703/1705` passing. The two reported failures
were `r209_cay_that_va_phan_chung` and `wp44_release_bundle_topology_under_200`; this branch-local unfinished
state is recorded rather than hidden and is not substituted for the required packet-head gate below.

### 3. NLM registry ref

Conflicts in `CHANGELOG.md`, `RELEASE_MANIFEST.json`, `SKILL.md`, `VERSION`, and `scripts/tl.py` were
initially resolved from the EOL-base side, avoiding a stale release/version rewrite. The golden inventory
path was not a conflict: `references/golden/tool_inventory_inventory_decision.json` had the same blob
`e1e00bbc42cc86fff4b2ae82fbbd45f1c2927bd2` at merge-base and old tip, so its canonical blob
`84528c51decca5735650591e06464120e08a1365` was a clean take (`WP82-R4-G3-F02`).

The initial whole-file take of `scripts/tl.py` also removed the old-tip `_STUB_MAP` exports
`'_reg_rows_split_by_drive_id', '_reg_row_for_drive_id'`. Rework commit `eaa753bd` restores exactly that
one line beside `_expect_precondition_verdict`; its diff from `1924038a` is exactly one path and one
insertion. The `VERSION` blob remains byte-identical to the EOL base at
`8331824f0abcb019eba69092d8b525753cd84230`; the old 1.36.18 -> 1.36.19 bump was not carried.

Behavior was measured on the corrected ref-3 content, not inferred from syntax or string presence:

| Behavioral check | Direct result | Positive evidence |
|---|---|---|
| Full source-ref selftest on tree `04b30d451a95bc02bd5ad78e910984233e040cdd` (the exact tree committed as `eaa753bd`) | rc=0 | `1704/1704` |
| Exact `eaa753bd` sidecar fixture through the exported helpers | rc=0 | exact=`PDF_SRC`, sidecar=`GDOC_CANON`, selected=`PDF_SRC` |
| Exact `eaa753bd` `_verified_reg_upsert` fixture with `reg_get` returning the sidecar first | rc=0 | `verified=true`, no dropped/retried/post-retried fields, exactly 1 `reg_upsert` and 1 `reg_get` |

The raw remote corrected tip contains the legacy old tip, the initial recovered tip, and the EOL base in
all required directions: `0bb60d2 -> eaa753bd`, `1924038a -> eaa753bd`, and `fbe5ab9e -> eaa753bd`
each returned direct rc=0. This closes `WP82-R4-G3-F01` with behavioral and ancestry evidence.

The two branch-only documents are preserved byte-for-byte and remain absent on the EOL base (rc=128):

| Path | Old and recovered blob |
|---|---|
| `rasoat/KETQUA_R281_V1_V2_V3_2026-07-31.md` | `bd0833811f482134b5579697cf891424dbf674e5` |
| `rasoat/PROMPT_TIEP_2026-07-31e.md` | `32a21c90d241c934f678761a185da19c65471c80` |

### 4. RAS-17 data ref

Conflicts in release metadata, golden inventory, and `scripts/tl.py` were initially resolved to canonical;
the r320 migration path and r321 scan path were both retained in `references/RASOAT_PLAN_SCHEMA.md`,
`scripts/tl_core/lookup_ops.py`, and `scripts/tl_selftest.py`. A pre-push behavioral run then correctly
caught that the r320 handler bridge was missing from canonical `scripts/tl.py` (rc=1,
`AttributeError: cmd_rasoat_anchor`). Nothing had been pushed. The old handler exports were added beside
the r321 export, syntax/EOL/diff checks were rerun, and the unpushed merge commit was amended to the final
tip in the table.

The required behavior was remeasured with the same external fixtures and an empty HOME:

| Tree / fixture | Direct result | Positive evidence |
|---|---|---|
| recovered tip / positive | rc=0 | `che_do=DRY`, `da_ghi=false`, `ke_hoach.di_tru=1`, `locator_trong_hash: 1 -> 0`, `findings_sau.san_sang=true` |
| recovered tip / negative control | rc=0 | `ke_hoach.di_tru=0`, `ke_hoach.bo_qua=1`, `THIEU_DIEU_TRONG_CACHE:99`, `findings_sau.san_sang=false` |
| EOL base / same positive | rc=2 | parser reports `invalid choice: 'rasoat-anchor'` |

This demonstrates the recovered behavior and the data-sensitive control; it is not a string-presence or
one-way added-file inference.

## Protected-path and ref-scope proof

On the packet tree, the protected baseline contains exactly 31 blobs:

| Protected group | EOL-base blob count | Changed blob count in packet diff |
|---|---:|---:|
| `.githooks/**` | 5 | 0 |
| `.github/workflows/**` | 1 | 0 |
| `VERSION`, `CHANGELOG.md`, `RELEASE_MANIFEST.json` | 3 | 0 |
| `references/golden/**` | 22 | 0 |
| **Total** | **31** | **0** |

The packet diff contains exactly one path: `.github/coordination/f2-d-groupb-recovery.md`. The 69 ancestor
branches, worktrees, wp84/MCR-54-03, Drive/NLM/registry/secrets, and all other refs were not touched.

## Packet-head gates

The following commands are run on the packet head with direct return codes and positive counters before
handoff:

| Gate | Direct result | Positive evidence |
|---|---|---|
| `python .githooks/eol_policy_test.py` | rc=0 | `30/30 dat` |
| `python .githooks/eol_policy.py --all --json` | rc=0 | `ok=true`, checked=278, scanned=300, skipped=22, violations=0 |
| `python scripts/tl.py --selftest` | rc=0 | `1696/1696` |
| `python scripts/tl.py doc-claims-check --strict --json` | rc=0 | `ok=true`, files_scanned=82, flags=0; 353 non-blocking advisories remain enumerated |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | rc=0 | `ok=true`, expected=179, checked=179; failed=0, extra=0, missing-from-manifest=0, required-missing=0, errors=0 |

## Verdict

All four and only four Group B source refs have exactly one disposition: **recovered**. Ref 3 additionally
has the reviewed corrective fast-forward described above. Each raw remote tip contains both its exact old
tip and the exact EOL base. Findings closed: `WP82-R4-G3-F01`, `WP82-R4-G3-F02`. Packet verdict:
`ready_for_independent_rereview`;
this record does not authorize review, merge, land, deploy,
source-branch deletion, writer reopening, or closure of #48, #49, #52, #63, #82, or #84.
