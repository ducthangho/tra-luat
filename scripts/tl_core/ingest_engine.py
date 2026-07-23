# -*- coding: utf-8 -*-
"""tl_core.ingest_engine — r187 (ADR-0004 WP7, tracer-bullet): primitive ENGINE dùng chung cho mọi
đường ingest (profile-ingest → ingest-local → ZIP → cache). Module ĐỘC LẬP stdlib — không bind(),
không import tl_core khác (ingest_contract/zip_ingest gọi VÀO đây, không ngược lại).

Ba primitive:
1. stage_slot(stage)      — stage scheduler: semaphore chặn concurrency theo giai đoạn
                            (upload≤2, nlm≤2 — ticket WP7/r185); stage lạ = không giới hạn.
2. run_scope()/hash_file_once — hash nguồn ĐÚNG 1 LẦN mỗi run: memo process-global theo realpath,
                            chỉ bật trong run_scope (nest được); ngoài scope tính lại như cũ.
                            Ghi nhận: trong 1 scope, re-hash archive để phát hiện file đổi giữa
                            plan↔extract thành memo-hit — guard nội dung per-member lúc extract
                            (so sha256 từng member khi ghi) GIỮ NGUYÊN và là guard thẩm quyền.
3. run_child_inprocess()  — chạy child CLI in-process (subprocess=0) cho cả DRY lẫn APPLY; stdout/
                            stderr route THEO THREAD (proxy thread-local) — redirect_stdout
                            process-global không thread-safe khi child chạy trong ThreadPool.
                            Giới hạn ghi nhận: không có timeout kiểu subprocess (child treo =
                            run treo; GAS client tự có timeout tầng dưới).
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import sys
import threading
from pathlib import Path

# ── 1. Stage scheduler ──
_STAGE_LIMITS = {"upload": 2, "nlm": 2}
_stage_sems: dict = {}
_stage_lock = threading.Lock()


def stage_limits() -> dict:
    """PURE: bảng giới hạn concurrency theo stage (upload≤2, nlm≤2 — WP7)."""
    return dict(_STAGE_LIMITS)


def _sem_for(stage: str):
    s = str(stage or "").strip().lower()
    lim = _STAGE_LIMITS.get(s)
    if not lim:
        return None
    with _stage_lock:
        if s not in _stage_sems:
            _stage_sems[s] = threading.BoundedSemaphore(int(lim))
        return _stage_sems[s]


@contextlib.contextmanager
def stage_slot(stage: str):
    """Giữ 1 slot của stage trong suốt thao tác I/O; stage không khai báo → no-op."""
    sem = _sem_for(stage)
    if sem is None:
        yield
        return
    sem.acquire()
    try:
        yield
    finally:
        sem.release()


# ── 2. Hash-once theo run scope ──
_memo_guard = threading.Lock()
_memo_state = {"depth": 0, "memo": None, "computed": 0}


@contextlib.contextmanager
def run_scope():
    """Bật memo hash cho MỘT run (nest được — scope trong cùng reuse memo ngoài)."""
    with _memo_guard:
        _memo_state["depth"] += 1
        if _memo_state["memo"] is None:
            _memo_state["memo"] = {}
    try:
        yield
    finally:
        with _memo_guard:
            _memo_state["depth"] -= 1
            if _memo_state["depth"] <= 0:
                _memo_state["depth"] = 0
                _memo_state["memo"] = None


def memo_active() -> bool:
    return _memo_state["memo"] is not None


def hash_stats() -> dict:
    """Telemetry/test: số lần hash THẬT đã tính (mọi scope) + trạng thái memo."""
    with _memo_guard:
        return {"computed": int(_memo_state["computed"]), "memo_active": _memo_state["memo"] is not None,
                "memo_size": len(_memo_state["memo"] or {})}


def hash_file_once(path, *, chunk_size: int = 1024 * 1024) -> str:
    """sha256 streaming bộ nhớ giới hạn; trong run_scope memo theo realpath — hash ĐÚNG 1 lần/run."""
    key = str(Path(path).resolve())
    memo = _memo_state["memo"]
    if memo is not None:
        with _memo_guard:
            v = (memo or {}).get(key)
        if v:
            return v
    h = hashlib.sha256()
    with open(key, "rb") as stream:
        while True:
            chunk = stream.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    digest = h.hexdigest()
    with _memo_guard:
        _memo_state["computed"] += 1
        if _memo_state["memo"] is not None:
            _memo_state["memo"][key] = digest
    return digest


# ── 2b. SEC-01 (r188): bounded-read member zip — chống zip-bomb DOCX/XML ──
_DOCX_XML_MAX_MB_DEFAULT = 50


def docx_xml_max_bytes() -> int:
    """Trần bytes GIẢI NÉN cho một member XML của DOCX — env TL_DOCX_XML_MAX_MB
    (mặc định 50, clamp [1, 500]); giá trị rác → mặc định."""
    import os as _os
    try:
        v = int(str(_os.environ.get("TL_DOCX_XML_MAX_MB", "") or _DOCX_XML_MAX_MB_DEFAULT))
    except (TypeError, ValueError):
        v = _DOCX_XML_MAX_MB_DEFAULT
    return max(1, min(v, 500)) * 1024 * 1024


def read_member_bounded(zf, member: str, *, max_bytes: int | None = None) -> bytes:
    """SEC-01 (r188): đọc member zip STREAMING với trần bytes giải nén — file nén nhỏ phình to
    (zip-bomb) bị chặn TRƯỚC khi nuốt RAM, raise ValueError ZIP_MEMBER_BOUND_EXCEEDED.
    Member không tồn tại giữ nguyên ngữ nghĩa KeyError của ZipFile.read."""
    cap = int(max_bytes or docx_xml_max_bytes())
    chunks, total = [], 0
    with zf.open(member, "r") as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > cap:
                raise ValueError(f"ZIP_MEMBER_BOUND_EXCEEDED:{member}:{total}>{cap}")
            chunks.append(chunk)
    return b"".join(chunks)


# ── 3. Child runner in-process với stdout/stderr route theo thread ──
class _ThreadRouteProxy:
    """Proxy file-like: thread có route → ghi vào buffer riêng; thread khác → stream gốc."""

    def __init__(self, original):
        self._orig = original
        self._routes = {}
        self._lock = threading.Lock()

    def _target(self):
        return self._routes.get(threading.get_ident(), self._orig)

    def write(self, s):
        return self._target().write(s)

    def flush(self):
        try:
            self._target().flush()
        except Exception:  # noqa: BLE001
            pass

    def __getattr__(self, name):   # encoding/isatty/… ủy quyền stream gốc
        return getattr(self._orig, name)

    def route(self, buf):
        with self._lock:
            self._routes[threading.get_ident()] = buf

    def unroute(self):
        with self._lock:
            self._routes.pop(threading.get_ident(), None)


_io_guard = threading.Lock()
_io_state = {"depth": 0, "out": None, "err": None}


@contextlib.contextmanager
def _routed_io():
    """Cài proxy (refcount) rồi route thread hiện tại vào buffer riêng — an toàn khi N child song song."""
    with _io_guard:
        if _io_state["depth"] == 0:
            _io_state["out"] = _ThreadRouteProxy(sys.stdout)
            _io_state["err"] = _ThreadRouteProxy(sys.stderr)
            sys.stdout, sys.stderr = _io_state["out"], _io_state["err"]
        _io_state["depth"] += 1
        out, err = _io_state["out"], _io_state["err"]
    bo, be = io.StringIO(), io.StringIO()
    out.route(bo)
    err.route(be)
    try:
        yield bo, be
    finally:
        out.unroute()
        err.unroute()
        with _io_guard:
            _io_state["depth"] -= 1
            if _io_state["depth"] <= 0:
                _io_state["depth"] = 0
                sys.stdout, sys.stderr = out._orig, err._orig
                _io_state["out"] = _io_state["err"] = None


def run_child_inprocess(child_args, *, parser_factory) -> dict:
    """Chạy child CLI in-process (0 subprocess): parse argv bằng parser_factory() → ns.fn(ns).
    Trả CÙNG SHAPE _run_child_tl: {cmd, returncode, ok, json, stdout_tail, stderr_tail} + inprocess=True."""
    args = [str(x) for x in (child_args or []) if str(x)]
    with _routed_io() as (bo, be):
        try:
            ns = parser_factory().parse_args(args)
            rc = ns.fn(ns)
        except SystemExit as e:   # argparse exit / sys.exit trong child
            code = e.code
            rc = int(code) if isinstance(code, int) else (0 if code in (None, "") else 2)
        except Exception as e:  # noqa: BLE001 — child lỗi không được giết parent
            be.write(f"\nCHILD_INPROCESS_ERROR:{type(e).__name__}: {e}")
            rc = 3
    so, se = bo.getvalue(), be.getvalue()
    try:
        payload = json.loads(so) if so.strip().startswith("{") else None
    except Exception:  # noqa: BLE001
        payload = None
    return {"cmd": " ".join(args), "returncode": int(rc or 0), "ok": (rc or 0) == 0,
            "json": payload, "stdout_tail": so[-2000:], "stderr_tail": se[-2000:], "inprocess": True}
