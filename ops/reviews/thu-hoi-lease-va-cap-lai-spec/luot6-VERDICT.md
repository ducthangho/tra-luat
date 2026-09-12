verdict: changes_requested
reviewed_spec_sha256: f78135cff428f0744476d7f27426f459d926578c4bac4a4339928330c4a0d6a5
reviewed_sha: b416830ef2a509d60203d55552ce17950afcf67c
reviewed_tree: 266a2aba97d925dac3ab7473dda55adb0fe23b8e
model_tu_khai: GPT-6 / Codex theo cấu hình phiên; provider OpenAI, bề mặt API/Codex với công cụ shell cục bộ, transport machine. Không có chứng thực độc lập build/variant/effort; không suy model từ người đăng verdict.

# Cross-review r6 — lượt 6, lời gọi 7

**changes_requested — còn 3 P1: S1, S3, S7; 3 P2: S5, S6, S8. S2 và S4 ĐÓNG.** S1 thuộc hình dạng **nguồn tin cậy**, cần quyết định nền thực thi mà ADR sẽ ghi. S3 là lỗi tiêu chí/mutant; S7 là xung đột biểu diễn bản ghi với parser sổ, **không thuộc hình dạng nguồn tin cậy**. S8 là phần hợp đồng vận hành object-store mới còn thiếu, P2; không giữ S2 ở P1 chỉ vì thiếu số trần hoặc hỗ trợ layout.

Bắt đầu theo user: `2026-09-08T03:12:57Z`. Ghi VERDICT sơ bộ ngay đầu lượt rồi bổ sung. Reroute comment PR #475 `5578460203` (review tới hết P1, lời gọi này là 7, không reset ID/bộ đếm) được nhận **theo chỉ thị user**, không giả đã readback API. Không lấy “chưa có ADR” hoặc trần cũ làm P1 tự thân; không tự trả packet về `blocked` chỉ vì câu cũ của r6. Đây là verdict nội dung, không phải lease/kích hoạt/approval triển khai.

`cay-kho/` và `kho.git/` chỉ đọc; chỉ đọc task-data trong cwd; không mạng, không agent phụ, không commit/push/comment vào kho review. Mọi fixture Git, thay ref bình thường, clone, partial clone, mode và symlink đều ở `scratch/luot6/`. Không dựng lại hoặc chạy các hướng user cấm. **Toàn bộ harness lượt này viết mới**; scratch cũ đã mất. Native CLI chạy bản sao riêng tại `scratch/luot6/native-copy/`.

`HINT.patch` là diff chỉ lên `SPEC.md`, dùng `patch -p0`; **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**. Không có hunk mã gate/runtime/workflow. Executor phải ghi `hint_provenance`, cập nhật revision và tự kiểm trên bản triển khai; không nhận model trong scratch là nghiệm thu sản phẩm.

Ký hiệu bằng chứng mới: **M**=`scratch/luot6/measurements.json`; **C**=`controls.json`; **F**=`more-controls.json`; **G**=`admission-controls.json`; **P**=`partial-and-symlink.json`; **N/N2**=`native.json`/`native-followup.json` (đều cùng thư mục). Mọi số cũ chưa chạy lại được ghi rõ, không chuyển thành số lượt 6.

## Bảng finding lượt 1–5 → trạng thái

ĐỐI CHIẾU LƯỢT TRƯỚC: “ĐÓNG” dưới đây là kết luận về hợp đồng, không tuyên bố implementation r6 đã tồn tại. R/N/L1 là ID lịch sử, không cộng lại vào số finding còn mở. S7/S8/S9 là ID mới của lượt này.

| ID lượt 5 | Hạng giữ nguyên | Trạng thái r6 | Bằng chứng / phần còn lại |
|---|---|---|---|
| S1 adapter-environment-boundary-is-not-specified | P1 | ĐÓNG-MỘT-PHẦN | Q4.1 bỏ dò substring và có mỏ neo digest. F profile fixture khớp hằng trong mã ⇒0. Chưa ghim execution/trust closure phía sau executable Git, helper/CA directory và nền runner; phân tích S1. |
| S2 raw-object-read-does-not-verify-content-identity | P1 | ĐÓNG | Q4.5 buộc mọi cạnh từ bytes cha đã băm, parser ăn cùng bytes, raw-parent traversal; C đọc commit/tree/blob0, thiếu routing12; G pinning; M witness9. Không còn kết luận graft đổi raw bytes. Layout/availability/budget là S8 P2 riêng. |
| S3 a6-single-mutant-is-shielded-by-cli-flag | P1 | ĐÓNG-MỘT-PHẦN | Replacement⇒verdict không đổi đã sửa. A6 vẫn hứa kill nhầm ca routing/profile; C.catalog cho12/12,12/12. Bỏ băm cần seam sau cat-file rõ ràng. |
| S4 q13-selected-mode-conflicts-with-a5-and-ready-fields | P1 | ĐÓNG | Ba nhánh policy/ngoại lệ/không neo + union Q12 còn đúng; F=11/0/11/12, tự khai[]⇒8. Lỗi tệp metadata mới là S7, không mở lại mâu thuẫn policy-vắng cũ. |
| S5 m9-check-publisher-consumer-is-unspecified | P2 | ĐÓNG-MỘT-PHẦN | Artifact là kênh cụ thể, STEP_SUMMARY đã rút; dependency có tên. Chưa khép API join/attempt/retention, SHA event, quyền đọc và thứ tự bootstrap. C.m9 chỉ là model. |
| S6 q13-exception-scope-and-retirement-are-not-bound | P2 | ĐÓNG-MỘT-PHẦN | Producer=chủ kho, verifier=hằng canonical là tiến bộ. C descriptor0; A/B/D có tệp thật. Cần bind descriptor với activation context và quy tắc tệp lịch sử khi policy đổi/rollback; bản ghi chưa có biểu diễn được M1 nhận (S7 mới P1). |

