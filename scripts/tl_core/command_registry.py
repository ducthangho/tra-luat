# -*- coding: utf-8 -*-
"""tl_core.command_registry — Pha E (v1.33.58, kế hoạch nợ-kỹ-thuật E1-E4).

Registry metadata cho lệnh MỚI (determinism-era) + lệnh GHI high-risk legacy:
  risk · read_only · write_scope · requires_confirm · supports_dry_run ·
  deterministic_json_required · workflow_task · idempotency_contract · card_required · module

E2 (incremental đúng kế hoạch — 'không cần chuyển hết một lần'): 8 lệnh determinism ĐƠN GIẢN được
SINH parser từ spec (`GENERATED_SPECS` + `register_generated`); phần còn lại của build_parser giữ nguyên.
E3: tool-inventory đọc `registry_summary()`. E4: workflow-audit gọi `validate_registry()`.

Module THUẦN (không bind, không đọc global tl) — chỉ argparse + data; handler resolve lúc gọi qua tl_module.
Legacy write commands được GRANDFATHER (card_required=False) — audit chỉ bắt lệnh MỚI thiếu card,
không phá gate hiện hành; mọi lệnh ghi PHẢI có ít nhất một gate (contract/confirm/dry-run).
"""
from __future__ import annotations

import argparse
import inspect

