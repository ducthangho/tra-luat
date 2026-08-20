# CONTEXT — Ngôn ngữ chung của dự án tra-luat

Thuật ngữ chuẩn dùng trong SKILL.md, CHANGELOG, commit message và các phiên làm việc.
File này là TỪ ĐIỂN — không chứa chi tiết triển khai. Quyết định kiến trúc ở `docs/adr/`
(cây nguồn dev — r291: KHÔNG nằm trong gói phát hành).

## Điều phối đa phiên

- **Mission Plan** — kế hoạch chuẩn của một mục tiêu lớn, gồm outcome, acceptance, risk, budget và đồ thị Packet.
  Thay đổi material chỉ có hiệu lực qua Mission Change Request được phê duyệt và một revision mới.
- **Packet Spec** — hợp đồng đóng băng của một đơn vị công việc tự đủ: objective, acceptance, write set,
  dependency, executor và environment. Khác **Session Plan**, đây là phạm vi được phép ghi và nghiệm thu.
- **Session Plan** — trình tự chiến thuật của một phiên để hoàn thành đúng một vai trò trên một Packet/review/land.
  Có thể đổi trong phiên nếu không làm đổi Packet Spec; việc ngoài spec trở thành successor Packet và phiên mới.
- **Mission Change Request (MCR)** — yêu cầu có audit để đổi Mission Plan, ghi lý do, tác động, quyết định của
  người có thẩm quyền và revision bị thay thế. MCR không tự có hiệu lực chỉ vì agent đề xuất.
- **Executor** — vai trò duy nhất được ghi vào branch/worktree của generation để thực hiện Packet Spec.
- **Reviewer** — vai trò độc lập, read-only với branch Executor, kiểm Spec và Standards/Security trên exact SHA
  rồi ghi verdict. Cùng provider chỉ được tính là độc lập khi dùng một phiên khác và assurance thấp hơn.
- **Model Reviewer Identity** — danh tính provider/model/session đã thực sự đọc diff và tạo verdict; không suy từ
  tài khoản đăng comment hoặc ghi receipt.
- **GitHub Submitter Identity** — actor vận chuyển verdict/comment/check lên GitHub; không tự chứng minh actor đó
  là model reviewer hoặc có quyền approval độc lập.
- **Review Delivery Receipt** — biên nhận bền neo verdict path/hash, exact reviewed SHA, Model Reviewer
  Identity, GitHub Submitter Identity và cường độ mỏ neo. Receipt v1 là lịch sử read-only; chỉ v2 đã
  validate mới đủ cho identity gate mới. _Tránh dùng:_ receipt là required check, submitter là reviewer.
- **Wall Deadline / Working-state Evidence** — deadline bắt buộc tính theo absolute wall clock; working-state
  time chỉ là bằng chứng phân biệt process chậm với máy ngủ, không thay deadline và không tự void attempt.
- **Review Class** — mức assurance/reviewer tối thiểu của một Packet sau khi đối chiếu khai báo với phạm vi thay
  đổi thật: `routine`, `systemic` hoặc `sensitive`. Mức không biết được xử lý như `sensitive`.
- **Thin Orchestration** — lớp điều phối tối thiểu tái dùng launcher, packet loop, ba skill và GitHub Issue/PR;
  chỉ tự động hóa kiểm tra/state transition tất định, còn quyết định tách, đổi thiết kế, land và cấp quyền chặn
  thuộc human cho tới khi đủ bằng chứng promote. _Tránh dùng:_ orchestrator mới, autopilot.
- **Review Rescue Checkpoint** — điểm quyết định bắt buộc khi một PR đã hết review budget hoặc chưa hội tụ sau
  ba vòng code/review; kết quả là tách phần độc lập, revision kế hoạch, fallback đúng assurance hoặc pause.
- **Stable Slice** — phần thay đổi hữu ích độc lập, đạt acceptance/evidence riêng và không phụ thuộc phần đang có
  finding; chỉ được tích hợp qua Packet/PR sạch và review trên exact head của chính nó.
- **Remediation Slice** — phần chưa hội tụ được tách khỏi Stable Slice thành successor Packet/PR, giữ finding IDs
  và lịch sử để sửa hoặc thiết kế lại. _Tránh dùng:_ phần thừa, phần để sau.
