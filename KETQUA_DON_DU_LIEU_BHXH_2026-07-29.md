# KẾT QUẢ dọn dữ liệu + NotebookLM — hồ sơ Luật BHXH, 29-07-2026

## 1. NotebookLM: ban đầu KHÔNG vào được, sau khi bạn làm tươi cookie thì SỐNG

| Mốc | Trạng thái |
|---|---|
| Đầu phiên | `nlm` CLI không có trên PATH ⇒ mọi con số NLM chỉ là ESTIMATE |
| Sau `tl nlm-install` | ✅ cài được `/root/.local/bin/nlm` (tải Python 3.11 standalone + notebooklm-mcp-cli) |
| `tl nlm-auth-load` lần 1 | ⚠ kéo được cookie từ Drive nhưng `__Secure-3PSIDRTS` **hết hạn 3906 phút** ⇒ gọi thật trả `Authentication expired` |
| Sau khi bạn stage cookie mới | ✅ `nlm-auth-load` lần 2 → `alive=True`; `nlm-get` trả `source_count=69, title="Luật BHXH"` |

⇒ Trong môi trường remote headless này **không tự khôi phục được phiên NLM** (cần `nlm login` tương tác
hoặc `TL_MASTER_KEY`); nhưng **một khi bundle được làm tươi từ ngoài thì chạy đầy đủ**.

## 2. Đưa 2 văn bản mới lên NotebookLM — và một lỗi NẶNG bắt được ngay trước khi đẩy

**NĐ 159/2025** — 32k ký tự, một nguồn: `nlm-add` → `source_id 887255af…`, ready.

**Luật 41/2024** — 183k ký tự, phải chunk. Khi lập kế hoạch chunk thì lộ lỗi:

> `chunk-plan` trả `part1 Điều **2**..65` — **mất Điều 1**. Đếm lại:
> `total_chars = 183.428` nhưng tổng ký tự các chunk chỉ **182.678** ⇒ **hụt 750 ký tự**,
> mà `warnings` vẫn **rỗng**.

750 ký tự đó là: `QUỐC HỘI` · `Luật số: 41/2024/QH15` · `LUẬT / BẢO HIỂM XÃ HỘI` · căn cứ Hiến pháp ·
`Chương I / NHỮNG QUY ĐỊNH CHUNG` · **trọn Điều 1 (Phạm vi điều chỉnh)**.

Nếu đẩy như vậy: nguồn NLM của luật gốc **không có cả số hiệu lẫn Điều 1**, hỏi "Điều 1 Luật BHXH quy
định gì" sẽ không có căn cứ — và không chỗ nào báo lỗi. **Đã vá (r230, v1.35.66) trước khi đẩy.**

Sau vá: `total 183.428 = tổng chunk 183.428` (hụt 0), ranh giới `part1 Điều 1..64` · `part2 Điều 65..141`
— **khớp** với `_split_by_dieu_chunks` (đã vá r229), hết cảnh hai bộ cắt cho hai kết quả.

**Lỗi công cụ thứ ba trong cùng chuỗi (CHƯA vá, đã lách):** `chunk-apply` xuất `.md`, nhưng
`profile-ingest` từ chối `.md` (`UNSUPPORTED_EXTENSION`, chỉ nhận doc/docx/odt/pdf/rtf/xls/xlsx)
⇒ `profile-ingest-chunks` gọi con luôn rc=2. Pipeline chunk **đứt ở chính khớp nối của nó**.
Lách bằng cách dựng .docx từ thân chunk (giữ nguyên văn + gắn dòng xuất xứ có sha256).

**Dọn hậu quả timeout:** lần `nlm-add` đầu bị timeout 2' nhưng server-side ĐÃ thành công, retry tạo bản
trùng ⇒ notebook phình 69→**74**. Đã đối chiếu registry để biết giữ source nào, gỡ 3 nguồn thừa
(gồm `37eec1d9…` cũ của NĐ 159 trỏ vào GDoc đã xoá) ⇒ còn **71**.

