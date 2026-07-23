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
import stat       # noqa: F401
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
_WINDOWS_RESERVED = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)),
                     *(f"lpt{i}" for i in range(1, 10))}


def _zip_is_ignored_member(name: str) -> bool:
    n = unicodedata.normalize("NFC", (name or "").replace("\\", "/"))
    parts = [p for p in n.split("/") if p and p != "."]
    if not parts:
        return False
    return bool(parts and (parts[-1].lower() in _IGNORED_ZIP_NAMES or parts[0].lower() == "__macosx"))


def _zip_is_safe_member(name: str) -> bool:
    if not name or name.endswith("/"):
        return False
    n = unicodedata.normalize("NFC", name.replace("\\", "/"))
    parts = [p for p in n.split("/") if p and p != "."]
    if not parts:
        return False
    if any(p == ".." for p in parts):
        return False
    if n.startswith("/") or re.match(r"^[A-Za-z]:", n):
        return False
    low_base = parts[-1].lower() if parts else ""
    if low_base in _IGNORED_ZIP_NAMES or (parts and parts[0].lower() == "__macosx"):
        return False
    # v1.33.56 (review PH2-03): ký tự cấm trên Windows (tên legacy/cp437 từ zip Linux) → unsafe TẠI PLAN,
    # không để rơi tới extract mới nổ OSError/ghi tên rác.
    if re.search(r'[<>:"|?*]|[\x00-\x1f]', n):
        return False
    for part in parts:
        if part.endswith((" ", ".")):
            return False
        stem = part.split(".", 1)[0].casefold()
        if stem in _WINDOWS_RESERVED:
            return False
    return True


def _zip_normalized_member_path(name: str) -> str:
    """Stable normalized zip member path for sorting/duplicate detection. Empty means unsafe."""
    n = unicodedata.normalize("NFC", (name or "").replace("\\", "/"))
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
    return sorted(zf.infolist(), key=lambda i: (_zip_normalized_member_path(i.filename).casefold(),
                                                 unicodedata.normalize("NFC", i.filename.replace("\\", "/"))))


def _zip_info_is_special(info: zipfile.ZipInfo) -> bool:
    mode = (int(info.external_attr) >> 16) & 0xFFFF
    if not mode:
        return False
    # ``ZipInfo.writestr`` commonly stores only permission bits (0600) and no
    # POSIX file-type bits.  Treat that as an ordinary file; otherwise every
    # ZIP produced by Python on Windows is falsely rejected as "special".
    kind = stat.S_IFMT(mode)
    return bool(kind and kind not in {stat.S_IFREG, stat.S_IFDIR})


def _zip_member_sha256(zf: zipfile.ZipFile, info: zipfile.ZipInfo) -> str:
    h = hashlib.sha256()
    count = 0
    with zf.open(info, "r") as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            count += len(chunk)
            h.update(chunk)
    if count != info.file_size:
        raise ValueError(f"ZIP_MEMBER_SIZE_MISMATCH:{info.filename}:{count}!={info.file_size}")
    return h.hexdigest()


