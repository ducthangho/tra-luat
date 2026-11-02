# -*- coding: utf-8 -*-
"""tl_core.workflow — Pha C (v1.33.56): tách NGUYÊN VĂN từ scripts/tl.py (kế hoạch nợ-kỹ-thuật C1).

KHÔNG gọi trực tiếp từ ngoài — public CLI vẫn là scripts/tl.py (stub ủy quyền). Module nhận các helper
dùng chung của tl qua `bind(tl_module)`: copy MỌI tên public/private của tl vào globals() TRỪ tên đã có
(def riêng của module thắng; tên thuộc module anh em resolve qua STUB đã định nghĩa trong tl trước bind).
Hàm tl là hàm THẬT (đọc global của tl lúc gọi) nên không stale; module KHÔNG đọc bare mutable-global của tl.
"""
from __future__ import annotations

import argparse   # noqa: F401
import datetime   # noqa: F401
import hashlib    # noqa: F401
import json       # noqa: F401
import os         # noqa: F401
import re         # noqa: F401
import shutil     # noqa: F401
import subprocess # noqa: F401
import sys        # noqa: F401
import tempfile   # noqa: F401
import time       # noqa: F401
import zipfile    # noqa: F401
from pathlib import Path  # noqa: F401

from tl_core.test_fragments import FragmentError, find_test_id_pointers, load_test_id_index

_TL = None


def bind(tl_module) -> None:
    global _TL
    _TL = tl_module
    g = globals()
    for _n in dir(tl_module):
        if _n.startswith("__") or _n in g:
            continue
        g[_n] = getattr(tl_module, _n)


# ───────────────────────── deterministic workflow inventory/router ─────────────────────────
_TOOL_GROUPS = {
    "bootstrap_health": {
        "title": "Bootstrap & Health",
        "commands": ["up", "boot", "ping", "doctor", "precheck", "verify-integrity", "transport-info", "gws-ping"],
        "purpose": "Khởi động, kiểm môi trường, kiểm config, kiểm transport.",
    },
    "inventory_decision": {
        "title": "Inventory & Decision",
        "commands": ["tool-inventory", "route-task", "workflow-audit", "doc-claims-check", "determinism-audit", "golden-test", "release-check", "release-manifest", "release-verify", "release-bundle", "live-readiness", "live-contract-check", "live-state-snapshot", "live-state-diff", "live-smoke-plan", "deploy-plan", "rollback-plan", "final-acceptance", "go-live-runbook"],
        "purpose": "Tra kho tool/script và định tuyến workflow trước khi viết tool mới hoặc làm tác vụ rủi ro.",
    },
    "source_discovery": {
        "title": "Source Discovery",
        "commands": ["find-doc", "fetch-links", "fetch-route", "fetch-batch", "exists", "locate", "source-map", "link-priority"],
        "purpose": "Tìm nguồn, kiểm hiện diện, chọn đúng văn bản/phiên bản.",
    },
    "legal_verification": {
        "title": "Legal Verification",
        "commands": ["extract", "status", "relation-check", "relation-backfill", "vbhn-check", "vbhn-verify", "vbhn-compare", "overlap", "source-verify"],
        "purpose": "Kiểm hiệu lực, VBHN, quan hệ sửa đổi/bổ sung và trích nguyên văn.",
    },
    "ingest_convert": {
        "title": "Ingest & Convert",
        "commands": ["ingest-route", "ingest-local", "ingest", "profile-ingest", "profile-file-add", "ingest-ocr", "profile-ingest-ocr", "ingest-zip", "profile-ingest-zip", "profile-ingest-chunks", "external-ingest", "preflight", "nlm-add", "convert-verify"],
        "planned_commands": [],
        "purpose": "Nạp file, convert, đổi tên, ghi registry, add NLM.",
    },
    "ocr_text_quality": {
        "title": "OCR & Text Quality",
        "commands": ["ocr-analyze", "ocr-run", "ocr-verify", "ingest-ocr", "profile-ingest-ocr", "source-verify", "cat-verify", "profile-ingest --text-file --source-quality ocr"],
        "planned_commands": [],
        "purpose": "Phát hiện PDF scan/OCR, kiểm chất lượng text trước khi dùng làm căn cứ.",
    },
    "chunk_query_quality": {
        "title": "Chunking & Query Quality",
        "commands": ["chunk-plan", "chunk-apply", "chunk-verify", "profile-ingest-chunks", "profile-ingest", "nlm-query-plan", "nlm-query", "nlm-cross", "nlm-content"],
        "planned_commands": [],
        "purpose": "Tách văn bản lớn có kiểm soát và truy vấn NLM hẹp, đúng nguồn.",
    },
    "nlm_operations": {
        "title": "NLM Operations",
        "commands": ["nlm-list", "nlm-get", "nlm-query", "nlm-cross", "nlm-content", "nlm-reconcile", "nlm-orphans", "slot-audit", "push-overflow", "overflow-resolve", "nlm-add"],
        "purpose": "Quản trị/đối soát NotebookLM và truy vấn nguồn đã nạp.",
    },
    "registry_profile_corpus": {
        "title": "Registry, Profile & Corpus",
        "commands": ["profile-info", "profile-list", "profile-create", "profile-adopt", "profile-doctor", "profile-index", "profile-files", "registry-map", "reg-query", "register", "manifest"],
        "purpose": "Quản trị registry, manifest, profile/corpus.",
    },
    "hygiene_maintenance": {
        "title": "Hygiene & Maintenance",
        "commands": ["sweep", "hygiene", "reconcile", "dedup-check", "dedup-plan", "source-rename", "source-update-corpus", "source-delete", "quarantine-fix", "cat-audit", "recat", "header-verify", "corpus-audit"],
        "purpose": "Dọn lỗi, dedup, rename, recat, audit corpus.",
    },
    "prompt_instruction_dev": {
        "title": "Prompt, Instruction & Dev",
        "commands": ["instructions", "instruction-audit", "workflow-audit", "determinism-audit", "golden-test", "release-check", "release-manifest", "release-verify", "release-bundle", "live-readiness", "live-contract-check", "live-state-snapshot", "live-state-diff", "live-smoke-plan", "deploy-plan", "rollback-plan", "final-acceptance", "go-live-runbook", "edit-skill", "verify-integrity", "bench", "perf"],
        "purpose": "Sinh prompt/instruction, audit, sửa skill an toàn.",
    },
}


_TASK_TO_WORKFLOW = {
    "write_new_tool": "write_new_tool",
    "viet_tool_moi": "write_new_tool",
    "nlm_query_quality": "nlm_query_quality",
    "nlm_query_plan": "nlm_query_quality",
    "nlm_query": "nlm_query_quality",
    "truy_van_nlm": "nlm_query_quality",
    "ingest_local": "ingest_local",
    "nap_file": "ingest_local",
    "convert_rename": "convert_rename",
    "doi_ten_convert": "convert_rename",
    "ingest_zip": "ingest_zip",
    "profile_ingest_zip": "ingest_zip",
    "ocr_pdf_scan": "ocr_pdf_scan",
    "ocr": "ocr_pdf_scan",
    "ocr_run": "ocr_pdf_scan",
    "ocr_ingest": "ocr_ingest",
    "ingest_ocr": "ocr_ingest",
    "profile_ingest_ocr": "ocr_ingest",
    "nap_ocr": "ocr_ingest",
    "large_doc_chunk": "large_doc_chunk",
    "chunk": "large_doc_chunk",
    "chunk_apply": "large_doc_chunk",
    "chunk_verify": "large_doc_chunk",
    "chunk_ingest": "chunk_ingest",
    "profile_ingest_chunks": "chunk_ingest",
    "nap_chunks": "chunk_ingest",
    "tach_van_ban_lon": "large_doc_chunk",
    "trich_nguyen_van": "nlm_query_quality",
    "workflow_audit": "workflow_audit",
    "audit_workflow": "workflow_audit",
    "determinism_audit": "workflow_audit",
    "audit_determinism": "workflow_audit",
    "golden_test": "workflow_audit",
    "release_check": "release_check",
    "deterministic_check": "release_check",
    "release_manifest": "release_manifest",
    "package_manifest": "release_manifest",
    "release_verify": "release_verify",
    "package_verify": "release_verify",
    "release_bundle": "release_bundle",
    "package_bundle": "release_bundle",
    "live_smoke": "live_smoke_plan",
    "live_smoke_plan": "live_smoke_plan",
    "live_readiness": "live_readiness",
    "live_contract_check": "live_contract_check",
    "contract_check": "live_contract_check",
    "live_state_snapshot": "live_state_snapshot",
    "live_state_diff": "live_state_diff",
    "state_snapshot": "live_state_snapshot",
    "state_diff": "live_state_diff",
    "env_readiness": "live_readiness",
    "readiness": "live_readiness",
    "deploy_plan": "deploy_plan",
    "install_plan": "deploy_plan",
    "rollback_plan": "rollback_plan",
    "restore_plan": "rollback_plan",
    "final_acceptance": "final_acceptance",
    "acceptance": "final_acceptance",
    "go_live_runbook": "go_live_runbook",
    "runbook_live": "go_live_runbook",
}


_IDEMPOTENCY_CONTRACTS = {
    # ── Pha-E-hoàn-thiện (v1.34.16): 3 lệnh NGUY HIỂM — contract THẬT phản ánh gate/journal có sẵn, KHÔNG đổi CLI ──
    "profile_rebuild_registry": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "profile+keep_notebook (xoá-dựng-lại từ manifest profile — chạy lại cùng args cho cùng kết quả từ cùng manifest)",
        "journal_key": "KHÔNG WAL riêng (reg_delete + regen tuần tự) — phá hủy CHỈ sau --apply --confirm yes; CLOBBER-guard chặn profile thiếu registryDocId riêng (PROFILE_REGISTRY_ID_EMPTY_WOULD_CLOBBER_BASE)",
        "resume_behavior": "chạy lại CÙNG LỆNH — dựng lại toàn bộ từ manifest hiện tại (regen idempotent theo nguồn)",
        "duplicate_guard": "DRY mặc định in plan partition; --keep-notebook bắt buộc (không suy own từ notebook)",
        "readback_command": "reg-query --profile <P> --json (đếm dòng own/ref khớp plan) + profile-doctor",
        "resume_command": "profile-rebuild-registry --keep-notebook <id> --apply --confirm yes (cùng profile)",
        "rollback_hint": "Google Sheets version-history của registry profile (bài học 1.23.21 — khôi phục Sheet), KHÔNG có undo journal",
    },
    "ingest_missing": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "drive_id từng nguồn (ckpt WAL 4 khóa done/pending/linked/fails — pending ghi TRƯỚC source_add)",
        "journal_key": "tl_journal/ingest-missing_<run_id> + ckpt file (resume FRESH-verify skip_freshness=False trước khi add lại — chống trùng VBHN_67×3)",
        "resume_behavior": "chạy lại CÙNG LỆNH — done bỏ qua, pending FRESH-verify rồi mới add, fails thử lại",
        "duplicate_guard": "dedup-live tiered (sohieu lỏng-năm + exact-title) + slot-guard overflow-route KHÔNG BAO GIỜ tạo notebook",
        "readback_command": "nlm-list <nb> (đối chiếu source_id) + reg-query --nlm --json",
        "resume_command": "ingest-missing --apply (cùng args; ckpt tự nối)",
        "rollback_hint": "undo <run_id> --apply cho phần registry; nguồn NLM đã add → source-delete từng cái (bất khả nghịch, cần user duyệt)",
    },
    "manifest": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "manifest = DẪN XUẤT tất định từ registry state (export lại = cùng nội dung khi registry không đổi)",
        "journal_key": "KHÔNG WAL — manifest_export ghi đè file manifest Drive; --touched-drive quét cây own CÓ confirm-gate (PROFILE_INHERITED_SCOPE/POLICY guard chặn inherit)",
        "resume_behavior": "chạy lại CÙNG LỆNH — export idempotent; --touched-drive quét lại từ đầu (an toàn, chỉ đắt thời gian)",
        "duplicate_guard": "mặc định CHỈ manifest_export (không đụng cấu trúc); --touched-drive + profile inherit → BẮT --confirm yes (chống PROFILE_MANIFEST_SCOPE_BLOWUP)",
        "readback_command": "boot (nạp lại manifest, đếm entries) + counts --json",
        "resume_command": "manifest [--touched-drive --confirm yes] (cùng args)",
        "rollback_hint": "manifest là dẫn xuất — regen từ registry là khôi phục; sự cố quét phình → profile-rebuild-registry (có guard riêng)",
    },

    "ingest_local": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "sha256(source_file_text_or_binary)+target_profile_or_cat+canonical_name",
        "journal_key": "tl_journal/run_id for upload/convert/register/nlm-add",
        "resume_behavior": "rerun same command with --resume when Drive/register succeeded but NLM/link step was interrupted",
        "duplicate_guard": "convert/readback + registry drive_id/src_id + NLM dedup by drive_id/title before add",
        "readback_command": "convert-verify --gdoc-id <id> --src-id <src_id> --expected-name <name> --json",
        "resume_command": "ingest-local <file> ... --resume --json",
        "rollback_hint": "journal <run_id> then undo <run_id> --apply --confirm yes for registry-safe rollback; Drive/NLM cleanup requires explicit source-delete/nlm-orphans review"
    },
    "profile_ingest": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "sha256(source_file_or_text)+profile+canonical_name",
        "journal_key": "profile ingest child run/journal where available",
        "resume_behavior": "rerun same profile-ingest command; duplicate guard should link existing target instead of adding another NLM source",
        "duplicate_guard": "profile folder/name + registry/profile manifest + NLM source title/drive_id",
        "readback_command": "profile-files --json and convert-verify --gdoc-id <id> --expected-name <name> --json",
        "resume_command": "profile-ingest <file> ... --json",
        "rollback_hint": "remove profile file via profile-file-remove or explicit source-delete after snapshot diff review"
    },
    "ingest_zip": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "sha256(content-v2: norm_path+crc32+size từng member accepted, sort)+mode+cat_or_profile",
        "journal_key": "batch item path + child pipeline journal",
        "resume_behavior": "rerun same zip apply; accepted members are re-planned and child pipelines perform duplicate/readback gates",
        "duplicate_guard": "zip-slip safe extraction + per-file source hash/path + child ingest duplicate guards",
        "readback_command": "ingest-zip <file.zip> --cat <NN> --json then inspect each child_result; run live-state-diff after smoke",
        "resume_command": "ingest-zip <file.zip> --cat <NN> --apply --confirm yes --continue-on-error --json",
        "rollback_hint": "use per-child journals plus live-state-diff; undo registry per run before any Drive/NLM cleanup"
    },
    "ocr_ingest": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "source_file_sha256+text_sha256+ocr_manifest_sha256+cat_or_profile+canonical_name",
        "journal_key": "ocr manifest path + child ingest journal",
        "resume_behavior": "do not rerun OCR unless source hash changed; rerun bridge apply after ocr-verify manifest_status=verified",
        "duplicate_guard": "verified OCR manifest + child ingest duplicate guards; VBQPPL blocks canonical ingest if manifest is missing/unverified",
        "readback_command": "ocr-verify <text_file> --source <source> --mode <mode> --json",
        "resume_command": "ingest-ocr <file> --text-file <text> --cat <NN> --apply --confirm yes --json",
        "rollback_hint": "delete only local OCR sidecars freely; for Drive/registry/NLM use child pipeline journal/snapshot diff"
    },
    "profile_ingest_ocr": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "source_file_sha256+text_sha256+ocr_manifest_sha256+profile+canonical_name",
        "journal_key": "ocr manifest path + profile child ingest journal",
        "resume_behavior": "reuse verified sidecar text/manifest; rerun profile-ingest-ocr apply if child step was interrupted",
        "duplicate_guard": "verified OCR manifest + profile ingest duplicate guards",
        "readback_command": "ocr-verify <text_file> --source <source> --mode profile --json",
        "resume_command": "profile-ingest-ocr <file> --text-file <text> --apply --confirm yes --json",
        "rollback_hint": "remove profile source only after snapshot diff identifies created item"
    },
    "ingest_inbox": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "drive_id per-file (diff registry qua reg_get_bulk — file đã có row KHÔNG vào kế hoạch)",
        "journal_key": "per-child journal (ingest-local/profile-ingest tự journal từng file)",
        "resume_behavior": "chạy lại CÙNG LỆNH — diff registry tự loại file đã xong; child 2-bước DRY→plan_hash→apply",
        "duplicate_guard": "reg_get_bulk diff + child guards (C2 dup-name registry, dedup-live title, contract plan_hash)",
        "readback_command": "reg-query --drive-id <id> --json",
        "resume_command": "ingest-inbox --apply --confirm yes --json",
        "rollback_hint": "per-file theo journal child (tl journal <run> / undo); lệnh cha không ghi gì ngoài child"
    },
    "profile_ingest_chunks": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "chunk_manifest.source_hash+chunk.sha256+profile+expected_name",
        "journal_key": "chunk manifest path + child profile-ingest result",
        "resume_behavior": "rerun profile-ingest-chunks; chunk-verify prevents source drift and child commands are per chunk",
        "duplicate_guard": "chunk_manifest hash verification + profile folder/name + NLM title/drive_id",
        "readback_command": "chunk-verify <manifest> --json",
        "resume_command": "profile-ingest-chunks <manifest> --apply --confirm yes --continue-on-error --json",
        "rollback_hint": "rollback per child result; chunks are helper/profile sources, not VBQPPL canonical"
    }
}

