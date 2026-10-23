# Independent read-only re-review with execution receipt — WP748 r22, PR #869, round 5

You are an independent reviewer (OpenAI Codex), invoked through `launcher.py run` (execution receipt). Do NOT edit `src/`, commit, push, comment on GitHub, or use credentials. Scratch via `mktemp -d` here is fine. Write `VERDICT.md` in THIS directory, incrementally.

Identity (verify first; stop with `VERDICT: blocked` if different): `./src` detached at `b9318cc26101d2697be19ac44be5700534ba0256`, tree `e499945931af024dbd3b2144c5a30c3788e095ab`. Your round 4 reviewed `6e96fefa2353158ba4b9eb405923c044922b56c6` (attached `VERDICT_LUOT4_6e96fef.md`: changes_requested, F02 P2 continuing within the owner's narrowed option (b); F05 closed). Base `9e9a74b2a396ef458d25c51a5563efafbb45ba0c` = `origin/master`.

Delta to review: `git -C src diff 6e96fefa2353158ba4b9eb405923c044922b56c6 b9318cc26101d2697be19ac44be5700534ba0256` (one file `ops/nhanh_don_duoc_test.py`, two commits).

Scope is unchanged from round 4: the owner chose option (b), the NARROWED timeout contract documented above `NGOAI_HOP_DONG_POSIX` (bounded return rc124 with check=False; kill the child's own group/job; truthfully report what was not done; Windows fail-closed rc126; cleanup exception keeps rc124). Detached POSIX descendants are out of scope and must not be re-raised by themselves.

Claimed fixes for each round-4 F02 row: (1) `_VeWindows.ket_thuc` no longer spawns `taskkill`; on TerminateJobObject failure/exception it kills the direct child via `_giet_truc_tiep` and reports, job closed in `finally`. (2) Cleanup-exception path reports the direct-kill outcome truthfully, appends `NGOAI_HOP_DONG_POSIX` on POSIX, no "con bi giet" wording anywhere. (3) Second drain: any `Exception` → rc124 with `thu output LOI`; `_giet_con_treo` wait OSError → rc126 with diagnostic. (4) `Popen` exception: job closed exactly once and a CloseHandle failure is attached via `add_note`. (5) Documentation discrepancies you listed (check=False convention, group wording, `gan_va_chay`/`dong` docstrings, heartbeat comment, the CI root-cause note now stated as an unverified hypothesis). r556 gains cases (b4)(b5)(c2)(w); five new mutants; `timeout-chi-giet-con` replacement is now `_giet_truc_tiep(q)` (bare `q.kill()` raised in r556 (c2) and was false credit).

Tasks:
1. For each round-4 row: closed / still open, with evidence. Look for any NEW path in the delta that returns unbounded, mis-reports, swallows BaseException (KeyboardInterrupt), double-closes, or lets a Windows child run outside a job.
2. Mutant soundness/radius for every mutant targeting r555 or r556 (list from the table), both platforms (reason about Windows).
3. Run from a `git archive` copy: product (`NHANH_DON_DUOC_KHONG_DOT_BIEN=1`), self (`NHANH_DON_DUOC_CHI_TU_KIEM=1`), and every mutant targeting r555/r556 in BOTH `chi_dich=True` and `chi_dich=False`. Report N/N. Describe hostile inputs in words; do not author unusual payloads.

`VERDICT.md`: reviewer identity (as runtime reports; say what you cannot verify), reviewed SHA + tree, UTC; findings ID/severity/`file:line`/scenario/fix; commands with rc and N/N; status of round-4 findings. Last line exactly one of `VERDICT: approve` (zero P0/P1/P2) · `VERDICT: changes_requested` · `VERDICT: blocked`.
