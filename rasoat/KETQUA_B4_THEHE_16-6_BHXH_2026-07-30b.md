# KẾT QUẢ B4 + r253 — hồ sơ «Luật BHXH», lượt 2 ngày 30-07-2026

Tiếp `KETQUA_VIEC_TREO_BHXH_2026-07-30.md` §A.8. Lượt này làm mục 1 (B4), 2 (phủ-bằng-chunk),
3 (readback `register`), 5 (cache `extract_*`). Mục 4 (kho NỀN) CHƯA làm.

## 0. Kết quả gọn

| # | Việc treo (A.8) | Kết quả |
|---|---|---|
| 1 | B4 — neo thế hệ 10 tệp 16.6.2026 | **XONG** — 10/10 dòng ghi + verify 2 cột; 7 cặp có bằng chứng, 3 dòng KẾT LUẬN "không có cặp 1:1" |
| 2 | Vá cờ phủ-bằng-chunk | **XONG** (r253) — backlog 1 → 0, 3 vế phản chứng |
| 3 | Vá readback `register` | **KHÔNG VÁ — giả thuyết A.5 SAI**, việc đó đã làm rồi (§3) |
| 5 | Xoá cache `extract_*` hồ sơ khác | **KHÔNG CÓ GÌ ĐỂ XOÁ trong container này** (§4) |
| 4 | Kho NỀN (80742228, `Luat_74-2025-QH15` trùng, B2/B3/B5) | **CHƯA LÀM** — mang sang lượt sau |

Repo: `0b336e4` · VERSION **1.35.90** · selftest **1402/1402** · gate **8/8 xanh** · đã push
`claude/luat-bhxh-30-07-fyc9tq`. **Package trên Drive VẪN 1.35.86 — r251+r252+r253 CHƯA deploy.**

> ⚠ **Lưu ý hạ tầng, đã trả giá trong lượt này:** chạy gate mà CÒN overlay env hồ sơ
> (`TL_NOTEBOOK_ID=59e8d0de…`) thì `golden` + `determinism` ĐỎ GIẢ — fixture golden ghim notebook
> `743ed200…`. Không phải bug bản vá. **Gate phải chạy với env SẠCH** (unset TL_PROFILE/TL_NOTEBOOK_ID/…).

## 1. B4 — trạng thái `removed_from_drive` nói một việc KHÔNG hề xảy ra

### 1a. Đo LIVE, có ĐỐI CHỨNG ÂM

`drive-parity --file-id` (get-meta THẬT qua GAS) trên cả 10 + 1 fileId BỊA làm đối chứng:

| | kết quả |
|---|---|
| 10 tệp thật | **LIVE, `trashed=false`**, CÙNG một thư mục cha `1qusmEcHlS96dBEorelTUaDL-drdiq0Et` («Hồ sơ Luật») |
| fileId bịa `1ZZZ…` | `gas_file=null`, `gas_ms=1987` (vòng gọi THẬT, không phải lỗi mạng) |

⇒ Cùng đường code, cùng transport, kết quả khác nhau **chỉ do tệp có tồn tại hay không** — nên
"LIVE" ở trên là bằng chứng dương, không phải mặc định im lặng.

**Sự thật bị ĐẢO NGƯỢC so với tên trạng thái:** tệp CÒN trên Drive, thứ bị gỡ là **nguồn trên
NotebookLM** (`nlm-reconcile`: `removed_family_still_live=0`). Ghi chú ADR-0010 hồi 21-07 chép
"file Drive đã xoá, nguồn NLM còn sống" — **ngược hoàn toàn với thực tế hôm nay**.

### 1b. Ghép cặp thế hệ — đo phủ 5-gram 2 CHIỀU, KHÔNG đoán theo tên

Tải 10 PDF (byte-size khớp metadata Drive 10/10), bóc text bằng pymupdf (cả 10 CÓ lớp text),
đối chiếu với 19 tài liệu thế hệ 16-7 lấy bằng `tl extract`.