# v1.33.59 (Pha G — siết lớp nguy hiểm, quyết định grilling #6): contract THẬT cho 6 lệnh ghi legacy
# đụng Drive/NLM/registry-corpus. Nhóm backfill/plan còn lại: advisory, deadline trước v1.34.1.
_IDEMPOTENCY_CONTRACTS.update({
    "nlm_add": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "notebook_id+drive_id (hoặc +url/file)",
        "journal_key": "n/a — 1 call API; an toàn nhờ gate, không nhờ journal",
        "resume_behavior": "chạy lại CÙNG LỆNH — dedup-live gate pre-add + post-add re-list làm lệnh idempotent",
        "duplicate_guard": "dedup-live theo drive_id/sohieu/title TRƯỚC add (ALREADY_ON_NOTEBOOK rc=2) + post-add dup check",
        "readback_command": "nlm-get <notebook> --json (source_count + list) / reg-query --sohieu <sh> --json",
        "resume_command": "nlm-add --drive-id <id> [--notebook-id <nb>] (in JSON sẵn, KHÔNG có cờ --json)",
        "rollback_hint": "xoá nguồn vừa add qua NLM UI/nlm source delete rồi reg_upsert clear nlm_source_id,nlm_status",
    },
    "recat": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "drive_id+cat_đích (relabel idempotent — chạy lại vô hại)",
        "journal_key": "tl_journal/recat_<run_id> (intent kèm before-cat từng drive_id)",
        "resume_behavior": "chạy lại CÙNG LỆNH — move + relabel đều idempotent; verified-write đối chiếu patched",
        "duplicate_guard": "boundary-rule cảnh báo cat lệch tên; nhãn ĐỦ canonical chống relabel giả",
        "readback_command": "reg-query --drive-id <id> --json (cat == nhãn đủ) + cat-verify",
        "resume_command": "recat <drive_id...> --cat NN --apply",
        "rollback_hint": "undo <run_id> --apply (journal giữ before-cat) + move file về folder cũ",
    },
    "source_rename": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "drive_id+new_name",
        "journal_key": "tl_journal/source-rename_<run_id> (before-name trong intent)",
        "resume_behavior": "chạy lại CÙNG LỆNH — rename Drive idempotent theo tên đích; NLM title sync theo sau",
        "duplicate_guard": "assert đọc-lại-tên sau rename (v1.22.60); 1 file/lệnh ở Cowork (S13)",
        "readback_command": "reg-query --drive-id <id> --json + files_get tên Drive",
        "resume_command": "source-rename <drive_id> --name <tên> --apply",
        "rollback_hint": "rename ngược về before-name trong journal; NLM title đồng bộ lại",
    },
    "source_delete": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "drive_id",
        "journal_key": "tl_journal/source-delete_<run_id>",
        "resume_behavior": "chạy lại an toàn: đã xoá → NOT_FOUND coi như done (idempotent theo trạng thái đích)",
        "duplicate_guard": "requires_confirm=yes; chặn xoá khi row đang corpus=true trừ khi cờ tường minh",
        "readback_command": "reg-query --drive-id <id> --json (status removed) + nlm-list không còn source",
        "resume_command": "source-delete <drive_id> --apply --confirm yes",
        "rollback_hint": "KHÔNG tự động: khôi phục từ Drive Trash (30 ngày) + nlm-add lại + reg_upsert khôi phục cột",
    },
    "reg_delete": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "drive_id (row registry)",
        "journal_key": "tl_journal/reg-delete_<run_id> (row đầy đủ trong before)",
        "resume_behavior": "chạy lại an toàn: row đã mất → done",
        "duplicate_guard": "requires_confirm=yes; chỉ xoá ROW registry — file Drive/nguồn NLM không đụng",
        "readback_command": "reg-query --drive-id <id> --json (miss = đã xoá)",
        "resume_command": "reg-delete --drive-ids <id[,id...]> (guard require_removed; --force gỡ bất kể status)",
        "rollback_hint": "undo <run_id> --apply nếu journal có before-row; không thì reg_upsert dựng lại từ manifest cache",
    },
    "dedup_plan": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "sha256(tập cụm trùng + canonical được chọn) — plan trước, apply theo plan",
        "journal_key": "tl_journal/dedup-plan_<run_id>",
        "resume_behavior": "chạy lại CÙNG LỆNH: dòng đã corpus=false bị bỏ qua (idempotent)",
        "duplicate_guard": "DRY mặc định; canonical-picker ưu tiên verified/VBHN-năm-mới; reversible corpus=false (không xoá)",
        "readback_command": "sweep --json (duplicates.by_* == 0) + reg-query từng cụm",
        "resume_command": "dedup-plan --apply",
        "rollback_hint": "undo <run_id> --apply — apply chỉ set corpus=false nên đảo lại được toàn phần",
    },
    # ── B1 (v1.34.63): dedup-corpus — trục NỘI DUNG (md5/content-hash/BoW), coexist dedup-plan (trục chủ đề) ──
    "dedup_corpus": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "nhóm content (key = md5 | content-hash) + tập act drive_id — re-plan tươi mỗi lần chạy; nhóm đã xử hết act tự biến mất",
        "journal_key": "tl_journal/dedup-corpus_<run_id> (plan+counts) + journal RIÊNG từng act ủy quyền source-update-corpus/source-delete (undo theo id)",
        "resume_behavior": "chạy lại CÙNG LỆNH — classifier re-plan từ manifest tươi (idempotent theo nguồn); dòng đã corpus=false bị bỏ qua (skipped_already_false)",
        "duplicate_guard": "DRY mặc định; --apply --confirm yes + _apply_gate; guards fail-closed NEAR/UNRESOLVED/PHYSICAL/CROSS_PROFILE đè MỌI mode; --only-md5/--limit duyệt từng bước; --all-profiles flag-only",
        "readback_command": "dedup-corpus --json (DRY re-plan phải hết nhóm đã xử) + reg-query <drive_id> --json từng act",
        "resume_command": "dedup-corpus --apply --confirm yes [--only-md5 <hash>] (re-plan tươi, không cần artifact)",
        "rollback_hint": "mode corpus-false: tl undo <journal source-update-corpus từng id> (reversible); mode delete: Drive trash restore + snapshot dòng trong journal source-delete",
    },
})

# v1.34.1 (siết-6 advisory — deadline r65 'trước v1.34.1' ĐÚNG HẠN): contract THẬT cho 6 lệnh ghi legacy
# còn grandfather. Contract PHẢN ÁNH hành vi đã có trong code (gate+journal+verified-write từ v1.29.2),
# không đổi bề mặt CLI (quyết định grilling 2026-07-09 #6: thêm cờ được, KHÔNG breaking).
_IDEMPOTENCY_CONTRACTS.update({
    "register": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "drive_id+cols+values từng dòng (reg_upsert/reg_bulk idempotent — ghi lại cùng giá trị vô hại)",
        "journal_key": "tl_journal/register-bulk_<run_id> (before theo key_field TỪNG BATCH — v1.29.2 B1#2)",
        "resume_behavior": "chạy lại CÙNG LỆNH — upsert theo drive_id, batch đã ghi giữ nguyên giá trị",
        "duplicate_guard": "_apply_gate precheck write_cols + verified-write đối chiếu từng batch",
        "readback_command": "reg-query --drive-id <id> --json (cols vừa ghi khớp giá trị)",
        "resume_command": "register --drive-id <id> ... (cùng args; bulk: --bulk <file> --cols <cols>; XOÁ TRẮNG: --clear-cols <cols> --confirm yes — server ≥2.21.2j)",
        "rollback_hint": "undo <run_id> --apply (journal giữ before theo key_field từng batch)",
    },
    "push_overflow": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "drive_id+source_id+notebook_đích (set row_kind=overflow — ghi lại cùng giá trị vô hại)",
        "journal_key": "tl_journal/push-overflow_<run_id>",
        "resume_behavior": "chạy lại CÙNG LỆNH — reg_write verified; row đã overflow giữ nguyên",
        "duplicate_guard": "_apply_gate precheck + verified-write; chỉ ghi cột row_kind/nlm_* của đúng drive_id",
        "readback_command": "reg-query --drive-id <id> --json (row_kind=overflow + nlm_notebook_id=shard phụ)",
        "resume_command": "push-overflow --drive-id <id> --source-id <sid> [--notebook-id <nb>]",
        "rollback_hint": "undo <run_id> --apply (journal before); nguồn NLM trên shard phụ gỡ tay nếu cần",
    },
    "nlm_reconcile": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "notebook_id+drive_id+nlm_source_id từng dòng plan (backfill/link idempotent)",
        "journal_key": "tl_journal/nlm-reconcile_<run_id> (before_by_key từng dòng ghi)",
        "resume_behavior": "chạy lại CÙNG LỆNH — DRY re-plan từ ground-truth CLI nlm-list rồi --apply phần còn thiếu",
        "duplicate_guard": "plan từ nlm-list ground-truth; _apply_gate write_cols nlm_source_id,nlm_notebook_id,nlm_status chống clobber/ghi-mù",
        "readback_command": "nlm-reconcile <nb> --json (desync_real=0) + reg-query --refresh",
        "resume_command": "nlm-reconcile <nb> --apply [--clear-stale]",
        "rollback_hint": "undo <run_id> --apply (before_by_key trong journal)",
    },
    "drive_push": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "md5(zip local)+file_id đích (cùng bytes → PATCH cùng nội dung, vô hại; fileId GIỮ NGUYÊN)",
        "journal_key": "n/a — 1 call REST PATCH; an toàn nhờ builtin_gate md5_verify_fixed_fileid + guard BUNDLE_META (ADR-0001), không nhờ journal",
        "resume_behavior": "chạy lại CÙNG LỆNH — upload lại cùng bytes idempotent theo md5 verify sau push",
        "duplicate_guard": "BLOCKED_BY_BUNDLE_META khi cây là bundle fork (--force thoát, ADR-0001); fileId cố định nên không sinh file mới",
        "readback_command": "gws files get <file_id> (md5Checksum khớp local) / curl public download + so SHA256 với zip local",
        "resume_command": "drive-push <zip> --via auto --rename-to-file",
        "rollback_hint": "Drive version history của fileId (Manage versions) hoặc re-push zip bản trước — fileId không đổi",
    },
    "shared_source_fix": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "sha256(tập nhóm shared + winner được chọn) — plan/report trước, apply theo plan",
        "journal_key": "tl_journal/shared-source-fix_<run_id> (groups + before per-loser)",
        "resume_behavior": "chạy lại CÙNG LỆNH — loser đã clear bị bỏ qua (reg_clear idempotent theo trạng thái đích)",
        "duplicate_guard": "DRY/report mặc định; --apply đòi --confirm yes (gỡ link NLM = destructive); verify nlm-content xem source THỰC thuộc bản nào TRƯỚC apply",
        "readback_command": "reg-query từng drive_id trong nhóm --json (chỉ winner còn nlm_source_id)",
        "resume_command": "shared-source-fix [notebook_id] --apply --confirm yes",
        "rollback_hint": "undo <run_id> --apply (before per-loser trong journal) — chỉ khôi phục cột link registry, không đụng NLM",
    },
    "source_update_corpus": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "drive_id+corpus_đích (true/false — set lại cùng giá trị vô hại)",
        "journal_key": "tl_journal/source-update-corpus_<run_id> (before row + ref_clear nếu có)",
        "resume_behavior": "chạy lại CÙNG LỆNH — trạng thái đích đã đạt → ghi lại cùng giá trị, vô hại",
        "duplicate_guard": "DRY mặc định; --apply đòi --confirm yes; GUARD shared_source_id + clear refs nlm_source_id/nlm_notebook_id khi corpus=false",
        "readback_command": "reg-query --drive-id <id> --json (corpus + nlm_status đúng đích)",
        "resume_command": "source-update-corpus <target> <status> --apply --confirm yes",
        "rollback_hint": "undo <run_id> --apply (before row) hoặc chạy lại với giá trị corpus ngược",
    },
    "verify_staged": {   # r200 staged lane (grill 24-07 C4/C5)
        "schema": "idempotency_contract.v1",
        "idempotency_key": "drive_id+verdict — PASS đã flip thì note hết staged:* nên RA KHỎI tập dò; FAIL ghi lại cùng note vô hại",
        "journal_key": "tl_journal/verify-staged_<run_id> (before corpus+note TỪNG dòng cả lô)",
        "resume_behavior": "chạy lại CÙNG LỆNH — tập dò tự thu hẹp theo note staged:* (parity đo lại từ đầu, không tin kết quả dở)",
        "duplicate_guard": "DRY mặc định; --apply đòi --confirm yes; CHỈ đụng dòng note staged:* trong scope profile",
        "readback_command": "reg-query --drive-id <id> --json (corpus + note đúng đích)",
        "resume_command": "verify-staged --apply --confirm yes",
        "rollback_hint": "undo <run_id> --apply (before corpus+note cả lô)",
    },
})

# v1.34.56 (A-#12 — kế hoạch 13-vấn-đề 2026-07-16): contract cho lệnh mới nlm-source-remove (gỡ nguồn
# KHỎI notebook NLM, KHÔNG trash Drive/đụng dòng registry — wrapper ngữ nghĩa của `nlm source delete`).
_IDEMPOTENCY_CONTRACTS.update({
    "nlm_source_remove": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "source_id (sid toàn cục — gỡ khỏi notebook, không cần notebook-id)",
        "journal_key": "tl_journal/nlm-source-remove_<run_id> (intent nlm_source_delete irreversible per-sid)",
        "resume_behavior": "chạy lại CÙNG LỆNH — sid đã gỡ trả deleted_count=0/not-found → noop OK (idempotent theo trạng thái đích, không FAIL)",
        "duplicate_guard": "DRY mặc định + --confirm yes; GUARD POINTER_STILL_ATTACHED (manifest + reg_get authoritative fail-closed) chặn sid còn con trỏ registry — --force thoát",
        "readback_command": "nlm-list <nb> --json (sid không còn) + reg-query --json (không dòng nào trỏ sid)",
        "resume_command": "nlm-source-remove <sid...> --apply --confirm yes",
        "rollback_hint": "KHÔNG tự động: nguồn chỉ bị gỡ khỏi notebook (file Drive còn nguyên) — nlm-add --drive-id lại rồi nlm-reconcile link",
    },
    # v1.34.57 (B-#4..#7 — kế hoạch 13-vấn-đề Q6=a/Q7=a): contract cho lệnh di dời physical-first.
    "nlm_migrate": {
        "schema": "idempotency_contract.v1",
        "idempotency_key": "drive_id+notebook_đích (re-plan physical-first mỗi lần chạy — lặp lại vô hại)",
        "journal_key": "tl_journal/nlm-migrate_<run_id> (intent reg_upsert per-doc kèm before nb/sid THẬT)",
        "resume_behavior": "chạy lại CÙNG LỆNH — plan tái tạo từ VẬT LÝ đích (luôn list tươi): đã xong → POINTER_OK; dán link xong → ADD tự chuyển REPOINT (harvest, không state file)",
        "duplicate_guard": "DRY mặc định + --confirm yes; đích LUÔN list tươi; ADD qua cmd_nlm_add (claim F-04 + dedup-gate + verify-then-link); repoint idempotent (ghi lại cùng giá trị vô hại); KHÔNG tự gỡ nguồn cũ (Q7 — chỉ in nlm-source-remove)",
        "readback_command": "reg_get_bulk verify CUỐI ngay trong lệnh (so nb+sid) + nlm-audit-physical / reg-query --drive-id <id> --json",
        "resume_command": "nlm-migrate --to <nb> (--name-contains X | --cat NN | --drive-ids f) --apply --confirm yes",
        "rollback_hint": "undo <run_id> --apply (journal before nb/sid per-doc); nguồn đã add trên đích gỡ bằng nlm-source-remove <sid> --apply --confirm yes",
    },
})



def _workflow_dir() -> Path:
    return HERE.parent / "references" / "workflows"


def _workflow_card_files() -> list[Path]:
    return [p for p in sorted(_workflow_dir().glob("*.json")) if not p.name.endswith(".schema.json")]


def _load_workflow_card(wid: str) -> dict:
    path = _workflow_dir() / f"{wid}.json"
    if not path.exists():
        return {"id": wid, "ok": False, "error": "WORKFLOW_CARD_NOT_FOUND", "path": str(path)}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        data.setdefault("ok", True)
        data.setdefault("path", str(path))
        return data
    except Exception as e:
        return {"id": wid, "ok": False, "error": f"WORKFLOW_CARD_INVALID:{type(e).__name__}", "path": str(path)}


