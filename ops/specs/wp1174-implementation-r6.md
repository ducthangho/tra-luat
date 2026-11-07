dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# WP1174 r6 — Thi công adapter theo thiết kế r20

- packet_id: WP1174; revision: 6;
- mission_issue: 1172; mission_revision: 10; mission_plan_sha256: edd5ba06259bbe5949dc548c364a21ef45911b612cf22c9ee4ac111b77f892cc
- contract_id: WP1174-r6-C6; generation: 5; review_class: sensitive
- executor: codex; execution_surface: codex_service; model_family: openai; transport: machine
- source reviewer: claude; execution_surface: claude_code; model_family: claude; transport: machine/local
- immutable_acceptance_baseline: 08bcb51fbed359eaeeca41bc3a0559fe308c0aa9
- metadata_parent: b24fc6333bd106a3413f4a007d411997908be32e; code continuation là exact metadata commit chứa spec này, ghi ở lease sau khi commit có OID

## 1. Hiệu lực, nguồn và outcome

Đây là hợp đồng trình duyệt. Chỉ có hiệu lực sau owner duyệt exact bundle, cài/readback Mission r10, publish metadata immutable và lease exclusive hợp lệ. Chưa source work/grant/CI/activation qua việc tạo file này.

Design normative là ops/specs/wp1174-c5-adapter-design.md, bytes SHA256 5a749f921de112565779b8b1e42a2324e8efbc1e5e053d11919d30d8cf20a117 tại design head c172150d64c4fa1382469c81a658410c85aff88d; native Claude review technical approve, 0 P1/P2/P3 ở #1174 comment6679977538. Không đổi bytes r20 để ghi source approval. Metadata contract r6 không tự nhận approval r20 trên SHA mới.

Outcome: hiện thực r20 trong packet-loop, giữ legacy ngoài scope; chứng minh admission/init/lease/advisory review/actual-human/accept và source/high_water/recovery bằng đúng profile. Adapter hỗ trợ Mission #1172/registered Packets theo authority canonical, không activate route toàn kho, không generic controller/registry.

## 2. Phạm vi đóng và drift

Write set exact, cũng là effective set CHỈ sau khi owner duyệt scoped manual closure exception:
- .claude/dev/packet_loop.py
- .claude/dev/packet_loop_test.py
- docs/PROTOCOL_DA_PHIEN.md
- ops/specs/wp1174-c5-adapter-design.md
- ops/specs/wp1174-implementation-r6.md

Không workflow, ruleset, credential, launcher, release manifest, ADR0041/0045 hoặc code Packet khác. New helper writer command thứ15 bị cấm. Giữ13mutator + adopt-state (2mode cùngcommand), guard-first-publication read-only. Canonical ADR0065 và URL-human identity delta ở base mới phải giữ; không cherry-pick code C5 cũ đè lên canonical.

R20 review base 825eb3561a94e05c36045d2c981b4108c523e31c khác source base này. Drift đã đọc: packet_loop 8 dòng, tests 119 dòng, protocol 17 dòng, ADR0065; source full diff đo từ 08bcb51fbed359eaeeca41bc3a0559fe308c0aa9, không đo từ H rework mới để giấu scope. Metadata parent merge chỉ mang r20MD vào nền canonical; chưa product source changes.

## 3. Bootstrap và P→H

1. Sau owner C6 approval, metadata ref ops/spec-wp1174-r6 được publish đúng candidate metadata commit của bundle, không product code. Authority là quyết định owner, không file candidate tự cấp. Canonical ADR0063 cho spec_ref immutable; ledger C2/C3/C5 giữ nguyên.
2. Fresh all-ref/normalized+symlink/prefix overlap check, actor allowlist+maintain proof và lease publication/readback phải đạt trước source. Bootstrap dùng canonical v2 codex_service/claude_code lane đã probe fixture init rc0→awaiting_lease, begin nolease rc8; không dùng r20 candidate để tự record/accept.
3. P là exact metadata commit mới chứa r20+contract r6, reviewed độc lập native Claude TRƯỚC first publish PR branch; P có giá trị documentation/contract độc lập, không activate behavior. P review tính đủ1round/1call. Tạo draft PR từ P sau gates để có PRID.
4. Executor cùng Packet tạo H từ P; native source review trọn base→H, không chỉ P→H. Windows focused và gates địa phương exact H trước push. Nếu rework thì H mới/review mới; Giữ P r2/r3/r4 rounds 1/2/3 đã dùng; P r5 round 4 đã dùng; P r6 round 5, H và một H rework trong trần mới. Không reset lịch sử. Coordinator ghi checkpoint hữu hạn theo ủy quyền owner thay vì hỏi lại.
5. Actual owner human audit schema v1 cho PRID/H/tree/spec/revision/gen TRƯỚC first publication H. Agent repost không phải human audit. CLI/source-native receipts khai đúng serving/sandbox/provider. K4 native và human truyền cùng thì cả hai phải hợp lệ. Giữ canonical human timing/URL identity, earliest remote run đầy đủ; candidate guard chỉ là code được test, không tự cấp source authority.
6. Controlled publish H một lần chính theo M5; automatic Ubuntu CI, Linux full M9 applicable, connector draft review và K0-K7 canonical. Formal GitHub Approve/land authorization exact H cần owner riêng ở thời điểm đó. Chưa grant trong C6.
7. Chỉ sau land/readback mới canary target route bằng canonical đã land, descriptor/grant thật, native Linux profile đã đo và **một phiên Codex service reviewer mới**, actual human K4 thật. Reserved canary call không phải code-review approval và không được fake CLI. Thiếu host/grant/human/budget thì canary blocked, #1174 chưa complete và PR0 chưa tiếp nhận.

## 4. Source predicates / transactions

Hiện thực nguyên invariants r20: immutable descriptor/resolver, closed witness+pending+history bytes, exact fresh image, pre/postimage validator mọi 9 action, fixed lock/O_CLOEXEC, no-replace publish, high_water cặp state+witness, source initialized active path/gen/v3/revision/hash exact high_water; imported legacy chỉ đúng branch; recovery immutable snapshot sau tombstone. Mọi validation biết tại entry phải trước write; I/O fail/no dispatch; state/witness ordinary mismatch terminal UNKNOWN. Không rollback counters, không gọi cachedv2 writer đã fence khi chưa quiescence.

