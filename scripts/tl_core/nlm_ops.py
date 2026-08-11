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


def _nlm_due_rows(entries: list, notebook_id: str, base_notebook_id: str | None = None) -> list[dict]:
    """r179 T8 (ADR-0010, PURE — CONTEXT «nlm_due»): diện PHẢI-CÓ-MẶT theo chính sách corpus trên notebook =
    dòng (corpus=true ∪ row_kind=ref) quy về notebook (nb khớp; blank quy về BASE — cùng luật fold
    _nlm_slot_count), LOẠI họ removed_* (gỡ có chủ đích = RỜI diện, lý do nằm ở hậu tố). KHÁC nlm_claim
    (sổ KHẲNG ĐỊNH có mặt — status họ sống/src). due↔vật lý = coverage_gap (nợ phủ, slot-audit);
    claim↔live = desync (nlm-reconcile). MỘT helper cho CẢ HAI lệnh — một từ vựng, một cách đếm."""
    base_notebook_id = (base_notebook_id or NLM_BASE_NOTEBOOK).strip()
    is_base = notebook_id == base_notebook_id
    out = []
    for e in entries or []:
        if _nlm_status_removed(str(e.get("nlm_status") or "")):
            continue
        if _entry_row_kind(e) != "ref" and str(e.get("corpus") or "").strip().lower() != "true":
            continue
        nbv = str(e.get("nlm_notebook_id") or e.get("notebook_id") or "").strip()
        if nbv == notebook_id or (not nbv and is_base):
            out.append(e)
    return out


def _backfill_nlm_status_candidates(entries: list) -> tuple[list[dict], list[dict]]:
    """r179 T2 (ADR-0010, PURE): ứng viên nắn nlm_status về từ vựng đóng — CHỈ map TẤT ĐỊNH added→pushed,
    live→active (so exact, case-insensitive; map INLINE — bẫy I11: hằng module-level không sống sót
    bind-REBASE). Giá trị ngoài map mà cũng ngoài từ vựng ghi (ready, typo, trash* cũ…) KHÔNG đụng —
    trả riêng `stray` để báo (sửa tay qua `register --nlm-status` sau khi hiểu vì sao có). Dòng map được
    nhưng THIẾU drive_id → stray NO_DRIVE_ID (reg_upsert khoá theo drive_id, không khoá thì không ghi
    an toàn). Trả (sug, stray)."""
    _map = {"added": "pushed", "live": "active"}
    sug, stray = [], []
    for e in entries or []:
        raw = str(e.get("nlm_status") or "").strip()
        if not raw:
            continue
        new = _map.get(raw.lower())
        did = _entry_drive_id(e)
        if new:
            if did:
                sug.append({"drive_id": did, "name": _entry_name(e)[:54],
                            "nlm_status": new, "nlm_status_old": raw})
            else:
                stray.append({"drive_id": "", "name": _entry_name(e)[:40],
                              "nlm_status_old": raw, "why": "NO_DRIVE_ID"})
        elif not _nlm_status_write_ok(raw):
            stray.append({"drive_id": did or "", "name": _entry_name(e)[:40],
                          "nlm_status_old": raw, "why": "OUTSIDE_MAP"})
    return sug, stray


