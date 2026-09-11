verdict: changes_requested
reviewed_spec_sha256: 415ce35db32aa370ce43315c1ff6d4db7b59005e6288538e72705ce4caed4d0e
model_tu_khai: GPT-6 / Codex theo cấu hình phiên; provider OpenAI, API với công cụ shell cục bộ, transport machine. Không có chứng thực độc lập biến thể backend/effort; không tự khai gpt-6-astra/xhigh từ tiêu đề hay submitter.

# Cross-review r4 — lượt 4b, lời gọi 5/6

**changes_requested — 4 P1 + 2 P2 còn lại**, gom theo 6 nguyên nhân S1–S6, không cộng đúp ID lịch sử. R1 còn một phần; R2–R10 đóng đúng vấn đề cũ. S1 là phần tiếp diễn R1; S2/S3 không phủ nhận việc R2 đã sửa replacement. Đây là review đặc tả, chưa có implementation r4 để nghiệm thu A1–A12 N/N.

Bắt đầu 2026-09-07T21:31:10Z; khung verdict ghi từ đầu lượt, bổ sung các kết luận lúc 21:36Z và 21:40Z trước bản hoàn chỉnh này. Neo Q13/Q14: PR #475 comment 5575587924 được **chấp nhận theo chỉ thị user như lời khai điều phối đã readback offline**. Không đòi chốt lại hai lựa chọn ấy; không giả đã tự gọi API.

HEAD `b416830ef2a509d60203d55552ce17950afcf67c`; tree `266a2aba97d925dac3ab7473dda55adb0fe23b8e`; core.abbrev=7. SPEC trong cay-kho cùng hash. Kho review chỉ đọc; fixture, copies vàoutput mới trong `scratch/r4b/` hoặc hai artifact được yêu cầu ở cwd. Không mạng; không đọc task-data ngoài cwd. Không tự soạn/chạy hướng đổi nguồn/đổi cây bị cấm. Không gọi reviewer/subagent, không commit/push/comment/merge.

`HINT.patch` là unified diff `patch -p0` chỉ lên SPEC.md, phủ mọi S1–S6 và cập nhật accounting. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Đây là đề xuất chữ hợp đồng; không phải code authority do reviewer tự viết rồi tự duyệt. Hint không cấp authority còn thiếu và không cho tự tiếp tục packet qua stop condition.

## Bảng finding lượt 1–3 → trạng thái

“ĐÓNG” = hợp đồng đã sửa finding cụ thể, không phải chứng nhận triển khai. Giữ nguyên hạng lịch sử. Có 35 hàng: R=9 đóng/1 một phần; N=10 đóng/1 một phần; L1=11 đóng/3 một phần. Không có finding cũ bị ĐÓNG SAI trong r4 theo các phản chứng được kiểm ở đây.

Ký hiệu bằng chứng: **P** `scratch/r4b/probes-r4.json`; **E** `extra-r4.json`; **G** `coverage-r4.json`; **L** `loop-r4.json`; **D** `measure-r4.json`; **K** `controls-r4b.json`. Tất cả thuộc `scratch/r4b/`; **K2** là `default-control-r4b.json`. JSON cũ tại `scratch/` là bằng chứng kế thừa 4a, được ghi riêng khi dùng.

