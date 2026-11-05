dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# WP1174 C5-A2 — Candidate đặc tả r8 (chưa freeze/lease)

- packet_id: WP1174; revision: 1; design_revision: 8;
- packet_issue: 1174
- review_class: sensitive
- candidate_kind: specification_proposal_only
- source_lease: none
- base: 825eb3561a94e05c36045d2c981b4108c523e31c

## 1. Assignment và giới hạn

Nguồn: chủ kho duyệt C5 ở #1172 comment 6666000374, rồi yêu cầu “Thực hiện đúng quy trình vá, cross review theo ADR 0060 đi, cho cả C5-A2 và C5-A1”. Candidate này hợp nhất sửa đổi r6→r7 thành một đặc tả duy nhất để cross review offline; không có implementation adapter, không tự cấp source authority. Lease/spec_hash và rollout M10 còn cần xác minh trước code Packet; chỉ thêm dòng ADR không tự kích hoạt hiệu lực.

Write set thực tế của proposal: `ops/specs/wp1174-c5-a2-design-r8.md` (một Markdown). Ngoài scope: product packet_loop/launcher/protocol, workflows, credential, registry, LIVE, merge/land. Write set implementation #1174 phải đóng băng riêng sau spec đạt và ownership rõ. Không mở source B qua commit proposal này.

M3 của diff Markdown-only: đề nghị not_required, reviewer quyết định; M9 full mutant không triggered bởi diff này. Windows CI/full mutant Windows vẫn bị cấm; native Windows focused được phép khi áp dụng. Không gọi những gate chưa chạy là passed. Spec proposal không được coi là M8 archival vì nằm trong ops/specs.

Executor/preparer: Codex service; reviewer: Claude Code độc lập, requested Opus 5.5/high, hai trục Spec và Standards/Security. Review source về sau giữ routing, actual human và gates riêng. C5-A1 giữ needs_revision lịch sử, không được sửa thành approve hồi tố.

## 2. Profile và activation

Profile đầu tiên chỉ có một coordinator Linux, một journal Packet đã được authority canonical chọn, local durable filesystem và các producer đáng tin tuân thủ admission. Không hứa chống admin malicious, arbitrary private writes hoặc distributed exactly-once.

Đường dispatch hợp lệ chỉ nằm ở coordinator được giao. Trước adoption phải đóng admission cũ, để mọi request cũ tới terminal hoặc unknown đã được đối soát, nhận handoff của các writer đang được đăng ký và xác nhận không còn writer v2 đang giữ snapshot để ghi. Không tự giết process của Packet khác, đổi ACL, chặn tài khoản hoặc thêm registry mới.

Không kiểm chứng được quiescence/lineage/budget/producer coverage thì **không adoption hoặc activation**. Snapshot process hay hostname đơn lẻ không phải attestation đầy đủ. Resume phải đọc lại facts, không dùng handoff cũ như grant mới.

## 3. Adoption và recovery

Giữ **14 mutator**, vì recovery là mode của `adopt-state`, không là command thứ 15. Hai mode loại trừ nhau:

- `adopt-state ... --mode initial --expected-source-sha256 HASH --expected-revision N --target-generation N`.
- `adopt-state ... --mode recovery --adoption-id ID --disposition resume_forward|abandon_before_cutover --expected-revision N`.

Cả hai mode cần admission/authority còn hiệu lực, exact adoption ID và generation; sau reboot phải readmission vì boot ID đổi. Các argument chỉ đối chiếu, không tự tạo authority. Không tự suy disposition từ lỗi.

### Record và thứ tự cutover

Prepared state giữ immutable source snapshot, hash bytes nguồn, deterministic target payload, tombstone bytes/hash, binding hash và lineage. `prepared_payload_sha256` được tính từ **immutable payload projection** đã liệt kê, loại trừ field hash của chính nó và các field phase/revision tiến trình; không dùng self-referential whole-file hash. Validator dẫn xuất lại payload từ source snapshot có hash ghim trong admission.

Trước khi thử ghi tombstone, ghi durable `cutover_started: true` vào prepared journal và readback; chỉ sau đó mới động tới path cũ. Flag này monotonic, không về false. Sau tombstone durable/readback, mới chuyển target adopted. Quiescence giữ xuyên quy trình. Đây là state machine nhiều bước, không hứa atomic nhiều file.

| Disposition | Preconditions | Hành động |
|---|---|---|
| resume_forward | Target prepared đúng immutable payload/hash/binding; old path có đúng source hash hoặc đúng tombstone hash | Nếu còn source, hoàn tất intent flag rồi tombstone; nếu đã tombstone, giữ bytes; chỉ chuyển adopted sau full durable/readback và tripwire |
| abandon_before_cutover | Target prepared, `cutover_started` được đọc chắc chắn là false, old path đúng source hash, authority cho phép abandon | Ghi target aborted có lịch sử, không xóa target/history; giữ admission paused. Không tự cho old generation dispatch trở lại |
| Bất kỳ mode gặp dữ liệu khác | Missing/corrupt, sai hash/ID/generation, intent unknown, old path không thuộc hai hash | UNKNOWN, không sửa hay dispatch |

