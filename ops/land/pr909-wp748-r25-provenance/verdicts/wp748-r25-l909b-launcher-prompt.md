# Independent read-only review with execution receipt — WP748 r25/g25, PR #909, round 1

You are an independent reviewer (OpenAI Codex), invoked through `launcher.py run` (execution receipt). Do NOT edit `src/`, commit, push, comment on GitHub, or use credentials. Scratch via `mktemp -d` here is fine. Write `VERDICT.md` in THIS directory, incrementally (create it early, update as you go).

Identity (verify first; stop with `VERDICT: blocked` if different): `./src` detached at `56263ec4a8f271e876a08709d3d7969110855f09`, tree `d3303dea883e3db4ec6aabb321c165ab798c2c04`. Base `1c20f3bd6a7ed08114feaf1d91c0790360b8f581`. Review Class `sensitive`.

Delta: `git -C src diff 56263ec4a8f271e876a08709d3d7969110855f09^2 56263ec4a8f271e876a08709d3d7969110855f09 (head is a merge of master `e739ac1` into the work commit `fea07f1`; this diff is exactly the write set — verify)` — `.claude/dev/launcher.py` (+87/-3) and `.claude/dev/launcher_test.py` (+129). Spec: `ops/specs/wp748-r25-launcher-model-phuc-vu.md` — look on `master` first; if absent `git -C src show origin/ops/wp748-r25-g25-lease:ops/specs/wp748-r25-launcher-model-phuc-vu.md`; the identifier is sha256 `5f85d350bc78a28693b1cb095bfa2fa62353975c3ba0e714a2a59c6e8e4dafa3`, not the branch. Authority: #748 issuecomment-6378484722 (quoted in the spec's constraints).

Purpose: for codex runs, `launcher.py run` records the model the SERVER returned per response (from `response.created`/`response.completed` frames in codex's `tungstenite::protocol` trace log) into run.json, while raw trace lines (which carry credentials) never touch disk.

Tasks (security first):
1. Secret exposure: can ANY trace/debug content, or any credential-bearing line, reach `stderr.log`, `stdout.log`, `run.json`, a temp file, or the run directory? Consider multi-line trace output, ANSI colour codes, lines without timestamps, partial lines at EOF, very long lines, non-UTF-8 bytes, interleaving, a user-supplied pre-existing `RUST_LOG` enabling other targets, INFO/WARN/ERROR-level lines that might carry headers, and whether codex can write trace somewhere other than stderr (e.g. a log file under `CODEX_HOME`/`~/.codex/log`) once `RUST_LOG` is set. Report each as LỖI / KHÔNG PHẢI LỖI / KHÔNG ĐO ĐƯỢC with the command and real output. Do NOT author new exploit payloads; describe a direction in words if it needs new attack content.
2. Correctness of measurement: is the parsed `model` really the server's per-response field and not something the client echoes? Dedupe semantics, ordering, `DO_DUOC` only with positive evidence, `KHONG_DO_DUOC` otherwise, filter-crash path.
3. No regression: timeout/kill paths (124/125), Windows (`creationflags`, Job Object, `codex.cmd`), the reader thread on a grandchild holding the pipe, non-codex runs unchanged, `stderr_byte`/`stderr_sha256` semantics.
4. Tests: do the 5 `r925_*` cases and the 8 `r25_*` mutants actually measure each guard (run them: `python3 src/.claude/dev/launcher_test.py --lap-ca <name> --lan 1`; for mutants apply each replacement to a TEMP COPY of launcher.py only)? Any guard without a mutant?
5. Size vs ADR-0053 sensitive ceiling (≤ 6 files, ≤ 450 added lines); write set exactly the two files.

`VERDICT.md`: reviewer identity (as runtime reports; say what you cannot verify), reviewed SHA + tree, UTC; findings ID/severity/`file:line`/scenario/fix; commands with rc and N/N. Last line exactly one of `VERDICT: approve` (zero P0/P1/P2) · `VERDICT: changes_requested` · `VERDICT: blocked`.
