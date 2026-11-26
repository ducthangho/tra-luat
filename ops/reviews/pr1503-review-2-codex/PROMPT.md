# Cross-review PR #1503 (ducthangho/tra-luat) — lượt 2, reviewer Codex

Bạn là reviewer độc lập. Thư mục làm việc là một bản sao RỜI của kho, checkout detached đúng commit
cần review. Thứ định danh lượt là BĂM, không phải tên nhánh:

- reviewed_sha: `ec0722ad128e3439899ba210ee567142f5552b34`
- base_sha (merge-base với master): `168d562b824db709ad88aa14f81d0ce3038cbfcb`
- Lượt 1 chấm `257beee354cf4861c2d2978d195dfebaf81904d0`; verdict lượt 1 nằm NGAY TRONG cây:
  `ops/reviews/pr1503-review-1-codex/VERDICT.md` (12 finding F1–F12, REQUEST_CHANGES).
- Bản vá cho lượt 1: commit `c3ba150` (`git show c3ba150`); `ec0722a` chỉ gộp thêm master
  (`git diff c3ba150 ec0722a` phải chỉ là các tệp của master: `.claude/dev/packet_loop*.py`,
  `docs/adr/0063-*`).
- Diff toàn PR: `git diff 168d562b824db709ad88aa14f81d0ce3038cbfcb ec0722ad128e3439899ba210ee567142f5552b34`

Đọc `CLAUDE.md` ở gốc kho trước (nhất là "Bài học đắt giá"). Mô tả PR và phạm vi giống lượt 1 —
đọc `ops/reviews/pr1503-review-1-codex/PROMPT.md` cho phần "PR này làm gì".

## Việc của bạn

1. **Đối chiếu từng finding lượt 1 (F1–F12):** ĐÃ VÁ THẬT / VÁ MỘT PHẦN / CHƯA VÁ / VÁ SINH LỖI MỚI,
   kèm bằng chứng chạy được (tái dùng probe lượt 1 nếu còn ý nghĩa — các probe cũ không còn trên đĩa,
   hãy dựng lại tối thiểu). Ghi rõ vì sao mỗi kết luận đứng được.
2. **Tìm lỗi MỚI** do bản vá sinh ra, đặc biệt:
   - `tach_khoan` / `lech_nguyen_van` (scripts/tl_core/llm_route.py): có văn bản "Giải thích từ ngữ"
     hợp lệ nào bị chặn oan (khoản nhiều dòng, khoản có điểm a) b), dòng không có " là ", số thứ tự
     kiểu khác, tiêu đề Điều có chữ cái `Điều 3a`)? Có kết quả sai nào còn lọt?
   - `kiem_dinh_tuyen_sub` + `CO_CLAUDE_CODE_VO_HAI`: danh sách cho phép có đúng với CLI đang cài không
     (`claude --version`, quét chuỗi `CLAUDE_CODE_USE_` trong binary)? Có đường nào khác khiến `claude -p`
     tính tiền ngoài subscription mà chốt bỏ sót (biến khác, tệp cấu hình nằm ngoài `--setting-sources ""`)?
     Mô tả bằng lời nếu cần nội dung tấn công.
   - Phân loại subtype/`is_error` ở `duong_sub`, các mã 503/529/504 ở `phan_loai_loi_api`.
   - Handler `cmd_llm_khai_niem` / `cmd_llm_order` (scripts/tl_core/ops_misc.py): `--out` nguyên tử,
     `--config`/`--profile`, `--tep` + `--dieu`, mã thoát.
   - `_do_anthropic_api` (.claude/dev/launcher.py) và ca `t162`.
3. **Test có răng không:** đột biến bản vá trên BẢN SAO TẠM và xem ca đích đỏ đúng lý do.

## Cách đo (không cần mạng)

```
python scripts/tl_core/llm_route_test.py
python .claude/dev/launcher_test.py --lap-ca t162 --lan 1
python scripts/tl.py --deterministic workflow-audit --strict --json
python scripts/tl.py --deterministic golden-test --json
python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
python scripts/tl.py --selftest        # ~6 phút; so với base để tách đỏ sẵn khỏi đỏ mới
```

## Ràng buộc

- KHÔNG gọi Claude/Anthropic API thật, KHÔNG chạy `claude -p` thật, KHÔNG chạy `tl llm-khai-niem` mà
  không có đồ giả. Không đọc/in giá trị biến bí mật.
- KHÔNG push, KHÔNG gọi GitHub, KHÔNG sửa tệp đã theo dõi trong cây.
- Hướng thử cần tự soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI.

## Đầu ra

Ghi TĂNG DẦN vào `.review/VERDICT.md` dưới thư mục làm việc:

```
# Verdict PR #1503 lượt 2 — Codex
reviewed_sha: ec0722ad128e3439899ba210ee567142f5552b34
## Đối chiếu lượt 1
| # | Trạng thái | Bằng chứng |
## Findings mới
### N1 [P?] <tiêu đề> — <tệp:dòng>
Kịch bản / Bằng chứng / Đề xuất
## Đã kiểm mà không thấy lỗi
## Không đo được
VERDICT: APPROVE | REQUEST_CHANGES
```

REQUEST_CHANGES nếu còn P0/P1 (mới hoặc chưa vá). Dòng `VERDICT:` cuối là bắt buộc.
