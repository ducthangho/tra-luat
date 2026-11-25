# Cross-review PR #1503 (ducthangho/tra-luat) — lượt 5, reviewer Codex

Trần lời gọi Codex của PR này đã được chủ kho nâng lên 5 (comment PR 7131878592, 24-11-2026). Đây là lời
gọi thứ 5, tức lời gọi CUỐI trong trần. Ghi nhận ở verdict, không cần xét lại.

Bạn là reviewer độc lập. Thư mục làm việc là bản sao RỜI của kho, checkout detached đúng commit cần
review. Thứ định danh lượt là BĂM, không phải tên nhánh:

- reviewed_sha: `9b4e0aa6ad48d361c91a76e18e12dd7c87ac9458`
- base_sha (merge-base với master): `5259239d763c9ffc1677f033bd9a9cf23ede9299`
- Lượt 4 chấm `82e46a319580c69b341270fdc75c4b709f960189`; verdict lượt 4 nằm trong cây:
  `ops/reviews/pr1503-review-4-codex/VERDICT.md` (Q1–Q5, REQUEST_CHANGES). Các lượt trước ở
  `ops/reviews/pr1503-review-{1,2,3}-codex/`.
- Commit sau lượt 4: `9b4e0aa` (vá Q1–Q5 + lưu hồ sơ review lượt 4). Diff bản vá: `git diff 82e46a3 9b4e0aa`.
- Diff toàn PR: `git diff 5259239d763c9ffc1677f033bd9a9cf23ede9299 9b4e0aa6ad48d361c91a76e18e12dd7c87ac9458`

Đọc `CLAUDE.md` ở gốc kho trước. Phần "PR này làm gì" ở `ops/reviews/pr1503-review-1-codex/PROMPT.md`.

## Việc của bạn

1. **Đối chiếu từng finding lượt 4 (Q1–Q5)** và bốn "lớp nguyên nhân còn mở" mà lượt 4 liệt kê
   (`ranh-gioi-khoan`, `phan-loai-sub`, `bang-chung-doctor`, `ghi-tep-local`): ĐÃ VÁ THẬT / VÁ MỘT PHẦN /
   CHƯA VÁ / VÁ SINH LỖI MỚI, kèm bằng chứng chạy được. Dùng lại các phép thử lượt 4 nếu cần.
2. **Tìm lỗi MỚI** do bản vá `9b4e0aa` sinh ra. Đặc biệt:
   - `_tu_noi` / `_dang_mo` / `_la_tiep_dong` / `tach_khoan` / `lech_nguyen_van`: ngoặc kép thẳng/cong,
     dấu `:` trước từ nối, dừng ở dòng điểm, tiếp dòng mở bằng "là", ngoặc trải nhiều dòng. Có kết quả SAI nào
     còn lọt? Có dạng "Giải thích từ ngữ" hợp lệ, phổ biến nào bị chặn oan? Kiểm cả nguồn mất số (Google Doc).
   - `_dau_model_da_chay` + nhánh `is_error is not True` trong `duong_sub`: còn đường nào gọi `api` khi chưa
     có bằng chứng dương rằng model chưa chạy? Có ca hạn mức/xác thực thật nào nay bị chặn oan?
   - `_do_anthropic_api` + `t162`: khung Message, khối nội dung, token dương.
   - Handler `--nhat-ky`: kiểm trước model, lỗi I/O muộn.
3. **Test có răng không:** đột biến bản vá trên BẢN SAO TẠM, xác nhận ca đích đỏ đúng lý do.

Đây là lượt cuối trong trần. Nếu Q1–Q5 đã vá thật và không còn P0/P1, hãy APPROVE — đừng giữ
REQUEST_CHANGES vì các giới hạn đã khai (khoản dùng từ nối khác "là" bị chặn; nguồn mất số có dòng tiếp
không chứa từ nối bị chặn; không phân biệt hạn mức gói với extra usage; chặn khi nguồn chạm CAP). Ghi P2/P3
nếu có, kèm đề xuất.

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
# Verdict PR #1503 lượt 5 — Codex
reviewed_sha: 9b4e0aa6ad48d361c91a76e18e12dd7c87ac9458
nang_tran: chủ kho nâng trần lên 5 (lời gọi thứ 5, cuối cùng)
## Đối chiếu lượt 4 (và các lớp còn mở)
| # | Trạng thái | Bằng chứng |
## Findings mới
### R1 [P?] <tiêu đề> — <tệp:dòng>
Kịch bản / Bằng chứng / Đề xuất
## Đã kiểm mà không thấy lỗi
## Không đo được
VERDICT: APPROVE | REQUEST_CHANGES
```

REQUEST_CHANGES nếu còn P0/P1 (mới hoặc chưa vá). Dòng `VERDICT:` cuối là bắt buộc.
