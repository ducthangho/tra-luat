# Cross-review packet #1514 LLM-RANH-GIOI-KHOAN r4 (PR #1517, ducthangho/tra-luat) — lượt 5, reviewer Codex

Lời gọi Codex thứ 5 — CUỐI CÙNG — trong trần 5 TÍNH CHUNG cho packet (lease r4 `ops/leases/llm-ranh-gioi-khoan-r4-g1-claude.yaml`,
`review_calls_limit: 5`, `review_calls_used_truoc: 4`). Bề mặt reviewer: `codex_cli` (`codex exec` qua `.claude/dev/launcher.py run`).

Bạn là reviewer độc lập. Thư mục làm việc là bản sao RỜI của kho, checkout detached đúng commit cần review:

- reviewed_sha: `9541e023bc5c0df8d346f2e5caaa54993a0aa60a`
- base_sha: `64b7f2c14776d5d0e1d34a6be4725490956f5bec` (master)
- Đặc tả đóng băng HIỆN HÀNH: `ops/specs/llm-ranh-gioi-khoan-r4.md` — kiểm sha256 khớp `spec_hash` trong lease r4 trước khi review.
  r4 thay r3 thay r2 thay r1 (bia mộ hai chiều từng cặp); §2.5 (r2), §2.6 (r3), §2.7 (r4) là phần bổ sung.
- Lượt 4 chấm `e9fc10c`; verdict ở `ops/acceptance/llm-ranh-gioi-khoan/r1/review-4-codex/VERDICT.md` (D1 P1, D2/D3 P2, REQUEST_CHANGES). Lượt này còn thêm sửa `scripts/tl_selftest.py` (lỗi đo trên Windows bản địa, §2.7).
  Diff bản vá: `git diff e9fc10c 9541e02`. Diff toàn packet: `git diff 64b7f2c 9541e02`.

Đọc `CLAUDE.md` ở gốc kho trước.

## PHẠM VI — lượt KIỂM CHỨNG

Các lượt review của mảng này từng bị nền từ chối phản hồi khi reviewer tự dựng nội dung thử nghiệm mới. Lượt này chỉ:
1. **Đối chiếu** D1, D2, D3 của lượt 4 (và các mục trước còn mở) (ĐÃ VÁ THẬT / VÁ MỘT PHẦN / CHƯA VÁ / VÁ SINH LỖI MỚI) và đặc tả r4 (§2, §2.5, §2.6, §2.7, §4); write set đúng
   lease r4; bia mộ hai chiều r1↔r2↔r3↔r4 đúng.
2. **Chạy** các bộ test có sẵn (mục "Cách đo") và báo số đạt/tổng.
3. **Đột biến bản vá** trên BẢN SAO TẠM: bảng `DOT_BIEN` có sẵn (bộ test tự chạy) và, nếu muốn, sửa vài dòng của chính bản vá
   (`_DAU_CAU_KET`, `_RE_SO_NOI_DONG`, `_RE_TIEU_DE_TRON`, `_ket_thuc_cau`, điều kiện câu dẫn) để xác nhận ca đích
   đỏ đúng lý do.
4. **Đọc mã** `scripts/tl_core/llm_route.py` và mô tả nghi vấn **bằng lời**. KHÔNG viết thêm tệp thử nghiệm, chuỗi thử nghiệm hay
   script dò mới; điều chỉ kiểm được bằng thử nghiệm mới thì ghi vào "Không đo được".

## Câu hỏi cần trả lời
- D1, D3 đã đóng chưa? D2 đã được khai thành giới hạn đúng chưa? Sửa selftest Windows (§2.7) có đúng phạm vi (chỉ nới phép kiểm quyền trên `nt`) không?
- Còn đường nào để một kết quả SAI (bỏ/gộp/cắt sai khoản) được nhận là nguyên văn, theo đọc mã?
- Có dạng "Giải thích từ ngữ" phổ biến nào bị chặn oan mà đặc tả KHÔNG khai là giới hạn? (Chặn oan là P2/P3.)

APPROVE nếu không còn P0/P1. Giới hạn đã khai (không tính là P1): `can_nguoi_duyet: true` giữ nguyên (kết quả luôn cần người duyệt
ranh giới khoản); mọi giới hạn liệt kê trong đặc tả r4 và `docs/GOI_AGENT_DA_NEN.md` mục script gọi Claude. Một dạng tách/bỏ khoản
MỚI mà chỉ có thể tạo bằng văn bản nguồn cố ý dị dạng (không phải dạng văn bản luật thường gặp) thì ghi P2 kèm lý do, vì kết quả vẫn
mang cờ cần người duyệt.

**Ghi dòng `VERDICT:` SỚM** (tạm), cập nhật nếu kết luận đổi.

## Cách đo (không cần mạng)

```
python scripts/tl_core/llm_route_test.py
python scripts/tl.py --deterministic workflow-audit --strict --json
python scripts/tl.py --deterministic golden-test --json
python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
python ops/lease_publish.py check --root . ops/leases/llm-ranh-gioi-khoan-r4-g1-claude.yaml
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
# Verdict packet #1514 r4 lượt 5 — Codex
reviewed_sha: 9541e023bc5c0df8d346f2e5caaa54993a0aa60a
## Đối chiếu lượt 4 và đặc tả r4
| Mục | Trạng thái | Bằng chứng |
## Findings
### E1 [P?] <tiêu đề> — <tệp:dòng>
Kịch bản (bằng lời) / Căn cứ / Đề xuất
## Kết quả test và đột biến
## Không đo được
VERDICT: APPROVE | REQUEST_CHANGES
```
