# PROMPT BÀN GIAO sau lượt 25→29 — 31-07-2026 (bản d, thay cho …-31b / …-31c)

Dán nguyên khối này vào phiên mới. Mốc: master ≥ `6e83da5`, client **v1.36.18**, gói 195 tệp.

## 0. Đọc trước khi làm gì

- `rasoat/KETQUA_US_NLM_QUEUE_2026-07-31.md` (lượt 25, §8-11 = vòng 2 chạy song song P15)
- `rasoat/KETQUA_R1_R3_2026-07-31.md` (lượt 27) · `rasoat/KETQUA_R2_2026-07-31.md` (lượt 28)
- `rasoat/KETQUA_R4_2026-07-31.md` (lượt 29 — **quan trọng nhất, chứa lỗi đang chặn**)
- Phía P15: `rasoat/KETQUA_NLM_QA_QB_QC_2026-07-31.md`, `rasoat/PROMPT_TIEP_NLM_2026-07-31c.md`

**KHÔNG chạy lại** Việc 1-4 lượt 25, Q-A/Q-B/Q-C, R-1, R-2, R-3, và file 1/3 của R-4 — mỗi mục đều có
readback keyed / audit làm bằng chứng.

## 1. Trạng thái corpus↔NLM hiện tại (đã sạch, giữ lấy)

- `nlm-audit-physical` → **rc=0 SẠCH**; `nlm-reconcile --all-notebooks` → **`clean:true`**,
  `desync_real` 0/0/0, `unregistered` 0/0/0.
- **Hai chiều mâu thuẫn sổ↔vật lý đều = 0** (sổ nói-gỡ-mà-còn = 0; sổ nói-còn-mà-mất = 0).
- Slot LIVE (**dùng cột này, KHÔNG dùng registry**): 743ed200 = 299/300 · 45739ff7 = 289/300 ·
  2d8c2fef = 22/300 · 80742228 = 108/300.

## 2. VIỆC ƯU TIÊN — đang CHẶN R-4 (việc CODE, phiên chính làm, KHÔNG giao subagent)

### V-1. Vá `ingest-local --drive-id`: nó TẠO DÒNG REGISTRY TRÙNG
Bằng chứng (lượt 29): sau khi chạy `ingest-local --drive-id 19_6Mp_8e1NQerD5ed42A5TRlO7W14VWt`,
`reg_get` trả **2 dòng** cho drive_id đó; hai file cùng lô **chưa chạy** (`1PWj5iUJ…`, `1h0kl-G4…`)
đều **1 dòng**. Chốt CAS r279 chặn đúng: `EXPECT_AMBIGUOUS_ROWS count=2`.
- Thăm dò an toàn (read-only, KHÔNG `--apply`):
  `tl register --drive-id <id> --corpus true --expect corpus=__khong_bao_gio_khop__ --no-autofill`
  → `EXPECT_MISMATCH` = 1 dòng · `EXPECT_AMBIGUOUS_ROWS` = nhiều dòng.
- ★ `reg-query` **kể cả `--live` GỘP** dòng trùng và báo `count=1` ⇒ **không phải công cụ phát hiện
  sheet-dup**. Chỉ `reg_get` (đường CAS dùng) mới thấy. Cân nhắc bổ sung detector vào `registry-doctor`
  + `sweep` cho lớp lỗi này — hiện KHÔNG detector nào bắt.
- Nhớ: test `rXX_` khoá lại; `python -m ruff check --select F scripts/tl.py` tiêu chí **DELTA so master = 0**.

### V-2. Chưa có đường DỌN một dòng sheet-dup
`reg-delete` **BỊ CẤM** cho ca này (xoá theo drive_id ⇒ xoá CẢ HAI dòng). Cần đường GAS xoá **đúng một
dòng theo vị trí/row index**. Hai ca đang chờ:
- `19_6Mp_8e1NQerD5ed42A5TRlO7W14VWt` (do V-1 sinh ra, lượt 29)
- `1Qja1Lwp…` Kế toán (ca cũ, tồn từ trước — cùng lớp lỗi)