def cmd_tool_inventory(a) -> int:
    commands_available = _available_commands_from_parser()
    cmd_set = set(commands_available)
    groups = []
    for name, meta in _TOOL_GROUPS.items():
        cmds = _unique_preserve_order(meta.get("commands", []))
        groups.append({
            "name": name,
            "title": meta.get("title", name),
            "purpose": meta.get("purpose", ""),
            "commands": cmds,
            "available_commands": [c for c in cmds if (c.split() or [""])[0] in cmd_set],
            "missing_commands": [c for c in cmds if (c.split() or [""])[0] not in cmd_set],
            "planned_commands": list(meta.get("planned_commands", [])),
        })
    task = (getattr(a, "task", None) or "").strip().lower().replace(" ", "_").replace("-", "_")
    group = (getattr(a, "group", None) or "").strip().lower().replace(" ", "_").replace("-", "_")
    if task:
        wf_id = _TASK_TO_WORKFLOW.get(task, task)
        card = _load_workflow_card(wf_id)
        out = {
            "ok": bool(card.get("ok", True)),
            "mode": "task",
            "task": task,
            "workflow_id": wf_id,
            "workflow": card,
            "do_not_write_new_tool_until_checked": True,
            "inventory_hint": "Nếu workflow báo thiếu capability, ưu tiên mở rộng lệnh hiện có trước khi viết tool mới.",
        }
    else:
        if group:
            groups = [g for g in groups if g["name"] == group or group in g["name"]]
        missing = []
        for g in groups:
            for planned in g.get("planned_commands", []):
                missing.append({"capability": planned, "group": g["name"], "status": "planned_not_implemented", "recommendation": "Dùng route-task/dry-run trước khi triển khai."})
        out = {
            "ok": True,
            "schema": "tool_inventory.v1",
            "groups": groups,
            "commands_available": commands_available,
            "scripts": _script_docstrings() if getattr(a, "scripts", False) else [],
            "workflow_cards": sorted(p.stem for p in _workflow_card_files()),
            "missing_capabilities": missing,
        }
    try:   # v1.33.58 (Pha E - E3): inventory đọc metadata chuẩn từ registry thay vì tự scan rời rạc
        import tl_core.command_registry as _reg
        out["registry"] = _reg.registry_summary()
    except Exception as _e:  # noqa: BLE001
        out["registry"] = {"ok": False, "error": type(_e).__name__ + ": " + str(_e)}
    _print_json_or_text(out, getattr(a, "json", False))
    return 0 if out.get("ok", True) else 2


def cmd_registry_coverage(a, tl_module=None) -> int:
    """READ-ONLY: báo cáo độ phủ hai chiều cây lệnh parser ↔ command registry (Packet AG-T0-03)."""
    import tl_core.command_registry as _reg
    parser = build_parser()
    strict = getattr(a, "strict", False)
    unreg_only = getattr(a, "unregistered_only", False)
    as_json = getattr(a, "json", False)

    report = _reg.compute_parser_coverage(parser, tl_module=tl_module or _TL, strict=strict, unregistered_only=unreg_only)

    if as_json:
        _print_json_or_text(report, True)
    else:
        summ = report["summary"]
        print(f"=== Argparse Parser-Tree Coverage (Schema: {report['schema']}) ===")
        print(f"Total Nodes: {summ['total_nodes']} (Containers: {summ['container_commands']}, Leaf Commands: {summ['total_leaf_commands']})")
        print(f"Registered Leaf Commands: {summ['registered_leaf_commands']} / {summ['total_leaf_commands']} ({summ['coverage_percent']}%)")
        print(f"Unregistered Leaf Commands: {summ['unregistered_leaf_commands']}")
        print(f"High-Risk Unregistered Commands: {summ['high_risk_unregistered_count']}")
        print(f"Registry Orphaned Commands: {summ['registry_orphaned_commands']}")
        print()
        if report["categories"]["unregistered"]:
            print(f"Unregistered Commands ({len(report['categories']['unregistered'])}):")
            for u in report["categories"]["unregistered"]:
                hr = " [HIGH-RISK]" if u in report["categories"]["high_risk_unregistered"] else ""
                print(f"  - {u}{hr}")
            print()
        if report["categories"]["registry_not_in_parser"]:
            print(f"Registry Commands Missing from Parser ({len(report['categories']['registry_not_in_parser'])}):")
            for o in report["categories"]["registry_not_in_parser"]:
                print(f"  - {o}")
            print()
        if not report["ok"]:
            print("STATUS: FAILED (strict mode violation: unregistered or orphaned commands detected)")
        else:
            print("STATUS: OK")

    return 0 if report.get("ok", True) else 1


def cmd_route_task(a) -> int:
    # v1.33.54 (merge determinism-53): nhận task ở CẢ positional lẫn --task — bundle bắt buộc --task làm gãy
    # cách gọi `route-task ingest_local` trong doc/log cũ (cùng lớp ma sát S8/A1: drift doc↔CLI).
    raw = ((getattr(a, "task", "") or "") or (getattr(a, "task_pos", "") or "")).strip()
    if not raw:
        print(json.dumps({"ok": False, "error": "MISSING_TASK",
                          "fix": "truyền tên tác vụ: `tl route-task <task>` hoặc `tl route-task --task <task>`"},
                         ensure_ascii=False), file=sys.stderr)
        return 2
    key = raw.lower().replace(" ", "_").replace("-", "_")
    wf_id = _TASK_TO_WORKFLOW.get(key, key)
    card = _load_workflow_card(wf_id)
    risk = card.get("risk", "unknown") if card.get("ok", True) else "unknown"
    card_recommended = _unique_preserve_order(card.get("recommended_commands", []) if isinstance(card.get("recommended_commands"), list) else [])
    recommended = list(card_recommended)
    if not recommended:
        for g in _TOOL_GROUPS.values():
            for cmd in _unique_preserve_order(g.get("commands", [])):
                # fallback hints for older workflow cards without recommended_commands
                if wf_id.startswith("nlm") and cmd.startswith("nlm"):
                    recommended.append(cmd)
                elif wf_id.startswith("ocr") and (cmd.split()[0] in {"ocr-analyze", "ocr-run", "ocr-verify", "ingest-ocr", "profile-ingest-ocr", "source-verify"} or "profile-ingest" in cmd):
                    recommended.append(cmd)
                elif wf_id.startswith("ingest") and (cmd.startswith("ingest") or cmd.startswith("profile-ingest") or cmd == "external-ingest"):
                    recommended.append(cmd)
                elif wf_id.startswith("convert") and (cmd in {"ingest-local", "profile-ingest", "external-ingest", "convert-verify"}):
                    recommended.append(cmd)
                elif (wf_id.startswith("large_doc") or wf_id.startswith("chunk_ingest")) and (cmd in {"chunk-plan", "chunk-apply", "chunk-verify", "profile-ingest-chunks", "profile-ingest", "nlm-query", "nlm-content"}):
                    recommended.append(cmd)
        if wf_id == "write_new_tool":
            recommended = ["tool-inventory --json", "route-task --task <task> --json", "edit-skill", "workflow-audit --json", "release-check --json"]
    out = {
        "ok": bool(card.get("ok", True)),
        "schema": "route_task.v1",
        "task": raw,
        "workflow_id": wf_id,
        "risk": risk,
        "workflow": card,
        "recommended_commands": _unique_preserve_order(recommended),
        "requires_dry_run": risk in {"medium", "high"},
        "requires_apply": risk in {"medium", "high"},
        "requires_readback": risk == "high" or wf_id in {"convert_rename", "ingest_local", "ingest_zip", "ocr_ingest", "chunk_ingest"},
        "stop_conditions": card.get("stop_conditions", []),
        "idempotency": _idempotency_contract_for_workflow(wf_id),
        "idempotency_key": (_idempotency_contract_for_workflow(wf_id) or {}).get("idempotency_key"),
        "resume_command": (_idempotency_contract_for_workflow(wf_id) or {}).get("resume_command"),
        "readback_command": (_idempotency_contract_for_workflow(wf_id) or {}).get("readback_command"),
        "rollback_hint": (_idempotency_contract_for_workflow(wf_id) or {}).get("rollback_hint"),
        "note": "Đây là router READ-ONLY. Không ghi Drive/registry/NLM. Dùng để chọn workflow trước khi thực thi.",
    }
    _print_json_or_text(out, getattr(a, "json", False))
    return 0 if out.get("ok", True) else 2

# ───────────────────────── deterministic release/audit helpers (stage5) ─────────────────────────
_WORKFLOW_CARD_SCHEMA = "workflow_card.v1"

_WORKFLOW_REQUIRED_FIELDS = {
    "schema", "id", "title", "risk", "plan", "write_scope",
    "dry_run_required", "confirm_required", "readback_required", "rollback_required", "live_state_required",
    "volatile_fields",
}

_WORKFLOW_BOOL_FIELDS = {"dry_run_required", "confirm_required", "readback_required", "rollback_required", "live_state_required"}

_WORKFLOW_RISKS = {"low", "medium", "high"}


def _workflow_cards_audit() -> dict:
    """Audit workflow cards and command references. Pure/read-only; catches drift between prose, router and CLI."""
    cards = []
    errors = []
    warnings = []
    available = set(_available_commands_from_parser())
    for fp in _workflow_card_files():
        try:
            obj = json.loads(fp.read_text(encoding="utf-8", errors="replace"))
        except Exception as e:  # noqa: BLE001
            errors.append({"file": str(fp), "error": f"JSON_INVALID:{type(e).__name__}:{e}"})
            continue
        missing = sorted(_WORKFLOW_REQUIRED_FIELDS - set(obj.keys()))
        if missing:
            errors.append({"file": str(fp), "id": obj.get("id"), "error": "MISSING_REQUIRED_FIELDS", "missing": missing})
        if obj.get("schema") != _WORKFLOW_CARD_SCHEMA:
            errors.append({"file": str(fp), "id": obj.get("id") or fp.stem, "error": "WORKFLOW_SCHEMA_MISMATCH", "expected": _WORKFLOW_CARD_SCHEMA, "actual": obj.get("schema")})
        if obj.get("id") and obj.get("id") != fp.stem:
            warnings.append({"file": str(fp), "warning": "ID_DIFFERS_FROM_FILENAME", "id": obj.get("id"), "filename": fp.stem})
        risk = str(obj.get("risk") or "").lower()
        if risk not in _WORKFLOW_RISKS:
            errors.append({"file": str(fp), "id": obj.get("id") or fp.stem, "error": "INVALID_RISK", "risk": obj.get("risk")})
        if not isinstance(obj.get("plan"), list) or not obj.get("plan"):
            errors.append({"file": str(fp), "id": obj.get("id") or fp.stem, "error": "PLAN_MUST_BE_NONEMPTY_LIST"})
        for b in sorted(_WORKFLOW_BOOL_FIELDS):
            if b in obj and not isinstance(obj.get(b), bool):
                errors.append({"file": str(fp), "id": obj.get("id") or fp.stem, "error": "CONTRACT_FIELD_MUST_BE_BOOL", "field": b})
        if "write_scope" in obj and not str(obj.get("write_scope") or "").strip():
            errors.append({"file": str(fp), "id": obj.get("id") or fp.stem, "error": "WRITE_SCOPE_EMPTY"})
        if "volatile_fields" in obj and not isinstance(obj.get("volatile_fields"), list):
            errors.append({"file": str(fp), "id": obj.get("id") or fp.stem, "error": "VOLATILE_FIELDS_MUST_BE_LIST"})
        rec = []
        rec_missing = []
        for cmd in obj.get("recommended_commands", []) or []:
            token = (str(cmd).split() or [""])[0]
            rec.append({"command": cmd, "available": token in available})
            if token not in available:
                rec_missing.append(cmd)
                warnings.append({"file": str(fp), "warning": "RECOMMENDED_COMMAND_NOT_AVAILABLE", "command": cmd})
        if risk in {"medium", "high"}:
            if not rec:
                errors.append({"file": str(fp), "id": obj.get("id") or fp.stem, "error": "RISKY_WORKFLOW_MISSING_RECOMMENDED_COMMANDS"})
            if rec_missing:
                errors.append({"file": str(fp), "id": obj.get("id") or fp.stem, "error": "RISKY_WORKFLOW_RECOMMENDS_MISSING_COMMAND", "commands": rec_missing})
            for field in ("verify", "stop_conditions"):
                if not isinstance(obj.get(field), list) or not obj.get(field):
                    errors.append({"file": str(fp), "id": obj.get("id") or fp.stem, "error": "RISKY_WORKFLOW_MISSING_NONEMPTY_LIST", "field": field})
        if risk == "high":
            if str(obj.get("write_scope") or "none") == "none":
                errors.append({"file": str(fp), "id": obj.get("id") or fp.stem, "error": "HIGH_RISK_WRITE_SCOPE_MUST_BE_EXPLICIT"})
            if not obj.get("dry_run_required") and not obj.get("confirm_required"):
                warnings.append({"file": str(fp), "id": obj.get("id") or fp.stem, "warning": "HIGH_RISK_WITHOUT_DRY_RUN_OR_CONFIRM_FLAG"})
            if not obj.get("readback_required"):
                warnings.append({"file": str(fp), "id": obj.get("id") or fp.stem, "warning": "HIGH_RISK_WITHOUT_READBACK_FLAG"})
        cards.append({
            "file": str(fp),
            "id": obj.get("id") or fp.stem,
            "schema": obj.get("schema"),
            "risk": obj.get("risk"),
            "write_scope": obj.get("write_scope"),
            "contract": {k: obj.get(k) for k in sorted(_WORKFLOW_BOOL_FIELDS)},
            "volatile_fields": obj.get("volatile_fields", []),
            "recommended": rec,
        })
    card_ids = {c["id"] for c in cards}
    for task, wf_id in sorted(_TASK_TO_WORKFLOW.items()):
        if wf_id not in card_ids:
            errors.append({"task": task, "workflow_id": wf_id, "error": "TASK_MAP_POINTS_TO_MISSING_WORKFLOW_CARD"})
    groups = []
    for gname, meta in _TOOL_GROUPS.items():
        missing = []
        raw_cmds = list(meta.get("commands", []) or [])
        duplicate_cmds = sorted({cmd for cmd in raw_cmds if raw_cmds.count(cmd) > 1})
        if duplicate_cmds:
            warnings.append({"group": gname, "warning": "GROUP_COMMAND_DUPLICATE", "commands": duplicate_cmds})
        for cmd in _unique_preserve_order(raw_cmds):
            token = (str(cmd).split() or [""])[0]
            if token not in available:
                missing.append(cmd)
        groups.append({"name": gname, "missing_commands": missing, "command_count": len(_unique_preserve_order(raw_cmds))})
        # Commands listed as planned are allowed to be missing; commands in commands should exist.
        for cmd in missing:
            warnings.append({"group": gname, "warning": "GROUP_COMMAND_NOT_AVAILABLE", "command": cmd})
    ok = not errors
    return {"ok": ok, "schema": "workflow_audit.v2", "card_schema": _WORKFLOW_CARD_SCHEMA, "cards": cards, "groups": groups, "errors": errors, "warnings": warnings,
            "summary": {"cards": len(cards), "tasks": len(_TASK_TO_WORKFLOW), "groups": len(_TOOL_GROUPS), "available_commands": len(available)}}


def _kernel_size_findings(size_bytes: int, *, warn_limit: int = 47 * 1024, fail_limit: int = 48 * 1024) -> dict:
    """PURE (G1a v1.34.66 — §11 kế hoạch guard-va-boc-tl-core, khuôn WARN/FAIL của §3): kernel SKILL.md
    là trần SÁT NHẤT toàn hệ (49.145/49.152B — đệm 7B); gate cũ CHỈ FAIL ≤48K, KHÔNG WARN. WARN >47KB
    advisory (KHÔNG vào out["warnings"] — strict không fail vì đệm; tín hiệu sớm cho kernel-diet G1b);
    FAIL >48KB GIỮ NGUYÊN ngữ nghĩa cũ (chặn cả hai mode qua size_ok)."""
    b = int(size_bytes or 0)
    return {"size_bytes": b, "size_limit": fail_limit, "size_warn_limit": warn_limit,
            "size_ok": b <= fail_limit, "size_warn": b > warn_limit}


def _py_size_findings(sizes: dict, *, warn_limit: int = 280 * 1024, fail_limit: int = 320 * 1024,
                      waiver: tuple = ("tl_selftest.py",)) -> dict:
    """PURE (ĐỢT A v1.34.64 — kế hoạch guard-va-boc-tl-core §3/Q1): guard TRẦN MOUNT ~343KB/file (lớp sự
    cố #5 — tl.py từng CẮT CỤT khi vượt; self-heal chỉ cứu NUL-pad, KHÔNG cứu cắt cụt). WARN >280KB
    (đệm ~60KB — vài release để xử lý); FAIL --strict >320KB (chặn release TRƯỚC vách — ép bóc trước
    cliff). WAIVER theo BASENAME: tl_selftest.py (936KB) — không bước runbook nào import nó trên Cowork;
    nếu hỏng → fail ỒN ÀO (không âm thầm); xét lại nếu có ngày selftest phải chạy trên Cowork."""
    warn, fail, waived = [], [], []
    for p in sorted(sizes):
        b = int(sizes[p] or 0)
        if p.replace("\\", "/").rsplit("/", 1)[-1] in waiver:
            waived.append(p)
            continue
        if b > warn_limit:
            warn.append({"path": p, "bytes": b})
        if b > fail_limit:
            fail.append({"path": p, "bytes": b})
    return {"warn_limit": warn_limit, "fail_limit": fail_limit, "files_scanned": len(sizes),
            "warn": warn, "fail": fail, "waived": waived, "size_ok": not fail}