| ID lịch sử | Hạng | Trạng thái r6 | Căn cứ đối chiếu lượt này |
|---|---|---|---|
| R1 canonical-url-check-does-not-bind-transport | P1 | ĐÓNG-MỘT-PHẦN | Endpoint tường minh/cô lập; G discovery sạch0, phần tiến trình còn S1. |
| R2 replace-refs-bypass-oid-pinning | P1 | ĐÓNG | Repo tạm không ref + no-replace + băm. Replacement chỉ MÔ TẢ; không dựng ref ấy. |
| R3 bootstrap-gate-trusts-pr-and-arrives-too-late | P1 | ĐÓNG | M9 ở A0, audit bootstrap ngoài cây PR, giữ đóng + receipt bền; lịch consumer còn S5 P2. |
| R4 inactive-a0-already-changes-lease-decisions | P1 | ĐÓNG | Q3/Q5 giữ verdict cũ khi inactive, DU_BAO riêng; bản ghi thu hồi khi inactive vẫn12. Metadata mới cần phân tuyến S7. |
| R5 admission-head-is-not-the-landed-candidate | P1 | ĐÓNG | Exact S/H/T, current base==S, tree(M)==T còn nguyên; G/M đo cây từ OID. Giao diện API không suy từ model, S5. |
| R6 self-declared-effective-set-shrinks-exclusion | P1 | ĐÓNG | Q3 tự tính closure, không tin[]; F claimed_empty8. |
| R7 symlink-resolution-lacks-source-and-termination-contract | P2 | ĐÓNG | P: cùng lease blob ở hai commit, alias→docs/a.md và other/a.md, hợp cả hai. Vòng/thoát cây chỉ đọc hợp đồng, không chạy. |
| R8 cutover-delta-and-fixed-g2-smoke-conflict | P1 | ĐÓNG | Q6 delta(a)/(b)/(c), C=null, smoke tập thật; M đo lại expiry. Không còn đòi g2 sống sau10:17:12. |
| R9 a8-mode-case-cannot-kill-stated-mutant | P1 | ĐÓNG | G mode: đúng8/only-new8; combined0; unit full-T12. Khai đúng mutant sống. |
| R10 spec-review-label-does-not-waive-review-cap | P1 | ĐÓNG | Reroute mới user cấp rõ; kế toán cũ P3 S9, không dùng để đình chỉ lời gọi7. |
| N1 canonical-remote-identity-unbound | P1 | ĐÓNG-MỘT-PHẦN | G control cùng nguồn0; phần profile còn S1. |
| N2 snapshot-pinned-after-unverified-recapture | P1 | ĐÓNG | G map chụp trước, cache ref đổi sau vẫn dùng H/tree cũ; map stale⇒12. |
| N3 admission-workflow-does-not-cover-canonical-updates | P1 | ĐÓNG | M9 mọi PR vào default, không lọc path/author/rc9, edited/queue có hợp đồng; API thật chưa đo S5. |
| N4 canonical-checker-bootstrap-is-circular | P1 | ĐÓNG | A0 có mã inactive + audit ngoài workflow. N new-command rc2 là hiện trạng base, không phải điều kiện bất khả thi để viết A0. |
| N5 effective-write-set-and-symlink-resolution-missing | P1 | ĐÓNG | Q13 ngoại lệ đã được cấp; Q3 closure/occurrence; F/P chạy lại model và cây thật. |
| N6 historical-cutoff-revives-feature-holders | P1 | ĐÓNG | Q6 chốt mốc sau A0 + delta có điều kiện. M đo base7 tomb vs feature11; không nhận HEAD hiện tại làm mốc đã có. |
| N7 candidate-map-omits-entry-mode | P1 | ĐÓNG | G cùng blob100644→100755: tuple-map8. |
| N8 record-lease-guard-has-no-candidate-id | P1 | ĐÓNG | Q5 target ID ứng viên trước record_lease; AST nền xác nhận cần5 cửa. Lượt này không chạy lại ma trận state machine cũ. |
| N9 acceptance-prepublish-and-second-parent-contradictions | P1 | ĐÓNG | Q3 tách hàm thuần/CLI, G/F Git merge S cha2 giữ0/mất8. |
| N10 authorization-json-and-url-contract-is-open | P2 | ĐÓNG | Q2 đúng6keys/type/duplicate/URL/envelope và thứ tự rc; đọc lại nguyên hợp đồng, không giả chạy API. |
| N11 readback-after-admission-lifecycle-undefined | P2 | ĐÓNG | Q2.3/A9 trước canonical đọc lại, sau canonical0 lần thêm; artifact mới không đổi hiệu lực event lịch sử. |
| L1 authority-signature-evidence-false | P1 | ĐÓNG | M: mỗi commit1 gpgsig; b416830 PGP,6635379 SSH. Không lấy2 marker làm2 chữ ký, không suy actor. |
| L1 default-ref-is-untrusted-cache | P1 | ĐÓNG-MỘT-PHẦN | G server main thắng master, pinning0; execution trust còn S1. |
| L1 standalone-revocation-has-no-admission-gate | P1 | ĐÓNG | M9 phủ standalone/rc9, M4 readback phần mới; publisher còn S5. |
| L1 evidence-mention-is-not-an-authorization | P1 | ĐÓNG | Q2 exact block và so kiểu/giá trị; prose không là lệnh. |
| L1 write-set-exclusion-is-incomplete | P1 | ĐÓNG | Q3 all-lease/exact/prefix/case-fold/occurrence; F/P model/cây sạch. Ngoại lệ lifecycle còn S6. |
| L1 snapshot-check-does-not-fence-writers | P1 | ĐÓNG | Q3 snapshot≠grant, Q11 C→stop→g3→readback→start; land fencing nợ có tên, không nhận đã làm. |
| L1 reads-are-not-pinned-to-one-snapshot | P1 | ĐÓNG | Q4 map một lần/clock một lần; G đổi ref vẫn đọc OID đã chụp. S2 đã khép đường bytes. |
| L1 legacy-fallback-conflicts-with-ledger | P1 | ĐÓNG | Q3/Q6 precedence sổ>lịch sử, chiều ngược, cờ inactive; đọc hợp đồng kế thừa. |
| L1 append-only-check-misses-candidate-and-merges | P1 | ĐÓNG | F cha2 giữ0/mất8, G mode8; tệp metadata mới riêng S7. |
| L1 packet-loop-guard-is-partial-and-boolean | P1 | ĐÓNG | Q5 cả5 cửa/3state/idempotence/error giữ bytes. Không nhận 35 ca/40 calls của lượt5 là số mới. |
| L1 acceptance-confuses-refs-blobs-and-mutations | P1 | ĐÓNG-MỘT-PHẦN | F3 pair/4 ref và1 pair/3 ref đúng; G A8 đúng. A6 vẫn S3. |
| L1 revocation-schema-and-error-contract-incomplete | P2 | ĐÓNG | Khôi phục r3 đúnghash, đọc trực tiếp M1. Không phải full parser N/N. Schema metadata mới riêng S7. |
| L1 size-estimate-and-slice-anchor-are-stale | P2 | ĐÓNG | F numstat merge-base→head:409/368/328; tổng825–1195 đúng phép cộng. Chưa có numstat implementation. |
| L1 ready-and-rollout-decisions-are-not-closed | P2 | ĐÓNG-MỘT-PHẦN | Q7–Q14 có phần bắt buộc/phần facts; các hợp đồng còn S5/S6/S8, không yêu cầu quyết lại Q13/Q14. |

## Findings mới

Các S1/S3/S5/S6 dưới giữ fingerprint cũ; nội dung mới của r6 được chỉ rõ. Không cộng đúp aliases R/N/L1.

### S1 — adapter-environment-boundary-is-not-specified · P1 · nguồn tin cậy

**Vị trí:** SPEC:209–224, đặc biệt215–218. **Độ tin:** cao về phần digest bỏ sót; các hướng đổi hành vi chỉ MÔ TẢ.

So digest với hằng canonical đã sửa lỗi “receipt chỉ ghi tên biến”: caller không thể đổi một thành phần *đã được đo thật và nằm trong digest* mà vẫn khớp mỏ neo (bỏ qua phá hàm băm). Đường Git, bytes Git, version, tệp CA, giá trị proxy nếu đều được chuẩn hoá và băm đúng đã được ràng buộc. Không nói “caller có thể chọn input” tự nó phá băm. Thay binary Git thông thường làm băm đổi ⇒12; đổi ubuntu image làm Git đổi có thể bị chặn hợp lệ, cần đăng ký profile mới.

