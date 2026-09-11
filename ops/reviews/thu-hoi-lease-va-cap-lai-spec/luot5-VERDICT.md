verdict: changes_requested
reviewed_spec_sha256: 23a7deaf60af17aea2fa3b027d08fb8c187b6f03499f34540822ab7b9c3b1672
reviewed_sha: b416830ef2a509d60203d55552ce17950afcf67c
reviewed_tree: 266a2aba97d925dac3ab7473dda55adb0fe23b8e
model_tu_khai: GPT-6 / Codex theo cấu hình phiên; provider OpenAI, API với công cụ shell cục bộ, transport machine. Không có chứng thực độc lập backend/model variant/effort; không suy identity từ tiêu đề hoặc submitter.

# Cross-review r5 — lượt 5, lời gọi 6/6

**changes_requested — còn 3 nhóm P1 (S1, S2, S3) và 2 nhóm P2 (S5, S6). S4 ĐÓNG.** Không cộng đúp các ID lịch sử. **S1/S2 thuộc hình dạng nguồn tin cậy ⇒ checkpoint kế + ADR nguồn tin cậy trước thi công. S3 là lỗi hợp đồng nghiệm thu/mutant, không phải một nguồn thẩm quyền mới.** Đây là lời gọi cuối; không đề nghị thêm model review, không reset bộ đếm theo revision/PR/slice. Trạng thái tiếp theo của packet là `blocked` theo stop condition; verdict nội dung đặc tả vẫn là `changes_requested`.

Bắt đầu theo user: 2026-09-07T22:07:34Z. Đã ghi khung VERDICT ngay từ đầu và bổ sung checkpoint 22:15Z; bản này tổng hợp bằng chứng cuối. Q13/Q14/comment PR #475 `5575587924` và quyền dùng call 6 được **chấp nhận theo chỉ thị user như lời khai điều phối đã readback offline**. Không đòi chốt lại hai lựa chọn, không giả đã gọi API.

Kho review chỉ đọc. Chỉ đọc task-data trong cwd; không mạng; không gọi agent/reviewer khác; không commit/push/comment/merge. Scratch mới ở `scratch/luot5/`, tái dùng script hợp lệ `scratch/luot4b/` qua loader, không sửa script cũ. Bản spec trong mirror cùng hash; HEAD/tree không đổi. Các file skill của kho được đọc như tài liệu hiện trạng, không chạy quy trình launcher/land của chúng.

`HINT.patch` chỉ là unified diff lên SPEC.md, dùng `patch -p0`; **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Patch mô tả hợp đồng đề xuất cho checkpoint/ADR; không tự cấp authority hoặc cho phép tiếp tục packet. Kiểm khả năng áp trên bản sao được ghi ở cuối bản này.

## Bảng finding lượt 1–4b → trạng thái

“ĐÓNG” là đóng vấn đề hợp đồng cụ thể; không phải chứng nhận implementation r5. Giữ hạng lịch sử. Các ID R/N/L1 chuyển tiếp về S không được đếm lần nữa. “ĐÓNG SAI” của S3 nghĩa là bản sửa r5 phát sinh assertion/catalog sai, không phủ nhận no-replace đã sửa vector R2.

Bằng chứng mới đều dưới `scratch/luot5/`: **D** `measure-r4.json`; **P** `probes-r4.json`; **G** `coverage-r4.json`; **E** `extra-r4.json`; **L** `loop-r4.json`; **K/K2** `controls-r4b.json` / `default-control-r4b.json`; **V** `contracts-r5.json`; **O** `objects-r5.json`. Tên r4 trong output là do tái dùng harness; không phải dùng kết quả cũ rồi đổi nhãn thành chạy mới.

| ID lượt 4b | Hạng | Trạng thái r5 | Bằng chứng / điều còn lại |
|---|---|---|---|
| S1 adapter-environment-boundary-is-not-specified | P1 | ĐÓNG-MỘT-PHẦN | Q4.1 có env từ rỗng, endpoint nội bộ control V=0. Predicate HTTP và profile chỉ ghi tập khoá chưa ràng buộc giá trị/chuỗi thực thi; phân tích bên dưới. |
| S2 raw-object-read-does-not-verify-content-identity | P1 | ĐÓNG-MỘT-PHẦN | Q4.5 đã yêu cầu băm bytes blob; control O xác minh 1186 object sạch. Chưa khép mọi cạnh tree/parent dùng quyết định; claim băm bắt graft không đủ. V cũng chỉ ra routing object-store còn bỏ trống. |
| S3 a6-single-mutant-is-shielded-by-cli-flag | P1 | ĐÓNG SAI | A6 r5 đòi replacement→12 dù env+cờ giữ object gốc, và hứa triple mutant đọc giả dù profile còn chặn. Chỉ MÔ TẢ; không dựng replacement. |
| S4 q13-selected-mode-conflicts-with-a5-and-ready-fields | P1 | ĐÓNG | Q3/A5/Q12 nay là union policy/ngoại lệ có neo/không neo. V: policy11; ngoại lệ rời0/giao11; không neo12; hỏng12; [] cả hai phía8. Không còn đòi SHA policy chưa tồn tại. Producer/retirement là S6. |
| S5 m9-check-publisher-consumer-is-unspecified | P2 | ĐÓNG-MỘT-PHẦN | Đã chọn check-run và có bootstrap audit bền. Chưa chứng minh kênh STEP_SUMMARY→output.summary, dispatch→H và phép join provenance độc lập; consumer vận hành chưa được chỉ định cụ thể. V receipt0/âm12 chỉ là model. |
| S6 q13-exception-scope-and-retirement-are-not-bound | P2 | ĐÓNG-MỘT-PHẦN | Có descriptor, sự kiện hết hiệu lực, cấm quay lại. V mismatch12; nhật ký retired đọc lại khớp. Chưa có producer/verifier trong repo chưa có dispatcher và cơ chế không bỏ lỡ sự kiện policy xuất hiện rồi biến mất. |

