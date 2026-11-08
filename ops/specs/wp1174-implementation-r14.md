dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# WP1174 R14 — Hoàn tất source adapter r20 và native review đầy đủ

- Packet 1174 revision 14, generation 11, Mission 1172 revision 18, review_class sensitive.
- Mission 18 SHA256: 2445cb3b09fec6617c43073a5aab602118d8011e1bd2dec98ee8aafa93617604.
- Source executor: codex / openai / codex_service / machine; serving model/effort không đo được.
- Reviewer: anthropic_claude / claude / claude_code / machine/local; yêu cầu Opus5.5/high, serving identity KHONG_DO_DUOC.
- Canonical acceptance baseline c6afde62c846f1ef3d6a83c14459966849edf756, raw27 27fd80803e9a8f80e660752f58c8dd477e9730c8 chỉ đối chiếu lịch sử.
- Metadata P14 parent P13 42a8c75f703b7ee56b38ce658887c764b803c7d5; actual metadata OID được bind sau commit, không fake future SHA.
- Private source predecessor 53aef2e36e384de46f022cecc2eb2e235fb59594, tree ebe530000a559d600e1ebcc744f1a07e419c14b8; public PR1275 cònH5.

## 1. Nguồn có hiệu lực và kỹ thuật kế thừa

Chỉ có hiệu lực sau exact C10 decision, installed/readback Mission 18, immutable P14 và source authority/lease/I2/doctor/begin thực tế. Metadata approval không là source approval, native verdict hoặc activation.

Design r20 tại ops/specs/wp1174-c5-adapter-design.md bất biến SHA256 5a749f921de112565779b8b1e42a2324e8efbc1e5e053d11919d30d8cf20a117, approved design head c172150d64c4fa1382469c81a658410c85aff88d. Toàn r20 là normative, không thay bytes để ghi approval mới.

Mọi yêu cầu kỹ thuật của R12 sections1–6,8,10–14 được incorporated bằng exact immutable file ops/specs/wp1174-implementation-r12.md tại P12, SHA256 624f0f5917e555d329efcd46349f60c878667b7b38cf96282bb64a6f5cf232a5. Không bỏ acceptance, negative, oracle, old finding slug hoặc profile. Binding R12/g9/Mission 16 và operational budget/review delivery R12 sections7,9 được thay bằng R14/C10 này; các historical verdict/usage vẫn giữ. Reviewer phải đọc assigned normative annex bytes; hash chỉ chứng minh integrity, không thay việc đọc. Coverage union phải phủ đủ mọi incorporated technical section và toàn source.

## 2. Phạm vi source g11 đóng

Whole c6→final đúng 5 paths, tối đa6000 added, không reanchor/golf/drop IDs:

- .claude/dev/packet_loop.py
- .claude/dev/packet_loop_test.py
- docs/PROTOCOL_DA_PHIEN.md
- ops/specs/wp1174-c5-adapter-design.md
- ops/specs/wp1174-implementation-r14.md

P14 chỉ metadata, normal descendant của P13 42a8c75f703b7ee56b38ce658887c764b803c7d5. Source predecessor final H53 53aef2e36e384de46f022cecc2eb2e235fb59594. Source executor g11 mới normal merge P14 + H53, đồng bộ scoped spec path r13→r14, rồi chỉ sửa hai actual native P2 classes:

