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


def _nlm_ref_slot_count(entries: list, notebook_id: str, base_notebook_id: str | None = None) -> int:
    """v1.34.40 B.1 (PURE, test offline): đếm dòng row_kind=ref ĐANG chiếm slot vật lý trên notebook —
    ref bị _nlm_slot_count skip by-design (ước lượng corpus) nhưng đã nlm-add nên vẫn chiếm slot thật.
    Cùng luật active/removed/blank-về-base với _nlm_slot_count để 2 số cộng được với nhau."""
    active = {"pushed", "synced", "added", "stale", "true", "1", "yes"}
    base_notebook_id = (base_notebook_id or NLM_BASE_NOTEBOOK).strip()
    is_base = notebook_id == base_notebook_id
    n = 0
    for e in entries or []:
        if _entry_row_kind(e) != "ref":
            continue
        status = str(e.get("nlm_status") or e.get("nlm") or "").strip().lower()
        src = e.get("nlm_source_id") or e.get("source_id")
        if status.startswith("removed") or status in ("other_notebook", "deleted", "gone"):
            continue
        if not src and status not in active:
            continue
        nb = str(e.get("nlm_notebook_id") or e.get("notebook_id") or "").strip()
        if nb == notebook_id or (not nb and is_base):
            n += 1
    return n


def _slot_count_all_shards(entries: list, base_nb: str | None = None) -> dict:
    """KH1 Pha 1.3 (II.5, PURE): đếm slot HIỆU LỰC theo TỪNG shard (nlm_notebook_id) — base + mọi overflow. Bỏ
    removed*/ref. Trả {notebook_id: count}. Dùng cảnh báo shard sắp đầy (>270/300) để chuẩn bị shard kế.
    v1.34.47 (Mod5 fix): khi có base_nb, dòng blank-nlm_notebook_id được quy về BASE (khớp _nlm_slot_count
    fold `matching + unknown_notebook if is_base`) — trước đây bỏ hẳn blank-nb ⇒ base UNDER-count so với
    slot-audit đơn-notebook ⇒ cảnh báo base gần-đầy kích trễ/không kích."""
    from collections import Counter as _C
    _active = {"pushed", "synced", "added", "stale", "true", "1", "yes"}
    _base = (base_nb or "").strip()
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
        elif _base:
            c[_base] += 1
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
        _base_sa = os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK
        per = _slot_count_all_shards(entries, _base_sa)
        # v1.34.49 (F-03/F-07): phủ shard DECLARED chưa có dòng registry (count=0 — VBQPPL-3 mới duyệt vẫn hiện)
        # + capacity PER-SHARD theo topology (shards[].capacity > TL_NLM_SOURCE_CAP > 300); lộ topology findings.
        _topo_sa = _resolve_shard_topology(entries, _base_sa)
        _caps_sa = {str(s.get("id") or ""): int(s.get("capacity") or NLM_SLOT_CAP)
                    for s in (_topo_sa.get("shards") or [])}
        for _sid_sa in _caps_sa:
            if _sid_sa:
                per.setdefault(_sid_sa, 0)
        _cap_of = lambda nb: _caps_sa.get(nb, NLM_SLOT_CAP)   # noqa: E731
        rows = sorted(per.items(), key=lambda kv: (-kv[1], kv[0]))
        warn = [{"notebook_id": nb, "count": n, "cap": _cap_of(nb)} for nb, n in rows
                if n >= min(near, _cap_of(nb))]
        res = {"ok": True, "gate": "slot-audit", "cap": NLM_SLOT_CAP, "near_full_threshold": near,
               "topology_ok": _topo_sa.get("ok"),
               "shards": [{"notebook_id": nb, "count": n, "cap": _cap_of(nb),
                           "near_full": n >= min(near, _cap_of(nb)), "full": n >= _cap_of(nb)} for nb, n in rows],
               "near_full_shards": warn}
        if _topo_sa.get("findings"):
            res["topology_findings"] = _topo_sa.get("findings")
        if getattr(a, "json", False):
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(f"== slot-audit --all-shards · {len(rows)} shard · cap default={NLM_SLOT_CAP} ngưỡng near-full={near} ==")
            for nb, n in rows:
                _c = _cap_of(nb)
                mk = "✗ FULL" if n >= _c else ("⚠ NEAR" if n >= min(near, _c) else "·")
                print(f"  {mk:7s} {nb[:40]:40s} {n}/{_c}")
            if warn:
                print(f"  ⚠ {len(warn)} shard chạm ngưỡng → chuẩn bị shard kế (đừng để ingest-missing chạm partial).")
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
    # v1.34.40 B.1 (log Chỉ thị — slot-audit mâu thuẫn nlm-reconcile + XÚI backfill dựa gap sai): slots_effective
    # SKIP row_kind=ref by-design (ước lượng slot corpus) nhưng ref ĐÃ nlm-add nên CHIẾM slot vật lý thật →
    # gap cũ (phys − corpus_rows) luôn dương giả khi profile có ref. Nay tách 3 số ĐỒNG ĐỊNH NGHĨA với
    # nlm-reconcile: nlm_claim_rows = corpus_estimate + ref_rows; gap tính trên claim; gợi ý backfill
    # (lệnh GHI) CHỈ in khi gap CÒN LẠI sau khi trừ ref ≠ 0.
    _ref_rows = _nlm_ref_slot_count(entries, notebook_id, getattr(a, "base_notebook_id", None))
    if phys is not None:
        reg = out.get("slots_effective", 0)
        out["physical_source_count"] = phys
        out["registry_estimate"] = reg
        out["ref_rows"] = _ref_rows
        out["nlm_claim_rows"] = reg + _ref_rows
        out["gap_vs_corpus_estimate"] = phys - reg
        out["gap"] = phys - out["nlm_claim_rows"]
        out["ground_truth"] = "physical (tl nlm-get / nlm notebook get)"
        if out["gap"] != 0:
            out["warning"] = (f"Lệch {phys} vật lý vs {out['nlm_claim_rows']} registry-claim (corpus {reg} + ref "
                              f"{_ref_rows}) ({out['gap']:+d}) — backfill nlm_notebook_id (`tl backfill-notebook`) "
                              f"hoặc nguồn add thẳng chưa ghi registry; đối chiếu `tl nlm-reconcile` trước khi ghi.")
        elif out["gap_vs_corpus_estimate"] != 0:
            out["note_ref"] = (f"Chênh {out['gap_vs_corpus_estimate']:+d} vs corpus-estimate giải thích TRỌN bằng "
                               f"{_ref_rows} dòng row_kind=ref (hợp lệ theo thiết kế — canonical VBQPPL add vào "
                               f"notebook để RAG). KHÔNG cần backfill.")
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
    if getattr(a, "cached", False):
        # v1.34.58 (C-#8 — Q10): opt-in đọc cache TTL 10' (chung helper với nlm-audit-physical);
        # mặc định GIỮ list tươi như cũ — cached chỉ dùng khi đối soát lặp trong 10'.
        r = _nlm_source_list_cached(nc, nb)
    else:
        r = nc.source_list(nb, skip_freshness=not getattr(a, "no_skip_freshness", False))
    if not r.get("ok"):
        # v1.34.60 (E3 — ADR-5/6): NLM hard-dead → phục vụ cache C-#8 BẤT KỂ TTL kèm cờ STALE_CACHE rc=0
        # (advisory hiển thị — KHÔNG phải bằng chứng vật lý; audit/migrate physical-first không đi đường này).
        _v60l = _nlm_or_corpus("nlm-list", a, err=r)
        _st60 = _nlm_list_stale_read(nb) if _v60l["route"] == "stale_cache" else None
        if _st60:
            _st60.update({"nlm_status": "offline", "fallback": "stale_cache", "flag": "STALE_CACHE"})
            print(f"[tl] ⚠ STALE_CACHE: listing từ cache cũ {_st60.get('age_s')}s (NLM offline) — CHỈ tham khảo "
                  f"hiển thị, KHÔNG dùng làm bằng chứng vật lý; chạy lại khi NLM sống để list tươi.",
                  file=sys.stderr)
            r = _st60
        else:
            print(json.dumps(r, ensure_ascii=False, indent=2), file=sys.stderr)
            print("[tl] nlm CLI không dùng được → fallback MCP `notebook_get` hoặc chạy `nlm login`.", file=sys.stderr)
            return 2
    if getattr(a, "json", False) or getattr(a, "out", None):
        _emit_json_payload(r, getattr(a, "out", None))   # N5 v1.33.41: --out atomic (đối soát đủ, né trần 30s)
    else:
        if r.get("stale"):
            print(f"notebook={nb} · {r['count']} nguồn STALE_CACHE tuổi {r.get('age_s')}s (NLM offline — KHÔNG phải live)")
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
            "unregistered": sorted(still_unreg),
            "registry_on_nlm_rows": n_rows}


