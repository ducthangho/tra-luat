# WP710 — NLM credential refresh, Packet Spec revision 3 (proposal)

## Identity and authority

- `packet_id`: `wp710`; `packet_issue`: https://github.com/ducthangho/tra-luat/issues/710
- `nguon_cap_viec`: người giữ kho, https://github.com/ducthangho/tra-luat/issues/710#issuecomment-5999414373. Comment confirms objective and requires a separate lease.
- `revision`: 3. Supersedes published r2 for executor reroute. r2 received owner approval to create a Claude lease, but no lease was recorded because Claude failed capability preflight.
- `state`: proposed. No executor lease, generation, branch or LIVE authority is granted by this file.
- `base_ref`: `refs/heads/master`; `base_sha`: `8c98afacb9285aa71e5200739236284f7a190d4f`; `base_tree`: `93a49ac374a8e182821e10861033f9eac2a0fd6f` (remote measurement 2026-10-06; remeasure before lease).
- `executor`: proposed `codex` / `openai_codex` / `codex_cli` / local Windows. This reroute requires a new owner GitHub comment; the r2 Claude grant does not authorize Codex. Codex CLI 0.155.1 reported ChatGPT login on 2026-10-06, but the separate execution session must prove runtime identity and capability.
- `risk`: sensitive; `review_class`: sensitive; proposed `effective_review_class`: sensitive. Credential boundary and LIVE adapter are sensitive under protocol §8.
- `depends_on`: owner approval of this reroute; scoped manual exception to missing change-impact policy; no overlapping live lease; canary notebook selection/readback; frozen Spec Git SHA and SHA-256.

## Objective and exact declared write set

Make NLM credential refresh on the host with the original browser profile safe to stage to Drive: run `nlm auth refresh`, prove the refreshed credentials with a real notebook read, and stage only on a positive canary. Report auth, network, timeout and inconclusive outcomes separately. Add a Windows keepalive that is off by default, explicitly enabled, stoppable and serialized across processes. Update RUNBOOK and behavioral tests.

| Path (exact) | Permitted change |
|---|---|
| `scripts/nlm-credential-refresh.ps1` | New Windows refresh and opt-in keepalive entry point. |
| `scripts/nlm-credential-refresh.Tests.ps1` | Hermetic PowerShell behavior and concurrent-process tests. |
| `scripts/tl_gws.py` | Make the existing `nlm-auth-stage` canary fail closed on dead, timeout, network failure and inconclusive result; remove or tightly fence `--force` bypass so this Packet's no-stage rule has no bypass. Keep pre-upload guard inside the stage command. |
| `scripts/tl_selftest.py` | Behavioral regression of the actual stage command, including `None`, auth failure, timeout, network failure, `--force` and positive canary, checking upload call count. |
| `references/RUNBOOK.md` | Host and browser profile prerequisites, canary evidence, commands, status meanings, safe keepalive enable/disable and recovery. |
| `changelog.d/wp-710.md` | Packet changelog fragment required by protocol; no version bump. |

Declared write set is the six exact paths above; no directory prefix or glob. `scripts/nlm-auth.ps1` is untracked in the canonical checkout and must remain untouched and unstaged. Do not alter it, overwrite it or adopt it into this Packet. Existing `scripts/nlm-auto-refresh.sh` and `scripts/nlm-auth-import.sh` call `tl nlm-auth-stage`; the stage guard must protect those calls too. Changes to those wrapper files require a new revision.

## Effective write set and current stop condition

Canonical protocol §5 requires closure from `.github/coordination/change-impact.v1.json`. At the measured remote base this file and its schema do not exist (GitHub contents returned 404 on 2026-10-06). The authorized effective write set and `write_set_hash` are therefore **not measured**. Do not infer that closure equals the declared set. Before `ready` or lease, the dispatcher/owner must resolve this policy mismatch by a protocol-valid, durable decision, re-evaluate closure and conflicts across active leases, and record policy SHA, effective paths, required checks, land obligations and their hashes. If that changes any Spec field, issue a new revision and hash.

## Acceptance and red-making measurements

1. Host-side `nlm auth refresh` runs against the original browser profile with bounded timeout. Capture CLI version, real rc, elapsed time and a non-secret profile fingerprint. Nonzero, timeout or missing profile gives no stage call.
2. Canary reads a specified real notebook through `nlm notebook get` or the existing `_nlm_auth_alive` path. Its notebook ID must be selected before execution from a trusted local config and must match the response. A 0 rc, `nlm login --check` or notebook count alone is not positive evidence. Wrong ID, missing body, parser failure, auth/network error and timeout yield zero stage calls.
3. `tl nlm-auth-stage` itself uploads only when its live canary is positively `True`. Tests inject `True`, `False`, `None`, timeout and network error through the actual command path and count `_stage_enc_upload`: exactly one for `True`, zero otherwise. The `--force` path must not upload after failed or inconclusive canary. Mutating `None` to allow must turn the test red.
4. Windows wrapper orders `refresh -> real canary -> stage` under one inter-process lock. Hermetic fake CLI records order and call counts. Stage failure is reported as failure; no claim that Drive is updated until upload succeeds. Secret sentinel in fake output must not appear in logs.
5. Error taxonomy has distinct machine-readable statuses and operator instructions for `auth_failure`, `network_failure`, `timeout`, `inconclusive` and `stage_failure`; ambiguous errors remain inconclusive. Tests inject each and prove no stage for the first four.
6. Keepalive makes zero scheduled/background/network calls by default. Explicit opt-in starts a bounded, stoppable cycle. Two native Windows processes contending for the lock must never overlap refresh, canary or stage; stale-lock handling must prove process death before takeover. Do not install or auto-start a Scheduled Task.
7. Native Windows targeted tests show true rc plus positive case counts; Python targeted selftest proves command-level guard. Required repository gates and independent exact-head/tree sensitive review must be recorded separately as passed, failed, skipped, not_run or not_measured. A fresh cross-provider reviewer recognized by the runtime, or `human_audited`, is required for sensitive land; Codex cannot review its own work. LIVE canary/stage is an owner-controlled operation on the browser host, not CI or worker acceptance evidence.

## Limits and handoff

- No dispatcher-session refresh, Drive stage, secret read/write, deployment or LIVE call. Worker/test jobs receive no LIVE credentials. No claim of LIVE success from mocks.
- `hinh_dang_ke_thua`: not applicable; new Packet. r1 had no execution or review history.
- `chua_do_duoc`: exact closure/overlap and required checks; chosen canary notebook and readback assertion; actual `nlm auth refresh` capability on the host; Windows lock behavior; all implementation gates. These are stop conditions, not passes.
- Executor handoff must give exact full head SHA/tree, declared and effective changed paths, commands/rc/positive evidence, provider/surface/transport, and all unmeasured items. Reviewer uses independent context and read-only source; same-provider Codex review alone is insufficient for this sensitive Packet. No self-review, approval, merge, land or LIVE authority follows from the executor lease.
