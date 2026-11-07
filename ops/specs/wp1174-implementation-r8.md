dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# WP1174 r8 — Thi công adapter theo thiết kế r20

- packet_id: WP1174; revision: 8;
- mission_issue: 1172; mission_revision: 12; mission_plan_sha256: 47871a14f209e2b5baf27bfdb97a1d5c8a967e968c39d8e830c7f3d4a6268808
- contract_id: WP1174-r8-C6; generation: 6; review_class: sensitive
- executor: codex; execution_surface: codex_service; model_family: openai; transport: machine
- source reviewer: claude; execution_surface: claude_code; model_family: claude; transport: machine/local
- immutable_acceptance_baseline: c6afde62c846f1ef3d6a83c14459966849edf756
- metadata_parent: ee6192b27cdebe59d7bdd6691fd271d8ce1a6bd0; code continuation là exact metadata commit chứa spec này, ghi ở lease sau khi commit có OID

## 1. Hiệu lực, nguồn và outcome

Đây là hợp đồng trình duyệt. Chỉ có hiệu lực sau owner duyệt exact bundle, cài/readback Mission r12, publish metadata immutable và lease exclusive hợp lệ. Chưa source work/grant/CI/activation qua việc tạo file này.

Design normative là ops/specs/wp1174-c5-adapter-design.md, bytes SHA256 5a749f921de112565779b8b1e42a2324e8efbc1e5e053d11919d30d8cf20a117 tại design head c172150d64c4fa1382469c81a658410c85aff88d; native Claude review technical approve, 0 P1/P2/P3 ở #1174 comment6679977538. Không đổi bytes r20 để ghi source approval. Metadata contract r8 không tự nhận approval r20 trên SHA mới.

Outcome: hiện thực r20 trong packet-loop, giữ legacy ngoài scope; chứng minh admission/init/lease/advisory review/actual-human/accept và source/high_water/recovery bằng đúng profile. Adapter hỗ trợ Mission #1172/registered Packets theo authority canonical, không activate route toàn kho, không generic controller/registry.

## 2. Phạm vi đóng và drift

Write set exact, cũng là effective set CHỈ sau khi owner duyệt scoped manual closure exception:
- .claude/dev/packet_loop.py
- .claude/dev/packet_loop_test.py
- docs/PROTOCOL_DA_PHIEN.md
- ops/specs/wp1174-c5-adapter-design.md
- ops/specs/wp1174-implementation-r8.md

Không workflow, ruleset, credential, launcher, release manifest, ADR0041/0045 hoặc code Packet khác. New helper writer command thứ15 bị cấm. Giữ13mutator + adopt-state (2mode cùngcommand), guard-first-publication read-only. Canonical ADR0065 và URL-human identity delta ở base mới phải giữ; không cherry-pick code C5 cũ đè lên canonical.

R20 review base 825eb3561a94e05c36045d2c981b4108c523e31c khác source base này. Drift đã đọc: packet_loop 8 dòng, tests 119 dòng, protocol 17 dòng, ADR0065; source full diff đo từ c6afde62c846f1ef3d6a83c14459966849edf756, không đo từ H rework mới để giấu scope. Metadata parent merge chỉ mang r20MD vào nền canonical; chưa product source changes.

## 3. Bootstrap, continuation và publication

