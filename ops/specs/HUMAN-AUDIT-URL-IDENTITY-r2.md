# HUMAN-AUDIT-URL-IDENTITY r2

- packet_id: HUMAN-AUDIT-URL-IDENTITY; revision: 2;
- packet_issue: 1254
- source_base: 4f03566fe9e686ed53c7f8ed0619300c1debba76
- review_class: sensitive; assurance_target: human_audited

Owner instruction: implement the accepted separate K4 infrastructure proposal; preserve PR1253 head and historical audit. This spec records that instruction, not a human audit of future code or an approval of an unknown head.

## Objective and effective write set

Correct K4 comment identity across GitHub issue-to-PR conversion. Four effective source paths, with three net files from the immutable base:
- .claude/dev/packet_loop.py
- .claude/dev/packet_loop_test.py
- docs/HUMAN_AUDIT_COMMENT_URL_IDENTITY.md
- docs/adr/0065-human-audit-comment-url-identity.md (remove provisional g1 file only)

Bounds: at most three source files and 450 added lines from the immutable source base. No release files, workflow, launcher, credential, old frozen spec or PR1253 source edits. A standalone normative appendix records a prospective amendment; do not rewrite Accepted ADR0063 or historical r2 spec bytes.

## Acceptance

A1: Accept only exact HTTPS github.com URLs for the canonical repo, same positive integer issue/PR number and actual comment ID, using /issues or /pull path. Raw issue_url, OWNER association, User actor and canonical owner remain mandatory. Reject query strings, encoded/foreign/extra paths and mismatched IDs. No network redirect as an authority substitute.
A2: The human_exact_head_audit.v1 audit_source may use either exact alias for that one identity, independently of the current raw html_url. Preserve closed schema/type checks, full H/tree/spec/Packet/revision/generation/PR bindings and both review axes. Restrict the amendment to audit schema; do not broaden unrelated authorization or transition consumers.
A3: Preserve the earliest-workflow rule and real timestamps. A changed body/updated_at after the earliest run still blocks; no reconstructed raw JSON or historical grandfather exception for new candidates.
A4: Positive conversion and canonical URL controls plus consumer negatives must exercise real K4 and CLI where practical. Baseline original consumer must reject the reported conversion case; patched consumer must accept it. Wrong repo/number/ID/actor/head/tree/spec, duplicate keys, late timestamps and P0-P2 findings must still block. Targeted mutation checks must have intended failures plus positive controls, not setup/import crashes.
A5: Keep PR1253 at ca49a1387216125fbf351551c2a5ab88794874c2 and tree a2844a835b2fd42ab273406e7d810c3009d121d4. Keep its old test archives attached to that head. Do not relabel them as validation of this correction or an integrated tree.
A6: Prepare an isolated local implementation, exact-head handoff and evidence. Run only bounded targeted/component checks. No fullstandard, full mutation audit, M9, Windows CI or full mutant Windows; no new PR or code push until trigger/cost assessment and required human audit. Unrun promotion gates are NOT_RUN, not PASSED or WAIVED. No blanket gate waiver is granted. No additional model/connector call is authorized by this Packet execution.
A7: Admission/master-drift workflow failure remains separate; do not disable ancestry checks or silently change source H to fix it.

## Authority and completion

The owner accepted this bounded development proposal in the current conversation. Controller may record the Packet/spec/lease; it must not invent a primary human audit or land authorization. Execute one bounded source run, preserve all attempts and stop before scope/cap/time overflow. A completed local implementation remains pending human audit and unresolved required promotion gates. No ready, merge, land, deploy or LIVE authority.

Scope narrowing before publication: docs/PROTOCOL_DA_PHIEN.md is held by active lease wp1240-r1-g1-claude. It is excluded; the new ADR is self-contained and does not modify that file or the other session. Source grants/run clocks are not reset.

Revision 2 / generation 2: adr-song requires every numbered ADR to be registered in protocol section20, which is owned by wp1240. Replace the provisional unlanded ADR with docs/HUMAN_AUDIT_COMMENT_URL_IDENTITY.md. Preserve g1 commit493e7d62b96053cdadd34a42fb5c9fbb3c18a084 and all g1 test results. Continue from that head without resetting the original source deadline or budgets; immutable acceptance base remains4f03566fe9e686ed53c7f8ed0619300c1debba76. No runtime scope expansion or long test permission.
