# Independent read-only review with execution receipt — packet wp919 (ADR-0055), round 3

You are an independent reviewer (OpenAI Codex), invoked through `launcher.py run` (execution receipt). Do NOT edit `src/`, commit, push, comment on GitHub, or use credentials. Scratch via `mktemp -d` here is fine. Write `VERDICT.md` in THIS directory, incrementally.

Identity (verify first; stop with `VERDICT: blocked` if different): `./src` is a FULL (non-shallow) clone, detached at `4e4d482e46cccc6b5e7e6c4f8cf4af636b63e070`, tree `b20fb04d7612bfa5ed4451c0a45c7e8b36fdc248`. LOCAL ONLY (not pushed) — the review is anchored to this SHA. Base (merge-base with `origin/master`): `0dbb4c22aaaaf801e6c392e235391a35c1a6a268`. Review Class `sensitive`.

Delta: `git -C src diff 0dbb4c22aaaaf801e6c392e235391a35c1a6a268 4e4d482e46cccc6b5e7e6c4f8cf4af636b63e070` — exactly `docs/adr/0055-tran-loi-goi-codex-len-muoi.md` (new) and `docs/PROTOCOL_DA_PHIEN.md` (§20 only). Round-3 change only: `git -C src diff 0a5c5e59af4c416e2524e1c349d50ac73bdde2a5 4e4d482e46cccc6b5e7e6c4f8cf4af636b63e070`.

Spec in force is REVISION 3: `ops/specs/wp919-adr-0055-tran-loi-goi-codex-muoi-r3.md` — on `master` first, else `git -C src show origin/ops/wp919-r1-g1-lease:ops/specs/wp919-adr-0055-tran-loi-goi-codex-muoi-r3.md`; identifier sha256 `7d0eb91dd35a36a547348dbc0370366975071c6b3ac3468c2bab7351edbf2987`. r3 replaces r2 because of your round-2 finding WP919-R2-01 (the invariant sentence of Hợp đồng 2). Lease in force: `origin/ops/wp919-r1-g1-lease:ops/leases/wp919-r3-g3-claude-remote-20261025.yaml` (g2 and g1 carry `da_bi_thay_the`). Owner authority comments: #919 issuecomment-6393799783 (r1), issuecomment-6394493260 (r2), issuecomment-6396165849 (r3) — you cannot read GitHub; say so.

Round 1 (on `3868e92`): `./VERDICT_ROUND1.md`. Round 2 (on `0a5c5e5`): `./VERDICT_ROUND2.md` — open WP919-R2-01. The owner requires rounds until ZERO P1, P2 and P3.

Tasks:
1. For WP919-R2-01 and EVERY round-1 finding: closed on `4e4d482e46cccc6b5e7e6c4f8cf4af636b63e070`? Measure (command + output), do not just read. Check the ADR's invariant sentence against r3's Hợp đồng 2 wording.
2. Re-check the whole diff against r3 (every Hợp đồng clause and Chấp nhận bullet), not only the changed lines: new contradictions, claims stronger than evidence, numbers that drifted, broken references.
3. The new selection rule: enumerate the cases you used in round 1 (and any new ones) against the "khi và chỉ khi" sentence and the table; confirm no added line can raise the ceiling and that a spec without ADR-0055 lines behaves exactly as under ADR-0052.
4. Gates: `python3 src/.claude/dev/packet_loop.py adr-song --root src`, `doctrine-scan --root src`, `python3 src/scripts/tl.py doc-claims-check --path <each changed file> --json` (run inside `src`, `core.abbrev 7`); report rc and the positive counts.

`VERDICT.md`: reviewer identity (as runtime reports; say what you cannot verify), reviewed SHA + tree, UTC; per-round-1-finding status; new findings ID/severity P0–P3/`file:line`/scenario/fix; commands with rc. Last line exactly one of `VERDICT: approve` (zero P0, P1, P2 AND P3) · `VERDICT: changes_requested` · `VERDICT: blocked`.
