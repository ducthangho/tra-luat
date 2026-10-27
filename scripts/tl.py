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
import argparse, json, os, re, sys, shutil, subprocess, tempfile, time
# v1.35.60 (ĐO: 1646 hàm tl_core có __globals__ IS namespace tl; phản chứng gate ĐỎ 2 lượt — NameError
# `unicodedata`@classify rồi `datetime`@profile_mgmt) — 5 tên dưới KHÔNG phải import thừa dù ruff báo F401.
# Hàm tách sang tl_core được RE-HOME về globals của tl.py nên tra tên toàn cục ở ĐÂY, không ở tệp gốc:
# profile_mgmt.py có `import datetime` riêng mà vẫn NameError khi tl.py thiếu. Số hàm re-home tra từng tên
# (đo 29-07-2026): unicodedata 19 · base64 9 · hashlib 3 · datetime 2 · zipfile 0 — giữ trọn mặt namespace.
# Xoá bất kỳ tên nào = NameError lúc chạy, có thể ở nhánh selftest chưa phủ. Để RIÊNG dòng cho noqa khỏi che dòng trên.
import base64, datetime, hashlib, unicodedata, zipfile  # noqa: F401 — namespace export cho hàm re-home tl_core

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
# r288 (Pha 1-0, Helper 1): LÕI kết luận giao dịch — nạp sớm cạnh deterministic/jsonio vì mọi tầng trên
# (ingest/profile/rasoat) đều dùng, và bản thân nó không import gì từ tl_core.
_tl_txn = _tl_core_import("txn")
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
EXPECT_VERSION = "2.21.2p"
# [lịch sử, đã gộp 1.24.0] 1.23.22: ROOT-CAUSE THẬT sự cố 2026-06-30 (ĐÍNH CHÍNH 1.23.21: KHÔNG mất data 766 dòng!). Thật ra config `registryDocId` trỏ NHẦM Doc legacy `1mATG` (vnd.google-apps.document) thay vì SHEET registry thật → webapp mở Doc-as-Sheet → đọc RỖNG → count=0 ẢO (data vẫn nguyên; corpus 552 là do dedup-plan −50). Template public init-config hay ghi đè về Doc legacy → tái diễn mỗi setup. FIX: (1) doctor CHẶN cứng `registryDocId == _LEGACY_REGISTRY_DOC_ID` (1mATG) → báo sửa về Sheet/để rỗng; (2) `init-config` AUTO-HEAL: blank registryDocId (base+profiles) nếu = Doc legacy → webapp auto-discover Sheet `tra_luat_registry`. (Giữ guard 1.23.21 cho ca profile registryDocId rỗng.) +1 test → 260/260. # 1.23.21: ⛔ GUARD CHỐNG CLOBBER REGISTRY NỀN (SỰ CỐ NGHIÊM TRỌNG 2026-06-30: profile dự án 'Khảo sát Luật XB' registryDocId RỖNG → webapp `regSS_` rơi nhánh BASE → manifest --touched-drive quét phình rồi profile-rebuild-registry XÓA SẠCH 766 dòng registry NỀN VBQPPL). FIX: `cmd_manifest` (--touched-drive) + `cmd_profile_rebuild_registry` CHẶN khi profile dự án có TL_REGISTRY_DOC_ID rỗng (PROFILE_REGISTRY_ID_EMPTY_WOULD_CLOBBER_BASE, rc=2) — phải tạo registry RIÊNG trước. PHÁT HIỆN từ GS: registry base = Google SHEET `tra_luat_registry` (regSS_ tìm theo tên/TL_REGSHEET_ID_AUTO), KHÔNG phải Doc 1mATG (chỉ ping/display); khôi phục = restore SHEET đó (version history Sheets), cache `tl212_reg_*` TTL 600s. +1 test → 259/259. # 1.23.20: DETECTOR `infra_in_corpus` (phát hiện khi rà 106 Luật dump) — file HẠ TẦNG (.json/.enc/secrets/nlm_sources_delta/manifest/registry) lẫn corpus=true = RÁC (vd tl_secrets.enc, nlm_sources_delta_*.json đếm như văn bản). `_is_infra_entry` (module-level, BẢO VỆ GDoc/PDF/Word) + thêm vào `tl sweep` (cờ + NEXT ACTION set corpus=false). +1 test → 258/258. # 1.23.19: COMPOSITE `tl dedup-plan` (user yêu cầu) — kế hoạch dedup TOÀN CORPUS 1 lệnh (thay chạy `hygiene plan <q>` từng cụm). Tái dùng canonical-picker của `_hygiene_groups` (reconcile_clusters `_cluster_same_doc` = CÙNG văn bản theo subject-sig + gộp sidecars .docx/.pdf cạnh GDoc). GIỮ canonical, set corpus=false bản dup (reversible). BẤT BIẾN AN TOÀN: không quarantine chính canonical / canonical của cụm khác / trùng lặp. DRY mặc định; --apply ghi reg_bulk corpus=false; review (thiếu canonical) + dups_on_nlm (còn nguồn NLM→cân nhắc xoá tay) chỉ BÁO. sweep NEXT ACTION trỏ dedup-plan. Pure `_dedup_plan`. +1 test → 257/257. # 1.23.18: FIX false-fire NLM_STATUS_MISMATCH (phát hiện khi nlm-orphans --fix-mismatch LIVE trả MISMATCH_LIVE=0 dù sweep báo 79). Whitelist status exact-match KHÔNG nhận biến thể `removed_*` (removed_superseded_by_VBHN, removed_dedup…) → false-fire + `_entry_on_nlm_live` coi NHẦM removed_* là sống (lệch still_on_nlm/ghost). FIX: `_nlm_status_known`/`_nlm_status_removed` nhận HỌ tiền tố (pushed*/synced/removed*/trash*/deleted), áp 4 site (doctor flag, _title_flags, _entry_on_nlm_live, vbhn-normalize removed). sweep NEXT ACTION: NLM_STATUS_MISMATCH = nhãn LẠ (registry hygiene) KHÔNG phải live desync. +2 test → 256/256. # 1.23.17: `tl sweep` NEXT ACTION nlm_drift TÁCH theo sub-type (phát hiện khi reconcile LIVE không giảm drift) — trước gộp 288 thành 'nlm-reconcile --apply' GÂY HIỂU NHẦM (reconcile chỉ chữa LINKAGE). Nay: NLM_NOTEBOOK_ID_MISSING→nlm-reconcile (linkage); NLM_STATUS_MISMATCH→nlm-orphans --fix-mismatch (đọc live); CORPUS_TRUE_NOT_ON_NLM→ingest-missing (job lớn, phần lớn CẤU TRÚC corpus>cap, KHÔNG về 0). # 1.23.16: DETECTOR `shared_source_id` (phát hiện khi dọn ghost NLM LIVE) — ≥2 drive_id KHÁC nhau CÙNG 1 nlm_source_id (backfill/reconcile gắn nhầm) = FALSE-LINK: xóa nguồn của row này GÃY link row kia (ca NQ42: canonical + ghost chung source_id → xóa ghost làm canonical mất NLM, phải re-push). Pure `_shared_source_id_groups` + thêm vào `tl sweep` (cờ + NEXT ACTION cảnh báo SỬA TRƯỚC nlm-reconcile/xóa nguồn). Dev cache thấy 4 nhóm. +1 test → 254/254. # 1.23.15: xử báo cáo rà 106 Luật (mục code còn lại; 5.1/5.3/5.6/4.B đã vá ở 1.23.11-14). 5.2 vbhn-check goc_hit cross-subject LỌT (14-2024 ATVSLĐ vào --goc 09-2017 Du lịch vì _disc_conflict không biết cặp) → `_vbhn_candidates`: khi ĐÃ biết subject, goc_hit phải TƯƠNG THÍCH chủ đề (sscore≥30) mới giữ. 5.5 Cowork /tmp sticky owner-nobody không ghi được → `_ensure_writable_tmpdir()` trỏ TMPDIR về CACHE/tmp ($HOME) lúc import (tempfile.* + script con kế thừa). 5.4 SKILL.md bootstrap options + cảnh báo 45s; 4.B thêm vbhn-normalize/sweep/quarantine-fix/vbhn-year-fix vào bảng CLI. +2 test → 253/253. # 1.23.14: COMPOSITE `tl quarantine-fix` (dọn nhóm B tất định) — phân loại dòng quarantine MÂU THUẪN: set_corpus_false (raw-dup .pdf/.docx gán nhầm corpus→false, AN TOÀN) + normalize_label (nhãn biến thể→QUARANTINE_CAT) tự động qua --apply; review_restore (GDoc corpus=true nghi canonical kẹt như A1/BLLĐ→KHÔNG auto, quyết tay) + ghost_nlm (quarantine còn nguồn NLM live→báo source_id, xoá tay sau verify). Pure `_quarantine_fix_items`. DRY mặc định. +1 test → 251/251. # 1.23.13: (1) MERGE HỘI TỤ bản Codex v1.23.11 (cùng vá report rà corpus) — PORT phần UNIQUE: A1 SUBJECT-GATE thật (`_name_subject_match`/`_name_subject_text`: source-map ghim canonical CHỈ trong hit KHỚP CHỦ ĐỀ, abbrev-aware BLLD/BHXH; hit generic→None+SUBJECT_MISMATCH) + `resolve_identity` +name_tokens (dedup-check 'Luật Thư viện') + vbhn-check SUBJECT_FILTER_WEAK + reg-query LIMIT_TRUNCATED rõ. GIỮ bản tôi đã verify cho A2-A5 + reg-query json-all. (2) GỠ `_parts` (chống mount-cắt-cụt — Cowork nay bootstrap qua tl_fetch zip sạch nên hết tác dụng): xoá scripts/_parts/ + build_parts.py + tl_rebuild.sh; tl_boot.py rút gọn (strip-NUL→compile→exec); `_reassemble_parts`→None (heal degrade về on-disk); edit-skill/verify-integrity bỏ build_parts. (3) COMPOSITE TẤT ĐỊNH `tl sweep`: 1 lệnh thay chuỗi 6 audit (hygiene+cat+slot+drift+vbhn-year+quarantine) → JSON/text + NEXT ACTIONS điền sẵn (pure `_sweep_report`). +4 test → selftest 250/250. # 1.23.12: 2 fix từ chạy B1 LIVE. (1) reg-query `--json` UNDERCOUNT âm thầm — mặc định cắt 60 rows → script đếm `len(rows)` thiếu (audit quarantine thấy 60/110). Nay `--json` trả TẤT CẢ rows mặc định (text vẫn cắt 60 + dòng '(hiện 60)') + cờ `truncated`. (2) hygiene scan thêm cờ TRẠNG THÁI MÂU THUẪN `quarantine_corpus_true` (trong quarantine nhưng corpus=true) + `quarantine_still_on_nlm` (quarantine nhưng còn nguồn NLM live = ghost) → surface để dọn. # 1.23.11: xử báo cáo rà corpus (nhóm A). A2: hằng `QUARANTINE_CAT` + `_is_quarantine_label_variant` + cờ hygiene scan `quarantine_label_variants` (audit hội tụ dù nhãn lệch QUARANTINE/_ZZZ — `_is_quarantine_cat` nhận mọi biến thể). A3: `slot-audit` TỰ neo `live_source_count` từ nlm CLI (+`--no-live`) → cảnh báo gap estimate↔live khỏi gọi `--physical` tay. A4: `doctor` in BREAKDOWN từng cờ (NLM_STATUS_MISMATCH/CORPUS_TRUE_NOT_ON_NLM/NLM_NOTEBOOK_ID_MISSING) + lệnh `nlm-reconcile <nb> --apply` ĐIỀN SẴN notebook id. A5: help `vbhn-check --subject` thêm cảnh báo QUOTE. A1 (source-map ghim sai canonical 'Bộ luật Lao động'→'Dân chủ 87'): KHÔNG tái hiện trên v1.23.11 với dữ liệu đại diện — gate LOW_CONFIDENCE_NAME_MATCH gốc đã null canonical khi top không strong-match; giữ gate (thử thay bằng nhóm tail-key gây regression abbrev/quarantine → revert). Cần `source-map --json` LIVE để soi nếu còn. +3 test. # 1.23.10: GUARD cat (phát hiện khi nạp THADS 106/2025 LIVE) — `register`/reg_bulk KHÔNG validate `cat` → workaround gõ tay folder RÁC '30_To_chuc_bo_may_nha_nuoc' (số 30 + tên cat 35) lọt im lặng → registry lệch folder vật lý. Nay `_is_valid_cat_value` chặn cat không thuộc taxonomy 45+2 (cả nhánh --bulk lẫn reg_upsert), rc=2, nhắc dùng `tl recat --cat <số>`. +1 test. BÀI HỌC: đổi cat LUÔN dùng recat (resolve+validate folder), KHÔNG register --bulk tên gõ tay. # 1.23.9: 2 FIX (phát hiện khi chạy vbhn-year-fix LIVE Cowork). (A) vbhn-year-fix CHỈ quét entry corpus=true — sidecar/quarantine (corpus=false) KHÔNG year-fix → hết CONFLICT GIẢ (sidecar corpus=false va sohieu với GDoc canonical cùng số; hygiene báo 'sạch' nhưng vbhn-year-fix báo conflict = mâu thuẫn do quét cả non-corpus). (B) HINT SAI: lệnh ghi in `MANIFEST_STALE_RUN_REGEN2` → `tl regen2` KHÔNG phải lệnh (chỉ có `tl manifest`; regen2 là action GAS qua `manifest --touched-drive`) → user chạy nhầm. Sửa 5 hint + dòng recat → `tl boot --refresh` (sau ghi registry sheet) / `tl manifest` (sau đổi cây Drive). +test corpus-skip. # 1.23.8: SAFEGUARD cho vbhn-year-fix (phát hiện khi soát DRY) — nếu ≥2 dòng suy ra CÙNG `NN-YYYY-VBHN-XXX` (dòng dup cùng văn bản, HOẶC 2 văn bản khác cùng số+năm) thì ghi sẽ TẠO collision MỚI → tách bucket `conflicts`, KHÔNG auto-apply (rc=1), in 🔴 CONFLICT để dedup/phân biệt tay. `_vbhn_year_fix_items` nay trả (fixable, needs_year, conflicts). +1 test. # 1.23.7: ★ BẤT BIẾN ĐẶT TÊN (user nhấn mạnh) — số hiệu VBQPPL PHẢI có NĂM; VBHN là thủ phạm (số VBHN tái dùng theo năm → collision, vd 61/VBHN-VPQH=ATTP 2025+Thuế TNDN 2026, 115/VBHN-VPQH=THADS 2025+Thi đua 2026). Lệnh MỚI `tl vbhn-year-fix [--with-name] [--apply]`: quét VBHN sohieu THIẾU năm (`NN-VBHN-XXX`) → suy năm (ngày ban hành/tên qua `_entry_issue_year`) → đề xuất `NN-YYYY-VBHN-XXX`, GHI qua reg_upsert (KHÔNG reg_bulk — sohieu là khóa immutable); ca không suy được năm → needs_year (xác minh tay). Pure `_vbhn_sohieu_inject_year`/`_name_inject_vbhn_year`/`_vbhn_year_fix_items` (test offline). + `register` cảnh báo `VBHN_SOHIEU_NO_YEAR` khi ghi sohieu VBHN thiếu năm. +3 test. (Phát hiện đã có sẵn: cờ VBHN_BARE_NUMBER/MISSING_YEAR_OR_DATE/NAME_MISSING_YEAR.) # 1.23.6: FIX (phát hiện khi KH2 Pha 2.6 recat Cowork) — `recat --apply` báo `reg_patched:0` ÂM THẦM khi Drive đã move nhưng webapp index chưa thấy row mới thêm (registry cat KHÔNG cập nhật → user tưởng xong). Nay LOUD cảnh báo stderr + rc=1 khi reg_patched < moved, chỉ rõ KHẮC PHỤC (regen2 --refresh rồi reg_bulk lại). Cùng họ "ghi im lặng" với 1.23.5. +1 test. # 1.23.5: FIX BUG (phát hiện khi KH2 Pha 2.8 chạy Cowork) — `missing-sohieu --apply` ghi reg_bulk cột `so_hieu` (có gạch dưới) → webapp BỎ IM LẶNG (đúng gotcha API_CONTRACT mục 0: khóa phải `sohieu`); apply thẳng trả patched=0 mà KHÔNG báo lỗi. Sửa items key + cols → `sohieu` (line ~8061) + help/docstring. Workaround Cowork (cols="sohieu") đã ghi 193/193; nay code gốc đúng. +1 test. # 1.23.4: ★ KH1 HOÀN TẤT — `tl relation-backfill --base <sh> [--apply]` (Pha 1.5 cuối, cho KH2 Pha 2.3): GHI quan hệ sửa đổi mà relation-check ĐÃ phát hiện (missing_links từ `_relation_audit`, tái dùng cổng footnote chống dương-tính-giả) — set `goc` cho luật SỬA, append `sua_doi` cho luật GỐC (pure `_relation_backfill_items` HỢP NHẤT sua_doi cũ + dedup, KHÔNG đè). CHỈ direct/ref-linked; subject-only → review (xác minh tay). DRY mặc định. +1 test → selftest 237/237. → TOÀN BỘ lệnh KH1 đã dựng (3 cổng + vòng lặp + dọn-corpus + nlm-orphans + relation-backfill). CÒN: cập nhật RUNBOOK/API_CONTRACT (tài liệu), KH2/KH3 (corpus). # 1.23.3: FIX DEPLOY-DISPLAY — SKILL.md header ghi CỨNG '(v1.22.70)' qua MỌI bump 1.22.71→1.23.2 (tôi quên sed SKILL.md) → bản deploy HIỂN THỊ 'v1.22.70' dù runtime đúng. Sửa SKILL.md→(v1.23.3) + GUARD selftest `skill_md_version_matches_VERSION` (bump nào quên cập nhật SKILL.md = selftest FAIL → chặn deploy). LƯU Ý vận hành: Package live khi kiểm = 1.23.0 (1.23.1/1.23.2 CHƯA push thành công — drive-push cần gws auth); verify push bằng curl Package fileId. +1 test → selftest 236/236. # 1.23.2:`tl nlm-orphans <notebook> [--fix-mismatch] [--deep]` — TỰ ĐỘNG HOÁ điều tra ghost (thay 6 vòng soi tay): đọc nguồn NLM LIVE (`nlm_cli.source_list`) ↔ registry → phân `_classify_nlm_sources` (PURE, test offline) thành REGISTERED_ACTIVE / **STATUS_MISMATCH_LIVE** (dòng registry removed* nhưng nguồn còn SỐNG = gắn nhãn SAI, vd 8 văn bản đã vá tay) / UNREGISTERED (trên NLM, không dòng registry). REPORT-ONLY; --fix-mismatch in bản vá metadata DRY (corpus=true,nlm_status=pushed) cho nhóm mislabel (KHÔNG đụng NLM/KHÔNG xóa); --deep đọc nội dung NLM lấy SỐ HIỆU header thật (vá cả sohieu cụt như '66'→'66.18/2026/NQ-CP'). +1 test → selftest 235/235. (CÒN: relation-backfill Pha 1.5 live; root-cause pipeline gắn nhầm removed_from_drive; SKILL.md/RUNBOOK/API_CONTRACT.) # 1.23.1: vá sweep-finding — `overflow-resolve` ĐỐI CHIẾU LIVE (nlm-get) thay vì registry-only: dùng MAX(registry, physical) làm slot hiệu lực (`_overflow_status`) → KHÔNG báo 'còn chỗ' giả khi vật lý vượt cap (vd base registry 279 / LIVE 315); cờ `REGISTRY_BEHIND_LIVE` lộ nguồn add thẳng CHƯA đăng ký (gợi `tl nlm-reconcile`); sửa cosmetic flag (BASE_HAS_ROOM khi base còn chỗ). `--no-live` để registry-only. (ingest-missing --apply ĐÃ physical-safe sẵn qua nlm-get.) +1 test → selftest 234/234. # 1.23.0: ★ KH1 (sửa skill sau báo cáo rà 70 Luật) — PHÁT HÀNH. Pha 1.3/III.2: `tl slot-audit --all-shards` (II.5 đếm slot TỪNG shard + cảnh báo near-full ≥270/300, pure `_slot_count_all_shards`) + `tl overflow-resolve` (II.1 kiểm shard overflow SẴN CÓ → cờ OVERFLOW_SHARD_EXISTS_DO_NOT_CREATE, chống tạo notebook nhầm; reuse `_overflow_route`) + `tl edit-skill <file> --patch` (III.2 sửa skill an toàn: assert-đếm→py_compile→write_text→build_parts, né Edit/Write mount; DRY mặc định). manifest-stale (II.4): lệnh ghi MỚI phát MANIFEST_STALE_RUN_REGEN2. canonical-not-sidecar (II.3): ĐÃ xử qua deep-resolver `_resolve_deep_target`+`_is_source_sidecar`+phạt raw-300. +3 test → selftest 233/233. ★ TỔNG KH1 (1.22.71→1.23.0): H1/H2/UTF-8/instructions--out; 3 CỔNG G1(source-verify)/G2(header-verify)/G3(cat-verify+cat-audit/recat FIX); vòng lặp frontier-expand/ingest-missing(no-new-notebook)/rasoat-loop; dọn corpus backfill-loai/sohieu-conflict/missing-sohieu; slot-audit/overflow-resolve/edit-skill. CÒN (1.23.1): relation-backfill (live, Pha 1.5); cập nhật SKILL.md/RUNBOOK/API_CONTRACT + upload Package (user-side). # 1.22.76: KH1 Pha 1.5 — `tl missing-sohieu` (đề xuất số hiệu cho dòng registry thiếu sohieu, parse từ TÊN qua `_parse_sohieu_from_name`, bỏ Mẫu/Phụ lục; DRY mặc định, --apply ghi reg_bulk so_hieu; ⚠ ĐỀ XUẤT theo tên — XÁC MINH bằng header-verify/G2; LIVE suy 194/307 dòng thiếu). +1 test → selftest 231/231. HOÀN TẤT Pha 1.5 quick-wins pure (backfill-loai+sohieu-conflict+missing-sohieu). CÒN (v1.23.0): Pha 1.5 relation-backfill (live) + Pha 1.3 (overflow-resolve/canonical-sidecar/manifest-stale/slot-audit per-shard) + III.2 edit-skill. # 1.22.75: KH1 Pha 1.5 (quick-wins pure) — `tl backfill-loai` (suy `loai` chuẩn cho dòng trống từ tên+số hiệu qua pure `_infer_loai`; DRY mặc định, --apply ghi reg_bulk; idempotent; LIVE manifest suy được 191/769) + TÁCH `SOHIEU_CONFLICT_DIFFERENT_DOC` (≥2 chữ-ký-chủ-đề KHÁC cùng số hiệu = văn bản KHÁC, NGUY HIỂM) khỏi `SAME_DOC` (sidecar) trong registry-doctor (`_subject_sig`; thêm khóa `sohieu_conflict_groups` vào schema text=json; LIVE 22 conflict/6 same trong 28 dup). +3 test → selftest 230/230. CÒN (v1.23.0): Pha 1.5 relation-backfill/missing-sohieu (live) + Pha 1.3 (overflow-resolve/canonical-sidecar/manifest-stale/slot-audit) + III.2 edit-skill. # 1.22.74: KH1 Pha 1.2 HOÀN TẤT P0 — `tl ingest-missing` (nạp backlog corpus chưa NLM → source_add+reg_bulk; IDEMPOTENT + checkpoint resume; DRY mặc định; định tuyến theo chỗ trống base→overflow shard SẴN CÓ; BẤT BIẾN `_overflow_route` KHÔNG BAO GIỜ tạo notebook (đầy→BLOCKED hỏi user); pure `_ingest_missing_select`/`_overflow_route` test offline) + `tl rasoat-loop` (orchestrator VÒNG LẶP KHÉP KÍN report-only: SEED→frontier-expand→mở rộng đệ quy in-corpus đọc nguyên-văn KHÔNG RAG→dedup seen chống lặp→hội tụ dry_rounds≥K; xuất GAP ngoài-corpus + in-corpus-chưa-NLM; pure `_rasoat_dedup_push`). +4 test → selftest 228/228. CÒN (v1.23.0): Pha 1.3 (overflow-resolve/canonical-sidecar/manifest-stale/slot-audit per-shard) + Pha 1.5 (backfill-loai/sohieu-conflict/relation-backfill/missing-sohieu) + III.2 edit-skill. LƯU Ý: ingest-missing/rasoat-loop nhánh mutate/expand-live CHƯA test trên dev (không NLM cred) — lần --apply đầu chạy Cowork batch nhỏ. # 1.22.73: KH1 Pha 1.2 — `tl frontier-expand <gdoc|sohieu>` (vòng lặp rà soát): trích MỌI dẫn chiếu (xref+footnote+inline) → ứng viên FRONTIER dedup theo số hiệu + ưu tiên (amending>VBHN>dẫn-chiếu) + cờ in_corpus; `missing_in_corpus` = đầu vào ingest-missing. Pure `_frontier_candidates` (test offline) + `_frontier_doc_text` reader; DISCOVERY/REPORT-ONLY, KHÔNG RAG; --text-file offline. +2 test → selftest 225/225. CÒN (v1.23.0): ingest-missing (mutate NLM, no-new-notebook), rasoat-loop (orchestrator); Pha 1.3; Pha 1.5. # 1.22.72: KH1 Pha 1.2 — DỰNG 3 CỔNG XÁC MINH G1/G2/G3 (dựng SẠCH, KHÔNG dùng bản agent tiêm đã revert). G3: helper pure `_load_linhvuc`/`_cat_taxonomy`/`_infer_cats_text`(suy cat theo NỘI DUNG alias, whole-word)/`_cat_boundary_rule`(ép quy_tac_ranh_gioi: BHXH/BHYT→02, đầu-tư-công/hải-quan→26, sửa≥2 luật→46, điều-ước→23, Đảng→00) + `tl cat-verify <gdoc|sohieu>` (read-only, --text-file offline) + FIX `cat-audit` (confidence/RULE/taxonomy-45+2/--strict) + FIX `recat` (BOUNDARY_CONFLICT advisory + --force-cat). G2: `_extract_header_facts` (ngày+cơ quan, pure) + `tl header-verify [--all/--sohieu/--drive-id/--cat] [--fix-suggest] [--strict]` (batch _verify_header_match, READ-ONLY, bắt DRIFT 775 dòng; KHÁC title_mismatch=metadata nội bộ). G1: `_content_md5` (NFC, pure) + `_official_rank` + `_DISCOVERY_SITES` re-rank OFFICIAL-FIRST (vbpl>congbao>luatvietnam>thuvienphapluat) + `tl source-verify <sohieu|gdoc>` (content_md5 + SOURCE_DISCREPANCY + nguồn official-first đối chiếu, --text-file offline). +14 test → selftest 223/223. CÒN (v1.23.0): rasoat-loop/frontier-expand/ingest-missing; Pha 1.3; Pha 1.5. # 1.22.71: KH1 (Pha 1.1/1.4) thực thi sau báo cáo rà 70 Luật. H2 `registry-doctor` text=JSON schema (dòng text SINH TỪ `_DOCTOR_SUMMARY_KEYS` → `build_doctor_summary`/`format_doctor_text`, hết lệch nhãn duplicate_sohieu↔_groups/title_mismatch↔_candidates/rows↔count). H1 `reg-query --json` rc=0+envelope KHÓA bằng test (không tái hiện ở canonical; rc=1 trong log = confound redirect/&&/bản cũ). III.1 `os.environ PYTHONUTF8=1`/PYTHONIOENCODING truyền xuống MỌI script con (hết UnicodeEncodeError 'charmap' gen_instructions.py… console Windows) + gen_instructions.py reconfigure standalone. III.3 `tl instructions --out <file>` ghi UTF-8 ra file. +3 test → selftest 209/209. (LƯU Ý: workflow thiết kế v1.23 từng tiêm nhầm header-verify/cat-verify vào canonical → ĐÃ revert, sẽ dựng lại CÓ REVIEW.) CÒN (v1.23.0): rasoat-loop/frontier-expand/ingest-missing; Pha 1.3 overflow-resolve/canonical-sidecar/manifest-stale/slot-audit; Pha 1.5 backfill-loai/sohieu-conflict/relation-backfill; cổng G1/G2/G3. # 1.22.70: ★ HỢP NHẤT bản Codex v1.22.69 (CONVERGENT — 2 nhánh cùng vá 13 lỗi 2 báo cáo, KHÁC code) + vá LOG RÀ MỚI (Nhóm A-E đa-profile) + LARGE-FILE SPLIT. MERGE: GIỮ bản Claude làm base (verify 197/198, có H/D/G/2.2 mà Codex THIẾU) + PORT phần Codex MẠNH HƠN: (1) DEEP-RESOLVER `_resolve_deep_target`+`_entry_mime`/`_entry_google_doc`/`_entry_raw_no_gdoc`/`_deep_entry_rank` cho extract/xref/footnote-map (ưu tiên GDoc native theo MIME + corpus + NLM-live; tên DÀI toàn chữ-gạch-dưới KHÔNG bị nhận nhầm DriveId → bug C TRỌN VẸN); (2) `_classify_ref` kiểm VBHN-COVERAGE TRƯỚC TYPO/MISSING (số hiệu gốc đã có VBHN → OUTDATED); (3) ENTRY_RAW_NO_GDOC rc=2 + ok:false (đúng yêu cầu báo cáo: chỉ-raw → rc≠0). NHÓM A-E (log đa-profile): B(NGHIÊM TRỌNG) `_ingest_target`/`nlm-add`/`nlm-query` push/query nhắm NOTEBOOK CỦA PROFILE (TL_NOTEBOOK_ID) — hết đẩy nhầm VBQPPL base khi `--profile NQ36` (+nlm-add/nlm-query nạp apply_profile_offline). A1 `profile-create --apply` GHI BỀN config.profiles.<name> (`_persist_profile_config` merge) → profile-info hết fallback VBQPPL. A2 next-steps cấm copy sheet VBQPPL tay (orphan), dùng `manifest` tạo registry rỗng. C1 `nlm-reconcile` BẮC CẦU gdoc↔source_id (`_nlm_source_drive_id` + link_candidates: nguồn live khớp drive_id/số hiệu của dòng registry thiếu source_id → backfill, hết 'unregistered' giả). C2 `register --nlm-notebook-id` (khỏi backfill-notebook riêng). C3 `backfill-notebook` khóa ĐÚNG NGUỒN: --src-ids→nlm_source_id, --drive-ids→drive_id (hết lệch khóa). D1 cảnh báo profile non-default + categories=inherit (văn bản vào cây chung VBQPPL). D2 `regen2` LOẠI registry/manifest/orphan (mime spreadsheet/json + tên + registryDocId/manifestId) khỏi scan own (hết 3 dòng corpus rác, count 8→5). D3 `reg-delete --force` (đã có) + thông điệp rõ. E1 `nlm_cli._strip_keyring` lọc 'Using keyring backend' khỏi stdout/stderr (hết vỡ json.loads). E2 `reg-query --refresh` (đã có) + help nhắc refresh sau khi ghi sheet. LARGE-FILE: `ingest-local` cổng HỎI TÁCH file > ~1.2MB (NLM_LARGE_SRC_BYTES, --large-threshold) → DỪNG gợi ý tách theo Phần/Chương/Điều (chất lượng RAG cao nhất), `--allow-large` để nạp nguyên (+SKILL.md doctrine). RÀ SOÁT ĐỐI KHÁNG (review+verify) gia cố 14 phát hiện: Group B `_resolve_nlm_notebook` (profile DỰ ÁN thiếu notebookId → ERROR, KHÔNG fallback VBQPPL base — vá GỐC bug B, guard cũ là dead-code vì base luôn truthy) áp nlm-add/query/get/reconcile/cross/ingest-local; C1 link theo số hiệu CHỈ khi DUY NHẤT (số VBHN tái dùng → bỏ qua, hết false-link); cmd_extract positional+--sohieu → ƯU TIÊN --sohieu; `_persist_profile_config` ghi NGUYÊN TỬ (temp+os.replace); `_is_infra_file` chặn false-positive (văn bản GDoc/PDF KHÔNG bao giờ là infra); `_strip_keyring` JSON-safe (chỉ bỏ dòng nhiễu THUẦN, không nuốt thân JSON có cụm keyring); large-file gate ra STDOUT. +6 test → selftest 206/206. # 1.22.69: vá 13 lỗi CÔNG CỤ từ 2 BÁO CÁO RÀ 71+105 LUẬT. A `tl status` verdict→rc=0 (REVIEW/ADD/SKIP = PHÁT HIỆN dữ liệu ≠ lỗi lệnh, hết phá &&/CI; +`--strict` mirror xref; preingest_gate.verdict_exit). C/P0-1 resolver đọc sâu: `_entry_score` PHẠT -300 file THÔ (.docx/.pdf/.html) → GDoc native THẮNG sidecar CÙNG số hiệu (hết xref/footnote im-lặng stdout-rỗng-rc0 bỏ sót ≥6 VBHN); ENTRY_RAW_NO_GDOC in STDOUT (caller agentic THẤY); `_resolve_base_gdoc` fallback drive_id khi sohieu rỗng. B+P1-3 xref: `extract_refs` DEDUP theo SỐ HIỆU (1 phán quyết/số hiệu/run — hết MISSING+MISMATCH mâu thuẫn + phantom 'DCHIẾU 258 này có hiệu lực…' do bắc-cầu mệnh-đề-chuyển-tiếp) + `_clean_ref_name_phrase` cắt prose (GIỮ tên luật thật 'Thi hành án dân sự'). P0-2 `DOC_TEXT_SOHIEU_TYPO` KHÔNG bắc cầu QUA HỌ loại VB (`_doctype_family`: QH≠NQ-TW≠KL-TW≠NĐ-CP — tái dùng số+năm hợp pháp; CÙNG họ QH14↔QH15 vẫn flag). P1-4 source-map: >1 VBHN CÙNG số hiệu KHÁC chủ đề → canonical=None + VBHN_REUSE_AMBIGUOUS_NO_CANONICAL (đòi --subject/năm; CÙNG chủ đề/nhiều version vẫn chốt). P1-5 amendment-detector: LOẠI văn bản PHI quy phạm (sohieu=∅ + 'góp ý/kiến nghị/ý kiến'); PAUSE_AND_ASK_USER CHỈ khi có ứng viên MANG SỐ HIỆU hợp lệ (sohieu=∅ vẫn liệt kê, confidence=low). P2-6 vbhn-check: CONTENT_VERIFY_REQUIRED chỉ khi collision CỦA CHÍNH số hiệu ứng viên (KHÔNG corpus-wide → hết 86 cờ máy móc); verified+năm+duy-nhất+không-tự-collision → VBHN_METADATA_OK. H `tl doctor` cảnh báo TRÔI registry↔NLM (đếm cờ OFFLINE từ cache → gợi ý `tl nlm-reconcile`, KHÔNG chặn/mạng). D `_read_doc_text`+`cmd_xref` TÁI DÙNG cache `extract_<gid>.txt` (Bộ luật Dân sự hết export lại 3 lần→timeout). E `standardize_name.normalize_name` bỏ đuôi .doc/.docx/.pdf khỏi tên CHUẨN (GIỮ ở tên FILE gốc). G `hygiene` bucket `sidecar_corpus_fix` (.docx cạnh GDoc mà corpus=true → đề xuất SET_CORPUS_FALSE). P2-7 chuẩn hoá ENUM `loai`/`hieuluc` lúc register (`_normalize_loai`/`_normalize_hieuluc`) + bucket hygiene `loai_noncanonical` (KHÔNG nhồi `_title_flags` → tránh nhiễu source-map). 2.2 nlm PATH: `nlm_cli` nối ~/.local/bin+user-base bin vào PATH (shutil.which + subprocess env); `doctor` dùng `nlm_exe()` (hết báo đỏ giả); `nlm-install` ghi PATH bền ~/.profile/~/.bashrc (POSIX). +14 test → selftest 194/194. HOÃN P2-8 (tách MISSING ngoài-phạm-vi-corpus vs resolver-trượt — cần enrich manifest). RÀ SOÁT ĐỐI KHÁNG (workflow review+verify) gia cố 9 phát hiện: cmd_status dùng inspect.signature thay except-mù + GIỮ ngữ nghĩa --strict ở fallback (rc=2→1); `_entry_score` chỉ phạt raw CHƯA-trên-NLM (raw đã-push NLM = canonical thật, không hạ oan); P1-4 `_subj_keys` chỉ đếm tail CHỦ-ĐỀ-RÕ (bản tên-trơ không gây false-ambiguity); P1-5 gate góp-ý theo SỐ HIỆU REGISTRY (file 'Góp ý Luật 64/2020' có số trong TÊN vẫn bị loại); `_normalize_loai` gộp mọi ký tự lạ (kể cả ngoặc); cmd_register log khi chuẩn hoá loai/hieuluc; preingest_gate main() thêm --strict. # 1.22.68: rà 133+81 LUẬT (2 log live) — vá robustness phần A. P1 RAW-ENTRY PRECONDITION (gốc chung log2 A1/A2/A3): xref+footnote-map gặp entry THÔ (.docx/.pdf/.html chưa convert GDoc) → ENTRY_RAW_NO_GDOC rc=0 + thông điệp gọn (thay rc=2/JSON-lỗi-thô/stdout-rỗng/rò "Export only…"); `_is_raw_no_gdoc_name`/`_raw_no_gdoc`/`_emit_raw_no_gdoc` THỐNG NHẤT .docx↔.pdf. P2 FOOTNOTE DEDUP (log1 A2): resolve_footnote_amendments GOM dieu_level_amendment_map theo (dieu,khoan,diem,amending_sohieu) — hết 47 dòng pending trùng (Đ73K1 ×3); footnote_defs giữ ĐỦ marker + footnote_raw_count. P3 BASE_NO_CLUSTER (log1 A1): rasoat-chongcheo CỜ RÕ khi base ngoài cụm E2 (61/133 trước no-op IM LẶNG) → dựa xref/footnote-map cấp Điều. P4 DEDUP related theo sohieu (log1 A6, hết 85-2015 ×4). P5 missing_in_corpus→`unresolved_refs`+note (log1 A5: CHƯA kết luận vắng mặt, khớp exists=UNKNOWN_NOT_ABSENT). A4 BASE_UNRESOLVED khi base tên/file thô không số hiệu. P7 strip keyring khỏi gws_bridge error (log2 A3). +2 test → selftest 179/179. CÒN (data/feature): mở rộng subject_clusters 45 chủ đề; parser khoản-điều-thêm (6a/16b, A3 log1 nhỏ); Cowork batch-checkpoint (A4 log2); GAS serial (A5 log2, frozen). + `drive-push --name`/`--rename-to-file` (đổi tên file Drive THEO TÊN FILE upload, GIỮ fileId — qua gws_bridge.rename có ASSERT). # 1.22.67: rà 59 LUẬT (log live) — vá 6/7 lỗi CÔNG CỤ (phần A). A1 `tl extract <số hiệu>` (vị trí) HẾT 404 giả: positional không-phải-gdoc-id(≥20 ký tự alnum)→tự định tuyến --sohieu (+SKILL.md). A2 vbhn-check suy subject SẠCH: `_clean_subject_text` bỏ hậu tố `_HL<ngày>`/goc/SuaDoi/ngày-trơ → query QT-5 web hết "thu do hl2026 07 01 hợp nhất" (đặt `_HL_SUFFIX_RE`, KHÔNG clobber `_HL_DATE_RE` thân-văn-bản — bắt được name-collision). A3 exit-code: xref/vbhn-check rc=0 khi CHẠY OK kể cả có MISSING/MISMATCH/no-hit (phát hiện ≠ lỗi lệnh, không phá &&/CI); `xref --strict` mới rc=1 (+SKILL.md). A4 extract cảnh báo chạm CAP export ~200k ký tự (văn bản dài có thể bị CẮT → cache-build). A6 `_strip_keyring_noise` lọc 'Using keyring backend' khỏi output gws subprocess. A7 `CONTENT_VERIFY_REQUIRED` CHỈ bật khi rủi-ro-tái-dùng-số/thiếu-metadata (>1 ứng viên/collision/bare-number/missing-year); metadata RÕ+DUY NHẤT → `VBHN_METADATA_OK` (giảm 37/59 cờ máy móc). A5 (GAS tuần-tự, không scale) = giới hạn webapp FROZEN, không sửa client. +4 test → selftest 177/177. # 1.22.66: HỢP NHẤT bản Codex v1.22.65 (cùng rẽ từ v1.22.64 — 2 nhánh CÙNG vá batch-2 run-log, KHÁC code). GIỮ bản Claude làm base (đã verify 173/173 + có `status_pending` PENDING_AMENDMENT_NOT_IN_VBHN + cụm `dau_tu_PPP` mà Codex THIẾU). PORT 2 cải tiến robustness CHỈ-CÓ-Ở-CODEX: (1) vbhn-check/vbhn-verify nhận POSITIONAL `target` (tương thích runbook cũ: `tl vbhn-verify "14/VBHN-VPQH"` tự định tuyến text-file/gdoc-id/sohieu qua `_read_verify_text`; `tl vbhn-check "84/2015/QH13"`→goc/subject); (2) reg-query --json ENVELOPE chuẩn {ok,schema:reg-query.v2,count,limit,rows,entries} (cả rows+entries cho mọi parser). Các fix batch-2 TRÙNG (doctype/PPP-alias/sidecar/issue_year-goc/dedup-VBHN-first/xref-typo/vbhn-verify-json/relation-check) GIỮ bản Claude đã verify-live (Codex impl khác nhưng chưa verify). Codex thiếu status_pending → giữ bản Claude. selftest 173/173. # 1.22.65: vá 6 RUN-LOG batch-2 (workflow điều tra+verify đối kháng trên COPY CÔ LẬP — canonical md5 NGUYÊN, agent KHÔNG đụng được). 10 fix: srcmap_name_resolution (query nêu "Luật/Bộ luật"→ƯU TIÊN hit tier≥Luật `_query_doctype_tier`, hết chốt NĐ/TT: "Luật Đầu tư"→VBHN_03 KHÔNG NĐ; PPP≡"đối tác công tư" vào _ABBREV_MAP→VBHN_123; LOW_CONFIDENCE hết over-fire khi có hit-strong tier-Luật); issue_year_goc_token (`_strip_goc_token`+reject năm-bản-gốc: VBHN_123 hết issue_year=2020 từ token goc_64-2020); dedup_vbhn_first (dedup áp VBHN-first qua goc-chain dù KHÁC số hiệu: 64/2020→canonical VBHN 123, gốc SUPERSEDED); relcheck_footnote_only_fp (chỉ giữ luật THỰC SỰ sửa base, hết bơm FOOTNOTE_AMENDMENT_NOT_IN_CORPUS từ dẫn-chiếu/chuyển-tiếp); status_pending_vbhn (preingest SKIP→USE_VBHN nay cảnh báo PENDING_AMENDMENT_NOT_IN_VBHN khi VBHN ra đời TRƯỚC sửa-pending); corpus_nlm_sidecar_fp (`_dup_of_live_sibling`: không flag CORPUS_TRUE_NOT_ON_NLM cho sidecar-raw khi anh-em GDoc đã trên NLM); relcheck_json_types (int→`amendment_candidates_subject_filtered_count`); vbhn_verify_json_schema (`_vbhn_verdict`→field verdict/official/provisional + populate head_sample); xref_sohieu_typo (`_classify_ref`→DOC_TEXT_SOHIEU_TYPO khi số hiệu near-match KHÁC mã cơ quan, vd 41/2024/QH14 vs QH15); cluster_ppp (THÊM cụm dau_tu_PPP base 123/VBHN). SKIP: xref_alias (false-alarm), regquery_json+skill_cli (ĐÃ đúng trên v1.22.64 — log là DEPLOY-LAG zip Drive v1.22.35). +10 test → selftest 173/173. # 1.22.64: vá 6 RUN-LOG (workflow điều tra+verify đối kháng 16 issue → áp 15 fix, 1 reject-trên-cơ-sở). name_rank_collision (CHÍNH): source-map/exists "Luật Dân số/Việc làm/Phí lệ phí/BLLĐ" HẾT chốt SAI canonical (Dân chủ/NLĐ-nước-ngoài/Học phí/ATVSLĐ) — `_name_strong_match` + gate `LOW_CONFIDENCE_NAME_MATCH` (canonical=None khi khớp-MỜ) + `_name_phrase_match` ≥2-token (reg-query --name hết match-all 87→2); LIVE 3/4 nay chốt ĐÚNG, 1 LOW_CONFIDENCE. cluster BHYT neo `y_te_kham_chua_benh` (subject_clusters.json, hết lao_dong). vbhn-verify: HEADER_NOT_CLEAR nhận số-hiệu "NN/VBHN-" + ASSEMBLED CHỈ soi TÊN (hết "không đúng" thân→ASSEMBLED giả). status→USE_VBHN (41/2024→19/VBHN). CORPUS_TRUE_NOT_ON_NLM suppress khi nlm_status=removed_*. footnote `_multi_diem` ("điểm c và d"). `_strip_font_runs` (bỏ dòng "Times New Roman"). relation-check --json preamble→stderr + skip backfill cho quarantine. `tl up` fallback init-config. `_scan_inline_amendments`+E1 LIEN_DOMAIN (Điều 53 sửa luật khác cụm). sohieu-exact ưu tiên fuzzy. REJECT đúng: vbhn_year (sẽ regress year-reuse). +13 test → selftest 164/164. (⚠ vài agent workflow vi phạm "no-edit" → ĐÃ revert clean v1.22.63 + áp lại CHỈ patch đã-verify thủ công.) # 1.22.63: ★ HỢP NHẤT 2 nhánh v1.22.62 (Codex ⊕ Claude, đổi xứng) — (A·Codex) vá log hygiene/NLM/pending: tên "Luật X"↔canonical, footnote-map body_effective_dates (pending hết 0 giả), hygiene lọc OMNIBUS_NARROW khỏi query hẹp + không emit cluster canonical=None, reg-query/summary nlm-live-aware + cờ CORPUS_TRUE_NOT_ON_NLM/NLM_NOTEBOOK_ID_MISSING. (B·Claude) `tl up` BOOTSTRAP TẤT ĐỊNH 1-lệnh (config→gws cred+binary→nlm→manifest→readiness; helper CHUNG `_ensure_gws_nlm` cho init-config+up) + `tl confirm`/`_verify_header_match` (ĐỌC HEADER xác minh sohieu/tiêu đề/loại/cat khớp tên+thư mục → nhãn registry.verified; source-map/dedup TIN entry confirm, bỏ DIRTY/WARN) + upload-flow `_upload_mime_ext` (.doc/.pdf upload MIME THẬT → Drive organize convert server-side). selftest 153/153 (147 Codex + 6 Claude). # 1.22.62: vá log hygiene/NLM/pending — tên luật dạng "Luật X" khớp canonical đuôi "X"; footnote-map đọc thêm Điều hiệu lực trong thân luật gốc (body_effective_dates, pending không còn 0 giả); hygiene plan lọc OMNIBUS_NARROW_TITLE_CHECK khỏi query chủ đề hẹp và không emit cluster apply với canonical=None; summary/reg-query phơi nlm_source_id+nlm_notebook_id live-aware, flag CORPUS_TRUE_NOT_ON_NLM/NLM_NOTEBOOK_ID_MISSING. 1.22.61: vá log Chat/Cowork — #2 (CHÍNH: "Chat không cài gws+nlm từ đầu") init-config --from-public GỘP gws BINARY (gws-bootstrap-cowork → find/GHI hết FALLBACK→GAS) + cờ --nlm (uv-install+auth) = 1 lệnh bootstrap đủ; SKILL.md startup MỌI env dùng `--from-public --nlm`; --no-binary để chỉ-cred. #1 (NGUY HIỂM) exists/source-map: VBHN-first redirect CHỈ khi query LÀ BẢN GỐC (base = năm nhỏ nhất chuỗi goc, `_vbhn_base_key`) — 114/2025 Phòng bệnh (luật-sửa NẰM TRONG chuỗi VBHN thuốc lá) hết bị chốt canonical=VBHN thuốc lá; thêm bucket `amends_vbhn` + cờ AMENDS_OTHER_VBHN/MULTIPLE_VBHN_BASE. #3 source-map dương-tính-giả: `_vb_tier_rank` chặn SAI THỨ BẬC — NĐ/TT (118/2016/NĐ-CP) KHÔNG thể 'sửa đổi' Luật → hết AMENDMENT_CANDIDATE+PAUSE giả (đọc loại cả từ TÊN khi sohieu rỗng; base=tier cao nhất nhóm). #5 source-map NỔI `PENDING_FUTURE_EFFECT` + pending_future_count (đếm VB hiệu-lực-tương-lai, rẻ-không-footnote-map). +7 test → selftest 140/140. # 1.22.60: log rà BHYT (workflow điều tra+verify đối kháng) — #5 extract --sohieu khớp entry sohieu-RỖNG qua _sohieu_key_entry (parse từ TÊN '114_2025_QH15_658530'); #1 gws_bridge.rename ASSERT đọc-lại-tên (hết nuốt-lỗi-im-lặng rename 200-nhưng-không-đổi); #4 footnote-map _footnote_rel_kind = CROSS_CUTTING (omnibus 35/2018) / PARTIAL_REPEAL (bãi-bỏ-cục-bộ 32/2013) → hạ ưu tiên; #3 preflight TỰ KHÁM PHÁ overflow notebook từ registry (row_kind=overflow) khi config trống/placeholder (phòng thủ; config canonical đã có id thật). #2 slot over-count: đã sạch sẵn (L5), "329" trong log là GAS server-side. selftest 133/133. 1.22.59: log rà BHYT — B1 subject_clusters.json THÊM cụm `y_te_kham_chua_benh` (base 40/VBHN-VPQH BHYT + KCB 15/2023 + Phòng bệnh 114/2025 + Dược + ATTP) → rasoat-chongcheo BHYT neo ĐÚNG cụm y tế (trước neo nhầm lao_dong_xa_hoi); B3 cờ OMNIBUS hết false-positive trên luật-sửa TÊN-SỐ-TRƠ (chỉ flag khi chủ đề RÕ + khác lĩnh vực, ≥2 token); B5 `_summ_entry.nlm` = LIVE (`_entry_on_nlm_live`, False nếu removed) → relation-check khớp reg-query; B6 message gws fallback PHÂN BIỆT thiếu-cred vs thiếu-binary. 1.22.58: B1 GWS — `_read_doc_text` ƯU TIÊN direct-media EXPORT text/plain bằng CRED (KHÔNG cần binary gws → extract/footnote-map hết rơi GAS ở Cowork khi đã gws-auth-load; B5 hết spam); init-config đổi thông điệp "gws cred ✓ (direct-media đọc; find/ghi cần gws-bootstrap-cowork)" hết hiểu nhầm "BẬT". locate FALLBACK webapp gắn LOW_CONFIDENCE/NO_EXACT_SOHIEU (Cowork: locate 58/2014 → fulltext lạc đề). `_entry_subject_text` BỎ `cat` (nhãn folder '02_Bao_hiem' làm mọi entry khớp 'bảo hiểm' giả) → relation-check vbhn_candidates 14→3 (BHXH/KDBH/ATVSLĐ). 1.22.57: ★ GỐC RỄ "subject filter quá lỏng" (phát hiện khi chạy mục B live) — `_subject_score` CHỐNG nhiễu từ-phổ-biến: token-overlap chỉ tính ĐỦ khi entry chứa CỤM-ĐẦU PHÂN BIỆT của chủ đề ('bảo hiểm'='baohiem'); nếu không (chỉ trùng 'bảo/hội' lẻ ở từ-khoá) → 0 điểm. → relation-check vbhn_candidates hết kéo Luật Xuất bản/Người cao tuổi/Thanh niên/Công đoàn (sscore 40→0); BHXH=140, BHYT=0(disc), giữ KDBH=60. 1.22.56: vá log rà BHXH (Chat+Cowork) — (regression) `locate` cụm danh từ ('bảo hiểm xã hội') KHÔNG còn bị coi là số hiệu → hết LOW_CONFIDENCE/NO_EXACT_SOHIEU giả (gate `_looks_like_sohieu_query`); `tl rasoat worksheet` TỰ dựng cache nếu thiếu (`_rasoat_autocache_worksheet`→`cache-build`, resolve gdoc từ manifest; --no-auto-cache để tắt) + message worksheet trỏ `tl cache-build`; `_find_amendment_candidates` thêm loại-trừ-chéo `_disc_conflict` (BHYT/BHTN khác BHXH); SKILL.md BƯỚC 0 TÁCH `--setup` (core nhanh) khỏi nlm (né timeout 45s Cowork). 1.22.55: #8 HỢP NHẤT footnote-map vào relation-check + rasoat-chongcheo — TỰ đọc nguyên văn base VBHN (auto-footnote, `_resolve_base_gdoc`, tắt --no-auto-footnote) → 2 lệnh nêu footnote_amendments thay vì rỗng; #11 cờ OMNIBUS_CROSS_DOMAIN (`_omnibus_cross_domain_note`): luật sửa có tên khác lĩnh vực base (84/2025 Thanh tra sửa BHXH = sửa-nhiều-luật) → cảnh báo đọc nguyên văn, KHÔNG hiểu nhầm lỗi tên. +test omnibus_cross_domain_flag. 1.22.54: ★ GỐC RỄ tên VBHN VIẾT TẮT — `_expand_abbrev`/`_ABBREV_MAP` (BHXH≡bảo hiểm xã hội, BHYT/BHTN/BLHS/BLLĐ…) nối vào `_token_set`+`_disc_conflict` → source-map/relation-check/reg-query/locate khớp đúng VBHN_19…BHXH (trước nhặt nhầm bản gốc 41/2024 viết-đầy-đủ đã quarantine). #3 extract: phân biệt CẮT-CỤT (export cap ~200k) vs sai cấu trúc → chỉ `tl cache-build --gdoc-id` lấy toàn văn. #10 locate: cờ LOW_CONFIDENCE/NO_EXACT_SOHIEU khi truy vấn số hiệu chỉ khớp-mờ-tên (vd 142/2025→VBHN_74 Đấu thầu). 1.22.53: log rà BHXH — A3 relation-check `_vbhn_candidates` KHÔNG nhận VBHN trùng-NĂM khác lĩnh vực (year-một-mình cần subject≥30; +disc_conflict) → hết VBHN_43 Xuất bản lọt vào BHXH; A4 `_cluster_for_base` reverse-map qua THÀNH VIÊN cụm (số hiệu VBHN 19/VBHN-VPQH → cụm, trước trả ∅); B1 rasoat alias --sohieu→--so-hieu (worksheet) / --file→--in (phuluc); B2 `tl cache-build <sh>` wrapper ingest_to_cache.py (sinh docs/<sh>--consolidated.json); B3 ingest_to_cache.py tự nạp webappUrl/token từ config/env. 1.22.52: TRA-THEO-TÊN âm-tính-giả (log Cowork #2/#3) — `_name_subset_match` token-subset (bỏ doctype/sốhiệu) cho source-map/locate/reg-query: 'Luật Bảo hiểm xã hội' KHỚP 'VBHN_19-VPQH_Bao_hiem_xa_hoi' (substring liền thất bại vì luat/vbhn/19 chèn giữa); reg-query --name trước CHỈ substring CÓ DẤU → 0 kết quả, nay khử dấu+token-subset. `_disc_conflict` chuẩn hoá underscore (BHXH↔BHYT đúng cả tên file). `_nlm_display` status-aware (locate hết báo nlm=Y khi removed → khớp reg-query). +test name_subset_match_vbhn/source_map_name_finds_vbhn_not_quarantine. 1.22.51: (A) ENV THỐNG NHẤT Chat=Cowork=Code — gỡ doctrine "chat hạn chế": nlm CLI BẮT BUỘC mọi env, gws-bootstrap BỎ QUA tải binary nếu gws đã có (--force ép), Chat dùng uv+python≥3.11 sẵn (không tải Drive). (B) footnote-map nhận "Cụm từ '…' được BỎ/THAY THẾ theo…" (84/2025 hết vô hình, +test footnote_remove_phrase_amendment); subject-score LOẠI TRỪ CHÉO BHXH↔BHYT↔BHTN (chung "bảo hiểm" ≠ cùng chủ đề, +test subject_bhxh_not_bhyt). 1.22.50: vá log Chat — B1/B2 `gws-auth-load`/`nlm-auth-load` + `init-config --from-public` tự bật gws từ cred PUBLIC (public-curl, KHÔNG cần master key); B3 gom log [FALLBACK→GAS] 1 lần/phiên (hết spam mỗi read); relation-check LỌC ứng viên chỉ-trùng-chủ-đề khỏi amendment_candidates (giảm dương-tính-giả 108/2026); B5 xref OUTDATED nêu RÕ số hiệu VBHN thay thế + SOHIEU_MISMATCH→VBHN ghi "đúng, trỏ bản mới". (B4 phantom-217 đã có test footnote_citation_not_amendment.) 1.22.49: SKILL.md §1 BƯỚC 0 — Cowork dùng KHỐI INLINE (curl zip public + unzip + chạy tl_fetch.sh SẠCH TRONG ZIP) vì mount cắt cụt CẢ scripts/tl_fetch.sh → `sh scripts/tl_fetch.sh` đường-mount hỏng. CẤM inspect/confirm truncation/dig-recovery (đã biết mount cắt). 1.22.48: GHI RÕ gws Cowork = BINARY MUSL-STATIC (đã verify static-pie, không GLIBC dep → chạy glibc 2.35) qua `gws-bootstrap-cowork` public-curl; CẤM `npm i -g @googleworkspace/cli` (bản GNU cần GLIBC 2.39, Cowork glibc 2.35 → không chạy). SKILL.md + help string. 1.22.47: nlm-install HẾT STALL ASTRAL — `uv tool install --python 3.11` chạy với UV_PYTHON_DOWNLOADS=never (cấm tải python từ astral/GitHub CDN bị Cowork chặn): system có 3.11→dùng ngay, chỉ 3.10→FAIL TỨC THÌ→rơi Python public-curl Drive; bỏ `uv python install 3.11` thừa. 1.22.46: BOOTSTRAP TỐC ĐỘ — `_fast_drive_fetch` ưu tiên PUBLIC-CURL (drive.usercontent) → direct-media → GAS, có ĐO THỜI GIAN ([fetch] log); PY311 + gws binary tải public-curl (hết kẹt GAS 31MB); tl_fetch.sh cài uv TRƯỚC (pip PyPI, astral chặn) rồi gws/nlm; rút timeout astral uv-python 420→90s (fail nhanh → Drive-public). 1.22.45: SKILL.md §1 BƯỚC 0 — Cowork ƯU TIÊN `sh tl_fetch.sh --setup` LÀM LỆNH ĐẦU TIÊN (tải bản sạch, KHÔNG đụng mount/_parts); CẤM chạy tl_boot/verify-integrity/build_parts/_parts TRƯỚC khi tl_fetch lỗi; tách rõ đường LOCAL A1–A3. 1.22.44: PACKAGE PUBLIC BOOTSTRAP — config v2 + creds (gws/nlm/secrets/binary/py311) ở Drive/Package (anyone-with-link). `init-config --from-public` + tl_fetch.sh curl CONFIG(apps script)+gws cred TRƯỚC (KHÔNG cần Drive MCP); uv-first cho nlm; Cowork tải zip skill; tl_boot loud-fail exit≠0 khi cắt cụt (B2); tl_rebuild.sh OUT mặc định $HOME (B4). 1.22.43: `tl drive-push <zip> [--file-id]` — cập nhật NỘI DUNG file Drive GIỮ fileId (gws update_content) → đẩy bản ship mới mỗi lần mà KHÔNG đổi fileId; SKILL_FILEID baked. 1.22.42: BUNDLE skill+gws — `gws-bootstrap-cowork --local-tgz` (dùng gws.tgz từ bundle, khỏi tải Drive; md5 vẫn verify); tl_fetch.sh tự dò assets/gws.tgz. Cắt 1 download. 1.22.41: `nlm-install --uv` (egress mở → uv tự lo Python 3.11, python hệ thống nếu ≥3.11, KHÔNG tải 31MB Drive; fallback Drive); `tl_fetch.sh --setup --nlm` dùng --uv → bootstrap đủ GAS+direct-media+gws+nlm+boot 1 lệnh. (v1.23.0 spec rasoat-loop/overlap: roadmap riêng.) 1.22.40: bake NLM_CRED_FILEID (đã stage+verify) → `--setup --nlm` có nlm headless ngay. 1.22.39: nlm HEADLESS — `nlm-auth-stage` (Code, sau `nlm login`: cookie nlm → mã hoá khoá=webapp-token → Drive) + `nlm-auth-load` (Cowork: tải+giải mã bằng token → ~/.notebooklm-mcp-cli, KHÔNG cần master key); `--setup --nlm` tự nlm-auth-load (mirror gws-auth-stage/load). 1.22.38: tl_fetch.sh ROUTE TỐI ƯU (curl public, $HOME, --setup) + gws TRƯỚC nlm. 1.22.37: tl_fetch.sh webapp GAS. 1.22.36: tl_fetch.sh bỏ qua mount. 1.22.35: tl_rebuild.sh + MANIFEST.sha256 + tl_boot verify sha. 1.22.34: dọn references/ 63→24 file. 1.22.33: _parts ≤200 file. 1.22.32: verify-integrity + COWORK_EDIT_SAFETY. 1.22.32: `tl verify-integrity` + COWORK_EDIT_SAFETY (write-side fallback); 1.22.31: truncation-resilience (FORCE _parts; _healed_script_path; --rebuild) + doctor nlm/gws + reg-query khóa NLM; 1.22.27: #4/#3/#6/#9; 1.22.26: #1 relation-check footnote-gate
# GĐ0 (tích hợp gws): PIN bản gws — KHÔNG `latest` (gws pre-v1.0 hay breaking). Nguồn-chân-lý
# duy nhất cho boot-check `tl gws-ping` và (GĐ1) gws_bridge.is_available(). Bump có chủ đích.
# [lịch sử] 1.34.44 (assignment gỡ v1.34.45 — chỉ 1 VERSION duy nhất bên dưới): MERGE bundle audit-profile phiên song song (ADR-0001; review 6-chiều + adversarial 0 blocker/major): P-01..P-16 — cách ly scope profile (block rỗng không kế thừa vbqppl, malformed fail-closed, env-switch xóa scope stale, cache slug an toàn Windows + chống traversal, mutation ghi đúng file config đã đọc, bỏ candidate ghi /tmp); giao dịch marker-first cho create/adopt/promote/from-nlm + rename cập nhật marker với rollback config + duplicate-marker detection + sync/backfill hết false-success + delete giữ config khi remote lỗi; PermissionError→data (live), selftest hermetic TL_CACHE_DIR, bundle-export credential-lazy, +12 test r106 (886 total), agents/openai.yaml, docs sync (ADR-0003 key schema/profile, SKILL.md liệt kê đủ lệnh ghi marker). (trước) 1.34.43: hoàn tất BUG2 — nlm-reconcile --refresh cũng nạp load_creds (ops-sweep dogfood bắt gap: reg-query/locate/status đã có, nlm-reconcile bỏ sót → chết Thiếu TL_WEBAPP khi --refresh; TDD r105). (trước) 1.34.42: vá 3 bug audit-tool (grill-with-docs; TDD r104 negative-input) — (BUG1) nlm-reconcile --all-notebooks HẾT báo 'mọi notebook sạch' oan khi ok=false: note ĐIỀU KIỆN `_reconcile_sweep_note` (liệt kê notebook rc≠0/finding) + upfront load_creds+_manifest_entries self-heal (chưa boot scope → tự nạp/build cache, hoặc NEEDS_BOOT_PROFILE rõ) thay vì lặp rc=2 im lặng (stderr bị nuốt khỏi per_notebook). (BUG2) reg-query --refresh gọi load_creds TRƯỚC _manifest_entries (khuôn locate/status) — hết chết 'Thiếu TL_WEBAPP' làm tưởng MẤT token; thông điệp lỗi refresh cụ thể hơn. (BUG3) reg-query +`--corpus-effective`: lọc corpus theo LUẬT SERVER (`_entry_is_corpus_effective` tách PURE từ _corpus_count_server_rule: corpus∈{true,vbqppl}∪overflow − ref − thuong) = KHỚP `tl boot` corpus_count (base 521 vs literal --corpus true 486); cảnh báo `--corpus true` là literal + cảnh báo --corpus-effective CHỈ đúng scope nền vbqppl (profile đếm khác — live-smoke bắt: BHXH 14 corpus=true đều ref → effective=0). Không bump GAS/kernel. LOẠI non-bug: manifest so_hieu/id (helper phủ), infra self-register (guard _is_infra_file đã có — legacy đã dọn). #OLD_1.34.41: B.2 GĐ2 — sửa TẬN GỐC _classify_doc_header nhận văn kiện ĐẢNG/hành chính (grill D1-D9; TDD r103 ×15, fixture ca thật + harness file thật bắt 2 bug fixture-rút-gọn che): kind mới dang/hanhchinh (nhận TRƯỚC nhánh vbqppl — không thì sohieu Đảng kích Điều-gate chặn oan cat 00; cả hai không đòi Điều, flag trace); _SOHIEU_NOYEAR_RE riêng bắt số Đảng NN-XX/CQ (04-CT/TW, Đđ trong mã CQ) + hành chính NN/XX-CQ (123/BC-UBND) CHỈ trên dòng letterhead thuần 'Số …' (fullmatch — ends-with dính trích dẫn ngắn '- Căn cứ Luật Lưu trữ số 33/2024/QH15' cướp sohieu, ca thật QĐ 383); pre-text dạng-có-năm cũng siết fullmatch '[loại] số:'; loai LETTERHEAD-FIRST (_declared_loai_from_header > prefix tên > mã sohieu — ca QĐ 383 file QD_ nói 'Quyết định' ruột nói 'QUY ĐỊNH'); _is_vbhn_doc +suy từ dạng sohieu (layout VPQH không banner bị declared 'LUẬT' đè); fallback 'nghi quyet' thu về title-zone 1500 (hết nhuộm loai từ thân); sohieu_key year-qualified NN-YYYY-XX-TW cho dang/hanhchinh (số Đảng tái dùng qua khóa = collision lớp VBHN); _dang_bare_key + nới matcher 1 chiều (khuôn _vbhn_bare_key); _LOAI_CANON +5 loại Đảng (Quy định/Chương trình/Quy chế/Điều lệ/Thông tri — 'qd' GIỮ Quyết định, mơ hồ thì blank-over-guess); _HEADER_AGENCY_PATS +9 cơ quan Đảng/UBND/HĐND; _safe_profile_doc_name +18 mã loại + năm bắt buộc khi key không năm; _infer_loai +CTr_. (trước) 1.34.40: vá 7 lỗi BÁO CÁO 13/7 (grill-with-docs chốt 7 quyết định; TDD r102 ×10 NEGATIVE-INPUT — lớp 'sai mà báo thành công'): (A.1) extract positional dạng-ID export THẲNG (id thật LUÔN thắng — resolver cũ coi id hợp lệ như query → ghi đè → TRẢ SAI VĂN BẢN im lặng + cache bẩn, ca PL01); NOT_FOUND (≠ lỗi auth/mạng) mới deep-resolve fallback (giữ false-404 fix tên-giống-id); exact-match manifest lấy metadata; bỏ except:pass. (A.2) register --clear-cols + field set → rc=2 TỪ CHỐI (trước VỨT LẶNG field set mà báo verified:true). (A.3) ocr-verify: input parse được JSON → rc=2 (từng ĐO manifest JSON như text Việt rồi PASS); manifest-missing → FAIL mặc định (không manifest = không đối chiếu hash = chưa verify gì); +--no-manifest opt-in đo-thô. (B.1) slot-audit tách corpus_rows/nlm_claim_rows(+ref)/ref_rows ĐỒNG ĐỊNH NGHĨA nlm-reconcile — hết mâu thuẫn 2 tool + hết XÚI backfill-notebook (lệnh ghi) khi gap giải thích được bằng ref (helper PURE _nlm_ref_slot_count). (B.2) BLANK-OVER-GUESS: profile thường chỉ persist loai có bằng chứng TƯỜNG MINH (--loai / letterhead _declared_loai_from_header / prefix _infer_loai — cả 2 hàm nền +loại VB thường, prefix-only để không đụng VK_ dị thể r93); heuristic thân-văn-bản → ĐỂ TRỐNG (helper _profile_loai_evidence; ca HD 09-HD/VPTW bị đoán 'Luật'); giai đoạn 2 sửa tận gốc bộ suy = backlog. (B.3) profile-ingest-chunks --apply STREAM per-chunk stderr + resume_command (khuôn doctor v1.34.30 — 9 chunk >600s từng buffer đến cuối tưởng thất bại). (C.1) by_heading REDESIGN: heading CẤP CAO NHẤT không bao giờ gộp (1 PHẦN = 1 chunk — Phần V hết bị nuốt); section vượt max-chars tách CON đệ quy theo cấp dưới (Chương/Mục/numbered) → hết cấp cắt paragraph-budget 'X (i/n)'; mọi mảnh vượt mang flag CHUNK_SPLIT_OVER_BUDGET (chunk 191k từng lọt qua max 90k im lặng). ★LUẬT ĐỨNG MỚI: lệnh ghi/verify MỚI phải kèm ≥1 NEGATIVE-INPUT test (input sai cố ý → bắt buộc fail rõ). D.1 (nhãn lỗi nlm login --check) = upstream watchlist. KHÔNG bump GAS/kernel. 1.34.39: vá heuristic _cat_likely_wrong pin-từ-khóa — 12/20 FP corpus-audit 2026-07-13 (TDD r101 ×9, fixture = CHÍNH các ca thật): (A) pin 'dân tộc=10' lookbehind `(?<!hoi dong )` — 'Hội đồng Dân tộc' là TÊN CƠ QUAN QH (ca NQ_71-2025 bị 35→10); công tác/chính sách dân tộc thật vẫn pin. (B) _CAT_KEYWORDS['19'] gỡ 'tieu_chuan' TRẦN (va chạm 'tiêu chuẩn sức khỏe/chức danh' — 10+ TT BYT/BQP/BCA cat 45 bị suy 19 giả) → cụm dài 'tieu_chuan_do_luong'/'quy_chuan_ky_thuat' (đề mục 19 = Tiêu chuẩn ĐO LƯỜNG chất lượng; 'do_luong'/'chat_luong_san_pham' sẵn phủ). (C) boundary 46 hết đếm token 'luat'≥3 trên scope GHÉP biến thể tiêu đề (sửa-MỘT-luật cũng ≥3 — ca 26-2018 TDTT/75-2025 Quảng cáo bị 41→46): helper PURE _distinct_target_luat_subjects đếm CHỦ ĐỀ PHÂN BIỆT sau token 'luat' (strip stopword sửa-đổi, lấy 2 từ đầu gộp biến thể) ≥2, + tín hiệu tường minh 'cac/nhieu luat'/'sua doi N luat'; +guard suggest-46 CHỈ cho Luật (NĐ/TT/QĐ sửa nhiều văn bản cùng cấp cat theo lĩnh vực — ca ND_187-2025 44→46). (D) entry ở 23 + là điều ước (loai/CU_/CPTPP_/EVFTA_) → KHÔNG đề xuất tách theo chủ đề nội dung (quy ước gom ĐƯQT — ca CPTPP_Chuong_19 23→20). Control r101: pin thật + omnibus thật + true-positive nợ-công 26→28 GIỮ NGUYÊN. KHÔNG bump GAS/kernel. 1.34.38: vá 4 lỗi log phiên Chỉ thị (TDD r100 ×12): (#1) gate PHULUC_MENTION_WITHOUT_HEADING hết dương-tính-giả — heading dò trên bản STRIP-ACCENT (regex có-dấu cũ miss 'PHỤ LỤC 01' NFD/hoa — PL01 chính LÀ phụ lục mà bị chặn), CHỈ nghi khi nhắc 'phụ lục' KÈM SỐ (văn xuôi 'kèm theo phụ lục' vô hại), gate CHẶN corpus chỉ trên corpus NỀN — profile thường hạ info-flag PHULUC_MENTION_PROFILE_INFO (mirror doctrine requires_dieu v1.34.27 #2; ca thật HD 09-HD/VPTW + PL01 + 9 chunk Đề án CĐS). (#2) chunk-plan/apply +strategy `by_heading` (PHẦN thứ-nhất/I/1 · Chương I/1 · Mục 1) cho văn kiện Đảng/Đề án KHÔNG có Điều — hết cắt mù by_paragraph_budget giữa mục; guard heading = dòng-trống-ngay-trước HOẶC kết-câu (khuôn by_article); preamble (tên đề án) đi cùng chunk 1; cần ≥2 heading; ★2 bug bắt khi TDD: \\s trong pattern nuốt newline (title dính dòng sau) → [ \\t]; guard kết-câu một mình loại oan heading sau đoạn không dấu chấm. (#3) _LOAI_CANON +10 loại văn bản thường (Kế hoạch/Đề án/Thông báo/Phụ lục/Công văn/Phát biểu/Tờ trình + Biểu mẫu/Báo cáo/Tài liệu; alias ngắn né khóa cũ: pl=Pháp lệnh giữ, ttr=Tờ trình, bc=Báo cáo) — hết loai_noncanonical=26/53 GIẢ. (#4) hygiene scan: chunk `__partNN` chung sohieu gốc = THIẾT KẾ (link qua goc) — _is_chunk_part_name loại khỏi _sohieu_dup_group_real + _reconcile_clusters flagged (9 chunk Đề án CĐS hết bị gom duplicate_identity + nhãn quarantine giả; dedup-plan vốn không mắc). +Ghi chú RUNBOOK A0.3: bẫy gws update --params vs --json (body qua --json, sai chỗ = HTTP 200 im lặng không đổi gì — mọi write gws trần phải readback). KHÔNG bump GAS/kernel. 1.34.37: ingest `--drive-id` — nạp file ĐÃ Ở TRÊN DRIVE (bỏ upload). `ingest-local --drive-id <fid>` (người dùng tự kéo-thả _HOP_NAP qua UI/điện thoại/shared drive) organize (convert→GDoc+tên chuẩn+xếp cat+register) NGAY trên file đó, tải nhị phân về temp để auto-plan/size chạy y như đường local, organize dùng CHÍNH drive_id (không re-upload), --resume tái dùng fileId qua journal; `profile-ingest --drive-id` CHỈ convert+đổi tên GIỮ PHẲNG root profile (không xếp cat). Helper chung _resolve_drive_id_source TỪ CHỐI Google-native (convert nhân đôi)/trashed/không-thấy, suy đuôi từ tên hoặc reverse-map MIME; <file> positional nay nargs='?' (loại trừ --drive-id). r99 ×3 + parser-surface regen → 823/823. Verify LIVE: từ chối GDoc thật + DRY file nhị phân (download temp + auto-plan) + loại-trừ. KHÔNG bump GAS/kernel. 1.34.36: doctor SKIP marker-check cho profile root==VBT gốc (backlog #2 handoff 2026-07-11 — dứt known-noise ops-sweep [vbthuong] MARKER_MISSING; lazy bootstrap vanBanThuongId 1 lần, marker ở _meta VBT gốc sẽ nhận VBT làm profile thường = sai bản thể; r98). Kèm fix ops-sweep.ps1 local (ngoài repo): B5 2>$null (doctor v1.34.30+ stream stderr làm 2>&1 hỏng parse) + B6 --refresh (cache stale báo desync oan). 1.34.35: `ingest-local --no-nlm-add` (quy trình ADD-TAY user chốt sau benchmark GDoc-add: API add chỉ 11-19s, settle GDoc-đã-index ≈0 — bottleneck THẬT là COOKIE ~1h chết 2 lần/ngày giữa lô; UI add dùng session browser + Drive-picker chọn nhiều file = né hẳn): DỪNG ở Drive+registry (organize register xong), KHÔNG đụng NLM (skip preflight/dedup-gate/add/link); corpus KHÔNG set (doctrine S4 — corpus=true chỉ khi đã lên NLM); output gdoc_url + suggested_notebook (routing GAS nlm_preflight vẫn chạy — không cần cookie) + notebook_url + next_steps 3 bước điền sẵn (add tay UI → nlm-reconcile --all-notebooks link bắc cầu exact-title → register --corpus true); journal run_end +no_nlm_add. ĐÍNH CHÍNH benchmark: phân rã '238s = settle ~115s' hôm qua SAI ở phân bổ — add GDoc thật no-wait 11.0s / wait 11.2s (settle≈0 doc đã index) / doc lớn 18.7s; 238s = 4×NLM-call lúc API chậm + GAS chain + settle GDoc MỚI-convert (caveat cache). r97 ×3 → 819/819. KHÔNG bump GAS/kernel. 1.34.34: vá 2 bài học THỰC CHỨNG lô song song 2026-07-12 (nạp 2 VBHN --nlm-no-wait ×2 process: 63s/file kể cả sự cố vs 238s; ca VBHN 06 registry TRỐNG dù journal patched=1+verified). (a) `_verified_reg_write` batch ≤_REG_BULK_READBACK_MAX(3): READBACK field-level per-item (reg_get refresh, khuôn N3) → lệch (RACE 2 process reg_bulk last-write-wins trên Sheet) → RETRY per-item 1 vòng (ghi-lại sau race là bền) → vẫn lệch = REG_BULK_FIELDS_DROPPED loud; batch lớn giữ patched-check (không phình backfill). (b) `nlm-reconcile --all-notebooks`: quét base+overflow 1 lệnh (DRY-only, apply per-notebook) — nguồn nạp overflow trước đây LỌT LƯỚI reconcile mặc định; dogfood LIVE bắt ngay 2 finding thật trên overflow (link_candidate 76-2026 Luật Dược → applied backfill; 1 unregistered VBHN_73-82 phụ lục chờ user). DATA-OP: 63-2025-VBHN XLVPHC corpus=false (superseded bởi 90-2026; nguồn NLM cũ còn live chờ user quyết gỡ). r96 ×6 + r3 mock cập nhật → 816/816. ★Bẫy I11 biến thể mới: HẰNG vào _STUB_MAP thành function → so sánh int nổ; hằng PHẢI re-export trực tiếp `X = _tl_mod.X`. KHÔNG bump GAS/kernel. 1.34.33: `ingest-local --nlm-no-wait` (#2 benchmark 2026-07-12 — báo cáo D:\Quốc hội\benchmark-ingest-2026-07-12.md): ingest ~238s/file HẰNG SỐ bất kể size, cổ chai = NLM 71% (settle-wait sau source_add ~115-125s = 50%; mỗi NLM CLI call 11-18s = spawn 2s + batchexecute API 10-16s), GAS chỉ 19%. Cờ mới BỎ chờ settle: source_id có NGAY từ add-response → reg_link vẫn ghi ĐỦ (corpus=true + nlm_* trọn); post-add dup-check BỎ khi no-wait (nguồn chưa settle → list âm tính giả + tốn 18s); output +nlm_settle=not_waited +next_step nlm-reconcile. Ước −55% → ~90-120s/file; lô lớn kết hợp --skip-nlm-preflight --skip-live-check + 2-3 process song song → ~35-50s/file wall. Sau lô no-wait PHẢI `tl nlm-reconcile` xác nhận settle+link; truy vấn NLM nội dung mới nạp cần chờ vài phút. r95 ×3 (parser + shape-lock khuôn r55 + PURE _add_args) → 810/810. KHÔNG bump GAS, KHÔNG đổi kernel. 1.34.32: VBHN-FIRST TẤT ĐỊNH cho corpus-relation-sweep (user bắt lỗi doctrine: sweep v1.34.31 đề xuất fetch Luật GỐC dù VBHN đã phủ — 4/7 đề xuất sai; + 46% vbhn false-positive do matcher fuzzy subject của relation-check). Fix 3 lớp TẤT ĐỊNH: (1) `_vbhn_goc_map` PURE — map norm_sohieu(gốc/luật-sửa)→VBHN corpus SẠCH phủ, từ field registry `goc` (';'-cách) + `sua_doi` 'Hợp nhất từ:' + pattern tên goc_<sohieu> (phủ 67/72 VBHN corpus); amendment thiếu NHƯNG chuỗi có VBHN phủ → `covered_by_vbhn` KHÔNG vào sources_to_add. (2) `vbhn_broken` CHỈ giữ khi GOC-TIE tất định (goc VBHN ứng viên ∩ {base ∪ mọi luật-sửa inline}) — hết gán VBHN Thư viện cho Luật Thủ đô/Viễn thông, VBHN Đầu tư cho Điện ảnh/Chuyển đổi số. (3) base nằm trong chuỗi VBHN → `vbhn_first_self` advisory (bản rời gốc/sửa-đổi redundant với VBHN — đúng nguyên tắc VBHN-first: giữ VBHN, bản rời cân nhắc loại). Verify LIVE ca 26-2018 TDTT: 77-2006 covered-by-64-2025, 0 fetch. r94 ×3 + r93 asserts đổi có chủ đích → 807/807. KHÔNG bump GAS, KHÔNG đổi kernel. 1.34.31: RÀ CORPUS VBQPPL (grill-with-docs). (a) `_infer_loai` +prefix điều ước (CU_→Công ước; CPTPP_/EVFTA_→Điều ước quốc tế) + văn kiện Đảng (KL_→Kết luận, CT_→Chỉ thị, HD_→Hướng dẫn; +sohieu-fallback -KL-/-CT-/-HD-); +enum "Hướng dẫn" — backfill-loai cũ bỏ trống 38 dòng corpus (ĐƯQT+Đảng) vì thiếu prefix; VK_ Đại hội dị thể ở lại manual. (b) TOOL MỚI `corpus-relation-sweep` (#T1): BATCH relation-check toàn bộ Luật/NQ corpus (SCRIPT-REUSE #15 — capture JSON per-doc) → gộp 'nguồn cần bổ sung' (vbhn_broken quarantine/removed/thiếu-năm + missing_links + [--deep] amendments_missing đọc nguyên văn base) + google_discovery; STREAM per-doc stderr, resumable --limit/--skip, --out; READ-ONLY. r93 ×5 TDD → 804/804. KHÔNG bump GAS, KHÔNG đổi kernel doctrine → re-import không bắt buộc. 1.34.30: vá 7 lỗi log grill (register/from-nlm/doctor/marker). GRILL chốt: register choices GIỮ own/overflow/ref (KHÔNG mở nlm_only — sentinel đi qua from-nlm --add-missing để ép đủ bó bất biến). (#1) register --bulk: surface missed_count/missed_ids LOUD + rc=1 khi missed>0 + force_insert_note (reg_bulk UPDATE-only, --force-insert chỉ bypass client-guard KHÔNG insert). (#2→) `profile-from-nlm --add-missing`: profile ĐÃ TỒN TẠI → seed CHỈ nguồn thiếu (khóa nlm_source_id, reuse _from_nlm_row_payload, journaled+verified, DRY mặc định) — lấp khoảng trống 'không có đường sanctioned thêm nguồn nlm_only vào profile có sẵn'; không cờ + folder có marker → ALREADY_PROFILE + hint. --notebook nay optional (lấy từ config). (#3) register đơn: precheck reg_get → field `inserted:true/false` (hết ngộ nhận updated:false = ghi hụt). (#4) register +--json no-op (đồng bộ CLI, hết đổ 150 lệnh khi arg lạ). (#5) profile-doctor --deep: --limit/--skip cắt lô + STREAM per-profile ra stderr (progress+JSONL, timeout không mất trắng) + resume_command; GIỮ scan-all mặc định (không breaking). (#6) _nlm_system_prompt_apply: field `verification`=local_artifact_and_api_ok_only + verification_note trung thực (nlm chat KHÔNG có lệnh đọc config LIVE) + sửa docstring. (#7) ROOT-CAUSE marker trùng: _marker_write upload force=true LUÔN tạo fileId mới, chỉ trash old_id do caller → create/from-nlm/promote (old_id='') gặp marker retry-đứt = DUPLICATE mồ côi → SELF-HEAL quét _meta trash MỌI marker khác fid mới; doctor +MARKER_DUPLICATE detect. r92 ×13 TDD → 799/799. KHÔNG bump GAS (2.21.2j), KHÔNG đổi kernel doctrine → re-import không bắt buộc. 1.34.29: profile-set-meta — cửa ghi chính thức phần MÔ TẢ trên marker (description/style/see_also/source_policy; DRY→apply journaled+readback+trash-cũ; identity từ chính marker; xoá=chuỗi rỗng; r91 ×6 TDD). 1.34.28: vá bug máy-phụ-thuộc #5 (phiên kia bắt trên zip 1.34.27, tái hiện bằng Python 3.11): r77a parser-surface hash cả `required` của POSITIONAL — field DẪN XUẤT theo version Python (nargs='*': 3.11=True vs 3.12+=False → cache-build/fetch-batch/rasoat lệch, selftest 778/779 trên máy 3.11). Fix: positional không hash required (optional giữ); regen snapshot; verify cross-Python 3.13+3.11 = 779/779. 1.34.27: HOTFIX 7 lỗi thực-chiến (log phiên tạo profile + nạp 4 file): (#1) _nlm_add_doc_type thiếu stub → nlm-add NameError, vá + r90 DRIFT-LOCK GENERIC AST (mọi tên top-level module REBASE phải resolve qua tl — bắt cả lớp bẫy); (#2) verify_gate đòi-Điều CHỈ trên corpus nền (profile thường kiểu-Mục hết dương-tính-giả); (#3) DRY probe .docx local (hết DRY/apply lệch); (#4) reconcile tier-3 exact-title duy nhất; (#5) FIELDS_DROPPED fallback POST reg_bulk; (#6) nlm-add +--json no-op; (#7) hết utcnow deprecated. r90 ×7 → 779/779. 1.34.26: PROFILE P4 — KẾT LỘ TRÌNH 4 PHASE: `profile-from-nlm` (notebook→profile: seed ref/nlm_only sentinel drive_id='nlm:<sid>' KHÔNG bump GAS, note=materialize=pending) + `profile-materialize-sources` (materialize_preferred: source_content→createtext→row own→xoá sentinel tạo-trước-xoá-sau, resumable --limit, blocked ở-lại-nlm-only hợp lệ) + `profile-doctor --deep` (Drive↔NLM↔registry: UNREGISTERED/PENDING/BLOCKED/SENTINEL_STALE). r89 ×7 TDD → 772/772. 1.34.25: PROFILE P3 (Q2+Q3+Q5): `profile-promote --name --folder [--notebook|--create-notebook]` — folder thường→profile: dựng hạ tầng thiếu (reuse idempotent; manifest lạ→FOREIGN_IGNORED) + seed registry own/corpus + NLM System Prompt tự áp (chat configure custom, fallback manual_required, lưu _meta/nlm_system_prompt.md) + notebook-create điều-kiện-kép nới có kiểm soát (confirm yes + journal + readback notebook_get); nạp NLM đi ingest-missing --allow-no-sohieu. nlm_cli +notebook_create/chat_configure. r88 ×7 TDD → 765/765. 1.34.24: PROFILE P2 (Q7+ADR-0003): `profile-load <p> [--target session|project]` — Instruction Block sinh từ MARKER (định danh+description+style+relations+source_policy), MỘT bản thống nhất mọi env, read-only; profile-use --apply in kèm block; generate_profile_load_block + 5 case gen_instructions + r87 ×7 TDD → 758/758; KERNEL-DIFF user DUYỆT: bullet 9 'config là nguồn sự thật' → 'MARKER là nguồn sự thật (ADR-0003)' + profile-load — SKILL.md ĐỔI DOCTRINE → RE-IMPORT. 1.34.23: vá live-smoke P1 — _profile_sync_rows nhận vbt_id (vbthuong root==VBT hết orphaned oan); backfill skip skipped_vbt_root (không đặt marker vào _meta của VBT gốc); ĐÃ backfill marker THẬT Luật BHXH + NQ80 (written+verified, journaled) → sync in_sync rc=0. 1.34.22: PROFILE P1 (ADR-0003): marker _meta/tra_luat_profile.json = nguồn sự thật tồn tại/định danh profile — profile-sync (một chiều marker→config, journaled+readback) + profile-backfill-markers (config→marker một lần, upload+readback+trash-cũ) + create/adopt tự ghi marker + discover MARKER-FIRST (configured/adoptable/broken_marker/orphaned, hết heuristic) + doctor kiểm marker 4 check + config-of-record report (cảnh báo duplicate config). TDD r86 ×10 viết trước → 752/752. 1.34.21: HOTFIX resilience `register --clear-cols` (thẩm định Codex + grilling): precheck NO_SUCH_ROW rc=2 hết thành-công-giả; verified = dòng-tồn-tại + cột-rỗng readback, already_empty idempotent (KHÔNG cleared>=1); về primitive _journaled_reg_clear(force=) → try/except + journal key_field/set/before chuẩn undo/resume; _apply_gate; contract_check LIVE_PING_FAILED(rc4)≠VERSION_DRIFT(rc3). TDD r85b ×7 viết trước → 742/742. 1.34.20: #5 TRỌN VẸN (webapp GAS + tl, TDD r85 viết trước): GAS 2.21.2j deploy qua clasp (gas-deploy.ps1, giữ /exec) — doRegClear_ 2 TẦNG: nlm_*/note như cũ; CỘT THƯỜNG ∈ REG_COLS_ cần force=yes; drive_id/name BẢO VỆ tuyệt đối; tương thích ngược 100%. tl-side: register --clear-cols <csv> --confirm yes (tự gắn force cho cột thường, journaled intent{before-từ-manifest}, readback field-level xác nhận RỖNG, guards client-side protected/confirm); note_empty gợi ý đường mới; contract register + API_CONTRACT reg_clear cập nhật; contract_check --bump nay sửa CẢ literal tl_selftest; EXPECT_VERSION 2.21.2i→2.21.2j (17 chỗ doc, references/Code đổi tên theo — SKILL ĐỔI → USER RE-IMPORT). ★Bẫy: def/const MỚI trong module cần stub/re-export ở tl (kiến trúc rebase); file .gs doc đổi tên phải theo bump. +5 r85 → 735/735. // 1.34.19: BACKLOG #11 (phát hiện khi làm #10, TDD r84 viết trước): _persist_profile_config ứng-viên-ghi = _config_candidates (CÙNG thứ tự resolution với ĐỌC — cwd/skill-side v2 TRƯỚC home) thay hardcode ~/.tra_luat_config.json → HẾT ghi-config-lạc-chỗ im lặng (ca thật: profile-adopt không --config ghi vào home-config KHÔNG active, profile-list vẫn inherit); --config tường minh vẫn thắng. +r84 → 730/730. // 1.34.18: I11 — VƯỢT ĐÍCH 2500: tl.py 3576→1394 dòng (lũy kế 19052→1394, −93%). (a) LEFTOVER-SWEEP 91 def ~1.5k dòng vào 14 module theo affinity-tốt-nhất ≥1-ref (10 def 0-affinity ở lại); (b) build_parser 391d → tl_core/cli.py NGUYÊN VĂN (35 block tay + doctrine-comment giữ tại chỗ; parser-surface KHỚP KHÔNG REGEN = tương đương byte); (c) 5 bảng hằng lớn (_CAT_KEYWORDS/_ABBREV_MAP/_LOAI_CANON/_FLAG_REASONS/INSTRUCTION_REQUIRED) → module dùng nhiều nhất + re-export 1 dòng ở tl. ★2 bẫy mới: (1) hằng DẪN XUẤT top-level (_ABBREV_RE compile từ map lúc import TRƯỚC khối import module) → phải sống cùng file với map gốc; (2) sweep chuyển nhầm _json_dumps (wrapper lõi đọc mutable-global _DETERMINISTIC_ON) vào ocr — r61 chặn ĐÚNG THIẾT KẾ → trả về tl + ghi PLUMB-list. tl.py nay = plumbing/self-heal + spec-call + _STUB_MAP + main. → 729/729. // 1.34.17: BACKLOG #4-#8 log phiên hồ sơ Luật BHXH (TDD r83 viết trước): (#4) nlm-add --type default None + _nlm_add_doc_type tự nhận GSheet từ MIME manifest OFFLINE (explicit thắng; surface regen CÓ CHỦ ĐÍCH đúng 1 lệnh); (#5) _verified_reg_upsert cảnh báo LOUD empty_ignored — giá trị RỖNG cột thường bị webapp bỏ im lặng by-design (chỉ nlm_*/note clear được; đính chính = ghi giá trị mới/note); (#6) FIELDS_DROPPED_ON_WRITE → tự retry per-field 1 vòng + re-readback (fields_retried; hết phải ghi lại tay từng lượt nhỏ); (#7) ocr-run recommendations kèm LỆNH CÀI cụ thể (pip install ocrmypdf + apt ghostscript tesseract-ocr-vie / Windows installer); (#8) instruction-audit --file dùng CÙNG gen_instructions.audit như --generate (hết list block riêng lệch → báo thiếu-khối giả). +5 r83 → 729/729. #5-webapp-clear-cột-thường cần đổi GAS = NGOÀI phạm vi (ghi CHANGELOG). // 1.34.16: Pha-E-hoàn-thiện — nhóm lệnh NGUY HIỂM lên risk=high + contract THẬT (TDD: r82 viết trước ĐỎ 3 đúng chỗ): profile-rebuild-registry (phá hủy reg_delete+regen; contract trung thực KHÔNG WAL → rollback=Sheets version-history bài học 1.23.21; CLOBBER-guard + --keep-notebook + DRY/confirm ghi rõ), ingest-missing (WAL ckpt 4 khóa done/pending/linked/fails + FRESH-verify + dedup-live tiered + overflow-route no-create), manifest (dẫn-xuất-tất-định từ registry; --touched-drive confirm-gate chống SCOPE_BLOWUP). _CONTRACT_REQUIRED 12→15; r65 exact-set nâng theo; +r82 meta-high/contract-đủ-8-field/cờ-khớp-code + r82 rollback-via-version-history. KHÔNG đổi CLI (parser-surface khớp); golden tool_inventory regen đúng 1 file (risk-counts). → 724/724. // 1.34.15: I10 — NÉN STUB-FARM (bước 3/3 chiến-lược-chặng-cuối): 488 def ủy-quyền 2-dòng (18 module) → bảng _STUB_MAP + factory _make_tl_stub (giữ __name__ cho parser-surface bất biến; gắn __tl_stub__=(module,name) làm định danh máy-đọc); tl.py 5381→3576 (lũy kế 19052→3576, −81%). ★ĐỔI CƠ CHẾ KIỂM: 12 wired-check r7x getsource(_tl_X.{n}) + 9 no-dual count==1 → marker __tl_stub__ + count==0 (tl KHÔNG còn def cho tên đã stub-hoá); +r81_stub_farm_map_complete quét TRỌN 488 entry (map↔module-def↔marker↔name↔no-def-in-tl, ≥480 sàn). Phần còn lại tl.py = plumbing 611 + 35 block parser tay + specs-call + hằng + main — đích 2500 CHẠM Ở MỨC 3.6k; ép tiếp = I11 tuỳ chọn (bóc 35 block tay + bảng hằng sang references) — cân nhắc lợi/hại vì phần này là wiring thật, không phải nợ. // 1.34.14: I9b — HOÀN TẤT I9 (bước 2/3): tách resolve.py (39 def ~1.28k: ĐỘNG CƠ _source_map_one+amendment-gate/dedup-status/classify-ref/footnote-VBHN/qt5/discovery) + regio.py (63 def ~741: manifest-entries/_entry_*/norm_sohieu/_cache_file + journal primitives + _journaled_reg_write/_verified_reg_*/_apply_gate) sang tl_core/; tl.py 7177→5381 (lũy kế 19052→5381, −72%; 13 module). ★ĐỔI LUẬT CÓ KIỂM SOÁT: r76_engine_stays_in_tl → r76_engine_canonical_in_resolve (def thật ở resolve.py, tl stub, vẫn 1-định-nghĩa). Characterization: +4 r80a khoá THÂN THẬT write-infra TRƯỚC cut (intent/commit-per-row theo missed_ids + bust-cache; error→all-uncommitted; apply-gate block/force/pass; before-snapshot dịch sohieu) — lâu nay r-test toàn mock các hàm này. ★2 bẫy mới: (a) OFF-BY-ONE máy cắt từ I1 — xoá từ a-1 nuốt dòng SÁT def (ca _LINHVUC_CACHE=None → NameError; trước giờ vô hại vì luôn là dòng trống) → fix xoá từ đúng dòng def + khôi phục cache ở tl (r80_linhvuc_cache_lives_in_tl); (b) mirror _DISCOVERY_SITES (r80_discovery_sites_mirror). +r80 wired/no-dual → 721/721. Kế: I10 nén ~490 stub. // 1.34.13: I9a — bước 2/3 chiến-lược-chặng-cuối: tách INFRA đa-module đợt 1 (đổi-luật-có-kiểm-soát đã grill) — classify.py (74 def ~1.22k dòng: loai/cat/title_vn/header-facts/strip-accents/sentence-case + misc-affinity>50%) + profile_env.py (36 def ~512 dòng: config/creds/profile-env/GAS-webapp/transport-helper) sang tl_core/; tl.py 8684→7177 (lũy kế 19052→7177, −62%; 11 module). ★Máy cắt I9a có 2 scanner MỚI: (a) TOP-LEVEL scanner — hàm được statement top-level gọi TRƯỚC bind phải ở lại (_ensure_writable_tmpdir/main/_tl_core_import tự loại); (b) AFFINITY assignment — def chưa-nhóm chỉ kéo theo khi >50% tham chiếu đến từ nhóm đang cắt. Characterization = 711 test hiện có (classify/profile_env là vùng phủ DÀY nhất codebase: r10/r11 title-block, _infer_loai case-list, r57 profile-env, r73a title-zone, r74a fixture-config) — PASS Y NGUYÊN sau cut, KHÔNG sửa test nào. +r79 wired/no-dual → 713/713. Kế: I9b resolve+regio (đổi r76 engine-stays → canonical-ở-resolve.py) rồi I10 nén stub. // 1.34.12: I8 — tách 56 def nhóm lệnh vận-hành/chẩn-đoán (~2.0k dòng NGUYÊN VĂN AST-cut: 32 cmd doctor/ping/precheck/boot/up/perf/bench/reg-query/counts/exists/registry-map/cat-list+verify/journal/undo/resume/confirm/manifest/backfill-notebook/vbhn-normalize/reg-delete/init-config/config-pin-registry/edit-skill/verify-integrity/instructions/instruction-audit/loop/cowork-plan/source-verify/profile-file-remove/convert-verify + 24 helper riêng-nhóm) sang tl_core/ops_misc.py; tl.py 10712→8684 (lũy kế 19052→8684, −54%). Chiến lược 3-bước grilling: I8 misc-cmd ✓ → I9 infra-module → I10 nén stub. ★Bẫy mới: canary REQUIRED-list nằm TRONG _skill_package_integrity (hàm bị move) → vá canary trong NỘI DUNG MODULE; mirror _LOOP_LIVE_FIELDS (bẫy I2 default-param, r78_loop_fields_mirror). Converter tự LOẠI def đã-ủy-quyền (thân chứa _tl_ — 6 wrapper). Characterization +4 r78a (reg-query bare-VBHN 1-chiều; counts mẫu-số; exists A3-doctrine rc=0/2; journal TL_JOURNAL_DIR) — PASS y nguyên sau cut; 2 guard test (legacy-registry/clobber) trỏ nguồn thật ops_misc. +r78 wired/no-dual/mirror → 711/711. // 1.34.11: I7 wave-2 — HOÀN TẤT Pha E bề mặt lệnh: +78 COMMAND_META baseline bằng-chứng-cờ (phủ registry 131→160 lệnh khi tính spec-only; --apply→dry_run, --confirm→confirm, ghi ngoài-repo→medium+scope đích, KHÔNG high mới — nâng high+contract để Pha-E-hoàn-thiện) rồi converter chạy lại: +78 lệnh SINH TỪ GENERATED_SPECS (tổng 124 spec; tl.py 11296→10712). Parser-surface snapshot KHỚP KHÔNG REGEN = bằng chứng tương đương byte. ★2 bẫy converter wave-2 (r77a bắt cả hai): (a) add_argument HẬU-set_defaults (ca sweep --live-nlm) → converter tiêu thụ tiếp sau set_defaults; (b) register_generated LOẠI dest khỏi kwargs (schema Pha E coi dest=positional) → cờ có dest= tường minh bị argparse tự suy dest khác (4 lệnh cache-snapshot/profile-doctor/file-remove/manifest) → dest-passthrough khi entry có flags. Còn 35 block tay có chủ đích (17 set_defaults phức [tlg.* + kwargs phụ], 9 kwarg-non-literal, 6 foreign-stmt, 3 has-comment). // 1.34.10: I7 wave-1 — 38 lệnh build_parser SINH TỪ GENERATED_SPECS (converter AST cơ học, flags/help NGUYÊN VĂN; chỉ block an-toàn: kwargs literal, fn=cmd_* trên tl, KHÔNG comment nội khối [giữ doctrine-comment tại chỗ], ĐÃ có COMMAND_META 1-dòng [bất biến r64 spec⇒generated=True]); tl.py 11602→11296; register_generated help-optional. ★CHARACTERIZATION MỚI: r77a PARSER-SURFACE SNAPSHOT — SHA256 per-command của bề mặt parser đầy đủ (opts/dest/nargs/const/default/type/choices/required/help/metavar/kind + handler, đệ quy nested; KHÔNG phụ thuộc thứ tự add_parser) tại references/golden/parser_surface.json 14KB; regen có chủ đích TL_WRITE_PARSER_SURFACE=1 — mọi drift CLI từ nay bị khoá vĩnh viễn (drift-lock mạnh hơn r64 nhiều bậc). Sau chuyển: surface KHỚP TỪNG HASH. Còn lại wave-2+: 113 block skip (78 thiếu meta [cần bổ sung COMMAND_META trước — việc hoàn tất Pha E], 17 set_defaults phức, 9 kwarg non-literal, 6 foreign-stmt, 3 has-comment). // 1.34.9: I6 — tách 16 cmd tra-cứu/quan-hệ + 25 helper riêng-cụm (~1.57k dòng) sang tl_core/lookup_ops.py (locate/source-map/status/relation-check+backfill/vbhn-check+verify+compare/xref/footnote-map/cluster/rasoat×3/header-verify/dedup-check); tl.py 13176→11602. ★RANH GIỚI GRILLING: động cơ _source_map_one (365d, 59 điểm test) + helper đa-module (_dedup_status/_classify_ref/resolve_footnote_amendments/_relation_audit/_rq_relation_probe/_scan_inline_amendments/_sohieu_query_hits_entry/_nlm_status_*/_qt5_search_hints) GIỮ Ở TL — r76_engine_stays_in_tl khoá cứng (def thật, không stub hoá). Characterization: +3 r76a wiring khoá shell cmd (source-map canonical shape/results-alias/verdict; MISS rc=0 A3-doctrine; status --amendment guard SKIP+ON_NLM offline). Scanner default-param 0 hit. +r76 wired/no-dual → 703/703. // 1.34.8: I5 — tách cụm ingest_pipeline sang tl_core/ingest_ops.py (37 def ~1.76k dòng NGUYÊN VĂN AST-cut: 12 cmd ingest-local/profile-ingest/ingest/ingest-analyze/ingest-route/ingest-missing/register/recat/source-rename+delete+update-corpus/shared-source-fix + 25 helper riêng-cụm: classification/_classify_doc_header+_sohieu_from_title_zone/verify-gate/chunk/mime/checkpoint/plan-helper); tl.py 14932→13176 dòng (lũy kế chuỗi I: 19052→13176 qua 7 module); bind REBASE __globals__ (khuôn I1-I4); scanner default-param 0 hit. WRITE-INFRA ĐA-MODULE GIỮ Ở TL: _journaled_reg_write/_apply_gate/_verified_reg_upsert/_reg_before_from_manifest (đếm-tham-chiếu: hygiene+nlm_ops+profile_mgmt cùng dùng). Characterization TRƯỚC cut: +5 r75a wiring offline (ingest-route ASK_USE_EXISTING/PROFILE_OWN; ingest-analyze letterhead→plan+lệnh điền sẵn; source-rename DRY gợi ý tên; shared-source-fix DRY group; register --bulk GUARDS P0-1 chặn drive_id-cắt-cụt/cat-rác KHÔNG ghi) — PASS y nguyên sau cut; 3 test getsource (recat/r55 ingest-local/clobber) trỏ nguồn thật. +r75 wired/no-dual → 697/697. // 1.34.7: I4 — tách cụm profile_mgmt sang tl_core/profile_mgmt.py (22 def ~967 dòng NGUYÊN VĂN AST-cut: profile-info/list/use/rename/delete/files/manifest/adopt/doctor/index/create/rebuild-registry + helper riêng-cụm); tl.py 15743→14932; bind REBASE __globals__ (khuôn I1-I3); scanner default-param 0 hit. Hạ tầng profile DÙNG CHUNG (_apply_profile_env/_profile_lookup/_read_config_record/_profiles_from_config/_persist_profile_config/_profile_policy_error/_active_profile) GIỮ Ở TL. ★FIXTURE-CONFIG tất định (references/golden/fixtures/config_fixture.json sinh-tại-chỗ, registryDocId pin sẵn) — cách ly trạng thái config máy (bài học CI I1): golden ops-plan HỒI SINH (hygiene_ops_plan_fixture_config: --config fixture + xoá env TL_* per-case, cross-machine). Characterization TRƯỚC cut: +4 r74a wiring trên fixture config (profile-list; profile-info CHỊU-LỖI-GÕ khoá P2 v1.33.48; profile-use DRY-không-ghi + PROFILE_NOT_FOUND; profile-rename DRY plan + cấm rename nền) — PASS y nguyên sau cut; test clobber-guard trỏ nguồn thật. +r74 wired/no-dual → 690/690. // 1.34.6: vá Nhóm 1+2 log phiên chạy thực 2026-07-09 (hồ sơ Luật BHXH — 3 defect profile văn-bản-thường): (#1) _classify_doc_header HẾT nhận số hiệu TRÍCH DẪN làm số hiệu tài liệu — sohieu CHỈ từ VÙNG TIÊU ĐỀ (head 1500, DÒNG NGẮN ≤80 ký tự kiểu letterhead, ưu tiên có Số: đứng trước — _sohieu_from_title_zone) + tên file; số trong CÂU VĂN DÀI = trích dẫn → BỎ (trước: báo cáo nhắc Luật 41/2024/QH15 bị gán loai=Luật+sohieu → ghi sai metadata âm thầm); nhánh VBHN N2a nay chạy CẢ khi sohieu title-zone rỗng (số VBHN ở khối ký cuối — quét sâu blob CHỈ dạng VBHN). (#3) _ingest_verify_gate bỏ vế OR-sohieu: requires_dieu CHỈ theo kind∈{vbqppl,draft,nq} — văn bản thường có số hiệu công văn không còn bị DIEU_STRUCTURE_NOT_VERIFIED chặn corpus_allowed (profile-ingest hết dừng nửa chừng phải nlm-add tay); +info flag DIEU_NOT_REQUIRED_NORMAL_DOC. (#2) bảng tính trọn đường ống: _MIME_BY_EXT +.xlsx/.xls (trước rơi về DOCX_MIME → convert fail); profile-ingest nhánh sheet = copy_convert toType=sheets → canonical Google SHEET + readback expected_gdoc_mime=_GSHEET_MIME (+param mới _verify_convert_readback) + NLM source_add doc_type=sheets nội bộ + skip text-gate (SPREADSHEET_TEXT_VERIFY_SKIPPED). TDD: 7 test r73a hành-vi-đúng viết TRƯỚC (4 đỏ đúng chỗ) → fix → 684/684. BACKLOG còn từ log: #4 nlm-add auto-detect --type sheets; #5 register clear cột thường (cần webapp GAS); #6 register auto-retry FIELDS_DROPPED; #7 ocr-run báo lệnh cài engine; #8 instruction-audit đồng bộ block-list từ gen_instructions; #9 user sửa Project Instruction version; #10 vbthuong categories=inherit→own (cần user duyệt). // 1.34.5: I3 — tách extract_cache (cmd_extract/cache-build/cache-snapshot, 3 def ~214d) + fetch_web (fetch-route/batch/links, find-doc, tvpl-url, external-ingest, link-priority, frontier + _fetch_plan/_external_ingest_plan, 12 def ~389d) sang tl_core/{extract_cache,fetch_web}.py; tl.py 16227→15743. Ranh giới đếm-tham-chiếu: hạ tầng đọc (_read_doc_text 16 site/_cache_file 13/_title_block_from_text 6/extract_dieu/extract_refs/_sanitize_export_text/_profile_cache_dir) + discovery QT-5 (_query_variants/_google_site_url/_discovery_links/_official_rank + _FETCH_SOURCES/_DISCOVERY_SITES/HOPNAP) GIỮ Ở TL. Characterization TRƯỚC cut: +5 r72a wiring (extract resolve+bóc Điều qua transport mock; tvpl-url pure; fetch-route VBHN-first+docx-rank; fetch-batch SKIP/REVIEW/FETCH+ckpt; fetch-links markdown+env) — PASS y nguyên sau cut; scanner default-param (bẫy I2) = 0 hit. +r72 wired/no-dual → 677/677. // 1.34.4: I2 — tách cụm nlm_wrappers/sharding sang tl_core/nlm_ops.py (28 def ~1.0k dòng NGUYÊN VĂN AST-cut: 13 cmd nlm-list/get/query/cross/content/add/orphans/reconcile/query-plan + preflight/push-overflow/overflow-resolve/slot-audit + 15 helper riêng-cụm reconcile-plan/dedup-gate/overflow-route+status/slot-count/sohieu-loose/preflight-invariants…); tl.py 17097→16227 dòng; bind REBASE __globals__ (khuôn I1). Helper ĐA-CỤM GIỮ Ở TL (_entry_on_nlm_live/_resolve_nlm_notebook/_nlm_display/_nlm_probe_summary/_nlm_status_known+removed/_gws_nlm_note/_entry_nlm_notebook_id — ranh giới đo bằng đếm-tham-chiếu-ngoài-cụm). Characterization TRƯỚC cut: +5 r71a wiring-test offline (mock _imp/_gas/registry-IO) khoá 5 cmd 0-hit: nlm-list shape, reconcile DRY 3 lớp desync/other/unregistered, preflight ⚠DUP-TL lỏng-năm + verify-LIVE slot, push-overflow verified-write, overflow-resolve MAX(reg,phys)+discover+gap — PASS y nguyên sau cut. ★Bẫy mới cho I3+: default-param `cap=NLM_SLOT_CAP` eval TRƯỚC bind → module cần MIRROR constant + r71_slot_cap_mirror drift-lock. +r71 wired/no-dual → 670/670. // 1.34.3: I1 — tách cụm hygiene_report sang tl_core/hygiene.py (29 def ~2.0k dòng NGUYÊN VĂN AST-cut: sweep/dedup-plan/missing-sohieu/vbhn-year-fix/ops-plan/corpus-audit/review-queue/backfill-loai+titlevn+hieuluc/hygiene/quarantine-fix/corpus-fix/consolidation-cleanup/cat-audit/registry-doctor + helper riêng-cụm); tl.py 19052→17097 dòng; tl giữ STUB ủy quyền mọi tên đã chuyển. ★ bind() hygiene KHÁC sibling: REBASE __globals__ từng hàm về namespace SỐNG của tl (monkeypatch selftest ăn ngay, helper không stale — copy-snapshot làm r54 gãy vì patch trên tl không thấm module). Characterization TRƯỚC cut: 6 golden hygiene_* trên FIXTURE MANIFEST (env per-case TL_CACHE_DIR — _run_tl_json +env_extra) KHỚP NGUYÊN TRẠNG sau cut; +bắt 1 bug thật: sweep phơi snapshot_age_s lọt deterministic mask (+snapshot_age_s/age_s/age_seconds vào VOLATILE_JSON_KEYS). Self-heal phủ module mới (canary/tl_boot preload/py_compile/REQUIRED/r36). +r70 parity (wired + no-dual-definition) → 662/662. // 1.34.2: Pha H live-smoke HOÀN TẤT (17 bước máy user, corpus net-zero diff {changed:0,unexpected:0}, apply_ready=true 3-tier LẦN ĐẦU — proof .tl_state/smoke_18_finaldiff.json) + vá 4 phát hiện smoke: (a) reg-query +--drive-id (10 contract readback hết drift doc↔CLI); (b) nlm-add --drive-id sau add OK + row TỒN TẠI → reg_link ngay (journaled+verified, chỉ cột nlm_*; không row → nhắc register/reconcile, KHÔNG tạo row xương — đúng ca S14 'unregistered'); (c) live-smoke-plan snapshot_diff +2 allow-prefix path THẬT (live_contract_report.nlm.notebook_get.source_count + contract_checks — hết 'unexpected' oan khi ghi hợp lệ); (d) contract text khớp parser (source_delete resume +--apply; reg_delete --drive-ids; nlm_add bỏ --json). +4 r69 → 660/660. Smoke đã tập sống: resume sau đứt mạng, overflow-route khi shard đầy 306/300, guard profile-nền, CONFIRM_REQUIRED zip, nlm-reconcile DRY bắt unregistered. // 1.34.1: siết-6 advisory ĐÚNG DEADLINE r65 — contract THẬT (idempotency_contract.v1 đủ 8 field, phản ánh gate+journal+verified-write có sẵn) cho register/drive-push/nlm-reconcile/push-overflow/shared-source-fix/source-update-corpus; _CONTRACT_REQUIRED = TRỌN 12 lệnh ghi high-risk (HẾT grandfather); meta requires_confirm=True cho shared-source-fix + source-update-corpus (khớp code --apply --confirm yes); KHÔNG đổi bề mặt CLI (grilling 2026-07-09 #6). r65 drift-lock: advisory set == RỖNG; +r68 wired/complete/confirm-meta. Cùng đợt, đã vá doctrine-loss v1.34.0 trước deploy (khôi phục NGUYÊN VĂN old 164-185 vào kernel §1 — F1 MÔI TRƯỜNG THỐNG NHẤT/F5 NLM-CLI mọi-env/F4 điều-kiện-kép notebook_create/F3 ⚠DUP-TL; +luật golden-test --write & .tl_state; sửa claim cờ toàn cục --json/--out). // 1.34.0: Pha F — SKILL.md kernel 91KB→41.7KB (user duyệt (a): TRÍCH NGUYÊN VĂN bất biến §0/§1-BƯỚC-0/§2/GATES, KHÔNG viết lại lời; §4→references/COMMANDS.md 27KB; §9→references/DEPENDENCIES.md 13KB; mapping references/SKILL_KERNEL_MAPPING.md); CHANGELOG 458KB→23KB (8 version + archive references/changelog_archive/); workflow-audit +kernel_size≤48KB +kernel_links (r67); xoá DRAFT sau promotion (chống 2-bản-doctrine). SAU DEPLOY: user re-import Capabilities. // 1.33.61: CI-fix #2 (run 2 nền tảng bắt 2 lớp bug máy-phụ-thuộc): (a) idempotency_key ingest-zip hash bytes CONTAINER → zipfile 3.12≠3.13 header khác → key lệch; đổi content-v2 = norm_path+CRC32+size từng member accepted (CRC sẵn trong central directory, re-zip cùng nội dung = cùng key — đúng ngữ nghĩa idempotency; r66 khoá STORED-vs-DEFLATED cùng key); (b) 3 writer atomic (_write_text/_write_json/_emit_json_payload) thiếu newline= → Windows ghi CRLF → manifest/golden hash lệch CI; +newline LF mọi OS (r66 khoá); .gitattributes `* -text` khoá byte toàn repo; renormalize 27 file CRLF di sản + regen goldens LF. Runtime-identical — ship cùng v1.34.0. // 1.33.60: CI-fix (run #1 GitHub Actions bắt đúng bug cross-platform NGAY LẦN ĐẦU — giá trị CI tự chứng minh): fixture zip DEFLATE cho bytes KHÁC NHAU giữa build zlib (Ubuntu zlib-ng ≠ Windows) → sha256(zip) trong idempotency_key lệch 2 golden ingest_zip_dryrun_*; đổi _golden_ensure_fixtures sang ZIP_STORED (bytes chỉ phụ thuộc nội dung+metadata — máy-độc-lập thật) + regen 2 golden. Runtime-identical, KHÔNG deploy riêng — ship cùng v1.34.0. // 1.33.59: Pha G (drift-test + siết gate, theo 9 quyết định grilling 2026-07-09): (a) SIẾT-6 contract THẬT (nlm_add/recat/source_rename/source_delete/reg_delete/dedup_plan — journal/resume/readback/rollback đầy đủ) + _CONTRACT_REQUIRED fail-strict; 6 legacy còn lại advisory deadline trước v1.34.1 (r65 drift-lock đúng-set); (b) `tl bundle-export` (ADR-0001): zip giữ VERSION fork-point + BUNDLE_META.json TRONG zip; drive-push guard BLOCKED_BY_BUNDLE_META rc=3 (+--force); card bundle_export + registry meta + GENERATED spec; (c) golden nâng cấp: raw-stability (stdout thô ×2 trùng byte — nợ P4-06 đóng theo phương án canonical+raw), {FIXTURES} token, +6 case offline-thuần trên fixtures cố định (chunk profile/vbqppl-blocked, ocr-analyze, zip slip/dup NEGATIVE rc=2, live-diff no-changes), harness chấp nhận JSON dict bất kể rc (case negative có chủ đích); (d) CI GitHub Actions ubuntu+windows full-gate (autocrlf off — hash parity), .github excluded khỏi manifest/zip; .gitattributes khoá byte golden dir; BUNDLE_META vào .gitignore + EXCLUDE_NAMES. // 1.33.58: Pha E kế hoạch — tl_core/command_registry.py: metadata 52 lệnh (risk/read_only/write_scope/confirm/dry-run/det-json/workflow_task/idempotency_contract/card_required; legacy write GRANDFATHER card_required=False, advisory riêng không fail strict); E2 incremental: 8 lệnh determinism SINH parser từ GENERATED_SPECS (flags/help nguyên văn, handler qua stub tl); E3 tool-inventory đọc registry_summary; E4 workflow-audit validate_registry (cmd↔parser↔card↔contract + JSON-through-gate scan source); luật gate: ghi NGOÀI-repo phải có contract/confirm/dry-run/builtin_gate (nlm-add=dedup-live, drive-push=md5-verify), ghi local miễn. +3 r64. // 1.33.57: Pha D kế hoạch — tách tl_core/{zip_ingest,ocr,chunking}.py (~790 dòng rời tl.py; cùng máy Pha C: AST-span + bind + 21 stub; _run_child_tl/_read_local_text_for_analysis/_text_quality_metrics ở lại tl vì dùng chung ≥2 module — D4 idempotency: contracts đã ở workflow.py từ Pha C, builders đi theo lệnh sở hữu, KHÔNG tạo module riêng tránh churn); canary + tl_boot preload + py_compile + REQUIRED_FILES phủ 3 module mới. // 1.33.56: Pha C kế hoạch nợ-kỹ-thuật — tách tl_core/{workflow,release,live}.py (~1.5k dòng rời tl.py: tool-inventory/route-task/cards/golden · determinism-audit/release-manifest+verify+bundle+check · live-readiness/contract/snapshot/diff/deploy/rollback/final-acceptance/go-live). Cơ chế: cắt NGUYÊN VĂN theo AST-span + bind(tl) copy-globals (bỏ tên đã có — def riêng module thắng) + 28 stub ủy quyền trong tl (tham chiếu chéo giữa module đi qua stub tl); helper chỉ-moved-code-dùng tự móc theo module (quy tắc an toàn referenced-only-by-one-module); public CLI KHÔNG đổi. +wiring reports/determinism_report.json khi strict-fail (tên đã EXCLUDE sẵn từ bundle 50-53 mà chưa ai ghi — 2 lần flake ok:false không giữ được diff); py_compile + REQUIRED_FILES phủ 3 module mới. // 1.33.55: MERGE bundle Pha B core-json-determinism (nhánh kia TỰ ĐÁNH "1.33.54" — TRÙNG SỐ KHÁC NỘI DUNG với canonical 1.33.54, fork từ 1.33.53 nên THIẾU 4 fix merge): tách tl_core/{deterministic,jsonio}.py, tl.py giữ wrapper mỏng tương thích ngược (public CLI không đổi); PORT LẠI fix #4 vào tl_core.jsonio (schema lạ → fallback JSON — bundle mang bug cũ trở lại); +r60 parity test wrapper↔tl_core; release-check py_compile + REQUIRED_FILES phủ tl_core. // 1.33.54: MERGE bundle determinism-hardening v1.33.50-53 (fork từ 78d6bfe, +tool-inventory/route-task/workflow cards+golden/ingest-zip/ocr-run+verify/chunk/convert-verify/live-readiness+contract+snapshot/diff/release-manifest+check/determinism-audit; đánh giá: repeat-run byte-identical, release zip date_time cố định, manifest reproducible cross-platform hash khớp, zip-slip + duplicate-normalized guard, volatile scrub namespace; giữ bất biến KHÔNG tách canonical VBQPPL — chunk chỉ ref/corpus=false/goc=canonical) + 2 fix khi gộp: route-task nhận CẢ positional (bundle bắt buộc --task → gãy cách gọi cũ, drift doc↔CLI lớp S8/A1) + r59 selftest khoá PURE helpers determinism (bundle thêm ~3300 dòng mà 0 test trong gate --selftest của upload script — audit riêng không chạy tự động). // 1.33.53: deterministic hardening (volatile scrub, release artifact exclusions, zip order/duplicate guard, readiness deployment_allowed). // 1.33.52: OCR manifest determinism + idempotency contract + release hardening (Pha 8-10). // 1.33.51: live-readiness 3-tier + live-contract-check + live-state-snapshot/diff (Pha 6-7). // 1.33.50: deterministic mode + volatile JSON scrub + workflow_card.v1 schema + determinism-audit/golden-test + release-check --strict-determinism. // 1.33.49: status --amendment registry guard + backfill-hieuluc + auth script hardening. // 1.33.48: rà Instruction Project 'Luật BHXH' (profile văn bản thường tên CÓ DẤU + KHOẢNG TRẮNG) → 3 fix + 1 QoL: (P1) _apply_profile_env HẾT rơi-âm-thầm-về-nền — profile yêu cầu tường minh KHÔNG có trong config.profiles → scope RỖNG + cảnh báo PROFILE_NOT_FOUND loud (trước: prof=fallback vbqppl → TL_REGISTRY_DOC_ID/TL_NOTEBOOK_ID trỏ NỀN trong khi TL_PROFILE=tên dự án → ghi/push NHẦM corpus VBQPPL, guard NO_NOTEBOOK_ID không bắt được vì env đã bị điền); (P2) _profile_lookup chịu-lỗi-gõ: khớp không-dấu/hoa-thường/space-_- khi DUY NHẤT 1 ứng viên ('luat_bhxh'→'Luật BHXH', TL_PROFILE set tên CANONICAL để cache-dir/scope nhất quán), ≥2 ứng viên mờ → không đoán; (P3) --profile/--config nhận Ở CẢ SAU subcommand cho MỌI lệnh (Instruction dặn 'mọi lệnh truyền --profile' nhưng flag chỉ ở root → `tl reg-query --profile X` gãy rc=2; default=SUPPRESS né bẫy namespace-con copy-đè của Python mới — root-position vẫn sống); (Q) counts +registry_claim_target_nb (nlm_notebook_id==đích + live-status, đúng luật Instruction 'không đếm mọi nlm_status') + registry_claim_by_notebook breakdown — registry_claim_nlm gộp mọi shard vô dụng cho slot per-notebook. +4 r57 (620/620). // 1.33.47: MERGE bundle-45 (`tra-luat_v1.33.45.zip`, nhánh song song fork từ v1.33.43, tự đánh 44/45) + ĐỐI CHIẾU fix v1.33.46 nhánh kia (đã publish Drive) + gói vá S5/S6 rời. (1) PORT bundle-45a: _qt5_search_hints subject ưu tiên title_vn/trich_yeu CÓ DẤU (+TINH CHỈNH guard _looks_like_filename_title — bài học P0-1 v1.31.0 bundle thiếu); 45b: backfill-title-vn --out atomic qua _emit_json_payload; 45c: _nlm_auth_alive retry ×3 backoff chống AUTH_EXPIRED oan do transient (+TINH CHỈNH GIỮ M1: auth_hint BỀN sau 3 lần → RED — bundle xếp clientauthentication vào transient-final → cookie chết thật thành INCONCLUSIVE vĩnh viễn = tái false-green). (2) REIMPLEMENT fix 46: bare-VBHN matcher 1 CHIỀU `_vbhn_bare_key`+`_sohieu_query_hits_entry` — web/footnote ghi số VBHN KHÔNG năm ('88/VBHN-VPQH') vs corpus year-qualified ('88-2025-VBHN-VPQH') → exact/substring miss (năm chèn giữa) = false-negative HỆ THỐNG 'VBHN đã có mà lần nào cũng báo thiếu' (ca thật 88 Quảng cáo); query có năm giữ CHẶT (collision 50-2025≠50-2026), chiều ngược không nới; áp 6 site: reg-query, source-map direct, locate, inline/footnote in_corpus, _classify_ref+frontier. (3) Gói vá S5/S6 rời = ĐÃ PHỦ bởi v1.33.44 canonical (S5 superset _normalize_loai mọi đầu vào; S6 tương đương _cat_reg_label). +6 r56 (616/616). // 1.33.44: vá lô 8 vấn đề vận hành skill từ log Cowork 7A (S4-S14): ingest-local ghi registry SẠCH ngay tại ingest (S5 loai enum chuẩn qua _normalize_loai, S6 reg_cat NHÃN ĐỦ qua _cat_reg_label, S4 bước link cuối kèm corpus=true — hết chuỗi vá backfill-loai/recat/register sau mỗi ingest); S7 `tl journal <run> --close` SELF-HEAL inflight đã được lệnh khác hoàn tất (đối chiếu intent.set↔registry, --force ép); S8 nlm-add alias --drive/--wait (drift doc↔CLI); S11 corpus-audit Cowork 45s: gợi ý + resume_command giữ `--limit` trang nhỏ (15/lệnh); S12 sweep name_nonstandard headline = VBQPPL thật (trừ loai='thuong'+quarantine → *_other, hết 65-vs-8 phồng ảo); S13 doc source-rename 1 file/lệnh Cowork; S14 gợi ý tên source-rename: chủ đề từ title_vn (bỏ từ-loại đầu, ≤10 từ) + số hiệu gạch-nối đủ + cảnh báo SOHIEU_MISSING. +5 r55 (611/611). // 1.32.2: (log rà 69 Luật — CHẠY TRÊN v1.32.x LIVE, xác nhận gate A1/A2 hoạt động: 90-2025 OK+SUPPRESSED_CONFIRMED, 115-2026 OK+CONSOLIDATED). 4 vá: S1 `tl ping` retry ×3 backoff 2s/5s CHỈ lỗi dạng COLD-START Apps Script (404/timeout 2-3 lần gọi đầu — từng kết luận sai 'webapp chết'). S3 backfill-loai --normalize +mode CONFLICT: loai hợp-lệ-enum nhưng mâu thuẫn 2 bằng chứng đồng thuận (tên VBHN_ + sohieu -VBHN-) → đề xuất 'Văn bản hợp nhất' (ca 115-2026-VBHN mang loai='Luật' lọt danh sách Luật; chỉ ca VBHN — prefix khác nhiều ngoại lệ). S5 `_is_omnibus_entry` +nhánh ĐỀ-TÀI-TRONG-TÊN so DẠNG NÉN ('SuaDoi_QuyHoach_DauTu' strip xong dính liền — 'dau tu' có-space không khớp; ca 57-2024 registry chưa backfill goc → nhánh ≥2-ref câm, vẫn REVIEW lặp). S4 tl_fetch.sh `--setup-step core|gws|boot|nlm` (Cowork 45s/lệnh giết --setup trọn gói; bước nlm lặp cùng lệnh tới hết PARTIAL). selftest 469/469 (+3 r12). // 1.32.1: canary cred + fast-fail + NLM-read fallback. // 1.32.0: amendment-gate A1/A2/A3. (log rà 119 Luật — read-path CHẾT TOÀN BỘ mà health-check FALSE-GREEN). P1a `_gws_cred_alive` CANARY đổi token THẬT (auth_method=oauth2 KHÔNG chứng minh cred sống — ca revoke): gws-ping + doctor nay ĐỎ + remediation khi invalid_grant (doctor --offline skip canary, ghi rõ). P1b corpus-audit + backfill-title-vn FAST-FAIL (≥3 lỗi đọc liên tiếp → ABORT READ_BACKEND_DOWN thay vì cày 531×22s all-error) + `_read_doc_text_via_nlm` đường đọc DỰ PHÒNG qua nlm-content (295 nguồn live; text đã-nạp vẫn verbatim — đủ cho header/audit). P0-msg sửa khẳng định SAI 'fallback GAS vẫn đúng': GAS chỉ cứu DOWNLOAD file; exporttext (đọc text) chết theo vì webapp thiếu scope script.external_request. selftest 467/467 (+1 r12). // 1.32.0: amendment-gate A1/A2/A3 + enum điều ước + sidecar noise. (log rà 77 Luật — 3 defect lớp AMENDMENT-GATE trong _source_map_one + enum + noise). A1 canonical CONFIRMED → suppress TOÀN BỘ escalation gate (UNLINKED/VBHN_RECHECK/PAUSE/LOW_CONF; cờ AMENDMENT_GATE_SUPPRESSED_CONFIRMED; action_required nhất quán — ca 90-2025 verified vẫn bị RECHECK). A2 canonical CHÍNH LÀ VBHN: refilter ứng viên thuộc chuỗi goc CỦA CHÍNH NÓ → consolidated (khối cũ chỉ gom goc related_vbhn — rỗng khi query thẳng số VBHN, ca 115-2026 bị đòi 'tìm VBHN cho VBHN'); còn lại → VBHN_GOC_VERIFY thay VBHN_RECHECK. A3 canonical OMNIBUS (_is_omnibus_entry: cat46/sua-doi-N-luat/sửa-đổi+≥2ref) → OMNIBUS_AMENDS_OTHER, bỏ UNLINKED/LOW_CONF (hết REVIEW lặp 4 luật omnibus). A4 _LOAI_CANON +'Điều ước quốc tế'/'Công ước' (hết 56 nonmappable giả công ước ILO). B3 RAW_NAME_NOT_NLM suppress khỏi risky khi là SIDECAR cạnh GDoc (_is_source_sidecar). selftest 466/466 (+7 r11_*). // 1.31.2: U1 _sanitize_export_text (byte hỏng vỡ capture driver) + U2 _title_block_from_text tier-1 trích yếu khối tiêu đề + GWS_CRED_EXPIRED tự-chẩn-đoán + _hush selftest noise. (log LIVE vòng 3 — 2 fix gốc, tham khảo script user đã thẩm định). **U1 sanitize export-text:** driver bash vỡ capture vì byte không hợp UTF-8 trong output extract → _sanitize_export_text (diệt lone-surrogate round-trip encode-replace + bỏ control-char, giữ newline/tab) bọc MỌI nhánh _read_doc_text + cmd_extract trước khi ghi đĩa/in (stdout reconfigure sẵn có KHÔNG cứu được file --out + text chui vào JSON driver). **U2 nguồn trích yếu = KHỐI TIÊU ĐỀ:** log chứng minh --dieu 1 trả nhầm khoản phạm-vi; _title_block_from_text bóc dòng LOẠI IN HOA đứng riêng (BỘ LUẬT ưu tiên trước LUẬT — script gốc match ngược làm 91/2015 thành Luật Dân sự SAI LOẠI) + gom ĐỦ các dòng chủ đề in hoa (script gốc cap 4 dòng → cụt HIV/AIDS, quy phạm pháp) + _title_sentence_case giữ token số/ngoặc (script gốc .lower() trần); làm TIER-1 trong _title_vn_from_header (tier-2 _doc_subject_for_name giữ nguyên fallback). KHÔNG import sidecar 34 mục của phiên kia (6+ mục cụt/sai lộ ngay trong file — backfill-title-vn tự re-derive từ nguồn, registry title_vn vẫn là nguồn duy nhất). selftest 458/458 (+7 r10_*).
# Canonical version after the v1.34.45 post-audit bundle was combined and verified.
VERSION = "1.36.69"
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
# v1.34.60 (E — NLM-death resilience, ADR-7): cache verdict probe NLM per-process (notebook → {alive, why}).
# MUTABLE state PHẢI sống ở tl (bẫy I11: hàm nlm_ops rebase __globals__ về namespace tl — mutable đặt trong
# nlm_ops sẽ vô hình sau bind). Reset qua _NLM_PROBE_CACHE.clear() (selftest làm mỗi harness).
_NLM_PROBE_CACHE: dict = {}
# r198 (ADR-0014): cache version webapp per-process cho feature-detect ingest_commit (1 ping/process).
# Cùng bẫy I11 với _NLM_PROBE_CACHE — mutable PHẢI sống ở tl; reset qua _GAS_VER_CACHE.clear().
_GAS_VER_CACHE: dict = {}
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


