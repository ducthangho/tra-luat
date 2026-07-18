# -*- coding: utf-8 -*-
"""tl_core.source_ops — ĐỢT A (v1.34.64, kế hoạch `ke-hoach-guard-va-boc-tl-core-2026-07-18.md` §4):
tách NGUYÊN VĂN cụm source-CRUD khỏi tl_core/ingest_ops.py (237KB = 69% trần mount ~343KB — lớp sự cố #5
cắt cụt, self-heal không cứu): 6 cmd `register/recat/source-rename/source-delete/source-update-corpus/
shared-source-fix` + 9 helper riêng-cụm + 2 hằng `_REG_CLEAR_*` (re-export TRỰC TIẾP ở tl.py — bẫy I11:
hằng KHÔNG vào _STUB_MAP). Helper dùng chung 2 phía (`_looks_like_drive_id/_resolve_drive_id_source/
_drive_info_file/_file_parents`…) Ở LẠI ingest_ops; WRITE-INFRA đa-module (`_journaled_reg_write/
_apply_gate/_verified_reg_upsert`…) ở tl.py — bind-REBASE khiến mọi tên thấy nhau qua tl globals.
Hành vi khoá bởi charact §6.1 (.tl_state/charact_pre_A) + r125 wiring + golden 0-diff."""
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
    """REBASE __globals__ từng hàm đã chuyển về namespace SỐNG của tl (khuôn I1/I2)."""
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


_REG_CLEAR_FREE_COLS = {"nlm_source_id", "nlm_status", "nlm_pushed_at", "nlm_title", "nlm_notebook_id", "note"}
_REG_CLEAR_PROTECTED = {"drive_id", "name"}


