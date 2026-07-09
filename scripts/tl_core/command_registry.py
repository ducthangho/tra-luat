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
     "help": "READ-ONLY: verify RELEASE_MANIFEST với root hiện tại",
     "args": [
         {"dest": "manifest"},
         {"flags": ["--root"], "help": "root gói skill; mặc định HERE.parent"},
         {"flags": ["--strict"], "action": "store_true", "help": "coi file thừa là lỗi"},
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
     "help": '(MERGE) bật/tắt cờ corpus 1 nguồn VBQPPL: `false`=BỎ RA KHỎI CORPUS (reg_upsert corpus=false reversible + gỡ nguồn NLM, GUARD shared_source_id); `true`=đưa vào lại. DRY mặc định; --apply --confirm yes',
     "args": [
         {"dest": 'target', "help": 'drive_id hoặc số hiệu'},
         {"dest": 'status', "help": 'true/false (đưa vào / bỏ ra khỏi corpus)'},
         {"flags": ['--apply'], "action": 'store_true'},
         {"flags": ['--confirm'], "default": ''},
         {"flags": ['--refresh'], "action": 'store_true'},
         {"flags": ['--force-unsafe'], "dest": 'force_unsafe', "action": 'store_true', "help": '(Pha 1+) bỏ qua precheck blocker (rủi ro)'},
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
     "help": 'DRY-RUN: giải nén zip an toàn và lập batch plan nạp VBQPPL; apply chưa bật ở pha an toàn',
     "args": [
         {"dest": 'file'},
         {"flags": ['--cat'], "help": 'category VBQPPL dự kiến; thiếu cat sẽ cảnh báo'},
         {"flags": ['--max-files'], "type": int, "default": 200},
         {"flags": ['--max-size-mb'], "type": int, "default": 100},
         {"flags": ['--apply'], "action": 'store_true', "help": 'thực thi batch sau dry-run; yêu cầu --confirm yes'},
         {"flags": ['--confirm'], "choices": ['yes'], "help": 'bắt buộc khi --apply'},
         {"flags": ['--continue-on-error'], "action": 'store_true', "help": 'tiếp tục file sau nếu một file lỗi'},
         {"flags": ['--skip-nlm-preflight'], "action": 'store_true', "help": 'truyền xuống ingest-local nếu cần tự vá NLM sau'},
         {"flags": ['--json'], "action": 'store_true'},
     ]},
    {"name": 'profile-ingest-zip', "handler": 'cmd_profile_ingest_zip',
     "help": 'DRY-RUN: giải nén zip an toàn và lập batch plan nạp profile; apply chưa bật ở pha an toàn',
     "args": [
         {"dest": 'file'},
         {"flags": ['--max-files'], "type": int, "default": 200},
         {"flags": ['--max-size-mb'], "type": int, "default": 100},
         {"flags": ['--apply'], "action": 'store_true', "help": 'thực thi batch sau dry-run; yêu cầu --confirm yes'},
         {"flags": ['--confirm'], "choices": ['yes'], "help": 'bắt buộc khi --apply'},
         {"flags": ['--continue-on-error'], "action": 'store_true', "help": 'tiếp tục file sau nếu một file lỗi'},
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
]


def register_generated(sub, tl_module) -> list[str]:
    """Sinh parser cho GENERATED_SPECS; handler resolve từ tl_module (stub ủy quyền). Trả list tên đã sinh."""
    made = []
    for spec in GENERATED_SPECS:
        p = sub.add_parser(spec["name"], **({"help": spec["help"]} if spec.get("help") else {}))
        for a in spec["args"]:
            kw = {k: v for k, v in a.items() if k not in ("flags", "dest")}
            if a.get("flags"):
                p.add_argument(*a["flags"], **kw)
            else:
                p.add_argument(a["dest"], **kw)
        p.set_defaults(fn=getattr(tl_module, spec["handler"]))
        made.append(spec["name"])
    return made


# ───────────────────────── E1: metadata ─────────────────────────
def _m(risk, read_only, write_scope, confirm, dry_run, det_json, task, contract, card_required, module, generated=False):
    return {"risk": risk, "read_only": read_only, "write_scope": write_scope,
            "requires_confirm": confirm, "supports_dry_run": dry_run,
            "deterministic_json_required": det_json, "workflow_task": task,
            "idempotency_contract": contract, "card_required": card_required,
            "module": module, "generated": generated}


COMMAND_META = {
    # ── determinism-era (card_required=True — card PHẢI tồn tại) ──
    "tool-inventory":       _m("low", True, "none", False, False, True, "workflow_audit", None, True, "workflow", True),
    "route-task":           _m("low", True, "none", False, False, True, "workflow_audit", None, True, "workflow", True),
    "workflow-audit":       _m("low", True, "none", False, False, True, "workflow_audit", None, True, "workflow", True),
    "golden-test":          _m("low", False, "local", False, True, True, "workflow_audit", None, True, "workflow", True),
    "determinism-audit":    _m("low", True, "none", False, False, True, "workflow_audit", None, True, "release", True),
    "release-manifest":     _m("low", False, "local", False, True, True, "release_manifest", None, True, "release", True),
    "release-verify":       _m("low", True, "none", False, False, True, "release_verify", None, True, "release", True),
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
    "ingest-local":         _m("high", False, "drive_registry_nlm", False, True, False, "ingest_local", "ingest_local", True, None),
    "profile-ingest":       _m("high", False, "drive_registry_nlm", False, True, False, "ingest_local", "profile_ingest", True, None),
    "nlm-add":              dict(_m("high", False, "nlm", False, False, False, None, "nlm_add", False, None),
                                 builtin_gate="nlm_dedup_live_gate"),
    "recat":                _m("high", False, "drive_registry", False, True, False, None, "recat", False, None, generated=True),
    "source-rename":        _m("high", False, "drive_registry_nlm", False, True, False, None, "source_rename", False, None, generated=True),
    "source-delete":        _m("high", False, "drive_registry_nlm", True, False, False, None, "source_delete", False, None, generated=True),
    "source-update-corpus": _m("high", False, "registry_nlm", True, True, False, None, "source_update_corpus", False, None, generated=True),
    "dedup-plan":           _m("high", False, "registry_nlm", False, True, False, None, "dedup_plan", False, None, generated=True),
    "register":             _m("high", False, "registry", False, True, False, None, "register", False, None),
    "backfill-loai":        _m("medium", False, "registry", False, True, False, None, None, False, None, generated=True),
    "backfill-title-vn":    _m("medium", False, "registry", False, True, False, None, None, False, None, generated=True),
    "backfill-hieuluc":     _m("medium", False, "registry", False, True, False, None, None, False, None, generated=True),
    "drive-push":           dict(_m("high", False, "drive", False, False, False, None, "drive_push", False, None),
                                 builtin_gate="md5_verify_fixed_fileid"),
    "reg-delete":           _m("high", False, "registry", True, False, False, None, "reg_delete", False, None, generated=True),
    "vbhn-year-fix":        _m("medium", False, "registry", False, True, False, None, None, False, None, generated=True),
    "quarantine-fix":       _m("medium", False, "registry", False, True, False, None, None, False, None, generated=True),
    "shared-source-fix":    _m("high", False, "registry_nlm", True, True, False, None, "shared_source_fix", False, None, generated=True),
    "corpus-fix":           _m("medium", False, "registry", False, True, False, None, None, False, None, generated=True),
    "push-overflow":        _m("high", False, "nlm_registry", False, True, False, None, "push_overflow", False, None, generated=True),
    "nlm-reconcile":        _m("high", False, "registry_nlm", False, True, False, None, "nlm_reconcile", False, None),
    "missing-sohieu":       _m("medium", False, "registry", False, True, False, None, None, False, None, generated=True),
    # ── I7 wave-2 (v1.34.11): meta BASELINE bằng-chứng-cờ cho 78 lệnh chuyển GENERATED_SPECS —
    # chính sách grilling: --apply→supports_dry_run (doctrine DRY-mặc-định), --confirm→requires_confirm,
    # ghi ngoài-repo→medium+scope đích, KHÔNG high mới (nâng high+contract = Pha-E-hoàn-thiện sau).
    "ping":                  _m("low", True, "none", False, False, False, None, None, False, None),
    "cowork-plan":           _m("low", True, "none", False, False, False, None, None, False, None),
    "perf":                  _m("low", True, "none", False, False, False, None, None, False, None),
    "init-config":           _m("low", False, "local", False, False, False, None, None, False, None),
    "doctor":                _m("low", True, "none", False, False, False, None, None, False, None),
    "precheck":              _m("low", True, "none", False, False, False, None, None, False, None),
    "journal":               _m("low", False, "local", False, False, False, None, None, False, None),
    "resume":                _m("medium", False, "registry", False, True, False, None, None, False, None),
    "undo":                  _m("medium", False, "registry", True, True, False, None, None, False, None),
    "verify-integrity":      _m("low", True, "none", False, False, False, None, None, False, None),
    "edit-skill":            _m("low", False, "local", False, True, False, None, None, False, None),
    "profile-info":          _m("low", True, "none", False, False, False, None, None, False, None),
    "config-pin-registry":   _m("low", False, "local", False, False, False, None, None, False, None),
    "profile-list":          _m("low", True, "none", False, False, False, None, None, False, None),
    "profile-use":           _m("low", False, "local", False, True, False, None, None, False, None),
    "profile-rename":        _m("medium", False, "drive_local", False, True, False, None, None, False, None),
    "profile-delete":        _m("medium", False, "drive_local", True, True, False, None, None, False, None),
    "profile-manifest":      _m("low", True, "none", False, False, False, None, None, False, None),
    "profile-adopt":         _m("medium", False, "drive_local", False, True, False, None, None, False, None),
    "profile-doctor":        _m("medium", False, "drive_local", False, True, False, None, None, False, None),
    "profile-index":         _m("medium", False, "drive_local", False, True, False, None, None, False, None),
    "boot":                  _m("low", False, "local", False, False, False, None, None, False, None),
    "up":                    _m("low", False, "local", False, False, False, None, None, False, None),
    "relation-check":        _m("low", True, "none", False, False, False, None, None, False, None),
    "relation-backfill":     _m("medium", False, "registry", False, True, False, None, None, False, None),
    "vbhn-check":            _m("low", True, "none", False, False, False, None, None, False, None),
    "vbhn-verify":           _m("low", True, "none", False, False, False, None, None, False, None),
    "vbhn-compare":          _m("low", True, "none", False, False, False, None, None, False, None),
    "status":                _m("low", True, "none", False, False, False, None, None, False, None),
    "extract":               _m("low", False, "local", False, False, False, None, None, False, None),
    "external-ingest":       _m("medium", False, "drive_nlm", True, False, False, None, None, False, None),
    "link-priority":         _m("low", True, "none", False, False, False, None, None, False, None),
    "slot-audit":            _m("low", True, "none", False, False, False, None, None, False, None),
    "xref":                  _m("low", True, "none", False, False, False, None, None, False, None),
    "frontier-expand":       _m("low", True, "none", False, False, False, None, None, False, None),
    "rasoat-loop":           _m("low", False, "local", False, False, False, None, None, False, None),
    "footnote-map":          _m("low", True, "none", False, False, False, None, None, False, None),
    "cluster":               _m("low", True, "none", False, False, False, None, None, False, None),
    "rasoat-chongcheo":      _m("low", True, "none", False, False, False, None, None, False, None),
    "dedup-check":           _m("low", True, "none", False, False, False, None, None, False, None),
    "confirm":               _m("medium", False, "registry", False, True, False, None, None, False, None),
    "header-verify":         _m("low", True, "none", False, False, False, None, None, False, None),
    "corpus-audit":          _m("low", False, "local", False, False, False, None, None, False, None),
    "review-queue":          _m("low", True, "none", False, False, False, None, None, False, None),
    "ingest-route":          _m("low", True, "none", False, False, False, None, None, False, None),
    "backfill-notebook":     _m("medium", False, "registry", False, True, False, None, None, False, None),
    "cache-snapshot":        _m("low", False, "local", False, False, False, None, None, False, None),
    "nlm-list":              _m("low", True, "none", False, False, False, None, None, False, None),
    "preflight":             _m("low", True, "none", False, False, False, None, None, False, None),
    "overflow-resolve":      _m("low", True, "none", False, False, False, None, None, False, None),
    "ingest-missing":        _m("medium", False, "nlm_registry", False, True, False, None, None, False, None),
    "nlm-orphans":           _m("low", True, "none", False, False, False, None, None, False, None),
    "sweep":                 _m("low", True, "none", False, False, False, None, None, False, None),
    "counts":                _m("low", True, "none", False, False, False, None, None, False, None),
    "ops-plan":              _m("low", True, "none", False, False, False, None, None, False, None),
    "loop":                  _m("medium", False, "registry", False, True, False, None, None, False, None),
    "consolidation-cleanup": _m("medium", False, "registry_nlm", False, True, False, None, None, False, None),
    "ingest-analyze":        _m("low", True, "none", False, False, False, None, None, False, None),
    "registry-map":          _m("low", True, "none", False, False, False, None, None, False, None),
    "cat-list":              _m("low", True, "none", False, False, False, None, None, False, None),
    "cat-verify":            _m("low", True, "none", False, False, False, None, None, False, None),
    "source-verify":         _m("low", True, "none", False, False, False, None, None, False, None),
    "cat-audit":             _m("low", True, "none", False, False, False, None, None, False, None),
    "nlm-content":           _m("low", True, "none", False, False, False, None, None, False, None),
    "nlm-query":             _m("low", True, "none", False, False, False, None, None, False, None),
    "bench":                 _m("low", False, "local", False, False, False, None, None, False, None),
    "tvpl-url":              _m("low", True, "none", False, False, False, None, None, False, None),
    "fetch-route":           _m("low", True, "none", False, False, False, None, None, False, None),
    "fetch-batch":           _m("low", False, "local", False, False, False, None, None, False, None),
    "fetch-links":           _m("low", True, "none", False, False, False, None, None, False, None),
    "find-doc":              _m("low", True, "none", False, False, False, None, None, False, None),
    "profile-create":        _m("medium", False, "drive_local", False, True, False, None, None, False, None),
    "profile-file-remove":   _m("medium", False, "drive_registry", True, True, False, None, None, False, None),
    "ingest":                _m("medium", False, "drive_registry_nlm", False, True, False, None, None, False, None),
    "manifest":              _m("medium", False, "drive_registry", True, False, False, None, None, False, None),
    "profile-rebuild-registry": _m("medium", False, "registry", True, True, False, None, None, False, None),
    "vbhn-normalize":        _m("low", True, "none", False, False, False, None, None, False, None),
    "registry-doctor":       _m("low", True, "none", False, False, False, None, None, False, None),
}


def registry_summary() -> dict:
    """E3: cho tool-inventory — metadata rút gọn, sort key tất định."""
    cmds = {}
    for name in sorted(COMMAND_META):
        m = COMMAND_META[name]
        cmds[name] = {k: m[k] for k in ("risk", "read_only", "write_scope", "requires_confirm",
                                        "supports_dry_run", "workflow_task", "idempotency_contract", "generated")}
    counts = {
        "total": len(cmds),
        "generated_parsers": sum(1 for m in COMMAND_META.values() if m["generated"]),
        "high_risk": sum(1 for m in COMMAND_META.values() if m["risk"] == "high"),
        "write_commands": sum(1 for m in COMMAND_META.values() if not m["read_only"]),
    }
    return {"schema": "command_registry.v1", "counts": counts, "commands": cmds}


# v1.34.1: siết TOÀN BỘ lệnh ghi high-risk legacy — hết grandfather (deadline r65 'trước v1.34.1' đúng hạn).
_CONTRACT_REQUIRED = {"nlm-add", "recat", "source-rename", "source-delete", "reg-delete", "dedup-plan",
                      "register", "drive-push", "nlm-reconcile", "push-overflow",
                      "shared-source-fix", "source-update-corpus"}


def validate_registry(parser, tl_module, *, load_card=None, contracts=None) -> dict:
    """E4: đối chiếu registry ↔ parser ↔ cards ↔ contracts. Trả {issues:[], warnings:[]} — issues = fail."""
    issues, warnings = [], []
    sub = next(a for a in parser._actions if isinstance(a, argparse._SubParsersAction))
    for name, m in sorted(COMMAND_META.items()):
        p = sub.choices.get(name)
        if p is None:
            issues.append(f"REGISTRY_CMD_NOT_IN_PARSER:{name}")
            continue
        if m["generated"]:
            fn = p.get_default("fn")
            spec = next(s for s in GENERATED_SPECS if s["name"] == name)
            if getattr(fn, "__name__", "") != spec["handler"]:
                issues.append(f"GENERATED_HANDLER_MISMATCH:{name}:{getattr(fn, '__name__', fn)}")
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
        used = {m["idempotency_contract"] for m in COMMAND_META.values() if m["idempotency_contract"]}
        for k in sorted(set(contracts) - used):
            warnings.append(f"CONTRACT_UNREFERENCED_BY_REGISTRY:{k}")
    return {"schema": "registry_validate.v1", "ok": not issues, "issues": issues, "warnings": warnings,
            "checked_commands": len(COMMAND_META)}
