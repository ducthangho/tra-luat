# PROMPT BÀN GIAO sau lượt 30 — 31-07-2026 (bản e, thay cho …-31d)

Dán nguyên khối này vào phiên mới. Mốc: nhánh `claude/nlm-registry-sheet-dup-s22fk7`, client **v1.36.19**,
gói 195 tệp.

## 0. Đọc trước khi làm gì

- `rasoat/KETQUA_R281_V1_V2_V3_2026-07-31.md` (lượt 30 — **quan trọng nhất**)
- `rasoat/KETQUA_R4_2026-07-31.md` (lượt 29 — ⚠ §3 của nó CHẨN SAI, đã bị lượt 30 bác bỏ bằng dữ liệu)
- `rasoat/KETQUA_R1_R3_…`, `KETQUA_R2_…`, `KETQUA_US_NLM_QUEUE_…` · phía P15: `KETQUA_NLM_QA_QB_QC_…`

**KHÔNG chạy lại:** Việc 1-4 lượt 25 · Q-A/Q-B/Q-C · R-1 · R-2 · R-3 · **R-4 (đã đóng: 2/3 file xong,
1/3 dừng có lý do)** · V-1 · V-2.

## 1. ĐÍNH CHÍNH LỚN — «sheet-dup» chưa bao giờ tồn tại

`reg_get` của webapp lọc `o.drive_id === X || o.src_id === X` ⇒ hỏi id một FILE NGUỒN trả kèm dòng GDoc
canonical trỏ `src_id` về nó. **Đo LIVE: 1317 dòng / 1317 `drive_id` phân biệt — 0 dòng trùng khoá**;
162 id rơi vào ca 2-dòng này. Mọi kết luận cũ dựa trên `reg_get count=2` đều SAI:
- «`ingest-local` tạo dòng trùng» (lượt 29) — **SAI**;
- «`1Qja1Lwp…` Kế toán là sheet-dup, CẤM `reg-delete`» (lượt 21) — **SAI** (`doRegDelete_` khớp đúng
  `o.drive_id`, chỉ xoá một dòng — nhưng vẫn KHÔNG có gì để xoá);
- «`reg-query --live` gộp dòng trùng» — **SAI**, nó vốn lọc đúng khoá.

r281 (v1.36.19) đã vá client: mọi đường đọc registry theo khoá chọn dòng `drive_id` KHỚP ĐÚNG thay cho
`rows[0]`; `EXPECT_AMBIGUOUS_ROWS` chỉ nổ khi ≥2 dòng THẬT cùng khoá. Thước mới để trả lời câu hỏi này
trong 1 lệnh: **`sweep.duplicates.by_drive_id`** và **`registry-doctor.duplicate_drive_id_groups`**
(hiện = 0). Thấy `reg_get count=2` thì **đừng suy trùng sổ** — đọc `drive_id` của từng dòng.

## 2. Trạng thái đang SẠCH, đừng làm hỏng (đo LIVE cuối lượt 30)

- `nlm-audit-physical` → **rc=0, `clean:true`**, cả 4 counts = 0 (`pointer_dead` đã về 0).
- `nlm-reconcile --all-notebooks` → **`ok:true, clean:true`**; desync_real / unregistered /
  link_candidates = **0/0/0** cả 3 notebook.
- Slot LIVE (**dùng cột này, KHÔNG dùng registry**): 743ed200 = 299/300 · 45739ff7 = 289/300 ·
  2d8c2fef = 22/300 · 80742228 = 108/300.

## 3. Việc ưu tiên

### U-1. Quyết số phận GDoc khuyết `1N3KuSagQw-M8qzpK9Ia7IvNI-yPYztjtUwfUVMzRFKc`
Drive convert PDF→GDoc **làm rơi số hiệu `3848` và ngày `29`** ở đầu văn bản (`Số: 3848 /BC-BHXH … ngày 29
tháng 6 năm 2026` → `Số: /BC-BHXH … ngày tháng 6 năm 2026`). Xác nhận bằng 2 đường đọc độc lập. Dòng đang
`corpus` RỖNG + `note` `CONVERT_LOSSY_KHONG_DUNG_LAM_CANONICAL…`, KHÔNG trên NLM. Bản corpus vẫn là PDF gốc
`1h0kl-G4-8l7r_rvOMSlVlXu3su1IwSvU` (sid `52f8ac58`, còn sống trên `2d8c2fef`) ⇒ **corpus không hụt**.
Chọn: (a) quarantine hẳn dòng GDoc; (b) vá 2 giá trị rồi verify token/ký tự lại rồi mới promote.

### U-2. Nợ deploy — **phiên này bump VERSION nên phiên này đẩy** (chưa được duyệt ⇒ chưa chạy)
master/nhánh nay **v1.36.19**. Theo §Quy ước deploy: `git fetch origin master` + không tụt sau → chạy
`deploy-guard` đọc version Package đang có trên Drive → chỉ đẩy khi Drive < v1.36.19 → sau đẩy đối chiếu
md5/sha256 + VERSION. **Đừng coi là nợ 0 khi chưa đo Drive.**

