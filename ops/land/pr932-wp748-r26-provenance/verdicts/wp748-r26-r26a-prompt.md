# Independent read-only review with execution receipt — WP748 r26 (spec r25 v2), PR #909 merged head, round 1

You are an independent reviewer (OpenAI Codex), invoked through `launcher.py run` (execution receipt). Do NOT edit `src/`, commit, push, comment on GitHub, or use credentials. Scratch via `mktemp -d` here is fine. Write `VERDICT.md` in THIS directory, incrementally.

Identity (verify first; stop with `VERDICT: blocked` if different): `./src` is a full clone detached at `b5b6aefa66a8ad037ff34430d0210f3b6873913f`, tree `6d47f211da364501e75ef4c622b577e619f2a7be`. This is the head of PR #909, ALREADY MERGED to master (merge `113e0d1`); the code is live. Findings will be fixed on a NEW branch from master. Review Class `sensitive`.

Delta: `git -C src diff e739ac1b74024a20949425c447fb6cf025317c0e b5b6aefa66a8ad037ff34430d0210f3b6873913f` — exactly `.claude/dev/launcher.py` and `.claude/dev/launcher_test.py`. Round-3 change (never reviewed through the launcher): `git -C src diff aaad9ab95ab170df4083e0c8203a88b5bd3b35a9 b5b6aefa66a8ad037ff34430d0210f3b6873913f`.

Spec in force: v2 `ops/specs/wp748-r25-launcher-model-phuc-vu-v2.md` — on `master` first, else `git -C src show origin/ops/wp748-r25-g25-lease:ops/specs/wp748-r25-launcher-model-phuc-vu-v2.md`; identifier sha256 `f20615ae559f377150cfd6a9cfd0bce4478bf28ae3d562a674588a9c6f9d4bdb`. v2 replaces v1: stderr of codex runs is an EXACT allow-list; everything else is dropped and only counted. Lease: `origin/ops/wp748-r25-g25-lease:ops/leases/wp748-r26-g26-claude-remote-20261025.yaml`. Authority: #748 issuecomment-6394503720 (cannot read GitHub; say so).

Previous rounds (on older heads): `./VERDICT_L909C.md` (83d305f: R25-SEC-01 P1, MEAS-02, TEST-03, ROBUST-04 P2) and `./VERDICT_L909D.md` (aaad9ab: SEC-01 P1, TEST-03, EVID-05, RACE-06, CONTRACT-07 P2). The owner requires rounds until ZERO P1, P2 and P3.

Tasks (security first):
1. For EACH earlier finding: closed on `b5b6aef` under spec v2? Measure (command + real output). CONTRACT-07 is to be judged against v2, not v1.
2. Any remaining path for trace/credential content to reach disk (allow-list comparison, partial lines, CR handling, oversized lines, error-drain, writes after close, temp files, run directory), and any path to `DO_DUOC` without complete positive evidence (loss counter, reader still alive, snapshot ordering, candidate regex false negatives/positives on real codex frames). Do NOT author new exploit payloads; describe a direction in words if it needs new attack content.
3. No regression: timeout/kill (124/125), Windows (`creationflags`, Job Object, `codex.cmd`, CRLF), non-codex runs unchanged, `stderr_byte`/`stderr_sha256` semantics, the 10 s join.
4. Tests: run every `r925_*` case (`python3 src/.claude/dev/launcher_test.py --lap-ca <name> --lan 1`) and every `r25_*` mutant (apply each replacement to a TEMP COPY of launcher.py only). Any guard without its own mutant?
5. Size vs the v2 `nang_tran` (≤ 2 files, ≤ 550 added lines vs `e739ac1`).

`VERDICT.md`: reviewer identity (as runtime reports; say what you cannot verify), reviewed SHA + tree, UTC; per-earlier-finding status; new findings ID/severity P0–P3/`file:line`/scenario/fix; commands with rc and N/N. Last line exactly one of `VERDICT: approve` (zero P0, P1, P2 AND P3) · `VERDICT: changes_requested` · `VERDICT: blocked`.
