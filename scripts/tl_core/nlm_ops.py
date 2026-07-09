# -*- coding: utf-8 -*-
"""tl_core.nlm_ops — I2 (v1.34.4): tách NGUYÊN VĂN cụm NLM-wrappers/sharding từ scripts/tl.py.

KHÔNG gọi trực tiếp từ ngoài — public CLI vẫn là scripts/tl.py (stub ủy quyền). bind(tl) REBASE
__globals__ của TỪNG HÀM về namespace SỐNG của tl (bài học I1: monkeypatch selftest trên tl thấm ngay,
helper không stale; copy-snapshot làm r54 gãy). Hành vi khoá bởi 5 wiring-test r71a (commit TRƯỚC cut)
+ selftest hiện có (dedup-gate/reconcile-plan/invariants/slot-count) — phải pass y nguyên sau cut.
Helper đa-cụm (_entry_on_nlm_live/_resolve_nlm_notebook/_nlm_display/...) GIỮ Ở TL — hàm ở đây resolve
chúng qua globals tl nhờ rebase."""
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

# MIRROR tl.py (default-param `cap=NLM_SLOT_CAP` của _overflow_status eval lúc ĐỊNH NGHĨA module — TRƯỚC
# bind nên không lấy từ tl được; r71 drift-lock khoá nlm_ops.NLM_SLOT_CAP == tl.NLM_SLOT_CAP).
NLM_SLOT_CAP = 300


def bind(tl_module) -> None:
    """REBASE __globals__ từng hàm đã chuyển về namespace SỐNG của tl (I1/I2 — KHÁC copy-snapshot sibling cũ)."""
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



def _preflight_invariants(state: dict) -> list:
    """PURE (test offline): các BẤT BIẾN phải đúng TRƯỚC mọi ghi mutate — gom guard rải rác từ 18 sự cố thật.
    state: {registryDocId, is_base_profile, profile_registry_id, write_cols?, snapshot_age_seconds?, stale_threshold?}.
    Trả list {name, ok, severity(critical|warn), detail}. critical fail = ABORT (Pha 1 nhúng vào --apply)."""
    checks = []

    def add(name, ok, sev, detail):
        checks.append({"name": name, "ok": bool(ok), "severity": sev, "detail": detail})

    rid = str(state.get("registryDocId") or "").strip()
    # (1) clobber/mispoint: registryDocId trỏ Doc legacy 1mATG → Doc-as-Sheet đọc rỗng count=0 ẢO.
    add("REGISTRY_NOT_LEGACY_DOC", rid != _LEGACY_REGISTRY_DOC_ID, "critical",
        "registryDocId trỏ Doc legacy 1mATG → sửa về Sheet tra_luat_registry / để rỗng auto-discover" if rid == _LEGACY_REGISTRY_DOC_ID else "OK")
    # (2) CLOBBER 766 dòng: profile dự án registryDocId RỖNG → ghi/regen2 rơi nhánh BASE → xoá sạch registry nền.
    if not state.get("is_base_profile", True):
        add("PROFILE_REGISTRY_ID_NOT_EMPTY", bool(str(state.get("profile_registry_id") or "").strip()), "critical",
            "profile dự án registryDocId RỖNG → ghi rơi nhánh BASE → CLOBBER registry nền (tạo registry riêng TRƯỚC)")
    # (3) ghi mù: cột định ghi phải ∈ schema (so_hieu≠sohieu bị bỏ im lặng).
    if state.get("write_cols") is not None:
        ok_cols, bad = _reg_cols_valid(state["write_cols"])
        add("WRITE_COLS_IN_SCHEMA", ok_cols, "critical",
            f"Cột lạ {bad} → webapp BỎ IM LẶNG (patched=0 không báo)" if bad else "OK")
    # (4) stale cache: snapshot quá cũ so với ngưỡng (GAS cache ~600s → nên >900s là đáng refresh).
    if state.get("snapshot_age_seconds") is not None:
        thr = int(state.get("stale_threshold") or 900)
        age = int(state["snapshot_age_seconds"])
        add("MANIFEST_FRESH", age <= thr, "warn",
            f"snapshot {age}s (>{thr}s) — chạy `tl manifest` + `tl boot --refresh` trước khi ghi (GAS cache ~600s)" if age > thr else "OK")
    return checks


def _preflight_verdict(checks: list) -> dict:
    """PURE: gộp verdict. ok = KHÔNG có critical fail. blockers/warnings = tên các check hỏng."""
    blockers = [c["name"] for c in (checks or []) if not c["ok"] and c["severity"] == "critical"]
    warnings = [c["name"] for c in (checks or []) if not c["ok"] and c["severity"] == "warn"]
    return {"ok": not blockers, "blockers": blockers, "warnings": warnings}


def _raw_on_nlm_rows(entries: list[dict]) -> list[dict]:
    """C2 (v1.33.4 — log: 'luat-dau-thau-…-d1.html' mime text/html, corpus=true, nlm_status=pushed — file THÔ
    đã bị đẩy thẳng làm nguồn NLM, trái quy tắc 'chỉ push GDoc'): gate #3 `_nlm_dedup_gate` chỉ chặn push MỚI —
    hàng tồn CŨ phải có detector quét ra. Fix từng ca: convert GDoc (copy_convert) → re-push → gỡ nguồn raw
    (source_delete) + dọn mapping (reg_clear) — xem hàng trong raw_on_nlm_rows."""
    return [e for e in entries if _entry_raw_no_gdoc(e) and _entry_on_nlm_live(e)]