- **Approver** — người có thẩm quyền chấp nhận exact SHA và điều kiện land; output của agent không tự tạo quyền này.
- **Land Operator** — người hoặc agent chỉ thực hiện thao tác land đã được Approver ủy quyền bền và có điều kiện.
  Executor có thể kiêm Land Operator nhưng không nhờ đó trở thành Reviewer hay Approver của code mình.
- **Merged** — một PR đã được hợp nhất vào nhánh đích của chính PR đó; chưa khẳng định kết quả đã vào canonical.
- **Integrated** — Packet đã được merge tuần tự vào mission integration branch sau worker gate và review.
- **Landed** — kết quả đã xuất hiện trên canonical ở exact SHA được duyệt, hậu-merge gate xanh và bookkeeping xong.
- **Mission complete** — mọi Packet cần thiết đã landed, final acceptance/readback đạt và không còn lease/công việc mở.
- **Bằng chứng chạy được** — dữ liệu reviewer kèm theo finding: cặp neo/thay đột biến nguyên văn, phác thảo ca test,
  script đo A/B — đã chạy trong sandbox/cây riêng của reviewer, ghi kết quả chạy kèm theo. Là DỮ LIỆU trong verdict,
  không phải commit, không mang quyền ghi; Executor tái dẫn xuất trên cây thật rồi tự đo. _Tránh dùng:_ bản vá hộ.
- **Patch-as-hint** — patch reviewer sinh từ cây riêng, đính dạng artifact (comment/tệp) kèm nhãn "chưa chạy trên
  cây thật"; Executor tự áp, tự đo, tự chịu trách nhiệm commit — cấm `git am` mù, cấm push ref vào kho.
- **hint_provenance** — trường TUỲ CHỌN trong handoff Executor: khai hunk nào bắt nguồn từ hint của reviewer nào
  và xác nhận đã tái dẫn xuất. Đã dùng hint mà thiếu khai là vi phạm quy trình; không dùng hint thì được vắng.
- **Treo theo review** — chế độ lease khi packet ở `reviewing`: đồng hồ thu-hồi-30-phút tạm dừng, tối đa tới trần
  `review_sla`; quá trần chưa có verdict thì lease trở lại đồng hồ thường.
- **Phiên ấm / phục-hồi-nguội** — phiên executor giữ context sống chờ verdict (tối ưu hoá, không phải quyền) đối lại
  đường dựng phiên mới từ handoff. Đường nguội luôn phải đủ sống một mình; phiên ấm thức dậy phải đo lại trước khi làm.

## Bản thể & phát hành

- **Canonical** — cây git chính thức duy nhất tại `D:\Quốc hội\tra-luat` (remote `github.com/ducthangho/tra-luat`).
  Chỉ canonical được đánh số VERSION và publish. Số version không phát từ canonical là không hợp lệ.
- **Nhánh song song** — phiên làm việc khác (Cowork/Chat/Codex…) sửa skill trên bản copy. Sản phẩm hợp lệ duy nhất
  của nhánh song song là **bundle** (không phải version mới, không phải publish). Xem ADR-0001.
- **Bundle** — zip giao nộp từ nhánh song song: giữ nguyên VERSION fork-point, kèm `BUNDLE_META.json`
  (commit gốc, danh sách file đổi, test thêm). Canonical merge bundle rồi mới đánh số.
- **LIVE (Package)** — file zip trên Drive Package (fileId cố định) mà Cowork/Chat thực tải qua `tl_fetch.sh`.
  LIVE có thể TRỄ so canonical (drift) — kết luận "skill có lỗi X" phải nói rõ đo trên LIVE hay canonical.
- **Deploy** — `tl drive-push` đưa zip canonical lên LIVE, giữ fileId. Luật vận hành: **xanh là deploy ngay**
  (gate xanh ⇒ push cùng ngày + verify tải lại VERSION; SKILL.md đổi ⇒ nhắc user re-import Capabilities).
- **Re-import** — user nạp lại zip vào Cowork Settings→Capabilities; bắt buộc khi SKILL.md đổi, vì agent đọc
  bản import chứ không phải bản Drive.

