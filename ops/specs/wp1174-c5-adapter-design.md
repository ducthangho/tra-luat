dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# WP1174 C5-A2 — Candidate đặc tả r11 (chưa freeze/lease)

- packet_id: WP1174; revision: 1; design_revision: 11;
- packet_issue: 1174
- review_class: sensitive
- candidate_kind: specification_proposal_only
- source_lease: none
- base: 825eb3561a94e05c36045d2c981b4108c523e31c

## 1. Assignment và giới hạn

Nguồn: chủ kho duyệt C5 ở #1172 comment 6666000374, rồi yêu cầu “Thực hiện đúng quy trình vá, cross review theo ADR 0060 đi, cho cả C5-A2 và C5-A1”. Candidate này hợp nhất sửa đổi r6→r7 và findings A2 thành một đặc tả duy nhất để cross review offline; không có implementation adapter, không tự cấp source authority. Lease/spec_hash và rollout M10 còn cần xác minh trước code Packet; chỉ thêm dòng ADR không tự kích hoạt hiệu lực.

Write set thực tế của proposal: `ops/specs/wp1174-c5-adapter-design.md` (một Markdown). Ngoài scope: product packet_loop/launcher/protocol, workflows, credential, registry, LIVE, merge/land. Write set implementation #1174 phải đóng băng riêng sau spec đạt và ownership rõ. Không mở source B qua commit proposal này.

M3 của diff Markdown-only: đề nghị not_required, reviewer quyết định; M9 full mutant không triggered bởi diff này. Windows CI/full mutant Windows vẫn bị cấm; native Windows focused được phép khi áp dụng. Không gọi những gate chưa chạy là passed. Spec proposal không được coi là M8 archival vì nằm trong ops/specs.

Executor/preparer: Codex service; reviewer: Claude Code độc lập, requested Opus 5.5/high, hai trục Spec và Standards/Security. Review source về sau giữ routing, actual human và gates riêng. C5-A1 giữ needs_revision lịch sử, không được sửa thành approve hồi tố.

## 2. Profile và activation

Profile đầu tiên chỉ có một coordinator Linux, một journal Packet đã được authority canonical chọn, local durable filesystem và các producer đáng tin tuân thủ admission. Không hứa chống admin malicious, arbitrary private writes hoặc distributed exactly-once.

Đường dispatch hợp lệ chỉ nằm ở coordinator được giao. Trước adoption phải đóng admission cũ, để mọi request cũ tới terminal hoặc unknown đã được đối soát, nhận handoff của các writer đang được đăng ký và xác nhận không còn writer v2 đang giữ snapshot để ghi. Không tự giết process của Packet khác, đổi ACL, chặn tài khoản hoặc thêm registry mới.

Không kiểm chứng được quiescence/lineage/budget/producer coverage thì **không adoption hoặc activation**. Snapshot process hay hostname đơn lẻ không phải attestation đầy đủ. Resume phải đọc lại facts, không dùng handoff cũ như grant mới.

## 3. Adoption và recovery

Giữ **14 mutator**, vì recovery là mode của `adopt-state`, không là command thứ 15. Hai mode loại trừ nhau:

- `adopt-state ... --mode initial --expected-source-sha256 HASH --expected-witness-revision absent|N --target-generation N`.
- `adopt-state ... --mode recovery --adoption-id ID --disposition resume_forward|abandon_before_cutover|abandon_before_prepare --expected-witness-revision N`.

Cả hai mode cần admission/authority còn hiệu lực, exact adoption ID và generation; sau reboot phải readmission vì boot ID đổi. Các argument chỉ đối chiếu, không tự tạo authority. Không tự suy disposition từ lỗi.

### Record và thứ tự cutover

Prepared state giữ immutable source snapshot, hash bytes nguồn, deterministic target payload, tombstone bytes/hash, binding hash và lineage. `prepared_payload_sha256` được tính từ **immutable payload projection** đã liệt kê, loại trừ field hash của chính nó và các field phase/revision tiến trình; không dùng self-referential whole-file hash. Validator dẫn xuất lại payload từ source snapshot có hash ghim trong admission.

