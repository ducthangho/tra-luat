# WP484 r2/g2 execution checkpoint for independent review

Status: candidate prepared; NOT final handoff acceptance, zero-P1, cross-approved or landed.
Executor: openai_codex / codex_service / machine-local, native Windows.
Frozen base: c0a5cbe89a90588115262e1a2c3ac84cbd98be9e; tree f9897f6dba19484900776d7af7e9b042070d4ce1.
Spec SHA256: 5927e9368fb4ae2aabe356579a8287d7d555fbc3d3ade884c1ac6065122726af.
Lease: wp-codex-credential-refresh-exec-g2, expires 2026-09-09T21:09:14Z. Attempt1/3.
Authority: https://github.com/ducthangho/tra-luat/issues/484#issuecomment-5605568174
Latest heartbeat: https://github.com/ducthangho/tra-luat/issues/484#issuecomment-5607090387
Exact candidate SHA/tree will be measured after this checkpoint is committed and recorded in the independent reviewer invocation and Issue484 receipt. This file cannot contain its own commit hash.

## Changes and measurements

Shared effective CODEX_HOME; private Windows handle/ACL and POSIX dirfd storage; reject repository/reparse/hardlink/unsafe destinations; guarded atomic replacement with rollback on failed probe. Recovery remembers rejected refresh-token identities and rejects formatting/metadata replay. Candidate probe uses existing codex_cred marker+rc contract in a separate credential home and cwd; successful probe's refreshed bytes are promoted. Checkpoint files contain only identity/head/prompt hashes, and resume checks all anchors before materialization. Raw snapshots are removed before launcher/hook descendants. Unknown child output/nonzero/timeout cannot acquire an automatic attempt-void certificate.

Targeted native Windows Python3.13.1 and WSL Linux Python3.12.3: storage, schema, home policy, rollback/recovery, actual inert child boundary, isolated marker/refresh, checkpoint and timeout-after-output cases passed. Windows kernel directory rename pin, junction, hardlink and ACL checks passed; POSIX directory-fd and symlink/hardlink checks passed. Native restricted sandbox could not open ancestor handles; tests ran as actual Windows user without weakening production checks.

codex_cred_test.py: 14/14 cases and14/14 mutants passed on each OS. Windows legacy symlink/O_NOFOLLOW cases use mocks, not kernel evidence; separate g2 native kernel tests cover Windows boundaries. New launcher targeted mutants:5/5 killed on Windows. Linux native-directory-pin mutation is platform-inapplicable and must be reported separately.

Related regression group: Windows11 passed,3 explicitly skipped(t108/t125/t126 POSIX fixtures); Linux15 passed,0 skipped, including actual shell boundary and bridge ordering. Bash syntax/Python AST passed. Temporary release manifest generated outside checkout and strict verification passed; canonical manifest unchanged. Full CI and full worker oracle NOT_RUN, deliberately final-only after independent review/zeroP1 per owner instruction. Actual credential/LIVE tests NOT_RUN.

## Re-derived predecessor regressions

- r357: wp484_g2_schema_truoc_freshness_va_home_materialize, doctor/home and env-policy tests.
- r358 / cred-r1-probe-inherits-raw-snapshot: real launcher child boundary, codex_cred t14 + scrub mutant, real isolated candidate probe.
- r359 / cred-r1-hook-keeps-stale-readable-auth: actual shell pre-probe materializer delegation and bridge tests, recovery tests. Login status no longer gates restoration.
- r360: two-way freshness and post-probe downgrade rejection in wp484_g2_recovery_probe_rollback_va_snapshot_moi; failed candidates leave old bytes intact.

R3 home-divergence/corrupt-disk candidates were remeasured with g2 home and controlled UTF-8/schema cases. Final severity belongs to the independent reviewer. Historical R1/R2 Codex calls/verdicts and R3 Claude timeout preserved. Independent Claude scope review54108b2b rejected the alleged packet_loop scope blocker, classifying unknown-timeout automatic-refund behavior at base as P2; producer-side certificate removal measured with real CLI and existing consumer. Scope review is not candidate approval.

## Remaining validation / limitations

Independent candidate review and final full CI remain pending. No successor PR created yet because opening it triggers full CI; review local frozen candidate first. No g1 push, merge, deploy or LIVE. Recovery does not claim that readable/structurally valid auth is live; initial materialization alone is not a live probe. Native Windows device-auth PTY availability is unchanged; interactive acquisition remains via WSL repository tool. Unknown agent output cannot automatically refund a content attempt; manual authorized packet-loop void remains audited.

Machine-specific transcripts, current source hashes and test JSON are outside Git under pr485-r3. They contain no actual credential values. Runtime source is frozen in this candidate; reviewer source checkout must stay read-only and test scratch must be external.
