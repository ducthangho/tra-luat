dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# WP1174 R15 — Vá neo KG cũ và hoàn tất gate của adapter r20

- Packet 1174 revision 15, generation 12, Mission 1172 revision 19; sensitive.
- Mission19 SHA256 `44d1f3b19d7bb0652756cca456e8bdd93870b6bddf966305316effbe88f19d8d`. Chỉ có hiệu lực sau exact human C11 decision, installed/readback Mission19, immutable P15, actual g12 lease/bot/I2/doctor/begin.
- Source: Codex / openai / codex_service / machine, actual model/effort chưa đo. Reviewer riêng: Claude Code native, requested Opus 5.5/high, actual serving identity KHONG_DO_DUOC.
- Baseline nghiệm thu bất biến `c6afde62c846f1ef3d6a83c14459966849edf756`; metadata P15 parent P14 `8ab6e20c71714006c033f83311c5c24170bfe46f`; source predecessor C4 `c4d40f84db95666e546f679c1bfc40859b2de8e6`, tree `0fd8088cd32efbe9b354edcc1c82b239c27b3cf3`. Public PR1275 vẫn H5, chưa source publication mới.
- R20 bất biến SHA256 `5a749f921de112565779b8b1e42a2324e8efbc1e5e053d11919d30d8cf20a117`. R12 technical sections1–6,8,10–14 tại P12/SHA256 `624f0f5917e555d329efcd46349f60c878667b7b38cf96282bb64a6f5cf232a5` được incorporated đầy đủ. R15 thay binding/budget/review delivery lịch sử; không bỏ technical acceptance hoặc biến historical verdict thành approval.

## 1. Finding thực tế và nguồn authority

Independent root proof trên exact C4 xác nhận P2 `wp1174-r14-legacy-kg-mutant-anchor-drift`: existing baseline `moc_dot_bien_phai_khop_DUNG_MOT_CHO` AssertionError, bốn KG anchors khớp0 vì `_CHECK_RUNS_PARSE1174` còn dùng Path.read_text cũ trong khi product đã chuyển sang immutable snapshot. Bốn IDs: kg_bo_hook_khoa_trung, kg_bo_hook_hang_ngoai_json, kg_r3_nested_suite_duplicates_ignored, kg_r3_extra_key_duplicates_ignored. Positive control `moc_kiem_TU_NO_co_rang` passed. Proof wrapper rc0 nghĩa xác nhận failure, không code gate pass.

C4 exact local fixture83,236 mutants/controls,237 WP1174 anchors, ADR64, selftest1777, regression460 retry, codepages2, independent17 và topology10 đạt; global anchor baseline vẫn đỏ nên C4 chưa được publish. First regression timeout360sec/-15, stale bfbb selftest/-15, failed inspection/anchor attempts và source outer exec rc unknown đều giữ. Source8 ended05:40:32; subsequent test collection là root read-only, không source extension.

C10 đã dùng source8 và không gọi native trên C4; năm native contexts chưa dùng đóng unused, không refund hoặc ẩn chi phí. Chưa thêm Windows/CI/M9. R15 chỉ được thi công sau exact C11 human MCR decision theo protocol §3.1; standing land grant không tự là exact MCR approval.

## 2. Scope và continuation đóng

P15 chỉ metadata, normal descendant P14; thay current contract MD r14 bằng r15, r20 giữ bytes. Source g12 context mới normal merge P15+C4, giữ toàn ancestry H1–H5/196/275/669/H53/C4/P12/P13/P14/P15, không reset/rebase/force/drop. Whole c6→final đúng5paths/+≤6000:

- .claude/dev/packet_loop.py
- .claude/dev/packet_loop_test.py
- docs/PROTOCOL_DA_PHIEN.md
- ops/specs/wp1174-c5-adapter-design.md
- ops/specs/wp1174-implementation-r15.md

Trong source call9≤15 phút, product packet_loop.py READ-ONLY, bắt buộc SHA256 `0e356754a8919e3bc1ee946f18580ecdb88cdd8771d0b6536dc97b71eddc6dc4`. Chỉ sửa test `_CHECK_RUNS_PARSE1174` thành anchor đủ hẹp khớp đúng actual immutable-snapshot parser; giữ đúng semantic của cả4 legacy mutants, targets và controls. Đồng bộ scoped spec path r14→r15 và source-only protocol binding. Hai MD frozen. Không thêm P3/product fixes hoặc tắt/skip global baseline, mutant hay acceptance; không đổi IDs/controller/inventory. Hint phải tự tái dẫn xuất và khai provenance nếu dùng.

