# Cross-review packet #1514 LLM-RANH-GIOI-KHOAN r5 (PR #1517, ducthangho/tra-luat) — lượt 6, reviewer Codex

Lời gọi Codex thứ 6 — CUỐI CÙNG — trong trần 6 TÍNH CHUNG cho packet (lease r5 `ops/leases/llm-ranh-gioi-khoan-r5-g1-claude.yaml`,
`review_calls_limit: 6`, `review_calls_used_truoc: 5`; chủ kho nâng trần 5 → 6 sau lượt 5). Bề mặt reviewer: `codex_cli` (`codex exec` qua `.claude/dev/launcher.py run`).

Bạn là reviewer độc lập. Thư mục làm việc là bản sao RỜI của kho, checkout detached đúng commit cần review:

- reviewed_sha: `aed16f390f4adf59dde5718bff170c5cddd44cbb`
- base_sha: `64b7f2c14776d5d0e1d34a6be4725490956f5bec` (master)
- Đặc tả đóng băng HIỆN HÀNH: `ops/specs/llm-ranh-gioi-khoan-r5.md` — kiểm sha256 khớp `spec_hash` trong lease r5 trước khi review.
  r5 thay r4 thay r3 thay r2 thay r1 (bia mộ hai chiều từng cặp); §2.5 (r2), §2.6 (r3), §2.7 (r4), §2.8 (r5) là phần bổ sung.
- Lượt 5 chấm `9541e02`; verdict ở `ops/acceptance/llm-ranh-gioi-khoan/r1/review-5-codex/VERDICT.md` (APPROVE, còn E1/E2 P2).
  Điều kiện merge theo ADR-0060 M1 (mặc định qua ADR-0062): 0 finding P0, P1, P2 mở — nên lượt này phải kết luận E1/E2 đã đóng chưa.
  Diff bản vá: `git diff 9541e02 aed16f390f4adf59dde5718bff170c5cddd44cbb`. Diff toàn packet: `git diff 64b7f2c aed16f390f4adf59dde5718bff170c5cddd44cbb`.

Đọc `CLAUDE.md` ở gốc kho trước.

## PHẠM VI — lượt KIỂM CHỨNG

Các lượt review của mảng này từng bị nền từ chối phản hồi khi reviewer tự dựng nội dung thử nghiệm mới. Lượt này chỉ:
1. **Đối chiếu** E1, E2 của lượt 5 (và các mục trước) (ĐÃ VÁ THẬT / VÁ MỘT PHẦN / CHƯA VÁ / VÁ SINH LỖI MỚI) và đặc tả r5 (§2, §2.5–§2.8, §4);
   write set đúng lease r5; bia mộ hai chiều r1↔r2↔r3↔r4↔r5 đúng.
2. **Chạy** các bộ test có sẵn (mục "Cách đo") và báo số đạt/tổng.
3. **Đột biến bản vá** trên BẢN SAO TẠM: bảng `DOT_BIEN` có sẵn (bộ test tự chạy; ba đột biến mới `wp1514_l5_*`) và, nếu muốn, sửa vài
   dòng của chính bản vá (`_RE_SO_NOI_DONG`, `_RE_LA_TU`, điều kiện câu dẫn) để xác nhận ca đích đỏ đúng lý do.
4. **Đọc mã** `scripts/tl_core/llm_route.py` và mô tả nghi vấn **bằng lời**. KHÔNG viết thêm tệp thử nghiệm, chuỗi thử nghiệm hay
   script dò mới; điều chỉ kiểm được bằng thử nghiệm mới thì ghi vào "Không đo được".

## Câu hỏi cần trả lời
- E1, E2 đã đóng chưa? Bản vá E1 (chữ cái sau dấu số) có chặn oan dạng văn bản luật thường gặp nào mà đặc tả không khai không?
  Bản vá E2 (đúng một `:`, không có chữ "là") có chặn oan câu dẫn chuẩn nào không?
- Còn đường nào để một kết quả SAI (bỏ/gộp/cắt sai khoản) được nhận là nguyên văn, theo đọc mã?
- Có dạng "Giải thích từ ngữ" phổ biến nào bị chặn oan mà đặc tả KHÔNG khai là giới hạn?

Phân hạng finding theo bảng severity của `docs/PROTOCOL_DA_PHIEN.md` và ADR-0060, nêu lý do hạng. Giới hạn đã khai (không phải finding):
`can_nguoi_duyet: true` giữ nguyên (kết quả luôn cần người duyệt ranh giới khoản); mọi giới hạn liệt kê trong đặc tả r5 và
`docs/GOI_AGENT_DA_NEN.md` mục script gọi Claude. VERDICT: APPROVE nếu không còn P0/P1; ghi riêng số P2 còn mở (điều kiện merge).

**Ghi dòng `VERDICT:` SỚM** (tạm), cập nhật nếu kết luận đổi.

## Cách đo (không cần mạng)

```
python scripts/tl_core/llm_route_test.py
python scripts/tl.py --deterministic workflow-audit --strict --json
python scripts/tl.py --deterministic golden-test --json
python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
python ops/lease_publish.py check --root . ops/leases/llm-ranh-gioi-khoan-r5-g1-claude.yaml
python scripts/tl.py --selftest        # ~6 phút
```

Lưu ý môi trường: thư mục RỖNG `/tmp/.git` (sandbox để lại) làm 14 ca selftest `r973_bootstrap_*`, `wp433_*`,
`wp727_tl_gws_refresh` đỏ trên CẢ base lẫn head — đỏ sẵn, không phải hồi quy.

## Ràng buộc
- KHÔNG gọi Claude/Anthropic API thật, KHÔNG chạy `claude -p` thật, KHÔNG chạy `tl llm-khai-niem` thật. Không đọc/in bí mật.
- KHÔNG push, KHÔNG gọi GitHub, KHÔNG sửa tệp đã theo dõi trong cây.

## Đầu ra
Ghi TĂNG DẦN vào `.review/VERDICT.md`:

```
# Verdict packet #1514 r5 lượt 6 — Codex
reviewed_sha: aed16f390f4adf59dde5718bff170c5cddd44cbb
## Đối chiếu lượt 5 và đặc tả r5
| Mục | Trạng thái | Bằng chứng |
## Findings
### F1 [P?] <tiêu đề> — <tệp:dòng>
Kịch bản (bằng lời) / Căn cứ / Đề xuất
## Kết quả test và đột biến
## Không đo được
P2_mo: <số>
VERDICT: APPROVE | REQUEST_CHANGES
```