def _zip_plan(path: str, *, mode: str, profile: str = "", cat: str = "", max_files: int = 200,
              max_size_mb: int = 100, max_total_mb: int = 500, max_ratio: float = 100.0) -> dict:
    zpath = Path(path)
    out = {"ok": False, "schema": "ingest_zip_plan.v1", "zip": str(zpath), "mode": mode, "profile": profile or None, "cat": cat or None,
           "files_total": 0, "accepted": 0, "skipped": 0, "items": [], "errors": [], "requires_apply": True,
           "note": "DRY-RUN only: zip là container đầu vào; không upload zip nguyên vào Drive/NLM.",
           "limits": {"max_files": int(max_files), "max_size_mb": int(max_size_mb),
                      "max_total_mb": int(max_total_mb), "max_ratio": float(max_ratio)}}
    if not zpath.exists():
        out["errors"].append("ZIP_NOT_FOUND")
        return out
    if not zipfile.is_zipfile(zpath):
        out["errors"].append("NOT_A_ZIP_FILE")
        return out
    max_bytes = max(1, int(max_size_mb)) * 1024 * 1024
    max_total_bytes = max(1, int(max_total_mb)) * 1024 * 1024
    total_accepted_bytes = 0
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
                item = {"path": info.filename, "normalized_path": norm_path or None, "size": info.file_size,
                        "crc32": info.CRC, "status": "planned"}   # v1.33.61: CRC nội-dung cho idempotency_key content-v2
                if _zip_is_ignored_member(info.filename):
                    item.update({"status": "skipped", "reason": "IGNORED_SYSTEM_PATH"})
                    out["items"].append(item); continue
                if _zip_info_is_special(info):
                    item.update({"status": "skipped", "reason": "SPECIAL_ZIP_ENTRY"})
                    out["errors"].append(f"SPECIAL_ZIP_ENTRY:{info.filename}")
                    out["items"].append(item); continue
                if not _zip_is_safe_member(info.filename) or not norm_path:
                    item.update({"status": "skipped", "reason": "UNSAFE_OR_SYSTEM_PATH"})
                    out["errors"].append(f"UNSAFE_ZIP_PATH:{info.filename}")
                    out["items"].append(item); continue
                norm_key = norm_path.casefold()
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
                    ratio = (float("inf") if info.compress_size == 0 and info.file_size
                             else (info.file_size / max(info.compress_size, 1)))
                    item["compression_ratio"] = round(ratio, 3) if ratio != float("inf") else "inf"
                    if ratio > float(max_ratio):
                        item.update({"status": "skipped", "reason": f"COMPRESSION_RATIO>{max_ratio}"})
                        out["errors"].append(f"ZIP_BOMB_RATIO:{info.filename}")
                        out["items"].append(item); continue
                    total_accepted_bytes += int(info.file_size)
                    if total_accepted_bytes > max_total_bytes:
                        item.update({"status": "skipped", "reason": f"TOTAL_SIZE>{max_total_mb}MB"})
                        out["errors"].append(f"ZIP_TOTAL_SIZE_EXCEEDED:{total_accepted_bytes}>{max_total_bytes}")
                        out["items"].append(item); continue
                    action = "profile-ingest" if mode == "profile" else "ingest-local"
                    convert = "drive_gdoc" if ext in {".doc", ".docx", ".pdf", ".rtf", ".odt"} else "text_source"
                    item.update({
                        "action": action,
                        "convert": convert,
                        "requires_ocr_review": ext == ".pdf",
                        "expected_pipeline": ["extract_to_temp", "upload_binary", "drive_convert_gdoc", "standardize_name", "verify_readback", "register", "nlm_add_after_verify"],
                        "status": "accepted",
                        "sha256": _zip_member_sha256(zf, info),
                    })
                out["items"].append(item)
    except Exception as e:
        out["errors"].append(f"ZIP_READ_ERROR:{type(e).__name__}")
        return out
    out["accepted"] = sum(1 for i in out["items"] if i.get("status") == "accepted")
    out["skipped"] = sum(1 for i in out["items"] if i.get("status") == "skipped")
    out["total_uncompressed_bytes"] = total_accepted_bytes
    out["ok"] = not out["errors"] and out["accepted"] > 0
    if mode == "vbqppl" and not cat:
        out["warnings"] = ["CAT_NOT_PROVIDED_FOR_VBQPPL_BATCH_REVIEW_REQUIRED"]
    else:
        out["warnings"] = []
    try:
        # v1.33.61 (CI run #2): KHÔNG hash bytes CONTAINER zip — zipfile 3.12 vs 3.13 (và zlib build) ghi
        # header khác nhau → key lệch cross-machine. Danh tính NỘI DUNG: norm_path+CRC32+size từng member
        # accepted (CRC lấy từ central directory — 0 IO thêm; re-zip cùng nội dung = CÙNG key, đúng ngữ
        # nghĩa idempotency hơn).
        member_basis = ";".join(f"{i.get('normalized_path','')}:{i.get('sha256','')}:{i.get('size','')}"
                                for i in out.get("items", []) if i.get("status") == "accepted")
        from tl_core.ingest_contract import canonical_json_bytes, sha256_file
        out["archive_sha256"] = sha256_file(zpath)
        out["idempotency"] = _idempotency_contract_for_workflow("ingest_zip")
        out["idempotency_key"] = hashlib.sha256(("content-v3|" + mode + "|" + (cat or profile or "") + "|" + member_basis).encode("utf-8")).hexdigest()
        _commit = {"schema": out["schema"], "mode": mode, "profile": profile or "", "cat": cat or "",
                   "archive_sha256": out["archive_sha256"], "members": [
                       {k: i.get(k) for k in ("normalized_path", "sha256", "size")}
                       for i in out.get("items", []) if i.get("status") == "accepted"],
                   "limits": out["limits"]}
        out["plan_hash"] = hashlib.sha256(canonical_json_bytes(_commit)).hexdigest()
    except Exception:
        out["idempotency"] = _idempotency_contract_for_workflow("ingest_zip")
    return out


