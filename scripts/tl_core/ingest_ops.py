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
    """Legacy Drive-id adapter for the shared ingest-local engine.

    QT-2 remains a pre-plan policy gate, but every accepted source is downloaded,
    validated and content-hashed by ``cmd_ingest_local``.  The legacy command no
    longer owns an independent, weakly verified write path.
    """
    pg = _need_base('preingest_gate')
    gate = None
    # 1) QT-2 nếu là sửa đổi/VBHN/nghi bị thay
    if a.sohieu and (a.amendment or a.vbhn or a.check):
        targets = [t for t in re.split(r"[;,]", a.targets or "") if t.strip()]
        g = _gas()
        gate = pg.decide(g.get("vb_status", q=a.sohieu),
                         [dict(g.get("vb_status", q=t), sohieu=t) for t in targets],
                         is_amendment=a.amendment or pg.is_amendment_name(a.sohieu),
                         is_vbhn=a.vbhn or pg.is_vbhn_name(a.sohieu))
        if gate["decision"] == "SKIP":
            out = {"ok": True, "skipped": True, "step": "qt2_gate", "gate": gate,
                   "note": "QT-2=SKIP; không thực hiện ghi."}
            print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
            return 0
        if gate["decision"] == "REVIEW":
            out = {"ok": False, "step": "qt2_gate", "gate": gate,
                   "error": "QT2_REVIEW_REQUIRED",
                   "note": "Phải giải quyết trạng thái pháp lý trước khi lập/apply plan ingest."}
            print(_json_dumps(out, deterministic=_deterministic_enabled(a)), file=sys.stderr)
            return 2

    # 2) Forward to the one content-addressed implementation.  Keep this
    # adapter intentionally small; advanced switches belong to ingest-local.
    child = dict(vars(a))
    child.update({
        "file": None,
        "drive_id": a.fileId,
        "name": a.ten,
        "auto_plan": True,
        "json": True,
    })
    defaults = {
        "goc": None,
        "hieuluc": None,
        "resume": False,
        "text_file": None,
        "source_quality": "auto",
        "ocr_verified": False,
        "force_cat": False,
        "allow_large": False,
        "large_threshold": None,
        "skip_nlm_preflight": False,
        "skip_live_check": False,
        "nlm_no_wait": False,
        "no_nlm_add": False,
    }
    for key, value in defaults.items():
        child.setdefault(key, value)
    return cmd_ingest_local(argparse.Namespace(**child))


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
    cmd = f'tl ingest-local "{f or tf}" --auto-plan --json'
    if tf:
        cmd += f' --text-file "{tf}"'
    if plan.get("cat"):
        cmd += f" --cat {plan['cat']}"
    plan["dry_run_command"] = cmd
    plan["apply_command_template"] = (
        cmd + " --apply --confirm yes --expected-plan-hash <plan_hash_from_dry_run>"
    )
    plan["hint"] = (
        "SUGGESTION — verify sohieu/cat/tên (`cat-verify`/`header-verify`), chạy dry-run, "
        "rồi gắn đúng plan_hash vào lệnh apply."
    )
    print(json.dumps({"ok": plan.get("ok", True), **plan}, ensure_ascii=False, indent=2))
    return 0 if plan.get("ok", True) else 2


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
    # v1.34.49: +row_kind vào gate-cols (superset — link shard overflow ghi row_kind, trước đây gate thiếu cột này)
    _ok_gate, _pfv = _apply_gate(a, write_cols="nlm_source_id,nlm_notebook_id,nlm_status,row_kind")
    if not _ok_gate:
        return 2
    run_id = _apply_journal_start("ingest-missing", {"snapshot": snapshot_ts, "profile": _active_profile(), "targets": len(targets)})
    try:
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    except (Exception, SystemExit):
        pass
    try:
        nc = _imp("nlm_cli")
    except Exception as e:  # noqa: BLE001
        print(f"[tl] ingest-missing --apply: nlm_cli lỗi ({e}) — DỪNG (an toàn).", file=sys.stderr); return 2
    # v1.34.49 (F-02/D3 + F-05/D4 + F-03 write-path — grill 2026-07-15): TOPOLOGY TOÀN CỤC thay cặp
    # base+1-overflow. Plan per-item theo live-count MỌI shard enabled (đọc FAIL-CLOSED + self-heal load_creds
    # 1 lần — {ok:False} KHÔNG BAO GIỜ thành 0/phantom-room); shard đầy giữa run (drift) → FAILOVER shard kế
    # TRONG CÙNG RUN với chính drive_id (KHÔNG upload lại); cạn mọi shard → partial TRUNG THỰC (ok=false +
    # remaining + resume_command + rc=2 — hết 'sai mà báo thành công' F-02). BẤT BIẾN GIỮ: không tạo notebook.
    topo = _resolve_shard_topology(entries, base_nb, profile=_active_profile())
    if not topo.get("ok"):
        print(json.dumps({"ok": False, "error": topo.get("error"), "gate": "ingest-missing",
                          "note": "Topology config conflict → DỪNG fail-closed (D5). Sửa shards[]/alias trong config."},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    shard_plan = [s for s in (topo.get("shards") or []) if s.get("enabled")]
    if base_nb and base_nb not in [s.get("id") for s in shard_plan]:
        shard_plan.insert(0, {"id": base_nb, "role": "primary", "capacity": _shard_capacity_default(),
                              "enabled": True, "priority": 0})
    order = [s["id"] for s in shard_plan]
    _heal = {"healed": False}
    rooms: dict[str, int] = {}
    for s in shard_plan:
        _cnt, _okc, _errc = _live_source_count(nc, s["id"], _heal)
        if not _okc:
            print(json.dumps({"ok": False, "error": "LIVE_READ_FAILED", "notebook": s["id"], "detail": _errc,
                              "note": "KHÔNG đếm được slot LIVE (auth/mạng) — DỪNG TRƯỚC mọi side-effect "
                                      "(F-05 fail-closed: {ok:false} KHÔNG coi là 0 nguồn/phantom-room). "
                                      "Sửa `nlm login` rồi chạy lại."}, ensure_ascii=False, indent=2),
                  file=sys.stderr)
            return 2
        rooms[s["id"]] = max(0, int(s.get("capacity") or NLM_SLOT_CAP) - int(_cnt))
    route = "base" if rooms.get(base_nb, 0) > 0 else ("overflow" if any(
        rooms.get(x, 0) > 0 for x in order if x != base_nb) else "blocked")
    reason = "topology multi-shard v1.34.49 (plan theo live-room từng shard)"
    if _apply_ing:   # HEARTBEAT: log timeout 43s → in ROOMS ngay khi biết để thấy đang chạy đúng.
        print("[tl]   ✓ slot LIVE: " + ", ".join(f"{x[:12]}…room={rooms[x]}" for x in order)
              + f" → route={route} — tiếp: dedup LIVE…", file=sys.stderr, flush=True)
    if route == "blocked":
        _resume0 = ("tl" + ((" --profile " + _active_profile()) if _active_profile() != DEFAULT_PROFILE else "")
                    + f" ingest-missing --apply --limit {lim}")
        print(json.dumps({"ok": False, "blocked": True, "partial": True, "remaining": len(targets),
                          "reason": "ALL_SHARDS_FULL_ASK_USER (mọi shard topology đầy — KHÔNG auto-create notebook)",
                          "rooms": rooms, "resume_command": _resume0}, ensure_ascii=False, indent=2))
        return 2    # v1.34.49: hết rc=0 'gate có chủ đích' — orchestrator phải THẤY backlog chưa xử lý (F-02)
    target_nb = base_nb if route == "base" else next((x for x in order if rooms.get(x, 0) > 0), base_nb)
    # S13: đối chiếu nguồn LIVE → tách target ĐÃ có nguồn (LINK/reconcile) khỏi target cần add.
    # v1.34.49 (F-04 read-side): dedup trên UNION MỌI shard topology (trước: chỉ notebook đích → nguồn đã nằm
    # shard khác vẫn bị add trùng sang shard mới). Reservation xuyên host (ghi) = đợt 50 GAS 2.21.2l.
    # (review#3) KHÔNG liệt kê được LIVE = KHÔNG xác minh trùng → DỪNG (an toàn) trừ khi --skip-live-check (checkpoint vẫn chống trùng trong-phiên).
    skip_live = getattr(a, "skip_live_check", False)
    to_add, already_live, unresolved = targets, [], 0
    _live, _live_ok = {}, True
    _live_union, _live_shard_by_sid = [], {}
    for _nbq in order:
        try:
            _lv = nc.source_list(_nbq, skip_freshness=True, drive=True)
        except Exception as _le:  # noqa: BLE001
            _lv = {"ok": False, "error": str(_le)}
        if not _lv.get("ok"):
            _live, _live_ok = _lv, False
            break
        for _s in (_lv.get("sources") or []):
            _live_union.append(_s)
            if _s.get("id"):
                _live_shard_by_sid[str(_s.get("id"))] = _nbq
    if _live_ok:
        to_add, already_live, unresolved = _ingest_missing_dedup_live(targets, _live_union)
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
    # v1.34.49: ckpt key theo BASE/primary (run nay đa-shard, không còn 1 notebook đích duy nhất); vẫn không
    # collide đa-profile (base mỗi profile khác nhau). MERGE READ-ONLY ckpt legacy key-theo-shard (run cũ chọn
    # target_nb=overflow) để không mất trạng thái done/linked; ghi mới CHỈ vào file base.
    _ck_key = re.sub(r"[^A-Za-z0-9_-]", "", str(base_nb))[:64] or "base"    # (review#4) checkpoint không collide đa-profile
    ckpt = Path(os.path.expanduser("~")) / f".tl_ingest_missing_ckpt_{_ck_key}.json"
    _ckf = _ingest_ckpt_load_full(ckpt)   # v1.29.1: {done, pending, linked, fails} — WAL-hoá (xử log LIVE 2026-07-02)
    done, pending, linked, fails = _ckf["done"], _ckf["pending"], _ckf["linked"], _ckf["fails"]
    for _nbq in order:
        _k2 = re.sub(r"[^A-Za-z0-9_-]", "", str(_nbq))[:64]
        if not _k2 or _k2 == _ck_key:
            continue
        _p2 = Path(os.path.expanduser("~")) / f".tl_ingest_missing_ckpt_{_k2}.json"
        if _p2.exists():
            try:
                _c2 = _ingest_ckpt_load_full(_p2)
                for _fld, _dst in (("done", done), ("pending", pending), ("linked", linked), ("fails", fails)):
                    for _k3, _v3 in (_c2.get(_fld) or {}).items():
                        _dst.setdefault(_k3, _v3)
            except Exception:  # noqa: BLE001 — merge best-effort; ckpt hỏng không chặn run
                pass

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
            # v1.34.49: fresh-verify trên UNION mọi shard (run trước có thể add dở vào shard KHÁC lựa chọn nay).
            _fresh_union = []
            for _nbq in order:
                _fresh = nc.source_list(_nbq, skip_freshness=False, drive=True)
                if not _fresh.get("ok"):
                    raise RuntimeError(str(_fresh.get("error") or "source_list !ok"))
                for _s in (_fresh.get("sources") or []):
                    _fresh_union.append(_s)
                    if _s.get("id"):
                        _live_shard_by_sid.setdefault(str(_s.get("id")), _nbq)
            _ta2, _al2, _u2 = _ingest_missing_dedup_live(
                [e for e in to_add if _entry_drive_id(e) in _pend_dids], _fresh_union)
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
    # v1.34.54 (B1/Q3=a — grill 2026-07-15): NGƯỠNG BATCH-LINK — (cookie chết ∨ pending > NLM_BATCH_LINKS_THRESHOLD)
    # → KHÔNG add API từng file (11-19s/file + rủi ro chết giữa lô ~1h cookie) mà in DANH SÁCH LINK để dán batch
    # vào UI notebook (1 lần), sau đó `tl nlm-reconcile --apply` link registry. Đường API cũ: --force-api-add.
    if to_add and not getattr(a, "force_api_add", False):
        _thr_over = len(to_add) > NLM_BATCH_LINKS_THRESHOLD
        _rep54 = _nlm_preflight_report(target_nb, probe=not _thr_over)   # >ngưỡng thì khỏi tốn probe
        # v1.34.60 (E3 control-surface, ADR-5): nhánh cookie-chết→BATCH_LINKS chịu điều khiển fallback
        # (--no-fallback/TL_NLM_FALLBACK=0 → không tự rẽ, đi tiếp đường API rồi fail-closed như trước
        # v1.34.54); ngưỡng pending>2 là tối ưu batch bình thường, KHÔNG phải fallback — giữ nguyên.
        _dead54 = (_rep54.get("alive") is False) and _nlm_fallback_enabled(a)
        if _thr_over or _dead54:
            _why54 = (f"pending={len(to_add)} > {NLM_BATCH_LINKS_THRESHOLD}" if _thr_over
                      else f"cookie NLM chết ({_rep54.get('why') or '?'})")
            _links54 = [_entry_links_url(e) for e in to_add]
            _nb_url54 = f"https://notebooklm.google.com/notebook/{target_nb}"
            print(f"[tl] ingest-missing → BATCH-LINK ({_why54}): KHÔNG add API. Dán {len(_links54)} link vào "
                  f"Add source → Websites của {_nb_url54} rồi chạy `tl nlm-reconcile {target_nb} --apply`. "
                  f"(Ép add API: --force-api-add; danh sách link thuần: `tl nlm-links`)", file=sys.stderr, flush=True)
            for _w54 in (_rep54.get("warn") or []):
                print(f"[tl]   ⚠ {_w54}", file=sys.stderr)
            print(json.dumps({"ok": True, "mode": "BATCH_LINKS", "reason": _why54, "notebook": target_nb,
                              "notebook_url": _nb_url54, "count": len(_links54), "links": _links54,
                              "note": "Chưa add gì qua API — dán links vào UI (batch), xong reconcile --apply "
                                      "để link registry (ownership-guard A2). Base đầy → dán vào shard overflow "
                                      "rồi reconcile --all-notebooks (DRY) xem hướng dẫn per-notebook."},
                             ensure_ascii=False, indent=2))
            return 0
    # v1.34.52 (F-04/D9 — grill GAS 2.21.2l 2026-07-15): ACQUIRE claim identity_hash cho TOÀN BỘ to_add
    # TRƯỚC vòng lặp add — chặn 2 host cùng add 1 identity trong cửa sổ race giữa preflight-dedup (xong ở
    # trên) và source_add thật (sắp chạy). Optional server-side (D8): webapp cũ (<2.21.2l) không có action
    # này → lỗi gọi được BẮT và DỪNG an toàn (KHÔNG âm thầm bỏ qua bảo vệ — client MỚI bắt buộc có claim).
    # Đơn giản hoá CÓ CHỦ ĐÍCH (ghi rõ, không giấu): KHÔNG release tường minh khi item fail — dựa TTL 5' tự
    # heal (đủ AN TOÀN vì claim che đúng cửa sổ add, không phải toàn bộ vòng đời item).
    from tl_core.ingest_contract import identity_hash_for_drive_source
    _profile_now = _active_profile()
    _hash_by_did: dict[str, str] = {}
    for _e0c in to_add:
        _did0c = _entry_drive_id(_e0c)
        if _did0c:
            _hash_by_did[_did0c] = identity_hash_for_drive_source(
                _did0c, target_scope=target_nb, canonical_name=_entry_name(_e0c), profile=_profile_now)
    _hash_to_did = {v: k for k, v in _hash_by_did.items()}
    _committed_candidates: list[tuple] = []   # [(identity_hash, drive_id, source_id)] — commit theo lô sau vòng lặp
    if _hash_by_did:
        try:
            _cl = g.get("ingest_claim", keys=json.dumps(list(_hash_by_did.values())),
                        run_id=run_id, drive_ids=json.dumps(list(_hash_by_did.keys())))
        except Exception as _cle:  # noqa: BLE001
            _cl = {"ok": False, "error": str(_cle)}
        if not _cl.get("ok"):
            print(json.dumps({"ok": False, "error": "INGEST_CLAIM_FAILED", "detail": _cl.get("error"),
                              "note": "Không xin được claim xuyên host (F-04, webapp cần ≥2.21.2l) — DỪNG "
                                      "an toàn thay vì add mù không bảo vệ race."}, ensure_ascii=False, indent=2),
                  file=sys.stderr)
            return 2
        _denied_dids = set()
        for _rr in (_cl.get("results") or []):
            if not _rr.get("granted"):
                _dd = _hash_to_did.get(_rr.get("identity_hash"))
                if _dd:
                    _denied_dids.add(_dd)
                    results.append({"drive_id": _dd, "ok": False, "skipped": "CLAIMED_ELSEWHERE",
                                    "reason": _rr.get("reason")})
        if _denied_dids:
            to_add = [e for e in to_add if _entry_drive_id(e) not in _denied_dids]
            print(f"[tl]   ⚠ {len(_denied_dids)} mục đang bị host khác giữ claim (F-04) → SKIP trong run này "
                  f"(không phải lỗi — thử lại sau khi claim hết hạn/host kia xong).", file=sys.stderr, flush=True)
    # v1.34.49 (F-06): row_kind SUY TỪ TOPOLOGY per-notebook (own→không ghi, overflow→ghi 'overflow'); kind
    # bảo hộ (ref/thuong) trên dòng sẵn có KHÔNG BAO GIỜ bị clobber. cols per-link theo item.
    _rk_by_did = {}
    for _e0 in entries or []:
        _d0 = str(_e0.get("drive_id") or _e0.get("gdoc_id") or "")
        if _d0:
            _rk_by_did[_d0] = str(_e0.get("row_kind") or "").strip().lower()

    def _reg_link(did, sid, nb_link=None) -> bool:
        # (Pha 1) qua `_journaled_reg_write`: journal intent{before}+commit{verify} + validate cột + patched≥1. reg_bulk có
        # thể lỗi (GAS down/quota) / patched=0 (dòng chưa index) → KHÔNG crash batch (source_id ĐÃ ở checkpoint → reconcile).
        nonlocal reg_fail_n
        _nb = (nb_link or _live_shard_by_sid.get(str(sid)) or target_nb)
        item = {"drive_id": did, "nlm_source_id": sid, "nlm_notebook_id": _nb, "nlm_status": "pushed"}
        _cols_l = "nlm_source_id,nlm_notebook_id,nlm_status"
        _before = {"nlm_source_id": "", "nlm_status": ""}
        if (_shard_row_kind(_nb, topo) == "overflow") and (_rk_by_did.get(did) not in _ROW_KIND_PROTECTED):
            item["row_kind"] = "overflow"
            _cols_l += ",row_kind"
            _before["row_kind"] = _rk_by_did.get(did, "")
        v = _journaled_reg_write(run_id, g, [item], _cols_l, before_by_key={did: _before})
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
        results.append({"drive_id": did, "ok": True, "linked": True, "source_id": sid,
                        "notebook": _live_shard_by_sid.get(str(sid)) or target_nb})
        print(f"  [link] {(_entry_sohieu(e) or '(?)')[:18]:18s} đã có LIVE → reconcile (không tạo trùng)", file=sys.stderr, flush=True)
    if al_skip_n:
        print(f"  [skip] {al_skip_n} mục ĐÃ link verified trước đó (ckpt) → bỏ relink lặp (GAS cache 600s; ép: --relink).",
              file=sys.stderr, flush=True)
    # (2) Nạp mới per-item. v1.29.1 WAL: pending ghi TRƯỚC source_add (subprocess wait tới 630s — client-timeout giết ở
    # đây là gốc trùng VBHN_67); done ghi NGAY SAU; fails đếm FAIL liên tiếp (≥3 → SKIP đỡ đốt batch, --retry-failed ép).
    # v1.34.49 (F-02/D3): ALLOCATOR đa-shard — con trỏ shard chạy theo `order`, hết chỗ/drift-FULL → shard kế
    # TRONG CÙNG RUN (chính drive_id, KHÔNG upload lại); cạn mọi shard → phần còn lại vào `remaining` (partial).
    _total = len(to_add)
    pf_skip_n = 0
    remaining_entries: list = []
    _shard_used: dict[str, int] = {}
    _sh_i = 0                    # con trỏ shard hiện hành trong `order`

    def _next_shard_with_room(_start: int) -> int:
        for _j in range(_start, len(order)):
            if rooms.get(order[_j], 0) > 0:
                return _j
        return -1

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
        _sh_i = _next_shard_with_room(_sh_i if _sh_i >= 0 else 0)
        if _sh_i < 0:
            remaining_entries = to_add[_i - 1:]
            print(f"  ⚠ HẾT CHỖ mọi shard topology giữa chừng → DỪNG partial ({len(remaining_entries)} mục còn lại; "
                  f"KHÔNG tạo notebook — duyệt shard mới rồi resume).", file=sys.stderr)
            break
        _cur_nb = order[_sh_i]
        print(f"  [{_i}/{_total}] + {(_entry_sohieu(e) or '(?)')[:18]:18s} {_entry_name(e)[:40]} → {_cur_nb[:12]}… …", file=sys.stderr, flush=True)
        pending[did] = _entry_name(e)[:120]   # WAL-pending TRƯỚC add — timeout giữa add → run sau fresh-verify, không add mù
        _ck_flush()
        r = nc.source_add(_cur_nb, drive_id=did, title=_entry_name(e)[:120], wait=True)
        while (not r.get("ok")) and _nlm_add_capacity_error(r.get("error")):
            # drift: shard báo ĐẦY dù plan còn chỗ (nguồn khác chen giữa) → tin SERVER, đóng shard, thử shard kế
            # với CHÍNH drive_id (ingest-missing không upload gì — file đã trên Drive). KHÔNG đếm FAIL.
            rooms[_cur_nb] = 0
            _j2 = _next_shard_with_room(_sh_i)
            if _j2 < 0:
                break
            _sh_i = _j2; _cur_nb = order[_sh_i]
            print(f"        ↪ shard đầy (drift) → reroute {_cur_nb[:12]}… (cùng run, không upload lại)", file=sys.stderr, flush=True)
            r = nc.source_add(_cur_nb, drive_id=did, title=_entry_name(e)[:120], wait=True)
        if not r.get("ok"):
            pending.pop(did, None)            # add fail THẬT (CLI trả lỗi) = không tạo source → bỏ dấu pending
            if _nlm_add_capacity_error(r.get("error")):
                _ck_flush()
                remaining_entries = to_add[_i - 1:]
                print(f"  ⚠ MỌI shard đầy (server xác nhận) → DỪNG partial ({len(remaining_entries)} mục còn lại).",
                      file=sys.stderr)
                break
            fail_n += 1
            fails[did] = int(fails.get(did) or 0) + 1
            _ck_flush()
            results.append({"drive_id": did, "ok": False, "error": r.get("error"), "fails": fails[did]})
            print(f"        FAIL ({fails[did]}×): {r.get('error')}", file=sys.stderr, flush=True); continue
        sid = r.get("source_id")
        done[did] = sid   # checkpoint NGAY sau add (trước reg_bulk) → ngắt sau đây, lần sau đối chiếu LIVE/ckpt sẽ LINK không add lại
        pending.pop(did, None)
        fails.pop(did, None)
        _ck_flush()
        _live_shard_by_sid[str(sid)] = _cur_nb
        _reg_link(did, sid, _cur_nb)
        _ih0 = _hash_by_did.get(did)
        if _ih0:
            _committed_candidates.append((_ih0, did, sid))
        ok_n += 1
        rooms[_cur_nb] = max(0, rooms.get(_cur_nb, 0) - 1)
        _shard_used[_cur_nb] = _shard_used.get(_cur_nb, 0) + 1
        results.append({"drive_id": did, "ok": True, "source_id": sid, "notebook": _cur_nb})
        print(f"        OK → {sid}", file=sys.stderr, flush=True)
    # v1.34.52 (F-08/D3/D7 — grill GAS 2.21.2l): COMMIT claim theo lô (hằng số batch=10) qua `reg_get_bulk`
    # — 1 round-trip vừa readback xác minh registry vừa đóng claim (gộp, KHÔNG round-trip riêng). Best-effort:
    # lô lỗi/claim không commit được → tự heal qua TTL 5' (KHÔNG chặn kết quả run, khớp dung sai reg_fail_n
    # đã có — reconcile sau vẫn thấy nlm_source_id đúng dù claim GAS chưa kịp đóng).
    _CLAIM_COMMIT_BATCH = 10   # D7: hằng số, không config env
    if _committed_candidates:
        for _bi in range(0, len(_committed_candidates), _CLAIM_COMMIT_BATCH):
            _chunk = _committed_candidates[_bi:_bi + _CLAIM_COMMIT_BATCH]
            _commit_claims = [{"identity_hash": ih, "source_id": sid, "run_id": run_id} for ih, _did, sid in _chunk]
            try:
                _rgb = g.get("reg_get_bulk", keys=json.dumps([did for _ih, did, _sid in _chunk]),
                            key_field="drive_id", commit_claims=json.dumps(_commit_claims))
            except Exception as _rgbe:  # noqa: BLE001
                _rgb = {"ok": False, "error": str(_rgbe)}
            if not _rgb.get("ok") or (_rgb.get("commit_failed")):
                print(f"[tl]   ⚠ claim commit chưa xác nhận cho {len(_rgb.get('commit_failed') or _chunk)} mục "
                      f"({_rgb.get('error') or 'commit_failed'}) — tự hết hạn sau 5' (F-04 TTL), không chặn kết quả.",
                      file=sys.stderr, flush=True)
    _partial = bool(remaining_entries)
    _resume_cmd = ("tl" + ((" --profile " + _active_profile()) if _active_profile() != DEFAULT_PROFILE else "")
                   + f" ingest-missing --apply --limit {lim}") if _partial else None
    _ok_all = (not _partial) and fail_n == 0 and reg_fail_n == 0
    _journal_append(run_id, {"t": "run_end", "ok": _ok_all, "partial": _partial, "remaining": len(remaining_entries),
                             "counts": {"OK": ok_n, "LINKED": link_n, "SKIP": skip_n, "FAIL": fail_n, "REG_WRITE_FAIL": reg_fail_n,
                                        "ALREADY_LINKED": al_skip_n, "PUSH_FAIL_SKIPPED": pf_skip_n}})
    print(json.dumps({"ok": _ok_all, "partial": _partial, "remaining": len(remaining_entries),
                      "remaining_targets": [{"drive_id": _entry_drive_id(x), "sohieu": _entry_sohieu(x),
                                             "name": _entry_name(x)[:60]} for x in remaining_entries[:20]],
                      "resume_command": _resume_cmd,
                      "route": ("multi" if len(_shard_used) > 1 else route), "notebook": target_nb,
                      "shards_used": [{"notebook_id": k, "added": v} for k, v in _shard_used.items()],
                      "reason": reason, "manifest_snapshot": snapshot_ts, "journal": run_id,
                      "OK": ok_n, "LINKED": link_n, "SKIP": skip_n, "FAIL": fail_n, "REG_WRITE_FAIL": reg_fail_n,
                      "ALREADY_LINKED": al_skip_n, "PUSH_FAIL_SKIPPED": pf_skip_n,
                      "unresolved_live": unresolved, "skipped_no_sohieu": len(_skip_note), "results": results}, ensure_ascii=False, indent=2))
    _hint = " ⚠ REG_WRITE_FAIL>0 → chạy `tl nlm-reconcile <nb> --apply` để khớp registry↔NLM." if reg_fail_n else ""
    _hint += f" ⚠ PARTIAL: còn {len(remaining_entries)} mục — duyệt shard mới rồi `{_resume_cmd}`." if _partial else ""
    print(f"[tl] ingest-missing: OK={ok_n} LINKED={link_n} SKIP={skip_n} FAIL={fail_n} REG_WRITE_FAIL={reg_fail_n} "
          f"no_sohieu={len(_skip_note)} partial={_partial} → shards={list(_shard_used) or [target_nb]} (route={route}). "
          f"journal={run_id}.{_hint} MANIFEST_STALE: `tl manifest` rồi `tl boot --refresh`.", file=sys.stderr)
    if _partial:
        return 2    # partial = KHÔNG phải success hoàn chỉnh (D3) — orchestrator phải thấy backlog còn
    return 0 if (fail_n == 0 and reg_fail_n == 0) else 1


def _ingest_perf_hint(nlm_no_wait: bool, no_nlm_add: bool):
    """PURE (v1.34.73 — mổ xẻ 30' nạp 3 file 2026-07-19, journal đo ~260s/file): chờ NLM settle mặc định
    ăn ≈NỬA thời gian mỗi ingest. Nạp LÔ ≥2 file → nhắc đường nhanh ngay trong DRY plan; chạy đơn lẻ giữ
    mặc định verify-then-link (an toàn v1.34.56). Trả None khi đã dùng cờ nhanh (không lải nhải)."""
    if nlm_no_wait or no_nlm_add:
        return None
    return ("PERF nạp LÔ ≥2 file: thêm --nlm-no-wait (−~50%/file; 3 lệnh chạy SONG SONG được) + "
            "`tl nlm-reconcile <notebook> --apply` MỘT lần cuối lô; lô lớn: --no-nlm-add (dừng sau "
            "Drive+registry) rồi nlm-links batch + reconcile. Đơn lẻ: giữ mặc định (verify-then-link).")


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
    overflow = (os.environ.get("TL_OVERFLOW_NOTEBOOK_ID") or "").strip()
    # v1.34.47 (Mod2): guard placeholder/id-không-hợp-lệ + discovery fallback (ĐỐI XỨNG 3 site kia:
    # preflight/ingest-missing/overflow-resolve). Trước đây chỉ `if not overflow`, nên config để literal
    # 'TL_OVERFLOW_NOTEBOOK_ID' bị đẩy thẳng làm target → LIVE_SOURCE_LIST_FAILED/'nlm login' oan SAU side-effect.
    if (not overflow) or overflow == "TL_OVERFLOW_NOTEBOOK_ID" or "-" not in overflow:
        try:
            overflow = _discover_overflow_from_registry(_manifest_entries(refresh=False), base)
        except Exception:  # noqa: BLE001
            overflow = ""
    if not overflow:
        return base, {"note": "không cấu hình/không phát hiện overflow → base"}
    params = {"notebookId": base, "overflowNotebookId": overflow, "normative": "true"}
    if sohieu: params["soHieu"] = sohieu
    else: params["name"] = name
    pf = g.get("nlm_preflight", **params)
    slots = pf.get("slots") or {}
    if not slots.get("full"):
        # base còn chỗ → base (giữ nhanh đường thường; KHÔNG gọi nlm-get overflow trừ khi base đầy)
        return base, {"decision": pf.get("decision"), "slots_full": False,
                      "used": slots.get("used"), "cap": slots.get("cap")}
    # v1.34.47 (M1 fix): base ĐẦY → tính overflow_room LIVE fail-closed (KHỚP batch `ingest-missing`); both-full
    # → 'blocked' để caller DỪNG TRƯỚC mọi side-effect (KHÔNG auto-create notebook — ADR).
    # v1.34.49 (F-03 write + F-05): duyệt MỌI shard overflow topology theo thứ tự (không chỉ 1 overflow đơn);
    # đọc slot CHECKED + self-heal 1 lần — auth-fail KHÔNG thành phantom-room.
    try:
        nc = _imp("nlm_cli")
    except Exception as e:  # noqa: BLE001
        return base, {"blocked": True, "overflow_shard": overflow,
                      "reason": f"OVERFLOW_ROOM_UNKNOWN: nlm_cli lỗi ({e}) — DỪNG an toàn."}
    try:
        _ent_t = _manifest_entries(refresh=False)
    except Exception:  # noqa: BLE001
        _ent_t = []
    _topo_t = _resolve_shard_topology(_ent_t, base)
    if not _topo_t.get("ok"):
        return base, {"blocked": True, "overflow_shard": overflow,
                      "reason": f"{_topo_t.get('error')} — DỪNG fail-closed (D5)."}
    _cands_t = [s for s in (_topo_t.get("shards") or []) if s.get("enabled") and s.get("id") != base]
    if overflow and overflow not in [s.get("id") for s in _cands_t]:
        _cands_t.append({"id": overflow, "capacity": _shard_capacity_default()})   # overflow đơn chưa vào topology (bootstrap)
    _heal_t = {"healed": False}
    for _s_t in _cands_t:
        _cnt_t, _ok_t, _err_t = _live_source_count(nc, _s_t["id"], _heal_t)
        if not _ok_t:
            return base, {"blocked": True, "overflow_shard": _s_t["id"],
                          "reason": f"OVERFLOW_ROOM_UNKNOWN: base đầy, không đếm được slot shard {str(_s_t['id'])[:12]}… "
                                    f"({_err_t}) — DỪNG an toàn (F-05: KHÔNG coi là 0 nguồn)."}
        _room_t = int(_s_t.get("capacity") or NLM_SLOT_CAP) - int(_cnt_t)
        if _room_t > 0:
            return _s_t["id"], {"decision": pf.get("decision"), "slots_full": True, "route": "overflow",
                                "overflow_shard": _s_t["id"], "overflow_room": _room_t}
    return base, {"blocked": True, "overflow_shard": overflow,
                  "reason": "ALL_SHARDS_FULL: base + mọi shard overflow topology đầy → HỎI người dùng duyệt shard mới (KHÔNG auto-create)"}


def _profile_source_quality(path: str, explicit: str = "auto") -> str:
    q = (explicit or "auto").strip().lower()
    if q in ("digital", "ocr"):
        return q
    ext = Path(path or "").suffix.lower()
    return "ocr" if ext in {".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff"} else "digital"


_PDF_BROKEN_FONT_WARN = ("PDF_TEXT_LAYER_BROKEN_FONT: text-layer mất dấu (density<0.005) — Google-convert "
                         "thường xử được; apply verify bằng text GDoc sau convert; KHÔNG vội OCR")


def _probe_pdf_quality(path: str) -> dict:
    """v1.34.58 (C-#9 — Q8=a): probe PDF đo MẬT ĐỘ DẤU tiếng Việt trên text-layer (tái dùng ngưỡng 0.005
    + letters>500 của LOW_VIETNAMESE_MARK_DENSITY trong ocr.py). Text ≥200 chars nhưng MẤT DẤU (font hỏng/
    CID không map — ca 7 phụ lục CPTPP pdftotext ra text không dấu) → broken_font=True + text RỖNG (KHÔNG
    đem text hỏng đi phân loại; quyết định corpus DỜI sang apply: text GDoc sau convert). <200 chars →
    broken_font=False, text rỗng (PDF scan thật — giữ đường OCR cũ). Trả {text, source, broken_font};
    hàm cũ `_profile_read_probe_text` giữ nguyên chữ ký cho các đuôi khác."""
    try:
        _txt, _ = _read_local_text_for_analysis(Path(path))
    except Exception:  # noqa: BLE001 — pdftotext lỗi → như probe rỗng (đường cũ)
        _txt = ""
    if len(_txt or "") < 200:
        return {"text": "", "source": "", "broken_font": False}
    _m = _text_quality_metrics(_txt)
    if _m["vietnamese_mark_density"] < 0.005 and _m["letters"] > 500:
        return {"text": "", "source": "", "broken_font": True}
    return {"text": _txt, "source": f"{path}#pdf-text-layer", "broken_font": False}


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
    if ext == ".pdf":
        # v1.34.54 (C6): probe dùng CHUNG extractor với ocr-run (pdftotext, ngưỡng ≥200 chars).
        # v1.34.58 (C-#9): qua _probe_pdf_quality — text-layer MẤT DẤU (broken_font) trả probe RỖNG
        # (không phân loại trên text hỏng; caller cần flag thì gọi _probe_pdf_quality trực tiếp).
        _q9 = _probe_pdf_quality(path)
        if _q9["text"]:
            return _q9["text"], _q9["source"]
    return "", ""


def _sohieu_from_title_zone(zone: str, strict_letterhead: bool = False) -> str:
    """(v1.34.6 #1 — log phiên 2026-07-09): số hiệu của CHÍNH tài liệu chỉ nằm ở VÙNG TIÊU ĐỀ trên DÒNG NGẮN
    kiểu letterhead ('Số: 41/2024/QH15', 'Luật số: …' ≤80 ký tự) — ƯU TIÊN dòng có 'Số:' đứng trước. Số hiệu
    trong CÂU VĂN DÀI là TRÍCH DẪN văn bản khác (báo cáo/tài liệu thường nhắc luật) → BỎ. Trước đây quét cả
    16k ký tự đầu nên báo cáo nhắc 'Luật số 41/2024/QH15' bị gán loai=Luật + sohieu=41/2024/QH15."""
    # v1.34.41 B.2 GĐ2 (harness file thật QĐ 383 bắt): pre-text 'Số' phải là DÒNG LETTERHEAD THUẦN — fullmatch
    # '[<loại>] số[:.]' — check ends-with cũ dính trích dẫn NGẮN kết bằng 'số' ('- Căn cứ Luật Lưu trữ số
    # 33/2024/QH15, ngày…' ≤80 ký tự cướp sohieu của chính văn bản). Letterhead thật chỉ có các dạng
    # 'Số:', 'Luật số:', 'Bộ luật số:', 'Nghị quyết/Nghị định/Pháp lệnh/Thông tư/Quyết định/Lệnh số:'.
    _LETTERHEAD_SO = r"\s*(?:(?:bo\s+luat|luat|nghi\s+quyet|nghi\s+dinh|phap\s+lenh|thong\s+tu|quyet\s+dinh|lenh)\s+)?so\s*[:.]?\s*"
    best = ""
    for _c in _RAW_SOHIEU_RE.finditer(zone or ""):
        _ls = zone.rfind("\n", 0, _c.start()) + 1
        _le = zone.find("\n", _c.end())
        _le = len(zone) if _le < 0 else _le
        if _le - _ls > 80:
            continue                                   # dòng dài = văn xuôi → trích dẫn, không phải letterhead
        _pre = _strip_accents(zone[_ls:_c.start()]).lower()
        if re.fullmatch(_LETTERHEAD_SO, _pre):
            return _c.group(0)                          # 'Số:' letterhead thuần — chắc chắn nhất
        best = best or _c.group(0)
    # (grill D1): số KHÔNG-NĂM (Đảng NN-XX/CQ, hành chính NN/XX-CQ) — CHỈ dòng letterhead thuần 'Số …'
    # (fullmatch, không ends-with — 'theo Chỉ thị số 04-CT/TW.' câu văn ngắn cũng kết bằng 'số', r103 negative).
    # Ưu tiên TRÊN `best`: letterhead-có-Số thắng số-năm-trôi-nổi (ca QĐ 383: 'Số 383-QĐ/TW' vs '33/2024/QH15' thân).
    for _c in _SOHIEU_NOYEAR_RE.finditer(zone or ""):
        _ls = zone.rfind("\n", 0, _c.start()) + 1
        _le = zone.find("\n", _c.end())
        _le = len(zone) if _le < 0 else _le
        if _le - _ls > 80:
            continue
        _pre = _strip_accents(zone[_ls:_c.start()]).lower()
        if re.fullmatch(r"\s*so\s*[:.]?\s*", _pre):
            return _c.group(0)
    # r179 T4: strict_letterhead — CHỈ nhận số trên DÒNG LETTERHEAD THUẦN (2 nhánh fullmatch trên), KHÔNG
    # best-fallback (số ngắn-dòng không tiền tố 'Số' = trích dẫn tiềm năng). Dùng cho bằng-chứng-official
    # của draft-tier: veto marker yếu đòi số hiệu CHẮC CHẮN của chính văn bản, không phải số trôi nổi.
    return "" if strict_letterhead else best


def _draft_banner_line(zone: str) -> bool:
    """r179 T4 (PURE): banner «DỰ THẢO» ĐỨNG ĐẦU DÒNG RIÊNG trong vùng tiêu đề (nhận hậu tố 'ngày…'/'lần N'),
    sau khi bỏ artifact toạ độ docx ('-44005514605Dự thảo…', '00Dự thảo…', 'left270510Dự thảo…' — đo trên
    file thật BNV 16/7/2026). «dự thảo» NẰM TRONG CÂU (trích yếu 'góp ý dự thảo X') KHÔNG phải banner —
    đó là marker yếu, xử ở tầng weak."""
    for ln in (zone or "").splitlines()[:40]:
        t = _strip_accents(re.sub(r"^(?:left|right|center)?-?\d+\s*", "", ln.strip())).lower()
        if re.match(r"^du\s*thao\b", t):
            return True
    return False


def _sohieu_line_khuyet(zone: str) -> bool:
    """r179 T4 (PURE): dòng Số LETTERHEAD mà SỐ BỎ TRỐNG — 'Số:      /TTr-BNV', 'Luật số: /2026/QH16',
    'Số:' trơ — dấu hiệu văn bản CHƯA BAN HÀNH mạnh (đo trên file thật: 3/6 file lô BNV có dạng này).
    Chỉ nhận dòng ngắn ≤80 (dòng dài = văn xuôi)."""
    _LETTERHEAD_SO = (r"(?:(?:bo\s+luat|luat|nghi\s+quyet|nghi\s+dinh|phap\s+lenh|thong\s+tu|"
                      r"quyet\s+dinh|lenh)\s+)?so\s*[:.]")
    for ln in (zone or "").splitlines()[:40]:
        raw = re.sub(r"^(?:left|right|center)?-?\d+\s*", "", ln.strip())
        if not raw or len(raw) > 80:
            continue
        t = _strip_accents(raw).lower()
        if re.fullmatch(_LETTERHEAD_SO + r"\s*(?:/\S{1,25})?", t):
            return True
    return False


def _issue_dateline_complete(zone: str) -> bool:
    """r179 T4 (PURE): dateline ban hành ĐỦ SỐ 'ngày D tháng M năm YYYY' trong vùng tiêu đề. Dạng khuyết
    'ngày   tháng 7 năm 2026' (chưa ký) KHÔNG đạt. ⚠ một mình dateline KHÔNG đủ làm bằng chứng official —
    trích dẫn 'Căn cứ NĐ… ngày 23 tháng 5 năm 2018' trong 1500 ký tự đầu cũng khớp (đo file thật 01_Du_thao
    — vì vậy veto đòi AND với Số-line letterhead có số)."""
    return bool(re.search(r"ngay\s+\d{1,2}\s+thang\s+\d{1,2}\s+nam\s+(?:19|20)\d{2}",
                          _strip_accents(zone or "").lower()))


def _is_dang_title_zone(zone: str, sohieu: str = "") -> bool:
    """v1.34.41 B.2 GĐ2 (grill D3, PURE): văn kiện ĐẢNG khi BẤT KỲ 1/3 tín hiệu — đều trong TITLE-ZONE
    (doctrine N2b: nhắc trong câu văn/thân không phải bằng chứng): (a) dòng MỞ ĐẦU bằng banner 'ĐẢNG CỘNG SẢN
    VIỆT NAM' (VB Đảng không có quốc hiệu CHXHCN — có quốc hiệu thì (a)/(c) tắt); (b) số hiệu dạng Đảng
    NN-XX/CQ với cơ quan TW/VPTW/TU*/ĐU* (bắt cả ca .DOC convert rác mất banner); (c) cơ quan Đảng trong zone."""
    z = _strip_accents(zone or "").lower()
    if "cong hoa xa hoi chu nghia viet nam" not in z:
        if any(ln.strip().startswith("dang cong san viet nam") for ln in z.splitlines()[:40]):
            return True
        if any(p in z for p in ("ban chap hanh trung uong", "bo chinh tri", "ban bi thu",
                                "van phong trung uong", "ban chi dao trung uong", "dang uy",
                                "tinh uy", "thanh uy")):
            return True
    if sohieu and _SOHIEU_DANG_FULL_RE.fullmatch(str(sohieu).strip()):
        _cq = _strip_accents(str(sohieu).split("/")[-1]).upper()
        return _cq in ("TW", "VPTW") or _cq.startswith(("TU", "DU"))
    return False


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
    # v1.34.41 B.2 GĐ2 (control VBHN 19 BHXH — harness file thật bắt): layout VPQH KHÔNG có banner 'VĂN BẢN
    # HỢP NHẤT' lẫn cụm trong text probe → trước đây _infer_loai cứu qua mã sohieu, nay declared-first (D4)
    # 'LUẬT' sẽ đè mất → nhận VBHN THẲNG từ dạng số hiệu (mã VBHN đứng riêng, hoặc NN/VPQH bare — KHÔNG dùng
    # substring 'VPQH' trần vì NQ-VPQH là văn bản thường của VPQH).
    if sohieu and not _is_vbhn_doc:
        _shu = str(sohieu).upper().strip()
        _is_vbhn_doc = bool(re.search(r"(?:^|[-_/])VBHN(?:[-_/]|$)", _shu)
                            or re.fullmatch(r"\d{1,5}[-_/]VPQH", _shu))
    # v1.34.6 #1: chạy quét-VBHN cả khi sohieu title-zone RỖNG — layout VPQH in số VBHN ở KHỐI KÝ CUỐI
    # (ngoài vùng tiêu đề), quét sâu blob 16k CHỈ cho dạng số VBHN (không nhận số thường trong thân).
    if _is_vbhn_doc and (not sohieu or ("VBHN" not in sohieu.upper() and "VPQH" not in sohieu.upper())):
        _mv = re.search(r"\d+[-_/](?:\d+[-_/])?VBHN[-_/][A-Za-zĐđ0-9]+|\d+[-_/](?:VPQH|VBHN)\b", blob, re.I)
        sohieu = _mv.group(0) if _mv else ""
    # v1.34.41 B.2 GĐ2 (grill D4): LETTERHEAD KHAI BÁO là bằng chứng bậc nhất — ruột văn bản là sự thật, tên file
    # là fallback (ca thật QĐ 383-QĐ/TW: file QD_ nói 'Quyết định', letterhead nói 'QUY ĐỊNH'; ca gốc HD 09-HD/VPTW
    # bị filename-first đoán 'Luật'). Không đọc được text (.DOC rác/sheet) → _declared rỗng → đường cũ giữ nguyên.
    loai = _declared_loai_from_header(head) or _infer_loai(filename or head[:200], sohieu)
    if _is_vbhn_doc:
        loai = "Văn bản hợp nhất"    # N2a: header VBHN in 'BỘ LUẬT'/'LUẬT' to → _infer_loai đoán nhầm loại gốc
    if not loai:
        # v1.34.41 B.2 GĐ2 (G3, cùng khuôn N2b): fallback marker CHỈ có nghĩa ở VÙNG TIÊU ĐỀ + tên file —
        # 'nghị quyết' nhắc sâu trong thân từng nhuộm loai cho tài liệu thường (r103 negative bắt).
        _tz_norm = _strip_accents((head[:1500] or "") + "\n" + (filename or "")).lower()
        if "nghi quyet" in _tz_norm:
            loai = "Nghị quyết"
        elif "du thao" in _tz_norm and "luat" in _tz_norm:
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
    # r179 T4 (grill 21-07 — BẬC BẰNG CHỨNG, MỌI HỆ, không riêng Đảng): (1) banner «DỰ THẢO» dòng riêng HOẶC
    # Số-line KHUYẾT số («Số:  /TTr-BNV») = bằng chứng draft MẠNH ⇒ draft; (2) Số-line letterhead CÓ SỐ THẬT
    # trong TEXT (strict — KHÔNG best-fallback/filename: đo file thật thấy sohieu nhiễm UUID tên file) AND
    # dateline «ngày D tháng M năm Y» ĐỦ SỐ = bằng chứng official MẠNH ⇒ PHỦ QUYẾT marker chữ yếu («lấy ý
    # kiến»/«góp ý»/«dự thảo» trong trích yếu — văn bản BÀN VỀ dự thảo không đổi bản chất nó); (3) không bằng
    # chứng nào ⇒ marker yếu giữ hành vi cũ. QĐ 383-QĐ/TW «lấy ý kiến» đã ký → hết draft oan (log vận hành).
    _draft_zone = _strip_accents((head[:1500] or "") + "\n" + (filename or "")).lower()
    _weak_draft = any(k in _draft_zone for k in ("du thao", "draft", "lay y kien", "gop y du thao"))
    _tz179 = head[:1500] or ""
    _strong_draft = _draft_banner_line(_tz179) or _sohieu_line_khuyet(_tz179)
    _strong_official = (bool(_sohieu_from_title_zone(_tz179, strict_letterhead=True))
                        and _issue_dateline_complete(_tz179))
    draft = (not _is_vbhn_doc) and (_strong_draft or (_weak_draft and not _strong_official))
    # v1.34.41 B.2 GĐ2 (grill D2 — G4 PHẢI vá cùng G1): văn kiện ĐẢNG/VB HÀNH CHÍNH nhận diện TRƯỚC nhánh
    # vbqppl — nếu không, sohieu Đảng vừa bắt được sẽ kích 'elif sohieu' → vbqppl → Điều-gate chặn oan cat 00.
    # dang thắng CẢ draft (văn kiện Đảng không bao giờ đòi Điều, draft hay không; cờ draft vẫn giữ ở field riêng).
    _is_dang = (not _is_vbhn_doc) and _is_dang_title_zone(head[:1500], sohieu)
    kind = "normal"
    if _is_dang:
        kind = "dang"
    elif draft:
        kind = "draft"
    elif (not _is_vbhn_doc) and sohieu and _SOHIEU_HC_FULL_RE.fullmatch(str(sohieu).strip()):
        kind = "hanhchinh"    # NN/VBHN-VPQH cũng khớp shape NN/XX-CQ → phải loại trừ VBHN trước
    elif loai == "Nghị quyết":
        kind = "nq"
    elif sohieu or loai in {"Luật", "Bộ luật", "Nghị định", "Thông tư", "Quyết định", "Pháp lệnh", "Văn bản hợp nhất"}:
        kind = "vbqppl"
    # v1.34.41 B.2 GĐ2 (grill D5): số Đảng/hành chính KHÔNG NĂM tái dùng qua khóa/năm — cùng lớp collision VBHN
    # → sohieu_key year-qualified NN-YYYY-… (năm từ issue_date; bất biến [[vbqppl-sohieu-must-have-year]]).
    # sohieu NGUYÊN VĂN giữ riêng; khóa canonical registry mới year-qualified.
    _shk = norm_sohieu(sohieu) if sohieu else ""
    if _shk and kind in ("dang", "hanhchinh") and year and not _sohieu_year(_shk):
        _shk = re.sub(r"^(\d{1,5})-", rf"\g<1>-{year}-", _shk, count=1)
    return {
        "kind": kind,
        "draft": draft,
        "sohieu": sohieu or "",
        "sohieu_key": _shk,
        "loai": loai,
        "issue_year": year,
        "issue_date": facts.get("issue_date") or "",
        "agency": facts.get("agency") or "",
        "title": _profile_title_from_header(head, filename),
        "header_chars": len(head),
    }


def _safe_profile_doc_name(info: dict, fallback_name: str = "") -> str:
    # v1.34.41 B.2 GĐ2 (grill D7): mã theo quy ước ĐANG SỐNG trên corpus (CT_/KL_/KH_… đã dùng thật);
    # Phụ lục=PL chung sống với Pháp lệnh (ngữ cảnh profile ≠ corpus nền — _infer_loai PL_ vẫn = Pháp lệnh,
    # Phụ lục cần bằng chứng letterhead/explicit); Quy định=QDi vì QD đã là Quyết định.
    loai_code = {
        "Luật": "Luat", "Bộ luật": "Bo_luat", "Nghị quyết": "NQ", "Nghị định": "ND",
        "Thông tư": "TT", "Quyết định": "QD", "Pháp lệnh": "PL", "Văn bản hợp nhất": "VBHN",
        "Chỉ thị": "CT", "Kết luận": "KL", "Hướng dẫn": "HD", "Kế hoạch": "KH", "Thông báo": "TB",
        "Công văn": "CV", "Tờ trình": "TTr", "Đề án": "DA", "Báo cáo": "BC", "Phát biểu": "PB",
        "Chương trình": "CTr", "Biểu mẫu": "Mau", "Công điện": "CD", "Phụ lục": "PL", "Tài liệu": "TL",
        "Quy định": "QDi", "Quy chế": "QC", "Thông tri": "TTri", "Điều lệ": "DL",
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
        # v1.34.41 B.2 GĐ2 (grill D7): key CHƯA year-qualified (số Đảng/hành chính không năm) → NĂM BẮT BUỘC
        # trong tên (bất biến chống collision — số Đảng tái dùng qua khóa; khớp tên thật KL_121-KL-TW_2025 đang có).
        if info.get("issue_year") and not _sohieu_year(str(info["sohieu_key"])):
            parts.append(str(info["issue_year"]))
    elif info.get("issue_year"):
        parts.append(str(info["issue_year"]))
    parts.append(title_slug)
    return re.sub(r"_+", "_", "_".join(parts)).strip("_")[:160]


def _profile_loai_evidence(loai: str, text: str, name: str, explicit: bool) -> tuple[str, str]:
    """v1.34.40 B.2 (log Chỉ thị — HD 09-HD/VPTW bị đoán loai='Luật' rồi ghi thẳng registry): profile VĂN BẢN
    THƯỜNG chỉ persist loai có BẰNG CHỨNG TƯỜNG MINH — (a) cờ --loai user truyền; (b) letterhead khai báo
    (dòng IN HOA đứng riêng, _declared_loai_from_header); (c) prefix tên file (_infer_loai). Suy diễn heuristic
    thân-văn-bản → ĐỂ TRỐNG ('blank-over-guess' — thà user điền còn hơn ghi sai). Corpus nền vbqppl KHÔNG qua
    gate này (heuristic đang đúng cho VBQPPL). Trả (loai_để_ghi, nguồn_bằng_chứng). PURE, test offline."""
    if explicit:
        return loai, "explicit"
    canon = _normalize_loai(str(loai or ""))
    if not canon:
        return "", ""
    dec = _normalize_loai(_declared_loai_from_header(text or ""))
    if dec and dec == canon:
        return canon, "letterhead"
    inf = _normalize_loai(_infer_loai(name or "", "") or "")
    if inf and inf == canon:
        return canon, "name_prefix"
    return "", "suppressed"


_DUP_DIEU_HEAD_RE = re.compile(r"(?im)^\s*Điều\s+(\d{1,3}[a-zđ]?)\s*[.:]")
_SECOND_LETTERHEAD_RE = re.compile(r"(?im)^\s*(CỘNG\s*H[OÒ]A\s*XÃ\s*HỘI|Số\s*:\s*\d{1,5}\s*/)")


def _dup_dieu_scan(text: str) -> dict:
    """PURE (v1.34.54 A7a — ca WCT_HOP_NAP trộn toàn văn Berne: 1 file điều ước chứa 2 văn bản nối nhau, 'Điều 8'
    xuất hiện 2 lần nội dung khác → NLM/RAG trả nhầm điều khoản): đếm số hiệu Điều LẶP + dò letterhead THỨ HAI
    sau dòng 80. KHÔNG kết luận thay người — caller quyết WARN (cat 23 điều ước) / info (VBHN/phụ lục sửa đổi
    lặp Điều là BÌNH THƯỜNG — không chặn để khỏi false-positive)."""
    counts: dict[str, int] = {}
    for m in _DUP_DIEU_HEAD_RE.finditer(text or ""):
        k = m.group(1).lower()
        counts[k] = counts.get(k, 0) + 1
    dups = {k: v for k, v in counts.items() if v >= 2}
    second = None
    for i, ln in enumerate((text or "").splitlines()[80:], start=81):
        if _SECOND_LETTERHEAD_RE.match(ln):
            second = i
            break
    return {"dup_articles": dups, "dup_count": len(dups), "second_header_line": second,
            "suspect": bool(dups and second is not None)}


def _dup_dieu_note(scan: dict) -> str:
    """PURE: 1 dòng mô tả kết quả _dup_dieu_scan cho stderr/warning."""
    _sample = ", ".join(f"Điều {k}×{v}" for k, v in list((scan.get("dup_articles") or {}).items())[:5])
    _sh = scan.get("second_header_line")
    return _sample + (f" + letterhead thứ 2 ~dòng {_sh}" if _sh else "")


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
    # v1.34.38 (#1 log phiên Chỉ thị — 3 dương-tính-giả chặn corpus HD 09-HD/VPTW + PL01 + 9 chunk Đề án CĐS):
    # (a) heading dò trên BẢN STRIP-ACCENT (regex có-dấu cũ miss 'PHỤ LỤC 01' dạng NFD/hoa — PL01 chính LÀ
    #     phụ lục mà không được nhận); (b) CHỈ nghi khi nhắc 'phụ lục' KÈM SỐ (văn xuôi 'kèm theo phụ lục'
    #     không phải bằng chứng thiếu ruột); (c) gate CHẶN corpus chỉ trên corpus NỀN vbqppl — profile văn bản
    #     thường hạ về info-flag (mirror doctrine requires_dieu v1.34.27 #2).
    mention_num = re.search(r"phu\s*luc\s*(?:so\s*)?[0-9ivx]{1,4}\b", norm)
    heading_pl = re.search(r"(?m)^\s*phu\s*luc\b", norm)
    phuluc_raw_ok = (not mention_num) or bool(heading_pl)
    phuluc_ok = phuluc_raw_ok if base_profile else True
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
    if info.get("kind") == "dang":
        info_flags.append("DANG_DOC_DIEU_NOT_REQUIRED")     # trace v1.34.41 B.2 GĐ2: văn kiện Đảng không đòi Điều
    elif info.get("kind") == "hanhchinh":
        info_flags.append("HANHCHINH_DOC_DIEU_NOT_REQUIRED")
    if not phuluc_raw_ok and not base_profile:
        info_flags.append("PHULUC_MENTION_PROFILE_INFO")    # trace v1.34.38 #1: profile thường không chặn corpus
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
    if getattr(a, "resume", False):   # v1.34.55 C4+C5: RESUME theo registry — không upload/organize lại
        return cmd_profile_ingest_resume(a)
    from tl_core.ingest_contract import authorize_apply, build_ingest_plan, validate_source_file
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    profile = _active_profile()
    if profile == DEFAULT_PROFILE and not getattr(a, "allow_default", False):
        print("[tl] profile-ingest chỉ dành cho profile dự án; thêm --allow-default nếu cố ý chạy trên vbqppl.", file=sys.stderr)
        return 2
    _perr = _profile_policy_error(require_registry=True, require_manifest=True, forbid_inherit=True)
    if _perr:
        return _emit_profile_policy_error(_perr, getattr(a, "json", False))
    f = getattr(a, "file", None)
    # v1.34.37: --drive-id = file ĐÃ Ở TRONG THƯ MỤC PROFILE → bỏ upload, CHỈ convert→GDoc + đổi tên chuẩn (giữ
    # PHẲNG trong root profile, KHÔNG xếp cat). Tải NHỊ PHÂN về temp để probe/verify chạy y như đường local.
    _from_drive = ""
    _source_sha256 = ""
    _drive_id = (getattr(a, "drive_id", None) or "").strip()
    if _drive_id:
        if f:
            print(json.dumps({"ok": False, "step": "drive_id_args",
                              "error": "CHỈ MỘT trong <file> (local) HOẶC --drive-id (đã ở Drive) — không cả hai."},
                             ensure_ascii=False), file=sys.stderr)
            return 2
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        _dsrc = _resolve_drive_id_source(_gas(), _drive_id)
        if not _dsrc.get("ok"):
            print(json.dumps({"ok": False, "step": "drive_id_resolve", **_dsrc}, ensure_ascii=False, indent=2),
                  file=sys.stderr)
            return 2
        f = _dsrc.get("local_path") or ""
        _from_drive = _drive_id
        _source_sha256 = str(_dsrc.get("sha256") or "")
    if not (f and Path(f).exists()):
        print(f"[tl] profile-ingest: không thấy file {f} (dùng <file> local HOẶC --drive-id <id> đã ở thư mục profile)",
              file=sys.stderr)
        return 2
    _source_check = validate_source_file(
        f, allowed_exts={".docx", ".doc", ".pdf", ".rtf", ".odt", ".xlsx", ".xls"},
        direct_upload=(not bool(_from_drive)),
    )
    if not _source_check.get("ok"):
        print(_json_dumps({"ok": False, "step": "source_validate", **_source_check},
                          deterministic=_deterministic_enabled(a)), file=sys.stderr)
        return 2
    source_quality = _profile_source_quality(f, getattr(a, "source_quality", "auto"))
    # v1.34.6 #2: bảng tính đi đường riêng — canonical = Google SHEET (copy_convert toType=sheets),
    # không probe text/không gate Điều (không có văn bản pháp quy dạng bảng tính), NLM add type=sheets.
    _is_sheet = Path(f).suffix.lower() in _SPREADSHEET_EXTS
    # v1.34.58 (C-#9): .pdf probe qua _probe_pdf_quality — lấy flag broken_font cho gate DRY bên dưới.
    _pdf_q9p = None
    if _is_sheet:
        probe_text, probe_source = "", None
    elif not getattr(a, "text_file", None) and Path(f).suffix.lower() == ".pdf":
        _pdf_q9p = _probe_pdf_quality(f)
        probe_text, probe_source = _pdf_q9p["text"], (_pdf_q9p["source"] or None)
    else:
        probe_text, probe_source = _profile_read_probe_text(f, getattr(a, "text_file", None))
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
        if _pdf_q9p and _pdf_q9p.get("broken_font"):
            # v1.34.58 (C-#9): DRY báo đúng bệnh — thay NO_TEXT/OCR_UNVERIFIED bằng flag broken-font
            # (gate không chặn từ probe local; apply giữ nguyên: _read_doc_text(gdoc) sau convert quyết corpus).
            gate["flags"] = [x for x in (gate.get("flags") or [])
                             if x not in ("NO_TEXT_FOR_VERIFY", "OCR_UNVERIFIED_NOT_CORPUS")]
            gate["flags"].append(_PDF_BROKEN_FONT_WARN)
        _dd54 = _dup_dieu_scan(probe_text)   # v1.34.54 A7a: profile = info-only (VBHN/mục lục lặp Điều bình thường)
        if _dd54.get("dup_count"):
            print(f"[tl] ℹ dup-Điều (A7a): {_dup_dieu_note(_dd54)} — info; nghi file trộn nhiều văn bản thì soi tay.",
                  file=sys.stderr)
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
    _contract = build_ingest_plan(
        f, target_scope=f"profile-root:{profile}", canonical_name=doc_name, profile=profile,
        source_kind=("drive" if _from_drive else "local"), source_id=_from_drive,
        source_sha256=_source_sha256,
        options={"source_quality": source_quality,
                 "ocr_verified": bool(getattr(a, "ocr_verified", False)),
                 "hieuluc": getattr(a, "hieuluc", None) or "",
                 "large_threshold": large_threshold, "chunk_max_chars": chunk_max,
                 "allow_default": bool(getattr(a, "allow_default", False)),
                 "skip_live_check": bool(getattr(a, "skip_live_check", False))},
    )
    if not _contract.get("ok"):
        print(_json_dumps({"ok": False, "step": "plan_build", "detail": _contract},
                          deterministic=_deterministic_enabled(a)), file=sys.stderr)
        return 2
    plan.update({"schema": _contract.get("schema"), "source_sha256": _contract.get("source", {}).get("sha256"),
                 "identity_hash": _contract.get("identity_hash"), "plan_hash": _contract.get("plan_hash")})
    if not getattr(a, "apply", False):
        plan["apply_requires"] = ["--apply", "--confirm yes", f"--expected-plan-hash {_contract['plan_hash']}"]
        print(_json_dumps(plan, deterministic=_deterministic_enabled(a)))
        return 0
    _auth = authorize_apply(apply=True, confirm=getattr(a, "confirm", None),
                            expected_plan_hash=getattr(a, "expected_plan_hash", None),
                            actual_plan_hash=_contract["plan_hash"])
    if not _auth.get("ok"):
        print(_json_dumps({"ok": False, "step": "apply_authorization", **_auth},
                          deterministic=_deterministic_enabled(a)), file=sys.stderr)
        return 2

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
    # v1.34.53 (C2 — log phiên OCR 2026-07-15: lệnh loạt timeout giữa chừng, chạy lại → 6 dòng registry trùng TÊN
    # y hệt, phải hygiene scan + xóa tay): DUP-GUARD THEO TÊN trong REGISTRY (live, refresh) TRƯỚC upload/tạo GDoc —
    # SỚM HƠN gate TITLE_ALREADY_ON_NOTEBOOK (gate đó chỉ chặn trước NLM add, khi GDoc+registry ĐÃ tạo = dup rồi).
    # Fail-closed: không đọc được registry → DỪNG (đằng nào bước sau cũng cần GAS). Cùng file Drive (--drive-id)
    # chạy lại = organize upsert cùng dòng, KHÔNG phải dup → bỏ qua dòng trùng drive_id nguồn.
    if not getattr(a, "allow_dup_name", False):
        try:
            _rg_dup = g.get("reg_get", name_contains=doc_name, refresh="true")
        except Exception as _dge:  # noqa: BLE001
            _rg_dup = {"ok": False, "error": str(_dge)}
        if not _rg_dup.get("ok"):
            print(json.dumps({"ok": False, "step": "registry_dup_name_gate", "aborted": True,
                              "error": "REGISTRY_DUP_CHECK_FAILED", "detail": _rg_dup.get("error"),
                              "note": "Không đọc được registry để kiểm tên trùng — DỪNG an toàn TRƯỚC upload."},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
        _dup_rows = [r for r in (_rg_dup.get("rows") or [])
                     if str(r.get("name") or "").strip() == doc_name
                     and str(r.get("drive_id") or r.get("gdoc_id") or "") != str(_from_drive or "")]
        if _dup_rows:
            print(json.dumps({"ok": False, "step": "registry_dup_name_gate", "aborted": True,
                              "error": "NAME_ALREADY_IN_REGISTRY", "name": doc_name,
                              "existing": [{"drive_id": str(r.get("drive_id") or r.get("gdoc_id") or ""),
                                            "src_id": str(r.get("src_id") or ""),
                                            "nlm_source_id": str(r.get("nlm_source_id") or "")} for r in _dup_rows[:5]],
                              "note": "DỪNG TRƯỚC upload/GDoc (chưa side-effect). Chạy lại sau timeout thường rơi "
                                      "vào đây — dòng cũ ĐÃ có: dùng dòng cũ / `tl source-delete` dòng hỏng rồi chạy "
                                      "lại; trùng tên hợp lệ (hiếm): --allow-dup-name."},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
    up_mime, up_ext = _upload_mime_ext(f)
    if _from_drive:
        # v1.34.37: dùng chính file Drive có sẵn làm nguồn convert (KHÔNG re-upload).
        fid = _from_drive
    else:
        inbox = (g.get("bootstrap") or {}).get("inboxFolderId")
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
            # v1.34.40 B.2 blank-over-guess: profile thường chỉ ghi loai có bằng chứng tường minh
            # (letterhead/prefix tên) — heuristic thân-văn-bản → để trống, user điền qua register.
            _lv, _lsrc = _profile_loai_evidence(info["loai"], probe_text, doc_name, False)
            if _lv:
                okw["loai"] = _lv
            else:
                print(f"[tl] B.2 blank-over-guess: loai '{info['loai']}' suy heuristic (không letterhead/prefix) "
                      f"→ ĐỂ TRỐNG; điền sau: tl register --drive-id <gdoc> --loai \"{info['loai']}\"",
                      file=sys.stderr)
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
    if not _is_sheet and not actual_text.strip():
        _stage_v = _verified_reg_write(g, [{"drive_id": gdoc, "name": doc_name, "corpus": "false",
                                            "row_kind": "own", "note": "canonical_readback_failed",
                                            "hieuluc": hieuluc}],
                                       "name,corpus,row_kind,note,hieuluc")
        print(_json_dumps({"ok": False, "step": "canonical_text_readback", "gdoc": gdoc,
                           "registry_verified": bool(_stage_v.get("verified")),
                           "note": "Không dùng probe trước upload thay cho canonical readback; tài liệu giữ staged."},
                          deterministic=_deterministic_enabled(a)), file=sys.stderr)
        return 2
    verify_text = actual_text if not _is_sheet else probe_text
    if verify_text:
        info = _classify_doc_header(verify_text, doc_name)
        if info.get("draft") and not doc_name.upper().startswith("DUTHAO_"):
            doc_name = "DUTHAO_" + doc_name
            try:
                _ren = g.get("rename", fileId=gdoc, name=doc_name)
            except Exception as _ren_exc:  # noqa: BLE001
                _ren = {"ok": False, "error": f"{type(_ren_exc).__name__}: {_ren_exc}"}
            _ren_rb = _verify_convert_readback(g, gdoc_id=gdoc, expected_name=doc_name,
                                                src_id="", expected_src_name="",
                                                expected_folder_id=root_id)
            _ren_reg = (_verified_reg_upsert(g, {"drive_id": gdoc, "name": doc_name,
                                                 "hieuluc": DRAFT_WARNING})
                        if _ren.get("ok") and _ren_rb.get("ok") else {"verified": False})
            if not (_ren.get("ok") and _ren_rb.get("ok") and _ren_reg.get("verified")):
                print(_json_dumps({"ok": False, "step": "late_draft_rename_readback", "rename": _ren,
                                   "drive_readback": _ren_rb, "registry": _ren_reg},
                                  deterministic=_deterministic_enabled(a)), file=sys.stderr)
                return 2
            hieuluc = DRAFT_WARNING
        gate = _ingest_verify_gate(verify_text, info, source_quality, getattr(a, "ocr_verified", False))
        _dd54a = _dup_dieu_scan(verify_text)   # v1.34.54 A7a: apply đọc text canonical — info-only cho profile
        if _dd54a.get("dup_count"):
            print(f"[tl] ℹ dup-Điều (A7a): {_dup_dieu_note(_dd54a)} — info; nghi file trộn nhiều văn bản thì soi tay.",
                  file=sys.stderr)
        chunks = _split_by_dieu_chunks(verify_text, chunk_max) if (len(verify_text) > chunk_max or size_bytes > large_threshold) else []
    note = _profile_ingest_note(info, gate, source_quality, len(chunks))
    if not gate.get("ok"):
        rb = _verified_reg_write(g, [{"drive_id": gdoc, "name": doc_name, "corpus": "false", "row_kind": "own",
                                      "note": note, "hieuluc": hieuluc}],
                                 "name,corpus,row_kind,note,hieuluc")
        out = {"ok": False, "step": "verify_gate", "gdoc": gdoc, "src_id": fid, "gate": gate,
               "registry_verified": bool(rb.get("verified")),
               "note": "Canonical đã tạo nhưng chưa corpus/NLM; cần verify/OCR lại."}
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
        return 2

    # v1.34.60 (E3 — tổng quát hoá B1 sang profile-ingest, ADR-4): NLM hard-dead → TỰ CHUYỂN --no-nlm-add
    # (mirror ingest-local v1.34.54) thay vì chết ở dedup-gate LIVE_SOURCE_LIST_FAILED phía dưới; Drive+registry
    # vẫn hoàn tất, corpus KHÔNG set, nạp NLM cuối lô qua nlm-links + reconcile. Tắt: --no-fallback/TL_NLM_FALLBACK=0.
    if not getattr(a, "no_nlm_add", False) and _nlm_fallback_enabled(a):
        _v60p = _nlm_verdict(notebook_id)
        if not _v60p["alive"]:
            _nlm_fallback_banner("profile-ingest", _v60p.get("why") or "", "deferred")
            a.no_nlm_add = True
    if getattr(a, "no_nlm_add", False):
        # v1.34.54 (B2 — trình tự grill Q4: Drive + sắp xếp TRƯỚC, NLM CUỐI LÔ qua nlm-links/batch dán tay):
        # dừng sau Drive+registry, mirror `ingest-local --no-nlm-add` (v1.34.35). corpus KHÔNG set (S4).
        rb = _verified_reg_write(g, [{"drive_id": gdoc, "name": doc_name, "corpus": "false", "row_kind": "own",
                                      "note": note, "hieuluc": hieuluc}],
                                 "name,corpus,row_kind,note,hieuluc")
        out = {"ok": bool(rb.get("verified")), "nlm": "SKIPPED_BY_FLAG", "gdoc": gdoc, "src_id": fid,
               "name": doc_name, "gdoc_url": f"https://docs.google.com/document/d/{gdoc}",
               "notebook_url": f"https://notebooklm.google.com/notebook/{notebook_id}",
               "registry_verified": bool(rb.get("verified")),
               "next_steps": [f"tl --profile {_active_profile()} nlm-links   # stdout = link dán batch vào notebook",
                              f"tl --profile {_active_profile()} nlm-reconcile {notebook_id} --apply   # link registry sau khi dán"]}
        if len(chunks) > 1:
            out["note"] = ("File LỚN cần chunk khi lên NLM — đường add-tay KHÔNG tự tạo chunk GDoc; khi nạp NLM "
                           "chạy lại profile-ingest KHÔNG --no-nlm-add (pipeline chunk+add đầy đủ).")
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
        return 0 if rb.get("verified") else 2
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
        nlm_sources = _profile_push_chunks(g, nc, notebook_id, gdoc, doc_name, info, note, meta_id, chunks)
        _children_ok = bool(nlm_sources) and all(x.get("ok") for x in nlm_sources) and len(nlm_sources) == len(chunks)
        rb = _verified_reg_write(g, [{"drive_id": gdoc, "name": doc_name,
                                      "corpus": ("true" if _children_ok else "false"), "row_kind": "own",
                                      "note": note, "hieuluc": hieuluc}],
                                 "name,corpus,row_kind,note,hieuluc")
        _final_ok = bool(_children_ok and rb.get("verified"))
    else:
        add = nc.source_add(notebook_id, drive_id=gdoc, doc_type=("sheets" if _is_sheet else "doc"), wait=True)
        if not (add.get("ok") and add.get("source_id")):
            print(json.dumps({"ok": False, "step": "nlm_add", "gdoc": gdoc, "detail": add}, ensure_ascii=False, indent=2),
                  file=sys.stderr)
            return 2
        src = add.get("source_id")
        rb = _verified_reg_write(g, [{"drive_id": gdoc, "name": doc_name, "nlm_source_id": src,
                                      "nlm_notebook_id": notebook_id, "row_kind": "own",
                                      "nlm_status": "pushed", "corpus": "true", "note": note,
                                      "hieuluc": hieuluc}],
                                 "name,nlm_source_id,nlm_notebook_id,row_kind,nlm_status,corpus,note,hieuluc")
        _final_ok = bool(rb.get("verified"))
        nlm_sources.append({"ok": _final_ok, "canonical": True, "gdoc": gdoc, "nlm_source_id": src,
                            "registry_verified": _final_ok})
    out = {"ok": _final_ok, "profile": profile, "gdoc": gdoc, "src_id": fid, "doc_name": doc_name,
           "plan_hash": _contract["plan_hash"], "identity_hash": _contract["identity_hash"],
           "classification": info, "verify_gate": gate, "split_count": len(chunks),
           "nlm_sources": nlm_sources, "registry_verified": bool(rb.get("verified")),
           "registry_patched": (rb.get("reg_bulk") or {}).get("patched"),
           "target_notebook": notebook_id, "hieuluc": hieuluc}
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0 if _final_ok else 2


def _profile_push_chunks(g, nc, notebook_id: str, gdoc: str, doc_name: str, info: dict, note: str,
                         meta_id: str, chunks: list, done_parts: dict | None = None) -> list:
    """v1.34.55 (C4 — tách NGUYÊN VĂN từ cmd_profile_ingest để --resume dùng CHUNG): đẩy từng chunk lên NLM +
    registry (createtext → source_add → reg_upsert row_kind=ref). done_parts: {part → row registry ĐÃ xong} —
    resume bỏ qua part đó (vẫn tính ok để _children_ok trung thực trên TOÀN bộ part)."""
    nlm_sources = []
    for c in chunks:
        _p = int(c["part"])
        if done_parts and _p in done_parts:
            _r0 = done_parts[_p]
            nlm_sources.append({"ok": True, "part": _p, "chunk_gdoc": str(_r0.get("drive_id") or ""),
                                "nlm_source_id": str(_r0.get("nlm_source_id") or ""), "resumed_skip": True})
            continue
        cname = f"{doc_name}__part{_p:02d}"
        cr = g.post("createtext", text=c["text"], name=cname, folderId=meta_id,
                    register="false", share="false", sourceUrl=f"profile-ingest:{gdoc}")
        chunk_id = cr.get("fileId")
        if not chunk_id:
            nlm_sources.append({"ok": False, "part": c["part"], "step": "createtext", "detail": cr})
            continue
        add = nc.source_add(notebook_id, drive_id=chunk_id, doc_type="doc", wait=True)
        src = add.get("source_id") if add.get("ok") else ""
        if not src:
            nlm_sources.append({"ok": False, "part": c["part"], "chunk_gdoc": chunk_id,
                                "step": "nlm_add_missing_source_id", "detail": add})
            continue
        _chunk_reg = _verified_reg_upsert(
            g, {"drive_id": chunk_id, "src_id": gdoc, "sohieu": info.get("sohieu") or "",
                "loai": info.get("loai") or "thuong", "name": cname, "cat": "own",
                "mime": "application/vnd.google-apps.document", "goc": gdoc,
                "nlm_source_id": src, "nlm_notebook_id": notebook_id,
                "nlm_status": "pushed", "corpus": "false", "row_kind": "ref",
                "note": (note + f"; chunk_part={c['part']}; dieu={c.get('start_dieu')}-{c.get('end_dieu')}")[:500]})
        nlm_sources.append({"ok": bool(_chunk_reg.get("verified")), "part": c["part"],
                            "chunk_gdoc": chunk_id, "nlm_source_id": src, "chars": c.get("chars"),
                            "registry_verified": bool(_chunk_reg.get("verified"))})
    return nlm_sources


_RESUME_PART_RE = re.compile(r"__part(\d{1,3})$")


def cmd_profile_ingest_resume(a) -> int:
    """v1.34.55 (C4+C5 — log phiên OCR: bị giết giữa lúc add chunk → phải reg-query dò tay, xóa sạch canonical
    lẫn chunk mồ côi rồi chạy lại TỪ ĐẦU ×2; + 4 canonical corpus=''/false dù chunk con pushed đủ): RESUME theo
    REGISTRY — KHÔNG upload/organize lại. Dò canonical (tên y hệt) + chunk `__partNN` hiện có; re-split text
    canonical TỪ DRIVE (tất định, cùng chunk_max) → CHỈ làm part còn thiếu; cuối cùng ghi corpus canonical theo
    _children_ok — nghĩa là chạy resume trên name đã-đủ-part cũng TỰ SỬA ca corpus kẹt false (C5). Nguồn đơn
    (không chunk): thiếu nlm_source_id → add; có rồi → chỉ repair corpus. Cần --name + --apply --confirm yes
    (không plan-hash — không có file nguồn local; xác nhận tường minh thay thế)."""
    name = (getattr(a, "name", None) or "").strip()
    if not name:
        print(json.dumps({"ok": False, "error": "RESUME_NEEDS_NAME",
                          "note": "Truyền --name '<tên canonical y hệt registry>' (lấy từ NAME_ALREADY_IN_REGISTRY "
                                  "hoặc reg-query --name)."}, ensure_ascii=False), file=sys.stderr)
        return 2
    if not getattr(a, "apply", False) or str(getattr(a, "confirm", "") or "").strip().lower() != "yes":
        print(json.dumps({"ok": False, "error": "CONFIRM_REQUIRED", "expected": "yes",
                          "note": "--resume ghi NLM/registry → cần --apply --confirm yes (không có plan-hash vì "
                                  "không có file nguồn local)."}, ensure_ascii=False), file=sys.stderr)
        return 2
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    _perr = _profile_policy_error(require_registry=True, require_manifest=True, forbid_inherit=True)
    if _perr:
        return _emit_profile_policy_error(_perr, getattr(a, "json", False))
    notebook_id, nb_err = _resolve_nlm_notebook(None)
    if nb_err:
        print(json.dumps({"ok": False, "step": "notebook_resolve", "error": nb_err}, ensure_ascii=False), file=sys.stderr)
        return 2
    g = _gas()
    try:
        _rg = g.get("reg_get", name_contains=name, refresh="true")
    except Exception as _e:  # noqa: BLE001
        _rg = {"ok": False, "error": str(_e)}
    if not _rg.get("ok"):
        print(json.dumps({"ok": False, "error": "RESUME_REGISTRY_READ_FAILED", "detail": _rg.get("error")},
                         ensure_ascii=False), file=sys.stderr)
        return 2
    rows = _rg.get("rows") or []
    canon = next((r for r in rows if str(r.get("name") or "").strip() == name), None)
    if not canon:
        print(json.dumps({"ok": False, "error": "RESUME_NOT_FOUND", "name": name,
                          "note": "Không có dòng canonical tên này — chạy profile-ingest thường (chưa có gì để nối)."},
                         ensure_ascii=False), file=sys.stderr)
        return 2
    gdoc = str(canon.get("drive_id") or canon.get("gdoc_id") or "")
    hieuluc = str(canon.get("hieuluc") or "") or "Còn"
    note = (str(canon.get("note") or "") or f"resume:{name}")[:300]
    info = {"sohieu": str(canon.get("sohieu") or ""), "loai": str(canon.get("loai") or "")}
    done_parts: dict[int, dict] = {}
    for r in rows:
        _nm = str(r.get("name") or "").strip()
        if not _nm.startswith(name + "__part"):
            continue
        m = _RESUME_PART_RE.search(_nm)
        if m and (str(r.get("nlm_source_id") or "").strip()):
            done_parts[int(m.group(1))] = r
    text = _read_doc_text(gdoc) or ""
    if not text:
        print(json.dumps({"ok": False, "error": "RESUME_TEXT_UNAVAILABLE", "gdoc": gdoc,
                          "note": "Không đọc được text canonical từ Drive để re-split — kiểm gdoc/export."},
                         ensure_ascii=False), file=sys.stderr)
        return 2
    chunk_max = int(getattr(a, "chunk_max_chars", None) or 100000)
    chunks = _split_by_dieu_chunks(text, chunk_max) if len(text) > chunk_max else []
    nc = _imp("nlm_cli")
    meta_id = os.environ.get("TL_META_FOLDER_ID", "").strip() or os.environ.get("TL_ROOT_FOLDER_ID", "").strip()
    if len(chunks) > 1:
        nlm_sources = _profile_push_chunks(g, nc, notebook_id, gdoc, name, info, note, meta_id, chunks,
                                           done_parts=done_parts)
        _children_ok = bool(nlm_sources) and all(x.get("ok") for x in nlm_sources) and len(nlm_sources) == len(chunks)
        rb = _verified_reg_write(g, [{"drive_id": gdoc, "name": name,
                                      "corpus": ("true" if _children_ok else "false"), "row_kind": "own",
                                      "note": note, "hieuluc": hieuluc}],
                                 "name,corpus,row_kind,note,hieuluc")
        _final_ok = bool(_children_ok and rb.get("verified"))
        out = {"ok": _final_ok, "resumed": True, "gdoc": gdoc, "name": name,
               "parts_total": len(chunks), "parts_skipped_done": len(done_parts),
               "parts_pushed_now": sum(1 for x in nlm_sources if x.get("ok") and not x.get("resumed_skip")),
               "children_ok": _children_ok, "corpus_written": "true" if _children_ok else "false",
               "registry_verified": bool(rb.get("verified")), "nlm_sources": nlm_sources}
    else:
        _sid = str(canon.get("nlm_source_id") or "").strip()
        if not _sid:
            add = nc.source_add(notebook_id, drive_id=gdoc, doc_type="doc", wait=True)
            if not (add.get("ok") and add.get("source_id")):
                print(json.dumps({"ok": False, "step": "nlm_add", "gdoc": gdoc, "detail": add},
                                 ensure_ascii=False, indent=2), file=sys.stderr)
                return 2
            _sid = add.get("source_id")
        rb = _verified_reg_write(g, [{"drive_id": gdoc, "name": name, "nlm_source_id": _sid,
                                      "nlm_notebook_id": notebook_id, "row_kind": "own",
                                      "nlm_status": "pushed", "corpus": "true", "note": note,
                                      "hieuluc": hieuluc}],
                                 "name,nlm_source_id,nlm_notebook_id,row_kind,nlm_status,corpus,note,hieuluc")
        out = {"ok": bool(rb.get("verified")), "resumed": True, "gdoc": gdoc, "name": name,
               "parts_total": 0, "single_source": True, "nlm_source_id": _sid,
               "corpus_written": "true", "registry_verified": bool(rb.get("verified"))}
        _final_ok = out["ok"]
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0 if _final_ok else 2


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


def _ingest_local_prev_state(file_path: str, name: str, *, identity_hash: str = "", plan_hash: str = "") -> dict:
    """Return resumable state only for the exact content-addressed plan.

    ``file_path`` and ``name`` remain in the signature for compatibility but
    are never identity.  Legacy journals without plan/identity hashes are
    deliberately not resumed because matching them by name can reuse IDs from
    different source bytes.
    """
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
        if not plan_hash or str(head.get("plan_hash") or "") != str(plan_hash):
            continue
        if identity_hash and str(head.get("identity_hash") or "") != str(identity_hash):
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
            st["plan_hash"] = str(head.get("plan_hash") or "")
            st["identity_hash"] = str(head.get("identity_hash") or "")
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
    from tl_core.ingest_contract import authorize_apply, build_ingest_plan, validate_source_file
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    _perr = _profile_policy_error(require_registry=True, require_manifest=False, forbid_inherit=True)
    if _perr:
        return _emit_profile_policy_error(_perr, getattr(a, "json", False))
    f = getattr(a, "file", None)
    # v1.34.37: --drive-id = file ĐÃ Ở TRÊN DRIVE (người dùng kéo-thả _HOP_NAP qua UI) → bỏ upload, organize
    # ngay trên file đó. Tải NHỊ PHÂN về temp để auto-plan/size chạy Y NHƯ đường local; fid = drive_id gốc.
    _from_drive = ""
    _source_sha256 = ""
    _drive_id = (getattr(a, "drive_id", None) or "").strip()
    if _drive_id:
        if f:
            print(json.dumps({"ok": False, "step": "drive_id_args",
                              "error": "CHỈ MỘT trong <file> (local) HOẶC --drive-id (đã ở Drive) — không cả hai."},
                             ensure_ascii=False), file=sys.stderr)
            return 2
        _dsrc = _resolve_drive_id_source(_gas(), _drive_id)
        if not _dsrc.get("ok"):
            print(json.dumps({"ok": False, "step": "drive_id_resolve", **_dsrc}, ensure_ascii=False, indent=2),
                  file=sys.stderr)
            return 2
        if _dsrc.get("is_sheet"):
            print(json.dumps({"ok": False, "step": "drive_id_sheet", "drive_id": _drive_id,
                              "error": "Bảng tính (.xlsx/.xls) không đi đường ingest-local (canonical vbqppl = Google Doc). "
                                       "Bảng tính thuộc profile riêng → dùng `tl profile-ingest --drive-id`."},
                             ensure_ascii=False), file=sys.stderr)
            return 2
        f = _dsrc.get("local_path") or ""
        _from_drive = _drive_id
        _source_sha256 = str(_dsrc.get("sha256") or "")
    if not (f and Path(f).exists()):
        print(f"[tl] ingest-local: không thấy file {f} (dùng <file> local HOẶC --drive-id <id> đã ở Drive)",
              file=sys.stderr); return 2
    _source_check = validate_source_file(
        f, allowed_exts={".docx", ".doc", ".pdf", ".rtf", ".odt"}, direct_upload=(not bool(_from_drive))
    )
    if not _source_check.get("ok"):
        print(_json_dumps({"ok": False, "step": "source_validate", **_source_check},
                          deterministic=_deterministic_enabled(a)), file=sys.stderr)
        return 2
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
    # v1.34.40 B.2 blank-over-guess: profile thường + loai KHÔNG tường minh (từ auto-plan heuristic) → đòi
    # bằng chứng letterhead/prefix; thiếu → để trống thay vì ghi sai (ca HD 09-HD/VPTW bị đoán 'Luật').
    if loai and not str(getattr(a, "loai", None) or "").strip() and _active_profile() != DEFAULT_PROFILE:
        _pt_b2, _ = _profile_read_probe_text(f, getattr(a, "text_file", None))
        _lv_b2, _lsrc_b2 = _profile_loai_evidence(loai, _pt_b2, name, False)
        if not _lv_b2:
            print(f"[tl] B.2 blank-over-guess: loai '{loai}' suy heuristic (không letterhead/prefix) — ĐỂ TRỐNG "
                  f"cho profile thường; điền sau: tl register --drive-id <gdoc> --loai \"{loai}\"", file=sys.stderr)
            loai = ""
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
            "from_drive_id": _from_drive or None,
            "auto_plan": auto_plan}
    _contract = build_ingest_plan(
        f,
        target_scope=f"drive:{_active_profile()}:{cat}",
        canonical_name=name,
        profile=_active_profile(),
        source_kind=("drive" if _from_drive else "local"),
        source_id=_from_drive,
        source_sha256=_source_sha256,
        options={
            "sohieu": sohieu, "cat": cat, "goc": goc, "hieuluc": hieuluc, "loai": loai,
            "auto_plan": bool(getattr(a, "auto_plan", False)),
            "source_quality": getattr(a, "source_quality", "auto"),
            "ocr_verified": bool(getattr(a, "ocr_verified", False)),
            "force_cat": bool(getattr(a, "force_cat", False)),
            "allow_large": bool(getattr(a, "allow_large", False)),
            "large_threshold": _large_threshold,
            "skip_nlm_preflight": bool(getattr(a, "skip_nlm_preflight", False)),
            "skip_live_check": bool(getattr(a, "skip_live_check", False)),
            "nlm_no_wait": bool(getattr(a, "nlm_no_wait", False)),
            "no_nlm_add": bool(getattr(a, "no_nlm_add", False)),
        },
    )
    if not _contract.get("ok"):
        print(_json_dumps({"ok": False, "step": "plan_build", "detail": _contract},
                          deterministic=_deterministic_enabled(a)), file=sys.stderr)
        return 2
    plan.update({"schema": _contract.get("schema"), "source_sha256": _contract.get("source", {}).get("sha256"),
                 "identity_hash": _contract.get("identity_hash"), "plan_hash": _contract.get("plan_hash")})
    _prev = (_ingest_local_prev_state(str(f), name, identity_hash=_contract["identity_hash"],
                                      plan_hash=_contract["plan_hash"])
             if getattr(a, "resume", False) else {})
    if not getattr(a, "apply", False):
        plan["mode"] = "DRY"
        plan["note"] = (("--apply để chạy: dùng file Drive có sẵn (bỏ upload)→organize(convert/cat/stamp/register)"
                         "→preflight→nlm add (CLI)→push.") if _from_drive else
                        "--apply để chạy: [mkdir nếu cần]→upload→organize(convert/cat/stamp/register)→preflight→nlm add (CLI)→push.")
        plan["apply_requires"] = ["--apply", "--confirm yes", f"--expected-plan-hash {_contract['plan_hash']}"]
        _ph = _ingest_perf_hint(bool(getattr(a, "nlm_no_wait", False)), bool(getattr(a, "no_nlm_add", False)))
        if _ph:
            plan["perf_hint"] = _ph   # v1.34.73: nhắc đường nạp-lô nhanh ngay tại DRY (nơi người vận hành đọc plan)
        print(_json_dumps(plan, deterministic=_deterministic_enabled(a))); return 0
    _auth = authorize_apply(apply=True, confirm=getattr(a, "confirm", None),
                            expected_plan_hash=getattr(a, "expected_plan_hash", None),
                            actual_plan_hash=_contract["plan_hash"],
                            resume_plan_hash=(_prev.get("plan_hash") if _prev else None))
    if not _auth.get("ok"):
        print(_json_dumps({"ok": False, "step": "apply_authorization", **_auth},
                          deterministic=_deterministic_enabled(a)), file=sys.stderr)
        return 2
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
    if not getattr(a, "skip_nlm_preflight", False) and not getattr(a, "no_nlm_add", False):
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
            # v1.34.54 (B1/Q3=a — TRƯỚC: abort NLM_NOT_READY rc=2, user phải tự chạy lại với --no-nlm-add):
            # cookie chết → TỰ CHUYỂN quy trình ADD-TAY (v1.34.35): vẫn hoàn tất Drive+registry, KHÔNG đụng NLM,
            # output kèm link dán tay + next_steps reconcile. Muốn ép thử API add bất chấp: --skip-nlm-preflight.
            # v1.34.60 (E3 control-surface, ADR-5): --no-fallback / TL_NLM_FALLBACK=0 → KHÔI PHỤC fail-closed
            # (NLM_NOT_READY rc=2 như trước v1.34.54) — CI strict/user muốn dừng cứng.
            if not _nlm_fallback_enabled(a):
                print(json.dumps({"ok": False, "error": "NLM_NOT_READY", "why": _nlm_why,
                                  "note": "--no-fallback/TL_NLM_FALLBACK=0: DỪNG trước mọi side-effect. "
                                          "Sửa `nlm login` rồi chạy lại; hoặc bỏ --no-fallback để tự chuyển "
                                          "--no-nlm-add (ADD-TAY)."}, ensure_ascii=False, indent=2),
                      file=sys.stderr)
                return 2
            print(f"[tl] ⚠ NLM chết ({_nlm_why}) → TỰ CHUYỂN --no-nlm-add (ADD-TAY): xong Drive+registry, "
                  f"dán link vào notebook rồi `tl nlm-reconcile --apply`. (Kiểm phiên: tl nlm-auth-status --wait)",
                  file=sys.stderr, flush=True)
            a.no_nlm_add = True
        else:
            for _w54 in (_nlm_preflight_report(_nb_check, probe=False).get("warn") or []):   # v1.34.54 A1 tầng-2
                print(f"[tl] ⚠ {_w54}", file=sys.stderr)
    g = _gas()
    # v1.29.1 (log LIVE 2.4): JOURNAL bao trùm CHUỖI composite (mkdir→upload→organize→nlm_add→reg_link) — ngắt giữa
    # chừng → `tl journal <run>` chỉ RÕ bước dở + việc còn lại (ca Luật Dược 76/VBHN phải dò tay). Intent các bước
    # non-registry KHÔNG kèm `before` + op ∉ {reg_bulk,reg_upsert} → resume/undo (chỉ reapply op reg) KHÔNG đụng.
    # N6 (v1.33.42): --resume đọc trạng thái run trước TỪ JOURNAL (tất định — không đoán) TRƯỚC khi mở run mới.
    if _prev:
        print(f"[tl] ingest-local --resume: nối từ journal {_prev.get('journal_prev')} — đã xong: "
              + (",".join(k for k in ("upload_fid", "gdoc", "nlm_source_id") if _prev.get(k)) or "(chưa bước nào)"),
              file=sys.stderr)
    run_id = _apply_journal_start("ingest-local", {"file": str(f), "name": name, "cat": cat, "profile": _active_profile(),
                                                   "source_sha256": _contract["source"]["sha256"],
                                                   "identity_hash": _contract["identity_hash"],
                                                   "plan_hash": _contract["plan_hash"],
                                                   **({"resumed_from": _prev.get("journal_prev")} if _prev else {})})
    # v1.34.55 (D1 — nối scope-cut v1.34.52 F-04; Q6=a: target_scope GIỮ trục Drive-folder của build_ingest_plan,
    # claim = khóa chống race per-cửa-sổ chứ không phải định danh toàn cục): ACQUIRE claim identity TRƯỚC cửa sổ
    # upload→dedup-live→source_add — chặn 2 host cùng ingest 1 nội dung. MANDATORY client-side như ingest-missing
    # (webapp <2.21.2l → DỪNG rc=2 TRƯỚC side-effect); denied → CLAIMED_ELSEWHERE (đơn file — không có gì để skip).
    # BỎ QUA khi --no-nlm-add (không có cửa sổ add NLM; Drive+registry đã có dup-guard C2 + organize idempotent).
    _claim_ih55 = None
    if not getattr(a, "no_nlm_add", False):
        _claim_ih55 = str(_contract["identity_hash"])
        try:
            _cl55 = g.get("ingest_claim", keys=json.dumps([_claim_ih55]), run_id=run_id,
                          drive_ids=json.dumps([str(getattr(a, "drive_id", None) or "")]))
        except Exception as _cle55:  # noqa: BLE001
            _cl55 = {"ok": False, "error": str(_cle55)}
        if not _cl55.get("ok"):
            _journal_append(run_id, {"t": "run_end", "ok": False, "counts": {"BLOCKED": 1}})
            print(json.dumps({"ok": False, "error": "INGEST_CLAIM_FAILED", "detail": _cl55.get("error"),
                              "journal": run_id,
                              "note": "Không xin được claim xuyên host (F-04, webapp cần ≥2.21.2l) — DỪNG an toàn "
                                      "TRƯỚC upload (chưa side-effect)."}, ensure_ascii=False, indent=2),
                  file=sys.stderr)
            return 2
        _gr55 = next((r for r in (_cl55.get("results") or []) if r.get("identity_hash") == _claim_ih55), None)
        if not (_gr55 or {}).get("granted"):
            _journal_append(run_id, {"t": "run_end", "ok": False, "counts": {"BLOCKED": 1}})
            print(json.dumps({"ok": False, "error": "CLAIMED_ELSEWHERE", "journal": run_id,
                              "reason": (_gr55 or {}).get("reason"),
                              "note": "Host khác đang ingest CÙNG nội dung/scope (claim F-04) — không phải lỗi; "
                                      "thử lại sau ~5' (TTL) hoặc để host kia xong."}, ensure_ascii=False, indent=2),
                  file=sys.stderr)
            return 2

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
    # v1.34.53 (A4 — log phiên 2026-07-15: cookie chết + base đầy → `--no-nlm-add` vẫn bị chặn
    # OVERFLOW_ROOM_UNKNOWN, phải thêm --skip-nlm-preflight --skip-live-check oan): --no-nlm-add KHÔNG đụng
    # NLM trong run này → BỎ _ingest_target (nlm_preflight GAS + đếm slot live); target chỉ còn dùng in URL
    # next-steps, notebook thật do add-tay UI + nlm-reconcile sau quyết (quy trình ADD-TAY v1.34.35).
    if getattr(a, "no_nlm_add", False):
        target, pf = _nb_check, {"note": "no_nlm_add: bỏ nlm_preflight/đếm slot — notebook thật do reconcile sau quyết"}
    else:
        target, pf = _ingest_target(g, sohieu, name)
    # v1.34.47 (M1 fix): MỌI shard đầy → DỪNG TRƯỚC upload/register (chưa side-effect nào), KHÔNG add mù vào
    # shard đầy. Khớp gate 'blocked' của batch ingest-missing (KHÔNG auto-create notebook — ADR).
    if pf.get("blocked"):
        print(json.dumps({"ok": False, "blocked": True, "step": "nlm_target", "journal": run_id,
                          "reason": pf.get("reason"), "overflow_shard": pf.get("overflow_shard"),
                          "overflow_room": pf.get("overflow_room"),
                          "note": "MỌI shard (base+overflow) đầy — chưa upload/ghi gì. Duyệt/chuẩn bị shard mới "
                                  "(cập nhật overflowNotebookId hoặc tạo shard) rồi chạy lại."},
                         ensure_ascii=False), file=sys.stderr)
        return 2
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
    elif _from_drive:
        # v1.34.37: file ĐÃ Ở TRÊN DRIVE → dùng chính fileId đó làm nguồn organize (KHÔNG re-upload). Journal
        # dưới op 'upload' (kèm from_drive) để --resume tái dùng fileId y như đường local.
        fid = _from_drive
        _step_ok("upload", name + up_ext, True, fileId=fid, from_drive=True)
        print(f"[tl] --drive-id: dùng file có sẵn trên Drive (fileId={fid}), bỏ bước upload.", file=sys.stderr)
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
            if not _vbf.get("verified"):
                _journal_append(run_id, {"t": "run_end", "ok": False, "counts": {"FAILED": 1}})
                print(_json_dumps({"ok": False, "step": "registry_backfill_readback", "journal": run_id,
                                   "detail": _vbf}, deterministic=_deterministic_enabled(a)), file=sys.stderr)
                return 2
    # Registry is a required postcondition of organize, including the
    # intentional --no-nlm-add path.  Never infer it from the write response.
    try:
        _reg_read = g.get("reg_get", drive_id=gdoc, refresh="true")
        _reg_rows = (_reg_read.get("rows") or []) if isinstance(_reg_read, dict) and _reg_read.get("ok") is True else []
    except Exception as _reg_exc:  # noqa: BLE001
        _reg_read, _reg_rows = {"error": f"{type(_reg_exc).__name__}: {_reg_exc}"}, []
    _registry_row = (_reg_rows[0] or {}) if _reg_rows else {}
    _registry_checks = {
        "row_exists": bool(_registry_row),
        "drive_id": str(_registry_row.get("drive_id") or _registry_row.get("gdoc_id") or "") == str(gdoc),
        "source_id": str(_registry_row.get("src_id") or "") == str(_src_for_rb),
        "name": str(_registry_row.get("name") or "") == str(name),
        "cat": (not cat) or str(_registry_row.get("cat") or "") == str(_cat_reg_label(cat)),
    }
    if not all(_registry_checks.values()):
        _journal_append(run_id, {"t": "run_end", "ok": False, "counts": {"FAILED": 1}})
        print(_json_dumps({"ok": False, "step": "registry_readback", "journal": run_id,
                           "checks": _registry_checks, "readback": _reg_read},
                          deterministic=_deterministic_enabled(a)), file=sys.stderr)
        return 2
    # v1.34.35 (quy trình ADD-TAY): --no-nlm-add DỪNG tại đây — Drive + registry (organize register) ĐÃ xong,
    # KHÔNG đụng NLM (né cookie ~1h). corpus KHÔNG set (doctrine S4: corpus=true chỉ khi đã lên NLM). In next_steps
    # điền sẵn: add tay URL trên UI notebook → nlm-reconcile --apply (link bắc cầu exact-title: tên GDoc = tên
    # nguồn) → register --corpus true. Journal run_end đánh dấu no_nlm_add để --resume/journal-close hiểu đúng.
    if getattr(a, "no_nlm_add", False):
        if str(_registry_row.get("corpus") or "").strip().lower() in {"1", "true", "yes", "vbqppl"}:
            _journal_append(run_id, {"t": "run_end", "ok": False, "counts": {"FAILED": 1}})
            print(_json_dumps({"ok": False, "step": "no_nlm_registry_readback", "journal": run_id,
                               "error": "CORPUS_MUST_BE_FALSE_BEFORE_NLM", "registry_row": _registry_row},
                              deterministic=_deterministic_enabled(a)), file=sys.stderr)
            return 2
        _journal_append(run_id, {"t": "run_end", "ok": True, "counts": {"OK": 1}, "no_nlm_add": True})
        _gdoc_url = f"https://docs.google.com/document/d/{gdoc}"
        _nb_url = f"https://notebooklm.google.com/notebook/{target}"
        out = {"ok": True, "name": name, "gdoc": gdoc, "src_docx": src_docx, "cat": cat, "journal": run_id,
               "plan_hash": _contract["plan_hash"], "identity_hash": _contract["identity_hash"],
               "reg_cat_label": (_cat_reg_label(cat) if cat else None), "loai": loai or None,
               "corpus": False, "nlm": "SKIPPED_BY_FLAG", "preflight": pf,
               "gdoc_url": _gdoc_url, "suggested_notebook": target, "notebook_url": _nb_url,
               "next_steps": [
                   f"1) Add tay trên UI: mở {_nb_url} → Add source → Google Drive → chọn '{name}' (Drive-picker chọn được NHIỀU file 1 lần cho cả lô)",
                   "2) tl nlm-reconcile --all-notebooks   (nguồn add tay hiện thành link_candidates bắc cầu exact-title → chạy per-notebook --apply để link registry)",
                   f"3) tl register --drive-id {gdoc} --corpus true   (đưa vào corpus SAU khi đã link NLM)",
               ]}
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
        return 0
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
            # v1.34.33 (#2 benchmark 2026-07-12): settle-wait chiếm ~50% tổng 238s/file — `--nlm-no-wait` bỏ chờ
            # settle (source_id có NGAY từ add-response → reg_link phía dưới vẫn ghi ĐỦ; settle chạy ngầm phía NLM).
            _no_wait = bool(getattr(a, "nlm_no_wait", False))
            _step("nlm_source_add", gdoc, notebook=target, title=name[:120], wait=(not _no_wait))
            add = nc.source_add(target, drive_id=gdoc, doc_type="doc", wait=(not _no_wait))
            _add_verified = bool(add.get("ok") and add.get("source_id"))
            _step_ok("nlm_source_add", gdoc, _add_verified, source_id=add.get("source_id"), wait=(not _no_wait))
            if not _add_verified:
                print(json.dumps({"ok": False, "step": "nlm_add(cli)", "journal": run_id, "gdoc": gdoc, "target": target, "detail": add,
                                  "note": "NLM add phải trả source_id; Drive+registry đã xong, chạy lại CÙNG LỆNH + --resume."}, ensure_ascii=False, indent=2), file=sys.stderr)
                return 2
            src = add.get("source_id")
            if _no_wait:
                # Post-add dup-check cần source_list — nguồn CHƯA settle có thể chưa liệt kê → âm tính giả + tốn
                # thêm ~18s (trái mục đích no-wait). BỎ QUA có chủ đích; lưới sau = `tl nlm-reconcile` cuối lô.
                print("[tl] --nlm-no-wait: bỏ chờ settle + bỏ post-add dup-check — nạp lô xong chạy "
                      "`tl nlm-reconcile` xác nhận settle/link; truy vấn NLM nội dung này cần chờ vài phút.",
                      file=sys.stderr, flush=True)
            else:
                _dup_after = _nlm_post_add_dup_check(nc, target, gdoc, src)   # N1 v1.33.41: bắt trùng-sau-add tại chỗ
                if _dup_after:
                    print(json.dumps(_dup_after, ensure_ascii=False, indent=2), file=sys.stderr)
                    _journal_append(run_id, {"t": "run_end", "ok": False, "counts": {"FAILED": 1}})
                    return 2
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
    if _claim_ih55 and v.get("verified"):
        # v1.34.55 (D1/F-08): COMMIT claim GỘP vào 1 call reg_get_bulk (vừa đóng claim vừa readback) — best-effort,
        # lô lỗi tự heal qua TTL 5' (khớp dung sai ingest-missing D3/D7; kết quả run KHÔNG phụ thuộc commit).
        try:
            g.get("reg_get_bulk", keys=json.dumps([gdoc]), key_field="drive_id",
                  commit_claims=json.dumps([{"identity_hash": _claim_ih55, "source_id": src, "run_id": run_id}]))
        except Exception:  # noqa: BLE001
            print("[tl]   ⚠ claim commit chưa xác nhận — tự hết hạn sau 5' (F-04 TTL), không chặn kết quả.",
                  file=sys.stderr, flush=True)
    _journal_append(run_id, {"t": "run_end", "ok": bool(v.get("verified")), "counts": {"OK": 1}})
    _final_ok = bool(v.get("verified"))
    out = {"ok": _final_ok, "name": name, "gdoc": gdoc, "src_docx": src_docx, "cat": cat, "journal": run_id,
           "plan_hash": _contract["plan_hash"], "identity_hash": _contract["identity_hash"],
            "reg_cat_label": (_cat_reg_label(cat) if cat else None), "loai": loai or None, "corpus": _final_ok,
           "cat_ten": (official or {}).get("ten"), "folder_created": need_mkdir, "preflight": pf,
           "target_notebook": target, "row_kind": rk, "nlm_source_id": src, "reg_pushed": rb.get("patched"),
           "reg_verified": bool(v.get("verified")), "via": "nlm-cli",
           **({"nlm_settle": "not_waited", "next_step": "tl nlm-reconcile (cuối lô) — xác nhận nguồn settle + link đủ"}
              if getattr(a, "nlm_no_wait", False) else {}),
           "sidecar": "src_id=docx gắn vào dòng GDoc (register atomic; regen2 cũng tự ghép cặp cùng base-name)"}
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0 if _final_ok else 2


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
    # v1.34.58 (C-#9): .pdf probe qua _probe_pdf_quality để LẤY CẢ flag broken_font (text-layer mất dấu
    # ≠ scan — cảnh báo đúng bệnh thay vì dọa OCR oan); các đuôi khác giữ nguyên đường cũ.
    _pdf_q9 = None
    if not text_file and Path(path).suffix.lower() == ".pdf":
        _pdf_q9 = _probe_pdf_quality(path)
        probe_text, probe_source = _pdf_q9["text"], (_pdf_q9["source"] or "")
    else:
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
    _broken9 = bool(_pdf_q9 and _pdf_q9.get("broken_font"))
    if not probe_text:
        # v1.34.58 (C-#9, Q8=a): text-layer mất dấu ≠ không có text — cảnh báo đúng bệnh (Google-convert
        # thường xử được), KHÔNG dọa NO_PROBE_TEXT/OCR; gate không chặn từ probe local, apply verify GDoc.
        warnings.append(_PDF_BROKEN_FONT_WARN if _broken9 else "NO_PROBE_TEXT_FOR_AUTO_CAT")
    if not merged.get("sohieu"):
        warnings.append("SOHIEU_MISSING")
    if cat_plan.get("confidence") in {"low", "missing"}:
        warnings.append("CAT_AUTO_LOW_CONFIDENCE")
    srcq = _profile_source_quality(path, source_quality)
    if srcq == "ocr" and not ocr_verified and not _broken9:
        warnings.append("OCR_UNVERIFIED_NOT_CORPUS")
    # v1.34.54 (A7a — grill Q9=c): gate dup-Điều tại ingest, chi phí ≈0 (text đã có). Cat 23 (điều ước) → WARN
    # nghi file TRỘN nhiều văn bản (ca WCT lẫn Berne); cat khác → info (VBHN lặp Điều hợp lệ). KHÔNG chặn.
    _dd = _dup_dieu_scan(probe_text)
    if _dd.get("dup_count"):
        _eff_cat = str(cat or cat_plan.get("cat") or "")
        warnings.append(("MIXED_DOCUMENT_SUSPECT_DUP_DIEU: " if _eff_cat.split("_")[0] == "23"
                         else "DUP_DIEU_INFO: ") + _dup_dieu_note(_dd))
    return {
        "ok": bool(doc_name and cat_plan.get("cat")),
        "file": path,
        "dup_dieu": _dd,
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

_INBOX_INFRA_NAME_RE = re.compile(r"(?i)^(registry|manifest|\.tl_|__tl_)|\.(json|enc)$")


def cmd_ingest_inbox(a) -> int:
    """B2 (v1.34.54, grill Q4=a): QUÉT FOLDER Drive tìm file user vừa upload tay CHƯA có trong registry rồi chạy
    pipeline sẵn có per-file. Trình tự chuẩn (doctrine): skill đưa link folder (scope nền = inbox _HOP_NAP,
    profile = root profile phẳng) + link tải nguồn (ưu tiên TVPL/LuatVietnam) → user tự tải + upload → lệnh này
    convert/đổi tên/(vbqppl) xếp cat/register — KHÔNG đụng NLM (--no-nlm-add; NLM cuối lô qua `nlm-links` dán
    batch + `nlm-reconcile --apply`). Đối chiếu registry bằng reg_get_bulk (1 call); list qua GAS (KHÔNG Drive
    MCP — search_files parentId không liệt kê được folder share người khác). Child chạy 2 BƯỚC DRY→plan_hash→
    apply (khuôn C1). Profile: file trông như VBQPPL chất lượng cao (sohieu year-qualified từ tên + mime
    docx/doc/pdf) → cờ `vbqppl_candidate` + câu hỏi cho USER quyết (KHÔNG tự nạp corpus; profile KHÔNG move
    file). DRY mặc định; --apply --confirm yes."""
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    g = _gas()
    _prof = _active_profile()
    _profile_scope = _prof != DEFAULT_PROFILE
    folder = (getattr(a, "folder", None) or "").strip()
    if not folder:
        folder = (os.environ.get("TL_ROOT_FOLDER_ID", "").strip() if _profile_scope
                  else str((g.get("bootstrap") or {}).get("inboxFolderId") or ""))
    if not folder:
        print(json.dumps({"ok": False, "error": "NO_INBOX_FOLDER",
                          "note": "Không suy được folder quét — truyền --folder <id> (scope nền cần bootstrap "
                                  "inboxFolderId; profile cần rootFolderId)."}, ensure_ascii=False), file=sys.stderr)
        return 2
    ls = g.get("list", folderId=folder)
    if not ls.get("ok"):
        print(json.dumps({"ok": False, "error": "LIST_FOLDER_FAILED", "folder": folder, "detail": ls},
                         ensure_ascii=False), file=sys.stderr)
        return 2
    items = [it for it in (ls.get("items") or [])
             if str(it.get("type") or "") != "folder" and not _INBOX_INFRA_NAME_RE.search(str(it.get("name") or ""))
             and "google-apps.folder" not in str(it.get("mime") or "")]
    # Google-native (đã là GDoc/Sheet) → _resolve_drive_id_source từ chối convert=true (nhân đôi) — loại khỏi
    # kế hoạch, báo riêng để user biết (file GDoc thả tay vào inbox thường là đã-convert/không cần ingest lại).
    _gnative = [it for it in items if "google-apps" in str(it.get("mime") or "")]
    items = [it for it in items if "google-apps" not in str(it.get("mime") or "")]
    ids = [str(it.get("id")) for it in items if it.get("id")]
    reg_known: set = set()
    if ids:
        try:
            _rgb = g.get("reg_get_bulk", keys=json.dumps(ids), key_field="drive_id")
        except Exception as _e:  # noqa: BLE001
            _rgb = {"ok": False, "error": str(_e)}
        if not _rgb.get("ok"):
            print(json.dumps({"ok": False, "error": "REGISTRY_DIFF_FAILED", "detail": _rgb.get("error"),
                              "note": "Không đối chiếu được registry (cần webapp ≥2.21.2l) — DỪNG an toàn, "
                                      "không đoán file nào mới."}, ensure_ascii=False), file=sys.stderr)
            return 2
        for _i, _r in enumerate(_rgb.get("rows") or []):
            if _r:
                reg_known.add(ids[_i])
    new_items = [it for it in items if str(it.get("id")) not in reg_known]
    _lim = int(getattr(a, "limit", None) or 20)
    plan_items = []
    for it in new_items[:_lim]:
        did, nm, mime = str(it.get("id")), str(it.get("name") or ""), str(it.get("mime") or "")
        if _profile_scope:
            child = ["--profile", _prof, "profile-ingest", "--drive-id", did, "--no-nlm-add", "--json"]
            try:
                _sh = _parse_sohieu_from_name(nm) or ""
            except Exception:  # noqa: BLE001
                _sh = ""
            _quality = any(x in mime for x in ("wordprocessingml", "msword", "pdf"))
            _extra = {}
            if _sh and _quality:
                _extra = {"vbqppl_candidate": True, "sohieu_from_name": _sh,
                          "ask_user": (f"File trông như VBQPPL chất lượng cao (sohieu {_sh}, {mime.split('.')[-1]}) "
                                       f"— có nạp thêm vào corpus/notebook VBQPPL/shard overflow không? CHỈ nạp nếu "
                                       f"KHÔNG trùng: kiểm `tl reg-query --sohieu \"{_sh}\"` (scope nền) trước; nạp: "
                                       f"`tl ingest-local --drive-id {did} --auto-plan --no-nlm-add --apply …` (scope nền).")}
        else:
            child = ["ingest-local", "--drive-id", did, "--auto-plan", "--no-nlm-add", "--json"]
            _extra = {}
        plan_items.append({"drive_id": did, "name": nm, "mime": mime, "child_dry": child, **_extra})
    out = {"ok": True, "schema": "ingest_inbox.v1", "folder": folder,
           "folder_url": f"https://drive.google.com/drive/folders/{folder}", "profile": _prof,
           "files_seen": len(items) + len(_gnative), "google_native_skipped": len(_gnative),
           "already_registered": len(items) - len(new_items), "new_files": len(new_items),
           "planned": len(plan_items), "limit": _lim, "items": plan_items,
           "mode": "APPLY" if getattr(a, "apply", False) else "DRY"}
    if not getattr(a, "apply", False):
        out["note"] = ("DRY — --apply --confirm yes chạy per-file pipeline (child DRY→plan_hash→apply, không đụng "
                       "NLM). Sau lô: `tl nlm-links` (link dán batch) → dán vào notebook → `nlm-reconcile --apply`.")
        _emit_json_payload(out, getattr(a, "out", None))
        return 0
    if str(getattr(a, "confirm", "") or "").strip().lower() != "yes":
        print(json.dumps({"ok": False, "error": "CONFIRM_REQUIRED", "expected": "yes"}, ensure_ascii=False),
              file=sys.stderr)
        return 2
    results, _ok_n, _fail_n = [], 0, 0
    for pi in plan_items:
        _pair = {"planned_child_dry": list(pi["child_dry"]),
                 "planned_child_command": list(pi["child_dry"]) + ["--apply", "--confirm", "yes"]}
        _res, _dry_fail = _bridge_run_child_apply(_pair)
        _okf = bool(_res.get("ok"))
        _ok_n += 1 if _okf else 0
        _fail_n += 0 if _okf else 1
        results.append({"drive_id": pi["drive_id"], "name": pi["name"], "ok": _okf,
                        **({"error": _res.get("error"), "child_dry_result": _dry_fail} if not _okf else {}),
                        **({"vbqppl_candidate": True, "ask_user": pi.get("ask_user")} if pi.get("vbqppl_candidate") else {})})
        print(f"[tl] ingest-inbox: {pi['name'][:50]} → {'OK' if _okf else 'FAIL'}", file=sys.stderr, flush=True)
    out.update({"ok": _fail_n == 0, "results": results, "counts": {"OK": _ok_n, "FAIL": _fail_n},
                "next_steps": [f"tl{(' --profile ' + _prof) if _profile_scope else ''} nlm-links   # stdout = link dán batch",
                                "dán links vào Add source → Websites của notebook",
                                f"tl{(' --profile ' + _prof) if _profile_scope else ''} nlm-reconcile --all-notebooks   # DRY xem hướng dẫn per-notebook"]})
    _emit_json_payload(out, getattr(a, "out", None))
    return 0 if _fail_n == 0 else 2


def _resolve_drive_id_source(g, drive_id: str, *, download: bool = True) -> dict:
    """v1.34.37: phân giải file ĐÃ Ở TRÊN DRIVE (drive_id) thành nguồn ingest — thay bước upload local.
    Dùng cho `ingest-local --drive-id` (file người dùng tự để _HOP_NAP qua UI) + `profile-ingest --drive-id`
    (file đã ở thư mục profile): skill convert→GDoc + tên chuẩn + (vbqppl) xếp cat / (profile) giữ phẳng +
    register + NLM, KHÔNG re-upload từ máy.
      • Đọc metadata (action=info); TỪ CHỐI: không thấy / trashed / Google-native (đã là GDoc/Sheet — convert=true
        sẽ NHÂN ĐÔI vì doCopyConvert_ copy GDoc→GDoc).
      • Đuôi/MIME suy từ tên hiện có (nếu khớp _MIME_BY_EXT) hoặc từ MIME thật (reverse-map) — để `organize
        convert=true` convert ĐÚNG định dạng và readback tên src khớp.
      • download=True → tải NHỊ PHÂN về temp (đường _fast_drive_fetch: public-curl→direct-media→GAS) để auto-plan/
        probe-text/verify-gate chạy Y NHƯ đường local. `organize` vẫn dùng CHÍNH drive_id gốc (không re-upload).
    KHÔNG raise — trả {ok:False, reason} khi lỗi."""
    drive_id = (drive_id or "").strip()
    if not drive_id:
        return {"ok": False, "reason": "EMPTY_DRIVE_ID"}
    info = _drive_info_file(g, drive_id)
    if not info.get("ok"):
        return {"ok": False, "reason": "DRIVE_FILE_NOT_FOUND", "drive_id": drive_id, "detail": info.get("error")}
    f = info.get("file") or {}
    if str(f.get("trashed")).strip().lower() == "true":
        return {"ok": False, "reason": "DRIVE_FILE_TRASHED", "drive_id": drive_id}
    mime = _file_mime(info)
    cur_name = str(f.get("name") or "").strip()
    if mime.startswith("application/vnd.google-apps"):
        return {"ok": False, "reason": "ALREADY_GOOGLE_NATIVE", "drive_id": drive_id, "mime": mime, "name": cur_name,
                "note": "File đã là Google Doc/Sheet (không cần convert). Đưa vào registry/NLM bằng "
                        "`tl register --drive-id <id>` + `tl nlm-add --drive-id <id>`; hoặc chọn file NHỊ PHÂN gốc "
                        "(.docx/.doc/.pdf/.xlsx) trong Drive để ingest đầy đủ (convert + chuẩn hoá tên/cat)."}
    _ext_by_mime = {_v: _k for _k, _v in _MIME_BY_EXT.items()}
    _name_ext = Path(cur_name).suffix.lower()
    ext = _name_ext if _name_ext in _MIME_BY_EXT else _ext_by_mime.get(mime, "")
    try:
        size_bytes = int(f.get("size") or f.get("fileSize") or 0)
    except (TypeError, ValueError):
        size_bytes = 0
    if not cur_name or not mime or size_bytes <= 0:
        return {"ok": False, "reason": "DRIVE_METADATA_INCOMPLETE", "drive_id": drive_id,
                "name": cur_name, "mime": mime, "size_bytes": size_bytes}
    try:
        max_source_bytes = int(os.environ.get("TL_SOURCE_MAX_BYTES") or 100 * 1024 * 1024)
    except (TypeError, ValueError):
        max_source_bytes = 100 * 1024 * 1024
    if size_bytes > max_source_bytes:
        return {"ok": False, "reason": "SOURCE_SIZE_LIMIT_EXCEEDED", "drive_id": drive_id,
                "name": cur_name, "size_bytes": size_bytes, "max_bytes": max_source_bytes,
                "note": "Môi trường có thể đặt TL_SOURCE_MAX_BYTES; giới hạn ingest trực tiếp vẫn là 35 MiB."}
    if not ext:
        return {"ok": False, "reason": "DRIVE_MIME_UNSUPPORTED", "drive_id": drive_id,
                "name": cur_name, "mime": mime}
    _expected_mime = _MIME_BY_EXT.get(ext)
    if _expected_mime and mime != _expected_mime:
        return {"ok": False, "reason": "DRIVE_EXTENSION_MIME_MISMATCH", "drive_id": drive_id,
                "name": cur_name, "ext": ext, "mime": mime, "expected_mime": _expected_mime}
    stem = Path(cur_name).stem or (cur_name or drive_id)
    out = {"ok": True, "drive_id": drive_id, "name": cur_name, "stem": stem, "mime": mime, "ext": ext,
           "size_bytes": size_bytes, "is_sheet": ext in _SPREADSHEET_EXTS}
    if download:
        try:
            import atexit
            _td = tempfile.mkdtemp(prefix="tl_driveid_")
            atexit.register(shutil.rmtree, _td, ignore_errors=True)
            _lp = os.path.join(_td, (stem or "drive_src") + ext)
            _imp("tl_gws")._fast_drive_fetch(drive_id, _lp, label="ingest --drive-id", verbose=False)
            _downloaded_size = os.path.getsize(_lp)
            if _downloaded_size <= 0:
                raise RuntimeError("tải về 0 byte")
            if _downloaded_size != size_bytes:
                raise RuntimeError(f"download size mismatch: metadata={size_bytes}, local={_downloaded_size}")
            from tl_core.ingest_contract import sha256_file
            out["local_path"] = _lp
            out["sha256"] = sha256_file(_lp)
            out["cleanup"] = "atexit"
        except Exception as _e:  # noqa: BLE001
            if locals().get("_td"):
                shutil.rmtree(_td, ignore_errors=True)
            out["ok"] = False
            out["reason"] = "DRIVE_DOWNLOAD_FAILED"
            out["detail"] = f"{type(_e).__name__}: {_e}"
    return out


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
    actual_id = str(f.get("id") or f.get("fileId") or "").strip()
    ok = info.get("ok") is True and bool(actual_id) and actual_id == str(file_id)
    return {"ok": ok, "error": (None if ok else "INFO_READBACK_INCOMPLETE_OR_ID_MISMATCH"),
            "raw": info, "file": f}

def _file_parents(info: dict) -> list[str]:
    f = info.get("file") or {}
    parents = f.get("parents") or f.get("parentIds") or []
    if isinstance(parents, str):
        return [parents]
    return [str(x.get("id") if isinstance(x, dict) else x) for x in parents if x]