Không chia source state/quota control giữa các worker. Không provider dispatch nếu rc0 đơn lẻ; chỉ rc0+reserved_for_dispatch+dispatch_allowed=true sau durability/tripwire. No-op replay no-write/no-slot. Win/NFS/SMB/overlay/unknown không claim supported runtime. Native Linux positive phải ext4/XFS measured, fsyncdir/link/lock probes; Cloud hiện dùng overlay: được chạy thuật toán trong fixture test tách biệt theo §5.1 và test từ chối profile thật; không được claim production profile hoặc activation.

## 5. Inventory frozen và focused runner

InventoryJSON SHA256 fd2cfe34775a102517245ffd9a870732328860c1cfd1fa36286dab007bfde572; 85 ID duy nhất dưới đây (giữ nguyên 83 ID cũ và thêm 2 ID harness). Đây là ID yêu cầu phải hiện thực, hiện NOT_RUN. Mỗi reject cần negative/mutant và positive/crossfamily control; non-assertion crash không kill credit. 28finding ID C5 nối với nhóm tương ứng, không thay tên/xóa lịch sử. Static named call graph13writers phải so với runtime14entry tests và gate helper; không claim bảo vệ arbitrary private write.

| ID | Platform | Stimulus | Expected | Mutation oracle |
|---|---|---|---|---|
| wp1174_admission_valid | both | immutable descriptor + current authority + scoped grant đúng | accept input only; no source/dispatch authority | m1174_reject_valid_admission |
| wp1174_admission_file_bytes | linux | FILE khác immutable bytes | rc8 trước write; guard rc12/admission_rejected | m1174_drop_file_bytes |
| wp1174_admission_oid_path_hash | linux | OID/path/hash sai | rc8 trước write; guard rc12/admission_rejected | m1174_drop_oid_path_hash |
| wp1174_admission_expired_revoked | linux | expired hoặc revoked dù hash đúng | rc8 trước write; guard rc12/admission_rejected | m1174_drop_expired_revoked |
| wp1174_admission_candidate_root | linux | descriptor chỉ do candidate/caller tự khai | rc8 trước write; guard rc12/admission_rejected | m1174_drop_candidate_root |
| wp1174_admission_wrong_scope | both | Mission/Packet/revision/generation sai | rc8 trước write; guard rc12/admission_rejected | m1174_drop_wrong_scope |
| wp1174_admission_unresolved | linux | authority/spec không resolve hoặc page thiếu | rc8 trước write; guard rc12/admission_rejected | m1174_drop_unresolved |
| wp1174_witness_valid | both | valid canonical bytes + grant + cross-field row | validate pass, chưa cấp dispatch | m1174_reject_valid_witness |
| wp1174_witness_keyset | both | extra/missing top-level key; pending absent != null | wrong combo rc8/UNKNOWN/no write; import_retry valid positive | m1174_drop_witness_keyset |
| wp1174_witness_int_bool | both | bool/float ở mọi integer | wrong combo rc8/UNKNOWN/no write; import_retry valid positive | m1174_drop_witness_int_bool |
| wp1174_witness_enum_hash | linux | origin/phase enum hoặc hex64 sai | wrong combo rc8/UNKNOWN/no write; import_retry valid positive | m1174_drop_witness_enum_hash |
| wp1174_witness_json_bytes | both | duplicate keys/NaN/noncanonical UTF8/BOM/LF | wrong combo rc8/UNKNOWN/no write; import_retry valid positive | m1174_drop_witness_json_bytes |
| wp1174_witness_fresh_reserved | both | fresh reserved phải exact image rev0 | wrong combo rc8/UNKNOWN/no write; import_retry valid positive | m1174_drop_witness_fresh_reserved |
| wp1174_witness_import_retry | both | imported reserved aborted history + pending mới | wrong combo rc8/UNKNOWN/no write; import_retry valid positive | m1174_drop_witness_import_retry |
| wp1174_witness_suspended | both | suspended không khớp node cuối | wrong combo rc8/UNKNOWN/no write; import_retry valid positive | m1174_drop_witness_suspended |
| wp1174_witness_active_pending | both | active/last adopted/high_water/pending generation sai | wrong combo rc8/UNKNOWN/no write; import_retry valid positive | m1174_drop_witness_active_pending |
| wp1174_init_fresh | linux | predecessor none + witness/target absent + absent sentinel | reserved→target awaiting_lease→initialized; counters từ grant; no dispatch | m1174_init_skip_witness |
| wp1174_init_preflight | linux | foreign target/symlink/witness existing/bad grant | preflight reject giữ bytes; valid resume tạo/advance đúng; missing initialized terminal UNKNOWN | m1174_init_preflight |
| wp1174_init_resume_absent | linux | reserved exact image + target absent | preflight reject giữ bytes; valid resume tạo/advance đúng; missing initialized terminal UNKNOWN | m1174_init_resume_absent |
| wp1174_init_resume_full | linux | reserved exact image + target exact full bytes | preflight reject giữ bytes; valid resume tạo/advance đúng; missing initialized terminal UNKNOWN | m1174_init_resume_full |
| wp1174_init_resume_mismatch | linux | reserved + target sai bytes; initialized+missing target | preflight reject giữ bytes; valid resume tạo/advance đúng; missing initialized terminal UNKNOWN | m1174_init_resume_mismatch |
| wp1174_writer_init | linux | init qua shared gate; init/adopt dùng namespace management | mỗi command đúng branch/revision/authority; no bypass _save | m1174_ungate_init |
| wp1174_race_init | linux | init tranh lock với record-codex-call | không lost update/double reservation; stale rc8/quota rc3; no auto retry | m1174_unlock_init |
| wp1174_writer_record_lease | linux | record-lease qua shared gate; init/adopt dùng namespace management | mỗi command đúng branch/revision/authority; no bypass _save | m1174_ungate_record_lease |
| wp1174_race_record_lease | linux | record-lease tranh lock với record-codex-call | không lost update/double reservation; stale rc8/quota rc3; no auto retry | m1174_unlock_record_lease |
| wp1174_writer_begin_attempt | linux | begin-attempt qua shared gate; init/adopt dùng namespace management | mỗi command đúng branch/revision/authority; no bypass _save | m1174_ungate_begin_attempt |
| wp1174_race_begin_attempt | linux | begin-attempt tranh lock với record-codex-call | không lost update/double reservation; stale rc8/quota rc3; no auto retry | m1174_unlock_begin_attempt |
| wp1174_writer_void_attempt | linux | void-attempt qua shared gate; init/adopt dùng namespace management | mỗi command đúng branch/revision/authority; no bypass _save | m1174_ungate_void_attempt |
| wp1174_race_void_attempt | linux | void-attempt tranh lock với record-codex-call | không lost update/double reservation; stale rc8/quota rc3; no auto retry | m1174_unlock_void_attempt |
| wp1174_writer_record_review | linux | record-review qua shared gate; init/adopt dùng namespace management | mỗi command đúng branch/revision/authority; no bypass _save | m1174_ungate_record_review |
| wp1174_race_record_review | linux | record-review tranh lock với record-codex-call | không lost update/double reservation; stale rc8/quota rc3; no auto retry | m1174_unlock_record_review |
| wp1174_writer_transition | linux | transition qua shared gate; init/adopt dùng namespace management | mỗi command đúng branch/revision/authority; no bypass _save | m1174_ungate_transition |
| wp1174_race_transition | linux | transition tranh lock với record-codex-call | không lost update/double reservation; stale rc8/quota rc3; no auto retry | m1174_unlock_transition |
| wp1174_writer_record_codex_call | linux | record-codex-call qua shared gate; init/adopt dùng namespace management | mỗi command đúng branch/revision/authority; no bypass _save | m1174_ungate_record_codex_call |
| wp1174_race_record_codex_call | linux | record-codex-call tranh lock với record-codex-call | không lost update/double reservation; stale rc8/quota rc3; no auto retry | m1174_unlock_record_codex_call |
| wp1174_writer_nang_tran | linux | nang-tran qua shared gate; init/adopt dùng namespace management | mỗi command đúng branch/revision/authority; no bypass _save | m1174_ungate_nang_tran |
| wp1174_race_nang_tran | linux | nang-tran tranh lock với record-codex-call | không lost update/double reservation; stale rc8/quota rc3; no auto retry | m1174_unlock_nang_tran |
| wp1174_writer_record_rescue | linux | record-rescue qua shared gate; init/adopt dùng namespace management | mỗi command đúng branch/revision/authority; no bypass _save | m1174_ungate_record_rescue |
| wp1174_race_record_rescue | linux | record-rescue tranh lock với record-codex-call | không lost update/double reservation; stale rc8/quota rc3; no auto retry | m1174_unlock_record_rescue |
| wp1174_writer_record_post | linux | record-post qua shared gate; init/adopt dùng namespace management | mỗi command đúng branch/revision/authority; no bypass _save | m1174_ungate_record_post |
| wp1174_race_record_post | linux | record-post tranh lock với record-codex-call | không lost update/double reservation; stale rc8/quota rc3; no auto retry | m1174_unlock_record_post |
| wp1174_writer_accept | linux | accept qua shared gate; init/adopt dùng namespace management | mỗi command đúng branch/revision/authority; no bypass _save | m1174_ungate_accept |
| wp1174_race_accept | linux | accept tranh lock với record-codex-call | không lost update/double reservation; stale rc8/quota rc3; no auto retry | m1174_unlock_accept |
| wp1174_writer_mo_lai | linux | mo-lai qua shared gate; init/adopt dùng namespace management | mỗi command đúng branch/revision/authority; no bypass _save | m1174_ungate_mo_lai |
| wp1174_race_mo_lai | linux | mo-lai tranh lock với record-codex-call | không lost update/double reservation; stale rc8/quota rc3; no auto retry | m1174_unlock_mo_lai |
| wp1174_writer_chu_kho_duyet | linux | chu-kho-duyet qua shared gate; init/adopt dùng namespace management | mỗi command đúng branch/revision/authority; no bypass _save | m1174_ungate_chu_kho_duyet |
| wp1174_race_chu_kho_duyet | linux | chu-kho-duyet tranh lock với record-codex-call | không lost update/double reservation; stale rc8/quota rc3; no auto retry | m1174_unlock_chu_kho_duyet |
| wp1174_writer_adopt_state | linux | adopt-state qua shared gate; init/adopt dùng namespace management | mỗi command đúng branch/revision/authority; no bypass _save | m1174_ungate_adopt_state |
| wp1174_race_adopt_state | linux | adopt-state tranh lock với record-codex-call | không lost update/double reservation; stale rc8/quota rc3; no auto retry | m1174_unlock_adopt_state |
| wp1174_adopt_entry_preflight | linux | source/identity/lstat collision trước pending | đúng r20 state table; no reset/overwrite/dispatch; invalid entry unchanged | m1174_adopt_entry_preflight |
| wp1174_adopt_import_first | linux | imported witness first bytes đã có full pending | đúng r20 state table; no reset/overwrite/dispatch; invalid entry unchanged | m1174_adopt_import_first |
| wp1174_adopt_resume_no_target | linux | pending đúng ID + target absent + intent false | đúng r20 state table; no reset/overwrite/dispatch; invalid entry unchanged | m1174_adopt_resume_no_target |
| wp1174_adopt_intent_cutover | linux | witness intent durable→prepared intent→tombstone | đúng r20 state table; no reset/overwrite/dispatch; invalid entry unchanged | m1174_adopt_intent_cutover |
| wp1174_adopt_abandon_prepare | linux | pending/no target → aborted_intent | đúng r20 state table; no reset/overwrite/dispatch; invalid entry unchanged | m1174_adopt_abandon_prepare |
| wp1174_adopt_abandon_cutover | linux | prepared→aborted target→witness; crash mọi cutpoint | đúng r20 state table; no reset/overwrite/dispatch; invalid entry unchanged | m1174_adopt_abandon_cutover |
| wp1174_adopt_retry | linux | aborted retained; new admission/gen/id/path, suspended retained | đúng r20 state table; no reset/overwrite/dispatch; invalid entry unchanged | m1174_adopt_retry |
| wp1174_adopt_finalize_replay | linux | adopted+pending finalize; terminal replay no write | đúng r20 state table; no reset/overwrite/dispatch; invalid entry unchanged | m1174_adopt_finalize_replay |
| wp1174_adopt_postimage_all | linux | 9 writer actions + init advance: reject bad proposed image before any write | đúng r20 state table; no reset/overwrite/dispatch; invalid entry unchanged | m1174_adopt_postimage_all |
| wp1174_adopt_fresh_reserved_adopt | linux | fresh reserved + valid adopt admission | đúng r20 state table; no reset/overwrite/dispatch; invalid entry unchanged | m1174_adopt_fresh_reserved_adopt |
| wp1174_source_active_positive | linux | source active path/v3/gen/revision/full hash == high_water | positive proceeds; mismatch rc8 unchanged/no pending; recovery phase-aware | m1174_source_active_positive |
| wp1174_source_backup | linux | backup cũ được admission ghim hash | positive proceeds; mismatch rc8 unchanged/no pending; recovery phase-aware | m1174_source_backup |
| wp1174_source_ahead | linux | state-ahead sau ordinary crash | positive proceeds; mismatch rc8 unchanged/no pending; recovery phase-aware | m1174_source_ahead |
| wp1174_source_foreign_path | linux | same bytes nhưng source path khác active | positive proceeds; mismatch rc8 unchanged/no pending; recovery phase-aware | m1174_source_foreign_path |
| wp1174_source_generation_revision | linux | predecessor/source gen/revision khác witness | positive proceeds; mismatch rc8 unchanged/no pending; recovery phase-aware | m1174_source_generation_revision |
| wp1174_source_legacy_branch | linux | legacy v2 chỉ absent/imported reserved; cấm bypass v3 | positive proceeds; mismatch rc8 unchanged/no pending; recovery phase-aware | m1174_source_legacy_branch |
| wp1174_source_recovery_snapshot | linux | sau tombstone kiểm immutable source snapshot + predecessor high_water | positive proceeds; mismatch rc8 unchanged/no pending; recovery phase-aware | m1174_source_recovery_snapshot |
| wp1174_durability_ordinary_pair | linux | state persist xong nhưng witness chưa advance | no dispatch; ordinary mismatch terminal UNKNOWN; không gọi cached writer đã fence | m1174_durable_ordinary_pair |
| wp1174_durability_fsync_readback | linux | fsync/file/dir/replace/readback lỗi | no dispatch; ordinary mismatch terminal UNKNOWN; không gọi cached writer đã fence | m1174_durable_fsync_readback |
| wp1174_durability_publish_noreplace | linux | kill trước/sau link witness/target; EEXIST | no dispatch; ordinary mismatch terminal UNKNOWN; không gọi cached writer đã fence | m1174_durable_publish_noreplace |
| wp1174_durability_legacy_tombstone | linux | golden product bytes qua đủ13legacy CLI, rc8 + bytes unchanged | no dispatch; ordinary mismatch terminal UNKNOWN; không gọi cached writer đã fence | m1174_durable_legacy_tombstone |
| wp1174_durability_cached_writer | linux | cached v2 private _save tái ghi; quiescence thiếu | no dispatch; ordinary mismatch terminal UNKNOWN; không gọi cached writer đã fence | m1174_durable_cached_writer |
| wp1174_lifecycle_identity_advisory | linux | service provider/surface/session/serving unknown khai thật | canonical bindings và r20 semantics; không fake native/human/acceptance | m1174_lifecycle_identity_advisory |
| wp1174_lifecycle_budget_replay | linux | expired/stale/replayed reservation; C2 unknown không cấp dư | canonical bindings và r20 semantics; không fake native/human/acceptance | m1174_lifecycle_budget_replay |
| wp1174_lifecycle_human_valid | linux | actual owner raw schema v1 + exact PR/H/tree/spec | canonical bindings và r20 semantics; không fake native/human/acceptance | m1174_lifecycle_human_valid |
| wp1174_lifecycle_human_negative | linux | agent repost/wrong owner/head/timing/page missing | canonical bindings và r20 semantics; không fake native/human/acceptance | m1174_lifecycle_human_negative |
| wp1174_lifecycle_first_publication | linux | earliest ref/ancestor/activity bounded; FAIL/UNKNOWN khác PASS | canonical bindings và r20 semantics; không fake native/human/acceptance | m1174_lifecycle_first_publication |
| wp1174_lifecycle_guard_readonly | linux | guard-first-publication no state/provider writes; closed rc table | canonical bindings và r20 semantics; không fake native/human/acceptance | m1174_lifecycle_guard_readonly |
| wp1174_lifecycle_scoped_lifecycle | linux | fixture admission→init→lease→review→human→accept | canonical bindings và r20 semantics; không fake native/human/acceptance | m1174_lifecycle_scoped_lifecycle |
| wp1174_lifecycle_legacy_unchanged | both | unscoped legacy lifecycle + new ADR0065/URL aliases giữ nguyên | canonical bindings và r20 semantics; không fake native/human/acceptance | m1174_lifecycle_legacy_unchanged |
| wp1174_profile_native_linux | linux | native Linux ext4/XFS + fsyncdir/link/no-replace/lock probes | positive chỉ khi measured supported; unsupported != pass | m1174_skip_fs_probe |
| wp1174_profile_unsupported | linux | overlay/NFS/SMB/unknown filesystem | reject scoped claim before write, không fallback | m1174_allow_unsupported |
| wp1174_windows_claim_rejected | windows | native Windows + otherwise valid scoped claim | native Windows CLI claim rejected unchanged; one pure platform guard mutant killed by assertion with Linux pure positive control; no full suite/matrix | m1174_allow_windows |
| wp1174_status_closed | both | mọi mutator/guard status và argv namespace | rc2/3/8/12 đóng; chỉ reserved_for_dispatch true mới dispatch | m1174_unknown_status_zero |
| wp1174_gate_required_skip | linux | Literal result maps: required native or fixture ID missing/BoQua/timeout/infra; valid full map control | main native gate fails and overall rc nonzero; skipped mutant required target/control cannot yield green; no fail-fast | m1174_gate_required_skip |
| wp1174_gate_evidence_schema | linux | Independent literal reports: wrong ID/profile/hash/checkout/H binding or missing capability measurement | Malformed report rejected; 1 native +83 fixture cases required; valid report control remains accepted as test data only | m1174_gate_fixture_as_native |