## Chất lượng & gate

- **Gate xanh** — đủ bộ: `--selftest` + `workflow-audit --strict` + `golden-test` + `determinism-audit --strict`
  + `gen_instructions --selftest` + `release-bundle` ×2 cùng SHA-256 + `release-verify` trong gói giải nén.
- **Ingest thành công** — mọi hậu điều bắt buộc của phạm vi đã chọn đều được đọc lại và xác nhận đúng. Kết quả
  thiếu, mơ hồ hoặc chỉ hoàn tất một phần là ingest thất bại có thể nối tiếp; ngoại lệ chủ ý dừng trước NLM chỉ
  thành công khi phần Drive/registry đã được xác nhận và tài liệu chưa được nhận là corpus. Ngoại lệ duy nhất
  của vế corpus (ADR-0015): tài liệu đã qua **verify parity** thì corpus được flip dù NLM còn nợ —
  nợ NLM theo dõi riêng bằng `nlm_status`.
- **Kế hoạch ingest** — bản mô tả bất biến của một lần ingest, ràng buộc byte nguồn, đích, tên canonical và toàn
  bộ tùy chọn bằng một dấu vân tay. Apply chỉ là quyền thực thi đúng kế hoạch đã xác nhận; nguồn hoặc cấu hình
  thay đổi thì phải lập và xác nhận kế hoạch mới. Resume có thể dùng kế hoạch đã ghi trong journal nhưng vẫn phải
  kiểm tra lại dấu vân tay trước khi tiếp tục.
- **Kết quả tất định** — cùng dữ liệu và cấu hình tạo ra cùng nội dung nghiệp vụ, không sửa giá trị để che khác
  biệt. Canonical hóa chỉ áp dụng cho cấu trúc và các trường có kiểu được khai báo; biến động hợp lệ phải được
  schema từng lệnh chỉ rõ và chỉ bị loại trong bản chiếu audit. Khác biệt thô không được khai báo là lỗi.
- **Ingest engine** — bộ điều phối dùng chung cho mọi đường ingest, sở hữu state machine, kế hoạch, journal,
  identity, idempotency và hậu điều; adapter chỉ thực hiện I/O với Drive, registry, NLM hoặc cache. Engine phải
  tránh đọc lại trùng lặp, hỗ trợ batch có thứ tự kết quả tất định và được kiểm soát bằng ngân sách hiệu năng.
- **Ngân sách hiệu năng ingest** — giới hạn có thể kiểm thử cho số lần đọc nguồn, số API call, concurrency và
  thời gian chạy. Hash nguồn một lần mỗi run; mỗi resource tối đa một write và một readback bắt buộc cho mỗi
  giai đoạn thành công; benchmark local không được chậm hơn baseline quá 15% ở median. Không được bỏ hậu điều
  an toàn để đạt ngân sách.
- **Source policy** — quyền quyết định nguồn/host/scheme nào được phép, do môi trường chạy cung cấp qua policy
  hoặc fetch adapter; skill không hard-code danh sách domain. Ingest engine luôn giữ các bất biến độc lập với
  host: giới hạn tài nguyên, streaming, xác minh loại và hash, không rò credential, dọn tệp tạm và audit provider.
- **Identity ingest** — tổ hợp `content_hash + target scope + canonical name + profile` dùng cho idempotency,
  deduplicate và resume. Tên file đơn lẻ không phải identity; cùng identity là no-op đã xác minh, còn cùng tên
  nhưng khác hash là conflict và chỉ được thay thế bằng một kế hoạch chỉ rõ source ID cũ.
- **Ba van NLM (r192)** — ba chốt điều tiết đường nạp NLM, con số chốt qua grilling 23-07: **van trước lô**
  (lô >4 nguồn → không auto-add API, xuất BẢNG TAY markdown + hẹn reconcile), **van kích thước** (nguồn
  >150k ký tự → tự `--nlm-no-wait`), **van runtime** (chờ settle quá 120s → thôi chờ KHÔNG huỷ, ghi
  deferred, chạy tiếp; cuối lô một lượt reconcile). Đường "nạp tay" chỉ kích hoạt ở van 1 hoặc khi NLM
  chết hẳn.