def _nlm_slot_count(entries: list[dict], notebook_id: str, base_notebook_id: str | None = None) -> dict:
    active = {"pushed", "synced", "added", "stale", "true", "1", "yes"}
    base_notebook_id = (base_notebook_id or NLM_BASE_NOTEBOOK).strip()
    is_base = notebook_id == base_notebook_id
    total_status = 0
    matching = 0
    unknown_notebook = 0
    for e in entries or []:
        if _entry_row_kind(e) == "ref":
            continue
        status = str(e.get("nlm_status") or e.get("nlm") or "").strip().lower()
        src = e.get("nlm_source_id") or e.get("source_id")
        # L5 (26/6): dòng đã GỠ khỏi NLM (removed*/other_notebook) KHÔNG tính slot dù còn nlm_source_id sót
        # (registry trước đếm cả removed_below_nd/superseded ⇒ used=322 > live 300).
        if status.startswith("removed") or status in ("other_notebook", "deleted", "gone"):
            continue
        if not src and status not in active:
            continue
        if status in active or src:
            total_status += 1
            nb = str(e.get("nlm_notebook_id") or e.get("notebook_id") or "").strip()
            if nb == notebook_id:
                matching += 1
            elif not nb:
                unknown_notebook += 1
    # v1.18 base-fallback: dòng rỗng nlm_notebook_id quy về notebook nền (VBQPPL). Vì vậy slot HIỆU DỤNG
    # của notebook nền = matching + rỗng; notebook dự án khác = matching (KHÔNG cộng dòng rỗng → hết full giả).
    slots_effective = matching + (unknown_notebook if is_base else 0)
    return {
        "notebook_id": notebook_id,
        "base_notebook_id": base_notebook_id,
        "is_base_notebook": is_base,
        "slots_for_notebook": matching,
        "slots_effective": slots_effective,
        "rows_with_nlm_status_any_notebook": total_status,
        "rows_missing_nlm_notebook_id": unknown_notebook,
        "rule": "nlm_slots/nlm_preflight chỉ đếm rows có nlm_notebook_id == notebookId; dòng rỗng quy về base_notebook_id (VBQPPL). slots_effective khớp Code.2.21.2i.gs.",
        "warning": "Dòng rỗng nlm_notebook_id chỉ tính vào notebook nền (VBQPPL); notebook dự án nên backfill nlm_notebook_id hoặc dùng registry riêng theo profile.",
    }


def _slot_count_all_shards(entries: list) -> dict:
    """KH1 Pha 1.3 (II.5, PURE): đếm slot HIỆU LỰC theo TỪNG shard (nlm_notebook_id) — base + mọi overflow. Bỏ
    removed*/ref. Trả {notebook_id: count}. Dùng cảnh báo shard sắp đầy (>270/300) để chuẩn bị shard kế."""
    from collections import Counter as _C
    _active = {"pushed", "synced", "added", "stale", "true", "1", "yes"}
    c = _C()
    for e in entries or []:
        if _entry_row_kind(e) == "ref":
            continue
        status = str(e.get("nlm_status") or e.get("nlm") or "").strip().lower()
        src = e.get("nlm_source_id") or e.get("source_id")
        if status.startswith("removed") or status in ("other_notebook", "deleted", "gone"):
            continue
        if not src and status not in _active:
            continue
        nb = str(e.get("nlm_notebook_id") or e.get("notebook_id") or "").strip()
        if nb:
            c[nb] += 1
    return dict(c)


def cmd_slot_audit(a) -> int:
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    if a.manifest:
        try:
            data = json.loads(Path(a.manifest).read_text(encoding="utf-8", errors="replace"))
        except Exception as e:
            print(f"[tl] slot-audit lỗi đọc manifest: {e}", file=sys.stderr)
            return 1
        entries = data if isinstance(data, list) else (data.get("entries") or data.get("files") or [])
    else:
        try:
            entries = _manifest_entries(refresh=getattr(a, "refresh", False))
        except Exception as e:
            print(f"[tl] slot-audit: không đọc được manifest: {e}", file=sys.stderr)
            return 1
    if getattr(a, "all_shards", False):
        # KH1 Pha 1.3 (II.5): đếm slot theo TỪNG shard + cảnh báo shard >ngưỡng (mặc định 270/300) để chuẩn bị shard kế.
        near = getattr(a, "near_full", None) or 270
        per = _slot_count_all_shards(entries)
        rows = sorted(per.items(), key=lambda kv: (-kv[1], kv[0]))
        warn = [{"notebook_id": nb, "count": n, "cap": NLM_SLOT_CAP} for nb, n in rows if n >= near]
        res = {"ok": True, "gate": "slot-audit", "cap": NLM_SLOT_CAP, "near_full_threshold": near,
               "shards": [{"notebook_id": nb, "count": n, "near_full": n >= near, "full": n >= NLM_SLOT_CAP} for nb, n in rows],
               "near_full_shards": warn}
        if getattr(a, "json", False):
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(f"== slot-audit --all-shards · {len(rows)} shard · cap={NLM_SLOT_CAP} ngưỡng near-full={near} ==")
            for nb, n in rows:
                mk = "✗ FULL" if n >= NLM_SLOT_CAP else ("⚠ NEAR" if n >= near else "·")
                print(f"  {mk:7s} {nb[:40]:40s} {n}/{NLM_SLOT_CAP}")
            if warn:
                print(f"  ⚠ {len(warn)} shard ≥{near} → chuẩn bị shard kế (đừng để ingest-missing chạm BLOCKED).")
        return 0
    notebook_id = a.notebook_id or os.environ.get("TL_NOTEBOOK_ID", "")
    if not notebook_id:
        print("[tl] slot-audit cần --notebook-id hoặc TL_NOTEBOOK_ID/profile config (hoặc --all-shards)", file=sys.stderr)
        return 1
    out = _nlm_slot_count(entries, notebook_id, getattr(a, "base_notebook_id", None))
    # WS1: neo SỨC CHỨA VẬT LÝ từ `tl nlm-get` (CLI nlm notebook get; registry chỉ là ước lượng dedup).
    # A3: TỰ neo live_source_count từ nlm CLI (khỏi gọi --physical tay); --no-live để bỏ qua (offline/không cred).
    phys = getattr(a, "physical", None)
    if phys is None and not getattr(a, "no_live", False):
        try:
            _nc = _imp("nlm_cli")
            _ng = _nc.notebook_get(notebook_id)
            # M2 (v1.33.35 — log rà 45 Luật: slot-audit lệch −288 GIẢ khi NLM auth hết hạn): notebook_get trả
            # {ok:False, auth_hint} khi cookie chết — KHÔNG raise → cũ `.get("source_count") or 0` = 0 → gap
            # = 0 − 288 = −288 giả. Nay kiểm .ok TRƯỚC: ok=False → live_read_failed, KHÔNG coi là 0 vật lý.
            if _ng.get("ok"):
                phys = int(_ng.get("source_count") or 0)
                out["live_source_count"] = phys
            else:
                out["live_read_failed"] = True
                out["live_note"] = ("KHÔNG đọc được live source_count (" + str(_ng.get("error") or "?")[:120] + ")"
                                    + (" — 🔴 AUTH hết hạn: `nlm login`" if _ng.get("auth_hint") else "")
                                    + " → KHÔNG suy gap (dùng `--physical N` neo tay nếu cần).")
        except Exception as e:  # noqa: BLE001 — không có cred/offline → bỏ qua, KHÔNG chặn
            out["live_read_failed"] = True
            out["live_note"] = (f"không lấy được live source_count ({type(e).__name__}) — dùng `--physical N` để neo "
                                f"thủ công, hoặc `--no-live` để tắt.")
    if phys is not None:
        reg = out.get("slots_effective", 0)
        out["physical_source_count"] = phys
        out["registry_estimate"] = reg
        out["gap"] = phys - reg
        out["ground_truth"] = "physical (tl nlm-get / nlm notebook get)"
        if out["gap"] != 0:
            out["warning"] = (f"Lệch {phys} vật lý vs {reg} registry ({out['gap']:+d}) — backfill nlm_notebook_id "
                              f"(`tl backfill-notebook`) hoặc nguồn add thẳng chưa ghi registry.")
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        line = (f"notebook={out['notebook_id']} used={out['slots_effective']} "
                f"matching={out['slots_for_notebook']} missing_nb={out['rows_missing_nlm_notebook_id']}")
        if phys is not None:
            line += f" | VẬT LÝ={phys} gap={out['gap']:+d}"
        print(line)
        if out.get("warning"):
            print("  ⚠ " + out["warning"])
        if out.get("live_read_failed"):   # M2: không im lặng nuốt lỗi đọc live thành 0-vật-lý
            print("  ⚠ " + out.get("live_note", "không đọc được live source_count"))
    return 0