# v1.34.50 (BUG1 hoàn tất — smoke v1.34.49 bắt): DRY reconcile trả ok:true bất kể finding → all_ok chỉ tính
# rc+ok KHÔNG đủ để khẳng định "sạch". Khoá "clean" = all_ok VÀ KHÔNG shard nào có finding thật.
# (Bẫy I11/bind: giữ tuple keys INLINE trong hàm — hằng module KHÔNG vào globals tl rebase → NameError.)
def _reconcile_sweep_problems(per_notebook: list) -> list[str]:
    """PURE (test offline): liệt kê shard có finding thật (desync/unregistered/link/backfill) HOẶC rc≠0."""
    _keys = ("desync_real", "unregistered_on_nlm", "link_candidates", "backfill_nlm_notebook_id")
    probs = []
    for p in per_notebook or []:
        nb = str(p.get("notebook") or "?")
        _find = [f"{k}={p.get(k)}" for k in _keys if p.get(k)]
        if _find:
            probs.append(f"{nb}({', '.join(_find)})")
        elif p.get("rc") not in (0, None):
            _er = f", {p['error']}" if p.get("error") else ""
            probs.append(f"{nb}(rc={p.get('rc')}{_er})")
    return probs


def _reconcile_sweep_clean(all_ok: bool, per_notebook: list) -> bool:
    """PURE: 'sạch' THẬT = all_ok VÀ KHÔNG finding. Dùng cho khoá `clean` (đường máy) + note (đường người)."""
    return bool(all_ok) and not _reconcile_sweep_problems(per_notebook)


def _reconcile_sweep_note(all_ok: bool, per_notebook: list) -> str:
    """v1.34.42 (BUG1) → v1.34.50 (hoàn tất): note ĐIỀU KIỆN cho `nlm-reconcile --all-notebooks`. Trước v1.34.42 là
    CHUỖI CỨNG 'mọi notebook sạch' in kể cả ok=false; v1.34.42 vá nhánh ok=false NHƯNG vẫn tin `all_ok` — DRY luôn
    ok:true nên desync>0 (rc=0) VẪN bị gọi 'SẠCH' (smoke v1.34.49 bắt: overflow desync=1 báo sạch oan — đúng lớp
    'sai mà báo thành công'). Nay KHÔNG tin all_ok đơn thuần: tự soi finding từ per_notebook. PURE, test offline."""
    probs = _reconcile_sweep_problems(per_notebook)
    if all_ok and not probs:
        return "Lưới cuối lô: mọi notebook SẠCH (desync=0, unregistered=0) = lô settle+link đủ."
    body = "; ".join(probs) if probs else "(không rõ — xem per_notebook)"
    return ("CÓ VẤN ĐỀ — chưa đồng bộ: " + body + ". "
            "rc=2 thường do thiếu cache/scope → chạy `tl --profile <P> boot` trước. "
            "Finding (desync/unregistered/link) → per-notebook `tl nlm-reconcile <nb> --apply` "
            "(desync stale: thêm `--clear-stale`).")


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
                                                     "already_removed", "error") if k in _r_i}})
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
           "foreign_skipped": len(plan.get("foreign_skipped") or []),  # v1.34.53 (A2): match dòng notebook KHÁC → guard chặn ghi, chỉ báo
           "unregistered_on_nlm": len(plan["unregistered"]),
           "mode": "APPLY" if getattr(a, "apply", False) else "DRY",
           "backfill_sample": [f"{_entry_nlm(e)}|{_entry_sohieu(e) or _sohieu_key_entry(e)}|{_entry_name(e)[:40]}" for e in plan["backfill"][:10]],
           "link_candidates_sample": [f"{c['source_id'][:12]}…→{_entry_drive_id(c['entry'])[:12]}… (by {c['by']}) | {(_entry_sohieu(c['entry']) or _entry_name(c['entry'])[:32])}" for c in (plan.get("link_candidates") or [])[:10]],
           "desync_real_sample": [f"{_entry_sohieu(e)}|{_entry_name(e)[:40]}" for e in plan["desync_real"][:10]],
           "foreign_skipped_sample": [f"{c['source_id'][:12]}…↛{(c.get('registry_notebook') or '?')[:12]}… (by {c['by']}) | {str(c.get('title') or '')[:32]}" for c in (plan.get("foreign_skipped") or [])[:10]],
           "unregistered_sample": plan["unregistered"][:8]}
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


def _shard_capacity_default() -> int:
    """v1.34.49 (F-07/D6): capacity mặc định — env TL_NLM_SOURCE_CAP (toàn cục, cho edition 50/100/400/600)
    thắng hằng NLM_SLOT_CAP=300 (bảo thủ, đúng account hiện tại). Per-shard: shards[].capacity thắng cả hai."""
    try:
        v = int(str(os.environ.get("TL_NLM_SOURCE_CAP") or "").strip() or 0)
        if v > 0:
            return v
    except (TypeError, ValueError):
        pass
    return NLM_SLOT_CAP


def _foreign_profile_notebooks(cfg: dict | None, current_profile: str | None) -> set:
    """v1.34.51 (điều tra live 2026-07-15): tập notebook (notebookId + shards[] ids) của MỌI profile KHÁC
    profile hiện tại. Dùng để resolver KHÔNG nhận nhầm notebook profile-khác thành vbqppl overflow-shard —
    ca 92 dòng dual-registered (base ⊕ Khảo sát Luật Xuất bản, notebook 80742228, corpus=false) lọt base scan
    do manifest lỡ gắn row_kind='overflow' vài dòng → v1.34.49 flag oan 55 drift. PURE."""
    cur = str(current_profile or "")
    out: set = set()
    for name, p in (_profiles_from_config(cfg or {}) or {}).items():
        if str(name) == cur or not isinstance(p, dict):
            continue
        nb = str(p.get("notebookId") or "").strip()
        if nb:
            out.add(nb)
        for s in (p.get("shards") if isinstance(p.get("shards"), list) else []):
            sid = str((s.get("id") if isinstance(s, dict) else s) or "").strip()
            if sid:
                out.add(sid)
    return out