def cmd_backfill_nlm_status(a) -> int:
    """r179 T2 (ADR-0010): nắn nlm_status về TỪ VỰNG ĐÓNG một lần — added→pushed, live→active, qua
    reg_upsert PER-ROW (journaled + verified + undo được; [[vbqppl-sohieu-must-have-year]] chọn upsert
    cho sửa-giá-trị, KHÔNG reg_bulk). DRY mặc định; giá trị ngoài map không đụng (báo stray)."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:  # noqa: BLE001
        print(f"[tl] backfill-nlm-status: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    sug, stray = _backfill_nlm_status_candidates(entries)
    lim = getattr(a, "limit", None) or len(sug)
    sel = sug[:lim]
    if getattr(a, "apply", False):
        _ok_gate, _ = _apply_gate(a, write_cols="nlm_status")
        if not _ok_gate:
            return 2
        try:
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        except (Exception, SystemExit):
            pass
        g = _gas()
        run_id = _apply_journal_start("backfill-nlm-status", {"n": len(sel)})
        applied, failed = 0, []
        for s in sel:
            v = _journaled_reg_upsert(run_id, g, {"drive_id": s["drive_id"], "nlm_status": s["nlm_status"]},
                                      before={"nlm_status": s["nlm_status_old"]})
            if v.get("verified"):
                applied += 1
            else:
                failed.append({"drive_id": s["drive_id"], "error": str(v.get("error") or "")[:120]})
        _invalidate_manifest_cache()
        _journal_append(run_id, {"t": "run_end", "ok": not failed,
                                 "counts": {"applied": applied, "failed": len(failed)}})
        out = {"ok": not failed, "applied": applied, "failed": failed, "suggested": len(sug),
               "stray_count": len(stray), "stray": stray[:20], "journal": run_id}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        print(f"[tl] backfill-nlm-status: ghi {applied}/{len(sel)}. journal={run_id}. "
              f"MANIFEST_STALE: `tl boot --refresh`.", file=sys.stderr)
        return 0 if not failed else 1
    from collections import Counter
    cnt = Counter(f"{s['nlm_status_old']}→{s['nlm_status']}" for s in sug)
    if getattr(a, "json", False):
        print(json.dumps({"ok": True, "mode": "DRY", "suggested_count": len(sug),
                          "distribution": dict(cnt), "stray_count": len(stray), "stray": stray[:20],
                          "suggested": sel}, ensure_ascii=False, indent=2))
    else:
        print(f"== backfill-nlm-status DRY · map được {len(sug)} · stray (không đụng) {len(stray)} "
              f"(--apply để ghi) ==")
        print("  phân bố: " + (", ".join(f"{k}={v}" for k, v in cnt.most_common()) or "(trống)"))
        for s in sel[:20]:
            print(f"  {s['nlm_status_old']:8s}→ {s['nlm_status']:8s} {s['name']}")
        for x in stray[:8]:
            print(f"  ⚠ STRAY [{x['why']}]: nlm_status='{x['nlm_status_old']}' — {x['name']}"
                  " (ngoài map — hiểu nguồn gốc rồi sửa tay `register --nlm-status`)")
    return 0


_SLOT_LIVE_DIFF_WARN = 2   # r208 (báo cáo 25-07 mục 2.2): lệch registry↔LIVE quá 2 ⇒ gắn cờ

# r208b (báo cáo 25-07 mục 3.2): thông điệp DỰ PHÒNG khi KHÔNG nạp được nlm_cli (nguồn sự thật là
# nlm_cli.AUTH_FIX_HINT*). Chỉ dùng ở chế độ suy hoá — selftest drift-lock bắt CẢ BA chuỗi phải nêu
# ĐÚNG thứ tự nlm-auth-load → nlm-auth-pull → nlm login, nên bản dự phòng không lệch đường được.
_AUTH_FIX_FALLBACK = ("🔴 AUTH hết hạn: `tl nlm-auth-load` → `tl nlm-auth-pull` (cần TL_MASTER_KEY) "
                      "→ `nlm login` (tương tác) · ⚠ ĐANG TRONG LƯỢT RÀ HỒ SƠ (RASOAT_HOSO_LOOP §4b): "
                      "KHÔNG tự chạy (1)/(2) — chuyển chế độ không-NLM và ĐI TIẾP")   # r213 ĐỢT 5: câu trừ ngữ cảnh


def nlm_auth_fix_hint(compact: bool = True) -> str:
    """r208b 3.2 (ca thật 25-07): CHUỖI KHẮC PHỤC AUTH đúng đường, một nguồn sự thật.
    compact=True → bản ngắn nối vào note/live_note; False → bản đầy đủ (giải thích headless vs
    tương tác + lấy TL_MASTER_KEY ở đâu). KHÔNG bao giờ chỉ hô `nlm login` — lệnh đó TƯƠNG TÁC,
    vô dụng trong Cowork/headless và chính là bẫy đã ngốn nhiều bước của người vận hành."""
    try:
        _nc = _imp("nlm_cli")
        return _nc.AUTH_FIX_HINT_SHORT if compact else _nc.AUTH_FIX_HINT
    except Exception:  # noqa: BLE001 — không nạp được adapter thì vẫn phải chỉ ĐÚNG đường
        return _AUTH_FIX_FALLBACK


def _slot_live_counts(notebook_ids, skip: bool = False) -> dict:
    """r208: đọc source_count LIVE cho TỪNG shard (nhánh --all-shards trước đây bỏ hẳn bước này).

    Trả {nb: {"live": int|None, "error": str|None}}. Bài học M2 (v1.33.35 — slot-audit lệch −288 GIẢ
    khi cookie chết): `notebook_get` trả {ok:False} chứ KHÔNG raise ⇒ TUYỆT ĐỐI không quy về 0; đọc
    hỏng thì để live=None và ghi lý do, để chỗ gọi giữ nguyên số registry thay vì suy ra gap ảo."""
    out: dict = {}
    if skip:
        return out
    try:
        _nc = _imp("nlm_cli")
    except Exception as e:  # noqa: BLE001 — offline/không cred: giữ nguyên hành vi cũ, KHÔNG chặn
        return {nb: {"live": None, "error": f"không nạp được nlm CLI ({type(e).__name__})"} for nb in notebook_ids}
    for nb in notebook_ids:
        if not nb:
            continue
        try:
            _ng = _nc.notebook_get(nb)
            if isinstance(_ng, dict) and _ng.get("ok"):
                out[nb] = {"live": int(_ng.get("source_count") or 0), "error": None}
            else:
                _err = str((_ng or {}).get("error") or "?")[:120]
                if (_ng or {}).get("auth_hint"):
                    _err += " — " + nlm_auth_fix_hint()   # r208b 3.2: một nguồn sự thật cho chuỗi khắc phục
                out[nb] = {"live": None, "error": _err}
        except Exception as e:  # noqa: BLE001
            out[nb] = {"live": None, "error": f"{type(e).__name__}"}
    return out


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
        # r208 (báo cáo 25-07 mục 2.2): nhánh --all-shards TRƯỚC ĐÂY chỉ đếm từ manifest/registry, KHÔNG hỏi
        # LIVE — trong khi nhánh 1-notebook đã neo LIVE từ v1.33.35 (WS1/A3). Hậu quả đo tươi 25-07 trên
        # registry LÀNH: mọi shard báo THIẾU (297 vs 300 · 275 vs 293 · 54 vs 108 · 17 vs 29) ⇒ base hiện
        # «còn 3 chỗ» trong khi ĐÃ ĐẦY ⇒ nạp tiếp = tràn. Nay đối chiếu LIVE từng shard, in cạnh nhau.
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
        # r208: LIVE là chân lý (quy tắc SKILL) — hỏi từng shard, KHÔNG suy 0 khi đọc hỏng (bài học M2
        # v1.33.35: cookie chết → source_count thiếu → gap −288 GIẢ). --no-live để tắt (offline/không cred).
        _live_sa = _slot_live_counts([nb for nb, _ in rows], skip=getattr(a, "no_live", False))
        _eff_of = lambda nb, n: (_live_sa.get(nb, {}).get("live") if _live_sa.get(nb, {}).get("live") is not None else n)  # noqa: E731
        warn = [{"notebook_id": nb, "count": n, "cap": _cap_of(nb)} for nb, n in rows
                if _eff_of(nb, n) >= min(near, _cap_of(nb))]
        _shards_sa = []
        for nb, n in rows:
            _lv = _live_sa.get(nb, {})
            _live_n, _eff = _lv.get("live"), _eff_of(nb, n)
            _row = {"notebook_id": nb, "count": n, "cap": _cap_of(nb),
                    "near_full": _eff >= min(near, _cap_of(nb)), "full": _eff >= _cap_of(nb)}
            if _live_n is not None:
                _row["live_source_count"] = _live_n
                _row["live_diff"] = _live_n - n          # dương = registry BÁO THIẾU so với LIVE
                _row["live_mismatch"] = abs(_live_n - n) > _SLOT_LIVE_DIFF_WARN
            elif _lv.get("error"):
                _row["live_read_failed"] = True
                _row["live_note"] = _lv["error"]
            _shards_sa.append(_row)
        res = {"ok": True, "gate": "slot-audit", "cap": NLM_SLOT_CAP, "near_full_threshold": near,
               "topology_ok": _topo_sa.get("ok"),
               "live_checked": not getattr(a, "no_live", False),
               "live_diff_warn_threshold": _SLOT_LIVE_DIFF_WARN,
               "shards": _shards_sa,
               "near_full_shards": warn}
        _mm_sa = [r for r in _shards_sa if r.get("live_mismatch")]
        if _mm_sa:
            res["live_mismatch_shards"] = _mm_sa
            res["live_mismatch_note"] = ("LIVE ≠ registry: LIVE LÀ CHÂN LÝ — quyết định còn/hết slot phải theo "
                                         "live_source_count. Lệch thường do dòng removed_*/ref hoặc nguồn thêm "
                                         "ngoài skill; đối soát per-source: `tl nlm-reconcile <nb>` (DRY).")
        if _topo_sa.get("findings"):
            res["topology_findings"] = _topo_sa.get("findings")
        if getattr(a, "json", False):
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(f"== slot-audit --all-shards · {len(rows)} shard · cap default={NLM_SLOT_CAP} ngưỡng near-full={near} ==")
            if res.get("live_checked"):
                print(f"   {'':7s} {'notebook':40s} {'registry':>9s} {'LIVE':>6s}   (LIVE là chân lý)")
            for _r in _shards_sa:
                nb, n, _c = _r["notebook_id"], _r["count"], _r["cap"]
                _live_n = _r.get("live_source_count")
                _eff = _live_n if _live_n is not None else n
                mk = "✗ FULL" if _eff >= _c else ("⚠ NEAR" if _eff >= min(near, _c) else "·")
                if _live_n is None:
                    _tail = f"{n}/{_c}" + ("   ⚠ không đọc được LIVE" if _r.get("live_read_failed") else "")
                    print(f"  {mk:7s} {nb[:40]:40s} {_tail}")
                else:
                    _flag = f"   ⚠ LỆCH {_live_n - n:+d}" if _r.get("live_mismatch") else ""
                    print(f"  {mk:7s} {nb[:40]:40s} {n:>9d} {_live_n:>4d}/{_c}{_flag}")
            if warn:
                print(f"  ⚠ {len(warn)} shard chạm ngưỡng → chuẩn bị shard kế (đừng để ingest-missing chạm partial).")
            if _mm_sa:
                print(f"  ⚠ {len(_mm_sa)} shard LỆCH registry↔LIVE > {_SLOT_LIVE_DIFF_WARN} — quyết định slot theo "
                      f"cột LIVE, KHÔNG theo registry. Đối soát: `tl nlm-reconcile <nb>` (DRY).")
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
                                    + (" — " + nlm_auth_fix_hint() if _ng.get("auth_hint") else "")   # r208b 3.2
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
    # r179 T8 (ADR-0010 — sự cố «51/40/51»: hai lệnh hai luật đếm, số vênh không nhãn): slot-audit nay in
    # CẢ HAI số tên tường minh — nlm_due/coverage_gap (diện PHẢI-CÓ ↔ ghi nhận) + desync_estimate (vật lý ↔
    # nlm_claim theo ĐẾM; per-source chuẩn ở nlm-reconcile). Khoá `gap` trần BỎ (cấm theo CONTEXT).
    _active179 = {"pushed", "synced", "added", "stale", "true", "1", "yes"}
    _due179 = _nlm_due_rows(entries, notebook_id, getattr(a, "base_notebook_id", None))
    _cov179 = [e for e in _due179
               if not (e.get("nlm_source_id") or e.get("source_id"))
               and str(e.get("nlm_status") or e.get("nlm") or "").strip().lower() not in _active179]
    _rm_point179 = 0
    for e in entries or []:
        if not _nlm_status_removed(str(e.get("nlm_status") or "")):
            continue
        if not (e.get("nlm_source_id") or e.get("source_id")):
            continue
        _nbv = str(e.get("nlm_notebook_id") or e.get("notebook_id") or "").strip()
        if _nbv == notebook_id or (not _nbv and out.get("is_base_notebook")):
            _rm_point179 += 1
    out["nlm_due_rows"] = len(_due179)
    out["coverage_gap"] = len(_cov179)
    if _cov179:
        out["coverage_gap_sample"] = [f"{_entry_sohieu(e) or ''}|{_entry_name(e)[:40]}" for e in _cov179[:10]]
    out["removed_family_still_pointing"] = _rm_point179
    out["labels_note"] = ("coverage_gap = nlm_due (diện PHẢI-CÓ-MẶT: corpus∪ref, trừ removed_*) CHƯA có ghi nhận "
                          "có mặt trong sổ — nợ phủ, mức sổ-cái (per-source: nlm-reconcile coverage_gap). "
                          "desync_estimate = vật_lý − nlm_claim_rows theo ĐẾM (per-source chuẩn: nlm-reconcile "
                          "desync_real). Hai phép đo trả lời hai câu hỏi KHÁC nhau (ADR-0010).")
    if phys is not None:
        reg = out.get("slots_effective", 0)
        out["physical_source_count"] = phys
        out["registry_estimate"] = reg
        out["ref_rows"] = _ref_rows
        out["nlm_claim_rows"] = reg + _ref_rows
        out["gap_vs_corpus_estimate"] = phys - reg
        out["desync_estimate"] = phys - out["nlm_claim_rows"]
        out["ground_truth"] = "physical (tl nlm-get / nlm notebook get)"
        if out["desync_estimate"] != 0 and out["desync_estimate"] == _rm_point179:
            out["note_removed_live"] = (f"desync_estimate {out['desync_estimate']:+d} được giải thích TRỌN bằng "
                                        f"{_rm_point179} dòng họ removed_* còn con trỏ nguồn (nguồn có thể vẫn "
                                        f"sống trên notebook — vd removed_from_drive: file Drive đã xoá, nguồn "
                                        f"NLM giữ). KHÔNG phải desync sổ; xác nhận per-source: `tl nlm-reconcile`.")
        elif out["desync_estimate"] != 0:
            out["warning"] = (f"Lệch {phys} vật lý vs {out['nlm_claim_rows']} nlm_claim_rows (corpus {reg} + ref "
                              f"{_ref_rows}) ({out['desync_estimate']:+d}) — backfill nlm_notebook_id "
                              f"(`tl backfill-notebook`) hoặc nguồn add thẳng chưa ghi registry; đối chiếu "
                              f"`tl nlm-reconcile` (desync_real per-source) trước khi ghi.")
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
            line += (f" | VẬT LÝ={phys} desync_estimate={out['desync_estimate']:+d}"
                     f" | nlm_due={out['nlm_due_rows']} coverage_gap={out['coverage_gap']}")
        print(line)
        if out.get("note_removed_live"):
            print("  ℹ " + out["note_removed_live"])
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


_ROW_KIND_PROTECTED = ("ref", "thuong")   # kind NGHIỆP VỤ — không suy từ topology, không bao giờ clobber


def _topology_row_kind_findings(entries: list[dict], topo: dict) -> list[dict]:
    """v1.34.49 (F-06 doctor, PURE): bất biến `notebook==primary ⇔ row_kind∈{own,''}` và `notebook∈overflow ⇔
    row_kind=='overflow'` cho dòng ĐÃ có nlm_notebook_id. Bỏ qua kind bảo hộ (ref/thuong) + dòng chưa lên NLM.
    Trả findings [{drive_id, notebook_id, row_kind, finding}] — REPORT-ONLY.

    r232 SỬA CHÚ THÍCH: bản cũ ghi «sửa: nlm-reconcile --apply / reg_upsert» — vế `nlm-reconcile
    --apply` SAI. Reconcile ghi row_kind theo topology nhưng chỉ KÈM dòng backfill/link, tức dòng
    THIẾU nlm_notebook_id; còn điều kiện lọt vào findings này là ĐÃ CÓ nlm_notebook_id (`if not nb:
    continue` ngay dưới) ⇒ hai tập RỜI NHAU theo cấu trúc, --apply không bao giờ chạm tới. Đường
    sửa thật là ghi registry cho từng dòng (reg_upsert row_kind)."""
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
                (" — " + nlm_auth_fix_hint() if r.get("auth_hint") else "")   # r208b 3.2
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


def _nlm_draft_sources(entries, *, source_ids=None, notebook_id: str = "") -> list:
    """PURE (r215 — sổ lỗi `DU_THAO_ND_BHXH_DE_CORPUS_TRUE_VA_DA_DAY_LEN_NLM`): các dòng registry LÀ
    DỰ THẢO mà đang NẰM TRONG phạm vi sắp hỏi NLM.

    Đo 27-07-2026 trên hồ sơ BHXH: hai DỰ THẢO nghị định (`DUTHAO_ND_…`) mang `corpus=true`,
    `nlm_status=pushed` trong chính notebook hồ sơ. Cờ `DRAFT_NOT_EFFECTIVE` CÓ bắn ở đường phân loại,
    nhưng **không đường nào nói ra vào lúc hỏi** ⇒ câu trả lời RAG có thể trộn chữ dự thảo với luật
    đang có hiệu lực mà người hỏi không biết.

    ★CỐ Ý KHÔNG CHẶN: dự thảo nằm trong notebook HỒ SƠ TRÌNH là đúng chỗ — chúng chính là đối tượng rà.
    Cái sai là phục vụ chúng LẶNG LẼ. Vì vậy đây là phép đo để CẢNH BÁO, không phải cổng cấm.

    Phạm vi: có `source_ids` → chỉ xét đúng các dòng trỏ tới sid đó; không có → cả notebook (dòng còn
    trỏ `nlm_source_id` và thuộc `notebook_id` nếu biết). Đọc registry, KHÔNG đoán từ envelope NLM."""
    _sids = {str(s).strip().lower() for s in (source_ids or []) if str(s).strip()}
    _nb = str(notebook_id or "").strip().lower()
    out = []
    for e in (entries or []):
        sid = str(_entry_nlm(e) or "").strip()
        if not sid:
            continue
        if _sids:
            if sid.lower() not in _sids:
                continue
        elif _nb:
            _enb = str(_entry_nlm_notebook_id(e) or "").strip().lower()
            if _enb and _enb != _nb:
                continue
        if _entry_is_draft(e):
            out.append({"source_id": sid, "name": _entry_name(e),
                        "sohieu": _entry_sohieu(e), "drive_id": _entry_drive_id(e)})
    return sorted(out, key=lambda r: (str(r["name"]), str(r["source_id"])))


def _nlm_scope_shortfall(requested, data) -> dict:
    """PURE (r214): đối chiếu phạm vi ĐÃ YÊU CẦU (`--source-id`) với phạm vi NLM TỰ KHAI đã dùng.

    Trả {"do_duoc": bool, "used": [id…], "thieu": [id…]}.

    ★`do_duoc=False` ⇒ envelope KHÔNG khai `sources_used` → KHÔNG kết luận gì. Tuyệt đối KHÔNG suy ra
    "đủ nguồn" từ chỗ không đo được (đúng bài học 26-07: câu trả lời «không tìm thấy» của NLM không
    phải kết luận âm tính).

    CỐ Ý chỉ nhận đúng khoá `sources_used`: các khoá họ hàng (`sources`, `citations`) là nguồn được
    TRÍCH DẪN — vốn là tập con HỢP LỆ của nguồn được QUÉT, đoán sang đó chỉ đẻ báo động giả."""
    _req = [str(s).strip() for s in (requested or []) if str(s).strip()]
    if not _req or not isinstance(data, dict):
        return {"do_duoc": False, "used": [], "thieu": []}
    raw = data.get("sources_used")
    if raw is None and isinstance(data.get("data"), dict):   # envelope lồng 1 tầng
        raw = data["data"].get("sources_used")
    if not isinstance(raw, list):
        return {"do_duoc": False, "used": [], "thieu": []}
    used = []
    for item in raw:
        if isinstance(item, str):
            used.append(item.strip())
        elif isinstance(item, dict):
            for k in ("id", "source_id", "sourceId"):
                if str(item.get(k) or "").strip():
                    used.append(str(item[k]).strip())
                    break
    _low = {u.lower() for u in used if u}
    return {"do_duoc": True, "used": used, "thieu": [s for s in _req if s.lower() not in _low]}


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
    # r214 (sổ lỗi NLM_QUERY_LOAI_NGUON_KHONG_BAO): tầng 2 sau khi đã vá argv `-s` gộp CSV ở nlm_cli —
    # NLM vẫn có thể thu hẹp phạm vi vì lý do phía nó (nguồn chưa index xong / bị loại). "Im lặng thu hẹp
    # phạm vi" là kiểu hỏng đẻ ra KẾT LUẬN ÂM TÍNH GIẢ, nên phải nói ra.
    _req_sids = list(getattr(a, "source_id", None) or [])
    _strict = bool(getattr(a, "strict_scope", False))
    _scope = _nlm_scope_shortfall(_req_sids, r.get("data"))
    if _strict and _req_sids and not _scope["do_duoc"]:
        # fail-CLOSED: người dùng ĐÃ đòi bảo đảm phạm vi mà envelope không khai `sources_used` ⇒ không
        # chứng minh được thì KHÔNG phát câu trả lời ra stdout (agent hạ nguồn sẽ tưởng là đủ nguồn).
        print(json.dumps({"ok": False, "error": "SCOPE_UNVERIFIABLE",
                          "requested": _req_sids,
                          "fix": "bỏ --strict-scope để nhận câu trả lời kèm cảnh báo, hoặc kiểm phạm vi "
                                 "bằng `tl nlm-get`/`nlm-list` rồi so nguyên văn trên cache."},
                         ensure_ascii=False), file=sys.stderr)
        return 2
    if _scope["thieu"]:
        _msg = (f"[tl] ⚠ NLM_SCOPE_SHORTFALL: yêu cầu {len(_req_sids)} nguồn, NLM khai dùng "
                f"{len(_scope['used'])} — THIẾU: {', '.join(_scope['thieu'])}. Câu trả lời chỉ phủ phần "
                f"nguồn còn lại ⇒ KHÔNG đọc 'không tìm thấy' thành kết luận âm tính.")
        if _strict:
            print(json.dumps({"ok": False, "error": "NLM_SCOPE_SHORTFALL", "requested": _req_sids,
                              "sources_used": _scope["used"], "missing": _scope["thieu"]},
                             ensure_ascii=False), file=sys.stderr)
            return 2
        print(_msg, file=sys.stderr)
    # r215: nguồn DỰ THẢO trong phạm vi vừa hỏi — nói ra TRƯỚC khi in câu trả lời, để người đọc không
    # đọc chữ dự thảo thành quy phạm đang có hiệu lực. Cảnh báo, KHÔNG chặn (dự thảo thuộc hồ sơ trình).
    try:
        _drafts = _nlm_draft_sources(_manifest_entries(refresh=False),
                                     source_ids=_req_sids, notebook_id=nb)
    except Exception:  # noqa: BLE001 — registry hỏng không được chặn đường hỏi
        _drafts = []
    if _drafts:
        print(f"[tl] ⚠ {DRAFT_WARNING}: phạm vi vừa hỏi có {len(_drafts)} nguồn là DỰ THẢO — "
              f"{', '.join(str(d['name'])[:56] for d in _drafts[:4])}"
              f"{' …' if len(_drafts) > 4 else ''}. Câu trả lời có thể TRỘN chữ dự thảo với văn bản đang "
              f"có hiệu lực; không viện dẫn phần nào chưa đối chiếu nguyên văn trên bản chính thức.",
              file=sys.stderr)
    print(json.dumps(r.get("data"), ensure_ascii=False, indent=2) if r.get("data") is not None else r.get("text", ""))
    print("[tl] LƯU Ý: RAG chỉ ĐỊNH VỊ; verify nguyên văn bằng cache/raw (KHÔNG nhận RAG làm nguyên văn).", file=sys.stderr)
    return 0


# ── v1.34.54 (A1+C8+B1 — grill Q3/Q8 2026-07-15): tuổi cookie + preflight 2 tầng + batch-link ──
_NLM_COOKIE_LIFE_MIN = 60      # hồ sơ DBSC 2026-07-12: đời cookie ~1h, `nlm login` là đủ
_NLM_COOKIE_WARN_AGE_MIN = 45  # tuổi vượt ngưỡng → khuyên re-auth trước lô dài / chuyển nlm-links
NLM_BATCH_LINKS_THRESHOLD = 4  # F5 van 1 (r192, grilling 23-07): lô >4 nguồn → KHÔNG auto-add, xuất bảng tay (trước: >2 — grill Q3(a); hằng số, KHÔNG config env — D7)
# r208d (user duyệt 26-07): F7 ĐỔI TỪ CHẶN-THEO-TUỔI SANG CANARY LIVE. Ngưỡng 50' cũ dựng trên «đời
# cookie ~60'» — đo tươi 25/26-07 chứng minh KHÔNG có TTL 1h nào (cookie phiên hạn 380 NGÀY; chết là do
# token xoay `__Secure-1PSIDRTS` hết hạn mà CLI nlm không gia hạn) ⇒ tuổi KHÔNG dự đoán được cái chết:
# phiên chết thật lúc `age_min` mới 5,2' trong khi công cụ hứa «còn 54,8'». Nay tuổi CHỈ CÒN CẢNH BÁO;
# chốt chặn là verdict probe LIVE. Đổi tên hằng cho khỏi nói dối (MAX ⇒ WARN).
NLM_COOKIE_BATCH_WARN_MIN = 50  # tuổi (phút) từ lần xác thực thành công gần nhất → CẢNH BÁO trước lô; KHÔNG chặn


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
            # v1.35.65: MIRROR quy tắc `_nlm_lv_age_seconds` (tl_gws) — viết INLINE vì hàm này re-home
            # __globals__ về namespace tl (bẫy I11), thêm tên module-level ở đây sẽ NameError sau bind.
            # Vì sao cần: jar vừa `nlm-auth-load` từ máy KHÁC MÚI GIỜ còn nguyên mốc naive của máy đó
            # (đo 29-07-2026: −465,6') ⇒ tuổi ÂM ⇒ ngưỡng NLM_COOKIE_BATCH_WARN_MIN im đúng lúc cần
            # nhất (ngay sau khi nạp bundle — lúc cookie dễ cũ nhất). Mốc ở TƯƠNG LAI quá dung sai
            # đồng hồ ⇒ BỎ, rơi xuống `extracted_at` (epoch — tz-safe).
            _t0 = _dt.fromisoformat(str(lv))
            _age = ((_dt.now(_t0.tzinfo) if _t0.tzinfo else _dt.now()) - _t0).total_seconds()
            if _age >= 0:
                return _age / 60.0
            if _age >= -120.0:                      # dung sai đồng hồ (NTP) — coi như vừa xác thực
                return 0.0
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


# r208c 3.1 (ĐO 25-07 23:5x — đo tươi jar cục bộ, xem CHANGELOG): token XOAY phiên của Google
# (DBSC). Đây là credential DUY NHẤT ngắn hạn trong jar — mọi cookie phiên khác (SID/__Secure-1PSID/
# HSID/SSID/APISID/OSID…) đo được hạn 2027-08-09 = 380 NGÀY, `1PSIDTS`/`SIDCC` 365 ngày. Hết hạn
# token này ⇒ phiên KHÔNG gia hạn được nữa, chỉ có thể THAY (`nlm login`). HẰNG ⇒ re-export TRỰC TIẾP
# ở tl.py, KHÔNG cho vào _STUB_MAP (bẫy stub-biến-hằng-thành-hàm).
_NLM_ROTATION_COOKIE_NAMES = ("__Secure-1PSIDRTS", "__Secure-3PSIDRTS")


def _nlm_rotation_token_state(jar=None) -> dict:
    """r208c 3.1 (PURE-ish, jar tiêm được): trạng thái token XOAY phiên trong cookie jar nlm — tín hiệu
    DUY NHẤT trong jar thật sự nói được điều gì về tuổi thọ phiên.

    Trả {"found":bool, "expired":bool|None, "expires_in_min":float|None, "name":str}. found=False ⇒
    KHÔNG kết luận gì (jar lạ/chưa login máy này) — TUYỆT ĐỐI không suy ra 'còn sống'.

    Vì sao cần: mô hình cũ ước lượng đời cookie bằng HẰNG SỐ 60' rồi in `est_remaining_min = 60 − tuổi`.
    Đo tươi 25-07 cho thấy con số đó sai CẢ HAI CHIỀU — đầu phiên `alive:true` mà báo còn 0,0'; cuối
    phiên `alive:false` (phiên ĐÃ CHẾT) mà báo **còn 54,8'** và `warn` RỖNG. Trấn an giả trên xác chết."""
    import time as _t
    out = {"found": False, "expired": None, "expires_in_min": None, "name": ""}
    rows = jar
    if rows is None:
        base = Path.home() / ".notebooklm-mcp-cli"
        for _rel in (("profiles", "default", "cookies.json"), ("auth.json",)):
            try:
                _d = json.loads((base.joinpath(*_rel)).read_text(encoding="utf-8"))
                rows = _d if isinstance(_d, list) else (_d.get("cookies") or [])
                if rows:
                    break
            except Exception:  # noqa: BLE001 — chưa login máy này / jar hỏng → found=False
                rows = None
    _best = None
    for c in (rows or []):
        if not isinstance(c, dict) or c.get("name") not in _NLM_ROTATION_COOKIE_NAMES:
            continue
        try:
            _e = float(c.get("expires") or c.get("expirationDate") or c.get("expiry") or 0)
        except Exception:  # noqa: BLE001
            continue
        if _e > 0 and (_best is None or _e > _best[1]):
            _best = (str(c.get("name")), _e)
    if _best:
        out.update(found=True, name=_best[0],
                   expires_in_min=round((_best[1] - _t.time()) / 60.0, 1),
                   expired=(_best[1] <= _t.time()))
    return out