1. R7/generation5 đã dừng ở H1 cục bộ, native Claude changes_requested; giữ toàn bộ commit, journal, 12 finding và counter. Lease cũ phải kết thúc và được đọc lại trước khi sửa metadata đang thuộc phạm vi đó. Không hồi sinh generation5.
2. R8/generation6 chỉ có hiệu lực sau quyết định theo ủy quyền gắn exact P8/spec hash/Mission r12 hash, install/readback r12 và native metadata review exact P8 trước publication. P8 chỉ chứa hai MD; không chứa code H1. Không gọi approve metadata là approve source.
3. Giữ PR1275 và branch vật lý agent/wp1174-g5-codex để không force push hoặc mất lịch sử. Tên branch là lịch sử; generation có thẩm quyền là6 trong lease/state/handoff. Spec ref immutable ops/spec-wp1174-r8@P8, path và hash được cấp sau khi P8 có OID thật.
4. Cấp lease mới exclusive sau fresh all-ref/normalized/symlink/prefix checks, issuer/authority, canonical check và workflow bot readback. Bootstrap source dùng canonical v2 Codex service/Claude Code hiện có, không dùng v3 candidate tự cấp quyền. Journal generation5 giữ nguyên. Generation6 dùng state riêng có tối đa1 source attempt và1 source review còn lại; evidence phải luôn ghi cumulative C6 đã dùng7 calls,6 native reviews và1 executor, không khai aggregate bằng0.
5. Executor phiên mới bắt đầu P8 sau begin-attempt hợp lệ, tích hợp H1 từ private handoff bằng merge giữ ancestry, rồi làm đủ contract. Immutable acceptance baseline mới là canonical c6afde6 theo quyết định revision này; không dùng H1/P8 làm baseline. Canonical27→c6 chỉ đổi launcher.py và launcher_test.py (+170/−23), ba source path Packet byte-identical; đây không làm mất bất kỳ source work H1 nào. Giữ raw27→H1, raw27→H2 bao gồm upstream và rawc6→H2 để đối soát; chỉ rawc6→H2 đo own scope5/4000. Hai MD mới giữ bytes đóng băng; source chỉ ba path đã cấp. H1 hoặc ancestor chưa đủ điều kiện không được publish riêng.
6. Native source review trọn baseline c6→H2, đọc thêm toàn H1 finding/diff và canonical launcher delta, gồm r20, r8 và mọi code, trên clone/context độc lập. Nếu H2 đổi thì review/gate/hash cũ stale. Local gates và Windows focused exact H2 trước first code publication. Theo chỉ thị trực tiếp cho phép AI audit thay chủ kho ở phiên khác executor, riêng source WP1174 r8 dùng independent delegated_owner_audit trên exact H2 trước publication, tách khỏi executor và verdict native. Audit này khai đúng AI/provider/session, không phải human_exact_head_audit hoặc human_audited. Formal K4 source vẫn phải là native Claude cross-provider thật và đầy đủ, không dùng delegated audit thay K4. Đây là ngoại lệ source-only, không đổi actual-human semantics của target r20 hoặc giả agent repost thành human.
7. Controlled publication H2 sau đủ pre-push gates; automatic Ubuntu CI, native report, full Linux M9, connector và canonical K0–K7 cần đạt. Formal GitHub Approve/land authorization exact H vẫn riêng theo protocol; không auto-merge/bỏ draft khi thiếu gate.
8. Sau land/readback mới canary bằng canonical đã land, target descriptor/grant riêng, private coordinator seed đã provision và native Linux profile đo thật. Codex service reviewer mới, requested model hoặc effort cao hơn, vẫn advisory và cần actual human riêng. Thiếu host/grant/human/budget thì canary blocked, không đóng1174 hoặc nhận PR0 đã qua dependency.

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

Workflow `.github/workflows/ci.yml`, job `gate-packet-loop (ubuntu-latest)`, step `packet-loop selftest` hiện gọi `python .claude/dev/packet_loop_test.py`. R8 giao chính `packet_loop_test.py main()` (đã nằm trong write set) chạy và tổng hợp native gate. Không thêm workflow, dependency hoặc manual ci.yml dispatch. Đường hồ sơ P chỉ là metadata, không nhận native/source acceptance từ job fastlane bỏ bước nặng. Gate nguồn H phải chạy thật bước này và có log dương.

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

## 7. Bounded rescue R8 và ngân sách

R8 thay R7 trước continuation; theo ủy quyền chủ kho1172/comment6709698499, điều phối phải ghi quyết định exact package và install/readback, không hỏi lại quyền thường lệ. Không giả human hoặc bỏ gate.