- **Bảng tay (nạp NLM)** — file markdown do van 1 sinh (`hand_sheet`): link bấm-được từng nguồn + link
  notebook đích + hẹn `nlm-reconcile --apply` sau khi người dùng nạp xong trên UI. Lô >4 nguồn chia
  **khối ≤4 URL** (r199): mỗi khối tự đủ (link notebook tại header), nạp từng khối và chờ NLM nhận
  xong khối trước — sự cố NLM khoanh vùng theo khối, không mất cả lô. Sinh bằng
  `tl nlm-links --drive-ids … --md-out …` hoặc tự động ở nhánh bảng-tay của `ingest-missing`.
- **PDF_IMAGE** — verdict đo text-layer PDF lúc lập plan ingest (r191): trung bình **< 100 ký tự
  không-trắng/trang** ⇒ PDF scan/ảnh (text layer chỉ còn metadata chữ ký số) → coi
  `source_quality=ocr` chưa verify, rơi vào ocr_gate hiện hành — KHÔNG convert mù. Không đo được
  (thiếu pdftotext) → `unknown`, cảnh báo chứ không đoán.
- **Manifest bẩn (marker)** — trạng thái sau một lệnh GHI registry (r191): cache manifest local bị xoá
  + để lại `manifest.dirty`; lệnh ĐỌC resolve-theo-số-hiệu kế tiếp PHẢI tự refresh LIVE rồi xoá marker
  (fail-closed nếu không fetch được). Đường đọc advisory (discovery) không bị ép.
- **Cache staged / verified** — `staged` là dữ liệu đã thu nhận nhưng chưa đạt đủ schema, provenance và quality
  gate; `verified` chỉ được đặt sau khi mọi gate này đọc lại thành công. Fallback hoặc candidate được suy đoán
  không bao giờ được tự nâng thành verified.
- **Staged ingest (lane trì hoãn, ADR-0015)** — đường `profile-ingest --staged` cho docx digital: GIỮ đủ cổng
  AN TOÀN lúc nạp (dedup tên/số hiệu LIVE, claim xuyên host, convert-readback), HOÃN cổng CHẤT LƯỢNG (đọc
  toàn văn canonical, verify_gate, quét Điều/chunk) và NLM. Dòng vào registry `corpus=false` +
  note `staged:pending;sq=…`; TỪ CHỐI pdf/ocr/bảng tính. Hoãn ≠ bỏ — ADR-0004 giữ nguyên.
- **Verify parity** — nguyên tắc của `verify-staged`: chạy ĐÚNG bộ cổng lane thường đã hoãn, không hơn không
  kém — lane staged đổi THỜI ĐIỂM kiểm, không đổi TIÊU CHUẨN. PASS → bulk-flip `corpus=true` cả lô (journal,
  undo được); FAIL → ở lại staged (note `staged:fail:<FLAG>`), không auto-xóa, không NLM.
- **ZIP portable-safe** — profile archive dùng path Unicode NFC với dấu `/`, từ chối traversal, special entry,
  tên không portable và mọi collision sau canonical hóa kể cả khác hoa thường. Kế hoạch ZIP ràng buộc hash toàn
  archive cùng `normalized_path + member_hash + size`; giới hạn tài nguyên do môi trường cấu hình và apply luôn
  giải nén vào staging riêng trước khi chuyển từng member qua ingest engine.
- **Reproducible bundle** — gói phát hành có `content_hash` từ manifest canonical và `archive_sha256` từ byte
  ZIP. Exporter dùng ZIP không nén với root, thứ tự, timestamp, permission và metadata cố định để cùng nội dung
  tạo đúng cùng byte trên mọi lần build; mọi hash mismatch luôn là lỗi.
- **Golden** — fixture JSON tất định tại `references/golden/`. Độ chặt đã chốt: PASS/FAIL so bản canonical-hoá,
  cộng check **raw-stability** (stdout thô chạy ×2 phải trùng byte) — không so raw-bytes với fixture.