def _safe_extract_zip_for_ingest(zip_path: str, temp_dir: str, *, plan: dict | None = None,
                                 max_size_mb: int | None = None, max_total_mb: int | None = None,
                                 max_ratio: float | None = None) -> list[dict]:
    """Extract accepted members only. Caller phải đã chạy _zip_plan. Chống zip-slip.
    v1.33.56 (review PH2-02): +max_size_mb — trước đây plan đánh dấu file quá cỡ 'skipped' nhưng extract
    KHÔNG kiểm → apply vẫn nạp file plan đã loại."""
    extracted = []
    base = Path(temp_dir).resolve()
    _cap = max(1, int(max_size_mb)) * 1024 * 1024 if max_size_mb else None
    _total_cap = max(1, int(max_total_mb)) * 1024 * 1024 if max_total_mb else None
    _expected = {i.get("normalized_path"): i for i in ((plan or {}).get("items") or [])
                 if i.get("status") == "accepted"}
    if plan:
        from tl_core.ingest_contract import sha256_file
        if sha256_file(zip_path) != plan.get("archive_sha256"):
            raise ValueError("ZIP_ARCHIVE_HASH_MISMATCH")
    _total = 0
    with zipfile.ZipFile(zip_path) as zf:
        for info in _zip_sorted_infos(zf):
            norm_path = _zip_normalized_member_path(info.filename)
            if info.is_dir() or _zip_info_is_special(info) or not _zip_is_safe_member(info.filename) or not norm_path:
                continue
            if _expected and norm_path not in _expected:
                continue
            if _cap is not None and info.file_size > _cap:
                raise ValueError(f"ZIP_MEMBER_EXCEEDS_APPLY_LIMIT:{norm_path}")
            _ratio = (float("inf") if info.compress_size == 0 and info.file_size
                      else info.file_size / max(info.compress_size, 1))
            if max_ratio is not None and _ratio > float(max_ratio):
                raise ValueError(f"ZIP_MEMBER_RATIO_EXCEEDS_APPLY_LIMIT:{norm_path}")
            _total += int(info.file_size)
            if _total_cap is not None and _total > _total_cap:
                raise ValueError("ZIP_TOTAL_EXCEEDS_APPLY_LIMIT")
            ext = Path(norm_path).suffix.lower()
            if ext not in _ALLOWED_INGEST_EXTS:
                continue
            dest = (base / norm_path).resolve()
            try:
                dest.relative_to(base)
            except ValueError as exc:
                raise ValueError(f"ZIP_PATH_ESCAPES_STAGING:{norm_path}") from exc
            dest.parent.mkdir(parents=True, exist_ok=True)
            h = hashlib.sha256()
            written = 0
            with zf.open(info) as src, open(dest, "xb") as dst:
                while True:
                    chunk = src.read(1024 * 1024)
                    if not chunk:
                        break
                    written += len(chunk)
                    h.update(chunk)
                    dst.write(chunk)
            digest = h.hexdigest()
            expected = _expected.get(norm_path) or {}
            if written != info.file_size or (expected.get("sha256") and digest != expected.get("sha256")):
                dest.unlink(missing_ok=True)
                raise ValueError(f"ZIP_MEMBER_CHANGED_OR_CORRUPT:{norm_path}")
            extracted.append({"zip_path": info.filename, "normalized_path": norm_path, "path": str(dest),
                              "size": info.file_size, "sha256": digest, "ext": ext})
    if _expected and len(extracted) != len(_expected):
        raise ValueError(f"ZIP_ACCEPTED_MEMBER_COUNT_MISMATCH:{len(extracted)}!={len(_expected)}")
    return extracted


