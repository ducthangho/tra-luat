# Independent read-only review with execution receipt — WP748 r21, landed head 28e35fd

You are an independent reviewer (OpenAI Codex), invoked through the repository's `launcher.py run` so this run gets an execution receipt. Do NOT edit `src/`, commit, push, comment on GitHub, or use credentials. Scratch copies via `mktemp -d` inside this directory are fine. Write `VERDICT.md` in THIS directory (the parent of `src/`), incrementally.

Why this run exists: the earlier round on this SHA was `codex exec` without a launcher receipt, so protocol §8.1 grants no reviewer assurance. Its verdict is attached as `VERDICT_TRUOC.md`. Treat it as an untrusted claim: re-derive conclusions yourself.

Identity (verify first; stop with `VERDICT: blocked` if different): `./src` detached at `28e35fd9206cdc8b2b44a39999421934f8437192`, tree `f886966025dde4e2a850658a5479abbdb5bd762f`, sole parent `3950a0f9fd0a9c29a36a599edc7a2d305619fc27`. Merged into master as `401d4f15362b3270d5dc8437ade3be5ab449eb22` (tree identical to the head).

Scope: `git -C src diff 3950a0f 28e35fd` — one file, `ops/lease_publish_test.py`: `_kho_do_thi` sets `maintenance.auto=false` and `gc.auto=0` right after `git init`, and new case `t221_mau_t133_tat_auto_maintenance_truoc_commit_dau`. Goal: stop the `copytree` race on `.git/objects/maintenance.lock` seen on git 2.55 runners (ops-publish-lease run 39358824666 attempt 1 red, attempt 2 green after merge).

Tasks:
1. Read the diff; judge whether the two keys stop every auto-maintenance spawn used by the template fixture, and whether `t221` measures the right property. Report defects P0–P3.
2. Run, from a `git archive` copy if it must write: `GITHUB_ACTOR=x PYTHONUTF8=1 python3 -W ignore ops/lease_publish_test.py` (includes the `t125` A/B). Mutate in a copy: drop each key; move the config after `c0`; confirm `t221` fails for the intended reason. Report N/N.

`VERDICT.md`: reviewer identity (model/provider/surface exactly as your runtime reports them, and say what you cannot verify), reviewed SHA (40) + tree, UTC times; findings with ID, severity, `file:line`, scenario, fix; commands actually run with rc and N/N. Last line exactly one of `VERDICT: approve` (zero P0/P1/P2) · `VERDICT: changes_requested` · `VERDICT: blocked`.