### U-3. Lớp lỗi sẽ lặp: `convert_readback` đỏ với file Drive KHÔNG có đuôi
`ingest-local --drive-id` kiểm `source_name_matches` = `<name> + <ext>`; file nguồn trên Drive vốn không
mang đuôi (ca `1PWj5iUJ…`) thì phép kiểm ĐỎ dù mọi thứ khác đúng ⇒ rc=2 giữa chừng, phải làm tay tiếp.
Quyết: đổi tên nguồn trên Drive cho đúng quy ước sidecar, hay nới phép kiểm (chấp nhận tên KHÔNG đuôi khi
Drive vốn vậy)? Nếu nới thì phải khoá bằng test `rXX_` và giữ được ý nghĩa gốc của phép kiểm.

## 4. Tồn kho dài hạn (giữ nguyên, chưa duyệt)

Note dup↔bản chuẩn (cần đường đọc cột note GAS) · lô 3b 43 tên thiếu chủ đề (chạy lệnh quét năm r276
trước) · rọ 3c chờ vá auditor (bucket họ-tên-riêng + neo «Số:» + cờ `NO_TEXT_LAYER`) · vá `doc-text`/export
.docx · nạp Luật Đấu thầu 22/2023 nguồn sạch · 43 `row_kind` overflow · quarantine hẳn bản khuyết 176
`1auEnrsyEz2FsCW2y39B244uYoSDlva2TgTi2DE9bw50` · BC thẩm tra mẫu P9.

## 5. Việc của P15 — đừng nhặt nếu chưa được giao

**R-5**: đếm lại `CORPUS_TRUE_NOT_ON_NLM` bằng **thước corpus-effective của P15**. Số 53 trong bàn giao cũ
đã lạc hậu; lượt 25-28 trả 7 dòng về phủ. (Thước riêng của phiên lượt 25-28 cho 113 → 106 — **khác thước,
đừng trộn hai con số**.)

## 6. NẾP BẮT BUỘC (đều đã trả giá)

1. **Hai phiên chạy song song là chuyện THẬT.** Trước lô ghi NLM: dump `nlm-list` **hai lần liên tiếp**,
   so tập hợp; lệch ⇒ DỪNG. Trước lô ghi registry: `register --expect col=val` (rc=3 = phiên khác vừa đụng).
2. **`rc=0` không phải bằng chứng.** Bằng chứng ghi DUY NHẤT là **readback keyed** — và nay phải hiểu đúng:
   `reg_get` trả cả dòng khớp `src_id`, nên **kiểm `drive_id` của từng dòng**, đừng chỉ đếm `count`.
3. **Tách stdout khỏi stderr rồi mới parse JSON** — `2>&1` cho JSON hỏng/`count=None` giả.
4. **Verify convert PDF→GDoc phải đo ĐA TẬP KÝ TỰ**, không dùng ratio thô (bảng làm ratio tụt còn 0.65 dù
   nội dung y hệt) và cũng đừng chỉ đếm token (token dính nhau che mất chênh lệch). Lượt 30: đa tập ký tự
   bắt đúng 6 chữ số bị mất mà token suýt cho qua.
5. **`nlm-content` đo nguồn sống/chết PHẢI kèm `--no-fallback`**.
6. **Trạng thái `removed_*` tự nó KHÔNG phải lỗi** — chỉ sai khi join với LIVE thấy nguồn còn đó.
7. **"Nguồn sống" ≠ "đáng ở trong corpus"** — đối chiếu bản sinh đôi trên Drive.
8. **Trước khi gỡ bất kỳ nguồn nào: kiểm canonical còn phủ không**, trùng thì so sha256 rồi mới gỡ.
   Guard `POINTER_STILL_ATTACHED` của `nlm-source-remove` chặn đúng — chỉ `--force` khi ĐÃ có bản thay thế
   và sẽ sửa dòng registry NGAY sau đó.
9. **`register` trả `FIELDS_DROPPED_ON_WRITE` CHƯA CHẮC hỏng** — webapp bỏ field RỖNG; và trước r281 nó còn
   có thể là ảo giác do đọc nhầm dòng sidecar.
10. **`--clear-stale` chỉ chạy sau khi ĐỌC `desync_real_sample`.**
11. **`slot-audit` LIVE là chân lý** — notebook gợi ý trong output `ingest-local --no-nlm-add` là
    `suggested_notebook` MẶC ĐỊNH (743ed200, chỉ còn 1 slot); phải tự chỉ đúng notebook đích.
12. **Không hành động trên id đã truncate.**
13. Console tiếng Việt: `PYTHONIOENCODING=utf-8`. Bootstrap container US: `sh scripts/tl_fetch.sh --setup`
    → `nlm-install --uv` → `nlm-auth-load` → **`nlm-auth-status` phải `alive:true`**. Thiếu
    `poppler-utils` thì `apt-get install -y poppler-utils` (cần cho `ocr-analyze`/verify PDF).
14. Ruff tiêu chí **DELTA so master = 0** trên `scripts/tl.py` (nền 12 F821 / 0 F401); tăng ở tl_core/
    selftest thuộc lớp tên-bind là bình thường — tên mới phải vào `_STUB_MAP`.

## 7. Kết phiên

Sổ mới `rasoat/KETQUA_<việc>_<ngày>.md` + commit/push + prompt bàn giao mới. `rasoat/` **KHÔNG nằm trong
gói** (manifest 195 tệp) nên thêm sổ không đụng trần 200 và không phải tái sinh `RELEASE_MANIFEST.json`.