def _resolve_shard_topology(entries: list[dict], base_nb: str, cfg: dict | None = None,
                            profile: str | None = None) -> dict:
    """v1.34.49 (D5 — grill 2026-07-15): TOPOLOGY declared+observed HỢP NHẤT, resolver DUY NHẤT cho mọi đường.
    Declared = config profiles.<p>.shards[] (dict {id,role,capacity,enabled,priority} HOẶC list[str] legacy) —
    nơi khai ý định vận hành (capacity/priority/enabled). Observed = env TL_OVERFLOW_NOTEBOOK_ID + registry
    row_kind='overflow'. Trả {ok, shards:[{id,role,capacity,enabled,priority,source}...], findings, declared, error}.
    Bất biến: (a) alias legacy (notebookId/overflowNotebookId/env) LỆCH declared → ok=False
    TOPOLOGY_CONFIG_CONFLICT (đường GHI/ROUTE phải rc=2; đường ĐỌC dùng union qua `_resolve_overflow_shards`);
    (b) declared CÓ → notebook lạ trong registry KHÔNG vào route (enabled=False, role='observed'), lộ findings
    UNDECLARED_REGISTRY_SHARD (doctor); declared VẮNG → materialize từ alias+env+registry (KHÔNG bắt sửa config).
    Capacity: shards[].capacity > TL_NLM_SOURCE_CAP > NLM_SLOT_CAP (live count vẫn là ground truth khi route)."""
    base_nb = (base_nb or "").strip()
    if cfg is None:
        _, cfg = _read_config_record(None)
    prof_name = (profile or _active_profile() or DEFAULT_PROFILE)
    prof = (_profiles_from_config(cfg or {}) or {}).get(prof_name) or {}
    foreign_nbs = _foreign_profile_notebooks(cfg, prof_name)   # v1.34.51: notebook profile-khác → KHÔNG là vbqppl shard
    cap_def = _shard_capacity_default()
    raw_shards = prof.get("shards") if isinstance(prof.get("shards"), list) else []
    findings: list[dict] = []
    declared: list[dict] = []
    seen: set[str] = set()
    _prof_nb = str(prof.get("notebookId") or "").strip()
    for i, s in enumerate(raw_shards):
        if isinstance(s, str):
            # schema cũ: list[str] = DANH SÁCH notebook base→overflow (ngữ nghĩa _vbqppl_notebooks — config live
            # thật có ["<base>", "<overflow>"]) → phần tử trùng notebookId/base = PRIMARY, còn lại overflow.
            sid = s.strip()
            role = "primary" if sid and sid in (_prof_nb, base_nb) else "overflow"
            cap, en, pri = None, True, i + 1
        elif isinstance(s, dict):
            sid = str(s.get("id") or "").strip()
            role = str(s.get("role") or "overflow").strip().lower()
            cap = s.get("capacity")
            en = s.get("enabled") is not False
            pri = s.get("priority") if isinstance(s.get("priority"), int) else i + 1
        else:
            findings.append({"finding": "SHARD_ENTRY_INVALID", "index": i}); continue
        if not sid:
            findings.append({"finding": "SHARD_ID_EMPTY", "index": i}); continue
        if sid in seen:
            return {"ok": False, "error": f"TOPOLOGY_CONFIG_CONFLICT: shard id trùng '{sid}'",
                    "shards": [], "findings": findings, "declared": True}
        try:
            cap_i = int(cap) if cap is not None else None
            if cap_i is not None and cap_i <= 0:
                raise ValueError
        except (TypeError, ValueError):
            return {"ok": False, "error": f"TOPOLOGY_CONFIG_CONFLICT: capacity không hợp lệ ở shard '{sid}'",
                    "shards": [], "findings": findings, "declared": True}
        seen.add(sid)
        declared.append({"id": sid, "role": ("primary" if role == "primary" else "overflow"),
                         "capacity": (cap_i if cap_i else cap_def), "enabled": bool(en),
                         "priority": pri, "source": "declared"})
    env_ovf = (os.environ.get("TL_OVERFLOW_NOTEBOOK_ID") or "").strip()
    env_ok = bool(env_ovf and env_ovf != base_nb and env_ovf != "TL_OVERFLOW_NOTEBOOK_ID")
    alias_ovf = str(prof.get("overflowNotebookId") or "").strip()
    if declared:
        declared.sort(key=lambda s: (0 if s["role"] == "primary" else 1, s["priority"], s["id"]))
        prim = [s for s in declared if s["role"] == "primary"]
        # primary khai báo phải KHỚP base đang dùng (alias notebookId/TL_NOTEBOOK_ID) — lệch = config conflict.
        if prim and base_nb and prim[0]["id"] != base_nb:
            return {"ok": False, "error": f"TOPOLOGY_CONFIG_CONFLICT: primary khai báo '{prim[0]['id']}' ≠ notebook "
                                          f"đang dùng '{base_nb}'", "shards": declared, "findings": findings,
                    "declared": True}
        if not prim and base_nb and base_nb not in seen:    # declared chỉ khai overflow → prepend primary (không dup)
            declared.insert(0, {"id": base_nb, "role": "primary", "capacity": cap_def, "enabled": True,
                                "priority": 0, "source": "alias"})
        dec_ids = {s["id"] for s in declared}
        for src, val in (("overflowNotebookId", alias_ovf), ("TL_OVERFLOW_NOTEBOOK_ID", env_ovf if env_ok else "")):
            if val and val not in dec_ids:
                return {"ok": False, "error": f"TOPOLOGY_CONFIG_CONFLICT: alias {src}='{val}' không thuộc shards[] "
                                              f"khai báo", "shards": declared, "findings": findings, "declared": True}
        # registry-observed KHÔNG khai báo → enabled=False + finding (doctor lộ drift; route KHÔNG tự nhận).
        # v1.34.51: notebook của PROFILE KHÁC (dual-registered) → 1 finding FOREIGN_PROFILE_NOTEBOOK (advisory),
        # KHÔNG thành observed vbqppl shard (né flag oan 92 dòng); notebook lạ KHÔNG-của-profile-nào = shard vbqppl
        # thật chưa declared → giữ observed như cũ.
        _foreign_seen: set = set()
        for e in entries or []:
            if _entry_row_kind(e) != "overflow":
                continue
            nb = str(e.get("nlm_notebook_id") or e.get("notebook_id") or "").strip()
            if not nb or nb == base_nb or nb in dec_ids:
                continue
            if nb in foreign_nbs:
                if nb not in _foreign_seen:
                    _foreign_seen.add(nb)
                    findings.append({"finding": "FOREIGN_PROFILE_NOTEBOOK", "notebook_id": nb})
                continue
            dec_ids.add(nb)
            findings.append({"finding": "UNDECLARED_REGISTRY_SHARD", "notebook_id": nb})
            declared.append({"id": nb, "role": "observed", "capacity": cap_def, "enabled": False,
                             "priority": 10_000, "source": "registry"})
        return {"ok": True, "error": None, "shards": declared, "findings": findings, "declared": True,
                "foreign_notebooks": sorted(foreign_nbs)}
    # ── declared VẮNG → materialize observed (giữ nguyên hành vi v1.34.47, thêm capacity/priority) ──
    out: list[dict] = []
    if base_nb:
        out.append({"id": base_nb, "role": "primary", "capacity": cap_def, "enabled": True,
                    "priority": 0, "source": "alias"})
    if env_ok:
        out.append({"id": env_ovf, "role": "overflow", "capacity": cap_def, "enabled": True,
                    "priority": 1, "source": "env"})
    counts: dict[str, int] = {}
    _foreign_seen2: set = set()
    for e in entries or []:
        if _entry_row_kind(e) != "overflow":
            continue
        nb = str(e.get("nlm_notebook_id") or e.get("notebook_id") or "").strip()
        if not nb or nb == base_nb:
            continue
        if nb in foreign_nbs:   # v1.34.51: notebook profile-khác KHÔNG là vbqppl overflow (kể cả khi config chưa có shards[])
            if nb not in _foreign_seen2:
                _foreign_seen2.add(nb)
                findings.append({"finding": "FOREIGN_PROFILE_NOTEBOOK", "notebook_id": nb})
            continue
        counts[nb] = counts.get(nb, 0) + 1
    have = {s["id"] for s in out}
    for i, (nb, _n) in enumerate(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))):
        if nb not in have:
            have.add(nb)
            out.append({"id": nb, "role": "overflow", "capacity": cap_def, "enabled": True,
                        "priority": 2 + i, "source": "registry"})
    return {"ok": True, "error": None, "shards": out, "findings": findings, "declared": False,
            "foreign_notebooks": sorted(foreign_nbs)}


