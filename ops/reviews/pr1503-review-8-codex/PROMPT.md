# Cross-review PR #1503 (ducthangho/tra-luat) — lượt 8, reviewer Codex

Lượt 7 chạm trần 7. Chủ kho quyết định đóng T1/T2 BẰNG THIẾT KẾ kèm MỘT lượt Codex nữa, nâng trần lên 8
(comment PR 7134926594, 24-11-2026). Đây là lời gọi thứ 8, tức lời gọi CUỐI.

Bạn là reviewer độc lập. Thư mục làm việc là bản sao RỜI của kho, checkout detached đúng commit cần
review. Thứ định danh lượt là BĂM, không phải tên nhánh:

- reviewed_sha: `a93b8f3069cd845468545fa79c501a2a6a1782f0`
- base_sha (merge-base với master): `a03a28ef076503c7fe93c208a4998c32590a977f`
- Lượt 7 chấm `b5dc962aa77d9d56acacafda406f9aa1ab202c8d`; verdict lượt 7 nằm trong cây:
  `ops/reviews/pr1503-review-7-codex/VERDICT.md` (T1 P1, T2 P2, REQUEST_CHANGES). Thiết kế hiện hành mô tả ở
  `ops/reviews/pr1503-review-6-codex/PROMPT.md` mục "Thiết kế mới", cộng thay đổi lượt này (dưới).
  Các lượt trước ở `ops/reviews/pr1503-review-{1..6}-codex/`.
- Commit sau lượt 7: `29611a8` (chỉ lưu hồ sơ lượt 7), `fcd8e08` (đóng T1/T2), `a93b8f3` (gộp master: PR #1510
  chỉ chạm `.claude/dev/launcher.py` + `launcher_test.py`, phần ACL Codex trên Windows — ngoài phạm vi PR này).
  Diff bản vá: `git diff b5dc962 fcd8e08`.
- Diff toàn PR: `git diff a03a28ef076503c7fe93c208a4998c32590a977f a93b8f3069cd845468545fa79c501a2a6a1782f0`

Đọc `CLAUDE.md` ở gốc kho trước. Phần "PR này làm gì" ở `ops/reviews/pr1503-review-1-codex/PROMPT.md`.

## Thay đổi lượt này (quyết định chủ kho — chấm việc THỰC HIỆN, không chấm lại quyết định)

- **T1**: ở nguồn có số, tiếp dòng KHÔNG còn dựa vào trạng thái ngoặc/trích dẫn. Dòng không số chỉ được nối khi là
  điểm (`a)`, `-`) hoặc mở bằng "là" sau một thuật ngữ chưa có từ nối; mọi dòng khác ⇒ nguồn mơ hồ, chặn. Ngoặc
  trải nhiều dòng bị chặn — giới hạn đã khai. `_dang_mo` đã bỏ. Bộ quét `_quet` (chỉ còn dùng để chọn từ nối trong
  MỘT khoản) giữ đúng một cụm trích dẫn đang mở; ký tự bên trong là nội dung.
- **T2**: `_chay_co_moc` khi lỗi sau khởi chạy: kill, đóng pipe, `wait(timeout=5)` — không đọc lại.

## Việc của bạn

1. **Đối chiếu T1, T2 và lớp `ranh-gioi-khoan`, `thu-hoi-tien-trinh-sub`**: ĐÃ ĐÓNG / CÒN MỞ / SINH LỖI MỚI,
   kèm bằng chứng chạy được. Dùng lại các probe lượt 7 nếu cần.
2. **Tìm lỗi MỚI** do `fcd8e08`. Còn đường nào để một kết quả SAI (bỏ/gộp/cắt sai khoản) được nhận là nguyên văn?
   Còn đường nào gọi `api` sau khi `claude -p` đã khởi chạy?
3. **Test có răng không:** đột biến bản vá trên BẢN SAO TẠM, xác nhận ca đích đỏ đúng lý do.

Đây là lượt CUỐI. Nếu không còn P0/P1, hãy APPROVE. Đừng giữ REQUEST_CHANGES vì các giới hạn đã khai: khoản
dùng từ nối khác "là" bị chặn; nguồn mất số có dòng gãy bị chặn; nguồn có số mà có dòng không số lạ, hay ngoặc/
trích dẫn trải nhiều dòng, bị chặn; tiêu đề Điều không có dấu `.`/`:` sau số bị coi như dòng thường; không tự
chuyển `api` khi hết hạn mức gói giữa chừng; không phân biệt hạn mức gói với extra usage; chặn khi nguồn chạm CAP.
Chặn oan (fail-closed) là P2/P3, không phải P1. Ghi P2/P3 nếu có, kèm đề xuất.

## Cách đo (không cần mạng)

```
python scripts/tl_core/llm_route_test.py
python .claude/dev/launcher_test.py --lap-ca t162 --lan 1
python .claude/hooks/pretooluse_guard.py --kiem-bang
python scripts/tl_core/command_registry_test.py
python scripts/tl.py --deterministic workflow-audit --strict --json
python scripts/tl.py --deterministic golden-test --json
python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
python scripts/tl.py --selftest        # ~6 phút; so với base để tách đỏ sẵn khỏi đỏ mới
```

## Ràng buộc

- KHÔNG gọi Claude/Anthropic API thật, KHÔNG chạy `claude -p` thật, KHÔNG chạy `tl llm-khai-niem` mà
  không có đồ giả. `claude auth status --json` chỉ đọc trạng thái cục bộ — được phép chạy để đối chiếu.
  Không đọc/in giá trị biến bí mật.
- KHÔNG push, KHÔNG gọi GitHub, KHÔNG sửa tệp đã theo dõi trong cây.
- Hướng thử cần tự soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI.

## Đầu ra

Ghi TĂNG DẦN vào `.review/VERDICT.md` dưới thư mục làm việc:

```
# Verdict PR #1503 lượt 8 — Codex
reviewed_sha: a93b8f3069cd845468545fa79c501a2a6a1782f0
nang_tran: chủ kho nâng trần lên 8 (lời gọi thứ 8, cuối cùng)
## Đối chiếu lượt 7 (và các lớp còn mở)
| # | Trạng thái | Bằng chứng |
## Findings mới
### U1 [P?] <tiêu đề> — <tệp:dòng>
Kịch bản / Bằng chứng / Đề xuất
## Đã kiểm mà không thấy lỗi
## Không đo được
VERDICT: APPROVE | REQUEST_CHANGES
```

REQUEST_CHANGES nếu còn P0/P1 (mới hoặc chưa vá). Dòng `VERDICT:` cuối là bắt buộc.