- **Characterization test** — test đặc tả hành vi hiện có của một cụm lõi cũ, viết TRƯỚC khi tách cụm đó
  khỏi tl.py (điều kiện bắt buộc của lộ trình về đích 2.500 dòng).
- **Grandfather** — nợ-đã-biết ghi ở `registry.warnings` (advisory, không fail strict), có deadline siết.
  Đã chốt: 6 lệnh ghi đụng Drive/NLM/registry-corpus siết ở Pha G; 6 backfill/plan siết pha kế tiếp.
- **Command registry** — `tl_core/command_registry.py`: metadata risk/gate/card/contract của LỆNH CLI;
  nguồn sự thật cho tool-inventory/workflow-audit. KHÁC **registry corpus** (Google Sheet `tra_luat_registry`
  — sổ cái văn bản pháp luật). Nói trần "registry" trong ngữ cảnh vận hành corpus = registry corpus.

## Sổ cái corpus & NLM

- **Draft (ingest)** — văn bản CHƯA BAN HÀNH, xét theo BẬC BẰNG CHỨNG (chốt 2026-07-21): banner «DỰ THẢO»
  hoặc số hiệu rỗng/khuyết là bằng chứng draft mạnh; số hiệu đầy đủ + ngày ban hành là bằng chứng official
  mạnh và PHỦ QUYẾT các marker chữ yếu («lấy ý kiến», «góp ý» — chỉ có nghĩa khi không có bằng chứng ban
  hành). Văn bản góp ý/BC về một dự thảo là văn bản official — đối tượng nó bàn tới không đổi bản chất nó.

- **nlm_status** — trạng thái NLM của một dòng registry corpus. Từ vựng ĐÓNG (chốt 2026-07-21): họ `pushed*`
  (đã đẩy nguồn lên notebook), họ `synced*` (đã đối soát khớp), `active` (xác nhận đang sống trên notebook),
  `deferred` (xem mục riêng), họ `removed_*` (đã gỡ CÓ CHỦ ĐÍCH — hậu tố ghi lý do, vd
  `removed_superseded_by_VBHN`), hoặc RỖNG (chưa từng đụng NLM). Giá trị ngoài họ là dữ liệu lỗi: cửa ghi
  từ chối, audit gắn cờ. `added`/`live` là từ cũ đã nắn về `pushed`/`active` — không phải trạng thái hợp lệ.
- **deferred (nlm_status)** — ngữ nghĩa MỞ RỘNG (r191, 2026-07-23): «việc đưa nguồn lên NLM đang TREO
  XÁC MINH» — gồm CẢ hai ca (a) NLM chết, chưa gửi (defer v1.34.60 — dòng không có nlm_source_id) và
  (b) ĐÃ GỬI qua `--no-wait`, có source_id thật nhưng CHƯA xác minh settle. deferred KHÔNG claim có mặt
  vật lý (không thuộc nlm_claim) nên không vi phạm VERIFY-THEN-LINK; corpus KHÔNG auto-true khi còn
  deferred. `nlm-reconcile` thấy sid có mặt live đúng notebook → nâng `deferred→pushed` (settle_confirm,
  chỉ cột nlm_status).
- **Thay bản (`--replace-sohieu`)** — thoát CÓ CHỦ ĐÍCH khỏi cổng dedup số hiệu LIVE của `ingest-local`
  (r191): nạp bản MỚI cùng số hiệu (khoá lỏng-năm) khi corpus đã có dòng effective — plan in dòng cũ +
  chuỗi hạ bản sau nạp; mặc định KHÔNG cờ là CHẶN rc=2. KHÁC «nạp trùng do cache nguội» (bug đã vá F1).
- **Scope (dòng kết quả)** — nguồn gốc của MỘT dòng trong kết quả lệnh đọc: dòng profile (mặc định, không
  đánh dấu) hay dòng NỀN VBQPPL kéo vào qua base-also — dòng nền mang `scope: vbqppl` + cờ `BASE_SCOPE_HIT`,
  MỘT cách mã hoá duy nhất ở mọi lệnh đọc (chốt 2026-07-21; khe `_scope`/`scope` hai kiểu là sự cố đã vá).
  Đếm/lọc "của profile" phải loại dòng nền bằng đúng hai dấu này.