H1 full baseline27→H1:5 tệp,+2132/−5; metadata563, còn468 dưới cap2600. Phần còn thiếu ước850–1200 dòng, chưa tính hết sửa12 finding. Trần mới5 tệp/4000 dòng thêm tính toàn baseline27→H2; không nén code/bỏ tests hoặc giấu metadata. Vì transaction, witness, adoption và postimage dùng cùng invariants, không tách hai PR chồng seam chưa land. Reviewer phải đo numstat và kiểm khai nâng trần trước review.

```yaml
nang_tran:
  ai_nang: ducthangho
  can_cu: owner delegation6709698499; H1 native review3d4daf09; exact MCR decision recorded before source grant
  tran_cu: {files: 5, added_lines: 2600}
  tran_moi: {files: 5, added_lines: 4000}
```

C6 cap11 model calls =2 Codex source runs,8 native Claude reviews,1 Codex canary review. Đã dùng7:5 metadata reviews,1 source executor,1 H1 native review; native đã dùng6/8. Còn đúng P8 metadata, source continuation, final H2 native review và canary. Mỗi source run≤55 phút; mỗi review≤10 phút. Không mở invocation ngoài sổ hoặc reset lịch sử C2/C3/C5/C6/PR1275.

Active C6≤420 phút, tính cả active đã dùng; đây không phải cấp thêm420 phút từ0. Trước dispatch phải đo actual used + remaining bounded deadlines + coordinator/tests≤420. User idle không tính active; lease/hard expiry vẫn wall clock. Hard expiry giữ2026-11-08T08:03:01Z. Tối đa7 ci.yml head/attempt gồm hai metadata đã chạy, P8, H2, hậu merge, canary metadata nếu cần và một contingency; mọi auto run/retry đều ghi. Hai full Linux M9,24 runner-giờ, hai Windows focused runs≤15 phút/run trong cap tổng60 phút. Operational lease workflows ghi riêng nhưng vẫn tính runner/time thật. Không mua credits, không AGY, không Windows CI/full Windows mutant.

Scoped manual closure exception WP1174-R8-CLOSURE-EXCEPTION SHA256 7b181eaf4725010a1b2ac74f7fcba47881b8d9bbaf80169502a982140d44d3da vì policy/schema ADR0032 chưa có tại baseline27. Exact five paths và mọi K0–K7/M9/native Windows/human giữ nguyên. Ngoài closure, stale/unknown source hoặc thiếu lease đều blocked. Trần mới không cấp quyền thêm file, provider, LIVE hoặc security configuration.

## 8. Acceptance và rollback

ZeroP0/P1/P2 trên exact H; P3 source chỉ theo owner exact H/slug/reason/remediation disposition theo M1, không tự carry spec waiver. Required tests đúng platform/ID đều passed, not_run/unknown/skip không thành pass. Full oldCLI/ADR0065/URL regression còn nguyên. Code land không đồng nghĩa Missioncomplete; actual canary/lifecycle phải đủ trước #1174complete và đưa PR0 qua dependency.

Rollback: trước activation, thiếu capability hoặc bất kỳ mismatch ngừng dispatch/admission, giữ unknown reservations/history, không decrement/ghi lại schema2. Không chạy cached legacy writer sau cutover. Product rollback phải revert code dưới exact authority, không phục hồi journal bằng backup cũ; active journal mismatch cần Packet reconciliation riêng. Source control/guard không tự nới authority để rollback. Vẫn giữ source plan PR0→PR1–PR8, full reference/shadow/rollback và outcome audit.

## 9. Prompt theo vai, cùng frozen spec bytes

Executor session mới đọc spec_ref/OID/hash, canonical/lease và exact branch, chỉ write set; không tự review/approve/land. Giữ code/temp/evidence khác nhau; báo state/usage trước mỗi run và sau terminal. Handoff full H/tree/diff/numstat/tests/rawresults/unknowns/history.