| ID lịch sử | Hạng | Trạng thái r4 | Bằng chứng và giới hạn |
|---|---|---|---|
| R1 canonical-url-check-does-not-bind-transport | P1 | ĐÓNG-MỘT-PHẦN | URL tường minh + repository rỗng đóng config origin trực tiếp; môi trường tiến trình/profile vẫn chưa thành hợp đồng đủ. S1. Control K rc=0; hướng đổi nguồn chỉ mô tả. |
| R2 replace-refs-bypass-oid-pinning | P1 | ĐÓNG | Q4.5 bắt cả biến và cờ CLI trên object/ancestry/diff, giữ cây thô hoặc 12. Không chạy lại replacement ở 4b. S2 là identity bytes cache khác; S3 là chọn mutant A6 sai, không phủ nhận fix replacement. |
| R3 bootstrap-gate-trusts-pr-and-arrives-too-late | P1 | ĐÓNG | Workflow có ởA0; biên audit chủ kho + giữ đóng cập nhật + readback trước A1. P bootstrap: rỗng 0, T có sổ 12, bỏ test/workflow vẫn12, S bẩn 12. Audit chỉ rỗng không đủ, nhưng r4 còn đòi review/gate theo §8. |
| R4 inactive-a0-already-changes-lease-decisions | P1 | ĐÓNG | Q3/M3/Q5 giữ verdict cũ, luật mới chỉ DU_BAO không đổi rc; mọi consumer sổ không rỗng 12. P forecast 0/dự báo 8; mutant áp sớm 8. L 5 cửa inactive giữ hành vi cũ. |
| R5 admission-head-is-not-the-landed-candidate | P1 | ĐÓNG | M9 exact S, event/fetched H bằng nhau, T=tree(H), current base S, tree(M)=T, strict/no queue. P control 0; drift/fetch/tree/checker sai 12. Giao diện phát/tiêu check còn thiếu mới S5(P2), facts ngoài kho not_run. |
| R6 self-declared-effective-set-shrinks-exclusion | P1 | ĐÓNG | Q3 tính lại closure, [] sai ở cảY/W đều 8; claim đúng giữ 11. Q13 là ngoại lệ đã được cấp, không còn fallback tự phát của r3. Mâu thuẫn A5/biểu diễn ready mới S4; vòng đời ngoại lệ S6. |
| R7 symlink-resolution-lacks-source-and-termination-contract | P2 | ĐÓNG | Q3 giữ từng occurrenceOID, hợp đích, relative parent, visited/depth và 12. E cùng blob hai cây ra other/a.md và docs/a.md, hợp va chạm11; vòng12; parent tệp mới đúng. |
| R8 cutover-delta-and-fixed-g2-smoke-conflict | P1 | ĐÓNG | Q6 phân loại(a)/(b)/(c), C không phải prerequisiteA1; C=null, g3 riêng theo Q11. E gate1→4 trước hạn, g2 hết09:52; sau C tập rỗng ở10:17:12. Không còn assert1g2 cố định. |
| R9 a8-mode-case-cannot-kill-stated-mutant | P1 | ĐÓNG | P Git mode: bản đúng8, only-new 8 sống, combined 0 bị assertion giết; unit full T12. R4 khai đúng shielding, không nhận công cho single mutant. |
| R10 spec-review-label-does-not-waive-review-cap | P1 | ĐÓNG | Q14/comment 5575587924 đã chốt6 theo lời khai được user cho chấp nhận. 4a đã sinh output tính4,4b tính5/6; không reset PR/slice. Còn stop nguồn tin cậy trước tự dùng lượt 6. |
| N1 canonical-remote-identity-unbound | P1 | ĐÓNG-MỘT-PHẦN | K adapter đúng endpoint/default/map rc=0; lời so URL đã thay. Phần biên process vẫnR1/S1. |
| N2 snapshot-pinned-after-unverified-recapture | P1 | ĐÓNG | Q4 chụp local/remote maps trước, canonical OID từ advertisement đã so. K đổi ref hợp lệ sau capture vẫn đọcS cũ; không recapture. |
| N3 admission-workflow-does-not-cover-canonical-updates | P1 | ĐÓNG | M9 riêng không path/author/rc9 filter; opened/reopened/sync/ready/edited, dispatch có input; direct push/bypass/queue chặn trước activation. E ma trận event model, Actions thật not_run; S5 là interface mới. |
| N4 canonical-checker-bootstrap-is-circular | P1 | ĐÓNG | A0 chứa workflow/checker inactive, lần đầu có audit ngoài workflow, giữ đóng tới readback. A1 base=A0 có command. Nền thật chưa có command(rc=2) là phép đo hiện trạng, không yêu cầu code tương lai có trước lease viết nó. |
| N5 effective-write-set-and-symlink-resolution-missing | P1 | ĐÓNG | Q3 closure tính lại + symlink theo occurrence/parent/vòng, Q13 có authority. P/E claims8, alias11, vòng12. Không coi việc chủ kho chấp nhận approximation tạm là lỗi fallback r3 còn nguyên. |
| N6 historical-cutoff-revives-feature-holders | P1 | ĐÓNG | Giữ mốc A0 readback; G dẫn xuất hai cây fixed W 8/mutant 0; E đo gate1→4 và Q6 cho delta bảo thủ có điều kiện, không tuyên bố gate không đổi. |
| N7 candidate-map-omits-entry-mode | P1 | ĐÓNG | M4 map path→mode/type/blob; P đổi mode cùng blob8; full T unit 12. Không materialize symlink mode có nội dung YAML. |
| N8 record-lease-guard-has-no-candidate-id | P1 | ĐÓNG | L route thật + guard tiêm: record-lease lấy candidate x từ awaiting_lease/null; live 0/leased, revoked 8/stale/event x, không record_lease; old-ID mutant không đạt. |
| N9 acceptance-prepublish-and-second-parent-contradictions | P1 | ĐÓNG | P pure0/0 và CLI12 trước publish tách biệt; sau publish11/11. Parent2 giữ entry 0/mất8. E exact pair phân biệt wrongpath/wrongblob/tag/pull/local-only12. |
| N10 authorization-json-and-url-contract-is-open | P2 | ĐÓNG | Q2 Issue comment đúng repo/Issue/globalID/login, đúng6 keys/type/duplicate/block. P/G correct0, float/duplicate/prose8, bad account 4, envelope12. Không readback API thật. |
| N11 readback-after-admission-lifecycle-undefined | P2 | ĐÓNG | Q2.3/A9 mọi lần delta trước canonical đều đọc lại; sau canonical không đọc căn cứ cũ. P stateful200→0, recheck404→12, downstream thêm 0 calls. |
| L1 authority-signature-evidence-false | P1 | ĐÓNG | D raw Git đếm1 gpgsigPGP b416830,1 gpgsigSSH6635379; marker BEGIN/END không phải2 signature. Không suy signer/human từ raw author hoặc APIactor. |
| L1 default-ref-is-untrusted-cache | P1 | ĐÓNG-MỘT-PHẦN | Q4 chọn server symref đã so, không localalias/fallback; control K đúngmaster. Danh tính nguồn/process còn R1/S1; không chạy nguồn giả. |
| L1 standalone-revocation-has-no-admission-gate | P1 | ĐÓNG | Q2/M4/M9 phủ bản ghi riêng và mọiPRdefault, A0 có bootstrap riêng; P standalone404→12. Receipt trên check thật còn S5(P2), không nhận model làm Actions. |
| L1 evidence-mention-is-not-an-authorization | P1 | ĐÓNG | Q2 đòi khối JSON lệnh và so giá trị/kiểu; P prose/prefix/broken8, correct0. |
| L1 write-set-exclusion-is-incomplete | P1 | ĐÓNG | Q3 mọi lease/closure/symlink/exact-prefix/casefold; P/E chạy các ca hợp lệ. Ngoại lệQ13 có authority, lifecycleS6 tách riêng. |
| L1 snapshot-check-does-not-fence-writers | P1 | ĐÓNG | Q3 pure snapshot không acquire; Q11 C→dừng worker→g3check/land/readback→start. Không khai M7 làm fencing ởland; nợ giữ nguyên. |
| L1 reads-are-not-pinned-to-one-snapshot | P1 | ĐÓNG | Q4 giữ map cả localheads trước so + mộtclock; K pinning control giữ S sau refupdate. S2 là content identity mới, không tái nhận recapture. |
| L1 legacy-fallback-conflicts-with-ledger | P1 | ĐÓNG | P legacyoldcopy0, reservation8 dù historyX→Y, historicalreverse8; active switchQ3 và deltaQ6 đã sửa. |
| L1 append-only-check-misses-candidate-and-merges | P1 | ĐÓNG | P candidate sửa8, parent2keep0/loss8, mode8; M9 exactmerge/currentbase. S2 rawcache là vector khác; không suy native log rỗng là append-only. |
| L1 packet-loop-guard-is-partial-and-boolean | P1 | ĐÓNG | Q5 target ID/5 cửa/3trạngthái; L 35 tổ hợp gồm 25 cũ +10inactive, unknown byte-match, revoked durable/idempotent. Helper-only mutant còn cho3route qua bị phát hiện. |
| L1 acceptance-confuses-refs-blobs-and-mutations | P1 | ĐÓNG-MỘT-PHẦN | G xác nhận3pair/4 refs và 1pair/3 refs theo hợp đồng, A8 sửa đúng. Nhưng A6 vẫn hứa giết single mutant bị che(S3), A5 tráiQ13(S4). GiữP1 lịch sử. |
| L1 revocation-schema-and-error-contract-incomplete | P2 | ĐÓNG | M1 kế thừa r3 hash ghim, mapping/duplicate/mode/ID/types/rc=4/8/12/errororder; Q2 bổ sungJSON. Không khai full parser r4 đã chạy. |
| L1 size-estimate-and-slice-anchor-are-stale | P2 | ĐÓNG | D numstat409/368/328 và 31commit đúng; r4 tổng825–1195,6 path, chỉ A0 vượt300. Ước lượng chưa là numstatimplementation. |
| L1 ready-and-rollout-decisions-are-not-closed | P2 | ĐÓNG-MỘT-PHẦN | Q7–Q12 tách hợp đồng/facts và proposed/inactive. Còn giao diệncheckS5, descriptor/phạm vingoại lệS6; A5/ready fields S4. GiữP2 lịch sử, không cộng đúp. |

## Findings mới

### S1 — adapter-environment-boundary-is-not-specified · P1 · tiếp diễn R1

**Vị trí:** SPEC:165–173 (Q4.1), A2, Q12; tuyên bố “cô lập khỏi mọi config runtime” ở phần hình dạng kế thừa.

Q4.1 đã sửa đúng việc discovery qua tên origin: URL tường minh, repository mới, nguồn credential/proxy tin cậy. Nhưng thao tác được chỉ ra chỉ tắt system/global config và giới hạn tên protocol. Nó chưa định nghĩa môi trường con được dựng từ đâu, trường nào được kế thừa, Git executable/transport implementation nào được tin, hay việc chọn repository/template/include gián tiếp chịu biên nào. “Profile chưa đo ⇒12” chưa có predicate đủ để đo những phần này. Đây là phần còn thiếu của biên nguồn, không phải yêu cầu chứng minh an toàn nếu toàn bộ máy tin cậy đã bị chiếm.

**MÔ TẢ BẰNG LỜI, not_run ở 4b:** nếu caller không tin cậy còn có thể ảnh hưởng lựa chọn thư mục Git qua môi trường tiến trình, cwd mới chưa bảo đảm Git dùng repository mới. Hoặc nếu lựa chọn executable/helper hay cấu hình include gián tiếp còn đến từ caller, allowlist tên `https` chưa chứng minh transport thật. Các lời gọi Git hợp lệ liên quan là `git init` và `git ls-remote --symref <endpoint> HEAD 'refs/heads/*'`. Một discovery vẫn rc=0 chỉ chứng minh chương trình được chọn đã trả output; kỳ vọng adapter là đọc đúng nguồn đã ghim, hoặc rc=12 khi không chứng minh được profile. Không cung cấp assignment, helper, config hoặc payload cho các hướng đó.

