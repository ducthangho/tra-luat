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
    {"name": "release-bundle", "handler": "cmd_release_bundle",
     "help": "OFFLINE: đóng gói zip tất định kèm RELEASE_MANIFEST.json; không gọi mạng",
     "args": [
         {"flags": ["--root"], "help": "root gói skill; mặc định HERE.parent"},
         {"flags": ["--out"], "required": True, "help": "đường dẫn zip output"},
         {"flags": ["--top"], "help": "tên thư mục top-level trong zip; mặc định tên root"},
         {"flags": ["--json"], "action": "store_true"},
     ]},
]


def register_generated(sub, tl_module) -> list[str]:
    """Sinh parser cho GENERATED_SPECS; handler resolve từ tl_module (stub ủy quyền). Trả list tên đã sinh."""
    made = []
    for spec in GENERATED_SPECS:
        p = sub.add_parser(spec["name"], help=spec["help"])
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
    "release-check":        _m("medium", False, "local", False, False, True, "release_check", None, True, "release"),
    "live-readiness":       _m("medium", True, "none", False, False, True, "live_readiness", None, True, "live"),
    "live-contract-check":  _m("medium", True, "none", False, False, True, "live_contract_check", None, True, "live"),
    "live-state-snapshot":  _m("medium", True, "local", False, False, True, "live_state_snapshot", None, True, "live"),
    "live-state-diff":      _m("low", True, "none", False, False, True, "live_state_diff", None, True, "live"),
    "live-smoke-plan":      _m("low", True, "none", False, False, True, "live_smoke_plan", None, True, "live"),
    "deploy-plan":          _m("medium", True, "none", False, False, True, "deploy_plan", None, True, "live"),
    "rollback-plan":        _m("medium", True, "none", False, False, True, "rollback_plan", None, True, "live"),
    "final-acceptance":     _m("medium", True, "none", False, False, True, "final_acceptance", None, True, "live"),
    "go-live-runbook":      _m("medium", True, "none", False, False, True, "go_live_runbook", None, True, "live"),
    "ingest-zip":           _m("high", False, "drive_registry_nlm", True, True, True, "ingest_zip", "ingest_zip", True, "zip_ingest"),
    "profile-ingest-zip":   _m("high", False, "drive_registry_nlm", True, True, True, "ingest_zip", "ingest_zip", True, "zip_ingest"),
    "ocr-analyze":          _m("low", True, "none", False, False, True, "ocr_pdf_scan", None, True, "ocr"),
    "ocr-run":              _m("medium", False, "local", False, True, True, "ocr_pdf_scan", None, True, "ocr"),
    "ocr-verify":           _m("low", True, "none", False, False, True, "ocr_pdf_scan", None, True, "ocr"),
    "ingest-ocr":           _m("high", False, "drive_registry_nlm", True, True, True, "ocr_ingest", "ocr_ingest", True, "ocr"),
    "profile-ingest-ocr":   _m("high", False, "drive_registry_nlm", True, True, True, "ocr_ingest", "profile_ingest_ocr", True, "ocr"),
    "chunk-plan":           _m("low", True, "none", False, False, True, "large_doc_chunk", None, True, "chunking"),
    "chunk-apply":          _m("medium", False, "local", False, True, True, "large_doc_chunk", None, True, "chunking"),
    "chunk-verify":         _m("low", True, "none", False, False, True, "chunk_ingest", None, True, "chunking"),
    "profile-ingest-chunks": _m("high", False, "drive_registry_nlm", True, True, True, "chunk_ingest", "profile_ingest_chunks", True, "chunking"),
    "convert-verify":       _m("low", True, "none", False, False, True, "convert_rename", None, True, None),
    "nlm-query-plan":       _m("low", True, "none", False, False, True, "nlm_query_quality", None, True, None),
    # ── legacy write high-risk (GRANDFATHER: card_required=False trừ khi card đã có; gate = --apply dry-run) ──
    "ingest-local":         _m("high", False, "drive_registry_nlm", False, True, False, "ingest_local", "ingest_local", True, None),
    "profile-ingest":       _m("high", False, "drive_registry_nlm", False, True, False, "ingest_local", "profile_ingest", True, None),
    "nlm-add":              dict(_m("high", False, "nlm", False, False, False, None, None, False, None),
                                 builtin_gate="nlm_dedup_live_gate"),
    "recat":                _m("high", False, "drive_registry", False, True, False, None, None, False, None),
    "source-rename":        _m("high", False, "drive_registry_nlm", False, True, False, None, None, False, None),
    "source-delete":        _m("high", False, "drive_registry_nlm", True, False, False, None, None, False, None),
    "source-update-corpus": _m("high", False, "registry_nlm", False, True, False, None, None, False, None),
    "dedup-plan":           _m("high", False, "registry_nlm", False, True, False, None, None, False, None),
    "register":             _m("high", False, "registry", False, True, False, None, None, False, None),
    "backfill-loai":        _m("medium", False, "registry", False, True, False, None, None, False, None),
    "backfill-title-vn":    _m("medium", False, "registry", False, True, False, None, None, False, None),
    "backfill-hieuluc":     _m("medium", False, "registry", False, True, False, None, None, False, None),
    "drive-push":           dict(_m("high", False, "drive", False, False, False, None, None, False, None),
                                 builtin_gate="md5_verify_fixed_fileid"),
    "reg-delete":           _m("high", False, "registry", True, False, False, None, None, False, None),
    "vbhn-year-fix":        _m("medium", False, "registry", False, True, False, None, None, False, None),
    "quarantine-fix":       _m("medium", False, "registry", False, True, False, None, None, False, None),
    "shared-source-fix":    _m("high", False, "registry_nlm", False, True, False, None, None, False, None),
    "corpus-fix":           _m("medium", False, "registry", False, True, False, None, None, False, None),
    "push-overflow":        _m("high", False, "nlm_registry", False, True, False, None, None, False, None),
    "nlm-reconcile":        _m("high", False, "registry_nlm", False, True, False, None, None, False, None),
    "missing-sohieu":       _m("medium", False, "registry", False, True, False, None, None, False, None),
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
        if m["risk"] == "high" and not m["read_only"] and not m["idempotency_contract"]:
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
