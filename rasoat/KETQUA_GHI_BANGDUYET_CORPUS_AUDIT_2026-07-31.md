# KẾT QUẢ LƯỢT GHI bảng duyệt corpus-audit (lượt 24) — 31-07-2026

Phê duyệt người dùng NGUYÊN VĂN: «duyệt A B C D1 D2; Q1=giữ 08; Q2=35; Q3=fetch congbao».
Kế hoạch + lệnh nguyên văn: `rasoat/KETQUA_THUCHIEN_BANGDUYET_CORPUS_AUDIT_2026-07-31.md` (§F, master `8bb9bad`).
Nếp thi hành: từng lô apply → **readback KEYED** (bằng chứng duy nhất; lần nào cache nghi ngờ thì
đo lại `reg-query --drive-id … --live`, count=1 từng id — không dính bẫy sheet-dup).

## Kết quả từng lô

| Lô | Kết quả | Journal |
|---|---|---|
| **GHI-A** 7 MAU_Phieu_trinh | ✅ 7/7 corpus=false + cat=QUARANTINE, readback keyed 7/7 | 7× `source-update-corpus_1785454217…454382` + `recat_1785454392_19976` (moved=7, reg_patched=7, reg_missed=0) |
| **GHI-B** PERF_TEST_raw.txt | ✅ corpus=false + QUARANTINE (giữ dòng, không reg-delete) | `source-update-corpus_1785454508_17580` + `recat_1785454529_25476` |
| **GHI-C** P2 | ✅ C1 Căn cước→39 · C2 TT02→10 (folder `10_Dan_toc` tự tạo) · C3 TT17→02 · C5 Sở Nội vụ→35 (Q2) · C6 loai=«Phụ lục» (register 1 lần, verified=true). **C4 KHÔNG chạy** (Q1=giữ 08) — readback đối chứng cat=08 nguyên | `recat_1785454671/…746/…834/…900` + `register_1785454962_7304` |
| **GHI-D1** 7 dup/rác 3a | ✅ 7/7 corpus=false + QUARANTINE (L97-2025 · L69-2020 · L74-2025 bản 3 · NQ112 docx · 142919vie≡CU_UNESCO-2005 · 80-nd-cp scan · html đấu thầu) | 7× `source-update-corpus_1785455120…455470` + `recat_1785455485_20000` |
| **GHI-D2** 13 rename | ✅ 13/13 registry + Drive + sohieu (6 lệnh kèm --sohieu, 2 vá thiếu-năm 127/804). Live keyed 4 mẫu đúng server-side. #11 TL_ILO_2026: drive_rename TIMEOUT nhưng **GAS đã hoàn thành sau timeout** — retry idempotent xác nhận (oldName=tên mới) | 13× `source-rename_1785455725…456194` + retry `source-rename_1785456522_19620` |
| **Q3** NĐ 176/2025 | ✅ trọn phần máy-VN, chi tiết dưới | `ingest-local_1785456915_21068` + `source-update-corpus_1785457034_10380` |

## Q3 — NĐ 176/2025: đã có bản text-first ĐẦY ĐỦ

- Nguồn: Công báo **số 913+914 ngày 17-7-2025**, trang văn bản
  `congbao.chinhphu.vn/van-ban/nghi-dinh-so-176-2025-nd-cp-45409.htm`, link tải trích từ trang
  (đúng recipe, không đoán path): `g7.cdnchinhphu.vn/api/download/stream?…176-2025-NĐ-CP.doc|.pdf`.
  Tải cả hai: `.doc` 654.848B (Word OLE2) + `.pdf` 344.855B (typeset, **có text**: 10 trang/17.015
  ký tự, đủ Điều 1→8 — xác nhận trước khi ingest).
- `ingest-local` (plan_hash `b551fb8f…`, ocr_gate digital, convert server-side .doc→GDoc):
  **GDoc mới `1hQedQKZvtumfVs4ELJP0EN4SsSAkCToxzyk7Gy3AS_M`** (src docx trung gian `1hpRdcS0g7BL…`),
  cat 02_Bao_hiem, loai Nghị định, sohieu 176-2025-ND-CP, hieuluc «Còn hiệu lực».
- **VERIFY qua đường sản xuất `doc-text` rc=0**: đủ Điều 1→8, «Số: 176/2025/NĐ-CP», «Phạm vi điều
  chỉnh», «Đối tượng và điều kiện hưởng», «500.000 đồng», Mẫu 01/02, ngày 30-6-2025 — đúng phần
  bản cũ khuyết. (Kèm cảnh báo `[markup] ⚠` vì export .docx không dùng được, chỉ text/plain —
  với NĐ mới không có gạch-bỏ ⇒ cosmetic; cùng họ bug export cần r vá đã đề xuất ở sổ lượt 23 §A.)
