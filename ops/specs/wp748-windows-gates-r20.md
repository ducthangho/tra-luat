# WP748 r20/g20 — inherit audited g19 candidate, integrate master, drive PR to green

## Authority and exact provenance

Owner authorization: https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6273564956 (2026-10-19T17:48:36Z). It grants r20/g20 to a Claude Code remote session (Linux, `claude_code`). This spec supersedes r19/g19. The r19 lease `wp748-r19-g19-claude-windows-20261018` expired at `2026-10-19T04:48:21Z` before this spec was written; its write-set exclusion already lapsed, so no tombstone is written into the expired lease file (writing one only adds a dead lease to the publish scan). The r20 lease declares `thay_the_cho: []` for that reason. Protocol §3.6 thirty-minute inactivity rule remains effective.

Continuation source: `agent/wp748-g19-claude` on GitHub at `12430197e76dfb87c0e72796d0299b6faaa8b70b`. Its ancestor `a2a358ae6b8649f9e2869f7042c42abf1c98dfd4` (tree `381528ea5ed1809965a49637f8def0f4159f51b6`, base `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9`) carries an owner-posted and a collaborator-posted Human Audit `approved` verdict (#748 issuecomment-6253307079, -6253378341). The two later commits `7a1740c8` and `12430197` (NaN/Infinity rejection, Codex P2) are NOT covered by that verdict and need fresh review. Owner pushed both refs on 2026-10-19; the session verified SHA and tree on the remote.

Executor: Claude Code (`anthropic_claude`, `claude_code`, remote Linux). Reviewer: fresh independent Codex session, read-only on exact final head. Review Class sensitive. No self-review, self-approve, LIVE, Drive, real credentials, merge or land in this lease.

## Effective Executor write set

Same twelve paths as r19, write-set hash `e06292877ba0a66faab54c598f54d9e4845e4c6c41a47a52dc5fd94f850db46d` (sorted NFC casefold, compact UTF-8 JSON):

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

A merge of `origin/master` brings in commits authored under other packets' leases; those paths are not written by this Executor. The Executor's own diff against the merge base remains inside the twelve paths.

## Integration rule

`git merge-tree` of `a2a358a` with master `5618020a` reports exactly one content conflict, `ops/cong_cu_test.py`. Master already carries the #671 fix for t23/t49 (PR #690 and #838, nine review rounds, landed, master gate green). Resolution per owner instruction: take master's `ops/cong_cu_test.py` verbatim. `ops/bash_nen.py` on master is byte-identical to the WP748 change. After the merge, WP748's net diff against master shrinks to the remaining ten paths; the G5 t23/t49 layer counts as closed by #671.

## Acceptance

- Merge commit made on `agent/wp748-g19-claude` (no rebase, no force push); `git diff --check` clean; ruff F delta versus master = 0 on changed Python files.
- Targeted local gates on Linux for every changed test suite, with positive N/N evidence.
- Draft PR into `master`; full CI matrix including Windows via `workflow_dispatch` on the exact head; every required check green, Windows `gate-ops` (`t217`) and `gate-registry` included. Failures are root-caused and fixed inside the write set, never skipped or relaxed.
- Independent Codex review on exact final head: zero P1/P2.
- Owner final approval on a specific SHA before merge. Land bookkeeping is a separate step.

## Stop

Stop and report on: holder overlap, need to write outside the twelve paths, Windows failure whose fix needs product code (`ops/lease_publish.py`, `.claude/hooks/subagent_ghi_detect.py`, `.claude/settings.json`), or missing positive evidence.
