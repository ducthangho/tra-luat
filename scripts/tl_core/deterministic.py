# -*- coding: utf-8 -*-
"""Deterministic JSON/path helpers for ``tl.py``.

This module is intentionally small and dependency-light.  Deterministic JSON
emission canonicalizes structure and Unicode but preserves business values.
Audits that need to compare volatile timestamps or typed paths must call
``audit_projection`` explicitly with the schema fields they own.

The public CLI remains ``scripts/tl.py``; this module is an internal helper.
"""
from __future__ import annotations

import json
import os
import tempfile
import unicodedata
from pathlib import Path
from typing import Any

TRUTHY = {"1", "true", "yes", "on"}

VOLATILE_JSON_KEYS = {
    "seconds", "elapsed_seconds", "duration_seconds", "duration", "elapsed", "wall_ms",
    "server_ms", "client_ms", "_client_ms", "stdout_tail", "stderr_tail",
    "generated_at", "generatedAt", "generated_epoch", "generatedEpoch",
    "created_at", "createdAt", "created_time", "createdTime",
    "updated_at", "updatedAt", "modified_time", "modifiedTime",
    "timestamp", "time", "mtime", "age_days", "out_dir", "temp_dir", "tmp_dir",
    # v1.34.3 (I1 characterization bắt): sweep phơi snapshot_age_s (tuổi cache theo GIÂY) → golden ×2 lệch byte
    # ngay trên 1 máy — cùng lớp bug age_days v1.33.56. Mask cả họ age-giây.
    "snapshot_age_s", "age_s", "age_seconds",
}

PATHISH_KEYS = {
    # Explicit path-typed fields used by CLI/report schemas.  Values under
    # other keys remain untouched even if they happen to look like paths.
    "path", "file", "root", "manifest", "report_path",
    "before", "after", "config_path", "cache_file",
    "input", "output", "out", "out_dir",
    "archive", "archive_path", "zip", "zip_path", "local_path", "source_path", "target_path",
}


def deterministic_enabled(args: Any = None, *, default_on: bool = False) -> bool:
    """Return whether deterministic mode is active for the current command."""
    if args is not None and bool(getattr(args, "deterministic", False)):
        return True
    if default_on:
        return True
    return str(os.environ.get("TL_DETERMINISTIC") or "").strip().lower() in TRUTHY


def unique_preserve_order(items) -> list[str]:
    seen = set()
    out: list[str] = []
    for item in items or []:
        s = str(item)
        if s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


def _default_project_root() -> Path:
    # scripts/tl_core/deterministic.py -> scripts/tl_core -> scripts -> project root
    return Path(__file__).resolve().parents[2]


def stable_string_for_json(s: str, *, project_root: str | os.PathLike | None = None) -> str:
    """Make common path-like strings stable while leaving ordinary text intact."""
    if not s:
        return s
    raw = s.replace("\\", os.sep)
    try:
        p = Path(raw)
    except Exception:
        return s
    if not p.is_absolute():
        # v1.33.56 (review tl_core/F5): chỉ normalize separator khi chuỗi TRÔNG như path (không whitespace) —
        # văn bản thường chứa backslash ('a\\b' trong nội dung pháp lý/ghi chú) không được sửa lệch.
        return s.replace("\\", "/") if ("\\" in s and "/" not in s and " " not in s
                                          and chr(10) not in s and chr(9) not in s) else s
    try:
        root = Path(project_root).resolve() if project_root is not None else _default_project_root().resolve()
        rel = p.resolve().relative_to(root)
        return rel.as_posix()
    except Exception:
        pass
    tmp_roots = unique_preserve_order([tempfile.gettempdir(), os.environ.get("TMP"), os.environ.get("TEMP")])
    for t in tmp_roots:
        if not t:
            continue
        try:
            tp = Path(t).resolve()
            pr = p.resolve()
            if pr == tp or tp in pr.parents:
                return "<tmp>"
        except Exception:
            continue
    return "<abs-path>"


def canonicalize_json(obj: Any) -> Any:
    """Canonicalize structure and Unicode without rewriting business values."""
    if isinstance(obj, dict):
        return {unicodedata.normalize("NFC", str(k)): canonicalize_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [canonicalize_json(x) for x in obj]
    if isinstance(obj, str):
        return unicodedata.normalize("NFC", obj)
    if isinstance(obj, os.PathLike):
        return unicodedata.normalize("NFC", str(obj))
    return obj


def audit_projection(obj: Any, *, volatile_keys=None, path_keys=None,
                     project_root: str | os.PathLike | None = None) -> Any:
    """Build an explicitly-declared comparison projection for an audit.

    This function is never used implicitly by :func:`json_dumps`.  Callers
    must declare which schema fields are volatile or typed as paths.
    """
    volatile = {str(k) for k in (volatile_keys or ())}
    paths = {str(k) for k in (path_keys or ())}
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            key = str(k)
            if key in volatile:
                out[key] = "<volatile>"
            elif key in paths:
                out[key] = (stable_string_for_json(str(v), project_root=project_root)
                            if isinstance(v, (str, os.PathLike))
                            else audit_projection(v, volatile_keys=volatile, path_keys=paths,
                                                  project_root=project_root))
            else:
                out[key] = audit_projection(v, volatile_keys=volatile, path_keys=paths,
                                            project_root=project_root)
        return out
    if isinstance(obj, list):
        return [audit_projection(x, volatile_keys=volatile, path_keys=paths,
                                 project_root=project_root) for x in obj]
    if isinstance(obj, tuple):
        return [audit_projection(x, volatile_keys=volatile, path_keys=paths,
                                 project_root=project_root) for x in obj]
    return canonicalize_json(obj)


def scrub_volatile(obj: Any, *, project_root: str | os.PathLike | None = None,
                   volatile_keys=None, path_keys=None) -> Any:
    """Compatibility alias for an explicit audit projection.

    With no declared fields it preserves all semantic values.  This prevents
    a generic JSON serializer from hiding undeclared instability.
    """
    return audit_projection(obj, volatile_keys=volatile_keys, path_keys=path_keys,
                            project_root=project_root)


def json_dumps(obj: Any, *, deterministic: bool | None = None, default_on: bool = False,
               project_root: str | os.PathLike | None = None) -> str:
    det = deterministic_enabled(default_on=default_on) if deterministic is None else bool(deterministic)
    payload = canonicalize_json(obj) if det else obj
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=det)