### V-3. R-4 còn 2/3 file — **CHỈ chạy SAU khi V-1 xong**
```
1PWj5iUJb1pcd5Q1TItAeDhuZvqrdgdK2   TL_ILO_2026_AI_tao_sinh_va_viec_lam_VN         sid 9c0611ad  nb 2d8c2fef  cat 23
1h0kl-G4-8l7r_rvOMSlVlXu3su1IwSvU   VBT_BC_BHXH_HaNoi_thuc_hien_CS_BHXH_2025.pdf   sid 52f8ac58  nb 2d8c2fef  cat 02
```
Công thức đã chạy đúng cho file 1 (lặp lại y hệt):
1. `apt-get install -y poppler-utils` (container thiếu) → `tl ocr-analyze <pdf local>` xác nhận
   `text_layer=True`, `garbled=0.0`.
2. `tl --profile vbqppl ingest-local --drive-id <pdf_id> --cat <SỐ> --name <tên không .pdf>
   --no-nlm-add` (DRY) → apply kèm `--confirm yes --expected-plan-hash <hash>`.
   ★ `--cat` phải là **SỐ** (`--cat 02`), **KHÔNG** slug (`--cat 02_Bao_hiem` ⇒ `review_cat` chặn với
   thông điệp gây hiểu lầm "không thuộc 45 chủ đề", dù `cat-list` có liệt kê).
3. **VERIFY NGUYÊN VĂN mức TOKEN** (bắt buộc — skill cảnh báo "PDF = HẠ SÁCH"): so `pdftotext -layout`
   bản gốc với `tl doc-text <gdoc mới>` bằng `collections.Counter` token. File 1 đạt **930/930, thiếu
   0 thừa 0**. **ĐỪNG dùng ratio ký tự thô** — tài liệu có bảng cho ratio ~0.79 dù nội dung y hệt.
4. `tl nlm-add 2d8c2fef-… --drive-id <gdoc mới> --type doc --row-kind own --title <tên>`
   ★ về **đúng notebook cũ 2d8c2fef**, đừng để rơi vào 743ed200 (chỉ còn 1 slot).
   ★ Nguồn thô mang **đúng tên** GDoc mới ⇒ cổng dedup chặn `ALREADY_ON_NOTEBOOK`: **gỡ trước, add
   sau**; TUYỆT ĐỐI không `--skip-live-check`.
5. `tl register --drive-id <gdoc mới> --corpus true --expect corpus= --no-autofill --apply --confirm yes`
6. Hạ dòng PDF cũ `corpus=false` + `nlm-status removed_from_drive` (kèm `--expect`), readback keyed.
> Ghi nhận lượt 29: nguồn thô **tự rụng** khỏi NLM sau bước organize (NLM bỏ nguồn Drive khi file bị
> sửa/di chuyển) ⇒ `nlm-source-remove` trả `noop/ALREADY_GONE`. Đó là ĐÚNG, không phải lỗi.

## 3. Việc của P15 — ĐỪNG nhặt nếu chưa được giao

- **R-5**: đếm lại `CORPUS_TRUE_NOT_ON_NLM` bằng **thước của P15** (luật corpus-effective server).
  Số 53 trong bàn giao cũ đã lạc hậu: lượt 25-28 trả 7 dòng về phủ. (Thước riêng của phiên lượt 25-28
  cho 113 → 106 — **khác thước, đừng trộn hai con số**.)
- Nợ deploy: master đã `v1.36.18` (r279+r280 của P15). **Kiểm Drive trước khi coi là nợ 0**
  (`deploy-guard`), và theo §Quy ước deploy: **phiên nào bump VERSION thì phiên đó đẩy**.

## 4. Tồn kho dài hạn (giữ nguyên, chưa duyệt)

