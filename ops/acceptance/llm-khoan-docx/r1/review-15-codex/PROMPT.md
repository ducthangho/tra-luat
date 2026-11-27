# Cross-review packet #1525 LLM-KHOAN-DOCX r15 (PR #1517, ducthangho/tra-luat) — lượt 15, reviewer Codex

Lời gọi Codex thứ 15 — CUỐI CÙNG — trong trần 15 (chủ kho nâng 14 → 15 sau lượt 14; lease `ops/leases/llm-khoan-docx-r15-g1-claude.yaml`, `review_calls_limit: 15`, `review_calls_used_truoc: 14`). r15 thay cách chuẩn hoá đầu đoạn bằng MỘT bản chiếu ký tự (§2.17 Q1) — đánh giá bản chiếu có đóng lớp biên ký tự hay không. Tại checkpoint, chốt `ranh-gioi-khoan` đã ĐỔI THIẾT KẾ từ nhận diện hình dạng tiêu đề sang CẤM TIỀN TỐ `Điều <số>` (§2.16 N1) — hãy đánh giá thiết kế mới đóng lớp hay không, không chỉ các biểu hiện cũ. Chặn oan dẫn chiếu MỞ ĐẦU đoạn là cái giá đã khai, không phải finding.
Bề mặt reviewer: `codex_cli` (`codex exec` qua `.claude/dev/launcher.py run`).

Bạn là reviewer độc lập. Thư mục làm việc là bản sao RỜI của kho, checkout detached đúng commit cần review:

- reviewed_sha: `b5cff4212a6abf052c74c772a525f54950b32b5e`
- base_sha: `64b7f2c14776d5d0e1d34a6be4725490956f5bec` (master)
- Đặc tả đóng băng HIỆN HÀNH: `ops/specs/llm-khoan-docx-r15.md` (thay r14; §2.4 (r2) … §2.17 (r15) THAY các điểm tương ứng trước đó) —
  kiểm sha256 khớp `spec_hash` trong lease r15. Lượt 14 chấm `0447395`: verdict `ops/acceptance/llm-khoan-docx/r1/review-14-codex/VERDICT.md`
  (Q1 P1, Q2 P2). Nhánh đã đẩy tới `f5201db` (chủ kho chọn tiếp tục; ghi ở đầu đặc tả r15). Nhánh đã được đẩy tới `fce28fd` trước approve (ngoại lệ M5 do chủ kho duyệt, ghi ở đầu đặc tả r12). r7 ĐỔI HỢP ĐỒNG theo quyết định chủ kho: tệp .docx chỉ chứa ĐÚNG Điều cần đọc (§2.9) — không còn
  đoán điểm kết thúc Điều; finding về "tệp nhiều Điều bị chặn" là giới hạn đã khai. Diff bản vá: `git diff f5201db b5cff4212a6abf052c74c772a525f54950b32b5e`.
- Bối cảnh: nhánh này mang packet #1514 (dừng ở r9 `fcb12b3`, verdict lượt 10 `ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md`:
  APPROVE, còn K1 P2). Packet #1525 làm tiếp trên cùng nhánh: thêm đường ranh giới từ CẤU TRÚC .docx và đóng K1 bằng cách cho đường
  văn bản thô chỉ nhận khoản đúng một dòng. Lease #1525 thay lease r9 của #1514 (bia mộ hai chiều).
  Diff packet này: `git diff fcb12b3 b5cff4212a6abf052c74c772a525f54950b32b5e` (bỏ qua các tệp hồ sơ `ops/acceptance/llm-ranh-gioi-khoan/`). Diff toàn PR: `git diff 64b7f2c b5cff4212a6abf052c74c772a525f54950b32b5e`.
- Điều kiện merge theo ADR-0060 M1 (mặc định qua ADR-0062): 0 finding P0, P1, P2 mở.

Đọc `CLAUDE.md` ở gốc kho trước.

## PHẠM VI — lượt KIỂM CHỨNG