def cmd_nlm_list(a) -> int:
    """B: liệt kê nguồn live của notebook qua CLI `nlm` (fast-lane, ~4s, --skip-freshness) —
    KHÔNG qua MCP source_list_drive (timeout ~4'). Gate: nlm trên PATH + auth OK; else fallback."""
    nb = getattr(a, "notebook_id", None) or os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK
    try:
        nc = _imp("nlm_cli")
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"không import được nlm_cli: {e}"}, ensure_ascii=False), file=sys.stderr); return 2
    r = nc.source_list(nb, skip_freshness=not getattr(a, "no_skip_freshness", False))
    if not r.get("ok"):
        print(json.dumps(r, ensure_ascii=False, indent=2), file=sys.stderr)
        print("[tl] nlm CLI không dùng được → fallback MCP `notebook_get` hoặc chạy `nlm login`.", file=sys.stderr)
        return 2
    if getattr(a, "json", False) or getattr(a, "out", None):
        _emit_json_payload(r, getattr(a, "out", None))   # N5 v1.33.41: --out atomic (đối soát đủ, né trần 30s)
    else:
        print(f"notebook={nb} · {r['count']} nguồn live (nlm-cli, skip_freshness={r.get('skip_freshness')})")
        # N5 (v1.33.41 — log rà VBHN-first: nlm-list cắt ~14 dòng IM LẶNG dù tổng đúng → không đối soát thành
        # viên được, phải dùng `nlm source list -d` thô 2000+ dòng): --max 0 = TẤT CẢ; cắt thì báo LOUD.
        _mx = getattr(a, "max", 15)
        _mx = len(r["sources"]) if (_mx is not None and int(_mx) == 0) else (_mx or 15)
        for s in r["sources"][:int(_mx)]:
            print(f"  - {s.get('id')} | {str(s.get('title',''))[:60]} | {s.get('type','')}")
        if len(r["sources"]) > int(_mx):
            print(f"  … còn {len(r['sources']) - int(_mx)} nguồn BỊ CẮT hiển thị — xem hết: --max 0 / --json / --out <file>")
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
       unregistered    = live id không link được dòng nào (NLM có, registry thực sự thiếu).
       v1.19.9: tách already_removed khỏi desync_real. C1: chấp nhận live_sources = list[dict] (mới) hoặc set ids (cũ)."""
    if isinstance(live_sources, (set, frozenset)):
        sources = [{"id": x} for x in live_sources]
    else:
        sources = list(live_sources or [])
    live_ids = {str(s.get("id")) for s in sources if s.get("id")}
    reg_ids = set()
    by_drive: dict[str, dict] = {}
    by_sohieu: dict[str, dict] = {}
    n_rows, backfill, desync_real, already_removed, other_notebook = 0, [], [], [], []
    for e in entries:
        did = _entry_drive_id(e)
        if did:
            by_drive.setdefault(did, e)
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
        elif nb and nb != notebook_id:
            other_notebook.append(e)   # v1.19.11: thuộc shard/notebook KHÁC (vd overflow VBQPPL-2) → KHÔNG phải desync
        else:
            st = str(e.get("nlm_status") or "").strip().lower()
            (already_removed if st.startswith("removed") else desync_real).append(e)
    # C1: bắc cầu gdoc↔source_id cho nguồn live 'chưa đăng ký' (id KHÔNG ∈ reg_ids).
    link_candidates, still_unreg = [], []
    for s in sources:
        sid = str(s.get("id") or "")
        if not sid or sid in reg_ids:
            continue
        did = _nlm_source_drive_id(s)
        ent = by_drive.get(did) if did else None
        by = "drive_id"
        if ent is None:
            shk = _sohieu_key_entry({"name": s.get("title") or "", "so_hieu": s.get("sohieu") or s.get("so_hieu") or ""})
            _cands = by_sohieu.get(shk) or [] if shk else []
            ent = _cands[0] if len(_cands) == 1 else None   # CHỈ link theo số hiệu khi DUY NHẤT (tránh false-link reuse)
            by = "sohieu"
        if ent is not None and (_entry_nlm(ent) or "").strip() != sid:
            link_candidates.append({"entry": ent, "source_id": sid, "by": by, "title": s.get("title") or ""})
        else:
            still_unreg.append(sid)
    return {"backfill": backfill, "desync_real": desync_real, "already_removed": already_removed,
            "other_notebook": other_notebook,
            "stale": desync_real,  # giữ khóa cũ = desync_real (tương thích ngược)
            "link_candidates": link_candidates,
            "unregistered": sorted(still_unreg),
            "registry_on_nlm_rows": n_rows}


def cmd_nlm_reconcile(a) -> int:
    """C (WS1): đối soát registry↔NLM bằng ground-truth từ CLI nlm. Backfill nlm_notebook_id cho dòng
    THỰC SỰ trên NLM; báo (và --clear-stale thì clear) dòng 'pushed' nhưng KHÔNG trên NLM. DRY mặc định."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    nb, _nberr = _resolve_nlm_notebook(getattr(a, "notebook_id", None))
    if _nberr:
        print(json.dumps({"ok": False, "error": _nberr}, ensure_ascii=False), file=sys.stderr); return 2
    try:
        nc = _imp("nlm_cli")
        live = nc.source_list(nb, skip_freshness=True)
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"nlm_cli lỗi: {e}"}, ensure_ascii=False), file=sys.stderr); return 2
    if not live.get("ok"):
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
           "unregistered_on_nlm": len(plan["unregistered"]),
           "mode": "APPLY" if getattr(a, "apply", False) else "DRY",
           "backfill_sample": [f"{_entry_nlm(e)}|{_entry_sohieu(e) or _sohieu_key_entry(e)}|{_entry_name(e)[:40]}" for e in plan["backfill"][:10]],
           "link_candidates_sample": [f"{c['source_id'][:12]}…→{_entry_drive_id(c['entry'])[:12]}… (by {c['by']}) | {(_entry_sohieu(c['entry']) or _entry_name(c['entry'])[:32])}" for c in (plan.get("link_candidates") or [])[:10]],
           "desync_real_sample": [f"{_entry_sohieu(e)}|{_entry_name(e)[:40]}" for e in plan["desync_real"][:10]],
           "unregistered_sample": plan["unregistered"][:8]}
    if not getattr(a, "apply", False):
        out["note"] = ("DRY. --apply: reg_bulk nlm_notebook_id cho backfill + LINK nlm_source_id cho link_candidates "
                       "(bắc cầu gdoc↔source_id). --clear-stale: CHỈ clear desync_real (status pushed/synced nhưng vắng "
                       "NLM); KHÔNG đụng already_removed (đã gỡ có chủ đích).")
        _emit_json_payload(out, getattr(a, "out", None)); return 0
    _ok_gate, _pfv = _apply_gate(a, write_cols="nlm_source_id,nlm_notebook_id,nlm_status")   # (Pha 1) chống clobber/ghi-mù
    if not _ok_gate:
        return 2
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))   # cần webapp để reg_bulk/reg_clear
    g = _gas()
    run_id = _apply_journal_start("nlm-reconcile", {"notebook": nb, "backfill": len(plan["backfill"]),
                                                    "link": len(plan.get("link_candidates") or [])})
    if plan["backfill"]:
        items = [{"nlm_source_id": _entry_nlm(e), "nlm_notebook_id": nb} for e in plan["backfill"]]
        _bf_before = {_entry_nlm(e): {"nlm_notebook_id": str(e.get("nlm_notebook_id") or "")} for e in plan["backfill"]}
        v = _journaled_reg_write(run_id, g, items, "nlm_notebook_id", key_field="nlm_source_id", before_by_key=_bf_before)
        rb = v.get("reg_bulk") or {}
        out["reg_bulk"] = {"ok": rb.get("ok"), "patched": v.get("patched"), "missed": rb.get("missed"), "verified": v.get("verified")}
    # C1: LINK nguồn live chưa-đăng-ký vào đúng dòng registry (khóa drive_id) → set nlm_source_id+notebook+status.
    if plan.get("link_candidates"):
        litems = [{"drive_id": _entry_drive_id(c["entry"]), "nlm_source_id": c["source_id"],
                   "nlm_notebook_id": nb, "nlm_status": "pushed"} for c in plan["link_candidates"] if _entry_drive_id(c["entry"])]
        _ln_before = {it["drive_id"]: {"nlm_source_id": ""} for it in litems}   # trước: chưa có source_id → undo = clear
        vl = _journaled_reg_write(run_id, g, litems, "nlm_source_id,nlm_notebook_id,nlm_status", before_by_key=_ln_before)
        rl = vl.get("reg_bulk") or {}
        out["reg_bulk_link"] = {"ok": rl.get("ok"), "patched": vl.get("patched"), "missed": rl.get("missed"), "verified": vl.get("verified")}
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