Reviewer session mới read-only clone riêng exact H; hai trục Spec và Standards/Security, mỗi finding đủ location/reason/fix/oracle/risk; quét mọi biểu hiện theo28ID/8classes. Kết thúc KET_LUAN: approve|changes_requested|blocked, reviewed_sha/tree, open_findings, windows classification, M9 scope, no fake serving/human. Owner audit không do reviewer agent giả lập.

Spec/prompt này materialize đúng bytes từ metadata source. Lease prompt_path trỏ chính file này và prompt_sha256_required=spec_hash; launcher outer instruction chỉ chọn vai và expected-head/ref, không đổi frozen bytes. Lease reviewer assignment/expectedH ghi sau code H có thật, không đặt futureH giả vào lease.

## 10. H1 findings và tiêu chuẩn đóng trong R8

Native H1 run3d4daf0932d3433aa69ee8f8ffabb4f7, actual rc0, changes_requested:2P1/5P2/5P3. Raw verdict và mọi nguồn giữ nguyên; không hạ severity hoặc tự đánh dấu đã đóng. Final H2 reviewer phải xác nhận từng F1–F12 theo slug cũ. H1 subset35/35, regression267/267, selftest1777/1777, ADR64/64 không thay85/native/M9. Frozen83 đã rc2 vì thiếu ID. Mutation subset6 reports phải kiểm lại vì finding crash-chain oracle.

### 10.1 F2 — private HMAC và deterministic initialization

Admission A và spec S không chứa seed hoặc hmac_key. Trước khi cấp A, operator provision một seed ngẫu nhiên32 byte ở file riêng trên enrolled native mount, regular, owner hiện hành, mode0600, O_NOFOLLOW, không alias journal/witness/lock/source. Đây là artifact enrollment ngoài Git, không command writer thứ15, không registry hoặc credential provider. Worker chỉ dùng fixture seed, không đọc seed thật của điều phối.

A đóng thêm private_seed_path và private_seed_sha256 (fingerprint SHA256), thay initial_state bằng initial_state_projection không chứa hmac_key. Projection phải khớp canonical fresh initializer và approved allowance, không tự quyết định schema từ A. Fresh có state awaiting_lease, counter/history/reviews/calls rỗng đúng grant lineage mới, chưa quyền lease/dispatch. Optional keys vắng giữ vắng.

Derivation dùng HKDF-SHA256, output32 byte rồi lowercase hex: extract với salt ASCII tra-luat/WP1174/v3-hmac-key/HKDF-SHA256/v1 và IKM seed; expand một block với info là canonical UTF8 JSON của {enrollment_id,binding_sha256,packet,g0}, sort_keys=True,separators=(',',':'),ensure_ascii=False,một LF, rồi byte0x01. binding_sha256 là immutable lineage binding, không hash của A đang chứa chính nó. Không dùng boot/time/random mới trong initial image; reboot cần readmission như r20.

Mọi lstat/O_NOFOLLOW/fstat/fingerprint/type/default/projection checks và derive/validate full bytes xong trước witness/target/temp publication. Fresh/resume đọc cùng seed và grant cho byte-identical image. Seed thiếu/sai trước publication: rc8/no write. Sau reserved publication: UNKNOWN, giữ witness, không generate key mới. Rotation cần enrollment/reconciliation mới. Legacy adoption giữ hmac_key từ source snapshot private đã hash/validate, không rederive hoặc đưa source bytes vào Git A.

Oracle tính secret fixture values để khẳng định chúng không xuất hiện trong A/S/stdout; không cấm mọi chuỗi64hex vì fingerprint và hash vẫn là64hex hợp lệ. Thêm wrong/missing/changed seed, resume byte equality và no-write assertions trong các init/preflight ID hiện có.

### 10.2 F3 — canonical state v3 và optional keys

Schema lấy từ code canonical cố định, không set(initial_state). Required legacy core có 27 key: schema_version,review_rounds_used,codex_review_calls_used,codex_calls,nang_tran,review_rounds_limit,codex_review_calls_limit,packet,mission,executor,reviewer,executor_identity,reviewer_identity,state,lease,attempts_used,attempts_limit,same_failure_limit,finding_counts,attempt_open,attempt_anchor,hmac_key,reviewing_head_sha,accepted_sha,reviews,posts,history.

