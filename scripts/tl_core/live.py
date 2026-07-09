# -*- coding: utf-8 -*-
"""tl_core.live — Pha C (v1.33.56): tách NGUYÊN VĂN từ scripts/tl.py (kế hoạch nợ-kỹ-thuật C3).

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

_TL = None


def bind(tl_module) -> None:
    global _TL
    _TL = tl_module
    g = globals()
    for _n in dir(tl_module):
        if _n.startswith("__") or _n in g:
            continue
        g[_n] = getattr(tl_module, _n)



def _live_smoke_plan(profile: str = "", include_ocr: bool = False) -> dict:
    """Produce a deterministic live acceptance plan. Does not call Drive/NLM."""
    profile_arg = ["--profile", profile] if profile else []
    steps = [
        {"id": "readiness_3tier", "risk": "low", "command": ["live-readiness", "--json"], "expect": "env_ready=true; live_contract_ready=true; apply_ready=false nếu chưa có smoke proof"},
        {"id": "contract_readonly", "risk": "low", "command": ["live-contract-check", "--json"], "expect": "webapp ping/info + NLM get/list read-only pass"},
        {"id": "snapshot_before", "risk": "low", "command": ["live-state-snapshot", "--out", ".tl_state/before.json", "--json"], "expect": "baseline live state saved before smoke"},
        {"id": "health", "risk": "low", "command": ["ping", "--json"], "expect": "ok=true; webapp version accepted"},
        {"id": "doctor", "risk": "low", "command": ["doctor", "--json"], "expect": "config/profile/registry/notebook readable"},
        {"id": "inventory", "risk": "low", "command": ["tool-inventory", "--json"], "expect": "inventory ok"},
        {"id": "workflow_audit", "risk": "low", "command": ["workflow-audit", "--json"], "expect": "workflow cards and route map ok"},
        {"id": "release_manifest", "risk": "low", "command": ["release-manifest", "--json", "--out", "RELEASE_MANIFEST.json"], "expect": "package manifest with SHA-256"},
        {"id": "release_verify", "risk": "low", "command": ["release-verify", "RELEASE_MANIFEST.json", "--json"], "expect": "hashes and required files verified"},
        {"id": "route_convert", "risk": "low", "command": ["route-task", "--task", "convert_rename", "--json"], "expect": "readback required"},
        {"id": "zip_dry_run", "risk": "low", "command": ["ingest-zip", "<sample.zip>", "--cat", "01", "--json"], "expect": "batch plan only; no Drive write"},
        {"id": "profile_zip_dry_run", "risk": "low", "command": ["profile-ingest-zip", "<sample.zip>", "--json"] + profile_arg, "expect": "profile batch plan only"},
        {"id": "convert_live_docx", "risk": "high", "command": ["ingest-local", "<small.docx>", "--cat", "01", "--apply", "--json"], "expect": "upload→Drive convert→rename→readback→register/NLM; no binary add NLM"},
        {"id": "profile_live_docx", "risk": "high", "command": ["profile-ingest", "<small.docx>", "--apply", "--json"] + profile_arg, "expect": "profile canonical GDoc verified before NLM"},
        {"id": "zip_apply_guard", "risk": "medium", "command": ["ingest-zip", "<sample.zip>", "--cat", "01", "--apply", "--json"], "expect": "must fail without --confirm yes"},
        {"id": "snapshot_after", "risk": "low", "command": ["live-state-snapshot", "--out", ".tl_state/after.json", "--json"], "expect": "state saved after smoke"},
        {"id": "snapshot_diff", "risk": "low", "command": ["live-state-diff", ".tl_state/before.json", ".tl_state/after.json", "--json", "--allow", "source_counts", "--allow", "notebooks.get.source_count",
                                                          # v1.34.2 (Pha H live bắt): path THẬT của source-count trong snapshot nằm dưới live_contract_report.*
                                                          # (nlm.notebook_get.source_count + contract_checks[N].detail.*) — thiếu 2 prefix này thì mọi lần ghi
                                                          # hợp lệ giữa 2 snapshot đều bị báo 'unexpected' oan. contract_checks được phép rộng vì bước 2
                                                          # (live-contract-check) đã verify contract riêng TRƯỚC đó.
                                                          "--allow", "live_contract_report.nlm.notebook_get.source_count",
                                                          "--allow", "live_contract_report.contract_checks"], "expect": "unexpected_changes=[]"},
    ]
    if include_ocr:
        steps.extend([
            {"id": "ocr_analyze", "risk": "low", "command": ["ocr-analyze", "<scan.pdf>", "--json"], "expect": "detect text-layer or recommend OCR"},
            {"id": "ocr_run_local", "risk": "medium", "command": ["ocr-run", "<scan.pdf>", "--engine", "auto", "--mode", "profile", "--json"], "expect": "sidecar text local only; no Drive write"},
            {"id": "ocr_verify", "risk": "medium", "command": ["ocr-verify", "<sidecar.txt>", "--mode", "profile", "--json"], "expect": "verified before --ocr-verified"},
        ])
    return {"ok": True, "schema": "live_smoke_plan.v1", "profile": profile or None, "include_ocr": include_ocr,
            "note": "READ-ONLY plan. Chạy từng bước trên máy có TL_WEBAPP/TL_TOKEN/GWS/NLM auth. Thay placeholder <...> bằng file mẫu thật.",
            "steps": steps,
            "stop_rule": "Dừng ngay khi bước high-risk fail; không chạy bước apply tiếp theo trước khi đọc report/readback."}


def cmd_live_smoke_plan(a) -> int:
    out = _live_smoke_plan(profile=getattr(a, "profile", None) or "", include_ocr=bool(getattr(a, "include_ocr", False)))
    _print_json_or_text(out, getattr(a, "json", False))
    return 0


def _safe_bool(v) -> bool:
    return bool(str(v or "").strip())


def _mask_secret(v: str | None) -> str:
    s = str(v or "")
    if not s:
        return ""
    if len(s) <= 8:
        return "***"
    return s[:4] + "…" + s[-4:]


def _live_config_context(profile: str = "", config: str = "") -> dict:
    """Read local config/profile context without printing secrets and without network calls."""
    cfg_path, cfg = _read_config_record(config)
    cfg = cfg if isinstance(cfg, dict) else {}
    profiles = _profiles_from_config(cfg) if cfg else {}
    selected0 = _selected_profile_name(profile, cfg)
    selected, hit = _profile_lookup(profiles, selected0) if profiles else (selected0 or DEFAULT_PROFILE, None)
    prof = hit or (profiles.get(DEFAULT_PROFILE) if selected == DEFAULT_PROFILE else {}) or {}
    def val(*names, env: str = "") -> str:
        if env and os.environ.get(env):
            return str(os.environ.get(env) or "").strip()
        for n in names:
            v = prof.get(n) if isinstance(prof, dict) else None
            if v:
                return str(v).strip()
        for n in names:
            v = cfg.get(n) if isinstance(cfg, dict) else None
            if v:
                return str(v).strip()
        return ""
    webapp = os.environ.get("TL_WEBAPP") or cfg.get("webappUrl") or cfg.get("TL_WEBAPP") or cfg.get("webapp") or ""
    token = os.environ.get("TL_TOKEN") or cfg.get("token") or cfg.get("TL_TOKEN") or ""
    ids = {
        "root_folder_id": val("rootFolderId", "root_id", "root", env="TL_ROOT_FOLDER_ID"),
        "meta_folder_id": val("metaFolderId", env="TL_META_FOLDER_ID"),
        "registry_doc_id": val("registryDocId", env="TL_REGISTRY_DOC_ID"),
        "manifest_id": val("manifestId", "TL_MANIFEST_ID", env="TL_MANIFEST_ID"),
        "notebook_id": val("notebookId", "notebookVbqpplId", "nlmNotebookId", env="TL_NOTEBOOK_ID"),
        "overflow_notebook_id": val("overflowNotebookId", env="TL_OVERFLOW_NOTEBOOK_ID"),
    }
    return {
        "config_path": cfg_path or "",
        "config_present": bool(cfg_path and Path(cfg_path).exists()),
        "config_readable": bool(cfg),
        "config_schema": cfg.get("schema") if isinstance(cfg, dict) else None,
        "default_profile": cfg.get("defaultProfile", DEFAULT_PROFILE) if isinstance(cfg, dict) else DEFAULT_PROFILE,
        "active_profile": selected,
        "profile_requested": profile or None,
        "profile_found": bool(hit) or (selected == DEFAULT_PROFILE and bool(prof)),
        "profile_names": sorted(profiles) if profiles else [],
        "ids": ids,
        "webapp_present": _safe_bool(webapp),
        "webapp_masked": _mask_secret(webapp),
        "token_present": _safe_bool(token),
        "token_masked": _mask_secret(token),
    }


def _live_env_report(profile: str = "", *, include_ocr: bool = False, config: str = "") -> dict:
    """Pha 6: readiness layer 1. Local/env/auth only; no Drive/NLM network calls."""
    home = Path.home()
    ctx = _live_config_context(profile, config)
    gws_cred = home / ".config" / "gws" / "credentials.json"
    nlm_dir = home / ".notebooklm-mcp-cli"
    nlm_cookie_candidates = [nlm_dir / "cookies.json", nlm_dir / "auth.json", nlm_dir / "storage_state.json"]
    nlm_auth_file = next((x for x in nlm_cookie_candidates if x.exists()), None)
    commands = {name: shutil.which(name) for name in ["gws", "nlm", "ocrmypdf", "tesseract"]}
    required_files = ["VERSION", "SKILL.md", "scripts/tl.py", "scripts/gen_instructions.py", "references/API_CONTRACT.md"]
    file_checks = [{"path": x, "exists": (HERE.parent / x).exists()} for x in required_files]
    checks = [
        {"id": "python_version", "ok": sys.version_info >= (3, 10), "detail": sys.version.split()[0], "tier": "offline"},
        {"id": "skill_root", "ok": (HERE.parent / "SKILL.md").exists(), "detail": str(HERE.parent), "tier": "offline"},
        {"id": "required_files", "ok": all(x["exists"] for x in file_checks), "detail": file_checks, "tier": "offline"},
        {"id": "config_present", "ok": ctx["config_present"], "detail": ctx.get("config_path") or "missing", "tier": "env"},
        {"id": "credential_source_present", "ok": ctx["config_present"] or (ctx["webapp_present"] and ctx["token_present"]), "detail": "config_or_env", "tier": "env"},
        {"id": "webapp_present", "ok": ctx["webapp_present"], "detail": ctx["webapp_masked"], "tier": "env"},
        {"id": "token_present", "ok": ctx["token_present"], "detail": ctx["token_masked"], "tier": "env"},
        {"id": "gws_binary", "ok": bool(commands.get("gws")), "detail": commands.get("gws") or "missing", "tier": "env"},
        {"id": "gws_credentials", "ok": gws_cred.exists(), "detail": _file_auth_state(gws_cred), "tier": "env"},
        {"id": "nlm_binary", "ok": bool(commands.get("nlm")), "detail": commands.get("nlm") or "missing", "tier": "env"},
        {"id": "nlm_auth_dir", "ok": nlm_dir.exists(), "detail": str(nlm_dir), "tier": "env"},
        {"id": "nlm_auth_file", "ok": bool(nlm_auth_file), "detail": _file_auth_state(nlm_auth_file) if nlm_auth_file else "missing", "tier": "env"},
    ]
    if profile:
        checks.append({"id": "profile_requested", "ok": True, "detail": profile, "tier": "env"})
    if include_ocr:
        checks.extend([
            {"id": "ocrmypdf_binary", "ok": bool(commands.get("ocrmypdf")), "detail": commands.get("ocrmypdf") or "optional_missing", "tier": "optional_ocr"},
            {"id": "tesseract_binary", "ok": bool(commands.get("tesseract")), "detail": commands.get("tesseract") or "optional_missing", "tier": "optional_ocr"},
        ])
    offline_ids = {"python_version", "skill_root", "required_files"}
    env_ids = {"credential_source_present", "webapp_present", "token_present", "gws_binary", "gws_credentials", "nlm_binary", "nlm_auth_file"}
    offline_fail = [c for c in checks if c["id"] in offline_ids and not c.get("ok")]
    env_fail = [c for c in checks if c["id"] in env_ids and not c.get("ok")]
    warnings = [c for c in checks if c["id"] not in offline_ids | env_ids and not c.get("ok")]
    ready_for_offline_release = not offline_fail
    env_ready = ready_for_offline_release and not env_fail
    return {
        "ok": True,
        "schema": "live_env_report.v1",
        "profile": profile or None,
        "active_profile": ctx.get("active_profile"),
        "include_ocr": include_ocr,
        "env_ready": env_ready,
        "ready_for_offline_release": ready_for_offline_release,
        "checks": checks,
        "offline_failures": offline_fail,
        "env_failures": env_fail,
        "warnings": warnings,
        "profile_context": ctx,
        "auth_state": {
            "gws_credentials": _file_auth_state(gws_cred),
            "nlm_auth_file": _file_auth_state(nlm_auth_file) if nlm_auth_file else {"path": "", "exists": False, "age_days": None},
        },
        "secret_policy": "Không in token/webapp đầy đủ; chỉ mask để xác nhận có cấu hình.",
    }


def _live_contract_check_report(profile: str = "", *, config: str = "", include_ocr: bool = False, timeout: int = 60) -> dict:
    """Pha 6: readiness layer 2. READ-ONLY live calls only: ping/info/NLM get/list."""
    env = _live_env_report(profile, include_ocr=include_ocr, config=config)
    ctx = env.get("profile_context") or {}
    contract_checks = []
    def add(cid: str, ok: bool, detail=None, **extra):
        rec = {"id": cid, "ok": bool(ok), "detail": detail if detail is not None else ""}
        rec.update(extra)
        contract_checks.append(rec)
        return rec
    if not env.get("env_ready"):
        return {
            "ok": True,
            "command_ok": True,
            "deployment_allowed": False,
            "schema": "live_contract_check.v1",
            "env_ready": False,
            "live_contract_ready": False,
            "apply_ready": False,
            "profile": profile or None,
            "active_profile": ctx.get("active_profile"),
            "skipped": True,
            "skip_reason": "ENV_NOT_READY",
            "env_failures": env.get("env_failures", []),
            "contract_checks": contract_checks,
            "policy": "READ-ONLY only: webapp ping/info + NLM notebook get/source list. No upload/register/add source.",
        }
    try:
        load_creds(config or None, profile or None)
    except SystemExit as e:
        add("load_creds", False, str(e))
        return {"ok": True, "command_ok": True, "deployment_allowed": False, "schema": "live_contract_check.v1", "env_ready": True, "live_contract_ready": False,
                "apply_ready": False, "profile": profile or None, "active_profile": ctx.get("active_profile"),
                "contract_checks": contract_checks, "policy": "READ-ONLY only"}
    g = _gas()
    ping = {}
    try:
        ping = g.get("ping")
        add("webapp_ping", bool(ping.get("version")), {"version": ping.get("version"), "expect": EXPECT_VERSION})
        add("webapp_version_match", ping.get("version") == EXPECT_VERSION, {"version": ping.get("version"), "expect": EXPECT_VERSION})
    except Exception as e:  # noqa: BLE001
        add("webapp_ping", False, f"{type(e).__name__}: {e}")
    ids = (ctx.get("ids") or {}).copy()
    # load_creds/_apply_profile_env may have overlaid env values after ctx was built.
    ids.update({
        "root_folder_id": os.environ.get("TL_ROOT_FOLDER_ID") or ids.get("root_folder_id") or "",
        "meta_folder_id": os.environ.get("TL_META_FOLDER_ID") or ids.get("meta_folder_id") or "",
        "registry_doc_id": os.environ.get("TL_REGISTRY_DOC_ID") or ids.get("registry_doc_id") or "",
        "manifest_id": os.environ.get("TL_MANIFEST_ID") or ids.get("manifest_id") or "",
        "notebook_id": os.environ.get("TL_NOTEBOOK_ID") or ids.get("notebook_id") or "",
    })
    drive_info = {}
    for kind in ["root_folder_id", "meta_folder_id", "registry_doc_id", "manifest_id"]:
        fid = (ids.get(kind) or "").strip()
        if not fid:
            add(f"drive_info:{kind}", kind in {"meta_folder_id", "manifest_id"}, "MISSING_OPTIONAL" if kind in {"meta_folder_id", "manifest_id"} else "MISSING_REQUIRED")
            continue
        inf = _drive_info_file(g, fid)
        f = inf.get("file") or {}
        drive_info[kind] = {"ok": bool(inf.get("ok")), "id": fid, "name": f.get("name") or f.get("title"), "mimeType": f.get("mimeType") or f.get("mime")}
        add(f"drive_info:{kind}", bool(inf.get("ok")), drive_info[kind])
    nb = (ids.get("notebook_id") or "").strip()
    if not nb:
        try:
            nb, nb_err = _resolve_nlm_notebook(None)
            if nb_err:
                add("nlm_notebook_resolve", False, nb_err)
        except Exception as e:  # noqa: BLE001
            add("nlm_notebook_resolve", False, f"{type(e).__name__}: {e}")
    nlm = {"notebook_id": nb or "", "notebook_get": {}, "source_list": {}, "source_count": None}
    if nb:
        try:
            nc = _imp("nlm_cli")
            nget = nc.notebook_get(nb)
            nlm["notebook_get"] = {k: nget.get(k) for k in ("ok", "source_count", "title", "via", "error", "fallback")}
            add("nlm_notebook_get", bool(nget.get("ok")), nlm["notebook_get"])
            sl = nc.source_list(nb, skip_freshness=True)
            nlm["source_list"] = {k: sl.get(k) for k in ("ok", "count", "skip_freshness", "error")}
            nlm["source_count"] = sl.get("count") if sl.get("ok") else nget.get("source_count")
            add("nlm_source_list", bool(sl.get("ok")), nlm["source_list"])
        except Exception as e:  # noqa: BLE001
            add("nlm_readonly", False, f"{type(e).__name__}: {e}")
    else:
        add("nlm_notebook_id", False, "MISSING_REQUIRED")
    # v1.33.56 (review F2): nhánh fail NLM (thiếu notebook_id / resolver lỗi / nlm_cli raise) ghi check id
    # NGOÀI tập required → live_contract_ready=true dù CHƯA kiểm chứng NLM nào (false-green tín hiệu deploy).
    required_prefixes = {"webapp_ping", "webapp_version_match", "drive_info:root_folder_id", "drive_info:registry_doc_id",
                         "nlm_notebook_get", "nlm_source_list", "nlm_notebook_id", "nlm_notebook_resolve", "nlm_readonly"}
    failed_required = [c for c in contract_checks if c["id"] in required_prefixes and not c.get("ok")]
    live_contract_ready = not failed_required and any(c["id"] == "webapp_version_match" and c.get("ok") for c in contract_checks)
    return {
        "ok": True,
        "command_ok": True,
        "deployment_allowed": False,
        "schema": "live_contract_check.v1",
        "env_ready": True,
        "live_contract_ready": live_contract_ready,
        "apply_ready": False,
        "profile": profile or None,
        "active_profile": os.environ.get("TL_PROFILE") or ctx.get("active_profile"),
        "webapp": {"version": ping.get("version"), "expect": EXPECT_VERSION, "match": ping.get("version") == EXPECT_VERSION},
        "ids": ids,
        "drive_info": drive_info,
        "nlm": nlm,
        "contract_checks": contract_checks,
        "failed_required": failed_required,
        "policy": "READ-ONLY only: webapp ping/info + NLM notebook get/source list. No upload/register/add source.",
        "timeout_seconds": timeout,
    }


def _smoke_proof_state(path: str = "") -> dict:
    if not path:
        return {"provided": False, "ok": False, "path": "", "reason": "SMOKE_PROOF_NOT_PROVIDED"}
    p = Path(path).expanduser()
    if not p.exists():
        return {"provided": True, "ok": False, "path": str(p), "reason": "SMOKE_PROOF_NOT_FOUND"}
    try:
        data = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        ok = bool(data.get("ok")) and not data.get("unexpected_changes")
        return {"provided": True, "ok": ok, "path": str(p), "schema": data.get("schema"), "summary": data.get("summary")}
    except Exception as e:  # noqa: BLE001
        return {"provided": True, "ok": False, "path": str(p), "reason": f"{type(e).__name__}: {e}"}


def _live_readiness_report(profile: str = "", *, include_ocr: bool = False, config: str = "", check_contract: bool = True, smoke_proof: str = "") -> dict:
    """Pha 6: readiness report with explicit env/contract/apply tiers."""
    env = _live_env_report(profile, include_ocr=include_ocr, config=config)
    contract = {"schema": "live_contract_check.v1", "env_ready": env.get("env_ready"), "live_contract_ready": False,
                "apply_ready": False, "skipped": True, "skip_reason": "CONTRACT_CHECK_SKIPPED"}
    if check_contract and env.get("env_ready"):
        contract = _live_contract_check_report(profile, config=config, include_ocr=include_ocr)
    elif check_contract and not env.get("env_ready"):
        contract["skip_reason"] = "ENV_NOT_READY"
    smoke = _smoke_proof_state(smoke_proof)
    env_ready = bool(env.get("env_ready"))
    contract_ready = bool(contract.get("live_contract_ready"))
    apply_ready = env_ready and contract_ready and bool(smoke.get("ok"))
    return {
        "ok": True,
        "command_ok": True,
        "deployment_allowed": apply_ready,
        "schema": "live_readiness.v2",
        "tiers": {
            "env_ready": env_ready,
            "live_contract_ready": contract_ready,
            "apply_ready": apply_ready,
        },
        "env_ready": env_ready,
        "live_contract_ready": contract_ready,
        "apply_ready": apply_ready,
        "ready_for_offline_release": bool(env.get("ready_for_offline_release")),
        "ready_for_live_smoke": env_ready and contract_ready,
        "profile": profile or None,
        "active_profile": env.get("active_profile"),
        "include_ocr": include_ocr,
        "env_report": env,
        "live_contract_report": contract,
        "smoke_proof": smoke,
        "checks": env.get("checks", []) + contract.get("contract_checks", []),
        "hard_failures": env.get("offline_failures", []) + env.get("env_failures", []) + contract.get("failed_required", []),
        "secret_policy": "Không in token/webapp đầy đủ; chỉ mask để xác nhận có cấu hình.",
        "ok_semantics": "ok/command_ok chỉ nghĩa là lệnh chạy xong; deployment_allowed mới là quyền tiếp tục apply.",
        "next": "Chạy `tl live-state-snapshot --out .tl_state/before.json --json`, smoke test, `tl live-state-snapshot --out .tl_state/after.json --json`, rồi `tl live-state-diff .tl_state/before.json .tl_state/after.json --json --allow <expected_path>` trước khi apply rộng.",
    }


def cmd_live_contract_check(a) -> int:
    out = _live_contract_check_report(profile=getattr(a, "profile", None) or "",
                                      config=getattr(a, "config_file", None) or getattr(a, "config", None) or "",
                                      include_ocr=bool(getattr(a, "include_ocr", False)),
                                      timeout=int(getattr(a, "timeout", 60) or 60))
    _print_json_or_text(out, getattr(a, "json", False))
    return 2 if getattr(a, "strict", False) and not out.get("live_contract_ready") else 0


def cmd_live_readiness(a) -> int:
    out = _live_readiness_report(profile=getattr(a, "profile", None) or "",
                                 include_ocr=bool(getattr(a, "include_ocr", False)),
                                 config=getattr(a, "config_file", None) or getattr(a, "config", None) or "",
                                 check_contract=not bool(getattr(a, "skip_contract", False)),
                                 smoke_proof=getattr(a, "smoke_proof", None) or "")
    _print_json_or_text(out, getattr(a, "json", False))
    return 2 if getattr(a, "strict", False) and not out.get("ready_for_live_smoke") else 0


def _live_state_snapshot(profile: str = "", *, config: str = "", include_contract: bool = True, include_ocr: bool = False) -> dict:
    ctx = _live_config_context(profile, config)
    manifest = _build_release_manifest(HERE.parent)
    env = _live_env_report(profile, include_ocr=include_ocr, config=config)
    contract = _live_contract_check_report(profile, config=config, include_ocr=include_ocr) if include_contract else {"live_contract_ready": False, "skipped": True}
    ids = (contract.get("ids") or ctx.get("ids") or {}).copy()
    gws_v = _cmd_version_probe("gws")
    nlm_v = _cmd_version_probe("nlm")
    auth = env.get("auth_state", {})
    return {
        "ok": True,
        "schema": "live_state_snapshot.v1",
        "skill": {"name": "tra-luat", "version": (HERE.parent / "VERSION").read_text(encoding="utf-8", errors="replace").strip() if (HERE.parent / "VERSION").exists() else VERSION,
                  "package_hash": manifest.get("package_hash"), "file_count": manifest.get("file_count")},
        "webapp": {"version": (contract.get("webapp") or {}).get("version"), "expect": EXPECT_VERSION,
                   "match": (contract.get("webapp") or {}).get("match")},
        "profile": {"active": contract.get("active_profile") or ctx.get("active_profile"), "requested": profile or None,
                    "found": ctx.get("profile_found"), "config_path": ctx.get("config_path")},
        "registry": {"id": ids.get("registry_doc_id") or "", "info": (contract.get("drive_info") or {}).get("registry_doc_id")},
        "manifest": {"id": ids.get("manifest_id") or "", "info": (contract.get("drive_info") or {}).get("manifest_id")},
        "folders": {"root_folder_id": ids.get("root_folder_id") or "", "meta_folder_id": ids.get("meta_folder_id") or "",
                    "info": {k: v for k, v in (contract.get("drive_info") or {}).items() if k.endswith("folder_id")}},
        "notebooks": {"primary": ids.get("notebook_id") or (contract.get("nlm") or {}).get("notebook_id") or "",
                      "overflow": ids.get("overflow_notebook_id") or "",
                      "get": (contract.get("nlm") or {}).get("notebook_get")},
        "source_counts": {"nlm_live": (contract.get("nlm") or {}).get("source_count"),
                          "nlm_source_list": ((contract.get("nlm") or {}).get("source_list") or {}).get("count")},
        "auth": {"env_ready": env.get("env_ready"), "live_contract_ready": contract.get("live_contract_ready"),
                 "gws_credentials": auth.get("gws_credentials"), "nlm_auth_file": auth.get("nlm_auth_file")},
        "command_versions": {"python": sys.version.split()[0], "tl": VERSION, "gws": gws_v, "nlm": nlm_v},
        "selected_command_versions": {"release_manifest_schema": "release_manifest.v1", "live_readiness_schema": "live_readiness.v2",
                                      "live_contract_check_schema": "live_contract_check.v1"},
        "live_contract_report": contract,
        "volatile": {"generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "generatedEpoch": time.time()},
    }


def cmd_live_state_snapshot(a) -> int:
    out = _live_state_snapshot(profile=getattr(a, "profile", None) or "",
                               config=getattr(a, "config_file", None) or getattr(a, "config", None) or "",
                               include_contract=not bool(getattr(a, "no_contract", False)),
                               include_ocr=bool(getattr(a, "include_ocr", False)))
    if getattr(a, "out", None):
        _out_path = Path(a.out)
        try:
            _rel = _out_path.expanduser().resolve().relative_to(HERE.parent.resolve())
            if ".tl_state" not in _rel.parts:
                out.setdefault("warnings", []).append("WARNING_RUNTIME_ARTIFACT_INSIDE_SKILL_ROOT: prefer .tl_state/<name>.json so release manifest/hash stays clean")
        except Exception:
            pass
        _write_json_atomic(_out_path, _scrub_volatile(out) if _deterministic_enabled(a) else out)   # v1.33.56 FIX B
    _print_json_or_text(out, getattr(a, "json", False))
    return 0


def _strip_snapshot_volatile(obj):
    # v1.33.56 (ROOT-CAUSE flake determinism-audit 3 lần 'ok:false không tái hiện'): giữa 2 snapshot con,
    # auth.gws_credentials.age_days nhảy bucket 0.001-ngày (86.4s) → diff báo unexpected (~5%/lần chạy —
    # khớp tần suất). age_days ∈ _VOLATILE_JSON_KEYS nhưng hàm này CHỈ bỏ block 'volatile', KHÔNG bỏ key
    # volatile ở LEAF → bỏ cả hai (đúng luôn cho live-smoke thật: file snapshot raw, diff tự lọc nhiễu thời gian).
    if isinstance(obj, dict):
        return {k: _strip_snapshot_volatile(v) for k, v in obj.items()
                if k != "volatile" and str(k) not in _VOLATILE_JSON_KEYS}
    if isinstance(obj, list):
        return [_strip_snapshot_volatile(x) for x in obj]
    return obj


def _flatten_snapshot(obj, prefix: str = "") -> dict:
    out = {}
    if isinstance(obj, dict):
        for k in sorted(obj):
            pfx = f"{prefix}.{k}" if prefix else str(k)
            out.update(_flatten_snapshot(obj[k], pfx))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.update(_flatten_snapshot(v, f"{prefix}[{i}]"))
        if not obj:
            out[prefix] = []
    else:
        out[prefix] = obj
    return out


def _path_allowed(path: str, allowed: list[str]) -> bool:
    for a in allowed:
        a = str(a or "").strip()
        if not a:
            continue
        if path == a or path.startswith(a + ".") or path.startswith(a + "["):
            return True
    return False


def _live_state_diff(before_path: str, after_path: str, *, allowed: list[str] | None = None) -> dict:
    allowed = ["volatile"] + list(allowed or [])
    bp, ap = Path(before_path).expanduser(), Path(after_path).expanduser()
    before = json.loads(bp.read_text(encoding="utf-8", errors="replace"))
    after = json.loads(ap.read_text(encoding="utf-8", errors="replace"))
    fb = _flatten_snapshot(_strip_snapshot_volatile(before))
    fa = _flatten_snapshot(_strip_snapshot_volatile(after))
    keys = sorted(set(fb) | set(fa))
    changes = []
    for k in keys:
        if fb.get(k, "<MISSING>") != fa.get(k, "<MISSING>"):
            changes.append({"path": k, "before": fb.get(k, "<MISSING>"), "after": fa.get(k, "<MISSING>"), "allowed": _path_allowed(k, allowed)})
    unexpected = [c for c in changes if not c.get("allowed")]
    return {
        "ok": not unexpected,
        "schema": "live_state_diff.v1",
        "before": str(bp),
        "after": str(ap),
        "allowed_prefixes": allowed,
        "summary": {"changed": len(changes), "unexpected": len(unexpected), "allowed": len(changes) - len(unexpected)},
        "changes": changes,
        "unexpected_changes": unexpected,
        "policy": "Diff bỏ qua block volatile + key volatile leaf (age_days/seconds/mtime/…). Thay đổi còn lại phải khai báo --allow <path_prefix> nếu là dự kiến.",
    }


def cmd_live_state_diff(a) -> int:
    out = _live_state_diff(getattr(a, "before"), getattr(a, "after"), allowed=getattr(a, "allow", None) or [])
    if getattr(a, "out", None):
        _write_json_atomic(Path(a.out), out)
    _print_json_or_text(out, getattr(a, "json", False))
    return 0 if out.get("ok") else 2


def cmd_deploy_plan(a) -> int:
    out = _deploy_plan(bundle=getattr(a, "bundle", None) or "", target_dir=getattr(a, "target_dir", None) or "", backup_dir=getattr(a, "backup_dir", None) or "", profile=getattr(a, "profile", None) or "", include_ocr=bool(getattr(a, "include_ocr", False)))
    _print_json_or_text(out, getattr(a, "json", False))
    return 0


def cmd_rollback_plan(a) -> int:
    out = _rollback_plan(target_dir=getattr(a, "target_dir", None) or "", backup_path=getattr(a, "backup_path", None) or "", bundle=getattr(a, "bundle", None) or "")
    _print_json_or_text(out, getattr(a, "json", False))
    return 0

# ───────────────────────── final acceptance/runbook helpers (stage8) ─────────────────────────
def _final_acceptance_report(profile: str = "", include_ocr: bool = False, *, strict_live: bool = False) -> dict:
    """Final offline acceptance + live handoff status. Không gọi Drive/NLM, không ghi corpus."""
    results = []
    def add(name: str, ok: bool, detail: str = "", **extra):
        rec = {"name": name, "ok": bool(ok), "detail": detail}
        rec.update(extra)
        results.append(rec)

    try:
        wa = _workflow_cards_audit()
        add("workflow_audit", bool(wa.get("ok")), json.dumps(wa.get("summary", {}), ensure_ascii=False), errors=wa.get("errors"), warnings=(wa.get("warnings") or [])[:12])
    except Exception as e:  # noqa: BLE001
        add("workflow_audit", False, f"{type(e).__name__}: {e}")

    try:
        # Reuse the same in-process primitives as release-check, but avoid subprocess/selftest in final acceptance.
        import py_compile
        py_compile.compile(str(HERE / "tl.py"), doraise=True)
        py_compile.compile(str(HERE / "gen_instructions.py"), doraise=True)
        for _mod in ["__init__.py", "deterministic.py", "jsonio.py"]:
            py_compile.compile(str(HERE / "tl_core" / _mod), doraise=True)
        add("py_compile", True, "scripts/tl.py + scripts/gen_instructions.py + scripts/tl_core/*.py")
    except Exception as e:  # noqa: BLE001
        add("py_compile", False, f"{type(e).__name__}: {e}")

    try:
        gi = _imp("gen_instructions")
        pa = gi.audit(gi.generate("project", VERSION), "project")
        na = gi.audit(gi.generate("nlm", VERSION), "nlm")
        add("project_instruction_audit", bool(pa.get("ok")), json.dumps(pa, ensure_ascii=False)[:600])
        add("nlm_instruction_audit", bool(na.get("ok")), json.dumps(na, ensure_ascii=False)[:600])
    except Exception as e:  # noqa: BLE001
        add("instruction_audit", False, f"{type(e).__name__}: {e}")

    try:
        rm = _build_release_manifest(HERE.parent)
        rv = _verify_release_manifest(HERE.parent, rm, strict=False)
        add("release_manifest_build", bool(rm.get("ok")) and not rm.get("required_missing"), f"files={rm.get('file_count')} hash={rm.get('package_hash')}", required_missing=rm.get("required_missing"))
        add("release_verify_self", bool(rv.get("ok")) and bool(rv.get("package_hash_match")), f"checked={rv.get('checked_file_count')} match={rv.get('package_hash_match')}", failed=rv.get("failed"))
    except Exception as e:  # noqa: BLE001
        add("release_manifest_or_verify", False, f"{type(e).__name__}: {e}")

    for task in ["write_new_tool", "nlm_query_quality", "convert_rename", "ingest_zip", "ocr_pdf_scan", "ocr_run", "large_doc_chunk", "chunk_apply", "live_readiness", "live_contract_check", "live_state_snapshot", "live_state_diff", "deploy_plan", "rollback_plan", "final_acceptance", "go_live_runbook"]:
        try:
            wf_id = _TASK_TO_WORKFLOW.get(task, task)
            card = _load_workflow_card(wf_id)
            add(f"route_task:{task}", bool(card.get("ok", True)), f"workflow={wf_id} risk={card.get('risk')}")
        except Exception as e:  # noqa: BLE001
            add(f"route_task:{task}", False, f"{type(e).__name__}: {e}")

    lr = _live_readiness_report(profile=profile, include_ocr=include_ocr, check_contract=False)
    live_ready = bool(lr.get("env_ready"))
    lp = _live_smoke_plan(profile=profile, include_ocr=include_ocr)
    dp = _deploy_plan(profile=profile, include_ocr=include_ocr)
    rp = _rollback_plan()
    add("live_readiness_report", (live_ready if strict_live else True), f"env_ready={live_ready}; contract skipped in offline final-acceptance; checks={len(lr.get('checks', []))}", readiness=lr)
    add("live_smoke_plan", bool(lp.get("ok")) and len(lp.get("steps", [])) >= 8, f"steps={len(lp.get('steps', []))}")
    add("deploy_plan", bool(dp.get("ok")) and len(dp.get("steps", [])) >= 6, f"steps={len(dp.get('steps', []))}")
    add("rollback_plan", bool(rp.get("ok")) and len(rp.get("steps", [])) >= 4, f"steps={len(rp.get('steps', []))}")

    offline_ok = all(r.get("ok") for r in results if r["name"] != "live_readiness_report")
    ok = offline_ok and (live_ready if strict_live else True)
    gate = "env_ready_contract_still_required" if live_ready else "offline_pass_live_auth_required"
    if strict_live and not live_ready:
        gate = "blocked_until_live_readiness_passes"
    return {
        "ok": ok,
        "schema": "final_acceptance.v1",
        "offline_ok": offline_ok,
        "live_ready": live_ready,
        "deployment_gate": gate,
        "strict_live": bool(strict_live),
        "profile": profile or None,
        "include_ocr": include_ocr,
        "results": results,
        "next": "Copy bundle sang máy live rồi chạy tl live-readiness --json, tl live-contract-check --json, live-state-snapshot before/after, live-state-diff và live-smoke-plan trước khi apply rộng.",
    }


def cmd_final_acceptance(a) -> int:
    out = _final_acceptance_report(profile=getattr(a, "profile", None) or "", include_ocr=bool(getattr(a, "include_ocr", False)), strict_live=bool(getattr(a, "strict_live", False)))
    if getattr(a, "out", None):
        _write_text_atomic(Path(a.out), json.dumps(out, ensure_ascii=False, indent=2))
    _print_json_or_text(out, getattr(a, "json", False))
    return 0 if out.get("ok") else 2


def _go_live_runbook_markdown(profile: str = "", include_ocr: bool = False) -> str:
    smoke = _live_smoke_plan(profile=profile, include_ocr=include_ocr)
    deploy = _deploy_plan(profile=profile, include_ocr=include_ocr)
    rollback = _rollback_plan()
    lines = [
        "# tra-luat Go-live Runbook",
        "",
        "Mục tiêu: triển khai skill theo chuỗi có kiểm chứng, không ghi Drive/NLM trước khi readiness đạt.",
        "",
        "## 1. Kiểm tra offline trên bundle",
        "",
        "```bash",
        "python scripts/tl.py release-check --json",
        "python scripts/tl.py workflow-audit --json",
        "python scripts/tl.py release-manifest --out RELEASE_MANIFEST.json --json",
        "python scripts/tl.py release-verify RELEASE_MANIFEST.json --json",
        "python scripts/tl.py final-acceptance --json",
        "```",
        "",
        "## 2. Kiểm tra readiness trên máy live",
        "",
        "```bash",
        "python scripts/tl.py live-readiness --json" + (" --include-ocr" if include_ocr else ""),
        "python scripts/tl.py live-contract-check --json",
        "python scripts/tl.py live-state-snapshot --out before.json --json",
        "python scripts/tl.py live-smoke-plan --json" + (" --include-ocr" if include_ocr else ""),
        "python scripts/tl.py live-state-snapshot --out after.json --json",
        "python scripts/tl.py live-state-diff before.json after.json --json --allow source_counts --allow notebooks.get.source_count",
        "```",
        "",
        "Chỉ tiếp tục khi `env_ready=true` và `live_contract_ready=true`. `apply_ready` không được true nếu chưa có smoke proof/diff hợp lệ.",
        "",
        "## 3. Kế hoạch triển khai",
        "",
    ]
    for step in deploy.get("steps", []):
        lines.append(f"- `{step.get('id')}`: `{' '.join(map(str, step.get('command', [])))}` — {step.get('expect','')}")
    lines += ["", "## 4. Smoke test live", ""]
    for step in smoke.get("steps", []):
        risk = step.get("risk")
        lines.append(f"- **{risk}** `{step.get('id')}`: `{' '.join(map(str, step.get('command', [])))}` — {step.get('expect','')}")
    lines += [
        "",
        "Quy tắc dừng: nếu bước `high` fail, dừng ngay, đọc report/readback, không chạy bước apply kế tiếp.",
        "Sau smoke, bắt buộc có `before.json`/`after.json` và `live-state-diff` chỉ gồm thay đổi dự kiến.",
        "",
        "## 5. Rollback",
        "",
    ]
    for step in rollback.get("steps", []):
        lines.append(f"- `{step.get('id')}`: `{' '.join(map(str, step.get('command', [])))}` — {step.get('expect','')}")
    lines += [
        "",
        "## 6. Tiêu chí hoàn thành",
        "",
        "- `release-check` ok=true.",
        "- `release-verify` ok=true.",
        "- `workflow-audit` ok=true.",
        "- `live-readiness` có `env_ready=true` và `live_contract_ready=true` trên máy live.",
        "- Có `live-state-snapshot` trước/sau smoke và `live-state-diff` không có unexpected_changes.",
        "- Smoke test high-risk đầu tiên thành công với file mẫu nhỏ trước khi chạy dữ liệu thật.",
        "- Có backup/rollback plan trước khi replace skill đang dùng.",
    ]
    return "\n".join(lines) + "\n"


def cmd_go_live_runbook(a) -> int:
    md = _go_live_runbook_markdown(profile=getattr(a, "profile", None) or "", include_ocr=bool(getattr(a, "include_ocr", False)))
    if getattr(a, "out", None):
        _write_text_atomic(Path(a.out), md)
    if getattr(a, "json", False):
        out = {"ok": True, "schema": "go_live_runbook.v1", "profile": getattr(a, "profile", None) or None, "include_ocr": bool(getattr(a, "include_ocr", False)), "markdown": md}
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(md)
    return 0