Trước khi thử ghi tombstone, ghi durable `pending_adoption.cutover_started=true` trong witness, rồi `cutover_started: true` vào prepared journal và readback; chỉ sau đó mới động tới path cũ. Flag này monotonic, không về false. Sau tombstone durable/readback, mới chuyển target adopted; bước finalize witness vẫn bắt buộc trước khi cho kết thúc adoption. Quiescence giữ xuyên quy trình. Đây là state machine nhiều bước, không hứa atomic nhiều file.

| Disposition | Preconditions | Hành động |
|---|---|---|
| resume_forward | Target prepared đúng immutable payload/hash/binding; old path có đúng source hash hoặc đúng tombstone hash | Nếu còn source, hoàn tất intent flag rồi tombstone; nếu đã tombstone, giữ bytes; chỉ chuyển adopted sau full durable/readback và tripwire |
| abandon_before_cutover | Target prepared, `cutover_started` được đọc chắc chắn là false, old path đúng source hash, authority cho phép abandon | Ghi target aborted có lịch sử, không xóa target/history; giữ admission paused. Không tự cho old generation dispatch trở lại |
| abandon_before_prepare | Pending đúng ID, target absent, witness pending.cutover_started chắc chắn false, source đúng hash | Clear pending durable, suspended=true, append aborted-intent identity dù chưa có target; không xóa witness/history hoặc resume predecessor |
| Bất kỳ mode gặp dữ liệu khác | Missing/corrupt, sai hash/ID/generation, intent unknown, old path không thuộc hai hash | UNKNOWN, không sửa hay dispatch |

Sau abandon, target aborted giữ nguyên trong lineage. Initial adoption không được ghi đè target aborted; muốn thử lại phải có admission mới, generation mới và adoption ID mới, giữ node aborted trong lineage. Không reset counter/history qua generation mới.

Nếu intent đã true, dù old path còn source do crash, chỉ xét resume_forward; không abandon. Không bao giờ ghi lại schema 2 sau khi có khả năng đã bắt đầu tombstone. Với target adopted cùng adoption ID, replay recovery chỉ trả `already_completed_no_dispatch`, không ghi counter hoặc dispatch.

Oracle thêm vào R6-A02: crash trước/sau durable intent, trước/sau tombstone và adopted; recovery đúng từng nhánh; abandon sau intent bị chặn; corrupt/missing giữ UNKNOWN; không rollback schema 2; boot đổi chưa readmission bị chặn. Các oracle này **chưa có implementation/test**.

## 4. Fresh init và lineage

Scoped `init` là ngoại lệ hẹp của gate load-state:

1. Admission canonical phải khai rõ `predecessor: none`, không source path/hash, generation đầu được cấp và lineage chưa từng dùng; authority/allowance/admission có thể có trước executor lease.
2. CLI phải truyền sentinel **`--expected-revision absent`**. Chỉ scoped init mới nhận sentinel này. Mọi mutator khác đòi số nguyên revision hợp lệ; không tự coi thiếu revision là absent.
3. Lấy lock, xác minh authority và absence bằng lstat cho đúng target; target tồn tại hoặc symlink thì rc 8. Không gọi normal `_load` cho target absent.
4. Tạo state `awaiting_lease`, counters ban đầu đúng grant và revision đầu quy định trong schema; chưa cấp quyền source/attempt/dispatch. Full executor lease vẫn được kiểm riêng ở transition tương ứng.

Admission có predecessor/source, lineage đã có history/counter hoặc không chứng minh được lineage mới ⇒ init rc 8, không tạo file. Missing target của generation đã được khai predecessor hoặc đã init trước đây ⇒ UNKNOWN, không init lại. `adopt-state` là lệnh duy nhất tạo **target có predecessor**.

Witness là một file durable **cho toàn Packet lineage**, không theo generation, ở path cố định do canonical binding chọn. Cùng mount với target/lock/temp, không unlink hoặc có khoảng absent sau lần publish đầu. Mọi lần đọc dùng lstat và O_NOFOLLOW, fstat regular file và so identity/readback; symlink/missing/corrupt ⇒ UNKNOWN. **Tạo đầu**: temp riêng cùng thư mục bằng O_EXCL, ghi đầy đủ → fsync file → fsyncdir → atomic publish-no-replace bằng hard link temp→final (EEXIST chặn) → fsyncdir → unlink temp → fsyncdir → readback final. Không ghi trực tiếp từng byte vào final path. Không hỗ trợ no-replace/link thì chặn, không fallback truncate. Crash trước publish không có final, chưa có target hoặc dispatch; crash sau publish có nguyên bytes đã fsync, ordinary init chặn và recovery theo phase. Cập nhật witness đã tồn tại: temp cùng thư mục → fsync file → atomic replace → fsyncdir → readback; không có gap absent. Lock giữ tới hết.