Nhưng danh sách215–216 chưa mô tả đầy đủ **những gì thực thi transport/trust**: tên helper không định danh bytes chương trình mà tên đó phân giải tới; hash executable Git chính không định danh transport HTTPS helper và runtime/shared libraries; `http.sslCAPath` chấp nhận **thư mục** nhưng digest chỉ nói băm **tệp** CA, không có manifest thư mục/default trust store. Cùng Git chính/version/tên helper/đường CA directory và cùng digest được liệt kê có thể đi qua bộ helper/runtime/trust material khác. Đây là thay input không nằm trong hàm băm, **không phải** tìm collision. R6 chưa đặt nền image/runtime ấy ra ngoài biên caller bằng một hợp đồng bất biến/được duyệt, nên vẫn cho executor tự ngầm tin nó.

Không cần băm đệ quy cả OS. Cần chốt một nền thực thi được tin: runner/image hoặc deployment manifest bất biến, bao gồm Git, chương trình HTTPS/credential thực sự dùng, runtime và toàn bộ trust store hiệu lực; ai sở hữu/cấp manifest, ai duyệt neo và ai giữ bất biến suốt invocation. “Commit có review” đủ để lưu mỏ neo, chưa chỉ định producer độc lập của giá trị neo. Không được tính digest từ chính deployment tuỳ ý rồi tự đăng ký làm accepted trong cùng lượt chạy.

Các chỗ vận hành cùng block cần ghi rõ: `credential.<url>.username` chỉ được scope URL canonical nào; các khoá Git được chuyển sang argv/env thế nào; `http.proxy` và hai biến proxy có thể xung đột theo thứ tự ưu tiên; host/port/scheme allowlist thực tế **chưa được giao**. Remote container dùng proxy + CA riêng có thể chạy với profile được duyệt; allowlist tên khoá không chứng minh profile ấy đã tồn tại. Đường HOME/GIT_DIR tạm phải được kiểm theo vai trò/ownership, không băm literal đường tạm vào một digest bất biến cho mọi invocation. Đổi image/profile phải fail-close tới khi neo mới qua quy trình duyệt; image đổi mà phần được băm không đổi vẫn cần kiểm image/manifest identity.

**Control mới:** F.profile env dựng từ rỗng, đổi thứ tự khoá, digest `0b756e06…` bằng hằng trong mã ⇒0. Tệp identity/CA là **dữ liệu fixture trơ**, không phải Git giả, helper hay CA hoạt động; không execute chúng. G discovery trên endpoint bare nội bộ0/1 call/621B. Không băm binary/CA hệ thống ngoài cwd; không chứng nhận production image/TLS/proxy.

**Vá:** Q4.1/A2/A6/Q10/Q12 quy định manifest/nền được duyệt, canonical serialization, immutable invocation và việc cập nhật neo. **Ca khoá:** positive profile thật trên runner được phép; ca do điều phối cung cấp giữ digest phần cũ nhưng đổi helper/runtime/CA-directory phải bị chặn bởi profile hoàn chỉnh; mọi ca âm nguồn chỉ MÔ TẢ ở lượt này. **Hệ quả:** runner mới có thể12 cho tới khi được đăng ký; phải có lộ trình duyệt profile, không fallback về env ambient. Đây là phần ADR cần quyết, không phải finding “thiếu tệp ADR”.

### S3 — a6-single-mutant-is-shielded-by-cli-flag · P1 · tiêu chí

**Vị trí:** SPEC:382–391. **Độ tin:** cao, có control/model mới trong C.catalog.

R6 đã sửa đúng `refs/replace` nguồn ⇒ verdict không đổi. Bỏ riêng/cả hai no-replace còn bị repo tạm không ref che: khai **sống** là đúng. Không chạy replacement theo phân công.

Hai lời hứa kill còn sai:

| Ca mà r6 chỉ tới | Bản đúng | Mutant được nêu | Kết quả |
|---|---|---|---|
| (iv) đầu vào đã thiếu routing, expected12 |12|Bỏ routing:12|SỐNG; không có khác biệt để giết |
| Giá trị **ngoài miền** (389), expected12 |12|Bỏ riêng so digest:12|SỐNG; validator miền209–214 còn chặn |
| Positive object-store hợp lệ, expected0 |0|Bỏ routing:12|ĐỎ thật, đây mới là ca khoá routing |
| Giá trị **trong miền cho phép**, nhưng khác profile approved, expected12 |12|Bỏ riêng so digest:0|ĐỎ ở model nếu không còn phép so profile trùng khác |

Dòng388 dùng “ngoài profile”, dòng389 lại định nghĩa “ngoài miền”: hai tập ấy không được dùng thay nhau. Dòng221 còn phép so “hồ sơ khác hồ sơ ghim” — nếu đó là chốt độc lập, nó cũng che mutant bỏ digest. Phải thống nhất rằng đó là cùng một phép so, hoặc khai mutant sống và chỉ rõ seam bỏ cả chốt tương đương.

Ca băm (i) cũng phải ghi **seam sau khi cat-file đã cung cấp response hợp lệ về framing, trước kiểm OID**. “Fixture cache” ở mức pack/loose disk không bảo đảm tới được seam này: Git có thể từ chối lỗi nén/framing/index trước. Khi ấy bỏ băm vẫn12, không được nhận công. Ngay sau cat-file, parser/readback downstream cũng có thể che nếu chỉ so rc cuối: ca unit nên kiểm không giao bytes chưa xác minh cho parser; ca tích hợp phải giữ các chốt downstream hợp lệ hoặc khai mutant sống. Không tạo bytes lệch OID để kiểm ở lượt này.

**Vá:** A6/A12 ghi input, expected, seam, từng chốt còn nguyên; dùng positive routing0 để giết mutant; profile trong-miền/khác-neo làm ca digest; các ca ngoài miền chỉ kiểm domain validator. **Ca khoá:** C đã đo routing0→12, (iv)12→12; predicate model profile12→12 và12→0. **Hệ quả:** số mutant credited có thể giảm; không sửa expected của ca lỗi thành0 để ép đỏ.

### S5 — m9-check-publisher-consumer-is-unspecified · P2

**Vị trí:** SPEC:299–302,340–355,401–406,Q10. Artifact + tên dependency là sửa thật; không còn suy STEP_SUMMARY thành output.summary.

Mũi tên `check-run → run_id` chưa chỉ ra khoá API. Check-run không được mặc nhiên có trường `run_id`, và tên job/app không định danh một workflow. Một đường cần đặc tả và canary là: raw check-run → `check_suite.id` → liệt kê workflow runs lọc suite, phân trang, lấy đúng run → jobs của **run attempt cụ thể**, đối chiếu `check_run_url` với check-run đang xét → artifacts của run, chọn bằng artifact ID. Không lấy run_id trong receipt hoặc parse URL giao diện làm thẩm quyền; không đồng nhất job ID/check-run ID. Các endpoint dự kiến: `GET /repos/{o}/{r}/check-runs/{id}`, `GET /repos/{o}/{r}/actions/runs?check_suite_id=...`, `GET /repos/{o}/{r}/actions/runs/{run_id}/attempts/{attempt}/jobs`, `GET /repos/{o}/{r}/actions/runs/{run_id}/artifacts` và download artifact theo ID. **Lượt này không gọi mạng và không có raw schema API hiện hành trong bundle; đây là đường đề xuất để điều phối kiểm, không phải chứng cứ API đã chạy.**