| ID lịch sử | Hạng | Trạng thái r5 | Bằng chứng / giới hạn |
|---|---|---|---|
| R1 canonical-url-check-does-not-bind-transport | P1 | ĐÓNG-MỘT-PHẦN | Endpoint tường minh/control nguồn đúng0; phần biên process còn S1. |
| R2 replace-refs-bypass-oid-pinning | P1 | ĐÓNG | Q4 giữ cả env+cờ no-replace. S2 là độ đầy đủ object graph; S3 là assertion/catalog. Không chạy replacement ở lượt này. |
| R3 bootstrap-gate-trusts-pr-and-arrives-too-late | P1 | ĐÓNG | Workflow ở A0; §write_set:266–273 audit exact S/H/tree + catalog + giữ đóng/readback bền. P inactive 0/12/12/12; V journal. |
| R4 inactive-a0-already-changes-lease-decisions | P1 | ĐÓNG | Q3/Q5 giữ luật cũ; P product0/DU_BAO8, mutant bật sớm8; L 5 cửa inactive giữ behavior, sổ không rỗng chặn. |
| R5 admission-head-is-not-the-landed-candidate | P1 | ĐÓNG | M9 exact S/fetched H/event H/T/current base/tree(M). P control0, base/fetch/tree/checker lệch12. Publisher còn S5. |
| R6 self-declared-effective-set-shrinks-exclusion | P1 | ĐÓNG | Q3 không nhận tự khai làm nguồn; V/P [] phía ứng viên hoặc holder đều8, giao thật11. Q13 đã được chủ kho chốt. |
| R7 symlink-resolution-lacks-source-and-termination-contract | P2 | ĐÓNG | Q3 từng occurrence OID, hợp đích, relative parent, vòng/depth12. E: cùng blob hai cây→other/a.md và docs/a.md; parent tệp mới đúng; vòng12. |
| R8 cutover-delta-and-fixed-g2-smoke-conflict | P1 | ĐÓNG | Q6 delta(a)/(b)/(c), C=null không prerequisite A1. E gate1→4 và sau C, khi g2 hết hạn, tập wp461=∅; không hứa1g2. |
| R9 a8-mode-case-cannot-kill-stated-mutant | P1 | ĐÓNG | P mode: đúng8, only-new8 sống; combined0 bị ca giết; unit full-T12. A8 khai đúng. |
| R10 spec-review-label-does-not-waive-review-cap | P1 | ĐÓNG | Q14/call6 có authority được user cho chấp nhận. §0 không còn tự miễn review-spec. Sau call này phải checkpoint/ADR; câu cuối Q14 còn typo P3. |
| N1 canonical-remote-identity-unbound | P1 | ĐÓNG-MỘT-PHẦN | K/K2/V đúng nguồn/default0; phần process/profile còn S1. |
| N2 snapshot-pinned-after-unverified-recapture | P1 | ĐÓNG | Q4 local map trước discovery; K ref đổi bình thường sau capture vẫn đọc S cũ. |
| N3 admission-workflow-does-not-cover-canonical-updates | P1 | ĐÓNG | M9 mọi PR default, không path/author/rc9 filter, retarget+dispatch+queue gate. E trigger model; association/publisher chưa đo, S5. |
| N4 canonical-checker-bootstrap-is-circular | P1 | ĐÓNG | A0 có workflow/checker inactive; lần land đầu có audit riêng+freeze. Mã mới chưa có trong base(rc2) là hiện trạng, không là điều kiện cần trước lease viết A0. |
| N5 effective-write-set-and-symlink-resolution-missing | P1 | ĐÓNG | Closure tính lại theo nguồn được chọn, symlink từng occurrence; V/P/E. Không gọi ngoại lệ Q13 đã có authority là fallback tự phát. |
| N6 historical-cutoff-revives-feature-holders | P1 | ĐÓNG | G history hai cây W8/mutant0; E gate1→4 được Q6 nhận diện là delta bảo thủ có điều kiện. |
| N7 candidate-map-omits-entry-mode | P1 | ĐÓNG | M4 tuple(mode,type,blob), P mode8/fullT12. Không materialize symlink có nội dung YAML. |
| N8 record-lease-guard-has-no-candidate-id | P1 | ĐÓNG | L route/parser/state thật + guard tiêm: candidate x, sống0; revoked8/stale/event x, không record_lease. |
| N9 acceptance-prepublish-and-second-parent-contradictions | P1 | ĐÓNG | P pure0/0 vs CLI12/12 rồi11/11; parent2 giữ0/mất8. E exact pair tách wrong path/blob/tag/pull/local-only12. |
| N10 authorization-json-and-url-contract-is-open | P2 | ĐÓNG | Q2 sáu keys/type/duplicate/block/API envelope. P/G control0, lệnh hỏng8, account4, HTTP/envelope12. |
| N11 readback-after-admission-lifecycle-undefined | P2 | ĐÓNG | Q2.3/A9: kiểm lại trước canonical404→12; sau canonical0 lời gọi lịch sử thêm. P model, không API thật. |
| L1 authority-signature-evidence-false | P1 | ĐÓNG | D raw Git: mỗi commit một gpgsig; b416830 PGP,6635379 SSH. Hai marker không phải hai chữ ký; không suy người thao tác. |
| L1 default-ref-is-untrusted-cache | P1 | ĐÓNG-MỘT-PHẦN | K2 server main thắng master, so map cũ12; nguồn tiến trình còn S1. |
| L1 standalone-revocation-has-no-admission-gate | P1 | ĐÓNG | Q2/M4/M9 phủ standalone, P readback404→12; bootstrap riêng đã có. Interface check còn S5(P2). |
| L1 evidence-mention-is-not-an-authorization | P1 | ĐÓNG | Q2 đúng block/giá trị/kiểu; P prose/prefix/broken8, control0. |
| L1 write-set-exclusion-is-incomplete | P1 | ĐÓNG | Q3 toàn lease, exact/prefix/case-fold/symlink/closure; P/E/V ca hợp lệ. S6 là provenance/lifecycle của ngoại lệ. |
| L1 snapshot-check-does-not-fence-writers | P1 | ĐÓNG | Q3 phân biệt ảnh chụp với grant; Q11 C→dừng worker→g3→readback→start. Không nhận guard là fencing của land. |
| L1 reads-are-not-pinned-to-one-snapshot | P1 | ĐÓNG | Q4 một map trước so + một clock; K pinning. Hash/cạnh object là S2 riêng. |
| L1 legacy-fallback-conflicts-with-ledger | P1 | ĐÓNG | P legacy0, reservation thắng8, historical reverse8; Q6 cutover đã sửa. |
| L1 append-only-check-misses-candidate-and-merges | P1 | ĐÓNG | P candidate sửa8/parent2keep0/loss8/mode8; M9 strict tree. Tính toàn vẹn đường đọc là S2 riêng. |
| L1 packet-loop-guard-is-partial-and-boolean | P1 | ĐÓNG | L 35 tổ hợp/40 guard calls; unknown byte-match, revoked idempotent; helper-only mutant lộ3 cửa bỏ sót. |
| L1 acceptance-confuses-refs-blobs-and-mutations | P1 | ĐÓNG-MỘT-PHẦN | G3pair/4ref và1pair/3ref đúng; A5/A8 đã sửa. A6 vẫn S3. |
| L1 revocation-schema-and-error-contract-incomplete | P2 | ĐÓNG | Giữ kết luận đóng từ r3/4b; r5 không sửa hợp đồng kế thừa M1, Q2 errors/mode đã đối chiếu. Bundle này không có nguyên SPEC.r3.md: không tuyên bố đã đọc/chạy lại full M1. |
| L1 size-estimate-and-slice-anchor-are-stale | P2 | ĐÓNG | D +409/+368/+328 và31 commit khớp; tổng825–1195/6path đúng phép cộng; vẫn là ước. |
| L1 ready-and-rollout-decisions-are-not-closed | P2 | ĐÓNG-MỘT-PHẦN | Q7–Q14 phân biệt contract/facts, chưa ready khi thiếu; S5/S6 còn producer/consumer/retirement cụ thể. |