Note dup↔bản chuẩn (cần đường đọc cột note GAS) · lô 3b 43 tên thiếu chủ đề (chạy lệnh quét năm r276
trước) · rọ 3c chờ vá auditor (bucket họ-tên-riêng + neo «Số:» + cờ `NO_TEXT_LAYER`) · vá
`doc-text`/export .docx · nạp Luật Đấu thầu 22/2023 nguồn sạch · 43 `row_kind` overflow · quarantine
hẳn bản khuyết 176 `1auEnrsyEz2FsCW2y39B244uYoSDlva2TgTi2DE9bw50` · BC thẩm tra mẫu P9 ·
`CU_ILO-128` đã xử xong (R-1) — không còn treo.

## 5. NẾP BẮT BUỘC (đều đã trả giá trong lượt 25-29)

1. **Hai phiên chạy song song là chuyện THẬT.** Trước mọi lô ghi NLM: dump `nlm-list` **hai lần liên
   tiếp**, so khớp tập hợp; lệch ⇒ DỪNG, hỏi người dùng. Trước mọi lô ghi registry: dùng
   **`register --expect col=val`** (CAS r279) — rc=3 nghĩa là phiên khác vừa đụng, KHÔNG ghi đè.
2. **`rc=0` không phải bằng chứng.** Bằng chứng ghi DUY NHẤT là **readback keyed** (`reg-query
   --drive-id … --live`, **kiểm `count` TRƯỚC khi tin `rows[0]`**).
3. **Tách stdout khỏi stderr rồi mới parse JSON** — `2>&1` cho `count=None rows=0` GIẢ.
4. **`nlm-content` đo nguồn sống/chết PHẢI kèm `--no-fallback`** — mặc định fallback CORPUS sẽ trả nội
   dung và làm tưởng nhầm nguồn NLM còn sống.
5. **Trạng thái `removed_*` tự nó KHÔNG phải lỗi** — chỉ sai khi **join với LIVE** thấy nguồn còn đó.
   Lượt 28 suýt ghi `pushed` cho 36 dòng, trong đó **32 dòng đã gỡ THẬT** ⇒ sẽ là bịa. Chỉ 4 dòng sai.
6. **"Nguồn sống" ≠ "đáng ở trong corpus"** — phải đối chiếu bản sinh đôi trên Drive (ca `e583ebea`:
   bản Drive nằm `_ZZZ_QUARANTINE_taluat` nên hạ corpus mới đúng).
7. **Trước khi gỡ bất kỳ nguồn nào: kiểm canonical còn phủ không** (bài học BLLĐ 45/2019 — suýt xoá
   sạch một bộ luật khỏi NLM). Trùng thì so **sha256 nội dung** hai bản rồi mới gỡ (ca `CU_ILO-128`,
   ca ref Luật Đầu tư 143/2025).
8. **`register` trả `FIELDS_DROPPED_ON_WRITE` + `verified:false` CHƯA CHẮC hỏng** — webapp bỏ field
   RỖNG. Phải **diff toàn dòng trước/sau** mới kết luận.
9. **`--clear-stale` chỉ chạy sau khi ĐỌC `desync_real_sample`** và xác nhận từng dòng đáng xoá mapping
   — nó có thể nhắm dòng ngoài phạm vi và CHE nợ phủ.
10. **`slot-audit` LIVE là chân lý** — notebook gợi ý trong prompt có thể đã FULL (743ed200 từng
    300/300; phải định tuyến sang shard khác chứ đừng ép).
11. **Không hành động trên id đã truncate** — copy id đầy đủ từ dữ liệu nguồn, không gõ lại từ digest.
12. Console tiếng Việt: `PYTHONIOENCODING=utf-8`. Bootstrap container US: `sh scripts/tl_fetch.sh
    --setup` → `nlm-install --uv` → `nlm-auth-load` → **`nlm-auth-status` phải `alive:true`** (probe
    LIVE là chốt duy nhất, đừng tin `nlm login --check`).

## 6. Kết phiên

Sổ mới `rasoat/KETQUA_<việc>_<ngày>.md` + commit/push (nếp repo: đẩy `HEAD:master`; nhánh dev nếu
harness yêu cầu) + prompt bàn giao mới. `rasoat/` **KHÔNG nằm trong gói** (manifest 195 tệp) nên thêm
sổ không đụng trần 200 và không phải tái sinh `RELEASE_MANIFEST.json`.