Prepublication thêm mandatory global `moc_dot_bien_phai_khop_DUNG_MOT_CHO` trên toàn registry và adversarial checker positive control, cùng cả4 KG mutants assertion kills/controls khỏe. Kiểm OLD+NEW anchors đúng1, không chỉ subset WP1174. Existing237 WP1174/236 fixture mutants và frozen85/83/84/13,14writers+14races giữ nguyên. Không coi CLI crash hoặc mismatched exception là kill.

Hai lớp P2 R13 đã sửa ở C4 là regression obligations, không scope để sửa product: cả nullable lineage.source_path và enrollment.legacy_source_path canonical/lexical/exact mount trước lock và readmission dưới lock, initial_state_path giữ; foreign device/same-device mount_id/symlink/lexical negatives no-write, same-mount imported-v2 và latest-adopted initialized-v3 controls. Secret-channel oracle kiểm concrete fixture seed/derived key vắng mặt trong A/S/stdout/stderr/tracebacks/native facts/native report/Windows serializer, named leak mutant và controls đúng. Windows-only unit không được chạy từ Linux helper; serializer fixture không là native-Windows unit proof.

## 3. Bất biến thực thi và phép đo

Giữ toàn r20/R12 technical annex: exact authority/installed mission/spec/lease binding, canonical Git no shallow/graft/replace/alternate/injected env, HKDF known-answer/private seed owner-mode-nlink/noFollow, closed core/optional/per-writer fields, fixed lock/no-replace/fsync/readback/tripwire, source high_water/immutable snapshot/recovery/durability và no dispatch trước reserved_for_dispatch. Không đọc/in token/seed/HMAC; project children dùng clean environment không LIVE/Drive/GAS/NLM credentials. Legacy v2/unscoped/golden/ADR0065 không đổi.

Ba H5 blockers vẫn phải được reviewer final xác minh cả class: PushEvent before/after ancestry, zeroOID/missing-object/retention; reused source/target/witness durability dưới khóa trước cutover/finalize/dispatch, terminal replay không rewrite history/counters; recovery immutable source snapshot khớp predecessor high_water/path/generation/revision/Packet/Mission trước mọi probe/temp/write. Imported-v2 controls và initialized-v3 absent/present đều bắt buộc.

Giữ frozen 85 IDs, Linux fixture 83, native Linux 84 và Windows frozen 13;14 writers+14 races=28. Không đổi inventory/controller hoặc làm yếu oracle. Mọi registered mutant OLD/NEW anchors unique, assertion kill đúng predicate, positive/cross-family controls passed; CliSapDo/crash/mismatched-exception không có kill credit. Hai survivor trên 275 đã được test-only669 xử lý bằng fresh target chứa đúng initial bytes và multi-anchor cùng class; phải đo lại trên final H, không coi275 fail/stale là final pass.

## 4. Gate và platform

Trước source publication: exact final H clean/tree/fivehash/snapshots; diff-check; selftest 1777 N/N; ADR 64; frozen fixture 83; mọi applicable fixture mutants/controls và all meta-anchors; regression 460 (r812_,r813_,r1187_,wp1254_); codepage actual cp1252/cp1258 và real-main selection composition; cloud overlay negative/no write (không nativepositive); root independent counterexamples/holdouts; native cross-provider composite approval; Windows focused13 và raw m1174_allow_windows oracle; independent AI delegated_owner_audit exact H theo r20 source only override. Không publication khi gate pending/unknown/failed.

Sau qualified publication: automatic Ubuntu CI requiredjobs gate,gate-cong-cu-gop,gate-ops,gate-packet-loop,gate-registry, native Linux 84 qua real main trên ext4/XFS và actual WP1174_NATIVE_REPORT_V1 M/H/clone/source tree/filehash/run/attempt/job/producer/snapshot provenance; full Linux M9 exact H; actual connector; canonical K0–K7. Required skipped/not_run/cancelled/timeout/infra/missing/unknown không pass. Sau đủ gates và exact head authority mới normal expected-head merge, hậu-merge checks/readback và bookkeeping/lease closure. Không formal GitHub Review Approve hoặc human signature giả.