def _sohieu_loose(s: str) -> str:
    """Khóa số hiệu LỎNG-NĂM: bỏ token năm để '72/NQ-TW' ≡ '72-2025-NQ-TW' (L4)."""
    k = norm_sohieu(s or "")
    return re.sub(r"-(19|20)\d{2}(?=-|$)", "", k)


def _discover_overflow_from_registry(entries: list[dict], main_nb: str) -> str:
    """Khám phá overflow notebook từ REGISTRY khi config để trống/placeholder: lấy nlm_notebook_id PHỔ BIẾN NHẤT
    ở các dòng row_kind='overflow' (≠ notebook chính). Webapp nlm_preflight KHÔNG tự discover ⇒ client phải truyền vào."""
    main_nb = (main_nb or "").strip()
    counts: dict[str, int] = {}
    for e in entries or []:
        if _entry_row_kind(e) != "overflow":
            continue
        nb = str(e.get("nlm_notebook_id") or e.get("notebook_id") or "").strip()
        if nb and nb != main_nb:
            counts[nb] = counts.get(nb, 0) + 1
    if not counts:
        return ""
    # nhiều nhất trước; hoà thì theo id (ổn định)
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


def cmd_preflight(a) -> int:
    """Định tuyến nạp 1 VBQPPL mới: gọi GAS nlm_preflight(notebookId=shard chính, overflowNotebookId từ config).
    decision=ADD ⇒ source_add vào notebookId; REVIEW+NOTEBOOK_NEAR_FULL_ROUTE_OVERFLOW ⇒ add vào overflow_route.notebookId
    (rồi `tl push-overflow`); SKIP ⇒ trùng/đầy không overflow. KHÔNG ghi gì (advisory)."""
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    nb = getattr(a, "notebook_id", None) or os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK
    overflow = getattr(a, "overflow_notebook_id", None) or os.environ.get("TL_OVERFLOW_NOTEBOOK_ID") or ""
    overflow_auto = False
    # FIX: overflowNotebookId từ config RỖNG/placeholder (vd 'TL_OVERFLOW_NOTEBOOK_ID') ⇒ webapp KHÔNG tự discover,
    # sẽ trả SKIP/NOTEBOOK_FULL với overflow_route=null. Tự KHÁM PHÁ từ registry (dòng row_kind=overflow phổ biến nhất).
    # v1.29.3 (AUDIT B2 #4): nạp manifest 1 LẦN dùng chung (trước: 2 lần parse ~800KB JSON / invocation —
    # discover-overflow + dedup-loose mỗi nơi tự gọi _manifest_entries).
    _pf_entries = None
    try:
        _pf_entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception:
        _pf_entries = None
    if (not overflow) or overflow == "TL_OVERFLOW_NOTEBOOK_ID" or "-" not in overflow:
        try:
            disc = _discover_overflow_from_registry(_pf_entries or [], nb)
        except Exception:
            disc = ""
        if disc:
            overflow, overflow_auto = disc, True
    q = getattr(a, "query", None) or getattr(a, "sohieu", None) or getattr(a, "name", None) or ""
    if not q:
        print("[tl] preflight cần <query> | --sohieu | --name", file=sys.stderr); return 2
    g = _gas()
    params = {"notebookId": nb, "normative": "true", "refresh": "true" if getattr(a, "refresh", False) else "false"}
    if overflow:
        params["overflowNotebookId"] = overflow
    if getattr(a, "sohieu", None): params["soHieu"] = a.sohieu
    if getattr(a, "name", None):   params["name"] = a.name
    if getattr(a, "query", None):  params["q"] = a.query
    if getattr(a, "drive_id", None): params["driveId"] = a.drive_id
    if getattr(a, "md5", None):      params["md5"] = a.md5
    r = g.get("nlm_preflight", **params)
    # L4 (26/6): dedup PHÍA TL — webapp so literal tên/số hiệu → bỏ sót trùng KHÁC TÊN (72-NQ-TW ≡ 72-2025-NQ-TW).
    tl_dups = []
    sh_q = getattr(a, "sohieu", None) or (getattr(a, "query", None) if "/" in str(getattr(a, "query", "") or "") else None)
    if sh_q:
        try:
            kq = _sohieu_loose(sh_q)
            for e in (_pf_entries or []):     # tái dùng manifest đã nạp 1 lần ở trên (v1.29.3)
                if kq and _entry_nlm(e) and _sohieu_loose(_entry_sohieu(e)) == kq:
                    tl_dups.append({"sohieu": _entry_sohieu(e), "name": _entry_name(e)[:60], "drive_id": _entry_drive_id(e)[:16]})
        except Exception:
            pass
    # L5 (26/6): verify-LIVE slot qua nlm-get (CLI) khi webapp báo FULL (registry có thể đếm cả removed_*).
    slots = r.get("slots") or {}
    live_cnt = None
    if slots.get("full"):
        try:
            live_cnt = _imp("nlm_cli").notebook_get(nb).get("source_count")
        except Exception:
            pass
    r["tl_dedup_loose"] = tl_dups
    r["live_source_count"] = live_cnt
    if overflow_auto:
        r["overflow_auto_discovered"] = overflow
    if getattr(a, "json", False):
        print(json.dumps(r, ensure_ascii=False, indent=2)); return 0 if r.get("ok") else 1
    print(f"== preflight · {q} ==")
    print(f"  decision : {r.get('decision')}  reasons={r.get('reasons')}")
    print(f"  notebook : {nb}  slots: used={slots.get('used')}/{slots.get('cap')} remaining={slots.get('remaining')} full={slots.get('full')} near_full={slots.get('near_full')}")
    if overflow:
        _osrc = "  (auto-discovered from registry: row_kind=overflow)" if overflow_auto else ""
        print(f"  overflow : {overflow}{_osrc}" + (f"  → route={(r.get('overflow_route') or {}).get('notebookId')}" if r.get("overflow_route") else ""))
    if (r.get("dedup") or {}).get("duplicate"):
        print(f"  DUP      : {(r.get('dedup') or {}).get('hits')}")
    if r.get("superseded_matches"):
        print(f"  SUPERSEDED: {len(r['superseded_matches'])} bản cũ — cân nhắc VBHN-first")
    if tl_dups:
        print(f"  ⚠ DUP-TL  : {len(tl_dups)} bản CÙNG SỐ HIỆU (lỏng-năm) đã trên NLM — có thể KHÁC TÊN, ĐỪNG push lại:")
        for d in tl_dups[:4]:
            print(f"             {d['sohieu']} | {d['name']} | {d['drive_id']}")
    if live_cnt is not None:
        cap = slots.get("cap") or 300
        if live_cnt < cap:
            print(f"  ⚠ SLOT    : webapp báo FULL nhưng LIVE nlm-get={live_cnt}/{cap} → registry đếm cả removed_*; verify-live trước khi chốt FULL/overflow.")
        else:
            print(f"  ✓ SLOT    : LIVE nlm-get={live_cnt}/{cap} (đầy thật).")
    print(f"  → {r.get('note','')}")
    return 0 if r.get("ok") else 1