def cmd_workflow_audit(a) -> int:
    out = _workflow_cards_audit()
    # v1.33.58 (Pha E - E4): đối chiếu command registry <-> parser <-> cards <-> idempotency contracts.
    try:
        import tl_core.command_registry as _reg
        _rv = _reg.validate_registry(build_parser(), _TL, load_card=_load_workflow_card,
                                     contracts=_IDEMPOTENCY_CONTRACTS)
        out["registry"] = _rv
        out["ok"] = bool(out.get("ok")) and bool(_rv.get("ok"))
        # warnings registry (grandfather legacy) là ADVISORY — giữ trong out["registry"]["warnings"],
        # KHÔNG merge vào out["warnings"] để --strict không fail vì nợ đã biết (mục tiêu Pha G siết dần).
    except Exception as _e:  # noqa: BLE001
        out["registry"] = {"ok": False, "issues": ["REGISTRY_VALIDATE_CRASH:" + type(_e).__name__ + ":" + str(_e)]}
        out["ok"] = False
    # v1.34.0 (Pha F — chống-phình kernel): SKILL.md phải ≤ 48KB và mọi đường references/ nhắc trong
    # kernel phải tồn tại (kernel = bất biến + con trỏ; con trỏ gãy/kernel phình = doctrine-drift).
    try:
        _sk = HERE.parent / "SKILL.md"
        _sk_b = _sk.read_bytes()
        _links = sorted({m.rstrip(".,;:)]}»") for m in re.findall(r"references/[A-Za-z0-9_./\-]+", _sk_b.decode("utf-8", "replace"))})
        _missing = [l for l in _links if "*" not in l and not (HERE.parent / l).exists()]
        # G1a v1.34.66: +WARN 47KB qua helper PURE (khuôn §3 — advisory, không đổi ngữ nghĩa FAIL 48K)
        out["kernel"] = {**_kernel_size_findings(len(_sk_b)),
                         "links_checked": len(_links), "links_missing": _missing, "links_ok": not _missing}
        out["ok"] = bool(out.get("ok")) and out["kernel"]["size_ok"] and out["kernel"]["links_ok"]
    except Exception as _ke:  # noqa: BLE001
        out["kernel"] = {"ok": False, "error": f"{type(_ke).__name__}: {_ke}"}
        out["ok"] = False
    # ĐỢT A v1.34.64 (kế hoạch guard-va-boc-tl-core §3): guard size .py RUNTIME bundle (scripts/ +
    # tl_core/ + _fallback/) — WARN >280KB advisory (KHÔNG merge vào out["warnings"], tiền lệ
    # registry-warnings :679 để --strict không fail vì đệm); FAIL >320KB chỉ chặn ở --strict.
    try:
        _pyfiles = {}
        for _d, _pref in ((HERE, "scripts"), (HERE / "tl_core", "scripts/tl_core"),
                          (HERE / "_fallback", "scripts/_fallback")):
            if _d.is_dir():
                for _f in sorted(_d.glob("*.py")):
                    _pyfiles[f"{_pref}/{_f.name}"] = _f.stat().st_size
        out["py_size"] = dict(_py_size_findings(_pyfiles),
                              basis="trần mount ~343KB/file (lớp sự cố #5 cắt cụt); WARN=đệm advisory, "
                                    "FAIL chỉ chặn --strict; waiver tl_selftest.py (không import trên Cowork)")
    except Exception as _pe:  # noqa: BLE001
        out["py_size"] = {"size_ok": False, "error": f"{type(_pe).__name__}: {_pe}"}
        out["ok"] = False
    if getattr(a, "strict", False):
        out["strict"] = True
        out["ok"] = (bool(out.get("ok")) and not out.get("warnings")
                     and bool((out.get("py_size") or {}).get("size_ok")))
    _print_json_or_text(out, getattr(a, "json", False))
    return 0 if out.get("ok") else 2


# ───────────────────────── r218: doc-claims-check (kiểm TRÍCH DẪN cơ học trong văn xuôi) ─────────────────────────
# Lỗ hổng đã ĐO 2026-07-28: gate 9 bước kiểm mã nguồn + manifest + bundle, KHÔNG bước nào kiểm tính đúng
# của trích dẫn trong tài liệu. Trong khi CHANGELOG/GOTCHAS/RUNBOOK/DOCTRINE_APPENDIX dày đặc `r216`,
# `9279426`, `tl.py:1504`, `references/X.md`, `v1.35.52`. Khuôn hỏng đã trả giá: doc dẫn tệp–cờ–số hiệu
# đã đổi chỗ, không ai phát hiện tới khi một phiên sau đi theo và lạc.
#
# READ-ONLY tuyệt đối: không ghi (trừ --out do người gọi chỉ định), không mạng, không GAS/NLM, không --fix.
# Cờ là ĐẦU VÀO ĐỂ PHÂN XỬ, không phải phán quyết ⇒ mặc định rc=1 (không fail); --strict mới đẩy 1→2.
_DOC_CLAIMS_SCHEMA = "doc_claims_check.v1"
# r264: +`docs` — trước đây `docs/` (19 tệp: 16 ADR + audit + 2 kế hoạch rà soát) KHÔNG được phủ, nên
# con trỏ chết ở đó KHÔNG cổng nào bắt. Đo khi mở: 18/19 tệp SẠCH tuyệt đối; 12 cờ còn lại dồn hết vào
# MỘT tệp và là NỘI DUNG của nó, không phải lỗi (xem _DOC_CLAIMS_HISTORICAL).
_DOC_CLAIMS_DEFAULT_PATHS = ("CHANGELOG.md", "SKILL.md", "CLAUDE.md", "CONTEXT.md", "references", "docs")
# r219 mở thêm L8 (tên lệnh `tl <cmd>` không tồn tại) + L9 (tài liệu mồ côi); r220 trả nốt L4.
# Hai đề xuất lịch sử L10/L11 đã ĐO và BỊ BÁC (xem `_DOC_CLAIMS_BAC_L10_L11`). F1-02 dùng L12 cho
# test-ID pointer vì đây là invariant mới, không hồi sinh hai lớp đã bác.
_DOC_CLAIMS_LAYERS = ("L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9", "L12")
# §2.2 nói thẳng: «tài liệu lịch sử được phép dẫn tệp đã xoá». Ba nguồn dưới đây GHI LẠI QUÁ KHỨ, không
# phải con trỏ để đi theo — DOCTRINE_APPENDIX tự khai «TOÀN BỘ thân SKILL.md trước refactor v1.16.0,
# GIỮ NGUYÊN để tra cứu lý do», changelog thì theo định nghĩa là sổ. Đo 28-07: 127/134 cờ L1 nằm ở đúng
# ba chỗ này; không hạ cấp thì 8 phát hiện SỐNG bị chôn dưới 127 mục không ai sửa được (sửa sổ = viết
# lại lịch sử). Phân định theo LOẠI TÀI LIỆU, không theo tuổi của tệp bị dẫn — git ở kho này chỉ có 265
# commit trong khi skill già hơn thế, nên `--diff-filter=D` không phân định nổi.
# r264: +`docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md`. Tệp này là bản KIỂM KÊ CON-TRỎ-CHẾT: nó nêu
# `scripts/nlm_log.py` · `build_parts.py` · `tl_rebuild.sh` · `templates/_nguon-goc/` · `manifest_build.py`
# CHÍNH VÌ chúng không tồn tại, và tự khai bằng chứng «`git log --all --diff-filter=ADR` RỖNG → chưa từng
# tồn tại». Các đường dẫn đó là PHÁT HIỆN của tài liệu, không phải con trỏ để đi theo — đúng định nghĩa
# §2.2 đã áp cho CHANGELOG/DOCTRINE_APPENDIX. Không hạ cấp thì 11 cờ này chặn gate vĩnh viễn và cách chữa
# duy nhất là XOÁ nội dung phát hiện — tức phá tài liệu để làm vui lòng bộ kiểm.
_DOC_CLAIMS_HISTORICAL = ("CHANGELOG.md", "references/changelog_archive/",
                          "references/DOCTRINE_APPENDIX.md",
                          "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
                          # r289/Q2 (user chốt 01-08): cả HAI tài liệu kế hoạch chuyển LƯU TRỮ. Chúng tự khai
                          # ở dòng đầu; đường dẫn/lệnh trong thân là PHÁT HIỆN của tài liệu (tệp đã chết,
                          # lệnh đã đổi tên), KHÔNG phải con trỏ để đi theo. Nguồn sự thật VẬN HÀNH đã dời
                          # sang `references/RASOAT_HOSO_LOOP.md` + `RASOAT_PLAN_SCHEMA.md` + thẻ rasoat_hoso.
                          "docs/WORKFLOW_RASOAT_TU_DONG.md")
_DOC_CLAIMS_FIXTURES = "references/golden/fixtures/"


def _doc_claims_is_historical(rel: str) -> bool:
    """wp1121 (#1121 F2) — mục `_DOC_CLAIMS_HISTORICAL` kết thúc `/` là TIỀN TỐ THƯ MỤC, mục còn lại là TÊN
    TỆP so BẰNG. Trước đây `rel.startswith(tuple)` nên `CHANGELOG.md.live.md` hay
    `references/DOCTRINE_APPENDIX.md.live.md` cũng được miễn như tài liệu lịch sử ở MỌI lớp (L1/L2/L4/L8/L12 qua
    `historical`, L9 qua nguồn trỏ). Đo trên `git ls-files` base `f4b513d`: 0 tệp đổi phân loại, 6 tệp lịch sử."""
    return any(rel.startswith(h) if h.endswith("/") else rel == h for h in _DOC_CLAIMS_HISTORICAL)
# §2.4 che nhiễu: token mang các ký tự này là GIÀN GIÁO/placeholder, không phải trích dẫn thật.
_DOC_CLAIMS_NOISE_CHARS = "<>{}*$"
_DOC_CLAIMS_NOISE_SUBSTR = ("path/to", "...", "…")

# ── r219: L8 — tên lệnh `tl <cmd>`. Nguồn sự thật = golden `parser_surface.json` (repo-local, tất
# định, đã bị `golden-test` khoá byte) chứ KHÔNG import `build_parser`: doctrine false-green-test-qua-bind
# nói thẳng rằng đọc qua đường đã bind không chứng minh gì, và import tl.py trong handler kéo theo
# `load_creds` — thứ mà lệnh READ-ONLY offline này cố ý không đụng. Thiếu tệp ⇒ BỎ QUA lớp và KHAI BÁO,
# không được đoán (hô sai tên lệnh là đúng loại lỗi lệnh này sinh ra để chặn).
_DOC_CLAIMS_PARSER_SURFACE = "references/golden/parser_surface.json"
_DOC_CLAIMS_TL_HEADS = ("python", "python3", "py")
_DOC_CLAIMS_CMD_RE = re.compile(r"^[a-z][a-z0-9\-]{2,}$")
# Option TOÀN CỤC ăn theo một giá trị — không nuốt thì `tl --profile P sweep` đọc ra lệnh «P».
_DOC_CLAIMS_GLOBAL_OPT_VAL = ("--profile", "--config")

# ── r219: L9 — tài liệu mồ côi. Chỉ chạy khi lượt quét ĐỦ RỘNG (xem `_doc_claims_orphan_scope`).
_DOC_CLAIMS_ORPHAN_DIR = "references/"
_DOC_CLAIMS_ORPHAN_EXTRA = (("scripts", "*.py"), ("scripts/tl_core", "*.py"),
                            ("scripts/_fallback", "*.py"), ("references/workflows", "*.json"),
                            ("docs/adr", "*.md"), (".", "*.md"))

# ── r220: L4 — giàn giáo nháp còn sót trong VĂN XUÔI ({{...}}, TODO/TBD/FIXME, XXX). Quét trên
# `nospan`: marker nằm trong fence/span là VÍ DỤ hay ký pháp đang được MÔ TẢ, không phải trạng thái
# của chính tài liệu. ★ĐO 2026-07-28 TRƯỚC KHI THIẾT KẾ (đúng khuôn đã bác L10/L11): 12/12 hit
# `XXX` toàn kho là placeholder cơ-quan-ban-hành trong KÝ PHÁP số hiệu `NN-YYYY-VBHN-XXX` — kề
# dấu '-' ⇒ mảnh của định danh dài, KHÔNG phải giàn giáo (cùng phép loại trừ kề '-' mà L2 dùng
# cho khúc UUID notebook). Sau loại trừ: 0 hit sống toàn kho; hit TODO duy nhất nằm ở
# DOCTRINE_APPENDIX (lịch sử, ghi chép cố ý lưu) ⇒ advisory. Lớp vào kho là XANH SẴN, khuôn L8/L9.
_DOC_CLAIMS_L4_MUSTACHE_RE = re.compile(r"\{\{[^{}\n]*\}\}")
_DOC_CLAIMS_L4_WORD_RE = re.compile(r"\b(?:TODO|TBD|FIXME|XXX)\b")

# ══ ĐO 2026-07-28 (r219) — VÌ SAO L10 VÀ L11 KHÔNG ĐƯỢC LÀM ═════════════════════════════════════
# Kế hoạch r218 xếp L11 vào «hai lớp đáng nhất». Đo trên kho thật thì cả hai đều hô ~100% báo giả,
# nên làm chúng là làm hỏng chính cái khiến báo cáo dùng được (ranh giới cờ-vs-advisory).
#
# L11 «số hiệu VBQPPL thiếu NĂM»: 20 hit / 5 tệp, trong đó 18 ở tài liệu LỊCH SỬ và ĐÚNG 2 ở tài
#   liệu sống — cả 2 đều VIẾT ĐÚNG. `62/VBHN-VPQH` (SKILL.md) là số hiệu CHÍNH THỨC in trên văn bản;
#   `88/VBHN-VPQH` (COMMANDS.md) nằm trong câu đang MÔ TẢ việc v1.33.47 cố ý chấp nhận dạng bare.
#   Bất biến «phải có NĂM» áp cho KHOÁ REGISTRY (`NN-YYYY-VBHN-XXX`), không áp cho trích dẫn văn
#   xuôi — và mặt registry ĐÃ CÓ cổng riêng (`vbhn-year-fix`, VBHN_MINISTRY_YEAR_GUARD.md).
#   Bản thu hẹp «bare number ĐA NGHĨA» (89/VBHN-VPQH = Luật MTTQ 2025 hay Luật NSNN 2026?) thì cần
#   tra registry cache — máy-phụ-thuộc, phá tính tất định của golden ⇒ không thuộc lệnh này.
# L10 «GAS version thiếu `references/Code.<ver>.gs`»: 30 version được dẫn, chỉ 6 có tệp ⇒ 24 cờ.
#   Kho GIỮ 6 bản .gs gần nhất là CÓ CHỦ ĐÍCH; và chính việc viết `Code.<ver>.gs` vào tài liệu đã
#   làm guard con trỏ r209 ĐỎ (regex của nó cắt ở '<'). Lớp này sẽ đòi thêm rác để tự nó xanh.
_DOC_CLAIMS_BAC_L10_L11 = {
    "L10": "24/30 version GAS được dẫn không có tệp .gs — kho giữ 6 bản gần nhất là có chủ đích",
    "L11": "2/2 hit ở tài liệu sống đều viết ĐÚNG (số hiệu chính thức là dạng bare); bất biến "
           "NN-YYYY-VBHN-XXX áp cho khoá registry, đã có cổng vbhn-year-fix",
}


def _doc_claims_noisy(tok: str) -> bool:
    t = str(tok)
    return (any(c in t for c in _DOC_CLAIMS_NOISE_CHARS)
            or any(s in t for s in _DOC_CLAIMS_NOISE_SUBSTR))