def _nlm_preflight_report(notebook_id: str, *, probe: bool = True) -> dict:
    """v1.34.54 (A1+C8, doctrine M1): tầng 1 = probe LIVE `notebook_get` (login --check KHÔNG chứng minh cookie
    sống — M1 v1.33.35); tầng 2 = tín hiệu cục bộ. warn[] chỉ CẢNH BÁO, caller tự quyết chặn/không.
    probe=False khi caller đã tự probe (không gọi NLM 2 lần).

    r208c 3.1: BỎ HẲN `est_remaining_min` (60 − tuổi) — đo tươi 25-07 chứng minh nó nói dối cả hai chiều,
    tệ nhất là hứa «còn 54,8 phút» trên phiên ĐÃ CHẾT với `warn` rỗng. Thay bằng thứ ĐO ĐƯỢC:
    `rotation_token_expired`/`rotation_token_min` (hạn thật trong jar) + verdict probe LIVE. `age_min`
    GIỮ nhưng đọc cho đúng nghĩa: thời gian từ LẦN XÁC THỰC THÀNH CÔNG GẦN NHẤT, KHÔNG phải tuổi cookie
    và KHÔNG dự đoán được cái chết. r208d ĐỔI van F7 theo đúng đó: cổng lô KHÔNG còn chặn theo tuổi mà là
    CANARY LIVE (`alive is False` → rc=2 `NLM_AUTH_DEAD_BEFORE_BATCH`); `age_min` chỉ còn nuôi CẢNH BÁO
    `NLM_COOKIE_BATCH_WARN_MIN` (50′); hằng ngưỡng-CHẶN cũ đã GỠ — đừng hồi sinh tên đó trong doc/mã."""
    rep = {"alive": None, "why": "", "age_min": None, "warn": []}
    age = _nlm_auth_age_minutes()
    if age is not None:
        rep["age_min"] = round(age, 1)
        if age > _NLM_COOKIE_WARN_AGE_MIN:
            rep["warn"].append(f"COOKIE_AGE_HIGH: {age:.0f}' kể từ lần xác thực THÀNH CÔNG gần nhất "
                               f"(ngưỡng {_NLM_COOKIE_WARN_AGE_MIN}') — nên `nlm login` trước lô dài, hoặc "
                               f"chuyển đường `tl nlm-links` (batch dán tay). LƯU Ý: đây KHÔNG phải tuổi "
                               f"cookie và KHÔNG dự đoán được thời điểm chết — chốt duy nhất là probe LIVE.")
    _rot = _nlm_rotation_token_state()
    if _rot.get("found"):
        rep["rotation_token_expired"] = bool(_rot["expired"])
        rep["rotation_token_min"] = _rot["expires_in_min"]
        if _rot["expired"]:
            rep["warn"].append(
                f"ROTATION_TOKEN_EXPIRED: {_rot['name']} hết hạn {abs(_rot['expires_in_min']):.0f}' trước "
                "⇒ phiên này KHÔNG GIA HẠN được nữa, chỉ có thể THAY bằng `nlm login` (tương tác). Phiên "
                "vẫn có thể sống thêm một lúc rồi chết ĐỘT NGỘT — không đoán trước được; đừng mở lô dài.")
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
    if rep["alive"] is False:
        # r208c 3.1 (đo 25-07): `nlm-auth-status` từng trả alive:false với warn RỖNG — báo chết mà KHÔNG
        # một dòng khắc phục nào, đúng thứ báo cáo mục 3.2 phàn nàn. Chết thì PHẢI kèm đường ra.
        rep["fix"] = nlm_auth_fix_hint(compact=False)
        rep["warn"].append("AUTH_DEAD: " + nlm_auth_fix_hint())
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


