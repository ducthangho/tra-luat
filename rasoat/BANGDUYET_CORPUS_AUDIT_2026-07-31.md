# BẢNG DUYỆT — kết quả lô corpus-audit toàn kho nền, 31-07-2026

Nguồn: `corpus-audit --all` 18 vòng resume, `coverage_complete=true`, pool **699 văn bản corpus**.
Kết quả: **107 đề xuất** (88 NAME_NONSTANDARD · 8 CAT_MISMATCH · 5 NAME_TRICH_YEU · 4 CAT_LIKELY_WRONG
· 1 LOAI_MISMATCH · 1 SOHIEU_MISMATCH) + 13 `need_manual_read` + 2 errors. Danh sách thô đầy đủ:
`corpus_audit_digest_2026-07-31.txt`. CHƯA áp đề xuất nào — bảng này để duyệt.

## P1 — ĐIỀU TRA / VÁ DỮ LIỆU (nặng hơn chuyện tên) — 4 mục

1. ★★ **`ND_176-2025-ND-CP_Huu_tri_xa_hoi` (`1auEnrsy…`) hỏng KÉP**: (a) `doc-text` KHÔNG đọc được
   bằng mọi đường (cache/GDoc-export/docx/pdftotext); (b) audit đọc header ra **`20-2021-ND-CP`** —
   nghi SAI RUỘT. Trong khi đó bản PDF thô `ND176_2025_Huu tri xa hoi.pdf` vừa bị hạ `corpus=false`
   (D1 lượt 20) vì tưởng là twin của bản này ⇒ **NĐ 176/2025 (hưu trí xã hội — văn bản BHXH lõi) có
   thể đang KHÔNG còn bản dùng được trong corpus**. Đề xuất: `tl download 1auEnrsy…` soi tay → nếu
   ruột sai: re-ingest từ nguồn official + rút lại việc hạ PDF thô; nếu ruột đúng: vá đường bóc text.
2. **7 bản `MAU_Phieu_trinh_UBVHXH_khung_sach` nằm TRONG corpus** (7 drive_id, cùng tên, cat rỗng) —
   template làm việc lọt corpus + trùng 7 bản. Đề xuất: `corpus=false` cả 7 + đưa về vbthuong/quarantine.
   **KHÔNG nhận đề xuất máy** (máy đòi recat `41` — vô nghĩa với mẫu phiếu trình).
3. **`PERF_TEST_raw.txt` còn trong registry** (`12Lisxtt…`, corpus rỗng) — di sản test hiệu năng.
   Đề xuất: quarantine/xoá dòng.
4. **2 dòng nlm-only header rỗng** (`nlm:398d50d7` NQ_59-NQ-TW hội nhập · `nlm:e583ebea` VBHN_73-82
   phụ lục) — Drive lẫn NLM đều không đọc được; cần nguồn lại (kiểm NLM phải từ container US).

## P2 — CAT / LOAI / SOHIEU — 6 quyết định đơn lẻ

| # | Văn bản | Hiện tại → Đề xuất | Nhận định |
|---|---|---|---|
| 1 | `VBHN_09-2026-VBHN-VPQH_Luat_Can_cuoc` | `03_Buu_chinh_vien_thong` → `39_Trat_tu_an_toan_xa_hoi` | **RÕ ĐÚNG** — Căn cước thuộc 39, đang lạc 03 |
| 2 | `TT_02-2026-TT-BGDDT` (đào tạo tiếng dân tộc thiểu số) | `13_Giao_duc` → `10_Dan_toc` | Hợp lý |
| 3 | `TT_17-2025-TT-BNV` (định mức KTKT dịch vụ) | `20_Lao_dong` → `02_Bao_hiem` | Hợp lý (dịch vụ lĩnh vực BHXH) |
| 4 | `ND_39-2015-ND-CP` (hỗ trợ phụ nữ DTTS nghèo sinh con) | `08_Dan_so…` → `10_Dan_toc` | **TRANH CHẤP** dân số vs dân tộc — người quyết |
| 5 | `VBHN_09-2026-VBHN-BNV_Chuc_nang_So_Noi_vu` | `Hồ sơ dự án Luật` → `02` | Cat hiện tại LẠC (nhãn hồ sơ); nhưng `02` chưa chắc — cân nhắc `35_To_chuc_bo_may` — người quyết |
| 6 | `000.0 Danh muc VB qd chi tiet BLLD 2019` | loai `Bộ luật` → `Phụ lục` | **RÕ ĐÚNG** — danh mục, không phải bộ luật |

## P3 — TÊN (93 dòng, chia 4 rọ — duyệt theo RỌ, không cần từng dòng)

| Rọ | Số | Nội dung | Đề xuất |
|---|---|---|---|
| 3a | ~15 | Tên RÁC thật: `142919vie` · `80-nd-cp.signed.pdf` · `1 Luat sua 4 Luat.docx` · `Luat Viec lam.docx` · `1. Luat ng VNDLVONN 2020.docx` · `112_NQ-CP_702934.docx` · 4 tên tiếng Việt đầy dấu cách (127/QĐ-TTg, 33/2026/QĐ-TTg, 353/2025, 356/2025, 804/QĐ-TTg) · 4 PDF ILO chữ hoa · `44_2024_QH15_Duoc_583839` · html đấu thầu | Rename tay từng cái (`header-verify --fix-suggest` hỗ trợ); đi lô `source-rename` có duyệt |
| 3b | ~40 | `ND_xxx`/`QD_`/`TT_` đúng số hiệu nhưng THIẾU `<Chu_de>` (vd `ND_318-2025-ND-CP`) | Lô rename bổ sung chủ đề — nửa máy nửa tay, làm dần |
| 3c | ~33 | Văn bản Đảng/VK/TL/VBT/CU (`KL_121-KL-TW_2025_Tong_ket_NQ_18`, `VK_DH_XIV_*`, `HD_*-VPTW`…) — **chuẩn tên RIÊNG của chúng đã ĐÚNG** | **BỎ QUA** + vá auditor thêm bucket văn-bản-Đảng/tài-liệu (r nhỏ) để cờ hết kêu vĩnh viễn |
| 3d | 5 | `NAME_TRICH_YEU` đề xuất máy — **SAI HƯỚNG CẢ 5**: lấy TÊN CƠ QUAN làm chủ đề (`…_bo_lao_dong_thuong_binh…`, `…_chinh_phu`), coi **Nghị định thư EVFTA là Nghị định** (`ND_nghi_dinh_thu_1/2`), đánh mất prefix họ `VK_DH_XIV` | **KHÔNG áp**; 5 tệp gộp vào rọ 3a sửa tay |

## Ghi chú phương pháp

- `need_manual_read` 13 = giao của rọ 3a + P1 (scan/không lớp text) — đã phân bổ ở trên, không phải mục riêng.
- Đề xuất CAT của audit chỉ suy từ TIÊU ĐỀ + alias pháp điển (thân văn bản không còn là bằng chứng cat)
  — vì vậy mục P2#4/#5 để người quyết thay vì tin máy.
- Mọi mục khi duyệt sẽ chạy DRY → apply → readback keyed, journal từng bước, theo đúng nếp các lượt 20-21.