Không Windows CI, main/full Windows mutants, registry/project suite hoặc manual ci.yml (runner_set gồmWindows). Chỉ frozen 13 baseline/candidate và một raw unit oracle trên owner host đã verify, ưu tiên host đang online phù hợp; không tladmin/ACL bypass/install security. Private bundle SHA/tree/fivehash verify và normal clone/LF/GitHub origin/symbolic ref/clean trước snapshot. Không chiếm process/lock #1124/#564. Offline tối đa10 phút rồi chọn route được phép khác hoặc blocked, không chờ ASUS vô hạn. H5/source 275/669 gates chỉ lịch sử cho final H mới.

## 5. Native K4 bằng coverage union có bằng chứng

C8 run eb318a05d06f4f209d3836288df487ca trên 275 actual rc0 nhưng verdict blocked vì context coverage, có3 P3; không approve, không refund/void, không carry qua head mới. Một context không đọc hết source; R15 thay review delivery một context bằng bốn part reviewers độc lập A/B/C/D rồi integrator E. Assurance vẫn native Claude cross-provider đối với Codex source, cộng independent source owner audit, không global provider/target human exception.

Mỗi part≤15 phút, tối đa2 đồng thời, context mới không fork source; E≤10 phút trong context mới sau cả 4 terminal. Tất cả dùng official canonical launcher, same final H/tree/fivehash/clean readonly checkout, prompt SHA/deadline/read-only restrictions và before/after snapshot. Không project tests, network/secrets/models con, hoặc viết source/plan. Yêu cầu Opus5.5/high nhưng không attested serving identity giả.

Trước dispatch đóng băng coverage manifest bằng byte/line ranges/digests, không cắt function và có boundary overlap. Từng part tự verify Git/head/hashes, đọc COMPLETE current authority package và full R15 này; đọc toàn assigned r20 clauses theo manifest, coverage union phải phủ đủ r20. E đọc full r20. Phân công tối thiểu:

- A: production diff nửa đầu+interfaces; r20 sections1,2,5,8 và R12 technical sections1–3.
- B: production diff nửa sau+interfaces và toàn protocol diff; r20 sections3,4,6,7,9,11 và R12 sections4,14.
- C: test diff nửa đầu+interfaces; r20 section10 và R12 sections5,10,11.
- D: test diff nửa sau+interfaces, native report/schema/producer/Windows; r20 section12 và R12 sections6,8,12,13.

Nếu function hoặc invariant băng qua phần, đọc trọn phần liên quan và khai overlap. Phủ toàn c6→final production/tests/protocol và cả hai MD, cùng tất cả incorporated technical clauses; không lấy bytehash hoặc verdict cũ làm đã đọc. Mỗi raw part report neoH/tree, ranges read to EOF, interfaces, findings P1/P2/P3 đầy đủ location/reason/fix/oracle/risk, limits và KET_LUAN cuối stdout. Incomplete coverage hoặc P0–P2 thì part không approve. Mọi P3 phải báo.

E đọc toàn raw A–D reports, coverage manifest và current authority/contracts; tự verify whole diff reconstruction/digests, ranges khônghở, exact head/snapshots/producer/gate trạng thái, và cross-part interfaces; đọc thêm code cần thiết. E chỉ approve khi cả 4 part đều đủ và không P0–P2, interfaces không mâu thuẫn, mọi P3 được ghi. E khai rõ personal reads và measured coverage union, không giả cá nhân đã đọc hết source. Final composite K4 thực tế là nguồn verdict canonical round g11; cả 5 native calls đều tính chi phí, không che bốn calls bằng nhãn part. Nếu thiếu coverage/context hoặc có blocker, không tự gọi lượt thứ6 trong C11.

## 6. Checkpoint C11 và ngân sách có giới hạn