- A `wp1174-r13-source-tombstone-topology-unmeasured`: canonicalize cả nonnull lineage.source_path và enrollment.legacy_source_path trong admission, reject lexical `..`/repeated slash; đưa cả hai vào measured runtime topology trước lock và khi authority refresh dưới lock. Giữ initial_state_path guards. Trước lock/probe/temp/witness/tombstone phải reject source khác exact mount hoặc symlinked parent; actual rc8 UNKNOWN và no write controls. Positive same mount và initialized-v3 latest adopted source controls bắt buộc. Independent scratch audit actual rc0/14 assertions tại `/workspace/scratch/wp1174-r13-topology-independent/report.md`: foreign-mount fixture trước fix rc0/7 writes; actual symlinkparent trước fix rc8 durability_unknown sau5 attempted writes; remedy đối chứng rc8 UNKNOWN zero lock/probe/write, positive 0. Không mở rộng credential/security policy.
- C `wp1174-r13-secret-channel-oracle-incomplete`: giữ 85 IDs, thêm subcases/oracles dùng concrete fixture seed và derived hmac_key để kiểm absence trong A, S, captured stdout/stderr/tracebacks, `_WP1174_NATIVE_FACTS`, emitted native report và Windows unit oracle record. Thêm named leak mutant trong emitted detail/probe facts; kill phải do đúng absence assertion, controls init_fresh/admission_wrong_scope xanh. Không in seed/key thật hoặc fixture values vào report.

Actual A/C raw findings trên H53 giữ đầy đủ. D đã terminal actual approve chỉ part scope, 3 old P3 và new P3 `wp1174-r13-water-identity-direct-call`; phải đọc raw terminal D và collector/readback trước freeze; P0–P2 mới ngoài hai class này cần checkpoint mới, không tự mở scope. C9 E old head đóng unused, không gọi integrator trên blocked H53, không refund. Hai MD frozen tại P14. Không sửa thêm P3 hoặc bỏ negative/oracle/inventory; mọi P3 cần fresh exact-final disposition nếu còn. Product digest H53 chỉ lịch sử, C10 cho phép đúng topology fix trên nên phải đo final digest mới, không ép digest cũ và không fake final hash.

Giữ normal ancestry H1–H5,196,275,669,H53 và P12/P13/P14; không reset/rebase/force hoặc refund. Whole c6→final giữ5 paths/+≤6000. Source≤20 phút gồm reads/tools/tests/waits. Root readonly gates dùng shared budget riêng đã tính; không kéo dài executor.

## 3. Bất biến thực thi và phép đo

Giữ toàn r20/R12 technical annex: exact authority/installed mission/spec/lease binding, canonical Git no shallow/graft/replace/alternate/injected env, HKDF known-answer/private seed owner-mode-nlink/noFollow, closed core/optional/per-writer fields, fixed lock/no-replace/fsync/readback/tripwire, source high_water/immutable snapshot/recovery/durability và no dispatch trước reserved_for_dispatch. Không đọc/in token/seed/HMAC; project children dùng clean environment không LIVE/Drive/GAS/NLM credentials. Legacy v2/unscoped/golden/ADR0065 không đổi.

Ba H5 blockers vẫn phải được reviewer final xác minh cả class: PushEvent before/after ancestry, zeroOID/missing-object/retention; reused source/target/witness durability dưới khóa trước cutover/finalize/dispatch, terminal replay không rewrite history/counters; recovery immutable source snapshot khớp predecessor high_water/path/generation/revision/Packet/Mission trước mọi probe/temp/write. Imported-v2 controls và initialized-v3 absent/present đều bắt buộc.

Giữ frozen 85 IDs, Linux fixture 83, native Linux 84 và Windows frozen 13;14 writers+14 races=28. Không đổi inventory/controller hoặc làm yếu oracle. Mọi registered mutant OLD/NEW anchors unique, assertion kill đúng predicate, positive/cross-family controls passed; CliSapDo/crash/mismatched-exception không có kill credit. Hai survivor trên 275 đã được test-only669 xử lý bằng fresh target chứa đúng initial bytes và multi-anchor cùng class; phải đo lại trên final H, không coi275 fail/stale là final pass.

## 4. Gate và platform

Trước source publication: exact final H clean/tree/fivehash/snapshots; diff-check; selftest 1777 N/N; ADR 64; frozen fixture 83; mọi applicable fixture mutants/controls và all meta-anchors; regression 460 (r812_,r813_,r1187_,wp1254_); codepage actual cp1252/cp1258 và real-main selection composition; cloud overlay negative/no write (không nativepositive); root independent counterexamples/holdouts; native cross-provider composite approval; Windows focused13 và raw m1174_allow_windows oracle; independent AI delegated_owner_audit exact H theo r20 source only override. Không publication khi gate pending/unknown/failed.

