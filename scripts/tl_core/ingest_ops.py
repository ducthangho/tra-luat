# -*- coding: utf-8 -*-
"""tl_core.ingest_ops — I5 (v1.34.8): tách NGUYÊN VĂN cụm ingest/registry-write từ scripts/tl.py
(ingest-local/profile-ingest/ingest/ingest-analyze/ingest-route/ingest-missing/register/recat/
source-rename+delete+update-corpus/shared-source-fix + classification/verify-gate/chunk/mime/checkpoint/
plan-helper riêng-cụm). WRITE-INFRA ĐA-MODULE GIỮ Ở TL: _journaled_reg_write/_apply_gate/
_verified_reg_upsert/_reg_before_from_manifest. Hành vi khoá bởi r75a wiring + r51/r53/r54/r73a hiện có."""
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
    """REBASE __globals__ từng hàm đã chuyển về namespace SỐNG của tl (khuôn I1-I4)."""
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



def cmd_ingest(a) -> int:
    """QT-2 gate → (--apply) copy_convert + standardize + organize. Mặc định DRY (an toàn)."""
    pg = _need_base('preingest_gate')
    # 1) QT-2 nếu là sửa đổi/VBHN/nghi bị thay
    if a.sohieu and (a.amendment or a.vbhn or a.check):
        targets = [t for t in re.split(r"[;,]", a.targets or "") if t.strip()]
        gate = pg.decide(_gas().get("vb_status", q=a.sohieu),
                         [dict(_gas().get("vb_status", q=t), sohieu=t) for t in targets],
                         is_amendment=a.amendment or pg.is_amendment_name(a.sohieu),
                         is_vbhn=a.vbhn or pg.is_vbhn_name(a.sohieu))
        print(f"[QT-2] {gate['decision']} ({gate['reason']}): {gate['surface']}")
        for act in gate["actions"]:
            print(f"   - {act}")
        if gate["decision"] == "SKIP":
            print("[tl] DỪNG: cổng QT-2 = SKIP (ưu tiên VBHN/đã có). Không nạp.")
            return 0
        if gate["decision"] == "REVIEW":
            print("[tl] REVIEW: cần HỎI người dùng quyết trước khi nạp.")
            if not a.apply:
                return 2
    # 2) kế hoạch / thực thi
    if not a.apply:
        print(f"[tl] DRY. Kế hoạch nạp fileId={a.fileId}:")
        print(f"   1) copy_convert fileId={a.fileId} cat={a.cat or '(?)'} → GDoc (khóa trả: fileId)")
        print(f"   2) standardize_name --type {a.loai or '?'} --number {a.sohieu or '?'} --name {a.ten or '?'}")
        print(f"   3) organize: rename+move(cat={a.cat or '?'})+stamp+register (1 RTT)")
        print(f"   4) verify: list cat={a.cat or '?'}  (ĐỪNG tin response của move)")
        print(f"   5) NLM: source_add(drive,doc, fileId) qua MCP + map_set (Claude làm, KHÔNG webapp)")
        print("   → thêm --apply để chạy bước 1+3.")
        return 0
    if not a.ten and not (HERE / "standardize_name.py").exists():
        print("[tl] overlay thiếu standardize_name.py; hãy truyền --ten tên chuẩn hoặc cài base skill đầy đủ trước khi --apply.", file=sys.stderr)
        return 2
    g = _gas()
    cv = g.get("copy_convert", fileId=a.fileId, **({"cat": a.cat} if a.cat else {}),
               **({"name": a.ten} if a.ten else {}))
    if not cv.get("ok"):
        print(f"[tl] copy_convert lỗi: {cv.get('error')}", file=sys.stderr)
        return 1
    gdoc = cv["fileId"]
    print(f"[tl] copy_convert ok → GDoc {gdoc}")
    org = g.post("organize", fileId=gdoc, register="true",
                 **({"cat": a.cat} if a.cat else {}),
                 **({"name": a.ten} if a.ten else {}),
                 **({"sohieu": a.sohieu} if a.sohieu else {}),
                 **({"loai": a.loai} if a.loai else {}))
    print(json.dumps(org, ensure_ascii=False))
    print(f"[tl] organize xong. Bước NLM (source_add + map_set) làm qua MCP, KHÔNG webapp.")
    return 0 if org.get("ok") else 1


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


def cmd_register(a) -> int:
    g = _gas()
    if getattr(a, "clear_cols", None):
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
        _verified_all, _rbs = True, []
        for _kf, _batch in (("drive_id", _b_drive), ("nlm_source_id", _b_src)):
            if not _batch:
                continue
            v = _journaled_reg_write(run_id, g, _batch, _cols_str, key_field=_kf,
                                     before_by_key=_reg_before_from_manifest(_batch, _cols_list, _kf))
            rb = v.get("reg_bulk") or {}
            _verified_all = _verified_all and bool(v.get("verified"))
            _rbs.append({**rb, "key_field": _kf, "verified": bool(v.get("verified")),
                         **({"error": v.get("error")} if v.get("error") else {})})
        print(json.dumps({"ok": _verified_all, "batches": _rbs, "journal": run_id}, ensure_ascii=False))
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
    if _fields:
        _before = (_reg_before_from_manifest([payload], _fields) or {}).get(str(a.drive_id))
        v = _journaled_reg_upsert(run_id, g, payload, before=_before)
        r = v.get("reg_upsert") or {}
    _clr = None
    if _clear_cols:
        _cbefore = (_reg_before_from_manifest([{"drive_id": a.drive_id}], _clear_cols) or {}).get(str(a.drive_id))
        _clr = _journaled_reg_clear(run_id, g, a.drive_id, ",".join(_clear_cols), before=_cbefore)
    _all_ok = bool(v.get("verified")) and (bool(_clr.get("verified")) if _clr is not None else True)
    print(json.dumps({**r, "verified": _all_ok, "journal": run_id,
                      **({"cleared_cols": _clear_cols, "cleared": _clr.get("cleared"),
                          **({"clear_error": _clr.get("error") or (_clr.get("resp") or {}).get("error")}
                             if not _clr.get("verified") else {})} if _clr is not None else {}),
                      **({"error": v.get("error")} if v.get("error") else {})}, ensure_ascii=False))
    return 0 if _all_ok else 1