def cmd_push_overflow(a) -> int:
    """Sau khi source_add (MCP) văn bản VBQPPL vào shard overflow: cập nhật registry dòng tương ứng
    nlm_notebook_id=<overflow>, row_kind='overflow', nlm_status='pushed', nlm_source_id=<mới>. KHÔNG tự source_add."""
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    nb = getattr(a, "notebook_id", None) or os.environ.get("TL_OVERFLOW_NOTEBOOK_ID") or ""
    if not (a.drive_id and a.source_id and nb):
        print("[tl] push-overflow cần --drive-id --source-id (và overflow notebook trong config hoặc --notebook-id)", file=sys.stderr); return 2
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


def _nlm_dedup_gate(nc, notebook_id: str, targets: list, skip: bool = False) -> tuple:
    """(v1.29.3 — AUDIT B3 #3) CỔNG dedup-live BẮT BUỘC trước MỌI đường source_add (nlm-add / profile-ingest /
    ingest-local): liệt kê nguồn LIVE notebook đích rồi khớp drive_id / exact-title.
    v1.29.7 (log NĐ131 #4 — dương tính giả): BỎ tầng SOHIEU khỏi GATE — chính văn + PHỤ LỤC chia sẻ CÙNG số hiệu
    (tên 'PL_131-2021…' parse ra key '131-2021-ND-CP' = key chính văn) → phụ lục hợp lệ bị chặn
    TITLE_ALREADY_ON_NOTEBOOK trỏ nhầm source_id chính văn, phải --skip-live-check tay. Gate chống RE-PUSH CÙNG
    MỘT TÀI LIỆU → chỉ drive_id (định danh cứng) + exact-title-duy-nhất (title tool tự đặt khi add) là đúng thước;
    biến thể cùng-số-hiệu (phụ lục/bản tách) là nguồn RIÊNG hợp lệ. (ingest-missing GIỮ 3 tầng — backlog của nó
    là bản chuẩn hoá 1-1 với sohieu, tier-sohieu ở đó là lưới cứu timeout.)
    targets = list[{'drive_id','name'}]. Trả (verdict, dups): verdict ∈ {'clear','dup','list_failed','skipped'};
    dups=[(pseudo, source_id)]. Doctrine S13: KHÔNG liệt kê được LIVE → caller DỪNG trừ --skip-live-check.
    KHÔNG raise; KHÔNG ghi gì (read-only gate)."""
    if skip:
        return "skipped", []
    try:
        r = nc.source_list(notebook_id, skip_freshness=True, drive=True)
        if not r.get("ok"):
            return "list_failed", []
        live_by_drive, live_by_title = {}, {}
        for s in (r.get("sources") or []):
            d = _nlm_source_drive_id(s)
            if d:
                live_by_drive.setdefault(d, s)
            tk = _ingest_dedup_title_key(s.get("title"))
            if tk:
                live_by_title.setdefault(tk, []).append(s)
        dups = []
        for e in (targets or []):
            s = live_by_drive.get(str(e.get("drive_id") or ""))
            if s is None:
                tk = _ingest_dedup_title_key(str(e.get("name") or "")[:120])
                tc = (live_by_title.get(tk) or []) if tk else []
                s = tc[0] if len(tc) == 1 else None
            if s and s.get("id"):
                dups.append((e, str(s.get("id"))))
        return ("dup" if dups else "clear"), dups
    except Exception:  # noqa: BLE001
        return "list_failed", []


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