Witness giữ origin (fresh_init hoặc imported_lineage), enrollment/binding ID, active generation, phase reserved|initialized, witness_revision, high_water {generation,state_revision,state_sha256}, pending_adoption khi có, suspended và history append-only. Full state SHA bao gồm mọi counter/run ID/history, là high-water counter/history digest, không chỉ số revision. phase chỉ đi reserved→initialized một lần, không lùi. Path không đổi qua các generation; witness initialized được đọc/cập nhật cho adoption tiếp, không O_EXCL lần nữa. Chỉ lần chưa từng có witness mới O_EXCL, và authority phải chứng minh fresh/import lineage tương ứng.

Fresh init đòi cả witness và target absent, registration xác minh lineage mới và sentinel absent. Tạo witness reserved durable trước target. Target initial awaiting_lease được dẫn xuất tất định từ exact grant, sau target durable/readback mới chuyển witness initialized với high_water {generation,0,hash(initial bytes)} durable; init chỉ trả thành công sau đó. Mọi mutator/dispatch kiểm witness initialized, binding/active_generation khớp, không pending_adoption và không suspended trước validate, rồi kiểm lại sau persist trước dispatch right.

`init --mode resume-initialization` cần disposition exact enrollment và origin=fresh_init, witness reserved. Target absent ⇒ tạo đúng initial bytes từ grant; target hiện hữu ⇒ chỉ nhận khi byte-for-byte bằng initial bytes ấy rồi chỉ advance witness, không ghi đè target. Sai bytes hoặc witness initialized mà target thiếu ⇒ UNKNOWN, không reset state. Provider không được gọi trong giai đoạn reserved. Witness initialized + target missing/corrupt hoặc hash/revision không khớp là **terminal UNKNOWN/checkpoint trong scope này**. Không có lệnh restore từ backup trong spec này, không giả có nguồn counter để tự khôi phục. Sửa/khôi phục ngoài scope cần Packet/authority/evidence riêng; không cho phép chạy lại từ state cũ.

Adopt-state trong cùng lock: witness tồn tại phải đúng lineage/binding và không có pending khác; nếu lineage v2 chưa có witness thì tạo reserved origin=imported_lineage bằng O_EXCL, giữ source generation/hash đã được admission ghim. History lưu target identity {canonical path,generation,adoption ID,as_of_revision/hash} cho mọi node, kể cả aborted; active node dùng high_water hiện tại, không so nó với hash cũ lúc adoption. Ghi pending_adoption exact ID/generation durable **trước prepared/cutover**, target identity từ binding phải khác mọi target path/generation/adoption ID trong witness history, lstat target absent và publish prepared bằng complete temp + no-replace như witness create; không replace một target không thuộc chính adoption hiện tại; witness tạo/đọc xong mới tới prepared → cutover_started → tombstone → adopted như §3. Witness đã initialized không lùi reserved; pending/suspended chặn ordinary mutator. Sau target adopted durable/readback và mọi tombstone khớp, mới advance witness active_generation, **đặt phase=initialized cả cho imported_lineage reserved**, ghi high_water của target mới, append history và clear pending/suspended atomically/durably. Chỉ sau witness final readback mới kết thúc adoption. Target adopted mà thiếu witness hoặc còn pending ⇒ chặn, không miễn.

Recovery adopt-state nếu witness có pending đúng ID nhưng target chưa được tạo: chỉ được dựng prepared từ source bytes còn đúng hash đã ghim, quiescence và authority còn hợp lệ; source đã là tombstone mà target mất ⇒ UNKNOWN. Nếu target đã adopted nhưng witness chưa advance, recovery kiểm mọi exact hash rồi chỉ finalize witness; không early-return already_completed trước khi witness khớp. Normal mutator không được finalize hộ. initialized witness có history adoption ID đã hoàn tất và target adopted khớp ⇒ replay already_completed_no_dispatch.