def _topology_hash(profile: str, shards: list[dict]) -> str:
    """v1.34.49 (F-09): hash TẤT ĐỊNH của topology — sha256(json canonical {profile, shards[{capacity,enabled,
    id,priority,role}]}). Khớp golden references/golden/topology_vectors.json (adopt bundle Codex c98321f0) để
    GAS 2.21.2l (đợt 50) đối chiếu chéo client↔server."""
    import hashlib as _hl
    norm = [{"id": str(s.get("id") or ""), "role": str(s.get("role") or ""),
             "capacity": int(s.get("capacity") or 0), "enabled": bool(s.get("enabled", True)),
             "priority": int(s.get("priority") or 0)} for s in (shards or [])]
    blob = json.dumps({"profile": str(profile or ""), "shards": norm},
                      ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return _hl.sha256(blob.encode("utf-8")).hexdigest()


def _topology_stamp(cfg: dict | None, entries: list[dict], profile: str | None = None) -> dict:
    """v1.34.49 (F-09): stamp dẫn xuất cho manifest/registry-map — {topology_hash, routing_epoch, registry_digest,
    shard_count}. registry_digest = sha256 các tuple định danh dòng (drive_id, nlm_source_id, nlm_notebook_id,
    row_kind) đã sort → chứng minh snapshot theo topology/registry NÀO (client-side; server-side = đợt 50)."""
    import hashlib as _hl
    prof = profile or _active_profile()
    base = (os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK or "").strip()
    topo = _resolve_shard_topology(entries or [], base, cfg=cfg, profile=prof)
    rows = sorted((str(e.get("drive_id") or e.get("gdoc_id") or ""), str(e.get("nlm_source_id") or ""),
                   str(e.get("nlm_notebook_id") or ""), str(e.get("row_kind") or ""))
                  for e in (entries or []))
    dig = _hl.sha256(json.dumps(rows, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()
    return {"topology_hash": _topology_hash(prof, topo.get("shards") or []),
            "topology_ok": topo.get("ok"), "shard_count": len(topo.get("shards") or []),
            "routing_epoch": int((cfg or {}).get("routingEpoch") or 0),
            "registry_digest": dig}


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


_ROW_KIND_PROTECTED = ("ref", "thuong")   # kind NGHIỆP VỤ — không suy từ topology, không bao giờ clobber


def _topology_row_kind_findings(entries: list[dict], topo: dict) -> list[dict]:
    """v1.34.49 (F-06 doctor, PURE): bất biến `notebook==primary ⇔ row_kind∈{own,''}` và `notebook∈overflow ⇔
    row_kind=='overflow'` cho dòng ĐÃ có nlm_notebook_id. Bỏ qua kind bảo hộ (ref/thuong) + dòng chưa lên NLM.
    Trả findings [{drive_id, notebook_id, row_kind, finding}] — REPORT-ONLY (sửa: nlm-reconcile --apply / reg_upsert)."""
    out: list[dict] = []
    _foreign = set((topo or {}).get("foreign_notebooks") or [])   # v1.34.51: dòng notebook profile-khác → KHÔNG flag
    for e in entries or []:
        nb = str(e.get("nlm_notebook_id") or e.get("notebook_id") or "").strip()
        if not nb or nb in _foreign:
            continue
        rk = str(e.get("row_kind") or "").strip().lower()
        if rk in _ROW_KIND_PROTECTED:
            continue
        kind = _shard_row_kind(nb, topo)
        did = str(e.get("drive_id") or e.get("gdoc_id") or "")
        if kind is None:
            out.append({"drive_id": did, "notebook_id": nb, "row_kind": rk,
                        "finding": "UNKNOWN_NOTEBOOK_NOT_IN_TOPOLOGY"})
        elif kind == "own" and rk == "overflow":
            out.append({"drive_id": did, "notebook_id": nb, "row_kind": rk,
                        "finding": "PRIMARY_ROW_MARKED_OVERFLOW"})
        elif kind == "overflow" and rk != "overflow":
            out.append({"drive_id": did, "notebook_id": nb, "row_kind": rk,
                        "finding": "OVERFLOW_ROW_NOT_MARKED_OVERFLOW"})
    return out


def _live_source_count(nc, notebook_id: str, heal_state: dict | None = None) -> tuple:
    """v1.34.49 (F-05/D4, dùng CHUNG): đọc source_count LIVE fail-closed — notebook_get {ok:False} KHÔNG BAO GIỜ
    thành 0 (mẫu đúng slot-audit M2 v1.33.35). Đường GHI/ROUTE: ok=False → self-heal load_creds ĐÚNG 1 LẦN/run
    (doctrine v1.34.43; heal_state={'healed':bool} chia sẻ cả run) → retry → vẫn fail → caller DỪNG rc=2, ZERO
    side-effect. Trả (count|None, ok, error)."""
    hs = heal_state if isinstance(heal_state, dict) else {"healed": True}   # không heal_state → không tự heal
    for _attempt in (0, 1):
        try:
            r = nc.notebook_get(notebook_id)
        except Exception as e:  # noqa: BLE001 — lỗi vận chuyển = read-fail, KHÔNG phải 0 nguồn
            r = {"ok": False, "error": f"{type(e).__name__}: {e}"}
        if r.get("ok"):
            return int(r.get("source_count") or 0), True, ""
        if hs.get("healed"):
            return None, False, str(r.get("error") or "notebook_get !ok") + \
                (" — 🔴 AUTH: `nlm login`" if r.get("auth_hint") else "")
        hs["healed"] = True
        try:
            load_creds(None, None)
        except (SystemExit, Exception):  # noqa: BLE001 — heal best-effort; vòng retry quyết định
            pass
    return None, False, "notebook_get !ok"


def _nlm_add_capacity_error(err) -> bool:
    """v1.34.49 (F-02 drift, PURE): lỗi source_add có phải SHARD ĐẦY (→ được reroute shard kế cùng run, KHÔNG
    upload lại) hay không. QUOTA account/lỗi khác → False (dừng/đếm FAIL như cũ — reroute không cứu được)."""
    s = str(err or "").lower()
    if not s or "quota" in s:
        return False
    return any(k in s for k in ("full", "limit", "capacity", "maximum number of sources", "max sources"))


def _resolve_overflow_shards(entries: list[dict], base_nb: str, cfg: dict | None = None) -> list[str]:
    """v1.34.47 (giữ nguyên hợp đồng list[str] cho 47 call-site ĐỌC/AUDIT/QUERY) — v1.34.49: wrapper UNION trên
    `_resolve_shard_topology` (D5): declared shards[] (kể cả disabled — sweep nhìn thấy để lộ lệch) + env +
    registry-observed. Đường ĐỌC dùng union AN TOÀN (không bỏ sót nguồn kể cả khi config conflict — conflict
    được resolver ghi findings, doctor/route mới fail-closed); thứ tự: declared theo priority → env → registry."""
    base_nb = (base_nb or "").strip()
    topo = _resolve_shard_topology(entries, base_nb, cfg=cfg)
    _foreign = set(topo.get("foreign_notebooks") or [])   # v1.34.51: KHÔNG sweep notebook profile-khác vào vbqppl overflow
    out: list[str] = []
    seen: set[str] = set(_foreign)   # loại foreign khỏi mọi nguồn (topo/env/alias/registry-fallback)
    for s in topo.get("shards") or []:
        sid = s.get("id") or ""
        if sid and sid != base_nb and sid not in seen:
            seen.add(sid); out.append(sid)
    # conflict (ok=False) có thể chặn materialize alias/env trong resolver → bù trực tiếp cho sweep-safety.
    env_ovf = (os.environ.get("TL_OVERFLOW_NOTEBOOK_ID") or "").strip()
    if env_ovf and env_ovf != base_nb and env_ovf != "TL_OVERFLOW_NOTEBOOK_ID" and env_ovf not in seen:
        seen.add(env_ovf); out.append(env_ovf)
    try:   # alias config (đường đọc nới hơn đường ghi): sweep cả overflowNotebookId dù lệch declared
        _cfg2 = cfg if cfg is not None else _read_config_record(None)[1]
        _prof = (_profiles_from_config(_cfg2 or {}) or {}).get(_active_profile() or DEFAULT_PROFILE) or {}
        _al = str(_prof.get("overflowNotebookId") or "").strip()
        if _al and _al != base_nb and "-" in _al and _al not in seen:
            seen.add(_al); out.append(_al)
    except Exception:  # noqa: BLE001
        pass
    for e in entries or []:
        if _entry_row_kind(e) != "overflow":
            continue
        nb = str(e.get("nlm_notebook_id") or e.get("notebook_id") or "").strip()
        if nb and nb != base_nb and nb not in seen:
            seen.add(nb); out.append(nb)
    return out


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
            # v1.34.49 (F-05): đọc CHECKED — auth-fail hết bị hiểu thành live=0 (advisory nhưng người đọc tin số này)
            _pc, _pok, _perr = _live_source_count(_imp("nlm_cli"), nb, None)
            if _pok:
                live_cnt = _pc
            else:
                r["live_read_failed"] = True
                r["live_note"] = _perr
        except Exception:
            r["live_read_failed"] = True
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


def cmd_nlm_content(a) -> int:
    """NLM read qua CLI (fast-lane Claude Code/Cowork): toàn văn raw 1 source. Thay MCP source_get_content."""
    try:
        nc = _imp("nlm_cli")
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False), file=sys.stderr); return 2
    r = nc.source_content(a.source_id)
    content = None
    if r.get("ok"):
        data = r.get("data") or {}
        content = (data.get("content") if isinstance(data, dict) else None) or r.get("text", "") or ""
    else:
        # v1.34.60 (E1 lossless-read — ADR-1/6): nguồn NLM chính là bản GDoc corpus → NLM hard-dead thì đọc
        # thẳng GDoc theo sid→registry (NỘI DUNG Y HỆT, không mất mát). Transient/--no-fallback → lỗi cũ rc=2;
        # sid không resolve được dòng registry → KHÔNG fallback mù, giữ lỗi cũ.
        _v60 = _nlm_or_corpus("nlm-content", a, err=r)
        if _v60["route"] == "corpus_read":
            _sid60 = str(a.source_id or "").strip()
            try:
                _row60 = next((e for e in _manifest_entries(refresh=False)
                               if str(e.get("nlm_source_id") or "").strip() == _sid60), None)
            except Exception:  # noqa: BLE001
                _row60 = None
            _fid60 = str((_row60 or {}).get("gdoc_id") or (_row60 or {}).get("drive_id") or "").strip()
            if _fid60:
                try:   # lazy-creds: nạp token best-effort cho đường GAS trong _doc_text_any
                    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
                except (SystemExit, Exception):  # noqa: BLE001
                    pass
                _txt60, _src60 = _doc_text_any(_fid60, entry=_row60)
                if _txt60:
                    print(json.dumps({"nlm_status": "offline", "fallback": "corpus_read",
                                      "source": f"corpus:{_src60}:{_fid60}", "source_id": _sid60},
                                     ensure_ascii=False), file=sys.stderr)
                    content = _txt60
            if content is None:
                print(f"[tl] nlm-content fallback: sid {_sid60} KHÔNG resolve được dòng registry/GDoc "
                      f"→ giữ lỗi cũ (không đọc mù).", file=sys.stderr)
        if content is None:
            print(json.dumps(r, ensure_ascii=False, indent=2), file=sys.stderr); return 2
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
    # v1.34.47 (Mod6): nlm-query CHỈ quét 1 notebook. Nếu scope đã sharded (base + shard overflow) và không
    # ghim source_id → nhắc dùng nlm-cross để phủ overflow (tránh lặng lẽ thiếu nguồn đã overflow).
    if not getattr(a, "notebook_id", None) and not (a.source_id or None):
        try:
            _q_shards = _resolve_overflow_shards(_manifest_entries(refresh=False), nb)
        except Exception:  # noqa: BLE001
            _q_shards = []
        if _q_shards:
            print(f"[tl] ⚠ corpus đã SHARDED (base {nb[:8]}… + {len(_q_shards)} shard overflow) — nlm-query chỉ quét 1 "
                  f"notebook, nguồn đã overflow KHÔNG hiện. Dùng `tl nlm-cross \"<câu hỏi>\"` để phủ base+overflow.",
                  file=sys.stderr)
    r = nc.notebook_query(nb, a.query, source_ids=(a.source_id or None))
    if not r.get("ok"):
        # v1.34.60 (E1 — ADR-1/2/6): NLM hard-dead → verbatim-return ≤5 văn bản corpus (manifest/webapp sống
        # độc lập cookie). Transient (probe xác nhận còn sống) / --no-fallback / TL_NLM_FALLBACK=0 → lỗi cũ rc=2.
        _v60 = _nlm_or_corpus("nlm-query", a, notebook_id=nb, err=r)
        if _v60["route"] == "corpus_read":
            return _nlm_query_corpus_fallback(a, a.query, cmd="nlm-query", why=_v60["why"])
        print(json.dumps(r, ensure_ascii=False, indent=2), file=sys.stderr); return 2
    print(json.dumps(r.get("data"), ensure_ascii=False, indent=2) if r.get("data") is not None else r.get("text", ""))
    print("[tl] LƯU Ý: RAG chỉ ĐỊNH VỊ; verify nguyên văn bằng cache/raw (KHÔNG nhận RAG làm nguyên văn).", file=sys.stderr)
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


# ── v1.34.54 (A1+C8+B1 — grill Q3/Q8 2026-07-15): tuổi cookie + preflight 2 tầng + batch-link ──
_NLM_COOKIE_LIFE_MIN = 60      # hồ sơ DBSC 2026-07-12: đời cookie ~1h, `nlm login` là đủ
_NLM_COOKIE_WARN_AGE_MIN = 45  # tuổi vượt ngưỡng → khuyên re-auth trước lô dài / chuyển nlm-links
NLM_BATCH_LINKS_THRESHOLD = 2  # grill Q3(a): >2 file → đường batch-link (hằng số, KHÔNG config env — D7)


def _nlm_auth_age_minutes():
    """v1.34.54 (A1/C8): tuổi cookie NLM local (PHÚT). Tín hiệu tươi THẬT = profiles/default/metadata.json
    .last_validated (mirror `_nlm_auth_age_days` tl_gws — root auth.json.extracted_at không được nlm CLI mới
    ghi lại); fallback auth.json.extracted_at (epoch). None = không đọc được (chưa login máy này)."""
    from datetime import datetime as _dt
    base = Path.home() / ".notebooklm-mcp-cli"
    try:
        meta = json.loads((base / "profiles" / "default" / "metadata.json").read_text(encoding="utf-8"))
        lv = meta.get("last_validated")
        if lv:
            return (_dt.now() - _dt.fromisoformat(lv)).total_seconds() / 60.0
    except Exception:  # noqa: BLE001
        pass
    try:
        ts = json.loads((base / "auth.json").read_text(encoding="utf-8")).get("extracted_at")
        if ts:
            import time as _t
            return (_t.time() - float(ts)) / 60.0
    except Exception:  # noqa: BLE001
        pass
    return None


def _nlm_preflight_report(notebook_id: str, *, probe: bool = True) -> dict:
    """v1.34.54 (A1+C8, doctrine M1): tầng 1 = probe LIVE `notebook_get` (login --check KHÔNG chứng minh cookie
    sống — M1 v1.33.35); tầng 2 = tuổi cookie + ước lượng còn lại (đời thường ~60'). warn[] chỉ CẢNH BÁO,
    caller tự quyết chặn/không. probe=False khi caller đã tự probe (không gọi NLM 2 lần)."""
    rep = {"alive": None, "why": "", "age_min": None, "est_remaining_min": None, "warn": []}
    age = _nlm_auth_age_minutes()
    if age is not None:
        rep["age_min"] = round(age, 1)
        rep["est_remaining_min"] = round(max(0.0, _NLM_COOKIE_LIFE_MIN - age), 1)
        if age > _NLM_COOKIE_WARN_AGE_MIN:
            rep["warn"].append(f"COOKIE_AGE_HIGH: cookie ~{age:.0f}' tuổi (đời thường ~{_NLM_COOKIE_LIFE_MIN}') "
                               f"— nên `nlm login` trước lô dài, hoặc chuyển đường `tl nlm-links` (batch dán tay).")
    if probe:
        try:
            nc = _imp("nlm_cli")
            # hasattr-guard CẢ 2 method: client fake trong harness/driver tối giản (chỉ source_add/source_list)
            # KHÔNG bị kết luận 'chết' oan — thiếu method probe thì alive giữ None (không probe được ≠ chết).
            if hasattr(nc, "nlm_available") and not nc.nlm_available():
                rep["alive"], rep["why"] = False, "nlm CLI không có trên PATH"
            elif hasattr(nc, "notebook_get"):
                r = nc.notebook_get(notebook_id)
                rep["alive"] = bool(r.get("ok"))
                if not rep["alive"]:
                    rep["why"] = str(r.get("error") or "")[:120]
        except Exception as e:  # noqa: BLE001
            rep["alive"], rep["why"] = False, f"{type(e).__name__}: {e}"
    return rep


# ── v1.34.60 (NLM-DEATH RESILIENCE R1 — kế hoạch E1–E3 grill 2026-07-16, ADR-1..7): lớp resolver
# _nlm_or_corpus + control surface. Bất biến giữ nguyên: physical-first (không ghi "verified" trên belief),
# nguyên văn #2 (corpus/cache đã xác minh — KHÔNG máy sinh RAG), corpus=true chỉ khi đã trên NLM. ──

def _nlm_fallback_enabled(a=None) -> bool:
    """(ADR-5) fallback MẶC ĐỊNH BẬT; tắt per-lệnh `--no-fallback` hoặc toàn cục TL_NLM_FALLBACK=0 (CI strict)."""
    if a is not None and getattr(a, "no_fallback", False):
        return False
    return str(os.environ.get("TL_NLM_FALLBACK", "") or "").strip().lower() not in {"0", "false", "off", "no"}


def _nlm_hard_dead(why: str) -> bool:
    """PURE (ADR-7): phân loại lỗi NLM. HARD-DEAD (auth/cookie chết, CLI vắng — trạng thái BỀN) mới được rẽ
    fallback; transient (mạng/timeout/rate-limit) KHÔNG — retry rồi mới kết luận, không âm thầm rẽ corpus."""
    low = (why or "").lower()
    if any(t in low for t in ("timeout", "timed out", "rate limit", "rate-limit", "429", "connection",
                              "network", "temporar", "unavailable", "503", "502", "500")):
        return False
    return any(t in low for t in ("auth", "401", "login", "unauthor", "credential", "cookie", "expired",
                                  "csrf", "invalid_grant", "403", "forbidden", "trên path", "not on path"))


def _nlm_verdict(notebook_id: str, *, refresh: bool = False) -> dict:
    """(ADR-7) probe LIVE đúng 1 LẦN/notebook/process (cache _NLM_PROBE_CACHE — hằng ở tl.py, bẫy I11), tái
    dùng _nlm_preflight_report. Hard-dead chốt ngay; lỗi transient retry 1 nhịp RỒI MỚI kết luận dead.
    alive=None (không probe được ≠ chết — client fake thiếu method) → coi như sống, KHÔNG rẽ fallback oan."""
    key = str(notebook_id or "").strip() or "_default"
    if not refresh and key in _NLM_PROBE_CACHE:
        return _NLM_PROBE_CACHE[key]
    rep = _nlm_preflight_report(notebook_id)
    alive, why = rep.get("alive"), str(rep.get("why") or "")
    if alive is False and not _nlm_hard_dead(why):
        rep2 = _nlm_preflight_report(notebook_id)
        alive, why = rep2.get("alive"), str(rep2.get("why") or why)
    v = {"alive": True if alive is None else bool(alive), "why": why, "age_min": rep.get("age_min")}
    _NLM_PROBE_CACHE[key] = v
    return v


def _nlm_fallback_banner(cmd: str, why: str, route: str) -> None:
    """(ADR-5) cảnh báo LỚN stderr MỖI LẦN rẽ fallback — thông báo, KHÔNG chặn."""
    print(f"[tl] ⚠⚠⚠ NLM OFFLINE ({(why or 'auth expired')[:100]}) — `{cmd}` KHÔNG dừng: rẽ fallback `{route}` "
          f"(corpus/webapp sống độc lập cookie NLM). Tắt: --no-fallback (per-lệnh) / TL_NLM_FALLBACK=0 (toàn cục). "
          f"Hồi phục: `nlm login` → `tl nlm-auth-status --wait` → `tl nlm-reconcile <nb> --apply`.",
          file=sys.stderr, flush=True)


def _nlm_or_corpus(cmd_name: str, a=None, *, notebook_id=None, err=None, probe: bool = False) -> dict:
    """Lớp resolver E (ADR-5/6/7): quyết định route khi thao tác NLM có nguy cơ chết.
    - err=<resp lỗi nlm_cli>: phân loại từ lỗi thật (auth_hint / fallback:mcp / marker hard) — hard → dead
      ngay (seed cache); transient → xác nhận bằng _nlm_verdict (probe cache 1 lần/run).
    - probe=True (đường GHI như nlm-add): probe chủ động TRƯỚC side-effect.
    Trả {"nlm_alive", "route", "mode", "why"}; route ∈ nlm | fail_closed | corpus_read | deferred |
    stale_cache | unverified | none — lệnh coi mọi route ∉ {corpus_read,deferred,stale_cache,unverified}
    là ĐƯỜNG CŨ (fail-closed giữ nguyên hành vi trước v1.34.60)."""
    from tl_core.command_registry import COMMAND_META
    mode = (COMMAND_META.get(cmd_name) or {}).get("nlm_fallback")
    out = {"nlm_alive": True, "route": "nlm", "mode": mode, "why": ""}
    if not mode:
        return out
    if not _nlm_fallback_enabled(a):
        out["route"] = "fail_closed"
        return out
    nb = str(notebook_id or os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK or "").strip()
    dead, why = False, ""
    if err is not None:
        why = str((err or {}).get("error") or (err or {}).get("why") or "")[:160]
        if (err or {}).get("auth_hint") or (err or {}).get("fallback") == "mcp" or _nlm_hard_dead(why):
            dead = True
            _NLM_PROBE_CACHE[nb or "_default"] = {"alive": False, "why": why, "age_min": None}
        else:
            v = _nlm_verdict(nb)
            dead, why = (not v["alive"]), (v["why"] or why)
    elif probe:
        v = _nlm_verdict(nb)
        dead, why = (not v["alive"]), v["why"]
    if not dead:
        return out
    out["nlm_alive"], out["why"] = False, why
    out["route"] = {"corpus_read": "corpus_read", "defer": "deferred", "stale_cache": "stale_cache",
                    "unverified": "unverified"}.get(mode, "none")
    _nlm_fallback_banner(cmd_name, why, out["route"])
    return out


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


def _corpus_question_resolve(question: str, entries: list, k: int = 5) -> dict:
    """PURE (ADR-1/2): resolve câu hỏi → ≤k văn bản corpus cho VERBATIM-RETURN. Tier EXACT-SOHIEU (số hiệu
    trong câu hỏi, khớp qua _sohieu_query_hits_entry như locate) → tier tên (token-overlap ≥2 sau strip-accent,
    tất định); >k hoặc 0 → HẠ AN TOÀN (docs rỗng + candidates — KHÔNG tổng hợp mù). Dòng removed* = tombstone
    bỏ qua; row_kind ref/thuong (không thuộc corpus luật) bỏ qua; thiếu drive/gdoc id bỏ qua."""
    q = str(question or "")
    m = re.search(r"[ĐđDd]iều\s+(\d+[a-zA-Z]?)", q)
    dieu = m.group(1) if m else None
    keys = []
    for s in (_SOHIEU_RE.findall(q) + re.findall(r"\b\d{1,4}/VBHN-[A-ZĐ][A-Z0-9Đ\-]*", q)):
        kk = norm_sohieu(s)
        if kk and kk not in keys:
            keys.append(kk)
    rows = []
    for e in entries or []:
        if not str(e.get("drive_id") or e.get("gdoc_id") or "").strip():
            continue
        if str(e.get("nlm_status") or "").strip().lower().startswith("removed"):
            continue
        if _entry_row_kind(e) in {"ref", "thuong"}:
            continue
        rows.append(e)

    def _rid(e):
        return str(e.get("drive_id") or e.get("gdoc_id") or "")

    docs, seen, conf = [], set(), "none"
    if keys:
        for kk in keys:
            for e in rows:
                sh = norm_sohieu(_entry_sohieu(e))
                if (kk == sh or _sohieu_query_hits_entry(kk, sh)
                        or _sohieu_query_hits_entry(kk, _sohieu_key_entry(e))):
                    if _rid(e) not in seen:
                        seen.add(_rid(e))
                        docs.append(e)
        if docs:
            conf = "exact"
    if not docs:
        qn = _strip_accents(q).lower()
        _stop = {"phap", "luat", "bo", "va", "cua", "ve", "tra", "dieu", "khoan", "diem", "muc", "cho",
                 "trong", "theo", "la", "gi", "nao", "the", "cac", "nhung", "mot", "so", "sanh", "hoi",
                 "voi", "den", "tu", "khi", "nay", "toan", "van", "noi", "dung"}
        qtok = [t for t in re.findall(r"[a-z0-9]{2,}", qn) if t not in _stop and not t.isdigit()]
        for e in rows:
            ntok = set(re.findall(r"[a-z0-9]{2,}", _strip_accents(_entry_name(e)).lower()))
            if sum(1 for t in qtok if t in ntok) >= 2 and _rid(e) not in seen:
                seen.add(_rid(e))
                docs.append(e)
        if docs:
            conf = "name"
    docs.sort(key=lambda e: (bool(_entry_corpus_true(e)), _entry_score(e)), reverse=True)
    if docs and len(docs) > k:
        return {"docs": [], "dieu": dieu, "confidence": "ambiguous", "candidates": docs[:max(2 * k, 10)]}
    return {"docs": docs, "dieu": dieu, "confidence": (conf if docs else "none"), "candidates": []}


def _nlm_query_corpus_fallback(a, question: str, *, cmd: str = "nlm-query", why: str = "") -> int:
    """E1 (ADR-1/6 — verbatim-return): NLM chết → CLI (KHÔNG phải LLM) trả NGUYÊN VĂN ≤5 văn bản corpus
    (+ Điều đã cắt nếu câu hỏi nêu) + ứng viên; AGENT gọi lệnh tự tổng hợp trong context — KHÔNG máy sinh
    RAG (bất biến #2). >5/mơ hồ → hạ an toàn: chỉ ứng viên + gợi ý tra tiếp. Mọi kết cục rc=0 (ADR-6)."""
    # nlm-query/cross là lệnh LAZY-CREDS (main không load) — fallback đọc corpus cần webapp/token cho đường
    # GAS exporttext: best-effort load_creds (live-smoke 2026-07-16 bắt 'Thiếu TL_WEBAPP/TL_TOKEN' giữa
    # fallback); máy không config → nuốt, đường gws-cred/cache vẫn tự chạy.
    try:
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    except (SystemExit, Exception):  # noqa: BLE001
        pass
    try:
        entries = _manifest_entries(refresh=False)
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"ok": False, "error": "FALLBACK_UNAVAILABLE_NO_MANIFEST", "detail": str(e)[:120],
                          "note": "NLM offline VÀ chưa có cache manifest — chạy `tl boot`/`tl manifest` "
                                  "(webapp độc lập cookie) rồi thử lại."}, ensure_ascii=False, indent=2),
              file=sys.stderr)
        return 2
    res = _corpus_question_resolve(question, entries, k=5)
    docs_out = []
    for e in res["docs"]:
        fid = str(e.get("gdoc_id") or "").strip() or _entry_drive_id(e)
        text, src = _doc_text_any(fid, entry=e)
        item = {"sohieu": _entry_sohieu(e), "name": _entry_name(e), "drive_id": _entry_drive_id(e),
                "source": src}
        if not text:
            item["text_error"] = "DOC_TEXT_UNAVAILABLE"
            item["text"] = ""
        elif res["dieu"]:
            item["dieu"] = res["dieu"]
            item["text"] = _slice_dieu(text, res["dieu"])
        else:
            _mx = int(getattr(a, "max", None) or 4000)
            full = bool(getattr(a, "out", None))
            item["text"] = text if full else text[:_mx]
            item["truncated"] = (not full) and len(text) > _mx
        docs_out.append(item)
    if docs_out:
        note = ("NLM offline — CLI trả NGUYÊN VĂN từ corpus (verbatim-return, ADR-1): agent tự tổng hợp; "
                "KHÔNG phải RAG. Toàn văn dài: --out <file> hoặc `tl doc-text <drive_id>`.")
    else:
        note = (f"NLM offline + {len(res['candidates'])} ứng viên (confidence={res['confidence']}) — "
                "KHÔNG tổng hợp mù. Tra tiếp: `tra Điều <X> của <sohieu>` hoặc "
                "`tl doc-text <drive_id> --dieu <n>`.")
    out = {"ok": True, "schema": "nlm_query_fallback.v1", "cmd": cmd, "nlm_status": "offline",
           "fallback": "corpus_read", "source": "corpus", "why": (why or "")[:120], "question": question,
           "dieu": res["dieu"], "confidence": res["confidence"], "resolved": len(res["docs"]),
           "docs": docs_out,
           "candidates": [{"sohieu": _entry_sohieu(e), "name": _entry_name(e),
                           "drive_id": _entry_drive_id(e)} for e in res["candidates"]],
           "note": note}
    if getattr(a, "out", None):
        _emit_json_payload(out, a.out)
    else:
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0


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
            _journal_append(_rid, {"t": "run_end", "ok": bool(_v.get("verified")), "counts": {"DEFERRED": 1}})
            _reg_deferred = bool(_v.get("verified"))
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


