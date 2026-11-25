# Cross-review PR #1503 (ducthangho/tra-luat) — lượt 4, reviewer Codex

Trần lời gọi Codex của PR này đã được chủ kho nâng lên 5 (comment PR 7131878592, 24-11-2026). Đây là lời
gọi thứ 4. Ghi nhận ở verdict, không cần xét lại.

Bạn là reviewer độc lập. Thư mục làm việc là bản sao RỜI của kho, checkout detached đúng commit cần
review. Thứ định danh lượt là BĂM, không phải tên nhánh:

- reviewed_sha: `82e46a319580c69b341270fdc75c4b709f960189`
- base_sha (merge-base với master): `5259239d763c9ffc1677f033bd9a9cf23ede9299`
- Lượt 3 chấm `254d4e2d3c789c32a29d6769170e2c0615a32502`; verdict lượt 3 nằm trong cây:
  `ops/reviews/pr1503-review-3-codex/VERDICT.md` (M1–M7, REQUEST_CHANGES). Lượt 1, 2 ở
  `ops/reviews/pr1503-review-1-codex/` và `-review-2-codex/`.
- Commit sau lượt 3: `7c826ae` (vá M1–M7 + lưu hồ sơ review), `82e46a3` (gộp master, không chạm tệp của PR).
  Diff bản vá: `git diff 254d4e2 7c826ae`.
- Diff toàn PR: `git diff 5259239d763c9ffc1677f033bd9a9cf23ede9299 82e46a319580c69b341270fdc75c4b709f960189`

Đọc `CLAUDE.md` ở gốc kho trước. Phần "PR này làm gì" ở `ops/reviews/pr1503-review-1-codex/PROMPT.md`.

## Việc của bạn

1. **Đối chiếu từng finding lượt 3 (M1–M7)** và các mục lượt 1/2 mà lượt 3 còn ghi VÁ MỘT PHẦN / VÁ SINH
   LỖI MỚI: ĐÃ VÁ THẬT / VÁ MỘT PHẦN / CHƯA VÁ / VÁ SINH LỖI MỚI, kèm bằng chứng chạy được.
2. **Tìm lỗi MỚI** do bản vá `7c826ae` sinh ra. Đặc biệt:
   - `tach_khoan` / `_la_ngoai_ngoac` / `lech_nguyen_van`: tách tại "là" đầu tiên ngoài ngoặc, so theo vị
     trí. Có dạng "Giải thích từ ngữ" hợp lệ, phổ biến nào bị chặn oan (ngoặc lồng, ngoặc kép, "là" trong
     từ ghép như "làm", khoản có điểm a) b))? Có kết quả SAI nào còn lọt (nhận nhầm là điều cần chặn nhất)?
   - `_dau_model_da_chay` / `_usage_sub`: ba trạng thái True/False/None; envelope thiếu/sai kiểu.
   - `kiem_xac_thuc_sub`: `--setting-sources ""` trước `auth status`; CLI cũ không nhận cờ đó thì sao.
   - `lay_dieu_qua_extract`: CAP luôn chặn, đọc một lần.
   - Handler: `_cung_dich` (`--out` vs `--nhat-ky`, symlink, hardlink, đường dẫn tương đối), ghi nguyên tử.
   - `_do_anthropic_api` khung Message + `t162`.
3. **Test có răng không:** đột biến bản vá trên BẢN SAO TẠM, xác nhận ca đích đỏ đúng lý do.

Nếu M1–M7 đã vá thật và không còn P0/P1, hãy APPROVE — đừng giữ REQUEST_CHANGES vì các giới hạn đã khai
(ví dụ khoản dùng từ nối khác "là" bị chặn; không phân biệt hạn mức gói với extra usage). Ghi P2/P3 nếu có.

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
# Verdict PR #1503 lượt 4 — Codex
reviewed_sha: 82e46a319580c69b341270fdc75c4b709f960189
nang_tran: chủ kho nâng trần lên 5 (lời gọi thứ 4)
## Đối chiếu lượt 3 (và các mục còn mở)
| # | Trạng thái | Bằng chứng |
## Findings mới
### Q1 [P?] <tiêu đề> — <tệp:dòng>
Kịch bản / Bằng chứng / Đề xuất
## Đã kiểm mà không thấy lỗi
## Không đo được
VERDICT: APPROVE | REQUEST_CHANGES
```

REQUEST_CHANGES nếu còn P0/P1 (mới hoặc chưa vá). Dòng `VERDICT:` cuối là bắt buộc.
