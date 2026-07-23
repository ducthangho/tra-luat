# ★ v1.35.18 — r188 SEC-01 BOUNDED-READ DOCX/XML + TELEMETRY degraded_reason + DOCS SYNC ADR (2026-07-23)

> Pha D (chốt) kế hoạch review p9 phần-còn-lại. +3 test r188 (1231/1231).

- **SEC-01 — chống zip-bomb DOCX/XML:** engine thêm `read_member_bounded(zf, member)` — đọc member
  STREAMING với TRẦN bytes giải nén (env `TL_DOCX_XML_MAX_MB`, mặc định 50, clamp [1,500]); vượt ⇒
  `ZIP_MEMBER_BOUND_EXCEEDED` (ValueError), member thiếu GIỮ ngữ nghĩa KeyError. Wire 9 điểm đọc:
  `_docx_unzip_text` (doc-text/extract), probe profile-ingest, `docx_markup.scan_file`,
  `normalize_document._docx_zip_text`, the_thuc (check/wrap-scan/landscape + normalize đọc
  TOÀN BỘ member khi repack). Các đường catch-all sẵn có fail-safe "" / scan(0) — không OOM,
  không traceback giữa pipeline.
- **Telemetry degraded_reason (WP5 dứt điểm):** `profile-list --discover` + `profile-sync` nay NỔI
  `degraded_reason` từ scan (SERVER_NO_PROFILE_CATALOG…) lên output JSON như doctor r185 —
  perf gate chỉ được coi xanh trên đường bulk, fallback phải tự khai.
- **Docs sync:** bổ sung 3 ADR bị tham chiếu từ r184 mà chưa có file trong cây:
  `0011-source-revision-tach-khoi-content-identity` (SourceRevision/claim-key/resume gate),
  `0012-marker-transaction-schema-v2` (state machine + v2 + rollout R1/R2 — R2 đã thi hành r186),
  `0013-zip-immutable-plan-bundle` (bundle hash, 1-extract r185, subprocess=0 r187).

# ★ v1.35.17 — r187 WP7 TRACER-BULLET: ENGINE INGEST CHUNG — SUBPROCESS=0 (ZIP) + STAGE SCHEDULER + HASH-ONCE (2026-07-23)

> Pha C kế hoạch review p9 phần-còn-lại (ADR-0004, ticket WP7/R3 ở r185). Module MỚI
> `tl_core/ingest_engine.py` — primitive engine ĐỘC LẬP stdlib (không bind, không import ngược
> tl_core): stage scheduler + hash-once run-scope + child runner in-process. +5 test r187 (1228).

- **Subprocess=0 cho ZIP apply:** `_zip_child_apply_one` chạy child APPLY **in-process** qua
  `run_child_inprocess` (một runner cho cả DRY lẫn apply — `_zip_child_plan_one` cũng ủy quyền);
  stdout/stderr route THEO THREAD (`_ThreadRouteProxy` refcount) — redirect_stdout process-global
  không thread-safe khi N child chạy trong ThreadPool. Giới hạn ghi nhận: (1) không còn timeout
  900s kiểu subprocess — child treo = run treo (GAS client tự timeout tầng dưới); (2) chunking/OCR
  vẫn `_run_child_tl` subprocess — NGOÀI scope ticket (ticket chỉ định child ingest-zip).
- **Stage scheduler (upload≤2, NLM≤2):** `stage_slot(stage)` BoundedSemaphore per-process; wire
  6 call-site: 2 upload (`profile-ingest`, `ingest-local`) + 4 `source_add` (profile-ingest,
  chunks, resume, ingest-local). Stage lạ = không giới hạn. Registry đã một lane từ r185/ING-05.
- **Hash nguồn ĐÚNG 1 lần/run (kể cả child plan):** `ingest_contract.sha256_file` ủy quyền
  `hash_file_once` — trong `run_scope()` (nest được) memo theo realpath; `_zip_plan_bundle` +
  `_zip_apply` mở scope trọn invocation → archive+member+child-plan hash 1 lượt (test đo:
  bundle = 1 compute, extract-verify memo-hit). Ghi nhận trade-off: re-hash archive giữa
  plan↔extract trong CÙNG run thành memo-hit — guard thẩm quyền là so sha256 TỪNG member lúc
  extract (GIỮ NGUYÊN, test ZIP_MEMBER_CHANGED_OR_CORRUPT còn đỏ đúng). Ngoài scope: hành vi cũ.
- Test r184/r185 zip apply chuyển patch funnel `_run_child_tl` → `_zip_child_apply_one` (đúng
  đường mới); +r187: cap concurrency đo bằng thread, hash-once trong/ngoài scope, routed-io 2
  thread song song bắt đúng stdout riêng, apply không đụng subprocess (fake raise nếu gọi).
- Golden regen CÓ CHỦ ĐÍCH (user duyệt): workflow_audit `py_size.files_scanned` 66→67 — đúng 1
  dòng, do file module MỚI `tl_core/ingest_engine.py` (không phải diff hành vi).

# ★ v1.35.16 — r186 R2 MARKER WRITER v2 + FAIL-CLOSED BODY + MIGRATION CANARY (2026-07-23)

> Pha B kế hoạch review p9 phần-còn-lại (P10). Reader v1/v2 đã LIVE từ r184 ⇒ flip WRITER an toàn
> (client cũ 1 phiên bản vẫn đọc v1; marker mới phát v2). +5 test r186 (1223). Offline-only — mọi
> migration LIVE trên profile thật vẫn chờ user duyệt plan.

- **Writer v2 (ADR-0012 R2):** `_marker_body` phát `schema=tra_luat_profile.v2` + `fingerprint`
  (sha256 canonical-JSON, đóng dấu CUỐI sau mọi trường); tham số mới `meta_id` = fallback
  `metaFolderId` khi prof thiếu (marker luôn nằm trong chính `_meta` được ghi) — rename/set-meta
  truyền `mr.meta_folder_id`.
- **Fail-closed TRƯỚC upload:** `_marker_write` validate body (`_marker_validate`) trước mutation —
  v2 thiếu trường bắt buộc theo `manifestScope` / fingerprint lệch ⇒ `status=REJECTED`, 0 call Drive,
  journal ghi errors + repair (own-scope cần notebookId/registryDocId/manifestId). Hết cửa tạo
  marker hỏng rồi mới phát hiện qua doctor.
- **Migration canary:** `profile-doctor --plan-marker-migration` chốt plan qua
  `_migration_plan_finalize` (PURE) — sort tất định, phần tử ĐẦU `canary=true`, action chạy được
  per-profile `tl profile-backfill-markers --profile-name <p> --apply --force` (canary trước →
  verify doctor sạch → mới đại trà; --apply do user duyệt). Note doctor MARKER_SCHEMA_V1 cập nhật.
- Fixture selftest vá-trường-sau-`_marker_body` re-mint fingerprint (`_remint186`) — marker giả lập
  không thành "v2 fingerprint lệch" bị validate chặn oan; r86 defaults đổi kỳ vọng schema→v2;
  fixture minimal thêm `metaFolderId` (v2 bắt buộc).

# ★ v1.35.15 — r185 WP5-WP6 PERF: BULK PROFILE (GAS 2.21.2n) + ZIP 1-PASS + D7 RAM BUDGET + REGISTRY LANE (2026-07-23)

> Thi hành WP5-WP6 kế hoạch review p9 (D3/D6/D7). GAS **2.21.2n** = 2.21.2m ⊕ 2 endpoint CỘNG THÊM
> CHỈ ĐỌC: `profile_catalog` (snapshot Van_ban_thuong 1 call — items + _meta + NỘI DUNG mọi marker)
> và `drive_info_bulk` (metadata ≤200 fileId 1 call, giữ thứ tự input). Client try-first + fallback
> tương thích server cũ (`degraded_reason` — perf gate chỉ xanh trên đường bulk). +9 test r185 (1218).

- **WP5 — call budget D6 (đo bằng test đếm call trên fake GAS):**
  · `profile-list --discover` / `profile-sync`: scan = **1 call** `profile_catalog` (tổng ≤2 kể bootstrap),
    KHÔNG tăng theo 1/10/50 profile (trước: ~3×N call list/list/download-marker).
  · `profile-doctor` shallow 50 profile: **≤3 GAS** (bootstrap + catalog + info_bulk; marker đọc từ
    catalog, asset info từ bulk — 0 call `info`/`list`/`download` trong vòng lặp).
  · `profile-doctor --deep` 1 profile, 300 nguồn + 50 template: **≤4 GAS + 1 NLM** — `reg_get_bulk`
    lô 300 (0 `reg_get` lẻ; ghi nhận: bulk 1 row/sid — sid nhiều row chỉ thấy row cuối, ca hiếm);
    template probe từ info-bulk prefetch (0 download-để-kiểm-tồn-tại; location theo parents,
    'shared' resolve LƯỜI ≤1 lần/run).
  · `profile-sync --apply`: `_persist_profiles_config_bulk` — TOÀN BỘ diff ghi config NGUYÊN TỬ
    **1 lần** + 1 journal run (trước: N lần read-modify-write + N run).
- **WP6 — I/O/RAM (ING-03/ING-05/D7):**
  · ZIP apply: **1 extract + 1 lượt hash member/invocation** — bundle lập từ CHÍNH lần extract của
    apply; bỏ pre-pass recompute trùng lặp (drift do authorize bắt: `PLAN_HASH_MISMATCH` + note
    `PLAN_DRIFT_REPLAN_REQUIRED`). Trước r185: 2 extract + hash member ×3.
  · D7: `TL_INGEST_MEMORY_BUDGET_MB` (mặc định 256, clamp 64-4096); `workers_effective =
    min(requested, 4, floor(budget / (32MiB + 2,5×size_max)))` — hard cap 4 (trước cap 8 không đếm
    RAM); plan/apply CÔNG KHAI `resources{workers_requested/effective, peak_memory_estimate}`;
    không đủ 1 worker ⇒ `INSUFFICIENT_MEMORY_BUDGET` DỪNG TRƯỚC mutation.
  · ING-05: `_verified_reg_write`/`_journaled_reg_write`/`_verified_reg_upsert` đi **một lane RLock**
    trong process (8 thread không chồng nhau — test đo max-concurrency=1). GIỚI HẠN GHI NHẬN: chưa
    phủ child SUBPROCESS ingest-zip (row khác nhau + claim F-04 che; lane xuyên-process = WP7).
- **Còn lại WP6 (ticket WP7/R3):** subprocess child ingest-zip → in-process engine (subprocess=0,
  member hash đúng 1 lần kể cả child plan); stage scheduler upload≤2/NLM≤2; GWS streaming upload;
  SEC-01 bounded-read DOCX/XML.
- EXPECT_VERSION → **2.21.2n**; API_CONTRACT đóng dấu 2.21.2n + 2 action mới; GAS deploy qua clasp
  giữ URL NGAY SAU deploy skill (thứ tự an toàn: client-có-fallback lên trước server).

# ★ v1.35.14 — r184 REVIEW P0: GATE ARTIFACT + MARKER TRANSACTION + IDENTITY/RESUME + ZIP BUNDLE (2026-07-23)

> Bốn vá P0 từ review hiệu năng/đúng đắn Profile+ingest (kế hoạch grill-with-docs 23-07, workspace
> `C:\qh\p9_review_v13512_2026-07-23` — evidence register 11/12 CONFIRMED). Fork v1.35.12, merge 3-way
> lên r183 (giữ nguyên vá gdoc --markup); +23 test r184 (1209/1209).

- **REL-01 — gate xanh giả trên artifact**: v1.35.12 deploy-zip fail 4 selftest (r67/r125/r127/r128) vì
  SKILL.md trỏ `references/changelog_archive/` (release-exclude) — cây dev xanh (exists() trên đĩa),
  artifact đỏ. Vá: `_skill_links_findings` (PURE) đối chiếu link SKILL.md với PACKAGE-SET của manifest,
  wire fail-closed vào `_verify_release_manifest` (`SKILL_LINKS_NOT_IN_PACKAGE` + `skill_links` trong
  release-verify); gỡ con trỏ dev-only khỏi kernel (không nới auditor).
- **PRO-01 — marker false-success (ADR-0012)**: `_marker_write` thành state machine journaled
  upload → FULL readback (so TRỌN payload — hết so 3 trường) → enumerate (HẾT nuốt `except: pass`) →
  cleanup → PROVE-ONE (re-list chứng minh 0 marker dư) → commit; trả `status COMMITTED/PARTIAL/FAILED`
  + `phases` + repair action trong journal. 6 caller (rename/adopt/create/backfill/promote/set-meta)
  chuyển `verified&&cleanup_ok` → `ok` trọn chuỗi. Reader hiểu marker v1/v2 (`tra_luat_profile.v2`,
  bộ trường bắt buộc theo manifestScope, fingerprint) — R1 writer GIỮ v1; `_marker_mutation_guard`
  chung; `profile-doctor --plan-marker-migration` (DRY, migration ghi ở R2).
- **ING-02 — identity đội lốt + resume mù nguồn (ADR-0011/D4-D5)**: `identity_hash_for_drive_source`
  hết nhét sha256(drive_id) vào slot content_hash — retype thành `build_source_revision`
  (identity_strength revision/metadata) + `claim_key_for_source` (payload KHÔNG có content_hash;
  observed_at CỐ Ý ngoài khóa). ⚠ giá trị claim key ĐỔI — 2 host lệch version không khóa chéo trong
  cửa sổ rollout (TTL 5'). `profile-ingest` apply NAY CÓ JOURNAL (name/sha256/identity_hash/plan_hash/
  drive_id + run_end). Resume: name-only = DRY REPAIR (mode `DRY_REPAIR`, 0 mutation, 1 phiên bản
  chuyển tiếp); `--apply` đòi `--journal <run_id>` HOẶC `--drive-id` + fingerprint khớp registry
  (`_resume_identity_gate` PURE); journal legacy → `LEGACY_JOURNAL_REPLAN_REQUIRED`; lệch →
  `RESUME_IDENTITY_MISMATCH`. CLI profile-ingest/profile-file-add + `--journal`.
- **ING-01 — ZIP self-confirm (ADR-0013)**: DRY (`ingest-zip`/`profile-ingest-zip` có --cat) lập ĐỦ
  child plan IN-PROCESS (`_zip_child_plan_one`, 0 subprocess DRY) → `plan_hash` = fingerprint TOÀN
  bundle (archive+member+mọi child plan, `ingest_zip_bundle.v1`). Apply: authorize trên bundle hash;
  pre-pass tuần tự recompute từng child — khác bundle đã duyệt ⇒ `PLAN_DRIFT_REPLAN_REQUIRED`,
  0 mutation; `--confirm yes` cho child CHỈ với hash NẰM TRONG bundle user duyệt (hết tự-phê-duyệt);
  journal record `plan` bundle + intent per-member. ⚠ plan hash ZIP cũ (chỉ parent) hết hợp lệ — DRY
  lại lấy bundle hash. DRY vbqppl KHÔNG --cat giữ DRY phân loại (note_bundle).
- Bẫy merge: msys sed text-mode TƯỚC 
 → 3 file CRLF (tl.py/tl_selftest/command_registry) thành
  whole-file-diff giả 19k dòng; khôi phục CRLF trước merge. Kernel 48.190B > 47K warn sau merge —
  rút gọn dòng bảng CHANGELOG-sâu về 48.121B. Golden regen CÓ CHỦ ĐÍCH: parser_surface (cờ CLI mới),
  workflow_audit (links 15→14).

# ★ v1.35.13 — r183 NGUỒN GOOGLE DOC: `--markup` HẾT LÀ NO-OP IM LẶNG (2026-07-23)

> **BẪY IM LẶNG — nguy hiểm hơn bug thường vì công cụ báo THÀNH CÔNG.** r182 vá 3 reader `.docx`, nhưng
> **nhánh Google Doc của `_doc_text_any` không hề đụng `docx_markup`**: nó đi `_read_doc_text` (export
> **text/plain**) — đường này san phẳng mọi định dạng, GIỮ CHỮ mà MẤT gạch-bỏ. Cờ `--markup` bị bỏ qua
> HOÀN TOÀN, vẫn rc=0, không một dòng cảnh báo.
>
> **Đo tươi 23-07-2026** (Dự thảo Luật BHXH 16/7, `1ltPv6AwO72wglCpEitkT7tmu-GZ3zPEGhTObiKF8p4s`): qua
> `drive_id` **mọi chế độ = 25.339 ký tự** (≈ bản thô), **0 nhãn ⟦BỎ⟧**; từ `.docx` gốc: strip **21.131** /
> mark **25.503** (60 nhãn) / raw 25.032, `docx_markup.scan_file` = **63 khối `w:strike`** ⇒ **4.405 ký tự
> chữ ĐÃ BỎ bị đọc như quy phạm hiện hành**. Tác hại đã xảy ra: **6 phát hiện SAI** trong một đợt rà soát
> («tối đa là 12 tháng», «phải được chứng thực», «là cơ quan nhà nước», «trước liền kề tháng»), phải chạy
> trọn một đợt sửa hơn 60 chỗ trên 10 file.
>
> **Vá — đi CẢ HAI hướng, vì không hướng nào đủ một mình:**
> (a) **LẤY CHO ĐƯỢC MARKUP** — `_gdoc_docx_text`: Google Doc + chế độ lọc ⇒ **export `.docx`**
> (`_doc_text_fetch_binary(..., export_mime=…wordprocessingml.document)`; `alt=media` KHÔNG tải được
> Docs-native) rồi qua CHÍNH bộ lọc `docx_markup` như nhánh .docx — source mới `gdoc-docx`. Hướng này cứu
> được các bản Google Doc CÒN giữ dấu vết (gạch-bỏ thủ công/suggestion), nhưng KHÔNG cứu được bản đã mất
> markup lúc convert ⇒ phải có (b).
> (b) **KHÔNG LẤY ĐƯỢC THÌ NÓI THẲNG** — export .docx fail, hoặc bản convert không còn dấu vết nào
> (del=0/strike=0/ins=0), hoặc text lấy từ **cache không kèm chứng nhận đã-lọc** ⇒ **CẢNH BÁO stderr**
> `[markup] ⚠ …` + khai vào `meta`/JSON (`markup_filter_ran`, `markup_found`, `markup_warning`).
> `--markup raw` = đối chứng CÓ CHỦ ĐÍCH ⇒ không cảnh báo. **IM LẶNG LÀ HÀNH VI ĐÃ LOẠI BỎ.**
>
> **`--markup-strict`** (mới): có cảnh báo ⇒ **TỪ CHỐI in văn bản, rc=3** (`MARKUP_UNVERIFIED`). Dành cho
> pipeline thẩm tra: thà thiếu văn bản còn hơn có văn bản mà người đọc tưởng đã lọc.
>
> **SIDECAR chứng nhận cache** `extract_<id>.txt.markup.json` (`{v, filter_ran, found, source}`): cache cũ —
> nhất là do `tl extract` ghi từ export text/plain — KHÔNG có sidecar ⇒ lần đọc sau **cảnh báo + gợi ý
> `--refresh`** thay vì im lặng tái diễn đúng bẫy cũ. Thêm `_read_doc_text(..., use_cache=False)` cho
> mark/raw (cache là bản CHUẨN strip — trả nó cho chế độ khác cũng là một kiểu im lặng).
>
> **CẮT STDOUT PHẢI BÁO** — `--max` cắt làm hai chế độ về CÙNG số ký tự và trông y hệt nhau (đúng cái bẫy
> suýt làm chẩn sai hôm 23-07): nay in `⚠ ĐẦU RA BỊ CẮT: x/y ký tự … dùng --max 0 --out <file>`.
>
> **TDD 5 ca ĐỎ→XANH** (đo trước vá: 5/5 FAIL, không ca nào khác đổi): `r183_gdoc_strip_qua_docx_export` ·
> `r183_gdoc_mat_markup_canh_bao` · `r183_markup_strict_tu_choi_rc3` · `r183_canh_bao_cat_stdout` ·
> `r183_cache_cu_khong_chung_nhan_canh_bao`. Selftest **1186/1186**.
>
> ★ **ĐO ĐƯỢC KHI DỰNG CA:** hai test double cũ của `r121` (`_read_doc_text` lambda không nhận `**kw`) làm
> ca ĐỎ vì `TypeError` bị `except Exception` của `_doc_text_any` NUỐT — đúng lớp lỗi âm-tính-giả mà chính
> r183 đang vá; đã nới double.
>
> ★ **DOCTRINE:** bản TRONG KHO không đương nhiên là bản dùng được làm căn cứ; với tài liệu có markup,
> **file `.docx` GỐC mới là nguồn chuẩn**. Công cụ không chứng minh được đã lọc thì PHẢI NÓI — không được
> để người dùng tự suy ra từ rc=0.
>
> **Còn mở:** `tl extract` trên Google Doc vẫn đọc bằng export text/plain (chưa có cờ `--markup`) — nay
> cache do nó ghi bị doc-text cảnh báo là CHƯA CHỨNG NHẬN; để vòng sau.

# ★ v1.35.12 — r182 ĐỌC ĐÚNG .docx CÓ MARKUP SỬA ĐỔI (cả 3 reader sản xuất đọc SAI dự thảo) (2026-07-22)

> Lỗi ĐÚNG-SAI về NỘI DUNG PHÁP LUẬT (không phải lỗi hình thức): mọi đường đọc .docx đều lấy chữ ĐÃ BỎ làm
> quy phạm CÒN HIỆU LỰC. **Đo TƯƠI qua ĐÚNG hàm sản xuất TRƯỚC khi vá — 20 sai / 4 đường đọc:** nhánh
> python-docx của `normalize_document._docx_to_text` GIỮ chữ `w:strike` và MẤT chữ `w:ins` (python-docx bỏ
> run không phải con TRỰC TIẾP của `w:p`); hai nhánh strip-tag — `lookup_ops._docx_unzip_text`
> (`tl doc-text`; doc-compare/dedup/nlm qua `_doc_text_any`) và `ingest_ops._profile_read_probe_text` (cổng
> nạp, DRY phân loại) — giữ CẢ `w:delText`. Bảng (`c.text`) CÙNG LỖI.
>
> ★ **TỰ KIỂM BÁC BỎ GIẢ ĐỊNH BAN ĐẦU:** `tl doc-text`/`tl extract` **KHÔNG** đi qua `_docx_to_text` ⇒ vá mỗi
> `normalize_document` là CHƯA chạm đường tra cứu (P6 vẫn sai). `_docx_to_text` chỉ phục vụ đường NẠP;
> `tl extract` đọc GDoc bằng export GAS. Bài học: xác minh call-graph trước khi tin phạm vi một bug.
>
> **Vá:** module dùng chung `scripts/docx_markup.py` (zero-dep) — bỏ `w:del`/`w:moveFrom`/`w:delText`, BÓC VỎ
> `w:ins`/`w:moveTo`, bỏ run `w:strike`/`w:dstrike` (tôn trọng `w:val="false"` = đè TẮT), quét
> `w:rPrChange`/`w:pPrChange` TRƯỚC khi dò strike (rPrChange lưu ĐỊNH DẠNG CŨ ⇒ dễ tưởng run hiện tại bị gạch).
> Cả 4 đường đọc + CẢ BẢNG dùng CHUNG bộ lọc; phát hiện markup → CẢNH BÁO stderr. Chế độ: `strip` (mặc định —
> bản chuẩn vào cache) · `mark` ⟦BỎ:…⟧ · `raw` (đối chứng). CLI: `tl doc-text --markup`,
> `normalize_document --markup-mode auto` (auto = **mark cho DỰ THẢO / strip cho VBQPPL đã ban hành**).
> mark/raw KHÔNG đọc/ghi cache `extract_<id>.txt` (giữ corpus sạch nhãn).
>
> ★ **ĐO ĐƯỢC KHI DỰNG CA TDD (giả thuyết ban đầu SAI):** bản `mark` KHÔNG an toàn cho parser — `ART_SPLIT`
> đòi CHỮ HOA ngay sau "Điều N." nên nhãn `⟦` CHẶN Điều THẬT, còn `:` trong `⟦BỎ:` lại THOẢ lookbehind
> `[\s.;:]` nên tiêu đề ĐÃ GẠCH BỎ đẻ ra "Điều ma" (đo: `split_articles(mark)` = `[5]`, MẤT `[1]`).
> Không nhãn nào chữa được cả hai chiều ⇒ **CẤU TRÚC LUÔN phân tích trên bản `strip`**; mark/raw chỉ đi vào
> `text_markup` (bản XEM). Nhãn phải là phần tử `w:t` THẬT — python-docx CHỈ nối `w:t`, chèn text trần thì
> nhánh lib nuốt nhãn còn nhánh strip-tag giữ ⇒ hai đường đọc lệch nhau.
>
> **BÁN KÍNH HỒI QUY = 0 (đo trên kho THẬT):** quét 210 .docx — **200 file sạch markup cho text `strip` ≡ `raw`
> (bytes y hệt) 200/200**; 10 file có markup đều là DỰ THẢO (`strike`, cao nhất 102 và 63). Đối chứng dự thảo
> 16/7/2026: `"là cơ quan nhà nước"` 1→0, `"12 tháng"` 1→0, `"chứng thực"` 3→0 — **đúng nguồn gốc 3 "phát hiện"
> sai của GĐ5–GĐ7** (4.098 ký tự đã gạch bỏ từng bị đọc như quy phạm sống).
>
> **Gate:** selftest **1181/1181** (+9 ca r182; nền 1172 GIỮ NGUYÊN) + gen_instructions 38/38; golden regen
> ĐÚNG 2 khoá có chủ đích (`doc-text` parser surface do thêm `--markup`; `workflow_audit.files_scanned`
> 65→66 do thêm 1 module). **Đối chứng bằng revert 7 chốt:** mỗi chốt có ca VÂN-TAY RIÊNG
> (N1→lib · N2→zip · N3→doc-text · N4→cổng nạp · N5→chỉ điều-ma · N6→chỉ cache · N7→nhãn), "FAIL khác = 0" mọi lượt.
>
> **KERNEL:** thêm bất biến **19** — (a) rà dự thảo PHẢI ĐỌC KÈM TỜ TRÌNH (tách MỤC TIÊU CHÍNH SÁCH khỏi CÂU
> CHỮ QUY PHẠM; phần lớn "vênh" là KHÁC TẦNG) · (b) markup = ĐÃ BỎ / MỚI THÊM, không kết luận trên bản chưa
> lọc · (c) MỌI KHẲNG ĐỊNH PHÁP LÝ verify NGUYÊN VĂN qua `get_legal_article`/`tl extract`, **CẤM nêu theo trí
> nhớ**. Bù byte theo khuôn kernel-diet: khối ADR-0003 trích NGUYÊN VĂN sang `references/KERNEL_APPENDIX.md`
> §D ⇒ SKILL.md 48.115 → **48.061 B** (dưới trần 47K, biên 67 B).

# ★ v1.35.11 — r181 HERMETIC SELFTEST+GOLDEN + CHECKPOINT MKDIR (nền+gate xanh dưới defaultProfile «Luật BHXH») (2026-07-22)

> Nối r180: cổng khởi động phát hiện selftest nền LỆCH **1167/1169** trên ĐÚNG commit `e45571a` (cây sạch,
> HEAD/VERSION khớp) → dừng đúng luật, chẩn gốc READ-ONLY. Hai ca resume/checkpoint (`r20`/`r30`) đỏ do
> **selftest KHÔNG hermetic w.r.t. defaultProfile máy**: S10 lật default `vbqppl`→«Luật BHXH» (config gitignored
> nên cây git vẫn sạch) + một ca sớm gọi `apply_profile_offline(config THẬT)` **leak** `TL_PROFILE=«Luật BHXH»`
> tới r20/r30 (cleanup env ở sau). Đo TƯƠI bằng probe-file: ckpt rơi vào `…\Luật BHXH\corpus_audit_ckpt_all.json`
> — mà `_ckpt_save` **NUỐT OSError** khi thư mục cha thiếu → checkpoint resume ghi HỤT im lặng → không hội tụ.
> Vá cả 2 (user duyệt P1); **gate bước 5/6 (golden-test, determinism-audit) cũng đỏ TIỀN TỒN cùng gốc** (kiểm
> `git stash` về r180: rc=2 y hệt; `TL_PROFILE=vbqppl golden-test` → xanh 100% ⇒ goldens ĐÚNG, chỉ non-hermetic)
> → thêm **Fix3**. Mỗi vá 1 ca **CHỈ-NÓ-CHẶN** (đối chứng revert đủ 3). selftest **1172/1172** (+3 ca r181; nền
> 1169 GIỮ NGUYÊN) + gen_instructions **38/38** + gate 9 bước TOÀN XANH.

- **Fix1 (production) — `_ckpt_save` mkdir thư mục cha** (`hygiene.py` `cmd_corpus_audit`): thêm
  `_ckpt.parent.mkdir(parents=True, exist_ok=True)` trước `write_text`. Bịt lỗ THẬT: profile mới toanh / phiên
  đầu, cache-subdir chưa tồn tại → `FileNotFoundError` bị `except OSError: pass` nuốt → mất tiến độ resume im
  lặng (nghịch ý checkpoint chống-hỏng-dữ-liệu). Ca `r181_ckpt_save_mkdirs_missing_parent` (ép
  `_profile_cache_dir()`→subdir chưa có; đo checkpoint GHI ĐƯỢC + resume 2 lượt hội tụ + tự dọn). Cô lập:
  revert mkdir → **CHỈ** ca này đỏ (1170/1171), r20/r30 vẫn xanh (Fix2 pin cứu về base cache).
- **Fix2 (harness) — `selftest()` ghim `TL_PROFILE=DEFAULT_PROFILE`** (`tl.py` `_selftest_pin_profile`/
  `_selftest_restore_profile` + wrap bare selftest, restore ở finally ngoài): hermetic w.r.t. defaultProfile
  máy, miễn nhiễm mọi leak env giữa suite (đúng doctrine "bare selftest must be hermetic"). Ca
  `r181_selftest_pin_profile_hermetic` (env non-default giả lập → pin đưa `active==DEFAULT` &
  `_profile_cache_dir()==CACHE`, `restore` trả nguyên env). Cô lập: neuter thân pin → **CHỈ** ca này đỏ
  (1170/1171), r20/r30 vẫn xanh (Fix1 mkdir cứu). Call-site xác nhận bởi nền-xanh-dưới-«Luật BHXH».
- **Fix3 (gate) — golden-test tự-hermetic** (`workflow.py` `_golden_env`): LUÔN tiêm `TL_PROFILE=DEFAULT_PROFILE`
  vào env mỗi subprocess golden (goldens là artifact NỀN; subprocess kế thừa defaultProfile máy — nếu ≠ nền thì
  `reg-query` trả `base_also` / corpus·đếm theo overlay → golden ĐỎ GIẢ; determinism-audit đỏ ăn theo vì gọi
  `_golden_test` in-process). Case tự khai `TL_PROFILE` thì tôn trọng (setdefault); đường `--write` nhờ đó regen
  dưới ĐÚNG nền. Ca `r181_golden_env_pins_base_profile` (máy-độc-lập). Cô lập: revert `_golden_env` → **CHỈ** ca
  này đỏ (1171/1172). 6 ca golden đỏ (`hygiene_*` + `doc_text_cache_fixture`) là TIỀN TỒN r180, r181 thêm 0 đỏ.
- **Doctrine:** nền/gate có thể LỆCH mà cây git SẠCH khi trạng thái sống (defaultProfile) ở config **gitignored**
  → cổng khởi động PHẢI đo selftest **VÀ gate** TƯƠI, không tin "cây sạch = xanh". Mọi lệnh hermetic-CI (selftest,
  golden-test/determinism) phải trung hoà active-profile về DEFAULT (thêm cache-dir với selftest).

# ★ v1.35.10 — r180 THĂNG FAIL 8 Ô TT-DT (ADR-0009 Đ3) + 7 FIX GĐ2/CỔNG-1 (2026-07-22)

> Phiên grill-with-docs 22-07: xử lý log vận hành GĐ2+Cổng-1 «Luật BHXH» (S1-S10/D1-D7 — mỗi quyết
> định user duyệt từng câu) + việc mở #1 của bàn giao: thăng FAIL từng ô lớp TT-DT theo chuẩn
> zero-oan tuyệt đối. selftest **1169/1169** (+18 ca r180; nền 1151 GIỮ NGUYÊN).
> Hồ sơ đo tươi + đối chiếu tay: `D:\Quốc hội\thang-o-2026-07-22\` (ket_luan_doi_chieu.md).

- **THĂNG FAIL 8 (hệ·ô·trục) — user duyệt từng ô 22-07** (the_thuc.py `_THANG_FAIL` inline — bẫy I11):
  `hanh_chinh·noi_nhan_ds·co` · `hanh_chinh·noi_nhan_tu·co` · `hanh_chinh·ten_loai·co` ·
  `hanh_chinh·dia_danh·kieu` · `dang·the_loai·co` · `dang·dia_danh·co` · `dang·so_ky_hieu·co` ·
  `dang·dia_danh·kieu`. Đo TƯƠI production v1.35.9 trên 159 file (129 corpus ngâm + 30 mới), lớp A
  191 WARN đối chiếu tay TỪNG finding; chỉ thăng vi phạm ĐO ĐƯỢC (nhánh «cỡ không khai báo» giữ WARN
  — guard `chua_do`); B3/tin-cậy-thấp giữ INFO vĩnh viễn (Đ1); trục chưa duyệt giữ WARN. Ô CÓ oan ở
  lại WARN kèm hồ sơ: `dieu·kieu` (neo ăn câu trích dẫn Điều trong báo cáo 9/9), `de_muc_than` (ăn
  khối ký/đuôi tiêu đề), mọi ô canh both≈left, cụm dàn-trang-bằng-indent (TB_20), gach=đường-kẻ
  (tieu_de Đảng/tiêu ngữ), thut lệch <3mm (thut='0' không dung sai). Khoá 10 ca selftest ba chiều
  (FAIL thuận · WARN nghịch · INFO bất khả xâm); fixture r136/r143 nắn ĐÚNG thể thức (địa danh
  nghiêng, «Nơi nhận:» 12pt — sửa fixture, KHÔNG nới bộ kiểm) + biến thể `_VN136_NOSZ`.
- **S1 — cổng OCR đường corpus NỀN** (`_ingest_local_ocr_gate` PURE + nối `cmd_ingest_local`):
  `--source-quality ocr` ∧ ¬`--ocr-verified` ⇒ ép đường no-nlm-add, registry corpus=false + note
  `OCR_UNVERIFIED_NOT_CORPUS`, rc=2 kèm next_steps ocr-verify/ingest-ocr; DRY plan mang `ocr_gate`.
  (Hố 21-07: Hiệp định VN–Hàn scan vẫn corpus=true — ingest-local coi cặp cờ là trang trí trong khi
  profile-ingest gate cứng; nay MỘT cổng MỘT luật.)
- **S2 — `source-update-corpus false --as-ref` (HẠ REF một bước):** corpus=false + row_kind=ref,
  GIỮ nguồn NLM + nlm_status họ sống (ca ILO C102 hết 3 bước xoá-rồi-add-lại); shared_source_id
  KHÔNG chặn nhánh này (không đụng NLM); journal ghi before row_kind thật. CONTEXT.md +«Hạ ref».
- **S3 — extract resolve --sohieu ĐỌC CỘNG NỀN dưới --profile** (`_extract_resolve_entries` mirror
  base-also reg-query, hit nền scope='vbqppl'). Chẩn đoán log SAI HƯỚNG nhưng bệnh thật: không phải
  thiếu pattern VPQH mà là thiếu base-also (đo 22-07: `52-2025-VPQH` resolve ngon KHÔNG profile,
  fail DƯỚI profile). Ghi nhận data: sohieu Hiến pháp `52-2025-VPQH` thiếu token VBHN — sổ hygiene.
- **S4 — DRY .doc cũ hết phán chắc** (`_profile_dry_gate_soften` PURE): NO_TEXT_FOR_VERIFY trên
  .doc binary (không --text-file) → info `OLD_DOC_VERIFY_AT_APPLY` + `verify_at_apply=true` +
  plan registry.corpus=null (quyết ở apply sau convert server-side — hố dry/apply lệch 21-07).
- **S5 — source-update-corpus NOT_FOUND tự refresh MỘT lần** trước khi kết luận (hố: gọi ngay sau
  apply dính cache cũ, phải --refresh tay).
- **S7 — reg-query positional = lọc mờ theo tên** (alias --name; trước rc=2 unrecognized).
- **S8 — nlm-add --row-kind** (`_nlm_link_row_kind` PURE): cờ tường minh thắng suy-topology F-06,
  kind bảo hộ giữ luật cũ khi không cờ — hết phải register --row-kind riêng sau nlm-add.
- **Vận hành trong phiên (data, journaled):** D1 xoá dòng own mồ côi profile «Luật BHXH» của Luật
  DN VBHN_67 (hai-scope-hai-ảnh đóng; dòng nền `67-2025-VBHN-VPQH` canonical khoẻ — căn cứ Đ122/88
  thông) · D4 đóng bằng đo: 382/BC-BTC là RIA định mức chi NSNN 2027-2030, KHÔNG phải RIA BHXH
  (giữ cat; RIA BHXH vào sổ chờ-nạp) · D3 sổ chờ-nạp 6 tài liệu · D2/D5/D6/D7 + tồn dư mới → phiên
  hygiene riêng · S6 xref deferred (cần đo tái hiện riêng) · S9 không làm (cookie phía Google).
- Golden regen CHỦ ĐÍCH: `parser_surface.json` (+3 bề mặt cờ mới: --as-ref · reg-query positional ·
  nlm-add --row-kind). SKILL.md: header + §184 cổng OCR máy-chặn + lối hạ ref → **re-import Capabilities**.

# ★ v1.35.9 — r179 BẢY FIX LOG PHIÊN VẬN HÀNH + ADR-0010 TỪ VỰNG NLM (2026-07-21)

> Thi công `BAN_GIAO_r179_2026-07-21.md` — 7 quyết định đã grill 21-07, mỗi cái đo trước phán sau.
> selftest **1151/1151** (+20 ca r179; 1131 cũ GIỮ NGUYÊN — added-fire 936/1118 là hành vi đúng).
> ADR-0010 mới: `docs/adr/0010-tu-vung-nlm-status-dong-va-tach-claim-due.md`.

- **T1 — `register --nlm-status` TỪ VỰNG ĐÓNG (ADR-0010 Q1):** `_nlm_status_write_ok` (classify.py)
  = họ `pushed*/synced*/active/removed_<lý do>` + rỗng (route clear); giá trị lạ (added/live/ready/
  typo) → `NLM_STATUS_UNKNOWN` **rc=2 TRƯỚC mọi round-trip** (test khoá: fake-gas 0 call). Cửa ĐỌC
  `_nlm_status_known` GIỮ NGUYÊN khoan dung (trash*/deleted/removed-trần) — bất đối xứng CÓ CHỦ ĐÍCH,
  selftest khoá cả hai chiều.
- **T2 — lệnh MỚI `backfill-nlm-status --dry/--apply`:** nắn MỘT LẦN added→pushed, live→active
  (map tất định, case-insens; map INLINE trong hàm — bẫy I11 hằng module-level không sống sót
  bind-REBASE, dính thật khi smoke). Per-row `reg_upsert` journaled + before → undo được; giá trị
  ngoài map KHÔNG đụng (stray `OUTSIDE_MAP`/`NO_DRIVE_ID`). Đo DRY trên «Luật BHXH»: **25 map
  (23 added + 2 live), 1 stray `ready`**. ⚠ CHẠY SAU DEPLOY (xem mục vận hành cuối).
- **T3 — guard `sua_doi` TỰ TRỎ chặn cứng:** `_sua_doi_self_ref` (PURE) — token trong sua_doi
  (tách `;`/`,`) sau `norm_sohieu` trùng số hiệu CHÍNH dòng (từ `--sohieu` cùng lệnh, fallback
  manifest theo drive_id) → `SUA_DOI_SELF_REFERENCE` rc=2, **KHÔNG có --force** (không tồn tại ca
  hợp lệ). Bắt biến thể `142/2025/QH15 ≡ 142-2025-QH15`. Xác minh bề mặt: cờ `--sua-doi` SINH ĐỘNG
  từ dest ở cli.py:437-439 (literal không có trong repo — log ghi đúng, grep sai chỗ).
- **T4 — draft theo BẬC BẰNG CHỨNG (mọi hệ) + vá title BOM/letterhead.** Đo 6 docx thật lô BNV
  16/7 trước khi sửa: sohieu classify nhiễm UUID tên file (`7_2026_e7c88c81`), issue_date nhiễm
  trích dẫn thân («Căn cứ NĐ… 2018») ⇒ veto official KHÔNG dùng được sohieu/issue_date thô.
  - Bậc: banner «DỰ THẢO» dòng riêng (`_draft_banner_line`, chịu artifact toạ độ docx
    `-44005514605Dự thảo…`) HOẶC Số-line KHUYẾT («Số:  /TTr-BNV», `_sohieu_line_khuyet`) ⇒ draft
    MẠNH; Số-line letterhead CÓ SỐ trong TEXT (`_sohieu_from_title_zone(strict_letterhead=True)` —
    KHÔNG best-fallback/filename) **AND** dateline đủ số (`_issue_dateline_complete`) ⇒ official
    PHỦ QUYẾT marker yếu («lấy ý kiến»/«góp ý»/«dự thảo» trong trích yếu); không bằng chứng ⇒ giữ
    hành vi cũ. Nghiệm thu: QĐ-TW ký + «lấy ý kiến» → draft:false (hết oan, ca log vận hành);
    6/6 file thật lô BNV GIỮ draft:true đúng (3 khuyết/banner + 3 weak-không-bằng-chứng).
  - Title (`_profile_title_from_header`): bỏ BOM đầu file (đường .txt/.html utf-8 — quốc hiệu hết
    thành title); bỏ dòng LETTERHEAD tên cơ quan (IN HOA ≤60, pattern agency BOUNDED — `bo\s+(?!luat)`
    né «BỘ LUẬT», không nhận `so|vu|ban` trần nên «SO SÁNH…»/«BAN HÀNH…» vẫn là title) + strip
    artifact toạ độ docx («598805267335BỘ NỘI VỤ»).
- **T5 — scope MỘT TỪ VỰNG ở 3 lệnh đọc (CONTEXT «Scope (dòng kết quả)»):** khoá `_scope` riêng
  của reg-query BỎ HẲN — dòng nền base-also mang `scope:'vbqppl'` + cờ `BASE_SCOPE_HIT` per-row
  Y HỆT source-map/exists ở CẢ reg-query (JSON rows + text `[nền]`) LẪN locate (text `[nền]` từng
  dòng + JSON). Selftest r6 cập nhật khoá `_scope` tuyệt chủng.
- **T6 — `vbhn-check --sohieu`:** alias MỎNG của positional (định tuyến y hệt: số hiệu → goc,
  trích yếu → subject; positional thắng nếu cả hai) — tay quen `--sohieu` hết usage-error.
- **T7 — `locate --json` JSON THẬT (`locate.v1`):** envelope cả 3 nhánh (offline_index /
  offline_manifest / webapp_find): `query/mode/count/shown/truncated/low_confidence/rows[]`
  (+`profile_hits/base_hits`, warnings token máy-đọc `OFFLINE_CACHE_*`); stdout sạch (narration
  tắt); row nền scope+BASE_SCOPE_HIT (T5). rc giữ nguyên ngữ nghĩa cũ.
- **T8 — tách nhãn claim/due (ADR-0010 Q2), sự cố «51/40/51» đóng bằng SỐ ĐO:** đo lại tươi trên
  «Luật BHXH»: vật lý 51 = claim 40 (24 own + 16 ref) + **11 dòng `removed_from_drive` nguồn CÒN
  SỐNG** (lô PDF dự thảo 16.6 — file Drive xoá, nguồn NLM giữ); reconcile desync_real=0; 10 dòng
  blank đều corpus=false (không thuộc diện). → Helper chung `_nlm_due_rows` (corpus∪ref − removed_*,
  blank-nb fold về base); **slot-audit**: khoá `gap` trần BỎ → `desync_estimate` (đếm) +
  `nlm_due_rows`/`coverage_gap`(+sample) + `removed_family_still_pointing` + `note_removed_live`
  khi giải thích TRỌN (hết lời khuyên backfill sai) + `labels_note`; **nlm-reconcile**: +`nlm_due_rows`/
  `coverage_gap` per-source (có live-set) + `removed_family_still_live`(+sample 11 file đúng tên) +
  `labels_note` (chỉ khi KHÔNG --from-plan — không có live ground-truth thì không phán). Hai lệnh
  nay kể CÙNG một câu chuyện với tên tường minh; «Hai phép đo ≠ nhau, lệch số KHÔNG phải mâu thuẫn».
- **Bề mặt/gate:** GENERATED_SPECS + COMMAND_META +`backfill-nlm-status` (medium/registry/dry-run,
  module nlm_ops); _STUB_MAP +7 tên (`_nlm_status_write_ok`/`_sua_doi_self_ref`/`_draft_banner_line`/
  `_sohieu_line_khuyet`/`_issue_dateline_complete`/`_nlm_due_rows`/`cmd_backfill_nlm_status`+
  `_backfill_nlm_status_candidates`); parser_surface regen CHỦ ĐÍCH (locate --json · vbhn-check
  --sohieu · lệnh mới). Selftest +20 ca `r179_t*` — kỷ luật đột biến r178: mỗi chốt có ca CHỈ nó
  chặn (vd `r179_t4_official_veto_requires_both_evidences` giết mutant nới strict→best-fallback;
  `r179_t1_register_gate_rc2_before_server` chứng minh gate đứng trước server bằng fake-gas 0 call).
- **Vận hành SAU deploy (một lần):** `tl --profile "Luật BHXH" backfill-nlm-status` DRY → `--apply`
  (25 dòng; stray `ready` trên VBHN_14 ATVSLĐ sửa tay sau khi hiểu nguồn gốc) — cờ
  `NLM_STATUS_MISMATCH` trên dòng added sẽ tự hết. Cân nhắc chạy thêm trên scope nền vbqppl.
- **CONTEXT.md** +5 mục từ vựng (Draft (ingest) · nlm_status · Scope (dòng kết quả) · nlm_claim ·
  nlm_due) — sản phẩm phiên grill 21-07, commit CÙNG release này.

# ★ v1.35.8 — r178 TIÊU CHÍ MÁY NHẬN DIỆN CÔNG VĂN HỆ ĐẢNG + ô mới `kinh_gui` (2026-07-21)

> Đóng việc-mở treo từ r175: biến thể `dang.cong_van` ĐÃ CÓ Ô từ lâu nhưng **chưa bao giờ kích
> hoạt được** — code chỉ bật cong_van cho `hanh_chinh` qua regex «V/v», mà HD05 không dùng «V/v».
> Đối soát nguyên văn HD05 27/5/2026 (GDoc `1Lko21mO…`). selftest **1131/1131** + gen_instructions 38/38.

- **Tiêu chí máy (2 vế, neo vào Ô):** ô `so_ky_hieu` khớp «Số N-CV/…» **∧** KHÔNG có ô `the_loai`.
  - Vế 1 — HD05 **3.1.2.b ví dụ 3**: *«Công văn của ban tuyên giáo và dân vận tỉnh uỷ — Số
    138-CV/BTGDVTU»*; bảng thống nhất viết tắt khi TRÙNG chữ cái đầu (**3.1.2.a**: QĐ, CT, CTr,
    TT, TTr) **không chứa CV** ⇒ không thể loại nào khác chiếm ký hiệu này. Khai **B2** (suy từ ví
    dụ + vắng mặt, không phải bảng liệt kê đóng) — cố ý KHÔNG khai B1.
  - Vế 2 — phản đảo **5.1.1** *«Văn bản ban hành đều ghi tên loại văn bản, **trừ công văn**»* ⇒
    CÓ tên loại ⇒ KHÔNG phải công văn (**B1**).
- **⚠ PHẢI neo vào Ô, KHÔNG dò head-blob như nhánh «V/v».** Đo 21-07 trên 190 docx thật: chuỗi
  «-CV/» khớp đúng **1 file — và là DƯƠNG TÍNH GIẢ**: `02_Bao-cao-tiep-thu-chi-dao.docx` là BÁO
  CÁO, chuỗi nằm ở **đoạn thân số 8** (*«Công văn số 3152-CV/VPTW, ngày 19/6/2026»*), **offset
  1040 < 3000** nên `_head[:3000]` CHẠM. Viết theo khuôn cũ là hỏng ngay trên dữ liệu đang có.
- **«Kính gửi» BỊ BÁC làm tiêu chí** (từng là ứng viên): khớp **35/190** file thật — báo cáo, tờ
  trình, phiếu trình. HD05 9.2.3 chỉ cho chiều *công văn ⇒ có Kính gửi*, KHÔNG cho chiều đảo.
- **Ô MỚI `dang.kinh_gui`** (trong bảng biến thể, chỉ sống khi cong_van bật) — HD05 **PL2 mục 5**:
  *«Từ "Kính gửi" đối với thể loại công văn … | In thường | **14** | **Nghiêng**»* + **9.2.3** (ô
  5a), **B1**. `canh`/`thut` = **"na"**: PL2 chỉ pin cỡ+kiểu, còn 9.2.3 *«ở chính giữa, trang đầu
  văn bản»* nhập nhằng giữa canh-giữa và vị-trí-giữa-trang ⇒ không kiểm (khuôn "na" r175).
- **Classifier hệ Đảng:** HD05 không có neo KÝ TỰ cho trích yếu công văn (PL2 nêu ví dụ *«về việc
  chuẩn bị hội nghị…»*, chữ thường) ⇒ neo VỊ TRÍ theo **5.2.3** *«trình bày cân đối dưới số và ký
  hiệu văn bản (ô số 5b)»* — đoạn chưa gán đầu tiên SAU `so_ky_hieu`, khai **B3** (user duyệt
  21-07). Nhánh tự phòng vệ 2 chốt (ô `so_ky_hieu` phải mang «-CV/»; ứng viên không in hoa) vì gán
  vô điều kiện sẽ **cướp đúng đoạn `the_loai`** của báo cáo (bước 3+4 chạy sau, `_set` không ghi đè).
- **⚠ Hồi quy tự bắt được và đã vá:** đặt nhánh `kinh_gui` ngoài cổng «-CV/» làm
  `01_To-trinh_Bo-Chinh-tri.docx` **rụng 1 `TT-DT-THAN-THUT`** (4170→4169) — ô `kinh_gui` không vào
  bảng khi biến thể tắt, nên đoạn bị nuốt thành **mất kiểm âm thầm**. Siết vào trong cổng ⇒
  **190/190 docx thật khớp r177 từng finding một** (183 file thật + 7 file khoá `~$` của Word;
  6 docx mới xuất hiện dưới `C:qh` sau mốc baseline đều hệ hành chính, không ca nào nhận nhầm).
- **Test r176 ca (f), f1-f10:** công văn Đảng chuẩn = 0 TT-DT · trích yếu 14 đứng →
  `TRICH-YEU-CV-{CO,KIEU}` · ô `kinh_gui` sai → `KINH-GUI-{CO,KIEU}` · ô đã `bo`
  (`the_loai`/`trich_yeu`) hết bị kiểm · **chiều nghịch**: BÁO CÁO (có tên loại + «Kính gửi:» +
  «-CV/» ở thân) không bị nhận nhầm và `the_loai` VẪN được kiểm · «Kính gửi» một mình không bật
  được biến thể · «-CV/» + CÓ tên loại không bật được biến thể (f7/f8) · không «-CV/» thì biến
  thể tắt (f9) · BÁO CÁO Đảng có «Kính gửi:» dài vẫn giữ `TT-DT-THAN-THUT` (f10).
- **⚠ Bộ đột biến 7 chốt — bắt được 3 CHỐT CHẾT mà selftest 1131/1131 vẫn xanh.** Vế «vắng
  the_loai», vế «-CV/» tầng check, cổng «-CV/» tầng classifier: gỡ từng cái ra, test vẫn XANH, vì
  mọi ca đều đã bị một chốt KHÁC chặn trước khi chạm tới. Thêm f7/f9/f10 mới đỏ đúng. Hai bẫy phụ
  lộ ra khi dựng ca: (i) dòng «Kính gửi» 23 ký tự rơi **dưới ngưỡng giỏ `than`** ⇒ ca rỗng nghĩa,
  phải kéo dài; (ii) `SK_PAT["dang"]` = `^\s*Số\s+\d+\s*-\s*[A-ZĐ]+/` **không khớp `TTr`** (chữ
  `r` thường) ⇒ `i_sk = None` ⇒ nhánh không chạy ⇒ ca đậu rỗng nghĩa, phải đổi sang «-BC/».
  **Trạng thái cuối:** 6/7 chốt SỐNG (có ca đỏ đúng). Vế «-CV/» ở **tầng check vẫn là CHỐT CHẾT**
  — cổng classifier đã chặn từ trước nên hạ nó xuống `True` không đổi finding nào. **Giữ lại như
  phòng vệ thừa CÓ CHỦ Ý và ghi thẳng vào code** (hai tầng cùng đọc một căn cứ 3.1.2.b), KHÔNG
  tuyên bố là đã được test khoá.
- **Sổ `_BAT_DUOC` giữ nguyên 53 ô** (KHÔNG bump): sổ r173 dựng `_tat_ca` từ bảng CHÍNH
  `_tt_dac_ta()`, còn `trich_yeu_cv`/`kinh_gui` thuộc bảng BIẾN THỂ — không đột biến được trên văn
  bản mẫu chung, nên khoá ở r176 (e)/(f) thay thế. Phạm vi này đã ghi vào comment sổ để khỏi tưởng thiếu.
- **Còn cách ly:** nhóm «văn bản/phụ lục ban hành kèm theo» (NQ351 Mẫu 6b/11b/14) — không đổi.

# ★ v1.35.7 — r177 PHÂN XỬ HAI CA CÁCH LY: trich_yeu·kieu GIỮ «đậm» (gỡ Đ5) · viết tắt Quy định = QĐ (2026-07-21)

> Đóng giỏ «chờ nguyên văn B1» treo từ r176, đúng trình tự «không đoán»: đối soát nguyên văn
> corpus NĐ30 PL I (GDoc `1YgArj3U…`) + HD05 27/5/2026 (GDoc `1Lko21mO…`). selftest **1131/1131**
> + gen_instructions 38/38.

- **Ca 1 — viết tắt "Quy định" hệ Đảng: `QĐ` THẮNG, `QĐi` bác.** HD05 mục 3.1.2.a nguyên văn:
  *«Trường hợp chữ cái đầu các âm tiết của tên loại văn bản trùng nhau thì thống nhất ký hiệu
  một số tên loại văn bản như sau: **Quyết định, Quy định: QĐ**; Chỉ thị: CT; Chương trình: CTr;
  Thông tri: TT; Tờ trình: TTr»*; ví dụ 3.1.2.b(ii): *«Quy định của Uỷ ban Kiểm tra Trung ương —
  Số 23-QĐ/UBKTTW»*. Chuỗi `QĐi` KHÔNG xuất hiện trong toàn văn HD05. `ABBR_DANG` + §5.3 vốn đã
  đúng — sửa phía SẢN PHẨM: `mau-dang-hd05/Mau_Dang_05_Quy_dinh.docx` `Số   -QĐi/ĐU` →
  `Số   -QĐ/ĐU` (readback sạch; quét cả 15 docx chỉ mẫu 05 dính) + bảng GHI_CHU.md kèm nguyên văn.
  ⚠ **ĐÍNH CHÍNH HỒ SƠ**: bảng viết tắt nằm ở HD05 **mục 3.1.2**, KHÔNG phải 3.2 như ghi chú r176
  (3.2 = kỹ thuật trình bày số-ký-hiệu) — cite cờ `TT-VIET-TAT` sửa `HD05 3.2` → `HD05 3.1.2`.
- **Ca 2 — `(hanh_chinh|dang)·trich_yeu·kieu` «đậm,nghiêng vs đậm»: «đậm» THẮNG, GỠ CÁCH LY Đ5.**
  NĐ30 PL I II.5.b nguyên văn: *«Trích yếu nội dung văn bản được đặt ngay dưới tên loại văn bản,
  trình bày bằng chữ in thường, cỡ chữ từ 13 đến 14, kiểu chữ **đứng, đậm**»*; HD05 PL2 mục 5:
  *«Trích yếu nội dung văn bản | In thường | 14-15 | **Đứng, đậm**»* (công văn: 12 nghiêng — khớp
  biến thể TT-5 sẵn có). Bảng đặc tả («dam», B1) vốn đúng ⇒ «đậm,nghiêng» đo được trong thực chiến
  là LỆCH CHUẨN THẬT, không oan. Gỡ khối `_bo_kiem` Đ5 trong `_the_thuc_check_dac_ta`; mức vẫn
  **INFO** (trich_yeu thuộc nhóm tin-cậy-thấp Đ1 — không FAIL, chưa thăng, không cần duyệt zero-oan).
- **Test:** r176 (d) LẬT CHIỀU — trich_yeu đậm+nghiêng nay PHẢI ra `TT-DT-TRICH-YEU-KIEU` mức INFO;
  sổ r173 `_BAT_DUOC` **51→53 ô** (thêm `(hanh_chinh|dang).trich_yeu`), gap ledger 8→6 (hồ sơ
  comment cập nhật). Docstring Đ1-Đ5 + baseline ghi lại theo trạng thái r177.
- **Nghiệm thu:** tầng 1 đo lại @r177 trên 34 file sản phẩm còn trên đĩa (15 docx Đảng + 19 NQ351):
  **0 TT-DT tuyệt đối**; `_TEST_dien_that` giữ **0/0/0**; mẫu trống giữ đúng 2 FAIL số-KH/địa-danh;
  mẫu 05 sau sửa không phát sinh finding mới. Corpus đo-lũ 129 file KHÔNG đo lại được (bản tạm đã
  xoá, `t2_corpus.json` chỉ lưu tên+findings) — theo bảng nghiệm thu r176 (`tong_hop_sau_va.md`
  dòng `trich_yeu·kieu 7/7`), lớp A số học 856 → **863** (+7 INFO, toàn bộ là ca đậm+nghiêng thật).
- **Reference đồng bộ:** §6.34 (Đ5 → phân xử xong kèm nguyên văn; sổ 53 ô; test d lật) · §5.3 hàng
  số-ký-hiệu đóng dấu «không có `QĐi`». ADR-0009 thêm mục «Hậu kiểm 2026-07-21 (r177)». Comment
  `ABBR_DANG` ghi căn cứ 3.1.2.a.
- **Việc mở KHÔNG đổi:** cong_van hệ Đảng chưa có tiêu chí máy · nhóm «kèm theo» (Mẫu 6b/11b/14)
  VẪN cách ly (chưa đối soát đủ căn cứ từng ô) · builder trục kiểu/canh/thụt còn inline · thăng
  FAIL từng ô = vòng sau.

# ★ v1.35.6 — r176 ADR-0009 BƯỚC 5 «NỐI BỘ KIỂM»: lớp đặc tả TT-DT đọc bảng vào production (2026-07-21)

> Hoàn tất trình tự 5 bước ADR-0009. `the-thuc-check` nay có LỚP ĐẶC TẢ đọc bảng `_tt_dac_ta()`
> (+ biến thể r175): finding `TT-DT-<Ô>-<CO|KIEU|CANH|THUT>` theo đúng gói Đ1-Đ5 user duyệt 21-07.
> selftest **1131/1131** (+1: r176) + gen_instructions 38/38.

- **Parser mở rộng** (`_the_thuc_parse_docx`): kênh `p["dt"]` per-đoạn — cỡ (mode), tỉ lệ
  đậm/nghiêng/gạch, `dam_dau` (run đầu — văn phạm `:tien_to`), jc/firstLine/left KẾ THỪA STYLE
  đủ tầng run → pPr/rPr → pStyle → Normal → docDefaults (1 cấp basedOn; thiếu tầng style từng đẻ
  701 finding oan ở đo lũ). Khoá cũ ind/jc/dam/szs GIỮ NGUYÊN ngữ nghĩa — cờ tay r143-r171 không đổi.
- **Classifier `_tt_dt_phan_loai`** port NGUYÊN TRẠNG từ bộ kiểm nháp đo-lũ (6 bẫy oan đã vá giữ
  đủ) + **vá oan mới lộ khi quét sổ**: neo `thong_qua` siết theo công thức Đ36 k1 «<loại> này được
  Quốc hội … thông qua» — thân Lệnh công bố («Luật X đã được Quốc hội thông qua») hết bị gán nhầm.
- **Lớp kiểm `_the_thuc_check_dac_ta`** nối sau T3: Đ1 B1/B2→WARN · B3→INFO · ô tin-cậy-thấp
  (than/ten_cq/ten_cq_tren/trich_yeu/tieu_de_pc/ho_ten_ky)→INFO, KHÔNG BAO GIỜ FAIL; Đ3 chỉ chạy
  khi nhận diện được khối đầu (quoc_hieu/tieu_de), nhóm «kèm theo»/phụ lục bỏ; Đ4 nhường cờ tay
  (TT-BAC-CO-CHU↔(quoc_hieu|tieu_ngu|tieu_de)·co mọi hệ · TT-CHUC-VU-DAM↔dang chuc_vu_ky·kieu ·
  TT-CHUONG-CANH-GIUA↔dang (phan_chuong|muc)·canh — một hiện tượng một finding); Đ5 cách ly
  (hanh_chinh|dang)·trich_yeu·kieu chờ nguyên văn NĐ30 PL I II.5. Biến thể resolve trước khi so:
  «/QĐ-CTN»→qd_ctn · «V/v» đầu dòng→cong_van hanh_chinh (cong_van hệ Đảng CHƯA có tiêu chí máy —
  để sau, không đoán).
- **Sổ `_BAT_DUOC` r173: 1 ô → 51 ô** (test tự cưỡng chế đúng thiết kế — nối xong là sổ buộc phải
  mở). 8 gap còn lại có hồ sơ trong comment r173: 2 Đ5 cách ly · 3 neo-bằng-chính-thuộc-tính-lật
  (de_muc_than ×2, co_quan_ban_hanh) · 2 đoạn văn bản test <25 ký tự · 1 biên quét 2n/3 văn bản ngắn.
- **r176 MỚI** khoá 6 hành vi: (a) tầng-1 builder 3 hệ + Lệnh/QĐ-CTN = 0 TT-DT; (b) Đ3 mất khối
  đầu → lớp im hẳn kể cả khi có lỗi thật; (c) Đ4 chuc_vu_ky Đảng đậm → chỉ TT-CHUC-VU-DAM;
  (d) Đ5 trich_yeu đậm+nghiêng → im; (e) công văn V/v chuẩn 12-13 đứng → 0, V/v 14 nghiêng →
  TT-DT-TRICH-YEU-CV-CO+KIEU, ô đã `bo` không kiểm; (f) `dam:tien_to` «Điều 3.» đậm + nội dung
  Đứng → không TT-DT-DIEU-KIEU, không giẫm TT-KHOAN-DAM.
- **NGHIỆM THU trên corpus đo-lũ** (129 file, baseline `t2_corpus.json` @v1.35.5): tầng 1 —
  19 mẫu NQ351 + 15 mẫu HD05 + builder qua PRODUCTION = **0 TT-DT tuyệt đối**; lớp A 876 → **856**,
  diff per-ô ĐÚNG 5 dòng giải trình 100% theo quyết định đã duyệt (−9 Đ4 nhường TT-BAC-CO-CHU:
  tieu_de 7 + quoc_hieu 1 + tieu_ngu 1 · −4 Đ4 nhường TT-CHUC-VU-DAM · −7 Đ5 cách ly trich_yeu);
  lớp B phụ lục 3.905 → **0** (Đ3); lớp C 46 → 42 (−4 cùng lý do Đ4/Đ5). Chống-trùng kiểm tay
  2 file đại diện: mỗi hiện tượng đúng 1 finding cờ tay, 0 TT-DT trùng.
- tl.py: +2 tên `_STUB_MAP["the_thuc"]` (`_tt_dt_phan_loai`, `_the_thuc_check_dac_ta`).

# ★ v1.35.5 — r175 ADR-0009 BƯỚC 4 ĐO LŨ xong + vòng-2 BƯỚC 1 vá bảng theo 5 quyết định Đ1-Đ5 (2026-07-21)

> BƯỚC 4 "đo lũ" chạy NGOÀI repo (bộ kiểm nháp đọc bảng, `D:\Quốc hội\do-lu-2026-07-21`), user duyệt
> cả gói Đ1-Đ5, rồi quay bước 1 vá bảng ngay trong release này. selftest **1130/1130** (+1: r175) + 38/38.

- **Số liệu bước 4** (skill v1.35.4): tầng 1 — builder tự dựng 0 finding; 33 mẫu chuẩn 15 finding,
  đối chiếu tay **100% là khiếm khuyết của BẢNG, không phải lỗi mẫu**. Tầng 2 — 129 file thật
  (khớp 105/111 dòng nền 19-07): lớp A 49 VB hoàn chỉnh **1.214 finding**, hai VB nền "đạt chuẩn
  hoàn toàn" ăn 85/57 ⇒ **Đ1: chưa ô nào thăng FAIL** (zero-oan chưa ai đạt). Phiên đo tự bắt
  6 nguồn cảnh báo oan của chính bản nháp (7.779 → 5.842) — "đo trước, phán sau" trả lãi.
- **5 quyết định Đ1-Đ5** (ADR-0009, user duyệt 21-07): Đ1 không thăng FAIL; Đ2 vá bảng trước khi
  nối; Đ3 chỉ áp lớp đặc tả cho file có khối đầu; Đ4 chống báo trùng cờ tay; Đ5 cách ly
  `trich_yeu·kieu` chờ nguyên văn NĐ30 PL I II.5.
- **Bảng 54 → 59 ô** (thi hành Đ2): vbqppl_qh +3 ô B1 đo từ sơ đồ mẫu (`cau_ban_hanh` «Quốc hội
  ban hành Luật … .» 14 nghiêng; `co_quan_ban_hanh` dòng chủ thể «CHỦ TỊCH / NƯỚC CHXHCNVN» 14 đậm
  giữa — tầng 1 lộ: 3 finding chuc_vu_ky 14pt là bản nháp GÁN NHẦM dòng này, chữ ký thật 13pt khớp
  bảng; `tu_lenh` «QUYẾT NGHỊ:»/«NAY …:» 14 đậm giữa); ô `can_cu` QH mở nghĩa gồm «Xét/Theo đề
  nghị»; `de_muc_than` hanh_chinh (B3→INFO vĩnh viễn) + dang (B2* — reference TT-6 «đề mục: đậm»).
- **Văn phạm ô mới**: kiểu `dam:tien_to` (ô `dieu` cả 3 hệ — đậm áp TIỀN TỐ «Điều N.»+tên, nội dung
  inline Đứng, khớp `dam_dau` r171); giá trị `na` cho canh/thụt = luật không ấn định + thực tiễn đa
  dạng ⇒ KHÔNG kiểm (đề mục tự do: kho mẫu HD05 canh giữa, corpus dàn đều thụt 1cm — hai kiểu cùng sống).
- **`_tt_dac_ta_bien_the()` MỚI** — trục thứ ba BIẾN THỂ THEO MẪU: override Mẫu 16 QĐ-CTN (quốc hiệu
  13, B1 sơ đồ); biến thể công văn hanh_chinh (ô 5b NĐ30: trích yếu «V/v» 12-13 đứng, B2*) và dang
  (TT-5: 12 nghiêng, B2*) kèm `bo` tên loại/trích yếu; nhóm «kèm theo» (6b/11b/14) VẪN CÁCH LY.
- **Test**: r170 mở rộng 59/59 ô (+spec Lệnh CTN thứ 5; parse `:tien_to`; skip `na`) · r173 đột biến
  phủ 59/59 (spec Lệnh CTN + câu ban hành + đề mục; sổ `_BAT_DUOC` KHÔNG đổi — đúng: bộ kiểm chưa
  nối) · **r175 MỚI** khoá cấu trúc bảng biến thể (override phải KHÁC gốc + đủ căn cứ/bậc; ô `them`
  tuple-6 không trùng bảng chính; `bo` trỏ ô có thật).
- **Builder BYTE-IDENTICAL** — không ô mới nào chảy vào `_tt_co_build`/`_CHON`; bundle ×2 cùng SHA.
- **Đo lại sau vá** (bộ kiểm nháp): tầng 1 **0/0/0 TUYỆT ĐỐI** (builder · 19 mẫu NQ351 · 15 mẫu
  HD05 — đạt chuẩn ADR "mẫu chuẩn 0 finding lệch bảng"); lũ lớp A 1.214 → **876**.
- Hồ sơ: `docs/adr/0009` cập nhật bước 4 + Đ1-Đ5 + nội dung r175 · reference §6.34 (59 ô, `:tien_to`,
  `na`, biến thể) · CONTEXT.md +«Biến thể mẫu», +«na».
- Còn lại bước 5 (nối bộ kiểm theo Đ3/Đ4/Đ5, cập nhật sổ `_BAT_DUOC` từng ô) — phiên sau.

# ★ v1.35.4 — r174 ADR-0009 BƯỚC 3a: cỡ chữ builder DẪN XUẤT từ bảng đặc tả — byte-identical (2026-07-21)

> BƯỚC 3 (phần a — cỡ chữ, thứ dễ trôi nhất vì là con số). selftest **1129/1129** + 38/38 giữ nguyên.

- **`_tt_co_build(he)` MỚI**: dict `S` của `the_thuc_build` không còn hard-code — dẫn xuất từ
  `_tt_dac_ta()`: ô đơn trị dùng thẳng; ô khai DẢI tra `_CHON` (lựa chọn nội bộ **bậc B3** trong dải
  luật, đặt CẠNH bảng, lệch dải là ValueError ngay lúc build — thà nổ sớm còn hơn lặng lẽ hard-code
  trở lại). Từ nay **sửa cỡ trong bảng là builder đổi theo** — đúng nghĩa nguồn sự thật cho trục cỡ chữ.
- **Bằng chứng an toàn**: đối chiếu tay 33 giá trị × 3 hệ khớp 100% S cũ; build lại 4 văn bản chuẩn
  (dang · Luật QH · NQ UBTVQH · hành chính) **BYTE-MATCH sha256 `word/document.xml`** trước/sau.
  Đăng ký `_tt_co_build` vào bảng re-export `tl.py` (bẫy #6).
- **Phạm vi trung thực**: kiểu/canh/thụt trong builder VẪN inline tại từng chỗ render — nhưng bị
  r170 (54/54 ô) + r173 (đột biến) khoá từ ngoài: builder lệch bảng là đỏ ngay. Nối nốt trục
  kiểu/canh vào lúc nối bộ kiểm (bước 5) nếu thực tế cho thấy cần — ghi chú trong ADR-0009.

# ★ v1.35.3 — r173 ADR-0009 BƯỚC 2: khoá test 100% (54/54 ô) + selftest đột biến sổ-hai-chiều (2026-07-21)

> BƯỚC 2/5 của ADR-0009. selftest 1128→**1129** (thêm r173), gate GIỮ 9 bước — đột biến là NỘI DUNG
> của bước selftest, không phải bước gate mới (Q7 user chốt).

- **r170 chiều thuận 28→54/54 ô**: thêm văn bản dựng thứ 3 (NQ UBTVQH — phủ `dia_danh/muc/quyen_han_ky/
  noi_nhan_*` hệ QH mà mẫu Luật không có) + thứ 4 (**hành chính 18/18 ô — trước đây hệ này 0 test**);
  dang bổ `muc` + `noi_nhan_tu`; qh-Luật bổ `thong_qua`. **KHOÁ ĐỦ-PHỦ tự cưỡng chế**: r170 đối chiếu
  tập (hệ, ô) đã test với toàn bảng — thêm ô vào bảng mà quên viết test là ĐỎ ngay, độ phủ không thể
  trôi ngầm lần nữa (bài học 28/48=58% âm thầm của r170 cũ).
- **r173 chiều nghịch — đột biến LẬT ĐẬM từng ô (54 đột biến) + SỔ HAI CHIỀU**: `_BAT_DUOC` ghi ô bộ
  kiểm HÔM NAY bắt được (duy nhất `dang.chuc_vu_ky` → TT-CHUC-VU-DAM, cờ viết tay — khớp thực nghiệm
  1/5 ngày 20-07); tụt lùi = đỏ · ô gap bật cờ mới (bước 5 nối dần) = đỏ buộc ghi sổ. Máy-canh-cho-
  máy-canh: bằng chứng sống rằng dây nối bảng→bộ kiểm hoạt động, sống sót qua refactor.
- **Bẫy mới ghi nhận**: `the_thuc_check()` gọi thẳng cấp module KHÔNG normalize `-`→`_` của tham số
  `he` (chỉ CLI normalize) — `he="vbqppl-qh"` nổ KeyError câm trong test. r173 dùng dạng gạch dưới.
- **Vá lệch version 3 nơi**: v1.35.2 commit trước bump file `VERSION` nhưng SÓT hằng `tl.py:94` và
  header SKILL.md ⇒ r65 (guard ADR-0001 `version_forked == VERSION`) đỏ đúng chức năng. v1.35.3 đồng
  bộ cả ba. Bài học: bump version = **3 chỗ** (VERSION · tl.py · SKILL.md header).
- Kernel chỉ đổi header ⇒ re-import Capabilities KHÔNG bắt buộc.

# ★ v1.35.2 — r172 ADR-0009 BƯỚC 1: vá bảng đặc tả (+bậc thẩm quyền) · normalize idempotent với build (2026-07-21)

> Grilling 20→21-07 chốt ADR-0009 (8 quyết định, user duyệt từng cái): `_tt_dac_ta()` sẽ thành nguồn
> sự thật DUY NHẤT (nối 5 bước); thang thẩm quyền B1>B2>B3; severity buộc vào bậc (B3→INFO vĩnh viễn);
> chuẩn thăng FAIL zero-oan; selftest đột biến hai chiều (gate GIỮ 9 bước). Đây là BƯỚC 1.
> Cứ liệu mở màn: đo 5 đột biến vi phạm bảng → bộ kiểm bắt 1/5; bảng không được hàm nào đọc (kể cả
> builder — chỉ selftest); file "0 finding" theo GHI_CHU thực chất 2 WARN thật. selftest **1128/1128** giữ.

- **`_tt_dac_ta()` 48→54 ô, tuple 5→6 trường (+`bac`)**: mỗi ô tự khai bậc thẩm quyền B1/B2/B3
  (hậu tố `*` = giá trị đơn chọn trong dải luật). `hanh_chinh` 13→18 ô: TÁCH `ten_cq_tren` (chủ quản
  KHÔNG đậm — hết mâu thuẫn §6.16) + 4 ô bố cục `phan_chuong/tieu_de_pc/muc/dieu` (NĐ30 PL I II.6);
  `vbqppl_qh` 18→19: bổ khuyết `quyen_han_ky` (Đ37 k1, Mẫu 10-13); 5 ô dẫn chiếu mơ hồ "PL I sơ đồ"
  → đích danh **Đ30/Đ31/Đ33**. Hai hệ `vbqppl`/`vbhn` **khai trắng tường minh** `__khai_trang__`
  (ADR-0009: cấm giả vờ kiểm). r170 unpack `[:5]`.
- **M5 CHẾT — normalize idempotent với build**: `_fix_sect` lề phải THEO HỆ (`he_eff`): nhà nước
  **1134=20mm** (= builder; NĐ30 dải 15-20, chọn 20 là B3 — Q4 user chốt), Đảng giữ **850=15mm** HD05
  đơn trị. Trước đây normalize ép 850 toàn cục ⇒ âm thầm đổi lề mọi file nhà nước đã build. Đã chứng
  minh: build→normalize giữ nguyên 4 lề (hành chính) · Đảng vẫn 850. `criteria["normalize"]` tách
  `le_nha_nuoc`/`le_dang` — NEO dòng 415 + r135 anchor + r138 fixture sửa cùng release (đúng quy trình
  drift-lock). **Lưu ý vận hành:** file NHÀ NƯỚC normalize từ nguồn lề 15mm nay ra 20mm (khác bản .35.1).
- **Comment nhánh WARN dải-hợp sửa đúng sự thật**: nhánh `rng is None` KHÔNG chết — chỉ còn `vbhn`
  chạm (ke_thua chưa materialize, không khai khoá lề); nhãn cũ "vbqppl_qh" sai từ v1.34.76.
- **Reference đồng bộ**: §6.34 viết lại (54 ô = 18+19+17, 22 khoá — hết cách đọc nhầm "48 × 3 hệ");
  §6.25 đệm ô 6pt→**4pt** theo r164 (nhãn B3); §6.17 làm rõ "Mẫu 1-16 = 19 sơ đồ" (mẫu 6/11/15 tách
  a/b) — hết vênh 16-vs-19; §8 normalize mô tả lề theo hệ.
- **Hồ sơ**: `docs/adr/0009` (8 quyết định + trình tự 5 bước + zero-oan) · `CONTEXT.md` cụm "Thể thức"
  (Đặc tả thể thức · Bậc thẩm quyền · Cách ly). **CÁCH LY chờ B1**: viết tắt `QĐi` (Mẫu Đảng 05) vs
  `QĐ` (`ABBR_DANG` + §5.3) — cần nguyên văn HD05 mục 3.2 mới phân xử, KHÔNG đoán.
- Ngoài repo: `mau-dang-hd05/_TEST_dien_that` điền lại đúng (0/0/0 thật @v1.35.1, dấu `;`, hết tổ chức
  KL121, một kiểu dấu) · GHI_CHU đóng dấu kiểm chạy-lại-được + sử liệu vụ trôi.

# ★ v1.35.1 — khoản/điểm không in đậm · công thức ban hành VB Đảng (§6.35-6.36) (2026-07-20)

> User rà mẫu Quyết định: *"đoạn BAN THƯỜNG VỤ QUYẾT ĐỊNH có căn giữa không · nội dung Điều 3 tại
> sao phải in đậm · kiểm tra tương tự với các mẫu khác"*. selftest 1127→**1128**.

- **§6.35 KHOẢN/ĐIỂM KHÔNG IN ĐẬM.** HD05 PL2 mục 6 tách ba dòng: *"Từ 'Điều', số thứ tự và tên
  điều"* = đậm · *"Khoản"* = Đứng · *"Điểm"* = Đứng. Minh hoạ ở cấp RUN xác nhận
  `1. Quy định về…`[đậm=0]. Điều KHÔNG có tên (6.2.4.c cho phép *"tên điều hoặc nội dung của
  điều"*) ⇒ chỉ tiền tố `Điều N.` đậm, nội dung in thường — HAI RUN trong cùng đoạn
  (`spec.body[].dam_dau`). Cờ mới **`TT-KHOAN-DAM`**; thêm `spec.body[].nghieng`.
  ★Bẫy: hàm phân loại đề mục dùng `t.upper() == t`, mà `"1- …"`/`"…"` không có chữ cái nào nên cũng
  thoả ⇒ **34 đoạn nội dung khoản bị in đậm** khắp bộ mẫu Đảng. Điều kiện đúng: in hoa **và ≥2 chữ cái**.
- **§6.36 CÔNG THỨC BAN HÀNH VB ĐẢNG LÀ CÂU THƯỜNG.** HD05 không quy định; cứ liệu là chính
  QĐ 399-QĐ/TW: *"Ban Bí thư quy định về … như sau:"* — in thường, không in hoa/đậm/canh giữa.
  NGƯỢC với VBQPPL (`QUYẾT NGHỊ:` in hoa đậm canh giữa). Mẫu Quyết định sửa
  `BAN THƯỜNG VỤ QUYẾT ĐỊNH` → `Ban Thường vụ quyết định:`.
- *"Kính trình"* chuyển sang **nghiêng** (HD05 PL2 mục 9), trước bị in đậm.
- **ĐÍNH CHÍNH CĂN CỨ**: quy tắc bố cục Phần/Chương/Mục/Điều của HD05 là **mục 6.2.4**, không phải
  6.2.3 (6.2.3 = phần căn cứ ban hành). Sửa trong reference §6.33 và bảng `_tt_dac_ta()`.

# ★★ v1.35.0 — TẤT ĐỊNH HOÁ quy tắc thể thức 3 hệ (§6.34) + thụt Điều NQ351 (2026-07-20)

> User: *"kiểm lại mẫu NQ351 có lỗi Chương/Điều tương tự không"* + *"nghiên cứu cách tất định hoá
> các quy tắc thể thức của Đảng, Quốc hội và hành chính"*. selftest 1126→**1127**.

**Kết quả rà 19 mẫu NQ351**: KHÔNG có lỗi như mẫu Quy chế Đảng — Phần/Chương/Mục đã `center` không
thụt, Điều đã có dấu chấm sau số. Nhưng lộ **một khác biệt tinh vi giữa hai hệ** đang bị làm giống
nhau: NQ351 Đ35 k2 c ghi Điều **"cách lề trái 1cm đến 1,27cm"** (thụt TRÁI cả khối) trong khi HD05
6.2.2 ghi **"khi xuống dòng thì chữ đầu dòng lùi vào"** (thụt DÒNG ĐẦU). Một dòng thì nhìn giống
nhau, chỉ lộ khi tiêu đề điều xuống dòng. Đã tách: `kieu="dieu"` ở hệ `vbqppl_qh` dùng `w:ind
w:left`, hệ `dang` giữ `w:firstLine`. `_tt_p` nhận thêm tham số `left`.

**TẤT ĐỊNH HOÁ — `_tt_dac_ta()`**: bảng đặc tả `(cỡ, kiểu, canh, thụt, căn_cứ)` cho **48 thành phần
× 3 hệ**. Bổ khuyết cho `_the_thuc_criteria()` vốn chỉ khoá ngưỡng SỐ, trong khi mọi lỗi thực chiến
đều ở kiểu chữ / canh lề / loại thụt. **`r170` đối soát HAI CHIỀU**: dựng văn bản thật cho từng hệ
rồi kiểm từng thành phần khớp bảng ⇒ builder và bảng không thể trôi khỏi nhau.

Bảng làm hiện rõ **ba chỗ ba hệ thực sự khác nhau — đúng ba lỗi đã mắc trong phiên**:
`chuc_vu_ky` (Đảng in thường, hai hệ kia đậm) · `noi_nhan_tu` (Đảng gạch chân, hai hệ kia đậm+
nghiêng) · `dieu` (QH thụt trái, Đảng thụt dòng đầu).

★Bẫy lặp lại: hàm module-level mới (`_tt_dac_ta`) phải đăng ký bảng re-export trong `tl.py`, nếu
không `_TL_MODULE._tt_dac_ta` không resolve và test đỏ **không kèm chẩn đoán**. ★Bẫy regex: đổi thẻ
`<w:ind>` thêm `w:left` làm `r'<w:ind w:firstLine="…"'` hết khớp — đừng neo vào thứ tự thuộc tính.

# ★ v1.34.99 — Chương/Mục canh giữa, Điều có dấu chấm (§6.33) (2026-07-20)

> User rà mẫu Quy chế Đảng: *"Chương, Điều được alignment trung tâm hay phải trái, font, size, in
> đậm đã chính xác chưa"*. Cỡ chữ/đậm đều đúng; **canh lề và dấu sau số Điều thì SAI**.

- **HD05 mục 6.2.3.a-b**: từ "Phần"/"Chương"/"Mục" + số thứ tự trình bày **CHÍNH GIỮA hai lề**, tên
  phần/chương/mục ở dòng liền kề dưới. Builder để `Chương I` **dàn đều + thụt 1cm** ⇒ sai.
  `kieu="giua"` trước chỉ dùng được cho hệ `vbqppl_qh`, nay **mở cho MỌI hệ**.
- **HD05 mục 6.2.3.c**: sau số thứ tự của điều có **DẤU CHẤM** (`Điều 1.`), mẫu đang dùng dấu hai
  chấm (`Điều 1:`). Ví dụ PL2 xác nhận: `Điều 1. Phạm vi điều chỉnh và đối tượng áp dụng`.
- **Điều KHÔNG canh giữa** — theo 6.2.2: dàn đều hai lề + thụt đầu dòng 10mm (giữ nguyên, đã đúng).
- Tiêu chí mới **`TT-CHUONG-CANH-GIUA`** (WARN); parser thêm cờ `jc` cấp đoạn.
- Đối chiếu phần còn lại của mẫu Quy chế đều ĐÚNG: ĐCSVN 15 đậm · tên CQ 14 (cấp trên không đậm,
  CQ ban hành đậm) · số-KH 14 · địa danh 14 nghiêng · thể loại 16 đậm · trích yếu 15 đậm ·
  Điều 15 đậm · giãn dòng 20pt Exactly · Nơi nhận 14 gạch chân + liệt kê 12 · T/M đậm, chức vụ
  không đậm, họ tên đậm.

# ★ v1.34.98 — khối tiêu đề mặc định chia đôi (§6.32) (2026-07-20)

> User: *"chưa thấy các mẫu Đảng xử lý vấn đề lệch phải của cột Tiêu ngữ"* — đúng, .97 mới sửa ngắt
> dòng chứ chưa đụng độ rộng cột.

- **Đo hình học THẬT của chính file HD 05-HD/VPTW**: `tblGrid` khối tiêu đề = **4612 | 4675** trên
  vùng chữ 9071 ⇒ ~**50/50**, tâm khối phải **74,8%**. Builder chỉ cấp cho ô phải đúng bề rộng tiêu
  đề cần (hệ Đảng 4256 = **45,5%**) ⇒ ô phải hẹp, bị đẩy sang phải, tâm **77,2%**.
- Quy tắc mới: `wr = min(max(need_r, 50%×W), 62%×W)` — **mặc định chia đôi**, chỉ nới ô phải khi
  Quốc hiệu/tiêu đề không đủ chỗ một dòng (§6.6). Kết quả hệ Đảng: `4677 | 4678`, tâm trái **25,0%**
  / tâm phải **75,0%** — khớp HD05 (24,8% / 74,8%).
- **Hệ nhà nước KHÔNG đổi** (Quốc hiệu 34 ký tự cần 58%) — r145 chốt cả hai chiều: hệ Đảng phải chia
  đôi (`|wl−wr| ≤ 2`, tâm phải 74-76%), hệ nhà nước ô phải vẫn rộng hơn ô trái. Xác minh ĐỎ-TRƯỚC.
- ★Bài học ghi vào reference: user kêu "lệch" thì **mở file nguồn chính thức ra đo `tblGrid` thật**,
  đừng suy từ nguyên tắc canh giữa. Tôi đã đo tỷ lệ khối rồi kết luận "đúng chuẩn" (sai), sửa ngắt
  dòng (đúng nhưng chưa đủ), rồi mới đo hình học HD05 mới thấy chênh 45,5% vs 51,5%.

# ★ v1.34.97 — cân dòng không cắt đôi cụm cố định (§6.27) (2026-07-20)

> User gửi ảnh đối chiếu: bản HD05 gốc vs bản dựng. Tỷ lệ khối trái/phải của bản dựng đã gần đúng
> (tâm khối trái 32% vs 33%, khối phải 77% vs 74%) — thứ làm nó TRÔNG lệch và chật là ĐIỂM NGẮT DÒNG.

- `_tt_can_dong` chia cân thuần theo độ dài cho ra `ĐẢNG ỦY ỦY BAN VĂN` | `HÓA VÀ XÃ HỘI` —
  **tách đôi "VĂN HÓA"**. Quy tắc mới, theo thứ tự ưu tiên:
  1. **cấm** điểm cắt phá cụm cố định (`NHÀ NƯỚC`, `VĂN HÓA`, `XÃ HỘI`, `TRUNG ƯƠNG`, `LAO ĐỘNG`,
     `THƯỜNG VỤ`, `CHẤP HÀNH`, `TỔ QUỐC`… — 50 cụm hay gặp trong tên cơ quan);
  2. **ưu tiên** cắt ngay sau từ chỉ loại hình tổ chức (`BAN`, `ỦY`, `VỤ`, `CỤC`, `SỞ`, `PHÒNG`,
     `VIỆN`, `KHỐI`, `BỘ`…) — tức cắt TRƯỚC phần tên lĩnh vực;
  3. rồi mới cân độ dài.
  Kết quả: `ĐẢNG ỦY ỦY BAN` | `VĂN HÓA VÀ XÃ HỘI` · `ỦY BAN QUẢN LÝ VỐN` | `NHÀ NƯỚC TẠI DOANH NGHIỆP`
  · `ĐẢNG BỘ KHỐI` | `CÁC CƠ QUAN TRUNG ƯƠNG`.
- Áp cho cả nhánh tối ưu (2 dòng) lẫn nhánh greedy (≥3 dòng). r145 chốt: cụm cố định không được
  nằm vắt qua hai dòng. Xác minh ĐỎ-TRƯỚC.

# ★ v1.34.96 — gạch chân "Nơi nhận" không trùm dấu hai chấm (§6.31) (2026-07-20)

> User yêu cầu kiểm KỸ LẠI thể thức nơi nhận và phần ký sau khi vá .94.

- **Xác minh lại phần ký bằng cột "Minh hoạ" của HD05 PL2** — mỗi ô minh hoạ được render ĐÚNG kiểu
  chữ mà dòng đó quy định, soi ở cấp RUN: `T/M BAN THƯỜNG VỤ`[đậm=1] · `PHÓ BÍ THƯ`[đậm=**0**] ·
  `Nguyễn Văn A`[đậm=1]. ⇒ **bản vá .94 ĐÚNG** (chức vụ người ký VB Đảng không in đậm), nay có
  bằng chứng định dạng chứ không chỉ mô tả chữ.
- **§6.31 lỗi mới lộ ra từ chính minh hoạ đó**: `Nơi nhận`[gạch chân] + `:`[KHÔNG gạch chân] là hai
  run tách nhau — builder đang gạch chân cả `Nơi nhận:`. Đã tách run.
- Ghi vào reference cách đọc PL2: **cột Minh hoạ = bằng chứng định dạng**; ⚠ KHÔNG dùng các bảng
  minh hoạ khổ nhỏ ở đầu HD05 (toàn 10pt, không đậm gì) làm chuẩn — chúng là HÌNH thu nhỏ.
- Nơi nhận VB Đảng vẫn dùng **dấu chấm phẩy `;`** — HD05 mục 9.2.5 nguyên văn và ví dụ minh hoạ
  trong chính HD05 đều `;`; đã trình nguyên văn cho user, chờ xác nhận nếu Uỷ ban có quy ước riêng.

# ★ v1.34.95 — cân dòng, keepNext, tổ chức hết hiệu lực, nhất quán dấu (§6.27-6.30) (2026-07-20)

> Bốn góp ý của user sau khi xem bộ mẫu Đảng, cộng một chỉnh cho Phiếu trình. selftest 1125/1125.

- **§6.29 TỔ CHỨC ĐÃ KẾT THÚC HOẠT ĐỘNG** — bộ mẫu Đảng ghi cơ quan cấp trên là *"Đảng bộ Khối các
  cơ quan Trung ương"*, mà KL 121-KL/TW mục II.2.1 đã **kết thúc hoạt động** tổ chức này; các cơ quan
  Quốc hội nay thuộc **Đảng uỷ Quốc hội** (Đảng bộ Quốc hội — QĐ 244-QĐ/TW ngày 24/01/2025).
  Cùng lỗi ở `BC_74_DU_UBQLV` (*"Khối Doanh nghiệp Trung ương"*, cũng đã giải thể). Cờ mới
  `TT-TO-CHUC-HET-HIEU-LUC` (WARN, hệ dang).
- **§6.30 NHẤT QUÁN KIỂU ĐẶT DẤU** — *"ĐẢNG UỶ ỦY BAN VĂN HOÁ VÀ XÃ HỘI"*: cùng chữ "ủy" mà hai từ
  cạnh nhau đánh dấu khác kiểu. Cả hai kiểu đều hợp lệ nhưng phải nhất quán trong một văn bản.
  Cờ mới `TT-CHINH-TA-DAU` (WARN).
- **§6.27 CÂN DÒNG, KIÊNG DÒNG 1 TỪ** — `_tt_can_dong` chia tên cơ quan dài thành các đoạn cân nhau
  tại ranh giới từ, mỗi dòng ≥2 từ. Không dùng `<w:br/>` (r143: br cứng làm dính chữ khi bóc text).
  ⚠ Kéo theo: ô trái có thể nhiều đoạn hơn ô phải ⇒ r145 nới assert §6.9 thành "cùng BỘ giá trị
  chiều cao dòng", chuỗi chỉ trùng khít khi hai ô cùng số đoạn (đúng §6.14).
- **§6.28 KHÔNG ĐỂ TRANG CHỈ CÓ KHỐI KÝ** — `keepNext` cho đoạn thân cuối + đoạn đệm + mọi đoạn
  trong bảng ký, `cantSplit` cho hàng bảng ký.
- **Phiếu trình**: đệm ô 6pt → **4pt** (user: hẹp lại một xíu, đừng như trước = 0).
- ★Hồi quy bắt được trong phiên: bỏ đoạn `chu_quan` RỖNG làm hai ô tiêu đề lệch chuỗi `w:line`
  (r145 đỏ) — chu_quan rỗng vẫn phải sinh một đoạn rỗng để giữ §6.9.

# ★ v1.34.94 — CHỨC VỤ người ký VB ĐẢNG không in đậm (HD05 PL2 mục 7) (2026-07-20)

> Rà TRỌN Phụ lục 2 HD 05-HD/VPTW (bản 27/5/2026) đối chiếu builder — cùng cách đã làm với NQ351.
> selftest 1124→**1125** (r162 đỏ-trước).

- **HD05 PL2 mục 7 tách rõ**: *quyền hạn* (`T/M …`, `K/T …`) = **Đứng, ĐẬM**; *chức vụ* (`BÍ THƯ`,
  `PHÓ BÍ THƯ`, `CHÁNH VĂN PHÒNG`…) = chỉ **Đứng**, KHÔNG đậm. Builder để **cả hai** đậm tới .93.
  Nhà nước thì ngược lại (NĐ30 PL I II.7.đ / NQ351 Đ37 k1: cả hai cùng đậm) — bẫy chéo hai hệ.
  **Reference §5.3 đã ghi ĐÚNG "đậm/đứng/đậm" từ trước** ⇒ lại là code mâu thuẫn neo của chính nó,
  y hệt ca TT-BAC-CO-CHU ở .86.
- Lỗi này **đã lọt vào văn bản giao ở .85** (`BC_74_DU_UBQLV_chuyen_doi_so_moi.docx` để `PHÓ BÍ THƯ`
  đậm). Đã dựng lại.
- **Tiêu chí mới `TT-CHUC-VU-DAM`** (WARN, hệ dang): đoạn IN HOA + mang từ chức danh + KHÔNG có tiền
  tố quyền hạn (T/M, K/T, TL., TUQ., Q.) mà in đậm ⇒ cảnh báo. Parser thêm cờ `dam` cấp đoạn.
- **Bộ 14 MẪU VĂN BẢN ĐẢNG** theo thể loại QĐ 399 dựng tại `D:\Quốc hội\mau-dang-hd05\`
  (nghị quyết, quyết định, chỉ thị, kết luận, quy định, quy chế, kế hoạch, chương trình, hướng dẫn,
  thông báo, báo cáo, tờ trình, đề án, biên bản). ⚠ HD05 **KHÔNG có** bộ mẫu theo thể loại như
  NQ351 — chỉ có sơ đồ bố trí (PL1), bảng cỡ chữ (PL2), mẫu dấu bản sao (PL3); bộ mẫu này dựng theo
  thể loại QĐ399 + thông số PL2. Mẫu TRỐNG FAIL `TT-SO-KY-HIEU`/`TT-DIA-DANH-NGAY` như thường lệ;
  bản điền số thật **0/0/0**.
- Sơ đồ PL1 (ảnh nhúng, trích `word/media/image1.png`) xác nhận lề Đảng **20/20/30/15mm ĐƠN TRỊ**.

# ★ v1.34.93 — đệm ô phải khai HAI TẦNG vì Google Docs bỏ tblCellMar (§6.26) (2026-07-20)

> Phát hiện khi verify bản mẫu .92 vừa upload: local đúng 120tw nhưng **trên Drive = 0**.

- Kho mẫu lưu **canonical dạng Google Doc** ⇒ .docx bị convert. Round-trip **BỎ HẲN** `tblCellMar`
  (và `tcMar`), trong khi `w:before`/`w:after` của đoạn **sống sót**. Chỉ dựa vào `tblCellMar` thì
  bản local đúng còn bản dùng thật (tải từ kho mẫu) lại dính nét kẻ — đúng lỗi user báo.
- **Khai hai tầng**: `tblCellMar` top/bottom (Word) **+** `w:after` cho **đoạn CUỐI mỗi ô có viền**
  (Google Docs). Áp cho bảng nội dung và bảng tổng hợp.
- r156 siết thêm: đoạn cuối của mọi ô có viền (trừ ô vMerge rỗng) phải có `w:after=120`.
  Xác minh ĐỎ-TRƯỚC.

# ★ v1.34.92 — ô có viền phải có đệm dọc (§6.25) (2026-07-20)

> User gửi ảnh: dòng cuối ô "Nội dung" của Phiếu trình **dính sát nét kẻ dưới**.

- **`tblCellMar` mặc định KHÔNG có top/bottom** — bộ dựng chỉ khai trái/phải 72tw nên chữ chạm viền.
  Nay khai **6pt = 120tw** trên và dưới cho **mọi bảng CÓ VIỀN**: bảng nội dung VÀ bảng tổng hợp ý
  kiến (bảng tổng hợp bị y hệt, sửa luôn cho nhất quán). Chỉnh: `spec.dem_o_pt`.
- **Bảng tiêu đề (không viền) giữ 0** — thêm đệm ở đó sẽ xô lệch khối tiêu đề đã tinh chỉnh theo
  §6.9-6.11 (gạch ôm sát chữ, hai ô cùng chuỗi `w:line`).
- r156 siết: đệm dọc bảng 1 = (0,0) · bảng 2 và 3 = (120,120). Xác minh ĐỎ-TRƯỚC.

# ★ v1.34.91 — Phiếu trình: "Kính gửi" không đậm, thụt 0,8cm trong bảng (§6.24) (2026-07-20)

- **"Kính gửi" KHÔNG in đậm** (user 20-07). Lưu ý: mẫu gốc CÓ đậm — đây là yêu cầu của Ủy ban ghi đè
  mẫu, không phải sửa lỗi.
- **Đề mục và mọi paragraph trong BẢNG nội dung thụt đầu dòng 0,8cm** (`spec.thut_bang_cm`, dải
  0,8–1cm, ưu tiên 0,8). Trước đó đề mục không thụt còn paragraph thụt 1cm. ⚠ 0,8cm THẤP HƠN dải
  1–1,27cm của NĐ30/NQ351 — hợp lệ vì phiếu trình là biểu mẫu NỘI BỘ (§6.21), không được áp sang
  văn bản phát hành.
- **Sửa thêm một chỗ tôi tự ý làm khác mẫu gốc**: dòng *"Nội dung: …"* — bản .90 để cỡ 13, dàn đều,
  thụt 1cm; mẫu gốc là **cỡ 14, canh giữa, không thụt**. Đối chiếu lại mới thấy, nay bám đúng gốc.
- r156 siết: "Kính gửi" không có `<w:b/>` · đề mục + paragraph trong bảng có `firstLine=454`.
  Xác minh ĐỎ-TRƯỚC.

# ★ v1.34.90 — Phiếu trình: mỗi cấp ký một dòng có viền + khe trước bảng (2026-07-20)

> User: *"khoảng cách giữa bảng nội dung và phần tiêu đề cần xa hơn. Phần ký bên cột trái của các
> chuyên viên cần có viền"*. Soi lại mẫu gốc thì đúng — và bản dựng của tôi sai CẤU TRÚC, không chỉ
> thiếu viền. selftest 1124 (r156 siết thêm).

- **§6.23 — bảng nội dung là bảng 4 DÒNG, không phải 1 dòng.** Mẫu gốc: dòng 1 = "Quá trình thực
  hiện" + "Đề xuất"; **mỗi cấp ký một dòng riêng** (Chuyên viên · Phó Vụ trưởng · Ủy viên chuyên
  trách); cột phải "Ý kiến của Chủ nhiệm Ủy ban" là MỘT ô dọc suốt bằng `<w:vMerge w:val="restart"/>`
  + `<w:vMerge/>`. Bản .88 gộp hết các cấp ký vào chung một ô ⇒ **không có viền ngăn giữa họ**.
  Nay mọi ô của bảng đều có viền trực tiếp.
- **Khe trước bảng nội dung** `spec.dem_bang_pt`, mặc định **18pt** (trước là 0 — bảng dính sát khối
  tiêu đề). Không có quy định định lượng, cùng lý do §6.19.
- r156 siết: số dòng = 1 + số cấp ký · vMerge đúng chỗ · MỌI ô bảng nội dung có `w:val="single"`.
  Xác minh ĐỎ-TRƯỚC.

# ★ v1.34.89 — sửa doctrine "tra-luat KHÔNG sinh docx" đã SAI từ .84 (2026-07-20)

> Lộ ra khi kiểm Instruction Block sau lúc nạp mẫu Phiếu trình vào profile UBVHXH.

- **`generate_profile_load_block` vẫn dạy "dựng .docx bằng công cụ docx của MÔI TRƯỜNG (tra-luat
  KHÔNG sinh docx)"** — sai kể từ v1.34.84 khi có `tl the-thuc-build`. Câu này nằm trong khối
  `trinh_bay_theo_mau` của MỌI profile có mẫu ⇒ đang chủ động dẫn nhầm sang công cụ ngoài trong khi
  skill dựng được và tự self-check. Thay bằng: dựng bằng `tl the-thuc-build` (hanh-chinh | dang |
  vbqppl-qh | mau=phieu_trinh) rồi kiểm `tl the-thuc-check`; mẫu phức tạp ngoài khả năng dựng mới
  dùng công cụ MÔI TRƯỜNG. RUNBOOK §D cùng nội dung.
- r132 trước đây **ghim đúng câu sai** (`"KHÔNG sinh docx" in _b`) nên đổi doctrine là test đỏ —
  đã cập nhật thành khẳng định NGƯỢC LẠI (`"tl the-thuc-build" in _b` và `"KHÔNG sinh docx" not in _b`).
- Mẫu Phiếu trình đã nạp vào profile "UBVHXH khóa XV": id `mau-phieu-trinh-ubvhxh-khung-sach`,
  drive_id `1cdDxcgyXrnW370yEzqLM8Kn9Xsci7C0qNICQM_Ej-8g` (bản CÓ viền). ★Lưu ý vận hành: kho mẫu lưu
  bản canonical dạng Google Doc ⇒ verify sau upload phải soi **CẤU TRÚC** (tblW/tcBorders), KHÔNG
  byte-match như deploy zip skill; và Google export ghi thuộc tính **thứ tự khác**
  (`<w:top w:color=… w:sz="4" w:val="single"/>`) nên đừng dò `<w:top w:val="single"`.
- ★`--template-scope` KHÔNG tự bỏ tiền tố: truyền "CHỈ KHI …" sẽ ra "CHỈ KHI CHỈ KHI …". Truyền vế
  điều kiện trần. Sửa entry = `--template-remove` rồi `--template-add` (add trùng id → TEMPLATE_ID_EXISTS).

# ★ v1.34.88 — Phiếu trình: bảng nội dung PHẢI có viền (§6.22) (2026-07-20)

> User: *"Phần nội dung Phiếu trình cần nằm trong bảng 02 cột, có border. Hiện nay không có border.
> Hãy nhìn cho kỹ"* — đúng, và nguyên nhân là tôi soi thiếu một tầng. selftest 1124 (r156 siết thêm).

- **Viền bảng có thể đến từ `tblStyle`, không chỉ `tblBorders` (§6.22)** — mẫu gốc VHXH để bảng nội
  dung mang `<w:tblStyle w:val="TableGrid"/>` với viền nằm trong `styles.xml`, KHÔNG có
  `<w:tblBorders>` trực tiếp. Lần rà trước chỉ tìm `tblBorders` nên kết luận NHẦM là "không viền" và
  dựng ra bảng nội dung trần. Quy trình soi viền nay ghi vào reference: tblBorders → tblStyle +
  styles.xml → tcBorders (ghi đè).
- Bộ dựng tự sinh `styles.xml` tối thiểu (không có TableGrid) ⇒ **đặt viền TRỰC TIẾP cấp ô**.
  Phiếu trình: bảng tiêu đề không viền · bảng nội dung CÓ viền · bảng tổng hợp CÓ viền.
- ★Bẫy khi viết test: dò `w:val="single"` trơn khớp cả `<w:u w:val="single"/>` (gạch chân tên cơ
  quan/Tiêu ngữ) ⇒ bảng tiêu đề bị coi nhầm là có viền. Dò `<w:top w:val="single"`. r156 đã siết
  thành `[False, True, True]` cho đúng ba bảng và xác minh ĐỎ-TRƯỚC.

# ★ v1.34.87 — khe khối ký (có rà quy định), Quốc huy, và bộ dựng PHIẾU TRÌNH (2026-07-20)

> Ba việc user nêu sau khi xem 19 mẫu + gửi mẫu Phiếu trình của Ủy ban Văn hóa và Xã hội.
> selftest 1123→**1124** (r154, r156).

- **Khe giữa nội dung và khối ký — RÀ QUY ĐỊNH, KẾT LUẬN: KHÔNG CÓ (§6.19)**. Đã đọc NĐ 30/2020
  PL I Mục II.6.e + **Mục IV sơ đồ bố trí** (ảnh nhúng trong docx, phải trích ra mới xem được) và
  NQ 351/2017 Đ35/Đ37: không văn bản nào ấn định khoảng cách này; ràng buộc duy nhất là "đoạn ≥6pt".
  Sơ đồ vẽ ô 6 và ô 7a ở hai băng tách rời nhưng chỉ ghi số cho LỀ TRANG. Đo tỷ lệ trên sơ đồ ⇒
  ≈8,4mm ≈ **24pt**, lấy làm mặc định (trước là 12pt — user thấy quá sát). Chỉnh: `spec.dem_ky_pt`
  (sàn 6pt). r154 khoá mặc định + khả năng chỉnh + sàn.
- **Quốc huy KHÔNG chừa chỗ bằng đoạn rỗng (§6.20)** — Mẫu 15a/15b/16 NQ351 trước đây chèn một đoạn
  trống để dành chỗ, Word hiển thị đúng là **một dòng trống ngay trên "CHỦ TỊCH NƯỚC"** (user phát
  hiện) và bộ kiểm cờ `TT-DONG-TRONG-DAU`. Quốc huy là ảnh NỔI, chèn đè. 19 mẫu đã dựng lại.
- **`the-thuc-build` dựng PHIẾU TRÌNH** — `spec.mau = "phieu_trinh"` (§6.21). Ba khối: tiêu đề 2 ô ·
  bảng 2 cột 70/30 "quá trình thực hiện + đề xuất + các cấp ký | ý kiến lãnh đạo" · bảng TỔNG HỢP Ý
  KIẾN 4 cột CÓ viền. Là **biểu mẫu nội bộ**, không phải VB phát hành ⇒ tự loại `TT-SO-KY-HIEU`,
  `TT-NOI-NHAN`, `TT-CHUC-VU-KY`, `TT-TEN-LOAI` khỏi kết luận self-check.
  ⚠ **Mẫu gốc để cả 3 bảng TRÀN lề** (9180 / 10065 / 9180 twips > vùng chữ 9072) và nội dung cỡ 12
  (NĐ30 đòi 13-14) — bộ dựng tính bề rộng từ `sectPr` nên bản sinh ra không tràn. r156 khoá.
  Thêm cấp phát ô tiêu đề theo nhu cầu THẬT của CẢ HAI nhánh (tên "ỦY BAN VĂN HÓA VÀ XÃ HỘI" cỡ 13
  tràn ô 59 twips ⇒ hạ về cỡ 12, NĐ30 cho 12-13).
- **r155 tách `_tt_ghi_docx`** — đóng gói docx dùng chung cho cả hai bộ dựng. ★Bẫy khi tách: chuỗi
  `env_chk = the_thuc_check(out_path` có MẶT ở `the_thuc_normalize` TRƯỚC `the_thuc_build` ⇒ phải
  `index(..., i)` tìm SAU mốc đầu, nếu không sẽ cắt nhầm khối rỗng (assert đã chặn).
  Tên module mới phải đăng ký vào bảng re-export trong `tl.py` nếu không r90 đỏ.

# ★ v1.34.86 — vá 3 lỗ hổng bộ kiểm hệ vbqppl_qh + `the-thuc-build --he vbqppl-qh` (2026-07-20)

> Bắt nguồn từ việc dựng thử **19 mẫu Phụ lục I NQ 351/2017**. Sơ đồ 19 mẫu là **ẢNH** ở PDF Công báo
> 287+288 trang 17-35 (bản GDoc mất sạch phần này) — render bằng PyMuPDF mới đọc được, nhờ đó chốt
> được ngưỡng treo từ 19-07. selftest 1118→**1122** (r150-r153, cả 4 ĐỎ-TRƯỚC đã xác minh).

- **(1) TT-BAC-CO-CHU áp nhầm NĐ30 cho hệ vbqppl_qh** — sơ đồ NQ351: **Quốc hiệu 12 · Tiêu ngữ 14**
  (bậc +2pt; Mẫu 16 là 13/14). Quy tắc "+1pt" của NĐ30 Mục V chỉ dành cho hành chính/vbqppl/vbhn.
  Hệ quả cũ: MỌI VBQPPL của Quốc hội bị WARN oan — trong khi **NEO cuối reference đã ghi ĐÚNG**
  (`quoc_hieu=12-12 tieu_ngu=14-14`), tức code mâu thuẫn với chính neo của nó. **§6.17**.
- **(2) TT-DIA-DANH-NGAY cảnh báo oan cho luật/NQ Quốc hội** — Đ3 k1 NQ351: phần mở đầu luật, bộ luật,
  nghị quyết của Quốc hội KHÔNG có địa danh; thời điểm thông qua ghi CUỐI văn bản (Đ36 k1). Nhận diện
  bám ký hiệu CỦA CHÍNH VB (match `Số: n/năm/KH` đầu tiên) — không bám `QH\d` trôi nổi vì căn cứ hay
  dẫn *"Luật … số 57/2014/QH13"*.
- **(3) Mẫu 6b/11b/14 bị FAIL oan** — văn bản ban hành kèm theo không có số-KH/địa danh/căn cứ; phụ lục
  (Mẫu 14) thêm nữa là không có Quốc hiệu/Tiêu ngữ/người ký. Đều LÀ THIẾT KẾ. **§6.18**.
  ⚠ **Bẫy đã sập trong phiên**: bỏ qua nhánh nhà nước cho phụ lục mà quên chặn ⇒ rơi xuống nhánh Đảng,
  đòi "ĐẢNG CỘNG SẢN VIỆT NAM" (FAIL oan kiểu khác). r152 khoá đúng ca này.
- **`tl the-thuc-build --he vbqppl-qh`** — hệ dựng thứ ba. Spec thêm `co_quan_ban_hanh`, `can_cu[]`,
  `tu_lenh` (QUYẾT NGHỊ:/NAY…:/QUYẾT ĐỊNH:), `thong_qua` (tự chèn kẻ ngang Đ36 k1), `body[].kieu="giua"`
  (Phần/Chương/Mục + tiêu đề, đậm canh giữa). Đặc trưng hệ: Tiêu ngữ 14 · **KHÔNG gạch dưới tên gọi** ·
  căn cứ nghiêng · "(Ký và đóng dấu)" · họ tên 14 trong khi chức vụ 13 · không Nơi nhận nếu không khai.
- **19 mẫu đã dựng**: `D:\Quốc hội\mau-nq351\` + `GHI_CHU.md` (Quốc huy Mẫu 15a/15b/16 chèn tay).
  Mẫu 6b/11b/14 nay **0/0/0**. Mẫu TRỐNG vẫn FAIL `TT-SO-KY-HIEU` vì số hiệu "…/20…/QH…" không có chữ
  số — đã kiểm chứng bằng bản điền số thật (Luật 45/2019/QH14) → **0 FAIL**, không phải lỗi mẫu.
- Golden `parser_surface` regen CHỦ ĐÍCH đúng **1 lệnh** (`the-thuc-build` — thêm choice `vbqppl-qh`).
  Kernel CHỈ đổi header (47.751B, đệm 377B) ⇒ **re-import Capabilities KHÔNG bắt buộc**.

# ★ v1.34.85 — vá 4 lỗi VB Đảng/đơn-vị-trực-thuộc do thực chiến lộ + §6.14-6.16 (2026-07-20)

> User thử 2 VB (khối Chính phủ tên đơn vị dài · thể thức Đảng) → chỉ ra 4 lỗi, tra NGUYÊN VĂN HD05
> xác nhận. selftest 1116→**1118** (r147 ×1, r148 ×1 đỏ-trước; +r149 nới regex chức vụ).

- **(1) "Nơi nhận" VB ĐẢNG KHÔNG ĐẬM** — PL2 HD05: In thường · cỡ 14 · *"Đứng, CÓ GẠCH CHÂN"*, không
  có "đậm"; builder .84 để đậm = SAI. Hệ nhà nước GIỮ nghiêng+đậm (NĐ30 Mục V). Reference thêm khối
  ⚠ĐÍNH CHÍNH vì đây là chỗ rất dễ nhầm giữa 2 hệ.
- **(2) Gạch dưới tiêu đề ĐCSVN cách quá xa** — builder .84 chèn đoạn đệm ép 2 ô cân số đoạn; nhánh
  trái (tên CQ dài 2 dòng) ≠ nhánh phải (tiêu đề 1 dòng) nên đệm đẩy gạch rơi xa. **§6.14**: hai nhánh
  lệch dòng thì KHÔNG bắt buộc ngang nhau, gạch phải ÔM SÁT chữ nhánh mình (HD05 1.2: gạch "ngăn cách
  tiêu đề với địa danh"). Bỏ đoạn đệm.
- **(3) Dấu sao (*) bị CẮT NGỌN, nhìn như vết bẩn** — đoạn dấu sao để `line 8pt exact` trong khi chữ
  14pt ⇒ Word cắt từ trên. **§6.15**: đoạn có CHỮ THẬT phải `line ≥ cỡ chữ` (hoặc `atLeast`); chỉ đoạn
  GẠCH (toàn NBSP) mới được ép nhỏ. r148 khoá quy tắc cho MỌI đoạn trong bảng tiêu đề.
- **(4) Cấu trúc chủ quản vs ban hành (§6.16)** — đơn vị trực thuộc (vụ/cục/phòng) ra VB nhân danh
  mình: chủ quản in hoa KHÔNG đậm ở trên, đơn vị ban hành in hoa ĐẬM + gạch dưới ở dưới; ký hiệu theo
  đơn vị ban hành; người ký ghi chức vụ ĐỨNG MỘT MÌNH (VỤ TRƯỞNG), không TL./KT. r149: bộ kiểm
  TT-CHUC-VU-KY nhận thêm chức danh cấp vụ/cục/phòng/chủ nhiệm; builder bỏ dòng ký rỗng khi chỉ 1 dòng.
- Thực chiến bản cuối: `BC_187_CNHT_ha_tang_CNTT.docx` (0 FAIL, 1 WARN wrap tên chủ quản 44 ký tự —
  đúng thực tế) · `BC_74_DU_UBQLV_chuyen_doi_so_moi.docx` (**0/0/0**). Kernel CHỈ đổi header.

# ★ v1.34.84 — ĐÚC KẾT THỰC CHIẾN: 4 tiêu chí kiểm mới + lệnh `tl the-thuc-build` (2026-07-20)

> User duyệt "OK, tổng hợp kinh nghiệm vào skill" sau khi nghiệm thu BC rà soát thể thức. Toàn bộ lỗi
> trình bày user chỉ ra trong phiên (kẻ ngang lạ trên Quốc hiệu · gạch không cân xứng · hai gạch lệch
> cao độ · spacing sít · Nơi nhận chưa đậm · khối ký lệch · bảng tràn lề · dòng trống thừa) nay thành
> TRI THỨC + BỘ KIỂM + BỘ SINH. selftest 1114→**1116** (r144 ×1, r145 ×1 đỏ-trước; +r146 vá bug).

- **Reference §6.9–6.13 MỚI**: hai gạch đồng cấu trúc + công thức độ dài gạch `len×K×pt×tỷ_lệ/(0.25×pt_gạch)`
  (K=0.62 hoa / 0.50 thường; tỷ lệ 0.42 tên CQ & trích yếu, 1.00 Tiêu ngữ) · bảng ≤ vùng chữ · cân
  khoảng quanh gạch · viền nil ĐỦ 4 cạnh · khối cuối = bảng 2 ô + ≥5 dòng ký + dọn đoạn rỗng đầu.
- **4 TIÊU CHÍ KIỂM MỚI (r144)**: `TT-BANG-TRAN-LE` (FAIL — tblW > pgSz−lề, lỗi kế thừa mẫu lề khác) ·
  `TT-VIEN-O-SOT` (WARN — tcBorders nil 3/4 cạnh → cạnh còn lại hiện thành kẻ ngang) · `TT-GACH-SHAPE`
  (WARN — gạch vẽ bằng drawing, không co theo chữ) · `TT-DONG-TRONG-DAU` (INFO — đoạn rỗng đầu VB).
- **LỆNH MỚI `tl the-thuc-build --spec <json> --out <docx>` (r145)**: sinh docx ĐÚNG-BY-CONSTRUCTION 2 hệ
  (hành chính NĐ30 · Đảng QĐ399+HD05) từ package tối thiểu tự dựng; bề rộng bảng tính từ lề, ô phải
  luôn đủ chứa Quốc hiệu/tiêu đề 1 dòng (tên CQ dài nhận phần còn lại — xuống dòng là chấp nhận được),
  gạch theo công thức, tự self-check bằng `the-thuc-check`. ⚠ Lề mặc định KHÁC theo hệ: nhà nước
  20/20/30/20 (§6.8) · **Đảng 20/20/30/15 ĐƠN TRỊ** (HD05 IV.4.1); giãn dòng Đảng 18–22pt Exactly áp
  MỌI khối kể cả tiêu đề/nơi nhận/ký (bug builder bắt được khi thử VB Đảng đầu tiên).
- **r146 vá bug do chính test thực chiến lộ ra**: `TT-THUT-DE-MUC` đếm nhầm dòng "Nơi nhận" trong BẢNG
  (§6.7 nói rõ bảng KHÔNG áp thụt) → parser nay đánh dấu `in_tbl`, T3 bỏ qua; regex đề mục nhận thêm
  kiểu Đảng `I-` / `1-` (HD05 dùng gạch nối thay dấu chấm).
- Golden regen chủ đích (+1 lệnh); _STUB_MAP +6. Kernel CHỈ đổi header.

# ★ v1.34.83 — QUỐC HIỆU/TIÊU NGỮ CHÍNH XÁC TUYỆT ĐỐI + tích hợp §6.6-6.8 (2026-07-19)

> User yêu cầu "tiêu ngữ, quốc hiệu phải chính xác tuyệt đối, không được sai" + tích hợp 3 điều chỉnh
> thể thức (bản THE_THUC_TRINH_BAY.md có §6.6-6.8 do user chép đè — đã THẨM ĐỊNH: diff chỉ +6 dòng §6
> + newline cuối, LF thuần, 18 anchor r135 + NEO nguyên vẹn, selftest xanh trước khi nhận).

- **EXACT-match r143 (đỏ-trước ×3, selftest 1111→1114):** Quốc hiệu/Tiêu ngữ/tiêu đề Đảng so ĐÚNG TỪNG
  KÝ TỰ sau chuẩn hoá NFC + space-class (NBSP/tab→space, gộp space — docx macOS dính NFD không FAIL
  oan): tìm thấy BIẾN THỂ gần đúng (bỏ dấu/case/gạch/space so lỏng) mà lệch nguyên văn → **FAIL
  `TT-QUOC-HIEU-SAI` / `TT-TIEU-NGU-SAI` / `TT-TIEU-DE-DANG-SAI`** kèm dòng sai — bắt được: en-dash
  "–" thay "-", thiếu dấu tiếng Việt, dính chữ do <w:br/> cứng giữa Quốc hiệu, sai hoa-thường.
- **WARN vỡ-dòng mềm §6.6** (đúng TÊN cờ reference hứa): `QUOC_HIEU_WRAPPED`/`TEN_CQ_WRAPPED` — ước
  lượng est=len×pt×0.62×20tw so tcW ô bảng header (hàng đầu chứa Quốc hiệu; K=0.62 TNR in hoa).
- **INFO `TT-THUT-DE-MUC` §6.7**: ≥3 đề mục/gạch đầu dòng và >50% thiếu thụt dòng đầu ~1cm (567tw).
- §6.8 (giá trị khuyến nghị tạo file) là advisory trong reference — normalize GIỮ 15mm lề phải (cận
  dưới dải; 18-20 của §6.8 cũng trong dải — cả hai đạt khi kiểm). Không đổi NEO/hằng → golden 0-diff
  (trừ bundle do reference đổi). Smoke: demo công văn giữ ok/0-FAIL, không cờ mới oan.
- _STUB_MAP +4 helper (bẫy r90). Kernel CHỈ đổi header.

# ★ v1.34.82 — bất biến 18 CORPUS-FIRST khi TÌM/NẠP (user yêu cầu nguyên văn) (2026-07-19)

> User bổ sung nguyên tắc bất biến 18 vào kernel: **rà corpus VBQPPL + mọi shard TRƯỚC khi tìm/tải nguồn
> ngoài** (`reg-query` biến thể số hiệu · `locate` · `dedup-check` · `slot-audit --all-shards`; nền
> 743ed200 + VBQPPL-2 45739ff7); CHỈ nạp phần MISS; đã corpus=true (nhất là VBHN mới nhất) → báo "đã có"
> + vị trí, KHÔNG nạp trùng; áp cho fetch-route/fetch-links/find-doc + "lấy văn bản này về". r142
> đỏ-trước khóa: anchor + MỌI lệnh mục 18 hứa phải TỒN TẠI trong parser (dedup-check cần positional
> query — test chỉnh theo cú pháp thật). selftest 1110→**1111**.

- **ĐÍNH CHÍNH mốc size kernel** (memory/CHANGELOG .81 ghi nhầm "đệm 18B"): code thật
  `_kernel_size_findings` warn=47×1024=**48.128B**, fail=48×1024=**49.152B** — kernel .82 = **47.751B**,
  đệm thật tới WARN còn **377B** (vẫn chật — cân nhắc diet trước khi thêm lớn).
- Kernel ĐỔI RUỘT (tiếp .81) → deploy .82 xong RE-IMPORT Capabilities (một lần cho cả chuỗi từ .69).
- Golden workflow_audit regen chủ đích (size_bytes 47.086→47.751); parser không đổi.

# ★ v1.34.81 — normalize choices 5 hệ (+vbqppl-qh) + kernel DANH MỤC trỏ THE_THUC_TRINH_BAY (2026-07-19)

> Đóng backlog seed 19-07 (r141 đỏ-trước, selftest 1109→**1110**): (1) `the-thuc-normalize --he` đồng
> bộ bộ choices với the-thuc-check — `auto|hanh-chinh|vbqppl|vbqppl-qh|vbhn|dang` (+`nha-nuoc` GIỮ làm
> alias cũ .78 = 13pt/self-check auto); `dang|vbqppl-qh` → 14pt — mẫu Luật HẾT phải mẹo `--he dang`;
> `auto` nay dùng `_the_thuc_detect_he` THẬT (envelope `he` = hệ detect; self-check ép đúng hệ khi
> flag). ★Bẫy vá kèm: bóc plain-text cho detect PHẢI chèn `\n` tại `</w:p>` TRƯỚC khi strip tag —
> detect anchored `^Số:` (r140) cần ranh giới dòng, thiếu là mẫu Luật auto rớt về hanh_chinh.
> (2) **Kernel DANH MỤC REFERENCES +1 dòng** trỏ `references/THE_THUC_TRINH_BAY.md` (99B — kernel
> 46.987→**47.086B**, đệm tới WARN-47.104 còn **18B**: KHÔNG thêm gì vào kernel nữa nếu chưa diet) —
> agent Capabilities nay thấy bộ thể thức ngay từ kernel thay vì chỉ qua RUNBOOK.
> **⚠ KERNEL ĐỔI RUỘT (lần đầu từ .70) → RE-IMPORT Capabilities BẮT BUỘC khi deploy .81** — gộp sạch
> nợ re-import treo từ .69 luôn một lần.

- Golden regen CHỦ ĐÍCH: parser_surface (hash the-thuc-normalize — choices đổi) + workflow_audit
  (size_bytes 47.086, links_checked 14→**15** — link-check xác nhận reference tồn tại).
- Backfill-markers DRY: 15 profile → 14 has_marker + vbthuong `skipped_vbt_root` **BY-DESIGN** (root
  là chính Van_ban_thuong gốc — marker ở đó nhiễu discover; định danh qua config). Backlog
  "vbthuong MARKER_MISSING" ĐÓNG bằng kết luận, không phải bug.

# ★ v1.34.80 — fix detect-hệ the-thuc-check: viện dẫn VBQPPL trong thân không làm lệch hệ (2026-07-19)

> Gap do DEMO điền Mẫu 1.5 bắt được (data-op seed 19-07): công văn hành chính viện dẫn "…Nghị định số
> 30/2020/NĐ-CP ngày…" trong THÂN → regex bare `\d+/\d{4}/` của `_the_thuc_detect_he` nhầm he=vbqppl
> (sai ngưỡng lề trên/dưới 15-20 thay 20-25 + đòi năm trong số ký hiệu) — ca PHỔ BIẾN vì mọi công văn
> đều viện dẫn VBQPPL. Fix r140 (đỏ-trước): detect vbqppl/vbhn chỉ nhận SỐ KÝ HIỆU CỦA CHÍNH văn bản —
> anchored đầu dòng `^\s*(Bộ luật|Luật|Pháp lệnh|Lệnh|Nghị quyết|Nghị định|Quyết định|Thông tư)? [Ss]ố:`
> ("Luật số: 64/2025/QH15" ✓, "Số: 250/2026/NĐ-CP" ✓, "Số: 4231/VBHN-BTP" ✓; viện dẫn giữa câu KHÔNG
> match). selftest 1108→**1109**.

- Hệ quả chủ đích: file PHỤ LỤC trộn ví dụ (BIEU_MAU/PHU_LUC_ND250) nay auto-detect về hanh_chinh —
  loại file này VỐN phải ép `--he` (hành vi ghi từ R2); VB đơn hệ thật đều đúng (4231→vbhn giữ nguyên,
  demo công văn→hanh_chinh ok:true fail=0).
- DEMO end-to-end 3 tầng ĐÃ CHẠY TRỌN: khung Mẫu 1.5 kho chung → điền công văn thật (thay text trong
  w:t theo para, GIỮ run-format; header mẫu là BẢNG — thao tác para-level, DROP chỉ ngoài bảng) →
  `the-thuc-check` PASS (0 FAIL; 1 WARN nhất-quán-bậc là của khung gốc NĐ30 in Quốc hiệu=Tiêu ngữ=13).
- Kernel CHỈ đổi header; không đổi CLI → golden 0-diff.

# ★ v1.34.79 — fix: profile-load hiện khối trinh_bay_theo_mau (templates pass-through chiều ĐỌC) (2026-07-19)

> BUG do SMOKE GHI THẬT 19-07 bắt (seed kho chung xong, template-add vào NQ80 marker verified NHƯNG
> `tl profile-load` không hiện khối): `_profile_block_meta` — WHITELIST hợp nhất marker→meta chiều
> ĐỌC — **thiếu pass-through `templates`** → khối trinh_bay_theo_mau (v1.34.71) không bao giờ tới
> profile-load dù marker có. Bản SONG SINH của bẫy `_marker_body` chiều GHI (r132a chỉ khóa ghi);
> r132 test gọi THẲNG generate_profile_load_block với meta tự dựng nên lọt gap đúng CHỖ NỐI.

- Vá 1 dòng `_profile_block_meta` +key `templates` (list, fail-safe []); phủ cả 2 caller
  (profile-load marker-live + profile-use offline). TDD r139 đỏ-trước khóa 2 tầng: unit
  (hàm pass-through) + tích hợp (marker → meta → generate → khối hiện). selftest 1107→**1108**.
- Smoke end-to-end THẬT sau vá: add `mau-cong-van-1-5` (kho chung `1WscZ5bK…`) vào NQ80 →
  `profile-load NQ80` hiện khối đủ id/tên/drive_id/scope "CHỈ KHI…" → remove sạch (2 journal).
- Bài học khóa: mọi WHITELIST hợp nhất field marker phải soi CẢ HAI CHIỀU ghi/đọc khi thêm field mới.
- Kernel CHỈ đổi header — re-import không bắt buộc. Không đổi CLI → golden 0-diff.

# ★ v1.34.78 — R4 the-thuc: lệnh `tl the-thuc-normalize` (chuẩn hoá khung mẫu) (2026-07-19)

> R4/4 — MẢNH CODE CUỐI của kế hoạch the-thuc (r138 ×3 đỏ-trước, selftest 1104→**1107**).
> `the-thuc-normalize <in> <out> [--he]`: sectPr portrait → A4 + lề **20/20/30/15 mm** (bộ giá trị nằm
> trong dải CẢ 3 hệ, trùng lề cố định VB Đảng — §2 kế hoạch); docDefaults → TNR + sz hệ (nhà nước
> 13pt/Đảng 14pt); style Normal BỎ rFonts/sz/szCs đè (ca ND250 Normal=Arial đè docDefaults=TNR);
> KHÔNG đụng run-level rPr; section landscape giữ nguyên trọn. Sửa bằng REGEX TARGETED trên string XML
> (không parse-serialize toàn bộ — tránh vỡ namespace); zip repack date cố định 1980 → deterministic,
> normalize(normalize(x)) == normalize(x) byte-equal (test khoá). **Self-gate: the_thuc_check(out)
> phải hết FAIL nhóm T1** — file có run-format sai (vd HD05 run 10pt) không cứu được là CHỦ ĐÍCH
> fail-closed. in==out chặn IN_OUT_SAME.

- Smoke thật: BIEU_MAU_ND187 (Arial 100% + lề 10mm + no-sz) → normalize → **t1_fail 0** (sections_fixed
  1, docdefaults_replaced); còn lại chỉ finding T2 của file-phụ-lục-trộn (ngoài phạm vi khung).
- GENERATED_SPECS + COMMAND_META (low/write local — không Drive/registry/NLM) + _STUB_MAP +2; golden
  parser_surface regen chủ đích +1 hash; workflow_audit/tool_inventory counters +1 lệnh (regen chủ
  đích). COMMANDS.md +1 row. Kernel CHỈ đổi header — re-import không bắt buộc.
- Data-op seed 10 mẫu kho chung `_meta/templates` chạy NGAY SAU release này (cắt mẫu từ file gộp bằng
  script scratchpad khuôn extract.py; mỗi mẫu normalize + check T1-clean trước upload).

# ★ v1.34.77 — R3 the-thuc: T2 cấu trúc + T3 khuyến nghị cho `the-thuc-check` (2026-07-19)

> R3/4 kế hoạch the-thuc (TDD r137 ×5 đỏ-trước, selftest 1099→**1104**). **T2 — hiện diện CẤU TRÚC**
> (regex trên text bóc): thành phần bắt buộc theo hệ (Quốc hiệu/Tiêu ngữ FAIL — hệ Đảng: tiêu đề ĐCSVN;
> TT-SO-KY-HIEU đúng cú-pháp-hệ với bẫy CHÉO `Số 06-CT/TU` Đảng vs `Số: 06/CT-UBND` nhà nước — dùng
> nhầm bị gọi tên tường minh; địa danh-ngày [vbqppl/vbqppl_qh WARN vì Đ71 "nếu có"]; Nơi nhận
> [hanh_chinh/dang FAIL, vbqppl WARN, luật skip]; tên loại + chức vụ ký + Căn cứ = WARN heuristic;
> Đảng: TT-DANG-SAO dấu (*) + TT-DANG-5GACH `-----` FAIL; VBHN: TT-VBHN-LIET-KE ≥2 tham chiếu
> `số n/năm/` + TT-VBHN-CHU-THICH mẫu câu "được sđbs theo quy định tại…" + TT-VBHN-XAC-THUC). **T3 —
> khuyến nghị**: TT-BAC-CO-CHU nhất-quán-bậc (đo sz Quốc hiệu↔Tiêu ngữ phải lệch đúng 1pt — footnote
> Mục V NĐ30; Đảng: tiêu đề ≠15pt); TT-SO-NHO-10 (ngày<10/tháng<3 đệm 0); TT-THUT-DAU-DONG (w:ind
> 1-1,27cm / Đảng ~10mm, INFO); TT-VIET-TAT (đối chiếu 4 bảng viết tắt, INFO); TT-DONG (Đảng 18-22pt
> Exactly, WARN).

- **2 fix từ smoke file thật (giá trị dogfooding):** (1) `_the_thuc_detect_he` nhận VBHN dạng số CŨ
  `n/VBHN-CQ` không năm (ca 4231/VBHN-BTP — trước bị phân nhầm vbqppl); (2) parser đọc thêm
  **word/footnotes.xml** — chú thích chân trang VBHN nằm ở đó trong docx chuẩn (bản GDoc inline-hoá nên
  corpus-text có; docx gốc tách file → TT-VBHN-CHU-THICH từng FAIL oan). Fixture builder hỗ trợ
  footnotes; ca khoá trong r137.
- Smoke: 4231 local → he=vbhn, T2 checklist PASS trọn (chỉ còn 4 FAIL T1 Arial/lề đã biết); HD05 →
  he=dang, sao/gạch/số/thể loại PASS. Parser mở rộng paras (ind/spacing/sz-resolved per-paragraph).
- Data-op cùng phiên (trước R3): **PDF NQ351 Công báo lưu Drive làm nguồn đối chiếu** — upload qua
  gws_bridge vào cat 44 (`1pHjHkm5AC1pgOfhCAjHESna5gAGmjxO_`), register `row_kind=ref corpus=false`
  (không đẩy NLM — mẫu dạng ảnh); reference §0 đã trỏ từ v1.34.76.
- COMMANDS.md row + RUNBOOK row cập nhật T1+T2+T3; _STUB_MAP +2; kernel CHỈ đổi header — re-import
  không bắt buộc.

# ★ v1.34.76 — the-thuc: chốt ngưỡng lề nhánh QH (NQ351) từ PDF sơ đồ; WARN→FAIL (2026-07-19)

> User cấp **PDF gốc NQ 351/2017 (Công báo 287+288)** — digital 39 trang, đủ lời văn Đ1-40 + Phụ lục I
> (16 mẫu sơ đồ) + Phụ lục II (viết hoa). Render sơ đồ Mẫu 1-2 (PyMuPDF): **chú thích lề trên mẫu =
> trên/dưới 20-25, trái 30-35, phải 15-20 mm** (nhất quán, = hệ hành chính NĐ30) — đúng số corpus GDoc
> thiếu (chỉ ghi "định lề theo Phụ lục"). Font/cỡ chữ trên sơ đồ khớp 100% text đã trích (Quốc hiệu 12,
> Tiêu ngữ 14, số ký hiệu 13, tên luật 14, nội dung 14, chức vụ 13, họ tên 14).

- Nhánh **vbqppl_qh** trước để lề WARN dải-hợp (corpus thiếu sơ đồ số) → nay áp **FAIL** với ngưỡng thật
  20-25/20-25/30-35/15-20 mm. Sửa `_the_thuc_criteria` (na→ranges, bỏ ghi_chu) + NEO block reference +
  CAN_LE citation + docstring. NEO drift-lock r136 tự khớp (render == reference).
- Test r136_vbqppl_qh_rules cập nhật: lề hợp lệ → 0 finding lề; lề 10mm → TT-LE-TREN/DUOI FAIL; 13pt →
  TT-CO-CHU FAIL (14 cố định). selftest 1099/1099 (không đổi count — sửa case sẵn).
- Reference §0 cập nhật drive_id NĐ30 phụ lục (bản docx gốc mới nạp 19-07, overflow) + nguồn NQ351 (GDoc
  lời văn + PDF sơ đồ). Kernel chỉ header — re-import không bắt buộc.
- **Quyết định corpus:** GIỮ GDoc `19YN7y4` làm bản NQ351 text-queryable (NLM); KHÔNG nạp PDF làm bản
  trùng (mẫu là ảnh, không query text được; số lề đã vào reference). PDF lưu làm nguồn đối chiếu.

# ★ v1.34.75 — R2 the-thuc: lệnh `tl the-thuc-check` (T1 + phân luồng 4+1 hệ) (2026-07-19)

> R2/4 kế hoạch the-thuc (user duyệt 6/6 + LÀM LUÔN cùng phiên R1). **ĐÍNH CHÍNH PHÁP LÝ từ user:
> NQ 351/2017/UBTVQH14 VẪN HIỆU LỰC cho thể thức VBQPPL của QH/UBTVQH/CTN** (chưa có văn bản thay thế;
> NĐ CP không bãi bỏ được NQ UBTVQH; user viết "NQ 371" = 351 — registry số 371: 0 hit) → hệ VBQPPL
> TÁCH 2 NHÁNH: `vbqppl_qh` (NQ351 — thân 14 CỐ ĐỊNH, Quốc hiệu 12, lề chỉ WARN vì Đ39.1 định lề theo
> Phụ lục SƠ ĐỒ chưa có bản máy-đọc trong corpus) và `vbqppl` (NĐ78+PL I NĐ187). Reference cập nhật
> §0/§1/§3.4/§9 + NEO thêm dòng vbqppl_qh; ĐỀ NGHỊ USER nạp bản NQ351 đầy đủ phụ lục để chốt ngưỡng lề.

- **Module MỚI `tl_core/the_thuc.py`** (stdlib-only zipfile+ET — docx=zip; KHÔNG python-docx):
  `tl the-thuc-check <docx> [--he auto|hanh-chinh|vbqppl|vbqppl-qh|vbhn|dang] [--strict] [--json]
  [--out f]` — T1 đo cứng: TT-KHO-GIAY (A4 ±1mm) / TT-LE-* (per-section, dải theo hệ; Đảng đơn trị
  20/20/30/15) / TT-TRINH-BAY-NGANG (landscape → WARN, bỏ kiểm lề section đó) / TT-FONT (resolve 3
  tầng run→Normal→docDefaults — ca ND187 0 rFonts bắt được) / TT-CO-CHU-NOI-DUNG (mode w:sz theo
  lượng chữ; vắng sz → WARN không đoán). Finding kèm `can_cu` nguyên văn. Envelope
  `the_thuc_check.v1` deterministic; rc 0/2; `--strict` nâng WARN→FAIL.
- **Drift-lock 2 chiều:** `the_thuc_neo_lines()` render từ hằng `_the_thuc_criteria()` phải == 6 dòng
  block NEO-DRIFT-LOCK trong THE_THUC_TRINH_BAY.md (r136 so từng dòng) — đổi 1 phía là selftest đỏ.
- **TDD r136 ×6 đỏ-trước** (fixture docx TỰ SINH temp-dir, không commit binary): pass/fail lề+font
  (tái tạo ca ND187), phân luồng 4 hệ, landscape+sz-missing WARN, nhánh QH (14 cố định pass / 13 FAIL
  / lề lệch chỉ WARN), CLI+deterministic+strict-rc. selftest 1093→**1099**.
- **SMOKE THẬT 4 docx `bieu-mau-the-thuc\`**: cả 4 FAIL đúng dự đoán mổ-XML 19-07 — ND187/HD05/ND250
  Arial 100% + lề 10mm + 12/10pt; HD05 nhận he=dang, ND250 nhận he=vbhn; ND30 lề 27,5/22,6mm. Bộ kiểm
  bắt lỗi thật ngay ngày đầu. (Hành vi biết: file PHỤ LỤC trộn ví dụ nhiều hệ → auto-detect có thể
  nghiêng vbqppl — ép `--he` khi kiểm file kiểu này; VB đơn hệ không bị.)
- Đăng ký: GENERATED_SPECS + COMMAND_META (`low/read-only/none`, det_json, module the_thuc);
  `_STUB_MAP` +8 tên; bind tuple +_tl_the_thuc. Golden `parser_surface` regen CHỦ ĐÍCH đúng +1 dòng
  hash lệnh mới. COMMANDS.md +1 row (CRLF giữ, escape `\|` GFM); RUNBOOK §D row thể thức cập nhật.
- Kernel CHỈ đổi header (46.987B giữ) — re-import không bắt buộc.

# ★ v1.34.74 — R1 the-thuc: reference THE_THUC_TRINH_BAY.md — NEO 4 hệ thể thức (2026-07-19)

> Kế hoạch `D:\Quốc hội\ke-hoach-the-thuc-2026-07-19.md` user duyệt 6/6 câu grill (tích hợp tra-luat,
> 3 tầng KHUNG/ĐIỀN/KIỂM, seam tách-được). R1 = neo tri thức: `references/THE_THUC_TRINH_BAY.md` trích
> NGUYÊN VĂN corpus (verify 19-07): 4 bảng ngưỡng (hành chính NĐ30 PL I; VBQPPL = lời văn NĐ78 Đ60-71 +
> **PL I NĐ187/2025 — PL I-IV NĐ78 bị NĐ187 THAY TOÀN BỘ** Đ3k3 hiệu lực 01/7/2025; VBHN NĐ250/2026
> font/lề DẪN CHIẾU VBQPPL + checklist cấu trúc; Đảng QĐ399+HD05 bảng riêng) + ma trận loại-VB→hệ→mẫu
> (NĐ30 14 mẫu; NĐ187 PL II 19 + PL III 26 + PL IV 12; HD05 PL 1-3) + cảnh báo 4 file mẫu bóc KHÔNG đạt
> chuẩn (Arial/lề 10mm — mổ XML 19-07, không seed thẳng, phải normalize R4) + block **NEO-DRIFT-LOCK**
> máy-đọc cho R2 `the-thuc-check`. selftest 1092→1093 (r135 đỏ-trước: exists+LF+in-bundle+18 anchor
> nguyên văn+6 dòng NEO).

- Số then chốt: lề 2 hệ nhà nước KHÁC nhau (NĐ30 trên/dưới 20-25mm vs NĐ187 trên/dưới/phải 15-20mm,
  trái đều 30-35); bộ lề 20/20/30/15 nằm trong dải CẢ 3 hệ (trùng lề cố định Đảng) = giá trị normalize
  duy nhất; số trang VBQPPL 13 CỐ ĐỊNH vs hành chính/VBHN 13-14 vs Đảng 14; Đảng: tiêu đề ĐCSVN 15, số
  ký hiệu `Số 127-QĐ/TW` KHÔNG hai chấm (`-` trước loại, `/` trước CQ — ngược nhà nước), dấu sao (*),
  5 gạch `-----`, dòng 18-22pt Exactly.
- RUNBOOK §D +1 row route "soạn/kiểm thể thức" → reference; kernel KHÔNG đổi ruột (chỉ header version)
  ⇒ re-import không bắt buộc.
- NQ 351/2017 hệ cũ: không bị bãi bỏ minh thị (grep 0 hit trong 78/187) nhưng bị thay trên thực tế từ
  01/7/2025 — không dùng làm chuẩn kiểm; registry `hieuluc=can_kiem_tra` GIỮ (sửa cờ = data-op riêng).
- Bẫy phiên ghi nhận: anchor selftest phải là chuỗi 1 DÒNG — wrap văn bản giữa chuỗi làm r135 đỏ oan
  (2 lần đầu); HD05 in "TCVN 6909: 2001" CÓ khoảng trắng (khác NĐ30/187) — trích đúng từng nguồn.

# ★ v1.34.73 — PERF nạp lô: perf_hint trong DRY plan + GOTCHAS §10 + RUNBOOK §D (2026-07-19)

> Mổ xẻ "30 phút / 3 file" (journal đo ~260s/file apply): **chờ NLM settle mặc định ăn ≈NỬA thời gian
> mỗi ingest** (help --nlm-no-wait v1.34.33 đã ghi −~50%); phần còn lại = chuỗi GAS (upload b64→convert
> →organize, ~80–110s "công việc thật") + chạy TUẦN TỰ + overhead agent (DRY rời, readback --refresh
> nhiều lần) + sự cố dedup 399/05. Đường 3-file-3-phút: `--nlm-no-wait` ×3 SONG SONG + reconcile 1 lần.
> selftest 1091→1092 (r134 viết CÙNG LÚC implement — doc+hint patch, không pha đỏ đúng nghĩa; ghi thật).

- **`_ingest_perf_hint` PURE** (ingest_ops) + wire DRY plan `perf_hint`: nhắc đường nạp-lô nhanh NGAY
  nơi người vận hành đọc plan; đã dùng `--nlm-no-wait`/`--no-nlm-add` → im. KHÔNG đổi default
  (verify-then-link giữ — an toàn v1.34.56). _STUB_MAP +1 tên (bind-REBASE).
- **GOTCHAS §10 PERF nạp lô**: quy tắc lô ≥2 (song song + reconcile cuối + readback 1 lần, không
  --refresh giữa chừng) + giải đáp b64: **upload b64 qua webapp là BẮT BUỘC** (Apps Script doPost không
  nhận multipart binary, trần 35MB); file <1MB b64 không phải bottleneck (+33% ≈ <1s) — độ trễ ở Apps
  Script runtime + convert GDoc; file rất lớn → cân nhắc gws CLI (backlog). **RUNBOOK §D** +1 dòng
  "Nạp LÔ ≥2 file".

# ★ v1.34.72 — Vá crash `tl ingest-local -h` (help chứa `%` chưa escape) + guard format_help mọi lệnh (2026-07-19)

> Lỗi lộ khi data-op nạp thể thức (rà backlog THE_THUC): `tl ingest-local -h` CRASH. TDD r133 ×1;
> selftest 1090→1091. Kernel SKILL.md chỉ đổi header → re-import khi tiện.

- **Bug**: help của `--nlm-no-wait` (cli.py:322) chứa `−~50% thời gian`; argparse dùng %-formatting cho
  help → `% t` bị hiểu là format-spec `%t` → `ValueError: unsupported format character 't' at index 53`
  khi `print_help()`. Sửa `%` → `%%` (giữ nguyên hiển thị "−~50%").
- **Guard chống tái diễn** (r133): selftest quét MỌI subparser `format_help()` không ném — bắt lớp bug
  help-`%` cho mọi lệnh hiện tại lẫn tương lai (TL_SELFTEST_DEBUG in danh sách lệnh crash). Golden
  `parser_surface` regen chủ đích đúng 1 dòng (ingest-local — raw help đổi `%`→`%%`).

# ★ v1.34.71 — Profile TEMPLATES: "trình bày theo mẫu người dùng đưa" per-profile (2026-07-18)

> Kế hoạch `ke-hoach-profile-templates-2026-07-18.md` (grill 11 câu Q0–Q8 + Q2b/Q2c chốt cùng ngày;
> Phương án B của review thể-thức-văn-bản). TDD r132 ×5 negative-trước; selftest 1085→1090; gen 37→38.
> Kernel SKILL.md CHỈ đổi header → re-import khi tiện. Mục (4) THE_THUC_TRINH_BAY.md = DEFER backlog
> data-op (Q0 — phải verify nguyên văn NĐ 30/2020 qua corpus trước khi neo).

- **Marker `templates`** (Q1): list `{id, drive_id, name, scope, note, added_at}` trong
  `_meta/tra_luat_profile.json` — KHÔNG bump schema v1. ⚠ `_marker_body` là WHITELIST (đính chính grill):
  pass-through `templates` TƯỜNG MINH (r132a khóa — thiếu là mọi đường rewrite marker NUỐT field).
- **`profile-set-meta` +7 flags** (Q2c/Q3/Q5): `--template-add <id>` (kèm `--template-drive-id`; THAM
  CHIẾU — hợp lệ không-WARN = cây profile hoặc KHO CHUNG `_meta/templates` VBQPPL) | `--template-upload
  <file.docx>` (≤35MB, upload vào `_meta/templates/` profile qua `resolvefolder` find-or-create + action
  `upload` b64 sẵn có; id = slug tên file; trùng tên → `TEMPLATE_FILE_NAME_EXISTS` không ghi đè) |
  `--template-remove <id>`; kèm `--template-name/scope/note`. ĐÚNG 1 op/lần (`TEMPLATE_ONE_OP_ONLY`);
  probe BẮT BUỘC khi `--apply` (LIST-first 2 vị trí hợp lệ → `download` fallback; fail →
  `TEMPLATE_NOT_FOUND` fail-closed, KHÔNG cờ bypass); DRY chỉ lập plan (không resolvefolder — không tạo
  folder ngoài apply); journal step `template_upload` riêng.
- **Kho mẫu chung** (Q2b): folder `_meta/templates/` dưới metaFolder VBQPPL — **folder-là-danh-mục**
  (nguồn sự thật = LISTING, không marker vbqppl); profile dùng mẫu chung bằng `--template-add` DẪN CHIẾU
  CHỦ ĐÍCH từng mẫu, KHÔNG auto-inherit.
- **`profile-list --templates`** (Q6): read-only LIVE — liệt kho chung + entries marker từng profile
  (kho chưa dựng → note hướng dẫn, rc=0). **`profile-doctor --deep`** +2 hạng mục: `TEMPLATE_MISSING`
  (warn, probe 404) / `TEMPLATE_OUTSIDE_TREE` (info advisory Q2).
- **Khối Instruction `## trinh_bay_theo_mau`** (Q4, `generate_profile_load_block`): CHỈ hiện khi marker
  có templates (profile cũ block Y NGUYÊN); liệt kê mẫu + vế điều kiện "**CHỈ KHI <scope>**"; 4 mệnh
  lệnh: đọc khung `tl doc-text` / GIỮ NGUYÊN khung, chỉ điền nội dung / căn cứ verify NGUYÊN VĂN /
  dựng .docx bằng công cụ docx MÔI TRƯỜNG (tra-luat KHÔNG sinh docx). Thân session==project byte-equal giữ.
- **TDD r132 ×5** (marker pass-through; `_templates_apply_change`/`_template_id_norm` PURE + inject
  `now`; parser 7+1 flags bọc SystemExit; block gen conditional; `_template_findings` PURE) + 1 ca gen.
  Wiring `_STUB_MAP` +4 tên (bẫy bind-REBASE: helper mới thiếu bảng → NameError runtime, r90 bắt).
  Golden `parser_surface` regen CHỦ ĐÍCH đúng 2 lệnh; COMMANDS.md 2 row (CRLF) + RUNBOOK §D +1 dòng.
- **Bàn giao**: live-smoke ĐỌC/DRY phiên này (không ghi marker); smoke GHI thật ở phiên sau deploy;
  seed kho chung + THE_THUC = backlog.
- **Smoke DRY lộ gap → vá trong-release** (`_base_meta_folder_id`): block `profiles.vbqppl` KHÔNG có
  `metaFolderId` và root nền nằm trong block (không top-level) → resolver kho chung: config-first
  (block → top-level) → LIST root nền tìm `_meta` (khuôn `_marker_read`); root nền HIỆN CHƯA CÓ `_meta`
  → note phân biệt rõ "kho chung CHƯA DỰNG (tạo `_meta/templates` trong root nền)" ≠ "config hỏng".
  Smoke sống: 15 profile marker đọc OK (templates đều [] đúng kỳ vọng); DRY --template-add id-giả →
  probe exists=false + warning "PROBE_FAIL — --apply sẽ TỪ CHỐI" + KHÔNG ghi (fail-closed Q5 ✓).

# ★ v1.34.70 — Sửa help zip-ingest lỗi-thời + nhãn TÀI LIỆU LỊCH SỬ 2 references (2026-07-18)

> Hai fix doc. TDD r131 ×2; selftest 1083→1085. SKILL.md chỉ đổi header version ⇒ re-import KHÔNG bắt buộc
> (khi tiện).

- **Help `ingest-zip` + `profile-ingest-zip`** (`tl_core/command_registry.py` GENERATED_SPECS): bỏ câu
  "apply chưa bật ở pha an toàn" — SAI từ v1.34.45 (zip_ingest có nhánh `child_apply` chạy thật, journal
  `ingest_zip_apply.v1`, meta supports_dry_run/confirm đầy đủ). Help mới: "DRY mặc định … --apply
  --confirm yes chạy thật từng member". Help thuộc parser_surface → golden regen CHỦ ĐÍCH
  (`TL_WRITE_PARSER_SURFACE=1`), đúng 2 dòng help đổi.
- **Nhãn TÀI LIỆU LỊCH SỬ** đầu 2 file: `references/REGEN2_PROFILE_SCOPE_V1.19.5.md` (nhắc server
  2.21.2i) + `references/MULTI_CORPUS_PROFILE_V1_18.md` (nhắc webapp 2.21.2g) — blockquote trỏ contract
  HIỆN HÀNH `references/API_CONTRACT.md` (2.21.2m) + RUNBOOK; nội dung lịch sử GIỮ NGUYÊN VĂN.
- **TDD r131**: (a) help 2 lệnh zip hết câu lỗi-thời + có "DRY"/"--apply --confirm yes" + parser thật có
  cờ tương ứng; (b) nhãn nằm trong 700 ký tự đầu, trỏ API_CONTRACT 2.21.2m, file giữ LF.

# ★ v1.34.69 — Trim dead-weight khỏi bundle deploy: Code.2.21.2k.gs (0-ref) + changelog_archive (2026-07-18)

> Best-practice review (rà kho shanraisshan vừa clone) — P1 "0-ref dead weight". TDD r130 ×1; selftest
> 1082→1083. SKILL.md đổi (header + annotate 1 dòng) ⇒ **RE-IMPORT CAPABILITIES BẮT BUỘC**.

- **Loại 2 file khỏi bundle** (~632KB, runtime agent claude.ai không cần): `references/Code.2.21.2k.gs`
  193KB (GAS bản cũ, **0 reference** toàn skill — thêm vào `_RELEASE_EXCLUDE_NAMES_ANYWHERE`) +
  `references/changelog_archive/` 439KB (CHANGELOG cũ ≤v1.33.53, deep-history — thêm `changelog_archive`
  vào `_RELEASE_EXCLUDE_DIRS`). **GIỮ** `Code.2.21.2m.gs` (current, 6 ref) + `Code.2.21.2l.gs` (9 ref).
- **SKILL.md:302** annotate con trỏ changelog_archive = "DEV-ONLY, KHÔNG trong bundle deploy" — bundle
  deploy KHÔNG có pointer chết; dev-side link-check (`links_ok`) vẫn xanh vì cây dev còn thư mục
  (`links_checked` giữ 14, token `references/changelog_archive/` giữ nguyên).
- **TDD r130** (khuôn r129/r59 temp-dir): `_release_should_include` loại 2.21.2k + changelog_archive/,
  GIỮ 2.21.2m/2.21.2l/API_CONTRACT + membership 2 hằng exclude. Golden `workflow_audit` regen CHỦ ĐÍCH
  đúng 1 dòng (`size_bytes` 46.946→46.987B do annotate; vẫn WARN-clear <47KB). Bundle ×2 same-SHA
  (byte-match) **171 file** (173→171, −2); nội dung 5.785.185→5.154.925B (−630KB), zip ~5.21MB.

# ★ v1.34.68 — Kho tham chiếu Claude Code (dev-only) + generator instruction tier CORE/FULL (2026-07-18)

> Kế hoạch `ke-hoach-instruction-refactor-va-kho-tham-chieu-2026-07-18.md` (grill Q1–Q6 chốt 2026-07-18),
> MỘT release 2 nhánh. TDD r129 ×6 negative-trước; selftest 1076→1082; gen_instructions selftest 29→37.
> Kernel SKILL.md CHỈ đổi header version — re-import Capabilities KHÔNG bắt buộc.

- **Nhánh I — Kho tham chiếu Claude Code (dev-only local, Q1/Q2)**: clone `--depth 1`
  `shanraisshan/claude-code-best-practice` tại skill-root `claude-code-best-practice/` (132MB, 454 file —
  CHỈ máy canonical); `.gitignore` + `_RELEASE_EXCLUDE_DIRS` +`"claude-code-best-practice"`
  (release.py:325 — r129 khoá loại MỌI CẤP, đỏ-trước); khối `## Kho tham chiếu Claude Code` vào
  `CLAUDE.md` bọc `<important if="phát triển Claude Code artifacts">` (dev-context, CLAUDE.md vốn bị
  loại bundle) + con trỏ 1 dòng đầu `references/DEV_TOOLING_GUIDE.md`. KHÔNG đụng kernel.
- **Nhánh II — `gen_instructions.py` tier `--tier core|full` (①–⑥, Q3–Q5)**:
  - ① **MẶC ĐỊNH = CORE (breaking CÓ CHỦ ĐÍCH)**: `tl instructions --target project` không cờ nay ra
    CORE **9.158 ký tự** (trước 15.126 — cắt 39%); 2 khối dev `script_reuse_va_quyet_dinh_viet_tool`
    (3.435 ký tự) + `van_ban_lon_va_pdf_scan` (2.712) chuyển tier FULL, CORE thay bằng con trỏ
    `## chi_khi_dev_release_ocr` ("**CHỈ KHI** nạp/ghi, đóng gói/release, live/deploy, OCR/chunk: theo
    `SKILL.md` + `references/RUNBOOK.md`/`DEV_TOOLING_GUIDE.md`; KHÔNG viết tool mới khi chưa qua
    `tl tool-inventory` + `tl route-task`; dry-run + verify/readback"). Bản cũ = `--tier full`
    (14.328 ký tự). Bootstrap CORE rút gọn 1 đoạn (giữ nguyên nghĩa 5 bước); FULL giữ bản đánh số.
  - ② **Khử trùng lặp**: litany release/live/deploy trong `script_reuse` LẶP 2 lần (steps 4–7 + đoạn
    kết) → đoạn kết còn 1 câu trỏ bước 4–7 (FULL 15.126→14.328). Cặp khối văn phong + cấu trúc trả lời
    Project↔NLM (near-identical) gộp 1 NGUỒN dùng chung (`_STYLE_*`/`_ANSWER_PARTS` +
    `_language_style_block`/`_answer_structure_block`) — output 2 phía GIỮ NGUYÊN BYTE.
  - ③ Cơ chế điều kiện trong prompt = tiền tố "**CHỈ KHI …:**" (Q4); `<important if>` CHỈ ở CLAUDE.md.
  - ④ **Size-guard CORE** `_core_size_findings` (khuôn `_kernel_size_findings`) đo **KÝ TỰ** (đơn vị đo
    instruction của kế hoạch; ô Instruction claude.ai đếm ký tự): WARN >9.216 advisory / FAIL >12.288
    (selftest đỏ). Hiện trạng CORE 9.158 = WARN-clear, đệm 58 ký tự.
  - ⑤ **audit() tách tier**: `REQUIRED_PROJECT` = 27 khóa CORE (guard tra-cứu + write-safety);
    19 khóa dev/release/live/deploy/OCR dời sang `_REQUIRED_FULL_EXTRA` → `REQUIRED_FULL` (46 khóa,
    target audit `"full"`); wrapper `tl instructions`/`tl instruction-audit` +`--tier`, tier=full ⇒
    audit theo REQUIRED_FULL. `prompt_generation_contract` GIỮ CORE, cập nhật tài liệu `--tier`.
  - ⑥ **NLM prompt GIỮ NGUYÊN BYTE** (drift-lock r129 pin sha256 `8d576ecf…` baseline v1.34.67 +
    `tier_nlm_unaffected_by_tier`); KHÔNG rút `chat_luong_truy_van_notebooklm`/`mau_cau_khi_khong_du_can_cu`.
- **TDD/wiring**: r129 ×6 (exclude clone; tier core default; tier full gates + litany-1-lần + negative
  CORE-fails-full-audit; size-guard biên 9K/12K; NLM sha256 pin; CLI --tier wired + audit full 46 khóa);
  5 ca selftest gen cũ đổi sang `tier="full"`; bẫy mới ghi nhận: `parse_args` cờ chưa tồn tại ném
  `SystemExit` (BaseException — `_t110` không bắt) → test CLI mới phải bọc SystemExit. Golden
  `parser_surface.json` regen CHỦ ĐÍCH đúng 2 lệnh (`instructions`/`instruction-audit` +--tier);
  `references/COMMANDS.md` row instructions cập nhật (CRLF giữ). **Re-paste CORE Project Instruction
  BẮT BUỘC** (`tl instructions --target project` → dán ô Instruction Claude Project).

# ★ v1.34.67 — G1b KERNEL-DIET: trích 3 khối nguyên văn → references/KERNEL_APPENDIX.md (2026-07-18)

> §11 G1b kế hoạch `ke-hoach-guard-va-boc-tl-core-2026-07-18.md` (user duyệt riêng). Kernel ĐỔI RUỘT ⇒
> **RE-IMPORT CAPABILITIES BẮT BUỘC**. TDD r128 ×2 negative-trước; selftest 1074→1076.

- **Kernel 49.145B → 46.946B** (net −2.199B, đúng dải 2–4KB §11; đệm 1.182B tới WARN 47K + 2.206B tới
  FAIL 48K — `size_warn` G1a tắt, hết cảnh báo thường trực). Nếp Pha F: kernel = bất biến + con trỏ,
  nội dung chuyển **NGUYÊN VĂN** ("đã chuyển khỏi kernel — nội dung không đổi").
- **`references/KERNEL_APPENDIX.md` MỚI 4.823B — hiệu lực như kernel**, 3 khối trích nguyên văn:
  **§A** bảng COWORK route tải-về (artifact public/curl + ⛔ bẫy NPM-GLIBC gws `GLIBC_2.39 not found`);
  **§B** chi tiết COWORK TIMEOUT 45s (nlm-install --resume từng-bước, uv/tarball, no-nohup
  bwrap --unshare-pid, temp $HOME); **§C** sharding topology chi tiết v1.34.49 (declared+observed 1
  resolver, TOPOLOGY_CONFIG_CONFLICT fail-closed, capacity, failover-trong-run, push-overflow, recovery
  row_kind). Kernel GIỮ mệnh lệnh sống còn dạng tóm: khối BƯỚC 0 curl nguyên vẹn; `⛔ KHÔNG npm`;
  45s tách-bước + `--resume` tới rc=0; sharding bất biến (preflight, tin nlm-get LIVE, nlm-cross,
  KHÔNG notebook_create) + con trỏ §A/§B/§C; DANH MỤC REFERENCES +1 dòng.
- **Drift-lock r128** (khuôn r127 pointer-đích 2 chiều): appendix chứa anchor đặc trưng từng khối
  (`GLIBC_2.39 not found`/`bwrap --unshare-pid`/`TOPOLOGY_CONFIG_CONFLICT`) + kernel KHÔNG còn các
  anchor đó (chống copy-đôi/trích-nửa-vời) + kernel có con trỏ + bất biến tóm còn nguyên + links-check
  xanh + LF; r128 pin kernel ≤47K/size_warn=False. **r127 cập nhật CÓ CHỦ ĐÍCH**: pin hiện-trạng đổi
  TRUE→FALSE (lịch sử ghi trong comment test). Golden `workflow_audit` regen chủ đích (size_bytes/
  size_warn/links_checked). Bundle 172→173 (<200 ✓).

# ★ v1.34.66 — G1a WARN-kernel 47KB + G2 references/GOTCHAS.md (2026-07-18)

> §11 kế hoạch `ke-hoach-guard-va-boc-tl-core-2026-07-18.md` — 2 mục user duyệt ghép 1 release
> dev-tối-ưu skill. TDD r127 ×3 negative-trước; selftest 1071→1074. Python-only (GAS 2.21.2m).

- **G1a — WARN kernel >47KB** (kernel 49.145/49.152B = trần SÁT NHẤT toàn hệ, đệm 7B; gate cũ CHỈ FAIL
  ≤48K không WARN): helper PURE `_kernel_size_findings` (workflow.py, khuôn WARN/FAIL của §3) — WARN
  advisory KHÔNG vào `out["warnings"]` (strict không fail vì đệm), FAIL >48K GIỮ NGUYÊN ngữ nghĩa;
  kernel block audit dùng helper (+`size_warn_limit`/`size_warn`). **Hiện trạng `size_warn=TRUE` NGAY
  từ release này — ĐÚNG CHỦ ĐÍCH** (báo sớm cần kernel-diet G1b, việc riêng chờ duyệt). Stub I11 +
  r127 pin biên 47K/47K+1/48K/48K+1.
- **G2 — `references/GOTCHAS.md` 7.715B** (5–8KB đúng ước §11): gom bẫy ĐÃ TRẢ GIÁ nhóm 9 CHỦ ĐỀ —
  trần mount/size (343KB, kernel 48K, bundle 200); I11/stub/bind (hằng re-export, no-sweep R2, drift
  2 lớp __tl_stub__ + getsource); nghi thức release (manifest `--out` dry, golden nhúng size, LF vs
  CRLF COMMANDS.md, commit -F, gate rc-thật); lazy-creds; journal-HOME + `.tl_state` repo-relative +
  fake-home 2 tầng; ghi registry (reg_bulk rỗng bị bỏ qua → reg_clear, readback âm tính giả → re-check
  authoritative, claim=ESTIMATE, key `gdoc_id`/`id`); dedup data-op (md5 mislabel, picker ngược,
  docx binary, sohieu-năm, gốc+convert không trùng); Windows console/heredoc (cp1258/PYTHONUTF8,
  chr(92), path tuyệt đối, junction C:\qh); NLM (cookie DBSC ~1h, fallback đọc/ghi/audit-belief,
  FILTER_REQUIRED). **Con trỏ đặt trong RUNBOOK.md (+2 dòng blockquote) — kernel 0 byte** (kernel đã
  trỏ RUNBOOK sẵn); bundle 171→172 (<200 guard ✓). Drift-lock r127 kiểu bài-học-handoff: kiểm POINTER
  ĐÍCH (RUNBOOK chứa đường dẫn + GOTCHAS chứa đủ anchor bẫy + LF).

# ★ v1.34.65 — ĐỢT B tách tl_core/nlm_admin_ops.py: ranh giới GHI/ĐỌC (2026-07-18)

> Kế hoạch `D:\Quốc hội\ke-hoach-guard-va-boc-tl-core-2026-07-18.md` §5 (ĐÓNG TRỌN kế hoạch 2 đợt).
> TDD r126 ×1 negative-trước (18-tên wiring composite); selftest 1070→1071. Python-only (GAS 2.21.2m).

- **Tách `tl_core/nlm_admin_ops.py` §5 — MOVE NGUYÊN VĂN 11 zone** (nlm_ops.py 208.652B/61% trần →
  **94.843B/28%**; nlm_admin_ops.py 116.354B/34%): **RANH GIỚI MODULE = RANH GIỚI QUYỀN GHI/ĐỌC** —
  7 cmd GHI/audit (`nlm-add/nlm-migrate/nlm-reconcile/nlm-source-remove/push-overflow/overflow-resolve/
  nlm-audit-physical`) + 11 helper (`_nlm_add_deferred/_nlm_add_doc_type/_shard_row_kind/_migrate_plan/
  _nlm_reconcile_plan/_physical_audit_classify/_migrate_resume_write/_nlm_post_add_dup_check/
  _nlm_source_drive_id/_nlm_source_list_cached/_nlm_list_stale_read`). Đường ĐỌC + fallback E1 Ở LẠI
  nlm_ops; plan-helper NGOÀI danh-sách-tên Ở LẠI theo R2 — không sweep (`_nlm_source_remove_plan/
  _source_remove_delete_verdict/_nlm_dedup_gate/_nlm_add_capacity_error`); HẰNG Ở LẠI nlm_ops
  (`_ROW_KIND_PROTECTED/NLM_BATCH_LINKS_THRESHOLD/_NLM_COOKIE_*` — re-export tl giữ nguồn cũ, bẫy I11).
  `COMMAND_META` Y NGUYÊN đủ 12 field ×7 lệnh (kể cả `nlm_fallback` §5: add/migrate=defer, reconcile/
  audit=unverified, source-remove=none; module-hint giữ 'nlm_ops' — chỉ dùng cho det_json scan, False cả 7).
- **BẰNG CHỨNG MOVE THUẦN (§6.5/R6):** selftest 1071/1071; golden diff DUY NHẤT ĐÚNG KẾ HOẠCH =
  `workflow_audit.py_size.files_scanned` 63→64 (+1 file mới — regen CÓ CHỦ ĐÍCH 1 dòng); 18 golden khác
  0-DIFF; charact §6.1 **31/31 cmd BYTE-MATCH TRỌN** post-vs-pre (`.tl_state/charact_pre_B`, capture tươi
  cùng phiên). Sau 2 đợt: **mọi .py runtime < WARN 280KB** (max còn lại: ingest_ops 182.775B) — nghiệm thu §7.
- **SMOKE B (Q5/§6.6) ĐẠT TRỌN — KHÔNG ghi sống:** [dead-path fake-home] audit-physical (GAS sống, NLM
  chết) → UNVERIFIED_NLM_STATE ×2 notebook cache stale, topology CLEAN 0/0/0/0, rc=0 read-only; migrate
  `--apply --confirm yes --name-contains CPTPP` → `DEFERRED_NLM_OFFLINE` deferred{repoint:0,add_api:0}
  (KHÔNG ghi by-design E2) + resume-artifact `migrate_resume.v1` local, rc=0; guard `FILTER_REQUIRED`
  fail-closed chứng kiến; nlm-add (GAS+NLM đều chết — 0 ghi tuyệt đối) → defer, note 'registry CHƯA có
  dòng' đúng, rc=0. [1 vòng đọc-sống DRY] cookie SỐNG: nlm-list **293 nguồn LIVE tươi** + audit vật lý
  **CLEAN 0/0/0/0 VERIFIED** (0 UNVERIFIED) — khớp trạng thái corpus đã biết.
- **Wiring cập nhật CÓ CHỦ ĐÍCH (§6.2/R3):** `r71_nlm_ops_module_wired` trim 7 tên (residency sang r126);
  `r126_nlm_admin_ops_wiring_moved_18_names` pin residency + chiều-ngược STAY-READ + hằng-ở-lại +
  meta snapshot + lazy y nguyên (add/reconcile/push-overflow/overflow-resolve lazy; migrate/source-remove/
  audit không) + parser resolve (kể cả `nlm-add` KHÔNG-generated); 2 tham chiếu lớp-getsource đổi nguồn
  theo (bài học Đợt A — quét TRƯỚC move bắt đủ: r69 `_no69.cmd_nlm_add` → alias `_na69` mới [giữ `_no69`
  cho r71 đường ĐỌC], r83 `_no83._nlm_add_doc_type` ×4 → import đổi module); `r81` tự thích nghi (0 sửa).

# ★ v1.34.64 — ĐỢT A guard trần-mount + tách tl_core/source_ops.py (2026-07-18)

> Kế hoạch `D:\Quốc hội\ke-hoach-guard-va-boc-tl-core-2026-07-18.md` §3+§4 (grill Q0–Q7 chốt 2026-07-18;
> Đợt 0 harness 2026-07-18: baseline KHÔNG drift, charact 31/31 cmd ×2 byte-hệt, probe bind-REBASE 3/3
> byte-identical). TDD r125 ×3 negative-trước; selftest 1067→1070. Python-only (GAS giữ 2.21.2m).

- **Guard TRẦN MOUNT §3** (lớp sự cố #5 — tl.py từng CẮT CỤT >~343KB; self-heal không cứu cắt cụt):
  `_py_size_findings` PURE trong workflow.py — **WARN >280KB** (đệm ~60KB, advisory KHÔNG merge vào
  `warnings` theo tiền lệ registry-warnings → `--strict` không fail vì đệm) / **FAIL --strict >320KB**
  (chặn release TRƯỚC vách); scope mọi `.py` runtime bundle (scripts/ + tl_core/ + _fallback/ — 63 file);
  **WAIVER `tl_selftest.py`** (936KB — không bước runbook nào import trên Cowork; hỏng → fail ỒN ÀO).
  Sống ở `workflow-audit` (mục `py_size`, tiền lệ kernel_size ≤48KB) + case selftest r125. Hiện trạng
  khi thêm: mọi file dưới WARN → guard XANH ngay, không nợ kỹ thuật giả.
- **Tách `tl_core/source_ops.py` §4 — MOVE NGUYÊN VĂN** (ingest_ops.py 237.603B/69% trần → **182.775B**;
  source_ops.py 56.801B): 6 cmd `register/recat/source-rename/source-delete/source-update-corpus/
  shared-source-fix` + 9 helper riêng-cụm (`_register_clear/_register_bulk_missing/_register_target_exists/
  _reg_row_present/_source_delete_plan/_source_rename_plan/_source_update_corpus_plan/
  _shared_source_fix_plan/_shared_source_id_groups`) + 2 hằng `_REG_CLEAR_FREE_COLS/_REG_CLEAR_PROTECTED`
  (re-export TRỰC TIẾP tl.py đổi nguồn `_tl_ingest_ops`→`_tl_source_ops` CÙNG commit — bẫy I11: hằng
  KHÔNG vào _STUB_MAP). Khuôn I5 (docstring nguồn gốc + stdlib noqa + bind REBASE); helper dùng chung
  2 phía Ở LẠI ingest_ops; WRITE-INFRA đa-module ở tl.py. Wiring: `_tl_core_import("source_ops")` + key
  `_STUB_MAP` CHUYỂN 15 tên + bind tuple.
- **BẰNG CHỨNG MOVE THUẦN (§6.5 — R6):** golden **19/19 PASS 0-DIFF, 0 file đổi, KHÔNG --write** ở pha
  move; charact §6.1 **31/31 cmd BYTE-MATCH TRỌN** post-move vs pre-move (`.tl_state/charact_pre_A`,
  capture tươi cùng phiên); live-smoke offline: source-update-corpus DRY row thật (plan đúng, không ghi)
  + shared-source-fix report thật + register guard chặn id giả P0-1 rc=2. Golden `workflow_audit` regen
  CÓ CHỦ ĐÍCH riêng pha guard (đúng 1 file, diff = khối `py_size`).
- **Wiring test cập nhật CÓ CHỦ ĐÍCH (§6.2/R3):** `r75_ingest_ops_module_wired` trim 11 tên (residency
  chuyển sang r125); `r125_source_ops_wiring_moved_15_names` pin residency mới + KHÔNG dual-definition +
  COMMAND_META snapshot ĐỦ 12 field/6 lệnh Y NGUYÊN (kể cả `register` KHÔNG-generated, `source-delete`
  supports_dry_run=False) + `_CREDS_LAZY_CMDS` membership y nguyên + parser resolve nguyên vẹn;
  1 tham chiếu residency `inspect.getsource(_io5.cmd_recat)` (test recat 1.23.6) đổi nguồn theo;
  `r81` stub-farm TỰ thích nghi (không sửa); `r99` giữ nguyên (helper ở lại).
- Bài học Đợt A: quét drift-check theo `__tl_stub__` tuple là chưa đủ — còn lớp tham chiếu
  `inspect.getsource(<module>.<fn>)` trỏ thẳng module nguồn (1 ca recat); trailing-blank cuối file mới
  trim về 1 newline (whitespace-EOF, không tính đổi nguyên văn).

# ★ v1.34.63 — A2 `doc-compare` + B1 `dedup-corpus`: dedup TRỤC NỘI DUNG (2026-07-18)

> Kế hoạch `D:\Quốc hội\ke-hoach-dedup-corpus-B1-2026-07-18.md` (grill chốt, ADR-1..7 + ADR-A2-1..4) —
> đóng nỗi đau data-op 2026-07-16 (dedup sweep phải viết ~10 script tay). TDD r124 ×19 negative-input
> trước; selftest 1048→1067. Python-only (GAS giữ 2.21.2m).

- **Module identity DÙNG CHUNG `tl_core/doc_identity.py` (ADR-A2-1/A2-2)** — 1 nguồn sự thật, B1 gọi CÙNG
  helper qua stub tl (drift-lock r124 cấm copy): `_doc_norm` = NFC + `_strip_font_runs` + lowercase + gộp
  whitespace, **GIỮ dấu + dấu câu**; `_content_hash` = sha256 (rỗng → '' — không sha-rỗng giả identical);
  `_bow_tokens`/`_bow_jaccard` (GIỮ dấu, bỏ dấu câu; rỗng → 0.0); `_compare_signals` → verdict
  IDENTICAL (md5 bytes | content-hash, đòi giá trị không-rỗng) / NEAR (jaccard ≥ T=0.95 `--near-threshold`)
  / DIFFERENT + `sohieu_differs` (raw signal — A2 KHÔNG kết luận tên đúng).
- **`tl doc-compare <a> <b>` (A2, ADR-A2-3/A2-4)** — CLI mỏng: input auto-detect drive_id | sohieu | name |
  **local-path** (local×local = pre-ingest dedup, KHÔNG cần manifest/boot); đọc text `_doc_text_any` (A1);
  NLM-độc-lập; rc=0 mọi verdict, rc=2 chỉ khi không resolve/không đọc được (fail-closed). Read-only,
  `nlm_fallback=corpus_read`, lazy-creds (khuôn doc-text — CI offline không gãy).
- **`tl dedup-corpus` (B1, ADR-1..7)** — dedup TRỤC NỘI DUNG, COEXIST `dedup-plan` (trục chủ đề):
  - Candidate-gen FREE md5-group + sohieu-group; **md5-first perf (ADR-7)**: dòng md5-unique KHÔNG BAO GIỜ
    đọc text; md5-group cùng-sohieu chốt DUP_EXACT bằng BYTES (0 lần doc-text); sohieu-group so content
    qua ĐẠI DIỆN cụm-md5; cache `.tl_state/content_hash_<did>.json` (tin CHỈ khi md5 khớp).
  - Classifier PURE `_dedup_corpus_classify` 7 loại, ưu tiên: CROSS_PROFILE_DUAL_REG (ADR-6, `--all-profiles`
    flag-only — dual-reg chủ đích) > PHYSICAL_DUP (ADR-4 lằn ranh: ≥2 on-NLM-live → đẩy `nlm-audit-physical`/
    `nlm-source-remove`, B1 KHÔNG tự đụng — bất biến #16) > JUNK (SMOKE_TEST/KhongPhaiVanBan) >
    MISLABEL_RESOLVED/_UNRESOLVED (ADR-3: content-verify header `_classify_doc_header` với filename RỖNG —
    ruột văn bản phân xử, khớp DUY NHẤT 1 → resolved, 0/>1/không đọc được → fail-closed) > DUP_EXACT
    (ADR-2: **CÙNG TYPE** — docx-gốc + GDoc-convert cùng content-hash = KHÔNG trùng → `legit_convert_pairs`,
    định nghĩa user 2026-07-16). Cặp không-exact Jaccard ≥ T → NEAR_DUP_REVIEW kèm jaccard + Δ số-Điều/
    độ-dài, **KHÔNG BAO GIỜ auto** (bất biến #6 gốc-vs-sửa-đổi).
  - Canonical-picker RIÊNG (ADR-1/ADR-4 — KHÔNG kế thừa bug picker-chọn-ngược của dedup-plan): on-NLM-live+
    corpus → corpus → tên chuẩn (phạt `_v2`/tên thô) → drive_id sort tất định.
  - Apply (ADR-5): `--apply --confirm yes`; mặc định `--mode corpus-false` ỦY QUYỀN `source-update-corpus
    <id> false` TỪNG id (tái dùng guard shared-source + gỡ NLM + journal-undo); `--mode delete` OPT-IN ủy
    quyền `source-delete` (trash Drive + reg row) cho file Drive dư/JUNK; guards fail-closed đè MỌI mode;
    `--only-md5`/`--limit` duyệt từng bước (ADR-7); dòng đã corpus=false bỏ qua (idempotent); journal
    dedup-corpus run_end = verdict cuối; `--all-profiles` + `--apply` → rc=2 (flag-only).
- **Wiring**: GENERATED_SPECS + COMMAND_META (`doc-compare` low/read-only/corpus_read; `dedup-corpus`
  high/confirm/dry-run/`drive_registry_nlm`/nlm_fallback=none) + contract `dedup_corpus` đủ 8 field +
  `_CONTRACT_REQUIRED` +dedup-corpus (drift-lock r65 cập nhật CÓ CHỦ ĐÍCH) + stub I11 (module mới
  `doc_identity` vào `_STUB_MAP`/bind; hằng `_DEDUP_JUNK_NAME_RE` re-export tl) + `_CREDS_LAZY_CMDS`
  +2 lệnh (bài học CI v1.34.60) + parser-surface regen (+2 lệnh, có chủ đích) + golden regen.
- **SKILL.md kernel**: bảng lệnh Registry & corpus `dedup-plan` → `dedup-plan/corpus` (49145B ≤ 48K limit
  49152B) → **đổi kernel ⇒ user re-import Capabilities khi tiện**; COMMANDS.md +2 dòng lệnh đầy đủ.

# ★ v1.34.62 — vá `registry_deferred=false` OAN: re-check authoritative reg_get_bulk (2026-07-17)

> Live-smoke dead-path 2026-07-17 bắt: `nlm-add` deferred ghi registry THÀNH CÔNG (reg-query --live thấy
> `nlm_status=deferred` ngay sau) nhưng envelope báo `registry_deferred=false` — readback field-level trong
> `_verified_reg_write` (reg_get refresh=true + retry) ÂM TÍNH GIẢ (GAS cache che). TDD r123 ×4
> negative-input trước; selftest 1044→1048. Python-only.

- **Vá `_nlm_add_deferred`**: `_journaled_reg_write` verified=False → RE-CHECK AUTHORITATIVE qua
  `reg_get_bulk` (cùng khuôn verify CUỐI của nlm-migrate/claim-commit) TRƯỚC khi kết luận: row thấy đúng
  `nlm_status=deferred` + nb → `registry_deferred=true` + note "AUTHORITATIVE (readback âm tính giả)";
  authoritative CŨNG không thấy → GIỮ false + note hướng kiểm `reg-query --live` (không báo láo cả 2 chiều);
  re-check RAISE → nuốt, giữ false. **Journal run_end nay phản ánh verdict CUỐI** (sau re-check) thay vì
  verdict readback — undo/resume đọc đúng sự thật.
- **Test r123 ×4**: auth-confirms-false giữ false + note "CHƯA xác minh" + run_end ok=False (NEGATIVE trước);
  auth-error giữ false không nổ lệnh; recheck-flips-true + note AUTHORITATIVE + run_end ok=True; verified=True
  bỏ re-check (0 call reg_get_bulk). Đường verified=True + hành vi r121 giữ nguyên byte.

# ★ v1.34.61 — NLM-DEATH RESILIENCE Release 2: E2 unverified-continue + defer/resume-artifact (2026-07-17)

> Release 2/2 CHỐT kế hoạch grill-with-docs (`D:\Quốc hội\ke-hoach-nlm-fallback-E1-E3-2026-07-16.md`,
> ADR-3): audit/DRY → UNVERIFIED-CONTINUE (cờ, không xử theo belief); đường GHI-cần-vật-lý → DEFER +
> resume-artifact `--from-plan`. TDD r122 ×10 negative-input trước; selftest 1034→1044. Python-only.

- **[E2 audit] `nlm-audit-physical`**: notebook list fail + NLM hard-dead → dùng cache stale BẤT KỂ TTL
  (`_nlm_list_stale_read`) — audit CHẠY TIẾP; verdict fallback tính 1 lần/loop (banner không spam); BẤT KỲ
  notebook stale → gắn `unverified_nlm_state` TOÀN BỘ finding (bảo thủ: 1 phần scope stale = cả bức tranh
  không chắc) + envelope `nlm_status:offline/fallback:unverified/stale_notebooks/source`; rc GIỮ 0/1.
  Không cache → notebook ra khỏi scope như cũ (pointer trỏ nó = unverified_scope advisory — không bịa
  tầng vật lý); `--no-fallback` → NO_NOTEBOOK_LISTED rc=2 như cũ.
- **[E2 migrate] `nlm-migrate`**: listing đích fail + hard-dead → (i) có cache stale: plan CHẠY TIẾP cờ
  `UNVERIFIED_NLM_STATE` — DRY trả plan flagged; `--apply` KHÔNG ghi registry/API-add trên belief, CHỈ
  BATCH_LINKS (in link dán tay không cần NLM — reconcile bắt trùng sau nếu stale lệch) + resume-artifact;
  (ii) không cache + `--apply`: `DEFERRED_NLM_OFFLINE` + resume-artifact, rc=0; (iii) không cache + DRY:
  LIVE_SOURCE_LIST_FAILED rc=2 (không ground truth nào). **Resume-artifact `.tl_state/migrate_resume_
  <to>.json`** (`_migrate_resume_write`, schema migrate_resume.v1) = THAM SỐ (to/filter/from/api_add/limit)
  — KHÁC A3 reconcile (plan-rows TTL 15'): plan LUÔN re-tạo TƯƠI lúc resume nên KHÔNG TTL. **`--from-plan
  [path|auto]`** nạp tham số rồi đi đường thường (fresh listing → re-plan → apply = chạy nốt repoint/verify);
  `auto` cần `--to`; artifact/CLI `--to` lệch → PLAN_MISMATCH. `--to` hết required=True ở parser (nhường
  from-plan) + guard TO_REQUIRED tường minh (không rơi về base mặc định).
- **[E2 reconcile] `nlm-reconcile`**: `--apply` + hard-dead → `DEFERRED_NLM_OFFLINE` rc=0 (KHÔNG ghi trên
  belief — physical-first), trỏ plan-artifact A3 (path/tuổi/fresh≤15') cho `--apply --from-plan`; DRY +
  dead GIỮ rc=2 (reconcile là VERIFY-TOOL — unverified-continue thuộc audit, không thuộc đây);
  `--no-fallback` giữ rc=2.
- Meta: `nlm-audit-physical`/`nlm-reconcile` nlm_fallback="unverified", `nlm-migrate`="defer" (đúng phân
  loại §2.2 kế hoạch); +`--no-fallback` cho cả 3 lệnh.
- **Test r122 ×10** (offline, fake nlm_cli/gas): wiring meta+from-plan parse; audit unverified flag +
  negative no-fallback/no-cache; migrate defer-artifact (KHÔNG upsert/claim/add) + no-fallback + BATCH_LINKS
  khi dead + DRY-stale-unverified (repoint 1/add 2 từ stale) + from-plan resume THẬT (writer thật temp-dir,
  artifact schema, repoint verify reg_get_bulk); reconcile apply-defer (GAS 0 call) + DRY/no-fallback rc=2.
- Docs: SKILL.md bất biến 17 mở rộng E2 (nén PHÁT HÀNH & NHÁNH + module-history giữ ≤48KB — 49138B)
  ⚠ **kernel đổi → user RE-IMPORT Capabilities**; COMMANDS.md 3 lệnh; parser_surface regen.

# ★ v1.34.60 — NLM-DEATH RESILIENCE Release 1: A1 doc-text + resolver fallback + E1 đọc + E3 đẩy (2026-07-16)

> Release 1/2 kế hoạch grill-with-docs (`D:\Quốc hội\ke-hoach-nlm-fallback-E1-E3-2026-07-16.md`, 7 ADR):
> *"NLM chết → KHÔNG dừng, fallback bằng văn bản TƯƠNG ỨNG trong corpus"*. TDD r121 ×17 negative-input
> trước; selftest 1017→1034. Python-only (GAS giữ 2.21.2m). Release 2 (E2 audit/migrate defer) = v1.34.61.

- **[A1] lệnh MỚI `tl doc-text <fileId> [--dieu N|--out|--max|--refresh|--json]`** — MỘT đường đọc text mọi
  định dạng (GENERATED_SPECS + meta + stub I11 + golden `doc_text_cache_fixture` offline): GDoc→export cũ;
  **.docx→download+unzip `word/document.xml` (text THẬT)**; .pdf→pdftotext; cache `extract_<id>.txt` chung
  khoá extract. **Footgun-fix `_read_doc_text`**: transport/GAS trả BINARY zip ('PK\x03\x04') → guard
  `_text_looks_binary` trả "" (hết so char-count trên rác binary — bài học dedup 2026-07-16).
- **[Resolver+control] `_nlm_or_corpus` (ADR-5/6/7)**: probe 1 lần/notebook/process (`_NLM_PROBE_CACHE` ở
  tl.py — bẫy I11 mutable), tái dùng `_nlm_preflight_report`; **hard-dead-only** (`_nlm_hard_dead`: auth/
  cookie/401; transient timeout/mạng/rate → retry 1 nhịp RỒI mới kết luận, không âm thầm rẽ). MẶC ĐỊNH BẬT +
  cảnh báo LỚN stderr mỗi lần rẽ; escape `--no-fallback` per-lệnh + `TL_NLM_FALLBACK=0` toàn cục (CI strict);
  phân loại per-lệnh qua field MỚI `COMMAND_META.nlm_fallback` (kwarg `_m()` default None; corpus_read=
  content/query/cross; defer=nlm-add/ingest-local/profile-ingest/ingest-missing; stale_cache=nlm-list;
  none=nlm-source-remove; +meta mới cho `nlm-cross` vốn chưa có meta).
- **[E1 đọc — ADR-1/2] `nlm-content`**: fail + hard-dead → resolve sid→registry→GDoc → `_doc_text_any` =
  NỘI DUNG Y HỆT (lossless), envelope stderr `nlm_status:offline/fallback:corpus_read`, rc=0; sid không
  resolve → giữ lỗi cũ rc=2 (không đọc mù). **`nlm-query`/`nlm-cross`**: hard-dead → **VERBATIM-RETURN ≤5**
  (`_corpus_question_resolve` PURE: tier exact-sohieu qua `_sohieu_query_hits_entry` → tier token-overlap;
  Điều trong câu hỏi → `_slice_dieu`) — CLI trả nguyên văn cho AGENT tự tổng hợp, KHÔNG máy sinh RAG;
  >5/mơ hồ → HẠ AN TOÀN chỉ ứng viên; `--out` né tràn stdout; mọi kết cục rc=0 (ADR-6).
- **[E3 đẩy — ADR-4] `nlm-add`**: probe TRƯỚC gate/claim/add — dead → `_nlm_add_deferred`: KHÔNG add mù/
  claim; registry `nlm_status=deferred` (KHÔNG corpus=true — chống corpus-ảo; row đã có sid → KHÔNG đè,
  stale-an-toàn; journaled+before thật) + in batch-link + rc=0; reconcile set pointer/corpus SAU.
  **ingest-local/ingest-missing**: nhánh tự-chuyển B1 (v1.34.54) nay chịu control-surface (`--no-fallback`
  → khôi phục fail-closed NLM_NOT_READY; ngưỡng pending>2 BATCH_LINKS giữ nguyên — không phải fallback).
  **profile-ingest**: MỚI tự chuyển `--no-nlm-add` khi hard-dead (mirror ingest-local; trước chết ở
  dedup-gate). **`nlm-list`**: dead → phục vụ cache C-#8 BẤT KỂ TTL + cờ `STALE_CACHE` rc=0 (advisory —
  KHÔNG phải bằng chứng vật lý; audit/migrate physical-first không đi đường này).
- **Test r121 ×17** (harness offline fake nlm_cli/gas/manifest): wiring meta+flags; env/flag disable unit;
  detection probe-once/hard-dead-only/transient-retry/no-probe-khi-tắt; query verbatim ≤5 + >5 hạ ứng viên +
  no-fallback + env-disable; cross envelope; content lossless + sid-lạ fail-closed; add deferred (không
  corpus/sid, claim=0, add=0) + no-fallback LIVE_SOURCE_LIST_FAILED + pointer-cũ không đè; list stale unit+
  wiring; doc-text docx-unzip/gdoc/pdf routing + cache + binary-guard + PURE resolver 5 ca.
- **Docs/goldens**: SKILL.md +bất biến 17 (NLM chết ≠ dừng) — nén history Pha B–E/prose giữ ≤48KB kernel
  (49141B) ⚠ **kernel đổi → user RE-IMPORT Capabilities**; parser_surface regen (doc-text + 8 lệnh thêm cờ);
  workflow_audit/tool_inventory golden regen (147 lệnh có meta); +golden doc_text_cache_fixture;
  COMMANDS.md cập nhật.

# ★ v1.34.59 — vá cosmetic: audit finding-output drive_id fallback gdoc_id (2026-07-16)

> Bug lộ khi dogfood data-op backlog 2026-07-16: `_physical_audit_classify` in `drive_id` RỖNG cho dòng
> registry key BẰNG gdoc_id (logic match đã fallback `drive_id or gdoc_id` nhưng OUTPUT thì không) →
> `suggested_commands` "tl nlm-migrate --drive-ids <rỗng>" vô dụng. TDD r120; selftest 1016→1017.

- **Vá**: 3 trường `drive_id` trong findings (pointer_mismatch/pointer_dead) + unverified_scope nay dùng
  `str(r0.get("drive_id") or r0.get("gdoc_id") or "")` ĐỒNG BỘ với logic match (`_phys_match` + `row_dids`);
  `suggested_commands` `--drive-ids <id>` kế thừa giá trị đúng. `_migrate_plan` vốn ĐÃ fallback — không đụng.
- **Test r120**: fixture 3 ca (mismatch/dead/unverified_scope) row CHỈ có gdoc_id → finding.drive_id = gdoc_id
  (không rỗng) + suggested_command mang gdoc_id. PURE, không cần NLM live.
- Chỉ đổi output cosmetic — KHÔNG đổi phân loại/hành vi ghi; scan thật KHÔNG lệch (data-op vừa qua match
  đúng vì logic đã fallback, chỉ hiển thị/lệnh-gợi-ý thiếu id).

# ★ v1.34.58 — ĐỢT C kế hoạch 13-vấn-đề: chất lượng + UX (PDF broken-font, reg-query --live, cache, guard 200) (2026-07-16)

> Đợt C/3 — CHỐT kế hoạch grill (`D:\Quốc hội\ke-hoach-sua-skill-13-van-de-2026-07-16.md`): C-#9 (Q8=a) +
> C-#11 (Q9=a) + C-#8/#10/#13 (Q10) + sửa lệch tài liệu API_CONTRACT (user yêu cầu). TDD r119 ×10
> (negative-input trước); 1016/1016 selftest. Python-only, GAS giữ 2.21.2m. **CẢ 13 VẤN ĐỀ ĐÃ XỬ TRỌN.**

- **[C-#9] `PDF_TEXT_LAYER_BROKEN_FONT`**: helper mới `_probe_pdf_quality` (KHÔNG đổi chữ ký
  `_profile_read_probe_text`) — text-layer ≥200 chars nhưng MẤT DẤU (density<0.005 + letters>500, tái dùng
  ngưỡng LOW_VIETNAMESE_MARK_DENSITY; ca 7 phụ lục CPTPP pdftotext ra text không dấu) → probe RỖNG + flag
  đúng bệnh *"Google-convert thường xử được; apply verify bằng text GDoc sau convert; KHÔNG vội OCR"* thay vì
  dọa NO_PROBE_TEXT/OCR_UNVERIFIED oan; `_vb_ingest_auto_plan` + profile-ingest DRY nối flag (gate không
  chặn từ probe local; apply giữ nguyên: `_read_doc_text(gdoc)` sau convert quyết corpus); PDF scan thật
  (<200 chars) giữ đường OCR cũ; text có dấu giữ nguyên đường C6.
- **[C-#11] `reg-query --live` (Q9=a)**: đọc AUTHORITATIVE qua `reg_get` (né manifest cache stale — bài học
  v1.34.50) — CHỈ hợp lệ kèm bộ lọc hẹp `--drive-id`|`--sohieu`|`--name` (thiếu → `LIVE_NEEDS_FILTER` rc=2);
  dịch: drive-id/sohieu(norm)/name_contains; rows qua đúng projection `_reg_query_row` + envelope v2, thêm
  `source='live'`; filter còn lại (cat/loai/nlm/corpus/row-kind/notebook) áp TIẾP phía client; KHÔNG merge
  base-also từ cache khi live.
- **[C-#8] `nlm-list --cached`** (opt-in, chung helper `_nlm_source_list_cached` TTL 10' với audit; mặc định
  vẫn list tươi) + test TTL-quá-hạn tự gọi lại.
- **[C-#10] pdftotext path phi-ASCII**: `_read_local_text_for_analysis` phát hiện path không encode ASCII
  được (`D:\Dữ liệu\…` — build Git Bash/cp1258 nhận arg hỏng, im lặng 0 output) → copy sang temp ASCII rồi
  chạy trên bản copy (tự xoá); +RUNBOOK B5b bẫy path Việt.
- **[C-#13] `release-bundle` guard trần import**: >200 entry (kể cả RELEASE_MANIFEST.json ghi thêm) → FAIL
  `IMPORT_LIMIT_EXCEEDED` TRƯỚC khi ghi zip, liệt kê `newest_20` theo mtime để lộ thủ phạm (suýt dính 205
  file khi zip -r tay); hiện 169/200 pass.
- **Sửa lệch tài liệu (user yêu cầu)**: `references/API_CONTRACT.md` dấu LIVE `2.21.2l`→`2.21.2m` (+ ping
  literal + note F-04/F-08 "CHƯA DEPLOY"→ĐÃ LIVE trong 2.21.2m) — kèm **drift-lock r119**: con dấu đầu file
  PHẢI khớp `tl.py EXPECT_VERSION`, trôi là selftest đỏ (hết lệch tài liệu âm thầm).
- ★Bài học harness lặp lại đúng dự báo: HẰNG mới `_PDF_BROKEN_FONT_WARN` phải re-export TRỰC TIẾP trong tl
  (bẫy I11 biến thể); `release.bind` = COPY-một-lần (như ocr) → stub test vá module `tl_core.release`,
  không phải `_TL_MODULE`.
- TDD r119 ×10: broken-font (flag thay OCR-scare / có-dấu đường cũ / scan<200 OCR cũ) + LIVE_NEEDS_FILTER +
  live-name-qua-reg_get-không-đụng-manifest + nlm-list --cached + cache TTL hết hạn + pdftotext non-ASCII
  temp-copy + IMPORT_LIMIT_EXCEEDED + drift-lock API_CONTRACT↔EXPECT_VERSION.

# ★ v1.34.57 — ĐỢT B kế hoạch 13-vấn-đề: bộ di dời physical-first (nlm-audit-physical + nlm-migrate) (2026-07-16)

> Đợt B/3 kế hoạch grill (`D:\Quốc hội\ke-hoach-sua-skill-13-van-de-2026-07-16.md`): B-#3 + B-#4..#7 (Q5=a,
> Q6=a, Q7=a) + cache listing (Q10, kéo lên vì audit dùng) + vá before-thật nhánh link nlm-add (phát hiện
> smoke A). TDD r118 ×15 (negative-input trước); 1006/1006 selftest. Python-only, GAS giữ 2.21.2m.

- **[B-#3] Lệnh MỚI `nlm-audit-physical` (READ-ONLY)**: đối soát VẬT LÝ ↔ con trỏ registry (physical-first —
  bài học 32/40 CPTPP: `nlm_notebook_id` chỉ là nơi registry NGHĨ). Scope mặc định topology VBQPPL
  (base + overflow, foreign profile KHÔNG quét — tham chiếu chủ đích không thành noise); `--notebooks` /
  `--all-profiles` mở rộng. Match 2 tầng như reconcile (drive_id → title-key DUY NHẤT; KHÔNG dùng is_stale).
  4 finding POINTER_MISMATCH / UNREGISTERED_PHYSICAL / DUP_PHYSICAL (keep = sid registry trỏ) /
  POINTER_DEAD (CHỈ khi scope ⊇ notebook pointer trỏ hoặc nb rỗng; ngoài scope → `unverified_scope`
  advisory, không oan); dòng removed* = tombstone bỏ qua; `suggested_commands` điền sẵn; rc=0 sạch/1 finding.
  Classifier PURE `_physical_audit_classify`. Doctor +1 advisory TĨNH nhắc chạy sau lô di dời/ingest lớn.
- **[B-#8→B] Cache listing `_nlm_source_list_cached`** (TTL 10', `scripts/.tl_state/nlm_list_cache_<nb>.json`,
  ghi bytes LF): audit dùng mặc định (`--refresh-live` ép tươi); nlm-migrate KHÔNG dùng cho notebook ĐÍCH
  (physical-first cần tươi). Bề mặt `nlm-list --cached` để đợt C (r119).
- **[B-#4..#7] Lệnh MỚI `nlm-migrate`** — MỘT lệnh di dời idempotent, re-plan TỪ VẬT LÝ mỗi lần chạy:
  PLAN (DRY mặc định): ĐÚNG 1 bộ lọc (--name-contains | --cat | --drive-ids file/csv; sai → FILTER_REQUIRED
  rc=2) → list ĐÍCH luôn TƯƠI (fail-closed LIVE_SOURCE_LIST_FAILED) → 3 nhóm POINTER_OK / REPOINT (sid vật
  lý thắng sid registry) / ADD + cleanup candidates (nguồn cũ ở --from cho doc POINTER_OK) dưới dạng lệnh
  `nlm-source-remove` điền sẵn — Q7: CHỈ IN, không bao giờ tự gỡ. APPLY: REPOINT in-process batch
  `_journaled_reg_upsert` (~2s/dòng, before nb/sid THẬT → undo được, row_kind suy topology mẫu F-06) +
  verify CUỐI `reg_get_bulk` toàn bộ drive_ids (so nb+sid); ADD >NLM_BATCH_LINKS_THRESHOLD (2) không
  --api-add → BATCH_LINKS (stdout = CHỈ link mỗi dòng 1 — mẫu nlm-links; stderr = notebook URL + "dán xong
  CHẠY LẠI đúng lệnh này"), rc=0 không side-effect thêm; --api-add/≤2 doc → per-doc qua `cmd_nlm_add`
  IN-PROCESS (đường A-#1/#2: claim F-04 + dedup-gate + verify-then-link; TRUYỀN title — bịt lỗ gate thiếu
  title phát hiện smoke A). Chạy lại sau dán: ADD tự chuyển REPOINT = harvest (không cờ riêng/state file).
  KHÔNG đi qua matcher reconcile (không đụng ownership-guard A2). Contract `nlm_migrate` + COMMAND_META
  high/registry_nlm/confirm/dry-run.
- **Vá phát hiện smoke A (2026-07-16)**: nhánh link `nlm-add` nay ghi journal `before_by_key` bằng sid/nb/status
  CŨ THẬT từ row hiện tại (trước hardcode "" → undo lần link-ĐÈ không khôi phục được sid cũ — đúng ca dup
  CPTPP 4e2bc585 đè a1322194).
- Kernel SKILL.md: bảng NLM +audit-physical/migrate/source-remove (49.142/49.152B — trim note archive §8);
  `references/COMMANDS.md` +2 dòng lệnh mới. Parser-surface + golden regen có chủ đích.
- TDD r118 ×15: audit classifier (mismatch / dead-vs-unverified-scope / unregistered+dup / clean+removed-skip)
  + cache hit/refresh + migrate plan PURE (3 nhóm, phys-sid thắng, title-tier, cleanup) + wiring (filter-
  required, DRY-no-writes, apply repoint+verify bulk, batch-links stdout thuần, api-add in-process + title,
  cleanup text-only-no-delete) + before-thật nlm-add + audit cmd wiring scope/rc + parser/meta/contract/doctor.
- **Fix giữa live-smoke (có test khoá)**: `_migrate_plan` +tier-0 sid-pointer-sống-tại-đích = POINTER_OK
  (nhất quán audit OK-check) — ca thật CPTPP Ch22/25 dup vật lý trên đích: listing không lộ drive-URL +
  title dup → did/title câm nhưng sid live; trước fix 2 doc rơi nhầm ADD (dedup-gate vẫn chặn nhưng phân
  loại sai). **Live-smoke B ĐẠT**: `nlm-migrate --to VBQPPL-2 --name-contains CPTPP` DRY = 40×POINTER_OK /
  0 ADD / 0 REPOINT (kỳ vọng §4); `nlm-audit-physical` topology (base 293 + VBQPPL-2 243) bắt drift THẬT:
  2 POINTER_MISMATCH di sản ca A2 (QD_100-2023-TW + HU_WCT vật lý ở Khảo sát 80742228), 4 DUP_PHYSICAL
  (CPTPP Ch22/25 ×2 trên VBQPPL-2 + TRIPS/WCT ×2 trên 80742228), 17 POINTER_DEAD (TT BGDĐT/BYT/BKHCN +
  EVFTA + HD_36…), 54 pointer khảo sát → unverified_scope advisory (không oan) rồi 0 khi thêm --notebooks;
  cache hit round-2 ✓. 2 dòng row_kind=overflow nb rỗng (Luat_57-2014/Luat_87-2015) có sid RỖNG → đúng
  doctrine KHÔNG phải pointer-drift (lộ qua doctor row_kind, không qua audit — nuance so kỳ vọng kế hoạch).
  Data-op backlog (USER QUYẾT): gỡ dup + repoint 2 mismatch + xử 17 dead theo suggested_commands.

# ★ v1.34.56 — ĐỢT A kế hoạch 13-vấn-đề: nlm-add an toàn (verify-then-link + claim F-04) + nlm-source-remove (2026-07-16)

> Đợt A/3 kế hoạch grill 11 quyết định (`D:\Quốc hội\ke-hoach-sua-skill-13-van-de-2026-07-16.md`): A-#1 + A-#2
> + A-#12. TDD r117 ×12 (negative-input trước — luật đứng r102); 991/991 selftest. Python-only, GAS giữ 2.21.2m.
> Doctrine kernel mới (bất biến 16): *Registry chỉ ghi sự thật ĐÃ XÁC MINH vật lý; nghi ngờ → để stale, KHÔNG
> ghi trước-xác-minh-sau.*

- **[A-#1] `nlm-add` VERIFY-THEN-LINK (Q2=a — chống con trỏ treo)**: nhánh reg_link sau add nay (a) `--no-wait`
  → BỎ HẲN reg_link + note lưới `nlm-reconcile --apply` cuối lô (sid chưa settle — probe sẽ âm tính giả;
  stale-an-toàn); (b) có wait → PROBE live 1 nhịp TRƯỚC khi ghi registry (`source_get` nếu nlm_cli có, fallback
  re-list FRESH — list của dedup-gate chụp TRƯỚC add nên không tái dùng); probe fail → `SID_NOT_LIVE_YET`,
  KHÔNG ghi registry, rc vẫn 0 (add đã thành công; link là bước phụ stale-an-toàn). Gốc: ca canary dbe706a0
  NOT_FOUND phải revert tay (memory NLM-MIGRATION 2026-07-16).
- **[A-#2] Claim F-04 cho `nlm-add` (Q3=b)**: acquire `ingest_claim` NGAY SAU dedup-live gate, TRƯỚC
  `source_add` — CHỈ khi có `--drive-id` (url/file/text không có drive identity); `--skip-live-check` KHÔNG bỏ
  claim; MANDATORY client-side khớp D1 (endpoint lỗi → `INGEST_CLAIM_FAILED` rc=2 TRƯỚC add; denied →
  `CLAIMED_ELSEWHERE` rc=2 + note "lần add trước/host khác có thể ĐÃ xong server-side — verify nlm-list/
  nlm-reconcile TRƯỚC khi retry; TTL 5'; sau timeout chờ ≥60s settle"). Journal mới `nlm-add_<run_id>` cấp
  run_id TRƯỚC add; COMMIT claim GỘP `reg_get_bulk` sau reg_link verified (best-effort TTL heal — no-wait/
  sid-not-live thì KHÔNG commit). Gốc: add timeout nhưng server-side xong → retry tạo 3 bản Phu_luc_I trùng.
- **[A-#12] Lệnh MỚI `nlm-source-remove <sid...> [--apply --confirm yes] [--force]`** (Q4=a): gỡ nguồn KHỎI
  notebook NLM (wrapper ngữ nghĩa `nlm source delete` — nlm_cli.source_delete có sẵn được tái dùng, KHÔNG
  trash Drive, KHÔNG đụng dòng registry; khác `source-delete` xóa cứng 3 tầng). DRY liệt kê con trỏ; GUARD
  `POINTER_STILL_ATTACHED` (manifest refresh + `reg_get` authoritative fail-closed — bài học manifest-không-
  đáng-tin v1.34.50) chặn sid còn con trỏ, thoát `--force`; sid đã gỡ → `deleted_count=0`/not-found = noop OK
  (idempotent, re-run không FAIL — helper PURE `_source_remove_delete_verdict`); batch N sid / 1 process;
  rc=2 khi toàn bộ chặn/có fail. COMMAND_META high/nlm/confirm/dry-run + contract `nlm_source_remove` +
  GENERATED_SPECS + stub I11; parser-surface snapshot regen có chủ đích.
- Kernel SKILL.md: +bất biến 16 (doctrine physical-first 1 dòng); §8 sửa note stale "2.21.2l LIVE tới khi
  deploy" → 2.21.2m ĐÃ LIVE. `references/COMMANDS.md`: nlm-add cập nhật hành vi mới + dòng mới
  nlm-source-remove.
- TDD r117 ×12: no_wait_skips_reg_link / verify_fail_no_link / verify_ok_links (positive control F-06) /
  claim_denied_stops_before_add / claim_endpoint_fail_stops / claim_granted_commit / url_path_no_claim /
  source_remove {pointer_guard_blocks, batch_and_noop, dry_lists_pointers, confirm_required,
  parser_meta_contract}.

# ★ v1.34.55 + GAS 2.21.2m (CHƯA DEPLOY — chờ xác nhận) — ĐỢT 3: row_kind export RAW + claim ingest-local + profile-ingest --resume (2026-07-15)

> Đợt 3 kế hoạch grill Q1–Q10 (`D:\Quốc hội\ke-hoach-nang-cap-tra-luat-2026-07-15.md`): D3→D2→D1 + C4+C5+C7.
> TDD r116 ×9; 979/979 selftest; node harness GAS ×2 (rowkind 9/9 + claim 19/19 trên 2.21.2m). **GAS 2.21.2m
> ĐÃ VIẾT + TEST nhưng CHƯA `clasp deploy`** (auto-mode chặn đúng gate production — cần user xác nhận; tới lúc
> đó ping LIVE vẫn 2.21.2l, chỉ lệch version-match, KHÔNG lệnh nào fail-closed). Client EXPECT_VERSION=2.21.2m.

- **[D3] GAS 2.21.2m — export `row_kind` RAW** (`references/Code.2.21.2m.gs`): `entryOf_` (manifest) +
  `nlmCompactRow_` bỏ default `||'own'` — dòng blank/legacy hết bị export che thành 'own' (gốc bất nhất 37
  CPTPP manifest↔registry + backlog v1.34.49); các hàm ĐẾM (`regIsCorpusCounted_`/`profileOwnCount_`/
  `doNlmSlots_`) GIỮ doctrine blank→own (v2.21.2e). Node harness MỚI `references/gas_rowkind_test.js` (9 case:
  export raw, đếm giữ default, assert mức nguồn) + gas_claim_test 19/19 chạy lại trên 2.21.2m. Deploy khi user
  duyệt: `cp references/Code.2.21.2m.gs gas-project/Code.gs && (cd gas-project && clasp push -f) && clasp
  deploy -i <deploymentId LIVE — xem memory gas-clasp-deploy / `clasp deployments`> -d "2.21.2m"` → `tl ping`.
- **[D2] Điều tra 92 dòng base trỏ notebook Khảo sát Luật Xuất bản (80742228)** — read-only, TRÌNH USER QUYẾT
  (không tự chọn): (i) **37 CPTPP** cat 23, corpus=TRUE, row_kind=OVERFLOW, pushed — được ĐẾM corpus nhưng
  notebook đích là notebook PROFILE (foreign từ v1.34.51) → `nlm-cross` vbqppl KHÔNG tra được các phụ lục này;
  VBQPPL-2 thật (45739ff7, 243 claim) còn ~57 chỗ = đủ di dời. (ii) **54 hồ sơ khảo sát** corpus=false,
  row_kind=own → vô hại với đếm, dual-registered CHỦ ĐÍCH. (iii) **1 dòng 04-CT/TW** (Đảng) corpus=true nhưng
  on_nlm=FALSE — trỏ notebook khảo sát mà không live ở đó → cần nạp lại đúng notebook. (iv) 2 dòng row_kind=
  overflow nhưng nlm_notebook_id RỖNG — drift nhỏ, backfill-notebook. Phương án chi tiết ở cuối phiên.
- **[D1] Claim F-04 cho `ingest-local`** (nối scope-cut v1.34.52; Q6=a target_scope GIỮ trục Drive-folder):
  acquire 1-key sau journal-start TRƯỚC cửa sổ upload→dedup→add (MANDATORY client-side: endpoint lỗi →
  `INGEST_CLAIM_FAILED` rc=2 trước side-effect; denied → `CLAIMED_ELSEWHERE`); BỎ QUA khi --no-nlm-add
  (không có cửa sổ add); COMMIT GỘP vào 1 call `reg_get_bulk` sau reg_link verified (best-effort, TTL 5' heal).
- **[C4+C5] `profile-ingest --resume --name <tên> --apply --confirm yes`**: NỐI THEO REGISTRY sau khi chết
  giữa chừng — dò canonical + chunk `__partNN` đã có, re-split text canonical TỪ DRIVE (tất định), CHỈ làm
  part thiếu (`_profile_push_chunks` tách chung với đường thường, done_parts skip); cuối cùng ghi corpus
  canonical theo children_ok → name đã đủ part mà corpus kẹt false = chạy resume là TỰ SỬA (C5 — data-op cho
  4 canonical kẹt của phiên OCR: BaocaoTienDo/TongHopYKien/SoSanhLuat/DuThaoLuatSuaDoi). Nguồn đơn: thiếu sid
  → add, có sid → chỉ repair corpus. Guards: RESUME_NEEDS_NAME/CONFIRM_REQUIRED/RESUME_NOT_FOUND/
  RESUME_TEXT_UNAVAILABLE (fail trước side-effect).
- **[C7] `profile-list --discover`**: 0 kết quả hành-động-được → note RÕ (json `note_zero_actionable` +
  stderr) nêu giới hạn quét (chỉ thư mục con trực tiếp Van_ban_thuong) + lệnh kiểm thẳng — hết im lặng sai.
  Live-check: ATVSLĐ nay hiện `configured` (scan 18/18) — ca sót cũ không tái hiện; guard vẫn cần.
- Test r116 ×9: claim granted→commit (bắt commit_claims kèm source_id/run_id) / denied 0-side-effect /
  endpoint-fail dừng / no-nlm-add bỏ claim; resume chỉ-làm-phần-thiếu / sửa-corpus-kẹt / nguồn-đơn / 3 guard
  negative; discover 0-kết-quả note. ★harness: `_nlm_post_add_dup_check` truthy=DUP (stub phải trả None).
- EXPECT_VERSION 2.21.2l→2.21.2m; SKILL.md §8 cập nhật target + doctrine deploy clasp (bác 'KHÔNG deploy từ
  skill được' — gas-clasp-deploy); kernel 49000B (< trần 48KB=49152).
- Backlog còn: E2 header-cache/E3 registry-first (chưa đủ số đo TL_PERF thực chiến — đo qua vài phiên nạp lô
  rồi quyết); A7b source-audit --dup-dieu; data-op WCT trộn Berne (chờ user quyết cùng D2).

# ★ v1.34.54 — ĐỢT 2 kế hoạch nâng cấp: batch-link NLM (nlm-links/ingest-inbox) + preflight 2 tầng + plan-artifact reconcile (2026-07-15)

> Tiếp grill Q1–Q10 (`D:\Quốc hội\ke-hoach-nang-cap-tra-luat-2026-07-15.md`) — đợt 2 trọn: B1+B2+A1/C8+A3+A7a+C6.
> TDD r115 ×12; 970/970 selftest; kernel SKILL.md giữ đúng trần 48KB (49151B — nén doctrine mới thành pointer).

- **[B1] `tl nlm-links`** (read-only): stdout = CHỈ link Drive (mỗi dòng 1 — dán BATCH vào Add source → Websites;
  UI nhận nhiều link cách nhau xuống dòng [docs Google], link Docs nhận thành nguồn Drive [user thực chứng]);
  notebook-URL/đếm/hướng dẫn/tuổi cookie ở stderr; --json envelope. Lọc dòng chưa-trên-NLM (scope nền loại
  ref/thuong; profile giữ chunk ref). **Ngưỡng batch-link** `NLM_BATCH_LINKS_THRESHOLD=2` (hằng số):
  `ingest-missing --apply` pending>2 ∨ cookie chết → mode BATCH_LINKS (in links, KHÔNG add API; ép:
  `--force-api-add`); `ingest-local` cookie chết → TỰ CHUYỂN add-tay --no-nlm-add (hết abort NLM_NOT_READY).
- **[B2] `tl ingest-inbox`**: quét folder Drive (nền=inbox _HOP_NAP, profile=rootFolderId, hoặc --folder) qua
  GAS list (né bẫy Drive MCP parentId folder share), diff registry reg_get_bulk 1 call, GDoc-native skip;
  per-file child 2-BƯỚC DRY→plan_hash→apply (khuôn C1): nền `ingest-local --drive-id --auto-plan --no-nlm-add`,
  profile `profile-ingest --drive-id --no-nlm-add` (MỚI — dừng sau Drive+registry, GIỮ PHẲNG); profile nghi
  VBQPPL chất lượng cao (sohieu từ tên + docx/doc/pdf) → `vbqppl_candidate` + ask_user (KHÔNG tự nạp corpus).
  Idempotency contract `ingest_inbox` (drift-lock r65 bắt đúng thiết kế). DRY mặc định; --apply --confirm yes.
- **[A1+C8] preflight NLM 2 tầng + `tl nlm-auth-status [--wait]`**: `_nlm_preflight_report` = probe LIVE
  notebook_get (M1) + tuổi cookie từ metadata.json last_validated (đời ~60'; >45' → WARN khuyên re-auth/
  nlm-links); hasattr-guard cả 2 method (client fake không bị kết luận chết oan — bắt khi r113 hồi quy).
  Warn nối vào ingest-local preflight + nlm-add + reconcile --apply. auth-status --wait poll 20s/300s.
  Dogfood live: alive=true, age 40.5', est_remaining 19.5'.
- **[A3] reconcile sweep plan-artifact + `--from-plan`**: --all-notebooks DRY ghi
  `.tl_state/reconcile_plan_<nb>.json` (slim rows đủ dữ liệu ghi) + in `apply_commands` copy-paste;
  `--all-notebooks --apply` vẫn chặn nhưng message ACTIONABLE (danh sách lệnh per-notebook đúng profile);
  per-notebook `--apply --from-plan` BỎ re-scan NLM (source_list) — TTL 15' (PLAN_STALE), freshness
  reg_get_bulk trên ĐÚNG dòng sắp ghi (đổi so plan → DROP + báo cáo), cấm kèm --clear-stale. Docs đã đúng
  từ v1.34.50 (COMMANDS.md ghi DRY-only) — bổ sung mô tả mới.
- **[A7a] gate dup-Điều tại ingest** (`_dup_dieu_scan` PURE): đếm Điều trùng số + letterhead thứ 2 sau dòng 80;
  `_vb_ingest_auto_plan` cat 23 → warning `MIXED_DOCUMENT_SUSPECT_DUP_DIEU` (ca WCT trộn Berne), cat khác →
  `DUP_DIEU_INFO`; profile-ingest in info stderr. KHÔNG chặn (VBHN lặp Điều hợp lệ).
- **[C6] probe PDF dùng CHUNG extractor ocr-run** (`_read_local_text_for_analysis`/pdftotext, ngưỡng ≥200
  chars): hết false-negative NO_TEXT_FOR_VERIFY trên PDF có text-layer (7/7 ca phiên OCR).
- Test r115 ×12 (probe PDF, preflight 2 tầng + fake-guard, links rows/URL/stdout-thuần, force-api-add,
  dup-Điều scan + auto-plan flags, from-plan fresh/DROP/STALE/clear-stale, all-notebooks actionable,
  dead-cookie autoswitch, profile --no-nlm-add, ingest-inbox DRY/confirm/apply). Parser snapshot regen.
- ★Bài học: kernel 48KB đã đầy 99.94% — doctrine mới phải là POINTER vài dòng (chi tiết COMMANDS.md), và
  edit tool bị kẹt classifier giữa chừng → LUÔN chạy lại selftest xác nhận cả cặp edit đã vào (1 edit rơi
  làm NameError doc_text).
- Backlog đợt 3 (v1.34.55 + GAS 2.21.2m): D3 manifest_export đọc cột row_kind → D2 điều tra 55 dòng 80742228
  (user quyết) → D1 claim ingest-local; C4 resume profile-ingest; C5 corpus canonical/chunks; C7 discover
  0-kết-quả; E2 header-cache/E3 registry-first theo số đo TL_PERF; data-op WCT; A7b source-audit --dup-dieu.

# ★ v1.34.53 — ĐỢT 1 kế hoạch nâng cấp (grill Q1–Q10): ownership-guard reconcile + 6 fix chặn-oan/false-success (2026-07-15)

> Grill-with-docs 10 quyết định (`D:\Quốc hội\ke-hoach-nang-cap-tra-luat-2026-07-15.md`) từ 2 log phiên thật
> (7 vấn đề phiên NLM + 8 vấn đề phiên OCR/profile). Đợt 1 = Python thuần, KHÔNG đụng GAS/data. TDD r114 ×12
> (negative-input theo luật đứng r102). 958/958 selftest; golden/workflow-audit/determinism-audit strict xanh.

- **[A2 — BLOCKER, sửa SAI DỮ LIỆU ÂM THẦM] `nlm-reconcile` ownership guard** (`_nlm_reconcile_plan`): dòng
  registry đã trỏ `nlm_notebook_id` notebook KHÁC không bao giờ thành link candidate nữa (mọi tier, kể cả
  drive_id — ca dual-registered là có chủ đích); tier YẾU (sohieu/title) chỉ link dòng CHƯA có `nlm_source_id`.
  `by_drive` thành LIST lọc theo chủ quyền (dual-registered chọn đúng dòng own). Khóa mới `foreign_skipped`
  (count + sample) trong output — match-nhưng-của-notebook-khác được BÁO, không GHI. Log gốc: reconcile
  profile-notebook 80742228 match TRIPS/WCT theo title rồi patch con trỏ dòng corpus VBQPPL-2 sang notebook
  profile → dòng corpus trỏ sai shard. Bonus đúng-hơn: sohieu/title trùng giữa 1 dòng foreign + 1 dòng own
  chưa-link → foreign bị loại khỏi ứng viên, own link được (trước: mơ hồ → bỏ).
- **[A4 — chặn oan] `ingest-local --no-nlm-add`** bỏ hẳn `_ingest_target` (nlm_preflight GAS + đếm slot live):
  cookie chết + base đầy hết bị `OVERFLOW_ROOM_UNKNOWN` chặn dù không đụng NLM; target chỉ để in URL
  next-steps, notebook thật do add-tay + reconcile quyết (v1.34.35).
- **[C1 — luồng OCR chết 100%] bridge `ingest-ocr`/`profile-ingest-ocr`** forward xác nhận xuống child: apply
  chạy child 2 BƯỚC (`planned_child_dry` lấy `plan_hash` → apply kèm `--apply --confirm yes
  --expected-plan-hash <hash>`, helper `_bridge_run_child_apply`). Trước: thiếu `--confirm yes` →
  child `CONFIRM_REQUIRED` mọi lần apply, phải bypass bridge. DRY child không trả hash → DỪNG rc=2
  `CHILD_DRY_PLAN_FAILED` TRƯỚC side-effect.
- **[C2 — dup 6 dòng khi timeout giữa lô] `profile-ingest`/`profile-file-add` dup-guard TÊN trong registry**
  (live `reg_get name_contains`, exact-match, fail-closed) TRƯỚC upload/tạo GDoc — sớm hơn
  `TITLE_ALREADY_ON_NOTEBOOK` (gate đó chạy khi GDoc+registry đã tạo). `NAME_ALREADY_IN_REGISTRY` liệt kê dòng
  cũ; cùng drive_id nguồn (`--drive-id` chạy lại) không tính dup; thoát chủ đích: `--allow-dup-name`.
- **[C3] `--json` NO-OP toàn cục** (generic-flag pass, SUPPRESS): cờ thừa không làm crash lệnh vốn in JSON
  (log: `source-delete <id> --json` chết unrecognized arguments).
- **[A5] `download`** nhận positional lẫn `--file-id` (đồng bộ extract/nlm-get); thiếu cả hai →
  `FILE_ID_REQUIRED` rc=2.
- **[A6] `reg-query --notebook <id>`** lọc theo `nlm_notebook_id` — hết lọc tay bằng Python khi dòng nhiều
  shard/profile lẫn nhau (projection JSON đã phơi `nlm_notebook_id` từ trước).
- **[E1 — đo trước, cache sau (Q5)] tổng kết hiệu năng cuối run**: `--timings`/`TL_TIMINGS=1`/**`TL_PERF=1`
  (alias mới)** in thêm TỔNG số GAS call + tổng ms + top-5 action chậm nhất (`_timing_summary_lines`, PURE) —
  baseline cho quyết định header-cache/registry-first đợt 3.
- Test: r114 ×12 — 6 reconcile guard (foreign title/drive_id không clobber, weak-tier không re-point dòng đã
  link, dual-registered chọn own, positive-control title/sohieu) + no-nlm-add BOOM-harness (slot count = nổ
  nếu bị gọi) + 2 bridge (confirm+hash forwarded; DRY-no-hash dừng trước apply) + 2 dup-guard (chặn trước
  upload; fail-closed + bypass) + json-noop/download-positional/reg-query-notebook/timing-summary. Parser
  surface snapshot regen (đổi CLI có chủ đích). ★Bài học harness: `ocr.bind` = COPY-một-lần (KHÔNG rebase
  `__globals__` như ingest_ops) → stub phải patch MODULE `_tl_ocr`, patch `_TL_MODULE` không ăn.
- Backlog đợt 2/3 (kế hoạch đã chốt): B1 `nlm-links` + ngưỡng batch-link, B2 `ingest-inbox`, A1+C8 preflight
  2 tầng + `nlm-auth-status --wait`, A3 plan-artifact reconcile, A7a gate dup-Điều, C6 hợp nhất text-probe;
  D3 GAS 2.21.2m (manifest_export đọc cột row_kind) → D2 điều tra 55 dòng 80742228 → D1 claim ingest-local;
  C4 resume profile-ingest, C5 corpus canonical/chunks, C7 discover 0-kết-quả, E2/E3 theo số đo E1.

# ★ v1.34.52 + GAS 2.21.2l (CHƯA DEPLOY) — F-04 ingest_claim + F-08 reg_get_bulk (2026-07-15)

> Grill-with-docs 12 quyết định D1–D12 (`D:\Quốc hội\ke-hoach-gas-2.21.2l-ingest-claim-2026-07-15.md`), ý tưởng
> tham khảo bundle Codex NHƯNG code viết lại từ đầu. **ĐỤNG WEBAPP LIVE PRODUCTION** — GAS `Code.2.21.2l.gs` đã
> viết + test node harness xanh, nhưng **CHƯA `clasp deploy`** (chờ xác nhận riêng trước khi ghi đè deployment
> live — xem việc tiếp theo). Client v1.34.52 đã đòi `EXPECT_VERSION=2.21.2l`; `tl ping` LIVE vẫn 2.21.2k cho
> tới khi deploy — mọi lệnh `--apply` cần webapp mới sẽ tự DỪNG rc=2 với lỗi rõ ràng cho tới lúc đó.

- **[F-04] `ingest_claim`** (Sheet tab `claims` riêng, cùng Spreadsheet với `files`, `LockService` — D1):
  reservation identity xuyên host. `identity_hash` THỐNG NHẤT cho mọi đường ingest (D2) — hàm mới
  `ingest_contract.identity_hash_for_drive_source()` dùng LẠI `_hash_payload` sẵn có (không thêm thuật toán
  hash). Acquire hàng loạt 1 action (D9), commit GỘP vào `reg_get_bulk` (D3, không thêm round-trip), release
  tường minh khi fail vĩnh viễn (D3). TTL 5 phút (D4); contested claim → skip + báo cáo, KHÔNG retry trong run
  (D5); lazy GC ngay trong acquire (D10, dọn `committed`/`released`>24h).
- **[F-08] `reg_get_bulk`**: đọc N key 1 lần, trả TOÀN BỘ 27 `REG_COLS_` (D6), commit claim gộp cùng round-trip.
- **Client `cmd_ingest_missing` (v1.34.52)**: acquire claim cho TOÀN BỘ `to_add` TRƯỚC vòng lặp add (D9); item bị
  host khác giữ → `CLAIMED_ELSEWHERE` vào `results`, loại khỏi batch, **KHÔNG tính FAIL** (rc vẫn 0 nếu phần còn
  lại ổn); webapp cũ (<2.21.2l)/lỗi mạng khi gọi `ingest_claim` → `INGEST_CLAIM_FAILED` DỪNG rc=2 TRƯỚC mọi
  side-effect (D8: claim optional server-side, mandatory client-side). Commit theo lô hằng số 10 (D7) qua
  `reg_get_bulk` SAU vòng lặp add — best-effort, lô lỗi tự heal qua TTL 5' (không chặn kết quả run).
  ★**Scope cut tường minh (không giấu)**: `ingest-local` (single-file, đã có `identity_hash`/confirm/plan_hash
  riêng, cửa sổ race hẹp hơn ingest-missing theo batch) **CHƯA wiring claim** — để đợt sau.
  ★**Scope cut khác**: KHÔNG release tường minh khi item fail tạm thời trong `ingest-missing` (dựa TTL 5' tự
  heal — đủ an toàn vì claim chỉ che đúng cửa sổ add, không phải toàn vòng đời item).
- **Test lần đầu cho GAS**: `references/gas_claim_test.js` — Node harness nạp `.gs` qua `vm` với stub GAS
  services tối thiểu, gọi thẳng 4 hàm PURE (`_claimGcFilter_`/`_claimAcquireDecide_`/`_claimCommitDecide_`/
  `_claimReleaseDecide_`) — test RACE THẬT (2 host cùng key, ai trước thắng), TTL reclaim, GC, double-commit
  chặn qua `run_id` mismatch (D12). **19/19**. `node --check` cú pháp toàn file (copy `.js` tạm — `.gs` không
  phải extension Node nhận trực tiếp).
- TDD Python: r113 ×3 negative-input (claim denied → skip không FAIL; claim-endpoint-lỗi → rc=2 zero
  side-effect; mọi claim bị từ chối → rc=0 zero-added). Selftest **940→943/943**.
- ★**Bug bắt khi chạy thật**: `contract_check.py --bump` ghi CRLF trên Windows (`write_text` thiếu
  `newline="\n"`) trong khi `.gitattributes` khóa `* -text` (byte thật, không eol-normalize) → SKILL.md
  49121→49440B, VƯỢT trần 48KB (r67 kernel-size đỏ). Vá 4 chỗ `write_text` thiếu `newline="\n"` trong
  `bump_after_deploy` (API_CONTRACT.md/tl.py/SKILL.md/RUNBOOK.md).

## Việc tiếp theo (KHÔNG tự làm — cần xác nhận riêng)
1. `clasp push -f` (an toàn, chưa đổi live) rồi **HỎI XÁC NHẬN** trước `clasp deploy -i <LIVE_DEPLOYMENT_ID>`
   (ghi đè deployment production).
2. Verify `tl ping`==2.21.2l, `contract_check.py --audit` khớp.
3. Canary LIVE 1 tài liệu identity biết trước: claim acquire → source_add → commit qua `reg_get_bulk` → verify
   registry đúng → thử race giả (2 acquire liên tiếp cùng key) trước khi mở rộng.

# ★ v1.34.51 — doctor KHÔNG nhận nhầm notebook profile-khác thành vbqppl overflow-shard (điều tra live 2026-07-15)

> Điều tra 55 finding row_kind "drift" còn lại sau v1.34.50 (user chọn "fix doctor code, giữ data"): READ-ONLY 2
> scope + reg_get authoritative → **92 dòng dual-registered** (base VBQPPL ⊕ profile "Khảo sát Luật Xuất bản",
> notebook 80742228, corpus=false: phụ lục CPTPP làm `ref` + hồ sơ khảo sát) — **CÓ CHỦ ĐÍCH, không phải rác**.
> Gốc noise: manifest lỡ gắn `row_kind='overflow'` vài dòng trên 80742228 → `_resolve_shard_topology` nhận nhầm
> notebook PROFILE-KHÁC thành vbqppl overflow-shard → flag oan 55 dòng. Python-only, KHÔNG đụng data, GAS giữ 2.21.2k.

- **`_foreign_profile_notebooks(cfg, current_profile)`** (PURE): tập notebook (notebookId + shards[] ids) của MỌI
  profile KHÁC. `_resolve_shard_topology` dùng để: notebook profile-khác có registry row `overflow` → **1 finding
  advisory `FOREIGN_PROFILE_NOTEBOOK`** (KHÔNG thành observed vbqppl shard), notebook lạ KHÔNG-của-profile-nào =
  shard vbqppl thật chưa declared → GIỮ `UNDECLARED_REGISTRY_SHARD` như cũ. Trả thêm khoá `foreign_notebooks`.
- **`_topology_row_kind_findings`**: bỏ qua dòng có notebook ∈ foreign (doctor hết flag oan 92 dòng dual-registered
  — dogfood live: **55 → 0** row_kind findings, chỉ còn 1 advisory).
- **`_resolve_overflow_shards`** (wrapper đọc/reconcile/cross/query): loại foreign khỏi MỌI nguồn (topo/env/alias/
  registry) → **vá luôn LỖI TIỀM ẨN**: trước đây vbqppl reconcile/cross có thể rò sang notebook profile-khác nếu
  registry có overflow row trên đó (dogfood: wrapper nay chỉ trả `[45739ff7]` = shard vbqppl thật, loại 80742228).
- TDD **r112 ×4** negative-input (foreign helper; topology loại foreign GIỮ genuine-undeclared; findings skip foreign;
  wrapper loại foreign). Selftest **936→940/940**. I11: stub `_foreign_profile_notebooks` vào `_STUB_MAP`.
- ★KHÔNG đụng 92 dòng dual-registered (hợp lệ theo user); corpus-count không đổi.

# ★ v1.34.50 — hoàn tất BUG1 reconcile-note "SẠCH" oan (smoke v1.34.49 bắt) + data-op row_kind drift (2026-07-15)

> Smoke read-only v1.34.49 (sau `nlm login`) tự bắt 2 việc: (1) `nlm-reconcile --all-notebooks` báo "mọi notebook
> SẠCH" oan trong khi overflow desync=1 — lớp "sai mà báo thành công"; (2) 17 dòng registry lệch row_kind theo
> topology (F-06 tồn đọng). Python-only, KHÔNG đụng GAS live (EXPECT giữ 2.21.2k).

- **BUG1 hoàn tất** (`nlm_ops._reconcile_sweep_note`): v1.34.42 vá nhánh `ok=false` nhưng vẫn TIN `all_ok`; DRY
  reconcile luôn trả `ok:true` → `desync>0` với `rc=0` VẪN bị gọi "SẠCH". Nay tách `_reconcile_sweep_problems`
  (PURE) + `_reconcile_sweep_clean`; note TỰ soi finding từ `per_notebook` (KHÔNG tin cờ `all_ok`), thêm khoá
  MÁY `clean` vào output `--all-notebooks` (orchestrator kiểm `clean` không chỉ `ok`; `ok`=scan-chạy-được giữ rc=0
  theo doctrine A3, `clean`=không-lệch). Dogfood live: overflow desync=1 nay note "CÓ VẤN ĐỀ — chưa đồng bộ:
  …(desync_real=1, link_candidates=1)", `clean:false`. +r111 ×3 negative-input (936/936). ★Bẫy I11 lặp: hằng
  module `_RECONCILE_FINDING_KEYS` không vào globals tl rebase → NameError → INLINE tuple trong hàm (không dùng
  hằng module).
- **Data-op row_kind cleanup** (registry live, journaled + verified per-row qua `_journaled_reg_upsert`; KHÔNG đổi
  code): sửa **12 dòng** lệch bất biến notebook↔row_kind trên SHARD VBQPPL DECLARED — 11 nguồn trên VBQPPL-2 mang
  `own` → `overflow`, 1 dòng (21-VBHN-VPQH Bộ luật TTDS) trên base mang `overflow` → `own`. **OK=12 FAIL=0**
  (journal `rowkind-drift-fix-v13450_…7188`). ★BÀI HỌC: doctor đọc MANIFEST — sau `reconcile` self-heal refresh,
  finding phình 13→70 GỒM NHIỄU: 3 điều ước (WCT/TRIPS/WIPO) registry ĐÃ `overflow` đúng (manifest stale nói `own`)
  + 55 dòng Xuất bản notebook `80742228` (corpus=false) lọt manifest scan của base. **Xác minh authoritative qua
  `reg_get refresh=true` TRƯỚC ghi**, lọc CHỈ shard declared → đúng 12 dòng thật. Sau data-op: drift vbqppl = 0.
- **CÒN MỞ (backlog, cần user quyết — KHÔNG đụng):** (1) 55 dòng notebook `80742228` (profile "Khảo sát Luật Xuất
  bản", corpus=false) hiện trong base manifest scan → câu hỏi SCOPING (base registry chứa row profile khác?);
  (2) `_topology_row_kind_findings` khi chạy base-scope FLAG nhầm row profile-lạ thành overflow drift (report-only,
  vô hại) — refinement: chỉ tin shard DECLARED, notebook lạ → UNKNOWN. Cả hai chờ quyết định corpus của user.

# ★ v1.34.49 — ĐỢT 1 audit overflow-sharding: topology declared+observed, allocator đa-shard, fail-closed live-count (2026-07-15)

> Xử lý audit overflow/sharding v1.34.46 (9 finding; ý tưởng theo bundle Codex `c98321f0…a6ca` — nền v1.34.46 LỖI THỜI
> + GAS "2.21.2k" đụng độ định danh với bản live nên **code VIẾT LẠI trên canonical v1.34.48**, KHÔNG merge file).
> Grill-with-docs 7 quyết định D1–D7 user duyệt (`D:\Quốc hội\ke-hoach-overflow-sharding-v1.34.49-50-2026-07-15.md`).
> **Python-only — KHÔNG đụng GAS/webapp live (EXPECT_VERSION giữ 2.21.2k).** Đợt 50 (+GAS 2.21.2l): F-04 ingest_claim
> xuyên host, F-08 reg_get_bulk micro-batch, manifest stamp server-side, export bỏ default row_kind='own'.

- **[D5/F-03/F-09] `_resolve_shard_topology()` — resolver topology DUY NHẤT declared+observed** (nlm_ops): config
  `profiles.<p>.shards[]` (dict `{id,role,capacity,enabled,priority}` HOẶC list[str] legacy — phần tử trùng
  notebookId = PRIMARY, đúng dạng config live) hợp nhất env + registry (`row_kind=overflow`). Alias legacy
  (`notebookId`/`overflowNotebookId`/env) LỆCH declared → `TOPOLOGY_CONFIG_CONFLICT` **fail-closed đường GHI/ROUTE**;
  shard lạ trong registry khi ĐÃ declared → `enabled=false` + finding `UNDECLARED_REGISTRY_SHARD` (KHÔNG tự route).
  `_resolve_overflow_shards` thành wrapper UNION (47 call-site đọc/audit/query nâng đa-shard declared MIỄN PHÍ,
  sweep-safe kể cả khi config conflict). +`_topology_hash` (sha256 canonical — golden
  `references/golden/topology_vectors.json` adopt từ bundle, tương thích chéo GAS 2.21.2l) + `_topology_stamp`
  (topology_hash/routing_epoch/registry_digest) stamp vào `tl manifest` + `registry-map` (client-side).
- **[D3/F-02 BLOCKER] `ingest-missing` hết "sai mà báo thành công"**: allocator đa-shard plan theo live-room MỌI
  shard enabled ngay từ đầu; shard đầy giữa run (drift, `_nlm_add_capacity_error` phân biệt SHARD-FULL vs QUOTA) →
  **failover shard kế TRONG CÙNG RUN** với chính drive_id (không upload lại); cạn mọi shard → `ok=false,
  partial=true, remaining[], remaining_targets, resume_command, rc=2` (blocked upfront cũng rc=2 — **ĐỔI HÀNH VI**
  từ rc=0 'gate có chủ đích': orchestrator phải THẤY backlog chưa xử lý). Dedup live trên UNION mọi shard (F-04
  read-side — nguồn nằm shard khác hết bị add trùng); WAL fresh-verify quét union; ckpt key theo BASE + merge
  read-only ckpt legacy per-shard; `_apply_gate` cols + `row_kind` (superset).
- **[D4/F-05 HIGH] `_live_source_count()` fail-closed dùng CHUNG**: `notebook_get {ok:false}` KHÔNG BAO GIỜ thành
  0 nguồn/phantom-room (mẫu slot-audit M2 nâng thành helper). Đường GHI (ingest-missing, `_ingest_target`): fail →
  self-heal `load_creds` ĐÚNG 1 lần/run (doctrine v1.34.43) → vẫn fail → `LIVE_READ_FAILED` rc=2 ZERO side-effect.
  Đường ĐỌC (preflight L5, overflow-resolve): `live_read_failed=true`, không suy 0. `_ingest_target` nay duyệt MỌI
  shard overflow topology (không chỉ 1 overflow đơn).
- **[F-06 HIGH] row_kind SUY TỪ TOPOLOGY trên mọi đường recovery/link**: `nlm-reconcile --apply`
  (backfill+link_candidates, tách 2 write) + `nlm-add` auto-link nay ghi `row_kind='overflow'` khi notebook đích là
  shard overflow — **kind bảo hộ `ref`/`thuong` KHÔNG BAO GIỜ clobber** (`_ROW_KIND_PROTECTED`; primary giữ blank=own,
  tránh churn). +doctor invariant REPORT-ONLY (`_topology_row_kind_findings`: PRIMARY_ROW_MARKED_OVERFLOW /
  OVERFLOW_ROW_NOT_MARKED_OVERFLOW / UNKNOWN_NOTEBOOK_NOT_IN_TOPOLOGY) + payload `topology` + liveness shard
  overflow (advisory, minor handoff #1).
- **[D6/F-07] capacity hết hard-code 300**: ưu tiên `shards[].capacity` > env `TL_NLM_SOURCE_CAP` > default 300
  (`NLM_SLOT_CAP` giữ làm default + mirror-lock). `slot-audit --all-shards` phủ shard DECLARED chưa có dòng registry
  (count=0 — VBQPPL-3 mới duyệt hiện ngay) + cap per-shard + topology findings.
- **[minor handoff #2] `push-overflow` validate `--notebook-id` ∈ topology overflow** → `TARGET_NOT_IN_TOPOLOGY`
  rc=2 TRƯỚC gate/ghi (bootstrap chưa biết shard nào → cho qua + cảnh báo; ép: `--force-unsafe`). `registry-map`
  hết bỏ `shards[]` sau overflow đầu tiên (bản đồ N-shard thật) + topology view/hash.
- **TDD r110 ×18** (RED trước — 8 probe harness Codex chuyển thể + negative-input): 3-shard thấy đủ ở
  reconcile/map/audit; failover/partial/authfail/drift của ingest-missing; alias conflict; capacity precedence;
  golden topology-hash; reconcile không clobber `ref`; push-overflow chặn ngoài topology. Selftest **915→933/933**.
  ★Fake `notebook_get` thiếu key `ok` (contract thật LUÔN có) được hiện đại hoá; test đụng resolver phải HERMETIC
  (`_read_config_record` patch) — resolver nay đọc config-of-record thật.
- ★Bẫy I11 lặp lại đúng kịch bản: hằng `_ROW_KIND_PROTECTED` mới phải re-export TRỰC TIẾP ở tl.py (hàm rebase đọc
  globals tl); 8 hàm mới vào `_STUB_MAP` (note CUỐI dòng).

# ★ v1.34.48 — GAS 2.21.2k: doNlmPreflight_ đếm slot SHARD OVERFLOW trước khi route (2026-07-14)

> Đóng backlog webapp của audit v1.34.46 (server-side defense-in-depth; client v1.34.47 đã fail-closed).

- **GAS `doNlmPreflight_` (Code.2.21.2k.gs)**: khi route overflow (base đầy/gần-đầy + overflow cấu hình), nay gọi
  `doNlmSlots_` cho CHÍNH shard overflow → trả `overflow_slots` + `overflow_route.{slots,has_room,full}`. Base+overflow
  ĐỀU đầy → reason `ALL_SHARDS_FULL_ASK_USER` (GIỮ decision=REVIEW: hỏi user duyệt shard mới, KHÔNG khuyên add vào
  shard đầy). Trước 2.21.2j chỉ đếm base rồi route overflow MÙ.
- Bump webapp **2.21.2j → 2.21.2k**: rename `Code.2.21.2j.gs`→`Code.2.21.2k.gs`, APP_VERSION, EXPECT_VERSION (tl.py +
  selftest literal), API_CONTRACT (stamp + doc field mới), SKILL/RUNBOOK 17 chỗ, webapp_target manifest.
- **⚠ CẦN DEPLOY GAS THỦ CÔNG (skill KHÔNG deploy được):** mở `references/Code.2.21.2k.gs` → Apps Script → New
  version (giữ URL+token) → `tl ping` phải ra `2.21.2k` → `contract_check.py --audit`. EXPECT_VERSION đã = 2.21.2k
  nên `tl ping` sẽ báo LỆCH tới khi deploy — deploy CÙNG NGÀY. **⚠ SKILL.md kernel đổi ⇒ RE-IMPORT.**

# ★ v1.34.47 — vá bất nhất shard overflow (VBQPPL-2) + đóng 3 dư release verifier (2026-07-14)

> Canonical audit v1.34.46 (adopt verifier F-01..F-05) + rà sâu shard overflow (yêu cầu user). Gốc rễ mọi lỗi
> overflow nặng: đường GHI/ĐỊNH-TUYẾN auto-discover shard từ registry khi config trống, nhưng đường ĐỌC/AUDIT/QUERY
> chỉ đọc env → config trống ⇒ BỎ shard. Vá bằng một `_resolve_overflow_shards()` DÙNG CHUNG (env + registry, đa-shard).

- **[BLOCKER] `nlm-reconcile --all-notebooks` báo "mọi notebook SẠCH" oan** khi config overflow trống (chỉ quét base,
  bỏ shard chưa quét — "sai mà báo thành công"). Nay quét đủ shard registry-biết qua `_resolve_overflow_shards`.
- **[MAJOR] `ingest-local` (single-file) route overflow khi base đầy mà KHÔNG check overflow-room** → both-full thì
  add vào shard đầy SAU side-effect. Nay `_ingest_target` tính overflow_room LIVE + `_overflow_route` fail-closed
  (both-full → BLOCKED trước upload/register, KHÔNG auto-create) — khớp batch `ingest-missing`. +guard placeholder.
- **[MAJOR] `nlm-cross` bỏ overflow cho profile DEFAULT** khi config trống (block `_base_also_enabled`=False). Nay
  LUÔN nối shard overflow của scope từ registry. `nlm-query` thêm cảnh báo dùng `nlm-cross` khi corpus đã sharded.
- **[MODERATE] `slot-audit --all-shards` under-count base**: dòng blank-nlm_notebook_id nay quy về base (khớp
  `_nlm_slot_count`) → cảnh báo base gần-đầy không còn kích trễ. `_resolve_overflow_shards` đa-shard (không chỉ 1).
- **Release verifier 3 dư (v1.34.46 audit):** `release-bundle --top a/b` (separator) nay bị từ chối; `release-verify`
  bắt 2 root khác-hoa (ROOT_NOT_SINGLE); repro-rebuild lỗi dọn CẢ tmp chính (hết rò + hết propagate uncaught).
- Test: +4 r109 (resolve-overflow env+registry, slot fold, ingest-target blocked both-full, top-separator). selftest
  **915/915**, golden 18/18, workflow/determinism strict. **⚠ SKILL.md kernel đổi (version + release gate) ⇒ RE-IMPORT.**
  GAS `doNlmPreflight_` (đếm slot overflow trước route) = backlog webapp riêng (chưa bump GAS).

# ★ v1.34.46 — kết hợp hậu kiểm v1.34.45 + đóng kín release archive verifier (2026-07-14)

- Lấy ZIP v1.34.45 hậu kiểm làm nền vì giữ nguyên 143/162 tệp và bổ sung đúng các vá Windows lock, SSRF/HTTPS-default, golden location/cross-platform, archive verification, cache conflict và tài liệu hợp đồng apply.
- Negative test độc lập phát hiện `release-verify --archive` vẫn false-pass ba dạng ZIP không canonical: entry trùng, metadata ngoài root và `RELEASE_MANIFEST.json` nhúng bị thay nội dung. Verifier mới duyệt một lượt O(n), chặn duplicate Unicode/casefold, path/root không portable, directory/special entry, metadata ZIP không cố định, size/SHA lệch và manifest/BUNDLE_META không khớp.
- `release-bundle --top` từ chối `.`/`..`, tên Windows reserved, trailing dot/space, ký tự cấm và Unicode không NFC. Bundle chỉ được publish ra `--out` sau khi hai build tạm cho cùng SHA-256; gate thất bại không ghi đè gói hợp lệ cũ.
- Thêm 4 negative tests r108 cho duplicate/root-meta/manifest-binding/top-portability; giữ một lượt hash/member và không thêm chi phí vào ingest file/local/ZIP runtime.

# ★ v1.34.45 — hardening ingest/local/cache/ZIP + determinism (2026-07-14)

- Mọi đường ingest ghi ra Drive/registry/NLM nay fail-closed: `ok` thiếu/rỗng không còn được coi là thành công; readback sai dừng pipeline. Lệnh `ingest` cũ chỉ còn là adapter sang engine `ingest-local` chung.
- Thêm hợp đồng `plan → --confirm yes → --expected-plan-hash`: plan gắn với SHA-256 byte nguồn, đích và tùy chọn; resume chỉ dùng journal cùng identity/plan.
- Ingest local/Drive/URL xác minh extension + magic + cấu trúc container DOCX/XLSX/ODT, giới hạn byte/timeout/redirect, cleanup temp. Host allowlist không hard-code: môi trường có thể cấp `TL_SOURCE_ALLOW_HOSTS`, `TL_SOURCE_SCHEMES`, `TL_SOURCE_MAX_BYTES`, `TL_SOURCE_TIMEOUT_S`.
- Cache vá đúng `doc_key` vừa normalize (không quét/chọn theo tên hay bản mới nhất), ghi atomic, staged/verified có quality checks, lock theo identity và tự thu hồi lock bị bỏ lại.
- ZIP chặn traversal, tên reserved/trailing-dot-space, symlink/special entry, collision Unicode/casefold, zip bomb theo tổng size/tỉ lệ nén; apply bị khóa bởi archive SHA-256 + member SHA-256; mặc định 4 worker (trần cứng 8), xử lý MỌI member rồi báo `counts{applied,failed}`+`partial` (ok=all).
- JSON deterministic không còn tự thay giá trị nghiệp vụ; audit dùng projection khai báo field volatile/path. Release ZIP dùng `ZIP_STORED` + metadata cố định; package/content/archive hash đều được verify fail-closed.
- Kiểm thử: selftest 900/900, golden 18/18, workflow strict và determinism strict đều đạt. Benchmark dry-run ZIP 10,49 MB: +1,09% end-to-end; cache 1.000 record: 275,4 ms → 6,58 ms.

> **MERGE-REVIEW canonical (ADR-0001) — bản audit v1.34.45 do phiên song song (Codex) giao, review + vá TRƯỚC merge.**
> Provenance sạch (zip khớp SHA byte-for-byte; baseline = LIVE v1.34.44). Gate offline chạy lại đạt. Review 6-chiều
> read-only + adversarial verify bắt và VÁ tại canonical trước khi merge:
> - **[BLOCKER gate] golden ingest-zip dryrun** nhúng path tuyệt đối (`PATHISH_KEYS` thiếu khóa `"zip"`) → golden-test
>   ĐỎ ngoài thư mục capture → thêm `"zip"` vào PATHISH_KEYS + regen 2 golden (đã kiểm chứng location-independent).
> - **[MAJOR] lock cache Windows**: `_pid_alive` dùng `os.kill(pid,0)` (=CTRL_C_EVENT trên Windows) → không phá được
>   lock chủ-chết → kẹt ingest tới stale_s → thêm nhánh `_pid_alive_windows` (OpenProcess+GetExitCodeProcess, mặc định
>   "sống" khi bất định).
> - **[MAJOR] ingest-zip `--continue-on-error`** thành no-op + mất fail-fast: chốt ngữ nghĩa "xử lý mọi member rồi báo
>   partial", thêm `counts`+`partial` vào output, sửa help cờ + doc cho trung thực (KHÔNG khôi phục fail-fast).
> - **[MODERATE] SSRF**: thêm lọc địa-chỉ (chặn IP non-global/loopback/RFC1918/link-local) trên đường fetch URL tùy ý
>   (`TL_SOURCE_ALLOW_PRIVATE=1` để opt-out); **http phẳng**: `TL_SOURCE_SCHEMES` mặc định chỉ `https` (http phải opt-in).
> - **[MODERATE] release-verify không kiểm archive**: `--archive`/`--expected-archive-sha256` mở .zip đối chiếu từng
>   member vs manifest + đường-dẫn-an-toàn; `release-bundle` build ×2 yêu cầu cùng SHA-256 (gate ADR-0007).
> - **[MODERATE] find() ném traceback thô**: `tra_cuu` bắt `CACHE_IDENTITY_CONFLICT` → thoát sạch rc=2 (không đoán nguyên văn).
> - **[MODERATE] doc/kernel**: SKILL.md + COMMANDS.md phản ánh hợp đồng apply fail-closed + `reg-delete --confirm yes` +
>   ingest-zip. **⚠ SKILL.md kernel đổi ⇒ USER CẦN RE-IMPORT Capabilities.** Minor: gỡ VERSION gán trùng ở tl.py; PDF magic nhận BOM.

# ★ v1.34.44 — MERGE bundle audit-profile từ phiên song song (ADR-0001) (2026-07-14)

> Phiên song song (Codex) audit v1.34.43 trọng tâm PROFILE, giao bundle 16 fix P-01..P-16 + báo cáo + patch.
> Canonical review theo đúng nếp ADR-0001 TRƯỚC khi merge: workflow 6 reviewer read-only song song
> (profile_env / profile_mgmt / tl+live / selftest / docs-kernel / security+claims-check) + adversarial verify
> → **0 blocker, 0 major; 16/16 claim có code tương ứng; security sạch (0 mạng mới/exec/eval, guards SIẾT thêm,
> bỏ candidate ghi /tmp); bẫy I11 xử đúng; r104/r105 nguyên vẹn.**
>
> Nội dung merge: **(P-01..05)** cách ly scope/config profile — block rỗng không kế thừa vbqppl, malformed
> fail-closed, env-switch xóa scope stale (fix tận gốc họ hàng bài học scope-leak 2026-07-13), cache path slug
> an toàn Windows + chống traversal, mutation ghi ĐÚNG file config đã đọc; **(P-06..11)** giao dịch danh tính
> profile — marker-first cho create/adopt/promote/from-nlm, rename cập nhật marker + rollback config,
> duplicate-marker detection, sync/backfill hết false-success (unresolved tường minh), delete giữ config khi
> remote lỗi một phần; **(P-12..14)** PermissionError→data ở đường report-only, selftest hermetic
> (TL_CACHE_DIR tạm — hết đụng cache thật), `tl_selftest.py` chạy trực tiếp được, bundle-export
> credential-lazy; **(P-15..16)** docs sync (ADR-0003 key marker `schema`/`profile` đúng code; SKILL.md mục 9
> liệt kê đủ lệnh ghi marker + detach semantics; COMMANDS.md) + `agents/openai.yaml` (metadata hiển thị; file
> inert — không code nào đọc). **+12 test r106** → selftest 874→**886**.
>
> Hành vi biên đổi CÓ CHỦ ĐÍCH (đã review, ghi nhận): (a) `--config` trỏ file KHÔNG tồn tại không còn là đích
> ghi authoritative — rơi về config phát hiện được (nhất quán read=write); (b) config implicit rỗng `{}` →
> CONFIG_WRITE_FAILED thay vì ghi đè. Promote sau-timeout vẫn re-run được (exact-match đi thẳng);
> `_nlm_system_prompt_apply` không đổi; ops-sweep B4 parse không vỡ.
> Kernel SKILL.md đổi (1 câu mục 9 + header version) ⇒ theo deploy policy: **nhắc user re-import Capabilities**.

# ★ v1.34.43 — hoàn tất BUG2 cho `nlm-reconcile --refresh` (ops-sweep dogfood bắt gap) (2026-07-14)

> Ngay sau v1.34.42, chạy `ops-sweep` (L1) → **warn 2**: `nlm-reconcile --profile "Luật BHXH" --refresh` chết
> rc=2 "Thiếu TL_WEBAPP". Chẩn đoán: BUG2 v1.34.42 (load_creds-on-refresh) tôi CHỈ vá `reg-query`, **bỏ sót
> `nlm-reconcile`** — cùng lớp gap (`locate`/`status`/`reg-query` đều gọi load_creds khi refresh; nlm-reconcile
> không). File `~/.tra_luat_config.json` xóa phiên trước làm lộ ra (trước nằm trong candidate-path mặc định nên che).
> **Vá:** `cmd_nlm_reconcile` nạp `load_creds` ở ĐẦU hàm khi `--refresh` (phủ cả plain lẫn `--all-notebooks`;
> TL_WEBAPP cho GAS/registry, NLM cookie riêng); gỡ bản load_creds trùng trong nhánh --all-notebooks (giữ
> self-heal `_manifest_entries`). **TDD r105** (negative-input: stub `_resolve_nlm_notebook` early-exit SAU load_creds
> → assert load_creds được gọi + rc=2). Verify LIVE: `nlm-reconcile --refresh` fresh (không boot) → ok=true, 41 nguồn,
> hết "Thiếu TL_WEBAPP". Selftest 873→**874**. KHÔNG bump GAS/kernel → re-import không bắt buộc.
> **DATA-OP kèm:** adopt marker profile **"Khảo sát Luật Xuất bản"** (130 items, registry+manifest đầy đủ, phiên
> khác tạo) vào config local qua `profile-sync --apply` (ADR-0003 marker→config một chiều) — clear warn 1 ops-sweep.

# ★ v1.34.42 — vá 3 bug audit-tool phát hiện khi chạy thật (data-op + audit corpus 2026-07-13)

> Nguồn: phiên Pha 5 (backfill sohieu/loai) + audit corpus 15 profile bắt 3 trục trặc CỦA CHÍNH CÔNG CỤ audit.
> Grill-with-docs chốt phương án (BUG3 A vs B; BUG1 tối thiểu vs sâu). TDD r104 ×4 negative-input (luật đứng v1.34.40).
> **Xác minh code TRƯỚC khi kết luận — loại 2 nghi vấn oan** (manifest `so_hieu`/`id` vs registry `sohieu`/`drive_id`:
> có helper `_entry_sohieu`/`_entry_drive_id` phủ, lỗi script audit của tôi; infra tự-đăng-ký: guard `_is_infra_file`
> ĐÃ CÓ, 2 dòng BHXH là legacy đã reg-delete). Không bump GAS/kernel → re-import không bắt buộc.

- **(BUG1 — lớp 'sai mà báo thành công') `nlm-reconcile --all-notebooks`**: dòng `note` trước là CHUỖI CỨNG "mọi
  notebook sạch" in KỂ CẢ khi `ok=false`; rc=2 (thiếu cache/scope) in ra stderr → `_r_i={}` → `per_notebook` NUỐT lý
  do. Chính công cụ audit tự báo sai. Vá: (a) `_reconcile_sweep_note(all_ok, per_notebook)` PURE — note ĐIỀU KIỆN
  (liệt kê notebook rc≠0/finding + hướng dẫn boot/per-notebook); (b) upfront `load_creds` + `_manifest_entries()`
  MỘT LẦN trước vòng lặp: self-heal khi có creds (config), báo `NEEDS_BOOT_PROFILE` rõ khi không — thay vì lặp rc=2
  im lặng. Live-smoke: xóa cache ISO → --all-notebooks tự nạp+build cache → reconcile thật ok:true (không note oan).
- **(BUG2) `reg-query --refresh` chết "Thiếu TL_WEBAPP" gây tưởng MẤT token**: `cmd_reg_query` chỉ gọi
  `apply_profile_offline` (creds offline — không đảm bảo TL_WEBAPP) rồi `_manifest_entries(refresh=True)` cần LIVE.
  `locate`/`status` ĐỀU gọi `load_creds` trước refresh — reg-query thiếu. Vá: gọi `load_creds` khi `--refresh`
  (self-heal từ config) + thông điệp lỗi refresh cụ thể (chỉ `tl boot --refresh`). Live: xóa manifest → --refresh
  rc=0, JSON hợp lệ, hết lỗi creds.
- **(BUG3) `reg-query --corpus true` literal ≠ luật corpus server → audit sai lệch**: filter cũ chỉ khớp
  `corpus=='true'` (bỏ sót vbqppl/overflow → base 486 vs `tl boot` 521). Vá: `_entry_is_corpus_effective(e)` PURE
  (tách từ `_corpus_count_server_rule`: corpus∈{true,vbqppl}∪overflow − ref − thuong) + cờ `--corpus-effective`
  (base KHỚP boot 521) + cảnh báo `--corpus true` là literal. **Live-smoke BẮT giới hạn**: luật server CHỈ đúng scope
  NỀN vbqppl — profile đếm khác (server: mọi dòng có drive_id); ca Luật BHXH 14 dòng corpus=true đều `row_kind=ref`
  → effective=0 → **cảnh báo khi --corpus-effective dùng trên profile** (không chặn).

# ★ v1.34.41 — B.2 GĐ2: sửa TẬN GỐC `_classify_doc_header` nhận diện văn kiện ĐẢNG + VB HÀNH CHÍNH (2026-07-13)

> Đóng backlog "Giai đoạn 2" của v1.34.40 B.2. Grill 9 quyết định D1-D9 (user duyệt) trên fixture CA THẬT
> Pha 0 (3 văn kiện Đảng cat 00 + HD 09-HD/VPTW + TB/KH/TTr/CTr profile Chỉ thị). TDD **r103 ×15** (kèm
> negative-input theo luật đứng); **harness file thật bắt 2 bug mà fixture rút gọn che** → 2 vòng đỏ-vá thêm.
> Kế hoạch + kết quả grill: `D:\Quốc hội\ke-hoach-B2-giai-doan-2-classify-doc-header-2026-07-13.md` (ngoài repo).

- **(D2+G4) `kind` mới `dang` + `hanhchinh`** — nhận diện TRƯỚC nhánh vbqppl (không thì sohieu Đảng vừa bắt
  được kích `elif sohieu` → vbqppl → Điều-gate chặn oan cat 00); cả hai KHÔNG đòi cấu trúc Điều kể cả corpus
  nền (info-flag `DANG_DOC_DIEU_NOT_REQUIRED`/`HANHCHINH_…`); `dang` thắng cả `draft` (văn kiện Đảng không
  bao giờ đòi Điều — cờ draft giữ ở field riêng). Consumer kind duy nhất = Điều-gate (khảo sát Pha 0) → additive-safe.
- **(D3) `_is_dang_title_zone` (PURE)**: dang khi BẤT KỲ 1/3 tín hiệu TRONG TITLE-ZONE 1500 — (a) dòng mở đầu
  banner 'ĐẢNG CỘNG SẢN VIỆT NAM' (không quốc hiệu CHXHCN trong zone); (b) sohieu dạng Đảng …/TW|VPTW|TU*|ĐU*;
  (c) cơ quan Đảng (BCH TW/Bộ Chính trị/Ban Bí thư/VPTW/BCĐ TW/đảng-tỉnh-thành ủy). Nhắc trong câu văn KHÔNG tính (N2b).
- **(D1) `_SOHIEU_NOYEAR_RE` RIÊNG** (không đụng `_RAW_SOHIEU_RE` dùng chung — 'Bao_cao_2024-2025' không bao giờ
  thành sohieu): số Đảng `NN-XX/CQ` (04-CT/TW; Đđ trong mã CQ — ca 20-TB/CQTTBCĐ) + hành chính `NN/XX-CQ`
  (123/BC-UBND), CHỈ trong `_sohieu_from_title_zone`, CHỈ dòng ≤80 có pre-text **'Số'/'Số:' THUẦN (fullmatch)**.
  ★Harness file thật QĐ 383 bắt: pre-text dạng-CÓ-NĂM cũng phải siết fullmatch `[loại] số:` — check ends-with cũ
  dính trích dẫn ngắn '- Căn cứ Luật Lưu trữ số 33/2024/QH15, ngày…' (≤80, kết bằng 'số') CƯỚP sohieu; thứ tự mới:
  năm-letterhead > không-năm-letterhead > best-trôi-nổi.
- **(D4) loai LETTERHEAD-FIRST toàn cục**: `_declared_loai_from_header` (ruột văn bản) > prefix tên file >
  mã sohieu — ca thật QĐ 383-QĐ/TW file `QD_` nói 'Quyết định', letterhead nói 'QUY ĐỊNH' → Quy định thắng
  (gốc ca HD 09-HD/VPTW bị filename-first đoán 'Luật'). VBHN-override giữ trên cùng. ★Harness VBHN 19 BHXH bắt:
  layout VPQH KHÔNG banner 'VĂN BẢN HỢP NHẤT' → declared 'LUẬT' đè mất suy-VBHN-từ-sohieu → `_is_vbhn_doc`
  +suy THẲNG từ dạng số hiệu (mã VBHN đứng riêng / NN/VPQH bare; KHÔNG substring 'VPQH' trần — NQ-VPQH là VB thường);
  nhánh hanhchinh loại trừ VBHN (NN/VBHN-VPQH cũng khớp shape NN/XX-CQ).
- **(G3) fallback 'nghi quyet'/'du thao…luat' thu về TITLE-ZONE 1500 + tên file** (trước quét cả 16k — tài liệu
  nhắc nghị quyết sâu trong thân bị nhuộm loai='Nghị quyết').
- **(D5) sohieu_key YEAR-QUALIFIED `NN-YYYY-XX-TW`** cho dang/hanhchinh (năm từ issue_date — số Đảng KHÔNG năm,
  tái dùng qua khóa = cùng lớp collision VBHN, bất biến phải-có-năm); sohieu NGUYÊN VĂN giữ field riêng.
  **`_dang_bare_key`** (khuôn `_vbhn_bare_key` y hệt, loại trừ khóa VBHN) + `_sohieu_query_hits_entry` nới
  1 CHIỀU: query bare '04-CT-TW' khớp entry year-qualified mọi năm; query có năm giữ so CHẶT.
- **(D8) `_LOAI_CANON` +5 loại hệ Đảng**: Quy định / Chương trình / Quy chế / Điều lệ / Thông tri (+alias không-dấu;
  'qd' GIỮ = Quyết định — QĐ/TW mơ hồ không letterhead → blank-over-guess để trống). `_DECLARED_LOAI_MAP` +5 tương ứng.
- **(D6) `_HEADER_AGENCY_PATS` +9**: BCH TW→TW, Bộ Chính trị→BCT, Ban Bí thư→BBT, VPTW, BCĐTW, đảng ủy→DU,
  tỉnh/thành ủy→TU, UBND, HĐND (nhóm Đảng đứng trước — đặc thù hơn; dài-trước-ngắn giữ).
- **(D7) `_safe_profile_doc_name` +18 mã loại** theo quy ước SỐNG trên corpus (CT/KL/HD/KH/TB/CV/TTr/DA/BC/PB/
  CTr/Mau/CD/TL + Phụ lục=PL chung sống Pháp lệnh + Quy định=QDi/Quy chế=QC/Thông tri=TTri/Điều lệ=DL);
  **năm BẮT BUỘC trong tên khi sohieu_key không năm** (khớp tên thật KL_121-KL-TW_2025). `_infer_loai` +CTr_
  (đã sống trên corpus; QDi/QC/TTri/DL chưa gặp tên thật — gặp thật mới thêm).
- **Verify**: selftest 869/869 (854 cũ + r103 ×15 — control r52/r73a/r100-102 xanh NGUYÊN, không sửa expectation);
  harness 8 file Đảng/hành chính THẬT + 6 control VBQPPL/VBHN thật đều đúng. KHÔNG bump GAS/kernel doctrine
  (chỉ version header) → re-import KHÔNG bắt buộc. Data-op backfill (sohieu/loai 121 dòng cũ + KL_121 dup 2 drive_id +
  QĐ 383 loai 'Quyết định'→'Quy định' + 2 loai sai profile Chỉ thị) = Pha 5 riêng, DRY trước, chờ user duyệt.

# ★ v1.34.40 — vá 7 lỗi BÁO CÁO 13/7 (lớp "sai mà báo thành công") + LUẬT negative-input test (2026-07-13)

> grill-with-docs chốt 7 quyết định thiết kế; TDD **r102 ×10 NEGATIVE-INPUT tests** (đầu vào sai cố ý →
> bắt buộc fail rõ) — fixture mô phỏng CHÍNH các ca thật trong `BAO_CAO_LOI_SKILL_v1.34.38.md`.

- **(A.1 🔴) `extract` hết TRẢ SAI VĂN BẢN im lặng** (ca PL01 → Công văn 386, rc=0 + cache bẩn): positional
  dạng-ID → **export THẲNG, id thật LUÔN thắng** (bỏ deep-resolve-trước-export từng coi id hợp lệ như query
  fuzzy rồi GHI ĐÈ); trước export chỉ tra EXACT drive_id trong manifest lấy metadata (draft-warning + cache
  sohieu — exact-match tất định). Ca tên-giống-id (false-404 v70) giữ nguyên đường sống: export trả
  **NOT_FOUND** (phân biệt với lỗi auth/mạng — các lỗi khác KHÔNG resolve) → deep-resolve fallback MỘT lần
  + in canonical + retry. Bỏ `except: pass` → cảnh báo stderr.
- **(A.2 🔴) `register --clear-cols` + field set → rc=2 TỪ CHỐI** kèm hướng dẫn "2 lệnh riêng" (trước: VỨT
  LẶNG LẼ mọi `--loai/--title-vn/…` mà vẫn báo `verified:true`). Không ghi gì khi từ chối.
- **(A.3 🔴) `ocr-verify` hết PASS với đầu vào rác**: input parse được thành JSON (nhất là schema
  `ocr_manifest`) → rc=2 + gợi ý file `.ocr.txt` đúng (từng đo file manifest JSON như text tiếng Việt rồi
  PASS); **manifest-missing → ok=false rc=2 MẶC ĐỊNH** (không manifest = không đối chiếu được hash = chưa
  verify gì); cờ mới `--no-manifest` opt-in cho đo-chất-lượng-thô cố ý (text tự extract không qua ocr-run).
- **(B.1) `slot-audit` hết mâu thuẫn `nlm-reconcile` + hết xúi lệnh ghi trên gap sai**: `slots_effective`
  skip `row_kind=ref` by-design nhưng ref ĐÃ nlm-add nên chiếm slot vật lý thật → tách 3 số
  `registry_estimate` / `ref_rows` / `nlm_claim_rows` (đồng định nghĩa reconcile); `gap` tính trên claim;
  gợi ý `backfill-notebook` CHỈ khi gap còn lại sau khi trừ ref ≠ 0 (helper PURE `_nlm_ref_slot_count`).
- **(B.2) BLANK-OVER-GUESS metadata cho profile văn bản thường** (ca HD 09-HD/VPTW bị đoán kind=vbqppl,
  loai='Luật', ghi thẳng registry): profile ≠ vbqppl chỉ persist `loai` có bằng chứng TƯỜNG MINH — (a) cờ
  `--loai`, (b) letterhead khai báo (`_declared_loai_from_header` — **+12 loại VB thường**), (c) prefix tên
  (`_infer_loai` — **+7 prefix KH_/TB_/CV_/TTR_/DA_/BC_/PHU_LUC, prefix-only** không đụng VK_ dị thể r93);
  heuristic thân-văn-bản → ĐỂ TRỐNG + hướng dẫn điền (helper PURE `_profile_loai_evidence`). Corpus nền
  vbqppl KHÔNG qua gate. **Giai đoạn 2 (sửa tận gốc bộ suy `_classify_doc_header`) = backlog có kế hoạch.**
- **(B.3) `profile-ingest-chunks --apply` STREAM tiến độ**: `[chunks] (i/n)` + JSONL per-chunk ra stderr +
  `resume_command` khi đứt giữa chừng (khuôn profile-doctor --deep v1.34.30) — 9 chunk >600s từng buffer
  đến cuối, timeout tưởng thất bại dù 9/9 đã lên Drive.
- **(C.1) `by_heading` REDESIGN (lỗi mới từ bản vá 1.34.38)**: heading CẤP CAO NHẤT xuất hiện (PHẦN >
  Chương > Mục) **không bao giờ gộp** — 1 section = 1 chunk (Phần V hết bị nuốt vào chunk IV); section vượt
  `max-chars` → **tách CON đệ quy** theo heading cấp dưới (Chương/Mục/numbered `1.`/`1.1.`), cấp dưới gộp
  liên tiếp theo budget; hết cấp → cắt paragraph-budget title `X (i/n)`; mọi mảnh từ section vượt mang flag
  **`CHUNK_SPLIT_OVER_BUDGET`** (chunk 191k từng lọt qua max 90k im lặng, phải tách tay).
- **★LUẬT ĐỨNG MỚI (từ báo cáo — 3 lỗi Đỏ cùng khuôn "thao tác thất bại nhưng trả tín hiệu thành công"):**
  lệnh ghi/verify MỚI phải kèm **≥1 negative-input test** (đầu vào sai cố ý: sai file/sai id/sai kết hợp cờ
  → bắt buộc fail rõ ràng, không im lặng). Ghi tại đây + memory; bộ r102 là mẫu khuôn.
- D.1 (nhãn lỗi `nlm login --check`) = upstream nlm CLI, watchlist. r102 ×10 + parser-surface regen
  (ocr-verify +--no-manifest) → **854/854**. KHÔNG bump GAS, KHÔNG đổi kernel → re-import KHÔNG bắt buộc.

---

# ★ v1.34.39 — vá heuristic `_cat_likely_wrong` pin-từ-khóa: 12/20 FP corpus-audit 2026-07-13 (2026-07-13)

> TDD r101 ×9 — fixture = CHÍNH các ca thật từ audit; 3 control giữ true-positive.

- **(A) Pin `dân tộc = 10` né TÊN CƠ QUAN:** lookbehind `(?<!hoi dong )` — "Hội đồng Dân tộc" là cơ quan
  Quốc hội (tổ chức bộ máy 35), không phải chính sách dân tộc (ca thật: NQ_71-2025-UBTVQH15 về nhiệm vụ/cơ
  cấu HĐDT bị đề xuất 35→10). "Công tác/chính sách dân tộc" thật vẫn pin bình thường.
- **(B) `_CAT_KEYWORDS["19"]` gỡ `tieu_chuan` TRẦN** (va chạm "tiêu chuẩn sức khỏe/chức danh nghề nghiệp" —
  10+ TT BYT/BQP/BCA ở cat 45 bị suy 19 GIẢ trong audit): đề mục 19 pháp điển là "Tiêu chuẩn, ĐO LƯỜNG,
  CHẤT LƯỢNG" → thay bằng cụm dài `tieu_chuan_do_luong`/`quy_chuan_ky_thuat`; `do_luong`/
  `chat_luong_san_pham` sẵn có phủ phần còn lại.
- **(C) Boundary "Luật sửa ≥2 luật → 46" hết đếm token lặp:** điều kiện cũ `count('luat') ≥ 3` chạy trên
  scope GHÉP nhiều biến thể tiêu đề của CÙNG một luật (tail + title_vn + khối tiêu đề) → văn bản sửa MỘT
  luật cũng thoả (ca thật: Luat_26-2018 TDTT + Luat_75-2025 Quảng cáo bị 41→46). Nay: helper PURE
  `_distinct_target_luat_subjects` đếm CHỦ ĐỀ PHÂN BIỆT sau token 'luat' (strip stopword sửa-đổi/bổ-sung,
  lấy 2 từ đầu để biến thể dài-ngắn gộp một) ≥ 2; + tín hiệu tường minh `cac/nhieu luat`, `sua doi N luat`.
  **+Guard đề-xuất-46 CHỈ cho Luật/Bộ luật** — NĐ/TT/QĐ sửa nhiều văn bản cùng cấp vẫn cat theo lĩnh vực
  đích (ca thật: ND_187-2025 sửa ND78+ND79 bị 44→46; rổ 46 pháp điển = "LUẬT sửa đổi, bổ sung nhiều LUẬT").
- **(D) Điều ước đang ở 23 → im:** entry là điều ước/công ước (loai hoặc prefix CU_/CPTPP_/EVFTA_) đang ở
  cat 23 → KHÔNG đề xuất tách theo chủ đề nội dung (quy ước corpus GOM MỌI ĐƯQT ở 23 — CU_ILO-168 chống
  thất nghiệp cũng 23; ca thật: CPTPP_Chuong_19_Lao_dong bị 23→20 vì alias 'lao dong').
- Control giữ nguyên: pin dân-tộc thật, omnibus thật (`Luật A, Luật B và Luật C` → 46), true-positive
  nợ công 26→28 (ca VBHN_59 đã recat đúng sáng nay). r101 ×9 → **844/844**. KHÔNG bump GAS/kernel.

---

# ★ v1.34.38 — vá 4 lỗi log phiên Chỉ thị: phuluc-gate / chunk by_heading / _LOAI_CANON / hygiene-chunk (2026-07-13)

- **(#1) Gate `PHULUC_MENTION_WITHOUT_HEADING` hết dương-tính-giả** (chặn oan corpus HD 09-HD/VPTW, PL01,
  9 chunk Đề án CĐS QH — PL01 chính LÀ phụ lục mà không được nhận): (a) heading dò trên bản STRIP-ACCENT
  (regex có-dấu cũ miss 'PHỤ LỤC 01' dạng NFD/hoa); (b) CHỈ nghi khi nhắc 'phụ lục' KÈM SỐ — văn xuôi
  'kèm theo phụ lục' không phải bằng chứng; (c) gate CHẶN corpus chỉ trên corpus NỀN vbqppl — profile văn
  bản thường hạ về info-flag `PHULUC_MENTION_PROFILE_INFO` (mirror doctrine requires_dieu v1.34.27 #2).
- **(#2) chunk-plan/chunk-apply + strategy `by_heading`** cho văn kiện Đảng/Đề án KHÔNG có cấu trúc Điều
  (trước rơi thẳng cắt mù `by_paragraph_budget`, có thể cắt giữa một Phần/Mục — phải dò tay + tự dựng
  manifest): nhận diện `PHẦN thứ-nhất/I/1` · `Chương I/1` · `Mục 1/I` đầu dòng; guard heading = dòng-trống-
  ngay-trước HOẶC kết-câu (khuôn `_is_heading` by_article); preamble (tên đề án) đi cùng chunk 1; cần ≥2
  heading. ★2 bug tự bắt khi TDD: `\s` trong pattern NUỐT newline (title dính dòng sau) → `[ \t]`; guard
  kết-câu một mình loại oan heading đứng sau đoạn không dấu chấm (bảng/số liệu).
- **(#3) `_LOAI_CANON` +10 loại văn bản thường** (log: loai_noncanonical=26/53 — gần nửa registry profile
  đếm phi-chuẩn GIẢ): Kế hoạch, Đề án, Thông báo, Phụ lục, Công văn, Phát biểu, Tờ trình (+Biểu mẫu, Báo
  cáo, Tài liệu — dùng ở 2 profile mới 2026-07-13). Alias ngắn né khóa cũ: `pl`=Pháp lệnh GIỮ (Phụ lục
  không alias 2 chữ), `ttr`=Tờ trình, `tb`/`cv`/`kh`/`bc` thêm mới.
- **(#4) hygiene scan hết báo nhầm chunk là trùng lặp**: chunk `<base>__partNN` (profile-ingest-chunks)
  dùng chung sohieu văn bản gốc BY DESIGN (link qua `goc`) — helper PURE `_is_chunk_part_name` loại chunk
  khỏi `_sohieu_dup_group_real` + ngưỡng flag `_reconcile_clusters` (9 chunk Đề án CĐS hết bị gom
  `duplicate_identity_groups` + gợi nhãn quarantine giả; `dedup-plan` — công cụ ra quyết định thật — vốn
  không mắc).
- **(#5 doc)** RUNBOOK §A0.3: bẫy `gws drive files update` — `--params` chỉ nhận query params, request body
  (`{"trashed":true}`) PHẢI qua `--json`; sai chỗ = HTTP 200 nhưng KHÔNG đổi gì (im lặng thất bại) → mọi
  write gws trần phải readback `files.get`.
- TDD r100 ×12 → **835/835**. KHÔNG bump GAS, KHÔNG đổi kernel doctrine → re-import KHÔNG bắt buộc.

---

# ★ v1.34.37 — ingest `--drive-id`: nạp file ĐÃ Ở TRÊN DRIVE (bỏ bước upload) (2026-07-13)

- **Nhu cầu (user):** người dùng tự tải file lên Drive (kéo-thả `_HOP_NAP` qua UI, điện thoại, shared
  drive) rồi muốn skill tự organize+register — KHÔNG phải re-upload từ máy Claude. Trước đây `ingest-local`/
  `profile-ingest` CHỈ nhận file local; chỉ `register`/`nlm-add` nhận drive_id nhưng bỏ qua convert/chuẩn-hoá.
- **`ingest-local --drive-id <fid>`** (vbqppl 45-cat): LOẠI TRỪ `<file>`. Bỏ upload, organize (convert→GDoc +
  tên chuẩn + xếp cat + stamp + register) NGAY trên file Drive đó → preflight → nlm add → push. Tải nhị phân
  về temp (đường `_fast_drive_fetch`: public-curl→direct-media→GAS) để `--auto-plan`/probe/size chạy Y NHƯ
  đường local; `organize` vẫn dùng CHÍNH drive_id gốc (không re-upload). `--resume` tái dùng fileId qua journal.
- **`profile-ingest --drive-id <fid>`** (profile phẳng): CHỈ convert→GDoc + đổi tên chuẩn, GIỮ PHẲNG trong
  root profile (KHÔNG xếp 45-cat) + register + NLM. Verify-gate đọc text SAU convert (`_read_doc_text`) quyết
  corpus. Bảng tính (.xlsx) → copy_convert Google Sheet.
- **Cổng an toàn** (helper chung `_resolve_drive_id_source`): TỪ CHỐI file Google-native (đã là GDoc/Sheet —
  `convert=true` nhân đôi vì `doCopyConvert_` copy GDoc→GDoc), trashed, không thấy; đuôi/MIME suy từ tên hiện
  có hoặc reverse-map MIME (readback tên src khớp); loại trừ `<file>` + `--drive-id`.
- Parser: `<file>` positional nay `nargs="?"` (bỏ khi dùng `--drive-id`) cho ingest-local/profile-ingest/
  profile-file-add → parser-surface snapshot regen (r77a). r99 ×3 (parser + `_resolve_drive_id_source` phân
  loại + stub-wired). **823/823.** Verify LIVE: từ chối GDoc thật + DRY file nhị phân thật (download temp +
  auto-plan đọc text) + loại-trừ. KHÔNG bump GAS, KHÔNG đổi kernel doctrine → re-import KHÔNG bắt buộc.

---

# ★ v1.34.36 — doctor skip marker-check cho profile root==VBT gốc (2026-07-12)

- Backlog #2 (handoff 2026-07-11): profile `vbthuong` có rootFolderId == CHÍNH thư mục Van_ban_thuong gốc,
  CỐ Ý không đặt marker (marker ở `_meta` VBT gốc sẽ nhận VBT làm 1 profile thường — sai bản thể) → doctor
  nay lazy-bootstrap `vanBanThuongId` 1 lần và SKIP trọn khối marker-check cho profile đó. Dứt known-noise
  `[vbthuong] MARKER_MISSING` lặp mỗi sáng trong ops-sweep. r98 → **820/820**.
- Kèm 2 fix `ops-sweep.ps1` local (ngoài repo, đã vào bundle chuyển giao): B5 dùng `2>$null` (doctor
  v1.34.30+ stream tiến độ ra stderr — `2>&1` cũ trộn làm hỏng parse JSON); B6 thêm `--refresh` (manifest
  cache stale sau data-ops làm desync/unregistered báo OAN).
- KHÔNG bump GAS, KHÔNG đổi kernel doctrine.

---

# ★ v1.34.35 — `ingest-local --no-nlm-add`: quy trình ADD-TAY trên UI (2026-07-12)

> User hỏi đúng chỗ: "file đã GDoc trên Drive mà add lâu là lạ". Benchmark GDoc-add THẬT xác nhận + **đính chính
> phân rã v1 (residual 'settle ~115s' phân bổ sai)**: API `nlm source add` GDoc chỉ **11.0s no-wait / 11.2s wait
> (settle GDoc-đã-index ≈ 0) / 18.7s doc lớn**. 238s hôm trước = 4×NLM-call lúc API chậm + chuỗi GAS + settle
> GDoc mới-convert (caveat cache). **Bottleneck THẬT = cookie NLM ~1h (chết 2 lần/ngày giữa lô), không phải add.**

- **`--no-nlm-add`**: dừng ở Drive+registry (organize register xong), KHÔNG đụng NLM — né hẳn cookie. corpus
  KHÔNG set (doctrine S4). Output: `gdoc_url` + `suggested_notebook` (routing GAS `nlm_preflight` vẫn chạy —
  không cần cookie) + `notebook_url` + `next_steps` 3 bước điền sẵn. Journal `run_end +no_nlm_add`.
- **Quy trình khép kín bằng tool sẵn có**: add tay trên UI NotebookLM (Drive-picker chọn NHIỀU GDoc 1 lần,
  session browser bền) → `nlm-reconcile --all-notebooks` (nguồn add tay = link_candidates bắc cầu EXACT-TITLE
  vì tên GDoc = tên nguồn) → per-notebook `--apply` link registry → `register --drive-id <gdoc> --corpus true`.
- r97 ×3 (parser + full-mock dừng-đúng-chỗ + journal sạch, nlm_cli Boom-guard chứng minh 0 đụng NLM) → **819/819**.
- KHÔNG bump GAS (2.21.2j), KHÔNG đổi kernel doctrine.

---

# ★ v1.34.34 — vá 2 bài học THỰC CHỨNG lô song song: race reg_bulk + reconcile overflow (2026-07-12)

> Nạp lô thực chứng 2 VBHN (`--nlm-no-wait` + skip-flags + 2 process song song): **~63s/file kể cả sự cố**
> (vs 238s baseline, ~3.8×). Sự cố thật lộ 2 lỗ hổng: ca VBHN 06 registry TRỐNG dù journal patched=1+verified
> (race), và reconcile báo "sạch" trong khi nguồn nằm ở overflow (ngoài phạm vi quét).

- **(a) Race `reg_bulk` concurrent** — 2 process ghi Sheet cùng lúc → last-write-wins NUỐT 1 bản dù server trả
  patched=1. `_verified_reg_write` nay với batch ≤`_REG_BULK_READBACK_MAX`(3): READBACK field-level per-item
  (reg_get refresh=true, khuôn N3 của reg_upsert) → lệch → RETRY reg_bulk per-item đúng 1 vòng (sau race,
  lần ghi lại là bền — tự chữa đúng ca lô song song) → vẫn lệch → `REG_BULK_FIELDS_DROPPED` loud (rc caller ≠ 0).
  Batch lớn giữ patched-check (backfill 33-dòng không phình thời gian). Đường reg_link ingest (1 item) nay an toàn race.
- **(b) `nlm-reconcile --all-notebooks`** — lưới cuối lô quét CẢ base + overflow shard (TL_OVERFLOW_NOTEBOOK_ID)
  1 lệnh, stream per-notebook, gộp `per_notebook`; DRY-only (apply vẫn per-notebook — chặn loud). Dogfood LIVE
  bắt ngay 2 finding thật trên overflow mà lưới cũ mù: link_candidate `76-2026-VBHN` Luật Dược (→ `--apply`
  backfilled) + 1 nguồn unregistered `VBHN_73-82-ND-CP_Phu_luc` (chờ user quyết).
- **DATA-OP cùng phiên**: `63-2025-VBHN-VPQH` XLVPHC → corpus=false (superseded bởi `90-2026-VBHN-VPQH` vừa nạp;
  nguồn NLM bản cũ còn live trên notebook chính — gỡ hay giữ do user quyết).
- r96 ×6 TDD + r3 mock cập nhật theo hành vi mới → **816/816**. ★Bẫy I11 biến thể mới ghi sổ: HẰNG cho vào
  `_STUB_MAP` thành function stub → so sánh int nổ; hằng PHẢI re-export trực tiếp `X = _tl_mod.X`.
- KHÔNG bump GAS (2.21.2j), KHÔNG đổi kernel doctrine.

---

# ★ v1.34.33 — `ingest-local --nlm-no-wait`: nạp lô nhanh −55% (2026-07-12)

> Benchmark từ 3 lần nạp thật + micro-bench từng op (`D:\Quốc hội\benchmark-ingest-2026-07-12.md`):
> ingest-local **~238s/file HẰNG SỐ bất kể size** (24-61KB). Cổ chai = **NLM 71%** (settle-wait sau
> `source_add` ~115-125s = 50%; mỗi NLM CLI call 11-18s = spawn 2s + batchexecute API 10-16s vốn có),
> GAS chỉ 19% (upload 24KB = 2.6s — không phải nút). `ingest-zip` không amortize (spawn child per-file).

- **`--nlm-no-wait`**: bỏ chờ nguồn settle sau `nlm source add` — `source_id` có NGAY từ add-response nên
  bước reg_link vẫn ghi ĐỦ (nlm_* + corpus=true); settle chạy ngầm phía NLM. Post-add dup-check BỎ khi
  no-wait (nguồn chưa settle → source_list âm tính giả + tốn thêm ~18s). Output thêm `nlm_settle=not_waited`
  + `next_step` nlm-reconcile. Ước **−55%: 238s → ~90-120s/file**.
- **Công thức nạp LÔ** (ghi COMMANDS.md): `--nlm-no-wait --skip-nlm-preflight --skip-live-check` (2 cờ sau
  CÓ SẴN, an toàn khi đã dedup trước bằng reg-query) + chạy 2-3 file song song → **~35-50s/file wall**;
  **cuối lô PHẢI `tl nlm-reconcile`** xác nhận settle + link đủ; truy vấn NLM nội dung vừa nạp cần chờ vài phút.
- r95 ×3 (parser + shape-lock khuôn r55 + PURE `_add_args` bỏ `--wait`) → **810/810**. KHÔNG bump GAS, KHÔNG đổi kernel.

---

# ★ v1.34.32 — VBHN-FIRST TẤT ĐỊNH cho corpus-relation-sweep (2026-07-11)

> User bắt lỗi doctrine trên kết quả sweep v1.34.31: đề xuất đi lấy Luật GỐC (77-2006 TDTT, 21-2017 Quy hoạch,
> 16-2012 Quảng cáo, 75-2015 MTTQ) trong khi **VBHN đã có trong corpus phủ trọn chuỗi** — trái nguyên tắc §0.1
> VBHN-first (4/7 đề xuất sai). Kèm 46% vbhn false-positive (VBHN Thư viện gán cho Luật Thủ đô/Viễn thông…)
> do matcher fuzzy subject của relation-check khi sweep không có `--subject` tường minh.

- **(1) `_vbhn_goc_map` (PURE)** — map `norm_sohieu(gốc/luật-sửa) → [VBHN corpus SẠCH phủ]` từ 3 nguồn TẤT ĐỊNH
  trên registry: field `goc` (';'-cách) + `sua_doi` dạng 'Hợp nhất từ: a, b' + pattern tên `goc_<sohieu>`
  (phủ 67/72 VBHN corpus; VBHN quarantine/non-corpus bị loại). KHÔNG fuzzy.
- **(2) `covered_by_vbhn`** — amendment thiếu-corpus NHƯNG chuỗi đã có VBHN phủ → xếp `covered_by_vbhn` (kèm số
  VBHN), KHÔNG vào `sources_to_add`. Đúng VBHN-first: có VBHN thì không đi lấy bản gốc/sửa-đổi rời.
- **(3) `vbhn_broken` goc-tie** — CHỈ giữ VBHN ứng viên hỏng khi goc của nó GIAO chuỗi `{base ∪ mọi luật-sửa
  inline}` (tra `goc` theo drive_id + pattern tên); không tie → drop (`vbhn_dropped_no_tie` đếm). Diệt trọn lớp
  VBHN-Thư-viện→Luật-Thủ-đô.
- **(4) `vbhn_first_self`** — chính base nằm trong chuỗi hợp nhất của VBHN corpus → advisory bản-rời-redundant
  (đúng chiều thứ hai của VBHN-first: giữ VBHN, bản gốc/sửa-đổi rời cân nhắc loại; chỉ báo, không tự xoá).
- Verify LIVE ca 26-2018 (sửa TDTT): `77-2006 → covered_by_vbhn [64-2025-VBHN-VPQH]`, `vbhn_first_self=[64-2025]`,
  0 sources_to_add (trước: đề xuất sai đi lấy 77-2006). r94 ×3 + r93 asserts đổi có chủ đích → **807/807**.
- KHÔNG bump GAS, KHÔNG đổi kernel doctrine (§0.1 vốn đã ghi VBHN-first — đây là vá TRIỂN KHAI cho đúng doctrine).

---

# ★ v1.34.31 — RÀ CORPUS VBQPPL: mở rộng suy loại + tool corpus-relation-sweep (2026-07-11)

> Sinh từ phiên `grill-with-docs` rà toàn bộ Luật/NQ corpus (749 dòng · 471 corpus · 33 Luật + 44 NQ + 72 VBHN).

- **(a) `_infer_loai` mở rộng — vá 38 dòng corpus loai RỖNG:** trước đây `backfill-loai` bỏ trống điều ước quốc tế
  (`CU_`/`CPTPP_`/`EVFTA_`) + văn kiện Đảng (`KL_`/`CT_`/`HD_`) vì thiếu prefix trong inference. Nay: `CU_`→Công ước;
  `CPTPP_`/`EVFTA_`→Điều ước quốc tế; `KL_`→Kết luận; `CT_`→Chỉ thị; `HD_`→Hướng dẫn (+thêm "Hướng dẫn" vào enum
  `_LOAI_CANON`); +sohieu-fallback `-KL-`/`-CT-`/`-HD-`. `VK_` (văn kiện Đại hội, dị thể: Báo cáo/NQ/Chương trình) ở
  lại manual (không đoán bừa). ⇒ ~30/38 dòng nay suy được loại; 6 VK_ chờ curate tay.
- **(b) TOOL MỚI `corpus-relation-sweep` (#T1) — trả lời "liệt kê nguồn liên quan cần bổ sung":** BATCH `relation-check`
  trên toàn bộ Luật/NQ corpus (hoặc `--loai`/`--cat` lọc) bằng cách **tái dùng chính `cmd_relation_check`** (SCRIPT-REUSE
  #15, capture JSON per-doc) → GỘP 1 báo cáo: mỗi VB → `vbhn_broken` (VBHN liên quan quarantine/removed/thiếu-năm) +
  `missing_links` + (chỉ `--deep`, đọc nguyên văn base) `amendments_missing` (VB gốc bị sửa nhưng chưa có corpus) +
  `google_discovery` kèm để đi lấy về. STREAM per-doc ra stderr (`[sweep] (i/N)` — timeout không mất trắng) + resumable
  `--limit`/`--skip` + `--out`. READ-ONLY. Lấp gap skill: `relation-check` chỉ chạy 1 `--base`/lần nên trước đây không
  có cách 1-lệnh liệt kê "mọi nguồn còn thiếu" toàn corpus.
- r93 ×5 TDD → 804/804. **KHÔNG bump GAS (2.21.2j), KHÔNG đổi kernel doctrine → re-import không bắt buộc.**

---

# ★ v1.34.30 — vá 7 lỗi log grill: register/from-nlm/doctor/marker (2026-07-11)

> Grill chốt (cây quyết định): register `--row-kind` choices GIỮ `own/overflow/ref` — KHÔNG mở `nlm_only`
> (đề xuất #2 gốc) vì sentinel cần cả bó bất biến `_from_nlm_row_payload` set; sentinel đi qua đường sanctioned mới.

- **#1 `register --bulk` không insert được (cờ `--force-insert` gây hiểu lầm):** `reg_bulk` là UPDATE-only theo
  thiết kế; `--force-insert` trên `--bulk` chỉ BỎ QUA kiểm client (drive_id format/tồn tại), KHÔNG khiến insert.
  Trước đây dòng key không khớp = `missed` báo IM LẶNG (operator tưởng `patched:0` là thành công). Nay SURFACE
  `missed_count`/`missed_ids` top-level + rc=1 khi missed>0 + `force_insert_note` chỉ đường đơn / `from-nlm --add-missing`.
- **#2→ `profile-from-nlm --add-missing` (lấp khoảng trống):** trước đây KHÔNG có đường sanctioned để thêm nguồn
  `nlm_only` vào profile ĐÃ TỒN TẠI (`profile-from-nlm` từ chối `ALREADY_PROFILE`; `reconcile` chỉ báo) → phải
  hand-craft sentinel qua `register`. Cờ mới seed CHỈ nguồn còn thiếu (khóa `nlm_source_id`; reuse `_from_nlm_row_payload`
  → ép đủ bó bất biến sentinel; journaled+verified; DRY mặc định; KHÔNG đụng marker/config/chat/system-prompt).
  Không cờ + folder có marker → `ALREADY_PROFILE` kèm hint. `--notebook` nay optional (mặc định lấy từ config profile).
- **#3 `register` đơn báo `updated:false` cả khi vừa INSERT dòng mới:** webapp không phát cờ phân biệt insert;
  nay precheck `reg_get` TRƯỚC upsert → field `inserted:true/false` (hết ngộ nhận ghi hụt, khỏi reg-query lại tay).
- **#4 `register` thiếu `--json`:** thêm no-op (nhất quán `nlm-add` #6) — gõ `register … --json` hết đổ ~150 lệnh top-level.
- **#5 `profile-doctor --deep` chậm + mất trắng khi timeout:** thêm `--limit`/`--skip` cắt lô + STREAM per-profile ra
  stderr (`[doctor]` progress + `[doctor-jsonl]` findings → timeout giữ phần đã xong) + `resume_command`; GIỮ scan-all
  mặc định (KHÔNG breaking ops-sweep/caller); stdout vẫn 1 JSON tổng hợp cho contract.
- **#6 wording "readback" system prompt gây ngộ nhận:** `nlm chat` chỉ có configure(ghi)/start, KHÔNG đọc được cấu
  hình chat LIVE. Sửa docstring `_nlm_system_prompt_apply` + thêm field runtime `verification=local_artifact_and_api_ok_only`
  + `verification_note` (operator thấy ngay mức xác minh thật, không tưởng 'applied' = đã xác nhận nội dung LIVE).
- **#7 ROOT-CAUSE marker "Chỉ thị" trùng tên/mồ côi:** `_marker_write` upload `force=true` LUÔN tạo `fileId` mới (Drive
  cho trùng tên) và TRƯỚC đây chỉ trash `old_id` do caller truyền → create/from-nlm/promote (`old_id=''`) gặp marker của
  lần retry đứt = DUPLICATE mồ côi (trỏ registry/manifest khác). SELF-HEAL: sau khi bản mới verified, quét `_meta` trash
  MỌI marker cùng tên khác `fileId` mới. Doctor +check `MARKER_DUPLICATE`. (Dọn bản mồ côi LIVE = data-op confirm riêng.)
- TDD r92 ×13 → 799/799. **KHÔNG bump GAS (2.21.2j), KHÔNG đổi kernel doctrine → re-import không bắt buộc.**

---

# ★ v1.34.29 — `profile-set-meta`: cửa ghi chính thức phần MÔ TẢ trên marker (2026-07-11)

- Gap lộ ra khi `profile-load "Chỉ thị"`: marker do luồng tự động tạo không có description/style —
  mà ADR-0003 định marker là NGUỒN SỰ THẬT phần mô tả nhưng CHƯA có lệnh nào ghi được các field đó
  (backfill chỉ build từ config vốn không mang mô tả).
- **`tl profile-set-meta [--profile-name <p>] --description/--style/--see-also/--source-policy`**:
  DRY mặc định (plan changes old→new); `--apply` ghi marker journaled + readback + trash bản cũ;
  identity lấy từ CHÍNH marker (không phải config); `created_at` giữ; XOÁ field = truyền chuỗi rỗng;
  `see_also` tên lạ chỉ warning (relations là MÔ TẢ, không mở scope); marker thiếu/hỏng → chặn với
  gợi ý backfill. KHÔNG đụng config (profile-sync một chiều không mang field mô tả).
- TDD r91 ×6 viết trước → **784/784**; parser-surface + golden regen có chủ đích.

# ★ v1.34.28 — vá bug máy-phụ-thuộc #5: r77a parser-surface lệch theo version Python (2026-07-11)

- Phiên kiểm chứng zip 1.34.27 (Python 3.11) báo selftest 778/779 — `r77a_parser_surface_matches_snapshot`
  FAIL tại `cache-build`/`fetch-batch`/`rasoat`, trong khi canonical (3.13) + CI (3.12) đều xanh.
  TÁI HIỆN được bằng Python 3.11 local → ROOT CAUSE: snapshot hash CẢ field `required` của POSITIONAL
  action — giá trị DẪN XUẤT theo version Python (positional nargs='*': 3.11 đặt required=True,
  3.12+ đặt False — thay đổi argparse thượng nguồn), KHÔNG phải bề mặt CLI thật.
- Fix: `_parser_surface_map` chỉ hash `required` cho OPTIONAL (positional → None; ngữ nghĩa đã nằm trọn
  trong `nargs`); regen snapshot; **verify cross-Python 3.13 + 3.11 cùng 779/779**.
- Bài học nhập sổ **máy-phụ-thuộc #5** (nối #1 zip-container-hash, #2 CRLF-writer, #3 w/mixed-eol,
  #4 load_creds-cache-vắng): snapshot/golden KHÔNG được hash field mà runtime DẪN XUẤT theo
  version/OS/env — chỉ hash bề mặt do MÌNH khai báo.

# ★ v1.34.27 — HOTFIX 7 lỗi thực-chiến từ log phiên tạo profile + nạp 4 file (2026-07-11)

- Nguồn: báo cáo phiên thật (Chỉ thị/Tờ trình/2 Công văn) — thẩm định 7/7 CONFIRMED trên canonical.
- **(#1 nghiêm trọng) `nlm-add` NameError `_nlm_add_doc_type`**: helper thêm v1.34.17 THIẾU stub tl
  (bẫy rebase I11 lặp lần 3) → đường add chuẩn chết, phải add tay. Vá stub + **r90 DRIFT-LOCK GENERIC**:
  AST-scan mọi module REBASE — mọi tên top-level được function trong module tham chiếu PHẢI resolve qua
  tl namespace (khoá CẢ LỚP bẫy; scan xác nhận không còn tên nào khác sót; module copy-globals Pha C/D
  tự resolve nên miễn).
- **(#2 nghiêm trọng) verify_gate đòi Điều sai với văn bản thường**: cả 4 file dừng
  `DIEU_STRUCTURE_NOT_VERIFIED` vì kind=draft/nq — nhưng văn kiện KIỂU MỤC (Chỉ thị/Tờ trình/Công văn,
  kể cả bản DỰ THẢO của Chỉ thị Đảng) không bao giờ có Điều. Vá: `requires_dieu` CHỈ khi corpus NỀN
  vbqppl (`base_profile` param, mặc định tự đọc `_active_profile()`); profile thường → info flag
  `PROFILE_DOC_DIEU_NOT_REQUIRED`, corpus_allowed đi tiếp. Corpus nền GIỮ NGUYÊN đòi Điều.
- **(#3) DRY/apply lệch phân loại**: probe không đọc được .docx local (`probe_text_source=null`) →
  phân loại rơi về tên file. Vá: `_profile_read_probe_text` trích text .docx CỤC BỘ (zip
  word/document.xml, strip tag, không cần lib) → DRY dự báo đúng kết quả apply.
- **(#4) reconcile không link nguồn Drive-add**: source_list không phơi url/drive_id cho nguồn add qua
  `--drive` → tier drive_id/sohieu đều MISS → unregistered OAN. Vá: TIER 3 EXACT-TITLE duy nhất
  (khoá `_ingest_dedup_title_key` — cùng chuẩn dedup-live S13; trùng ≥2 dòng → KHÔNG link).
- **(#5) FIELDS_DROPPED không tự phục hồi**: retry-GET per-field (v1.34.17 #6) vẫn rớt lặp với giá trị
  tiếng Việt dài (nghi giới hạn/encoding GET query — ca thật cột `tukhoa`). Vá: FALLBACK **POST
  reg_bulk per-field** + readback lần cuối (`fields_retried_post`); còn rớt mới báo lỗi.
- **(#6)** `nlm-add` +`--json` no-op (hết rc=2 usage-error, đồng bộ bề mặt CLI). **(#7)** hết
  `datetime.utcnow()` deprecated (regio manifest_export — DeprecationWarning lẫn vào JSON capture).
- TDD r90 ×7 viết trước (đỏ xác nhận: scan bắt đúng 1 tên thiếu + gate TypeError) → **779/779**;
  parser-surface regen (nlm-add +--json).

# ★ v1.34.26 — PROFILE P4 (KẾT LỘ TRÌNH 4 PHASE): profile-from-nlm + nguồn nlm-only + materialize (2026-07-11)

- **`tl profile-from-nlm --name <p> --notebook <nb> [--folder <id>]`** MỚI (Q4): notebook→profile —
  folder riêng + registry/manifest/marker/config own+own; seed row theo nguồn notebook: có file Drive →
  `row_kind=ref` (drive_id thật, `_nlm_source_drive_id` bóc); text/URL/YouTube → **`row_kind=nlm_only`**
  với **SENTINEL `drive_id=nlm:<source_id>`** — KHÔNG bump GAS (REG_COLS_ hằng server, cột mới = đắt vô
  ích): materialize_status suy diễn (pending/blocked ghi cột `note` sẵn có; done = row thật tồn tại).
  KHÔNG ghi đè chat config notebook đang dùng (khác promote — notebook MỚI mới áp sysprompt).
- **`tl profile-materialize-sources`** MỚI (chính sách mặc định **materialize_preferred**, chốt grilling
  2026-07-10): `source_content` → `createtext` GDoc vào folder profile → row own verified → xoá sentinel
  (`reg_delete`, TẠO-TRƯỚC-XOÁ-SAU — đứt giữa chừng để lại SENTINEL_STALE, run sau tự dọn, idempotent);
  RESUMABLE `--limit`/`resume_command`, lặp tới `pending_remaining=0`; không xuất được →
  `note=materialize=blocked:<reason>` — Ở LẠI nlm-only HỢP LỆ (Q4), `--retry-blocked` thử lại.
- **`tl profile-doctor --deep`**: chiều Drive↔NLM↔registry (reg_get theo nlm_source_id, scope registry
  PROFILE): `NLM_SOURCE_UNREGISTERED` / `NLM_ONLY_PENDING` / `NLM_ONLY_BLOCKED` / `SENTINEL_STALE`.
- Ghi chú giới hạn: row nlm_only có thể KHÔNG vào manifest (manifest_export quét theo Drive/registry
  server-side) — tra nguồn nlm-only qua `reg-query`/doctor --deep; Instruction Block (profile-load) đã
  buộc nói rõ nguồn nào chỉ có trên NLM.
- TDD r89 ×7 (from-nlm DRY/APPLY, materialize DRY/APPLY nâng-cấp+blocked, doctor deep, parser) →
  **772/772**; golden + parser-surface regen có chủ đích. **HOÀN TẤT lộ trình profile P1→P4** (grilling
  10 quyết định + hợp nhất nhánh song song, 2026-07-10).

# ★ v1.34.25 — PROFILE P3: profile-promote (folder→profile) + create-notebook có kiểm soát + NLM System Prompt tự áp (2026-07-10)

- **`tl profile-promote --name <p> --folder <id> [--notebook <nb>|--create-notebook]`** MỚI (Q2+Q3+Q5):
  biến folder Drive THƯỜNG thành profile — dựng hạ tầng CÒN THIẾU (_meta/registry Sheet/manifest JSON/
  marker/config own+own), asset sẵn có DÙNG LẠI (idempotent, khuôn adopt); **manifest chỉ reuse khi JSON
  tự nhận đúng profile** (file tên manifest nhưng của profile khác/lạc → `MANIFEST_FOREIGN_IGNORED`,
  tạo mới — TDD bắt được trước khi thành bug); SEED registry từ file trong folder (`row_kind=own,
  corpus=true`, per-row `_journaled_reg_upsert`, bỏ asset hạ tầng). Nạp NLM KHÔNG trộn vào promote —
  next_steps: `ingest-missing --allow-no-sohieu` (idempotent/resume, văn bản thường không có số hiệu).
- **`--create-notebook`** = nới điều-kiện-kép notebook_create CÓ KIỂM SOÁT (quyết định Q2): chỉ trong
  ngữ cảnh tạo profile, `--apply` đòi `--confirm yes`, journal intent/commit `nlm_notebook_create` +
  READBACK `notebook_get` canary; id ghi vào config + marker. `nlm_cli` +2 wrapper `notebook_create`/
  `chat_configure`.
- **NLM System Prompt (Q5)**: generator-sinh (`generate('nlm')`, KHÔNG viết tự do, 4.6k chars) → LƯU
  `_meta/nlm_system_prompt.md` (bản-đã-áp/bản-cần-dán) → TỰ ÁP `nlm chat configure <nb> --goal custom
  --prompt …`; CLI fail/quá 10000 chars → `manual_required` kèm chỉ dẫn dán tay, KHÔNG chặn promote.
- Guards: `ALREADY_PROFILE` (folder có marker → profile-sync/adopt), `PROFILE_EXISTS_DIFFERENT_FOLDER`,
  `REFUSE_PROMOTE_VBT_ROOT`, `--notebook`⊕`--create-notebook`. COMMAND_META medium/drive_registry_nlm
  (contract thật → backlog pha siết; drift-lock r65 giữ nguyên tắc high-phải-có-contract).
- TDD r88 ×8 viết trước (confirm-guard/already-profile/DRY-plan/apply-full/sysprompt-fallback/
  reuse-assets/seed-dedup-gdoc-raw/parser) → **766/766**; golden + parser-surface regen có chủ đích.
  Live-smoke DRY folder thật 'Khảo sát Luật Xuất bản' bắt 2 nâng cấp: seed quét ĐỆ QUY (file lồng
  subfolder chủ đề) + dedup cặp GDoc↔raw cùng tên (16 item → seed 8). ★Bẫy I11 lặp: hằng module mới
  (_SEED_RAW_EXT_RE) quên re-export ở tl → NameError; đã vá + ghi khuôn.
- **MERGE từ _patch-inbox-2026-07-10 (THẨM ĐỊNH XONG)**: `tl_gws._stage_enc_upload` fallback gws→gcloud
  khi `update_content` lỗi (giữ fileId, verify md5 — cùng khuôn drive-push --via v1.33.49; diff +15 dòng,
  dùng helper sẵn có; gate 766/766 xanh với patch). Patch được install-patch.ps1 áp thẳng vào canonical
  lúc 00:42/01:07 (11-07) — 4 file .bak/refresh-tokens.ps1 lạc vào repo (ĐÃ nhiễm RELEASE_MANIFEST một
  nhịp) → dọn về `_patch-inbox-2026-07-10/applied-20260711/` + regen manifest. refresh-tokens.ps1 bản
  patched nằm ở đó — user tự đối chiếu/thay bản local D:\Quốc hội\ (file local-only, không thuộc repo).

# ★ v1.34.24 — PROFILE P2: profile-load (Instruction Block từ marker) + KERNEL-DIFF ADR-0003 user duyệt (2026-07-10)

- **`tl profile-load <p> [--target session|project] [--offline]`** MỚI (Q7 + ADR-0003): "dùng profile X
  trong PHIÊN" = xuất **Instruction Block** sinh từ MARKER (định danh + description + style văn phong +
  relations{base vbqppl luôn bật, see_also} + source_policy) — MỘT bản THỐNG NHẤT mọi môi trường
  (Chat=Cowork=Code), chỉ rẽ `--target` đúng 1 dòng (thân block bằng nhau từng byte — selftest khoá).
  READ-ONLY: không ghi config/marker. Marker best-effort LIVE; offline → config + `marker_note`;
  marker↔config lệch → cảnh báo gợi ý `profile-sync`; profile chưa vào config → PROFILE_NOT_FOUND
  kèm gợi ý `profile-sync --apply`. Block chứa guard không-bịa ("Chưa tìm thấy căn cứ…", "Không nhận
  RAG làm nguyên văn"), tra-NLM-đúng-notebook (1–3 source, hard cap 5, canonical profile thắng),
  scope ghi riêng + nlm-only/materialize_preferred. `profile-use --apply` nay in kèm block (offline).
- `gen_instructions.generate_profile_load_block` + biến thể corpus nền vbqppl; +5 case selftest
  gen_instructions (29/29); r87 ×7 TDD viết trước (marker-source/drift-warn/offline-fallback/not-found/
  use-apply-emits/parser) → **758/758**; golden tool_inventory/workflow_audit + parser-surface regen.
- **KERNEL-DIFF (USER ĐÃ DUYỆT nguyên văn)**: §1 bullet 9 — bỏ "nguồn sự thật duy nhất vẫn là config",
  thay bằng khối "★ v1.34.22-24 (ADR-0003) — MARKER là nguồn sự thật" (+ profile-sync/backfill/
  profile-load/discover marker-first). **SKILL.md ĐỔI DOCTRINE → USER RE-IMPORT Capabilities sau deploy.**
- Live-smoke: `profile-load "Luật BHXH"` đọc marker THẬT (source=marker, đúng notebook 59e8d0de…,
  không drift). KẾ TIẾP: P3 promote + notebook_create + NLM system prompt; P4 from-nlm/nlm_only/materialize.

# ★ v1.34.23 — vá live-smoke P1: guard vbt_id + backfill marker THẬT cho Luật BHXH/NQ80 (2026-07-10)

- Live-smoke `profile-sync` DRY trên Drive thật (13 folder) bắt ngay 1 bug: `vbthuong` (profile đặc biệt
  root == CHÍNH Van_ban_thuong) bị báo `orphaned` OAN — `_profile_sync_rows` thiếu guard `vbt_id` mà
  `_discover_classify` có. Vá: +tham số `vbt_id`; backfill thêm `skipped_vbt_root` (không đặt marker vào
  `_meta` của VBT gốc — sẽ nhiễu discover; vbthuong định danh qua config, xử lý ở P2). TDD: r86 mở rộng
  2 assert viết trước → **752/752**.
- **DATA-OPS THẬT (hoàn tất rollout P1)**: `profile-backfill-markers --apply` LIVE — marker `Luật BHXH`
  (1dLahha4…) + `NQ80` (12HV4iCF…) written + readback verified, journaled; chạy lại `profile-sync` →
  **in_sync ×2, rc=0**. Vòng marker→sync→config khép kín trên hạ tầng thật.

# ★ v1.34.22 — PROFILE P1 (ADR-0003): marker là nguồn sự thật + profile-sync/backfill + discover marker-first (2026-07-10)

- Thực thi Phase 1 lộ trình profile (grilling 2026-07-10 + hợp nhất nhánh song song): **marker
  `_meta/tra_luat_profile.json`** (schema `tra_luat_profile.v1`: định danh rootFolderId/metaFolderId/
  notebookId/registryDocId/manifestId/categories/manifestScope + mô tả description/style/relations{base:vbqppl}/
  source_policy=materialize_preferred/created_at/updated_at) = **nguồn sự thật về TỒN TẠI + ĐỊNH DANH +
  metadata mô tả**; config = lựa chọn runtime + cache; `_PROFILES_INDEX` = chỉ mục đọc nhanh.
- **`tl profile-sync`** MỚI: đồng bộ MỘT CHIỀU marker→config (quét Van_ban_thuong; new_from_marker/drift/
  marker_missing/broken_marker/root_conflict/orphaned/refused_base; --apply ghi config journaled + READBACK
  từng field; KHÔNG bao giờ ghi marker; marker tự nhận vbqppl bị bỏ qua). **`tl profile-backfill-markers`**
  MỚI: backfill một-lần config→marker (upload + readback + trash bản cũ, journal `marker_write`; tạo `_meta`
  nếu thiếu + điền metaFolderId; --force ghi đè có chủ đích).
- **profile-create/adopt --apply GHI LUÔN MARKER** (mutation ghi 2 nơi marker+config; marker fail không
  rollback config — doctor/backfill vá). **discover MARKER-FIRST**: statuses mới `configured`(+marker_status
  ok/missing/broken/drift)/`adoptable`(gợi ý profile-sync — HẾT heuristic)/`broken_marker`/`unregistered_profile`
  (hạ tầng không marker)/`orphaned`(tên cũ config_only). **profile-doctor** +4 check marker (MISSING/INVALID/
  READ_FAILED/CONFIG_DRIFT). **Observability**: `config_report` (config-of-record + cảnh báo
  DUPLICATE_CONFIG_CANDIDATES) trong profile-list/info/sync.
- Cơ chế ghi marker THUẦN GAS webapp sẵn có (upload POST + resolvefolder + list + download + trash) —
  KHÔNG bump GAS; mọi env (Chat=Cowork=Code) dùng chung một đường.
- TDD: +10 `r86` viết trước (PURE body/validate/diff + classify marker-first + wiring sync DRY/APPLY +
  backfill DRY/APPLY journal-shape + config-of-record + parser) & r6 đổi status có chủ đích → **752/752**;
  parser-surface regen (2 lệnh mới); golden tool_inventory/workflow_audit regen có chủ đích.
- SKILL.md chỉ đổi số version header — kernel wording "config là nguồn sự thật" sẽ sửa ở **P2** (kernel-diff
  cần user duyệt + re-import, kèm profile-load/Instruction Block). KẾ TIẾP: P2 profile-load + generator đọc
  marker; P3 promote + notebook_create + system prompt; P4 from-nlm + nlm_only + materialize.

# ★ v1.34.21 — HOTFIX resilience `register --clear-cols` + contract_check phân loại (2026-07-10)

- Nguồn: thẩm định review nhánh Codex trên zip 1.34.20 — 4/4 finding CONFIRMED trên canonical; grilling
  chốt 2 quyết định (verify theo precheck+readback, KHÔNG dùng cleared>=1 vì phá idempotency; hotfix riêng
  TRƯỚC Profile P1). KHÔNG bump GAS (client tự kiểm bằng reg_get).
- **P1 hết thành-công-giả**: `_register_clear` PRECHECK `reg_get` — drive_id không khớp dòng nào →
  `NO_SUCH_ROW` rc=2 KHÔNG ghi (trước: GAS `ok:true, cleared:0` + readback no-row → `verified:true` GIẢ).
  Verified = dòng CÒN TỒN TẠI + cột RỖNG sau readback; dòng tồn tại + `cleared=0` = `already_empty`
  THÀNH CÔNG idempotent (re-run sau đứt mạng vẫn rc=0). Precheck/readback raise → `REG_PRECHECK_FAILED`/
  `READBACK_FAILED` rc=1, không traceback.
- **P1 về primitive chung**: `--clear-cols` nay đi `_journaled_reg_clear(force=)` (mở rộng: force='yes'
  cho cột thường server 2.21.2j; validate chặn `_REG_CLEAR_PROTECTED`) — được miễn phí: try/except quanh
  `reg_clear`, journal intent{`key_field`,`set`,`before`} đúng khuôn `_journal_undo_ops`/`_journal_resume_ops`
  (trước đây intent thiếu set/key_field → undo/resume MÙ với clear). `before` lấy từ dòng LIVE precheck
  (chuẩn hơn manifest stale). Commit CUỐI ghi theo READBACK (re-run đã-rỗng không treo inflight).
  `_apply_gate(write_cols=...)` chặn như mọi đường ghi registry.
- **contract_check**: classifier thuần `live_verdict` — `LIVE_PING_FAILED` rc=4 (mạng/auth/runtime,
  kèm detail; ping raise cũng bắt) TÁCH KHỎI `VERSION_DRIFT` rc=3 (trước: ping hỏng in
  'deploy = None ≠ hợp đồng' như drift thật); selftest 2→6 case.
- TDD: +7 `r85b` VIẾT TRƯỚC (đỏ xác nhận bằng chính traceback boom-clear làm sập selftest — bằng chứng
  sống finding thiếu-try/except) → **742/742**. Backlog nhận thêm từ review: log config-of-record +
  cảnh báo duplicate config candidates (ghép Profile P1); smoke `--clear-cols` fixture an toàn → smoke-plan.
- SKILL.md chỉ đổi số version header — KHÔNG đổi doctrine → không cần re-import.

# ★ v1.34.20 — #5 TRỌN VẸN: webapp GAS 2.21.2j reg_clear 2-tầng + `register --clear-cols` (2026-07-10)

- **GAS 2.21.2j** (deploy clasp `gas-deploy.ps1`, GIỮ URL /exec, version 74): `doRegClear_` 2 TẦNG —
  `nlm_*`/note như cũ (confirm=yes); **cột thường ∈ REG_COLS_ cần thêm `force='yes'`**; `drive_id`/`name`
  BẢO VỆ tuyệt đối. Tương thích ngược 100% (call cũ không force vẫn chỉ nlm_*/note).
- **tl-side**: `register --drive-id <id> --clear-cols <csv> --confirm yes` — tự gắn force cho cột thường,
  journaled (intent{before-từ-manifest} cho undo tay) + **readback field-level xác nhận đã RỖNG**;
  guards client-side (protected/confirm/thiếu-drive-id). `note_empty` (#5 v1.34.17) nay gợi ý đường mới.
  Đóng ca thật hồ sơ BHXH: "sohieu gán nhầm không xoá trắng được".
- **Đóng dấu version**: EXPECT_VERSION 2.21.2i→2.21.2j (`contract_check --bump` — nay sửa CẢ literal
  tl_selftest; 17 chỗ SKILL/RUNBOOK; `references/Code.2.21.2j.gs` đổi tên theo + gas-deploy.ps1 5 chỗ).
  **SKILL.md ĐỔI → user RE-IMPORT Capabilities sau deploy.**
- TDD: +5 `r85` viết trước (parser/force-routing/guards/nlm-no-force/note) → **735/735**.

# ★ v1.34.19 — BACKLOG #11: _persist_profile_config ghi đúng config ACTIVE (2026-07-10)

- Phát hiện từ ca thật #10: `profile-adopt` không `--config` ghi block vào `~/.tra_luat_config.json`
  (hardcode) trong khi config ACTIVE là `tra_luat_config.v2.json` cạnh skill → ghi lạc chỗ IM LẶNG,
  `profile-list` vẫn inherit không rõ vì sao.
- Fix: ứng viên ghi = `_config_candidates(config_path)` — CÙNG thứ tự resolution với đường ĐỌC config
  (cwd/skill-side v2 trước home); `--config` tường minh vẫn thắng. TDD `r84` viết trước (đỏ) → **730/730**.

# ★ v1.34.18 — I11: VƯỢT ĐÍCH 2.500 — tl.py 3.576→1.394 dòng (−93% từ 19.052) (2026-07-10)

- **(a) LEFTOVER-SWEEP**: 91 def ~1.5k dòng (hụt ngưỡng affinity 50% hồi I9) gán vào 14 module theo
  **affinity-tốt-nhất ≥1-ref**; 10 def 0-affinity ở lại. **(b) `build_parser` 391d → `tl_core/cli.py`**
  NGUYÊN VĂN (35 block tay + doctrine-comment giữ tại chỗ) — **parser-surface KHỚP KHÔNG REGEN** = bằng chứng
  tương đương byte. **(c) 5 bảng hằng lớn** → module dùng nhiều nhất + re-export 1 dòng (hàm rebase đọc globals tl).
- ★ 2 bẫy mới ghi sổ: (1) **hằng DẪN XUẤT top-level** (`_ABBREV_RE` compile từ `_ABBREV_MAP` lúc import,
  TRƯỚC khối import tl_core) → dẫn xuất phải sống CÙNG FILE với map gốc; (2) sweep chuyển nhầm `_json_dumps`
  (wrapper lõi jsonio đọc mutable-global `_DETERMINISTIC_ON`) vào ocr.py — **r61 chặn đúng thiết kế** →
  trả về tl, bổ sung PLUMB-list máy cắt.
- tl.py còn lại = plumbing/self-heal + spec-call + `_STUB_MAP` + re-export + `main` — đúng hình hài
  "tl = facade mỏng" mà chuỗi I nhắm tới. Selftest **729/729**; golden 18/18; audit strict xanh.

# ★ v1.34.17 — BACKLOG #4-#8 từ log phiên hồ sơ Luật BHXH (TDD) (2026-07-10)

- **(#4) `nlm-add` tự nhận Google Sheet**: `--type` default None; `_nlm_add_doc_type` tra MIME manifest OFFLINE
  → spreadsheet ⇒ `sheets` (hết "Could not add drive source" với phụ lục bảng tính); explicit luôn thắng.
  Parser-surface regen CÓ CHỦ ĐÍCH đúng 1 lệnh.
- **(#5) cảnh báo giá-trị-rỗng**: `_verified_reg_upsert` trả `empty_ignored` + note — webapp BỎ IM LẶNG giá trị
  rỗng cho cột thường (by-design; chỉ `nlm_*`/note clear được qua reg_clear). Đổi hành-vi-clear thật cần sửa
  webapp GAS — NGOÀI phạm vi đợt này, ghi nhận tại đây.
- **(#6) tự retry FIELDS_DROPPED**: rớt cột khi ghi nhiều trường → tự ghi lại per-field đúng 1 vòng +
  re-readback (`fields_retried`) — hết phải ghi lại tay từng lượt nhỏ.
- **(#7) `ocr-run` thiếu engine** → recommendations kèm LỆNH CÀI cụ thể (pip ocrmypdf + apt ghostscript
  tesseract-ocr-vie / hướng dẫn Windows).
- **(#8) `instruction-audit --file`** dùng CÙNG nguồn-chân-lý `gen_instructions.audit` như `--generate` —
  hết lệch block-list giữa 2 module (báo "thiếu khối" giả).
- TDD: +5 `r83` viết trước → **729/729**; golden 18/18; audit strict xanh.

# ★ v1.34.16 — Pha-E-hoàn-thiện: nhóm lệnh NGUY HIỂM lên high + contract THẬT (2026-07-10)

- **TDD**: r82 viết TRƯỚC (đỏ đúng 3 chỗ) → implement → 724/724. KHÔNG đổi CLI (parser-surface khớp).
- **3 lệnh lên `risk=high` + idempotency_contract.v1 đủ 8 field, phản ánh TRUNG THỰC gate/journal có sẵn**:
  - `profile-rebuild-registry` (tiền sự XÓA SẠCH 766 dòng 2026-06-30): contract ghi rõ KHÔNG WAL —
    phá hủy chỉ sau `--apply --confirm yes`; CLOBBER-guard + `--keep-notebook` bắt buộc;
    **rollback = Google Sheets version-history** (bài học 1.23.21) — r82 khoá riêng câu này.
  - `ingest-missing`: WAL ckpt 4 khóa done/pending/linked/fails, pending-trước-add + FRESH-verify
    (chống trùng VBHN_67×3), dedup-live tiered, overflow-route KHÔNG BAO GIỜ tạo notebook.
  - `manifest`: dẫn-xuất-tất-định từ registry (export idempotent); `--touched-drive` confirm-gate
    chống PROFILE_MANIFEST_SCOPE_BLOWUP.
- `_CONTRACT_REQUIRED` 12→15 (r65 exact-set nâng theo — drift-lock giữ nguyên tính chất: thêm lệnh ghi
  high thiếu contract là fail). Golden `tool_inventory` regen đúng 1 file (risk-counts 12→15).

# ★ v1.34.15 — I10: NÉN STUB-FARM — 488 stub → bảng _STUB_MAP + factory (2026-07-10)

- Bước 3/3 chiến-lược-chặng-cuối. **488 def ủy-quyền 2-dòng (18 module) → `_STUB_MAP` + `_make_tl_stub`**:
  giữ `__name__` (parser-surface KHỚP KHÔNG REGEN — bằng chứng bề mặt CLI bất biến), gắn `__tl_stub__ =
  (module, name)` làm định danh máy-đọc. **tl.py 5.381→3.576 (lũy kế 19.052→3.576, −81%; 15 file).**
- **Đổi cơ chế kiểm theo**: 12 wired-check r7x (getsource tìm `_tl_X.{n}`) + 9 no-dual (`count == 1`) →
  marker `__tl_stub__` + `count == 0` (tl không còn def cho tên đã stub-hoá). +`r81_stub_farm_map_complete`
  quét TRỌN map: mỗi entry phải có def thật trong module + marker đúng + __name__ đúng + không def ở tl.
- Phần còn lại của tl.py là wiring THẬT (plumbing tl_core/self-heal 611 + 35 block parser tay có chủ đích +
  spec-call + bảng hằng + main) — đích 2.500 chạm ở mức 3.6k; ép tiếp là I11 tuỳ chọn, cân nhắc lợi/hại.
- Selftest **722/722**; golden 18/18; parser-surface khớp nguyên trạng; audit strict xanh.

# ★ v1.34.14 — I9b: HOÀN TẤT I9 — resolve + regio → tl_core/ (đổi luật engine có kiểm soát) (2026-07-10)

- **`tl_core/resolve.py`** (39 def ~1.28k): ĐỘNG CƠ `_source_map_one` + amendment-gate A1/A2/A3, dedup-status,
  classify-ref, footnote/VBHN, qt5/discovery. **`tl_core/regio.py`** (63 def ~741): manifest-entries/`_entry_*`/
  norm_sohieu/`_cache_file` + journal primitives + `_journaled_reg_write`/`_verified_reg_*`/`_apply_gate`.
  **tl.py 7.177→5.381 (lũy kế 19.052→5.381, −72%; 13 module).**
- ★ **ĐỔI LUẬT CÓ KIỂM SOÁT** (đúng cam kết grilling): `r76_engine_stays_in_tl` → `r76_engine_canonical_in_resolve`
  — def THẬT ở resolve.py, tl chỉ stub, vẫn khoá 1-định-nghĩa-duy-nhất.
- **Characterization TRƯỚC cut**: +4 `r80a` khoá THÂN THẬT write-infra (lâu nay r-test toàn MOCK):
  intent{set,before} + commit-per-row theo `missed_ids` + bust-cache 1 lần; `reg_ok=False` → all-uncommitted;
  `_apply_gate` block/force-unsafe/pass; before-snapshot dịch sohieu. PASS y nguyên sau cut.
- ★ 2 bẫy mới: (a) **OFF-BY-ONE máy cắt tồn tại từ I1** — xoá từ `a-1` nuốt dòng SÁT def (lần đầu gây hại:
  `_LINHVUC_CACHE = None` → NameError; trước giờ dòng đó luôn trống nên vô hại) → fix xoá từ đúng dòng def +
  khôi phục cache ở tl + `r80_linhvuc_cache_lives_in_tl` (biến cache module-level PHẢI sống ở tl vì hàm rebase
  về globals tl); (b) mirror `_DISCOVERY_SITES` (`r80_discovery_sites_mirror`).
- +r80 wired/no-dual/mirror → selftest **721/721**; golden 18/18; parser-surface khớp; audit strict xanh.

# ★ v1.34.13 — I9a: tách INFRA đợt 1 — classify + profile_env → tl_core/ (2026-07-10)

- Bước 2/3 chiến-lược-chặng-cuối đã grill (I8 ✓ → **I9** → I10). **Đổi-luật-có-kiểm-soát**: infra đa-module
  nay sống ở tl_core (tl giữ stub, bind REBASE __globals__ — khuôn đã chứng minh qua 9 module).
- `tl_core/classify.py` (74 def ~1.22k dòng: loai/cat/title_vn/header-facts/strip-accents/sentence-case
  + misc kéo theo affinity>50%) + `tl_core/profile_env.py` (36 def ~512 dòng: config/creds/profile-env/
  GAS-webapp/transport-helper). **tl.py 8.684→7.177 (lũy kế 19.052→7.177, −62%; 11 module).**
- ★ Máy cắt I9a thêm 2 SCANNER mới: (a) **top-level scanner** — hàm được statement top-level gọi TRƯỚC bind
  phải ở lại (bắt `_ensure_writable_tmpdir`); (b) **affinity assignment** — def chưa-nhóm chỉ kéo theo khi
  >50% tham chiếu đến từ nhóm đang cắt (tránh kéo nhầm đồ của resolve/regio sang I9b).
- Characterization = 711 test HIỆN CÓ (classify/profile_env là vùng phủ dày nhất codebase — r10/r11
  title-block, _infer_loai case-list, r57 profile-env, r73a title-zone, r74a fixture-config): PASS Y NGUYÊN
  sau cut, KHÔNG sửa test nào — bằng chứng bind-rebase + stub đã trưởng thành. +r79 wired/no-dual → **713/713**;
  golden 18/18; parser-surface khớp; audit strict xanh.

# ★ v1.34.12 — I8: tách 56 def nhóm lệnh vận-hành/chẩn-đoán → tl_core/ops_misc.py (2026-07-10)

- Bước 1/3 của **chiến lược chặng-cuối đã grill** (I8 misc-cmd → I9 infra-module → I10 nén stub, đích 2.500).
- **Characterization TRƯỚC cut** (commit riêng): +4 `r78a_*` — reg-query **bare-VBHN 1-chiều** (v1.33.47);
  counts bảng-mẫu-số cùng-snapshot; exists **A3-exit-doctrine** (FOUND rc=0 / MISS rc=2 +
  NOT_FOUND_DO_NOT_CONCLUDE_ABSENT); journal đọc TL_JOURNAL_DIR. PASS y nguyên sau cut.
- **AST-cut NGUYÊN VĂN 56 def (~2.0k dòng)**: 32 cmd (doctor/ping/precheck/boot/up/perf/bench · reg-query/
  counts/exists/registry-map/cat-* · journal/undo/resume/confirm · manifest/backfill-notebook/vbhn-normalize/
  reg-delete · init-config/config-pin-registry/edit-skill/verify-integrity/instructions/instruction-audit/
  loop/cowork-plan/source-verify/profile-file-remove/convert-verify) + 24 helper riêng-nhóm.
  **tl.py 10.712→8.684 dòng (lũy kế chuỗi I: 19.052→8.684, −54%).**
- ★ Bẫy mới ghi sổ: (a) canary REQUIRED-list nằm TRONG `_skill_package_integrity` — hàm bị move nên vá canary
  trong NỘI DUNG MODULE, không phải tl.py; (b) mirror `_LOOP_LIVE_FIELDS` (bẫy default-param I2,
  drift-lock `r78_loop_fields_mirror`); (c) converter tự LOẠI def đã-ủy-quyền (thân chứa `_tl_` — 6 wrapper,
  tránh phá r7x wired-check của module trước).
- 2 guard test lịch sử (legacy-registry-doc, clobber-guard) trỏ nguồn thật ở ops_misc. +r78 wired/no-dual/mirror
  → selftest **711/711**; golden 18/18; audit strict xanh; parser-surface khớp nguyên trạng.

# ★ v1.34.11 — I7 wave-2: HOÀN TẤT bề mặt lệnh — +78 meta + 78 lệnh sinh từ GENERATED_SPECS (2026-07-09)

- **+78 COMMAND_META baseline bằng-chứng-cờ** (commit 1 riêng): chính sách grilling — `--apply` →
  `supports_dry_run=True` (doctrine mọi-lệnh-GHI-DRY-mặc-định), `--confirm` → `requires_confirm`, ghi
  ngoài-repo → `medium` + write_scope đúng đích (registry/nlm/drive), đọc-chỉ → low/none, cache/config →
  local. **KHÔNG high mới** (r65 drift-lock nguyên vẹn); nâng high+contract cho nhóm nguy hiểm
  (profile-rebuild-registry, ingest-missing, manifest --touched-drive…) = việc Pha-E-hoàn-thiện, có meta
  làm nền. validate_registry: WRITE_CMD_NO_GATE = 0.
- **Converter chạy lại: +78 lệnh → GENERATED_SPECS** (tổng 124 spec / 160 lệnh; tl.py 11.296→10.712 —
  lũy kế chuỗi I: 19.052→10.712, −44%). **Parser-surface snapshot KHỚP KHÔNG REGEN** = bằng chứng
  tương đương byte của toàn bộ 78 lệnh.
- ★ **2 bẫy converter mới — r77a bắt CẢ HAI đúng vai trò** (không lọt CI, không lọt tay):
  (a) `add_argument` HẬU-`set_defaults` (ca `sweep --live-nlm`) — block cũ gắn cờ sau set_defaults, converter
  wave-1 dừng sớm → cờ mồ côi gắn nhầm parser kế; nay tiêu thụ tiếp sau set_defaults.
  (b) `register_generated` LOẠI `dest` khỏi kwargs (schema Pha E coi `dest` = positional) → 4 cờ có `dest=`
  tường minh (`--in dest=in_file`…) bị argparse tự suy dest khác; nay dest-passthrough khi entry có `flags`.
- Còn **35 block tay CÓ CHỦ ĐÍCH**: 17 set_defaults phức (tlg.* / kwargs phụ), 9 kwarg-non-literal,
  6 foreign-stmt, 3 has-comment (giữ doctrine-comment tại chỗ). Selftest 704/704; golden 18/18; audit strict xanh.

# ★ v1.34.10 — I7 wave-1: 38 lệnh build_parser SINH TỪ GENERATED_SPECS + PARSER-SURFACE SNAPSHOT (2026-07-09)

- **Characterization TRƯỚC chuyển (commit riêng)**: `r77a` PARSER-SURFACE SNAPSHOT — SHA256 per-command của
  bề mặt parser đầy đủ (opts/dest/nargs/const/default/type/choices/required/help/metavar/kind + handler,
  đệ quy nested subparsers; KHÔNG phụ thuộc thứ tự add_parser) tại `references/golden/parser_surface.json`
  (~14KB; bản full 510KB không lưu repo). Regen có chủ đích: `TL_WRITE_PARSER_SURFACE=1 tl --selftest`
  (kỷ luật như golden --write). **Drift-lock CLI vĩnh viễn — mạnh hơn r64 nhiều bậc.**
- **Converter AST cơ học** chuyển 38 block `sub.add_parser` an-toàn → GENERATED_SPECS (flags/help NGUYÊN VĂN):
  chỉ block kwargs literal + `fn=cmd_*` trên tl + KHÔNG comment nội khối (doctrine-comment giữ tại chỗ) +
  ĐÃ có COMMAND_META 1-dòng (bất biến r64 spec⇒generated=True — flip 38 meta). tl.py **11.602→11.296** dòng.
  `register_generated` nhận spec không help. Sau chuyển: **surface khớp TỪNG HASH** (r77a) — bằng chứng
  bề mặt CLI không suy suyển.
- Sửa nguồn-vỡ-theo-bump phát hiện khi verify: `instructions --skill-version default=VERSION` nhúng số version
  vào surface → sentinel `<TL_VERSION>` trong extractor. Golden regen ĐÚNG 2 file kỳ vọng (tool-inventory
  `generated:true` ×38 + workflow_audit kernel_size ±1 byte version-string).
- **Wave-2+ còn lại** (113 block skip có lý do): 78 thiếu COMMAND_META (việc hoàn tất Pha E — thêm meta trước
  rồi chuyển), 17 set_defaults phức, 9 kwarg non-literal, 6 foreign-stmt, 3 has-comment.

# ★ v1.34.9 — I6: tách 16 cmd tra-cứu/quan-hệ → tl_core/lookup_ops.py (động cơ Ở LẠI tl) (2026-07-09)

- **RANH GIỚI GRILLING (quyết định user)**: động cơ resolution `_source_map_one` (365 dòng, 59 điểm test,
  amendment-gate A1/A2/A3) + helper đa-module (`_dedup_status`/`_classify_ref`/`resolve_footnote_amendments`/
  `_relation_audit`/`_rq_relation_probe`/`_scan_inline_amendments`/`_sohieu_query_hits_entry`/`_nlm_status_*`)
  **GIỮ Ở TL** — test mới `r76_engine_stays_in_tl` khoá cứng (def thật trong tl.py, không được stub hoá).
- **Characterization TRƯỚC cut**: +3 wiring `r76a_*` khoá SHELL cmd quanh engine — source-map canonical shape
  + alias results==items + verdict/qt5_queries top-level; MISS vẫn rc=0 (A3 rc-doctrine); status --amendment
  guard offline SKIP + AMENDMENT_ALREADY_IN_CORPUS_ON_NLM. PASS y nguyên sau cut.
- **AST-cut NGUYÊN VĂN 41 def (~1.57k dòng)** → `tl_core/lookup_ops.py`: 16 lệnh (locate, source-map, status,
  relation-check/backfill, vbhn-check/verify/compare, xref, footnote-map, cluster, rasoat/rasoat-loop/
  rasoat-chongcheo, header-verify, dedup-check) + 25 helper riêng-cụm. tl.py 13.176→**11.602 dòng**.
- Scanner default-param 0 hit; self-heal phủ module mới (canary/tl_boot/py_compile+REQUIRED/r36).
  +r76 wired/no-dual/engine-stays → selftest **703/703**; golden 18/18 khớp nguyên trạng; audit strict xanh.

# ★ v1.34.8 — I5: tách ingest_pipeline → tl_core/ingest_ops.py (test-first, cụm ghi chính) (2026-07-09)

- **Characterization TRƯỚC cut**: +5 wiring `r75a_*` OFFLINE cho 5 cmd 0-hit — ingest-route cây quyết định
  (ASK_USE_EXISTING / PROFILE_OWN); ingest-analyze `--text-file` letterhead → plan + lệnh `ingest-local
  --auto-plan` điền sẵn; source-rename DRY gợi ý tên chuẩn + không gọi gas; shared-source-fix DRY group;
  **register --bulk GUARDS P0-1** (drive_id cắt cụt / cat rác → rc=2, KHÔNG post). PASS y nguyên sau cut.
- **AST-cut NGUYÊN VĂN 37 def (~1.76k dòng)** → `tl_core/ingest_ops.py`: 12 lệnh (ingest-local, profile-ingest,
  ingest, ingest-analyze, ingest-route, ingest-missing, register, recat, source-rename/delete/update-corpus,
  shared-source-fix) + 25 helper riêng-cụm (classification `_classify_doc_header`/`_sohieu_from_title_zone`
  vừa vá v1.34.6, verify-gate, chunk, mime, checkpoint, plan-helper). tl.py 14.932→**13.176** dòng
  (lũy kế chuỗi I: 19.052→13.176 qua 7 module).
- **WRITE-INFRA đa-module GIỮ Ở TL** (đếm-tham-chiếu: hygiene+nlm_ops+profile_mgmt cùng dùng):
  `_journaled_reg_write`/`_apply_gate`/`_verified_reg_upsert`/`_reg_before_from_manifest`.
- 3 test getsource (recat 1.23.6, r55 ingest-local, clobber-guard đã sửa ở I4) trỏ nguồn thật ở module.
  +r75 wired/no-dual → selftest **697/697**; golden 18/18 khớp nguyên trạng; audit strict xanh.

# ★ v1.34.7 — I4: tách profile_mgmt → tl_core/ + FIXTURE-CONFIG (golden ops-plan hồi sinh) (2026-07-09)

- **FIXTURE-CONFIG tất định** (`fixtures/config_fixture.json` sinh-tại-chỗ, 2 profile, registryDocId pin sẵn) —
  giải bài cách-ly-config từ CI I1: golden **ops-plan HỒI SINH** (`hygiene_ops_plan_fixture_config`: `--config`
  fixture + xoá env `TL_*` per-case → cross-machine; không chứa path máy, ổn định ×2). Fixture dùng lại được
  cho mọi case cần config.
- **Characterization TRƯỚC cut**: +4 wiring `r74a_*` trên fixture config — profile-list; profile-info
  **CHỊU-LỖI-GÕ** ('ho_so_74'→'Hồ sơ 74', khoá P2 v1.33.48); profile-use DRY-không-ghi-config +
  PROFILE_NOT_FOUND rc=2; profile-rename DRY plan + cấm rename profile nền. PASS y nguyên sau cut.
- **AST-cut NGUYÊN VĂN 22 def (~967 dòng)** → `tl_core/profile_mgmt.py`. tl.py 15.743→**14.932** dòng.
  Hạ tầng profile dùng chung (`_apply_profile_env`/`_profile_lookup`/`_read_config_record`/
  `_persist_profile_config`/`_profile_policy_error`/`_active_profile`…) GIỮ Ở TL (đếm-tham-chiếu).
  Test clobber-guard trỏ nguồn thật ở module. +r74 wired/no-dual → selftest **690/690**; golden 18/18
  khớp nguyên trạng; audit strict xanh.

# ★ v1.34.6 — vá 3 defect profile văn-bản-thường (log phiên hồ sơ Luật BHXH 2026-07-09) (2026-07-09)

- **(#1 — ghi sai metadata âm thầm)** `_classify_doc_header` hết nhận số hiệu TRÍCH DẪN làm số hiệu tài liệu:
  sohieu CHỈ lấy từ **vùng tiêu đề** (head 1500 — cùng vùng draft-marker N2b) trên **DÒNG NGẮN ≤80 ký tự** kiểu
  letterhead (ưu tiên có `Số:` đứng trước — helper mới `_sohieu_from_title_zone`) + tên file. Số hiệu nằm trong
  câu văn dài = trích dẫn văn bản khác → BỎ. Ca thật: báo cáo Thái Nguyên nhắc "Luật số 41/2024/QH15" bị gán
  `loai=Luật, sohieu=41/2024/QH15`. Nhánh VBHN N2a nay chạy CẢ khi sohieu vùng-tiêu-đề rỗng (layout VPQH in số
  ở khối ký cuối — quét sâu 16k CHỈ cho dạng số VBHN).
- **(#3 — gate áp nhầm)** `_ingest_verify_gate`: bỏ vế `or có sohieu` — `requires_dieu` CHỈ theo
  `kind ∈ {vbqppl, draft, nq}`. Văn bản thường (kể cả có số hiệu công văn 123/BC-UBND) không còn bị
  `DIEU_STRUCTURE_NOT_VERIFIED` chặn `corpus_allowed` → profile-ingest đi trọn pipeline tự động (hết cảnh
  nlm-add tay 6 nguồn). +info flag `DIEU_NOT_REQUIRED_NORMAL_DOC`. VBQPPL/draft/NQ giữ nguyên độ chặt.
- **(#2 — .xlsx gãy convert)** bảng tính trọn đường ống: `_MIME_BY_EXT` +`.xlsx/.xls` (trước rơi về DOCX_MIME →
  "Conversion ... not supported"); profile-ingest nhánh sheet: `copy_convert toType=sheets` → canonical =
  **Google Sheet** + readback mime sheet (param mới `expected_gdoc_mime`) + NLM `source_add doc_type=sheets`
  nội bộ + bỏ text-gate (`SPREADSHEET_TEXT_VERIFY_SKIPPED`). CLI `nlm-add --type` public không đổi (backlog #4).
- TDD: 7 test `r73a_*` hành-vi-đúng viết TRƯỚC (4 đỏ đúng chỗ, 3 chống-thụt-lùi xanh) → fix → **684/684**.
- **BACKLOG còn lại từ log phiên** (chưa vá đợt này): #4 nlm-add auto-detect type theo mime Drive; #5 register
  clear cột thường (cần đổi webapp GAS + API_CONTRACT); #6 register auto-retry khi FIELDS_DROPPED_ON_WRITE;
  #7 ocr-run báo rõ lệnh cài engine (ocrmypdf/ghostscript/tesseract-vie); #8 instruction-audit lấy block-list
  từ gen_instructions (single source of truth); #9 user sửa Project Instruction (đang ghi 1.33.43, thực tế
  1.34.6); #10 di trú `vbthuong categories: inherit→own` (cần user duyệt).

# ★ v1.34.5 — I3: tách extract_cache + fetch_web → tl_core/ (test-first, 2 module) (2026-07-09)

- **Characterization TRƯỚC cut**: +5 wiring-test `r72a_*` OFFLINE — extract resolve-canonical THẬT từ manifest
  fixture + bóc đúng Điều (transport mock); tvpl-url pure (khoá hành vi `quote` giữ `/`); fetch-route VBHN-first
  + docx-rank TVPL#1; fetch-batch phân SKIP_DEDUP/REVIEW_DEDUP/FETCH + checkpoint; fetch-links markdown bấm-được
  + _HOP_NAP + env-aware. PASS y nguyên sau cut.
- **AST-cut NGUYÊN VĂN 15 def (~603 dòng)** → `tl_core/extract_cache.py` (cmd_extract/cache-build/cache-snapshot)
  + `tl_core/fetch_web.py` (fetch-route/batch/links, find-doc, tvpl-url, external-ingest, link-priority,
  frontier-expand + _fetch_plan/_external_ingest_plan/_frontier_*). tl.py 16.227→15.743 dòng.
- **Ranh giới đếm-tham-chiếu (đúng khuôn I2)**: hạ tầng đọc (`_read_doc_text` 16 site, `_cache_file` 13,
  `_title_block_from_text` 6, `extract_dieu`/`extract_refs`/`_extract_header_facts`/`_sanitize_export_text`/
  `_profile_cache_dir`) và hạ tầng discovery QT-5 (`_query_variants`/`_google_site_url`/`_discovery_links`/
  `_official_rank` + `_FETCH_SOURCES`/`_DISCOVERY_SITES`/`HOPNAP_FOLDER_ID`) **GIỮ Ở TL** — cụm extract thực chất
  phần lớn là read-infra dùng chung, chỉ 3 lệnh CLI tách được.
- Cut script nay có **SCANNER bẫy default-param** (bài học I2, quét AST defaults tham chiếu Name) — 0 hit đợt này.
  Self-heal phủ 2 module mới (canary/tl_boot preload/py_compile+REQUIRED/r36). +r72 wired/no-dual → selftest
  **677/677**; golden 17/17 khớp nguyên trạng; audit strict xanh.

# ★ v1.34.4 — I2: tách cụm nlm_wrappers/sharding → tl_core/nlm_ops.py (test-first) (2026-07-09)

- **Characterization TRƯỚC cut** (commit riêng): +5 wiring-test `r71a_*` OFFLINE (mock `_imp`/`_gas`/registry-IO
  trên tl — bind REBASE nên patch thấm cả sau cut) khoá 5 cmd 0-hit-selftest: nlm-list shape JSON; nlm-reconcile
  DRY phân 3 lớp desync_real/other_notebook/unregistered; preflight ⚠DUP-TL lỏng-năm (L4) + verify-LIVE slot khi
  FULL (L5); push-overflow verified-write; overflow-resolve MAX(registry,physical) + discover shard + gap.
  PASS y nguyên sau cut.
- **AST-cut NGUYÊN VĂN 28 def (~1.0k dòng)** → `tl_core/nlm_ops.py`: 13 lệnh (nlm-list/get/query/cross/content/
  add/orphans/reconcile/query-plan, preflight, push-overflow, overflow-resolve, slot-audit) + 15 helper riêng-cụm.
  tl.py 17.097→16.227 dòng. **Ranh giới đo bằng đếm-tham-chiếu-ngoài-cụm**: helper đa-cụm GIỮ Ở TL
  (`_entry_on_nlm_live` 16 site, `_resolve_nlm_notebook` 6, `_nlm_display`, `_nlm_probe_summary`,
  `_nlm_status_known/removed`, `_gws_nlm_note`, `_entry_nlm_notebook_id`).
- ★ **Bẫy mới cho I3+**: default-param (`cap=NLM_SLOT_CAP` của `_overflow_status`) eval lúc ĐỊNH NGHĨA module —
  TRƯỚC bind → NameError khi import. Module cần MIRROR constant + drift-lock `r71_slot_cap_mirror`
  (nlm_ops.NLM_SLOT_CAP == tl.NLM_SLOT_CAP).
- Self-heal phủ module mới (canary/tl_boot preload/py_compile+REQUIRED/r36); r69 nlm-add source-check trỏ nguồn
  thật ở nlm_ops. +r71 wired/no-dual/slot-cap-mirror → selftest **670/670**; golden 17/17 khớp nguyên trạng
  (ổn định ×3); audit strict xanh.

# ★ v1.34.3 — I1: tách cụm hygiene_report → tl_core/hygiene.py (test-first, golden khớp nguyên trạng) (2026-07-09)

- **Characterization TRƯỚC cut** (commit riêng để bisect): 6 golden `hygiene_*` offline trên FIXTURE MANIFEST
  (case golden nay mang env riêng — `_run_tl_json +env_extra`, `TL_CACHE_DIR` trỏ `fixtures/cache_hygiene`
  sinh-tại-chỗ, gài đủ defect cho detector nổ). Bắt ngay 1 bug thật: sweep phơi `snapshot_age_s` lọt
  deterministic mask → ×2 lệch byte cùng máy (cùng lớp age_days v1.33.56) → +`snapshot_age_s/age_s/age_seconds`
  vào VOLATILE_JSON_KEYS.
- **AST-cut NGUYÊN VĂN 29 def (~2.0k dòng)** → `tl_core/hygiene.py`: 16 lệnh (sweep, dedup-plan,
  missing-sohieu, vbhn-year-fix, ops-plan, corpus-audit, review-queue, backfill-loai/title-vn/hieuluc,
  hygiene, quarantine-fix, corpus-fix, consolidation-cleanup, cat-audit, registry-doctor) + helper riêng-cụm.
  tl.py 19.052→17.097 dòng; tl giữ STUB ủy quyền mọi tên (mọi caller cũ + tl_selftest bind giữ nguyên).
- ★ `bind()` của hygiene KHÁC sibling-module: **REBASE `__globals__` từng hàm về namespace SỐNG của tl** —
  monkeypatch của selftest trên tl ăn ngay, helper không stale (copy-snapshot kiểu cũ làm r54 gãy: patch
  `_manifest_entries` trên tl không thấm vào module). Bài học cho I2..In.
- Golden 18/18 **KHỚP NGUYÊN TRẠNG** sau cut (không regen — bằng chứng cắt nguyên văn). Self-heal phủ module
  mới: canary core list, tl_boot preload, py_compile + REQUIRED (release-check), r36. +r70 parity
  (wired + no-dual-definition); test missing_sohieu_reg_bulk trỏ nguồn thật ở hygiene → selftest **662/662**.

# ★ v1.34.2 — Pha H live-smoke PASS (apply_ready=true LẦN ĐẦU) + vá 4 phát hiện smoke (2026-07-09)

- **Pha H hoàn tất trên máy user**: 17/17 bước live-smoke-plan, rc thật từng bước. Ghi thật 2 bước HIGH
  (ingest-local + profile-ingest --allow-default) rồi DỌN NET-ZERO: 3× source-delete --apply --confirm yes
  (journal) + xoá NLM source mồ côi + trash sidecar docx → diff cuối so before `{changed:0, unexpected:0}`;
  diff đó làm smoke-proof → `live-readiness --smoke-proof` = **apply_ready=true cả 3 tier, deployment_allowed=true**.
  Tập sống thêm: ingest --resume nối journal sau đứt mạng; overflow-route khi shard chính ĐẦY THẬT (306/300);
  guard chống-ghi-profile-nền; zip-apply CONFIRM_REQUIRED; nlm-reconcile DRY bắt đúng nguồn unregistered.
- Vá 4 phát hiện smoke (chính sách grilling: lỗi nhỏ rõ nguyên nhân → vá ngay kèm test):
  (a) `reg-query --drive-id` MỚI — 10 idempotency contract dặn readback `reg-query --drive-id` mà parser
  thiếu cờ (drift doc↔CLI); (b) `nlm-add --drive-id`: add OK + row registry TỒN TẠI → **reg_link ngay**
  (journaled+verified-write, chỉ cột nlm_*; không row → nhắc register/nlm-reconcile, không tạo row xương) —
  hết ca nguồn 'unregistered' khi nlm-add đứng một mình (S14); (c) live-smoke-plan bước snapshot_diff
  +2 allow-prefix đúng path thật snapshot (`live_contract_report.nlm.notebook_get.source_count`,
  `live_contract_report.contract_checks`) — hết diff 'unexpected' oan; (d) contract text khớp parser:
  source_delete resume +`--apply`, reg_delete dùng `--drive-ids`, nlm_add ghi rõ không có `--json`.
- Selftest +4 r69 (flag/reg_link-wired/allow-prefix/contract-text) → **660/660**.

# ★ v1.34.1 — siết-6 advisory: contract THẬT, HẾT grandfather (đúng deadline r65 'trước v1.34.1') (2026-07-09)

- 6 contract `idempotency_contract.v1` mới (đủ 8 field, PHẢN ÁNH hành vi gate+journal+verified-write đã có
  trong code từ v1.29.2 — KHÔNG đổi bề mặt CLI, quyết định grilling 2026-07-09 #6): `register`, `drive_push`
  (builtin_gate md5 + guard BUNDLE_META ADR-0001 ghi thành văn), `nlm_reconcile`, `push_overflow`,
  `shared_source_fix`, `source_update_corpus`. Commit 2 đợt (3+3) để bisect được, mỗi đợt gate xanh.
- `_CONTRACT_REQUIRED` = TRỌN 12 lệnh ghi high-risk (Pha G 6 + siết-6); registry.warnings advisory → RỖNG;
  nhánh warning giữ làm lưới cho lệnh ghi high-risk MỚI quên contract.
- COMMAND_META: `requires_confirm=True` cho `shared-source-fix`/`source-update-corpus` (khớp code
  `--apply --confirm yes` — metadata nói thật).
- Selftest: r65_contract_required_six_wired → 12-set; r65_grandfather_advisory_exact_set → set RỖNG
  (drift-lock giữ nguyên ngữ nghĩa); +r68_contract_siet6_wired_and_complete (key meta↔contracts + đủ 8 field)
  +r68_confirm_meta_matches_code → 656/656. Regen golden tool_inventory/workflow_audit (nhúng registry).

# ★ v1.34.0 — Pha F: SKILL.md kernel (user duyệt phương án (a) 41.8KB — grilling #3 'draft-trước-duyệt-sau') (2026-07-09)

## Vá doctrine-loss check (2026-07-09, TRƯỚC deploy — vẫn v1.34.0 vì chưa từng LIVE)

- Workflow 3-reviewer + skeptic đối chiếu ad413e7:SKILL.md ↔ bộ mới: **6 finding CONFIRMED** (F1/Z3-01 P1;
  F3/F4/F5/Z3-02 P2), 4 bị skeptic bẻ (F2/F6/Z3-03/V2-01-phần-loss). Nguyên nhân gốc: mapping hàng 5 khai
  "RUNBOOK §A đã có nội dung tương đương" — SAI cho dải old 164-185 (RUNBOOK §A0/§A4 giữ bản CŨ đối nghịch:
  'Chat SKIP/Drive MCP', header A4 thiếu Chat).
- **KHÔI PHỤC NGUYÊN VĂN dải old 164-185 vào kernel §1** (F1 MÔI TRƯỜNG THỐNG NHẤT; F5 nguyên tắc NLM-CLI
  BẮT BUỘC mọi env; F4 cấm notebook_create điều-kiện-kép; F3 ⚠DUP-TL lỏng-năm; L6 khôi phục kèm cho trọn khối)
  + xoá fence ```bash mồ côi (F6 render bug). Kernel 41.7→46.6KB (trần 48KB).
- Doctrine rút gọn +2 bullet nguyên văn: Z3-01 luật `golden-test --write` (CẤM xanh-hóa gate đỏ);
  Z3-02 snapshot/report vận hành → `.tl_state/`.
- V2-01: dòng "Quy tắc chung" kernel phóng đại `--json/--out` thành cờ toàn cục — SAI so parser (probe:
  `tl --json …` rc=2, `exists --out` unrecognized) → sửa về đúng: chỉ `--profile/--config/--deterministic`
  toàn cục. MAPPING hàng 5 cập nhật ghi rõ tách-đôi.

- SKILL.md 91KB → **kernel 41.6KB**: lắp bằng TRÍCH NGUYÊN VĂN các khối bất biến (§0 Nguyên tắc, §1 Khởi động
  kèm BƯỚC-0 curl, §2 Cổng vận hành, GATES + PHÁT HÀNH & NHÁNH, v1.17.26 gate) + khối pointer viết tay.
  KHÔNG câu doctrine nào bị viết lại lời (lựa chọn (a) của user — an toàn ngữ nghĩa trên hết).
- Nội dung chuyển đi (nguyên văn): §4 bảng lệnh 27KB → `references/COMMANDS.md`; §9 phụ thuộc 13.3KB →
  `references/DEPENDENCIES.md`; chú giải khởi động dài → đã có RUNBOOK §A; Stage4/5 → doctrine rút gọn
  (chi tiết ở workflow cards). Bảng đối chiếu 12 mục: `references/SKILL_KERNEL_MAPPING.md`.
- CHANGELOG 458KB cắt còn từ v1.33.54 (8 version + entry này); phần cũ NGUYÊN VĂN →
  `references/changelog_archive/CHANGELOG-den-1.33.53.md`.
- Chống-phình: workflow-audit +2 check `kernel_size` (fail nếu SKILL.md > 48KB) và `kernel_links`
  (mọi đường dẫn references/ nhắc trong kernel phải tồn tại) — r67 khoá.
- Xoá `references/SKILL_KERNEL_DRAFT.md` sau promotion (tránh 2 bản doctrine trôi dạt — đúng lớp anti-pattern
  bundle-trùng-số đã cấm); MAPPING giữ làm hồ sơ.
- ⚠ SAU DEPLOY: user PHẢI re-import zip vào Cowork Settings→Capabilities (đổi lớn doctrine).

# v1.33.61 — CI-fix #2: khử nốt 2 lớp bug máy-phụ-thuộc (2026-07-09)

- (a) `idempotency_key` ingest-zip hash bytes CONTAINER zip → `zipfile` 3.12 (CI) ≠ 3.13 (local) ghi header
  khác → key lệch dù ZIP_STORED. Đổi **content-v2**: norm_path+CRC32+size từng member accepted (CRC sẵn
  trong central directory — 0 IO; re-zip cùng nội dung = CÙNG key, đúng ngữ nghĩa idempotency hơn).
  r66 khoá: STORED vs DEFLATED cùng nội dung → cùng key. Contract text cập nhật (dict + card + golden).
- (b) 3 writer atomic thiếu `newline=` → Windows ghi CRLF (writer PHỤ THUỘC OS = bug determinism gốc) →
  release-verify windows-CI fail (manifest hash CRLF vs checkout LF). +`newline` LF mọi OS (r66 khoá);
  `.gitattributes` `* -text` khoá byte toàn repo; renormalize 27 file CRLF di sản; regen goldens LF.
- Selftest 653/653 (+2 r66). Runtime-identical — không deploy riêng, ship cùng v1.34.0.

# v1.33.60 — CI-fix: fixture zip ZIP_STORED (2026-07-09)

- CI run #1 (ubuntu+windows) bắt đúng lớp bug nó sinh ra để bắt: DEFLATE bytes khác nhau giữa build zlib
  (Ubuntu zlib-ng ≠ Windows) → sha256(zip fixture) trong idempotency_key lệch 2 golden `ingest_zip_dryrun_*`.
- `_golden_ensure_fixtures` chuyển ZIP_STORED — bytes máy-độc-lập thật; regen 2 golden. Runtime-identical,
  không deploy riêng (ship cùng v1.34.0).

# ★ v1.33.59 — Pha G: drift-test expansion + siết gate (thực thi 9 quyết định grilling 2026-07-09)

- **Siết-6 (quyết định #6):** contract idempotency THẬT cho nlm-add/recat/source-rename/source-delete/
  reg-delete/dedup-plan (journal_key, resume, readback, rollback từng lệnh — khớp cơ chế thật: dedup-live
  gate của nlm-add, before-cat trong journal recat, Trash-30-ngày của source-delete…); `_CONTRACT_REQUIRED`
  → thiếu contract = FAIL-strict. 6 legacy còn lại (register, drive-push, nlm-reconcile, push-overflow,
  shared-source-fix, source-update-corpus) advisory với DEADLINE trước v1.34.1; r65 drift-lock đúng-set
  (thêm lệnh ghi high-risk mới mà quên contract → selftest đỏ).
- **bundle-export + guard (quyết định #2, ADR-0001):** `tl bundle-export` zip giữ VERSION fork-point +
  BUNDLE_META.json nhúng TRONG zip (không ghi ra cây); `drive-push` từ chối cây có BUNDLE_META.json
  (BLOCKED_BY_BUNDLE_META rc=3, `--force` thoát tường minh); card workflow chuẩn schema v1 + registry meta
  + GENERATED spec; BUNDLE_META vào .gitignore + _RELEASE_EXCLUDE_NAMES.
- **Golden nâng cấp (quyết định #7 — đóng nợ P4-06):** check `raw_stable` (stdout THÔ chạy ×2 trùng byte,
  bắt nondeterminism format thật) + `raw_sha256` ghi vào record; token `{FIXTURES}`; +6 case offline-thuần
  trên fixtures cố định: chunk-plan profile, chunk-plan vbqppl-canonical BỊ CHẶN, ocr-analyze, ingest-zip
  dry-run zip-slip + tên-cấm-Windows, ingest-zip duplicate-normalized, live-state-diff no-changes. Harness
  chấp nhận JSON dict bất kể rc (case NEGATIVE rc=2 có chủ đích). Goldens cũ regen: diff ngữ nghĩa = 0
  (đối chiếu key-level), chỉ rewrite EOL do .gitattributes mới khoá byte golden dir.
- **CI (quyết định #8):** .github/workflows/ci.yml — ubuntu + windows, full gate (py_compile, 2 selftest,
  3 audit, release-verify, bundle ×2 cùng SHA, tl_boot smoke); autocrlf OFF trước checkout (hash parity
  manifest); `.github` excluded khỏi manifest/zip (dev-side).
- Selftest **651/651** (+4 r65: siết-6 wired, advisory exact-set, bundle-export meta+guard+--force,
  {FIXTURES} substitution).

# ★ v1.33.58 — Pha E kế hoạch nợ-kỹ-thuật: command registry (2026-07-09)

- **E1 `tl_core/command_registry.py`** (module THUẦN — không bind): metadata 52 lệnh (31 determinism-era +
  21 legacy write high-risk): risk · read_only · write_scope · requires_confirm · supports_dry_run ·
  deterministic_json_required · workflow_task · idempotency_contract · card_required · module · builtin_gate.
- **E2 (incremental đúng kế hoạch):** 8 lệnh determinism đơn giản (tool-inventory/route-task/workflow-audit/
  golden-test/determinism-audit/release-manifest/-verify/-bundle) SINH parser từ `GENERATED_SPECS` —
  flags/help giữ NGUYÊN VĂN, handler qua stub tl, `--profile/--config/--deterministic` vẫn do vòng inject
  phủ; build_parser bớt 8 block tay. Phần còn lại chuyển dần các pha sau.
- **E3:** tool-inventory đính `registry` (registry_summary — counts + metadata từng lệnh, sort tất định).
- **E4:** workflow-audit gọi `validate_registry`: lệnh-trong-registry phải có trong parser; handler generated
  khớp; **lệnh GHI NGOÀI-repo (drive/registry/nlm/live) phải có ≥1 gate** (contract/confirm/dry-run/
  builtin_gate — nlm-add=dedup-live-gate, drive-push=md5-verify-fixed-fileId; ghi artifact LOCAL miễn);
  card_required → card phải load được; contract key phải tồn tại; **JSON-through-gate**: scan source handler
  thật trong module — lệnh mới phải đi qua _json_dumps/_print_json_or_text/_emit_json_payload.
- **Grandfather có kiểm soát:** 12 advisory (legacy write thiếu idempotency contract + contract chưa được
  lệnh nào tham chiếu) nằm ở `registry.warnings` — KHÔNG merge vào warnings strict (nợ đã biết, Pha G siết).
- Hiệu chỉnh theo thực tế khi validate lần đầu: determinism-audit card → workflow_audit (không có card riêng);
  live-state-snapshot read_only=True (chỉ ghi report local).
- Golden regen: tool_inventory (+registry section 531 dòng) + workflow_audit (+20). Hạ tầng phủ module mới:
  canary + tl_boot preload + py_compile + REQUIRED_FILES + r36.
- **Gate:** selftest **647/647** (+3 r64: validate-clean, generated-parser-behavior kể cả required/positional,
  meta-invariants); workflow-audit --strict ✅ · golden-test ✅ · determinism-audit --strict ✅ ·
  gen_instructions 24/24 ✅ · release-bundle ×2 CÙNG SHA ✅ · tl_boot smoke ✅. Kế hoạch: A-E ✓ → F (SKILL.md
  kernel, v1.34.0 — cần user duyệt + re-import Cowork), G drift-test, H live-smoke.

# ★ v1.33.57 — Pha D kế hoạch nợ-kỹ-thuật: tách tl_core/{zip_ingest,ocr,chunking} (2026-07-08)

- tl.py **19.840 → 19.051 dòng** (−789; lũy kế từ Pha B: 21.312 → 19.051). Modules mới: `zip_ingest.py` (235 —
  plan/safe-extract/zip-slip+dup guard/apply fan-out), `ocr.py` (470 — analyze/run/verify, manifest v1, page
  report, bridges ingest-ocr/profile-ingest-ocr), `chunking.py` (276 — plan/apply/verify, ranh giới Điều,
  profile-ingest-chunks).
- Cùng máy Pha C (AST-span + bind copy-globals + 21 stub ủy quyền, CLI KHÔNG đổi) + nâng cấp: quét tham chiếu
  tính CẢ `tl_core/*.py` (release.py đang gọi `_zip_plan`/`_zip_sorted_infos` qua bind → stub tự sinh đúng).
- Helper dùng chung ≥2 module GIỮ Ở tl.py theo quy tắc an toàn: `_run_child_tl`, `_read_local_text_for_analysis`,
  `_text_quality_metrics`, `_sha256_bytes_file_local`, `_VIET_CHARS`, `_bridge_confirm_apply`, `_write_text_atomic`.
- **Điều chỉnh D4 (idempotency.py):** KHÔNG tạo module riêng — contracts đã nằm ở `workflow.py` từ Pha C
  (tool-inventory/route-task tiêu thụ tại đó), key/resume/readback builders đi theo lệnh sở hữu; tách thêm
  chỉ tạo churn không giảm rủi ro.
- Hạ tầng self-heal phủ 3 module mới: canary `_skill_package_integrity` (+3), tl_boot preload strip-NUL (+3),
  release-check py_compile (+3), `_RELEASE_REQUIRED_FILES` (+3), r36 mock + r61 no-bare-mutable (+3).
- **Gate:** selftest 644/644 (r63 chunk-roundtrip/zip-caps chạy XUYÊN stub mới — parity tự chứng minh);
  workflow-audit --strict ✅ · golden-test ✅ · determinism-audit --strict ✅ · gen_instructions 24/24 ✅ ·
  release-bundle ×2 CÙNG SHA-256 ✅ · tl_boot smoke ✅. Kế hoạch: A✓ B✓ C✓ D✓ → E (command registry) = 1.33.58.

# ★ v1.33.56 — Pha C kế hoạch nợ-kỹ-thuật: tách tl_core/{workflow,release,live} + rà lỗi tiềm ẩn (2026-07-08)

## Tách module (tl.py 21.266 → 19.761 dòng, −1.505)
- `tl_core/workflow.py` (513 dòng): _TOOL_GROUPS/_TASK_TO_WORKFLOW/_IDEMPOTENCY_CONTRACTS, cards/schema/golden,
  tool-inventory, route-task, workflow-audit, golden-test.
- `tl_core/release.py` (533+ dòng): determinism-audit, release-check/-manifest/-verify/-bundle, exclude rules,
  zip-write deterministic, _run_release_child.
- `tl_core/live.py` (680 dòng): live-readiness/contract-check/state-snapshot/state-diff, smoke-plan,
  deploy-plan, rollback-plan, final-acceptance, go-live-runbook (+_mask_secret/_smoke_proof_state/… cụm-riêng).
- **Cơ chế an toàn:** cắt NGUYÊN VĂN theo AST-span (kèm comment liền trước); `bind(tl)` copy-globals bỏ-tên-đã-có
  (def riêng module thắng, hàm tl là hàm THẬT — không snapshot-stale); 26 stub hàm + 2 alias hằng trong tl cho
  phần còn lại/selftest/parser; tham chiếu CHÉO giữa 3 module đi qua stub tl (release→workflow/live 6 tên,
  live→release 1 tên); helper chỉ-moved-code-dùng tự móc theo (quy tắc referenced-only-by-one-module, 14 helper).
  Public CLI KHÔNG đổi; module cấm đọc bare mutable-global của tl (khoá bằng r61).
- Extraction bằng script AST tự sinh (assert mọi giả định: span, chồng lấn, 2-tên-1-statement, module-đơn-nhất).

## Rà lỗi tiềm ẩn — workflow review 5 phân hệ (37 agent, adversarial verify): 31 CONFIRMED, vá 30, defer 1
### 🔴 ROOT-CAUSE flake determinism-audit (3 lần 'ok:false không tái hiện') — CHỐT + TẮT
- Wiring mới `reports/determinism_report.json` khi strict-fail BẮT ĐƯỢC flake ngay lần chạy chuỗi kế tiếp:
  giữa 2 snapshot con, `auth.gws_credentials.age_days` nhảy bucket 0.001-ngày (86.4s) → live-state-diff báo
  unexpected (~5%/lần — khớp tần suất 3 lần quan sát). Vá kép: (a) `_strip_snapshot_volatile` bỏ CẢ key
  volatile ở LEAF (đúng luôn cho live-smoke thật với file snapshot raw); (b) snapshot `--out` ghi bản SCRUB
  khi deterministic. Stress chuỗi ×5 sau fix: 5/5 PASS (+r62 khoá).
### P0 (2, trùng nhau — 2 finder độc lập cùng bắt)
- `_run_child_tl` decode stdout con bằng LOCALE (cp1258 máy VN) trong khi con LUÔN in UTF-8 → UnicodeDecodeError
  → cp.stdout=None → TypeError KHÔNG được bắt: CẢ HỌ lệnh bridge (ingest-zip apply, ocr/chunk kể cả DRY-RUN)
  chết trên chính máy user với bất kỳ output có 'Đ/ề/ố'; nạp dở Drive/NLM giữa batch. Verifier reproduce
  end-to-end. Vá: encoding='utf-8' + errors='replace' + bắt TimeoutExpired (audit-path _run_tl_json vốn đúng
  — bundle tự viết đúng ở gate, sai ở apply-path nên gate mù).
### P1 đã vá (9)
- ingest-zip --apply nạp CẢ file plan đã loại FILE_TOO_LARGE (extract tự suy tập file, không kiểm size) →
  extract nhận max_size_mb (+r63). · Tên member zip chứa ký tự cấm Windows ('?<>|*:', control) lọt plan →
  unsafe ngay tại plan (+r63). · --config (và --profile mode vbqppl) KHÔNG forward xuống child fan-out →
  child đọc config MẶC ĐỊNH ở gốc → sai đích (đúng lớp 'ghi nhầm corpus' v1.33.48) → forward cả hai. ·
  chunk-plan cap 5M ≠ apply/verify 10M → plan cắt cụt âm thầm → thống nhất 10M. · Cards/_nlm_query_plan/
  contracts khuyên cờ KHÔNG TỒN TẠI (`ingest-local --json`, `nlm-cross --source-id`) → agent làm theo là rc=2:
  +--json no-op 4 lệnh (tiền lệ nlm-get v1.33.18) + sửa chuỗi nlm-cross → --notebooks + regen 2 golden. ·
  6 subparser tự khai --profile/--config default=None đè mất root-position → SUPPRESS (+r63). ·
  live_contract_ready=true dù nhánh NLM fail ghi check-id NGOÀI required set (false-green deploy) → +3 id vào
  required. · determinism-audit GHI ĐÈ before.json THẬT của user ở repo root (kill giữa write→restore = mất
  baseline) → probe tên riêng `.__det_audit_probe__.json` excluded + từ chối nếu tồn tại. · tl_core = ĐIỂM-CHẾT-ĐƠN
  mới không lớp self-heal nào phủ (tl_boot chỉ strip NUL tl.py; canary không liệt kê tl_core) → canary
  _skill_package_integrity +6 file tl_core; tl_boot PRELOAD bản strip-NUL của tl_core vào sys.modules; import
  tl_core trong tl.py qua helper in remediation rõ (rc=3) thay vì SyntaxError trần.
### P2 đã vá (12)
- OCR manifest JSON-hợp-lệ-nhưng-không-phải-object → lỗi sạch thay AttributeError (+r63). · chunk-verify
  split('---',2) vỡ khi path chứa '---' → neo delimiter theo DÒNG (+r63 end-to-end). · Ranh giới 'Điều N.'
  nhận cả THAM CHIẾU wrap dòng → heading chỉ khi dòng trước trống/kết câu (+r63). · `tl hygiene` trần
  AttributeError traceback → guard fn=None in help + rc2 (+r63). · Vòng inject --profile/--config bỏ sót
  NESTED subparsers → đệ quy. · tool-inventory/cards-audit IndexError trên chuỗi lệnh rỗng → guard. ·
  Manifest walk đi xuyên symlink/junction → skip. · release-bundle TOCTOU (hash lúc manifest ≠ bytes lúc zip)
  → đọc 1 lần + đối chiếu sha, lệch → RELEASE_BUNDLE_FILE_CHANGED. · Bundle mặc định rơi VÀO repo root (nhiễm
  manifest, gói lồng gói) → tự chuyển ra cạnh root + warn + exclude '*-release.zip'. · Atomic-write tmp tên
  CỐ ĐỊNH đụng nhau/AV → mkstemp duy nhất (3 writer). · jsonio nhận diện tool-inventory bằng key 'groups' đụng
  workflow_audit.v2 → nhận diện theo schema. · --deterministic NO-OP âm thầm cho ~19 lệnh đường _emit_json_payload
  → đi qua cổng _json_dumps (mặc định OFF giữ nguyên format cũ). · stable_string đổi '\'→'/' trong VĂN BẢN
  thường → chỉ normalize chuỗi trông-như-path (không whitespace). · Deploy đè + zip mtime 1980 → __pycache__
  STALE im lặng → tl_fetch.sh dọn pycache sau unzip.
### Defer có chủ đích (1)
- P4-06: golden-test/determinism-audit so JSON đã re-canonicalize (json.loads→dumps) thay vì stdout THÔ —
  hạn chế thiết kế đã ghi nhận (drift formatting thuần sẽ không bị bắt); cân nhắc so raw-bytes ở Pha G.
- (P4-01 'repo đổi giữa lúc review' = chính phiên này đang vá — không phải bug.)
- py_compile trong release-check/determinism-audit + _RELEASE_REQUIRED_FILES phủ thêm workflow/release/live.py.

## Gate
Selftest **644/644** (+3 r61 bind/facade, +1 r62 root-cause diff-volatile-leaf, +7 r63 khoá lô vá);
workflow-audit --strict ✅ · golden-test ✅ · determinism-audit --strict ✅ · gen_instructions 24/24 ✅ ·
release-bundle ×2 CÙNG SHA-256 ✅.

# ★ v1.33.55 — MERGE bundle Pha B `core-json-determinism` (nhánh kia tự đánh "1.33.54" — TRÙNG SỐ khác nội dung với canonical) + đánh giá kế hoạch nợ-kỹ-thuật A-H (2026-07-08)

## Merge Pha B — tách tl_core (deterministic/jsonio)
- Bundle fork từ 1.33.53 nhánh kia (KHÔNG có 4 fix canonical v1.33.54 — đã kiểm 0/0/0/0 marker). Delta thật
  của Pha B nhỏ + sạch: `scripts/tl_core/{__init__,deterministic,jsonio}.py` mới; tl.py giữ 6 wrapper mỏng
  (`_VOLATILE_JSON_KEYS`/`_deterministic_enabled`/`_stable_string_for_json`/`_scrub_volatile`/`_json_dumps`/
  `_print_json_or_text`) — public CLI KHÔNG đổi; release-check py_compile + REQUIRED_FILES phủ tl_core.
- Áp delta LÊN canonical (không lấy nguyên tl.py bundle — giữ đủ 4 fix v1.33.54 + r59). +bootstrap sys.path
  phòng thủ trước import tl_core (ca tl.py nạp qua importlib từ cwd khác).
- 🔴 PORT LẠI fix #4 vào `tl_core.jsonio.print_json_or_text`: bundle viết jsonio từ code 1.33.53 → bug
  'schema lạ in nhầm route-task ok=True task=None' TÁI XUẤT — nay schema ∉ {tool-inventory, route_task*} →
  fallback JSON đầy đủ (khoá bằng r60).
- +3 `r60_*`: PARITY wrapper↔tl_core trên cùng payload (det/không-det/scrub/identity VOLATILE_JSON_KEYS),
  jsonio unknown-schema fallback, `deterministic_enabled` 3 tầng (flag > default_on > env đọc động).
  **Selftest 633/633.**

## Gate kiểm cuối (theo kế hoạch, phần offline)
- determinism-audit --strict ✅ · workflow-audit --strict ✅ · golden-test ✅ · gen_instructions --selftest
  24/24 ✅ · release-manifest regen + release-verify ✅ · **release-bundle build ×2 CÙNG SHA-256 ✅**.

## Đánh giá kế hoạch A-H (nhận + điều chỉnh)
- Kế hoạch HỢP LÝ: thứ tự 'khóa determinism trước, refactor sau', giữ tl.py là entrypoint, mỗi pha có
  acceptance. Pha A = ĐÃ XONG (merge v1.33.54); Pha B = bản này.
- Điều chỉnh 1 — ĐÁNH SỐ: kế hoạch đề xuất 1.33.53→57 nhưng canonical đã dùng 1.33.54 cho merge-A → từ nay
  Pha C=1.33.56, D=1.33.57, E=1.33.58, F=1.34.0, G/H giữ 1.34.1/1.34.2. Nhánh song song KHÔNG tự đánh số
  version canonical — để canonical đánh khi merge (đã 2 lần trùng số: Codex-49, PhaB-54).
- Điều chỉnh 2 — mỗi pha PHẢI kèm selftest trong gate `--selftest` (không chỉ audit rời — bài học 50-53
  thêm 3300 dòng 0 test; PhaB cũng 0 test parity → r60 do canonical thêm).
- Điều chỉnh 3 — Pha A3 exclude-list của kế hoạch còn THIẾU nhóm dev/local (.claude/.githooks/CLAUDE.md/
  config THẬT/.enc — đã vá 🔴 ở v1.33.54); kế hoạch nên ghi rõ 'manifest regen SAU MỌI sửa file, TRƯỚC zip'.
- Điều chỉnh 4 — Pha F (SKILL.md kernel): làm CUỐI như kế hoạch, và thêm bước RE-IMPORT zip vào Cowork
  Settings→Capabilities + user duyệt (SKILL.md là bản agent đọc — đổi lớn phải có người rà).

# ★ v1.33.54 — MERGE bundle determinism-hardening v1.33.50-53 (`tra-luat-skill-v1.33.53-determinism-hardening.zip`) + đánh giá tất định/drift + 2 fix khi gộp (2026-07-08)

Bundle nhánh song song fork ĐÚNG từ canonical 78d6bfe (v1.33.49), +3320/−55 dòng tl.py + 30 file mới
(references/workflows/*.json cards + references/golden/*.json fixtures + RELEASE_MANIFEST.json) + SKILL.md/
gen_instructions/RUNBOOK/DOCTRINE_APPENDIX. −55 dòng chỉ là refactor `print(json.dumps(out))` → `_json_dumps`
(mặc định KHÔNG sort/scrub — tương thích ngược) + VERSION/import. KHÔNG mất dòng canonical nào.

## Đánh giá TẤT ĐỊNH (verified bằng chạy thật, không tin CHANGELOG bundle)
- ✅ Repeat-run byte-identical (`tool-inventory --json --deterministic` ×2 cmp = identical).
- ✅ Release zip dùng `ZipInfo.date_time=(1980,1,1)` cố định + member sort → zip reproducible.
- ✅ `RELEASE_MANIFEST.json` tự-loại-mình (109/110), 0 volatile key, `package_hash` TÁI TẠO ĐƯỢC cross-platform
  (regen trên Windows khớp hash bundle build nơi khác: dcca0cd7…).
- ✅ Volatile scrub: namespace `volatile{}` + key-list (generatedAt/epoch/mtime/age_days/seconds/…) → `"<volatile>"`;
  `_deterministic_enabled` = flag > hằng import-time > re-read env (3 tầng nhất quán — nghi vấn 2-cơ-chế là SAI).
- ✅ Zip-slip guard (`..`→unsafe, chuẩn hoá `./`+backslash) + `DUPLICATE_NORMALIZED_ZIP_PATH` reject.
- ✅ Tự-gate: `determinism-audit --strict` + `workflow-audit --strict` (60 task/159 lệnh) PASS; selftest 625/625 giữ.
- ⚠ Quan sát 1 lần `determinism-audit` top ok:false ngay SAU khi sửa file hàng loạt — không tái hiện qua 5 lần
  chạy (kể cả sau xoá __pycache__); __pycache__/.pyc ĐÃ nằm trong _RELEASE_EXCLUDE — xếp transient, theo dõi.

## Đánh giá DRIFT
- ✅ Doctrine GIỮ BẤT BIẾN: không tách canonical VBQPPL (chunk chỉ là nguồn phụ `row_kind=ref, corpus=false,
  goc=<canonical>`); large_file_split_gate vẫn HỎI người dùng; OCR gate (VBQPPL thiếu manifest verified → chặn).
- ✅ Cờ `--profile`/`--config` injection loop v1.33.48 tự phủ mọi subparser MỚI của bundle (parse-test PASS).
- ⚠ Fix drift #1: bundle đổi `route-task <task>` (positional, như doc/log cũ) → BẮT BUỘC `--task` → gãy cách gọi
  cũ (lớp S8/A1 doc↔CLI). Gộp: nhận CẢ HAI (positional + --task; thiếu cả hai → MISSING_TASK rc=2).
- ⚠ Fix gap #2: bundle thêm ~3300 dòng mà 0 test trong gate `--selftest` (audit là lệnh RIÊNG, upload script
  không tự chạy) → +5 `r59_*` khoá PURE helpers: `_zip_normalized_member_path` (slip/normalize),
  `_zip_sorted_infos` (thứ tự tất định — lưu ý '.'(2E)<'/'(2F)), `_json_dumps` det (sort+scrub vs default giữ
  nguyên), route-task positional+flag, release-exclude dev-local. **Selftest 630/630.**
- 🔴 Fix #3 (lộ khi regen manifest trên dev-tree): `_release_should_include` walk THƯ MỤC (không phải git
  ls-files) → LIỆT KÊ + HASH cả `tra_luat_config.v2.json` (config THẬT chứa webappUrl/token), `CLAUDE.md`,
  `.claude/`, `.githooks/`, `.enc` vào RELEASE_MANIFEST (rò metadata + file_count 115≠109 → release-verify
  trong gói giải nén FAIL). Vá: `_RELEASE_EXCLUDE_DIRS` += .claude/.githooks; SUFFIXES += .enc;
  `_RELEASE_EXCLUDE_NAMES_ANYWHERE` (CLAUDE.md + tra_luat_config[.v2].json mọi cấp — GIỮ example).
  Sau vá: dev-tree manifest == zip-set (109), hash tái lập.
- 🟡 Fix #4: `_print_json_or_text` không --json chỉ biết render tool-inventory/route-task — lệnh MỚI khác
  (release-manifest/verify/…) in nhầm `route-task ok=True task=None` → schema lạ fallback JSON đầy đủ.