def cmd_nlm_auth_status(a) -> int:
    """C8 (v1.34.54): trạng thái phiên NLM — probe live + tuổi cookie; `--wait` poll (mặc định 20s/lần, timeout
    300s) tới khi SỐNG — dùng ngay sau khi login trình duyệt/`nlm login` để biết credential đã chảy vào chưa,
    khỏi đoán thời điểm thử lại. rc=0 sống; rc=2 chết/hết timeout."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    nb, _nberr = _resolve_nlm_notebook(getattr(a, "notebook_id", None))
    if _nberr:
        nb = NLM_BASE_NOTEBOOK   # auth-status chỉ cần 1 notebook BẤT KỲ đọc được để probe — base là đủ
    _interval = max(5, int(getattr(a, "interval", None) or 20))
    _deadline = None
    if getattr(a, "wait", False):
        import time as _t
        _deadline = _t.time() + max(_interval, int(getattr(a, "timeout", None) or 300))
    _n = 0
    while True:
        _n += 1
        rep = _nlm_preflight_report(nb)
        out = {"ok": bool(rep.get("alive")), "schema": "nlm_auth_status.v1", "notebook_probed": nb,
               "attempt": _n, **rep}
        if rep.get("alive") or _deadline is None:
            print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
            return 0 if rep.get("alive") else 2
        import time as _t
        if _t.time() + _interval > _deadline:
            out["timeout"] = True
            print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
            return 2
        print(f"[tl] nlm-auth-status: chưa sống (lần {_n}: {rep.get('why') or '?'}) — thử lại sau {_interval}s…",
              file=sys.stderr, flush=True)
        _t.sleep(_interval)


def _entry_links_url(e: dict) -> str:
    """B1: URL dán-được cho 1 dòng registry — Docs mặc định; Sheets theo mime."""
    did = _entry_drive_id(e)
    if "spreadsheet" in str(e.get("mime") or "").lower():
        return f"https://docs.google.com/spreadsheets/d/{did}"
    return f"https://docs.google.com/document/d/{did}"


def _nlm_links_rows(entries: list, *, profile_scope: bool) -> list:
    """PURE (v1.34.54 B1): dòng CẦN NẠP NLM = có drive_id + CHƯA có nlm_source_id + không removed*.
    Scope NỀN vbqppl loại row_kind ref/thuong (dòng tham khảo không thuộc notebook luật); profile giữ nguyên
    (chunk con row_kind=ref của profile VẪN lên NLM)."""
    out = []
    for e in entries:
        if not _entry_drive_id(e) or (_entry_nlm(e) or "").strip():
            continue
        if str(e.get("nlm_status") or "").strip().lower().startswith("removed"):
            continue
        if not profile_scope and _entry_row_kind(e) in {"ref", "thuong"}:
            continue
        out.append(e)
    return out


def cmd_nlm_links(a) -> int:
    """B1 (v1.34.54, grill Q2/Q3=a): in DANH SÁCH LINK Drive để NẠP BATCH TAY vào NotebookLM — né cookie ~1h
    khi lô dài. STDOUT = CHỈ LINK (mỗi dòng 1 — dán thẳng vào ô Websites/Links của UI; NLM nhận nhiều link cách
    nhau xuống dòng [docs Google], link Docs được nhận thành nguồn Drive [user thực chứng 2026-07-15]).
    Mọi chú thích (notebook URL, đếm, hướng dẫn, tuổi cookie) ở STDERR. OFFLINE đọc cache manifest (--refresh
    khi cần tươi). Sau khi dán xong: `tl nlm-reconcile <notebook> --apply` để link registry (exact-title/A2-guard)."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    if getattr(a, "refresh", False):
        try:
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        except (SystemExit, Exception):  # noqa: BLE001
            pass
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:  # noqa: BLE001
        print(f"[tl] nlm-links: cần `tl boot`/`manifest` trước ({e}).", file=sys.stderr)
        return 2
    nb = (getattr(a, "notebook", None) or "").strip()
    if not nb:
        nb, _nberr = _resolve_nlm_notebook(None)
        if _nberr:
            print(json.dumps({"ok": False, "error": _nberr}, ensure_ascii=False), file=sys.stderr)
            return 2
    rows = _nlm_links_rows(entries, profile_scope=_active_profile() != DEFAULT_PROFILE)
    _cat = (getattr(a, "cat", None) or "").strip()
    if _cat:
        rows = [e for e in rows if str(_entry_cat(e) or "").startswith(_cat) or str(_entry_cat(e) or "").split("_")[0] == _cat]
    _lim = getattr(a, "limit", None)
    _total = len(rows)
    if _lim:
        rows = rows[:int(_lim)]
    links = [_entry_links_url(e) for e in rows]
    nb_url = f"https://notebooklm.google.com/notebook/{nb}"
    rep = _nlm_preflight_report(nb, probe=False)   # chỉ tuổi cookie — lệnh này OFFLINE, không gọi NLM
    if getattr(a, "json", False) or getattr(a, "out", None):
        payload = {"ok": True, "schema": "nlm_links.v1", "notebook": nb, "notebook_url": nb_url,
                   "count": len(links), "total_pending": _total, "links": links,
                   "rows": [{"drive_id": _entry_drive_id(e), "name": _entry_name(e), "cat": _entry_cat(e)} for e in rows],
                   "cookie_age_min": rep.get("age_min"),
                   "next_steps": [f"Dán links vào Add source → Websites của {nb_url}",
                                   f"tl nlm-reconcile {nb} --apply   # link registry (exact-title, ownership-guard A2)",
                                   "tl register --drive-id <id> --corpus true  # từng dòng sau khi link (scope nền)"]}
        _emit_json_payload(payload, getattr(a, "out", None))
        return 0
    for ln in links:
        print(ln)
    print(f"[tl] nlm-links: {len(links)}/{_total} dòng chưa-trên-NLM (scope {_active_profile()}).", file=sys.stderr)
    print(f"[tl]   Notebook: {nb_url}", file=sys.stderr)
    print("[tl]   Dán TOÀN BỘ stdout vào Add source → Websites (nhiều link/lần, cách nhau xuống dòng).", file=sys.stderr)
    print(f"[tl]   Xong: tl nlm-reconcile {nb} --apply  (link exact-title; đã có ownership-guard).", file=sys.stderr)
    for w in rep.get("warn") or []:
        print(f"[tl]   ⚠ {w}", file=sys.stderr)
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
    # v1.34.60 (E3 push-defer — ADR-4): probe chủ động TRƯỚC mọi side-effect (gate/claim/add). NLM hard-dead
    # + fallback bật → defer: registry nlm_status=deferred + batch-link, KHÔNG add mù, rc=0. --no-fallback/
    # TL_NLM_FALLBACK=0 → đường cũ (gate dedup sẽ fail-closed LIVE_SOURCE_LIST_FAILED như trước).
    _v60a = _nlm_or_corpus("nlm-add", a, notebook_id=nb, probe=True)
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
            _cl56 = _gas().get("ingest_claim", keys=json.dumps([_claim56]), run_id=_run56,
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
                              "note": "Lần add trước/host khác có thể ĐÃ thành công server-side — `tl nlm-list "
                                      "<nb>` hoặc `tl nlm-reconcile` xác minh TRƯỚC khi retry; claim TTL 5'. "
                                      "Sau timeout NLM: chờ ≥60s cho settle rồi mới kiểm."},
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
        if getattr(a, "no_wait", False):
            print("[tl] nlm-add --no-wait: sid chưa settle — KHÔNG ghi registry; "
                  "lưới cuối lô: tl nlm-reconcile <nb> --apply", file=sys.stderr)
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
                        if _shard_row_kind(nb, _topo_na) == "overflow" and _cur_rk_na not in _ROW_KIND_PROTECTED:
                            _it_na["row_kind"] = "overflow"
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


