# Cross-review PR #1503 (ducthangho/tra-luat) — lượt 11, reviewer Codex (kiểm chứng, không dò tấn công)

Lượt 9 và lượt 10 dừng giữa chừng vì nền từ chối phản hồi khi reviewer tự dựng nội dung thử nghiệm mới. Chủ kho
nâng trần lên 11 và ĐỔI CÁCH GIAO VIỆC (comment PR 7136813807, 24-11-2026). Đây là lời gọi thứ 11, tức lời gọi CUỐI.

Bạn là reviewer độc lập. Thư mục làm việc là bản sao RỜI của kho, checkout detached đúng commit cần review:

- reviewed_sha: `74fbf22a113e40cfa75d75e8ceaf6a3fd988d388` (mã giống `7bcb4bb`; `74fbf22` chỉ thêm hồ sơ review)
- base_sha (merge-base với master): `a03a28ef076503c7fe93c208a4998c32590a977f`
- Hồ sơ các lượt trước: `ops/reviews/pr1503-review-{1..10}-codex/`. Lượt 8 có verdict đầy đủ cuối cùng (U1–U3);
  lượt 9 dở dang nhưng đã ghi U1–U3 ĐÃ ĐÓNG và một finding V1; lượt 10 không có verdict.
- Bản vá V1: `git diff 1325e35 7bcb4bb`. Diff toàn PR: `git diff a03a28e 74fbf22`.

Đọc `CLAUDE.md` ở gốc kho trước. Phần "PR này làm gì" ở `ops/reviews/pr1503-review-1-codex/PROMPT.md`; thiết kế
hiện hành ở mục "Thiết kế mới" của `ops/reviews/pr1503-review-6-codex/PROMPT.md` và mục "Thay đổi lượt này" của
`ops/reviews/pr1503-review-{8,9,10}-codex/PROMPT.md`.

## PHẠM VI LƯỢT NÀY — đọc kỹ

Lượt này là KIỂM CHỨNG. Chỉ làm bốn việc dưới đây:

1. **Chạy** các bộ test có sẵn trong cây (danh sách ở mục "Cách đo") và báo số đạt/tổng.
2. **Đột biến bản vá** trên BẢN SAO TẠM: lấy các đột biến đã có trong bảng `DOT_BIEN` của
   `scripts/tl_core/llm_route_test.py` (bộ test tự chạy chúng) và, nếu muốn, sửa vài dòng của chính bản vá V1
   (`_dong_mo_ho`, `_DAU_HIEU_DUOC`, `_DAU_KEP_PO`) để xác nhận ca đích đỏ đúng lý do.
3. **Đọc mã**: `scripts/tl_core/llm_route.py` (`tach_khoan`, `_bo_dau_dong`, `_dong_mo_ho`, `_quet`, `_tu_noi`,
   `lech_nguyen_van`, `_chay_co_moc`, `duong_sub`) và handler trong `scripts/tl_core/ops_misc.py`.
4. **Mô tả bằng lời** mọi nghi vấn: nêu dạng văn bản nguồn hoặc tình huống nào có thể làm hỏng, và vì sao, mà
   KHÔNG viết thêm tệp thử nghiệm, chuỗi thử nghiệm hay script dò mới. Câu hỏi "có đúng không" thì trả lời bằng đọc
   mã + test có sẵn; điều gì chỉ kiểm được bằng thử nghiệm mới thì ghi vào "Không đo được".

Không cần đo Windows bản địa. Không cần dựng lại các probe của lượt trước.

## Câu hỏi cần trả lời

- V1 (dấu ngoặc/trích dẫn ngoài danh sách cho phép ⇒ từ chối cả nguồn) đã đóng chưa? Danh sách có hở không?
- Còn đường nào để một kết quả SAI (bỏ/gộp/cắt sai khoản) được nhận là nguyên văn, theo đọc mã?
- Còn đường nào gọi `api` sau khi `claude -p` đã khởi chạy, theo đọc mã?
- Test có răng không (đột biến)?

Đây là lượt CUỐI. Nếu không còn P0/P1, hãy APPROVE. Chặn oan (fail-closed) là P2/P3, không phải P1. Các giới hạn
đã khai: khoản dùng từ nối khác "là" bị chặn; nguồn mất số có dòng gãy bị chặn; nguồn có số mà có dòng không số
lạ bị chặn; nguồn có dòng ngoặc/trích dẫn không khép trong dòng, dấu lẻ, trích dẫn lồng, hay kiểu dấu ngoặc/trích
dẫn ngoài danh sách cho phép bị chặn; tiêu đề Điều không có dấu `.`/`:` sau số bị coi như dòng thường; không tự
chuyển `api` khi hết hạn mức gói giữa chừng; không phân biệt hạn mức gói với extra usage; chặn khi nguồn chạm CAP;
Windows bản địa chưa đo.

**Ghi dòng `VERDICT:` SỚM**: ngay khi đủ căn cứ, ghi dòng `VERDICT:` tạm ở cuối `.review/VERDICT.md`, rồi cập nhật
nếu kết luận đổi.

## Cách đo (không cần mạng)

```
python scripts/tl_core/llm_route_test.py
python .claude/dev/launcher_test.py --lap-ca t162 --lan 1
python .claude/hooks/pretooluse_guard.py --kiem-bang
python scripts/tl_core/command_registry_test.py
python scripts/tl.py --deterministic workflow-audit --strict --json
python scripts/tl.py --deterministic golden-test --json
python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
python scripts/tl.py --selftest        # ~6 phút
```

Lưu ý môi trường: thư mục RỖNG `/tmp/.git` (do sandbox để lại) làm 14 ca selftest `r973_bootstrap_*`, `wp433_*`,
`wp727_tl_gws_refresh` đỏ trên CẢ base lẫn head — đỏ sẵn, không phải hồi quy (bài học trong `CLAUDE.md`).

## Ràng buộc

- KHÔNG gọi Claude/Anthropic API thật, KHÔNG chạy `claude -p` thật, KHÔNG chạy `tl llm-khai-niem` thật.
  Không đọc/in giá trị biến bí mật.
- KHÔNG push, KHÔNG gọi GitHub, KHÔNG sửa tệp đã theo dõi trong cây (đột biến chỉ trên bản sao tạm).

## Đầu ra

Ghi TĂNG DẦN vào `.review/VERDICT.md` dưới thư mục làm việc:

```
# Verdict PR #1503 lượt 11 — Codex
reviewed_sha: 74fbf22a113e40cfa75d75e8ceaf6a3fd988d388
nang_tran: chủ kho nâng trần lên 11 (lời gọi thứ 11, cuối cùng); lượt kiểm chứng
## Đối chiếu (V1 và các lớp lượt 9 kết luận)
| # | Trạng thái | Bằng chứng |
## Findings mới
### X1 [P?] <tiêu đề> — <tệp:dòng>
Kịch bản (bằng lời) / Căn cứ đọc mã / Đề xuất
## Kết quả test và đột biến
## Không đo được
VERDICT: APPROVE | REQUEST_CHANGES
```

REQUEST_CHANGES nếu còn P0/P1. Dòng `VERDICT:` cuối là bắt buộc.