**Neo trạng thái LIVE:** `nlm-reconcile` ⇒ **`coverage_gap = 0`, `desync_real = 0`**.
Từ nay số liệu NLM của hồ sơ này là ĐO THẬT, không còn là claim ước lượng.

## 3. Dọn dữ liệu registry

| Việc | Kết quả | Journal |
|---|---|---|
| Chuẩn hoá `loai` | **13/13** dòng (`VBHN`→`Văn bản hợp nhất`, `Nghi_dinh`→`Nghị định`, `Luat`→`Luật`, `Thong_tu`→`Thông tư`, `Nghi_quyet`→`Nghị quyết`); `loai_noncanonical` 4→**2** | `backfill-loai_1785319522_4087` |
| Chuẩn hoá `hieuluc` | **29/29** dòng. Trước: `Còn hiệu lực` 21 · `Còn` 11 · `con_hieu_luc` 1 · 2 biến thể DỰ THẢO. Sau: chỉ còn **`Còn` 35 · rỗng 45 · `DỰ THẢO — chưa hiệu lực` 13** | `register-bulk_1785320808_19952` |
| Làm tươi manifest | `count=93`, treeHash `2a7ccd5c-93` (trước kẹt ở **43 / 25-06**, lệch hơn 1 tháng) | — |
| Ghi chú 3 dòng Luật 41 | Đánh dấu rõ bản canonical vs 2 chunk phụ trợ, để lượt sau không đọc nhầm 3 dòng cùng số hiệu là lỗi trùng | `register-bulk_1785320950_22129` |

**Chọn chuẩn `hieuluc` = `{Còn, Hết, Chưa}`** — đây là bộ mà chính `_normalize_hieuluc` của công cụ sinh
ra, nên các lần ghi tự động sau này sẽ đồng bộ. (Ban đầu tôi định chuẩn hoá ngược lại thành
`Còn hiệu lực`; đọc code mới thấy sai hướng.)

## 4. Những khuyến nghị tôi CỐ Ý KHÔNG áp, kèm bằng chứng

Bạn nói "đồng ý hết các khuyến nghị". Tôi đã áp mọi khuyến nghị **trừ hai nhóm dưới đây**, vì có bằng
chứng chính công cụ đề xuất SAI — áp vào sẽ làm hỏng dữ liệu:

**(a) `corpus-audit` đề xuất `CAT_MISMATCH → cat 46` cho 3 mục.** Rổ 46 = "Luật sửa đổi nhiều luật"
(phi-pháp-điển). Bị đẩy vào đó gồm `ND_233-2025-ND-CP`, `ND_212-2025-ND-CP` và **một Công văn**
(`CV_10593-NHNo-ALCO`) — trong khi quy tắc ranh giới nói BHXH → cat **02**. Gốc: header NĐ 233 trích 13 số
hiệu, ≥8 là Luật ⇒ nhánh omnibus trong `_cat_boundary_rule` bắn TRƯỚC nhánh BHXH→02, và nhánh đó **thiếu
guard loại văn bản**. Chạy `recat --cat 46 --apply` sẽ nhiễm rổ 46 bằng Nghị định và Công văn.

**(b) `NAME_TRICH_YEU` đề xuất đổi tên phá cấu trúc bundle.** Ví dụ
`VBT_Y_kien_gop_y_Luat_BHXH_16-7_phan_6_cua_8` → `Luat_Cong_ngan_hang_nha_nuoc`: lấy trích yếu của **công
văn ĐẦU TIÊN trong bundle**, mất chỉ số `phan_N_cua_8`, và gắn tiền tố `Luat_` cho thứ không phải luật.

⇒ Hai nhóm này cần **vá code** (thêm guard doctype trước khi ép cat 46; chặn NAME_TRICH_YEU khi tên khớp
`phan_\d+_cua_\d+`), không phải áp đề xuất. Chưa vá trong phiên này.

## 5. Còn treo — cần bạn quyết