def _nlm_source_remove_plan(entries: list, sids: list) -> dict:
    """v1.34.56 (A-#12) PURE: đối chiếu sid ↔ con trỏ registry (nlm_source_id). Dòng còn TRỎ sid mà vẫn gỡ
    nguồn = tự tạo con trỏ treo (không tự lành — bài học canary dbe706a0) → POINTER_STILL_ATTACHED."""
    rows = []
    for sid in sids:
        _s = str(sid)
        att = [{"drive_id": str(e.get("drive_id") or e.get("gdoc_id") or ""),
                "name": str(e.get("name") or ""),
                "nlm_notebook_id": str(e.get("nlm_notebook_id") or "")}
               for e in (entries or []) if str(e.get("nlm_source_id") or "") == _s]
        rows.append({"source_id": _s, "pointer_attached": bool(att), "pointers": att})
    return {"rows": rows,
            "attached": [r0["source_id"] for r0 in rows if r0["pointer_attached"]],
            "clean": [r0["source_id"] for r0 in rows if not r0["pointer_attached"]]}


def _source_remove_delete_verdict(r: dict) -> str:
    """v1.34.56 (A-#12) PURE: verdict sau nlm_cli.source_delete — 'deleted' (ok, count≥1 hoặc không rõ count),
    'noop' (sid đã gỡ từ trước: deleted_count=0 / not-found → idempotent theo trạng thái đích, KHÔNG FAIL), 'fail'."""
    raw = str((r or {}).get("raw") or (r or {}).get("error") or "").lower()
    m = re.search(r"deleted[_\s]*(?:count)?\D*?(\d+)", raw)
    if (r or {}).get("ok"):
        return "noop" if (m and m.group(1) == "0") else "deleted"
    return "noop" if ("not found" in raw or "not_found" in raw or (m and m.group(1) == "0")) else "fail"


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
    phys_by_nb, nb_meta, fails = {}, [], []
    for nb in scope:
        r = _nlm_source_list_cached(nc, nb, refresh=bool(getattr(a, "refresh_live", False)))
        if r.get("ok"):
            phys_by_nb[nb] = r.get("sources") or []
            nb_meta.append({"notebook_id": nb, "count": len(phys_by_nb[nb]), "cached": bool(r.get("cached"))})
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
    payload = {"ok": True, "schema": "nlm_audit_physical.v1", "clean": res["clean"],
               "notebooks": nb_meta, "list_failed": fails, "counts": counts,
               "findings": res["findings"],
               "unverified_scope": {"count": len(res["unverified_scope"]),
                                    "sample": res["unverified_scope"][:10]},
               "suggested_commands": res["suggested_commands"],
               "note": "physical-first: kết luận từ listing VẬT LÝ; nlm_notebook_id chỉ là nơi registry NGHĨ."}
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
    if not _lt.get("ok"):
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
                   "note": "DRY re-plan từ vật lý đích (luôn tươi). ADD >"
                           f"{NLM_BATCH_LINKS_THRESHOLD} doc → BATCH_LINKS khi apply (--api-add ép API). "
                           "Apply: thêm --apply --confirm yes. Dán link xong: CHẠY LẠI đúng lệnh (harvest)."}
        _emit_json_payload(payload, getattr(a, "out", None))
        return 0
    if str(getattr(a, "confirm", "") or "").strip().lower() != "yes":
        print(json.dumps({"ok": False, "error": "CONFIRM_REQUIRED",
                          "note": "nlm-migrate ghi registry (repoint) / add NLM — thêm --confirm yes"},
                         ensure_ascii=False), file=sys.stderr)
        return 2
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
        # v1.34.47 (M2 fix): LUÔN nối shard overflow của scope hiện tại từ REGISTRY (đối xứng đường ghi).
        # Trước đây chỉ env + block _base_also_enabled (=False cho DEFAULT profile) ⇒ base VBQPPL đã overflow
        # bị BỎ nguồn khỏi tra-cứu khi config overflow trống. Best-effort (cross không boot đầy đủ).
        _cur_base = (os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK)
        try:
            for _nb in _resolve_overflow_shards(_manifest_entries(refresh=False), _cur_base):
                if _nb not in nbs:
                    nbs.append(_nb)
        except Exception:  # noqa: BLE001 — chưa có cache → giữ env-only, không chặn cross
            pass
        # A (v1.30.0): profile CỘNG VBQPPL — nối thêm notebook NỀN (base+overflow+shards từ config), profile đứng TRƯỚC.
        if _base_also_enabled(a):
            _, _cfg = _read_config_record(getattr(a, "config", None))
            for _nb in _vbqppl_notebooks(_cfg):
                if _nb not in nbs:
                    nbs.append(_nb)
    r = nc.cross_query(a.query, notebooks=nbs or None, all_notebooks=getattr(a, "all", False))
    if not r.get("ok"):
        # v1.34.60 (E1): cross NLM hard-dead → CÙNG đường verbatim-return (corpus không shard — 1 manifest).
        _v60 = _nlm_or_corpus("nlm-cross", a, notebook_id=(nbs[0] if nbs else None), err=r)
        if _v60["route"] == "corpus_read":
            return _nlm_query_corpus_fallback(a, a.query, cmd="nlm-cross", why=_v60["why"])
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