EVIDENCE chỉ khai một check xuất hiện dưới H, không đưa raw check/run/job và không suy được `run.head_sha == H`. C.m9 tách giả thuyết run mang H(control0) và run mang S(12). Không dùng model ấy kết luận GitHub thực tế mang S hay H. R6 cần phân biệt SHA check/PR, SHA của run, `workflow_sha` và commit mã checkout; phải chứng minh raw quan hệ workflow-definition==S, không chỉ chép S vào receipt. Nếu mapping thực tế khác giả thuyết r6, phải đổi hợp đồng association trước kích hoạt, không nới so SHA bằng cảm tính.

Chưa có hợp đồng retention/attempt: artifact `name` là container tải xuống, không mặc nhiên JSON trần; cần đúng một receipt file, upload thiếu file là lỗi, artifact ID/digest/expired, attempt khớp job/run hiện tại và lựa chọn khi rerun cùng H. Artifact hết hạn/xoá trước land⇒mất pass và chạy lại; sau land không được làm X sống lại. ADR-0025/0028 cần journal/readback bền của transition, artifact có hạn không thay neo bền. Comment projection đơn thuần không tự thành journal có thẩm quyền.

“dispatch không tạo pass” mới là ý định: cần job chẩn đoán khác tên, không tạo một job `thu-hoi` success/skipped có thể trùng required check; consumer vẫn kiểm event, conclusion, attempt, S/H/T. Quyền đọc Checks/Actions thuộc consumer nào, token nào và upload quyền runtime nào phải ghi rõ; không tự suy upload-artifact cần actions:write, cũng không suy ba quyền340 đủ cho mọi API readback.

Dependency ngoài write set **không làm A1 bất khả thi**: có thể land consumer bằng packet riêng trước A0/A1, với fixture rồi canary sau A0. Nhưng bootstrap đòi “consumer xác minh run đầu” trước mở canonical, trong khi M9 chỉ chốt dependency trước kích hoạt. Phải chốt thứ tự khả thi; hint chọn consumer land trước cửa sổ bootstrap A0, không tự mở write set A0.

**Vá:** M9/Q7/Q10/Q12, schema join và retention/attempt, consumer prerequisite với acceptance riêng. **Ca khoá:** C model control0; missing/expired/unrelated suite/stale attempt/dispatch/run-head-S giả thuyết đều12; raw Actions canary trên chính workflow là phần **chưa đo được**, không gọi pass. **Hệ quả:** thêm dependency chuẩn bị và quyền đọc phù hợp; giữ inactive khi facts thiếu.

### S6 — q13-exception-scope-and-retirement-are-not-bound · P2

**Vị trí:** SPEC:174–183,Q12/Q13. C/F chứng minh producer/verifier fixture so bằng được, retired còn tại D ngăn ngoại lệ current-only sống lại. Chưa có body comment thật để tự băm; đây là thiếu fact trước ready, không là finding tự thân.

Còn phải định nghĩa đối tượng “descriptor trong Issue/lease” là **activation A1 nào** (Packet/revision/generation/spec_hash và repo), đối chiếu với authority được ghim từ canonical nào; không đòi mọi lease lịch sử phải mới có trường này, và không để bất kỳ packet tự copy một hằng chung thành quyền ready. Không tự cấp vai dispatcher từ việc có comment chủ kho.

Tệp retired là sự kiện **policy đầu tiên**, không phải cache của policy hiện tại. R6 chưa nêu `policy_sha256` được so ở lần tạo hay mọi lần đọc. Sau B(P1,R1), policy hợp lệ đổi sang P2 nhưng R1 append-only không thể sửa; phải cho biết R1 vẫn ghi P1, còn closure/check/spec hash so với policy hiện tại qua revision/generation. Tương tự D giữ R nhưng policy vắng: r6 **đã chọn chặn D tại M9**, nên A→B→D không phải một chuỗi canonical được cổng này chấp nhận. Đây không là fail-open. Rollback về policy hợp lệ trước đó khác với xoá policy về trạng thái vắng; trường hợp thứ hai chưa có nguồn closure hợp lệ sau retirement, không được tự gọi là rollback được phép rồi dùng lại ngoại lệ.

PR nào kèm metadata: PR đầu tiên đưa policy hợp lệ vào canonical sau khi guard tồn tại; A0/A1 khi policy còn vắng không tự phải thêm file. Nếu policy đã tới trước khi guard A0 được cài thì phải có bootstrap/revision rõ, không chữa bằng bỏ qua missing metadata. Kích thước và lease của PR policy phải gồm path metadata; nó không được âm thầm thêm vào write set A1/C.

**Vá:** Q3/Q13/Q12 ghi activation context, first-policy semantics, bảng transition, pre-guard bootstrap và rollback policy; S7 giải schema. **Ca khoá:** descriptor fixture hợp lệ0, lệch binding12; B(P1,R1)→B2(P2,R1) phải xử lý theo policy mới mà giữ event cũ; B→D(candidate vắng,R1)12, không quay ngoại lệ; không nhận commit feature có policy rồi bỏ trước canonical là retirement. **Hệ quả:** đổi policy vẫn kéo pause/revision/generation theo §5/ADR-0025, không sửa event lịch sử.

### S7 — retirement-file-conflicts-with-ledger-schema · P1 · mới, không phải nguồn tin cậy

**Vị trí:** SPEC:179–181 đối với M4:322, M1:357–358, A5/A7/A8. **Độ tin: cao.** Bản r3 kế thừa đã khôi phục từ Git và khớp chính hash r6 ghim, xem `scratch/luot6/SPEC.r3.recovered.md:313` (M1) và:319 (append-only).

M1 yêu cầu **mọi** entry `ops/thu-hoi/<lease_id>.yaml` là regular100644, mapping có `schema_version:1`, `event:lease_revoked`, `lease_id==stem`, cùng các trường thu hồi; M4 validate toàn namespace T, Q2 readback mọi bản ghi mới. Tệp r6 bắt buộc `_ngoai-le-closure.retired.yaml` chỉ có `{policy_sha256,oid_T,thoi_diem}`, không có lease_id/event/schema. **Có tệp⇒M1 từ chối; thiếu tệp khi có policy⇒Q13 từ chối.** PR đầu tiên đưa policy vào không có biểu diễn được cả hai hợp đồng chấp nhận. A5 policy11 không thể là ca tích hợp hợp lệ nếu fixture đi qua reader M1 như đã yêu cầu.

C dùng commit Git bình thường: revocation x hợp lệ qua mô hình cấu trúc M1⇒0; B có policy+tệp retired qua lớp hiện diện⇒0 nhưng M1 trên metadata⇒12. Đây là model tối thiểu kiểm đúng điều kiện filename/lease_id đã ghi trong M1, **không** full parser chưa tồn tại. Không cần một payload độc hại để phát hiện xung đột này.

