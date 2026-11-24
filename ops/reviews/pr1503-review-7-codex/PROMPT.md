# Cross-review PR #1503 (ducthangho/tra-luat) — lượt 7, reviewer Codex

Lượt 6 chạm trần 6. Chủ kho quyết định vá S1–S3 kèm MỘT lượt Codex nữa, nâng trần lên 7 (comment PR
7134111088, 24-11-2026). Đây là lời gọi thứ 7, tức lời gọi CUỐI.

Bạn là reviewer độc lập. Thư mục làm việc là bản sao RỜI của kho, checkout detached đúng commit cần
review. Thứ định danh lượt là BĂM, không phải tên nhánh:

- reviewed_sha: `b5dc962aa77d9d56acacafda406f9aa1ab202c8d`
- base_sha (merge-base với master): `5259239d763c9ffc1677f033bd9a9cf23ede9299`
- Lượt 6 chấm `9af35ba16c9c096d6a42330d92c8ae8c2c6a5b1c`; verdict lượt 6 nằm trong cây:
  `ops/reviews/pr1503-review-6-codex/VERDICT.md` (S1–S3, REQUEST_CHANGES). Thiết kế hiện hành (quyết định
  chủ kho sau Rescue Checkpoint lượt 5) mô tả ở `ops/reviews/pr1503-review-6-codex/PROMPT.md` mục "Thiết kế mới".
  Các lượt trước ở `ops/reviews/pr1503-review-{1..5}-codex/`.
- Commit sau lượt 6: `2595a19` (chỉ lưu hồ sơ lượt 6), `b5dc962` (vá S1–S3). Diff bản vá: `git diff 9af35ba b5dc962`.
- Diff toàn PR: `git diff 5259239d763c9ffc1677f033bd9a9cf23ede9299 b5dc962aa77d9d56acacafda406f9aa1ab202c8d`

Đọc `CLAUDE.md` ở gốc kho trước. Phần "PR này làm gì" ở `ops/reviews/pr1503-review-1-codex/PROMPT.md`.

## Việc của bạn

1. **Đối chiếu S1–S3 và hai lớp còn mở** (`ranh-gioi-khoan`, `phan-loai-sub`) cùng `ghi-tep-local`: ĐÃ ĐÓNG /
   CÒN MỞ / SINH LỖI MỚI, kèm bằng chứng chạy được. Dùng lại các probe lượt 6 nếu cần.
2. **Tìm lỗi MỚI** do bản vá `b5dc962`. Đặc biệt:
   - `_chay_co_moc` / `KhongKhoiChay` / `duong_sub`: còn đường nào gọi `api` SAU khi `Popen` đã trả tiến trình?
     Lỗi trước mốc còn chuyển đúng? Tiến trình con có được giết + thu hồi khi quá hạn/lỗi đọc? `auth status`
     dùng cùng bộ chạy — có hồi quy?
   - `_quet` (ngoặc trong trích dẫn), `tach_khoan` (nguồn mất số không có tiếp dòng), `_RE_TIEU_DE_DIEU` chặt
     (dấu `.`/`:` sau số Điều — có làm hỏng tiêu đề thật nào, ví dụ đầu ra của `tl extract`?).
   - `_cung_dich` với quan hệ tổ tiên–hậu duệ.
3. **Test có răng không:** đột biến bản vá trên BẢN SAO TẠM, xác nhận ca đích đỏ đúng lý do.

Đây là lượt CUỐI. Nếu không còn P0/P1, hãy APPROVE. Đừng giữ REQUEST_CHANGES vì các giới hạn đã khai: khoản
dùng từ nối khác "là" bị chặn; nguồn mất số có dòng gãy bị chặn; nguồn có số mà có dòng không số lạ bị chặn;
tiêu đề Điều không có dấu `.`/`:` sau số bị coi như dòng thường (fail-closed); không tự chuyển `api` khi hết
hạn mức gói giữa chừng; không phân biệt hạn mức gói với extra usage; chặn khi nguồn chạm CAP. Ghi P2/P3 nếu
có, kèm đề xuất.

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
# Verdict PR #1503 lượt 7 — Codex
reviewed_sha: b5dc962aa77d9d56acacafda406f9aa1ab202c8d
nang_tran: chủ kho nâng trần lên 7 (lời gọi thứ 7, cuối cùng)
## Đối chiếu lượt 6 (và các lớp còn mở)
| # | Trạng thái | Bằng chứng |
## Findings mới
### T1 [P?] <tiêu đề> — <tệp:dòng>
Kịch bản / Bằng chứng / Đề xuất
## Đã kiểm mà không thấy lỗi
## Không đo được
VERDICT: APPROVE | REQUEST_CHANGES
```

REQUEST_CHANGES nếu còn P0/P1 (mới hoặc chưa vá). Dòng `VERDICT:` cuối là bắt buộc.
