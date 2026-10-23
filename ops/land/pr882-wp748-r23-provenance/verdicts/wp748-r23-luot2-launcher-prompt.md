# Independent read-only review with execution receipt — WP748 r23/g23, PR #882, round 2

You are an independent reviewer (OpenAI Codex), invoked through `launcher.py run` (execution receipt). Do NOT edit `src/`, commit, push, comment on GitHub, or use credentials. Scratch via `mktemp -d` here is fine. Write `VERDICT.md` in THIS directory, incrementally.

Identity (verify first; stop with `VERDICT: blocked` if different): `./src` detached at `682c8880e493e9b4019e599482a33081fa35576f`, tree `15e043161156b5be9e9d496aab71ec10b3a7f3ae`. Base `747f983ccbcaf29a8e5228d09fd05b5a5ab6e479`. Review Class `sensitive`.

Delta: `git -C src diff 747f983ccbcaf29a8e5228d09fd05b5a5ab6e479 682c8880e493e9b4019e599482a33081fa35576f` (delta since round 1: `git -C src diff 8f12e02856eb130160c40188470f7e5911ab1687 682c8880e493e9b4019e599482a33081fa35576f`) (three commits; your round 1 on `8f12e02856eb130160c40188470f7e5911ab1687` is attached as `VERDICT_LUOT1_8f12e02.md`: changes_requested F01 P2, F02 P2, F03 P3, F04 P3 — also report each one closed / still open with evidence). Spec: `ops/specs/wp748-r23-don-so-assurance-81.md` on branch `ops/wp748-r23-g23-lease` (look on `master` first; if absent, `git -C src show origin/ops/wp748-r23-g23-lease:ops/specs/wp748-r23-don-so-assurance-81.md` if available, else judge from the diff; the identifier is the sha256 `6190ebbb943f1d017de32d9f316f85623906fded49379f4ce2540d957bee9584`, not the branch name). Write set: `ops/land/pr846-wp845-land-evidence.yaml`, `ops/land/pr869-wp748-r22-land-evidence.yaml`, `ops/land/pr869-wp748-r22-provenance/`.

Purpose: apply `docs/PROTOCOL_DA_PHIEN.md` §8/§8.1 uniformly — a launcher receipt with no served-model field leaves the reviewer model family at `khong_do_duoc`, so reviewer assurance is not met. (1) Demote `pr846` (#845) from `landed: true` to `landed: false`. (2) Create the r22 (#869) land record with `landed: false`.

Tasks:
1. Is every factual claim in both records true and traceable to a file in the provenance (or in git)? Check each `measured` claim against its cited file (e.g. job counts per attempt, run conclusions, timestamps, sha256 of prompt vs `run.json`, `SHA256SUMS` integrity, merge parents/tree). Flag claims stronger than their evidence, wrong numbers, or wrong labels (`measured` vs `loi_khai_co_neo` vs `not_measured`).
2. Is `landed: false` correctly justified and are the re-open conditions correct and complete per §8/§8.1/§10.2.4? Does anything in the diff still certify assurance from the tool name?
3. Does `pr846`'s demotion preserve history without rewriting measured facts? Any other record on this tree with the same evidence level left at `landed: true` that this packet should have covered (report only; do not expand scope)?
4. Run `python3 ops/land_evidence_nguon.py --root .` from a `git archive` copy and `sha256sum -c` on the provenance `SHA256SUMS`. Report rc and N/N. Check no secrets and no lone CR in added files.

`VERDICT.md`: reviewer identity (as runtime reports; say what you cannot verify), reviewed SHA + tree, UTC; findings ID/severity/`file:line`/scenario/fix; commands with rc and N/N. Last line exactly one of `VERDICT: approve` (zero P0/P1/P2) · `VERDICT: changes_requested` · `VERDICT: blocked`.