`oid_T` còn có vấn đề biểu diễn: T được M4/M9 định nghĩa là tree(H). Nếu metadata nằm trong T và phải ghi chính T thì sửa trường đó lại đổi blob→tree→T. Hai commit bình thường trong C cho stored-tree khác containing-tree ở cả hai lần “điền OID”. Không gọi đây là chứng minh không có fixed point về toán; đây là yêu cầu tự băm không có quy trình tạo hữu dụng. Nếu `oid_T` định mang nghĩa khác, r6 chưa định nghĩa. **P1 trên M1 ở trên vẫn đứng độc lập**, không cần chọn cách hiểu này để nâng hạng.

**Vá:** Q3 + M1/M4 định tuyến **đúng một path reserved** sang schema metadata riêng; mọi path khác vẫn M1, không bỏ qua cả prefix `_`. Metadata regular100644, exact keys/types/duplicate/order/error contract, append-only như record khác nhưng không đếm là thu hồi/không readback Q2 cho một lease giả. Ghim descriptor hash + policy hash đầu tiên + **S trước khi thêm**, đưa containing H/T vào receipt ngoài cây; không tự tham chiếu. Định nghĩa “sổ rỗng khi inactive” theo tập revocation, metadata vẫn được validator kiểm riêng.

**Ca khoá:** first-policy+metadata hợp lệ qua M4⇒0; thiếu/hỏng/mode sai metadata12; sửa/xoá metadata8; record thu hồi thật khi inactive12; tệp khác gần tên reserved vẫn phải M1; policy đổi sau retirement vẫn giữ marker gốc. **Hệ quả:** đây là thêm schema và nhánh parser có ảnh hưởng authority; A0 phải cài guard trước PR policy, ước dòng phải đo lại. Không tự ghi tệp retired lên repo hiện tại.

### S8 — object-store-layout-and-resource-contract-is-open · P2 · mới

**Vị trí:** SPEC:232–243,A6,Q12. Đây là phần thiếu của API mới; **không phủ nhận S2 đã khép identity/cạnh**.

C: packfile0, `objects/info/alternates` do shared clone thật tạo (chỉ trỏ trong cwd)0. Q4.5 không chỉ đọc loose object. Git vẫn đọc alternate metadata trong object-store nguồn; băm OID bảo vệ identity bytes lấy về, không tự giới hạn nơi đọc, số tầng alternate hoặc chi phí. Phải phân biệt allowlist store dữ liệu do adapter xác định với env caller tự truyền; không “sửa routing” bằng quay lại GIT_DIR/config/ref nguồn.

Literal `<source>/.git/objects` không là API đủ cho bare/linked worktree. C linked worktree hợp lệ: định vị bằng Git git-path đúng nguồn⇒0; ghép literal path⇒Git128/reader12. `.git` ở đó là tệp. R3 A8 đã yêu cầu dùng Git để biết kho, không đoán thư mục `.git`. Cần ghi cách resolve gitdir/common object dir một lần rồi giới hạn read-only stores; `GIT_COMMON_DIR` nguồn vẫn không được kế thừa vào reader tạm.

P dựng **partial clone thật** `--filter=blob:none --no-checkout` qua endpoint file nội bộ: commit/tree đã xác minh và entry x tồn tại, blob x chưa có⇒`missing`/12. Sau Git fetch object thật từ nguồn fixture để chuẩn bị cache mới⇒0. Không phải cache hỏng, và **không** được đổi missing thành “sổ vắng”. Chấp nhận12 khi thiếu dữ liệu là fail-close đúng, không phải bug cần bypass; contract còn thiếu chọn “không hỗ trợ clone thiếu dữ liệu” hay chuẩn bị đầy đủ trước snapshot. C shallow thật: raw-parent traversal gặp parent thiếu⇒12; M1 kế thừa đã nói shallow⇒12. Absence của một entry thực sự vắng dưới tree đã băm có thể chứng minh riêng, nhưng không làm toàn bộ invocation qua nếu còn prerequisite/ancestry thiếu.

Memoize `(type,OID)` là **đúng** với expected type được kiểm mỗi lần và typed Git hash; cùng chuỗi OID bị yêu cầu như blob rồi tree phải12 (C đã đo). Không có finding “memo key phải chỉ là OID”, không giả có object cùng OID hai type hợp lệ. Parser phải dùng actual type/size trong header hash và so expected type; memo không được bỏ kiểm đó.

“Đặt trần fail-close” chưa có đơn vị/giá trị: độ sâu parent tính theo cạnh hay số commit; số object phân biệt; raw byte/object/tổng byte; cây rộng/alias occurrence; thời gian subprocess/đồ thị; số bước alternate. Chỉ depth không chặn đồ thị rộng hoặc blob khổng lồ trước allocation. Số1186/9/2622 là số đo, không là giới hạn. Cho executor tự chọn đồng nghĩa tự chọn miền snapshot hợp lệ.

**Vá:** Q4.5/Q12 ghi layout/stores được hỗ trợ, partial/shallow preflight và thông báo remedy trước snapshot, ngân sách có đơn vị/default ghim trong profile cùng error12 trước cấp phát/timeout. **Ca khoá:** C/P như trên, bound−1/bound/bound+1 ở seam object/byte/depth/time (điều phối đo giá trị), thiếu object⇒12 chứ không absent0. **Hệ quả:** có thể cần chuẩn bị fetch trước chụp; số lời gọi và thời gian fetch đó đo riêng, không giấu dưới “1ls-remote”.

### S9 — reroute-accounting-is-stale · P3 · mới

§0/Q14 còn6/6, §ngoai_pham_vi và hình dạng còn `blocked/ADR trước/không vá thêm`. Reroute `5578460203` thắng cho review này; đếm7, giữ ID. Sửa đồng bộ ở r7 theo điều phối, không coi là P1 hay dành probe cho nó. Câu r5 “tận cùng” chỉ nên là lời khai lịch sử đã bị review bác, không là chứng minh hiện tại.

## Phản chứng đã chạy lại + mới

Các harness đều mới, không loader/tái dùng scratch các lượt cũ. Những lệnh dưới chạy từ cwd với `PYTHONDONTWRITEBYTECODE=1`; subprocess native dùng TMPDIR dưới cwd. Git refs/commits/pack/alternates/shallow/partial/symlink/mode chỉ là fixture thông thường; các commit mới **không** nằm trong kho review.

| Harness/lệnh | Kết quả chính | Phạm vi |
|---|---|---|
| `python3 scratch/luot6/measure.py` | scan1204 object/4.350.922B; closure2658 commit; witness9 | Bytes object thật băm lại, parent/tree parser viết mới; counts snapshot hiện tại |
| `python3 scratch/luot6/controls.py` | routing0/0/0 vs12/12/12; Git rc0 cả hai; absence có tree proof; pack/shared0; shallow ancestry12 | Object-store và graph thật; metadata/profile/receipt là model phân lớp |
| `python3 scratch/luot6/more_controls.py` | profile digest khớp hằng0;3 pair/4 ref,1 pair/3 ref; cha2 giữ0/mất8; closure11/0/11/12/[]8 | Git+model; sửa phạm vi numstat về merge-base→PR head |
| `python3 scratch/luot6/admission_controls.py` | env rỗng + bare main/master discovery0; map stale12; ref đổi sau capture vẫn pinned H; mode8/8/0, full-validator12 | Control hợp lệ, không symref giả/đổi authority |
| `python3 scratch/luot6/partial_and_symlink.py` | partial clone commit/tree0/blobmissing12→materialize thật→0; cùng leaseblob hai đích, hợp3 path | File transport nội bộ; không Internet; symlink không thoát cây |
| `python3 scratch/luot6/native.py` + `native_followup.py` | bốn path wp461 đều holder 2/rc11; check g2 byte-match từ ref0; command mới chưa tồn tại2; doc-claims0/ok:true; doctrine8 file/0 | Mã base thật trong bản sao; không có implementation r6 |