# r196 (TRINH 3.9 — ca KL 137-KL/TW 24-07): NOT_FOUND trên MỘT notebook = ĐÍCH KHÔNG NHÌN THẤY (id sai /
# flake backend sau mutation lớn — eventual consistency), KHÔNG phải «NLM chết» (auth alive, MCP cùng
# notebook OK cùng lúc). Backoff mirror F6 r192 (GAS retry 5s/15s kể cả 404).
_NLM_NOT_FOUND_RETRY_DELAYS = (5, 15)


def _nlm_not_found(why: str) -> bool:
    """PURE (r196): lỗi lớp NOT_FOUND của NLM API (nlm CLI in «Failed to get notebook: API error (code 5):
    NOT_FOUND»). Đứng SAU _nlm_hard_dead khi phân loại — chuỗi auth không bao giờ khớp lớp này."""
    low = (why or "").lower()
    return ("not_found" in low or "not found" in low or "(code 5)" in low or "404" in low)


def _nlm_verdict_sleep(seconds: float) -> None:
    """Hook ngủ giữa các nhịp retry NOT_FOUND của _nlm_verdict — tách riêng để selftest stub (bẫy I11:
    hàm rebase đọc globals tl → test patch _TL_MODULE._nlm_verdict_sleep)."""
    import time as _t
    _t.sleep(seconds)


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
        # r196 (TRINH 3.9): NOT_FOUND retry backoff 5s/15s (flake backend sau mutation lớn cần thời gian
        # settle — retry tức thì ×1 của ADR-7 vẫn trong cửa sổ flake); transient khác giữ 1 nhịp tức thì.
        _delays = list(_NLM_NOT_FOUND_RETRY_DELAYS) if _nlm_not_found(why) else [0]
        for _d in _delays:
            if _d:
                _nlm_verdict_sleep(_d)
            rep2 = _nlm_preflight_report(notebook_id)
            alive, why = rep2.get("alive"), str(rep2.get("why") or why)
            if alive is not False:
                break
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
    # r196 (TRINH 3.9): NOT_FOUND bền (đã backoff 5s/15s) ≠ NLM chết — KHÔNG rẽ fallback/defer (defer ghi
    # nlm_status=deferred trỏ notebook không nhìn thấy = poison registry nếu id sai; banner «NLM OFFLINE»
    # nói dối trạng thái khi auth sống). Route 'not_found' fail-closed + playbook; lệnh không xử route này
    # rơi về đường cũ (gate live tự fail với lỗi thật).
    if _nlm_not_found(why) and not _nlm_hard_dead(why):
        out["route"] = "not_found"
        print(f"[tl] ⚠ NOTEBOOK NOT_FOUND qua nlm CLI ({(why or '')[:100]}) — auth có thể VẪN SỐNG, đây là "
              f"đích-không-nhìn-thấy chứ không phải NLM offline. Kiểm --notebook-id (UUID ĐẦY ĐỦ theo config "
              f"topology, đừng gõ tay/prefix); NLM có thể chập chờn sau mutation lớn (đã retry 5s/15s) — chờ "
              f"≥60s thử lại; lane thay thế: MCP source_add + `tl register` nối sổ.",
              file=sys.stderr, flush=True)
        return out
    out["route"] = {"corpus_read": "corpus_read", "defer": "deferred", "stale_cache": "stale_cache",
                    "unverified": "unverified"}.get(mode, "none")
    _nlm_fallback_banner(cmd_name, why, out["route"])
    return out


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
        # r208c 3.1: schema v2 — BỎ `est_remaining_min` (bịa: 60 − tuổi), THÊM `rotation_token_*` + `fix`.
        out = {"ok": bool(rep.get("alive")), "schema": "nlm_auth_status.v2", "notebook_probed": nb,
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


def _nlm_links_md(rows: list, nb: str, *, title: str = "Bảng tay nạp NotebookLM") -> str:
    """F5 van 1 (r192, PURE): dựng BẢNG TAY markdown — link bấm-được từng nguồn (QT-1) + link notebook đích
    + hẹn `nlm-reconcile` sau khi người dùng nạp xong. Dùng bởi `nlm-links --md-out` và nhánh bảng-tay
    của `ingest-missing` (lô > NLM_BATCH_LINKS_THRESHOLD). r199 (grill 24-07 C1): lô >ngưỡng chia KHỐI
    ≤NLM_BATCH_LINKS_THRESHOLD URL — NLM dễ chết khi dồn lô; mỗi khối tự đủ (link notebook tại header),
    dặn CHỜ khối trước xử lý xong; lô ≤ngưỡng giữ dạng phẳng r192 y hệt."""
    nb_url = f"https://notebooklm.google.com/notebook/{nb}"
    _thr = NLM_BATCH_LINKS_THRESHOLD
    lines = [f"# {title} — {len(rows)} nguồn", "",
             f"Notebook đích: [{nb}]({nb_url})", ""]
    if len(rows) <= _thr:
        lines += ["Mở notebook → Add source → Google Drive (picker chọn được NHIỀU file 1 lần) hoặc dán link:", ""]
        for e in rows:
            lines.append(f"- [{_entry_name(e)}]({_entry_links_url(e)})")
    else:
        _nblk = (len(rows) + _thr - 1) // _thr
        lines += [f"Lô {len(rows)} nguồn → chia {_nblk} khối ≤{_thr} URL (NLM dễ chết khi dồn lô). "
                  "Nạp TỪNG KHỐI: Add source → Google Drive (picker chọn NHIỀU file) hoặc dán link của khối, "
                  "CHỜ NLM nhận xong khối này rồi mới sang khối kế.", ""]
        for _bi in range(_nblk):
            lines.append(f"## Khối {_bi + 1}/{_nblk} — [mở notebook]({nb_url})")
            lines.append("")
            for e in rows[_bi * _thr:(_bi + 1) * _thr]:
                lines.append(f"- [{_entry_name(e)}]({_entry_links_url(e)})")
            lines.append("")
    lines += ["", "Sau khi nạp xong TRÊN UI:", "",
              f"1. `tl nlm-reconcile {nb} --apply`   # bắc cầu registry (exact-title, ownership-guard A2)",
              "2. Scope nền: `tl register --drive-id <id> --corpus true` từng dòng sau khi link.", ""]
    return "\n".join(lines)


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
    # F5 van 1 (r192): --drive-ids = bảng tay cho LÔ CỤ THỂ (caller — vd ingest-missing chuyển tay — đưa
    # danh sách id); lọc trực tiếp trên entries, KHÔNG đòi điều-kiện 'chưa có nlm_source_id' của mặc định.
    _dids91 = [s.strip() for s in str(getattr(a, "drive_ids", "") or "").split(",") if s.strip()]
    if _dids91:
        _by_did91 = {str(_entry_drive_id(e) or ""): e for e in entries}
        rows = [_by_did91[d] for d in _dids91 if d in _by_did91]
        _miss91 = [d for d in _dids91 if d not in _by_did91]
        if _miss91:
            print(f"[tl] ⚠ nlm-links --drive-ids: {len(_miss91)} id không thấy trong manifest (bỏ qua): "
                  f"{_miss91[:5]}", file=sys.stderr)
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
    # F5 van 1 (r192): --md-out = ghi BẢNG TAY markdown (link bấm-được + notebook + hẹn reconcile) ra file
    # sổ trong gói việc — dùng khi lô > NLM_BATCH_LINKS_THRESHOLD chuyển nạp tay.
    _md_out91 = getattr(a, "md_out", None)
    if _md_out91:
        try:
            _p91 = Path(_md_out91)
            _p91.parent.mkdir(parents=True, exist_ok=True)
            _p91.write_text(_nlm_links_md(rows, nb), encoding="utf-8", newline="\n")
            print(f"[tl] nlm-links: bảng tay → {_p91}", file=sys.stderr)
        except Exception as _me91:  # noqa: BLE001
            print(f"[tl] ⚠ nlm-links --md-out lỗi ghi ({_me91}) — dùng stdout/JSON thay.", file=sys.stderr)
            _md_out91 = None
    if getattr(a, "json", False) or getattr(a, "out", None):
        payload = {"ok": True, "schema": "nlm_links.v1", "notebook": nb, "notebook_url": nb_url,
                   "count": len(links), "total_pending": _total, "links": links,
                   **({"hand_sheet": str(_md_out91)} if _md_out91 else {}),
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


def _nlm_remove_presence_verdict(listed_ok: bool, live_ids, sid: str) -> str:
    """v1.36.17 (r279 — va chạm HAI PHIÊN 31-07-2026) PURE: sid còn SỐNG trên notebook TRƯỚC khi gỡ?
    'present' | 'absent' (đã bị gỡ từ trước — nhiều khả năng phiên khác vừa làm) | 'list_failed'.

    VÌ SAO CẦN — bằng chứng đã trả giá: `nlm_cli.source_delete` trả ok cho CẢ sid ĐÃ biến mất và raw
    KHÔNG kèm deleted_count ⇒ `_source_remove_delete_verdict` cho 'deleted' KHỐNG. Ca thật: hai phiên
    cùng gỡ sid 04e51f9c cách nhau 59 GIÂY, phiên sau vẫn in `deleted:1` — sổ ghi nhận công việc mà nó
    không hề làm. `nlm-add` đã có cổng dedup-live đối chiếu LIVE trước khi ghi; đường GỠ thì chưa có
    ⇒ đây là vế đối xứng còn thiếu. Không tin rc/ok — đòi bằng chứng DƯƠNG từ listing vật lý."""
    if not listed_ok:
        return "list_failed"
    return "present" if str(sid) in {str(x) for x in (live_ids or [])} else "absent"


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
    # r296 (P16-F15): điểm DỪNG phải nhận cả Điều có HẬU TỐ CHỮ (7a/7b/7đ — điều được luật sửa đổi CHÈN
    # THÊM). Bản cũ dùng `Điều\s+\d+\b` làm lookahead: ở "Điều 7a" thì `\d+` ăn "7" rồi `\b` đòi ranh giới
    # giữa "7" và "a" — cả hai là ký tự từ nên KHÔNG có ranh giới ⇒ lookahead TRƯỢT ⇒ lát cắt chạy tiếp
    # qua 7a/7b. Đo được: hỏi Điều 7 thì trả về nguyên văn của CẢ 7, 7a và 7b — tức trả nội dung điều KHÁC
    # dưới danh nghĩa điều được hỏi. Với skill mà hợp đồng là "đúng từng chữ", đó là sai lệch NỘI DUNG.
    # ★ Phần NEO (`{dieu}\b`) ĐÚNG và phải GIỮ NGUYÊN: chính `\b` đó chặn "Điều 7" khớp nhầm vào "Điều 7a".
    #   Neo không sai — chỉ điểm dừng sai.
    import re as _re
    m = _re.search(rf"(?mi)^\s*Điều\s+{_re.escape(str(dieu))}\b.*?(?=^\s*Điều\s+\d+[a-zđ]*\b|\Z)", text or "", _re.S)
    return m.group(0).strip() if m else f"[không thấy Điều {dieu}]"

def _split_source_ids(values: list[str] | None, combined: str = "") -> list[str]:
    raw = []
    for val in values or []:
        raw.extend(str(val).split(","))
    if combined:
        raw.extend(str(combined).split(","))
    return _unique_preserve_order([x.strip() for x in raw if x and x.strip()])
