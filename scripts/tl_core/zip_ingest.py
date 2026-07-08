# -*- coding: utf-8 -*-
"""tl_core.zip_ingest — Pha D (v1.33.57): tách NGUYÊN VĂN từ scripts/tl.py (kế hoạch nợ-kỹ-thuật D).

Public CLI vẫn là scripts/tl.py (stub ủy quyền). Nhận helper dùng chung của tl qua `bind(tl_module)`
(copy-globals, bỏ tên đã có — xem tl_core.workflow docstring). KHÔNG đọc bare mutable-global của tl.
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
import unicodedata  # noqa: F401
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


# ───────────────────────── safe dry-run helpers: zip/OCR/chunk ─────────────────────────
_ALLOWED_INGEST_EXTS = {".doc", ".docx", ".pdf", ".txt", ".md", ".rtf", ".odt"}

_IGNORED_ZIP_NAMES = {".ds_store", "thumbs.db"}


def _zip_is_safe_member(name: str) -> bool:
    if not name or name.endswith("/"):
        return False
    n = name.replace("\\", "/")
    parts = [p for p in n.split("/") if p]
    if any(p == ".." for p in parts):
        return False
    if n.startswith("/") or re.match(r"^[A-Za-z]:", n):
        return False
    low_base = parts[-1].lower() if parts else ""
    if low_base in _IGNORED_ZIP_NAMES or n.startswith("__MACOSX/"):
        return False
    # v1.33.56 (review PH2-03): ký tự cấm trên Windows (tên legacy/cp437 từ zip Linux) → unsafe TẠI PLAN,
    # không để rơi tới extract mới nổ OSError/ghi tên rác.
    if re.search(r'[<>:"|?*]|[\x00-\x1f]', n):
        return False
    return True


def _zip_normalized_member_path(name: str) -> str:
    """Stable normalized zip member path for sorting/duplicate detection. Empty means unsafe."""
    n = (name or "").replace("\\", "/")
    if not n or n.endswith("/"):
        return ""
    parts: list[str] = []
    for part in n.split("/"):
        if not part or part == ".":
            continue
        if part == "..":
            return ""
        parts.append(part)
    if not parts:
        return ""
    return "/".join(parts)


def _zip_sorted_infos(zf: zipfile.ZipFile) -> list[zipfile.ZipInfo]:
    """Return members in deterministic order independent of original zip entry order."""
    return sorted(zf.infolist(), key=lambda i: (_zip_normalized_member_path(i.filename).lower(), i.filename.replace("\\", "/")))


def _zip_plan(path: str, *, mode: str, profile: str = "", cat: str = "", max_files: int = 200, max_size_mb: int = 100) -> dict:
    zpath = Path(path)
    out = {"ok": False, "schema": "ingest_zip_plan.v1", "zip": str(zpath), "mode": mode, "profile": profile or None, "cat": cat or None,
           "files_total": 0, "accepted": 0, "skipped": 0, "items": [], "errors": [], "requires_apply": True,
           "note": "DRY-RUN only: zip là container đầu vào; không upload zip nguyên vào Drive/NLM."}
    if not zpath.exists():
        out["errors"].append("ZIP_NOT_FOUND")
        return out
    if not zipfile.is_zipfile(zpath):
        out["errors"].append("NOT_A_ZIP_FILE")
        return out
    max_bytes = max(1, int(max_size_mb)) * 1024 * 1024
    try:
        with zipfile.ZipFile(zpath) as zf:
            infos = _zip_sorted_infos(zf)
            out["files_total"] = len([i for i in infos if not i.is_dir()])
            seen_norm: dict[str, str] = {}
            if out["files_total"] > max_files:
                out["errors"].append(f"TOO_MANY_FILES:{out['files_total']}>{max_files}")
            for info in infos:
                if info.is_dir():
                    continue
                norm_path = _zip_normalized_member_path(info.filename)
                item = {"path": info.filename, "normalized_path": norm_path or None, "size": info.file_size, "status": "planned"}
                if not _zip_is_safe_member(info.filename) or not norm_path:
                    item.update({"status": "skipped", "reason": "UNSAFE_OR_SYSTEM_PATH"})
                    out["items"].append(item); continue
                norm_key = norm_path.lower()
                if norm_key in seen_norm:
                    item.update({"status": "skipped", "reason": "DUPLICATE_NORMALIZED_ZIP_PATH", "duplicate_of": seen_norm[norm_key]})
                    out["errors"].append(f"DUPLICATE_NORMALIZED_ZIP_PATH:{info.filename}->{seen_norm[norm_key]}")
                    out["items"].append(item); continue
                seen_norm[norm_key] = info.filename
                ext = Path(norm_path).suffix.lower()
                item["ext"] = ext
                if ext not in _ALLOWED_INGEST_EXTS:
                    item.update({"status": "skipped", "reason": "UNSUPPORTED_EXTENSION"})
                elif info.file_size > max_bytes:
                    item.update({"status": "skipped", "reason": f"FILE_TOO_LARGE>{max_size_mb}MB"})
                else:
                    action = "profile-ingest" if mode == "profile" else "ingest-local"
                    convert = "drive_gdoc" if ext in {".doc", ".docx", ".pdf", ".rtf", ".odt"} else "text_source"
                    item.update({
                        "action": action,
                        "convert": convert,
                        "requires_ocr_review": ext == ".pdf",
                        "expected_pipeline": ["extract_to_temp", "upload_binary", "drive_convert_gdoc", "standardize_name", "verify_readback", "register", "nlm_add_after_verify"],
                        "status": "accepted",
                    })
                out["items"].append(item)
    except Exception as e:
        out["errors"].append(f"ZIP_READ_ERROR:{type(e).__name__}")
        return out
    out["accepted"] = sum(1 for i in out["items"] if i.get("status") == "accepted")
    out["skipped"] = sum(1 for i in out["items"] if i.get("status") == "skipped")
    out["ok"] = not out["errors"] and out["accepted"] > 0
    if mode == "vbqppl" and not cat:
        out["warnings"] = ["CAT_NOT_PROVIDED_FOR_VBQPPL_BATCH_REVIEW_REQUIRED"]
    else:
        out["warnings"] = []
    try:
        member_basis = ";".join(i.get("path", "") for i in out.get("items", []) if i.get("status") == "accepted")
        out["idempotency"] = _idempotency_contract_for_workflow("ingest_zip")
        out["idempotency_key"] = hashlib.sha256(((_sha256_bytes_file_local(zpath) if zpath.exists() else "") + "|" + mode + "|" + (cat or profile or "") + "|" + member_basis).encode("utf-8", errors="replace")).hexdigest()
    except Exception:
        out["idempotency"] = _idempotency_contract_for_workflow("ingest_zip")
    return out


def _safe_extract_zip_for_ingest(zip_path: str, temp_dir: str, *, max_size_mb: int | None = None) -> list[dict]:
    """Extract accepted members only. Caller phải đã chạy _zip_plan. Chống zip-slip.
    v1.33.56 (review PH2-02): +max_size_mb — trước đây plan đánh dấu file quá cỡ 'skipped' nhưng extract
    KHÔNG kiểm → apply vẫn nạp file plan đã loại."""
    extracted = []
    base = Path(temp_dir).resolve()
    _cap = max(1, int(max_size_mb)) * 1024 * 1024 if max_size_mb else None
    with zipfile.ZipFile(zip_path) as zf:
        for info in _zip_sorted_infos(zf):
            norm_path = _zip_normalized_member_path(info.filename)
            if info.is_dir() or not _zip_is_safe_member(info.filename) or not norm_path:
                continue
            if _cap is not None and info.file_size > _cap:
                continue
            ext = Path(norm_path).suffix.lower()
            if ext not in _ALLOWED_INGEST_EXTS:
                continue
            dest = (base / norm_path).resolve()
            if not str(dest).startswith(str(base) + os.sep):
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, open(dest, "wb") as dst:
                shutil.copyfileobj(src, dst)
            extracted.append({"zip_path": info.filename, "normalized_path": norm_path, "path": str(dest), "size": info.file_size, "ext": ext})
    return extracted


def _zip_apply(a, *, mode: str) -> int:
    cat = getattr(a, "cat", "") or ""
    profile = getattr(a, "profile", None) or os.environ.get("TL_PROFILE") or DEFAULT_PROFILE
    if mode == "vbqppl" and not cat:
        print(_json_dumps({"ok": False, "error": "CAT_REQUIRED_FOR_VBQPPL_ZIP_APPLY", "note": "Dùng --cat NN hoặc chạy dry-run để phân loại trước."}, deterministic=_deterministic_enabled(a)))
        return 2
    if getattr(a, "confirm", "") != "yes":
        print(_json_dumps({"ok": False, "error": "CONFIRM_REQUIRED", "note": "Zip apply sẽ gọi ingest-local/profile-ingest từng file. Thêm --confirm yes sau khi đã xem dry-run."}, deterministic=_deterministic_enabled(a)))
        return 2
    plan = _zip_plan(a.file, mode=mode, profile=(profile if mode == "profile" else ""), cat=cat, max_files=a.max_files, max_size_mb=a.max_size_mb)
    if not plan.get("ok"):
        print(_json_dumps(plan, deterministic=_deterministic_enabled(a))); return 2
    results = []
    with tempfile.TemporaryDirectory(prefix="tl_zip_ingest_") as td:
        extracted = _safe_extract_zip_for_ingest(a.file, td, max_size_mb=getattr(a, "max_size_mb", None))
        for item in extracted:
            if mode == "profile":
                child = ["profile-ingest", item["path"], "--apply", "--json"]
                if profile:
                    child += ["--profile", profile]
            else:
                child = ["ingest-local", item["path"], "--cat", cat, "--apply", "--json"]
            if getattr(a, "skip_nlm_preflight", False) and mode != "profile":
                child.append("--skip-nlm-preflight")
            if mode != "profile" and getattr(a, "profile", None):   # v1.33.56 (regression/F2)
                child += ["--profile", a.profile]
            if getattr(a, "config", None):   # v1.33.56 (PH2-04): child PHẢI thấy cùng config với parent
                child += ["--config", str(Path(a.config).expanduser().resolve())]
            r = _run_child_tl(child)
            r.update({"zip_path": item["zip_path"], "file": item["path"]})
            results.append(r)
            if not r.get("ok") and not getattr(a, "continue_on_error", False):
                break
    out = {"ok": bool(results) and all(r.get("ok") for r in results), "schema": "ingest_zip_apply.v1",
           "mode": mode, "profile": (profile if mode == "profile" else None), "cat": (cat if mode == "vbqppl" else None),
           "dry_run_plan": {k: plan.get(k) for k in ("zip", "files_total", "accepted", "skipped", "warnings")},
           "results": results, "note": "Apply gọi lại pipeline hiện có từng file; từng pipeline tự upload→convert→readback→register→NLM."}
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0 if out.get("ok") else 2


def cmd_ingest_zip(a) -> int:
    out = _zip_plan(a.file, mode="vbqppl", cat=getattr(a, "cat", "") or "", max_files=a.max_files, max_size_mb=a.max_size_mb)
    if not getattr(a, "apply", False):
        _print_json_or_text(out, getattr(a, "json", False))
        return 0 if out.get("ok") else 2
    return _zip_apply(a, mode="vbqppl")


def cmd_profile_ingest_zip(a) -> int:
    prof = getattr(a, "profile", None) or os.environ.get("TL_PROFILE") or DEFAULT_PROFILE
    out = _zip_plan(a.file, mode="profile", profile=prof, max_files=a.max_files, max_size_mb=a.max_size_mb)
    if not getattr(a, "apply", False):
        _print_json_or_text(out, getattr(a, "json", False))
        return 0 if out.get("ok") else 2
    return _zip_apply(a, mode="profile")
