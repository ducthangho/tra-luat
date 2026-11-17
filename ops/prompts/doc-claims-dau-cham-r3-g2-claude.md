# Giao việc executor — DOC-CLAIMS-DAU-CHAM r3 g2 (Claude)

Bạn là **executor** Claude (Claude Code, model `claude-fable-5-2`) của packet `DOC-CLAIMS-DAU-CHAM`, revision 3, generation 2,
Packet Issue #1326, lease `doc-claims-dau-cham-r3-g2-claude` (`ops/leases/doc-claims-dau-cham-r3-g2-claude.yaml` trên nhánh
`ops/doc-claims-dau-cham-g2-lease`). Reviewer là Codex do phiên điều phối #1206 gọi sau bạn. Bạn không review, không approve,
không merge. Generation 1 chưa từng thi công (lease rút hạn để nhường `RELEASE_MANIFEST.json`); không có mã g1 để kế thừa.

## Đọc trước

1. `docs/PROTOCOL_DA_PHIEN.md`: §3.2.1, §4, §5, §7, §10.2, §12, §13.
2. `.claude/skills/work-packet/SKILL.md` (adapter Claude: cú pháp và công cụ).
3. Lease: `git fetch origin ops/doc-claims-dau-cham-g2-lease` rồi `git show FETCH_HEAD:ops/leases/doc-claims-dau-cham-r3-g2-claude.yaml`.
4. Đặc tả `ops/specs/DOC-CLAIMS-DAU-CHAM-r3.md`. Tệp KHÔNG nằm trong checkout: `git fetch origin ops/spec-doc-claims-dau-cham`, đọc bằng
   `git show 889d8a7e49b9940d8d20de896b1656a06c809222:ops/specs/DOC-CLAIMS-DAU-CHAM-r3.md`, chép ra thư mục nháp, đo sha256 byte
   thô; phải bằng `0712647206e62eaca32701ddc05dd4aa0930f43174722aa016883d645be84864`. Khác thì dừng. Mục 2 (M1–M4) là việc; mục 5
   (N1–N8) là nghiệm thu; mục 6 là luật dừng.

## Phạm vi

- Checkout của phiên, nhánh `agent/doc-claims-dau-cham-g2-claude` tạo từ base `13bf69f6eb797e859619a2062e7c9577e6a9cc0b`
  (= `origin/master` lúc cấp lease g2). Kiểm `git rev-parse HEAD` bằng base trước khi sửa. Thư mục nháp NGOÀI checkout (scratchpad
  của phiên): vị từ, log, bản sao đột biến, handoff để ở đó.
- Write set đúng bốn tệp: `scripts/tl_core/workflow.py`, `scripts/test_fragments/wp1326_doc_claims_dau_cham.py` (mới),
  `scripts/tl_test_fragments_bundled.py` (chỉ tái sinh, M3), `RELEASE_MANIFEST.json` (chỉ tái sinh, M4). Không sửa tệp nào khác.
- Không chạy `packet_loop.py init`, `begin-attempt` hay lệnh ghi state nào. Không ghi Drive/NLM/registry.
- Đột biến N2 làm trên BẢN SAO TẠM ngoài checkout, không bao giờ sửa tệp thật rồi khôi phục.
- N6 (Windows) KHÔNG phải việc của bạn: phiên điều phối chạy trên máy Windows của chủ kho sau review. Ghi N6 là `chưa đo được`.

## Việc

1. Thi công M1–M4 đúng đặc tả. Giữ idiom chú thích của kho (dẫn #1326, `ADR-0032`, `ADR-0066` ở hằng miễn trừ).
2. Đo N3 và N4 TRƯỚC khi chạy `golden-test` (lệnh ấy sinh thư mục `references/golden/fixtures/`, làm số N3 khác điều kiện
   "checkout sạch"); nếu thư mục đã có thì ghi rõ và đo lại sau khi xác nhận nó là thư mục sinh, không phải tệp tracked. Đặc tả
   đo số đếm trên base r3; base g2 khác (xem `start_from_sha_note` trong lease): lệch thì ghi số mới kèm lý do. Nếu lệch vì
   một cờ `PATH_MISSING` mới trên tài liệu có thật ngoài 9 cặp miễn trừ: DỪNG theo mục 6 (E3), không tự thêm cặp.
3. Chạy N1 (`python scripts/tl.py --selftest`, đủ N/N hai số bằng nhau; ghi dòng fragment `wp1326_doc_claims_dau_cham`), N2
   (D1–D9, mỗi cái ghi TÊN ca lệch đọc từ thông báo FAIL), N5 (từng cổng và phép làm đỏ của nó), N8. Ghi rc thật của từng lệnh.
   `core.abbrev 7` khi chạy gate. Kiểm `release-verify RELEASE_MANIFEST.json --strict --json` (ok=true, expected == checked).
4. Một commit trên nhánh, chỉ bốn tệp. Thông điệp: dòng đầu `DOC-CLAIMS-DAU-CHAM r3 g2: doc-claims-check L1 kiểm đúng
   đường dẫn bắt đầu bằng dấu chấm`; thân nêu Issue #1326 và sha256 đặc tả. Không tên model trong commit; không viết dấu bỏ qua CI.
5. Đẩy nhánh `agent/doc-claims-dau-cham-g2-claude` ĐÚNG MỘT lần (`git push -u origin agent/doc-claims-dau-cham-g2-claude`).
   KHÔNG mở PR (ADR-0060 M5: PR mở sau khi review Codex offline approve). Không push lần hai.
6. Gửi phiên điều phối `session_015GtxrZk6gmfQKo7g4BfMBS` (send_message) một báo cáo: SHA H và tree, base, `git diff --numstat`
   so base, từng lệnh kèm rc và dòng kết luận, bảng ca N2, số đếm N3 (cũ/mới, lý do), những gì không làm hoặc không đo được, và
   mọi chỗ bạn thấy đặc tả có vấn đề.

## Khi nào dừng

- sha256 đặc tả không khớp, hay tiền điều kiện của mục 2 sai trên base: dừng, báo phiên điều phối.
- Một tiêu chí đỏ vì văn bản đặc tả (không phải vì mã của bạn): dừng và báo đề xuất revision (mục 6 đặc tả; E3 nếu mâu thuẫn
  quyết định của chủ kho).