def _zip_child_args(item, *, mode: str, profile: str, cat: str, a) -> list:
    """r184 (ADR-0013): argv child CHUNG cho plan-bundle (DRY) lẫn apply — một nguồn sự thật,
    bundle drift không thể đến từ hai cách dựng args khác nhau."""
    if mode == "profile":
        child = ["profile-ingest", item["path"], "--json"]
        if profile:
            child += ["--profile", profile]
    else:
        child = ["ingest-local", item["path"], "--cat", cat, "--json"]
    if getattr(a, "skip_nlm_preflight", False) and mode != "profile":
        child.append("--skip-nlm-preflight")
    if mode != "profile" and getattr(a, "profile", None):   # v1.33.56 (regression/F2)
        child += ["--profile", a.profile]
    if getattr(a, "config", None):   # v1.33.56 (PH2-04): child PHẢI thấy cùng config với parent
        child += ["--config", str(Path(a.config).expanduser().resolve())]
    return child


def _zip_child_plan_one(child_args: list) -> dict:
    """r184 (ADR-0013): chạy child CLI ở chế độ DRY **in-process** (0 subprocess, 0 mutation) để lấy
    child plan_hash cho bundle. stdout child bị nuốt; chỉ trả JSON + plan_hash."""
    import io as _io, contextlib as _ctx
    try:
        _ns = build_parser().parse_args([str(x) for x in (child_args or []) if str(x)])
        _bo, _be = _io.StringIO(), _io.StringIO()
        with _ctx.redirect_stdout(_bo), _ctx.redirect_stderr(_be):
            _rc = _ns.fn(_ns)
        try:
            _j = json.loads(_bo.getvalue())
        except Exception:  # noqa: BLE001
            _j = {}
        return {"ok": _rc == 0 and bool(_j.get("plan_hash")), "returncode": _rc, "json": _j,
                "plan_hash": str(_j.get("plan_hash") or ""), "stderr_tail": _be.getvalue()[-400:]}
    except SystemExit as _e:  # argparse exit
        return {"ok": False, "returncode": int(getattr(_e, "code", 2) or 0), "json": {}, "plan_hash": "",
                "error": "CHILD_ARGPARSE_EXIT"}
    except Exception as _e:  # noqa: BLE001
        return {"ok": False, "json": {}, "plan_hash": "", "error": f"{type(_e).__name__}: {_e}"}


