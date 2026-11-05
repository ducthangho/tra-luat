# Proposed continuation #1187 r2/g5 — self-contained historical spec fixtures

Status: proposed only; no lease, source edit, push, new PR or review request authorized by this document.

Confirmed trigger: automatic draft-ready review https://github.com/ducthangho/tra-luat/pull/1205#discussion_r4477622209. Non-shallow single-branch H33 fails three cases with Git rc128; provisioning their exact pinned objects restores all three. Existing all-branch CI does not measure source-ancestry-only portability. M1/M2 already merged; Packet1187 and Mission1177 remain open, no landed/complete claim.

Normative r2 spec and A1–A9 remain frozen at SHA256 975c5d31be6ec4f26145f14893b5c8f7063e5921d1c6dafdca020f50e795299d. This operational addendum proposes a new generation and expanded effective write set only after actual owner approval. Preserve previous generation history, expiry, spent calls, unknown costs and attempts; no reset or borrowing product budget.

Source start: H33 33df4b678e3d1f12e68a9c9d362dc0446f0dd5c2, already merged at M1 6fc9f6d93fdc61a78af407ddc2f142264da79877. Immutable acceptance baseline remains 1f0941e9bba1d1d517eda4174167b81963c06bd5. Use a fresh branch/PR because1205 is merged. Fence actual canonical/master and integrate without changing the audited head merely for drift.

Exactly four writable source paths:
- .claude/dev/packet_loop_test.py
- .claude/dev/fixtures/specs1187/wp1178_r3.md
- .claude/dev/fixtures/specs1187/own_r1.md
- .claude/dev/fixtures/specs1187/own_r2.md

The concrete scratch patch changes only the fixture loader and adds three byte-exact frozen spec snapshots. It verifies existing SHA256 constants, creates explicitly synthetic metadata commits to exercise the actual consumer, records both original provenance OID and synthetic fixture OID distinctly, and preserves the actual-spec-at-H case. No network fetch, cache dependency, skip or fallback is added. Runtime checker, ADR and CI code remain untouched by this generation. Proposed patch SHA256 61a622d64f73eef616d55667ffbc23cd78ab92c3175cf22c0d27f67be561b3fa; measured continuation4files/+270/-9. Cumulative baseline8files/+1488/-11 (direct Git tree diff): proposed ceiling8files/+1600, replacing prior5/+1250 only for this continuation. Never compress/remove tests to fit the cap.

Acceptance: retain A1–A9; additionally a full-history non-shallow branch-only clone lacking all three original metadata objects must pass the three historical byte cases and own-spec-at-H offline. The four actual scratch controls already pass, but this is not final-head evidence. Fixture bytes/hash/provenance must match all three original objects exactly. Consumer-specific negative tests and mutants must still demonstrate failures at the intended consumer; fixture/setup/import errors give no mutation credit. Preserve independent real canonical rollout/source evidence separately from synthetic fixtures.

Requested allowance, ONLY after owner approves this addendum: one fresh separate Codex Executor, one90-minute absolute-clock cloud source run, one read-only fullstandard run<=180minutes with its own absolute deadline, one source push/new draftPR after new-head human audit, exactly one additional connector (total cap6→7), one new-head M9 workflow dispatch. No local model review; no retries/reruns/pushes beyond this allowance; no deploy, LIVE, forcepush or ruleset bypass. Apply standard paired native Windows M3 and required local/supporting/source/masterCI gates to the final frozen head, with all true failures retained. Existing sealed writers are not revived; issue a fresh actual-time g5 lease after namespace/admission checks.

New final H/tree requires new independent human spec/full-diff audit and exact-head land authorization; this proposal cannot authorize an unknown future head or transfer H33 audit. Merge only after all gates, then exact-M postCI, M8/readback and D1–D4. Product H916 remains unchanged. Do not close Mission until every required Packet/obligation is actually landed and no owned work/lease remains.
