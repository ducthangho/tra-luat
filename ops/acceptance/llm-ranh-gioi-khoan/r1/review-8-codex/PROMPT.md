# Cross-review packet #1514 LLM-RANH-GIOI-KHOAN r7 (PR #1517, ducthangho/tra-luat) — lượt 8, reviewer Codex

Lời gọi Codex thứ 8 — CUỐI CÙNG — trong trần 8 TÍNH CHUNG cho packet (lease r7 `ops/leases/llm-ranh-gioi-khoan-r7-g1-claude.yaml`,
`review_calls_limit: 8`, `review_calls_used_truoc: 7`; chủ kho nâng trần 7 → 8 sau lượt 7). Bề mặt reviewer: `codex_cli` (`codex exec` qua `.claude/dev/launcher.py run`).

Bạn là reviewer độc lập. Thư mục làm việc là bản sao RỜI của kho, checkout detached đúng commit cần review:

- reviewed_sha: `4d357d1ad679d1a0aeea9795fe9777be8a32c1e5`
- base_sha: `64b7f2c14776d5d0e1d34a6be4725490956f5bec` (master)
- Đặc tả đóng băng HIỆN HÀNH: `ops/specs/llm-ranh-gioi-khoan-r7.md` — kiểm sha256 khớp `spec_hash` trong lease r7 trước khi review.
  r7 thay r6 … thay r1 (bia mộ hai chiều từng cặp); §2.5 (r2), §2.6 (r3), §2.7 (r4), §2.8 (r5), §2.9 (r6), §2.10 (r7) là phần bổ sung.
- Lượt 7 chấm `0ec7ca0`; verdict ở `ops/acceptance/llm-ranh-gioi-khoan/r1/review-7-codex/VERDICT.md` (APPROVE, còn G1 P2; lớp
  `ranh-gioi-khoan` 2→1 biểu hiện). Điều kiện merge theo ADR-0060 M1 (mặc định qua ADR-0062): 0 finding P0, P1, P2 mở.
  r7 (§2.10) chặn cả nguồn mất số khi dòng đầu còn lại kết `:` mà không phải câu dẫn chuẩn. Câu hỏi chính: LỚP đã đóng chưa (M2).
  Diff bản vá: `git diff a1e5022 4d357d1ad679d1a0aeea9795fe9777be8a32c1e5`. Diff toàn packet: `git diff 64b7f2c 4d357d1ad679d1a0aeea9795fe9777be8a32c1e5`.

Đọc `CLAUDE.md` ở gốc kho trước.

## PHẠM VI — lượt KIỂM CHỨNG

Các lượt review của mảng này từng bị nền từ chối phản hồi khi reviewer tự dựng nội dung thử nghiệm mới. Lượt này chỉ:
1. **Đối chiếu** G1 của lượt 7 (và F1, F2, các mục trước) (ĐÃ VÁ THẬT / VÁ MỘT PHẦN / CHƯA VÁ / VÁ SINH LỖI MỚI) và đặc tả r7 (§2, §2.5–§2.10, §4);
   write set đúng lease r7; bia mộ hai chiều r1↔…↔r7 đúng.
2. **Chạy** các bộ test có sẵn (mục "Cách đo") và báo số đạt/tổng.
3. **Đột biến bản vá** trên BẢN SAO TẠM: bảng `DOT_BIEN` có sẵn (bộ test tự chạy; đột biến mới `wp1514_l7_*`) và, nếu muốn, sửa vài
   dòng của chính bản vá (`_RE_SO_NOI_DONG`, `_RE_CAU_DAN_TRON`, điều kiện câu dẫn, chốt dòng đầu kết `:` ở nguồn mất số) để xác nhận ca đích đỏ đúng lý do.
4. **Đọc mã** `scripts/tl_core/llm_route.py` và mô tả nghi vấn **bằng lời**. KHÔNG viết thêm tệp thử nghiệm, chuỗi thử nghiệm hay
   script dò mới; điều chỉ kiểm được bằng thử nghiệm mới thì ghi vào "Không đo được".

## Câu hỏi cần trả lời
- G1 và LỚP `ranh-gioi-khoan` (câu dẫn: cả lựa chọn BỎ dòng lẫn GIỮ rồi gộp sai; đánh số nội dòng) đã đóng chưa? Chốt nội dòng có thật là tập bao của mọi dạng
  `_RE_SO_KHOAN` nhận ở đầu dòng không (đối chiếu hai regex, bằng lời)? Danh sách câu dẫn có chặn oan câu dẫn chuẩn THƯỜNG GẶP nào
  mà §2.9 không khai không?
- Còn đường nào để một kết quả SAI (bỏ/gộp/cắt sai khoản) được nhận là nguyên văn, theo đọc mã?
- Có dạng "Giải thích từ ngữ" phổ biến nào bị chặn oan mà đặc tả KHÔNG khai là giới hạn?

Phân hạng finding theo bảng severity của `docs/PROTOCOL_DA_PHIEN.md` và ADR-0060, nêu lý do hạng. Giới hạn đã khai (không phải finding):
`can_nguoi_duyet: true` giữ nguyên (kết quả luôn cần người duyệt ranh giới khoản); mọi giới hạn liệt kê trong đặc tả r7 và
`docs/GOI_AGENT_DA_NEN.md` mục script gọi Claude. VERDICT: APPROVE nếu không còn P0/P1; ghi riêng số P2 còn mở (điều kiện merge).

**Ghi dòng `VERDICT:` SỚM** (tạm), cập nhật nếu kết luận đổi.

## Cách đo (không cần mạng)

```
python scripts/tl_core/llm_route_test.py
python scripts/tl.py --deterministic workflow-audit --strict --json
python scripts/tl.py --deterministic golden-test --json
python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
python ops/lease_publish.py check --root . ops/leases/llm-ranh-gioi-khoan-r7-g1-claude.yaml
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
# Verdict packet #1514 r7 lượt 8 — Codex
reviewed_sha: 4d357d1ad679d1a0aeea9795fe9777be8a32c1e5
## Đối chiếu lượt 7 và đặc tả r7
| Mục | Trạng thái | Bằng chứng |
## Findings
### H1 [P?] <tiêu đề> — <tệp:dòng>
Kịch bản (bằng lời) / Căn cứ / Đề xuất
## Kết quả test và đột biến
## Không đo được
P2_mo: <số>
VERDICT: APPROVE | REQUEST_CHANGES
```