Abandon trước cutover giữ aborted target/node trong lineage, clear pending bằng durable update, đặt suspended=true và append aborted history; không cho predecessor tự dispatch lại. imported witness nếu còn reserved vẫn giữ reserved, không xóa để trông như fresh. Adoption lần sau phải có admission/generation/adoption ID mới, dùng lại witness đã tồn tại và giữ toàn history; chỉ clear suspended sau target mới adopted + witness finalize. `init` không bao giờ nhận witness của imported lineage hoặc abandoned adoption làm fresh lineage.

Oracle: mọi điểm crash giữa witness/source/target/cutover/adopted/finalize/abandon đều không reset hoặc dispatch; reserved+initial-target-present chỉ advance witness khi bytes đúng; adopted+missing/pending witness bị chặn. Mutant bỏ witness ở gate, lần kiểm sau persist hoặc adopt-state đều phải đỏ.

Oracle bổ sung: fresh lineage + absent sentinel dương; predecessor + init âm; generation đổi + init âm; sentinel sai/thiếu âm; state đã có/corrupt/symlink âm. Không được xóa lịch sử canonical để làm lineage trông mới.

## 5. Authority của admission

`--admission FILE` chỉ là bản payload để đối chiếu. Consumer phải lấy descriptor từ **frozen Packet spec đã được admission bởi nguồn canonical hiện hành**, không lấy root trust từ FILE, cwd hoặc candidate.

Descriptor bổ sung trong spec/lease được cấp:

```yaml
admission_ref: refs/heads/<metadata-ref>@<OID40>
admission_path: <repo-relative-path>
admission_sha256: <64 lowercase hex>
```

Tái dùng nguồn spec/lease immutable và rollout checks của ADR0063 cùng canonical grant/registration đã có; không thêm registry hoặc control plane. Trước init chưa có executor lease thì descriptor phải có trong frozen Packet spec đã được authority chấp thuận; file spec tùy ý do caller chọn không đủ. Nếu không resolve được Packet spec authoritative từ nguồn canonical đã được cấp thì chặn init, không fallback.

Chuỗi kiểm bắt buộc:

1. Xác minh frozen spec/source authority, registration đúng Mission/Packet/revision/generation và expiry/revocation bằng canonical hiện hành. Candidate tự chứa descriptor không cấp quyền cho chính nó.
2. Đọc Git object đúng OID/path từ ref descriptor; không resolve nhánh trôi. Hash bytes phải bằng admission_sha256. Ref chỉ là nhãn nguồn, không phải chứng minh reachability hiện thời.
3. So bytes của FILE với chính bytes immutable ấy, không chỉ parse rồi so subset. Mọi resolver rejection (FILE/OID/path/hash/spec/generation/revocation/expiry/canonical source lỗi) ⇒ mutator rc 8 trước mọi write, guard-first-publication rc 12 với status admission_rejected. rc 2 chỉ cho argv syntax, không dùng cho rejection dữ liệu FILE. Không có resolver rejection nào cho guard trả 0 hoặc 8. Kể cả FILE khớp, consumer vẫn validate fields và current authority/expiry/revocation.
4. Payload đóng các binding bắt buộc: schema, Mission/plan hash, Packet/spec contract ID/revision/generation, base, coordinator enrollment, state/lock/root identities, predecessor/lineage, source hash khi có predecessor, allowance window/limits và expiry. Không nhúng SHA256 của spec S vào payload A khi S đã ghim hash A: dùng đồ thị hash một chiều S → A. Resolver receipt ràng đồng thời spec_sha256(S) và admission_sha256(A) từ nguồn authority đã xác minh; contract ID trong A phải khớp identity của S. Nếu chọn layout lease ghim A thay vì S thì cũng phải khai đồ thị hash không vòng, không ngầm tạo cặp hash tự tham chiếu. Freshness của grant/revocation là kiểm riêng; OID immutable không tự chứng minh grant còn hiệu lực.
5. `init`, cả hai mode adopt-state, mọi mutator scoped và guard-first-publication dùng cùng resolver này. Không lấy CLI expected hash từ FILE làm root authority.

Closed fixtures phải có positive descriptor hợp lệ và các negative: FILE khác bytes, OID/path sai, same-hash nhưng revoked, wrong Packet/generation, old predecessor, candidate-only descriptor và không resolve được spec canonical. Không dùng test_only descriptor làm production grant.

## 6. Tombstone

