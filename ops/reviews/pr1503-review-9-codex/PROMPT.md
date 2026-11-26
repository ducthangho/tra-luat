# Cross-review PR #1503 (ducthangho/tra-luat) — lượt 9, reviewer Codex

Lượt 8 chạm trần 8. Chủ kho quyết định CHẶN MỌI NGUỒN MƠ HỒ kèm MỘT lượt Codex nữa, nâng trần lên 9 (comment PR
7135632032, 24-11-2026). Đây là lời gọi thứ 9, tức lời gọi CUỐI.

Bạn là reviewer độc lập. Thư mục làm việc là bản sao RỜI của kho, checkout detached đúng commit cần
review. Thứ định danh lượt là BĂM, không phải tên nhánh:

- reviewed_sha: `50d151899ae528e2a7e4dbc67288b092c0961cd5`
- base_sha (merge-base với master): `a03a28ef076503c7fe93c208a4998c32590a977f`
- Lượt 8 chấm `a93b8f3069cd845468545fa79c501a2a6a1782f0`; verdict lượt 8 nằm trong cây:
  `ops/reviews/pr1503-review-8-codex/VERDICT.md` (U1 P1, U2 P2, U3 P1, REQUEST_CHANGES). Thiết kế hiện hành: mục
  "Thiết kế mới" của `ops/reviews/pr1503-review-6-codex/PROMPT.md`, mục "Thay đổi lượt này" của
  `ops/reviews/pr1503-review-8-codex/PROMPT.md`, cộng thay đổi lượt này (dưới).
- Commit sau lượt 8: `f681b75` (chỉ lưu hồ sơ lượt 8), `50d1518` (vá U1–U3). Diff bản vá: `git diff a93b8f3 50d1518`.
- Diff toàn PR: `git diff a03a28ef076503c7fe93c208a4998c32590a977f 50d151899ae528e2a7e4dbc67288b092c0961cd5`

Đọc `CLAUDE.md` ở gốc kho trước. Phần "PR này làm gì" ở `ops/reviews/pr1503-review-1-codex/PROMPT.md`.

## Thay đổi lượt này (quyết định chủ kho — chấm việc THỰC HIỆN, không chấm lại quyết định)

- **U1/U3**: `tach_khoan` từ chối CẢ nguồn khi BẤT KỲ dòng nào (sau khi `_bo_dau_dong` bỏ dấu số khoản `1.`/`1)`/
  `(1)` hoặc dấu điểm `a)`/`-` ở đầu dòng) mà `_dong_mo_ho` báo mơ hồ: ngoặc tròn hay trích dẫn không khép trong
  dòng, `)` hoặc `”` lẻ, hoặc trích dẫn cong lồng cùng kiểu. Chốt bảo thủ: chặn oan được, nhận nhầm thì không.
- **U2**: `_chay_co_moc` khi lỗi sau khởi chạy: kill → `wait(timeout=5)` → (chỉ ngoài Windows) đóng pipe.

## Việc của bạn

1. **Đối chiếu U1–U3 và lớp `ranh-gioi-khoan`, `thu-hoi-tien-trinh-sub`**: ĐÃ ĐÓNG / CÒN MỞ / SINH LỖI MỚI, kèm
   bằng chứng chạy được. Dùng lại các probe lượt 8 nếu cần.
2. **Tìm lỗi MỚI** do `50d1518`. Còn đường nào để một kết quả SAI (bỏ/gộp/cắt sai khoản) được nhận là nguyên văn?
   Còn đường nào gọi `api` sau khi `claude -p` đã khởi chạy?
3. **Test có răng không:** đột biến bản vá trên BẢN SAO TẠM, xác nhận ca đích đỏ đúng lý do.

Đây là lượt CUỐI. Nếu không còn P0/P1, hãy APPROVE. Chặn oan (fail-closed) là P2/P3, không phải P1. Các giới hạn
đã khai: khoản dùng từ nối khác "là" bị chặn; nguồn mất số có dòng gãy bị chặn; nguồn có số mà có dòng không số
lạ bị chặn; nguồn có dòng ngoặc/trích dẫn không khép trong dòng, dấu lẻ hay trích dẫn lồng bị chặn; tiêu đề Điều
không có dấu `.`/`:` sau số bị coi như dòng thường; không tự chuyển `api` khi hết hạn mức gói giữa chừng; không
phân biệt hạn mức gói với extra usage; chặn khi nguồn chạm CAP. Ghi P2/P3 nếu có, kèm đề xuất.

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
# Verdict PR #1503 lượt 9 — Codex
reviewed_sha: 50d151899ae528e2a7e4dbc67288b092c0961cd5
nang_tran: chủ kho nâng trần lên 9 (lời gọi thứ 9, cuối cùng)
## Đối chiếu lượt 8 (và các lớp còn mở)
| # | Trạng thái | Bằng chứng |
## Findings mới
### V1 [P?] <tiêu đề> — <tệp:dòng>
Kịch bản / Bằng chứng / Đề xuất
## Đã kiểm mà không thấy lỗi
## Không đo được
VERDICT: APPROVE | REQUEST_CHANGES
```

REQUEST_CHANGES nếu còn P0/P1 (mới hoặc chưa vá). Dòng `VERDICT:` cuối là bắt buộc.
