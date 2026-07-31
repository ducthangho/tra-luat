# PROMPT BÀN GIAO sau lượt 25 (hàng đợi NLM đã xử) — 31-07-2026

Hàng đợi NLM của prompt `PROMPT_US_NLM_QUEUE_2026-07-31.md` **ĐÃ XỬ XONG phần duyệt được**.
Sổ kết quả: `rasoat/KETQUA_US_NLM_QUEUE_2026-07-31.md`. **KHÔNG chạy lại** Việc 1/2/3 và 2 ghost của
Việc 4 — đã có readback keyed làm bằng chứng.

## Còn lại — CHỜ NGƯỜI DÙNG DUYỆT (3 mục, tất cả đều TRÌNH chứ chưa làm)

Cả 3 đều CÓ TRƯỚC lượt 25 (đã nằm trong DRY chụp trước lệnh ghi đầu tiên), không phải hồi quy.

**Q-A. `KL_195-2025-KL-TW` con trỏ CHẾT** — row `1rpMJpDBLjGpOzgyIdymppiANnlD2dPqlkKDTbeR6Tgg`
(corpus=true, sohieu 195-2025-KL-TW), sid `6039b2a5-6416-4fd2-8161-b14c514bc948` không còn trên NLM
(nb 45739ff7). Đây là `desync_real` DUY NHẤT của shard và cũng là `coverage_gap`.
- (a) **KHUYẾN NGHỊ** — nạp lại NLM: `tl nlm-add 45739ff7-347a-45c7-8066-0f2f3b55f76a --drive-id 1rpMJpDBLjGpOzgyIdymppiANnlD2dPqlkKDTbeR6Tgg --type doc --row-kind own` (shard còn 8 slot)
- (b) xoá mapping: `tl nlm-reconcile 45739ff7-… --clear-stale --apply` — **CHE nợ phủ**, không khuyến nghị.
★ Chừng nào chưa quyết Q-A thì **ĐỪNG chạy `--clear-stale`** — hiện nó chỉ nhắm đúng dòng này.

**Q-B. Cụm `raw_on_nlm` 4 nguồn** (phác đồ đã ghi: convert GDoc → re-push → gỡ raw + reg_clear):
```
1PWj5iUJb1pcd5Q1TItAeDhuZvqrdgdK2     TL_ILO_2026_AI_tao_sinh_va_viec_lam_VN        9c0611ad…
1zsmfCS1IjtwIaeuftBx5H0h6iInGzIsU     Luat_45-2019-QH14_Bo_luat_lao_dong.docx       04e51f9c…
19_6Mp_8e1NQerD5ed42A5TRlO7W14VWt     VBT_PL_BC_BHXH_HaNoi_khao_sat_6-2026.pdf      c0d3c268…
1h0kl-G4-8l7r_rvOMSlVlXu3su1IwSvU     VBT_BC_BHXH_HaNoi_thuc_hien_CS_BHXH_2025.pdf  52f8ac58…
```
★ **45-2019 ưu tiên và CẤM gỡ trần**: canonical `1rjx9MLS3i7IMIOuQps0R7HjfVPPPl4SAK3I9p6Nrry8`
(corpus=true) hiện VẮNG khỏi NLM ⇒ docx thô là nguồn NLM DUY NHẤT của Bộ luật Lao động 2019.
Trình tự đúng: re-push canonical vào 45739ff7 TRƯỚC → verify ready → mới `nlm-source-remove 04e51f9c…`.
★ 2 nguồn PDF: theo memory `nlm-add-pdf-drive-fail` không add được bằng `--drive-id` — cần phiên **có
MCP notebooklm** (container lượt 25 KHÔNG có).

**Q-C. Trùng vật lý `Luat_50-2024-QH15_Cong_doan`** trên 45739ff7 — `9e985570-0c0f-4749-90a0-17f61acaa173`
và `1e9d957b-7967-45d7-a4f0-f1171dfd3ed0`. `nlm-audit-physical` khuyên gỡ `9e985570…`, giữ `1e9d957b…`.
Duyệt thì: `tl nlm-source-remove 9e985570-0c0f-4749-90a0-17f61acaa173 --apply --confirm yes`.

## Trạng thái slot sau lượt 25 (LIVE, dùng cột này chứ không dùng registry)

| notebook | LIVE | trống |
|---|---|---|
| 743ed200 (nền) | 299/300 | 1 — **hết FULL** |
| 45739ff7 (VBQPPL-2) | 292/300 | 8 |
| 2d8c2fef (ILO/điều ước) | 22/300 | 278 |
| 80742228 | 108/300 | 192 |

`CORPUS_TRUE_NOT_ON_NLM` = 53 (nợ CẤU TRÚC do trần 300/notebook) — 9 slot dôi không đủ, cần shard mới
nếu muốn kéo về 0.

## Nếp phải giữ (đã trả giá trong lượt 25)

- `nlm-content` phải kèm **`--no-fallback`** khi đo nguồn NLM còn sống hay chết — mặc định có fallback
  CORPUS, đọc được sẽ tưởng nhầm nguồn sống.
- `reg-query --live --json`: **tách stdout khỏi stderr** rồi mới parse; `2>&1` làm hỏng JSON và cho
  `count=None rows=0` GIẢ.
- `nlm-add` có cổng dedup-live theo **tên**: thay bản trùng tên phải **gỡ trước, add sau** (đừng
  `--skip-live-check`).
- `slot-audit` LIVE là chân lý — notebook gợi ý trong prompt có thể đã FULL.
- Ngoài phạm vi (giữ nguyên): note dup↔bản chuẩn · lô 3b 43 tên · r vá auditor/doc-text · sheet-dup
  `1Qja1Lwp…` Kế toán (CẤM reg-delete) · 43 row_kind overflow · quarantine hẳn `1auEnrsy…` · BC thẩm
  tra mẫu P9. Deploy: nợ 0 (Drive = v1.36.16).
