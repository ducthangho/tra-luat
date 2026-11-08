dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# WP1174 R13 — Hoàn tất source adapter r20 và native review đầy đủ

- Packet1174 revision13, generation10, Mission1172 revision17, review_class sensitive.
- Mission17 SHA256: 6cb8aa57fa61240fc3f1cc7f661f3ad8d42d9a836d341ad7ff2963a91d5e4194.
- Source executor: codex / openai / codex_service / machine; serving model/effort không đo được.
- Reviewer: anthropic_claude / claude / claude_code / machine/local; yêu cầu Opus5.5/high, serving identity KHONG_DO_DUOC.
- Canonical acceptance baseline c6afde62c846f1ef3d6a83c14459966849edf756, raw27 27fd80803e9a8f80e660752f58c8dd477e9730c8 chỉ đối chiếu lịch sử.
- Metadata P13 parent P12 52b21666e064f2c648555e8ebb377d2a48a12cbe; actual metadata OID được bind sau commit, không fake future SHA.
- Private source predecessor6692082917429bd366f30c5c320a823513f60028, tree628517cff1c3b70770b6fdfd12f81e9f65602322; public PR1275 cònH5.

## 1. Nguồn có hiệu lực và kỹ thuật kế thừa

Chỉ có hiệu lực sau exact C9 decision, installed/readback Mission17, immutable P13 và source authority/lease/I2/doctor/begin thực tế. Metadata approval không là source approval, native verdict hoặc activation.

Design r20 tại ops/specs/wp1174-c5-adapter-design.md bất biến SHA2565a749f921de112565779b8b1e42a2324e8efbc1e5e053d11919d30d8cf20a117, approved design head c172150d64c4fa1382469c81a658410c85aff88d. Toàn r20 là normative, không thay bytes để ghi approval mới.

Mọi yêu cầu kỹ thuật của R12 sections1–6,8,10–14 được incorporated bằng exact immutable file ops/specs/wp1174-implementation-r12.md tại P12, SHA256624f0f5917e555d329efcd46349f60c878667b7b38cf96282bb64a6f5cf232a5. Không bỏ acceptance, negative, oracle, old finding slug hoặc profile. Binding R12/g9/Mission16 và operational budget/review delivery R12 sections7,9 được thay bằng R13/C9 này; các historical verdict/usage vẫn giữ. Reviewer phải đọc assigned normative annex bytes; hash chỉ chứng minh integrity, không thay việc đọc. Coverage union phải phủ đủ mọi incorporated technical section và toàn source.

## 2. Phạm vi source g10 đóng

Whole c6→final đúng5paths, tối đa6000 added, không reanchor/golf/drop IDs:

- .claude/dev/packet_loop.py
- .claude/dev/packet_loop_test.py
- docs/PROTOCOL_DA_PHIEN.md
- ops/specs/wp1174-c5-adapter-design.md
- ops/specs/wp1174-implementation-r13.md

P13 chỉ metadata từP12, không publish source669. Source executor g10 mới chỉ normal merge P13+669, đồng bộ test scoped path r12→r13 và ghi chú composite SOURCE-ONLY trong protocol. Product bắt buộc giữ SHA256ade7bac84b7465ae7bef10b25d10aef0bc8b79d296cb780a1aa6b4afde5848fe. Hai MD frozen tạiP13. Không sửa thêm product/P3, thêm writer/registry, workflow/ruleset/credential/security/release manifest/LIVE. Nếu cần thêm source ngoài việc nêu rõ thì blocked/checkpoint mới.

Giữ normal ancestry H1–H5,196,275,669 và P12/P13; không reset/rebase/force hoặc refund. Current R13 thay tên spec trong final5paths nhưng mọi R12 bytes/history vẫn có trong ancestry. Source mới≤15 phút gồm reads/tools/tests/waits; root có thể sở hữu readonly regression riêng trong shared budget, không kéo dài executor.

## 3. Bất biến thực thi và phép đo

Giữ toàn r20/R12 technical annex: exact authority/installed mission/spec/lease binding, canonical Git no shallow/graft/replace/alternate/injected env, HKDF known-answer/private seed owner-mode-nlink/noFollow, closed core/optional/per-writer fields, fixed lock/no-replace/fsync/readback/tripwire, source high_water/immutable snapshot/recovery/durability và no dispatch trước reserved_for_dispatch. Không đọc/in token/seed/HMAC; project children dùng clean environment không LIVE/Drive/GAS/NLM credentials. Legacy v2/unscoped/golden/ADR0065 không đổi.