Probe r6 minimal tombstone bị v2 từ chối vì thiếu field bắt buộc (`KeyError: reviewer`), **không chứng minh nó đã đi tới nhánh kiểm schema_version**. Không lấy nhãn 13/13 đó thành coverage cho một tombstone khác.

Tombstone đề xuất `packet_state_retired.v1` có đúng các key:

- `format`: chuỗi cố định `packet_state_retired.v1`;
- `packet_id`: int dương, không nhận bool;
- `from_generation`, `to_generation`: int thật, không bool, from không âm, to > from theo binding được cấp;
- `adoption_id`: type(value) is str và `re.fullmatch(r"[a-z0-9][a-z0-9._-]{0,127}", value, flags=re.ASCII)`, đồng thời exact trong authority/record;
- `source_sha256`, `binding_sha256`: đúng 64 lowercase hex.

Không chứa key `packet`, `schema_version`, `reviewer`, `reviews` hoặc payload schema 2. Serialization: JSON UTF-8, `ensure_ascii=False`, `sort_keys=True`, separators `(',', ':')`, **một LF cuối**. Tombstone hash tính từ chính bytes này trước prepared persist, không field hash self-reference.

Golden phải ghi đúng bytes do renderer này sinh; chạy lại đủ 13 entry point trên bytes ấy và kiểm old path cùng target fixture không đổi. Đây vẫn chỉ là proof reader cũ từ chối, không chặn cached private writer. Product acceptance còn phải kiểm đúng renderer/bytes của implementation cùng authority thật; fixture không là production receipt.

## 7. Transaction và dispatch

Gate có common prelude: lock cố định → resolve authority/binding/topology, rồi **nhánh theo command/mode**:
- Ordinary mutator (không init/adopt management): load target, expected state_revision N, witness initialized + active generation/no pending/no suspended, high_water generation/revision/full-state SHA khớp tuyệt đối, legacy tripwire lần 1 → validate → persist state → advance witness high_water → readback cả cặp → kiểm witness/tripwire lần 2 → kết luận → unlock.
- Fresh init: target+witness absent, predecessor none, expected-revision absent; không normal _load. Resume-initialization: witness reserved origin fresh_init, **expected-witness-revision N**, target absent hoặc đúng initial bytes; không expected state_revision vì target có thể chưa có.
- Adopt initial: **expected-witness-revision absent** chỉ khi admission cho imported lineage chưa có witness và source hash exact; nếu witness đã có thì expected-witness-revision N đúng hiện tại. Existing initialized/suspended được nhận chỉ theo admission mới, target mới và điều kiện §3–4, không ordinary gate. Source CAS dùng exact expected-source-sha256, không giả revision cho legacy v2.
- Adopt recovery: expected-witness-revision N, pending phải đúng adoption ID/binding; imported reserved hoặc initialized+pending/suspended được nhận đúng nhánh được mô tả, foreign pending bị chặn. Không tự yêu cầu initialized/no pending trước khi recovery có thể chạy.
- Cả init/adopt chỉ quản trị journal; **không bao giờ trả quyền dispatch provider**. Có chung lock, resolver và durability nhưng predicate phase khác ordinary mutator. Trộn expected-revision và expected-witness-revision sai mode là argv rc2.

Đối với ordinary commit, sau state mới durable/readback phải cập nhật witness high_water bằng atomic replace/fsyncdir/readback trước khi trả kết quả. Revision state tăng 1 trong generation; SHA toàn state bảo vệ mọi counter/history. State và witness không phải commit atomic hai file: bất kỳ mismatch/cutpoint sau crash đều terminal UNKNOWN/checkpoint, không tự promote từ state "ahead", không replay dispatch hoặc restore backup cũ. Chỉ cặp khớp tuyệt đối và mọi gate đạt mới trả success. Profile không hứa tự recovery ordinary-commit crash; recovery adoption/init vẫn theo nhánh riêng. Full journal/VM rollback hoặc mất cả witness lẫn state không được claim phát hiện bằng dữ liệu local: ngoài profile, cần re-enrollment/reconciliation được authority xác nhận trước activation lại.