Windows focused IDs giữ đúng 13 tên trong windows-focused-ids.json. Enum platform đóng: `linux`, `both`, `windows`. Tập ID có platform `both` hoặc `windows` bằng chính xác tập Windows focused, không phải quyền claim scoped mutator trên Windows. Các ca Windows admission/witness/status phải gọi validator thuần để chứng minh lỗi đúng tầng, không nhận rc8 do chặn OS thay cho schema assertion. Chỉ Windows-only claim test chứng minh đường từ chối native Windows. Trong Mission này không chạy main hoặc full mutants trên Windows; hành vi main của CI Windows do Packet khác kích hoạt được quy định riêng ở §5.2, không thay quyền Mission.

## 5.1. Controller focused chỉ ghi bằng chứng fixture/pure

Controller scratch `focused_runner.py`, SHA256 0ac9f035764e8da05b434d224f2fa77df67e027374aaf8f190a71dd56a40ae6c, chỉ có hai mode: `linux-fixture` và `windows-focused`. Không có mode `linux-native`, không gán trách nhiệm cho CI gọi file ngoài checkout. Linux fixture chọn 83 ID, loại đúng Windows-only và native_required; Windows chọn 13 ID. Controller chỉ import module exact H rồi gọi `chay_suite(..., chi_chay=frozenIDs)`, không gọi main/MUTANTS.

