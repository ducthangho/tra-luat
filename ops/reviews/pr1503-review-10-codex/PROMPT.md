# Cross-review PR #1503 (ducthangho/tra-luat) — lượt 10, reviewer Codex

Lượt 9 chết giữa chừng (`ma_thoat` 1, verdict thiếu dòng `VERDICT:`) và chạm trần 9. Chủ kho quyết định vá V1 kèm
MỘT lượt Codex nữa, nâng trần lên 10 (comment PR 7136230652, 24-11-2026). Đây là lời gọi thứ 10, tức lời gọi CUỐI.

Bạn là reviewer độc lập. Thư mục làm việc là bản sao RỜI của kho, checkout detached đúng commit cần
review. Thứ định danh lượt là BĂM, không phải tên nhánh:

- reviewed_sha: `7bcb4bb3cb1bd4c6dc9f1321e848e78bd08d1fd1`
- base_sha (merge-base với master): `a03a28ef076503c7fe93c208a4998c32590a977f`
- Lượt 9 chấm `50d151899ae528e2a7e4dbc67288b092c0961cd5`; verdict (DỞ DANG) lượt 9 nằm trong cây:
  `ops/reviews/pr1503-review-9-codex/VERDICT.md` — đối chiếu U1–U3, một finding V1 (P1), không có dòng `VERDICT:`.
  Thiết kế hiện hành: mục "Thiết kế mới" của `ops/reviews/pr1503-review-6-codex/PROMPT.md`, mục "Thay đổi lượt
  này" của `ops/reviews/pr1503-review-8-codex/PROMPT.md` và `ops/reviews/pr1503-review-9-codex/PROMPT.md`, cộng
  thay đổi lượt này (dưới).
- Commit sau lượt 9: `1325e35` (chỉ lưu hồ sơ lượt 9), `7bcb4bb` (vá V1). Diff bản vá: `git diff 1325e35 7bcb4bb`.
- Diff toàn PR: `git diff a03a28ef076503c7fe93c208a4998c32590a977f 7bcb4bb3cb1bd4c6dc9f1321e848e78bd08d1fd1`

Đọc `CLAUDE.md` ở gốc kho trước. Phần "PR này làm gì" ở `ops/reviews/pr1503-review-1-codex/PROMPT.md`.

**Lưu ý môi trường:** sandbox của lượt trước để lại thư mục RỖNG `/tmp/.git`, làm 14 ca selftest
(`r973_bootstrap_*`, `wp433_*`, `wp727_tl_gws_refresh`) đỏ cả trên base lẫn head (bài học có sẵn trong `CLAUDE.md`).
So selftest với base để tách đỏ sẵn khỏi đỏ mới; đừng đọc 14 ca ấy thành hồi quy.

## Thay đổi lượt này (quyết định chủ kho — chấm việc THỰC HIỆN, không chấm lại quyết định)

- **V1**: DANH SÁCH CHO PHÉP kiểu dấu. `_dong_mo_ho` chỉ hiểu `(` `)` `"` `“` `”`; mọi ký tự thuộc nhóm Unicode
  Ps/Pe/Pi/Pf ngoài tập ấy, cùng vài dấu kép loại Po (`＂` `″` `‶` `＇`), làm dòng mơ hồ ⇒ `tach_khoan` từ chối CẢ
  nguồn. Vì cổng này chạy TRƯỚC mọi phân đoạn, `_quet` (chọn từ nối trong một khoản) chỉ còn gặp các dấu đã hiểu.

## Việc của bạn

1. **Đối chiếu V1** và các lớp lượt 9 kết luận (U1–U3 đóng; `phan-loai-sub`, `thu-hoi-tien-trinh-sub` đóng trong
   phạm vi đã đo): ĐÃ ĐÓNG / CÒN MỞ / SINH LỖI MỚI, kèm bằng chứng chạy được.
2. **Tìm lỗi MỚI** do `7bcb4bb`. Còn đường nào để một kết quả SAI (bỏ/gộp/cắt sai khoản) được nhận là nguyên văn?
   Còn đường nào gọi `api` sau khi `claude -p` đã khởi chạy?
3. **Test có răng không:** đột biến bản vá trên BẢN SAO TẠM, xác nhận ca đích đỏ đúng lý do.

Đây là lượt CUỐI. Nếu không còn P0/P1, hãy APPROVE. Chặn oan (fail-closed) là P2/P3, không phải P1. Các giới hạn
đã khai: khoản dùng từ nối khác "là" bị chặn; nguồn mất số có dòng gãy bị chặn; nguồn có số mà có dòng không số
lạ bị chặn; nguồn có dòng ngoặc/trích dẫn không khép trong dòng, dấu lẻ, trích dẫn lồng, hay BẤT KỲ kiểu dấu ngoặc/
trích dẫn ngoài danh sách cho phép bị chặn; tiêu đề Điều không có dấu `.`/`:` sau số bị coi như dòng thường; không
tự chuyển `api` khi hết hạn mức gói giữa chừng; không phân biệt hạn mức gói với extra usage; chặn khi nguồn chạm
CAP; Windows bản địa chưa đo. Ghi P2/P3 nếu có, kèm đề xuất.

**Ghi dòng `VERDICT:` SỚM**: khi đã đủ căn cứ, ghi dòng `VERDICT:` tạm vào cuối `.review/VERDICT.md` rồi mới đi
tiếp các phép đo phụ, cập nhật nó nếu kết luận đổi — lượt 9 chết trước khi kịp ghi dòng này.

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
# Verdict PR #1503 lượt 10 — Codex
reviewed_sha: 7bcb4bb3cb1bd4c6dc9f1321e848e78bd08d1fd1
nang_tran: chủ kho nâng trần lên 10 (lời gọi thứ 10, cuối cùng)
## Đối chiếu lượt 9 (và các lớp còn mở)
| # | Trạng thái | Bằng chứng |
## Findings mới
### W1 [P?] <tiêu đề> — <tệp:dòng>
Kịch bản / Bằng chứng / Đề xuất
## Đã kiểm mà không thấy lỗi
## Không đo được
VERDICT: APPROVE | REQUEST_CHANGES
```

REQUEST_CHANGES nếu còn P0/P1 (mới hoặc chưa vá). Dòng `VERDICT:` cuối là bắt buộc.