**Control đã chạy:** K dùng API nội bộ nhận bare đúng nguồn, adapter ở Git directory riêng, default/master và advertisement khớp map; rc=0, một discovery. Sổ feature không trở thành sổ canonical. Control không chứng nhận TLS/proxy production.

**Sửa:** xác định runner/process tin cậy; executable/transport, môi trường con allowlist và profile được dựng tường minh; không hợp ambient caller vào profile và không có indirection quay lại config ứng viên. Profile và consumer phải có provenance từ deployment, không từ receipt tự khai của process ứng viên. Thêm control dương cùng phép âm do điều phối dựng. R1 giữ P1; câu bất biến hiện tại chưa được các bước cụ thể bảo đảm.

### S2 — raw-object-read-does-not-verify-content-identity · P1

**Vị trí:** SPEC:180–187 (Q4.5–7), M1/M4, A6. Đây là vector khác replacement/graft của R2.

Advertisement SHA đúng và tắt replacement vẫn chưa kiểm bytes trong object cache băm về SHA ấy. R4 dùng cache của kho đang đọc nhưng chưa nói cache được bảo vệ khỏi ghi, hay xác minh identity bytes trước parser. Với cache local không tin cậy như biên config/ref đang xét, không cần collision SHA hoặc quyền thay nguồn canonical để có bytes khác nằm ở vị trí cache mà reader tra bằng OID.

**MÔ TẢ BẰNG LỜI, không tạo/chạy lại ở 4b:** giữ commit/tree canonical đúng; nội dung cache của blob được tree tham chiếu không còn khớp OID. Lệnh đọc hợp lệ `git --no-replace-objects cat-file -p <blob-OID>` có thể trả rc=0 và bytes có schema hợp lệ; parser chưa băm lại có thể dùng đích cấp lại khác. Kỳ vọng reader phải rc=12 trước quyết định, không phải coi rc=0 hoặc không có replacement là chứng minh integrity. Nếu chọn cache được bảo vệ như một trusted component thay việc băm, spec phải định nghĩa và kiểm được biên ấy; r4 chưa làm vậy.

**Bằng chứng kế thừa, không nhận là phép chạy4b:** `scratch/object-integrity-r4.json`, mục `blob_identity`: expected `8a8331e1372c3a03a6f420641db9e9de42237934`, bytes đọc băm thành `22c866a0db358378027433551a2b100dc50fdfc4`, `read_rc=0`, `tree_unchanged=true`; model eligibility Y đổi8→0, reader có kiểm hash→12. Không tái dùng script dựng ca ấy. Mục commit khác của 4a có `ls_tree_rc=128` đã fail-close; **không tính mục đó thành bypass**.

**Control4b:** K đọc commit/tree/blob sạch, băm lại cả ba khớp, raw tree không đổi, ancestry 0, `fsck --strict`0. Control không tái hiện ca âm.

**Sửa:** xác minh type/length/hash của các object thực sự dùng trong đường commit→tree→blob và ancestry, bắt đầu từ OID đã được adapter/event ghim; parse trên chính bytes đã xác minh, không mở lại cache mutable sau kiểm. Lệch/thiếu⇒12. Cộng chi phí vào A6; không yêu cầu quét mọi object không liên quan để kết luận một snapshot.

### S3 — a6-single-mutant-is-shielded-by-cli-flag · P1

**Vị trí:** SPEC:180–181 so với303 (Q4.5/A6).

Q4.5 yêu cầu đồng thời `GIT_NO_REPLACE_OBJECTS=1` **và** `--no-replace-objects`. A6 lại hứa bỏ riêng biến môi trường sẽ đọc cây/bản ghi thay thế và làm ca đỏ. Khi cờ CLI vẫn còn, bảo vệ vẫn hoạt động; ca hành vi ấy không phân biệt bản đúng với mutant đơn. Đây là cùng lỗi chọn đột biến mà r4 vừa sửa đúng cho A8/R9.

**Bằng chứng:** đối chiếu hai câu quy phạm; control raw K đúng cây. Hướng replacement và mutant chỉ **MÔ TẢ BẰNG LỜI**, không dựng hay chạy ở 4b. Không khai giết mutant qua một chốt chưa tới được. Nếu tác giả định “bỏ biến” thực ra là bỏ cả wrapper cấp hai cơ chế thì phải nêu chính xác mutant đó, không gọi là đột biến đơn.

**Sửa:** ghi single mutant sống khi lớp độc lập còn che; định nghĩa mutant kết hợp bằng đầy đủ protection set bị bỏ, có output/verdict phân biệt thật. Sau thêm S2, lớp kiểm bytes cũng có thể che ca replacement: không tiếp tục hứa combined hai cờ chắc chắn lọt khi vẫn còn integrity check. Catalog phải ghi sống/chết theo đo, giữ control sạch xanh. P1 theo rubric tiêu chí không thể đỏ với mutant được viện ra, không phải khẳng định replacement vẫn lọt r4.

### S4 — q13-selected-mode-conflicts-with-a5-and-ready-fields · P1

**Vị trí:** SPEC:140–146,299–301,364–370 (Q3/A5/Q12/Q13); bảng ngoài phạm vi:246.

Q13 đã chọn ngoại lệ khi policy chưa có; Q3 nêu có neo thì tính closure khai báo+symlink. A5 vẫn đòi “policy vắng ⇒12 (kích hoạt)” và ca companion⇒11 không ghi prerequisite policy. Cùng đầu vào hợp lệ theo Q13 không thể đồng thời đạt cả hai acceptance. Đây không phải yêu cầu bỏ quyết định Q13 hoặc buộc #473 land trước.

**P đã chạy, model closure bắc cầu và so tập:**

| Fixture nguồn closure | Kết quả theo Q3/Q13 | A5 cần quy định |
|---|---:|---|
| Policy hợp lệ có SKILL→GOTCHAS; hai raw set tách nhau nhưng closure giao |11|11, ghi rõ policy fixture |
| Policy vắng, Q13 có neo; cùng hai raw set, không có symlink giao |0|Control 0 của ngoại lệ; không đòi11 |
| Policy vắng, Q13 có neo; hai lease cùng raw `docs/a.md` |11|11, ngoại lệ không bỏ kiểm độc quyền |
| Policy vắng, không neo hợp lệ, active |12|12 |
| Policy/ngoại lệ hợp lệ; Y hoặc W khai effective rỗng trái closure |8|8 ở cả hai phía |

Q12 còn đòi policy SHA trước ready của mọi slice nhưng policy vắng và Q13 chỉ nêu neo trong A1; chưa có biểu diễn nguồn ngoại lệ để dispatcher đóng băng. Không được giả một SHA của policy chưa tồn tại, bỏ trường phái sinh, hoặc tự mở rộng ngoại lệ A1 thành quyền ready mọi packet. Chỗ này là phần thiếu hợp đồng trước ready; P1 chính ở acceptance mâu thuẫn đã tái hiện.

