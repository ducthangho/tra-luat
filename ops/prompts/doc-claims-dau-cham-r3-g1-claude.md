# Giao việc executor — DOC-CLAIMS-DAU-CHAM r3 g1 (Claude)

Bạn là **executor** Claude (Claude Code CLI, model `claude-fable-5-2`) của packet `DOC-CLAIMS-DAU-CHAM`, revision 3, generation 1,
Packet Issue #1326, lease `doc-claims-dau-cham-r3-g1-claude` (`ops/leases/doc-claims-dau-cham-r3-g1-claude.yaml` trên nhánh
`ops/doc-claims-dau-cham-lease`). Reviewer là Codex (phiên mới, sau bạn). Bạn không review, không approve, không merge.

## Đọc trước

1. `docs/PROTOCOL_DA_PHIEN.md`: §3.2.1, §4, §5, §7, §10.2, §12, §13.
2. `.claude/skills/work-packet/SKILL.md` (adapter Claude: cú pháp và công cụ).
3. Đặc tả `ops/specs/DOC-CLAIMS-DAU-CHAM-r3.md`. Tệp KHÔNG nằm trong checkout: đọc bằng
   `git show 889d8a7e49b9940d8d20de896b1656a06c809222:ops/specs/DOC-CLAIMS-DAU-CHAM-r3.md` (ref
   `origin/ops/spec-doc-claims-dau-cham`), chép ra thư mục nháp, đo sha256 byte thô; phải bằng
   `0712647206e62eaca32701ddc05dd4aa0930f43174722aa016883d645be84864`. Khác thì dừng. Mục 2 (M1–M4) là việc; mục 5 (N1–N8) là
   nghiệm thu; mục 6 là luật dừng.

## Phạm vi

- Thư mục làm việc là clone `D:/tlx/dcc`, nhánh `agent/doc-claims-dau-cham-g1-claude` tại base `9c1661f76d5f4ef811aa349df102989cc2e2d53d` (= `origin/master` lúc
  cấp lease). Thư mục nháp ngoài checkout: `D:/tlx/dcc-scratch` (vị từ, log, bản sao đột biến, handoff để ở đó, không trong
  checkout).
- Write set đúng bốn tệp: `scripts/tl_core/workflow.py`, `scripts/test_fragments/wp1326_doc_claims_dau_cham.py` (mới),
  `scripts/tl_test_fragments_bundled.py` (chỉ tái sinh, M3), `RELEASE_MANIFEST.json` (chỉ tái sinh, M4). Không sửa tệp nào khác.
- Không đổi nhánh, không push, không gọi GitHub, không dùng mạng. Không chạy `packet_loop.py init`, `begin-attempt` hay lệnh ghi
  state nào.
- Đột biến N2 làm trên BẢN SAO TẠM trong `D:/tlx/dcc-scratch`, không bao giờ sửa tệp thật rồi khôi phục.

## Việc

1. Thi công M1–M4 đúng đặc tả. Giữ idiom chú thích của kho (dẫn #1326, `ADR-0032`, `ADR-0066` ở hằng miễn trừ).
2. Đo N3 và N4 TRƯỚC khi chạy `golden-test` (lệnh ấy sinh thư mục `references/golden/fixtures/`, làm số N3 khác điều kiện
   "checkout sạch"); nếu thư mục đã có thì ghi rõ và đo lại sau khi xác nhận nó là thư mục sinh, không phải tệp tracked.
3. Chạy N1 (`python scripts/tl.py --selftest`, đủ N/N hai số bằng nhau; ghi dòng fragment `wp1326_doc_claims_dau_cham`), N2
   (D1–D9, mỗi cái ghi TÊN ca lệch đọc từ thông báo FAIL), N5 (từng cổng và phép làm đỏ của nó), N8. Ghi rc thật của từng lệnh.
4. Một commit trên nhánh hiện tại, chỉ bốn tệp. Thông điệp: dòng đầu `DOC-CLAIMS-DAU-CHAM r3 g1: doc-claims-check L1 kiểm đúng
   đường dẫn bắt đầu bằng dấu chấm`; thân nêu Issue #1326 và sha256 đặc tả; dòng cuối
   `Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>`.
5. Ghi `D:/tlx/dcc-scratch/HANDOFF.md`: SHA H và tree, base, `git diff --numstat` so base, từng lệnh kèm rc và dòng kết luận, bảng
   ca N2, số đếm N3, những gì không làm hoặc không đo được, và mọi chỗ bạn thấy đặc tả có vấn đề.

## Khi nào dừng

- sha256 đặc tả không khớp, hay tiền điều kiện của mục 2 sai trên base: dừng, ghi lý do vào handoff.
- Một tiêu chí đỏ vì văn bản đặc tả (không phải vì mã của bạn): dừng và ghi đề xuất revision vào handoff (mục 6 đặc tả; E3 nếu
  mâu thuẫn quyết định của chủ kho).
