# Cross-review PR #1503 (ducthangho/tra-luat) — lượt 6, reviewer Codex

Lượt 5 chạm trần 5 lời gọi ⇒ Review Rescue Checkpoint. Chủ kho quyết định ĐỔI THIẾT KẾ kèm MỘT lượt Codex
nữa, nâng trần lên 6 (comment PR 7132839836, 24-11-2026). Đây là lời gọi thứ 6, tức lời gọi CUỐI.

Bạn là reviewer độc lập. Thư mục làm việc là bản sao RỜI của kho, checkout detached đúng commit cần
review. Thứ định danh lượt là BĂM, không phải tên nhánh:

- reviewed_sha: `9af35ba16c9c096d6a42330d92c8ae8c2c6a5b1c`
- base_sha (merge-base với master): `5259239d763c9ffc1677f033bd9a9cf23ede9299`
- Lượt 5 chấm `9b4e0aa6ad48d361c91a76e18e12dd7c87ac9458`; verdict lượt 5 nằm trong cây:
  `ops/reviews/pr1503-review-5-codex/VERDICT.md` (R1–R5, REQUEST_CHANGES, 4 lớp nguyên nhân còn mở).
  Các lượt trước ở `ops/reviews/pr1503-review-{1,2,3,4}-codex/`.
- Commit sau lượt 5: `6f843b5` (chỉ lưu hồ sơ lượt 5), `9af35ba` (đổi thiết kế + vá R1–R5).
  Diff bản vá: `git diff 9b4e0aa 9af35ba`.
- Diff toàn PR: `git diff 5259239d763c9ffc1677f033bd9a9cf23ede9299 9af35ba16c9c096d6a42330d92c8ae8c2c6a5b1c`

Đọc `CLAUDE.md` ở gốc kho trước. Phần "PR này làm gì" ở `ops/reviews/pr1503-review-1-codex/PROMPT.md`.

## Thiết kế mới (quyết định của chủ kho — chấm việc THỰC HIỆN, không chấm lại quyết định)

1. **Chuyển đường `sub` → `api`**: CHỈ khi lỗi xảy ra TRƯỚC lúc `claude -p` khởi chạy (thiếu CLI, định
   tuyến `CLAUDE_CODE_USE_*`/`ANTHROPIC_BASE_URL`, `auth status` không phải subscription, spawn hỏng).
   Đã khởi chạy thì MỌI lỗi (quá hạn, mất envelope, envelope lỗi, kể cả hết hạn mức gói) ⇒ DỪNG, gợi ý chạy
   lại với `--thu-tu api`. Phép đoán "model đã chạy chưa" từ envelope đã bị BỎ.
2. **Ranh giới khoản theo CẤU TRÚC dòng**, không đoán theo chữ "là":
   - nguồn CÓ số: số khoản phải liên tục từ 1; dòng không số chỉ được nhận khi là điểm (`a)`, `-`) hoặc tiếp
     dòng có bằng chứng (khoản đang mở còn trong ngoặc/trích dẫn; hoặc dòng mở bằng "là" khi khoản đang mở
     CHƯA có từ nối); mọi dòng khác ⇒ nguồn mơ hồ, chặn;
   - nguồn MẤT số (Google Doc — Điều 3 Luật 134/2025/QH15 lấy qua `extract` không có số khoản): MỖI DÒNG là
     một khoản. Đây là chỉnh so với phương án ban đầu "chặn mọi nguồn mất số", vì nếu chặn thì ca dùng chính
     không chạy được.
   - Tách thuật ngữ/định nghĩa trong một khoản vẫn tại chữ "là" đầu tiên ngoài ngoặc/trích dẫn, ở phần đầu
     khoản, không sau dấu `:` ngoài ngoặc — nay bằng bộ quét có trạng thái `_quet`.

## Việc của bạn

1. **Đối chiếu R1–R5 và bốn lớp nguyên nhân còn mở** (`ranh-gioi-khoan`, `phan-loai-sub`,
   `bang-chung-doctor`, `ghi-tep-local`): ĐÃ ĐÓNG / CÒN MỞ / SINH LỖI MỚI, kèm bằng chứng chạy được. Dùng lại các
   phép thử lượt 5 nếu cần.
2. **Tìm lỗi MỚI** do bản đổi thiết kế. Đặc biệt:
   - `tach_khoan` / `_quet` / `_dang_mo` / `_tu_noi` / `lech_nguyen_van`: còn kết quả SAI nào được nhận (nhận
     nhầm là điều cần chặn nhất)? Ở nguồn mất số, có cách nào một khoản bị gộp/tách sai mà vẫn đạt?
   - `duong_sub` / `goi`: còn đường nào gọi `api` SAU khi `claude -p` đã khởi chạy? Lỗi trước khởi chạy còn
     chuyển đúng không?
   - `_do_anthropic_api` + `t162`; handler `--out`/`--nhat-ky`.
3. **Test có răng không:** đột biến bản vá trên BẢN SAO TẠM, xác nhận ca đích đỏ đúng lý do.

Đây là lượt CUỐI. Nếu hai lớp P1 đã đóng bằng thiết kế và không còn P0/P1, hãy APPROVE. Đừng giữ
REQUEST_CHANGES vì các giới hạn đã khai: khoản dùng từ nối khác "là" bị chặn; nguồn mất số có dòng gãy giữa câu
bị chặn; nguồn có số mà có dòng không số lạ bị chặn; không tự chuyển `api` khi hết hạn mức gói giữa chừng; không
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
# Verdict PR #1503 lượt 6 — Codex
reviewed_sha: 9af35ba16c9c096d6a42330d92c8ae8c2c6a5b1c
nang_tran: chủ kho nâng trần lên 6 sau Rescue Checkpoint (lời gọi thứ 6, cuối cùng)
## Đối chiếu lượt 5 (và các lớp còn mở)
| # | Trạng thái | Bằng chứng |
## Findings mới
### S1 [P?] <tiêu đề> — <tệp:dòng>
Kịch bản / Bằng chứng / Đề xuất
## Đã kiểm mà không thấy lỗi
## Không đo được
VERDICT: APPROVE | REQUEST_CHANGES
```

REQUEST_CHANGES nếu còn P0/P1 (mới hoặc chưa vá). Dòng `VERDICT:` cuối là bắt buộc.