def _overflow_route(base_room: int, overflow_shard: str, overflow_room: int) -> tuple:
    """PURE (test offline): định tuyến nạp THEO CHỖ TRỐNG, BẤT BIẾN KHÔNG BAO GIỜ tạo notebook. Trả (route, shard, reason).
    route ∈ {base, overflow, blocked}; KHÔNG có 'create'. blocked = mọi shard đầy → caller HỎI người dùng duyệt shard mới."""
    if base_room > 0:
        return ("base", None, "base còn chỗ")
    if overflow_shard and overflow_room > 0:
        return ("overflow", overflow_shard, "OVERFLOW_SHARD_EXISTS_DO_NOT_CREATE: base đầy → dùng shard overflow SẴN CÓ")
    if overflow_shard:
        return ("blocked", overflow_shard, "ALL_SHARDS_FULL: base+overflow đầy → HỎI người dùng duyệt shard mới (KHÔNG auto-create)")
    return ("blocked", None, "NO_OVERFLOW_SHARD_ROOM: base đầy + chưa có shard overflow → HỎI người dùng (KHÔNG auto-create)")


def _overflow_status(base_reg, base_phys, overflow, ov_reg, ov_phys, cap=NLM_SLOT_CAP) -> dict:
    """PURE (test offline): trạng thái shard dùng MAX(registry, physical) làm slot HIỆU LỰC — AN TOÀN, không under-count
    khi VẬT LÝ vượt registry (vd base registry 279 nhưng nlm-get 315 → dùng 315). Trả {base_used, overflow_used, route,
    flag, registry_live_gap[]}. gap = shard có physical>registry (nguồn add thẳng CHƯA đăng ký → cần nlm-reconcile)."""
    bu = max(int(base_reg or 0), int(base_phys or 0))
    ou = max(int(ov_reg or 0), int(ov_phys or 0)) if overflow else 0
    route, _shard, reason = _overflow_route(cap - bu, overflow, cap - ou)
    if bu < cap:
        flag = "BASE_HAS_ROOM"
    elif overflow and ou < cap:
        flag = "OVERFLOW_SHARD_EXISTS_DO_NOT_CREATE"
    else:
        flag = "ALL_SHARDS_FULL_ASK_USER_BEFORE_CREATE"
    gap = []
    if base_phys is not None and int(base_phys) > int(base_reg or 0):
        gap.append({"shard": "base", "registry": int(base_reg or 0), "physical": int(base_phys), "gap": int(base_phys) - int(base_reg or 0)})
    if overflow and ov_phys is not None and int(ov_phys) > int(ov_reg or 0):
        gap.append({"shard": "overflow", "registry": int(ov_reg or 0), "physical": int(ov_phys), "gap": int(ov_phys) - int(ov_reg or 0)})
    return {"base_used": bu, "overflow_used": ou, "route": route, "flag": flag, "reason": reason, "registry_live_gap": gap}


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
    per = _slot_count_all_shards(entries)
    base_reg, ov_reg = per.get(base_nb, 0), (per.get(overflow, 0) if overflow else 0)
    # LIVE physical cross-check (nlm-get) — registry có thể TỤT SAU vật lý (nguồn add thẳng chưa ghi registry).
    # MAX(registry, physical) làm slot hiệu lực → KHÔNG báo "còn chỗ" giả khi vật lý đã vượt cap (vd base 279 reg / 315 live).
    base_phys = ov_phys = None
    if not getattr(a, "no_live", False):
        try:
            nc = _imp("nlm_cli")
            base_phys = int(nc.notebook_get(base_nb).get("source_count") or 0)
            if overflow:
                ov_phys = int(nc.notebook_get(overflow).get("source_count") or 0)
        except Exception:
            base_phys = ov_phys = None
    st = _overflow_status(base_reg, base_phys, overflow, ov_reg, ov_phys)
    out = {"ok": True, "gate": "overflow-resolve", "base_notebook": base_nb,
           "base_used": st["base_used"], "base_registry": base_reg, "base_physical": base_phys,
           "overflow_shard": overflow or None, "overflow_discovered_from_registry": discovered,
           "overflow_used": st["overflow_used"], "overflow_registry": ov_reg, "overflow_physical": ov_phys,
           "cap": NLM_SLOT_CAP, "route": st["route"], "decision_flag": st["flag"], "reason": st["reason"],
           "used_basis": "max(registry, physical-nlm-get)", "registry_live_gap": st["registry_live_gap"],
           "note": "ADVISORY — KHÔNG tạo notebook. Chỉ `notebook create` khi MỌI shard đầy LIVE + người dùng duyệt."}
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


def cmd_nlm_content(a) -> int:
    """NLM read qua CLI (fast-lane Claude Code/Cowork): toàn văn raw 1 source. Thay MCP source_get_content."""
    try:
        nc = _imp("nlm_cli")
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False), file=sys.stderr); return 2
    r = nc.source_content(a.source_id)
    if not r.get("ok"):
        print(json.dumps(r, ensure_ascii=False, indent=2), file=sys.stderr); return 2
    data = r.get("data") or {}
    content = (data.get("content") if isinstance(data, dict) else None) or r.get("text", "") or ""
    content = _strip_font_runs(content)   # lọc dòng rác tên font rò từ DOCX/GDoc nguồn
    if getattr(a, "out", None):
        Path(a.out).write_text(content, encoding="utf-8")
        print(f"[tl] nlm-content → {a.out} ({len(content)} ký tự, via nlm-cli)")
    elif getattr(a, "dieu", None):
        print(_slice_dieu(content, a.dieu))
    else:
        print(content[: getattr(a, "max", 4000) or 4000])
    return 0