Case fixture được phép monkeypatch resolver topology trong test process/driver cô lập ở scratch. Không thêm flag, biến môi trường, descriptor field hoặc command production để bật seam. Entry production vẫn probe mountinfo/statfs/capabilities thật và phải từ chối overlay. Mutant làm seam reachable từ argv/env/descriptor phải bị test bắt. Các phép I/O thực trong fixture chỉ chứng minh trên filesystem quan sát được, không biến overlay thành ext4. Native profile không được thay bằng fixture.

Profile từng ca lấy từ inventory: 83 ca `fixture_or_pure`, một `native_required`, một `native_windows_rejection`. Controller không đổi nhãn theo mode hoặc OS. Driver đo được của controller là test module cùng product module, inventory và runner; ghi SHA256 trước/sau. Các CLI/driver con bên trong case không được `chay_suite` trả thành receipt riêng: report ghi rõ giới hạn này, không bịa per-case CLI rc hoặc digest của mọi child. Handoff giữ raw outer stdout/stderr và actual command rc từ launcher; reviewer kiểm các assertions/fixture driver trong source H.

Report `wp1174_focused_report.v2` có exact H/tree, mode, OS/Python thật, outcome/profile mỗi ID, digest producer trước/sau, cả hai snapshot (content hash, file count, HEAD/tree/ref/status/index/work diff hash), expected runner rc và measurement limits. Không gọi `runner_rc_expected` là rc đã quan sát: actual rc/hash/terminal do outer launcher ghi. `case_cli_rc: null` vì helper trả function outcomes, không CLI receipts. Missing ID, duplicate ID, skipped/exception, sai head/hash/root, drift hoặc crash đều nonzero; mọi guard dùng if/raise, không assert có thể mất dưới python -O. Controller từ chối interpreter optimized để không vô hiệu assert của test module. Report path phải mới, không tái sử dụng evidence cũ. Error trước report vẫn blocked khi outer rc khác 0 hoặc report thiếu.