- Post_step theo plan: **hạ bản GDoc khuyết `1auEnrsyEz2FsCW2y39B244uYoSDlva2TgTi2DE9bw50`
  corpus=false** — live keyed: corpus=false, row_kind=overflow, count=1. `nlm_delete` fail rc=1
  (bản khuyết CÓ nguồn NLM — gỡ phải từ US, đã xếp hàng đợi).
- ★Trạng thái CHỦ ĐÍCH tạm thời: **176/2025 đang NGOÀI corpus-effective** — bản mới corpus=∅ chờ
  đúng trình tự next_steps của ingest: (US) add nguồn NLM (notebook gợi ý
  `743ed200-2e55-4673-b7a0-9bfd13b41ce6`) → `nlm-reconcile` → `register --drive-id 1hQedQKZ… --corpus true`.
  KHÔNG flip corpus=true trước khi NLM link (thiết kế pipeline).

## Lệch so với kế hoạch (có lý do, không giấu)

1. **Note 2 chiều dup↔bản chuẩn (khuyến nghị kèm D1): HOÃN.** Không có đường CLI đọc note hiện hành
   (`reg-query` v2 + `--live` không chiếu cột note; `register` đơn không có cờ note; ghi bulk mù =
   nguy cơ ĐÈ note cũ trên 6 bản chuẩn — vi phạm nếp merge lượt 21). Văn bản note đề xuất cho phiên
   có đường đọc GAS (reg_get đầy đủ cột):
   - 7 dòng dup: «DUP — bản chuẩn: `<tên bản chuẩn>` (`<drive_id>`); quarantine 31-07 lượt 24»
   - 6 bản chuẩn (`1oObRzQxd…` L97 · `1uGeVjiDK…` L69 · `1PfTsnRY…` L74 · `18_Ybzz…` NQ112 ·
     `1pjGKKFn…` CU_UNESCO · `1GRmvvF5…` ND80): «+ bản trùng `<tên cũ>` (`<id>`) đã quarantine 31-07»
2. **C4 không chạy** — đúng Q1 (người giữ 08_Dan_so).
3. **Mọi thao tác NLM từ máy VN fail như dự kiến** (geo-block) — dồn hàng đợi US, không retry mù.

## Hàng đợi container US (NLM) — TỔNG HỢP MỚI sau lượt 24

1. ★MỚI: **9 nguồn NLM mang tên cũ** sau GHI-D2 (nlm_rename rc=1): QD_127 · QD_33 · ND_353 · ND_356
   · QD_804 · NQ_112 · TL_ILO_2026 · TT_10-2020 · ND_118-2016 — re-title/reconcile per-notebook.
2. ★MỚI: **chuỗi 176/2025**: add NLM cho `1hQedQKZ…` → reconcile → corpus=true → gỡ nguồn NLM bản
   khuyết `1auEnrsy…` → `nlm-reconcile --clear-stale`.
3. Cũ: `nlm:398d50d7` NQ_59 + `nlm:e583ebea` VBHN_73-82 (P1#4 ghi sổ lượt 23) · ghost CD_32-2026
   (`5ec30323…`) · docx thô 45-2019 (`04e51f9c…`) · 4 `raw_on_nlm` · nguồn bản thiếu 131-2021 (`1831Z…`).

## Trạng thái sau lượt + còn treo

- Pool corpus-audit rời 15 dòng (7 MAU + PERF + 7 dup); 13 tên đã chuẩn hoá; 2 sohieu hết thiếu-năm.
- Cặp identity CÓ CHỦ ĐÍCH 2 file cùng tên `ND_176-2025-ND-CP_Huu_tri_xa_hoi` (mới own + khuyết
  overflow corpus=false) — hygiene sweep sẽ kêu tới khi note/quarantine bản khuyết (quyết sau khi
  chuỗi US xong).
- Còn treo (tuỳ duyệt, ngoài lượt): r vá auditor (bucket họ-tên-riêng 3c + neo «Số:» + cờ
  NO_TEXT_LAYER + doc-text/export fallback) · lô 3b 43 tên (chạy lệnh quét năm r276 trước) · nạp
  Luật Đấu thầu 22/2023 nguồn sạch · sheet-dup `1Qja1Lwp…` Kế toán (CẤM reg-delete) · 43 row_kind
  overflow · BC thẩm tra mẫu P9.
- Nợ deploy hiện hành thuộc chuỗi P15 (master đã r278b/v1.36.16 trong lúc lượt này chạy) — phiên
  này không đụng code/deploy.
