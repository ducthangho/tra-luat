# Independent read-only review with execution receipt — WP748 r23/g23, PR #882, round 3

You are an independent reviewer (OpenAI Codex), invoked through `launcher.py run` (execution receipt). Do NOT edit `src/`, commit, push, comment on GitHub, or use credentials. Scratch via `mktemp -d` here is fine. Write `VERDICT.md` in THIS directory, incrementally.

Identity (verify first; stop with `VERDICT: blocked` if different): `./src` detached at `bab8702692f1d723ac1a84b865660597aa6291e6`, tree `8568aa04e0dfa1dbd014e7b4a3ebd215cb40b522`. Base `747f983ccbcaf29a8e5228d09fd05b5a5ab6e479`. Review Class `sensitive`.

Delta: `git -C src diff 747f983ccbcaf29a8e5228d09fd05b5a5ab6e479 bab8702692f1d723ac1a84b865660597aa6291e6` (delta since round 2: `git -C src diff 682c8880e493e9b4019e599482a33081fa35576f bab8702692f1d723ac1a84b865660597aa6291e6`) (four commits; your round 1 on `8f12e02` is `VERDICT_LUOT1_8f12e02.md`, round 2 on `682c888` is `VERDICT_LUOT2_682c888.md`: F01 P2 still open, F02–F04 closed — report F01 closed / still open with evidence, and re-check F02–F04 did not regress). Spec: `ops/specs/wp748-r23-don-so-assurance-81.md` on branch `ops/wp748-r23-g23-lease` (look on `master` first; if absent, `git -C src show origin/ops/wp748-r23-g23-lease:ops/specs/wp748-r23-don-so-assurance-81.md` if available, else judge from the diff; the identifier is the sha256 `6190ebbb943f1d017de32d9f316f85623906fded49379f4ce2540d957bee9584`, not the branch name). Write set: `ops/land/pr846-wp845-land-evidence.yaml`, `ops/land/pr869-wp748-r22-land-evidence.yaml`, `ops/land/pr869-wp748-r22-provenance/`.

Purpose: apply `docs/PROTOCOL_DA_PHIEN.md` §8/§8.1 uniformly — a launcher receipt with no served-model field leaves the reviewer model family at `khong_do_duoc`, so reviewer assurance is not met. (1) Demote `pr846` (#845) from `landed: true` to `landed: false`. (2) Create the r22 (#869) land record with `landed: false`.

Tasks:
1. Is every factual claim in both records true and traceable to a file in the provenance (or in git)? Check each `measured` claim against its cited file (e.g. job counts per attempt, run conclusions, timestamps, sha256 of prompt vs `run.json`, `SHA256SUMS` integrity, merge parents/tree). Flag claims stronger than their evidence, wrong numbers, or wrong labels (`measured` vs `loi_khai_co_neo` vs `not_measured`).
2. Is `landed: false` correctly justified and are the re-open conditions correct and complete per §8/§8.1/§10.2.4? Does anything in the diff still certify assurance from the tool name?
3. Does `pr846`'s demotion preserve history without rewriting measured facts? Any other record on this tree with the same evidence level left at `landed: true` that this packet should have covered (report only; do not expand scope)?
4. Run `python3 ops/land_evidence_nguon.py --root .` from a `git archive` copy and `sha256sum -c` on the provenance `SHA256SUMS`. Report rc and N/N. Check no secrets and no lone CR in added files.

`VERDICT.md`: reviewer identity (as runtime reports; say what you cannot verify), reviewed SHA + tree, UTC; findings ID/severity/`file:line`/scenario/fix; commands with rc and N/N. Last line exactly one of `VERDICT: approve` (zero P0/P1/P2) · `VERDICT: changes_requested` · `VERDICT: blocked`.