| tệp 16.6 | bản thay thế | bằng chứng |
|---|---|---|
| 03. Bản thuyết minh QPH | `VBT_Ban_thuyet_minh_quy_pham_hoa…16-7-2026` | 70,00% · cách 36,05pp |
| 02. Dự thảo Luật 16.06 | `DUTHAO_Luat_sua_doi…16-7-2026` | xem cảnh báo dưới |
| 01. Tờ trình Chính phủ | `DUTHAO_To_trinh_BNV…16-7-2026` | 65,00% · cách 26,51pp |
| 07. Bảng so sánh, thuyết minh | `VBT_Ban_so_sanh_thuyet_minh…16-7` phần 1-3/3 | 87,48% · cách 65,03pp |
| 06. BC đánh giá TTHC | `VBT_Ban_danh_gia_TTHC…16-7-2026` | 85,72% · cách 34,43pp |
| 05. Báo cáo tổng kết | `VBT_BC_7692-BC-BNV_Tong_ket_thi_hanh…2026` | 83,90% · cách 61,43pp |
| 04. BC rà soát pháp luật | `VBT_BC_BNV_Ra_soat_chu_truong…19-7-2026` | 67,14% · cách 26,24pp |
| **00. VB xin ý kiến bộ ngành** | **KHÔNG CÓ** | 571 từ, công văn CHUYỂN; khớp cao nhất 32,08% chỉ là văn mẫu |
| **08. Bảng tổng hợp ý kiến** | **KHÔNG CÓ** | 22,91% vs 21,59%, **cách 1,32pp = không phân biệt được** |
| **09. Văn bản góp ý (384tr)** | **KHÔNG PHẢI** nguồn bộ 8 phần | xem dưới |

> ⚠ **Top-1 phủ xuôi CHỌN SAI CẶP cho tệp 02.** Đo xuôi ra `Bảng so sánh` 73,14% > `Dự thảo Luật`
> 53,35% — vì **bảng so sánh trích NGUYÊN dự thảo vào trong nó**. Bắt được nhờ 3 thứ khác:
> bản mới tự ghi **"Dự thảo ngày 16/7/2026"** trong khối đầu; phủ **NGƯỢC** (new-in-old) **80,81%**;
> cùng thể loại + cùng cấu trúc Điều. Đây đúng bài học "không grep chuỗi" — một phép đo thì lừa được.

> ⚠ **Tệp 09 KHÔNG phải nguồn của bộ `VBT_Y_kien_gop_y_16-7` 8 phần.** Chính `MUC_LUC` của bộ đó tự
> khai nguồn là PDF **307 trang, 97 trang ảnh quét**; còn tệp 09 là **384 trang, CÓ lớp text ở CẢ
> 384 trang** (đo bằng pymupdf). Phủ chỉ 7,36%. **GIỮ LẠI — xoá là mất dữ liệu không có ở bộ 16-7.**

### 1c. Đã GHI (journal `register-bulk_1785397964_1444`, undo được)

10 dòng · 2 cột · `register --bulk --cols "nlm_status,note"`. KHÔNG chạm Drive/NLM/corpus/hieuluc/cat.

- `nlm_status`: `removed_from_drive` → **`removed_superseded_gen_16-7-2026`** (hợp lệ `removed_<lý do>`)
- `note`: rỗng → đính chính + bản thay thế, hoặc ghi RÕ "KHÔNG có cặp 1:1" cho 3 dòng

Verify: `patched 10 / missed 0`, và đọc lại độc lập (`reg_get refresh=true`) **10/10 khớp CẢ hai cột**.
Sau khi ghi: NLM 70 · `desync_real=0` · `coverage_gap=0` · `already_removed=10` ·
**`NLM_STATUS_MISMATCH=0`** (chứng minh cửa đọc theo tiền tố nhận giá trị mới).