def _doc_claims_tl_cmd(span_text: str):
    """r219/L8 — trả tên lệnh trong span dạng `tl <cmd> …`, hoặc None nếu span không phải câu lệnh.

    Phân tích theo TOKEN chứ không bằng một regex dài, vì ba ca dưới đây đã đo được và mỗi ca giết
    một cách viết regex khác nhau:
      • `tl nlm-*` (sổ lưu trữ) — regex tham lam trả về «nlm», một lệnh KHÔNG tồn tại ⇒ báo giả.
        Xét TRỌN token rồi lọc nhiễu (`*`) thì tự rụng.
      • `tl --profile "Luật BHXH" sweep` — không nuốt giá trị của option toàn cục thì đọc ra lệnh
        «Luật» hoặc «P».
      • văn xuôi tiếng Việt «`tl` cho phép…» — quét trần bắt 8 hit toàn báo giả; neo `tl` phải ở
        ĐẦU span mới loại được (đo: 8 → 4, và 4 còn lại đều nằm trong sổ lưu trữ).
    """
    toks = str(span_text).strip().split()
    if not toks:
        return None
    def _is_tl_py(t):
        return t.replace("\\", "/").rstrip(",;").endswith("scripts/tl.py")
    if toks[0] == "tl":
        i = 1
    elif len(toks) >= 2 and toks[0] in _DOC_CLAIMS_TL_HEADS and _is_tl_py(toks[1]):
        i = 2
    elif _is_tl_py(toks[0]):
        i = 1
    else:
        return None
    while i < len(toks) and toks[i].startswith("-"):
        i += 2 if (toks[i] in _DOC_CLAIMS_GLOBAL_OPT_VAL) else 1
    if i >= len(toks):
        return None                      # `tl --selftest`, `tl --version` — không có subcommand
    tok = toks[i].strip(_DOC_CLAIMS_TRIM)
    # CỐ Ý KHÔNG gọi thêm `_doc_claims_noisy(tok)` ở đây: phản chứng r219 (M3) chạy thật cho thấy nó
    # là MÃ CHẾT — `_DOC_CLAIMS_CMD_RE` chỉ nhận `[a-z][a-z0-9-]{2,}` nên mọi ký tự nhiễu `<>{}*$`,
    # `/`, `…` đã rụng trước; tắt bộ lọc nhiễu đi mà không test nào đỏ. Một chốt không đột biến nào
    # giết được là chốt CHƯA ĐƯỢC CHỨNG MINH, giữ lại chỉ tạo cảm giác an toàn giả. Cái gánh việc
    # thật là CMD_RE — và nó có phản chứng riêng (nới lớp ký tự ⇒ `tl nlm-*` nổ thành lệnh «nlm-*»).
    if not tok or not _DOC_CLAIMS_CMD_RE.match(tok):
        return None
    return tok


def _doc_claims_mask(text: str) -> tuple:
    """§2.4 — che nhiễu GIỮ NGUYÊN OFFSET (thay bằng dấu cách, chừa `\\n`) để số dòng báo cáo vẫn đúng.

    Trả (nofence, nofence_nospan):
      • nofence       — đã che khối fence ```/~~~ (L1/L3/L7 quét trên bản này: đường dẫn và
                        `tl.py:1504` VỐN nằm trong span backtick, che span đi là mù).
      • nofence_nospan— che thêm span backtick (L2/L5/L6 quét bản này: SHA/version/số hiệu đợt
                        trong ví dụ lệnh là MINH HOẠ, không phải khẳng định).
    Quét fence theo DÒNG (không regex đa dòng): fence lồng/không đóng vẫn cho kết quả xác định."""
    out, fence = [], None
    for ln in str(text).split("\n"):
        m = re.match(r"^(`{3,}|~{3,})", ln.lstrip())
        if fence is None:
            if m:
                fence = m.group(1)[0]
                out.append(" " * len(ln))
            else:
                out.append(ln)
        else:
            out.append(" " * len(ln))
            if m and m.group(1)[0] == fence:
                fence = None
    nofence = "\n".join(out)
    nospan = re.sub(r"`[^`\n]*`", lambda m: " " * len(m.group(0)), nofence)
    return nofence, nospan


def _doc_claims_linestarts(text: str) -> list:
    starts, pos = [0], 0
    for ln in str(text).split("\n"):
        pos += len(ln) + 1
        starts.append(pos)
    return starts


def _doc_claims_lineno(starts: list, offset: int) -> int:
    import bisect as _bs
    return max(1, _bs.bisect_right(starts, int(offset)))


def _doc_claims_rel(p, root) -> str:
    """Đường dẫn ỔN ĐỊNH cho JSON: repo-relative posix khi nằm trong cây, ngược lại absolute posix.
    (Tự relative hoá thay vì trông vào audit_projection — `roots`/`file` trong list không được scrub.)"""
    try:
        return Path(p).resolve().relative_to(Path(root).resolve()).as_posix()
    except Exception:  # noqa: BLE001
        return Path(p).as_posix()


def _doc_claims_targets(paths, root: Path) -> tuple:
    """Trả (files, roots_decl, errors). Thư mục → mọi *.md bên dưới; tệp → chính nó."""
    decl = [str(x) for x in (paths or [])] or list(_DOC_CLAIMS_DEFAULT_PATHS)
    files, errors, roots = [], [], []
    for raw in decl:
        p = Path(raw)
        if not p.is_absolute():
            p = root / raw
        roots.append(_doc_claims_rel(p, root))
        if p.is_dir():
            # BẪY TỰ GÂY: fixture golden nằm DƯỚI `references/` và CỐ TÌNH chứa trích dẫn chết (đó là
            # nội dung test). Quét mặc định mà nuốt chúng thì gate `--strict` không bao giờ xanh, và tệ
            # hơn: 8 phát hiện thật lẫn với dữ liệu test. Bỏ qua khi ĐI NGANG; vẫn quét khi người dùng
            # trỏ THẲNG vào đó (chính là cách case golden chạy).
            _skip = not _doc_claims_rel(p, root).startswith(_DOC_CLAIMS_FIXTURES)
            for f in sorted(p.rglob("*.md")):
                if _skip and _doc_claims_rel(f, root).startswith(_DOC_CLAIMS_FIXTURES):
                    continue
                files.append(f)
        elif p.is_file():
            files.append(p)
        elif paths:            # --path người dùng khai mà không tồn tại = lỗi DÙNG LỆNH (rc=2)
            errors.append(str(raw))
    seen, uniq = set(), []
    for f in sorted(files, key=lambda x: _doc_claims_rel(x, root)):
        k = _doc_claims_rel(f, root)
        if k not in seen:
            seen.add(k)
            uniq.append(f)
    return uniq, roots, errors


def _doc_claims_context(root: Path) -> dict:
    """Ngữ cảnh xác minh, đọc MỘT LẦN cho cả lượt quét (không mạng, không fetch).

    ★ĐO 2026-07-28 — hai tiền đề của kế hoạch phải sửa, cả hai đều do đo chứ không do đoán:

    (1) `CHANGELOG.md` chỉ còn 50 mục (v1.35.0…v1.35.53), nhưng sổ CŨ KHÔNG MẤT: nó nằm ở
        `references/changelog_archive/*.md`. Đọc thiếu chỗ đó thì 184 version bị hô sai. Vì vậy tập
        tra cứu = CHANGELOG.md + toàn bộ archive, và quét TOÀN VĂN chứ không chỉ dòng tiêu đề — số
        hiệu đợt (rNNN) phần lớn nằm trong thân bài, headings-only chỉ thấy 4/191.

    (2) Ngay cả khi gộp đủ archive, dải v1.9.x–v1.22.x vẫn thủng (46/420 version được dẫn không có
        ở đâu trong sổ). Đó là KHUYẾT của sổ, không phải bằng chứng trích dẫn sai ⇒ hạ
        VERSION_NOT_IN_CHANGELOG xuống advisory. Cờ THẬT của L5 chỉ còn VERSION_AHEAD_OF_CURRENT —
        version lớn hơn VERSION hiện hành thì SAI trong mọi hoàn cảnh, không phụ thuộc sổ đầy hay vơi.
        (Đối chiếu: L6 giữ nguyên mức cờ vì đo ra chỉ 1/192 số hiệu đợt không tra được ⇒ nhiễu ~0.)"""
    ver_txt = ""
    try:
        ver_txt = (root / "VERSION").read_text(encoding="utf-8").strip()
    except OSError:
        pass
    heads, cl_versions, cl_rs = [], set(), set()
    _cl_files = [root / "CHANGELOG.md"]
    _arc = root / "references" / "changelog_archive"
    if _arc.is_dir():
        _cl_files.extend(sorted(_arc.glob("*.md")))
    for _cf in _cl_files:
        try:
            _txt = _cf.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        # Khuôn nhận dạng phải KHỚP HỆT bên tài liệu (v1.* và rNN+), nếu không sàn tính ra vô nghĩa:
        # lấy cả `v0.7.7` thì sàn version tụt xuống 0.7.7 và nhánh advisory không bao giờ chạy; lấy cả
        # `r0` thì sàn r = 0 (falsy) — cùng một lỗi, hai chỗ.
        cl_versions.update(re.findall(r"\bv(1\.\d+\.\d+)\b", _txt))
        cl_rs.update(int(x) for x in re.findall(r"\br(\d{2,4})[a-z]?\b", _txt))
        heads.extend(ln for ln in _txt.split("\n") if ln.startswith("#"))
    def _vt(s):
        try:
            return tuple(int(x) for x in str(s).split("."))
        except ValueError:
            return None
    cur = _vt(ver_txt)
    floor_v = min((_vt(v) for v in cl_versions if _vt(v)), default=None)
    floor_r = min(cl_rs, default=None)
    max_r = max(cl_rs, default=None)
    pyindex = {}
    for d in ("scripts", "scripts/tl_core", "scripts/_fallback", "."):
        dd = root / d
        if dd.is_dir():
            for f in sorted(dd.glob("*.py")):
                pyindex.setdefault(f.name, []).append(f)
    toplevel = {p.name for p in root.iterdir()} if root.is_dir() else set()
    _rc_ab, _ab = _doc_claims_git(root, ["rev-parse", "--short", "HEAD"])
    sha_lens = {40} | ({len(_ab.strip())} if _rc_ab == 0 and _ab.strip() else {7})
    # r219/L8 — tập lệnh. Thiếu/hỏng golden ⇒ commands=None ⇒ lớp TỰ TẮT và khai báo lý do.
    commands, cmd_src = None, None
    try:
        _ps = json.loads((root / _DOC_CLAIMS_PARSER_SURFACE).read_text(encoding="utf-8"))
        if isinstance(_ps, dict) and _ps:
            commands, cmd_src = set(_ps), _DOC_CLAIMS_PARSER_SURFACE
    except (OSError, ValueError):
        pass
    test_id_index, test_id_error = None, None
    try:
        test_id_index = load_test_id_index(root)
    except FragmentError as exc:
        test_id_error = {"code": exc.code, "fragment": exc.fragment, "detail": exc.detail}
    test_id_kinds = {}
    if test_id_index is not None:
        for entry in test_id_index.entries:
            test_id_kinds[entry.kind] = test_id_kinds.get(entry.kind, 0) + 1
    return {"version": cur, "version_text": ver_txt, "changelog_versions": cl_versions,
            "changelog_rs": cl_rs, "floor_version": floor_v, "floor_r": floor_r, "max_r": max_r,
            "pyindex": pyindex, "root": root, "_deleted": None, "toplevel": toplevel,
            "sha_lens": sha_lens, "commands": commands, "test_id_index": test_id_index,
            "test_id_error": test_id_error,
            "basis": {"version": ver_txt, "sha_lens": sorted(sha_lens),
                      "changelog_files": len(_cl_files),
                      "changelog_versions": len(cl_versions), "changelog_rs": len(cl_rs),
                      "changelog_headings": len(heads),
                      "floor_version": ".".join(str(x) for x in floor_v) if floor_v else None,
                      "floor_r": floor_r, "max_r": max_r,
                      "commands_source": cmd_src,
                      "commands_known": len(commands) if commands else 0,
                      "test_ids_known": len(test_id_index.entries) if test_id_index is not None else 0,
                      "test_id_kinds": test_id_kinds,
                      "layers_bac": dict(_DOC_CLAIMS_BAC_L10_L11),
                      "note": "tập tra cứu = CHANGELOG.md + references/changelog_archive/*.md, quét "
                              "toàn văn; dưới sàn ⇒ advisory (khuyết của sổ, không phải trích dẫn sai)"}}


_DOC_CLAIMS_SPAN_RE = re.compile(r"`([^`\n]+)`")
_DOC_CLAIMS_PATH_RE = re.compile(r"^([A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)+)(/?)$")
_DOC_CLAIMS_RELPATH_RE = re.compile(r"^(\.{1,2}/[A-Za-z0-9_.\-/]+?)(/?)$")
_DOC_CLAIMS_EXT_RE = re.compile(r"\.[A-Za-z][A-Za-z0-9]{0,4}$")
_DOC_CLAIMS_SHA_RE = re.compile(r"\b[0-9a-f]{7,40}\b")
_DOC_CLAIMS_LINK_RE = re.compile(r"\[[^\]\n]*\]\(([^)\s]+)\)")
# CHỈ nhánh v1.* — `v2.21.2p` là version WEBAPP GAS, hệ đánh số KHÁC hẳn; xét chung thì 56 trích dẫn
# GAS đúng đắn bị hô «vượt VERSION hiện hành» (đo 28-07). Kế hoạch §2.3 viết `v1.NN.NN` là có lý do.
_DOC_CLAIMS_VER_RE = re.compile(r"\bv(1\.\d+\.\d+)\b")
_DOC_CLAIMS_R_RE = re.compile(r"\br(\d{2,4})[a-z]?\b")
_DOC_CLAIMS_PYLOC_RE = re.compile(
    r"(?<![A-Za-z0-9_./\-])([A-Za-z0-9_.][A-Za-z0-9_./\-]*\.py):(\d+)\b"
)
_DOC_CLAIMS_TRIM = ".,;:!?)]}»›\"'(«‹[{"


def _doc_claims_git(root: Path, args: list) -> tuple:
    """git CỤC BỘ, đọc-thuần (§2.5: không fetch, không mạng). Thiếu git ⇒ (rc≠0, '') để đường gọi tự
    hạ cấp, KHÔNG được nổ giữa lượt quét."""
    try:
        p = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=120)
        return p.returncode, p.stdout
    except Exception:  # noqa: BLE001
        return 127, ""


def _doc_claims_deleted_set(ctx: dict) -> set:
    """Tập đường dẫn TỪNG bị xoá — phân loại «đã xoá» vs «sai» (§2.2). Từ wp1121: chỉ tài liệu LỊCH SỬ được miễn
    (`PATH_DELETED_IN_HISTORICAL_DOC`, advisory); tài liệu sống trích tệp đã xoá ⇒ cờ `PATH_DELETED`.
    MỘT lệnh git cho cả lượt, gọi lười (chỉ khi có ≥1 đường dẫn hụt)."""
    if ctx.get("_deleted") is None:
        rc, out = _doc_claims_git(ctx["root"], ["log", "--diff-filter=D", "--name-only",
                                                "--pretty=format:"])
        ctx["_deleted"] = {ln.strip() for ln in out.split("\n") if ln.strip()} if rc == 0 else set()
    return ctx["_deleted"]


def _doc_claims_sha_state(ctx: dict, sha: str) -> str:
    """'commit' | 'reachable' | 'missing' — cache theo lượt (tài liệu lặp lại cùng SHA rất nhiều)."""
    cache = ctx.setdefault("_sha_cache", {})
    if sha not in cache:
        rc, _ = _doc_claims_git(ctx["root"], ["cat-file", "-e", sha + "^{commit}"])
        if rc != 0:
            cache[sha] = "missing"
        else:
            rc2, _ = _doc_claims_git(ctx["root"], ["merge-base", "--is-ancestor", sha, "HEAD"])
            cache[sha] = "reachable" if rc2 == 0 else "commit"
    return cache[sha]