def _add_base_also_flags(p) -> None:
    """A (v1.30.0): cặp cờ override chế độ 'profile CỘNG VBQPPL' cho lệnh ĐỌC (default None = theo TL_BASE_ALSO)."""
    p.add_argument("--base-also", dest="base_also", action="store_true", default=None,
                   help="quét THÊM nền VBQPPL+shards (mặc định BẬT ở profile dự án — v1.30.0)")
    p.add_argument("--no-base-also", dest="base_also", action="store_false",
                   help="CHỈ quét scope profile đang chọn")


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════
# PHA 0 — NỀN TẢNG CHECKPOINT/AN TOÀN (yêu cầu user: hệ thống checkpoint chống hỏng-dữ-liệu khi chạy dài).
# Ba primitive PURE (test offline), CHƯA đổi hành vi lệnh nào: (1) WAL Journal (nhật ký ghi-trước, resume/undo);
# (2) verified reg-write (đối chiếu patched==expected + validate cột schema → chống 'ghi mù' im lặng); (3) preflight
# invariant gate (gom guard rải rác → chặn clobber/mispoint/cột-sai TRƯỚC khi ghi). Bọc vào lệnh ở Pha 1.
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════


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


# ── PHA 1: bọc lệnh MUTATE qua precheck + journal + verified-write (bắt đầu ĐỔI hành vi: chặn ghi mù/clobber, resume/undo) ──