**Sửa:** tách ba nhánh policy/ngoại lệ có neo/không neo trong A5, giữ forecast tách verdict A0. Chốt descriptor nguồn closure trong spec_hash, kiểu biểu diễn policy vắng và phạm vi từng slice; slice không có authority hợp lệ vẫn proposed. Bảng ngoài phạm vi phải hiểu dependency là **policy hoặc ngoại lệ Q13**, không đòi cả #473 lẫn lối đã chọn.

### S5 — m9-check-publisher-consumer-is-unspecified · P2

**Vị trí:** SPEC:264–280,317–320,356–360 (M9/A11/Q10); protocol§8:581–588.

R4 đã đóng đúng exact S/H/T và strict merge predicate của R5. Phần còn thiếu là **object nào phát vàobject nào tiêu** required check có provenance đó. M9 chỉ liệt kê contents/read, pull-requests/read, issues/write để chiếu comment; chưa chọn check/run/status object, publisher/App, API/quyền và consumer được bảo vệ đọc lại liên kết với H. Một receipt viết H trong thân không tự biến object check gắn S thành object của H. Workflow-target/dispatch chạy đúng mã S cũng chưa là bằng chứng association check với H.

Không nâng thành P1 “mọi M9 không thể xanh”: Q10 đã yêu cầu facts trước activation, nên thiếu interface giữ inactive. Nhưng executor đang phải tự thiết kế thêm phần thẩm quyền/capability ngoài nội dung và quyền được giao. Đây là P2 đúng rubric, không khai đã quan sát check object GitHub trong lượt offline.

**Sửa:** chốt publisher/consumer interface trước ready A0, object ID/run/attempt, repository/PR/S/H/T/checker/workflow OID, conclusion, publisher identity và cách readback object thật trên H. Phân biệt comment projection. Nếu cần App/quyền ngoài M9 thì chốt dependency/authority, không tự nâng permissions. Ca âm: đúng receipt nhưng check thuộc S, sai publisher, sai checker, stale H đều không pass; ca dương exact H phải có Actions receipt thật. Audit bootstrap theo §8 được neo bền trong Packet Issue/journal, gồm khoảng giữ đóng và readback run đầu; không chỉ có prose “đã cấu hình”.

### S6 — q13-exception-scope-and-retirement-are-not-bound · P2

**Vị trí:** SPEC:140–146,364–370; protocol§3.2/§5, ADR-0025.

Đáp án chủ kho đã có: dùng lối (ii), tới khi policy canonical xuất hiện, neo Issue/spec_hash A1. **Không coi việc thiếu ngày UTC hoặc mô hình “năm2036 policy vẫn vắng” là phản chứng**: nếu sự kiện chưa xảy ra, chưa chứng minh ngoại lệ đã hết hiệu lực. Không tự đặt hạn mới thay authority đã chốt.

Phần chưa đóng là descriptor/phép kiểm “có neo”: source object/body hash nào, phạm vi tính holder toàn kho khác gì quyền ready packet khác, so với Packet/revision/spec_hash nào và ghi trạng thái retired ở đâu. Hết hiệu lực theo sự kiện cần dùng canonical snapshot hiện tại, xử policy có mặt nhưng hỏng/mismatch pin, và không tự trở lại exemption cũ sau khi sự kiện kết thúc đã xảy ra. R4 chưa nói gì đủ để executor phân biệt “A1 đã từng được miễn” với “lần đọc hiện tại còn được miễn”. §5/ADR-0025 đã buộc pause/re-evaluate và revision/generation khi closure/check/hash đổi; không được grandfather các lease đang chạy.

**Sửa:** descriptor owner/reason/object ID/hash/phạm vi/điều kiện hết hiệu lực được đóng băng; mismatch⇒12. Hết theo **lần đầu** policy xuất hiện, ghi retired bền, policy hỏng⇒12; không dùng cờ cached từ A1. Chỉ ngoại lệ phép tính va chạm của packet này, không miễn phái sinh/authority của packet khác. Nêu rõ hoạt động pause/re-evaluate và cấp generation theo luật, không ngầm sửa/gia hạn ID cũ. P2 vì thiếu binding/lifecycle cụ thể; không thêm một P1 giả vì lựa chọn deadline đã được chủ kho chốt.

## Phản chứng đã chạy lại + mới

Chỉ các script sau được chạy mới, với task-data trong cwd; script cũ bị cấm không được gọi nguyên file:

```text
PYTHONDONTWRITEBYTECODE=1 python3 scratch/r4b/measure_r4.py
PYTHONDONTWRITEBYTECODE=1 python3 scratch/r4b/allowed_probes.py
PYTHONDONTWRITEBYTECODE=1 python3 scratch/r4b/allowed_coverage.py
PYTHONDONTWRITEBYTECODE=1 python3 scratch/r4b/extra_r4.py
PYTHONDONTWRITEBYTECODE=1 python3 scratch/r4b/loop_r4.py
PYTHONDONTWRITEBYTECODE=1 python3 scratch/r4b/controls.py
PYTHONDONTWRITEBYTECODE=1 python3 scratch/r4b/default_control.py
PYTHONDONTWRITEBYTECODE=1 python3 scratch/r4b/baseline_r4.py lease
PYTHONDONTWRITEBYTECODE=1 python3 scratch/r4b/baseline_r4.py loop
PYTHONDONTWRITEBYTECODE=1 python3 scratch/r4b/baseline_r4.py docs
PYTHONDONTWRITEBYTECODE=1 python3 scratch/r4b/baseline_r4.py doctrine
```

Bảy harness đầu rc=0. P có 26 mục, E11, G4; đây là số mục JSON, **không** số acceptance A1–A12 pass. L35 tổ hợp/40 guard calls; K control Git/adapter. Wrapper đo baseline trả0 để lưu report kể cả lệnh con đỏ; mã thật của suite lease là1, được giữ ở report. Không nhầm wrapper rc với gate rc.

`allowed_probes.py` tái dùng phần hợp lệ từ dòng170 trở đi của script 4a với prelude Git thông thường mới. `allowed_coverage.py` chỉ tái dùng phần từ dòng28 (cardinality/history/API model). Không chạy `scratch/probes_r4.py`, `coverage_r4.py`, `followup_r4.py`, `object_integrity_r4.py` nguyên bản. Các control K được soạn mới chỉ đọc đúng nguồn/đúng cây. Không dựng helper/config đổi nguồn, replacement/graft, đường thoát, đồng tự hoặc chuỗi thoát tấn công.

