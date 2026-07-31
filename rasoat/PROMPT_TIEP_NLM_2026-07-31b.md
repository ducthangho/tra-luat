# PROMPT BÀN GIAO sau lượt 25 (đã gồm vòng 2) — 31-07-2026

Hàng đợi NLM của `PROMPT_US_NLM_QUEUE_2026-07-31.md` **ĐÃ XỬ XONG**, và 3 mục trình thêm (Q-A/Q-B/Q-C)
cũng đã xong sau khi người dùng duyệt «theo khuyến nghị».
Sổ: `rasoat/KETQUA_US_NLM_QUEUE_2026-07-31.md` (§1-7 vòng 1, §8-11 vòng 2).
**KHÔNG chạy lại** bất kỳ mục nào ở trên — mỗi mục đều có readback keyed / audit làm bằng chứng.

## Trạng thái chốt (đo cuối lượt 25)

- `nlm-audit-physical` → **rc=0 "SẠCH — pointer khớp vật lý toàn scope"**.
- `nlm-reconcile --all-notebooks` → `desync_real` = 0/0/0 · `coverage_gap` = 0.
- LIVE slot: 743ed200 = **299/300** (hết FULL) · 45739ff7 = **292/300** · 2d8c2fef = 22/300 ·
  80742228 = 108/300. **Dùng cột LIVE, không dùng registry.**
- NĐ 176/2025 đã vào corpus-effective bằng bản mới `1hQedQKZ…` (sid `64c5c6a4…`).
- Bộ luật Lao động 45/2019 nay đứng bằng **canonical GDoc** `1rjx9MLS…` (sid `6cce35ec…`), bản docx
  thô đã gỡ khỏi NLM.

## ★ CẢNH BÁO VẬN HÀNH — có phiên khác ghi song song vào notebook 45739ff7

Trong lượt 25, ba thay đổi (thêm `52eb0e58` KL_195, gỡ `9e985570` dup Công đoàn, thêm `6cce35ec` BLLĐ
canonical) xảy ra **không do phiên này** — `tl journal` chứng minh phiên này chỉ có 13 run và không
run nào tạo/gỡ các sid đó. NotebookLM **không có LockService** như registry ⇒ hai phiên cùng đẩy một
notebook là last-writer-wins, im lặng.
**Nếp bắt buộc từ nay:** trước mọi lô ghi NLM, dump `nlm-list` **hai lần liên tiếp** và so khớp tập
hợp; khác nhau ⇒ có phiên khác đang chạy ⇒ DỪNG, hỏi người dùng. Cổng dedup của `nlm-add` là chốt cuối
(đã chặn đúng một cú tạo trùng) — **đừng bao giờ ép qua bằng `--skip-live-check`**.

## Còn treo (chờ duyệt / chờ điều kiện)

**T-1. 3 nguồn PDF `raw_on_nlm` — CHẶN KỸ THUẬT, cần phiên CÓ MCP notebooklm.**
```
1PWj5iUJb1pcd5Q1TItAeDhuZvqrdgdK2     TL_ILO_2026_AI_tao_sinh_va_viec_lam_VN        9c0611ad…
19_6Mp_8e1NQerD5ed42A5TRlO7W14VWt     VBT_PL_BC_BHXH_HaNoi_khao_sat_6-2026.pdf      c0d3c268…
1h0kl-G4-8l7r_rvOMSlVlXu3su1IwSvU     VBT_BC_BHXH_HaNoi_thuc_hien_CS_BHXH_2025.pdf  52f8ac58…
```
Cả 3 đã xác minh `mimeType = application/pdf`. Theo memory `nlm-add-pdf-drive-fail`: KHÔNG add được
bằng `--drive-id`, phải download + MCP `source_add source_type=file` + `register --nlm-source-id` tay.
Phác đồ: convert GDoc (copy_convert) → re-push → gỡ nguồn raw + reg_clear mapping. **Chưa duyệt.**

**T-2. `c4f16911-f255-4876-9735-ad7c3fa40964` = `CU_ILO-128_Tro_cap_tan_tat_tuoi_gia`** — nằm VẬT LÝ
trên 45739ff7 nhưng registry trỏ 743ed200 (`foreign_skipped` by title). Có trước lượt 25. Cần quyết:
sửa con trỏ notebook, hay `nlm-migrate` về đúng shard?

**T-3. `CORPUS_TRUE_NOT_ON_NLM` = 53** — nợ CẤU TRÚC do trần 300/notebook. 9 slot dôi hiện có không đủ;
muốn về 0 phải mở shard mới.

## Ngoài phạm vi (giữ nguyên, đừng nhặt nhầm)

Note dup↔bản chuẩn (cần đường đọc cột note GAS) · lô 3b 43 tên thiếu chủ đề (chạy lệnh quét năm r276
trước) · r vá auditor/doc-text · sheet-dup `1Qja1Lwp…` Kế toán (**CẤM `reg-delete`**) · 43 row_kind
overflow · quarantine hẳn bản khuyết 176 `1auEnrsy…` · BC thẩm tra mẫu P9. Deploy: **nợ 0**
(Drive = v1.36.16).

## Nếp đã trả giá trong lượt 25 (giữ lấy)

- `nlm-content` đo nguồn sống/chết **bắt buộc `--no-fallback`** — mặc định fallback CORPUS sẽ trả nội
  dung và làm tưởng nhầm nguồn NLM còn sống.
- `reg-query --live --json`: **tách stdout khỏi stderr** rồi mới parse (`2>&1` cho `count=None rows=0`
  GIẢ). Luôn kiểm `count` trước khi tin `rows[0]`.
- `nlm-add` chặn dedup theo **tên**: thay bản trùng tên ⇒ **gỡ trước, add sau**.
- `nlm-source-remove` fail-closed `POINTER_STILL_ATTACHED` là ĐÚNG; dùng `--force` (gỡ vật lý trước,
  sổ theo sau) rồi đồng bộ `register --nlm-status removed_by_user` — KHÔNG xoá con trỏ registry trước.
- `register` trả `FIELDS_DROPPED_ON_WRITE` + `verified:false` **chưa chắc hỏng**: webapp bỏ qua field
  RỖNG. Phải **diff toàn dòng trước/sau** mới kết luận (lượt 25 diff 17 trường: chỉ 2 trường mục tiêu đổi).
- `--clear-stale` chỉ chạy khi đã ĐỌC `desync_real_sample` và xác nhận từng dòng đáng xoá mapping —
  nó có thể nhắm dòng ngoài phạm vi và CHE nợ phủ.
