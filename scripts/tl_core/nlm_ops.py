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
        if ent is None:
            _tk = _ingest_dedup_title_key(str(s.get("title") or ""))
            _tcands = by_title.get(_tk) or [] if _tk else []
            ent = _tcands[0] if len(_tcands) == 1 else None  # tier 3: title CHUẨN HOÁ duy nhất mới link
            by = "title"
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


def _reconcile_sweep_note(all_ok: bool, per_notebook: list) -> str:
    """v1.34.42 (BUG1 — grill-with-docs): note ĐIỀU KIỆN cho `nlm-reconcile --all-notebooks`. Trước đây là CHUỖI
    CỨNG 'mọi notebook sạch' in ra KỂ CẢ khi ok=false (lớp 'sai mà báo thành công' — chính công cụ audit tự báo sai).
    all_ok=True → khẳng định sạch; ngược lại → liệt kê notebook rc≠0/finding + hướng dẫn (boot cho rc=2, per-notebook
    --apply cho finding). PURE, test offline."""
    if all_ok:
        return "Lưới cuối lô: mọi notebook SẠCH (desync=0, unregistered=0) = lô settle+link đủ."
    probs = []
    for p in per_notebook or []:
        nb = str(p.get("notebook") or "?")
        _find = [f"{k}={p.get(k)}" for k in ("desync_real", "unregistered_on_nlm", "link_candidates",
                                             "backfill_nlm_notebook_id") if p.get(k)]
        if _find:
            probs.append(f"{nb}({', '.join(_find)})")
        elif p.get("rc") not in (0, None):
            _er = f", {p['error']}" if p.get("error") else ""
            probs.append(f"{nb}(rc={p.get('rc')}{_er})")
    body = "; ".join(probs) if probs else "(không rõ — xem per_notebook)"
    return ("CÓ VẤN ĐỀ — chưa đồng bộ: " + body + ". "
            "rc=2 thường do thiếu cache/scope → chạy `tl --profile <P> boot` trước. "
            "Finding (desync/unregistered/link) → per-notebook `tl nlm-reconcile <nb> --apply`.")


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
        if getattr(a, "apply", False) or getattr(a, "clear_stale", False):
            print(json.dumps({"ok": False, "error": "ALL_NOTEBOOKS_IS_DRY_ONLY",
                              "note": "--all-notebooks chỉ QUÉT (DRY). Sửa: chạy per-notebook "
                                      "`tl nlm-reconcile <notebook_id> --apply`."}, ensure_ascii=False),
                  file=sys.stderr)
            return 2
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
        _per, _all_ok = [], True
        for _nb_i in _nbs:
            _buf = _io.StringIO()
            _ns_i = _ap.Namespace(config=getattr(a, "config", None), profile=getattr(a, "profile", None),
                                  notebook_id=_nb_i, apply=False, clear_stale=False,
                                  force_unsafe=getattr(a, "force_unsafe", False),
                                  refresh=getattr(a, "refresh", False), json=True, out=None, all_notebooks=False)
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
        _out_all = {"ok": _all_ok, "mode": "DRY", "all_notebooks": True, "notebooks_swept": len(_nbs),
                    "per_notebook": _per,
                    "note": _reconcile_sweep_note(_all_ok, _per)}   # v1.34.42 (BUG1): note ĐIỀU KIỆN, hết 'sạch' oan
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
        for e in entries or []:
            if _entry_row_kind(e) != "overflow":
                continue
            nb = str(e.get("nlm_notebook_id") or e.get("notebook_id") or "").strip()
            if nb and nb != base_nb and nb not in dec_ids:
                dec_ids.add(nb)
                findings.append({"finding": "UNDECLARED_REGISTRY_SHARD", "notebook_id": nb})
                declared.append({"id": nb, "role": "observed", "capacity": cap_def, "enabled": False,
                                 "priority": 10_000, "source": "registry"})
        return {"ok": True, "error": None, "shards": declared, "findings": findings, "declared": True}
    # ── declared VẮNG → materialize observed (giữ nguyên hành vi v1.34.47, thêm capacity/priority) ──
    out: list[dict] = []
    if base_nb:
        out.append({"id": base_nb, "role": "primary", "capacity": cap_def, "enabled": True,
                    "priority": 0, "source": "alias"})
    if env_ok:
        out.append({"id": env_ovf, "role": "overflow", "capacity": cap_def, "enabled": True,
                    "priority": 1, "source": "env"})
    counts: dict[str, int] = {}
    for e in entries or []:
        if _entry_row_kind(e) != "overflow":
            continue
        nb = str(e.get("nlm_notebook_id") or e.get("notebook_id") or "").strip()
        if nb and nb != base_nb:
            counts[nb] = counts.get(nb, 0) + 1
    have = {s["id"] for s in out}
    for i, (nb, _n) in enumerate(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))):
        if nb not in have:
            have.add(nb)
            out.append({"id": nb, "role": "overflow", "capacity": cap_def, "enabled": True,
                        "priority": 2 + i, "source": "registry"})
    return {"ok": True, "error": None, "shards": out, "findings": findings, "declared": False}


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
    for e in entries or []:
        nb = str(e.get("nlm_notebook_id") or e.get("notebook_id") or "").strip()
        if not nb:
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
    out: list[str] = []
    seen: set[str] = set()
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
    _dt, _dt_src = _nlm_add_doc_type(getattr(a, "type", None), getattr(a, "drive_id", None))
    if _dt_src.startswith("auto"):
        print(f"[tl] nlm-add: tự nhận --type {_dt} ({_dt_src}) — ép kiểu khác bằng --type.", file=sys.stderr)
    r = nc.source_add(nb, drive_id=getattr(a, "drive_id", None), url=getattr(a, "url", None),
                      file=getattr(a, "file", None), doc_type=_dt,
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
                _bef_na = {"nlm_source_id": "", "nlm_notebook_id": "", "nlm_status": ""}
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