Các lượt review của mảng này từng bị nền từ chối phản hồi khi reviewer tự dựng nội dung thử nghiệm mới. Lượt này chỉ:
1. **Đối chiếu** Q1–Q2 của lượt 14 (và A–N trước đó) (ĐÃ VÁ THẬT / VÁ MỘT PHẦN / CHƯA VÁ / VÁ SINH LỖI MỚI / HẾT ĐỐI TƯỢNG do hợp đồng r7)
   và đặc tả r15 (§1, §2.1–§2.17, §3); write set đúng lease r15; bia mộ hai chiều r9 (#1514) ↔ r1 ↔ … ↔ r15 đúng; K1 (nợ #1514) vẫn đóng.
2. **Chạy** các bộ test có sẵn (mục "Cách đo") và báo số đạt/tổng.
3. **Đột biến bản vá** trên BẢN SAO TẠM: bảng `DOT_BIEN` có sẵn (bộ test tự chạy; đột biến `wp1525_*`) và, nếu muốn, sửa vài dòng của
   `doc_dieu_docx` / `_phan_tich_doan` / `_doan_trong` / `_doc_danh_so` / `doc_dieu_cau_truc` để xác nhận ca đích đỏ đúng lý do.
4. **Đọc mã** `scripts/tl_core/llm_route.py` (`doc_dieu_docx`, `_doan_trong`, `_phan_tich_doan`, `_doc_danh_so`, `_doc_kieu`, `_theo_kieu`, `_nhan`, `doc_dieu_cau_truc`, `tach_khoan`, `lech_nguyen_van`)
   và `scripts/tl_core/ops_misc.py` (`cmd_llm_khai_niem`), mô tả nghi vấn **bằng lời**. KHÔNG viết thêm tệp thử nghiệm, tệp .docx,
   chuỗi thử nghiệm hay script dò mới; điều chỉ kiểm được bằng thử nghiệm mới thì ghi vào "Không đo được".

## Câu hỏi cần trả lời
- Còn đường nào để một kết quả SAI (bỏ/gộp/cắt/tráo khoản, hoặc chữ đã bỏ của dự thảo) được nhận là nguyên văn — ở đường cấu trúc
  hay đường thô — theo đọc mã? Đặc biệt: bộ đếm số Word (`start`, `startOverride`, đặt lại cấp con, nhiều numId), định vị vùng Điều,
  điểm gõ tay, câu dẫn, `KhongCauTruc` lùi về đường thô.
- K1 (nhánh điểm và tiếp dòng "là" ở nguồn có số) đã đóng ở đường thô chưa? Lớp `ranh-gioi-khoan` còn biểu hiện nào trên đường thô?
- Có dạng .docx văn bản luật THƯỜNG GẶP (Word/Google Doc) bị chặn oan mà đặc tả không khai không? Danh sách cho phép của §2.5 có
  thiếu phần tử phổ biến của bản export Google Doc / Word (ghi P2 kèm lý do; chặn oan không phải nhận sai)?

Phân hạng finding theo bảng severity của `docs/PROTOCOL_DA_PHIEN.md` và ADR-0060, nêu lý do hạng. Giới hạn đã khai (không phải finding):
`can_nguoi_duyet: true` giữ nguyên; mọi giới hạn liệt kê trong đặc tả r15 và `docs/GOI_AGENT_DA_NEN.md` mục script gọi Claude.
VERDICT: APPROVE nếu không còn P0/P1; ghi riêng số P2 còn mở (điều kiện merge).

**Ghi dòng `VERDICT:` SỚM** (tạm), cập nhật nếu kết luận đổi.

## Cách đo (không cần mạng)

```
python scripts/tl_core/llm_route_test.py
python scripts/tl.py --deterministic workflow-audit --strict --json
python scripts/tl.py --deterministic golden-test --json
python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r15-g1-claude.yaml
python scripts/tl.py --selftest        # ~6 phút
```

Lưu ý môi trường: thư mục RỖNG `/tmp/.git` (sandbox để lại) làm 14 ca selftest `r973_bootstrap_*`, `wp433_*`,
`wp727_tl_gws_refresh` đỏ trên CẢ base lẫn head — đỏ sẵn, không phải hồi quy.

## Ràng buộc
- KHÔNG gọi Claude/Anthropic API thật, KHÔNG chạy `claude -p` thật, KHÔNG chạy `tl llm-khai-niem` với model thật. Không đọc/in bí mật.
- KHÔNG push, KHÔNG gọi GitHub, KHÔNG sửa tệp đã theo dõi trong cây.

## Đầu ra
Ghi TĂNG DẦN vào `.review/VERDICT.md`:

```
# Verdict packet #1525 r15 lượt 15 — Codex
reviewed_sha: b5cff4212a6abf052c74c772a525f54950b32b5e
## Đối chiếu lượt 14 và đặc tả r15
| Mục | Trạng thái | Bằng chứng |
## Findings
### R1 [P?] <tiêu đề> — <tệp:dòng>
Kịch bản (bằng lời) / Căn cứ / Đề xuất
## Kết quả test và đột biến
## Không đo được
P2_mo: <số>
VERDICT: APPROVE | REQUEST_CHANGES
```