def cmd_nlm_query(a) -> int:
    """RAG query qua CLI nlm (fast-lane). Thay MCP notebook_query. VẪN phải verify nguyên văn với cache/raw."""
    # Group B: nạp TL_NOTEBOOK_ID từ PROFILE ĐANG DÙNG (trước đây thiếu → --profile NQ36 nlm-query nhắm VBQPPL base).
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        nc = _imp("nlm_cli")
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False), file=sys.stderr); return 2
    nb, _nberr = _resolve_nlm_notebook(a.notebook_id)
    if _nberr:
        print(json.dumps({"ok": False, "error": _nberr}, ensure_ascii=False), file=sys.stderr); return 2
    r = nc.notebook_query(nb, a.query, source_ids=(a.source_id or None))
    if not r.get("ok"):
        print(json.dumps(r, ensure_ascii=False, indent=2), file=sys.stderr); return 2
    print(json.dumps(r.get("data"), ensure_ascii=False, indent=2) if r.get("data") is not None else r.get("text", ""))
    print("[tl] LƯU Ý: RAG chỉ ĐỊNH VỊ; verify nguyên văn bằng cache/raw (KHÔNG nhận RAG làm nguyên văn).", file=sys.stderr)
    return 0


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
    r = nc.source_add(nb, drive_id=getattr(a, "drive_id", None), url=getattr(a, "url", None),
                      file=getattr(a, "file", None), doc_type=getattr(a, "type", None) or "doc",
                      title=getattr(a, "title", None), wait=not getattr(a, "no_wait", False))
    print(json.dumps(r, ensure_ascii=False, indent=2))
    if not r.get("ok"):
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
    if getattr(a, "drive_id", None) and r.get("source_id"):
        try:
            _row_exists = any(str(e.get("drive_id") or e.get("gdoc_id") or "") == str(a.drive_id)
                              for e in _manifest_entries(refresh=True))
        except Exception:
            _row_exists = False
        if _row_exists:
            try:
                load_creds(getattr(a, "config", None), getattr(a, "profile", None))
                _g = _gas()
                _rid = _apply_journal_start("nlm-add-link", {"drive_id": a.drive_id, "source_id": r.get("source_id")})
                _v = _journaled_reg_write(_rid, _g, [{"drive_id": a.drive_id, "nlm_source_id": r.get("source_id"),
                                                      "nlm_notebook_id": nb, "nlm_status": "pushed"}],
                                          "nlm_source_id,nlm_notebook_id,nlm_status",
                                          before_by_key={a.drive_id: {"nlm_source_id": "", "nlm_notebook_id": "", "nlm_status": ""}})
                _journal_append(_rid, {"t": "run_end", "ok": bool(_v.get("verified")), "counts": {"OK": 1}})
                print(json.dumps({"reg_link": {"ok": bool(_v.get("verified")), "journal": _rid}}, ensure_ascii=False), file=sys.stderr)
            except Exception as _e:  # noqa: BLE001
                print(f"[tl] nlm-add: add OK nhưng reg_link lỗi ({type(_e).__name__}: {_e}) → `tl nlm-reconcile --apply` để bắc cầu.", file=sys.stderr)
        else:
            print("[tl] nlm-add: add OK nhưng registry CHƯA có dòng cho drive_id này → `tl register --drive-id …` "
                  "hoặc `tl nlm-reconcile --apply` để bắc cầu (không tự tạo row xương).", file=sys.stderr)
    return 0


def cmd_nlm_cross(a) -> int:
    """Cross-shard query qua CLI `nlm cross query` (thay MCP cross_notebook_query). Verify nguyên văn sau."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))  # nạp TL_*NOTEBOOK_ID từ config (không cần webapp)
    try:
        nc = _imp("nlm_cli")
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False), file=sys.stderr); return 2
    nbs = [x.strip() for x in (getattr(a, "notebooks", None) or "").split(",") if x.strip()]
    # mặc định: các shard VBQPPL trong config (base + overflow) nếu không truyền --notebooks
    if not nbs and not getattr(a, "all", False):
        # Group B: shard mặc định theo PROFILE ĐANG DÙNG (TL_NOTEBOOK_ID) + overflow; default profile → VBQPPL base.
        nbs = [x for x in [(os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK), os.environ.get("TL_OVERFLOW_NOTEBOOK_ID")] if x]
        # A (v1.30.0): profile CỘNG VBQPPL — nối thêm notebook NỀN (base+overflow+shards từ config), profile đứng TRƯỚC.
        if _base_also_enabled(a):
            _, _cfg = _read_config_record(getattr(a, "config", None))
            for _nb in _vbqppl_notebooks(_cfg):
                if _nb not in nbs:
                    nbs.append(_nb)
    r = nc.cross_query(a.query, notebooks=nbs or None, all_notebooks=getattr(a, "all", False))
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if r.get("ok") else 2


def _classify_nlm_sources(sources: list, entries: list) -> dict:
    """KH1 1.23.2 (PURE, test offline): phân loại nguồn NLM LIVE (id,title) đối chiếu registry theo nlm_source_id →
    REGISTERED_ACTIVE (lành) / STATUS_MISMATCH_LIVE (dòng registry status=removed* NHƯNG nguồn còn SỐNG trên NLM → GẮN
    NHÃN SAI, cần vá metadata) / UNREGISTERED (trên NLM nhưng KHÔNG có dòng registry). Tự-động-hoá việc soi tay. KHÔNG mạng."""
    by_src = {}
    for e in entries or []:
        sid = e.get("nlm_source_id") or e.get("source_id")
        if sid:
            by_src[sid] = e
    _active = {"pushed", "synced", "added", "stale", "true", "1", "yes"}
    registered_active, mismatch_live, unregistered = 0, [], []
    for s in sources or []:
        sid = s.get("id") or s.get("source_id") or ""
        title = s.get("title") or s.get("name") or ""
        e = by_src.get(sid)
        if e is None:
            unregistered.append({"source_id": sid, "title": title})
            continue
        status = str(e.get("nlm_status") or "").strip().lower()
        if status.startswith("removed") or status in ("other_notebook", "deleted", "gone"):
            mismatch_live.append({"source_id": sid, "title": title, "drive_id": _entry_drive_id(e),
                                  "registry_sohieu": _entry_sohieu(e), "registry_status": status, "name": _entry_name(e)})
        else:
            registered_active += 1
    return {"live_count": len(sources or []), "registered_active": registered_active,
            "status_mismatch_live": mismatch_live, "unregistered": unregistered,
            "mismatch_count": len(mismatch_live), "unregistered_count": len(unregistered)}


def cmd_nlm_orphans(a) -> int:
    """KH1 1.23.2: PHÂN LOẠI nguồn NLM LIVE đối chiếu registry → tự bắt 'ghost gắn nhãn SAI' (STATUS_MISMATCH_LIVE:
    registry removed* nhưng nguồn còn SỐNG) + UNREGISTERED (trên NLM, không dòng registry). Thay việc soi tay nhiều vòng.
    REPORT-ONLY. --fix-mismatch: in bản vá metadata DRY (corpus=true,nlm_status=pushed) cho nhóm mislabel (an toàn — KHÔNG
    đụng NLM, KHÔNG xóa). --deep: đọc nội dung NLM từng mismatch → trích SỐ HIỆU header thật (vá cả sohieu cụt)."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        nc = _imp("nlm_cli")
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False), file=sys.stderr); return 2
    nb, nberr = _resolve_nlm_notebook(getattr(a, "notebook_id", None))
    if nberr:
        print(json.dumps({"ok": False, "error": nberr}, ensure_ascii=False), file=sys.stderr); return 2
    r = nc.source_list(nb)
    if not r.get("ok"):
        print(json.dumps({"ok": False, "error": r.get("error"), "fallback": r.get("fallback")}, ensure_ascii=False), file=sys.stderr); return 2
    sources = r.get("sources", [])
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception:
        entries = []
    cls = _classify_nlm_sources(sources, entries)
    if getattr(a, "deep", False):           # đọc nội dung NLM từng mismatch → số hiệu header thật (vá sohieu cụt)
        for m in cls["status_mismatch_live"]:
            try:
                rc = nc.source_content(m["source_id"])
                txt = (rc.get("text") or ((rc.get("data") or {}) if isinstance(rc.get("data"), dict) else {}).get("content") or "")[:2500]
                shs = _SOHIEU_RE.findall(txt)
                if shs:
                    m["header_sohieu"] = shs[0]
            except Exception:
                pass
    patch = []
    if getattr(a, "fix_mismatch", False):
        for m in cls["status_mismatch_live"]:
            if m.get("drive_id"):
                it = {"drive_id": m["drive_id"], "nlm_source_id": m["source_id"], "corpus": "true", "nlm_status": "pushed"}
                if m.get("header_sohieu"):
                    it["sohieu"] = m["header_sohieu"]      # --deep: vá cả số hiệu từ header
                patch.append(it)
    out = {"ok": True, "gate": "nlm-orphans", "notebook_id": nb, **cls,
           "physical_vs_registry_active_gap": cls["live_count"] - cls["registered_active"],
           "proposed_metadata_fix": patch,
           "note": "REPORT-ONLY. STATUS_MISMATCH_LIVE → vá metadata (corpus/status[/sohieu nếu --deep]) qua "
                   "`tl register --bulk <file> --cols corpus,nlm_status[,sohieu]`. UNREGISTERED → điều tra đăng ký/xóa "
                   "(đọc `tl nlm-content <id>`). KHÔNG tự xóa nguồn NLM (mọi source_delete cần người duyệt)."}
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"== nlm-orphans {nb[:14]} · live={cls['live_count']} · active={cls['registered_active']} · "
              f"MISMATCH_LIVE={cls['mismatch_count']} · UNREGISTERED={cls['unregistered_count']} ==")
        for m in cls["status_mismatch_live"][:30]:
            sh = m.get("header_sohieu") or m.get("registry_sohieu") or "(?)"
            print(f"  ⚠ MISLABEL  {sh:18s} {(m.get('title') or m.get('name') or '')[:40]:40s} status={m['registry_status']} [{(m.get('drive_id') or '')[:12]}]")
        for u in cls["unregistered"][:30]:
            print(f"  ? UNREG     {(u.get('title') or '(Drive Document)'):46s} [{u['source_id'][:12]}]")
        if patch:
            print(f"  → bản vá metadata DRY: {len(patch)} dòng (corpus=true,nlm_status=pushed{',sohieu' if any('sohieu' in p for p in patch) else ''}). Ghi: tl register --bulk <file> --cols …")
        print("  (REPORT-ONLY — KHÔNG xóa. UNREGISTERED: đọc nlm-content để định danh.)")
    return 0


