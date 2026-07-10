#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tl — CLI hợp nhất tra-luat (phiên bản: HẰNG `VERSION` bên dưới là nguồn chân lý DUY NHẤT — docstring không
lặp số nữa sau ca drift v1.22.68/log rà 2026-07-04; webapp LIVE 2.21.2i; + fast-lane CLI nlm (nlm-list/
nlm-reconcile, ~4s skip-freshness) + xref/dedup/ingest-route/cache-snapshot/perf). `tl --version` in version.

GỘP các thao tác hay dùng thành lệnh con TẤT ĐỊNH, bọc quanh gas.py + các module đã
kiểm thử (boot, preingest_gate, manifest_build, standardize_name, keywords). KHÔNG
reimplement logic — chỉ điều phối + chống "đoán tham số" bằng cách trỏ đúng action/khóa.

Tham số/khóa response webapp: xem references/API_CONTRACT.md (đóng dấu version 2.21.2i).

Lệnh con:
  tl ping                      — ping; cảnh báo nếu version != 2.21.2i (cổng A2 của RUNBOOK)
  tl boot                      — đọc manifest → dựng index offline (= boot.py)
  tl locate <q>                — tra số hiệu/từ khóa: manifest offline trước, có WARN nhãn/registry
  tl source-map <q...>          — lập bản đồ nguồn rà soát, VBHN-first + WARN nhãn/registry
  tl exists <q>                 — kiểm tra hiện diện bằng source-map chuẩn hóa, không overclaim
  tl relation-check             — soi văn bản sửa đổi/VBHN đã có nhưng registry thiếu goc/sua_doi
  tl external-ingest            — gate nạp nguồn web/NLM-native: research_* discovery-only, QT-3 trước NLM
  tl link-priority              — xếp link tải cho người dùng (TVPL/LuatVietnam/Công báo trước)
  tl profile-info               — đọc config v2, chọn profile corpus, in folder/notebook/manifest/registry
  tl slot-audit                 — đếm slot NLM theo nlm_notebook_id, chống NOTEBOOK_FULL giả
  tl instruction-audit           — kiểm Instruction có ràng buộc skill/QT-3/research discovery-only
  tl instructions                — sinh Instruction/Project prompt tự ràng buộc với skill tra-luat
  tl vbhn-check                 — QT-5: dò VBHN theo trích yếu + gốc + năm; không overclaim
  tl vbhn-verify                — verify nội dung VBHN; --official-required chặn bản tự ghép làm canonical
  tl vbhn-compare               — so bản chính thức với bản tạm/tự ghép, soi footnote + điều trọng tâm
  tl status <sohieu> [...]     — CỔNG TIỀN-NẠP QT-2 (= preingest_gate): ADD/SKIP/REVIEW
  tl extract <gdocId> --dieu N — export ra ĐĨA + in ĐÚNG Điều (token-saving B2)
  tl ingest <fileId> [...]     — QT-2 gate → (—-apply) copy_convert+organize; mặc định DRY
  tl register [...]            — reg_upsert (1 dòng) / reg_bulk (--bulk items.json)
  tl manifest [--touched-drive]— kết phiên: export-only; profile inherit cần --confirm để regen2 own-scope
  tl profile-rebuild-registry  — phục hồi registry profile: giữ notebook + file trong root + ref (DRY mặc định)
  tl hygiene scan/plan/reconcile — registry hygiene: duplicate/orphan/quarantine plan
  tl registry-doctor [...]     — compat/report-only registry hygiene, không sửa Drive
  tl rasoat <sub> [...]        — passthrough/fallback: keywords|titles|worksheet|orchestrate

Creds: env (TL_WEBAPP/TL_TOKEN) → --config FILE → ~/.tra_luat_config.json → /tmp/tra_luat_config.json.
Offline: tl --selftest   (logic thuần, không gọi mạng)
"""
from __future__ import annotations
import argparse, base64, datetime, hashlib, json, os, re, sys, shutil, subprocess, tempfile, time, unicodedata, zipfile

# v1.33.55: bảo đảm scripts/ trên sys.path TRƯỚC import tl_core (ca tl.py nạp qua importlib/spec từ cwd khác).
_TL_DIR = os.path.dirname(os.path.abspath(__file__))
if _TL_DIR not in sys.path:
    sys.path.insert(0, _TL_DIR)


def _tl_core_import(name: str):
    """v1.33.56 (review tl_core/F3): tl_core hỏng (mount NUL-pad/cắt cụt — lớp sự cố #51435) → chết có
    HƯỚNG DẪN thay vì SyntaxError trần; tl_boot.py preload bản strip-NUL vào sys.modules TRƯỚC nên đường
    cứu hộ vẫn chạy được toàn CLI."""
    try:
        import importlib
        return importlib.import_module(f"tl_core.{name}")
    except SystemExit:
        raise
    except BaseException as e:  # noqa: BLE001 — SyntaxError/ValueError NUL/ImportError đều cần remediation
        print(f"[tl] ✗ KHÔNG nạp được scripts/tl_core/{name}.py ({type(e).__name__}: {e}).\n"
              f"    Từ v1.33.55/56 package tách module — file này là LÕI. Mount Cowork có thể NUL-pad/cắt cụt.\n"
              f"    KHẮC PHỤC: (a) chạy qua launcher tự-strip-NUL: python scripts/tl_boot.py <lệnh>;\n"
              f"    (b) re-fetch zip sạch: sh scripts/tl_fetch.sh --setup; (c) kiểm: tl doctor --offline.",
              file=sys.stderr)
        raise SystemExit(3)


_tl_det = _tl_core_import("deterministic")
_tl_jsonio = _tl_core_import("jsonio")
from pathlib import Path

# UTF-8 hardening (Windows codepage / tiếng Việt)
for _s in (getattr(sys, "stdout", None), getattr(sys, "stderr", None)):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# III.1: truyền UTF-8 xuống MỌI script con spawn qua subprocess. Windows console (cp125x) khiến script con
# in tiếng Việt (gen_instructions.py, sapxep.py…) ném UnicodeEncodeError 'charmap'. PYTHONUTF8=1 bật UTF-8
# mode ở interpreter con BẤT KỂ codepage; setdefault → không đè nếu người dùng đã chủ ý set khác.
os.environ.setdefault("PYTHONUTF8", "1")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")

HERE = Path(__file__).resolve().parent
CACHE = Path(os.environ.get("TL_CACHE_DIR", str(Path.home() / ".tra_luat_cache")))
EXPECT_VERSION = "2.21.2i"
# [lịch sử, đã gộp 1.24.0] 1.23.22: ROOT-CAUSE THẬT sự cố 2026-06-30 (ĐÍNH CHÍNH 1.23.21: KHÔNG mất data 766 dòng!). Thật ra config `registryDocId` trỏ NHẦM Doc legacy `1mATG` (vnd.google-apps.document) thay vì SHEET registry thật → webapp mở Doc-as-Sheet → đọc RỖNG → count=0 ẢO (data vẫn nguyên; corpus 552 là do dedup-plan −50). Template public init-config hay ghi đè về Doc legacy → tái diễn mỗi setup. FIX: (1) doctor CHẶN cứng `registryDocId == _LEGACY_REGISTRY_DOC_ID` (1mATG) → báo sửa về Sheet/để rỗng; (2) `init-config` AUTO-HEAL: blank registryDocId (base+profiles) nếu = Doc legacy → webapp auto-discover Sheet `tra_luat_registry`. (Giữ guard 1.23.21 cho ca profile registryDocId rỗng.) +1 test → 260/260. # 1.23.21: ⛔ GUARD CHỐNG CLOBBER REGISTRY NỀN (SỰ CỐ NGHIÊM TRỌNG 2026-06-30: profile dự án 'Khảo sát Luật XB' registryDocId RỖNG → webapp `regSS_` rơi nhánh BASE → manifest --touched-drive quét phình rồi profile-rebuild-registry XÓA SẠCH 766 dòng registry NỀN VBQPPL). FIX: `cmd_manifest` (--touched-drive) + `cmd_profile_rebuild_registry` CHẶN khi profile dự án có TL_REGISTRY_DOC_ID rỗng (PROFILE_REGISTRY_ID_EMPTY_WOULD_CLOBBER_BASE, rc=2) — phải tạo registry RIÊNG trước. PHÁT HIỆN từ GS: registry base = Google SHEET `tra_luat_registry` (regSS_ tìm theo tên/TL_REGSHEET_ID_AUTO), KHÔNG phải Doc 1mATG (chỉ ping/display); khôi phục = restore SHEET đó (version history Sheets), cache `tl212_reg_*` TTL 600s. +1 test → 259/259. # 1.23.20: DETECTOR `infra_in_corpus` (phát hiện khi rà 106 Luật dump) — file HẠ TẦNG (.json/.enc/secrets/nlm_sources_delta/manifest/registry) lẫn corpus=true = RÁC (vd tl_secrets.enc, nlm_sources_delta_*.json đếm như văn bản). `_is_infra_entry` (module-level, BẢO VỆ GDoc/PDF/Word) + thêm vào `tl sweep` (cờ + NEXT ACTION set corpus=false). +1 test → 258/258. # 1.23.19: COMPOSITE `tl dedup-plan` (user yêu cầu) — kế hoạch dedup TOÀN CORPUS 1 lệnh (thay chạy `hygiene plan <q>` từng cụm). Tái dùng canonical-picker của `_hygiene_groups` (reconcile_clusters `_cluster_same_doc` = CÙNG văn bản theo subject-sig + gộp sidecars .docx/.pdf cạnh GDoc). GIỮ canonical, set corpus=false bản dup (reversible). BẤT BIẾN AN TOÀN: không quarantine chính canonical / canonical của cụm khác / trùng lặp. DRY mặc định; --apply ghi reg_bulk corpus=false; review (thiếu canonical) + dups_on_nlm (còn nguồn NLM→cân nhắc xoá tay) chỉ BÁO. sweep NEXT ACTION trỏ dedup-plan. Pure `_dedup_plan`. +1 test → 257/257. # 1.23.18: FIX false-fire NLM_STATUS_MISMATCH (phát hiện khi nlm-orphans --fix-mismatch LIVE trả MISMATCH_LIVE=0 dù sweep báo 79). Whitelist status exact-match KHÔNG nhận biến thể `removed_*` (removed_superseded_by_VBHN, removed_dedup…) → false-fire + `_entry_on_nlm_live` coi NHẦM removed_* là sống (lệch still_on_nlm/ghost). FIX: `_nlm_status_known`/`_nlm_status_removed` nhận HỌ tiền tố (pushed*/synced/removed*/trash*/deleted), áp 4 site (doctor flag, _title_flags, _entry_on_nlm_live, vbhn-normalize removed). sweep NEXT ACTION: NLM_STATUS_MISMATCH = nhãn LẠ (registry hygiene) KHÔNG phải live desync. +2 test → 256/256. # 1.23.17: `tl sweep` NEXT ACTION nlm_drift TÁCH theo sub-type (phát hiện khi reconcile LIVE không giảm drift) — trước gộp 288 thành 'nlm-reconcile --apply' GÂY HIỂU NHẦM (reconcile chỉ chữa LINKAGE). Nay: NLM_NOTEBOOK_ID_MISSING→nlm-reconcile (linkage); NLM_STATUS_MISMATCH→nlm-orphans --fix-mismatch (đọc live); CORPUS_TRUE_NOT_ON_NLM→ingest-missing (job lớn, phần lớn CẤU TRÚC corpus>cap, KHÔNG về 0). # 1.23.16: DETECTOR `shared_source_id` (phát hiện khi dọn ghost NLM LIVE) — ≥2 drive_id KHÁC nhau CÙNG 1 nlm_source_id (backfill/reconcile gắn nhầm) = FALSE-LINK: xóa nguồn của row này GÃY link row kia (ca NQ42: canonical + ghost chung source_id → xóa ghost làm canonical mất NLM, phải re-push). Pure `_shared_source_id_groups` + thêm vào `tl sweep` (cờ + NEXT ACTION cảnh báo SỬA TRƯỚC nlm-reconcile/xóa nguồn). Dev cache thấy 4 nhóm. +1 test → 254/254. # 1.23.15: xử báo cáo rà 106 Luật (mục code còn lại; 5.1/5.3/5.6/4.B đã vá ở 1.23.11-14). 5.2 vbhn-check goc_hit cross-subject LỌT (14-2024 ATVSLĐ vào --goc 09-2017 Du lịch vì _disc_conflict không biết cặp) → `_vbhn_candidates`: khi ĐÃ biết subject, goc_hit phải TƯƠNG THÍCH chủ đề (sscore≥30) mới giữ. 5.5 Cowork /tmp sticky owner-nobody không ghi được → `_ensure_writable_tmpdir()` trỏ TMPDIR về CACHE/tmp ($HOME) lúc import (tempfile.* + script con kế thừa). 5.4 SKILL.md bootstrap options + cảnh báo 45s; 4.B thêm vbhn-normalize/sweep/quarantine-fix/vbhn-year-fix vào bảng CLI. +2 test → 253/253. # 1.23.14: COMPOSITE `tl quarantine-fix` (dọn nhóm B tất định) — phân loại dòng quarantine MÂU THUẪN: set_corpus_false (raw-dup .pdf/.docx gán nhầm corpus→false, AN TOÀN) + normalize_label (nhãn biến thể→QUARANTINE_CAT) tự động qua --apply; review_restore (GDoc corpus=true nghi canonical kẹt như A1/BLLĐ→KHÔNG auto, quyết tay) + ghost_nlm (quarantine còn nguồn NLM live→báo source_id, xoá tay sau verify). Pure `_quarantine_fix_items`. DRY mặc định. +1 test → 251/251. # 1.23.13: (1) MERGE HỘI TỤ bản Codex v1.23.11 (cùng vá report rà corpus) — PORT phần UNIQUE: A1 SUBJECT-GATE thật (`_name_subject_match`/`_name_subject_text`: source-map ghim canonical CHỈ trong hit KHỚP CHỦ ĐỀ, abbrev-aware BLLD/BHXH; hit generic→None+SUBJECT_MISMATCH) + `resolve_identity` +name_tokens (dedup-check 'Luật Thư viện') + vbhn-check SUBJECT_FILTER_WEAK + reg-query LIMIT_TRUNCATED rõ. GIỮ bản tôi đã verify cho A2-A5 + reg-query json-all. (2) GỠ `_parts` (chống mount-cắt-cụt — Cowork nay bootstrap qua tl_fetch zip sạch nên hết tác dụng): xoá scripts/_parts/ + build_parts.py + tl_rebuild.sh; tl_boot.py rút gọn (strip-NUL→compile→exec); `_reassemble_parts`→None (heal degrade về on-disk); edit-skill/verify-integrity bỏ build_parts. (3) COMPOSITE TẤT ĐỊNH `tl sweep`: 1 lệnh thay chuỗi 6 audit (hygiene+cat+slot+drift+vbhn-year+quarantine) → JSON/text + NEXT ACTIONS điền sẵn (pure `_sweep_report`). +4 test → selftest 250/250. # 1.23.12: 2 fix từ chạy B1 LIVE. (1) reg-query `--json` UNDERCOUNT âm thầm — mặc định cắt 60 rows → script đếm `len(rows)` thiếu (audit quarantine thấy 60/110). Nay `--json` trả TẤT CẢ rows mặc định (text vẫn cắt 60 + dòng '(hiện 60)') + cờ `truncated`. (2) hygiene scan thêm cờ TRẠNG THÁI MÂU THUẪN `quarantine_corpus_true` (trong quarantine nhưng corpus=true) + `quarantine_still_on_nlm` (quarantine nhưng còn nguồn NLM live = ghost) → surface để dọn. # 1.23.11: xử báo cáo rà corpus (nhóm A). A2: hằng `QUARANTINE_CAT` + `_is_quarantine_label_variant` + cờ hygiene scan `quarantine_label_variants` (audit hội tụ dù nhãn lệch QUARANTINE/_ZZZ — `_is_quarantine_cat` nhận mọi biến thể). A3: `slot-audit` TỰ neo `live_source_count` từ nlm CLI (+`--no-live`) → cảnh báo gap estimate↔live khỏi gọi `--physical` tay. A4: `doctor` in BREAKDOWN từng cờ (NLM_STATUS_MISMATCH/CORPUS_TRUE_NOT_ON_NLM/NLM_NOTEBOOK_ID_MISSING) + lệnh `nlm-reconcile <nb> --apply` ĐIỀN SẴN notebook id. A5: help `vbhn-check --subject` thêm cảnh báo QUOTE. A1 (source-map ghim sai canonical 'Bộ luật Lao động'→'Dân chủ 87'): KHÔNG tái hiện trên v1.23.11 với dữ liệu đại diện — gate LOW_CONFIDENCE_NAME_MATCH gốc đã null canonical khi top không strong-match; giữ gate (thử thay bằng nhóm tail-key gây regression abbrev/quarantine → revert). Cần `source-map --json` LIVE để soi nếu còn. +3 test. # 1.23.10: GUARD cat (phát hiện khi nạp THADS 106/2025 LIVE) — `register`/reg_bulk KHÔNG validate `cat` → workaround gõ tay folder RÁC '30_To_chuc_bo_may_nha_nuoc' (số 30 + tên cat 35) lọt im lặng → registry lệch folder vật lý. Nay `_is_valid_cat_value` chặn cat không thuộc taxonomy 45+2 (cả nhánh --bulk lẫn reg_upsert), rc=2, nhắc dùng `tl recat --cat <số>`. +1 test. BÀI HỌC: đổi cat LUÔN dùng recat (resolve+validate folder), KHÔNG register --bulk tên gõ tay. # 1.23.9: 2 FIX (phát hiện khi chạy vbhn-year-fix LIVE Cowork). (A) vbhn-year-fix CHỈ quét entry corpus=true — sidecar/quarantine (corpus=false) KHÔNG year-fix → hết CONFLICT GIẢ (sidecar corpus=false va sohieu với GDoc canonical cùng số; hygiene báo 'sạch' nhưng vbhn-year-fix báo conflict = mâu thuẫn do quét cả non-corpus). (B) HINT SAI: lệnh ghi in `MANIFEST_STALE_RUN_REGEN2` → `tl regen2` KHÔNG phải lệnh (chỉ có `tl manifest`; regen2 là action GAS qua `manifest --touched-drive`) → user chạy nhầm. Sửa 5 hint + dòng recat → `tl boot --refresh` (sau ghi registry sheet) / `tl manifest` (sau đổi cây Drive). +test corpus-skip. # 1.23.8: SAFEGUARD cho vbhn-year-fix (phát hiện khi soát DRY) — nếu ≥2 dòng suy ra CÙNG `NN-YYYY-VBHN-XXX` (dòng dup cùng văn bản, HOẶC 2 văn bản khác cùng số+năm) thì ghi sẽ TẠO collision MỚI → tách bucket `conflicts`, KHÔNG auto-apply (rc=1), in 🔴 CONFLICT để dedup/phân biệt tay. `_vbhn_year_fix_items` nay trả (fixable, needs_year, conflicts). +1 test. # 1.23.7: ★ BẤT BIẾN ĐẶT TÊN (user nhấn mạnh) — số hiệu VBQPPL PHẢI có NĂM; VBHN là thủ phạm (số VBHN tái dùng theo năm → collision, vd 61/VBHN-VPQH=ATTP 2025+Thuế TNDN 2026, 115/VBHN-VPQH=THADS 2025+Thi đua 2026). Lệnh MỚI `tl vbhn-year-fix [--with-name] [--apply]`: quét VBHN sohieu THIẾU năm (`NN-VBHN-XXX`) → suy năm (ngày ban hành/tên qua `_entry_issue_year`) → đề xuất `NN-YYYY-VBHN-XXX`, GHI qua reg_upsert (KHÔNG reg_bulk — sohieu là khóa immutable); ca không suy được năm → needs_year (xác minh tay). Pure `_vbhn_sohieu_inject_year`/`_name_inject_vbhn_year`/`_vbhn_year_fix_items` (test offline). + `register` cảnh báo `VBHN_SOHIEU_NO_YEAR` khi ghi sohieu VBHN thiếu năm. +3 test. (Phát hiện đã có sẵn: cờ VBHN_BARE_NUMBER/MISSING_YEAR_OR_DATE/NAME_MISSING_YEAR.) # 1.23.6: FIX (phát hiện khi KH2 Pha 2.6 recat Cowork) — `recat --apply` báo `reg_patched:0` ÂM THẦM khi Drive đã move nhưng webapp index chưa thấy row mới thêm (registry cat KHÔNG cập nhật → user tưởng xong). Nay LOUD cảnh báo stderr + rc=1 khi reg_patched < moved, chỉ rõ KHẮC PHỤC (regen2 --refresh rồi reg_bulk lại). Cùng họ "ghi im lặng" với 1.23.5. +1 test. # 1.23.5: FIX BUG (phát hiện khi KH2 Pha 2.8 chạy Cowork) — `missing-sohieu --apply` ghi reg_bulk cột `so_hieu` (có gạch dưới) → webapp BỎ IM LẶNG (đúng gotcha API_CONTRACT mục 0: khóa phải `sohieu`); apply thẳng trả patched=0 mà KHÔNG báo lỗi. Sửa items key + cols → `sohieu` (line ~8061) + help/docstring. Workaround Cowork (cols="sohieu") đã ghi 193/193; nay code gốc đúng. +1 test. # 1.23.4: ★ KH1 HOÀN TẤT — `tl relation-backfill --base <sh> [--apply]` (Pha 1.5 cuối, cho KH2 Pha 2.3): GHI quan hệ sửa đổi mà relation-check ĐÃ phát hiện (missing_links từ `_relation_audit`, tái dùng cổng footnote chống dương-tính-giả) — set `goc` cho luật SỬA, append `sua_doi` cho luật GỐC (pure `_relation_backfill_items` HỢP NHẤT sua_doi cũ + dedup, KHÔNG đè). CHỈ direct/ref-linked; subject-only → review (xác minh tay). DRY mặc định. +1 test → selftest 237/237. → TOÀN BỘ lệnh KH1 đã dựng (3 cổng + vòng lặp + dọn-corpus + nlm-orphans + relation-backfill). CÒN: cập nhật RUNBOOK/API_CONTRACT (tài liệu), KH2/KH3 (corpus). # 1.23.3: FIX DEPLOY-DISPLAY — SKILL.md header ghi CỨNG '(v1.22.70)' qua MỌI bump 1.22.71→1.23.2 (tôi quên sed SKILL.md) → bản deploy HIỂN THỊ 'v1.22.70' dù runtime đúng. Sửa SKILL.md→(v1.23.3) + GUARD selftest `skill_md_version_matches_VERSION` (bump nào quên cập nhật SKILL.md = selftest FAIL → chặn deploy). LƯU Ý vận hành: Package live khi kiểm = 1.23.0 (1.23.1/1.23.2 CHƯA push thành công — drive-push cần gws auth); verify push bằng curl Package fileId. +1 test → selftest 236/236. # 1.23.2:`tl nlm-orphans <notebook> [--fix-mismatch] [--deep]` — TỰ ĐỘNG HOÁ điều tra ghost (thay 6 vòng soi tay): đọc nguồn NLM LIVE (`nlm_cli.source_list`) ↔ registry → phân `_classify_nlm_sources` (PURE, test offline) thành REGISTERED_ACTIVE / **STATUS_MISMATCH_LIVE** (dòng registry removed* nhưng nguồn còn SỐNG = gắn nhãn SAI, vd 8 văn bản đã vá tay) / UNREGISTERED (trên NLM, không dòng registry). REPORT-ONLY; --fix-mismatch in bản vá metadata DRY (corpus=true,nlm_status=pushed) cho nhóm mislabel (KHÔNG đụng NLM/KHÔNG xóa); --deep đọc nội dung NLM lấy SỐ HIỆU header thật (vá cả sohieu cụt như '66'→'66.18/2026/NQ-CP'). +1 test → selftest 235/235. (CÒN: relation-backfill Pha 1.5 live; root-cause pipeline gắn nhầm removed_from_drive; SKILL.md/RUNBOOK/API_CONTRACT.) # 1.23.1: vá sweep-finding — `overflow-resolve` ĐỐI CHIẾU LIVE (nlm-get) thay vì registry-only: dùng MAX(registry, physical) làm slot hiệu lực (`_overflow_status`) → KHÔNG báo 'còn chỗ' giả khi vật lý vượt cap (vd base registry 279 / LIVE 315); cờ `REGISTRY_BEHIND_LIVE` lộ nguồn add thẳng CHƯA đăng ký (gợi `tl nlm-reconcile`); sửa cosmetic flag (BASE_HAS_ROOM khi base còn chỗ). `--no-live` để registry-only. (ingest-missing --apply ĐÃ physical-safe sẵn qua nlm-get.) +1 test → selftest 234/234. # 1.23.0: ★ KH1 (sửa skill sau báo cáo rà 70 Luật) — PHÁT HÀNH. Pha 1.3/III.2: `tl slot-audit --all-shards` (II.5 đếm slot TỪNG shard + cảnh báo near-full ≥270/300, pure `_slot_count_all_shards`) + `tl overflow-resolve` (II.1 kiểm shard overflow SẴN CÓ → cờ OVERFLOW_SHARD_EXISTS_DO_NOT_CREATE, chống tạo notebook nhầm; reuse `_overflow_route`) + `tl edit-skill <file> --patch` (III.2 sửa skill an toàn: assert-đếm→py_compile→write_text→build_parts, né Edit/Write mount; DRY mặc định). manifest-stale (II.4): lệnh ghi MỚI phát MANIFEST_STALE_RUN_REGEN2. canonical-not-sidecar (II.3): ĐÃ xử qua deep-resolver `_resolve_deep_target`+`_is_source_sidecar`+phạt raw-300. +3 test → selftest 233/233. ★ TỔNG KH1 (1.22.71→1.23.0): H1/H2/UTF-8/instructions--out; 3 CỔNG G1(source-verify)/G2(header-verify)/G3(cat-verify+cat-audit/recat FIX); vòng lặp frontier-expand/ingest-missing(no-new-notebook)/rasoat-loop; dọn corpus backfill-loai/sohieu-conflict/missing-sohieu; slot-audit/overflow-resolve/edit-skill. CÒN (1.23.1): relation-backfill (live, Pha 1.5); cập nhật SKILL.md/RUNBOOK/API_CONTRACT + upload Package (user-side). # 1.22.76: KH1 Pha 1.5 — `tl missing-sohieu` (đề xuất số hiệu cho dòng registry thiếu sohieu, parse từ TÊN qua `_parse_sohieu_from_name`, bỏ Mẫu/Phụ lục; DRY mặc định, --apply ghi reg_bulk so_hieu; ⚠ ĐỀ XUẤT theo tên — XÁC MINH bằng header-verify/G2; LIVE suy 194/307 dòng thiếu). +1 test → selftest 231/231. HOÀN TẤT Pha 1.5 quick-wins pure (backfill-loai+sohieu-conflict+missing-sohieu). CÒN (v1.23.0): Pha 1.5 relation-backfill (live) + Pha 1.3 (overflow-resolve/canonical-sidecar/manifest-stale/slot-audit per-shard) + III.2 edit-skill. # 1.22.75: KH1 Pha 1.5 (quick-wins pure) — `tl backfill-loai` (suy `loai` chuẩn cho dòng trống từ tên+số hiệu qua pure `_infer_loai`; DRY mặc định, --apply ghi reg_bulk; idempotent; LIVE manifest suy được 191/769) + TÁCH `SOHIEU_CONFLICT_DIFFERENT_DOC` (≥2 chữ-ký-chủ-đề KHÁC cùng số hiệu = văn bản KHÁC, NGUY HIỂM) khỏi `SAME_DOC` (sidecar) trong registry-doctor (`_subject_sig`; thêm khóa `sohieu_conflict_groups` vào schema text=json; LIVE 22 conflict/6 same trong 28 dup). +3 test → selftest 230/230. CÒN (v1.23.0): Pha 1.5 relation-backfill/missing-sohieu (live) + Pha 1.3 (overflow-resolve/canonical-sidecar/manifest-stale/slot-audit) + III.2 edit-skill. # 1.22.74: KH1 Pha 1.2 HOÀN TẤT P0 — `tl ingest-missing` (nạp backlog corpus chưa NLM → source_add+reg_bulk; IDEMPOTENT + checkpoint resume; DRY mặc định; định tuyến theo chỗ trống base→overflow shard SẴN CÓ; BẤT BIẾN `_overflow_route` KHÔNG BAO GIỜ tạo notebook (đầy→BLOCKED hỏi user); pure `_ingest_missing_select`/`_overflow_route` test offline) + `tl rasoat-loop` (orchestrator VÒNG LẶP KHÉP KÍN report-only: SEED→frontier-expand→mở rộng đệ quy in-corpus đọc nguyên-văn KHÔNG RAG→dedup seen chống lặp→hội tụ dry_rounds≥K; xuất GAP ngoài-corpus + in-corpus-chưa-NLM; pure `_rasoat_dedup_push`). +4 test → selftest 228/228. CÒN (v1.23.0): Pha 1.3 (overflow-resolve/canonical-sidecar/manifest-stale/slot-audit per-shard) + Pha 1.5 (backfill-loai/sohieu-conflict/relation-backfill/missing-sohieu) + III.2 edit-skill. LƯU Ý: ingest-missing/rasoat-loop nhánh mutate/expand-live CHƯA test trên dev (không NLM cred) — lần --apply đầu chạy Cowork batch nhỏ. # 1.22.73: KH1 Pha 1.2 — `tl frontier-expand <gdoc|sohieu>` (vòng lặp rà soát): trích MỌI dẫn chiếu (xref+footnote+inline) → ứng viên FRONTIER dedup theo số hiệu + ưu tiên (amending>VBHN>dẫn-chiếu) + cờ in_corpus; `missing_in_corpus` = đầu vào ingest-missing. Pure `_frontier_candidates` (test offline) + `_frontier_doc_text` reader; DISCOVERY/REPORT-ONLY, KHÔNG RAG; --text-file offline. +2 test → selftest 225/225. CÒN (v1.23.0): ingest-missing (mutate NLM, no-new-notebook), rasoat-loop (orchestrator); Pha 1.3; Pha 1.5. # 1.22.72: KH1 Pha 1.2 — DỰNG 3 CỔNG XÁC MINH G1/G2/G3 (dựng SẠCH, KHÔNG dùng bản agent tiêm đã revert). G3: helper pure `_load_linhvuc`/`_cat_taxonomy`/`_infer_cats_text`(suy cat theo NỘI DUNG alias, whole-word)/`_cat_boundary_rule`(ép quy_tac_ranh_gioi: BHXH/BHYT→02, đầu-tư-công/hải-quan→26, sửa≥2 luật→46, điều-ước→23, Đảng→00) + `tl cat-verify <gdoc|sohieu>` (read-only, --text-file offline) + FIX `cat-audit` (confidence/RULE/taxonomy-45+2/--strict) + FIX `recat` (BOUNDARY_CONFLICT advisory + --force-cat). G2: `_extract_header_facts` (ngày+cơ quan, pure) + `tl header-verify [--all/--sohieu/--drive-id/--cat] [--fix-suggest] [--strict]` (batch _verify_header_match, READ-ONLY, bắt DRIFT 775 dòng; KHÁC title_mismatch=metadata nội bộ). G1: `_content_md5` (NFC, pure) + `_official_rank` + `_DISCOVERY_SITES` re-rank OFFICIAL-FIRST (vbpl>congbao>luatvietnam>thuvienphapluat) + `tl source-verify <sohieu|gdoc>` (content_md5 + SOURCE_DISCREPANCY + nguồn official-first đối chiếu, --text-file offline). +14 test → selftest 223/223. CÒN (v1.23.0): rasoat-loop/frontier-expand/ingest-missing; Pha 1.3; Pha 1.5. # 1.22.71: KH1 (Pha 1.1/1.4) thực thi sau báo cáo rà 70 Luật. H2 `registry-doctor` text=JSON schema (dòng text SINH TỪ `_DOCTOR_SUMMARY_KEYS` → `build_doctor_summary`/`format_doctor_text`, hết lệch nhãn duplicate_sohieu↔_groups/title_mismatch↔_candidates/rows↔count). H1 `reg-query --json` rc=0+envelope KHÓA bằng test (không tái hiện ở canonical; rc=1 trong log = confound redirect/&&/bản cũ). III.1 `os.environ PYTHONUTF8=1`/PYTHONIOENCODING truyền xuống MỌI script con (hết UnicodeEncodeError 'charmap' gen_instructions.py… console Windows) + gen_instructions.py reconfigure standalone. III.3 `tl instructions --out <file>` ghi UTF-8 ra file. +3 test → selftest 209/209. (LƯU Ý: workflow thiết kế v1.23 từng tiêm nhầm header-verify/cat-verify vào canonical → ĐÃ revert, sẽ dựng lại CÓ REVIEW.) CÒN (v1.23.0): rasoat-loop/frontier-expand/ingest-missing; Pha 1.3 overflow-resolve/canonical-sidecar/manifest-stale/slot-audit; Pha 1.5 backfill-loai/sohieu-conflict/relation-backfill; cổng G1/G2/G3. # 1.22.70: ★ HỢP NHẤT bản Codex v1.22.69 (CONVERGENT — 2 nhánh cùng vá 13 lỗi 2 báo cáo, KHÁC code) + vá LOG RÀ MỚI (Nhóm A-E đa-profile) + LARGE-FILE SPLIT. MERGE: GIỮ bản Claude làm base (verify 197/198, có H/D/G/2.2 mà Codex THIẾU) + PORT phần Codex MẠNH HƠN: (1) DEEP-RESOLVER `_resolve_deep_target`+`_entry_mime`/`_entry_google_doc`/`_entry_raw_no_gdoc`/`_deep_entry_rank` cho extract/xref/footnote-map (ưu tiên GDoc native theo MIME + corpus + NLM-live; tên DÀI toàn chữ-gạch-dưới KHÔNG bị nhận nhầm DriveId → bug C TRỌN VẸN); (2) `_classify_ref` kiểm VBHN-COVERAGE TRƯỚC TYPO/MISSING (số hiệu gốc đã có VBHN → OUTDATED); (3) ENTRY_RAW_NO_GDOC rc=2 + ok:false (đúng yêu cầu báo cáo: chỉ-raw → rc≠0). NHÓM A-E (log đa-profile): B(NGHIÊM TRỌNG) `_ingest_target`/`nlm-add`/`nlm-query` push/query nhắm NOTEBOOK CỦA PROFILE (TL_NOTEBOOK_ID) — hết đẩy nhầm VBQPPL base khi `--profile NQ36` (+nlm-add/nlm-query nạp apply_profile_offline). A1 `profile-create --apply` GHI BỀN config.profiles.<name> (`_persist_profile_config` merge) → profile-info hết fallback VBQPPL. A2 next-steps cấm copy sheet VBQPPL tay (orphan), dùng `manifest` tạo registry rỗng. C1 `nlm-reconcile` BẮC CẦU gdoc↔source_id (`_nlm_source_drive_id` + link_candidates: nguồn live khớp drive_id/số hiệu của dòng registry thiếu source_id → backfill, hết 'unregistered' giả). C2 `register --nlm-notebook-id` (khỏi backfill-notebook riêng). C3 `backfill-notebook` khóa ĐÚNG NGUỒN: --src-ids→nlm_source_id, --drive-ids→drive_id (hết lệch khóa). D1 cảnh báo profile non-default + categories=inherit (văn bản vào cây chung VBQPPL). D2 `regen2` LOẠI registry/manifest/orphan (mime spreadsheet/json + tên + registryDocId/manifestId) khỏi scan own (hết 3 dòng corpus rác, count 8→5). D3 `reg-delete --force` (đã có) + thông điệp rõ. E1 `nlm_cli._strip_keyring` lọc 'Using keyring backend' khỏi stdout/stderr (hết vỡ json.loads). E2 `reg-query --refresh` (đã có) + help nhắc refresh sau khi ghi sheet. LARGE-FILE: `ingest-local` cổng HỎI TÁCH file > ~1.2MB (NLM_LARGE_SRC_BYTES, --large-threshold) → DỪNG gợi ý tách theo Phần/Chương/Điều (chất lượng RAG cao nhất), `--allow-large` để nạp nguyên (+SKILL.md doctrine). RÀ SOÁT ĐỐI KHÁNG (review+verify) gia cố 14 phát hiện: Group B `_resolve_nlm_notebook` (profile DỰ ÁN thiếu notebookId → ERROR, KHÔNG fallback VBQPPL base — vá GỐC bug B, guard cũ là dead-code vì base luôn truthy) áp nlm-add/query/get/reconcile/cross/ingest-local; C1 link theo số hiệu CHỈ khi DUY NHẤT (số VBHN tái dùng → bỏ qua, hết false-link); cmd_extract positional+--sohieu → ƯU TIÊN --sohieu; `_persist_profile_config` ghi NGUYÊN TỬ (temp+os.replace); `_is_infra_file` chặn false-positive (văn bản GDoc/PDF KHÔNG bao giờ là infra); `_strip_keyring` JSON-safe (chỉ bỏ dòng nhiễu THUẦN, không nuốt thân JSON có cụm keyring); large-file gate ra STDOUT. +6 test → selftest 206/206. # 1.22.69: vá 13 lỗi CÔNG CỤ từ 2 BÁO CÁO RÀ 71+105 LUẬT. A `tl status` verdict→rc=0 (REVIEW/ADD/SKIP = PHÁT HIỆN dữ liệu ≠ lỗi lệnh, hết phá &&/CI; +`--strict` mirror xref; preingest_gate.verdict_exit). C/P0-1 resolver đọc sâu: `_entry_score` PHẠT -300 file THÔ (.docx/.pdf/.html) → GDoc native THẮNG sidecar CÙNG số hiệu (hết xref/footnote im-lặng stdout-rỗng-rc0 bỏ sót ≥6 VBHN); ENTRY_RAW_NO_GDOC in STDOUT (caller agentic THẤY); `_resolve_base_gdoc` fallback drive_id khi sohieu rỗng. B+P1-3 xref: `extract_refs` DEDUP theo SỐ HIỆU (1 phán quyết/số hiệu/run — hết MISSING+MISMATCH mâu thuẫn + phantom 'DCHIẾU 258 này có hiệu lực…' do bắc-cầu mệnh-đề-chuyển-tiếp) + `_clean_ref_name_phrase` cắt prose (GIỮ tên luật thật 'Thi hành án dân sự'). P0-2 `DOC_TEXT_SOHIEU_TYPO` KHÔNG bắc cầu QUA HỌ loại VB (`_doctype_family`: QH≠NQ-TW≠KL-TW≠NĐ-CP — tái dùng số+năm hợp pháp; CÙNG họ QH14↔QH15 vẫn flag). P1-4 source-map: >1 VBHN CÙNG số hiệu KHÁC chủ đề → canonical=None + VBHN_REUSE_AMBIGUOUS_NO_CANONICAL (đòi --subject/năm; CÙNG chủ đề/nhiều version vẫn chốt). P1-5 amendment-detector: LOẠI văn bản PHI quy phạm (sohieu=∅ + 'góp ý/kiến nghị/ý kiến'); PAUSE_AND_ASK_USER CHỈ khi có ứng viên MANG SỐ HIỆU hợp lệ (sohieu=∅ vẫn liệt kê, confidence=low). P2-6 vbhn-check: CONTENT_VERIFY_REQUIRED chỉ khi collision CỦA CHÍNH số hiệu ứng viên (KHÔNG corpus-wide → hết 86 cờ máy móc); verified+năm+duy-nhất+không-tự-collision → VBHN_METADATA_OK. H `tl doctor` cảnh báo TRÔI registry↔NLM (đếm cờ OFFLINE từ cache → gợi ý `tl nlm-reconcile`, KHÔNG chặn/mạng). D `_read_doc_text`+`cmd_xref` TÁI DÙNG cache `extract_<gid>.txt` (Bộ luật Dân sự hết export lại 3 lần→timeout). E `standardize_name.normalize_name` bỏ đuôi .doc/.docx/.pdf khỏi tên CHUẨN (GIỮ ở tên FILE gốc). G `hygiene` bucket `sidecar_corpus_fix` (.docx cạnh GDoc mà corpus=true → đề xuất SET_CORPUS_FALSE). P2-7 chuẩn hoá ENUM `loai`/`hieuluc` lúc register (`_normalize_loai`/`_normalize_hieuluc`) + bucket hygiene `loai_noncanonical` (KHÔNG nhồi `_title_flags` → tránh nhiễu source-map). 2.2 nlm PATH: `nlm_cli` nối ~/.local/bin+user-base bin vào PATH (shutil.which + subprocess env); `doctor` dùng `nlm_exe()` (hết báo đỏ giả); `nlm-install` ghi PATH bền ~/.profile/~/.bashrc (POSIX). +14 test → selftest 194/194. HOÃN P2-8 (tách MISSING ngoài-phạm-vi-corpus vs resolver-trượt — cần enrich manifest). RÀ SOÁT ĐỐI KHÁNG (workflow review+verify) gia cố 9 phát hiện: cmd_status dùng inspect.signature thay except-mù + GIỮ ngữ nghĩa --strict ở fallback (rc=2→1); `_entry_score` chỉ phạt raw CHƯA-trên-NLM (raw đã-push NLM = canonical thật, không hạ oan); P1-4 `_subj_keys` chỉ đếm tail CHỦ-ĐỀ-RÕ (bản tên-trơ không gây false-ambiguity); P1-5 gate góp-ý theo SỐ HIỆU REGISTRY (file 'Góp ý Luật 64/2020' có số trong TÊN vẫn bị loại); `_normalize_loai` gộp mọi ký tự lạ (kể cả ngoặc); cmd_register log khi chuẩn hoá loai/hieuluc; preingest_gate main() thêm --strict. # 1.22.68: rà 133+81 LUẬT (2 log live) — vá robustness phần A. P1 RAW-ENTRY PRECONDITION (gốc chung log2 A1/A2/A3): xref+footnote-map gặp entry THÔ (.docx/.pdf/.html chưa convert GDoc) → ENTRY_RAW_NO_GDOC rc=0 + thông điệp gọn (thay rc=2/JSON-lỗi-thô/stdout-rỗng/rò "Export only…"); `_is_raw_no_gdoc_name`/`_raw_no_gdoc`/`_emit_raw_no_gdoc` THỐNG NHẤT .docx↔.pdf. P2 FOOTNOTE DEDUP (log1 A2): resolve_footnote_amendments GOM dieu_level_amendment_map theo (dieu,khoan,diem,amending_sohieu) — hết 47 dòng pending trùng (Đ73K1 ×3); footnote_defs giữ ĐỦ marker + footnote_raw_count. P3 BASE_NO_CLUSTER (log1 A1): rasoat-chongcheo CỜ RÕ khi base ngoài cụm E2 (61/133 trước no-op IM LẶNG) → dựa xref/footnote-map cấp Điều. P4 DEDUP related theo sohieu (log1 A6, hết 85-2015 ×4). P5 missing_in_corpus→`unresolved_refs`+note (log1 A5: CHƯA kết luận vắng mặt, khớp exists=UNKNOWN_NOT_ABSENT). A4 BASE_UNRESOLVED khi base tên/file thô không số hiệu. P7 strip keyring khỏi gws_bridge error (log2 A3). +2 test → selftest 179/179. CÒN (data/feature): mở rộng subject_clusters 45 chủ đề; parser khoản-điều-thêm (6a/16b, A3 log1 nhỏ); Cowork batch-checkpoint (A4 log2); GAS serial (A5 log2, frozen). + `drive-push --name`/`--rename-to-file` (đổi tên file Drive THEO TÊN FILE upload, GIỮ fileId — qua gws_bridge.rename có ASSERT). # 1.22.67: rà 59 LUẬT (log live) — vá 6/7 lỗi CÔNG CỤ (phần A). A1 `tl extract <số hiệu>` (vị trí) HẾT 404 giả: positional không-phải-gdoc-id(≥20 ký tự alnum)→tự định tuyến --sohieu (+SKILL.md). A2 vbhn-check suy subject SẠCH: `_clean_subject_text` bỏ hậu tố `_HL<ngày>`/goc/SuaDoi/ngày-trơ → query QT-5 web hết "thu do hl2026 07 01 hợp nhất" (đặt `_HL_SUFFIX_RE`, KHÔNG clobber `_HL_DATE_RE` thân-văn-bản — bắt được name-collision). A3 exit-code: xref/vbhn-check rc=0 khi CHẠY OK kể cả có MISSING/MISMATCH/no-hit (phát hiện ≠ lỗi lệnh, không phá &&/CI); `xref --strict` mới rc=1 (+SKILL.md). A4 extract cảnh báo chạm CAP export ~200k ký tự (văn bản dài có thể bị CẮT → cache-build). A6 `_strip_keyring_noise` lọc 'Using keyring backend' khỏi output gws subprocess. A7 `CONTENT_VERIFY_REQUIRED` CHỈ bật khi rủi-ro-tái-dùng-số/thiếu-metadata (>1 ứng viên/collision/bare-number/missing-year); metadata RÕ+DUY NHẤT → `VBHN_METADATA_OK` (giảm 37/59 cờ máy móc). A5 (GAS tuần-tự, không scale) = giới hạn webapp FROZEN, không sửa client. +4 test → selftest 177/177. # 1.22.66: HỢP NHẤT bản Codex v1.22.65 (cùng rẽ từ v1.22.64 — 2 nhánh CÙNG vá batch-2 run-log, KHÁC code). GIỮ bản Claude làm base (đã verify 173/173 + có `status_pending` PENDING_AMENDMENT_NOT_IN_VBHN + cụm `dau_tu_PPP` mà Codex THIẾU). PORT 2 cải tiến robustness CHỈ-CÓ-Ở-CODEX: (1) vbhn-check/vbhn-verify nhận POSITIONAL `target` (tương thích runbook cũ: `tl vbhn-verify "14/VBHN-VPQH"` tự định tuyến text-file/gdoc-id/sohieu qua `_read_verify_text`; `tl vbhn-check "84/2015/QH13"`→goc/subject); (2) reg-query --json ENVELOPE chuẩn {ok,schema:reg-query.v2,count,limit,rows,entries} (cả rows+entries cho mọi parser). Các fix batch-2 TRÙNG (doctype/PPP-alias/sidecar/issue_year-goc/dedup-VBHN-first/xref-typo/vbhn-verify-json/relation-check) GIỮ bản Claude đã verify-live (Codex impl khác nhưng chưa verify). Codex thiếu status_pending → giữ bản Claude. selftest 173/173. # 1.22.65: vá 6 RUN-LOG batch-2 (workflow điều tra+verify đối kháng trên COPY CÔ LẬP — canonical md5 NGUYÊN, agent KHÔNG đụng được). 10 fix: srcmap_name_resolution (query nêu "Luật/Bộ luật"→ƯU TIÊN hit tier≥Luật `_query_doctype_tier`, hết chốt NĐ/TT: "Luật Đầu tư"→VBHN_03 KHÔNG NĐ; PPP≡"đối tác công tư" vào _ABBREV_MAP→VBHN_123; LOW_CONFIDENCE hết over-fire khi có hit-strong tier-Luật); issue_year_goc_token (`_strip_goc_token`+reject năm-bản-gốc: VBHN_123 hết issue_year=2020 từ token goc_64-2020); dedup_vbhn_first (dedup áp VBHN-first qua goc-chain dù KHÁC số hiệu: 64/2020→canonical VBHN 123, gốc SUPERSEDED); relcheck_footnote_only_fp (chỉ giữ luật THỰC SỰ sửa base, hết bơm FOOTNOTE_AMENDMENT_NOT_IN_CORPUS từ dẫn-chiếu/chuyển-tiếp); status_pending_vbhn (preingest SKIP→USE_VBHN nay cảnh báo PENDING_AMENDMENT_NOT_IN_VBHN khi VBHN ra đời TRƯỚC sửa-pending); corpus_nlm_sidecar_fp (`_dup_of_live_sibling`: không flag CORPUS_TRUE_NOT_ON_NLM cho sidecar-raw khi anh-em GDoc đã trên NLM); relcheck_json_types (int→`amendment_candidates_subject_filtered_count`); vbhn_verify_json_schema (`_vbhn_verdict`→field verdict/official/provisional + populate head_sample); xref_sohieu_typo (`_classify_ref`→DOC_TEXT_SOHIEU_TYPO khi số hiệu near-match KHÁC mã cơ quan, vd 41/2024/QH14 vs QH15); cluster_ppp (THÊM cụm dau_tu_PPP base 123/VBHN). SKIP: xref_alias (false-alarm), regquery_json+skill_cli (ĐÃ đúng trên v1.22.64 — log là DEPLOY-LAG zip Drive v1.22.35). +10 test → selftest 173/173. # 1.22.64: vá 6 RUN-LOG (workflow điều tra+verify đối kháng 16 issue → áp 15 fix, 1 reject-trên-cơ-sở). name_rank_collision (CHÍNH): source-map/exists "Luật Dân số/Việc làm/Phí lệ phí/BLLĐ" HẾT chốt SAI canonical (Dân chủ/NLĐ-nước-ngoài/Học phí/ATVSLĐ) — `_name_strong_match` + gate `LOW_CONFIDENCE_NAME_MATCH` (canonical=None khi khớp-MỜ) + `_name_phrase_match` ≥2-token (reg-query --name hết match-all 87→2); LIVE 3/4 nay chốt ĐÚNG, 1 LOW_CONFIDENCE. cluster BHYT neo `y_te_kham_chua_benh` (subject_clusters.json, hết lao_dong). vbhn-verify: HEADER_NOT_CLEAR nhận số-hiệu "NN/VBHN-" + ASSEMBLED CHỈ soi TÊN (hết "không đúng" thân→ASSEMBLED giả). status→USE_VBHN (41/2024→19/VBHN). CORPUS_TRUE_NOT_ON_NLM suppress khi nlm_status=removed_*. footnote `_multi_diem` ("điểm c và d"). `_strip_font_runs` (bỏ dòng "Times New Roman"). relation-check --json preamble→stderr + skip backfill cho quarantine. `tl up` fallback init-config. `_scan_inline_amendments`+E1 LIEN_DOMAIN (Điều 53 sửa luật khác cụm). sohieu-exact ưu tiên fuzzy. REJECT đúng: vbhn_year (sẽ regress year-reuse). +13 test → selftest 164/164. (⚠ vài agent workflow vi phạm "no-edit" → ĐÃ revert clean v1.22.63 + áp lại CHỈ patch đã-verify thủ công.) # 1.22.63: ★ HỢP NHẤT 2 nhánh v1.22.62 (Codex ⊕ Claude, đổi xứng) — (A·Codex) vá log hygiene/NLM/pending: tên "Luật X"↔canonical, footnote-map body_effective_dates (pending hết 0 giả), hygiene lọc OMNIBUS_NARROW khỏi query hẹp + không emit cluster canonical=None, reg-query/summary nlm-live-aware + cờ CORPUS_TRUE_NOT_ON_NLM/NLM_NOTEBOOK_ID_MISSING. (B·Claude) `tl up` BOOTSTRAP TẤT ĐỊNH 1-lệnh (config→gws cred+binary→nlm→manifest→readiness; helper CHUNG `_ensure_gws_nlm` cho init-config+up) + `tl confirm`/`_verify_header_match` (ĐỌC HEADER xác minh sohieu/tiêu đề/loại/cat khớp tên+thư mục → nhãn registry.verified; source-map/dedup TIN entry confirm, bỏ DIRTY/WARN) + upload-flow `_upload_mime_ext` (.doc/.pdf upload MIME THẬT → Drive organize convert server-side). selftest 153/153 (147 Codex + 6 Claude). # 1.22.62: vá log hygiene/NLM/pending — tên luật dạng "Luật X" khớp canonical đuôi "X"; footnote-map đọc thêm Điều hiệu lực trong thân luật gốc (body_effective_dates, pending không còn 0 giả); hygiene plan lọc OMNIBUS_NARROW_TITLE_CHECK khỏi query chủ đề hẹp và không emit cluster apply với canonical=None; summary/reg-query phơi nlm_source_id+nlm_notebook_id live-aware, flag CORPUS_TRUE_NOT_ON_NLM/NLM_NOTEBOOK_ID_MISSING. 1.22.61: vá log Chat/Cowork — #2 (CHÍNH: "Chat không cài gws+nlm từ đầu") init-config --from-public GỘP gws BINARY (gws-bootstrap-cowork → find/GHI hết FALLBACK→GAS) + cờ --nlm (uv-install+auth) = 1 lệnh bootstrap đủ; SKILL.md startup MỌI env dùng `--from-public --nlm`; --no-binary để chỉ-cred. #1 (NGUY HIỂM) exists/source-map: VBHN-first redirect CHỈ khi query LÀ BẢN GỐC (base = năm nhỏ nhất chuỗi goc, `_vbhn_base_key`) — 114/2025 Phòng bệnh (luật-sửa NẰM TRONG chuỗi VBHN thuốc lá) hết bị chốt canonical=VBHN thuốc lá; thêm bucket `amends_vbhn` + cờ AMENDS_OTHER_VBHN/MULTIPLE_VBHN_BASE. #3 source-map dương-tính-giả: `_vb_tier_rank` chặn SAI THỨ BẬC — NĐ/TT (118/2016/NĐ-CP) KHÔNG thể 'sửa đổi' Luật → hết AMENDMENT_CANDIDATE+PAUSE giả (đọc loại cả từ TÊN khi sohieu rỗng; base=tier cao nhất nhóm). #5 source-map NỔI `PENDING_FUTURE_EFFECT` + pending_future_count (đếm VB hiệu-lực-tương-lai, rẻ-không-footnote-map). +7 test → selftest 140/140. # 1.22.60: log rà BHYT (workflow điều tra+verify đối kháng) — #5 extract --sohieu khớp entry sohieu-RỖNG qua _sohieu_key_entry (parse từ TÊN '114_2025_QH15_658530'); #1 gws_bridge.rename ASSERT đọc-lại-tên (hết nuốt-lỗi-im-lặng rename 200-nhưng-không-đổi); #4 footnote-map _footnote_rel_kind = CROSS_CUTTING (omnibus 35/2018) / PARTIAL_REPEAL (bãi-bỏ-cục-bộ 32/2013) → hạ ưu tiên; #3 preflight TỰ KHÁM PHÁ overflow notebook từ registry (row_kind=overflow) khi config trống/placeholder (phòng thủ; config canonical đã có id thật). #2 slot over-count: đã sạch sẵn (L5), "329" trong log là GAS server-side. selftest 133/133. 1.22.59: log rà BHYT — B1 subject_clusters.json THÊM cụm `y_te_kham_chua_benh` (base 40/VBHN-VPQH BHYT + KCB 15/2023 + Phòng bệnh 114/2025 + Dược + ATTP) → rasoat-chongcheo BHYT neo ĐÚNG cụm y tế (trước neo nhầm lao_dong_xa_hoi); B3 cờ OMNIBUS hết false-positive trên luật-sửa TÊN-SỐ-TRƠ (chỉ flag khi chủ đề RÕ + khác lĩnh vực, ≥2 token); B5 `_summ_entry.nlm` = LIVE (`_entry_on_nlm_live`, False nếu removed) → relation-check khớp reg-query; B6 message gws fallback PHÂN BIỆT thiếu-cred vs thiếu-binary. 1.22.58: B1 GWS — `_read_doc_text` ƯU TIÊN direct-media EXPORT text/plain bằng CRED (KHÔNG cần binary gws → extract/footnote-map hết rơi GAS ở Cowork khi đã gws-auth-load; B5 hết spam); init-config đổi thông điệp "gws cred ✓ (direct-media đọc; find/ghi cần gws-bootstrap-cowork)" hết hiểu nhầm "BẬT". locate FALLBACK webapp gắn LOW_CONFIDENCE/NO_EXACT_SOHIEU (Cowork: locate 58/2014 → fulltext lạc đề). `_entry_subject_text` BỎ `cat` (nhãn folder '02_Bao_hiem' làm mọi entry khớp 'bảo hiểm' giả) → relation-check vbhn_candidates 14→3 (BHXH/KDBH/ATVSLĐ). 1.22.57: ★ GỐC RỄ "subject filter quá lỏng" (phát hiện khi chạy mục B live) — `_subject_score` CHỐNG nhiễu từ-phổ-biến: token-overlap chỉ tính ĐỦ khi entry chứa CỤM-ĐẦU PHÂN BIỆT của chủ đề ('bảo hiểm'='baohiem'); nếu không (chỉ trùng 'bảo/hội' lẻ ở từ-khoá) → 0 điểm. → relation-check vbhn_candidates hết kéo Luật Xuất bản/Người cao tuổi/Thanh niên/Công đoàn (sscore 40→0); BHXH=140, BHYT=0(disc), giữ KDBH=60. 1.22.56: vá log rà BHXH (Chat+Cowork) — (regression) `locate` cụm danh từ ('bảo hiểm xã hội') KHÔNG còn bị coi là số hiệu → hết LOW_CONFIDENCE/NO_EXACT_SOHIEU giả (gate `_looks_like_sohieu_query`); `tl rasoat worksheet` TỰ dựng cache nếu thiếu (`_rasoat_autocache_worksheet`→`cache-build`, resolve gdoc từ manifest; --no-auto-cache để tắt) + message worksheet trỏ `tl cache-build`; `_find_amendment_candidates` thêm loại-trừ-chéo `_disc_conflict` (BHYT/BHTN khác BHXH); SKILL.md BƯỚC 0 TÁCH `--setup` (core nhanh) khỏi nlm (né timeout 45s Cowork). 1.22.55: #8 HỢP NHẤT footnote-map vào relation-check + rasoat-chongcheo — TỰ đọc nguyên văn base VBHN (auto-footnote, `_resolve_base_gdoc`, tắt --no-auto-footnote) → 2 lệnh nêu footnote_amendments thay vì rỗng; #11 cờ OMNIBUS_CROSS_DOMAIN (`_omnibus_cross_domain_note`): luật sửa có tên khác lĩnh vực base (84/2025 Thanh tra sửa BHXH = sửa-nhiều-luật) → cảnh báo đọc nguyên văn, KHÔNG hiểu nhầm lỗi tên. +test omnibus_cross_domain_flag. 1.22.54: ★ GỐC RỄ tên VBHN VIẾT TẮT — `_expand_abbrev`/`_ABBREV_MAP` (BHXH≡bảo hiểm xã hội, BHYT/BHTN/BLHS/BLLĐ…) nối vào `_token_set`+`_disc_conflict` → source-map/relation-check/reg-query/locate khớp đúng VBHN_19…BHXH (trước nhặt nhầm bản gốc 41/2024 viết-đầy-đủ đã quarantine). #3 extract: phân biệt CẮT-CỤT (export cap ~200k) vs sai cấu trúc → chỉ `tl cache-build --gdoc-id` lấy toàn văn. #10 locate: cờ LOW_CONFIDENCE/NO_EXACT_SOHIEU khi truy vấn số hiệu chỉ khớp-mờ-tên (vd 142/2025→VBHN_74 Đấu thầu). 1.22.53: log rà BHXH — A3 relation-check `_vbhn_candidates` KHÔNG nhận VBHN trùng-NĂM khác lĩnh vực (year-một-mình cần subject≥30; +disc_conflict) → hết VBHN_43 Xuất bản lọt vào BHXH; A4 `_cluster_for_base` reverse-map qua THÀNH VIÊN cụm (số hiệu VBHN 19/VBHN-VPQH → cụm, trước trả ∅); B1 rasoat alias --sohieu→--so-hieu (worksheet) / --file→--in (phuluc); B2 `tl cache-build <sh>` wrapper ingest_to_cache.py (sinh docs/<sh>--consolidated.json); B3 ingest_to_cache.py tự nạp webappUrl/token từ config/env. 1.22.52: TRA-THEO-TÊN âm-tính-giả (log Cowork #2/#3) — `_name_subset_match` token-subset (bỏ doctype/sốhiệu) cho source-map/locate/reg-query: 'Luật Bảo hiểm xã hội' KHỚP 'VBHN_19-VPQH_Bao_hiem_xa_hoi' (substring liền thất bại vì luat/vbhn/19 chèn giữa); reg-query --name trước CHỈ substring CÓ DẤU → 0 kết quả, nay khử dấu+token-subset. `_disc_conflict` chuẩn hoá underscore (BHXH↔BHYT đúng cả tên file). `_nlm_display` status-aware (locate hết báo nlm=Y khi removed → khớp reg-query). +test name_subset_match_vbhn/source_map_name_finds_vbhn_not_quarantine. 1.22.51: (A) ENV THỐNG NHẤT Chat=Cowork=Code — gỡ doctrine "chat hạn chế": nlm CLI BẮT BUỘC mọi env, gws-bootstrap BỎ QUA tải binary nếu gws đã có (--force ép), Chat dùng uv+python≥3.11 sẵn (không tải Drive). (B) footnote-map nhận "Cụm từ '…' được BỎ/THAY THẾ theo…" (84/2025 hết vô hình, +test footnote_remove_phrase_amendment); subject-score LOẠI TRỪ CHÉO BHXH↔BHYT↔BHTN (chung "bảo hiểm" ≠ cùng chủ đề, +test subject_bhxh_not_bhyt). 1.22.50: vá log Chat — B1/B2 `gws-auth-load`/`nlm-auth-load` + `init-config --from-public` tự bật gws từ cred PUBLIC (public-curl, KHÔNG cần master key); B3 gom log [FALLBACK→GAS] 1 lần/phiên (hết spam mỗi read); relation-check LỌC ứng viên chỉ-trùng-chủ-đề khỏi amendment_candidates (giảm dương-tính-giả 108/2026); B5 xref OUTDATED nêu RÕ số hiệu VBHN thay thế + SOHIEU_MISMATCH→VBHN ghi "đúng, trỏ bản mới". (B4 phantom-217 đã có test footnote_citation_not_amendment.) 1.22.49: SKILL.md §1 BƯỚC 0 — Cowork dùng KHỐI INLINE (curl zip public + unzip + chạy tl_fetch.sh SẠCH TRONG ZIP) vì mount cắt cụt CẢ scripts/tl_fetch.sh → `sh scripts/tl_fetch.sh` đường-mount hỏng. CẤM inspect/confirm truncation/dig-recovery (đã biết mount cắt). 1.22.48: GHI RÕ gws Cowork = BINARY MUSL-STATIC (đã verify static-pie, không GLIBC dep → chạy glibc 2.35) qua `gws-bootstrap-cowork` public-curl; CẤM `npm i -g @googleworkspace/cli` (bản GNU cần GLIBC 2.39, Cowork glibc 2.35 → không chạy). SKILL.md + help string. 1.22.47: nlm-install HẾT STALL ASTRAL — `uv tool install --python 3.11` chạy với UV_PYTHON_DOWNLOADS=never (cấm tải python từ astral/GitHub CDN bị Cowork chặn): system có 3.11→dùng ngay, chỉ 3.10→FAIL TỨC THÌ→rơi Python public-curl Drive; bỏ `uv python install 3.11` thừa. 1.22.46: BOOTSTRAP TỐC ĐỘ — `_fast_drive_fetch` ưu tiên PUBLIC-CURL (drive.usercontent) → direct-media → GAS, có ĐO THỜI GIAN ([fetch] log); PY311 + gws binary tải public-curl (hết kẹt GAS 31MB); tl_fetch.sh cài uv TRƯỚC (pip PyPI, astral chặn) rồi gws/nlm; rút timeout astral uv-python 420→90s (fail nhanh → Drive-public). 1.22.45: SKILL.md §1 BƯỚC 0 — Cowork ƯU TIÊN `sh tl_fetch.sh --setup` LÀM LỆNH ĐẦU TIÊN (tải bản sạch, KHÔNG đụng mount/_parts); CẤM chạy tl_boot/verify-integrity/build_parts/_parts TRƯỚC khi tl_fetch lỗi; tách rõ đường LOCAL A1–A3. 1.22.44: PACKAGE PUBLIC BOOTSTRAP — config v2 + creds (gws/nlm/secrets/binary/py311) ở Drive/Package (anyone-with-link). `init-config --from-public` + tl_fetch.sh curl CONFIG(apps script)+gws cred TRƯỚC (KHÔNG cần Drive MCP); uv-first cho nlm; Cowork tải zip skill; tl_boot loud-fail exit≠0 khi cắt cụt (B2); tl_rebuild.sh OUT mặc định $HOME (B4). 1.22.43: `tl drive-push <zip> [--file-id]` — cập nhật NỘI DUNG file Drive GIỮ fileId (gws update_content) → đẩy bản ship mới mỗi lần mà KHÔNG đổi fileId; SKILL_FILEID baked. 1.22.42: BUNDLE skill+gws — `gws-bootstrap-cowork --local-tgz` (dùng gws.tgz từ bundle, khỏi tải Drive; md5 vẫn verify); tl_fetch.sh tự dò assets/gws.tgz. Cắt 1 download. 1.22.41: `nlm-install --uv` (egress mở → uv tự lo Python 3.11, python hệ thống nếu ≥3.11, KHÔNG tải 31MB Drive; fallback Drive); `tl_fetch.sh --setup --nlm` dùng --uv → bootstrap đủ GAS+direct-media+gws+nlm+boot 1 lệnh. (v1.23.0 spec rasoat-loop/overlap: roadmap riêng.) 1.22.40: bake NLM_CRED_FILEID (đã stage+verify) → `--setup --nlm` có nlm headless ngay. 1.22.39: nlm HEADLESS — `nlm-auth-stage` (Code, sau `nlm login`: cookie nlm → mã hoá khoá=webapp-token → Drive) + `nlm-auth-load` (Cowork: tải+giải mã bằng token → ~/.notebooklm-mcp-cli, KHÔNG cần master key); `--setup --nlm` tự nlm-auth-load (mirror gws-auth-stage/load). 1.22.38: tl_fetch.sh ROUTE TỐI ƯU (curl public, $HOME, --setup) + gws TRƯỚC nlm. 1.22.37: tl_fetch.sh webapp GAS. 1.22.36: tl_fetch.sh bỏ qua mount. 1.22.35: tl_rebuild.sh + MANIFEST.sha256 + tl_boot verify sha. 1.22.34: dọn references/ 63→24 file. 1.22.33: _parts ≤200 file. 1.22.32: verify-integrity + COWORK_EDIT_SAFETY. 1.22.32: `tl verify-integrity` + COWORK_EDIT_SAFETY (write-side fallback); 1.22.31: truncation-resilience (FORCE _parts; _healed_script_path; --rebuild) + doctor nlm/gws + reg-query khóa NLM; 1.22.27: #4/#3/#6/#9; 1.22.26: #1 relation-check footnote-gate
# GĐ0 (tích hợp gws): PIN bản gws — KHÔNG `latest` (gws pre-v1.0 hay breaking). Nguồn-chân-lý
# duy nhất cho boot-check `tl gws-ping` và (GĐ1) gws_bridge.is_available(). Bump có chủ đích.
VERSION = "1.34.13"             # 1.34.13: I9a — bước 2/3 chiến-lược-chặng-cuối: tách INFRA đa-module đợt 1 (đổi-luật-có-kiểm-soát đã grill) — classify.py (74 def ~1.22k dòng: loai/cat/title_vn/header-facts/strip-accents/sentence-case + misc-affinity>50%) + profile_env.py (36 def ~512 dòng: config/creds/profile-env/GAS-webapp/transport-helper) sang tl_core/; tl.py 8684→7177 (lũy kế 19052→7177, −62%; 11 module). ★Máy cắt I9a có 2 scanner MỚI: (a) TOP-LEVEL scanner — hàm được statement top-level gọi TRƯỚC bind phải ở lại (_ensure_writable_tmpdir/main/_tl_core_import tự loại); (b) AFFINITY assignment — def chưa-nhóm chỉ kéo theo khi >50% tham chiếu đến từ nhóm đang cắt. Characterization = 711 test hiện có (classify/profile_env là vùng phủ DÀY nhất codebase: r10/r11 title-block, _infer_loai case-list, r57 profile-env, r73a title-zone, r74a fixture-config) — PASS Y NGUYÊN sau cut, KHÔNG sửa test nào. +r79 wired/no-dual → 713/713. Kế: I9b resolve+regio (đổi r76 engine-stays → canonical-ở-resolve.py) rồi I10 nén stub. // 1.34.12: I8 — tách 56 def nhóm lệnh vận-hành/chẩn-đoán (~2.0k dòng NGUYÊN VĂN AST-cut: 32 cmd doctor/ping/precheck/boot/up/perf/bench/reg-query/counts/exists/registry-map/cat-list+verify/journal/undo/resume/confirm/manifest/backfill-notebook/vbhn-normalize/reg-delete/init-config/config-pin-registry/edit-skill/verify-integrity/instructions/instruction-audit/loop/cowork-plan/source-verify/profile-file-remove/convert-verify + 24 helper riêng-nhóm) sang tl_core/ops_misc.py; tl.py 10712→8684 (lũy kế 19052→8684, −54%). Chiến lược 3-bước grilling: I8 misc-cmd ✓ → I9 infra-module → I10 nén stub. ★Bẫy mới: canary REQUIRED-list nằm TRONG _skill_package_integrity (hàm bị move) → vá canary trong NỘI DUNG MODULE; mirror _LOOP_LIVE_FIELDS (bẫy I2 default-param, r78_loop_fields_mirror). Converter tự LOẠI def đã-ủy-quyền (thân chứa _tl_ — 6 wrapper). Characterization +4 r78a (reg-query bare-VBHN 1-chiều; counts mẫu-số; exists A3-doctrine rc=0/2; journal TL_JOURNAL_DIR) — PASS y nguyên sau cut; 2 guard test (legacy-registry/clobber) trỏ nguồn thật ops_misc. +r78 wired/no-dual/mirror → 711/711. // 1.34.11: I7 wave-2 — HOÀN TẤT Pha E bề mặt lệnh: +78 COMMAND_META baseline bằng-chứng-cờ (phủ registry 131→160 lệnh khi tính spec-only; --apply→dry_run, --confirm→confirm, ghi ngoài-repo→medium+scope đích, KHÔNG high mới — nâng high+contract để Pha-E-hoàn-thiện) rồi converter chạy lại: +78 lệnh SINH TỪ GENERATED_SPECS (tổng 124 spec; tl.py 11296→10712). Parser-surface snapshot KHỚP KHÔNG REGEN = bằng chứng tương đương byte. ★2 bẫy converter wave-2 (r77a bắt cả hai): (a) add_argument HẬU-set_defaults (ca sweep --live-nlm) → converter tiêu thụ tiếp sau set_defaults; (b) register_generated LOẠI dest khỏi kwargs (schema Pha E coi dest=positional) → cờ có dest= tường minh bị argparse tự suy dest khác (4 lệnh cache-snapshot/profile-doctor/file-remove/manifest) → dest-passthrough khi entry có flags. Còn 35 block tay có chủ đích (17 set_defaults phức [tlg.* + kwargs phụ], 9 kwarg-non-literal, 6 foreign-stmt, 3 has-comment). // 1.34.10: I7 wave-1 — 38 lệnh build_parser SINH TỪ GENERATED_SPECS (converter AST cơ học, flags/help NGUYÊN VĂN; chỉ block an-toàn: kwargs literal, fn=cmd_* trên tl, KHÔNG comment nội khối [giữ doctrine-comment tại chỗ], ĐÃ có COMMAND_META 1-dòng [bất biến r64 spec⇒generated=True]); tl.py 11602→11296; register_generated help-optional. ★CHARACTERIZATION MỚI: r77a PARSER-SURFACE SNAPSHOT — SHA256 per-command của bề mặt parser đầy đủ (opts/dest/nargs/const/default/type/choices/required/help/metavar/kind + handler, đệ quy nested; KHÔNG phụ thuộc thứ tự add_parser) tại references/golden/parser_surface.json 14KB; regen có chủ đích TL_WRITE_PARSER_SURFACE=1 — mọi drift CLI từ nay bị khoá vĩnh viễn (drift-lock mạnh hơn r64 nhiều bậc). Sau chuyển: surface KHỚP TỪNG HASH. Còn lại wave-2+: 113 block skip (78 thiếu meta [cần bổ sung COMMAND_META trước — việc hoàn tất Pha E], 17 set_defaults phức, 9 kwarg non-literal, 6 foreign-stmt, 3 has-comment). // 1.34.9: I6 — tách 16 cmd tra-cứu/quan-hệ + 25 helper riêng-cụm (~1.57k dòng) sang tl_core/lookup_ops.py (locate/source-map/status/relation-check+backfill/vbhn-check+verify+compare/xref/footnote-map/cluster/rasoat×3/header-verify/dedup-check); tl.py 13176→11602. ★RANH GIỚI GRILLING: động cơ _source_map_one (365d, 59 điểm test) + helper đa-module (_dedup_status/_classify_ref/resolve_footnote_amendments/_relation_audit/_rq_relation_probe/_scan_inline_amendments/_sohieu_query_hits_entry/_nlm_status_*/_qt5_search_hints) GIỮ Ở TL — r76_engine_stays_in_tl khoá cứng (def thật, không stub hoá). Characterization: +3 r76a wiring khoá shell cmd (source-map canonical shape/results-alias/verdict; MISS rc=0 A3-doctrine; status --amendment guard SKIP+ON_NLM offline). Scanner default-param 0 hit. +r76 wired/no-dual → 703/703. // 1.34.8: I5 — tách cụm ingest_pipeline sang tl_core/ingest_ops.py (37 def ~1.76k dòng NGUYÊN VĂN AST-cut: 12 cmd ingest-local/profile-ingest/ingest/ingest-analyze/ingest-route/ingest-missing/register/recat/source-rename+delete+update-corpus/shared-source-fix + 25 helper riêng-cụm: classification/_classify_doc_header+_sohieu_from_title_zone/verify-gate/chunk/mime/checkpoint/plan-helper); tl.py 14932→13176 dòng (lũy kế chuỗi I: 19052→13176 qua 7 module); bind REBASE __globals__ (khuôn I1-I4); scanner default-param 0 hit. WRITE-INFRA ĐA-MODULE GIỮ Ở TL: _journaled_reg_write/_apply_gate/_verified_reg_upsert/_reg_before_from_manifest (đếm-tham-chiếu: hygiene+nlm_ops+profile_mgmt cùng dùng). Characterization TRƯỚC cut: +5 r75a wiring offline (ingest-route ASK_USE_EXISTING/PROFILE_OWN; ingest-analyze letterhead→plan+lệnh điền sẵn; source-rename DRY gợi ý tên; shared-source-fix DRY group; register --bulk GUARDS P0-1 chặn drive_id-cắt-cụt/cat-rác KHÔNG ghi) — PASS y nguyên sau cut; 3 test getsource (recat/r55 ingest-local/clobber) trỏ nguồn thật. +r75 wired/no-dual → 697/697. // 1.34.7: I4 — tách cụm profile_mgmt sang tl_core/profile_mgmt.py (22 def ~967 dòng NGUYÊN VĂN AST-cut: profile-info/list/use/rename/delete/files/manifest/adopt/doctor/index/create/rebuild-registry + helper riêng-cụm); tl.py 15743→14932; bind REBASE __globals__ (khuôn I1-I3); scanner default-param 0 hit. Hạ tầng profile DÙNG CHUNG (_apply_profile_env/_profile_lookup/_read_config_record/_profiles_from_config/_persist_profile_config/_profile_policy_error/_active_profile) GIỮ Ở TL. ★FIXTURE-CONFIG tất định (references/golden/fixtures/config_fixture.json sinh-tại-chỗ, registryDocId pin sẵn) — cách ly trạng thái config máy (bài học CI I1): golden ops-plan HỒI SINH (hygiene_ops_plan_fixture_config: --config fixture + xoá env TL_* per-case, cross-machine). Characterization TRƯỚC cut: +4 r74a wiring trên fixture config (profile-list; profile-info CHỊU-LỖI-GÕ khoá P2 v1.33.48; profile-use DRY-không-ghi + PROFILE_NOT_FOUND; profile-rename DRY plan + cấm rename nền) — PASS y nguyên sau cut; test clobber-guard trỏ nguồn thật. +r74 wired/no-dual → 690/690. // 1.34.6: vá Nhóm 1+2 log phiên chạy thực 2026-07-09 (hồ sơ Luật BHXH — 3 defect profile văn-bản-thường): (#1) _classify_doc_header HẾT nhận số hiệu TRÍCH DẪN làm số hiệu tài liệu — sohieu CHỈ từ VÙNG TIÊU ĐỀ (head 1500, DÒNG NGẮN ≤80 ký tự kiểu letterhead, ưu tiên có Số: đứng trước — _sohieu_from_title_zone) + tên file; số trong CÂU VĂN DÀI = trích dẫn → BỎ (trước: báo cáo nhắc Luật 41/2024/QH15 bị gán loai=Luật+sohieu → ghi sai metadata âm thầm); nhánh VBHN N2a nay chạy CẢ khi sohieu title-zone rỗng (số VBHN ở khối ký cuối — quét sâu blob CHỈ dạng VBHN). (#3) _ingest_verify_gate bỏ vế OR-sohieu: requires_dieu CHỈ theo kind∈{vbqppl,draft,nq} — văn bản thường có số hiệu công văn không còn bị DIEU_STRUCTURE_NOT_VERIFIED chặn corpus_allowed (profile-ingest hết dừng nửa chừng phải nlm-add tay); +info flag DIEU_NOT_REQUIRED_NORMAL_DOC. (#2) bảng tính trọn đường ống: _MIME_BY_EXT +.xlsx/.xls (trước rơi về DOCX_MIME → convert fail); profile-ingest nhánh sheet = copy_convert toType=sheets → canonical Google SHEET + readback expected_gdoc_mime=_GSHEET_MIME (+param mới _verify_convert_readback) + NLM source_add doc_type=sheets nội bộ + skip text-gate (SPREADSHEET_TEXT_VERIFY_SKIPPED). TDD: 7 test r73a hành-vi-đúng viết TRƯỚC (4 đỏ đúng chỗ) → fix → 684/684. BACKLOG còn từ log: #4 nlm-add auto-detect --type sheets; #5 register clear cột thường (cần webapp GAS); #6 register auto-retry FIELDS_DROPPED; #7 ocr-run báo lệnh cài engine; #8 instruction-audit đồng bộ block-list từ gen_instructions; #9 user sửa Project Instruction version; #10 vbthuong categories=inherit→own (cần user duyệt). // 1.34.5: I3 — tách extract_cache (cmd_extract/cache-build/cache-snapshot, 3 def ~214d) + fetch_web (fetch-route/batch/links, find-doc, tvpl-url, external-ingest, link-priority, frontier + _fetch_plan/_external_ingest_plan, 12 def ~389d) sang tl_core/{extract_cache,fetch_web}.py; tl.py 16227→15743. Ranh giới đếm-tham-chiếu: hạ tầng đọc (_read_doc_text 16 site/_cache_file 13/_title_block_from_text 6/extract_dieu/extract_refs/_sanitize_export_text/_profile_cache_dir) + discovery QT-5 (_query_variants/_google_site_url/_discovery_links/_official_rank + _FETCH_SOURCES/_DISCOVERY_SITES/HOPNAP) GIỮ Ở TL. Characterization TRƯỚC cut: +5 r72a wiring (extract resolve+bóc Điều qua transport mock; tvpl-url pure; fetch-route VBHN-first+docx-rank; fetch-batch SKIP/REVIEW/FETCH+ckpt; fetch-links markdown+env) — PASS y nguyên sau cut; scanner default-param (bẫy I2) = 0 hit. +r72 wired/no-dual → 677/677. // 1.34.4: I2 — tách cụm nlm_wrappers/sharding sang tl_core/nlm_ops.py (28 def ~1.0k dòng NGUYÊN VĂN AST-cut: 13 cmd nlm-list/get/query/cross/content/add/orphans/reconcile/query-plan + preflight/push-overflow/overflow-resolve/slot-audit + 15 helper riêng-cụm reconcile-plan/dedup-gate/overflow-route+status/slot-count/sohieu-loose/preflight-invariants…); tl.py 17097→16227 dòng; bind REBASE __globals__ (khuôn I1). Helper ĐA-CỤM GIỮ Ở TL (_entry_on_nlm_live/_resolve_nlm_notebook/_nlm_display/_nlm_probe_summary/_nlm_status_known+removed/_gws_nlm_note/_entry_nlm_notebook_id — ranh giới đo bằng đếm-tham-chiếu-ngoài-cụm). Characterization TRƯỚC cut: +5 r71a wiring-test offline (mock _imp/_gas/registry-IO) khoá 5 cmd 0-hit: nlm-list shape, reconcile DRY 3 lớp desync/other/unregistered, preflight ⚠DUP-TL lỏng-năm + verify-LIVE slot, push-overflow verified-write, overflow-resolve MAX(reg,phys)+discover+gap — PASS y nguyên sau cut. ★Bẫy mới cho I3+: default-param `cap=NLM_SLOT_CAP` eval TRƯỚC bind → module cần MIRROR constant + r71_slot_cap_mirror drift-lock. +r71 wired/no-dual → 670/670. // 1.34.3: I1 — tách cụm hygiene_report sang tl_core/hygiene.py (29 def ~2.0k dòng NGUYÊN VĂN AST-cut: sweep/dedup-plan/missing-sohieu/vbhn-year-fix/ops-plan/corpus-audit/review-queue/backfill-loai+titlevn+hieuluc/hygiene/quarantine-fix/corpus-fix/consolidation-cleanup/cat-audit/registry-doctor + helper riêng-cụm); tl.py 19052→17097 dòng; tl giữ STUB ủy quyền mọi tên đã chuyển. ★ bind() hygiene KHÁC sibling: REBASE __globals__ từng hàm về namespace SỐNG của tl (monkeypatch selftest ăn ngay, helper không stale — copy-snapshot làm r54 gãy vì patch trên tl không thấm module). Characterization TRƯỚC cut: 6 golden hygiene_* trên FIXTURE MANIFEST (env per-case TL_CACHE_DIR — _run_tl_json +env_extra) KHỚP NGUYÊN TRẠNG sau cut; +bắt 1 bug thật: sweep phơi snapshot_age_s lọt deterministic mask (+snapshot_age_s/age_s/age_seconds vào VOLATILE_JSON_KEYS). Self-heal phủ module mới (canary/tl_boot preload/py_compile/REQUIRED/r36). +r70 parity (wired + no-dual-definition) → 662/662. // 1.34.2: Pha H live-smoke HOÀN TẤT (17 bước máy user, corpus net-zero diff {changed:0,unexpected:0}, apply_ready=true 3-tier LẦN ĐẦU — proof .tl_state/smoke_18_finaldiff.json) + vá 4 phát hiện smoke: (a) reg-query +--drive-id (10 contract readback hết drift doc↔CLI); (b) nlm-add --drive-id sau add OK + row TỒN TẠI → reg_link ngay (journaled+verified, chỉ cột nlm_*; không row → nhắc register/reconcile, KHÔNG tạo row xương — đúng ca S14 'unregistered'); (c) live-smoke-plan snapshot_diff +2 allow-prefix path THẬT (live_contract_report.nlm.notebook_get.source_count + contract_checks — hết 'unexpected' oan khi ghi hợp lệ); (d) contract text khớp parser (source_delete resume +--apply; reg_delete --drive-ids; nlm_add bỏ --json). +4 r69 → 660/660. Smoke đã tập sống: resume sau đứt mạng, overflow-route khi shard đầy 306/300, guard profile-nền, CONFIRM_REQUIRED zip, nlm-reconcile DRY bắt unregistered. // 1.34.1: siết-6 advisory ĐÚNG DEADLINE r65 — contract THẬT (idempotency_contract.v1 đủ 8 field, phản ánh gate+journal+verified-write có sẵn) cho register/drive-push/nlm-reconcile/push-overflow/shared-source-fix/source-update-corpus; _CONTRACT_REQUIRED = TRỌN 12 lệnh ghi high-risk (HẾT grandfather); meta requires_confirm=True cho shared-source-fix + source-update-corpus (khớp code --apply --confirm yes); KHÔNG đổi bề mặt CLI (grilling 2026-07-09 #6). r65 drift-lock: advisory set == RỖNG; +r68 wired/complete/confirm-meta. Cùng đợt, đã vá doctrine-loss v1.34.0 trước deploy (khôi phục NGUYÊN VĂN old 164-185 vào kernel §1 — F1 MÔI TRƯỜNG THỐNG NHẤT/F5 NLM-CLI mọi-env/F4 điều-kiện-kép notebook_create/F3 ⚠DUP-TL; +luật golden-test --write & .tl_state; sửa claim cờ toàn cục --json/--out). // 1.34.0: Pha F — SKILL.md kernel 91KB→41.7KB (user duyệt (a): TRÍCH NGUYÊN VĂN bất biến §0/§1-BƯỚC-0/§2/GATES, KHÔNG viết lại lời; §4→references/COMMANDS.md 27KB; §9→references/DEPENDENCIES.md 13KB; mapping references/SKILL_KERNEL_MAPPING.md); CHANGELOG 458KB→23KB (8 version + archive references/changelog_archive/); workflow-audit +kernel_size≤48KB +kernel_links (r67); xoá DRAFT sau promotion (chống 2-bản-doctrine). SAU DEPLOY: user re-import Capabilities. // 1.33.61: CI-fix #2 (run 2 nền tảng bắt 2 lớp bug máy-phụ-thuộc): (a) idempotency_key ingest-zip hash bytes CONTAINER → zipfile 3.12≠3.13 header khác → key lệch; đổi content-v2 = norm_path+CRC32+size từng member accepted (CRC sẵn trong central directory, re-zip cùng nội dung = cùng key — đúng ngữ nghĩa idempotency; r66 khoá STORED-vs-DEFLATED cùng key); (b) 3 writer atomic (_write_text/_write_json/_emit_json_payload) thiếu newline= → Windows ghi CRLF → manifest/golden hash lệch CI; +newline LF mọi OS (r66 khoá); .gitattributes `* -text` khoá byte toàn repo; renormalize 27 file CRLF di sản + regen goldens LF. Runtime-identical — ship cùng v1.34.0. // 1.33.60: CI-fix (run #1 GitHub Actions bắt đúng bug cross-platform NGAY LẦN ĐẦU — giá trị CI tự chứng minh): fixture zip DEFLATE cho bytes KHÁC NHAU giữa build zlib (Ubuntu zlib-ng ≠ Windows) → sha256(zip) trong idempotency_key lệch 2 golden ingest_zip_dryrun_*; đổi _golden_ensure_fixtures sang ZIP_STORED (bytes chỉ phụ thuộc nội dung+metadata — máy-độc-lập thật) + regen 2 golden. Runtime-identical, KHÔNG deploy riêng — ship cùng v1.34.0. // 1.33.59: Pha G (drift-test + siết gate, theo 9 quyết định grilling 2026-07-09): (a) SIẾT-6 contract THẬT (nlm_add/recat/source_rename/source_delete/reg_delete/dedup_plan — journal/resume/readback/rollback đầy đủ) + _CONTRACT_REQUIRED fail-strict; 6 legacy còn lại advisory deadline trước v1.34.1 (r65 drift-lock đúng-set); (b) `tl bundle-export` (ADR-0001): zip giữ VERSION fork-point + BUNDLE_META.json TRONG zip; drive-push guard BLOCKED_BY_BUNDLE_META rc=3 (+--force); card bundle_export + registry meta + GENERATED spec; (c) golden nâng cấp: raw-stability (stdout thô ×2 trùng byte — nợ P4-06 đóng theo phương án canonical+raw), {FIXTURES} token, +6 case offline-thuần trên fixtures cố định (chunk profile/vbqppl-blocked, ocr-analyze, zip slip/dup NEGATIVE rc=2, live-diff no-changes), harness chấp nhận JSON dict bất kể rc (case negative có chủ đích); (d) CI GitHub Actions ubuntu+windows full-gate (autocrlf off — hash parity), .github excluded khỏi manifest/zip; .gitattributes khoá byte golden dir; BUNDLE_META vào .gitignore + EXCLUDE_NAMES. // 1.33.58: Pha E kế hoạch — tl_core/command_registry.py: metadata 52 lệnh (risk/read_only/write_scope/confirm/dry-run/det-json/workflow_task/idempotency_contract/card_required; legacy write GRANDFATHER card_required=False, advisory riêng không fail strict); E2 incremental: 8 lệnh determinism SINH parser từ GENERATED_SPECS (flags/help nguyên văn, handler qua stub tl); E3 tool-inventory đọc registry_summary; E4 workflow-audit validate_registry (cmd↔parser↔card↔contract + JSON-through-gate scan source); luật gate: ghi NGOÀI-repo phải có contract/confirm/dry-run/builtin_gate (nlm-add=dedup-live, drive-push=md5-verify), ghi local miễn. +3 r64. // 1.33.57: Pha D kế hoạch — tách tl_core/{zip_ingest,ocr,chunking}.py (~790 dòng rời tl.py; cùng máy Pha C: AST-span + bind + 21 stub; _run_child_tl/_read_local_text_for_analysis/_text_quality_metrics ở lại tl vì dùng chung ≥2 module — D4 idempotency: contracts đã ở workflow.py từ Pha C, builders đi theo lệnh sở hữu, KHÔNG tạo module riêng tránh churn); canary + tl_boot preload + py_compile + REQUIRED_FILES phủ 3 module mới. // 1.33.56: Pha C kế hoạch nợ-kỹ-thuật — tách tl_core/{workflow,release,live}.py (~1.5k dòng rời tl.py: tool-inventory/route-task/cards/golden · determinism-audit/release-manifest+verify+bundle+check · live-readiness/contract/snapshot/diff/deploy/rollback/final-acceptance/go-live). Cơ chế: cắt NGUYÊN VĂN theo AST-span + bind(tl) copy-globals (bỏ tên đã có — def riêng module thắng) + 28 stub ủy quyền trong tl (tham chiếu chéo giữa module đi qua stub tl); helper chỉ-moved-code-dùng tự móc theo module (quy tắc an toàn referenced-only-by-one-module); public CLI KHÔNG đổi. +wiring reports/determinism_report.json khi strict-fail (tên đã EXCLUDE sẵn từ bundle 50-53 mà chưa ai ghi — 2 lần flake ok:false không giữ được diff); py_compile + REQUIRED_FILES phủ 3 module mới. // 1.33.55: MERGE bundle Pha B core-json-determinism (nhánh kia TỰ ĐÁNH "1.33.54" — TRÙNG SỐ KHÁC NỘI DUNG với canonical 1.33.54, fork từ 1.33.53 nên THIẾU 4 fix merge): tách tl_core/{deterministic,jsonio}.py, tl.py giữ wrapper mỏng tương thích ngược (public CLI không đổi); PORT LẠI fix #4 vào tl_core.jsonio (schema lạ → fallback JSON — bundle mang bug cũ trở lại); +r60 parity test wrapper↔tl_core; release-check py_compile + REQUIRED_FILES phủ tl_core. // 1.33.54: MERGE bundle determinism-hardening v1.33.50-53 (fork từ 78d6bfe, +tool-inventory/route-task/workflow cards+golden/ingest-zip/ocr-run+verify/chunk/convert-verify/live-readiness+contract+snapshot/diff/release-manifest+check/determinism-audit; đánh giá: repeat-run byte-identical, release zip date_time cố định, manifest reproducible cross-platform hash khớp, zip-slip + duplicate-normalized guard, volatile scrub namespace; giữ bất biến KHÔNG tách canonical VBQPPL — chunk chỉ ref/corpus=false/goc=canonical) + 2 fix khi gộp: route-task nhận CẢ positional (bundle bắt buộc --task → gãy cách gọi cũ, drift doc↔CLI lớp S8/A1) + r59 selftest khoá PURE helpers determinism (bundle thêm ~3300 dòng mà 0 test trong gate --selftest của upload script — audit riêng không chạy tự động). // 1.33.53: deterministic hardening (volatile scrub, release artifact exclusions, zip order/duplicate guard, readiness deployment_allowed). // 1.33.52: OCR manifest determinism + idempotency contract + release hardening (Pha 8-10). // 1.33.51: live-readiness 3-tier + live-contract-check + live-state-snapshot/diff (Pha 6-7). // 1.33.50: deterministic mode + volatile JSON scrub + workflow_card.v1 schema + determinism-audit/golden-test + release-check --strict-determinism. // 1.33.49: status --amendment registry guard + backfill-hieuluc + auth script hardening. // 1.33.48: rà Instruction Project 'Luật BHXH' (profile văn bản thường tên CÓ DẤU + KHOẢNG TRẮNG) → 3 fix + 1 QoL: (P1) _apply_profile_env HẾT rơi-âm-thầm-về-nền — profile yêu cầu tường minh KHÔNG có trong config.profiles → scope RỖNG + cảnh báo PROFILE_NOT_FOUND loud (trước: prof=fallback vbqppl → TL_REGISTRY_DOC_ID/TL_NOTEBOOK_ID trỏ NỀN trong khi TL_PROFILE=tên dự án → ghi/push NHẦM corpus VBQPPL, guard NO_NOTEBOOK_ID không bắt được vì env đã bị điền); (P2) _profile_lookup chịu-lỗi-gõ: khớp không-dấu/hoa-thường/space-_- khi DUY NHẤT 1 ứng viên ('luat_bhxh'→'Luật BHXH', TL_PROFILE set tên CANONICAL để cache-dir/scope nhất quán), ≥2 ứng viên mờ → không đoán; (P3) --profile/--config nhận Ở CẢ SAU subcommand cho MỌI lệnh (Instruction dặn 'mọi lệnh truyền --profile' nhưng flag chỉ ở root → `tl reg-query --profile X` gãy rc=2; default=SUPPRESS né bẫy namespace-con copy-đè của Python mới — root-position vẫn sống); (Q) counts +registry_claim_target_nb (nlm_notebook_id==đích + live-status, đúng luật Instruction 'không đếm mọi nlm_status') + registry_claim_by_notebook breakdown — registry_claim_nlm gộp mọi shard vô dụng cho slot per-notebook. +4 r57 (620/620). // 1.33.47: MERGE bundle-45 (`tra-luat_v1.33.45.zip`, nhánh song song fork từ v1.33.43, tự đánh 44/45) + ĐỐI CHIẾU fix v1.33.46 nhánh kia (đã publish Drive) + gói vá S5/S6 rời. (1) PORT bundle-45a: _qt5_search_hints subject ưu tiên title_vn/trich_yeu CÓ DẤU (+TINH CHỈNH guard _looks_like_filename_title — bài học P0-1 v1.31.0 bundle thiếu); 45b: backfill-title-vn --out atomic qua _emit_json_payload; 45c: _nlm_auth_alive retry ×3 backoff chống AUTH_EXPIRED oan do transient (+TINH CHỈNH GIỮ M1: auth_hint BỀN sau 3 lần → RED — bundle xếp clientauthentication vào transient-final → cookie chết thật thành INCONCLUSIVE vĩnh viễn = tái false-green). (2) REIMPLEMENT fix 46: bare-VBHN matcher 1 CHIỀU `_vbhn_bare_key`+`_sohieu_query_hits_entry` — web/footnote ghi số VBHN KHÔNG năm ('88/VBHN-VPQH') vs corpus year-qualified ('88-2025-VBHN-VPQH') → exact/substring miss (năm chèn giữa) = false-negative HỆ THỐNG 'VBHN đã có mà lần nào cũng báo thiếu' (ca thật 88 Quảng cáo); query có năm giữ CHẶT (collision 50-2025≠50-2026), chiều ngược không nới; áp 6 site: reg-query, source-map direct, locate, inline/footnote in_corpus, _classify_ref+frontier. (3) Gói vá S5/S6 rời = ĐÃ PHỦ bởi v1.33.44 canonical (S5 superset _normalize_loai mọi đầu vào; S6 tương đương _cat_reg_label). +6 r56 (616/616). // 1.33.44: vá lô 8 vấn đề vận hành skill từ log Cowork 7A (S4-S14): ingest-local ghi registry SẠCH ngay tại ingest (S5 loai enum chuẩn qua _normalize_loai, S6 reg_cat NHÃN ĐỦ qua _cat_reg_label, S4 bước link cuối kèm corpus=true — hết chuỗi vá backfill-loai/recat/register sau mỗi ingest); S7 `tl journal <run> --close` SELF-HEAL inflight đã được lệnh khác hoàn tất (đối chiếu intent.set↔registry, --force ép); S8 nlm-add alias --drive/--wait (drift doc↔CLI); S11 corpus-audit Cowork 45s: gợi ý + resume_command giữ `--limit` trang nhỏ (15/lệnh); S12 sweep name_nonstandard headline = VBQPPL thật (trừ loai='thuong'+quarantine → *_other, hết 65-vs-8 phồng ảo); S13 doc source-rename 1 file/lệnh Cowork; S14 gợi ý tên source-rename: chủ đề từ title_vn (bỏ từ-loại đầu, ≤10 từ) + số hiệu gạch-nối đủ + cảnh báo SOHIEU_MISSING. +5 r55 (611/611). // 1.32.2: (log rà 69 Luật — CHẠY TRÊN v1.32.x LIVE, xác nhận gate A1/A2 hoạt động: 90-2025 OK+SUPPRESSED_CONFIRMED, 115-2026 OK+CONSOLIDATED). 4 vá: S1 `tl ping` retry ×3 backoff 2s/5s CHỈ lỗi dạng COLD-START Apps Script (404/timeout 2-3 lần gọi đầu — từng kết luận sai 'webapp chết'). S3 backfill-loai --normalize +mode CONFLICT: loai hợp-lệ-enum nhưng mâu thuẫn 2 bằng chứng đồng thuận (tên VBHN_ + sohieu -VBHN-) → đề xuất 'Văn bản hợp nhất' (ca 115-2026-VBHN mang loai='Luật' lọt danh sách Luật; chỉ ca VBHN — prefix khác nhiều ngoại lệ). S5 `_is_omnibus_entry` +nhánh ĐỀ-TÀI-TRONG-TÊN so DẠNG NÉN ('SuaDoi_QuyHoach_DauTu' strip xong dính liền — 'dau tu' có-space không khớp; ca 57-2024 registry chưa backfill goc → nhánh ≥2-ref câm, vẫn REVIEW lặp). S4 tl_fetch.sh `--setup-step core|gws|boot|nlm` (Cowork 45s/lệnh giết --setup trọn gói; bước nlm lặp cùng lệnh tới hết PARTIAL). selftest 469/469 (+3 r12). // 1.32.1: canary cred + fast-fail + NLM-read fallback. // 1.32.0: amendment-gate A1/A2/A3. (log rà 119 Luật — read-path CHẾT TOÀN BỘ mà health-check FALSE-GREEN). P1a `_gws_cred_alive` CANARY đổi token THẬT (auth_method=oauth2 KHÔNG chứng minh cred sống — ca revoke): gws-ping + doctor nay ĐỎ + remediation khi invalid_grant (doctor --offline skip canary, ghi rõ). P1b corpus-audit + backfill-title-vn FAST-FAIL (≥3 lỗi đọc liên tiếp → ABORT READ_BACKEND_DOWN thay vì cày 531×22s all-error) + `_read_doc_text_via_nlm` đường đọc DỰ PHÒNG qua nlm-content (295 nguồn live; text đã-nạp vẫn verbatim — đủ cho header/audit). P0-msg sửa khẳng định SAI 'fallback GAS vẫn đúng': GAS chỉ cứu DOWNLOAD file; exporttext (đọc text) chết theo vì webapp thiếu scope script.external_request. selftest 467/467 (+1 r12). // 1.32.0: amendment-gate A1/A2/A3 + enum điều ước + sidecar noise. (log rà 77 Luật — 3 defect lớp AMENDMENT-GATE trong _source_map_one + enum + noise). A1 canonical CONFIRMED → suppress TOÀN BỘ escalation gate (UNLINKED/VBHN_RECHECK/PAUSE/LOW_CONF; cờ AMENDMENT_GATE_SUPPRESSED_CONFIRMED; action_required nhất quán — ca 90-2025 verified vẫn bị RECHECK). A2 canonical CHÍNH LÀ VBHN: refilter ứng viên thuộc chuỗi goc CỦA CHÍNH NÓ → consolidated (khối cũ chỉ gom goc related_vbhn — rỗng khi query thẳng số VBHN, ca 115-2026 bị đòi 'tìm VBHN cho VBHN'); còn lại → VBHN_GOC_VERIFY thay VBHN_RECHECK. A3 canonical OMNIBUS (_is_omnibus_entry: cat46/sua-doi-N-luat/sửa-đổi+≥2ref) → OMNIBUS_AMENDS_OTHER, bỏ UNLINKED/LOW_CONF (hết REVIEW lặp 4 luật omnibus). A4 _LOAI_CANON +'Điều ước quốc tế'/'Công ước' (hết 56 nonmappable giả công ước ILO). B3 RAW_NAME_NOT_NLM suppress khỏi risky khi là SIDECAR cạnh GDoc (_is_source_sidecar). selftest 466/466 (+7 r11_*). // 1.31.2: U1 _sanitize_export_text (byte hỏng vỡ capture driver) + U2 _title_block_from_text tier-1 trích yếu khối tiêu đề + GWS_CRED_EXPIRED tự-chẩn-đoán + _hush selftest noise. (log LIVE vòng 3 — 2 fix gốc, tham khảo script user đã thẩm định). **U1 sanitize export-text:** driver bash vỡ capture vì byte không hợp UTF-8 trong output extract → _sanitize_export_text (diệt lone-surrogate round-trip encode-replace + bỏ control-char, giữ newline/tab) bọc MỌI nhánh _read_doc_text + cmd_extract trước khi ghi đĩa/in (stdout reconfigure sẵn có KHÔNG cứu được file --out + text chui vào JSON driver). **U2 nguồn trích yếu = KHỐI TIÊU ĐỀ:** log chứng minh --dieu 1 trả nhầm khoản phạm-vi; _title_block_from_text bóc dòng LOẠI IN HOA đứng riêng (BỘ LUẬT ưu tiên trước LUẬT — script gốc match ngược làm 91/2015 thành Luật Dân sự SAI LOẠI) + gom ĐỦ các dòng chủ đề in hoa (script gốc cap 4 dòng → cụt HIV/AIDS, quy phạm pháp) + _title_sentence_case giữ token số/ngoặc (script gốc .lower() trần); làm TIER-1 trong _title_vn_from_header (tier-2 _doc_subject_for_name giữ nguyên fallback). KHÔNG import sidecar 34 mục của phiên kia (6+ mục cụt/sai lộ ngay trong file — backfill-title-vn tự re-derive từ nguồn, registry title_vn vẫn là nguồn duy nhất). selftest 458/458 (+7 r10_*).
GWS_PINNED_VERSION = "0.22.5"   # @googleworkspace/cli; npm i -g @googleworkspace/cli@0.22.5
# Bootstrap gws cho Cowork (sandbox chặn github + no root): binary MUSL STATIC (chạy mọi glibc, kể cả
# Ubuntu 22.04/glibc 2.35 — bản gnu cần GLIBC_2.39 nên KHÔNG chạy). Stage sẵn trên Drive _HOP_NAP.
# Re-stage bản mới → cập nhật 2 hằng này (id + md5).
GWS_COWORK_FILEID = "1z2cxBifvYdQhhGfWuapFW9zrS4ki4bRF"   # x86_64-unknown-linux-musl v0.22.5
GWS_COWORK_MD5 = "deab5ebf45cd492b56ac563e6c471c99"
# Python 3.11 STANDALONE relocatable (python-build-standalone) trên Drive — cho Cowork CHẶN egress astral CDN
# (uv không tải managed Python được). `tl nlm-install` tải từ Drive (egress mở) → giải nén ~/.local/python311
# → cài notebooklm-mcp-cli. cpython-3.11.15 x86_64-linux-gnu install_only_stripped (~31MB).
PY311_FILEID = "15JsTAuM0iLkza758cTN2Qv-H3NCAcjMi"
PY311_MD5 = "9c4168a6da7824e81836be9abb7d55c3"
# gws credential ĐÃ MÃ HOÁ (khoá = webapp token, dẫn xuất PBKDF2) trên Drive _HOP_NAP — KHÔNG plaintext,
# KHÔNG trong zip. `gws-auth-load` (và bootstrap) tự tải+giải mã → ~/.config/gws/credentials.json (zero-setup).
# v1.33.1: `gws-auth-stage` (và `secrets-set --gws` đồng-bộ-public) nay GHI ĐÈ TẠI CHỖ fileId này —
# KHÔNG cần cập nhật hằng sau mỗi lần token rụng; chỉ đổi khi chủ đích tạo file mới bằng `--new`.
GWS_CRED_FILEID = "1Wb_-7FhH_SOzS9Nr0bEhgmurT565LG8e"
# nlm cookie ĐÃ MÃ HOÁ (khoá = webapp token, PBKDF2) trên Drive — cho Cowork nạp nlm HEADLESS (KHÔNG cần master key/
# `nlm login`). `nlm-auth-load` tải+giải mã → ~/.notebooklm-mcp-cli. Stage 1 lần ở Code (sau `nlm login`):
# `tl nlm-auth-stage` → in fileId → điền vào đây (hoặc env TL_NLM_CRED_FILEID). Cookie hết hạn (~2–4 tuần):
# v1.33.1 re-stage (hoặc `secrets-set --nlm`) GHI ĐÈ TẠI CHỖ — fileId GIỮ NGUYÊN, không cần điền lại (trừ --new).
NLM_CRED_FILEID = "156StZcgqk-TYNRGCX76HrvueRgoV2Rpq"
# fileId ZIP/BUNDLE skill trên Drive (public anyone-with-link) — tl_fetch.sh curl về; `drive-push <zip>` cập nhật NỘI DUNG
# file này (GIỮ fileId) mỗi lần ship (qua gws, máy đã auth). Đồng bộ với TL_SKILL_FILEID trong tl_fetch.sh.
SKILL_FILEID = "1H5kAt3SRVP7_xmLMIzcqyFtFc4VSDH0P"
# Config v2 (PLAINTEXT token) trên Drive/Package — nay PUBLIC (anyone-with-link). Phiên TRỐNG (không token/env):
# `tl init-config --from-public` curl `drive.usercontent` (KHÔNG cần Drive MCP/token); fallback Drive MCP `--file`
# hoặc (đã có gws cred) `--from-drive`. SEED cho đường GAS-only (không cần master key). Re-stage đổi config → cập nhật id.
CONFIG_FILEID = "1dEOBJ8PRmKoLgziEF5xuKjRhHLNhUUYq"
CONFIG_PUBLIC = True   # config + creds (gws/nlm/secrets/binary/py311) ở Package anyone-with-link → curl-able, off Drive MCP
# Bundle secrets THỐNG NHẤT (mã hoá bằng TL_MASTER_KEY): {webappUrl, token GAS, gws_cred}. KHÔNG plaintext,
# KHÔNG trong zip. `tl bootstrap` giải mã → nạp GAS (+gws ở Code/Cowork). `tl secrets-stage/-set` tạo/xoay vòng.
SECRETS_FILEID = "1V0rSVFg7tcbXN12aicp_wonZ2UJ5Pq6V"  # tl_secrets.enc trên Drive (chỉ là fileId — vô dụng nếu
# thiếu TL_MASTER_KEY). Bootstrap THIẾU --secrets-file → tự tải bằng id này (webapp GAS nếu có token / direct-media
# nếu có gws cred). Re-stage đổi id thì cập nhật ở đây (hoặc dùng --secrets-id / env TL_SECRETS_FILEID).
DEFAULT_PROFILE = "vbqppl"
VBQPPL_CONFIG_DRIVE_ID = "1_-rK3Vv1nCfF1a44JL0kLUXwSks7YOSP"
# v1.18: notebook NỀN (VBQPPL). Dòng registry rỗng nlm_notebook_id (legacy đẩy lên VBQPPL trước khi có
# cột) được quy về notebook nền này khi đếm slot — khớp logic baseNotebookId trong Code.2.21.2i.gs.
NLM_BASE_NOTEBOOK = "743ed200-2e55-4673-b7a0-9bfd13b41ce6"
# SỰ CỐ 2026-06-30 (root-cause): registry base THẬT = Google SHEET `tra_luat_registry` (webapp regSS_ auto-discover).
# Doc dưới đây (vnd.google-apps.document) là LEGACY chỉ dùng ping/display — config trỏ registryDocId vào nó → webapp
# mở Doc-as-Sheet → đọc RỖNG (count=0 ẢO, KHÔNG mất data). Template public hay ghi đè về đây qua init-config →
# doctor/init-config CHẶN giá trị này (để rỗng → webapp auto-discover Sheet thật).
_LEGACY_REGISTRY_DOC_ID = "1mATGFhaW0e_CYienAD80DsTS1K4zfJNlTAx-DsHaCD8"

# Large-file split (log rà, yêu cầu user): nguồn QUÁ LỚN nạp NGUYÊN vào 1 source NLM → chất lượng RAG GIẢM
# (NLM tổng hợp tốt nhất ~≤100k ký tự/nguồn; webapp exporttext CAP ~200k). Ngưỡng MỀM theo BYTE file nguồn
# (.docx/.pdf phình hơn text nhưng > ngưỡng này gần như chắc chắn vượt giới hạn chất lượng) → ingest HỎI tách.
NLM_LARGE_SRC_BYTES = 1_200_000        # ~1.2MB file nguồn → cảnh báo/hỏi tách (chỉnh bằng --large-threshold)

REGISTRY_SCHEMA_COLS = [
    "drive_id", "src_id", "sohieu", "loai", "name", "cat", "mime", "md5",
    "size", "modified_time", "linhvuc", "goc", "nlm_source_id", "nlm_status",
    "nlm_pushed_at", "verified", "registered_at", "note", "title_vn",
    "linhvuc_list", "hieuluc", "sua_doi", "nlm_title", "corpus",
    "nlm_notebook_id", "tukhoa", "row_kind",
]
REGISTRY_SHEET_MIME = "application/vnd.google-apps.spreadsheet"
DRAFT_WARNING = "DỰ THẢO — chưa hiệu lực"


def _base_also_enabled(a=None) -> bool:
    """A (v1.30.0): chế độ 'profile CỘNG VBQPPL' cho lệnh ĐỌC. Ưu tiên: cờ lệnh --base-also/--no-base-also >
    env TL_BASE_ALSO (do _apply_profile_env set theo config.profiles.<p>.baseAlso) > TẮT ở profile nền vbqppl."""
    v = getattr(a, "base_also", None) if a is not None else None
    if v is not None:
        return bool(v)
    if _active_profile() == DEFAULT_PROFILE:
        return False
    return (os.environ.get("TL_BASE_ALSO") or "").strip().lower() in ("1", "true", "yes", "on")


def _vbqppl_notebooks(cfg: dict) -> list[str]:
    """A (v1.30.0, PURE): danh sách notebook NỀN VBQPPL từ config — base + overflow + shards (dedup, giữ thứ tự
    base→overflow→shards). Dùng mở rộng đích nlm-cross khi TL_BASE_ALSO."""
    prof = _profiles_from_config(cfg or {}).get(DEFAULT_PROFILE) or {}
    shards = prof.get("shards") if isinstance(prof.get("shards"), list) else []
    out, seen = [], set()
    for x in [prof.get("notebookId") or NLM_BASE_NOTEBOOK, prof.get("overflowNotebookId"), *shards]:
        x = str(x or "").strip()
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out


def _add_base_also_flags(p) -> None:
    """A (v1.30.0): cặp cờ override chế độ 'profile CỘNG VBQPPL' cho lệnh ĐỌC (default None = theo TL_BASE_ALSO)."""
    p.add_argument("--base-also", dest="base_also", action="store_true", default=None,
                   help="quét THÊM nền VBQPPL+shards (mặc định BẬT ở profile dự án — v1.30.0)")
    p.add_argument("--no-base-also", dest="base_also", action="store_false",
                   help="CHỈ quét scope profile đang chọn")


def _cache_file(name: str) -> Path:
    return _profile_cache_dir() / name


def _invalidate_manifest_cache() -> None:
    """(MERGE) Sau khi GHI registry (rename/delete/corpus-toggle) → xoá cache manifest LOCAL để lần đọc sau lấy LIVE
    (khỏi đọc cache CŨ nlm rỗng/tên cũ). Lần boot/reg-query kế tự nạp lại."""
    for _n in ("manifest.json", "manifest_index.json"):
        try:
            _p = _cache_file(_n)
            if _p.exists():
                _p.unlink()
        except Exception:
            pass


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════
# PHA 0 — NỀN TẢNG CHECKPOINT/AN TOÀN (yêu cầu user: hệ thống checkpoint chống hỏng-dữ-liệu khi chạy dài).
# Ba primitive PURE (test offline), CHƯA đổi hành vi lệnh nào: (1) WAL Journal (nhật ký ghi-trước, resume/undo);
# (2) verified reg-write (đối chiếu patched==expected + validate cột schema → chống 'ghi mù' im lặng); (3) preflight
# invariant gate (gom guard rải rác → chặn clobber/mispoint/cột-sai TRƯỚC khi ghi). Bọc vào lệnh ở Pha 1.
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════

def _journal_dir() -> Path:
    # MERGE Codex v1.33.10→v1.33.11: env-override — selftest/sandbox + môi trường cache tách profile không
    # mất dấu journal (TL_JOURNAL_DIR > TL_CACHE_DIR/_journal > ~/.tl_journal như cũ).
    explicit = os.environ.get("TL_JOURNAL_DIR")
    if explicit:
        return Path(os.path.expanduser(explicit))
    cache_root = os.environ.get("TL_CACHE_DIR")
    if cache_root:
        return Path(os.path.expanduser(cache_root)) / "_journal"
    return Path(os.path.expanduser("~")) / ".tl_journal"


def _journal_path(run_id: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", str(run_id))[:120] or "run"
    return _journal_dir() / f"{safe}.jsonl"


def _journal_new_run_id(cmd: str) -> str:
    import time as _t
    safe = re.sub(r"[^A-Za-z0-9_-]", "", str(cmd))[:40] or "run"
    return f"{safe}_{int(_t.time())}_{os.getpid()}"


def _journal_append(run_id: str, rec: dict) -> None:
    """Ghi 1 dòng JSONL vào nhật ký (append-only). Best-effort — KHÔNG raise (nhật ký hỏng KHÔNG được làm hỏng lệnh)."""
    try:
        _journal_dir().mkdir(parents=True, exist_ok=True)
        with _journal_path(run_id).open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _journal_resume_state(records: list) -> dict:
    """PURE (test offline): từ các dòng nhật ký → trạng thái resume. `intent` ghi TRƯỚC call remote; `commit` (ok) ghi
    SAU khi verify. Op có intent NHƯNG chưa commit-ok = DỞ/không rõ (ngắt giữa chừng) → caller phải VERIFY remote rồi
    mới quyết retry/skip. done = op đã commit-ok (bỏ qua khi resume)."""
    meta, plan, intents, commits = {}, None, {}, {}
    for r in records or []:
        t = r.get("t")
        if t == "run_start":
            meta = r
        elif t == "plan":
            plan = r
        elif t == "intent" and r.get("key") is not None:
            intents.setdefault(r["key"], r)   # GIỮ intent ĐẦU TIÊN (retry ghi intent 2 lần → 'before' gốc ở bản đầu; undo cần bản gốc)
        elif t == "commit" and r.get("ok") and r.get("key") is not None:
            commits[r["key"]] = r
    inflight = [iv for k, iv in intents.items() if k not in commits]   # ghi intent nhưng chưa commit-ok
    return {"run_id": meta.get("run_id"), "cmd": meta.get("cmd"), "snapshot": meta.get("snapshot"),
            "plan": plan, "done": commits, "done_keys": sorted(commits.keys()),
            "inflight": inflight,
            "counts": {"intents": len(intents), "done": len(commits), "inflight": len(inflight)}}


# ── PHA 3: LOOP HỢP NHẤT — controller thuần (không bỏ bước, không né quy trình; hội tụ + fail-safe pause) ──

def _pipeline_step_decision(precond_ok: bool, action_ok: bool, verify_ok: bool) -> str:
    """PURE: quyết định 1 BƯỚC trong runner. precond sai → SKIP (KHÔNG âm thầm bỏ — ghi lý do). action ok + verify-readback
    ok → DONE (CHỈ 'done' khi verify PASS). action ok nhưng verify sai → PAUSE (ghi tưởng thành công nhưng hụt = fail-safe).
    action sai → PAUSE. → 'bước chỉ DONE khi verify đạt' ép không-bỏ-bước/không-né-quy-trình."""
    if not precond_ok:
        return "SKIP"
    if not action_ok:
        return "PAUSE"
    return "DONE" if verify_ok else "PAUSE"


def _corpus_safe_reversible(entries: list) -> dict:
    """Tập AN TOÀN ĐẢO-NGƯỢC cần set corpus=false: infra lẫn corpus (_sweep_report) + dup (dedup_plan ready). Dùng CHUNG
    `corpus-fix --tier safe` và `loop`. Trả {ids, infra, dedup} (giữ breakdown cho output corpus-fix)."""
    infra_ids = [r["drive_id"] for r in _sweep_report(entries)["infra_in_corpus_rows"] if r.get("drive_id")]
    dp = _dedup_plan(entries)
    dup_ids = [d["drive_id"] for it in dp["ready"] for d in it["quarantine"] if d.get("drive_id")]
    return {"ids": list(dict.fromkeys(infra_ids + dup_ids)), "infra": len(infra_ids), "dedup": len(dup_ids)}


def _reg_cols_valid(cols) -> tuple:
    """PURE: mọi cột định ghi PHẢI ∈ REGISTRY_SCHEMA_COLS. Bắt lỗi 'ghi mù' kinh điển: cột `so_hieu` (đúng là `sohieu`)
    → webapp BỎ IM LẶNG, patched=0 không báo (sự cố missing-sohieu 193 dòng). Trả (ok, cột_lạ)."""
    col_list = [c.strip() for c in cols.split(",")] if isinstance(cols, str) else list(cols or [])
    col_list = [c for c in col_list if c]
    if not col_list:
        return (False, ["<empty>"])   # cols RỖNG/None → webapp CHỈ vá `nlm_title` mặc định (ghi mù ngoài ý muốn) → CHẶN
    bad = [c for c in col_list if c not in REGISTRY_SCHEMA_COLS]
    return (len(bad) == 0, bad)


def _verify_reg_result(rb: dict, expected: int) -> dict:
    """PURE: đối chiếu kết quả reg_bulk. verified = `ok` VÀ KHÔNG có dòng `missed` (drive_id KHÔNG khớp = hụt THẬT).
    ⚠ **KHÔNG dùng patched làm cờ hụt**: reg_bulk `patched` = số dòng ĐỔI; ghi lại giá trị ĐÃ ĐÚNG → patched=0 nhưng
    dòng VẪN khớp (idempotent) → thành công, KHÔNG phải lỗi. (Sự cố báo động GIẢ 'REG_WRITE_FAIL' khi loop ghi lại giá
    trị đã đúng — log 2026-07-02.) Silent-write cột-sai đã bị `_reg_cols_valid` CHẶN TRƯỚC ghi nên không cần patched ở đây.
    Trả `missed_ids` (miss[] từ API) để commit per-row + `no_change` (patched<expected nhưng không miss = idempotent)."""
    rb = rb or {}
    patched = int(rb.get("patched") or 0)
    reg_ok = bool(rb.get("ok", True))
    miss_ids = rb.get("miss") if isinstance(rb.get("miss"), (list, tuple)) else None
    _missed_raw = rb.get("missed")
    if miss_ids is not None:
        missed = len(miss_ids)
    elif isinstance(_missed_raw, (list, tuple)):      # phòng webapp trả `missed` là LIST thay vì count (chống crash int([...]))
        missed = len(_missed_raw); miss_ids = _missed_raw
    else:
        missed = int(_missed_raw or 0) if isinstance(_missed_raw, (int, str)) else 0
    return {"verified": reg_ok and missed == 0, "patched": patched, "expected": int(expected), "reg_ok": reg_ok,
            "missed": missed, "missed_ids": [str(m) for m in (miss_ids or [])],
            "no_change": reg_ok and missed == 0 and patched < int(expected)}


def _verified_reg_write(g, items: list, cols) -> dict:
    """Bọc reg_bulk AN TOÀN (Pha 1 sẽ thay mọi g.post('reg_bulk',...) trực tiếp): (1) validate cột ∈ schema TRƯỚC ghi
    (chống cột lạ bị bỏ im lặng); (2) sau ghi đối chiếu patched==len(items). Trả verify dict. KHÔNG raise."""
    items = list(items or [])
    ok_cols, bad = _reg_cols_valid(cols)
    if not ok_cols:
        return {"verified": False, "error": "REG_COLS_NOT_IN_SCHEMA", "bad_cols": bad, "patched": 0, "expected": len(items),
                "note": f"Cột {bad} KHÔNG ∈ REGISTRY_SCHEMA_COLS → webapp BỎ IM LẶNG (vd 'so_hieu'≠'sohieu'). KHÔNG ghi."}
    try:
        rb = g.post("reg_bulk", items=items, cols=cols)
    except Exception as e:  # noqa: BLE001
        return {"verified": False, "error": f"REG_BULK_RAISED:{type(e).__name__}", "patched": 0, "expected": len(items)}
    v = _verify_reg_result(rb, len(items))
    v["reg_bulk"] = rb
    return v


# ── PHA 1: bọc lệnh MUTATE qua precheck + journal + verified-write (bắt đầu ĐỔI hành vi: chặn ghi mù/clobber, resume/undo) ──

def _manifest_cache_age_seconds() -> float | None:
    """Tuổi (giây) của cache manifest LOCAL theo mtime — quyết định có cần force-refresh không (giảm overhead 43s khi vừa refresh)."""
    try:
        import time as _t
        p = _cache_file("manifest.json")
        return (_t.time() - p.stat().st_mtime) if p.exists() else None
    except Exception:
        return None


def _apply_precheck(write_cols=None) -> dict:
    """Chạy preflight invariant TRƯỚC ghi (dùng state môi trường active). Trả {ok, blockers, warnings, checks}. Caller
    ABORT nếu not ok (trừ --force-unsafe). (apply_profile_offline phải chạy trước để TL_REGISTRY_DOC_ID đúng scope.)"""
    active = _active_profile()
    is_base = (active == DEFAULT_PROFILE)
    rid = (os.environ.get("TL_REGISTRY_DOC_ID") or "").strip()
    checks = _preflight_invariants({"registryDocId": rid, "is_base_profile": is_base,
                                    "profile_registry_id": rid, "snapshot_age_seconds": _manifest_cache_age_seconds(),
                                    "write_cols": write_cols})
    return {**_preflight_verdict(checks), "checks": checks, "profile": active}


def _apply_gate(a, write_cols=None, stream=True) -> tuple:
    """Cổng --apply THỐNG NHẤT: chạy precheck; blocker critical → (False, verdict) trừ khi --force-unsafe. Trả (ok, verdict)."""
    v = _apply_precheck(write_cols)
    if v["ok"] or getattr(a, "force_unsafe", False):
        if not v["ok"] and stream:
            print(f"[tl] ⚠ --force-unsafe: BỎ QUA blocker {v['blockers']} (RỦI RO — bạn tự chịu).", file=sys.stderr, flush=True)
        return True, v
    if stream:
        print(json.dumps({"ok": False, "aborted": True, "reason": "PRECHECK_BLOCKED", "blockers": v["blockers"],
                          "detail": [c for c in v["checks"] if not c["ok"] and c["severity"] == "critical"],
                          "note": "SỬA bất biến trên TRƯỚC khi --apply (vd registryDocId về Sheet thật; tạo registry profile). "
                                  "Hoặc --force-unsafe nếu CHẮC (rủi ro clobber/ghi-mù)."}, ensure_ascii=False, indent=2), file=sys.stderr)
    return False, v


def _apply_journal_start(cmd: str, meta: dict | None = None) -> str:
    rec = {"t": "run_start", "cmd": cmd}
    run_id = _journal_new_run_id(cmd)
    rec["run_id"] = run_id
    if isinstance(meta, dict):
        for k, val in meta.items():
            rec[k] = val
    _journal_append(run_id, rec)
    return run_id


def _journaled_reg_write(run_id: str, g, items: list, cols, key_field: str = "drive_id", before_by_key: dict | None = None) -> dict:
    """Ghi registry AN TOÀN + CÓ NHẬT KÝ: (1) journal `intent{before}` TRƯỚC (before=giá trị cũ để undo); (2) verified
    reg-write (validate cột + patched≥expected); (3) journal `commit{verify}` SAU. Trả verify dict (verified/patched/…).
    KHÔNG raise. Tổng quát hoá đường ghi cho MỌI lệnh mutate (Pha 1)."""
    items = list(items or [])
    keys = [str(it.get(key_field) or "") for it in items]
    _cols_list = [c.strip() for c in cols.split(",")] if isinstance(cols, str) else [str(c) for c in (cols or [])]
    for it, k in zip(items, keys):
        # LƯU `set` (giá trị định ghi) + `key_field` → Pha 2 resume LÀM LẠI được op dở; `before` → undo khôi phục.
        rec = {"t": "intent", "op": "reg_bulk", "key": k, "key_field": key_field, "cols": ",".join(_cols_list),
               "set": {c: it.get(c) for c in _cols_list if c in it}}
        if before_by_key and k in before_by_key:
            rec["before"] = before_by_key[k]
        _journal_append(run_id, rec)
    v = _verified_reg_write(g, items, cols)
    # commit PER-ROW dùng `missed_ids` (drive_id KHÔNG khớp = hụt THẬT). Dòng khớp (kể cả idempotent patched=0) = done →
    # KHÔNG còn báo động giả REG_WRITE_FAIL khi ghi lại giá trị đã đúng. bad-cols/error → tất cả not-committed.
    missed_set = set(v.get("missed_ids") or [])
    _reg_ok = bool(v.get("reg_ok", True)) and not v.get("error")
    for k in keys:
        row_ok = _reg_ok and k not in missed_set
        _journal_append(run_id, {"t": "commit", "op": "reg_bulk", "key": k, "ok": row_ok,
                                 "verify": {"patched": v.get("patched"), "expected": v.get("expected"), "missed": v.get("missed"), "error": v.get("error")}})
    # v1.29.2 (AUDIT B5 #1 — bust-cache-after-write THỐNG NHẤT): mọi lệnh mutate đi qua đây → xoá cache manifest LOCAL
    # 1 CHỖ (thay vì nhớ gọi rải rác từng lệnh — trước chỉ 3-4/16 lệnh gọi → đọc sau ghi dính stale). Unlink idempotent,
    # rẻ; lần đọc kế `_load_manifest_full` (không cache) gọi manifest_export → GAS regReadAll_(true) = dữ liệu TƯƠI
    # (né luôn cache đọc 600s server-side). KHÔNG bust khi items rỗng (không có ghi).
    if items:
        _invalidate_manifest_cache()
    return v


def _verified_reg_upsert(g, payload: dict) -> dict:
    """Bọc reg_upsert AN TOÀN (cho khóa immutable: sohieu/goc/name — reg_bulk bỏ IM LẶNG): (1) validate field ghi ∈ schema
    (chống cột lạ); (2) sau ghi verify = `ok` (upsert ĐƯỢC CHẤP NHẬN). ⚠ `updated=False` = giá trị ĐÃ ĐÚNG (idempotent)
    → THÀNH CÔNG, KHÔNG phải hụt (chống báo động giả như reg_bulk patched=0). `changed`=đã thực sự đổi (thông tin).
    Trả {verified, changed, reg_upsert}. KHÔNG raise."""
    fields = [k for k in (payload or {}).keys() if k not in ("drive_id", "confirm", "merge")]
    ok_cols, bad = _reg_cols_valid(fields)
    if not ok_cols:
        return {"verified": False, "error": "REG_COLS_NOT_IN_SCHEMA", "bad_cols": bad}
    try:
        r = g.get("reg_upsert", **payload)
    except Exception as e:  # noqa: BLE001
        return {"verified": False, "error": f"REG_UPSERT_RAISED:{type(e).__name__}"}
    changed = bool(r.get("updated") or r.get("upserted") or r.get("created"))
    ok = bool(r.get("ok"))
    # N3 (v1.33.41 — log rà VBHN-first: `register --goc … --title-vn …` xong dòng 62/2025 vẫn goc=null/
    # title_vn=null): verify cũ CHỈ kiểm `ok` = request ĐƯỢC NHẬN — cột bị webapp bỏ IM LẶNG vẫn 'verified'
    # (cùng lớp ảo giác 'updated:true' của ghi-giá-trị-rỗng). Nay READ-BACK field-level qua reg_get
    # (refresh=true — né cache đọc 600s): field ĐÃ SET mà đọc lại LỆCH → verified=False + fields_dropped LOUD.
    # Read-back lỗi mạng → không phủ nhận write (ok giữ) nhưng ghi readback=FAILED để người vận hành biết CHƯA
    # xác nhận field-level.
    dropped, readback = [], "OK"
    _did = str((payload or {}).get("drive_id") or "")
    if ok and fields and _did:
        try:
            rb = g.get("reg_get", drive_id=_did, refresh="true")
            _rows = (rb.get("rows") or []) if isinstance(rb, dict) else []
            if _rows:
                _row = _rows[0] or {}
                for k in fields:
                    want = str(payload.get(k) or "").strip()
                    got = str(_row.get(k) or "").strip()
                    if want and got != want:
                        dropped.append({"col": k, "want": want[:80], "got": got[:80]})
            else:
                readback = "NO_ROW"   # reg_get không trả row → KHÔNG kết luận (không phủ nhận write đã ok)
        except Exception as e:  # noqa: BLE001
            readback = f"FAILED:{type(e).__name__}"
    if dropped:
        return {"verified": False, "changed": changed, "reg_upsert": r, "error": "FIELDS_DROPPED_ON_WRITE",
                "fields_dropped": dropped,
                "note": "reg_upsert ok NHƯNG read-back thấy field LỆCH — webapp bỏ cột im lặng "
                        "(kiểm tên cột ∈ REG_COLS_ / GAS version; KHÔNG tin updated:true suông)."}
    return {"verified": ok, "changed": changed, "reg_upsert": r,
            **({"readback": readback} if readback != "OK" else {})}


def _journaled_reg_upsert(run_id: str, g, payload: dict, before: dict | None = None) -> dict:
    """Ghi reg_upsert CÓ NHẬT KÝ: intent{before} → verified upsert → commit{verify}. Trả verify dict."""
    did = str((payload or {}).get("drive_id") or "")
    _set = {k: payload[k] for k in (payload or {}) if k not in ("drive_id", "confirm", "merge")}
    rec = {"t": "intent", "op": "reg_upsert", "key": did, "key_field": "drive_id",
           "cols": ",".join(_set.keys()), "set": _set}
    if before:
        rec["before"] = before
    _journal_append(run_id, rec)
    v = _verified_reg_upsert(g, payload)
    _journal_append(run_id, {"t": "commit", "op": "reg_upsert", "key": did, "ok": bool(v.get("verified")),
                             "verify": {"error": v.get("error"), "changed": v.get("changed")}})
    _invalidate_manifest_cache()   # v1.29.2 (AUDIT B5 #1): bust-cache-after-write thống nhất (như _journaled_reg_write)
    return v


# Cột XÓA ĐƯỢC qua action `reg_clear` (khớp allowed-list doRegClear_ webapp). ⚠ GHI GIÁ TRỊ RỖNG qua reg_bulk/reg_upsert
# bị webapp BỎ QUA IM LẶNG ("empty string KHÔNG ghi đè") → muốn XÓA field PHẢI đi reg_clear — gốc 2 sự cố LIVE:
# shared-source-fix 'links_cleared:0' + register --nlm-source-id "" 'updated:true' mà không đổi.
_REG_CLEARABLE_COLS = {"nlm_source_id", "nlm_status", "nlm_pushed_at", "nlm_title", "nlm_notebook_id", "note"}


def _journaled_reg_clear(run_id: str, g, drive_id: str, cols, before: dict | None = None) -> dict:
    """v1.29.4: XÓA giá trị cột registry CÓ NHẬT KÝ qua action `reg_clear` (keyed drive_id + confirm=yes server-side).
    intent{op:reg_clear, before=giá trị cũ → UNDO khôi phục được qua `tl undo` (restore đi reg_bulk giá trị non-empty)}
    → gọi reg_clear → commit{ok = cleared≥1}. Validate cols ∈ _REG_CLEARABLE_COLS TRƯỚC. Trả {verified, cleared, resp}."""
    _cols_list = [c.strip() for c in cols.split(",")] if isinstance(cols, str) else [str(c) for c in (cols or [])]
    bad = [c for c in _cols_list if c not in _REG_CLEARABLE_COLS]
    if bad:
        return {"verified": False, "cleared": 0, "error": f"COLS_NOT_CLEARABLE:{','.join(bad)}"}
    rec = {"t": "intent", "op": "reg_clear", "key": str(drive_id), "key_field": "drive_id",
           "cols": ",".join(_cols_list), "set": {c: "" for c in _cols_list}}
    if before:
        rec["before"] = before
    _journal_append(run_id, rec)
    try:
        r = g.get("reg_clear", drive_id=drive_id, cols=",".join(_cols_list), confirm="yes")
    except Exception as e:  # noqa: BLE001
        r = {"ok": False, "error": f"REG_CLEAR_RAISED:{type(e).__name__}"}
    cleared = int(r.get("cleared") or 0) if isinstance(r, dict) else 0
    ok = bool(isinstance(r, dict) and r.get("ok") and cleared >= 1)
    _journal_append(run_id, {"t": "commit", "op": "reg_clear", "key": str(drive_id), "ok": ok,
                             "verify": {"cleared": cleared, "error": (r or {}).get("error")}})
    _invalidate_manifest_cache()
    return {"verified": ok, "cleared": cleared, "resp": r}


def _reg_before_from_manifest(items: list, cols_list, key_field: str = "drive_id") -> dict:
    """v1.29.2 (AUDIT B1 #2): before-snapshot BEST-EFFORT cho undo — đọc manifest cache LOCAL (có thể stale vài phút;
    chỉ phục vụ `tl undo` tham khảo, KHÔNG phải điều kiện ghi). Map key manifest: drive_id qua _entry_drive_id
    (manifest đổi drive_id→id), sohieu qua _entry_sohieu (manifest đổi sohieu→so_hieu). Lỗi/không cache → {} (im lặng)."""
    try:
        ents = _manifest_entries(refresh=False)
    except Exception:
        return {}
    if key_field == "drive_id":
        by = {_entry_drive_id(e): e for e in ents if _entry_drive_id(e)}
    else:
        by = {str(e.get(key_field) or ""): e for e in ents if e.get(key_field)}
    out = {}
    for it in (items or []):
        k = str((it or {}).get(key_field) or "")
        e = by.get(k)
        if not e:
            continue
        out[k] = {c: (_entry_sohieu(e) if c == "sohieu" else str(e.get(c) or "")) for c in (cols_list or [])}
    return out


def _ensure_writable_tmpdir() -> None:
    """5.5 (report rà corpus): Cowork /tmp = sticky-bit owner nobody → ghi /tmp = Permission denied (tempfile.* + script
    con vấp). Nếu TMPDIR/gettempdir KHÔNG ghi được → trỏ TMPDIR về cache dir ($HOME/.tra_luat_cache/tmp, luôn ghi được).
    tempfile.* và subprocess con (kế thừa os.environ) tự dùng dir này. Idempotent, im lặng nếu /tmp vốn ghi được."""
    import tempfile as _tf
    cur = os.environ.get("TMPDIR") or _tf.gettempdir()
    try:
        Path(cur).mkdir(parents=True, exist_ok=True)
        _probe = Path(cur) / ".tl_wtest"
        _probe.write_text("x", encoding="utf-8"); _probe.unlink()
        return                                      # /tmp ghi được → giữ nguyên
    except Exception:                               # noqa: BLE001
        pass
    try:
        alt = CACHE / "tmp"
        alt.mkdir(parents=True, exist_ok=True)
        os.environ["TMPDIR"] = str(alt)
        _tf.tempdir = str(alt)                      # reset cache nội bộ của tempfile
    except Exception:                               # noqa: BLE001
        pass


_ensure_writable_tmpdir()


class _BuiltinGas:
    """Client webapp TỐI GIẢN (stdlib) — dùng khi KHÔNG có gas.py của bộ skill đầy đủ
    (gói overlay chạy độc lập). Đọc TL_WEBAPP/TL_TOKEN từ env (load_creds đã đặt)."""

    def __init__(self):
        self.url = os.environ.get("TL_WEBAPP", "")
        self.token = os.environ.get("TL_TOKEN", "")
        if not self.url or not self.token:
            sys.exit("[tl] _BuiltinGas: thiếu TL_WEBAPP/TL_TOKEN (load_creds chưa chạy?)")

    def _call(self, action, params, method):
        import urllib.parse, urllib.request
        q = {"token": self.token, "action": action}
        for k, v in params.items():
            if v is not None:
                q[k] = v
        enc = urllib.parse.urlencode(q)
        if method == "GET":
            req = urllib.request.Request(self.url + "?" + enc)
        else:
            req = urllib.request.Request(self.url, data=enc.encode("utf-8"), method="POST")
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = resp.read().decode("utf-8", "replace")
        except Exception as e:
            return {"ok": False, "error": f"webapp {method} {action}: {type(e).__name__}: {e}"}
        try:
            return json.loads(body)
        except Exception:
            return {"ok": False, "error": "non-JSON response", "raw": body[:500]}

    def get(self, action, **params):
        return self._call(action, params, "GET")

    def post(self, action, **params):
        return self._call(action, params, "POST")


def _reassemble_parts(name: str) -> str | None:
    """ĐÃ BỎ cơ chế `_parts/` (chia nhỏ chống mount-cắt-cụt) — Cowork nay bootstrap qua `tl_fetch.sh` tải bản zip
    SẠCH từ Drive (không qua mount nên không cắt cụt) → `_parts` hết tác dụng, đã xoá khỏi skill. Hàm GIỮ chữ ký
    (luôn None) để mọi caller heal degrade an toàn về bản on-disk (strip-NUL nếu cần)."""
    return None


def _selfheal_module(name: str):
    """Mount Cowork NUL-pad/CẮT CỤT file .py → import lỗi. (1) đọc nguồn, BỎ NUL → compile (tự lành NUL-pad);
    (2) vẫn cắt cụt → GHÉP từ `_parts/<name>/` (mảnh nhỏ sống sót delivery). Hết cách → None."""
    import importlib.util
    src = next((d / f"{name}.py" for d in (HERE, HERE / "_fallback") if (d / f"{name}.py").exists()), None)
    code = None
    if src is not None:
        try:
            code = compile(src.read_bytes().replace(b"\x00", b"").decode("utf-8", "replace"), str(src), "exec")
        except SyntaxError:
            code = None
    if code is None:                                    # cắt cụt thật → thử ghép từ _parts
        asm = _reassemble_parts(name)
        if asm is None:
            return None
        try:
            code = compile(asm, str(src or (HERE / f"{name}.py")), "exec")
            sys.stderr.write(f"[tl] ⚠ {name}.py cắt cụt do mount — đã GHÉP lại từ _parts/ ({len(asm)}B).\n")
        except SyntaxError:
            return None
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(name, loader=None))
    mod.__file__ = str(src or (HERE / f"{name}.py")); sys.modules[name] = mod
    exec(code, mod.__dict__)   # noqa: S102 — nguồn skill của chính mình, đã strip NUL/ghép
    return mod


def _healed_script_path(name: str):
    """Đường dẫn 1 bản .py CHẠY-ĐƯỢC của script con chạy bằng SUBPROCESS (rasoat_worksheet/phuluc/orchestrate…).
    Bản gốc lành & sạch NUL → trả thẳng. Mount NUL-pad/CẮT CỤT → strip NUL hoặc GHÉP từ _parts/<name>/ ra file tạm
    (trong cache GHI-ĐƯỢC — né thư mục skill read-only) rồi trả file tạm. None nếu hết cách. (subprocess KHÔNG đi qua
    _imp self-heal nên cần lối làm-lành riêng này — vá log Cowork: rasoat_worksheet cắt cụt, không có lối cứu.)"""
    src = HERE / f"{name}.py"
    raw = src.read_bytes() if src.exists() else None
    asm = _reassemble_parts(name)                  # nguồn CHÂN LÝ nếu có _parts (đã verify==gốc lúc đóng gói)
    # bản gốc lành & sạch NUL & (nếu có parts) KHỚP parts → chạy thẳng, khỏi tạo temp.
    if raw is not None and b"\x00" not in raw:
        text = raw.decode("utf-8", "replace")
        try:
            compile(text, str(src), "exec")
            if asm is None or text == asm:
                return str(src)
            # compiles NHƯNG khác _parts → nghi CẮT CỤT-mà-vẫn-compile (mất hàm/đuôi) → ưu tiên _parts.
        except SyntaxError:
            pass
    candidates = []
    if asm is not None:
        candidates.append(asm)                                                    # ưu tiên _parts (đã verify)
    if raw is not None:
        candidates.append(raw.replace(b"\x00", b"").decode("utf-8", "replace"))   # NUL-pad fallback
    for code_src in candidates:
        try:
            compile(code_src, str(src), "exec")
        except SyntaxError:
            continue
        tmp = _cache_file(f"_healed_{name}.py")
        tmp.parent.mkdir(parents=True, exist_ok=True)   # phiên trống: cache dir có thể chưa tồn tại
        tmp.write_text(code_src, encoding="utf-8")
        sys.stderr.write(f"[tl] ⚠ {name}.py hỏng/khác _parts do mount — chạy bản làm-lành ở {tmp}.\n")
        return str(tmp)
    return None


def _compiles(text) -> bool:
    if text is None:
        return False
    try:
        compile(text, "<integrity>", "exec"); return True
    except SyntaxError:
        return False


_INTEGRITY_BAD = ("TRUNCATED", "NUL", "MISSING")


def _imp(name: str):
    """Import module ƯU TIÊN scripts/ GỐC (bản nền thật) → rồi mới scripts/_fallback/ (bản tối thiểu).
    Nhờ vậy overlay tự chạy được khi đứng riêng MÀ không đè bản nền thật khi cài lên skill đầy đủ.
    NUL-pad do mount → tự strip+exec (_selfheal_module)."""
    import importlib
    sys.path.insert(0, str(HERE))                       # gốc: bản thật thắng
    fb = HERE / "_fallback"
    if fb.exists() and str(fb) not in sys.path:
        sys.path.append(str(fb))                         # _fallback: chỉ khi gốc không có
    try:
        return importlib.import_module(name)
    except (SyntaxError, ValueError):                    # NUL byte / source bẩn do mount → thử tự làm lành
        healed = _selfheal_module(name)
        if healed is not None:
            sys.stderr.write(f"[tl] ⚠ {name}.py có NUL/bẩn do mount — đã tự strip+nạp (self-heal).\n")
            return healed
        raise


def _scope_params() -> dict:
    """Forward request scope của profile. rootFolderId/categoriesMode chỉ được server dùng để chặn
    regen2 quét nhầm cây kế thừa; organize vẫn có thể fallback category VBQPPL."""
    if _active_profile() == DEFAULT_PROFILE:
        return {}
    out = {}
    reg = os.environ.get("TL_REGISTRY_DOC_ID", "").strip()
    man = os.environ.get("TL_MANIFEST_ID", "").strip()
    if reg:
        out["registryDocId"] = reg
    if man:
        out["manifestId"] = man
    root = os.environ.get("TL_ROOT_FOLDER_ID", "").strip()
    categories = os.environ.get("TL_CATEGORIES_MODE", "").strip()
    if root:
        out["rootFolderId"] = root
    if categories:
        out["categoriesMode"] = categories
    manifest_scope = os.environ.get("TL_MANIFEST_SCOPE", "").strip()
    if manifest_scope:
        out["manifestScope"] = manifest_scope
    out["profileName"] = _active_profile()
    return out


# v1.19.6: đo thời gian từng call webapp. Bật bằng global --timings hoặc env TL_TIMINGS=1.
# Apps Script /exec ~2–3s/round-trip dù server_ms tí xíu → biết được nút thắt I/O.
_TIMING_ON = bool(os.environ.get("TL_TIMINGS"))
_TIMING_LOG: list = []
_DETERMINISTIC_ON = str(os.environ.get("TL_DETERMINISTIC") or "").strip().lower() in {"1", "true", "yes", "on"}


def _record_timing(action: str, wall_ms: int, out) -> None:
    server = out.get("elapsed_ms") if isinstance(out, dict) else None
    client = out.get("_client_ms") if isinstance(out, dict) else None
    _TIMING_LOG.append({"action": action, "wall_ms": wall_ms, "server_ms": server, "client_ms": client})
    if _TIMING_ON:
        print(f"[timing] {action:18s} wall={wall_ms:5d}ms server={server}ms client={client}ms", file=sys.stderr)


class _ScopedGas:
    """Bọc gas.py/_BuiltinGas: tự chèn registryDocId/manifestId của profile vào get/post (không đè nếu
    call đã truyền tường minh) + đo thời gian. Mọi thuộc tính khác delegate sang client gốc."""

    def __init__(self, inner):
        self._inner = inner

    def _merge(self, params: dict) -> dict:
        for k, v in _scope_params().items():
            params.setdefault(k, v)
        return params

    def get(self, action, **params):
        t0 = time.time()
        out = self._inner.get(action, **self._merge(params))
        _record_timing(action, int((time.time() - t0) * 1000), out)
        return out

    def post(self, action, **params):
        t0 = time.time()
        out = self._inner.post(action, **self._merge(params))
        _record_timing(action, int((time.time() - t0) * 1000), out)
        return out

    def __getattr__(self, name):
        return getattr(self._inner, name)


def _need_base(modname: str):
    """Import module NỀN (preingest_gate/manifest_build/…); nếu thiếu → thoát với thông báo RÕ
    thay vì ModuleNotFoundError trần trụi (đây là gói overlay, cần script nền của bộ skill đầy đủ)."""
    try:
        return _imp(modname)
    except ModuleNotFoundError:
        sys.exit(f"[tl] Lệnh này cần script nền '{modname}.py' (không có ở scripts/ gốc lẫn _fallback/). "
                 f"Cài overlay LÊN bộ skill tra-luat đầy đủ. Lệnh chạy độc lập: "
                 f"ping/locate/source-map/status/boot/manifest/preingest/doctor. Xem `tl doctor`.")


# ───────────────────────── helpers thuần (test offline) ─────────────────────────
def norm_sohieu(s: str) -> str:
    """Chuẩn hóa số hiệu về khóa: 113/2025/QH15 → 113-2025-QH15 (Đ→D, HOA)."""
    if not s:
        return ""
    s = s.strip().upper().replace("Đ", "D")
    s = re.sub(r"[\/\s]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    # Manifest cũ có VBHN VPQH lưu thiếu đoạn "VBHN" (19-VPQH, 40-VPQH).
    # Với VPQH, số trần không đủ định danh; nội bộ luôn dùng NN-VBHN-VPQH.
    m = re.fullmatch(r"(\d{1,4})-VPQH", s)
    if m:
        return f"{m.group(1)}-VBHN-VPQH"
    return s


_VBHN_KEY_RE = re.compile(r"^\d{1,5}(?:-\d{1,5})?-VBHN-([A-Z0-9D]+)$")


def _vbhn_agency_from_key(key: str) -> str:
    m = _VBHN_KEY_RE.fullmatch(norm_sohieu(key or ""))
    return m.group(1) if m else ""


def _sohieu_query_hits_entry(shq_key: str, entry_key: str, substring: bool = False) -> bool:
    """(v1.33.47): khớp SỐ HIỆU truy vấn ↔ khóa entry, NỚI ĐÚNG 1 CHIỀU cho VBHN bare — query THIẾU năm
    ('88-VBHN-VPQH') khớp entry year-qualified CÙNG số+cơ-quan MỌI năm (trúng nhiều năm → trả CẢ, người rà tự
    chốt, không im lặng chọn bừa). Query CÓ NĂM giữ so CHẶT như cũ ('50-2025-VBHN-VPQH' ≠ '50-2026-…' — giữ phân
    biệt collision). Chiều ngược (entry thiếu năm) KHÔNG nới — đó là nợ vbhn-year-fix, có detector riêng.
    substring=True cho site vốn lọc substring (reg-query); mặc định exact (source-map/locate/in_corpus)."""
    q, ek = (shq_key or ""), (entry_key or "")
    if not q:
        return True
    if (q in ek) if substring else (q == ek):
        return True
    bq = _vbhn_bare_key(q)
    return bool(bq) and bq == q and _vbhn_bare_key(ek) == bq


_DIEU_HEAD = lambda n: re.compile(r"(?m)^\s*Điều\s+%d\b" % int(n))
_DIEU_ANY = re.compile(r"(?m)^\s*Điều\s+\d+\b")


def extract_dieu(text: str, n: int) -> str | None:
    """Trích NGUYÊN VĂN Điều n: từ 'Điều n' tới 'Điều <kế tiếp>' (chịu số nhảy cóc)."""
    m = _DIEU_HEAD(n).search(text or "")
    if not m:
        return None
    end = len(text)
    nxt = _DIEU_ANY.search(text, m.end())
    if nxt:
        end = nxt.start()
    return text[m.start():end].strip()


def _nlm_probe_summary(env=None) -> dict:
    """Canary NLM không mạng: tl dùng absolute path nội bộ, nhưng shell non-interactive có thể không thấy `nlm`."""
    import shutil as _sh
    try:
        nc = _imp("nlm_cli")
        tl_path = nc.nlm_exe() or ""
    except Exception:
        tl_path = ""
    shell_path = _sh.which("nlm") or ""
    try:
        st = _imp("tl_gws")._nlm_install_probe(nlm_path=tl_path or shell_path or None)
    except Exception as e:  # noqa: BLE001
        st = {"next_step": "unknown", "error": f"{type(e).__name__}: {e}", "nlm": tl_path or shell_path}
    return {"tl_nlm_path": tl_path, "shell_nlm_path": shell_path, "probe": st,
            "path_note": ("OK: shell cũng thấy nlm" if shell_path else
                          "shell non-interactive có thể chưa thấy nlm; dùng `tl nlm-*` hoặc export PATH=$HOME/.local/bin:$PATH")}


_IMMUTABLE_UPSERT_COLS = {"sohieu", "goc"}   # reg_bulk BỎ IM LẶNG khi ĐỔI các cột này → phải reg_upsert (keyed drive_id)


def _doctor_exporttext_probe_target(entries: list[dict]) -> dict | None:
    """MERGE Codex v1.33.10→v1.33.11: chọn một GDoc nhẹ để `doctor --deep` kiểm riêng GAS exporttext/scope.
    Không dùng file thô vì lỗi raw không nói gì về OAuth scope."""
    cands = [e for e in (entries or []) if _entry_google_doc(e) and _entry_corpus_true(e)]
    if not cands:
        cands = [e for e in (entries or []) if _entry_google_doc(e)]
    cands.sort(key=_entry_score, reverse=True)
    return cands[0] if cands else None


def _looks_like_sohieu_query(q: str) -> bool:
    return bool(re.search(r"\d{1,4}\s*[-/_]\s*(?:\d{4}|VBHN|VPQH|LCT\s*[-/_]\s*HDNN\d*)", q or "", re.I))


def _sohieu_year(s: str) -> int | None:
    m = re.search(r"(?:[-/_]|^)(20\d{2}|19\d{2})(?:[-/_]|$)", s or "")
    return int(m.group(1)) if m else None


def _sohieu_base_sort_year(s: str) -> int:
    """Sort-key cho goc-chain VBHN: LCT-HDNN là luật trước 1992 nhưng số hiệu không chứa năm."""
    y = _sohieu_year(s)
    if y is not None:
        return y
    return 1987 if re.search(r"(?:^|[-/_])LCT[-/_]HDNN\d+\b", s or "", re.I) else 9999


def _qt5_search_hints(q: str, hits: list[dict]) -> list[str]:
    """Gợi ý QT-5 2-LƯỢT (S9): 'hợp nhất' (lượt 1) + 'mới nhất <năm>'/Công báo (lượt 2 BẮT BUỘC — chống chốt VBHN lỗi thời)."""
    import datetime as _dt
    cur_year = _dt.date.today().year
    hints = []
    for e in hits[:3]:
        # MERGE bundle-45a (v1.33.47 — log phiên rà 34 Luật của nhánh kia): subject ưu tiên title_vn/trich_yeu
        # CÓ DẤU (registry đã backfill ~88%) — tail tên file ASCII ('cong chung'/'cntt') làm recall Google lượt-2
        # yếu. TINH CHỈNH so bundle: +guard _looks_like_filename_title (title_vn nhiều dòng = chính TÊN FILE —
        # bài học P0-1 v1.31.0, query literal filename tìm ra 0; bundle thiếu guard này).
        subj = str(e.get("title_vn") or e.get("trich_yeu") or "").strip()
        if subj and _looks_like_filename_title(subj):
            subj = ""
        tail = subj if (subj and len(_token_set(subj)) >= 2) else _name_tail_key(_entry_name(e))
        if tail and len(_token_set(tail)) >= 2:
            hints.append(f'"{tail}" "hợp nhất"')
            hints.append(f'"{tail}" "hợp nhất" mới nhất {cur_year}')          # S9 lượt-2
    if q:
        hints.append(f'"{q}" "văn bản hợp nhất"')
        hints.append(f'"{q}" "hợp nhất" mới nhất {cur_year}')                 # S9 lượt-2
        hints.append(f'site:congbao.chinhphu.vn "{q}" "hợp nhất"')           # S9 official-first
    out = []
    for h in hints:
        if h not in out:
            out.append(h)
    return out[:8]


def _entry_goc(e: dict):
    return e.get("goc") or e.get("goc_luat") or e.get("targets") or e.get("target") or ""


def _goc_keys(e: dict) -> set[str]:
    raw = _entry_goc(e)
    parts: list[str] = []
    if isinstance(raw, (list, tuple, set)):
        parts = [str(x) for x in raw if x]
    elif isinstance(raw, dict):
        parts = [str(x) for x in raw.values() if x]
    else:
        parts = re.split(r"[;,|]+", str(raw or ""))
    keys = set()
    for part in parts:
        k = norm_sohieu(part.strip().replace("_", "-"))
        if k:
            keys.add(k)
    return keys


def _vbhn_base_key(e: dict) -> str:
    """Số hiệu BẢN GỐC (base) của VBHN hợp nhất = sohieu có NĂM NHỎ NHẤT trong chuỗi goc (luật gốc cũ nhất; các luật
    SỬA thì mới hơn). Phân biệt 'query LÀ gốc của VBHN' (VBHN-first redirect ĐÚNG, vd 45/2019→VBHN_18) với 'query chỉ là
    1 luật SỬA trong chuỗi' (vd 114/2025 Phòng bệnh nằm trong chuỗi VBHN Luật thuốc lá → KHÔNG phải canonical của 114/2025)."""
    keys = _goc_keys(e)
    if not keys:
        return ""
    return min(keys, key=_sohieu_base_sort_year)


def _source_map_one(q: str, entries: list[dict]) -> dict:
    """Resolve nguồn rà soát theo VBHN-first, chống nhầm do file gán tên sai."""
    q = q.strip()
    qkey = norm_sohieu(q.replace("_", "-")) if _looks_like_sohieu_query(q) else ""
    qn = _strip_accents(q).lower()
    qnk = _name_key(q)
    direct, by_name, related_vbhn, amends_vbhn, goc_mismatch_vbhn = [], [], [], [], []
    _vbhn_goc_hits = []
    for e in entries:
        sh = _sohieu_key_entry(e)
        nm_plain = _strip_accents(_entry_name(e)).lower()
        nk = _name_key(_entry_name(e))
        if qkey and _sohieu_query_hits_entry(qkey, sh):   # v1.33.47: +bare-VBHN 1 chiều (query không năm ↔ entry có năm)
            direct.append(e)
        if qn and (qn in nm_plain or (qnk and nk and (qnk in nk or nk in qnk))
                   or _entry_query_match(q, e, include_subject=False)):   # token/phrase: bắt 'Luật Dân số' ↔ '...Dan_so'
            by_name.append(e)
        if qkey and _is_vbhn_entry(e) and qkey in _goc_keys(e):
            _vbhn_goc_hits.append(e)
    # Phân loại VBHN-goc-hit SAU vòng lặp (cần direct/by_name để biết CHỦ ĐỀ truy vấn cho cổng chống goc-nhiễm).
    _q_subject = _derive_subject_from_entries(direct or by_name)
    for e in _vbhn_goc_hits:
        # VBHN-first redirect CHỈ khi query LÀ GỐC của VBHN (base = năm nhỏ nhất chuỗi goc). Nếu query chỉ là 1 luật
        # SỬA trong chuỗi (vd 114/2025 Phòng bệnh trong chuỗi VBHN thuốc lá) → amends_vbhn (liên quan, KHÔNG canonical).
        if _vbhn_base_key(e) != qkey:
            amends_vbhn.append(e)
        elif _vbhn_goc_corroborated(e, qkey, _q_subject):
            related_vbhn.append(e)
        else:
            # §1.1: registry.goc trỏ qkey NHƯNG tên/chủ đề VBHN thuộc văn bản KHÁC (goc nhiễm) → KHÔNG redirect.
            goc_mismatch_vbhn.append(e)
    amendment_candidates = _find_amendment_candidates(qkey, direct, by_name, entries)
    # §1.2 (log rà): nếu đã có VBHN-first (related_vbhn) thì luật-sửa NẰM TRONG CHUỖI goc của VBHN đó ĐÃ ĐƯỢC HỢP NHẤT
    # → KHÔNG còn là 'thiếu liên kết' và KHÔNG cần PAUSE (vd PPP 64/2020: 57/2024 & 90/2025 đã trong goc VBHN 123).
    _consolidated_keys = set()
    for v in related_vbhn:
        _consolidated_keys |= _goc_keys(v)
    consolidated_amendments = [e for e in amendment_candidates
                               if _consolidated_keys and _sohieu_key_entry(e) in _consolidated_keys]
    if _consolidated_keys:
        amendment_candidates = [e for e in amendment_candidates
                                if _sohieu_key_entry(e) not in _consolidated_keys]
    unlinked_amendments = [e for e in amendment_candidates if not e.get("_amendment_linked_to_query")]
    # P1-5 (log rà 71 luật): chỉ ESCALATE PAUSE_AND_ASK_USER khi có ÍT NHẤT 1 ứng viên MANG SỐ HIỆU VBQPPL hợp lệ
    # (QH/NĐ/TT/PL…). Ứng viên sohieu=∅ (raw chưa bóc số / thư góp ý) vẫn LIỆT KÊ nhưng KHÔNG tự dừng workflow.
    amendment_candidates_normative = [e for e in amendment_candidates if e.get("_amendment_has_sohieu")]
    # v1.29.6 (P0b): chỉ ứng viên MẠNH (linked/high — xem _find_amendment_candidates) mới đủ lực ESCALATE PAUSE.
    amendment_candidates_strong = [e for e in amendment_candidates_normative if e.get("_amendment_strong")]
    pool = related_vbhn or direct or by_name
    pool = list({(_entry_drive_id(e) or str(id(e))): e for e in pool}.values())
    pool.sort(key=_entry_score, reverse=True)
    canonical = pool[0] if pool else None
    # srcmap_name_resolution: truy van TEN neu LOAI 'Luat/Bo luat/Phap lenh' -> UU TIEN hit tier>=loai-neu (chong
    # chot ND/TT lam canonical chi vi diem cao). Chi nhan hit KHOP-CHAT (_name_strong_match) & KHONG cach ly -> vua
    # sua 'Luat Dau tu'->Luat (khong ND), vua KHONG over-fire LOW_CONFIDENCE khi co hit tier-Luat chac.
    _qdt = _query_doctype_tier(q)
    if (not qkey) and _qdt >= 4 and pool:
        _tier_strong = [e for e in pool if not _entry_quarantined(e)
                        and _vb_tier_rank(e) >= _qdt and _name_strong_match(q, _entry_name(e))]
        if _tier_strong:
            canonical = max(_tier_strong, key=_entry_score)
    warnings = []
    # name_rank_collision gate: truy vấn THEO TÊN (không số hiệu) có >1 hit nhưng hit điểm-cao chỉ khớp-MỜ
    # (không đủ chủ đề: 'Luật Dân số'→'Dân chủ ở cơ sở'/'Dân sự', 'Việc làm'→'đi làm việc ở nước ngoài',
    # 'Phí và lệ phí'→'Học phí'). KHÔNG chốt 1 canonical sai → trả None + LOW_CONFIDENCE thay vì in RÀ SOÁT TRÊN.
    name_only = (not qkey) and (not related_vbhn) and (not direct) and bool(by_name)
    # A1 (port Codex, verified): truy vấn THEO TÊN — ghim canonical CHỈ trong các hit KHỚP CHỦ ĐỀ thật
    # (_name_subject_match, abbrev-aware: 'BLLD'≡'Bộ luật Lao động', 'BHXH'≡'bảo hiểm xã hội'), KHÔNG cho token chung
    # chốt nhầm ('Bộ luật Lao động'→'Dân chủ cơ sở'). Query tier-Luat/Bộ luật → siết thêm tier+strong. Nếu KHÔNG có
    # hit chủ đề → canonical=None + SUBJECT_MISMATCH (thay vì ghim sai). Loại quarantine khỏi ứng viên (gốc rễ A1=B1).
    name_subject_hits = []
    if name_only:
        name_subject_hits = [e for e in pool if not _entry_quarantined(e) and _name_subject_match(q, e)]
        if _qdt >= 4:
            name_subject_hits = [e for e in name_subject_hits
                                 if _vb_tier_rank(e) >= _qdt and _name_strong_match(q, _entry_name(e))]
        if name_subject_hits:
            canonical = max(name_subject_hits, key=_entry_score)
        elif canonical is not None:
            canonical = None
            warnings.append("NAME_QUERY_SUBJECT_MISMATCH_NO_CANONICAL: truy vấn tên có chủ đề rõ nhưng các hit KHÔNG "
                            "khớp chủ đề — KHÔNG chốt canonical; chạy lại bằng SỐ HIỆU hoặc thêm chủ đề/năm.")
    if name_only and len(by_name) > 1 and canonical is not None and not _name_strong_match(q, _entry_name(canonical)):
        canonical = None
        warnings.append("LOW_CONFIDENCE_NAME_MATCH: nhiều hit theo tên nhưng hit điểm-cao chỉ KHỚP-MỜ (thiếu chủ đề "
                        "đầy đủ của truy vấn) — KHÔNG chốt canonical; xem name_hits, verify trích yếu/số hiệu trước khi rà.")
    if goc_mismatch_vbhn:
        warnings.append("GOC_SUBJECT_MISMATCH: registry.goc của 1 VBHN trỏ số hiệu này NHƯNG tên/chủ đề VBHN thuộc "
                        "văn bản KHÁC (goc bị nhiễm) — KHÔNG redirect sang VBHN đó; rà bản gốc đích. "
                        "Sửa registry.goc của VBHN (xem goc_mismatch_vbhn) qua `tl register` (reg_upsert).")
    if related_vbhn:
        warnings.append("VBHN_FIRST_APPLIED: có VBHN hợp nhất nhận số hiệu đích là BẢN GỐC (base) trong trường goc; nên rà trên VBHN.")
        # S9 (log 2026-07-01): VBHN TRONG CORPUS có thể LỖI THỜI (đã có bản hợp nhất mới hơn trên web chưa nạp — ca BLHS
        # 01/VBHN 2017 vs 135/VBHN 2025). BẮT BUỘC xác minh bản mới nhất (QT-5 lượt-2 'mới nhất <năm>' + Công báo).
        warnings.append("VBHN_CANDIDATE_UNVERIFIED_LATEST: VBHN trong corpus CHƯA chắc là BẢN MỚI NHẤT — chạy `tl vbhn-check "
                        "--goc <số> --subject <chủ đề>` rồi QT-5 lượt-2 ('mới nhất <năm>' + site:congbao.chinhphu.vn) tìm số "
                        "VBHN lớn hơn/ngày sau cùng VPQH trước khi trích dẫn (số VBHN tăng dần mỗi lần hợp nhất, KHÔNG semver).")
        if any(_is_high_amendment_subject(_entry_name(v)) or _is_high_amendment_subject(_derive_subject_from_entries([v])) for v in related_vbhn):
            warnings.append("VBHN_HIGH_AMENDMENT_VELOCITY: luật SỬA ĐỔI DỒN DẬP (2024-2026) — BẮT BUỘC kiểm Công báo năm hiện tại.")
    if len(related_vbhn) > 1:
        warnings.append("MULTIPLE_VBHN_BASE: số hiệu là GỐC của >1 VBHN (có thể số hiệu tái dùng theo năm) — KHÔNG chốt 1 canonical; xem related_vbhn và verify năm/loại trước khi rà.")
    if amends_vbhn and not related_vbhn:
        warnings.append("AMENDS_OTHER_VBHN: số hiệu đích là LUẬT SỬA nằm trong chuỗi hợp nhất của VBHN khác (KHÔNG phải bản gốc của VBHN đó); canonical là CHÍNH văn bản đích — KHÔNG redirect sang VBHN ấy. Xem amends_vbhn.")
    if consolidated_amendments:
        warnings.append(f"AMENDMENTS_ALREADY_CONSOLIDATED: {len(consolidated_amendments)} luật-sửa đã nằm trong chuỗi "
                        "hợp nhất của VBHN canonical (đã phản ánh) — KHÔNG cần nạp/link/PAUSE; xem consolidated_amendments.")
    # §1.2 cổng PHỤ (port Codex): với luật-sửa CÒN LẠI (chưa nằm trong chuỗi goc) — nếu VBHN canonical ban hành KHÔNG
    # sớm hơn TẤT CẢ (đều có ngày rõ) → coi như đã phản ánh, hạ PAUSE→INFO. Bổ trợ cổng goc-chain (dùng khi goc thiếu
    # nhưng ngày ban hành đủ). Trên manifest hiện thiếu ngày → cổng này im lặng; goc-chain đã lo phần lớn ca.
    _pause_vbhn = canonical if (canonical and _is_vbhn_entry(canonical)) else (related_vbhn[0] if related_vbhn else None)
    # ═══ v1.32.0 (log rà 77 Luật — 3 defect lớp amendment-gate A1/A2/A3) ═══
    _canon_confirmed = bool(canonical is not None and _entry_confirmed(canonical))
    _canon_is_vbhn = bool(canonical is not None and _is_vbhn_entry(canonical))
    _canon_is_omnibus = bool(canonical is not None and _is_omnibus_entry(canonical))
    # A2: canonical CHÍNH LÀ VBHN (query trực tiếp số VBHN — ca 115-2026-VBHN): luật nằm trong chuỗi goc CỦA NÓ là
    # thành-phần-đã-hợp-nhất, KHÔNG phải amendment mồ côi (khối consolidated ở trên chỉ gom goc của related_vbhn —
    # rỗng khi query thẳng VBHN). Chuyển các ứng viên đó sang consolidated_amendments.
    if _canon_is_vbhn:
        _ck2 = _goc_keys(canonical)
        _moved = [e for e in amendment_candidates if _ck2 and _sohieu_key_entry(e) in _ck2]
        if _moved:
            consolidated_amendments = consolidated_amendments + _moved
            _mkeys = {_sohieu_key_entry(e) for e in _moved}
            amendment_candidates = [e for e in amendment_candidates if _sohieu_key_entry(e) not in _mkeys]
            unlinked_amendments = [e for e in unlinked_amendments if _sohieu_key_entry(e) not in _mkeys]
            amendment_candidates_normative = [e for e in amendment_candidates_normative if _sohieu_key_entry(e) not in _mkeys]
            amendment_candidates_strong = [e for e in amendment_candidates_strong if _sohieu_key_entry(e) not in _mkeys]
            warnings.append(f"AMENDMENTS_ALREADY_CONSOLIDATED: {len(_moved)} luật-sửa nằm trong chuỗi goc của CHÍNH "
                            "canonical VBHN này (đã phản ánh) — KHÔNG nạp/link/PAUSE; xem consolidated_amendments.")
    vbhn_date_covered, vbhn_issue_date, covered_amendments = _amendments_covered_by_vbhn_date(
        _pause_vbhn, amendment_candidates_normative)
    # S-8 (v1.33.15 — log rà 67 Luật: 37/67 vào hàng web LƯỢT-2, ~15 ca CHỈ vì UNVERIFIED_LATEST dù VBHN
    # 2025-2026 vừa hợp nhất xong — 33-2024 Lưu trữ/45-2024 Di sản/50-2024 Công đoàn/87-2025): VBHN DUY NHẤT
    # + năm ban hành rõ ≥ năm-nay−1 + KHÔNG luật-sửa nào MỚI HƠN đã biết (covered theo ngày, hoặc không có ứng
    # viên normative) → hạ UNVERIFIED_LATEST thành cờ INFO — hàng đợi lượt-2 hết loãng, ưu tiên thật nổi lên.
    # KHÔNG đổi doctrine: HIGH_VELOCITY giữ nguyên (nhóm dồn dập vẫn bắt buộc Công báo), và trước khi TRÍCH DẪN
    # chính thức vẫn `tl vbhn-verify --official-required` như cũ — đây chỉ là hạ ƯU TIÊN hàng đợi.
    if related_vbhn and len(related_vbhn) == 1 and _pause_vbhn is not None:
        _vy8 = _entry_issue_year(_pause_vbhn) or _sohieu_year(_sohieu_key_entry(_pause_vbhn))
        # Nhóm HIGH_VELOCITY (BLHS/Đầu tư/Thuế…) KHÔNG hạ — doctrine S10: sửa dồn dập, Google rank trang cũ,
        # bản hợp nhất mới có thể ra TRONG NĂM → UNVERIFIED_LATEST của nhóm này luôn là việc thật.
        _hi_vel8 = any(w.startswith("VBHN_HIGH_AMENDMENT_VELOCITY") for w in warnings)
        if (_vy8 and _vy8 >= time.localtime().tm_year - 1 and not _hi_vel8
                and (vbhn_date_covered or not amendment_candidates_normative)):
            warnings = [w for w in warnings if not w.startswith("VBHN_CANDIDATE_UNVERIFIED_LATEST")]
            warnings.append(f"VBHN_LATEST_RECENT_COVERED: VBHN duy nhất ban hành {_vy8} (rất mới) và không có "
                            "luật-sửa nào MỚI HƠN đã biết trong corpus → hạ ưu tiên web LƯỢT-2; vẫn chạy "
                            "`tl vbhn-verify --official-required` trước khi trích dẫn chính thức.")
    # A1: canonical ĐÃ CONFIRM (registry.verified) → doctrine §confirm 'tin dùng luôn' phải phủ CẢ nhóm cờ
    # amendment-gate (ca 90-2025 confirmed=yes vẫn bị VBHN_RECHECK + UNLINKED). Suppression NHẤT QUÁN với
    # action_required bên dưới. Gỡ nhãn confirm nếu nghi có sửa đổi MỚI hơn ngày confirm.
    _gate_escalate = bool(amendment_candidates_strong) and not vbhn_date_covered and not _canon_confirmed
    if amendment_candidates:
        warnings.append("AMENDMENT_CANDIDATE_IN_CORPUS: phát hiện văn bản sửa đổi liên quan trong corpus/NLM; không được rà bản gốc đơn lẻ.")
        if _canon_confirmed:
            warnings.append("AMENDMENT_GATE_SUPPRESSED_CONFIRMED: canonical verified (đã rà kỹ) — bỏ UNLINKED/"
                            "VBHN_RECHECK/PAUSE theo doctrine §confirm; amendment_candidates chỉ liệt kê tham khảo. "
                            "Nghi có sửa đổi MỚI HƠN ngày confirm → gỡ nhãn verified rồi rà lại.")
        elif vbhn_date_covered:
            warnings.append(f"AMENDMENT_CANDIDATES_COVERED_BY_VBHN_DATE: VBHN ban hành ngày {vbhn_issue_date} không sớm "
                            "hơn toàn bộ luật-sửa có ngày rõ — hạ cảnh báo xuống INFO, KHÔNG PAUSE; vẫn nên verify footnote khi chốt.")
        else:
            # A3: canonical là OMNIBUS (sửa nhiều luật) — bản chất AMENDS_OTHER, không bao giờ có VBHN của chính nó;
            # ứng viên mồ-côi quanh nó phần lớn là nhiễu cùng-chủ-đề → cờ riêng, KHÔNG UNLINKED/LOW_CONF (hết REVIEW lặp).
            if unlinked_amendments and not _canon_is_omnibus:
                warnings.append("UNLINKED_AMENDMENT_CANDIDATE: văn bản sửa đổi có trong corpus nhưng thiếu goc/sua_doi; "
                                "phải hỏi người dùng để cập nhật registry trước khi rà tiếp "
                                "(DANH SÁCH ứng viên: key `unlinked_amendment_candidates`/`amendment_candidates` — v1.33.6).")
            if not related_vbhn:
                if _canon_is_vbhn:
                    # A2: KHÔNG 'tìm VBHN cho một VBHN' — chuyển sang xác minh chuỗi goc/sua_doi + bản mới nhất.
                    warnings.append("VBHN_GOC_VERIFY: canonical CHÍNH LÀ bản hợp nhất — không tìm VBHN cho VBHN; "
                                    "xác minh chuỗi goc/sua_doi phủ đủ (`tl footnote-map <id>` / `tl relation-check "
                                    "--base <goc>`) và bản MỚI NHẤT (QT-5 lượt-2, số VBHN tăng dần).")
                elif _canon_is_omnibus:
                    warnings.append(f"OMNIBUS_AMENDS_OTHER: canonical là luật SỬA NHIỀU LUẬT — không có VBHN của chính nó; "
                                    f"rà theo từng luật ĐÍCH trong goc/`tl relation-check --base <đích>`"
                                    + (f" ({len(unlinked_amendments)} ứng viên mồ-côi quanh nó = tham khảo, không REVIEW)."
                                       if unlinked_amendments else "."))
                else:
                    warnings.append("VBHN_RECHECK_REQUIRED: luật đã/ có thể đã được sửa đổi; chạy `tl vbhn-check` theo trích yếu + 'hợp nhất' và không kết luận chưa có VBHN.")
            # v1.29.6 (P0b — log 118 Luật: 15 PAUSE giả, 100% conf=low non-linked): PAUSE CHỈ khi có ứng viên MẠNH
            # (linked đúng số hiệu / confidence=high; omnibus non-linked = weak). Weak-only → REVIEW với cờ riêng.
            if _gate_escalate:
                warnings.append("PAUSE_AND_ASK_USER: DỪNG rà soát, trình danh sách amendment_candidates và xin xác nhận nạp/link/VBHN official-first.")
            elif amendment_candidates_normative and not _canon_is_omnibus:
                warnings.append("AMENDMENT_CANDIDATE_LOW_CONFIDENCE: ứng viên sửa-đổi đều KHỚP MỜ (confidence=low, "
                                "không dẫn chiếu số hiệu base / omnibus chưa xác định luật đích) — REVIEW khi rà, "
                                "KHÔNG dừng workflow; verify goc/sua_doi nếu nghi thật.")
    qyear = _sohieu_year(qkey)
    # D (v1.33.18 — MERGE bundle-18, log rà 67: cặp gốc/sửa LỆCH PHA — 64-2006 HIV verdict OK 'đã hợp nhất'
    # nhưng luật sửa 71-2020 của CHÍNH chuỗi đó vẫn bị NO_VERIFIED_VBHN + QT5 đẩy vào web lượt-2): luật SỬA đã
    # nằm trong chuỗi goc của VBHN khác (amends_vbhn ≠ ∅, cờ AMENDS_OTHER_VBHN) thì nội dung của nó ĐÃ được
    # phản ánh trong VBHN của luật ĐÍCH — không đòi VBHN riêng cho nó nữa (đồng dạng nhánh omnibus AMENDS_OTHER).
    if (not related_vbhn) and (not amends_vbhn) and qkey and direct \
            and not any(_is_vbhn_entry(e) for e in direct) and (qyear is None or qyear <= 2021):
        warnings.append("NO_VERIFIED_VBHN_IN_CORPUS: manifest chưa có VBHN đã xác minh; KHÔNG kết luận là không tồn tại.")
        warnings.append("QT5_WEB_REQUIRED: chạy tìm web theo trích yếu/chủ đề + 'hợp nhất' (không tìm một lần theo số hiệu bản gốc).")
    elif (not related_vbhn) and (not amends_vbhn) and (not qkey) and canonical is not None and not _canon_is_vbhn \
            and not any(_is_vbhn_entry(e) for e in pool):
        # A1 (v1.33.2 — log rà 111 Luật: source-map "Bộ luật Hình sự" trả OK/flags=[] chọn bản gốc 2015 dù §0.1
        # lấy chính BLHS làm ví dụ VBHN lỗi thời 135/VBHN-2025): gate trên đòi qkey+direct → truy vấn THEO TÊN
        # câm hoàn toàn = false-clean. Cùng điều kiện với gate sohieu, năm lấy từ CANONICAL thay vì query.
        _cyr = _sohieu_year(_sohieu_key_entry(canonical)) or _entry_issue_year(canonical)
        if _cyr is None or _cyr <= 2021:
            warnings.append("NO_VERIFIED_VBHN_IN_CORPUS: manifest chưa có VBHN đã xác minh; KHÔNG kết luận là không tồn tại.")
            warnings.append("QT5_WEB_REQUIRED: chạy tìm web theo trích yếu/chủ đề + 'hợp nhất' (không tìm một lần theo số hiệu bản gốc).")
    # A1b (v1.33.2): nhóm SỬA DỒN DẬP (S10) phải cảnh báo CẢ khi corpus chưa có VBHN nào — trước chỉ gắn trong
    # nhánh `related_vbhn` nên đúng ca cần nhất (thiếu VBHN) lại im.
    if (not related_vbhn) and canonical is not None and not _canon_is_vbhn and (
            _is_high_amendment_subject(q) or _is_high_amendment_subject(_entry_name(canonical))):
        warnings.append("VBHN_HIGH_AMENDMENT_VELOCITY: luật SỬA ĐỔI DỒN DẬP (2024-2026) mà corpus CHƯA có VBHN "
                        "tương ứng — BẮT BUỘC kiểm Công báo năm hiện tại trước khi rà bản gốc.")
    if qkey:
        direct_vbhn = [e for e in direct if _is_vbhn_entry(e)]
        if direct_vbhn:
            # v1.17.17: chỉ bật reuse-risk khi metadata chưa đủ hoặc có nhiều ứng viên cùng số.
            # Một VBHN đã có năm/chủ đề rõ không cần cảnh báo nhiễu ở mọi truy vấn.
            # v1.33.0 (log rà 15 — B4: 25-2025-VBHN-VPQH năm ĐỦ ở cả sohieu-key lẫn tên VẪN bị REVIEW): 'nhiều
            # ứng viên cùng số' và cờ thiếu-năm chỉ xét trên VĂN BẢN PHÂN BIỆT — bỏ sidecar file-thô + quarantine
            # (cặp GDoc+.docx cùng số là MỘT văn bản, không phải tái dùng số). Tên trơ thiếu năm (133/61/72) vẫn
            # cờ đúng qua VBHN_NAME_MISSING_YEAR trên chính bản phân biệt.
            _distinct_vbhn = [e for e in direct_vbhn
                              if not _entry_quarantined(e) and not _is_source_sidecar(e, direct, canonical)]
            risky_vbhn = (len(_distinct_vbhn) > 1) or any(
                (not _vbhn_year_complete(e)) and
                set(_title_flags(e)) & {"VBHN_BARE_NUMBER", "VBHN_MISSING_YEAR_OR_DATE", "VBHN_NAME_MISSING_YEAR"}
                for e in (_distinct_vbhn or direct_vbhn)
            )
            if risky_vbhn:
                warnings.append("VBHN_NUMBER_REUSE_RISK: số VBHN có thể tái sử dụng theo năm; phải verify ngày ban hành + tiêu đề + dòng hợp nhất trước khi tin.")
            # P1-4 (log rà 71 luật): TÁI DÙNG SỐ THẬT — >1 VBHN CÙNG số hiệu nhưng KHÁC CHỦ ĐỀ (vd 89-VBHN-VPQH =
            # NSNN 2026 + NSNN gốc + MTTQ). KHÔNG tự chốt 1 canonical theo điểm (dễ trả nhầm MTTQ khi người hỏi NSNN);
            # trả canonical=None + đòi phân định. CHỈ khi ĐA CHỦ ĐỀ (nhiều version cùng chủ đề → vẫn chốt bản điểm cao).
            _nonraw_vbhn = [e for e in direct_vbhn
                            if not _is_raw_no_gdoc_name(_entry_name(e)) and not _entry_quarantined(e)]
            # CHỈ đếm CHỦ ĐỀ RÕ (tail không rỗng): bản tên-trơ '89-VBHN-VPQH' (tail='') KHÔNG tính là chủ đề khác
            # → tránh false-ambiguity (trước fallback full-name làm bản trơ ≠ bản có chủ đề → clear canonical oan).
            _subj_keys = {tk for e in _nonraw_vbhn if (tk := _name_tail_key(_entry_name(e)))}
            if len(_nonraw_vbhn) > 1 and len(_subj_keys) > 1:
                canonical = None
                warnings.append("VBHN_REUSE_AMBIGUOUS_NO_CANONICAL: >1 VBHN dùng CÙNG số hiệu nhưng KHÁC chủ đề — "
                                "KHÔNG tự chốt canonical theo điểm. Phân định bằng `tl source-map \"<số hiệu> <chủ đề/năm>\"` "
                                "(hoặc `tl vbhn-check --goc <số> --subject <chủ đề>`); xem direct_hits chọn đúng bản trước khi rà.")
    if len(by_name) > 1 and not qkey:
        warnings.append("NAME_QUERY_MULTIPLE_HITS: truy vấn theo tên có nhiều hit; phải dựa canonical/vb_status, không lấy hit đầu theo tên.")
    # entry ĐÃ CONFIRM (registry.verified) = đã rà kỹ → TIN dùng luôn, KHÔNG nhồi vào DIRTY/WARN (giảm nhiễu, tăng tốc).
    dirty = [e for e in pool if not _entry_confirmed(e) and ((not _entry_sohieu(e)) or _bad_cat(_entry_cat(e)) or ("root" in _entry_cat(e).lower()))]
    if dirty:
        warnings.append("DIRTY_CANDIDATES: có dòng root/orphan/metadata rỗng trong nhóm; chạy `tl hygiene plan` trước khi thao tác ghi.")
    risky = []
    for e in pool:
        if _entry_quarantined(e) or _entry_confirmed(e):   # cách ly HOẶC đã-confirm → không WARN (giảm nhiễu)
            continue
        # A1 (log rà 122 Luật): ghost/rỗng-tên trong candidate set không được kích TITLE_OR_REGISTRY_WARN hàng loạt.
        if not _name_key(_entry_name(e)):
            continue
        flags = _source_map_flags(e)
        # B3 (v1.32.0 — log rà 77: 21 ca RAW_NAME_NOT_NLM là sidecar .docx/.pdf cạnh GDoc, đúng thiết kế nhưng loãng
        # tín hiệu mỗi lần rà): bỏ cờ này khỏi risky khi entry là SIDECAR của bản chuẩn trong cùng nhóm.
        if "RAW_NAME_NOT_NLM" in flags and _is_source_sidecar(e, pool, canonical):
            # review v1.32.0 (CONFIRMED): PHẢI truyền canonical — thiếu nó, guard 'other is not canonical' trong
            # _is_source_sidecar không kích hoạt → có thể suppress nhầm khi sidecar chỉ khớp entry thường.
            flags = [f for f in flags if f != "RAW_NAME_NOT_NLM"]
        # A3 (tối ưu MERGE): CHỈ kích WARN trên cờ SIÊU-DỮ-LIỆU per-law thật; cờ TRÔI toàn cục (NLM/raw-sibling) không
        # WARN (đã ở doctor/sweep + nlm_gaps). Vẫn giữ `flags` đầy đủ trong risky entry để không mất thông tin.
        substantive = [f for f in flags if f not in _TITLE_WARN_GLOBAL_FLAGS]
        if substantive:
            risky.append({"entry": _summ_entry_source_map(e), "flags": flags, "reason": _flags_reason(flags)})
    if risky:
        warnings.append("TITLE_OR_REGISTRY_WARN: có ứng viên bị WARN; xem `risky_candidates` và chạy `tl hygiene plan --json`.")
    if canonical is not None and _entry_confirmed(canonical):
        warnings.append(f"CONFIRMED: canonical đã rà kỹ & gán nhãn verified={_entry_confirmed(canonical)} — tin dùng luôn, không cần re-review.")
    # A3 (log rà): canonical là VBHN nhưng số hiệu CHỈ MỤC (registry/qkey) là số hiệu BẢN GỐC khác hẳn số hiệu VBHN
    # thật (vd row 52-2014-QH13 nhưng canonical = VBHN_121-VBHN-VPQH Hôn nhân) → cảnh báo để KHÔNG trích dẫn nhầm số.
    if canonical is not None:
        _can_name_sh = norm_sohieu(_parse_sohieu_from_name(_entry_name(canonical)).replace("_", "-"))
        _can_reg_sh = _sohieu_key_entry(canonical)
        if _can_name_sh and _can_reg_sh and _can_name_sh != _can_reg_sh \
                and "VBHN" in _can_name_sh and "VBHN" not in _can_reg_sh:
            warnings.append(f"CANONICAL_VBHN_NUMBER_DIFFERS: số hiệu chỉ mục ({_can_reg_sh}) khác số hiệu VBHN thật của "
                            f"bản canonical ({_can_name_sh}) — trích dẫn theo số hiệu VBHN, không theo số bản gốc.")
    # #5 log (đề xuất): NỔI số đếm PENDING ngay ở source-map — rủi ro hiệu-lực-tương-lai lặp xuyên BHXH/BLLĐ/BHYT.
    # Rẻ: chỉ soi NGÀY HIỆU LỰC (registry) của nhóm > hôm nay (KHÔNG chạy footnote-map nặng); rỗng thì im lặng.
    import datetime as _dt
    _today = _dt.date.today().isoformat()
    _pp = {(_entry_drive_id(e) or str(id(e))): e
           for e in (([canonical] if canonical else []) + direct + related_vbhn + amends_vbhn + by_name)}
    pending_future = [(e, hl) for e in _pp.values() if (hl := _entry_hieuluc_date(e)) and hl > _today]
    if pending_future:
        warnings.append(f"PENDING_FUTURE_EFFECT: {len(pending_future)} văn bản trong nhóm có NGÀY HIỆU LỰC tương lai (> {_today}) "
                        "— rủi ro 'chưa/đang có hiệu lực'; chạy `tl footnote-map` để rà pending cấp Điều trước khi kết luận.")
    _pp_vals = list(_pp.values())
    draft_hits = [e for e in _pp_vals if _entry_is_draft(e)]
    if draft_hits:
        warnings.append(f"DRAFT_NOT_EFFECTIVE: {len(draft_hits)} nguồn là DỰ THẢO — chưa hiệu lực; không dùng như luật/văn bản đang có hiệu lực.")
    nlm_gaps = [e for e in _pp_vals if "CORPUS_TRUE_NOT_ON_NLM" in _title_flags(e)
                and not _dup_of_live_sibling(e, _pp_vals)]
    if nlm_gaps:
        warnings.append(f"CORPUS_TRUE_NOT_ON_NLM: {len(nlm_gaps)} văn bản corpus=true nhưng chưa có nguồn NLM live "
                        "— chạy `tl ingest-local`/`tl nlm-push` hoặc xác nhận để ngoài NLM có chủ ý.")
    out = {
        "query": q,
        "query_key": qkey or None,
        "canonical": _summ_entry_source_map(canonical),
        "mode": "vbhn_related" if related_vbhn else ("direct_sohieu" if direct else "name" if by_name else "not_found"),
        "direct_hits": [_summ_entry_source_map(e) for e in sorted(direct, key=_entry_score, reverse=True)[:10]],
        "name_hits": [_summ_entry_source_map(e) for e in sorted(by_name, key=_entry_score, reverse=True)[:10]],
        "related_vbhn": [_summ_entry_source_map(e) for e in sorted(related_vbhn, key=_entry_score, reverse=True)[:10]],
        "amends_vbhn": [(_summ_entry_source_map(e) or {}) | {"vbhn_base": _vbhn_base_key(e)} for e in sorted(amends_vbhn, key=_entry_score, reverse=True)[:10]],
        "goc_mismatch_vbhn": [(_summ_entry_source_map(e) or {}) | {"registry_goc": _entry_goc(e), "name_goc_base": _name_goc_base_key(_entry_name(e))} for e in sorted(goc_mismatch_vbhn, key=_entry_score, reverse=True)[:10]],
        "consolidated_amendments": [_summ_entry_source_map(e) for e in sorted(consolidated_amendments, key=_entry_score, reverse=True)[:10]],
        "amendment_candidates": [(_summ_entry_source_map(e) or {}) | {"linked_to_query": bool(e.get("_amendment_linked_to_query")), "subject_overlap": e.get("_amendment_subject_overlap", 0), "confidence": e.get("_amendment_confidence", "low"), "strong": bool(e.get("_amendment_strong")), "omnibus": bool(e.get("_amendment_omnibus"))} for e in amendment_candidates[:10]],
        "unlinked_amendment_candidates": [(_summ_entry_source_map(e) or {}) | {"subject_overlap": e.get("_amendment_subject_overlap", 0), "confidence": "low"} for e in unlinked_amendments[:10]],
        "pending_future_count": len(pending_future),
        "pending_future": [(_summ_entry_source_map(e) or {}) | {"hieu_luc": hl} for e, hl in sorted(pending_future, key=lambda x: x[1], reverse=True)[:10]],
        "draft_count": len(draft_hits),
        "draft_hits": [_summ_entry_source_map(e) for e in draft_hits[:10]],
        "nlm_gap_count": len(nlm_gaps),
        "nlm_gaps": [_summ_entry_source_map(e) for e in nlm_gaps[:10]],
        "risky_candidates": risky[:10],
        "qt5_search_hints": list(dict.fromkeys((_qt5_search_hints(q, direct or by_name) + _qt5_queries(_derive_subject_from_entries(direct or by_name), qkey or q, ""))))[:8],
        "action_required": "PAUSE_AND_ASK_USER" if _gate_escalate else None,   # v1.29.6 P0b chỉ MẠNH; v1.32.0 A1: confirmed KHÔNG escalate (nhất quán warning)
        "covered_by_vbhn_date": bool(vbhn_date_covered),
        "vbhn_issue_date": vbhn_issue_date,
        "covered_amendment_candidates": [(_summ_entry_source_map(x["entry"]) or {}) | {"issue_date": x["issue_date"]} for x in covered_amendments[:10]],
        "warnings": warnings,
    }
    # 4D (v1.33.30 — MERGE bundle-29, STRUCTURED thay compact-string v1.33.29 ta): item tự mang chi tiết
    # ứng viên sửa đổi (số hiệu/tên/confidence/linked/strong/omnibus) — driver hết phải gọi thêm review-queue.
    _cand_seen: set = set()
    _cand_rows: list = []
    for _kind, _lst in (("amendment", amendment_candidates), ("unlinked_amendment", unlinked_amendments)):
        for _ce in (_lst or [])[:10]:
            _ck = _entry_drive_id(_ce) or _sohieu_key_entry(_ce) or str(id(_ce))
            if _ck in _cand_seen:
                continue
            _cand_seen.add(_ck)
            _row = (_summ_entry_source_map(_ce) or {})
            _row.update({"candidate_type": _kind,
                         "sohieu_key": _sohieu_key_entry(_ce),
                         "linked_to_query": bool(_ce.get("_amendment_linked_to_query")),
                         "subject_overlap": _ce.get("_amendment_subject_overlap", 0),
                         "confidence": _ce.get("_amendment_confidence", "low"),
                         "strong": bool(_ce.get("_amendment_strong")),
                         "omnibus": bool(_ce.get("_amendment_omnibus"))})
            _cand_rows.append(_row)
    out["candidates"] = _cand_rows
    out["candidate_count"] = len(_cand_rows)
    out["flags"] = _warning_codes(warnings)
    # v1.33.25 — schema parity với review-queue: source-map đơn lẻ cũng có flags_all/review_reason.
    out["flags_all"] = list(out["flags"])
    out["review_reason"] = list(out["flags"])
    # v1.33.25 — QT-5 fallback: nếu có cờ web nhưng hint rỗng, sinh query tối thiểu từ canonical/direct/related.
    if not out.get("qt5_search_hints") and (set(out["flags"]) & _RQ_WEB_FLAGS or "QT5_WEB_REQUIRED" in out["flags"]):
        _hint_pool = ([canonical] if canonical else []) + direct + related_vbhn + amends_vbhn + by_name
        _hint_subject = _derive_subject_from_entries(_hint_pool)
        _hint_key = qkey or (_sohieu_key_entry(canonical) if canonical else q)
        _hint_year = str(_sohieu_year(_hint_key) or "")
        out["qt5_search_hints"] = _qt5_queries(_hint_subject, _hint_key, _hint_year)[:8]
    out["verdict"] = _source_map_verdict(out)
    out["qt5_queries"] = out["qt5_search_hints"]   # P1-5 (v1.31.0): vocab thống nhất họ QT-5 {verdict,flags,qt5_queries} — giữ key cũ compat
    return out


def _entry_sua_doi(e: dict) -> str:
    return e.get("sua_doi") or e.get("sua_doi_bo_sung") or e.get("amended_by") or e.get("superseded_by") or ""


def _vb_tier_rank(e: dict) -> int:
    """Thứ bậc hiệu lực VBQPPL để chặn 'cấp dưới sửa cấp trên' (sai thứ bậc): một VB chỉ bị SỬA bởi VB NGANG/CAO hơn.
    5=Hiến pháp/Bộ luật/Luật/NQ-QH/VBHN-VPQH · 4=Pháp lệnh/NQ-UBTVQH · 3=Nghị định/NQ-CP · 2=Thông tư/TTLT/QĐ-TTg · 0=không rõ.
    Khóa theo HẬU TỐ số hiệu (tin cậy nhất), fallback trường `loai`."""
    shraw = (_sohieu_key_entry(e) or str(_entry_sohieu(e) or "")).upper().replace("Đ", "D")
    name = _strip_accents(_entry_name(e)).upper().replace("Đ", "D")
    nameblob = shraw + " " + name              # gồm cả TÊN: dòng rác sohieu=∅ vẫn mang 'ND-CP'/'TT-' trong tên
    loai = _strip_accents(str(e.get("loai") or "")).lower()
    # NĐ/TT/PL: nhận từ TÊN nữa (rac thường mang loại ở tên). LUẬT (QH\d) CHỈ nhận từ số hiệu THẬT (shraw) —
    # tránh nhầm 1 NĐ "quy định chi tiết Luật 57/2024/QH15" thành cấp luật do tên nhúng số hiệu luật khác.
    if "VPQH" in shraw or "hien phap" in loai:
        return 5                                   # Hiến pháp / VBHN của luật (VBHN-VPQH)
    if "UBTVQH" in nameblob or "-PL-" in nameblob or "phap lenh" in loai:
        return 4                                   # Pháp lệnh / NQ-UBTVQH  (xét TRƯỚC QH vì 'UBTVQH' chứa 'QH')
    if re.search(r"QH\d", shraw) or "bo luat" in loai or re.fullmatch(r"luat", loai or "") \
       or loai.startswith("luat ") or "nghi quyet cua quoc hoi" in loai:
        return 5                                   # Bộ luật / Luật / NQ-QH
    if "ND-CP" in nameblob or "nghi dinh" in loai:
        return 3                                   # Nghị định / NQ-CP
    if "TT-" in nameblob or "TTLT" in nameblob or "QD-TTG" in nameblob or "thong tu" in loai or "quyet dinh" in loai:
        return 2                                   # Thông tư / TTLT / QĐ-TTg
    if "nghi quyet" in loai:
        return 4
    return 0


def _query_doctype_tier(q: str) -> int:
    """Bac LOAI van ban NEU TRONG TRUY VAN ten (Luat/Bo luat/Phap lenh) de source-map uu tien hit dung cap, KHONG
    chot ND/TT (tier thap) lam canonical khi nguoi dung hoi 'Luat'. 0 neu query khong neu loai."""
    qn = _strip_accents(str(q or "")).lower().strip()
    if re.match(r"^bo\s+luat\b", qn):
        return 5
    if re.match(r"^phap\s+lenh\b", qn):
        return 4
    if re.match(r"^luat\b", qn):
        return 5
    return 0


def _today_iso() -> str:
    import datetime as _dt
    return _dt.date.today().isoformat()


def _entry_confirmed(e: dict | None) -> str:
    """Nhãn 'ĐÃ RÀ KỸ & CHẮC ĐÚNG' = field registry `verified` (có sẵn REG_COLS_, sống qua regen2). '' nếu chưa confirm.
    Entry có nhãn này → dedup/source-map/locate TIN dùng luôn, bỏ qua re-review nhiễu (tăng tốc rà soát)."""
    v = str((e or {}).get("verified") or "").strip()
    return "" if v.lower() in ("", "no", "false", "0", "chua", "pending", "none") else v


_HEADER_DATE_RE = re.compile(r"ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})", re.I)
# Cơ quan ban hành (kiểm pattern DÀI trước NGẮN vì 'quốc hội' nằm trong 'ủy ban thường vụ quốc hội'/'văn phòng quốc hội').
_HEADER_AGENCY_PATS = (("uy ban thuong vu quoc hoi", "UBTVQH"), ("van phong quoc hoi", "VPQH"),
                       ("quoc hoi", "QH"), ("chinh phu", "CP"), ("thu tuong", "TTg"))


_HL_SUFFIX_RE = re.compile(r"\bhl\s*\d{4}([\s\-/.]\d{1,2}){0,2}\b", re.I)   # hậu tố TÊN-FILE _HL<ngày> (KHÁC _HL_DATE_RE thân-văn-bản)


def _relation_audit(entries: list[dict], base: str = "", subject: str = "", amendments: list[str] | None = None, footnote_amend_keys: set | None = None) -> dict:
    base_key = norm_sohieu(base.replace("_", "-")) if base else ""
    amendment_keys = {norm_sohieu(x.replace("_", "-")) for x in (amendments or []) if x}
    base_entries = []
    if base_key:
        base_entries = [e for e in entries if _sohieu_key_entry(e) == base_key]
    if not subject:
        subject = _derive_subject_from_entries(base_entries)
    candidates: list[dict] = []
    cand_reason: dict[str, str] = {}   # drive_id → 'direct'|'ref'|'subject' (vì sao khớp — quyết định backfill)
    vbhn: list[dict] = []
    base_year = _sohieu_year(base_key) or 0
    for e in entries:
        sh = _sohieu_key_entry(e)
        refs = _relation_refs(e)
        sscore = _subject_score(e, subject)
        is_direct_amend = bool(amendment_keys and sh in amendment_keys)
        is_related_amend = bool(base_key and base_key in refs and _is_amendment_like(e))
        is_subject_amend = bool(subject and sscore >= 35 and _is_amendment_like(e) and sh != base_key)
        if base_year and _sohieu_year(sh) and _sohieu_year(sh) < base_year:
            is_subject_amend = False
        if is_direct_amend or is_related_amend or is_subject_amend:
            candidates.append(e)
            did = _entry_drive_id(e) or str(id(e))
            cand_reason[did] = "direct" if is_direct_amend else ("ref" if is_related_amend else "subject")
        if _is_vbhn_entry(e) and ((base_key and base_key in refs) or (subject and sscore >= 35)):
            # P1-4 (v1.31.0): VBHN cấp Bộ + base Luật QH → CHỈ giữ khi goc-chain THẬT dẫn chiếu base (refs);
            # subject-match sscore≥35 một mình KHÔNG đủ (log: VBHN-BGDDT nổi cho Luật Giáo dục 123/2025).
            if _vbhn_agency_mismatch(base_key, e) and not (base_key and base_key in refs):
                continue
            vbhn.append(e)
    candidates = list({(_entry_drive_id(e) or str(id(e))): e for e in candidates}.values())
    candidates.sort(key=_entry_score, reverse=True)
    vbhn = list({(_entry_drive_id(e) or str(id(e))): e for e in vbhn}.values())
    vbhn.sort(key=_entry_score, reverse=True)
    # ── #1 FIX: footnote-map của VBHN là nguồn XÁC THỰC, ưu tiên hơn heuristic trùng chủ đề ──
    # Reason MẠNH NHẤT theo số hiệu (1 số hiệu có thể nhiều entry): direct > ref > subject.
    _reason_rank = {"direct": 3, "ref": 2, "subject": 1}
    key_reason: dict[str, str] = {}
    for e in candidates:
        k = _sohieu_key_entry(e)
        if not k:
            continue
        did = _entry_drive_id(e) or str(id(e))
        r = cand_reason.get(did, "subject")
        if _reason_rank.get(r, 0) > _reason_rank.get(key_reason.get(k, ""), 0):
            key_reason[k] = r
    fn_keys = {norm_sohieu(str(k).replace("_", "-")) for k in (footnote_amend_keys or []) if k}
    def _eligible_sua_doi(k: str) -> bool:
        # direct (user xác nhận qua --amendment) / ref (registry trỏ base) = luôn đủ điều kiện.
        # subject-only (CHỈ trùng chủ đề) = CHỈ khi footnote-map của VBHN xác nhận; không có footnote-map → KHÔNG backfill.
        if key_reason.get(k, "subject") in ("direct", "ref"):
            return True
        return bool(fn_keys) and k in fn_keys
    eligible_keys = sorted(k for k in key_reason if _eligible_sua_doi(k))
    blocked_subject_keys = sorted(k for k in key_reason if not _eligible_sua_doi(k))
    footnote_only_amendments = sorted(fn_keys - set(key_reason)) if fn_keys else []
    missing_links = []
    for e in base_entries:
        sua = {norm_sohieu(x) for x in re.split(r"[;,|]+", str(_entry_sua_doi(e) or "")) if x.strip()}
        # CHỈ backfill sua_doi cho số hiệu ĐỦ ĐIỀU KIỆN (direct/ref/footnote-confirmed) — KHÔNG dùng candidate thô.
        missing = [k for k in eligible_keys if k and k not in sua]
        if missing:
            missing_links.append({"action": "BACKFILL_SUA_DOI_ON_BASE", "drive_id": _entry_drive_id(e),
                                  "sohieu": _entry_sohieu(e), "add": missing,
                                  "evidence": "footnote-map" if fn_keys else "direct/registry-linked"})
    subject_only_review = []
    for e in candidates:
        k = _sohieu_key_entry(e)
        did = _entry_drive_id(e) or str(id(e))
        reason = cand_reason.get(did, "subject")
        refs = _relation_refs(e)
        # #6: BỎ QUA dòng đã CÁCH LY / corpus=false (bản TRÙNG đã quarantine) — KHÔNG đề xuất backfill goc/review (action vô nghĩa → nhiễu).
        if _entry_quarantined(e) or str(e.get("corpus") or "").strip().lower() == "false":
            continue
        if reason == "direct" and base_key and base_key not in refs:
            # CHỈ amendment XÁC THỰC (base liệt kê nó ở amendment_keys) mới đề xuất set_goc.
            missing_links.append({"action": "BACKFILL_GOC_ON_AMENDMENT", "drive_id": _entry_drive_id(e),
                                  "sohieu": _entry_sohieu(e), "set_goc": base})
        elif reason == "subject" and k not in eligible_keys:
            # Trùng CHỦ ĐỀ nhưng KHÔNG tham chiếu base & KHÔNG trong footnote-map → KHÔNG auto-backfill (dương tính giả #1/#3).
            subject_only_review.append({"sohieu": _entry_sohieu(e), "name": _entry_name(e)[:90],
                                        "in_footnote_map": False,
                                        "note": ("Trùng chủ đề nhưng KHÔNG có trong footnote-map của VBHN — KHÔNG ghi sua_doi/goc; xác minh nguyên văn thủ công."
                                                 if fn_keys else
                                                 "Trùng chủ đề, CHƯA tham chiếu base — xác minh nội dung thủ công, KHÔNG set_goc/sua_doi tự động.")})
    warnings = []
    if candidates:
        warnings.append("AMENDMENT_FOUND_IN_CORPUS: có văn bản sửa đổi trong corpus/NLM; không được kết luận corpus thiếu văn bản.")
    if subject_only_review:
        warnings.append("SUBJECT_ONLY_CANDIDATES: có ứng viên CHỈ trùng chủ đề (không tham chiếu base) — "
                        "KHÔNG đề xuất backfill goc/sua_doi cho chúng; phải đọc nguyên văn xác minh quan hệ trước khi kết luận.")
    if fn_keys and blocked_subject_keys:
        warnings.append("SUBJECT_ONLY_BLOCKED_BY_FOOTNOTE: ứng viên trùng chủ đề KHÔNG xuất hiện trong footnote-map của VBHN đã bị loại khỏi backfill sua_doi (footnote-map ưu tiên hơn heuristic).")
    if footnote_only_amendments:
        warnings.append("FOOTNOTE_AMENDMENT_NOT_IN_CORPUS: footnote-map của VBHN có văn bản sửa đổi CHƯA thấy trong corpus — nạp QT-5 trước khi kết luận (xem footnote_only_amendments).")
    if missing_links:
        warnings.append("RELATION_BACKFILL_REQUIRED: registry thiếu goc/sua_doi; hỏi người dùng rồi ghi registry trước khi rà soát tiếp.")
    if not vbhn:
        warnings.append("NO_VERIFIED_VBHN_IN_CORPUS: chưa thấy VBHN trong manifest; KHÔNG kết luận không có, phải chạy tìm web QT-5.")
        warnings.append("QT5_WEB_REQUIRED: chạy các truy vấn `vbhn_queries`, gồm cả nguồn secondary như Thư viện Pháp luật để phát hiện nhanh.")
    # Lọc NHIỄU khỏi amendment_candidates: ứng viên CHỈ-trùng-chủ-đề (reason=subject, KHÔNG trong eligible/footnote) đã nằm
    # trong subject_only_review rồi — đừng lặp lại như "ứng viên sửa đổi" (dương-tính-giả: vd 108/2026 với BLLĐ, Luật
    # Thanh niên/Công đoàn theo cụm chủ đề quá rộng). Backfill-gate KHÔNG đổi (chỉ lọc DANH SÁCH HIỂN THỊ).
    def _is_subject_noise(e):
        did = _entry_drive_id(e) or str(id(e))
        return cand_reason.get(did, "subject") == "subject" and _sohieu_key_entry(e) not in eligible_keys
    real_amend = [e for e in candidates if not _is_subject_noise(e)]
    subject_noise_n = len(candidates) - len(real_amend)
    if subject_noise_n:
        warnings.append(f"SUBJECT_ONLY_FILTERED: lọc {subject_noise_n} ứng viên CHỈ-trùng-chủ-đề (không tham chiếu base, không trong "
                        "footnote-map) KHỎI amendment_candidates → chỉ còn ở subject_only_review (giảm dương-tính-giả kiểu 108/2026).")
    out = {
        "ok": True,
        "base": base or None,
        "base_key": base_key or None,
        "subject": subject or None,
        "amendment_keys": sorted(amendment_keys),
        "base_entries": [_summ_entry(e) for e in sorted(base_entries, key=_entry_score, reverse=True)],
        "amendment_candidates": [{"entry": _summ_entry(e), "flags": _relation_candidate_flags(e, base_key, subject)} for e in real_amend[:20]],
        "amendment_candidates_subject_filtered_count": subject_noise_n,
        "vbhn_candidates": [{"entry": _summ_entry(e), "flags": _vbhn_quality_flags(e, subject, {base_key} if base_key else set(), "")} for e in vbhn[:20]],
        "missing_links": missing_links,
        "subject_only_review": subject_only_review,
        "footnote_gate": bool(fn_keys),
        "footnote_amend_keys": sorted(fn_keys),
        "footnote_only_amendments": footnote_only_amendments,
        "blocked_subject_only": blocked_subject_keys,
        "warnings": warnings,
        "vbhn_queries": _qt5_queries(subject, base, ""),
        "google_discovery": _discovery_links(subject or base or "")["links_markdown"],
    }
    # P1-5 (v1.31.0): vocab thống nhất họ QT-5 {verdict, flags, qt5_queries, google_discovery} — driver batch hết
    # đặc-cách từng lệnh. Giữ vbhn_queries (compat). Verdict cùng vocab vbhn-check: REVIEW khi cần người xử
    # (missing_links/footnote-thiếu-corpus/subject-only) · QT5_WEB_REQUIRED khi chưa thấy VBHN · OK còn lại.
    out["qt5_queries"] = out["vbhn_queries"]
    out["flags"] = _warning_codes(warnings)
    out["verdict"] = ("REVIEW" if (missing_links or footnote_only_amendments or subject_only_review)
                      else ("QT5_WEB_REQUIRED" if not vbhn else "OK"))
    return out


def _entry_sohieu(e: dict) -> str:
    return e.get("so_hieu") or e.get("sohieu") or e.get("soHieu") or ""


def _entry_drive_id(e: dict) -> str:
    return e.get("drive_id") or e.get("driveId") or e.get("gdoc_id") or e.get("id") or ""


def _entry_cat(e: dict) -> str:
    return str(e.get("cat") or e.get("path") or "")


def _entry_nlm(e: dict) -> str:
    return e.get("nlm_source_id") or e.get("nlmSourceId") or ""


def _entry_nlm_notebook_id(e: dict) -> str:
    return str(e.get("nlm_notebook_id") or e.get("notebook_id") or "").strip()


def _entry_corpus_true(e: dict) -> bool:
    return str(e.get("corpus") or "").strip().lower() == "true"


def _entry_is_draft(e: dict) -> bool:
    text = " ".join(str(x or "") for x in (
        _entry_name(e), e.get("hieuluc"), e.get("hieu_luc"), e.get("status"),
        e.get("note"), e.get("verified"), e.get("title_vn"), e.get("nlm_title"),
    ))
    norm = _strip_accents(text).lower()
    return (
        _entry_name(e).upper().startswith("DUTHAO_")
        or "du thao" in norm
        or "draft" in norm
        or "chua hieu luc" in norm
        or "chua co hieu luc" in norm
    )


_NLM_REMOVED_STATUS = {"removed", "removed_from_drive", "deleted", "trash", "trashed"}


def _nlm_status_removed(status: str) -> bool:
    """HỌ status 'đã gỡ': mọi biến thể tiền tố `removed*` (removed_superseded_by_VBHN, removed_dedup…) + deleted/trash*.
    Trước đây check exact-set → biến thể removed_* bị coi NHẦM là 'còn sống' (lệch still_on_nlm/ghost)."""
    s = (status or "").strip().lower()
    return s.startswith("removed") or s.startswith("trash") or s == "deleted"


def _nlm_display(e: dict) -> str:
    """Hiển thị NLM STATUS-AWARE (đồng bộ locate ↔ reg-query): '-' không có source; 'removed' có source nhưng đã gỡ;
    'Y' đang sống. Trước đây locate in nlm=Y dù nlm_status=removed → lệch với reg-query (báo removed)."""
    if not _entry_nlm(e):
        return "-"
    return "removed" if _nlm_status_removed(str(e.get("nlm_status") or "")) else "Y"


def _entry_on_nlm_live(e: dict) -> bool:
    """CÓ trên NLM THẬT (live): có source_id VÀ status KHÔNG phải removed/deleted. B5: relation-check/_summ_entry trước
    in nlm=True chỉ vì có source_id (dù đã gỡ) → lệch reg-query (removed). Dùng cái này để 2 lệnh nhất quán."""
    return bool(_entry_nlm(e)) and not _nlm_status_removed(str(e.get("nlm_status") or ""))


def _entry_date_text(e: dict) -> str:
    for k in ("ngay_ban_hanh", "ngayBanHanh", "ngaybanhanh", "issued_date", "issue_date", "date", "ngay", "ban_hanh"):
        v = e.get(k)
        if v:
            return str(v)
    return ""


def _entry_issue_date_iso(e: dict | None) -> str | None:
    """(port Codex hotfix) Ngày ban hành ISO yyyy-mm-dd nếu metadata đủ rõ; None khi chỉ có năm/text mơ hồ.
    Dùng cho cổng date-coverage: hạ PAUSE khi VBHN ban hành KHÔNG sớm hơn mọi luật-sửa có ngày rõ."""
    s = _entry_date_text(e or {})
    if not s:
        return None
    s = unicodedata.normalize("NFC", str(s))
    m = re.search(r"\b(20\d{2}|19\d{2})\s*[-/.]\s*(\d{1,2})\s*[-/.]\s*(\d{1,2})\b", s)
    if m:
        return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    m = re.search(r"\b(\d{1,2})\s*[/\-.]\s*(\d{1,2})\s*[/\-.]\s*(20\d{2}|19\d{2})\b", s)
    if m:
        return f"{int(m.group(3)):04d}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"
    low = _strip_accents(s).lower()
    m = re.search(r"\bngay\s+(\d{1,2})\s+thang\s+(\d{1,2})\s+nam\s+(20\d{2}|19\d{2})\b", low)
    if m:
        return f"{int(m.group(3)):04d}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"
    return None


def _year_from_text_safe(text: str) -> int | None:
    """Suy năm ban hành một cách an toàn.

    Không lấy năm bất kỳ trong title/từ khóa, vì VBHN thường chứa số hiệu luật gốc
    như 84/2015/QH13 hoặc 22/2019/TT-BYT. Những năm đó KHÔNG phải issue_year
    của văn bản hợp nhất. Chỉ nhận năm khi có ngữ cảnh ngày ban hành/năm ban hành
    hoặc năm tách rõ trong tên file/metadata chuyên biệt.
    """
    txt = unicodedata.normalize("NFC", str(text or ""))
    pats = [
        r"(?:ngày|ngay)\s+\d{1,2}\s*(?:/|-|\s+tháng\s+|\s+thang\s+)\s*\d{1,2}\s*(?:/|-|\s+năm\s+|\s+nam\s+)(19\d{2}|20\d{2})",
        r"(?:năm|nam|issue[_\s-]*year|issued[_\s-]*year|nam[_\s-]*ban[_\s-]*hanh)\D{0,8}(19\d{2}|20\d{2})",
        r"(?:^|[_\s.-])(19\d{2}|20\d{2})(?=$|[_\s.-])",
    ]
    low = _strip_accents(txt).lower()
    for pat in pats:
        m = re.search(pat, low, re.I)
        if m:
            return int(m.group(1))
    return None


_GOC_TAIL_RE = re.compile(r"[_\s.\-]goc[_\s.\-].*$", re.I)


_GOC_BASE_RE = re.compile(r"[_\s.\-]goc[_\s.\-]+([0-9]+[-/_][0-9A-Za-z][-/_0-9A-Za-z]*)", re.I)


def _vbhn_goc_corroborated(vbhn_entry: dict, qkey: str, query_subject: str = "") -> bool:
    """§1.1 (log rà 108 lần): chống registry.goc bị NHIỄM khiến source-map/status redirect VBHN-first SANG SAI văn bản.
    Ca thật: VBHN 'Bảo vệ sức khỏe nhân dân' (tên goc_21-LCT-HDNN8) bị registry.goc=113-2025 (Luật Dân số) → query
    Dân số redirect nhầm sang VBHN Bảo vệ sức khỏe. True chỉ khi quan hệ goc=qkey được CORROBORATE:
      • tên VBHN mã hoá base (goc_<base>) phải KHỚP qkey (nếu tên có mã hoá), VÀ
      • chủ đề truy vấn KHÔNG xung khắc lĩnh vực với chủ đề VBHN (BHXH↔BHYT…).
    Tên không mã hoá base + không xung khắc chủ đề → vẫn tin registry.goc (giữ tương thích VBHN chưa đặt tên goc_)."""
    name_base = _name_goc_base_key(_entry_name(vbhn_entry))
    if name_base and qkey and name_base != qkey:
        return False
    if query_subject and _disc_conflict(query_subject, _entry_subject_text(vbhn_entry)):
        return False
    return True


def _entry_issue_year(e: dict) -> int | None:
    # issue_year_goc_token: VBHN — năm BẢN GỐC cũ nhất trong chuỗi goc KHÔNG bao giờ là năm ban hành của bản hợp nhất.
    # (vd VBHN_123 ban hành 2025 nhưng issue_year/tên file dính '64-2020' của luật gốc PPP → trước trả 2020 sai.)
    base_goc_year = None
    if _is_vbhn_entry(e):
        _bk = _vbhn_base_key(e)
        base_goc_year = _sohieu_year(_bk) if _bk else None

    def _reject(y: int | None) -> bool:
        return y is not None and base_goc_year is not None and y == base_goc_year

    # 1) Chỉ tin các trường chuyên biệt trước (bỏ nếu trùng năm bản gốc của VBHN — bị nhiễm).
    explicit = e.get("issue_year") or e.get("issued_year") or e.get("year") or e.get("nam") or e.get("nam_ban_hanh")
    if explicit:
        y = _year_from_text_safe(str(explicit))
        if y and not _reject(y):
            return y
        if not y:
            m0 = re.fullmatch(r"\s*(19\d{2}|20\d{2})\s*", str(explicit))
            if m0 and not _reject(int(m0.group(1))):
                return int(m0.group(1))

    # 2) Ngày ban hành là nguồn an toàn — TIN tuyệt đối (không reject theo năm gốc).
    y = _year_from_text_safe(_entry_date_text(e))
    if y:
        return y

    # 3) Tên file/nhan đề NLM có năm tách bằng _ . - hoặc khoảng trắng. BỎ token 'goc_...' trước khi tách năm
    # (năm trong token goc là năm bản gốc, không phải VBHN). Không đọc tukhoa/keywords/trich yếu tự do.
    for text in (_entry_name(e), e.get("nlm_title"), e.get("title_vn")):
        y = _year_from_text_safe(_strip_goc_token(text))
        if y and not _reject(y):
            return y
    return None


def _is_vbhn_entry(e: dict) -> bool:
    txt = " ".join(str(x or "") for x in (_entry_sohieu(e), e.get("loai"), _entry_name(e))).upper()
    return "VBHN" in txt or "VAN BAN HOP NHAT" in _strip_accents(txt).upper()


def _vbhn_metadata_flags(e: dict, tail: str) -> list[str]:
    if not _is_vbhn_entry(e):
        return []
    flags = []
    issue_year = _entry_issue_year(e)
    raw = norm_sohieu(_entry_sohieu(e) or "")
    name = _entry_name(e)
    sh_key = _sohieu_key_entry(e)
    # v1.29.6 (log 118 Luật — P2.2: VBHN_NUMBER_REUSE_RISK nổ trên MỌI VBHN kể cả bản ĐÃ CÓ NĂM trong sohieu-key
    # như VBHN_133-2025 → kéo TITLE_OR_REGISTRY_WARN nhiễu 24×): sohieu-key dạng chuẩn NN-YYYY-VBHN-XXX = năm ĐÃ
    # XÁC ĐỊNH (bất biến đặt tên) → coi như biết năm, KHÔNG cờ thiếu-năm dù _entry_issue_year không suy được.
    _key_m = _VBHN_WITHYEAR_RE.fullmatch(sh_key or "")
    _key_year = int(_key_m.group(2)) if _key_m else None
    _known_years = {y for y in (issue_year, _key_year) if y}
    # B4 (v1.33.0 — log rà 15: ca 25-2025 'Luat_Ke_toan' bị coi TÊN TRƠ → kéo REUSE_RISK + TITLE_WARN oan):
    # _token_set bỏ 'luat' (stop-word) + 'ke' (ngắn) nên tail CÓ chủ đề vẫn đếm <2. Fallback: đếm TỪ-CHỮ ≥2 ký tự
    # trong tail — 'luat ke toan' = 3 từ = có chủ đề; tail rỗng/'hopnhat' đơn độc vẫn là trơ đúng.
    if len(_token_set(tail)) < 2 and len(re.findall(r"[a-z]{2,}", _ascii_lower(tail))) < 2:
        flags.append("VBHN_BARE_NUMBER")
    if not _known_years:
        flags.append("VBHN_MISSING_YEAR_OR_DATE")
    agency = _vbhn_agency_from_key(sh_key)
    if re.fullmatch(r"\d{1,4}-VBHN-VPQH", raw) and "VBHN" not in str(_entry_sohieu(e) or "").upper():
        flags.append("VBHN_SOHIEU_NORMALIZED_FROM_SHORT_VPQH")
    _year_in_name = any(re.search(rf"(?<!\d){y}(?!\d)", name or "") for y in _known_years)
    if _known_years and not _year_in_name:
        flags.append("VBHN_NAME_MISSING_YEAR")
    if agency and agency != "VPQH":
        flags.append("VBHN_MINISTRY_SCOPE")
        if not _known_years:
            flags.append("VBHN_MINISTRY_MISSING_YEAR")
        elif not _year_in_name:
            flags.append("VBHN_MINISTRY_NAME_MISSING_YEAR")
    return flags


# BẤT BIẾN: số hiệu VBHN PHẢI có NĂM (số VBHN tái dùng theo năm → collision). Chuẩn = NN-YYYY-VBHN-XXX.
_VBHN_NOYEAR_RE = re.compile(r"^(\d{1,5})-VBHN-([A-Z0-9D]+)$")            # NN-VBHN-XXX (THIẾU năm)
_VBHN_WITHYEAR_RE = re.compile(r"^(\d{1,5})-(19\d{2}|20\d{2})-VBHN-([A-Z0-9D]+)$")


def _vbhn_sohieu_inject_year(sohieu_key: str, year) -> str | None:
    """`61-VBHN-VPQH` + 2025 → `61-2025-VBHN-VPQH`. None nếu sohieu KHÔNG phải VBHN-thiếu-năm hoặc year rỗng/sai."""
    m = _VBHN_NOYEAR_RE.fullmatch(norm_sohieu(sohieu_key or ""))
    try:
        y = int(year)
    except (TypeError, ValueError):
        return None
    if not m or not (1900 <= y <= 2100):
        return None
    return f"{m.group(1)}-{y}-VBHN-{m.group(2)}"


def _name_inject_vbhn_year(name: str, number: str, year, agency: str) -> str:
    """Chèn năm vào token số-VBHN trong TÊN (chịu / - _ phân tách); idempotent (đã có năm → giữ nguyên).
    v1.33.21: nhận CẢ dạng NGẮN `NN-VPQH` (thiếu segment VBHN — ca thật 'VBHN_34-VPQH_Luat_Luu_tru': trước trả
    nguyên tên → lane name-only câm với đúng lớp cần sửa nhất)."""
    if not name or not year:
        return name
    pat = re.compile(rf"(?<!\d){re.escape(str(number))}([/_-])VBHN([/_-]){re.escape(str(agency))}(?![A-Za-z0-9])")
    out = pat.sub(rf"{number}\g<1>{year}\g<1>VBHN\g<2>{agency}", name)
    if out != name:
        return out
    # dạng NGẮN 'NN-VPQH' (không có 'VBHN' giữa) → chuẩn hoá thẳng về NN-YYYY-VBHN-XXX
    pat2 = re.compile(rf"(?<!\d){re.escape(str(number))}([/_-]){re.escape(str(agency))}(?![A-Za-z0-9])")
    return pat2.sub(rf"{number}\g<1>{year}\g<1>VBHN\g<1>{agency}", name)


_STOP_TOKENS = {
    "luat", "bo", "nghi", "dinh", "thong", "tu", "quyet", "dinh", "van", "ban",
    "hop", "nhat", "vbhn", "qh", "vpqh", "cp", "tt", "bqp", "ubtvqh", "docx",
    "pdf", "goc", "raw", "final", "copy", "ve", "cua", "va", "cac", "mot", "so",
}
_OMNIBUS_TITLE_HINTS = (
    "sua doi", "bo sung", "mot so dieu", "mot so luat", "nhieu luat",
    "quy hoach", "dau tu", "dau thau", "ppp", "doi tac cong tu", "luat khac",
)


_META_TITLE_KEYS = (
    "title_vn", "nlm_title", "trich_yeu", "mo_ta", "description",
    "official_title", "ten", "ten_van_ban",
)
_REF_KEYS = (
    "goc", "sua_doi", "sua_doi_bo_sung", "sdbs", "supersedes",
    "targets", "target_sohieu", "related", "relations",
)


# Viết tắt pháp lý phổ biến → dạng đầy đủ (tên file VBHN HAY viết tắt: 'BHXH', 'BLHS'…). Khớp chủ đề phải nhận
# 'BHXH' ≡ 'bảo hiểm xã hội', nếu không source-map/relation-check bỏ sót VBHN viết-tắt (VBHN_19…BHXH) và nhặt bản
# gốc viết-đầy-đủ (41/2024…Bao_hiem_xa_hoi) đã quarantine. ASCII không dấu, key là token đứng-một-mình.
_ABBREV_MAP = {
    "bhxh": "bao hiem xa hoi", "bhyt": "bao hiem y te", "bhtn": "bao hiem that nghiep",
    "bluat": "bo luat",   # P1-3 v1.33.12: prefix chuẩn sinh-tự-động của standardize_name
    "blhs": "bo luat hinh su", "blld": "bo luat lao dong", "blds": "bo luat dan su",
    "bltths": "bo luat to tung hinh su", "blttds": "bo luat to tung dan su",
    "atvsld": "an toan ve sinh lao dong", "kdbh": "kinh doanh bao hiem",
    "tnld": "tai nan lao dong", "bnn": "benh nghe nghiep", "nsnn": "ngan sach nha nuoc",
    "ppp": "doi tac cong tu", "doi tac cong tu": "ppp",
    # N2 (v1.31.1 — bài học #2 log phiên rà 68 Luật): viết tắt trong TÊN FILE làm cross-check token FALSE-REJECT
    # bản đúng ('CNTT' ∌ token 'cong nghe thong tin') → bổ sung các viết tắt phổ biến còn thiếu.
    "cntt": "cong nghe thong tin", "pcth": "phong chong tac hai", "pccc": "phong chay chua chay",
    "hnvgd": "hon nhan va gia dinh", "gtvt": "giao thong van tai", "khcn": "khoa hoc cong nghe",
    # D2 (v1.33.3 — log rà 66×3: 87/2015 'HD_giam_sat_QH_HDND' FAIL title-check vì 'hdnd' không bao giờ xuất
    # hiện nguyên dạng trong header viết đầy đủ): viết tắt CƠ QUAN DÂN CỬ/đoàn thể còn thiếu.
    "hdnd": "hoi dong nhan dan", "ubnd": "uy ban nhan dan", "mttq": "mat tran to quoc",
    # S-2e (v1.33.15 — log rà 40: ND_47-2024 'CSDL_Quoc_gia' + TT_95-2025 'uu_dai_NCC' FAIL title-check vì
    # viết tắt không có trong map): bổ sung viết tắt còn thiếu gặp trong corpus thật.
    "csdl": "co so du lieu", "ncc": "nguoi co cong",
    # B.2 (v1.33.19 — log rà v1.33.18: GDDH khớp 0/1, BH_VBQPPL khớp 0/1 — title-check fail oan dù
    # sohieu/loai/cat đều PASS): viết tắt giáo dục + VBQPPL trong tên chuẩn.
    "gddh": "giao duc dai hoc", "gdnn": "giao duc nghe nghiep",
    "vbqppl": "van ban quy pham phap luat",
    # v1.33.20 (MERGE bundle-20): thêm họ hàng cùng lớp — 'bh' đứng-một-mình theo quy ước tên corpus = Ban hành
    # (bảo hiểm luôn viết BHXH/BHYT/KDBH dài hơn); expansion chỉ APPEND token nên rủi ro = 0 thay thế.
    "gdpt": "giao duc pho thong", "bh": "ban hanh", "qppl": "quy pham phap luat",
}
_ABBREV_RE = re.compile(r"(?<![a-z])(" + "|".join(_ABBREV_MAP) + r")(?![a-z])")


def _expand_abbrev(text: str) -> str:
    """Nối thêm dạng ĐẦY ĐỦ của viết tắt pháp lý vào text (KHÔNG thay thế → không phá token khác). 'Luat BHXH' →
    'Luat BHXH bao hiem xa hoi'. Dùng trong _token_set + _disc_conflict để khớp chủ đề bất kể viết tắt/đầy đủ."""
    low = _strip_accents(str(text or "")).lower()
    extra = [_ABBREV_MAP[m] for m in dict.fromkeys(_ABBREV_RE.findall(low))]
    return (str(text or "") + " " + " ".join(extra)) if extra else str(text or "")


_NAME_CODE_TOK = re.compile(r"^[a-z]+\d+$")   # token mã số hiệu dính chữ-số: qh15, qh13, tt09…


def _entry_query_match(q: str, e: dict, include_subject: bool = False) -> bool:
    """Một điểm vào chung cho locate/source-map/reg-query/hygiene query matching."""
    qkey = norm_sohieu(q.replace("_", "-")) if _looks_like_sohieu_query(q) else ""
    if qkey and _sohieu_key_entry(e) == qkey:
        return True
    hay = _entry_subject_text(e) if include_subject else _entry_name(e)
    qn, hn = _strip_accents(q).lower(), _strip_accents(hay).lower()
    qnk, hnk = _name_key(q), _name_key(hay)
    return bool(
        (qn and qn in hn)
        or (qnk and hnk and (qnk in hnk or hnk in qnk))
        or _name_subset_match(q, hay)
        or _name_phrase_match(q, hay)
    )


def _entry_query_match_safe_for_hygiene(q: str, e: dict) -> bool:
    """Query match cho hygiene: không để tên hẹp/sai kéo omnibus vào plan chủ đề hẹp.

    Nếu query là số hiệu chính xác thì vẫn cho qua để người vận hành soi văn bản đó.
    Với query chủ đề/tên, bản có OMNIBUS_NARROW_TITLE_CHECK hoặc TITLE_METADATA_MISMATCH
    phải khớp cả metadata tiêu đề, không chỉ filename bị đặt nhầm.
    """
    qkey = norm_sohieu(q.replace("_", "-")) if _looks_like_sohieu_query(q) else ""
    if qkey and _sohieu_key_entry(e) == qkey:
        return True
    if not _entry_query_match(q, e, include_subject=False):
        return False
    flags = set(_title_flags(e))
    if (not _is_vbhn_entry(e)) and (flags & {"OMNIBUS_NARROW_TITLE_CHECK", "TITLE_METADATA_MISMATCH"}):
        meta = _field_text(e, _META_TITLE_KEYS)
        return bool(meta and _entry_query_match(q, {"name": meta}, include_subject=False))
    return True


def _field_text(e: dict, keys: tuple[str, ...]) -> str:
    vals = []
    for k in keys:
        v = e.get(k)
        if isinstance(v, (list, tuple, set)):
            vals.extend(str(x) for x in v if x)
        elif isinstance(v, dict):
            vals.extend(str(x) for x in v.values() if x)
        elif v:
            vals.append(str(v))
    return " ".join(vals)


# P2-7 (log rà 71 luật): chuẩn hoá ENUM `loai`/`hieuluc` — registry hiện lẫn Luật/Luat, Văn bản hợp nhất/VBHN,
# Nghị định/nghi_dinh/ND/nd; hieuluc=Con/Còn → lọc/đếm theo loại KHÔNG tin cậy. Chuẩn hoá lúc register + cờ
# hygiene LOAI_NONCANONICAL (bucket riêng, KHÔNG nhét _title_flags để tránh nhiễu source-map/risky).
_LOAI_CANON = {
    "luat": "Luật", "bo luat": "Bộ luật", "bluat": "Bộ luật", "bo_luat": "Bộ luật",
    "van ban hop nhat": "Văn bản hợp nhất", "vbhn": "Văn bản hợp nhất", "vanbanhopnhat": "Văn bản hợp nhất",
    "nghi dinh": "Nghị định", "nd": "Nghị định", "nghidinh": "Nghị định",
    "thong tu": "Thông tư", "tt": "Thông tư", "thongtu": "Thông tư",
    "thong tu lien tich": "Thông tư liên tịch", "ttlt": "Thông tư liên tịch",
    "nghi quyet": "Nghị quyết", "nq": "Nghị quyết", "nghiquyet": "Nghị quyết",
    "quyet dinh": "Quyết định", "qd": "Quyết định", "quyetdinh": "Quyết định",
    "phap lenh": "Pháp lệnh", "pl": "Pháp lệnh", "phaplenh": "Pháp lệnh",
    "ket luan": "Kết luận", "kl": "Kết luận", "chi thi": "Chỉ thị", "ct": "Chỉ thị",
    "hien phap": "Hiến pháp", "hp": "Hiến pháp", "lenh": "Lệnh",
    # v1.30.1 (#4): Công điện = họ tên-chuẩn từ v1.29.4 (CD_32-2026-CD-TTg) nhưng THIẾU trong enum → dòng
    # loai='Công điện' bị đếm phi-chuẩn vĩnh viễn + --normalize không map được. Review CONFIRMED: 'cd' trần
    # CŨNG phải map (CD ∈ họ canonical dòng _canon_fams; nhất quán nd/tt/nq/qd/kl/ct đã có; 'CĐ'→'cd' sau norm).
    "cong dien": "Công điện", "congdien": "Công điện", "cd": "Công điện",
    # A4 (v1.32.0 — log rà 77 Luật): công ước ILO/điều ước mang loai='Điều ước quốc tế' HỢP LỆ nhưng thiếu trong
    # enum → 56 dòng đếm nonmappable/loai_noncanonical GIẢ mỗi lần sweep/backfill. Thêm cả 2 giá trị canonical.
    "dieu uoc quoc te": "Điều ước quốc tế", "dieu uoc": "Điều ước quốc tế", "dieuuoc": "Điều ước quốc tế",
    "cong uoc": "Công ước", "conguoc": "Công ước",
}
_LOAI_CANON_VALUES = set(_LOAI_CANON.values())


def _normalize_hieuluc(s: str) -> str:
    """Map biến thể `hieuluc` → {Còn, Hết, Chưa} (giữ nguyên ngày/chuỗi khác nếu không nhận diện trạng thái trần)."""
    raw = str(s or "").strip()
    if not raw:
        return raw
    k = _strip_accents(raw).lower()
    if k in ("con", "con hieu luc", "conhieuluc"):
        return "Còn"
    if k in ("het", "het hieu luc", "hethieuluc", "thay the", "da thay the", "bai bo", "het hl"):
        return "Hết"
    if k in ("chua", "chua hieu luc", "chuahieuluc", "pending"):
        return "Chưa"
    return raw      # ngày/chuỗi cụ thể (vd '01/07/2026') → giữ nguyên


_FLAG_REASONS = {
    "RAW_NAME_NOT_NLM": "bản thô (chưa GDoc/NLM) cạnh bản canonical",
    "CORPUS_TRUE_NOT_ON_NLM": "corpus=true nhưng chưa có nguồn NLM live",
    "NLM_STATUS_MISMATCH": "nlm_status lệch trạng thái thực (registry hygiene)",
    "NLM_NOTEBOOK_ID_MISSING": "trên NLM nhưng thiếu nlm_notebook_id",
    "NLM_GHOST_SOURCE": "nguồn NLM rỗng (không tên/số hiệu)",
    "ORPHAN_CAT": "thiếu folder chủ đề hợp lệ",
    "MISSING_SOHIEU": "chưa có số hiệu chuẩn",
    "DRAFT_NOT_EFFECTIVE": "là DỰ THẢO, chưa hiệu lực",
    "OMNIBUS_NARROW_TITLE_CHECK": "tên hẹp nhưng quan hệ sửa nhiều luật (omnibus)",
    "TITLE_METADATA_MISMATCH": "tên file lệch metadata quan hệ",
    "VBHN_BARE_NUMBER": "VBHN tên trơ, thiếu năm/cơ quan",
    "VBHN_MISSING_YEAR_OR_DATE": "VBHN thiếu năm trong số hiệu/tên",
    "VBHN_NAME_MISSING_YEAR": "tên VBHN thiếu năm ban hành",
    "VBHN_NAME_MISSING_SUBJECT": "tên VBHN thiếu chủ đề",
    "VBHN_MINISTRY_SCOPE": "VBHN cấp Bộ — cần năm + xử lý riêng",
    "VBHN_MINISTRY_MISSING_YEAR": "VBHN cấp Bộ thiếu năm trong số hiệu",
    "VBHN_MINISTRY_NAME_MISSING_YEAR": "VBHN cấp Bộ thiếu năm trong tên",
    "VBHN_SOHIEU_NORMALIZED_FROM_SHORT_VPQH": "số hiệu VBHN suy từ dạng rút gọn -VPQH",
    "VBHN_YEAR_NOT_IN_METADATA": "năm VBHN không thấy trong metadata",
    "SUBJECT_NOT_EVIDENT_IN_METADATA": "metadata không thể hiện rõ chủ đề",
    "GOC_NOT_EVIDENT_IN_METADATA": "metadata không dẫn-chiếu văn bản gốc đã cho",
}


def _flags_reason(flags: list) -> str:
    """Diễn giải NGẮN GỌN cho mỗi cờ rủi ro (vá log: risky_candidates trước đây trống trường lý do)."""
    parts = [_FLAG_REASONS.get(f, f) for f in (flags or [])]
    return "; ".join(dict.fromkeys(parts))


# A2: NHÃN QUARANTINE CHUẨN DUY NHẤT = tên folder Drive thật. Mọi đường GHI nên dùng hằng này; mọi đường ĐỌC/AUDIT
# dùng `_is_quarantine_cat` (nhận MỌI biến thể: 'QUARANTINE' code cũ, '_ZZZ_QUARANTINE_taluat' folder) → audit hội tụ
# dù nhãn lệch. `quarantine_label_variants` trong hygiene scan bắt dòng còn nhãn cũ để chuẩn hoá dần.
QUARANTINE_CAT = "_ZZZ_QUARANTINE_taluat"


def _is_quarantine_cat(cat: str) -> bool:
    """A1: nhận diện cat cách ly/loại bỏ (MỌI biến thể: code 'QUARANTINE', folder `_ZZZ_QUARANTINE_taluat`) →
    KHÔNG cho thắng canonical + audit hội tụ bất kể nhãn."""
    c = _strip_accents(str(cat or "")).lower()
    return ("quarantine" in c) or ("zzz" in c)


def _is_quarantine_label_variant(cat: str) -> bool:
    """A2: dòng ĐÃ quarantine nhưng nhãn KHÁC chuẩn QUARANTINE_CAT (vd code 'QUARANTINE' trơ) → nên chuẩn hoá."""
    c = str(cat or "").strip()
    return _is_quarantine_cat(c) and c != QUARANTINE_CAT


def _entry_quarantined(e: dict) -> bool:
    """#6: dòng đã CÁCH LY — nằm trong cat quarantine, HOẶC corpus=false & không còn trên NLM (bản trơ bị guard loại).
    Dùng để KHÔNG nhồi các dòng đã xử lý vào WARN/risky (giảm nhiễu); chúng vẫn hiện ở direct_hits."""
    if _is_quarantine_cat(_entry_cat(e)):
        return True
    return str(e.get("corpus") or "").strip().lower() == "false" and not _entry_nlm(e)


def _entry_score(e: dict) -> int:
    """Heuristic chọn canonical: không cho nguồn NLM mồ côi/bản quarantine thắng.
    A1: VBHN-first áp cho CẢ truy vấn theo tên — phạt nặng quarantine/orphan, thưởng VBHN có 'goc' + còn hiệu lực."""
    score = 0
    name = _entry_name(e)
    sohieu = _entry_sohieu(e) or _parse_sohieu_from_name(name)
    cat = _entry_cat(e)
    ghost = _entry_nlm(e) and (not name) and (not sohieu) and _bad_cat(cat)
    if _entry_nlm(e) and not ghost:
        score += 50
    if ghost:
        score -= 500
    elif _entry_nlm(e) and (not name or not sohieu) and _bad_cat(cat):
        score -= 200
    elif (not sohieu) and _bad_cat(cat):
        score -= 80
    # A1: bản trong _ZZZ_QUARANTINE KHÔNG được làm canonical kể cả khi truy vấn theo tên chủ đề.
    if _is_quarantine_cat(cat):
        score -= 400
    # P0-1 (log rà): file THÔ (.docx/.pdf/.html) CHƯA trên NLM KHÔNG được thắng bản GDoc native cùng số hiệu
    # (vd VBHN có sidecar .docx). Phạt CHỈ khi sidecar CHƯA push NLM (raw đã-push NLM = canonical thật, vd PDF
    # gốc đã nạp → KHÔNG phạt, tránh hạ oan bản raw-only hợp lệ). Sidecar đúng nghĩa luôn ngoài NLM → vẫn bị hạ.
    if _is_raw_no_gdoc_name(name) and not _entry_nlm(e):
        score -= 300
    if _is_vbhn_entry(e):
        score += 20
        if _goc_keys(e):           # VBHN-first: hợp nhất có gốc → ưu tiên rõ rệt
            score += 35
    if sohieu: score += 25
    cat_l = str(cat or "").lower()
    if cat_l and "root" not in cat_l and cat_l not in ("", "(root)") and not _is_quarantine_cat(cat):
        score += 15
    hl = str(e.get("hieuluc") or e.get("hieu_luc") or "").lower()
    if "còn" in hl: score += 8
    if "hết" in hl or "thay thế" in hl or "het" in _strip_accents(hl): score -= 30
    if str(e.get("corpus", "")).lower() == "true": score += 5
    if str(e.get("trashed", "")).lower() == "true": score -= 100
    return score


# ── (HỢP NHẤT Codex v1.22.69) DEEP-RESOLVER cho lệnh ĐỌC SÂU (extract/xref/footnote-map) ──────────────
# Mạnh hơn `_canonical_for_query` cho đường đọc: ƯU TIÊN GDoc native (mime) + corpus + live, PHẠT NẶNG raw/
# quarantine; LUÔN thử by-name (tên DÀI toàn chữ-gạch-dưới như 'Luat_Phong_chong_benh_truyen_nhiem' KHÔNG còn bị
# regex nhận nhầm là DriveId → hết 404 giả = bug C trọn vẹn). Tách riêng để KHÔNG đụng source-map/locate.
def _entry_mime(e: dict) -> str:
    return str(e.get("mime") or e.get("mimeType") or e.get("mime_type") or "").strip().lower()


def _entry_google_doc(e: dict) -> bool:
    if not _entry_drive_id(e):
        return False
    mime = _entry_mime(e)
    return ("application/vnd.google-apps.document" in mime) or (not mime and not _is_raw_no_gdoc_name(_entry_name(e)))


def _entry_raw_no_gdoc(e: dict) -> bool:
    """Entry KHÔNG đọc-sâu được (chưa GDoc native): tên có đuôi .docx/.pdf/.html HOẶC mime thô (word/pdf/html/rtf/odt)."""
    mime = _entry_mime(e)
    if _is_raw_no_gdoc_name(_entry_name(e)):
        return True
    return bool(mime and "application/vnd.google-apps.document" not in mime and any(
        x in mime for x in ("word", "pdf", "html", "rtf", "text", "opendocument")))


def _deep_entry_rank(e: dict) -> int:
    """Điểm chọn target ĐỌC SÂU: GDoc native +80, corpus +35, NLM-live +20, có drive_id +20; raw −900, quarantine −700."""
    score = _entry_score(e)
    if _entry_drive_id(e):
        score += 20
    else:
        score -= 1000
    if _entry_corpus_true(e):
        score += 35
    if _entry_on_nlm_live(e):
        score += 20
    if _entry_google_doc(e):
        score += 80
    if _entry_raw_no_gdoc(e):
        score -= 900
    if _entry_quarantined(e):
        score -= 700
    return score


def _resolve_deep_target(target: str, entries: list[dict]) -> tuple[dict | None, str, str, list[dict]]:
    """Resolve target (gdocId|số hiệu|tên) cho lệnh đọc sâu → (entry tốt nhất, gid, name, danh sách ranked).
    Ưu tiên GDoc/corpus/live thay vì sidecar raw/quarantine. Trả (None,target,target,[]) nếu không có hit."""
    target = str(target or "").strip()
    if not target:
        return None, "", "", []
    cands: list[dict] = []
    cands.extend([e for e in entries if _entry_drive_id(e) == target])          # khớp drive_id chính xác
    qkey = norm_sohieu(target.replace("_", "-")) if _looks_like_sohieu_query(target) else ""
    if qkey:
        cands.extend([e for e in entries if _sohieu_key_entry(e) == qkey])      # khớp số hiệu
    cands.extend([e for e, _s, _r in resolve_identity(target, entries, max_hits=8)])  # LUÔN thử theo tên/alias
    seen, uniq = set(), []
    for e in cands:
        k = _entry_drive_id(e) or id(e)
        if k in seen:
            continue
        seen.add(k); uniq.append(e)

    # v1.29.7 (log NĐ131 #2): query SỐ HIỆU có ≥2 ứng viên (chính văn + PHỤ LỤC cùng khớp '131-2021') từng chọn
    # NHẦM phụ lục (dù sohieu rỗng, tên PL_). Tie-break: (a) registry-sohieu KHỚP THẬT qkey (+150 — thắng bản chỉ
    # parse-từ-tên); (b) tên dạng PHỤ LỤC (PL_/Phu_luc đầu tên) −120 (bản PHỤ không làm canonical cho query số hiệu).
    def _rk(e):
        r = _deep_entry_rank(e)
        if qkey:
            if norm_sohieu(str(_entry_sohieu(e) or "")) == qkey:
                r += 150
            if re.match(r"^(pl|phu[\s_]?luc)[\s_\-]", _strip_accents(_entry_name(e)).lower()):
                r -= 120
        return r

    uniq.sort(key=_rk, reverse=True)
    if not uniq:
        return None, target, target, []
    best = uniq[0]
    return best, (_entry_drive_id(best) or ""), _entry_name(best), uniq


def _atomic_write_text(p, text: str):
    """v1.29.1 (audit cache-coherence): ghi file cache ATOMIC (tmp + os.replace) — process bị giết giữa write_text
    TRUNCATE để lại manifest.json cụt → boot/reads sau parse fail hoặc đọc nửa dữ liệu âm thầm."""
    tmp = Path(str(p) + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(str(tmp), str(p))


def _rebuild_manifest_index(full: dict) -> None:
    """v1.29.4 (FIX log LIVE i5 'sau source-rename lệnh kế timeout/PARSEERR tới khi boot --refresh'): bust-cache xoá
    CẢ manifest_index.json nhưng chỉ `tl boot` mới dựng lại → locate/reg-query mất index → rơi fallback webapp chậm/
    dễ timeout. Nay: MỖI lần _load_manifest_full tải manifest mới → tự DỰNG LẠI index (boot.build_index, best-effort)
    → index tự-hồi-phục, KHÔNG cần nhớ chạy boot --refresh sau mỗi lần sửa."""
    try:
        idx = _imp("boot").build_index(full)
        _atomic_write_text(_cache_file("manifest_index.json"), json.dumps(idx, ensure_ascii=False))
    except Exception:
        pass


def _load_manifest_full(refresh: bool=False) -> dict:
    """Đọc manifest đầy đủ có entries. Ưu tiên cache do `tl boot`; nếu chưa có thì tải qua webapp."""
    _profile_cache_dir().mkdir(parents=True, exist_ok=True)
    p = _cache_file("manifest.json")
    if p.exists() and not refresh:
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    g = _gas()
    head = _gas_get_retry(g, "manifest_export")     # v1.29.4 i5: đọc idempotent + retry transient (hết PARSEERR loạt)
    if head.get("ok") is False:
        return head
    if head.get("entries"):
        _atomic_write_text(p, json.dumps(head, ensure_ascii=False))
        _rebuild_manifest_index(head)   # v1.29.4 i5: index tự-hồi-phục sau bust
        return head
    mid = head.get("manifestId") or head.get("manifestFileId") or head.get("driveFileId")
    if not mid:
        rd = _gas_get_retry(g, "manifest")
        mid = rd.get("manifestFileId") or rd.get("driveFileId")
    if not mid:
        return {"ok": False, "error": "không lấy được manifestId để tải entries", "head": head}
    # R1 (nhóm-D READ gws-primary): tải manifest.json qua DIRECT-MEDIA gws (raw, KHÔNG cap 9MB webapp, nhanh hơn,
    # byte-exact) TRƯỚC; thiếu cred/lỗi → FALLBACK GAS b64 (đường cũ). CHỈ đổi đường ĐỌC file JSON — KHÔNG đụng
    # manifest_export (D2: treeHash/scan ở Apps Script) ⇒ 0 rủi ro phân kỳ. Xem tra-luat-DESIGN-nhomD-gws-primary.md.
    full = None
    try:
        _tlg = _imp("tl_gws")
        _cred = _tlg._read_gws_cred()
        if _cred:
            _dl = str(p) + ".dl"                                 # v1.29.1: tải vào TẠM — chỉ replace sau parse+validate OK
            _tlg._drive_media_download(mid, _dl, _cred)          # (streaming; kill giữa chừng KHÔNG hỏng cache đang có)
            full = json.loads(Path(_dl).read_text(encoding="utf-8"))
            # An toàn (defense-in-depth): manifest HỢP LỆ phải có entries/files/rows là LIST. Nếu KHÔNG (tải cụt/hỏng
            # mà JSON vẫn parse được, hoặc body lạ) → coi như THẤT BẠI → FALLBACK GAS (KHÔNG trả manifest rỗng âm thầm).
            if not any(isinstance(full.get(k), list) for k in ("entries", "files", "rows")):
                raise ValueError("manifest gws thiếu entries/files/rows (list) — nghi tải cụt/hỏng")
            os.replace(_dl, str(p))
    except Exception as e:
        if not getattr(_load_manifest_full, "_gws_warned", False):
            _load_manifest_full._gws_warned = True
            print(f"[manifest] gws direct-media lỗi ({type(e).__name__}: {e}) → FALLBACK GAS b64. [ẩn lặp sau]",
                  file=sys.stderr)
        full = None
    if full is None:
        d = _gas_get_retry(g, "download", fileId=mid)   # v1.29.4 i5: retry transient
        if d.get("ok") is False or not d.get("b64"):
            return {"ok": False, "error": "download manifest thất bại", "download": d, "head": head}
        try:
            full = json.loads(base64.b64decode(d["b64"]).decode("utf-8"))
        except Exception as e:
            return {"ok": False, "error": f"parse manifest JSON lỗi: {e}"}
    full["manifestId"] = mid
    full.setdefault("ok", True)
    _atomic_write_text(p, json.dumps(full, ensure_ascii=False))
    _rebuild_manifest_index(full)       # v1.29.4 i5: index tự-hồi-phục sau bust (hết PHẢI boot --refresh tay)
    return full


def _manifest_entries(refresh: bool=False) -> list[dict]:
    m = _load_manifest_full(refresh=refresh)
    if m.get("ok") is False:
        raise RuntimeError(m.get("error") or json.dumps(m, ensure_ascii=False)[:500])
    return m.get("entries") or m.get("files") or m.get("rows") or []


def _canonical_for_query(q: str, refresh: bool=False) -> tuple[dict|None, list[dict]]:
    key = norm_sohieu(q)
    qn = _strip_accents(q).lower()
    # EXACT-SỐ-HIỆU PRIORITY: khi query SUY RA được số hiệu THẬT (vd '45/2019/QH14', '18/VBHN-VPQH') thì khớp số hiệu
    # CHÍNH XÁC LUÔN thắng fuzzy by-name — chống name-collision (1 VBHN/luật khác chỉ trùng cụm tên/dẫn-chiếu thắng nhờ
    # _entry_score cao). KHÔNG đụng VBHN-first redirect (doctrine ở _source_map_one.related_vbhn).
    shkey = norm_sohieu(q.replace("_", "-")) if _looks_like_sohieu_query(q) else ""
    entries = _manifest_entries(refresh=refresh)
    hits, exact = [], []
    for e in entries:
        sh = norm_sohieu(_entry_sohieu(e))
        nm = _strip_accents(_entry_name(e)).lower()
        # Fallback: entry có sohieu RỖNG trong registry nhưng TÊN mang số hiệu (vd '114_2025_QH15_658530').
        # _sohieu_key_entry parse từ tên + .replace('_','-')→norm_sohieu (khớp '114-2025-QH15'); trả '' cho tên Mẫu_/PL_.
        is_exact = bool(shkey) and (sh == shkey or _sohieu_key_entry(e) == shkey)
        if is_exact or (key and sh == key) or (qn and qn in nm) or (key and _sohieu_key_entry(e) == key):
            hits.append(e)
            if is_exact:
                exact.append(e)
    hits.sort(key=_entry_score, reverse=True)
    exact.sort(key=_entry_score, reverse=True)
    # direct exact-sohieu LUÔN ưu tiên hơn by-name fuzzy; trong mỗi nhóm vẫn lấy _entry_score cao nhất.
    canonical = exact[0] if exact else (hits[0] if hits else None)
    return canonical, hits


_FONT_RUN_RE = re.compile(
    r"^\s*(?:Times New Roman|Arial|Calibri|Cambria|Tahoma|Verdana|Courier New|"
    r"Wingdings|\.?VnTimeH?|VNI-Times|UTM Avo)"
    r"\s*(?:[,;]\s*\d{1,3}(?:[.,]\d+)?\s*(?:pt)?)?\s*$", re.I)


def _strip_font_runs(text: str) -> str:
    """Lọc bỏ dòng RÁC chỉ chứa TÊN FONT ĐẦY ĐỦ (\"Times New Roman\", \"Arial\", \".VnTime\"...)
    do bộ export DOCX/GDoc rò run-font của ô header bảng vào text trích. Chỉ xóa dòng mà TOÀN BỘ
    nội dung là tên font ĐẦY ĐỦ (+ cỡ tùy chọn) → KHÔNG đụng nội dung pháp lý thật (\"Theo Times
    báo\", \"Arial Group\", \"UTM 48N\", dòng \"Times\"/\"Symbol\" đơn lẻ vẫn giữ). Cố ý KHÔNG dùng
    wildcard tiền-tố (UTM/VNI/SVN + .*) để tránh nuốt nội dung thật. Gọi SAU khi đọc, TRƯỚC khi trả."""
    if not text or "\n" not in text:
        return text
    return "".join(ln for ln in text.splitlines(keepends=True)
                   if not _FONT_RUN_RE.match(ln.rstrip("\r\n")))


def _find_nfc(text: str, term: str, window: int = 120) -> list[dict]:
    """Tìm chuỗi trong văn bản sau khi chuẩn hóa NFC + casefold.

    Dùng thay `grep` trần để tránh âm tính giả với tiếng Việt có dấu / tổ hợp Unicode.
    Trả về snippet từ văn bản đã NFC-normalize để phục vụ verify pháp lý.
    """
    hay = unicodedata.normalize("NFC", text or "")
    needle = unicodedata.normalize("NFC", term or "")
    if not needle:
        return []
    hay_cmp, needle_cmp = hay.casefold(), needle.casefold()
    out, start = [], 0
    while True:
        i = hay_cmp.find(needle_cmp, start)
        if i < 0:
            break
        a = max(0, i - window); b = min(len(hay), i + len(needle) + window)
        snip = hay[a:b].replace("\r", " ").replace("\n", " ")
        out.append({"pos": i, "snippet": snip})
        start = i + max(1, len(needle_cmp))
        if len(out) >= 50:
            break
    return out


_RAW_SOHIEU_RE = re.compile(
    r"\d+[-_/]\d{4}[-_/][A-Za-zĐđ]+[A-Za-z0-9Đđ]*(?:-[A-Za-zĐđ][A-Za-z0-9Đđ]*)*|"
    r"\d+[-_/]LCT[-_/]HDNN\d+|"
    r"\d+[-_/](?:\d+[-_/])?VBHN[-_/][A-Za-zĐđA-Z0-9]+|"
    r"\d+[-_/](?:VPQH|VBHN)",
    re.I,
)
_TEMPLATE_PREFIX_RE = re.compile(
    r"^(m[aã]u|mẫu|pl|phu[_\s-]*luc|phụ[_\s-]*lục|phuluc|appendix|bieu[_\s-]*mau|biểu[_\s-]*mẫu)[_\s.-]*\d{1,3}(?:\D|$)",
    re.I,
)


def _sohieu_key_entry(e: dict) -> str:
    sh = _entry_sohieu(e) or _parse_sohieu_from_name(_entry_name(e))
    return norm_sohieu((sh or "").replace("_", "-"))


def _entry_md5(e: dict) -> str:
    return str(e.get("md5") or e.get("md5Checksum") or "")


def _entry_row_kind(e: dict) -> str:
    return str(e.get("row_kind") or "own").strip().lower() or "own"


def _entry_is_own_thuong(e: dict) -> bool:
    corpus = str(e.get("corpus") or "").strip().lower()
    loai = str(e.get("loai") or "").strip().lower()
    return _entry_row_kind(e) == "own" and (loai == "thuong" or corpus in {"false", "thuong"})


def _split_distinct_vbhn_docs(arr: list[dict]) -> list[list[dict]]:
    """Chia nhóm CÙNG SỐ HIỆU thành các VĂN BẢN KHÁC NHAU theo XUNG ĐỘT metadata: 2 entry là khác-document nếu
    NĂM ban hành rời nhau (cùng có) HOẶC goc rời nhau (cùng có). Entry thiếu cả năm lẫn goc → KHÔNG xung đột với
    ai → gộp vào doc có sẵn. Phân biệt reuse-thật (vd 14/VBHN: ATVSLĐ-2024 vs NLĐ-2023, năm khác) với nhân-đôi
    cùng-document (vd 18/VBHN BLLĐ: GDoc 2026 + .docx thiếu năm). Xếp entry CÓ metadata trước để neo nhóm."""
    groups: list[dict] = []

    def conflict(g, ys, gos):
        if ys and g["years"] and not (ys & g["years"]):
            return True
        if gos and g["gocs"] and not (gos & g["gocs"]):
            return True
        return False

    for e in sorted(arr, key=lambda x: (bool(_entry_years(x)) or bool(_goc_keys(x))), reverse=True):
        ys, gos = set(_entry_years(e)), set(_goc_keys(e))
        g = next((g for g in groups if not conflict(g, ys, gos)), None)
        if g is None:
            g = {"years": set(), "gocs": set(), "entries": []}
            groups.append(g)
        g["years"] |= ys
        g["gocs"] |= gos
        g["entries"].append(e)
    return [g["entries"] for g in groups]


def _vbhn_subject_key(e: dict) -> str:
    """Tách các VBHN tái sử dụng cùng số theo năm/chủ đề/gốc."""
    y = str(_entry_issue_year(e) or "")
    refs = sorted(_goc_keys(e) | _ref_tokens(_field_text(e, _REF_KEYS + _META_TITLE_KEYS)))
    tail = _name_tail_key(_entry_name(e))
    # Bỏ năm trong tail để bản GDoc và file gốc cùng năm vẫn nhập cụm.
    tail = re.sub(r"\b(?:20\d{2}|19\d{2})\b", " ", tail)
    tail = re.sub(r"\s+", " ", tail).strip()
    if refs:
        return "G" + ",".join(refs[:6])
    if y or tail:
        return "Y" + y + ":T" + tail
    return "UNKNOWN"


def _dup_of_live_sibling(e: dict, group: list[dict]) -> bool:
    """True nếu `e` (corpus, KHÔNG trên NLM live) chỉ là BẢN SAO/SIDECAR của một anh-em CÙNG
    văn bản trong nhóm ĐÃ trên NLM live → KHÔNG báo nhầm CORPUS_TRUE_NOT_ON_NLM cho dòng phụ
    (GDoc trùng `..._m_<id>`, file gốc .doc/.docx/.pdf cạnh GDoc). An toàn va-chạm-số-hiệu: yêu cầu
    CÙNG dedupe-key (VBHN khóa theo chủ đề/gốc) VÀ (md5 trùng HOẶC chủ-đề-tail không mâu thuẫn —
    1 bên rỗng/coded HOẶC chứa nhau). Bản thô CÙNG số nhưng KHÁC chủ đề (vd 60/2024 Phòng_bệnh vs
    Dữ_liệu, 67/2006 NLĐ vs CNTT) VẪN bị flag — đó là gap thật, không suppress."""
    if _entry_on_nlm_live(e):
        return False
    dk = _dedupe_key_entry(e)
    if not dk:
        return False
    def _topic(x: dict) -> str:
        sig = _subject_sig(_entry_name(x))
        return re.sub(r"^(?:luat|bo|nghidinh|thongtu|quyetdinh|chithi|nghiquyet|hopnhat|goc|nd|ndcp|cp|tt|qd|nq|ct|pl|vbhn|vpqh|m|qh|ubtvqh)+", "", sig)
    et = _topic(e)
    emd5 = _entry_md5(e)
    for s in group:
        if s is e or not _entry_on_nlm_live(s):
            continue
        if emd5 and emd5 == _entry_md5(s):
            return True
        if _dedupe_key_entry(s) != dk:
            continue
        st = _topic(s)
        if (not et) or (not st) or et == st or et in st or st in et:
            return True
    return False


def _dedupe_key_entry(e: dict) -> str:
    sh = _sohieu_key_entry(e)
    if not sh:
        return ""
    if _is_vbhn_entry(e):
        return "VBHN:" + sh + ":" + _vbhn_subject_key(e)
    return sh


def _is_source_sidecar(e: dict, group: list[dict], canonical: dict | None = None) -> bool:
    """File .doc/.docx/.pdf gốc nằm cạnh GDoc là sidecar hợp lệ, không phải rác."""
    name = _entry_name(e)
    if _entry_nlm(e) or not re.search(r"\.(docx?|pdf)$", name or "", re.I):
        return False
    base = _name_key(re.sub(r"\.(docx?|pdf)$", "", name, flags=re.I))
    for other in group:
        if other is e:
            continue
        if canonical is not None and other is not canonical and not _entry_nlm(other):
            continue
        if _dedupe_key_entry(other) and _dedupe_key_entry(other) == _dedupe_key_entry(e):
            return True
        obase = _name_key(re.sub(r"\.(docx?|pdf)$", "", _entry_name(other), flags=re.I))
        if base and obase and (base == obase or base in obase or obase in base):
            return True
    return False


def _bad_cat(cat: str) -> bool:
    c = str(cat or "").strip().lower()
    return (not c) or c in ("root", "(root)", "none", "null")


def _reconcile_clusters(entries: list[dict]) -> list[dict]:
    """Gộp cụm registry theo khóa an toàn HOẶC md5.

    VBHN không gom theo số hiệu trần vì VPQH có thể tái sử dụng cùng số ở năm/chủ đề khác nhau.
    Đây là lớp bù cho vb_status vốn dedup theo số hiệu và bỏ lọt orphan `sohieu=''`."""
    entries = [e for e in entries if _entry_row_kind(e) != "ref" and not _entry_is_own_thuong(e)]
    n = len(entries)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[ry] = rx
    for key_fn in (lambda e: _dedupe_key_entry(e), _entry_md5):
        buckets: dict[str, list[int]] = {}
        for i, e in enumerate(entries):
            k = key_fn(e)
            if k:
                buckets.setdefault(k, []).append(i)
        for idxs in buckets.values():
            for j in idxs[1:]:
                union(idxs[0], j)
    groups: dict[int, list[dict]] = {}
    for i, e in enumerate(entries):
        groups.setdefault(find(i), []).append(e)
    clusters = []
    for group in groups.values():
        # Cụm đáng quan tâm: có hơn 1 dòng, hoặc có orphan/root/số hiệu rỗng/tên thô.
        # Nhưng tuyệt đối KHÔNG suy luận số hiệu/quarantine từ tài liệu làm việc kiểu Mẫu_/PL_:
        # đây là số thứ tự biểu mẫu/phụ lục, không phải số hiệu VBQPPL.
        if all(_name_is_template_or_appendix(_entry_name(e)) for e in group):
            continue
        def rawish(e):
            return (not _name_is_template_or_appendix(_entry_name(e))) and bool(re.search(r"(^|[/_ -])\d{2,4}[_-]\d{4}[_-]", _entry_name(e)))
        def orphanish(e):
            return (not _name_is_template_or_appendix(_entry_name(e))) and ((not _entry_sohieu(e)) or _bad_cat(_entry_cat(e)) or (rawish(e) and not _entry_nlm(e) and not _is_source_sidecar(e, group)))
        flagged = len(group) > 1 or any(orphanish(e) for e in group)
        if not flagged:
            continue
        # Canonical = điểm cao nhất, nhưng ưu tiên có số hiệu + cat không root.
        ordered = sorted(group, key=_entry_score, reverse=True)
        canonical = ordered[0] if ordered else None

        # 2026-06: chỉ đề xuất QUARANTINE bản THỰC SỰ trùng văn bản với canonical (cùng chữ ký chủ đề,
        # hoặc một bên là tên thô/coded). Khác-cơ-quan (TT-BNV vs TT-BYT) hay phụ-lục-vs-chính (cùng số hiệu,
        # chủ đề khác) → GIỮ cả hai (cụm vẫn hiện để rà tay, nhưng không tự xếp quarantine).
        def _cluster_same_doc(e):
            if not _entry_drive_id(e) or _is_source_sidecar(e, group, canonical):
                return False
            cs = _subject_sig(_entry_name(canonical)) if canonical else ""
            es = _subject_sig(_entry_name(e))
            return (not es) or (not cs) or (es == cs) or (es in cs) or (cs in es)
        quarantine = [e for e in ordered[1:] if _cluster_same_doc(e)]
        # Nếu cụm chỉ có 1 orphan không canonical rõ, vẫn đưa vào candidates để rà tay/quarantine.
        if len(group) == 1 and orphanish(group[0]):
            canonical = None
            quarantine = [group[0]] if _entry_drive_id(group[0]) else []
        key = _dedupe_key_entry(canonical or group[0]) or _sohieu_key_entry(canonical or group[0]) or _name_key(_entry_name(canonical or group[0]))
        clusters.append({"key": key, "canonical": canonical, "entries": group, "quarantine": quarantine,
                         "sidecars": [e for e in group if _is_source_sidecar(e, group, canonical)]})
    clusters.sort(key=lambda c: (0 if c.get("canonical") else 1, c.get("key") or ""))
    return clusters


def _cluster_matches(c: dict, q: str) -> bool:
    if not q:
        return True
    for e in c.get("entries") or []:
        if _entry_query_match_safe_for_hygiene(q, e):
            return True
    return False


def _select_hygiene_clusters(clusters: list[dict], q: str) -> tuple[list[dict], list[dict]]:
    """Chọn cụm cho plan/apply.

    Cụm thiếu canonical chỉ được báo ở `skipped_clusters`, không đưa vào tập có thể apply.
    Như vậy consumer JSON không còn gặp object apply với `canonical: null`.
    """
    raw = [c for c in clusters if _cluster_matches(c, q)]
    selected = [c for c in raw if c.get("canonical")]
    skipped = []
    for c in raw:
        if c.get("canonical"):
            continue
        cc = dict(c)
        cc["skip_reason"] = "MISSING_CANONICAL_REVIEW_ONLY"
        skipped.append(cc)
    return selected, skipped


def _sohieu_dup_group_real(group: list[dict]) -> bool:
    """C4 (v1.33.0 — log rà 15 Luật: sweep by_sohieu=93 'trùng' nhưng chỉ 4 cụm có ≥2 bản corpus=true và CẢ 4 là
    tách Phụ lục/Final CỐ Ý; 49 cụm còn lại là cặp gốc+VBHN/quarantine LÀNH — headline 93 = báo động giả, trái
    doctrine 'không gom VBHN theo số hiệu trần' v1.17.9/15): cụm trùng THẬT = ≥2 bản corpus=true CÙNG PHÍA
    (≥2 VBHN hoặc ≥2 non-VBHN) sau khi loại sidecar/quarantine/template/phụ-lục. Cặp gốc+VBHN cùng số (row VBHN
    chỉ mục theo số bản gốc) là quan hệ HỢP LỆ, không phải trùng."""
    core = []
    for e in group:
        if not _entry_corpus_true(e) or _entry_quarantined(e):
            continue
        nm = _entry_name(e)
        if _name_is_template_or_appendix(nm) or _is_source_sidecar(e, group):
            continue
        if "phuluc" in re.sub(r"[\s_-]", "", _ascii_lower(nm)):
            continue                       # phụ lục tách riêng cố ý (PhuLuc/Phu_luc/phu-luc — cả dạng nén)
        core.append(e)
    if len(core) < 2:
        return False
    n_vbhn = sum(1 for e in core if _is_vbhn_entry(e))
    return n_vbhn >= 2 or (len(core) - n_vbhn) >= 2


def _summ_entry(e: dict|None) -> dict|None:
    if not e:
        return None
    return {
        "drive_id": _entry_drive_id(e), "name": _entry_name(e), "sohieu": _entry_sohieu(e),
        # B5: `nlm` = CÓ TRÊN NLM LIVE (False nếu removed) → khớp reg-query; `nlm_status` giữ chi tiết.
        "sohieu_key": _sohieu_key_entry(e), "cat": _entry_cat(e), "nlm": _entry_on_nlm_live(e),
        "nlm_source_id": _entry_nlm(e), "nlm_notebook_id": _entry_nlm_notebook_id(e),
        "nlm_status": str(e.get("nlm_status") or ""),
        "row_kind": e.get("row_kind") or "own", "corpus": e.get("corpus") or "",
        "hieuluc": e.get("hieuluc") or e.get("hieu_luc") or "", "issue_year": _entry_issue_year(e),
        "score": _entry_score(e),
        "confirmed": _entry_confirmed(e),   # nhãn đã-rà-kỹ (registry.verified) → tin dùng luôn
        "flags": _title_flags(e),
    }


_SRCMAP_GLOBAL_ONLY_FLAGS = {"NLM_STATUS_MISMATCH"}

# A3 (log rà 122 luật — tối ưu MERGE): CỔNG WARN rộng hơn cổng HIỂN THỊ. Cờ TRÔI/HYGIENE registry↔NLM đã hiện ở
# `doctor`/`sweep` (+ warning `nlm_gaps` riêng trong source-map) → KHÔNG kích `TITLE_OR_REGISTRY_WARN` per-law (đo thật:
# 12/22 luật chỉ WARN vì CORPUS_TRUE_NOT_ON_NLM/RAW_NAME_NOT_NLM của BẢN THÔ song song). Vẫn HIỂN THỊ đủ ở risky_candidates.
_TITLE_WARN_GLOBAL_FLAGS = frozenset({
    "NLM_STATUS_MISMATCH", "CORPUS_TRUE_NOT_ON_NLM", "NLM_NOTEBOOK_ID_MISSING", "RAW_NAME_NOT_NLM",
})


def _warning_codes(warnings: list[str]) -> list[str]:
    """Mã cờ = tiền tố MÃ dẫn đầu warning (mọi warning format `CODE_NAME: mô tả` hoặc mã trần). CHỈ lấy mã dẫn đầu →
    `flags` SẠCH cho driver máy-đọc, KHÔNG nhặt token IN-HOA phụ trong phần mô tả (vd 'VBHN'/'NLM' trong câu chữ)."""
    out = []
    for w in warnings or []:
        head = str(w or "").split(":", 1)[0].strip()
        if re.fullmatch(r"[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*", head) and head not in out:
            out.append(head)
    return out


def _aggregate_verdict(items: list[dict]) -> str:
    verdicts = [it.get("verdict") for it in items or []]
    if any(v == "PAUSE_AND_ASK_USER" for v in verdicts):
        return "PAUSE_AND_ASK_USER"
    if any(v == "REVIEW" for v in verdicts):
        return "REVIEW"
    if verdicts and all(v == "UNKNOWN_NOT_ABSENT" for v in verdicts):
        return "UNKNOWN_NOT_ABSENT"
    return "OK"


def _print_reconcile(clusters: list[dict]) -> None:
    print(f"== tl reconcile — cụm vấn đề: {len(clusters)} | ứng viên QUARANTINE: {sum(len(c['quarantine']) for c in clusters)} ==\n")
    for c in clusters:
        canon = c.get("canonical")
        print(f"▸ cụm '{c.get('key') or '∅'}' ({len(c.get('entries') or [])} bản)")
        if canon:
            s = _summ_entry(canon)
            print(f"    GIỮ: {s['name'][:70]} | cat={s['cat']} | sohieu={s['sohieu'] or '∅'} | id={s['drive_id']}")
        else:
            print("    ⚠ KHÔNG có canonical rõ — rà tay trước khi move.")
        for e in c.get("quarantine") or []:
            s = _summ_entry(e)
            print(f"    → QUARANTINE? {s['name'][:70]} | cat={s['cat'] or '(root)'} | sohieu={s['sohieu'] or '∅'} | id={s['drive_id']}")
    print("\n[tl] DRY-RUN — KHÔNG trash. Dùng hygiene plan/reconcile --apply --confirm yes sau khi duyệt.")


def _apply_quarantine(entries: list[dict], to_cat: str = "QUARANTINE") -> list[dict]:
    g = _gas(); results = []
    dest = to_cat or "QUARANTINE"
    for e in entries:
        did = _entry_drive_id(e)
        if did:
            results.append({"drive_id": did, "name": _entry_name(e), "to_cat": dest, "move": g.get("move", fileId=did, cat=dest)})
    return results


# ───────────────────────── external ingest gate + instruction binding ─────────────────────────
def _looks_like_new_target(x: str | None) -> bool:
    y = (x or "").strip().lower()
    return y in {"new", "new_notebook", "new-folder", "new_folder", "temp", "temporary", "notebook_tam", "tạm", "tam"} or "notebook tạm" in y or "temporary" in y


def _external_format_class(fmt: str | None, url: str | None = None) -> str:
    raw = (fmt or "").strip().lower()
    u = (url or "").lower()
    if not raw:
        for ext in (".docx", ".doc", ".rtf", ".odt", ".pdf", ".html", ".htm"):
            if ext in u.split("?")[0]:
                raw = ext.lstrip(".")
                break
    if raw in {"gdoc", "google-doc", "google_docs", "google doc"}:
        return "gdoc"
    if raw in {"docx", "doc", "rtf", "odt"}:
        return "docx_convertible"
    if raw == "pdf":
        return "pdf"
    if raw in {"html", "htm", "text", "txt"}:
        return "text_html"
    return raw or "unknown"


def _looks_like_drive_id(s: str) -> bool:
    """P0-1 LỚP 1 (MERGE patch AUDIT 07/2026 → v1.33.13): Drive file ID thật luôn [A-Za-z0-9_-] và ≥20 ký tự
    (thường 33/44) — id ngắn = gần như chắc chắn CẮT CỤT/typo khi copy-paste output rút gọn. Check OFFLINE rẻ,
    chạy TRƯỚC lớp 2 existence-check (manifest/Drive live). Cho phép prefix 'nlm:' (khóa ghost hợp lệ)."""
    s = (s or "").strip()
    if s.startswith("nlm:"):
        return len(s) > 10
    return bool(re.fullmatch(r"[A-Za-z0-9_-]{20,}", s))


def _register_bulk_missing(items: list, known_ids: set, live_prober, cap: int = 20) -> list:
    """P0-1 bulk LỚP 2 (MERGE nhánh-3 v1.33.14 — PURE, testable): item drive_id đúng-dạng nhưng KHÔNG có trong
    manifest → probe Drive live tối đa `cap` id (mỗi probe 1 round-trip); quá cap → coi là missing luôn (bulk
    đăng-ký-file-mới hàng loạt là hiếm; muốn ép → --force-insert). Trả danh sách id thật sự không tồn tại."""
    missing = [str((it or {}).get("drive_id")) for it in (items or [])
               if (it or {}).get("drive_id") and (it or {}).get("drive_id") not in known_ids]
    really = []
    for did in missing[:cap]:
        try:
            if not live_prober(did):
                really.append(did)
        except Exception:  # noqa: BLE001
            really.append(did)
    really.extend(missing[cap:])
    return really


def _register_target_exists(drive_id: str, live_prober=None) -> bool:
    """P0-1 (v1.33.12 — log phiên khắc phục: `register --drive-id <id CẮT CỤT>` → reg_upsert INSERT dòng registry
    MỚI RỖNG, ok:true không báo, registry 746→747 sai mọi mẫu số): drive_id phải TỒN TẠI — trong manifest cache,
    HOẶC trên Drive live (files_get — cho file VỪA upload chưa vào cache, luồng ingest hợp lệ). PURE-ish:
    live_prober tiêm được để test offline."""
    try:
        if any(_entry_drive_id(e) == drive_id for e in _manifest_entries()):
            return True
    except Exception:  # noqa: BLE001
        pass
    try:
        if live_prober is None:
            def live_prober(fid):
                _fg = _imp("transport").drive_op("files_get", file_id=fid, _quiet=True)
                return bool(isinstance(_fg, dict) and _fg.get("ok") and (_fg.get("file") or {}).get("id"))
        return bool(live_prober(drive_id))
    except Exception:  # noqa: BLE001
        return False


def _resolve_headerverify_targets(a, entries: list[dict]) -> list[dict]:
    """G2: target cho header-verify. --drive-id(1) / --sohieu(canonical) / --cat NN(corpus) / --all(mọi corpus).
    KHÁC confirm: KHÔNG lọc 'chưa-confirm' (audit lại CẢ bản đã confirm để bắt DRIFT). Batch giới hạn --limit."""
    did = getattr(a, "drive_id", None)
    if did:
        return [e for e in entries if _entry_drive_id(e) == did]
    shf = getattr(a, "sohieu_file", None)
    if shf:
        # B3 (v1.33.0 — log rà 69: vòng `corpus-audit --sohieu X` ×69 PROCESS RỜI = 69 lần boot + retry gws
        # per-doc, dễ vượt timeout shell): cả lô trong 1 PROCESS. Mỗi dòng 1 số hiệu, '#' comment; resolve
        # canonical như --sohieu, dedup theo drive_id; dòng không resolve được báo LOUD (không nuốt câm).
        try:
            _lines = Path(shf).read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as _ex:
            print(f"[targets] --sohieu-file không đọc được: {_ex}", file=sys.stderr)
            return []
        out, seen = [], set()
        for _ln in _lines:
            q = _ln.split("#", 1)[0].strip()
            if not q:
                continue
            canon, _hits = _canonical_for_query(q, refresh=False)
            if canon is None:
                print(f"[targets] ⚠ --sohieu-file: không resolve được '{q}' — bỏ qua (kiểm chính tả/`tl locate`).",
                      file=sys.stderr)
                continue
            _cd = _entry_drive_id(canon)
            if _cd and _cd not in seen:
                seen.add(_cd); out.append(canon)
        try:
            a._targets_pool_total = len(out)
        except Exception:  # noqa: BLE001
            pass
        # A6 (v1.33.2 — log rà 111: --limit bị BỎ QUA IM LẶNG ở nhánh --sohieu-file): mặc định (không --limit)
        # = CẢ LÔ (đúng thiết kế 1-process + checkpoint --resume); truyền --limit/--offset → cắt LOUD như --all.
        _off = max(0, int(getattr(a, "offset", None) or 0))
        _lim = getattr(a, "limit", None)
        if _off or _lim:
            _end = min(_off + _lim, len(out)) if _lim else len(out)
            print(f"[targets] ⚠ CẮT BATCH --sohieu-file: {_off}..{_end}/{len(out)}"
                  + (f" — trang kế: --offset {_end}." if _end < len(out) else ".")
                  + " (Bỏ --limit/--offset để chạy CẢ LÔ + --resume.)", file=sys.stderr, flush=True)
            out = out[_off:_end]
        return out
    sh = getattr(a, "sohieu", None)
    if sh:
        canon, _hits = _canonical_for_query(sh, refresh=getattr(a, "refresh", False))
        return [canon] if canon else []
    cat = getattr(a, "cat", None)
    if cat or getattr(a, "all", False):
        cc = re.sub(r"\D", "", str(cat))[:2] if cat else ""
        pool = [e for e in entries if _entry_drive_id(e) and str(e.get("corpus") or "").lower() != "false"
                and not _entry_quarantined(e) and (not cc or re.sub(r"\D", "", str(_entry_cat(e)))[:2] == cc)]
        # v1.29.4 (log LIVE i1): --offset PHÂN TRANG — trước đây mỗi lần gọi quét lại TỪ ĐẦU nên limit lớn (cat 45,
        # limit 30-40) chạy quá dài → client-timeout giết = "treo im lặng". Nay: chạy lô nhỏ + --offset tiếp trang.
        _off = max(0, int(getattr(a, "offset", None) or 0))
        # A6 v1.33.2: corpus-audit --limit nay default=None (phân biệt explicit cho --sohieu-file) → fallback 40
        # ở đây giữ NGUYÊN hành vi --all/--cat cũ (header-verify vẫn truyền default 20 tường minh của nó).
        _lim = getattr(a, "limit", None) or 40
        # v1.29.6 (log 118 Luật — P1: `--all` bị cap ÂM THẦM ở limit mặc định → scanned=40/515, 0 proposal → tưởng
        # corpus SẠCH giả). KHÔNG bỏ cap (515 lần đọc-header = ~25' sẽ lại client-timeout như i1) — nhưng phải LOUD.
        if len(pool) > _off + _lim:
            print(f"[targets] ⚠ CẮT BATCH: quét {_off}..{min(_off + _lim, len(pool))}/{len(pool)} target "
                  f"(limit={_lim}). CHƯA PHỦ HẾT — trang kế: --offset {_off + _lim} --limit {_lim}. "
                  f"KHÔNG kết luận 'corpus sạch' khi chưa quét đủ.", file=sys.stderr, flush=True)
        try:
            a._targets_pool_total = len(pool)     # cho caller (corpus-audit) in pool_total/next_offset vào JSON
        except Exception:
            pass
        return pool[_off: _off + _lim]
    return []


def _flag_value(args: list, flag: str):
    """Lấy giá trị đi sau cờ `flag` trong list args (hỗ trợ `--flag val` và `--flag=val`). None nếu không có."""
    for i, x in enumerate(args):
        if x == flag and i + 1 < len(args):
            return args[i + 1]
        if x.startswith(flag + "="):
            return x.split("=", 1)[1]
    return None


def _entry_years(e: dict) -> set[str]:
    """Lấy năm từ metadata/tên để phát hiện số VBHN tái sử dụng theo năm."""
    txt = _field_text(e, (
        "ngay", "ngay_ban_hanh", "ngayBanHanh", "banhanh", "ban_hanh", "issued",
        "date", "year", "nam", "name", "title", "title_vn", "trichyeu", "trich_yeu", "summary",
    ))
    yrs = set(re.findall(r"(?<!\d)(?:20\d{2}|19\d{2})(?!\d)", txt or ""))
    iy = _entry_issue_year(e)
    if iy:
        yrs.add(str(iy))
    return yrs


# Cụm CHUNG TIỀN TỐ nhưng KHÁC BẢN CHẤT — token phân biệt PHẢI khớp, KHÔNG match theo tiền tố chung
# (vd "bảo hiểm xã hội" ≠ "bảo hiểm y tế" ≠ "bảo hiểm thất nghiệp"; chung "bảo hiểm" → đừng coi là cùng chủ đề).
# Mỗi nhóm: (chuỗi-CHUNG, [danh sách bộ-token-PHÂN-BIỆT]). So trên text ĐÃ bỏ dấu (token ngắn 'xã'/'y tế' bị
# _subject_tokens lọc len≥3 nên phải so chuỗi). Có thể bổ sung nhóm khác khi gặp ca tương tự.
_SUBJECT_DISC_GROUPS = [
    ("bao hiem", [("xa hoi",), ("y te", "yte"), ("that nghiep",), ("tien gui",), ("nong nghiep",),
                  ("tai nan lao dong", "tai nan", "benh nghe nghiep", "tnld")]),
]


def _vbhn_quality_flags(e: dict, subject: str = "", goc_keys: set[str] | None = None, year: str = "") -> list[str]:
    flags = list(_title_flags(e))
    if _is_vbhn_entry(e):
        yrs = _entry_years(e)
        if year and year not in yrs and year not in _entry_name(e):
            flags.append("VBHN_YEAR_NOT_IN_METADATA")
        if "VBHN_BARE_NUMBER" in flags:
            flags.append("VBHN_NAME_MISSING_SUBJECT")
    if subject and _subject_score(e, subject) < 30:
        flags.append("SUBJECT_NOT_EVIDENT_IN_METADATA")
    if goc_keys:
        refs = _goc_keys(e) | _ref_tokens(_field_text(e, _REF_KEYS + _META_TITLE_KEYS))
        if not (refs & goc_keys):
            flags.append("GOC_NOT_EVIDENT_IN_METADATA")
    out = []
    for f in flags:
        if f not in out:
            out.append(f)
    return out


def _vbhn_scan(entries: list[dict]) -> dict:
    vbhn = [e for e in entries if _is_vbhn_entry(e)]
    by_num: dict[str, list[dict]] = {}
    missing_subject = []
    for e in vbhn:
        k = norm_sohieu(_entry_sohieu(e) or _parse_sohieu_from_name(_entry_name(e)))
        if k:
            by_num.setdefault(k, []).append(e)
        flags = _vbhn_quality_flags(e)
        if "VBHN_BARE_NUMBER" in flags or "VBHN_MISSING_YEAR_OR_DATE" in flags or "VBHN_NAME_MISSING_SUBJECT" in flags:
            missing_subject.append(e)
    collisions = []
    for k, arr in by_num.items():
        if len(arr) > 1:
            years = sorted(set().union(*[_entry_years(x) for x in arr]))
            collisions.append({"key": k, "years": years, "entries": sorted(arr, key=_entry_score, reverse=True)})
    return {"vbhn_count": len(vbhn), "collisions": collisions, "missing_subject": missing_subject}


# S10 (log 2026-07-01): LUẬT/BỘ LUẬT bị SỬA ĐỔI DỒN DẬP giai đoạn cải cách 2024-2026 — với nhóm này BẮT BUỘC lượt-2
# "mới nhất" + kiểm Công báo theo năm hiện tại (Google xếp trang cũ 2017/2020 lên đầu → dễ chốt VBHN LỖI THỜI). ascii-lower.
_HIGH_AMENDMENT_SUBJECTS = (
    "hinh su", "to tung hinh su", "to tung dan su", "to tung hanh chinh", "thi hanh an",
    "phi va le phi", "phi le phi", "dat dai", "doanh nghiep", "dau tu", "dau thau", "thue",
    "chung khoan", "xay dung", "nha o", "kinh doanh bat dong san", "quy hoach", "quang cao",
    "cong chung", "dau gia", "vien chuc", "can bo cong chuc", "to chuc tin dung", "bao hiem xa hoi",
)


def _vbhn_latest_low_priority_recent_law(subject: str, goc: str, year: str, has_candidates: bool) -> bool:
    """S-8b (v1.33.16 — MERGE nhánh-4, PURE): vbhn-check trên LUẬT RẤT MỚI chưa có ứng viên VBHN nào trong
    corpus không nên gắn VBHN_CANDIDATE_UNVERIFIED_LATEST nặng như luật ĐÃ có VBHN chưa xác minh mới nhất —
    QT5_WEB_REQUIRED giữ nguyên, chỉ hạ riêng cờ latest. Điều kiện: không candidate + năm luật (từ --year hoặc
    sohieu goc) ≥ năm-nay−2 [ĐỘNG — nhánh-4 hardcode 2024 sẽ mục theo thời gian] + không thuộc nhóm dồn dập."""
    if has_candidates:
        return False
    y = 0
    try:
        y = int(str(year or "").strip()[:4]) if str(year or "").strip() else 0
    except (TypeError, ValueError):
        y = 0
    if not y and goc:
        y = _sohieu_year(norm_sohieu(goc)) or 0
    if not y or y < time.localtime().tm_year - 2:
        return False
    return not (_is_high_amendment_subject(subject) or _is_high_amendment_subject(goc))


def _vbhn_agency_mismatch(base_key: str, e: dict) -> bool:
    """P1-4 (v1.31.0, PURE): True khi ứng viên là VBHN CẤP BỘ/ngành (VBHN-BTP/BGDDT/BTC/NHNN…) mà base là văn bản
    QUỐC HỘI (…-QHxx/UBTVQH/LCT-HDNN/Pháp lệnh). VBHN cấp Bộ hợp nhất NĐ/TT — KHÔNG BAO GIỜ là VBHN của Luật QH
    (VBHN của Luật do VPQH ban hành). Log LIVE 2026-07-03: 4231-2025-VBHN-BTP (NĐ) score 158 nổi làm candidate
    Luật 90/2025; loạt VBHN-BGDDT nổi cho Luật Giáo dục 123/2025. Agency rỗng/VPQH → KHÔNG chặn."""
    bk = str(base_key or "")
    # base QH-family: Luật/Bộ luật/NQ-QH (…-QHxx) · Pháp lệnh/NQ-UBTVQH (…-UBTVQHxx) · luật trước-1992 (LCT-HDNN).
    if not bk or not re.search(r"-QH\d+$|-UBTVQH\d+$|LCT-HDNN", bk):
        return False
    ag = _vbhn_agency_from_key(_sohieu_key_entry(e))
    return bool(ag) and ag != "VPQH"


def _vbhn_candidates(entries: list[dict], subject: str = "", goc: str = "", year: str = "") -> list[dict]:
    gkeys = {norm_sohieu(goc)} if goc else set()
    # #7: số hiệu ĐÃ có bản NLM → bản .docx/.pdf thô cùng số hiệu là THỪA. (GIỮ .docx VBHN mới CHƯA-NLM để người
    # dùng vẫn thấy lúc vừa tải về — tránh regression mà workflow xác minh chỉ ra.)
    _nlm_keys = {_sohieu_key_entry(e) for e in entries if _entry_nlm(e) and _sohieu_key_entry(e)}
    out = []
    for e in entries:
        if not _is_vbhn_entry(e):
            continue
        # Bỏ file gốc thô (.doc/.docx/.pdf, KHÔNG nằm NLM) khi: là sidecar, HOẶC số hiệu rỗng, HOẶC đã có bản NLM
        # TRÙNG số hiệu (bản thô thừa — vd "000.01…18_VBHN-VPQH.docx" hay "108-VBHN-VPQH.docx" cạnh GDoc NLM).
        _raw_doc = (not _entry_nlm(e)) and bool(re.search(r"\.(docx?|pdf)$", _entry_name(e), re.IGNORECASE))
        if _is_source_sidecar(e, entries) or (
                _raw_doc and ((not _entry_sohieu(e)) or (_sohieu_key_entry(e) in _nlm_keys))):
            continue
        refs = _goc_keys(e) | _ref_tokens(_field_text(e, _REF_KEYS + _META_TITLE_KEYS))
        # A3: loại trừ chéo lĩnh vực ngay (BHXH↔BHYT… dù trùng năm/tiền tố) — đừng để lọt ứng viên khác bản chất.
        if subject and _disc_conflict(subject, _entry_subject_text(e)):
            continue
        sscore = _subject_score(e, subject)
        yscore = 20 if (year and year in _entry_years(e)) else 0
        gscore = 80 if (gkeys and refs & gkeys) else 0
        goc_hit = bool(gkeys and refs & gkeys)
        # #2/A3: goc-ref = tín hiệu mạnh. subject≥60 = trùng tên/đủ token. **year CHỈ tính KHI subject cũng liên quan
        # (≥30)** — year-MỘT-MÌNH kéo nhầm VBHN khác lĩnh vực cùng năm. Không có subject → year là tín hiệu duy nhất.
        # 5.2 (report rà 106 Luật): goc_hit cross-subject LỌT khi `_disc_conflict` KHÔNG biết cặp (vd 'du lịch' vs 'lao
        # động' → 14-2024 ATVSLĐ lọt vào --goc 09-2017 Du lịch). FIX: khi ĐÃ biết subject (truyền/suy từ goc), goc_hit
        # phải TƯƠNG THÍCH chủ đề (sscore≥30) — chặn bare-number/goc-ref nhiễu khác lĩnh vực. subject rỗng → goc_hit
        # vẫn nhận (không có chủ đề để đối chiếu).
        goc_keep = goc_hit and ((not subject) or sscore >= 30)
        # P1-4 (v1.31.0): base --goc là văn bản QH + ứng viên VBHN CẤP BỘ (hợp nhất NĐ/TT) → LOẠI khi KHÔNG có
        # goc-chain dẫn chiếu base (subject/year-match KHÔNG đủ bằng chứng — chặn 4231-VBHN-BTP nổi cho Luật 90/2025).
        if gkeys and not goc_hit and _vbhn_agency_mismatch(next(iter(gkeys)), e):
            continue
        keep = (goc_keep
                or (subject and sscore >= 60)
                or (subject and sscore >= 30 and yscore)
                or (not subject and yscore))
        if keep:
            out.append((gscore + sscore + yscore + _entry_score(e), e))
    out.sort(key=lambda x: x[0], reverse=True)
    return [e for _, e in out]


def _read_verify_text(a) -> tuple[str, str]:
    text_file = getattr(a, "text_file", None)
    gdoc = getattr(a, "gdoc_id", None)
    sohieu = getattr(a, "sohieu", None)
    # vbhn positional-compat (tương thích runbook cũ): `tl vbhn-verify "<text-file|gdoc-id|số hiệu>"` → tự định tuyến.
    target = getattr(a, "target", None)
    if target and not (text_file or gdoc or sohieu):
        tp = Path(target)
        if tp.exists():
            text_file = str(tp)
        elif re.fullmatch(r"[A-Za-z0-9_\-]{20,}", target):
            gdoc = target
        else:
            sohieu = target
    if text_file:
        p = Path(text_file)
        return p.read_text(encoding="utf-8", errors="replace"), str(p)
    if not gdoc and sohieu:
        canon, _hits = _canonical_for_query(sohieu, refresh=getattr(a, "refresh", False))
        if canon:
            gdoc = _entry_drive_id(canon)
    if not gdoc:
        raise RuntimeError("cần --text-file hoặc --gdoc-id hoặc --sohieu resolve được")
    load_creds(getattr(a, "config", None))
    # A1 (v1.33.10 — log: xref/vbhn-verify chết 'thiếu scope script.external_request' TRONG KHI direct-media gws
    # đang SỐNG): đường đọc phải GWS-FIRST như extract/corpus-audit — _read_doc_text = cache → direct-media →
    # transport → exporttext CUỐI CÙNG; không gọi thẳng exporttext nữa.
    _txt = _read_doc_text(gdoc, getattr(a, "config", None))
    if not (_txt or "").strip():
        raise RuntimeError("đọc nguyên văn thất bại MỌI đường (cache/direct-media/gws/exporttext) — kiểm `tl gws-ping`; "
                           "webapp exporttext chỉ sống khi có scope script.external_request (fallback cuối).")
    return _txt, gdoc


_ASSEMBLED_HINTS = (
    "assembled", "self assembled", "tu lap", "tu ghep", "tu tao", "lap tu",
    "ban tam", "tam thoi", "draft", "synthetic", "generated", "khong dung",
    "khong_dung", "zzz_assembled",
)

_OFFICIAL_HINTS = (
    "van phong quoc hoi", "cong bao", "vbpl", "quochoi",
    "chinhphu", "official", "_official", "629950",
)


def _vbhn_official_flags(text: str, source_name: str = "", official_required: bool = False,
                         allow_provisional: bool = False) -> list[str]:
    """Guard quy trình: bản tự ghép chỉ được là bản tạm, không được chốt làm canonical."""
    blob = unicodedata.normalize("NFC", (source_name or "") + "\n" + (text or "")[:30000])
    norm = _strip_accents(blob).lower().replace("_", " ")
    flags = []
    # vbhn_verify_header_unread: marker 'tự ghép'/'không dùng'/'zzz_assembled' là tín hiệu ĐẶT-TÊN-FILE/quarantine —
    # CHỈ soi SOURCE_NAME, KHÔNG soi thân văn bản (vd 'không đúng'='khong dung' trong thân luật bình thường → ASSEMBLED giả).
    name_norm = _strip_accents(source_name or "").lower().replace("_", " ")
    assembled = any(h in name_norm for h in _ASSEMBLED_HINTS)
    if assembled and not allow_provisional:
        flags.append("ASSEMBLED_VBHN_NOT_ALLOWED_AS_CANONICAL")
    if official_required:
        official_hit = any(h in norm for h in _OFFICIAL_HINTS)
        if not official_hit:
            flags.append("OFFICIAL_SOURCE_NOT_CONFIRMED")
        if not re.search(r"\[\d+\]", blob):
            flags.append("VBHN_FOOTNOTES_NOT_EVIDENT")
    return flags


def _vbhn_verdict(flags: list[str], allow_provisional: bool = False) -> tuple[str, bool, bool]:
    """Suy verdict tường minh từ flags: OFFICIAL_OK / PROVISIONAL / FAIL.
    official = qua gate sạch (không flags) và không phải bản tạm/tự ghép;
    provisional = chạy ở chế độ bản tạm (--allow-provisional) hoặc bị bắt là bản tự ghép."""
    flags = list(flags or [])
    provisional = bool(allow_provisional) or ("ASSEMBLED_VBHN_NOT_ALLOWED_AS_CANONICAL" in flags)
    official = (not flags) and not provisional
    verdict = "FAIL" if flags else ("OFFICIAL_OK" if official else "PROVISIONAL")
    return verdict, official, provisional


def _norm_compare_text(s: str) -> str:
    s = unicodedata.normalize("NFC", s or "")
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\s*\n\s*", "\n", s)
    return s.strip()


def _legal_refs(text: str) -> list[str]:
    """Rút các tham chiếu kiểu 'khoản 1 Điều 90' để bắt stale-ref trong bản tự ghép."""
    out = []
    for m in re.finditer(r"(?iu)\b(?:khoản\s+\d+\s+)?Điều\s+\d+\b", text or ""):
        ref = re.sub(r"\s+", " ", m.group(0).strip())
        if ref not in out:
            out.append(ref)
    return out


def _emit_json_payload(obj, out_path: str | None = None) -> None:
    """Emit JSON consistently; --out writes atomically so Cowork scripts can parse a file instead of long stdout/heredoc."""
    txt = _json_dumps(obj)   # v1.33.56 (review regression/F4): tôn trọng TL_DETERMINISTIC/--deterministic (mặc định OFF → output y cũ)
    if out_path:
        target = Path(out_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        _fd, _tmp = tempfile.mkstemp(prefix=target.name + ".", suffix=".tmp", dir=str(target.parent))
        with os.fdopen(_fd, "w", encoding="utf-8", errors="replace", newline="\n") as _f:   # v1.33.56 (F7)
            _f.write(txt + "\n")
        os.replace(_tmp, str(target))
        print(str(target))
    else:
        print(txt)


_PROFILE_ENV_OVERLAY_KEYS = ("TL_PROFILE", "TL_ROOT_FOLDER_ID", "TL_META_FOLDER_ID", "TL_NOTEBOOK_ID",
                             "TL_REGISTRY_DOC_ID", "TL_MANIFEST_ID", "TL_OVERFLOW_NOTEBOOK_ID",
                             "TL_CATEGORIES_MODE", "TL_MANIFEST_SCOPE", "TL_BASE_ALSO")


def _base_manifest_entries(config_path: str | None = None, refresh: bool = False) -> tuple[list[dict], str | None]:
    """A (v1.30.0): đọc entries manifest NỀN VBQPPL khi đang đứng ở profile dự án (TL_BASE_ALSO) — snapshot env
    overlay, đọc qua _profile_manifest_entries_for(vbqppl) rồi KHÔI PHỤC nguyên trạng (kể cả TL_PROFILE).
    Cache nền rơi đúng thư mục cache gốc (per-profile dir tách sẵn) — không nhiễm cache profile."""
    if _active_profile() == DEFAULT_PROFILE:
        return _profile_manifest_entries_for(DEFAULT_PROFILE, config_path, refresh)
    snap = {k: os.environ.get(k) for k in _PROFILE_ENV_OVERLAY_KEYS}
    try:
        return _profile_manifest_entries_for(DEFAULT_PROFILE, config_path, refresh)
    finally:
        for k, v in snap.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


class _ProfileEnvGuard:
    """Review v1.30.0 (CONFIRMED — load_creds(DEFAULT_PROFILE) nhiễm env cùng-process): các lệnh profile-ops
    (discover/adopt/doctor/index) ép scope NỀN để quét Drive → snapshot overlay profile khi VÀO và KHÔI PHỤC
    nguyên trạng khi RA (kể cả lỗi) — caller cùng-process (selftest/API/lệnh kế) không bị đổi TL_PROFILE ngầm.
    CLI chạy process riêng thì vô hại nhưng giữ bất biến cho chắc."""

    def __enter__(self):
        self._snap = {k: os.environ.get(k) for k in _PROFILE_ENV_OVERLAY_KEYS}
        return self

    def __exit__(self, *exc):
        for k, v in self._snap.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        return False


def _strip_shared_fixes(findings: list[dict], profiles: dict) -> list[dict]:
    """Review v1.30.0 (PURE, CONFIRMED): finding có fix-move nhưng fileId DÙNG CHUNG ≥2 profile → BỎ fix, nâng
    thành SHARED_ASSET_MULTI_PROFILE critical (move theo profile này = phá layout profile kia — tách asset trước)."""
    out = []
    for f in findings or []:
        if f.get("fix"):
            owners = _profile_asset_owners(profiles, f.get("fileId") or "")
            if len(owners) > 1:
                f = {k: v for k, v in f.items() if k != "fix"}
                f["check"] = "SHARED_ASSET_MULTI_PROFILE"
                f["severity"] = "critical"
                f["owners"] = owners
                f["note"] = (f"asset dùng chung {len(owners)} profile ({', '.join(owners)}) — KHÔNG auto-move "
                             "(phá layout profile kia); tách registry/manifest riêng trước (doctrine own-assets).")
        out.append(f)
    return out


def _notebook_from_manifest_json(mj: dict, profile_name: str) -> tuple[str, str | None]:
    """Review v1.30.0 (PURE, CONFIRMED): lấy notebookId từ manifest JSON CHỈ khi manifest thuộc ĐÚNG profile
    (trường 'profile' khớp tên/slug, so không-phân-biệt-hoa-thường) — manifest lạ lạc vào folder KHÔNG được phép
    cấp notebookId (nguy cơ ghi đè notebook đúng bằng notebook profile khác)."""
    mj = mj if isinstance(mj, dict) else {}
    nb = str(mj.get("notebookId") or mj.get("notebook_id") or "").strip()
    mp = str(mj.get("profile") or "").strip()
    if mp and _profile_file_slug(mp).lower() != _profile_file_slug(profile_name).lower():
        return "", (f"MANIFEST_PROFILE_MISMATCH: manifest ghi profile='{mp}' ≠ '{profile_name}' — KHÔNG lấy "
                    f"notebookId từ manifest này; truyền --notebook tường minh nếu chắc chắn.")
    return nb, None


def _manifest_placeholder(profile: str, root_id: str = "", notebook_id: str = "") -> dict:
    import datetime as _dt
    return {
        "version": EXPECT_VERSION,
        "schema": "uniform-v1",
        "profile": profile,
        "rootFolderId": root_id,
        "notebookId": notebook_id,
        "generatedAt": _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "treeHash": "",
        "count": 0,
        "corpus_count": 0,
        "entries": [],
    }


def _b64_text(s: str) -> str:
    import base64
    return base64.b64encode((s or "").encode("utf-8")).decode("ascii")


def _mime_from_info(info: dict) -> str:
    f = info.get("file") if isinstance(info.get("file"), dict) else {}
    return str(info.get("mime") or info.get("mimeType") or f.get("mimeType") or "").strip()


def _verify_registry_sheet(g, registry_id: str) -> dict:
    if not registry_id:
        return {"ok": False, "error": "REGISTRY_ID_EMPTY"}
    info = g.get("info", fileId=registry_id)
    mime = _mime_from_info(info) if isinstance(info, dict) else ""
    if mime and mime != REGISTRY_SHEET_MIME:
        return {"ok": False, "error": "REGISTRY_NOT_GOOGLE_SHEET", "registryDocId": registry_id, "mime": mime}
    add = g.get("reg_addcols", registryDocId=registry_id, confirm="yes")
    ok = bool(add.get("ok")) and int(add.get("cols") or 0) == len(REGISTRY_SCHEMA_COLS)
    return {
        "ok": ok,
        "registryDocId": registry_id,
        "mime": mime or REGISTRY_SHEET_MIME,
        "reg_addcols": add,
        "error": None if ok else (add.get("error") or "REGISTRY_SCHEMA_VERIFY_FAILED"),
    }


def _create_profile_registry_sheet(g, meta_id: str, profile: str) -> dict:
    slug = _profile_file_slug(profile)
    csv = ",".join(REGISTRY_SCHEMA_COLS) + "\n"
    up = g.post("upload", b64=_b64_text(csv), name=f"tra_luat_registry.{slug}.csv",
                mime="text/csv", folderId=meta_id, convert="false", register="false",
                share="false", force="true")
    csv_id = up.get("fileId") or up.get("id")
    if not csv_id:
        return {"ok": False, "step": "registry_csv_upload", "detail": up}
    cv = g.get("copy_convert", fileId=csv_id, name=f"tra_luat_registry.{slug}",
               folderId=meta_id, toType="sheets", register="false", share="false")
    reg_id = cv.get("fileId") or cv.get("id")
    if not reg_id:
        return {"ok": False, "step": "registry_sheet_convert", "csvFileId": csv_id, "detail": cv}
    ver = _verify_registry_sheet(g, reg_id)
    return {"ok": bool(ver.get("ok")), "csvFileId": csv_id, "registryDocId": reg_id,
            "convert": cv, "verify": ver, "error": ver.get("error")}


# ============ v1.30.0 — PROFILE OPS: discover (B) / adopt (C) / doctor (D) / index (E) ============
# BẤT BIẾN LAYOUT (D): registry + manifest của profile phải nằm TRONG thư mục profile (root hoặc _meta của nó).
# Sổ cái _PROFILES_INDEX (E) là BẢN CHIẾU đọc-được từ config — nguồn sự thật DUY NHẤT vẫn là config
# (tránh nguồn-sự-thật-thứ-4 trôi như sự cố 2026-06-30).

_PROFILES_INDEX_NAME = "_PROFILES_INDEX"


def _discover_item_kind(item: dict) -> str:
    """B (PURE): phân loại 1 item Drive (shape action `list`: {id,name,mime,type}) cho discovery/adopt.
    Nhận diện KHOAN DUNG các biến thể tên thật trên Drive: 'tra_luat_registry.LuatBHXH', 'Registry_NQ36',
    'tra_luat_registry' trơ, '_manifest_DinhMucChi.json', 'tra_luat_manifest.NQ36.json'."""
    name = str(item.get("name") or "")
    mime = str(item.get("mime") or item.get("mimeType") or "")
    if str(item.get("type") or "") == "folder" or mime.endswith("apps.folder"):
        return "folder"
    if name.startswith(_PROFILES_INDEX_NAME):
        return "index"    # sổ cái (E) = hạ tầng, KHÔNG phải asset profile lạc chỗ
    if re.match(r"^(tra_luat_registry|registry)([._\-]|$)", name, re.IGNORECASE):
        if mime == REGISTRY_SHEET_MIME:
            return "registry"
        return "registry_csv" if name.lower().endswith(".csv") else "registry_nonsheet"
    if re.search(r"manifest[\w.\-]*\.json$", name, re.IGNORECASE):
        return "manifest"
    return "other"


def _discover_scan_vbthuong(g, vbt_id: str, folder_cap: int = 60) -> dict:
    """B: quét Van_ban_thuong 2 cấp read-only qua GAS `list` — con trực tiếp + trong `_meta` của từng thư mục con
    (registry/manifest kiểu mới nằm trong _meta, kiểu cũ nằm thẳng trong folder). Cap thư mục quét, LOUD khi cắt."""
    top = _gas_get_retry(g, "list", folderId=vbt_id)
    items = top.get("items") or []
    root_files = [x for x in items if str(x.get("type")) != "folder"]
    subfolders = [x for x in items if str(x.get("type")) == "folder"]
    out_folders = []
    for fo in subfolders[:folder_cap]:
        try:
            sitems = _gas_get_retry(g, "list", folderId=fo.get("id")).get("items") or []
        except Exception:
            sitems = []
        meta = next((x for x in sitems if str(x.get("type")) == "folder" and str(x.get("name")) == "_meta"), None)
        if meta:
            try:
                sitems = sitems + (_gas_get_retry(g, "list", folderId=meta.get("id")).get("items") or [])
            except Exception:
                pass
        out_folders.append({"id": fo.get("id"), "name": fo.get("name"), "items": sitems,
                            "meta_folder_id": (meta or {}).get("id")})
    return {"ok": True, "vbt_id": vbt_id, "folders": out_folders, "root_files": root_files,
            "capped": len(subfolders) > folder_cap, "folder_total": len(subfolders)}


def _adopt_pick_assets(items: list[dict], reg_override: str = "", man_override: str = "") -> dict:
    """C (PURE, test offline): chọn registry Sheet + manifest JSON từ items (con folder + _meta). Override thắng.
    Nhiều ứng viên không override → AMBIGUOUS (bắt người chọn — KHÔNG đoán); tên-registry-nhưng-không-Sheet → chặn."""
    regs, mans, reg_nonsheet = [], [], []
    for it in items or []:
        k = _discover_item_kind(it)
        if k == "registry":
            regs.append(it)
        elif k == "manifest":
            mans.append(it)
        elif k == "registry_nonsheet":
            reg_nonsheet.append(it)
    out = {"registry_candidates": [{"id": x.get("id"), "name": x.get("name")} for x in regs],
           "manifest_candidates": [{"id": x.get("id"), "name": x.get("name")} for x in mans],
           "registry_nonsheet": [{"id": x.get("id"), "name": x.get("name")} for x in reg_nonsheet],
           "registry": None, "manifest": None, "errors": []}
    if reg_override:
        out["registry"] = {"id": reg_override, "name": "(override --registry)"}
    elif len(regs) == 1:
        out["registry"] = {"id": regs[0].get("id"), "name": regs[0].get("name")}
    elif len(regs) > 1:
        out["errors"].append("REGISTRY_AMBIGUOUS: nhiều registry Sheet trong thư mục — truyền --registry <id>.")
    elif reg_nonsheet:
        out["errors"].append("REGISTRY_NOT_SHEET: thấy file tên registry nhưng KHÔNG phải Google Sheet "
                             "(Doc/legacy?) — bài học CLOBBER: Doc-as-Sheet đọc RỖNG. Truyền --registry <Sheet thật>.")
    else:
        out["errors"].append("REGISTRY_NOT_FOUND: không thấy tra_luat_registry*/Registry_* (Sheet) trong thư mục/_meta — "
                             "truyền --registry <id> (vd asset lạc gốc từ --discover) hoặc dựng mới bằng profile-create.")
    if man_override:
        out["manifest"] = {"id": man_override, "name": "(override --manifest)"}
    elif len(mans) == 1:
        out["manifest"] = {"id": mans[0].get("id"), "name": mans[0].get("name")}
    elif len(mans) > 1:
        std = [m for m in mans if str(m.get("name") or "").lower().startswith("tra_luat_manifest")]
        if len(std) == 1:
            out["manifest"] = {"id": std[0].get("id"), "name": std[0].get("name")}
        else:
            out["errors"].append("MANIFEST_AMBIGUOUS: nhiều *manifest*.json — truyền --manifest <id>.")
    else:
        out["errors"].append("MANIFEST_NOT_FOUND: không thấy *manifest*.json — truyền --manifest <id>, "
                             "hoặc --bootstrap-manifest để sinh mới từ registry sẵn có.")
    return out


_PROFILES_INDEX_COLS = ["profile", "default", "rootFolderId", "folder_name", "notebookId", "registryDocId",
                        "manifestId", "categories", "manifestScope", "baseAlso", "note"]


def _index_old_candidates(items: list[dict]) -> list[dict]:
    """Review v1.30.0 (PURE, CONFIRMED): bản index CŨ cần dọn = TÊN CHÍNH XÁC `_PROFILES_INDEX` (Sheet) /
    `_PROFILES_INDEX.csv` — KHÔNG startswith (file người dùng đặt `_PROFILES_INDEX_backup…` từng có nguy cơ trash nhầm)."""
    keep = {_PROFILES_INDEX_NAME, f"{_PROFILES_INDEX_NAME}.csv"}
    return [x for x in (items or []) if str(x.get("name") or "") in keep]


INSTRUCTION_REQUIRED = {
    "SKILL_OF_RECORD": "Instruction phải nêu skill tra-luat là nguồn quy tắc cho phiên ghi/nạp.",
    "ingest_handoff": "Instruction phải chuyển research_* thành discovery-only và handoff sang QT-3.",
    "confirm_gate_web": "Instruction phải có cổng xác nhận riêng trước khi nạp web/corpus/NLM.",
    "research_import": "Instruction phải nhắc rõ research_import không được nạp thẳng VBQPPL.",
    "source_add(url)": "Instruction phải nhắc rõ source_add(url) không được nạp thẳng VBQPPL.",
    "QT-3": "Instruction phải buộc tải/convert/đặt tên/sắp xếp/verify trước nlm_push.",
    "notebook đang dùng": "Instruction phải mặc định dùng corpus/folder/notebook đang dùng.",
    "docx": "Instruction phải ưu tiên docx/GDoc-convertible hơn PDF.",
    "official-first": "Instruction phải giữ nguyên tắc nguồn chính thức trước.",
    "download_link_priority": "Instruction phải phân biệt link tải người dùng với canonical official-first.",
    "corpus_profile": "Instruction phải nêu profile đa-corpus và không mặc định VBQPPL cho văn bản thường.",
    "manifest_fallback": "Instruction phải nêu manifest profile-first, fallback VBQPPL và cross_notebook_query.",
    "cross_notebook_query": "Instruction phải nhắc QA xuyên corpus.",
    "nlm_notebook_id": "Instruction phải nhắc slot theo notebook đích.",
    "verify nguyên văn": "Instruction phải buộc kiểm chứng bằng nguyên văn.",
    "VBHN-first": "Instruction phải giữ nguyên tắc VBHN-first.",
    "DỰ THẢO": "Instruction phải cảnh báo dự thảo chưa hiệu lực.",
    "source id": "Instruction phải neo về source id/drive_id.",
    "Điều": "Instruction phải neo về Điều/khoản/điểm.",
}


# ═════════════════ WS1: bộ giải danh tính chuẩn hóa + alias (dùng chung) ═════════════════
# Alias chỉ để MỞ RỘNG ứng viên — KHÔNG tự chốt. Sau khi khớp vẫn phải verify số hiệu+năm+loại+dòng đầu.
_ALIASES = [
    ("bo luat lao dong", ["blld", "bo luat lao dong"]),
    ("bo luat hinh su", ["blhs", "bo luat hinh su"]),
    ("bo luat dan su", ["blds", "bo luat dan su"]),
    ("bo luat to tung hinh su", ["bltths"]),
    ("bo luat to tung dan su", ["blttds"]),
    ("bao hiem xa hoi", ["bhxh", "bao hiem xa hoi"]),
    ("bao hiem y te", ["bhyt", "bao hiem y te"]),
    ("an toan ve sinh lao dong", ["atvsld", "an toan ve sinh lao dong"]),
    ("nguoi lao dong", ["nld", "nguoi lao dong"]),
    ("giao duc nghe nghiep", ["gdnn", "giao duc nghe nghiep"]),
    ("giao duc dai hoc", ["gddh"]),
    ("phong chong tham nhung", ["pctn", "phong chong tham nhung"]),
    ("ngan sach nha nuoc", ["nsnn", "ngan sach nha nuoc"]),
    ("doanh nghiep", ["dn", "doanh nghiep"]),
    ("dau tu cong", ["dtc", "dau tu cong"]),
    ("xu ly vi pham hanh chinh", ["xlvphc"]),
    ("kham benh chua benh", ["kbcb", "kham benh chua benh"]),
    ("binh dang gioi", ["bdg", "binh dang gioi"]),
]
_ALIAS_INDEX = None


def _alias_terms(s: str) -> set:
    """Trả tập term chuẩn hóa của s, MỞ RỘNG theo alias 2 chiều (BHXH↔bao hiem xa hoi…)."""
    global _ALIAS_INDEX
    if _ALIAS_INDEX is None:
        _ALIAS_INDEX = {}
        for canon, abbrs in _ALIASES:
            members = set([canon] + abbrs)
            for m in members:
                _ALIAS_INDEX.setdefault(m, set()).update(members)
    plain = _strip_accents(str(s or "")).lower()
    terms = {plain}
    for m, group in _ALIAS_INDEX.items():
        if m and m in plain:
            terms |= group
    return {t for t in terms if t}


def resolve_identity(q: str, entries: list, max_hits: int = 8) -> list:
    """Giải danh tính chuẩn hóa: khớp qua SỐ HIỆU (chuẩn hóa) → tên/name_key → alias trên
    _entry_subject_text (gồm name+title_vn+trichyeu+TUKHOA+nlm_title+cat). Trả [(entry, score, reasons)]
    đã xếp hạng. Đây là bộ DÙNG CHUNG cho exists/source-map/dedup/xref/ingest-route (WS1)."""
    key = norm_sohieu(q)
    qn = _strip_accents(q).lower()
    qnk = _name_key(q)
    aterms = _alias_terms(q)
    out = []
    for e in entries:
        sh = norm_sohieu(_entry_sohieu(e))
        subj = _strip_accents(_entry_subject_text(e)).lower()
        nm = _strip_accents(_entry_name(e)).lower()
        nk = _name_key(_entry_name(e))
        score, reasons = 0, []
        if key and sh and sh == key:
            score += 100; reasons.append("sohieu")
        if qn and len(qn) >= 4 and qn in nm:
            score += 40; reasons.append("name_substr")
        if qnk and nk and (qnk in nk or nk in qnk):
            score += 30; reasons.append("name_key")
        hit_alias = [t for t in aterms if len(t) >= 3 and t in subj]
        if hit_alias:
            score += 20 + min(len(hit_alias), 3)
            reasons.append("alias/tukhoa:" + ",".join(sorted(hit_alias)[:3]))
        # B2 (port Codex): khớp tên theo TOKEN-subset (gồm subject) → bắt 'Luật Thư viện'↔'Luat_46-2019-QH14_Thu_vien'
        # khi substring/name_key hổng (số hiệu chèn giữa). Tăng độ tất định của dedup-check/identity resolver.
        if _entry_query_match(q, e, include_subject=True):
            score += 35; reasons.append("name_tokens")
        if score > 0:
            out.append((e, score + _entry_score(e) // 10, reasons))
    out.sort(key=lambda t: t[1], reverse=True)
    return out[:max_hits]


# ═════════════════ WS2: Reference Integrity engine (tl xref) ═════════════════
_LOAI_WORDS = r"(?:Bộ luật|Luật|Pháp lệnh|Nghị định|Thông tư|Nghị quyết|Quyết định)"
_SOHIEU_RE = re.compile(r"\b(\d{1,4}/\d{4}/[A-ZĐ][A-Z0-9Đ\-]*)")
_REF_RE = re.compile(
    r"(?P<loai>" + _LOAI_WORDS + r")\s+(?P<name>[^.;:,\n(]{0,80}?)?\s*(?:số\s+)?(?P<sh>\d{1,4}/\d{4}/[A-ZĐ][A-Z0-9Đ\-]*)",
    re.IGNORECASE | re.UNICODE)


# B (log rà 71 luật): mệnh đề CHUYỂN TIẾP/tự-quy-chiếu lẫn vào name_phrase (regex bắc qua "Luật NÀY có hiệu
# lực thi hành thì…") → name_phrase ảo. Cắt tại các mốc prose CHẮC CHẮN không xuất hiện trong tên luật thật
# (KHÔNG dùng 'thi hành'/'thì' vì có trong tên: "Luật Thi hành án dân sự").
_REF_PROSE_RE = re.compile(
    r"(?iu)(\bnày\b|nêu trên|nói trên|có hiệu lực|thực hiện theo|quy định tại|được sửa đổi|được bổ sung|được thay thế)")


def extract_refs(text: str) -> list:
    """Bóc các viện dẫn 'Luật/Bộ luật/… [số hiệu]' trong thân + footnote. NFC-normalize trước.
    Trả [{raw, name_phrase, sohieu, loai}] — DEDUP theo SỐ HIỆU (P1-3: MỘT phán quyết / số hiệu / run; B: hết
    'phantom' 1 số hiệu xuất hiện 2-3 lần do mệnh đề chuyển tiếp). name_phrase đã cắt prose; giữ bản SẠCH nhất."""
    txt = unicodedata.normalize("NFC", text or "")
    by_sh: dict[str, dict] = {}
    for m in _REF_RE.finditer(txt):
        sh = norm_sohieu(m.group("sh"))
        if not sh:
            continue
        name = _clean_ref_name_phrase((m.group("name") or "").strip(" -–—\t"))
        rec = {"raw": m.group(0).strip()[:90], "name_phrase": name, "sohieu": sh,
               "loai": (m.group("loai") or "").strip()}
        prev = by_sh.get(sh)
        # Giữ MỘT bản / số hiệu: ưu tiên bản có name_phrase (sau khi cắt prose) hơn bản rỗng; giữa 2 tên → bản ĐẦU.
        if prev is None or (not prev.get("name_phrase") and rec["name_phrase"]):
            by_sh[sh] = rec
    return list(by_sh.values())


_SOHIEU_PARTS_RE = re.compile(r"^(\d{1,4})-(\d{4})-(.+)$")


def _sohieu_num_typo(a: str, b: str) -> bool:
    """True nếu số thứ tự a↔b chênh đúng 1 ký tự (thay 1 chữ số) hoặc đảo 2 chữ số liền kề."""
    if len(a) != len(b) or a == b:
        return False
    diff = [i for i in range(len(a)) if a[i] != b[i]]
    if len(diff) == 1:
        return True
    return (len(diff) == 2 and diff[1] == diff[0] + 1
            and a[diff[0]] == b[diff[1]] and a[diff[1]] == b[diff[0]])


def _doctype_family(agency: str) -> str:
    """P0-2 (log rà 71 luật): HỌ loại văn bản theo mã cơ quan trong số hiệu. Dùng để CHẶN gợi ý
    DOC_TEXT_SOHIEU_TYPO VƯỢT BIÊN họ — tái dùng SỐ+NĂM giữa Luật QH ↔ NQ-TW/KL-TW (Đảng) ↔ NĐ-CP (Chính phủ)
    là HỢP PHÁP, KHÔNG phải gõ nhầm (vd 29/2013/QH13 ≠ 29/2013/NQ-TW). Chỉ flag typo trong CÙNG họ (QH14↔QH15)."""
    a = _strip_accents(agency or "").upper().replace(" ", "")
    if "TW" in a:                                   # NQ-TW/KL-TW/QD-TW/CT-TW — văn bản của Đảng
        return "TW"
    if "VPQH" in a or re.search(r"QH\d", a) or a in ("QH", "LCT-HDNN8") or "UBTVQH" in a or "-PL-" in a or a.startswith("PL-"):
        return "QH"                                 # Quốc hội / UBTVQH / VBHN-VPQH / Pháp lệnh / Lệnh CTN
    if "CP" in a:                                   # ND-CP / NQ-CP — Chính phủ
        return "CP"
    if "TTG" in a:                                  # QD-TTg — Thủ tướng
        return "TTG"
    if a.startswith("TT") or "TTLT" in a or re.search(r"-B[A-Z]{2,}", a):  # Thông tư / TTLT / QĐ-Bộ
        return "TT"
    return a or "?"                                 # mã lạ → chính nó (khác mọi họ trên → KHÔNG bắc cầu)


def _sohieu_typo_near(cited: str, entries: list, name_q: str = ""):
    """Số hiệu dẫn-chiếu KHÔNG khớp exact nhưng CÓ near-match trong corpus → (entry, sohieu) gợi ý.
    (1) cùng SỐ+NĂM, KHÁC mã cơ quan/loại (vd QH14↔QH15) = typo mã, không cần đối chiếu tên.
    (2) cùng NĂM+mã, số thứ tự lệch 1 chữ số = typo số, CHỈ nhận khi tên (loai+name) đối chiếu DUY NHẤT 1 ứng viên (tránh dương tính giả)."""
    m = _SOHIEU_PARTS_RE.fullmatch(cited or "")
    if not m:
        return None
    cn, cy, ca = m.group(1), m.group(2), m.group(3)
    agency_hit, num_cands = None, []
    for e in entries:
        sh = norm_sohieu(_entry_sohieu(e))
        if sh == cited:
            return None   # số hiệu dẫn TỒN TẠI đúng → không phải typo
        em = _SOHIEU_PARTS_RE.fullmatch(sh)
        if not em:
            continue
        en, ey, ea = em.group(1), em.group(2), em.group(3)
        # P0-2: cùng SỐ+NĂM, KHÁC mã cơ quan = typo CHỈ KHI cùng HỌ loại văn bản (QH14↔QH15). Khác họ
        # (QH ↔ NQ-TW/NĐ-CP…) = tái dùng số+năm hợp pháp → KHÔNG phải typo (hết gợi ý ảo xuyên-không-gian).
        if en == cn and ey == cy and ea != ca and _doctype_family(ca) == _doctype_family(ea):
            agency_hit = (e, sh)
        elif ey == cy and ea == ca and _sohieu_num_typo(cn, en):
            num_cands.append((e, sh))
    if agency_hit:
        return agency_hit
    if name_q and num_cands:
        hit_ids = {id(e) for e, _s, _r in resolve_identity(name_q, entries, max_hits=8)}
        corro = [(e, sh) for e, sh in num_cands if id(e) in hit_ids]
        if len(corro) == 1:
            return corro[0]
    return None


def _vbhn_for_goc(sohieu_key: str, entries: list) -> list:
    """Các entry VBHN/bản hợp nhất có 'goc' chứa số hiệu này → tín hiệu OUTDATED."""
    out = []
    for e in entries:
        goc = e.get("goc")
        gtxt = json.dumps(goc, ensure_ascii=False) if isinstance(goc, (list, dict)) else str(goc or "")
        if sohieu_key and norm_sohieu(sohieu_key).replace("/", "-") in norm_sohieu(gtxt).replace("/", "-"):
            if _is_vbhn_entry(e) or "VBHN" in gtxt.upper():
                out.append(e)
    return out


# ═════════════════ B3: footnote-resolver (bản đồ sửa đổi cấp Điều trong VBHN) ═════════════════
_DIEU_HEAD_RE = re.compile(r"^\s*Điều\s+(\d+[a-zđ]?)\b", re.IGNORECASE)
_KHOAN_HEAD_RE = re.compile(r"^\s*(\d+[a-zđ]?)\s*[\.\)]")   # L1: khoản có hậu tố chữ (8a, 154 K8a…)
_MARK_RE = re.compile(r"\[(\d{1,3})\]")
_HL_DATE_RE = re.compile(r"hiệu lực[^0-9]{0,40}?(\d{1,2})\s*[/\-.]\s*(\d{1,2})\s*[/\-.]\s*(\d{4})", re.IGNORECASE)
# VBHN dùng chữ: "có hiệu lực kể từ ngày 01 tháng 7 năm 2026" → bắt riêng (đây là gốc lỗi pending=0).
_HL_DATE_VN_RE = re.compile(r"hiệu lực[^0-9]{0,40}?ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})", re.IGNORECASE)


def _date_from_effect_match(m) -> str | None:
    if not m:
        return None
    return f"{int(m.group(3)):04d}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"


def resolve_body_effective_dates(text: str, today: str | None = None) -> list[dict]:
    """Parse mệnh đề hiệu lực trong THÂN văn bản, không chỉ footnote VBHN.

    Dùng để bắt luật gốc mới có Điều hiệu lực tương lai (vd "Luật này có hiệu lực
    từ ngày..." và ngoại lệ "điểm c, d khoản 1 Điều 14 có hiệu lực...").
    """
    import datetime as _dt
    today = today or _dt.date.today().isoformat()
    txt = unicodedata.normalize("NFC", text or "")
    chunks = re.split(r"(?<=[.;])\s+|\n+", txt)
    out, seen = [], set()
    for raw in chunks:
        clause = re.sub(r"\s+", " ", raw).strip()
        if "hiệu lực" not in clause.lower():
            continue
        for dm in (_HL_DATE_RE.search(clause), _HL_DATE_VN_RE.search(clause)):
            hl = _date_from_effect_match(dm)
            if not hl:
                continue
            key = (hl, clause[:160])
            if key in seen:
                continue
            seen.add(key)
            positions = []
            for pm in _POS_RE.finditer(clause):
                positions.append(" ".join(p for p in [
                    ("điểm " + pm.group(1)) if pm.group(1) else None,
                    ("khoản " + pm.group(2)) if pm.group(2) else None,
                    ("Điều " + pm.group(3)) if pm.group(3) else None,
                ] if p))
            out.append({
                "scope": clause[:240],
                "positions": positions,
                "hieu_luc": hl,
                "pending_effect": hl > today,
                "source": "body_effective_clause",
            })
    return out


# B1 def-driven (26/6): parse 1 chú thích thành bản ghi sửa đổi ĐỘC LẬP.
# B3 (84/2025): nhận thêm "Cụm từ '…' được BỎ / THAY THẾ BẰNG '…' theo…" (verb 'bỏ'/'thay thế' yêu cầu được/bị
# đứng trước → tránh dương-tính-giả với 'bỏ' lẻ). Giữ nguyên các verb cũ (alt sau) cho tương thích.
_AMEND_VERB_RE = re.compile(
    r"(?:được|bị)\s*(?:bỏ|thay thế(?:\s+bằng)?)\b"
    r"|(?:được|bị)?\s*(sửa đổi(?:,?\s*bổ sung)?|bổ sung|bãi bỏ|thay thế|hủy bỏ)\b", re.IGNORECASE)
_POS_RE = re.compile(r"(?:điểm\s+([a-zđ]{1,3}\d?)\s+)?(?:khoản\s+(\d+[a-zđ]?)\s+)?Điều\s+(\d+[a-zđ]?)", re.IGNORECASE)
_AMEND_LAW_RE = re.compile(r"của\s+(?:Bộ\s+luật|Luật)\b[^0-9]{0,90}?số\s+(\d{1,4}\s*/\s*\d{4}\s*/\s*[A-ZĐa-zđ\-]+\d*)", re.IGNORECASE)
_DIEMLIST_RE = re.compile(r"diem\s+([a-z]{1,3}\d?(?:\s*(?:,|va|;)\s*(?:diem\s+)?[a-z]{1,3}\d?)+)")


def _multi_diem(target_clause: str, single):
    """footnote_multidiem: _POS_RE chỉ bắt 1 điểm (sát khoản) → "điểm c VÀ điểm d khoản 2 Điều 30" rơi mất "c".
    Bắt CẢ DÃY điểm đích → trả "c và d"; không phải dãy → giữ `single` (1 điểm) như cũ."""
    if not target_clause:
        return single
    s = _strip_accents(target_clause).lower()
    m = _DIEMLIST_RE.search(s)
    if m:
        items, seen = re.findall(r"\b([a-z]{1,3}\d?)\b", m.group(1)), []
        for x in items:
            if x not in ("va",) and x not in seen:
                seen.append(x)
        if len(seen) >= 2:
            return " và ".join(seen)
    return single


def _entry_hieuluc_date(e: dict | None) -> str | None:
    """B2 fallback: lấy ngày hiệu lực ISO từ field hieuluc của registry (nếu có dạng dd/mm/yyyy)."""
    s = str((e or {}).get("hieuluc") or (e or {}).get("hieu_luc") or "")
    m = re.search(r"(\d{1,2})\s*[/\-.]\s*(\d{1,2})\s*[/\-.]\s*(\d{4})", s)
    return f"{int(m.group(3)):04d}-{int(m.group(2)):02d}-{int(m.group(1)):02d}" if m else None


def _hieuluc_date_display(iso: str | None) -> str:
    if not iso:
        return ""
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", str(iso))
    return f"{m.group(3)}/{m.group(2)}/{m.group(1)}" if m else str(iso)


def _hieuluc_from_header_text(text: str, today: str | None = None, infer_from_date: bool = False) -> tuple[str, str]:
    """Bóc trạng thái hiệu lực từ header/text đã export. Mặc định chỉ tin nhãn trạng thái rõ; date-only cần opt-in."""
    import datetime as _dt
    today = today or _dt.date.today().isoformat()
    head = unicodedata.normalize("NFC", text or "")
    head = "\n".join(head.splitlines()[:160])
    plain = _strip_accents(head).lower()
    status = ""
    if re.search(r"\b(khong\s+con\s+hieu\s+luc|het\s+hieu\s+luc|ngung\s+hieu\s+luc|da\s+het\s+hieu\s+luc)\b", plain):
        status = "Hết hiệu lực"
    elif re.search(r"\b(chua\s+co\s+hieu\s+luc|chua\s+hieu\s+luc|chua\s+den\s+hieu\s+luc)\b", plain):
        status = "Chưa có hiệu lực"
    elif re.search(r"\b(con\s+hieu\s+luc|dang\s+co\s+hieu\s+luc)\b", plain):
        status = "Còn hiệu lực"
    iso = _date_from_effect_match(_HL_DATE_RE.search(head)) or _date_from_effect_match(_HL_DATE_VN_RE.search(head))
    if not iso:
        body_dates = resolve_body_effective_dates(head, today=today)
        iso = (body_dates[0].get("hieu_luc") if body_dates else None)
    if status:
        ds = _hieuluc_date_display(iso)
        return (f"{status}; hiệu lực từ {ds}" if ds else status), ""
    if infer_from_date and iso:
        ds = _hieuluc_date_display(iso)
        status = "Chưa có hiệu lực" if iso > today else "Còn hiệu lực"
        return f"{status}; hiệu lực từ {ds}", ""
    return "", "NO_EFFECTIVE_STATUS"


_INLINE_AMEND_RE = re.compile(
    r"(?:Sửa đổi(?:,?\s*bổ sung)?|Bổ sung)\s+(?:một số điều của\s+)?"
    r"(?:Bộ\s+luật|Luật|Pháp lệnh|Nghị quyết)\s+(?:[^.;:\n0-9]{0,60}?)\s*"
    r"số\s+(?P<sh>\d{1,4}/\d{4}/[A-ZĐ][A-Z0-9Đ\-]*)", re.IGNORECASE | re.UNICODE)


def _scan_inline_amendments(text: str) -> list:
    """E1 liên-domain: số hiệu luật KHÁC bị base sửa cấp Điều (outgoing) từ tiêu đề điều-khoản-thi-hành
    "Sửa đổi, bổ sung [một số điều của] Luật ... số <sh>". KHÔNG bắt repeal "Bãi bỏ ... của Luật ... số X"
    (động từ sửa phải liền trước "Luật") hay recital "Luật số X đã được sửa đổi". Trả list sohieu chuẩn hoá, dedup."""
    out, seen = [], set()
    for m in _INLINE_AMEND_RE.finditer(unicodedata.normalize("NFC", text or "")):
        sh = norm_sohieu(m.group("sh"))
        if sh and sh not in seen:
            seen.add(sh); out.append(sh)
    return out


# BUG#4: chú thích sửa đổi CẮT-NGANG / BÃI-BỎ-CỤC-BỘ phải HẠ ƯU TIÊN trong footnote-map — đừng để ngang hàng luật
# sửa chuyên đề (dễ hiểu nhầm phải nạp cả luật quy hoạch/thanh tra/omnibus). Phát hiện TỪ NGUYÊN VĂN chú thích:
#   CROSS_CUTTING = luật sửa "một số điều của <N>/các/nhiều luật" hoặc "<N> luật … có liên quan" (35/2018 quy hoạch…).
#   PARTIAL_REPEAL = loại='bãi bỏ' VÀ phạm vi hẹp (chỉ 1 khoản/điểm, không bãi cả Điều) — vd 32/2013 bỏ 1 khoản TNDN.
_FOOTNOTE_CROSSCUT_RE = re.compile(
    r"(?:mot so dieu cua\s+(?:\d+|cac|nhieu)\s+luat|"
    r"sua doi,?\s*bo sung\s+(?:\d+|mot so|cac|nhieu)\s+luat|"
    r"\d+\s+luat\b|cac luat\b|nhieu luat\b|luat\b[^.]{0,40}\bco lien quan)",
    re.IGNORECASE)


def resolve_footnote_amendments(text: str, today: str | None = None, entries: list | None = None) -> dict:
    """B3 def-driven: MỖI chú thích '[n] …' = 1 bản ghi ĐỘC LẬP (không mượn số/đích/luật marker khác).
    B2: hiệu_lực từ chú thích ('có hiệu lực kể từ ngày…') hoặc registry (entries) theo số hiệu luật sửa; pending_effect = hl>today."""
    import datetime as _dt
    txt = unicodedata.normalize("NFC", text or "")
    # L1: tách dấu dính số-khoản↔số-chú-thích
    txt = re.sub(r"(\d+)\.(\d+[a-zđ]?)\s*\[(\d{1,3})\]", r"\1.\2 [\3]", txt)
    txt = re.sub(r"(?<=[\dA-Za-zđ])\[(\d{1,3})\]", r" [\1]", txt)
    txt = re.sub(r"\[(\d{1,3})\](\d)", r"[\1] \2", txt)
    today = today or _dt.date.today().isoformat()
    # Khối CHÚ THÍCH = từ dòng bắt đầu '[n]' đầu tiên (def ở line-start; marker inline trong thân ở giữa dòng)
    first = re.search(r"(?m)^\s*\[\d{1,3}\]\s", txt)
    foot_region = txt[first.start():] if first else ""
    body_txt = txt[: first.start()] if first else txt
    # body-anchor fallback: marker inline trong thân → Điều/khoản đang theo dõi
    anchor, cur_dieu, cur_khoan = {}, None, None
    for line in body_txt.splitlines():
        dh = _DIEU_HEAD_RE.match(line)
        if dh: cur_dieu = dh.group(1); cur_khoan = None
        kh = _KHOAN_HEAD_RE.match(line)
        if kh: cur_khoan = kh.group(1)
        for mk in _MARK_RE.finditer(line):
            anchor.setdefault(mk.group(1), (cur_dieu, cur_khoan))
    # Tách def THEO MARKER (không phụ thuộc xuống dòng): mỗi [n] → tới [next]
    rows, processed = [], set()
    marks = [(m.start(), m.end(), m.group(1)) for m in _MARK_RE.finditer(foot_region)]
    bracketed = {n for _, _, n in marks}
    # Một số def đánh marker SỐ TRẦN đầu dòng (vd [2] bị viết "\n2 Điểm này được sửa đổi…") → _MARK_RE bỏ sót.
    # CHỈ cứu cho số CÓ anchor trong thân (là footnote thật) + theo sau là ngôn ngữ def (Điểm/Khoản/Điều/Cụm từ).
    for am in anchor:
        if am in bracketed:
            continue
        bm = re.search(r"(?:^|\n)[ \t]*" + re.escape(am) + r"[ \t]+(?=(?:Điểm|Khoản|Điều|Cụm từ)\b)", foot_region)
        if bm:
            marks.append((bm.start(), bm.end(), am))
    marks.sort()
    max_foot = max((int(n) for _, _, n in marks if n.isdigit()), default=0)
    for i, (mstart, mend, n) in enumerate(marks):
        if n in processed:
            continue
        processed.add(n)                                   # đánh dấu ĐÃ XỬ LÝ (kể cả bỏ) để body-loop không lặp
        end = marks[i + 1][0] if i + 1 < len(marks) else len(foot_region)
        body = re.sub(r"\s+", " ", foot_region[mend:end]).strip()
        rec = _parse_footnote_def(n, body)
        if "căn cứ ban hành" in body.lower():              # Type C: chỉ căn cứ ban hành → KHÔNG sửa đổi ([1])
            continue
        if not rec.get("is_amend"):
            # is_amend=False = def TRÍCH DẪN (vd "Điều 50 của Luật 71/2025 quy định như sau: 'Điều 50. Hiệu lực
            # thi hành…'") — KHÔNG phải sửa đổi cấp Điều. BỎ. (Trước đây Type-B anchor-recovery gắn nhầm vào Điều
            # gần nhất — vd [6] marker nằm trên TIÊU ĐỀ CHƯƠNG "ĐIỀU KHOẢN THI HÀNH" sau Điều 217 → false-positive
            # "Điều 217 ← 71/2025"; đã bỏ. Amendment THẬT luôn có động-từ-sửa trong def → is_amend=True.)
            continue
        if not rec["dieu"] and n in anchor:                # Type A: anchor-fallback khi def thiếu Điều
            rec["dieu"], rec["khoan"] = anchor[n][0], rec["khoan"] or anchor[n][1]
        if not (rec["dieu"] or rec["amending_sohieu"]):
            continue
        rows.append(rec)
    # Marker trong THÂN nhưng KHÔNG có def ở foot_region (vd [2] ở Điều 59) → emit đích từ anchor, NGUỒN chưa rõ.
    for n, (ad, ak) in anchor.items():
        if n not in processed and ad and n.isdigit() and int(n) <= max_foot:
            rows.append({"marker": n, "dieu": ad, "khoan": ak, "diem": None, "is_amend": True,
                         "amending_sohieu": None, "amending_vitri": None, "hieu_luc": None,
                         "loai": "", "footnote": "", "def_missing": True})
            processed.add(n)
    # B2: điền hiệu_lực còn thiếu từ registry theo số hiệu luật sửa
    if entries:
        idx = {norm_sohieu(_entry_sohieu(e)): e for e in entries if _entry_sohieu(e)}
        for r in rows:
            if not r.get("hieu_luc") and r.get("amending_sohieu"):
                hl = _entry_hieuluc_date(idx.get(r["amending_sohieu"]))
                if hl: r["hieu_luc"] = hl
    for r in rows:
        r["pending_effect"] = bool(r.get("hieu_luc") and r["hieu_luc"] > today)
        r["rel_kind"] = _footnote_rel_kind(r)   # BUG#4: HẠ ƯU TIÊN omnibus cắt-ngang / bãi-bỏ-cục-bộ
    rows.sort(key=lambda r: int(r["marker"]) if r["marker"].isdigit() else 999)
    # A2 (log1): footnote phát mỗi marker[n] thành 1 dòng → cùng (Điều,Khoản,Điểm,luật-sửa) bị đếm 2-3 lần (vd Đ73K1 ×3 =47 dòng
    # trùng/316). GOM theo khoá (dieu,khoan,diem,amending_sohieu) cho MAP cấp-Điều + đếm pending. footnote_defs giữ ĐỦ marker.
    _seen_dl, dieu_rows = set(), []
    for r in rows:
        k = (r.get("dieu"), r.get("khoan"), r.get("diem"), r.get("amending_sohieu"))
        if k in _seen_dl:
            continue
        _seen_dl.add(k); dieu_rows.append(r)
    # L3: chuỗi hợp nhất CỦA CHÍNH VBHN (cho B1 không-OUTDATED + B2 rel_type)
    mapped_sohieu = {r["amending_sohieu"] for r in rows if r.get("amending_sohieu")}
    footnote_sohieu = {norm_sohieu(m.group(1)) for m in _SOHIEU_RE.finditer(foot_region)}
    hdr_end = re.search(r"(?m)^\s*(Chương\s+[IVX]+\b|Điều\s+1\b)", body_txt)
    header = body_txt[: hdr_end.start()] if hdr_end else body_txt[:2000]
    header_sohieu = {norm_sohieu(m.group(1)) for m in _SOHIEU_RE.finditer(header)}
    body_effective = resolve_body_effective_dates(body_txt, today=today)
    body_pending = sum(1 for r in body_effective if r.get("pending_effect"))
    footnote_pending = sum(1 for r in dieu_rows if r.get("pending_effect"))   # A2: đếm trên bản ĐÃ GOM (không trùng)
    return {"today": today, "footnote_count": len(dieu_rows), "footnote_raw_count": len(rows),
            "pending_effect_count": footnote_pending + body_pending,   # tổng pending (footnote + thân Điều hiệu lực)
            "footnote_pending_effect_count": footnote_pending,
            "body_pending_effect_count": body_pending,
            "body_effective_dates": body_effective,
            "footnote_defs": {r["marker"]: r for r in rows}, "dieu_level_amendment_map": dieu_rows,
            "mapped_sohieu": sorted(mapped_sohieu), "footnote_sohieu": sorted(footnote_sohieu),
            "header_sohieu": sorted(header_sohieu)}


def _classify_ref(ref: dict, entries: list, base_goc_keys: set | None = None) -> dict:
    """Gắn cờ 1 dẫn chiếu: OK | MISSING | SOHIEU_MISMATCH | OUTDATED (report-only).
    B1: KHÔNG gắn OUTDATED nếu canonical còn hiệu lực hoặc nằm trong chuỗi hợp nhất của VBHN đang xét."""
    cited = ref["sohieu"]
    # 1) khớp theo số hiệu trước — v1.33.47: +bare-VBHN 1 chiều (văn bản dẫn '88/VBHN-VPQH' không năm ↔ entry
    # year-qualified; trước đây miss → frontier/refs-audit gắn MISSING giả cho VBHN đã có).
    by_sohieu = [e for e in entries if _sohieu_query_hits_entry(cited, norm_sohieu(_entry_sohieu(e)))
                 or _sohieu_query_hits_entry(cited, _sohieu_key_entry(e))]
    # 2) khớp theo TÊN (alias) — để bắt SOHIEU_MISMATCH khi số hiệu sai
    by_name = resolve_identity(ref["name_phrase"], entries, max_hits=3) if ref["name_phrase"] else []
    flag, canonical, conf, note = "OK", None, "", ""
    if by_sohieu:
        canonical = by_sohieu[0]
        # số hiệu khớp; kiểm OUTDATED nếu có VBHN hợp nhất số này — TRỪ các ca B1:
        hl = _strip_accents(str(canonical.get("hieuluc") or canonical.get("hieu_luc") or "")).lower()
        in_base_chain = bool(base_goc_keys and cited.replace("/", "-") in base_goc_keys)
        _vbhn_hits = _vbhn_for_goc(cited, entries)
        if (_vbhn_hits and not _is_vbhn_entry(canonical)
                and "con" not in hl                 # B1: bản CÒN hiệu lực → không OUTDATED
                and not in_base_chain):             # B1: nằm trong chuỗi hợp nhất của chính VBHN đang xét → không OUTDATED
            # B5: NÊU RÕ số hiệu VBHN thay thế (đừng lặp lại số gốc → tránh đọc nhầm "VBHN cùng số").
            _vbhn_sh = _entry_sohieu(_vbhn_hits[0]) or ""
            flag, conf = "OUTDATED", "medium"
            note = (f"đã có VBHN hợp nhất '{_vbhn_sh}' chứa số hiệu gốc {cited} → nên rà trên VBHN '{_vbhn_sh}'"
                    if _vbhn_sh else "có VBHN hợp nhất số hiệu này trong corpus (cân nhắc dùng VBHN)")
    else:
        # số hiệu dẫn KHÔNG khớp exact. (HỢP NHẤT Codex) VBHN-COVERAGE TRƯỚC TYPO/MISSING: nếu số hiệu gốc đã được
        # 1 VBHN trong corpus bao phủ (goc-chain) → OUTDATED (rà trên VBHN), KHÔNG vội gắn TYPO/MISSING (giảm dương
        # tính giả P0-2/P2-8). Chỉ khi KHÔNG có VBHN-coverage mới bắt TYPO (near-match) rồi resolve theo tên.
        _covered_by_vbhn = _vbhn_for_goc(cited, entries)
        _typo = None if _covered_by_vbhn else _sohieu_typo_near(cited, entries, ((ref.get("loai") or "") + " " + (ref.get("name_phrase") or "")).strip())
        if _covered_by_vbhn:
            canonical = _covered_by_vbhn[0]
            flag, conf = "OUTDATED", "medium"
            note = (f"số hiệu gốc '{cited}' không là canonical trực tiếp nhưng đã được VBHN "
                    f"'{_entry_sohieu(canonical)}' bao phủ trong corpus → rà trên VBHN trước khi kết luận MISSING/TYPO")
        elif _typo:
            canonical = _typo[0]
            flag, conf = "DOC_TEXT_SOHIEU_TYPO", "high"
            note = (f"số hiệu dẫn '{cited}' KHÔNG có trong corpus; gần khớp '{_typo[1]}' "
                    f"(cùng số/năm, sai mã cơ quan/số thứ tự) → nhiều khả năng GÕ SAI, nên dùng '{_typo[1]}'")
        elif by_name:
            cano = by_name[0][0]
            cano_sh = norm_sohieu(_entry_sohieu(cano))
            if cano_sh and cano_sh != cited:
                flag, canonical, conf = "SOHIEU_MISMATCH", cano, "high"
                # B5: phân biệt "trỏ sang VBHN mới" (HÀNH VI ĐÚNG) với "dẫn sai số hiệu" (lỗi) — đừng để cờ gây hiểu nhầm.
                if _is_vbhn_entry(cano):
                    note = (f"dẫn '{cited}' → canonical là VBHN hợp nhất '{_entry_sohieu(cano)}' "
                            "(ĐÚNG: trỏ sang bản hợp nhất mới, KHÔNG phải lỗi dẫn sai)")
                else:
                    note = f"văn bản dẫn '{cited}' nhưng canonical là '{_entry_sohieu(cano)}' — kiểm lại số hiệu"
            elif cano_sh:
                canonical = cano; flag = "OK"
            else:
                # khớp tên nhưng entry THIẾU số hiệu → KHÔNG xác nhận OK (vá lỗi false-OK).
                flag, conf = "MISSING", "medium"
                note = "khớp theo tên nhưng entry THIẾU số hiệu — không xác nhận được; kiểm QT-5/web"
        else:
            flag, conf = "MISSING", "medium"
            note = "không thấy canonical theo số hiệu lẫn tên (alias) — kiểm QT-5/web"
    res = {**ref, "flag": flag, "confidence": conf, "note": note}
    if canonical is not None:
        res["canonical"] = {"sohieu": _entry_sohieu(canonical), "name": _entry_name(canonical)[:70],
                            "cat": _entry_cat(canonical), "nlm": bool(_entry_nlm(canonical))}
    return res


_RAW_EXT_RE = re.compile(r"\.(docx?|pdf|html?|rtf|txt|odt)$", re.I)


def _raw_no_gdoc(name: str = "", api_resp=None) -> bool:
    """P1: nhận diện 'entry THÔ chưa có bản GDoc' — theo đuôi tên HOẶC lỗi API 'Export only supports Docs Editors files'."""
    if _is_raw_no_gdoc_name(name):
        return True
    s = (json.dumps(api_resp, ensure_ascii=False).lower() if api_resp is not None else "")
    return "export only" in s or "docs editors" in s


def _emit_raw_no_gdoc(name: str, as_json: bool) -> int:
    """ENTRY_RAW_NO_GDOC → rc=2 (TIỀN ĐIỀU KIỆN đọc sâu CHƯA ĐẠT: entry thô, không export GDoc được) + STDOUT rõ.
    HỢP NHẤT P0-1: trước (bản Claude) rc=0 → caller agentic hiểu nhầm 'thành công, 0 dẫn chiếu' → bỏ sót luật;
    nay rc=2 + ok:false (đúng yêu cầu báo cáo 'chỉ-raw → rc≠0 + thông điệp stdout'). Resolver đã ưu tiên GDoc trước
    nên path này CHỈ chạy khi GENUINE raw-only (không có bản GDoc) → rc≠0 hợp lý, KHÔNG phá batch sai."""
    note = (f"ENTRY_RAW_NO_GDOC: '{(name or '?')[:60]}' là file THÔ (chưa có bản GDoc Google-native) → "
            f"`tl ingest-local`/convert sang GDoc trước khi rà sâu (xref/footnote-map/extract).")
    if as_json:
        print(json.dumps({"ok": False, "error": "ENTRY_RAW_NO_GDOC", "note": note}, ensure_ascii=False))
    else:
        print(f"[tl] {note}")
    return 2


def _sanitize_export_text(s: str) -> str:
    """U1 (v1.31.2 — log LIVE: driver bash vỡ capture vì 'byte không hợp UTF-8' trong output extract): làm sạch
    text export TRƯỚC khi ghi đĩa/in — (a) diệt lone-surrogate (rò từ decode errors=surrogateescape của các đường
    export/gws) bằng round-trip encode-replace; (b) bỏ control-char (giữ \\n \\t). stdout đã reconfigure
    errors='replace' từ lâu nhưng KHÔNG cứu được file --out + text chui vào JSON của driver."""
    s = str(s or "")
    try:
        s = s.encode("utf-8", errors="replace").decode("utf-8")
    except Exception:
        s = s.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", s)


def _read_doc_text(gdoc_id: str, config=None):
    """Đọc nguyên văn GDoc → text. THỨ TỰ: (B1) direct-media EXPORT text/plain bằng gws CRED (KHÔNG cần binary gws —
    chỉ cần ~/.config/gws/credentials.json → né GAS, hết spam FALLBACK) → transport→gws (binary) → webapp exporttext.
    Trả str (rỗng nếu lỗi mọi đường). v1.31.2: mọi nhánh qua _sanitize_export_text (U1)."""
    # (D — log rà: timeout văn bản lớn) TÁI DÙNG cache text mà cmd_extract/cmd_cache_build đã ghi ra đĩa
    # (extract_<gdoc>.txt) TRƯỚC khi export lại → xref/footnote-map trên cùng văn bản (vd Bộ luật Dân sự)
    # không phải export lần 2 (hết timeout > 20s). Chỉ dùng khi cache CÓ + đọc được.
    try:
        _cf = _cache_file(f"extract_{gdoc_id}.txt")
        if _cf.exists():
            _ct = _cf.read_text(encoding="utf-8", errors="replace")
            if _ct.strip():
                return _sanitize_export_text(_strip_font_runs(_ct))
    except Exception:
        pass
    # (1) direct-media export bằng cred — cred-only đủ, không cần `gws-bootstrap-cowork`/binary.
    # v1.33.0 (log rà 69 A3): cred đã chết auth (invalid_grant) 1 lần trong phiên → SKIP thẳng (circuit-breaker),
    # không retry-fail per-doc (~2-20s/doc × 69 làm batch vượt timeout shell).
    try:
        _tlg = _imp("tl_gws")
        _cred = _tlg._read_gws_cred()
        if _cred and not getattr(_tlg, "_CRED_AUTH_DEAD", False):
            with tempfile.TemporaryDirectory() as _d:
                _dst = os.path.join(_d, "doc.txt")
                _tlg._drive_media_download(gdoc_id, _dst, _cred, export_mime="text/plain")
                _txt = open(_dst, encoding="utf-8", errors="replace").read()
                if _txt.strip():
                    return _sanitize_export_text(_strip_font_runs(_txt))
    except Exception:
        pass
    # (2) transport→gws binary; (3) webapp exporttext (GAS).
    try:
        rr = _imp("transport").drive_op("read", file_id=gdoc_id, limit=2_000_000)
        if isinstance(rr, dict) and rr.get("ok") and rr.get("text") is not None:
            return _sanitize_export_text(_strip_font_runs(rr.get("text", "")))
    except Exception:
        pass
    r = _gas().get("exporttext", fileId=gdoc_id)
    return _sanitize_export_text(_strip_font_runs(r.get("text", ""))) if r.get("ok") is not False else ""


def _read_doc_text_via_nlm(entry: dict) -> str:
    """P1 (v1.32.1 — log rà 119: gws cred revoke + webapp exporttext thiếu scope script.external_request →
    KHÔNG còn đường đọc Drive nào sống, corpus-audit 6/6 'header rỗng'): đường đọc DỰ PHÒNG qua NLM CLI
    (nlm-content vẫn CHẠY — 295 nguồn live). Text = bản đã nạp NLM (vẫn verbatim nguồn) — đủ cho header/audit;
    KHÔNG thay thế extract chính-văn khi cần byte-exact. Entry cần nlm_source_id live."""
    sid = str(entry.get("nlm_source_id") or "").strip()
    if not sid or not _entry_on_nlm_live(entry):
        return ""
    try:
        nc = _imp("nlm_cli")
        r = nc.source_content(sid)
        txt = str(r.get("text") or ((r.get("data") or {}) if isinstance(r.get("data"), dict) else {}).get("content") or "")
        return _sanitize_export_text(_strip_font_runs(txt))
    except Exception:
        return ""


NLM_SLOT_CAP = 300   # cap nguồn/notebook NLM (khớp slots.cap webapp). Dùng cho ingest-missing/slot guard.


def _slice_dieu(text: str, dieu: str) -> str:
    import re as _re
    m = _re.search(rf"(?mi)^\s*Điều\s+{_re.escape(str(dieu))}\b.*?(?=^\s*Điều\s+\d+\b|\Z)", text or "", _re.S)
    return m.group(0).strip() if m else f"[không thấy Điều {dieu}]"


# ═══════════ Official-first polite fetcher: ưu tiên FORMAT docx>doc>pdf ═══════════
# Trục TẢI FILE đi theo ĐỊNH DẠNG (docx tốt nhất cho ingest GDoc verbatim) → TVPL/LuatVietnam trước.
# Trục CANONICAL/HIỆU-LỰC vẫn dùng official (vbpl/Công báo) để xác minh bản đúng.
_FMT_RANK = {"docx": 1, "doc": 2, "pdf": 3, "html": 4}
_FETCH_SOURCES = [
    {"source": "thuvienphapluat.vn", "fmt": "docx", "login": True, "quota": True,
     "search": "https://thuvienphapluat.vn/page/tim-van-ban.aspx?keyword={q}",
     "recipe": "Chrome (login VIP): mở /van-ban/ → CLICK TAB 'Tải về' TRƯỚC (link docx mới đổi từ javascript:postback → URL /documents/d... thật) → rồi click link '(docx)'. "
               "Trang lớn → `find` tràn token: dùng JS lấy tọa độ theo TỈ LỆ viewport (sx=center/innerWidth*1568, sy=.../innerHeight*737) rồi click thật. "
               "QUOTA ~1 docx/ngày/tài khoản: nếu lần 2 'bật về home'/không ra file ⇒ HẾT QUOTA → chuyển luatvietnam."},
    {"source": "luatvietnam.vn", "fmt": "docx", "login": True, "quota": True,
     "search": "https://luatvietnam.vn/tim-van-ban.html?keywords={q}",
     "recipe": "Chrome (login): mở văn bản → tab 'Tải về' → mục 'VĂN BẢN TIẾNG VIỆT' → '... DOC (Bản Word)'. "
               "Nút tải là thẻ <a> ICON (không phải DIV chữ): JS click <a> (`el.closest row → querySelector('a[href],[onclick]').click()`) là tải được. KHÔNG vướng quota TVPL."},
    {"source": "vbpl.vn", "fmt": "doc", "login": False, "quota": False,
     "search": "https://vbpl.vn/van-ban/trung-uong  [radio Số hiệu = {q}]",
     "recipe": "Chrome (FREE): radio 'Số hiệu' → gõ số → 'Tìm kiếm' → kết quả 'Tải về' → dialog 'File đính kèm' → 'Tải xuống' .doc. "
               "LƯU Ý: vbpl KHÔNG index VBHN (tìm '17/VBHN-VPQH' → 0 kết quả) — chỉ có BẢN GỐC theo số (có thể 'hết hiệu lực một phần'). Muốn VBHN docx → TVPL/LVN."},
    {"source": "congbao.chinhphu.vn", "fmt": "pdf", "login": False, "quota": False,
     "search": "https://congbao.chinhphu.vn  (tìm số hiệu {q})",
     "recipe": "web_fetch trang công báo → TRÍCH link g7.cdnchinhphu.vn (đừng đoán path) → tải PDF official"},
]


def _query_variants(q: str) -> list:
    """VBHN-FIRST: với truy vấn theo TÊN luật → thử '<tên> hợp nhất' TRƯỚC, rồi '<tên> mới nhất', rồi tên gốc.
    Truy vấn theo SỐ HIỆU → tìm thẳng số (không thêm keyword)."""
    if _looks_like_sohieu_query(q):
        return [q]
    ql = _strip_accents(q).lower()
    if "hop nhat" in ql or "moi nhat" in ql:
        return [q]                     # người dùng đã nêu rõ → tôn trọng nguyên trạng
    return [f"{q} hợp nhất", f"{q} mới nhất", q]   # VBHN-first


def _google_site_url(query: str, site: str | None = None) -> str:
    """Google search URL (ưu tiên dùng Google vì search nội bộ TVPL/LVN kém). site=None → Google toàn cục."""
    import urllib.parse as _up
    q = f"site:{site} {query}" if site else query
    return "https://www.google.com/search?q=" + _up.quote(q)


# Discovery DÙNG CHUNG: tìm văn bản trên web = Google `site:` + VBHN-first.
# Áp cho MỌI tính năng tìm-văn-bản-web: fetch-route/links + QT-5 (vbhn-check/status/relation-check).
# G1 [FIX]: OFFICIAL-FIRST — vbpl.vn (CSDL quốc gia) > congbao.chinhphu.vn (Công báo) > luatvietnam > thuvienphapluat.
_DISCOVERY_SITES = ("vbpl.vn", "congbao.chinhphu.vn", "luatvietnam.vn", "thuvienphapluat.vn")


def _official_rank(url: str) -> int:
    """G1: hạng UY TÍN nguồn (NHỎ = chính thống hơn). 1=vbpl/congbao, 2=.gov.vn/.chinhphu.vn, 3=luatvietnam,
    4=thuvienphapluat, 5=khác. Dùng xếp nguồn đối chiếu official-first + gate G1."""
    u = (url or "").lower()
    if "vbpl.vn" in u or "congbao.chinhphu.vn" in u:
        return 1
    if ".gov.vn" in u or "chinhphu.vn" in u:
        return 2
    if "luatvietnam.vn" in u:
        return 3
    if "thuvienphapluat.vn" in u:
        return 4
    return 5


def _discovery_links(q: str, sites=_DISCOVERY_SITES) -> dict:
    """Trả link Google `site:` (VBHN-first: '<q> hợp nhất' → 'mới nhất' → gốc) cho 'tìm văn bản' — markdown bấm-được."""
    q = (q or "").strip()
    if not q:
        return {"query_variants": [], "links_markdown": [], "google": {}}
    variants = _query_variants(q)
    md = []
    for site in sites:
        md.append(f"- [Google site:{site} — “{variants[0]}”]({_google_site_url(variants[0], site)})")
    md.append(f"- [Google (toàn cục) — “{variants[0]}”]({_google_site_url(variants[0])})")
    return {"query_variants": variants, "links_markdown": md,
            "note": "Tìm văn bản web = Google site: (tốt hơn search nội bộ) + VBHN-first ('hợp nhất' trước).",
            "google": {site: [_google_site_url(v, site) for v in variants] for site in sites}}


def _dedup_status(q: str):
    try:
        entries = _manifest_entries()
    except Exception:
        return {"checked": False, "hits": []}, []
    hits = resolve_identity(q, entries, max_hits=6)
    rows = []
    by_sohieu = False   # khớp SỐ HIỆU + đang active ⇒ chắc chắn đã có
    by_name = False     # chỉ khớp tên/alias + active ⇒ KHẢ NĂNG đã có (cần review)
    for e, score, reasons in hits[:6]:
        st = str(e.get("nlm_status") or "").strip().lower()
        is_active = st in ("pushed", "synced", "added", "live")
        if is_active and "sohieu" in reasons:
            by_sohieu = True
        elif is_active and any(r in reasons for r in ("name_key", "name_substr", "alias")):
            by_name = True
        rows.append({"name": _entry_name(e), "so_hieu": _entry_sohieu(e), "status": st or "(rỗng)",
                     "active": is_active, "score": score, "match": reasons})
    # Dò TÊN bằng token-overlap (bù chỗ resolve_identity hụt khi số hiệu chèn giữa tên chuẩn hóa)
    _STOP = {"luat", "bo", "nghi", "dinh", "thong", "tu", "quyet", "so", "ve", "cua", "va", "cac", "mot", "dieu"}
    qtok = {t for t in re.findall(r"[a-z0-9]+", _strip_accents(q).lower()) if len(t) >= 3 and t not in _STOP}
    if qtok and not by_sohieu:
        for e in entries:
            st = str(e.get("nlm_status") or "").strip().lower()
            if st not in ("pushed", "synced", "added", "live"):
                continue
            subj = set(re.findall(r"[a-z0-9]+", _strip_accents(_entry_subject_text(e)).lower()))
            if len(qtok & subj) / len(qtok) >= 0.8:
                by_name = True
                if not any(r["name"] == _entry_name(e) for r in rows):
                    rows.insert(0, {"name": _entry_name(e), "so_hieu": _entry_sohieu(e), "status": st,
                                    "active": True, "score": "tok", "match": ["name_tokens"]})
                break
    return {"checked": True, "in_corpus_active": by_sohieu, "likely_in_corpus": by_name,
            "hits": rows}, hits


# C2(b)/C4 (đặc tả 26/6): thư mục _HOP_NAP trên Drive để người dùng thả file (link bấm-được, KHÔNG URL trần).
HOPNAP_FOLDER_ID = "1bNSAKGACtk0x0cqX5QRVEGT12udi2g67"


def _runtime_env(override: str | None = None) -> str:
    """C3: RUNTIME_ENV ∈ {code, cowork, chat}. Heuristic env-var; KHÔNG chắc → 'chat' (an toàn = đưa link, không tự tải)."""
    v = (override or "").strip().lower()
    if v in ("code", "cowork", "chat"):
        return v
    import os
    ev = (os.environ.get("TL_RUNTIME_ENV") or "").strip().lower()
    if ev in ("code", "cowork", "chat"):
        return ev
    if os.environ.get("CLAUDE_COWORK") or os.environ.get("COWORK"):
        return "cowork"
    if os.environ.get("CLAUDECODE") or os.environ.get("CLAUDE_CODE_ENTRYPOINT") or os.environ.get("CLAUDE_CODE"):
        return "code"
    return "chat"   # mặc định an toàn (C3)


# ═════════════════ E2: subject-cluster map ('pháp luật về X' → số hiệu canonical) ═════════════════
_SUBJECT_CLUSTERS_CACHE = None


def _cluster_lookup(q: str) -> dict:
    """E2: 'pháp luật về X' / tên lĩnh vực → {sohieu canonical, cluster, base}. Khớp token chứa nhau."""
    qn = _strip_accents(q or "").lower()
    qn = re.sub(r"\b(phap luat ve|phap luat|bo luat|luat)\b", " ", qn)
    qn = re.sub(r"\s+", " ", qn).strip()
    hits, seen = [], set()
    def _add(subject, sh, c, cname):
        key = (cname, sh)
        if sh and key not in seen:
            seen.add(key)
            hits.append({"subject": subject, "sohieu": sh, "cluster": cname,
                         "base": c.get("base"), "base_name": c.get("base_name")})
    for cname, c in (_load_subject_clusters().get("clusters") or {}).items():
        # B7: khớp TÊN CỤM / base_name → trả BASE (canonical VBHN). Vd "lao động" → lao_dong_xa_hoi → 18/VBHN-VPQH.
        cn = _strip_accents(cname.replace("_", " ")).lower()
        bn = _strip_accents(c.get("base_name") or "").lower()
        if qn and (qn in cn or cn in qn or (bn and (qn in bn or bn in qn))):
            _add(c.get("base_name") or cname, c.get("base"), c, cname)
        for subj, sh in (c.get("members") or {}).items():
            sjn = _strip_accents(subj).lower()
            if sjn and qn and (sjn in qn or qn in sjn):
                _add(subj, sh, c, cname)
    return {"query": q, "matches": hits}


def _cluster_for_base(base_sh: str):
    bn = norm_sohieu(base_sh or "").replace("/", "-")
    if not bn:
        return None, None
    clusters = (_load_subject_clusters().get("clusters") or {})
    for cname, c in clusters.items():
        keys = [c.get("base", "")] + list(c.get("base_aliases") or [])   # khớp cả Luật GỐC (vd 45/2019→cụm BLLĐ)
        if any(x and norm_sohieu(x).replace("/", "-") == bn for x in keys):
            return cname, c
    # A4: reverse-map qua THÀNH VIÊN cụm — input là số hiệu VBHN/thành viên (vd 19/VBHN-VPQH) cũng tìm ra cụm
    # (trước đây chỉ khớp base=Luật gốc → truyền số hiệu VBHN vào rasoat-chongcheo trả cụm=∅ dù cluster-theo-tên đúng).
    for cname, c in clusters.items():
        for sh in (c.get("members") or {}).values():
            if sh and norm_sohieu(sh).replace("/", "-") == bn:
                return cname, c
    return None, None


def _resolve_cluster_member(sh: str, subj: str, entries: list[dict]) -> dict:
    """Resolve số hiệu thành viên cụm → entry CỤ THỂ. Khi số hiệu TRÙNG (vd 14/VBHN-VPQH dùng cho CẢ ATVSLĐ
    lẫn NLĐ-đi-nước-ngoài): ưu tiên TÊN khớp chủ đề (subj) > còn-hiệu-lực > là VBHN > năm mới. GIỮ VBHN-first
    (chọn ĐÚNG bản hợp nhất của chủ đề, không tụt về Luật gốc)."""
    k = norm_sohieu(sh)
    cands = [e for e in entries if norm_sohieu(_entry_sohieu(e)) == k]
    if not cands:
        return {"in_corpus": False, "ambiguous": False}

    def _alive(e) -> int:
        hl = _strip_accents(str(e.get("hieuluc") or e.get("hieu_luc") or "")).lower()
        return 1 if ("hieu luc" in hl and "het" not in hl and "khong" not in hl) else 0

    def _yr(e) -> int:
        ys = [int(y) for y in _entry_years(e) if str(y).isdigit()]
        return max(ys) if ys else (_sohieu_year(_entry_sohieu(e)) or 0)

    subj_toks = _token_set(_strip_accents(subj or "").lower())
    best = max(cands, key=lambda e: (len(subj_toks & _token_set(_strip_accents(_entry_name(e)).lower())),
                                     _alive(e), 1 if _is_vbhn_entry(e) else 0, _yr(e)))
    # ambiguous CHỈ khi số hiệu trỏ ≥2 VĂN BẢN KHÁC NHAU thật (name-key khác nhau) — KHÔNG tính bản quarantine
    # hay bản trùng-lặp cùng tên (vd canonical + bản NLM/Drive cùng văn bản). Tránh nhãn nhiễu cho mọi thành viên.
    live = [e for e in cands if not _is_quarantine_cat(_entry_cat(e))] or cands
    distinct = {_name_key(_entry_name(e)) for e in live}
    return {"in_corpus": True, "name": _entry_name(best), "drive_id": _entry_drive_id(best),
            "hieuluc": best.get("hieuluc") or best.get("hieu_luc") or "",
            "ambiguous": len(distinct) > 1, "n_candidates": len(cands)}


def _omnibus_cross_domain_note(amending_sh: str, base_subject: str, entries: list[dict]) -> str | None:
    """#11: luật SỬA (amending_sh) có trong corpus nhưng TÊN/chủ đề khác hẳn base → nhiều khả năng là LUẬT SỬA-NHIỀU-LUẬT
    (omnibus, vd 84/2025 Luật Thanh tra sửa cả Luật BHXH). Trả note cảnh báo để KHÔNG hiểu nhầm là lỗi tên/đối chiếu;
    PHẢI đọc nguyên văn điều khoản sửa. None nếu cùng chủ đề (sửa-trong-lĩnh-vực bình thường) hoặc không có trong corpus."""
    if not amending_sh or not base_subject:
        return None
    k = norm_sohieu(amending_sh).replace("/", "-")
    hits = [e for e in entries if _sohieu_key_entry(e) == k]
    if not hits:
        return None                       # chưa có trong corpus → đã có cảnh báo khác (missing/QT-5)
    e = hits[0]
    # B3 (false-positive): CHỈ kết luận omnibus khi luật sửa CÓ chủ đề RÕ và KHÁC base. Tên số TRƠ
    # ("51_2024_QH15_505750", "46_2014_QH13_238506") → _subject_tokens RỖNG → sscore 0 KHÔNG phải vì khác lĩnh vực
    # mà vì THIẾU metadata → ĐỪNG gắn omnibus (51/2024, 46/2014 thực ra là luật sửa BHYT chuyên đề).
    e_subj_tokens = _subject_tokens(_entry_subject_text(e))
    if len(e_subj_tokens) < 2:
        return None                            # chủ đề luật sửa KHÔNG RÕ → không kết luận cross-domain
    if _subject_score(e, base_subject) < 30:   # CÓ chủ đề rõ NHƯNG khác lĩnh vực base → omnibus thật
        return (f"OMNIBUS_CROSS_DOMAIN: luật sửa {amending_sh} trong corpus = '{_entry_name(e)[:48]}' — TÊN CHÍNH khác "
                f"lĩnh vực base; nhiều khả năng là LUẬT SỬA-NHIỀU-LUẬT (sửa base trong số nhiều luật). ĐỪNG coi là lỗi "
                f"tên/đối chiếu; ĐỌC NGUYÊN VĂN điều khoản sửa để xác nhận quan hệ.")
    return None


def _resolve_base_gdoc(base: str, entries: list[dict]):
    """Resolve `base` (số hiệu|tên) → (entry canonical VBHN-first, gdoc_id, subject_text). Cho auto-footnote: đọc
    nguyên văn VBHN base để chạy footnote-map mà KHÔNG cần truyền --target tay. (entry, gid, subject) hoặc (None,'','')."""
    if not base:
        return None, "", ""
    item = _source_map_one(base, entries)
    can = None
    pool_ids = [c.get("drive_id") for c in [item.get("canonical")] if c]
    if pool_ids and pool_ids[0]:
        can = next((e for e in entries if _entry_drive_id(e) == pool_ids[0]), None)
    if can is None:                       # fallback: khớp số hiệu trực tiếp, ưu tiên VBHN
        k = norm_sohieu(base).replace("/", "-")
        cands = [e for e in entries if _sohieu_key_entry(e) == k]
        cands.sort(key=_entry_score, reverse=True)
        can = cands[0] if cands else None
    # C (log rà #70): entry có sohieu RỖNG nhưng corpus=true + có drive_id → fallback khớp trực tiếp theo
    # tên/drive_id (thay vì 404/File-not-found). Đọc sâu vẫn chạy được dù registry chưa backfill số hiệu.
    if can is None:
        for e in entries:
            if _entry_corpus_true(e) and _entry_drive_id(e) and base in (_entry_name(e), _entry_sohieu(e), _entry_drive_id(e)):
                can = e
                break
    if can is None:
        return None, "", ""
    return can, (_entry_drive_id(can) or ""), _entry_name(can)


_DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
_XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
_MIME_BY_EXT = {
    ".docx": _DOCX_MIME, ".doc": "application/msword", ".pdf": "application/pdf",
    ".rtf": "application/rtf", ".odt": "application/vnd.oasis.opendocument.text", ".txt": "text/plain",
    # v1.34.6 #2 (log phiên 2026-07-09): thiếu bảng tính → .xlsx rơi về DOCX_MIME → convert GDoc fail
    # 'Conversion of the uploaded content to the requested output type is not supported'.
    ".xlsx": _XLSX_MIME, ".xls": "application/vnd.ms-excel",
}
_SPREADSHEET_EXTS = (".xlsx", ".xls")


def _valid_cats(config_path=None, profile=None) -> set:
    """(4) Tập mã cat có FOLDER THỰC của profile, đọc từ config.profiles.<p>.categories."""
    for p in _config_candidates(config_path):
        if p and Path(p).exists():
            cfg = _read_json_file(p)
            if cfg:
                prof = _profiles_from_config(cfg).get(_selected_profile_name(profile, cfg)) or {}
                cats = prof.get("categories")
                # MERGE nhánh-3 v1.33.14: profile categories='inherit' (doctrine §12) → tra cây của profile mặc định.
                if isinstance(cats, str) and cats == "inherit":
                    prof = _profiles_from_config(cfg).get(cfg.get("defaultProfile", DEFAULT_PROFILE)) or {}
                    cats = prof.get("categories")
                if isinstance(cats, dict):
                    return set(cats.keys()) | {"QUARANTINE"}
    return set()


def _load_phapdien() -> dict:
    """(4) Bảng 45 chủ đề pháp điển chính thức (references/phap_dien_45.json): {code: {ten, folder, exists}}.
    Gộp custom 00/46. Trả {} nếu thiếu file."""
    for cand in (Path(__file__).resolve().parent.parent / "references" / "phap_dien_45.json",
                 Path.cwd() / "references" / "phap_dien_45.json"):
        try:
            if cand.exists():
                d = json.loads(cand.read_text(encoding="utf-8"))
                m = dict(d.get("chu_de") or {})
                m.update(d.get("custom_non_phapdien") or {})
                return m
        except Exception:
            pass
    return {}


# (4) Gợi ý CHỦ ĐỀ ĐÚNG theo Bộ pháp điển (Quyết định 843/QĐ-TTg) cho lĩnh vực dễ gán nhầm.


# Từ khóa MẠNH → mã chủ đề pháp điển (ASCII, theo phap_dien_45.json). Chỉ tín hiệu rõ để cat-audit ít nhiễu.
_CAT_KEYWORDS = {
    "01": ["an_ninh_quoc_gia", "xuat_canh", "nhap_canh", "qua_canh", "bi_mat_nha_nuoc", "an_ninh_mang", "co_yeu"],
    "02": ["bao_hiem_xa_hoi", "bhxh", "bao_hiem_y_te", "bhyt", "kinh_doanh_bao_hiem", "bao_hiem_that_nghiep", "bao_hiem_tien_gui"],
    "03": ["buu_chinh", "vien_thong", "cong_nghe_thong_tin", "cntt", "giao_dich_dien_tu", "du_lieu", "an_toan_thong_tin", "tan_so", "bao_ve_du_lieu_ca_nhan", "csdl"],
    "05": ["can_bo", "cong_chuc", "vien_chuc", "cong_vu"],
    "06": ["nguoi_cao_tuoi", "nguoi_khuyet_tat", "bao_tro_xa_hoi", "giam_ngheo", "nguoi_co_cong"],
    "08": ["dan_so", "binh_dang_gioi", "bao_luc_gia_dinh", "tre_em", "nuoi_con_nuoi", "hon_nhan"],
    "09": ["dan_su", "bo_luat_dan_su"],
    "10": ["dan_toc"],
    "11": ["dat_dai", "dia_chinh"],
    "12": ["doanh_nghiep", "hop_tac_xa", "ho_kinh_doanh"],
    "13": ["giao_duc", "dao_tao", "nha_giao", "giao_vien", "day_nghe", "nghe_nghiep", "dai_hoc"],
    "14": ["giao_thong", "van_tai", "duong_bo", "duong_sat", "hang_khong", "hang_hai", "duong_thuy"],
    "15": ["ho_tich", "quoc_tich", "ly_lich_tu_phap", "boi_thuong_nha_nuoc"],
    "16": ["hinh_su", "thi_hanh_an_hinh_su", "dac_xa"],
    "17": ["ke_toan", "kiem_toan"],
    "18": ["khieu_nai", "to_cao", "tiep_cong_dan", "phong_chong_tham_nhung", "thanh_tra"],
    "19": ["khoa_hoc", "so_huu_tri_tue", "tieu_chuan", "do_luong", "chat_luong_san_pham", "nang_luong_nguyen_tu", "chuyen_giao_cong_nghe"],
    "20": ["lao_dong", "viec_lam", "an_toan_ve_sinh_lao_dong", "tien_luong"],
    "21": ["moi_truong", "da_dang_sinh_hoc"],
    "22": ["ngan_hang", "tien_te", "cac_tctd", "tin_dung", "ngoai_hoi"],
    "23": ["ngoai_giao", "dieu_uoc_quoc_te", "lanh_su"],
    "24": ["nong_nghiep", "nong_thon", "thuy_san", "lam_nghiep", "chan_nuoi", "thu_y", "bao_ve_thuc_vat", "thuy_loi", "de_dieu"],
    "25": ["quoc_phong", "bien_phong", "dan_quan", "nghia_vu_quan_su", "sy_quan"],
    "26": ["ngan_sach", "dau_tu_cong"],
    "27": ["tai_nguyen", "khoang_san", "dia_chat", "bien_va_hai_dao"],
    "28": ["tai_san_cong", "du_tru_nha_nuoc"],
    "29": ["thi_dua", "khen_thuong", "danh_hieu_vinh_du"],
    "30": ["thi_hanh_an_dan_su"],
    "31": ["thong_ke"],
    "32": ["bao_chi", "xuat_ban", "thu_vien"],
    "33": ["thue", "le_phi", "hai_quan", "hoa_don"],
    "34": ["thuong_mai", "chung_khoan", "canh_tranh", "nguoi_tieu_dung", "ppp", "dau_thau"],
    "35": ["to_chuc_chinh_phu", "to_chuc_quoc_hoi", "chinh_quyen_dia_phuong", "to_chuc_toa_an", "to_chuc_vien_kiem_sat"],
    "36": ["mat_tran_to_quoc", "thanh_nien", "cong_doan", "cuu_chien_binh"],
    "37": ["to_tung", "trong_tai_thuong_mai", "hoa_giai"],
    "38": ["ton_giao", "tin_nguong"],
    "39": ["ma_tuy", "mai_dam", "phong_chay", "chua_chay", "vu_khi", "vat_lieu_no", "can_cuoc", "phong_chong_thien_tai"],
    "40": ["tuong_tro_tu_phap"],
    "41": ["van_hoa", "the_thao", "du_lich", "di_san", "dien_anh", "quang_cao", "the_duc"],
    "42": ["van_thu", "luu_tru"],
    "43": ["xay_dung", "nha_o", "do_thi", "quy_hoach", "kien_truc"],
    "44": ["ban_hanh_van_ban", "vbqppl", "thi_hanh_phap_luat", "pho_bien_giao_duc_phap_luat", "phap_dien"],
    "45": ["y_te", "kham_benh", "chua_benh", "an_toan_thuc_pham", "duoc_pham", "phong_chong_benh", "hien_mau", "hien_tang"],
}
# Hint cho ingest (lĩnh vực dễ gán nhầm) — dẫn xuất từ map chính thức ở trên (đã sửa: hình sự=16, DN=12, giao thông=14).
_CAT_REVIEW_HINTS = {"tố tụng": "37", "xuất nhập cảnh": "01", "hình sự": "16", "doanh nghiệp": "12", "giao thông": "14", "kế toán": "17"}


# ───────────────────────── G3: phân loại theo NỘI DUNG + quy tắc ranh giới ─────────────────────────
_LINHVUC_CACHE = None
def _load_linhvuc() -> dict:
    """G3: bảng 45+2 chủ đề + quy_tac_ranh_gioi + alias (references/linhvuc_phapdien.json). {} nếu thiếu/parse lỗi
    (cảnh báo, KHÔNG im lặng). Mirror _load_subject_clusters/_load_phapdien (cache + nhiều ứng viên đường dẫn)."""
    global _LINHVUC_CACHE
    if _LINHVUC_CACHE is None:
        here = Path(__file__).resolve().parent
        for cand in (here.parent / "references" / "linhvuc_phapdien.json", here / "linhvuc_phapdien.json",
                     Path.cwd() / "references" / "linhvuc_phapdien.json"):
            try:
                if cand.exists():
                    _LINHVUC_CACHE = json.loads(cand.read_text(encoding="utf-8")); break
            except Exception as e:  # noqa: BLE001
                sys.stderr.write(f"[tl] ⚠ linhvuc_phapdien.json KHÔNG parse được ({type(e).__name__}: {e}) — quy tắc "
                                 f"ranh giới G3 RỖNG; ĐỪNG kết luận cat. Re-sync references/linhvuc_phapdien.json.\n")
                _LINHVUC_CACHE = {}; break
        if _LINHVUC_CACHE is None:
            _LINHVUC_CACHE = {}
    return _LINHVUC_CACHE


_ALIAS_CAT_PAIRS = None
_ALIAS_TOO_GENERIC = {"giam sat", "quan ly", "to chuc", "hoat dong", "chinh sach",
                      # v1.31.2 (FP thật phiên rà): alias trần 'cong nghe' (chude 19) kéo nhầm Luật CNTT (03 đúng
                      # chuẩn) — quá chung; các alias 19 đặc thù (khoa hoc cong nghe/chuyen giao cong nghe/...) giữ.
                      "cong nghe"}


_TITLE_BLOCK_KIND_RE = re.compile(r"^(BỘ\s*LUẬT|LUẬT|PHÁP\s*LỆNH|NGHỊ\s*QUYẾT|NGHỊ\s*ĐỊNH|THÔNG\s*TƯ)\s*$")
_TITLE_BLOCK_STOP_RE = re.compile(r"^(Căn cứ|CĂN CỨ|CHƯƠNG|Chương|Điều|ĐIỀU|Luật này|Bộ luật này|Nghị định này|_{3,}|-{3,})", re.I)
# v1.33.37 (MERGE bundle-14 — log rà: title_vn ca QD_671-QD-BTTTT ra 'Quyết định ﻿bộ thông tin và' lẫn BOM +
# cụt): BOM/zero-width UTF-8-HỢP-LỆ nên _sanitize_export_text (chỉ diệt control/surrogate) KHÔNG đụng → lọt vào
# bóc trích yếu. Strip Ở ĐƯỜNG ĐẶT TÊN/title_vn (KHÔNG đụng đường export nguyên văn — giữ verbatim). Escape \u
# tường minh thay ký tự vô hình trong source (chính là lỗi đang sửa). Set: BOM · ZWSP..ZWJ · word-joiner · U+FFFE.
_ZERO_WIDTH_RE = re.compile("[﻿​-‍⁠￾]")


_TUKHOA_TITLE_RE = re.compile(r"(Bộ luật|Luật)\s+([A-Za-zÀ-ỹ][A-Za-zÀ-ỹ ,]{2,55})", re.I)
_TUKHOA_TAIL_JUNK = ("này", "số", "trong", "về việc", "và", "các", "của", "có", "liên", "quan", "luật", "một",
                     "số điều", "năm", "quy", "định")
# Cắt heading-mới giữa câu: theo TỪ-KHÓA heading THẬT (tukhoa = chuỗi tiêu đề Điều nối nhau) — review v1.31.1
# CONFIRMED: đoán theo chữ-hoa ([A-ZĐ][a-z…]) cắt trước MỌI từ viết-Hoa → tukhoa Title-Case ('Bảo Hiểm Xã Hội
# Điều 2') cụt còn 'Bảo'; trước đó dải [A-ZÀ-Ỹ] còn tệ hơn ('đ' thường ∈ À-Ỹ cắt giữa 'quy định').
_TUKHOA_HEADING_SPLIT_RE = re.compile(r"\s+(?=(?:Điều|Chương|Mục|Phần|Khoản)\b|(?:Giải thích|Phạm vi|Đối tượng|Hiệu lực)\b)")


def _goc_pollution_groups(entries: list) -> list:
    """PURE (§1.1 log rà 108 lần): VBHN có TÊN mã hoá base (token goc_<X>) NHƯNG registry.goc KHÔNG chứa X = goc NHIỄM.
    Ca thật: VBHN_22 'Bảo vệ sức khỏe nhân dân' tên goc_21-LCT-HDNN8 nhưng registry.goc=113-2025 (Dân số) → source-map
    redirect Dân số SANG VBHN Bảo vệ sức khỏe + webapp vb_status superseded_by sai. Trả [{drive_id,name,sohieu,
    registry_goc, name_goc_base, suggested_goc}] để SỬA registry.goc qua reg_upsert (KHÔNG reg_bulk — goc là quan hệ)."""
    out = []
    for e in entries:
        if not _is_vbhn_entry(e):
            continue
        nb = _name_goc_base_key(_entry_name(e))
        if nb and nb not in _goc_keys(e):
            out.append({"drive_id": _entry_drive_id(e), "name": _entry_name(e)[:60],
                        "sohieu": _entry_sohieu(e) or "", "registry_goc": _entry_goc(e),
                        "name_goc_base": nb, "suggested_goc": nb})
    return out


def _is_infra_entry(e: dict) -> bool:
    """File HẠ TẦNG (KHÔNG phải văn bản) lẫn vào corpus=true = RÁC: .json/.enc + tên nlm_sources/manifest/registry/
    secrets/_delta/reg_query. BẢO VỆ văn bản thật (GDoc/PDF/Word) → KHÔNG false-positive (vd tl_secrets.enc,
    nlm_sources_delta_2026-06-11.json bị đếm corpus)."""
    mime = str(e.get("mimeType") or e.get("mime") or "").lower()
    nm = _strip_accents(str(_entry_name(e) or "")).lower()
    if any(t in mime for t in ("vnd.google-apps.document", "pdf", "wordprocessing", "msword")):
        return False
    if "spreadsheet" in mime or mime.endswith("/json") or nm.endswith(".json") or nm.endswith(".enc"):
        return True
    return any(t in nm for t in ("nlm_sources", "manifest", "registry", "reg_query", "secrets", "_delta"))


def _dedup_lite(e: dict) -> dict:
    return {"drive_id": _entry_drive_id(e), "sohieu": _entry_sohieu(e) or "", "name": _entry_name(e)[:50],
            "corpus": str(e.get("corpus")).lower() == "true", "on_nlm": _entry_on_nlm_live(e),
            "nlm_source_id": _entry_nlm(e) or ""}


def _dedup_plan(entries: list) -> dict:
    """PURE: kế hoạch DEDUP tất định, tái dùng canonical-picker của `_hygiene_groups` (reconcile_clusters dùng
    `_cluster_same_doc` = CÙNG văn bản theo subject-sig, AN TOÀN). Mỗi cụm: GIỮ canonical, quarantine các bản dup.
    BẤT BIẾN AN TOÀN: (1) không quarantine chính canonical; (2) không quarantine drive_id LÀ canonical của cụm khác;
    (3) mỗi drive_id chỉ vào 1 lần. ready=cụm có canonical rõ; review=cụm thiếu canonical (quyết tay)."""
    g = _hygiene_groups(entries)
    canon_ids, seen = set(), set()
    ready, review = [], []
    for c in g["reconcile_clusters"]:
        # gộp quarantine (same-doc dup) + sidecars (.docx/.pdf cạnh GDoc canonical = dup định dạng) — cả 2 đều là bản dư.
        _qd, _q = {}, []
        for e in (c.get("quarantine") or []) + (c.get("sidecars") or []):
            did = _entry_drive_id(e)
            if did and did not in _qd:
                _qd[did] = e; _q.append(e)
        q = _q
        if not q:
            continue
        can = c.get("canonical")
        if not can:
            review.append({"key": c.get("key"), "dups": [_dedup_lite(e) for e in q]})
            continue
        cid = _entry_drive_id(can)
        canon_ids.add(cid)
        dups = [e for e in q if _entry_drive_id(e) != cid and _entry_drive_id(e) not in seen]
        for e in dups:
            seen.add(_entry_drive_id(e))
        if dups:
            ready.append({"key": c.get("key"), "canonical": _dedup_lite(can), "quarantine": [_dedup_lite(e) for e in dups]})
    # BẤT BIẾN (2): loại khỏi quarantine mọi drive_id là canonical của 1 cụm khác
    for it in ready:
        it["quarantine"] = [d for d in it["quarantine"] if d["drive_id"] not in canon_ids]
    ready = [it for it in ready if it["quarantine"]]
    dups_on_nlm = [d for it in ready for d in it["quarantine"] if d["on_nlm"]]
    return {"ready": ready, "review": review,
            "total_quarantine": sum(len(it["quarantine"]) for it in ready),
            "dups_on_nlm": dups_on_nlm}


_RAW_LOOSE_SOHIEU_RE = re.compile(
    r"(?i)(?<![0-9A-Za-zĐđ])(ND|NĐ|TT|QD|QĐ|NQ|PL|CT|TTLT|BLDS|BLHS|L)?[\s_\-\.]*?(\d{1,4})[\s_\-\.]+((?:19|20)\d{2})(?![0-9])")


def _raw_dup_of_standard_rows(entries: list) -> list:
    """PURE (v1.29.3 — AUDIT #5, log LIVE 2.3): bắt 'BẢN TẢI THÔ TRÙNG BẢN CHUẨN' — dòng corpus=true có tên thô KHÔNG
    trích được sohieu chuẩn (vd 'ND274_2025_cham dong-tron dong BH.pdf' — mã loại DÍNH TRƯỚC số nên _RAW_SOHIEU_RE miss)
    nhưng tên chứa <MÃ-LOẠI><số>_<năm> khớp LỎNG với ĐÚNG 1 bản CHUẨN corpus=true trong corpus → đề xuất corpus=false.
    PROPOSE-ONLY (match lỏng KHÔNG đủ tin auto; regex lỏng CHỈ để dedup-match, KHÔNG bao giờ dùng gán sohieu).
    An toàn: chỉ xét raw corpus=true + sohieu-key RỖNG; chỉ đề xuất khi match DUY NHẤT (num+năm[+family]); bản chuẩn
    phải corpus=true (chuẩn đã tắt → raw có thể là bản duy nhất, KHÔNG đề xuất)."""
    _fam_norm = {"NĐ": "ND", "QĐ": "QD"}
    # Họ mã-loại CANONICAL — key trích ra family NGOÀI họ này (vd '274-2025-CHAM' từ tên thô 'ND274_2025_cham dong…',
    # 'CHAM' = từ đầu trích yếu bị nhận nhầm) = trích SAI → vẫn là ứng viên raw (chính là ca 5 dòng LIVE lọt qua S12).
    _canon_fams = {"ND", "TT", "QD", "NQ", "PL", "CT", "TTLT", "QH", "UBTVQH", "VBHN", "L", "LCT", "HDNN", "BTC",
                   "NHNN", "BYT", "BCA", "BQP", "CP", "TW", "KL", "HD", "CD"}   # CD = Công điện (CĐ→CD sau norm)

    def _key_fam(k: str) -> tuple:
        m = re.match(r"^(\d{1,4})-((?:19|20)\d{2})-([A-ZĐ]+)", k or "")
        # num chuẩn hoá str(int(...)) — số ZERO-PADDED ('06-2003-PL-UBTVQH11', đúng ca PL_06 log LIVE) phải khớp
        # lookup lỏng int('06')→'6' phía raw; giữ raw '06' sẽ MISS.
        return (str(int(m.group(1))), m.group(2), _fam_norm.get(m.group(3), m.group(3))) if m else (None, None, None)

    std_by_numyear: dict[tuple, list] = {}
    std_keys = set()
    for e in entries or []:
        if not _entry_corpus_true(e):
            continue
        k = _sohieu_key_entry(e)
        num, yr, fam = _key_fam(k)
        if fam and fam in _canon_fams:
            std_by_numyear.setdefault((num, yr), []).append((fam, e))
            std_keys.add(k)
    rows = []
    for e in entries or []:
        if not _entry_corpus_true(e):
            continue
        _k = _sohieu_key_entry(e)
        if _k:
            _n, _y, _f = _key_fam(_k)
            if (_f and _f in _canon_fams) or _k in std_keys:
                continue                               # key chuẩn thật (hoặc trùng chuẩn → việc của dedup-plan)
        nm = _entry_name(e)
        # Ứng viên PHẢI trông như FILE THÔ: có đuôi file hoặc chứa SPACE — tên chuẩn hoá không bao giờ có cả hai
        # (chống false-positive smoke LIVE: 'CD_32-2026-CD-TTg_…' tên CHUẨN loại hiếm bị ghép nhầm TT_32-2026).
        if not (re.search(r"\.(docx?|pdf|html?)\b", nm or "", re.I) or " " in (nm or "")):
            continue
        lm = _RAW_LOOSE_SOHIEU_RE.search(nm or "")
        if not lm:
            continue
        fam_raw = _fam_norm.get((lm.group(1) or "").upper(), (lm.group(1) or "").upper())
        cands = std_by_numyear.get((str(int(lm.group(2))), lm.group(3))) or []
        if fam_raw:
            cands = [(f, s) for f, s in cands if f.startswith(fam_raw) or fam_raw.startswith(f)]
        if len(cands) != 1:
            continue                                   # 0 hoặc >1 → KHÔNG đủ tin, bỏ
        _f, std = cands[0]
        did = _entry_drive_id(e)
        rows.append({"drive_id": did, "name": nm[:60],
                     "loose_match": f"{fam_raw or '?'}{int(lm.group(2))}-{lm.group(3)}",
                     "standard": {"drive_id": _entry_drive_id(std), "sohieu": _entry_sohieu(std) or _sohieu_key_entry(std),
                                  "name": _entry_name(std)[:60]},
                     "fix_command": f"tl source-update-corpus {did} false --apply"})
    return rows


def _corpus_count_server_rule(entries: list) -> int:
    """v1.30.1 (#7 log — PURE): đếm corpus THEO ĐÚNG LUẬT SERVER GAS (manifestHashObjs_/regIsCorpusCounted_,
    Code.2.21.2i.gs:2173-2183) trên CÙNG snapshot entries: corpus∈{true,vbqppl} HOẶC row_kind=overflow; TRỪ ref;
    TRỪ loai='thuong'. Đây là con số `manifest_export.corpus_count` mà `tl boot` in ra — KHÁC `sweep.corpus`
    (corpus=='true' thuần). In CẢ HAI cạnh nhau ⇒ hết 'chênh 12 dòng' bí ẩn giữa 2 lệnh (527 boot vs 515 sweep:
    khác TIÊU CHÍ + khác snapshot GAS-cache ~600s, không phải mất dữ liệu). Profile có registryDocId riêng: server
    đếm MỌI dòng có drive_id (nhánh _REQ_REGISTRY_ID_) — số này chỉ áp cho scope VBQPPL nền."""
    n = 0
    for e in entries or []:
        rk = str(_entry_row_kind(e) or "own").lower()
        if rk == "ref":
            continue
        c = str(e.get("corpus") or "").lower()
        if not (c in ("true", "vbqppl") or rk == "overflow"):
            continue
        # Review v1.30.1 (CONFIRMED): GAS so `o.loai!=='thuong'` EXACT (không lower/strip — Code.gs:2183) →
        # mirror NGUYÊN XI; 'Thuong' hoa server VẪN đếm. Lower hoá ở đây = tự tạo lệch mới với boot.
        if str(e.get("loai") or "") == "thuong":
            continue
        n += 1
    return n


# ══════════ Corpus cleanup: orchestrator (corpus-fix) + source CRUD (source-rename) + fixer (shared-source-fix) ══════════
# Nguyên tắc: DRY/plan mặc định; ghi Drive/NLM/registry = --apply LIVE (Cowork). THỨ TỰ SỬA cố định (sai thứ tự=hỏng thêm).
# Tầng: safe_auto (reversible: corpus=false) auto khi --apply --tier safe; còn lại in lệnh + người duyệt.

def _corpus_fix_plan(entries: list) -> dict:
    """PURE (test offline): ĐIỀU PHỐI dọn/chỉnh lý corpus — gộp mọi detector (sweep) → kế hoạch THEO THỨ TỰ PHỤ THUỘC +
    phân TẦNG an toàn. Thứ tự CỐ ĐỊNH: shared-link→goc-nhiễm→infra→dedup→year→loai→title/cat→nlm-relabel→ingest→
    consolidation→quarantine. KHÔNG mutate; chỉ trả plan (mỗi step: order,id,tier,problem,count,command,reversible,note)."""
    rep = _sweep_report(entries)
    nb = os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK
    d = rep["duplicates"]
    dr = rep["nlm_drift"]
    _vgoc = set()
    for e in entries:
        if _is_vbhn_entry(e):
            _vgoc |= _goc_keys(e)
    consol = sum(1 for e in entries if _entry_corpus_true(e) and not _is_vbhn_entry(e)
                 and _sohieu_key_entry(e) and _sohieu_key_entry(e) in _vgoc)
    steps = []

    def add(order, sid, tier, problem, count, command, reversible, note, sample=None):
        if count:
            st = {"order": order, "id": sid, "tier": tier, "problem": problem, "count": count,
                  "command": command, "reversible": reversible, "note": note}
            if sample:
                st["sample"] = sample[:5]
            steps.append(st)

    add(1, "shared_source_id", "human_confirm",
        "Link NLM SAI (≥2 drive_id chung 1 source_id) — SỬA TRƯỚC mọi thao tác NLM (xóa 1 nguồn gãy link kia)",
        rep["shared_source_id"], f"tl shared-source-fix {nb}", False,
        "Tách: giữ link ở bản đúng, reg_clear link sai bản kia rồi re-push.", rep.get("shared_source_id_groups"))
    add(2, "goc_pollution", "human_confirm",
        "registry.goc NHIỄM → source-map/status redirect SAI văn bản",
        rep["goc_pollution"], "tl register --drive-id <id> --goc <suggested_goc>", False,
        "Sửa goc về suggested_goc (reg_upsert, KHÔNG reg_bulk). Xem sweep.goc_pollution_rows.", rep.get("goc_pollution_rows"))
    add(3, "infra_in_corpus", "safe_auto",
        "File HẠ TẦNG (.json/.enc/secrets) đánh dấu corpus=true = RÁC",
        rep["infra_in_corpus"], "tl corpus-fix --apply --tier safe", True,
        "REVERSIBLE: chỉ set corpus=false.", rep.get("infra_in_corpus_rows"))
    add(4, "duplicates", "safe_auto",
        "Trùng lặp thật (same-document / md5 / identity)",
        d["same_document"] + d["by_md5"] + d["identity"], "tl dedup-plan --apply (hoặc corpus-fix --apply --tier safe)", True,
        "REVERSIBLE: GIỮ canonical, bản dup → corpus=false.")
    add(5, "vbhn_missing_year", "metadata_deterministic",
        "VBHN sohieu/tên THIẾU năm (số tái dùng theo năm → collision)",
        rep["vbhn_year"]["fixable"], "tl vbhn-year-fix --with-name --apply", False,
        f"{rep['vbhn_year']['needs_year']} cần xác minh năm tay; {rep['vbhn_year']['conflicts']} conflict phân biệt tay.")
    add(6, "loai_noncanonical", "metadata_deterministic",
        "Trường `loai` phi chuẩn", rep["loai_noncanonical"], "tl backfill-loai --normalize --apply", False,
        "Suy loai từ số hiệu/tên; --normalize sửa cả dòng loai SAI enum (map tất định 'Luat'→'Luật').")
    add(7, "title_cat_mismatch", "human_confirm",
        "Tên/cat/trích yếu LỆCH nội dung (cần ĐỌC header — cat-verify suy bừa khi GAS-fallback)",
        rep["title_mismatch"], "tl corpus-audit  → tl source-rename/recat theo header-verify", False,
        "KHÔNG auto: dùng `header-verify` ground-truth rồi sửa tay.")
    # MERGE Codex v1.33.11: bước raw_on_nlm vào orchestrator (detector v1.33.4 đã đếm — plan phải có đường sửa).
    add(8, "raw_on_nlm", "human_confirm",
        "FILE THÔ (.html/.docx/.pdf) đang là nguồn NLM live — trái doctrine 'chỉ push GDoc'",
        rep["raw_on_nlm"],
        "tl sweep --json  # xem raw_on_nlm_rows; từng dòng: copy_convert → nlm-add GDoc mới → source-update-corpus raw false --apply --confirm yes",
        False,
        "KHÔNG auto: phải bảo đảm GDoc mới đã push thành công trước khi gỡ source raw cũ; ưu tiên Luật trước.",
        rep.get("raw_on_nlm_rows"))
    add(9, "raw_dup_of_standard", "human_confirm",
        "Bản TẢI THÔ nghi TRÙNG bản chuẩn (tên thô không trích được sohieu, kẹt corpus=true, đốt batch ingest-missing)",
        rep["raw_dup_of_standard"], "tl source-update-corpus <drive_id> false --apply   # per-row, undo được", True,
        "PROPOSE-ONLY (match lỏng số+năm[+loại]): soát từng dòng raw_dup_of_standard_rows rồi tắt corpus bản thô.",
        rep.get("raw_dup_of_standard_rows"))
    add(10, "nlm_status_mismatch", "safe_auto",
        "Nhãn nlm_status LẠ (hygiene, KHÔNG phải desync sống)",
        dr.get("NLM_STATUS_MISMATCH", 0), f"tl nlm-orphans {nb} --fix-mismatch --apply", True,
        "Vá nhãn metadata (removed*→pushed nếu nguồn sống).")
    add(11, "corpus_not_on_nlm", "structural",
        "corpus=true CHƯA trên NLM (phần lớn do cap 300/notebook)",
        dr.get("CORPUS_TRUE_NOT_ON_NLM", 0), "tl ingest-missing --apply   (cần slot/overflow — JOB LỚN, KHÔNG về 0)", False,
        "CẤU TRÚC: corpus>cap → cần sharding/overflow.")
    add(12, "consolidation", "human_confirm",
        "Cùng lúc CÓ VBHN + gốc/sửa đổi RỜI còn corpus=true → nên gộp về VBHN (khi tìm thành phần trả ra VBHN)",
        consol, "tl consolidation-cleanup", True, "Set thành phần corpus=false khi VBHN verify phủ (reversible).")
    add(13, "quarantine_conflict", "safe_auto",
        "Quarantine MÂU THUẪN (corpus=true / stale NLM ref; nguồn LIVE xoá tay)",
        rep["quarantine"]["corpus_true"] + rep["quarantine"]["stale_nlm_ref"] + rep["quarantine"]["still_on_nlm"],
        "tl quarantine-fix --apply", True,
        "REVERSIBLE: chuẩn nhãn + corpus=false + reg_clear stale nlm_source_id (B3/B9 v1.33.22); "
        "still_on_nlm chỉ báo — xoá nguồn LIVE tay sau verify.")
    steps.sort(key=lambda s: s["order"])
    return {"ok": True, "total": rep["total"], "corpus": rep["corpus"], "step_count": len(steps), "steps": steps,
            "safe_auto": [s for s in steps if s["tier"] == "safe_auto"],
            "needs_human": [s for s in steps if s["tier"] != "safe_auto"],
            "note": "CHẠY THEO `order` (sai thứ tự=hỏng thêm). safe_auto=reversible (corpus=false) → `corpus-fix --apply "
                    "--tier safe`. metadata/human_confirm/structural: chạy lệnh in sẵn, người duyệt (đọc header/xác minh)."}


_LOOP_LIVE_FIELDS = ("corpus", "nlm_source_id", "nlm_status", "nlm_notebook_id")


def _source_find(entries: list, target: str):
    tkey = norm_sohieu(target.replace("_", "-")) if _looks_like_sohieu_query(target) else ""
    return next((x for x in entries if _entry_drive_id(x) == target or (tkey and _sohieu_key_entry(x) == tkey)), None)


# N2c (v1.33.41): +van phong — 'VĂN PHÒNG QUỐC HỘI' (cơ quan ký VBHN) từng lọt thành CHỦ ĐỀ đặt tên
# ('Văn phòng quốc hội' thay vì chủ đề luật); 'quoc hoi' trần không bắt vì dòng bắt đầu bằng 'van phong'.
_SUBJ_NOISE_RE = re.compile(r"^(cong hoa|doc lap|quoc hoi|van phong|chinh phu|uy ban|ha noi|can cu|bo truong|thu tuong|"
                            r"du thao|draft|lay y kien|độc lập|cộng hòa)", re.I)
_SUBJ_LOAI_RE = re.compile(r"^(bộ luật|bo luat|luật|luat|pháp lệnh|phap lenh|nghị định|nghi dinh|nghị quyết|nghi quyet|"
                           r"thông tư|thong tu|quyết định|quyet dinh|văn bản hợp nhất|van ban hop nhat|chỉ thị|chi thi|"
                           r"kế hoạch|ke hoach)\b\s*", re.I)


def _vb_ingest_auto_plan(path: str, text_file: str | None = None, name: str = "", sohieu: str = "",
                         loai: str = "", cat: str = "", source_quality: str = "auto",
                         ocr_verified: bool = False) -> dict:
    probe_text, probe_source = _profile_read_probe_text(path, text_file)
    _fname = Path(path).name    # (MERGE Claude) CHỈ tên file (KHÔNG full path) → tránh _RAW_SOHIEU_RE bắt nhầm fragment UUID trong đường dẫn
    info = _classify_doc_header(probe_text, _fname)
    fallback_info = _classify_doc_header("", _fname)
    merged = dict(info)
    for k in ("sohieu", "sohieu_key", "loai", "issue_year"):
        if not merged.get(k) and fallback_info.get(k):
            merged[k] = fallback_info.get(k)
    if sohieu:
        merged["sohieu"] = sohieu
        merged["sohieu_key"] = norm_sohieu(sohieu)
    if loai:
        merged["loai"] = loai
    # (MERGE Claude) CHỦ ĐỀ đặt tên lấy từ dòng tiêu đề THẬT (bỏ dòng số hiệu/DỰ THẢO, strip loại, ALL-CAPS→sentence)
    # → chống tên Codex lặp số hiệu; dự thảo dùng _safe_profile_doc_name (DUTHAO_).
    _subj = _doc_subject_for_name(probe_text, merged)
    if _subj:
        merged["title"] = _subj.capitalize() if _subj.isupper() else _subj
    if (name or "").strip():
        doc_name = name.strip()
    elif merged.get("draft"):
        doc_name = _safe_profile_doc_name(merged, Path(_fname).stem)
    else:
        doc_name = _vb_standard_doc_name(merged, Path(_fname).stem)
    cat_plan = _vb_auto_cat_from_text(probe_text, doc_name + "\n" + Path(path).stem, cat)
    warnings = []
    # N2d (v1.33.41 — log rà VBHN-first: auto-plan gợi cat=00 [văn kiện Đảng] cho VBHN Luật giám sát QH): cat 00
    # KHÔNG BAO GIỜ hợp lệ cho VBQPPL (mirror gate _CAT_PIN/_cat_likely_wrong 'Luật không→23, VBHN không→46') —
    # thân luật nhắc 'Đảng' làm alias 00 thắng điểm. Hạ về rỗng + cảnh báo, KHÔNG ghi bừa.
    if cat_plan.get("cat") == "00" and str(merged.get("loai") or "") in {
            "Luật", "Bộ luật", "Pháp lệnh", "Văn bản hợp nhất", "Nghị định", "Thông tư", "Quyết định"}:
        warnings.append("CAT_00_PARTY_BLOCKED_FOR_VBQPPL")
        cat_plan = dict(cat_plan, cat="", confidence="low",
                        note="cat 00 (văn kiện Đảng) không hợp lệ cho VBQPPL — truyền --cat tường minh")
    # N2 (v1.33.41): VBHN auto-plan KHÔNG đáng tin bằng luật thường (số VBHN ở khối ký cuối, tên chủ đề dễ dính
    # cơ quan) — nhắc tường minh để driver set --name/--sohieu/--cat theo bản hợp nhất.
    if str(merged.get("loai") or "") == "Văn bản hợp nhất":
        warnings.append("VBHN_AUTO_PLAN_VERIFY_EXPLICIT: đối chiếu --sohieu (số VBHN, KHÔNG phải số luật gốc) "
                        "+ --name (chủ đề) + --cat trước khi --apply")
    if not probe_text:
        warnings.append("NO_PROBE_TEXT_FOR_AUTO_CAT")
    if not merged.get("sohieu"):
        warnings.append("SOHIEU_MISSING")
    if cat_plan.get("confidence") in {"low", "missing"}:
        warnings.append("CAT_AUTO_LOW_CONFIDENCE")
    srcq = _profile_source_quality(path, source_quality)
    if srcq == "ocr" and not ocr_verified:
        warnings.append("OCR_UNVERIFIED_NOT_CORPUS")
    return {
        "ok": bool(doc_name and cat_plan.get("cat")),
        "file": path,
        "probe_text_source": probe_source or None,
        "probe_chars": len(probe_text or ""),
        "classification": merged,
        "name": doc_name,
        "sohieu": merged.get("sohieu") or "",
        "loai": merged.get("loai") or "",
        "cat": cat_plan.get("cat") or "",
        "cat_plan": cat_plan,
        "source_quality": srcq,
        "ocr_verified": bool(ocr_verified),
        "warnings": warnings,
        "note": "Auto-plan chỉ đáng tin khi có probe text/OCR text; thiếu text thì cần --text-file, --cat hoặc --force-cat.",
    }


# corpus-audit (A+B): ENGINE ĐỀ XUẤT dùng CHUNG — đọc HEADER thật, SO registry, trả worklist SỬA (propose-only).
# Xếp hạng: số nhỏ = nặng hơn (in trước). PROPOSE-ONLY: nội dung/trích yếu là phán đoán → KHÔNG auto (chỉ header làm ground-truth).
_AUDIT_SEVERITY = {
    "SOHIEU_MISMATCH": (0, "🔴"), "LOAI_MISMATCH": (1, "🔴"), "NAME_TRICH_YEU": (2, "🟠"),
    "NAME_NONSTANDARD": (2, "🟠"), "CAT_LIKELY_WRONG": (3, "🟡"),
    "MISSING_YEAR": (3, "🟡"), "CAT_MISMATCH": (4, "🟢"),
}

# A2 (v1.33.0 — log rà 69: 'BLDS_91-2015-QH13_Bo_luat_Dan_su' bị NAME_NONSTANDARD đòi đổi tên dù BLDS_ là quy
# ước HỢP LỆ — viết tắt Bộ luật, khớp _ABBREV_MAP): whitelist các viết tắt Bộ luật vào tiền tố chuẩn.
# _NAME_PREFIX_FAMILY: đổi tên BLDS_↔Bo_luat_ là CÙNG HỌ loại — không tính 'đổi mã loại' (guard i2c v1.29.4).
_NAME_TYPE_PREFIX_RE = re.compile(
    r"^(Luat|Bo_luat|BLuat|BLDS|BLHS|BLLD|BLTTHS|BLTTDS|BLHH|VBHN|ND|TT|NQ|QD|PL|HP|KL|CT|CD|TTLT|TB)[_\-]")
# P1-3 (v1.33.12 — log phiên khắc phục: standardize_name SINH `BLuat_` cho mọi Bộ luật, corpus đã có
# BLuat_100-2015/45-2019 sau source-rename, nhưng checker chưa nhận → sẽ flag oan chính tên chuẩn hoá vừa sinh):
# DOCTRINE ĐẶT TÊN chốt: `BLuat_` là CHUẨN SINH TỰ ĐỘNG cho Bộ luật; BLDS_/BLHS_/BLLĐ_… là legacy HỢP LỆ
# (cùng họ Bo_luat — không coi là 'đổi mã loại'; migrate dần khi rename, không bắt buộc).
_NAME_PREFIX_FAMILY = {"BLuat": "Bo_luat", "BLDS": "Bo_luat", "BLHS": "Bo_luat", "BLLD": "Bo_luat",
                       "BLTTHS": "Bo_luat", "BLTTDS": "Bo_luat", "BLHH": "Bo_luat"}


# Trích yếu KHÔNG được là tên CƠ QUAN/boilerplate — chống dựng tên LỆCH chủ đề (vd header VBHN nêu 'VĂN PHÒNG QUỐC HỘI'
# ở đầu → _doc_subject_for_name nhặt nhầm thay vì 'Kế toán'). Đây là ca thật lộ khi chạy corpus-audit trên manifest.
# v1.29.4 (log LIVE i2b — ca 'TT_104-2017-TT-BTC_Bo_tai_chinh'): thêm tên BỘ-NGÀNH cụ thể. KHÔNG dùng pattern '^bo '
# chung chung: strip-accents làm 'Bổ sung…'→'bo sung' đụng 'Bộ…' → false-positive trên trích yếu thật.
_SUBJECT_BOILERPLATE = ("van phong quoc hoi", "quoc hoi", "uy ban thuong vu quoc hoi", "chinh phu", "thu tuong",
                        "bo truong", "hoi dong nhan dan", "hoi dong", "van ban hop nhat", "cong hoa xa hoi",
                        "bo tai chinh", "bo y te", "bo cong an", "bo noi vu", "bo tu phap", "bo giao duc",
                        "bo cong thuong", "bo quoc phong", "bo khoa hoc", "bo xay dung", "bo giao thong",
                        "bo nong nghiep", "bo ke hoach", "bo thong tin", "bo van hoa", "bo lao dong",
                        "bo tai nguyen", "bo ngoai giao", "ngan hang nha nuoc", "bo chinh tri", "ban bi thu",
                        "ban chap hanh trung uong")


# Quyết định 26/6 (SKILL.md — pháp điển CHƯA có đề mục riêng): AI/Chuyển đổi số/Công nghiệp công nghệ số TẠM giữ
# cat 19 (KHCN) — auditor KHÔNG được coi là misfile hay đề xuất dời (log rà 69 A1d: corpus-audit từng vi phạm
# chính doctrine này, đề xuất dời 134/148/71/93 khỏi 19). IM LẶNG CẢ 2 CHIỀU ("KHÔNG tự chuyển 03/flag misfile").
_CAT19_PIN_RE = re.compile(r"tri tue nhan tao|chuyen doi so|cong nghiep cong nghe so")

# A2 (v1.33.2 — log rà 111: VBHN_62 XNC người NN bị đề xuất 01→39, trái thẳng §0.13): PIN CAT theo doctrine
# SKILL.md §0.13 "KHÔNG đoán cat" — title khớp pin thì DOCTRINE thắng mọi alias/boundary suy diễn:
# cat hiện tại ĐÚNG pin → im; KHÁC pin → đề xuất CHÍNH pin (không đề xuất cat suy diễn).
_CAT_PIN_RULES = (
    (re.compile(r"xuat canh|nhap canh|xuat nhap canh"), "01", "xuất/nhập cảnh = 01 An ninh quốc gia (§0.13 — không 23/39)"),
    (re.compile(r"\bto tung\b"), "37", "tố tụng = 37 (§0.13 — không 09/16)"),
    (re.compile(r"\bdan toc\b"), "10", "dân tộc = 10 (§0.13)"),
)


_DECLARED_LOAI_MAP = (("van ban hop nhat", "Văn bản hợp nhất"), ("bo luat", "Bộ luật"),
                      ("phap lenh", "Pháp lệnh"), ("nghi dinh", "Nghị định"),
                      ("thong tu lien tich", "Thông tư liên tịch"), ("thong tu", "Thông tư"),
                      ("nghi quyet", "Nghị quyết"), ("quyet dinh", "Quyết định"),
                      ("hien phap", "Hiến pháp"), ("luat", "Luật"))


def _audit_row_flatten(r: dict) -> dict:
    """S-1 (v1.33.15 — log rà 40: driver đọc rows[].type/severity/suggested_name/proposal = null trong khi
    summary đếm proposal_count=2 — chi tiết chỉ nằm LỒNG trong proposals[], schema summary↔row lệch nhau):
    MIRROR đề xuất CHÍNH (proposals[0] — đã sort severity, nặng nhất) lên top-level row để driver phẳng đọc
    được; proposals[] giữ nguyên là nguồn sự thật đầy đủ. Idempotent (gọi lại trên row đã flatten vô hại)."""
    ps = r.get("proposals") or []
    p0 = ps[0] if ps else {}
    r["type"] = p0.get("type")
    r["severity"] = p0.get("severity")
    r["icon"] = p0.get("icon")
    r["current"] = p0.get("current")
    r["suggested"] = p0.get("suggested")
    r["suggested_name"] = p0.get("suggested")   # alias — driver log rà 40 đọc key này
    r["fix_command"] = p0.get("fix_command")
    r["command"] = p0.get("fix_command")        # v1.33.16 (MERGE nhánh-4): alias `command` cho driver phẳng
    r["proposal"] = p0 or None
    r["proposal_count"] = len(ps)               # v1.33.16 (MERGE nhánh-4): đối soát nhanh không cần đếm proposals[]
    r["flags"] = [p.get("type") for p in ps]
    return r


# B (v1.33.3): nhóm cờ → VIỆC-CẦN-LÀM cho review-queue (đối chiếu _source_map_verdict.review).
_RQ_WEB_FLAGS = frozenset({"NO_VERIFIED_VBHN_IN_CORPUS", "QT5_WEB_REQUIRED",
                           "VBHN_CANDIDATE_UNVERIFIED_LATEST", "VBHN_HIGH_AMENDMENT_VELOCITY"})
_RQ_REL_FLAGS = frozenset({"UNLINKED_AMENDMENT_CANDIDATE", "VBHN_RECHECK_REQUIRED",
                           "AMENDMENT_CANDIDATE_IN_CORPUS", "AMENDMENT_CANDIDATE_LOW_CONFIDENCE"})
# A1 (v1.33.4 — log chạy LIVE review-queue lần đầu: 2/5 relation_backfill là VIỆC KHỐNG — 19-2012 verdict=OK +
# AMENDMENT_CANDIDATES_COVERED_BY_VBHN_DATE, 90-2025 OK + CONFIRMED): cờ HOÁ-GIẢI mà source-map đã tính —
# bucket rel phải tôn trọng, không phân loại lại thuần theo cờ thô AMENDMENT_CANDIDATE_IN_CORPUS.
_RQ_REL_SUPPRESS = frozenset({"AMENDMENTS_ALREADY_CONSOLIDATED", "AMENDMENT_CANDIDATES_COVERED_BY_VBHN_DATE",
                              "AMENDMENT_GATE_SUPPRESSED_CONFIRMED", "CONFIRMED", "OMNIBUS_AMENDS_OTHER"})


def _rq_rel_strong(cands: list[dict]) -> bool:
    """P2-2 (v1.33.12): ứng viên đủ MẠNH cho bucket HÀNH ĐỘNG relation_backfill — linked/strong/confidence≠low
    (cùng ngưỡng escalate v1.29.6). Toàn low-conf → relation_low_confidence (INFO), vì `relation-check --base
    --subject` (chuẩn) thường phủ định các ca này (log: 3/3 trả OK, missing_links=[])."""
    return any(bool(c.get("linked_to_query")) or bool(c.get("strong"))
               or (str(c.get("confidence") or "low") != "low") for c in (cands or []))


def _rq_relation_probe(entries: list[dict], e: dict) -> dict:
    """S-1 (v1.33.32 — MERGE bundle-12 hội tụ trên cùng log): cross-check cờ ứng-viên-sửa-đổi của source-map
    bằng CHÍNH engine relation-check (`_relation_audit`, PURE). source-map chủ động RỘNG để không bỏ sót; bucket
    rel của nó đã nhiều lần tạo P0 giả (124/125-2025, 68-2025, 44-2019 — LIVE relation-check trả OK/candidates=[]).
    Tiêu chí phủ định (PORT bundle-12, tinh chỉnh): KHÔNG còn tín hiệu HÀNH ĐỘNG ĐƯỢC — missing_links /
    subject_only_review / footnote_only_amendments đều rỗng. KHÔNG đòi verdict=OK (thiếu VBHN → QT5 là việc của
    bucket WEB, không giữ oan tín hiệu rel); candidates ĐÃ-linked-đủ cũng không chặn (không có gì để backfill —
    tinh chỉnh so với bundle: họ tính cả amend_n → giữ oan ca đã hợp nhất xong)."""
    base = _sohieu_key_entry(e) or _entry_sohieu(e) or ""
    subject = (_derive_subject_from_entries([e]) or _clean_subject_text(_name_tail_pretty(_entry_name(e)))
               or _entry_name(e))
    try:
        audit = _relation_audit(entries, base=base, subject=subject)
    except Exception as ex:  # noqa: BLE001 — probe phụ trợ không được giết queue
        return {"ok": False, "suppressed": False, "error": f"{type(ex).__name__}: {str(ex)[:120]}"}
    missing_n = len(audit.get("missing_links") or [])
    subject_only_n = len(audit.get("subject_only_review") or [])
    footnote_only_n = len(audit.get("footnote_only_amendments") or [])
    actionable = bool(missing_n or subject_only_n or footnote_only_n)
    return {"ok": True, "suppressed": not actionable, "verdict": audit.get("verdict"),
            "flags": sorted(audit.get("flags") or []), "subject": audit.get("subject") or subject,
            "missing_links": missing_n,
            "amendment_candidates": len(audit.get("amendment_candidates") or []),
            "subject_only_review": subject_only_n, "footnote_only_amendments": footnote_only_n,
            "note": ("relation-check PHỦ ĐỊNH — không missing_links/subject_only/footnote-thiếu; "
                     "không đưa P0/backfill" if not actionable else
                     "relation-check còn tín hiệu cần soi — giữ INFO, không tự ghi")}


def _dieu_sequence_stats(text: str) -> dict:
    nums = [int(x) for x in re.findall(r"(?mi)^\s*Điều\s+(\d+)\b", text or "")]
    gaps = []
    for a, b in zip(nums, nums[1:]):
        if b > a + 1:
            gaps.append({"after": a, "before": b})
    return {"count": len(nums), "first": nums[0] if nums else None, "last": nums[-1] if nums else None,
            "monotonic": all(b > a for a, b in zip(nums, nums[1:])), "gaps": gaps[:20]}


def _idempotency_contract_for_workflow(wf_id: str) -> dict:
    key = wf_id
    if wf_id == "chunk_ingest":
        key = "profile_ingest_chunks"
    if wf_id == "ocr_ingest":
        key = "ocr_ingest"
    if wf_id == "ingest_zip":
        key = "ingest_zip"
    return dict(_IDEMPOTENCY_CONTRACTS.get(key, {}))


def _available_commands_from_parser() -> list[str]:
    try:
        ap = build_parser()
        for act in ap._actions:
            if isinstance(act, argparse._SubParsersAction):
                return sorted(act.choices.keys())
    except Exception:
        pass
    return []


def _script_docstrings(limit: int = 200) -> list[dict]:
    out = []
    for sp in sorted(HERE.glob("*.py"))[:limit]:
        try:
            txt = sp.read_text(encoding="utf-8", errors="replace")
            m = re.search(r'^[uUrRfFbB]*(?:"""|\'\'\')(.*?)(?:"""|\'\'\')', txt, re.S)
            doc = " ".join((m.group(1).strip().splitlines()[:2] if m else []))
        except Exception as e:
            doc = f"ERROR_READING:{type(e).__name__}"
        out.append({"script": sp.name, "doc": doc[:240]})
    return out


def _unique_preserve_order(items) -> list[str]:
    seen = set()
    out = []
    for item in items or []:
        s = str(item)
        if s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


_VOLATILE_JSON_KEYS = _tl_det.VOLATILE_JSON_KEYS   # v1.33.55: nguồn chuẩn ở tl_core.deterministic


def _deterministic_enabled(a=None) -> bool:
    return _tl_det.deterministic_enabled(a, default_on=_DETERMINISTIC_ON)


def _stable_string_for_json(s: str) -> str:
    return _tl_det.stable_string_for_json(s, project_root=HERE.parent)


def _scrub_volatile(obj):
    return _tl_det.scrub_volatile(obj, project_root=HERE.parent)


def _json_dumps(obj, *, deterministic: bool | None = None) -> str:
    return _tl_det.json_dumps(
        obj,
        deterministic=(_deterministic_enabled() if deterministic is None else bool(deterministic)),
        default_on=_DETERMINISTIC_ON,
        project_root=HERE.parent,
    )


def _print_json_or_text(obj: dict, as_json: bool) -> None:
    return _tl_jsonio.print_json_or_text(obj, as_json, json_dumps_func=_json_dumps)


def _split_source_ids(values: list[str] | None, combined: str = "") -> list[str]:
    raw = []
    for val in values or []:
        raw.extend(str(val).split(","))
    if combined:
        raw.extend(str(combined).split(","))
    return _unique_preserve_order([x.strip() for x in raw if x and x.strip()])


# ───────────────────────── convert / rename readback verification ─────────────────────────
_GDOC_MIME = "application/vnd.google-apps.document"
_GSHEET_MIME = "application/vnd.google-apps.spreadsheet"   # v1.34.6 #2: canonical bảng tính = Google Sheet


def _drive_info_file(g, file_id: str) -> dict:
    """Best-effort Drive metadata readback qua webapp action=info. Không raise."""
    if not file_id:
        return {"ok": False, "error": "EMPTY_FILE_ID", "file": {}}
    try:
        info = g.get("info", fileId=file_id)
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"INFO_EXCEPTION:{type(e).__name__}:{e}", "file": {}}
    if not isinstance(info, dict):
        return {"ok": False, "error": "INFO_NON_DICT", "raw": str(info)[:200], "file": {}}
    f = info.get("file") if isinstance(info.get("file"), dict) else info
    return {"ok": bool(info.get("ok", True) and (f.get("id") or f.get("fileId") or file_id)), "raw": info, "file": f}


def _file_mime(info: dict) -> str:
    f = info.get("file") or {}
    return str(f.get("mimeType") or f.get("mime") or "").strip()


def _file_parents(info: dict) -> list[str]:
    f = info.get("file") or {}
    parents = f.get("parents") or f.get("parentIds") or []
    if isinstance(parents, str):
        return [parents]
    return [str(x.get("id") if isinstance(x, dict) else x) for x in parents if x]


_VIET_CHARS = set("ăâđêôơưáàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵĂÂĐÊÔƠƯÁÀẢÃẠẮẰẲẴẶẤẦẨẪẬÉÈẺẼẸẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌỐỒỔỖỘỚỜỞỠỢÚÙỦŨỤỨỪỬỮỰÝỲỶỸỴ")


def _run_child_tl(args: list[str]) -> dict:
    cmd = [sys.executable, str(HERE / "tl.py")] + args
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUTF8", "1")
    try:
        # v1.33.56 (review PH2-01 P0): encoding tường minh — text=True trần decode theo LOCALE (cp1258 máy VN)
        # trong khi child LUÔN in UTF-8 → UnicodeDecodeError/mojibake với output tiếng Việt.
        cp = subprocess.run(cmd, text=True, encoding="utf-8", errors="replace", capture_output=True,
                            timeout=900, env=env)
    except subprocess.TimeoutExpired as e:  # PH2-09: không để traceback giữa pipeline
        return {"cmd": " ".join(args), "returncode": 124, "ok": False, "json": None,
                "error": "CHILD_TIMEOUT_900S",
                "stdout_tail": (e.stdout or "")[-2000:] if isinstance(e.stdout, str) else "",
                "stderr_tail": (e.stderr or "")[-2000:] if isinstance(e.stderr, str) else ""}
    payload = None
    try:
        payload = json.loads(cp.stdout) if cp.stdout.strip().startswith("{") else None
    except Exception:
        payload = None
    return {"cmd": " ".join(args), "returncode": cp.returncode, "ok": cp.returncode == 0,
            "json": payload, "stdout_tail": cp.stdout[-2000:], "stderr_tail": cp.stderr[-2000:]}


def _text_quality_metrics(text: str) -> dict:
    chars = len(text or "")
    letters = sum(1 for c in text if c.isalpha())
    vi_marks = sum(1 for c in text if c in _VIET_CHARS)
    garbled = len(re.findall(r"[�\ufffd]", text or ""))
    articles = len(re.findall(r"(?im)^\s*Điều\s+\d+[a-zA-Z]?\s*[\.:]", text or ""))
    appendices = len(re.findall(r"(?im)^\s*Phụ\s*lục\b", text or ""))
    lines = len((text or "").splitlines())
    return {
        "chars": chars,
        "lines": lines,
        "letters": letters,
        "vietnamese_mark_density": round(vi_marks / max(letters, 1), 6),
        "garbled_ratio": round(garbled / max(chars, 1), 6),
        "article_count": articles,
        "appendix_count": appendices,
    }


def _read_local_text_for_analysis(path: Path, max_chars: int = 500000) -> tuple[str, list[str]]:
    warnings = []
    ext = path.suffix.lower()
    if ext in {".txt", ".md"}:
        return path.read_text(encoding="utf-8", errors="replace")[:max_chars], warnings
    if ext == ".pdf":
        exe = shutil.which("pdftotext")
        if not exe:
            return "", ["PDFTOTEXT_NOT_AVAILABLE_TEXT_LAYER_UNKNOWN"]
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out.txt"
            try:
                subprocess.run([exe, "-layout", str(path), str(out)], timeout=30, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if out.exists():
                    return out.read_text(encoding="utf-8", errors="replace")[:max_chars], warnings
            except Exception as e:
                return "", [f"PDFTOTEXT_ERROR:{type(e).__name__}"]
        return "", ["PDFTOTEXT_NO_OUTPUT"]
    return "", ["TEXT_EXTRACTION_NOT_IMPLEMENTED_FOR_EXT:" + ext]


def _write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    _fd, _tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    with os.fdopen(_fd, "w", encoding="utf-8", errors="replace", newline="\n") as _f:   # v1.33.56 (F7): tmp duy nhất
        _f.write(text)
    os.replace(_tmp, str(path))


def _sha256_bytes_file_local(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _bridge_confirm_apply(a, *, what: str) -> tuple[bool, dict]:
    if not getattr(a, "apply", False):
        return True, {}
    if getattr(a, "confirm", "") != "yes":
        return False, {"ok": False, "error": "CONFIRM_REQUIRED", "what": what,
                       "note": "Bridge apply sẽ gọi lại pipeline ingest hiện có. Thêm --confirm yes sau khi đã xem dry-run/verify."}
    return True, {}


def _run_tl_json(args: list[str], *, timeout: int = 60, env_extra: dict | None = None) -> dict:
    env = os.environ.copy()
    env["TL_DETERMINISTIC"] = "1"
    if env_extra:
        # v1.34.3 (I1): golden case tự mang env (vd TL_CACHE_DIR → fixture manifest) — cách ly trạng thái máy.
        env.update({str(k): str(v) for k, v in env_extra.items()})
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("TZ", "UTC")
    cmd = [sys.executable, str(HERE / "tl.py"), "--deterministic"] + list(args)
    try:
        cp = subprocess.run(cmd, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired as e:
        return {
            "ok": False,
            "cmd": cmd,
            "returncode": 124,
            "error": "TIMEOUT_EXPIRED",
            "stdout_tail": (e.stdout or "")[-1200:] if isinstance(e.stdout, str) else "",
            "stderr_tail": (e.stderr or "")[-1200:] if isinstance(e.stderr, str) else "",
        }
    stdout = (cp.stdout or "").strip()
    data = None
    parse_error = ""
    if stdout:
        try:
            data = json.loads(stdout)
        except Exception as e:  # noqa: BLE001
            parse_error = f"{type(e).__name__}: {e}"
    return {
        "ok": cp.returncode == 0 and isinstance(data, dict),
        "cmd": cmd,
        "returncode": cp.returncode,
        "data": data,
        "parse_error": parse_error,
        "stdout": stdout,   # v1.33.59: raw đầy đủ cho check raw-stability của golden-test
        "stdout_tail": stdout[-1200:],
        "stderr_tail": (cp.stderr or "")[-1200:],
    }


def _first_text_diff(expected: str, actual: str) -> dict:
    exp_lines = expected.splitlines()
    act_lines = actual.splitlines()
    for idx, (e, a) in enumerate(zip(exp_lines, act_lines), 1):
        if e != a:
            return {"line": idx, "expected": e[:240], "actual": a[:240]}
    if len(exp_lines) != len(act_lines):
        return {"line": min(len(exp_lines), len(act_lines)) + 1, "expected": "<EOF>" if len(exp_lines) < len(act_lines) else exp_lines[-1][:240], "actual": "<EOF>" if len(act_lines) < len(exp_lines) else act_lines[-1][:240]}
    return {}


def _path_age_days(path: Path) -> float | None:
    try:
        if not path.exists():
            return None
        return round(max(0.0, (time.time() - path.stat().st_mtime) / 86400.0), 3)
    except Exception:
        return None


def _file_auth_state(path: Path) -> dict:
    return {"path": str(path), "exists": path.exists(), "age_days": _path_age_days(path)}


def _cmd_version_probe(name: str, args: list[str] | None = None, *, timeout: int = 10) -> dict:
    exe = shutil.which(name)
    out = {"command": name, "path": exe or "", "ok": False, "version": "", "returncode": None}
    if not exe:
        out["error"] = "BINARY_NOT_FOUND"
        return out
    try:
        cp = subprocess.run([exe] + (args or ["--version"]), text=True, encoding="utf-8", errors="replace",
                            capture_output=True, timeout=timeout)
        text = ((cp.stdout or "") + "\n" + (cp.stderr or "")).strip()
        out.update({"ok": cp.returncode == 0, "returncode": cp.returncode, "version": text.splitlines()[0][:160] if text else ""})
        if cp.returncode != 0:
            out["error"] = text[-300:]
    except Exception as e:  # noqa: BLE001
        out.update({"error": f"{type(e).__name__}: {e}"})
    return out


def _sha256_path_or_empty(path: str) -> str:
    try:
        p = Path(path).expanduser()
        return _sha256_file(p) if p.exists() and p.is_file() else ""
    except Exception:
        return ""


def _deploy_plan(bundle: str = "", target_dir: str = "", backup_dir: str = "", profile: str = "", include_ocr: bool = False) -> dict:
    bundle_path = Path(bundle).expanduser().resolve() if bundle else None
    target = Path(target_dir).expanduser().resolve() if target_dir else Path.cwd().resolve() / "tra-luat"
    backup = Path(backup_dir).expanduser().resolve() if backup_dir else target.parent / "_tra_luat_backups"
    steps = [
        {"id": "verify_bundle_sha", "mode": "manual", "command": ["sha256sum", str(bundle_path) if bundle_path else "<bundle.zip>"], "expect": "so sánh với SHA-256 đã công bố"},
        {"id": "extract_to_temp", "mode": "manual", "command": ["unzip", "-q", str(bundle_path) if bundle_path else "<bundle.zip>", "-d", "<temp_dir>"], "expect": "giải nén vào thư mục tạm, không ghi đè bản đang chạy"},
        {"id": "verify_extracted_manifest", "mode": "manual", "command": ["python", "scripts/tl.py", "release-verify", "RELEASE_MANIFEST.json", "--json"], "expect": "ok=true trong thư mục đã giải nén"},
        {"id": "backup_current", "mode": "manual", "command": ["cp", "-a", str(target), str(backup / "tra-luat-<timestamp>")], "expect": "có bản rollback trước khi thay"},
        {"id": "replace_or_sync", "mode": "manual", "command": ["rsync", "-a", "--delete", "<temp_dir>/tra-luat/", str(target) + "/"], "expect": "chỉ thay sau khi verify extracted pass"},
        {"id": "offline_release_check", "mode": "manual", "command": ["python", "scripts/tl.py", "release-check", "--json"], "expect": "ok=true tại target"},
        {"id": "live_readiness", "mode": "manual", "command": ["python", "scripts/tl.py", "live-readiness", "--json"], "expect": "env_ready=true và live_contract_ready=true trước smoke"},
        {"id": "snapshot_before", "mode": "manual", "command": ["python", "scripts/tl.py", "live-state-snapshot", "--out", "before.json", "--json"], "expect": "lưu baseline trạng thái live trước smoke"},
        {"id": "live_smoke_plan", "mode": "manual", "command": ["python", "scripts/tl.py", "live-smoke-plan", "--json"] + (["--include-ocr"] if include_ocr else []), "expect": "chạy từng bước, dừng khi high-risk fail"},
        {"id": "snapshot_after", "mode": "manual", "command": ["python", "scripts/tl.py", "live-state-snapshot", "--out", "after.json", "--json"], "expect": "lưu trạng thái sau smoke"},
        {"id": "snapshot_diff", "mode": "manual", "command": ["python", "scripts/tl.py", "live-state-diff", "before.json", "after.json", "--json", "--allow", "source_counts", "--allow", "notebooks.get.source_count"], "expect": "chỉ có thay đổi dự kiến"},
    ]
    return {"ok": True, "schema": "deploy_plan.v1", "bundle": str(bundle_path) if bundle_path else None, "bundle_exists": bool(bundle_path and bundle_path.exists()), "bundle_sha256": _sha256_path_or_empty(str(bundle_path)) if bundle_path else "", "target_dir": str(target), "backup_dir": str(backup), "profile": profile or None, "include_ocr": include_ocr, "steps": steps, "stop_rule": "Không replace/sync nếu release-verify trong temp fail. Không chạy apply live nếu live-readiness chưa đạt env+contract hoặc snapshot diff có thay đổi ngoài dự kiến.", "note": "READ-ONLY plan; lệnh này không giải nén, không copy, không gọi Drive/NLM."}


def _rollback_plan(target_dir: str = "", backup_path: str = "", bundle: str = "") -> dict:
    target = Path(target_dir).expanduser().resolve() if target_dir else Path.cwd().resolve() / "tra-luat"
    backup = Path(backup_path).expanduser().resolve() if backup_path else None
    bundle_path = Path(bundle).expanduser().resolve() if bundle else None
    source_desc = str(backup or bundle_path or "<backup_dir_or_previous_bundle.zip>")
    steps = [
        {"id": "stop_running_clients", "mode": "manual", "command": ["<close Claude/terminal sessions using this skill>"], "expect": "không còn process ghi vào skill dir"},
        {"id": "snapshot_failed_state", "mode": "manual", "command": ["cp", "-a", str(target), str(target.parent / "_failed_tra_luat_<timestamp>")], "expect": "giữ lại bản lỗi để diff"},
        {"id": "restore_backup", "mode": "manual", "command": ["rsync", "-a", "--delete", source_desc.rstrip('/') + "/", str(target) + "/"], "expect": "khôi phục từ backup đã pass"},
        {"id": "verify_manifest", "mode": "manual", "command": ["python", "scripts/tl.py", "release-verify", "RELEASE_MANIFEST.json", "--json"], "expect": "ok=true nếu backup có manifest"},
        {"id": "release_check", "mode": "manual", "command": ["python", "scripts/tl.py", "release-check", "--json"], "expect": "ok=true sau rollback"},
        {"id": "live_readiness", "mode": "manual", "command": ["python", "scripts/tl.py", "live-readiness", "--json"], "expect": "cấu hình/auth vẫn còn"},
    ]
    return {"ok": True, "schema": "rollback_plan.v1", "target_dir": str(target), "backup_path": str(backup) if backup else None, "bundle": str(bundle_path) if bundle_path else None, "source_exists": bool((backup and backup.exists()) or (bundle_path and bundle_path.exists())), "steps": steps, "stop_rule": "Không xóa bản lỗi trước khi snapshot; không rollback từ nguồn chưa verify.", "note": "READ-ONLY plan; không copy/replace thật."}


def _run_release_child(args: list[str], *, timeout: int = 60) -> dict:
    cmd = [sys.executable, str(HERE / "tl.py")] + args
    t0 = time.time()
    try:
        cp = subprocess.run(cmd, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=timeout)
        return {"cmd": args, "returncode": cp.returncode, "ok": cp.returncode == 0, "seconds": round(time.time() - t0, 3),
                "stdout_tail": cp.stdout[-1500:], "stderr_tail": cp.stderr[-1500:]}
    except subprocess.TimeoutExpired as e:
        return {"cmd": args, "returncode": 124, "ok": False, "seconds": round(time.time() - t0, 3),
                "timeout_seconds": timeout, "stdout_tail": (e.stdout or "")[-1500:] if isinstance(e.stdout, str) else "",
                "stderr_tail": (e.stderr or "")[-1500:] if isinstance(e.stderr, str) else "", "error": "TIMEOUT_EXPIRED"}


def _sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


# ───────────────────────── selftest (offline) ─────────────────────────
def selftest() -> int:
    try:
        ts = _imp("tl_selftest"); ts.bind(sys.modules[__name__])
    except Exception as e:  # noqa: BLE001 — tl_selftest hỏng do mount → báo, không crash câm
        print(f"[tl] selftest: không nạp được tl_selftest.py ({type(e).__name__}: {e})", file=sys.stderr)
        return 1
    return ts.run()


# ───────────────────────── argparse ─────────────────────────
def _optional_bool_flag(v):
    """v1.29.6 (log 118 Luật — P2.3): cờ boolean NHẬN CẢ dạng có giá trị. `--corpus` (trần) = True; `--corpus true` /
    `--corpus false` cũng hợp lệ (trước đây store_true trần → '--corpus true' nổ rc=2 usage-error khó hiểu)."""
    s = str(v).strip().lower()
    if s in ("true", "1", "yes", "y"):
        return True
    if s in ("false", "0", "no", "n"):
        return False
    raise argparse.ArgumentTypeError(f"giá trị boolean không hợp lệ: {v!r} (dùng true/false, hoặc cờ trần)")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="tl", description="CLI hợp nhất tra-luat (webapp target 2.21.2i)")
    # F (v1.33.6 — log rà: `tl --version` in usage-error thay vì version): flag chuẩn, nguồn = hằng VERSION.
    ap.add_argument("--version", action="version",
                    version=f"tl {VERSION} (webapp target {globals().get('EXPECT_VERSION', '2.21.2i')})")
    ap.add_argument("--config", help="file JSON webappUrl/token")
    ap.add_argument("--profile", help="corpus profile trong config v2: vbqppl, vbthuong, hoặc profile dự án")
    ap.add_argument("--timings", action="store_true", help="in thời gian từng call webapp ra stderr (=env TL_TIMINGS=1)")
    ap.add_argument("--deterministic", action="store_true", help="chuẩn hoá JSON output: sort keys + scrub path/temp/time volatile (=env TL_DETERMINISTIC=1)")
    ap.add_argument("--selftest", action="store_true", help="logic thuần, không mạng")
    sub = ap.add_subparsers(dest="cmd")
    try:
        tlg = _imp("tl_gws"); tlg.bind(sys.modules[__name__])
    except Exception as _e:   # noqa: BLE001 — tl_gws.py bị mount CẮT CỤT/NUL → KHÔNG để chết cả CLI.
        # Lệnh LÕI (footnote-map/cluster/rasoat-chongcheo/locate…) dùng hàm trong tl.py nên VẪN chạy; chỉ lệnh
        # gws/bootstrap/nlm/secrets (dùng tlg.*) báo lỗi rõ + cách khắc phục, thay vì SyntaxError sập toàn bộ.
        _tlg_err = (f"tl_gws.py không nạp được ({type(_e).__name__}: {_e}) — file bị mount cắt cụt/NUL? "
                    "Re-sync skill, HOẶC mirror scripts/ sang thư mục ghi được + strip NUL rồi chạy lại.")
        def _tlg_stub(_a, _m=_tlg_err):
            print(f"[tl] {_m}", file=sys.stderr); return 3
        class _TlgStub:
            def __getattr__(self, _n):
                return _tlg_stub
        tlg = _TlgStub()
        print(f"[tl] ⚠ {_tlg_err} (lệnh rà soát lõi vẫn chạy)", file=sys.stderr)

    p = sub.add_parser("gws-ping", help="GĐ0: cổng boot transport gws (PATH+pin version+auth), env-aware; Chat SKIP")
    p.add_argument("--env", choices=["code", "cowork", "chat"], help="ép runtime env (mặc định tự dò)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=tlg.cmd_gws_ping)
    p = sub.add_parser("download", help="Tải file Drive → đĩa (gws raw-fast cho binary, tự fallback GAS cho text/JSON raw)")
    p.add_argument("--file-id", dest="file_id", required=True)
    p.add_argument("--out", help="đường dẫn lưu (mặc định <fileId>.bin)")
    p.add_argument("--export-mime", dest="export_mime", help="MIME export cho Google-native (vd application/pdf)")
    p.add_argument("--env", choices=["code", "cowork", "chat"], help="ép runtime env")
    p.set_defaults(fn=tlg.cmd_download)
    p = sub.add_parser("gws-bootstrap-cowork", help="Cài gws BINARY MUSL-STATIC (public-curl Drive→chmod→PATH) + nạp cred. Cowork PHẢI dùng lệnh này — KHÔNG `npm i -g @googleworkspace/cli` (bản GNU cần GLIBC 2.39, Cowork glibc 2.35 → không chạy)")
    p.add_argument("--file-id", dest="file_id", help="fileId binary gws trên Drive (mặc định bản musl đã stage)")
    p.add_argument("--local-tgz", dest="local_tgz", help="dùng gws.tgz CÓ SẴN local (tl_fetch.sh giải nén từ bundle) → KHỎI tải Drive (md5 vẫn verify)")
    p.add_argument("--md5", help="md5 kỳ vọng (mặc định theo bản stage)")
    p.add_argument("--bindir", help="thư mục đặt gws (mặc định ~/.local/bin)")
    p.add_argument("--cred-file-id", dest="cred_file_id", help="fileId cred mã hoá (mặc định GWS_CRED_FILEID)")
    p.add_argument("--no-auth", dest="no_auth", action="store_true", help="chỉ cài binary, KHÔNG tự nạp credential")
    p.add_argument("--force", action="store_true", help="ép tải lại binary kể cả khi gws đã có trên PATH (mặc định: gws có sẵn → chỉ nạp cred)")
    p.set_defaults(fn=tlg.cmd_gws_bootstrap_cowork)
    p = sub.add_parser("drive-push", help="[máy có gws auth] cập nhật NỘI DUNG file Drive (GIỮ fileId) = zip/bundle local, qua gws — đẩy bản ship mới mà KHÔNG đổi fileId")
    p.add_argument("path", help="đường dẫn zip/bundle local cần đẩy lên Drive")
    p.add_argument("--file-id", dest="file_id", help="fileId đích (mặc định SKILL_FILEID = file zip skill/bundle)")
    p.add_argument("--name", help="đổi tên file Drive thành tên này (GIỮ fileId)")
    p.add_argument("--rename-to-file", dest="rename_to_file", action="store_true", help="đổi tên file Drive theo TÊN FILE upload (basename, GIỮ fileId)")
    p.add_argument("--force", action="store_true",
                   help="(v1.33.59 ADR-0001) bỏ qua guard BUNDLE_META.json — chỉ khi CHẮC cây này là canonical")
    p.add_argument("--via", choices=["auto", "gws", "gcloud"], default="auto",
                   help="(v1.33.49) đường upload: auto = gws trước, chết → FALLBACK gcloud (cần `gcloud auth login "
                        "--enable-gdrive-access` 1 lần; OAuth production — né hạn-7-ngày Testing của gws)")
    p.set_defaults(fn=tlg.cmd_drive_push)
    p = sub.add_parser("bootstrap", help="ENV-AWARE: giải mã bundle (TL_MASTER_KEY) → nạp GAS token + gws (Code/Cowork)")
    p.add_argument("--secrets-id", dest="secrets_id", help="fileId tl_secrets.enc (mặc định SECRETS_FILEID)")
    p.add_argument("--secrets-file", dest="secrets_file", help="đường dẫn .enc đã tải sẵn (Cowork: agent tải qua MCP)")
    p.add_argument("--bindir", help="thư mục đặt gws (mặc định ~/.local/bin)")
    p.add_argument("--no-gws", dest="no_gws", action="store_true", help="chỉ nạp GAS token, bỏ qua gws")
    p.add_argument("--no-nlm", dest="no_nlm", action="store_true", help="bỏ qua pip install nlm (notebooklm-mcp-cli)")
    p.add_argument("--env", choices=["code", "cowork", "chat"], help="ép runtime env")
    p.set_defaults(fn=tlg.cmd_bootstrap)
    p = sub.add_parser("nlm-install", help="Cài nlm: mặc định tải Python 3.11 từ Drive (Cowork CHẶN astral). `--uv`: egress mở → uv tự cài Python 3.11 (dùng python hệ thống nếu đã ≥3.11) → KHÔNG tải 31MB từ Drive. ★Cowork 45s/lệnh: LẶP `--resume` tới rc=0 (mỗi lần 1 bước fetch→extract→install; rc=3=PARTIAL còn bước)")
    p.add_argument("--py-file-id", dest="py_file_id", help="fileId tarball Python 3.11 (mặc định PY311_FILEID)")
    p.add_argument("--uv", action="store_true", help="ƯU TIÊN uv (cài uv → uv python install 3.11 nếu hệ thống <3.11; egress mở) thay vì tải Drive; tự fallback Drive khi uv lỗi")
    p.add_argument("--resume", action="store_true",
                   help="(v1.30.1 #1) chạy ĐÚNG 1 bước kế tiếp rồi thoát (trạng thái dò từ đĩa, idempotent) — "
                        "cho env giới hạn 45s/lệnh (Cowork): lặp lại CÙNG lệnh tới rc=0; rc=3=PARTIAL")
    p.add_argument("--version", help="pin phiên bản notebooklm-mcp-cli (mặc định mới nhất)")
    p.add_argument("--env", choices=["code", "cowork", "chat"], help="ép runtime env")
    p.set_defaults(fn=tlg.cmd_nlm_install)
    p = sub.add_parser("overlap", help="E1+ SO QUY PHẠM: trích nguyên văn Điều bị sửa (VBHN) + cờ PENDING/đa-luật-sửa; --with-source thêm điều luật sửa")
    p.add_argument("target", nargs="?", help="gdocId | số hiệu VBHN canonical")
    p.add_argument("--text-file", dest="text_file", help="đọc canonical từ file thay vì Drive")
    p.add_argument("--with-source", dest="with_source", action="store_true", help="trích thêm điều của luật sửa (online, từ corpus)")
    p.add_argument("--refresh", action="store_true", help="refresh manifest")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=tlg.cmd_overlap)
    p = sub.add_parser("nlm-auth-pull", help="[COWORK] kéo cookie nlm mới nhất từ bundle → ~/.notebooklm-mcp-cli (refresh giữa phiên)")
    p.add_argument("--secrets-id", dest="secrets_id", help="fileId bundle (mặc định SECRETS_FILEID)")
    p.add_argument("--secrets-file", dest="secrets_file", help="dùng .enc local (project file) thay vì tải")
    p.add_argument("--env", choices=["code", "cowork", "chat"], help="ép runtime env")
    p.set_defaults(fn=tlg.cmd_nlm_auth_pull)
    p = sub.add_parser("secrets-stage", help="[CODE] gói {webappUrl,token GAS,gws_cred,nlm_auth} → mã hoá (TL_MASTER_KEY) → upload Drive")
    p.add_argument("--folder", help="folderId đích (mặc định _HOP_NAP)")
    p.add_argument("--secrets-id", dest="secrets_id", help="ghi đè bundle có sẵn (giữ fileId) thay vì tạo mới")
    p.add_argument("--no-gws", dest="no_gws", action="store_true", help="không gói gws_cred")
    p.add_argument("--no-nlm", dest="no_nlm", action="store_true", help="không gói nlm_auth (cookies NotebookLM)")
    p.set_defaults(fn=tlg.cmd_secrets_stage)
    p = sub.add_parser("secrets-set", help="[CODE] xoay vòng secret trong bundle: --gas-token/--webapp/--gws (ghi đè tại chỗ)")
    p.add_argument("--gas-token", dest="gas_token", help="token webapp GAS mới")
    p.add_argument("--webapp", help="webappUrl mới")
    p.add_argument("--gws", action="store_true", help="re-export gws cred hiện tại vào bundle")
    p.add_argument("--nlm", action="store_true", help="refresh cookie NotebookLM (nlm_auth) vào bundle — định kỳ ~2–4 tuần")
    p.add_argument("--no-public", dest="no_public", action="store_true",
                   help="(v1.33.1) KHÔNG đồng bộ file public .enc — mặc định --gws/--nlm ghi đè luôn GWS_CRED_FILEID/NLM_CRED_FILEID tại chỗ để CẢ 2 đường cùng tươi")
    p.add_argument("--secrets-id", dest="secrets_id", help="fileId bundle (mặc định SECRETS_FILEID)")
    p.add_argument("--secrets-file", dest="secrets_file", help="dùng .enc local thay vì tải")
    p.add_argument("--folder", help="folderId (khi cần tạo lại)")
    p.set_defaults(fn=tlg.cmd_secrets_set)
    p = sub.add_parser("gws-auth-stage", help="[CODE] export gws cred → mã hoá (khoá=webapp token) → v1.33.1: GHI ĐÈ TẠI CHỖ GWS_CRED_FILEID (fileId giữ nguyên, không bake lại); --new tạo file mới")
    p.add_argument("--folder", help="folderId đích (mặc định _HOP_NAP; chỉ dùng khi --new)")
    p.add_argument("--cred-file-id", dest="cred_file_id", help="fileId đích ghi đè tại chỗ (mặc định GWS_CRED_FILEID baked)")
    p.add_argument("--new", action="store_true", help="tạo file MỚI thay vì ghi đè tại chỗ (hành vi cũ — nhớ bake fileId in ra)")
    p.set_defaults(fn=tlg.cmd_gws_auth_stage)
    p = sub.add_parser("gws-auth-load", help="[COWORK] tải cred mã hoá từ Drive → giải mã → ~/.config/gws/credentials.json (zero-setup)")
    p.add_argument("--cred-file-id", dest="cred_file_id", help="fileId cred mã hoá (mặc định GWS_CRED_FILEID)")
    p.set_defaults(fn=tlg.cmd_gws_auth_load)
    p = sub.add_parser("nlm-auth-stage", help="[CODE, sau `nlm login`] gói cookie nlm → mã hoá (khoá=webapp token) → v1.33.1: GHI ĐÈ TẠI CHỖ NLM_CRED_FILEID (fileId giữ nguyên); --new tạo file mới")
    p.add_argument("--folder", help="folderId đích (mặc định _HOP_NAP; chỉ dùng khi --new)")
    p.add_argument("--refresh", action="store_true", help="ép nlm tái sinh cookie từ browser profile trước khi gói")
    p.add_argument("--cred-file-id", dest="cred_file_id", help="fileId đích ghi đè tại chỗ (mặc định NLM_CRED_FILEID / env TL_NLM_CRED_FILEID)")
    p.add_argument("--new", action="store_true", help="tạo file MỚI thay vì ghi đè tại chỗ (hành vi cũ — nhớ bake fileId in ra)")
    p.add_argument("--force", action="store_true", help="(v1.33.39) bỏ qua cổng verify-LIVE — ép stage DÙ cookie đang chết (mặc định TỪ CHỐI cookie chết để không kẹt vòng lặp Cowork)")
    p.set_defaults(fn=tlg.cmd_nlm_auth_stage)
    p = sub.add_parser("nlm-auth-load", help="[COWORK] tải nlm cookie mã hoá từ Drive → giải mã (webapp token) → ~/.notebooklm-mcp-cli (HEADLESS, KHÔNG cần master key/`nlm login`)")
    p.add_argument("--cred-file-id", dest="cred_file_id", help="fileId nlm cred mã hoá (mặc định NLM_CRED_FILEID / env TL_NLM_CRED_FILEID)")
    p.set_defaults(fn=tlg.cmd_nlm_auth_load)
    p = sub.add_parser("drive-parity", help="GĐ1 pilot: đối chứng get-meta 1 fileId qua gws vs GAS (+spec MCP), đo ms, test fallback")
    p.add_argument("--file-id", dest="file_id", required=True, help="Drive fileId để get-meta đối chứng")
    p.add_argument("--test-fallback", dest="test_fallback", action="store_true", help="tắt gws (TL_GWS_DISABLE=1) → kiểm [FALLBACK→GAS]")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=tlg.cmd_drive_parity)
    p = sub.add_parser("transport-info", help="GĐ4: in ma trận định tuyến transport (A–E × 3-env) + trạng thái gws")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=tlg.cmd_transport_info)


    p = sub.add_parser("profile-files", help="liệt kê file trong manifest profile (lọc row-kind/NLM/corpus/name)")
    p.add_argument("--profile-name", dest="target_profile", help="profile cần đọc; mặc định global --profile/defaultProfile")
    p.add_argument("--name")
    p.add_argument("--row-kind", dest="row_kind")
    p.add_argument("--nlm", nargs="?", const=True, default=False, type=_optional_bool_flag,
                   help="lọc đã-trên-NLM (cờ trần; nhận cả '--nlm true/false')")
    p.add_argument("--no-nlm", dest="no_nlm", action="store_true")
    p.add_argument("--corpus", nargs="?", const=True, default=False, type=_optional_bool_flag,
                   help="lọc corpus=true (cờ trần; nhận cả '--corpus true/false' — v1.29.6 P2.3)")
    p.add_argument("--no-corpus", dest="no_corpus", action="store_true")
    p.add_argument("--limit", type=int)
    p.add_argument("--refresh", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_profile_files)


    p = sub.add_parser("locate"); p.add_argument("query"); p.add_argument("--max", type=int, default=10)
    p.add_argument("--trust-cache", dest="trust_cache", action="store_true",
                   help="(v1.29.4 #9) TẮT auto-refresh khi cache >900s (mặc định tự refresh — chống báo-động-giả cache lệch)")
    p.add_argument("--refresh", action="store_true", help="tải lại manifest trước khi locate")
    p.add_argument("--debug", action="store_true", help="in lỗi fallback manifest nếu có")
    _add_base_also_flags(p)
    p.set_defaults(fn=cmd_locate)

    p = sub.add_parser("exists", help="kiểm tra hiện diện bằng source-map chuẩn hóa; không overclaim nếu miss")
    p.add_argument("query")
    p.add_argument("--refresh", action="store_true")
    p.add_argument("--json", action="store_true")
    _add_base_also_flags(p)
    p.set_defaults(fn=cmd_exists)

    p = sub.add_parser("source-map", help="lập bản đồ nguồn rà soát theo nguyên tắc VBHN-first")
    p.add_argument("queries", nargs="+")
    p.add_argument("--refresh", action="store_true")
    p.add_argument("--strict", "--fail-on-finding", action="store_true",
                   help="(v1.29.4 #8) rc=1 khi verdict REVIEW/PAUSE (mặc định rc=0: phát-hiện ≠ lỗi lệnh — doctrine rc thống nhất; --fail-on-finding = alias CI)")
    p.add_argument("--json", action="store_true")
    p.add_argument("--out", help="ghi JSON ra file atomically (hữu ích trên Cowork để tránh stdout/heredoc timeout); tự bật JSON")
    _add_base_also_flags(p)
    p.set_defaults(fn=cmd_source_map)


    p = sub.add_parser("instruction-audit", help="kiểm Instruction có ràng buộc skill/QT-3/research discovery-only")
    p.add_argument("--file", help="file Instruction/Project prompt cần kiểm")
    p.add_argument("--generate", action="store_true", help="generate bằng scripts/gen_instructions.py rồi audit")
    p.add_argument("--target", choices=["project", "nlm", "both", "config"], default="both")
    p.add_argument("--skill-version", default=VERSION)
    p.add_argument("--profile", help="profile corpus khi generate để audit (mặc định TL_PROFILE/default)")
    p.add_argument("--notebook", "--notebook-id", dest="notebook", help="notebookId của profile dự án")
    p.add_argument("--folder-name", dest="folder_name", help="tên folder trong Van_ban_thuong")
    p.add_argument("--root-folder-id", dest="root_folder_id", help="rootFolderId nếu đã tạo folder")
    p.add_argument("--print-text", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_instruction_audit)


    # ── WS1/WS2/WS3/WS5 (v1.19.7) ──


    p = sub.add_parser("nlm-reconcile", help="WS1: đối soát registry↔NLM bằng ground-truth CLI; backfill nlm_notebook_id (DRY mặc định)")
    p.add_argument("notebook_id", nargs="?")
    p.add_argument("--apply", action="store_true", help="THỰC THI reg_bulk backfill (mặc định DRY)")
    p.add_argument("--clear-stale", dest="clear_stale", action="store_true", help="clear mapping NLM của dòng KHÔNG có trên NLM")
    p.add_argument("--force-unsafe", dest="force_unsafe", action="store_true", help="(Pha 1) bỏ qua precheck blocker (rủi ro)")
    p.add_argument("--refresh", action="store_true")
    # A5 (v1.33.2 — log rà 111: `nlm-reconcile --json` crash unrecognized arguments trong khi mọi lệnh audit khác
    # đều nhận): output vốn ĐÃ là JSON — nhận cờ cho đồng bộ CLI (no-op), driver batch không phải case riêng.
    p.add_argument("--json", action="store_true", help="chấp nhận cho đồng bộ CLI (output vốn đã JSON)")
    p.add_argument("--out", help="ghi JSON ra file atomically; tự bật JSON")
    p.set_defaults(fn=cmd_nlm_reconcile)


    p = sub.add_parser("nlm-add", help="(1) thêm nguồn NLM qua CLI `nlm source add` (thay MCP source_add) — CLI-first")
    p.add_argument("notebook_id", nargs="?")
    # S8 (v1.33.44 — log 7A: drift doc↔CLI, ghi chú cũ dùng --drive/--wait): --drive = ALIAS của --drive-id;
    # --wait = NO-OP tương thích (mặc định ĐÃ wait; tắt bằng --no-wait) — driver theo doc cũ không gãy usage-error.
    p.add_argument("--drive-id", "--drive", dest="drive_id"); p.add_argument("--url"); p.add_argument("--file")
    p.add_argument("--type", default="doc"); p.add_argument("--title"); p.add_argument("--no-wait", action="store_true")
    p.add_argument("--wait", action="store_true",
                   help="no-op: mặc định ĐÃ wait tới khi nguồn settle; nhận cờ cho tương thích ghi chú cũ (tắt: --no-wait)")
    p.add_argument("--skip-live-check", dest="skip_live_check", action="store_true",
                   help="(v1.29.3) BỎ cổng dedup-live trước add (mặc định DỪNG nếu nguồn đã LIVE / không liệt kê được)")
    p.set_defaults(fn=cmd_nlm_add)

    p = sub.add_parser("nlm-cross", help="cross-shard query qua CLI `nlm cross query` (thay MCP cross_notebook_query)")
    p.add_argument("--json", action="store_true", help="(no-op v1.33.56 — output vốn đã JSON/verbatim; nhận để tương thích workflow cards)")
    p.add_argument("query")
    p.add_argument("--notebooks", help="csv id/tên shard (mặc định: base+overflow VBQPPL trong config)")
    p.add_argument("--all", action="store_true", help="query MỌI notebook (rate-limit)")
    _add_base_also_flags(p)
    p.set_defaults(fn=cmd_nlm_cross)

    p = sub.add_parser("nlm-get", help="số nguồn vật lý + chi tiết notebook qua CLI `nlm notebook get` (thay MCP notebook_get; slot/preflight)")
    p.add_argument("notebook_id", nargs="?")
    # A1 (v1.33.18 — log rà 67: `nlm-get <nb> --json` chết `unrecognized arguments` dù lệnh VỐN luôn xuất JSON
    # → driver quen thêm --json đồng nhất cho nhóm read-only bị gãy riêng lệnh này): nhận làm NO-OP.
    p.add_argument("--json", action="store_true", help="no-op: lệnh luôn xuất JSON; nhận cờ để driver thêm --json đồng nhất không gãy")
    p.add_argument("--out", help="ghi JSON ra file atomically; tự bật JSON")
    p.set_defaults(fn=cmd_nlm_get)


    p = sub.add_parser("ingest-local", help="(2)+(3) ingest 1 file local → upload→organize→preflight→nlm add (CLI)→push (DRY mặc định, --apply để chạy; timeout giữa chừng → chạy lại CÙNG LỆNH + --resume)")
    p.add_argument("--json", action="store_true", help="(no-op v1.33.56 — output vốn đã JSON/verbatim; nhận để tương thích workflow cards)")
    p.add_argument("file")
    p.add_argument("--name"); p.add_argument("--sohieu"); p.add_argument("--cat"); p.add_argument("--goc")
    p.add_argument("--hieuluc"); p.add_argument("--loai"); p.add_argument("--apply", action="store_true")
    p.add_argument("--resume", action="store_true",
                   help="(N6 v1.33.42) NỐI TIẾP tất định sau timeout/đứt giữa chừng: đọc journal run trước cho CÙNG file "
                        "→ skip bước đã xong (tái dùng fileId/gdoc/source_id), nguồn NLM đã live → LINK thay vì abort. "
                        "Cowork 45s: lặp CÙNG LỆNH + --resume tới rc=0 (mirror nlm-install --resume)")
    p.add_argument("--auto-plan", "--auto", dest="auto_plan", action="store_true",
                   help="đọc file/text local để suy tên chuẩn, số hiệu, loại, cat trước khi upload")
    p.add_argument("--text-file", dest="text_file", help="text đã OCR/extract cho PDF/DOCX để auto-plan và verify cat")
    p.add_argument("--source-quality", choices=["auto", "digital", "ocr"], default="auto",
                   help="gắn cảnh báo OCR trong auto-plan")
    p.add_argument("--ocr-verified", dest="ocr_verified", action="store_true",
                   help="xác nhận OCR đã đối chiếu; chỉ ghi vào auto-plan/cảnh báo")
    p.add_argument("--force-cat", dest="force_cat", action="store_true",
                   help="cho phép apply cat auto từ tên file/low-confidence khi đã kiểm tra tay")
    p.add_argument("--allow-large", dest="allow_large", action="store_true", help="nạp NGUYÊN file lớn (bỏ cổng HỎI tách; chấp nhận giảm chất lượng RAG)")
    p.add_argument("--large-threshold", dest="large_threshold", type=int, help=f"ngưỡng byte coi là 'lớn' (mặc định {NLM_LARGE_SRC_BYTES})")
    p.add_argument("--skip-nlm-preflight", dest="skip_nlm_preflight", action="store_true",
                   help="(v1.29.7) BỎ kiểm NLM sẵn-sàng trước upload (mặc định DỪNG sớm nếu NLM chưa cài/auth — tránh chuỗi dở dang)")
    p.add_argument("--skip-live-check", dest="skip_live_check", action="store_true",
                   help="(v1.29.3) BỎ cổng dedup-live trước nlm add (mặc định DỪNG nếu title đã LIVE / không liệt kê được)")
    p.set_defaults(fn=cmd_ingest_local)


    p = sub.add_parser("reg-query", help="truy vấn registry/manifest OFFLINE (đọc CACHE) + lọc (name/sohieu/cat/loai/nlm/row-kind/corpus/mime). E2: SAU khi ghi sheet (reg_upsert/ingest/backfill) phải `--refresh` để thấy thay đổi LIVE, nếu không sẽ đọc cache CŨ (vd nlm rỗng dù sheet đã ghi).")
    p.add_argument("--name"); p.add_argument("--sohieu"); p.add_argument("--cat")
    p.add_argument("--loai", help="(v1.33.6) lọc theo LOẠI văn bản, so CHUẨN HOÁ enum ('Luật' khớp cả 'Luat'/'luật'; 'Bộ luật' riêng) — trước đây phải lọc tay theo tiền tố tên")
    p.add_argument("--nlm", nargs="?", const=True, default=False, type=_optional_bool_flag,
                   help="lọc đã-trên-NLM (cờ trần; nhận cả '--nlm true/false')")
    p.add_argument("--no-nlm", dest="no_nlm", action="store_true")
    p.add_argument("--corpus", nargs="?", const=True, default=False, type=_optional_bool_flag,
                   help="lọc corpus=true (cờ trần; nhận cả '--corpus true/false' — v1.29.6 P2.3)")
    p.add_argument("--no-corpus", dest="no_corpus", action="store_true")
    p.add_argument("--row-kind", dest="row_kind"); p.add_argument("--mime"); p.add_argument("--limit", type=int)
    p.add_argument("--drive-id", dest="drive_id",
                   help="(v1.34.2) lọc ĐÚNG 1 file theo drive_id/gdoc_id — readback chuẩn của các idempotency contract (Pha H bắt drift: contract dặn `reg-query --drive-id` mà parser thiếu cờ)")
    p.add_argument("--refresh", action="store_true", help="tải LẠI manifest/registry LIVE trước khi lọc (dùng sau khi vừa ghi sheet)"); p.add_argument("--json", action="store_true")
    p.add_argument("--out", help="(S-4 v1.33.34) ghi JSON envelope ra file atomically; tự bật JSON (né stdout/heredoc timeout Cowork)")
    _add_base_also_flags(p)
    p.set_defaults(fn=cmd_reg_query)


    # v1.33.58 (Pha E - E2): 8 lệnh determinism sinh parser từ tl_core.command_registry
    # (GENERATED_SPECS giữ NGUYÊN VĂN flags/help; handler = stub tl; --profile/--config/--deterministic
    # do vòng inject cuối build_parser phủ như mọi subparser khác).
    _tl_registry.register_generated(sub, sys.modules[__name__])


    p = sub.add_parser("instructions", help="sinh Instruction/Project prompt; mặc định VBQPPL, --profile <tên> cho dự án văn bản thường")
    p.add_argument("--target", choices=["nlm", "project", "both", "config", "style-template"], default="both")
    p.add_argument("--skill-version", default=VERSION)
    p.add_argument("--notebook", "--notebook-id", dest="notebook", help="notebookId của profile dự án (văn bản thường)")
    p.add_argument("--folder-name", dest="folder_name", help="tên folder trong Van_ban_thuong (mặc định = tên profile)")
    p.add_argument("--root-folder-id", dest="root_folder_id", help="rootFolderId nếu đã tạo folder")
    p.add_argument("--check", action="store_true", help="chỉ kiểm output có đủ block bắt buộc")
    p.add_argument("--out", help="III.3: ghi Instruction ra FILE (UTF-8) thay vì in stdout (khỏi gọi thẳng gen_instructions.py)")
    p.set_defaults(fn=cmd_instructions)


    p = sub.add_parser("profile-ingest", help="profile own-scope: upload→GDoc canonical flat→verify draft/OCR→registry→NLM chunks (DRY mặc định)")
    p.add_argument("file")
    p.add_argument("--text-file", dest="text_file", help="file text đã OCR/extract để verify và lập split plan trước khi upload")
    p.add_argument("--name", help="tên canonical GDoc (mặc định suy từ header)")
    p.add_argument("--source-quality", choices=["auto", "digital", "ocr"], default="auto")
    p.add_argument("--ocr-verified", dest="ocr_verified", action="store_true", help="xác nhận OCR đã đối chiếu đủ để cho corpus/NLM")
    p.add_argument("--hieuluc", help="trạng thái hiệu lực nếu không phải dự thảo")
    p.add_argument("--large-threshold", dest="large_threshold", type=int, help=f"ngưỡng byte lập split plan (mặc định {NLM_LARGE_SRC_BYTES})")
    p.add_argument("--chunk-max-chars", dest="chunk_max_chars", type=int, default=100000, help="kích thước chunk text tối đa cho NLM")
    p.add_argument("--allow-default", dest="allow_default", action="store_true", help="cho phép chạy trên profile vbqppl (mặc định chặn)")
    p.add_argument("--apply", action="store_true")
    p.add_argument("--skip-live-check", dest="skip_live_check", action="store_true",
                   help="(v1.29.3) BỎ cổng dedup-live trước nlm add (mặc định DỪNG nếu title đã LIVE / không liệt kê được)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_profile_ingest)

    p = sub.add_parser("profile-file-add", help="alias rõ nghĩa của profile-ingest: thêm file local vào profile + NLM")
    p.add_argument("file")
    p.add_argument("--text-file", dest="text_file", help="file text đã OCR/extract để verify và lập split plan trước khi upload")
    p.add_argument("--name", help="tên canonical GDoc (mặc định suy từ header)")
    p.add_argument("--source-quality", choices=["auto", "digital", "ocr"], default="auto")
    p.add_argument("--ocr-verified", dest="ocr_verified", action="store_true", help="xác nhận OCR đã đối chiếu đủ để cho corpus/NLM")
    p.add_argument("--hieuluc", help="trạng thái hiệu lực nếu không phải dự thảo")
    p.add_argument("--large-threshold", dest="large_threshold", type=int, help=f"ngưỡng byte lập split plan (mặc định {NLM_LARGE_SRC_BYTES})")
    p.add_argument("--chunk-max-chars", dest="chunk_max_chars", type=int, default=100000, help="kích thước chunk text tối đa cho NLM")
    p.add_argument("--allow-default", dest="allow_default", action="store_true", help="cho phép chạy trên profile vbqppl (mặc định chặn)")
    p.add_argument("--apply", action="store_true")
    p.add_argument("--skip-live-check", dest="skip_live_check", action="store_true",
                   help="(v1.29.3) BỎ cổng dedup-live trước nlm add (mặc định DỪNG nếu title đã LIVE / không liệt kê được)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_profile_file_add)


    p = sub.add_parser("register")
    p.add_argument("--drive-id", dest="drive_id"); p.add_argument("--bulk"); p.add_argument("--cols")
    p.add_argument("--force-insert", dest="force_insert", action="store_true",
                   help="(P0-1 v1.33.12) bỏ qua kiểm drive_id tồn tại (manifest/Drive) — CỐ Ý tạo dòng mới không gắn Drive; mặc định id lạ bị CHẶN vì reg_upsert insert-if-absent sẽ chèn dòng rác")
    for k in ("sohieu", "loai", "name", "cat", "linhvuc", "goc", "hieuluc", "sua_doi",
              "nlm_source_id", "nlm_notebook_id", "nlm_status", "nlm_title", "tukhoa", "corpus", "title_vn"):
        p.add_argument("--" + k.replace("_", "-"), dest=k)   # Group C2: +--nlm-notebook-id (khỏi backfill-notebook riêng)
    # v1.29.7 (log NĐ131 #7): cho SỬA row_kind qua CLI có kiểm soát (trước không có đường nào — dòng bị gán nhầm
    # overflow bởi bug #6 không sửa được). choices chặn giá trị lạ.
    p.add_argument("--row-kind", dest="row_kind", choices=["own", "overflow", "ref"],
                   help="(v1.29.7) sửa row_kind (own/overflow/ref) — vd chữa dòng bị gán nhầm overflow")
    p.add_argument("--force-unsafe", dest="force_unsafe", action="store_true", help="(v1.29.2) BỎ QUA precheck blocker — RỦI RO, tự chịu")
    # N3 (v1.33.41 — log rà: agent quen tay `register … --apply` bị usage-error rc=2 giữa loop): register GHI
    # TRỰC TIẾP by-design (journaled+verified, không DRY) — nhận cờ --apply làm NO-OP để không vỡ muscle-memory.
    p.add_argument("--apply", action="store_true", help="(no-op compat) register luôn ghi trực tiếp — cờ này chỉ để khỏi vỡ script/agent-loop quen các lệnh DRY-mặc-định")
    p.set_defaults(fn=cmd_register)


    p = sub.add_parser("hygiene", help="registry hygiene: duplicate/orphan/quarantine plan")
    hsub = p.add_subparsers(dest="hsub")
    hp = hsub.add_parser("scan"); hp.add_argument("--refresh", action="store_true"); hp.add_argument("--json", action="store_true"); hp.set_defaults(fn=cmd_hygiene)
    hp = hsub.add_parser("plan"); hp.add_argument("query"); hp.add_argument("--refresh", action="store_true"); hp.add_argument("--json", action="store_true")
    hp.add_argument("--apply", action="store_true"); hp.add_argument("--confirm"); hp.add_argument("--to-cat", dest="to_cat"); hp.set_defaults(fn=cmd_hygiene)
    hp = hsub.add_parser("query"); hp.add_argument("query"); hp.add_argument("--refresh", action="store_true"); hp.add_argument("--json", action="store_true")
    hp.set_defaults(fn=cmd_hygiene)
    hp = hsub.add_parser("reconcile", help="global reconcile theo số hiệu parse từ tên hoặc md5")
    hp.add_argument("query", nargs="?"); hp.add_argument("--refresh", action="store_true"); hp.add_argument("--json", action="store_true")
    hp.add_argument("--apply", action="store_true"); hp.add_argument("--confirm"); hp.add_argument("--to-cat", dest="to_cat"); hp.set_defaults(fn=cmd_hygiene)

    p = sub.add_parser("reconcile", help="alias: hygiene reconcile")
    p.add_argument("query", nargs="?"); p.add_argument("--refresh", action="store_true"); p.add_argument("--json", action="store_true")
    p.add_argument("--apply", action="store_true"); p.add_argument("--confirm"); p.add_argument("--to-cat", dest="to_cat"); p.set_defaults(fn=cmd_hygiene, hsub="reconcile")


    p = sub.add_parser("rasoat")
    p.add_argument("sub", help="keywords|titles|worksheet|phuluc|orchestrate")
    p.add_argument("rest", nargs=argparse.REMAINDER); p.set_defaults(fn=cmd_rasoat)
    p = sub.add_parser("cache-build", help="B2: dựng cache cấu trúc docs/<sh>--consolidated.json (wrapper ingest_to_cache.py) cho `rasoat worksheet`; chain --gdoc-id/--input, tự nạp config")
    p.add_argument("sohieu", nargs="?", help="số hiệu canonical (vd 19/VBHN-VPQH)")
    p.add_argument("rest", nargs=argparse.REMAINDER, help="cờ chuyển thẳng cho ingest_to_cache.py: --gdoc-id/--input/--goc/--method/--nlm-source-id/--vbhn-first…")
    p.set_defaults(fn=cmd_cache_build)
    # v1.33.48 (rà Instruction 'Luật BHXH' — dặn 'MỌI lệnh truyền --profile' nhưng flag chỉ ở ROOT parser →
    # `tl reg-query --profile "Luật BHXH"` gãy `unrecognized arguments` rc=2; agent phải nhớ đặt TRƯỚC subcommand):
    # nhận --profile/--config Ở CẢ SAU subcommand — thêm vào từng subparser CHƯA có (subparser đã tự khai thì giữ).
    # ⚠ PHẢI default=SUPPRESS: Python mới parse subcommand vào NAMESPACE CON rồi copy-đè lên namespace gốc —
    # default None của cờ injected sẽ ĐÈ MẤT giá trị `tl --profile X <cmd>` đặt trước subcommand (bắt được bằng
    # smoke ngay khi viết). SUPPRESS = không truyền thì không set attr → giá trị root sống; truyền sau → thắng.
    def _walk_subparsers(_root):
        # v1.33.56 (review P4-04): đệ quy nested subparsers (hygiene có cấp con) — vòng cũ chỉ quét top-level.
        out = list(_root.choices.values())
        for _p in _root.choices.values():
            for _act0 in _p._actions:
                if isinstance(_act0, argparse._SubParsersAction):
                    out.extend(_walk_subparsers(_act0))
        return out
    for _sp in _walk_subparsers(sub):
        _opts = {o for _act in _sp._actions for o in _act.option_strings}
        if "--profile" not in _opts:
            _sp.add_argument("--profile", default=argparse.SUPPRESS, help="corpus profile (nhận cả trước lẫn sau subcommand)")
        if "--config" not in _opts:
            _sp.add_argument("--config", default=argparse.SUPPRESS, help="file JSON webappUrl/token (nhận cả sau subcommand)")
        if "--deterministic" not in _opts:
            _sp.add_argument("--deterministic", action="store_true", default=argparse.SUPPRESS,
                             help="chuẩn hoá JSON output (nhận cả sau subcommand)")
    return ap


# Lệnh TỰ LO creds (chạy được khi THIẾU webapp/token) → KHÔNG gọi load_creds tự động.
# Tách hằng nhiều dòng: KHÔNG để 1 dòng >800 ký tự (vài trình nạp skill cắt cụt file ở dòng quá dài).
# gws-ping/transport-info = chẩn đoán transport gws, KHÔNG cần webapp creds.
_CREDS_LAZY_CMDS = frozenset({
    "boot", "locate", "exists", "source-map", "relation-check", "relation-backfill", "external-ingest",
    "instructions", "instruction-audit", "tool-inventory", "route-task", "workflow-audit", "determinism-audit", "golden-test", "release-check", "release-manifest", "release-verify", "release-bundle", "live-readiness", "live-contract-check", "live-state-snapshot", "live-state-diff", "live-smoke-plan", "deploy-plan", "rollback-plan", "final-acceptance", "go-live-runbook", "link-priority", "profile-info", "config-pin-registry", "profile-list", "profile-use",
    "profile-rename", "profile-delete", "profile-files", "profile-manifest", "profile-create", "profile-ingest",
    "profile-file-add", "profile-file-remove", "ingest-ocr", "profile-ingest-ocr", "ingest-zip", "profile-ingest-zip", "profile-ingest-chunks", "ocr-analyze", "ocr-run", "ocr-verify", "chunk-plan", "chunk-apply", "chunk-verify",
    "slot-audit", "vbhn-check", "vbhn-verify", "vbhn-compare", "vbhn-normalize", "rasoat",
    "doctor", "cowork-plan", "ops-plan", "init-config", "hygiene", "reconcile", "registry-doctor", "xref", "dedup-check",
    "ingest-route", "backfill-notebook", "cache-snapshot", "nlm-list", "nlm-reconcile", "nlm-query-plan",
    "preflight", "push-overflow", "nlm-content", "nlm-query", "reg-delete", "bench", "tvpl-url",
    "fetch-route", "fetch-batch", "fetch-links", "find-doc", "footnote-map", "cluster",
    "rasoat-chongcheo", "frontier-expand", "rasoat-loop", "ingest-missing", "overflow-resolve", "nlm-orphans", "nlm-add", "ingest-local", "nlm-cross", "nlm-get", "cat-list",
    "reg-query", "cat-audit", "cat-verify", "source-verify", "backfill-loai", "backfill-hieuluc", "missing-sohieu", "vbhn-year-fix", "sweep", "quarantine-fix", "dedup-plan", "gws-ping", "transport-info", "bootstrap", "cache-build",
    "nlm-install", "nlm-auth-pull", "nlm-auth-stage", "nlm-auth-load", "overlap", "verify-integrity", "edit-skill", "drive-push",   # tự lo cred (--secrets-file / direct-media / _read_doc_text)
    "up",   # tl up TỰ bootstrap cred (init-config --from-public) → KHÔNG để main() sys.exit khi phiên trống; cmd_up tự gọi load_creds
})


def main(argv) -> int:
    ap = build_parser()
    a = ap.parse_args(argv)
    global _TIMING_ON, _DETERMINISTIC_ON
    if getattr(a, "timings", False):
        _TIMING_ON = True
        os.environ["TL_TIMINGS"] = "1"   # cho subprocess (boot) thừa hưởng
    if _deterministic_enabled(a):
        _DETERMINISTIC_ON = True
        os.environ["TL_DETERMINISTIC"] = "1"
        os.environ.setdefault("TZ", "UTC")
        os.environ.setdefault("PYTHONHASHSEED", "0")   # child processes inherit; current process hash seed is already fixed/decided.
    if a.selftest:
        return selftest()
    if not getattr(a, "cmd", None):
        ap.print_help(); return 1
    if a.cmd not in _CREDS_LAZY_CMDS:   # ngoài nhóm này → nạp creds webapp (cần token)
        load_creds(a.config, getattr(a, "profile", None))
    # (v1.33.29 — log rà v1.33.28 báo 'sweep/review-queue --json rc=1 dù chạy OK' KHÔNG tái hiện được trên
    # canonical [cả 2 return 0 vô điều kiện]; triệu chứng khớp `--json | head/jq-thoát-sớm` → BrokenPipeError
    # exit 1 + traceback noise): consumer đóng pipe sớm là chuyện của CONSUMER — nuốt, rc=0. Driver muốn
    # payload trọn dùng `--out <file>` (atomic, có sẵn trên mọi lệnh JSON nặng từ v1.33.26/28).
    if getattr(a, "fn", None) is None:   # v1.33.56 (P4-05): parser cha thiếu subcommand con → help sạch
        ap.parse_args([a.cmd, "--help"]) if getattr(a, "cmd", None) else ap.print_help()
        return 2
    try:
        return a.fn(a)
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:  # noqa: BLE001
            pass
        return 0


# ───────────────────────── Pha C (v1.33.56): tl_core.workflow/release/live ─────────────────────────
# Nạp SAU khi mọi symbol tl đã định nghĩa; stub định nghĩa TRƯỚC bind để bind copy stub cho tham chiếu chéo.
_tl_workflow = _tl_core_import("workflow")   # noqa: E402 — v1.33.56: qua helper cứu hộ (tl_core/F3)
_tl_release = _tl_core_import("release")      # noqa: E402
_tl_live = _tl_core_import("live")            # noqa: E402
_tl_hygiene = _tl_core_import("hygiene")     # noqa: E402 — I1 v1.34.3
_tl_nlm_ops = _tl_core_import("nlm_ops")    # noqa: E402 — I2 v1.34.4
_tl_extract_cache = _tl_core_import("extract_cache")   # noqa: E402 — I3 v1.34.5
_tl_fetch_web = _tl_core_import("fetch_web")            # noqa: E402 — I3 v1.34.5
_tl_profile_mgmt = _tl_core_import("profile_mgmt")      # noqa: E402 — I4 v1.34.7
_tl_ingest_ops = _tl_core_import("ingest_ops")          # noqa: E402 — I5 v1.34.8
_tl_lookup_ops = _tl_core_import("lookup_ops")     # noqa: E402 — I6 v1.34.9
_tl_ops_misc = _tl_core_import("ops_misc")        # noqa: E402 — I8 v1.34.12
_tl_classify = _tl_core_import("classify")        # noqa: E402 — I9a v1.34.13
_tl_profile_env = _tl_core_import("profile_env")  # noqa: E402 — I9a v1.34.13
_tl_zip_ingest = _tl_core_import("zip_ingest")   # noqa: E402 — Pha D (v1.33.57)
_tl_ocr = _tl_core_import("ocr")                 # noqa: E402
_tl_chunking = _tl_core_import("chunking")       # noqa: E402
_tl_registry = _tl_core_import("command_registry")   # noqa: E402 - Pha E (module thuần, không bind)

def _chunk_plan_from_text(*_a, **_kw):
    return _tl_chunking._chunk_plan_from_text(*_a, **_kw)


def _chunk_records_from_text(*_a, **_kw):
    return _tl_chunking._chunk_records_from_text(*_a, **_kw)


def _load_ocr_manifest_for_text(*_a, **_kw):
    return _tl_ocr._load_ocr_manifest_for_text(*_a, **_kw)


def _ocr_manifest_path_for_text(*_a, **_kw):
    return _tl_ocr._ocr_manifest_path_for_text(*_a, **_kw)


def _ocr_out_paths(*_a, **_kw):
    return _tl_ocr._ocr_out_paths(*_a, **_kw)


def _safe_extract_zip_for_ingest(*_a, **_kw):
    return _tl_zip_ingest._safe_extract_zip_for_ingest(*_a, **_kw)


def _zip_is_safe_member(*_a, **_kw):
    return _tl_zip_ingest._zip_is_safe_member(*_a, **_kw)


def _zip_normalized_member_path(*_a, **_kw):
    return _tl_zip_ingest._zip_normalized_member_path(*_a, **_kw)


def _zip_plan(*_a, **_kw):
    return _tl_zip_ingest._zip_plan(*_a, **_kw)


def _zip_sorted_infos(*_a, **_kw):
    return _tl_zip_ingest._zip_sorted_infos(*_a, **_kw)


def cmd_chunk_apply(*_a, **_kw):
    return _tl_chunking.cmd_chunk_apply(*_a, **_kw)


def cmd_chunk_plan(*_a, **_kw):
    return _tl_chunking.cmd_chunk_plan(*_a, **_kw)


def cmd_chunk_verify(*_a, **_kw):
    return _tl_chunking.cmd_chunk_verify(*_a, **_kw)


def cmd_ingest_ocr(*_a, **_kw):
    return _tl_ocr.cmd_ingest_ocr(*_a, **_kw)


def cmd_ingest_zip(*_a, **_kw):
    return _tl_zip_ingest.cmd_ingest_zip(*_a, **_kw)


def cmd_ocr_analyze(*_a, **_kw):
    return _tl_ocr.cmd_ocr_analyze(*_a, **_kw)


def cmd_ocr_run(*_a, **_kw):
    return _tl_ocr.cmd_ocr_run(*_a, **_kw)


def cmd_ocr_verify(*_a, **_kw):
    return _tl_ocr.cmd_ocr_verify(*_a, **_kw)


def cmd_profile_ingest_chunks(*_a, **_kw):
    return _tl_chunking.cmd_profile_ingest_chunks(*_a, **_kw)


def cmd_profile_ingest_ocr(*_a, **_kw):
    return _tl_ocr.cmd_profile_ingest_ocr(*_a, **_kw)


def cmd_profile_ingest_zip(*_a, **_kw):
    return _tl_zip_ingest.cmd_profile_ingest_zip(*_a, **_kw)


def _build_release_manifest(*_a, **_kw):
    return _tl_release._build_release_manifest(*_a, **_kw)


def _golden_test(*_a, **_kw):
    return _tl_workflow._golden_test(*_a, **_kw)


def _live_readiness_report(*_a, **_kw):
    return _tl_live._live_readiness_report(*_a, **_kw)


def _live_smoke_plan(*_a, **_kw):
    return _tl_live._live_smoke_plan(*_a, **_kw)


def _load_workflow_card(*_a, **_kw):
    return _tl_workflow._load_workflow_card(*_a, **_kw)


def _release_should_include(*_a, **_kw):
    return _tl_release._release_should_include(*_a, **_kw)


def _verify_release_manifest(*_a, **_kw):
    return _tl_release._verify_release_manifest(*_a, **_kw)


def _workflow_cards_audit(*_a, **_kw):
    return _tl_workflow._workflow_cards_audit(*_a, **_kw)


def cmd_deploy_plan(*_a, **_kw):
    return _tl_live.cmd_deploy_plan(*_a, **_kw)


def cmd_determinism_audit(*_a, **_kw):
    return _tl_release.cmd_determinism_audit(*_a, **_kw)


def cmd_final_acceptance(*_a, **_kw):
    return _tl_live.cmd_final_acceptance(*_a, **_kw)


def cmd_go_live_runbook(*_a, **_kw):
    return _tl_live.cmd_go_live_runbook(*_a, **_kw)


def cmd_golden_test(*_a, **_kw):
    return _tl_workflow.cmd_golden_test(*_a, **_kw)


def cmd_live_contract_check(*_a, **_kw):
    return _tl_live.cmd_live_contract_check(*_a, **_kw)


def cmd_live_readiness(*_a, **_kw):
    return _tl_live.cmd_live_readiness(*_a, **_kw)


def cmd_live_smoke_plan(*_a, **_kw):
    return _tl_live.cmd_live_smoke_plan(*_a, **_kw)


def cmd_live_state_diff(*_a, **_kw):
    return _tl_live.cmd_live_state_diff(*_a, **_kw)


def cmd_live_state_snapshot(*_a, **_kw):
    return _tl_live.cmd_live_state_snapshot(*_a, **_kw)


def cmd_release_bundle(*_a, **_kw):
    return _tl_release.cmd_release_bundle(*_a, **_kw)


def cmd_bundle_export(*_a, **_kw):
    return _tl_release.cmd_bundle_export(*_a, **_kw)


def cmd_release_check(*_a, **_kw):
    return _tl_release.cmd_release_check(*_a, **_kw)


def cmd_release_manifest(*_a, **_kw):
    return _tl_release.cmd_release_manifest(*_a, **_kw)


def cmd_release_verify(*_a, **_kw):
    return _tl_release.cmd_release_verify(*_a, **_kw)


def cmd_rollback_plan(*_a, **_kw):
    return _tl_live.cmd_rollback_plan(*_a, **_kw)


def cmd_route_task(*_a, **_kw):
    return _tl_workflow.cmd_route_task(*_a, **_kw)


def cmd_tool_inventory(*_a, **_kw):
    return _tl_workflow.cmd_tool_inventory(*_a, **_kw)


def cmd_workflow_audit(*_a, **_kw):
    return _tl_workflow.cmd_workflow_audit(*_a, **_kw)


# ── I1 (v1.34.3): stub ủy quyền cụm hygiene → tl_core/hygiene.py (mọi caller cũ giữ nguyên) ──


def _vbhn_year_complete(*_a, **_kw):
    return _tl_hygiene._vbhn_year_complete(*_a, **_kw)


def _vbhn_year_fix_items(*_a, **_kw):
    return _tl_hygiene._vbhn_year_fix_items(*_a, **_kw)


def _quarantine_fix_items(*_a, **_kw):
    return _tl_hygiene._quarantine_fix_items(*_a, **_kw)


def _quarantine_clear_stale(*_a, **_kw):
    return _tl_hygiene._quarantine_clear_stale(*_a, **_kw)


def _hygiene_groups(*_a, **_kw):
    return _tl_hygiene._hygiene_groups(*_a, **_kw)


def cmd_hygiene(*_a, **_kw):
    return _tl_hygiene.cmd_hygiene(*_a, **_kw)


def cmd_registry_doctor(*_a, **_kw):
    return _tl_hygiene.cmd_registry_doctor(*_a, **_kw)


def cmd_cat_audit(*_a, **_kw):
    return _tl_hygiene.cmd_cat_audit(*_a, **_kw)


def _backfill_loai_candidates(*_a, **_kw):
    return _tl_hygiene._backfill_loai_candidates(*_a, **_kw)


def cmd_backfill_loai(*_a, **_kw):
    return _tl_hygiene.cmd_backfill_loai(*_a, **_kw)


def cmd_backfill_titlevn(*_a, **_kw):
    return _tl_hygiene.cmd_backfill_titlevn(*_a, **_kw)


def _backfill_hieuluc_candidates(*_a, **_kw):
    return _tl_hygiene._backfill_hieuluc_candidates(*_a, **_kw)


def cmd_backfill_hieuluc(*_a, **_kw):
    return _tl_hygiene.cmd_backfill_hieuluc(*_a, **_kw)


def cmd_missing_sohieu(*_a, **_kw):
    return _tl_hygiene.cmd_missing_sohieu(*_a, **_kw)


def cmd_vbhn_year_fix(*_a, **_kw):
    return _tl_hygiene.cmd_vbhn_year_fix(*_a, **_kw)


def cmd_dedup_plan(*_a, **_kw):
    return _tl_hygiene.cmd_dedup_plan(*_a, **_kw)


def _sweep_report(*_a, **_kw):
    return _tl_hygiene._sweep_report(*_a, **_kw)


def cmd_sweep(*_a, **_kw):
    return _tl_hygiene.cmd_sweep(*_a, **_kw)


def cmd_corpus_fix(*_a, **_kw):
    return _tl_hygiene.cmd_corpus_fix(*_a, **_kw)


def _consolidation_cleanup_plan(*_a, **_kw):
    return _tl_hygiene._consolidation_cleanup_plan(*_a, **_kw)


def cmd_consolidation_cleanup(*_a, **_kw):
    return _tl_hygiene.cmd_consolidation_cleanup(*_a, **_kw)


def cmd_quarantine_fix(*_a, **_kw):
    return _tl_hygiene.cmd_quarantine_fix(*_a, **_kw)


def _corpus_audit_row(*_a, **_kw):
    return _tl_hygiene._corpus_audit_row(*_a, **_kw)


def cmd_corpus_audit(*_a, **_kw):
    return _tl_hygiene.cmd_corpus_audit(*_a, **_kw)


def _review_queue_report(*_a, **_kw):
    return _tl_hygiene._review_queue_report(*_a, **_kw)


def _ops_plan_add(*_a, **_kw):
    return _tl_hygiene._ops_plan_add(*_a, **_kw)


def _ops_plan_report(*_a, **_kw):
    return _tl_hygiene._ops_plan_report(*_a, **_kw)


def cmd_ops_plan(*_a, **_kw):
    return _tl_hygiene.cmd_ops_plan(*_a, **_kw)


def cmd_review_queue(*_a, **_kw):
    return _tl_hygiene.cmd_review_queue(*_a, **_kw)


# ── I2 (v1.34.4): stub ủy quyền cụm nlm_wrappers → tl_core/nlm_ops.py (mọi caller cũ giữ nguyên) ──


def _preflight_invariants(*_a, **_kw):
    return _tl_nlm_ops._preflight_invariants(*_a, **_kw)


def _preflight_verdict(*_a, **_kw):
    return _tl_nlm_ops._preflight_verdict(*_a, **_kw)


def _raw_on_nlm_rows(*_a, **_kw):
    return _tl_nlm_ops._raw_on_nlm_rows(*_a, **_kw)


def _nlm_slot_count(*_a, **_kw):
    return _tl_nlm_ops._nlm_slot_count(*_a, **_kw)


def _slot_count_all_shards(*_a, **_kw):
    return _tl_nlm_ops._slot_count_all_shards(*_a, **_kw)


def cmd_slot_audit(*_a, **_kw):
    return _tl_nlm_ops.cmd_slot_audit(*_a, **_kw)


def cmd_nlm_list(*_a, **_kw):
    return _tl_nlm_ops.cmd_nlm_list(*_a, **_kw)


def _nlm_source_drive_id(*_a, **_kw):
    return _tl_nlm_ops._nlm_source_drive_id(*_a, **_kw)


def _nlm_reconcile_plan(*_a, **_kw):
    return _tl_nlm_ops._nlm_reconcile_plan(*_a, **_kw)


def cmd_nlm_reconcile(*_a, **_kw):
    return _tl_nlm_ops.cmd_nlm_reconcile(*_a, **_kw)


def _sohieu_loose(*_a, **_kw):
    return _tl_nlm_ops._sohieu_loose(*_a, **_kw)


def _discover_overflow_from_registry(*_a, **_kw):
    return _tl_nlm_ops._discover_overflow_from_registry(*_a, **_kw)


def cmd_preflight(*_a, **_kw):
    return _tl_nlm_ops.cmd_preflight(*_a, **_kw)


def cmd_push_overflow(*_a, **_kw):
    return _tl_nlm_ops.cmd_push_overflow(*_a, **_kw)


def _nlm_dedup_gate(*_a, **_kw):
    return _tl_nlm_ops._nlm_dedup_gate(*_a, **_kw)


def _nlm_post_add_dup_check(*_a, **_kw):
    return _tl_nlm_ops._nlm_post_add_dup_check(*_a, **_kw)


def _overflow_route(*_a, **_kw):
    return _tl_nlm_ops._overflow_route(*_a, **_kw)


def _overflow_status(*_a, **_kw):
    return _tl_nlm_ops._overflow_status(*_a, **_kw)


def cmd_overflow_resolve(*_a, **_kw):
    return _tl_nlm_ops.cmd_overflow_resolve(*_a, **_kw)


def cmd_nlm_content(*_a, **_kw):
    return _tl_nlm_ops.cmd_nlm_content(*_a, **_kw)


def cmd_nlm_query(*_a, **_kw):
    return _tl_nlm_ops.cmd_nlm_query(*_a, **_kw)


def cmd_nlm_add(*_a, **_kw):
    return _tl_nlm_ops.cmd_nlm_add(*_a, **_kw)


def cmd_nlm_cross(*_a, **_kw):
    return _tl_nlm_ops.cmd_nlm_cross(*_a, **_kw)


def _classify_nlm_sources(*_a, **_kw):
    return _tl_nlm_ops._classify_nlm_sources(*_a, **_kw)


def cmd_nlm_orphans(*_a, **_kw):
    return _tl_nlm_ops.cmd_nlm_orphans(*_a, **_kw)


def cmd_nlm_get(*_a, **_kw):
    return _tl_nlm_ops.cmd_nlm_get(*_a, **_kw)


def _nlm_query_plan(*_a, **_kw):
    return _tl_nlm_ops._nlm_query_plan(*_a, **_kw)


def cmd_nlm_query_plan(*_a, **_kw):
    return _tl_nlm_ops.cmd_nlm_query_plan(*_a, **_kw)


# ── I3 (v1.34.5): stub ủy quyền extract_cache + fetch_web → tl_core/ (mọi caller cũ giữ nguyên) ──


def cmd_extract(*_a, **_kw):
    return _tl_extract_cache.cmd_extract(*_a, **_kw)


def cmd_cache_build(*_a, **_kw):
    return _tl_extract_cache.cmd_cache_build(*_a, **_kw)


def cmd_cache_snapshot(*_a, **_kw):
    return _tl_extract_cache.cmd_cache_snapshot(*_a, **_kw)


def _external_ingest_plan(*_a, **_kw):
    return _tl_fetch_web._external_ingest_plan(*_a, **_kw)


def cmd_external_ingest(*_a, **_kw):
    return _tl_fetch_web.cmd_external_ingest(*_a, **_kw)


def cmd_link_priority(*_a, **_kw):
    return _tl_fetch_web.cmd_link_priority(*_a, **_kw)


def _frontier_candidates(*_a, **_kw):
    return _tl_fetch_web._frontier_candidates(*_a, **_kw)


def _frontier_doc_text(*_a, **_kw):
    return _tl_fetch_web._frontier_doc_text(*_a, **_kw)


def cmd_frontier_expand(*_a, **_kw):
    return _tl_fetch_web.cmd_frontier_expand(*_a, **_kw)


def cmd_tvpl_url(*_a, **_kw):
    return _tl_fetch_web.cmd_tvpl_url(*_a, **_kw)


def _fetch_plan(*_a, **_kw):
    return _tl_fetch_web._fetch_plan(*_a, **_kw)


def cmd_fetch_route(*_a, **_kw):
    return _tl_fetch_web.cmd_fetch_route(*_a, **_kw)


def cmd_fetch_batch(*_a, **_kw):
    return _tl_fetch_web.cmd_fetch_batch(*_a, **_kw)


def cmd_fetch_links(*_a, **_kw):
    return _tl_fetch_web.cmd_fetch_links(*_a, **_kw)


def cmd_find_doc(*_a, **_kw):
    return _tl_fetch_web.cmd_find_doc(*_a, **_kw)


# ── I4 (v1.34.7): stub ủy quyền cụm profile_mgmt → tl_core/profile_mgmt.py ──


def _profile_rebuild_partition(*_a, **_kw):
    return _tl_profile_mgmt._profile_rebuild_partition(*_a, **_kw)


def cmd_profile_rebuild_registry(*_a, **_kw):
    return _tl_profile_mgmt.cmd_profile_rebuild_registry(*_a, **_kw)


def _profile_info_from_config(*_a, **_kw):
    return _tl_profile_mgmt._profile_info_from_config(*_a, **_kw)


def cmd_profile_info(*_a, **_kw):
    return _tl_profile_mgmt.cmd_profile_info(*_a, **_kw)


def _profile_manifest_entries_for(*_a, **_kw):
    return _tl_profile_mgmt._profile_manifest_entries_for(*_a, **_kw)


def cmd_profile_list(*_a, **_kw):
    return _tl_profile_mgmt.cmd_profile_list(*_a, **_kw)


def cmd_profile_use(*_a, **_kw):
    return _tl_profile_mgmt.cmd_profile_use(*_a, **_kw)


def cmd_profile_rename(*_a, **_kw):
    return _tl_profile_mgmt.cmd_profile_rename(*_a, **_kw)


def cmd_profile_delete(*_a, **_kw):
    return _tl_profile_mgmt.cmd_profile_delete(*_a, **_kw)


def cmd_profile_files(*_a, **_kw):
    return _tl_profile_mgmt.cmd_profile_files(*_a, **_kw)


def cmd_profile_manifest(*_a, **_kw):
    return _tl_profile_mgmt.cmd_profile_manifest(*_a, **_kw)


def _create_profile_manifest_json(*_a, **_kw):
    return _tl_profile_mgmt._create_profile_manifest_json(*_a, **_kw)


def _profile_list_discover(*_a, **_kw):
    return _tl_profile_mgmt._profile_list_discover(*_a, **_kw)


def cmd_profile_adopt(*_a, **_kw):
    return _tl_profile_mgmt.cmd_profile_adopt(*_a, **_kw)


def _cmd_profile_adopt_impl(*_a, **_kw):
    return _tl_profile_mgmt._cmd_profile_adopt_impl(*_a, **_kw)


def cmd_profile_doctor(*_a, **_kw):
    return _tl_profile_mgmt.cmd_profile_doctor(*_a, **_kw)


def _cmd_profile_doctor_impl(*_a, **_kw):
    return _tl_profile_mgmt._cmd_profile_doctor_impl(*_a, **_kw)


def _profile_index_rows(*_a, **_kw):
    return _tl_profile_mgmt._profile_index_rows(*_a, **_kw)


def _profile_index_csv(*_a, **_kw):
    return _tl_profile_mgmt._profile_index_csv(*_a, **_kw)


def cmd_profile_index(*_a, **_kw):
    return _tl_profile_mgmt.cmd_profile_index(*_a, **_kw)


def _cmd_profile_index_impl(*_a, **_kw):
    return _tl_profile_mgmt._cmd_profile_index_impl(*_a, **_kw)


def cmd_profile_create(*_a, **_kw):
    return _tl_profile_mgmt.cmd_profile_create(*_a, **_kw)


# ── I5 (v1.34.8): stub ủy quyền cụm ingest_pipeline → tl_core/ingest_ops.py ──


def cmd_ingest(*_a, **_kw):
    return _tl_ingest_ops.cmd_ingest(*_a, **_kw)


def cmd_register(*_a, **_kw):
    return _tl_ingest_ops.cmd_register(*_a, **_kw)


def cmd_ingest_analyze(*_a, **_kw):
    return _tl_ingest_ops.cmd_ingest_analyze(*_a, **_kw)


def cmd_ingest_route(*_a, **_kw):
    return _tl_ingest_ops.cmd_ingest_route(*_a, **_kw)


def _ingest_missing_select(*_a, **_kw):
    return _tl_ingest_ops._ingest_missing_select(*_a, **_kw)


def _ingest_missing_partition(*_a, **_kw):
    return _tl_ingest_ops._ingest_missing_partition(*_a, **_kw)


def _ingest_dedup_title_key(*_a, **_kw):
    return _tl_ingest_ops._ingest_dedup_title_key(*_a, **_kw)


def _ingest_missing_dedup_live(*_a, **_kw):
    return _tl_ingest_ops._ingest_missing_dedup_live(*_a, **_kw)


def _ingest_ckpt_load(*_a, **_kw):
    return _tl_ingest_ops._ingest_ckpt_load(*_a, **_kw)


def _ingest_ckpt_load_full(*_a, **_kw):
    return _tl_ingest_ops._ingest_ckpt_load_full(*_a, **_kw)


def cmd_ingest_missing(*_a, **_kw):
    return _tl_ingest_ops.cmd_ingest_missing(*_a, **_kw)


def _upload_mime_ext(*_a, **_kw):
    return _tl_ingest_ops._upload_mime_ext(*_a, **_kw)


def _ingest_target(*_a, **_kw):
    return _tl_ingest_ops._ingest_target(*_a, **_kw)


def cmd_recat(*_a, **_kw):
    return _tl_ingest_ops.cmd_recat(*_a, **_kw)


def _shared_source_id_groups(*_a, **_kw):
    return _tl_ingest_ops._shared_source_id_groups(*_a, **_kw)


def _shared_source_fix_plan(*_a, **_kw):
    return _tl_ingest_ops._shared_source_fix_plan(*_a, **_kw)


def cmd_shared_source_fix(*_a, **_kw):
    return _tl_ingest_ops.cmd_shared_source_fix(*_a, **_kw)


def _source_rename_plan(*_a, **_kw):
    return _tl_ingest_ops._source_rename_plan(*_a, **_kw)


def cmd_source_rename(*_a, **_kw):
    return _tl_ingest_ops.cmd_source_rename(*_a, **_kw)


def _source_delete_plan(*_a, **_kw):
    return _tl_ingest_ops._source_delete_plan(*_a, **_kw)


def cmd_source_delete(*_a, **_kw):
    return _tl_ingest_ops.cmd_source_delete(*_a, **_kw)


def _source_update_corpus_plan(*_a, **_kw):
    return _tl_ingest_ops._source_update_corpus_plan(*_a, **_kw)


def cmd_source_update_corpus(*_a, **_kw):
    return _tl_ingest_ops.cmd_source_update_corpus(*_a, **_kw)


def _profile_source_quality(*_a, **_kw):
    return _tl_ingest_ops._profile_source_quality(*_a, **_kw)


def _profile_read_probe_text(*_a, **_kw):
    return _tl_ingest_ops._profile_read_probe_text(*_a, **_kw)


def _sohieu_from_title_zone(*_a, **_kw):
    return _tl_ingest_ops._sohieu_from_title_zone(*_a, **_kw)


def _classify_doc_header(*_a, **_kw):
    return _tl_ingest_ops._classify_doc_header(*_a, **_kw)


def _safe_profile_doc_name(*_a, **_kw):
    return _tl_ingest_ops._safe_profile_doc_name(*_a, **_kw)


def _ingest_verify_gate(*_a, **_kw):
    return _tl_ingest_ops._ingest_verify_gate(*_a, **_kw)


def _split_by_dieu_chunks(*_a, **_kw):
    return _tl_ingest_ops._split_by_dieu_chunks(*_a, **_kw)


def _chunk_summaries(*_a, **_kw):
    return _tl_ingest_ops._chunk_summaries(*_a, **_kw)


def _profile_ingest_note(*_a, **_kw):
    return _tl_ingest_ops._profile_ingest_note(*_a, **_kw)


def cmd_profile_ingest(*_a, **_kw):
    return _tl_ingest_ops.cmd_profile_ingest(*_a, **_kw)


def _ingest_local_cat_gate(*_a, **_kw):
    return _tl_ingest_ops._ingest_local_cat_gate(*_a, **_kw)


def _ingest_local_prev_state(*_a, **_kw):
    return _tl_ingest_ops._ingest_local_prev_state(*_a, **_kw)


def cmd_ingest_local(*_a, **_kw):
    return _tl_ingest_ops.cmd_ingest_local(*_a, **_kw)


def _verify_convert_readback(*_a, **_kw):
    return _tl_ingest_ops._verify_convert_readback(*_a, **_kw)


# ── I6 (v1.34.9): stub ủy quyền cụm lookup → tl_core/lookup_ops.py (mọi caller cũ giữ nguyên) ──


def _vbhn_bare_key(*_a, **_kw):
    return _tl_lookup_ops._vbhn_bare_key(*_a, **_kw)


def cmd_locate(*_a, **_kw):
    return _tl_lookup_ops.cmd_locate(*_a, **_kw)


def _find_amendment_candidates(*_a, **_kw):
    return _tl_lookup_ops._find_amendment_candidates(*_a, **_kw)


def cmd_source_map(*_a, **_kw):
    return _tl_lookup_ops.cmd_source_map(*_a, **_kw)


def cmd_status(*_a, **_kw):
    return _tl_lookup_ops.cmd_status(*_a, **_kw)


def _status_amendment_registry_guard(*_a, **_kw):
    return _tl_lookup_ops._status_amendment_registry_guard(*_a, **_kw)


def _relation_refs(*_a, **_kw):
    return _tl_lookup_ops._relation_refs(*_a, **_kw)


def _is_amendment_like(*_a, **_kw):
    return _tl_lookup_ops._is_amendment_like(*_a, **_kw)


def _header_verify_infer_cats(*_a, **_kw):
    return _tl_lookup_ops._header_verify_infer_cats(*_a, **_kw)


def _relation_candidate_flags(*_a, **_kw):
    return _tl_lookup_ops._relation_candidate_flags(*_a, **_kw)


def _relation_backfill_items(*_a, **_kw):
    return _tl_lookup_ops._relation_backfill_items(*_a, **_kw)


def cmd_relation_backfill(*_a, **_kw):
    return _tl_lookup_ops.cmd_relation_backfill(*_a, **_kw)


def cmd_relation_check(*_a, **_kw):
    return _tl_lookup_ops.cmd_relation_check(*_a, **_kw)


def _amendments_covered_by_vbhn_date(*_a, **_kw):
    return _tl_lookup_ops._amendments_covered_by_vbhn_date(*_a, **_kw)


def _source_map_flags(*_a, **_kw):
    return _tl_lookup_ops._source_map_flags(*_a, **_kw)


def _summ_entry_source_map(*_a, **_kw):
    return _tl_lookup_ops._summ_entry_source_map(*_a, **_kw)


def _source_map_verdict(*_a, **_kw):
    return _tl_lookup_ops._source_map_verdict(*_a, **_kw)


def _vbhn_check_verdict(*_a, **_kw):
    return _tl_lookup_ops._vbhn_check_verdict(*_a, **_kw)


def cmd_header_verify(*_a, **_kw):
    return _tl_lookup_ops.cmd_header_verify(*_a, **_kw)


def _rasoat_fallback_plan(*_a, **_kw):
    return _tl_lookup_ops._rasoat_fallback_plan(*_a, **_kw)


def _rasoat_map_positional(*_a, **_kw):
    return _tl_lookup_ops._rasoat_map_positional(*_a, **_kw)


def _rasoat_autocache_worksheet(*_a, **_kw):
    return _tl_lookup_ops._rasoat_autocache_worksheet(*_a, **_kw)


def cmd_rasoat(*_a, **_kw):
    return _tl_lookup_ops.cmd_rasoat(*_a, **_kw)


def _is_high_amendment_subject(*_a, **_kw):
    return _tl_lookup_ops._is_high_amendment_subject(*_a, **_kw)


def _qt5_queries(*_a, **_kw):
    return _tl_lookup_ops._qt5_queries(*_a, **_kw)


def cmd_vbhn_check(*_a, **_kw):
    return _tl_lookup_ops.cmd_vbhn_check(*_a, **_kw)


def _vbhn_verify_flags(*_a, **_kw):
    return _tl_lookup_ops._vbhn_verify_flags(*_a, **_kw)


def _focus_block(*_a, **_kw):
    return _tl_lookup_ops._focus_block(*_a, **_kw)


def _vbhn_compare(*_a, **_kw):
    return _tl_lookup_ops._vbhn_compare(*_a, **_kw)


def cmd_vbhn_verify(*_a, **_kw):
    return _tl_lookup_ops.cmd_vbhn_verify(*_a, **_kw)


def cmd_vbhn_compare(*_a, **_kw):
    return _tl_lookup_ops.cmd_vbhn_compare(*_a, **_kw)


def _parse_footnote_def(*_a, **_kw):
    return _tl_lookup_ops._parse_footnote_def(*_a, **_kw)


def _footnote_rel_kind(*_a, **_kw):
    return _tl_lookup_ops._footnote_rel_kind(*_a, **_kw)


def cmd_xref(*_a, **_kw):
    return _tl_lookup_ops.cmd_xref(*_a, **_kw)


def _rasoat_dedup_push(*_a, **_kw):
    return _tl_lookup_ops._rasoat_dedup_push(*_a, **_kw)


def _rasoat_expand_text(*_a, **_kw):
    return _tl_lookup_ops._rasoat_expand_text(*_a, **_kw)


def cmd_rasoat_loop(*_a, **_kw):
    return _tl_lookup_ops.cmd_rasoat_loop(*_a, **_kw)


def cmd_footnote_map(*_a, **_kw):
    return _tl_lookup_ops.cmd_footnote_map(*_a, **_kw)


def cmd_dedup_check(*_a, **_kw):
    return _tl_lookup_ops.cmd_dedup_check(*_a, **_kw)


def cmd_cluster(*_a, **_kw):
    return _tl_lookup_ops.cmd_cluster(*_a, **_kw)


def cmd_rasoat_chongcheo(*_a, **_kw):
    return _tl_lookup_ops.cmd_rasoat_chongcheo(*_a, **_kw)


# ── I8 (v1.34.12): stub ủy quyền nhóm lệnh vận-hành/chẩn-đoán → tl_core/ops_misc.py ──


def _journal_read(*_a, **_kw):
    return _tl_ops_misc._journal_read(*_a, **_kw)


def _journal_undo_ops(*_a, **_kw):
    return _tl_ops_misc._journal_undo_ops(*_a, **_kw)


def _journal_resume_ops(*_a, **_kw):
    return _tl_ops_misc._journal_resume_ops(*_a, **_kw)


def _journal_close_plan(*_a, **_kw):
    return _tl_ops_misc._journal_close_plan(*_a, **_kw)


def _loop_controller(*_a, **_kw):
    return _tl_ops_misc._loop_controller(*_a, **_kw)


def _integrity_scan(*_a, **_kw):
    return _tl_ops_misc._integrity_scan(*_a, **_kw)


def cmd_edit_skill(*_a, **_kw):
    return _tl_ops_misc.cmd_edit_skill(*_a, **_kw)


def cmd_verify_integrity(*_a, **_kw):
    return _tl_ops_misc.cmd_verify_integrity(*_a, **_kw)


def gas_parallel(*_a, **_kw):
    return _tl_ops_misc.gas_parallel(*_a, **_kw)


def cmd_ping(*_a, **_kw):
    return _tl_ops_misc.cmd_ping(*_a, **_kw)


def cmd_perf(*_a, **_kw):
    return _tl_ops_misc.cmd_perf(*_a, **_kw)


def cmd_boot(*_a, **_kw):
    return _tl_ops_misc.cmd_boot(*_a, **_kw)


def save_local_config(*_a, **_kw):
    return _tl_ops_misc.save_local_config(*_a, **_kw)


def public_download_text(*_a, **_kw):
    return _tl_ops_misc.public_download_text(*_a, **_kw)


def _skill_package_integrity(*_a, **_kw):
    return _tl_ops_misc._skill_package_integrity(*_a, **_kw)


def _ensure_gws_nlm(*_a, **_kw):
    return _tl_ops_misc._ensure_gws_nlm(*_a, **_kw)


def cmd_init_config(*_a, **_kw):
    return _tl_ops_misc.cmd_init_config(*_a, **_kw)


def cmd_up(*_a, **_kw):
    return _tl_ops_misc.cmd_up(*_a, **_kw)


def cmd_precheck(*_a, **_kw):
    return _tl_ops_misc.cmd_precheck(*_a, **_kw)


def cmd_journal(*_a, **_kw):
    return _tl_ops_misc.cmd_journal(*_a, **_kw)


def _journal_reapply_one(*_a, **_kw):
    return _tl_ops_misc._journal_reapply_one(*_a, **_kw)


def cmd_undo(*_a, **_kw):
    return _tl_ops_misc.cmd_undo(*_a, **_kw)


def cmd_resume(*_a, **_kw):
    return _tl_ops_misc.cmd_resume(*_a, **_kw)


def _doctor_exporttext_probe(*_a, **_kw):
    return _tl_ops_misc._doctor_exporttext_probe(*_a, **_kw)


def cmd_doctor(*_a, **_kw):
    return _tl_ops_misc.cmd_doctor(*_a, **_kw)


def cmd_cowork_plan(*_a, **_kw):
    return _tl_ops_misc.cmd_cowork_plan(*_a, **_kw)


def cmd_exists(*_a, **_kw):
    return _tl_ops_misc.cmd_exists(*_a, **_kw)


def _resolve_registry_doc_id(*_a, **_kw):
    return _tl_ops_misc._resolve_registry_doc_id(*_a, **_kw)


def cmd_instructions(*_a, **_kw):
    return _tl_ops_misc.cmd_instructions(*_a, **_kw)


def _resolve_confirm_targets(*_a, **_kw):
    return _tl_ops_misc._resolve_confirm_targets(*_a, **_kw)


def cmd_confirm(*_a, **_kw):
    return _tl_ops_misc.cmd_confirm(*_a, **_kw)


def cmd_manifest(*_a, **_kw):
    return _tl_ops_misc.cmd_manifest(*_a, **_kw)


def _vbhn_normalize_recommendations(*_a, **_kw):
    return _tl_ops_misc._vbhn_normalize_recommendations(*_a, **_kw)


def cmd_vbhn_normalize(*_a, **_kw):
    return _tl_ops_misc.cmd_vbhn_normalize(*_a, **_kw)


def _pin_registry_doc_id_config(*_a, **_kw):
    return _tl_ops_misc._pin_registry_doc_id_config(*_a, **_kw)


def cmd_config_pin_registry(*_a, **_kw):
    return _tl_ops_misc.cmd_config_pin_registry(*_a, **_kw)


def _merge_base_entries(*_a, **_kw):
    return _tl_ops_misc._merge_base_entries(*_a, **_kw)


def cmd_profile_file_remove(*_a, **_kw):
    return _tl_ops_misc.cmd_profile_file_remove(*_a, **_kw)


def cmd_registry_map(*_a, **_kw):
    return _tl_ops_misc.cmd_registry_map(*_a, **_kw)


def _instruction_audit_text(*_a, **_kw):
    return _tl_ops_misc._instruction_audit_text(*_a, **_kw)


def cmd_instruction_audit(*_a, **_kw):
    return _tl_ops_misc.cmd_instruction_audit(*_a, **_kw)


def cmd_backfill_notebook(*_a, **_kw):
    return _tl_ops_misc.cmd_backfill_notebook(*_a, **_kw)


def cmd_reg_delete(*_a, **_kw):
    return _tl_ops_misc.cmd_reg_delete(*_a, **_kw)


def cmd_bench(*_a, **_kw):
    return _tl_ops_misc.cmd_bench(*_a, **_kw)


def _content_md5(*_a, **_kw):
    return _tl_ops_misc._content_md5(*_a, **_kw)


def cmd_source_verify(*_a, **_kw):
    return _tl_ops_misc.cmd_source_verify(*_a, **_kw)


def _reg_query_row(*_a, **_kw):
    return _tl_ops_misc._reg_query_row(*_a, **_kw)


def cmd_reg_query(*_a, **_kw):
    return _tl_ops_misc.cmd_reg_query(*_a, **_kw)


def cmd_cat_verify(*_a, **_kw):
    return _tl_ops_misc.cmd_cat_verify(*_a, **_kw)


def _registry_claim_by_notebook(*_a, **_kw):
    return _tl_ops_misc._registry_claim_by_notebook(*_a, **_kw)


def _registry_claim_target(*_a, **_kw):
    return _tl_ops_misc._registry_claim_target(*_a, **_kw)


def cmd_counts(*_a, **_kw):
    return _tl_ops_misc.cmd_counts(*_a, **_kw)


def _entries_with_live_fields(*_a, **_kw):
    return _tl_ops_misc._entries_with_live_fields(*_a, **_kw)


def cmd_loop(*_a, **_kw):
    return _tl_ops_misc.cmd_loop(*_a, **_kw)


def cmd_cat_list(*_a, **_kw):
    return _tl_ops_misc.cmd_cat_list(*_a, **_kw)


def cmd_convert_verify(*_a, **_kw):
    return _tl_ops_misc.cmd_convert_verify(*_a, **_kw)


# ── I9a (v1.34.13): stub ủy quyền infra classify + profile_env → tl_core/ ──


def _selected_profile_name(*_a, **_kw):
    return _tl_classify._selected_profile_name(*_a, **_kw)


def _subject_tokens_for_entry(*_a, **_kw):
    return _tl_classify._subject_tokens_for_entry(*_a, **_kw)


def _verify_header_match(*_a, **_kw):
    return _tl_classify._verify_header_match(*_a, **_kw)


def _extract_header_facts(*_a, **_kw):
    return _tl_classify._extract_header_facts(*_a, **_kw)


def _clean_subject_text(*_a, **_kw):
    return _tl_classify._clean_subject_text(*_a, **_kw)


def _has_diacritics(*_a, **_kw):
    return _tl_classify._has_diacritics(*_a, **_kw)


def _looks_like_filename_title(*_a, **_kw):
    return _tl_classify._looks_like_filename_title(*_a, **_kw)


def _name_tail_pretty(*_a, **_kw):
    return _tl_classify._name_tail_pretty(*_a, **_kw)


def _derive_subject_from_entries(*_a, **_kw):
    return _tl_classify._derive_subject_from_entries(*_a, **_kw)


def _strip_accents(*_a, **_kw):
    return _tl_classify._strip_accents(*_a, **_kw)


def _entry_name(*_a, **_kw):
    return _tl_classify._entry_name(*_a, **_kw)


def _nlm_status_known(*_a, **_kw):
    return _tl_classify._nlm_status_known(*_a, **_kw)


def _name_goc_base_key(*_a, **_kw):
    return _tl_classify._name_goc_base_key(*_a, **_kw)


def _name_key(*_a, **_kw):
    return _tl_classify._name_key(*_a, **_kw)


def _omnibus_name_text(*_a, **_kw):
    return _tl_classify._omnibus_name_text(*_a, **_kw)


def _omnibus_name_evidence(*_a, **_kw):
    return _tl_classify._omnibus_name_evidence(*_a, **_kw)


def _is_omnibus_entry(*_a, **_kw):
    return _tl_classify._is_omnibus_entry(*_a, **_kw)


def _name_subset_match(*_a, **_kw):
    return _tl_classify._name_subset_match(*_a, **_kw)


def _compact_phrase(*_a, **_kw):
    return _tl_classify._compact_phrase(*_a, **_kw)


def _name_phrase_match(*_a, **_kw):
    return _tl_classify._name_phrase_match(*_a, **_kw)


def _name_content_tokens(*_a, **_kw):
    return _tl_classify._name_content_tokens(*_a, **_kw)


def _name_strong_match(*_a, **_kw):
    return _tl_classify._name_strong_match(*_a, **_kw)


def _name_subject_text(*_a, **_kw):
    return _tl_classify._name_subject_text(*_a, **_kw)


def _name_subject_match(*_a, **_kw):
    return _tl_classify._name_subject_match(*_a, **_kw)


def _normalize_loai(*_a, **_kw):
    return _tl_classify._normalize_loai(*_a, **_kw)


def _infer_loai(*_a, **_kw):
    return _tl_classify._infer_loai(*_a, **_kw)


def _loai_is_noncanonical(*_a, **_kw):
    return _tl_classify._loai_is_noncanonical(*_a, **_kw)


def _name_tail_key(*_a, **_kw):
    return _tl_classify._name_tail_key(*_a, **_kw)


def _title_flags(*_a, **_kw):
    return _tl_classify._title_flags(*_a, **_kw)


def _is_treaty_entry(*_a, **_kw):
    return _tl_classify._is_treaty_entry(*_a, **_kw)


def _name_is_template_or_appendix(*_a, **_kw):
    return _tl_classify._name_is_template_or_appendix(*_a, **_kw)


def _parse_sohieu_from_name(*_a, **_kw):
    return _tl_classify._parse_sohieu_from_name(*_a, **_kw)


def _doc_subject_key(*_a, **_kw):
    return _tl_classify._doc_subject_key(*_a, **_kw)


def _cat_bare_full_variants(*_a, **_kw):
    return _tl_classify._cat_bare_full_variants(*_a, **_kw)


def _subject_tokens(*_a, **_kw):
    return _tl_classify._subject_tokens(*_a, **_kw)


def _entry_subject_text(*_a, **_kw):
    return _tl_classify._entry_subject_text(*_a, **_kw)


def _disc_conflict(*_a, **_kw):
    return _tl_classify._disc_conflict(*_a, **_kw)


def _subject_score(*_a, **_kw):
    return _tl_classify._subject_score(*_a, **_kw)


def _discover_classify(*_a, **_kw):
    return _tl_classify._discover_classify(*_a, **_kw)


def _clean_ref_name_phrase(*_a, **_kw):
    return _tl_classify._clean_ref_name_phrase(*_a, **_kw)


def _is_raw_no_gdoc_name(*_a, **_kw):
    return _tl_classify._is_raw_no_gdoc_name(*_a, **_kw)


def _load_subject_clusters(*_a, **_kw):
    return _tl_classify._load_subject_clusters(*_a, **_kw)


def _norm_cat(*_a, **_kw):
    return _tl_classify._norm_cat(*_a, **_kw)


def _is_valid_cat_value(*_a, **_kw):
    return _tl_classify._is_valid_cat_value(*_a, **_kw)


def _ascii_lower(*_a, **_kw):
    return _tl_classify._ascii_lower(*_a, **_kw)


def _infer_cats(*_a, **_kw):
    return _tl_classify._infer_cats(*_a, **_kw)


def _cat_taxonomy(*_a, **_kw):
    return _tl_classify._cat_taxonomy(*_a, **_kw)


def _alias_cat_pairs(*_a, **_kw):
    return _tl_classify._alias_cat_pairs(*_a, **_kw)


def _expected_cat_from_alias(*_a, **_kw):
    return _tl_classify._expected_cat_from_alias(*_a, **_kw)


def _infer_cats_text(*_a, **_kw):
    return _tl_classify._infer_cats_text(*_a, **_kw)


def _cat_boundary_rule(*_a, **_kw):
    return _tl_classify._cat_boundary_rule(*_a, **_kw)


def _subject_sig(*_a, **_kw):
    return _tl_classify._subject_sig(*_a, **_kw)


def _cat_reg_label(*_a, **_kw):
    return _tl_classify._cat_reg_label(*_a, **_kw)


def _resolve_cat_folder_impl(*_a, **_kw):
    return _tl_classify._resolve_cat_folder_impl(*_a, **_kw)


def _resolve_cat_folder(*_a, **_kw):
    return _tl_classify._resolve_cat_folder(*_a, **_kw)


def _title_sentence_case(*_a, **_kw):
    return _tl_classify._title_sentence_case(*_a, **_kw)


def _title_block_from_text(*_a, **_kw):
    return _tl_classify._title_block_from_text(*_a, **_kw)


def _title_vn_from_header(*_a, **_kw):
    return _tl_classify._title_vn_from_header(*_a, **_kw)


def _title_vn_from_tukhoa(*_a, **_kw):
    return _tl_classify._title_vn_from_tukhoa(*_a, **_kw)


def _title_vn_from_plan(*_a, **_kw):
    return _tl_classify._title_vn_from_plan(*_a, **_kw)


def _backfill_titlevn_candidates(*_a, **_kw):
    return _tl_classify._backfill_titlevn_candidates(*_a, **_kw)


def _profile_title_from_header(*_a, **_kw):
    return _tl_classify._profile_title_from_header(*_a, **_kw)


def _doc_subject_for_name(*_a, **_kw):
    return _tl_classify._doc_subject_for_name(*_a, **_kw)


def _vb_title_short_for_name(*_a, **_kw):
    return _tl_classify._vb_title_short_for_name(*_a, **_kw)


def _vb_standard_doc_name(*_a, **_kw):
    return _tl_classify._vb_standard_doc_name(*_a, **_kw)


def _vb_auto_cat_from_text(*_a, **_kw):
    return _tl_classify._vb_auto_cat_from_text(*_a, **_kw)


def _name_prefix_family(*_a, **_kw):
    return _tl_classify._name_prefix_family(*_a, **_kw)


def _name_structural_issues(*_a, **_kw):
    return _tl_classify._name_structural_issues(*_a, **_kw)


def _name_looks_nonstandard(*_a, **_kw):
    return _tl_classify._name_looks_nonstandard(*_a, **_kw)


def _subject_is_boilerplate(*_a, **_kw):
    return _tl_classify._subject_is_boilerplate(*_a, **_kw)


def _cat_alias_evidence_for(*_a, **_kw):
    return _tl_classify._cat_alias_evidence_for(*_a, **_kw)


def _cat_likely_wrong_suggest(*_a, **_kw):
    return _tl_classify._cat_likely_wrong_suggest(*_a, **_kw)


def _declared_loai_from_header(*_a, **_kw):
    return _tl_classify._declared_loai_from_header(*_a, **_kw)


def _file_name(*_a, **_kw):
    return _tl_classify._file_name(*_a, **_kw)


def _read_json_file(*_a, **_kw):
    return _tl_profile_env._read_json_file(*_a, **_kw)


def _config_candidates(*_a, **_kw):
    return _tl_profile_env._config_candidates(*_a, **_kw)


def _profiles_from_config(*_a, **_kw):
    return _tl_profile_env._profiles_from_config(*_a, **_kw)


def _profile_lookup(*_a, **_kw):
    return _tl_profile_env._profile_lookup(*_a, **_kw)


def _apply_profile_env(*_a, **_kw):
    return _tl_profile_env._apply_profile_env(*_a, **_kw)


def _active_profile(*_a, **_kw):
    return _tl_profile_env._active_profile(*_a, **_kw)


def _resolve_nlm_notebook(*_a, **_kw):
    return _tl_profile_env._resolve_nlm_notebook(*_a, **_kw)


def _profile_policy_error(*_a, **_kw):
    return _tl_profile_env._profile_policy_error(*_a, **_kw)


def _emit_profile_policy_error(*_a, **_kw):
    return _tl_profile_env._emit_profile_policy_error(*_a, **_kw)


def _profile_cache_dir(*_a, **_kw):
    return _tl_profile_env._profile_cache_dir(*_a, **_kw)


def load_creds(*_a, **_kw):
    return _tl_profile_env.load_creds(*_a, **_kw)


def apply_profile_offline(*_a, **_kw):
    return _tl_profile_env.apply_profile_offline(*_a, **_kw)


def _gas(*_a, **_kw):
    return _tl_profile_env._gas(*_a, **_kw)


def _gws_nlm_note(*_a, **_kw):
    return _tl_profile_env._gws_nlm_note(*_a, **_kw)


def _strip_goc_token(*_a, **_kw):
    return _tl_profile_env._strip_goc_token(*_a, **_kw)


def _token_set(*_a, **_kw):
    return _tl_profile_env._token_set(*_a, **_kw)


def _ref_tokens(*_a, **_kw):
    return _tl_profile_env._ref_tokens(*_a, **_kw)


def _gas_get_retry(*_a, **_kw):
    return _tl_profile_env._gas_get_retry(*_a, **_kw)


def _download_link_rank(*_a, **_kw):
    return _tl_profile_env._download_link_rank(*_a, **_kw)


def _download_link_plan(*_a, **_kw):
    return _tl_profile_env._download_link_plan(*_a, **_kw)


def _persist_profile_config(*_a, **_kw):
    return _tl_profile_env._persist_profile_config(*_a, **_kw)


def _read_config_record(*_a, **_kw):
    return _tl_profile_env._read_config_record(*_a, **_kw)


def _write_json_atomic(*_a, **_kw):
    return _tl_profile_env._write_json_atomic(*_a, **_kw)


def _mutable_config_target(*_a, **_kw):
    return _tl_profile_env._mutable_config_target(*_a, **_kw)


def _profile_config_rows(*_a, **_kw):
    return _tl_profile_env._profile_config_rows(*_a, **_kw)


def _rename_profile_config(*_a, **_kw):
    return _tl_profile_env._rename_profile_config(*_a, **_kw)


def _remove_profile_config(*_a, **_kw):
    return _tl_profile_env._remove_profile_config(*_a, **_kw)


def _set_default_profile_config(*_a, **_kw):
    return _tl_profile_env._set_default_profile_config(*_a, **_kw)


def _profile_asset_ids(*_a, **_kw):
    return _tl_profile_env._profile_asset_ids(*_a, **_kw)


def _profile_live_source_ids(*_a, **_kw):
    return _tl_profile_env._profile_live_source_ids(*_a, **_kw)


def _profile_asset_owners(*_a, **_kw):
    return _tl_profile_env._profile_asset_owners(*_a, **_kw)


def cmd_profile_file_add(*_a, **_kw):
    return _tl_profile_env.cmd_profile_file_add(*_a, **_kw)


def _profile_file_slug(*_a, **_kw):
    return _tl_profile_env._profile_file_slug(*_a, **_kw)


def _doctor_check_profile(*_a, **_kw):
    return _tl_profile_env._doctor_check_profile(*_a, **_kw)


def _hopnap_upload_md(*_a, **_kw):
    return _tl_profile_env._hopnap_upload_md(*_a, **_kw)


def _profile_deletable_sources(*_a, **_kw):
    return _tl_profile_env._profile_deletable_sources(*_a, **_kw)

_IDEMPOTENCY_CONTRACTS = _tl_workflow._IDEMPOTENCY_CONTRACTS
_TASK_TO_WORKFLOW = _tl_workflow._TASK_TO_WORKFLOW

for _m in (_tl_workflow, _tl_release, _tl_live, _tl_zip_ingest, _tl_ocr, _tl_chunking, _tl_hygiene, _tl_nlm_ops, _tl_extract_cache, _tl_fetch_web, _tl_profile_mgmt, _tl_ingest_ops, _tl_lookup_ops, _tl_ops_misc, _tl_classify, _tl_profile_env):
    _m.bind(sys.modules[__name__])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))