def _register_clear(a, g) -> int:
    """#5 TRỌN (v1.34.20) + v1.34.21 resilience (thẩm định review Codex, grilling 2026-07-10):
    register --clear-cols → primitive `_journaled_reg_clear(force=)` (server ≥2.21.2j 2-tầng) — journal
    intent{key_field,set,before} chuẩn undo/resume + try/except quanh reg_clear. PRECHECK reg_get: drive_id
    không khớp dòng nào → NO_SUCH_ROW rc=2 KHÔNG ghi (trước v1.34.21: readback no-row → verified:true GIẢ).
    Verified = dòng CÒN TỒN TẠI và cột RỖNG sau readback; dòng tồn tại + cleared=0 = already_empty THÀNH CÔNG
    idempotent (chạy lại sau đứt mạng vẫn rc=0 — KHÔNG dùng cleared>=1 làm điều kiện). Qua _apply_gate như
    mọi đường ghi registry."""
    cols = [c.strip() for c in str(a.clear_cols or "").split(",") if c.strip()]
    did = (getattr(a, "drive_id", None) or "").strip()
    if not did or not cols:
        print("[tl] --clear-cols cần --drive-id và danh sách cột.", file=sys.stderr); return 2
    if getattr(a, "confirm", None) != "yes":
        print("[tl] --clear-cols là thao tác XOÁ GIÁ TRỊ → cần --confirm yes.", file=sys.stderr); return 2
    bad = sorted(set(cols) & _REG_CLEAR_PROTECTED)
    if bad:
        print(json.dumps({"ok": False, "error": "REG_CLEAR_PROTECTED_COLS", "cols": bad,
                          "note": "drive_id/name là khoá cấu trúc — không bao giờ clear."},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    needs_force = [c for c in cols if c not in _REG_CLEAR_FREE_COLS]
    ok_gate, _gv = _apply_gate(a, write_cols=",".join(cols))
    if not ok_gate:
        return 2

    def _rb_row():
        rb = g.get("reg_get", drive_id=did, refresh="true")
        rows = rb.get("rows") if isinstance(rb, dict) else None
        for row in (rows or []):
            if isinstance(row, dict) and str(row.get("drive_id") or "").strip() == did:
                return row
        # reg_get keyed theo drive_id — nhận hàng đầu nếu server không echo cột drive_id
        if rows and isinstance(rows[0], dict) and "drive_id" not in rows[0]:
            return rows[0]
        return None

    try:
        pre = _rb_row()
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"ok": False, "error": f"REG_PRECHECK_FAILED:{type(e).__name__}",
                          "note": "Không đọc được dòng registry để đối chiếu (mạng/auth?) — KHÔNG ghi."},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 1
    if pre is None:
        print(json.dumps({"ok": False, "error": "NO_SUCH_ROW", "drive_id": did,
                          "note": "drive_id không khớp dòng registry nào — kiểm `tl reg-query --json`. KHÔNG ghi."},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    run_id = _apply_journal_start("register-clear", {"drive_id": did, "cols": ",".join(cols)})
    _before = {c: (pre.get(c) or "") for c in cols}   # before từ dòng LIVE (chuẩn hơn manifest có-thể-stale)
    _clr = _journaled_reg_clear(run_id, g, did, ",".join(cols), before=_before, force=bool(needs_force))
    resp = _clr.get("resp") if isinstance(_clr.get("resp"), dict) else {}
    ok = bool(resp.get("ok"))
    still, rb_err, row2 = [], None, None
    if ok:
        try:
            row2 = _rb_row()
        except Exception as e:  # noqa: BLE001
            rb_err = f"READBACK_FAILED:{type(e).__name__}"
    if row2 is not None:
        still = [c for c in cols if str(row2.get(c) or "").strip()]
        verified = not still
    else:
        verified = False
        if ok and not rb_err:
            rb_err = "ROW_GONE_AFTER_CLEAR"
    # commit CUỐI theo READBACK — resume/close-plan tôn trọng verdict này (đè commit cleared>=1 của primitive
    # để re-run đã-rỗng không bị treo inflight).
    _journal_append(run_id, {"t": "commit", "op": "reg_clear", "key": did, "ok": verified,
                             "verify": {"cleared": _clr.get("cleared"), "still_set": still,
                                        "error": _clr.get("error") or rb_err or resp.get("error")}})
    out = {"ok": ok, "verified": verified, "cleared_cols": cols, "forced": bool(needs_force),
           "cleared": _clr.get("cleared"), "journal": run_id, "reg_clear": resp}
    if verified and int(_clr.get("cleared") or 0) == 0:
        out["already_empty"] = True
    if still:
        out["still_set"] = still
    if rb_err:
        out["readback_error"] = rb_err
    if _clr.get("error"):
        out["clear_error"] = _clr.get("error")
    if not ok and "force" in str(resp.get("error") or ""):
        out["note"] = "Server chưa 2.21.2j? Kiểm `tl ping` version; deploy GAS mới rồi chạy lại."
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if verified else 1


def _reg_row_present(g, drive_id) -> bool | None:
    """#3 (v1.34.30, log grill): CÓ dòng registry khớp drive_id này KHÔNG? Dùng để phân biệt 'vừa INSERT dòng mới'
    vs 'khớp giá trị cũ, không đổi' — cả hai đều cho reg_upsert `updated:false` (ảo giác ghi-hụt). reg_get refresh=true
    né cache 600s. Trả True/False; None khi KHÔNG xác định được (reg_get lỗi mạng) → caller bỏ qua field inserted."""
    try:
        rb = g.get("reg_get", drive_id=str(drive_id), refresh="true")
    except Exception:  # noqa: BLE001
        return None
    if not isinstance(rb, dict):
        return None
    return bool(rb.get("rows") or [])


def cmd_register(a) -> int:
    g = _gas()
    if getattr(a, "clear_cols", None):
        # v1.34.40 A.2 (log Chỉ thị — 'sai mà báo verified:true'): --clear-cols đi kèm field set từng bị VỨT
        # LẶNG LẼ (early-return bỏ mọi --loai/--title-vn/… mà vẫn báo verified). Nay TỪ CHỐI lệnh hỗn hợp rc=2
        # — 2 thao tác khác cơ chế ghi (reg_clear force-gate vs reg_upsert), tách 2 lệnh là tất định nhất.
        _set_fields = [k for k in ("sohieu", "loai", "name", "cat", "linhvuc", "goc", "hieuluc", "sua_doi",
                                   "nlm_source_id", "nlm_notebook_id", "nlm_status", "nlm_title", "tukhoa",
                                   "corpus", "title_vn", "row_kind")
                       if getattr(a, k, None) not in (None, "")]
        if _set_fields:
            print(json.dumps({"ok": False, "step": "clear_cols_mixed_with_set", "rejected_fields": _set_fields,
                              "error": "--clear-cols KHÔNG đi cùng field set (trước đây field set bị bỏ im lặng). "
                                       "Chạy 2 lệnh riêng: (1) register --drive-id … --clear-cols …; "
                                       "(2) register --drive-id … --loai …/--title-vn …"},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
        return _register_clear(a, g)
    if a.bulk:
        items = json.loads(Path(a.bulk).read_text(encoding="utf-8"))
        # P0-1 LỚP 1 cho --bulk (MERGE AUDIT 07/2026 — v1.33.12 ta chỉ guard đường đơn): item drive_id CẮT CỤT/
        # sai định dạng → reg_bulk cũng chèn dòng rác. --force-insert để bỏ qua (cố ý).
        _bad_did = sorted({(it or {}).get("drive_id") for it in items
                           if (it or {}).get("drive_id") and not _looks_like_drive_id((it or {}).get("drive_id"))})
        if _bad_did and not getattr(a, "force_insert", False):
            print(f"[tl] register --bulk CHẶN: {len(_bad_did)} drive_id quá ngắn/sai định dạng (nghi CẮT CỤT): "
                  f"{_bad_did[:5]}. Dùng ID đầy đủ hoặc --force-insert. KHÔNG ghi.", file=sys.stderr)
            return 2
        # P0-1 bulk LỚP 2 (MERGE nhánh-3 v1.33.14): id đúng-dạng nhưng KHÔNG tồn tại (manifest + Drive live)
        # cũng chặn — reg_bulk với drive_id lạ khớp 0 dòng hoặc tệ hơn tuỳ webapp; đằng nào cũng là input sai.
        if not getattr(a, "force_insert", False):
            try:
                _known = {_entry_drive_id(e) for e in _manifest_entries() if _entry_drive_id(e)}
            except Exception:  # noqa: BLE001
                _known = set()

            def _bulk_prober(_fid):
                _fg = _imp("transport").drive_op("files_get", file_id=_fid, _quiet=True)
                return bool(isinstance(_fg, dict) and _fg.get("ok") and (_fg.get("file") or {}).get("id"))

            _really_missing = _register_bulk_missing(items, _known, _bulk_prober)
            if _really_missing:
                print(json.dumps({"ok": False, "error": "DRIVE_IDS_NOT_FOUND",
                                  "missing_count": len(_really_missing),
                                  "missing_drive_ids": _really_missing[:10],
                                  "note": "drive_id không có trong manifest lẫn Drive (probe cap 20) — kiểm id "
                                          "hoặc --force-insert nếu cố ý."}, ensure_ascii=False, indent=2),
                      file=sys.stderr)
                return 2
        # GUARD cat: chặn folder rác gõ tay (vd '30_To_chuc_bo_may_nha_nuoc' = số 30 + tên cat 35) — reg_bulk
        # KHÔNG validate, ghi đại sẽ lệch folder vật lý ↔ registry. Dùng `tl recat --cat <số>` để đổi cat an toàn.
        bad_cat = sorted({it.get("cat") for it in items if it.get("cat") and not _is_valid_cat_value(it.get("cat"))})
        if bad_cat:
            print(f"[tl] register --bulk CHẶN: cat KHÔNG thuộc taxonomy 45+2: {bad_cat}. Dùng mã số (vd 30) hoặc tên "
                  f"folder ĐÚNG từ `tl cat-list`; đổi cat nên dùng `tl recat --cat <số>`. KHÔNG ghi.", file=sys.stderr)
            return 2
        # v1.29.2 (AUDIT B1 #2): gate + journal + verified-write — trước là g.post reg_bulk TRẦN (không precheck/
        # journal/verify → thuộc nhóm đường ghi lọt lưới). cols mặc định 'nlm_title' = ĐÚNG default webapp (giữ hành vi).
        # Items có thể TRỘN khóa (webapp khớp per-item drive_id HOẶC nlm_source_id) → BUCKET 2 batch theo key_field
        # (review: 1 key_field cho cả batch trộn → journal key='' → false-committed + undo hỏng dòng đó).
        _cols_str = (a.cols or "nlm_title").strip()
        _b_drive = [it for it in items if (it or {}).get("drive_id")]
        _b_src = [it for it in items if not (it or {}).get("drive_id") and (it or {}).get("nlm_source_id")]
        _b_none = len(items) - len(_b_drive) - len(_b_src)
        if _b_none:
            print(f"[tl] register --bulk CHẶN: {_b_none} item KHÔNG có drive_id lẫn nlm_source_id → không khớp được "
                  f"dòng registry nào. Sửa items.json.", file=sys.stderr)
            return 2
        ok_gate, _gv = _apply_gate(a, write_cols=_cols_str)
        if not ok_gate:
            return 2
        run_id = _apply_journal_start("register-bulk", {"items": len(items), "cols": _cols_str})
        _cols_list = [c.strip() for c in _cols_str.split(",") if c.strip()]
        _verified_all, _rbs, _missed_all = True, [], []
        for _kf, _batch in (("drive_id", _b_drive), ("nlm_source_id", _b_src)):
            if not _batch:
                continue
            v = _journaled_reg_write(run_id, g, _batch, _cols_str, key_field=_kf,
                                     before_by_key=_reg_before_from_manifest(_batch, _cols_list, _kf))
            rb = v.get("reg_bulk") or {}
            _mids = [str(m) for m in (v.get("missed_ids") or [])]
            _missed_all.extend(_mids)
            _verified_all = _verified_all and bool(v.get("verified"))
            _rbs.append({**rb, "key_field": _kf, "verified": bool(v.get("verified")),
                         "patched": v.get("patched"), "missed": v.get("missed"),
                         **({"missed_ids": _mids} if _mids else {}),
                         **({"error": v.get("error")} if v.get("error") else {})})
        _out = {"ok": _verified_all, "batches": _rbs, "journal": run_id}
        # #1 (v1.34.30, log grill): reg_bulk chỉ UPDATE dòng ĐÃ TỒN TẠI. Dòng key không khớp = `missed` — TRƯỚC đây
        # chỉ nằm chìm trong batches[].miss → operator tưởng 'patched:0' là thành công. Nay SURFACE top-level LOUD.
        if _missed_all:
            _out["missed_count"] = len(_missed_all)
            _out["missed_ids"] = _missed_all[:20]
            _out["note_missed"] = ("reg_bulk KHÔNG insert — các key trên không khớp dòng registry nào nên bị BỎ. "
                                   "Tạo dòng MỚI: đường đơn `register --drive-id <id> --force-insert` (reg_upsert "
                                   "insert-if-absent), hoặc `profile-from-nlm --add-missing` cho nguồn nlm_only.")
        # cờ đặt-tên gây hiểu lầm: --force-insert trên --bulk CHỈ bỏ qua kiểm client, KHÔNG khiến reg_bulk insert.
        if getattr(a, "force_insert", False):
            _out["force_insert_note"] = ("--force-insert trên --bulk chỉ BỎ QUA kiểm client (drive_id format/tồn tại) "
                                         "— reg_bulk vẫn UPDATE-only, KHÔNG insert. Muốn insert: đường đơn / from-nlm --add-missing.")
        print(json.dumps(_out, ensure_ascii=False))
        return 0 if _verified_all else 1
    if not a.drive_id:
        print("[tl] cần --drive-id (reg_upsert) hoặc --bulk items.json (reg_bulk)", file=sys.stderr)
        return 1
    # P0-1 (v1.33.12 + LỚP 1 v1.33.13): reg_upsert là INSERT-IF-ABSENT theo drive_id — id sai/cắt cụt = CHÈN
    # DÒNG RÁC im lặng. Lớp 1 (offline, rẻ): FORMAT — id <20 ký tự = cắt cụt, lỗi RÕ ngay không tốn round-trip.
    if not getattr(a, "force_insert", False) and not _looks_like_drive_id(a.drive_id):
        print(json.dumps({"ok": False, "error": "DRIVE_ID_MALFORMED", "drive_id": a.drive_id,
                          "note": "drive_id quá ngắn/sai định dạng (Drive ID thật ≥20 ký tự [A-Za-z0-9_-]) — "
                                  "nghi CẮT CỤT khi copy. Dùng ID ĐẦY ĐỦ; cố ý → --force-insert."},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    # Lớp 2: TỒN TẠI — id đúng dạng nhưng không có trong manifest lẫn Drive live → vẫn chặn.
    if not getattr(a, "force_insert", False) and not _register_target_exists(a.drive_id):
        print(json.dumps({"ok": False, "error": "DRIVE_ID_NOT_FOUND", "drive_id": a.drive_id,
                          "note": "drive_id KHÔNG có trong manifest lẫn Drive (files_get) — reg_upsert sẽ INSERT "
                                  "dòng rác rỗng nên bị CHẶN (P0-1). Kiểm id ĐẦY ĐỦ (hay bị cắt cụt khi copy); "
                                  "nếu cố ý tạo dòng mới không gắn Drive → --force-insert. Dọn rác lỡ chèn: "
                                  "`tl reg-delete --drive-ids <id> --force`."},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    # reg_upsert: dùng khóa 'sohieu' (KHÔNG so_hieu) — xem API_CONTRACT.md mục 0
    payload = {"drive_id": a.drive_id}
    _REG_FIELDS = ("sohieu", "loai", "name", "cat", "linhvuc", "goc", "hieuluc",
                   "sua_doi", "nlm_source_id", "nlm_notebook_id", "nlm_status", "nlm_title", "tukhoa", "corpus",
                   "title_vn", "row_kind")   # v1.29.7 #7: row_kind sửa được qua CLI (parser choices đã chặn giá trị lạ)
    # v1.29.4 (FIX log LIVE 'register --nlm-source-id \"\" không xóa được'): giá trị RỖNG trước đây bị DROP client-side
    # (if v: — falsy) → upsert phần còn lại trả updated=true = ẢO GIÁC đã xóa. Nay: arg RỖNG TƯỜNG MINH ("") = lệnh XÓA
    # field → route action `reg_clear` (chỉ cột clearable — webapp allowed-list); cột KHÔNG xóa được → CHẶN LOUD.
    _clear_cols = [k for k in _REG_FIELDS if getattr(a, k, None) == ""]
    _bad_clear = [k for k in _clear_cols if k not in _REG_CLEARABLE_COLS]
    if _bad_clear:
        print(json.dumps({"ok": False, "error": "COLS_NOT_CLEARABLE", "cols": _bad_clear,
                          "note": f"Webapp CHỈ cho xóa: {sorted(_REG_CLEARABLE_COLS)}. Cột khác không xóa được qua "
                                  "upsert (giá trị rỗng bị bỏ qua by design) — ghi giá trị mới thay vì xóa."},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    for k in _REG_FIELDS:
        v = getattr(a, k, None)
        if v:
            # P2-7: chuẩn hoá ENUM loai/hieuluc TRƯỚC khi ghi registry → lọc/đếm theo loại tin cậy về sau.
            if k in ("loai", "hieuluc"):
                _v0 = v
                v = _normalize_loai(v) if k == "loai" else _normalize_hieuluc(v)
                if v != _v0:
                    print(f"[tl] chuẩn hoá {k}: {_v0!r} → {v!r}", file=sys.stderr)
            payload[k] = v
    # BẤT BIẾN ĐẶT TÊN: số hiệu VBHN PHẢI có NĂM (số VBHN tái dùng theo năm → collision). Cảnh báo nếu ghi sohieu
    # VBHN thiếu năm (không chặn — vẫn cho ghi, nhưng nhắc dùng NN-YYYY-VBHN-XXX / `tl vbhn-year-fix`).
    if _VBHN_NOYEAR_RE.fullmatch(norm_sohieu(payload.get("sohieu", ""))):
        print(f"[tl] ⚠ VBHN_SOHIEU_NO_YEAR: '{payload['sohieu']}' THIẾU năm → số VBHN tái dùng theo năm sẽ COLLISION. "
              f"Dùng dạng NN-YYYY-VBHN-XXX (năm ban hành VBHN), hoặc chạy `tl vbhn-year-fix` để backfill.", file=sys.stderr)
    # GUARD cat: chặn ghi folder rác (xem _is_valid_cat_value). Đổi cat nên dùng `tl recat --cat <số>`.
    if payload.get("cat") and not _is_valid_cat_value(payload["cat"]):
        print(f"[tl] register CHẶN: cat '{payload['cat']}' KHÔNG thuộc taxonomy 45+2 (xem `tl cat-list`); đổi cat nên "
              f"dùng `tl recat --cat <số>`. KHÔNG ghi.", file=sys.stderr)
        return 2
    # v1.29.2 (AUDIT B1 #2): reg_upsert đơn cũng qua gate + journaled-upsert (trước g.get trần) — có intent{before}
    # từ manifest (best-effort) → `tl undo` khôi phục được (kể cả khóa immutable sohieu/goc vì đi reg_upsert).
    _fields = [k for k in payload if k != "drive_id"]
    if not _fields and not _clear_cols:
        print("[tl] register: không có field nào để ghi/xóa.", file=sys.stderr)
        return 1
    ok_gate, _gv = _apply_gate(a, write_cols=",".join(_fields + _clear_cols))
    if not ok_gate:
        return 2
    run_id = _apply_journal_start("register", {"drive_id": a.drive_id, "cols": ",".join(_fields + _clear_cols)})
    v = {"verified": True}
    r = {}
    # #3 (v1.34.30, log grill): reg_upsert trả `updated:false` cho CẢ 'vừa insert dòng mới' LẪN 'khớp giá trị cũ,
    # không đổi' → operator tưởng ghi hụt, phải reg-query lại. Precheck reg_get TRƯỚC ghi để phát cờ `inserted` rõ.
    _existed_before = _reg_row_present(g, a.drive_id) if _fields else None
    if _fields:
        _before = (_reg_before_from_manifest([payload], _fields) or {}).get(str(a.drive_id))
        v = _journaled_reg_upsert(run_id, g, payload, before=_before)
        r = v.get("reg_upsert") or {}
    _clr = None
    if _clear_cols:
        _cbefore = (_reg_before_from_manifest([{"drive_id": a.drive_id}], _clear_cols) or {}).get(str(a.drive_id))
        _clr = _journaled_reg_clear(run_id, g, a.drive_id, ",".join(_clear_cols), before=_cbefore)
    _all_ok = bool(v.get("verified")) and (bool(_clr.get("verified")) if _clr is not None else True)
    _inserted = (not _existed_before) if (_fields and _existed_before is not None) else None
    print(json.dumps({**r, "verified": _all_ok, "journal": run_id,
                      **({"inserted": _inserted} if _inserted is not None else {}),
                      **({"cleared_cols": _clear_cols, "cleared": _clr.get("cleared"),
                          **({"clear_error": _clr.get("error") or (_clr.get("resp") or {}).get("error")}
                             if not _clr.get("verified") else {})} if _clr is not None else {}),
                      **({"error": v.get("error")} if v.get("error") else {})}, ensure_ascii=False))
    return 0 if _all_ok else 1


def _register_bulk_missing(items: list, known_ids: set, live_prober, cap: int = 20) -> list:
    """P0-1 bulk LỚP 2 (MERGE nhánh-3 v1.33.14 — PURE, testable): item drive_id đúng-dạng nhưng KHÔNG có trong
    manifest → probe Drive live tối đa `cap` id (mỗi probe 1 round-trip); quá cap → coi là missing luôn (bulk
    đăng-ký-file-mới hàng loạt là hiếm; muốn ép → --force-insert). Trả danh sách id thật sự không tồn tại."""
    missing = [str((it or {}).get("drive_id")) for it in (items or [])
               if (it or {}).get("drive_id") and (it or {}).get("drive_id") not in known_ids]
    really = []
    for did in missing[:cap]:
        try:
            if not live_prober(did):
                really.append(did)
        except Exception:  # noqa: BLE001
            really.append(did)
    really.extend(missing[cap:])
    return really

def _register_target_exists(drive_id: str, live_prober=None) -> bool:
    """P0-1 (v1.33.12 — log phiên khắc phục: `register --drive-id <id CẮT CỤT>` → reg_upsert INSERT dòng registry
    MỚI RỖNG, ok:true không báo, registry 746→747 sai mọi mẫu số): drive_id phải TỒN TẠI — trong manifest cache,
    HOẶC trên Drive live (files_get — cho file VỪA upload chưa vào cache, luồng ingest hợp lệ). PURE-ish:
    live_prober tiêm được để test offline."""
    try:
        if any(_entry_drive_id(e) == drive_id for e in _manifest_entries()):
            return True
    except Exception:  # noqa: BLE001
        pass
    try:
        if live_prober is None:
            def live_prober(fid):
                _fg = _imp("transport").drive_op("files_get", file_id=fid, _quiet=True)
                return bool(isinstance(_fg, dict) and _fg.get("ok") and (_fg.get("file") or {}).get("id"))
        return bool(live_prober(drive_id))
    except Exception:  # noqa: BLE001
        return False


def cmd_recat(a) -> int:
    """Di dời 1+ file → folder chủ đề (mkdir đúng tên nếu thiếu) + cập nhật registry cat. DRY mặc định; --apply để chạy.
    --quarantine: chuyển vào QUARANTINE (cách ly khỏi corpus). Thay ~chục snippet move+reg_bulk tay."""
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    code = "QUARANTINE" if getattr(a, "quarantine", False) else _norm_cat(getattr(a, "cat", "") or "")
    ids = [x for x in (getattr(a, "drive_id", None) or []) if x]
    if not code or not ids:
        print("[tl] recat: cần <drive_id...> và --cat NN (hoặc --quarantine).", file=sys.stderr); return 2
    pd = _load_phapdien()
    valid = set(pd.keys()) | {"QUARANTINE"}
    if code not in valid:
        print(json.dumps({"ok": False, "error": f"cat '{code}' không thuộc 45 chủ đề/QUARANTINE", "hint": "xem tl cat-list"}, ensure_ascii=False), file=sys.stderr); return 2
    # G3: cảnh báo ADVISORY nếu quy_tac_ranh_gioi (suy theo TÊN) gợi cat KHÁC --cat yêu cầu. KHÔNG chặn (giữ omnibus/
    # trường hợp hợp lệ); --force-cat để xác nhận cố ý. Best-effort lookup tên qua manifest offline.
    boundary = []
    if code != "QUARANTINE" and not getattr(a, "force_cat", False):
        try:
            _ents = {_entry_drive_id(e): e for e in _manifest_entries()}
        except Exception:
            _ents = {}
        for did in ids:
            nm = _entry_name(_ents.get(did, {})) if _ents else ""
            fc, rule = _cat_boundary_rule(nm) if nm else (None, None)
            if fc and fc != code:
                boundary.append({"drive_id": did, "name": nm, "rule_cat": fc, "rule": rule})
                print(f"  ⚠ BOUNDARY_CONFLICT: '{nm[:46]}' → quy tắc gợi cat {fc} ≠ --cat {code} ({rule}). "
                      f"--force-cat nếu cố ý.", file=sys.stderr)
    # P1-1 (v1.33.12 — log: `recat --cat 05` khi registry cat='05' trơ trả rc=0 mà KHÔNG relabel, bare-cat 36→36):
    # registry từ nay ghi NHÃN ĐỦ canonical `NN_Ten` (khớp cat-list/folder) — nhãn trơ cùng mã vẫn được RELABEL
    # (webapp sẽ patch vì giá trị khác), không còn 'đã đúng cat' giả.
    _reg_label = _cat_reg_label(code)
    plan = {"cat": code, "reg_label": _reg_label, "cat_label": _reg_label,   # cat_label = alias (vocab patch AUDIT 07/2026)
            "ten": (pd.get(code) or {}).get("ten"), "n": len(ids),
            "drive_ids": ids, "boundary_warnings": boundary}
    if not getattr(a, "apply", False):
        plan["mode"] = "DRY"; plan["note"] = "--apply để chạy (mkdir đúng tên canonical nếu cần + move + reg cat=NHÃN ĐỦ)."
        print(json.dumps(plan, ensure_ascii=False, indent=2)); return 0
    cols = "cat,nlm_source_id" if code == "QUARANTINE" else "cat"
    _ok_gate, _pfv = _apply_gate(a, write_cols=cols)   # (Pha 1) chống clobber/mispoint/ghi-mù TRƯỚC khi ghi
    if not _ok_gate:
        return 2
    run_id = _apply_journal_start("recat", {"cat": code, "n": len(ids)})
    g = _gas()
    folder, created = _resolve_cat_folder(g, code)
    if not folder:
        print(json.dumps({"ok": False, "step": "resolve_cat", "cat": code}, ensure_ascii=False), file=sys.stderr); return 2
    _before = {}
    try:
        _bm = {_entry_drive_id(e): e for e in _manifest_entries()}
        _before = {did: {"cat": _entry_cat(_bm.get(did, {}))} for did in ids if did in _bm}
    except Exception:
        _before = {}
    reg = []
    for did in ids:
        r = g.get("move", fileId=did, folderId=folder, removeFromParent="true")
        row = {"drive_id": did, "cat": _reg_label}   # P1-1: nhãn ĐỦ canonical, không phải mã trơ
        if code == "QUARANTINE":
            row["nlm_source_id"] = ""
        reg.append(row)
        print(f"  recat→{_reg_label} {did[:18]:18s} {r.get('ok')}{' '+(r.get('error') or '')}")
    v = _journaled_reg_write(run_id, g, reg, cols, before_by_key=_before)   # journal intent{before cat}+verify
    patched = v.get("patched") or 0
    _missed = v.get("missed") or 0
    _journal_append(run_id, {"t": "run_end", "ok": bool(v.get("verified")), "counts": {"moved": len(ids), "reg_patched": patched, "missed": _missed}})
    print(json.dumps({"ok": True, "cat": code, "folder_created": created, "moved": len(ids), "reg_patched": patched, "reg_missed": _missed, "journal": run_id}, ensure_ascii=False))
    # LOUD chỉ khi có dòng MISS THẬT (drive_id không khớp) — KHÔNG cảnh báo khi patched=0 do cat đã đúng sẵn (idempotent).
    if not v.get("verified"):
        print(f"[tl] ⚠ recat: {_missed} dòng registry KHÔNG khớp drive_id (cat CHƯA cập nhật) — {v.get('missed_ids')}. KHẮC PHỤC: "
              f"`tl boot --refresh` (row mới webapp chưa index?) rồi recat lại. (patched={patched} — patched=0 mà không miss = cat đã đúng, KHÔNG lỗi.)", file=sys.stderr)
        return 1
    return 0


def _shared_source_id_groups(entries: list) -> list:
    """PURE: FALSE-LINK NLM — ≥2 drive_id KHÁC nhau cùng 1 nlm_source_id (backfill/reconcile gắn nhầm). NGUY HIỂM:
    xóa nguồn của 1 row làm GÃY link của row kia (đúng ca NQ42 user gặp 2026-06-30). Trả [{source_id, rows[]}]."""
    by_sid: dict = {}
    for e in entries:
        sid = (_entry_nlm(e) or "").strip()
        did = _entry_drive_id(e)
        if not sid or not did:
            continue
        seen = by_sid.setdefault(sid, [])
        if did not in [r["drive_id"] for r in seen]:
            seen.append({"drive_id": did, "name": _entry_name(e)[:46], "sohieu": _entry_sohieu(e) or ""})
    return [{"source_id": sid, "rows": rows} for sid, rows in by_sid.items() if len(rows) > 1]


def _shared_source_fix_plan(entries: list) -> list:
    """PURE: cho mỗi nhóm shared_source_id (≥2 drive_id chung 1 source_id = FALSE-LINK) → chọn GIỮ bản điểm cao nhất
    (GDoc/NLM canonical), CLEAR nlm_source_id các bản còn lại (để re-push riêng). Advisory: verify nlm-content xem source
    THỰC SỰ thuộc bản nào trước khi ghi."""
    out = []
    for g in _shared_source_id_groups(entries):
        rows = []
        for r in g["rows"]:
            e = next((x for x in entries if _entry_drive_id(x) == r["drive_id"]), None)
            rows.append({"drive_id": r["drive_id"], "name": r.get("name", ""), "sohieu": r.get("sohieu", ""),
                         "score": _entry_score(e) if e else 0})
        rows.sort(key=lambda x: x["score"], reverse=True)
        keep, clear = rows[0], rows[1:]
        out.append({"source_id": g["source_id"], "keep": keep, "clear": clear,
                    # v1.29.4: ghi rỗng qua reg_bulk bị webapp BỎ QUA — xóa link phải đi reg_clear (per drive_id bản thua)
                    "clear_command": "tl shared-source-fix --apply --confirm yes  (reg_clear per-loser; hoặc tay: "
                                     "tl register --drive-id <loser> --nlm-source-id \"\" → tự route reg_clear)",
                    "verify": "ĐỌC `tl nlm-content " + g["source_id"] + "` xác minh source thuộc bản nào → GIỮ bản đó, re-push bản kia."})
    return out


def cmd_shared_source_fix(a) -> int:
    """FIXER cho shared_source_id FALSE-LINK (≥2 drive_id chung 1 nlm_source_id → xóa nguồn 1 gãy link kia). Kế hoạch:
    GIỮ link ở bản điểm cao, CLEAR link bản còn lại. DRY/report mặc định; --apply đi action `reg_clear` per-loser
    (v1.29.4 — reg_bulk giá-trị-rỗng bị webapp bỏ qua im lặng, gốc vụ 'links_cleared: 0').
    ⚠ verify `nlm-content` xem source THỰC thuộc bản nào trước khi apply (report-only nếu không chắc)."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:
        print(f"[tl] shared-source-fix: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    plan = _shared_source_fix_plan(entries)
    if getattr(a, "apply", False):
        if getattr(a, "confirm", "") != "yes":
            print(json.dumps({"ok": False, "error": "CONFIRM_YES_REQUIRED",
                              "why": "gỡ link NLM = destructive; verify nlm-content TRƯỚC. `--apply --confirm yes`."},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
        _ok_gate, _ = _apply_gate(a, write_cols="nlm_source_id")
        if not _ok_gate:
            return 2
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        g = _gas()
        run_id = _apply_journal_start("shared-source-fix", {"groups": len(plan)})
        # v1.29.4 (FIX log LIVE 'links_cleared: 0'): GHI GIÁ TRỊ RỖNG qua reg_bulk bị webapp BỎ QUA IM LẶNG ("empty
        # string KHÔNG ghi đè") → bản cũ báo verified/ok mà KHÔNG clear gì. XÓA field PHẢI đi action `reg_clear`
        # (keyed drive_id CỦA BẢN THUA — không key nlm_source_id vì sẽ clear CẢ 2 dòng). Per-loser + journal before
        # (undo = trả shared source_id cũ) + đếm cleared THẬT + LOUD khi hụt.
        cleared_n, fail_n = 0, 0
        for grp in plan:
            for c in grp["clear"]:
                vc = _journaled_reg_clear(run_id, g, c["drive_id"], "nlm_source_id,nlm_status,nlm_pushed_at",
                                          before={"nlm_source_id": grp.get("source_id") or "",
                                                  "nlm_status": c.get("nlm_status") or ""})
                if vc.get("verified"):
                    cleared_n += 1
                else:
                    fail_n += 1
                    print(f"  ⚠ reg_clear HỤT drive_id={c['drive_id'][:16]} ({vc.get('error') or (vc.get('resp') or {}).get('error')})",
                          file=sys.stderr, flush=True)
        _journal_append(run_id, {"t": "run_end", "ok": fail_n == 0, "counts": {"links_cleared": cleared_n, "fail": fail_n}})
        print(json.dumps({"ok": fail_n == 0, "groups": len(plan), "links_cleared": cleared_n, "clear_failed": fail_n,
                          "journal": run_id,
                          "note": "Đã gỡ link SAI qua reg_clear (undo: `tl undo <journal>` trả source_id cũ); re-push bản "
                                  "đã clear bằng `tl nlm-add`/`ingest-missing`."}, ensure_ascii=False, indent=2))
        return 0 if fail_n == 0 else 1
    print(json.dumps({"ok": True, "mode": "DRY (report-only)", "groups": len(plan), "plan": plan,
                      "note": "GIỮ bản điểm cao, CLEAR link bản kia. VERIFY `nlm-content <source_id>` TRƯỚC `--apply --confirm yes`."},
                     ensure_ascii=False, indent=2))
    return 0


def _source_rename_plan(entries: list, target: str, new_name: str = "", new_sohieu: str = "") -> dict:
    """PURE: kế hoạch đổi tên 1 nguồn VBQPPL — sửa registry.name (+sohieu qua reg_upsert) + tùy chọn đổi tên GDoc trên
    Drive (rename action). Gợi ý tên chuẩn từ standardize_name nếu không truyền --name. Cảnh báo VBHN thiếu năm/đổi sohieu."""
    tkey = norm_sohieu(target.replace("_", "-")) if _looks_like_sohieu_query(target) else ""
    e = next((x for x in entries if _entry_drive_id(x) == target or (tkey and _sohieu_key_entry(x) == tkey)), None)
    if not e:
        return {"ok": False, "error": "NOT_FOUND", "target": target}
    old_name = _entry_name(e)
    old_sohieu = _entry_sohieu(e) or _sohieu_key_entry(e)
    suggested = new_name.strip()
    already_standard = False
    if not suggested:
        # S14 (v1.33.44 — log 7A: gợi ý cũ ra 'TT_28_2023_TT-BYT' TỐI GIẢN — số hiệu lẫn vào tail underscore,
        # THIẾU chủ đề): (1) số hiệu = --sohieu mới > registry (normalize_number tự gạch-nối 28/2023/TT-BYT →
        # 28-2023-TT-BYT); (2) CHỦ ĐỀ ưu tiên title_vn/trich_yeu (_derive_subject_from_entries — CÓ DẤU, đã
        # backfill ~83% corpus, guard tên-file) cắt ≤10 từ, bỏ từ-loại đứng đầu ('Thông tư …' → '…' vì prefix
        # loại đã có); fallback tail tên cũ NHƯNG lọc token số-hiệu lọt vào (gốc ca 'TT_28_2023_TT-BYT').
        try:
            _num = (new_sohieu or old_sohieu or "").strip()
            _kind = _infer_loai(old_name, _num) or "VB"
            _subj = _derive_subject_from_entries([e]) or ""
            if _subj:
                for _kv in sorted(_LOAI_CANON_VALUES, key=len, reverse=True):   # bỏ từ-loại mở đầu trích yếu
                    if _strip_accents(_subj).lower().startswith(_strip_accents(_kv).lower() + " "):
                        _subj = _subj[len(_kv):].strip(" ,;:-")
                        break
                _subj = " ".join(_subj.split()[:10])
            if not _subj:
                _t = _name_tail_key(old_name)
                if _num:   # lọc cụm số-hiệu còn sót trong tail (tên phi-chuẩn kiểu 'thong-tu-28-2023-tt-byt-…')
                    _numtok = {t for t in re.split(r"[^a-z0-9]+", _strip_accents(_num).lower()) if t}
                    _t = " ".join(w for w in _t.split() if w not in _numtok)
                _subj = (_t[:1].upper() + _t[1:]) if _t else ""   # 'dan so' → 'Dan so' (đúng quy ước Dan_so)
            suggested = _imp("standardize_name").build_doc_name(_kind, _num, _subj)
        except Exception:
            suggested = old_name
        if _strip_accents(suggested).lower().replace("-", "_") == _strip_accents(old_name).lower().replace("-", "_"):
            already_standard = True    # gợi ý TRÙNG tên cũ → không cần đổi
    warns = []
    if not (new_sohieu or old_sohieu):
        warns.append("SOHIEU_MISSING_IN_SUGGESTION: registry chưa có số hiệu → tên gợi ý THIẾU cụm số hiệu; đọc header "
                     "(`tl header-verify --drive-id <id>`) rồi truyền --sohieu (đủ gạch-nối NN-YYYY-…, VBQPPL phải CÓ NĂM).")
    if already_standard and not new_sohieu:
        warns.append("ALREADY_STANDARD: tên hiện tại đã chuẩn — truyền --name nếu muốn đổi khác.")
    if _is_vbhn_entry(e) and not re.search(r"(?:19|20)\d{2}", suggested):
        warns.append("VBHN_NAME_MISSING_YEAR: tên VBHN nên có năm (số VBHN tái dùng theo năm).")
    if new_sohieu and norm_sohieu(new_sohieu) != _sohieu_key_entry(e):
        warns.append("SOHIEU_CHANGE: đổi số hiệu (khóa) — reg_upsert theo drive_id đổi trường sohieu; KIỂM collision "
                     "(số VBQPPL phải CÓ NĂM, tránh trùng số+năm với văn bản khác) TRƯỚC khi apply.")
    cmd = f'tl register --drive-id {_entry_drive_id(e)} --name "{suggested}"'
    if new_sohieu:
        cmd += f' --sohieu "{new_sohieu}"'
    return {"ok": True, "drive_id": _entry_drive_id(e), "old_name": old_name, "new_name": suggested,
            "already_standard": already_standard,
            "old_sohieu": old_sohieu, "new_sohieu": new_sohieu or None, "cat": _entry_cat(e),
            "reg_upsert_command": cmd,
            "drive_rename_command": f"rename GDoc {_entry_drive_id(e)} → '{suggested}' (gws `rename` action, khi --rename-drive)",
            "warnings": warns,
            "note": "SUGGESTION — verify header (`tl header-verify --drive-id <id>`) TRƯỚC khi ghi. Sidecar .docx/.pdf cùng base nên đổi tên theo."}


def cmd_source_rename(a) -> int:
    """Đổi TÊN (và tùy chọn số hiệu) 1 nguồn VBQPPL: sửa registry.name qua reg_upsert + tùy chọn đổi tên GDoc trên Drive
    (`--rename-drive`). Gợi ý tên chuẩn nếu bỏ trống --name. DRY mặc định; --apply ghi (LIVE Cowork). Verify header trước."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:
        print(f"[tl] source-rename: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    plan = _source_rename_plan(entries, (getattr(a, "target", "") or "").strip(),
                               getattr(a, "name", "") or "", getattr(a, "sohieu", "") or "")
    if not plan.get("ok"):
        print(json.dumps(plan, ensure_ascii=False, indent=2), file=sys.stderr); return 2
    if not getattr(a, "apply", False):
        print(json.dumps({"mode": "DRY", **plan}, ensure_ascii=False, indent=2)); return 0
    _ok_gate, _ = _apply_gate(a, write_cols=("name,sohieu" if plan.get("new_sohieu") else "name"))
    if not _ok_gate:
        return 2
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    g = _gas()
    run_id = _apply_journal_start("source-rename", {"drive_id": plan["drive_id"]})
    payload = {"drive_id": plan["drive_id"], "name": plan["new_name"]}
    _before = {"name": plan.get("old_name") or ""}
    if plan.get("new_sohieu"):
        payload["sohieu"] = plan["new_sohieu"]; _before["sohieu"] = plan.get("old_sohieu") or ""
    _vr = _journaled_reg_upsert(run_id, g, payload, before=_before)   # undo = trả name/sohieu cũ (chỉ registry, KHÔNG hoàn tên GDoc/NLM)
    reg = _vr.get("reg_upsert") or {"ok": _vr.get("verified")}
    drive_r = nlm_r = None
    if getattr(a, "rename_drive", False):
        try:
            drive_r = g.get("rename", fileId=plan["drive_id"], name=plan["new_name"])
        except Exception as e:  # noqa: BLE001
            drive_r = {"ok": False, "error": str(e)}
        # (MERGE) đổi tên CẢ nguồn NLM (nlm_cli.source_rename) — đồng bộ tên everywhere.
        _e = next((x for x in entries if _entry_drive_id(x) == plan["drive_id"]), None)
        _sid = _entry_nlm(_e) if _e else ""
        if _sid:
            _nb, _nberr = _resolve_nlm_notebook(None)
            try:
                nc = _imp("nlm_cli")
                nlm_r = nc.source_rename(_sid, plan["new_name"], _nb) if (not _nberr and nc.nlm_available()) else {"ok": False, "skip": _nberr or "nlm CLI N/A"}
            except Exception as e:  # noqa: BLE001
                nlm_r = {"ok": False, "error": str(e)}
    _journal_append(run_id, {"t": "run_end", "ok": bool(reg.get("ok")), "counts": {"renamed": 1}})
    _invalidate_manifest_cache()
    print(json.dumps({"ok": bool(reg.get("ok")), "reg_upsert": reg, "drive_rename": drive_r, "nlm_rename": nlm_r, "journal": run_id,
                      "renamed": f"{plan['old_name']} → {plan['new_name']}",
                      "note": "cache manifest đã xoá → `tl boot --refresh`. Undo TÊN registry: `tl undo <journal>` (KHÔNG hoàn tên GDoc/NLM). Sidecar cùng base đổi tên riêng nếu cần."},
                     ensure_ascii=False, indent=2))
    return 0 if reg.get("ok") else 2


def _source_delete_plan(entries: list, target: str) -> dict:
    """PURE: kế hoạch XÓA CỨNG 1 nguồn VBQPPL (bất khả nghịch): gỡ NLM + trash Drive + xóa dòng registry. GUARD
    shared_source_id (nguồn dùng chung → KHÔNG xóa NLM, gãy link kia). Nêu lựa chọn REVERSIBLE (source-update-corpus false)."""
    e = _source_find(entries, target)
    if not e:
        return {"ok": False, "error": "NOT_FOUND", "target": target}
    sid = _entry_nlm(e)
    shared = bool(sid) and sid in {g["source_id"] for g in _shared_source_id_groups(entries)}
    base = {"ok": True, "drive_id": _entry_drive_id(e), "name": _entry_name(e), "sohieu": _entry_sohieu(e) or "",
            "cat": _entry_cat(e), "nlm_source_id": sid or None, "shared_source_id": shared, "reversible": False}
    if shared:
        # (MERGE, an toàn — review đối kháng): nguồn NLM DÙNG CHUNG (FALSE-LINK) → CHẶN TOÀN BỘ (không xóa registry/Drive/NLM),
        # tránh để nguồn MỒ CÔI + sibling gãy link. Phải resolve FALSE-LINK trước (bản THẬT sở hữu nguồn), rồi mới xóa.
        base.update({"blocked_shared": True, "error": "SHARED_SOURCE_MUST_FIX_FIRST", "actions": ["⛔ CHẶN — KHÔNG xóa gì"],
                     "note": "⛔ Nguồn NLM DÙNG CHUNG với văn bản KHÁC (shared_source_id/FALSE-LINK). KHÔNG xóa (xóa registry/Drive "
                             "để nguồn NLM MỒ CÔI + sibling gãy). SỬA TRƯỚC: `tl shared-source-fix` (xác định bản THẬT sở hữu "
                             "nguồn) → rồi mới `source-delete`."})
        return base
    base.update({"actions": [("nlm source delete " + sid) if sid else "SKIP nlm (không có nguồn)",
                             "trash Drive file + xóa dòng registry (reg_delete force)"],
                 "note": "XÓA CỨNG bất khả nghịch. Muốn REVERSIBLE (bỏ khỏi corpus, GIỮ registry+Drive): "
                         "`tl source-update-corpus <target> false`. Cần `--apply --confirm yes`."})
    return base


def cmd_source_delete(a) -> int:
    """(MERGE) Xóa CỨNG 1 nguồn VBQPPL: gỡ NLM (GUARD shared_source_id) + trash Drive + xóa dòng registry. Bất khả nghịch
    → DRY mặc định, `--apply --confirm yes`. Cân nhắc `source-update-corpus false` (reversible) trước khi xóa cứng."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:
        print(f"[tl] source-delete: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    plan = _source_delete_plan(entries, (getattr(a, "target", "") or "").strip())
    if not plan.get("ok"):
        print(json.dumps(plan, ensure_ascii=False, indent=2), file=sys.stderr); return 2
    if plan.get("blocked_shared"):    # CHẶN TOÀN BỘ khi shared (kể cả --apply) — resolve FALSE-LINK trước
        print(json.dumps({"ok": False, **plan}, ensure_ascii=False, indent=2), file=sys.stderr); return 2
    if not (getattr(a, "apply", False) and getattr(a, "confirm", "").strip().lower() == "yes"):
        print(json.dumps({"mode": "DRY", "confirm_required": "--apply --confirm yes", **plan}, ensure_ascii=False, indent=2))
        return 0
    _ok_gate, _ = _apply_gate(a)   # (Pha 1+) precheck (chống clobber/mispoint) TRƯỚC khi xóa cứng
    if not _ok_gate:
        return 2
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    g = _gas()
    run_id = _apply_journal_start("source-delete", {"drive_id": plan["drive_id"], "irreversible": True})
    # FORENSIC: ghi TOÀN BỘ dòng TRƯỚC khi xóa cứng (undo TỰ ĐỘNG KHÔNG được — Drive trash + NLM delete; snapshot để tra cứu /
    # khôi phục TAY). op='reg_delete' KHÔNG nằm trong undo/resume-ops → không bị auto-đảo.
    _e = next((x for x in entries if _entry_drive_id(x) == plan["drive_id"]), {}) or {}
    _snap = {k: _e.get(k) for k in ("drive_id", "name", "sohieu", "so_hieu", "cat", "loai", "corpus", "goc", "sua_doi",
                                    "nlm_source_id", "nlm_notebook_id", "nlm_status", "hieuluc", "md5") if _e.get(k) is not None}
    _journal_append(run_id, {"t": "intent", "op": "reg_delete", "key": plan["drive_id"], "irreversible": True, "snapshot": _snap})
    nlm_r = None
    sid = plan.get("nlm_source_id")
    if sid:    # tới đây chắc chắn KHÔNG shared (đã chặn ở trên)
        _nb, _nberr = _resolve_nlm_notebook(None)
        try:
            nc = _imp("nlm_cli")
            nlm_r = nc.source_delete(sid) if (not _nberr and nc.nlm_available()) else {"ok": False, "skip": _nberr or "nlm CLI N/A"}
        except Exception as e:  # noqa: BLE001
            nlm_r = {"ok": False, "error": str(e)}
    # v1.33.40 (MERGE bundle-15 'complete'): source-delete TRƯỚC KIA 2 lỗi WRITE-path: (a) docstring nói 'trash
    # Drive' NHƯNG code KHÔNG trash (chỉ nlm-delete + reg_delete) → file rác kẹt Drive; (b) reg_delete gọi SAI
    # shape `g.get(fileId=,force=)` — GAS reg_delete là POST + drive_ids[] + confirm=yes (fileId/force bị bỏ qua
    # → dòng registry KHÔNG xóa, ok giả). Sửa cả 2 theo pattern ĐÃ CHỨNG MINH (cmd_reg_delete + 3 call trash khác
    # + API_CONTRACT). require_removed='no': hard-delete có chủ đích sau --apply --confirm yes + _apply_gate.
    try:
        drive_trash = g.get("trash", fileId=plan["drive_id"], confirm="yes")   # doTrash_ — reversible qua 'restore'
    except Exception as e:  # noqa: BLE001
        drive_trash = {"ok": False, "error": str(e)}
    _journal_append(run_id, {"t": "commit", "op": "drive_trash", "key": plan["drive_id"], "ok": bool(drive_trash.get("ok"))})
    reg = g.post("reg_delete", drive_ids=json.dumps([plan["drive_id"]]), confirm="yes", require_removed="no")
    _journal_append(run_id, {"t": "commit", "op": "reg_delete", "key": plan["drive_id"], "ok": bool(reg.get("ok"))})
    _journal_append(run_id, {"t": "run_end", "ok": bool(reg.get("ok")), "counts": {"deleted": 1}})
    _invalidate_manifest_cache()
    print(json.dumps({"ok": bool(reg.get("ok")), "deleted": plan["name"], "nlm_delete": nlm_r,
                      "drive_trash": drive_trash, "reg_delete": reg, "journal": run_id,
                      "note": "Drive→trash (restore được), NLM source deleted, dòng registry xoá. cache manifest đã xoá "
                              "→ `tl boot --refresh`. ⚠ BẤT KHẢ NGHỊCH (trừ Drive restore) — snapshot dòng đã lưu journal."},
                     ensure_ascii=False, indent=2))
    return 0 if reg.get("ok") else 2


def _source_update_corpus_plan(entries: list, target: str, is_corpus: bool) -> dict:
    """PURE: kế hoạch bật/tắt cờ corpus 1 nguồn. corpus=false = 'bỏ ra khỏi corpus' (reversible ở registry) + gỡ nguồn NLM
    (GUARD shared_source_id). corpus=true = đưa lại vào corpus (cần nlm-add/ingest sau nếu chưa có nguồn)."""
    e = _source_find(entries, target)
    if not e:
        return {"ok": False, "error": "NOT_FOUND", "target": target}
    sid = _entry_nlm(e)
    shared = bool(sid) and sid in {g["source_id"] for g in _shared_source_id_groups(entries)}
    plan = {"ok": True, "drive_id": _entry_drive_id(e), "name": _entry_name(e), "sohieu": _entry_sohieu(e) or "",
            "set_corpus": is_corpus, "nlm_source_id": sid or None, "shared_source_id": shared}
    if not is_corpus:
        if shared:
            # (MERGE, an toàn — review) 'bỏ ra khỏi corpus' khi nguồn DÙNG CHUNG (FALSE-LINK) → CHẶN (tránh nhầm status
            # trên nguồn của sibling). Resolve FALSE-LINK trước.
            plan.update({"blocked_shared": True, "will_remove_nlm": False, "error": "SHARED_SOURCE_MUST_FIX_FIRST",
                         "note": "⛔ Nguồn NLM DÙNG CHUNG (shared_source_id/FALSE-LINK) — KHÔNG 'bỏ ra khỏi corpus' khi còn "
                                 "FALSE-LINK (nhầm status trên nguồn của sibling). SỬA `tl shared-source-fix` trước."})
            return plan
        plan["will_remove_nlm"] = bool(sid)
        plan["note"] = ("BỎ RA KHỎI CORPUS: reg_upsert corpus=false (reversible) + gỡ nguồn NLM. "
                        "Đưa lại: `tl source-update-corpus <t> true` rồi nlm-add/ingest.")
    else:
        plan["needs_ingest"] = not bool(sid)
        plan["note"] = "ĐƯA VÀO CORPUS: reg_upsert corpus=true." + (" Chưa có nguồn NLM → chạy `tl nlm-add`/`ingest-missing` sau." if not sid else "")
    return plan


def cmd_source_update_corpus(a) -> int:
    """(MERGE) Bật/tắt cờ corpus 1 nguồn VBQPPL. `false` = BỎ RA KHỎI CORPUS (reg_upsert corpus=false reversible + gỡ nguồn
    NLM, GUARD shared_source_id). `true` = đưa vào lại. DRY mặc định; `--apply --confirm yes` ghi."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    status_str = (getattr(a, "status", "") or "").strip().lower()
    if status_str not in ("true", "false", "yes", "no", "1", "0"):
        print("[tl] source-update-corpus: cần <target> và <status> (true/false).", file=sys.stderr); return 2
    is_corpus = status_str in ("true", "yes", "1")
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:
        print(f"[tl] source-update-corpus: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    plan = _source_update_corpus_plan(entries, (getattr(a, "target", "") or "").strip(), is_corpus)
    if not plan.get("ok"):
        print(json.dumps(plan, ensure_ascii=False, indent=2), file=sys.stderr); return 2
    if plan.get("blocked_shared"):    # CHẶN TOÀN BỘ khi shared+false — resolve FALSE-LINK trước
        print(json.dumps({"ok": False, **plan}, ensure_ascii=False, indent=2), file=sys.stderr); return 2
    if not (getattr(a, "apply", False) and getattr(a, "confirm", "").strip().lower() == "yes"):
        print(json.dumps({"mode": "DRY", "confirm_required": "--apply --confirm yes", **plan}, ensure_ascii=False, indent=2))
        return 0
    _ok_gate, _ = _apply_gate(a, write_cols="corpus,nlm_status")   # (Pha 1+) precheck + journal + verified upsert
    if not _ok_gate:
        return 2
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    g = _gas()
    run_id = _apply_journal_start("source-update-corpus", {"corpus": is_corpus, "drive_id": plan["drive_id"]})
    payload = {"drive_id": plan["drive_id"], "corpus": "true" if is_corpus else "false"}
    if not is_corpus:
        payload["nlm_status"] = "removed_by_user"
    _before = {"corpus": "false" if is_corpus else "true"}   # undo = trả cờ corpus ngược lại
    _vu = _journaled_reg_upsert(run_id, g, payload, before=_before)
    reg = _vu.get("reg_upsert") or {"ok": _vu.get("verified")}
    nlm_r = None
    ref_clear = None
    if (not is_corpus) and plan.get("will_remove_nlm"):
        _nb, _nberr = _resolve_nlm_notebook(None)
        try:
            nc = _imp("nlm_cli")
            nlm_r = nc.source_delete(plan["nlm_source_id"]) if (not _nberr and nc.nlm_available()) else {"ok": False, "skip": _nberr or "nlm CLI N/A"}
        except Exception as e:  # noqa: BLE001
            nlm_r = {"ok": False, "error": str(e)}
        # N4 (v1.33.41 — log rà VBHN-first: 5 dòng đã gỡ [100-2015, 97-2015, 87-2015, 57-2014, 62-2025] vẫn giữ
        # nlm_source_id cũ dù corpus=false + source NLM ĐÃ XÓA → nhiễu reconcile về sau): sau khi NLM delete
        # THÀNH CÔNG, clear luôn nlm_source_id/nlm_notebook_id qua reg_clear (2 cột đều ∈ _REG_CLEARABLE_COLS;
        # KHÔNG reg_bulk giá-trị-rỗng — webapp bỏ qua). Delete FAIL → GIỮ ref để thử lại, không mất dấu.
        if nlm_r and nlm_r.get("ok"):
            _rc_before = {"nlm_source_id": plan.get("nlm_source_id") or "",
                          "nlm_notebook_id": str(next((x.get("nlm_notebook_id") for x in entries
                                                       if _entry_drive_id(x) == plan["drive_id"]), "") or "")}
            ref_clear = _journaled_reg_clear(run_id, g, plan["drive_id"], "nlm_source_id,nlm_notebook_id",
                                             before=_rc_before)
    _journal_append(run_id, {"t": "run_end", "ok": bool(reg.get("ok")), "counts": {"corpus": is_corpus}})
    _invalidate_manifest_cache()
    print(json.dumps({"ok": bool(reg.get("ok")), "corpus": is_corpus, "reg_upsert": reg, "nlm_delete": nlm_r,
                      **({"nlm_ref_cleared": bool(ref_clear.get("verified"))} if ref_clear is not None else {}),
                      "journal": run_id,
                      "nlm_blocked_shared": plan.get("nlm_shared_blocked", False),
                      "note": "cache manifest đã xoá → `tl boot --refresh`. Undo cờ corpus: `tl undo <journal>`." + (" Đưa vào corpus: nhớ nlm-add/ingest." if (is_corpus and plan.get("needs_ingest")) else "")},
                     ensure_ascii=False, indent=2))
    return 0 if reg.get("ok") else 2