- **nlm_claim** — điều SỔ CÁI KHẲNG ĐỊNH đang có mặt trên notebook: dòng có `nlm_status` thuộc họ sống
  (`pushed*`/`synced*`/`active`). Đối chiếu claim ↔ live (đếm vật lý trên NLM) ra **desync** — việc của
  `nlm-reconcile`. KHÁC nlm_due.
- **Hạ ref (demote corpus→ref)** — thao tác MỘT BƯỚC đưa một nguồn ra khỏi diện căn cứ nhưng GIỮ nó
  truy-vấn-được: corpus=false + row_kind=ref, nguồn NLM và nlm_status họ sống GIỮ NGUYÊN (chốt
  2026-07-22, ca ILO C102). KHÁC «bỏ ra khỏi corpus» thường (corpus=false + GỠ nguồn NLM + removed_*).
  Nhất quán [[nlm_due]]: due = corpus ∪ ref nên dòng hạ ref không sinh nhiễu desync/coverage_gap.
- **nlm_due** — diện PHẢI-CÓ-MẶT theo chính sách corpus (dòng corpus ∪ ref). Đối chiếu due ↔ vật lý ra
  **coverage_gap** (nợ phủ) — việc của `slot-audit`. Hai phép đo trả lời hai câu hỏi khác nhau; con số
  lệch nhau giữa chúng KHÔNG phải mâu thuẫn. Cấm dùng trần chữ "claim"/"gap" không kèm định nghĩa
  (chốt 2026-07-21 — sự cố hai lệnh cho số "vênh" 51/40/51).

## Thể thức

- **Đặc tả thể thức** — bản khai duy nhất về trình bày (cỡ/kiểu/canh/thụt + căn cứ) của từng thành phần
  văn bản theo hệ. Builder và bộ kiểm cùng đọc từ đây; giá trị trình bày không được ghi nơi thứ hai. Xem ADR-0009.
- **Bậc thẩm quyền (B1/B2/B3)** — thứ tự phân xử khi các nguồn quy định lệch nhau: **B1** văn bản gốc
  nguyên văn thắng tuyệt đối; **B2** reference có trích § cụ thể thắng code; **B3** quy ước nội bộ — hợp lệ
  nhưng buộc mang nhãn "quy ước", cấm trình bày như căn cứ pháp lý. Mỗi ô đặc tả tự khai bậc của mình.
- **Cách ly (ô đặc tả)** — trạng thái của ô chưa xác minh được căn cứ: không dùng để build/kiểm, chờ đối
  soát văn bản gốc. Khác với **khai trắng** — hệ tuyên bố tường minh là chưa được đặc tả.
- **Biến thể mẫu** — trục thứ ba chồng lên (thành phần × hệ): cùng một hệ nhưng nhóm mẫu khác trình bày
  khác (Mẫu 16 QĐ-CTN quốc hiệu 13; công văn không tên loại, trích yếu «V/v» riêng). Bản khai
  `_tt_dac_ta_bien_the()`: override/thêm/bỏ ô theo nhóm, mỗi mục vẫn mang căn cứ + bậc. Xem ADR-0009 r175.
- **«na» (ô đặc tả)** — giá trị thuộc tính nghĩa «luật KHÔNG ấn định và thực tiễn đa dạng — không kiểm».
  Khác «0» (ấn định là không-thụt) và khác cách ly (cả Ô không dùng được).
- **Lớp đặc tả (TT-DT)** — lớp kiểm của `the-thuc-check` ĐỌC bảng đặc tả (ADR-0009 bước 5, r176):
  phân loại từng đoạn bằng neo văn bản rồi so 4 thuộc tính với ô, finding `TT-DT-<Ô>-<THUỘC_TÍNH>`.
  Chỉ chạy khi nhận diện được khối đầu (Đ3); nhường cờ viết tay các thuộc tính đã có người canh (Đ4);
  mức WARN/INFO theo bậc + độ tin cậy nhận diện, không FAIL (Đ1 — thăng FAIL từng ô do user duyệt
  theo chuẩn zero-oan).

## Profile