def _doc_claims_scan_one(doc: Path, nofence: str, nospan: str, starts: list, *,
                         root: Path, ctx: dict) -> list:
    """Các lớp kiểm CƠ HỌC. Mỗi phát hiện là dict; `_advisory=True` ⇒ xếp vào advisories (không fail
    --strict). Ranh giới cờ-vs-advisory là điều KHIẾN báo cáo dùng được: cái máy CHẮC CHẮN sai mới là cờ."""
    out = []
    rel = _doc_claims_rel(doc, root)
    historical = _doc_claims_is_historical(rel)

    def _add(layer, off, claim, reason, detail=None, advisory=False):
        d = {"layer": layer, "file": rel, "line": _doc_claims_lineno(starts, off),
             "claim": claim, "reason": reason}
        if detail is not None:
            d["detail"] = detail
        if advisory:
            d["_advisory"] = True
        out.append(d)

    # ── L1: đường dẫn trong span backtick có chứa '/' ──────────────────────────────────────────────
    # Tách TOKEN trong span (span thật hay là cả câu lệnh: `python scripts/tl.py extract <id>`) —
    # xét nguyên span thì token nhiễu `<id>` sẽ nuốt luôn đường dẫn thật đứng cạnh.
    for sp in _DOC_CLAIMS_SPAN_RE.finditer(nofence):
        for tk in re.finditer(r"\S+", sp.group(1)):
            tok = tk.group(0).strip(_DOC_CLAIMS_TRIM)
            if not tok or "/" not in tok or _doc_claims_noisy(tok):
                continue
            off = sp.start() + 1 + tk.start()
            m = _DOC_CLAIMS_PATH_RE.match(tok) or _DOC_CLAIMS_RELPATH_RE.match(tok)
            if not m:
                continue
            body, slash = m.group(1), m.group(2)
            if not slash and not _DOC_CLAIMS_EXT_RE.search(body.rsplit("/", 1)[-1]):
                continue     # không phần mở rộng và không kết bằng '/' ⇒ chưa chắc là đường dẫn
            docrel = (doc.parent / body)
            if body.startswith("."):
                if docrel.exists():
                    continue
                _add("L1", off, tok, "PATH_MISSING")
                continue
            # CHỈ xét khẳng định VỀ CÂY NÀY: đoạn đầu phải là một mục top-level có thật. `word/document.xml`
            # (đường dẫn BÊN TRONG file .docx), `~/.tra_luat_cache/…`, `12_Lao_dong_BHXH/…` không phải
            # khẳng định về repo ⇒ im lặng, chứ không hô sai.
            if body.split("/", 1)[0] not in ctx["toplevel"]:
                continue
            if (root / body).exists() or docrel.exists():
                continue
            # wp1121 (#1121, lỗ DO6: xoá tệp còn được trích mà đã COMMIT thì rc=0) — tệp từng bị xoá chỉ được
            # miễn ở TÀI LIỆU LỊCH SỬ (§2.2: sổ được phép dẫn tệp đã chết). Tài liệu sống trích nó là con trỏ
            # chết thật ⇒ CỜ. Đo base `f4b513d`: 3/3 phát hiện PATH_DELETED nằm ở tài liệu lịch sử ⇒ 0 cờ mới.
            if body in _doc_claims_deleted_set(ctx):
                if historical:
                    _add("L1", off, tok, "PATH_DELETED_IN_HISTORICAL_DOC", advisory=True)
                else:
                    _add("L1", off, tok, "PATH_DELETED")
            elif historical:
                _add("L1", off, tok, "PATH_MISSING_IN_HISTORICAL_DOC", advisory=True)
            else:
                _add("L1", off, tok, "PATH_MISSING")

    # ── L2: commit SHA (7-40 hex, PHẢI có ≥1 chữ a-f) ─────────────────────────────────────────────
    # ★Kế hoạch r218 TỰ MÂU THUẪN: §2.3 đòi «≥1 chữ số VÀ ≥1 chữ a-f», §2.7 lại lấy `deadbeef` (KHÔNG
    # có chữ số nào) làm phản chứng — dưới luật §2.3 thì `deadbeef` không đời nào nổ. ĐO để phân xử:
    # trong TOÀN BỘ tài liệu kho, số token hex-7-40 toàn-chữ-cái = 0 (giả thuyết nhiễu 'defaced' không
    # có thật) ⇒ bỏ vế «phải có chữ số», giữ vế «phải có chữ a-f». Vế giữ lại mới là vế gánh việc: nó
    # loại token TOÀN SỐ (ngày viết liền `20260728`, số thứ tự) vốn nhiều thật.
    for m in _DOC_CLAIMS_SHA_RE.finditer(nospan):
        sha = m.group(0)
        if not any("a" <= c <= "f" for c in sha):
            continue
        # ĐO: `743ed200-aaaa-…`, `fec6c125-e01c-…` là UUID notebook, `\b` cắt ngay dấu '-' nên khúc đầu
        # trông y hệt SHA ngắn. Kề '-' ⇒ mảnh của định danh dài, KHÔNG phải khẳng định về commit.
        if (m.start() > 0 and nospan[m.start() - 1] == "-") or nospan[m.end():m.end() + 1] == "-":
            continue
        st = _doc_claims_sha_state(ctx, sha)
        if st == "reachable":
            continue
        if st == "commit":
            _add("L2", m.start(), sha, "SHA_NOT_REACHABLE_FROM_HEAD", advisory=True)
            continue
        # ĐO 28-07: cả 18 token hex bị bắt trên kho đều DÀI ĐÚNG 8 và đều là khúc đầu UUID notebook
        # («query notebook fec6c125»), trong khi git ở kho này viết tắt 7. Độ dài GIT tự khai
        # (`rev-parse --short`) + 40 = hình dạng của một khẳng định về commit; hình dạng khác mà không
        # tra ra commit thì AMBIGU, không phải sai ⇒ advisory. Tự hiệu chỉnh khi kho lớn lên, git nới
        # viết tắt thì ngưỡng nới theo.
        if len(sha) in ctx["sha_lens"]:
            # r264: L1/L4/L8/L9 đã hạ cấp cho tài liệu LỊCH SỬ; L2 bị BỎ SÓT dù chú thích L4 ngay dưới
            # tự nói khuôn đúng là «cùng khuôn L1/L8». Một bản GHI CHÉP dẫn commit không còn trong kho (nhánh
            # đã xoá ⇒ unreachable; hoặc clone SHALLOW) là ghi chép, không phải con trỏ sống. Đo lúc mở: 0 cờ
            # cứng loại này trên roots mặc định ⇒ KHÔNG mất phát hiện nào đang sống. Giá phải trả, nói thẳng:
            # SHA gõ sai trong CHANGELOG từ nay là advisory chứ không chặn gate.
            _add("L2", m.start(), sha, "SHA_NOT_A_COMMIT"
                 if not historical else "SHA_NOT_A_COMMIT_IN_HISTORICAL_DOC", advisory=historical)
        else:
            _add("L2", m.start(), sha, "SHA_LIKE_NOT_A_COMMIT", {"len": len(sha)}, advisory=True)

    # ── L3: link markdown tương đối — resolve TỪ VỊ TRÍ TÀI LIỆU ──────────────────────────────────
    for m in _DOC_CLAIMS_LINK_RE.finditer(nofence):
        tgt = m.group(1).strip()
        if (not tgt or tgt.startswith(("#", "http://", "https://", "mailto:", "ftp://", "<"))
                or _doc_claims_noisy(tgt) or re.match(r"^[A-Za-z]:[\\/]", tgt)):
            continue
        bare = tgt.split("#", 1)[0].split("?", 1)[0]
        # `[nhãn](url)` — chỗ giữ chỗ trong tài liệu mẫu, không có '/' cũng không có đuôi ⇒ không phải
        # khẳng định về một tệp nào cả.
        if not bare or ("/" not in bare and "." not in bare):
            continue
        try:
            hit = (doc.parent / bare).exists() or (root / bare).exists()
        except OSError:
            hit = False
        if not hit:
            _add("L3", m.start(1), tgt, "LINK_TARGET_MISSING")

    # ── L4 (r220): giàn giáo nháp còn sót ─────────────────────────────────────────────────────────
    # Tài liệu SỐNG trình bày như đã xong mà còn `{{chỗ_điền}}`/TODO trong văn xuôi thì không hoàn
    # cảnh nào đúng ⇒ CỜ; tài liệu lịch sử nhắc lại là ghi chép ⇒ advisory (cùng khuôn L1/L8).
    for m in _DOC_CLAIMS_L4_MUSTACHE_RE.finditer(nospan):
        _add("L4", m.start(), m.group(0), "DRAFT_PLACEHOLDER", advisory=historical)
    for m in _DOC_CLAIMS_L4_WORD_RE.finditer(nospan):
        tok = m.group(0)
        # `NN-YYYY-VBHN-XXX` — ký pháp số hiệu (12/12 hit đo được toàn kho 28-07): XXX kề '-' là
        # mảnh của định danh dài, không phải khẳng định «chỗ này chưa viết» ⇒ im, cùng phép của L2.
        if tok == "XXX" and ((m.start() > 0 and nospan[m.start() - 1] == "-")
                             or nospan[m.end():m.end() + 1] == "-"):
            continue
        _add("L4", m.start(), tok, "DRAFT_MARKER", advisory=historical)

    # ── L5: version vX.Y.Z ────────────────────────────────────────────────────────────────────────
    for m in _DOC_CLAIMS_VER_RE.finditer(nospan):
        v = m.group(1)
        try:
            t = tuple(int(x) for x in v.split("."))
        except ValueError:
            continue
        if ctx["version"] and t > ctx["version"]:
            _add("L5", m.start(), "v" + v, "VERSION_AHEAD_OF_CURRENT", ctx["version_text"])
        elif ctx["floor_version"] and t < ctx["floor_version"]:
            _add("L5", m.start(), "v" + v, "VERSION_BELOW_CHANGELOG_FLOOR", advisory=True)
        elif v not in ctx["changelog_versions"]:
            _add("L5", m.start(), "v" + v, "VERSION_NOT_IN_CHANGELOG", advisory=True)

    # ── L6: số hiệu đợt vá rNNN (chấp hậu tố: `r208d` là đợt 208) ─────────────────────────────────
    # ĐỐI XỨNG VỚI L5 — và lý do là ca thật: `r160` (THE_THUC_TRINH_BAY.md) không tra được, nhưng sổ
    # cũng KHÔNG có r158/159/161/163/165 ⇒ vắng mặt trong dải thưa KHÔNG chứng minh trích dẫn sai.
    # Chỉ khẳng định BẤT KHẢ mới là cờ: đợt lớn hơn đợt mới nhất từng ghi thì chưa tồn tại, không có
    # cách nào đúng. Trong-dải-mà-vắng = advisory.
    for m in _DOC_CLAIMS_R_RE.finditer(nospan):
        n, claim = int(m.group(1)), m.group(0)
        if ctx["max_r"] and n > ctx["max_r"]:
            _add("L6", m.start(), claim, "R_AHEAD_OF_LATEST", {"latest": ctx["max_r"]})
        elif ctx["floor_r"] and n < ctx["floor_r"]:
            _add("L6", m.start(), claim, "R_BELOW_CHANGELOG_FLOOR", advisory=True)
        elif n not in ctx["changelog_rs"]:
            _add("L6", m.start(), claim, "R_NOT_IN_CHANGELOG", advisory=True)

    # ── L7: con trỏ mã <file>.py:<dòng> ───────────────────────────────────────────────────────────
    for m in _DOC_CLAIMS_PYLOC_RE.finditer(nofence):
        fname, num = m.group(1), int(m.group(2))
        claim = m.group(0)
        if _doc_claims_noisy(fname):
            continue
        if "/" in fname:
            # `./` / `../` đã được L7 hiểu từ trước như con trỏ từ gốc kho. Giữ đúng ngữ nghĩa ấy
            # sau khi regex bắt cả tiền tố, thay vì để tiền tố vô tình biến mất ở tầng regex.
            repo_fname = re.sub(r"^(?:\.\.?/)+", "", fname)
            cands = [root / repo_fname, doc.parent / fname]
        else:
            cands = list(ctx["pyindex"].get(fname.rsplit("/", 1)[-1], []))
        root_resolved = root.resolve()
        resolved_cands = []
        for cand in cands:
            try:
                resolved = Path(cand).resolve()
                if resolved.is_relative_to(root_resolved):
                    resolved_cands.append(resolved)
            except (OSError, RuntimeError):
                continue
        hit = next((c for c in resolved_cands if c.is_file()), None)
        if hit is None:
            _add("L7", m.start(), claim, "PYLOC_FILE_MISSING")
            continue
        try:
            total = Path(hit).read_text(encoding="utf-8", errors="replace").count("\n") + 1
        except OSError:
            continue
        if num < 1 or num > total:
            _add("L7", m.start(), claim, "PYLOC_LINE_OUT_OF_RANGE", {"file_lines": total})

    # ── L8 (r219): tên lệnh `tl <cmd>` không có trong parser ──────────────────────────────────────
    # Đây là lớp ĐÚNG TRỌNG TÂM của cả lệnh doc-claims-check: tài liệu bảo phiên sau chạy một lệnh
    # KHÔNG TỒN TẠI thì phiên đó đi thẳng vào ngõ cụt — không cách nào đúng, nên là CỜ chứ không
    # phải advisory. Quét trên `nofence` và CHỈ trong span backtick (lệnh luôn được viết trong
    # backtick; văn xuôi thì không) — đo 28-07: quét trần 8 hit toàn báo giả, trong-span còn 4 và
    # cả 4 đều ở sổ lưu trữ, tức 0 cờ trên tài liệu sống ⇒ lớp này vào kho là XANH SẴN.
    # Tài liệu LỊCH SỬ được phép nhắc lệnh đã gỡ (`tl regen2` — ca thật) ⇒ hạ advisory, cùng khuôn L1.
    if ctx.get("commands"):
        for sp in _DOC_CLAIMS_SPAN_RE.finditer(nofence):
            cmd = _doc_claims_tl_cmd(sp.group(1))
            if not cmd or cmd in ctx["commands"]:
                continue
            _add("L8", sp.start(), "tl " + cmd, "TL_COMMAND_UNKNOWN", advisory=historical)

    # ── L12 (F1-02): con trỏ tên ca selftest legacy/packet dùng CHUNG resolver của fragment loader ──
    test_ids = ctx.get("test_id_index")
    if test_ids is not None:
        for sp in _DOC_CLAIMS_SPAN_RE.finditer(nofence):
            for test_id, offset in find_test_id_pointers(sp.group(1)):
                if test_ids.resolve(test_id) is None:
                    _add("L12", sp.start() + 1 + offset, test_id, "TEST_ID_UNKNOWN",
                         advisory=historical)
    return out


def _doc_claims_orphan_scope(scanned: dict) -> bool:
    """L9 chỉ có nghĩa khi lượt quét ĐỦ RỘNG. Chạy nó trên `--path references/GOTCHAS.md` thì mọi tệp
    khác đều «không ai trỏ tới» — một kết luận vô nghĩa sinh ra 28 cờ rác. Điều kiện: có SKILL.md
    (nơi giữ danh mục) VÀ ít nhất một tệp dưới references/."""
    return ("SKILL.md" in scanned
            and any(k.startswith(_DOC_CLAIMS_ORPHAN_DIR) for k in scanned))


def _doc_claims_orphans(scanned: dict, root: Path) -> list:
    """L9 — tài liệu mồ côi.

    ★ĐO 28-07 BÁC ĐỊNH NGHĨA CỦA KẾ HOẠCH, và đây là chỗ đáng ghi lại nhất của lớp này. Kế hoạch
    r218 định nghĩa mồ côi = «vắng trong mục DANH MỤC REFERENCES của SKILL.md». Đo: 20/29 tệp
    references/*.md vắng ⇒ hô 69% cây tài liệu. Tệ hơn: cách «sửa» duy nhất là thêm 20 dòng vào
    SKILL.md, trong khi kernel chỉ còn 162 B đệm tới trần WARN 47KB ⇒ lớp đó BẤT KHẢ THI HÀNH.
    Danh mục kernel là bản CHỌN LỌC có chủ đích (9 mục + 2 glob), không phải chỉ mục đầy đủ —
    đọc nó thành chỉ mục là đọc sai chức năng của nó.

    Định nghĩa dùng được (đo ra 0 cờ + 5 advisory trên kho, tức vào kho là xanh sẵn):
      • cờ  `DOC_NO_INBOUND_POINTER` — KHÔNG nguồn nào trong kho nhắc tới (md đã quét + mọi .py +
        workflow card + docs/adr). Tệp nằm trong gói mà không đường nào dẫn tới: BẤT KHẢ đúng.
      • adv `DOC_POINTED_ONLY_BY_HISTORICAL` — chỉ CHANGELOG/sổ lưu trữ/DOCTRINE_APPENDIX nhắc.
        Người đọc hiện tại không có lối tới, nhưng có thể là ghi chép thiết kế cố ý lưu ⇒ advisory.
    """
    refs = sorted(p for p in (root / "references").glob("*.md")) if root.is_dir() else []
    if not refs:
        return []
    extra = {}
    for sub, pat in _DOC_CLAIMS_ORPHAN_EXTRA:
        d = root / sub
        if not d.is_dir():
            continue
        for f in sorted(d.glob(pat)):
            try:
                extra[_doc_claims_rel(f, root)] = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
    out = []
    for p in refs:
        rel = _doc_claims_rel(p, root)
        base = p.name
        live = hist = 0
        for src, txt in list(scanned.items()) + list(extra.items()):
            if src == rel or (rel not in txt and base not in txt):
                continue
            if _doc_claims_is_historical(src):
                hist += 1
            else:
                live += 1
        if live:
            continue
        d = {"layer": "L9", "file": rel, "line": 1, "claim": rel}
        if hist:
            d.update(reason="DOC_POINTED_ONLY_BY_HISTORICAL", detail={"historical_refs": hist},
                     _advisory=True)
        else:
            d["reason"] = "DOC_NO_INBOUND_POINTER"
        out.append(d)
    return out