| Ca | Kết quả chạy mới | Đã đo gì / chưa đo gì |
|---|---|---|
| A0 workflow ở canonical fixture, inactive | S/T rỗng 0; T có sổ 12; sổ+PR bỏ test/wrapper/workflow12; S có sổ 12 | Git trees + M4 model; không phải Actions |
| A0 forecast | product check0/dự báo 8; product holder11/dự báo 0; mutant gắn luật mới vào product8 | Hàm model cho contract; không phải wiring code A0 chưa viết |
| Nơi dùng forecast | Q3 “luật mới chỉ” + Q4.6 sharedstate + Q5 guard cùng cờ | Không tìm thấy chỗ nào trong spec cho DU_BAO làm grant/activation decision; Q6 dùng dự báo để audit delta, quyết định vẫn quaQ10 |
| Bootstrap lần land A0 | Empty-only rig có thể 0 với checker sai; **không** là counterexample đầy đủ r4 | §8 review semantics, independent catalog A12, audit exacttree và freeze/readback đều vẫn bắt buộc. Đọc together không còn R3 |
| M9 exact candidate | OldS0/H receipt0; currentB/M append8; strict control 0; base/fetch/tree/checker lệch12 | Git merge parents/tree thật; check publisher association ngoài kho not_run |
| Effective tự khai | overlap11; Y[]8; W[]8; claim bằng closure11 | R6 đóng; parser nền checkg2 vẫn0 với[] không phải parser r4 |
| Symlink hai cây | Cùng blob/path lease; đíchother/a.md và docs/a.md; hợp conservatively va chạm11 | Source occurrences được giữ, mutant canonical-only0 |
| Symlink nội bộ vòng / parent mới | Vòng12 hữu hạn; nested/link/new.md→nested/dest/new.md | Không dùng host filesystem resolve cây khác; ca ngoài cây not_run |
| Cutover | Tại14:33:15 và 21:05Z: gateold1/new4; wp461 trước C={r2, g2}, sau C={g2} | Clock cố định trên frozen Git; không giả quan sát production vào giờ ấy |
| C không đích + g2 hết hạn | 09:52:00Z và 10:17:12Z: wp461 sau C=∅ | C vẫn event thu hồi; không tự sinh holder g3, không tái dùng/gia hạn g2 |
| g3 trước C | Pure check có thể 0 sau expiry; Q11 vẫn **không cho cấp/bắt đầu** trước C+dừng worker | G3 là ops PR riêng sau activation **và theo thứ tự Q11**; cụm “sau kích hoạt” ở Q6 không miễn Q11. Không có finding mới chỉ vì pure check 0 |
| History đóng hai cây | Cutoff X→Y; cây sau thêm Z→W; fixed check W 8, mutant đọc cây sau 0 | G có Git OID và 4 tuple thực, canonical 7 cặp hợp lệ |
| A8 mode | Full 8, single only-new 8 sống, combined 0 bị ca giết; full T unit 12 | Git mode fixture không materialize symlink YAML |
| A8 merge parent2 | Giữ entry 0, bỏ 8 | Phép ancestry parent2 tự nó hợp lệ |
| CLI exact pair | Ordinary/ops/default có pair 0; wrong blob/path/local/tag/pull 12 | Model publication; không mô phỏng lock acquire |
| Q2 JSON/API lifecycle | Control 0; float/duplicate/prose/broken command 8; bad account 4; envelope/HTTP failure 12; sau canonical thêm 0 calls | Không có HTTP request; representative API model |
| A10 record-lease | Candidate ID x; live 0/leased; revoked 8/stale/event x1/no record_lease; unknown 8/byte-match | Parser/entrypoint/state thật; doctor precondition và guard snapshot được tiêm trong bộ nhớ |
| A10 5 cửa và inactive | 5×4 active; 2 old-ID mutants; 3 helper-only; 5 inactive preview; 5 inactive nonempty =35 | Revoked lặp không đổi state/event; ba route helper-only vẫn qua nên ca phân biệt được |
| A12 catalog | Control đủ true; bỏ invocation false; bỏ cả registration+invocation false | Expected catalog ngoài candidate model; không chứng nhận catalog production |
| Q4 control nguồn/thô | Discovery rc=0,1 call; default OID khớp; feature không canonical;3 hash object đúng; ancestry/fsck 0 | Không chạy ca âm đổi nguồn/đổi cây |
| Default main hợp lệ, master vẫn tồn tại | K2 discovery0; main không sổ, master có sổ; map hiện tại0, map cũ cùng tên/SHA lệch12 | Một bare nguồn bình thường, không config giả hoặc đổi nguồn; adapter phải chọn server main. |

**Các hướng chỉ MÔ TẢ BẰNG LỜI:** (1) remote helper/config/rewrite và thay môi trường chọn nguồn: S1; (2) replacement/graft và shielding A6: R2/S3; (3) bytes cache không khớp OID: S2, chỉ kế thừa JSON 4a; (4) absolute/outside-tree/Unicode đồng tự/chuỗi thoát. Điều phối dựng các ca này, gọi reader bằng `ls-remote`, `ls-tree`, `cat-file`, ancestry/diff hợp lệ, kỳ vọng nguồn/cây canonical không đổi hoặc 12; path/input không hợp lệ phải 12 trước truy cập, không được biến thành vắng dữ liệu. Riêng status gate có thể native Git 0 nhưng reader 12: phải giữ cả hai rc, không nhận native 0 là pass authority.

## Tiêu chí A1–A12

Audit khả năng đo và giết mutant, không phải biên nhận nghiệm thu implementation chưa tồn tại. Các mục “như r3” được đọc cùng SPEC.r3.md đã ghim hash; không coi việc r4 rút gọn schema là tự xoá hợp đồng kế thừa.

| Tiêu chí | Đơn vị / phép đỏ thật | Đột biến, ca không thể đỏ hoặc không thể xanh |
|---|---|---|
| A1 | Holder là tập ID; chẩn đoán theo cặp (blob, path); MAP_REF giữ occurrence. | G có 3 blob/4 ref và 1 blob ngoài known-list; mutant known-only để X sống, nên có phép đỏ. Smoke ∅/{g2} theo clock đã sửa R8. Output CLI mới chưa chạy. |
| A2 | 1 cặp/3 ref; danh tính nguồn, default, map OID, rc=12. | Các chốt any-ref/local-symref/fallback có ca phân biệt trong hợp đồng. K/K2 control đúng nguồn xanh. Config/helper/nguồn lạ chỉ mô tả; S1 còn thiếu biên môi trường. Bare fixture không chứng nhận TLS production. |
| A3 | Rc của 5 nhánh; history tại hai OID; verdict sản phẩm và DU_BAO riêng. | P: 8/0/8/0/8; G fixed W=8, mutant=0. A0 product=0/forecast=8 phân biệt bật sớm. Q3 “chỉ dự báo” + Q4.6 buộc body/kiem-github/guard dùng cùng chế độ. |
| A4 | Y chết từ sổ/history; có hoặc không thay thế; control sống=0. | Hợp đồng có 2 nguồn × 2 dạng lease. P đo historical reverse=8 và ledger=8 qua state predicate; ma trận/output đầy đủ của implementation chưa chạy. |
| A5 | Closure, path, OID và rc=11; claim sai=8; CLI chưa có exact pair=12. | Symlink/claims/normalization hợp lệ có phép đỏ. S4: đòi active=12 chỉ vì policy vắng không thể xanh dưới Q13 có neo; companion=11 phải có policy fixture. Pure 0/0 không phải cấp lease an toàn trước race. |
| A6 | Map/OID/clock được ghim; identity bytes; ba cặp chạy xen kẽ, median ratio ≤2. | K/K2 pinning/default/map controls đúng. S3: bỏ riêng biến bị CLI flag che. S2 cần kiểm bytes; mutant kết hợp phải nêu mọi lớp bị bỏ. Chưa có tử số r4 nên ratio not_run. |
| A7 | Mỗi ràng buộc schema/mode/clock/authority có control; rc=4/8/12 theo thứ tự lỗi. | Entry mới mode120000→12 qua validator; entry cũ đổi mode→8 qua append-map là nhất quán. Inactive/nonempty→12; command JSON8/envelope12. raise→continue phải so verdict thật, có thể0 hoặc11. Full parser × consumer r4 chưa chạy. |
| A8 | Map path→(mode,type,blob); cây/cha; S/H/T/checker OID. | Git sửa entry8, parent2 giữ0/mất8. R9 đã sửa: single8 sống, combined0, full-T unit12. M9 model âm12/control0; association của check thật còn S5. |
| A9 | Object ID/repo/Issue/login/body hash/types/API call count. | P/G control và âm8/4/12 phân biệt đúng; sau canonical thêm0 call lịch sử. Cần actual API receipt lúc A1/C. Băm UTF-8 bytes đã đến, không dựng lại JSON rồi băm. |
| A10 | 5 cửa ×4 trạng thái; target ID; rc/state bytes/event/attempt/idempotence. | L có35 tổ hợp, đặc biệt record-lease đúng candidate ID. Snapshot guard được tiêm, REST calls=0. Chưa đo profile thật, disk failure hay cancellation/fencing. Không khai đã gọi HTTP403. |
| A11 | Base/candidate cùng môi trường; delta theo tên; check object/provenance; rc và bằng chứng dương. | Nền lease120/121(rc1, thiếu actionlint), loop278/278+81(rc0), docs/doctrine0. Chưa có candidate nên chưa đo delta. A0 canonical model chặn PR bỏ test; A1 cần Actions receipt thật. Lint/thân bước không thay publisher binding S5. |
| A12 | Catalog độc lập; executed/failed/skipped/not_run; mutant sống/chết. | P bỏ cả registration và lời gọi vẫn thiếu catalog, có thể đỏ. Catalog phải neo trong ready Spec/audit A0 rồi canonical. A6 single phải ghi sống; A8 single r4 đã ghi đúng. |