V3 đổi schema_version=3 và thêm required state_revision,generation,enrollment_id,binding_sha256,adoption,scoped_review,human_acceptance. Ba field cuối null ở fresh và là closed typed records ở các phase áp dụng. Optional legacy allowlist chính xác: luat_adr0054,ngu_canh_lease,dem_tu_suy,ly_do,truc,pending_sha,bien_nhan_approve,mo_lai_tu,checkpoint_day,moc_connector,quyet_dinh_p3. Mọi key khác bị chặn. Mỗi optional có kiểu/absent-null semantics và cross-field predicate của canonical legacy; không preseed null để giả absent. Static inventory phải bao gồm helper/transitive dict construction, không chỉ st[key] assignments.

Postimage table theo command chỉ cho phép core transitions đã khai và optional writes thực tế: record-lease luat_adr0054/ngu_canh_lease; rescue ly_do/truc với delete hợp lệ; review pending_sha/bien_nhan_approve khi đúng lane; accept moc_connector/quyet_dinh_p3; mo-lai mo_lai_tu; chu-kho-duyet checkpoint_day/mo_lai_tu. Optional migration dem_tu_suy không được tự clear. Counter không giảm; history/calls/reviews giữ prefix, chỉ thao tác void hợp lệ của canonical có phép hoàn attempt theo bằng chứng thật. Không dùng câu monotonic chung để vô hiệu void contract.

Factor invariant validation thuần dùng preimage/postimage thật; legacy v2 ngoài scope giữ nguyên. Không đổi schema trong file, normalize optional hoặc giả identity để qua loader. HMAC bất biến sau initial creation; full anchor/counter/history predicates của legacy giữ hiệu lực. Profile đầu chỉ cam kết adoption giữ executor/reviewer identity tuple; tuple khác hoặc counters lịch sử không chứng minh được thì UNKNOWN và cần migration/reconciliation riêng, không relabel records/reset counts.

Adoption record phải đóng phase,payload,payload_sha256,cutover_started. Immutable payload chứa source snapshot/hash, target core projection (không chứa chính adoption record), tombstone bytes/hash, IDs/generations/paths/binding/lineage. Hash chỉ projection immutable, không hash tự tham chiếu hoặc mutable phase/revision. Final target được dẫn xuất từ projection rồi thêm adoption record; giữ snapshot để recovery sau tombstone. Full keysets/types cho payload và scoped_review/human_acceptance phải được khai tập trung trong code và được literal negative fixtures kiểm; không lấy schema từ input hoặc renderer. Ordinary current high_water không bị ép bằng as-of adoption hash sau mutation.

### 10.3 F4/F5 — source authority và Git view

Không gọi _record_lease_ref bằng state giả hoặc monkeypatch _save để tạo authority. Tách verifier I2 thuần khỏi transition/commit, trả verified lease/spec/identity facts. Fresh init dùng identity pinned trong grant; ordinary dùng identity thật từ journal dưới lock và phải khớp grant. Legacy record-lease tái dùng verifier rồi tự commit state như trước. Không phát log state leased khi journal chưa ghi.

Scoped root phải khai explicit, khớp enrolled identity; không default cwd. Git reads dùng no-replace-objects; reject replace/graft/alternates/shallow hoặc object/config view không đo được. Root/object/remote identity phải được kiểm bằng nguồn canonical đã ghim, không caller FILE. Scratch fetch/verification ngoài enrolled repo/journal được phép để lấy current facts; guard không đổi refs/index/worktrees của enrolled repo, journal/witness hoặc dispatch. Không gọi prompt read-only là OS isolation.

Consumer scoped phải đã land trên first-parent canonical và code đang chạy phải khớp canonical snapshot hiện hành đã xác minh; candidate chưa land không tự activate qua descriptor/grant. Fixture chỉ monkeypatch adapter nội bộ trong driver cô lập, không thêm argv/env/schema flag để bỏ rollout. Native CI capability probe đo kernel/filesystem thật nhưng không là enrollment hoặc quyền activate consumer candidate.