Sau qualified publication: automatic Ubuntu CI requiredjobs gate,gate-cong-cu-gop,gate-ops,gate-packet-loop,gate-registry, native Linux 84 qua real main trên ext4/XFS và actual WP1174_NATIVE_REPORT_V1 M/H/clone/source tree/filehash/run/attempt/job/producer/snapshot provenance; full Linux M9 exact H; actual connector; canonical K0–K7. Required skipped/not_run/cancelled/timeout/infra/missing/unknown không pass. Sau đủ gates và exact head authority mới normal expected-head merge, hậu-merge checks/readback và bookkeeping/lease closure. Không formal GitHub Review Approve hoặc human signature giả.

Không Windows CI, main/full Windows mutants, registry/project suite hoặc manual ci.yml (runner_set gồmWindows). Chỉ frozen 13 baseline/candidate và một raw unit oracle trên owner host đã verify, ưu tiên host đang online phù hợp; không tladmin/ACL bypass/install security. Private bundle SHA/tree/fivehash verify và normal clone/LF/GitHub origin/symbolic ref/clean trước snapshot. Không chiếm process/lock #1124/#564. Offline tối đa10 phút rồi chọn route được phép khác hoặc blocked, không chờ ASUS vô hạn. H5/source 275/669 gates chỉ lịch sử cho final H mới.

## 5. Native K4 bằng coverage union có bằng chứng

C8 run eb318a05d06f4f209d3836288df487ca trên 275 actual rc0 nhưng verdict blocked vì context coverage, có3 P3; không approve, không refund/void, không carry qua head mới. Một context không đọc hết source; R14 thay review delivery một context bằng bốn part reviewers độc lập A/B/C/D rồi integrator E. Assurance vẫn native Claude cross-provider đối với Codex source, cộng independent source owner audit, không global provider/target human exception.

Mỗi part≤15 phút, tối đa2 đồng thời, context mới không fork source; E≤10 phút trong context mới sau cả 4 terminal. Tất cả dùng official canonical launcher, same final H/tree/fivehash/clean readonly checkout, prompt SHA/deadline/read-only restrictions và before/after snapshot. Không project tests, network/secrets/models con, hoặc viết source/plan. Yêu cầu Opus5.5/high nhưng không attested serving identity giả.

Trước dispatch đóng băng coverage manifest bằng byte/line ranges/digests, không cắt function và có boundary overlap. Từng part tự verify Git/head/hashes, đọc COMPLETE current authority package và full R14 này; đọc toàn assigned r20 clauses theo manifest, coverage union phải phủ đủ r20. E đọc full r20. Phân công tối thiểu:

- A: production diff nửa đầu+interfaces; r20 sections1,2,5,8 và R12 technical sections1–3.
- B: production diff nửa sau+interfaces và toàn protocol diff; r20 sections3,4,6,7,9,11 và R12 sections4,14.
- C: test diff nửa đầu+interfaces; r20 section10 và R12 sections5,10,11.
- D: test diff nửa sau+interfaces, native report/schema/producer/Windows; r20 section12 và R12 sections6,8,12,13.

Nếu function hoặc invariant băng qua phần, đọc trọn phần liên quan và khai overlap. Phủ toàn c6→final production/tests/protocol và cả hai MD, cùng tất cả incorporated technical clauses; không lấy bytehash hoặc verdict cũ làm đã đọc. Mỗi raw part report neoH/tree, ranges read to EOF, interfaces, findings P1/P2/P3 đầy đủ location/reason/fix/oracle/risk, limits và KET_LUAN cuối stdout. Incomplete coverage hoặc P0–P2 thì part không approve. Mọi P3 phải báo.