## Findings mới

Các mục dưới giữ ID S ổn định của cùng vấn đề; phần mới r5 được nêu cụ thể, không đổi slug để reset fingerprint.

### S1 — adapter-environment-boundary-is-not-specified · P1 · nguồn tin cậy

**Vị trí:** SPEC:184–200, đặc biệt191–197; §0.2:65; câu “tận cùng”381. **Độ tin: cao với lỗi predicate; không có probe tấn công.**

Env từ rỗng đã sửa đúng ambient inheritance. Nhưng allowlist `credential.*`/`http.*` cộng kiểm *chuỗi trong giá trị* không phải validator Git config. Với khoá `http.sslVerify`, Git nhận giá trị boolean riêng; giá trị boolean ấy không chứa nguyên cụm tên-khoá-dấu-bằng mà câu192 tìm. Tương tự giá trị của `http.proxy` là endpoint, không cần chứa chữ `proxy=`. Vì receipt chỉ ghi **tập tên biến env**, đường+băm Git và endpoint, đổi giá trị `GIT_CONFIG_KEY_n/VALUE_n` mà giữ tập tên biến có thể giữ nguyên hồ sơ được so. Spec đã chỉ ra một phép kiểm có thể nhận cấu hình trái chính yêu cầu TLS/proxy của nó.

`http.*` còn gồm cấu hình theo URL, CA/trust, redirect và định tuyến như `http.curloptResolve`; cần parse khoá đầy đủ, kiểu/giá trị và phạm vi URL. Định tuyến DNS riêng nó không phá TLS nếu hostname/trust còn ghim: không nhận nó là bypass độc lập. `credential.helper` có thể chọn chương trình; họ credential không tự là tập dữ liệu vô hại. `core.*` **không được** kế thừa theo allowlist hiện tại — đó là phần đã đóng; không viện ra core như một khe ambient còn được phép. Tuy nhiên sửa routing cache S2 bằng cách quay lại Git repo gốc mà đọc config của nó sẽ mở lại biên này.

`GIT_ALLOW_PROTOCOL=https` giới hạn tên protocol, không chứng minh identity của helper HTTPS, CA/proxy hay redirect cuối. `PATH` tối thiểu + executable tuyệt đối giải một lần là tiến bộ; chỉ băm executable chính chưa chỉ rõ bộ Git/helper/runtime nào thuộc nền tin cậy. Không đòi băm đệ quy cả OS: cần **runner/deployment profile được duyệt, bất biến trong invocation**, bao gồm phần thực thi transport và trust store. “Ghi băm vào receipt” không thay phép so với mỏ neo độc lập đã duyệt.

**Đã chạy:** V control dựng env từ rỗng + endpoint bare qua API nội bộ, discovery0,1 call,188 byte; K/K2 default/pinning0. Không băm `/usr/bin/git` vì nằm ngoài cwd; không chứng nhận production profile. **Chỉ MÔ TẢ:** mọi trường hợp giá trị HTTP/credential, env bẩn, helper/executable hay nguồn khác; không soạn config/assignment/payload của chúng.

**Sửa ở Q4.1/A2/Q12:** allowlist hữu hạn **khoá + kiểu + giá trị/phạm vi**, không wildcard credential/http hoặc substring; profile digest gồm cấu hình không bí mật và định danh/version credential/CA/helper đã duyệt, độc lập caller. Unknown/mismatch12. ADR chốt nền runner/transport được tin. **Ca khoá:** profile sạch0, cùng tập tên biến nhưng giá trị ngoài profile12, helper/trust/redirect ngoài profile12; điều phối dựng ca âm. **Hệ quả:** có thể chặn deployment hợp lệ chưa đăng ký; xử bằng duyệt profile có receipt, không fallback thừa kế env.

### S2 — raw-object-read-does-not-verify-content-identity · P1 · nguồn tin cậy

**Vị trí:** SPEC:207–214,154–175,239–243,292,302–317. **Độ tin: cao về lỗ hợp đồng đường dữ liệu; ca bytes/graph sai chỉ MÔ TẢ.**

Băm blob đúng là fix thật. Nhưng quyết định còn phụ thuộc **các cạnh chọn object**, không chỉ identity của leaf được chọn. Q4.5 nêu đường *commit canonical→tree→sổ*, blob lease/symlink và commit trên ancestry; chưa ràng buộc đầy đủ tree trung gian của **mọi occurrence local/remote**, cây H/M, policy/schema và cây mốc lịch sử. Một blob lease hợp lệ, băm đúng, chưa chứng minh nó nằm tại path nào dưới commit đã quảng bá. Một lời khai “sổ vắng” cũng phải có cây cha đã xác minh chứng minh absence, kể cả namespace con không được thấy.

Commit object băm bao gồm **tree và toàn bộ parent header**. Vì vậy **đủ** cho ancestry *nếu* thuật toán đi đúng các parent OID trích từ bytes ấy và xác minh tiếp object cần đọc. Nó **không đủ** nếu lấy kết luận/đồ thị từ `merge-base`/revision walker/metadata tăng tốc rồi chỉ băm các commit được walker đưa ra. Graft/metadata thay cách traversal không nhất thiết sửa raw commit bytes; câu212 “băm bắt luôn graft vì object thay thế có OID khác” không phải chứng minh tổng quát. Không kết luận mọi Git flag đều vô dụng hoặc đã chạy graft; no-replace vẫn là một chốt riêng. Phải nêu nguồn các cạnh traversal và cách kiểm tương đương với raw parents, hoặc tự đi đồ thị đã xác minh; lỗi/thiếu/giới hạn traversal→12.

**Control có vấn đề cụ thể về object-store:** Q4.5 bảo dùng “env adapter”; Q4.1 đã đặt `GIT_DIR` về repo tạm mới. V cho thấy discovery0 nhưng cùng env ấy, `cat-file --batch` với commit hợp lệ của source trả `<OID> missing` (Git rc0, reader phải12). Không hề có object hỏng. R5 chưa có bước đưa object vào repo tạm hay API đọc cache riêng. Đừng sửa bằng một biến caller chọn repo khác; phải mô tả reader dữ liệu có store đúng, vẫn cách ly config/ref/runtime. Đây là phần routing cần làm rõ cùng sửa S2, không cộng thêm một finding P1.

**Đã chạy:** O đọc và băm đúng commit/tree/blob, parse tree binary/parent header trên object sạch:1186 object,4,311,029 byte cho scan lease; witness S→H có9 commit, DFS đã thăm1815 commit; full parent closure toàn mirror2622 commit. K raw object/ancestry/fsck control0. **Chỉ MÔ TẢ:** bytes lệch OID tại bất kỳ leaf/tree/commit, replacement/graft và metadata cache làm đổi đường quyết định. Không tạo chúng.

