# -*- coding: utf-8 -*-
"""tl_core.regio — I9b (v1.34.14): hạ tầng ĐỌC-GHI registry/manifest/journal (manifest-entries/_entry_*/norm_sohieu/_cache_file + _journaled_reg_write/_verified_reg_*/_apply_gate/journal primitives) tách NGUYÊN VĂN từ tl.py. Thân thật khoá bởi r80a TRƯỚC cut; tl giữ stub; bind REBASE __globals__."""
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
    """REBASE __globals__ từng hàm đã chuyển về namespace SỐNG của tl (khuôn I1-I8)."""
    global _TL
    _TL = tl_module
    import types
    g = globals()
    tg = tl_module.__dict__
    for _n, _fn in list(g.items()):
        if isinstance(_fn, types.FunctionType) and _fn.__module__ == __name__ and _n != "bind":
            _re = types.FunctionType(_fn.__code__, tg, _n, _fn.__defaults__, _fn.__closure__)
            _re.__kwdefaults__ = _fn.__kwdefaults__
            _re.__doc__ = _fn.__doc__
            _re.__module__ = __name__
            g[_n] = _re



def _cache_file(name: str) -> Path:
    return _profile_cache_dir() / name


def _invalidate_manifest_cache() -> None:
    """(MERGE) Sau khi GHI registry (rename/delete/corpus-toggle) → xoá cache manifest LOCAL để lần đọc sau lấy LIVE
    (khỏi đọc cache CŨ nlm rỗng/tên cũ). Lần boot/reg-query kế tự nạp lại."""
    for _n in ("manifest.json", "manifest_index.json"):
        try:
            _p = _cache_file(_n)
            if _p.exists():
                _p.unlink()
        except Exception:
            pass


def _journal_dir() -> Path:
    # MERGE Codex v1.33.10→v1.33.11: env-override — selftest/sandbox + môi trường cache tách profile không
    # mất dấu journal (TL_JOURNAL_DIR > TL_CACHE_DIR/_journal > ~/.tl_journal như cũ).
    explicit = os.environ.get("TL_JOURNAL_DIR")
    if explicit:
        return Path(os.path.expanduser(explicit))
    cache_root = os.environ.get("TL_CACHE_DIR")
    if cache_root:
        return Path(os.path.expanduser(cache_root)) / "_journal"
    return Path(os.path.expanduser("~")) / ".tl_journal"