# ── I11 (v1.34.18): leftover-sweep từ tl.py (affinity-tốt-nhất) ──


def _vbqppl_notebooks(cfg: dict) -> list[str]:
    """A (v1.30.0, PURE): danh sách notebook NỀN VBQPPL từ config — base + overflow + shards (dedup, giữ thứ tự
    base→overflow→shards). Dùng mở rộng đích nlm-cross khi TL_BASE_ALSO."""
    prof = _profiles_from_config(cfg or {}).get(DEFAULT_PROFILE) or {}
    shards = prof.get("shards") if isinstance(prof.get("shards"), list) else []
    out, seen = [], set()
    for x in [prof.get("notebookId") or NLM_BASE_NOTEBOOK, prof.get("overflowNotebookId"), *shards]:
        x = str(x or "").strip()
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out

def _strip_font_runs(text: str) -> str:
    """Lọc bỏ dòng RÁC chỉ chứa TÊN FONT ĐẦY ĐỦ (\"Times New Roman\", \"Arial\", \".VnTime\"...)
    do bộ export DOCX/GDoc rò run-font của ô header bảng vào text trích. Chỉ xóa dòng mà TOÀN BỘ
    nội dung là tên font ĐẦY ĐỦ (+ cỡ tùy chọn) → KHÔNG đụng nội dung pháp lý thật (\"Theo Times
    báo\", \"Arial Group\", \"UTM 48N\", dòng \"Times\"/\"Symbol\" đơn lẻ vẫn giữ). Cố ý KHÔNG dùng
    wildcard tiền-tố (UTM/VNI/SVN + .*) để tránh nuốt nội dung thật. Gọi SAU khi đọc, TRƯỚC khi trả."""
    if not text or "\n" not in text:
        return text
    return "".join(ln for ln in text.splitlines(keepends=True)
                   if not _FONT_RUN_RE.match(ln.rstrip("\r\n")))

def _slice_dieu(text: str, dieu: str) -> str:
    import re as _re
    m = _re.search(rf"(?mi)^\s*Điều\s+{_re.escape(str(dieu))}\b.*?(?=^\s*Điều\s+\d+\b|\Z)", text or "", _re.S)
    return m.group(0).strip() if m else f"[không thấy Điều {dieu}]"

def _split_source_ids(values: list[str] | None, combined: str = "") -> list[str]:
    raw = []
    for val in values or []:
        raw.extend(str(val).split(","))
    if combined:
        raw.extend(str(combined).split(","))
    return _unique_preserve_order([x.strip() for x in raw if x and x.strip()])
