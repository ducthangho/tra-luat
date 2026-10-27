# Independent read-only re-review — WP748 r20/g20, PR #849, round 5

- Reviewer: OpenAI Codex, GPT-6 family as identified by runtime; exact served model identifier is not exposed. Provider `openai_codex`; execution surface hosted Codex shell tools (`codex_service`); transport `machine`.
- Started UTC: 2026-10-19T23:56:50Z.
- Reviewed SHA: `3818bd4a9685e1782afdd7e8a593482f74b663ff`.
- Reviewed tree: `b5d32c370207b8f8a35bdc15c591b9947dc5ae92`.
- Scope: resolve round-4 environment blocker B1 only. Read `VERDICT_LUOT4.md`; prior findings are not reopened. No source edits, repository commits/pushes, GitHub comments, or credentials.
- `./src` is a symlink to `../src`, the reviewed checkout.

## Incremental evidence

- `git -C ../src rev-parse HEAD HEAD^{tree}` — rc 0; exact SHA and tree above, matching the requested identities.
- `git -C ../src status --porcelain=v1 --untracked-files=all` — rc 0; empty output (clean).
- Socket probe and unchanged full regression command: pending. Tests will run in a scratch `git archive` copy of the exact SHA.

- `socket-probe`: `python3 unix_socket_probe.py` in `review-r5.wSMPwR` — rc **0**; started UTC `2026-10-19T23:57:25.678715+00:00`, duration 0.024 s. Logs/receipt: `review-r5.wSMPwR/socket-probe.*`.

- `archive`: `git -C /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rv4/l5/src archive --format=tar --output=/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rv4/l5/review-r5.wSMPwR/source.tar 3818bd4a9685e1782afdd7e8a593482f74b663ff` in `.` — rc **0**; started UTC `2026-10-19T23:57:25.703513+00:00`, duration 0.555 s. Logs/receipt: `review-r5.wSMPwR/archive.*`.

- `extract`: `tar -xf source.tar -C src` in `review-r5.wSMPwR` — rc **0**; started UTC `2026-10-19T23:57:26.259367+00:00`, duration 1.154 s. Logs/receipt: `review-r5.wSMPwR/extract.*`.

- Standalone socket probe: **1/1 passed**. Full suite now running from the unmodified exact-SHA archive, with temporary fixtures confined to scratch. The wrapper disables bytecode writes, Git prompts/optional locks, and user/system Git config; no test-selection or source override is set.

- `git get-tar-commit-id < review-r5.wSMPwR/source.tar` — rc 0; archive identity is `3818bd4a9685e1782afdd7e8a593482f74b663ff`.
- Runtime: Linux, Python 3.13.16 (`python3 --version` — rc 0).
- Full-suite live output: `CA: 104/104 dat · 0 do · 0 hong`. All **104/104** cases measured passing; mutant run pending.

- `full-suite`: `bash -c cd src && PYTHONUTF8=1 python3 ops/ci_duong_nhanh_test.py` in `review-r5.wSMPwR` — rc **0**; started UTC `2026-10-19T23:57:27.414572+00:00`, duration 116.052 s. Logs/receipt: `review-r5.wSMPwR/full-suite.*`.

## Completed measurement and disposition

| Command / measurement | rc | Result |
|---|---:|---|
| `python3 unix_socket_probe.py` in `review-r5.wSMPwR/` | 0 | **1/1** AF_UNIX stream-socket bind probe passed; socket file type verified |
| `cd src && PYTHONUTF8=1 python3 ops/ci_duong_nhanh_test.py` from `review-r5.wSMPwR/` | 0 | **104/104** cases passed, **0** assertion failures, **0** infrastructure errors; **383/383** mutants killed for the intended reason; `TONG: DAT`; 116.052 s |
| Suite classifier self-check (included above) | 0 (suite) | **5/5** rc samples and **3/3** real mutation controls; `TU KIEM PHAN HANG: DAT` |
| Python comparison of every regular file in `source.tar` with reviewed checkout | 0 | **4,645/4,645** file contents identical |

Positive suite evidence, preserved verbatim in `review-r5.wSMPwR/full-suite.stdout`:

```text
CA: 104/104 dat · 0 do · 0 hong
DOT BIEN: 383/383 bi giet dung ly do
TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)
TONG: DAT
```

**B1 closed by measurement.** The previously blocked case `t20zo_la_khong_phai_tep_thuong_do` and all five previously blocked mutants are covered by the complete passing run: `symlink_treo_khong_theo_bi_danh`, `la_bo_chot_tep_thuong`, `la_cho_phep_fifo`, `la_cho_phep_socket`, and `la_khong_theo_symlink`. No case was skipped, socket substituted, assertion weakened, or source modified.

**The round-4 findings disposition stands unchanged:** no new P0–P3 code finding; R2 `mandatory-group-validation`, R3 `shared-ctypes-signature-race`, and connector P2 `ram-pmc-truncated-layout` remain closed. The inherited R1 `full-audit-enforcement` escalation remains unresolved; this B1-only rerun makes no new external-enforcement claim. Those findings were not re-audited in round 5.

Final identity commands (individual rc and output retained in `review-r5.wSMPwR/final-identity.json`):

- `git -C src rev-parse HEAD HEAD^{tree}` — rc **0**; same requested SHA/tree.
- `git -C src status --porcelain=v1 --untracked-files=all` — rc **0**; empty output.
- `git -C src diff --exit-code` — rc **0**; empty output.
- `git -C src diff --cached --exit-code` — rc **0**; empty output.

The reviewed checkout remains clean at the exact SHA/tree above. All review writes and suite fixtures stayed in the workspace outside the reviewed checkout. No source edits, commits/pushes to the reviewed repository, GitHub comments, credentials, or network requests were used. Suite-created Git fixture repositories are scratch only. Native Windows and hosted CI checks were not rerun; they are outside this B1-only scope.

Completed UTC: 2026-10-19T23:59:51Z.

VERDICT: approve
