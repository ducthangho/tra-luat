# WP607 Windows lease gate / r1 / generation 1

Owner directive in task 01a0c978-e49e-7de1-a05c-e99215f53b2e:
"Tôi là chủ kho, nếu cần thu hồi lease cũ hoặc bất cứ phương án nào khả thi để merge và land thì đề xuất và thực hiện cho tôi. Đọc kỹ skill"
This packet records the necessary repair identified by the premerge gate for #568.
It does not grant approval of its future code or transfer the human audit of #568.

Objective: repair two Windows defect classes without weakening lease validation:
platform-dependent byte fixtures (t129/t144 and t139's inherited control), and
asynchronous subprocess decoding of malformed UTF-8 (t150).

Base: 714f36e6aad844f2c1a6713256f3abbdea64aec9.
Branch: codex/wp607-windows-gate-r1.
Product write set: ops/lease_publish.py; ops/lease_publish_test.py.
Metadata: ops/specs/windows-lease-gate-r1.md and ops/leases/windows-lease-gate-r1-g1-codex.yaml on separate authority branch.
Provider/surface/transport: openai_codex / codex_desktop / machine.
Review class: sensitive. Max300 added lines, two model-review rounds.
Assurance required for land: human_audited on the new exact SHA.
Independent Codex reviewer requested at higher model/effort; model identity must be declared honestly.
Expiry: 2026-09-23T14:37:00Z. No merge/land/deploy/LIVE authority for this new candidate.

Acceptance:
1. Exact LF fixture bytes remain equal on Windows/Linux; reader assertions not weakened.
2. t129/t144/t150 positive/negative controls pass on native Windows.
3. t139 catalog retains all intended killed/surviving outcomes on a declared capable environment; native missing symlink privilege stays an explicit limitation.
4. GOI_GIT decodes UTF-8 synchronously, preserving returncode and established newline behavior; valid Unicode succeeds, invalid stdout or stderr raises synchronously without reader-thread traceback.
5. Invalid filename fixture uses Git's index/object layer, avoiding native filesystem assumptions.
6. Independent review, canonical admission and required full CI before merge; no skips, workflow edits, ruleset edits or reinterpretation of failures as passes.

Preserve #568 exact-head audit boundaries. No changes to its product file in this packet.
