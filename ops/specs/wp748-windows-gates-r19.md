# WP748 r19/g19 — complete two G3 children, then prepare Human Audit

## Authority and exact provenance

Owner authorization: https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6252394793, exact readback. Human Audit preparation authorization: https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6252357389. The latter is not an audit verdict. This spec supersedes r18/g18 after its inactivity tombstone at commit `439a6b9853600ac6b71a3df855a19603073d4662`. All r18 and inherited earlier acceptance, review and stop conditions remain unless narrowed below. The current protocol §3.6 thirty-minute inactivity rule remains effective; the separately proposed three-hour change is not effective.

Immutable acceptance base: `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9`. The only continuation source is clean, unpushed `agent/wp748-g18-claude` at HEAD `a2a358ae6b8649f9e2869f7042c42abf1c98dfd4`, tree `381528ea5ed1809965a49637f8def0f4159f51b6`. Its parent is g17 source `b643cfca250497964e2d920dddf6f8eccfb85fce`. Transfer this exact committed source into a fresh isolated g19 clone only after source/destination, live-ref, unique-holder, write-set, provider, lease and cleanliness checks. No cherry-pick without an explicit provenance record. No stale gate evidence becomes exact-head evidence merely by transfer.

Executor: Claude Code Opus 5.5 (`anthropic_claude`, `claude_code`, machine/local Windows), sole product writer on `agent/wp748-g19-claude`. Reviewer: fresh independent Codex session, read-only on exact final head. Review Class sensitive; assurance target cross-provider approval or an independent durable Human Audit verdict. Dispatcher may edit coordination metadata only. No self-review, product push before readiness, merge, land, LIVE, deploy or real credentials.

## Effective Executor write set

1. `ops/bash_nen.py`
2. `ops/cong_cu_test.py`
3. `ops/lease_publish_test.py`
4. `.claude/dev/ci_dang_ky_test.py`
5. `ops/nhanh_don_duoc_test.py`
6. `.github/workflows/ci.yml`
7. `.github/workflows/ci-dot-bien-du.yml`
8. `ops/ci_duong_nhanh_test.py`
9. `.claude/dev/doc_receipt_thu_hoi_test.py`
10. `.claude/skills/work-packet/SKILL.md`
11. `.agents/skills/work-packet/SKILL.md`
12. `.claude/hooks/subagent_ghi_detect_test.py`

Write-set hash, sorted NFC casefold exact paths encoded as compact UTF-8 JSON: `e06292877ba0a66faab54c598f54d9e4845e4c6c41a47a52dc5fd94f850db46d`. `.claude/settings.json` and `.claude/hooks/subagent_ghi_detect.py` remain outside scope. A need to edit either requires a new revision and generation.

## Immediate g19 phase and evidence

The g18 `k01_so_dang_ky_nhan_muc_da_noi` receipt on `a2a358a` is rc0 with a Git-ignored mirror present; registry self-check with `PYTHONUTF8=1` is rc0, 1040/1040 counterexamples. Independently verify command, source HEAD/tree, content and log hashes before credit. Do not rerun completed k01 solely to fill time. Historical g17 light-mode rc0 checks for the two G3 children are not full-suite results on g19.

`subagent_ghi_detect_test.py` on g18 had two memory-killed attempts without final rc, thus inconclusive. `ops/nhanh_don_duoc_test.py` was not run on g18. Run these two children serially on one committed exact g19 HEAD, first hook then fast-mutant. Capture command, start/end, real rc, bounded log, SHA256, head/tree, environment and positive totals. Avoid simultaneous heavy suites and do not cancel merely because elapsed wall time is long. If Claude Code kills a child for memory pressure or Windows returns `0xC0000142`, preserve its log and classify inconclusive unless a code defect is proved. Do not disable Claude Code memory-pressure handling. If a code defect is demonstrated, modify only this write set; commit through hooks, then remeasure the affected red child on the new exact head. Keep prior green children as historical; do not run them solely to fill time.

Once both G3 children have positive receipts and no unresolved code red remains, freeze the committed head and prepare the Human Audit evidence packet. `human_audited` requires an independent human with durable GitHub identity to read spec/diff/receipts and post a verdict anchored to full reviewed SHA; owner permission to prepare is not a verdict or a `running → reviewing` transition. Keep full local gates, independent Codex review, exact-head CI, and separate full 239×52 mutant audit unmeasured until actually run as required by the inherited r18 acceptance path. The targeted 239 declared-target gate does not replace full audit. Product push remains once per PR only after all fixes, complete local gates and independent zero-P1/P2 review; exact-head CI follows push. No merge, land or LIVE authority is granted.

## Preflight and stop

Before Executor write or test, verify owner comment, published spec SHA256, bilateral g18/g19 tombstones, full live refs, sole holder of all twelve paths, valid lease and expiry, clean isolated g19 branch, exact source/base/head/tree/diff, provider/model/surface and required capabilities. Stop on mismatch, overlap, stale generation, denied tool, out-of-write-set need or missing positive evidence. Finish expensive read-only checks before publishing the lease and start Executor promptly after final preflight. Do not promote targeted, background, memory-killed or stale evidence to full pass.