Profile này cần current remote canonical executor grant/spec để resolve admission trước init; journal vẫn chưa record lease/attempt. Khi chưa có grant remote, init bị chặn. Đây là giới hạn triển khai đầu của F12, không tuyên bố đã hỗ trợ mọi pre-lease source có thể có trong r20. Không tạo registration record mới hoặc mở trust fallback để lấp nguồn chưa có verifier. Registered Packet lấy từ installed Mission packet_graph cùng current canonical grant, owner instruction và bot readback đủ trang.

### 10.4 F6/F7/F8/F9/F10/F11 — closed errors và independent oracles

Scoped flags không admission, namespace thiếu/trộn/sai mode hoặc syntax sai: rc2,input_rejected. Stale revision hợp lệ: rc8,revision_rejected. Quota: rc3,quota_exhausted. Authority/state/profile mismatch hoặc unknown trước write: rc8,UNKNOWN (guard rc12,admission_rejected). Durability_unknown chỉ sau khả năng đã ghi journal/witness; giữ reservation, không retry. Legacy_changed rc8. Success đúng ba status r20; chỉ reserved_for_dispatch có dispatch_allowed=true. Guard PASS0,FAIL/UNKNOWN/admission_rejected12; mọi stdout status đúng một JSON record, không helper print giả. Catch đúng Chan/SystemExit/TimeoutExpired/parse/I/O classes, không biến KeyboardInterrupt/process kill thành pass. Legacy ngoài scope giữ codes cũ.

Admission phải đóng kiểu mọi field và pin base đúng spec. Phân biệt git_root explicit của code với journal root của generation và lineage root cố định chứa seed/lock/witness. state_path=journal_root/wp{packet}.json; CLI state-dir phải khớp journal root đã cấp. initial_state_path là genesis journal path được authority ghim: fresh cho phép state_path bằng initial_state_path; adoption bắt buộc target khác source/genesis và mọi target lịch sử. Source g0 có thể bằng initial_state_path. Seed/lock/witness không alias journal nào; không áp một blanket inequality sai cho hai tên cùng vai trò genesis. Target journal root mới phải được enrollment trước và cùng mount; fixed lineage lock/witness không đổi qua generation. Wrong schema phải bị đúng validator/reason; không nhận OS/network rejection làm schema proof. Mock raise exception thật; assert reason, unchanged entry bytes và positive/cross-family control. Mọi exception chain có crash marker không được kill credit, kể cả AssertionError bọc crash. Không bỏ _co_sap_do cho WP1174.

Mount selection không so mount IDs như chuỗi. Khi có nhiều entry cùng mountpoint và không đo được active mount identity, UNKNOWN; không giả thứ tự mountinfo là proof. Probe magic/name/mount identity và mọi capability r20 vẫn bắt buộc.

Tombstone golden là literal exact bytes độc lập renderer. Chạy13 legacy entries trên đúng bytes, kiểm cả old path và target fixture unchanged. Base27 old reader có thể chặn ở missing reviewer trước schema; phải ghi đúng reason quan sát, không gọi đó schema_version coverage. Current reader có thể nhận exact retired-format sớm rồi reject rõ, nhưng không mở reader v2 hợp lệ cho payload retired hoặc giả đã sửa cached old reader.

### 10.5 F1 — toàn bộ source acceptance vẫn bắt buộc

Không giữ hardcoded incomplete flag rồi báo hoàn thành. Chỉ bỏ chặn sau khi14 actual entry/race, adoption/recovery, lifecycle/advisory/human/collector,84-ID native/event reports và toàn mutants/controls hoàn chỉnh. Frozen85 ID và13 Windows giữ nguyên; bổ sung stimulus/oracle trong các ID hiện hữu cho12 finding, không rename/placeholder hoặc skip acceptance. Native H2 reviewer xác nhận closure trên exact H2; metadata approval không đóng code findings.