# ───────────────────────── E2: specs sinh parser (giữ NGUYÊN VĂN help từ v1.33.50-53) ─────────────────────────
GENERATED_SPECS = [
    {"name": "tool-inventory", "handler": "cmd_tool_inventory",
     "help": "READ-ONLY: bản đồ tool/script/workflow dạng máy-đọc để Claude tra trước khi viết tool mới",
     "args": [
         {"flags": ["--group"], "help": "lọc nhóm tool, ví dụ ingest_convert/nlm_operations"},
         {"flags": ["--task"], "help": "truy vấn theo tác vụ, ví dụ 'ocr pdf scan' hoặc write_new_tool"},
         {"flags": ["--scripts"], "action": "store_true", "help": "kèm docstring scripts/*.py"},
         {"flags": ["--json"], "action": "store_true"},
     ]},
    {"name": "route-task", "handler": "cmd_route_task",
     "help": "READ-ONLY: định tuyến workflow chuẩn cho tác vụ rủi ro trước khi dry-run/apply",
     "args": [
         {"dest": "task_pos", "nargs": "?", "metavar": "task", "help": "tên tác vụ (positional — tương đương --task)"},
         {"flags": ["--task"], "help": "write_new_tool|nlm_query_quality|ingest_local|convert_rename|ingest_zip|ocr_pdf_scan|large_doc_chunk"},
         {"flags": ["--json"], "action": "store_true"},
     ]},
    {"name": "workflow-audit", "handler": "cmd_workflow_audit",
     "help": "READ-ONLY: audit workflow cards, route-task map, command inventory + registry (Pha E) để bắt drift",
     "args": [
         {"flags": ["--strict"], "action": "store_true", "help": "fail cả khi có warnings"},
         {"flags": ["--json"], "action": "store_true"},
     ]},
    {"name": "rasoat-dot-check", "handler": "cmd_rasoat_dot_check",
     "help": "READ-ONLY (offline): cổng kiểm CUỐI ĐỢT — NFC trước khi đếm · tra kho ĐỦ 3 khoá trước khi "
             "kết luận thiếu · sổ số liệu tái lập",
     "args": [
         {"flags": ["--in"], "dest": "in_dir", "help": "<out-dir> của lượt rà (NGOÀI cây skill)"},
         {"flags": ["--dot"], "help": "chỉ kiểm một Đợt (`dot_id`); bỏ trống = cả hồ sơ"},
         {"flags": ["--state"], "help": "file state; mặc định <in>/rasoat_state.json"},
         {"flags": ["--claim"], "action": "append",
          "help": "thêm một kết luận «kho thiếu» ngoài q_ingest (lặp được)"},
         {"flags": ["--ngay-chot"], "dest": "ngay_chot", "help": "ngày chốt số liệu; mặc định state.cap_nhat"},
         {"flags": ["--strict"], "action": "store_true", "help": "biến rc=1 (có phát hiện) thành rc=2 — dùng khi vào gate"},
         {"flags": ["--json"], "action": "store_true"},
         {"flags": ["--out"], "help": "ghi payload JSON ra file"},
     ]},
    {"name": "doc-claims-check", "handler": "cmd_doc_claims_check",
     "help": "READ-ONLY: kiểm CƠ HỌC trích dẫn trong văn xuôi (đường dẫn, SHA, link, version, rNNN, file.py:dòng)",
     "args": [
         {"flags": ["--path"], "action": "append",
          "help": "tệp/thư mục .md cần quét (lặp được); mặc định CHANGELOG/SKILL/CLAUDE/CONTEXT + references/"},
         {"flags": ["--strict"], "action": "store_true", "help": "biến rc=1 (có cờ) thành rc=2 — dùng khi đưa vào gate"},
         {"flags": ["--json"], "action": "store_true"},
         {"flags": ["--out"], "help": "ghi payload JSON ra file (atomic)"},
     ]},
    {"name": "golden-test", "handler": "cmd_golden_test",
     "help": "READ-ONLY mặc định: so JSON golden fixtures; --write để cập nhật fixtures",
     "args": [
         {"flags": ["--write"], "action": "store_true", "help": "ghi lại references/golden/*.json từ output deterministic hiện tại"},
         {"flags": ["--json"], "action": "store_true"},
     ]},
    {"name": "determinism-audit", "handler": "cmd_determinism_audit",
     "help": "READ-ONLY: audit schema, volatile scrub, output ổn định và golden fixtures",
     "args": [
         {"flags": ["--strict"], "action": "store_true", "help": "bắt warnings workflow và chạy golden-test"},
         {"flags": ["--full"], "action": "store_true", "help": "chạy golden-test trong audit"},
         {"flags": ["--json"], "action": "store_true"},
     ]},
    {"name": "release-manifest", "handler": "cmd_release_manifest",
     "help": "READ-ONLY: tạo RELEASE_MANIFEST SHA-256 tất định cho gói skill",
     "args": [
         {"flags": ["--root"], "help": "root gói skill; mặc định HERE.parent"},
         {"flags": ["--out"], "help": "ghi manifest ra file JSON"},
         {"flags": ["--json"], "action": "store_true"},
     ]},
    {"name": "release-verify", "handler": "cmd_release_verify",
     "help": "READ-ONLY: verify RELEASE_MANIFEST với root hiện tại (tùy chọn kiểm cả .zip qua --archive)",
     "args": [
         {"dest": "manifest"},
         {"flags": ["--root"], "help": "root gói skill; mặc định HERE.parent"},
         {"flags": ["--strict"], "action": "store_true", "help": "coi file thừa là lỗi"},
         {"flags": ["--archive"], "help": "kiểm bytes .zip: mở archive, đối chiếu từng member vs manifest + đường dẫn an toàn"},
         {"flags": ["--expected-archive-sha256"], "dest": "expected_archive_sha256",
          "help": "SHA-256 archive mong đợi (dùng với --archive) để chốt byte đã giao"},
         {"flags": ["--json"], "action": "store_true"},
     ]},
    {"name": "test-fragments-check", "handler": "cmd_test_fragments_check",
     "help": "LAND-ONLY READ-ONLY: fail nếu bundled test module committed lệch generator trên source tree",
     "args": [
         {"flags": ["--root"], "help": "repo root chứa scripts/test_fragments; mặc định HERE.parent"},
         {"flags": ["--json"], "action": "store_true"},
     ]},
    {"name": "bundle-export", "handler": "cmd_bundle_export",
     "help": "NHÁNH SONG SONG: xuất bundle giao nộp (zip + BUNDLE_META.json, GIỮ VERSION fork-point) — ADR-0001; không đổi version, không drive-push",
     "args": [
         {"flags": ["--root"], "help": "root gói skill; mặc định HERE.parent"},
         {"flags": ["--out"], "help": "đường dẫn zip output; mặc định <root>-bundle.zip cạnh root"},
         {"flags": ["--note"], "help": "ghi chú nhánh (mục đích, log gốc) — vào BUNDLE_META.json"},
         {"flags": ["--json"], "action": "store_true"},
     ]},
    {"name": "release-bundle", "handler": "cmd_release_bundle",
     "help": "OFFLINE: đóng gói zip tất định kèm RELEASE_MANIFEST.json; không gọi mạng",
     "args": [
         {"flags": ["--root"], "help": "root gói skill; mặc định HERE.parent"},
         {"flags": ["--out"], "required": True, "help": "đường dẫn zip output"},
         {"flags": ["--top"], "help": "tên thư mục top-level trong zip; mặc định tên root"},
         {"flags": ["--json"], "action": "store_true"},
     ]},
    {"name": "registry-coverage", "handler": "cmd_registry_coverage",
     "help": "READ-ONLY: báo cáo độ phủ hai chiều cây lệnh parser ↔ command registry (Packet AG-T0-03)",
     "args": [
         {"flags": ["--json"], "action": "store_true"},
         {"flags": ["--strict"], "action": "store_true", "help": "fail (rc=1) nếu có lệnh thiếu metadata"},
         {"flags": ["--unregistered-only"], "action": "store_true", "help": "chỉ in danh sách lệnh chưa có metadata"},
     ]},
    # ── I7 wave-1 (v1.34.10): sinh CƠ HỌC từ build_parser (converter AST; flags/help NGUYÊN VĂN) ──
    {"name": 'push-overflow', "handler": 'cmd_push_overflow',
     "help": 'sharding: sau source_add vào shard overflow → cập nhật registry (row_kind=overflow)',
     "args": [
         {"flags": ['--drive-id'], "dest": 'drive_id', "required": True},
         {"flags": ['--source-id'], "dest": 'source_id', "required": True},
         {"flags": ['--notebook-id'], "dest": 'notebook_id', "help": 'shard overflow (mặc định từ config overflowNotebookId)'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": '(v1.29.2) BỎ QUA precheck blocker — RỦI RO, tự chịu'},
     ]},
    {"name": 'corpus-fix', "handler": 'cmd_corpus_fix',
     "help": 'ORCHESTRATOR dọn/chỉnh lý corpus: kế hoạch THEO THỨ TỰ PHỤ THUỘC + 2 tầng (safe_auto reversible / human_confirm). DRY mặc định; --apply --tier safe chạy CHỈ reversible (infra+dedup→corpus=false)',
     "args": [
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--tier'], "choices": ['safe'], "help": '--apply --tier safe: chỉ chạy bước reversible'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": '(Pha 1) bỏ qua precheck blocker (rủi ro)'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'shared-source-fix', "handler": 'cmd_shared_source_fix',
     "help": 'FIXER shared_source_id FALSE-LINK (≥2 drive_id chung 1 nlm_source_id): GIỮ bản điểm cao, reg_clear link bản kia. DRY/report; --apply --confirm yes ghi (verify nlm-content trước)',
     "args": [
         {"dest": 'notebook_id', "nargs": '?'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--confirm'], "default": ''},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": '(Pha 1+) bỏ qua precheck blocker (rủi ro)'},
     ]},
    {"name": 'source-rename', "handler": 'cmd_source_rename',
     "help": 'đổi TÊN (+tùy chọn số hiệu) 1 nguồn VBQPPL: reg_upsert registry.name + tùy chọn đổi tên GDoc Drive (--rename-drive). Gợi ý tên chuẩn nếu bỏ --name (S14 v1.33.44: chủ đề từ title_vn + số hiệu gạch-nối đủ). DRY mặc định; verify header trước. S13: Cowork 45s chạy 1 FILE/lệnh — --rename-drive tốn ~3 round-trip (registry+Drive+NLM), batch ≥2 file SẼ timeout',
     "args": [
         {"dest": 'target', "help": 'drive_id hoặc số hiệu'},
         {"flags": ['--name'], "help": 'tên mới (bỏ trống = gợi ý chuẩn từ standardize_name)'},
         {"flags": ['--sohieu'], "help": 'số hiệu mới (tùy chọn; reg_upsert --merge)'},
         {"flags": ['--rename-drive'], "dest": 'rename_drive', "action": 'store_true', "help": 'đổi CẢ tên GDoc trên Drive + nguồn NLM (gws rename + nlm source_rename)'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": '(Pha 1+) bỏ qua precheck blocker (rủi ro)'},
     ]},
    {"name": 'source-update-corpus', "handler": 'cmd_source_update_corpus',
     "help": '(MERGE) bật/tắt cờ corpus nguồn VBQPPL: `false`=BỎ RA KHỎI CORPUS (reg_upsert corpus=false reversible + gỡ nguồn NLM, GUARD shared_source_id); `false --as-ref`=HẠ REF (r180 S2: corpus=false + row_kind=ref, GIỮ NLM); `true`=đưa vào lại. r197: N target = LÔ registry-thuần (CHỈ true hoặc false --as-ref; 1 reg_bulk + 1 reg_get_bulk verify, journal 1 run undo cả lô, auto-refresh manifest trước plan). DRY mặc định; --apply --confirm yes',
     "args": [
         {"dest": 'target', "nargs": '+', "help": 'drive_id hoặc số hiệu (N giá trị = lô r197; bulk CHỈ true hoặc false --as-ref)'},
         {"dest": 'status', "help": 'true/false (đưa vào / bỏ ra khỏi corpus)'},
         {"flags": ['--as-ref'], "dest": 'as_ref', "action": 'store_true', "help": 'r180 S2 (chỉ với false): hạ thành ref — corpus=false + row_kind=ref, GIỮ nguồn NLM/nlm_status (tham khảo truy-vấn-được)'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--confirm'], "default": ''},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": '(Pha 1+) bỏ qua precheck blocker (rủi ro)'},
     ]},
    {"name": 'verify-staged', "handler": 'cmd_verify_staged',
     "help": '(r200 staged lane — grill 24-07) verify PARITY các dòng staged (đọc toàn văn + verify_gate + quét Điều/chunk — ĐÚNG bộ cổng lane thường, đổi thời điểm KHÔNG đổi tiêu chuẩn): DRY = báo cáo; --apply --confirm yes: PASS → bulk-flip corpus=true + note thật (1 reg_bulk journaled, undo cả lô), FAIL → ở lại staged (note staged:fail:<FLAG>), KHÔNG auto-xóa/KHÔNG NLM. NLM nạp SAU qua nlm-links (bảng tay khối ≤4)/nlm-reconcile',
     "args": [
         {"flags": ['--drive-ids'], "dest": 'drive_ids', "help": 'CSV drive_id — chỉ verify các dòng này (mặc định: mọi dòng note staged:* trong scope profile)'},
         {"flags": ['--chunk-max-chars'], "dest": 'chunk_max_chars', "type": int, "help": 'ngưỡng flag needs_chunk_pipeline (mặc định 100000 — parity profile-ingest)'},
         {"flags": ['--allow-default'], "dest": 'allow_default', "action": 'store_true', "help": 'cho phép chạy trên profile vbqppl (mặc định chặn — mirror profile-ingest)'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--confirm'], "default": ''},
         {"flags": ['--refresh'], "action": 'store_true', "help": '(danh nghĩa — dò staged LUÔN refresh manifest LIVE, bài học 24-07)'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": '(Pha 1+) bỏ qua precheck blocker (rủi ro)'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'source-delete', "handler": 'cmd_source_delete',
     "help": '(MERGE) XÓA CỨNG 1 nguồn VBQPPL (bất khả nghịch): gỡ NLM (GUARD shared_source_id) + trash Drive + xóa dòng registry. DRY mặc định; --apply --confirm yes. Cân nhắc `source-update-corpus false` (reversible) trước',
     "args": [
         {"dest": 'target', "help": 'drive_id hoặc số hiệu'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--confirm'], "default": ''},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": '(Pha 1+) bỏ qua precheck blocker (rủi ro)'},
     ]},
    {"name": 'quarantine-fix', "handler": 'cmd_quarantine_fix',
     "help": 'COMPOSITE dọn quarantine mâu thuẫn: set corpus=false cho raw-dup gán nhầm + chuẩn hoá nhãn biến thể (--apply); báo review_restore (GDoc kẹt) + ghost_nlm (xoá nguồn tay). DRY mặc định',
     "args": [
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": '(Pha 1+) bỏ qua precheck blocker (rủi ro)'},
     ]},
    {"name": 'dedup-plan', "handler": 'cmd_dedup_plan',
     "help": 'COMPOSITE: kế hoạch dedup toàn corpus 1 lệnh (thay hygiene plan từng cụm) — GIỮ canonical, set corpus=false bản dup CÙNG văn bản (reversible). DRY mặc định; review/dups-on-nlm chỉ báo',
     "args": [
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": '(Pha 1+) bỏ qua precheck blocker (rủi ro)'},
     ]},
    {"name": 'dedup-corpus', "handler": 'cmd_dedup_corpus',
     "help": '(v1.34.63 B1) dedup TRỤC NỘI DUNG (md5-first → content-hash → BoW-Jaccard; COEXIST dedup-plan trục chủ đề): 7 classification DUP_EXACT/MISLABEL_RESOLVED/_UNRESOLVED/PHYSICAL_DUP/NEAR_DUP_REVIEW/JUNK/CROSS_PROFILE_DUAL_REG; docx-gốc+GDoc-convert KHÔNG dup; picker on-NLM-first. DRY mặc định; --apply --confirm yes: mode corpus-false (reversible) | delete (opt-in)',
     "args": [
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--confirm'], "default": '', "help": "gõ 'yes' xác nhận apply (contract high-risk)"},
         {"flags": ['--mode'], "choices": ['corpus-false', 'delete'], "default": 'corpus-false', "help": 'corpus-false = reversible (mặc định); delete = source-delete trash Drive (OPT-IN, ADR-5)'},
         {"flags": ['--only-md5'], "dest": 'only_md5', "help": 'chỉ apply nhóm có key/md5 này (duyệt từng bước — ADR-7)'},
         {"flags": ['--limit'], "type": int, "help": 'trần số NHÓM apply mỗi lần'},
         {"flags": ['--near-threshold'], "dest": 'near_threshold', "type": float, "default": 0.95, "help": 'ngưỡng Jaccard dải NEAR (ADR-A2-3, mặc định 0.95)'},
         {"flags": ['--all-profiles'], "dest": 'all_profiles', "action": 'store_true', "help": 'quét XUYÊN profile — FLAG-ONLY (CROSS_PROFILE_DUAL_REG, không apply — ADR-6)'},
         {"flags": ['--refresh'], "action": 'store_true', "help": 'bỏ cache manifest + content-hash, đọc lại từ nguồn'},
         {"flags": ['--out'], "help": 'ghi envelope JSON ra file (kế hoạch lớn — né tràn stdout)'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": '(Pha 1+) bỏ qua precheck blocker (rủi ro)'},
     ]},
    {"name": 'vbhn-year-fix', "handler": 'cmd_vbhn_year_fix',
     "help": 'BẤT BIẾN ĐẶT TÊN: số hiệu VBHN PHẢI có NĂM (số tái dùng theo năm→collision). Quét VBHN sohieu THIẾU năm → suy năm (ngày ban hành) → reg_upsert sohieu NN-YYYY-VBHN-XXX. DRY mặc định; --apply ghi; --with-name sửa cả tên',
     "args": [
         {"flags": ['--limit'], "type": int, "help": 'số dòng tối đa mỗi lần'},
         {"flags": ['--with-name'], "dest": 'with_name', "action": 'store_true', "help": 'cập nhật CẢ trường tên (chèn năm vào token VBHN trong tên)'},
         {"flags": ['--apply'], "action": 'store_true', "help": 'THỰC THI ghi reg_upsert (mặc định DRY)'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": '(Pha 1) bỏ qua precheck blocker (rủi ro)'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'recat', "handler": 'cmd_recat',
     "help": 'di dời file → folder chủ đề (mkdir nếu thiếu) + cập nhật registry; --quarantine để cách ly (DRY mặc định)',
     "args": [
         {"dest": 'drive_id', "nargs": '+'},
         {"flags": ['--cat']},
         {"flags": ['--quarantine'], "action": 'store_true'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--force-cat'], "dest": 'force_cat', "action": 'store_true', "help": 'G3: bỏ qua cảnh báo BOUNDARY_CONFLICT (xác nhận cố ý đặt cat này)'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": '(Pha 1) bỏ qua precheck blocker (rủi ro clobber/ghi-mù)'},
     ]},
    {"name": 'backfill-loai', "handler": 'cmd_backfill_loai',
     "help": "KH1 Pha 1.5: suy `loai` chuẩn cho dòng registry thiếu loai (từ tên+số hiệu); ★--normalize (v1.30.1): sửa CẢ dòng loai PHI-CHUẨN map tất định ('Luat'→'Luật'). DRY mặc định, --apply ghi",
     "args": [
         {"flags": ['--limit'], "type": int, "help": 'số dòng tối đa mỗi lần (mặc định: tất cả suy được)'},
         {"flags": ['--normalize'], "action": 'store_true', "help": '(v1.30.1 #4) sửa cả dòng loai ĐÃ CÓ nhưng SAI enum, chỉ map TẤT ĐỊNH qua _normalize_loai; giá trị lạ → báo, không đoán'},
         {"flags": ['--apply'], "action": 'store_true', "help": 'THỰC THI ghi reg_bulk cột loai (mặc định DRY)'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'backfill-title-vn', "handler": 'cmd_backfill_titlevn',
     "help": '(v1.31.0 P0-1) BACKFILL cột title_vn = TRÍCH YẾU CÓ DẤU từ HEADER thật (cột sẵn có v2.13.0) → QT-5 sinh query có dấu, hết literal-filename. DRY mặc định; đọc header chậm → lô 40 + --offset',
     "args": [
         {"flags": ['--limit'], "type": int, "help": 'số dòng đọc header mỗi lần (mặc định 40)'},
         {"flags": ['--offset'], "type": int, "help": 'phân trang (next_offset in ở cuối trang trước)'},
         {"flags": ['--force-refresh'], "dest": 'force_refresh', "action": 'store_true', "help": 'đè CẢ title_vn hiện có nếu nó là tên-file/không dấu (title_vn có dấu THẬT không bao giờ bị đè)'},
         {"flags": ['--from-tukhoa'], "dest": 'from_tukhoa', "action": 'store_true', "help": "(v1.31.1 N2) tier-2 OFFLINE: bóc '(Bộ luật|Luật) <chủ đề>' từ field tukhoa (0 call/dòng, quét cả pool) — guard cross-check token tên (đã expand viết tắt CNTT/BHXH…); chạy TRƯỚC, header vét phần còn lại"},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": 'bỏ qua precheck blocker (rủi ro)'},
         {"flags": ['--apply'], "action": 'store_true', "help": 'ghi reg_bulk cột title_vn (journaled, undo được)'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--out'], "help": '(MERGE bundle-45b v1.33.47) ghi JSON summary ra file atomically; tự bật JSON (né trần 30s Cowork)'},
     ]},
    {"name": 'backfill-hieuluc', "handler": 'cmd_backfill_hieuluc',
     "help": '(v1.33.49 P1) BACKFILL cột hieuluc từ header thật: Còn/Hết/Chưa hiệu lực + ngày hiệu lực nếu có. DRY mặc định; đọc header chậm → lô 40 + --offset',
     "args": [
         {"flags": ['--limit'], "type": int, "help": 'số dòng đọc header mỗi lần (mặc định 40)'},
         {"flags": ['--offset'], "type": int, "help": 'phân trang (next_offset in ở cuối trang trước)'},
         {"flags": ['--force-refresh'], "dest": 'force_refresh', "action": 'store_true', "help": 'refresh cả dòng hieuluc mơ hồ như can_kiem_tra/unknown; không đè nhãn rõ'},
         {"flags": ['--infer-from-date'], "dest": 'infer_from_date', "action": 'store_true', "help": 'cho phép suy Còn/Chưa từ ngày hiệu lực khi header không có nhãn trạng thái rõ'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": 'bỏ qua precheck blocker (rủi ro)'},
         {"flags": ['--apply'], "action": 'store_true', "help": 'ghi reg_bulk cột hieuluc (journaled, undo được)'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--out'], "help": 'ghi JSON summary ra file atomically; tự bật JSON'},
     ]},
    {"name": 'backfill-nlm-status', "handler": 'cmd_backfill_nlm_status',
     "help": "r179 (ADR-0010): nắn nlm_status về TỪ VỰNG ĐÓNG — map tất định added→pushed, live→active "
             "(reg_upsert per-row, journaled, undo được); giá trị ngoài map (ready/typo) KHÔNG đụng, báo stray. "
             "DRY mặc định, --apply ghi. Chạy MỘT LẦN sau deploy r179 (cửa ghi register đã đóng từ vựng)",
     "args": [
         {"flags": ['--limit'], "type": int, "help": 'số dòng tối đa mỗi lần (mặc định: tất cả map được)'},
         {"flags": ['--apply'], "action": 'store_true', "help": 'THỰC THI reg_upsert per-row (mặc định DRY)'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'missing-sohieu', "handler": 'cmd_missing_sohieu',
     "help": 'KH1 Pha 1.5: đề xuất số hiệu cho dòng registry thiếu sohieu (parse từ tên); DRY mặc định, --apply ghi. ⚠ xác minh bằng header-verify (G2)',
     "args": [
         {"flags": ['--limit'], "type": int, "help": 'số dòng tối đa mỗi lần'},
         {"flags": ['--apply'], "action": 'store_true', "help": 'THỰC THI ghi reg_bulk cột sohieu (mặc định DRY)'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": '(Pha 1) bỏ qua precheck blocker (rủi ro)'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'reg-delete', "handler": 'cmd_reg_delete',
       "help": 'gỡ dòng registry theo drive_ids (bọc reg_delete); --force bỏ bảo vệ removed*',
       "args": [
           {"flags": ['--drive-ids'], "dest": 'drive_ids', "required": True, "help": 'id1,id2,...'},
           {"flags": ['--force'], "action": 'store_true', "help": 'gỡ bất kể nlm_status (bỏ require_removed)'},
           {"flags": ['--confirm'], "choices": ['yes'], "required": True,
            "help": 'xác nhận tường minh trước khi xóa dòng registry'},
       ]},
    {"name": 'nlm-query-plan', "handler": 'cmd_nlm_query_plan',
     "help": 'READ-ONLY: lập kế hoạch truy vấn NLM hẹp theo source_id trước khi gọi nlm-query/nlm-cross',
     "args": [
         {"dest": 'question', "nargs": '?', "help": 'câu hỏi dự kiến gửi NLM'},
         {"flags": ['--source-id'], "action": 'append', "default": [], "help": 'source_id đã chọn; có thể lặp lại'},
         {"flags": ['--source-ids'], "help": 'danh sách source_id cách nhau bằng dấu phẩy'},
         {"flags": ['--justification'], "help": 'bắt buộc khi dùng 4-5 nguồn trong một lượt hỏi'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'live-smoke-plan', "handler": 'cmd_live_smoke_plan',
     "help": 'READ-ONLY: xuất kế hoạch test live Drive/NLM theo thứ tự an toàn; không gọi mạng',
     "args": [
         {"flags": ['--include-ocr'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'live-readiness', "handler": 'cmd_live_readiness',
     "help": 'READ-ONLY: báo cáo 3 tầng env/contract/apply; không ghi Drive/NLM',
     "args": [
         {"flags": ['--include-ocr'], "action": 'store_true'},
         {"flags": ['--config-file'], "help": 'file config để kiểm hiện diện webapp/token; không in secret'},
         {"flags": ['--skip-contract'], "action": 'store_true', "help": 'chỉ kiểm env local, không gọi live read-only'},
         {"flags": ['--smoke-proof'], "help": 'file JSON diff/smoke proof; thiếu proof thì apply_ready=false'},
         {"flags": ['--strict'], "action": 'store_true', "help": 'rc=2 nếu chưa ready_for_live_smoke'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'live-contract-check', "handler": 'cmd_live_contract_check',
     "help": 'READ-ONLY: gọi webapp ping/info + NLM get/list tối thiểu; không upload/register/add',
     "args": [
         {"flags": ['--include-ocr'], "action": 'store_true'},
         {"flags": ['--config-file'], "help": 'file config để nạp TL_WEBAPP/TL_TOKEN/profile'},
         {"flags": ['--timeout'], "type": int, "default": 60},
         {"flags": ['--strict'], "action": 'store_true', "help": 'rc=2 nếu live_contract_ready=false'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'live-state-snapshot', "handler": 'cmd_live_state_snapshot',
     "help": 'READ-ONLY: chụp trạng thái live trước/sau smoke để diff',
     "args": [
         {"flags": ['--out'], "required": True, "help": 'file JSON snapshot cần ghi'},
         {"flags": ['--config-file'], "help": 'file config để nạp TL_WEBAPP/TL_TOKEN/profile'},
         {"flags": ['--include-ocr'], "action": 'store_true'},
         {"flags": ['--no-contract'], "action": 'store_true', "help": 'không gọi live-contract-check trong snapshot'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'live-state-diff', "handler": 'cmd_live_state_diff',
     "help": 'READ-ONLY: so before/after snapshot; fail nếu có thay đổi ngoài --allow',
     "args": [
         {"dest": 'before'},
         {"dest": 'after'},
         {"flags": ['--allow'], "action": 'append', "default": [], "help": 'path prefix được phép thay đổi, ví dụ source_counts hoặc notebooks.get.source_count'},
         {"flags": ['--out'], "help": 'ghi diff JSON'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'deploy-plan', "handler": 'cmd_deploy_plan',
     "help": 'READ-ONLY: kế hoạch triển khai bundle an toàn có backup, verify, smoke test',
     "args": [
         {"flags": ['--bundle'], "help": 'zip release cần triển khai'},
         {"flags": ['--target-dir'], "help": 'thư mục skill đích'},
         {"flags": ['--backup-dir'], "help": 'thư mục lưu backup'},
         {"flags": ['--include-ocr'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'rollback-plan', "handler": 'cmd_rollback_plan',
     "help": 'READ-ONLY: kế hoạch rollback từ backup hoặc bundle trước đó',
     "args": [
         {"flags": ['--target-dir'], "help": 'thư mục skill đích'},
         {"flags": ['--backup-path'], "help": 'thư mục backup đã biết'},
         {"flags": ['--bundle'], "help": 'bundle cũ dùng để rollback nếu không có backup dir'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'final-acceptance', "handler": 'cmd_final_acceptance',
     "help": 'OFFLINE: kiểm cuối trước bàn giao; tổng hợp release/workflow/live-readiness plan',
     "args": [
         {"flags": ['--include-ocr'], "action": 'store_true'},
         {"flags": ['--strict-live'], "action": 'store_true', "help": 'fail nếu live-readiness chưa đạt; mặc định offline pass vẫn ok'},
         {"flags": ['--out'], "help": 'ghi report JSON'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'go-live-runbook', "handler": 'cmd_go_live_runbook',
     "help": 'READ-ONLY: xuất runbook triển khai live + smoke test + rollback dạng Markdown',
     "args": [
         {"flags": ['--include-ocr'], "action": 'store_true'},
         {"flags": ['--out'], "help": 'ghi Markdown ra file'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'release-check', "handler": 'cmd_release_check',
     "help": 'OFFLINE: acceptance harness tất định trước khi đóng gói; không ghi Drive/NLM',
     "args": [
         {"flags": ['--out-dir']},
         {"flags": ['--out']},
         {"flags": ['--full'], "action": 'store_true', "help": 'chạy thêm tl --selftest nặng; mặc định release-check chỉ chạy harness nhanh'},
         {"flags": ['--strict-determinism'], "action": 'store_true', "help": 'chạy thêm determinism-audit --strict, gồm golden-test'},
         {"flags": ['--verbose'], "action": 'store_true', "help": 'in tiến độ từng bước ra stderr'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'convert-verify', "handler": 'cmd_convert_verify',
     "help": 'READ-ONLY: verify/readback sau Drive convert/rename/move trước khi add NLM',
     "args": [
         {"flags": ['--gdoc-id'], "required": True},
         {"flags": ['--src-id'], "help": 'file gốc nhị phân nếu có'},
         {"flags": ['--expected-name'], "help": 'tên GDoc kỳ vọng'},
         {"flags": ['--expected-src-name'], "help": 'tên file gốc kỳ vọng'},
         {"flags": ['--expected-folder-id'], "help": 'folder đích kỳ vọng'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'ingest-zip', "handler": 'cmd_ingest_zip',
     "help": 'DRY mặc định: giải nén zip an toàn và lập batch plan nạp VBQPPL; --apply --confirm yes chạy thật từng member (child_apply, journal ingest_zip_apply.v1)',
     "args": [
         {"dest": 'file'},
         {"flags": ['--cat'], "help": 'category VBQPPL dự kiến; thiếu cat sẽ cảnh báo'},
         {"flags": ['--max-files'], "type": int, "default": 200},
         {"flags": ['--max-size-mb'], "type": int, "default": 100},
         {"flags": ['--max-total-mb'], "dest": 'max_total_mb', "type": int, "default": 500},
         {"flags": ['--max-ratio'], "dest": 'max_ratio', "type": float, "default": 100.0},
         {"flags": ['--workers'], "type": int, "default": 4},
         {"flags": ['--apply'], "action": 'store_true', "help": 'thực thi batch sau dry-run; yêu cầu --confirm yes'},
         {"flags": ['--confirm'], "choices": ['yes'], "help": 'bắt buộc khi --apply'},
         {"flags": ['--expected-plan-hash'], "dest": 'expected_plan_hash', "help": 'plan_hash từ dry-run'},
         {"flags": ['--continue-on-error'], "action": 'store_true', "help": 'không đổi hành vi ingest-zip (LUÔN xử lý mọi member rồi báo counts/partial, ok=all); giữ để tương thích'},
         {"flags": ['--skip-nlm-preflight'], "action": 'store_true', "help": 'truyền xuống ingest-local nếu cần tự vá NLM sau'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-ingest-zip', "handler": 'cmd_profile_ingest_zip',
     "help": 'DRY mặc định: giải nén zip an toàn và lập batch plan nạp profile; --apply --confirm yes chạy thật từng member (child_apply, journal ingest_zip_apply.v1)',
     "args": [
         {"dest": 'file'},
         {"flags": ['--max-files'], "type": int, "default": 200},
         {"flags": ['--max-size-mb'], "type": int, "default": 100},
         {"flags": ['--max-total-mb'], "dest": 'max_total_mb', "type": int, "default": 500},
         {"flags": ['--max-ratio'], "dest": 'max_ratio', "type": float, "default": 100.0},
         {"flags": ['--workers'], "type": int, "default": 4},
         {"flags": ['--apply'], "action": 'store_true', "help": 'thực thi batch sau dry-run; yêu cầu --confirm yes'},
         {"flags": ['--confirm'], "choices": ['yes'], "help": 'bắt buộc khi --apply'},
         {"flags": ['--expected-plan-hash'], "dest": 'expected_plan_hash', "help": 'plan_hash từ dry-run'},
         {"flags": ['--continue-on-error'], "action": 'store_true', "help": 'không đổi hành vi ingest-zip (LUÔN xử lý mọi member rồi báo counts/partial, ok=all); giữ để tương thích'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'ingest-ocr', "handler": 'cmd_ingest_ocr',
     "help": 'BRIDGE: verify OCR text rồi gọi lại ingest-local cho VBQPPL; không ghi trực tiếp',
     "args": [
         {"dest": 'file'},
         {"flags": ['--text-file'], "dest": 'text_file', "required": True},
         {"flags": ['--cat'], "required": True},
         {"flags": ['--name']},
         {"flags": ['--sohieu']},
         {"flags": ['--goc']},
         {"flags": ['--hieuluc']},
         {"flags": ['--loai']},
         {"flags": ['--force-cat'], "dest": 'force_cat', "action": 'store_true'},
         {"flags": ['--allow-large'], "dest": 'allow_large', "action": 'store_true'},
         {"flags": ['--skip-nlm-preflight'], "dest": 'skip_nlm_preflight', "action": 'store_true'},
         {"flags": ['--skip-live-check'], "dest": 'skip_live_check', "action": 'store_true'},
         {"flags": ['--ocr-verified'], "dest": 'ocr_verified', "action": 'store_true',
          "help": '(r196) CAM KẾT đã đối chiếu OCR với bản gốc (neo ≥6 từ, đủ trang/Điều/phụ lục) — bridge chỉ forward cờ này cho child; thiếu = chặn rc=2'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--confirm'], "choices": ['yes'], "help": 'bắt buộc khi --apply'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-ingest-ocr', "handler": 'cmd_profile_ingest_ocr',
     "help": 'BRIDGE: verify OCR text rồi gọi lại profile-ingest; không ghi trực tiếp',
     "args": [
         {"dest": 'file'},
         {"flags": ['--text-file'], "dest": 'text_file', "required": True},
         {"flags": ['--name']},
         {"flags": ['--hieuluc']},
         {"flags": ['--chunk-max-chars'], "dest": 'chunk_max_chars', "type": int, "default": 100000},
         {"flags": ['--allow-default'], "dest": 'allow_default', "action": 'store_true'},
         {"flags": ['--skip-live-check'], "dest": 'skip_live_check', "action": 'store_true'},
         {"flags": ['--ocr-verified'], "dest": 'ocr_verified', "action": 'store_true',
          "help": '(r196) CAM KẾT đã đối chiếu OCR với bản gốc (neo ≥6 từ, đủ trang) — bridge chỉ forward cờ này cho child; thiếu = chặn rc=2'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--confirm'], "choices": ['yes'], "help": 'bắt buộc khi --apply'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-ingest-chunks', "handler": 'cmd_profile_ingest_chunks',
     "help": 'BRIDGE: verify chunk_manifest rồi gọi lại profile-ingest từng chunk; không ghi trực tiếp',
     "args": [
         {"dest": 'manifest'},
         {"flags": ['--allow-default'], "dest": 'allow_default', "action": 'store_true'},
         {"flags": ['--skip-live-check'], "dest": 'skip_live_check', "action": 'store_true'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--confirm'], "choices": ['yes'], "help": 'bắt buộc khi --apply'},
         {"flags": ['--continue-on-error'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'ocr-analyze', "handler": 'cmd_ocr_analyze',
     "help": 'READ-ONLY: phân tích text-layer/chất lượng text của file, ưu tiên PDF scan/OCR',
     "args": [
         {"dest": 'file'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'ocr-run', "handler": 'cmd_ocr_run',
     "help": 'LOCAL: tạo sidecar text OCR/text-layer; Drive/Paddle/DocumentAI bị gate nếu chưa cấu hình',
     "args": [
         {"dest": 'file'},
         {"flags": ['--engine'], "choices": ['auto', 'none', 'ocrmypdf', 'drive', 'paddle', 'documentai'], "default": 'auto'},
         {"flags": ['--lang'], "default": 'vi', "help": 'Drive/Paddle dùng vi; OCRmyPDF/Tesseract thường dùng vie+eng'},
         {"flags": ['--mode'], "choices": ['vbqppl', 'profile'], "default": 'profile'},
         {"flags": ['--out-dir']},
         {"flags": ['--force-ocr'], "action": 'store_true'},
         {"flags": ['--timeout'], "type": int, "default": 600},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'ocr-verify', "handler": 'cmd_ocr_verify',
     "help": 'READ-ONLY: kiểm chất lượng text OCR trước khi cho phép --ocr-verified',
     "args": [
         {"dest": 'text_file'},
         {"flags": ['--source']},
         {"flags": ['--mode'], "choices": ['vbqppl', 'profile'], "default": 'profile'},
         {"flags": ['--no-manifest'], "action": 'store_true',
          "help": '(v1.34.40 A.3) đo chất-lượng-thô CỐ Ý không có ocr_manifest (text tự extract, không qua ocr-run) — mặc định thiếu manifest = FAIL vì không đối chiếu được hash'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'chunk-plan', "handler": 'cmd_chunk_plan',
     "help": 'READ-ONLY: lập kế hoạch tách văn bản lớn theo cấu trúc',
     "args": [
         {"dest": 'file'},
         {"flags": ['--mode'], "choices": ['profile', 'vbqppl-helper', 'vbqppl-canonical'], "default": 'profile'},
         {"flags": ['--name']},
         {"flags": ['--max-chars'], "type": int, "default": 100000},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'chunk-apply', "handler": 'cmd_chunk_apply',
     "help": 'LOCAL: tạo chunk files + manifest từ kế hoạch tách; chưa ghi Drive/NLM',
     "args": [
         {"dest": 'file'},
         {"flags": ['--mode'], "choices": ['profile', 'vbqppl-helper', 'vbqppl-canonical'], "default": 'profile'},
         {"flags": ['--name']},
         {"flags": ['--max-chars'], "type": int, "default": 100000},
         {"flags": ['--out-dir']},
         {"flags": ['--expected-hash']},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'chunk-verify', "handler": 'cmd_chunk_verify',
     "help": 'READ-ONLY: verify manifest/files do chunk-apply tạo',
     "args": [
         {"dest": 'manifest'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    # ── I7 wave-2 (v1.34.11): sinh CƠ HỌC từ build_parser (converter AST; flags/help NGUYÊN VĂN) ──
    {"name": 'ping', "handler": 'cmd_ping',
     "args": [
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'cowork-plan', "handler": 'cmd_cowork_plan',
     "help": 'READ-ONLY: checklist bootstrap Cowork (package integrity, gws MUSL, nlm --resume/PATH, slot/counts) — không gọi mạng nặng',
     "args": [
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--out'], "help": 'ghi JSON ra file atomically; tự bật JSON'},
         {"flags": ['--env'], "choices": ['code', 'cowork', 'chat'], "default": 'cowork'},
     ]},
    {"name": 'perf', "handler": 'cmd_perf',
     "help": 'đo thời gian thật từng thao tác (round-trip Apps Script, lợi ích song song, cache)',
     "args": [
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'init-config', "handler": 'cmd_init_config',
     "help": 'lưu ~/.tra_luat_config.json — phiên trống: --from-public (curl, mặc định) / --file (Drive MCP) / --from-drive (direct-media)',
     "args": [
         {"flags": ['--from-public'], "dest": 'from_public', "action": 'store_true', "help": '★ curl CONFIG_FILEID PUBLIC (drive.usercontent) — KHÔNG cần Drive MCP/token'},
         {"flags": ['--no-gws'], "dest": 'no_gws', "action": 'store_true', "help": 'ĐỪNG tự bật gws sau khi lưu config (mặc định: tự gws-auth-load + gws-bootstrap-cowork từ cred public)'},
         {"flags": ['--no-binary'], "dest": 'no_binary', "action": 'store_true', "help": '(với --from-public) chỉ nạp gws CRED, KHÔNG tải gws BINARY (find/ghi sẽ đi GAS)'},
         {"flags": ['--nlm'], "dest": 'nlm', "action": 'store_true', "help": '(với --from-public) GỘP cài nlm CLI (uv) + auth headless — bootstrap đầy đủ 1 lệnh'},
         {"flags": ['--file'], "help": 'đọc config từ file JSON đã tải (Drive MCP) — phiên trống, KHÔNG cần master key'},
         {"flags": ['--from-drive'], "dest": 'from_drive', "action": 'store_true', "help": 'tự tải CONFIG_FILEID bằng direct-media (cần gws cred)'},
         {"flags": ['--file-id'], "dest": 'file_id', "help": 'fileId config trên Drive (mặc định CONFIG_FILEID)'},
         {"flags": ['--env'], "choices": ['code', 'cowork', 'chat'], "help": 'ép runtime env'},
         {"flags": ['--config-json']},
         {"flags": ['--webapp']},
         {"flags": ['--token']},
         {"flags": ['--manifest-id'], "dest": 'manifest_id'},
         {"flags": ['--out']},
         {"flags": ['--replace'], "action": 'store_true', "help": 'r280: GHI ĐÈ TRỌN thay vì HOÀ vào config có sẵn — XOÁ block profiles đang có (mặc định: hoà + backup)'},
     ]},
    {"name": 'doctor', "handler": 'cmd_doctor',
     "args": [
         {"flags": ['--config'], "default": argparse.SUPPRESS},
         {"flags": ['--offline'], "action": 'store_true'},
         {"flags": ['--deep'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--out'], "help": 'ghi JSON ra file atomically; tự bật JSON'},
     ]},
    {"name": 'precheck', "handler": 'cmd_precheck',
     "help": '(Pha 0, write-safety) kiểm BẤT BIẾN trước khi ghi: registryDocId≠Doc-legacy, profile-registryDocId≠rỗng (chống clobber 766 dòng), snapshot tươi, --cols ∈ schema. READ-ONLY, rc=1 nếu blocker. (khác `preflight`=sharding NLM)',
     "args": [
         {"flags": ['--config'], "default": argparse.SUPPRESS},
         {"flags": ['--profile'], "default": argparse.SUPPRESS},
         {"flags": ['--cols'], "help": '(tùy chọn) danh sách cột định ghi, phẩy — kiểm ∈ REGISTRY_SCHEMA_COLS (chống so_hieu≠sohieu)'},
         {"flags": ['--gws-live'], "action": 'store_true', "help": '(R1) đọc registry Sheet LIVE qua gws + báo DRIFT so với manifest (read-only, opt-in)'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'journal', "handler": 'cmd_journal',
     "help": '(Pha 0) xem nhật ký WAL ~/.tl_journal: KHÔNG tham số=liệt kê run; <run_id>=done/inflight/undo. READ-ONLY trừ --close (S7 v1.33.44: tự đóng inflight đã được lệnh khác hoàn tất)',
     "args": [
         {"dest": 'run_id', "nargs": '?'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--close'], "action": 'store_true', "help": '(S7 v1.33.44) SELF-HEAL: đối chiếu intent.set các op inflight với registry HIỆN TẠI — khớp hết → append commit healed vào journal (resume/undo hết coi là dở). Chỉ ghi file journal local.'},
         {"flags": ['--force'], "action": 'store_true', "help": 'đóng CẢ op không khớp/không so được (chỉ khi ĐÃ verify remote tay)'},
         {"flags": ['--refresh'], "action": 'store_true', "help": 'ép manifest tươi trước khi đối chiếu --close (né GAS cache 600s)'},
     ]},
    {"name": 'resume', "handler": 'cmd_resume',
     "help": '(Pha 2) tiếp tục 1 run bị ngắt: LÀM LẠI op DỞ (intent chưa commit) bằng `set` đã lưu (idempotent, chỉ registry). DRY mặc định; --apply ghi',
     "args": [
         {"dest": 'run_id'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": 'bỏ qua precheck blocker (rủi ro)'},
         {"flags": ['--config'], "default": argparse.SUPPRESS},
         {"flags": ['--profile'], "default": argparse.SUPPRESS},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'undo', "handler": 'cmd_undo',
     "help": '(Pha 2) HOÀN TÁC ghi registry của 1 run: khôi phục `before` các dòng đã commit-ok reversible (chỉ registry; NLM/Drive KHÔNG undo). DRY mặc định; --apply --confirm yes',
     "args": [
         {"dest": 'run_id'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--confirm']},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": 'bỏ qua precheck blocker (rủi ro)'},
         {"flags": ['--config'], "default": argparse.SUPPRESS},
         {"flags": ['--profile'], "default": argparse.SUPPRESS},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'verify-integrity', "handler": 'cmd_verify_integrity',
     "help": 'DETECT cắt cụt/NUL MỌI scripts/*.py (đối chiếu _parts); --fix ghép lại file hỏng từ _parts (ghi Python, né Edit/Write Cowork)',
     "args": [
         {"flags": ['--fix'], "action": 'store_true', "help": 'ghép lại file TRUNCATED/NUL/MISSING từ _parts (không đụng DRIFT)'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'edit-skill', "handler": 'cmd_edit_skill',
     "help": 'III.2: sửa file skill AN TOÀN (assert đếm → py_compile → write_text), né Edit/Write mount Cowork. DRY mặc định',
     "args": [
         {"dest": 'file', "help": 'tên/đường dẫn file skill (mặc định trong scripts/)'},
         {"flags": ['--patch'], "help": 'JSON [{"old":..,"new":..,"count":1}]'},
         {"flags": ['--patch-file'], "dest": 'patch_file', "help": 'đọc patch JSON từ file'},
         {"flags": ['--apply'], "action": 'store_true', "help": 'GHI thật (mặc định DRY: chỉ assert + py_compile)'},
     ]},
    {"name": 'profile-info', "handler": 'cmd_profile_info',
     "help": 'đọc config v2 và in folder/notebook/registry/manifest của profile',
     "args": [
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'config-pin-registry', "handler": 'cmd_config_pin_registry',
     "help": 'pin registryDocId Sheet thật vào config local (không gọi Drive/Sheets; xử S-9 auto-discover)',
     "args": [
         {"dest": 'registry_doc_id'},
         {"flags": ['--profile-name'], "dest": 'profile_name', "help": 'profile cần pin; mặc định defaultProfile/vbqppl'},
         {"flags": ['--root'], "action": 'store_true', "help": 'pin vào root registryDocId thay vì profiles.<name>.registryDocId'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--out'], "help": 'ghi JSON kết quả ra file'},
     ]},
    {"name": 'profile-list', "handler": 'cmd_profile_list',
     "help": 'liệt kê profiles trong config; --discover quét Van_ban_thuong LIVE đối chiếu (v1.30.0); --templates liệt kho mẫu chung + mẫu từng profile (v1.34.71)',
     "args": [
         {"flags": ['--discover'], "action": 'store_true', "help": 'quét Van_ban_thuong trên Drive: profile-thật chưa vào config (gợi ý profile-adopt), vỏ rỗng, asset lạc gốc'},
         {"flags": ['--templates'], "dest": 'templates', "action": 'store_true',
          "help": '(v1.34.71 Q6) liệt kê KHO MẪU CHUNG (_meta/templates VBQPPL — folder-là-danh-mục) + entries templates trong marker từng profile đã cấu hình. Cần webapp LIVE'},
         {"flags": ['--folder-cap'], "dest": 'folder_cap', "type": int, "default": 60, "help": 'trần số thư mục con quét (mặc định 60, LOUD khi cắt)'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-promote', "handler": 'cmd_profile_promote',
     "help": '(v1.34.25, Q2+Q3+Q5) BIẾN FOLDER DRIVE THƯỜNG THÀNH PROFILE: dựng hạ tầng còn thiếu (_meta/registry/manifest/notebook/marker/config, asset sẵn có DÙNG LẠI) + seed registry từ nội dung folder + NLM System Prompt generator-sinh tự áp; nạp NLM đi ingest-missing --allow-no-sohieu SAU. DRY mặc định',
     "args": [
         {"flags": ['--name'], "required": True, "help": 'tên profile mới'},
         {"flags": ['--folder'], "required": True, "help": 'folder id Drive thường cần promote'},
         {"flags": ['--notebook'], "help": 'notebookId NLM sẵn có (loại trừ với --create-notebook)'},
         {"flags": ['--create-notebook'], "dest": 'create_notebook', "action": 'store_true', "help": 'tạo notebook NLM MỚI (điều-kiện-kép nới có kiểm soát — cần --confirm yes khi --apply; journaled + readback notebook_get)'},
         {"flags": ['--confirm'], "choices": ['yes'], "help": 'bắt buộc khi --apply --create-notebook'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-from-nlm', "handler": 'cmd_profile_from_nlm',
     "help": '(v1.34.26, Q4) BIẾN NOTEBOOK NLM THÀNH PROFILE: folder riêng (mặc định tạo dưới Van_ban_thuong) + registry/manifest/marker/config own+own; seed row từ nguồn notebook (có file Drive → ref; còn lại → nlm_only sentinel, materialize=pending). KHÔNG ghi đè chat config notebook. DRY mặc định',
     "args": [
         {"flags": ['--name'], "required": True, "help": 'tên profile mới'},
         {"flags": ['--notebook'], "help": 'notebookId NLM sẵn có (nguồn sự thật danh sách nguồn). Bắt buộc khi TẠO mới; --add-missing mặc định lấy từ config profile'},
         {"flags": ['--folder'], "help": 'folder Drive sẵn có làm root (mặc định: tạo mới Van_ban_thuong/<name>)'},
         {"flags": ['--add-missing'], "dest": 'add_missing', "action": 'store_true', "help": '(v1.34.30) profile ĐÃ TỒN TẠI: seed CHỈ nguồn notebook CÒN THIẾU (khóa nlm_source_id) vào registry — KHÔNG đụng marker/config/chat/system-prompt. Không cờ + folder đã có marker → ALREADY_PROFILE'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-materialize-sources', "handler": 'cmd_profile_materialize_sources',
     "help": '(v1.34.26, materialize_preferred) nâng cấp nguồn nlm-only → GDoc trong folder profile + row own (createtext + reg_upsert + xoá sentinel, tạo-trước-xoá-sau, journaled); resumable --limit, chạy lặp tới pending=0; không xuất được → materialize=blocked (Ở LẠI nlm-only hợp lệ). DRY mặc định',
     "args": [
         {"flags": ['--profile-name'], "dest": 'target_profile', "help": 'profile đích; mặc định profile active (không phải vbqppl)'},
         {"flags": ['--limit'], "type": int, "default": 10, "help": 'số nguồn xử tối đa mỗi run (resumable)'},
         {"flags": ['--retry-blocked'], "dest": 'retry_blocked', "action": 'store_true', "help": 'thử lại cả nguồn đã đánh dấu blocked'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-set-meta', "handler": 'cmd_profile_set_meta',
     "help": '(v1.34.29, ADR-0003) curate metadata MÔ TẢ của profile trên MARKER: --description/--style/--see-also/--source-policy (xoá = chuỗi rỗng) + templates mẫu trình bày --template-add/upload/remove (v1.34.71 — 1 op/lần, probe fail-closed); ghi marker journaled+readback+trash-bản-cũ, KHÔNG đụng config. DRY mặc định',
     "args": [
         {"flags": ['--profile-name'], "dest": 'target_profile', "help": 'profile đích; mặc định profile active (không phải vbqppl)'},
         {"flags": ['--description'], "help": 'mô tả phạm vi profile (hiện trong Instruction Block)'},
         {"flags": ['--style'], "help": 'văn phong trả lời riêng của profile'},
         {"flags": ['--see-also'], "dest": 'see_also', "help": 'danh sách profile liên quan, phẩy-cách (relations.see_also — chỉ MÔ TẢ, không mở scope)'},
         {"flags": ['--source-policy'], "dest": 'source_policy', "choices": ['materialize_preferred', 'nlm_only'], "help": 'chính sách nguồn nlm-only của profile'},
         {"flags": ['--template-add'], "dest": 'template_add',
          "help": '(v1.34.71 Q3) thêm THAM CHIẾU mẫu trình bày: id slug — BẮT BUỘC kèm --template-drive-id; probe Drive bắt buộc khi --apply (fail-closed); vị trí không-WARN = cây profile hoặc kho chung _meta/templates VBQPPL'},
         {"flags": ['--template-upload'], "dest": 'template_upload',
          "help": '(v1.34.71 Q2c) upload file mẫu local (.docx, ≤35MB) vào _meta/templates/ của profile (resolvefolder find-or-create) rồi TỰ add entry (id = slug tên file); trùng tên file trong folder → TEMPLATE_FILE_NAME_EXISTS'},
         {"flags": ['--template-remove'], "dest": 'template_remove', "help": '(v1.34.71) gỡ entry mẫu theo id'},
         {"flags": ['--template-drive-id'], "dest": 'template_drive_id', "help": 'drive_id file mẫu (dùng với --template-add)'},
         {"flags": ['--template-name'], "dest": 'template_name', "help": 'tên hiển thị mẫu (mặc định = id/tên file)'},
         {"flags": ['--template-scope'], "dest": 'template_scope', "help": 'vế điều kiện "CHỈ KHI …" — khi nào dùng mẫu (hiện trong Instruction Block)'},
         {"flags": ['--template-note'], "dest": 'template_note', "help": 'ghi chú thêm cho mẫu'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-load', "handler": 'cmd_profile_load',
     "help": '(v1.34.24, ADR-0003) "dùng profile X trong PHIÊN": xuất Instruction Block thống nhất mọi env (rẽ --target session|project); đọc marker best-effort, KHÔNG ghi config/marker (đổi mặc định máy = profile-use --apply)',
     "args": [
         {"dest": 'name'},
         {"flags": ['--target'], "choices": ['session', 'project'], "default": 'session', "help": 'session = doctrine phiên; project = khối dán Claude Project Instruction'},
         {"flags": ['--offline'], "action": 'store_true', "help": 'không thử đọc marker LIVE — sinh block thuần từ config'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-use', "handler": 'cmd_profile_use',
     "help": 'chọn profile làm chế độ làm việc mặc định trong config (DRY mặc định); --apply in kèm Instruction Block phiên (v1.34.24)',
     "args": [
         {"dest": 'name'},
         {"flags": ['--apply'], "action": 'store_true', "help": 'ghi defaultProfile vào config'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-rename', "handler": 'cmd_profile_rename',
     "help": 'đổi tên profile trong config; --rename-assets đổi tên folder/manifest/registry Drive',
     "args": [
         {"dest": 'old'},
         {"dest": 'new'},
         {"flags": ['--force'], "action": 'store_true', "help": 'cho phép merge nếu profile đích đã tồn tại'},
         {"flags": ['--rename-assets'], "dest": 'rename_assets', "action": 'store_true', "help": 'đổi tên root folder + manifest/registry trên Drive'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-delete', "handler": 'cmd_profile_delete',
     "help": 'xóa profile khỏi config; NLM/Drive chỉ xử lý khi có cờ riêng (DRY mặc định)',
     "args": [
         {"dest": 'name'},
         {"flags": ['--delete-nlm-sources'], "dest": 'delete_nlm_sources', "action": 'store_true', "help": 'xóa mọi nguồn NLM trong manifest profile'},
         {"flags": ['--trash-assets'], "dest": 'trash_assets', "action": 'store_true', "help": 'đưa root/_meta/registry/manifest của profile vào trash Drive'},
         {"flags": ['--refresh'], "action": 'store_true', "help": 'refresh manifest profile trước khi lập danh sách NLM'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--confirm'], "choices": ['yes'], "help": 'bắt buộc khi --apply'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-manifest', "handler": 'cmd_profile_manifest',
     "help": 'load/export manifest của profile đang chọn',
     "args": [
         {"flags": ['--profile-name'], "dest": 'target_profile', "help": 'profile cần đọc; mặc định global --profile/defaultProfile'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--out'], "help": 'ghi manifest JSON ra file'},
         {"flags": ['--json'], "action": 'store_true', "help": 'in toàn bộ manifest thay vì summary'},
     ]},
    {"name": 'profile-adopt', "handler": 'cmd_profile_adopt',
     "help": '(v1.30.0) SEED profile ĐÃ CÓ hạ tầng Drive vào config (khác profile-create=dựng mới); dò registry/manifest trong folder+_meta, guard Doc-legacy/mime/schema; DRY mặc định',
     "args": [
         {"flags": ['--name'], "required": True, "help": 'tên profile ghi vào config.profiles'},
         {"flags": ['--folder'], "required": True, "help": 'folder id của profile (thư mục con Van_ban_thuong)'},
         {"flags": ['--notebook'], "help": 'notebookId NLM (mặc định: đọc từ manifest JSON nếu có)'},
         {"flags": ['--registry'], "help": 'override registryDocId (vd asset lạc gốc từ --discover)'},
         {"flags": ['--manifest'], "help": 'override manifestId'},
         {"flags": ['--bootstrap-manifest'], "dest": 'bootstrap_manifest', "action": 'store_true', "help": 'thiếu manifest → sinh mới tra_luat_manifest.<slug>.json + manifest_export bootstrap'},
         {"flags": ['--apply'], "action": 'store_true', "help": 'verify schema registry rồi GHI config.profiles (journaled)'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-doctor', "handler": 'cmd_profile_doctor',
     "help": '(v1.30.0) kiểm BẤT BIẾN LAYOUT (registry+manifest trong thư mục profile) + hạ tầng (legacy-Doc/mime/trashed/thiếu id); --fix --apply move asset lạc chỗ vào _meta',
     "args": [
         {"flags": ['--profile-name'], "dest": 'target_profile', "help": 'chỉ kiểm 1 profile; mặc định MỌI profile dự án trong config'},
         {"flags": ['--deep'], "action": 'store_true', "help": '(v1.34.26) thêm chiều Drive↔NLM↔registry: nguồn notebook không có row / nlm-only pending|blocked / sentinel sót (cần NLM auth)'},
         {"flags": ['--limit'], "type": int, "default": 0, "help": '(v1.34.30) CHỈ kiểm N profile mỗi run (0=tất cả) — cho --deep khỏi timeout khi nhiều profile; giữ scan-all mặc định; kèm resume_command khi còn dư'},
         {"flags": ['--skip'], "type": int, "default": 0, "help": '(v1.34.30) bỏ qua N profile đầu (offset resume, dùng với --limit)'},
         {"flags": ['--fix'], "action": 'store_true', "help": 'lập kế hoạch move asset lạc chỗ (cần --apply để chạy)'},
         {"flags": ['--plan-marker-migration'], "dest": 'plan_marker_migration', "action": 'store_true',
          "help": '(r184/ADR-0012) liệt kê DRY plan nâng marker v1→v2 (KHÔNG ghi — migration chạy ở R2)'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-index', "handler": 'cmd_profile_index',
     "help": '(v1.30.0) SỔ CÁI Van_ban_thuong/_PROFILES_INDEX (Sheet) — BẢN CHIẾU đọc nhanh (nguồn sự thật tồn tại/định danh = MARKER, ADR-0003); DRY in CSV; --rebuild --apply ghi Drive',
     "args": [
         {"flags": ['--rebuild'], "action": 'store_true', "help": 'xác nhận tạo Sheet mới + trash bản cũ (id Sheet ĐỔI mỗi rebuild)'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-sync', "handler": 'cmd_profile_sync',
     "help": '(v1.34.22, ADR-0003) đồng bộ MỘT CHIỀU marker Drive → config: quét Van_ban_thuong đọc _meta/tra_luat_profile.json, báo new/drift/missing; --apply ghi config theo marker (journaled+readback). KHÔNG ghi marker',
     "args": [
         {"flags": ['--profile-name'], "dest": 'target_profile', "help": 'chỉ sync 1 profile; mặc định toàn bộ marker dưới Van_ban_thuong'},
         {"flags": ['--folder-cap'], "dest": 'folder_cap', "type": int, "default": 60, "help": 'trần số thư mục con quét (mặc định 60, LOUD khi cắt)'},
         {"flags": ['--apply'], "action": 'store_true', "help": 'ghi config theo marker (thêm profile mới + sửa field drift)'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-backfill-markers', "handler": 'cmd_profile_backfill_markers',
     "help": '(v1.34.22, ADR-0003) backfill MỘT LẦN config → marker cho profile hiện hữu chưa có tra_luat_profile.json (upload+readback+trash bản cũ, journaled); --force ghi đè marker lệch theo config',
     "args": [
         {"flags": ['--profile-name'], "dest": 'target_profile', "help": 'chỉ backfill 1 profile; mặc định mọi profile dự án trong config'},
         {"flags": ['--force'], "action": 'store_true', "help": 'ghi đè marker hiện có theo config (migration có chủ đích — bình thường marker là nguồn sự thật)'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'boot', "handler": 'cmd_boot',
     "args": [
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--refresh'], "action": 'store_true', "help": 'bỏ qua cache local, tải lại manifest từ webapp'},
         {"flags": ['--max-age'], "dest": 'max_age', "type": float, "help": 'tuổi tối đa (giây) cache local còn tái dùng (mặc định 600; env TL_BOOT_TTL)'},
     ]},
    {"name": 'up', "handler": 'cmd_up',
     "help": 'BOOTSTRAP TẤT ĐỊNH 1-lệnh: config→gws cred+binary→nlm(--nlm)→manifest→readiness (idempotent)',
     "args": [
         {"flags": ['--nlm'], "action": 'store_true', "help": 'GỘP cài nlm CLI + auth (RAG); bỏ qua nếu chỉ cần tra cứu'},
         {"flags": ['--no-binary'], "dest": 'no_binary', "action": 'store_true', "help": 'chỉ nạp gws CRED (đọc), KHÔNG tải gws BINARY'},
         {"flags": ['--no-config-fetch'], "dest": 'no_config_fetch', "action": 'store_true', "help": 'KHÔNG tự curl config public khi thiếu cred'},
         {"flags": ['--refresh'], "action": 'store_true', "help": 'tải lại manifest (bỏ cache)'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'relation-check', "handler": 'cmd_relation_check',
     "help": 'soi văn bản sửa đổi/VBHN đã có nhưng registry thiếu goc/sua_doi',
     "args": [
         {"flags": ['--base'], "required": True, "help": 'số hiệu văn bản gốc, ví dụ: 06/2022/QH15'},
         {"flags": ['--subject'], "help": 'trích yếu/chủ đề, ví dụ: thi đua khen thưởng'},
         {"flags": ['--amendment'], "action": 'append', "help": 'số hiệu văn bản sửa đổi đã biết; lặp lại được hoặc ngăn cách ;/,'},
         {"flags": ['--footnote-source'], "help": 'gdocId|số hiệu VBHN gốc → lấy footnote-map làm cổng XÁC THỰC backfill (ưu tiên hơn heuristic chủ đề)'},
         {"flags": ['--footnote-file'], "help": 'file toàn văn VBHN (thay --footnote-source) để lấy footnote-map'},
         {"flags": ['--no-auto-footnote'], "dest": 'no_auto_footnote', "action": 'store_true', "help": 'TẮT tự đọc nguyên văn base để hợp nhất footnote-map (mặc định BẬT khi không có --footnote-source/-file)'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'corpus-relation-sweep', "handler": 'cmd_corpus_relation_sweep',
     "help": '(v1.34.31) BATCH relation-check toàn bộ Luật/NQ corpus → gộp "nguồn cần bổ sung" (vbhn_broken + missing_links + [--deep] amendments_missing đọc nguyên văn) + google_discovery kèm; STREAM per-doc stderr, resumable --skip, --out. READ-ONLY',
     "args": [
         {"flags": ['--loai'], "help": 'lọc theo loại, phẩy-cách (mặc định "Luật,Nghị quyết")'},
         {"flags": ['--cat'], "help": 'lọc theo mã chủ đề (prefix)'},
         {"flags": ['--deep'], "action": 'store_true', "help": 'đọc nguyên văn base mỗi VB để bắt inline_amendments (chậm); mặc định FAST registry-only'},
         {"flags": ['--limit'], "type": int, "default": 0, "help": 'số VB mỗi run (0=tất cả); kèm resume_command khi còn dư'},
         {"flags": ['--skip'], "type": int, "default": 0, "help": 'offset resume (dùng với --limit)'},
         {"flags": ['--out'], "help": 'ghi báo cáo JSON ra file'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'relation-backfill', "handler": 'cmd_relation_backfill',
     "help": 'KH1 Pha 1.5: GHI quan hệ sửa đổi relation-check tìm ra (set goc luật sửa, append sua_doi luật gốc); DRY mặc định, --apply ghi. Chỉ direct/ref-linked; subject-only → review',
     "args": [
         {"flags": ['--base'], "help": 'số hiệu văn bản gốc (vd 19/2012/QH13)'},
         {"flags": ['--subject'], "help": 'trích yếu/chủ đề thay --base'},
         {"flags": ['--apply'], "action": 'store_true', "help": 'THỰC THI ghi reg_bulk goc/sua_doi (mặc định DRY)'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": '(Pha 1+) bỏ qua precheck blocker (rủi ro)'},
     ]},
    {"name": 'vbhn-check', "handler": 'cmd_vbhn_check',
     "help": 'QT-5: dò VBHN theo trích yếu + gốc + năm; không overclaim nếu không có hit',
     "args": [
         {"dest": 'target', "nargs": '?', "help": 'tương thích runbook cũ: trích yếu HOẶC số hiệu gốc/VBHN (định tuyến tự động)'},
         {"flags": ['--sohieu'], "help": 'r179: alias mỏng của positional — số hiệu gốc/VBHN, định tuyến y hệt (tay quen --sohieu hết usage-error)'},
         {"flags": ['--subject'], "help": 'trích yếu/tên luật. ⚠ QUOTE cả cụm có dấu cách: --subject "bộ luật lao động" (KHÔNG `--subject bộ luật lao động` → shell word-split → unrecognized arguments)'},
         {"flags": ['--goc'], "help": 'số hiệu luật gốc/sửa đổi, ví dụ: 84/2015/QH13'},
         {"flags": ['--year'], "help": 'năm VBHN kỳ vọng, ví dụ: 2024'},
         {"flags": ['--scan'], "action": 'store_true', "help": 'quét collision/tên VBHN thiếu chủ đề trong manifest'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'vbhn-verify', "handler": 'cmd_vbhn_verify',
     "help": 'verify nội dung VBHN: tiêu đề + văn bản gốc + năm',
     "args": [
         {"dest": 'target', "nargs": '?', "help": 'tương thích runbook cũ: text-file, gdoc-id HOẶC số hiệu (định tuyến tự động)'},
         {"flags": ['--text-file']},
         {"flags": ['--gdoc-id']},
         {"flags": ['--sohieu']},
         {"flags": ['--expect-title']},
         {"flags": ['--expect-goc'], "action": 'append'},
         {"flags": ['--expect-year']},
         {"flags": ['--head'], "type": int, "default": 5000},
         {"flags": ['--official-required'], "action": 'store_true', "help": 'fail nếu không xác nhận được dấu hiệu nguồn chính thức/footnote VBHN'},
         {"flags": ['--source-name'], "help": 'tên file/nguồn để soi dấu hiệu official hoặc bản tự ghép'},
         {"flags": ['--allow-provisional'], "action": 'store_true', "help": 'cho phép verify bản tạm; không dùng để chốt canonical'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--sample'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'vbhn-compare', "handler": 'cmd_vbhn_compare',
     "help": 'so VBHN chính thức với bản tạm/tự ghép; soi footnote và điều trọng tâm',
     "args": [
         {"flags": ['--official-text'], "required": True},
         {"flags": ['--candidate-text'], "required": True},
         {"flags": ['--focus'], "action": 'append', "help": "ví dụ: --focus 'Điều 53'; lặp lại được"},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'status', "handler": 'cmd_status',
     "args": [
         {"dest": 'sohieu'},
         {"flags": ['--targets'], "default": ''},
         {"flags": ['--amendment'], "action": 'store_true'},
         {"flags": ['--vbhn'], "action": 'store_true'},
         {"flags": ['--strict', '--fail-on-finding'], "action": 'store_true', "help": 'rc=1 khi verdict REVIEW (mặc định rc=0: verdict ≠ lỗi lệnh, mirror xref)'},
         {"flags": ['--refresh'], "action": 'store_true', "help": 'tải lại manifest/registry trước guard offline của --amendment'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'extract', "handler": 'cmd_extract',
     "args": [
         {"flags": ['--json'], "action": 'store_true', "help": '(no-op v1.33.56 — output vốn đã JSON/verbatim; nhận để tương thích workflow cards)'},
         {"dest": 'gdoc_id', "nargs": '?', "help": 'GDoc id; có thể bỏ nếu dùng --sohieu'},
         {"flags": ['--sohieu'], "help": 'số hiệu/tên để tự chọn canonical từ manifest'},
         {"flags": ['--refresh'], "action": 'store_true', "help": 'tải lại manifest trước khi resolve --sohieu'},
         {"flags": ['--out'], "help": 'đường dẫn file text toàn văn'},
         {"flags": ['--dieu'], "type": int, "action": 'append', "help": 'lặp lại được'},
         {"flags": ['--find'], "action": 'append', "help": 'tìm chuỗi sau chuẩn hóa Unicode NFC; lặp lại được'},
         {"flags": ['--find-window'], "type": int, "default": 120, "help": 'số ký tự ngữ cảnh mỗi phía cho --find'},
         {"flags": ['--markup'], "default": 'strip', "choices": ['strip', 'mark', 'raw'],
          "help": '(r186) dự thảo CÓ markup sửa đổi: strip=loại chữ ĐÃ BỎ, giữ w:ins — MẶC ĐỊNH, bản chuẩn vào cache · mark=đánh dấu ⟦BỎ:…⟧ · raw=giữ nguyên (đối chứng). Nguồn Google Doc: tự export .docx để lấy markup; không lấy được thì CẢNH BÁO stderr. mark/raw ghi ra khoá cache RIÊNG, không đụng khoá chuẩn'},
         {"flags": ['--markup-strict'], "dest": 'markup_strict', "action": 'store_true',
          "help": '(r186) không chứng minh được đã lọc markup → KHÔNG ghi file, rc=3. File extract là nguồn nuôi corpus: thà thiếu còn hơn bơm chữ đã bỏ vào kho'},
     ]},
    {"name": 'external-ingest', "handler": 'cmd_external_ingest',
     "help": 'gate nạp nguồn web/NLM-native: research_* discovery-only, QT-3 trước NLM',
     "args": [
         {"dest": 'url'},
         {"flags": ['--format'], "default": '', "help": 'docx|doc|pdf|html|gdoc; nếu bỏ trống sẽ suy từ URL'},
         {"flags": ['--source-kind'], "default": 'unknown', "help": 'official|secondary|unknown'},
         {"flags": ['--action'], "default": 'discover', "help": 'discover|qt3_plan|research_import|source_add|nlm_direct'},
         {"flags": ['--cat']},
         {"flags": ['--folder']},
         {"flags": ['--notebook']},
         {"flags": ['--name']},
         {"flags": ['--sohieu']},
         {"flags": ['--year']},
         {"flags": ['--trichyeu']},
         {"flags": ['--no-convert'], "action": 'store_true', "help": 'khai báo ý định nạp PDF thô/không convert (sẽ bị chặn với PDF)'},
         {"flags": ['--confirm'], "default": '', "help": 'yes nếu người dùng đã duyệt riêng phương thức+đích'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'link-priority', "handler": 'cmd_link_priority',
     "help": 'xếp link tải cho người dùng; canonical vẫn official-first',
     "args": [
         {"dest": 'urls', "nargs": '+'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'slot-audit', "handler": 'cmd_slot_audit',
     "help": 'đếm slot NLM theo nlm_notebook_id; --all-shards: đếm TỪNG shard + cảnh báo near-full; chống NOTEBOOK_FULL giả',
     "args": [
         {"flags": ['--manifest']},
         {"flags": ['--notebook-id']},
         {"flags": ['--all-shards'], "dest": 'all_shards', "action": 'store_true', "help": 'II.5: đếm slot theo TỪNG shard (base+overflow) + cảnh báo shard ≥ngưỡng'},
         {"flags": ['--near-full'], "dest": 'near_full', "type": int, "help": 'ngưỡng cảnh báo near-full (mặc định 270/300)'},
         {"flags": ['--base-notebook-id'], "help": 'notebook nền để quy dòng rỗng nlm_notebook_id (mặc định VBQPPL)'},
         {"flags": ['--physical'], "type": int, "help": 'WS1: sức chứa VẬT LÝ từ `tl nlm-get` (nlm notebook get; neo ground-truth); đối soát với registry'},
         {"flags": ['--no-live'], "dest": 'no_live', "action": 'store_true', "help": 'A3: TẮT tự lấy live_source_count từ nlm CLI (offline/không cred)'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'xref', "handler": 'cmd_xref',
     "help": 'WS2: bóc dẫn chiếu trong văn bản → giải canonical → cờ MISSING/OUTDATED/SOHIEU_MISMATCH (report-only)',
     "args": [
         {"dest": 'target', "nargs": '?', "help": 'gdocId hoặc số hiệu (resolve canonical rồi exporttext)'},
         {"flags": ['--text-file'], "dest": 'text_file', "help": 'đọc text từ file thay vì webapp'},
         {"flags": ['--strict', '--fail-on-finding'], "action": 'store_true', "help": 'rc=1 khi có MISSING/MISMATCH/TYPO (mặc định rc=0: phát hiện ≠ lỗi lệnh)'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'frontier-expand', "handler": 'cmd_frontier_expand',
     "help": 'VÒNG LẶP: trích MỌI dẫn chiếu (xref+footnote+inline) → ứng viên frontier dedup + cờ in_corpus; missing_in_corpus = đầu vào ingest-missing. <gdoc|sohieu>; --text-file offline',
     "args": [
         {"dest": 'target', "nargs": '?', "help": 'gdocId hoặc số hiệu'},
         {"flags": ['--text-file'], "dest": 'text_file', "help": 'đọc text từ file (offline)'},
         {"flags": ['--strict', '--fail-on-finding'], "action": 'store_true', "help": 'rc=1 nếu có missing_in_corpus'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'rasoat-loop', "handler": 'cmd_rasoat_loop',
     "help": 'VÒNG LẶP RÀ SOÁT KHÉP KÍN (orchestrator, report-only): SEED→frontier-expand→mở rộng đệ quy in-corpus→dedup seen→hội tụ (dry_rounds≥K). Xuất GAP + in-corpus-chưa-NLM. <gdoc|sohieu>; --text-file offline',
     "args": [
         {"dest": 'target', "nargs": '?', "help": 'base: gdocId hoặc số hiệu'},
         {"flags": ['--text-file'], "dest": 'text_file', "help": 'đọc base từ file (offline)'},
         {"flags": ['--max-iter'], "dest": 'max_iter', "type": int, "default": 12, "help": 'trần số vòng (mặc định 12)'},
         {"flags": ['--dry-rounds'], "dest": 'dry_rounds', "type": int, "default": 2, "help": 'K: số vòng liên tiếp không sinh ứng viên mới thì dừng (mặc định 2)'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    # ── r213 (v1.35.49) ĐỢT 5: hai mắt xích BẮT BUỘC của lớp điều phối mà lượt rà LIVE 26-07 phơi ra ──
    {"name": 'rasoat-merge', "handler": 'cmd_rasoat_merge',
     "help": 'PHA 4: DỒN N phiếu master/<unit>.json (khuôn §6) → MỘT bảng master mà rasoat_phuluc.py đọc thẳng được. Không mạng, không NLM',
     "args": [
         {"flags": ['--in'], "dest": 'in_dir', "required": True, "help": 'thư mục master/ (hoặc 1 file .json)'},
         {"flags": ['--out'], "help": 'file bảng master ra; mặc định <in>/../BANG_MASTER.json'},
         {"flags": ['--state'], "help": 'kèm HOÀ GIẢI state: đơn vị doing mà ĐÃ có master → done, không có → pending'},
         {"flags": ['--dry-run'], "dest": 'dry_run', "action": 'store_true', "help": 'không ghi lại --state (vẫn xuất bảng master)'},
         {"flags": ['--check'], "action": 'store_true', "help": 'r216: ĐỐI CHIẾU bảng master đang có với kết quả merge, KHÔNG ghi đè; lệch ⇒ rc=2 kèm danh sách'},
         {"flags": ['--anchor-strict'], "dest": 'anchor_strict', "action": 'store_true', "help": 'r321 (RAS-17): anchor.doc_deps[].text_hash sai khuôn sha256:<64hex> ⇒ rc=2, KHÔNG ghi. Mặc định chỉ khai so_anchor_hong'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'state-get', "handler": 'cmd_state_get',
     "help": 'READ-ONLY: đọc state rà hồ sơ từ Drive _meta/ (WRITE_PATHS_v1). rc=3 = chưa có (lượt đầu), KHÔNG phải lỗi',
     "args": [
         {"flags": ['--name'], "default": 'rasoat_state.json', "help": 'tên file trong _meta/ (danh sách đóng)'},
         {"flags": ['--folder-id'], "dest": 'folder_id', "help": 'folder _meta/; mặc định env TL_META_FOLDER_ID'},
         {"flags": ['--out'], "help": 'ghi state ra file local'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'state-put', "handler": 'cmd_state_put',
     "help": 'GHI state rà hồ sơ lên Drive _meta/ (WRITE_PATHS_v1) — KHÔNG cần người duyệt; khoá bằng danh sách tên đóng + folder _meta/ bắt buộc + --expect-claim',
     "args": [
         {"flags": ['--in'], "dest": 'in_file', "required": True, "help": 'file JSON state local để đẩy lên'},
         {"flags": ['--name'], "default": 'rasoat_state.json', "help": 'tên file trong _meta/ (danh sách đóng)'},
         {"flags": ['--folder-id'], "dest": 'folder_id', "help": 'folder _meta/; mặc định env TL_META_FOLDER_ID'},
         {"flags": ['--expect-claim'], "dest": 'expect_claim', "help": 'TỪ CHỐI ghi nếu session_claim.id trên Drive khác (single-writer §9)'},
         {"flags": ['--dry-run'], "dest": 'dry_run', "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    # ── r217 (v1.35.53): SỬA THEO ĐIỂM thay cho thay-trọn-gói (lượt rà 6: không bản nào trùm bản nào) ──
    {"name": 'doc-patch', "handler": 'cmd_doc_patch',
     "help": 'SỬA record cache theo DANH SÁCH ĐIỂM (không thay trọn gói): mỗi điểm phải khớp ĐÚNG 1 lần trong vùng đã khai. DRY mặc định; --apply --confirm yes; tự sao lưu + nhật ký undo. Không mạng',
     "args": [
         {"dest": 'sohieu', "nargs": '?', "help": 'số hiệu văn bản trong cache (vd 158/2025/NĐ-CP)'},
         {"flags": ['--diem'], "help": 'file JSON danh sách điểm: {"so_hieu":…, "diem":[{"ma","vung","tim","thay","ly_do"}]} — vung = khoi_dau|dieu:<N>|phu_luc'},
         {"flags": ['--undo'], "help": 'run_id của lượt patch cần hoàn tác (chép lại bản sao lưu; có cổng sha256)'},
         {"flags": ['--cache-dir'], "dest": 'cache_dir', "help": 'thư mục cache; mặc định env TRA_LUAT_CACHE / ~/.tra_luat_cache'},
         {"flags": ['--apply'], "action": 'store_true', "help": 'GHI thật (mặc định DRY)'},
         {"flags": ['--confirm'], "help": 'phải là `yes` khi --apply'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'footnote-map', "handler": 'cmd_footnote_map',
     "help": 'B3: bản đồ sửa đổi cấp Điều từ footnote VBHN (marker[n]↔chú thích luật sửa) + PENDING_EFFECT',
     "args": [
         {"dest": 'target', "nargs": '?', "help": 'gdocId hoặc số hiệu'},
         {"flags": ['--text-file'], "dest": 'text_file'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'cluster', "handler": 'cmd_cluster',
     "help": "E2: cụm lĩnh vực 'pháp luật về X' → số hiệu canonical (VBHN-first); bỏ trống = liệt kê",
     "args": [
         {"dest": 'query', "nargs": '?'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'rasoat-chongcheo', "handler": 'cmd_rasoat_chongcheo',
     "help": 'E1 (v1 discovery): tập liên quan của base (cụm E2 + footnote B3, TỰ đọc base VBHN) + hiện diện + PENDING + cờ OMNIBUS',
     "args": [
         {"dest": 'base', "nargs": '?'},
         {"flags": ['--text-file'], "dest": 'text_file'},
         {"flags": ['--target'], "help": 'gdocId|số hiệu của VBHN để export text → footnote pending (B3)'},
         {"flags": ['--no-auto-footnote'], "dest": 'no_auto_footnote', "action": 'store_true', "help": 'TẮT tự đọc nguyên văn base để chạy footnote-map (mặc định BẬT khi không có --target)'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'dedup-check', "handler": 'cmd_dedup_check',
     "help": 'WS1: dedup theo manifest OFFLINE + bộ danh tính/alias (thay nlm_dedup hỏng)',
     "args": [
         {"dest": 'query'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'confirm', "handler": 'cmd_confirm',
     "help": 'gán nhãn ĐÃ-RÀ-KỸ (registry.verified) sau khi ĐỌC HEADER xác minh sohieu/tiêu đề/loại/cat',
     "args": [
         {"flags": ['--drive-id'], "dest": 'drive_id', "help": '1 văn bản theo drive_id'},
         {"flags": ['--sohieu'], "help": '1 văn bản theo số hiệu (resolve canonical)'},
         {"flags": ['--cat'], "help": 'cả nhóm theo mã chủ đề NN (chưa-confirm, corpus) — giới hạn --limit'},
         {"flags": ['--all-unconfirmed'], "dest": 'all_unconfirmed', "action": 'store_true', "help": 'mọi văn bản corpus chưa confirm (giới hạn --limit)'},
         {"flags": ['--limit'], "type": int, "default": 20, "help": 'giới hạn batch --cat/--all-unconfirmed (mặc định 20; mỗi target đọc 1 header)'},
         {"flags": ['--label'], "help": 'giá trị nhãn (mặc định ngày ISO hôm nay)'},
         {"flags": ['--force'], "action": 'store_true', "help": "gán dù header MISMATCH (ghi 'verified=…|FORCED')"},
         {"flags": ['--apply'], "action": 'store_true', "help": 'GHI thật (mặc định DRY: chỉ in kế hoạch xác minh)'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": '(Pha 1+) bỏ qua precheck blocker (rủi ro)'},
     ]},
    {"name": 'header-verify', "handler": 'cmd_header_verify',
     "help": 'G2: đọc HEADER thật → đối chiếu sohieu/tiêu đề/loại/cat khớp registry (READ-ONLY, hàng loạt). Bổ trợ confirm, bắt DRIFT 775 dòng cũ.',
     "args": [
         {"flags": ['--all'], "action": 'store_true', "help": 'audit MỌI văn bản corpus (kể cả đã confirm) — giới hạn --limit'},
         {"flags": ['--sohieu'], "help": '1 văn bản theo số hiệu (resolve canonical)'},
         {"flags": ['--drive-id'], "dest": 'drive_id', "help": '1 văn bản theo drive_id'},
         {"flags": ['--cat'], "help": 'cả nhóm theo mã chủ đề NN (corpus) — giới hạn --limit'},
         {"flags": ['--limit'], "type": int, "default": 20, "help": 'giới hạn batch --all/--cat (mỗi target đọc 1 header → tốn)'},
         {"flags": ['--offset'], "type": int, "default": 0, "help": '(v1.29.4) BỎ QUA N target đầu — phân trang batch lớn (limit nhỏ + offset tăng dần, chống client-timeout)'},
         {"flags": ['--head-chars'], "dest": 'head_chars', "type": int, "default": 6000, "help": 'số ký tự đầu cho --fix-suggest trích ngày/cơ quan'},
         {"flags": ['--fix-suggest'], "dest": 'fix_suggest', "action": 'store_true', "help": 'gợi backfill: header_sohieu, cat suy tên, ngày ban hành, cơ quan'},
         {"flags": ['--strict', '--fail-on-finding'], "action": 'store_true', "help": 'rc=1 nếu có HEADER_MISMATCH'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'corpus-audit', "handler": 'cmd_corpus_audit',
     "help": '(A) ĐỌC HEADER toàn corpus → worklist SỬA xếp hạng (số hiệu/tên-trích-yếu/năm/loại/cat/ngày) + lệnh điền sẵn. PROPOSE-ONLY (KHÔNG --apply; sửa qua source-rename/vbhn-year-fix/recat). Dùng chung engine với header-verify --fix-suggest',
     "args": [
         {"flags": ['--all'], "action": 'store_true', "help": 'audit MỌI văn bản corpus — giới hạn --limit'},
         {"flags": ['--sohieu'], "help": '1 văn bản theo số hiệu'},
         {"flags": ['--sohieu-file'], "dest": 'sohieu_file', "help": "(v1.33.0) FILE danh sách số hiệu (mỗi dòng 1 số, '#' comment) — cả lô 1 PROCESS thay vì ×N lệnh rời; có checkpoint, tiếp bằng --resume"},
         {"flags": ['--resume'], "action": 'store_true', "help": '(v1.33.0/1.33.7) tiếp batch chạy dở: với --sohieu-file (checkpoint theo nội dung file) HOẶC --all (cày TRỌN pool theo trang --limit; rc=3=PARTIAL → LẶP CÙNG LỆNH tới rc=0)'},
         {"flags": ['--workers'], "type": int, "default": 1, "help": '(v1.33.8) đọc header SONG SONG N luồng (I/O-bound; prefetch theo chùm, xử tuần tự — streak/checkpoint giữ nguyên). Gợi ý 4-6; mặc định 1 = tuần tự như cũ'},
         {"flags": ['--drive-id'], "dest": 'drive_id', "help": '1 văn bản theo drive_id'},
         {"flags": ['--cat'], "help": 'cả nhóm theo mã chủ đề NN — giới hạn --limit'},
         {"flags": ['--limit'], "type": int, "default": None, "help": 'giới hạn batch (mặc định 40 cho --all/--cat; --sohieu-file mặc định CẢ LÔ — chỉ cắt khi truyền --limit, cắt LOUD). S11 v1.33.44: Cowork 45s đọc được ~15-20 header/lệnh → dùng `--all --resume --limit 15 --workers 4` lặp tới rc=0; trang 40 mặc định SẼ timeout'},
         {"flags": ['--offset'], "type": int, "default": 0, "help": "(v1.29.4) BỎ QUA N target đầu — phân trang: chạy 'limit 20' nhiều lượt với offset 0/20/40… thay 1 lượt lớn treo"},
         {"flags": ['--strict', '--fail-on-finding'], "action": 'store_true', "help": 'rc=1 nếu có đề xuất 🔴 (sai số hiệu/loại)'},
         {"flags": ['--full'], "action": 'store_true', "help": '(A3 v1.33.18) đi với --all: quét HẾT pool trong 1 lệnh (bỏ cap trang 40) NHƯNG vẫn qua checkpoint — chết giữa chừng chạy lại là nối, không mất tiến độ. Tốn header LIVE dài (~530 doc), nên kèm --workers 4-6; Cowork trần-lệnh-ngắn dùng --all --resume trang nhỏ'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--out'], "help": '(S-4 v1.33.34) ghi JSON worklist ra file atomically; tự bật JSON (đọc rows[].fix_command tách bước, né trần 30s Cowork)'},
     ]},
    {"name": 'review-queue', "handler": 'cmd_review_queue',
     "help": '(v1.33.3) 1 LỆNH gom HÀNG ĐỢI rà soát Luật: source-map offline toàn bộ Luật/Bộ luật → nhóm việc (web LƯỢT-2 ưu tiên HIGH_VELOCITY / relation-backfill / PAUSE / sạch) + qt5_queries sẵn dán cho phiên Chrome',
     "args": [
         {"flags": ['--limit'], "type": int, "default": None, "help": 'giới hạn số Luật quét (mặc định TẤT CẢ — offline, nhanh)'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--out'], "help": 'ghi JSON ra file atomically; tự bật JSON'},
     ]},
    {"name": 'ingest-route', "handler": 'cmd_ingest_route',
     "help": 'WS3: cây quyết định ĐỊNH HƯỚNG file người dùng nhập (advisory)',
     "args": [
         {"dest": 'query'},
         {"flags": ['--vbqppl'], "action": 'store_true'},
         {"flags": ['--thuong'], "action": 'store_true'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'backfill-notebook', "handler": 'cmd_backfill_notebook',
     "help": 'WS1: ghi nlm_notebook_id cho dòng thuộc 1 notebook (DRY mặc định)',
     "args": [
         {"flags": ['--notebook'], "help": 'notebookId đích (mặc định lấy từ profile)'},
         {"flags": ['--src-ids'], "dest": 'src_ids', "help": 'danh sách nlm_source_id (phẩy/space)'},
         {"flags": ['--drive-ids'], "dest": 'drive_ids', "help": 'danh sách drive_id (phẩy/space)'},
         {"flags": ['--ids-file'], "dest": 'ids_file', "help": 'file chứa id (mỗi dòng 1)'},
         {"flags": ['--by-src'], "dest": 'by_src', "action": 'store_true', "help": 'khóa theo nlm_source_id thay vì drive_id'},
         {"flags": ['--apply'], "action": 'store_true', "help": 'THỰC THI reg_bulk (mặc định DRY)'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": '(v1.29.2) BỎ QUA precheck blocker — RỦI RO, tự chịu'},
     ]},
    {"name": 'cache-snapshot', "handler": 'cmd_cache_snapshot',
     "help": 'WS5: export/import snapshot manifest_index có cổng treeHash',
     "args": [
         {"dest": 'sub', "choices": ['export', 'import']},
         {"flags": ['--out']},
         {"flags": ['--in'], "dest": 'in_file'},
         {"flags": ['--force'], "action": 'store_true', "help": 'bỏ qua cổng treeHash khi import'},
     ]},
    {"name": 'nlm-list', "handler": 'cmd_nlm_list',
     "help": 'fast-lane: liệt kê nguồn NLM qua CLI `nlm` --skip-freshness (~4s, không qua MCP timeout)',
     "args": [
         {"dest": 'notebook_id', "nargs": '?'},
         {"flags": ['--no-skip-freshness'], "action": 'store_true', "help": 'bật lại freshness (chậm)'},
         {"flags": ['--cached'], "action": 'store_true', "help": '(v1.34.58 C-#8) opt-in đọc cache TTL 10 phút (chung helper nlm-audit-physical) — mặc định vẫn list tươi'},
         {"flags": ['--max'], "type": int, "default": 15, "help": '(N5 v1.33.41) số dòng hiển thị; 0 = TẤT CẢ (đối soát thành viên)'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--out'], "help": '(N5 v1.33.41) ghi JSON đầy đủ ra file atomically; tự bật JSON'},
         {"flags": ['--no-fallback'], "dest": 'no_fallback', "action": 'store_true', "help": '(v1.34.60 ADR-5) NLM chết → GIỮ rc=2 như cũ, không phục vụ cache STALE_CACHE'},
     ]},
    {"name": 'preflight', "handler": 'cmd_preflight',
     "help": 'sharding: định tuyến nạp VBQPPL mới (nlm_preflight + overflow khi notebook đầy)',
     "args": [
         {"dest": 'query', "nargs": '?'},
         {"flags": ['--sohieu']},
         {"flags": ['--name']},
         {"flags": ['--notebook-id'], "dest": 'notebook_id', "help": 'shard chính (mặc định base VBQPPL)'},
         {"flags": ['--overflow-notebook-id'], "dest": 'overflow_notebook_id', "help": 'ghi đè overflow (mặc định từ config)'},
         {"flags": ['--drive-id'], "dest": 'drive_id'},
         {"flags": ['--md5']},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'overflow-resolve', "handler": 'cmd_overflow_resolve',
     "help": 'II.1: kiểm shard overflow SẴN CÓ + slot từng shard (MAX registry/LIVE nlm-get) trước khi nghĩ tạo notebook; cờ OVERFLOW_SHARD_EXISTS_DO_NOT_CREATE + REGISTRY_BEHIND_LIVE (advisory)',
     "args": [
         {"flags": ['--no-live'], "dest": 'no_live', "action": 'store_true', "help": 'bỏ đối chiếu LIVE nlm-get (chỉ registry — nhanh/offline)'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'ingest-missing', "handler": 'cmd_ingest_missing',
     "help": 'nạp hàng loạt corpus CHƯA trên NLM (backlog) → source_add + ghi registry; idempotent, DRY mặc định, KHÔNG tạo notebook mới (đầy→BLOCKED)',
     "args": [
         {"flags": ['--cat'], "help": 'chỉ nạp nhóm cat NN'},
         {"flags": ['--limit'], "type": int, "default": 25, "help": 'số tối đa mỗi lần (mặc định 25)'},
         {"flags": ['--apply'], "action": 'store_true', "help": 'THỰC THI source_add + ghi registry (mặc định DRY); định tuyến theo chỗ trống, KHÔNG tạo notebook'},
         {"flags": ['--allow-no-sohieu'], "dest": 'allow_no_sohieu', "action": 'store_true', "help": "(S12) NẠP CẢ dòng sohieu='' (mặc định BỎ QUA — thường là rác chưa chuẩn hoá)"},
         {"flags": ['--skip-live-check'], "dest": 'skip_live_check', "action": 'store_true', "help": '(S13) BỎ đối chiếu nguồn LIVE (mặc định --apply DỪNG nếu không liệt kê được LIVE — tránh tạo trùng cross-run)'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": '(Pha 1) BỎ QUA precheck blocker (registryDocId legacy / profile-registry rỗng) — RỦI RO clobber/ghi-mù, tự chịu'},
         {"flags": ['--refresh'], "action": 'store_true', "help": 'ép tải lại manifest (nhưng field corpus vẫn qua GAS cache ~600s — sửa corpus xong nên `manifest`+`boot --refresh` rồi đợi)'},
         {"flags": ['--retry-failed'], "dest": 'retry_failed', "action": 'store_true', "help": '(v1.29.1) THỬ LẠI cả mục đã FAIL ≥3 lần (mặc định SKIP đỡ đốt batch — soi header-verify/source-update-corpus trước)'},
         {"flags": ['--relink'], "action": 'store_true', "help": '(v1.29.1) ÉP reg_link lại cả mục ckpt ghi ĐÃ-link-verified (mặc định SKIP — GAS cache 600s hay che nlm_source_id)'},
         {"flags": ['--force-api-add'], "dest": 'force_api_add', "action": 'store_true',
          "help": '(v1.34.54 B1) ÉP add API từng file kể cả khi pending>2/cookie chết (mặc định chuyển BATCH_LINKS: in link dán tay + reconcile)'},
         {"flags": ['--no-fallback'], "dest": 'no_fallback', "action": 'store_true',
          "help": '(v1.34.60 ADR-5) NLM chết → KHÔNG tự chuyển BATCH_LINKS theo nhánh cookie-chết (fail-closed; ngưỡng pending>2 vẫn chạy như cũ)'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'ingest-inbox', "handler": 'cmd_ingest_inbox',
     "help": '(v1.34.54 B2) QUÉT folder Drive (inbox _HOP_NAP / root profile / --folder) tìm file upload-tay CHƯA có registry → per-file pipeline convert/rename/(vbqppl xếp cat)/register, KHÔNG đụng NLM (nlm-links cuối lô). DRY mặc định; profile phát hiện VBQPPL chất lượng cao → HỎI user',
     "args": [
         {"flags": ['--folder'], "help": 'folder Drive quét (mặc định: scope nền = inbox _HOP_NAP; profile = rootFolderId)'},
         {"flags": ['--limit'], "type": int, "default": 20, "help": 'trần số file xử lý mỗi lần (mặc định 20)'},
         {"flags": ['--apply'], "action": 'store_true', "help": 'THỰC THI per-file (child DRY→plan_hash→apply)'},
         {"flags": ['--confirm'], "default": '', "help": 'bắt buộc "yes" khi --apply'},
         {"flags": ['--out'], "help": 'ghi JSON ra file (atomic)'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'nlm-links', "handler": 'cmd_nlm_links',
     "help": '(v1.34.54 B1) IN DANH SÁCH LINK Drive các dòng CHƯA trên NLM để dán BATCH vào UI notebook (stdout = CHỈ link, mỗi dòng 1; chú thích ở stderr). OFFLINE cache; sau khi dán: nlm-reconcile --apply. F5 r192: --drive-ids lô cụ thể + --md-out bảng tay markdown',
     "args": [
         {"flags": ['--notebook'], "help": 'notebook đích (mặc định theo profile/scope)'},
         {"flags": ['--cat'], "help": 'lọc nhóm cat NN (scope nền)'},
         {"flags": ['--drive-ids'], "help": '(F5 r192) danh sách drive_id (phẩy) — bảng tay cho LÔ CỤ THỂ, không đòi điều kiện chưa-trên-NLM'},
         {"flags": ['--md-out'], "help": '(F5 r192) ghi BẢNG TAY markdown (link bấm-được + notebook + hẹn reconcile) ra file'},
         {"flags": ['--limit'], "type": int, "help": 'trần số link in ra'},
         {"flags": ['--refresh'], "action": 'store_true', "help": 'ép tải lại manifest trước khi liệt kê'},
         {"flags": ['--out'], "help": 'ghi JSON ra file (atomic)'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'nlm-auth-status', "handler": 'cmd_nlm_auth_status',
     "help": '(v1.34.54 C8) trạng thái phiên NLM: probe LIVE notebook_get (M1 — login --check không đủ) + tuổi cookie/ước lượng còn lại (~60 phút đời thường); --wait poll tới khi sống (sau khi login trình duyệt/nlm login)',
     "args": [
         {"dest": 'notebook_id', "nargs": '?', "help": 'notebook probe (mặc định base/profile)'},
         {"flags": ['--wait'], "action": 'store_true', "help": 'poll tới khi sống / hết timeout'},
         {"flags": ['--interval'], "type": int, "default": 20, "help": 'giây giữa 2 lần probe (mặc định 20)'},
         {"flags": ['--timeout'], "type": int, "default": 300, "help": 'tổng giây chờ tối đa khi --wait (mặc định 300)'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'nlm-audit-physical', "handler": 'cmd_nlm_audit_physical',
     "help": '(v1.34.57 B-#3) READ-ONLY đối soát VẬT LÝ↔con trỏ registry (physical-first): mặc định quét topology VBQPPL (base+overflow); 4 finding POINTER_MISMATCH/UNREGISTERED_PHYSICAL/DUP_PHYSICAL/POINTER_DEAD (+unverified_scope advisory cho pointer ngoài scope) + suggested_commands điền sẵn. Listing cache TTL 10 phút; rc=1 khi có finding',
     "args": [
         {"flags": ['--notebooks'], "help": 'csv notebook id THÊM vào scope quét'},
         {"flags": ['--all-profiles'], "dest": 'all_profiles', "action": 'store_true', "help": 'quét MỌI notebookId trong config (đắt ~90s/notebook lớn)'},
         {"flags": ['--refresh-live'], "dest": 'refresh_live', "action": 'store_true', "help": 'ép list tươi (bỏ cache TTL 10 phút)'},
         {"flags": ['--out'], "help": 'ghi JSON ra file (atomic)'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--no-fallback'], "dest": 'no_fallback', "action": 'store_true', "help": '(v1.34.61 E2) NLM chết → GIỮ NO_NOTEBOOK_LISTED rc=2 thay vì audit tiếp trên cache stale cờ UNVERIFIED_NLM_STATE'},
     ]},
    {"name": 'nlm-migrate', "handler": 'cmd_nlm_migrate',
     "help": '(v1.34.57 B-#4..#7) DI DỜI physical-first idempotent: re-plan từ VẬT LÝ đích (luôn list tươi) mỗi lần chạy — POINTER_OK / REPOINT (sid vật lý thắng, chỉ ghi registry) / ADD (>2 doc → BATCH_LINKS dán tay; --api-add ép API qua nlm-add claim+verify-then-link); KHÔNG bao giờ tự gỡ nguồn cũ (in sẵn nlm-source-remove). DRY mặc định; dán xong CHẠY LẠI đúng lệnh (harvest). (v1.34.61 E2) --apply NLM-chết → DEFERRED + resume-artifact; NLM sống lại: --from-plan chạy nốt',
     "args": [
         {"flags": ['--to'], "help": 'notebook ĐÍCH (bắt buộc trừ khi --from-plan mang sẵn trong artifact)'},
         {"flags": ['--from-plan'], "dest": 'from_plan', "nargs": '?', "const": 'auto', "help": '(v1.34.61 E2) nạp resume-artifact .tl_state/migrate_resume_<to>.json (THAM SỐ — plan vẫn re-tạo TƯƠI physical-first, không TTL); "auto" cần --to để tìm file'},
         {"flags": ['--no-fallback'], "dest": 'no_fallback', "action": 'store_true', "help": '(v1.34.61 E2) NLM chết → GIỮ LIVE_SOURCE_LIST_FAILED rc=2 (không defer/artifact/stale-plan)'},
         {"flags": ['--from'], "dest": 'from_nb', "help": 'notebook NGUỒN (để in cleanup candidates — không bắt buộc)'},
         {"flags": ['--name-contains'], "dest": 'name_contains', "help": 'bộ lọc dòng registry theo tên (chọn ĐÚNG 1 bộ lọc)'},
         {"flags": ['--cat'], "help": 'bộ lọc nhóm cat NN (chọn ĐÚNG 1 bộ lọc)'},
         {"flags": ['--drive-ids'], "dest": 'drive_ids', "help": 'file (mỗi dòng 1 id) hoặc csv drive_id (chọn ĐÚNG 1 bộ lọc)'},
         {"flags": ['--api-add'], "dest": 'api_add', "action": 'store_true', "help": 'ép nhóm ADD qua API nlm-add per-doc (mặc định >2 doc = BATCH_LINKS)'},
         {"flags": ['--limit'], "type": int, "help": 'trần số dòng xử lý'},
         {"flags": ['--apply'], "action": 'store_true', "help": 'THỰC THI (mặc định DRY re-plan)'},
         {"flags": ['--confirm'], "default": '', "help": 'bắt buộc "yes" khi --apply'},
         {"flags": ['--out'], "help": 'ghi JSON ra file (atomic)'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'nlm-source-remove', "handler": 'cmd_nlm_source_remove',
     "help": '(v1.34.56 A-#12) GỠ nguồn KHỎI notebook NLM theo source_id (batch; KHÔNG trash Drive, KHÔNG đụng dòng registry — khác source-delete). GUARD chặn sid còn con trỏ registry (POINTER_STILL_ATTACHED — tránh con trỏ treo); DRY mặc định; --apply --confirm yes; --force bỏ guard',
     "args": [
         {"dest": 'source_id', "nargs": '+', "help": 'một hoặc nhiều nlm_source_id cần gỡ (sid toàn cục — không cần notebook-id)'},
         {"flags": ['--apply'], "action": 'store_true', "help": 'THỰC THI gỡ (mặc định DRY liệt kê con trỏ)'},
         {"flags": ['--confirm'], "default": '', "help": 'bắt buộc "yes" khi --apply'},
         {"flags": ['--force'], "action": 'store_true', "help": 'gỡ CẢ sid còn con trỏ registry (rủi ro con trỏ treo — tự chịu)'},
         {"flags": ['--refresh'], "action": 'store_true', "help": 'ép tải lại manifest trước khi đối chiếu con trỏ'},
         {"flags": ['--skip-live-check'], "dest": 'skip_live_check', "action": 'store_true', "help": '(r279) BỎ chốt đo nguồn LIVE trước khi gỡ (mặc định: sid đã vắng ⇒ noop ALREADY_GONE_CONCURRENT thay vì in "deleted" khống; không liệt kê được LIVE ⇒ fail-closed)'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'nlm-orphans', "handler": 'cmd_nlm_orphans',
     "help": '1.23.2: phân loại nguồn NLM live ↔ registry → bắt STATUS_MISMATCH_LIVE (removed* nhưng nguồn sống = gắn nhãn sai) + UNREGISTERED; --fix-mismatch vá metadata DRY; --deep lấy sohieu header. Thay soi tay',
     "args": [
         {"dest": 'notebook_id', "nargs": '?', "help": 'notebook (mặc định base/profile)'},
         {"flags": ['--fix-mismatch'], "dest": 'fix_mismatch', "action": 'store_true', "help": 'in bản vá metadata DRY (corpus=true,nlm_status=pushed) cho nhóm mislabel'},
         {"flags": ['--deep'], "action": 'store_true', "help": 'đọc nội dung NLM từng mismatch → số hiệu header thật (vá cả sohieu cụt) — chậm'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'sweep', "handler": 'cmd_sweep',
     "help": 'COMPOSITE read-only: chấm sức khoẻ corpus 1 lệnh (hygiene+cat+slot+drift+vbhn-year+quarantine) + NEXT ACTIONS điền sẵn. Thay chuỗi 6 lệnh audit',
     "args": [
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--out'], "help": 'ghi JSON ra file atomically; tự bật JSON'},
         {"flags": ['--verbose'], "action": 'store_true', "help": '(v1.31.0 P1-7) in giải thích đầy đủ 2-thước-đo corpus (mặc định 1 headline server-rule + 1 dòng Δ gọn)'},
         {"flags": ['--live-nlm'], "dest": 'live_nlm', "action": 'store_true', "help": '(P0-2 v1.33.12) sweep TỰ đối soát NLM LIVE 1 lượt (nlm-reconcile read-only) — bật khi rà TOÀN corpus; mặc định offline như cũ'},
     ]},
    {"name": 'counts', "handler": 'cmd_counts',
     "help": '(v1.33.9) MỘT BẢNG mẫu số corpus trên CÙNG snapshot; thêm --live-nlm để neo slot vật lý, tránh nhầm registry_claim_nlm=ESTIMATE',
     "args": [
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--live-nlm'], "dest": 'live_nlm', "action": 'store_true', "help": 'gọi nlm-get/notebook_get LIVE để in số nguồn vật lý + remaining slot'},
         {"flags": ['--notebook-id'], "dest": 'notebook_id', "help": 'notebook để lấy live slot (mặc định profile/TL_NOTEBOOK_ID/base)'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--out'], "help": 'ghi JSON ra file atomically; tự bật JSON'},
     ]},
    {"name": 'ops-plan', "handler": 'cmd_ops_plan',
     "help": 'READ-ONLY: gom kế hoạch xử lý sau review-queue+sweep (P0/P1/P2, lệnh mẫu, confirm_required) — khỏi đọc log dài rồi suy tay',
     "args": [
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--out'], "help": 'ghi JSON ra file atomically; tự bật JSON'},
     ]},
    {"name": 'loop', "handler": 'cmd_loop',
     "help": '(Pha 3) LOOP hợp nhất có cổng-verify + hội tụ + fail-safe: detect→fix(corpus=false verified+journaled)→re-detect đến HỘI TỤ; PAUSE khi no-progress/verify-hụt/max-iter. Chỉ tầng reversible (undo được). DRY mặc định',
     "args": [
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--dry-rounds'], "dest": 'dry_rounds', "type": int, "default": 2, "help": 'số vòng CUỐI hết-việc để coi là HỘI TỤ (mặc định 2)'},
         {"flags": ['--max-iter'], "dest": 'max_iter', "type": int, "default": 8, "help": 'trần số vòng (fail-safe, mặc định 8)'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": 'bỏ qua precheck blocker (rủi ro)'},
         {"flags": ['--config'], "default": argparse.SUPPRESS},
         {"flags": ['--profile'], "default": argparse.SUPPRESS},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'consolidation-cleanup', "handler": 'cmd_consolidation_cleanup',
     "help": "Pha sau: 'có đồng thời VBHN + gốc/sửa đổi rời' → GIỮ VBHN, set THÀNH PHẦN corpus=false (reversible) khi VBHN phủ ĐÃ verify (on NLM). DRY mặc định; component còn NLM → review",
     "args": [
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": '(Pha 1+) bỏ qua precheck blocker (rủi ro)'},
     ]},
    {"name": 'ingest-analyze', "handler": 'cmd_ingest_analyze',
     "help": 'ĐỌC HEADER file → ĐỀ XUẤT tên chuẩn + cat + sohieu/loai + lệnh `ingest-local --auto-plan --apply` điền sẵn (DRY, read-only). Nhị phân .docx/.pdf: Claude đọc→lưu .txt→--text-file',
     "args": [
         {"flags": ['--file'], "help": 'đường dẫn file gốc (lấy tên+đuôi; .txt/.html đọc thẳng)'},
         {"flags": ['--text-file'], "dest": 'text_file', "help": 'file .txt Claude trích từ .docx/.pdf'},
         {"flags": ['--cat'], "help": 'ép cat (bỏ qua suy tự động)'},
         {"flags": ['--source-quality'], "dest": 'source_quality', "choices": ['auto', 'digital', 'ocr'], "default": 'auto'},
         {"flags": ['--ocr-verified'], "dest": 'ocr_verified', "action": 'store_true'},
     ]},
    {"name": 'registry-map', "handler": 'cmd_registry_map',
     "help": 'VIEW hợp nhất folder+shard+notebook của VBQPPL (base+overflow) và MỌI profile (dẫn xuất config; validate live bằng nlm-get/profile-info)',
     "args": []},
    {"name": 'cat-list', "handler": 'cmd_cat_list',
     "help": '(4) liệt kê 45 chủ đề pháp điển chính thức (references/phap_dien_45.json) + folder đã có',
     "args": [
         {"flags": ['--missing'], "action": 'store_true', "help": 'chỉ in chủ đề CHƯA có folder'},
     ]},
    {"name": 'cat-verify', "handler": 'cmd_cat_verify',
     "help": 'G3: suy cat theo NỘI DUNG (Điều 1) + ép quy_tac_ranh_gioi (read-only). <gdoc|sohieu>; --text-file để offline',
     "args": [
         {"dest": 'target', "nargs": '?'},
         {"flags": ['--text-file'], "dest": 'text_file', "help": 'đọc nội dung từ FILE (offline, khỏi gọi gws/webapp)'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--strict'], "action": 'store_true', "help": 'rc=1 nếu cat gợi ý ≠ cat hiện tại'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'source-verify', "handler": 'cmd_source_verify',
     "help": 'G1: official-first + content md5 + cờ SOURCE_DISCREPANCY; liệt kê nguồn web xếp uy tín để đối chiếu. <sohieu|gdoc>; --text-file offline',
     "args": [
         {"dest": 'target', "nargs": '?'},
         {"flags": ['--cross'], "type": int, "default": 2, "help": 'số nguồn tối thiểu cần đối chiếu (mặc định 2)'},
         {"flags": ['--text-file'], "dest": 'text_file', "help": 'đọc nội dung từ FILE (offline)'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--strict'], "action": 'store_true', "help": 'rc=1 nếu SOURCE_DISCREPANCY'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'cat-audit', "handler": 'cmd_cat_audit',
     "help": 'audit cấp 2: rà doc corpus folder ≠ chủ đề (quy tắc ranh giới + từ khóa tên) + kiểm taxonomy 45+2',
     "args": [
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--strict', '--fail-on-finding'], "action": 'store_true', "help": 'rc=1 nếu có cờ nghi sai cat / cat ngoài 45+2'},
     ]},
    {"name": 'nlm-content', "handler": 'cmd_nlm_content',
     "help": 'NLM read qua CLI: toàn văn raw 1 source (thay MCP source_get_content). NLM chết → tự đọc bản GDoc corpus theo sid→registry (lossless, cờ corpus_read; tắt: --no-fallback)',
     "args": [
         {"dest": 'source_id'},
         {"flags": ['--out']},
         {"flags": ['--dieu']},
         {"flags": ['--max'], "type": int, "default": 4000},
         {"flags": ['--no-fallback'], "dest": 'no_fallback', "action": 'store_true', "help": '(v1.34.60 ADR-5) NLM chết → GIỮ dừng rc=2 như cũ (fail-closed), không rẽ corpus'},
     ]},
    {"name": 'nlm-query', "handler": 'cmd_nlm_query',
     "help": 'NLM RAG query qua CLI (thay MCP notebook_query); verify nguyên văn sau. NLM chết → verbatim-return ≤5 văn bản corpus cho agent tự tổng hợp (KHÔNG máy sinh RAG; tắt: --no-fallback)',
     "args": [
         {"flags": ['--json'], "action": 'store_true', "help": '(no-op v1.33.56 — output vốn đã JSON/verbatim; nhận để tương thích workflow cards)'},
         {"dest": 'query'},
         {"flags": ['--notebook-id'], "dest": 'notebook_id'},
         {"flags": ['--source-id'], "dest": 'source_id', "action": 'append', "help": 'scope source_id (lặp được)'},
         {"flags": ['--strict-scope'], "dest": 'strict_scope', "action": 'store_true', "help": '(r214) rc=2 khi NLM khai dùng THIẾU nguồn so với --source-id, hoặc không khai `sources_used` để kiểm (fail-closed; mặc định chỉ CẢNH BÁO)'},
         {"flags": ['--no-fallback'], "dest": 'no_fallback', "action": 'store_true', "help": '(v1.34.60 ADR-5) NLM chết → GIỮ dừng rc=2 như cũ, không verbatim-return'},
         {"flags": ['--out'], "help": '(v1.34.60 ADR-6) ghi envelope fallback (toàn văn không cắt --max) ra file — né tràn stdout'},
         {"flags": ['--max'], "type": int, "default": 4000, "help": '(v1.34.60) trần ký tự/văn bản khi fallback in stdout (0/âm → 4000); --out bỏ trần'},
     ]},
    {"name": 'doc-text', "handler": 'cmd_doc_text',
     "help": '(v1.34.60 A1) MỘT đường đọc text mọi định dạng: GDoc→export; .docx→download+unzip word/document.xml (text THẬT, hết footgun binary); .pdf→pdftotext; cache extract_<id>.txt. --dieu cắt Điều; nền cho fallback NLM-chết',
     "args": [
         {"dest": 'file_id'},
         {"flags": ['--out'], "help": 'ghi text ra file (né tràn stdout với văn bản lớn)'},
         {"flags": ['--dieu'], "help": 'chỉ in Điều N (cắt _slice_dieu)'},
         {"flags": ['--max'], "type": int, "default": 0, "help": 'trần ký tự in stdout; 0 = toàn văn'},
         {"flags": ['--refresh'], "action": 'store_true', "help": 'bỏ qua cache extract_<id>.txt, đọc lại từ nguồn'},
         {"flags": ['--markup'], "default": 'strip', "choices": ['strip', 'mark', 'raw'],
          "help": '(r182) .docx CÓ markup sửa đổi: strip=loại chữ ĐÃ BỎ (w:del/gạch-ngang), giữ w:ins — MẶC ĐỊNH, bản chuẩn vào cache · mark=đánh dấu ⟦BỎ:…⟧ để rà dự thảo · raw=giữ nguyên (đối chứng). mark/raw KHÔNG đọc/ghi cache. (r183) nguồn Google Doc: tự export .docx để lấy được markup; không lấy được thì CẢNH BÁO stderr, không im lặng',
          },
         {"flags": ['--markup-strict'], "dest": 'markup_strict', "action": 'store_true',
          "help": '(r183) không chứng minh được đã lọc markup (nguồn Google Doc mất dấu vết / cache chưa chứng nhận) → TỪ CHỐI in văn bản, rc=3. Dùng cho pipeline thẩm tra: thà thiếu văn bản còn hơn đọc bản THÔ tưởng đã lọc'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'doc-compare', "handler": 'cmd_doc_compare',
     "help": '(v1.34.63 A2) so-cặp identity NỘI DUNG 2 văn bản: <a> <b> = drive_id | sohieu | name | LOCAL-PATH (auto-detect; local×local = pre-ingest dedup, không cần boot). Tín hiệu md5/content-hash/BoW-Jaccard/same_type/sohieu_differs → verdict IDENTICAL/NEAR/DIFFERENT. NLM-độc-lập; rc=0 mọi verdict',
     "args": [
         {"dest": 'ref_a'},
         {"dest": 'ref_b'},
         {"flags": ['--near-threshold'], "dest": 'near_threshold', "type": float, "default": 0.95, "help": 'ngưỡng Jaccard verdict NEAR (ADR-A2-3, mặc định 0.95)'},
         {"flags": ['--refresh'], "action": 'store_true', "help": 'bỏ cache extract, đọc lại text từ nguồn'},
         {"flags": ['--out'], "help": 'ghi envelope JSON ra file'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'bench', "handler": 'cmd_bench',
     "help": 'đo hiệu năng các tính năng tính-toán-trong-code (offline) trên manifest hiện có',
     "args": [
         {"flags": ['--rounds'], "type": int, "default": 3},
         {"flags": ['--query']},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'tvpl-url', "handler": 'cmd_tvpl_url',
     "help": 'dựng URL tìm TVPL + luồng auto-download docx (Claude in Chrome đã login VIP)',
     "args": [
         {"dest": 'sohieu', "nargs": '?'},
         {"flags": ['--query']},
     ]},
    {"name": 'fetch-route', "handler": 'cmd_fetch_route',
     "help": 'RESOLVE+DEDUP+kế hoạch tải official-first (ưu tiên docx>doc>pdf: TVPL/LVN→vbpl→Công báo); F9 r192: mặc định DỪNG ở link bấm-được (10b hỏi-trước), recipe tự tải cần --auto-download-approved',
     "args": [
         {"dest": 'query', "nargs": '?'},
         {"flags": ['--sohieu']},
         {"flags": ['--auto-download-approved'], "action": 'store_true',
          "help": '(F9 r192) xuất fetch_plan cho agent TỰ TẢI — CHỈ gõ sau khi người dùng đồng ý trong phiên (mặc định: link bấm-được để người dùng tự tải)'},
     ]},
    {"name": 'fetch-batch', "handler": 'cmd_fetch_batch',
     "help": 'điều phối danh sách: dedup + route + checkpoint (DRY); tải thật do agent chạy qua Chrome có throttle',
     "args": [
         {"dest": 'items', "nargs": '*'},
         {"flags": ['--file']},
         {"flags": ['--delay'], "type": int, "default": 4},
         {"flags": ['--jitter'], "type": int, "default": 2},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'fetch-links', "handler": 'cmd_fetch_links',
     "help": 'C2(b): link bấm-được TẢI XUỐNG (gated docx) + TẢI LÊN _HOP_NAP để người dùng tự làm',
     "args": [
         {"dest": 'query', "nargs": '?'},
         {"flags": ['--sohieu']},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--env'], "choices": ['code', 'cowork', 'chat'], "help": 'ép RUNTIME_ENV (C3); mặc định auto-detect, không chắc→chat'},
     ]},
    {"name": 'find-doc', "handler": 'cmd_find_doc',
     "help": 'tìm văn bản trên web = Google site: + VBHN-first (dùng chung, thay search nội bộ kém)',
     "args": [
         {"dest": 'query', "nargs": '?'},
         {"flags": ['--sohieu']},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-create', "handler": 'cmd_profile_create',
     "help": 'dựng profile văn bản thường: tạo folder trong Van_ban_thuong + sinh config snippet + Instruction (DRY mặc định)',
     "args": [
         {"flags": ['--name'], "required": True, "help": 'tên profile/dự án (cũng là tên folder mặc định)'},
         {"flags": ['--notebook', '--notebook-id'], "dest": 'notebook', "required": True, "help": 'notebookId NotebookLM của dự án'},
         {"flags": ['--folder-name'], "dest": 'folder_name', "help": 'tên folder trong Van_ban_thuong (mặc định = --name)'},
         {"flags": ['--target'], "choices": ['nlm', 'project', 'both', 'config', 'style-template'], "default": 'project'},
         {"flags": ['--apply'], "action": 'store_true', "help": 'THỰC THI tạo folder trong Van_ban_thuong (mặc định DRY)'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-file-remove', "handler": 'cmd_profile_file_remove',
     "help": 'gỡ file khỏi profile registry; tùy chọn xóa NLM và trash Drive (DRY mặc định)',
     "args": [
         {"dest": 'drive_ids', "nargs": '+'},
         {"flags": ['--profile-name'], "dest": 'target_profile', "help": 'profile cần sửa; mặc định global --profile/defaultProfile'},
         {"flags": ['--delete-nlm'], "dest": 'delete_nlm', "action": 'store_true', "help": 'xóa source NLM tương ứng'},
         {"flags": ['--trash-drive'], "dest": 'trash_drive', "action": 'store_true', "help": 'đưa GDoc/chunk tương ứng vào trash Drive'},
         {"flags": ['--keep-registry'], "dest": 'keep_registry', "action": 'store_true', "help": 'không gọi reg_delete; chỉ xóa NLM/Drive theo cờ'},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--confirm'], "choices": ['yes'], "help": 'bắt buộc khi --apply'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'ingest', "handler": 'cmd_ingest',
     "help": 'legacy adapter: file Drive nhị phân → engine ingest-local chung (DRY mặc định)',
     "args": [
         {"dest": 'fileId'},
         {"flags": ['--cat']},
         {"flags": ['--sohieu']},
         {"flags": ['--loai']},
         {"flags": ['--ten']},
         {"flags": ['--targets'], "default": ''},
         {"flags": ['--amendment'], "action": 'store_true'},
         {"flags": ['--vbhn'], "action": 'store_true'},
          {"flags": ['--check'], "action": 'store_true', "help": 'ép chạy QT-2 dù không gắn cờ amendment/vbhn'},
          {"flags": ['--apply'], "action": 'store_true', "help": 'THỰC THI (mặc định DRY)'},
          {"flags": ['--confirm'], "choices": ['yes'], "help": 'bắt buộc khi --apply'},
          {"flags": ['--expected-plan-hash'], "dest": 'expected_plan_hash',
           "help": 'SHA-256 plan_hash từ dry-run; apply từ chối nếu nguồn/tùy chọn đã đổi'},
          {"flags": ['--json'], "action": 'store_true'},
      ]},
    {"name": 'manifest', "handler": 'cmd_manifest',
     "args": [
         {"flags": ['--touched-drive'], "dest": 'touched_drive', "action": 'store_true'},
         {"flags": ['--manifest-scope'], "choices": ['own', 'inherited'], "help": 'phạm vi regen2; mặc định own cho profile khác vbqppl'},
         {"flags": ['--confirm'], "choices": ['yes'], "help": 'xác nhận --touched-drive trên profile categories=inherit'},
         {"flags": ['--confirm-blowup'], "choices": ['yes'], "help": 'cho phép ghi dù guard PROFILE_MANIFEST_SCOPE_BLOWUP phát hiện tăng đột biến'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-rebuild-registry', "handler": 'cmd_profile_rebuild_registry',
     "help": 'phục hồi registry profile: giữ file trong rootFolderId + notebook + row_kind=ref',
     "args": [
         {"flags": ['--keep-notebook'], "dest": 'keep_notebook', "help": 'notebookId cần giữ (mặc định lấy từ profile config)'},
         {"flags": ['--apply'], "action": 'store_true', "help": 'thực thi reg_delete; mặc định DRY'},
         {"flags": ['--confirm'], "choices": ['yes'], "help": 'bắt buộc cùng --apply'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'vbhn-normalize', "handler": 'cmd_vbhn_normalize',
     "help": 'report-only: đề xuất chuẩn hóa số hiệu/tên/năm VBHN và liệt kê ghost NLM',
     "args": [
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--limit'], "type": int, "default": 50},
     ]},
    {"name": 'registry-doctor', "handler": 'cmd_registry_doctor',
     "help": 'phát hiện duplicate/orphan/root rows trong manifest; không mutate Drive',
     "args": [
         {"flags": ['--manifest']},
         {"flags": ['--json'], "action": 'store_true'},
         {"flags": ['--limit'], "type": int, "default": 20},
     ]},
    {"name": 'the-thuc-check', "handler": 'cmd_the_thuc_check',
     "help": 'READ-ONLY offline: kiểm THỂ THỨC file .docx (T1: khổ giấy/lề/font/cỡ chữ + phân luồng hệ) '
             'theo 4+1 hệ — hanh-chinh NĐ30/2020 | vbqppl NĐ78+PL I NĐ187/2025 | vbqppl-qh NQ351/2017 '
             '(QH/UBTVQH/CTN — vẫn hiệu lực) | vbhn NĐ250/2026 | dang QĐ399+HD05; căn cứ nguyên văn: '
             'references/THE_THUC_TRINH_BAY.md (R2 v1.34.75)',
     "args": [
         {"dest": 'docx_path', "metavar": 'docx', "help": 'đường dẫn file .docx cần kiểm (local, offline)'},
         {"flags": ['--he'], "choices": ['auto', 'hanh-chinh', 'vbqppl', 'vbqppl-qh', 'vbhn', 'dang'],
          "default": 'auto', "help": 'ép hệ tiêu chí; auto = phân luồng theo nội dung'},
         {"flags": ['--strict'], "action": 'store_true', "help": 'nâng WARN thành FAIL (rc=2)'},
         {"flags": ['--json'], "action": 'store_true', "help": 'envelope JSON (mặc định đã in JSON)'},
         {"flags": ['--out'], "help": 'ghi envelope JSON ra file'},
     ]},
    {"name": 'the-thuc-normalize', "handler": 'cmd_the_thuc_normalize',
     "help": 'chuẩn hoá KHUNG mẫu docx (ghi file OUT local): sectPr portrait → A4 + lề 20/20/30/15mm '
             '(bộ thoả cả 3 hệ), docDefaults → Times New Roman + cỡ theo hệ (nhà nước 13pt/Đảng 14pt), '
             'Normal bỏ font/sz đè; KHÔNG đụng run-level; landscape giữ nguyên; self-gate '
             'the-thuc-check hết FAIL T1 (R4 v1.34.78 — bước bắt buộc trước khi seed mẫu kho chung)',
     "args": [
         {"dest": 'in_docx', "metavar": 'in', "help": 'file .docx nguồn (không bị sửa)'},
         {"dest": 'out_docx', "metavar": 'out', "help": 'file .docx output (ghi đè nếu tồn tại; phải khác in)'},
         {"flags": ['--he'], "choices": ['auto', 'hanh-chinh', 'vbqppl', 'vbqppl-qh', 'vbhn', 'dang', 'nha-nuoc'],
          "default": 'auto',
          "help": 'hệ cỡ chữ mặc định (r141 đồng bộ the-thuc-check): dang|vbqppl-qh → 14pt, còn lại 13pt; '
                  'auto = detect 5 hệ theo nội dung; nha-nuoc = alias cũ (13pt, self-check auto)'},
         {"flags": ['--json'], "action": 'store_true', "help": 'envelope JSON (mặc định đã in JSON)'},
     ]},
    {"name": 'the-thuc-build', "handler": 'cmd_the_thuc_build',
     "help": 'DỰNG .docx ĐÚNG THỂ THỨC từ spec JSON (r145 v1.34.84 — đúc kết thực chiến): bề rộng bảng '
             'tính từ lề (không tràn), độ dài gạch theo công thức, hai ô tiêu đề đối xứng ⇒ gạch ngang '
             'nhau, viền nil đủ 4 cạnh, khoảng ký ≥5 dòng; hệ hanh-chinh (NĐ30) | dang (QĐ399+HD05) | '
             'vbqppl-qh (NQ 351/2017 — 19 mẫu Phụ lục I: Tiêu ngữ 14, không gạch dưới tên gọi, '
             'căn cứ nghiêng, kẻ ngang trước dòng thông qua); '
             'tự self-check bằng the-thuc-check',
     "args": [
         {"flags": ['--spec'], "required": True, "help": 'file JSON: he, chu_quan, ten_cq, so_kh, dia_danh, ten_loai, trich_yeu, body[], noi_nhan[], quyen_han, chuc_vu, ho_ten, le{}, dong_trong_ky; riêng vbqppl-qh thêm: co_quan_ban_hanh, can_cu[], tu_lenh, thong_qua, body[].kieu="giua"; khe trước khối ký dem_ky_pt (mặc định 24pt); mau="phieu_trinh" ⇒ dựng PHIẾU TRÌNH (chu_quan, kinh_gui, noi_dung, qua_trinh[], de_xuat[], ky_trai[], y_kien_phai[], tong_hop[])'},
         {"flags": ['--out'], "required": True, "help": 'đường dẫn .docx output'},
         {"flags": ['--he'], "choices": ['auto', 'hanh-chinh', 'vbqppl-qh', 'dang'], "default": 'auto',
          "help": 'ép hệ (mặc định lấy từ spec.he)'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
]


def register_generated(sub, tl_module) -> list[str]:
    """Sinh parser cho GENERATED_SPECS; handler resolve từ tl_module (stub ủy quyền). Trả list tên đã sinh."""
    made = []
    for spec in GENERATED_SPECS:
        p = sub.add_parser(spec["name"], **({"help": spec["help"]} if spec.get("help") else {}))
        for a in spec["args"]:
            kw = {k: v for k, v in a.items() if k not in ("flags", "dest")}
            if a.get("flags"):
                if "dest" in a:      # I7 wave-2: cờ có dest= tường minh (vd --in dest=in_file) — PHẢI truyền xuống
                    kw["dest"] = a["dest"]
                p.add_argument(*a["flags"], **kw)
            else:
                p.add_argument(a["dest"], **kw)
        p.set_defaults(fn=getattr(tl_module, spec["handler"]))
        made.append(spec["name"])
    return made


# ───── r310 (RAS-01 vế metadata/CLI · RAS-14): `rasoat <sub>` là LỆNH THẬT, hết argparse.REMAINDER ─────
# BỆNH. `rasoat` khai đúng hai thứ: một positional `sub` và `rest=argparse.REMAINDER`. REMAINDER nuốt TRỌN
# phần đuôi dòng lệnh, nên:
#   (a) KHÔNG cờ nào của `rasoat` được KHAI ⇒ ba đường GHI (`keywords`/`titles`/`orchestrate` — cả ba đều
#       `reg_bulk`/`changes_pull` vào registry THẬT) vô hình với `tool-inventory` và `workflow-audit
#       --strict`: không meta, không cổng, không ai đối chiếu. Cổng WRITE_CMD_NO_GATE chỉ soi được cái nó
#       NHÌN THẤY, và nó không nhìn thấy gì ở đây.
#   (b) RAS-14: `--profile` gõ SAU sub bị đẩy NGUYÊN cho script con. `backfill_nlm_title.py` có `--profile`
#       RIÊNG (profile của **nlm CLI**, không phải corpus profile của tl) ⇒ `tl rasoat titles --profile
#       "Luật BHXH"` âm thầm ĐỔI NGHĨA: corpus profile của tl KHÔNG được áp (scope rơi về vbqppl nền), còn
#       script con nhận nhầm tên hồ sơ làm profile nlm. Hai lỗi cùng một dòng REMAINDER.
# VÁ. Mỗi sub là một subparser khai ĐỦ cờ; cờ script con được ÁNH XẠ TƯỜNG MINH bằng khoá `child`
# (`child=None` = cờ chỉ sống ở tầng tl, KHÔNG chuyển xuống). `--profile` nay thuộc về tl (áp offline
# TRƯỚC dispatch); profile của nlm CLI đổi tên thành `--nlm-profile` nên hai nghĩa hết chồng lên nhau.
# Đường GHI đòi `--apply` TƯỜNG MINH; thiếu `--apply` ⇒ tl bơm `dry_flag` của script con (fail-CLOSED:
# script không có chế độ DRY thì TỪ CHỐI chạy, xem `cmd_rasoat`).
RASOAT_SPECS = [
    {"name": "keywords", "script": "backfill_keywords_live.py", "writes": "registry", "dry_flag": "--dry",
     "help": "backfill cột `tukhoa` cho doc trên NLM (reg_bulk) — GHI registry, đòi --apply",
     "args": [
         {"flags": ["--manifest"], "child": "--manifest", "help": "tra_luat_manifest.json"},
         {"flags": ["--budget"], "child": "--budget", "type": int, "help": "ngân sách giây/đợt (mặc định script con: 200)"},
         {"flags": ["--batch"], "child": "--batch", "type": int, "help": "vá reg_bulk mỗi N doc (mặc định script con: 40)"},
         {"flags": ["--all"], "child": "--all", "action": "store_true", "help": "cả doc chưa lên NLM (mặc định chỉ NLM)"},
         {"flags": ["--progress"], "child": "--progress", "help": "file checkpoint tiến độ"},
         {"flags": ["--apply"], "child": None, "action": "store_true",
          "help": "GHI THẬT vào registry; thiếu cờ này = chạy DRY (script con nhận --dry)"},
     ]},
    {"name": "titles", "script": "backfill_nlm_title.py", "writes": "registry", "dry_flag": "--dry",
     "help": "đồng bộ nlm_title (+describe) vào registry bằng 1 call reg_bulk — GHI registry, đòi --apply",
     "args": [
         {"flags": ["--from-nlm"], "child": "--from-nlm", "help": "notebook_id — lấy nguồn qua nlm CLI"},
         {"flags": ["--nlm-json"], "child": "--nlm-json", "help": "dump MCP/JSON [{id,title,desc?,keywords?}]"},
         {"flags": ["--manifest"], "child": "--manifest", "help": "tra_luat_manifest.json (thay thế)"},
         {"flags": ["--all-sources"], "child": "--all-sources", "action": "store_true", "help": "--from-nlm: mọi nguồn"},
         {"flags": ["--with-describe"], "child": "--with-describe", "action": "store_true"},
         {"flags": ["--desc-col"], "child": "--desc-col", "help": "cột registry để vá describe (phải tồn tại sẵn)"},
         {"flags": ["--source-ids"], "child": "--source-ids", "help": "giới hạn describe theo id (phân tách dấu phẩy)"},
         {"flags": ["--limit"], "child": "--limit", "type": int, "help": "giới hạn số nguồn describe"},
         {"flags": ["--cols"], "child": "--cols", "help": "cột registry cần vá (mặc định script con: nlm_title)"},
         {"flags": ["--nlm-bin"], "child": "--nlm-bin"},
         {"flags": ["--docker"], "child": "--docker"},
         # RAS-14: KHÔNG để tên `--profile` — nó là profile của **nlm CLI**, còn `--profile` của tl là
         # corpus profile. Trùng tên = trùng nghĩa, và REMAINDER cũ khiến hai nghĩa đó ĐỔI CHỖ im lặng.
         {"flags": ["--nlm-profile"], "child": "--profile",
          "help": "profile của **nlm CLI** (KHÁC `--profile` corpus của tl — RAS-14)"},
         {"flags": ["--cmd-list"], "child": "--cmd-list"},
         {"flags": ["--cmd-describe"], "child": "--cmd-describe"},
         {"flags": ["--timeout"], "child": "--timeout", "type": int},
         {"flags": ["--export"], "child": "--export", "action": "store_true", "help": "manifest_export sau backfill"},
         {"flags": ["--apply"], "child": None, "action": "store_true",
          "help": "GHI THẬT vào registry; thiếu cờ này = chạy DRY (script con nhận --dry)"},
     ]},
    {"name": "orchestrate", "script": "registry_orchestrator.py", "writes": "registry", "dry_flag": "--dry",
     "help": "bộ điều phối sổ cái theo THỜI ĐIỂM (boot/end) — GHI registry, đòi --apply",
     "args": [
         {"dest": "phase", "nargs": "?", "choices": ["boot", "end"], "default": "boot", "child_positional": True},
         {"flags": ["--manifest"], "child": "--manifest"},
         {"flags": ["--regen-threshold"], "child": "--regen-threshold", "type": int},
         {"flags": ["--bulk-threshold"], "child": "--bulk-threshold", "type": int},
         {"flags": ["--tukhoa-threshold"], "child": "--tukhoa-threshold", "type": int},
         {"flags": ["--touched-drive"], "child": "--touched-drive", "action": "store_true"},
         {"flags": ["--min-version"], "child": "--min-version"},
         # KHÔNG đặt tên `--selftest`: root parser của tl đã có `--selftest` và main() đọc `a.selftest`
         # TRƯỚC dispatch ⇒ trùng tên sẽ chạy selftest của TL thay vì của script con.
         {"flags": ["--orchestrator-selftest"], "child": "--selftest", "action": "store_true",
          "help": "chạy selftest của registry_orchestrator.py (22/22, offline)"},
         {"flags": ["--apply"], "child": "--apply", "action": "store_true",
          "help": "GHI THẬT; thiếu cờ này = chạy DRY (script con nhận --dry)"},
     ]},
    {"name": "worksheet", "script": "rasoat_worksheet.py", "writes": None, "dry_flag": None,
     "help": "dựng worksheet rà soát từ cache cấu trúc — chỉ ghi file cục bộ trong --out-dir",
     "args": [
         {"dest": "target", "nargs": "?", "metavar": "so-hieu", "fills": "so_hieu",
          "help": "số hiệu canonical (tương đương --so-hieu)"},
         {"flags": ["--so-hieu", "--sohieu", "--so_hieu"], "dest": "so_hieu", "child": "--so-hieu"},
         {"flags": ["--variant"], "child": "--variant"},
         {"flags": ["--cache-dir"], "child": "--cache-dir"},
         {"flags": ["--out-dir"], "child": "--out-dir"},
         {"flags": ["--title"], "child": "--title"},
         # Cờ này VỐN đã được `cmd_rasoat` đọc (`getattr(a, "no_auto_cache", False)`) nhưng CHƯA TỪNG được
         # khai ở đâu — REMAINDER nuốt mất nên nó luôn False. Nay khai thật ở tầng tl (không chuyển xuống).
         {"flags": ["--no-auto-cache"], "child": None, "action": "store_true",
          "help": "TẮT tự dựng cache khi thiếu docs/<sh>--<variant>.json"},
     ]},
    {"name": "phuluc", "script": "rasoat_phuluc.py", "writes": None, "dry_flag": None,
     "help": "dựng phụ lục rà soát từ bảng master — chỉ ghi file cục bộ trong --out-dir",
     "args": [
         {"dest": "target", "nargs": "?", "metavar": "in", "fills": "inp",
          "help": "file master.json hoặc thư mục .json (tương đương --in)"},
         {"flags": ["--in", "--file"], "dest": "inp", "child": "--in"},
         {"flags": ["--out-dir"], "child": "--out-dir"},
         {"flags": ["--title"], "child": "--title"},
     ]},
]

RASOAT_SPEC_BY_NAME = {s["name"]: s for s in RASOAT_SPECS}


def _rasoat_dest(arg: dict) -> str:
    """dest của một mục spec — tường minh, hoặc suy từ cờ ĐẦU (khuôn argparse)."""
    if arg.get("dest"):
        return arg["dest"]
    return arg["flags"][0].lstrip("-").replace("-", "_")


def register_rasoat(parent, tl_module) -> list[str]:
    """Sinh subparser THẬT cho `rasoat <sub>` từ RASOAT_SPECS. Trả list tên đã sinh.

    KHÔNG set `fn` trên parser CHA: `tl rasoat` trần phải rơi vào nhánh help của main() (rc=2), không
    được dispatch với `sub=None`."""
    rsub = parent.add_subparsers(dest="sub")
    made = []
    for spec in RASOAT_SPECS:
        p = rsub.add_parser(spec["name"], **({"help": spec["help"]} if spec.get("help") else {}))
        for a in spec["args"]:
            kw = {k: v for k, v in a.items()
                  if k not in ("flags", "dest", "child", "child_positional", "fills")}
            if a.get("flags"):
                if "dest" in a:
                    kw["dest"] = a["dest"]
                p.add_argument(*a["flags"], **kw)
            else:
                p.add_argument(a["dest"], **kw)
        p.set_defaults(fn=getattr(tl_module, "cmd_rasoat"))
        made.append(spec["name"])
    return made


def rasoat_child_argv(spec: dict, ns, *, apply_on: bool = False) -> list[str]:
    """Dựng argv cho script con TỪ NAMESPACE đã parse (thay REMAINDER).

    `child=None` ⇒ cờ chỉ sống ở tầng tl. `fills` ⇒ positional điền cho cờ chính khi cờ đó trống (giữ
    hành vi `tl rasoat worksheet 18/VBHN-VPQH` = `--so-hieu 18/VBHN-VPQH`). Thiếu `--apply` trên đường
    GHI ⇒ nối `dry_flag` của script con."""
    vals = {}
    for a in spec["args"]:
        d = _rasoat_dest(a)
        vals[d] = getattr(ns, d, a.get("default"))
    for a in spec["args"]:                       # positional → cờ chính (chỉ khi cờ chính TRỐNG)
        fills = a.get("fills")
        if not fills:
            continue
        d = _rasoat_dest(a)
        if vals.get(d) and not vals.get(fills):
            vals[fills] = vals[d]
        vals[d] = None
    head, tail = [], []
    for a in spec["args"]:
        d = _rasoat_dest(a)
        v = vals.get(d)
        if v is None or v is False or v == "":
            continue
        if a.get("child_positional"):
            head.append(str(v))
            continue
        child = a.get("child")
        if not child:
            continue
        if a.get("action") == "store_true":
            tail.append(child)
        else:
            tail += [child, str(v)]
    argv = head + tail
    if spec.get("writes") and not apply_on and spec.get("dry_flag"):
        argv.append(spec["dry_flag"])
    return argv


# ───────────────────────── E1: metadata ─────────────────────────
def _m(risk, read_only, write_scope, confirm, dry_run, det_json, task, contract, card_required, module, generated=False,
       nlm_fallback=None):
    # nlm_fallback (v1.34.60 — kế hoạch NLM-death resilience E1–E3, ADR-5): phân loại per-lệnh cho lớp
    # _nlm_or_corpus khi NLM chết: corpus_read (đường ĐỌC — nlm-content/query/cross) | defer (đường ĐẨY —
    # nlm-add/ingest-*) | stale_cache (nlm-list) | unverified (audit/reconcile — Release 2) | none (chỉ báo
    # offline, không rẽ) | None (mặc định — lệnh không dính NLM). Kwarg default → không phải sửa call cũ.
    return {"risk": risk, "read_only": read_only, "write_scope": write_scope,
            "requires_confirm": confirm, "supports_dry_run": dry_run,
            "deterministic_json_required": det_json, "workflow_task": task,
            "idempotency_contract": contract, "card_required": card_required,
            "module": module, "generated": generated, "nlm_fallback": nlm_fallback}


COMMAND_META = {
    # ── determinism-era (card_required=True — card PHẢI tồn tại) ──
    "tool-inventory":       _m("low", True, "none", False, False, True, "workflow_audit", None, True, "workflow", True),
    "route-task":           _m("low", True, "none", False, False, True, "workflow_audit", None, True, "workflow", True),
    "workflow-audit":       _m("low", True, "none", False, False, True, "workflow_audit", None, True, "workflow", True),
    "golden-test":          _m("low", False, "local", False, True, True, "workflow_audit", None, True, "workflow", True),
    # read_only=True + write_scope="local": chỉ ghi khi người gọi tự khai `--out` (khuôn live-state-snapshot)
    "doc-claims-check":     _m("low", True, "local", False, False, True, "workflow_audit", None, True, "workflow", True),
    "determinism-audit":    _m("low", True, "none", False, False, True, "workflow_audit", None, True, "release", True),
    "release-manifest":     _m("low", False, "local", False, True, True, "release_manifest", None, True, "release", True),
    "release-verify":       _m("low", True, "none", False, False, True, "release_verify", None, True, "release", True),
    "test-fragments-check": _m("low", True, "none", False, False, True, "release_verify", None, True, "release", True),
    "release-bundle":       _m("medium", False, "local", False, False, True, "release_bundle", None, True, "release", True),
    "bundle-export":        _m("low", False, "local", False, False, True, "bundle_export", None, True, "release", True),
    "release-check":        _m("medium", False, "local", False, False, True, "release_check", None, True, "release", generated=True),
    "live-readiness":       _m("medium", True, "none", False, False, True, "live_readiness", None, True, "live", generated=True),
    "live-contract-check":  _m("medium", True, "none", False, False, True, "live_contract_check", None, True, "live", generated=True),
    "live-state-snapshot":  _m("medium", True, "local", False, False, True, "live_state_snapshot", None, True, "live", generated=True),
    "live-state-diff":      _m("low", True, "none", False, False, True, "live_state_diff", None, True, "live", generated=True),
    "live-smoke-plan":      _m("low", True, "none", False, False, True, "live_smoke_plan", None, True, "live", generated=True),
    "deploy-plan":          _m("medium", True, "none", False, False, True, "deploy_plan", None, True, "live", generated=True),
    "rollback-plan":        _m("medium", True, "none", False, False, True, "rollback_plan", None, True, "live", generated=True),
    "final-acceptance":     _m("medium", True, "none", False, False, True, "final_acceptance", None, True, "live", generated=True),
    "go-live-runbook":      _m("medium", True, "none", False, False, True, "go_live_runbook", None, True, "live", generated=True),
    "ingest-zip":           _m("high", False, "drive_registry_nlm", True, True, True, "ingest_zip", "ingest_zip", True, "zip_ingest", generated=True),
    "profile-ingest-zip":   _m("high", False, "drive_registry_nlm", True, True, True, "ingest_zip", "ingest_zip", True, "zip_ingest", generated=True),
    "ocr-analyze":          _m("low", True, "none", False, False, True, "ocr_pdf_scan", None, True, "ocr", generated=True),
    "ocr-run":              _m("medium", False, "local", False, True, True, "ocr_pdf_scan", None, True, "ocr", generated=True),
    "ocr-verify":           _m("low", True, "none", False, False, True, "ocr_pdf_scan", None, True, "ocr", generated=True),
    "ingest-ocr":           _m("high", False, "drive_registry_nlm", True, True, True, "ocr_ingest", "ocr_ingest", True, "ocr", generated=True),
    "profile-ingest-ocr":   _m("high", False, "drive_registry_nlm", True, True, True, "ocr_ingest", "profile_ingest_ocr", True, "ocr", generated=True),
    "chunk-plan":           _m("low", True, "none", False, False, True, "large_doc_chunk", None, True, "chunking", generated=True),
    "chunk-apply":          _m("medium", False, "local", False, True, True, "large_doc_chunk", None, True, "chunking", generated=True),
    "chunk-verify":         _m("low", True, "none", False, False, True, "chunk_ingest", None, True, "chunking", generated=True),
    "profile-ingest-chunks": _m("high", False, "drive_registry_nlm", True, True, True, "chunk_ingest", "profile_ingest_chunks", True, "chunking", generated=True),
    "convert-verify":       _m("low", True, "none", False, False, True, "convert_rename", None, True, None, generated=True),
    "nlm-query-plan":       _m("low", True, "none", False, False, True, "nlm_query_quality", None, True, None, generated=True),
    # ── legacy write high-risk (card_required=False trừ khi card đã có; gate = --apply dry-run;
    #    v1.34.1: HẾT grandfather contract — mọi lệnh high-risk ghi đều có idempotency_contract) ──
    "ingest-local":         _m("high", False, "drive_registry_nlm", True, True, False, "ingest_local", "ingest_local", True, None, nlm_fallback="defer"),
    "profile-ingest":       _m("high", False, "drive_registry_nlm", True, True, False, "ingest_local", "profile_ingest", True, None, nlm_fallback="defer"),
    "nlm-add":              dict(_m("high", False, "nlm", False, False, False, None, "nlm_add", False, None, nlm_fallback="defer"),
                                 builtin_gate="nlm_dedup_live_gate"),
    "recat":                _m("high", False, "drive_registry", False, True, False, None, "recat", False, None, generated=True),
    "source-rename":        _m("high", False, "drive_registry_nlm", False, True, False, None, "source_rename", False, None, generated=True),
    "source-delete":        _m("high", False, "drive_registry_nlm", True, False, False, None, "source_delete", False, None, generated=True),
    "source-update-corpus": _m("high", False, "registry_nlm", True, True, False, None, "source_update_corpus", False, None, generated=True),
    "verify-staged":        _m("high", False, "registry", True, True, False, None, "verify_staged", False, None, generated=True),   # r200 staged lane grill 24-07

    "dedup-plan":           _m("high", False, "registry_nlm", False, True, False, None, "dedup_plan", False, None, generated=True),
    "dedup-corpus":         _m("high", False, "drive_registry_nlm", True, True, False, None, "dedup_corpus", False, "hygiene", generated=True, nlm_fallback="none"),   # v1.34.63 B1 (trục NỘI DUNG; apply ủy quyền source-update-corpus/source-delete; ghi → none)
    "register":             _m("high", False, "registry", False, True, False, None, "register", False, None),
    "backfill-loai":        _m("medium", False, "registry", False, True, False, None, None, False, None, generated=True),
    "backfill-title-vn":    _m("medium", False, "registry", False, True, False, None, None, False, None, generated=True),
    "backfill-hieuluc":     _m("medium", False, "registry", False, True, False, None, None, False, None, generated=True),
    "backfill-nlm-status":  _m("medium", False, "registry", False, True, False, None, None, False, "nlm_ops", generated=True),   # r179 ADR-0010: nắn added→pushed, live→active (một lần, journaled)
    "drive-push":           dict(_m("high", False, "drive", False, False, False, None, "drive_push", False, None),
                                 builtin_gate="md5_verify_fixed_fileid"),
    "reg-delete":           _m("high", False, "registry", True, False, False, None, "reg_delete", False, None, generated=True),
    "vbhn-year-fix":        _m("medium", False, "registry", False, True, False, None, None, False, None, generated=True),
    "quarantine-fix":       _m("medium", False, "registry", False, True, False, None, None, False, None, generated=True),
    "shared-source-fix":    _m("high", False, "registry_nlm", True, True, False, None, "shared_source_fix", False, None, generated=True),
    "corpus-fix":           _m("medium", False, "registry", False, True, False, None, None, False, None, generated=True),
    "push-overflow":        _m("high", False, "nlm_registry", False, True, False, None, "push_overflow", False, None, generated=True),
    "nlm-reconcile":        _m("high", False, "registry_nlm", False, True, False, None, "nlm_reconcile", False, None, nlm_fallback="unverified"),   # v1.34.61 E2: --apply NLM-chết → DEFER trỏ artifact A3 (DRY giữ rc=2 — verify-tool cần live)
    "nlm-links":            _m("low", True, "none", False, False, False, None, None, False, "nlm_ops", generated=True),   # v1.34.54 B1 read-only
    "ingest-inbox":         _m("high", False, "drive_registry", True, True, False, None, "ingest_inbox", False, "ingest_ops", generated=True),   # v1.34.54 B2 (KHÔNG đụng NLM — nlm-links cuối lô)
    "nlm-auth-status":      _m("low", True, "none", False, False, False, None, None, False, "nlm_ops", generated=True),   # v1.34.54 C8 read-only (probe live, không ghi)
    "nlm-source-remove":    _m("high", False, "nlm", True, True, False, None, "nlm_source_remove", False, "nlm_ops", generated=True, nlm_fallback="none"),   # v1.34.56 A-#12 (gỡ nguồn khỏi notebook — guard con trỏ; v1.34.60: offline chỉ báo, KHÔNG defer xoá)
    "nlm-audit-physical":   _m("low", True, "local", False, False, False, None, None, False, "nlm_ops", generated=True, nlm_fallback="unverified"),   # v1.34.57 B-#3 read-only; v1.34.61 E2: NLM-chết → stale-cache + cờ UNVERIFIED_NLM_STATE
    "nlm-migrate":          _m("high", False, "registry_nlm", True, True, False, None, "nlm_migrate", False, "nlm_ops", generated=True, nlm_fallback="defer"),   # v1.34.57 B-#4..#7; v1.34.61 E2: --apply NLM-chết → DEFERRED + resume-artifact --from-plan
    "nlm-cross":            _m("low", True, "none", False, False, False, None, None, False, "nlm_ops", nlm_fallback="corpus_read"),   # v1.34.60 E1 (meta mới — lệnh cũ ở cli.py chưa từng có meta)
    "doc-text":             _m("low", True, "local", False, False, False, None, None, False, "lookup_ops", generated=True),   # v1.34.60 A1 (read-only; ghi cache extract local)
    "doc-compare":          _m("low", True, "local", False, False, False, None, None, False, "doc_identity", generated=True, nlm_fallback="corpus_read"),   # v1.34.63 A2 (read-only; đọc corpus — chạy khi NLM chết; ghi cache extract local)
    "missing-sohieu":       _m("medium", False, "registry", False, True, False, None, None, False, None, generated=True),
    # ── I7 wave-2 (v1.34.11): meta BASELINE bằng-chứng-cờ cho 78 lệnh chuyển GENERATED_SPECS —
    # chính sách grilling: --apply→supports_dry_run (doctrine DRY-mặc-định), --confirm→requires_confirm,
    # ghi ngoài-repo→medium+scope đích, KHÔNG high mới (nâng high+contract = Pha-E-hoàn-thiện sau).
    "ping":                  _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "cowork-plan":           _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "perf":                  _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "init-config":           _m("low", False, "local", False, False, False, None, None, False, None, generated=True),
    "doctor":                _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "precheck":              _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "journal":               _m("low", False, "local", False, False, False, None, None, False, None, generated=True),
    "resume":                _m("medium", False, "registry", False, True, False, None, None, False, None, generated=True),
    "undo":                  _m("medium", False, "registry", True, True, False, None, None, False, None, generated=True),
    "verify-integrity":      _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "edit-skill":            _m("low", False, "local", False, True, False, None, None, False, None, generated=True),
    "profile-info":          _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "config-pin-registry":   _m("low", False, "local", False, False, False, None, None, False, None, generated=True),
    "profile-list":          _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "profile-use":           _m("low", False, "local", False, True, False, None, None, False, None, generated=True),
    "profile-rename":        _m("medium", False, "drive_local", False, True, False, None, None, False, None, generated=True),
    "profile-delete":        _m("medium", False, "drive_local", True, True, False, None, None, False, None, generated=True),
    "profile-manifest":      _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "profile-adopt":         _m("medium", False, "drive_local", False, True, False, None, None, False, None, generated=True),
    "profile-doctor":        _m("medium", False, "drive_local", False, True, False, None, None, False, None, generated=True),
    "profile-index":         _m("medium", False, "drive_local", False, True, False, None, None, False, None, generated=True),
    "profile-load":          _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    # promote = dựng hạ tầng 1-lần idempotent (họ profile-create/adopt = medium); ghi registry PROFILE MỚI rỗng,
    # notebook-create có confirm riêng. Contract thật → backlog pha siết kế (như grandfather-theo-lớp).
    "profile-promote":       _m("medium", False, "drive_registry_nlm", False, True, False, None, None, False, None, generated=True),
    "profile-from-nlm":      _m("medium", False, "drive_registry_nlm", False, True, False, None, None, False, None, generated=True),
    "profile-materialize-sources": _m("medium", False, "drive_registry", False, True, False, None, None, False, None, generated=True),
    "profile-set-meta":      _m("medium", False, "drive_local", False, True, False, None, None, False, None, generated=True),
    "profile-sync":          _m("low", False, "local", False, True, False, None, None, False, None, generated=True),
    "profile-backfill-markers": _m("medium", False, "drive_local", False, True, False, None, None, False, None, generated=True),
    "boot":                  _m("low", False, "local", False, False, False, None, None, False, None, generated=True),
    "up":                    _m("low", False, "local", False, False, False, None, None, False, None, generated=True),
    "relation-check":        _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "corpus-relation-sweep": _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "relation-backfill":     _m("medium", False, "registry", False, True, False, None, None, False, None, generated=True),
    "vbhn-check":            _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "vbhn-verify":           _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "vbhn-compare":          _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "status":                _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "extract":               _m("low", False, "local", False, False, False, None, None, False, None, generated=True),
    "external-ingest":       _m("medium", False, "drive_nlm", True, False, False, None, None, False, None, generated=True),
    "link-priority":         _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "slot-audit":            _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "xref":                  _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "frontier-expand":       _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "rasoat-loop":           _m("low", False, "local", False, False, False, None, None, False, None, generated=True),
    # r213 ĐỢT 5 — state-put GHI Drive nhưng CỐ Ý không requires_confirm: mượn cổng duyệt = bắt người
    # xen mỗi lần chốt state, phá nghiệm thu H7 (≤2 lần xen/hồ sơ). Cổng thật = builtin_gate
    # (_rasoat_state_scope fail-CLOSED: danh sách tên đóng + folder _meta/ bắt buộc) + --dry-run.
    "rasoat-merge":          _m("low", False, "local", False, True, True, "rasoat_hoso", None, True, "lookup_ops", generated=True),
    # LỚP 3 — cổng kiểm cuối Đợt: READ-ONLY, chỉ ghi khi người gọi tự khai `--out` (khuôn doc-claims-check)
    "rasoat-dot-check":      _m("low", True, "local", False, False, True, "rasoat_hoso", None, True, "rasoat_dot_check", generated=True),
    "state-get":             _m("low", True, "none", False, False, True, "rasoat_hoso", None, True, "lookup_ops", generated=True),
    "state-put":             dict(_m("medium", False, "drive", False, True, True, "rasoat_hoso", None, True, "lookup_ops", generated=True),
                                  builtin_gate="rasoat_state_scope_guard"),
    # r217: GHI record cache cục bộ (không mạng) — có --confirm và DRY mặc định vì đây là sửa NGUỒN
    # pháp lý đang phục vụ tra cứu; risk medium chứ không low, dù phạm vi ghi chỉ là "local".
    "doc-patch":             _m("medium", False, "local", True, True, True, "rasoat_hoso", None, False, "lookup_ops", generated=True),
    "footnote-map":          _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "cluster":               _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "rasoat-chongcheo":      _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "dedup-check":           _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "confirm":               _m("medium", False, "registry", False, True, False, None, None, False, None, generated=True),
    "header-verify":         _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "corpus-audit":          _m("low", False, "local", False, False, False, None, None, False, None, generated=True),
    "review-queue":          _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "ingest-route":          _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "backfill-notebook":     _m("medium", False, "registry", False, True, False, None, None, False, None, generated=True),
    "cache-snapshot":        _m("low", False, "local", False, False, False, None, None, False, None, generated=True),
    "nlm-list":              _m("low", True, "none", False, False, False, None, None, False, None, generated=True, nlm_fallback="stale_cache"),
    "preflight":             _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "overflow-resolve":      _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "ingest-missing":        _m("high", False, "nlm_registry", False, True, False, None, "ingest_missing", False, None, generated=True, nlm_fallback="defer"),   # Pha-E-hoàn-thiện v1.34.16
    "nlm-orphans":           _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "sweep":                 _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "counts":                _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "ops-plan":              _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "loop":                  _m("medium", False, "registry", False, True, False, None, None, False, None, generated=True),
    "consolidation-cleanup": _m("medium", False, "registry_nlm", False, True, False, None, None, False, None, generated=True),
    "ingest-analyze":        _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "registry-map":          _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "cat-list":              _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "cat-verify":            _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "source-verify":         _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "cat-audit":             _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "nlm-content":           _m("low", True, "none", False, False, False, None, None, False, None, generated=True, nlm_fallback="corpus_read"),
    "nlm-query":             _m("low", True, "none", False, False, False, None, None, False, None, generated=True, nlm_fallback="corpus_read"),
    "bench":                 _m("low", False, "local", False, False, False, None, None, False, None, generated=True),
    "tvpl-url":              _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "fetch-route":           _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "fetch-batch":           _m("low", False, "local", False, False, False, None, None, False, None, generated=True),
    "fetch-links":           _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "find-doc":              _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "profile-create":        _m("medium", False, "drive_local", False, True, False, None, None, False, None, generated=True),
    "profile-file-remove":   _m("medium", False, "drive_registry", True, True, False, None, None, False, None, generated=True),
    "ingest":                _m("high", False, "drive_registry_nlm", True, True, False, "ingest_local", "ingest_local", True, None, generated=True),
    "manifest":              _m("high", False, "drive_registry", True, False, False, None, "manifest", False, None, generated=True),   # Pha-E-hoàn-thiện v1.34.16
    "profile-rebuild-registry": _m("high", False, "registry", True, True, False, None, "profile_rebuild_registry", False, None, generated=True),   # Pha-E-hoàn-thiện v1.34.16
    "vbhn-normalize":        _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "registry-doctor":       _m("low", True, "none", False, False, False, None, None, False, None, generated=True),
    "the-thuc-check":        _m("low", True, "none", False, False, True, None, None, False, "the_thuc", generated=True),   # R2 v1.34.75 — PURE offline, đọc docx local, envelope deterministic
    "the-thuc-build":       _m("low", False, "local", False, False, True, None, None, False, "the_thuc", generated=True),
    "the-thuc-normalize":    _m("low", False, "local", False, False, True, None, None, False, "the_thuc", generated=True),   # R4 v1.34.78 — ghi file OUT local (không Drive/registry/NLM)
    "registry-coverage":     _m("low", True, "none", False, False, True, "workflow_audit", None, False, "workflow", generated=True),
    # ── AG-T0-05: 26 top-level commands metadata ──
    "gws-ping":              _m("low", True, "none", False, False, False, None, None, False, "gws"),
    "download":              _m("low", False, "local", False, False, False, None, None, False, "gws"),
    "gws-bootstrap-cowork":  _m("low", False, "local", False, False, False, None, None, False, "gws"),
    "drive-parity":          _m("low", True, "none", False, False, False, None, None, False, "gws"),
    "bootstrap":             _m("low", False, "local", False, False, False, None, None, False, "gws"),
    "nlm-install":           _m("low", False, "local", False, False, False, None, None, False, "gws"),
    "overlap":               _m("low", True, "none", False, False, False, None, None, False, "lookup_ops"),
    "nlm-auth-pull":         _m("low", False, "local", False, False, False, None, None, False, "gws"),
    "secrets-stage":         dict(_m("medium", False, "drive", False, False, False, None, None, False, "gws"),
                                  builtin_gate="secrets_master_key_gate"),
    "secrets-set":           dict(_m("medium", False, "drive", False, False, False, None, None, False, "gws"),
                                  builtin_gate="secrets_master_key_gate"),
    "gws-auth-stage":        dict(_m("medium", False, "drive", False, False, False, None, None, False, "gws"),
                                  builtin_gate="gws_auth_stage_gate"),
    "gws-auth-load":         _m("low", False, "local", False, False, False, None, None, False, "gws"),
    "nlm-auth-stage":        dict(_m("medium", False, "drive", False, False, False, None, None, False, "gws"),
                                  builtin_gate="nlm_auth_stage_gate"),
    "nlm-auth-load":         _m("low", False, "local", False, False, False, None, None, False, "gws"),
    "transport-info":        _m("low", True, "none", False, False, False, None, None, False, "gws"),
    "profile-files":         _m("low", True, "none", False, False, False, None, None, False, "profile_mgmt"),
    "locate":                _m("low", True, "none", False, False, False, None, None, False, "lookup_ops"),
    "exists":                _m("low", True, "none", False, False, False, None, None, False, "lookup_ops"),
    "source-map":            _m("low", True, "local", False, False, False, None, None, False, "lookup_ops"),
    "instruction-audit":     _m("low", True, "none", False, False, False, None, None, False, "ops_misc"),
    "nlm-get":               _m("low", True, "local", False, False, False, None, None, False, "nlm_ops", nlm_fallback="unverified"),
    "reg-query":             _m("low", True, "local", False, False, False, None, None, False, "ops_misc"),
    "instructions":          _m("low", False, "local", False, False, False, None, None, False, "ops_misc"),
    "profile-file-add":      _m("high", False, "drive_registry_nlm", True, True, False, "ingest_local", "profile_ingest", True, "ingest_ops", nlm_fallback="defer"),
    "reconcile":             _m("medium", False, "drive_registry", True, True, False, None, None, False, "hygiene"),
    "cache-build":           _m("low", False, "local", False, False, False, None, None, False, "extract_cache"),
}


# r310 (RAS-01 vế metadata/CLI): meta cho lệnh LỒNG `<cha> <con>`. Trước đây registry chỉ biết tên
# TOP-LEVEL nên mọi writer nằm dưới một subcommand đều VÔ HÌNH với `tool-inventory`/`workflow-audit
# --strict` — đúng ba đường GHI của `rasoat`. Khoá = ĐƯỜNG DẪN đầy đủ ngăn bằng dấu cách.
# `deterministic_json_required=False`: handler chung là `cmd_rasoat` (passthrough sang script con), không
# phải lệnh JSON của determinism-era; ép cổng _json_dumps ở đây sẽ là cờ GIẢ.
NESTED_COMMAND_META = {
    "rasoat keywords":    _m("medium", False, "registry", False, True, False, None, None, False, "lookup_ops"),
    "rasoat titles":      _m("medium", False, "registry", False, True, False, None, None, False, "lookup_ops"),
    "rasoat orchestrate": _m("medium", False, "registry", False, True, False, None, None, False, "lookup_ops"),
    # worksheet/phuluc chỉ sinh file trong --out-dir ⇒ write_scope local, không cần cổng ngoài-repo.
    "rasoat worksheet":   _m("low", False, "local", False, False, False, None, None, False, "lookup_ops"),
    "rasoat phuluc":      _m("low", False, "local", False, False, False, None, None, False, "lookup_ops"),
    # ── AG-T0-05: hygiene nested commands metadata ──
    "hygiene scan":       _m("low", True, "none", False, False, False, None, None, False, "hygiene"),
    "hygiene plan":       _m("medium", False, "drive_registry", True, True, False, None, None, False, "hygiene"),
    "hygiene query":      _m("low", True, "none", False, False, False, None, None, False, "hygiene"),
    "hygiene reconcile":  _m("medium", False, "drive_registry", True, True, False, None, None, False, "hygiene"),
}


def all_command_meta() -> dict:
    """COMMAND_META + NESTED_COMMAND_META — bề mặt ĐẦY ĐỦ mà audit/inventory phải soi."""
    return {**COMMAND_META, **NESTED_COMMAND_META}


def registry_summary() -> dict:
    """E3: cho tool-inventory — metadata rút gọn, sort key tất định.

    r310: gộp cả lệnh LỒNG (`rasoat keywords`…) — inventory phải kê MỌI public writer, kể cả writer nằm
    dưới một subcommand. `counts.nested` tách riêng để đọc được delta khi thêm/bớt nhánh lồng."""
    _all = all_command_meta()
    cmds = {}
    for name in sorted(_all):
        m = _all[name]
        cmds[name] = {k: m[k] for k in ("risk", "read_only", "write_scope", "requires_confirm",
                                        "supports_dry_run", "workflow_task", "idempotency_contract", "generated")}
    counts = {
        "total": len(cmds),
        "generated_parsers": sum(1 for m in _all.values() if m["generated"]),
        "high_risk": sum(1 for m in _all.values() if m["risk"] == "high"),
        "write_commands": sum(1 for m in _all.values() if not m["read_only"]),
        "nested": len(NESTED_COMMAND_META),
    }
    return {"schema": "command_registry.v1", "counts": counts, "commands": cmds}


# v1.34.1: siết TOÀN BỘ lệnh ghi high-risk legacy — hết grandfather (deadline r65 'trước v1.34.1' đúng hạn).
_CONTRACT_REQUIRED = {"ingest", "nlm-add", "recat", "source-rename", "source-delete", "reg-delete", "dedup-plan",
                      "profile-rebuild-registry", "ingest-missing", "manifest",   # Pha-E-hoàn-thiện v1.34.16
                      "register", "drive-push", "nlm-reconcile", "push-overflow",
                      "shared-source-fix", "source-update-corpus",
                      "dedup-corpus"}   # v1.34.63 B1 (apply high-risk — contract dedup_corpus)


def _parser_for_path(sub, name: str):
    """r310: resolve tên lệnh (kể cả LỒNG, `"rasoat keywords"`) → parser. None nếu không có nhánh nào."""
    parts = name.split()
    p = sub.choices.get(parts[0])
    for seg in parts[1:]:
        if p is None:
            return None
        nxt = next((a for a in p._actions if isinstance(a, argparse._SubParsersAction)), None)
        p = nxt.choices.get(seg) if nxt else None
    return p


def collect_parser_tree(parser) -> list[dict]:
    """Duyệt đệ quy toàn bộ cây lệnh Argparse (top-level + nested subparsers).

    Trả danh sách các node có thứ tự tất định (sort theo path).
    """
    nodes = []

    def _walk(p, prefix="", parent=None, depth=1):
        sub_actions = [a for a in p._actions if isinstance(a, argparse._SubParsersAction)]
        for sub_act in sub_actions:
            helps = {ca.dest: ca.help for ca in getattr(sub_act, "_choices_actions", [])}
            for choice_name, sub_p in sorted(sub_act.choices.items()):
                path = f"{prefix} {choice_name}".strip() if prefix else choice_name
                child_subs = [a for a in sub_p._actions if isinstance(a, argparse._SubParsersAction)]
                is_container = len(child_subs) > 0
                opts = sorted(set(getattr(sub_p, "_option_string_actions", {}).keys()))
                pos = sorted([a.dest for a in sub_p._actions if not isinstance(a, argparse._SubParsersAction) and not a.option_strings])
                fn = sub_p.get_default("fn")
                has_handler = fn is not None
                help_text = (helps.get(choice_name) or getattr(sub_p, "description", "") or getattr(sub_p, "help", "") or "").strip()
                nodes.append({
                    "path": path,
                    "name": choice_name,
                    "parent": parent,
                    "depth": depth,
                    "is_container": is_container,
                    "help": help_text,
                    "options": opts,
                    "positionals": pos,
                    "has_handler": has_handler,
                })
                if is_container:
                    _walk(sub_p, prefix=path, parent=path, depth=depth + 1)

    _walk(parser)
    return sorted(nodes, key=lambda x: x["path"])


def compute_parser_coverage(parser, tl_module=None, *, strict: bool = False, unregistered_only: bool = False) -> dict:
    """Báo cáo độ phủ hai chiều cây lệnh parser ↔ command registry (Packet AG-T0-03).

    Schema: parser_tree_coverage.v1
    """
    tree = collect_parser_tree(parser)
    if tl_module is not None and (hasattr(tl_module, "COMMAND_META") or hasattr(tl_module, "NESTED_COMMAND_META")):
        raw_top = getattr(tl_module, "COMMAND_META", {})
        raw_nested = getattr(tl_module, "NESTED_COMMAND_META", {})
        meta = {**raw_top, **raw_nested}
    else:
        meta = all_command_meta()

    containers = [n for n in tree if n["is_container"]]
    leaf_nodes = [n for n in tree if not n["is_container"]]

    leaf_paths = {n["path"]: n for n in leaf_nodes}
    meta_paths = set(meta.keys())

    covered_paths = sorted(set(leaf_paths.keys()) & meta_paths)
    unregistered_paths = sorted(set(leaf_paths.keys()) - meta_paths)
    registry_not_in_parser = sorted(meta_paths - set(leaf_paths.keys()) - {c["path"] for c in containers})

    total_leaf = len(leaf_nodes)
    covered_count = len(covered_paths)
    unregistered_count = len(unregistered_paths)
    pct = round((covered_count / total_leaf * 100), 2) if total_leaf else 0.0

    commands_detail = []
    for node in leaf_nodes:
        p = node["path"]
        m = meta.get(p)
        if unregistered_only and m is not None:
            continue
        entry = {
            "path": p,
            "name": node["name"],
            "parent": node["parent"],
            "depth": node["depth"],
            "has_meta": m is not None,
            "options": node["options"],
            "positionals": node["positionals"],
            "has_handler": node["has_handler"],
        }
        if m:
            entry["risk"] = m.get("risk", "low")
            entry["read_only"] = m.get("read_only", True)
            entry["write_scope"] = m.get("write_scope", "none")
            entry["requires_confirm"] = m.get("requires_confirm", False)
            entry["supports_dry_run"] = m.get("supports_dry_run", False)
            entry["workflow_task"] = m.get("workflow_task", None)
            entry["idempotency_contract"] = m.get("idempotency_contract", None)
            entry["generated"] = m.get("generated", False)
            entry["module"] = m.get("module", None)
        else:
            entry["risk"] = "unregistered"
            entry["read_only"] = None
            entry["write_scope"] = "unregistered"
            entry["requires_confirm"] = None
            entry["supports_dry_run"] = None
            entry["workflow_task"] = None
            entry["idempotency_contract"] = None
            entry["generated"] = False
            entry["module"] = None
        commands_detail.append(entry)

    high_risk_unregistered = [
        p for p in unregistered_paths
        if any(flag in leaf_paths[p]["options"] for flag in ("--apply", "--delete", "--trash", "--write", "--purge"))
    ]

    ok = True
    if strict:
        if unregistered_paths or registry_not_in_parser:
            ok = False

    return {
        "schema": "parser_tree_coverage.v1",
        "ok": ok,
        "summary": {
            "total_nodes": len(tree),
            "container_commands": len(containers),
            "total_leaf_commands": total_leaf,
            "registered_leaf_commands": covered_count,
            "unregistered_leaf_commands": unregistered_count,
            "coverage_percent": pct,
            "registry_orphaned_commands": len(registry_not_in_parser),
            "high_risk_unregistered_count": len(high_risk_unregistered),
        },
        "categories": {
            "covered": covered_paths,
            "unregistered": unregistered_paths,
            "containers": sorted([c["path"] for c in containers]),
            "registry_not_in_parser": registry_not_in_parser,
            "high_risk_unregistered": sorted(high_risk_unregistered),
        },
        "commands": commands_detail,
    }


def validate_registry(parser, tl_module, *, load_card=None, contracts=None) -> dict:
    """E4: đối chiếu registry ↔ parser ↔ cards ↔ contracts. Trả {issues:[], warnings:[]} — issues = fail."""
    issues, warnings = [], []
    sub = next(a for a in parser._actions if isinstance(a, argparse._SubParsersAction))
    for name, m in sorted(all_command_meta().items()):
        p = _parser_for_path(sub, name)
        if p is None:
            issues.append(f"REGISTRY_CMD_NOT_IN_PARSER:{name}")
            continue
        if m["generated"]:
            fn = p.get_default("fn")
            spec = next(s for s in GENERATED_SPECS if s["name"] == name)
            if getattr(fn, "__name__", "") != spec["handler"]:
                issues.append(f"GENERATED_HANDLER_MISMATCH:{name}:{getattr(fn, '__name__', fn)}")
        option_strings = set(p._option_string_actions)
        if m["requires_confirm"] and "--confirm" not in option_strings:
            issues.append(f"REQUIRES_CONFIRM_FLAG_MISSING:{name}")
        # lệnh GHI NGOÀI-repo (drive/registry/nlm/live) phải có ÍT NHẤT một gate:
        # contract / confirm / dry-run / builtin_gate; ghi artifact LOCAL (zip/report/golden) miễn.
        _external = any(t in str(m["write_scope"]) for t in ("drive", "registry", "nlm", "live"))
        if not m["read_only"] and _external and not (m["idempotency_contract"] or m["requires_confirm"]
                                                     or m["supports_dry_run"] or m.get("builtin_gate")):
            issues.append(f"WRITE_CMD_NO_GATE:{name}")
        # high-risk ghi mà không có contract → warning (mục tiêu Pha G nâng thành fail)
        # v1.33.59 (Pha G — quyết định grilling #6): 6 lệnh ghi đụng Drive/NLM/registry-corpus PHẢI có
        # contract (fail-strict); nhóm còn lại advisory với deadline pha kế (trước v1.34.1).
        # v1.34.1: deadline ĐÚNG HẠN — cả 12 lệnh ghi high-risk đều trong _CONTRACT_REQUIRED; nhánh
        # warning giữ lại làm lưới cho lệnh ghi high-risk MỚI chưa kịp contract (drift-lock r65 bắt).
        if m["risk"] == "high" and not m["read_only"] and not m["idempotency_contract"]:
            if name in _CONTRACT_REQUIRED:
                issues.append(f"CONTRACT_REQUIRED_MISSING:{name}")
            else:
                warnings.append(f"HIGH_RISK_WRITE_NO_IDEMPOTENCY_CONTRACT:{name}")
        # card_required → card phải load được
        if m["card_required"] and m["workflow_task"] and callable(load_card):
            card = load_card(m["workflow_task"])
            if not (isinstance(card, dict) and card.get("ok", True) and (card.get("id") or card.get("workflow_id"))):
                issues.append(f"CARD_MISSING_FOR:{name}:{m['workflow_task']}")
            elif isinstance(card.get("command_contracts"), dict) and name in card["command_contracts"]:
                cc = card["command_contracts"][name]
                if bool(cc.get("confirm_required")) != bool(m["requires_confirm"]):
                    issues.append(f"CARD_CONFIRM_META_MISMATCH:{name}")
                if bool(cc.get("dry_run_required")) != bool(m["supports_dry_run"]):
                    issues.append(f"CARD_DRY_RUN_META_MISMATCH:{name}")
                if cc.get("confirm_required") and "--confirm" not in option_strings:
                    issues.append(f"CARD_CONFIRM_FLAG_MISSING:{name}")
                if cc.get("plan_hash_required") and "--expected-plan-hash" not in option_strings:
                    issues.append(f"CARD_PLAN_HASH_FLAG_MISSING:{name}")
        # contract khai trong meta phải tồn tại trong _IDEMPOTENCY_CONTRACTS
        if m["idempotency_contract"] and isinstance(contracts, dict) and m["idempotency_contract"] not in contracts:
            issues.append(f"CONTRACT_KEY_UNKNOWN:{name}:{m['idempotency_contract']}")
        # JSON của lệnh mới phải đi qua cổng deterministic (scan source handler THẬT trong module)
        if m["deterministic_json_required"] and m["module"]:
            try:
                import importlib
                mod = importlib.import_module(f"tl_core.{m['module']}")
                real = getattr(mod, f"cmd_{name.replace('-', '_')}", None)
                if real is not None:
                    src = inspect.getsource(real)
                    if not any(g in src for g in ("_json_dumps", "_print_json_or_text", "_emit_json_payload")):
                        issues.append(f"JSON_NOT_THROUGH_DETERMINISTIC_GATE:{name}")
            except Exception as e:  # noqa: BLE001
                warnings.append(f"GATE_SCAN_FAILED:{name}:{type(e).__name__}")
    # chiều ngược: contract key nào không có lệnh nào tham chiếu → warning (card mồ côi đã có audit riêng)
    if isinstance(contracts, dict):
        used = {m["idempotency_contract"] for m in all_command_meta().values() if m["idempotency_contract"]}
        for k in sorted(set(contracts) - used):
            warnings.append(f"CONTRACT_UNREFERENCED_BY_REGISTRY:{k}")
    # r310 (RAS-01): chiều NGƯỢC cho nhánh `rasoat` — mỗi sub trong RASOAT_SPECS PHẢI có meta. Không có
    # lưới này thì thêm một sub GHI mới lại tái diễn đúng lỗ cũ: writer chạy được mà audit không biết.
    for _s in RASOAT_SPECS:
        if f"rasoat {_s['name']}" not in NESTED_COMMAND_META:
            issues.append(f"RASOAT_SUB_NOT_IN_REGISTRY:{_s['name']}")
    cov = compute_parser_coverage(parser, tl_module=tl_module)
    for unreg in cov["categories"]["unregistered"]:
        issues.append(f"UNREGISTERED_PARSER_CMD:{unreg}")
    for hr_cmd in cov["categories"]["high_risk_unregistered"]:
        warnings.append(f"UNREGISTERED_HIGH_RISK_PARSER_CMD:{hr_cmd}")
    return {"schema": "registry_validate.v1", "ok": not issues, "issues": issues, "warnings": warnings,
            "checked_commands": len(all_command_meta()), "coverage": cov["summary"]}