def _zip_plan_bundle(a, *, mode: str, profile: str, cat: str) -> dict:
    """r184 (ADR-0013 — ING-01): IMMUTABLE PLAN BUNDLE. DRY lập ĐẦY ĐỦ child plan cho từng member
    (in-process, tuần tự — tránh đua trạng thái profile toàn cục); parent `plan_hash` = fingerprint
    TOÀN bundle (archive + member list + mọi child plan). Xác nhận hash này = duyệt đúng bộ kế hoạch
    con — apply không được lập kế hoạch mới (khác ⇒ PLAN_DRIFT_REPLAN_REQUIRED)."""
    plan = _zip_plan(a.file, mode=mode, profile=(profile if mode == "profile" else ""), cat=cat,
                     max_files=a.max_files, max_size_mb=a.max_size_mb,
                     max_total_mb=getattr(a, "max_total_mb", 500), max_ratio=getattr(a, "max_ratio", 100.0))
    if not plan.get("ok"):
        return plan
    child_plans, child_errors = [], []
    with tempfile.TemporaryDirectory(prefix="tl_zip_plan_") as _td:
        try:
            _extracted = _safe_extract_zip_for_ingest(
                a.file, _td, plan=plan, max_size_mb=getattr(a, "max_size_mb", None),
                max_total_mb=getattr(a, "max_total_mb", 500), max_ratio=getattr(a, "max_ratio", 100.0))
        except Exception as _exc:  # noqa: BLE001
            return {**plan, "ok": False, "step": "zip_extract_verify_plan",
                    "error": f"{type(_exc).__name__}: {_exc}"}
        for _item in _extracted:
            _dry = _zip_child_plan_one(_zip_child_args(_item, mode=mode, profile=profile, cat=cat, a=a))
            _rec = {"zip_path": _item["normalized_path"], "member_sha256": _item.get("sha256"),
                    "child_plan_hash": str(_dry.get("plan_hash") or ""), "ok": bool(_dry.get("ok"))}
            if not _dry.get("ok"):
                _rec.update({"error": "CHILD_PLAN_FAILED", "returncode": _dry.get("returncode"),
                             "detail": str(_dry.get("error") or "")[:200],
                             "stderr_tail": str(_dry.get("stderr_tail") or "")[-400:]})
                child_errors.append(_rec)
            child_plans.append(_rec)
    child_plans.sort(key=lambda r: str(r.get("zip_path") or "").casefold())
    from tl_core.ingest_contract import canonical_json_bytes
    _bundle_commit = {"schema": "ingest_zip_bundle.v1", "parent_plan_hash": plan.get("plan_hash"),
                      "archive_sha256": plan.get("archive_sha256"),
                      "children": [{k: c.get(k) for k in ("zip_path", "member_sha256", "child_plan_hash")}
                                   for c in child_plans]}
    _bundle_hash = hashlib.sha256(canonical_json_bytes(_bundle_commit)).hexdigest()
    return {**plan, "schema": "ingest_zip_bundle.v1", "parent_plan_hash": plan.get("plan_hash"),
            "plan_hash": _bundle_hash, "child_plans": child_plans,
            "ok": bool(plan.get("ok")) and not child_errors,
            **({"error": "CHILD_PLAN_FAILED", "child_errors": child_errors} if child_errors else {}),
            "bundle_note": "plan_hash = fingerprint TOÀN bundle (ADR-0013): archive + member + MỌI child "
                           "plan. --expected-plan-hash giá trị này khi apply; hash cũ (chỉ parent) hết "
                           "hợp lệ — replan bằng DRY mới."}


