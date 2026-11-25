# Cross-review packet #1514 LLM-RANH-GIOI-KHOAN r2 (PR #1517, ducthangho/tra-luat) — lượt 3, reviewer Codex

Lời gọi Codex thứ 3 trong trần 5 TÍNH CHUNG cho packet (lease r2 `ops/leases/llm-ranh-gioi-khoan-r2-g1-claude.yaml`,
`review_calls_limit: 5`, `review_calls_used_truoc: 2`). Bề mặt reviewer: `codex_cli` (`codex exec` qua `.claude/dev/launcher.py run`).

Bạn là reviewer độc lập. Thư mục làm việc là bản sao RỜI của kho, checkout detached đúng commit cần review:

- reviewed_sha: `64153dbfb402bcf1d0ac7ecd614b7aa23bb57d8f`
- base_sha: `64b7f2c14776d5d0e1d34a6be4725490956f5bec` (master)
- Đặc tả đóng băng HIỆN HÀNH: `ops/specs/llm-ranh-gioi-khoan-r2.md` — kiểm sha256 khớp `spec_hash` trong lease r2 trước khi review.
  r2 thay r1 (bia mộ hai chiều giữa hai lease); §2.5 của r2 là phần bổ sung.
- Lượt 2 chấm `53c49ab`; verdict ở `ops/acceptance/llm-ranh-gioi-khoan/r1/review-2-codex/VERDICT.md` (A1–A4, REQUEST_CHANGES).
  Diff bản vá: `git diff 53c49ab 64153db`. Diff toàn packet: `git diff 64b7f2c 64153db`.

Đọc `CLAUDE.md` ở gốc kho trước.

## PHẠM VI — lượt KIỂM CHỨNG

Các lượt review của mảng này từng bị nền từ chối phản hồi khi reviewer tự dựng nội dung thử nghiệm mới. Lượt này chỉ:
1. **Đối chiếu** A1–A4 của lượt 2 (ĐÃ VÁ THẬT / VÁ MỘT PHẦN / CHƯA VÁ / VÁ SINH LỖI MỚI) và đặc tả r2 (§2, §2.5, §4); write set đúng
   lease r2; bia mộ hai chiều r1↔r2 đúng.
2. **Chạy** các bộ test có sẵn (mục "Cách đo") và báo số đạt/tổng.
3. **Đột biến bản vá** trên BẢN SAO TẠM: bảng `DOT_BIEN` có sẵn (bộ test tự chạy) và, nếu muốn, sửa vài dòng của chính bản vá
   (`_DAU_CAU_KET`, `_RE_SO_NOI_DONG`, nhánh tiêu đề `_RE_LA.search(dong[0])`, `_ket_thuc_cau`, điều kiện câu dẫn) để xác nhận ca đích
   đỏ đúng lý do.
4. **Đọc mã** `scripts/tl_core/llm_route.py` và mô tả nghi vấn **bằng lời**. KHÔNG viết thêm tệp thử nghiệm, chuỗi thử nghiệm hay
   script dò mới; điều chỉ kiểm được bằng thử nghiệm mới thì ghi vào "Không đo được".

## Câu hỏi cần trả lời
- A1–A4 đã đóng chưa? Ba luật r2 (A2a/A2b/A2c) đúng đặc tả và có răng?
- Còn đường nào để một kết quả SAI (bỏ/gộp/cắt sai khoản) được nhận là nguyên văn, theo đọc mã?
- Có dạng "Giải thích từ ngữ" phổ biến nào bị chặn oan mà đặc tả KHÔNG khai là giới hạn? (Chặn oan là P2/P3.)

APPROVE nếu không còn P0/P1. Giới hạn đã khai (không tính là P1): `can_nguoi_duyet: true` giữ nguyên (kết quả luôn cần người duyệt
ranh giới khoản); mọi giới hạn liệt kê trong đặc tả r2 và `docs/GOI_AGENT_DA_NEN.md` mục script gọi Claude. Một dạng tách/bỏ khoản
MỚI mà chỉ có thể tạo bằng văn bản nguồn cố ý dị dạng (không phải dạng văn bản luật thường gặp) thì ghi P2 kèm lý do, vì kết quả vẫn
mang cờ cần người duyệt.

**Ghi dòng `VERDICT:` SỚM** (tạm), cập nhật nếu kết luận đổi.

## Cách đo (không cần mạng)

```
python scripts/tl_core/llm_route_test.py
python scripts/tl.py --deterministic workflow-audit --strict --json
python scripts/tl.py --deterministic golden-test --json
python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
python ops/lease_publish.py check --root . ops/leases/llm-ranh-gioi-khoan-r2-g1-claude.yaml
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
# Verdict packet #1514 r2 lượt 3 — Codex
reviewed_sha: 64153dbfb402bcf1d0ac7ecd614b7aa23bb57d8f
## Đối chiếu lượt 2 và đặc tả r2
| Mục | Trạng thái | Bằng chứng |
## Findings
### C1 [P?] <tiêu đề> — <tệp:dòng>
Kịch bản (bằng lời) / Căn cứ / Đề xuất
## Kết quả test và đột biến
## Không đo được
VERDICT: APPROVE | REQUEST_CHANGES
```