**Sửa Q4.5/M4:** đặc tả API object-store, tập roots, mọi cạnh từ bytes đã xác minh, memoize theo(type,OID) trong snapshot; parser/ancestry/path map ăn cùng bytes. Bao gồm từng commit occurrence→các tree cha→lease/symlink, S/H/M→sổ, policy+schema, mốc lịch sử và inputs xác minh code/workflow. Không cần băm mọi tree của mọi commit tổ tiên nếu cây đó không tham gia quyết định. **Ca khoá:** graph hợp lệ nhiều parent/đường/mode0 hoặc mã nghiệp vụ đúng; fixture điều phối hỏng ở từng cạnh→12; control repo tạm có thể đọc đủ objects. **Hệ quả:** chi phí theo số object reachable; đặt giới hạn fail-close và đo, không cắt graph rồi coi vắng là thật.

### S3 — a6-single-mutant-is-shielded-by-cli-flag · P1 · tiêu chí nghiệm thu

**Vị trí:** SPEC:66–67,207–212,346–350,367–368. **Độ tin: cao về mâu thuẫn predicates.**

A6 mới viết `refs/replace` cho OID canonical **⇒12 (bị lớp băm bắt)**. Nhưng khi hai chốt no-replace đang hoạt động, reader đọc **object gốc**, băm ra đúng OID gốc: lớp băm không có mismatch để bắt. Một implementation đúng về “không đổi cây/nguồn” có thể giữ nguyên verdict control0. Assertion bắt buộc12 vì riêng sự hiện diện replacement có thể làm code đúng đỏ; nếu muốn policy từ chối presence thì cần một detector riêng được nêu rõ và có trong catalog.

Catalog cũng quên chốt **profile ghim Q4.1**. Bỏ biến env làm tập khoá hồ sơ khác: validator còn nguyên có thể12 trước `cat-file`. Bỏ cả env+cờ+băm vì thế **chưa đủ** để hứa “đọc bản ghi giả”; profile/detector còn lại có thể che. Không được khai sống/chết vô điều kiện cho mutant khi chưa ghi seam và các chốt giữ nguyên. Dùng mutant sửa luôn expected profile/catalog sẽ là thay oracle, không phải giết mutant độc lập A12.

**Bảng phân tích, KHÔNG CHẠY replacement:**

| Ca | Chốt còn lại / kết quả có căn cứ |
|---|---|
| Replacement hiện diện, env+cờ+băm đủ | Đọc object gốc; hash khớp; verdict nguồn giữ như control, hoặc12 nếu có detector presence riêng. Không suy12 từ băm. |
| Chỉ bỏ cờ CLI | Env vẫn giữ object gốc; không buộc giết bằng ca này. |
| Chỉ bỏ env | Cờ giữ object gốc; profile có thể chặn12 trước I/O. Ghi lớp thực sự phát hiện; không gán công cho hash. |
| Bỏ env+cờ | Nếu profile cho tới reader, hash còn bắt bytes replacement; nếu không, profile đã chặn. |
| Bỏ env+cờ+băm | Profile/detector còn nguyên vẫn có thể chặn; **không đủ** hứa đọc giả. |
| Bytes cache thực sự lệch OID, không qua replacement | Ca riêng giết việc bỏ xác minh bytes tại seam reader, nếu không còn detector khác che; điều phối dựng, not_run. |

**Đã chạy:** K/O clean-object controls, V clean env0; không gọi bất kỳ mutant nguồn/bytes bị cấm nào. **Sửa A6/A12:** thay assertion replacement bằng “cây/verdict canonical không đổi hoặc12 có nguyên nhân”; ca bytes mismatch riêng luôn12; catalog độc lập ghi seam, đầy đủ chốt, native rc/reader rc và kết quả quan sát. Chỉ hứa kill tổ hợp đã chứng minh reachable. **Hệ quả:** số mutant “chết” được nhận có thể giảm; phải giữ tên/số mẫu độc lập, không bù bằng xoá ca hoặc nới oracle.

### S5 — m9-check-publisher-consumer-is-unspecified · P2

**Vị trí:** SPEC:69,298–318,361–366,397–398,407–419. **Độ tin: cao về phần hợp đồng còn thiếu; GitHub thật not_run.**

Có tên publisher/consumer là tiến bộ. Nhưng `GITHUB_STEP_SUMMARY` là kênh job summary; câu314 đồng nhất nó với trường Checks API `output.summary` **chưa có bằng chứng readback trong bundle**, cũng không có bước/API ghi check output được đặc tả. Không thể coi việc ghi tệp summary là control publisher hoàn chỉnh. Receipt model V chỉ chứng minh consumer có thể chấp nhận *khi object API đã chứa đúng receipt*, và từ chối khi không có field ấy; nó không chứng minh GitHub đã vận chuyển receipt đến đó.

Lời khai check-run `cong` id101767296495 dưới head1ebd86e được giữ đúng nhãn điều phối; tôi **không có raw API object** để so `head_sha`, run/job/attempt, workflow definition. Suy cùng event cho workflow mới phải giữ là inference như §chua_do_duoc10. Hơn nữa M9 có **workflow_dispatch**: input H không tự là OID mà native job/check-run gắn vào. Cần canary riêng với H≠S, không suy association của dispatch từ phép đo pull_request_target.

`workflow OID == canonical` cần nguồn đối chiếu **độc lập receipt**: join check_run→job/run/attempt→event/repository/PR→definition commit S/path/blob. So OID do chính receipt tự ghi chỉ là lời khai lặp lại; tên job+App GitHub Actions không định danh một workflow. Phải phân biệt commit nguồn workflow, blob workflow, code thực chạy tại S và mốc bootstrap A0 — S sau A1 không mặc nhiên là code A0.

Consumer code/checklist cụ thể cũng chưa ở write set. Tệp `.claude/skills/land-packets/SKILL.md` hiện chỉ có prepare/gate/guard chung, không có phép đọc mới này. Không đồng nhất nợ *land đọc sổ* với *land đọc receipt*, nhưng cả hai đều không tự xuất hiện do nhắc tên land-packets. Chốt nơi cưỡng chế/người vận hành/receipt bền trước ready A0, hoặc dependency riêng nếu cần code/App/quyền ngoài scope.

**Giữ P2, không nâng theo suy đoán:** Q10 đã chặn activation khi thiếu facts. Lượt offline này chưa chứng minh rằng mọi lane Actions không thể xanh hay một check-run thật có số thẩm quyền sai. Phần chắc chắn là executor còn phải tự thiết kế và đo giao diện vận chuyển/tiêu thụ.