def _journal_path(run_id: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", str(run_id))[:120] or "run"
    return _journal_dir() / f"{safe}.jsonl"


def _journal_new_run_id(cmd: str) -> str:
    import time as _t
    safe = re.sub(r"[^A-Za-z0-9_-]", "", str(cmd))[:40] or "run"
    return f"{safe}_{int(_t.time())}_{os.getpid()}"


def _journal_append(run_id: str, rec: dict) -> None:
    """Ghi 1 dòng JSONL vào nhật ký (append-only). Best-effort — KHÔNG raise (nhật ký hỏng KHÔNG được làm hỏng lệnh)."""
    try:
        _journal_dir().mkdir(parents=True, exist_ok=True)
        with _journal_path(run_id).open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _journal_resume_state(records: list) -> dict:
    """PURE (test offline): từ các dòng nhật ký → trạng thái resume. `intent` ghi TRƯỚC call remote; `commit` (ok) ghi
    SAU khi verify. Op có intent NHƯNG chưa commit-ok = DỞ/không rõ (ngắt giữa chừng) → caller phải VERIFY remote rồi
    mới quyết retry/skip. done = op đã commit-ok (bỏ qua khi resume)."""
    meta, plan, intents, commits = {}, None, {}, {}
    for r in records or []:
        t = r.get("t")
        if t == "run_start":
            meta = r
        elif t == "plan":
            plan = r
        elif t == "intent" and r.get("key") is not None:
            intents.setdefault(r["key"], r)   # GIỮ intent ĐẦU TIÊN (retry ghi intent 2 lần → 'before' gốc ở bản đầu; undo cần bản gốc)
        elif t == "commit" and r.get("ok") and r.get("key") is not None:
            commits[r["key"]] = r
    inflight = [iv for k, iv in intents.items() if k not in commits]   # ghi intent nhưng chưa commit-ok
    return {"run_id": meta.get("run_id"), "cmd": meta.get("cmd"), "snapshot": meta.get("snapshot"),
            "plan": plan, "done": commits, "done_keys": sorted(commits.keys()),
            "inflight": inflight,
            "counts": {"intents": len(intents), "done": len(commits), "inflight": len(inflight)}}


def _reg_cols_valid(cols) -> tuple:
    """PURE: mọi cột định ghi PHẢI ∈ REGISTRY_SCHEMA_COLS. Bắt lỗi 'ghi mù' kinh điển: cột `so_hieu` (đúng là `sohieu`)
    → webapp BỎ IM LẶNG, patched=0 không báo (sự cố missing-sohieu 193 dòng). Trả (ok, cột_lạ)."""
    col_list = [c.strip() for c in cols.split(",")] if isinstance(cols, str) else list(cols or [])
    col_list = [c for c in col_list if c]
    if not col_list:
        return (False, ["<empty>"])   # cols RỖNG/None → webapp CHỈ vá `nlm_title` mặc định (ghi mù ngoài ý muốn) → CHẶN
    bad = [c for c in col_list if c not in REGISTRY_SCHEMA_COLS]
    return (len(bad) == 0, bad)


def _verify_reg_result(rb: dict, expected: int) -> dict:
    """PURE: đối chiếu kết quả reg_bulk. verified = `ok` VÀ KHÔNG có dòng `missed` (drive_id KHÔNG khớp = hụt THẬT).
    ⚠ **KHÔNG dùng patched làm cờ hụt**: reg_bulk `patched` = số dòng ĐỔI; ghi lại giá trị ĐÃ ĐÚNG → patched=0 nhưng
    dòng VẪN khớp (idempotent) → thành công, KHÔNG phải lỗi. (Sự cố báo động GIẢ 'REG_WRITE_FAIL' khi loop ghi lại giá
    trị đã đúng — log 2026-07-02.) Silent-write cột-sai đã bị `_reg_cols_valid` CHẶN TRƯỚC ghi nên không cần patched ở đây.
    Trả `missed_ids` (miss[] từ API) để commit per-row + `no_change` (patched<expected nhưng không miss = idempotent)."""
    rb = rb or {}
    patched = int(rb.get("patched") or 0)
    reg_ok = bool(rb.get("ok", True))
    miss_ids = rb.get("miss") if isinstance(rb.get("miss"), (list, tuple)) else None
    _missed_raw = rb.get("missed")
    if miss_ids is not None:
        missed = len(miss_ids)
    elif isinstance(_missed_raw, (list, tuple)):      # phòng webapp trả `missed` là LIST thay vì count (chống crash int([...]))
        missed = len(_missed_raw); miss_ids = _missed_raw
    else:
        missed = int(_missed_raw or 0) if isinstance(_missed_raw, (int, str)) else 0
    return {"verified": reg_ok and missed == 0, "patched": patched, "expected": int(expected), "reg_ok": reg_ok,
            "missed": missed, "missed_ids": [str(m) for m in (miss_ids or [])],
            "no_change": reg_ok and missed == 0 and patched < int(expected)}


def _verified_reg_write(g, items: list, cols) -> dict:
    """Bọc reg_bulk AN TOÀN (Pha 1 sẽ thay mọi g.post('reg_bulk',...) trực tiếp): (1) validate cột ∈ schema TRƯỚC ghi
    (chống cột lạ bị bỏ im lặng); (2) sau ghi đối chiếu patched==len(items). Trả verify dict. KHÔNG raise."""
    items = list(items or [])
    ok_cols, bad = _reg_cols_valid(cols)
    if not ok_cols:
        return {"verified": False, "error": "REG_COLS_NOT_IN_SCHEMA", "bad_cols": bad, "patched": 0, "expected": len(items),
                "note": f"Cột {bad} KHÔNG ∈ REGISTRY_SCHEMA_COLS → webapp BỎ IM LẶNG (vd 'so_hieu'≠'sohieu'). KHÔNG ghi."}
    try:
        rb = g.post("reg_bulk", items=items, cols=cols)
    except Exception as e:  # noqa: BLE001
        return {"verified": False, "error": f"REG_BULK_RAISED:{type(e).__name__}", "patched": 0, "expected": len(items)}
    v = _verify_reg_result(rb, len(items))
    v["reg_bulk"] = rb
    return v


def _manifest_cache_age_seconds() -> float | None:
    """Tuổi (giây) của cache manifest LOCAL theo mtime — quyết định có cần force-refresh không (giảm overhead 43s khi vừa refresh)."""
    try:
        import time as _t
        p = _cache_file("manifest.json")
        return (_t.time() - p.stat().st_mtime) if p.exists() else None
    except Exception:
        return None


def _apply_precheck(write_cols=None) -> dict:
    """Chạy preflight invariant TRƯỚC ghi (dùng state môi trường active). Trả {ok, blockers, warnings, checks}. Caller
    ABORT nếu not ok (trừ --force-unsafe). (apply_profile_offline phải chạy trước để TL_REGISTRY_DOC_ID đúng scope.)"""
    active = _active_profile()
    is_base = (active == DEFAULT_PROFILE)
    rid = (os.environ.get("TL_REGISTRY_DOC_ID") or "").strip()
    checks = _preflight_invariants({"registryDocId": rid, "is_base_profile": is_base,
                                    "profile_registry_id": rid, "snapshot_age_seconds": _manifest_cache_age_seconds(),
                                    "write_cols": write_cols})
    return {**_preflight_verdict(checks), "checks": checks, "profile": active}


def _apply_gate(a, write_cols=None, stream=True) -> tuple:
    """Cổng --apply THỐNG NHẤT: chạy precheck; blocker critical → (False, verdict) trừ khi --force-unsafe. Trả (ok, verdict)."""
    v = _apply_precheck(write_cols)
    if v["ok"] or getattr(a, "force_unsafe", False):
        if not v["ok"] and stream:
            print(f"[tl] ⚠ --force-unsafe: BỎ QUA blocker {v['blockers']} (RỦI RO — bạn tự chịu).", file=sys.stderr, flush=True)
        return True, v
    if stream:
        print(json.dumps({"ok": False, "aborted": True, "reason": "PRECHECK_BLOCKED", "blockers": v["blockers"],
                          "detail": [c for c in v["checks"] if not c["ok"] and c["severity"] == "critical"],
                          "note": "SỬA bất biến trên TRƯỚC khi --apply (vd registryDocId về Sheet thật; tạo registry profile). "
                                  "Hoặc --force-unsafe nếu CHẮC (rủi ro clobber/ghi-mù)."}, ensure_ascii=False, indent=2), file=sys.stderr)
    return False, v


def _apply_journal_start(cmd: str, meta: dict | None = None) -> str:
    rec = {"t": "run_start", "cmd": cmd}
    run_id = _journal_new_run_id(cmd)
    rec["run_id"] = run_id
    if isinstance(meta, dict):
        for k, val in meta.items():
            rec[k] = val
    _journal_append(run_id, rec)
    return run_id


def _journaled_reg_write(run_id: str, g, items: list, cols, key_field: str = "drive_id", before_by_key: dict | None = None) -> dict:
    """Ghi registry AN TOÀN + CÓ NHẬT KÝ: (1) journal `intent{before}` TRƯỚC (before=giá trị cũ để undo); (2) verified
    reg-write (validate cột + patched≥expected); (3) journal `commit{verify}` SAU. Trả verify dict (verified/patched/…).
    KHÔNG raise. Tổng quát hoá đường ghi cho MỌI lệnh mutate (Pha 1)."""
    items = list(items or [])
    keys = [str(it.get(key_field) or "") for it in items]
    _cols_list = [c.strip() for c in cols.split(",")] if isinstance(cols, str) else [str(c) for c in (cols or [])]
    for it, k in zip(items, keys):
        # LƯU `set` (giá trị định ghi) + `key_field` → Pha 2 resume LÀM LẠI được op dở; `before` → undo khôi phục.
        rec = {"t": "intent", "op": "reg_bulk", "key": k, "key_field": key_field, "cols": ",".join(_cols_list),
               "set": {c: it.get(c) for c in _cols_list if c in it}}
        if before_by_key and k in before_by_key:
            rec["before"] = before_by_key[k]
        _journal_append(run_id, rec)
    v = _verified_reg_write(g, items, cols)
    # commit PER-ROW dùng `missed_ids` (drive_id KHÔNG khớp = hụt THẬT). Dòng khớp (kể cả idempotent patched=0) = done →
    # KHÔNG còn báo động giả REG_WRITE_FAIL khi ghi lại giá trị đã đúng. bad-cols/error → tất cả not-committed.
    missed_set = set(v.get("missed_ids") or [])
    _reg_ok = bool(v.get("reg_ok", True)) and not v.get("error")
    for k in keys:
        row_ok = _reg_ok and k not in missed_set
        _journal_append(run_id, {"t": "commit", "op": "reg_bulk", "key": k, "ok": row_ok,
                                 "verify": {"patched": v.get("patched"), "expected": v.get("expected"), "missed": v.get("missed"), "error": v.get("error")}})
    # v1.29.2 (AUDIT B5 #1 — bust-cache-after-write THỐNG NHẤT): mọi lệnh mutate đi qua đây → xoá cache manifest LOCAL
    # 1 CHỖ (thay vì nhớ gọi rải rác từng lệnh — trước chỉ 3-4/16 lệnh gọi → đọc sau ghi dính stale). Unlink idempotent,
    # rẻ; lần đọc kế `_load_manifest_full` (không cache) gọi manifest_export → GAS regReadAll_(true) = dữ liệu TƯƠI
    # (né luôn cache đọc 600s server-side). KHÔNG bust khi items rỗng (không có ghi).
    if items:
        _invalidate_manifest_cache()
    return v


def _verified_reg_upsert(g, payload: dict) -> dict:
    """Bọc reg_upsert AN TOÀN (cho khóa immutable: sohieu/goc/name — reg_bulk bỏ IM LẶNG): (1) validate field ghi ∈ schema
    (chống cột lạ); (2) sau ghi verify = `ok` (upsert ĐƯỢC CHẤP NHẬN). ⚠ `updated=False` = giá trị ĐÃ ĐÚNG (idempotent)
    → THÀNH CÔNG, KHÔNG phải hụt (chống báo động giả như reg_bulk patched=0). `changed`=đã thực sự đổi (thông tin).
    Trả {verified, changed, reg_upsert}. KHÔNG raise."""
    fields = [k for k in (payload or {}).keys() if k not in ("drive_id", "confirm", "merge")]
    ok_cols, bad = _reg_cols_valid(fields)
    if not ok_cols:
        return {"verified": False, "error": "REG_COLS_NOT_IN_SCHEMA", "bad_cols": bad}
    try:
        r = g.get("reg_upsert", **payload)
    except Exception as e:  # noqa: BLE001
        return {"verified": False, "error": f"REG_UPSERT_RAISED:{type(e).__name__}"}
    changed = bool(r.get("updated") or r.get("upserted") or r.get("created"))
    ok = bool(r.get("ok"))
    # N3 (v1.33.41 — log rà VBHN-first: `register --goc … --title-vn …` xong dòng 62/2025 vẫn goc=null/
    # title_vn=null): verify cũ CHỈ kiểm `ok` = request ĐƯỢC NHẬN — cột bị webapp bỏ IM LẶNG vẫn 'verified'
    # (cùng lớp ảo giác 'updated:true' của ghi-giá-trị-rỗng). Nay READ-BACK field-level qua reg_get
    # (refresh=true — né cache đọc 600s): field ĐÃ SET mà đọc lại LỆCH → verified=False + fields_dropped LOUD.
    # Read-back lỗi mạng → không phủ nhận write (ok giữ) nhưng ghi readback=FAILED để người vận hành biết CHƯA
    # xác nhận field-level.
    dropped, readback = [], "OK"
    _did = str((payload or {}).get("drive_id") or "")
    if ok and fields and _did:
        try:
            rb = g.get("reg_get", drive_id=_did, refresh="true")
            _rows = (rb.get("rows") or []) if isinstance(rb, dict) else []
            if _rows:
                _row = _rows[0] or {}
                for k in fields:
                    want = str(payload.get(k) or "").strip()
                    got = str(_row.get(k) or "").strip()
                    if want and got != want:
                        dropped.append({"col": k, "want": want[:80], "got": got[:80]})
            else:
                readback = "NO_ROW"   # reg_get không trả row → KHÔNG kết luận (không phủ nhận write đã ok)
        except Exception as e:  # noqa: BLE001
            readback = f"FAILED:{type(e).__name__}"
    # #5 backlog (v1.34.17): giá trị RỖNG cho cột thường bị webapp BỎ IM LẶNG by-design (chỉ nlm_*/note clear
    # được qua reg_clear) — cảnh báo LOUD thay vì để người vận hành tưởng đã xoá (ca sohieu gán nhầm hồ sơ BHXH).
    _empty_ignored = sorted(k for k in fields if not str((payload or {}).get(k) or "").strip())
    _empty_extra = ({"empty_ignored": _empty_ignored,
                     "note_empty": "giá trị RỖNG bị webapp BỎ QUA cho cột thường (by-design — chỉ nlm_*/note "
                                   "clear được qua reg_clear); muốn đính chính: ghi giá trị mới hoặc chú thích note/title_vn."}
                    if _empty_ignored else {})
    # #6 backlog (v1.34.17): FIELDS_DROPPED → TỰ RETRY per-field ĐÚNG 1 VÒNG (ca thật: ghi nhiều trường 1 lượt
    # bị rớt, ghi lại lượt nhỏ thì verified) rồi re-readback; vẫn lệch → báo như cũ.
    _retried = []
    if dropped and _did:
        for d in dropped:
            try:
                g.get("reg_upsert", drive_id=_did, **{d["col"]: d["want"]})
                _retried.append(d["col"])
            except Exception:  # noqa: BLE001
                pass
        if _retried:
            try:
                rb2 = g.get("reg_get", drive_id=_did, refresh="true")
                _rows2 = (rb2.get("rows") or []) if isinstance(rb2, dict) else []
                if _rows2:
                    _row2 = _rows2[0] or {}
                    dropped = [d for d in dropped
                               if str(_row2.get(d["col"]) or "").strip() != str(d["want"]).strip()]
            except Exception:  # noqa: BLE001
                pass
    if dropped:
        return {"verified": False, "changed": changed, "reg_upsert": r, "error": "FIELDS_DROPPED_ON_WRITE",
                "fields_dropped": dropped, **({"fields_retried": _retried} if _retried else {}), **_empty_extra,
                "note": "reg_upsert ok NHƯNG read-back thấy field LỆCH (đã tự retry per-field 1 vòng) — webapp bỏ cột "
                        "im lặng (kiểm tên cột ∈ REG_COLS_ / GAS version; KHÔNG tin updated:true suông)."}
    return {"verified": ok, "changed": changed, "reg_upsert": r,
            **({"fields_retried": _retried} if _retried else {}), **_empty_extra,
            **({"readback": readback} if readback != "OK" else {})}


def _journaled_reg_upsert(run_id: str, g, payload: dict, before: dict | None = None) -> dict:
    """Ghi reg_upsert CÓ NHẬT KÝ: intent{before} → verified upsert → commit{verify}. Trả verify dict."""
    did = str((payload or {}).get("drive_id") or "")
    _set = {k: payload[k] for k in (payload or {}) if k not in ("drive_id", "confirm", "merge")}
    rec = {"t": "intent", "op": "reg_upsert", "key": did, "key_field": "drive_id",
           "cols": ",".join(_set.keys()), "set": _set}
    if before:
        rec["before"] = before
    _journal_append(run_id, rec)
    v = _verified_reg_upsert(g, payload)
    _journal_append(run_id, {"t": "commit", "op": "reg_upsert", "key": did, "ok": bool(v.get("verified")),
                             "verify": {"error": v.get("error"), "changed": v.get("changed")}})
    _invalidate_manifest_cache()   # v1.29.2 (AUDIT B5 #1): bust-cache-after-write thống nhất (như _journaled_reg_write)
    return v


def _journaled_reg_clear(run_id: str, g, drive_id: str, cols, before: dict | None = None) -> dict:
    """v1.29.4: XÓA giá trị cột registry CÓ NHẬT KÝ qua action `reg_clear` (keyed drive_id + confirm=yes server-side).
    intent{op:reg_clear, before=giá trị cũ → UNDO khôi phục được qua `tl undo` (restore đi reg_bulk giá trị non-empty)}
    → gọi reg_clear → commit{ok = cleared≥1}. Validate cols ∈ _REG_CLEARABLE_COLS TRƯỚC. Trả {verified, cleared, resp}."""
    _cols_list = [c.strip() for c in cols.split(",")] if isinstance(cols, str) else [str(c) for c in (cols or [])]
    bad = [c for c in _cols_list if c not in _REG_CLEARABLE_COLS]
    if bad:
        return {"verified": False, "cleared": 0, "error": f"COLS_NOT_CLEARABLE:{','.join(bad)}"}
    rec = {"t": "intent", "op": "reg_clear", "key": str(drive_id), "key_field": "drive_id",
           "cols": ",".join(_cols_list), "set": {c: "" for c in _cols_list}}
    if before:
        rec["before"] = before
    _journal_append(run_id, rec)
    try:
        r = g.get("reg_clear", drive_id=drive_id, cols=",".join(_cols_list), confirm="yes")
    except Exception as e:  # noqa: BLE001
        r = {"ok": False, "error": f"REG_CLEAR_RAISED:{type(e).__name__}"}
    cleared = int(r.get("cleared") or 0) if isinstance(r, dict) else 0
    ok = bool(isinstance(r, dict) and r.get("ok") and cleared >= 1)
    _journal_append(run_id, {"t": "commit", "op": "reg_clear", "key": str(drive_id), "ok": ok,
                             "verify": {"cleared": cleared, "error": (r or {}).get("error")}})
    _invalidate_manifest_cache()
    return {"verified": ok, "cleared": cleared, "resp": r}


def _reg_before_from_manifest(items: list, cols_list, key_field: str = "drive_id") -> dict:
    """v1.29.2 (AUDIT B1 #2): before-snapshot BEST-EFFORT cho undo — đọc manifest cache LOCAL (có thể stale vài phút;
    chỉ phục vụ `tl undo` tham khảo, KHÔNG phải điều kiện ghi). Map key manifest: drive_id qua _entry_drive_id
    (manifest đổi drive_id→id), sohieu qua _entry_sohieu (manifest đổi sohieu→so_hieu). Lỗi/không cache → {} (im lặng)."""
    try:
        ents = _manifest_entries(refresh=False)
    except Exception:
        return {}
    if key_field == "drive_id":
        by = {_entry_drive_id(e): e for e in ents if _entry_drive_id(e)}
    else:
        by = {str(e.get(key_field) or ""): e for e in ents if e.get(key_field)}
    out = {}
    for it in (items or []):
        k = str((it or {}).get(key_field) or "")
        e = by.get(k)
        if not e:
            continue
        out[k] = {c: (_entry_sohieu(e) if c == "sohieu" else str(e.get(c) or "")) for c in (cols_list or [])}
    return out


def norm_sohieu(s: str) -> str:
    """Chuẩn hóa số hiệu về khóa: 113/2025/QH15 → 113-2025-QH15 (Đ→D, HOA)."""
    if not s:
        return ""
    s = s.strip().upper().replace("Đ", "D")
    s = re.sub(r"[\/\s]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    # Manifest cũ có VBHN VPQH lưu thiếu đoạn "VBHN" (19-VPQH, 40-VPQH).
    # Với VPQH, số trần không đủ định danh; nội bộ luôn dùng NN-VBHN-VPQH.
    m = re.fullmatch(r"(\d{1,4})-VPQH", s)
    if m:
        return f"{m.group(1)}-VBHN-VPQH"
    return s


def _entry_goc(e: dict):
    return e.get("goc") or e.get("goc_luat") or e.get("targets") or e.get("target") or ""


def _entry_sua_doi(e: dict) -> str:
    return e.get("sua_doi") or e.get("sua_doi_bo_sung") or e.get("amended_by") or e.get("superseded_by") or ""


def _entry_confirmed(e: dict | None) -> str:
    """Nhãn 'ĐÃ RÀ KỸ & CHẮC ĐÚNG' = field registry `verified` (có sẵn REG_COLS_, sống qua regen2). '' nếu chưa confirm.
    Entry có nhãn này → dedup/source-map/locate TIN dùng luôn, bỏ qua re-review nhiễu (tăng tốc rà soát)."""
    v = str((e or {}).get("verified") or "").strip()
    return "" if v.lower() in ("", "no", "false", "0", "chua", "pending", "none") else v


def _entry_sohieu(e: dict) -> str:
    return e.get("so_hieu") or e.get("sohieu") or e.get("soHieu") or ""


def _entry_drive_id(e: dict) -> str:
    return e.get("drive_id") or e.get("driveId") or e.get("gdoc_id") or e.get("id") or ""


def _entry_cat(e: dict) -> str:
    return str(e.get("cat") or e.get("path") or "")


def _entry_nlm(e: dict) -> str:
    return e.get("nlm_source_id") or e.get("nlmSourceId") or ""


def _entry_nlm_notebook_id(e: dict) -> str:
    return str(e.get("nlm_notebook_id") or e.get("notebook_id") or "").strip()


def _entry_corpus_true(e: dict) -> bool:
    return str(e.get("corpus") or "").strip().lower() == "true"


def _entry_is_draft(e: dict) -> bool:
    text = " ".join(str(x or "") for x in (
        _entry_name(e), e.get("hieuluc"), e.get("hieu_luc"), e.get("status"),
        e.get("note"), e.get("verified"), e.get("title_vn"), e.get("nlm_title"),
    ))
    norm = _strip_accents(text).lower()
    return (
        _entry_name(e).upper().startswith("DUTHAO_")
        or "du thao" in norm
        or "draft" in norm
        or "chua hieu luc" in norm
        or "chua co hieu luc" in norm
    )


def _entry_on_nlm_live(e: dict) -> bool:
    """CÓ trên NLM THẬT (live): có source_id VÀ status KHÔNG phải removed/deleted. B5: relation-check/_summ_entry trước
    in nlm=True chỉ vì có source_id (dù đã gỡ) → lệch reg-query (removed). Dùng cái này để 2 lệnh nhất quán."""
    return bool(_entry_nlm(e)) and not _nlm_status_removed(str(e.get("nlm_status") or ""))


def _entry_date_text(e: dict) -> str:
    for k in ("ngay_ban_hanh", "ngayBanHanh", "ngaybanhanh", "issued_date", "issue_date", "date", "ngay", "ban_hanh"):
        v = e.get(k)
        if v:
            return str(v)
    return ""


def _entry_issue_date_iso(e: dict | None) -> str | None:
    """(port Codex hotfix) Ngày ban hành ISO yyyy-mm-dd nếu metadata đủ rõ; None khi chỉ có năm/text mơ hồ.
    Dùng cho cổng date-coverage: hạ PAUSE khi VBHN ban hành KHÔNG sớm hơn mọi luật-sửa có ngày rõ."""
    s = _entry_date_text(e or {})
    if not s:
        return None
    s = unicodedata.normalize("NFC", str(s))
    m = re.search(r"\b(20\d{2}|19\d{2})\s*[-/.]\s*(\d{1,2})\s*[-/.]\s*(\d{1,2})\b", s)
    if m:
        return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    m = re.search(r"\b(\d{1,2})\s*[/\-.]\s*(\d{1,2})\s*[/\-.]\s*(20\d{2}|19\d{2})\b", s)
    if m:
        return f"{int(m.group(3)):04d}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"
    low = _strip_accents(s).lower()
    m = re.search(r"\bngay\s+(\d{1,2})\s+thang\s+(\d{1,2})\s+nam\s+(20\d{2}|19\d{2})\b", low)
    if m:
        return f"{int(m.group(3)):04d}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"
    return None


def _year_from_text_safe(text: str) -> int | None:
    """Suy năm ban hành một cách an toàn.

    Không lấy năm bất kỳ trong title/từ khóa, vì VBHN thường chứa số hiệu luật gốc
    như 84/2015/QH13 hoặc 22/2019/TT-BYT. Những năm đó KHÔNG phải issue_year
    của văn bản hợp nhất. Chỉ nhận năm khi có ngữ cảnh ngày ban hành/năm ban hành
    hoặc năm tách rõ trong tên file/metadata chuyên biệt.
    """
    txt = unicodedata.normalize("NFC", str(text or ""))
    pats = [
        r"(?:ngày|ngay)\s+\d{1,2}\s*(?:/|-|\s+tháng\s+|\s+thang\s+)\s*\d{1,2}\s*(?:/|-|\s+năm\s+|\s+nam\s+)(19\d{2}|20\d{2})",
        r"(?:năm|nam|issue[_\s-]*year|issued[_\s-]*year|nam[_\s-]*ban[_\s-]*hanh)\D{0,8}(19\d{2}|20\d{2})",
        r"(?:^|[_\s.-])(19\d{2}|20\d{2})(?=$|[_\s.-])",
    ]
    low = _strip_accents(txt).lower()
    for pat in pats:
        m = re.search(pat, low, re.I)
        if m:
            return int(m.group(1))
    return None


def _entry_issue_year(e: dict) -> int | None:
    # issue_year_goc_token: VBHN — năm BẢN GỐC cũ nhất trong chuỗi goc KHÔNG bao giờ là năm ban hành của bản hợp nhất.
    # (vd VBHN_123 ban hành 2025 nhưng issue_year/tên file dính '64-2020' của luật gốc PPP → trước trả 2020 sai.)
    base_goc_year = None
    if _is_vbhn_entry(e):
        _bk = _vbhn_base_key(e)
        base_goc_year = _sohieu_year(_bk) if _bk else None

    def _reject(y: int | None) -> bool:
        return y is not None and base_goc_year is not None and y == base_goc_year

    # 1) Chỉ tin các trường chuyên biệt trước (bỏ nếu trùng năm bản gốc của VBHN — bị nhiễm).
    explicit = e.get("issue_year") or e.get("issued_year") or e.get("year") or e.get("nam") or e.get("nam_ban_hanh")
    if explicit:
        y = _year_from_text_safe(str(explicit))
        if y and not _reject(y):
            return y
        if not y:
            m0 = re.fullmatch(r"\s*(19\d{2}|20\d{2})\s*", str(explicit))
            if m0 and not _reject(int(m0.group(1))):
                return int(m0.group(1))

    # 2) Ngày ban hành là nguồn an toàn — TIN tuyệt đối (không reject theo năm gốc).
    y = _year_from_text_safe(_entry_date_text(e))
    if y:
        return y

    # 3) Tên file/nhan đề NLM có năm tách bằng _ . - hoặc khoảng trắng. BỎ token 'goc_...' trước khi tách năm
    # (năm trong token goc là năm bản gốc, không phải VBHN). Không đọc tukhoa/keywords/trich yếu tự do.
    for text in (_entry_name(e), e.get("nlm_title"), e.get("title_vn")):
        y = _year_from_text_safe(_strip_goc_token(text))
        if y and not _reject(y):
            return y
    return None


def _entry_query_match(q: str, e: dict, include_subject: bool = False) -> bool:
    """Một điểm vào chung cho locate/source-map/reg-query/hygiene query matching."""
    qkey = norm_sohieu(q.replace("_", "-")) if _looks_like_sohieu_query(q) else ""
    if qkey and _sohieu_key_entry(e) == qkey:
        return True
    hay = _entry_subject_text(e) if include_subject else _entry_name(e)
    qn, hn = _strip_accents(q).lower(), _strip_accents(hay).lower()
    qnk, hnk = _name_key(q), _name_key(hay)
    return bool(
        (qn and qn in hn)
        or (qnk and hnk and (qnk in hnk or hnk in qnk))
        or _name_subset_match(q, hay)
        or _name_phrase_match(q, hay)
    )


def _entry_query_match_safe_for_hygiene(q: str, e: dict) -> bool:
    """Query match cho hygiene: không để tên hẹp/sai kéo omnibus vào plan chủ đề hẹp.

    Nếu query là số hiệu chính xác thì vẫn cho qua để người vận hành soi văn bản đó.
    Với query chủ đề/tên, bản có OMNIBUS_NARROW_TITLE_CHECK hoặc TITLE_METADATA_MISMATCH
    phải khớp cả metadata tiêu đề, không chỉ filename bị đặt nhầm.
    """
    qkey = norm_sohieu(q.replace("_", "-")) if _looks_like_sohieu_query(q) else ""
    if qkey and _sohieu_key_entry(e) == qkey:
        return True
    if not _entry_query_match(q, e, include_subject=False):
        return False
    flags = set(_title_flags(e))
    if (not _is_vbhn_entry(e)) and (flags & {"OMNIBUS_NARROW_TITLE_CHECK", "TITLE_METADATA_MISMATCH"}):
        meta = _field_text(e, _META_TITLE_KEYS)
        return bool(meta and _entry_query_match(q, {"name": meta}, include_subject=False))
    return True


def _entry_quarantined(e: dict) -> bool:
    """#6: dòng đã CÁCH LY — nằm trong cat quarantine, HOẶC corpus=false & không còn trên NLM (bản trơ bị guard loại).
    Dùng để KHÔNG nhồi các dòng đã xử lý vào WARN/risky (giảm nhiễu); chúng vẫn hiện ở direct_hits."""
    if _is_quarantine_cat(_entry_cat(e)):
        return True
    return str(e.get("corpus") or "").strip().lower() == "false" and not _entry_nlm(e)


def _entry_score(e: dict) -> int:
    """Heuristic chọn canonical: không cho nguồn NLM mồ côi/bản quarantine thắng.
    A1: VBHN-first áp cho CẢ truy vấn theo tên — phạt nặng quarantine/orphan, thưởng VBHN có 'goc' + còn hiệu lực."""
    score = 0
    name = _entry_name(e)
    sohieu = _entry_sohieu(e) or _parse_sohieu_from_name(name)
    cat = _entry_cat(e)
    ghost = _entry_nlm(e) and (not name) and (not sohieu) and _bad_cat(cat)
    if _entry_nlm(e) and not ghost:
        score += 50
    if ghost:
        score -= 500
    elif _entry_nlm(e) and (not name or not sohieu) and _bad_cat(cat):
        score -= 200
    elif (not sohieu) and _bad_cat(cat):
        score -= 80
    # A1: bản trong _ZZZ_QUARANTINE KHÔNG được làm canonical kể cả khi truy vấn theo tên chủ đề.
    if _is_quarantine_cat(cat):
        score -= 400
    # P0-1 (log rà): file THÔ (.docx/.pdf/.html) CHƯA trên NLM KHÔNG được thắng bản GDoc native cùng số hiệu
    # (vd VBHN có sidecar .docx). Phạt CHỈ khi sidecar CHƯA push NLM (raw đã-push NLM = canonical thật, vd PDF
    # gốc đã nạp → KHÔNG phạt, tránh hạ oan bản raw-only hợp lệ). Sidecar đúng nghĩa luôn ngoài NLM → vẫn bị hạ.
    if _is_raw_no_gdoc_name(name) and not _entry_nlm(e):
        score -= 300
    if _is_vbhn_entry(e):
        score += 20
        if _goc_keys(e):           # VBHN-first: hợp nhất có gốc → ưu tiên rõ rệt
            score += 35
    if sohieu: score += 25
    cat_l = str(cat or "").lower()
    if cat_l and "root" not in cat_l and cat_l not in ("", "(root)") and not _is_quarantine_cat(cat):
        score += 15
    hl = str(e.get("hieuluc") or e.get("hieu_luc") or "").lower()
    if "còn" in hl: score += 8
    if "hết" in hl or "thay thế" in hl or "het" in _strip_accents(hl): score -= 30
    if str(e.get("corpus", "")).lower() == "true": score += 5
    if str(e.get("trashed", "")).lower() == "true": score -= 100
    return score


def _entry_mime(e: dict) -> str:
    return str(e.get("mime") or e.get("mimeType") or e.get("mime_type") or "").strip().lower()


def _entry_google_doc(e: dict) -> bool:
    if not _entry_drive_id(e):
        return False
    mime = _entry_mime(e)
    return ("application/vnd.google-apps.document" in mime) or (not mime and not _is_raw_no_gdoc_name(_entry_name(e)))


def _entry_raw_no_gdoc(e: dict) -> bool:
    """Entry KHÔNG đọc-sâu được (chưa GDoc native): tên có đuôi .docx/.pdf/.html HOẶC mime thô (word/pdf/html/rtf/odt)."""
    mime = _entry_mime(e)
    if _is_raw_no_gdoc_name(_entry_name(e)):
        return True
    return bool(mime and "application/vnd.google-apps.document" not in mime and any(
        x in mime for x in ("word", "pdf", "html", "rtf", "text", "opendocument")))


def _deep_entry_rank(e: dict) -> int:
    """Điểm chọn target ĐỌC SÂU: GDoc native +80, corpus +35, NLM-live +20, có drive_id +20; raw −900, quarantine −700."""
    score = _entry_score(e)
    if _entry_drive_id(e):
        score += 20
    else:
        score -= 1000
    if _entry_corpus_true(e):
        score += 35
    if _entry_on_nlm_live(e):
        score += 20
    if _entry_google_doc(e):
        score += 80
    if _entry_raw_no_gdoc(e):
        score -= 900
    if _entry_quarantined(e):
        score -= 700
    return score


def _atomic_write_text(p, text: str):
    """v1.29.1 (audit cache-coherence): ghi file cache ATOMIC (tmp + os.replace) — process bị giết giữa write_text
    TRUNCATE để lại manifest.json cụt → boot/reads sau parse fail hoặc đọc nửa dữ liệu âm thầm."""
    tmp = Path(str(p) + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(str(tmp), str(p))


def _rebuild_manifest_index(full: dict) -> None:
    """v1.29.4 (FIX log LIVE i5 'sau source-rename lệnh kế timeout/PARSEERR tới khi boot --refresh'): bust-cache xoá
    CẢ manifest_index.json nhưng chỉ `tl boot` mới dựng lại → locate/reg-query mất index → rơi fallback webapp chậm/
    dễ timeout. Nay: MỖI lần _load_manifest_full tải manifest mới → tự DỰNG LẠI index (boot.build_index, best-effort)
    → index tự-hồi-phục, KHÔNG cần nhớ chạy boot --refresh sau mỗi lần sửa."""
    try:
        idx = _imp("boot").build_index(full)
        _atomic_write_text(_cache_file("manifest_index.json"), json.dumps(idx, ensure_ascii=False))
    except Exception:
        pass


def _load_manifest_full(refresh: bool=False) -> dict:
    """Đọc manifest đầy đủ có entries. Ưu tiên cache do `tl boot`; nếu chưa có thì tải qua webapp."""
    _profile_cache_dir().mkdir(parents=True, exist_ok=True)
    p = _cache_file("manifest.json")
    if p.exists() and not refresh:
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    g = _gas()
    head = _gas_get_retry(g, "manifest_export")     # v1.29.4 i5: đọc idempotent + retry transient (hết PARSEERR loạt)
    if head.get("ok") is False:
        return head
    if head.get("entries"):
        _atomic_write_text(p, json.dumps(head, ensure_ascii=False))
        _rebuild_manifest_index(head)   # v1.29.4 i5: index tự-hồi-phục sau bust
        return head
    mid = head.get("manifestId") or head.get("manifestFileId") or head.get("driveFileId")
    if not mid:
        rd = _gas_get_retry(g, "manifest")
        mid = rd.get("manifestFileId") or rd.get("driveFileId")
    if not mid:
        return {"ok": False, "error": "không lấy được manifestId để tải entries", "head": head}
    # R1 (nhóm-D READ gws-primary): tải manifest.json qua DIRECT-MEDIA gws (raw, KHÔNG cap 9MB webapp, nhanh hơn,
    # byte-exact) TRƯỚC; thiếu cred/lỗi → FALLBACK GAS b64 (đường cũ). CHỈ đổi đường ĐỌC file JSON — KHÔNG đụng
    # manifest_export (D2: treeHash/scan ở Apps Script) ⇒ 0 rủi ro phân kỳ. Xem tra-luat-DESIGN-nhomD-gws-primary.md.
    full = None
    try:
        _tlg = _imp("tl_gws")
        _cred = _tlg._read_gws_cred()
        if _cred:
            _dl = str(p) + ".dl"                                 # v1.29.1: tải vào TẠM — chỉ replace sau parse+validate OK
            _tlg._drive_media_download(mid, _dl, _cred)          # (streaming; kill giữa chừng KHÔNG hỏng cache đang có)
            full = json.loads(Path(_dl).read_text(encoding="utf-8"))
            # An toàn (defense-in-depth): manifest HỢP LỆ phải có entries/files/rows là LIST. Nếu KHÔNG (tải cụt/hỏng
            # mà JSON vẫn parse được, hoặc body lạ) → coi như THẤT BẠI → FALLBACK GAS (KHÔNG trả manifest rỗng âm thầm).
            if not any(isinstance(full.get(k), list) for k in ("entries", "files", "rows")):
                raise ValueError("manifest gws thiếu entries/files/rows (list) — nghi tải cụt/hỏng")
            os.replace(_dl, str(p))
    except Exception as e:
        if not getattr(_load_manifest_full, "_gws_warned", False):
            _load_manifest_full._gws_warned = True
            print(f"[manifest] gws direct-media lỗi ({type(e).__name__}: {e}) → FALLBACK GAS b64. [ẩn lặp sau]",
                  file=sys.stderr)
        full = None
    if full is None:
        d = _gas_get_retry(g, "download", fileId=mid)   # v1.29.4 i5: retry transient
        if d.get("ok") is False or not d.get("b64"):
            return {"ok": False, "error": "download manifest thất bại", "download": d, "head": head}
        try:
            full = json.loads(base64.b64decode(d["b64"]).decode("utf-8"))
        except Exception as e:
            return {"ok": False, "error": f"parse manifest JSON lỗi: {e}"}
    full["manifestId"] = mid
    full.setdefault("ok", True)
    _atomic_write_text(p, json.dumps(full, ensure_ascii=False))
    _rebuild_manifest_index(full)       # v1.29.4 i5: index tự-hồi-phục sau bust (hết PHẢI boot --refresh tay)
    return full


def _manifest_entries(refresh: bool=False) -> list[dict]:
    m = _load_manifest_full(refresh=refresh)
    if m.get("ok") is False:
        raise RuntimeError(m.get("error") or json.dumps(m, ensure_ascii=False)[:500])
    return m.get("entries") or m.get("files") or m.get("rows") or []


def _sohieu_key_entry(e: dict) -> str:
    sh = _entry_sohieu(e) or _parse_sohieu_from_name(_entry_name(e))
    return norm_sohieu((sh or "").replace("_", "-"))


def _entry_md5(e: dict) -> str:
    return str(e.get("md5") or e.get("md5Checksum") or "")


def _entry_row_kind(e: dict) -> str:
    return str(e.get("row_kind") or "own").strip().lower() or "own"


def _entry_is_own_thuong(e: dict) -> bool:
    corpus = str(e.get("corpus") or "").strip().lower()
    loai = str(e.get("loai") or "").strip().lower()
    return _entry_row_kind(e) == "own" and (loai == "thuong" or corpus in {"false", "thuong"})


def _summ_entry(e: dict|None) -> dict|None:
    if not e:
        return None
    return {
        "drive_id": _entry_drive_id(e), "name": _entry_name(e), "sohieu": _entry_sohieu(e),
        # B5: `nlm` = CÓ TRÊN NLM LIVE (False nếu removed) → khớp reg-query; `nlm_status` giữ chi tiết.
        "sohieu_key": _sohieu_key_entry(e), "cat": _entry_cat(e), "nlm": _entry_on_nlm_live(e),
        "nlm_source_id": _entry_nlm(e), "nlm_notebook_id": _entry_nlm_notebook_id(e),
        "nlm_status": str(e.get("nlm_status") or ""),
        "row_kind": e.get("row_kind") or "own", "corpus": e.get("corpus") or "",
        "hieuluc": e.get("hieuluc") or e.get("hieu_luc") or "", "issue_year": _entry_issue_year(e),
        "score": _entry_score(e),
        "confirmed": _entry_confirmed(e),   # nhãn đã-rà-kỹ (registry.verified) → tin dùng luôn
        "flags": _title_flags(e),
    }


def _entry_years(e: dict) -> set[str]:
    """Lấy năm từ metadata/tên để phát hiện số VBHN tái sử dụng theo năm."""
    txt = _field_text(e, (
        "ngay", "ngay_ban_hanh", "ngayBanHanh", "banhanh", "ban_hanh", "issued",
        "date", "year", "nam", "name", "title", "title_vn", "trichyeu", "trich_yeu", "summary",
    ))
    yrs = set(re.findall(r"(?<!\d)(?:20\d{2}|19\d{2})(?!\d)", txt or ""))
    iy = _entry_issue_year(e)
    if iy:
        yrs.add(str(iy))
    return yrs


def _base_manifest_entries(config_path: str | None = None, refresh: bool = False) -> tuple[list[dict], str | None]:
    """A (v1.30.0): đọc entries manifest NỀN VBQPPL khi đang đứng ở profile dự án (TL_BASE_ALSO) — snapshot env
    overlay, đọc qua _profile_manifest_entries_for(vbqppl) rồi KHÔI PHỤC nguyên trạng (kể cả TL_PROFILE).
    Cache nền rơi đúng thư mục cache gốc (per-profile dir tách sẵn) — không nhiễm cache profile."""
    if _active_profile() == DEFAULT_PROFILE:
        return _profile_manifest_entries_for(DEFAULT_PROFILE, config_path, refresh)
    snap = {k: os.environ.get(k) for k in _PROFILE_ENV_OVERLAY_KEYS}
    try:
        return _profile_manifest_entries_for(DEFAULT_PROFILE, config_path, refresh)
    finally:
        for k, v in snap.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def _notebook_from_manifest_json(mj: dict, profile_name: str) -> tuple[str, str | None]:
    """Review v1.30.0 (PURE, CONFIRMED): lấy notebookId từ manifest JSON CHỈ khi manifest thuộc ĐÚNG profile
    (trường 'profile' khớp tên/slug, so không-phân-biệt-hoa-thường) — manifest lạ lạc vào folder KHÔNG được phép
    cấp notebookId (nguy cơ ghi đè notebook đúng bằng notebook profile khác)."""
    mj = mj if isinstance(mj, dict) else {}
    nb = str(mj.get("notebookId") or mj.get("notebook_id") or "").strip()
    mp = str(mj.get("profile") or "").strip()
    if mp and _profile_file_slug(mp).lower() != _profile_file_slug(profile_name).lower():
        return "", (f"MANIFEST_PROFILE_MISMATCH: manifest ghi profile='{mp}' ≠ '{profile_name}' — KHÔNG lấy "
                    f"notebookId từ manifest này; truyền --notebook tường minh nếu chắc chắn.")
    return nb, None


def _manifest_placeholder(profile: str, root_id: str = "", notebook_id: str = "") -> dict:
    import datetime as _dt
    return {
        "version": EXPECT_VERSION,
        "schema": "uniform-v1",
        "profile": profile,
        "rootFolderId": root_id,
        "notebookId": notebook_id,
        "generatedAt": _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "treeHash": "",
        "count": 0,
        "corpus_count": 0,
        "entries": [],
    }


def _b64_text(s: str) -> str:
    import base64
    return base64.b64encode((s or "").encode("utf-8")).decode("ascii")


def _mime_from_info(info: dict) -> str:
    f = info.get("file") if isinstance(info.get("file"), dict) else {}
    return str(info.get("mime") or info.get("mimeType") or f.get("mimeType") or "").strip()


def _verify_registry_sheet(g, registry_id: str) -> dict:
    if not registry_id:
        return {"ok": False, "error": "REGISTRY_ID_EMPTY"}
    info = g.get("info", fileId=registry_id)
    mime = _mime_from_info(info) if isinstance(info, dict) else ""
    if mime and mime != REGISTRY_SHEET_MIME:
        return {"ok": False, "error": "REGISTRY_NOT_GOOGLE_SHEET", "registryDocId": registry_id, "mime": mime}
    add = g.get("reg_addcols", registryDocId=registry_id, confirm="yes")
    ok = bool(add.get("ok")) and int(add.get("cols") or 0) == len(REGISTRY_SCHEMA_COLS)
    return {
        "ok": ok,
        "registryDocId": registry_id,
        "mime": mime or REGISTRY_SHEET_MIME,
        "reg_addcols": add,
        "error": None if ok else (add.get("error") or "REGISTRY_SCHEMA_VERIFY_FAILED"),
    }


def _create_profile_registry_sheet(g, meta_id: str, profile: str) -> dict:
    slug = _profile_file_slug(profile)
    csv = ",".join(REGISTRY_SCHEMA_COLS) + "\n"
    up = g.post("upload", b64=_b64_text(csv), name=f"tra_luat_registry.{slug}.csv",
                mime="text/csv", folderId=meta_id, convert="false", register="false",
                share="false", force="true")
    csv_id = up.get("fileId") or up.get("id")
    if not csv_id:
        return {"ok": False, "step": "registry_csv_upload", "detail": up}
    cv = g.get("copy_convert", fileId=csv_id, name=f"tra_luat_registry.{slug}",
               folderId=meta_id, toType="sheets", register="false", share="false")
    reg_id = cv.get("fileId") or cv.get("id")
    if not reg_id:
        return {"ok": False, "step": "registry_sheet_convert", "csvFileId": csv_id, "detail": cv}
    ver = _verify_registry_sheet(g, reg_id)
    return {"ok": bool(ver.get("ok")), "csvFileId": csv_id, "registryDocId": reg_id,
            "convert": cv, "verify": ver, "error": ver.get("error")}


def _entry_hieuluc_date(e: dict | None) -> str | None:
    """B2 fallback: lấy ngày hiệu lực ISO từ field hieuluc của registry (nếu có dạng dd/mm/yyyy)."""
    s = str((e or {}).get("hieuluc") or (e or {}).get("hieu_luc") or "")
    m = re.search(r"(\d{1,2})\s*[/\-.]\s*(\d{1,2})\s*[/\-.]\s*(\d{4})", s)
    return f"{int(m.group(3)):04d}-{int(m.group(2)):02d}-{int(m.group(1)):02d}" if m else None


def _load_phapdien() -> dict:
    """(4) Bảng 45 chủ đề pháp điển chính thức (references/phap_dien_45.json): {code: {ten, folder, exists}}.
    Gộp custom 00/46. Trả {} nếu thiếu file."""
    for cand in (Path(__file__).resolve().parent.parent / "references" / "phap_dien_45.json",
                 Path.cwd() / "references" / "phap_dien_45.json"):
        try:
            if cand.exists():
                d = json.loads(cand.read_text(encoding="utf-8"))
                m = dict(d.get("chu_de") or {})
                m.update(d.get("custom_non_phapdien") or {})
                return m
        except Exception:
            pass
    return {}


def _load_linhvuc() -> dict:
    """G3: bảng 45+2 chủ đề + quy_tac_ranh_gioi + alias (references/linhvuc_phapdien.json). {} nếu thiếu/parse lỗi
    (cảnh báo, KHÔNG im lặng). Mirror _load_subject_clusters/_load_phapdien (cache + nhiều ứng viên đường dẫn)."""
    global _LINHVUC_CACHE
    if _LINHVUC_CACHE is None:
        here = Path(__file__).resolve().parent
        for cand in (here.parent / "references" / "linhvuc_phapdien.json", here / "linhvuc_phapdien.json",
                     Path.cwd() / "references" / "linhvuc_phapdien.json"):
            try:
                if cand.exists():
                    _LINHVUC_CACHE = json.loads(cand.read_text(encoding="utf-8")); break
            except Exception as e:  # noqa: BLE001
                sys.stderr.write(f"[tl] ⚠ linhvuc_phapdien.json KHÔNG parse được ({type(e).__name__}: {e}) — quy tắc "
                                 f"ranh giới G3 RỖNG; ĐỪNG kết luận cat. Re-sync references/linhvuc_phapdien.json.\n")
                _LINHVUC_CACHE = {}; break
        if _LINHVUC_CACHE is None:
            _LINHVUC_CACHE = {}
    return _LINHVUC_CACHE