Pre-push fixture pass là `prepush_fixture_passed_native_pending`; Windows là `windows_focused_passed`. Cả hai `acceptance_complete=false`, native Linux/canary vẫn pending. Controller không claim native capability probes hoặc OS sandbox attestation. Snapshot chỉ chứng minh không có delta ở hai mốc, không chứng minh chưa từng ghi rồi hoàn nguyên. Thực thi controller bằng outer launcher đã probe với deadline tuyệt đối và kill-tree; không coi prompt read-only là OS isolation.

## 5.2. Carrier native Linux là main hiện có trong CI, không sửa workflow

Workflow `.github/workflows/ci.yml`, job `gate-packet-loop (ubuntu-latest)`, step `packet-loop selftest` hiện gọi `python .claude/dev/packet_loop_test.py`. R6 giao chính `packet_loop_test.py main()` (đã nằm trong write set) chạy và tổng hợp native gate. Không thêm workflow, dependency hoặc manual ci.yml dispatch. Đường hồ sơ P chỉ là metadata, không nhận native/source acceptance từ job fastlane bỏ bước nặng. Gate nguồn H phải chạy thật bước này và có log dương.

Trên Linux, main bắt buộc đủ 84 ID không Windows: 83 fixture/pure cộng một native profile. Missing/duplicate required ID, `BoQua`, timeout, infra, error hoặc thiếu report hợp lệ làm `that_bai_tong` tăng và exit nonzero. Không chỉ in BỎ QUA rồi trả xanh. Required mutant target hoặc cross-family control áp dụng trên Linux bị BoQua/missing cũng làm tổng đỏ; Windows-only oracle được phân tách rõ ở §5.3; không có fake kill credit. Giữ toàn legacy baseline, mutations và controls, không thêm fail-fast hoặc bỏ acceptance cũ. Hai ca harness mới dùng literal inputs độc lập để bắt missing/skip và report sai, không chỉ gọi renderer rồi so chính nó.

Native `wp1174_profile_native_linux` không dùng topology seam. Probe thật mountinfo + statfs magic/name (ext4 hoặc XFS), device/mount identity của target/lock/temp, và lock contention qua process khác, no-replace link/EEXIST, replace, file fsync, directory fsync và readback/tripwire. Ghi từng phép cùng outcome và raw facts đo được. Unsupported/unknown/probe error phải fail hoặc blocked nonzero, cấm BoQua. Chỉ một ID này mang `native_required`; 83 ID còn lại luôn `fixture_or_pure` dù chạy trên runner ext4. Không tự gọi các test fixture là production native lifecycle.

### Trục actual runner OS — áp trước bảng sự kiện Linux

| Actual OS và entry | New WP1174 cases/mutants chạy | Record và nghĩa vụ |
|---|---|---|
| Linux main | 84 ID không Windows; Linux-required mutants/controls | Áp bảng sự kiện Linux bên dưới, native probe thật; không bỏ required skip/missing |
| Windows main do CI/Packet khác gọi (mọi event, kể cả dispatch mặc định/windows-only hoặc PR label windows) | Giữ legacy suite/mutants với semantics skip cũ; thêm đúng12 ID `both` thuần. Không chạy72 Linux-only ID hoặc Windows-only focused case, không chạy bất kỳ new WP1174 mutant nào | In `WP1174_PLATFORM_REPORT_V1`, scope `ci_non_linux_runner` khi GitHub hoặc `local_non_linux_runner`; proof_eligible=false, native_required=false. 73 ID không áp dụng ghi not_run_platform, không tính required Linux skip-fail, không kill credit. 12 both missing/BoQua/failure vẫn đỏ. Actual rc là legacy failures +12 pure results, không ép Linux84 |
| OS khác Windows/Linux hoặc không đo được OS | Giữ legacy suite/mutants, bỏ toàn bộ85 new WP1174 IDs/new mutants khỏi main | Scope `ci_other_platform` hoặc `local_other_platform`, proof_eligible=false,85not_run_platform/no kill credit. Không native probe/cloneH, không giả source acceptance; thiếu OS không cấp quyền routing |
| Windows controller focused của Mission | 13 ID đã đóng băng, gồm focused Windows-only case và1 unit oracle | Không gọi main/MUTANTS/full suite. Bắt buộc native Windows record theo §5.3; không phải CI Windows |