def cmd_ingest_analyze(a) -> int:
    """(MERGE Claude) ĐỌC HEADER file → ĐỀ XUẤT tên chuẩn + cat + sohieu/loai + cảnh báo + lệnh `ingest-local --auto-plan
    --apply` điền sẵn (DRY, read-only). Dùng CHUNG analyzer `_vb_ingest_auto_plan`. .docx/.pdf: Claude đọc→.txt→--text-file."""
    f = getattr(a, "file", None)
    tf = getattr(a, "text_file", None)
    if not ((f and Path(f).exists()) or (tf and Path(tf).exists())):
        print(json.dumps({"ok": False, "error": "NEED_FILE_OR_TEXT",
                          "note": "--file <gốc> (+/hoặc) --text-file <txt Claude trích từ .docx/.pdf>."},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    plan = _vb_ingest_auto_plan(f or tf, text_file=tf, cat=_norm_cat(getattr(a, "cat", "") or ""),
                                source_quality=getattr(a, "source_quality", "auto"),
                                ocr_verified=getattr(a, "ocr_verified", False))
    cmd = f'tl ingest-local --file "{f or tf}" --auto-plan'
    if tf:
        cmd += f' --text-file "{tf}"'
    if plan.get("cat"):
        cmd += f" --cat {plan['cat']}"
    cmd += " --apply"
    plan["ingest_command"] = cmd
    plan["hint"] = "SUGGESTION — verify sohieu/cat/tên (`cat-verify`/`header-verify`) TRƯỚC khi `--apply`."
    print(json.dumps({"ok": plan.get("ok", True), **plan}, ensure_ascii=False, indent=2))
    return 0


def cmd_ingest_route(a) -> int:
    """WS3 (3.bis): cây quyết định ĐỊNH HƯỚNG cho file người dùng nhập. ADVISORY — không ghi gì."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    q = a.query
    kind = "vbqppl" if (_looks_like_sohieu_query(q) or getattr(a, "vbqppl", False)) else ("thuong" if getattr(a, "thuong", False) else "unknown")
    steps, route = [], ""
    if kind == "thuong":
        route = "PROFILE_OWN"; steps = ["Văn bản thường → profile dự án (row_kind=own, corpus=false). DỪNG."]
    else:
        try:
            entries = _manifest_entries(refresh=getattr(a, "refresh", False))
        except Exception as e:
            print(f"[tl] ingest-route: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
        hits = resolve_identity(q, entries, max_hits=4)
        exact = [h for h in hits if "sohieu" in h[2]]
        if exact:
            route = "ASK_USE_EXISTING"
            steps = ["VBQPPL đã CÓ canonical trong corpus.",
                     "HỎI: dùng bản sẵn có? Có → không nạp mới; cần ở notebook dự án thì thêm dòng ref (nlm_notebook_id).",
                     "Không (bản mới/chính thức hơn) → `tl vb_status`/`vbhn-verify --official-required` → thay thế + quarantine bản cũ (VBHN-first)."]
        elif hits:
            route = "REVIEW_NEARMATCH"
            steps = ["Có ứng viên gần (khớp tên/alias) nhưng KHÁC số hiệu — verify số+năm+loại+dòng đầu trước khi quyết.",
                     "Nếu thực sự là văn bản KHÁC → coi như CHƯA CÓ (xem nhánh dưới)."]
        else:
            route = "ASK_ADD_TO_VBQPPL"
            steps = ["VBQPPL CHƯA CÓ. HỎI: bổ sung vào corpus VBQPPL?",
                     "Có → định tuyến vào shard còn chỗ (`tl nlm-get` đếm vật lý, margin 5); đầy hết → HỎI tạo shard mới (notebook_create qua MCP, cần xác nhận).",
                     "Không → giữ ở profile dự án (own, corpus=false)."]
    out = {"ok": True, "query": q, "classified": kind, "route": route, "decision_tree": steps,
           "note": "ADVISORY: mọi ghi/source_add/tạo notebook/quarantine PHẢI qua xác nhận người dùng."}
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"== ingest-route · {q} · class={kind} · ROUTE={route} ==")
        for s in steps:
            print("  → " + s)
    return 0


def _ingest_missing_select(entries: list, cat: str | None = None, only_ids: set | None = None) -> list:
    """PURE (test offline): chọn văn bản corpus CHƯA trên NLM cần nạp. IDEMPOTENT — bỏ bản đã on NLM live. Yêu cầu
    drive_id, KHÔNG quarantine. Lọc theo cat (2 số đầu) / chỉ drive_id ∈ only_ids nếu truyền."""
    cc = re.sub(r"\D", "", str(cat))[:2] if cat else ""
    out = []
    for e in entries or []:
        if str(e.get("corpus") or "").lower() != "true":
            continue
        if _entry_on_nlm_live(e):                 # đã trên NLM → bỏ (idempotent, chạy lại an toàn)
            continue
        did = _entry_drive_id(e)
        if not did or _entry_quarantined(e):
            continue
        if cc and re.sub(r"\D", "", str(_entry_cat(e)))[:2] != cc:
            continue
        if only_ids is not None and did not in only_ids:
            continue
        out.append(e)
    return out


def _ingest_missing_partition(targets: list) -> tuple[list, list]:
    """PURE (S12): tách target CÓ số hiệu (nạp được) khỏi target sohieu RỖNG. sohieu='' gần như luôn là dòng registry
    RÁC/chưa chuẩn hoá (vd '80-nd-cp.signed.pdf') → KHÔNG auto-push lên NLM (skip + cảnh báo, buộc chuẩn hoá tay trước)."""
    valid, no_sohieu = [], []
    for e in targets:
        (valid if (_entry_sohieu(e) or "").strip() else no_sohieu).append(e)
    return valid, no_sohieu


def _ingest_dedup_title_key(x) -> str:
    """PURE: khóa so TITLE cho dedup-live — strip accents + lower + gộp space/`_`/`-`. Title nguồn NLM do CHÍNH tool đặt
    khi add (= _entry_name[:120]) → exact-title là định danh MẠNH, né bất-đối-xứng sohieu (vd registry đã year-fix
    `67-2025-VBHN-VPQH` nhưng title parse ra `67-VBHN-VPQH` → tier-sohieu MISS → từng đẩy trùng VBHN_67 3×)."""
    return re.sub(r"[\s_\-]+", " ", _strip_accents(str(x or "")).lower()).strip()


def _ingest_missing_dedup_live(targets: list, live_sources: list) -> tuple[list, list, int]:
    """PURE (S13 idempotency — chống trùng): đối chiếu target với nguồn LIVE THẬT trên notebook đích. 3 TẦNG khớp:
    (1) Drive fileId (`_nlm_source_drive_id`); (2) FALLBACK số hiệu DUY NHẤT (chống VBHN reuse false-link);
    (3) v1.29.1: EXACT-TITLE chuẩn hoá DUY NHẤT (title do tool đặt = _entry_name[:120] — bắt ca sohieu bất-đối-xứng
    năm/format khiến tầng 2 miss, gốc vụ VBHN_67 trùng 3×). Trả (to_add, already_live, unresolved_live):
    already_live=[(entry, source_id)] → LINK reconcile KHÔNG tạo trùng; unresolved_live=số nguồn LIVE không trích được
    cả drive_id lẫn sohieu (dedup có thể SÓT → cảnh báo)."""
    live_by_drive: dict[str, dict] = {}
    live_by_sohieu: dict[str, list] = {}
    live_by_title: dict[str, list] = {}
    unresolved = 0
    for s in live_sources or []:
        d = _nlm_source_drive_id(s)
        shk = _sohieu_key_entry({"name": s.get("title") or "", "so_hieu": s.get("sohieu") or s.get("so_hieu") or ""})
        tk = _ingest_dedup_title_key(s.get("title"))
        if d:
            live_by_drive.setdefault(d, s)
        if shk:
            live_by_sohieu.setdefault(shk, []).append(s)
        if tk:
            live_by_title.setdefault(tk, []).append(s)
        if not d and not shk:
            unresolved += 1
    to_add, already_live = [], []
    for e in targets:
        s = live_by_drive.get(_entry_drive_id(e))
        if s is None:
            shk = _sohieu_key_entry(e)
            cands = (live_by_sohieu.get(shk) or []) if shk else []
            s = cands[0] if len(cands) == 1 else None   # CHỈ khớp sohieu khi DUY NHẤT (chống false-link số hiệu tái dùng)
        if s is None:
            tk = _ingest_dedup_title_key(_entry_name(e)[:120])   # cùng phép cắt [:120] như lúc add
            tc = (live_by_title.get(tk) or []) if tk else []
            s = tc[0] if len(tc) == 1 else None          # tầng 3: exact-title DUY NHẤT
        if s and s.get("id"):
            already_live.append((e, str(s.get("id"))))
        else:
            to_add.append(e)
    return to_add, already_live, unresolved


def _ingest_ckpt_load(ckpt) -> dict:
    """Đọc checkpoint {drive_id: source_id}. CHỈ giữ entry CÓ source_id THẬT — format list cũ (chỉ drive_id, không source_id)
    hoặc None bị BỎ HẲN: entry không source_id vô giá trị idempotency (không link được) VÀ có thể là 'đã thử nhưng FAIL'
    (chưa hề push) → nếu skip mù sẽ KHÔNG BAO GIỜ nạp lại (BUG review#1). Bỏ đi → để live-dedup/source_add xử lại đúng."""
    try:
        raw = json.loads(ckpt.read_text(encoding="utf-8")).get("done", {}) if ckpt.exists() else {}
    except Exception:
        return {}
    return {str(k): v for k, v in raw.items() if v} if isinstance(raw, dict) else {}


def _ingest_ckpt_load_full(ckpt) -> dict:
    """v1.29.1 (WAL-hoá ingest-missing, xử log LIVE 2026-07-02): đọc checkpoint ĐẦY ĐỦ 4 khóa —
      done    {drive_id: source_id}  đã add OK (lọc như _ingest_ckpt_load: chỉ source_id thật);
      pending {drive_id: title}      ghi TRƯỚC source_add → client-timeout GIỮA add (subprocess wait tới 630s!)
                                     run sau BẮT BUỘC xác minh FRESH trước khi add lại (gốc vụ trùng VBHN_67 3×);
      linked  {drive_id: source_id}  reg_link ĐÃ verified → skip relink lặp khi GAS cache 600s còn che nlm_source_id
                                     (gốc vụ hàng-đợi-relink 1→8; --relink để ép);
      fails   {drive_id: n}          đếm FAIL push liên tiếp → n≥3 SKIP + LOUD (đỡ đốt batch cho bản thô hỏng; --retry-failed để ép).
    Backward-compat: file cũ chỉ có done → 3 khóa kia {}."""
    out = {"done": {}, "pending": {}, "linked": {}, "fails": {}}
    try:
        raw = json.loads(ckpt.read_text(encoding="utf-8")) if ckpt.exists() else {}
    except Exception:
        return out
    if not isinstance(raw, dict):
        return out
    d = raw.get("done")
    if isinstance(d, dict):
        out["done"] = {str(k): v for k, v in d.items() if v}
    for k in ("pending", "linked", "fails"):
        v = raw.get(k)
        if isinstance(v, dict):
            out[k] = {str(a): b for a, b in v.items()}
    return out


def cmd_ingest_missing(a) -> int:
    """Nạp HÀNG LOẠT văn bản corpus CHƯA trên NLM (backlog) → source_add + ghi registry PER-ITEM. IDEMPOTENT nhiều lớp,
    DRY MẶC ĐỊNH. Định tuyến THEO CHỖ TRỐNG (base→overflow shard SẴN CÓ) — BẤT BIẾN: KHÔNG BAO GIỜ tạo notebook mới.
    S12: skip+cảnh báo dòng sohieu='' (rác chưa chuẩn hoá); in mốc snapshot manifest (freshness). S13: TRƯỚC source_add
    ĐỐI CHIẾU nguồn LIVE trên notebook (drive_id) → đã có thì LINK (reconcile) KHÔNG tạo trùng; checkpoint source_id NGAY
    sau add; stream tiến độ per-item ra stderr (biết dừng ở đâu nếu timeout).
    v1.29.1 (xử log LIVE 2026-07-02): WAL-hoá ckpt 4 khóa {done,pending,linked,fails} — (a) `pending` ghi TRƯỚC
    source_add → run sau FRESH-verify (skip_freshness=False) trước khi add lại (chống trùng VBHN_67 3×); (b) dedup-live
    thêm tầng 3 EXACT-TITLE duy nhất (né bất-đối-xứng sohieu year-fix); (c) `linked` = reg_link đã verified → SKIP relink
    lặp khi GAS cache 600s che (--relink ép); (d) `fails` ≥3 → SKIP mục fail dai (--retry-failed ép)."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    _apply_ing = getattr(a, "apply", False)
    if _apply_ing:   # HEARTBEAT khởi động (log: startup ~43s che mất bằng chứng → tưởng treo). In NGAY, flush.
        print("[tl] ingest-missing --apply: KHỞI ĐỘNG (refresh manifest + đếm slot LIVE 2 notebook + dedup LIVE — Cowork ~vài chục giây, ĐỪNG kill)…", file=sys.stderr, flush=True)
    # refresh CÓ ĐIỀU KIỆN (Pha 1, vá log timeout): --apply chỉ FORCE khi cache CŨ (>300s); cache vừa refresh → dùng lại
    # (giảm overhead startup). Vẫn bound staleness (GAS cache ~600s server-side cảnh báo snapshot_ts bên dưới).
    _cache_age = _manifest_cache_age_seconds()
    _force_refresh = getattr(a, "refresh", False) or (_apply_ing and (_cache_age is None or _cache_age > 300))
    try:
        man = _load_manifest_full(refresh=_force_refresh)
        if man.get("ok") is False:
            raise RuntimeError(man.get("error") or "manifest lỗi")
        entries = man.get("entries") or man.get("files") or man.get("rows") or []
    except Exception as e:  # noqa: BLE001
        print(f"[tl] ingest-missing: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    snapshot_ts = str(man.get("generatedAt") or man.get("generated_at") or "?")
    if _apply_ing:
        print(f"[tl]   ✓ manifest {len(entries)} dòng ({'refresh' if _force_refresh else f'cache {int(_cache_age or 0)}s'}) — tiếp: đếm slot LIVE…", file=sys.stderr, flush=True)
    backlog = _ingest_missing_select(entries, cat=getattr(a, "cat", None))
    lim = getattr(a, "limit", None) or 25
    picked = backlog[:lim]
    valid, no_sohieu = _ingest_missing_partition(picked)
    allow_no_sohieu = getattr(a, "allow_no_sohieu", False)
    targets = picked if allow_no_sohieu else valid    # mặc định BỎ dòng sohieu='' khỏi nạp (chỉ cảnh báo)
    base_nb = os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK
    overflow_shard = (os.environ.get("TL_OVERFLOW_NOTEBOOK_ID") or "").strip()
    if not overflow_shard or "-" not in overflow_shard:
        overflow_shard = _discover_overflow_from_registry(entries, base_nb)
    _skip_note = ([{"drive_id": _entry_drive_id(e), "name": _entry_name(e)[:60]} for e in no_sohieu]) if not allow_no_sohieu else []
    if not getattr(a, "apply", False):
        out = {"ok": True, "gate": "ingest-missing", "mode": "DRY", "manifest_snapshot": snapshot_ts,
               "backlog": len(backlog), "to_ingest": len(targets), "skipped_no_sohieu": len(_skip_note),
               "base_notebook": base_nb, "overflow_shard": overflow_shard or None,
               "targets": [{"drive_id": _entry_drive_id(e), "sohieu": _entry_sohieu(e), "name": _entry_name(e)[:60]} for e in targets],
               "skipped_no_sohieu_rows": _skip_note[:20],
               "note": "DRY — --apply: source_add + ghi registry per-item + ĐỐI CHIẾU nguồn LIVE (chống trùng). sohieu='' BỎ QUA "
                       "(dùng --allow-no-sohieu nếu THỰC SỰ muốn nạp). ⚠ manifest_snapshot có thể LỆCH registry live (GAS cache ~600s) "
                       "— sửa corpus xong nên đợi/`manifest`+`boot --refresh` rồi kiểm lại targets."}
        if getattr(a, "json", False):
            print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
        else:
            print(f"== ingest-missing DRY · snapshot={snapshot_ts} · backlog={len(backlog)} · nạp {len(targets)} (limit {lim}) · "
                  f"skip sohieu='' {len(_skip_note)} · base={base_nb[:12]} overflow={overflow_shard or '(chưa có)'} ==")
            for e in targets:
                print(f"  + {(_entry_sohieu(e) or '(?)'):18s} {_entry_name(e)[:54]}  [{_entry_drive_id(e)[:14]}]")
            for r in _skip_note[:10]:
                print(f"  ⚠ SKIP sohieu='' : {r['name'][:54]}  [{r['drive_id'][:14]}] — chuẩn hoá số hiệu TRƯỚC (rác?)")
            print("  → --apply để nạp (per-item + đối chiếu LIVE chống trùng + guard no-new-notebook).")
        return 0
    # --apply: PHA 1 — cổng precheck (chống clobber/ghi-mù) + mở nhật ký WAL + cred + đếm slot LIVE + guard no-create
    _ok_gate, _pfv = _apply_gate(a, write_cols="nlm_source_id,nlm_notebook_id,nlm_status")
    if not _ok_gate:
        return 2
    run_id = _apply_journal_start("ingest-missing", {"snapshot": snapshot_ts, "profile": _active_profile(), "targets": len(targets)})
    try:
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    except (Exception, SystemExit):
        pass
    try:
        nc = _imp("nlm_cli")
        base_room = NLM_SLOT_CAP - int(nc.notebook_get(base_nb).get("source_count") or 0)
        overflow_room = (NLM_SLOT_CAP - int(nc.notebook_get(overflow_shard).get("source_count") or 0)) if overflow_shard else 0
    except Exception as e:  # noqa: BLE001
        print(f"[tl] ingest-missing --apply: không đếm được slot LIVE ({e}) — DỪNG (an toàn).", file=sys.stderr); return 2
    route, shard, reason = _overflow_route(base_room, overflow_shard, overflow_room)
    if _apply_ing:   # HEARTBEAT: log timeout 43s → in ROUTE ngay khi biết (base đầy → overflow) để thấy đang chạy đúng.
        print(f"[tl]   ✓ slot LIVE: base {NLM_SLOT_CAP - base_room}/{NLM_SLOT_CAP}, overflow {(NLM_SLOT_CAP - overflow_room) if overflow_shard else '-'}/{NLM_SLOT_CAP} → route={route} — tiếp: dedup LIVE…", file=sys.stderr, flush=True)
    if route == "blocked":
        print(json.dumps({"ok": False, "blocked": True, "reason": reason, "base_room": base_room,
                          "overflow_room": overflow_room}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 0    # GATE có chủ đích (không tạo notebook), KHÔNG phải lỗi lệnh
    target_nb = base_nb if route == "base" else shard
    # S13: đối chiếu nguồn LIVE trên notebook đích → tách target ĐÃ có nguồn (LINK/reconcile) khỏi target cần add.
    # (review#3) KHÔNG liệt kê được LIVE = KHÔNG xác minh trùng → DỪNG (an toàn) trừ khi --skip-live-check (checkpoint vẫn chống trùng trong-phiên).
    skip_live = getattr(a, "skip_live_check", False)
    to_add, already_live, unresolved = targets, [], 0
    _live, _live_ok = {}, False
    try:
        _live = nc.source_list(target_nb, skip_freshness=True, drive=True)
        _live_ok = bool(_live.get("ok"))
        if _live_ok:
            to_add, already_live, unresolved = _ingest_missing_dedup_live(targets, _live.get("sources") or [])
    except Exception as _le:  # noqa: BLE001
        _live = {"error": str(_le)}
    if not _live_ok:
        if not skip_live:
            print(json.dumps({"ok": False, "aborted": True, "reason": "LIVE_SOURCE_LIST_FAILED",
                              "error": _live.get("error") if isinstance(_live, dict) else None,
                              "note": "KHÔNG xác minh được nguồn LIVE trên notebook → DỪNG (an toàn, tránh tạo trùng cross-run). "
                                      "Sửa `nlm login` rồi chạy lại; HOẶC --skip-live-check nếu CHẮC không trùng."},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
        print("[tl] ⚠ --skip-live-check: BỎ dedup cross-run (chỉ checkpoint trong-phiên) — rủi ro trùng nếu lần trước ngắt giữa chừng.", file=sys.stderr)
    if unresolved:
        print(f"[tl] ⚠ {unresolved} nguồn LIVE không trích được drive_id/sohieu → dedup có thể SÓT các nguồn đó (soi `nlm-orphans`).", file=sys.stderr)
    if _apply_ing:
        print(f"[tl]   ✓ dedup LIVE: {len(to_add)} cần add, {len(already_live)} đã có (reconcile) — BẮT ĐẦU (journal run={run_id}) …", file=sys.stderr, flush=True)
    _ck_key = re.sub(r"[^A-Za-z0-9_-]", "", str(target_nb))[:64] or "base"    # (review#4) checkpoint PER-NOTEBOOK (không collide đa-profile/shard)
    ckpt = Path(os.path.expanduser("~")) / f".tl_ingest_missing_ckpt_{_ck_key}.json"
    _ckf = _ingest_ckpt_load_full(ckpt)   # v1.29.1: {done, pending, linked, fails} — WAL-hoá (xử log LIVE 2026-07-02)
    done, pending, linked, fails = _ckf["done"], _ckf["pending"], _ckf["linked"], _ckf["fails"]

    def _ck_flush():
        try:
            ckpt.write_text(json.dumps({"done": done, "pending": pending, "linked": linked, "fails": fails},
                                       ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    # (v1.29.1 WAL-pending) run trước bị NGẮT GIỮA source_add (pending còn dấu — subprocess wait tới 630s, client-timeout
    # hay giết ở đây) → target đó BẮT BUỘC xác minh FRESH (skip_freshness=False; listing thường có thể CHƯA thấy source
    # vừa tạo) TRƯỚC khi cho add lại — chống trùng kiểu VBHN_67 3×. Thấy → LINK; không thấy → clear pending, cho add.
    _pend_dids = ({_entry_drive_id(e) for e in to_add} & set(pending.keys())) if pending else set()
    if _pend_dids and _live_ok:
        try:
            _fresh = nc.source_list(target_nb, skip_freshness=False, drive=True)
            if _fresh.get("ok"):
                _ta2, _al2, _u2 = _ingest_missing_dedup_live(
                    [e for e in to_add if _entry_drive_id(e) in _pend_dids], _fresh.get("sources") or [])
                if _al2:
                    _found = {_entry_drive_id(e) for e, _sid in _al2}
                    already_live.extend(_al2)
                    to_add = [e for e in to_add if _entry_drive_id(e) not in _found]
                    print(f"[tl]   ⚠ WAL-pending: {len(_al2)} nguồn add DỞ ở run trước ĐÃ có LIVE (fresh) → LINK, KHÔNG add lại.",
                          file=sys.stderr, flush=True)
        except Exception as _pe:  # noqa: BLE001
            print(f"[tl]   ⚠ WAL-pending: fresh-verify lỗi ({_pe}) — vẫn tiếp (dedup thường + title-tier đã chạy).",
                  file=sys.stderr, flush=True)
        for _d in list(_pend_dids):
            pending.pop(_d, None)     # đã xác minh fresh xong (thấy→link / không thấy→cho add lại)
        _ck_flush()
    elif _pend_dids and not _live_ok:
        print(f"[tl]   ⚠ WAL-pending: {len(_pend_dids)} mục add-dở run trước NHƯNG không list được LIVE → rủi ro trùng CAO nếu --skip-live-check.",
              file=sys.stderr, flush=True)
    g = _gas()
    ok_n, link_n, skip_n, fail_n, reg_fail_n, results = 0, 0, 0, 0, 0, []
    room = base_room if route == "base" else overflow_room
    cols = "nlm_source_id,nlm_notebook_id,nlm_status" + (",row_kind" if route == "overflow" else "")

    def _reg_link(did, sid) -> bool:
        # (Pha 1) qua `_journaled_reg_write`: journal intent{before}+commit{verify} + validate cột + patched≥1. reg_bulk có
        # thể lỗi (GAS down/quota) / patched=0 (dòng chưa index) → KHÔNG crash batch (source_id ĐÃ ở checkpoint → reconcile).
        nonlocal reg_fail_n
        item = {"drive_id": did, "nlm_source_id": sid, "nlm_notebook_id": target_nb, "nlm_status": "pushed"}
        if route == "overflow":
            item["row_kind"] = "overflow"
        v = _journaled_reg_write(run_id, g, [item], cols, before_by_key={did: {"nlm_source_id": "", "nlm_status": ""}})
        ok = bool(v.get("verified"))
        if not ok:
            _emsg = v.get("error") or f"patched={v.get('patched')}/{v.get('expected')}"
            print(f"        ⚠ reg_bulk chưa xác nhận ({_emsg}) — source_id ĐÃ ở checkpoint+journal, lần sau reconcile.", file=sys.stderr, flush=True)
        done[did] = sid
        pending.pop(did, None)  # đã có source thật + link xong → hết "add dở" (kể cả khi vào qua already_live)
        if ok:
            linked[did] = sid   # v1.29.1: verified → run sau SKIP relink (GAS cache 600s che nlm_source_id ≠ chưa ghi)
        _ck_flush()
        if not ok:
            reg_fail_n += 1
        return ok

    # (1) ĐÃ có nguồn LIVE nhưng registry chưa ghi → LINK (reconcile), KHÔNG source_add lại (chống trùng S13/S12-repush).
    # v1.29.1: ckpt.linked ghi nhận link ĐÃ verified → SKIP relink lặp (manifest GAS-cache 600s còn che nlm_source_id
    # khiến mục cứ bị liệt lại — log LIVE: hàng đợi 1→8 qua 6 lần gọi). Ép relink lại: --relink (hoặc nlm-reconcile).
    al_skip_n = 0
    for e, sid in already_live:
        did = _entry_drive_id(e)
        if not getattr(a, "relink", False) and linked.get(did) == sid and done.get(did) == sid:
            al_skip_n += 1
            if pending.pop(did, None) is not None:   # review 3a: nhánh skip không qua _reg_link → tự dọn pending
                _ck_flush()
            results.append({"drive_id": did, "ok": True, "already_linked": True, "source_id": sid})
            continue
        _reg_link(did, sid); link_n += 1
        results.append({"drive_id": did, "ok": True, "linked": True, "source_id": sid, "notebook": target_nb})
        print(f"  [link] {(_entry_sohieu(e) or '(?)')[:18]:18s} đã có LIVE → reconcile (không tạo trùng)", file=sys.stderr, flush=True)
    if al_skip_n:
        print(f"  [skip] {al_skip_n} mục ĐÃ link verified trước đó (ckpt) → bỏ relink lặp (GAS cache 600s; ép: --relink).",
              file=sys.stderr, flush=True)
    # (2) Nạp mới per-item. v1.29.1 WAL: pending ghi TRƯỚC source_add (subprocess wait tới 630s — client-timeout giết ở
    # đây là gốc trùng VBHN_67); done ghi NGAY SAU; fails đếm FAIL liên tiếp (≥3 → SKIP đỡ đốt batch, --retry-failed ép).
    _total = len(to_add)
    pf_skip_n = 0
    for _i, e in enumerate(to_add, 1):
        did = _entry_drive_id(e)
        if did in done:      # done chỉ chứa source_id THẬT → LINK (idempotent), KHÔNG add lại
            _reg_link(did, done[did]); skip_n += 1; continue
        if not getattr(a, "retry_failed", False) and int(fails.get(did) or 0) >= 3:
            pf_skip_n += 1
            results.append({"drive_id": did, "ok": False, "skipped": "PUSH_FAIL_SKIPPED", "fails": int(fails.get(did) or 0)})
            print(f"  [skip] {(_entry_sohieu(e) or '(?)')[:18]:18s} FAIL {fails.get(did)} lần trước → SKIP (đỡ đốt batch; ép: --retry-failed). "
                  f"Soi: `tl header-verify --drive-id {did}`; bản-thô-trùng → `tl source-update-corpus {did} false --apply`.",
                  file=sys.stderr, flush=True)
            continue
        if room <= 0:
            print("  ⚠ HẾT CHỖ giữa chừng → DỪNG (KHÔNG tạo notebook). Chạy lại sau khi duyệt shard mới.", file=sys.stderr); break
        print(f"  [{_i}/{_total}] + {(_entry_sohieu(e) or '(?)')[:18]:18s} {_entry_name(e)[:40]} …", file=sys.stderr, flush=True)
        pending[did] = _entry_name(e)[:120]   # WAL-pending TRƯỚC add — timeout giữa add → run sau fresh-verify, không add mù
        _ck_flush()
        r = nc.source_add(target_nb, drive_id=did, title=_entry_name(e)[:120], wait=True)
        if not r.get("ok"):
            fail_n += 1
            fails[did] = int(fails.get(did) or 0) + 1
            pending.pop(did, None)            # add fail THẬT (CLI trả lỗi) = không tạo source → bỏ dấu pending
            _ck_flush()
            results.append({"drive_id": did, "ok": False, "error": r.get("error"), "fails": fails[did]})
            print(f"        FAIL ({fails[did]}×): {r.get('error')}", file=sys.stderr, flush=True); continue
        sid = r.get("source_id")
        done[did] = sid   # checkpoint NGAY sau add (trước reg_bulk) → ngắt sau đây, lần sau đối chiếu LIVE/ckpt sẽ LINK không add lại
        pending.pop(did, None)
        fails.pop(did, None)
        _ck_flush()
        _reg_link(did, sid)
        ok_n += 1; room -= 1
        results.append({"drive_id": did, "ok": True, "source_id": sid, "notebook": target_nb})
        print(f"        OK → {sid}", file=sys.stderr, flush=True)
    _journal_append(run_id, {"t": "run_end", "ok": (fail_n == 0 and reg_fail_n == 0),
                             "counts": {"OK": ok_n, "LINKED": link_n, "SKIP": skip_n, "FAIL": fail_n, "REG_WRITE_FAIL": reg_fail_n,
                                        "ALREADY_LINKED": al_skip_n, "PUSH_FAIL_SKIPPED": pf_skip_n}})
    print(json.dumps({"ok": True, "route": route, "notebook": target_nb, "reason": reason, "manifest_snapshot": snapshot_ts, "journal": run_id,
                      "OK": ok_n, "LINKED": link_n, "SKIP": skip_n, "FAIL": fail_n, "REG_WRITE_FAIL": reg_fail_n,
                      "ALREADY_LINKED": al_skip_n, "PUSH_FAIL_SKIPPED": pf_skip_n,
                      "unresolved_live": unresolved, "skipped_no_sohieu": len(_skip_note), "results": results}, ensure_ascii=False, indent=2))
    _hint = " ⚠ REG_WRITE_FAIL>0 → chạy `tl nlm-reconcile <nb> --apply` để khớp registry↔NLM." if reg_fail_n else ""
    print(f"[tl] ingest-missing: OK={ok_n} LINKED={link_n} SKIP={skip_n} FAIL={fail_n} REG_WRITE_FAIL={reg_fail_n} "
          f"no_sohieu={len(_skip_note)} → {target_nb} (route={route}). journal={run_id}.{_hint} MANIFEST_STALE: `tl manifest` rồi `tl boot --refresh`.", file=sys.stderr)
    return 0 if (fail_n == 0 and reg_fail_n == 0) else 1


def _upload_mime_ext(path: str) -> tuple[str, str]:
    """MIME + đuôi THẬT cho file local upload (để Drive `organize convert=true` convert ĐÚNG định dạng — KHÔNG ép .docx
    cho mọi file: upload .pdf/.doc giả .docx sẽ hỏng convert). Lạ đuôi → coi như .docx (giữ hành vi cũ)."""
    ext = Path(path).suffix.lower()
    return _MIME_BY_EXT.get(ext, _DOCX_MIME), (ext if ext in _MIME_BY_EXT else ".docx")


def _ingest_target(g, sohieu: str, name: str):
    """(3) preflight → chọn notebook đích: base = NOTEBOOK CỦA PROFILE ĐANG DÙNG (TL_NOTEBOOK_ID, do
    `_apply_profile_env` set từ config.profiles.<active>.notebookId), đầy → overflow shard.
    Group B (log rà, NGHIÊM TRỌNG): trước hard-code NLM_BASE_NOTEBOOK (743ed200 = VBQPPL) → `ingest-local
    --profile NQ36` ĐẨY NHẦM về VBQPPL thay vì notebook NQ36 → 'Could not add drive source'. Nay theo profile."""
    base = (os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK or "").strip()
    overflow = os.environ.get("TL_OVERFLOW_NOTEBOOK_ID") or ""
    if not overflow:
        return base, {"note": "không cấu hình overflow → base"}
    params = {"notebookId": base, "overflowNotebookId": overflow, "normative": "true"}
    if sohieu: params["soHieu"] = sohieu
    else: params["name"] = name
    pf = g.get("nlm_preflight", **params)
    slots = pf.get("slots") or {}
    route_overflow = bool(slots.get("full") or (pf.get("overflow_route") and pf.get("decision") == "REVIEW"))
    return (overflow if route_overflow else base), {"decision": pf.get("decision"), "slots_full": slots.get("full"),
                                                    "used": slots.get("used"), "cap": slots.get("cap")}


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


def _profile_source_quality(path: str, explicit: str = "auto") -> str:
    q = (explicit or "auto").strip().lower()
    if q in ("digital", "ocr"):
        return q
    ext = Path(path or "").suffix.lower()
    return "ocr" if ext in {".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff"} else "digital"


def _profile_read_probe_text(path: str, text_file: str | None = None) -> tuple[str, str]:
    """v1.34.27 #3 (log phiên nạp 4 file): DRY phải TRUNG THỰC — trước đây .docx local không probe được
    (probe_text_source=null) → phân loại rơi về tên file, DRY báo kind=normal nhưng --apply (đọc text sau
    convert) lại thành draft và chặn ở cổng Điều. Nay trích text .docx CỤC BỘ (zip word/document.xml,
    strip tag — không cần lib ngoài) để DRY dự báo đúng kết quả apply."""
    if text_file:
        return Path(text_file).read_text(encoding="utf-8", errors="replace"), str(text_file)
    ext = Path(path).suffix.lower()
    if ext in {".txt", ".md", ".csv", ".html", ".htm", ".json"}:
        return Path(path).read_text(encoding="utf-8", errors="replace"), str(path)
    if ext == ".docx":
        try:
            import zipfile as _zf
            with _zf.ZipFile(path) as z:
                xml = z.read("word/document.xml").decode("utf-8", errors="replace")
            xml = re.sub(r"</w:p>", "\n", xml)
            txt = re.sub(r"[ \t]+", " ", re.sub(r"<[^>]+>", "", xml)).strip()
            if txt:
                return txt, f"{path}#docx-local"
        except Exception:  # noqa: BLE001 — docx hỏng/mã hoá → giữ hành vi cũ (probe rỗng)
            pass
    return "", ""


def _sohieu_from_title_zone(zone: str) -> str:
    """(v1.34.6 #1 — log phiên 2026-07-09): số hiệu của CHÍNH tài liệu chỉ nằm ở VÙNG TIÊU ĐỀ trên DÒNG NGẮN
    kiểu letterhead ('Số: 41/2024/QH15', 'Luật số: …' ≤80 ký tự) — ƯU TIÊN dòng có 'Số:' đứng trước. Số hiệu
    trong CÂU VĂN DÀI là TRÍCH DẪN văn bản khác (báo cáo/tài liệu thường nhắc luật) → BỎ. Trước đây quét cả
    16k ký tự đầu nên báo cáo nhắc 'Luật số 41/2024/QH15' bị gán loai=Luật + sohieu=41/2024/QH15."""
    best = ""
    for _c in _RAW_SOHIEU_RE.finditer(zone or ""):
        _ls = zone.rfind("\n", 0, _c.start()) + 1
        _le = zone.find("\n", _c.end())
        _le = len(zone) if _le < 0 else _le
        if _le - _ls > 80:
            continue                                   # dòng dài = văn xuôi → trích dẫn, không phải letterhead
        _pre = _strip_accents(zone[_ls:_c.start()]).lower()
        if re.search(r"\bso\s*[:.]?\s*$", _pre):
            return _c.group(0)                          # 'Số:' ngay trước — chắc chắn nhất
        best = best or _c.group(0)
    return best


def _classify_doc_header(text: str, filename: str = "") -> dict:
    head = (text or "")[:16000]
    blob = f"{head}\n{filename or ''}"
    norm = _strip_accents(blob).lower()
    sohieu = _sohieu_from_title_zone(head[:1500]) or _parse_sohieu_from_name(filename or "")
    # N2a (v1.33.41 — log rà VBHN-first: ingest-analyze đề xuất sohieu 100/2015 [luật GỐC] cho VBHN 135): layout
    # VPQH in số VBHN ở KHỐI KÝ CUỐI văn bản (đã biết từ S-2 v1.33.15) → match ĐẦU TIÊN trong head là số luật
    # gốc trong câu 'Bộ luật Hình sự số 100/2015/QH13 … được hợp nhất'. Văn bản LÀ VBHN (marker text/tên file)
    # mà match đầu KHÔNG phải dạng VBHN → quét tìm match VBHN ưu tiên; không thấy trong probe → sohieu RỖNG
    # (SOHIEU_MISSING sẽ bắn — ép --sohieu tường minh, KHÔNG đăng ký nhầm số gốc cho bản hợp nhất).
    _is_vbhn_doc = ("van ban hop nhat" in norm) or ("vbhn" in _strip_accents(filename or "").lower())
    # v1.34.6 #1: chạy quét-VBHN cả khi sohieu title-zone RỖNG — layout VPQH in số VBHN ở KHỐI KÝ CUỐI
    # (ngoài vùng tiêu đề), quét sâu blob 16k CHỈ cho dạng số VBHN (không nhận số thường trong thân).
    if _is_vbhn_doc and (not sohieu or ("VBHN" not in sohieu.upper() and "VPQH" not in sohieu.upper())):
        _mv = re.search(r"\d+[-_/](?:\d+[-_/])?VBHN[-_/][A-Za-zĐđ0-9]+|\d+[-_/](?:VPQH|VBHN)\b", blob, re.I)
        sohieu = _mv.group(0) if _mv else ""
    loai = _infer_loai(filename or head[:200], sohieu)
    if _is_vbhn_doc:
        loai = "Văn bản hợp nhất"    # N2a: header VBHN in 'BỘ LUẬT'/'LUẬT' to → _infer_loai đoán nhầm loại gốc
    if not loai:
        if "nghi quyet" in norm:
            loai = "Nghị quyết"
        elif "du thao" in norm and "luat" in norm:
            loai = "Luật"
    facts = _extract_header_facts(head)
    year = _sohieu_year(norm_sohieu(sohieu)) if sohieu else None
    if not year and facts.get("issue_date"):
        try:
            year = int(str(facts["issue_date"])[:4])
        except Exception:
            year = None
    # N2b (v1.33.41): draft trước quét TOÀN 16000 chars — 'lấy ý kiến' trong THÂN luật (điều khoản về lấy ý kiến
    # nhân dân) bắn cờ DUTHAO cho luật chính thức. Marker dự thảo chỉ có nghĩa ở VÙNG TIÊU ĐỀ (đầu văn bản/tên
    # file); VBHN là văn bản ĐÃ ban hành — không bao giờ draft.
    _draft_zone = _strip_accents((head[:1500] or "") + "\n" + (filename or "")).lower()
    draft = (not _is_vbhn_doc) and any(k in _draft_zone for k in ("du thao", "draft", "lay y kien", "gop y du thao"))
    kind = "normal"
    if draft:
        kind = "draft"
    elif loai == "Nghị quyết":
        kind = "nq"
    elif sohieu or loai in {"Luật", "Bộ luật", "Nghị định", "Thông tư", "Quyết định", "Pháp lệnh", "Văn bản hợp nhất"}:
        kind = "vbqppl"
    return {
        "kind": kind,
        "draft": draft,
        "sohieu": sohieu or "",
        "sohieu_key": norm_sohieu(sohieu) if sohieu else "",
        "loai": loai,
        "issue_year": year,
        "issue_date": facts.get("issue_date") or "",
        "agency": facts.get("agency") or "",
        "title": _profile_title_from_header(head, filename),
        "header_chars": len(head),
    }


def _safe_profile_doc_name(info: dict, fallback_name: str = "") -> str:
    loai_code = {
        "Luật": "Luat", "Bộ luật": "Bo_luat", "Nghị quyết": "NQ", "Nghị định": "ND",
        "Thông tư": "TT", "Quyết định": "QD", "Pháp lệnh": "PL", "Văn bản hợp nhất": "VBHN",
    }.get(str(info.get("loai") or ""), "VB")
    title = info.get("title") or fallback_name or "van_ban"
    title = re.sub(r"\.[A-Za-z0-9]{1,8}$", "", str(title))
    title = re.sub(r"(?i)\bdu\s*thao\b|dự\s*thảo", "", title)
    title_slug = re.sub(r"[^A-Za-z0-9]+", "_", _strip_accents(title)).strip("_")[:70] or "van_ban"
    parts = []
    if info.get("draft"):
        parts.append("DUTHAO")
    parts.append(loai_code)
    if info.get("sohieu_key"):
        parts.append(str(info["sohieu_key"]).replace("-", "_"))
    elif info.get("issue_year"):
        parts.append(str(info["issue_year"]))
    parts.append(title_slug)
    return re.sub(r"_+", "_", "_".join(parts)).strip("_")[:160]


def _ingest_verify_gate(text: str, classification: dict | None = None,
                        source_quality: str = "digital", ocr_verified: bool = False,
                        base_profile: bool | None = None) -> dict:
    info = classification or {}
    stats = _dieu_sequence_stats(text or "")
    # (v1.34.6 #3 — log phiên 2026-07-09): đòi cấu trúc Điều CHỈ theo kind (vbqppl/draft/nq). Bỏ vế
    # 'or có sohieu' — văn bản thường CÓ số hiệu (công văn/báo cáo 123/BC-UBND) không có Điều là bản chất,
    # không phải lỗi; trước đây gate chặn corpus_allowed làm profile-ingest dừng nửa chừng, phải nlm-add tay.
    # v1.34.27 #2 (log phiên nạp 4 file): đòi Điều CHỈ trên corpus NỀN vbqppl — profile VĂN BẢN THƯỜNG
    # (categories=own) chứa văn kiện KIỂU MỤC (Chỉ thị/Tờ trình/Công văn, kể cả bản DỰ THẢO của chúng)
    # không bao giờ có Điều → dương-tính-giả DIEU_STRUCTURE_NOT_VERIFIED chặn cả 4 file, phải nlm-add tay.
    if base_profile is None:
        base_profile = (_active_profile() == DEFAULT_PROFILE)
    requires_dieu = (info.get("kind") in {"vbqppl", "draft", "nq"}) and bool(base_profile)
    dieu_ok = (stats["count"] > 0) if requires_dieu else True
    norm = _strip_accents(text or "").lower()
    has_phuluc = "phu luc" in norm
    phuluc_ok = (not has_phuluc) or bool(re.search(r"(?mi)^\s*phụ\s*lục\b|^\s*phu\s*luc\b", text or ""))
    source_quality = (source_quality or "digital").lower()
    ocr_ok = source_quality != "ocr" or bool(ocr_verified)
    ok = bool(text) and dieu_ok and phuluc_ok and ocr_ok
    flags = []
    if not text:
        flags.append("NO_TEXT_FOR_VERIFY")
    if not dieu_ok:
        flags.append("DIEU_STRUCTURE_NOT_VERIFIED")
    if not phuluc_ok:
        flags.append("PHULUC_MENTION_WITHOUT_HEADING")
    if not ocr_ok:
        flags.append("OCR_UNVERIFIED_NOT_CORPUS")
    info_flags = []
    if not requires_dieu and stats["count"] == 0:
        info_flags.append("DIEU_NOT_REQUIRED_NORMAL_DOC")   # trace v1.34.6 #3: thường-không-Điều là hợp lệ
    if (info.get("kind") in {"vbqppl", "draft", "nq"}) and not base_profile:
        info_flags.append("PROFILE_DOC_DIEU_NOT_REQUIRED")  # trace v1.34.27 #2: profile thường tắt đòi-Điều
    return {"ok": ok, "dieu_ok": dieu_ok, "phuluc_ok": phuluc_ok, "ocr_ok": ocr_ok,
            "source_quality": source_quality, "ocr_verified": bool(ocr_verified),
            "requires_dieu": requires_dieu, "dieu_stats": stats, "flags": flags, "info": info_flags,
            "corpus_allowed": ok and ocr_ok}


def _split_by_dieu_chunks(text: str, max_chars: int = 100000) -> list[dict]:
    text = text or ""
    max_chars = max(10000, int(max_chars or 100000))
    marks = list(re.finditer(r"(?mi)^\s*Điều\s+(\d+)\b", text))
    if not marks:
        return [{"part": 1, "start_dieu": None, "end_dieu": None, "chars": len(text), "text": text}] if text else []
    spans = []
    preamble = text[:marks[0].start()].strip()
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        spans.append((int(m.group(1)), text[m.start():end].strip()))
    chunks, cur, start_dieu, end_dieu = [], "", None, None
    for n, block in spans:
        if cur and len(cur) + len(block) + 2 > max_chars:
            chunks.append({"part": len(chunks) + 1, "start_dieu": start_dieu, "end_dieu": end_dieu,
                           "chars": len(cur), "text": cur.strip()})
            cur, start_dieu, end_dieu = "", None, None
        if not cur and not chunks and preamble:
            cur = preamble + "\n\n"
        if start_dieu is None:
            start_dieu = n
        end_dieu = n
        cur += (("\n\n" if cur.strip() else "") + block)
    if cur.strip():
        chunks.append({"part": len(chunks) + 1, "start_dieu": start_dieu, "end_dieu": end_dieu,
                       "chars": len(cur), "text": cur.strip()})
    return chunks


def _chunk_summaries(chunks: list[dict]) -> list[dict]:
    return [{k: c.get(k) for k in ("part", "start_dieu", "end_dieu", "chars")} for c in chunks]


def _profile_ingest_note(info: dict, gate: dict, source_quality: str, split_count: int = 0) -> str:
    bits = [f"source_quality={source_quality}", "status=du_thao" if info.get("draft") else "status=profile_own"]
    if split_count:
        bits.append(f"nlm_split_count={split_count}")
    if gate.get("flags"):
        bits.append("verify_flags=" + "|".join(gate.get("flags") or []))
    return "; ".join(bits)[:500]


def cmd_profile_ingest(a) -> int:
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    profile = _active_profile()
    if profile == DEFAULT_PROFILE and not getattr(a, "allow_default", False):
        print("[tl] profile-ingest chỉ dành cho profile dự án; thêm --allow-default nếu cố ý chạy trên vbqppl.", file=sys.stderr)
        return 2
    _perr = _profile_policy_error(require_registry=True, require_manifest=True, forbid_inherit=True)
    if _perr:
        return _emit_profile_policy_error(_perr, getattr(a, "json", False))
    f = getattr(a, "file", None)
    if not (f and Path(f).exists()):
        print(f"[tl] profile-ingest: không thấy file {f}", file=sys.stderr)
        return 2
    source_quality = _profile_source_quality(f, getattr(a, "source_quality", "auto"))
    # v1.34.6 #2: bảng tính đi đường riêng — canonical = Google SHEET (copy_convert toType=sheets),
    # không probe text/không gate Điều (không có văn bản pháp quy dạng bảng tính), NLM add type=sheets.
    _is_sheet = Path(f).suffix.lower() in _SPREADSHEET_EXTS
    probe_text, probe_source = ("", None) if _is_sheet else _profile_read_probe_text(f, getattr(a, "text_file", None))
    info = _classify_doc_header(probe_text, f)
    doc_name = getattr(a, "name", None) or _safe_profile_doc_name(info, Path(f).stem)
    if info.get("draft") and not doc_name.upper().startswith("DUTHAO_"):
        doc_name = "DUTHAO_" + doc_name
    if _is_sheet:
        gate = {"ok": True, "corpus_allowed": True, "dieu_ok": True, "phuluc_ok": True, "ocr_ok": True,
                "source_quality": source_quality, "ocr_verified": bool(getattr(a, "ocr_verified", False)),
                "requires_dieu": False, "dieu_stats": {"count": 0}, "flags": [],
                "info": ["SPREADSHEET_TEXT_VERIFY_SKIPPED"]}
    else:
        gate = _ingest_verify_gate(probe_text, info, source_quality, getattr(a, "ocr_verified", False))
    size_bytes = Path(f).stat().st_size
    large_threshold = int(getattr(a, "large_threshold", None) or NLM_LARGE_SRC_BYTES)
    chunk_max = int(getattr(a, "chunk_max_chars", None) or 100000)
    chunks = _split_by_dieu_chunks(probe_text, chunk_max) if (probe_text and (len(probe_text) > chunk_max or size_bytes > large_threshold)) else []
    plan = {
        "ok": True,
        "mode": "APPLY" if getattr(a, "apply", False) else "DRY",
        "profile": profile,
        "file": f,
        "probe_text_source": probe_source or None,
        "source_quality": source_quality,
        "classification": info,
        "doc_name": doc_name,
        "verify_gate": gate,
        "size_bytes": size_bytes,
        "large": bool(chunks),
        "chunk_plan": _chunk_summaries(chunks),
        "registry": {"row_kind": "own", "cat": "own", "corpus": bool(gate.get("corpus_allowed"))},
        "note": "DRY mặc định. --apply tạo canonical GDoc flat trong root profile; nếu tách, chunk NLM nằm trong _meta.",
    }
    if not getattr(a, "apply", False):
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0

    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    _perr = _profile_policy_error(require_registry=True, require_manifest=True, forbid_inherit=True)
    if _perr:
        return _emit_profile_policy_error(_perr, getattr(a, "json", False))
    root_id = os.environ.get("TL_ROOT_FOLDER_ID", "").strip()
    meta_id = os.environ.get("TL_META_FOLDER_ID", "").strip() or root_id
    if not root_id:
        print("[tl] profile-ingest: profile thiếu rootFolderId.", file=sys.stderr)
        return 2
    notebook_id, nb_err = _resolve_nlm_notebook(None)
    if nb_err:
        print(json.dumps({"ok": False, "step": "notebook_resolve", "error": nb_err}, ensure_ascii=False), file=sys.stderr)
        return 2
    g = _gas()
    inbox = (g.get("bootstrap") or {}).get("inboxFolderId")
    up_mime, up_ext = _upload_mime_ext(f)
    import base64
    up = g.post("upload", b64=base64.b64encode(Path(f).read_bytes()).decode("ascii"), name=Path(f).stem + up_ext,
                mime=up_mime, parentId=inbox, convert="false", register="false", share="false", force="true")
    fid = up.get("fileId") or up.get("id")
    if not fid:
        print(json.dumps({"ok": False, "step": "upload", "detail": up}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    hieuluc = DRAFT_WARNING if info.get("draft") else (getattr(a, "hieuluc", None) or "Còn")
    if _is_sheet:
        # v1.34.6 #2: organize chỉ convert→GDoc; bảng tính phải copy_convert toType=sheets (API_CONTRACT).
        org = g.get("copy_convert", fileId=fid, name=doc_name, folderId=root_id, toType="sheets",
                    register="true", share="true")
    else:
        okw = {"fileId": fid, "convert": "true", "name": doc_name, "moveSrc": "true", "register": "true",
               "cat": root_id, "reg_cat": "own", "reg_note": _profile_ingest_note(info, gate, source_quality),
               "hieuluc": hieuluc, "reg_hieuluc": hieuluc, "share": "true"}
        if info.get("sohieu"):
            okw["sohieu"] = info["sohieu"]
        if info.get("loai"):
            okw["loai"] = info["loai"]
        org = g.get("organize", **okw)
    gdoc = org.get("fileId")
    if not gdoc:
        print(json.dumps({"ok": False, "step": ("copy_convert_sheets" if _is_sheet else "organize"), "detail": org},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    # Deterministic readback: không add NLM/registry tiếp nếu Drive convert/rename chưa xác nhận được.
    src_id = (org.get("srcFileId") if _is_sheet else org.get("srcId")) or fid
    rb_convert = _verify_convert_readback(g, gdoc_id=gdoc, expected_name=doc_name,
                                          src_id=("" if _is_sheet else src_id),
                                          expected_src_name=("" if _is_sheet else doc_name + up_ext),
                                          expected_folder_id=root_id,
                                          expected_gdoc_mime=(_GSHEET_MIME if _is_sheet else None))
    if not rb_convert.get("ok"):
        print(json.dumps({"ok": False, "step": "convert_readback", "gdoc": gdoc, "src_id": src_id,
                          "readback": rb_convert,
                          "note": "Dừng trước NLM add: Drive convert/rename/move chưa đạt readback."},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2

    actual_text = ""
    if not _is_sheet:   # v1.34.6 #2: bảng tính không re-read/re-classify text (gate sheet đã chốt ở trên)
        try:
            actual_text = _read_doc_text(gdoc, getattr(a, "config", None)) or ""
        except Exception:
            actual_text = ""
    verify_text = actual_text or probe_text
    if verify_text:
        info = _classify_doc_header(verify_text, doc_name)
        if info.get("draft") and not doc_name.upper().startswith("DUTHAO_"):
            doc_name = "DUTHAO_" + doc_name
            try:
                g.get("rename", fileId=gdoc, name=doc_name)
            except Exception:
                pass
            hieuluc = DRAFT_WARNING
        gate = _ingest_verify_gate(verify_text, info, source_quality, getattr(a, "ocr_verified", False))
        chunks = _split_by_dieu_chunks(verify_text, chunk_max) if (len(verify_text) > chunk_max or size_bytes > large_threshold) else []
    note = _profile_ingest_note(info, gate, source_quality, len(chunks))
    if not gate.get("ok"):
        rb = g.post("reg_bulk", items=[{"drive_id": gdoc, "name": doc_name, "corpus": "false", "row_kind": "own",
                                        "note": note, "hieuluc": hieuluc}],
                    cols="name,corpus,row_kind,note,hieuluc")
        out = {"ok": False, "step": "verify_gate", "gdoc": gdoc, "src_id": fid, "gate": gate,
               "registry_patched": rb.get("patched"), "note": "Canonical đã tạo nhưng chưa corpus/NLM; cần verify/OCR lại."}
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
        return 2

    nc = _imp("nlm_cli")
    # v1.29.3 (AUDIT B3 #3): dedup-live gate TRƯỚC source_add — ca thật: re-run profile-ingest sau fail giữa chừng tạo
    # GDoc MỚI nhưng TITLE CŨ → nguồn trùng nội dung trên notebook. Gate khớp title canonical + mọi chunk-title.
    _gate_targets = [{"drive_id": gdoc, "name": doc_name[:120]}] + \
                    [{"drive_id": "", "name": f"{doc_name}__part{int(c['part']):02d}"[:120]} for c in (chunks if len(chunks) > 1 else [])]
    _verd, _dups = _nlm_dedup_gate(nc, notebook_id, _gate_targets, skip=getattr(a, "skip_live_check", False))
    if _verd == "dup":
        print(json.dumps({"ok": False, "step": "nlm_dedup_gate", "aborted": True, "reason": "TITLE_ALREADY_ON_NOTEBOOK",
                          "gdoc": gdoc, "matches": [{"name": p.get("name"), "source_id": sid} for p, sid in _dups[:5]],
                          "note": "Nguồn CÙNG title đã LIVE trên notebook (re-run sau fail giữa chừng?). GDoc đã tạo nhưng "
                                  "KHÔNG add NLM. Xử: `tl nlm-orphans`/`tl nlm-reconcile` link bản cũ, hoặc xóa nguồn cũ "
                                  "trước khi ingest bản mới. Ép add: --skip-live-check."},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    if _verd == "list_failed" and not getattr(a, "skip_live_check", False):
        print(json.dumps({"ok": False, "step": "nlm_dedup_gate", "aborted": True, "reason": "LIVE_SOURCE_LIST_FAILED",
                          "gdoc": gdoc,
                          "note": "KHÔNG liệt kê được nguồn LIVE (S13) → DỪNG trước source_add. `nlm login` rồi chạy lại; "
                                  "HOẶC --skip-live-check nếu CHẮC không trùng."}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    nlm_sources = []
    if len(chunks) > 1:
        for c in chunks:
            cname = f"{doc_name}__part{int(c['part']):02d}"
            cr = g.post("createtext", text=c["text"], name=cname, folderId=meta_id,
                        register="false", share="false", sourceUrl=f"profile-ingest:{gdoc}")
            chunk_id = cr.get("fileId")
            if not chunk_id:
                nlm_sources.append({"ok": False, "part": c["part"], "step": "createtext", "detail": cr})
                continue
            add = nc.source_add(notebook_id, drive_id=chunk_id, doc_type="doc", wait=True)
            src = add.get("source_id") if add.get("ok") else ""
            g.post("reg_upsert", drive_id=chunk_id, src_id=gdoc, sohieu=info.get("sohieu") or "",
                   loai=info.get("loai") or "thuong", name=cname, cat="own",
                   mime="application/vnd.google-apps.document", goc=gdoc,
                   nlm_source_id=src, nlm_notebook_id=notebook_id,
                   nlm_status=("pushed" if src else "error"), corpus="false", row_kind="ref",
                   note=(note + f"; chunk_part={c['part']}; dieu={c.get('start_dieu')}-{c.get('end_dieu')}")[:500])
            nlm_sources.append({"ok": bool(src), "part": c["part"], "chunk_gdoc": chunk_id,
                                "nlm_source_id": src, "chars": c.get("chars")})
        rb = g.post("reg_bulk", items=[{"drive_id": gdoc, "name": doc_name, "corpus": "true", "row_kind": "own",
                                        "note": note, "hieuluc": hieuluc}],
                    cols="name,corpus,row_kind,note,hieuluc")
    else:
        add = nc.source_add(notebook_id, drive_id=gdoc, doc_type=("sheets" if _is_sheet else "doc"), wait=True)
        if not add.get("ok"):
            print(json.dumps({"ok": False, "step": "nlm_add", "gdoc": gdoc, "detail": add}, ensure_ascii=False, indent=2),
                  file=sys.stderr)
            return 2
        src = add.get("source_id")
        rb = g.post("reg_bulk", items=[{"drive_id": gdoc, "name": doc_name, "nlm_source_id": src, "nlm_notebook_id": notebook_id,
                                        "row_kind": "own", "nlm_status": "pushed", "corpus": "true",
                                        "note": note, "hieuluc": hieuluc}],
                    cols="name,nlm_source_id,nlm_notebook_id,row_kind,nlm_status,corpus,note,hieuluc")
        nlm_sources.append({"ok": True, "canonical": True, "gdoc": gdoc, "nlm_source_id": src})
    out = {"ok": True, "profile": profile, "gdoc": gdoc, "src_id": fid, "doc_name": doc_name,
           "classification": info, "verify_gate": gate, "split_count": len(chunks),
           "nlm_sources": nlm_sources, "registry_patched": rb.get("patched"),
           "target_notebook": notebook_id, "hieuluc": hieuluc}
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0 if all(x.get("ok") for x in nlm_sources) else 2


def _ingest_local_cat_gate(cat: str, folders_now, pd: dict) -> dict:
    """PURE (v1.29.4 — AUDIT #10 tách testable từ cmd_ingest_local): cổng validate cat theo 45 chủ đề pháp điển +
    folder thực. Trả {official, cat_in_45, folder_exists, need_mkdir, cat_valid, review_cat, cat_note}."""
    official = pd.get(cat) if cat else None
    cat_in_45 = bool(cat) and (cat in pd if pd else (cat in folders_now))
    folder_exists = bool(cat) and cat in folders_now
    need_mkdir = cat_in_45 and not folder_exists      # chủ đề hợp lệ nhưng chưa có folder → tạo
    cat_note = None
    if not cat:
        cat_note = "CHƯA gán cat — truyền --cat <mã 1-45 theo Bộ pháp điển>."
    elif not cat_in_45:
        cat_note = (f"cat '{cat}' KHÔNG thuộc 45 chủ đề pháp điển. Tra `references/phap_dien_45.json` "
                    "(vd tố tụng→37, xuất nhập cảnh→01, hình sự→16).")
    elif need_mkdir:
        cat_note = f"chủ đề HỢP LỆ '{cat}: {(official or {}).get('ten')}' nhưng chưa có folder → sẽ tạo `{(official or {}).get('folder')}`."
    return {"official": official, "cat_in_45": cat_in_45, "folder_exists": folder_exists,
            "need_mkdir": need_mkdir, "cat_valid": cat_in_45, "review_cat": (not cat) or (not cat_in_45),
            "cat_note": cat_note}


def _ingest_local_prev_state(file_path: str, name: str) -> dict:
    """N6 (v1.33.42 — TĂNG TÍNH TẤT ĐỊNH, log rà VBHN-first: pipeline vượt 45s Cowork bị cắt giữa chừng → agent
    phải TỰ SUY 'còn bước nào' rồi tự chạy register/nlm-add tay, 4-5 round-trip/file): đọc journal các run
    ingest-local TRƯỚC cho CÙNG file (match meta.file, fallback meta.name) → trạng thái bước ĐÃ XONG
    {upload_fid, gdoc, src_docx, nlm_source_id, journal_prev}. `--resume` dùng để NỐI TIẾP tất định: bước xong
    → skip (tái dùng id từ journal), bước dở → chạy tiếp. Run MỚI NHẤT thắng. Best-effort, KHÔNG raise."""
    out: dict = {}
    try:
        runs = sorted(_journal_dir().glob("ingest-local_*.jsonl"))
    except Exception:  # noqa: BLE001
        return out
    for p in runs:                     # cũ → mới: run sau ghi đè run trước
        try:
            recs = [json.loads(ln) for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
        except Exception:  # noqa: BLE001
            continue
        if not recs or recs[0].get("cmd") != "ingest-local":
            continue
        head = recs[0]
        if str(head.get("file") or "") != str(file_path) and str(head.get("name") or "") != str(name or ""):
            continue
        st: dict = {}
        for r in recs:
            if r.get("t") != "commit" or not r.get("ok"):
                continue
            vf = r.get("verify") or {}
            if r.get("op") == "upload" and vf.get("fileId"):
                st["upload_fid"] = vf["fileId"]
            elif r.get("op") == "organize" and vf.get("gdoc"):
                st["gdoc"], st["src_docx"] = vf["gdoc"], vf.get("srcId")
            elif r.get("op") == "nlm_source_add" and vf.get("source_id"):
                st["nlm_source_id"] = vf["source_id"]
        if st:
            st["journal_prev"] = p.stem
            out = st
    return out


def cmd_ingest_local(a) -> int:
    """(2)+(3) Ingest 1 file local vào corpus bằng 1 lệnh: upload _HOP_NAP → organize (convert GDoc + tên chuẩn + cat + stamp + register)
    → preflight chọn base/overflow → `nlm source add` (CLI) → push registry. DRY mặc định; --apply để thực thi.
    (4) validate cat ∈ tập folder thực; lệch → REVIEW_CAT (chặn trừ --force-cat). (5) register=true → 1 dòng atomic (GDoc drive_id + src_id=docx).
    N6 (v1.33.42): `--resume` nối tiếp TẤT ĐỊNH sau timeout — đọc journal run trước, skip bước đã xong (tái dùng
    fileId/gdoc/source_id), gate dup → LINK thay vì abort. Cowork: chạy lại CÙNG LỆNH + --resume tới rc=0.
    v1.33.44 (log 7A S4/S5/S6): registry sạch NGAY tại ingest — loai chuẩn enum (_normalize_loai), reg_cat NHÃN ĐỦ
    (_cat_reg_label), bước link cuối ghi KÈM corpus=true — hết chuỗi vá backfill-loai/recat/register sau mỗi ingest."""
    import base64
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    _perr = _profile_policy_error(require_registry=True, require_manifest=False, forbid_inherit=True)
    if _perr:
        return _emit_profile_policy_error(_perr, getattr(a, "json", False))
    f = getattr(a, "file", None)
    if not (f and Path(f).exists()):
        print(f"[tl] ingest-local: không thấy file {f}", file=sys.stderr); return 2
    explicit_name = getattr(a, "name", None)
    explicit_cat = getattr(a, "cat", None)
    sohieu = (getattr(a, "sohieu", None) or "").strip()
    name = (explicit_name or Path(f).stem).strip()
    cat = _norm_cat(explicit_cat or "")
    goc = (getattr(a, "goc", None) or "").strip()
    hieuluc = (getattr(a, "hieuluc", None) or "Còn hiệu lực").strip()
    loai = (getattr(a, "loai", None) or ("VBHN" if name.upper().startswith("VBHN") else "")).strip()
    auto_plan = None
    if getattr(a, "auto_plan", False):
        try:
            auto_plan = _vb_ingest_auto_plan(
                f,
                text_file=getattr(a, "text_file", None),
                name=(explicit_name or ""),
                sohieu=sohieu,
                loai=loai,
                cat=cat,
                source_quality=getattr(a, "source_quality", "auto"),
                ocr_verified=getattr(a, "ocr_verified", False),
            )
        except Exception as e:  # noqa: BLE001
            print(json.dumps({"ok": False, "step": "auto_plan", "error": str(e)}, ensure_ascii=False, indent=2),
                  file=sys.stderr)
            return 2
        if not explicit_name and auto_plan.get("name"):
            name = auto_plan["name"]
        if not sohieu and auto_plan.get("sohieu"):
            sohieu = auto_plan["sohieu"]
        if not loai and auto_plan.get("loai"):
            loai = auto_plan["loai"]
        if not explicit_cat and auto_plan.get("cat"):
            cat = _norm_cat(auto_plan["cat"])
    # S5 (v1.33.44 — log 7A Cowork): loai ghi registry PHẢI là ENUM CHUẨN ngay lúc ingest ('VBHN' trơ →
    # 'Văn bản hợp nhất') — trước đây mỗi ingest xong phải `backfill-loai --normalize` vá lại (drift lặp mãi).
    if loai:
        loai = _normalize_loai(loai)
    # (4) validate cat theo ĐỦ 45 chủ đề pháp điển (không chỉ folder đang có)
    folders_now = _valid_cats(getattr(a, "config", None), getattr(a, "profile", None))   # folder THỰC
    pd = _load_phapdien()                                                                # 45 chủ đề + 00/46
    _cg = _ingest_local_cat_gate(cat, folders_now, pd)                                   # v1.29.4 (#10): PURE, test offline
    official, folder_exists = _cg["official"], _cg["folder_exists"]
    need_mkdir, cat_valid, review_cat, cat_note = _cg["need_mkdir"], _cg["cat_valid"], _cg["review_cat"], _cg["cat_note"]
    _src_ext = Path(f).suffix.lower()
    _fmt_warn = ("PDF = HẠ SÁCH (convert Google ~OCR, dễ lệch cấu trúc) — ưu tiên .docx official trước; sau convert PHẢI verify nguyên văn."
                if _src_ext == ".pdf" else None)
    _size_bytes = Path(f).stat().st_size
    _large_threshold = int(getattr(a, "large_threshold", None) or NLM_LARGE_SRC_BYTES)
    _large_file = _size_bytes > _large_threshold
    _large_note = (f"FILE LỚN: {_size_bytes:,}B > ngưỡng {_large_threshold:,}B → nạp NGUYÊN vào 1 nguồn NLM sẽ "
                   f"GIẢM chất lượng truy vấn (NLM tổng hợp tốt nhất ~≤100k ký tự/nguồn). NÊN HỎI người dùng cho "
                   f"phép TÁCH theo Phần/Chương/cụm Điều rồi ingest từng phần (mỗi phần 1 nguồn). Nạp nguyên: `--allow-large`."
                   if _large_file else None)
    # D1 (log rà): profile non-default + categories=inherit → văn bản ORGANIZE vào CÂY CHUNG VBQPPL (45 chủ đề),
    # KHÔNG nằm trong rootFolder RIÊNG của profile. Cảnh báo (advisory) để người dùng biết/đổi categories='own'.
    _inherit_warn = None
    if _active_profile() != DEFAULT_PROFILE and os.environ.get("TL_CATEGORIES_MODE", "").strip().lower() == "inherit":
        _inherit_warn = ("PROFILE categories=inherit → văn bản vào CÂY CHUNG VBQPPL theo cat, KHÔNG vào rootFolder RIÊNG "
                         "của profile. Muốn profile SỞ HỮU cây riêng: đặt config.profiles.<p>.categories='own' rồi ingest lại.")
    plan = {"file": f, "name": name, "sohieu": sohieu or None, "cat": cat or None,
            "reg_cat_label": (_cat_reg_label(cat) if cat else None),   # S6 v1.33.44: giá trị THẬT sẽ ghi registry
            "cat_ten": (official or {}).get("ten"), "cat_valid": cat_valid, "folder_exists": folder_exists,
            "need_mkdir": need_mkdir, "review_cat": review_cat, "cat_note": cat_note, "goc": goc or None,
            "hieuluc": hieuluc, "loai": loai or None, "size_bytes": _size_bytes,
            "large_file": _large_file, "large_threshold": _large_threshold, "large_note": _large_note,
            "inherit_tree_warn": _inherit_warn,
            "src_ext": _src_ext, "convert": "Drive organize convert=true (server-side)", "format_warn": _fmt_warn,
            "auto_plan": auto_plan}
    if not getattr(a, "apply", False):
        plan["mode"] = "DRY"; plan["note"] = "--apply để chạy: [mkdir nếu cần]→upload→organize(convert/cat/stamp/register)→preflight→nlm add (CLI)→push."
        print(json.dumps(plan, ensure_ascii=False, indent=2)); return 0
    if auto_plan and not explicit_cat and not getattr(a, "force_cat", False):
        auto_flags = set(auto_plan.get("warnings") or [])
        if "NO_PROBE_TEXT_FOR_AUTO_CAT" in auto_flags or "CAT_AUTO_LOW_CONFIDENCE" in auto_flags:
            print(json.dumps({"ok": False, "step": "auto_cat_review", "auto_plan": auto_plan,
                              "fix": "Truyền --text-file <ocr.txt> để phân tích nội dung, hoặc --cat <mã> / --force-cat nếu đã kiểm tra tay."},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
    if review_cat:
        print(json.dumps({"ok": False, "step": "cat_review", "cat": cat or None, "cat_note": cat_note,
                          "fix": "Truyền --cat <mã 1-45 đúng Bộ pháp điển> (xem references/phap_dien_45.json)."},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    # Large-file gate (yêu cầu user): file LỚN → DỪNG để HỎI người dùng cho phép TÁCH (chất lượng RAG cao nhất).
    # Bỏ qua bằng `--allow-large` (nạp nguyên, chấp nhận giảm chất lượng). KHÔNG tự tách (cần người duyệt cách tách).
    if _large_file and not getattr(a, "allow_large", False):
        # In ra STDOUT (đây là QUYẾT ĐỊNH cần người dùng thấy, như plan DRY) — không chôn ở stderr.
        print(json.dumps({"ok": False, "step": "large_file_split_gate", "size_bytes": _size_bytes,
                          "threshold": _large_threshold, "size_is_bytes": True,
                          "note": (_large_note or "") + " (ngưỡng theo BYTE file nguồn — ước lượng; chỉnh --large-threshold).",
                          "options": ["TÁCH theo Phần/Chương/cụm Điều → ingest từng phần (mỗi phần 1 nguồn, chất lượng cao nhất)",
                                       "Hoặc `--allow-large` để nạp NGUYÊN file (chấp nhận giảm chất lượng truy vấn)"]},
                         ensure_ascii=False, indent=2))
        return 2
    # Group B: profile DỰ ÁN thiếu notebookId → DỪNG (KHÔNG đẩy nhầm vào VBQPPL base). load_creds ở trên đã set
    # TL_NOTEBOOK_ID nếu profile có; nếu KHÔNG có và profile != vbqppl → lỗi NO_NOTEBOOK_ID (đúng gốc lỗi Nhóm B).
    _nb_check, _nb_err = _resolve_nlm_notebook(None)
    if _nb_err:
        print(json.dumps({"ok": False, "step": "notebook_resolve", "error": _nb_err}, ensure_ascii=False)); return 2
    # v1.29.7 (log NĐ131 #9): PRE-CHECK NLM TRƯỚC MỌI side-effect — pipeline giả định NLM sẵn sàng nhưng
    # `boot --setup` cố tình bỏ NLM (né timeout) → bước CUỐI `nlm add` gãy sau khi upload+organize+register ĐÃ xong
    # (chuỗi dở dang phải vá tay). Kiểm binary + notebook_get LIVE (~2s) NGAY ĐÂY; fail → DỪNG với hướng dẫn,
    # CHƯA đụng Drive/registry. Ép bỏ (biết NLM sẽ tự lo sau): --skip-nlm-preflight.
    if not getattr(a, "skip_nlm_preflight", False):
        _nlm_ok, _nlm_why = False, ""
        try:
            _nc0 = _imp("nlm_cli")
            if not _nc0.nlm_available():
                _nlm_why = "nlm CLI KHÔNG có trên PATH"
            else:
                _ng = _nc0.notebook_get(_nb_check)
                _nlm_ok = bool(_ng.get("ok"))   # notebook_get LUÔN có key 'ok' (review v1.29.7: bỏ nhánh or-source_count — {'ok':False,'source_count':0} từng lọt)
                if not _nlm_ok:
                    _nlm_why = f"notebook_get fail ({str(_ng.get('error'))[:80]}) — thường CHƯA auth"
        except Exception as _ne:  # noqa: BLE001
            _nlm_why = f"{type(_ne).__name__}: {_ne}"
        if not _nlm_ok:
            print(json.dumps({"ok": False, "step": "nlm_preflight", "aborted": True, "reason": "NLM_NOT_READY",
                              "detail": _nlm_why, "notebook": _nb_check,
                              "note": "DỪNG TRƯỚC upload (chưa đụng Drive/registry — không có chuỗi dở dang). "
                                      "Sửa: `tl up --nlm` (cài + auth NLM) rồi chạy lại; HOẶC --skip-nlm-preflight "
                                      "nếu chấp nhận tự vá bước nlm add sau (`tl nlm-add` + `tl nlm-reconcile`)."},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
    g = _gas()
    # v1.29.1 (log LIVE 2.4): JOURNAL bao trùm CHUỖI composite (mkdir→upload→organize→nlm_add→reg_link) — ngắt giữa
    # chừng → `tl journal <run>` chỉ RÕ bước dở + việc còn lại (ca Luật Dược 76/VBHN phải dò tay). Intent các bước
    # non-registry KHÔNG kèm `before` + op ∉ {reg_bulk,reg_upsert} → resume/undo (chỉ reapply op reg) KHÔNG đụng.
    # N6 (v1.33.42): --resume đọc trạng thái run trước TỪ JOURNAL (tất định — không đoán) TRƯỚC khi mở run mới.
    _prev = _ingest_local_prev_state(str(f), name) if getattr(a, "resume", False) else {}
    if _prev:
        print(f"[tl] ingest-local --resume: nối từ journal {_prev.get('journal_prev')} — đã xong: "
              + (",".join(k for k in ("upload_fid", "gdoc", "nlm_source_id") if _prev.get(k)) or "(chưa bước nào)"),
              file=sys.stderr)
    run_id = _apply_journal_start("ingest-local", {"file": str(f), "name": name, "cat": cat, "profile": _active_profile(),
                                                   **({"resumed_from": _prev.get("journal_prev")} if _prev else {})})

    def _step(op, key, **kw):
        _journal_append(run_id, {"t": "intent", "op": op, "key": key, "set": dict(kw)})

    def _step_ok(op, key, ok, **verify):
        _journal_append(run_id, {"t": "commit", "op": op, "key": key, "ok": bool(ok), "verify": dict(verify)})

    # (4) tạo folder chủ đề đúng tên chính thức nếu chưa có (mkdir idempotent + xoá cache cat)
    if need_mkdir:
        _step("mkdir_cat", cat, folder=(official or {}).get("folder"))
        mk = g.get("mkdir", name=(official or {}).get("folder"))
        _step_ok("mkdir_cat", cat, mk.get("ok"))
        if not mk.get("ok"):
            print(json.dumps({"ok": False, "step": "mkdir_cat", "journal": run_id, "detail": mk}, ensure_ascii=False), file=sys.stderr); return 2
    target, pf = _ingest_target(g, sohieu, name)
    inbox = (g.get("bootstrap") or {}).get("inboxFolderId")
    # convert=false + register=false: GIỮ file NHỊ PHÂN làm src (KHÔNG để upload tự convert→GDoc + tự register,
    # nếu không organize convert sẽ tạo GDoc THỨ HAI → trùng. Chỉ organize tạo 1 GDoc + 1 dòng registry.)
    # MIME/đuôi THẬT theo file (item upload-flow): .doc/.pdf/.docx upload đúng định dạng → organize convert=true convert đúng.
    up_mime, up_ext = _upload_mime_ext(f)
    if _prev.get("upload_fid"):
        # N6: upload đã xong ở run trước → tái dùng fileId từ journal (upload lại = file trùng ở _HOP_NAP).
        fid = _prev["upload_fid"]
        _step_ok("upload", name + up_ext, True, fileId=fid, resumed=True)
        print(f"[tl] --resume: skip upload (fileId={fid}).", file=sys.stderr)
    else:
        _step("upload", name + up_ext, mime=up_mime)
        up = g.post("upload", b64=base64.b64encode(Path(f).read_bytes()).decode(), name=name + up_ext,
                    mime=up_mime, parentId=inbox, convert="false", register="false")
        fid = up.get("fileId") or up.get("id")
        _step_ok("upload", name + up_ext, bool(fid), fileId=fid)
        if not fid:
            print(json.dumps({"ok": False, "step": "upload", "journal": run_id, "detail": up}, ensure_ascii=False), file=sys.stderr); return 2
    # (5) register=true → tạo 1 dòng registry atomic ngay (drive_id=GDoc, src_id=docx) — không lệ thuộc regen2 ghép cặp
    okw = {"fileId": fid, "convert": "true", "name": name, "moveSrc": "true", "hieuluc": hieuluc, "register": "true"}
    if cat:
        # S6 (v1.33.44 — log 7A): registry cat = NHÃN ĐỦ canonical `NN_Ten` (P1-1 v1.33.12 — recat/sapxep đã ghi
        # vậy; ingest để mã trơ '03' → sweep cat_label_variants + phải `recat` vá sau MỖI ingest). Folder resolve
        # server-side vẫn theo mã (okw.cat); chỉ giá trị GHI REGISTRY (reg_cat) lên nhãn đủ.
        okw["cat"] = cat; okw["reg_cat"] = _cat_reg_label(cat)
    if sohieu: okw["sohieu"] = sohieu
    if goc: okw["goc"] = goc
    if loai: okw["loai"] = loai
    if _prev.get("gdoc"):
        # N6: organize (convert+register) đã xong ở run trước → tái dùng gdoc/srcId (organize lại tạo GDoc THỨ 2).
        gdoc, src_docx = _prev["gdoc"], _prev.get("src_docx")
        _step_ok("organize", fid, True, gdoc=gdoc, srcId=src_docx, resumed=True)
        print(f"[tl] --resume: skip organize (gdoc={gdoc}).", file=sys.stderr)
    else:
        _step("organize", fid, cat=cat, sohieu=sohieu)
        org = g.get("organize", **okw)
        gdoc = org.get("fileId")
        src_docx = org.get("srcId")
        _step_ok("organize", fid, bool(gdoc), gdoc=gdoc, srcId=src_docx)
        if not gdoc:
            print(json.dumps({"ok": False, "step": "organize", "journal": run_id, "detail": org}, ensure_ascii=False), file=sys.stderr); return 2
    # Deterministic readback sau convert/rename/move: không add NLM nếu GDoc/source chưa đúng tên, đúng MIME.
    _src_for_rb = src_docx or fid
    _rb_convert = _verify_convert_readback(g, gdoc_id=gdoc, expected_name=name,
                                           src_id=_src_for_rb, expected_src_name=name + up_ext,
                                           expected_folder_id="")
    _step_ok("convert_readback", gdoc, bool(_rb_convert.get("ok")), checks=_rb_convert.get("checks"))
    if not _rb_convert.get("ok"):
        print(json.dumps({"ok": False, "step": "convert_readback", "journal": run_id, "gdoc": gdoc,
                          "src_id": _src_for_rb, "readback": _rb_convert,
                          "note": "Dừng trước NLM add: Drive convert/rename chưa đạt readback."},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    # v1.29.7 (log NĐ131 #1 — dòng registry sohieu=None dù đã truyền --sohieu): organize register CÓ nhận sohieu
    # server-side nhưng thực tế từng KHÔNG persist → theo doctrine verified-write: READ-BACK registry sau organize,
    # thiếu thì BACKFILL tường minh qua journaled reg_upsert (sohieu = khóa immutable → upsert, không reg_bulk).
    # N1 (v1.31.1): title_vn CÓ DẤU bắt ngay lúc ingest từ auto-plan (analyzer đã đọc header — 0 call thêm) →
    # dòng registry mới KHÔNG rơi vào nợ backfill-title-vn; QT-5 có trích yếu dấu từ đầu.
    _tvn = _title_vn_from_plan(auto_plan)
    if sohieu or _tvn:
        _rb_row, _rg_ok = {}, False
        try:
            _rg = g.get("reg_get", drive_id=gdoc)
            _rg_ok = bool(_rg.get("ok"))
            _rb_row = (_rg.get("rows") or [{}])[0] if _rg_ok else {}
        except Exception:  # noqa: BLE001
            _rb_row, _rg_ok = {}, False
        _need_sh = bool(sohieu) and norm_sohieu(str(_rb_row.get("sohieu") or "")) != norm_sohieu(sohieu)
        # review v1.31.1: title_vn CHỈ ghi khi read-back OK và field thật sự rỗng — reg_get lỗi thì thôi
        # (dòng vừa tạo gần như chắc chắn rỗng, nhưng không ghi mù; backfill-title-vn vét sau).
        _need_tv = bool(_tvn) and _rg_ok and not str(_rb_row.get("title_vn") or "").strip()
        if _need_sh or _need_tv:
            _bf = {"drive_id": gdoc}
            _before = {}
            if _need_sh:
                _bf["sohieu"] = sohieu
                _before["sohieu"] = str(_rb_row.get("sohieu") or "")
                if loai:
                    _bf["loai"] = loai
                if goc:
                    _bf["goc"] = goc
            if _need_tv:
                _bf["title_vn"] = _tvn
                _before["title_vn"] = str(_rb_row.get("title_vn") or "")
            _vbf = _journaled_reg_upsert(run_id, g, _bf, before=_before)
            print(f"[tl] {'⚠ organize KHÔNG persist sohieu → ' if _need_sh else ''}backfill reg_upsert"
                  f"{' (+title_vn at-ingest)' if _need_tv else ''}: "
                  f"{'OK' if _vbf.get('verified') else 'FAIL ' + str(_vbf.get('error'))}", file=sys.stderr, flush=True)
    nc = _imp("nlm_cli")
    src = _prev.get("nlm_source_id") or ""
    if src:
        # N6: nguồn NLM đã add ở run trước (journal có source_id) → skip gate+add, chỉ còn LINK registry.
        _step_ok("nlm_source_add", gdoc, True, source_id=src, resumed=True)
        print(f"[tl] --resume: skip nlm add (source_id={src}) → LINK registry.", file=sys.stderr)
    else:
        # v1.29.3 (AUDIT B3 #3): dedup-live gate trước source_add — re-run ingest-local sau fail giữa chừng tạo GDoc MỚI
        # nhưng TÊN CŨ → nguồn trùng nội dung. (GDoc mới không thể đã-live theo drive_id; tier title bắt ca re-run.)
        _verd, _dups = _nlm_dedup_gate(nc, target, [{"drive_id": gdoc, "name": name[:120]}],
                                       skip=getattr(a, "skip_live_check", False))
        if _verd == "dup":
            if getattr(a, "resume", False):
                # N6: --resume + nguồn ĐÃ live (run trước client-timeout nhưng add XONG server-side — đúng ca
                # 130/135 double-add) → LINK nguồn có sẵn thay vì abort bắt agent tự nlm-reconcile tay.
                src = _dups[0][1]
                _step_ok("nlm_dedup_gate", gdoc, True, reason="RESUME_LINK_EXISTING", source_id=src)
                print(f"[tl] --resume: nguồn ĐÃ LIVE trên notebook (source_id={src}) → LINK registry, KHÔNG add trùng.",
                      file=sys.stderr)
            else:
                _step_ok("nlm_dedup_gate", gdoc, False, reason="TITLE_ALREADY_ON_NOTEBOOK", source_id=_dups[0][1])
                print(json.dumps({"ok": False, "step": "nlm_dedup_gate", "journal": run_id, "aborted": True,
                                  "reason": "TITLE_ALREADY_ON_NOTEBOOK", "gdoc": gdoc, "source_id": _dups[0][1],
                                  "note": "Nguồn CÙNG tên đã LIVE trên notebook (re-run sau fail? bản cũ chưa gỡ?). Drive+register "
                                          "XONG, KHÔNG add NLM trùng. Xử: chạy lại với --resume (tự LINK nguồn có sẵn); hoặc "
                                          "`tl nlm-reconcile`/`tl nlm-orphans`; hoặc gỡ nguồn cũ rồi `tl nlm-add`. Ép: --skip-live-check."},
                                 ensure_ascii=False, indent=2), file=sys.stderr)
                return 2
        if not src and _verd == "list_failed" and not getattr(a, "skip_live_check", False):
            _step_ok("nlm_dedup_gate", gdoc, False, reason="LIVE_SOURCE_LIST_FAILED")
            print(json.dumps({"ok": False, "step": "nlm_dedup_gate", "journal": run_id, "aborted": True,
                              "reason": "LIVE_SOURCE_LIST_FAILED",
                              "note": "KHÔNG liệt kê được nguồn LIVE (S13) → DỪNG trước source_add (Drive+register XONG). "
                                      "`nlm login` rồi `tl nlm-add` bước còn lại; HOẶC --skip-live-check."},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
        if not src:
            _step("nlm_source_add", gdoc, notebook=target, title=name[:120])
            add = nc.source_add(target, drive_id=gdoc, doc_type="doc", wait=True)
            _step_ok("nlm_source_add", gdoc, add.get("ok"), source_id=add.get("source_id"))
            if not add.get("ok"):
                print(json.dumps({"ok": False, "step": "nlm_add(cli)", "journal": run_id, "gdoc": gdoc, "target": target, "detail": add,
                                  "note": "Drive+register XONG; chỉ NLM add lỗi → chạy lại CÙNG LỆNH + --resume, hoặc `tl nlm-add`."}, ensure_ascii=False, indent=2), file=sys.stderr)
                return 2
            src = add.get("source_id")
            _dup_after = _nlm_post_add_dup_check(nc, target, gdoc, src)   # N1 v1.33.41: bắt trùng-sau-add tại chỗ
            if _dup_after:
                print(json.dumps(_dup_after, ensure_ascii=False, indent=2), file=sys.stderr)
    # v1.29.7 (log NĐ131 #6): trước đây `target != NLM_BASE_NOTEBOOK → overflow` — SAI cho profile own (notebook
    # profile ≠ base VBQPPL toàn cục → mọi tài liệu profile bị gán overflow dù preflight nói 'không overflow → base').
    # ĐÚNG: overflow CHỈ khi target == overflow-shard ĐÃ CẤU HÌNH của profile đang chạy; còn lại (base VBQPPL hoặc
    # notebook riêng của profile own) = own.
    _ovf_nb = (os.environ.get("TL_OVERFLOW_NOTEBOOK_ID") or "").strip()
    rk = "overflow" if (_ovf_nb and target == _ovf_nb) else "own"
    # reg_link qua journaled+verified-write (thay g.post reg_bulk trần — đủ intent{before}+commit{verify}+validate cột)
    # S4 (v1.33.44 — log 7A Cowork): ghi KÈM corpus=true — trước đây bước link cuối KHÔNG set corpus (đường
    # profile-ingest 1 file CÓ set), timeout 45s cắt giữa add↔link để lại dòng registry corpus/nlm trống, phải
    # vá tay nlm-add + register. corpus=true thuộc đúng bước này (văn bản CHỈ vào corpus khi đã push NLM xong);
    # đứt giữa chừng → chạy lại CÙNG LỆNH + --resume là ghi nốt (idempotent).
    v = _journaled_reg_write(run_id, g, [{"drive_id": gdoc, "nlm_source_id": src, "nlm_notebook_id": target,
                                          "row_kind": rk, "nlm_status": "pushed", "corpus": "true"}],
                             "nlm_source_id,nlm_notebook_id,row_kind,nlm_status,corpus",
                             before_by_key={gdoc: {"nlm_source_id": "", "nlm_status": "", "corpus": ""}})
    rb = v.get("reg_bulk") or {}
    _journal_append(run_id, {"t": "run_end", "ok": bool(v.get("verified")), "counts": {"OK": 1}})
    out = {"ok": True, "name": name, "gdoc": gdoc, "src_docx": src_docx, "cat": cat, "journal": run_id,
           "reg_cat_label": (_cat_reg_label(cat) if cat else None), "loai": loai or None, "corpus": True,
           "cat_ten": (official or {}).get("ten"), "folder_created": need_mkdir, "preflight": pf,
           "target_notebook": target, "row_kind": rk, "nlm_source_id": src, "reg_pushed": rb.get("patched"),
           "reg_verified": bool(v.get("verified")), "via": "nlm-cli",
           "sidecar": "src_id=docx gắn vào dòng GDoc (register atomic; regen2 cũng tự ghép cặp cùng base-name)"}
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0


def _verify_convert_readback(g, *, gdoc_id: str, expected_name: str = "", src_id: str = "", expected_src_name: str = "", expected_folder_id: str = "", expected_gdoc_mime: str | None = None) -> dict:
    """Readback sau upload→convert→rename/move. Không ghi. Dùng bởi convert-verify và ingest pipelines.
    v1.34.6 #2: expected_gdoc_mime cho đường bảng tính (canonical = Google SHEET, không phải GDoc)."""
    checks = []
    def add(name, ok, detail=""):
        checks.append({"name": name, "ok": bool(ok), "detail": str(detail)[:300]})
    gi = _drive_info_file(g, gdoc_id)
    gf = gi.get("file") or {}
    add("gdoc_exists", gi.get("ok"), gi.get("error") or gf.get("id") or gf.get("fileId") or gdoc_id)
    gm = _file_mime(gi)
    _want_mime = expected_gdoc_mime or _GDOC_MIME
    add("gdoc_mime_is_google_native", gm == _want_mime, f"{gm or '<missing>'} (expect {_want_mime})")
    gn = _file_name(gi)
    if expected_name:
        add("gdoc_name_matches", gn == expected_name, f"actual={gn!r} expected={expected_name!r}")
    if expected_folder_id:
        gps = _file_parents(gi)
        add("gdoc_in_expected_folder", expected_folder_id in gps, ",".join(gps) or "<missing>")
    si = {}
    if src_id:
        si = _drive_info_file(g, src_id)
        sf = si.get("file") or {}
        add("source_exists", si.get("ok"), si.get("error") or sf.get("id") or sf.get("fileId") or src_id)
        sm = _file_mime(si)
        add("source_not_google_doc", sm != _GDOC_MIME, sm or "<missing>")
        sn = _file_name(si)
        if expected_src_name:
            add("source_name_matches", sn == expected_src_name, f"actual={sn!r} expected={expected_src_name!r}")
        if expected_folder_id:
            sps = _file_parents(si)
            add("source_in_expected_folder", expected_folder_id in sps, ",".join(sps) or "<missing>")
    ok = all(c["ok"] for c in checks)
    return {"ok": ok, "schema": "convert_readback.v1", "gdoc_id": gdoc_id, "src_id": src_id or None,
            "expected_name": expected_name or None, "expected_src_name": expected_src_name or None,
            "expected_folder_id": expected_folder_id or None, "checks": checks,
            "gdoc": {"name": gn, "mime": gm, "parents": _file_parents(gi)},
            "source": ({"name": _file_name(si), "mime": _file_mime(si), "parents": _file_parents(si)} if src_id else None)}

# ── I11 (v1.34.18): leftover-sweep từ tl.py (affinity-tốt-nhất) ──


def _normalize_hieuluc(s: str) -> str:
    """Map biến thể `hieuluc` → {Còn, Hết, Chưa} (giữ nguyên ngày/chuỗi khác nếu không nhận diện trạng thái trần)."""
    raw = str(s or "").strip()
    if not raw:
        return raw
    k = _strip_accents(raw).lower()
    if k in ("con", "con hieu luc", "conhieuluc"):
        return "Còn"
    if k in ("het", "het hieu luc", "hethieuluc", "thay the", "da thay the", "bai bo", "het hl"):
        return "Hết"
    if k in ("chua", "chua hieu luc", "chuahieuluc", "pending"):
        return "Chưa"
    return raw      # ngày/chuỗi cụ thể (vd '01/07/2026') → giữ nguyên

def _looks_like_drive_id(s: str) -> bool:
    """P0-1 LỚP 1 (MERGE patch AUDIT 07/2026 → v1.33.13): Drive file ID thật luôn [A-Za-z0-9_-] và ≥20 ký tự
    (thường 33/44) — id ngắn = gần như chắc chắn CẮT CỤT/typo khi copy-paste output rút gọn. Check OFFLINE rẻ,
    chạy TRƯỚC lớp 2 existence-check (manifest/Drive live). Cho phép prefix 'nlm:' (khóa ghost hợp lệ)."""
    s = (s or "").strip()
    if s.startswith("nlm:"):
        return len(s) > 10
    return bool(re.fullmatch(r"[A-Za-z0-9_-]{20,}", s))

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

def _valid_cats(config_path=None, profile=None) -> set:
    """(4) Tập mã cat có FOLDER THỰC của profile, đọc từ config.profiles.<p>.categories."""
    for p in _config_candidates(config_path):
        if p and Path(p).exists():
            cfg = _read_json_file(p)
            if cfg:
                prof = _profiles_from_config(cfg).get(_selected_profile_name(profile, cfg)) or {}
                cats = prof.get("categories")
                # MERGE nhánh-3 v1.33.14: profile categories='inherit' (doctrine §12) → tra cây của profile mặc định.
                if isinstance(cats, str) and cats == "inherit":
                    prof = _profiles_from_config(cfg).get(cfg.get("defaultProfile", DEFAULT_PROFILE)) or {}
                    cats = prof.get("categories")
                if isinstance(cats, dict):
                    return set(cats.keys()) | {"QUARANTINE"}
    return set()

def _vb_ingest_auto_plan(path: str, text_file: str | None = None, name: str = "", sohieu: str = "",
                         loai: str = "", cat: str = "", source_quality: str = "auto",
                         ocr_verified: bool = False) -> dict:
    probe_text, probe_source = _profile_read_probe_text(path, text_file)
    _fname = Path(path).name    # (MERGE Claude) CHỈ tên file (KHÔNG full path) → tránh _RAW_SOHIEU_RE bắt nhầm fragment UUID trong đường dẫn
    info = _classify_doc_header(probe_text, _fname)
    fallback_info = _classify_doc_header("", _fname)
    merged = dict(info)
    for k in ("sohieu", "sohieu_key", "loai", "issue_year"):
        if not merged.get(k) and fallback_info.get(k):
            merged[k] = fallback_info.get(k)
    if sohieu:
        merged["sohieu"] = sohieu
        merged["sohieu_key"] = norm_sohieu(sohieu)
    if loai:
        merged["loai"] = loai
    # (MERGE Claude) CHỦ ĐỀ đặt tên lấy từ dòng tiêu đề THẬT (bỏ dòng số hiệu/DỰ THẢO, strip loại, ALL-CAPS→sentence)
    # → chống tên Codex lặp số hiệu; dự thảo dùng _safe_profile_doc_name (DUTHAO_).
    _subj = _doc_subject_for_name(probe_text, merged)
    if _subj:
        merged["title"] = _subj.capitalize() if _subj.isupper() else _subj
    if (name or "").strip():
        doc_name = name.strip()
    elif merged.get("draft"):
        doc_name = _safe_profile_doc_name(merged, Path(_fname).stem)
    else:
        doc_name = _vb_standard_doc_name(merged, Path(_fname).stem)
    cat_plan = _vb_auto_cat_from_text(probe_text, doc_name + "\n" + Path(path).stem, cat)
    warnings = []
    # N2d (v1.33.41 — log rà VBHN-first: auto-plan gợi cat=00 [văn kiện Đảng] cho VBHN Luật giám sát QH): cat 00
    # KHÔNG BAO GIỜ hợp lệ cho VBQPPL (mirror gate _CAT_PIN/_cat_likely_wrong 'Luật không→23, VBHN không→46') —
    # thân luật nhắc 'Đảng' làm alias 00 thắng điểm. Hạ về rỗng + cảnh báo, KHÔNG ghi bừa.
    if cat_plan.get("cat") == "00" and str(merged.get("loai") or "") in {
            "Luật", "Bộ luật", "Pháp lệnh", "Văn bản hợp nhất", "Nghị định", "Thông tư", "Quyết định"}:
        warnings.append("CAT_00_PARTY_BLOCKED_FOR_VBQPPL")
        cat_plan = dict(cat_plan, cat="", confidence="low",
                        note="cat 00 (văn kiện Đảng) không hợp lệ cho VBQPPL — truyền --cat tường minh")
    # N2 (v1.33.41): VBHN auto-plan KHÔNG đáng tin bằng luật thường (số VBHN ở khối ký cuối, tên chủ đề dễ dính
    # cơ quan) — nhắc tường minh để driver set --name/--sohieu/--cat theo bản hợp nhất.
    if str(merged.get("loai") or "") == "Văn bản hợp nhất":
        warnings.append("VBHN_AUTO_PLAN_VERIFY_EXPLICIT: đối chiếu --sohieu (số VBHN, KHÔNG phải số luật gốc) "
                        "+ --name (chủ đề) + --cat trước khi --apply")
    if not probe_text:
        warnings.append("NO_PROBE_TEXT_FOR_AUTO_CAT")
    if not merged.get("sohieu"):
        warnings.append("SOHIEU_MISSING")
    if cat_plan.get("confidence") in {"low", "missing"}:
        warnings.append("CAT_AUTO_LOW_CONFIDENCE")
    srcq = _profile_source_quality(path, source_quality)
    if srcq == "ocr" and not ocr_verified:
        warnings.append("OCR_UNVERIFIED_NOT_CORPUS")
    return {
        "ok": bool(doc_name and cat_plan.get("cat")),
        "file": path,
        "probe_text_source": probe_source or None,
        "probe_chars": len(probe_text or ""),
        "classification": merged,
        "name": doc_name,
        "sohieu": merged.get("sohieu") or "",
        "loai": merged.get("loai") or "",
        "cat": cat_plan.get("cat") or "",
        "cat_plan": cat_plan,
        "source_quality": srcq,
        "ocr_verified": bool(ocr_verified),
        "warnings": warnings,
        "note": "Auto-plan chỉ đáng tin khi có probe text/OCR text; thiếu text thì cần --text-file, --cat hoặc --force-cat.",
    }

def _dieu_sequence_stats(text: str) -> dict:
    nums = [int(x) for x in re.findall(r"(?mi)^\s*Điều\s+(\d+)\b", text or "")]
    gaps = []
    for a, b in zip(nums, nums[1:]):
        if b > a + 1:
            gaps.append({"after": a, "before": b})
    return {"count": len(nums), "first": nums[0] if nums else None, "last": nums[-1] if nums else None,
            "monotonic": all(b > a for a, b in zip(nums, nums[1:])), "gaps": gaps[:20]}

def _drive_info_file(g, file_id: str) -> dict:
    """Best-effort Drive metadata readback qua webapp action=info. Không raise."""
    if not file_id:
        return {"ok": False, "error": "EMPTY_FILE_ID", "file": {}}
    try:
        info = g.get("info", fileId=file_id)
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"INFO_EXCEPTION:{type(e).__name__}:{e}", "file": {}}
    if not isinstance(info, dict):
        return {"ok": False, "error": "INFO_NON_DICT", "raw": str(info)[:200], "file": {}}
    f = info.get("file") if isinstance(info.get("file"), dict) else info
    return {"ok": bool(info.get("ok", True) and (f.get("id") or f.get("fileId") or file_id)), "raw": info, "file": f}

def _file_parents(info: dict) -> list[str]:
    f = info.get("file") or {}
    parents = f.get("parents") or f.get("parentIds") or []
    if isinstance(parents, str):
        return [parents]
    return [str(x.get("id") if isinstance(x, dict) else x) for x in parents if x]