- Lockfile cố định, không unlink, mở `O_CLOEXEC`; fd không truyền cho provider. Temp cùng filesystem/thư mục. Giữ lock tới sau readback và tripwire lần 2.
- **Chỉ trả `dispatch_allowed=true` sau toàn bộ fsync file, replace, fsyncdir, readback và tripwire lần 2 thành công.** Đây mới là điểm coordinator được phép gọi provider.
- Ordinary expected state revision là input bắt buộc từ snapshot caller đã nhận; init/adopt management dùng đúng revision namespace ở bảng nhánh trên. Thiếu/sai loại ⇒ input_rejected/nonzero; stale ⇒ revision_rejected/nonzero; đúng revision nhưng hết quota ⇒ quota_exhausted/nonzero. Không tự suy revision hoặc dùng source v2 không có revision làm số 0. Mã cụ thể phải freeze theo CLI contract, không dùng rc 77 của prototype như canonical đã có.
- `fsyncdir`/readback/tripwire lỗi sau reservation: giữ slot, không dispatch, kết quả durability_unknown hoặc legacy_changed. Không giảm counter hoặc tự retry. Nếu không biết commit đã tới đâu, lần kiểm tiếp theo checkpoint; không tạo record thay thế để che unknown.
- Process bị kill không thể báo verdict. Harness quan sát process rc và journal sau crash: reservation đã thấy thì replay không được dispatch; missing/corrupt/phase trung gian thì UNKNOWN. Không kết luận mất điện đã được mô phỏng bằng process kill.
- Hash/check regular file trước và sau persist không bảo đảm phát hiện mọi write ngoài profile hoặc write rồi hoàn nguyên. Không suy hai lần check thành fencing tuyệt đối.

## 8. Topology

Đề xuất allowlist **Linux ext4 hoặc XFS**: đồng thời khớp mountinfo filesystem name, `statfs` magic (`0xEF53` cho ext4 kèm name ext4; `0x58465342` cho XFS), target/lock/temp cùng mount đã chọn và capability fsync/replace/readback đạt. Symlink hoặc mount identity trôi thì chặn. NFS/CIFS/9p/virtiofs/FUSE/overlay/tmpfs và FS không xác định không nằm trong profile đầu.

Coordinator ID là ID enrollment được authority ghim cho runtime, kèm boot ID quan sát và root/mount identity. ID này không phải secret hoặc attestation chống root. Mỗi boot thay đổi cần readmission/handoff có quyền, không tự đổi binding. Mount không bị host khác chia sẻ và storage tôn trọng fsync là giả định phải được operator xác nhận, không tuyên bố đã chứng minh tổng quát bằng statfs.

Cloud hiện tại dùng overlay cho prototype; vì vậy các số đo scratch chứng minh thuật toán/CLI controls, **chưa chứng minh production profile ext4/XFS**. Có thể viết và review source ở đó, nhưng không activation profile claim tại đó. Trước activation phải có native Linux runtime phù hợp và evidence thật. Windows focused chỉ test phần phù hợp và đường từ chối claim ngoài profile, không mở mutator claim Windows.

## 9. PR identity và collector

### PR chuẩn bị P

P phải có acceptance và giá trị độc lập nếu land riêng, nằm trong write set, qua offline review exact P trước push và đủ gate áp dụng cho P. Không commit rỗng/trivial chỉ để lấy số PR. P và H dùng cùng lineage, budget và revision/generation đã cấp; đổi binding làm evidence cũ stale.

P chỉ khả thi khi có **lane canonical độc lập đã có trước** để review P trước push mà không cần số PR của chính P. Không đệ quy tạo P0/P1 vô hạn và không để candidate tự mở lane. Nếu scope chỉ cho human schema v1 mà chưa có PR identity, phải checkpoint chọn lane model canonical hoặc sửa contract được duyệt riêng.

Sau khi PR thật từ P tồn tại: tạo H local → review trọn exact H → owner audit theo schema v1 với đúng PR/H/tree/spec/bindings, trước first publication H → controlled publish/readback → collector và CI → canonical K0–K7. Không đổi sang hai schema human mới; review diff P..H chỉ là phần hỗ trợ, không thay review exact H.

Review P tiêu lượt thứ nhất, H tiêu lượt cuối trong trần hai vòng: finding buộc sửa H thì checkpoint. Theo yêu cầu người dùng, mọi P1/P2/P3 phải đóng trước nghiệm thu; không dùng việc P3 có đường K5 để miễn điều kiện zero findings riêng của Packet.

### Collector