def _zip_apply(a, *, mode: str) -> int:
    from concurrent.futures import ThreadPoolExecutor
    from tl_core.ingest_contract import authorize_apply
    cat = getattr(a, "cat", "") or ""
    profile = getattr(a, "profile", None) or os.environ.get("TL_PROFILE") or DEFAULT_PROFILE
    if mode == "vbqppl" and not cat:
        print(_json_dumps({"ok": False, "error": "CAT_REQUIRED_FOR_VBQPPL_ZIP_APPLY", "note": "Dùng --cat NN hoặc chạy dry-run để phân loại trước."}, deterministic=_deterministic_enabled(a)))
        return 2
    # r184 (ADR-0013): plan = BUNDLE — child plans lập lại tất định, authorize phủ TOÀN bundle.
    plan = _zip_plan_bundle(a, mode=mode, profile=profile, cat=cat)
    if not plan.get("ok"):
        print(_json_dumps(plan, deterministic=_deterministic_enabled(a))); return 2
    auth = authorize_apply(apply=True, confirm=getattr(a, "confirm", None),
                           expected_plan_hash=getattr(a, "expected_plan_hash", None),
                           actual_plan_hash=plan.get("plan_hash") or "")
    if not auth.get("ok"):
        print(_json_dumps({"ok": False, "step": "apply_authorization", **auth},
                          deterministic=_deterministic_enabled(a)))
        return 2
    _child_hash_by_path = {str(c.get("zip_path") or ""): str(c.get("child_plan_hash") or "")
                           for c in (plan.get("child_plans") or [])}
    results = []
    run_id = _apply_journal_start("profile-ingest-zip" if mode == "profile" else "ingest-zip",
                                  {"file": str(a.file), "plan_hash": plan.get("plan_hash"),
                                   "parent_plan_hash": plan.get("parent_plan_hash"),
                                   "archive_sha256": plan.get("archive_sha256"), "profile": profile, "cat": cat})
    _journal_append(run_id, {"t": "plan", "op": "zip_bundle", "key": str(a.file),
                             "set": {"child_plans": plan.get("child_plans")}})
    with tempfile.TemporaryDirectory(prefix="tl_zip_ingest_") as td:
        try:
            extracted = _safe_extract_zip_for_ingest(
                a.file, td, plan=plan, max_size_mb=getattr(a, "max_size_mb", None),
                max_total_mb=getattr(a, "max_total_mb", 500), max_ratio=getattr(a, "max_ratio", 100.0))
        except Exception as exc:  # noqa: BLE001
            _journal_append(run_id, {"t": "run_end", "ok": False, "counts": {"FAILED": 1}})
            print(_json_dumps({"ok": False, "step": "zip_extract_verify", "journal": run_id,
                               "error": f"{type(exc).__name__}: {exc}"}, deterministic=_deterministic_enabled(a)))
            return 2

        # r184 (ADR-0013): tiền-kiểm DRIFT tuần tự (in-process — không đua profile-state):
        # recompute child plan hash, KHÁC bundle đã duyệt ⇒ PLAN_DRIFT_REPLAN_REQUIRED, KHÔNG mutation.
        _verified, _drifted = [], []
        for item in extracted:
            _recheck = _zip_child_plan_one(_zip_child_args(item, mode=mode, profile=profile, cat=cat, a=a))
            _recorded = _child_hash_by_path.get(str(item.get("normalized_path") or ""), "")
            if not (_recheck.get("ok") and _recorded and str(_recheck.get("plan_hash")) == _recorded):
                _drifted.append({"ok": False, "step": "child_plan_drift", "error": "PLAN_DRIFT_REPLAN_REQUIRED",
                                 "zip_path": item["normalized_path"],
                                 "recorded_plan_hash": _recorded,
                                 "recomputed_plan_hash": str(_recheck.get("plan_hash") or ""),
                                 "returncode": _recheck.get("returncode")})
            else:
                _verified.append((item, _recorded))

        def _run_member(pair):
            item, child_plan_hash = pair
            child = _zip_child_args(item, mode=mode, profile=profile, cat=cat, a=a)
            _journal_append(run_id, {"t": "intent", "op": "ingest_member", "key": item["normalized_path"],
                                     "set": {"plan_hash": child_plan_hash, "member_sha256": item.get("sha256")}})
            # --confirm yes hợp lệ Ở ĐÂY vì child_plan_hash nằm TRONG bundle user đã duyệt (ADR-0013)
            applied = _run_child_tl(child + ["--apply", "--confirm", "yes",
                                             "--expected-plan-hash", child_plan_hash])
            applied_ok = bool(applied.get("ok") and isinstance(applied.get("json"), dict)
                              and applied["json"].get("ok") is True)
            return {"ok": applied_ok, "step": "child_apply", "zip_path": item["normalized_path"],
                    "member_sha256": item.get("sha256"), "plan_hash": child_plan_hash,
                    "returncode": applied.get("returncode"), "result": applied.get("json"),
                    **({"stderr_tail": applied.get("stderr_tail"), "stdout_tail": applied.get("stdout_tail")}
                       if not applied_ok else {})}

        workers = max(1, min(int(getattr(a, "workers", 4) or 4), 8, len(_verified) or 1))
        with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="tl-zip-ingest") as pool:
            results = list(pool.map(_run_member, _verified))
        results.extend(_drifted)
        results.sort(key=lambda r: str(r.get("zip_path") or "").casefold())
        for r in results:
            _journal_append(run_id, {"t": "commit", "op": "ingest_member", "key": r.get("zip_path"),
                                     "ok": bool(r.get("ok")), "verify": {"plan_hash": r.get("plan_hash"),
                                                                            "member_sha256": r.get("member_sha256")}})
    _applied_ok = sum(1 for r in results if r.get("ok"))
    _applied_fail = sum(1 for r in results if not r.get("ok"))
    out = {"ok": bool(results) and all(r.get("ok") for r in results), "schema": "ingest_zip_apply.v1",
           "mode": mode, "profile": (profile if mode == "profile" else None), "cat": (cat if mode == "vbqppl" else None),
           # v1.34.45 (audit merge): ingest-zip apply ALWAYS processes every accepted member (children are
           # independent + idempotent), then reports partial explicitly. There is no fail-fast; `--continue-on-error`
           # does not change ingest-zip behavior. `ok` is true only when every member applied.
           "counts": {"applied": _applied_ok, "failed": _applied_fail, "total": len(results)},
           "partial": bool(_applied_fail) and bool(_applied_ok),
           "journal": run_id, "plan_hash": plan.get("plan_hash"), "archive_sha256": plan.get("archive_sha256"),
           "workers": workers,
           "dry_run_plan": {k: plan.get(k) for k in ("zip", "files_total", "accepted", "skipped", "warnings", "limits")},
           "results": results, "note": "Apply xử lý MỌI member (child độc lập+idempotent); ok=all(member). Xem counts/partial. Từng pipeline tự upload→convert→readback→register→NLM."}
    _journal_append(run_id, {"t": "run_end", "ok": bool(out["ok"]),
                             "counts": {"OK": sum(1 for r in results if r.get("ok")),
                                        "FAILED": sum(1 for r in results if not r.get("ok"))}})
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0 if out.get("ok") else 2