## Nhất quán luật, bootstrap và kích thước slice

| Nguồn luật | Kết luận r4 |
|---|---|
| §3.2 + ADR-0025 | Ready đòi Issue/revision/spec_hash/phái sinh do dispatcher; Q13 không làm mọi lease có policy SHA thật khi policy vắng. S4/S6 cần tagged source có authority, scope và re-evaluation. Policy đổi làm closure/check/hash đổi ⇒ revision/generation trước chạy tiếp. |
| §4 + ADR-0028 | Q5/Q11 đúng stale/generation/dừng worker/last SHA/state; C không làm g2 sống lại. Retention branch tới mission land/hủy+30 ngày và cleanup sau process dừng vẫn kế thừa, không nằm trong quyền xoá của packet này. B chưa triển khai không được khai đã chặn heartbeat/push/land thật. |
| §5 | Exclusion toàn repo theo closure, symlink và parent; Q13 là ngoại lệ đã chốt của phép tính. Không đặt lại câu hỏi chọn lối (i)/(ii). Scope/retirement còn S6; malformed policy không được fallback. M9 chủ động không dùng master drift§5.1 là quy tắc chặt hơn đã nêu, không mâu thuẫn. |
| §8 + AGENTS | Review read-only, exact hash/base/tree, khai identity thật; hint là chữ SPEC, không code authority. Audit A0 không chỉ kiểm sổ rỗng: phải đọc semantics/diff, gates, expected catalog độc lập; evidence/verdict bền neo exact SHA theo §8. S5 cần gắn chuỗi audit/run/readback vào object thật. |
| §12 | Trần 6 đã có authority. 4a sinh output dù chết vẫn tiêu 1 call;4b là 5/6. Không đồng nhất codex_review_calls_used với review_rounds_used. Source pattern tái hiện dạng S1/S2 kích hoạt stop riêng của chính r4: dừng packet/ADR nguồn tin cậy trước tiếp tục, không tự tiêu lượt 6 vì còn quota. |
| CLAUDE.md | “Có mặt” không bằng “có đo”: A6 mutant bị che, S5 chưa actual receipt. Đo cổng nền theo delta, không đổi lease 120/121 thành 121/121. Đo bytes nhận trước suy authority; tắt replacement không chứng minh object hash S2. Không chạy gate cần mạng bằng stub để nhận pass. |

**Bootstrap A0 (câu 2c):** Điều kiện đủ về contract là cùng lúc có review/gate hiện hữu theo §8, audit exact S/H/cây sẽ nhận và sổ rỗng, catalog độc lập A12, biện pháp giữ đóng cập nhật từ land A0 qua cấu hình/check readback, rồi run đầu từ chính A0 được consumer xác minh. Nếu chỉ lấy predicate “empty” thì rig bad checker 0 không đủ; nhưng bỏ các điều kiện còn lại sẽ không còn là A0 đúng r4. Vì vậy không giữ R3 dưới tên mới. Nơi ghi phải là audit/verdict bền trong Packet Issue/journal theo §8/ADR-0025, có object ID/hash và OID A0 sau land; r4 chưa có receipt thật. Hint làm rõ các trường/bootstrap chain dưới S5, không cấp quyền bootstrap bằng một comment tự chiếu.

**Slice:** A0=3 tệp,560–780 dòng; A1=3 tệp,90–160; B=2 tệp,160–240; C=1 tệp, ~15. Cộng **825–1195**, **6 path duy nhất** (A0/A1 chung 3 path). ADR-0044 sensitive≤3 tệp/≤300 dòng thêm: chỉ A0 vượt dòng theo ước. R4 đã khai lý do có phạm vi (adapter+validator+workflow+fail-close/mutant), phù hợp lựa chọn “revision thiết kế hoặc khai lý do”; không tự áp trần 300 lên tổng bốn slice. A1/B/C không vượt **theo ước**, chưa có diff. S1/S2 có thể tăng chi phí/dòng; phải đo lại numstat, không bịa ước mới là số đo. #250 +409 là SPEC, #275 +368 và #248 +328 là code; không dùng các mốc ấy làm bằng chứng đủ cho ước A0. Mỗi slice có scope/acceptance/Issue/lease riêng và base đã nhận slice trước; tách slice không reset counter.

## Q7–Q14: câu thiếu và đáp án bắt buộc

| Câu | Còn phải chốt/đo | Đáp án đã bắt buộc hoặc đã được chủ kho chốt |
|---|---|---|
| Q7 | Packaging/spec/Issue/lease từng slice; ngoại lệ dòng A0 và audit bootstrap được neo | Chuỗi A0→A1→B→C, A0 phải có workflow inactive; scope/acceptance tự đủ, base đã nhận; ADR-0044 không cho PR chồng lấn hay cắt test để né trần. |
| Q8 | Object lệnh thật trên #461, readback 6 field/account/URL; chưa tồn tại trong bundle | R4 mục tiêu C=null; không còn chọn g2 làm đích. Comment Q13/Q14 trên PR #475 không phải lệnh thu hồi này; không chiếu bot comment thành authority. |
| Q9 | Chủ kho còn cần chốt lựa chọn sản phẩm nhận event cho lease hết hạn | Khuyến nghị nhận được giữ; event không gia hạn/tái dùng ID, không tạo holder còn hạn. Không có luật bắt từ chối event chỉ vì lease hết hạn. |
| Q10 | Workflow/checker A0/run thật, profile transport, publisher consumer S5, ruleset/direct push/bypass/strict/tree/queue, plan delta owner và sổ rỗng | Thiếu facts⇒False; không đủ chỉ đặt tên required check. S/H/T/checker/provenance đều đúng trước activation. Q13 là lối (ii) được chọn, không bắt #473 land trước. |
| Q11 | Ai tuần tự hoá; facts C land, worker đã dừng, last SHA/state, journal, g3 new check/land/readback | C→dừng worker→cấp g3 mới→readback NGƯỜI_GIỮ 1→mới bắt đầu. G3 chỉ “sau kích hoạt” chưa đủ bỏ qua C. Check 0 không là lease/fencing; generation cũ không hồi sinh. |
| Q12 | Typed source closure/descriptor/hợp đồng S1/S2/S5/S6 trước ready; authority scope mỗi slice | Không kế thừa miễn phái sinh từ b416830. Không cần code A0 chưa viết đã chạy trước lease A0, nhưng contract phải đóng; runtime facts phải có trước dùng quyền tương ứng. |
| Q13 | **Không thiếu lựa chọn (i)/(ii)**; thiếu binding/phạm vi/retirement/schema mô tả trong S4/S6 | Đã chốt (ii), raw+symlink đến sự kiện policy canonical xuất hiện, neo Issue/spec_hash A1. Không nhận EWS tự khai làm nguồn. Không tự thêm deadline UTC; không grandfather sau sự kiện kết thúc. |
| Q14 | Cập nhật durable counter 5/6 và checkpoint nguồn; tổng mission budget khác không có receipt để đo | Đã chốt trần 6, giữ counts/IDs. 4a tính call 4 dù không verdict;4b là call 5. Lượt 4b chỉ thành review round hợp lệ sau schema/exact SHA/receipt validation; không tự đếm như một round đã được GitHub công nhận. |