Chỉ sau exact human approval: thêm source call9≤15 phút và5 fresh native contexts A–D≤15 phút/part, E≤10 phút, tối đa2 song song. Cumulative source9/native21/connector2/canary1 cộng2 independent scratch roles =35 calls. Actual trước C11: source8/native16/connector1/canary0/scratch2. Năm native chưa dùng trong C10 đóng unused, không giả đã dùng hoặc refund; C11 cấp mới tối đa5 nhưng cumulative native cap vẫn21. Không tiếp tục source8 sau terminal hoặc reset g11 journal. G12 local1attempt/1review chỉ bootstrap source, clamped bằng global usage; không candidate v3 tự cấp quyền. Đầu source chỉ khi g11 quiescent/end và actual g12 lease/bot/I2/doctor/begin.

Shared cloud cap1150 phút BAO GỒM toàn bộ đã dùng, thay995, hard expiry `2026-11-08T11:03:01Z` thay08:03:01. Công thức51 + ceil((now UTC−2026-11-07T16:17:24Z)/60). Mọi wait tính thật; trước mỗi admission ghi used/reserved/limit. Reservation250 phút gồm metadata/lease15 + source15 + local read-only15 + native composite40 + CI/M9/postmerge150 + canary10 + bookkeeping5. Windows focused pair tối đa30 phút có thể chạy song song với native40, không cộng hai lần nhưng vẫn giữ actual Windows minutes. Tại 2026-11-08T05:59:03.684787+00:00, used=873, total forecast=1123, cap1150; chỉ dispatch nếu phép đo mới vẫn feasible. Không coi pending/timeout/infra/notrun là pass để fit budget, không tự giảm forecast khi chưa có số đo.

CI giữ9 heads/attempts, đã6; full Linux M9 giữ2 runs/24 runner-hours, đã1; Windows giữ5 runs/60 phút, đã3/26, mỗi run≤15 phút, chỉ remaining pair frozen13 + một unit oracle. Không Windows CI/main/full mutant/project suite, không AGY hoặc paid credits/overage/purchases, không workflow/global/security/credential change. Hai MD và product frozen. Fresh final head phải đo lại các gate, không carry C4 pass sang head mới. Chỉ publication khi mọi prepush gate đủ, actual native composite approve và independent delegated_owner_audit exact H; sau đó actual CI/native84/M9/connector/K0–K7, owner exact-head land authority, normal expected-head merge và postmerge/readback. Không formal GitHub Approve.

Blocker mới P0–P2, source/native cap hết hoặc deadline/reservation infeasible thì checkpoint/handoff, không tự gọi thêm. P3 chỉ exact-head disposition với slug/reason/follow-up theo quyền chủ kho đã cho. Source-only AI audit khác Executor giữ đúng nhãn delegated_owner_audit; target actual-human/canary và PR0–PR8 dependency/acceptance không thay.

## 7. Findings, audit, rollback và completion

Bảy P3 phải được fresh reviewer xét lại, không tự đóng hoặc đổi severity: wp1174-r12-human-verifier-path-aba; wp1174-r12-accept-workflow-runs-double-read; wp1174-r12-recheck-status-label; wp1174-r13-git-env-denylist-graft; wp1174-r13-f6-closed-errors-host-traceability; wp1174-r13-f7-wrong-type-stimulus-absent; wp1174-r13-water-identity-direct-call. Giữ aliases cũ. Mission17 routing-history/graph omission đã được sửa bằng Mission18 và Mission19 kế thừa; đây là metadata closure có bằng chứng, không phải product bypass.

Ba P3 của native 275 giữ slugs wp1174-r12-human-verifier-path-aba, wp1174-r12-accept-workflow-runs-double-read, wp1174-r12-recheck-status-label. Không tự đóng/carry debt. Final reviewers xét lại severity; nếu cònP3 thì owner disposition exact final H/slug/reason/follow-up riêng trước publish/land. Mọi P0–P2 chặn. Owner audit source là AI delegated_owner_audit ở session khác executor, không human_audited hoặc human_exact_head_audit. Target actual-human/enrollment/canary không thay; không tự ký hộ người thật.

Rollback r20/R12 giữ nguyên: ngừng dispatch khi mismatch; không decrement/copyback old journal, không cached legacy writer sau cutover. Revert code chỉ theo exact authority; active journal mismatch cần reconciliation Packet. Source merged/landed chưa đồng nghĩa Packet 1174/Mission 1172complete. Target actual canary/human/lifecycle phải đủ trước activation và đưa PR0/#1166 qua dependency; PR1–PR8/full reference/shadow/rollback vẫn theo graph, chưa triển khai qua việc land adapter.