Non-Linux main không áp điều kiện 84 ID hoặc các row PR/H/native của Linux. Không in `WP1174_NATIVE_REPORT_V1` trên non-Linux. Platform report ghi actual OS/context khi đo được, legacy/new applicable IDs và outcomes, skipped-platform IDs/mutants, mutation credit0 cho phần không chạy, eligibility=false; context thiếu/không xác minh được phải ghi unverified, không giả GitHub proof. Native/context UNKNOWN luôn ineligible cho WP1174; việc giữ rc của legacy suite không biến kết quả đó thành native pass.

Chọn applicable ID set TRƯỚC `chay_suite` và mutation/control selection: Windows main chỉ legacy+12both; other OS chỉ legacy. New inapplicable IDs không được chọn làm cross-family controls của legacy mutant. Không loại hoặc đổi nghĩa required legacy targets/controls. New WP1174 mutants không áp dụng được liệt kê riêng not_run_platform, không tăng killed/executed counts. Pure12 both phải gọi validator thuần, không dựa ext4 hoặc kernel Linux. `m1174_allow_windows` chỉ chạy trong native Windows focused case, không full main trên bất kỳ OS.

`wp1174_gate_evidence_schema` phải có literal OS×event cases cho Windows dispatch mặc định/windows-only, other PR label windows và source PR bị label windows: non-Linux scope/ineligible/không native84 dù job cũ được Packet khác tạo. Source PR Windows record không đủ nghiệm thu; dispatcher vẫn cấm trigger/label Windows trong Mission và phải có Ubuntu native proof. Mutants `m1174_gate_windows_as_linux` và `m1174_gate_nonlinux_eligible` phải bị test bắt cùng positive controls; thêm other OS/unknown OS cases. Model OS/event trong metadata chỉ design probe, không chứng minh đã chạy Windows CI.

### Bảng sự kiện đóng CHỈ cho Linux main và phạm vi bằng chứng

`WP1174_SOURCE_PR` là literal PR ID thật do dispatcher cấp sau khi mở draft PR từ metadata P đã review. Executor ghi nó vào test module tại H và đối chiếu với lease/handoff; đây không phải input argv/env cho caller tự chọn. Chưa biết PR ID là precondition trước source H, không tự suy từ title, branch hay việc spec path tồn tại. Record luôn ghi source PR ID này và PR ID thực từ event. Coordinator đối chiếu với GitHub/lease, không chỉ tin literal trong candidate.

| Context | SHA thực thi và kiểm tra | 5 path M/H | Scope và giá trị bằng chứng |
|---|---|---|---|
| GitHub pull_request đúng source PR WP1174 | Event JSON đầy đủ và đúng repo/source PR; full head H, checkout M; dựng normal clone scratch exact H và chạy subset 84 ID tại H | Bắt buộc đủ 5 path M/H/clone khớp bytes; lệch thì blocked, không tự rebase hoặc fallback | `wp1174_candidate`; chỉ record này mới eligible cho native pre-merge proof WP1174 |
| GitHub pull_request khác source PR | Event đúng repo và head hợp lệ; full suite/subset native trên actual checkout M theo workflow | Không so M với H của PR khác; không ép PR khác rebase vì path WP1174 khác | `integration_pr`; giữ baseline/mutants/controls và probe thật, không eligible proof WP1174 |
| GitHub push | Full GITHUB_SHA bằng actual checkout HEAD; repo/event hợp lệ; H ở row này là snapshot SHA đó | Không đòi PR payload hoặc so với source H cũ | `ci_push_snapshot`; post-merge baseline, không dùng làm PR approval/proof |
| GitHub workflow_dispatch | Full GITHUB_SHA bằng HEAD và repo/event hợp lệ | Không đòi PR payload | `ci_dispatch_snapshot`; không eligible PR proof. Mission này vẫn cấm dispatch ci.yml vì Windows matrix |
| GitHub schedule | Full GITHUB_SHA bằng HEAD và repo/event hợp lệ | Không đòi PR payload | `ci_schedule_snapshot`; không eligible PR proof |
| Local không GitHub Actions | H là actual HEAD; ghi rõ local OS/root/scope | Không giả GitHub facts | `native_local`; không eligible CI/PR proof |
| GitHub context thiếu/sai repo/event/SHA, PR thiếu head, hoặc event khác bảng | Không fallback HEAD/local/source PR khác | Không tự bỏ kiểm tra | blocked/nonzero, không eligible |

Chỉ trong Linux main, mọi GitHub row trước hết kiểm full GITHUB_SHA bằng actual checkout HEAD; PR head H có thể khác SHA checkout M và không được trộn hai nghĩa. Mọi Linux row supported vẫn giữ legacy suite và native probe thật trên Linux; routing runtime ngoài Mission không được activate bởi test record. Tách nghĩa test gate của repository khỏi quyền dispatch/admission của adapter. PR khác không bị điều kiện 5 path của WP1174 chặn. Push master sau land là row riêng, không bị thiếu PR payload làm đỏ. Unknown event có hành vi đóng cụ thể, không tự suy tương đương PR.

Chỉ row `wp1174_candidate` dựng clone exact H vì CI có thể checkout synthetic merge M. Không relabel M thành H. Kiểm object/source hashes trước clone; clone normal trong scratch, set origin về endpoint GitHub thật đã kiểm, bootstrap config/branch trước snapshot rồi checkout exact H/tree. Đọc lại producer digests, chạy `chay_suite` chọn đúng 84 ID; không main đệ quy/full mutants lần hai, không network từ tests. Repo/PR/H binding và capability lỗi thì native proof blocked. Các row khác chạy actual checkout snapshot và ghi đúng provenance, không tạo giả binding source H.

