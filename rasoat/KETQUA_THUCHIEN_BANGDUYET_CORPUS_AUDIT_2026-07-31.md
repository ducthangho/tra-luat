# KẾT QUẢ THI HÀNH BẢNG DUYỆT corpus-audit (lượt 23) — phiên ĐIỀU TRA + DRY, 31-07-2026

Đề bài: `rasoat/BANGDUYET_CORPUS_AUDIT_2026-07-31.md` + `D:\Quốc hội\PROMPT_thuchien_bangduyet_corpus_audit.md`.
Trạng thái phiên: **TOÀN BỘ chỉ-đọc + DRY — CHƯA APPLY BẤT KỲ GHI NÀO.** Mọi lệnh GHI chính xác ở §F,
chờ duyệt theo nếp DRY → trình → CHỜ DUYỆT → apply → readback keyed.

Đo nền lúc làm: registry `--refresh` 1315 dòng (corpus_true=690, pool audit 699 khớp true+∅);
origin/master trôi trong phiên `5b869b3` → `9c8e5b2` (r275/v1.36.13) → `44da738` (r276/v1.36.14) —
đều là P15-F04/F06 của **phiên P15 song song**; Drive LIVE v1.36.12 ⇒ **nợ deploy r275+r276 THUỘC
PHIÊN P15**, phiên này không đụng. Xác nhận bằng chứng cứ: **chưa phiên nào thi hành bảng duyệt**
(không sổ KETQUA mới, registry còn nguyên trạng thái tiền-quyết ở mọi mục).

## A. P1#1 — NĐ 176/2025 hỏng kép: ĐIỀU TRA XONG, ruột ĐÚNG nhưng KHUYẾT

- ★**Id trong PROMPT sai đuôi** (`…PzC8w` ≠ id thật `1auEnrsyEz2FsCW2y39B244uYoSDlva2TgTi2DE9bw50`)
  — đúng bẫy tái-dựng id từ digest truncate; đã lấy id nguyên văn từ registry rồi mới hành động.
- Tải GDoc (export docx 690KB qua fallback GAS — direct-media 403) + bóc tay: **ruột ĐÚNG là
  NĐ 176/2025 hưu trí xã hội** — 42× «hưu trí xã hội», 1× «176/2025/NĐ-CP» (ở header Phụ lục),
  «20/2021» chỉ xuất hiện 4 lần dưới dạng TRÍCH DẪN NĐ 20/2021 trợ giúp xã hội.
- **NHƯNG KHUYẾT TRANG 1**: text chỉ có từ «2 \ Điều 3» trở đi (Đ3→Đ8 + Mẫu 01/02, 12.077 ký tự);
  MẤT tiêu đề + Số + căn cứ + **Điều 1 (phạm vi) + Điều 2 (đối tượng)** — trang 1 là scan không có
  lớp text/OCR; kèm noise OCR vùng dấu/chữ ký («HOAX», «awill»…).
- PDF thô `10ZKaqguP8pLOdZIKgxaMANOwAHsLHjG7` (`ND176_2025_Huu tri xa hoi.pdf`): 10 trang scan,
  **0 text** ngoài khối chữ ký Cổng TTĐT 04.07.2025 (cùng mốc ký với bản GDoc — cùng nguồn gốc).
  ⇒ việc hạ corpus=false ở D1 lượt 20 là ĐÚNG, **không rút lại**.
- Phán xử audit `SOHIEU_MISMATCH 176-2025 vs 20-2021` = **BÁO ĐỘNG GIẢ**: đường đọc header vớ
  sohieu ĐẦU TIÊN trong text (một citation) vì trang 1 không có text. Registry row hiện ĐÚNG
  (cat 02_Bao_hiem, loai Nghị định, sohieu 176-2025-ND-CP, corpus=true) — **KHÔNG sửa dữ liệu**.