Ba H5 blockers vẫn phải được reviewer final xác minh cả class: PushEvent before/after ancestry, zeroOID/missing-object/retention; reused source/target/witness durability dưới khóa trước cutover/finalize/dispatch, terminal replay không rewrite history/counters; recovery immutable source snapshot khớp predecessor high_water/path/generation/revision/Packet/Mission trước mọi probe/temp/write. Imported-v2 controls và initialized-v3 absent/present đều bắt buộc.

Giữ frozen85 IDs, Linux fixture83, native Linux84 và Windows frozen13;14writers+14races=28. Không đổi inventory/controller hoặc làm yếu oracle. Mọi registered mutant OLD/NEW anchors unique, assertion kill đúng predicate, positive/cross-family controls passed; CliSapDo/crash/mismatched-exception không có kill credit. Hai survivor trên275 đã được test-only669 xử lý bằng fresh target chứa đúng initial bytes và multi-anchor cùng class; phải đo lại trên final H, không coi275 fail/stale là finalpass.

## 4. Gate và platform

Trước source publication: exact finalH clean/tree/fivehash/snapshots; diff-check; selftest1777 N/N; ADR64; frozen fixture83; mọi applicable fixture mutants/controls và all meta-anchors; regression460 (r812_,r813_,r1187_,wp1254_); codepage actual cp1252/cp1258 và real-main selection composition; cloud overlay negative/no-write (không nativepositive); root independent counterexamples/holdouts; native cross-provider composite approval; Windows focused13 và raw m1174_allow_windows oracle; independent AI delegated_owner_audit exactH theo r20 source-only override. Không publication khi gate pending/unknown/failed.

Sau qualified publication: automatic Ubuntu CI requiredjobs gate,gate-cong-cu-gop,gate-ops,gate-packet-loop,gate-registry, native Linux84 qua real main trên ext4/XFS và actual WP1174_NATIVE_REPORT_V1 M/H/clone/source tree/filehash/run/attempt/job/producer/snapshot provenance; full Linux M9 exactH; actual connector; canonical K0–K7. Required skipped/not_run/cancelled/timeout/infra/missing/unknown khôngpass. Sau đủ gates và exacthead authority mới normal expected-head merge, hậu-merge checks/readback và bookkeeping/lease closure. Không formal GitHub Review Approve hoặc human signature giả.

Không Windows CI, main/full Windows mutants, registry/project suite hoặc manual ci.yml (runner_set gồmWindows). Chỉ frozen13 baseline/candidate và một raw unit oracle trên owner host đã verify, ưu tiên host đang online phù hợp; không tladmin/ACL bypass/install security. Private bundle SHA/tree/fivehash verify và normal clone/LF/GitHub origin/symbolic ref/clean trước snapshot. Không chiếm process/lock #1124/#564. Offline tối đa10phút rồi chọn route được phép khác hoặc blocked, không chờ ASUS vô hạn. H5/source275/669 gates chỉ lịch sử cho finalH mới.

## 5. Native K4 bằng coverage union có bằng chứng

C8 run eb318a05d06f4f209d3836288df487ca trên275 actualrc0 nhưng verdict blocked vì context coverage, có3P3; không approve, không refund/void, không carry qua head mới. Một context không đọc hết source; R13 thay review delivery một context bằng bốn part reviewers độc lập A/B/C/D rồi integrator E. Assurance vẫn native Claude cross-provider đối với Codex source, cộng independent source owner audit, không global provider/target human exception.

Mỗi part≤15 phút, tối đa2 đồng thời, context mới không fork source; E≤10 phút trong context mới sau cả4 terminal. Tất cả dùng official canonical launcher, same finalH/tree/fivehash/clean readonly checkout, prompt SHA/deadline/read-only restrictions và before/after snapshot. Không project tests, network/secrets/models con, hoặc viết source/plan. Yêu cầu Opus5.5/high nhưng không attested serving identity giả.

Trước dispatch đóng băng coverage manifest bằng byte/line ranges/digests, không cắt function và có boundary overlap. Từng part tự verify Git/head/hashes, đọc COMPLETE current authority package và full R13 này; đọc toàn assigned r20 clauses theo manifest, coverage union phải phủ đủ r20. E đọc full r20. Phân công tối thiểu:

- A: production diff nửa đầu+interfaces; r20 sections1,2,5,8 và R12 technical sections1–3.
- B: production diff nửa sau+interfaces và toàn protocol diff; r20 sections3,4,6,7,9,11 và R12 sections4,14.
- C: test diff nửa đầu+interfaces; r20 section10 và R12 sections5,10,11.
- D: test diff nửa sau+interfaces, native report/schema/producer/Windows; r20 section12 và R12 sections6,8,12,13.

Nếu function hoặc invariant băng qua phần, đọc trọn phần liên quan và khai overlap. Phủ toàn c6→final production/tests/protocol và cả hai MD, cùng tất cả incorporated technical clauses; không lấy bytehash hoặc verdict cũ làm đã đọc. Mỗi raw part report neoH/tree, ranges read-to-EOF, interfaces, findings P1/P2/P3 đầy đủ location/reason/fix/oracle/risk, limits và KET_LUAN cuối stdout. Incomplete coverage hoặc P0–P2 thì part không approve. Mọi P3 phải báo.

E đọc toàn raw A–D reports, coverage manifest và current authority/contracts; tự verify whole diff reconstruction/digests, ranges khônghở, exact head/snapshots/producer/gate trạng thái, và cross-part interfaces; đọc thêm code cần thiết. E chỉ approve khi cả4 part đều đủ và khôngP0–P2, interfaces không mâu thuẫn, mọiP3 được ghi. E khai rõ personal reads và measured coverage union, không giả cá nhân đã đọc hết source. Final composite K4 thực tế là nguồn verdict canonical roundg10; cả5 native calls đều tính chi phí, không che bốn calls bằng nhãn part. Nếu thiếu coverage/context hoặc có blocker, không tự gọi lượt thứ6 trong C9.

## 6. Checkpoint C9 và ngân sách

C9 thêm tối đa6 calls: source1≤15 phút, native4parts×15 phút (parallel≤2) +E≤10 phút. Cumulative source7/native17/connector2; known C6+C7+C8+C9≤27 gồm canary C6 còn1≤10 phút. Prior C2unknown/C3closed/C5closed/C6/C7/C8 và blocked/stale/failed đều giữ; không reset/refund/unknown=0. Per-PR native call cap17 riêngPR1275; final composite1round không xóa actualcalls.

Shared active cap960 phút BAO GỒM toàn bộ đã dùng, supersedes900; công thức51closed+ceil(nowUTC−2026-11-07T16:17:24Z), mọi wait thật. Trước mỗi dispatch used+reserved≤960; hard expiry2026-11-08T08:03:01Z không đổi. CI vẫn9heads/attempts (đã6H5; finalsource7,postmerge8,canary9nếucần), M9 vẫn2runs/24Linux runner-hours (H5run1), Windows5runs/60min/15mỗi run (đã3/26; pair mới chưa dispatch). Không paid purchase/overage/AGY hoặc đổicredential/security/workflow/ruleset/LIVE.

G9 phải quiescent và lease ended/readback, giữ actual old275 blocked journal/counters. P13 metadata exact delegated approval và actual selftest; source authority, actual g10 lease bot/I2/doctor/begin1/1 rồi mới source. Không reuse accepted/stale journal cho head mới. G10 freeze, mọi local/root gates exacthead trước composite; Windows có thể chạy parallel sau localcriticalgates/rootpass nhưng trước publish. Mọi native/meta approval không tự grantsource/land.

## 7. Findings, audit, rollback và completion

Ba P3 của native275 giữ slugs wp1174-r12-human-verifier-path-aba, wp1174-r12-accept-workflow-runs-double-read, wp1174-r12-recheck-status-label. Không tự đóng/carry debt. Final reviewers xét lại severity; nếu cònP3 thì owner disposition exact finalH/slug/reason/follow-up riêng trước publish/land. Mọi P0–P2 chặn. Owner audit source là AI delegated_owner_audit ở session khác executor, không human_audited hoặc human_exact_head_audit. Target actual-human/enrollment/canary không thay; không tự ký hộ người thật.

Rollback r20/R12 giữ nguyên: ngừng dispatch khi mismatch; không decrement/copyback old journal, không cached legacy writer sau cutover. Revert code chỉ theo exactauthority; active journal mismatch cần reconciliation Packet. Source merged/landed chưa đồng nghĩa Packet1174/Mission1172complete. Target actual canary/human/lifecycle phải đủ trước activation và đưa PR0/#1166 qua dependency; PR1–PR8/full reference/shadow/rollback vẫn theo graph, chưa triển khai qua việc land adapter.