Receipt đề xuất đóng field: schema, repo ID/full_name, H, audit comment ID/updated_at/hash, collection start/end, query/ref/event scope, raw snapshot hash, cursor coverage, DAG coverage, earliest matching event ID/time/ref/actor/before/after, residual class IDs và status.

`RECORDED_EARLIEST_MATCH` chỉ là kết quả collector, không phải K4 PASS. `UNKNOWN` khi thiếu page/object, không đọc được phạm vi hoặc gặp introduction không hỗ trợ; `FAIL` khi H/descendant có publication sớm hơn audit bắt buộc. Comment sửa sau publication phải kiểm lại theo updated_at. Giữ full K2/raw earliest run và logic/rc `_human_merge` hiện hành.

Residual policy đề xuất chỉ có hai lớp: hoạt động server không được API công bố; object storage của fork nằm ngoài repo/ref scope đã khai. Owner phải duyệt policy trước activation. **Retention hoặc thiếu page trong phạm vi cần kiểm không được đổi nhãn thành residual.** Một đường introduction thực tế không được hỗ trợ vẫn UNKNOWN.

Đọc lại API do eventual consistency tối đa ba lần trong một cửa sổ 180 giây; mỗi lần thu tối đa 100 trang/120 giây/30 MiB và phải còn trong wall deadline chung. Hết số lần/thời gian ⇒ UNKNOWN, không PASS do timeout, không mở thêm invocation provider. Consumer đề xuất là command read-only `guard-first-publication --packet N --admission FILE --receipt FILE`, chạy canonical có hiệu lực sau rollout trước `kiem-merge`. Nó không ghi state; exit 0 chỉ khi điều kiện collector/audit/publication đủ theo policy đã duyệt, exit 12 cho FAIL, UNKNOWN hoặc admission_rejected kèm JSON status phân biệt, exit 2 cho lỗi đối số. Chưa có command production mới được triển khai trong bản này.

## 10. Inventory, acceptance và hình dạng kế thừa

Inventory product dự kiến: 13 mutator legacy + adopt-state (initial/recovery cùng command), tổng 14. guard-first-publication read-only. Không thêm writer recovery thứ 15 hoặc writer ngoài transaction gate. Mã thoát đóng: argv/input syntax rc2; exhausted/quota rc3; mutator authority/state/revision/witness mismatch, UNKNOWN, durability_unknown, legacy_changed đều rc8 và dispatch_allowed=false; guard resolver rejection rc12/admission_rejected; guard evidence FAIL/UNKNOWN rc12 với status tương ứng; success rc0 chỉ cho completed_no_dispatch, already_completed_no_dispatch hoặc reserved_for_dispatch. **Chỉ rc0 + status reserved_for_dispatch + dispatch_allowed=true** cấp quyền gọi provider; rc0 đơn lẻ không đủ. Mọi status chưa biết không được mặc định rc0. Init/adopt và replay luôn no_dispatch. Frozen fixtures phải đối chiếu cả parser và call graph trước source lease.

Các lớp do reviewer quyết định sau khi quét mọi biểu hiện; các nhóm sau là handoff, không là trần review:

| Slug ổn định đề xuất | Biểu hiện nguồn | Phép kiểm đóng |
|---|---|---|
| legacy-writer-reentry | r5 N1, A1 đã đóng ở thiết kế | Tombstone đúng bytes; quiescence/producer coverage trước activation; cached writer không bị gọi là đã fence |
| adoption-lineage-counter-integrity | r5 N2 và A1 F2 | Exact source bytes, missing/corrupt UNKNOWN; fresh init predecessor none+absent; không reset generation/history |
| dispatch-durability-order | r5 N3 | Quyền dispatch chỉ sau fsync/readback/tripwire; lỗi giữ slot, không retry |
| pr-preparation-identity | r5 N4 | P có giá trị độc lập, PR ID thật, review exact H, budget chung |
| recovery-state-machine | A1 F1/P2 | Hai mode, disposition đóng, durable cutover intent, reboot readmission, không rollback schema 2 |
| admission-authority-anchor | A1 F3/P2 | Ref/OID/path/hash từ authority canonical; FILE không là trust root; tránh hash cycle |
| tombstone-bytes-coverage | A1 F4/P3 | Golden đúng renderer/tập field, lý do từ chối đúng, không gán fixture thành product acceptance |