**Đã chạy:** V control receipt0, wrong head/app/independent workflow/missing summary12; P exact candidate0/âm12; bootstrap audit local đọc lại khớp. **Sửa M9/Q10/A11/Q12:** định nghĩa kênh lưu receipt có readback thật, joins độc lập, consumer có tên; job summary/comment chỉ là projection cho tới khi có raw evidence về kênh authority. Dispatch chưa chứng minh H association thì không tạo pass; dùng lane PR đã xác minh hoặc dependency publisher được duyệt. **Ca khoá:** canary từng event với H≠S, thiếu/sai join, summary-only, same-name khác workflow; exact H control thật bắt buộc. **Hệ quả:** có thể cần capability/scope bổ sung; giữ inactive, không tự nâng quyền.

### S6 — q13-exception-scope-and-retirement-are-not-bound · P2

**Vị trí:** SPEC:155–165,414–424; protocol§3.2/§5; ADR-0025. **Độ tin: cao về lifecycle/producer chưa nêu.**

Tag union Q12 đã giải việc không có policy SHA. Nó **không tạo người có quyền** duyệt dữ liệu phái sinh. Repo hôm nay chưa có dispatcher thực hiện phép dẫn xuất ấy; protocol không cho agent tự khai. Q13 đã phê chuẩn lựa chọn ngoại lệ, không biến mỗi descriptor do executor viết thành verified receipt. Còn thiếu producer, verifier và phép bind descriptor với Packet/revision/generation/spec_hash/approved object body. Placeholder body_sha256 chưa điền là dependency trước ready, không được dùng một băm reviewer bịa để điền; không cần xin lại lựa chọn(i)/(ii).

Retirement theo **sự kiện**, không cần tự thêm ngày UTC. R5 ghi “receipt A1 kế tiếp”, nhưng A1 là slice kích hoạt đã xong; policy có thể xuất hiện nhiều ngày sau. V dựng ba commit Git hoàn toàn bình thường A(vắng)→B(có policy fixture)→D(vắng), rồi đưa lần lượt cả ba lên ref canonical của fixture và đọc lại journal: reader chỉ nhìn D thấy cùng trạng thái “vắng” như A. “Không cache kết luận còn miễn” không chứng minh B chưa từng tồn tại. Model current-only cho0; model nhận event retired bền cho12. Đây là minh hoạ phần thiếu cơ chế, **không tuyên bố model current-only tuân toàn bộ r5**.

Cần xác định ai ghi event retired khi policy được nhận, journal nào là authority, và reader xử lý khi chưa có record/đã bỏ lỡ transition thế nào. Journal phải chỉ rõ các cây thật sự được canonical nhận: một commit feature có policy rồi bỏ trước merge không tự là sự kiện hết ngoại lệ. Nếu policy canonical mới làm closure/check/hash thay đổi, phải pause/re-evaluate và revision/generation theo§5/ADR-0025 trước chạy tiếp; không tự chuyển những lease còn sống sang policy mới dưới descriptor exception cũ. Policy hiện diện nhưng hỏng vẫn12, không fallback.

**Đã chạy:** V policy11/ngoại lệ0/không neo12/hỏng12/[]8; descriptor mismatch12; A→B→D thật; journal retirement ghi/đọc khớp. Body/object Q13 thật không có trong bundle để tự băm lại. **Sửa Q3/Q12/Q13:** descriptor validator với nguồn approved độc lập, producer/verifier có authority bền; chưa có dispatcher thì proposed tới khi có người vận hành được chỉ định hợp lệ hoặc predecessor cung cấp; retired event tại chính transition policy, hồi phục từ lịch sử/journal đã xác minh, không chờ “A1 kế tiếp”. **Ca khoá:** mismatch12, mất/journal không đo được12, policy xuất hiện rồi mất giữa hai read vẫn không quay lại ngoại lệ, source đổi kéo đúng revision/generation. **Hệ quả:** có thể tăng việc đọc lịch sử và có thêm readiness dependency; không grandfather lease hoặc tự mở rộng ngoại lệ sang packet khác.

## Phản chứng đã chạy lại + mới

Lệnh chạy (mọi output mới trong `scratch/luot5/`):

```text
PYTHONDONTWRITEBYTECODE=1 python3 scratch/luot5/run_reused.py measure_r4.py
PYTHONDONTWRITEBYTECODE=1 python3 scratch/luot5/run_reused.py allowed_coverage.py
PYTHONDONTWRITEBYTECODE=1 python3 scratch/luot5/run_reused.py controls.py
PYTHONDONTWRITEBYTECODE=1 python3 scratch/luot5/run_reused.py default_control.py
PYTHONDONTWRITEBYTECODE=1 python3 scratch/luot5/run_reused.py extra_r4.py
PYTHONDONTWRITEBYTECODE=1 python3 scratch/luot5/run_reused.py loop_r4.py
PYTHONDONTWRITEBYTECODE=1 python3 scratch/luot5/run_reused.py baseline_r4.py docs
PYTHONDONTWRITEBYTECODE=1 python3 scratch/luot5/run_reused.py baseline_r4.py doctrine
PYTHONDONTWRITEBYTECODE=1 python3 scratch/luot5/contracts_r5.py
PYTHONDONTWRITEBYTECODE=1 python3 scratch/luot5/objects_r5.py
PYTHONDONTWRITEBYTECODE=1 python3 scratch/luot5/retirement_readback_r5.py
```

`contracts_r5.py` gọi lại `allowed_probes.py` qua loader, tái dùng functions/Git fixture của nó. Loader chỉ đổi scratch path, danh sách hash có mặt, clock phân loại; trong extra bỏ đoạn xoá object cũ. Các harness trên đều rc0; docs/doctrine child rc0. P26 mục JSON, G4, E10, L35 tổ hợp/40 guard calls — **không phải số acceptance pass hoặc số test của implementation r5**. Trace giữ command/native rc/outputs; state/receipt models có rc riêng trong JSON.