# Cột XÓA ĐƯỢC qua action `reg_clear` (khớp allowed-list doRegClear_ webapp). ⚠ GHI GIÁ TRỊ RỖNG qua reg_bulk/reg_upsert
# bị webapp BỎ QUA IM LẶNG ("empty string KHÔNG ghi đè") → muốn XÓA field PHẢI đi reg_clear — gốc 2 sự cố LIVE:
# shared-source-fix 'links_cleared:0' + register --nlm-source-id "" 'updated:true' mà không đổi.
_REG_CLEARABLE_COLS = {"nlm_source_id", "nlm_status", "nlm_pushed_at", "nlm_title", "nlm_notebook_id", "note"}


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
_TIMING_ON = bool(os.environ.get("TL_TIMINGS") or os.environ.get("TL_PERF"))   # v1.34.53 E1: TL_PERF = alias
_TIMING_LOG: list = []


def _timing_summary_lines() -> list[str]:
    """v1.34.53 (E1 — grill Q5=đo-trước-cache-sau): TỔNG KẾT cuối run cho baseline hiệu năng — tổng wall GAS,
    số call, top-5 action chậm nhất (gộp theo action). PURE trên _TIMING_LOG, test offline."""
    if not _TIMING_LOG:
        return []
    _by: dict[str, dict] = {}
    for r in _TIMING_LOG:
        s = _by.setdefault(str(r.get("action")), {"n": 0, "ms": 0})
        s["n"] += 1
        s["ms"] += int(r.get("wall_ms") or 0)
    _tot = sum(s["ms"] for s in _by.values())
    _top = sorted(_by.items(), key=lambda kv: -kv[1]["ms"])[:5]
    lines = [f"[timing] TỔNG: {len(_TIMING_LOG)} GAS call · {_tot}ms wall"]
    lines += [f"[timing]   top: {k:18s} n={v['n']:3d} sum={v['ms']:6d}ms avg={v['ms'] // max(v['n'], 1):5d}ms"
              for k, v in _top]
    return lines
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


