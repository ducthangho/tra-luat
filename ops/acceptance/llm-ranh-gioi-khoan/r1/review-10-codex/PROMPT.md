# Cross-review packet #1514 LLM-RANH-GIOI-KHOAN r9 (PR #1517, ducthangho/tra-luat) — lượt 10, reviewer Codex

Lời gọi Codex thứ 10 — CUỐI CÙNG — trong trần 10 TÍNH CHUNG cho packet (lease r9 `ops/leases/llm-ranh-gioi-khoan-r9-g1-claude.yaml`,
`review_calls_limit: 10`, `review_calls_used_truoc: 9`; chủ kho nâng trần 9 → 10 sau lượt 9). Bề mặt reviewer: `codex_cli` (`codex exec` qua `.claude/dev/launcher.py run`).

Bạn là reviewer độc lập. Thư mục làm việc là bản sao RỜI của kho, checkout detached đúng commit cần review:

- reviewed_sha: `fcb12b3873c3bec2c339029136243ed2c804ce05`
- base_sha: `64b7f2c14776d5d0e1d34a6be4725490956f5bec` (master)
- Đặc tả đóng băng HIỆN HÀNH: `ops/specs/llm-ranh-gioi-khoan-r9.md` — kiểm sha256 khớp `spec_hash` trong lease r9 trước khi review.
  r9 thay r8 … thay r1 (bia mộ hai chiều từng cặp); §2.5 (r2), §2.6 (r3), §2.7 (r4), §2.8 (r5), §2.9 (r6), §2.10 (r7), §2.11 (r8, THAY §2.10), §2.12 (r9, THAY §2.10–§2.11) là phần bổ sung.
- Lượt 9 chấm `5aa5b34`; verdict ở `ops/acceptance/llm-ranh-gioi-khoan/r1/review-9-codex/VERDICT.md` (APPROVE, còn J1 P2).
  Điều kiện merge theo ADR-0060 M1 (mặc định qua ADR-0062): 0 finding P0, P1, P2 mở. r9 (§2.12) đóng nhánh "giữ rồi ghép" bằng CẤU
  TRÚC: nguồn mất số không được có dòng điểm nào, nên mỗi khoản của nó đúng một dòng. Câu hỏi chính: LỚP đã đóng chưa (M2) —
  nhánh bỏ dòng (§2.9), nhánh giữ rồi ghép (§2.12, nay cả nguồn có số: điểm và tiếp dòng `là`), đánh số nội dòng (§2.9).
  Diff bản vá: `git diff acedac5 fcb12b3873c3bec2c339029136243ed2c804ce05`. Diff toàn packet: `git diff 64b7f2c fcb12b3873c3bec2c339029136243ed2c804ce05`.

Đọc `CLAUDE.md` ở gốc kho trước.

## PHẠM VI — lượt KIỂM CHỨNG

Các lượt review của mảng này từng bị nền từ chối phản hồi khi reviewer tự dựng nội dung thử nghiệm mới. Lượt này chỉ:
1. **Đối chiếu** J1 của lượt 9 (và H1, G1, F1, F2, các mục trước) (ĐÃ VÁ THẬT / VÁ MỘT PHẦN / CHƯA VÁ / VÁ SINH LỖI MỚI) và đặc tả r9 (§2, §2.5–§2.12, §4);
   write set đúng lease r9; bia mộ hai chiều r1↔…↔r9 đúng.
2. **Chạy** các bộ test có sẵn (mục "Cách đo") và báo số đạt/tổng.
3. **Đột biến bản vá** trên BẢN SAO TẠM: bảng `DOT_BIEN` có sẵn (bộ test tự chạy; đột biến mới `wp1514_l9_*`) và, nếu muốn, sửa vài
   dòng của chính bản vá (`_RE_SO_NOI_DONG`, `_RE_CAU_DAN_TRON`, điều kiện câu dẫn, chốt dòng điểm ở nguồn mất số) để xác nhận ca đích đỏ đúng lý do.
4. **Đọc mã** `scripts/tl_core/llm_route.py` và mô tả nghi vấn **bằng lời**. KHÔNG viết thêm tệp thử nghiệm, chuỗi thử nghiệm hay
   script dò mới; điều chỉ kiểm được bằng thử nghiệm mới thì ghi vào "Không đo được".

## Câu hỏi cần trả lời
- J1 (và H1, G1) và LỚP `ranh-gioi-khoan` (câu dẫn: cả lựa chọn BỎ dòng lẫn GIỮ rồi gộp sai; đánh số nội dòng) đã đóng chưa? Chốt nội dòng có thật là tập bao của mọi dạng
  `_RE_SO_KHOAN` nhận ở đầu dòng không (đối chiếu hai regex, bằng lời)? Danh sách câu dẫn có chặn oan câu dẫn chuẩn THƯỜNG GẶP nào
  mà §2.9 không khai không?
- Còn đường nào để một kết quả SAI (bỏ/gộp/cắt sai khoản) được nhận là nguyên văn, theo đọc mã?
- Có dạng "Giải thích từ ngữ" phổ biến nào bị chặn oan mà đặc tả KHÔNG khai là giới hạn?

Phân hạng finding theo bảng severity của `docs/PROTOCOL_DA_PHIEN.md` và ADR-0060, nêu lý do hạng. Giới hạn đã khai (không phải finding):
`can_nguoi_duyet: true` giữ nguyên (kết quả luôn cần người duyệt ranh giới khoản); mọi giới hạn liệt kê trong đặc tả r9 và
`docs/GOI_AGENT_DA_NEN.md` mục script gọi Claude. VERDICT: APPROVE nếu không còn P0/P1; ghi riêng số P2 còn mở (điều kiện merge).

**Ghi dòng `VERDICT:` SỚM** (tạm), cập nhật nếu kết luận đổi.

## Cách đo (không cần mạng)

```
python scripts/tl_core/llm_route_test.py
python scripts/tl.py --deterministic workflow-audit --strict --json
python scripts/tl.py --deterministic golden-test --json
python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
python ops/lease_publish.py check --root . ops/leases/llm-ranh-gioi-khoan-r9-g1-claude.yaml
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
# Verdict packet #1514 r9 lượt 10 — Codex
reviewed_sha: fcb12b3873c3bec2c339029136243ed2c804ce05
## Đối chiếu lượt 9 và đặc tả r9
| Mục | Trạng thái | Bằng chứng |
## Findings
### K1 [P?] <tiêu đề> — <tệp:dòng>
Kịch bản (bằng lời) / Căn cứ / Đề xuất
## Kết quả test và đột biến
## Không đo được
P2_mo: <số>
VERDICT: APPROVE | REQUEST_CHANGES
```