| Ca chạy mới | Kết quả | Mức bằng chứng |
|---|---|---|
| A5 nguồn policy/ngoại lệ/không neo | 11;0(rời)/11(giao);12 | Model nhánh r5, policy mapping và descriptor fixture độc lập; chưa là schema production |
| Policy hỏng / descriptor lệch / [] tự khai | 12/12/8 ở cả hai phía | V; positive và negative đều có |
| Policy A→B→D + retirement journal | Có object tại B, vắng tại A/D; current-only0 vs event-bền12 | Git bình thường + lifecycle model, không thay byte dưới OID |
| Adapter env từ rỗng, endpoint đúng | 0,1 discovery,188 byte; default main | V; protocol file chỉ là seam API fixture, production HTTPS not_run |
| Adapter dùng nguyên GIT_DIR rỗng đọc object | cat-file rc0 nhưng `missing`, reader12; source cùng OID type commit | V; chứng minh thiếu routing, không tấn công nguồn |
| Clean raw objects | K: 3 hash khớp/fsck0; O1186 hash khớp | Đọc bytes hợp lệ và parse cạnh trực tiếp |
| A0 inactive | S/T rỗng0; T có sổ12; thêm sổ+xóa workflow/test12; S bẩn12 | P Git trees+model checker canonical |
| Bootstrap ghi bền | Journal JSON đọc lại khớp, catalog3, có hash | V local control ghi/readback; chưa là audit chủ kho/Actions thật |
| M9 receipt+strict tree | 0 control; base/fetch/tree/checker/head/app/join lệch12 | P/V; synthetic API facts, không tạo check-run thật |
| A1 cardinality | 3(blob,path)/4ref;1blob ngoài known-list | G ordinary Git; known-only để X sống, có phép đỏ |
| A2 cardinality/default/map | 1pair/3ref; main/master đúng; map hiện tại0/map cũ12 | P/K/K2; same-source fixture |
| History đóng / cutover | W8/mutant0; gate1→4; sau C khi g2 hết hạn∅ | G/E fixed OIDs/clock |
| Symlink occurrence/vòng/parent | other/a.md + docs/a.md; vòng12; nested/dest/new.md | E symlink chỉ nội bộ, không resolve host path ngoài cây |
| Mode/merge | old-entry mode8, single only-new8 sống, combined0; full-T unit12; parent2keep0/loss8 | P ordinary Git; không materialize link YAML |
| Q2 API/JSON/lifecycle | control0; command8; account4; HTTP/envelope12; downstream thêm0call | P/G models, không HTTP |
| A10 5 cửa | 18 rc0,17 rc8 trong35 tổ hợp; unknown byte-match, revoked1event/idempotent | L entrypoint/parser/state thật, doctor/guard snapshot tiêm trong bộ nhớ |
| A12 catalog độc lập | đủ=true; bỏ invocation=false; bỏ cả registration+invocation=false | P model oracle độc lập, không catalog production |

**Chỉ MÔ TẢ, not_run:** remote helper giả, remote.vcs/rewrite nguồn, env đổi nguồn/executable giả, replacement/graft/metadata làm đổi traversal, bytes cache lệch OID, đường thoát cây, đồng tự Unicode/chuỗi thoát. Không dựng/chạy lại hướng bị cấm từ script khác. Các ca âm S1/S2/A6 thuộc điều phối, với oracle độc lập và chốt profile/raw-reader phải được ghi rõ.

**Không chạy nguyên suite nền:** `lease_publish_test.py` có ca symlink ra ngoài cây (t19), `packet_loop_test.py` có ca ngoài cây và executable giả. Chỉ tái dùng harness hợp lệ theo phân công lượt này; không tạo số N/N mới từ suite rút ca. Số121/121 hoặc278/278+81 trong spec là bằng chứng lịch sử, không phải kết quả lượt5.

## Tiêu chí A1–A12

| Tiêu chí | Đơn vị / phép đỏ thật | Mutant và khả năng xanh/đỏ r5 |
|---|---|---|
| A1 | Holder=tập ID; dòng revoked theo(blob,path); MAP_REF theo occurrence | G3pair/4ref,1blob ngoài known-list; bỏ nạp sổ/known-only/không in đều có phép phân biệt. Smoke∅/{g2} theo clock đúng. |
| A2 | 1pair/3ref; identity/default/map/rc | Control nguồn đúng xanh K/K2/V; local default/any-ref/fallback có mục tiêu đúng. S1 chưa đủ predicate profile; ca đổi nguồn not_run. |
| A3 | 5 mã8/0/8/0/8; hai tree lịch sử; product vs DU_BAO | P/G fixedW8 vs mutant0; bật sớm product8 thay0 bị bắt. Không tự nhận forecast là grant. |
| A4 | Hai nguồn chết(sổ/history), có/không thay thế; live0 | Q3 chiều ngược trước thay thế có phép đỏ. Historical reverse được chạy; full ma trận output sản phẩm chưa có. |
| A5 | Closure/path/OID; claim sai8; giao11; unknown12; publication exact pair | V đã sửa đúng ba nhánh: không còn policy-vắng-có-neo mà bắt12; companion cần policy fixture. Pure0/0 không là cấp lease; CLI trước12/sau11. S6 là binding/transition, không phục hồi mâu thuẫn S4. |
| A6 | Pinned map/OID, identity bytes, process profile; thời gian median3 cặp | **S3:** replacement bắt buộc12 không suy từ hash khi no-replace đủ; triple mutant còn bị profile che. Clean controls đã chạy; ca bytes sai chưa chạy. Component benchmark O không phải ratio end-to-end≤2. |
| A7 | Mỗi constraint M1/type/mode/authority/clock một ca; rc4/8/12 và precedence | P command8/envelope12/inactive12/mode fullT12. Entry cũ mode8 qua append-map khác entry mới parser12 là nhất quán. Full schema r3 không có trong bundle, không nhận N/N. raise→continue phải so verdict thật kể cả11, không chỉ grep/count. |
| A8 | Map(mode,type,blob), parents, S/H/T/checker | P đúng8, single-only-new8 sống, combined0 mới bị ca mode giết; full-T unit12. Parent2 giữ0/mất8; strict tree control0/âm12. S5 chưa actual check association. |
| A9 | Endpoint/globalID/repo/Issue/login/block/type/bytes-hash và call count | P/G control/âm phân biệt; trước canonical404→12, sau canonical thêm0call. HTTP thực/object Q8 chưa có. |
| A10 | 5 cửa×4trạngthái, target ID/state bytes/history/attempt/idempotence | L35 tổ hợp gồm mutants/inactive. REST403 chỉ là điều kiện độc lập Git; không giả đã gọi REST403. Full guard adapter r5/disk failure/fencing chưa chạy. |
| A11 | Cùng môi trường base/candidate, delta theo tên; lint, check provenance, positive evidence | Docs0+ok:true/doctrine0; full suite không chạy vì giới hạn user, candidate chưa có. A0 checker model không thay Actions; A1 phải canary từng event S5. Không gọi skipped/not-created hoặc receipt tự khai là pass. |
| A12 | Catalog/expected/executed/failed/skipped/not_run; seam và lớp che mutant | P catalog độc lập có thể đỏ cả xoá registration+lời gọi. Phải sửa catalog A6 S3; không giảm mẫu số để giữ banner xanh. Số mục model không phải N/N sản phẩm. |

## Nhất quán luật và kích thước slice