def _doc_claims_check(paths=None, *, root: Path = None) -> dict:
    root = Path(root) if root else HERE.parent
    files, roots, bad = _doc_claims_targets(paths, root)
    if bad:
        return {"ok": False, "schema": _DOC_CLAIMS_SCHEMA, "error": "PATH_NOT_FOUND",
                "missing_paths": sorted(bad), "usage_error": True}
    ctx = _doc_claims_context(root)
    flags, advisories, checked = [], [], 0
    if ctx.get("test_id_error"):
        flags.append({"layer": "L12", "file": "scripts/tl_selftest.py", "line": 1,
                      "claim": "test-id-index", "reason": "TEST_ID_INDEX_UNAVAILABLE",
                      "detail": ctx["test_id_error"]})
        checked += 1
    scanned = {}
    for f in files:
        try:
            raw = f.read_text(encoding="utf-8", errors="replace")   # GOTCHAS §8: encoding TƯỜNG MINH
        except OSError as e:
            flags.append({"layer": "L0", "file": _doc_claims_rel(f, root), "line": 1,
                          "claim": f.name, "reason": "FILE_UNREADABLE", "detail": type(e).__name__})
            continue
        scanned[_doc_claims_rel(f, root)] = raw
        nofence, nospan = _doc_claims_mask(raw)
        starts = _doc_claims_linestarts(raw)
        for fl in _doc_claims_scan_one(f, nofence, nospan, starts, root=root, ctx=ctx):
            checked += 1
            if fl.pop("_advisory", False):
                advisories.append(fl)
            else:
                flags.append(fl)
    l9_ran = _doc_claims_orphan_scope(scanned)
    if l9_ran:
        for fl in _doc_claims_orphans(scanned, root):
            checked += 1
            if fl.pop("_advisory", False):
                advisories.append(fl)
            else:
                flags.append(fl)
    def _key(d):   # thứ tự TẤT ĐỊNH (đích §2.7-10: hai lượt cho JSON byte-identical)
        return (d["file"], d["line"], d["layer"], d["claim"], d["reason"])
    flags.sort(key=_key)
    advisories.sort(key=_key)
    by_layer = {L: sum(1 for x in flags if x["layer"] == L) for L in _DOC_CLAIMS_LAYERS}
    # Lớp TỰ TẮT phải KHAI BÁO — «0 cờ vì không chạy» và «0 cờ vì sạch» là hai kết luận khác hẳn.
    skipped = {}
    if not ctx.get("commands"):
        skipped["L8"] = "thiếu " + _DOC_CLAIMS_PARSER_SURFACE
    if not l9_ran:
        skipped["L9"] = "lượt quét không đủ rộng (cần SKILL.md + ≥1 tệp references/)"
    if ctx.get("test_id_index") is None:
        skipped["L12"] = "không dựng được shared test-ID index"
    return {"ok": not flags, "schema": _DOC_CLAIMS_SCHEMA, "roots": roots,
            "files_scanned": len(files), "claims_flagged": checked,
            "flags": flags, "advisories": advisories,
            "by_layer": by_layer, "advisory_count": len(advisories),
            "layers": list(_DOC_CLAIMS_LAYERS), "layers_skipped": skipped, "basis": ctx["basis"]}


def cmd_doc_claims_check(a) -> int:
    out = _doc_claims_check(getattr(a, "path", None) or None)
    strict = bool(getattr(a, "strict", False))
    out["strict"] = strict
    if getattr(a, "out", None):
        _write_text_atomic(Path(a.out), _json_dumps(out, deterministic=True) + "\n")
    _print_json_or_text(out, getattr(a, "json", False))
    if out.get("usage_error"):
        return 2
    if out.get("ok"):
        return 0
    return 2 if strict else 1


def _golden_dir() -> Path:
    return HERE.parent / "references" / "golden"


_GOLDEN_CASES = [
    {"id": "route_task_ingest_zip", "file": "route_task_ingest_zip.json", "args": ["route-task", "--task", "ingest_zip", "--json"]},
    {"id": "nlm_query_plan_3_sources", "file": "nlm_query_plan_3_sources.json", "args": ["nlm-query-plan", "Trích Điều 1 của văn bản mẫu", "--source-id", "src_A", "--source-id", "src_B", "--source-id", "src_C", "--json"]},
    {"id": "workflow_audit", "file": "workflow_audit.json", "args": ["workflow-audit", "--json"]},
    {"id": "tool_inventory_inventory_decision", "file": "tool_inventory_inventory_decision.json", "args": ["tool-inventory", "--group", "inventory_decision", "--json"]},
    {"id": "route_task_ocr_ingest", "file": "route_task_ocr_ingest.json", "args": ["route-task", "--task", "ocr_ingest", "--json"]},
    {"id": "route_task_profile_ingest_chunks", "file": "route_task_profile_ingest_chunks.json", "args": ["route-task", "--task", "profile_ingest_chunks", "--json"]},
    # v1.33.59 (Pha G1 — mở rộng theo kế hoạch): case OFFLINE-thuần trên fixtures cố định.
    {"id": "chunk_plan_profile_fixture", "file": "chunk_plan_profile_fixture.json", "args": ["chunk-plan", "{FIXTURES}/sample_profile.txt", "--mode", "profile", "--name", "sample", "--max-chars", "200", "--json"]},
    {"id": "chunk_plan_vbqppl_canonical_blocked", "file": "chunk_plan_vbqppl_canonical_blocked.json", "args": ["chunk-plan", "{FIXTURES}/sample_profile.txt", "--mode", "vbqppl-canonical", "--json"]},
    {"id": "ocr_analyze_fixture", "file": "ocr_analyze_fixture.json", "args": ["ocr-analyze", "{FIXTURES}/sample_profile.txt", "--json"]},
    {"id": "ingest_zip_dryrun_slip", "file": "ingest_zip_dryrun_slip.json", "args": ["ingest-zip", "{FIXTURES}/slip.zip", "--cat", "01", "--json"]},
    {"id": "ingest_zip_dryrun_dup", "file": "ingest_zip_dryrun_dup.json", "args": ["ingest-zip", "{FIXTURES}/dup.zip", "--cat", "01", "--json"]},
    {"id": "live_state_diff_no_changes", "file": "live_state_diff_no_changes.json", "args": ["live-state-diff", "{FIXTURES}/snap_a.json", "{FIXTURES}/snap_a2.json", "--json"]},
    # v1.34.3 (I1 characterization — TRƯỚC khi tách cụm hygiene sang tl_core/hygiene.py): 6 case offline trên
    # FIXTURE MANIFEST (env TL_CACHE_DIR trỏ fixtures/cache_hygiene — cách ly trạng thái máy; fixture gài đủ
    # defect: dup by_sohieu, VBHN thiếu năm, thiếu sohieu-tên-mang-số, tên thô, removed_*, overflow, ref-chunk,
    # infra_in_corpus). Khóa byte-level hành vi hiện tại; sau AST-cut golden PHẢI khớp nguyên trạng.
    {"id": "hygiene_sweep_fixture", "file": "hygiene_sweep_fixture.json", "args": ["sweep", "--json"],
     "volatile_keys": ["snapshot_age_s"], "env": {"TL_CACHE_DIR": "{FIXTURES}/cache_hygiene"}},
    {"id": "hygiene_dedup_plan_dry", "file": "hygiene_dedup_plan_dry.json", "args": ["dedup-plan", "--json"], "env": {"TL_CACHE_DIR": "{FIXTURES}/cache_hygiene"}},
    {"id": "hygiene_missing_sohieu_dry", "file": "hygiene_missing_sohieu_dry.json", "args": ["missing-sohieu", "--json"], "env": {"TL_CACHE_DIR": "{FIXTURES}/cache_hygiene"}},
    {"id": "hygiene_vbhn_year_fix_dry", "file": "hygiene_vbhn_year_fix_dry.json", "args": ["vbhn-year-fix", "--json"], "env": {"TL_CACHE_DIR": "{FIXTURES}/cache_hygiene"}},
    {"id": "hygiene_reg_query_corpus", "file": "hygiene_reg_query_corpus.json", "args": ["reg-query", "--corpus", "--json"], "env": {"TL_CACHE_DIR": "{FIXTURES}/cache_hygiene"}},
    # v1.34.60 (A1 — golden CÓ CHỦ ĐÍCH cho lệnh mới doc-text): offline thuần qua cache extract_<id>.txt
    # trong fixture TL_CACHE_DIR (không mạng, không Drive) — khoá envelope doc_text.v1 + đường cắt --dieu.
    {"id": "doc_text_cache_fixture", "file": "doc_text_cache_fixture.json",
     "args": ["doc-text", "gd_doctext60", "--dieu", "2", "--json"],
     "env": {"TL_CACHE_DIR": "{FIXTURES}/cache_hygiene"}},
    # (v1.34.7 I4) ops-plan HỒI SINH golden nhờ FIXTURE CONFIG (bài học v1.34.3: output phụ thuộc trạng thái
    # config máy — nay --config fixture + xoá env TL_* để fixture quyết định tất cả → cross-machine).
    # r218: doc-claims-check trên fixture .md cố định — khoá cả 6 lớp + phép che fence trong MỘT ảnh.
    # `basis` (VERSION, sàn sổ) và `detail` (số dòng tệp, đợt mới nhất) đổi theo thời điểm ⇒ khai volatile,
    # phần nghiệp vụ (lớp/lý do/dòng/thứ tự) vẫn bị khoá byte.
    {"id": "doc_claims_check_fixture", "file": "doc_claims_check_fixture.json",
     "args": ["doc-claims-check", "--path", "{FIXTURES}/doc_claims", "--json"],
     "volatile_keys": ["basis", "detail"]},
    {"id": "hygiene_ops_plan_fixture_config", "file": "hygiene_ops_plan_fixture_config.json",
     "args": ["ops-plan", "--config", "{FIXTURES}/config_fixture.json", "--json"],
     "env": {"TL_CACHE_DIR": "{FIXTURES}/cache_hygiene", "TL_REGISTRY_DOC_ID": "", "TL_NOTEBOOK_ID": "",
             "TL_PROFILE": "", "TL_ROOT_FOLDER_ID": "", "TL_META_FOLDER_ID": "", "TL_MANIFEST_ID": "",
             "TL_MANIFEST_SCOPE": "", "TL_WEBAPP": "", "TL_TOKEN": ""}},
]


def _golden_fixdir() -> Path:
    return _golden_dir() / "fixtures"


def _golden_ensure_fixtures() -> None:
    """v1.33.59: fixtures SINH-TẠI-CHỖ byte-tất-định (zip date_time 1980, nội dung cố định) — repo giữ
    text-only (pre-commit hook chặn binary là ĐÚNG, không nới); CI/gói giải nén tự tái tạo y hệt."""
    fd = _golden_fixdir()
    fd.mkdir(parents=True, exist_ok=True)
    _nl = chr(10)
    sample = _nl.join([
        "Điều 1. Phạm vi điều chỉnh",
        "Văn bản mẫu dùng cho golden fixtures — nội dung ổn định, không đổi.",
        "",
        "Điều 2. Đối tượng áp dụng",
        "Cơ quan, tổ chức, cá nhân có liên quan đến kiểm thử tất định.",
        "",
        "Điều 3. Hiệu lực thi hành",
        "Văn bản này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2026.",
        "",
    ]).encode("utf-8")
    snap_a = json.dumps({
        "schema": "live_state_snapshot.v1",
        "auth": {"gws_credentials": {"present": True, "age_days": 4.793}},
        "registry": {"rows": 745},
        "volatile": {"generatedAt": "2026-07-09T00:00:00Z"},
    }, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
    snap_b = snap_a.replace(b"4.793", b"4.794").replace(b"00:00:00", b"11:11:11")
    def _zip_bytes(members):
        # v1.34.0 (CI run #1 bắt được): DEFLATE cho output KHÁC NHAU giữa các build zlib (Ubuntu zlib-ng ≠
        # Windows) → sha256(zip) trong idempotency_key lệch golden cross-platform. STORED = bytes chỉ phụ
        # thuộc nội dung + metadata → máy-độc-lập thật sự.
        # v1.34.45 (CI ubuntu bắt): STORED CHƯA đủ — ZipInfo.create_system mặc định = 0 (Windows) / 3 (Linux)
        # → "version made by" khác byte → archive_sha256 (ingest_zip golden) lệch Windows↔ubuntu. Pin create_system=3
        # + extra/comment rỗng (khớp release._zip_write_bytes_deterministic) để fixture zip máy-độc-lập THẬT.
        import io as _io
        buf = _io.BytesIO()
        with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_STORED) as zf:
            for name, data in members:
                info = zipfile.ZipInfo(name)
                info.date_time = (1980, 1, 1, 0, 0, 0)
                info.compress_type = zipfile.ZIP_STORED
                info.create_system = 3
                info.extra = b""
                info.comment = b""
                info.external_attr = 0o100644 << 16
                zf.writestr(info, data)
        return buf.getvalue()
    # v1.34.3 (I1): fixture manifest cho 6 golden hygiene — entries gài đủ defect để detector nổ:
    # dup by_sohieu (45-2019-QH14 ×2), VBHN thiếu năm (14-VBHN-BTC), thiếu sohieu tên-mang-số, tên thô loai
    # thuong, removed_by_user, row_kind overflow/ref (goc trỏ canonical), infra .json corpus=true.
    _me = [
        {"drive_id": "gd_luat45", "name": "Luat_Bao_hiem_xa_hoi_45_2019_QH14", "so_hieu": "45-2019-QH14", "cat": "12_Lao_dong_BHXH", "loai": "Luật", "corpus": "true", "nlm_source_id": "src_45", "nlm_notebook_id": "nb_base", "nlm_status": "pushed", "row_kind": "own", "mime": "application/vnd.google-apps.document", "title_vn": "Luật Bảo hiểm xã hội"},
        {"drive_id": "gd_luat45_dup", "name": "Luat_BHXH_45_2019_QH14_ban_trung", "so_hieu": "45-2019-QH14", "cat": "12_Lao_dong_BHXH", "loai": "Luật", "corpus": "true", "nlm_source_id": "src_45b", "nlm_notebook_id": "nb_base", "nlm_status": "pushed", "row_kind": "own", "mime": "application/vnd.google-apps.document"},
        {"drive_id": "gd_vbhn18", "name": "VBHN_18_2024_VBHN_VPQH_Bo_luat_Lao_dong", "so_hieu": "18-2024-VBHN-VPQH", "cat": "12_Lao_dong_BHXH", "loai": "Văn bản hợp nhất", "corpus": "true", "nlm_source_id": "src_18", "nlm_notebook_id": "nb_base", "nlm_status": "pushed", "row_kind": "own", "mime": "application/vnd.google-apps.document"},
        {"drive_id": "gd_vbhn_bare", "name": "VBHN_14_VBHN_BTC_Thue", "so_hieu": "14-VBHN-BTC", "cat": "21_Thue_phi", "loai": "Văn bản hợp nhất", "corpus": "true", "nlm_source_id": "", "nlm_notebook_id": "", "nlm_status": "", "row_kind": "own", "mime": "application/vnd.google-apps.document"},
        {"drive_id": "gd_no_sohieu", "name": "114_2025_QH15_658530", "so_hieu": "", "cat": "03_To_chuc_bo_may", "loai": "Luật", "corpus": "true", "nlm_source_id": "src_114", "nlm_notebook_id": "nb_base", "nlm_status": "pushed", "row_kind": "own", "mime": "application/vnd.google-apps.document"},
        {"drive_id": "gd_raw_name", "name": "bao cao tinh hinh 2026.docx", "so_hieu": "", "cat": "99_Van_ban_thuong", "loai": "thuong", "corpus": "", "nlm_source_id": "", "nlm_notebook_id": "", "nlm_status": "", "row_kind": "own", "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"},
        {"drive_id": "gd_removed", "name": "Nghi_dinh_cu_da_go_01_2020_ND_CP", "so_hieu": "01-2020-ND-CP", "cat": "05_Hanh_chinh", "loai": "Nghị định", "corpus": "false", "nlm_source_id": "src_rm", "nlm_notebook_id": "nb_base", "nlm_status": "removed_by_user", "row_kind": "own", "mime": "application/vnd.google-apps.document"},
        {"drive_id": "gd_overflow", "name": "Thong_tu_02_2026_TT_BTC", "so_hieu": "02-2026-TT-BTC", "cat": "21_Thue_phi", "loai": "Thông tư", "corpus": "true", "nlm_source_id": "src_ovf", "nlm_notebook_id": "nb_ovf", "nlm_status": "pushed", "row_kind": "overflow", "mime": "application/vnd.google-apps.document"},
        {"drive_id": "gd_ref_chunk", "name": "Chunk_45_2019_QH14_phan_1", "so_hieu": "", "cat": "12_Lao_dong_BHXH", "loai": "Luật", "corpus": "false", "nlm_source_id": "src_chunk", "nlm_notebook_id": "nb_base", "nlm_status": "pushed", "row_kind": "ref", "goc": "gd_luat45", "mime": "application/vnd.google-apps.document"},
        {"drive_id": "gd_infra", "name": "nlm_sources_delta_2026.json", "so_hieu": "", "cat": "12_Lao_dong_BHXH", "loai": "", "corpus": "true", "nlm_source_id": "", "nlm_notebook_id": "", "nlm_status": "", "row_kind": "own", "mime": "application/json"},
    ]
    manifest_fixture = json.dumps({"ok": True, "entries": _me}, ensure_ascii=False, sort_keys=True, indent=1).encode("utf-8")
    # v1.34.7 (I4): FIXTURE CONFIG tất định — cách ly trạng thái config máy (mở khoá golden ops-plan; dùng
    # chung cho mọi case cần --config). registryDocId ĐÃ pin (không phải Doc legacy) → không advisory P0 pin.
    config_fixture = json.dumps({
        "schema": 2, "webappUrl": "https://fixture.invalid/exec", "token": "tk_fixture",
        "defaultProfile": "vbqppl",
        "profiles": {
            "vbqppl": {"notebookId": "nb_base", "rootFolderId": "root_fix", "metaFolderId": "meta_fix",
                       "registryDocId": "regsheet_fixture_1234567890", "manifestId": "manifest_fix",
                       "overflowNotebookId": "nb_ovf"},
            "Hồ sơ 74": {"notebookId": "nb_p74", "rootFolderId": "root_p74", "metaFolderId": "meta_p74",
                          "registryDocId": "regsheet_p74_1234567890", "manifestId": "manifest_p74",
                          "categories": "own", "manifestScope": "own"},
        },
    }, ensure_ascii=False, sort_keys=True, indent=1).encode("utf-8")
    # r218: tài liệu mẫu cho golden doc-claims-check — gài đủ MỌI LỚP quét-theo-token (r219: thêm
    # L8; r220: thêm L4 — cặp nổ/im trên cùng một dòng, và marker trong fence/span phải im), mỗi
    # lớp một khẳng định sai VÀ một khẳng định đúng, cộng khối fence để khoá phép che nhiễu. Mọi
    # giá trị chọn sao cho ổn định qua các đợt bump: `v1.0.1` mãi dưới sàn sổ, `r09` mãi dưới sàn đợt,
    # `references/GOTCHAS.md` là tệp bất biến của kho. (Số hiệu phụ thuộc thời điểm nằm hết trong
    # `basis`/`detail` — khai volatile.) L9 KHÔNG có ở đây được: nó cần lượt quét đủ rộng, nên cái
    # golden khoá là dòng `layers_skipped.L9` — chính bằng chứng lớp đã tự tắt đúng lúc.
    # ★Fixture này SINH TỪ MÃ: sửa tay tệp dưới `references/golden/fixtures/` sẽ bị ghi đè lặng lẽ ở
    # lần `golden-test` kế tiếp — muốn đổi thì đổi Ở ĐÂY (r219 đã trả giá một lượt).
    doc_claims = ("\n".join([
        "# Tài liệu mẫu cho doc-claims-check",
        "",
        "Đúng: `references/GOTCHAS.md` và `scripts/tl.py:1`; bản v1.0.1 cũ, đợt r09 xa xưa.",
        "Sai: `references/KHONG_CO_FILE.md`, commit deadbee, sổ notebook fec6c125.",
        "Sai tiếp: bản v1.99.0, đợt r999, con trỏ `scripts/tl.py:999999`.",
        "Link gãy [kế hoạch](./KHONG_CO_KE_HOACH.md); link ngoài [web](https://example.invalid/x.md).",
        "Lệnh `tl sweep --json` có thật, `tl khong-co-lenh-nay` thì không.",
        "Nháp sót: {{dien_sau}} và việc TODO dang dở; ký pháp NN-YYYY-VBHN-XXX với `TODO trong span` thì im.",
        "",
        chr(96) * 3 + "bash",
        "cat references/KHONG_CO_TRONG_FENCE.md   # r998 v1.98.0 TODO {{trong_fence}}",
        chr(96) * 3,
        "",
    ])).encode("utf-8")
    want = {
        "doc_claims/claims.md": doc_claims,
        "sample_profile.txt": sample,
        "snap_a.json": snap_a,
        "snap_a2.json": snap_b,
        "slip.zip": _zip_bytes([("../evil.docx", b"slip"), ("van_ban_hop_le.docx", b"binh thuong"), ("bao cao?.docx", b"ten cam win")]),
        "dup.zip": _zip_bytes([("a.docx", b"mot"), ("./a.docx", b"hai")]),
        "cache_hygiene/manifest.json": manifest_fixture,
        # v1.34.60 (A1): cache extract cho golden doc-text — cùng nội dung sample (Điều 1..3 ổn định).
        "cache_hygiene/extract_gd_doctext60.txt": sample,
        "config_fixture.json": config_fixture,
    }
    for name, data in want.items():
        fp = fd / name
        fp.parent.mkdir(parents=True, exist_ok=True)
        if not fp.exists() or fp.read_bytes() != data:
            fp.write_bytes(data)


