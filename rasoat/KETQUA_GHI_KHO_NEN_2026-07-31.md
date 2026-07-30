# KẾT QUẢ LƯỢT GHI KHO NỀN + 2 mẩu BHXH — 2026-07-31 (lượt 20, thi hành duyệt A+B+C+D)

Thi hành bảng điểm chạm đã được người dùng duyệt («chạy A+B+C+D, C5 giữ nguyên, Luat_74 quarantine»).
Bổ trợ cho lượt 19 (`KETQUA_DON_KHO_NEN_2026-07-31.md` — đo chỉ-đọc, kế hoạch GHI-1/2/3 của lượt đó
**vẫn chờ duyệt riêng**, lượt này KHÔNG chạy hộ). Mọi khẳng định dưới đây neo readback LIVE sau ghi.

## 0. Kết quả gọn — 11/12 mục ghi thành công, 1 mục hoá ra no-op

| # | Việc | Kết quả | Journal |
|---|---|---|---|
| A1 | BHXH: xoá `sohieu='16'` rác (`VB_16_7_2026_CONG_VAN…`) | ✅ readback `sohieu=''` | reg_clear (register --clear-cols) |
| A2 | BHXH: 9 dòng own `cat 02` → `02_Bao_hiem` | ✅ `02` trơ = 0; `02_Bao_hiem` 21→30 | `register-bulk_1785447439_1408` |
| A3 | Nền: recat `NQ_351-2017` → `44_…`, `CU_ILO-080` → `23_…` | ✅ moved=1+1, reg_patched=1+1, cat trơ 44/23 = 0 | `recat_1785447275_11752` · `recat_1785447363_21328` |
| B | Dedup 2 nhóm ready (`45-2019-QH14`, `60-2026-VBHN-VPQH`) | ✅ `corpus_false_patched=1` (60-2026 dup `''`→`false`; 45-2019 docx vốn đã false), canonical giữ | `dedup-plan_1785447133_20056` |
| C1 | Nền hieuluc → `Còn` (255 dòng: `Còn hiệu lực` 216 + `Con hieu luc` 31 + `(bản hợp nhất)` 8) | ✅ biến thể còn lại = **0** | `register-bulk_1785446633_20696` (+lượt idempotent `…679`) |
| C2 | → `Hết` (6 dòng) | ✅ | `register-bulk_1785446819_7280` |
| C3 | 3 dòng «đã hợp nhất tại X» → `Còn` + note con trỏ | ✅ (1 dòng note cũ 39 ký tự đã MERGE, không đè) | `register-bulk_1785446850_18612` |
| C4 | 2 dòng «hết - thay bằng X» → `Hết` + note con trỏ | ✅ (cùng journal C3) | — |
| C5 | `can_kiem_tra` (351-2017-UBTVQH14) | ⏸ GIỮ NGUYÊN theo duyệt | — |
| D1 | 4 PDF thô ND274/197/176/85 corpus true→false | ✅ keyed-readback 4/4 `'false'` | `source-update-corpus_17854476…` ×4 |
| D2 | loai phi chuẩn | ✅ applied 6 | `backfill-loai_1785446957_15588` |
| D3 | quarantine-fix (nhãn biến thể) | ✅ normalize_label 1; ghost_nlm 1 → hàng đợi NLM | quarantine-fix --apply |
| — | Luat_74 quarantine | **NO-OP đúng nghĩa**: dòng trùng `1mGRs4vs…` ĐÃ ở `_ZZZ_QUARANTINE_taluat` từ trước (lượt 19 đo) — không ghi gì; note chi tiết thuộc GHI-2 lượt 19 chờ duyệt | — |

**Trạng thái nền sau lượt:** 1315 dòng · hieuluc chỉ còn `{rỗng 1047 · Còn 259 · Hết 8 · can_kiem_tra 1}`
· corpus true 692 · cat trơ 44/23/02(BHXH) = 0. (Chênh +1 `Còn` so với 258 dự tính — một dòng được
chuẩn hoá thêm giữa hai lần đo; registry là dữ liệu sống, các phiên container đang chạy song song.)

## 1. Điều chỉnh so với bảng duyệt (đều ĐÃ báo trong phiên)

1. **3 dòng `ref` loại khỏi A2** (VBHN_14-2024, QD_178, VBHN_18-2026): bản gốc ở registry NỀN đã mang
   nhãn đủ (`20_Lao_dong`/`00_Van_ban_cua_Dang`) — nhãn trơ chỉ là artefact overlay của view profile,
   không có gì để sửa. A2 12→9 dòng.
2. **A2 đổi cơ chế recat → ghi nhãn registry** (`register --bulk --cols cat`): cùng đích nhất quán nhãn,
   tránh recat di chuyển file hồ sơ vào cây thư mục nền.
3. **Luat_74**: xem bảng — trạng thái đích đã đạt từ trước.

## 2. Ba bẫy công cụ dính trong lượt (ghi để không mất lần nữa)

1. **`register --bulk` GHI NGAY cả khi KHÔNG có `--apply`** — «DRY» đầu tiên của tôi đã ghi thật 255
   dòng (journal `…633`), lượt `--apply` sau `patched=0` idempotent. Đúng bẫy A.5-1 lượt 18 đã ghi cho
   `register` đơn — nay xác nhận **cả nhánh --bulk**. (Nội dung đúng như duyệt nên không hại.)
2. **`source-update-corpus <id> false --apply` KHÔNG ghi mà vẫn `ok:true`** — thiếu `--confirm yes` thì
   nó ở lại DRY, `mode:"DRY"` + `confirm_required` nằm trong output nhưng `ok:true` đánh lừa parser chỉ
   đọc ok. Phát hiện nhờ readback toàn cục (4 dòng vẫn true) — **rc/ok không bao giờ là bằng chứng ghi**.
3. **Suýt recat bằng drive_id BỊA**: output đếm trước đó cắt id ở 14 ký tự, tôi gõ lại «đủ 44 ký tự»
   theo trí nhớ — cả hai id sai đuôi. May DRY bắt được trước apply (đối chiếu lại regbase mới lấy id
   thật). **Luật: không hành động trên id đã truncate; mọi id phải copy từ dữ liệu nguồn.**

## 3. Còn treo (không thuộc phạm vi duyệt lượt này)

- **GHI-1/2/3 của lượt 19** (6 `reg_upsert` sohieu B3 — trong đó cụm 25 là collision thật Kế toán 2025
  vs NHNN 2022; note twin 18-2026/60-2026/L74; quarantine bản cũ `1FqSESXbEdh4…`) — kế hoạch + lệnh
  nguyên văn trong `KETQUA_DON_KHO_NEN_2026-07-31.md`, **chờ người dùng duyệt riêng**.
- **Hàng đợi NLM (container US-egress):** ghost `CD_32-2026-CD-TTg` (src `5ec30323…`); nguồn docx thô
  `45-2019` (src `04e51f9c…`) sau dedup; 4 nguồn thô `raw_on_nlm` (convert→re-push→gỡ);
  `nlm-reconcile --clear-stale`; `CORPUS_TRUE_NOT_ON_NLM` 53 (cấu trúc, trần 300/notebook).
- 43 dòng own-trên-notebook-overflow (doctor đếm 17 theo bộ lọc riêng) — lượt phân tích riêng
  (lật `row_kind` đổi phép đếm corpus server; đường sửa theo ghi chú r232: reg_upsert từng dòng).
- 97 tên phi chuẩn + 203 cụm `review` thiếu canonical — lô `corpus-audit --all` riêng.