def cmd_nlm_get(a) -> int:
    """Chi tiết + SỐ NGUỒN VẬT LÝ notebook qua CLI `nlm notebook get -j` (thay MCP notebook_get) — dùng cho slot/preflight."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        nc = _imp("nlm_cli")
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False), file=sys.stderr); return 2
    nb, _nberr = _resolve_nlm_notebook(a.notebook_id)
    if _nberr:
        print(json.dumps({"ok": False, "error": _nberr}, ensure_ascii=False), file=sys.stderr); return 2
    r = nc.notebook_get(nb)
    payload = {k: r.get(k) for k in ("ok", "source_count", "title", "via", "error", "fallback")}
    payload["notebook"] = nb
    _emit_json_payload(payload, getattr(a, "out", None))
    return 0 if r.get("ok") else 2


def _nlm_query_plan(question: str, source_ids: list[str], *, justification: str = "") -> dict:
    count = len(source_ids)
    errors = []
    warnings = []
    if not question.strip():
        warnings.append("QUESTION_EMPTY_OR_MISSING")
    if count == 0:
        errors.append("NO_SOURCE_IDS_SELECTED")
    if count > 5:
        errors.append("SOURCE_HARD_CAP_EXCEEDED")
    elif count > 3 and not justification.strip():
        errors.append("JUSTIFICATION_REQUIRED_FOR_4_OR_5_SOURCES")
    elif count > 3:
        warnings.append("SOURCE_COUNT_ABOVE_DEFAULT_1_TO_3")
    batches = []
    if count > 3:
        for i in range(0, count, 3):
            batches.append({"index": len(batches) + 1, "source_ids": source_ids[i:i+3]})
    else:
        batches.append({"index": 1, "source_ids": source_ids})
    return {
        "ok": not errors,
        "schema": "nlm_query_plan.v1",
        "question": question,
        "source_ids": source_ids,
        "source_count": count,
        "default_source_window": "1-3",
        "hard_cap": 5,
        "justification": justification or None,
        "errors": errors,
        "warnings": warnings,
        "recommended_commands": [
            "nlm-query <question> --source-id <id> --json",
            "nlm-cross <question> --notebooks <nb1,nb2> --json",
            "extract <query> --json",
        ],
        "batches": batches,
        "verify_after_nlm": [
            "Không coi RAG là trích nguyên văn cuối cùng.",
            "Với VBQPPL, kiểm lại bằng tl extract/source-verify hoặc nguồn canonical.",
            "Nếu cần hơn 3 nguồn, chia câu hỏi theo batches thay vì hỏi một lượt rộng.",
        ],
    }


def cmd_nlm_query_plan(a) -> int:
    source_ids = _split_source_ids(getattr(a, "source_id", None), getattr(a, "source_ids", "") or "")
    out = _nlm_query_plan(getattr(a, "question", "") or "", source_ids, justification=getattr(a, "justification", "") or "")
    if getattr(a, "json", False):
        print(_json_dumps(out))
    else:
        print(f"nlm-query-plan ok={out.get('ok')} sources={out.get('source_count')} hard_cap={out.get('hard_cap')}")
        for e in out.get("errors", []):
            print(f"ERROR: {e}")
        for w in out.get("warnings", []):
            print(f"WARN: {w}")
        for b in out.get("batches", []):
            print(f"batch {b['index']}: {', '.join(b.get('source_ids', []))}")
    return 0 if out.get("ok") else 2