Harness refinement được ghi trung thực: `more_controls.py` lần đầu rc1 do pattern `for-each-ref` của harness không khớp tên prefix; sửa pattern thường thành `card-*`, chạy lại rc0. Đây là lỗi harness, không nhận làm mutant kill. Numstat hai tip phân kỳ ban đầu đo sai đơn vị PR, giữ ở trường `numstats_initial_tip_comparison_not_pr_diff`; số kết luận dùng merge-base→head đã sửa. Native lượt đầu chọn thêm3 path không thuộc wp461 và g2 chưa có trên cây base⇒2; sau đọc lease, chạy đúng3 path còn lại và materialize **bytes g2 nguyên từ ref** trong bản sao⇒0. Không dùng các kết quả đầu làm chứng cứ “bốn path wp461”.

**CHỈ MÔ TẢ, not_run:** fake remote helper, `remote.<x>.vcs`, URL rewrite sang nguồn khác, replacement/graft, env/executable đổi nguồn, bytes cache lệch OID, helper/runtime/CA giả, đường thoát cây, đồng tự Unicode/chuỗi thoát. Không tạo payload, không chạy script cũ có thể chứa các hướng ấy. Ca băm mismatch và negative production profile thuộc điều phối; model boolean seam không là probe tấn công.

**Không nhận công:** C/F chưa là code r6; không có live GitHub/API/auth/TLS; full lease/packet-loop suites và81 mutant không chạy lại vì có ca ngoài phân công. Không lấy banner model0, số case giả, hoặc legacy test pass thay A1–A12.

## Tiêu chí A1–A12

| Tiêu chí | Đơn vị / phép đỏ | Kết luận r6 và phép đo mới |
|---|---|---|
| A1 | Dòng theo(blob,path), holder theo ID, MAP_REF theo occurrence; known-list mutant bỏ blob thứ3 | F:3 pair/4 ref, ngoài known1, model đúng3 dòng vs2; có phép đỏ. Smoke∅/{g2} theo clock, không hứa land giết lease. |
| A2 |1 pair/3 ref; endpoint/default/name+OID/profile | F cardinality; G main/master/discovery/pinning0; nguồn sai chỉ MÔ TẢ. Profile còn S1, không nhận production xanh. |
| A3 | Năm mã r3=8/0/8/0/8; hai cây mốc; inactive product vs DU_BAO | Đã đọc r3 đúnghash. Mốc và flag có phép đỏ đúng; không chạy lại5 case/suite sản phẩm. Current master đổi lịch sử được ghi ở bảng đo, không chọn nó làm mốc A0 chưa có. |
| A4 | Reverse ledger/history, có/không thay_thế; live0 | Hợp đồng đủ phân biệt bỏ từng nguồn; lượt này chỉ đối chiếu hợp đồng, không N/N sản phẩm. |
| A5 |Closure/exact/prefix/case-fold/alias perOID; claims[]8, clash11, unknown12; pure vs published exact pair | F ba nhánh xanh theo model; P alias đa occurrence. **Ca policy qua reader tích hợp không thể xanh cho tới S7**; fixture phải có metadata hợp lệ. Không dựng vòng/thoát/Unicode. |
| A6 |Map/ref/bytes/type/graph/routing/profile/cost; mỗi seam một oracle | S2 đã sửa raw graph. **S3 còn lời hứa kill không thể đỏ**; C phân biệt sống12/12 với kill0/12. No-replace mutants sống đúng; byte mismatch chỉ mô tả. S8 trần chưa có đơn vị/default. Benchmark component không phải ratio E2E. |
| A7 |Mỗi constraint M1 một field lỗi; source12/content8/account4; qua consumer | M1 r3 đọc đủ; source missing12 đã chạy. **Reserved retired chưa có schema⇒S7**, không thể gọi whole-namespace validator xanh. Không chạy toàn matrix API/consumer. |
| A8 |Map(path,mode,type,blob), toànT; ancestor/merge; strict S/H/T | F cha2 giữ0/mất8; G mode đúng8, only-new8 sống, combined0 bị bắt, full-T12. Đột biến chọn đúng. Cần thêm metadata tuple/schema và bỏ self-T. |
| A9 |Stateful API endpoint/ID/calls; trước canonical recheck, sau0 thêm | Q2/A9 rõ; artifact hết hạn sau land không được gỡ event. Lượt này không mô phỏng/chạy lại cả matrix comment API; số0 lời gọi là hợp đồng, chưa thực chứng sản phẩm. |
| A10 |5entrypoint×4trạng thái, candidateID, bytes state,1event/idempotence; REST không là nguồn guard | AST nền1/1/0/0/0 đo lại. Hợp đồng đủ phép đỏ đúng từng cửa.35 case/40 call cũ không nhận mới; ma trận chưa chạy lượt6. |
| A11 |Exact head/base, actual workflow/job/step, N/N+delta; no skipped/missing/wrong SHA | Doc/doctrine mới0;121/121, 278/278,81 mutant **not_run mới**. Raw Actions canary cần S5; dependency không tự làm A1 bất khả thi nhưng phải vào thứ tự bootstrap. |
| A12 |Catalog độc lập expected/registered/executed/passed/failed/skipped/not_run; credit đúng seam | F expected catalog bất biến bắt thiếu invocation và xoá cảregistration+invocation; ca model nhỏ không là catalog sản phẩm. S3 phải sửa trước credit mutant. |

### Nhất quán luật và slice

| Luật | Đối chiếu |
|---|---|
| §3.2 / ADR-0025 | Không có Issue/lease⇒chưa thi công; thay dependency/profile/schema metadata phải vào revision/spec_hash trước ready. Q13 không miễn ngầm phái sinh của packet khác. S6 binding cần rõ. |
| §4 / ADR-0028 | Q5/Q11 giữ stale/generation/stop/readback/retention; không nhận snapshot như fencing. Artifact receipt có hạn cần life cycle/journal S5; metadata canonical là event khác, không thay state journal mission. |
| §5 | Closure+symlink mọi occurrence; Q13 ngoại lệ được user cho nhận; policy đổi cần pause/re-evaluate/revision/generation. S7 không thể cài policy vào hợp đồng hiện tại; sửa schema có phạm vi. |
| §8 / CLAUDE.md | Review read-only, exact hash, hai trục spec/standards, đối chiếu từng ID và behavior thật; không nhận mutant chết vì chốt khác. S3 còn vi phạm tiêu chuẩn bằng chứng dương. Hint chỉ chữ spec, không hunk runtime authority. |
| §12 | Call 7 có reroute bền được user cung cấp. Giữ lịch sử5lần hình dạng nguồn; S1 còn vấn đề thật cần quyết định ADR, không tự chặn review chỉ vì ADR vắng. S9 P3. |
| ADR-0044 | A0=3 path,+560–780;A1=3,+90–160;B=2,+160–240;C=1,~15; tổng825–1195/6 path duy nhất. A0 vượt300 có lý do phạm vi, Q7 còn cần chốt; số mốc409/368/328 đo đúng. Schema metadata+reader+profile có thể tăng ước, không bịa numstat tương lai. |

