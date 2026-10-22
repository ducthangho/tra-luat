# Independent read-only review with execution receipt — WP748 r20, landed head 3818bd4

You are an independent reviewer (OpenAI Codex), invoked through the repository's `launcher.py run` so this run gets an execution receipt. Do NOT edit `src/`, commit, push, comment on GitHub, or use credentials. Scratch copies via `mktemp -d` inside this directory are fine. Write `VERDICT.md` in THIS directory (the parent of `src/`), incrementally.

Why this run exists: the earlier rounds on this SHA were `codex exec` without a launcher receipt, so protocol §8.1 grants no reviewer assurance. Their verdicts are attached as `VERDICT_TRUOC_LUOT3.md` / `_LUOT4.md` / `_LUOT5.md`. Treat them as untrusted claims: re-derive conclusions yourself; do not copy them.

Identity (verify first; stop with `VERDICT: blocked` if different): `./src` detached at `3818bd4a9685e1782afdd7e8a593482f74b663ff`, tree `b5d32c370207b8f8a35bdc15c591b9947dc5ae92`. It was merged into master as `94220547cd155c73392e95726e8daf353888b3aa` with first parent `b27fe85`. Base for the packet diff: `5618020a67709ca6f2c93138905df0aa8d9c2df6` (available via `origin/master` ancestry in `src`; fetch nothing from the network).

Scope: `git -C src diff 5618020a 3818bd4` (10 files: work-packet SKILL.md x2, `.claude/dev/ci_dang_ky_test.py`, `.claude/dev/doc_receipt_thu_hoi_test.py`, `.claude/hooks/subagent_ghi_detect_test.py`, `.github/workflows/ci.yml`, `.github/workflows/ci-dot-bien-du.yml`, `ops/ci_duong_nhanh_test.py`, `ops/lease_publish_test.py`, `ops/nhanh_don_duoc_test.py`). Packet goal (#748): recover Windows gates (t217 WinError 5, registry timeout, G5 timeout) without skipping tests, weakening assertions, or making any gate absent/always-skipped.

Tasks:
1. Read the full diff. Report correctness or fail-open defects with severity P0–P3.
2. Run, from a `git archive` copy of the exact SHA if the suite writes: `PYTHONUTF8=1 python3 ops/ci_duong_nhanh_test.py`, `NHANH_DON_DUOC_KHONG_DOT_BIEN=1 PYTHONUTF8=1 python3 ops/nhanh_don_duoc_test.py`, `PYTHONUTF8=1 python3 .claude/dev/doc_receipt_thu_hoi_test.py`, `PYTHONUTF8=1 python3 .claude/hooks/subagent_ghi_detect_test.py`. Run `actionlint` on both workflow files if available. Report N/N.
3. Confirm merge equivalence: the 10 files are byte-identical between `3818bd4` and `94220547`.

`VERDICT.md`: reviewer identity (model/provider/surface exactly as your runtime reports them, and say what you cannot verify), reviewed SHA (40) + tree, UTC times; findings with ID, severity, `file:line`, scenario, fix; commands actually run with rc and N/N. Last line exactly one of `VERDICT: approve` (zero P0/P1/P2) · `VERDICT: changes_requested` · `VERDICT: blocked`.