_VBHN_KEY_RE = re.compile(r"^\d{1,5}(?:-\d{1,5})?-VBHN-([A-Z0-9D]+)$")


_DIEU_HEAD = lambda n: re.compile(r"(?m)^\s*Điều\s+%d\b" % int(n))   # NEO: `\b` sau số là ĐÚNG (chặn "Điều 7" khớp "Điều 7a")
# r296 (P16-F15): `_DIEU_ANY` là điểm DỪNG của `extract_dieu` ⇒ phải nhận cả hậu tố chữ (7a/7b/7đ).
# KHÔNG có cờ `re.I` ở đây nên phải khai TƯỜNG MINH cả chữ hoa lẫn `Đ` (khác `_slice_dieu` vốn có `(?mi)`).
_DIEU_ANY = re.compile(r"(?m)^\s*Điều\s+\d+[a-zA-ZđĐ]*\b")


_IMMUTABLE_UPSERT_COLS = {"sohieu", "goc"}   # reg_bulk BỎ IM LẶNG khi ĐỔI các cột này → phải reg_upsert (keyed drive_id)


def _looks_like_sohieu_query(q: str) -> bool:
    if re.search(r"\d{1,4}\s*[-/_]\s*(?:\d{4}|VBHN|VPQH|LCT\s*[-/_]\s*HDNN\d*)", q or "", re.I):
        return True
    # FIX-A r201 (grill 24-07 đêm — ca sống 342-QĐ/BTCTW): số Đảng/hành-chính BARE (không năm) rớt cổng cũ
    # (đòi năm/VBHN) → tier sohieu KHÔNG BAO GIỜ chạy dù _sohieu_query_hits_entry đã có phép nới D5
    # (v1.34.41). Nhận đúng khuôn _dang_bare_key: fullmatch trên KHÓA CHUẨN HOÁ toàn truy vấn — truy vấn
    # tên/câu chữ không thể khớp (không phải substring), không nới gì thêm ở tầng khớp.
    return bool(_dang_bare_key((q or "").replace("_", "-")))


