# -*- coding: utf-8 -*-
"""tl_core.nlm_admin_ops — ĐỢT B (v1.34.65, kế hoạch `ke-hoach-guard-va-boc-tl-core-2026-07-18.md` §5):
tách NGUYÊN VĂN đường GHI + audit vật lý NLM khỏi tl_core/nlm_ops.py (208KB = 61% trần mount ~343KB) —
**RANH GIỚI MODULE = RANH GIỚI QUYỀN GHI/ĐỌC**: 7 cmd `nlm-add/nlm-migrate/nlm-reconcile/
nlm-source-remove/push-overflow/overflow-resolve/nlm-audit-physical` + 11 helper (`_nlm_add_deferred/
_nlm_add_doc_type/_shard_row_kind/_migrate_plan/_nlm_reconcile_plan/_physical_audit_classify/
_migrate_resume_write` [đi theo migrate về NGỮ NGHĨA dù --from-plan đọc]/`_nlm_post_add_dup_check/
_nlm_source_drive_id/_nlm_source_list_cached/_nlm_list_stale_read`). Đường ĐỌC + fallback E1 Ở LẠI
nlm_ops (`nlm_query/cross/get/links/list, _nlm_or_corpus, _nlm_hard_dead`, banner/slots/preflight/
auth_status/orphans/slot_audit); plan-helper ngoài danh-sách-tên §5 Ở LẠI (R2 — không sweep:
`_nlm_source_remove_plan/_source_remove_delete_verdict/_nlm_dedup_gate/_nlm_add_capacity_error`);
HẰNG (`_ROW_KIND_PROTECTED/NLM_BATCH_LINKS_THRESHOLD/_NLM_COOKIE_*`) Ở LẠI nlm_ops — re-export tl giữ
nguồn cũ. `COMMAND_META.nlm_fallback` các cmd move GIỮ NGUYÊN (add/migrate=defer; reconcile/audit=
unverified; source-remove=none). Hành vi khoá bởi charact §6.1 (.tl_state/charact_pre_B) + r126 wiring
+ golden (diff CÓ KẾ HOẠCH duy nhất: py_size.files_scanned 63→64)."""
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


def _nlm_link_row_kind(explicit, cur_rk: str, shard_is_overflow: bool):
    """r180 S8 (PURE, test offline): row_kind ghi ở bước reg_link của nlm-add — cờ --row-kind tường
    minh THẮNG suy-topology (trước đây nlm-add trả row_kind=null, phải `register --row-kind` riêng);
    không cờ → luật cũ v1.34.49 F-06: shard overflow suy 'overflow' trừ kind bảo hộ (ref/thuong);
    còn lại None (không đụng cột)."""
    rk = (explicit or "").strip().lower()
    if rk:
        return rk
    if shard_is_overflow and (cur_rk or "") not in _ROW_KIND_PROTECTED:
        return "overflow"
    return None