def cmd_ingest_zip(a) -> int:
    if not getattr(a, "apply", False):
        cat = getattr(a, "cat", "") or ""
        if not cat:
            # Chưa có --cat: DRY phân loại như cũ (parent-only) — bundle child plans cần cat.
            out = _zip_plan(a.file, mode="vbqppl", cat="", max_files=a.max_files,
                            max_size_mb=a.max_size_mb, max_total_mb=getattr(a, "max_total_mb", 500),
                            max_ratio=getattr(a, "max_ratio", 100.0))
            out["note_bundle"] = ("r184/ADR-0013: đây là DRY PHÂN LOẠI (chưa có --cat) — plan_hash này "
                                  "KHÔNG apply được; chạy lại DRY với --cat NN để nhận bundle plan_hash.")
        else:
            # r184 (ADR-0013): DRY in BUNDLE — child plans đầy đủ + plan_hash phủ toàn bundle.
            out = _zip_plan_bundle(a, mode="vbqppl", profile="", cat=cat)
        _print_json_or_text(out, getattr(a, "json", False))
        return 0 if out.get("ok") else 2
    return _zip_apply(a, mode="vbqppl")


def cmd_profile_ingest_zip(a) -> int:
    prof = getattr(a, "profile", None) or os.environ.get("TL_PROFILE") or DEFAULT_PROFILE
    if not getattr(a, "apply", False):
        # r184 (ADR-0013): DRY in BUNDLE — child plans đầy đủ + plan_hash phủ toàn bundle.
        out = _zip_plan_bundle(a, mode="profile", profile=prof, cat="")
        _print_json_or_text(out, getattr(a, "json", False))
        return 0 if out.get("ok") else 2
    return _zip_apply(a, mode="profile")
