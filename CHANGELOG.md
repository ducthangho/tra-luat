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