Mỗi slice cần Issue/spec/lease/acceptance/base đã nhận predecessor; A0 không phải Stable Slice nếu còn S1/S3/S7 cắt ngang gate. `LAND-DOC-RECEIPT-THU-HOI` là packet riêng, không tính path của nó như đã nằm trong6 path hiện tại. M9 đòi mã canonical, nên predecessor chỉ integrated trên nhánh khác chưa đủ cho bootstrap. Q4.1/Q4.5 là hạt ADR có thể dùng được; phần đã kín là verified-object graph, phần vẫn mở là trust nền thực thi/profile governance và giới hạn/khả năng vận hành. Không tuyên bố “bytes đã băm ⇒ mọi nguồn đều đã tin cậy”.

### Q7–Q14

| Câu | Đã bắt buộc/đã chốt | Còn thiếu trước bước tương ứng |
|---|---|---|
| Q7 |A0→A1→B→C, từng slice riêng; A0 cóworkflow; không dùng PR chồng lấn để né300 | Chốt ngoại lệ dòng/A0 audit; chèn dependency consumer trước bootstrap; đo lại ước có schema/profile. |
| Q8 |C thu hồi r2 **không đích**; g3 là opsPR khác | Object lệnh chủ kho đúng Q2 chưa có trong bundle; không thể cấp từ lời khai review. |
| Q9 |Khuyến nghị nhận thu hồi lease hết hạn; event không biến mất, không tái dùngID | Quyết định chủ kho chưa được giao. Không tự đổi C chỉ vì lease sẽ hết hạn trước triển khai. |
| Q10 |Thiếufacts⇒False; exact S/H/T, strict/update/bypass/queue, delta, closureQ13, revocation-set rỗng | Profile thật/image/CA/proxy; Actions canary + join/attempt/artifact; consumer landed; ruleset và audit; S5/S7/S8 sửa contract. |
| Q11 |C→dừng worker/giữ SHA/state→g3 check+land+readback1→start | Facts C/stop/g3 thực; reviewer không thực hiện land hoặc fencing ngoài write set. |
| Q12 |Issue/revision/generation/spec_hash/phái sinh/base đã nhận predecessor; closure descriptor union | Hợp đồng còn S1/S3/S5/S6/S7/S8 và các giá trị profile/budget/binding được đóng băng; thiếucontract⇒proposed. |
| Q13 |**ĐÃ CHỐT(ii)** comment5575587924; raw+symlink tới policy đầu tiên, không EWS tự khai | Bodyhash thật, activation context; metadata schema/first-policy transitions; xử pre-guard policy. Không hỏi lại chọn(i)/(ii). |
| Q14 |**ĐÃ REROUTE** comment5578460203, review tới hếtP1, khôngreset, call 7 | Sửa chữ6/6 ởr7 và ledger điều phối; không yêu cầu thêm permission cho lượt này. |

## Bảng đo lại

Map mới ở `scratch/luot6/refs.json`; không có manifest map 303 ref của lượt5. Số lịch sử và số snapshot mới được tách. Clock quá khứ là phân loại lại **dữ liệu hiện có**, không phải quan sát GitHub tại giờ ấy. Không thấy một con số sai đang được dùng để tự cấp thẩm quyền; thay đổi ref/master dưới đây không tự là P1.

| Đại lượng | Đo lượt6 | Đối chiếu/giới hạn |
|---|---|---|
| SPEC.md / bản untracked mirror |f78135cff428f0744476d7f27426f459d926578c4bac4a4339928330c4a0d6a5 |Khớp bản giao; anchored content ở commit2aee80a2ff6a088ff39a2a8bc882db978df64c75 |
| R5 / verdict5 / hint5 / verdict4b |23a7deaf… /1596d562… /8ca8474b… /7d3017ec… |Fullhash kiểm đầu lượt, khớp |
| R3 khôi phục |ef9b3700514921d4cabe95947f86937fc36f4aecf2f4e2e39587cafe88a9bb20 |Git3c0cf9106974d326bc9643acd81e2db8fbd73943; đã đọc trực tiếp M1/A7/A8 |
| HEAD/tree/core.abbrev |b416830… /266a2aba97d925dac3ab7473dda55adb0fe23b8e /7 |Detached; codebase không trôi |
| origin/master |585c7d510e026b4ea5a2b395c69581f24c1d8fa0; **48 commit sau base** |Tree6939cb7ce3d4c80f4fe3120de4da4e27a214005e; code lease/loop/workflow CI/protocol/CLAUDE/policy không diff so base, dữ liệu/ops đã đổi |
| Ref công thức spec |**310=309remote+1local;306unique tip** |Cũ303/299tips là snapshot khác; local giờ là nhánh spec, không master |
| Cặp/path/leaseID/multi-blob-ID |**288/273/273/7** |Khớp số cũ dù ref tăng |
| Live/chưa tomb, clock13:41Z07-09 |**8/4** |Phân loại lại từ M, khớp |
| Live/chưa tomb,14:33:15Z07-09 |**7/3** |Khớp; #456 hết14:30:07 |
| Live/chưa tomb,03:12:57Z08-09 |**6/3** |r1wp461 hết03:05; không lấy số7 cũ làm hiện tại |
| Tại03:37:33 /09:52 /10:17:12Z08-09 |**5/3;1/1;0/0** |Clock fixture; không là nghiệm thu smoke sauC |
| Hạn wp461 r1/r2/g2 |03:05:00 /05:27:42 /09:52:00Z08-09 |Khớp |
| Hạn gate r1/r2/r3/r4 |03:37:33 /07:50:35 /09:44:51 /10:17:12Z08-09 |Khớp; gate cuối sau g2 25phút12 giây |
| r2 blob26f07b4 /fdfde3a |**9 ref /1 ref** |Cũ4/1; map mới có nhánh spec và các nhánh land. Chi tiết M.special_blobs |
| #456 blob8b2103c /1f95042 |**14 ref /5 ref** |Cũ11/1; không quy thay ref thành lỗi thẩm quyền |
| Tomb tại base / H02b0b86 /master 585c7d5 |**7 /11 /11** |R6 câu “master 7” đúng nếu hiểu snapshot b416830; sai nếu gọi đó là master hiện tại. #468 đã vào master ở802fc01b5db866478459dbc4a65d008a38619898 |
| Divergence base…H02b0b86 |**0 trái/31 phải** |Khớp31; không đồng nghĩa ancestry cần đọc31 commit |
| Raw signatures b416830 /6635379 |Mỗi commit **1 gpgsig**, PGP/SSH |Không chạy keyring/chứng thực signer; không suy author.login/actorAPI |
| planned: lease |**3 ID**, đều hết hạn |plat-x4-exec-1,plat-x5-exec-1,plat-x5-exec-1r2 |
| kiem→_lease_cham_duong / guard schema5 cửa |**0 /1,1,0,0,0** |AST base; không phải guard mới đã cài |
| _kiem_bia_mo dùng any / tomb hai chiều ở base |**1 lời gọi any; 7/7 cặp hai chiều đúng** |Đo mới bằng AST và bytes YAML ở đúng cây b416830; `final-checks.json` |
| Nhánh spec so với master hiện tại |**48 commit bên master /9 commit bên spec** |Khớp bàn giao; không dùng số9 này thay witness ancestry9 ở phép đo khác |
| CI/wrapper nền |checkout fetch-depth 0; packet_loop_test dòng 133; wrapper lease dòng 206; ops-publish chỉ paths ops/leases yaml/yml |Đọc lại tại base; không chạy installer actionlint qua mạng |
| Policy/schema/sổ/workflow mới |Đều **vắng** tại base vàmaster 585c7d5 |Kiểm cảschema đúng coordination path; không nhận current master đã triển khai r6 |
| Native4 pathwp461/checkg2 |Cả 4 **holder 2,rc11**;checkg2 **rc0** |N/N2 bản sao; checkg2 từ bytes đúng ref, không có API readback |
| commandkiem-thu-hoi-github nền |**rc2** |Chưa có command; không thể nghiệm thu r6 như code đã tồn tại |
| Doc claims strict |**rc0,ok:true,70.861stdoutB** |N, cùngbase/core.abbrev=7; không phải không advisory |
| Doctrine cóspec |**rc0,8 tệp,0chỗ chép** |N2; lượt không--path chỉ7 tệp, không trộn hai mẫu số |
| NumstatPR250/275/248 |**+409/−0;+368/−0;+328/−1** |F exactmergebase/head và per-file;250 là2SPEC, không code |
| ƯớcA0/A1/B/C |560–780/90–160/160–240/~15; tổng**825–1195** |Đúng phép cộng, chưa có implementation để xác nhận số dòng |
| Scan lease + absence tại frozenbase |**1204 object=307 commit+609 tree+288 blob;4.350.922B;2,41036s** |306tips mới + extra base; số tối thiểu, chưa toàn bộ symlink/policy workflow closures. Cũ1186/4.311.029B không tái lập exact vì thiếu map cũ |
| AncestryS→H02b0b86 |Witness **9 commit/8cạnh**, visited9 với DFS parent-cuối-trước |Full S/H/witness trongM. Cũ1815visited phụ thuộc thứ tự traversal, không phải bound; witness9 khớp |
| Full raw-parent closure map hiện tại |**2658 commit;3555 object cộngscan;8.883.868B** |Cũ2622 commit không phải số hiện tại; không có mapcũ để kiểm2622exact |
| Componentbenchmark3 cặp |Median khôngbăm0,069960s;cóbăm0,057999s;ratio0,829032 |1204 object/4.350.922B,1cat-file/lượt; raw6 lượt trongM. Nhiễu/cache; không kết luận băm tăng tốc, không phải A6E2E≤2 |
| Nativebareorigin của bundle |HEADsymref=nhánh spec; advertisement không córefs/heads/master ở probe |Bare đóng gói này không phải serverGitHub309heads; không dùng nó chứng nhận MAP_REFtươi. G mới dựng serverfixture riêng cómain/master chocontrol |
| Full suites/API/receipt production |**chua_do_duoc /not_run** |Không chép121/121, 278/278+81 hoặccheck101767296495 thành số chạy mới |

