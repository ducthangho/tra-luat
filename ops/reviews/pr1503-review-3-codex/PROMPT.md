# Cross-review PR #1503 (ducthangho/tra-luat) — lượt 3, reviewer Codex

Lượt này VƯỢT trần mặc định 2 lời gọi Codex; chủ kho đã đồng ý nâng trần trong phiên điều phối
("Đồng ý nâng trần, chạy Codex review lượt 3", 24-11-2026). Ghi nhận ở verdict, không cần xét lại.

Bạn là reviewer độc lập. Thư mục làm việc là bản sao RỜI của kho, checkout detached đúng commit cần
review. Thứ định danh lượt là BĂM, không phải tên nhánh:

- reviewed_sha: `254d4e2d3c789c32a29d6769170e2c0615a32502`
- base_sha (merge-base với master): `2cbb552876c2f0dd6e957db7c2408112c7527127`
- Lượt 2 chấm `ec0722ad128e3439899ba210ee567142f5552b34`; verdict lượt 2 nằm trong cây:
  `ops/reviews/pr1503-review-2-codex/VERDICT.md` (N1–N8, REQUEST_CHANGES). Lượt 1:
  `ops/reviews/pr1503-review-1-codex/VERDICT.md` (F1–F12).
- Commit sau lượt 2 (`git log --oneline ec0722a..HEAD`):
  - `b2933c8` gỡ mục `anthropic` khỏi `ops/cong_cu.yaml` (CI đỏ vì runner không có SDK);
  - `11db814` vá N1–N8;
  - `39dd04e` gộp master;
  - `f351916` số lệnh ghim trong `scripts/tl_core/command_registry_test.py`;
  - `254d4e2` xếp `llm-order` + `llm-khai-niem` vào lớp GHI của `.claude/hooks/pretooluse_guard.py`
    và chuyển `llm-khai-niem` sang `read_only=False` trong `command_registry.py`.
- Diff toàn PR: `git diff 2cbb552876c2f0dd6e957db7c2408112c7527127 254d4e2d3c789c32a29d6769170e2c0615a32502`

Đọc `CLAUDE.md` ở gốc kho trước. Phần "PR này làm gì" ở `ops/reviews/pr1503-review-1-codex/PROMPT.md`.

## Việc của bạn

1. **Đối chiếu từng finding lượt 2 (N1–N8)** và các finding lượt 1 mà lượt 2 ghi VÁ MỘT PHẦN / VÁ SINH
   LỖI MỚI: ĐÃ VÁ THẬT / VÁ MỘT PHẦN / CHƯA VÁ / VÁ SINH LỖI MỚI, kèm bằng chứng chạy được.
2. **Tìm lỗi MỚI** do bản vá sinh ra. Đặc biệt:
   - `tach_khoan` / `lech_nguyen_van` (fail-closed): có nguồn "Giải thích từ ngữ" hợp lệ, phổ biến nào bị
     chặn oan không (đo trên dạng thật của văn bản luật Việt Nam: khoản đánh số `1.`, khoản không số, có
     điểm a) b), xuống dòng)? Có kết quả sai nào còn lọt?
   - `kiem_xac_thuc_sub` (`claude auth status --json`): tập `AUTH_SUBSCRIPTION`, cách gọi (env, cwd,
     timeout), hành vi khi CLI cũ không có lệnh `auth status`. Đối chiếu với `claude` đang cài.
   - Phân loại envelope `duong_sub` theo token đã chạy; `_usage_sub`; `phan_loai_loi_api` mã trước `type`.
   - `lay_dieu_qua_extract` + `_co_dieu` (CAP), handler `--out` giữ quyền, `--tep` BOM.
   - `pretooluse_guard.py` bảng `_TL_LENH_GHI`, metadata `read_only` của hai lệnh, golden liên quan.
   - `_do_anthropic_api` + `t162`.
3. **Test có răng không:** đột biến bản vá trên BẢN SAO TẠM, xác nhận ca đích đỏ đúng lý do.

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
# Verdict PR #1503 lượt 3 — Codex
reviewed_sha: 254d4e2d3c789c32a29d6769170e2c0615a32502
nang_tran: chủ kho đồng ý trong phiên điều phối (lượt thứ 3 > trần 2)
## Đối chiếu lượt 2 (và các mục lượt 1 còn mở)
| # | Trạng thái | Bằng chứng |
## Findings mới
### M1 [P?] <tiêu đề> — <tệp:dòng>
Kịch bản / Bằng chứng / Đề xuất
## Đã kiểm mà không thấy lỗi
## Không đo được
VERDICT: APPROVE | REQUEST_CHANGES
```

REQUEST_CHANGES nếu còn P0/P1 (mới hoặc chưa vá). Dòng `VERDICT:` cuối là bắt buộc.