Nếu intent đã true, dù old path còn source do crash, chỉ xét resume_forward; không abandon. Không bao giờ ghi lại schema 2 sau khi có khả năng đã bắt đầu tombstone. Với target adopted cùng adoption ID, replay recovery chỉ trả `already_completed_no_dispatch`, không ghi counter hoặc dispatch.

Oracle thêm vào R6-A02: crash trước/sau durable intent, trước/sau tombstone và adopted; recovery đúng từng nhánh; abandon sau intent bị chặn; corrupt/missing giữ UNKNOWN; không rollback schema 2; boot đổi chưa readmission bị chặn. Các oracle này **chưa có implementation/test**.

## 4. Fresh init và lineage

Scoped `init` là ngoại lệ hẹp của gate load-state:

1. Admission canonical phải khai rõ `predecessor: none`, không source path/hash, generation đầu được cấp và lineage chưa từng dùng; authority/allowance/admission có thể có trước executor lease.
2. CLI phải truyền sentinel **`--expected-revision absent`**. Chỉ scoped init mới nhận sentinel này. Mọi mutator khác đòi số nguyên revision hợp lệ; không tự coi thiếu revision là absent.
3. Lấy lock, xác minh authority và absence bằng lstat cho đúng target; target tồn tại hoặc symlink thì rc 8. Không gọi normal `_load` cho target absent.
4. Tạo state `awaiting_lease`, counters ban đầu đúng grant và revision đầu quy định trong schema; chưa cấp quyền source/attempt/dispatch. Full executor lease vẫn được kiểm riêng ở transition tương ứng.

Admission có predecessor/source, lineage đã có history/counter hoặc không chứng minh được lineage mới ⇒ init rc 8, không tạo file. Missing target của generation đã được khai predecessor hoặc đã init trước đây ⇒ UNKNOWN, không init lại. `adopt-state` là lệnh duy nhất tạo **target có predecessor**.

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
3. So bytes của FILE với chính bytes immutable ấy, không chỉ parse rồi so subset. FILE khác hash/bytes ⇒ rc 8 trước mọi write. Kể cả FILE khớp, consumer vẫn validate fields và current authority/expiry/revocation.
4. Payload đóng các binding bắt buộc: schema, Mission/plan hash, Packet/spec contract ID/revision/generation, base, coordinator enrollment, state/lock/root identities, predecessor/lineage, source hash khi có predecessor, allowance window/limits và expiry. Không nhúng SHA256 của spec S vào payload A khi S đã ghim hash A: dùng đồ thị hash một chiều S → A. Resolver receipt ràng đồng thời spec_sha256(S) và admission_sha256(A) từ nguồn authority đã xác minh; contract ID trong A phải khớp identity của S. Nếu chọn layout lease ghim A thay vì S thì cũng phải khai đồ thị hash không vòng, không ngầm tạo cặp hash tự tham chiếu. Freshness của grant/revocation là kiểm riêng; OID immutable không tự chứng minh grant còn hiệu lực.
5. `init`, cả hai mode adopt-state, mọi mutator scoped và guard-first-publication dùng cùng resolver này. Không lấy CLI expected hash từ FILE làm root authority.

Closed fixtures phải có positive descriptor hợp lệ và các negative: FILE khác bytes, OID/path sai, same-hash nhưng revoked, wrong Packet/generation, old predecessor, candidate-only descriptor và không resolve được spec canonical. Không dùng test_only descriptor làm production grant.

## 6. Tombstone

Probe r6 minimal tombstone bị v2 từ chối vì thiếu field bắt buộc (`KeyError: reviewer`), **không chứng minh nó đã đi tới nhánh kiểm schema_version**. Không lấy nhãn 13/13 đó thành coverage cho một tombstone khác.

Tombstone đề xuất `packet_state_retired.v1` có đúng các key:

- `format`: chuỗi cố định `packet_state_retired.v1`;
- `packet_id`: int dương, không nhận bool;
- `from_generation`, `to_generation`: int, from không âm, to > from theo binding được cấp;
- `adoption_id`: ID exact trong authority/record;
- `source_sha256`, `binding_sha256`: đúng 64 lowercase hex.

Không chứa key `packet`, `schema_version`, `reviewer`, `reviews` hoặc payload schema 2. Serialization: JSON UTF-8, `ensure_ascii=False`, `sort_keys=True`, separators `(',', ':')`, **một LF cuối**. Tombstone hash tính từ chính bytes này trước prepared persist, không field hash self-reference.

Golden phải ghi đúng bytes do renderer này sinh; chạy lại đủ 13 entry point trên bytes ấy và kiểm old path cùng target fixture không đổi. Đây vẫn chỉ là proof reader cũ từ chối, không chặn cached private writer. Product acceptance còn phải kiểm đúng renderer/bytes của implementation cùng authority thật; fixture không là production receipt.

## 7. Transaction và dispatch