def _golden_args(case: dict) -> list[str]:
    """v1.33.59: thay token {FIXTURES} bằng đường dẫn fixtures thật (output đã được deterministic-scrub
    về project-relative nên golden ổn định cross-machine/CI)."""
    fd = str(_golden_fixdir())
    return [a.replace("{FIXTURES}", fd) for a in case["args"]]


def _golden_env(case: dict) -> dict:
    """v1.34.3 (I1): env per-case (vd TL_CACHE_DIR → fixture manifest), thay {FIXTURES} như args.
    (r181) LUÔN ghim TL_PROFILE=DEFAULT_PROFILE: golden fixtures chụp dưới profile NỀN; subprocess golden kế thừa
    defaultProfile máy — nếu ≠ nền (vd S10 «Luật BHXH») thì reg-query trả base_also / corpus·đếm theo overlay
    profile → golden ĐỎ GIẢ (cùng bệnh hermetic-profile như selftest). Case tự khai TL_PROFILE thì tôn trọng
    (setdefault). Đường --write cũng nhờ đó regen dưới ĐÚNG nền."""
    fd = str(_golden_fixdir())
    env = {k: str(v).replace("{FIXTURES}", fd) for k, v in (case.get("env") or {}).items()}
    env.setdefault("TL_PROFILE", DEFAULT_PROFILE)
    return env


def _golden_test(*, write: bool = False) -> dict:
    from tl_core.deterministic import PATHISH_KEYS, audit_projection
    _golden_ensure_fixtures()
    gdir = _golden_dir()
    if write:
        gdir.mkdir(parents=True, exist_ok=True)
    cases = []
    for case in _GOLDEN_CASES:
        path = gdir / case["file"]
        _args = _golden_args(case)
        _env = _golden_env(case)
        run = _run_tl_json(_args, env_extra=_env)
        rec = {"id": case["id"], "file": str(path), "command": _args, "ok": False, "mode": "write" if write else "verify"}
        # v1.33.59 (Pha G1): case NEGATIVE (vd DO_NOT_SPLIT, DUPLICATE_NORMALIZED) exit rc=2 CÓ CHỦ ĐÍCH —
        # golden chấp nhận mọi output là JSON dict (payload đã mang ok:false); chỉ fail khi KHÔNG parse được.
        if not isinstance(run.get("data"), dict):
            rec.update({"error": "COMMAND_FAILED_OR_NON_JSON", "returncode": run.get("returncode"), "parse_error": run.get("parse_error"), "stderr_tail": run.get("stderr_tail")})
            cases.append(rec)
            continue
        # So sánh trên projection do case khai báo.  Raw output vẫn được báo
        # để quan sát, nhưng giá trị nghiệp vụ/volatile không bị serializer
        # sửa ngầm chỉ nhằm làm test xanh.
        run2 = _run_tl_json(_args, env_extra=_env)
        _raw1, _raw2 = str(run.get("stdout") or ""), str(run2.get("stdout") or "")
        rec["raw_stable"] = (_raw1 == _raw2)
        rec["raw_sha256"] = hashlib.sha256(_raw1.encode("utf-8")).hexdigest()
        if not isinstance(run2.get("data"), dict):
            rec.update({"error": "SECOND_RUN_FAILED_OR_NON_JSON", "returncode": run2.get("returncode"),
                        "parse_error": run2.get("parse_error"), "stderr_tail": run2.get("stderr_tail")})
            cases.append(rec)
            continue
        volatile_keys = set(case.get("volatile_keys") or [])
        path_keys = set(case.get("path_keys") or PATHISH_KEYS)
        projected1 = audit_projection(run.get("data"), volatile_keys=volatile_keys, path_keys=path_keys,
                                      project_root=HERE.parent)
        projected2 = audit_projection(run2.get("data"), volatile_keys=volatile_keys, path_keys=path_keys,
                                      project_root=HERE.parent)
        projected_text1 = _json_dumps(projected1, deterministic=True) + "\n"
        projected_text2 = _json_dumps(projected2, deterministic=True) + "\n"
        rec["projection_stable"] = projected_text1 == projected_text2
        rec["projection_schema"] = {"volatile_keys": sorted(volatile_keys), "path_keys": sorted(path_keys)}
        if not rec["projection_stable"]:
            rec.update({"error": "AUDIT_PROJECTION_UNSTABLE",
                        "diff": _first_text_diff(projected_text1, projected_text2)})
            cases.append(rec)
            continue
        if not rec["raw_stable"]:
            # r288 (GATE-01 — audit lõi 31-07): raw drift HẾT là ghi chú quan sát. Mọi dòng stdout lệch phải
            # QUY được về một khoá ĐÃ KHAI trong `volatile_keys`/`path_keys` của chính case; chạm khoá CHƯA
            # KHAI — hoặc có dòng không quy được về khoá nào — ⇒ case ĐỎ và `--write` TỪ CHỐI ghi fixture
            # (lỗ nặng nhất của bản cũ: đóng băng luôn cái bất định vào golden).
            # ★ ĐO TRƯỚC KHI VÁ (31-07, scripts/.tl_state/deploy/golden.out): 20 case, ĐÚNG 1 case
            #   raw-unstable (`sweep`), dòng lệch DUY NHẤT là `snapshot_age_s` — vốn ĐÃ khai volatile.
            #   Nên bản vá này giữ `sweep` XANH. Hai phương án từng cân nhắc và BÁC:
            #   (a) "raw_stable=false ⇒ ok=false" trần trụi → gate ĐỎ NGAY ở case hoàn toàn lành;
            #   (b) scrub/đóng băng `snapshot_age_s` khỏi raw → raw hết là raw, mất luôn khả năng phát
            #       hiện bất định THẬT, và tự mâu thuẫn với chính điều "không nới định nghĩa raw-stability".
            rec["raw_diff"] = _first_text_diff(_raw1, _raw2)
            # r294: `_raw_drift_keys` nay trả ĐƯỜNG DẪN khoá (tuple gốc→lá). Một đường dẫn coi là ĐÃ
            # KHAI nếu BẤT KỲ mắt xích nào của nó được khai — ĐỐI XỨNG với `audit_projection`, vốn che
            # TRỌN CÂY CON của khoá đã khai (`deterministic.py`: `out[key] = "<volatile>"`). Trước r294
            # phép so là `k not in ...` trên TÊN KHOÁ LÁ ⇒ drift bên trong một khoá container ĐÃ KHAI
            # (vd `basis` của `doc_claims_check_fixture` — dict 13 trường) sinh khoá lá chưa khai ⇒
            # RAW_UNSTABLE_UNDECLARED = BÁO GIẢ, đúng cái hậu quả mà chú thích trên đã BÁC phương án (a)
            # để tránh. Báo cáo vẫn in dạng `cha.con` cho người đọc; phép so dùng TUPLE nên khoá có dấu
            # chấm trong tên không bị tách nhầm.
            _khai294 = volatile_keys | path_keys
            _drift_keys, _all_attributed = _raw_drift_keys(_raw1, _raw2)
            _undeclared = [".".join(p) for p in _drift_keys if not (set(p) & _khai294)]
            rec["raw_drift_keys"] = [".".join(p) for p in _drift_keys]
            rec["raw_drift_undeclared"] = _undeclared
            rec["raw_drift_attributed"] = _all_attributed
            if _undeclared or not _all_attributed:
                rec.update({"ok": False, "error": "RAW_UNSTABLE_UNDECLARED", "written": False,
                            "note": ("stdout lệch ở khoá CHƯA khai volatile/path — khai vào case nếu đúng là "
                                     "giá trị volatile, KHÔNG nới định nghĩa raw-stability"
                                     if _undeclared else
                                     "stdout lệch ở dòng KHÔNG quy được về khoá JSON nào ⇒ fail-closed")})
                cases.append(rec)
                continue
        actual = projected_text1
        actual_hash = hashlib.sha256(actual.encode("utf-8")).hexdigest()
        rec["actual_sha256"] = actual_hash
        if write:
            _write_text_atomic(path, actual)
            rec.update({"ok": True, "written": True})
        elif not path.exists():
            rec.update({"error": "GOLDEN_FILE_MISSING", "expected_path": str(path)})
        else:
            expected = path.read_text(encoding="utf-8", errors="replace")
            expected_hash = hashlib.sha256(expected.encode("utf-8")).hexdigest()
            same = expected == actual
            rec.update({"ok": same, "expected_sha256": expected_hash, "diff": {} if same else _first_text_diff(expected, actual)})
            if not same:
                rec["error"] = "GOLDEN_MISMATCH"
        cases.append(rec)
    ok = all(c.get("ok") for c in cases)
    out = {"ok": ok, "schema": "golden_test.v1", "golden_dir": str(gdir), "case_count": len(cases), "cases": cases}
    # r293 (hoà nhánh): mã lỗi RIÊNG nổi lên TOP để người đọc phân biệt "fixture lệch" (GOLDEN_MISMATCH —
    # chữa bằng cách xem lại thay đổi) với "lệnh bất định" (RAW_UNSTABLE_UNDECLARED — CẤM regen, phải làm
    # tất định trước). Hai bệnh khác nhau, cách chữa NGƯỢC nhau; gộp một mã là mời người ta chạy `--write`
    # cho xong. Cơ chế phát hiện là của r288 (quy-khoá) — khối này CHỈ nổi kết luận lên đầu payload để
    # CI/`deploy-package.sh` đọc được mà không phải duyệt 20 case.
    _raw_bad = [c["id"] for c in cases if c.get("error") == "RAW_UNSTABLE_UNDECLARED"]
    if _raw_bad:
        out["error"] = "RAW_UNSTABLE_UNDECLARED"
        out["raw_unstable_cases"] = _raw_bad
        if write:
            out["write_refused"] = True
    return out


def cmd_golden_test(a) -> int:
    out = _golden_test(write=bool(getattr(a, "write", False)))
    _print_json_or_text(out, getattr(a, "json", False))
    return 0 if out.get("ok") else 2

# ── I11 (v1.34.18): leftover-sweep từ tl.py (affinity-tốt-nhất) ──


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

def _raw_key_paths_by_line(text: str) -> list[tuple]:
    """r294: với MỖI dòng của `text`, trả ĐƯỜNG DẪN khoá JSON (tuple gốc→lá) chứa dòng đó.

    Dựa vào ĐỘ THỤT: stdout của gate luôn là JSON `indent=2` (`deterministic.py` `_json_dumps`), nên
    độ thụt CHÍNH LÀ độ sâu lồng. Dòng `"k":` ở thụt d là con của khoá gần nhất có thụt < d.
    Dòng KHÔNG phải khoá (phần tử mảng, ngoặc đóng/mở) nhận đường dẫn của khoá đang mở — nhờ vậy một
    phần tử mảng lệch bên trong khoá ĐÃ KHAI không còn bị coi là "không quy được".
    Dòng ở NGOÀI mọi khoá (vd banner không phải JSON) nhận `()` ⇒ người gọi vẫn fail-closed.
    """
    import re as _re294
    out, stack = [], []          # stack: [(thụt, tên khoá), …]
    for ln in text.splitlines():
        s = ln.lstrip()
        ind = len(ln) - len(s)
        while stack and stack[-1][0] >= ind:
            stack.pop()
        m = _re294.match(r'"((?:[^"\\]|\\.)*)"\s*:', s)
        if m:
            out.append(tuple(k for _i, k in stack) + (m.group(1),))
            stack.append((ind, m.group(1)))
        else:
            out.append(tuple(k for _i, k in stack))
    return out


def _raw_drift_keys(a: str, b: str) -> tuple[list[tuple], bool]:
    """r288 (GATE-01 — audit lõi 31-07): quy MỌI dòng stdout lệch giữa hai lượt về KHOÁ JSON của nó.

    r294: trả **ĐƯỜNG DẪN** khoá (tuple gốc→lá) thay cho tên khoá lá, để phép so của người gọi ĐỐI XỨNG
    được với `audit_projection` — vốn che TRỌN CÂY CON của khoá đã khai. Bản r288 trả tên lá nên drift
    nằm BÊN TRONG một khoá container đã khai bị hô là chưa khai ⇒ BÁO GIẢ.

    Trả `(danh sách đường dẫn đã sắp xếp, quy_được_hết)`. Dòng lệch nào nằm NGOÀI mọi khoá ⇒
    `quy_được_hết=False`, và người gọi PHẢI fail-closed. Tuyệt đối không được đọc "không quy được khoá
    nào" thành "không có khoá nào lệch" — đó đúng là chỗ fail-OPEN mà GATE-01 sinh ra để chặn.
    """
    import difflib as _dl288
    a_lines, b_lines = a.splitlines(), b.splitlines()
    a_paths, b_paths = _raw_key_paths_by_line(a), _raw_key_paths_by_line(b)
    keys, attributed = set(), True
    for tag, i1, i2, j1, j2 in _dl288.SequenceMatcher(None, a_lines, b_lines, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        for p in a_paths[i1:i2] + b_paths[j1:j2]:
            if p:
                keys.add(p)
            else:
                attributed = False
    return sorted(keys), attributed


def _first_text_diff(expected: str, actual: str) -> dict:
    exp_lines = expected.splitlines()
    act_lines = actual.splitlines()
    for idx, (e, a) in enumerate(zip(exp_lines, act_lines), 1):
        if e != a:
            return {"line": idx, "expected": e[:240], "actual": a[:240]}
    if len(exp_lines) != len(act_lines):
        return {"line": min(len(exp_lines), len(act_lines)) + 1, "expected": "<EOF>" if len(exp_lines) < len(act_lines) else exp_lines[-1][:240], "actual": "<EOF>" if len(act_lines) < len(exp_lines) else act_lines[-1][:240]}
    return {}
