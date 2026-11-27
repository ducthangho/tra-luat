# Cross-review packet #1525 LLM-KHOAN-DOCX r1 (PR #1517, ducthangho/tra-luat) — lượt 1, reviewer Codex

Lời gọi Codex thứ 1 trong trần 5 (lease `ops/leases/llm-khoan-docx-r1-g1-claude.yaml`, `review_calls_limit: 5`).
Bề mặt reviewer: `codex_cli` (`codex exec` qua `.claude/dev/launcher.py run`).

Bạn là reviewer độc lập. Thư mục làm việc là bản sao RỜI của kho, checkout detached đúng commit cần review:

- reviewed_sha: `3d247516aaeb0ad3d836a2dc51dda13052fdbe47`
- base_sha: `64b7f2c14776d5d0e1d34a6be4725490956f5bec` (master)
- Đặc tả đóng băng: `ops/specs/llm-khoan-docx-r1.md` — kiểm sha256 khớp `spec_hash` trong lease trước khi review.
- Bối cảnh: nhánh này mang packet #1514 (dừng ở r9 `fcb12b3`, verdict lượt 10 `ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md`:
  APPROVE, còn K1 P2). Packet #1525 làm tiếp trên cùng nhánh: thêm đường ranh giới từ CẤU TRÚC .docx và đóng K1 bằng cách cho đường
  văn bản thô chỉ nhận khoản đúng một dòng. Lease #1525 thay lease r9 của #1514 (bia mộ hai chiều).
  Diff packet này: `git diff fcb12b3 3d247516aaeb0ad3d836a2dc51dda13052fdbe47` (bỏ qua các tệp hồ sơ `ops/acceptance/llm-ranh-gioi-khoan/`). Diff toàn PR: `git diff 64b7f2c 3d247516aaeb0ad3d836a2dc51dda13052fdbe47`.
- Điều kiện merge theo ADR-0060 M1 (mặc định qua ADR-0062): 0 finding P0, P1, P2 mở.

Đọc `CLAUDE.md` ở gốc kho trước.

## PHẠM VI — lượt KIỂM CHỨNG

Các lượt review của mảng này từng bị nền từ chối phản hồi khi reviewer tự dựng nội dung thử nghiệm mới. Lượt này chỉ:
1. **Đối chiếu** đặc tả r1 (§1, §2.1–§2.3, §3) với mã; write set đúng lease; bia mộ hai chiều r9 (#1514) ↔ r1 (#1525) đúng; K1 đã đóng chưa.
2. **Chạy** các bộ test có sẵn (mục "Cách đo") và báo số đạt/tổng.
3. **Đột biến bản vá** trên BẢN SAO TẠM: bảng `DOT_BIEN` có sẵn (bộ test tự chạy; đột biến `wp1525_*`) và, nếu muốn, sửa vài dòng của
   `doc_dieu_docx` / `doc_dieu_cau_truc` / nhánh dòng điểm của `tach_khoan` để xác nhận ca đích đỏ đúng lý do.
4. **Đọc mã** `scripts/tl_core/llm_route.py` (`doc_dieu_docx`, `_doc_danh_so`, `_nhan`, `doc_dieu_cau_truc`, `tach_khoan`, `lech_nguyen_van`)
   và `scripts/tl_core/ops_misc.py` (`cmd_llm_khai_niem`), mô tả nghi vấn **bằng lời**. KHÔNG viết thêm tệp thử nghiệm, tệp .docx,
   chuỗi thử nghiệm hay script dò mới; điều chỉ kiểm được bằng thử nghiệm mới thì ghi vào "Không đo được".

## Câu hỏi cần trả lời
- Còn đường nào để một kết quả SAI (bỏ/gộp/cắt/tráo khoản, hoặc chữ đã bỏ của dự thảo) được nhận là nguyên văn — ở đường cấu trúc
  hay đường thô — theo đọc mã? Đặc biệt: bộ đếm số Word (`start`, `startOverride`, đặt lại cấp con, nhiều numId), định vị vùng Điều,
  điểm gõ tay, câu dẫn, `KhongCauTruc` lùi về đường thô.
- K1 (nhánh điểm và tiếp dòng "là" ở nguồn có số) đã đóng ở đường thô chưa? Lớp `ranh-gioi-khoan` còn biểu hiện nào trên đường thô?
- Có dạng .docx văn bản luật THƯỜNG GẶP (Word/Google Doc) bị chặn oan mà đặc tả không khai không?

Phân hạng finding theo bảng severity của `docs/PROTOCOL_DA_PHIEN.md` và ADR-0060, nêu lý do hạng. Giới hạn đã khai (không phải finding):
`can_nguoi_duyet: true` giữ nguyên; mọi giới hạn liệt kê trong đặc tả r1 và `docs/GOI_AGENT_DA_NEN.md` mục script gọi Claude.
VERDICT: APPROVE nếu không còn P0/P1; ghi riêng số P2 còn mở (điều kiện merge).

**Ghi dòng `VERDICT:` SỚM** (tạm), cập nhật nếu kết luận đổi.

## Cách đo (không cần mạng)

```
python scripts/tl_core/llm_route_test.py
python scripts/tl.py --deterministic workflow-audit --strict --json
python scripts/tl.py --deterministic golden-test --json
python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r1-g1-claude.yaml
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
# Verdict packet #1525 r1 lượt 1 — Codex
reviewed_sha: 3d247516aaeb0ad3d836a2dc51dda13052fdbe47
## Đối chiếu đặc tả r1
| Mục | Trạng thái | Bằng chứng |
## Findings
### A1 [P?] <tiêu đề> — <tệp:dòng>
Kịch bản (bằng lời) / Căn cứ / Đề xuất
## Kết quả test và đột biến
## Không đo được
P2_mo: <số>
VERDICT: APPROVE | REQUEST_CHANGES
```