Gate gồm 13 entry point legacy và adopt-state (14 mutator tổng). Fresh init dùng nhánh absent được mô tả riêng, không load target chưa tồn tại. Các trường hợp còn lại đi qua: lấy lock → load → kiểm authority/binding/topology/revision/phase và tripwire lần 1 → validate → mutate/reserve → persist durable → readback → tripwire lần 2 → kết luận → nhả lock.

- Lockfile cố định, không unlink, mở `O_CLOEXEC`; fd không truyền cho provider. Temp cùng filesystem/thư mục. Giữ lock tới sau readback và tripwire lần 2.
- **Chỉ trả `dispatch_allowed=true` sau toàn bộ fsync file, replace, fsyncdir, readback và tripwire lần 2 thành công.** Đây mới là điểm coordinator được phép gọi provider.
- Expected revision là input bắt buộc từ snapshot caller đã nhận. Thiếu ⇒ input_rejected/nonzero; stale ⇒ revision_rejected/nonzero; đúng revision nhưng hết quota ⇒ quota_exhausted/nonzero. Không tự biến revision thành optional để tạo rc 3. Mã cụ thể phải freeze theo CLI contract, không dùng rc 77 của prototype như canonical đã có.
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

Đọc lại API do eventual consistency tối đa ba lần trong một cửa sổ 180 giây; mỗi lần thu tối đa 100 trang/120 giây/30 MiB và phải còn trong wall deadline chung. Hết số lần/thời gian ⇒ UNKNOWN, không PASS do timeout, không mở thêm invocation provider. Consumer đề xuất là command read-only `guard-first-publication --packet N --admission FILE --receipt FILE`, chạy canonical có hiệu lực sau rollout trước `kiem-merge`. Nó không ghi state; exit 0 chỉ khi điều kiện collector/audit/publication đủ theo policy đã duyệt, exit 12 cho FAIL hoặc UNKNOWN kèm JSON status phân biệt, exit 2 cho lỗi đối số. Chưa có command production mới được triển khai trong bản này.

## 10. Inventory, acceptance và hình dạng kế thừa

Inventory product dự kiến: 13 mutator legacy + adopt-state (initial/recovery cùng command), tổng 14. guard-first-publication read-only. Không thêm writer recovery thứ 15 hoặc writer ngoài transaction gate. Mã thoát: input 2; state/revision/authority mismatch 8; exhausted 3; gate UNKNOWN/FAIL 12; thành công 0 có status riêng. Frozen fixtures phải đối chiếu cả parser và call graph trước source lease.

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

Bằng chứng đã có: r7 golden tombstone 13/13 legacy CLI từ chối (hash 99aa16ab7d70793d36361757fe84a883ddb5b86fbd1dd85ed2948bfdb34d0c03); phản chứng cached writer phục hồi schema 2; prototype single host 7/7; không production migration, Windows claim, power-loss hoặc cross-host proof. Root phải mang raw results/hash vào review bundle, không chỉ tổng suite.

## 11. ADR-0060 và publication

M1/M2: reviewer quét theo lớp, giữ slug và đọc nghĩa, zero P0/P1/P2; mọi P3 phải reviewer xác nhận đóng hoặc owner miễn exact H. Yêu cầu riêng của #1174 vẫn zero P1/P2/P3 trước nghiệm thu. Không reset history qua C5-A2.

M5/M12: local candidate H/tree và diff được freeze, handoff lên Packet Issue, cross review độc lập offline hai trục trước push. Có commit mới thì review/gates cũ stale. Không push candidate chưa approve; không đổi namespace để miễn push count. Không tự coi bundle hash cũ là Git SHA.

M6/M7: chưa nói sẵn sàng merge, bỏ draft, formal Approve/merge/land khi thiếu CI/connector/exact owner authority. Nếu proposal có PR, nó là làn thường, không M8 archival. Không mở PR/CI hoặc dùng budget source B trước khi đủ authority riêng.

M10: declaration ở đầu là anchor dự kiến; khi lease trỏ đúng spec_hash, phải đo hiệu lực ADR trên canonical non-shallow/first-parent và commit giới thiệu. Trước khi có lease/candidate implementation, review proposal là advisory spec review, không tự thành K4/kiem-merge pass hoặc Packet accepted.

M9/Windows của implementation đọc lại theo diff thật; không lấy not_required của Markdown proposal áp cho packet_loop/protocol code về sau. Không CI Windows/full mutant Windows theo owner; Linux CI/full M9 giữ khi scope triggered.

Ngân sách: C5-A1 đã tiêu 1 closure, giữ raw needs_revision. C5-A2 là lượt bổ sung được yêu cầu với quy trình vá/cross review cho cả lịch sử A1 lẫn candidate này. Source B vẫn 2 executor +2 reviewer chưa mở, không chuyển slot để chạy thêm closure tùy ý; không mua credits. Chạm trần thì checkpoint.

Chưa đo: product tests, actual human, remote runs, merge/land, capability native ext4/XFS và complete ownership của write set implementation. Đặc tả không tự cấp quyền cho những bước đó.