1. **17 tài liệu hồ sơ dự thảo 16-7-2026 đang `corpus=true` nhưng không số hiệu** (thuyết minh, bản so
   sánh 3 phần, 80 công văn góp ý 8 phần, mục lục…), trong khi 10 file "Hồ sơ Luật" thế hệ 16.6 lại để
   `corpus=false`. Quyết định này chi phối luôn 20/22 dòng bị gắn cờ `name_nonstandard` — nên tôi không
   tự chọn. Hai hướng: giữ trong corpus (chấp nhận cờ tên) hoặc hạ `corpus=false`/`loai=thuong` cho nhất
   quán với thế hệ trước.
2. **3 nguồn NLM là PDF thô** (góp ý Agribank / Vietcombank / BIDV) — nên convert sang GDoc rồi re-push.
3. **Notebook `80742228-…` giữ 54 dòng nhưng NGOÀI topology đã khai** — cần quyết là notebook cũ đã bỏ
   hay khai thiếu topology.
4. **`chunk-apply` xuất `.md` mà `profile-ingest` không nhận** — nên vá để pipeline chunk chạy thẳng.

## 5b. Sau khi NLM sống: chạy nốt các lệnh trước đây bị chặn — và bật luôn gws

**`doctor` giờ rc=0, TẤT CẢ cổng xanh** (trước đó rc=2). Ngoài NLM, tôi bật được luôn đường đọc Drive
nhanh: `tl gws-auth-load` (dùng token, KHÔNG cần master key) + `npm i -g @googleworkspace/cli@0.22.5`
⇒ `gws-ping` trả `authed=true, auth_method=oauth2, cred_alive=true`. Từ giờ đọc Drive không còn rơi về GAS.

| Lệnh (trước đây chết vì thiếu nlm CLI) | Kết quả LIVE |
|---|---|
| `nlm-audit-physical` | **`clean: true`** — `pointer_mismatch 0 · unregistered_physical 0 · dup_physical 0 · pointer_dead 0` |
| `nlm-reconcile` | `coverage_gap 0` · `desync_real 0` |
| `nlm-orphans` | `live 71 = registered_active 71`; `mismatch 0`, `unregistered 0`, gap `0` |
| `slot-audit` | `physical 71 = live 71`, `desync_estimate 0` |

### Bản đồ notebook — lần đầu ĐO ĐƯỢC (trước chỉ là claim trong sổ)

| Notebook | Nguồn LIVE | Tên thật | Nhận xét |
|---|---|---|---|
| `743ed200…` | **300** | VBQPPL | ⚠ **KỊCH TRẦN** (giới hạn NLM = 300/notebook) |
| `45739ff7…` | **293** | VBQPPL-2 | ⚠ chỉ còn **7 chỗ** |
| `2d8c2fef…` | 22 | VBQPPL-3 | còn nhiều chỗ — đây là nơi đổ tiếp |
| `59e8d0de…` | 71 | Luật BHXH | notebook hồ sơ này |
| `80742228…` | 108 | **Khảo sát Luật XB** | ✅ **giải được nghi vấn**: KHÔNG phải "shard ngoài topology" như `doctor` gợi, mà là notebook của **hồ sơ KHÁC**; 54 dòng thấy được là do quét kèm scope nền |

⇒ Việc cần biết trước: **nạp thêm vào VBQPPL/VBQPPL-2 sẽ đụng trần rất sớm**; lô sau phải định tuyến
sang VBQPPL-3 (`tl push-overflow`).

Còn `removed_family_still_pointing: 10` — 10 dòng `removed_from_drive` vẫn giữ `nlm_source_id`
(mục B4 cũ). Không gây lệch (audit vật lý sạch), nhưng nên `nlm-reconcile --clear-stale` ở lượt dọn kho nền.

## 6. Trạng thái cuối

`total=93` · `corpus` (client) `40` / theo luật server `25` · `nlm_drift`: `NLM_STATUS_MISMATCH=0`,
`NLM_NOTEBOOK_ID_MISSING=0`, `CORPUS_TRUE_NOT_ON_NLM=1` (đúng thiết kế: bản canonical Luật 41 không tự
lên NLM, đi qua 2 chunk) · `duplicates.by_name_active=0`, `by_md5=0` · NLM `coverage_gap=0`,
`desync_real=0` · selftest **1384/1384**.