- **Profile** — không gian corpus tự chủ (folder Drive + notebook NLM + registry Sheet riêng + manifest JSON riêng,
  own/own), tách khỏi corpus nền vbqppl nhưng ĐỌC cộng nền (base-also).
- **Profile marker** — file tự mô tả của một profile trên Drive (trong `_meta` của folder profile). Là nguồn
  sự thật về TỒN TẠI + ĐỊNH DANH + metadata mô tả của profile (đã chốt 2026-07-10, thay heuristic discover).
- **Config (profile)** — bản materialize cây profile về local + nguồn sự thật về LỰA CHỌN runtime
  (defaultProfile, token, webapp). KHÔNG còn là nguồn sự thật duy nhất về tồn tại profile.
- **profile-sync** — đồng bộ MỘT CHIỀU marker Drive → config. Ghi marker chỉ qua lệnh tl (journaled);
  cấm sync hai chiều.
- **Adopt** — seed vào config một profile ĐÃ có hạ tầng Drive (registry/manifest sẵn). KHÁC **Promote**.
- **Promote (folder→profile)** — biến một folder Drive thường thành profile: dựng phần hạ tầng còn thiếu
  (marker, registry, manifest, notebook) rồi seed registry từ nội dung folder; việc nạp NLM đi đường
  ingest chuẩn, không nạp trọn gói trong lệnh promote.
- **Nguồn nlm-only** — nguồn của profile chỉ tồn tại trên notebook NLM (URL/YouTube/text/nguồn chưa xuất),
  không có file Drive tương ứng; định danh bằng nlm_source_id.
- **Materialize (nguồn)** — xuất nội dung một nguồn nlm-only thành file trong folder profile trên Drive,
  nâng cấp nó thành nguồn thường. Chính sách mặc định (chốt 2026-07-10): **materialize_preferred** —
  ưu tiên materialize mọi nguồn xuất được, chạy bằng lệnh riêng resumable (không trộn vào lệnh adopt);
  nguồn không xuất được (URL/YouTube/text) ở lại nlm-only với materialize_status tường minh — hợp lệ,
  và Instruction phải nói rõ nguồn nào chỉ có trên NLM để Claude không tưởng nhầm đã có file Drive.
- **Nền VBQPPL luôn bật** — mọi profile nghiệp vụ mặc định ĐỌC cộng nền vbqppl (base-also), không phụ
  thuộc khai báo relations; profile không phải "đảo riêng" — luôn có nền pháp lý để đối chiếu.
- **Instruction Block (profile)** — khối instruction generator-sinh từ marker của một profile (tra NLM
  đúng notebook, luật không-bịa, văn phong, quan hệ với vbqppl/profile khác, scope đọc/ghi). MỘT bản
  thống nhất cho mọi môi trường (Chat=Cowork=Code); chỉ rẽ theo TARGET artifact (session | project).
- **profile-load** — hành vi "dùng profile X trong phiên": xuất Instruction Block làm doctrine PHIÊN,
  không ghi config. Khác **profile-use** (đổi defaultProfile — trạng thái máy, cần --apply).

## Kiến trúc skill

- **Kernel (SKILL.md)** — doctrine agent đọc mỗi phiên; đích Pha F: 20-35KB, chỉ bất biến + con trỏ references.
  Quy trình đổi kernel: draft ở tệp nháp CỤC BỘ trong `references/` (tên đang dùng: `SKILL_KERNEL_DRAFT.md`;
  KHÔNG commit — chưa từng có trong lịch sử git) → user duyệt → thay thật → re-import.
- **tl_core** — package module tách từ tl.py (Pha B trở đi); tl.py là CLI facade duy nhất, bên ngoài không
  gọi tl_core trực tiếp. Đích dài hạn: tl.py ≈ 2.500 dòng (facade + parser skeleton + stubs).
- **bind(tl)** — cơ chế copy-globals cấp helper cho module tl_core trong GIAI ĐOẠN DI CƯ; là giàn giáo,
  không phải kiến trúc đích (xem ADR-0002). Module tl_core cấm đọc bare mutable-global của tl.
- **Stub ủy quyền** — hàm trong tl.py chỉ forward sang tl_core (giữ tương thích selftest/parser/tham chiếu chéo).
