# ADR-0010 — nlm_status là từ vựng ĐÓNG ở cửa ghi; tách nlm_claim/nlm_due (desync ≠ coverage_gap)

- **Trạng thái:** accepted (2026-07-21, grill + domain-modeling; thi hành r179 v1.35.9).
- **Vì sao thành ADR (3 tiêu chí):** (a) **khó đảo** — kèm backfill dữ liệu một lần trên registry
  live (added→pushed, live→active); đảo lại là một cuộc di trú dữ liệu nữa; (b) **ngạc nhiên** —
  người đến sau sẽ hỏi «trạng thái `added` đi đâu?» và «vì sao slot-audit với nlm-reconcile ra hai
  số khác nhau mà không lệnh nào sai?»; (c) **trade-off thật** — ba phương án đã cân (dưới).

## Bối cảnh (đo 21-07 trên profile «Luật BHXH», notebook 59e8d0de)

- Cột `nlm_status` tích 5+ biến thể từ vựng: `added`(×23) `live`(×2) `ready`(×1) lẫn với họ chuẩn
  `pushed*/synced*/active/removed_*`. Bộ audit đọc (`_nlm_status_known`) coi `added` là lạ →
  `NLM_STATUS_MISMATCH` bắn đúng (selftest 936/1118 KHOÁ hành vi này — added-fire là ĐÚNG), nhưng
  không có cửa nào chặn ghi tiếp giá trị lạ, cũng không có đường nắn giá trị cũ.
- Sự cố «51/40/51»: slot-audit báo `51 vật lý vs 40 claim (+11)` kèm lời khuyên backfill;
  nlm-reconcile cùng lúc báo `51 = 51, desync 0`. Đo lại: +11 = đúng 11 dòng `removed_from_drive`
  (lô PDF dự thảo 16.6 — file Drive đã xoá, nguồn NLM còn sống) — slot-audit loại họ removed khỏi
  claim, reconcile đếm src-bearing rows. **Hai phép đo đều đúng, chỉ thiếu TÊN** — chữ «gap»/«claim»
  trần không nói phép đo nào đang trả lời câu hỏi nào.

## Quyết định 1 — từ vựng ĐÓNG ở cửa ghi, khoan dung ở cửa đọc

`nlm_status` hợp lệ GHI = họ `pushed*` (đã đẩy) · `synced*` (đã đối soát) · `active` (xác nhận
sống) · `removed_<lý do>` (gỡ có chủ đích, hậu tố BẮT BUỘC ghi lý do) · rỗng (route clear).
`register --nlm-status` giá trị ngoài họ → rc=2 + danh sách hợp lệ (`_nlm_status_write_ok`,
r179 T1). Cửa ĐỌC (`_nlm_status_known`) GIỮ NGUYÊN khoan dung (nhận thêm trash*/deleted/removed
trần) — audit không false-fire trên dữ liệu lịch sử; bất đối xứng này CÓ CHỦ ĐÍCH và bị selftest
khoá (`r179_t1_nlm_status_write_vocab_closed`).

Dữ liệu cũ nắn MỘT LẦN bằng lệnh mới `backfill-nlm-status --dry/--apply` (r179 T2): map tất định
`added→pushed`, `live→active`, per-row `reg_upsert` journaled (undo được); giá trị ngoài map
(`ready`…) KHÔNG đụng — báo `stray`, sửa tay sau khi hiểu nguồn gốc. Chạy SAU deploy r179.

## Quyết định 2 — tách nlm_claim / nlm_due; cấm «gap»/«claim» trần

- **nlm_claim** = điều SỔ KHẲNG ĐỊNH đang có mặt (dòng status họ sống / src). Đối chiếu claim↔live
  → **desync** — việc của `nlm-reconcile` (`desync_real` per-source; slot-audit chỉ có bản ĐẾM:
  `desync_estimate`).
- **nlm_due** = diện PHẢI-CÓ-MẶT theo chính sách corpus (dòng corpus=true ∪ ref, TRỪ họ removed_*
  — gỡ có chủ đích là RỜI diện; attribution nb-khớp, blank quy về base). Đối chiếu due↔vật lý →
  **coverage_gap** (nợ phủ) — việc của `slot-audit` (mức sổ-cái) và `nlm-reconcile` (per-source,
  vì nó có live-set). MỘT helper chung `_nlm_due_rows` cho cả hai lệnh — một từ vựng, một cách đếm.
- CẢ HAI lệnh in CẢ HAI số với tên tường minh + `labels_note` định nghĩa tại chỗ; khoá `gap` trần
  của slot-audit BỎ. Chênh đếm được GIẢI THÍCH thay vì bỏ lửng: `removed_family_still_pointing`
  (slot-audit) / `removed_family_still_live` (+sample, reconcile). Nghiệm thu trên ca thật:
  slot-audit `desync_estimate=+11` kèm note «giải thích TRỌN bằng 11 dòng removed_*»; reconcile
  `removed_family_still_live=11` liệt kê đúng 11 PDF; `nlm_due=16, coverage_gap=0, desync_real=0`.

## Ba phương án đã cân

1. **Mở từ vựng đọc để hết MISMATCH** (thêm added/live/ready vào `_nlm_status_known`) — BÁC: hợp
   thức hoá phân mảnh, audit mù thêm một lớp, không giải quyết hai-phép-đo-một-tên.
2. **Đóng cả đọc lẫn ghi ngay** — BÁC: audit false-fire hàng loạt trên dữ liệu lịch sử chưa nắn,
   buộc backfill phải chạy TRƯỚC deploy (ngược trình tự an toàn).
3. **Đóng cửa ghi + backfill một lần + đọc khoan dung** (CHỌN) — chặn tái nhiễm từ nay, dữ liệu cũ
   nắn có journal, audit giữ độ nhạy (added-fire vẫn đúng cho tới khi backfill chạy xong).

## Dấu vết thi hành

- r179 (v1.35.9): T1 `_nlm_status_write_ok` + gate register (classify.py / source_ops.py) · T2
  `backfill-nlm-status` (nlm_ops.py, GENERATED_SPECS + COMMAND_META) · T8 `_nlm_due_rows` +
  nhãn slot-audit/nlm-reconcile. Selftest r179_t1_*/t2_*/t8_* (20 ca r179, 1151/1151).
- Từ điển: CONTEXT.md mục «Sổ cái corpus & NLM» (nlm_status/nlm_claim/nlm_due/Scope/Draft —
  commit cùng r179).