**Vì sao đổi tên trạng thái là AN TOÀN** (đã kiểm 3 chỗ dùng `removed_from_drive` dạng khớp-CHÍNH-XÁC):
`tl.py:497 _NLM_REMOVED_STATUS` là **hằng CHẾT** (khai mà không ai dùng) · `registry_orchestrator.py:177`
nằm sau cổng mime GDoc mà cả 10 tệp đều `application/pdf` nên không đụng · `registry_hygiene.py:197`
là chỗ thứ 3 — **và chính nó là bug §2 dưới đây**.

## 2. r253 — hai vá code (chi tiết ở CHANGELOG ★ v1.35.90)

- **Phủ-bằng-chunk**: `_chunk_covered_sohieu` + `_title_flags(e, covered_sohieu=None)` +
  `_ingest_missing_select`. Backlog **1 → 0**, `covered_sohieu` đúng 1 phần tử (không quét rộng).
- **`registry_hygiene` từ vựng trôi lệch**: exact-set → luật TIỀN TỐ + test PARITY.
  **Nói đúng mức độ: chưa false-fire THẬT** — `analyze()` skip `row_kind=ref` + `own_thuong` TRƯỚC khi
  gắn cờ, mà 6 dòng `active` đều `ref`, 10 dòng B4 đều `own_thuong`. Vá vì nó sẽ nổ khi có dòng
  `own`/khác-`thuong`, và B4 vừa thêm một họ `removed_<lý do>` mới vào sổ.

## 3. ĐÍNH CHÍNH A.5 mục 3 — readback `register` KHÔNG phải lỗi cache

A.5 đoán cờ đỏ oan do readback đọc qua cache GAS TTL~600s → đề xuất "bust cache". **Đã làm rồi:**
`_verified_reg_upsert` (N3) và `_verified_reg_write` (batch ≤3) đều gọi `reg_get … refresh="true"`;
`regReadAll_(force)` phía GAS bỏ cache, đọc thẳng Sheet. Đo thực nghiệm (ghi lại ĐÚNG giá trị đang
có = no-op): `verified=true`, `fields_dropped=null`.

⇒ **Không vá theo giả thuyết sai.** Muốn truy tiếp cần lệnh/output GỐC của lượt đó. Nghi vấn còn lại
(CHƯA có bằng chứng): mỗi `reg_upsert` rewrite TOÀN BỘ sheet (tab tạm rồi swap) — readback rơi trúng
lúc swap của lượt kế có thể thấy bản chưa xong. Cũng lưu ý `_REG_BULK_READBACK_MAX = 3`: lô >3 item
KHÔNG readback field-level, chỉ đối chiếu `patched==expected` (lô B4 10 dòng đi đường này).

## 4. Cache `extract_*` — không có gì để xoá Ở ĐÂY

`~/.tra_luat_cache` trong container này sinh lúc **07:30 hôm nay**, chỉ chứa `manifest.json` +
`manifest_index.json`, **0 tệp `.txt`**. Cache nhiễm `&amp;` của r252 nằm trên MÁY đã chạy các lượt
trước (Windows), không phải ở đây. Việc cần làm **trên máy đó**:
`Remove-Item "$env:USERPROFILE\.tra_luat_cache\*\extract_*.txt"` (và `extract_*.txt` ngay thư mục gốc
cache = hồ sơ nền), rồi đọc lại bằng `tl extract --refresh`.

## 5. Còn treo sang lượt sau

1. **Kho NỀN** (A.8 mục 4): notebook `80742228` chưa khai topology · 2 dòng `Luat_74-2025-QH15` trùng ·
   B2/B3/B5 trong `RASOAT_PROFILE_LUAT_BHXH_2026-07-29.md`.
2. **Deploy** — Package Drive đang 1.35.86, thiếu r251+r252+r253. Chờ user duyệt; nhớ chốt chống thụt
   lùi (đọc tên file Package trên Drive TRƯỚC khi push).
3. Xoá cache `extract_*` trên máy Windows (§4).
4. Nếu muốn truy tiếp cờ đỏ oan của `register`: giữ lại lệnh + output GỐC lúc nó xảy ra (§3).