def _sohieu_year(s: str) -> int | None:
    m = re.search(r"(?:[-/_]|^)(20\d{2}|19\d{2})(?:[-/_]|$)", s or "")
    return int(m.group(1)) if m else None


def _today_iso() -> str:
    import datetime as _dt
    return _dt.date.today().isoformat()


_HEADER_DATE_RE = re.compile(r"ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})", re.I)
# Cơ quan ban hành (kiểm pattern DÀI trước NGẮN vì 'quốc hội' nằm trong 'ủy ban thường vụ quốc hội'/'văn phòng quốc hội').
# v1.34.41 B.2 GĐ2 (grill D6): +cơ quan Đảng/địa phương — nhóm Đảng ĐỨNG TRƯỚC (đặc thù hơn; 'đảng ủy quốc hội'
# phải ra DU chứ không QH); 'van phong trung uong' TRƯỚC 'ban chap hanh trung uong'? — không: hai cụm không lồng nhau.
_HEADER_AGENCY_PATS = (("ban chi dao trung uong", "BCDTW"), ("ban chap hanh trung uong", "TW"),
                       ("van phong trung uong", "VPTW"), ("bo chinh tri", "BCT"), ("ban bi thu", "BBT"),
                       ("dang uy", "DU"), ("tinh uy", "TU"), ("thanh uy", "TU"),
                       ("uy ban thuong vu quoc hoi", "UBTVQH"), ("van phong quoc hoi", "VPQH"),
                       ("uy ban nhan dan", "UBND"), ("hoi dong nhan dan", "HDND"),
                       ("quoc hoi", "QH"), ("chinh phu", "CP"), ("thu tuong", "TTg"))


_HL_SUFFIX_RE = re.compile(r"\bhl\s*\d{4}([\s\-/.]\d{1,2}){0,2}\b", re.I)   # hậu tố TÊN-FILE _HL<ngày> (KHÁC _HL_DATE_RE thân-văn-bản)


_NLM_REMOVED_STATUS = {"removed", "removed_from_drive", "deleted", "trash", "trashed"}


_GOC_TAIL_RE = re.compile(r"[_\s.\-]goc[_\s.\-].*$", re.I)


_GOC_BASE_RE = re.compile(r"[_\s.\-]goc[_\s.\-]+([0-9]+[-/_][0-9A-Za-z][-/_0-9A-Za-z]*)", re.I)


# BẤT BIẾN: số hiệu VBHN PHẢI có NĂM (số VBHN tái dùng theo năm → collision). Chuẩn = NN-YYYY-VBHN-XXX.
_VBHN_NOYEAR_RE = re.compile(r"^(\d{1,5})-VBHN-([A-Z0-9D]+)$")            # NN-VBHN-XXX (THIẾU năm)
_VBHN_WITHYEAR_RE = re.compile(r"^(\d{1,5})-(19\d{2}|20\d{2})-VBHN-([A-Z0-9D]+)$")


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




