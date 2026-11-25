# Cross-review packet #1514 LLM-RANH-GIOI-KHOAN r1 (PR #1517, ducthangho/tra-luat) — lượt 2, reviewer Codex

Lời gọi Codex thứ 2 trong trần 5. Lượt 1 dừng ở preflight vì lease khai sai bề mặt reviewer (`codex_service`); commit `53c49ab` sửa thành `codex_cli` — bề mặt THẬT của lượt này (`codex exec` qua `.claude/dev/launcher.py run`). Hồ sơ lượt 1: `ops/acceptance/llm-ranh-gioi-khoan/r1/review-1-codex/` (lease `ops/leases/llm-ranh-gioi-khoan-r1-g1-claude.yaml`, `review_calls_limit: 5`).

Bạn là reviewer độc lập. Thư mục làm việc là bản sao RỜI của kho, checkout detached đúng commit cần review:

- reviewed_sha: `53c49ab125290b0a937c60aefe5481201b42cd4e`
- base_sha: `64b7f2c14776d5d0e1d34a6be4725490956f5bec` (master)
- Đặc tả đóng băng: `ops/specs/llm-ranh-gioi-khoan-r1.md` — kiểm sha256 khớp `spec_hash` trong lease
  `ops/leases/llm-ranh-gioi-khoan-r1-g1-claude.yaml` trước khi review.
- Diff: `git diff 64b7f2c 53c49ab`. Ngữ cảnh: nợ #1512 từ PR #1503; verdict lượt 11 của PR ấy ở
  `ops/reviews/pr1503-review-11-codex/VERDICT.md` (X2, X3, X4).

Đọc `CLAUDE.md` ở gốc kho trước.

## PHẠM VI — lượt KIỂM CHỨNG

Các lượt review gần đây của mảng này từng bị nền từ chối phản hồi khi reviewer tự dựng nội dung thử nghiệm mới. Lượt này chỉ:
1. **Đối chiếu đặc tả**: mỗi mục §2 (X2, X3b/X3c, X3, X4) và §4 (test) đã được thực hiện đúng chưa; write set có đúng lease không.
2. **Chạy** các bộ test có sẵn (mục "Cách đo") và báo số đạt/tổng.
3. **Đột biến bản vá** trên BẢN SAO TẠM: dùng bảng `DOT_BIEN` có sẵn (bộ test tự chạy) và, nếu muốn, sửa vài dòng của chính bản vá
   (`_ket_thuc_cau`, `_RE_CAU_DAN`, `_DAU_CAU_KET`, nhánh `ln.count('"') >= 3`, `_gon`) để xác nhận ca đích đỏ đúng lý do.
4. **Đọc mã** `scripts/tl_core/llm_route.py` (`tach_khoan`, `_ket_thuc_cau`, `_dong_mo_ho`, `_gon`, `lech_nguyen_van`) và mô tả
   nghi vấn **bằng lời**: dạng văn bản nguồn nào làm hỏng và vì sao. KHÔNG viết thêm tệp thử nghiệm, chuỗi thử nghiệm hay script dò
   mới; điều chỉ kiểm được bằng thử nghiệm mới thì ghi vào "Không đo được".

## Câu hỏi cần trả lời
- Bốn chốt có làm đúng như đặc tả? Có chốt nào đặt sai chỗ làm nó không có tác dụng (vd bị chốt khác che)?
- Còn đường nào để một kết quả SAI (bỏ/gộp/cắt sai khoản) được nhận là nguyên văn, theo đọc mã?
- Có dạng "Giải thích từ ngữ" phổ biến nào bị chặn oan mà đặc tả KHÔNG khai là giới hạn? (Chặn oan là P2/P3.)
- Test có răng không?

APPROVE nếu không còn P0/P1. Giới hạn đã khai (không tính là P1): `can_nguoi_duyet: true` giữ nguyên; dòng có hai cụm `"…"` độc lập
bị chặn; khoản không kết thúc bằng `.` `;` `!` `?` bị chặn; câu dẫn không theo mẫu chuẩn không được bỏ; mọi giới hạn đã khai ở
`docs/GOI_AGENT_DA_NEN.md` mục script gọi Claude.

**Ghi dòng `VERDICT:` SỚM** (tạm), cập nhật nếu kết luận đổi.

## Cách đo (không cần mạng)

```
python scripts/tl_core/llm_route_test.py
python scripts/tl.py --deterministic workflow-audit --strict --json
python scripts/tl.py --deterministic golden-test --json
python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
python ops/lease_publish.py check --root . ops/leases/llm-ranh-gioi-khoan-r1-g1-claude.yaml
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
# Verdict packet #1514 r1 lượt 2 — Codex
reviewed_sha: 53c49ab125290b0a937c60aefe5481201b42cd4e
## Đối chiếu đặc tả
| Mục | Trạng thái | Bằng chứng |
## Findings
### A1 [P?] <tiêu đề> — <tệp:dòng>
Kịch bản (bằng lời) / Căn cứ / Đề xuất
## Kết quả test và đột biến
## Không đo được
VERDICT: APPROVE | REQUEST_CHANGES
```