Không cần xin lại Q13/Q14 để hoàn tất review này. Các quyết định/facts còn thiếu thuộc readiness/activation tương lai; không thực hiện thay chủ kho trong lượt read-only.

## Bảng đo lại

D đo lại từ `cay-kho/` theo ref/OID, không sửa kho. Native CLI/suites chạy trên bản sao mới `scratch/r4b/base/`, origin là bare mới trong `scratch/r4b/`. Dữ liệu clock lịch sử là phân loại frozen Git tại timestamp được chỉ định; không phải quan sát live production lúc đó. Thời gian dưới đây là một lượt đo mỗi lệnh, có suite chạy đồng thời; không dùng làm benchmark A6.

| Lời khai / đơn vị | Kết quả offline lượt 4b | Bằng chứng / giới hạn |
|---|---|---|
| SPEC.md và bản untracked trong cay-kho | Cùng `415ce35db32aa370ce43315c1ff6d4db7b59005e6288538e72705ce4caed4d0e` | Hash trước và sau; review đúng r4 |
| SPEC.r3.md / VERDICT.luot3.md / HINT.luot3.patch | `ef9b3700…` / `6b8dde21…` / `0a81bd8b…` khớp full hash được giao | Không phải chứng thực model/runtime metadata lịch sử |
| HEAD/tree/core.abbrev | `b416830ef2a509d60203d55552ce17950afcf67c` / `266a2aba97d925dac3ab7473dda55adb0fe23b8e` /7 | Detached; status ban đầu chỉ spec untracked |
| Ref theo đơn vị SPEC | **303 =302 remote +1 local master**, trừ HEAD alias | User mô tả mirror302 là số remote; tổng thực tế theo công thức SPEC là303 |
| Cặp(blob, path) / path / lease_id | **288 /273 /273** | Không lấy số ref làm số cặp |
| ID có nhiều blob | **7**, số blob2/2/4/4/5/3/2 | D.multiblob có full ID/OID |
| CÒN_HẠN / còn bản chưa bia mộ | **8/4 tại 13:41:00Z**, **7/3 tại 14:33:15Z và 21:35:00Z**, **1/1 tại 09:52:00Z08-09**, **0/0 tại 10:17:12Z08-09** | Các timestamp là clock fixture, không so “7” qua hai ngày mà không ghi giờ |
| #456 expiry | **2026-09-07T14:30:07Z** | Sau hạn không còn trong 7 ID live |
| Gate r1/r2/r3/r4 expiry, ngày 08-09 | **03:37:33 /07:50:35 /09:44:51 /10:17:12Z** | Cả4 còn hạn tại 14:33 và 21:05Z ngày 07 |
| Wp461 r1/r2/g2 expiry, ngày 08-09 | **03:05:00 /05:27:42 /09:52:00Z** | G2 hết trước gate cuối25 phút 12 giây |
| Bia mộ canonical / feature#468 | **7 /11**; cả 7canonical hai chiều hợp lệ | G có tuple(old, new, oldblob, newblob) và hash biểu diễn sorted |
| Commit riêng nhánh có #468 | **0 /31** so master | D.divergence; không 28 |
| R2 blob chưa tomb `26f07b4fe49964034c710864f350402fe5bf55c3` | **4 ref** | heads/master, origin/master, origin/ops/cap-lease-461, origin/claude/soan-spec-3-viec-treo-20260906 |
| R2 blob tomb `fdfde3a57ab9fd2c83454e9b9b2eff96f77ef229` | **1 ref** | origin/ops/lease-wp461-g2 |
| R2 “ref thứ 5 ởPR475” | **Chưa đo** | [API] theo SPEC; mirror không chứng minh thêmref ấy |
| #456 blob chưa/có tomb | `8b2103c06687546379a17f6deafc97f1fe0173fd`: **11 ref**; `1f9504281c3415f7194e124eb7b2702c34c8efd1`: **1 ref** | Expiry không làm ref tự biến mất |
| Policy và schema canonical đúng vị trí§5 | **Đều vắng** | `.github/coordination/change-impact.v1.json` và `.github/coordination/schemas/change-impact.v1.schema.json`; root schemas path cũng vắng |
| Lease planned | **3 ID**, đều hết hạn tháng 08 | Plat-x4-exec1, plat-x5-exec1/r2; dedupID, không đếm blob/ref |
| Canonical sổ / workflow M9 | **0 entry / chưa có workflow** | M1–M9 là code tương lai; A0 chưa land |
| M4 native command | **rc=2 invalid choice** | Nền chưa có `kiem-thu-hoi-github`; không gán lỗi này cho executor chưa bắt đầu |
| `kiem()` gọi `_lease_cham_duong` | **0** | AST của code nền |
| 5 cửa packet_loop gọi schema helper | **1/1/0/0/0** | record-lease/begin-attempt/record-post/transition/record-review; code nền, không M7 mới |
| B416830 raw chữ ký | **1 gpgsig PGP**; author ducthangho, committer GitHub | Không xác minh keyring/signer; không dùng `%G?` làm bằng chứng human |
| 6635379 raw chữ ký | **1 gpgsig SSH**,2 marker; author/committer Claude | Không phải2 chữ ký; API author.login khác raw header |
| 5 workflow actor / author.login / GitHub mapping | **Chưa đo** | Giữ [API]; không biến lời khai actor thành phân biệt chủ kho với agent cầm PAT |
| `ai-dang-giu` launcher.py | **NGƯỜI_GIỮ 2, rc=11;3,492s;2217 B stdout** | Native baseline trên copy |
| `ai-dang-giu` CHANGELOG.md | **NGƯỜI_GIỮ 2, rc=11;3,367s;941B** | Native baseline |
| `ai-dang-giu` provider plan | **NGƯỜI_GIỮ 2, rc=11;3,451s;941B** | Native baseline |
| `ai-dang-giu` bien_nhan_v2_test.py | **NGƯỜI_GIỮ 2, rc=11;3,415s;941B** | Native baseline |
| `check` g2 gốc / thêm effective [] | **0 /0** | Baseline parser; model r4 với claim sai là 8, không nhận baseline 0 làm pass r4 |
| Cutover gate old/new tại 14:33Z | **{r4} /{r1, r2, r3, r4}** | E; delta bảo thủ phải có dừng lane và expiry/xử lý, không tự bật khi chưa facts Q10 |
| Sau C wp461 tại 09:52 và 10:17:12Z08-09 | **∅** | C không tự cấp g3; đã sửa smoke r3 |
| Numstat mốc #250/#275/#248 | **+409/−0 /+368/−0 /+328/−1**, mỗi 2 tệp | Diff first parent của2854380/7883aad/647cfea; #250 là2 SPEC |
| Ước r4 | **825–1195**,6 path duy nhất; chỉ A0 vượt300 dòng | Đúng phép cộng; chưa có implementation numstat |
| Lease suite nền | **120/121 đạt,121 executed,0 skipped, rc=1;65,225s;8971 B stdout+56 B stderr** | Chỉt33 thiếu actionlint; không cài mạng hay stub công cụ |
| Wrapper121/121 / actionlint / shellcheck r4 | **Chưa đo** | Wrapper có bước lấy tool qua mạng nên không chạy; không gọi parser YAML thay actionlint |
| Packet-loop suite nền | **278/278,81 mutant,78 lớp,35 ca bắt oan,0 ngoại lệAC 18; rc=0;217,695s;8752B** | Raw log `loop-baseline.log` có TỔNG: ĐẠT |
| Doc-claims strict | **rc=0, ok:true,106 tệp,0 flags,367 advisories;3,117s;70861B** | Không chứng nhận semantic SPEC |
| Doctrine-scan kèm spec | **8 tệp,0 chỗ chép, rc=0;0,195s;69B** | Không suy không mâu thuẫn§12 chỉ vì scan 0 |
| Adapter fixture hợp lệ | **1 discovery, rc=0;0,0067s;193B** | K; không mạng; không numerator/ratio A6 production |
| Raw object controls | **3/3 hash đúng, raw tree bằng nhau, ancestry 0, fsck 0** | K; không chạy ca âm bị cấm |
| Q13/Q14 comment | **Chấp nhận lời khai user/điều phối đã readback** | ID5575587924; OWNER ducthangho theo EVIDENCE; không tựreadback mạng |
| 4a runtime/4b accounting | **4a tính call 4;4b tính call 5/6** | 4a error content filter, stdout 0 không là preflight fail;183508 token/thời lượng 1601,457s chỉ lời khai EVIDENCE |