## chua_do_duoc

1. Implementation r6 chưa tồn tại: không có full M1×consumer, A1–A12 N/N, catalog mutant sản phẩm, delta suite base/candidate hay benchmark E2E≤2. Số native là base; số model là model.
2. Không chạy probe bị cấm, kể cả từ script/bundle cũ. Không có ca bytes lệch OID hoặc replacement thực trong scratch. Full suites nền 121/121, 278/278+81 mutant chỉ là lịch sử; không đọc binary/CA/secret ngoài cwd để chứng nhận profile.
3. Raw GitHub check/run/job/artifact/attempt/permissions, association pull_request_target, actual workflow_sha, retention và publisher/consumer thật; body hash/actor của comment 5575587924/5578460203 chưa tự readback. User cấp authority cho reroute review và lựa chọn Q13; không suy authority triển khai.
4. Profile production, Git/helper/runtime/image/trust-store manifest, proxy host/port/scheme, CA riêng và quyền người duyệt. Không nói remote container chắc chắn chạy được từ control file:// hoặc dữ liệu identity fixture.
5. Chính xác 1186 object/4.311.029 B, 2622 commit trên **map cũ**; map 303 ref và raw logs của scratch lượt 5 không còn. Đã đo map mới 1204/4.350.922 B/2658, witness S/H dài 9 commit có thể tái lập. Không kết luận con số cũ gian/sai chỉ vì snapshot mới khác.
6. Facts rollout: Packet Issue/lease từng slice, marker/mốc A0 sau canonical, producer phái sinh, bootstrap audit/freeze/readback, required checks/rulesets/bypass/direct push/queue, consumer dependency đã land, Q8 event, worker stop/last SHA/state/g3 độc quyền. Không thực hiện hoặc tự cấp chúng.
7. Ranh giới chủ kho gõ và agent cầm PAT/chữ ký web-flow; dữ liệu Git chỉ chứng minh object/header, không chứng minh người thao tác.

### Kiểm tra hiện vật cuối

`HINT.patch`: **7 hunk**, 48.769 byte; sha256 `47fbf8cba3265a8f4ad285d03f1fe21136a0c7edff01bc5155959501b05fb84c`. Đã chạy `patch --dry-run --batch --fuzz=0 -p0` rồi áp thật **chỉ vào bản sao** `scratch/luot6/patch-check/SPEC.md`, cả hai rc=0; `cmp` với `SPEC.hinted.md` rc=0, sha256 bản sau áp `60d87d515b65bc699681ace65e65e9e1c57c07a552f2d95cb65f7079709a4c6b`.

Hint phủ S1/S3/S5/S6/S7/S8. Nó chọn bỏ dispatch khỏi workflow required, đặt consumer trước cửa sổ bootstrap và thêm schema đúng một path reserved; đó là các thay đổi hợp đồng để executor đưa vào r7, không phải mã đã nghiệm thu. Các giá trị budget mới trong hint là **đề xuất chưa đo đủ trên deployment production**, phải đóng băng và canary theo Q12, không nhận chúng như số đo. Kế toán P3 S9 để điều phối sửa đồng bộ ở r7 như đã giao.

`final-checks.json`: HEAD/tree và map ref không đổi; SPEC đúng hash ban đầu, byte-match bản untracked và commit r6. Status kho review chỉ `?? ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md`. Đủ mọi section bắt buộc; không NUL trong hiện vật. Kết luận nội dung vẫn **changes_requested: P1 S1/S3/S7**, không dùng các mục chưa đo để thêm P1 hay để tuyên bố approve.

Hoàn tất `2026-09-08T04:00:58Z`; elapsed từ mốc user: 2881.4 giây, trong trần 60 phút. Băm các hiện vật đã giao ở `scratch/luot6/ARTIFACTS.sha256`.