- KẾT LUẬN KHO: corpus **không có bản 176/2025 đầy đủ dùng được** (GDoc khuyết Đ1-Đ2; PDF thô 0 text).
  ĐỀ XUẤT (Q3 §F): nạp bản text-first từ nguồn official (congbao.chinhphu.vn đi được từ máy VN;
  vbpl.vn không đi được) hoặc link TVPL cho user tự tải (nếp HỎI TRƯỚC) → ingest xong hạ bản GDoc khuyết.
- Bug công cụ ghi nhận (r nhỏ, TUỲ DUYỆT, phiên này không chạm code): (i) `doc-text` chết mọi đường
  trên file này trong khi `download` export-docx GAS sống — chuỗi fallback doc-text thiếu nhánh;
  (ii) audit header nên neo mẫu «Số: X» / gần nhãn loại VB thay vì sohieu đầu tiên trong text;
  (iii) scan-không-text đáng có cờ riêng `NO_TEXT_LAYER` thay vì đề xuất rename/sohieu.

## B. P1#2 + P1#3 — DRY XONG (chờ duyệt GHI-A/GHI-B)

- 7 dòng `MAU_Phieu_trinh_UBVHXH_khung_sach` (row_kind=own, flags ORPHAN_CAT+MISSING_SOHIEU,
  on_nlm=False, corpus=∅ — ∅ vẫn nằm trong pool audit): DRY `recat --quarantine` lô 7 sạch
  (boundary_warnings=[]) + DRY `source-update-corpus false` từng id 7/7 ok (bulk false trần bị van
  `BULK_PLAIN_FALSE_REFUSED` chặn — ĐÚNG thiết kế, chạy đơn từng id; không dùng `--as-ref` vì đây là
  template làm việc, không phải tài liệu tham khảo). KHÔNG nhận recat 41 của máy — đúng bảng duyệt.
- `PERF_TEST_raw.txt` (`12LisxttFh7oIbNitaz_yyBnt6s14IYND`): DRY cặp lệnh tương tự sạch;
  will_remove_nlm=false. Chọn phương án QUARANTINE (reversible) thay vì xoá dòng — `reg-delete`
  không cần thiết và mang rủi ro (bẫy sheet-dup xoá cả hai của ca `1Qja1Lwp…`).

## C. P1#4 — 2 dòng nlm-only chết: GHI SỔ (không đụng registry)

| khóa | tên | trạng thái | việc phải làm (container US) |
|---|---|---|---|
| `nlm:398d50d7-a639-4528-8820-56644b12fb3e` | NQ_59-NQ-TW_Hoi_nhap_quoc_te_2025 (sohieu 59-2025-NQ-TW, corpus=true) | Drive + NLM đều không đọc được header | kiểm source trên NLM; nạp lại nguồn nếu chết thật |
| `nlm:e583ebea-db66-4cdd-94d9-df663cfc5f54` | VBHN_73-82-ND-CP_Phu_luc (corpus=true) | như trên | như trên |

→ ĐÃ XẾP vào hàng đợi NLM (US-egress — NLM web geo-block IP VN). Hàng đợi US hiện có: ghost
`CD_32-2026` (src `5ec30323…`) · docx thô 45-2019 (src `04e51f9c…`) · 4 `raw_on_nlm` ·
`nlm-reconcile --clear-stale` · nguồn NLM bản thiếu 131-2021 (`1831Z…`) · **+ 2 dòng này**.

## D. P2 — 6 quyết cat/loai: DRY XONG (chờ duyệt GHI-C; #4/#5 chờ NGƯỜI CHỌN)

