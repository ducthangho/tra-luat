# -*- coding: utf-8 -*-
"""Deterministic JSON/path helpers for ``tl.py``.

This module is intentionally small and dependency-light.  It centralizes the
rules that make read-only JSON output stable across repeated runs:

* volatile time/duration fields are masked;
* absolute paths are made project-relative where possible;
* temp paths are normalized to ``<tmp>``;
* JSON is emitted with sorted keys when deterministic mode is enabled.

The public CLI remains ``scripts/tl.py``; this module is an internal helper.
"""
from __future__ import annotations

import json
import os
import tempfile
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

PATHISH_KEYS = {"path", "file", "root", "manifest", "report_path"}


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


def scrub_volatile(obj: Any, *, project_root: str | os.PathLike | None = None) -> Any:
    """Return a copy of ``obj`` with volatile fields/path-like values normalized."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            key = str(k)
            if key in VOLATILE_JSON_KEYS:
                out[key] = "<volatile>"
            elif key.endswith("_path") or key in PATHISH_KEYS:
                out[key] = stable_string_for_json(str(v), project_root=project_root) if isinstance(v, (str, os.PathLike)) else scrub_volatile(v, project_root=project_root)
            else:
                out[key] = scrub_volatile(v, project_root=project_root)
        return out
    if isinstance(obj, list):
        return [scrub_volatile(x, project_root=project_root) for x in obj]
    if isinstance(obj, tuple):
        return [scrub_volatile(x, project_root=project_root) for x in obj]
    if isinstance(obj, (str, os.PathLike)):
        return stable_string_for_json(str(obj), project_root=project_root)
    return obj


def json_dumps(obj: Any, *, deterministic: bool | None = None, default_on: bool = False,
               project_root: str | os.PathLike | None = None) -> str:
    det = deterministic_enabled(default_on=default_on) if deterministic is None else bool(deterministic)
    payload = scrub_volatile(obj, project_root=project_root) if det else obj
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=det)
