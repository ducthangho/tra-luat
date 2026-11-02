# Independent read-only review with execution receipt — WP748 r27 (spec r27), round 4

You are an independent reviewer (OpenAI Codex), invoked through `launcher.py run` (execution receipt). Do NOT edit `src/`, commit, push, comment on GitHub, or use credentials. Scratch via `mktemp -d` here is fine. Write `VERDICT.md` in THIS directory, incrementally.

Identity (verify first; stop with `VERDICT: blocked` if different): `./src` is a full clone detached at `483a006b1e436dfe655478ce8e371475b3d649cd`, tree `741e4e99a439ab32ef640c0071e9c5f963dfe46e`, a LOCAL, UNPUSHED merge commit on branch `agent/wp748-r27-claude`: parent 1 `8fbab5f58f0a056c7cfc74208680d97859762a84` (round-3 fixes `98d5cb2` + narrowing `8fbab5f`, on top of the round-3 head `c6906bba897602a975c0b106fa17a8a856955954`), parent 2 master `356eb262cbd491b9599b56d5f7c41c93dd9a28a1`. `refs/remotes/origin/master` in the clone may be newer (master moves). Verify `git -C src diff 8fbab5f58f0a056c7cfc74208680d97859762a84 483a006b1e436dfe655478ce8e371475b3d649cd -- .claude/dev/launcher.py .claude/dev/launcher_test.py` is empty and master-side changes do not interact with the launcher or its tests. The hash is the identifier, not the branch name. Review Class `sensitive`.

Spec (frozen): `git -C src show origin/ops/wp748-r27-g27-lease:ops/specs/wp748-r27-launcher-effort-sandbox.md`, sha256 `7b8b51ffc355540d70df3e897082a498a62d95d285482f2117192b29f19d6fcd`. Lease: same branch, `ops/leases/wp748-r27-g27-claude-remote-20261026.yaml`.

History: `./VERDICT_R27A.md` (`838d7e7`), `./VERDICT_R27B.md` (`cfeafe4`), `./VERDICT_R27C.md` (`c6906bb`). Round 3 left one class open, `sandbox-process-identity-race`, as R27-PID-04c (a zombie parent made a normal run `KHONG_DO_DUOC`) and R27-PID-04d (a root not pinned at init was adopted later).

**Owner decision to evaluate against (not to re-litigate):** after four rounds on the same class, the owner chose to NARROW the sandbox measurement instead of modelling process lifecycles. Consequences, intended:
- Every identity deviation observed in a scan — a child whose ppid/starttime differs from the snapshot, an ancestor that vanished or changed, INCLUDING an ordinary zombie parent with a reparented child — records `DanhTinhDoi` and aborts the scan, which forces `KHONG_DO_DUOC`. The ONLY benign case is the process being read itself vanishing from `/proc`.
- So a normal run may be downgraded to `KHONG_DO_DUOC` (a false negative); the receipt says so in `sandbox_gioi_han`. R27-PID-04c is therefore resolved by design as "conservative, documented", not by distinguishing zombies. Raise it again only if the receipt can claim MORE than was measured, or if the downgrade is undocumented.
- R27-PID-04d: a failed initial pin records `GocKhongGhimDuoc` and the sampler never pins later.

Tasks:
1. Closure of R27-PID-04c (against the owner decision above) and R27-PID-04d, measured. Sweep the class: is there any remaining path where `DO_DUOC` can be reached with an unanchored root, an unvalidated child, or an ancestor that changed? Confirm earlier-closed findings (ALLOW-01, PARSE-02/02b, PROC-03, TEST-05) stayed closed.
2. Re-measure ON THIS SHA: every `r925_*`/`r926_*`/`r927_*` case (`python3 src/.claude/dev/launcher_test.py --lap-ca <name> --lan 1`), including `r926_dot_bien_tu_sinh_moi_thanh_phan_regex`, and every `r25_*`/`r26_*`/`r27_*` mutant in `DOT_BIEN` on a TEMP COPY of launcher.py, a kill counted ONLY via `TinHieuChotCa` raised by the named target. Report counts with rc.
3. Substantive review of the full delta vs master `356eb26` (`git -C src diff 356eb262cbd491b9599b56d5f7c41c93dd9a28a1 483a006b1e436dfe655478ce8e371475b3d649cd`) against the spec: any new P0–P3. Do NOT author new exploit payloads; describe a direction in words if needed.
4. Size: added lines vs master (cap ≤ 2 files / ≤ 800 added, `#748 issuecomment-6408141574`; expected exactly 800) and Codex calls (this is call 4 of 10). You cannot read GitHub; say so.

`VERDICT.md`: reviewer identity (as runtime reports; say what you cannot verify), reviewed SHA + tree, UTC; per-finding closure; re-measured counts; new findings ID/severity P0–P3/`file:line`/scenario/fix; commands with rc. Last line exactly one of `VERDICT: approve` (zero P0, P1, P2 AND P3) · `VERDICT: changes_requested` · `VERDICT: blocked`.