| # | drive_id | hiện tại → đề xuất | DRY | nhận định |
|---|---|---|---|---|
| 1 | `1wD6qMdqUEpuP-WAX9th_o9vM-E8Hmxxq1TAh5t2Zn6c` | 03 → **39_Trat_tu_an_toan_xa_hoi** | sạch | RÕ ĐÚNG (Căn cước) |
| 2 | `1JSadlq1Cv8OOfWFrVARUAycyhzomY5O0_n6A-YjLuz0` | 13 → **10_Dan_toc** | sạch | hợp lý (đào tạo tiếng DTTS) |
| 3 | `1uqmUbNC1Cat8-ntZA7lNmvb1XffdxGmI-vRhMlmA_no` | 20 → **02_Bao_hiem** | sạch | hợp lý (định mức KTKT dịch vụ BHXH) |
| 4 | `1-iPFLO80xTDvlBhTiE0W4b_UU-fnB0PwJWXcRGBfJNE` | 08 → 10? | sạch (DRY 10) | **NGƯỜI QUYẾT** — Q1 §F |
| 5 | `1Ks_Ynvw45lIbbtZNjHUoQQHLdGH120_tNCFjgC0C0ps` | «Hồ sơ dự án Luật» → 35? / 02? | DRY cả 35 lẫn 02 sạch | **NGƯỜI QUYẾT** — Q2 §F |
| 6 | `1d3i4NCh-Jo7gZhsmUymabVHXIXcrD8JISzEo5wpvTCE` | loai «Bộ luật» → **«Phụ lục»** | không DRY được (register GHI NGAY — bẫy đã biết) | RÕ ĐÚNG; chạy đúng 1 lần sau duyệt |

## E. P3 — điều tra tên: KẾT QUẢ ĐẢO NGHĨA MỘT PHẦN RỌ 3a

Đọc ruột (download + bóc docx/fitz/html) từng file không đọc được header. **Phát hiện lớn: 6 CẶP
IDENTITY-DUP MỚI** — 7 file rọ 3a không phải «tên rác cần đặt lại» mà là **BẢN TRÙNG của văn bản đã
có trong corpus** ⇒ hướng xử đúng là QUARANTINE (GHI-D1), không phải rename:

