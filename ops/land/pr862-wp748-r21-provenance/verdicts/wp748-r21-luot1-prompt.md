# Independent read-only review — WP748 r21/g21, PR #862, exact head

You are an independent reviewer (OpenAI Codex). Do NOT edit `src/`, commit, push, comment on GitHub, or use credentials. Throwaway copies via `mktemp -d` inside this workspace are fine. Write `VERDICT.md` here incrementally.

Identity: `./src` detached at `28e35fd9206cdc8b2b44a39999421934f8437192` (verify full SHA + tree); sole parent must be `3950a0f9fd0a9c29a36a599edc7a2d305619fc27` (= `origin/master` in `src`). Diff: `git -C src diff 3950a0f 28e35fd` — one file, `ops/lease_publish_test.py`.

Context: `.github/workflows/ops-publish-lease.yml` runs master's `ops/lease_publish_test.py`. Run 39352202619 failed twice on GitHub runners (git 2.55): `t125` A/B saw `t133` fail only in the with-`GITHUB_ACTOR` child, reason `shutil.Error` from `copytree` of the `_mau_t133` template repo: `[Errno 2] No such file or directory: .../.git/objects/maintenance.lock`. Hypothesis: `git commit` spawns detached auto-maintenance that creates/removes that lock inside the template while `copytree` copies it. This container's git (2.43) does not reproduce it.

Fix under review: `_kho_do_thi` sets `maintenance.auto=false` and `gc.auto=0` right after `git init`; new case `t221_mau_t133_tat_auto_maintenance_truoc_commit_dau` checks the template's local config and that `.git/config` mtime <= object mtime of `c0`.

Tasks:
1. Is the root-cause hypothesis plausible (git `run_auto_maintenance` after commit, `--detach`, lock file at `.git/objects/maintenance.lock`)? Do the two config keys actually stop every spawning path used by `_mau_t133` and `_them_commit` (commit, checkout, update-index, rev-parse...)? Any other background git writer (e.g. `gc --auto` from other commands, fsmonitor, commit-graph) that could still race `copytree`? If the fix is insufficient, say what is.
2. Does `t221` measure the right thing and fail for the right reason? Check the mtime ordering assertion for flakiness (filesystems with coarse mtime, a later git op rewriting `.git/config`, Windows). Try mutants in a copy: drop each key, move config after commits; confirm red with the intended assertion.
3. Any other users of `_kho_do_thi` whose behavior changes because of the new config?
4. Run `cd src && GITHUB_ACTOR=x PYTHONUTF8=1 python3 -W ignore ops/lease_publish_test.py` (from a `git archive` copy if it must write) and report N/N; it includes the `t125` A/B. If the sandbox blocks something, describe it; do not author hostile payloads.

`VERDICT.md`: reviewer identity, reviewed SHA + tree, UTC; findings P0–P3 with file:line, scenario, fix; commands with rc and N/N. Last line exactly one of `VERDICT: approve` · `VERDICT: changes_requested` · `VERDICT: blocked`.