_NAME_CODE_TOK = re.compile(r"^[a-z]+\d+$")   # token mã số hiệu dính chữ-số: qh15, qh13, tt09…


# P2-7 (log rà 71 luật): chuẩn hoá ENUM `loai`/`hieuluc` — registry hiện lẫn Luật/Luat, Văn bản hợp nhất/VBHN,
# Nghị định/nghi_dinh/ND/nd; hieuluc=Con/Còn → lọc/đếm theo loại KHÔNG tin cậy. Chuẩn hoá lúc register + cờ
# hygiene LOAI_NONCANONICAL (bucket riêng, KHÔNG nhét _title_flags để tránh nhiễu source-map/risky).




# A2: NHÃN QUARANTINE CHUẨN DUY NHẤT = tên folder Drive thật. Mọi đường GHI nên dùng hằng này; mọi đường ĐỌC/AUDIT
# dùng `_is_quarantine_cat` (nhận MỌI biến thể: 'QUARANTINE' code cũ, '_ZZZ_QUARANTINE_taluat' folder) → audit hội tụ
# dù nhãn lệch. `quarantine_label_variants` trong hygiene scan bắt dòng còn nhãn cũ để chuẩn hoá dần.
QUARANTINE_CAT = "_ZZZ_QUARANTINE_taluat"


# ── (HỢP NHẤT Codex v1.22.69) DEEP-RESOLVER cho lệnh ĐỌC SÂU (extract/xref/footnote-map) ──────────────
# Mạnh hơn `_canonical_for_query` cho đường đọc: ƯU TIÊN GDoc native (mime) + corpus + live, PHẠT NẶNG raw/
# quarantine; LUÔN thử by-name (tên DÀI toàn chữ-gạch-dưới như 'Luat_Phong_chong_benh_truyen_nhiem' KHÔNG còn bị


_FONT_RUN_RE = re.compile(
    r"^\s*(?:Times New Roman|Arial|Calibri|Cambria|Tahoma|Verdana|Courier New|"
    r"Wingdings|\.?VnTimeH?|VNI-Times|UTM Avo)"
    r"\s*(?:[,;]\s*\d{1,3}(?:[.,]\d+)?\s*(?:pt)?)?\s*$", re.I)


_RAW_SOHIEU_RE = re.compile(
    r"\d+[-_/]\d{4}[-_/][A-Za-zĐđ]+[A-Za-z0-9Đđ]*(?:-[A-Za-zĐđ][A-Za-z0-9Đđ]*)*|"
    r"\d+[-_/]LCT[-_/]HDNN\d+|"
    r"\d+[-_/](?:\d+[-_/])?VBHN[-_/][A-Za-zĐđA-Z0-9]+|"
    r"\d+[-_/](?:VPQH|VBHN)",
    re.I,
)
# v1.34.41 B.2 GĐ2 (grill D1): số hiệu KHÔNG-NĂM — Đảng `NN-XX/CƠQUAN` (04-CT/TW, 20-TB/CQTTBCĐ) + hành chính
# `NN/XX-CƠQUAN` (123/BC-UBND, 3260/KH-ĐĐQH). RIÊNG BIỆT với _RAW_SOHIEU_RE (không đụng _parse_sohieu_from_name/
# audit — tránh nhận nhầm 'Bao_cao_2024-2025'); CHỈ _sohieu_from_title_zone dùng, CHỈ trên dòng letterhead thuần
# 'Số …'. Mã loại cho phép chữ thường xen (TTr/CTr); mã cơ quan cho phép Đđ (norm_sohieu sẽ ra D).
_SOHIEU_NOYEAR_RE = re.compile(
    r"\d{1,5}-[A-ZĐ][A-Za-zĐđ]{1,5}/[A-ZĐ][A-ZĐđ0-9]{1,15}|"
    r"\d{1,5}/[A-ZĐ][A-Za-zĐđ]{1,5}-[A-ZĐ][A-ZĐđ0-9]{1,15}")
_SOHIEU_DANG_FULL_RE = re.compile(r"\d{1,5}-[A-ZĐ][A-Za-zĐđ]{1,5}/[A-ZĐ][A-ZĐđ0-9]{1,15}$")
_SOHIEU_HC_FULL_RE = re.compile(r"\d{1,5}/[A-ZĐ][A-Za-zĐđ]{1,5}-[A-ZĐ][A-ZĐđ0-9]{1,15}$")
_TEMPLATE_PREFIX_RE = re.compile(
    r"^(m[aã]u|mẫu|pl|phu[_\s-]*luc|phụ[_\s-]*lục|phuluc|appendix|bieu[_\s-]*mau|biểu[_\s-]*mẫu)[_\s.-]*\d{1,3}(?:\D|$)",
    re.I,
)


def _bad_cat(cat: str) -> bool:
    c = str(cat or "").strip().lower()
    return (not c) or c in ("root", "(root)", "none", "null")


_SRCMAP_GLOBAL_ONLY_FLAGS = {"NLM_STATUS_MISMATCH"}

# A3 (log rà 122 luật — tối ưu MERGE): CỔNG WARN rộng hơn cổng HIỂN THỊ. Cờ TRÔI/HYGIENE registry↔NLM đã hiện ở
# `doctor`/`sweep` (+ warning `nlm_gaps` riêng trong source-map) → KHÔNG kích `TITLE_OR_REGISTRY_WARN` per-law (đo thật:
# 12/22 luật chỉ WARN vì CORPUS_TRUE_NOT_ON_NLM/RAW_NAME_NOT_NLM của BẢN THÔ song song). Vẫn HIỂN THỊ đủ ở risky_candidates.
_TITLE_WARN_GLOBAL_FLAGS = frozenset({
    "NLM_STATUS_MISMATCH", "CORPUS_TRUE_NOT_ON_NLM", "NLM_NOTEBOOK_ID_MISSING", "RAW_NAME_NOT_NLM",
})


# ───────────────────────── external ingest gate + instruction binding ─────────────────────────
def _looks_like_new_target(x: str | None) -> bool:
    y = (x or "").strip().lower()
    return y in {"new", "new_notebook", "new-folder", "new_folder", "temp", "temporary", "notebook_tam", "tạm", "tam"} or "notebook tạm" in y or "temporary" in y


# Cụm CHUNG TIỀN TỐ nhưng KHÁC BẢN CHẤT — token phân biệt PHẢI khớp, KHÔNG match theo tiền tố chung
# (vd "bảo hiểm xã hội" ≠ "bảo hiểm y tế" ≠ "bảo hiểm thất nghiệp"; chung "bảo hiểm" → đừng coi là cùng chủ đề).
# Mỗi nhóm: (chuỗi-CHUNG, [danh sách bộ-token-PHÂN-BIỆT]). So trên text ĐÃ bỏ dấu (token ngắn 'xã'/'y tế' bị
# _subject_tokens lọc len≥3 nên phải so chuỗi). Có thể bổ sung nhóm khác khi gặp ca tương tự.
_SUBJECT_DISC_GROUPS = [
    ("bao hiem", [("xa hoi",), ("y te", "yte"), ("that nghiep",), ("tien gui",), ("nong nghiep",),
                  ("tai nan lao dong", "tai nan", "benh nghe nghiep", "tnld")]),
]


# S10 (log 2026-07-01): LUẬT/BỘ LUẬT bị SỬA ĐỔI DỒN DẬP giai đoạn cải cách 2024-2026 — với nhóm này BẮT BUỘC lượt-2
# "mới nhất" + kiểm Công báo theo năm hiện tại (Google xếp trang cũ 2017/2020 lên đầu → dễ chốt VBHN LỖI THỜI). ascii-lower.
_HIGH_AMENDMENT_SUBJECTS = (
    "hinh su", "to tung hinh su", "to tung dan su", "to tung hanh chinh", "thi hanh an",
    "phi va le phi", "phi le phi", "dat dai", "doanh nghiep", "dau tu", "dau thau", "thue",
    "chung khoan", "xay dung", "nha o", "kinh doanh bat dong san", "quy hoach", "quang cao",
    "cong chung", "dau gia", "vien chuc", "can bo cong chuc", "to chuc tin dung", "bao hiem xa hoi",
)


_ASSEMBLED_HINTS = (
    "assembled", "self assembled", "tu lap", "tu ghep", "tu tao", "lap tu",
    "ban tam", "tam thoi", "draft", "synthetic", "generated", "khong dung",
    "khong_dung", "zzz_assembled",
)

_OFFICIAL_HINTS = (
    "van phong quoc hoi", "cong bao", "vbpl", "quochoi",
    "chinhphu", "official", "_official", "629950",
)


_PROFILE_ENV_OVERLAY_KEYS = ("TL_PROFILE", "TL_ROOT_FOLDER_ID", "TL_META_FOLDER_ID", "TL_NOTEBOOK_ID",
                             "TL_REGISTRY_DOC_ID", "TL_MANIFEST_ID", "TL_OVERFLOW_NOTEBOOK_ID",
                             "TL_CATEGORIES_MODE", "TL_MANIFEST_SCOPE", "TL_BASE_ALSO",
                             "TL_PROFILE_MISSING")   # r286 (P16-F09): chốt đường ĐỌC — theo cùng overlay


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


# ============ v1.30.0 — PROFILE OPS: discover (B) / adopt (C) / doctor (D) / index (E) ============
# BẤT BIẾN LAYOUT (D): registry + manifest của profile phải nằm TRONG thư mục profile (root hoặc _meta của nó).
# Sổ cái _PROFILES_INDEX (E) là BẢN CHIẾU đọc nhanh: marker là nguồn sự thật về tồn tại/định danh,
# config là cache + lựa chọn runtime (ADR-0003); index không được trở thành nguồn-sự-thật thứ tư.

_PROFILES_INDEX_NAME = "_PROFILES_INDEX"


_PROFILES_INDEX_COLS = ["profile", "default", "rootFolderId", "folder_name", "notebookId", "registryDocId",
                        "manifestId", "categories", "manifestScope", "baseAlso", "note"]


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


_SOHIEU_PARTS_RE = re.compile(r"^(\d{1,4})-(\d{4})-(.+)$")


# ═════════════════ B3: footnote-resolver (bản đồ sửa đổi cấp Điều trong VBHN) ═════════════════
_DIEU_HEAD_RE = re.compile(r"^\s*Điều\s+(\d+[a-zđ]?)\b", re.IGNORECASE)
_KHOAN_HEAD_RE = re.compile(r"^\s*(\d+[a-zđ]?)\s*[\.\)]")   # L1: khoản có hậu tố chữ (8a, 154 K8a…)
_MARK_RE = re.compile(r"\[(\d{1,3})\]")
# r323 — MỐC «khối chú thích hợp nhất bắt đầu ở đâu». Đặt Ở ĐÂY chứ không ở `tl_core/resolve.py`
# vì `resolve.bind()` REBASE `__globals__` của từng hàm sang namespace SỐNG của tl ⇒ hằng khai bên
# resolve là MÃ CHẾT, hàm vẫn tra trong globals của tl (đúng lý do `_MARK_RE` nằm đây; selftest bắt
# được ngay khi tôi thử khai bên resolve — NameError trên đường sản xuất).
# Đường ĐỌC dùng nó cắt `foot_region`; đường NẠP dùng `verify_deep.VBHN_CHU_THICH_DEF` — hai module
# KHÔNG import lẫn nhau (tl_core chưa bao giờ nạp script gốc `scripts/`) nên bất biến «cùng một mốc»
# do drift-lock `r323_khuon_chu_thich_khong_duoc_lech` canh.
_FOOT_DEF_FIRST = re.compile(r"(?m)^\s*\[\d{1,3}\]\s")
_HL_DATE_RE = re.compile(r"hiệu lực[^0-9]{0,40}?(\d{1,2})\s*[/\-.]\s*(\d{1,2})\s*[/\-.]\s*(\d{4})", re.IGNORECASE)
# VBHN dùng chữ: "có hiệu lực kể từ ngày 01 tháng 7 năm 2026" → bắt riêng (đây là gốc lỗi pending=0).
_HL_DATE_VN_RE = re.compile(r"hiệu lực[^0-9]{0,40}?ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})", re.IGNORECASE)


# B1 def-driven (26/6): parse 1 chú thích thành bản ghi sửa đổi ĐỘC LẬP.
# B3 (84/2025): nhận thêm "Cụm từ '…' được BỎ / THAY THẾ BẰNG '…' theo…" (verb 'bỏ'/'thay thế' yêu cầu được/bị
# đứng trước → tránh dương-tính-giả với 'bỏ' lẻ). Giữ nguyên các verb cũ (alt sau) cho tương thích.
_AMEND_VERB_RE = re.compile(
    r"(?:được|bị)\s*(?:bỏ|thay thế(?:\s+bằng)?)\b"
    r"|(?:được|bị)?\s*(sửa đổi(?:,?\s*bổ sung)?|bổ sung|bãi bỏ|thay thế|hủy bỏ)\b", re.IGNORECASE)
_POS_RE = re.compile(r"(?:điểm\s+([a-zđ]{1,3}\d?)\s+)?(?:khoản\s+(\d+[a-zđ]?)\s+)?Điều\s+(\d+[a-zđ]?)", re.IGNORECASE)
_AMEND_LAW_RE = re.compile(r"của\s+(?:Bộ\s+luật|Luật)\b[^0-9]{0,90}?số\s+(\d{1,4}\s*/\s*\d{4}\s*/\s*[A-ZĐa-zđ\-]+\d*)", re.IGNORECASE)
_DIEMLIST_RE = re.compile(r"diem\s+([a-z]{1,3}\d?(?:\s*(?:,|va|;)\s*(?:diem\s+)?[a-z]{1,3}\d?)+)")


def _hieuluc_date_display(iso: str | None) -> str:
    if not iso:
        return ""
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", str(iso))
    return f"{m.group(3)}/{m.group(2)}/{m.group(1)}" if m else str(iso)


_INLINE_AMEND_RE = re.compile(
    r"(?:Sửa đổi(?:,?\s*bổ sung)?|Bổ sung)\s+(?:một số điều của\s+)?"
    r"(?:Bộ\s+luật|Luật|Pháp lệnh|Nghị quyết)\s+(?:[^.;:\n0-9]{0,60}?)\s*"
    r"số\s+(?P<sh>\d{1,4}/\d{4}/[A-ZĐ][A-Z0-9Đ\-]*)", re.IGNORECASE | re.UNICODE)


# BUG#4: chú thích sửa đổi CẮT-NGANG / BÃI-BỎ-CỤC-BỘ phải HẠ ƯU TIÊN trong footnote-map — đừng để ngang hàng luật
# sửa chuyên đề (dễ hiểu nhầm phải nạp cả luật quy hoạch/thanh tra/omnibus). Phát hiện TỪ NGUYÊN VĂN chú thích:
#   CROSS_CUTTING = luật sửa "một số điều của <N>/các/nhiều luật" hoặc "<N> luật … có liên quan" (35/2018 quy hoạch…).
#   PARTIAL_REPEAL = loại='bãi bỏ' VÀ phạm vi hẹp (chỉ 1 khoản/điểm, không bãi cả Điều) — vd 32/2013 bỏ 1 khoản TNDN.
_FOOTNOTE_CROSSCUT_RE = re.compile(
    r"(?:mot so dieu cua\s+(?:\d+|cac|nhieu)\s+luat|"
    r"sua doi,?\s*bo sung\s+(?:\d+|mot so|cac|nhieu)\s+luat|"
    r"\d+\s+luat\b|cac luat\b|nhieu luat\b|luat\b[^.]{0,40}\bco lien quan)",
    re.IGNORECASE)


_RAW_EXT_RE = re.compile(r"\.(docx?|pdf|html?|rtf|txt|odt)$", re.I)


NLM_SLOT_CAP = 300   # cap nguồn/notebook NLM (khớp slots.cap webapp). Dùng cho ingest-missing/slot guard.
# r208: ngưỡng gắn cờ lệch registry↔LIVE ở slot-audit --all-shards. HẰNG SỐ ⇒ khai Ở CẢ HAI NƠI
# (tl + tl_core/nlm_ops) như NLM_SLOT_CAP, KHÔNG cho vào _STUB_MAP — trạm stub biến tên thành HÀM,
# hàm rebase globals sang tl sẽ nhận function thay vì int (bẫy đã trả giá khi làm r208).
_SLOT_LIVE_DIFF_WARN = 2


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


# Discovery DÙNG CHUNG: tìm văn bản trên web = Google `site:` + VBHN-first.
# Áp cho MỌI tính năng tìm-văn-bản-web: fetch-route/links + QT-5 (vbhn-check/status/relation-check).
# G1 [FIX]: OFFICIAL-FIRST — vbpl.vn (CSDL quốc gia) > congbao.chinhphu.vn (Công báo) > luatvietnam > thuvienphapluat.
_DISCOVERY_SITES = ("vbpl.vn", "congbao.chinhphu.vn", "luatvietnam.vn", "thuvienphapluat.vn")


# C2(b)/C4 (đặc tả 26/6): thư mục _HOP_NAP trên Drive để người dùng thả file (link bấm-được, KHÔNG URL trần).
HOPNAP_FOLDER_ID = "1bNSAKGACtk0x0cqX5QRVEGT12udi2g67"


# ═════════════════ E2: subject-cluster map ('pháp luật về X' → số hiệu canonical) ═════════════════
_SUBJECT_CLUSTERS_CACHE = None


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
# r251: allowlist phần mở rộng của `profile-ingest` — ĐẶT TÊN thay vì set trần trong thân hàm, để cầu nối
# chunk (`_chunk_ingest_target`) và test neo vào ĐÚNG hợp đồng này, không neo vào một bản COPY sẽ trôi lệch.
# Định nghĩa Ở ĐÂY vì `ingest_ops.bind` re-home `__globals__` về namespace tl (bẫy I11) — hằng để ở
# ingest_ops thì hàm re-home KHÔNG thấy.
PROFILE_INGEST_ALLOWED_EXTS = frozenset({".docx", ".doc", ".pdf", ".rtf", ".odt", ".xlsx", ".xls"})


# (4) Gợi ý CHỦ ĐỀ ĐÚNG theo Bộ pháp điển (Quyết định 843/QĐ-TTg) cho lĩnh vực dễ gán nhầm.


# Từ khóa MẠNH → mã chủ đề pháp điển (ASCII, theo phap_dien_45.json). Chỉ tín hiệu rõ để cat-audit ít nhiễu.


# Hint cho ingest (lĩnh vực dễ gán nhầm) — dẫn xuất từ map chính thức ở trên (đã sửa: hình sự=16, DN=12, giao thông=14).
_CAT_REVIEW_HINTS = {"tố tụng": "37", "xuất nhập cảnh": "01", "hình sự": "16", "doanh nghiệp": "12", "giao thông": "14", "kế toán": "17"}


# ───────────────────────── G3: phân loại theo NỘI DUNG + quy tắc ranh giới ─────────────────────────


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


_RAW_LOOSE_SOHIEU_RE = re.compile(
    r"(?i)(?<![0-9A-Za-zĐđ])(ND|NĐ|TT|QD|QĐ|NQ|PL|CT|TTLT|BLDS|BLHS|L)?[\s_\-\.]*?(\d{1,4})[\s_\-\.]+((?:19|20)\d{2})(?![0-9])")


# ══════════ Corpus cleanup: orchestrator (corpus-fix) + source CRUD (source-rename) + fixer (shared-source-fix) ══════════
# Nguyên tắc: DRY/plan mặc định; ghi Drive/NLM/registry = --apply LIVE (Cowork). THỨ TỰ SỬA cố định (sai thứ tự=hỏng thêm).
# Tầng: safe_auto (reversible: corpus=false) auto khi --apply --tier safe; còn lại in lệnh + người duyệt.


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
    # v1.34.39 (audit 2026-07-13 FP: NQ_71-2025-UBTVQH15 'nhiệm vụ, cơ cấu HỘI ĐỒNG DÂN TỘC + các Ủy ban' bị
    # pin đề xuất 35→10): 'dân tộc' trong cụm 'Hội đồng Dân tộc' là TÊN CƠ QUAN Quốc hội (tổ chức bộ máy),
    # không phải chính sách dân tộc — lookbehind loại; văn bản nhắc CẢ 'chính sách dân tộc' vẫn pin bình thường.
    (re.compile(r"(?<!hoi dong )\bdan toc\b"), "10", "dân tộc = 10 (§0.13)"),
)


_DECLARED_LOAI_MAP = (("van ban hop nhat", "Văn bản hợp nhất"), ("bo luat", "Bộ luật"),
                      ("phap lenh", "Pháp lệnh"), ("nghi dinh", "Nghị định"),
                      ("thong tu lien tich", "Thông tư liên tịch"), ("thong tu", "Thông tư"),
                      ("nghi quyet", "Nghị quyết"), ("quyet dinh", "Quyết định"),
                      ("hien phap", "Hiến pháp"),
                      # v1.34.40 B.2: loại VĂN BẢN THƯỜNG khai báo letterhead (HƯỚNG DẪN/KẾ HOẠCH… dòng IN HOA
                      # đứng riêng) — thiếu thì blank-over-guess không bao giờ nhận được bằng chứng hợp lệ.
                      ("huong dan", "Hướng dẫn"), ("ke hoach", "Kế hoạch"), ("de an", "Đề án"),
                      ("thong bao", "Thông báo"), ("cong van", "Công văn"), ("to trinh", "Tờ trình"),
                      ("phat bieu", "Phát biểu"), ("bao cao", "Báo cáo"), ("chi thi", "Chỉ thị"),
                      ("ket luan", "Kết luận"), ("cong dien", "Công điện"), ("phu luc", "Phụ lục"),
                      # v1.34.41 B.2 GĐ2 (grill D8): loại VB Đảng khai báo letterhead — 'quy dinh' KHÔNG đụng
                      # 'quyet dinh' (so exact/prefix-từ, 'quye'≠'quy '); ca thật QĐ 383-QĐ/TW ruột là QUY ĐỊNH.
                      ("quy dinh", "Quy định"), ("chuong trinh", "Chương trình"), ("quy che", "Quy chế"),
                      ("dieu le", "Điều lệ"), ("thong tri", "Thông tri"),
                      ("luat", "Luật"))


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


_VOLATILE_JSON_KEYS = _tl_det.VOLATILE_JSON_KEYS   # v1.33.55: nguồn chuẩn ở tl_core.deterministic


def _deterministic_enabled(a=None) -> bool:
    return _tl_det.deterministic_enabled(a, default_on=_DETERMINISTIC_ON)


def _stable_string_for_json(s: str) -> str:
    return _tl_det.stable_string_for_json(s, project_root=HERE.parent)


def _scrub_volatile(obj):
    return _tl_det.scrub_volatile(obj, project_root=HERE.parent)


def _print_json_or_text(obj: dict, as_json: bool) -> None:
    return _tl_jsonio.print_json_or_text(obj, as_json, json_dumps_func=_json_dumps)


# ───────────────────────── convert / rename readback verification ─────────────────────────
_GDOC_MIME = "application/vnd.google-apps.document"
_GSHEET_MIME = "application/vnd.google-apps.spreadsheet"   # v1.34.6 #2: canonical bảng tính = Google Sheet