| file rác (id) | ruột thật | bản đã có trong kho (corpus=true) |
|---|---|---|
| `1 Luat sua 4 Luat.docx` (`1asc-wQ0Uhm4KAqNIDFD_lJVexVzlbGzG`) | Luật 97/2025/QH15 (MTTQ+CĐ+TN+THDCCS, 27/6/2025) | `Luat_97-2025-QH15_SuaDoi_MTTQ_CongDoan_ThanhNien_DanChuCoSo` (`1oObRzQxd…`) |
| `1. Luat ng VNDLVONN 2020.docx` (`1IN8TN_3HTyUxLaccc5cSMxtzWH3hd5FJ`) | Luật 69/2020/QH14 | `Luat_69-2020-QH14_NLD_VN_di_lam_viec_o_nuoc_ngoai` (`1uGeVjiDK…`) |
| `Luat Viec lam.docx` (`1yXg-_VuiMKr_u1ILwAj9-RrdXNQyNa_q`) | Luật 74/2025/QH15 | `Luat_74-2025-QH15_Viec_lam` (`1PfTsnRY…`) — đây là bản trùng THỨ BA (1 bản đã quarantine lượt 20) |
| `112_NQ-CP_702934.docx` (`1NGVXxQCLUWrWG8NGCIM5JfmnBs_2JknX`) | NQ 112/NQ-CP 20/4/2026 (bổ sung CTLP 2026) | trùng khớp nội dung + độ dài với GDoc `NQ_112-NQ-CP` (`18_Ybzz…`, rọ 3b) — GIỮ bản GDoc, rename nó (GHI-D2#7) |
| `142919vie` (`1leJoyJKSEfljHj2wPbtdTCkjR7cfEKABfH7k1BUyv8Q`) | Công ước UNESCO 2005 đa dạng biểu đạt văn hóa | `CU_UNESCO-2005_Da_dang_bieu_dat_van_hoa` (`1pjGKKFn…`) |
| `80-nd-cp.signed.pdf` (`1aRKrGw6PEkRZvi1MIbb7CfBibe_l8Q3f`) | scan 21 trang **0 text** (ký 09.04.2025); theo cat 44 + kho ⇒ NĐ 80/2025/NĐ-CP | `ND_80-2025-ND-CP_To_chuc_thi_hanh_VBQPPL` (`1GRmvvF5…`) |
| `luat-dau-thau-so-22-2023-qh15-…html` (`1-Feyc6sgQNq83zQSlO6bCSZkQ0LDMIys`) | trang web LuatVietnam chứa Luật Đấu thầu 22/2023/QH15 (369k ký tự lẫn nav rác) | **KHÔNG có** bản 22-2023-QH15 nào khác trong kho — nếu kho cần Luật Đấu thầu thì phải nạp nguồn sạch (hàng đợi tải, HỎI TRƯỚC); html rác không đáng làm corpus |

**13 RENAME thật (GHI-D2)** — định danh bằng ruột/header, DRY 13/13 sạch không collision
(3 lệnh kèm đổi sohieu đi đúng đường `reg_upsert theo drive_id`; 4 TL_ILO không sohieu là đúng chuẩn họ TL_):

| # | drive_id | tên cũ → TÊN MỚI (+sohieu) | bằng chứng |
|---|---|---|---|
| 1 | `1MZlRu4DcICseY1jpXGL2080vbilN_h79mksFt2xY_c4` | 127/QĐ-TTg… → `QD_127-2021-QD-TTG_Chien_luoc_quoc_gia_AI_2030` + sohieu `127-2021-QD-TTG` | «Số: 127/QĐ-TTg … 26/01/2021» (sohieu cũ THIẾU NĂM) |
| 2 | `18-39wTx-jZ9bLTzo51ihyrj2w4G0rcVd87IrRm2Jg-4` | 33/2026/QĐ-TTg… → `QD_33-2026-QD-TTG_Danh_muc_he_thong_AI_rui_ro_cao` | header 33-2026 + issue 2026-06-30 |
| 3 | `1ZOTW36-6T58A5VumrbLx9EElXSUdEN90MTS8GYcHfW8` | 353/2025/NĐ-CP… → `ND_353-2025-ND-CP_Co_che_thu_nghiem_cong_nghiep_cong_nghe_so` | header 353-2025-ND-CP |
| 4 | `1T65C_hLSjIhDuhGmNn_L2EYJ_F5TYQsgpp3P-t0Tlx4` | 356/2025/NĐ-CP… → `ND_356-2025-ND-CP_Chi_tiet_Luat_Bao_ve_du_lieu_ca_nhan` | header 356-2025-ND-CP |
| 5 | `1e1KpRRSHzTA1VOzWPTIt2pHj5r9G-RE_hC_Es0gVF_g` | 804/QĐ-TTg… → `QD_804-2026-QD-TTG_Danh_muc_bo_du_lieu_AI` + sohieu `804-2026-QD-TTG` | «Số: 804/QĐ-TTg … 06/5/2026» (sohieu cũ THIẾU NĂM) |
| 6 | `1Weu1RNqWcBqV_CUHZkJTP-3pkKJOWO9AXyVDDbjuz7Y` | 44_2024_QH15_Duoc_583839 → `Luat_44-2024-QH15_Sua_doi_Luat_Duoc` + sohieu `44-2024-QH15` | header 44-2024-QH15 (+105-2016, 28-2018 được sửa); kho chưa có bản khác |
| 7 | `18_Ybzz8XHRnmilzgDdqgPj5TZGhBwrdKUwsXH7rhtPk` | NQ_112-NQ-CP → `NQ_112-2026-NQ-CP_Bo_sung_CTLP_2026_sua_Luat_69-2020` + sohieu `112-2026-NQ-CP` | ruột NQ 112/NQ-CP 20/4/2026; bất biến sohieu-có-NĂM |
| 8 | `1RY7HUHODAvBqUbhe5xcqgA2ojVE3AjBh` | BC QUOC GIA VIEC LAM THOA DANG ILO.pdf → `TL_ILO_2019_BC_quoc_gia_Viec_lam_thoa_dang_SDG_VN` | bìa «BÁO CÁO QUỐC GIA 2019 … SDG» |
| 9 | `1TKqDl_WgCuSxmUe_n6HpiLk3PgCPGJfo` | CT VIEC LAM THOA DANG ILO.pdf → `TL_ILO_Khung_CTQG_Viec_lam_thoa_dang_2022-2026` | trang iv-xi «Khung Chương trình quốc gia về Việc làm thỏa đáng tại Việt Nam 2022-2026» |
| 10 | `1U0L3gIJ9Feie_Hw5SxDsY9WsmrdLi8TY` | GIOI VA HOAN THIEN CHINH SACH VIEC LAM.pdf → `TL_ILO_2025_Gioi_va_hoan_thien_chinh_sach_viec_lam` | © ILO 2025, xuất bản lần đầu 2025 |
| 11 | `1PWj5iUJb1pcd5Q1TItAeDhuZvqrdgdK2` | TRI TUE NHAN TAO VA KHUYEN NGHI ILO.pdf → `TL_ILO_2026_AI_tao_sinh_va_viec_lam_VN` | «Báo cáo tóm tắt ILO … Tháng 4/2026, GenAI và việc làm tại VN» |
| 12 | `1nHnfEQDEJao4E_kt8MbE0F9T3NVgNLshEgkLFvRMdA8` | 010. Thong tu 10_2020… → `TT_10-2020-TT-BLDTBXH_Chi_tiet_BLLD_ve_HDLD` + sohieu `10-2020-TT-BLDTBXH` | header 10-2020-TT-BLDTBXH (3d, máy đề xuất sai hướng cơ-quan) |
| 13 | `1iEiWmiBvd-WTFI2xeWpYy8LlJlDY9xUWk7OB7B0OBbI` | 118_2016_ND-CP_ngày 22/7/2016… → `ND_118-2016-ND-CP_Sua_doi_ND_56-2008_ngan_hang_mo_ghep_tang` + sohieu `118-2016-ND-CP` | header 118-2016-ND-CP (3d) |

**GIỮ NGUYÊN (3 — thuộc 3d/3c):** `EVFTA_PL_Nghi_dinh_thu_1_quy_tac_xuat_xu` ·
`EVFTA_PL_Nghi_dinh_thu_2` · `VK_DH_XIV_NQ_Dai_hoi` — tên đúng chuẩn họ riêng (điều-ước/văn-kiện);
máy vẫn lặp đề xuất sai `ND_nghi_dinh_thu_*` (coi Nghị định thư là Nghị định) — xác nhận nhận định 3d.

**Rọ 3b (43 dòng)** — đúng số hiệu, thiếu `<Chu_de>`: KHÔNG làm phiên này (đúng bảng duyệt: lô nhỏ
làm dần). Danh sách id đầy đủ: `p3_ro.json` mục 3b (kèm sổ này trong scratchpad phiên; tái tạo được
bằng `an1.py`+`p3_prep.py` từ digest). Ghi chú thêm cho lô 3b: 4 sohieu THIẾU NĂM/male-format cần
backfill khi làm lô (`2092-NQ-UBTVQH15`, `560-NQ-UBTVQH15`, `02-BGDDT`, `04-BGDDT` — 2 cái sau còn
sai khuôn VBHN `NN-YYYY-VBHN-XXX`); **r276 (P15-F06) vừa land lệnh quét bất biến năm — phiên GHI nên
chạy lệnh quét mới đó thay vì tin danh sách tay này.**

**Rọ 3c (28 dòng)** — BỎ QUA đúng bảng duyệt. Đề xuất vá auditor (r nhỏ, TUỲ DUYỆT): thêm bucket
họ-tên-riêng cho tiền tố `VK_ KL_ HD_ TL_ VBT_ CU_ HU_ EVFTA_` + mẫu `NQ/QD/CT/KL_*-TW` để 28+ dòng
này im vĩnh viễn. 1 ngoại lệ trong 3c: `Chỉ thị 04-CT/TW — Ban Bí thư…` (`16qPnV5eCYtKyatND4NRuAPMDRu_encEnHV4RbFgmZOM`,
sohieu đã có 04-2026-CT-TW) tên CHƯA theo chuẩn họ → ứng viên rename lẻ `CT_04-CT-TW_2026_Tang_cuong_lanh_dao_xuat_ban`
(gộp vào lô 3b sau, không gấp).

## F. LỆNH GHI CHÍNH XÁC — CHỜ DUYỆT (GHI-A → GHI-D2 + 3 câu hỏi Q1-Q3)

Nếp áp dụng: chạy theo THỨ TỰ trong từng lô; sau MỖI lô chạy readback keyed
(`tl --profile vbqppl reg-query --refresh --limit 3000 --json` → kiểm đúng các id vừa ghi: corpus/cat/name/sohieu);
bằng chứng ghi duy nhất là readback, không phải rc/ok (bẫy silent-DRY). Journal đủ, undo được.

### GHI-A — 7 MAU_Phieu_trinh: corpus=false + quarantine
```
tl --profile vbqppl source-update-corpus 1JjIPSLJ3Wjpw_15xcxjAFY4RBRxQfKQB1mom1tzeqpE false --apply --confirm yes
tl --profile vbqppl source-update-corpus 1cdDxcgyXrnW370yEzqLM8Kn9Xsci7C0qNICQM_Ej-8g false --apply --confirm yes
tl --profile vbqppl source-update-corpus 1cIREIoRm6h3P3J3AtJrFqs3HQRQpW-Oc5s768GEkdEc false --apply --confirm yes
tl --profile vbqppl source-update-corpus 1RObiuQRLtSQAW1gNoFq0iXQKm6gkIK_SGzZZuF-7Rmw false --apply --confirm yes
tl --profile vbqppl source-update-corpus 1UfrxU3RIiwNo4qcrTVwlF_cqIoYv99ispT38-nGRWV8 false --apply --confirm yes
tl --profile vbqppl source-update-corpus 1tIHMc_kM_RKQ_T8dAbYmmb84jgoO9bQHb4lhbwqtuKA false --apply --confirm yes
tl --profile vbqppl source-update-corpus 1qhwPZypiqwfCyRIvrQjOIkSdLHeW-ErE3hUyx3dfsoE false --apply --confirm yes
tl --profile vbqppl recat 1JjIPSLJ3Wjpw_15xcxjAFY4RBRxQfKQB1mom1tzeqpE 1cdDxcgyXrnW370yEzqLM8Kn9Xsci7C0qNICQM_Ej-8g 1cIREIoRm6h3P3J3AtJrFqs3HQRQpW-Oc5s768GEkdEc 1RObiuQRLtSQAW1gNoFq0iXQKm6gkIK_SGzZZuF-7Rmw 1UfrxU3RIiwNo4qcrTVwlF_cqIoYv99ispT38-nGRWV8 1tIHMc_kM_RKQ_T8dAbYmmb84jgoO9bQHb4lhbwqtuKA 1qhwPZypiqwfCyRIvrQjOIkSdLHeW-ErE3hUyx3dfsoE --quarantine --apply
```

### GHI-B — PERF_TEST_raw.txt: corpus=false + quarantine
```
tl --profile vbqppl source-update-corpus 12LisxttFh7oIbNitaz_yyBnt6s14IYND false --apply --confirm yes
tl --profile vbqppl recat 12LisxttFh7oIbNitaz_yyBnt6s14IYND --quarantine --apply
```

### GHI-C — P2 (C4/C5 tùy đáp án Q1/Q2)
```
tl --profile vbqppl recat 1wD6qMdqUEpuP-WAX9th_o9vM-E8Hmxxq1TAh5t2Zn6c --cat 39 --apply
tl --profile vbqppl recat 1JSadlq1Cv8OOfWFrVARUAycyhzomY5O0_n6A-YjLuz0 --cat 10 --apply
tl --profile vbqppl recat 1uqmUbNC1Cat8-ntZA7lNmvb1XffdxGmI-vRhMlmA_no --cat 02 --apply
# C4 (CHỈ nếu Q1 = đổi 10): tl --profile vbqppl recat 1-iPFLO80xTDvlBhTiE0W4b_UU-fnB0PwJWXcRGBfJNE --cat 10 --apply
# C5 (theo Q2, 35 hoặc 02):  tl --profile vbqppl recat 1Ks_Ynvw45lIbbtZNjHUoQQHLdGH120_tNCFjgC0C0ps --cat 35 --apply
tl --profile vbqppl register --drive-id 1d3i4NCh-Jo7gZhsmUymabVHXIXcrD8JISzEo5wpvTCE --loai "Phụ lục" --no-autofill --apply --confirm yes
```
(★dòng register GHI NGAY từ lần gọi đầu — không gọi thử, chạy đúng 1 lần SAU duyệt.)

### GHI-D1 — 7 dup/rác rọ 3a: corpus=false + quarantine
```
tl --profile vbqppl source-update-corpus 1asc-wQ0Uhm4KAqNIDFD_lJVexVzlbGzG false --apply --confirm yes
tl --profile vbqppl source-update-corpus 1IN8TN_3HTyUxLaccc5cSMxtzWH3hd5FJ false --apply --confirm yes
tl --profile vbqppl source-update-corpus 1yXg-_VuiMKr_u1ILwAj9-RrdXNQyNa_q false --apply --confirm yes
tl --profile vbqppl source-update-corpus 1NGVXxQCLUWrWG8NGCIM5JfmnBs_2JknX false --apply --confirm yes
tl --profile vbqppl source-update-corpus 1leJoyJKSEfljHj2wPbtdTCkjR7cfEKABfH7k1BUyv8Q false --apply --confirm yes
tl --profile vbqppl source-update-corpus 1aRKrGw6PEkRZvi1MIbb7CfBibe_l8Q3f false --apply --confirm yes
tl --profile vbqppl source-update-corpus 1-Feyc6sgQNq83zQSlO6bCSZkQ0LDMIys false --apply --confirm yes
tl --profile vbqppl recat 1asc-wQ0Uhm4KAqNIDFD_lJVexVzlbGzG 1IN8TN_3HTyUxLaccc5cSMxtzWH3hd5FJ 1yXg-_VuiMKr_u1ILwAj9-RrdXNQyNa_q 1NGVXxQCLUWrWG8NGCIM5JfmnBs_2JknX 1leJoyJKSEfljHj2wPbtdTCkjR7cfEKABfH7k1BUyv8Q 1aRKrGw6PEkRZvi1MIbb7CfBibe_l8Q3f 1-Feyc6sgQNq83zQSlO6bCSZkQ0LDMIys --quarantine --apply
```
(khuyến nghị kèm: note 2 chiều dup↔bản chuẩn theo nếp merge-note lượt 21-22 — soạn khi apply.)

### GHI-D2 — 13 rename (kèm sohieu khi ghi chú)
```
tl --profile vbqppl source-rename 1MZlRu4DcICseY1jpXGL2080vbilN_h79mksFt2xY_c4 --name QD_127-2021-QD-TTG_Chien_luoc_quoc_gia_AI_2030 --sohieu 127-2021-QD-TTG --rename-drive --apply
tl --profile vbqppl source-rename 18-39wTx-jZ9bLTzo51ihyrj2w4G0rcVd87IrRm2Jg-4 --name QD_33-2026-QD-TTG_Danh_muc_he_thong_AI_rui_ro_cao --rename-drive --apply
tl --profile vbqppl source-rename 1ZOTW36-6T58A5VumrbLx9EElXSUdEN90MTS8GYcHfW8 --name ND_353-2025-ND-CP_Co_che_thu_nghiem_cong_nghiep_cong_nghe_so --rename-drive --apply
tl --profile vbqppl source-rename 1T65C_hLSjIhDuhGmNn_L2EYJ_F5TYQsgpp3P-t0Tlx4 --name ND_356-2025-ND-CP_Chi_tiet_Luat_Bao_ve_du_lieu_ca_nhan --rename-drive --apply
tl --profile vbqppl source-rename 1e1KpRRSHzTA1VOzWPTIt2pHj5r9G-RE_hC_Es0gVF_g --name QD_804-2026-QD-TTG_Danh_muc_bo_du_lieu_AI --sohieu 804-2026-QD-TTG --rename-drive --apply
tl --profile vbqppl source-rename 1Weu1RNqWcBqV_CUHZkJTP-3pkKJOWO9AXyVDDbjuz7Y --name Luat_44-2024-QH15_Sua_doi_Luat_Duoc --sohieu 44-2024-QH15 --rename-drive --apply
tl --profile vbqppl source-rename 18_Ybzz8XHRnmilzgDdqgPj5TZGhBwrdKUwsXH7rhtPk --name NQ_112-2026-NQ-CP_Bo_sung_CTLP_2026_sua_Luat_69-2020 --sohieu 112-2026-NQ-CP --rename-drive --apply
tl --profile vbqppl source-rename 1RY7HUHODAvBqUbhe5xcqgA2ojVE3AjBh --name TL_ILO_2019_BC_quoc_gia_Viec_lam_thoa_dang_SDG_VN --rename-drive --apply
tl --profile vbqppl source-rename 1TKqDl_WgCuSxmUe_n6HpiLk3PgCPGJfo --name TL_ILO_Khung_CTQG_Viec_lam_thoa_dang_2022-2026 --rename-drive --apply
tl --profile vbqppl source-rename 1U0L3gIJ9Feie_Hw5SxDsY9WsmrdLi8TY --name TL_ILO_2025_Gioi_va_hoan_thien_chinh_sach_viec_lam --rename-drive --apply
tl --profile vbqppl source-rename 1PWj5iUJb1pcd5Q1TItAeDhuZvqrdgdK2 --name TL_ILO_2026_AI_tao_sinh_va_viec_lam_VN --rename-drive --apply
tl --profile vbqppl source-rename 1nHnfEQDEJao4E_kt8MbE0F9T3NVgNLshEgkLFvRMdA8 --name TT_10-2020-TT-BLDTBXH_Chi_tiet_BLLD_ve_HDLD --sohieu 10-2020-TT-BLDTBXH --rename-drive --apply
tl --profile vbqppl source-rename 1iEiWmiBvd-WTFI2xeWpYy8LlJlDY9xUWk7OB7B0OBbI --name ND_118-2016-ND-CP_Sua_doi_ND_56-2008_ngan_hang_mo_ghep_tang --sohieu 118-2016-ND-CP --rename-drive --apply
```

### 3 câu hỏi cần NGƯỜI trả lời
- **Q1 (P2#4)** `ND_39-2015 hỗ trợ phụ nữ DTTS nghèo sinh con`: GIỮ `08_Dan_so…` hay đổi `10_Dan_toc`?
- **Q2 (P2#5)** `VBHN_09-2026-VBHN-BNV chức năng Sở Nội vụ`: `35_To_chuc_bo_may_nha_nuoc` (khuyến nghị) hay `02_Bao_hiem` (máy)?
- **Q3 (P1#1)** NĐ 176/2025 khuyết Đ1-Đ2: duyệt nạp bản text-first (congbao.chinhphu.vn tự fetch, hay
  user tải TVPL đưa file)? Sau nạp mới quyết số phận bản GDoc khuyết.

### TUỲ DUYỆT (không chặn lô trên)
- r vá auditor: bucket họ-tên-riêng (28 dòng 3c im vĩnh viễn) + neo «Số: X» khi đọc header + cờ NO_TEXT_LAYER.
- r vá doc-text: thêm nhánh fallback export-docx GAS (đường `download` đang sống mà `doc-text` chết).
- Nạp Luật Đấu thầu 22/2023/QH15 nguồn sạch (kho đang trống sau khi quarantine html rác).

## G. Ngoài phạm vi — ghi nhận

- Nợ deploy r275+r276 (v1.36.13/14) thuộc phiên P15 song song; Drive đo được v1.36.12 đầu phiên.
- Ca sheet-dup 2-dòng-cùng-drive_id `1Qja1Lwp…` Kế toán: KHÔNG đụng (đúng dặn).
- 43 dòng row_kind overflow · 6 cụm identity residue: nguyên trạng.
