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