def cmd_nlm_add(a) -> int:
    """(1) Thêm nguồn NLM qua CLI `nlm source add` (thay MCP source_add) — đúng directive CLI-first."""
    # Group B: nạp TL_NOTEBOOK_ID từ PROFILE ĐANG DÙNG (trước đây thiếu → --profile NQ36 nlm-add rơi về VBQPPL base).
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        nc = _imp("nlm_cli")
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False), file=sys.stderr); return 2
    nb, _nberr = _resolve_nlm_notebook(a.notebook_id)
    if _nberr:
        print(json.dumps({"ok": False, "error": _nberr}, ensure_ascii=False), file=sys.stderr); return 2
    # v1.34.60 (E3 push-defer — ADR-4): probe chủ động TRƯỚC mọi side-effect (gate/claim/add). NLM hard-dead
    # + fallback bật → defer: registry nlm_status=deferred + batch-link, KHÔNG add mù, rc=0. --no-fallback/
    # TL_NLM_FALLBACK=0 → đường cũ (gate dedup sẽ fail-closed LIVE_SOURCE_LIST_FAILED như trước).
    _v60a = _nlm_or_corpus("nlm-add", a, notebook_id=nb, probe=True)
    # r196 (TRINH 3.9 — ca KL 137 24-07): notebook 404 bền ≠ NLM offline → rc=2 fail-closed TRƯỚC mọi
    # side-effect (KHÔNG defer — defer trỏ đích không nhìn thấy; trước r196 banner «NLM OFFLINE» đánh lừa,
    # --url còn chết NLM_OFFLINE_NO_DEFER_FOR_URL khó hiểu ×2).
    if _v60a["route"] == "not_found":
        print(json.dumps({"ok": False, "error": "NOTEBOOK_NOT_FOUND", "notebook": nb,
                          "detail": _v60a["why"],
                          "note": "nlm CLI không nhìn thấy notebook này (auth có thể vẫn sống). "
                                  "(1) Kiểm --notebook-id = UUID ĐẦY ĐỦ theo config topology; "
                                  "(2) NLM chập chờn sau mutation lớn — đã retry 5s/15s, chờ ≥60s thử lại; "
                                  "(3) lane thay thế: MCP source_add + `tl register` nối sổ."},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    if _v60a["route"] == "deferred":
        return _nlm_add_deferred(a, nb, why=_v60a["why"])
    for _w54 in (_nlm_preflight_report(nb, probe=False).get("warn") or []):   # v1.34.54 A1: tầng-2 tuổi cookie (WARN, không chặn; tầng-1 live = gate dedup bên dưới)
        print(f"[tl] ⚠ {_w54}", file=sys.stderr)
    # v1.29.3 (AUDIT B3 #3): CỔNG dedup-live BẮT BUỘC trước source_add — nlm-add là đường push TRẦN duy nhất còn lại
    # (từng tạo trùng khi dùng làm recovery sau timeout). Khớp drive_id/title; url/file/text KHÔNG title → gate không
    # khớp được (vẫn liệt kê để lộ list_failed). Ép bỏ: --skip-live-check.
    _did, _title = getattr(a, "drive_id", None), getattr(a, "title", None)
    if _did or _title:
        _verd, _dups = _nlm_dedup_gate(nc, nb, [{"drive_id": _did or "", "name": _title or ""}],
                                       skip=getattr(a, "skip_live_check", False))
        if _verd == "dup":
            print(json.dumps({"ok": False, "aborted": True, "reason": "ALREADY_ON_NOTEBOOK",
                              "source_id": _dups[0][1], "notebook": nb,
                              "note": "Nguồn ĐÃ có LIVE (khớp drive_id/sohieu/title) → KHÔNG add trùng. Link registry: "
                                      "`tl nlm-reconcile` (hoặc register). Ép add: --skip-live-check."},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
        if _verd == "list_failed" and not getattr(a, "skip_live_check", False):
            print(json.dumps({"ok": False, "aborted": True, "reason": "LIVE_SOURCE_LIST_FAILED",
                              "note": "KHÔNG liệt kê được nguồn LIVE → không xác minh được trùng (S13) → DỪNG. "
                                      "Sửa `nlm login` rồi chạy lại; HOẶC --skip-live-check nếu CHẮC không trùng."},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
    # v1.34.56 (A-#2 — kế hoạch 13-vấn-đề 2026-07-16, Q3=b): CLAIM F-04 TRƯỚC source_add — nlm-add là đường
    # push trần CUỐI chưa có claim (timeout client nhưng add server-side vẫn xong → retry tạo 3 bản Phu_luc_I
    # trùng). CHỈ claim khi có --drive-id (url/file/text không có drive identity → giữ nguyên, chỉ dedup-gate);
    # --skip-live-check KHÔNG bỏ claim. MANDATORY client-side (khớp D1 ingest-local): endpoint lỗi → rc=2 TRƯỚC add.
    _claim56, _run56 = None, None
    if getattr(a, "drive_id", None):
        from tl_core.ingest_contract import identity_hash_for_drive_source
        try:
            _row_nm56 = next((str(e.get("name") or "") for e in _manifest_entries(refresh=False)
                              if str(e.get("drive_id") or e.get("gdoc_id") or "") == str(a.drive_id)), "")
        except Exception:  # noqa: BLE001
            _row_nm56 = ""
        _claim56 = identity_hash_for_drive_source(str(a.drive_id), target_scope=nb,
                                                  canonical_name=(getattr(a, "title", None) or _row_nm56 or ""),
                                                  profile=_active_profile())
        _run56 = _apply_journal_start("nlm-add", {"drive_id": a.drive_id, "notebook_id": nb,
                                                  "identity_hash": _claim56})
        try:
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))
            # F6 r192: claim qua _ingest_claim_get — retry chọn lọc 5s/15s (GAS 404 chập chờn đo 23-07)
            _cl56 = _ingest_claim_get(_gas(), a, keys=json.dumps([_claim56]), run_id=_run56,
                                      drive_ids=json.dumps([str(a.drive_id)]))
        except Exception as _ce56:  # noqa: BLE001
            _cl56 = {"ok": False, "error": str(_ce56)}
        if not _cl56.get("ok"):
            _journal_append(_run56, {"t": "run_end", "ok": False, "counts": {"BLOCKED": 1}})
            print(json.dumps({"ok": False, "error": "INGEST_CLAIM_FAILED", "detail": _cl56.get("error"),
                              "journal": _run56,
                              "note": "Không xin được claim xuyên host (F-04, webapp ≥2.21.2l) — DỪNG an toàn "
                                      "TRƯỚC add (chưa side-effect)."}, ensure_ascii=False, indent=2),
                  file=sys.stderr)
            return 2
        _gr56 = next((r0 for r0 in (_cl56.get("results") or []) if r0.get("identity_hash") == _claim56), None)
        if not (_gr56 or {}).get("granted"):
            _journal_append(_run56, {"t": "run_end", "ok": False, "counts": {"BLOCKED": 1}})
            print(json.dumps({"ok": False, "error": "CLAIMED_ELSEWHERE", "journal": _run56,
                              "reason": (_gr56 or {}).get("reason"),
                              "claim_ttl_hint": _claim_ttl_hint(),
                              "note": "Lần add trước/host khác có thể ĐÃ thành công server-side — `tl nlm-list "
                                      "<nb>` hoặc `tl nlm-reconcile` xác minh TRƯỚC khi retry; giờ hết hạn ở "
                                      "claim_ttl_hint. Sau timeout NLM: chờ ≥60s cho settle rồi mới kiểm."},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
    _dt, _dt_src = _nlm_add_doc_type(getattr(a, "type", None), getattr(a, "drive_id", None))
    if _dt_src.startswith("auto"):
        print(f"[tl] nlm-add: tự nhận --type {_dt} ({_dt_src}) — ép kiểu khác bằng --type.", file=sys.stderr)
    r = nc.source_add(nb, drive_id=getattr(a, "drive_id", None), url=getattr(a, "url", None),
                      file=getattr(a, "file", None), doc_type=_dt,
                      title=getattr(a, "title", None), wait=not getattr(a, "no_wait", False))
    print(json.dumps(r, ensure_ascii=False, indent=2))
    if not r.get("ok"):
        if _run56:
            _journal_append(_run56, {"t": "run_end", "ok": False, "counts": {"FAIL": 1}})
        print("[tl] nlm-add lỗi → fallback MCP source_add hoặc `nlm login`.", file=sys.stderr); return 2
    # N1 (v1.33.41): self-check TRÙNG-SAU-ADD — gate pre-add thua cuộc đua async (add trước timeout client
    # nhưng xong server-side, nguồn chưa hiện lúc gate list) → re-list FRESH ngay sau add, ≥2 nguồn cùng
    # drive_id = báo 🔴 tại chỗ kèm lệnh xóa (thay vì đợi nlm-reconcile).
    if getattr(a, "drive_id", None):
        _dup = _nlm_post_add_dup_check(nc, nb, a.drive_id, r.get("source_id"))
        if _dup:
            print(json.dumps(_dup, ensure_ascii=False, indent=2), file=sys.stderr)
    # v1.34.2 (Pha H live bắt): add OK mà dòng registry sẵn có vẫn trống nlm_source_id → nguồn thành 'unregistered'
    # nếu agent quên nlm-reconcile (đúng ca S14 smoke). Nay --drive-id + add OK + row ĐÃ TỒN TẠI trong registry →
    # reg_link NGAY (journaled+verified-write, cùng khuôn S4). CHỈ link cột nlm_* (không đụng corpus/row_kind —
    # đó là việc của pipeline ingest); KHÔNG có row → không tự tạo row xương, chỉ nhắc register/nlm-reconcile;
    # link lỗi → cảnh báo, KHÔNG fail add (nguồn đã lên NLM thật).
    # v1.34.56 (A-#1, Q2=a): VERIFY-THEN-LINK — registry chỉ ghi sự thật ĐÃ XÁC MINH vật lý (ca canary dbe706a0:
    # reg_link ghi sid NOT_FOUND → con trỏ treo phải revert tay). --no-wait → BỎ HẲN reg_link (sid chưa settle,
    # probe sẽ âm tính giả — stale-an-toàn, reconcile chữa); ngược lại probe live 1 nhịp TRƯỚC khi link.
    if getattr(a, "drive_id", None) and r.get("source_id"):
        if r.get("settle_timeout") and not getattr(a, "no_wait", False):
            # F5 van 3 (r192): CLI thôi chờ settle sau 120s (không huỷ — sid THẬT đã có) → xử NHƯ no-wait:
            # reg_link deferred (F3), reconcile cuối lô nâng pushed.
            print("[tl] ⚠ Van runtime (F5 r192): thôi chờ settle sau 120s — sid đã có, link DEFERRED; "
                  "`tl nlm-reconcile --apply` xác minh + nâng pushed.", file=sys.stderr)
        if getattr(a, "no_wait", False) or r.get("settle_timeout"):
            # F3 r191 (đề xuất #2 — đo 23-07: 3 nguồn add no-wait có source_id trả về mà registry nlm=''
            # nb='-', phải register tay từng dòng): no-wait KHÔNG bỏ reg_link nữa — link NGAY bằng
            # source_id THẬT từ add-response (link không cần đợi settle) + nlm_status='deferred' (ngữ
            # nghĩa mở rộng r191: ĐÃ GỬI NLM, CHƯA xác minh settle — không claim có mặt vật lý nên không
            # vi phạm VERIFY-THEN-LINK A-#1 v1.34.56). corpus KHÔNG đụng (không auto-true khi còn
            # deferred); `tl nlm-reconcile --apply` thấy nguồn live → nâng deferred→pushed. Claim KHÔNG
            # commit (sid chưa xác minh — TTL 5' tự heal, giữ nguyên hành vi cũ).
            _lk91 = _nlm_no_wait_reg_link(a, nb, str(r.get("source_id")))
            print(json.dumps({"reg_link": _lk91}, ensure_ascii=False), file=sys.stderr)
        else:
            # Probe rẻ: source_get nếu nlm_cli có; fallback re-list FRESH (list của dedup-gate chụp TRƯỚC add
            # — KHÔNG tái dùng được). Probe fail → KHÔNG ghi registry, rc vẫn 0 (add đã thành công; link là
            # bước phụ stale-an-toàn — nlm-reconcile --apply link khi nguồn đã live).
            _live56 = False
            try:
                if hasattr(nc, "source_get"):
                    _live56 = bool((nc.source_get(r["source_id"]) or {}).get("ok"))
                else:
                    _pl56 = nc.source_list(nb, skip_freshness=True)
                    _live56 = bool(_pl56.get("ok")) and any(
                        str(s.get("id") or "") == str(r["source_id"]) for s in (_pl56.get("sources") or []))
            except Exception:  # noqa: BLE001
                _live56 = False
            if not _live56:
                print(json.dumps({"reg_link": {"ok": False, "reason": "SID_NOT_LIVE_YET",
                                               "note": "add có thể đang settle — chạy tl nlm-reconcile <nb> "
                                                       "--apply để link khi đã live"}},
                                 ensure_ascii=False), file=sys.stderr)
            else:
                try:
                    _ents_na = _manifest_entries(refresh=True)
                    _row_e = next((e for e in _ents_na
                                   if str(e.get("drive_id") or e.get("gdoc_id") or "") == str(a.drive_id)), None)
                    _row_exists = _row_e is not None
                except Exception:
                    _ents_na, _row_e, _row_exists = [], None, False
                if _row_exists:
                    try:
                        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
                        _g = _gas()
                        _rid = _apply_journal_start("nlm-add-link", {"drive_id": a.drive_id, "source_id": r.get("source_id")})
                        # v1.34.49 (F-06): link nay ghi CẢ row_kind suy từ topology khi nb là shard overflow (trước đây
                        # cố ý bỏ → recovery add-tay vào VBQPPL-2 để row_kind=own, sweep mất dấu shard). Kind bảo hộ
                        # (ref/thuong) giữ nguyên; corpus vẫn không đụng (việc của pipeline ingest).
                        _it_na = {"drive_id": a.drive_id, "nlm_source_id": r.get("source_id"),
                                  "nlm_notebook_id": nb, "nlm_status": "pushed"}
                        _cols_na = "nlm_source_id,nlm_notebook_id,nlm_status"
                        # v1.34.57 (phát hiện smoke A 2026-07-16): before THẬT từ row hiện tại — link có thể
                        # ĐÈ dòng đã có pointer (hardcode "" cũ → journal undo không khôi phục được sid cũ).
                        _bef_na = {"nlm_source_id": str((_row_e or {}).get("nlm_source_id") or ""),
                                   "nlm_notebook_id": str((_row_e or {}).get("nlm_notebook_id") or ""),
                                   "nlm_status": str((_row_e or {}).get("nlm_status") or "")}
                        try:
                            _topo_na = _resolve_shard_topology(_ents_na, (os.environ.get("TL_NOTEBOOK_ID")
                                                                          or NLM_BASE_NOTEBOOK or "").strip())
                        except Exception:  # noqa: BLE001
                            _topo_na = {"shards": []}
                        _cur_rk_na = str((_row_e or {}).get("row_kind") or "").strip().lower()
                        _rk80 = _nlm_link_row_kind(getattr(a, "row_kind", None), _cur_rk_na,
                                                   _shard_row_kind(nb, _topo_na) == "overflow")   # r180 S8
                        if _rk80:
                            _it_na["row_kind"] = _rk80
                            _cols_na += ",row_kind"
                            _bef_na["row_kind"] = _cur_rk_na
                        _v = _journaled_reg_write(_rid, _g, [_it_na], _cols_na,
                                                  before_by_key={a.drive_id: _bef_na})
                        _journal_append(_rid, {"t": "run_end", "ok": bool(_v.get("verified")), "counts": {"OK": 1}})
                        print(json.dumps({"reg_link": {"ok": bool(_v.get("verified")), "journal": _rid,
                                                       "row_kind": _it_na.get("row_kind")}}, ensure_ascii=False), file=sys.stderr)
                        # v1.34.56 (A-#2): COMMIT claim GỘP reg_get_bulk sau link verified (best-effort, mẫu D1
                        # v1.34.55 — lỗi tự heal TTL 5'). no-wait / sid-not-live → KHÔNG commit (TTL tự heal).
                        if _claim56 and bool(_v.get("verified")):
                            try:
                                _g.get("reg_get_bulk", keys=json.dumps([str(a.drive_id)]), key_field="drive_id",
                                       commit_claims=json.dumps([{"identity_hash": _claim56,
                                                                  "source_id": r.get("source_id"),
                                                                  "run_id": _run56}]))
                            except Exception:  # noqa: BLE001
                                print("[tl]   ⚠ claim commit chưa xác nhận — tự hết hạn sau 5' (F-04 TTL), "
                                      "không chặn kết quả.", file=sys.stderr)
                    except Exception as _e:  # noqa: BLE001
                        print(f"[tl] nlm-add: add OK nhưng reg_link lỗi ({type(_e).__name__}: {_e}) → `tl nlm-reconcile --apply` để bắc cầu.", file=sys.stderr)
                else:
                    print("[tl] nlm-add: add OK nhưng registry CHƯA có dòng cho drive_id này → `tl register --drive-id …` "
                          "hoặc `tl nlm-reconcile --apply` để bắc cầu (không tự tạo row xương).", file=sys.stderr)
    if _run56:
        _journal_append(_run56, {"t": "run_end", "ok": True, "counts": {"OK": 1}})
    return 0


def _nlm_no_wait_reg_link(a, nb: str, sid: str) -> dict:
    """F3 r191: reg_link cho `nlm-add --no-wait` — ghi sid THẬT + nlm_status='deferred' (đã gửi NLM, chưa
    xác minh settle). Chỉ link dòng ĐÃ TỒN TẠI và CHƯA có nlm_source_id KHÁC (stale-an-toàn — không ghi đè
    pointer sẵn có bằng sid chưa settle); KHÔNG tự tạo row xương; KHÔNG đụng corpus/row_kind. Lỗi → note,
    KHÔNG fail add (nguồn đã lên NLM thật; nlm-reconcile là lưới)."""
    did = str(getattr(a, "drive_id", "") or "")
    try:
        _row = next((e for e in _manifest_entries(refresh=False)
                     if str(e.get("drive_id") or e.get("gdoc_id") or "") == did), None)
    except Exception as _e:  # noqa: BLE001
        return {"ok": False, "reason": "MANIFEST_UNAVAILABLE", "detail": f"{type(_e).__name__}: {_e}"[:200],
                "note": "reg_link no-wait cần manifest — `tl nlm-reconcile --apply` bắc cầu sau."}
    if _row is None:
        return {"ok": False, "reason": "ROW_NOT_FOUND",
                "note": "registry CHƯA có dòng cho drive_id — `tl register --drive-id …` hoặc "
                        "`tl nlm-reconcile --apply` (không tự tạo row xương)."}
    _old_sid = str(_row.get("nlm_source_id") or "").strip()
    if _old_sid and _old_sid != sid:
        return {"ok": False, "reason": "ROW_HAS_POINTER", "existing_source_id": _old_sid,
                "note": "dòng đã có nlm_source_id KHÁC — KHÔNG ghi đè bằng sid chưa settle; "
                        "`tl nlm-reconcile` phân xử."}
    try:
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        _rid = _apply_journal_start("nlm-add-link", {"drive_id": did, "source_id": sid, "no_wait": True})
        _bef = {"nlm_source_id": _old_sid,
                "nlm_notebook_id": str(_row.get("nlm_notebook_id") or ""),
                "nlm_status": str(_row.get("nlm_status") or "")}
        _v = _journaled_reg_write(_rid, _gas(), [{"drive_id": did, "nlm_source_id": sid,
                                                  "nlm_notebook_id": nb, "nlm_status": "deferred"}],
                                  "nlm_source_id,nlm_notebook_id,nlm_status",
                                  before_by_key={did: _bef})
        _journal_append(_rid, {"t": "run_end", "ok": bool(_v.get("verified")), "counts": {"DEFERRED": 1}})
        return {"ok": bool(_v.get("verified")), "journal": _rid, "nlm_status": "deferred", "source_id": sid,
                "next": "tl nlm-reconcile <nb> --apply — xác minh settle live, nâng deferred→pushed"}
    except Exception as _e:  # noqa: BLE001
        return {"ok": False, "reason": type(_e).__name__, "detail": str(_e)[:200],
                "note": "add OK; link lỗi → `tl nlm-reconcile --apply` bắc cầu."}


def _nlm_add_deferred(a, nb: str, *, why: str = "") -> int:
    """E3 (ADR-4 — push-defer): NLM chết → KHÔNG source_add mù, KHÔNG claim; hoàn tất mức registry:
    nlm_status=deferred (KHÔNG đụng corpus — chống corpus-ảo; KHÔNG bịa nlm_source_id) + in batch-link để
    dán tay; `tl nlm-reconcile --apply` set pointer/corpus SAU khi NLM sống. rc=0 (chuỗi chạy tiếp)."""
    did = str(getattr(a, "drive_id", None) or "").strip()
    if not did:
        print(json.dumps({"ok": False, "error": "NLM_OFFLINE_NO_DEFER_FOR_URL", "nlm_status": "offline",
                          "note": "nlm-add --url/--file không có drive identity để defer — chạy lại khi NLM "
                                  "sống (`tl nlm-auth-status --wait`)."}, ensure_ascii=False, indent=2),
              file=sys.stderr)
        return 2
    try:
        _row = next((e for e in _manifest_entries(refresh=False)
                     if str(e.get("drive_id") or e.get("gdoc_id") or "") == did), None)
    except Exception:  # noqa: BLE001
        _row = None
    _reg_deferred, _note_reg = False, ""
    if _row is None:
        _note_reg = "registry CHƯA có dòng cho drive_id — `tl register` trước; defer chỉ in link."
    elif str(_row.get("nlm_source_id") or "").strip():
        _note_reg = ("dòng registry ĐÃ có nlm_source_id — KHÔNG ghi đè deferred (stale-an-toàn); "
                     "`tl nlm-reconcile --apply` xử khi NLM sống.")
    else:
        try:
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))
            _rid = _apply_journal_start("nlm-add-deferred", {"drive_id": did, "notebook_id": nb})
            _bef = {"nlm_notebook_id": str(_row.get("nlm_notebook_id") or ""),
                    "nlm_status": str(_row.get("nlm_status") or "")}
            _v = _journaled_reg_write(_rid, _gas(), [{"drive_id": did, "nlm_notebook_id": nb,
                                                      "nlm_status": "deferred"}],
                                      "nlm_notebook_id,nlm_status", before_by_key={did: _bef})
            _reg_deferred = bool(_v.get("verified"))
            if not _reg_deferred:
                # v1.34.62 (live-smoke 2026-07-17 bắt OAN): readback field-level trong _verified_reg_write
                # (reg_get refresh=true + retry) có thể ÂM TÍNH GIẢ dù write ĐÃ vào — reg-query --live thấy
                # deferred ngay sau đó. RE-CHECK AUTHORITATIVE qua reg_get_bulk (cùng khuôn verify CUỐI của
                # nlm-migrate/claim-commit) TRƯỚC khi kết luận; chỉ giữ False khi authoritative CŨNG không
                # thấy (write thật fail) — không báo láo cả hai chiều.
                try:
                    _rgb62 = _gas().get("reg_get_bulk", keys=json.dumps([did]), key_field="drive_id")
                    _row62 = next((x for x in (_rgb62.get("rows") or [])
                                   if str(x.get("drive_id") or "") == did), None)
                    if (str((_row62 or {}).get("nlm_status") or "").strip().lower() == "deferred"
                            and str((_row62 or {}).get("nlm_notebook_id") or "").strip() == str(nb)):
                        _reg_deferred = True
                        _note_reg = ("verified qua reg_get_bulk AUTHORITATIVE (readback journaled âm tính "
                                     "giả — GAS cache; write đã vào).")
                except Exception:  # noqa: BLE001 — re-check best-effort, không nổ lệnh
                    pass
                if not _reg_deferred:
                    _note_reg = (f"reg-write deferred CHƯA xác minh được (readback + reg_get_bulk đều không "
                                 f"thấy) — kiểm `tl reg-query --live --drive-id {did}` rồi chạy lại nếu thiếu.")
            _journal_append(_rid, {"t": "run_end", "ok": _reg_deferred, "counts": {"DEFERRED": 1}})
        except Exception as _e:  # noqa: BLE001
            _note_reg = f"reg-write deferred lỗi ({type(_e).__name__}) — vẫn in link, reconcile xử sau."
    _url = _entry_links_url(_row or {"drive_id": did})
    print(json.dumps({"ok": True, "mode": "DEFERRED_NLM_OFFLINE", "nlm_status": "offline",
                      "fallback": "deferred", "source": "registry", "notebook": nb,
                      "notebook_url": f"https://notebooklm.google.com/notebook/{nb}",
                      "links": [_url], "registry_deferred": _reg_deferred,
                      **({"note_registry": _note_reg} if _note_reg else {}),
                      "why": (why or "")[:120],
                      "note": "NLM offline → CHƯA add gì (không claim, không corpus=true — chống corpus-ảo). "
                              "Dán link vào Add source → Websites của notebook rồi chạy "
                              f"`tl nlm-reconcile {nb} --apply`; hoặc nlm-add lại khi NLM sống."},
                     ensure_ascii=False, indent=2))
    return 0


def _nlm_add_doc_type(explicit, drive_id) -> tuple:
    """#4 backlog log-phiên (v1.34.17): --type KHÔNG truyền → tự nhận từ MIME manifest (OFFLINE, không gọi mạng):
    Google Sheet → 'sheets' (trước default cứng 'doc' → 'Could not add drive source' với phụ lục bảng tính).
    explicit LUÔN thắng; drive_id không có trong manifest → 'doc' (hành vi cũ). Trả (doc_type, nguồn-quyết-định)."""
    if explicit:
        return explicit, "explicit"
    if drive_id:
        try:
            for e in _manifest_entries(refresh=False):
                if _entry_drive_id(e) == str(drive_id):
                    if "spreadsheet" in str(e.get("mime") or "").lower():
                        return "sheets", "auto:manifest-mime-spreadsheet"
                    break
        except Exception:  # noqa: BLE001 — manifest thiếu/hỏng → giữ hành vi cũ
            pass
    return "doc", "default"


def _nlm_post_add_dup_check(nc, notebook_id: str, drive_id: str, new_sid: str | None) -> dict | None:
    """N1 (v1.33.41 — log rà VBHN-first: ingest-local vượt 45s Cowork, client BỊ GIẾT nhưng source_add server-side
    vẫn XONG → nlm-add tường minh sau đó add LẦN 2 [130/135 mỗi cái 2 nguồn]; gate PRE-add thua cuộc đua
    LẮNG-ĐỌNG-ASYNC — nguồn vừa add chưa hiện trong source_list / drive-metadata chưa expose, log ghi số nguồn
    LIVE dao động 286→292→290→288): SELF-CHECK NGAY SAU add — re-list FRESH (skip_freshness=False, mirror
    fresh-verify của ingest-missing), đếm nguồn CÙNG drive_id; ≥2 → trả payload 🔴 kèm lệnh xóa điền sẵn
    (phát hiện TẠI CHỖ thay vì đợi nlm-reconcile lộ link_candidates). Best-effort read-only: KHÔNG raise,
    KHÔNG tự xóa (xóa nguồn phải người duyệt). Trả None khi sạch/không kiểm được."""
    try:
        r = nc.source_list(notebook_id, skip_freshness=False, drive=True)
        if not r.get("ok"):
            return None
        same = [s for s in (r.get("sources") or []) if _nlm_source_drive_id(s) == str(drive_id or "")]
        if len(same) <= 1:
            return None
        others = [str(s.get("id")) for s in same if str(s.get("id")) != str(new_sid or "")]
        return {"dup_after_add": True, "drive_id": drive_id, "count": len(same),
                "source_ids": [str(s.get("id")) for s in same],
                "fix": ("nlm source delete " + (others[0] if others else "<source_id_cũ>")
                        + " -y   # xác minh title 2 nguồn rồi xóa 1 (giữ bản registry trỏ tới)"),
                "note": "🔴 TRÙNG SAU ADD: cùng drive_id có ≥2 nguồn LIVE — lần add trước có thể client-timeout "
                        "nhưng XONG server-side. Xóa 1 bản rồi `tl nlm-reconcile` link lại registry."}
    except Exception:  # noqa: BLE001 — self-check phụ trợ không được làm hỏng add đã thành công
        return None


def cmd_push_overflow(a) -> int:
    """Sau khi source_add (MCP) văn bản VBQPPL vào shard overflow: cập nhật registry dòng tương ứng
    nlm_notebook_id=<overflow>, row_kind='overflow', nlm_status='pushed', nlm_source_id=<mới>. KHÔNG tự source_add."""
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    nb = getattr(a, "notebook_id", None) or os.environ.get("TL_OVERFLOW_NOTEBOOK_ID") or ""
    if not (a.drive_id and a.source_id and nb):
        print("[tl] push-overflow cần --drive-id --source-id (và overflow notebook trong config hoặc --notebook-id)", file=sys.stderr); return 2
    # v1.34.49 (minor handoff #2): validate nb ∈ shard overflow TOPOLOGY (declared/env/registry) TRƯỚC gate/ghi —
    # chặn ghi row_kind='overflow' cho notebook lạ/nhầm id (registry trỏ notebook ngoài cấu hình = drift khó lần).
    # Bootstrap (topology CHƯA biết shard overflow nào) → cho qua + cảnh báo (không deadlock lần push đầu).
    if not getattr(a, "force_unsafe", False):
        try:
            _ent_po = _manifest_entries(refresh=False)
        except Exception:  # noqa: BLE001 — chưa boot → validate theo config/env
            _ent_po = []
        _base_po = (os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK or "").strip()
        _topo_po = _resolve_shard_topology(_ent_po, _base_po)
        _known_po = {str(s.get("id") or "") for s in (_topo_po.get("shards") or [])} - {_base_po, ""}
        if _known_po and nb not in _known_po:
            print(json.dumps({"ok": False, "error": "TARGET_NOT_IN_TOPOLOGY", "notebook": nb,
                              "known_overflow": sorted(_known_po)[:6],
                              "note": "--notebook-id không thuộc shard overflow topology (config shards[]/env/"
                                      "registry) — chặn ghi nhãn overflow nhầm notebook. Cố ý: --force-unsafe."},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
        if not _known_po:
            print("[tl] ⚠ push-overflow: topology chưa biết shard overflow nào (bootstrap) — tin --notebook-id/config như cũ.",
                  file=sys.stderr)
    g = _gas()
    # v1.29.2 (AUDIT B1 #2): gate + journal + verified-write (trước reg_bulk TRẦN). Sửa luôn rc: trước đòi
    # `patched>0` → chạy LẠI idempotent (giá trị đã đúng, patched=0) bị rc=1 SAI; doctrine v1.28.6: verified
    # (ok + KHÔNG miss) = thành công, patched chỉ thông tin.
    _cols = "nlm_source_id,nlm_notebook_id,row_kind,nlm_status"
    ok_gate, _gv = _apply_gate(a, write_cols=_cols)
    if not ok_gate:
        return 2
    run_id = _apply_journal_start("push-overflow", {"drive_id": a.drive_id, "notebook": nb})
    _items = [{"drive_id": a.drive_id, "nlm_source_id": a.source_id,
               "nlm_notebook_id": nb, "row_kind": "overflow", "nlm_status": "pushed"}]
    v = _journaled_reg_write(run_id, g, _items, _cols,
                             before_by_key=_reg_before_from_manifest(_items, _cols.split(",")))
    rb = v.get("reg_bulk") or {}
    print(json.dumps({"ok": bool(v.get("verified")), "patched": rb.get("patched"), "missed": rb.get("missed"),
                      "journal": run_id, "notebook": nb, "row_kind": "overflow",
                      **({"error": v.get("error")} if v.get("error") else {})}, ensure_ascii=False, indent=2))
    return 0 if v.get("verified") else 1


def cmd_overflow_resolve(a) -> int:
    """KH1 Pha 1.3 (II.1): KIỂM shard overflow SẴN CÓ trước khi nghĩ tới tạo notebook mới. Đếm slot từng shard (registry
    + overflowNotebookId (config/discover) → `_overflow_route`. Cờ OVERFLOW_SHARD_EXISTS_DO_NOT_CREATE khi đã có shard còn
    chỗ. ADVISORY, KHÔNG tạo/ghi gì. (Chống sự cố tạo nhầm 'VBQPPL_overflow_1' rỗng khi VBQPPL-2 đã có chỗ.)"""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:  # noqa: BLE001
        print(f"[tl] overflow-resolve: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    base_nb = os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK
    overflow = (os.environ.get("TL_OVERFLOW_NOTEBOOK_ID") or "").strip()
    discovered = False
    if not overflow or "-" not in overflow:
        overflow = _discover_overflow_from_registry(entries, base_nb); discovered = bool(overflow)
    per = _slot_count_all_shards(entries, base_nb)
    base_reg, ov_reg = per.get(base_nb, 0), (per.get(overflow, 0) if overflow else 0)
    # LIVE physical cross-check (nlm-get) — registry có thể TỤT SAU vật lý (nguồn add thẳng chưa ghi registry).
    # MAX(registry, physical) làm slot hiệu lực → KHÔNG báo "còn chỗ" giả khi vật lý đã vượt cap (vd base 279 reg / 315 live).
    base_phys = ov_phys = None
    _live_read_failed_or = False
    if not getattr(a, "no_live", False):
        try:
            nc = _imp("nlm_cli")
            # v1.34.49 (F-05): đọc CHECKED — {ok:False} KHÔNG thành 0 vật lý (0 giả che gap + shard đầy thành 'trống')
            _bc, _bok, _ = _live_source_count(nc, base_nb, None)
            base_phys = _bc if _bok else None
            _live_read_failed_or = _live_read_failed_or or (not _bok)
            if overflow:
                _oc, _ook, _ = _live_source_count(nc, overflow, None)
                ov_phys = _oc if _ook else None
                _live_read_failed_or = _live_read_failed_or or (not _ook)
        except Exception:
            base_phys = ov_phys = None
            _live_read_failed_or = True
    st = _overflow_status(base_reg, base_phys, overflow, ov_reg, ov_phys)
    out = {"ok": True, "gate": "overflow-resolve", "base_notebook": base_nb,
           "base_used": st["base_used"], "base_registry": base_reg, "base_physical": base_phys,
           "overflow_shard": overflow or None, "overflow_discovered_from_registry": discovered,
           "overflow_used": st["overflow_used"], "overflow_registry": ov_reg, "overflow_physical": ov_phys,
           "cap": NLM_SLOT_CAP, "route": st["route"], "decision_flag": st["flag"], "reason": st["reason"],
           "used_basis": "max(registry, physical-nlm-get)", "registry_live_gap": st["registry_live_gap"],
           "note": "ADVISORY — KHÔNG tạo notebook. Chỉ `notebook create` khi MỌI shard đầy LIVE + người dùng duyệt."}
    if _live_read_failed_or:
        out["live_read_failed"] = True
        out["live_note"] = "KHÔNG đọc được live source_count (auth/mạng) — route chỉ dựa registry, KHÔNG suy 0 vật lý (F-05). `nlm login` rồi chạy lại để đối chiếu LIVE."
    if st["registry_live_gap"]:
        out["warning"] = "REGISTRY_BEHIND_LIVE: có nguồn vật lý CHƯA đăng ký registry → chạy `tl nlm-reconcile <notebook> --apply` để khớp LIVE TRƯỚC khi nạp thêm."
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        _bp = f" (LIVE {base_phys})" if base_phys is not None else " (registry-only — chạy với nlm để đối chiếu LIVE)"
        print(f"== overflow-resolve · base={base_nb[:12]} {st['base_used']}/{NLM_SLOT_CAP}{_bp} · "
              f"overflow={overflow or '(chưa có)'} {st['overflow_used']}/{NLM_SLOT_CAP} ==")
        print(f"  route={st['route']} | {st['flag']} | {st['reason']}")
        if st["registry_live_gap"]:
            for g in st["registry_live_gap"]:
                print(f"  ⚠ REGISTRY_BEHIND_LIVE [{g['shard']}]: registry {g['registry']} < vật lý {g['physical']} (+{g['gap']}) "
                      f"→ `tl nlm-reconcile` đăng ký nguồn lạc TRƯỚC khi nạp.")
        if st["flag"] == "OVERFLOW_SHARD_EXISTS_DO_NOT_CREATE":
            print("  ✓ base ĐẦY nhưng có shard overflow còn chỗ → DÙNG shard này, ĐỪNG tạo notebook mới.")
        elif st["flag"] == "ALL_SHARDS_FULL_ASK_USER_BEFORE_CREATE":
            print("  ⚠ MỌI shard đầy → HỎI người dùng duyệt tạo shard mới (KHÔNG auto-create).")
    return 0


def _nlm_source_drive_id(s: dict) -> str:
    """C1 (log rà): trích Drive fileId mà 1 NLM drive-source trỏ tới — field trực tiếp HOẶC parse từ URL Google Docs."""
    for k in ("drive_id", "driveId", "document_id", "documentId", "file_id", "fileId", "sourceFileId"):
        v = str(s.get(k) or "").strip()
        if v and re.fullmatch(r"[A-Za-z0-9_\-]{20,}", v):
            return v
    url = str(s.get("url") or s.get("source_url") or s.get("link") or "")
    m = re.search(r"/d/([A-Za-z0-9_\-]{20,})", url) or re.search(r"[?&]id=([A-Za-z0-9_\-]{20,})", url)
    return m.group(1) if m else ""


def _nlm_reconcile_plan(live_sources, entries: list, notebook_id: str) -> dict:
    """PURE: phân loại registry rows so với ground-truth live của notebook.
       backfill        = có nlm_source_id ∈ live nhưng nlm_notebook_id != notebook;
       desync_real     = có nlm_source_id ∉ live VÀ status pushed/synced/… (claims trên NLM nhưng VẮNG) — cần xử lý;
       already_removed = có nlm_source_id ∉ live nhưng status `removed*` (đã gỡ CÓ CHỦ ĐÍCH) — KHÔNG phải lỗi, chỉ báo;
       link_candidates = (C1) nguồn live KHÔNG khớp source_id nào NHƯNG bắc cầu được qua Drive fileId / số hiệu sang
                         1 dòng registry (registry khóa drive_id ≠ NLM khóa source_id) → backfill nlm_source_id;
       unregistered    = live id không link được dòng nào (NLM có, registry thực sự thiếu);
       foreign_skipped = (v1.34.53 A2) live id match được dòng registry NHƯNG dòng đã trỏ notebook KHÁC →
                         KHÔNG BAO GIỜ ghi (ownership guard — chống clobber con trỏ chéo shard), chỉ báo cáo.
       v1.19.9: tách already_removed khỏi desync_real. C1: chấp nhận live_sources = list[dict] (mới) hoặc set ids (cũ)."""
    if isinstance(live_sources, (set, frozenset)):
        sources = [{"id": x} for x in live_sources]
    else:
        sources = list(live_sources or [])
    live_ids = {str(s.get("id")) for s in sources if s.get("id")}
    reg_ids = set()
    by_drive: dict[str, list] = {}   # v1.34.53 (A2): LIST — dòng dual-registered (cùng drive_id, 2 notebook) phải lọc theo chủ quyền, không lấy dòng-đầu mù
    by_sohieu: dict[str, dict] = {}
    n_rows, backfill, desync_real, already_removed, other_notebook = 0, [], [], [], []
    settle_confirm = []   # F3 r191: dòng deferred (no-wait/defer) mà sid NAY THẤY live → nâng pushed
    for e in entries:
        did = _entry_drive_id(e)
        if did:
            by_drive.setdefault(did, [])
            if e not in by_drive[did]:
                by_drive[did].append(e)
        shk = _sohieu_key_entry(e)
        if shk:
            by_sohieu.setdefault(shk, []).append(e)   # LIST: số hiệu VBHN có thể tái dùng → KHÔNG link nếu >1
        sid = (_entry_nlm(e) or "").strip()
        if not sid:
            continue
        reg_ids.add(sid); n_rows += 1
        nb = str(e.get("nlm_notebook_id") or "").strip()
        if sid in live_ids:
            if nb != notebook_id:
                backfill.append(e)
            elif str(e.get("nlm_status") or "").strip().lower() == "deferred":
                # F3 r191: 'đã gửi, chưa xác minh settle' mà nguồn NAY có mặt live đúng notebook →
                # xác minh xong, nâng deferred→pushed (CHỈ nlm_status — corpus KHÔNG auto-true).
                settle_confirm.append(e)
        elif nb and nb != notebook_id:
            other_notebook.append(e)   # v1.19.11: thuộc shard/notebook KHÁC (vd overflow VBQPPL-2) → KHÔNG phải desync
        else:
            st = str(e.get("nlm_status") or "").strip().lower()
            (already_removed if st.startswith("removed") else desync_real).append(e)
    # C1: bắc cầu gdoc↔source_id cho nguồn live 'chưa đăng ký' (id KHÔNG ∈ reg_ids).
    # v1.34.27 #4 (log phiên nạp 4 file): nguồn add qua `nlm source add --drive` KHÔNG phơi url/drive_id
    # trong source_list → tier drive_id MISS; văn bản thường không số hiệu → tier sohieu MISS → báo
    # unregistered OAN dù registry đã có dòng đúng drive_id. Thêm TIER 3 EXACT-TITLE duy nhất (chuẩn hoá
    # _ingest_dedup_title_key — cùng khoá dedup-live S13; title do CHÍNH tool đặt khi add = định danh mạnh).
    by_title: dict[str, list] = {}
    for e in entries:
        for _tt in (str(e.get("name") or ""), str(e.get("nlm_title") or "")):
            _tk = _ingest_dedup_title_key(_tt)
            if _tk:
                by_title.setdefault(_tk, [])
                if e not in by_title[_tk]:
                    by_title[_tk].append(e)
    # v1.34.53 (A2 — log phiên 80742228: reconcile profile-notebook match TRIPS/WCT theo title rồi PATCH
    # nlm_notebook_id của dòng corpus VBQPPL-2 sang notebook đang reconcile → dòng corpus trỏ SAI shard, phải
    # reconcile lại đúng shard mới nắn về): OWNERSHIP GUARD — dòng registry đã trỏ notebook KHÁC không bao giờ
    # thành link candidate (mọi tier, kể cả drive_id: ca dual-registered là CÓ CHỦ ĐÍCH — v1.34.51); tier YẾU
    # (sohieu/title) chỉ được link dòng CHƯA có nlm_source_id (không re-point con trỏ sẵn có bằng định danh yếu).
    def _ent_foreign(_e: dict) -> bool:
        _nb = str(_e.get("nlm_notebook_id") or "").strip()
        return bool(_nb) and _nb != str(notebook_id)
    link_candidates, still_unreg, foreign_skipped = [], [], []
    for s in sources:
        sid = str(s.get("id") or "")
        if not sid or sid in reg_ids:
            continue
        _foreign_hit = None   # ent foreign đầu tiên bị guard chặn (để báo cáo, KHÔNG ghi)
        did = _nlm_source_drive_id(s)
        _dcands = (by_drive.get(did) or []) if did else []
        _down = [e for e in _dcands if not _ent_foreign(e)]
        if _dcands and not _down:
            _foreign_hit = (_dcands[0], "drive_id")
        ent = _down[0] if len(_down) == 1 else None   # >1 dòng own cùng drive_id = mơ hồ → bỏ qua
        by = "drive_id"
        if ent is None:
            shk = _sohieu_key_entry({"name": s.get("title") or "", "so_hieu": s.get("sohieu") or s.get("so_hieu") or ""})
            _cands = by_sohieu.get(shk) or [] if shk else []
            _own = [e for e in _cands if not _ent_foreign(e) and not (_entry_nlm(e) or "").strip()]
            if _cands and not _own and _foreign_hit is None and any(_ent_foreign(e) for e in _cands):
                _foreign_hit = (next(e for e in _cands if _ent_foreign(e)), "sohieu")
            ent = _own[0] if len(_own) == 1 else None   # CHỈ link theo số hiệu khi DUY NHẤT (tránh false-link reuse)
            by = "sohieu"
        if ent is None:
            _tk = _ingest_dedup_title_key(str(s.get("title") or ""))
            _tcands = by_title.get(_tk) or [] if _tk else []
            _town = [e for e in _tcands if not _ent_foreign(e) and not (_entry_nlm(e) or "").strip()]
            if _tcands and not _town and _foreign_hit is None and any(_ent_foreign(e) for e in _tcands):
                _foreign_hit = (next(e for e in _tcands if _ent_foreign(e)), "title")
            ent = _town[0] if len(_town) == 1 else None  # tier 3: title CHUẨN HOÁ duy nhất mới link
            by = "title"
        if ent is not None and (_entry_nlm(ent) or "").strip() != sid:
            link_candidates.append({"entry": ent, "source_id": sid, "by": by, "title": s.get("title") or ""})
        else:
            if _foreign_hit is not None:
                foreign_skipped.append({"source_id": sid, "by": _foreign_hit[1], "title": s.get("title") or "",
                                        "registry_notebook": str(_foreign_hit[0].get("nlm_notebook_id") or ""),
                                        "drive_id": _entry_drive_id(_foreign_hit[0])})
            still_unreg.append(sid)
    return {"backfill": backfill, "desync_real": desync_real, "already_removed": already_removed,
            "other_notebook": other_notebook,
            "foreign_skipped": foreign_skipped,   # v1.34.53 (A2): match được NHƯNG dòng thuộc notebook khác → KHÔNG ghi, chỉ báo
            "stale": desync_real,  # giữ khóa cũ = desync_real (tương thích ngược)
            "link_candidates": link_candidates,
            "settle_confirm": settle_confirm,   # F3 r191: deferred + sid live đúng notebook → nâng pushed
            "unregistered": sorted(still_unreg),
            "registry_on_nlm_rows": n_rows}


# FIX-C r201 (grill 24-07 đêm C2 — ca sống «300 unregistered» phiên Chat): kênh liệt kê NLM suy hoá
# (3 kênh chết) trả id lạc namespace → ~100% nguồn live thành 'unregistered' mà reconcile IM LẶNG;
# --apply mù theo đó link/clear bậy hàng loạt. Ngưỡng 50% xa mọi ca lành (máy khỏe đo 2/300 = 0,7%);
# sàn live ≥ 20 tránh kích oan notebook nhỏ/mới. HẰNG re-export tl.py (bẫy I11).
_RECONCILE_SUSPECT_MIN_LIVE = 20
_RECONCILE_SUSPECT_UNREG_RATIO = 0.5


def _reconcile_channel_suspect(live_n: int, unreg_n: int) -> bool:
    """PURE (FIX-C r201): True khi tỷ lệ 'unregistered'/live vượt ngưỡng nghi-kênh — dấu hiệu kênh
    liệt kê trả dữ liệu sai namespace, KHÔNG phải registry lệch thật."""
    return live_n >= _RECONCILE_SUSPECT_MIN_LIVE and unreg_n > live_n * _RECONCILE_SUSPECT_UNREG_RATIO


def cmd_nlm_reconcile(a) -> int:
    """C (WS1): đối soát registry↔NLM bằng ground-truth từ CLI nlm. Backfill nlm_notebook_id cho dòng
    THỰC SỰ trên NLM; báo (và --clear-stale thì clear) dòng 'pushed' nhưng KHÔNG trên NLM. DRY mặc định.
    v1.34.34 --all-notebooks: quét base + overflow shard 1 lệnh (DRY — thực chứng 2026-07-12: nguồn nạp vào
    overflow lọt lưới reconcile mặc định). Tái dùng chính hàm này per-notebook (capture JSON), gộp báo cáo."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    # v1.34.43 (hoàn tất BUG2 v1.34.42 — ops-sweep dogfood bắt): `--refresh` cần creds LIVE (TL_WEBAPP) để fetch
    # manifest, mà apply_profile_offline KHÔNG đảm bảo có → trước đây `nlm-reconcile --refresh` chết 'Thiếu TL_WEBAPP'
    # (khuôn load_creds-on-refresh của reg-query/locate/status đã có, nlm-reconcile BỎ SÓT). Nạp ở ĐẦU hàm phủ CẢ
    # plain lẫn --all-notebooks (self-heal từ config). TL_WEBAPP cho GAS/registry; NLM cookie riêng.
    if getattr(a, "refresh", False):
        try:
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        except (SystemExit, Exception):  # noqa: BLE001 — thiếu creds → rơi xuống thông điệp NEEDS_BOOT bên dưới
            pass
    if getattr(a, "all_notebooks", False):
        import argparse as _ap, io as _io, contextlib as _ctx
        _blocked_apply = getattr(a, "apply", False) or getattr(a, "clear_stale", False)
        # v1.34.42 (BUG1): đảm bảo manifest cache MỘT LẦN trước vòng lặp — self-heal khi có creds (load_creds đã nạp
        # ở đầu hàm khi --refresh; v1.34.43), báo NEEDS_BOOT_PROFILE RÕ khi không, thay vì để mỗi inner reconcile fail
        # rc=2 (in stderr, bị nuốt khỏi per_notebook) rồi note khẳng định 'sạch' oan.
        if not getattr(a, "refresh", False):   # --refresh đã nạp creds ở đầu hàm; nếu không, thử nạp cho self-heal cache
            try:
                load_creds(getattr(a, "config", None), getattr(a, "profile", None))
            except (SystemExit, Exception):  # noqa: BLE001 — load_creds có thể sys.exit khi thiếu cred; không giết audit
                pass
        _ent = []
        try:
            _ent = _manifest_entries(refresh=getattr(a, "refresh", False))
        except Exception:  # noqa: BLE001 — chưa có cache → thử build 1 lần (cần creds LIVE)
            try:
                _ent = _manifest_entries(refresh=True)
            except Exception as _me0:  # noqa: BLE001
                print(json.dumps({"ok": False, "error": "NEEDS_BOOT_PROFILE", "detail": str(_me0),
                                  "note": "Chạy `tl --profile <P> boot` (hoặc `boot --refresh`) trước "
                                          "`nlm-reconcile --all-notebooks` — chưa có manifest cache cho scope này."},
                                 ensure_ascii=False), file=sys.stderr)
                return 2
        _base, _nberr0 = _resolve_nlm_notebook(getattr(a, "notebook_id", None))
        if _nberr0:
            print(json.dumps({"ok": False, "error": _nberr0}, ensure_ascii=False), file=sys.stderr); return 2
        # v1.34.47 (B1 fix): resolve MỌI shard overflow từ env + REGISTRY (đối xứng đường ghi/định-tuyến).
        # Trước đây chỉ đọc env → config trống ⇒ chỉ quét base ⇒ _reconcile_sweep_note báo 'mọi notebook
        # SẠCH' oan trên shard chưa quét ('sai mà báo thành công'). Nay quét đủ shard registry-biết.
        _shards = _resolve_overflow_shards(_ent, _base)
        _nbs = [_base] + [s for s in _shards if s != _base]
        _prof_pfx = f"tl --profile {_active_profile()} " if _active_profile() != DEFAULT_PROFILE else "tl "
        _apply_cmds = [f"{_prof_pfx}nlm-reconcile {_n} --apply --from-plan" for _n in _nbs]
        if _blocked_apply:
            # v1.34.54 (A3/Q7=b — grill: 'chặn nhưng thông báo mơ hồ, docs lệch'): GIỮ DRY-only (apply diện rộng
            # 1 lệnh đi ngược nếp apply-per-scope) nhưng thông báo ACTIONABLE — in sẵn lệnh per-notebook đúng
            # profile, đúng thứ tự base→overflow, copy-paste được. --from-plan tái dùng plan sweep vừa ghi.
            print(json.dumps({"ok": False, "error": "ALL_NOTEBOOKS_IS_DRY_ONLY",
                              "notebooks": _nbs, "run_per_notebook": _apply_cmds,
                              "note": "--all-notebooks chỉ QUÉT (DRY) — chạy sweep DRY trước (ghi plan-artifact) "
                                      "rồi apply per-notebook bằng các lệnh trên (--from-plan bỏ re-scan; bỏ "
                                      "--from-plan nếu muốn re-scan tươi)."}, ensure_ascii=False, indent=2),
                  file=sys.stderr)
            return 2
        _per, _all_ok = [], True
        for _nb_i in _nbs:
            _buf = _io.StringIO()
            _ns_i = _ap.Namespace(config=getattr(a, "config", None), profile=getattr(a, "profile", None),
                                  notebook_id=_nb_i, apply=False, clear_stale=False,
                                  force_unsafe=getattr(a, "force_unsafe", False),
                                  refresh=getattr(a, "refresh", False), json=True, out=None, all_notebooks=False,
                                  plan_out=str(HERE / ".tl_state" / f"reconcile_plan_{_nb_i}.json"))
            try:
                with _ctx.redirect_stdout(_buf):
                    _rc_i = cmd_nlm_reconcile(_ns_i)
                _r_i = json.loads(_buf.getvalue() or "{}")
            except Exception as _e_i:  # noqa: BLE001
                _rc_i, _r_i = 1, {"ok": False, "error": f"{type(_e_i).__name__}: {_e_i}"}
            _all_ok = _all_ok and (_rc_i == 0) and bool(_r_i.get("ok"))
            _per.append({"notebook": _nb_i, "rc": _rc_i,
                         **{k: _r_i.get(k) for k in ("ok", "live_on_nlm", "desync_real", "unregistered_on_nlm",
                                                     "link_candidates", "backfill_nlm_notebook_id",
                                                     "already_removed", "error",
                                                     "verdict") if k in _r_i}})   # verdict: FIX-C r201 nổi lên sweep
            print(f"[reconcile] {_nb_i[:8]}…: desync={_r_i.get('desync_real')} unregistered="
                  f"{_r_i.get('unregistered_on_nlm')} link_candidates={_r_i.get('link_candidates')}",
                  file=sys.stderr, flush=True)
        # v1.34.50: `clean` = tín hiệu MÁY trung thực (all_ok VÀ 0 finding) — orchestrator kiểm `clean` KHÔNG chỉ
        # `ok` (ok=DRY-scan-chạy-được, giữ rc=0 theo doctrine A3; clean=không-lệch). note = tín hiệu NGƯỜI.
        _sweep_clean = _reconcile_sweep_clean(_all_ok, _per)
        _out_all = {"ok": _all_ok, "clean": _sweep_clean, "mode": "DRY", "all_notebooks": True,
                    "notebooks_swept": len(_nbs), "per_notebook": _per,
                    "plan_artifacts": [str(HERE / ".tl_state" / f"reconcile_plan_{_n}.json") for _n in _nbs],
                    "apply_commands": _apply_cmds,   # v1.34.54 A3: copy-paste per-notebook (--from-plan bỏ re-scan)
                    "note": _reconcile_sweep_note(_all_ok, _per)}   # v1.34.42/50 (BUG1): note ĐIỀU KIỆN, hết 'sạch' oan
        _o = getattr(a, "out", None)
        if _o:
            Path(_o).write_text(json.dumps(_out_all, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8", newline="\n")
            print(json.dumps({"ok": _all_ok, "out": _o, "notebooks_swept": len(_nbs)}, ensure_ascii=False))
        else:
            print(json.dumps(_out_all, ensure_ascii=False, indent=1))
        return 0 if _all_ok else 1
    nb, _nberr = _resolve_nlm_notebook(getattr(a, "notebook_id", None))
    if _nberr:
        print(json.dumps({"ok": False, "error": _nberr}, ensure_ascii=False), file=sys.stderr); return 2
    # v1.34.54 (A3/Q7b — 'lần 2 phải nhanh hơn sau DRY'): --apply --from-plan [path] nạp PLAN ARTIFACT sweep DRY
    # vừa ghi → BỎ re-scan (source_list NLM + manifest refresh = phần đắt nhất); an toàn bằng TTL 15' + freshness
    # reg_get_bulk trên ĐÚNG các dòng sắp ghi (dòng đổi so plan → DROP, báo cáo — không ghi mù theo plan cũ).
    _from_plan = None
    _fp_arg = getattr(a, "from_plan", None)
    if _fp_arg is not None and getattr(a, "apply", False):
        if getattr(a, "clear_stale", False):
            print(json.dumps({"ok": False, "error": "FROM_PLAN_NO_CLEAR_STALE",
                              "note": "--clear-stale đòi trạng thái LIVE tươi — chạy không --from-plan."},
                             ensure_ascii=False), file=sys.stderr)
            return 2
        _fp = _fp_arg if str(_fp_arg) not in ("", "auto") else str(HERE / ".tl_state" / f"reconcile_plan_{nb}.json")
        try:
            _art = json.loads(Path(_fp).read_text(encoding="utf-8"))
        except Exception as _fpe:  # noqa: BLE001
            print(json.dumps({"ok": False, "error": "PLAN_NOT_FOUND", "path": str(_fp), "detail": str(_fpe),
                              "note": "Chạy `tl nlm-reconcile --all-notebooks` (DRY, ghi plan) trước; hoặc bỏ "
                                      "--from-plan để re-scan tươi."}, ensure_ascii=False), file=sys.stderr)
            return 2
        import time as _t54
        _age_s = _t54.time() - float(_art.get("created_ts") or 0)
        if _art.get("schema") != "reconcile_plan.v1" or str(_art.get("notebook")) != str(nb):
            print(json.dumps({"ok": False, "error": "PLAN_MISMATCH", "path": str(_fp),
                              "plan_notebook": _art.get("notebook"), "notebook": nb}, ensure_ascii=False),
                  file=sys.stderr)
            return 2
        if _age_s > 900:
            print(json.dumps({"ok": False, "error": "PLAN_STALE", "age_s": round(_age_s), "ttl_s": 900,
                              "note": "Plan quá 15' — chạy lại sweep DRY (hoặc bỏ --from-plan)."},
                             ensure_ascii=False), file=sys.stderr)
            return 2
        _from_plan = {"path": str(_fp), "age_s": round(_age_s, 1), "art": _art}
    if _from_plan is None:
        try:
            nc = _imp("nlm_cli")
            live = nc.source_list(nb, skip_freshness=True)
        except Exception as e:
            print(json.dumps({"ok": False, "error": f"nlm_cli lỗi: {e}"}, ensure_ascii=False), file=sys.stderr); return 2
        if not live.get("ok"):
            # v1.34.61 (E2 — ADR-3): --apply + NLM hard-dead → DEFER rc=0 (KHÔNG ghi trên belief —
            # physical-first), trỏ đường A3: plan-artifact sweep DRY còn tươi (≤15') thì --from-plan, không
            # thì chạy lại khi NLM sống. DRY + dead GIỮ rc=2 — reconcile là VERIFY-TOOL, không live thì
            # không kết luận (unverified-continue của E2 nằm ở nlm-audit-physical, không phải đây).
            _v62r = _nlm_or_corpus("nlm-reconcile", a, notebook_id=nb, err=live)
            if _v62r["route"] == "unverified" and getattr(a, "apply", False):
                _fp62 = HERE / ".tl_state" / f"reconcile_plan_{nb}.json"
                _art62 = None
                try:
                    _a62 = json.loads(_fp62.read_text(encoding="utf-8"))
                    _age62 = round(time.time() - float(_a62.get("created_ts") or 0))
                    _art62 = {"path": str(_fp62), "age_s": _age62, "fresh": _age62 <= 900}
                except Exception:  # noqa: BLE001 — chưa có plan-artifact → chỉ hướng dẫn chạy lại
                    pass
                print(json.dumps({"ok": True, "mode": "DEFERRED_NLM_OFFLINE", "nlm_status": "offline",
                                  "fallback": "deferred", "notebook": nb, "applied": 0,
                                  "why": _v62r["why"][:120],
                                  **({"plan_artifact": _art62} if _art62 else {}),
                                  "note": "NLM offline → KHÔNG ghi registry trên belief (physical-first). "
                                          "Khi NLM sống: chạy lại lệnh này; plan-artifact A3 còn tươi (≤15') "
                                          f"thì `tl nlm-reconcile {nb} --apply --from-plan` (bỏ re-scan)."},
                                 ensure_ascii=False, indent=2))
                return 0
            print(json.dumps({**live, "note": "fallback: MCP notebook_get hoặc `nlm login`"}, ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
        live_ids = {s.get("id") for s in live["sources"] if s.get("id")}
        try:
            entries = _manifest_entries(refresh=getattr(a, "refresh", False))
        except Exception as e:
            print(f"[tl] nlm-reconcile: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
        plan = _nlm_reconcile_plan(live.get("sources") or list(live_ids), entries, nb)
        # v1.29.7 (log NĐ131 #5): nguồn vừa thêm qua nlm-add báo 'unregistered' oan vì manifest CACHE CŨ (row registry
        # đã có nhưng chưa vào cache) → bắc-cầu drive_id không thấy entry. SELF-HEAL: có unregistered mà chưa refresh
        # → tự refresh manifest 1 LẦN + re-plan (nhiều ca unregistered → link_candidates ngay, --apply backfill được).
        if plan["unregistered"] and not getattr(a, "refresh", False):
            print(f"[tl] {len(plan['unregistered'])} nguồn 'unregistered' + manifest chưa refresh → tự refresh + đối soát lại "
                  f"(row vừa ingest thường chỉ thiếu trong cache)…", file=sys.stderr, flush=True)
            try:
                entries = _manifest_entries(refresh=True)
                plan = _nlm_reconcile_plan(live.get("sources") or list(live_ids), entries, nb)
            except Exception as _re:  # noqa: BLE001
                print(f"[tl] ⚠ refresh manifest lỗi ({_re}) — dùng plan cũ.", file=sys.stderr, flush=True)
    else:
        live_ids = set()
        try:
            entries = _manifest_entries(refresh=False)   # cache LOCAL (rẻ) — chỉ cho topology row_kind bên dưới
        except Exception:  # noqa: BLE001
            entries = []
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        g0 = _gas()
        _artd = _from_plan["art"]
        _rows_ln, _rows_bf = list(_artd.get("link_candidates") or []), list(_artd.get("backfill") or [])
        _dids54 = [r.get("drive_id") for r in (_rows_ln + _rows_bf) if r.get("drive_id")]
        _dropped54 = []
        if _dids54:
            try:
                _rgb54 = g0.get("reg_get_bulk", keys=json.dumps(_dids54), key_field="drive_id")
            except Exception as _rge54:  # noqa: BLE001
                _rgb54 = {"ok": False, "error": str(_rge54)}
            if not _rgb54.get("ok"):
                print(json.dumps({"ok": False, "error": "FRESHNESS_CHECK_FAILED", "detail": _rgb54.get("error"),
                                  "note": "Không đọc được registry để đối chiếu plan — DỪNG (bỏ --from-plan để "
                                          "re-scan, hoặc thử lại)."}, ensure_ascii=False), file=sys.stderr)
                return 2
            _cur_by_did = {str((r or {}).get("drive_id") or ""): (r or {}) for r in (_rgb54.get("rows") or []) if r}
            def _fresh_ln(r):
                _cur = _cur_by_did.get(str(r.get("drive_id")))
                _sid = str((_cur or {}).get("nlm_source_id") or "").strip()
                _cnb = str((_cur or {}).get("nlm_notebook_id") or "").strip()
                return _cur is not None and (not _sid or _sid == str(r.get("source_id"))) and (not _cnb or _cnb == str(nb))
            def _fresh_bf(r):
                _cur = _cur_by_did.get(str(r.get("drive_id")))
                return _cur is not None and str((_cur or {}).get("nlm_source_id") or "").strip() == str(r.get("nlm_source_id"))
            _keep_ln = [r for r in _rows_ln if _fresh_ln(r)]
            _keep_bf = [r for r in _rows_bf if _fresh_bf(r)]
            _dropped54 = ([{"drive_id": r.get("drive_id"), "kind": "link", "reason": "CHANGED_SINCE_PLAN"}
                           for r in _rows_ln if r not in _keep_ln]
                          + [{"drive_id": r.get("drive_id"), "kind": "backfill", "reason": "CHANGED_SINCE_PLAN"}
                             for r in _rows_bf if r not in _keep_bf])
            _rows_ln, _rows_bf = _keep_ln, _keep_bf
        plan = {"backfill": _rows_bf, "desync_real": [], "already_removed": [], "other_notebook": [],
                "foreign_skipped": [], "stale": [], "unregistered": [], "registry_on_nlm_rows": None,
                "settle_confirm": [],   # F3 r191: đường from-plan không re-scan live → không phân xử deferred
                "link_candidates": [{"entry": r, "source_id": r.get("source_id"), "by": r.get("by") or "plan",
                                     "title": r.get("name") or ""} for r in _rows_ln]}
        print(f"[tl] nlm-reconcile --from-plan: {_from_plan['path']} (tuổi {_from_plan['age_s']}s) — "
              f"link={len(_rows_ln)} backfill={len(_rows_bf)} dropped={len(_dropped54)} (bỏ re-scan NLM).",
              file=sys.stderr, flush=True)
    from collections import Counter as _Counter
    rm_by_status = dict(_Counter(str(e.get("nlm_status") or "").strip().lower() for e in plan["already_removed"]))
    out = {"ok": True, "notebook": nb, "live_on_nlm": len(live_ids),
           "registry_rows_claiming_nlm": plan["registry_on_nlm_rows"],
           "backfill_nlm_notebook_id": len(plan["backfill"]),
           "desync_real": len(plan["desync_real"]),          # status pushed/synced nhưng VẮNG NLM — đáng xử lý
           "already_removed": len(plan["already_removed"]),  # status removed* — đã gỡ có chủ đích, KHÔNG phải lỗi
           "already_removed_by_status": rm_by_status,
           "other_notebook": len(plan.get("other_notebook") or []),  # thuộc shard/notebook khác (overflow) — không tính desync
           "link_candidates": len(plan.get("link_candidates") or []),  # C1: nguồn live bắc cầu được sang registry (chỉ thiếu source_id)
           "settle_confirm": len(plan.get("settle_confirm") or []),  # F3 r191: deferred + sid live → nâng pushed khi --apply
           "foreign_skipped": len(plan.get("foreign_skipped") or []),  # v1.34.53 (A2): match dòng notebook KHÁC → guard chặn ghi, chỉ báo
           "unregistered_on_nlm": len(plan["unregistered"]),
           "mode": "APPLY" if getattr(a, "apply", False) else "DRY",
           "backfill_sample": [f"{_entry_nlm(e)}|{_entry_sohieu(e) or _sohieu_key_entry(e)}|{_entry_name(e)[:40]}" for e in plan["backfill"][:10]],
           "link_candidates_sample": [f"{c['source_id'][:12]}…→{_entry_drive_id(c['entry'])[:12]}… (by {c['by']}) | {(_entry_sohieu(c['entry']) or _entry_name(c['entry'])[:32])}" for c in (plan.get("link_candidates") or [])[:10]],
           "desync_real_sample": [f"{_entry_sohieu(e)}|{_entry_name(e)[:40]}" for e in plan["desync_real"][:10]],
           "foreign_skipped_sample": [f"{c['source_id'][:12]}…↛{(c.get('registry_notebook') or '?')[:12]}… (by {c['by']}) | {str(c.get('title') or '')[:32]}" for c in (plan.get("foreign_skipped") or [])[:10]],
           "unregistered_sample": plan["unregistered"][:8]}
    # FIX-C r201 (grill C2): guard nghi-kênh — live ≥ 20 VÀ unregistered/live > 50% ⇒ dữ liệu liệt kê
    # KHÔNG đáng tin. DRY vẫn in report (verdict trong out) + banner LOUD + playbook; --apply DỪNG rc=2
    # TRƯỚC mọi ghi (chốt đặt sau nhánh DRY, trước preflight/gate/journal); override --force-unsafe.
    # Đường --from-plan không re-scan live (live_ids rỗng, unregistered rỗng) → guard bất hoạt by design.
    _suspect_c2 = _reconcile_channel_suspect(len(live_ids), len(plan["unregistered"]))
    if _suspect_c2:
        out["verdict"] = "LISTING_CHANNEL_SUSPECT"
        out["verdict_note"] = (f"unregistered {len(plan['unregistered'])}/{len(live_ids)} live "
                               f"(>{int(_RECONCILE_SUSPECT_UNREG_RATIO * 100)}%, live≥"
                               f"{_RECONCILE_SUSPECT_MIN_LIVE}) — nghi KÊNH LIỆT KÊ NLM suy hoá trả id "
                               "lạc namespace, KHÔNG phải registry lệch thật. ĐỪNG tin plan này.")
        print(f"[tl] 🛑🛑 LISTING_CHANNEL_SUSPECT: {len(plan['unregistered'])}/{len(live_ids)} nguồn live "
              "bị coi là 'unregistered' — kênh liệt kê NLM khả nghi (đã từng thấy 3 kênh chết trả id lạc "
              "namespace).", file=sys.stderr)
        print("[tl]    playbook: (1) đổi kênh liệt kê / `tl nlm-auth-status` soi 3 kênh; (2) `nlm login` "
              "làm tươi cookie; (3) đo lại trên máy khỏe rồi so verdict. --apply bị CHẶN rc=2 trước mọi "
              "ghi (override tường minh: --force-unsafe).", file=sys.stderr)
    if _from_plan is None:
        # r179 T8 (ADR-0010 — «CẢ HAI lệnh in CẢ HAI số, tên tường minh»): reconcile có live-set per-source →
        # coverage_gap CHÍNH XÁC = dòng nlm_due (diện phải-có: corpus∪ref, trừ removed_*) mà nguồn VẮNG live.
        # removed_family_still_live giải thích chênh đếm với slot-audit (đo 21-07: 11 dòng removed_from_drive
        # nguồn còn sống = trọn desync_estimate +11 của slot-audit — hai lệnh 51/40 KHÔNG mâu thuẫn).
        _due179 = _nlm_due_rows(entries, nb, None)
        _live179 = {str(x) for x in (live_ids or set())}
        _cov179 = [e for e in _due179 if str(_entry_nlm(e) or "").strip() not in _live179]
        _rmlive179 = [e for e in (entries or [])
                      if _nlm_status_removed(str(e.get("nlm_status") or ""))
                      and str(_entry_nlm(e) or "").strip() in _live179 and str(_entry_nlm(e) or "").strip()]
        out["nlm_due_rows"] = len(_due179)
        out["coverage_gap"] = len(_cov179)
        if _cov179:
            out["coverage_gap_sample"] = [f"{_entry_sohieu(e) or _sohieu_key_entry(e)}|{_entry_name(e)[:40]}"
                                          for e in _cov179[:10]]
        out["removed_family_still_live"] = len(_rmlive179)
        if _rmlive179:
            out["removed_family_still_live_sample"] = [_entry_name(e)[:44] for e in _rmlive179[:10]]
        out["labels_note"] = ("coverage_gap = nlm_due (diện PHẢI-CÓ-MẶT: corpus∪ref, trừ removed_*) có nguồn "
                              "VẮNG live — nợ phủ (slot-audit chủ trì, đây là bản per-source). desync_real = "
                              "nlm_claim (sổ KHẲNG ĐỊNH có mặt) nhưng VẮNG live — reconcile chủ trì. Hai phép đo "
                              "trả lời hai câu hỏi KHÁC nhau — lệch số không phải mâu thuẫn (ADR-0010).")
    if _from_plan is not None:   # v1.34.54 A3: chỉ số live lấy từ artifact (run này KHÔNG gọi NLM)
        out["live_on_nlm"] = _from_plan["art"].get("live_on_nlm")
        out["from_plan"] = {"path": _from_plan["path"], "age_s": _from_plan["age_s"],
                            "dropped": _dropped54, "note": "re-scan NLM đã bỏ — freshness check reg_get_bulk trên dòng sắp ghi"}
    if not getattr(a, "apply", False):
        out["note"] = ("DRY. --apply: reg_bulk nlm_notebook_id cho backfill + LINK nlm_source_id cho link_candidates "
                       "(bắc cầu gdoc↔source_id). --clear-stale: CHỈ clear desync_real (status pushed/synced nhưng vắng "
                       "NLM); KHÔNG đụng already_removed (đã gỡ có chủ đích).")
        _plan_out = getattr(a, "plan_out", None)
        if _plan_out:
            # v1.34.54 (A3 — yêu cầu hiệu năng Q7b: 'lần apply sau phải nhanh hơn sau khi đã DRY'): ghi PLAN
            # ARTIFACT đủ dữ liệu ghi (slim rows) để `--apply --from-plan` BỎ re-scan (source_list + manifest =
            # phần đắt nhất); apply chỉ còn freshness-check reg_get_bulk trên đúng các dòng sắp ghi + verify write.
            import time as _t
            _slim = lambda e: {"drive_id": _entry_drive_id(e), "nlm_source_id": (_entry_nlm(e) or "").strip(),   # noqa: E731
                               "nlm_notebook_id": str(e.get("nlm_notebook_id") or ""),
                               "row_kind": str(e.get("row_kind") or ""), "name": _entry_name(e)}
            _art = {"schema": "reconcile_plan.v1", "notebook": nb, "created_ts": _t.time(),
                    "live_on_nlm": len(live_ids),
                    "backfill": [_slim(e) for e in plan["backfill"]],
                    "link_candidates": [{**_slim(c["entry"]), "source_id": c["source_id"], "by": c["by"]}
                                        for c in (plan.get("link_candidates") or [])],
                    "desync_real": [_slim(e) for e in plan["desync_real"]]}
            try:
                Path(_plan_out).parent.mkdir(parents=True, exist_ok=True)
                Path(_plan_out).write_text(json.dumps(_art, ensure_ascii=False, indent=1) + "\n",
                                           encoding="utf-8", newline="\n")
                out["plan_artifact"] = str(_plan_out)
            except Exception as _pae:  # noqa: BLE001 — artifact best-effort, DRY vẫn trọn vẹn
                out["plan_artifact_error"] = str(_pae)
        _emit_json_payload(out, getattr(a, "out", None)); return 0
    if _suspect_c2 and not getattr(a, "force_unsafe", False):
        # FIX-C r201: DỪNG TRƯỚC MỌI GHI (preflight/gate/journal/reg_bulk đều chưa chạy tới).
        print(json.dumps({"ok": False, "error": "LISTING_CHANNEL_SUSPECT",
                          "unregistered_on_nlm": len(plan["unregistered"]), "live_on_nlm": len(live_ids),
                          "note": "Kênh liệt kê NLM khả nghi — apply theo plan này sẽ link/clear bậy hàng "
                                  "loạt. Làm theo playbook banner (đổi kênh / nlm login / đo máy khỏe); "
                                  "cố ý đi tiếp: --force-unsafe."}, ensure_ascii=False), file=sys.stderr)
        return 2
    for _w54 in (_nlm_preflight_report(nb, probe=False).get("warn") or []):   # v1.34.54 A1: tuổi cookie trước lô ghi (WARN; tầng-1 live đã nằm ở source_list phía trên)
        print(f"[tl] ⚠ {_w54}", file=sys.stderr)
    # v1.34.49 (F-06): +row_kind vào gate-cols (superset — backfill/link trên shard overflow nay ghi row_kind)
    _ok_gate, _pfv = _apply_gate(a, write_cols="nlm_source_id,nlm_notebook_id,nlm_status,row_kind")   # (Pha 1) chống clobber/ghi-mù
    if not _ok_gate:
        return 2
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))   # cần webapp để reg_bulk/reg_clear
    g = _gas()
    run_id = _apply_journal_start("nlm-reconcile", {"notebook": nb, "backfill": len(plan["backfill"]),
                                                    "link": len(plan.get("link_candidates") or [])})
    # v1.34.49 (F-06 — grill D-F6): recovery/link/backfill SUY row_kind TỪ TOPOLOGY cho notebook nb — trước đây
    # reconcile chỉ ghi nlm_* ⇒ nguồn recovery trên VBQPPL-2 để row_kind=own ⇒ sweep v1.34.47 (discover shard qua
    # row_kind=overflow) MẤT DẤU shard. primary → GIỮ blank (=own convention, tránh churn); kind bảo hộ
    # (ref/thuong) KHÔNG BAO GIỜ clobber; notebook ngoài topology → không ghi row_kind (doctor lộ UNKNOWN).
    _topo_rc = _resolve_shard_topology(entries, (os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK or "").strip())
    _rk_rc = _shard_row_kind(nb, _topo_rc)

    def _split_rk(pairs, key_of, before_of):
        # pairs: list[(entry, item)] → (plain, rked, before_plain, before_rk); rked chỉ khi nb=overflow + kind không bảo hộ
        _plain, _rked, _bp, _brk = [], [], {}, {}
        for _e, _it in pairs:
            _cur_rk = str((_e or {}).get("row_kind") or "").strip().lower()
            if _rk_rc == "overflow" and _cur_rk not in _ROW_KIND_PROTECTED:
                _rked.append({**_it, "row_kind": "overflow"})
                _brk[key_of(_e, _it)] = {**before_of(_e), "row_kind": _cur_rk}
            else:
                _plain.append(_it)
                _bp[key_of(_e, _it)] = before_of(_e)
        return _plain, _rked, _bp, _brk

    def _merge_writes(vs, rk_n):
        return {"ok": (all(bool((x.get("reg_bulk") or {}).get("ok")) for x in vs) if vs else None),
                "patched": sum(int(x.get("patched") or 0) for x in vs),
                "verified": (all(bool(x.get("verified")) for x in vs) if vs else None),
                "row_kind_written": rk_n}
    if plan["backfill"]:
        _pairs_bf = [(e, {"nlm_source_id": _entry_nlm(e), "nlm_notebook_id": nb}) for e in plan["backfill"]]
        _pl_bf, _rk_bf, _bp_bf, _brk_bf = _split_rk(
            _pairs_bf, key_of=lambda e, it: _entry_nlm(e),
            before_of=lambda e: {"nlm_notebook_id": str(e.get("nlm_notebook_id") or "")})
        _vs_bf = []
        if _pl_bf:
            _vs_bf.append(_journaled_reg_write(run_id, g, _pl_bf, "nlm_notebook_id",
                                               key_field="nlm_source_id", before_by_key=_bp_bf))
        if _rk_bf:
            _vs_bf.append(_journaled_reg_write(run_id, g, _rk_bf, "nlm_notebook_id,row_kind",
                                               key_field="nlm_source_id", before_by_key=_brk_bf))
        out["reg_bulk"] = _merge_writes(_vs_bf, len(_rk_bf))
    # C1: LINK nguồn live chưa-đăng-ký vào đúng dòng registry (khóa drive_id) → set nlm_source_id+notebook+status.
    if plan.get("link_candidates"):
        _pairs_ln = [(c["entry"], {"drive_id": _entry_drive_id(c["entry"]), "nlm_source_id": c["source_id"],
                                   "nlm_notebook_id": nb, "nlm_status": "pushed"})
                     for c in plan["link_candidates"] if _entry_drive_id(c["entry"])]
        _pl_ln, _rk_ln, _bp_ln, _brk_ln = _split_rk(
            _pairs_ln, key_of=lambda e, it: it["drive_id"],
            before_of=lambda e: {"nlm_source_id": ""})   # trước: chưa có source_id → undo = clear
        _vs_ln = []
        if _pl_ln:
            _vs_ln.append(_journaled_reg_write(run_id, g, _pl_ln, "nlm_source_id,nlm_notebook_id,nlm_status",
                                               before_by_key=_bp_ln))
        if _rk_ln:
            _vs_ln.append(_journaled_reg_write(run_id, g, _rk_ln, "nlm_source_id,nlm_notebook_id,nlm_status,row_kind",
                                               before_by_key=_brk_ln))
        out["reg_bulk_link"] = _merge_writes(_vs_ln, len(_rk_ln))
    # F3 r191: nâng deferred→pushed cho dòng đã XÁC MINH sid live đúng notebook (nlm-add --no-wait / defer).
    # CHỈ ghi nlm_status — corpus KHÔNG auto-true khi còn/deferred vừa nâng (corpus là việc pipeline ingest).
    if plan.get("settle_confirm"):
        _items_sc = [{"drive_id": _entry_drive_id(e), "nlm_status": "pushed"}
                     for e in plan["settle_confirm"] if _entry_drive_id(e)]
        _bef_sc = {_entry_drive_id(e): {"nlm_status": str(e.get("nlm_status") or "deferred")}
                   for e in plan["settle_confirm"] if _entry_drive_id(e)}
        if _items_sc:
            _v_sc = _journaled_reg_write(run_id, g, _items_sc, "nlm_status", before_by_key=_bef_sc)
            out["reg_bulk_settle_confirm"] = {"ok": bool((_v_sc.get("reg_bulk") or {}).get("ok")),
                                              "verified": bool(_v_sc.get("verified")), "count": len(_items_sc)}
    # --clear-stale CHỈ áp desync_real (KHÔNG xoá mapping/ status của dòng already_removed).
    if getattr(a, "clear_stale", False) and plan["desync_real"]:
        ops = [{"action": "reg_clear", "drive_id": _entry_drive_id(e),
                "cols": "nlm_source_id,nlm_status,nlm_pushed_at,nlm_title,nlm_notebook_id", "confirm": "yes"}
               for e in plan["desync_real"] if _entry_drive_id(e)]
        _journal_append(run_id, {"t": "intent", "op": "reg_clear", "key": "desync_batch",
                                 "cols": "nlm_source_id,nlm_status,nlm_pushed_at,nlm_title,nlm_notebook_id",
                                 "note": f"clear {len(ops)} dòng desync (KHÔNG reversible tự động)"})
        rc = g.post("batch", ops=ops)
        _journal_append(run_id, {"t": "commit", "op": "reg_clear", "key": "desync_batch", "ok": bool(rc.get("ok"))})
        out["clear_desync_real"] = {"ok": rc.get("ok"), "summary": rc.get("summary"), "count": len(ops)}
    _journal_append(run_id, {"t": "run_end", "ok": out["ok"],
                             "counts": {"backfill": len(plan["backfill"]), "link": len(plan.get("link_candidates") or [])}})
    out["journal"] = run_id
    _emit_json_payload(out, getattr(a, "out", None))
    return 0 if out["ok"] else 1


def _nlm_list_stale_read(nb: str, *, cache_dir=None):
    """E3 (v1.34.60): đọc cache listing C-#8 BẤT KỂ TTL (stale) khi NLM chết — kèm age để caller in cờ
    STALE_CACHE. Không có/hỏng cache → None (caller giữ đường lỗi cũ). CHỈ advisory — không phải bằng
    chứng vật lý (physical-first của audit/migrate KHÔNG dùng đường này)."""
    _dir = Path(cache_dir) if cache_dir else (HERE / ".tl_state")
    fp = _dir / f"nlm_list_cache_{nb}.json"
    try:
        data = json.loads(fp.read_text(encoding="utf-8"))
        srcs = data.get("sources")
        if not isinstance(srcs, list):
            return None
        age = max(0, int(time.time() - float(data.get("fetched_at") or 0)))
        return {"ok": True, "count": len(srcs), "sources": srcs, "cached": True, "stale": True,
                "age_s": age, "via": "cache_stale"}
    except Exception:  # noqa: BLE001
        return None


def _shard_row_kind(nb: str, topo: dict) -> str | None:
    """v1.34.49 (F-06): row_kind SUY TỪ TOPOLOGY cho dòng corpus theo notebook chứa nguồn — primary→'own',
    overflow (declared/env/registry-observed)→'overflow', ngoài topology→None (caller lộ UNKNOWN_NOTEBOOK,
    KHÔNG đoán). KHÔNG áp cho row_kind bảo hộ (ref/thuong) — caller phải giữ nguyên các kind đó."""
    nb = (nb or "").strip()
    if not nb:
        return None
    for s in (topo or {}).get("shards") or []:
        if s.get("id") == nb:
            return "own" if s.get("role") == "primary" else "overflow"
    return None


def cmd_nlm_source_remove(a) -> int:
    """(A-#12 v1.34.56) Gỡ nguồn KHỎI notebook NLM theo source_id (batch N sid / 1 process) — KHÔNG trash
    Drive, KHÔNG đụng dòng registry (khác source-delete; dòng stale là việc của nlm-reconcile/--clear-stale).
    GUARD: sid còn con trỏ registry → CHẶN (POINTER_STILL_ATTACHED), thoát --force. DRY mặc định."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        nc = _imp("nlm_cli")
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False), file=sys.stderr); return 2
    sids = [str(s).strip() for s in (getattr(a, "source_id", None) or []) if str(s).strip()]
    if not sids:
        print(json.dumps({"ok": False, "error": "NO_SOURCE_ID"}, ensure_ascii=False), file=sys.stderr); return 2
    do_apply = bool(getattr(a, "apply", False))
    # Đối chiếu con trỏ qua manifest; apply/--refresh ÉP refresh (bài học v1.34.50: manifest KHÔNG đáng tin
    # khi stale) + double-check reg_get authoritative bên dưới cho sid manifest bảo 'sạch'.
    try:
        entries = _manifest_entries(refresh=bool(getattr(a, "refresh", False) or do_apply))
    except Exception:  # noqa: BLE001
        entries = []
    plan = _nlm_source_remove_plan(entries, sids)
    if not do_apply:
        print(json.dumps({"ok": True, "dry_run": True, "rows": plan["rows"],
                          "attached": plan["attached"], "clean": plan["clean"],
                          "note": "DRY — chưa gỡ gì. Gỡ: --apply --confirm yes (KHÔNG trash Drive, KHÔNG đụng "
                                  "dòng registry; dòng stale: nlm-reconcile --apply / --clear-stale)."},
                         ensure_ascii=False, indent=2))
        return 0
    if str(getattr(a, "confirm", "") or "").strip().lower() != "yes":
        print(json.dumps({"ok": False, "error": "CONFIRM_REQUIRED",
                          "note": "gỡ nguồn NLM là bất khả nghịch phía notebook — thêm --confirm yes"},
                         ensure_ascii=False), file=sys.stderr)
        return 2
    force = bool(getattr(a, "force", False))
    run_id = _apply_journal_start("nlm-source-remove", {"sids": sids, "force": force})
    _g_sr = None
    if not force and plan["clean"]:
        try:
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))
            _g_sr = _gas()
        except Exception:  # noqa: BLE001
            _g_sr = None
    results, blocked, failed = [], 0, 0
    by_sid = {r0["source_id"]: r0 for r0 in plan["rows"]}
    for sid in sids:
        row = by_sid.get(sid) or {"pointer_attached": False, "pointers": []}
        att = bool(row.get("pointer_attached"))
        if not att and not force:
            # Fail-closed: manifest 'sạch' phải qua reg_get authoritative; không xác minh được → skip (không gỡ mù).
            if _g_sr is None:
                results.append({"source_id": sid, "action": "skipped", "reason": "REGISTRY_VERIFY_UNAVAILABLE",
                                "note": "không xác minh được con trỏ (creds/webapp) — fail-closed; --force bỏ guard"})
                blocked += 1
                continue
            try:
                _rg = _g_sr.get("reg_get", nlm_source_id=sid, refresh="false")
                if (_rg or {}).get("rows"):
                    att = True
                    row = {"pointer_attached": True,
                           "pointers": [{"drive_id": str(x.get("drive_id") or ""),
                                         "name": str(x.get("name") or ""),
                                         "nlm_notebook_id": str(x.get("nlm_notebook_id") or "")}
                                        for x in (_rg.get("rows") or [])]}
            except Exception:  # noqa: BLE001
                results.append({"source_id": sid, "action": "skipped", "reason": "REGISTRY_VERIFY_UNAVAILABLE",
                                "note": "reg_get lỗi — fail-closed; --force bỏ guard"})
                blocked += 1
                continue
        if att and not force:
            results.append({"source_id": sid, "action": "skipped", "reason": "POINTER_STILL_ATTACHED",
                            "pointers": row.get("pointers"),
                            "note": "dòng registry còn trỏ sid — gỡ sẽ tạo con trỏ treo; repoint/clear trước hoặc --force"})
            blocked += 1
            continue
        _journal_append(run_id, {"t": "intent", "op": "nlm_source_delete", "key": sid, "set": {"irreversible": True}})
        _dr = nc.source_delete(sid)
        verdict = _source_remove_delete_verdict(_dr)
        _journal_append(run_id, {"t": "commit", "op": "nlm_source_delete", "key": sid,
                                 "ok": verdict in ("deleted", "noop"), "verify": {"verdict": verdict}})
        if verdict == "fail":
            failed += 1
            results.append({"source_id": sid, "action": "fail", "detail": _dr.get("error") or _dr.get("raw")})
        else:
            results.append({"source_id": sid, "action": verdict})
    counts = {"deleted": sum(1 for r0 in results if r0["action"] == "deleted"),
              "noop": sum(1 for r0 in results if r0["action"] == "noop"),
              "skipped": blocked, "fail": failed}
    ok = failed == 0 and blocked < len(sids)
    _journal_append(run_id, {"t": "run_end", "ok": ok, "counts": counts})
    print(json.dumps({"ok": ok, "journal": run_id, "results": results, "counts": counts,
                      "note": "KHÔNG đụng Drive/dòng registry — dòng stale: nlm-reconcile --apply / --clear-stale."},
                     ensure_ascii=False, indent=2))
    return 0 if ok else 2


def _nlm_source_list_cached(nc, nb: str, *, ttl_s: int = 600, refresh: bool = False, cache_dir=None) -> dict:
    """v1.34.57 (B-#3/#8 — Q10): cache client-side TTL 10' chồng lên listing `-S` (skip_freshness mặc định).
    nlm-audit-physical dùng mặc định; nlm-migrate KHÔNG dùng cho notebook ĐÍCH (physical-first cần tươi);
    --refresh-live ép tươi. File: scripts/.tl_state/nlm_list_cache_<nb>.json {fetched_at, count, sources}
    (write_bytes — giữ LF, bài học kernel CRLF)."""
    _dir = Path(cache_dir) if cache_dir else (HERE / ".tl_state")
    fp = _dir / f"nlm_list_cache_{nb}.json"
    if not refresh:
        try:
            data = json.loads(fp.read_text(encoding="utf-8"))
            age = time.time() - float(data.get("fetched_at") or 0)
            if 0 <= age <= ttl_s and isinstance(data.get("sources"), list):
                return {"ok": True, "count": len(data["sources"]), "sources": data["sources"],
                        "cached": True, "age_s": int(age), "via": "cache"}
        except Exception:  # noqa: BLE001 — cache thiếu/hỏng → coi như miss, list tươi
            pass
    r = nc.source_list(nb, skip_freshness=True)
    if r.get("ok"):
        try:
            _dir.mkdir(parents=True, exist_ok=True)
            fp.write_bytes(json.dumps({"fetched_at": time.time(), "count": r.get("count"),
                                       "sources": r.get("sources") or []},
                                      ensure_ascii=False).encode("utf-8"))
        except Exception:  # noqa: BLE001 — ghi cache best-effort, không chặn kết quả
            pass
    return r


def _physical_audit_classify(reg_rows: list, phys_by_nb: dict) -> dict:
    """v1.34.57 (B-#3 — Q5=a) PURE: đối soát registry ↔ VẬT LÝ (physical-first — bài học 32/40 CPTPP:
    nlm_notebook_id CHỈ là nơi registry NGHĨ). Match 2 tầng như reconcile: drive_id (cứng) → title-key
    chuẩn hóa (chỉ khi DUY NHẤT); KHÔNG BAO GIỜ dùng is_stale. 4 finding: POINTER_MISMATCH /
    UNREGISTERED_PHYSICAL / DUP_PHYSICAL / POINTER_DEAD — dead CHỈ kết luận khi scope quét ⊇ notebook
    pointer trỏ (hoặc pointer nb RỖNG = row nhận topology làm nhà); nb ngoài scope → unverified_scope
    (advisory, tránh oan — 37 CPTPP tham chiếu là CÓ CHỦ ĐÍCH). Dòng nlm_status removed* = tombstone, bỏ qua.
    v1.34.59: OUTPUT drive_id (findings + unverified_scope + suggested_commands) fallback gdoc_id ĐỒNG BỘ với
    logic match (dòng key gdoc_id trước đây in drive_id RỖNG → suggested `--drive-ids <rỗng>` vô dụng)."""
    scanned = sorted(str(nb) for nb in (phys_by_nb or {}))
    sid_at: dict = {}
    by_did: dict = {}
    by_title: dict = {}
    for nb in scanned:
        d1, t1 = {}, {}
        for s in (phys_by_nb.get(nb) or []):
            sid = str(s.get("id") or s.get("source_id") or "")
            if sid:
                sid_at.setdefault(sid, set()).add(nb)
            did = _nlm_source_drive_id(s)
            if did:
                d1.setdefault(did, []).append(s)
            tk = _ingest_dedup_title_key(s.get("title") or "")
            if tk:
                t1.setdefault(tk, []).append(s)
        by_did[nb] = d1
        by_title[nb] = t1

    def _phys_match(row):
        did = str(row.get("drive_id") or row.get("gdoc_id") or "").strip()
        tk = _ingest_dedup_title_key(row.get("name") or "")
        out = []
        for nb in scanned:
            hits = list(by_did[nb].get(did) or []) if did else []
            if not hits and tk:
                cand = by_title[nb].get(tk) or []
                if len(cand) == 1:
                    hits = cand
            for s in hits:
                out.append((nb, s))
        return out

    mismatch, dead, unverified = [], [], []
    rows_use = [r0 for r0 in (reg_rows or [])
                if not str(r0.get("nlm_status") or "").strip().lower().startswith("removed")]
    for r0 in rows_use:
        p_sid = str(r0.get("nlm_source_id") or "").strip()
        if not p_sid:
            continue   # chưa có pointer = stale-an-toàn (nlm-links/reconcile lo) — KHÔNG phải drift
        p_nb = str(r0.get("nlm_notebook_id") or "").strip()
        if p_nb and p_nb in set(scanned) and p_nb in (sid_at.get(p_sid) or set()):
            continue   # pointer khớp vật lý
        if p_nb and p_nb not in set(scanned):
            unverified.append({"drive_id": str(r0.get("drive_id") or r0.get("gdoc_id") or ""), "name": str(r0.get("name") or ""),
                               "nlm_source_id": p_sid, "nlm_notebook_id": p_nb,
                               "note": "pointer trỏ notebook NGOÀI scope quét — thêm --notebooks/--all-profiles để verify"})
            continue
        hits = _phys_match(r0)
        if hits:
            nb_hit, s_hit = hits[0]
            mismatch.append({"drive_id": str(r0.get("drive_id") or r0.get("gdoc_id") or ""), "name": str(r0.get("name") or ""),
                             "pointer_nb": p_nb, "pointer_sid": p_sid, "physical_nb": nb_hit,
                             "physical_sid": str(s_hit.get("id") or s_hit.get("source_id") or "")})
        else:
            dead.append({"drive_id": str(r0.get("drive_id") or r0.get("gdoc_id") or ""), "name": str(r0.get("name") or ""),
                         "nlm_source_id": p_sid, "nlm_notebook_id": p_nb})
    row_sids = {str(r0.get("nlm_source_id") or "").strip() for r0 in (reg_rows or []) if r0.get("nlm_source_id")}
    row_dids = {str(r0.get("drive_id") or r0.get("gdoc_id") or "").strip() for r0 in (reg_rows or [])}
    row_title_counts: dict = {}
    for r0 in (reg_rows or []):
        tk = _ingest_dedup_title_key(r0.get("name") or "")
        if tk:
            row_title_counts[tk] = row_title_counts.get(tk, 0) + 1
    unreg, dups = [], []
    for nb in scanned:
        for did in sorted(by_did[nb]):
            group = by_did[nb][did]
            if len(group) >= 2:
                sids = [str(s.get("id") or s.get("source_id") or "") for s in group]
                keep = next((x for x in sids if x in row_sids), sids[0])
                dups.append({"notebook_id": nb, "drive_id": did, "sids": sids, "keep": keep,
                             "titles": [str(s.get("title") or "") for s in group]})
        for tk in sorted(by_title[nb]):
            group = [s for s in by_title[nb][tk] if not _nlm_source_drive_id(s)]
            if len(group) >= 2:   # identity theo title khi KHÔNG có drive-URL nào trong nhóm
                sids = [str(s.get("id") or s.get("source_id") or "") for s in group]
                keep = next((x for x in sids if x in row_sids), sids[0])
                dups.append({"notebook_id": nb, "drive_id": "", "title_key": tk, "sids": sids, "keep": keep,
                             "titles": [str(s.get("title") or "") for s in group]})
        for s in (phys_by_nb.get(nb) or []):
            sid = str(s.get("id") or s.get("source_id") or "")
            did = _nlm_source_drive_id(s)
            tk = _ingest_dedup_title_key(s.get("title") or "")
            if sid and sid in row_sids:
                continue
            if did and did in row_dids:
                continue
            if tk and row_title_counts.get(tk) == 1:
                continue
            unreg.append({"notebook_id": nb, "source_id": sid, "title": str(s.get("title") or ""),
                          **({"drive_id": did} if did else {})})
    sugg = []
    for f in mismatch:
        sugg.append(f"tl nlm-migrate --to {f['physical_nb']} --drive-ids {f['drive_id']} --apply --confirm yes"
                    "   # repoint theo VẬT LÝ (physical-first)")
    for nb in sorted({u["notebook_id"] for u in unreg}):
        sugg.append(f"tl nlm-reconcile {nb} --apply   # link bắc cầu / register nguồn chưa đăng ký")
    for d in dups:
        extras = [x for x in d["sids"] if x != d["keep"]]
        if extras:
            sugg.append("tl nlm-source-remove " + " ".join(extras)
                        + f" --apply --confirm yes   # gỡ bản THỪA trên {d['notebook_id'][:16]}… (giữ {d['keep']})")
    for f in dead:
        sugg.append(f"tl nlm-reconcile --all-notebooks   # dò lại {f['drive_id']}; mất thật → nlm-links/nlm-migrate nạp lại")
    findings = {"pointer_mismatch": mismatch, "unregistered_physical": unreg,
                "dup_physical": dups, "pointer_dead": dead}
    return {"clean": not any(findings.values()), "findings": findings,
            "unverified_scope": unverified, "suggested_commands": sugg}


def _migrate_resume_write(to_nb: str, filter_kind: str, filter_value, a, *, state_dir=None) -> str:
    """E2 (v1.34.61 — ADR-3): ghi resume-artifact cho nlm-migrate khi NLM chết giữa --apply. KHÁC A3
    reconcile (plan-rows, TTL 15'): artifact này CHỈ chứa THAM SỐ — plan LUÔN re-tạo TƯƠI từ vật lý đích
    lúc --from-plan (physical-first) nên KHÔNG cần TTL. File: .tl_state/migrate_resume_<to>.json (LF)."""
    _dir = Path(state_dir) if state_dir else (HERE / ".tl_state")
    _dir.mkdir(parents=True, exist_ok=True)
    fp = _dir / f"migrate_resume_{to_nb}.json"
    art = {"schema": "migrate_resume.v1", "created_ts": time.time(), "to": str(to_nb),
           "filter": {str(filter_kind): str(filter_value)},
           "from_nb": str(getattr(a, "from_nb", None) or ""),
           "api_add": bool(getattr(a, "api_add", False)),
           "limit": int(getattr(a, "limit", None) or 0),
           "note": "THAM SỐ resume nlm-migrate (NLM offline lúc apply) — chạy nốt khi NLM sống: "
                   f"tl nlm-migrate --from-plan {fp} --apply --confirm yes (plan re-tạo tươi, không TTL)."}
    fp.write_bytes((json.dumps(art, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    return str(fp)


def cmd_nlm_audit_physical(a) -> int:
    """(B-#3 v1.34.57, Q5=a) READ-ONLY đối soát VẬT LÝ ↔ con trỏ registry (physical-first). Scope mặc định:
    topology VBQPPL (base + overflow shards) — foreign profile KHÔNG quét mặc định; --notebooks thêm đích;
    --all-profiles quét mọi notebookId config (đắt ~90s/notebook lớn). Listing qua cache TTL 10'
    (--refresh-live ép tươi). rc=0 sạch / 1 có finding / 2 lỗi chạy. Doctor chỉ advisory nhắc, KHÔNG tự chạy."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        nc = _imp("nlm_cli")
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False), file=sys.stderr); return 2
    try:
        entries = _manifest_entries(refresh=False)
    except Exception as e:  # noqa: BLE001
        print(f"[tl] nlm-audit-physical: cần `tl boot`/`manifest` trước ({e}).", file=sys.stderr)
        return 2
    base, _nberr = _resolve_nlm_notebook(None)
    if _nberr:
        print(json.dumps({"ok": False, "error": _nberr}, ensure_ascii=False), file=sys.stderr); return 2
    scope = [base] + [s for s in _resolve_overflow_shards(entries, base) if s and s != base]
    for nb_x in str(getattr(a, "notebooks", None) or "").split(","):
        nb_x = nb_x.strip()
        if nb_x and nb_x not in scope:
            scope.append(nb_x)
    if getattr(a, "all_profiles", False):
        try:
            _, cfg = _read_config_record(None)
            for _pname in sorted((_profiles_from_config(cfg or {}) or {})):
                p = (_profiles_from_config(cfg or {}) or {}).get(_pname)
                if not isinstance(p, dict):
                    continue
                _ids = [str(p.get("notebookId") or "").strip()]
                for s in (p.get("shards") if isinstance(p.get("shards"), list) else []):
                    _ids.append(str((s.get("id") if isinstance(s, dict) else s) or "").strip())
                for nb_x in _ids:
                    if nb_x and nb_x not in scope:
                        scope.append(nb_x)
        except Exception as e:  # noqa: BLE001
            print(f"[tl] ⚠ --all-profiles: không đọc được config ({e}) — giữ scope topology.", file=sys.stderr)
    phys_by_nb, nb_meta, fails, stale_nbs = {}, [], [], []
    _v62 = None   # verdict fallback tính 1 LẦN cho cả loop (banner không spam per-notebook)
    for nb in scope:
        r = _nlm_source_list_cached(nc, nb, refresh=bool(getattr(a, "refresh_live", False)))
        if r.get("ok"):
            phys_by_nb[nb] = r.get("sources") or []
            nb_meta.append({"notebook_id": nb, "count": len(phys_by_nb[nb]), "cached": bool(r.get("cached"))})
            continue
        # v1.34.61 (E2 unverified-continue — ADR-3): NLM hard-dead → dùng cache stale BẤT KỂ TTL cho notebook
        # này (audit CHẠY TIẾP, mọi finding gắn UNVERIFIED_NLM_STATE); KHÔNG cache → giữ hành vi cũ: notebook
        # RA KHỎI scope (pointer trỏ nó → unverified_scope advisory tự nhiên — không bịa tầng vật lý).
        if _v62 is None:
            _v62 = _nlm_or_corpus("nlm-audit-physical", a, notebook_id=nb, err=r)
        _st62 = _nlm_list_stale_read(nb) if _v62["route"] == "unverified" else None
        if _st62:
            phys_by_nb[nb] = _st62.get("sources") or []
            stale_nbs.append(nb)
            nb_meta.append({"notebook_id": nb, "count": len(phys_by_nb[nb]), "cached": True,
                            "stale": True, "age_s": _st62.get("age_s")})
            print(f"[tl] ⚠ UNVERIFIED_NLM_STATE: {str(nb)[:16]}… dùng cache STALE tuổi {_st62.get('age_s')}s "
                  f"(NLM offline) — finding CHỈ là belief, chạy lại khi NLM sống để verify.", file=sys.stderr)
        else:
            fails.append({"notebook_id": nb, "error": str(r.get("error") or "")[:160]})
            print(f"[tl] ⚠ không list được {str(nb)[:16]}… ({str(r.get('error') or '')[:80]}) — notebook RA KHỎI "
                  "scope (POINTER_DEAD sẽ không kết luận trên nó).", file=sys.stderr)
    if not phys_by_nb:
        print(json.dumps({"ok": False, "error": "NO_NOTEBOOK_LISTED", "failed": fails},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    res = _physical_audit_classify(entries, phys_by_nb)
    counts = {k: len(v) for k, v in res["findings"].items()}
    # E2: BẤT KỲ notebook nào chạy trên stale → gắn unverified TOÀN BỘ finding (bảo thủ: 1 phần scope stale
    # là cả bức tranh vật lý không còn chắc — vd doc 'dead' ở nb tươi có thể sống ở nb stale lệch).
    if stale_nbs:
        for _fl in res["findings"].values():
            for _f in _fl:
                _f["unverified_nlm_state"] = True
    payload = {"ok": True, "schema": "nlm_audit_physical.v1", "clean": res["clean"],
               "notebooks": nb_meta, "list_failed": fails, "counts": counts,
               "findings": res["findings"],
               "unverified_scope": {"count": len(res["unverified_scope"]),
                                    "sample": res["unverified_scope"][:10]},
               "suggested_commands": res["suggested_commands"],
               **({"nlm_status": "offline", "fallback": "unverified", "unverified_nlm_state": True,
                   "stale_notebooks": stale_nbs, "source": "stale_cache+registry_belief"} if stale_nbs else {}),
               "note": ("UNVERIFIED_NLM_STATE: một phần scope chạy trên cache STALE (NLM offline) — finding là "
                        "belief, KHÔNG ghi/xử lý theo nó; chạy lại khi NLM sống để verify (physical-first)."
                        if stale_nbs else
                        "physical-first: kết luận từ listing VẬT LÝ; nlm_notebook_id chỉ là nơi registry NGHĨ.")}
    if getattr(a, "json", False) or getattr(a, "out", None):
        _emit_json_payload(payload, getattr(a, "out", None))
    else:
        print(("SẠCH — pointer khớp vật lý toàn scope." if res["clean"]
               else "CÓ FINDING: " + " · ".join(f"{k}={v}" for k, v in counts.items() if v)))
        for c in res["suggested_commands"][:12]:
            print(f"  → {c}")
        if res["unverified_scope"]:
            print(f"  ℹ {len(res['unverified_scope'])} pointer trỏ notebook ngoài scope (unverified — không oan).")
    return 0 if res["clean"] else 1


def _migrate_plan(reg_rows: list, phys_target: list, target_nb: str, phys_from: list | None = None) -> dict:
    """v1.34.57 (B-#4..#7, Q6=a) PURE: phân loại per-doc theo VẬT LÝ ĐÍCH — POINTER_OK (vật lý ở đích +
    pointer đúng) / REPOINT (vật lý ở đích, pointer sai — sid VẬT LÝ là chân lý, chỉ ghi registry) /
    ADD (thiếu ở đích). Match tier-0 sid-pointer-sống-tại-đích (nhất quán audit — ca live CPTPP Ch22/25:
    listing không lộ drive-URL + title dup → did/title đều câm nhưng sid live = VẬT LÝ ở đích) → drive_id →
    title-key duy nhất. cleanup = nguồn cũ ở --from cho doc đã POINTER_OK (Q7=a: CHỈ IN, không bao giờ tự gỡ)."""
    t_by_did, t_by_title, f_by_did = {}, {}, {}
    t_sids = {str(s.get("id") or s.get("source_id") or "") for s in (phys_target or [])}
    t_sids.discard("")
    for s in (phys_target or []):
        did = _nlm_source_drive_id(s)
        if did:
            t_by_did.setdefault(did, []).append(s)
        tk = _ingest_dedup_title_key(s.get("title") or "")
        if tk:
            t_by_title.setdefault(tk, []).append(s)
    for s in (phys_from or []):
        did = _nlm_source_drive_id(s)
        if did:
            f_by_did.setdefault(did, []).append(s)
    pointer_ok, repoint, add, cleanup = [], [], [], []
    for r0 in (reg_rows or []):
        did = str(r0.get("drive_id") or r0.get("gdoc_id") or "").strip()
        if not did:
            continue
        name = str(r0.get("name") or "")
        _p_sid0 = str(r0.get("nlm_source_id") or "").strip()
        _p_nb0 = str(r0.get("nlm_notebook_id") or "").strip()
        if _p_sid0 and _p_sid0 in t_sids and _p_nb0 == str(target_nb):
            # tier-0: pointer sid SỐNG tại đích + nb đúng = POINTER_OK (cùng quy tắc audit OK-check)
            pointer_ok.append({"drive_id": did, "name": name, "phys_sid": _p_sid0})
            for s_f in (f_by_did.get(did) or []):
                sid_f = str(s_f.get("id") or s_f.get("source_id") or "")
                if sid_f and sid_f != _p_sid0:
                    cleanup.append({"drive_id": did, "name": name, "source_id": sid_f})
            continue
        hits = list(t_by_did.get(did) or [])
        if not hits:
            tk = _ingest_dedup_title_key(r0.get("name") or "")
            cand = t_by_title.get(tk) or []
            if tk and len(cand) == 1:
                hits = cand
        if not hits:
            add.append({"drive_id": did, "name": name, "row": r0})
            continue
        phys_sid = str(hits[0].get("id") or hits[0].get("source_id") or "")
        p_sid = str(r0.get("nlm_source_id") or "").strip()
        p_nb = str(r0.get("nlm_notebook_id") or "").strip()
        if p_sid == phys_sid and p_nb == str(target_nb):
            pointer_ok.append({"drive_id": did, "name": name, "phys_sid": phys_sid})
            for s_f in (f_by_did.get(did) or []):
                sid_f = str(s_f.get("id") or s_f.get("source_id") or "")
                if sid_f and sid_f != phys_sid:
                    cleanup.append({"drive_id": did, "name": name, "source_id": sid_f})
        else:
            repoint.append({"drive_id": did, "name": name, "phys_sid": phys_sid,
                            "before": {"nlm_source_id": p_sid, "nlm_notebook_id": p_nb,
                                       "nlm_status": str(r0.get("nlm_status") or "")},
                            "row_kind_before": str(r0.get("row_kind") or ""), "row": r0})
    return {"pointer_ok": pointer_ok, "repoint": repoint, "add": add, "cleanup": cleanup}


def cmd_nlm_migrate(a) -> int:
    """(B-#4..#7 v1.34.57, Q6=a/Q7=a) DI DỜI physical-first idempotent: PLAN re-tạo từ VẬT LÝ ĐÍCH (luôn
    list TƯƠI, không cache) mỗi lần chạy → POINTER_OK / REPOINT (in-process batch ~2s/dòng) / ADD (mặc định
    BATCH_LINKS khi >NLM_BATCH_LINKS_THRESHOLD doc — user dán link; --api-add ép API per-doc qua cmd_nlm_add
    đường đã vá A-#1/#2: claim + verify-then-link). KHÔNG bao giờ tự gỡ nguồn cũ — in sẵn nlm-source-remove
    (Q7). Dán xong: CHẠY LẠI đúng lệnh này (ADD tự thành REPOINT = harvest, không cờ riêng/state file).
    Danh sách tường minh — KHÔNG đi qua matcher reconcile (không đụng ownership-guard A2)."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    # v1.34.61 (E2 — ADR-3): --from-plan nạp THAM SỐ từ resume-artifact (ghi lúc --apply gặp NLM chết).
    # KHÁC A3 reconcile: artifact KHÔNG chứa dòng ghi — plan LUÔN re-tạo TƯƠI từ vật lý đích ngay dưới
    # (physical-first) nên KHÔNG cần TTL; chỉ validate schema + khớp --to nếu user đưa cả hai.
    _fp_m = getattr(a, "from_plan", None)
    if _fp_m is not None:
        _fpp = str(_fp_m)
        if _fpp in ("", "auto"):
            _to_h = str(getattr(a, "to", None) or "").strip()
            if not _to_h:
                print(json.dumps({"ok": False, "error": "FROM_PLAN_NEEDS_TO_OR_PATH",
                                  "note": "--from-plan auto cần --to <nb> để tìm .tl_state/migrate_resume_<to>"
                                          ".json; hoặc đưa thẳng đường dẫn artifact."},
                                 ensure_ascii=False), file=sys.stderr)
                return 2
            _fpp = str(HERE / ".tl_state" / f"migrate_resume_{_to_h}.json")
        try:
            _art_m = json.loads(Path(_fpp).read_text(encoding="utf-8"))
        except Exception as _fe_m:  # noqa: BLE001
            print(json.dumps({"ok": False, "error": "PLAN_NOT_FOUND", "path": _fpp, "detail": str(_fe_m)[:120]},
                             ensure_ascii=False), file=sys.stderr)
            return 2
        if _art_m.get("schema") != "migrate_resume.v1" or (
                str(getattr(a, "to", None) or "").strip()
                and str(getattr(a, "to")).strip() != str(_art_m.get("to"))):
            print(json.dumps({"ok": False, "error": "PLAN_MISMATCH", "path": _fpp,
                              "plan_to": _art_m.get("to"), "to": getattr(a, "to", None)},
                             ensure_ascii=False), file=sys.stderr)
            return 2
        a.to = str(_art_m.get("to") or "")
        for _k_m in ("name_contains", "cat", "drive_ids"):
            if (_art_m.get("filter") or {}).get(_k_m) and not getattr(a, _k_m, None):
                setattr(a, _k_m, (_art_m.get("filter") or {})[_k_m])
        if not getattr(a, "from_nb", None) and _art_m.get("from_nb"):
            a.from_nb = _art_m["from_nb"]
        if _art_m.get("api_add"):
            a.api_add = True
        if _art_m.get("limit") and not getattr(a, "limit", None):
            a.limit = int(_art_m["limit"])
        print(f"[tl] nlm-migrate --from-plan: tham số từ {_fpp} (to={a.to}) — plan vẫn re-tạo TƯƠI từ vật lý "
              f"đích (physical-first, không TTL).", file=sys.stderr)
    elif not str(getattr(a, "to", None) or "").strip():
        # --to hết required=True ở parser (nhường --from-plan) → giữ guard tường minh, KHÔNG rơi về base mặc định
        print(json.dumps({"ok": False, "error": "TO_REQUIRED",
                          "note": "nlm-migrate cần --to <nb> (hoặc --from-plan <artifact>)."},
                         ensure_ascii=False), file=sys.stderr)
        return 2
    _filters = [x for x in (("name_contains", getattr(a, "name_contains", None)),
                            ("cat", getattr(a, "cat", None)),
                            ("drive_ids", getattr(a, "drive_ids", None))) if str(x[1] or "").strip()]
    if len(_filters) != 1:
        print(json.dumps({"ok": False, "error": "FILTER_REQUIRED",
                          "note": "chọn ĐÚNG 1 bộ lọc: --name-contains X | --cat NN | --drive-ids <file|csv>"},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    try:
        nc = _imp("nlm_cli")
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False), file=sys.stderr); return 2
    to_nb, _nberr = _resolve_nlm_notebook(getattr(a, "to", None))
    if _nberr or not to_nb:
        print(json.dumps({"ok": False, "error": _nberr or "TO_REQUIRED"}, ensure_ascii=False), file=sys.stderr)
        return 2
    try:
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    except (SystemExit, Exception):  # noqa: BLE001 — DRY vẫn plan được từ manifest cache offline
        pass
    try:
        entries = _manifest_entries(refresh=False)
    except Exception as e:  # noqa: BLE001
        print(f"[tl] nlm-migrate: cần `tl boot`/`manifest` trước ({e}).", file=sys.stderr)
        return 2
    fk, fv = _filters[0]
    rows = [e for e in entries if str(e.get("drive_id") or e.get("gdoc_id") or "").strip()
            and not str(e.get("nlm_status") or "").strip().lower().startswith("removed")]
    if fk == "name_contains":
        rows = [e for e in rows if str(fv).lower() in str(e.get("name") or "").lower()]
    elif fk == "cat":
        rows = [e for e in rows if str(_entry_cat(e) or "").startswith(str(fv))
                or str(_entry_cat(e) or "").split("_")[0] == str(fv)]
    else:
        try:
            _p_ids = Path(str(fv))
            _raw_ids = _p_ids.read_text(encoding="utf-8") if _p_ids.is_file() else str(fv)
        except Exception:  # noqa: BLE001
            _raw_ids = str(fv)
        _want = {x.strip() for x in re.split(r"[,\s]+", _raw_ids) if x.strip()}
        rows = [e for e in rows if str(e.get("drive_id") or e.get("gdoc_id") or "").strip() in _want]
    if getattr(a, "limit", None):
        rows = rows[:int(a.limit)]
    if not rows:
        print(json.dumps({"ok": False, "error": "NO_ROWS_MATCH_FILTER", "filter": {fk: str(fv)}},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    # (2) VẬT LÝ ĐÍCH — LUÔN TƯƠI (physical-first; fail-closed nếu không list được); --from → cache OK.
    _lt = nc.source_list(to_nb, skip_freshness=True)
    _unver62 = None   # E2: meta stale khi plan buộc chạy trên cache STALE (NLM offline)
    if not _lt.get("ok"):
        # v1.34.61 (E2 — ADR-3): NLM hard-dead → (i) có cache STALE của đích: plan CHẠY TIẾP trên stale, cờ
        # UNVERIFIED_NLM_STATE (apply sẽ DEFER phần ghi, chỉ BATCH_LINKS chạy — nhánh dưới); (ii) không cache
        # + --apply: DEFER + resume-artifact THAM SỐ, rc=0; (iii) không cache + DRY: giữ rc=2 (không ground
        # truth nào để plan). --no-fallback/TL_NLM_FALLBACK=0/transient → fail-closed như cũ.
        _v62m = _nlm_or_corpus("nlm-migrate", a, notebook_id=to_nb, err=_lt)
        _st62m = _nlm_list_stale_read(to_nb) if _v62m["route"] == "deferred" else None
        if _st62m:
            _unver62 = {"age_s": _st62m.get("age_s")}
            _lt = _st62m
            print(f"[tl] ⚠ UNVERIFIED_NLM_STATE: plan từ cache STALE tuổi {_st62m.get('age_s')}s (NLM "
                  f"offline) — apply sẽ DEFER repoint/API-add, chỉ BATCH_LINKS (dán tay) chạy.", file=sys.stderr)
        elif _v62m["route"] == "deferred" and getattr(a, "apply", False):
            _fp62m = _migrate_resume_write(to_nb, fk, fv, a)
            print(json.dumps({"ok": True, "schema": "nlm_migrate.v1", "mode": "DEFERRED_NLM_OFFLINE",
                              "nlm_status": "offline", "fallback": "deferred", "to": to_nb,
                              "filter": {fk: str(fv)}, "why": _v62m["why"][:120],
                              "resume_artifact": _fp62m,
                              "note": "NLM offline + không có cache listing đích → CHƯA làm gì (không ghi "
                                      "trên belief). Chạy nốt khi NLM sống: `tl nlm-migrate --from-plan "
                                      f"{_fp62m} --apply --confirm yes` (plan re-tạo tươi)."},
                             ensure_ascii=False, indent=2))
            return 0
        else:
            print(json.dumps({"ok": False, "error": "LIVE_SOURCE_LIST_FAILED", "notebook": to_nb,
                              "detail": str(_lt.get("error") or "")[:200],
                              "note": "physical-first cần ground truth ĐÍCH — `nlm login` rồi chạy lại."},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
    phys_t = _lt.get("sources") or []
    from_nb = str(getattr(a, "from_nb", None) or "").strip()
    phys_f = None
    if from_nb:
        _lf = _nlm_source_list_cached(nc, from_nb)
        phys_f = (_lf.get("sources") or []) if _lf.get("ok") else []
    plan = _migrate_plan(rows, phys_t, to_nb, phys_from=phys_f)
    counts = {"pointer_ok": len(plan["pointer_ok"]), "repoint": len(plan["repoint"]), "add": len(plan["add"])}
    cleanup_cmds = ([("tl nlm-source-remove " + " ".join(c["source_id"] for c in plan["cleanup"])
                      + " --apply --confirm yes   # nguồn cũ ở --from cho doc đã POINTER_OK — Q7: CHỈ IN, user duyệt")]
                    if plan["cleanup"] else [])

    def _mk(its, keys):
        return [{k: it.get(k) for k in keys if k in it} for it in its]
    groups_out = {"pointer_ok": _mk(plan["pointer_ok"], ("drive_id", "name", "phys_sid")),
                  "repoint": _mk(plan["repoint"], ("drive_id", "name", "phys_sid", "before")),
                  "add": _mk(plan["add"], ("drive_id", "name")),
                  "cleanup": plan["cleanup"]}
    if not getattr(a, "apply", False):
        payload = {"ok": True, "schema": "nlm_migrate.v1", "dry_run": True, "to": to_nb,
                   "filter": {fk: str(fv)}, "counts": counts, "plan": groups_out,
                   "cleanup_commands": cleanup_cmds,
                   **({"nlm_status": "offline", "unverified_nlm_state": True,
                       "stale_age_s": _unver62.get("age_s")} if _unver62 else {}),
                   "note": (("UNVERIFIED_NLM_STATE: plan từ cache STALE (NLM offline) — phân loại là belief, "
                             "chạy lại khi NLM sống để chốt. ") if _unver62 else "")
                           + "DRY re-plan từ vật lý đích (luôn tươi). ADD >"
                           f"{NLM_BATCH_LINKS_THRESHOLD} doc → BATCH_LINKS khi apply (--api-add ép API). "
                           "Apply: thêm --apply --confirm yes. Dán link xong: CHẠY LẠI đúng lệnh (harvest)."}
        _emit_json_payload(payload, getattr(a, "out", None))
        return 0
    if str(getattr(a, "confirm", "") or "").strip().lower() != "yes":
        print(json.dumps({"ok": False, "error": "CONFIRM_REQUIRED",
                          "note": "nlm-migrate ghi registry (repoint) / add NLM — thêm --confirm yes"},
                         ensure_ascii=False), file=sys.stderr)
        return 2
    if _unver62:
        # v1.34.61 (E2 — ADR-3): apply trên plan STALE → KHÔNG ghi registry / KHÔNG API-add trên belief
        # (physical-first); CHỈ BATCH_LINKS (in link, dán tay không cần NLM — reconcile bắt trùng sau nếu
        # stale lệch) + resume-artifact để chạy nốt repoint/API khi NLM sống. rc=0 (ADR-6).
        _fp62m = _migrate_resume_write(to_nb, fk, fv, a)
        links62 = ([_entry_links_url(it.get("row") or {"drive_id": it["drive_id"]}) for it in plan["add"]]
                   if (plan["add"] and len(plan["add"]) > NLM_BATCH_LINKS_THRESHOLD
                       and not getattr(a, "api_add", False)) else [])
        payload62 = {"ok": True, "schema": "nlm_migrate.v1", "mode": "DEFERRED_NLM_OFFLINE",
                     "nlm_status": "offline", "fallback": "deferred", "unverified_nlm_state": True,
                     "stale_age_s": _unver62.get("age_s"), "to": to_nb, "filter": {fk: str(fv)},
                     "counts": counts,
                     "deferred": {"repoint": len(plan["repoint"]),
                                  "add_api": (0 if links62 else len(plan["add"]))},
                     **({"links": links62} if links62 else {}),
                     "resume_artifact": _fp62m,
                     "note": "NLM offline: plan từ cache STALE (UNVERIFIED) — repoint/API-add DEFER, links "
                             "dán tay được ngay. Chạy nốt khi NLM sống: `tl nlm-migrate --from-plan "
                             f"{_fp62m} --apply --confirm yes`."}
        if links62 and not (getattr(a, "json", False) or getattr(a, "out", None)):
            for ln in links62:
                print(ln)
            print(f"[tl] nlm-migrate BATCH_LINKS (UNVERIFIED — plan stale, NLM offline): {len(links62)} link "
                  f"— dán vào Add source → Websites của https://notebooklm.google.com/notebook/{to_nb}; "
                  f"repoint/API-add DEFER.", file=sys.stderr)
            print(f"[tl]   chạy nốt khi NLM sống: tl nlm-migrate --from-plan {_fp62m} --apply --confirm yes",
                  file=sys.stderr)
        else:
            _emit_json_payload(payload62, getattr(a, "out", None))
        return 0
    run_id = _apply_journal_start("nlm-migrate", {"to": to_nb, "filter": {fk: str(fv)}, "counts": counts})
    results = {"repoint": [], "add": [], "repoint_verified": None}
    ok_all = True
    if plan["repoint"]:
        try:
            g = _gas()
        except Exception as e:  # noqa: BLE001
            _journal_append(run_id, {"t": "run_end", "ok": False, "counts": {"BLOCKED": 1}})
            print(json.dumps({"ok": False, "error": f"GAS_UNAVAILABLE: {e}", "journal": run_id},
                             ensure_ascii=False), file=sys.stderr)
            return 2
        try:
            _topo_m = _resolve_shard_topology(entries, (os.environ.get("TL_NOTEBOOK_ID")
                                                        or NLM_BASE_NOTEBOOK or "").strip())
        except Exception:  # noqa: BLE001
            _topo_m = {"shards": []}
        _rk_target = _shard_row_kind(to_nb, _topo_m)
        for it in plan["repoint"]:
            payload_u = {"drive_id": it["drive_id"], "nlm_source_id": it["phys_sid"],
                         "nlm_notebook_id": to_nb, "nlm_status": "pushed"}
            before_u = dict(it.get("before") or {})
            _cur_rk = str(it.get("row_kind_before") or "").strip().lower()
            if _rk_target == "overflow" and _cur_rk not in _ROW_KIND_PROTECTED:
                payload_u["row_kind"] = "overflow"
                before_u["row_kind"] = _cur_rk
            v = _journaled_reg_upsert(run_id, g, payload_u, before=before_u)
            _ok_i = bool(v.get("verified"))
            ok_all = ok_all and _ok_i
            results["repoint"].append({"drive_id": it["drive_id"], "phys_sid": it["phys_sid"], "ok": _ok_i,
                                       **({"error": v.get("error")} if not _ok_i else {})})
        try:
            _keys_v = [it["drive_id"] for it in plan["repoint"]]
            _sid_by_did = {it["drive_id"]: it["phys_sid"] for it in plan["repoint"]}
            _rgb = g.get("reg_get_bulk", keys=json.dumps(_keys_v), key_field="drive_id")
            _rows_v = {str(x.get("drive_id") or ""): x for x in (_rgb.get("rows") or [])}
            _bad_v = [k for k in _keys_v
                      if str((_rows_v.get(k) or {}).get("nlm_source_id") or "") != _sid_by_did[k]
                      or str((_rows_v.get(k) or {}).get("nlm_notebook_id") or "") != to_nb]
            results["repoint_verified"] = not _bad_v
            if _bad_v:
                ok_all = False
                results["repoint_verify_failed"] = _bad_v
        except Exception as _ev:  # noqa: BLE001
            results["repoint_verified"] = False
            results["repoint_verify_error"] = f"{type(_ev).__name__}: {_ev}"[:160]
            ok_all = False
    add_mode = None
    links = []
    if plan["add"]:
        if len(plan["add"]) > NLM_BATCH_LINKS_THRESHOLD and not getattr(a, "api_add", False):
            add_mode = "BATCH_LINKS"
            links = [_entry_links_url(it.get("row") or {"drive_id": it["drive_id"]}) for it in plan["add"]]
        else:
            add_mode = "API"
            for it in plan["add"]:
                _ns_add = argparse.Namespace(notebook_id=to_nb, drive_id=it["drive_id"], url=None, file=None,
                                             type=None, title=(str(it.get("name") or "")[:120] or None),
                                             no_wait=False, wait=False, skip_live_check=False, json=False,
                                             config=getattr(a, "config", None),
                                             profile=getattr(a, "profile", None))
                _rc_add = cmd_nlm_add(_ns_add)
                _ok_a = _rc_add == 0
                ok_all = ok_all and _ok_a
                results["add"].append({"drive_id": it["drive_id"], "ok": _ok_a, "rc": _rc_add})
    _journal_append(run_id, {"t": "run_end", "ok": ok_all,
                             "counts": {**counts, "add_fail": sum(1 for x in results["add"] if not x["ok"])},
                             "add_mode": add_mode})
    payload = {"ok": ok_all, "schema": "nlm_migrate.v1", "to": to_nb, "journal": run_id, "counts": counts,
               "mode": add_mode, "repoint": results["repoint"], "repoint_verified": results["repoint_verified"],
               **({"repoint_verify_failed": results.get("repoint_verify_failed")} if results.get("repoint_verify_failed") else {}),
               **({"repoint_verify_error": results.get("repoint_verify_error")} if results.get("repoint_verify_error") else {}),
               "add": results["add"], **({"links": links} if links else {}),
               "cleanup": plan["cleanup"], "cleanup_commands": cleanup_cmds,
               "next": "CHẠY LẠI đúng lệnh này sau khi dán links / để harvest (ADD → REPOINT → POINTER_OK)."}
    if add_mode == "BATCH_LINKS" and not (getattr(a, "json", False) or getattr(a, "out", None)):
        for ln in links:
            print(ln)
        print(f"[tl] nlm-migrate BATCH_LINKS: {len(links)} link — dán TOÀN BỘ stdout vào Add source → Websites "
              f"của https://notebooklm.google.com/notebook/{to_nb}", file=sys.stderr)
        print("[tl]   Dán xong: CHẠY LẠI đúng lệnh này (plan mới tự thấy nguồn ở đích → REPOINT/harvest).",
              file=sys.stderr)
        if results["repoint"]:
            print(f"[tl]   repoint: {len(results['repoint'])} dòng, verified={results['repoint_verified']}",
                  file=sys.stderr)
        for c in cleanup_cmds:
            print(f"[tl]   {c}", file=sys.stderr)
    else:
        _emit_json_payload(payload, getattr(a, "out", None))
    return 0 if ok_all else 2
