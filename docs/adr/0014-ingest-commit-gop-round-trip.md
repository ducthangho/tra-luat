# ADR-0014 — `ingest_commit`: gộp organize+rename+upsert+readback thành MỘT round-trip GAS

- **Trạng thái:** Accepted (2026-07-24, r198/v1.35.29 + GAS 2.21.2o — kế hoạch p11 §5, user duyệt từng câu 24-07)
- **Bối cảnh:**
  - Supersede mục **HOÃN `ingest_pipeline`** tại `KE_HOACH_VA_SKILL_r191_r192.md` §3 (23-07). Điều kiện
    mở lại khi đó là «đo lại sau ~1 tuần, ingest lô VẪN nút cổ chai». **User quyết 24-07: số đo 24-07 ĐỦ,
    bỏ cổng-1-tuần CÓ CHỦ ĐÍCH** — căn cứ: đo trên ĐƯỜNG SẢN XUẤT THẬT (lô 14 file ATVSLĐ, song song 4,
    khuôn r192 ĐÃ áp đủ ba van + no-wait + reconcile cuối lô) mà `profile-ingest --apply --no-nlm-add`
    vẫn 53–108 s/file (tb ~78 s), lô 14 = 362 s wall — ingest vẫn ĐỒNG-nút-cổ-chai với NLM (393 s).
  - Cấu phần 78 s: **12 GAS call ≈ 68 s**, trong đó organize 21,1 s · reg_upsert 11,0 s · reg_bulk 10,4 s ·
    **reg_get ×3 + info ×3 = 14 s CHỈ ĐỂ ĐỌC LẠI** · rename 2,3 s. Round-trip thuần ~2 s/call là chi phí
    đường truyền cố định (ping server 51 ms, client 2 028 ms) — giảm SỐ CALL là đòn bẩy duy nhất còn lại.
  - Nỗi sợ cũ khiến HOÃN («gộp server-side phá tính verify-từng-bước/journal/resume») được xử bằng
    **sub-step marker** trong response (xem Quyết định 2) — journal/`--resume` (ADR-0011/D5) vẫn map được
    điểm đứt như đường cũ.
- **Quyết định:**
  1. GAS 2.21.2o thêm action **`ingest_commit`** gộp trong MỘT call: organize (convert→GDoc + xếp cat
     vbqppl / flat root profile) + rename + reg_upsert + readback (row snapshot + file info). Tham số viết
     ĐỦ cho CẢ `ingest-local` (cat routing) lẫn `profile-ingest` (flat) ngay từ đầu — client đời này CHỈ
     dùng nhánh profile (quyết định #6: ingest-local chuyển ở release SAU khi action đã soak).
  2. Response bắt buộc mang **sub-step marker**: `{ok, organize_done, rename_done, upsert_done,
     row: {...}, file: {...}, elapsed_ms}`; lỗi giữa chừng trả **partial marker** (đã-xong-gì) chứ KHÔNG
     im lặng — client ghi journal theo marker, resume đọc lại đúng bước đứt.
  3. Client: helper `_ingest_commit_call` + **feature-detect** version webapp (ping ≥ 2.21.2o → đường gộp;
     cũ hơn → đường 12-call HIỆN TẠI giữ nguyên làm fallback). Journal GIỮ NGUYÊN SỐ BƯỚC intent/commit
     (chỉ giảm số GAS call) — resume contract không đổi.
  4. Trần GAS 6 phút/request: organize 21 s + upsert 11 s còn xa trần; file lớn convert lâu → giữ timeout
     budget phía client, partial marker là van xả. Action ADDITIVE — client cũ (kể cả ≤ r197) không ảnh hưởng.
  5. Thứ tự ship: ADR này → GAS 2.21.2o deploy clasp GIỮ deployment ID (xác nhận `tl ping` = 2.21.2o, đo
     lại sau 25 s) → client r198 bump 3 chỗ + webapp target → gate 9 bước → deploy 5 bước → ĐO lô thật
     ≥3 file, ghi số vào hồ sơ p11 + memory perf.
- **Phương án đã loại:**
  - *Giữ cổng đo-lại ~30-07 rồi mới quyết* — số đo 24-07 đã lấy đúng điều kiện «sau-tối-ưu r192»; chờ thêm
    1 tuần không đổi dữ kiện, chỉ tốn thêm ~40 s/file cho mọi lô nạp trong tuần đó (quyết định user 24-07).
  - *Gộp cả NLM add vào action* — NLM đi cookie phía client, không thuộc thẩm quyền webapp; ba van r192
    giữ nguyên.
  - *Đổi hẳn sang ingest_commit, xoá đường 12-call* — mất fallback khi webapp cũ/rollback GAS; giữ 2 code
    path là NỢ BẢO TRÌ CÓ CHỦ ĐÍCH, gỡ sau khi soak (release riêng, cùng đợt chuyển ingest-local).
- **Hệ quả:**
  - Kỳ vọng đo được: 12 → ~5-6 call/file, ~68 s → ~35-40 s/file trên nhánh profile; số thật ghi tại
    `C:\qh\p11_perf_2026-07-24\KE_HOACH_r196_r197.md` (mục 5c) sau lô đo.
  - 2 code path ingest profile tồn tại song song tới khi soak xong; mọi sửa hành vi ingest phải sửa CẢ HAI
    hoặc chứng minh chỉ chạm một đường.
  - `references/API_CONTRACT.md` thêm spec `ingest_commit`; client không đoán tham số (doctrine tra-trước).