## chua_do_duoc

1. **Nguồn production:** không GitHub network/default/freshness/PRhead thực, TLS/CA/proxy/credential profile, executable/helper provenance deployment. Bare fixture chỉ kiểm hợp đồng nội bộ. Các hướng đổi nguồn/đổi cây bị cấm ở 4b chỉ mô tả bằng lời; không coi không chạy là pass.
2. **Object integrity âm:** không chạy lại 4a hoặc tạo bytes cache sai. S2 dùng contract analysis, control sạch mới và JSON 4a kế thừa; ca commit 4a có ls-tree 128 không được nhận thành fail-open. Replacement/graft và hai mutant A6 chỉ mô tả.
3. **Authority:** Q8 chưa có object lệnh; chưa readback Actions/check publisher/consumer, ruleset/direct push/bypass, queue, strict tại merge, dispatch/retarget thật hoặc freeze/bootstrap audit. Q13/Q14 được user cho chấp nhận là readback, không phải reviewer tự đo từ API.
4. **Implementation r4:** M1–M9 chưa tồn tại trên base, không có A0/A1 landed OID, BIA_MO_LICH_SU sau A0, registry active, candidate test delta hoặc A1–A12 N/N. Models có predicate đơn giản hoá, ví dụ M4 fixture kiểm tuple/mode chứ không toàn parser M1. Không dùng model nhỏ chứng nhận parser/runtime đầy đủ.
5. **Forecast/wiring:** contract buộc mọi operational consumer cùng mode; chưa có code để đo `body`/`kiem-github`/M7 có thật sự tách DU_BAO khỏi exit/status hay không. A0 dùng projection delta cho audit Q6 không phải đường grant tự động. Phải nghiệm thu trên implementation.
6. **Symlink/paths:** đã chạy alias nội bộ, hai occurrence, vòng và parent tệp mới; chưa đo Windows filesystem, toàn bộ prefix descendants và mọi biên object thiếu. Không tự dựng absolute/outside/Unicode đồng tự/chuỗi thoát. Ca mode Git không checkout thành symlink có YAML.
7. **Guard/fencing:** L dùng parser/state thật với doctor precondition và snapshot guard tiêm trong bộ nhớ. Không đo disk failure, process kill, cancellation/heartbeat/push/handoff/land enforcement thật. REST calls 0 không phải đã gọi API 403. Không gộp M7 guard với nợ fencing ngoài write_set.
8. **Gate/timing/size:** suite lease còn thiếu actionlint nên 120/121, không được gọi wrapper 121/121. Chưa actionlint/shellcheck workflow r4, full selftest/release gate không chạy vì không có runtime diff. Ratio A6/numstat r4 chỉ có estimate, không có tử số/candidate; không dùng đo nền và các fixture nhỏ thay.
9. **Metadata/counters:** không raw run/backend attestation/working clock của 4a hoặc ba lượt cũ. EVIDENCE thời gian/token/error được ghi là lời khai. 4b được tính call 5 theo §12, còn review_rounds chỉ tăng sau validation của điều phối. Các trần mission/provider quota khác ngoài bundle không đo.
10. **Quyết định tiếp theo:** còn 4 P1 nên không approve. Không tự phóng lời gọi 6: theo chính r4, S1/S2 cùng hình dạng nguồn tin cậy buộc dừng packet/chốt ADR trước tiếp tục. Hoàn tất artifact read-only của lời gọi 5 vẫn nằm trong chỉ thị trực tiếp. Patch chỉ đề xuất chữ và prerequisites, không cấp lease/kích hoạt/authority.


## Kiểm tra artifact cuối

- `patch --dry-run -p0` và áp patch thật trong `scratch/r4b/patch-check/` đều rc=0; bản sau áp khớp từng byte với `scratch/r4b/SPEC.proposed.md`. Không áp patch vào SPEC gốc hoặc cay-kho.
- HINT sha256: `4a0321fd79f2ec0e1ea330dd7526e8aaf4cd7dbdb20c0be211a7d3e4a2751706`; SPEC đề xuất sau áp trên bản sao: `1cb274e1cad051a0bebfe23db4fd67124b72951a37d290edbe3933c2a8801528`.
- Validator xác nhận 35 hàng lịch sử (30 ĐÓNG, 5 ĐÓNG-MỘT-PHẦN), 6 finding S1–S6 đúng 4 P1/2 P2, 12 hàng acceptance, 8 hàng Q7–Q14; coverage hint đủ cả 6 finding.
- Hash SPEC gốc và bản trong cay-kho không đổi; tracked/cached diff đều rc=0; status vẫn chỉ `?? ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` như đầu lượt.
- Bằng chứng kế thừa S2 `scratch/object-integrity-r4.json` có sha256 `1aecf6f0342437d633e1e0c9ace042a28d3f942abfb8c075dc62069b3e9a7c1b`. Giữ riêng với các control mới K/K2; không chạy lại script dựng hướng ấy.
- L chỉ tiêm status ở biên guard: ca inactive “revoked” mô hình hoá kết quả dự báo khi sổ canonical rỗng; sổ canonical không rỗng được thử riêng qua status `nonempty-inactive` và chặn rc8. Đây không phải phép đo loader thực phân biệt hai nguồn, cũng không cho phép bỏ luật False+nonempty⇒chặn.
- Nội dung chốt lúc `2026-09-07T22:05:12.813487+00:00`; wall time từ mốc user giao khoảng 2042.8 giây (34.0 phút), dưới 60 phút. Verdict đã được ghi từ đầu lượt, không chờ phút 45.

Biên nhận máy cuối ở `scratch/r4b/artifact-validation.json`; hash VERDICT cuối được xuất riêng ra stdout để tránh tự tham chiếu trong nội dung được băm.