def _file_mime(info: dict) -> str:
    f = info.get("file") or {}
    return str(f.get("mimeType") or f.get("mime") or "").strip()


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
            src = path
            # v1.34.58 (C-#10 — Q10): path phi-ASCII (vd `D:\Dữ liệu\…`) → pdftotext build Git Bash/cp1258
            # nhận arg hỏng, im lặng không ra output → copy sang temp ASCII rồi chạy trên bản copy
            # (tự xoá theo TemporaryDirectory; %TEMP% của user là ASCII).
            try:
                str(path).encode("ascii")
            except UnicodeEncodeError:
                src = Path(td) / ("in" + ext)
                shutil.copyfile(path, src)
            try:
                subprocess.run([exe, "-layout", str(src), str(out)], timeout=30, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if out.exists():
                    return out.read_text(encoding="utf-8", errors="replace")[:max_chars], warnings
            except Exception as e:
                return "", [f"PDFTOTEXT_ERROR:{type(e).__name__}"]
        return "", ["PDFTOTEXT_NO_OUTPUT"]
    return "", ["TEXT_EXTRACTION_NOT_IMPLEMENTED_FOR_EXT:" + ext]


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


def _path_age_days(path: Path) -> float | None:
    try:
        if not path.exists():
            return None
        return round(max(0.0, (time.time() - path.stat().st_mtime) / 86400.0), 3)
    except Exception:
        return None


def _file_auth_state(path: Path) -> dict:
    try:
        exists = path.exists()
        return {"path": str(path), "exists": exists,
                "age_days": _path_age_days(path) if exists else None}
    except (OSError, PermissionError) as e:
        # Report-only health checks must not crash when a sandbox denies stat().
        return {"path": str(path), "exists": False, "age_days": None, "error": type(e).__name__}


def _sha256_path_or_empty(path: str) -> str:
    try:
        p = Path(path).expanduser()
        return _sha256_file(p) if p.exists() and p.is_file() else ""
    except Exception:
        return ""


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


# ───────────────────────── selftest (offline) ─────────────────────────
def _selftest_pin_profile():
    """(r181) Bare selftest phải HERMETIC w.r.t. defaultProfile máy: ghim TL_PROFILE=DEFAULT_PROFILE để
    _profile_cache_dir()==CACHE. Không ghim thì máy có defaultProfile≠vbqppl (vd S10 «Luật BHXH») → cache rơi
    vào subdir profile CHƯA tồn tại trong temp → checkpoint resume ghi hụt (r20/r30 đỏ giả). Trả old để restore."""
    _old = os.environ.get("TL_PROFILE")
    os.environ["TL_PROFILE"] = DEFAULT_PROFILE
    return _old


def _selftest_restore_profile(old) -> None:
    if old is None:
        os.environ.pop("TL_PROFILE", None)
    else:
        os.environ["TL_PROFILE"] = old


def _selftest_seal_env():
    """r262 — THI HÀNH lời hứa "A bare selftest must be hermetic" ngay dưới đây (trước chỉ đúng cho
    CACHE + profile, còn MẠNG và CREDS thì không). Trả callable hoàn nguyên.

    ĐO ĐƯỢC 30-07: bare selftest gọi 11 lần ra MẠNG THẬT từ >=6 chỗ (tl_selftest 2646 · 5317 _cap72 ·
    5596 _cap75 · 7253 · 7261 · 15437) tới script.google.com/exec, oauth2.googleapis.com/token,
    drive/v3/files. Hậu quả KÉP:
      · thời gian gate BẤT ĐỊNH — `ingest_claim` 404 retry 5s+15s, timeout GET 120s ⇒ có lượt >580s,
        `deploy-package.sh --push` chết ở bước 1 dù cây lành;
      · KHÔNG hermetic theo CẢ HAI chiều — máy KHÔNG creds thì `cmd_doc_text`→`load_creds` sys.exit CỨNG
        (test r183) giết cả bộ trước khi in tổng; máy CÓ creds thì kết quả phụ thuộc mạng người khác.

    Vá ở MỘT chỗ, không phải 6: cả 6 chỗ đó là dò-PHỤ mà thất bại vốn đã được bỏ qua — đo bằng cách chặn
    sạch mạng thì 1425/1425, 0 test đỏ, còn NHANH HƠN 10s. Sửa từng chỗ = 6 lần đoán ý test người khác.

    (1) MẠNG: `urlopen` → `URLError` — ĐÚNG tín hiệu máy-không-mạng mà các nhánh fallback đó vốn xử lý,
        KHÔNG phải exception lạ. Lối ra tường minh: `TL_SELFTEST_ALLOW_NET=1`.
    (2) CREDS: chỉ ghim khi THIẾU (máy có creds thật KHÔNG bị đụng) — `.invalid` là TLD DỰ TRỮ RFC 2606,
        không bao giờ resolve, nên kể cả ai tắt (1) thì vẫn không chạm máy thật.
    """
    import urllib.request as _ur, urllib.error as _ue
    _undo = []
    if str(os.environ.get("TL_SELFTEST_ALLOW_NET", "")).strip().lower() not in ("1", "true", "yes", "on"):
        _real_urlopen = _ur.urlopen

        def _no_net(*_a, **_k):
            raise _ue.URLError("TL_SELFTEST_NO_NET: selftest chặn mạng (hermetic). "
                               "Cần mạng thật: TL_SELFTEST_ALLOW_NET=1")
        _ur.urlopen = _no_net
        _undo.append(lambda: setattr(_ur, "urlopen", _real_urlopen))
    for _k, _v in (("TL_WEBAPP", "https://tl-selftest.invalid/exec"), ("TL_TOKEN", "tl_selftest_dummy")):
        if not str(os.environ.get(_k, "")).strip():
            os.environ[_k] = _v
            _undo.append(lambda k=_k: os.environ.pop(k, None))

    def _restore():
        for _f in reversed(_undo):
            try:
                _f()
            except Exception:  # noqa: BLE001 — dọn best-effort, không che lỗi test
                pass
    return _restore


def selftest() -> int:
    global CACHE

    def _run() -> int:
        try:
            ts = _imp("tl_selftest"); ts.bind(sys.modules[__name__])
        except Exception as e:  # noqa: BLE001 — tl_selftest hỏng do mount → báo, không crash câm
            print(f"[tl] selftest: không nạp được tl_selftest.py ({type(e).__name__}: {e})", file=sys.stderr)
            return 1
        return ts.run()

    # A bare selftest must be hermetic. Previously it wrote to ~/.tra_luat_cache
    # and could fail before testing anything in restricted environments.
    # (r181) Cũng phải ĐỘC LẬP defaultProfile máy — ghim TL_PROFILE=DEFAULT_PROFILE (restore ở finally NGOÀI).
    _prof_old = _selftest_pin_profile()
    _seal_undo = _selftest_seal_env()          # r262: chặn mạng + ghim creds giả (xem docstring)
    try:
        if os.environ.get("TL_CACHE_DIR"):
            return _run()
        old_cache = CACHE
        old_env = os.environ.get("TL_CACHE_DIR")
        with tempfile.TemporaryDirectory(prefix="tra-luat-selftest-") as td:
            CACHE = Path(td)
            os.environ["TL_CACHE_DIR"] = td
            try:
                return _run()
            finally:
                CACHE = old_cache
                if old_env is None:
                    os.environ.pop("TL_CACHE_DIR", None)
                else:
                    os.environ["TL_CACHE_DIR"] = old_env
    finally:
        _seal_undo()
        _selftest_restore_profile(_prof_old)


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


# Lệnh TỰ LO creds (chạy được khi THIẾU webapp/token) → KHÔNG gọi load_creds tự động.
# Tách hằng nhiều dòng: KHÔNG để 1 dòng >800 ký tự (vài trình nạp skill cắt cụt file ở dòng quá dài).
# gws-ping/transport-info = chẩn đoán transport gws, KHÔNG cần webapp creds.
_CREDS_LAZY_CMDS = frozenset({
    "boot", "locate", "exists", "source-map", "relation-check", "relation-backfill", "external-ingest",
    "instructions", "instruction-audit", "tool-inventory", "route-task", "workflow-audit", "determinism-audit", "golden-test", "release-check", "release-manifest", "release-verify", "test-fragments-check", "release-bundle", "bundle-export", "live-readiness", "live-contract-check", "live-state-snapshot", "live-state-diff", "live-smoke-plan", "deploy-plan", "rollback-plan", "final-acceptance", "go-live-runbook", "link-priority", "profile-info", "config-pin-registry", "profile-list", "profile-use",
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
    "doc-text",   # v1.34.60 A1 (bug CI bắt: thiếu → main() load_creds sys.exit TRƯỚC handler dù cache không cần token) — offline-first, export/download tự lo cred
    "doc-compare", "dedup-corpus",   # v1.34.63 A2+B1 (cùng lớp doc-text): local×local/cache/DRY chạy không token; handler tự best-effort load_creds khi cần export
    "up",   # tl up TỰ bootstrap cred (init-config --from-public) → KHÔNG để main() sys.exit khi phiên trống; cmd_up tự gọi load_creds
    "doc-patch",   # r217: sửa-theo-điểm chạy HOÀN TOÀN trên record cache cục bộ — không webapp, không Drive, không NLM
    "doc-claims-check",   # r218: chỉ đọc file .md + git cục bộ — GOTCHAS §4: thiếu dòng này thì main() load_creds sys.exit TRƯỚC handler trên máy không config
    # r226 (CI ĐỎ ≥9 run từ 27-07, ubuntu+windows, luôn chết ở ca r216_merge_fail_closed_tren_duong_san_xuat)
    # — ĐO: máy dev có tra_luat_config.v2.json (.gitignore:7) nên `tl rasoat-merge` chạy được; runner CI
    # clone SẠCH nên main() sys.exit rc=1 TRƯỚC handler ⇒ stdout RỖNG ⇒ test parse JSON gãy. Không phải
    # khác OS, không phải khác Python (đo 3.12 và 3.13 cùng đỏ trên máy không config, cùng xanh khi có).
    # Cùng LỚP với dòng doc-claims-check ngay trên. Bằng chứng riêng cho từng lệnh:
    "rasoat-merge",   # handler tự khai "Không gọi mạng, không NLM" — thuần cục bộ, không có đường dùng creds
    "state-get",      # handler CÓ `except SystemExit → CAN_WEBAPP_LIVE` (rc=2 + JSON) nhưng là CODE CHẾT khi main() thoát trước
    "state-put",      # nhánh `--dry-run` return TRƯỚC load_creds (cục bộ thuần) + cùng `CAN_WEBAPP_LIVE` chết như trên
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
    finally:
        if _TIMING_ON:   # v1.34.53 (E1): tổng kết baseline — bật bằng --timings / TL_TIMINGS=1 / TL_PERF=1
            for _tl_ln in _timing_summary_lines():
                print(_tl_ln, file=sys.stderr)


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
_tl_resolve = _tl_core_import("resolve")          # noqa: E402 — I9b v1.34.14
_tl_regio = _tl_core_import("regio")              # noqa: E402 — I9b v1.34.14
_tl_cli = _tl_core_import("cli")                  # noqa: E402 — I11 v1.34.18
_tl_zip_ingest = _tl_core_import("zip_ingest")   # noqa: E402 — Pha D (v1.33.57)
_tl_ocr = _tl_core_import("ocr")                 # noqa: E402
_tl_chunking = _tl_core_import("chunking")       # noqa: E402
_tl_doc_identity = _tl_core_import("doc_identity")   # noqa: E402 — A2 v1.34.63 (identity nội dung dùng chung)
_tl_source_ops = _tl_core_import("source_ops")       # noqa: E402 — ĐỢT A v1.34.64 (source-CRUD tách từ ingest_ops, kế hoạch guard-va-boc-tl-core §4)
_tl_nlm_admin_ops = _tl_core_import("nlm_admin_ops")   # noqa: E402 — ĐỢT B v1.34.65 (đường GHI+audit NLM tách từ nlm_ops, kế hoạch §5 — ranh giới GHI/ĐỌC)
_tl_the_thuc = _tl_core_import("the_thuc")             # noqa: E402 — R2 v1.34.75 (kiểm thể thức docx, kế hoạch the-thuc 2026-07-19)
_tl_registry = _tl_core_import("command_registry")   # noqa: E402 - Pha E (module thuần, không bind)


# ── I1 (v1.34.3): stub ủy quyền cụm hygiene → tl_core/hygiene.py (mọi caller cũ giữ nguyên) ──


# ── I2 (v1.34.4): stub ủy quyền cụm nlm_wrappers → tl_core/nlm_ops.py (mọi caller cũ giữ nguyên) ──


# ── I3 (v1.34.5): stub ủy quyền extract_cache + fetch_web → tl_core/ (mọi caller cũ giữ nguyên) ──


# ── I4 (v1.34.7): stub ủy quyền cụm profile_mgmt → tl_core/profile_mgmt.py ──


# ── I5 (v1.34.8): stub ủy quyền cụm ingest_pipeline → tl_core/ingest_ops.py ──


# ── I6 (v1.34.9): stub ủy quyền cụm lookup → tl_core/lookup_ops.py (mọi caller cũ giữ nguyên) ──


# ── I8 (v1.34.12): stub ủy quyền nhóm lệnh vận-hành/chẩn-đoán → tl_core/ops_misc.py ──


# ── I9a (v1.34.13): stub ủy quyền infra classify + profile_env → tl_core/ ──


# ── I9b (v1.34.14): stub ủy quyền infra resolve + regio → tl_core/ ──


# I9b: biến cache module-level của _load_linhvuc (hàm rebase về globals tl nên cache PHẢI sống ở đây;
# bị máy-cắt off-by-one nuốt vì nằm SÁT def không dòng trống — bài học: xoá từ đúng dòng def).
_LINHVUC_CACHE = None


# ── I10 (v1.34.15): STUB-FARM DATA-DRIVEN — thay ~488 def ủy quyền 2-dòng bằng bảng + factory.
# Mỗi stub: __name__=tên thật (parser-surface bất biến), __tl_stub__=(module, name) làm drift-lock
# (r81 + các r7x wired-check đối chiếu marker thay getsource). KHÔNG def tay stub mới — thêm vào bảng.
_STUB_MAP = {
    "cli": [
        'build_parser',   # I11
    ],
    "chunking": [
        '_chunk_plan_from_text', '_chunk_records_from_text', 'cmd_chunk_apply', 'cmd_chunk_plan', 'cmd_chunk_verify', 'cmd_profile_ingest_chunks',
    ],
    "classify": [
        '_discover_item_kind', '_expand_abbrev', '_nlm_status_removed',   # I11
        '_alias_cat_pairs', '_ascii_lower', '_backfill_titlevn_candidates', '_cat_alias_evidence_for', '_cat_bare_full_variants', '_cat_boundary_rule',
        '_cat_likely_wrong_suggest', '_cat_reg_label', '_cat_taxonomy', '_clean_ref_name_phrase', '_clean_subject_text', '_compact_phrase',
        '_declared_loai_from_header', '_derive_subject_from_entries', '_disc_conflict', '_discover_classify', '_distinct_target_luat_subjects', '_doc_subject_for_name', '_doc_subject_key',   # +_distinct_target_luat_subjects v1.34.39
        '_entry_name', '_entry_subject_text', '_expected_cat_from_alias', '_extract_header_facts', '_file_name', '_has_diacritics',
        '_infer_cats', '_infer_cats_text', '_infer_loai', '_is_omnibus_entry', '_is_raw_no_gdoc_name', '_is_treaty_entry',
        '_is_valid_cat_value', '_load_subject_clusters', '_loai_is_noncanonical', '_looks_like_filename_title', '_name_content_tokens', '_name_goc_base_key',
        '_name_is_template_or_appendix', '_name_key', '_name_looks_nonstandard', '_name_phrase_match', '_name_prefix_family', '_name_strong_match',
        '_name_structural_issues', '_name_subject_match', '_name_subject_text', '_name_subset_match', '_name_tail_key', '_name_tail_pretty',
        '_nlm_status_known', '_nlm_status_write_ok', '_norm_cat', '_normalize_loai', '_omnibus_name_evidence', '_omnibus_name_text', '_parse_sohieu_from_name',
        '_profile_title_from_header', '_resolve_cat_folder', '_resolve_cat_folder_impl', '_selected_profile_name', '_strip_accents', '_subject_is_boilerplate',
        '_subject_score', '_subject_sig', '_subject_tokens', '_subject_tokens_for_entry', '_title_block_from_text', '_title_flags',
        '_title_sentence_case', '_title_vn_from_header', '_title_vn_from_plan', '_title_vn_from_tukhoa', '_vb_auto_cat_from_text', '_vb_standard_doc_name',
        '_vb_title_short_for_name', '_verify_header_match',
    ],
    "extract_cache": [
        '_find_nfc', '_sanitize_export_text', 'extract_dieu',   # I11
        '_extract_resolve_entries',   # r180 S3 base-also cho resolve --sohieu (note CUỐI dòng — I11)
        '_consolidated_text',   # r215 dựng lại ĐỦ khối đầu+Điều+phụ lục (note CUỐI dòng — I11)
        'cmd_cache_build', 'cmd_cache_snapshot', 'cmd_extract',
    ],
    "fetch_web": [
        '_external_format_class', '_google_site_url', '_query_variants', '_runtime_env', 'extract_refs',   # I11
        '_external_ingest_plan', '_fetch_plan', '_frontier_candidates', '_frontier_doc_text', 'cmd_external_ingest', 'cmd_fetch_batch',
        'cmd_fetch_links', 'cmd_fetch_route', 'cmd_find_doc', 'cmd_frontier_expand', 'cmd_link_priority', 'cmd_tvpl_url',
    ],
    "hygiene": [
        '_apply_quarantine', '_audit_row_flatten', '_cluster_matches', '_corpus_count_server_rule', '_entry_is_corpus_effective', '_corpus_fix_plan', '_dedup_lite', '_dedup_plan', '_emit_json_payload', '_goc_pollution_groups', '_hieuluc_from_header_text', '_is_chunk_part_name', '_is_infra_entry', '_is_quarantine_cat', '_is_quarantine_label_variant', '_print_reconcile', '_raw_dup_of_standard_rows', '_read_doc_text_via_nlm', '_reconcile_clusters', '_resolve_headerverify_targets', '_rq_rel_strong', '_select_hygiene_clusters', '_sohieu_dup_group_real',   # I11 (+_is_chunk_part_name v1.34.38, +_entry_is_corpus_effective v1.34.42 BUG3)
        '_backfill_hieuluc_candidates', '_backfill_loai_candidates', '_consolidation_cleanup_plan', '_corpus_audit_row', '_hygiene_groups', '_ops_plan_add',
        '_ops_plan_report', '_quarantine_clear_stale', '_quarantine_fix_items', '_review_queue_report', '_sweep_report', '_vbhn_year_complete',
        '_src_id_dup_groups',   # v1.36.46 r312/ING-09 — bind() re-home __globals__ về tl ⇒ helper MỚI phải khai ở đây, không thì NameError lúc chạy
        '_vbhn_year_fix_items', 'cmd_backfill_hieuluc', 'cmd_backfill_loai', 'cmd_backfill_titlevn', 'cmd_cat_audit', 'cmd_consolidation_cleanup',
        'cmd_corpus_audit', 'cmd_corpus_fix', 'cmd_dedup_plan', 'cmd_hygiene', 'cmd_missing_sohieu', 'cmd_ops_plan',
        'cmd_quarantine_fix', 'cmd_registry_doctor', 'cmd_review_queue', 'cmd_sweep', 'cmd_vbhn_year_fix',
        '_dedup_corpus_candidates', '_dedup_corpus_classify', '_dedup_corpus_content', '_dedup_corpus_pick_canonical', '_dedup_md5_cluster', '_dedup_sohieu_reps', 'cmd_dedup_corpus',   # v1.34.63 B1 (note CUỐI dòng — I11)
    ],
    "doc_identity": [
        '_bow_jaccard', '_bow_tokens', '_compare_signals', '_content_hash', '_doc_compare_read', '_doc_compare_resolve', '_doc_norm', '_doc_type_kind', '_sohieu_cmp_key', 'cmd_doc_compare',   # v1.34.63 A2 (note CUỐI dòng — I11)
    ],
    "the_thuc": [
        '_the_thuc_criteria', 'the_thuc_neo_lines', '_tt_range', '_tt_mm', '_the_thuc_parse_docx',
        '_the_thuc_detect_he', 'the_thuc_check', 'cmd_the_thuc_check',   # R2 v1.34.75 (note CUỐI dòng — I11)
        '_the_thuc_check_t2', '_the_thuc_check_t3',   # R3 v1.34.77 T2/T3 (note CUỐI dòng — I11)
        'the_thuc_normalize', 'cmd_the_thuc_normalize',   # R4 v1.34.78 (note CUỐI dòng — I11)
        '_tt_chuan_hoa_space', '_tt_loose_key', '_tt_dong_gan_dung', '_the_thuc_wrap_scan',   # r143 v1.34.83 (note CUỐI dòng — I11)
        '_the_thuc_check_layout', '_tt_p', '_tt_so_nbsp', '_tt_gach', 'the_thuc_build', 'cmd_the_thuc_build',   # r144/r145 v1.34.84 (note CUỐI dòng — I11)
        '_tt_ghi_docx',   # r155 v1.34.87 tách đóng gói docx (note CUỐI dòng — I11)
        '_phieu_trinh_build',   # r156 v1.34.87 dựng Phiếu trình (note CUỐI dòng — I11)
        '_tt_can_dong',   # r164 v1.34.95 cân dòng tên cơ quan (note CUỐI dòng — I11)
        '_tt_dac_ta',     # r170 v1.35.0 bảng đặc tả thành phần × hệ (note CUỐI dòng — I11)
        '_tt_co_build',   # r174 v1.35.4 cỡ chữ builder dẫn xuất từ bảng (note CUỐI dòng — I11)
        '_tt_dac_ta_bien_the',   # r175 v1.35.5 biến thể theo mẫu — trục thứ ba (note CUỐI dòng — I11)
        '_tt_dt_phan_loai', '_the_thuc_check_dac_ta',   # r176 v1.35.6 bước 5 nối bộ kiểm đọc bảng (note CUỐI dòng — I11)
    ],
    "ingest_ops": [
        '_dieu_sequence_stats', '_drive_info_file', '_file_parents', '_looks_like_drive_id', '_normalize_hieuluc', '_profile_loai_evidence', '_resolve_drive_id_source', '_valid_cats', '_vb_ingest_auto_plan', '_is_dang_title_zone',   # I11 (+_resolve_drive_id_source v1.34.37; +_profile_loai_evidence v1.34.40; +_is_dang_title_zone v1.34.41)
        '_dup_dieu_scan', '_dup_dieu_note',   # v1.34.54 A7a (note CUỐI dòng — I11)
        '_dieu_head_marks',   # r229 v1.35.65 tiêu đề Điều dùng chung đếm+cắt (note CUỐI dòng — I11)
        '_snapshot_age_seconds', '_snapshot_stale_warn',   # r251 v1.35.88 cờ snapshot nguội cho ingest-missing (hằng `_SNAPSHOT_STALE_S` re-export TRỰC TIẾP, không vào đây — bẫy I11/r81) (note CUỐI dòng — I11)
        '_probe_pdf_quality',   # v1.34.58 C-#9 (note CUỐI dòng — I11)
        '_ingest_perf_hint',   # v1.34.73 perf nạp-lô (note CUỐI dòng — I11)
        '_ingest_local_ocr_gate',   # r180 S1 cổng OCR đường nền (note CUỐI dòng — I11)
        '_profile_dry_gate_soften',   # r180 S4 DRY .doc cũ VERIFY_AT_APPLY (note CUỐI dòng — I11)
        '_gas_version_at_least', '_ingest_commit_supported', '_ingest_commit_call', '_ingest_commit_readback',   # r198 ADR-0014 ingest_commit (note CUỐI dòng — I11)
        '_ingest_commit_verdict',   # r291 (ING-03) cổng marker cho CẢ HAI call site — bẫy I11: symbol mới PHẢI re-export (hằng `_INGEST_COMMIT_MARKERS` re-export TRỰC TIẾP bên dưới, không vào đây)
        '_gas_ver_note',   # r207 p11 món 3: nhặt version từ bootstrap ⇒ bỏ ping riêng (note CUỐI dòng — I11)
        '_pi_stage_plan', '_pi_stage_confirm', '_pi_stage_prepare', '_pi_stage_write', '_pi_stage_readback', '_pi_stage_commit',   # R-a WP7 r203 bảng stage profile-ingest (note CUỐI dòng — I11: hàm rebase tra tên qua globals tl)
        '_il_stage_plan', '_il_stage_confirm', '_il_stage_prepare', '_il_stage_write', '_il_stage_readback', '_il_stage_commit',   # R-b WP7 r204 bảng stage ingest-local (note CUỐI dòng — I11)
        '_pr_stage_plan', '_pr_stage_confirm', '_pr_stage_prepare', '_pr_stage_write', '_pr_stage_commit',   # R-c WP7 r205 bảng 5 stage resume — không readback riêng (note CUỐI dòng — I11)
        '_ingest_dedup_sohieu_live',   # F1 r191 dedup sohieu LIVE lỏng-năm (note CUỐI dòng — I11)
        '_pdf_image_verdict', '_pdf_text_layer_stats',   # F4 r191 cổng PDF-ảnh (note CUỐI dòng — I11)
        '_ingest_claim_get', '_claim_ttl_hint',   # F6+F8 r192 claim một-cửa + hint TTL (note CUỐI dòng — I11)
        '_profile_push_chunks', 'cmd_profile_ingest_resume',   # v1.34.55 C4+C5 (note CUỐI dòng — I11)
        'cmd_verify_staged',   # r200 staged lane grill 24-07 (note CUỐI dòng — I11)
        '_resume_identity_gate', '_journal_head',   # r184 ADR-0011/D5 siết resume (note CUỐI dòng — I11)
        '_chunk_summaries', '_classify_doc_header', '_ingest_ckpt_load', '_ingest_ckpt_load_full', '_ingest_dedup_title_key', '_ingest_local_cat_gate',
        '_ingest_local_prev_state', '_ingest_missing_dedup_live', '_ingest_missing_partition', '_ingest_missing_select', '_ingest_target', '_ingest_verify_gate',
        '_profile_ingest_note', '_profile_read_probe_text', '_profile_source_quality', '_safe_profile_doc_name',
        '_draft_banner_line', '_sohieu_line_khuyet', '_issue_dateline_complete',   # r179 T4 (bậc bằng chứng draft)
        '_sohieu_from_title_zone', '_split_by_dieu_chunks', '_upload_mime_ext',
        '_verify_convert_readback', 'cmd_ingest', 'cmd_ingest_analyze', 'cmd_ingest_inbox', 'cmd_ingest_local', 'cmd_ingest_missing', 'cmd_ingest_route',
        'cmd_profile_ingest',
    ],
    "source_ops": [
        '_reg_row_present', '_register_bulk_missing', '_register_clear', '_register_target_exists', '_shared_source_fix_plan', '_shared_source_id_groups', '_source_delete_plan', '_source_rename_plan', '_source_update_corpus_plan', 'cmd_recat', 'cmd_register', 'cmd_shared_source_fix', 'cmd_source_delete', 'cmd_source_rename', 'cmd_source_update_corpus',   # ĐỢT A v1.34.64 — 15 tên CHUYỂN NGUYÊN VĂN từ ingest_ops (kế hoạch §4; hằng _REG_CLEAR_* re-export trực tiếp, KHÔNG vào đây — bẫy I11)
        '_sua_doi_self_ref',   # r179 T3 (guard sua_doi tự trỏ — chặn cứng rc=2, không --force)
        '_source_update_corpus_bulk',   # r197 bulk corpus-flip (note CUỐI dòng — I11)
        '_reg_row_get', '_register_autofill', '_register_infer_name_cat', '_register_cat_folder_ids',   # r208b báo cáo 25-07 mục 2.1: register tự điền/cảnh báo name+cat (note CUỐI dòng — I11)
    ],
    "live": [
        '_cmd_version_probe', '_deploy_plan', '_rollback_plan',   # I11
        '_live_readiness_report', '_live_smoke_plan', 'cmd_deploy_plan', 'cmd_final_acceptance', 'cmd_go_live_runbook', 'cmd_live_contract_check',
        'cmd_live_readiness', 'cmd_live_smoke_plan', 'cmd_live_state_diff', 'cmd_live_state_snapshot', 'cmd_rollback_plan',
    ],
    "lookup_ops": [
        '_base_also_enabled', '_cluster_for_base', '_cluster_lookup', '_date_from_effect_match', '_emit_raw_no_gdoc', '_flag_value', '_legal_refs', '_multi_diem', '_nlm_display', '_norm_compare_text', '_omnibus_cross_domain_note', '_raw_no_gdoc', '_read_doc_text', '_read_verify_text', '_resolve_base_gdoc', '_resolve_cluster_member',   # I11
        '_amendments_covered_by_vbhn_date', '_find_amendment_candidates', '_focus_block', '_footnote_rel_kind', '_header_verify_infer_cats', '_is_amendment_like',
        '_is_high_amendment_subject', '_parse_footnote_def', '_qt5_queries', '_rasoat_autocache_worksheet', '_rasoat_dedup_push', '_rasoat_expand_text',
        '_rasoat_fallback_plan', '_rasoat_map_positional', '_relation_backfill_items', '_relation_candidate_flags', '_relation_refs', '_source_map_flags',
        '_source_map_verdict', '_status_amendment_registry_guard', '_summ_entry_source_map', '_vbhn_bare_key', '_dang_bare_key', '_vbhn_check_verdict', '_vbhn_compare',   # +_dang_bare_key v1.34.41
        '_text_looks_binary', '_doc_text_fetch_binary', '_docx_unzip_text', '_doc_text_any', 'cmd_doc_text', '_gdoc_docx_text',
        '_markup_warn', '_markup_cert_path', '_markup_cert_write', '_markup_cert_read',   # v1.34.60 A1 doc-text; +_gdoc_docx_text r183; +4 helper markup r186 dùng chung với cmd_extract (note CUỐI dòng — I11)
        '_vbhn_verify_flags', 'cmd_cluster', 'cmd_dedup_check', 'cmd_footnote_map', 'cmd_header_verify', 'cmd_locate',
        'cmd_rasoat', 'cmd_rasoat_chongcheo', 'cmd_rasoat_loop', 'cmd_relation_backfill', 'cmd_relation_check', 'cmd_corpus_relation_sweep', '_vbhn_goc_map', 'cmd_source_map',
        'cmd_status', 'cmd_vbhn_check', 'cmd_vbhn_compare', 'cmd_vbhn_verify', 'cmd_xref',
        '_rasoat_state_scope', '_rasoat_sohieu_key', '_rasoat_unit_shape', '_rasoat_unit_to_bang', '_rasoat_merge_units',
        '_rasoat_state_reconcile', '_rasoat_meta_folder', '_rasoat_state_find',
        'cmd_state_get', 'cmd_state_put', 'cmd_rasoat_merge',   # r213 v1.35.49 ĐỢT 5 (note CUỐI dòng — I11)
        '_text_thieu_khoi_dau',   # r215 cổng «text vào thẳng thân» (note CUỐI dòng — I11)
        '_rasoat_la_ban_sao', '_rasoat_trung_lap', '_rasoat_check_lech',   # r216 (note CUỐI dòng — I11)
        '_rasoat_vong_doi_enums',
        '_rasoat_vong_doi_findings', '_rasoat_vong_doi_dong_hop_le',   # r300 vòng đời hồ sơ (note CUỐI dòng — I11)
        '_rasoat_anchor_khuon', '_rasoat_anchor_findings', '_rasoat_anchor_hop_le',   # r313 RAS-17 khuôn anchor (note CUỐI dòng — I11)
        '_rasoat_anchor_quet',   # r321 RAS-17 vế rasoat-merge (note CUỐI dòng — I11)
        '_docpatch_norm', '_docpatch_vung_doc', '_docpatch_vung_ghi', '_docpatch_ap',
        '_docpatch_tim_file', '_docpatch_sha', '_docpatch_cache_dir', 'cmd_doc_patch',   # r217 sửa-theo-điểm (note CUỐI dòng — I11)
        '_rasoat_corpus_hieu_luc',   # r295 RAS-13 predicate corpus-hiệu-lực dùng chung (note CUỐI dòng — I11)
        '_rasoat_state_validate', '_rasoat_state_newest',   # r295 RAS-09/RAS-03 (note CUỐI dòng — I11)
    ],
    "nlm_ops": [
        '_slice_dieu', '_split_source_ids', '_strip_font_runs', '_vbqppl_notebooks',   # I11
        '_classify_nlm_sources', '_discover_overflow_from_registry', '_resolve_overflow_shards', '_nlm_dedup_gate', '_nlm_query_plan',
        '_nlm_ref_slot_count',   # v1.34.40 B.1 ; v1.34.47: +_resolve_overflow_shards (đối xứng discovery read↔write)
        '_reconcile_sweep_note', '_reconcile_sweep_problems', '_reconcile_sweep_clean',   # v1.34.42/50 BUG1 (note điều kiện + clean máy --all-notebooks)
        '_resolve_shard_topology', '_topology_hash', '_topology_stamp', '_topology_row_kind_findings', '_live_source_count', '_nlm_add_capacity_error', '_shard_capacity_default',   # v1.34.49 r110 topology D5/F-05/F-06/F-07/F-09 (I11: note CUỐI dòng)
        '_foreign_profile_notebooks',   # v1.34.51 r112 (doctor không nhận nhầm notebook profile-khác thành vbqppl overflow-shard)
        '_nlm_auth_age_minutes', '_nlm_preflight_report', '_nlm_links_rows', '_entry_links_url', 'cmd_nlm_links', 'cmd_nlm_auth_status',   # v1.34.54 A1+C8+B1 (note CUỐI dòng — I11)
        '_nlm_links_md',   # F5 van 1 r192 bảng tay markdown (note CUỐI dòng — I11)
        '_nlm_source_remove_plan', '_source_remove_delete_verdict',   # v1.34.56 A-#12 (note CUỐI dòng — I11; cmd sang nlm_admin_ops v1.34.65, plan-helper Ở LẠI theo danh-sách-tên §5/R2)
        '_nlm_remove_presence_verdict',   # r279 chốt đo LIVE trước khi gỡ (note CUỐI dòng — I11)
        '_nlm_fallback_enabled', '_nlm_hard_dead', '_nlm_verdict', '_nlm_or_corpus', '_nlm_fallback_banner',   # v1.34.60 E resolver+control (note CUỐI dòng — I11)
        '_nlm_not_found', '_nlm_verdict_sleep',   # r196 TRINH 3.9: phân loại NOT_FOUND + hook backoff (note CUỐI dòng — I11)
        '_corpus_question_resolve', '_nlm_query_corpus_fallback',   # v1.34.60 E1 (note CUỐI dòng — I11)
        '_backfill_nlm_status_candidates', 'cmd_backfill_nlm_status', '_nlm_due_rows',   # r179 T2+T8 (ADR-0010: nắn từ vựng + diện phải-có due↔claim)
        '_nlm_slot_count', '_overflow_route', '_overflow_status', '_preflight_invariants', '_preflight_verdict',
        '_raw_on_nlm_rows', '_slot_count_all_shards', '_sohieu_loose', 'cmd_nlm_content', 'cmd_nlm_cross',
        '_slot_live_counts',   # r208 báo cáo 25-07 mục 2.2: --all-shards đối chiếu LIVE (note CUỐI dòng — I11)
        'nlm_auth_fix_hint',   # r208b báo cáo 25-07 mục 3.2: chuỗi khắc phục auth đúng đường, một nguồn sự thật (note CUỐI dòng — I11)
        '_nlm_rotation_token_state',   # r208c báo cáo 25-07 mục 3.1: hạn THẬT của token xoay phiên thay cho est_remaining_min bịa (note CUỐI dòng — I11)
        '_nlm_scope_shortfall',   # r214: đối chiếu sources_used ↔ --source-id, chặn kết luận âm tính giả (note CUỐI dòng — I11)
        '_nlm_draft_sources',   # r215: nguồn DỰ THẢO trong phạm vi sắp hỏi — cảnh báo, KHÔNG chặn (note CUỐI dòng — I11)
        'cmd_nlm_get', 'cmd_nlm_list', 'cmd_nlm_orphans', 'cmd_nlm_query', 'cmd_nlm_query_plan',
        'cmd_preflight', 'cmd_slot_audit',
    ],
    "nlm_admin_ops": [
        '_migrate_plan', '_migrate_resume_write', '_nlm_add_deferred', '_nlm_add_doc_type', '_nlm_list_stale_read', '_nlm_post_add_dup_check', '_nlm_reconcile_plan', '_nlm_source_drive_id', '_nlm_source_list_cached', '_physical_audit_classify', '_shard_row_kind', 'cmd_nlm_add', 'cmd_nlm_audit_physical', 'cmd_nlm_migrate', 'cmd_nlm_reconcile', 'cmd_nlm_source_remove', 'cmd_overflow_resolve', 'cmd_push_overflow',   # ĐỢT B v1.34.65 — 18 tên GHI/audit CHUYỂN NGUYÊN VĂN từ nlm_ops (kế hoạch §5, ranh giới GHI/ĐỌC; hằng Ở LẠI nlm_ops — bẫy I11)
        '_nlm_link_row_kind',   # r180 S8 row_kind tường minh ở reg_link (note CUỐI dòng — I11)
        '_nlm_no_wait_reg_link',   # F3 r191 no-wait reg_link deferred (note CUỐI dòng — I11)
        '_reconcile_channel_suspect', '_reconcile_suspect_kind',   # FIX-C r201 guard nghi-kênh liệt kê + r206 phân định registry-mỏng (note CUỐI dòng — I11)
        '_reconcile_plan_path', '_reconcile_plan_artifact', '_reconcile_write_artifact',   # r208b báo cáo 25-07 mục 2.4: LUÔN in/ghi plan DRY, kể cả khi guard chặn --apply (note CUỐI dòng — I11)
    ],
    "ocr": [
        '_bridge_confirm_apply', '_bridge_run_child_apply', '_sha256_bytes_file_local',   # I11; _bridge_run_child_apply v1.34.53 C1
        '_load_ocr_manifest_for_text', '_ocr_manifest_path_for_text', '_ocr_out_paths', 'cmd_ingest_ocr', 'cmd_ocr_analyze', 'cmd_ocr_run',
        'cmd_ocr_verify', 'cmd_profile_ingest_ocr',
    ],
    "ops_misc": [
        '_alias_terms', '_canonical_for_query', '_compiles', '_corpus_safe_reversible', '_doctor_exporttext_probe_target', '_nlm_probe_summary', '_official_rank', '_reassemble_parts',   # I11
        '_content_md5', '_doctor_exporttext_probe', '_drift_hint_lines', '_ensure_gws_nlm', '_entries_with_live_fields', '_instruction_audit_text', '_integrity_scan',
        '_journal_close_plan', '_journal_read', '_journal_reapply_one', '_journal_resume_ops', '_journal_undo_ops', '_loop_controller',
        '_merge_base_entries', '_pin_registry_doc_id_config', '_reg_query_row', '_registry_claim_by_notebook', '_registry_claim_target', '_resolve_confirm_targets',
        '_resolve_registry_doc_id', '_skill_package_integrity', '_vbhn_normalize_recommendations', 'cmd_backfill_notebook', 'cmd_bench', 'cmd_boot',
        'cmd_cat_list', 'cmd_cat_verify', 'cmd_config_pin_registry', 'cmd_confirm', 'cmd_convert_verify', 'cmd_counts',
        'cmd_cowork_plan', 'cmd_doctor', 'cmd_edit_skill', 'cmd_exists', 'cmd_init_config', 'cmd_instruction_audit',
        'cmd_instructions', 'cmd_journal', 'cmd_loop', 'cmd_manifest', 'cmd_perf', 'cmd_ping',
        'cmd_precheck', 'cmd_profile_file_remove', 'cmd_reg_delete', 'cmd_reg_query', 'cmd_registry_map', 'cmd_resume',
        'cmd_source_verify', 'cmd_undo', 'cmd_up', 'cmd_vbhn_normalize', 'cmd_verify_integrity', 'gas_parallel',
        'public_download_text', 'save_local_config',
        '_merge_local_config', '_heal_legacy_registry_doc_id',   # r280 (P16-F01) — bẫy I11: symbol mới PHẢI re-export
        '_pfr_count', '_pfr_reg_delete_verdict',   # r289 (PRO-01) readback client cho reg_delete — bẫy I11: symbol mới PHẢI re-export
        '_doc_dep_probe',   # r319 — bẫy I11 LẶP LẠI: `bind()` re-home __globals__, helper mới không khai ở đây = NameError LÚC CHẠY
    ],
    "profile_env": [
        '_active_profile', '_apply_profile_env', '_apply_unconfigured_profile_env', '_config_backup_dir', '_goc_cay_skill', '_trong_cay_skill', '_config_candidates', '_doctor_check_profile', '_download_link_plan', '_download_link_rank',   # r202: +_config_backup_dir (bẫy I11 — symbol mới PHẢI re-export)
        '_emit_profile_policy_error', '_gas', '_gas_get_retry', '_gws_nlm_note', '_hopnap_upload_md', '_mutable_config_target',
        '_path_exists_safe', '_persist_profile_config', '_persist_profiles_config_bulk', '_profile_asset_ids', '_profile_asset_owners', '_profile_cache_component', '_profile_cache_dir', '_profile_config_rows', '_profile_deletable_sources',
        '_profile_file_slug', '_profile_live_source_ids', '_profile_lookup', '_profile_policy_error', '_profiles_from_config', '_read_config_record',
        '_read_json_file', '_ref_tokens', '_remove_profile_config', '_rename_profile_config', '_resolve_nlm_notebook', '_set_default_profile_config',
        '_strip_goc_token', '_token_set', '_write_json_atomic', 'apply_profile_offline', 'cmd_profile_file_add', 'load_creds',
    ],
    "profile_mgmt": [
        '_adopt_pick_assets', '_discover_scan_vbthuong', '_index_old_candidates', '_strip_shared_fixes',   # I11
        '_catalog_to_scan', '_marker_from_catalog',   # r185/WP5 bulk (note CUỐI dòng — I11)
        '_cmd_profile_adopt_impl', '_cmd_profile_doctor_impl', '_cmd_profile_index_impl', '_create_profile_manifest_json', '_profile_index_csv', '_profile_index_rows',
        '_profile_info_from_config', '_profile_list_discover', '_profile_manifest_entries_for', '_profile_rebuild_partition', 'cmd_profile_adopt', 'cmd_profile_create',
        'cmd_profile_delete', 'cmd_profile_doctor', 'cmd_profile_files', 'cmd_profile_index', 'cmd_profile_info', 'cmd_profile_list',
        'cmd_profile_manifest', 'cmd_profile_rebuild_registry', 'cmd_profile_rename', 'cmd_profile_use',
        # P1 marker (v1.34.22, ADR-0003)
        '_marker_body', '_marker_validate', '_marker_diff', '_marker_find_in_items', '_marker_read', '_marker_write',
        '_marker_fingerprint', '_marker_required_keys', '_marker_mutation_guard',   # r184 (ADR-0012)
        '_migration_plan_finalize',   # r186 (ADR-0012 R2) — bẫy I11: symbol mới PHẢI re-export
        '_config_candidates_report', '_profile_sync_rows', '_cmd_profile_sync_impl', '_cmd_profile_backfill_markers_impl',
        'cmd_profile_sync', 'cmd_profile_backfill_markers',
        '_profile_block_meta', '_cmd_profile_load_impl', 'cmd_profile_load',   # P2 (v1.34.24)
        '_promote_seed_candidates', '_nlm_system_prompt_apply', '_cmd_profile_promote_impl', 'cmd_profile_promote',   # P3 (v1.34.25)
        'cmd_profile_set_meta', '_cmd_profile_set_meta_impl',   # v1.34.29
        '_template_id_norm', '_templates_apply_change', '_template_findings', '_template_probe', '_base_meta_folder_id',   # v1.34.71 templates (Q1/Q3/Q5/Q6)
        '_nlm_only_sentinel', '_from_nlm_row_payload', '_cmd_profile_from_nlm_impl', 'cmd_profile_from_nlm',   # P4 (v1.34.26)
        '_profile_from_nlm_add_missing',   # v1.34.30 #2 (from-nlm --add-missing)
        '_cmd_profile_materialize_sources_impl', 'cmd_profile_materialize_sources',
    ],
    "regio": [
        '_apply_gate', '_apply_journal_start', '_apply_precheck', '_atomic_write_text', '_b64_text', '_base_manifest_entries',
        '_cache_file', '_chunk_covered_sohieu', '_create_profile_registry_sheet',   # +_chunk_covered_sohieu r253 (phủ-bằng-chunk)
        '_deep_entry_rank', '_entry_cat', '_entry_confirmed', '_entry_corpus_true',
        '_entry_date_text', '_entry_drive_id', '_entry_goc', '_entry_google_doc', '_entry_hieuluc_date', '_entry_is_draft',
        '_entry_is_own_thuong', '_entry_issue_date_iso', '_entry_issue_year', '_entry_md5', '_entry_mime', '_entry_nlm',
        '_entry_nlm_notebook_id', '_entry_on_nlm_live', '_entry_quarantined', '_entry_query_match', '_entry_query_match_safe_for_hygiene', '_entry_raw_no_gdoc',
        '_entry_row_kind', '_entry_score', '_entry_sohieu', '_entry_sua_doi', '_entry_years', '_invalidate_manifest_cache',
        '_manifest_dirty_marker',   # F2 r191 marker manifest bẩn sau lệnh ghi (note CUỐI dòng — I11)
        '_journal_append', '_journal_dir', '_journal_new_run_id', '_journal_path', '_journal_resume_state', '_journaled_reg_clear',
        '_expect_precondition_verdict',   # r279 chốt CAS trước khi ghi registry (note CUỐI dòng — I11)
        '_journaled_reg_upsert', '_journaled_reg_write', '_load_linhvuc', '_load_manifest_full', '_load_phapdien', '_manifest_cache_age_seconds',
        '_verified_reg_write_unlocked', '_journaled_reg_write_unlocked', '_verified_reg_upsert_unlocked',   # r185/WP6 lane (I11)
        '_manifest_entries', '_manifest_placeholder', '_mime_from_info', '_notebook_from_manifest_json', '_rebuild_manifest_index', '_reg_before_from_manifest',
        '_reg_cols_valid', '_sohieu_key_entry', '_summ_entry', '_verified_reg_upsert', '_verified_reg_write', '_verify_reg_result',
        '_verify_registry_sheet', '_year_from_text_safe', 'norm_sohieu',
    ],
    "release": [
        '_sha256_file', '_write_text_atomic',   # I11
        '_release_secret_findings',   # r193 cổng quét token trong bundle (note CUỐI dòng — I11)
        '_build_release_manifest', '_release_should_include', '_skill_links_findings', '_verify_release_manifest', 'cmd_bundle_export', 'cmd_determinism_audit', 'cmd_release_bundle',
        'cmd_release_check', 'cmd_release_manifest', 'cmd_release_verify', 'cmd_test_fragments_check',
    ],
    "resolve": [
        '_dedupe_key_entry', '_doctype_family', '_is_source_sidecar', '_sohieu_num_typo', 'resolve_body_effective_dates',   # I11
        '_aggregate_verdict', '_classify_ref', '_dedup_status', '_discovery_links', '_dup_of_live_sibling', '_field_text',
        '_flags_reason', '_goc_keys', '_is_vbhn_entry', '_name_inject_vbhn_year', '_qt5_search_hints', '_query_doctype_tier',
        '_relation_audit', '_resolve_deep_target', '_rq_relation_probe', '_scan_inline_amendments', '_sohieu_base_sort_year', '_sohieu_query_hits_entry',
        '_sohieu_typo_near', '_source_map_one', '_split_distinct_vbhn_docs', '_vb_tier_rank', '_vbhn_agency_from_key', '_vbhn_agency_mismatch',
        '_vbhn_base_key', '_vbhn_candidates', '_vbhn_for_goc', '_vbhn_goc_corroborated', '_vbhn_latest_low_priority_recent_law', '_vbhn_metadata_flags',
        '_vbhn_official_flags', '_vbhn_quality_flags', '_vbhn_scan', '_vbhn_sohieu_inject_year', '_vbhn_subject_key', '_vbhn_verdict',
        '_warning_codes', 'resolve_footnote_amendments', 'resolve_identity',
    ],
    "workflow": [
        '_available_commands_from_parser', '_first_text_diff', '_idempotency_contract_for_workflow', '_script_docstrings', '_unique_preserve_order',   # I11
        '_golden_test', '_load_workflow_card', '_workflow_cards_audit', 'cmd_golden_test', 'cmd_route_task', 'cmd_tool_inventory',
        'cmd_workflow_audit', 'cmd_registry_coverage',
        # r218 doc-claims-check (chỉ FUNCTION vào stub — hằng `_DOC_CLAIMS_*` là module-level, GOTCHAS §2)
        '_doc_claims_check', '_doc_claims_context', '_doc_claims_lineno', '_doc_claims_linestarts',
        '_doc_claims_mask', '_doc_claims_noisy', '_doc_claims_rel', '_doc_claims_scan_one',
        '_doc_claims_targets', 'cmd_doc_claims_check',
        '_py_size_findings',   # ĐỢT A v1.34.64 — guard trần mount §3 (note CUỐI dòng — I11)
        '_kernel_size_findings',   # G1a v1.34.66 — WARN kernel 47KB (note CUỐI dòng — I11)
    ],
    "zip_ingest": [
        '_safe_extract_zip_for_ingest', '_zip_is_safe_member', '_zip_normalized_member_path', '_zip_plan', '_zip_sorted_infos', 'cmd_ingest_zip',
        'cmd_profile_ingest_zip',
    ],
}


def _make_tl_stub(_mod, _name, _mod_key):
    def _stub(*_a, **_kw):
        return getattr(_mod, _name)(*_a, **_kw)
    _stub.__name__ = _name
    _stub.__qualname__ = _name
    _stub.__doc__ = f"stub ủy quyền → tl_core.{_mod_key}.{_name} (I10 data-driven)"
    _stub.__tl_stub__ = (_mod_key, _name)
    return _stub


for _sm_key, _sm_names in _STUB_MAP.items():
    _sm_mod = globals()["_tl_" + _sm_key]
    for _sm_n in _sm_names:
        globals()[_sm_n] = _make_tl_stub(_sm_mod, _sm_n, _sm_key)
del _sm_key, _sm_names, _sm_mod, _sm_n


# I11-fix: _json_dumps là WRAPPER LÕI jsonio đọc mutable-global _DETERMINISTIC_ON — PHẢI sống ở tl
# (r61 cấm token này trong tl_core; máy sweep affinity từng chuyển nhầm sang ocr.py).
def _json_dumps(obj, *, deterministic: bool | None = None) -> str:
    return _tl_det.json_dumps(
        obj,
        deterministic=(_deterministic_enabled() if deterministic is None else bool(deterministic)),
        default_on=_DETERMINISTIC_ON,
        project_root=HERE.parent,
    )


# v1.34.20 (#5): hằng cột clear của register (hàm rebase đọc globals tl)
_REG_CLEAR_FREE_COLS = _tl_source_ops._REG_CLEAR_FREE_COLS   # ĐỢT A v1.34.64 — hằng theo cụm source-CRUD (bẫy I11: re-export trực tiếp)
_REG_CLEAR_PROTECTED = _tl_source_ops._REG_CLEAR_PROTECTED   # ĐỢT A v1.34.64 — như trên
_REGISTER_EXPECT_COLS = _tl_source_ops._REGISTER_EXPECT_COLS   # r279 — hằng cột cho chốt CAS `--expect`; hằng ⇒ re-export trực tiếp (bẫy I11: _STUB_MAP đòi callable)
_SNAPSHOT_STALE_S = _tl_ingest_ops._SNAPSHOT_STALE_S   # r251 — ngưỡng snapshot nguội; hằng ⇒ re-export trực tiếp (vào _STUB_MAP là vỡ r81: stub phải callable)
_INGEST_COMMIT_MARKERS = _tl_ingest_ops._INGEST_COMMIT_MARKERS   # r291 (ING-03) — HẰNG (tuple) ⇒ re-export trực tiếp, không vào _STUB_MAP
# r288 (Pha 1-0, Helper 1 — kết luận giao dịch): re-export TRỰC TIẾP, KHÔNG qua _STUB_MAP. Lý do khác với
# hằng ở trên: `Txn` là LỚP và `TxnBlocked` là LỚP NGOẠI LỆ — bọc stub thì `except TxnBlocked` bắt hụt và
# `isinstance` sai (stub là function, không phải class). `step_result_ok` đi cùng cho đủ bộ một chỗ.
Txn = _tl_txn.Txn
TxnBlocked = _tl_txn.TxnBlocked
step_result_ok = _tl_txn.step_result_ok
# v1.34.22 (P1, ADR-0003): hằng marker profile (hàm rebase — kể cả classify._discover_classify — đọc globals tl)
_PROFILE_MARKER_NAME = _tl_profile_mgmt._PROFILE_MARKER_NAME
_PROFILE_MARKER_SCHEMA = _tl_profile_mgmt._PROFILE_MARKER_SCHEMA
_PROFILE_MARKER_SCHEMA_V2 = _tl_profile_mgmt._PROFILE_MARKER_SCHEMA_V2   # r184 (ADR-0012) — bẫy I11: hằng mới PHẢI re-export
_MARKER_SCHEMAS_READABLE = _tl_profile_mgmt._MARKER_SCHEMAS_READABLE     # r184 — như trên
_MARKER_IDENTITY_KEYS = _tl_profile_mgmt._MARKER_IDENTITY_KEYS
_PROFILE_SYSPROMPT_NAME = _tl_profile_mgmt._PROFILE_SYSPROMPT_NAME   # P3 (v1.34.25)
_SEED_RAW_EXT_RE = _tl_profile_mgmt._SEED_RAW_EXT_RE                 # P3 — bẫy I11: hằng mới PHẢI re-export
_NLM_ONLY_SENTINEL_PREFIX = _tl_profile_mgmt._NLM_ONLY_SENTINEL_PREFIX   # P4
_REG_BULK_READBACK_MAX = _tl_regio._REG_BULK_READBACK_MAX   # v1.34.34 — bẫy I11: HẰNG re-export trực tiếp, KHÔNG vào _STUB_MAP (stub = function → so sánh int nổ)
_REG_LANE = _tl_regio._REG_LANE   # r185/WP6 (ING-05) — RLock re-export trực tiếp (bẫy I11; hàm rebase đọc globals tl)
_ROW_KIND_PROTECTED = _tl_nlm_ops._ROW_KIND_PROTECTED   # v1.34.49 F-06 — bẫy I11: HẰNG re-export trực tiếp (ref/thuong không bao giờ suy từ topology)
NLM_BATCH_LINKS_THRESHOLD = _tl_nlm_ops.NLM_BATCH_LINKS_THRESHOLD   # v1.34.54 B1 — HẰNG re-export trực tiếp (bẫy I11)
NLM_COOKIE_BATCH_WARN_MIN = _tl_nlm_ops.NLM_COOKIE_BATCH_WARN_MIN   # F7 r192→r208d: chặn-theo-tuổi ⇒ CANARY LIVE, tuổi chỉ còn CẢNH BÁO — HẰNG re-export trực tiếp (bẫy I11)
_NLM_SIZE_VAN_CHARS = _tl_ingest_ops._NLM_SIZE_VAN_CHARS            # F5 van 2 r192 — HẰNG re-export trực tiếp (bẫy I11)
_DUP_DIEU_HEAD_RE = _tl_ingest_ops._DUP_DIEU_HEAD_RE               # v1.34.54 A7a — HẰNG re-export trực tiếp
_SECOND_LETTERHEAD_RE = _tl_ingest_ops._SECOND_LETTERHEAD_RE       # v1.34.54 A7a — HẰNG re-export trực tiếp
_INBOX_INFRA_NAME_RE = _tl_ingest_ops._INBOX_INFRA_NAME_RE         # v1.34.54 B2 — HẰNG re-export trực tiếp
_PDF_BROKEN_FONT_WARN = _tl_ingest_ops._PDF_BROKEN_FONT_WARN       # v1.34.58 C-#9 — HẰNG re-export trực tiếp (bẫy I11)
_PDF_PROBE_TOOL_WARN = _tl_ingest_ops._PDF_PROBE_TOOL_WARN         # r251 — HẰNG re-export trực tiếp (bẫy I11)
_PDF_IMAGE_CHARS_PER_PAGE = _tl_ingest_ops._PDF_IMAGE_CHARS_PER_PAGE   # F4 r191 — HẰNG re-export trực tiếp (bẫy I11)
_RESUME_PART_RE = _tl_ingest_ops._RESUME_PART_RE                   # v1.34.55 C4 — HẰNG re-export trực tiếp
STAGED_NOTE_PREFIX = _tl_ingest_ops.STAGED_NOTE_PREFIX             # r200 staged lane — HẰNG re-export trực tiếp (bẫy I11)
_NLM_COOKIE_LIFE_MIN = _tl_nlm_ops._NLM_COOKIE_LIFE_MIN             # v1.34.54 A1 — HẰNG re-export trực tiếp
_NLM_COOKIE_WARN_AGE_MIN = _tl_nlm_ops._NLM_COOKIE_WARN_AGE_MIN     # v1.34.54 A1 — HẰNG re-export trực tiếp
_NLM_NOT_FOUND_RETRY_DELAYS = _tl_nlm_ops._NLM_NOT_FOUND_RETRY_DELAYS   # r196 TRINH 3.9 — HẰNG re-export trực tiếp (bẫy I11)
_DEDUP_JUNK_NAME_RE = _tl_hygiene._DEDUP_JUNK_NAME_RE               # v1.34.63 B1 — HẰNG re-export trực tiếp (bẫy I11)
_GDOC_DOCX_MIME = _tl_lookup_ops._GDOC_DOCX_MIME                    # r183 — HẰNG re-export trực tiếp (bẫy I11)
_GDOC_MARKUP_WARN = _tl_lookup_ops._GDOC_MARKUP_WARN                # r183 — HẰNG re-export trực tiếp (bẫy I11)
_RECONCILE_SUSPECT_MIN_LIVE = _tl_nlm_admin_ops._RECONCILE_SUSPECT_MIN_LIVE       # FIX-C r201 — HẰNG re-export trực tiếp (bẫy I11)
_RECONCILE_SUSPECT_UNREG_RATIO = _tl_nlm_admin_ops._RECONCILE_SUSPECT_UNREG_RATIO # FIX-C r201 — như trên
_RECONCILE_REGISTRY_THIN_RATIO = _tl_nlm_admin_ops._RECONCILE_REGISTRY_THIN_RATIO  # r206 — HẰNG mới PHẢI re-export (bẫy I11)
_AUTH_FIX_FALLBACK = _tl_nlm_ops._AUTH_FIX_FALLBACK                 # r208b 3.2 — HẰNG re-export trực tiếp (bẫy I11; nlm_auth_fix_hint đọc qua globals tl)
_REGISTER_AUTOFILL_COLS = _tl_source_ops._REGISTER_AUTOFILL_COLS    # r208b 2.1 — như trên
_REGISTER_NAME_EXT_RE = _tl_source_ops._REGISTER_NAME_EXT_RE        # r208b 2.1 — như trên
_RECONCILE_PLAN_BLOCKED_SUFFIX = _tl_nlm_admin_ops._RECONCILE_PLAN_BLOCKED_SUFFIX  # r208b 2.4 — như trên
_NLM_ROTATION_COOKIE_NAMES = _tl_nlm_ops._NLM_ROTATION_COOKIE_NAMES  # r208c 3.1 — HẰNG re-export trực tiếp (bẫy I11)
_RASOAT_STATE_ALLOWED = _tl_lookup_ops._RASOAT_STATE_ALLOWED         # r213 ĐỢT 5 — HẰNG re-export trực tiếp (bẫy I11)
_RASOAT_BANG_SCHEMA = _tl_lookup_ops._RASOAT_BANG_SCHEMA             # r213 ĐỢT 5 — như trên
_RASOAT_VB_META_FIELDS = _tl_lookup_ops._RASOAT_VB_META_FIELDS       # r213 ĐỢT 5 — như trên

# ── I11: re-export bảng hằng đã chuyển (hàm rebase đọc globals tl → giữ tên tại đây) ──
INSTRUCTION_REQUIRED = _tl_ops_misc.INSTRUCTION_REQUIRED
_ABBREV_MAP = _tl_classify._ABBREV_MAP
_CAT_KEYWORDS = _tl_classify._CAT_KEYWORDS
_FLAG_REASONS = _tl_resolve._FLAG_REASONS
_LOAI_CANON = _tl_classify._LOAI_CANON
_ABBREV_RE = _tl_classify._ABBREV_RE
_LOAI_CANON_VALUES = _tl_classify._LOAI_CANON_VALUES

_IDEMPOTENCY_CONTRACTS = _tl_workflow._IDEMPOTENCY_CONTRACTS
_TASK_TO_WORKFLOW = _tl_workflow._TASK_TO_WORKFLOW
BackupTrongCaySkill = _tl_profile_env.BackupTrongCaySkill   # v1.36.69 (#972) — LỚP, không stub được (bẫy I11)

for _m in (_tl_workflow, _tl_release, _tl_live, _tl_zip_ingest, _tl_ocr, _tl_chunking, _tl_hygiene, _tl_nlm_ops, _tl_extract_cache, _tl_fetch_web, _tl_profile_mgmt, _tl_ingest_ops, _tl_lookup_ops, _tl_ops_misc, _tl_classify, _tl_profile_env, _tl_resolve, _tl_regio, _tl_cli, _tl_doc_identity, _tl_source_ops, _tl_nlm_admin_ops, _tl_the_thuc):
    _m.bind(sys.modules[__name__])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