| Nguồn | Kết luận |
|---|---|
| §3.2 / ADR-0025 | Q12 tag đúng kiểu absence; producer/phái sinh vẫn không được tự khai, S6. Spec/Issue/revision/generation/hash phải đóng băng, đổi source/closure/check/hash theo luật. Đây chưa là lease/ready của bất kỳ slice nào. |
| §4 / ADR-0028 | Q5/Q11 đúng stale/dừng worker/giữ last SHA-state-journal/generation mới. Không hồi sinh g2. Giữ retention tới mission land/hủy+30ngày; cleanup sau process dừng/readback, không thuộc quyền lượt review. |
| §5 | Q3 exact/prefix/NFC/casefold/symlink/closure toàn repo; ngoại lệ Q13 có authority đã chốt, không miễn ready packet khác. Retirement phải pause/re-evaluate và không tự tái miễn, S6. Strict up-to-date của M9 chủ động bỏ ngoại lệ§5.1 là luật chặt hơn đã khai, không mâu thuẫn. |
| §8 / CLAUDE.md | Phải đo behavior, bằng chứng dương, bytes đã đến; catalog A6 còn lời hứa vượt phép đo S3. App/job name/summary projection chưa là receipt authority S5. Read-only, exact hashes và identity khai đúng; hint chỉ chữ hợp đồng. |
| §12 | Call6 có authority của user/Q14;4a đã sinh output vẫn tính call. Không suy số review_rounds đã validate từ số calls. R5 đúng ở dừng sau trần, nhưng câu “hai lớp tận cùng” chưa được chứng minh S1/S2; lần tái diễn này kích hoạt checkpoint+ADR, không vá rồi tự gọi7. |
| ADR-0044 | A0=3tệp,+560–780;A1=3,+90–160;B=2,+160–240;C=1,~15. Tổng825–1195,6path duy nhất. Chỉ A0 vượt300 theo ước; đã có lý do ngoại lệ có phạm vi. Không lấy tổng bốn slice áp trần một packet hoặc lấy mốc lịch sử chứng minh ước đủ. |

A0/A1/B/C phải có objective, acceptance, Issue/spec/lease riêng; slice sau mọc trên base đã nhận slice trước. M9 cần mã canonical trước khi dùng quyền; predecessor chỉ còn ở PR/integration chưa đủ cho điều đó. Những phần cắt ngang adapter/object-source hiện có P1 không được gọi Stable Slice để land rồi hẹn ADR sau. `numstat` implementation và scope consumer/profile mới phải đo trước review/ready theo luật; không bịa con số thay thế.

## Q7–Q14: câu thiếu và đáp án bắt buộc

| Câu | Còn phải chốt/đo | Đã bắt buộc/đã chốt |
|---|---|---|
| Q7 | Issue/spec/lease từng slice; người audit A0 và scope ngoại lệ dòng | A0→A1→B→C; workflow ở A0; acceptance/base tự đủ; không né trần bằng PR chồng lấn. Chưa được tiến tới packet triển khai khi S1/S2 còn P1. |
| Q8 | Object lệnh thực trên #461, sáu field/type/account và body readback | C=null; Q13/Q14 PR#475 không thay authorization thu hồi; g3 riêng theo Q11. |
| Q9 | Chủ kho chốt lựa chọn sản phẩm nhận event cho lease đã hết hạn | Khuyến nghị nhận; event không gia hạn/tái dùng ID hoặc tự tạo holder. Chưa có lời khai chốt Q9 tương đương Q13/Q14 trong bundle. |
| Q10 | Profile thật; A0 workflow/checker; publisher/consumer joins; canary PR+dispatch; protection/directpush/bypass/strict/tree/queue; delta/lane đã dừng | Thiếu facts⇒False. Naming required check không đủ. Sổ rỗng S/A1; Q13 là lối(ii), không tự đổi sang buộc #473 trước A1. |
| Q11 | Người tuần tự hoá, C land/worker dừng/lastSHA-state-journal/g3 readback | C→dừng worker→check/land/readback g3 mới→start. Snapshot0 không fencing, không thay quyền grant/merge. |
| Q12 | **Ai dẫn xuất, ai xác minh/duyệt descriptor khi chưa có dispatcher**; approved profile; object-reader/API store; publisher/consumer dependency | Không tự nhận owner field/hash tự viết là authority. Không kế thừa miễn phái sinh b416830. Hợp đồng thiếu⇒proposed; runtime facts thiếu⇒inactive. Không cần code A0 chạy trước lease viết code, nhưng contract phải đủ. |
| Q13 | Điền body hash thực, bind Packet/hash; producer/verifier và retirement event/journal/missed-transition | **ĐÃ CHỐT(ii)**, ngoại lệ phép giao raw+symlink tới sự kiện policy hợp lệ đầu tiên. Không đặt thêm deadline; không tự quay lại sau retirement; không tự khai effective[]. |
| Q14 | Ghi durable counter6/6 và checkpoint/ADR; facts budget mission khác chưa có | **ĐÃ CHỐT trần6**; hết P1 thì Packet Issue theo chỉ thị, còn P1 như lượt này thì checkpoint kế+ADR. Không còn call dự phòng. Câu “Lượt4 phóng trên bản này” là P3, sửa thành accounting cuối đúng. |

Không thiếu một lựa chọn(i)/(ii) hay một lần xin trần mới. Câu còn thiếu nằm **trong Q12/Q10/Q13**: producer/verifier/consumer cụ thể và cơ chế authority bền của chúng. Reviewer không tự trả lời thay chủ kho bằng fixture.

## Bảng đo lại

D đọc Git mirror; native CLI/docs/doctrine chạy bản sao mới với origin bare nội bộ. Clock lịch sử là phân loại frozen data tại giờ chỉ định, không quan sát GitHub live. Các số API chỉ có lời khai được giữ nhãn, không biến thành phép đo offline.