E đọc toàn raw A–D reports, coverage manifest và current authority/contracts; tự verify whole diff reconstruction/digests, ranges khônghở, exact head/snapshots/producer/gate trạng thái, và cross-part interfaces; đọc thêm code cần thiết. E chỉ approve khi cả 4 part đều đủ và không P0–P2, interfaces không mâu thuẫn, mọi P3 được ghi. E khai rõ personal reads và measured coverage union, không giả cá nhân đã đọc hết source. Final composite K4 thực tế là nguồn verdict canonical round g11; cả 5 native calls đều tính chi phí, không che bốn calls bằng nhãn part. Nếu thiếu coverage/context hoặc có blocker, không tự gọi lượt thứ6 trong C10.

## 6. Checkpoint C10 và ngân sách

C10 thêm tối đa6 calls: source call 8≤20 phút và native 5 fresh contexts A–D≤15 phút/part, E≤10 phút, max 2 parallel. New exact H bắt buộc fresh đủ 5; không carry approve/coverage từH53. Cumulative source 8/native 21/connector 2/canary 1 =32; cộng 2 independent Codex service scratch roles (topology audit và metadata planning) = combined34. Actual trước C10 source 7/native 16 sau D terminal/connector 1/canary 0, cộng 2 scratch; D terminal actual approve chỉ part scope có P3; collector/readback phải reconcile trước install. C9 E unused đóng ở old head, không refund/reassign. Giữ C2unknown/C3closed/C5closed và toàn C6/C7/C8/C9 calls, blocked/stale/failed/unknown exits. Per-PR native actual-call cap21, không ẩn4parts sau1 round.

Shared inclusive cap995 phút, supersedes960; counter51closed+ceil((nowUTC−2026-11-07T16:17:24Z)/60), mọi wait thật, hard expiry2026-11-08T08:03:01Z không đổi. Trước mỗi dispatch đo used+reserved≤995 và absolute deadlines. Finite source/review checkpoint reserve70 phút (20 source+30 native+20 coordination) có thể feasible khi đo. Full completion forecast220 phút =20 source+30 native+150 CI/M9/postmerge+10 canary+10 metadata/bookkeeping hiện vượt995: không claim đủ budget tới merge. Chỉ source/review checkpoint được conditional admit; trước publication/CI/land phải đo lại full remaining reservations, nếu infeasible giữ pending/paused và durable handoff, không tự hạ CI forecast hoặc fake pass.

CI giữ9heads/attempts đã 6; M9 giữ2runs/24Linux runner-hours đã 1; Windows 5 runs/60phút/15 mỗi run đã 3 runs/26 phút; remaining 2 runs/≤30 min, same frozen 13 pair và đúng1 unit mutant. No Windows CI/full suites/global workflow/security changes/paid purchase. Tất cả gates section4 vẫn required, không budget waiver.

G10 phải quiescent, D terminal/readback và old lease ended, giữ actual A/C blocker journal/history. C10 exact decision/install Mission 18, immutableP14 metadata actual selftest/readback, source authority, actual g11 exclusive lease bot/I2/doctor/begin1/1 rồi mới source. Metadata không cấp source/land hoặc native approval. Target actual-human route và original Mission objective không đổi.

## 7. Findings, audit, rollback và completion

Ba P3 của native 275 giữ slugs wp1174-r12-human-verifier-path-aba, wp1174-r12-accept-workflow-runs-double-read, wp1174-r12-recheck-status-label. Không tự đóng/carry debt. Final reviewers xét lại severity; nếu cònP3 thì owner disposition exact final H/slug/reason/follow-up riêng trước publish/land. Mọi P0–P2 chặn. Owner audit source là AI delegated_owner_audit ở session khác executor, không human_audited hoặc human_exact_head_audit. Target actual-human/enrollment/canary không thay; không tự ký hộ người thật.

Rollback r20/R12 giữ nguyên: ngừng dispatch khi mismatch; không decrement/copyback old journal, không cached legacy writer sau cutover. Revert code chỉ theo exact authority; active journal mismatch cần reconciliation Packet. Source merged/landed chưa đồng nghĩa Packet 1174/Mission 1172complete. Target actual canary/human/lifecycle phải đủ trước activation và đưa PR0/#1166 qua dependency; PR1–PR8/full reference/shadow/rollback vẫn theo graph, chưa triển khai qua việc land adapter.