Harness literal event cases trong `wp1174_gate_evidence_schema`: source PR hợp lệ; source PR thiếu head; source PR path mismatch; PR khác có M/H paths khác vẫn chạy integration; push hợp lệ/sha lệch; dispatch; schedule; local; unknown event; missing event/repo. Thêm mutant `m1174_gate_event_scope` bắt nhầm row hoặc cho integration/push record eligible source proof. Đây là test logic sự kiện, không mô phỏng GitHub facts thành receipt thật.

Sau các phép trên main in đúng một dòng JSON record `WP1174_NATIVE_REPORT_V1 ` trong log của chính step trước dòng tổng cuối. Record schema `wp1174_native_report.v1`: context/scope/eligibility, source PR ID, actual repo/PR/run_id/run_attempt/job, actual checkout SHA/tree và executed SHA/tree; riêng row wp1174_candidate có expected H/tree, executed clone H/tree và hashes 5 path M/H/clone; mọi row có test/product producer digests, 84 ID/outcome/profile, required-ID set/count, native probe facts/outcomes, native case không dùng seam, và overall status. Cấm duplicate IDs/extra native labels hoặc fields thiếu bắt buộc. Record chỉ native pass khi 84 required passed và mọi binding/probe của row đạt; chỉ wp1174_candidate eligible source proof và coordinator phải kiểm đúng source PR/H từ lease/GitHub; otherwise failure/blocked, không accepted authority. Hai case harness mới phải bác literal report wrong head/hash/missing ID/fixture-as-native/capability unknown. Sửa native failure thành BoQua phải làm regression case hoặc required-result aggregator đỏ.

Native evidence bàn giao là immutable raw GitHub job/step log đã tải và SHA256 của bytes, record JSON, producer/module digests, cùng workflow run ID/attempt/job ID/actual rc và canonical provenance K2/I7. Không cần upload-artifact mới: log là carrier hiện có; log mất, truncation, nhiều record, thiếu record, checkout binding không xác minh được hoặc native case không dương thì blocked, job xanh đơn lẻ không đủ. Coordinator tải/kiểm đầy đủ log và so H/tree/hash, không lấy bản tự khai trong candidate thay GitHub facts. CI checkout M không được che bằng H; native child thật sự chạy exact H. CI log/report chỉ là test evidence, không enrollment/grant cho production coordinator.

Native gate đạt sau publication H và trước accept/land; actual canary sau land vẫn yêu cầu canonical code, runtime ext4/XFS được enrollment/grant, reviewer độc lập và human K4 thật. Chưa có host/grant/human thì canary blocked và #1174 chưa complete. Không cài mount/WSL/đổi bảo mật trong Packet này.

## 5.3. Windows focused và nơi chạy oracle Windows-only

13 Windows focused IDs giữ nguyên. `wp1174_windows_claim_rejected` phải vừa chứng minh native Windows CLI claim bị từ chối, bytes không đổi/no dispatch, vừa chạy đúng một unit mutant `m1174_allow_windows` nhắm pure platform guard trong test process/scratch. Mutant phải bị kill bằng assertion về guard, không nhận crash/import/fcntl/platform error làm kill credit; Linux fixture positive control cho pure guard vẫn pass. Không cố chạy full scoped mutator được hỗ trợ trên Windows, không gọi main/MUTANTS hay full matrix. Đây là test Windows tập trung trong lượt H đã cấp, không thêm Windows CI hoặc thêm lượt riêng.

Không thêm mutant Windows-only này vào Linux MUTANTS. Linux native report ghi `m1174_allow_windows: not_run_platform, deferred_to_windows_focused`, không kill credit, không coi là Linux-required mutant bị BoQua. Windows evidence là raw outer log chứa đúng một `WP1174_WINDOWS_ORACLE_V1` JSON record: exact H/tree, actual OS=Windows, original/mutated module hashes, mutation_id, kind=pure_platform_guard, executed=1, killed_by_assertion=1, positive_control=passed, real_cli_rejection_rc và unchanged/no_dispatch observations. Thiếu/malformed/wrong H/rc/không kill hoặc control đỏ thì Windows gate failed/blocked dù 13 function outcomes nhìn xanh. Coordinator kiểm raw log và launcher actual rc/report, không giả per-case CLI receipts mà helper không cung cấp.

Trước snapshot và test Windows: private bundle SHA256 phải được verify; clone normal `--no-checkout` trong folder mới với LF config, đặt origin đúng endpoint `https://github.com/ducthangho/tra-luat.git`, tạo nhánh test riêng trỏ exact H và kiểm HEAD/tree/clean/ref. Đây là bootstrap bắt buộc được cấp trong read-only test clone, không đổi source branch/H, không network-fetch H chưa publish. Không giao checkout detached/origin bundle cho controller vốn đòi GitHub origin và symbolic-ref. Các bước config/set-url/switch kết thúc trước read-only snapshot; sai H vẫn blocked. Windows focused chỉ test actual runtime đã probe, không dùng tladmin hoặc đổi quyền để làm xanh.

## 6. Lệnh và gate

- Local exact H: git diff --check; python scripts/tl.py --selftest N/N; python -B packet_loop.py adr-song --root; focused Linux fixture runner theo §5.1 trước full gate; preflight lease canonical/metadata/numstat/negative tests. Không chạy tests để tạo N/N giả từ implementation mirror.
- Full Linux: automatic CI jobs gate,gate-cong-cu-gop,gate-ops,gate-packet-loop,gate-registry (ubuntu-latest), exact H provenance; applicable full Linux M9 ci-dot-bien-du.yml trên exact H. python .claude/dev/packet_loop_test.py chạy baseline+mutation, chỉ Linux. Không tùy tiện failfast/skip acceptance.
- Trước PR/CI: không label windows, không manual ci.yml dispatch (hai runner_set đều có Windows), không Windows workflow. Automatic non-windows PR/master matrix đã đọc là Ubuntu. Không thay workflow/ruleset để lách.
- Native Windows: ưu tiên device f7281f27-f79f-40a2-a2f5-b454b58a166a (TRA-LUAT-WIN/tlcommander; Python 3.12/Git/PS 5.1 probe dương); ASUS fallback khi readiness dương. Hai device VM khác account tladmin không dùng để cần quyền cao hơn. Normal clone riêng .git directory, private bundle exact H verifySHA khi H chưa GitHub; outputs/cache/tmp ngoài checkout. Không đụng process/lock #1124/#564. Host offline tối đa 10 phút điều phối rồi đổi host hợp lệ hoặc blocked, không chờ vô hạn/không thay failed thành pass.
- Global source gates không được lấy approve Markdown làm evidence. Human code audit/connector/K0-K7/full M9/Linux/native Windows/exact H land vẫn riêng.