| Lời khai / đơn vị | Kết quả đo lượt5 | Khớp / giới hạn |
|---|---|---|
| Hash SPEC và bản untracked trong mirror | 23a7deaf60af17aea2fa3b027d08fb8c187b6f03499f34540822ab7b9c3b1672 | Khớp đầu/cuối |
| SPEC.r4 / VERDICT4b / HINT4b | 415ce35d… /7d3017ec… /4a0321fd… | Full hash kiểm trước đọc; không chứng thực model lịch sử |
| HEAD/tree/core.abbrev | b416830ef2a509d60203d55552ce17950afcf67c /266a2aba97d925dac3ab7473dda55adb0fe23b8e /7 | Detached; worktree chỉ spec untracked |
| Ref theo công thức SPEC | **303=302remote+1localmaster**;299 unique tips | “mirror302” trong lời giao là số remote, không tổng theo công thức |
| Pair/path/lease_id/multiblob-ID | **288/273/273/7** | Khớp; không lấy ref thay pair |
| Live/chưa bia mộ | 13:41Z **8/4**;14:33:15Z và22:12Z **7/3** | Clock fixed ngày07-09; khớp |
| Tại09:52Z08-09 và10:17:12Z08-09 | **1/1** rồi **0/0** | Toàn repo, không phải wp461 holder sauC |
| #456 expiry | 2026-09-07T14:30:07Z | Đã hết hạn tại review |
| Gate r1/r2/r3/r4 expiry08-09 | 03:37:33/07:50:35/09:44:51/10:17:12Z | Khớp; gate-r4 hết sau g2 25phút12giây |
| Wp461 r1/r2/g2 expiry08-09 | 03:05:00/05:27:42/09:52:00Z | Khớp; C không tạo g3 |
| r2 blob26f07b4 /fdfde3a | 4ref/1ref | Offline không có PR#475 ref thứ5 [API] |
| #456 blob8b2103c /1f95042 | 11ref/1ref | Khớp |
| Tomb canonical/feature; feature divergence | **7/11;0 trái,31 phải** | G kiểm7tuple hai chiều; D có full OID/ref |
| Chữ ký raw | b416830:1gpgsig PGP;6635379:1gpgsig SSH | Không chạy keyring hoặc suy actor; marker BEGIN/END không đếm chữ ký |
| kiem→_lease_cham_duong | 0 call AST | Khớp nền |
| Guard schema5cửa nền | record-lease1,begin-attempt1;record-post/transition/record-review0 | Khớp, chưa phải guard r5 |
| planned lease | 3 ID, đều hết hạn tháng08 | Khớp |
| Policy/schema/sổ/workflow mới trên HEAD | Đều vắng | Cả schema đúng path coordination và root-path được đo; không suy đã triển khai |
| `ai-dang-giu` 4 path wp461 | Cả4 rc11,NGƯỜI_GIỮ2 | E native offline, không claim source authority |
| Native check g2 /check g2 thêm EWS[] | 0/0 | Nền vẫn nhận extra field; khác V model r5 phải8, không gọi là r5 fail |
| Native kiem-thu-hoi-github nền | rc2, command chưa có | Dependency thực của A0, không lập luận bootstrap không bao giờ làm được |
| Doc claims strict | rc0, **ok:true**,10 layers,367advisory,70,861stdout byte | Bản sao cùng core.abbrev7; không assert “không advisory” |
| Doctrine scan | rc0,8tệp,0chỗ chép | Bao gồm spec r5 bản sao; không sửa mirror |
| Lease/packet-loop full suite | **not_run lượt5** | Lịch sử121/121(wrapper),120/121thiếu actionlint;278/278+81mutant chỉ kế thừa. Không chạy ca user cấm |
| #250 /#275 /#248 numstat | +409/−0; +368/−0; +328/−1 | Khớp: #250 là2SPEC, không code; full per-file D |
| Kích thước slice | A0 560–780;A1 90–160;B160–240;C15; tổng825–1195 | Đúng phép cộng; estimate, chưa có code numstat |
| Adapter env sạch | Git2.43.0;0,1call,188byte,0.006418s | Bare API fixture; executable hash/production TLS not_measured |
| Object scan lease qua bytes băm | **1186=299commit+599tree+288blob;4,311,029byte;0.211283s** | Đường lease+canonical absence; chưa tính full symlink/prefix/closure, là phần công việc tối thiểu |
| Ancestry S→feature H | DFS1815commit visited, witness9commit | S=b416830…;H=02b0b86…; không lấy31commit riêng làm bound traversal |
| Full parent closure toàn mirror | **2622commit;3509object tổng;8,782,600byte** | Cộng với tree/blob scan ở trên; không băm mọi tree của lịch sử |
| Component benchmark cat-file batch | Không băm median0.114994s; có băm0.106707s; ratio0.927938;3cặp,1Git command/lượt | Cùng1186object/4,311,029byte; chênh nhỏ có nhiễu, không kết luận băm tăng tốc. **Không phải** A6 end-to-end≤2 |
| Check-run101767296495/H1ebd86e và các lần lặp | **Không đo lại offline** | Lời khai EVIDENCE; raw check/job/run/output chưa được giao. Không kết luận con số đúng/sai từ một synthetic receipt |

Chi phí object theo invocation là số object **khác nhau thật sự dùng**, không phải3object(commit/tree/blob), không phải số ref, và không nhất thiết bằng số commit riêng của H. Cận đo1186 chưa có closure symlink/prefix; đường ancestry dài có thể thêm hàng nghìn commit. Không cần băm cây của commit tổ tiên không dùng, hoặc fetch mọi object qua mạng chỉ để băm. Phải đo candidate hoàn chỉnh cùng baseline mới nghiệm thu ratio≤2; spec chưa có implementation nên không thể nhận con số component ở đây làm pass.

## chua_do_duoc

1. Implementation r5 chưa tồn tại: chưa có full M1×consumer, full A1–A12 N/N, delta suite hay benchmark CLI end-to-end; không có candidate numstat.
2. Không chạy các hướng user cấm, kể cả khi script cũ có thể tạo chúng. Full suite nền cũng chưa chạy lượt5 do có các ca ấy. Điều phối phải cung cấp fixture/receipt hợp lệ để nghiệm thu sau ADR, không nhờ reviewer lách phân công.
3. Không mạng: Q8 object thật, body hash Q13 thật, identity người/PAT, TLS/proxy/CA/credential/helper/executable production, ruleset/bypass/directpush/strict/queue, Actions check-run/job/run/attempt/summary mapping và dispatch H association đều chưa đo.
4. Không đọc executable ngoài cwd để băm; V chỉ ghi version/path và env keys của control fixture. Không bịa production profile digest.
5. SPEC.r3.md nguyên bản và HINT.luot3.patch không có trong bundle này, cũng không có commit mang spec ấy trong lịch sử mirror được giao. M1/A7 “như r3” chỉ đối chiếu được qua hash tham chiếu, verdict lịch sử và các harness; executor phải có bản dependency đúng hash khi đóng băng Packet. Đây là giới hạn bundle, không tự kết luận mọi schema cũ bị xoá khỏi hợp đồng.
6. Không có receipt rollout thực: audit bootstrap chủ kho, khoảng giữ đóng canonical, mốc A0, retired event thực, producer phái sinh và consumer land được chỉ định, worker-stop/lastSHA/state/g3 readback. Các journal ở scratch là control, không cấp authority.
7. Không xác minh độc lập model/backend/effort/token/wall metadata lịch sử hoặc tổng budget mission. Call6 được tính theo authority user; số review rounds hợp lệ chỉ tăng sau validation/receipt, chưa làm thao tác đó.
8. SHA1 object format khớp mirror đang review; không mở scope SHA256 repositories hoặc đòi hash cả OS. Nền runner tin cậy/giới hạn tài nguyên/raw graph/provenance phải được ADR chốt, không tuyên bố “tận cùng” từ việc đã băm một nhóm object.

## Kiểm artifact cuối

Hoàn tất 2026-09-07T22:47:21.684502+00:00; 2387.7 giây theo wall clock kể từ mốc user, trong trần60phút. `HINT.patch` có 12 hunk, phủ S1/S2/S3/S5/S6; sha256 `8ca8474be2654a60d9e5a98d688f442e940c8ab12521a4f07697c25ef4621ab9`. `patch --dry-run -p0` rc0; áp bằng `patch -p0` trên bản sao rc0; bytes kết quả bằng SPEC.proposed.md. Mirror HEAD/tree/ref-map/status giữ nguyên, tracked diff rc0, không shallow; SPEC gốc và bản untracked trong mirror giữ đúng hash được review. Chi tiết command/rc nằm ở `scratch/luot5/artifact-validation.json`. Không áp hint lên SPEC.md gốc hoặc cay-kho.