Có 8 finding ID nguồn (N1–N4, A1 F1–F4), dự kiến 7 lớp; N2 và F2 nối cùng cơ chế counter/lineage, không giảm severity. Reviewer phải xác nhận hoặc sửa phân lớp, nêu lý do tách/gộp và mọi biểu hiện cùng cơ chế còn lại. A1 có 4 finding mở trong 4 lớp; lớp lineage không được ghi closed chỉ vì biểu hiện adopt-state đã đóng.

Acceptance cho implementation: init dương/âm; adoption exact bytes; crash trước/sau cutover intent/tombstone/adopted; missing/corrupt không reset; resolver authority sai OID/path/hash/revocation; contention đúng một reservation; mọi writer cùng gate; fsync/readback lỗi không dispatch; topology dương thật và ngoài profile âm; full advisory→actual human→canonical gates lifecycle; scope ngoài Mission không nới. Mỗi ca cần negative/mutant oracle trong frozen inventory; chưa có product tests nào chạy trong proposal này.

Bằng chứng đã có: r7 golden tombstone 13/13 legacy CLI từ chối (hash 99aa16ab7d70793d36361757fe84a883ddb5b86fbd1dd85ed2948bfdb34d0c03), chỉ là prototype fixture của revision r7, KHÔNG là coverage renderer revision hiện hành; phản chứng cached writer phục hồi schema 2; prototype single host 7/7; không production migration, Windows claim, power-loss hoặc cross-host proof. Root phải mang raw results/hash vào review bundle, không chỉ tổng suite.

## 11. ADR-0060 và publication

M1/M2: reviewer quét theo lớp, giữ slug và đọc nghĩa, zero P0/P1/P2; mọi P3 phải reviewer xác nhận đóng hoặc owner miễn exact H. Yêu cầu riêng của #1174 vẫn zero P1/P2/P3 trước nghiệm thu. Không reset history qua C5-A2.

M5/M12: local candidate H/tree và diff được freeze, handoff lên Packet Issue, cross review độc lập offline hai trục trước push. Có commit mới thì review/gates cũ stale. Không push candidate chưa approve; không đổi namespace để miễn push count. Không tự coi bundle hash cũ là Git SHA.

M6/M7: chưa nói sẵn sàng merge, bỏ draft, formal Approve/merge/land khi thiếu CI/connector/exact owner authority. Nếu proposal có PR, nó là làn thường, không M8 archival. Không mở PR/CI hoặc dùng budget source B trước khi đủ authority riêng.

M10: declaration ở đầu là anchor dự kiến; khi lease trỏ đúng spec_hash, phải đo hiệu lực ADR trên canonical non-shallow/first-parent và commit giới thiệu. Trước khi có lease/candidate implementation, review proposal là advisory spec review, không tự thành K4/kiem-merge pass hoặc Packet accepted.

M9/Windows của implementation đọc lại theo diff thật; không lấy not_required của Markdown proposal áp cho packet_loop/protocol code về sau. Không CI Windows/full mutant Windows theo owner; Linux CI/full M9 giữ khi scope triggered.

Ngân sách: C5-A1 đã tiêu 1 closure, giữ raw needs_revision. C5-A2 là lượt bổ sung được yêu cầu với quy trình vá/cross review cho cả lịch sử A1 lẫn candidate này. Source B vẫn 2 executor +2 reviewer chưa mở, không chuyển slot để chạy thêm closure tùy ý; không mua credits. Chạm trần thì checkpoint.

Chưa đo: product tests, actual human, remote runs, merge/land, capability native ext4/XFS và complete ownership của write set implementation. Đặc tả không tự cấp quyền cho những bước đó.

## 12. Hình dạng kế thừa từ A2

A2-01/P2 thuộc adoption-lineage-counter-integrity: witness outside target; A2-02/P3 thuộc recovery-state-machine: aborted generation nằm trong lineage và cần admission mới; A2-03/P3 thuộc admission-authority-anchor: guard map resolver error ra12/admission_rejected; A2-04/P3 thuộc tombstone-bytes-coverage: bool/grammar và golden bytes. Các thay đổi này mới là executor patch, chưa reviewer xác nhận đóng. Review A2 trên H trước chỉ đọc snapshot do prompt lỗi cấm Git; không dùng nó làm M12 approval hồi tố. Không push candidate mới trước offline review hợp lệ.