## 7. Review Rescue C6-R3 theo ủy quyền owner, có giới hạn

Owner đã giao toàn quyền điều phối cần thiết tới merge tại #1172 issuecomment6709698499, không hỏi lại các quyền đã giao. Coordinator ghi quyết định governance có exact package hash và cài/readback revision mới trước dispatch; không giả human code audit/Approve hoặc bỏ gate. C6 đã dùng 4 native metadata reviews P r2/r3/r4/r5, giữ verdict/counters. Trần tổng10 calls =2 Codex executor (<=60 phút/run),7 native Claude reviews (đã dùng 4; còn P r6, H và một H rework, <=10 phút/run),1 Codex service canary reviewer độc lập (<=10 phút). Trần rounds cùng PR7. Optional reserve không phải nghĩa vụ gọi hết. Requested source Opus5.5/high, Codex executor high; serving không đo được ghi KHONG_DO_DUOC, provider/session/run/sandbox phải thật.

Active cloud<=300 phút, giữ checkpoint 90/150/180/210/240, thêm 270/300. User idle không tính active; lease/expiry vẫn wall clock. Trước dispatch đo used + bounded remaining deadlines + coordinator/tests <=300; worst remaining trước P r6 là 200 phút (2 executor ×60 +3 review ×10 +1 canary ×10 +40 điều phối). Thiếu thì siết deadline run đã đặt hoặc checkpoint hữu hạn có audit, không zero lịch sử/không vay C2 unknown/C3/C5. Giữ 2 Ubuntu CI head/attempt, 2 Linux M9 chỉ relevant change, 24 runner-giờ, 2 native Windows focused runs/tổng 60 phút, 1 writer. Không paid/AGY/CI Windows/full Windows matrix/project/registry hoặc đổi credentials/security.

nang_tran (pending owner exact package): ai_nang=ducthangho; tran_cu=6files/450added; tran_moi=5files/2600added; can_cu=state/transaction/lifecycle và tests coupled, source additions hiện0, metadata count đo riêng. Đo actual full base→H numstat TRƯỚC review, vượt2600 hoặc 5files stop để replan, không bỏ tests. Đây là proposed ceiling chứ chưa số đo source.

ADR0032 policy/schema vắng ở baseline. Xin scoped manual closure exception WP1174-R6-CLOSURE-EXCEPTION (payload SHA256 b6ecc5516e74e7d46044d49208b85b8123ccbf6f752b0f2effb228abb8ccd97a), đúng 5 path, required native Linux gate và mọi K0–K7/M9/human giữ nguyên, owner ducthangho, expires 2026-11-08T08:03:01Z. Thiếu exact owner approval hoặc impact_hint/companion/symlink/prefix overlap mới thì blocked/revision; không bịa canonical policy SHA hoặc sửa policy toàn kho.

## 8. Acceptance và rollback

ZeroP0/P1/P2 trên exact H; P3 source chỉ theo owner exact H/slug/reason/remediation disposition theo M1, không tự carry spec waiver. Required tests đúng platform/ID đều passed, not_run/unknown/skip không thành pass. Full oldCLI/ADR0065/URL regression còn nguyên. Code land không đồng nghĩa Missioncomplete; actual canary/lifecycle phải đủ trước #1174complete và đưa PR0 qua dependency.

Rollback: trước activation, thiếu capability hoặc bất kỳ mismatch ngừng dispatch/admission, giữ unknown reservations/history, không decrement/ghi lại schema2. Không chạy cached legacy writer sau cutover. Product rollback phải revert code dưới exact authority, không phục hồi journal bằng backup cũ; active journal mismatch cần Packet reconciliation riêng. Source control/guard không tự nới authority để rollback. Vẫn giữ source plan PR0→PR1–PR8, full reference/shadow/rollback và outcome audit.

## 9. Prompt theo vai, cùng frozen spec bytes

Executor session mới đọc spec_ref/OID/hash, canonical/lease và exact branch, chỉ write set; không tự review/approve/land. Giữ code/temp/evidence khác nhau; báo state/usage trước mỗi run và sau terminal. Handoff full H/tree/diff/numstat/tests/rawresults/unknowns/history.

Reviewer session mới read-only clone riêng exact H; hai trục Spec và Standards/Security, mỗi finding đủ location/reason/fix/oracle/risk; quét mọi biểu hiện theo28ID/8classes. Kết thúc KET_LUAN: approve|changes_requested|blocked, reviewed_sha/tree, open_findings, windows classification, M9 scope, no fake serving/human. Owner audit không do reviewer agent giả lập.

Spec/prompt này materialize đúng bytes từ metadata source. Lease prompt_path trỏ chính file này và prompt_sha256_required=spec_hash; launcher outer instruction chỉ chọn vai và expected-head/ref, không đổi frozen bytes. Lease reviewer assignment/expectedH ghi sau code H có thật, không đặt futureH giả vào lease.

## 10. Lịch sử và thay đổi cách kiểm chứng

Giữ toàn bộ P r2/r3/r4/r5 verdicts/counters và28 ID thiết kế r20. P5 review4 xác nhận P4-01/P2 và P4-02/P3/P4-03/P3/P4-04/P3 fixed; mới C6-P5-01/P2 về actual runner OS. R6 thêm OS trước event table, tách chính sách không trigger Windows của Mission khỏi hành vi legacy Windows ở Packet khác, không xóa hoặc hạ severity. R6 chỉ proposed remediation tới khi independent review xác nhận.

Checkpoint lớp dispatch-durability-order tái diễn: dùng ma trận OS×event×entry và exact applicable case/mutant/control sets thay vì chỉ prose cho happy-path PR. Design model có counterexamples OS/event, không gọi là product proof hoặc closure. Source vẫn chưa được cấp qua việc chuẩn bị r6; giữ85 IDs/13 Windows focused, không CI Windows của Mission. Trần metadata rounds dự phòng đã được dùng: nếu r6 vẫn có finding phải checkpoint hữu hạn, không gọi thêm dưới tên khác hoặc âm thầm vay code-review slots.
