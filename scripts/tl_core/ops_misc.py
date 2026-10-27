# -*- coding: utf-8 -*-
"""tl_core.ops_misc — I8 (v1.34.12): tách NGUYÊN VĂN nhóm lệnh vận-hành/chẩn-đoán còn lại từ scripts/tl.py
(doctor/ping/precheck/boot/up/perf/bench · reg-query/counts/exists/registry-map/cat-* · journal/undo/resume/
confirm · manifest/backfill-notebook/vbhn-normalize/reg-delete · init-config/config-pin-registry/edit-skill/
verify-integrity/instructions/instruction-audit/loop/cowork-plan + helper riêng-nhóm). Khuôn I1-I6: stub ủy
quyền trong tl; bind REBASE __globals__ về namespace SỐNG của tl. Hành vi khoá bởi r78a wiring + selftest."""
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

# MIRROR tl.py (default-param của _entries_with_live_fields eval TRƯỚC bind — bẫy I2;
# r78_loop_fields_mirror drift-lock khoá ops_misc._LOOP_LIVE_FIELDS == tl._LOOP_LIVE_FIELDS).
_LOOP_LIVE_FIELDS = ("corpus", "nlm_source_id", "nlm_status", "nlm_notebook_id")


def bind(tl_module) -> None:
    """REBASE __globals__ từng hàm đã chuyển về namespace SỐNG của tl (khuôn I1-I6)."""
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


def _journal_read(run_id: str) -> list:
    recs = []
    try:
        p = _journal_path(run_id)
        if p.exists():
            for ln in p.read_text(encoding="utf-8").splitlines():
                ln = ln.strip()
                if ln:
                    try:
                        recs.append(json.loads(ln))
                    except Exception:
                        pass
    except Exception:
        pass
    return recs


def _journal_undo_ops(records: list) -> list:
    """PURE: sinh danh sách op KHÔI PHỤC (restore giá trị 'before') cho các ghi ĐÃ commit-ok + reversible (có snapshot
    `before`), NGƯỢC thứ tự (undo mới-nhất-trước). Chỉ cho tầng registry (before=giá trị cũ các cột đã đổi); xoá NLM/Drive
    KHÔNG undo được → bỏ qua (before rỗng)."""
    st = _journal_resume_state(records)
    seen, ops = set(), []
    for iv in [r for r in (records or []) if r.get("t") == "intent"]:
        key = iv.get("key")
        before = iv.get("before")
        # 1 restore/key, dùng intent ĐẦU TIÊN có 'before' hợp lệ (retry → không sinh 2 restore / không restore giá trị đã đổi).
        if key in st["done"] and key not in seen and isinstance(before, dict) and before:
            seen.add(key)
            ops.append({"op": "restore", "key": key, "key_field": iv.get("key_field", "drive_id"),
                        "cols": iv.get("cols"), "before": before, "orig_op": iv.get("op")})
    ops.reverse()
    return ops


def _journal_resume_ops(records: list) -> list:
    """PURE (Pha 2): các op DỞ (intent chưa commit-ok) cần LÀM LẠI — dùng `set` (giá trị định ghi đã lưu trong intent).
    reg_clear / op thiếu `set` → bỏ (không tái tạo được). Idempotent: ghi lại giá trị đã định = an toàn."""
    st = _journal_resume_state(records)
    out = []
    for iv in st["inflight"]:
        if isinstance(iv.get("set"), dict) and iv.get("set") and iv.get("op") in ("reg_bulk", "reg_upsert"):
            out.append({"op": iv.get("op"), "key": iv.get("key"), "key_field": iv.get("key_field", "drive_id"),
                        "cols": iv.get("cols"), "set": iv["set"]})
    return out


def _journal_close_plan(records: list, entries_by_key: dict) -> dict:
    """PURE (S7 v1.33.44 — log 7A: journal giữ cờ inflight VĨNH VIỄN dù việc đã được LỆNH KHÁC hoàn tất — ca thật:
    ingest-local đứt trước reg_link, vá tay nlm-add + register xong mà run vẫn báo inflight=1 mãi): quyết định op
    inflight nào ĐÓNG được TẤT ĐỊNH. Heal = op có `set` (giá trị đích đã lưu trong intent) mà MỌI giá trị ĐÃ khớp
    registry hiện tại (entries_by_key theo drive_id, so mềm strip+lower) → remote đạt trạng thái đích, commit thiếu
    chỉ vì client chết sau khi việc xong. Op không so được (không set / key không có trong manifest / giá trị chưa
    khớp) → blocked, KHÔNG tự đóng (đóng ép: --force sau khi người vận hành tự verify)."""
    def _soft(x) -> str:
        return str(x if x is not None else "").strip().lower()
    st = _journal_resume_state(records)
    healable, blocked = [], []
    for iv in st["inflight"]:
        key, s = iv.get("key"), (iv.get("set") if isinstance(iv.get("set"), dict) else {}) or {}
        e = (entries_by_key or {}).get(key) or {}
        mism = sorted(k for k, v in s.items() if _soft(e.get(k)) != _soft(v)) if (s and e) else []
        if s and e and not mism:
            healable.append({"op": iv.get("op"), "key": key, "matched_cols": sorted(s.keys())})
        else:
            blocked.append({"op": iv.get("op"), "key": key,
                            "reason": ("NO_SET_TO_VERIFY" if not s else
                                       ("KEY_NOT_IN_MANIFEST" if not e else "VALUES_NOT_MATCHED")),
                            "mismatch_cols": mism})
    return {"healable": healable, "blocked": blocked,
            "counts": {"inflight": len(st["inflight"]), "healable": len(healable), "blocked": len(blocked)}}


def _loop_controller(rounds: list, k_dry: int = 2, max_iter: int = 8) -> dict:
    """PURE: điều khiển vòng lặp HỘI TỤ detect→fix→re-detect. rounds=[{fixed, remaining}] theo thứ tự (remaining=số việc PHÁT
    HIỆN đầu vòng, fixed=số đã sửa). Trả {status ∈ continue|converged|paused, reason}:
      • ≥ max_iter vòng → PAUSED (MAX_ITER, tránh lặp vô hạn).
      • k_dry vòng CUỐI đều remaining==0 → CONVERGED (hết việc).
      • vòng cuối fixed>0 nhưng remaining KHÔNG giảm so với vòng trước → PAUSED (NO_PROGRESS: fix không ăn, đừng lặp làm hỏng thêm).
      • còn lại → CONTINUE."""
    n = len(rounds)
    if n == 0:
        return {"status": "continue", "reason": "chưa chạy vòng nào"}
    if n >= max_iter:
        return {"status": "paused", "reason": f"MAX_ITER ({max_iter}) — dừng an toàn, rà tay"}
    if n >= k_dry and all((r.get("remaining") or 0) == 0 for r in rounds[-k_dry:]):
        return {"status": "converged", "reason": f"{k_dry} vòng cuối KHÔNG còn việc"}
    last = rounds[-1]
    if (last.get("fixed") or 0) > 0 and n >= 2:
        prev = rounds[-2]
        if (last.get("remaining") or 0) >= (prev.get("remaining") or 0) > 0:
            return {"status": "paused", "reason": "NO_PROGRESS: đã fix nhưng số tồn KHÔNG giảm — dừng, rà tay"}
    return {"status": "continue", "reason": "còn việc, tiếp vòng sau"}


def _integrity_scan() -> list:
    """DETECT (md5/wc-l hoá thành 1 lệnh): soi cắt-cụt/NUL MỌI scripts/*.py — đối chiếu on-disk ↔ ghép-từ-_parts.
    status: OK (khớp _parts) · NOPARTS (compile được, không có _parts để đối chiếu) · DRIFT (compile được nhưng KHÁC
    _parts → sửa tay chưa `build_parts`) · NUL (NUL-pad, strip là chạy) · TRUNCATED (không compile = mất byte) · MISSING."""
    import glob as _glob
    names = {Path(fp).stem for fp in _glob.glob(str(HERE / "*.py"))}
    pr = HERE / "_parts"
    if pr.is_dir():
        names |= {d.name for d in pr.iterdir() if d.is_dir()}
    rows = []
    for name in sorted(names):
        src = HERE / f"{name}.py"
        asm = _reassemble_parts(name)                       # str ghép từ _parts (đã verify==gốc lúc đóng gói) | None
        has_parts = asm is not None
        if not src.exists():
            rows.append({"name": name, "size": 0, "parts": has_parts,
                         "status": "MISSING", "repairable": has_parts and _compiles(asm)})
            continue
        raw = src.read_bytes()
        nul = b"\x00" in raw
        disk = raw.replace(b"\x00", b"").decode("utf-8", "replace")
        if not _compiles(disk):
            status = "TRUNCATED"
        elif nul:
            status = "NUL"
        elif has_parts and disk != asm:
            status = "DRIFT"
        elif has_parts:
            status = "OK"
        else:
            status = "NOPARTS"
        rows.append({"name": name, "size": len(raw), "parts": has_parts,
                     "status": status, "repairable": has_parts and _compiles(asm)})
    return rows


def cmd_edit_skill(a) -> int:
    """III.2: sửa file skill AN TOÀN (né tầng Edit/Write mount Cowork hay revert): đọc → thay chuỗi CÓ ASSERT ĐẾM →
    py_compile (nếu .py) → write_text → build_parts (re-chunk). --patch '[{"old":..,"new":..,"count":1}]' (hoặc --patch-file).
    DRY mặc định (chỉ assert + compile, KHÔNG ghi); --apply mới ghi. ASSERT lệch / compile fail → DỪNG, KHÔNG ghi."""
    fp = Path(getattr(a, "file", "") or "")
    if not fp.is_absolute():
        fp = HERE / fp.name           # chỉ thao tác trong scripts/ (an toàn)
    if not fp.exists():
        print(f"[tl] edit-skill: không thấy {fp}", file=sys.stderr); return 2
    try:
        raw = Path(a.patch_file).read_text(encoding="utf-8") if getattr(a, "patch_file", None) else (getattr(a, "patch", None) or "[]")
        patch = json.loads(raw)
    except Exception as e:  # noqa: BLE001
        print(f"[tl] edit-skill: --patch JSON lỗi: {e}", file=sys.stderr); return 2
    if not isinstance(patch, list) or not patch:
        print('[tl] edit-skill cần --patch \'[{"old":..,"new":..,"count":1}]\' (list không rỗng).', file=sys.stderr); return 2
    text = fp.read_text(encoding="utf-8")
    new_text, applied = text, []
    for i, p in enumerate(patch):
        old, new, want = p.get("old", ""), p.get("new", ""), int(p.get("count", 1))
        if not old:
            print(f"[tl] edit-skill: patch[{i}] thiếu 'old'.", file=sys.stderr); return 2
        got = new_text.count(old)
        if got != want:
            print(json.dumps({"ok": False, "patch_index": i, "expected_count": want, "found": got,
                              "error": "ASSERT_COUNT_MISMATCH — DỪNG, KHÔNG ghi (an toàn)"}, ensure_ascii=False), file=sys.stderr)
            return 2
        new_text = new_text.replace(old, new)
        applied.append({"index": i, "count": want})
    if fp.suffix == ".py":          # py_compile trên nội dung MỚI trước khi ghi
        import py_compile, tempfile
        tdir = os.environ.get("TMPDIR") or tempfile.gettempdir() or os.path.expanduser("~")
        tf = Path(tdir) / f"_editskill_{fp.stem}.py"
        try:
            tf.write_text(new_text, encoding="utf-8")
            py_compile.compile(str(tf), doraise=True)
        except py_compile.PyCompileError as e:
            print(json.dumps({"ok": False, "error": "PY_COMPILE_FAIL — DỪNG, KHÔNG ghi", "detail": str(e)[:300]}, ensure_ascii=False), file=sys.stderr)
            return 2
        finally:
            try: tf.unlink()
            except Exception: pass
    if not getattr(a, "apply", False):
        print(json.dumps({"ok": True, "mode": "DRY", "file": str(fp), "patches": applied, "compiles": True,
                          "bytes_before": len(text), "bytes_after": len(new_text),
                          "note": "DRY: assert đếm + py_compile PASS. --apply để ghi (write_text)."}, ensure_ascii=False, indent=2))
        return 0
    fp.write_text(new_text, encoding="utf-8")     # write_text (Python) — né tầng Edit/Write mount
    print(json.dumps({"ok": True, "file": str(fp), "patches": applied, "bytes_after": len(new_text),
                      "next": "chạy `python scripts/tl.py --selftest` xác nhận xanh."}, ensure_ascii=False, indent=2))
    return 0


def cmd_verify_integrity(a) -> int:
    """DETECT + RECOVER cắt cụt/NUL (mount Cowork #51435/#53940). `--fix` GHÉP file hỏng từ _parts, ghi bằng Python
    write_text (an toàn — né tầng Edit/Write Cowork hay cắt cụt). KHÔNG đụng DRIFT (sửa tay hợp lệ chưa re-chunk)."""
    rows = _integrity_scan()
    fixed = []
    if getattr(a, "fix", False):
        for r in rows:
            if r["status"] in _INTEGRITY_BAD and r["repairable"]:
                asm = _reassemble_parts(r["name"])
                dst = HERE / f"{r['name']}.py"
                try:
                    dst.write_text(asm, encoding="utf-8")   # ghi an toàn bằng Python
                    fixed.append(r["name"]); r["status"] = "FIXED"
                except Exception as e:  # noqa: BLE001
                    r["fix_error"] = str(e)
    bad = [r for r in rows if r["status"] in _INTEGRITY_BAD]
    if getattr(a, "json", False):
        print(json.dumps({"ok": not bad, "fixed": fixed, "rows": rows}, ensure_ascii=False, indent=2))
    else:
        mk = {"OK": "✓", "NOPARTS": "·", "DRIFT": "~", "NUL": "⚠", "TRUNCATED": "✗", "MISSING": "✗", "FIXED": "⟲"}
        for r in rows:
            print(f"  {mk.get(r['status'], ' ')} {r['name']:24s} {r['status']:9s} size={r['size']:7d} parts={'Y' if r['parts'] else '-'}")
        if fixed:
            print(f"  ⟲ đã GHÉP lại từ _parts (ghi bằng Python): {', '.join(fixed)}")
        unrep = [r["name"] for r in rows if r["status"] in _INTEGRITY_BAD and not r["repairable"] and r["status"] != "FIXED"]
        if unrep:
            print(f"  ✗ HỎNG: {', '.join(unrep)} → tải lại bản sạch `sh scripts/tl_fetch.sh <args>`.")
        print("  (_parts đã bỏ — toàn file NOPARTS là bình thường; nếu file cắt cụt: re-fetch `tl_fetch.sh`.)")
        print(f"== integrity: {len(rows)} file · lỗi={len([r for r in rows if r['status'] in _INTEGRITY_BAD])}"
              + (f" · đã sửa {len(fixed)}" if fixed else "") + " ==")
    return 0 if not [r for r in rows if r["status"] in _INTEGRITY_BAD] else 2


def gas_parallel(calls, max_workers: int = 8):
    """v1.19.6: chạy NHIỀU call webapp ĐỘC LẬP song song (Apps Script KHÔNG serialize — đo được ~3.2x
    nhanh hơn tuần tự). calls = list[(action, params_dict)]. Trả list kết quả theo đúng thứ tự.
    Dùng cho: verify/tra cứu nhiều số hiệu, source-map nhóm luật, prefetch cache."""
    import concurrent.futures as _cf
    g = _gas()
    results = [None] * len(calls)

    def _one(i_call):
        i, (action, params) = i_call
        try:
            results[i] = g.get(action, **(params or {}))
        except Exception as e:
            results[i] = {"ok": False, "error": f"{type(e).__name__}: {e}", "action": action}

    with _cf.ThreadPoolExecutor(max_workers=min(max_workers, max(1, len(calls)))) as ex:
        list(ex.map(_one, list(enumerate(calls))))
    return results


def cmd_ping(a) -> int:
    g = _gas()
    # v1.32.2 (log rà 69 — Cowork): Apps Script COLD-START trả 404/timeout 2-3 lần gọi ĐẦU rồi mới ấm → từng bị
    # kết luận sai 'webapp chết'. Retry ×3 backoff 2s/5s — CHỈ với lỗi dạng cold-start (404/timeout), lỗi khác giữ nguyên.
    import time as _t
    r = {}
    for _try in range(3):
        try:
            r = g.get("ping")
        except Exception as e:  # noqa: BLE001
            r = {"ok": False, "error": str(e)}
        if r.get("ok") is not False and r.get("version"):
            break
        _err = str(r.get("error") or "")
        if _try < 2 and re.search(r"404|timed?\s*out|timeout", _err, re.I):
            _wait = (2, 5)[_try]
            print(f"[ping] webapp nghi COLD-START (lần {_try + 1}: {_err[:90]}) — thử lại sau {_wait}s…",
                  file=sys.stderr, flush=True)
            _t.sleep(_wait)
            continue
        break
    v = r.get("version")
    match = (v == EXPECT_VERSION)
    if getattr(a, "json", False):
        print(json.dumps({"ok": bool(match), "version": v, "expect": EXPECT_VERSION, "match": bool(match), "raw": r},
                         ensure_ascii=False))
    else:
        print(json.dumps(r, ensure_ascii=False))
    if not match:
        print(f"[tl] ⚠ CẢNH BÁO: webapp version={v} ≠ {EXPECT_VERSION} (API_CONTRACT.md). "
              f"Đối chiếu hợp đồng trước khi gọi action.", file=sys.stderr)
        return 3
    return 0


def cmd_perf(a) -> int:
    """v1.19.6: đo thời gian THẬT — round-trip Apps Script, lợi ích gọi song song, trạng thái cache boot.
    server_ms (xử lý) thường tí xíu; phần lớn wall là ĐỘ TRỄ HTTP /exec → biết tối ưu đúng chỗ."""
    import statistics
    g = _gas()
    rows, r = [], {}
    walls = []
    for _ in range(5):
        t0 = time.time(); r = g.get("ping"); walls.append(int((time.time() - t0) * 1000))
    srv = r.get("elapsed_ms")
    rtt = int(statistics.median(walls))
    rows.append({"op": "ping x5 tuần tự (median round-trip)", "wall_ms": rtt, "server_ms": srv, "calls": 1})
    t0 = time.time(); gas_parallel([("ping", {})] * 4); par = int((time.time() - t0) * 1000)
    rows.append({"op": "ping x4 SONG SONG (tổng)", "wall_ms": par, "calls": 4})
    speedup = round((rtt * 4) / par, 1) if par else None
    t0 = time.time(); m = g.get("manifest"); rows.append({"op": "manifest (metadata)", "wall_ms": int((time.time() - t0) * 1000), "server_ms": m.get("elapsed_ms"), "calls": 1})
    t0 = time.time(); f = g.get("find", q="57/2024/QH15", max=3); rows.append({"op": "find (1 số hiệu)", "wall_ms": int((time.time() - t0) * 1000), "server_ms": f.get("elapsed_ms"), "calls": 1})
    idxp = _cache_file("manifest_index.json")
    if idxp.exists():
        age = int(time.time() - idxp.stat().st_mtime)
        cache_state = f"có (tuổi {age}s) → boot tái dùng 0 call nếu < TTL"
    else:
        cache_state = "chưa có → boot lần đầu ~2 call (~6–12s)"
    out = {
        "ok": True, "profile": _active_profile(),
        "round_trip_ms_median": rtt, "server_ms_sample": srv,
        "parallel_speedup_x": speedup, "boot_cache": cache_state, "rows": rows,
        "diagnosis": [
            f"Apps Script /exec ≈ {rtt}ms/call round-trip, server xử lý chỉ ~{srv}ms → nút thắt là ĐỘ TRỄ HTTP, KHÔNG phải logic/Python.",
            f"Gọi song song nhanh ~{speedup}x (Apps Script không serialize) → gộp tra cứu độc lập bằng gas_parallel.",
            "Giảm SỐ call: boot tái dùng cache local (TTL), locate/find ưu tiên offline manifest_index, changes_pull thay full reload.",
        ],
    }
    if a.json:
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"== tl perf (profile={_active_profile()}) ==")
        for x in rows:
            print(f"  {x['op']:40s} wall={x['wall_ms']:6d}ms  server={x.get('server_ms')}  calls={x.get('calls')}")
        print(f"  → round-trip ≈ {rtt}ms/call · server ~{srv}ms · song song ~{speedup}x · boot_cache: {cache_state}")
        for d in out["diagnosis"]:
            print("  • " + d)
    return 0


def cmd_boot(a) -> int:
    # v1.17.3: nạp --config/env TRƯỚC subprocess → boot.py con thấy creds qua env (kể cả boot.py thật).
    # v1.19.2: profile truyền qua --profile; boot.py tự đọc config profiles, tách cache
    # ~/.tra_luat_cache/<profile>/ và forward registryDocId/manifestId (qua _fallback/gas.py env-driven).
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    cfg = getattr(a, "config", None)
    # v1.19.6: boot tái dùng cache local theo TTL (mỗi call Apps Script ~3s); --refresh/--max-age xuyên xuống.
    extra = []
    if getattr(a, "refresh", False):
        extra.append("--refresh")
    if getattr(a, "max_age", None) is not None:
        extra += ["--max-age", str(a.max_age)]
    real, fb = HERE / "boot.py", HERE / "_fallback" / "boot.py"
    for cand in (real, fb):
        if cand.exists():
            cmd = [sys.executable, str(cand)] + (["--json"] if a.json else [])
            if cfg:
                cmd += ["--config", cfg]
            if getattr(a, "profile", None):
                cmd += ["--profile", a.profile]
            cmd += extra
            return subprocess.call(cmd)
    # boot-lite (không có boot.py ở gốc lẫn _fallback): cổng ping + tóm tắt config
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    g = _gas(); r = g.get("ping"); v = r.get("version")
    info = {"mode": "boot-lite (overlay, thiếu boot.py)", "version": v,
            "expect_version": EXPECT_VERSION, "version_match": v == EXPECT_VERSION,
            "profile": _active_profile(),
            "manifest_id": os.environ.get("TL_MANIFEST_ID", ""),
            "notebook_id": os.environ.get("TL_NOTEBOOK_ID", ""),
            "webapp": (os.environ.get("TL_WEBAPP", "")[:48] + "…") if os.environ.get("TL_WEBAPP") else ""}
    print(json.dumps(info, ensure_ascii=False, indent=None if a.json else 2))
    if v != EXPECT_VERSION:
        print(f"[tl] ⚠ version webapp={v} ≠ EXPECT={EXPECT_VERSION} → đối chiếu/bump trước khi gọi action.",
              file=sys.stderr)
        return 3
    return 0


def _merge_local_config(old: dict, new: dict) -> dict:
    """r280 (P16-F01) — PURE: hoà `new` (template public / tham số rời) LÊN TRÊN `old` (file đang có).

    Luật: khoá cấp 1 → `new` thắng KHI CÓ MẶT (khoá `old` mà `new` không nhắc thì GIỮ).
    `profiles` → hoà theo TỪNG TÊN profile, và trong mỗi block lại hoà theo TỪNG Ô — vì đây chính
    là thứ cần cứu: block dự án chỉ có ở `old` phải sống, ô người dùng ghim (`config-pin-registry`)
    phải sống, còn ô template nhắc tới thì template thắng. Không đụng khoá nào khác.
    """
    if not isinstance(old, dict) or not old:
        return dict(new or {})
    merged = {**old, **(new or {})}
    old_p, new_p = old.get("profiles"), (new or {}).get("profiles")
    if isinstance(old_p, dict) and isinstance(new_p, dict):
        out_p = dict(old_p)
        for name, blk in new_p.items():
            cur = out_p.get(name)
            out_p[name] = {**cur, **blk} if isinstance(cur, dict) and isinstance(blk, dict) else blk
        merged["profiles"] = out_p
    elif isinstance(old_p, dict) and new_p is None:
        merged["profiles"] = old_p
    return merged


def _heal_legacy_registry_doc_id(data: dict) -> bool:
    """Blank registryDocId trỏ Doc legacy 1mATG (base + mọi profile). Trả True nếu có sửa.
    r280: tách khỏi `cmd_init_config` để chạy được trên bản ĐÃ HOÀ — nếu chỉ heal template thì
    id legacy nằm sẵn trong file cũ sẽ sống sót qua bước merge mới (xem sự cố 2026-06-30)."""
    healed = False
    if not isinstance(data, dict):
        return False
    if str(data.get("registryDocId") or "") == _LEGACY_REGISTRY_DOC_ID:
        data["registryDocId"] = ""; healed = True
    for blk in (data.get("profiles") or {}).values():
        if isinstance(blk, dict) and str(blk.get("registryDocId") or "") == _LEGACY_REGISTRY_DOC_ID:
            blk["registryDocId"] = ""; healed = True
    return healed


def save_local_config(config_json=None, webapp=None, token=None, manifest_id=None, out=None, replace=False):
    """Lưu cấu hình local để phiên trống KHÔNG phụ thuộc mirror Drive public (mirror nay private — F7/F7b).
    Nguồn: chuỗi JSON đọc từ mirror qua Drive MCP, hoặc tham số rời.

    r280 (P16-F01, P0 mất dữ liệu): trước đây GHI ĐÈ TRỌN file đích bằng template public — không đọc
    file cũ, không backup, không atomic ⇒ `tl init-config --from-public` (chính lệnh mà ≥5 thông điệp
    lỗi của CLI khuyên chạy) XOÁ TRẮNG block `profiles` của mọi profile dự án. Nay: HOÀ lên file cũ
    (`_merge_local_config`), BACKUP bản cũ ra `_config_backup_dir()` (ngoài cây skill — doctrine r193/r202,
    backup chứa token), ghi ATOMIC (`_write_json_atomic`). `replace=True` = đường reset CỐ Ý, có cảnh báo.
    Trả `(path, info)` — `info` cho caller in ra đã giữ/ghi đè những gì.
    """
    data = {}
    if config_json:
        data = json.loads(config_json)
        if not isinstance(data, dict):
            raise ValueError("config-json phải là JSON object")
    if webapp: data["webappUrl"] = webapp
    if token: data["token"] = token
    if manifest_id: data["manifestId"] = manifest_id
    path = Path(out or (Path.home() / ".tra_luat_config.json"))
    old = {}
    try:
        if path.is_file():
            _cur = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(_cur, dict):
                old = _cur
    except Exception:  # noqa: BLE001
        old = {}     # file cũ hỏng/không parse được → coi như trống, nhưng VẪN backup ở dưới
    # ĐỌC file cũ ngay cả khi `replace`: bản cũ vẫn cần cho BACKUP và cho việc NÓI RA đã xoá những gì.
    merged = data if replace else _merge_local_config(old, data)
    _heal_legacy_registry_doc_id(merged)
    # Kiểm BẤT BIẾN trên bản SẼ GHI (không phải trên riêng input): template thiếu token mà file cũ có
    # thì kết quả vẫn dùng được — cái phải chặn là file ĐÍCH thiếu webapp/token.
    if not (merged.get("webappUrl") or merged.get("TL_WEBAPP")) or not (merged.get("token") or merged.get("TL_TOKEN")):
        raise ValueError("Thiếu webappUrl/token trong config")
    _old_profiles = sorted((old.get("profiles") or {}).keys()) if isinstance(old.get("profiles"), dict) else []
    backup = None
    if path.is_file():
        try:
            _bkp = _config_backup_dir() / f"{path.name}.init-config.{time.strftime('%Y%m%dT%H%M%S')}.bak.json"
            shutil.copyfile(str(path), str(_bkp))    # copy BYTE — giữ nguyên cả file cũ không parse được
            backup = str(_bkp)
        except BackupTrongCaySkill:   # v1.36.69 (#972): KHÔNG ghi đè config khi không backup được ra ngoài cây
            raise
        except Exception:  # noqa: BLE001
            backup = None
    _write_json_atomic(path, merged)
    info = {"merged": not replace, "replaced": bool(replace), "backup": backup,
            "profiles_giu": _old_profiles,
            "profiles_sau": sorted((merged.get("profiles") or {}).keys()) if isinstance(merged.get("profiles"), dict) else []}
    return path, info


def public_download_text(fid: str, timeout: int = 180) -> str | None:
    """Tải file PUBLIC (anyone-with-link) từ Drive qua drive.usercontent → text. None nếu lỗi/không public.
    Dùng cho config + creds ở Package (CONFIG_PUBLIC). Trả về None nếu nhận trang HTML login (file chưa public)."""
    import urllib.request as _u
    url = f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t"
    try:
        with _u.urlopen(url, timeout=timeout) as r:
            data = r.read()
    except Exception:  # noqa: BLE001
        return None
    txt = data.decode("utf-8", "replace")
    low = txt.lstrip()[:512].lower()
    if low.startswith("<!doctype html") or "<html" in low[:64] or "accounts.google.com" in txt[:2048]:
        return None   # trang login → file CHƯA public (anyone-with-link) → caller fallback Drive MCP
    return txt


def _skill_package_integrity(root: str | os.PathLike | None = None) -> dict:
    """v1.33.23: kiểm nhanh package skill trong Cowork/Code có bị mount cắt cụt/NUL/SyntaxError không.
    Không thay thế verify-integrity đầy đủ; đây là canary rẻ để doctor/cowork-plan chỉ rõ: nếu core hỏng thì phải
    curl/unzip bản zip sạch từ Drive thay vì chạy trực tiếp file mount. Trả JSON thuần để test offline."""
    base = Path(root) if root else HERE
    core = ["tl.py", "tl_gws.py", "nlm_cli.py", "transport.py", "gas.py", "boot.py", "contract_check.py",
            # v1.33.56 (review tl_core/F3): tl_core = điểm-chết-đơn sau Pha B/C — NUL-pad 1 file là sập CẢ CLI
            "tl_core/__init__.py", "tl_core/deterministic.py", "tl_core/jsonio.py",
            "tl_core/workflow.py", "tl_core/release.py", "tl_core/live.py",
            "tl_core/zip_ingest.py", "tl_core/ocr.py", "tl_core/chunking.py",
            "tl_core/command_registry.py",   # Pha D v1.33.57 + Pha E v1.33.58
            "tl_core/hygiene.py",
            "tl_core/nlm_ops.py",
            "tl_core/extract_cache.py", "tl_core/fetch_web.py", "tl_core/profile_mgmt.py",
            "tl_core/ingest_ops.py",
            "tl_core/lookup_ops.py",
            "tl_core/ops_misc.py",
            "tl_core/classify.py", "tl_core/profile_env.py",
            "tl_core/resolve.py", "tl_core/regio.py", "tl_core/cli.py"]   # I1..I11
    optional = ["backfill_keywords_live.py", "backfill_nlm_title.py", "registry_orchestrator.py",
                "tra_cuu.py", "vb_status.py", "vbhn_query.py"]
    rows, bad = [], []
    def _one(fn: str, required: bool) -> dict:
        path = base / fn
        if not path.exists() and (base / "_fallback" / fn).exists():
            path = base / "_fallback" / fn
        rel = str(path.relative_to(base)) if path.exists() else fn
        r = {"file": fn, "path": rel, "required": required, "exists": path.exists(), "bytes": 0, "ok": False, "error": ""}
        if not path.exists():
            r["error"] = "missing"
        else:
            try:
                data = path.read_bytes()
                r["bytes"] = len(data)
                if b"\x00" in data:
                    raise ValueError("NUL byte trong file — dấu hiệu mount cắt cụt/hỏng")
                txt = data.decode("utf-8", "replace")
                compile(txt, str(path), "exec")
                # File python gần-rỗng là dấu hiệu zip/mount lỗi; ngưỡng cố ý thấp để không false alarm helper nhỏ.
                if required and len(data) < 200:
                    raise ValueError("file core quá ngắn")
                r["ok"] = True
            except Exception as e:  # noqa: BLE001
                r["error"] = f"{type(e).__name__}: {e}"
        return r
    for fn in core:
        r = _one(fn, True); rows.append(r)
        if not r["ok"]: bad.append(r)
    opt_bad = []
    for fn in optional:
        r = _one(fn, False); rows.append(r)
        if r["exists"] and not r["ok"]: opt_bad.append(r)
    ok = not bad
    note = ("package core OK" if ok else
            "package core HỎNG/cắt cụt — đừng chạy file mount; tải zip sạch từ Drive rồi unzip vào thư mục ghi được")
    return {"ok": ok, "core_bad": bad, "optional_bad": opt_bad, "files": rows, "note": note}


def _ensure_gws_nlm(want_binary: bool, want_nlm: bool, config=None, profile=None, env=None) -> dict:
    """Best-effort nạp 'một cụm phải đi cùng nhau': gws CRED (direct-media ĐỌC) + (want_binary) gws BINARY (find/GHI) +
    (want_nlm) nlm CLI + auth. Giả định TL_TOKEN/TL_WEBAPP đã ở env. IDEMPOTENT (binary bỏ qua nếu đã có; nlm bỏ qua nếu cài).
    Dùng CHUNG bởi `init-config --from-public` và `tl up`. Trả {gws_cred,gws_binary,nlm,nlm_auth}.
    v1.33.23: Cowork có trần ~45s/lệnh, nên KHÔNG gọi cài nlm trọn gói từ `tl up --nlm`; chỉ chạy 1 bước
    `nlm-install --resume` rồi báo PARTIAL để người vận hành lặp lại, tránh timeout làm bootstrap chết giữa chừng."""
    st = {"gws_cred": None, "gws_binary": None, "nlm": None, "nlm_auth": None,
          "nlm_partial": False, "nlm_next": ""}
    tok = os.environ.get("TL_TOKEN"); url = os.environ.get("TL_WEBAPP")
    if tok and url:
        try:
            ok, _m = _imp("tl_gws")._gws_auth_load(tok, GWS_CRED_FILEID)
            st["gws_cred"] = bool(ok)
            if ok and want_binary:
                try:
                    rc = _imp("tl_gws").cmd_gws_bootstrap_cowork(argparse.Namespace(
                        file_id=None, md5=None, bindir=None, local_tgz=None, no_auth=True, force=False,
                        cred_file_id=None, config=config, profile=profile, env=env))
                    st["gws_binary"] = (rc == 0)
                except Exception:  # noqa: BLE001
                    st["gws_binary"] = False
        except Exception:  # noqa: BLE001
            st["gws_cred"] = False
    if want_nlm:
        try:
            try:
                rt_env = _imp("transport").runtime_env(env)
            except Exception:
                rt_env = str(env or "")
            cowork = (rt_env == "cowork")
            rc = _imp("tl_gws").cmd_nlm_install(argparse.Namespace(
                uv=(not cowork), resume=cowork, version=None, py_file_id=None,
                env=env, config=config, profile=profile, no_nlm=False))
            st["nlm"] = (rc == 0)
            st["nlm_partial"] = (rc == 3)
            if st["nlm_partial"]:
                st["nlm_next"] = "tl nlm-install --resume"
            if st["nlm"]:
                try:
                    ra = _imp("tl_gws").cmd_nlm_auth_load(argparse.Namespace(cred_file_id=None, config=config, profile=profile, env=env))
                    st["nlm_auth"] = (ra == 0)
                except Exception:  # noqa: BLE001
                    st["nlm_auth"] = False
            else:
                st["nlm_auth"] = False
        except Exception:  # noqa: BLE001
            st["nlm"] = False
    return st


def cmd_init_config(a) -> int:
    """Khởi tạo ~/.tra_luat_config.json cho phiên TRỐNG. Nguồn (theo thứ tự):
      --from-public       : curl CONFIG_FILEID PUBLIC (drive.usercontent) — KHÔNG cần Drive MCP/token (đường mặc định nay).
      --file <path>       : đọc JSON config agent đã tải (Drive MCP) từ file → ghi config (đường GAS-only, KHÔNG cần master key).
      --from-drive        : tự tải CONFIG_FILEID bằng direct-media (CHỈ khi đã có gws cred).
      --config-json/-webapp/-token : truyền trực tiếp."""
    config_json = getattr(a, "config_json", None)
    if getattr(a, "from_public", False):
        fid = getattr(a, "file_id", None) or CONFIG_FILEID
        config_json = public_download_text(fid)
        if not config_json:
            print(f"[tl] init-config --from-public: KHÔNG curl được config public (fileId={fid}).\n"
                  f"  → file chưa 'anyone-with-link'? Chạy script set-public, hoặc fallback Drive MCP → `--file`.", file=sys.stderr)
            return 2
    elif getattr(a, "file", None):
        try:
            config_json = Path(a.file).read_text(encoding="utf-8")
        except Exception as e:  # noqa: BLE001
            print(f"[tl] init-config: không đọc được --file {a.file}: {e}", file=sys.stderr); return 1
    elif getattr(a, "from_drive", False):
        fid = getattr(a, "file_id", None) or CONFIG_FILEID
        import tempfile as _tf
        try:
            with _tf.TemporaryDirectory() as _d:
                _dst = os.path.join(_d, "cfg.json")
                r = _imp("transport").drive_op("download", env=getattr(a, "env", None), file_id=fid, dest=_dst)
                config_json = open(_dst, encoding="utf-8").read() if (isinstance(r, dict) and r.get("ok")) else None
        except Exception as e:  # noqa: BLE001
            config_json = None
            print(f"[tl] init-config --from-drive lỗi ({e}); cần gws cred. Dùng --file sau khi tải qua Drive MCP.", file=sys.stderr)
        if not config_json:
            print(f"[tl] init-config: không tải được config (fileId={fid}). Phiên trống: agent tải qua Drive MCP → "
                  f"`tl init-config --file <path>`.", file=sys.stderr)
            return 2
    # AUTO-HEAL (sự cố 2026-06-30): template public hay set registryDocId = Doc legacy 1mATG → webapp mở Doc-as-Sheet →
    # đọc registry RỖNG (count=0 ẢO). Blank nó (base + mọi profile) → webapp auto-discover Sheet `tra_luat_registry` THẬT.
    # r280: phép heal nay nằm TRONG save_local_config, chạy trên bản ĐÃ HOÀ (template + file cũ) — heal riêng
    # template thì id legacy có sẵn trong file cũ sẽ sống sót qua merge. Ở đây chỉ còn phần BÁO cho người dùng.
    if config_json:
        try:
            import json as _jh
            _cj = _jh.loads(config_json)
            if _heal_legacy_registry_doc_id(dict(_cj)):
                print("[tl] ⚠ init-config AUTO-HEAL: registryDocId = Doc legacy 1mATG → ĐỂ RỖNG (webapp auto-discover "
                      "Sheet tra_luat_registry THẬT). Nên cập nhật template public để hết tái diễn.", file=sys.stderr)
        except Exception:  # noqa: BLE001
            pass
    try:
        path, _cfg_info = save_local_config(config_json, a.webapp, a.token, a.manifest_id, a.out,
                                            replace=getattr(a, "replace", False))
    except BackupTrongCaySkill as e:   # v1.36.69 (#972): config CHƯA bị ghi
        print(_json_dumps({"ok": False, "error": "CONFIG_BACKUP_TRONG_CAY_SKILL", "detail": str(e),
                           "note": "CHƯA ghi config. Đặt TL_CONFIG_BACKUP_DIR ra NGOÀI cây skill rồi chạy lại."}),
              file=sys.stderr)
        return 2
    except Exception as e:  # noqa: BLE001
        print(f"[tl] init-config lỗi: {e}", file=sys.stderr); return 1
    # r280 (P16-F01): NÓI RA đã giữ/xoá gì — im lặng chính là cách bản cũ làm mất block profiles.
    _giu = _cfg_info.get("profiles_giu") or []
    if _cfg_info.get("replaced"):
        if _giu:
            print(f"[tl] ⚠ init-config --replace: GHI ĐÈ TRỌN — {len(_giu)} block profiles bị XOÁ "
                  f"({', '.join(_giu)}). Khôi phục: {_cfg_info.get('backup') or '(không backup được)'}", file=sys.stderr)
    elif _giu:
        print(f"[tl] init-config: HOÀ vào config có sẵn — giữ {len(_giu)} block profiles ({', '.join(_giu)})"
              + (f"; backup {_cfg_info.get('backup')}" if _cfg_info.get("backup") else ""), file=sys.stderr)
    # FIX (log Chat): --from-public GỘP gws CRED + BINARY (find/GHI) + (--nlm) nlm — qua `_ensure_gws_nlm` (dùng chung `tl up`).
    _from_public = getattr(a, "from_public", False)
    note = ""
    if not getattr(a, "no_gws", False):
        try:
            import json as _json
            _cfg = _json.loads(config_json) if config_json else {}
            _tok = _cfg.get("token") or getattr(a, "token", None) or os.environ.get("TL_TOKEN")
            _url = _cfg.get("webappUrl") or _cfg.get("TL_WEBAPP") or getattr(a, "webapp", None) or os.environ.get("TL_WEBAPP")
            if _tok and _url:
                os.environ["TL_TOKEN"] = _tok; os.environ["TL_WEBAPP"] = _url
                st = _ensure_gws_nlm(want_binary=_from_public and not getattr(a, "no_binary", False),
                                     want_nlm=getattr(a, "nlm", False) and _from_public,
                                     config=getattr(a, "config", None), profile=getattr(a, "profile", None), env=getattr(a, "env", None))
                note = _gws_nlm_note(st)
        except Exception as e:  # noqa: BLE001
            note = f" · gws chưa bật ({type(e).__name__})"
    print(f"✓ đã lưu config: {path}{note} — chạy `tl ping`."
          + ("" if "binary ✓" in note else "  (binary: `tl gws-bootstrap-cowork`; nlm: thêm `--nlm`)"))
    return 0


def cmd_up(a) -> int:
    """BOOTSTRAP TẤT ĐỊNH 1-LỆNH (tăng tính tất định/ổn định): config → gws cred+binary → nlm (--nlm) → manifest → tóm tắt
    readiness. Mỗi bước IDEMPOTENT + best-effort, in trạng thái từng phần. Thay việc chain tay nhiều lệnh.
    Exit: 0 = lõi sẵn sàng (config + manifest), 1 = lõi thiếu (xem bước ✗)."""
    steps = []
    jsonout = getattr(a, "json", False)
    def rec(name, ok, detail=""):
        steps.append({"step": name, "ok": (None if ok is None else bool(ok)), "detail": detail})
        if not jsonout:
            mark = "•" if ok is None else ("✓" if ok else "✗")
            print(f"  {mark} {name}" + (f" — {detail}" if detail else ""))
    if not jsonout:
        print("== tl up — bootstrap tất định ==")
    # 1) CONFIG (env/file; thiếu → init-config --from-public, GỘP gws+nlm luôn)
    try:
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    except (SystemExit, Exception):  # noqa: BLE001  — load_creds sys.exit() khi thiếu cred → KHÔNG được giết tl up; rơi xuống nhánh auto-fetch
        pass
    cfg_ok = bool(os.environ.get("TL_WEBAPP") and os.environ.get("TL_TOKEN"))
    if not cfg_ok and not getattr(a, "no_config_fetch", False):
        try:
            rc = cmd_init_config(argparse.Namespace(
                from_public=True, file=None, file_id=None, from_drive=False, config_json=None, webapp=None, token=None,
                manifest_id=None, out=None, no_gws=False, no_binary=getattr(a, "no_binary", False),
                nlm=getattr(a, "nlm", False), config=getattr(a, "config", None), profile=getattr(a, "profile", None),
                env=getattr(a, "env", None)))
            cfg_ok = bool(os.environ.get("TL_WEBAPP") and os.environ.get("TL_TOKEN")) and rc == 0
            rec("config (init-config --from-public)", cfg_ok)
        except Exception as e:  # noqa: BLE001
            rec("config", False, f"init-config lỗi: {type(e).__name__}")
    else:
        rec("config", cfg_ok, "đã có TL_WEBAPP/TL_TOKEN" if cfg_ok else "thiếu cred (offline?)")
    # 2/3) gws cred + binary + nlm — idempotent (init-config có thể đã làm; gọi lại để CHẮC + báo trạng thái)
    if cfg_ok:
        st = _ensure_gws_nlm(want_binary=not getattr(a, "no_binary", False), want_nlm=getattr(a, "nlm", False),
                             config=getattr(a, "config", None), profile=getattr(a, "profile", None), env=getattr(a, "env", None))
        rec("gws cred (direct-media đọc)", st.get("gws_cred"))
        rec("gws binary (find/ghi)", st.get("gws_binary"), "" if st.get("gws_binary") else "find/ghi sẽ đi GAS")
        if getattr(a, "nlm", False):
            if st.get("nlm_partial"):
                rec("nlm CLI", None, "PARTIAL do trần thời gian Cowork — chạy tiếp `tl nlm-install --resume` tới rc=0")
            else:
                rec("nlm CLI", st.get("nlm"), "auth ✓" if st.get("nlm_auth") else "auth chưa (`tl nlm-auth-load`/`nlm login`; gọi tay nên export PATH=$HOME/.local/bin:$PATH)")
    # 4) MANIFEST (nạp + cache offline)
    man_ok = False
    try:
        ents = _manifest_entries(refresh=getattr(a, "refresh", False))
        man_ok = len(ents) > 0
        rec("manifest", man_ok, f"{len(ents)} entries (cache offline)")
    except Exception as e:  # noqa: BLE001
        rec("manifest", False, f"{type(e).__name__}")
    core_ok = cfg_ok and man_ok
    if jsonout:
        print(json.dumps({"ok": core_ok, "ready": core_ok, "steps": steps}, ensure_ascii=False, indent=2))
    else:
        print(f"  → {'SẴN SÀNG (lõi: config+manifest).' if core_ok else 'CHƯA đủ lõi — xem bước ✗.'}"
              + ("  Chẩn đoán đầy đủ: `tl doctor`." if core_ok else ""))
    return 0 if core_ok else 1


def cmd_precheck(a) -> int:
    """(Pha 0) Kiểm BẤT BIẾN TRƯỚC KHI GHI (write-safety) — gom guard chống 18 sự cố: registryDocId≠Doc-legacy,
    profile-registryDocId≠rỗng (chống CLOBBER 766 dòng), snapshot manifest đủ tươi (GAS cache ~600s), (tùy chọn) --cols
    ∈ schema (chống 'so_hieu'≠'sohieu' bị bỏ im lặng). READ-ONLY, KHÔNG ghi gì. rc=1 nếu có critical blocker. Pha 1 sẽ
    nhúng vào mọi `--apply`. (KHÁC lệnh `preflight` = định tuyến sharding NLM.)"""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    active = _active_profile()
    is_base = (active == DEFAULT_PROFILE)
    rid = (os.environ.get("TL_REGISTRY_DOC_ID") or "").strip()
    snapshot_age = None
    try:
        import time as _t
        _p = _cache_file("manifest.json")
        if _p.exists():
            snapshot_age = _t.time() - _p.stat().st_mtime
    except Exception:
        snapshot_age = None
    state = {"registryDocId": rid, "is_base_profile": is_base,
             "profile_registry_id": rid,   # profile đang active → registryDocId của nó chính là TL_REGISTRY_DOC_ID
             "snapshot_age_seconds": snapshot_age,
             "write_cols": getattr(a, "cols", None)}
    checks = _preflight_invariants(state)
    verdict = _preflight_verdict(checks)
    out = {"ok": verdict["ok"], "gate": "preflight", "profile": active, "is_base_profile": is_base,
           "registryDocId": rid or "(rỗng → auto-discover)", "snapshot_age_seconds": None if snapshot_age is None else int(snapshot_age),
           "checks": checks, "blockers": verdict["blockers"], "warnings": verdict["warnings"]}
    # R1 (--gws-live): ĐỌC registry Sheet LIVE qua gws + báo DRIFT so với manifest (read-only, opt-in — KHÔNG thêm
    # độ trễ/lỗi vào cổng --apply mặc định). Phát hiện manifest cũ (chưa manifest_export) so với sheet nguồn thật.
    if getattr(a, "gws_live", False):
        gl = {"attempted": True}
        try:
            _tlg = _imp("tl_gws")
            rows = _tlg._gws_read_registry_rows(rid, REGISTRY_SCHEMA_COLS) if rid else None
            if rows is None:
                gl.update({"ok": False, "note": "gws Sheets không đọc được (thiếu cred/binary, hoặc registryDocId "
                           "rỗng/không-phải-Sheet) → hệ thống dùng GAS/manifest như cũ (an toàn)."})
            else:
                man_n = None
                try:
                    man_n = len(_manifest_entries(refresh=False))
                except Exception:
                    man_n = None
                gl.update({"ok": True, "sheet_rows_live": len(rows), "manifest_entries": man_n,
                           "drift": (None if man_n is None else len(rows) - man_n)})
        except Exception as e:  # noqa: BLE001
            gl.update({"ok": False, "error": f"{type(e).__name__}: {e}"})
        out["gws_live"] = gl
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"== precheck (write-safety) · profile={active} · {'BASE' if is_base else 'DỰ ÁN'} · registry={rid[:16] or '(rỗng)'} ==")
        for c in checks:
            mark = "✓" if c["ok"] else ("⛔" if c["severity"] == "critical" else "⚠")
            print(f"  {mark} {c['name']}: {c['detail']}")
        if verdict["blockers"]:
            print(f"  ⛔ BLOCKER: {', '.join(verdict['blockers'])} → SỬA TRƯỚC khi --apply (Pha 1 sẽ chặn cứng).")
        else:
            print("  ✓ Không có blocker — an toàn để ghi.")
        gl = out.get("gws_live")
        if gl:
            if gl.get("ok"):
                dr = gl.get("drift")
                print(f"  ℹ gws-live: sheet={gl.get('sheet_rows_live')} dòng · manifest={gl.get('manifest_entries')}"
                      f" · drift={dr}" + ("  ⚠ manifest LỆCH sheet → `tl boot --refresh`/manifest_export" if dr else ""))
            else:
                print(f"  ℹ gws-live: {gl.get('note') or gl.get('error')}")
    return 0 if verdict["ok"] else 1


def cmd_journal(a) -> int:
    """(Pha 0) Xem/soi nhật ký WAL (`TL_JOURNAL_DIR` hoặc `TL_CACHE_DIR/_journal`, mặc định `~/.tl_journal`) — liệt kê run, hoặc trạng thái resume 1 run (done/inflight)
    + kế hoạch undo. READ-ONLY trừ `--close` (S7 v1.33.44: SELF-HEAL inflight đã được lệnh khác hoàn tất — đối chiếu
    intent.set với registry hiện tại, khớp hết → append commit healed; chỉ ghi vào FILE JOURNAL local, không đụng remote).
    Sửa/hoàn tác qua `tl resume <run>` / `tl undo <run>` (Pha 2)."""
    run_id = getattr(a, "run_id", None)
    if not run_id:
        runs = []
        try:
            d = _journal_dir()
            if d.exists():
                runs = sorted([p.stem for p in d.glob("*.jsonl")])
        except Exception:
            runs = []
        if getattr(a, "json", False):
            print(json.dumps({"ok": True, "runs": runs}, ensure_ascii=False, indent=2))
        else:
            print(f"== journal: {len(runs)} run ==")
            for r in runs[-30:]:
                print(f"  - {r}")
            print("  → `tl journal <run_id>` để xem done/inflight/undo.")
        return 0
    recs = _journal_read(run_id)
    if not recs:
        print(f"[tl] journal: không có bản ghi cho run '{run_id}'.", file=sys.stderr); return 1
    st = _journal_resume_state(recs)
    # S7 (v1.33.44 — log 7A): `--close` = SELF-HEAL inflight khi việc đã được LỆNH KHÁC hoàn tất (vd đứt trước
    # reg_link rồi vá tay nlm-add + register): đối chiếu `set` của intent với registry HIỆN TẠI (manifest offline)
    # — khớp hết → append commit healed (resume/undo hết coi là dở). Không khớp → giữ inflight (ép: --force).
    # Manifest có thể stale (GAS cache ~600s) → `tl boot --refresh` trước khi close nếu vừa vá xong.
    if getattr(a, "close", False):
        if not st["inflight"]:
            print(json.dumps({"ok": True, "run_id": run_id, "closed": 0,
                              "note": "không có op inflight — journal đã sạch, không cần --close"}, ensure_ascii=False))
            return 0
        try:
            apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
            _ents = {_entry_drive_id(e2): e2 for e2 in _manifest_entries(refresh=getattr(a, "refresh", False))}
        except Exception as _ce:  # noqa: BLE001
            print(f"[tl] journal --close: cần manifest để verify ({_ce}) — chạy `tl boot` trước.", file=sys.stderr)
            return 2
        cp = _journal_close_plan(recs, _ents)
        _to_close = cp["healable"] + (cp["blocked"] if getattr(a, "force", False) else [])
        for it in _to_close:
            _journal_append(run_id, {"t": "commit", "op": it.get("op"), "key": it.get("key"), "ok": True,
                                     "verify": {"healed": True, "via": ("journal --close --force" if it in cp["blocked"]
                                                                        else "journal --close (registry match)")}})
        if _to_close and (getattr(a, "force", False) or not cp["blocked"]):
            _journal_append(run_id, {"t": "run_end", "ok": True, "healed": True})
        print(json.dumps({"ok": True, "run_id": run_id, "closed": len(_to_close),
                          "healable": cp["healable"], "blocked_remaining": (cp["blocked"] if not getattr(a, "force", False) else []),
                          "note": ("blocked = giá trị intent CHƯA khớp registry (việc chưa xong thật / manifest stale — "
                                   "`tl boot --refresh` rồi thử lại; chắc chắn đã verify tay: --close --force)"
                                   if (cp["blocked"] and not getattr(a, "force", False)) else "inflight đã đóng (healed)")},
                         ensure_ascii=False, indent=2))
        return 0 if not (cp["blocked"] and not getattr(a, "force", False)) else 1
    undo = _journal_undo_ops(recs)
    out = {"ok": True, "run_id": st["run_id"] or run_id, "cmd": st["cmd"], "counts": st["counts"],
           "done_keys": st["done_keys"][:30], "inflight": [iv.get("key") for iv in st["inflight"]][:30],
           "undo_ops": len(undo)}
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"== journal {run_id} · cmd={st['cmd']} · done={st['counts']['done']} inflight={st['counts']['inflight']} ==")
        if st["inflight"]:
            print(f"  ⚠ INFLIGHT (ghi intent chưa commit-ok — cần VERIFY remote): {[iv.get('key') for iv in st['inflight']][:10]}")
            print(f"    → việc đã được lệnh KHÁC hoàn tất? `tl journal {run_id} --close` (đối chiếu registry rồi tự đóng — S7 v1.33.44)")
        print(f"  undo khả dụng: {len(undo)} op reversible (Pha 2: `tl undo {run_id}`).")
    return 0


def _journal_reapply_one(new_run: str, g, op: dict, values: dict) -> dict:
    """Ghi LẠI 1 op (undo restore / resume reapply). Dùng reg_upsert khi: op gốc là reg_upsert HOẶC write chạm cột IMMUTABLE
    (sohieu/goc — reg_bulk bỏ im lặng khi ĐỔI giá trị đã có → review#2: undo/resume qua reg_bulk sẽ NO-OP âm thầm). Ngược lại
    reg_bulk (giữ được key_field ≠ drive_id, vd nlm-reconcile backfill keyed nlm_source_id). values = before (undo) / set (resume)."""
    key = op.get("key"); kf = op.get("key_field", "drive_id"); cols = op.get("cols") or ",".join(values.keys())
    orig = op.get("orig_op") or op.get("op")
    if orig == "reg_upsert" or (set(values.keys()) & _IMMUTABLE_UPSERT_COLS):
        return _journaled_reg_upsert(new_run, g, {"drive_id": key, **values})
    return _journaled_reg_write(new_run, g, [{kf: key, **values}], cols, key_field=kf)


def cmd_undo(a) -> int:
    """(Pha 2) HOÀN TÁC ghi registry của 1 run (đọc WAL journal): khôi phục giá trị `before` các dòng ĐÃ commit-ok reversible
    (đúng loại reg_upsert/reg_bulk gốc). CHỈ registry — xóa NLM/Drive/reg_clear KHÔNG undo được. DRY mặc định; --apply --confirm yes."""
    run_id = getattr(a, "run_id", None)
    recs = _journal_read(run_id) if run_id else []
    if not recs:
        print(f"[tl] undo: không có journal cho run '{run_id}'.", file=sys.stderr); return 2
    undo = _journal_undo_ops(recs)
    if not undo:
        print(json.dumps({"ok": True, "run_id": run_id, "undo_ops": 0,
                          "note": "Không có op reversible (chưa commit-ok / không có `before` / op không đảo được như reg_clear/xóa NLM)."},
                         ensure_ascii=False, indent=2)); return 0
    if not getattr(a, "apply", False):
        print(json.dumps({"ok": True, "mode": "DRY", "run_id": run_id, "undo_ops": len(undo),
                          "sample": [{"key": o["key"], "key_field": o["key_field"], "orig_op": o["orig_op"], "restore": o["before"]} for o in undo[:20]],
                          "note": "--apply --confirm yes để KHÔI PHỤC giá trị cũ (theo `before`). ⚠ Xóa NLM/Drive KHÔNG undo được (chỉ registry)."},
                         ensure_ascii=False, indent=2)); return 0
    if getattr(a, "confirm", None) != "yes":
        print(json.dumps({"ok": False, "error": "NEED_CONFIRM", "note": "undo GHI ĐÈ registry về giá trị cũ — thêm `--confirm yes`."},
                         ensure_ascii=False, indent=2), file=sys.stderr); return 2
    _ok_gate, _ = _apply_gate(a)
    if not _ok_gate:
        return 2
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    g = _gas()
    undo_run = _apply_journal_start("undo", {"of_run": run_id, "ops": len(undo)})
    ok_n, fail_n = 0, 0
    for o in undo:
        v = _journal_reapply_one(undo_run, g, o, o["before"])
        if v.get("verified"):
            ok_n += 1
        else:
            fail_n += 1
        print(f"  ↩ restore {o['key'][:16]:16s} {o['before']}  {'OK' if v.get('verified') else '⚠ '+str(v.get('error') or '')}", file=sys.stderr, flush=True)
    _journal_append(undo_run, {"t": "run_end", "ok": fail_n == 0, "counts": {"restored": ok_n, "failed": fail_n}})
    _invalidate_manifest_cache()
    print(json.dumps({"ok": fail_n == 0, "run_id": run_id, "restored": ok_n, "failed": fail_n, "undo_journal": undo_run,
                      "note": "Registry đã trả về `before`. `tl boot --refresh` để cache thấy. NLM/Drive (nếu có) KHÔNG tự hoàn."},
                     ensure_ascii=False, indent=2))
    return 0 if fail_n == 0 else 1


def cmd_resume(a) -> int:
    """(Pha 2) TIẾP TỤC 1 run bị ngắt (đọc WAL journal): LÀM LẠI các op DỞ (intent chưa commit-ok) bằng giá trị `set` đã lưu,
    ĐÚNG loại gốc. Idempotent (ghi lại giá trị đã định). CHỈ registry — NLM `source_add` do CHẠY LẠI lệnh gốc (live-dedup lo trùng).
    DRY mặc định; --apply ghi."""
    run_id = getattr(a, "run_id", None)
    recs = _journal_read(run_id) if run_id else []
    if not recs:
        print(f"[tl] resume: không có journal cho run '{run_id}'.", file=sys.stderr); return 2
    st = _journal_resume_state(recs)
    ops = _journal_resume_ops(recs)
    if not ops:
        print(json.dumps({"ok": True, "run_id": run_id, "done": st["counts"]["done"], "inflight": 0,
                          "note": "Không có op dở để làm lại (run đã xong, hoặc op dở không có `set`). Nạp NLM thiếu: chạy lại lệnh gốc."},
                         ensure_ascii=False, indent=2)); return 0
    if not getattr(a, "apply", False):
        print(json.dumps({"ok": True, "mode": "DRY", "run_id": run_id, "done": st["counts"]["done"], "inflight": len(ops),
                          "sample": [{"key": o["key"], "op": o["op"], "cols": o["cols"]} for o in ops[:20]],
                          "note": "--apply để LÀM LẠI op dở (ghi lại `set`, idempotent). NLM source_add: chạy lại lệnh gốc (vd ingest-missing)."},
                         ensure_ascii=False, indent=2)); return 0
    _ok_gate, _ = _apply_gate(a)
    if not _ok_gate:
        return 2
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    g = _gas()
    resume_run = _apply_journal_start("resume", {"of_run": run_id, "ops": len(ops)})
    ok_n, fail_n = 0, 0
    for o in ops:
        v = _journal_reapply_one(resume_run, g, o, o["set"])
        if v.get("verified"):
            ok_n += 1
        else:
            fail_n += 1
        print(f"  ▶ reapply {o['key'][:16]:16s} {o['set']}  {'OK' if v.get('verified') else '⚠ '+str(v.get('error') or '')}", file=sys.stderr, flush=True)
    _journal_append(resume_run, {"t": "run_end", "ok": fail_n == 0, "counts": {"reapplied": ok_n, "failed": fail_n}})
    _invalidate_manifest_cache()
    print(json.dumps({"ok": fail_n == 0, "run_id": run_id, "reapplied": ok_n, "failed": fail_n, "resume_journal": resume_run,
                      "note": "Op dở đã ghi lại. Nạp NLM thiếu: chạy lại lệnh gốc. `tl boot --refresh` để cache thấy."},
                     ensure_ascii=False, indent=2))
    return 0 if fail_n == 0 else 1


def _doctor_exporttext_probe(g, entries: list[dict]) -> dict:
    """MERGE Codex: probe `exporttext` TRỰC TIẾP (cố ý KHÔNG qua _read_doc_text gws-first) để bắt đúng ca
    webapp ping XANH nhưng UrlFetchApp.fetch/exporttext chết vì deployment thiếu scope script.external_request
    — bổ trợ cho GWS-FIRST v1.33.10 (client sống bằng direct-media nhưng fallback GAS vẫn phải được chẩn đúng)."""
    e = _doctor_exporttext_probe_target(entries)
    if not e:
        return {"ok": True, "skipped": True, "detail": "không có GDoc target trong manifest cache để probe exporttext"}
    did = _entry_drive_id(e)
    try:
        r = g.get("exporttext", fileId=did)
    except Exception as ex:  # noqa: BLE001
        return {"ok": False, "drive_id": did, "detail": f"{type(ex).__name__}: {ex}"}
    ok = (r.get("ok") is not False) and bool((r.get("text") or "") or int(r.get("chars") or 0))
    if ok:
        return {"ok": True, "drive_id": did, "detail": f"chars={r.get('chars') or len(r.get('text') or '')}"}
    raw = json.dumps(r, ensure_ascii=False)[:500]
    hint = ""
    if "script.external_request" in raw or "UrlFetchApp.fetch" in raw:
        hint = (" — thiếu OAuth scope script.external_request: cập nhật appsscript.json theo "
                "references/APPSSCRIPT_MANIFEST.open-egress.json, RUN một hàm trong editor để re-authorize, rồi Deploy New version.")
    return {"ok": False, "drive_id": did, "detail": raw + hint}


def _drift_hint_lines(bd: dict, nb: str) -> list[str]:
    """r232 (PURE): dòng GỢI Ý cho cảnh báo drift registry↔NLM của doctor — tách khỏi chỗ in để test
    được, và để gợi ý KHỚP đúng thứ `nlm-reconcile --apply` THẬT SỰ ghi được.

    Bug đo 29-07-2026: doctor in MỘT câu duy nhất «đồng bộ 1 bước: `tl nlm-reconcile <nb> --apply`»
    cho MỌI kiểu drift. Đo trên kho thật: breakdown = NLM_STATUS_MISMATCH 0 · CORPUS_TRUE_NOT_ON_NLM
    53 · NLM_NOTEBOOK_ID_MISSING 0; DRY của reconcile trên CẢ notebook nền LẪN notebook overflow đều
    cho backfill=0 · link=0 · desync=0 ⇒ `--apply` ghi ĐÚNG 0 DÒNG. Người vận hành làm theo gợi ý sẽ
    tin đã sửa xong trong khi không có gì đổi — đúng lớp bẫy nguy hiểm nhất (câu đọc như hướng dẫn
    vận hành), cùng họ với bẫy «`nlm login` là đủ» đã bị bác ở GOTCHAS §9.

    Lý do CẤU TRÚC (không phải ngẫu nhiên theo dữ liệu): reconcile chỉ ghi cho dòng THIẾU
    nlm_notebook_id/nlm_source_id (tập backfill/link). `CORPUS_TRUE_NOT_ON_NLM` là NỢ PHỦ — nguồn
    CHƯA CÓ MẶT trên NLM; không lệnh registry nào tạo ra nguồn, nên `--apply` không thể chạm tới."""
    out: list[str] = []
    _fix = int(bd.get("NLM_NOTEBOOK_ID_MISSING") or 0) + int(bd.get("NLM_STATUS_MISMATCH") or 0)
    if _fix:
        out.append(f"     {_fix} mục chữa được 1 bước: `tl nlm-reconcile {nb} --apply` "
                   "(backfill nlm_notebook_id + link gdoc↔source_id; gợi ý, KHÔNG chặn).")
    _gap = int(bd.get("CORPUS_TRUE_NOT_ON_NLM") or 0)
    if _gap:
        out.append(f"     {_gap} mục CORPUS_TRUE_NOT_ON_NLM = NỢ PHỦ (nguồn CHƯA có mặt trên NLM) — "
                   "`nlm-reconcile --apply` KHÔNG chạm tới: nó chỉ điền trường cho dòng ĐÃ có nguồn. "
                   f"Soi bằng `tl slot-audit --notebook-id {nb}`; đẩy nguồn bằng `tl ingest-missing`.")
    return out


def _doc_dep_probe() -> list:
    """r319 — PURE-đọc: phụ thuộc NGOÀI thư viện chuẩn của đường NẠP tài liệu, kèm HẬU QUẢ cụ thể.

    Vì sao cần: `requirements.txt` khai «uses only Python standard library» — đúng với overlay core
    (`tl.py`/`contract_check.py`) nhưng SAI với đường nạp (`ingest_to_cache`/`normalize_document`).
    Hệ quả đo được 02-08: máy cài sạch không có `pypdf` ⇒ `assert_pdf_not_scanned` không đo được lớp
    text ⇒ CHẶN mọi .pdf (r315). Trước r319 không lệnh nào nói ra điều đó trước khi đâm vào tường.

    `bat_buoc=True` = thiếu là CHẶN CỨNG một đường nạp; `False` = giảm chất lượng, vẫn chạy."""
    import shutil as _sh319
    import importlib.util as _ilu319
    loi_import = {}   # r337: tên module → "Lớp: thông điệp" khi CÓ MẶT mà import HỎNG

    def _co_mod(ten):
        try:
            __import__(ten)
            return True
        except KeyboardInterrupt:
            raise
        except BaseException as e:  # noqa: BLE001 — import hỏng cũng coi như không có
            # "CÓ MẶT nhưng import HỎNG" khác "THIẾU": pip/hook báo đủ mà vẫn hỏng thì lời
            # khuyên `pip install` là sai chỗ — người đọc cần biết LỚP lỗi để đi đúng hướng.
            try:
                co_mat = _ilu319.find_spec(ten) is not None
            except BaseException:  # noqa: BLE001 — find_spec cũng có thể nổ trên cây hỏng
                co_mat = False
            if co_mat:
                loi_import[ten] = f"{type(e).__name__}: {str(e)[:80]}"
            # r337 (đo 02-09-2026, container remote) — fix: `import pypdf` kéo `cryptography` 41.0.7
            # thiếu `cffi` ⇒ pyo3 ném `PanicException`, kế thừa BaseException chứ không phải Exception,
            # nên `except Exception` cũ để nó XUYÊN QUA và giết cả `tl doctor` ngay tại phép đo phụ
            # thuộc — một lệnh chẩn đoán chết vì một phép đo là lệnh vắng mặt đúng lúc cần nó nhất.
            # Import hỏng vì BẤT KỲ lý do gì đều là "không có" (cùng doctrine `launcher.py doctor`);
            # chỉ Ctrl-C được xuyên qua vì đó là ý người dùng, không phải trạng thái của module.
            return False

    # r349 — MỘT backend HỎNG mà backend KIA chạy thì đường PDF KHÔNG bị chặn, nên đừng
    # nói là bị chặn. Bản r337 tính `co` bằng `pypdf or pdfplumber` (đúng) nhưng vẫn in
    # `loi_import` (sai): `pypdf` hỏng + `pdfplumber` chạy ⇒ `co=True` mà hậu quả vẫn ghi
    # "MỌI .pdf bị chặn ... cài lại phụ thuộc". Một chẩn đoán tự mâu thuẫn thì đẩy người
    # đọc đi sai hướng — cùng doctrine với `codex login status` NÓI DỐI.
    _pdf_co = _co_mod("pypdf") or _co_mod("pdfplumber")
    if _pdf_co:
        # Còn đường chạy: chỉ NHẮC backend hỏng, không tuyên bố bị chặn.
        _pdf_hq = ("đường PDF vẫn chạy" + (
            " (nhưng " + "; ".join(f"{k} → {v}" for k, v in loi_import.items())
            + " — bản dự phòng đang gánh)" if loi_import else ""))
    elif loi_import:
        _pdf_hq = ("MỌI .pdf bị chặn (reason=pdf_probe_unavailable, r315). "
                   "CÓ MẶT nhưng import HỎNG ("
                   + "; ".join(f"{k} → {v}" for k, v in loi_import.items())
                   + ") — cài lại phụ thuộc: pip install -r requirements.txt")
    else:
        _pdf_hq = ("MỌI .pdf bị chặn (reason=pdf_probe_unavailable, r315). "
                   "Cài: pip install pypdf")
    return [
        {"ten": "pypdf|pdfplumber", "bat_buoc": True, "co": _pdf_co, "hau_qua": _pdf_hq},
        {"ten": "pdftotext (poppler-utils)", "bat_buoc": True,
         "co": bool(_sh319.which("pdftotext")),
         "hau_qua": "không bóc được text .pdf. Cài: apt-get install poppler-utils"},
        {"ten": "python-docx", "bat_buoc": False, "co": _co_mod("docx"),
         "hau_qua": "vẫn đọc .docx bằng nhánh bóc-tag (r317 đã hết rò trị đo DrawingML); "
                    "có lib thì cấu trúc đoạn/bảng sát bản gốc hơn"},
        {"ten": "antiword|catdoc", "bat_buoc": False,
         "co": bool(_sh319.which("antiword") or _sh319.which("catdoc")),
         "hau_qua": "không đọc được .doc CŨ (binary); .docx/.pdf không ảnh hưởng"},
    ]


def cmd_doctor(a) -> int:
    """Chẩn đoán phiên trống: script lõi (gốc HOẶC _fallback), optional, credential,
    API_CONTRACT↔tl EXPECT, webapp ping, (--deep) manifest_export + exporttext-scope probe. (--offline) bỏ phần webapp."""
    report = []
    _json = getattr(a, "json", False) or bool(getattr(a, "out", None))
    drift = {"total": 0, "breakdown": {}, "notebook": ""}
    def add(name, ok, detail=""):
        report.append((name, bool(ok), detail))
        if not _json:
            print(f"{'✓' if ok else '✗'} {name}{(' — ' + detail) if detail else ''}")
    topology_report = {"ok": None, "shards": 0, "row_kind_findings": 0, "config_findings": []}   # v1.34.49
    def _emit_json(rc):
        _emit_json_payload({"ok": rc == 0, "rc": rc,
                            "checks": [{"name": n, "ok": o, "detail": d} for n, o, d in report],
                            "registry_nlm_drift": drift, "topology": topology_report}, getattr(a, "out", None))
        return rc
    fb = HERE / "_fallback"
    def where(fn):
        if (HERE / fn).exists(): return "gốc"
        if (fb / fn).exists(): return "_fallback"
        return ""
    core = ["gas.py", "boot.py", "manifest_build.py", "preingest_gate.py", "contract_check.py", "tl.py"]
    for fn in core:
        w = where(fn); add(f"core {fn}", bool(w), w or "THIẾU cả gốc lẫn _fallback")
    integ = _skill_package_integrity(HERE)
    add("package integrity", integ.get("ok"), integ.get("note") or "")
    optional = ["backfill_keywords_live.py", "backfill_nlm_title.py", "rasoat_worksheet.py",
                "rasoat_phuluc.py", "registry_orchestrator.py", "tra_cuu.py", "vb_status.py", "vbhn_query.py"]
    missing_opt = [fn for fn in optional if not where(fn)]
    add("optional rasoat/backfill", not missing_opt,
        "đủ" if not missing_opt else f"thiếu {len(missing_opt)} (chỉ ảnh hưởng tl rasoat): {', '.join(missing_opt[:5])}")
    # r319: KHAI phụ thuộc NGOÀI stdlib của đường NẠP tài liệu. Trước đây không có chỗ nào nói ra:
    # `requirements.txt` khai "stdlib only" nên máy cài sạch KHÔNG có `pypdf` ⇒ MỌI .pdf bị chặn
    # (r315), mà người vận hành chỉ biết khi đã đâm vào tường giữa lượt nạp. Tên bắt đầu bằng
    # "optional" ⇒ báo ĐỎ to nhưng KHÔNG lật rc (đúng nếp `optional rasoat/backfill`): máy không
    # bao giờ nạp PDF vẫn xanh.
    _dep = _doc_dep_probe()
    _thieu_cung = [d for d in _dep if d["bat_buoc"] and not d["co"]]
    _thieu_mem = [d for d in _dep if not d["bat_buoc"] and not d["co"]]
    add("optional phụ thuộc nạp tài liệu", not _thieu_cung,
        "đủ" + (f" (thiếu tuỳ chọn: {', '.join(d['ten'] for d in _thieu_mem)})" if _thieu_mem else "")
        if not _thieu_cung else " · ".join(f"{d['ten']} THIẾU ⇒ {d['hau_qua']}" for d in _thieu_cung))
    cfg_paths = [Path(a.config)] if a.config else [Path.home()/".tra_luat_config.json", Path("/tmp/tra_luat_config.json")]
    cfg_hit = next((x for x in cfg_paths if x and x.exists()), None)
    env_ok = bool(os.environ.get("TL_WEBAPP") and os.environ.get("TL_TOKEN"))
    add("credential", env_ok or bool(cfg_hit), "env" if env_ok else (str(cfg_hit) if cfg_hit else "chưa có env/local config — dùng `tl init-config`"))
    # nlm CLI: nếu thiếu, mọi thao tác NLM rơi về MCP (chậm, dễ timeout) — báo rõ + cách cài (vá log Cowork: không kiểm nlm).
    # 2.2 (log rà): KHÔNG dùng `shutil.which('nlm')` trần (shell non-login Cowork thiếu ~/.local/bin trên PATH →
    # báo đỏ GIẢ dù nlm đã cài). Dùng nlm_cli.nlm_exe() (đã nối ~/.local/bin + user-base bin) → khớp lúc tl spawn nlm.
    nprobe = _nlm_probe_summary(getattr(a, "env", None))
    nlm_bin = nprobe.get("tl_nlm_path") or nprobe.get("shell_nlm_path")
    # A (log Cowork 2026-07-05): cookie ~19 ngày nạp không ai nhắc — doctor nay đọc tuổi cookie local
    # (extracted_at trong auth.json) và nối cảnh báo chủ động khi ≥ ngưỡng (advisory, KHÔNG đổi ok/rc).
    _nlm_age_note = ""
    if nlm_bin:
        try:
            _tlgd = _imp("tl_gws")
            _nlm_age_note = _tlgd._nlm_cookie_age_note(_tlgd._nlm_auth_age_days(_tlgd._nlm_auth_files() or {}))
        except Exception:   # noqa: BLE001 — advisory best-effort
            _nlm_age_note = ""
    add("nlm CLI (fast-lane)", bool(nlm_bin),
        (f"tl={nlm_bin}; {nprobe.get('path_note')}{_nlm_age_note}" if nlm_bin else
         "KHÔNG tìm thấy → NLM rơi về MCP (chậm). Cowork: chạy lặp `tl nlm-install --resume` tới rc=0; "
         "sau đó " + nlm_auth_fix_hint()))   # r208b 3.2: chuỗi khắc phục auth đúng thứ tự (một nguồn sự thật)
    # M1 (v1.33.35 — log rà 45 Luật LIVE FALSE-GREEN: nlm-auth-load/`nlm login --check` báo OK [rc=0] nhưng
    # nlm-get/list/reconcile LIVE 'Authentication expired'): CANARY LIVE THẬT — 1 `nlm notebook get` base
    # notebook, KHÔNG tin tuổi cookie / login --check. Chỉ chạy khi có binary + KHÔNG --offline. alive=False
    # (auth hết hạn) → RED có remediation; alive=None (thiếu binary/mạng/timeout) → KHÔNG hạ đỏ oan (note).
    if nlm_bin and not a.offline:
        _nb_probe = os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK
        _nlm_alive, _nlm_alive_msg = _imp("tl_gws")._nlm_auth_alive(_nb_probe)
        add("nlm auth (LIVE probe)", _nlm_alive is not False,   # None (không kết luận) KHÔNG đỏ; chỉ False = đỏ
            ("cookie sống — " + _nlm_alive_msg if _nlm_alive is True else
             ("🔴 " + _nlm_alive_msg if _nlm_alive is False else
              "CHƯA kết luận (không network/binary) — " + _nlm_alive_msg)))
    elif nlm_bin and a.offline:
        add("nlm auth (LIVE probe)", True, "offline-skip (kiểm thật: bỏ --offline; `nlm login --check` KHÔNG đủ tin)")
    # gws/direct-media: cần gws binary + cred nạp; thiếu → đọc Drive rơi về GAS (ĐÚNG nhưng chậm + tốn round-trip).
    try:
        gws_ok = bool(_imp("transport").gws_bridge.is_available())
    except Exception:
        gws_ok = False
    # P1 (v1.32.1 — log rà 119 FALSE-GREEN): 'sẵn sàng' cũ chỉ kiểm binary+file cred TỒN TẠI — token revoke vẫn ✓
    # rồi mọi op đọc chết invalid_grant giữa run. CANARY đổi token thật (bỏ qua ở --offline: không network).
    _cred_alive, _cred_msg = (True, "offline-skip") if a.offline else _imp("tl_gws")._gws_cred_alive()
    add("gws/direct-media", gws_ok and _cred_alive,
        ("sẵn sàng (canary token OK)" if not a.offline else "sẵn sàng (offline — CHƯA canary token; kiểm thật: tl gws-ping)")
        if (gws_ok and _cred_alive) else
        (f"CRED CHẾT (canary): {_cred_msg}" if gws_ok and not _cred_alive else
         "CHƯA nạp → đọc Drive rơi về GAS (đúng, chậm hơn). Bật: có TL_MASTER_KEY → `tl bootstrap --secrets-file` "
         "(tải tl_secrets.enc từ Drive, giải mã token+gws+nlm); hoặc đã có token → `tl gws-auth-load` (tải gws cred, giải mã bằng token)."))
    try:
        cc = _imp("contract_check")
        cv, tv = cc.contract_version(), cc.tl_expect_version()
        add("API_CONTRACT ↔ tl EXPECT", cv == tv == EXPECT_VERSION, f"contract={cv}, tl={tv}, expect={EXPECT_VERSION}")
    except Exception as e:
        add("API_CONTRACT ↔ tl EXPECT", False, str(e))
    # SỰ CỐ 2026-06-30: registryDocId trỏ Doc legacy 1mATG → webapp đọc registry RỖNG (count=0 ẢO). CHẶN cứng.
    # S-9 (v1.33.16 — MERGE nhánh-4 CÓ SỬA): rỗng vẫn PASS (auto-discover là fallback AN TOÀN by-design từ
    # v1.23.22 — nhánh-4 cho FAIL sẽ làm doctor đỏ trường kỳ tới khi user pin + kích Cowork loop tự-sửa-config)
    # nhưng note nay KHUYẾN NGHỊ RÕ pin Sheet thật: rỗng = +1 lookup/call + rủi ro bắt nhầm Sheet trùng tên.
    # S-9b (v1.33.29 — log verify v1.33.28: pin xong bằng config-pin-registry mà doctor VẪN '(rỗng)' —
    # check cũ env-only): resolve env → profile → root config qua helper dùng chung với ops-plan.
    _active_reg, _reg_src = _resolve_registry_doc_id(getattr(a, "config", None), getattr(a, "profile", None))
    add("registryDocId KHÔNG phải Doc legacy", _active_reg != _LEGACY_REGISTRY_DOC_ID,
        ("⛔ trỏ Doc legacy 1mATG (chỉ ping/display) → webapp mở Doc-as-Sheet → count=0 ẢO (KHÔNG mất data). "
         "Sửa config registryDocId về Sheet `tra_luat_registry` THẬT (hoặc để RỖNG cho webapp auto-discover) rồi "
         "`tl reg-query --refresh`." if _active_reg == _LEGACY_REGISTRY_DOC_ID
         else ((f"{_active_reg} (pinned · {_reg_src})") if _active_reg
               else "(rỗng → auto-discover chạy được nhưng ⚠ NÊN PIN: `tl config-pin-registry <SHEET_ID>` — "
                    "bớt 1 lookup/call, hết rủi ro bắt nhầm Sheet trùng tên [S-9 log rà 67])")))
    # H (log rà): CẢNH BÁO định kỳ TRÔI registry↔NLM — đếm cờ từ cache OFFLINE (KHÔNG gọi mạng), gợi ý
    # `tl nlm-reconcile`. KHÔNG phải 'check' (in trực tiếp, KHÔNG đổi exit code) — registry biết drift mà
    # nlm-reconcile phải chạy tay; nhắc ở doctor để khỏi quên (log: 97 NLM_STATUS_MISMATCH chưa tự chữa).
    try:
        _drift_keys = ("NLM_STATUS_MISMATCH", "CORPUS_TRUE_NOT_ON_NLM", "NLM_NOTEBOOK_ID_MISSING")
        _ents = _manifest_entries(refresh=False)
        # A4: breakdown TỪNG cờ (không gộp 1 số) + điền sẵn notebook id để chạy 1 bước.
        _bd = {k: 0 for k in _drift_keys}
        _cov_bd = _chunk_covered_sohieu(_ents)     # r253: phủ-bằng-chunk KHÔNG tính là nợ NLM
        for e in _ents:
            _ef = set(_title_flags(e, _cov_bd))
            for k in _drift_keys:
                if k in _ef:
                    _bd[k] += 1
        _drift_n = sum(1 for e in _ents if set(_drift_keys) & set(_title_flags(e, _cov_bd)))
        if _drift_n:
            _nb = os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK
            drift = {"total": _drift_n, "breakdown": dict(_bd), "notebook": _nb}
            if not _json:
                print(f"  ⚠ registry↔NLM lệch: {_drift_n} mục → "
                      + " · ".join(f"{k}={_bd[k]}" for k in _drift_keys))
                for _hl in _drift_hint_lines(_bd, _nb):   # r232: gợi ý theo TỪNG cờ, xem docstring
                    print(_hl)
    except Exception:
        pass
    # v1.34.49 (F-06/F-09 doctor — ADVISORY/REPORT-ONLY theo grill, KHÔNG đổi rc): bất biến notebook↔row_kind
    # theo TOPOLOGY (primary⇔own/blank, overflow⇔overflow, notebook lạ) + findings resolver (alias lệch declared,
    # shard lạ trong registry) + stamp F-09. r232 SỬA CHÚ THÍCH: reconcile --apply ghi row_kind theo topology
    # NHƯNG chỉ KÈM dòng backfill/link (dòng THIẾU nlm_notebook_id) — dòng vào findings này đã CÓ
    # nlm_notebook_id ⇒ --apply KHÔNG bao giờ chạm tới. Lớp này thực sự REPORT-ONLY.
    _topo_doc = None
    try:
        _ents_t = _manifest_entries(refresh=False)
    except Exception:  # noqa: BLE001
        _ents_t = []
    try:
        _base_t = os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK
        _topo_doc = _resolve_shard_topology(_ents_t, _base_t)
        _rkf_doc = _topology_row_kind_findings(_ents_t, _topo_doc)
        topology_report.update({"ok": _topo_doc.get("ok"), "error": _topo_doc.get("error"),
                                "shards": len(_topo_doc.get("shards") or []),
                                "config_findings": _topo_doc.get("findings") or [],
                                "row_kind_findings": len(_rkf_doc), "row_kind_sample": _rkf_doc[:8],
                                "stamp": _topology_stamp(None, _ents_t),
                                # v1.34.57 (B-#3 — advisory TĨNH, doctor KHÔNG tự chạy vì tốn list live)
                                "audit_physical_hint": "tl nlm-audit-physical — chạy sau LÔ di dời/ingest lớn "
                                                       "(đối soát VẬT LÝ↔con trỏ, physical-first)"})
        if not _json:
            print("  ℹ sau LÔ di dời/ingest lớn: `tl nlm-audit-physical` (đối soát VẬT LÝ↔con trỏ — physical-first).")
            if _topo_doc.get("ok") is False:
                print(f"  ⚠ topology CONFIG CONFLICT: {_topo_doc.get('error')} — đường ghi/route sẽ fail-closed (D5).")
            if _rkf_doc:
                # r232: gợi ý cũ («sửa: nlm-reconcile <nb> --apply») KHÔNG chữa được lớp này —
                # reconcile chỉ ghi row_kind KÈM dòng backfill/link, mà dòng lọt vào đây BẮT BUỘC
                # đã có nlm_notebook_id (điều kiện của `_topology_row_kind_findings`) ⇒ hai tập RỜI
                # NHAU theo cấu trúc. Đo 29-07 trên notebook overflow mang 71 dòng lệch: backfill=0,
                # link=0 ⇒ --apply ghi 0 dòng.
                print(f"  ⚠ topology row_kind lệch: {len(_rkf_doc)} dòng (primary⇔own, overflow⇔overflow, notebook lạ)"
                      f" → mẫu trong --json. REPORT-ONLY: `nlm-reconcile --apply` KHÔNG chữa lớp này "
                      f"(chỉ ghi row_kind kèm dòng backfill/link — dòng ở đây đã có nlm_notebook_id, "
                      f"hai tập rời nhau); phải sửa qua đường ghi registry cho từng dòng.")
            for _f_d in (_topo_doc.get("findings") or [])[:4]:
                print(f"  ⚠ topology: {_f_d}")
    except Exception:  # noqa: BLE001 — advisory không được làm hỏng doctor
        pass
    if a.offline:
        rc = 0 if all(ok for n, ok, _ in report if not n.startswith("optional")) else 2
        return _emit_json(rc) if _json else rc
    try:
        load_creds(a.config); g = _gas(); ping = g.get("ping"); live = ping.get("version")
        add("webapp ping", live == EXPECT_VERSION, f"live={live}, expect={EXPECT_VERSION}")
        if a.deep:
            man = g.get("manifest_export")
            add("manifest_export", man.get("ok", True) is not False,
                f"version={man.get('version') or man.get('schema_version')}, count={man.get('count')}, corpus_count={man.get('corpus_count')}")
            # MERGE Codex v1.33.11: probe exporttext-scope — bắt ca ping xanh nhưng fallback GAS chết vì thiếu
            # scope script.external_request (log rà: xref từng chết trong khi doctor toàn xanh).
            try:
                _probe_entries = _manifest_entries(refresh=False)
            except Exception:  # noqa: BLE001
                _probe_entries = []
            xp = _doctor_exporttext_probe(g, _probe_entries)
            add("webapp exporttext scope", bool(xp.get("ok")),
                (("SKIP: " if xp.get("skipped") else "") + str(xp.get("detail") or "")))
    except SystemExit as e:
        add("webapp ping", False, str(e))
    except Exception as e:
        add("webapp ping", False, f"{type(e).__name__}: {e}")
    # v1.34.49 (minor handoff #1): LIVENESS shard overflow — 1 notebook_get/shard (ADVISORY, KHÔNG đổi rc):
    # shard trashed/renamed/mất quyền lộ ngay ở doctor thay vì chết giữa ingest/reconcile.
    if _topo_doc:
        try:
            _nc_d = _imp("nlm_cli")
            _hl_d = {"healed": True}   # doctor chỉ BÁO, không tự heal
            _ovl = []
            for _s_d in (_topo_doc.get("shards") or []):
                if _s_d.get("role") == "primary" or not _s_d.get("enabled"):
                    continue
                _c_d, _ok_d, _err_d = _live_source_count(_nc_d, _s_d.get("id"), _hl_d)
                _ovl.append({"notebook_id": _s_d.get("id"), "alive": bool(_ok_d), "source_count": _c_d,
                             **({"error": str(_err_d)[:120]} if not _ok_d else {})})
                if not _ok_d and not _json:
                    print(f"  ⚠ overflow liveness: {str(_s_d.get('id'))[:16]}… KHÔNG đọc được "
                          f"({str(_err_d)[:80]}) — kiểm shard còn sống; nếu do auth: "
                          + nlm_auth_fix_hint())   # r208c 3.2: chỗ sót cuối còn hô `nlm login` trần
            if _ovl:
                topology_report["overflow_liveness"] = _ovl
        except Exception:  # noqa: BLE001 — advisory best-effort
            pass
    fail_core = [x for x in report if not x[1] and not x[0].startswith("optional")]
    rc = 0 if not fail_core else 2
    return _emit_json(rc) if _json else rc


def cmd_cowork_plan(a) -> int:
    """v1.33.23: checklist bootstrap Cowork KHÔNG mạng-nặng. Mục tiêu: biến 5 ma sát lặp lại (mount cắt cụt,
    gws GNU/glibc, nlm 45s, PATH non-interactive, registry/counts dễ nhầm) thành next-action máy đọc được."""
    integ = _skill_package_integrity(HERE)
    nprobe = _nlm_probe_summary(getattr(a, "env", "cowork"))
    try:
        gws_path = _imp("gws_bridge").gws_exe() or shutil.which("gws") or ""
    except Exception:
        gws_path = shutil.which("gws") or ""
    try:
        st = _imp("tl_gws")._nlm_install_probe(nlm_path=nprobe.get("tl_nlm_path") or nprobe.get("shell_nlm_path") or None)
    except Exception:
        st = nprobe.get("probe") or {"next_step": "unknown"}
    actions = []
    if not integ.get("ok"):
        actions.append("Tải zip skill sạch từ Drive/drive.usercontent rồi unzip vào thư mục ghi được; không chạy file mount bị cắt cụt.")
    if not gws_path:
        actions.append("Cài gws MUSL-static: `tl gws-bootstrap-cowork` — KHÔNG `npm i -g @googleworkspace/cli` trên Ubuntu 22/glibc 2.35.")
    if (st or {}).get("next_step") != "done":
        actions.append("Cài nlm theo từng bước: lặp `tl nlm-install --resume` tới rc=0; rc=3 nghĩa là còn bước, không phải lỗi.")
    if nprobe.get("tl_nlm_path") and not nprobe.get("shell_nlm_path"):
        actions.append("Gõ `nlm` trực tiếp cần `export PATH=$HOME/.local/bin:$PATH`; còn trong skill hãy dùng `tl nlm-*`.")
    actions.append("Kế toán slot: dùng LIVE `tl counts --live-nlm` hoặc `tl nlm-get <notebook> --json`; không dùng registry_claim_nlm để chốt FULL.")
    actions.append("Pin registryDocId khi có Sheet ID thật: ghi vào config/TL_REGISTRY_DOC_ID để bỏ auto-discover.")
    out = {"ok": bool(integ.get("ok")), "env": "cowork", "package": {"ok": integ.get("ok"), "core_bad": integ.get("core_bad")},
           "gws": {"path": gws_path, "ok": bool(gws_path), "note": "cần bản MUSL-static trong Cowork"},
           "nlm": nprobe, "next_actions": actions}
    if getattr(a, "json", False) or getattr(a, "out", None):
        _emit_json_payload(out, getattr(a, "out", None)); return 0 if out["ok"] else 1
    print("== tl cowork-plan ==")
    print(f"  {'✓' if integ.get('ok') else '✗'} package: {integ.get('note')}")
    print(f"  {'✓' if gws_path else '✗'} gws: {gws_path or 'chưa có — dùng gws-bootstrap-cowork'}")
    print(f"  {'✓' if (st or {}).get('next_step') == 'done' else '•'} nlm: next_step={(st or {}).get('next_step')} · {nprobe.get('path_note')}")
    for i, act in enumerate(actions, 1):
        print(f"  {i}. {act}")
    return 0 if out["ok"] else 1


def cmd_exists(a) -> int:
    """Cổng chống overclaim: kiểm tra hiện diện bằng source-map, không dùng reg_get thô."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    if getattr(a, "refresh", False) or not (_cache_file("manifest.json")).exists():
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:
        print(f"[tl] exists: không đọc được manifest: {e}", file=sys.stderr)
        return 1
    item = _source_map_one(a.query, entries)
    found = bool(item.get("canonical") or item.get("direct_hits") or item.get("name_hits") or item.get("amendment_candidates"))
    _scope = _active_profile()
    if not found and _base_also_enabled(a):
        # A (v1.30.0): profile MISS → tra tiếp trên manifest NỀN VBQPPL (profile-first, nền bổ sung; gắn scope rõ).
        _b_entries, _ = _base_manifest_entries(getattr(a, "config", None))
        if _b_entries:
            b_item = _source_map_one(a.query, _b_entries)
            if b_item.get("canonical") or b_item.get("direct_hits") or b_item.get("name_hits") or b_item.get("amendment_candidates"):
                b_item["scope"] = "vbqppl"
                b_item["flags"] = list(b_item.get("flags") or []) + ["BASE_SCOPE_HIT"]
                item, found, _scope = b_item, True, "vbqppl"
    out = {
        "ok": True,
        "query": a.query,
        "exists_in_manifest_or_nlm": found,
        "scope": _scope,
        "conclusion": "FOUND_OR_RELATED" if found else "UNKNOWN_NOT_ABSENT",
        "source_map": item,
        "rule": "Không kết luận vắng mặt nếu chưa chạy source-map theo tên + locate/status theo số hiệu + QT-5 nếu là VBHN/sửa đổi.",
    }
    if found and _scope == "vbqppl" and _active_profile() != DEFAULT_PROFILE:
        out["warnings"] = ["BASE_SCOPE_HIT: tìm thấy ở NỀN VBQPPL (KHÔNG phải profile đang chọn)."]
    if not found:
        out["warnings"] = ["NOT_FOUND_IN_MANIFEST_DO_NOT_CONCLUDE_ABSENT", "TRY_BY_SOHIEU_AND_SUBJECT", "IF_AMENDED_RUN_VBHN_CHECK_QT5"]
    if a.json:
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"== tl exists — {a.query} ==")
        print(out["conclusion"])
        c = item.get("canonical")
        if c:
            print(f"canonical: {c.get('name','')[:90]} | sohieu={c.get('sohieu') or '∅'} | nlm={c.get('nlm')}")
        for ac in item.get("amendment_candidates") or []:
            print(f"amendment: {ac.get('name','')[:90]} | sohieu={ac.get('sohieu') or '∅'} | linked={ac.get('linked_to_query')}")
        for w in item.get("warnings") or out.get("warnings") or []:
            print(f"⚠ {w}")
    return 0 if found else 2


def _resolve_registry_doc_id(config_path: str | None = None, profile: str | None = None) -> tuple[str, str]:
    """S-9b (v1.33.29, PURE-ish): registryDocId hiệu lực = env TL_REGISTRY_DOC_ID → profile.registryDocId →
    root config.registryDocId. Trả (id, nguồn). Log verify v1.33.28: ĐÃ pin vào config (root+profile) mà doctor
    VẪN in '(rỗng → NÊN PIN)' vì check cũ CHỈ đọc env (apply_profile_offline không export key này) — cảnh báo
    stale ngay sau khi pin. Doctor + ops-plan nay resolve CÙNG một đường."""
    rid = (os.environ.get("TL_REGISTRY_DOC_ID") or "").strip()
    if rid:
        return rid, "env"
    try:
        cfg_path, cfg = _read_config_record(config_path)
        prof_name = (profile or (cfg.get("defaultProfile") if isinstance(cfg, dict) else None)
                     or os.environ.get("TL_PROFILE") or DEFAULT_PROFILE)
        prof = (_profiles_from_config(cfg).get(prof_name) if isinstance(cfg, dict) else {}) or {}
        rid = (prof.get("registryDocId") or (cfg.get("registryDocId") if isinstance(cfg, dict) else "") or "").strip()
        return rid, (f"config:{cfg_path}" if rid else "")
    except Exception:  # noqa: BLE001
        return "", ""


def cmd_instructions(a) -> int:
    try:
        import gen_instructions  # type: ignore
    except Exception as e:
        print(f"[tl] Không import được gen_instructions.py: {e}", file=sys.stderr)
        return 2
    # v1.19: mặc định profile = vbqppl; profile dự án (văn bản thường) lấy từ --profile (global) hoặc env.
    prof = getattr(a, "profile", None) or os.environ.get("TL_PROFILE") or DEFAULT_PROFILE
    nb = getattr(a, "notebook", None) or os.environ.get("TL_NOTEBOOK_ID") or None
    fld = getattr(a, "folder_name", None) or None
    root = getattr(a, "root_folder_id", None) or os.environ.get("TL_ROOT_FOLDER_ID") or None
    target = getattr(a, "target", "both") or "both"
    tier = (getattr(a, "tier", None) or "core").lower()   # v1.34.68 Q3: mặc định CORE (breaking chủ đích)
    if hasattr(gen_instructions, "generate"):
        try:
            text = gen_instructions.generate(target,
                                             getattr(a, "skill_version", VERSION) or VERSION,
                                             prof, nb, fld, root, tier=tier)
        except TypeError:  # tương thích ngược nếu generate() bản cũ chưa nhận profile/tier
            text = gen_instructions.generate(target,
                                             getattr(a, "skill_version", VERSION) or VERSION)
        audit_target = "project" if target == "config" else target
        if tier == "full" and audit_target == "project":
            audit_target = "full"                          # ⑤ audit theo bộ khóa REQUIRED_FULL
        audit = {"ok": True, "missing": []} if target == "style-template" else (
            gen_instructions.audit(text, audit_target) if hasattr(gen_instructions, "audit") else {"ok": True, "missing": []})
        ok, missing = bool(audit.get("ok")), audit.get("missing", [])
    else:
        text = gen_instructions.build_instruction(target=a.target, skill_version=a.skill_version or VERSION)
        ok, missing = gen_instructions.validate_instruction(text)
    if a.check:
        print(json.dumps({"ok": ok, "missing": missing}, ensure_ascii=False, indent=2))
        return 0 if ok else 1
    out_path = getattr(a, "out", None)
    if out_path:
        # III.3: ghi UTF-8 ra file (Path.write_text, không phụ thuộc codepage console). In tóm tắt ra stderr.
        try:
            Path(out_path).write_text(text, encoding="utf-8")
        except Exception as e:
            print(f"[tl] instructions --out: KHÔNG ghi được {out_path}: {e}", file=sys.stderr)
            return 2
        print(f"[tl] instructions → {out_path} ({len(text)} ký tự){'' if ok else ' ⚠ THIẾU block: '+', '.join(missing)}", file=sys.stderr)
        return 0 if ok else 1
    print(text)
    return 0 if ok else 1


def _resolve_confirm_targets(a, entries: list[dict]) -> list[dict]:
    """Chọn văn bản để confirm: --drive-id (1) / --sohieu (canonical) / --cat NN (chưa-confirm, corpus) / --all-unconfirmed.
    Chế độ batch (--cat/--all-unconfirmed) GIỚI HẠN --limit (mỗi target đọc 1 header → tốn)."""
    did = getattr(a, "drive_id", None)
    if did:
        return [e for e in entries if _entry_drive_id(e) == did]
    sh = getattr(a, "sohieu", None)
    if sh:
        canon, _hits = _canonical_for_query(sh, refresh=getattr(a, "refresh", False))
        return [canon] if canon else []
    cat = getattr(a, "cat", None)
    pool = entries
    if cat:
        cc = re.sub(r"\D", "", str(cat))[:2]
        pool = [e for e in entries if re.sub(r"\D", "", str(_entry_cat(e)))[:2] == cc]
    if getattr(a, "all_unconfirmed", False) or cat:
        pool = [e for e in pool if not _entry_confirmed(e) and _entry_drive_id(e)
                and str(e.get("corpus") or "").lower() != "false" and not _entry_quarantined(e)]
        return pool[: (getattr(a, "limit", None) or 20)]
    return []


def cmd_confirm(a) -> int:
    """Gán nhãn ĐÃ-RÀ-KỸ & CHẮC-ĐÚNG (registry.verified) — CHỈ sau khi ĐỌC HEADER xác minh sohieu/tiêu đề/loại/cat khớp
    tên + thư mục (`_verify_header_match`). KHÔNG tin metadata suông. Mismatch → KHÔNG gán (trừ --force → 'verified=…|FORCED').
    Mặc định DRY (in kế hoạch); --apply mới ghi. Entry đã confirm → source-map/dedup/locate tin dùng luôn, bỏ re-review."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:  # noqa: BLE001
        print(f"[tl] confirm: không đọc được manifest: {e}", file=sys.stderr); return 1
    targets = _resolve_confirm_targets(a, entries)
    if not targets:
        msg = "confirm: không có target — dùng --drive-id / --sohieu / --cat <NN> / --all-unconfirmed (+--limit)"
        print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False) if getattr(a, "json", False)
              else f"[tl] {msg}", file=sys.stderr)
        return 1
    g = _gas()
    run_id = None
    if getattr(a, "apply", False):
        _ok_gate, _ = _apply_gate(a, write_cols="verified")   # (Pha 1+) precheck TRƯỚC khi ghi verified
        if not _ok_gate:
            return 2
        run_id = _apply_journal_start("confirm", {})
    results = []
    for e in targets:
        did = _entry_drive_id(e); nm = _entry_name(e)
        try:
            txt = _read_doc_text(did, getattr(a, "config", None))
        except Exception as ex:  # noqa: BLE001
            results.append({"drive_id": did, "name": nm, "error": f"đọc header lỗi: {type(ex).__name__}"}); continue
        if not (txt or "").strip():
            results.append({"drive_id": did, "name": nm, "error": "header rỗng (không đọc được nội dung — kiểm gws/quyền)"}); continue
        vr = _verify_header_match(e, txt)
        forced = (not vr["ok"]) and getattr(a, "force", False)
        applied = ""
        if (vr["ok"] or forced) and getattr(a, "apply", False):
            val = (getattr(a, "label", None) or _today_iso()) + ("|FORCED" if forced else "")
            _cv = _journaled_reg_write(run_id, g, [{"drive_id": did, "verified": val}], "verified", before_by_key={did: {"verified": str(e.get("verified") or "")}})
            applied = val if _cv.get("verified") else ""
        results.append({"drive_id": did, "name": nm, "ok": vr["ok"], "forced": forced,
                        "checks": vr["checks"], "mismatches": vr["mismatches"],
                        "applied": bool(applied), "verified": applied})
    nap = sum(1 for r in results if r.get("applied"))
    if run_id:
        _journal_append(run_id, {"t": "run_end", "ok": True, "counts": {"applied": nap}})
        _invalidate_manifest_cache()
    if getattr(a, "json", False):
        print(json.dumps({"ok": True, "targets": len(results), "applied": nap, "journal": run_id,
                          "dry": not getattr(a, "apply", False), "results": results}, ensure_ascii=False, indent=2))
        return 0
    head = "DRY (chưa ghi — thêm --apply)" if not getattr(a, "apply", False) else f"ĐÃ GHI verified: {nap}/{len(results)}"
    print(f"== tl confirm — {len(results)} target · {head} ==")
    for r in results:
        if r.get("error"):
            print(f"  ✗ {r['name'][:55]} — {r['error']}"); continue
        mark = "✓ PASS" if r["ok"] else ("⚠ FORCED" if r["forced"] else "✗ MISMATCH")
        cks = " ".join(f"{k}={'✓' if v else '✗'}" for k, v in r["checks"].items())
        print(f"  {mark}  {r['name'][:55]} | {cks}" + (f" | verified={r['verified']}" if r.get("applied") else ""))
        for m in r["mismatches"]:
            print(f"        - {m}")
    if not getattr(a, "apply", False):
        print("  → thêm --apply để ghi nhãn cho bản PASS (mismatch cần --force).")
    return 0


def cmd_manifest(a) -> int:
    """Kết phiên. Profile categories=inherit mặc định export-only; nếu ép --touched-drive phải xác nhận,
    và regen2 chỉ quét rootFolderId riêng (manifestScope=own)."""
    profile = _active_profile()
    categories_mode = os.environ.get("TL_CATEGORIES_MODE", "").strip().lower()
    inherited_profile = profile != DEFAULT_PROFILE and categories_mode == "inherit"
    manifest_scope = a.manifest_scope or ("inherited" if profile == DEFAULT_PROFILE else "own")
    _perr = _profile_policy_error(require_registry=True, require_manifest=bool(a.touched_drive), forbid_inherit=True)
    if _perr:
        return _emit_profile_policy_error(_perr, getattr(a, "json", False))
    if a.touched_drive and inherited_profile and a.confirm != "yes":
        out = {
            "ok": False,
            "error": "PROFILE_INHERIT_TOUCHED_DRIVE_CONFIRM_REQUIRED",
            "profile": profile,
            "categories": categories_mode,
            "warning": "categories=inherit chỉ dùng để ORGANIZE/tra cứu fallback; regen2 sẽ chỉ quét rootFolderId riêng.",
            "required": "--confirm yes",
        }
        print(json.dumps(out, ensure_ascii=False) if a.json else
              f"✗ {out['error']}: profile '{profile}' categories=inherit. Thêm --confirm yes nếu thật sự cần quét cây own.",
              file=sys.stderr)
        return 2
    if profile != DEFAULT_PROFILE and manifest_scope == "inherited" and a.confirm != "yes":
        print("[tl] PROFILE_INHERITED_SCOPE_CONFIRM_REQUIRED: --manifest-scope inherited cần --confirm yes.",
              file=sys.stderr)
        return 2
    if a.touched_drive and profile != DEFAULT_PROFILE:
        # ⛔ SỰ CỐ 2026-06-30: profile DỰ ÁN có registryDocId RỖNG → webapp `regSS_` rơi nhánh BASE → regen2 ghi/quét
        # PHÌNH rồi clobber registry NỀN VBQPPL (Sheet `tra_luat_registry`). CHẶN trước khi đụng server.
        _prof_reg = (os.environ.get("TL_REGISTRY_DOC_ID") or "").strip()
        if not _prof_reg:
            out = {"ok": False, "error": "PROFILE_REGISTRY_ID_EMPTY_WOULD_CLOBBER_BASE", "profile": profile,
                   "note": "Profile dự án KHÔNG có registryDocId riêng → regen2 sẽ rơi vào registry NỀN VBQPPL và làm hỏng nó. "
                           "Tạo registry riêng (Sheet mới) + ghi registryDocId vào config TRƯỚC khi --touched-drive."}
            print(json.dumps(out, ensure_ascii=False) if a.json else f"⛔ {out['error']}: {out['note']}", file=sys.stderr)
            return 2
        # Server cũ có thể bỏ qua rootFolderId/manifestScope và ghi phình registry trước khi client kịp cảnh báo.
        # Vì vậy profile regen chỉ được chạy khi ping chứng minh đúng contract có guard server-side.
        ping = _gas().get("ping")
        if ping.get("version") != EXPECT_VERSION:
            out = {
                "ok": False,
                "error": "PROFILE_REGEN_SERVER_GUARD_REQUIRED",
                "profile": profile,
                "live_version": ping.get("version"),
                "required_version": EXPECT_VERSION,
                "note": "Dừng trước regen2: deploy Code.2.21.2i.gs để có own-scope + blowup guard.",
            }
            print(json.dumps(out, ensure_ascii=False) if a.json else
                  f"✗ {out['error']}: live={out['live_version']} required={EXPECT_VERSION}. {out['note']}",
                  file=sys.stderr)
            return 3
    mb = _need_base('manifest_build')
    kwargs = {
        "no_regen": not a.touched_drive,
        "manifest_scope": manifest_scope,
        "confirm_blowup": a.confirm_blowup,
        "confirm_inherited": a.confirm,
    }
    try:
        r = mb.build(**kwargs)
    except TypeError:
        # Tương thích helper nền cũ: export-only vẫn chạy; regen profile phải nâng helper để không mất guard.
        if a.touched_drive and profile != DEFAULT_PROFILE:
            print("[tl] manifest_build.py quá cũ, không hỗ trợ profile scope guard; hãy dùng helper kèm v1.19.4.",
                  file=sys.stderr)
            return 2
        r = mb.build(no_regen=not a.touched_drive)
    # Nếu đã chạy regen2 mà manifest_export lệch treeHash/corpus_count thì không được xanh giả.
    if a.touched_drive and (r.get("treeHash_match") is False or r.get("corpus_count_match") is False):
        r["ok"] = False
        r["error"] = "regen2 và manifest_export không khớp treeHash/corpus_count"
    # v1.34.49 (F-09): stamp topology dẫn xuất CLIENT-SIDE (topology_hash + routing_epoch + registry_digest) —
    # chứng minh snapshot theo topology/registry nào (server-side stamp = đợt 50 GAS 2.21.2l). Best-effort.
    try:
        _cfg_m = _read_config_record(getattr(a, "config", None))[1]
        _ents_m = _manifest_entries(refresh=False)
        r["topology"] = _topology_stamp(_cfg_m, _ents_m, profile=profile)
    except Exception:  # noqa: BLE001 — stamp không được làm hỏng manifest
        pass
    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        mode = f"regen2({manifest_scope})+export" if a.touched_drive else "export-only"
        ok = "✓" if r.get("ok") else "✗"
        extra = ""
        if a.touched_drive:
            extra = (f" | treeHash_match={r.get('treeHash_match')} "
                     f"corpus_count_match={r.get('corpus_count_match')}")
        print(f"{ok} manifest ({mode}) | webapp {r.get('version') or r.get('schema_version')} | treeHash {r.get('treeHash')} "
              f"| count {r.get('count')} corpus={r.get('corpus_count')} | {r.get('total_ms',0)/1000:.1f}s{extra}")
    return 0 if r.get("ok") else 1


def _vbhn_normalize_recommendations(entries: list[dict]) -> list[dict]:
    """Đề xuất backfill/rename VBHN; report-only, không ghi Drive/NLM."""
    recs = []
    for e in entries:
        if not _is_vbhn_entry(e):
            continue
        sh_raw = _entry_sohieu(e) or _parse_sohieu_from_name(_entry_name(e))
        sh_norm = _sohieu_key_entry(e)
        agency = _vbhn_agency_from_key(sh_norm)
        pattern = "VBHN_<so-hieu>_<year>_<ten_rut_gon>"
        if agency and agency != "VPQH":
            pattern = "VBHN_<so>-VBHN-<co_quan>_<year>_<ten_rut_gon>"
        flags = _title_flags(e)
        actions = []
        if sh_norm and norm_sohieu(sh_raw) != sh_norm:
            actions.append({"action": "BACKFILL_SOHIEU", "from": sh_raw, "to": sh_norm})
        iy = _entry_issue_year(e)
        if iy and "VBHN_NAME_MISSING_YEAR" in flags:
            actions.append({"action": "RENAME_ADD_YEAR", "year": iy, "suggested_pattern": pattern})
        if "VBHN_MINISTRY_MISSING_YEAR" in flags:
            actions.append({"action": "BACKFILL_ISSUE_YEAR_REQUIRED", "scope": "ministerial_vbhn",
                            "note": "VBHN cấp Bộ cũng phải có năm; verify dòng ngày ban hành trước khi rename."})
        if "VBHN_MINISTRY_NAME_MISSING_YEAR" in flags:
            actions.append({"action": "RENAME_MINISTRY_ADD_YEAR", "year": iy, "suggested_pattern": pattern})
        if "VBHN_BARE_NUMBER" in flags:
            actions.append({"action": "RENAME_ADD_SUBJECT", "suggested_pattern": pattern})
        if "VBHN_SOHIEU_NORMALIZED_FROM_SHORT_VPQH" in flags:
            actions.append({"action": "BACKFILL_SOHIEU_CANONICAL_VBHN", "from": sh_raw, "to": sh_norm})
        if flags or actions:
            recs.append({"entry": _summ_entry(e), "flags": flags, "actions": actions})
    return recs


def cmd_vbhn_normalize(a) -> int:
    if getattr(a, "refresh", False) or not (_cache_file("manifest.json")).exists():
        load_creds(getattr(a, "config", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:
        print(f"[tl] vbhn-normalize: không đọc được manifest: {e}", file=sys.stderr)
        return 1
    recs = _vbhn_normalize_recommendations(entries)
    ghosts = [_summ_entry(e) for e in entries if "NLM_GHOST_SOURCE" in _title_flags(e)]
    removed_with_mapping = [_summ_entry(e) for e in entries
                            if _entry_nlm(e) and _nlm_status_removed(str(e.get("nlm_status") or ""))]
    out = {
        "ok": True,
        "entries": len(entries),
        "recommendations": recs[:200],
        "count": len(recs),
        "ghost_nlm_sources": ghosts[:100],
        "ghost_count": len(ghosts),
        "removed_nlm_mappings": removed_with_mapping[:100],
        "removed_nlm_mapping_count": len(removed_with_mapping),
        "note": "report-only; mọi backfill/rename/quarantine/clear_nlm_mapping vẫn phải duyệt riêng",
    }
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"== tl vbhn-normalize — recommendations={len(recs)} ghost_nlm={len(ghosts)} removed_nlm_mapping={len(removed_with_mapping)} ==")
        for r in recs[:getattr(a, "limit", 50)]:
            e = r["entry"]
            print(f"- {e['name'][:90]} | sohieu={e['sohieu'] or '∅'} → key={e['sohieu_key']} | flags={','.join(r['flags'])}")
            for act in r["actions"]:
                print("    * " + json.dumps(act, ensure_ascii=False))
        if ghosts:
            print("\nNguồn NLM mồ côi thiếu metadata:")
            for g in ghosts[:getattr(a, "limit", 50)]:
                print(f"- id={g['drive_id']} name={g['name'] or '∅'} sohieu={g['sohieu'] or '∅'} cat={g['cat'] or '∅'}")
    return 0


def _pin_registry_doc_id_config(config_path: str | None, registry_doc_id: str, profile: str | None = None, root: bool = False) -> dict:
    """Pin registryDocId into local config without touching Drive/Sheets. Safe fix for S-9 auto-discover friction."""
    rid = (registry_doc_id or "").strip()
    if not rid:
        return {"ok": False, "error": "REGISTRY_DOC_ID_REQUIRED"}
    if rid == _LEGACY_REGISTRY_DOC_ID:
        return {"ok": False, "error": "REFUSE_LEGACY_DOC_ID", "note": "registryDocId phải là Google Sheet, không phải Doc legacy 1mATG"}
    target, data, err = _mutable_config_target(config_path)
    if err:
        return {"ok": False, "error": err, "path": str(target) if target else None}
    prof_name = (profile or data.get("defaultProfile") or DEFAULT_PROFILE).strip() or DEFAULT_PROFILE
    before = None
    if root:
        before = data.get("registryDocId") or ""
        data["registryDocId"] = rid
    else:
        profs = data.get("profiles") if isinstance(data.get("profiles"), dict) else {}
        prof = profs.get(prof_name) if isinstance(profs.get(prof_name), dict) else {}
        before = prof.get("registryDocId") or ""
        prof["registryDocId"] = rid
        profs[prof_name] = prof
        data["profiles"] = profs
        if prof_name == DEFAULT_PROFILE and not data.get("registryDocId"):
            data["registryDocId"] = rid
    _write_json_atomic(target, data)
    return {"ok": True, "path": str(target), "profile": None if root else prof_name, "root": bool(root),
            "registryDocId_before": before, "registryDocId_after": rid}


def cmd_config_pin_registry(a) -> int:
    res = _pin_registry_doc_id_config(getattr(a, "config", None), getattr(a, "registry_doc_id", ""),
                                      getattr(a, "profile_name", None), getattr(a, "root", False))
    if getattr(a, "json", False) or getattr(a, "out", None):
        _emit_json_payload(res, getattr(a, "out", None)); return 0 if res.get("ok") else 2
    if not res.get("ok"):
        print(f"[tl] config-pin-registry lỗi: {res.get('error')} {res.get('note') or ''}", file=sys.stderr); return 2
    scope = "root" if res.get("root") else f"profile={res.get('profile')}"
    print(f"✓ pinned registryDocId ({scope}) vào {res['path']}: {res['registryDocId_after']}")
    print("  → chạy `tl doctor` hoặc `tl precheck` để xác nhận không còn auto-discover.")
    return 0


def _merge_base_entries(profile_hits: list[dict], base_hits: list[dict]) -> list[dict]:
    """A (v1.30.0, PURE): hợp nhất hit — PROFILE TRƯỚC, nền VBQPPL BỔ SUNG (dedup theo drive_id); hit nền được
    đánh dấu scope='vbqppl' để hiển thị/máy-đọc phân biệt nguồn. Canonical của profile luôn thắng.
    r179 T5 (CONTEXT «Scope (dòng kết quả)»): khoá `_scope` riêng của reg-query BỎ — MỘT cách mã hoá duy nhất
    `scope:'vbqppl'` (+ cờ BASE_SCOPE_HIT gắn ở tầng emit row) đồng nhất với source-map/exists/locate."""
    seen = {_entry_drive_id(e) for e in (profile_hits or []) if _entry_drive_id(e)}
    out = list(profile_hits or [])
    for e in base_hits or []:
        did = _entry_drive_id(e)
        if did and did in seen:
            continue
        e2 = dict(e)
        e2["scope"] = "vbqppl"
        out.append(e2)
    return out


def _pfr_count(x) -> int:
    """Đếm một trường có thể là số HOẶC danh sách (`reg_delete` trả cả hai kiểu tuỳ phiên bản GAS)."""
    if isinstance(x, (list, tuple, set)):
        return len(x)
    try:
        return int(x)
    except (TypeError, ValueError):
        return -1          # KHÔNG đọc được ⇒ -1, để phép so ở dưới fail-closed chứ không coi là 0


def _pfr_reg_delete_verdict(resp, requested_ids: list) -> dict:
    """r289 (PRO-01): READBACK phía CLIENT cho `reg_delete` — biến response thành KẾT QUẢ có kiểm.

    Vì sao không dùng `require_removed='yes'` (chốt phía server) — ĐÃ ĐO, và câu trả lời là KHÔNG:
    `require_removed='yes'` chỉ xoá dòng có `nlm_status` bắt đầu `removed*` (API_CONTRACT §reg_delete).
    Nhưng `profile-file-remove` **không hề ghi `nlm_status`** ở bất kỳ đường nào — nên bật `'yes'` sẽ
    làm lệnh thành VÔ TÁC DỤNG với gần như mọi dòng (rơi hết vào `skipped_live`), tức đổi một lỗi
    fail-open lấy một lỗi fail-silent. `'no'` giữ nguyên là hard-delete CÓ CHỦ ĐÍCH sau
    `--apply --confirm yes` (cùng lý lẽ đã ghi ở `source_ops.py:954`).

    Chốt thật nằm ở đây: `ok=true` của response **chưa phải** bằng chứng dòng đã bị gỡ —
    `skipped_live>0` vẫn có thể đi kèm `ok=true`. Luật:
      * response phải dương (`ok=true`);
      * `skipped_live` phải bằng 0 — server từ chối gỡ dòng nào là ta CHƯA xong;
      * `removed + not_found` phải phủ hết `requested` — `not_found` được chấp nhận vì chạy lại sau một
        lượt thành công một phần thì dòng đã biến mất, không phải lỗi mới.
    """
    _ok, _why = step_result_ok(resp)
    if not _ok:
        return {"ok": False, "error": f"REG_DELETE_AM:{_why}", "resp": resp}
    _want = len(requested_ids)
    _removed, _nf, _skip = (_pfr_count(resp.get("removed")), _pfr_count(resp.get("not_found")),
                            _pfr_count(resp.get("skipped_live")))
    if _skip != 0:
        return {"ok": False, "error": f"REG_DELETE_CON_SKIPPED_LIVE:{_skip}", "resp": resp}
    if _removed < 0 or _nf < 0 or (_removed + _nf) < _want:
        return {"ok": False,
                "error": f"REG_DELETE_KHONG_PHU_HET:removed={_removed} not_found={_nf} requested={_want}",
                "resp": resp}
    return {"ok": True, "removed": _removed, "not_found": _nf, "requested": _want, "resp": resp}


def cmd_profile_file_remove(a) -> int:
    profile = getattr(a, "target_profile", None) or getattr(a, "profile", None)
    ids = {x.strip() for x in (getattr(a, "drive_ids", None) or []) if x.strip()}
    if not ids:
        print("[tl] profile-file-remove cần drive_id...", file=sys.stderr)
        return 2
    # r282 (P16-F04, P0 mất dữ liệu): lệnh này KHÔNG có `_profile_policy_error` trong khi mọi đường GHI
    # cùng lớp đều có (ingest_ops ×5, ops_misc:1429, profile_mgmt:79) — kể cả lệnh ANH EM `profile-file-add`
    # (= cmd_profile_ingest). Hệ quả khi gõ SAI tên profile: `_profile_manifest_entries_for` trả manifest
    # NỀN (1315 dòng), drive_id vẫn khớp nên KHÔNG rơi NO_MATCHING_PROFILE_ROWS, rồi `source_delete`
    # (BẤT KHẢ NGHỊCH) + `trash` + `reg_delete` bắn thẳng vào registry/notebook NỀN, in ok:true rc=0.
    # Khuôn giống cmd_profile_ingest: áp scope TRƯỚC → soi cổng → RỒI mới đọc manifest. Thứ tự này còn
    # chặn luôn việc nạp manifest NỀN vào cache của profile-ma (F09) vì ta thoát TRƯỚC khi đọc.
    try:
        apply_profile_offline(getattr(a, "config", None), profile)
    except (SystemExit, Exception):  # noqa: BLE001 — thiếu config KHÔNG được giết lệnh; cổng dưới tự fail-closed
        pass
    _perr = _profile_policy_error(require_registry=True, require_manifest=True, forbid_inherit=True)
    if _perr:
        return _emit_profile_policy_error(_perr, getattr(a, "json", False))
    entries, err = _profile_manifest_entries_for(profile, getattr(a, "config", None), getattr(a, "refresh", False))
    if err:
        print(json.dumps({"ok": False, "error": err}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    matched = []
    for e in entries:
        did = _entry_drive_id(e)
        goc = str(e.get("goc") or e.get("src_id") or "").strip()
        if did in ids or goc in ids:
            matched.append(e)
    reg_ids = [_entry_drive_id(e) for e in matched if _entry_drive_id(e)]
    source_ids = _profile_live_source_ids(matched)
    # (MERGE Claude, an toàn) GUARD shared_source_id trên TOÀN manifest (nguồn dùng chung với dòng KHÁC ngoài matched
    # → xóa gãy link kia). Chỉ xóa nguồn KHÔNG shared.
    nlm_deletable, nlm_blocked_shared = _profile_deletable_sources(entries, source_ids)
    plan = {"ok": bool(matched), "mode": "APPLY" if getattr(a, "apply", False) else "DRY",
            "profile": profile or _active_profile(), "requested": sorted(ids), "matched_rows": len(matched),
            "registry_drive_ids": reg_ids, "nlm_source_ids": source_ids,
            "nlm_deletable": nlm_deletable, "nlm_blocked_shared_source_id": nlm_blocked_shared,
            "delete_nlm": bool(getattr(a, "delete_nlm", False)),
            "trash_drive": bool(getattr(a, "trash_drive", False)),
            "keep_registry": bool(getattr(a, "keep_registry", False)),
            "note": "DRY mặc định; --apply --confirm yes mới gỡ registry/NLM/Drive theo cờ. Nguồn shared_source_id KHÔNG xóa."}
    if not matched:
        plan["error"] = "NO_MATCHING_PROFILE_ROWS"
        print(json.dumps(plan, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    if not getattr(a, "apply", False):
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0
    if getattr(a, "confirm", "") != "yes":
        print(json.dumps({**plan, "ok": False, "error": "CONFIRM_YES_REQUIRED"}, ensure_ascii=False, indent=2),
              file=sys.stderr)
        return 2
    load_creds(getattr(a, "config", None), profile)
    # ── r289 (PRO-01, P1 fail-open PHÁ HUỶ — mục nguy hiểm nhất sổ audit) ────────────────────────────
    # TRƯỚC: `_dr`/`r` của `nlm source_delete` và `drive trash` CHỈ được ghi nhật ký, KHÔNG kiểm; rồi
    # `reg_delete` chạy VÔ ĐIỀU KIỆN; rồi `out = {**plan, "ok": True, ...}` GÁN CỨNG và `return 0`.
    # ⇒ Mọi bước con hỏng vẫn `rc=0`, mà con trỏ registry ĐÃ BỊ THÁO: file Drive/nguồn NLM còn nguyên
    # nhưng không còn dòng nào tra ra chúng — tài sản MỒ CÔI, và vì rc=0 nên không ai đi tìm.
    # NAY: Helper 1 (`tl_core/txn.py`) — kết quả từng bước được KIỂM, `reg_delete` bị CHẶN (TxnBlocked)
    # nếu một thao tác ĐƯỢC YÊU CẦU trước đó hỏng, `ok` được TÍNH, `rc` dẫn xuất, và output kê rõ
    # ĐÃ GHI ĐƯỢC GÌ RỒI (`txn.wrote`) / CHƯA CHẮC (`txn.uncertain`) để người vận hành biết đi dọn đâu.
    _t = Txn("profile-file-remove")
    _want_nlm = bool(getattr(a, "delete_nlm", False))
    _want_trash = bool(getattr(a, "trash_drive", False))
    _keep_reg = bool(getattr(a, "keep_registry", False))
    nlm_results = []
    # v1.29.3 (AUDIT B1 #6): journal như profile-delete (NLM delete = forensic; trash = visibility) — cùng pattern.
    _pf_rid = None
    if _want_nlm or _want_trash:
        _pf_rid = _apply_journal_start("profile-file-remove-assets", {"nlm": len(nlm_deletable) if _want_nlm else 0,
                                                                      "trash": len(reg_ids) if _want_trash else 0})
    _blocked = None
    if _want_nlm:
        nc = _imp("nlm_cli")
        for sid in nlm_deletable:       # CHỈ nguồn KHÔNG shared
            _journal_append(_pf_rid, {"t": "intent", "op": "nlm_source_delete", "key": sid, "set": {"irreversible": True}})
            try:
                _dr = nc.source_delete(sid)
            except Exception as e:  # noqa: BLE001 — transport nổ là bước HỎNG, không phải bước vắng mặt
                _dr = {"ok": False, "error": f"{type(e).__name__}: {e}"}
            _journal_append(_pf_rid, {"t": "commit", "op": "nlm_source_delete", "key": sid,
                                      "ok": bool(isinstance(_dr, dict) and _dr.get("ok"))})
            _t.record(f"nlm_source_delete:{sid}", _dr, mutating=True, wrote={"nlm_source_id": sid})
            nlm_results.append({"source_id": sid, "result": _dr})
    else:
        _t.skipped("nlm_source_delete", "KHONG_YEU_CAU")
    g = _gas()
    trash_results = []
    if _want_trash:
        for did in reg_ids:
            # Bước NLM hỏng ⇒ CHẶN ngay tại đây, không trash tiếp: mỗi mutation thừa là một thứ nữa
            # phải đi dọn tay, trong khi đằng nào lệnh cũng đã hỏng.
            try:
                _t.guard(f"drive_trash:{did}")
            except TxnBlocked as _blk:
                _blocked = {"blocking_step": _blk.blocking_step, "attempted": _blk.attempted}
                break
            _journal_append(_pf_rid, {"t": "intent", "op": "drive_trash", "key": did, "set": {}})
            try:
                r = g.get("trash", fileId=did, confirm="yes")
            except Exception as e:  # noqa: BLE001
                r = {"ok": False, "error": str(e)}
            _journal_append(_pf_rid, {"t": "commit", "op": "drive_trash", "key": did,
                                      "ok": bool(isinstance(r, dict) and r.get("ok"))})
            _t.record(f"drive_trash:{did}", r, mutating=True, wrote={"drive_id": did})
            trash_results.append({"drive_id": did, "result": r})
    else:
        _t.skipped("drive_trash", "KHONG_YEU_CAU")
    reg_result = None
    if _keep_reg:
        _t.skipped("reg_delete", "KEEP_REGISTRY")
    else:
        # CỔNG QUAN TRỌNG NHẤT của mục này: con trỏ registry chỉ được tháo khi MỌI thao tác ĐƯỢC YÊU CẦU
        # trước đó đã thành công. Hỏng ⇒ `TxnBlocked` ⇒ registry CÒN NGUYÊN ⇒ vẫn còn đường tra ra tài sản.
        try:
            _t.guard("reg_delete")
        except TxnBlocked as _blk:
            _blocked = _blocked or {"blocking_step": _blk.blocking_step, "attempted": _blk.attempted}
        if _blocked is None:
            try:
                reg_result = g.post("reg_delete", drive_ids=json.dumps(reg_ids), confirm="yes", require_removed="no")
            except Exception as e:  # noqa: BLE001
                reg_result = {"ok": False, "error": f"{type(e).__name__}: {e}"}
            _t.record("reg_delete", _pfr_reg_delete_verdict(reg_result, reg_ids),
                      mutating=True, wrote={"registry_drive_ids": reg_ids})
    if not any(s.get("required") for s in _t.steps):
        # Không thao tác nào ĐƯỢC YÊU CẦU (vd `--keep-registry` mà không `--delete-nlm`/`--trash-drive`).
        # Trước đây in `ok:true, rc=0` cho một lệnh KHÔNG LÀM GÌ — nói dối theo hướng vô hại nhưng vẫn là
        # nói dối. `ok` được TÍNH thì câu trả lời đúng là: chưa có gì được chứng minh.
        _t.record("khong_co_thao_tac", {"ok": False, "error": "KHONG_CO_THAO_TAC_NAO_DUOC_YEU_CAU"})
    out = _t.conclude(**{**plan, "nlm_deletes": nlm_results,
                         "nlm_blocked_shared_source_id": nlm_blocked_shared,
                         "drive_trash": trash_results, "reg_delete": reg_result})
    if _blocked:
        out["blocked"] = _blocked
    _rc = _t.rc()
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)), file=(sys.stderr if _rc else sys.stdout))
    return _rc


def cmd_registry_map(a) -> int:
    """(MERGE Claude) VIEW hợp nhất folder+shard+notebook của VBQPPL (base+overflow) và MỌI profile. Dẫn xuất config —
    validate live bằng `tl nlm-get <nb>` / `tl profile-info`. KHÔNG store ghi tay (tránh nguồn-sự-thật-thứ-4 trôi)."""
    path, cfg = _read_config_record(getattr(a, "config", None))
    profs = _profiles_from_config(cfg)

    def _nbs(p, is_base):
        out = []
        nb = p.get("notebookId") or (NLM_BASE_NOTEBOOK if is_base else None)
        if nb:
            out.append({"role": "primary", "id": nb})
        ov = p.get("overflowNotebookId")
        if ov and "-" in str(ov):
            out.append({"role": "overflow_shard", "id": ov})
        # v1.34.49 (F-03): shards[] KHAI BÁO (dict {id,role,capacity,enabled,priority} hoặc str legacy) — trước
        # đây registry-map BỎ QUA hoàn toàn phần tử sau overflow đầu tiên ⇒ không phải bản đồ N-shard.
        _seen = {x["id"] for x in out}
        for s in (p.get("shards") if isinstance(p.get("shards"), list) else []):
            if isinstance(s, dict):
                sid = str(s.get("id") or "").strip()
                row = {"role": ("primary" if s.get("role") == "primary" else "overflow_shard"), "id": sid,
                       "capacity": s.get("capacity"), "enabled": s.get("enabled", True) is not False,
                       "priority": s.get("priority")}
            else:
                sid = str(s or "").strip()
                row = {"role": "overflow_shard", "id": sid}
            if sid and sid not in _seen:
                _seen.add(sid)
                out.append(row)
        return out

    base = profs.get(DEFAULT_PROFILE) or {}
    vbqppl = {"profile": DEFAULT_PROFILE, "rootFolderId": base.get("rootFolderId"),
              "registryDocId": base.get("registryDocId"), "manifestId": base.get("manifestId"), "notebooks": _nbs(base, True)}
    # v1.34.49 (F-09): topology view + hash cho scope nền (declared+env; registry-observed cần manifest — xem doctor)
    try:
        _topo_rm = _resolve_shard_topology([], str(base.get("notebookId") or NLM_BASE_NOTEBOOK),
                                           cfg=cfg, profile=DEFAULT_PROFILE)
        vbqppl["topology"] = {"ok": _topo_rm.get("ok"), "error": _topo_rm.get("error"),
                              "declared": _topo_rm.get("declared"),
                              "topology_hash": _topology_hash(DEFAULT_PROFILE, _topo_rm.get("shards") or []),
                              "findings": _topo_rm.get("findings") or []}
    except Exception:  # noqa: BLE001 — view best-effort
        pass
    others = [{"profile": n, "rootFolderId": p.get("rootFolderId"), "registryDocId": p.get("registryDocId"),
               "manifestId": p.get("manifestId"),
               "categories": (p.get("categories") if isinstance(p.get("categories"), str) else ("own" if p.get("categories") else None)),
               "notebooks": _nbs(p, False)} for n, p in profs.items() if n != DEFAULT_PROFILE]
    print(json.dumps({"ok": True, "config": path, "base_notebook_constant": NLM_BASE_NOTEBOOK, "vbqppl": vbqppl,
                      "profiles": others, "profile_count": len(others),
                      "note": "VIEW dẫn xuất config — validate live: `tl nlm-get <nb>`/`tl profile-info`. KHÔNG store ghi tay."},
                     ensure_ascii=False, indent=2))
    return 0


def _instruction_audit_text(text: str) -> dict:
    low = (text or "").lower()
    missing = [k for k in INSTRUCTION_REQUIRED if k.lower() not in low]
    return {
        "ok": not missing,
        "missing": missing,
        "required": INSTRUCTION_REQUIRED,
        "flags": [] if not missing else ["INSTRUCTION_NOT_BOUND_TO_TRA_LUAT_SKILL"],
        "note": "Fail nghĩa là Claude/NLM Instruction có thể hợp thức hóa lối tắt research_import/source_add(url), tạo notebook tạm, hoặc nạp PDF thô vào NLM mà không đi QT-3.",
    }


def cmd_instruction_audit(a) -> int:
    if getattr(a, "generate", False):
        try:
            import gen_instructions
            # Không dùng VERSION hard-code trong gen_instructions.py; truyền version thật của tl.py
            # và giữ các tham số profile giống lệnh `tl instructions`.
            prof = getattr(a, "profile", None) or os.environ.get("TL_PROFILE") or DEFAULT_PROFILE
            nb = getattr(a, "notebook", None) or os.environ.get("TL_NOTEBOOK_ID") or None
            fld = getattr(a, "folder_name", None) or None
            root = getattr(a, "root_folder_id", None) or os.environ.get("TL_ROOT_FOLDER_ID") or None
            tier = (getattr(a, "tier", None) or "core").lower()   # v1.34.68 Q3
            text = gen_instructions.generate(getattr(a, "target", "both") or "both",
                                             getattr(a, "skill_version", VERSION) or VERSION,
                                             prof, nb, fld, root, tier=tier)
            audit_target = "project" if (getattr(a, "target", "both") or "both") == "config" else (getattr(a, "target", "both") or "both")
            if tier == "full" and audit_target == "project":
                audit_target = "full"                              # ⑤ audit theo REQUIRED_FULL
            out = gen_instructions.audit(text, audit_target) if hasattr(gen_instructions, "audit") else _instruction_audit_text(text)
            out["generated"] = text
        except Exception as e:
            print(f"[tl] instruction-audit: không generate được: {e}", file=sys.stderr)
            return 1
    else:
        if not getattr(a, "file", None):
            print("[tl] instruction-audit cần --file hoặc --generate", file=sys.stderr)
            return 1
        try:
            text = Path(a.file).read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"[tl] instruction-audit lỗi đọc file: {e}", file=sys.stderr)
            return 1
        # #8 backlog (v1.34.17): --file dùng CÙNG nguồn-chân-lý gen_instructions.audit như nhánh --generate
        # (trước: list block riêng trong tl → lệch bản sinh thật → báo 'thiếu khối' GIẢ). Fallback khi thiếu module.
        try:
            import gen_instructions as _gi
            _tgt = getattr(a, "target", "project") or "project"
            _tgt = "project" if _tgt in ("both", "config") else _tgt
            if _tgt == "project" and (getattr(a, "tier", None) or "core").lower() == "full":
                _tgt = "full"                                      # v1.34.68 ⑤: --file + --tier full
            out = _gi.audit(text, _tgt)
        except Exception:  # noqa: BLE001
            out = _instruction_audit_text(text)
    if a.json:
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        if out["ok"]:
            print("OK instruction-audit")
        else:
            print("MISSING: " + ", ".join(out["missing"]))
            print(out["note"])
        if getattr(a, "print_text", False) and out.get("generated"):
            print("\n" + out["generated"])
    return 0 if out["ok"] else 2


def cmd_backfill_notebook(a) -> int:
    """WS1: ghi nlm_notebook_id cho các dòng thuộc 1 notebook (từ danh sách src_ids/drive_ids của
    notebook_get). reg_bulk theo cột nlm_notebook_id. DRY mặc định; --apply mới ghi."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))  # nb default từ TL_NOTEBOOK_ID profile
    nb = (getattr(a, "notebook", None) or os.environ.get("TL_NOTEBOOK_ID") or "").strip()
    # C3 (log rà): KHÓA THEO ĐÚNG NGUỒN INPUT — `--src-ids` → khóa `nlm_source_id`; `--drive-ids` → khóa `drive_id`
    # (TRƯỚC ĐÂY gộp chung 1 list rồi khóa drive_id cho cả 2 → --src-ids LỆCH KHÓA, không khớp). KHÔNG cần --by-src
    # cho 2 cờ này nữa; --by-src CHỈ còn quyết định khóa cho --ids-file (mặc định drive_id).
    src_ids = [x.strip() for x in re.split(r"[,\s]+", (getattr(a, "src_ids", None) or "")) if x.strip()]
    drive_ids = [x.strip() for x in re.split(r"[,\s]+", (getattr(a, "drive_ids", None) or "")) if x.strip()]
    file_ids = []
    if getattr(a, "ids_file", None):
        try:
            file_ids = [x.strip() for x in Path(a.ids_file).read_text(encoding="utf-8").split() if x.strip()]
        except Exception as e:
            print(f"[tl] backfill-notebook: lỗi đọc ids-file: {e}", file=sys.stderr); return 2
    _file_key = "nlm_source_id" if getattr(a, "by_src", False) else "drive_id"
    items, _seen = [], set()
    for k, lst in (("nlm_source_id", src_ids), ("drive_id", drive_ids), (_file_key, file_ids)):
        for i in lst:
            if (k, i) in _seen:
                continue
            _seen.add((k, i)); items.append({k: i, "nlm_notebook_id": nb})
    if not nb or not items:
        print("[tl] backfill-notebook cần --notebook <id> và --src-ids/--drive-ids/--ids-file", file=sys.stderr); return 2
    _key_counts = {"nlm_source_id": sum(1 for it in items if "nlm_source_id" in it),
                   "drive_id": sum(1 for it in items if "drive_id" in it)}
    plan = {"ok": True, "notebook": nb, "keys": _key_counts, "rows": len(items), "mode": "APPLY" if getattr(a, "apply", False) else "DRY",
            "sample": [next(iter(it.items())) for it in items[:8]]}
    if not getattr(a, "apply", False):
        plan["note"] = "Thêm --apply để reg_bulk ghi nlm_notebook_id (cols=nlm_notebook_id)."
        print(json.dumps(plan, ensure_ascii=False, indent=2)); return 0
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))   # cần webapp để reg_bulk
    # v1.29.2 (AUDIT B1 #2): gate + journal + verified-write (trước g.post reg_bulk TRẦN — lọt lưới checkpoint).
    # Items có thể TRỘN khóa (nlm_source_id/drive_id) → tách 2 batch theo key_field (journaled-write 1 khóa/batch).
    ok_gate, _gv = _apply_gate(a, write_cols="nlm_notebook_id")
    if not ok_gate:
        return 2
    run_id = _apply_journal_start("backfill-notebook", {"notebook": nb, "rows": len(items)})
    g = _gas()
    _verified_all = True
    plan["reg_bulk"] = []
    for _kf in ("drive_id", "nlm_source_id"):
        _batch = [it for it in items if _kf in it]
        if not _batch:
            continue
        v = _journaled_reg_write(run_id, g, _batch, "nlm_notebook_id", key_field=_kf,
                                 before_by_key=_reg_before_from_manifest(_batch, ["nlm_notebook_id"], _kf))
        rb = v.get("reg_bulk") or {}
        _verified_all = _verified_all and bool(v.get("verified"))
        plan["reg_bulk"].append({**rb, "key_field": _kf, "verified": bool(v.get("verified")),
                                 **({"error": v.get("error")} if v.get("error") else {})})
    plan["journal"] = run_id
    plan["ok"] = _verified_all
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0 if _verified_all else 1


def cmd_reg_delete(a) -> int:
    """Vá D: gỡ dòng registry theo drive_ids (mảng) — bọc reg_delete đúng tham số. Mặc định BẢO VỆ dòng
    chưa removed* (require_removed); --force để gỡ bất kể status. Chỉ xóa DÒNG registry, KHÔNG đụng Drive/NLM."""
    if getattr(a, "confirm", None) != "yes":
        print(json.dumps({"ok": False, "error": "CONFIRM_REQUIRED", "expected": "yes"},
                         ensure_ascii=False), file=sys.stderr)
        return 2
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    ids = [x.strip() for x in (a.drive_ids or "").split(",") if x.strip()]
    if not ids:
        print("[tl] reg-delete cần --drive-ids id1,id2,...", file=sys.stderr); return 2
    g = _gas()
    r = g.post("reg_delete", drive_ids=json.dumps(ids), confirm="yes",
               require_removed=("no" if getattr(a, "force", False) else "yes"))
    print(json.dumps({"ok": r.get("ok"), "requested": r.get("requested"), "removed": r.get("removed"),
                      "skipped_live": r.get("skipped_live"), "not_found": r.get("not_found")}, ensure_ascii=False, indent=2))
    if r.get("skipped_live"):
        print(f"[tl] {r.get('skipped_live')} dòng bị bảo vệ (chưa removed*); thêm --force nếu chắc chắn.", file=sys.stderr)
    return 0 if r.get("ok") else 1


def cmd_bench(a) -> int:
    """Vá C: đo hiệu năng MỌI tính năng tính-toán-trong-code (offline) trên manifest hiện có → bảng wall-time.
    Webapp/NLM riêng đã có timing qua --timings / tl perf."""
    rounds = getattr(a, "rounds", 1) or 1
    try:
        entries = _manifest_entries()
    except Exception as e:
        print(f"[tl] bench cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    q = getattr(a, "query", None) or "bảo hiểm xã hội"
    nb = os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK
    live_ids = {(_entry_nlm(e) or "").strip() for e in entries if _entry_nlm(e)}
    name0 = (entries[0].get("name") if entries else "") or ""

    def t(fn):
        best = None
        for _ in range(rounds):
            t0 = time.perf_counter(); fn(); dt = (time.perf_counter() - t0) * 1000
            best = dt if best is None else min(best, dt)
        return round(best, 3)

    feats = [
        ("manifest_load", lambda: _manifest_entries()),
        ("resolve_identity", lambda: resolve_identity(q, entries, max_hits=5)),
        ("alias_terms", lambda: _alias_terms(q)),
        ("nlm_reconcile_plan", lambda: _nlm_reconcile_plan(live_ids, entries, nb)),
        ("extract_refs", lambda: extract_refs(name0 + " " + q)),
        ("scan_all_entries", lambda: [(_entry_sohieu(e), _entry_name(e), _entry_row_kind(e)) for e in entries]),
    ]
    rows = []
    for label, fn in feats:
        try:
            rows.append((label, t(fn)))
        except Exception as e:
            rows.append((label, f"ERR {str(e)[:40]}"))
    out = {"ok": True, "entries": len(entries), "rounds": rounds, "timings_ms": dict(rows)}
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"== tl bench · {len(entries)} entries · {rounds} round(s) · best ms ==")
        for label, ms in rows:
            print(f"  {str(ms):>10}  {label}")
    return 0


def _content_md5(text: str) -> str:
    """G1: md5 nội dung (NFC-normalize) để ghi provenance + đối chiếu TOÀN VẸN. '' cho rỗng. Thuần, tất định."""
    import hashlib
    t = unicodedata.normalize("NFC", text or "")
    return hashlib.md5(t.encode("utf-8")).hexdigest() if t else ""


def cmd_source_verify(a) -> int:
    """G1 (cổng NGUỒN): official-first + TOÀN VẸN nội dung. Resolve canonical <sohieu|gdoc> → đọc nội dung (doc/--text-file)
    → content_md5 + số hiệu trong HEADER. Cờ SOURCE_DISCREPANCY nếu header sohieu ≠ registry. Liệt kê nguồn web XẾP THEO
    UY TÍN (vbpl>congbao>.gov>luatvietnam>thuvienphapluat) để đối chiếu ≥N nguồn. Read-only; rc=0 (phát hiện ≠ lỗi),
    --strict → rc=1 nếu discrepancy. KHÔNG tự scrape (dùng link official-first để đối chiếu tay/agent — research=discovery)."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    target = getattr(a, "target", None)
    if not target:
        print("[tl] source-verify cần <sohieu|gdoc> (hoặc --text-file).", file=sys.stderr); return 2
    entry = None
    try:
        entry, _hits = _canonical_for_query(target, refresh=getattr(a, "refresh", False))
    except Exception:
        entry = None
    if entry is None and re.fullmatch(r"[A-Za-z0-9_\-]{20,}", target or ""):
        gdoc = target
    else:
        gdoc = _entry_drive_id(entry) if entry else None
    name = _entry_name(entry) if entry else (target or "")
    reg_sh = _sohieu_key_entry(entry) if entry else norm_sohieu(target)
    text = ""
    tf = getattr(a, "text_file", None)
    if tf:
        try:
            text = Path(tf).read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"[tl] source-verify --text-file lỗi: {e}", file=sys.stderr); return 2
    elif gdoc:
        try:
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        except (Exception, SystemExit):
            pass
        try:
            text = _read_doc_text(gdoc, getattr(a, "config", None)) or ""
        except Exception:
            text = ""
    md5 = _content_md5(text)
    head_shs = sorted({norm_sohieu(m.group(1)) for m in _SOHIEU_RE.finditer((text or "")[:6000])})
    discrepancy = bool(reg_sh and head_shs and reg_sh not in head_shs)
    subj = name or reg_sh or target
    sites = sorted(_DISCOVERY_SITES, key=_official_rank)
    sources = [{"site": s, "rank": _official_rank(s), "url": _google_site_url(subj, s)} for s in sites]
    out = {"ok": True, "gate": "G1", "target": target, "drive_id": gdoc, "name": name,
           "registry_sohieu": reg_sh, "header_sohieu": head_shs, "content_md5": md5, "content_read": bool(text),
           "source_discrepancy": discrepancy, "cross_n": getattr(a, "cross", None) or 2,
           "official_first_sources": sources}
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"== source-verify {target} (G1) ==")
        print(f"  registry sohieu: {reg_sh or '(?)'} | header sohieu: {head_shs or '(chưa đọc)'} | md5: {md5[:12] or '(rỗng)'}")
        if discrepancy:
            print(f"  ⚠ SOURCE_DISCREPANCY: số hiệu registry {reg_sh} KHÔNG có trong header {head_shs}.")
        if not text:
            print("  ⚠ chưa đọc được nội dung (gws/webapp/--text-file) → bỏ md5/đối chiếu header.")
        print(f"  Nguồn đối chiếu ≥{out['cross_n']} (official-first):")
        for s in sources:
            print(f"    [{s['rank']}] {s['site']:24s} {s['url']}")
    return 1 if (getattr(a, "strict", False) and discrepancy) else 0


def _reg_query_row(e: dict) -> dict:
    """#3: KHÓA NLM rõ-nghĩa, khớp tên raw — `on_nlm` (bool có/không trên NLM), `nlm_source_id` (id), `nlm_status`
    (trạng thái). BỎ khóa `nlm` cũ (giữ source_id nhưng dễ đọc nhầm là status → None giả) và `src_id` (sai tên, luôn rỗng)."""
    return {"drive_id": _entry_drive_id(e), "name": _entry_name(e), "cat": _entry_cat(e),
            "sohieu": _entry_sohieu(e), "corpus": str(e.get("corpus")),
            # B7 (v1.33.6 — log rà: reg-query trả loai=None cho MỌI dòng dù loai là khái niệm hạng nhất →
            # không liệt kê được Luật theo loại): phát cả raw lẫn bản CHUẨN HOÁ enum.
            "loai": str(e.get("loai") or ""), "loai_canon": _normalize_loai(str(e.get("loai") or "")),
            # v1.33.42 (MERGE bundle-16 — ROOT CAUSE 'register --title-vn/--goc không persist' hoá ra CHẨN ĐOÁN
            # SAI: field ĐƯỢC ghi đúng [reg_get raw thấy] nhưng projection này THIẾU title_vn+goc → đọc lại =None
            # → tưởng bị bỏ im lặng): phơi title_vn+goc; + sua_doi/hieuluc CÙNG LỚP gap (backfill quan hệ phải
            # reg_get raw mới thấy — agent khỏi suy luận vì sao reg-query 'thiếu' field registry).
            "title_vn": str(e.get("title_vn") or ""), "goc": str(e.get("goc") or ""),
            "sua_doi": str(e.get("sua_doi") or ""), "hieuluc": str(e.get("hieuluc") or ""),
            "on_nlm": _entry_on_nlm_live(e), "nlm_source_id": _entry_nlm(e),
            "nlm_notebook_id": _entry_nlm_notebook_id(e),
            "nlm_status": str(e.get("nlm_status") or ""), "row_kind": _entry_row_kind(e),
            "flags": _title_flags(e)}


def cmd_reg_query(a) -> int:
    """Truy vấn registry/manifest OFFLINE với bộ lọc (thay ~chục snippet json.load+filter tay).
    Lọc: --name (substring), --sohieu, --cat (mã/tiền tố), --nlm/--no-nlm, --row-kind, --corpus/--no-corpus, --mime.
    r180 S7: positional tự do = lọc mờ theo tên (alias --name) — `reg-query "Hien_phap"` chạy được."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    _q80 = (getattr(a, "query", None) or "").strip()
    if _q80:
        if getattr(a, "name", None):
            print(f"[tl] reg-query: có cả positional {_q80!r} lẫn --name → dùng --name.", file=sys.stderr)
        else:
            a.name = _q80   # r180 S7: positional = fuzzy --name (trước đây rc=2 unrecognized arguments)
    # v1.34.58 (C-#11 — Q9=a): --live đọc AUTHORITATIVE qua reg_get (né manifest cache stale — bài học
    # 'manifest không đáng tin' v1.34.50) — CHỈ hợp lệ kèm bộ lọc HẸP (--drive-id | --sohieu | --name);
    # không lọc → LIVE_NEEDS_FILTER rc=2 (reg_get toàn bảng đắt/vô nghĩa; đọc rộng dùng manifest/--refresh).
    _live_mode = bool(getattr(a, "live", False))
    if _live_mode:
        _did_lv = str(getattr(a, "drive_id", None) or "").strip()
        _sh_lv = str(getattr(a, "sohieu", None) or "").strip()
        _nm_lv = str(getattr(a, "name", None) or "").strip()
        if not (_did_lv or _sh_lv or _nm_lv):
            print(json.dumps({"ok": False, "error": "LIVE_NEEDS_FILTER",
                              "note": "--live cần bộ lọc hẹp: --drive-id | --sohieu | --name "
                                      "(đọc rộng: bỏ --live, dùng manifest cache / --refresh)"},
                             ensure_ascii=False), file=sys.stderr)
            return 2
        try:
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))
            _g_lv = _gas()
            if _did_lv:
                _rg_lv = _g_lv.get("reg_get", drive_id=_did_lv, refresh="true")
            elif _sh_lv:
                _rg_lv = _g_lv.get("reg_get", sohieu=norm_sohieu(_sh_lv), refresh="true")
            else:
                _rg_lv = _g_lv.get("reg_get", name_contains=_nm_lv, refresh="true")
        except (SystemExit, Exception) as _e_lv:  # noqa: BLE001
            print(json.dumps({"ok": False, "error": f"LIVE_REG_GET_FAILED: {_e_lv}"},
                             ensure_ascii=False), file=sys.stderr)
            return 2
        if isinstance(_rg_lv, dict) and _rg_lv.get("ok") is False:
            print(json.dumps({"ok": False, "error": "LIVE_REG_GET_FAILED",
                              "detail": str(_rg_lv.get("error") or "")[:200]},
                             ensure_ascii=False), file=sys.stderr)
            return 2
        entries = list((_rg_lv or {}).get("rows") or [])
    # v1.34.42 (BUG2 — grill-with-docs): `--refresh` cần creds LIVE (TL_WEBAPP) để fetch — apply_profile_offline
    # KHÔNG đảm bảo có. Trước đây thiếu bước này → `--refresh` chết 'Thiếu TL_WEBAPP' làm tưởng MẤT token (thực ra
    # chỉ chưa nạp creds LIVE). Khuôn y locate/status: nạp load_creds TRƯỚC refresh (self-heal từ config).
    if not _live_mode:
        if getattr(a, "refresh", False):
            try:
                load_creds(getattr(a, "config", None), getattr(a, "profile", None))
            except (SystemExit, Exception):  # noqa: BLE001 — thiếu creds → rơi xuống thông điệp cụ thể bên dưới
                pass
        try:
            entries = _manifest_entries(refresh=getattr(a, "refresh", False))
        except Exception as e:
            _hint = (" `--refresh` cần webapp LIVE — chạy `tl --profile <P> boot --refresh` (hoặc bỏ `--refresh` "
                     "để đọc cache).") if getattr(a, "refresh", False) else ""
            print(f"[tl] reg-query: cần `tl boot`/`manifest` trước ({e}).{_hint}", file=sys.stderr); return 2
    # v1.34.42 (BUG3): nhắc `--corpus true` là LITERAL cột — audit 'corpus như server' phải dùng --corpus-effective.
    if getattr(a, "corpus", False) and not getattr(a, "corpus_effective", False):
        print("[tl] ⚠ `--corpus true` = literal cột corpus=='true' (mọi row_kind, kể cả overflow/blank-trên-NLM bị "
              "BỎ SÓT). Muốn corpus theo LUẬT SERVER (như `tl boot` đếm) dùng `--corpus-effective`.", file=sys.stderr)
    # v1.34.42 (BUG3, live-smoke bắt): luật server corpus (corpus∈{true,vbqppl}∪overflow − ref − thuong) CHỈ đúng cho
    # scope NỀN vbqppl; profile riêng đếm khác (server: mọi dòng có drive_id) → --corpus-effective trên profile có thể
    # ra 0/sai (ca Luật BHXH: 14 dòng corpus=true đều row_kind=ref → effective=0). Cảnh báo, không chặn.
    if getattr(a, "corpus_effective", False) and _active_profile() != DEFAULT_PROFILE:
        print(f"[tl] ⚠ `--corpus-effective` dùng LUẬT SERVER NỀN (vbqppl) nhưng scope hiện tại = profile "
              f"'{_active_profile()}' (đếm khác: mọi dòng có drive_id). Kết quả có thể LỆCH/BẰNG 0 — với profile "
              f"dùng `--nlm` hoặc reg-query toàn dòng rồi lọc tay.", file=sys.stderr)
    nm = (getattr(a, "name", None) or "").lower()
    shq = norm_sohieu(getattr(a, "sohieu", None) or "") if getattr(a, "sohieu", None) else ""
    cat = (getattr(a, "cat", None) or "").strip()
    rk = (getattr(a, "row_kind", None) or "").strip().lower()
    mime = (getattr(a, "mime", None) or "").lower()
    # B7 (v1.33.6): lọc theo LOẠI — so bản CHUẨN HOÁ enum ('luat'/'Luật' ≡ 'Luật'; 'Bộ luật' là loại RIÊNG).
    loai_q = _normalize_loai(str(getattr(a, "loai", None) or "")) or str(getattr(a, "loai", None) or "").strip()

    nm_q = getattr(a, "name", None) or ""
    did = (getattr(a, "drive_id", None) or "").strip()
    _nbq = str(getattr(a, "notebook", None) or "").strip()   # v1.34.53 (A6): lọc theo nlm_notebook_id
    def ok(e):
        if _nbq and str(e.get("nlm_notebook_id") or "").strip() != _nbq:
            return False
        if did and did not in (str(e.get("drive_id") or ""), str(e.get("gdoc_id") or ""), str(e.get("gdoc") or "")):
            return False
        if nm:
            # khớp tên: substring KHÔNG-dấu HOẶC token-subset phân biệt (đồng bộ với locate/source-map; trước đây chỉ
            # substring CÓ DẤU trên _entry_name → "Bảo hiểm xã hội" vs "...bao_hiem_xa_hoi" = 0 kết quả).
            if not _entry_query_match(nm_q, e, include_subject=True):
                return False
        # v1.33.47: bare-VBHN 1 chiều — '88/VBHN-VPQH' (web, không năm) khớp entry '88-2025-VBHN-VPQH'
        # (trước: substring miss vì năm chèn giữa → 'lần nào chạy cũng báo thiếu' với MỌI VBHN đã có).
        if shq and not _sohieu_query_hits_entry(shq, _sohieu_key_entry(e), substring=True):
            return False
        if loai_q:
            _el = _normalize_loai(str(e.get("loai") or "")) or str(e.get("loai") or "").strip()
            if _el != loai_q:
                return False
        if cat:
            ec = str(_entry_cat(e) or "")
            want = cat.lower()
            if want in ("root", "(root)"):
                if ec not in ("(root)", ""):
                    return False
            elif not (ec.startswith(cat) or ec.split("_")[0] == cat or ec.lower() == want):
                return False
        if getattr(a, "nlm", False) and not _entry_on_nlm_live(e):
            return False
        if getattr(a, "no_nlm", False) and _entry_on_nlm_live(e):
            return False
        if getattr(a, "corpus", False) and str(e.get("corpus")).lower() != "true":
            return False
        if getattr(a, "no_corpus", False) and str(e.get("corpus")).lower() == "true":
            return False
        # v1.34.42 (BUG3): `--corpus-effective` lọc theo ĐÚNG LUẬT SERVER (corpus∈{true,vbqppl}∪overflow − ref −
        # thuong) — KHÁC `--corpus true` literal (bỏ sót vbqppl/overflow/blank-trên-NLM → audit thiếu, ca Luật BHXH
        # 14 vs 41). Dùng khi cần 'corpus như boot/server đếm'.
        if getattr(a, "corpus_effective", False) and not _entry_is_corpus_effective(e):
            return False
        if rk and _entry_row_kind(e) != rk:
            return False
        if mime and mime not in str(e.get("mime", "")).lower():
            return False
        return True

    hits = [e for e in entries if ok(e)]
    # A (v1.30.0): profile CỘNG VBQPPL — hợp nhất thêm hit từ manifest NỀN (profile trước, nền bổ sung, dedup drive_id).
    # v1.34.58 (C-#11): live mode KHÔNG merge nền từ cache (authoritative không trộn stale).
    _base_note = None
    if not _live_mode and _base_also_enabled(a):
        _b_entries, _b_err = _base_manifest_entries(getattr(a, "config", None))
        _n0 = len(hits)
        hits = _merge_base_entries(hits, [e for e in _b_entries if ok(e)])
        _base_note = {"enabled": True, "base_hits": len(hits) - _n0, "base_error": _b_err}
    _is_json = getattr(a, "json", False) or bool(getattr(a, "out", None))   # S-4 (v1.33.34): --out tự bật JSON
    # FIX undercount âm thầm: --json là cho TOOL → trả TẤT CẢ rows mặc định (trước cắt 60 → script đếm len(rows) thiếu,
    # vd audit quarantine 60/110). Text mode vẫn cắt 60 cho dễ đọc (có dòng "(hiện 60)"). --limit để ép trần.
    lim = getattr(a, "limit", None) or (len(hits) if _is_json else 60)
    if _is_json:
        # reg-query --json envelope chuẩn (rows + entries cho mọi parser; ok/count/limit/truncated để công cụ kiểm tải).
        _rows = [_reg_query_row(e) for e in hits[:lim]]
        for _r, _e in zip(_rows, hits[:lim]):
            if _e.get("scope") == "vbqppl":
                # r179 T5: MỘT từ vựng scope — row nền mang scope:'vbqppl' + cờ BASE_SCOPE_HIT (đồng nhất
                # source-map/exists/locate; khoá `_scope` riêng đã BỎ). Đếm "của profile" = loại đúng 2 dấu này.
                _r["scope"] = "vbqppl"
                _r["flags"] = list(dict.fromkeys(list(_r.get("flags") or []) + ["BASE_SCOPE_HIT"]))
        _env = {"ok": True, "schema": "reg-query.v2", "count": len(hits), "limit": lim,
                "truncated": len(hits) > lim, "rows": _rows, "entries": _rows}
        if _live_mode:
            _env["source"] = "live"   # v1.34.58 (C-#11): rows từ reg_get authoritative, không phải manifest cache
        if _base_note:
            _env["base_also"] = _base_note
        _emit_json_payload(_env, getattr(a, "out", None))   # S-4 (v1.33.34): atomic --out, mirror doctor/sweep
    else:
        for e in hits[:lim]:
            _sc = " [nền]" if e.get("scope") == "vbqppl" else ""
            print(f"  {_entry_drive_id(e)}\tcat={str(_entry_cat(e)).split('_')[0]:3s} "
                  f"corpus={'Y' if str(e.get('corpus')).lower()=='true' else '-'} nlm={_nlm_display(e)}  {_entry_name(e)[:54]}{_sc}")
        print(f"— {len(hits)} kết quả" + (f" (hiện {lim})" if len(hits) > lim else ""))
        if len(hits) > lim:
            print(f"  ⚠ LIMIT_TRUNCATED: chỉ hiện {lim}/{len(hits)} dòng — thêm `--limit {len(hits)}` (hoặc `--json` để lấy đủ) khi thống kê toàn corpus.")
    return 0


def cmd_cat_verify(a) -> int:
    """G3 (cổng category theo NỘI DUNG): đọc phạm vi điều chỉnh/Điều 1 của <gdoc|sohieu> → suy cat bằng alias TRÊN
    NỘI DUNG (không chỉ tên) + ÉP quy_tac_ranh_gioi. Read-only (KHÔNG mutate). Trả cat_suggested/confidence/rule_applied/
    tie/cat_current/in_taxonomy. rc=0 (phát hiện ≠ lỗi); --strict → rc=1 nếu lệch cat hiện tại. --text-file để chạy OFFLINE."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    target = getattr(a, "target", None)
    if not target:
        print("[tl] cat-verify cần <gdoc|sohieu> (hoặc --text-file để offline).", file=sys.stderr); return 2
    entry = None
    try:
        entry, _hits = _canonical_for_query(target, refresh=getattr(a, "refresh", False))
    except Exception:
        entry = None
    if entry is None and re.fullmatch(r"[A-Za-z0-9_\-]{20,}", target or ""):
        gdoc = target                       # target LÀ gdoc-id trực tiếp
    else:
        gdoc = _entry_drive_id(entry) if entry else None
    name = _entry_name(entry) if entry else (target or "")
    cat_current = str(_entry_cat(entry) or "") if entry else ""
    cur_code = cat_current.split("_")[0] if re.match(r"\d", cat_current) else ("00" if cat_current.startswith("00") else "")
    text = ""
    tf = getattr(a, "text_file", None)
    if tf:
        try:
            text = Path(tf).read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"[tl] cat-verify --text-file lỗi: {e}", file=sys.stderr); return 2
    elif gdoc:
        try:
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))   # best-effort cho _read_doc_text
        except (Exception, SystemExit):
            pass
        try:
            text = _read_doc_text(gdoc, getattr(a, "config", None)) or ""
        except Exception:
            text = ""
    d1 = (extract_dieu(text, 1) or "") if text else ""
    basis = name + "\n" + d1 + "\n" + text[:6000]
    forced, rule = _cat_boundary_rule(basis)
    scored = _infer_cats_text(basis)
    if forced:
        cat_suggested, confidence, rule_applied, tie = forced, "high", rule, []
    elif scored:
        top = scored[0][1]; second = scored[1][1] if len(scored) > 1 else 0
        cat_suggested = scored[0][0]
        confidence = ("high" if (text and top >= 2 and top >= 2 * max(second, 1))
                      else ("medium" if text else "low"))
        rule_applied = None
        tie = [c for c, sc, _ in scored[1:] if sc == top]
    else:
        cat_suggested, confidence, rule_applied, tie = "", "low", None, []
    out = {"ok": True, "gate": "G3", "target": target, "drive_id": gdoc, "name": name,
           "cat_current": cur_code, "cat_suggested": cat_suggested, "confidence": confidence,
           "rule_applied": rule_applied, "tie": tie, "content_read": bool(text),
           "in_taxonomy": (cat_suggested in _cat_taxonomy()) if cat_suggested else False,
           "mismatch": bool(cat_suggested and cur_code and cat_suggested != cur_code),
           "matches": [{"cat": c, "score": sc, "alias": al} for c, sc, al in scored]}
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"== cat-verify {target} ==")
        print(f"  hiện tại: {cur_code or '(?)'} | gợi ý: {cat_suggested or '(?)'} ({confidence})"
              + (f" | rule: {rule_applied}" if rule_applied else "")
              + (f" | tie: {','.join(tie)}" if tie else ""))
        if not text:
            print("  ⚠ CHƯA đọc được nội dung (cần gws/webapp, hoặc --text-file) → suy theo TÊN, độ tin THẤP.")
        if out["mismatch"]:
            print(f"  ⚠ MISMATCH: folder {cur_code} ≠ gợi ý {cat_suggested}. (tl recat <drive_id> --cat {cat_suggested} [--force-cat] --apply)")
    return 1 if (getattr(a, "strict", False) and out["mismatch"]) else 0


def _registry_claim_by_notebook(entries: list) -> dict:
    """PURE (v1.33.48 — rà Instruction 'Luật BHXH' manifest_fallback: 'khi tính slot NLM, chỉ đếm rows có
    nlm_notebook_id == notebook đích, không đếm mọi nlm_status'): breakdown claim theo nlm_notebook_id —
    registry_claim_nlm gộp MỌI shard/notebook nên vô dụng cho kế toán slot per-notebook. Vẫn là ESTIMATE
    (offline); chốt FULL bằng LIVE."""
    from collections import Counter
    c = Counter((str(e.get("nlm_notebook_id") or "").strip() or "(trống)") for e in (entries or []) if _entry_nlm(e))
    return dict(sorted(c.items(), key=lambda kv: (-kv[1], kv[0])))


def _registry_claim_target(entries: list, nb: str) -> int | None:
    """PURE (v1.33.48): claim ĐÚNG SCOPE notebook đích = nlm_notebook_id == nb VÀ status live (loại removed*/
    deleted — 'không đếm mọi nlm_status'). None nếu không có notebook đích."""
    nb = (nb or "").strip()
    if not nb:
        return None
    return sum(1 for e in (entries or []) if _entry_on_nlm_live(e) and str(e.get("nlm_notebook_id") or "").strip() == nb)


def cmd_counts(a) -> int:
    """B (v1.33.9 — 5 log rà liên tiếp vấp '6 con số corpus khác nhau' 743/509/521/531/110-68/544-295): MỘT BẢNG
    mẫu số trên CÙNG snapshot, mỗi dòng ghi rõ ĐỊNH NGHĨA — diệt bẫy nhận thức khi đối soát nhanh. OFFLINE;
    NLM VẬT LÝ luôn phải neo `tl nlm-get <nb>` LIVE (L4/L5) — ở đây chỉ in registry-claim kèm nhãn ESTIMATE.
    v1.33.48: +registry_claim_target_nb (nlm_notebook_id==đích + live-status) + registry_claim_by_notebook."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:  # noqa: BLE001
        print(f"[tl] counts: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    _luat = [e for e in entries if _normalize_loai(str(e.get("loai") or "")) in ("Luật", "Bộ luật")]
    rows = [
        ("registry_rows", len(entries),
         "mọi dòng registry/manifest (own+ref+overflow, kể cả quarantine/thường)"),
        ("corpus_client", sum(1 for e in entries if str(e.get("corpus")).lower() == "true"),
         "corpus=='true' thuần (= sweep.corpus)"),
        ("corpus_server_rule", _corpus_count_server_rule(entries),
         "luật GAS regIsCorpusCounted_ (= tl boot = sweep.corpus_server_rule_equiv)"),
        ("corpus_audit_pool", sum(1 for e in entries if _entry_drive_id(e)
                                  and str(e.get("corpus") or "").lower() != "false" and not _entry_quarantined(e)),
         "pool corpus-audit --all: có drive_id + corpus≠false + không quarantine"),
        ("luat_loai_all", len(_luat), "loai canon ∈ {Luật, Bộ luật} — MỌI dòng (cả bản thô corpus=false)"),
        ("luat_corpus", sum(1 for e in _luat if str(e.get("corpus")).lower() == "true"),
         "trong đó corpus=true (review-queue quét nhóm này, trừ VBHN đội lốt loai)"),
        ("registry_claim_nlm", sum(1 for e in entries if _entry_nlm(e)),
         "dòng có nlm_source_id — ESTIMATE (gồm shard khác + đã gỡ); VẬT LÝ: `tl nlm-get <nb>` LIVE"),
    ]
    # v1.33.48 (Instruction 'Luật BHXH'): claim ĐÚNG SCOPE notebook đích — nlm_notebook_id == đích + live-status
    # (loại removed*). registry_claim_nlm gộp mọi shard nên KHÔNG dùng ước lượng slot per-notebook được.
    _nb_target = ((getattr(a, "notebook_id", None) or "").strip()
                  or (os.environ.get("TL_NOTEBOOK_ID") or "").strip()
                  or (NLM_BASE_NOTEBOOK if _active_profile() == DEFAULT_PROFILE else ""))
    _claim_tgt = _registry_claim_target(entries, _nb_target)
    if _claim_tgt is not None:
        rows.append(("registry_claim_target_nb", _claim_tgt,
                     f"nlm_notebook_id == đích ({_nb_target[:12]}…) + status live — ước lượng ĐÚNG SCOPE; chốt FULL vẫn bằng LIVE"))
    _age = _manifest_cache_age_seconds()
    out = {"ok": True, "snapshot_age_s": None if _age is None else int(_age),
           "counts": {k: v for k, v, _ in rows}, "basis": {k: b for k, _, b in rows},
           "target_notebook": _nb_target or None,
           "registry_claim_by_notebook": _registry_claim_by_notebook(entries),
           "note": "CÙNG snapshot manifest — lệch giữa các mẫu số là ĐỊNH NGHĨA, không phải mất dữ liệu; "
                   "khớp live: `tl boot --refresh` rồi `tl counts --refresh` cùng phiên.",
           "slot_rule": "registry_claim_nlm là ESTIMATE gộp MỌI notebook; ước lượng slot theo đích dùng "
                        "registry_claim_target_nb; FULL/overflow chỉ chốt bằng NLM LIVE."}
    if getattr(a, "live_nlm", False):
        nb, nberr = _resolve_nlm_notebook(getattr(a, "notebook_id", None))
        if nberr:
            out["nlm_live"] = {"ok": False, "error": nberr}
        else:
            try:
                r = _imp("nlm_cli").notebook_get(nb)
                cap = NLM_SLOT_CAP
                used = int(r.get("source_count") or 0) if r.get("ok") else None
                out["nlm_live"] = {"ok": bool(r.get("ok")), "notebook": nb, "source_count": used,
                                   "cap": cap, "remaining": (None if used is None else max(0, cap - used)),
                                   "near_full": (None if used is None else used >= cap - 5),
                                   "title": r.get("title"), "error": r.get("error"),
                                   "basis": "LIVE notebook_get/nlm-get — nguồn đúng để chốt slot"}
            except Exception as e:  # noqa: BLE001
                out["nlm_live"] = {"ok": False, "notebook": nb, "error": f"{type(e).__name__}: {e}"}
    if getattr(a, "json", False) or getattr(a, "out", None):
        _emit_json_payload(out, getattr(a, "out", None))
    else:
        print(f"== tl counts · snapshot {out['snapshot_age_s'] if out['snapshot_age_s'] is not None else '?'}s ==")
        for k, v, b in rows:
            print(f"  {k:<20s} {v:>5d}  — {b}")
        _bynb = out.get("registry_claim_by_notebook") or {}
        if _bynb:
            print("  claim theo notebook: " + ", ".join(
                (f"{k[:12]}…={v}" if k != "(trống)" else f"(trống)={v}") for k, v in list(_bynb.items())[:4]))
        live = out.get("nlm_live")
        if live:
            if live.get("ok"):
                print(f"  nlm_live{'':<13s} {live.get('source_count'):>5d}/{live.get('cap')}  — VẬT LÝ LIVE notebook={str(live.get('notebook'))[:12]}… remaining={live.get('remaining')}"
                      + ("  ⚠ gần/full" if live.get("near_full") else ""))
            else:
                print(f"  nlm_live{'':<13s}     ?  — không lấy được LIVE: {live.get('error')}")
        print(f"  ℹ {out['note']} {out['slot_rule']} Dùng `--live-nlm` để in ngay số vật lý.")
    return 0


def _entries_with_live_fields(entries: list, live_rows: list, fields=_LOOP_LIVE_FIELDS) -> list:
    """PURE (v1.29.3 — AUDIT B2 #4): OVERLAY các trường MUTABLE từ registry-sheet LIVE (gws, raw rows) lên entries
    manifest ĐÃ-LÀM-GIÀU. GIỮ NGUYÊN shape/enrichment manifest (so_hieu canonical, issue_year… — tránh đúng loại
    phân kỳ R1 đã né); CHỈ thay giá trị corpus/nlm_* — thứ duy nhất đổi giữa các vòng loop. Khớp theo drive_id;
    entry không khớp → giữ nguyên. Trả list entries MỚI (copy shallow từng entry được overlay)."""
    by_did = {}
    for r in live_rows or []:
        d = str(r.get("drive_id") or "")
        if d:
            by_did[d] = r
    out = []
    for e in entries or []:
        r = by_did.get(_entry_drive_id(e))
        if r is None:
            out.append(e)
            continue
        e2 = dict(e)
        for f in fields:
            if f in r:
                e2[f] = r.get(f)
        out.append(e2)
    return out


def cmd_loop(a) -> int:
    """(Pha 3) LOOP HỢP NHẤT có cổng-verify + hội tụ + fail-safe — khép kín triết lý 'không bỏ bước, không né quy trình'.
    Mỗi vòng: detect (tầng an toàn infra+dedup) → set corpus=false (VERIFIED-write + JOURNAL) → re-detect. HỘI TỤ khi hết
    việc (`--dry-rounds` vòng); PAUSE khi no-progress / max-iter / verify HỤT. CHỈ tầng REVERSIBLE (undo được: `tl undo`);
    metadata/human vẫn qua `corpus-fix` DRY, người duyệt. DRY mặc định (1 vòng detect); --apply chạy vòng lặp thật."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    k_dry = getattr(a, "dry_rounds", None) or 2
    max_iter = getattr(a, "max_iter", None) or 8
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:  # noqa: BLE001
        print(f"[tl] loop: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    sr0 = _corpus_safe_reversible(entries)
    if not getattr(a, "apply", False):
        out = {"ok": True, "mode": "DRY", "detect_now": len(sr0["ids"]), "infra": sr0["infra"], "dedup": sr0["dedup"],
               "k_dry": k_dry, "max_iter": max_iter,
               "note": "--apply: mỗi vòng set corpus=false (verified+journaled) rồi RE-DETECT đến HỘI TỤ; fail-safe PAUSE nếu "
                       "no-progress/verify hụt/max-iter. Hoàn tác toàn bộ: `tl undo <journal>`. (metadata/human: `corpus-fix` DRY.)"}
        print(_json_dumps(out, deterministic=_deterministic_enabled(a))) if getattr(a, "json", False) else \
            print(f"== loop DRY · phát hiện {len(sr0['ids'])} việc reversible (infra {sr0['infra']} + dedup {sr0['dedup']}) · "
                  f"k_dry={k_dry} max_iter={max_iter} · --apply để chạy vòng lặp (verified+journaled+fail-safe) ==")
        return 0
    _ok_gate, _ = _apply_gate(a, write_cols="corpus")
    if not _ok_gate:
        return 2
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    g = _gas()
    run_id = _apply_journal_start("loop", {"k_dry": k_dry, "max_iter": max_iter})
    rounds, status, reason, done_ids = [], "continue", "", set()
    _base_entries = None      # entries manifest-enriched của vòng 1 — nền cho overlay gws-live các vòng sau
    _rid_live = (os.environ.get("TL_REGISTRY_DOC_ID") or "").strip()
    for _i in range(max_iter):
        # v1.29.3 (AUDIT B2 #4 — bỏ N+1 manifest_export): vòng 1 = manifest refresh (nền enriched, authoritative);
        # vòng ≥2 CHỈ cần trạng thái MỚI của trường mutable (corpus/nlm_*) → đọc registry-sheet LIVE qua gws (~1.2s,
        # KHÔNG re-export + KHÔNG dính cache đọc GAS 600s) rồi OVERLAY lên nền vòng 1 (shape enriched GIỮ NGUYÊN —
        # không phân kỳ detector). gws lỗi/thiếu → FALLBACK đúng hành vi cũ: manifest refresh=True (chậm hơn, vẫn đúng).
        if _i == 0 or _base_entries is None:
            entries = _manifest_entries(refresh=True)
            _base_entries = entries
        else:
            _rows = None
            try:
                _rows = _imp("tl_gws")._gws_read_registry_rows(_rid_live, REGISTRY_SCHEMA_COLS) if _rid_live else None
            except Exception:  # noqa: BLE001
                _rows = None
            if _rows is not None:
                entries = _entries_with_live_fields(_base_entries, _rows)
                print(f"  [vòng {_i + 1}] re-detect trên gws-live overlay ({len(_rows)} dòng sheet)", file=sys.stderr, flush=True)
            else:
                entries = _manifest_entries(refresh=True)      # fallback = hành vi cũ
                _base_entries = entries
        sr = _corpus_safe_reversible(entries)
        # LOẠI id ĐÃ xử trong phiên (done_ids): GAS cache registry ~600s → re-read có thể VẪN thấy corpus=true dòng vừa set
        # → nếu đếm lại sẽ NO_PROGRESS GIẢ. Hội tụ dựa trạng thái TRONG-PHIÊN, không phụ thuộc GAS lan truyền.
        todo_ids = [x for x in sr["ids"] if x not in done_ids]
        remaining = len(todo_ids)
        fixed, verify_ok = 0, True
        if remaining:
            items = [{"drive_id": x, "corpus": "false"} for x in todo_ids]
            before = {x: {"corpus": "true"} for x in todo_ids}
            v = _journaled_reg_write(run_id, g, items, "corpus", before_by_key=before)
            fixed = v.get("patched") or 0
            verify_ok = bool(v.get("verified"))
            done_ids.update(todo_ids)
            _invalidate_manifest_cache()
        rounds.append({"fixed": fixed, "remaining": remaining})
        _journal_append(run_id, {"t": "step", "iter": _i + 1, "remaining": remaining, "fixed": fixed, "verify_ok": verify_ok})
        print(f"  [vòng {_i + 1}] phát hiện {remaining} · sửa {fixed} · verify={'ok' if verify_ok else 'HỤT'}", file=sys.stderr, flush=True)
        if not verify_ok:      # cổng-verify từng bước: ghi không xác nhận → DỪNG (fail-safe, không lặp mù)
            status, reason = "paused", "VERIFY_FAILED: ghi corpus=false KHÔNG xác nhận → DỪNG (fail-safe)"; break
        dec = _loop_controller(rounds, k_dry, max_iter)
        status, reason = dec["status"], dec["reason"]
        if status in ("converged", "paused"):
            break
    _journal_append(run_id, {"t": "run_end", "ok": status == "converged", "counts": {"rounds": len(rounds), "status": status}})
    _invalidate_manifest_cache()
    print(json.dumps({"ok": status == "converged", "status": status, "reason": reason, "rounds": rounds, "journal": run_id,
                      "note": f"Hoàn tác toàn bộ: `tl undo {run_id} --apply --confirm yes`. Còn metadata/human: `corpus-fix` DRY."},
                     ensure_ascii=False, indent=2))
    return 0 if status == "converged" else 1


def cmd_cat_list(a) -> int:
    """(4) Liệt kê 45 chủ đề pháp điển chính thức + trạng thái folder."""
    pd = _load_phapdien()
    if not pd:
        print("[tl] thiếu references/phap_dien_45.json", file=sys.stderr); return 2
    folders_now = _valid_cats(getattr(a, "config", None), getattr(a, "profile", None))
    only_missing = getattr(a, "missing", False)
    rows = sorted(pd.items())
    for code, info in rows:
        has = code in folders_now
        if only_missing and has:
            continue
        mark = "✓" if has else "·(chưa có folder)"
        print(f"  {code}  {mark:18s} {info.get('ten')}   [{info.get('folder')}]")
    print(f"— {sum(1 for c in pd if c in folders_now)}/{len(pd)} chủ đề đã có folder (gồm 00/46 custom).")
    return 0


def cmd_convert_verify(a) -> int:
    g = _gas()
    out = _verify_convert_readback(g, gdoc_id=a.gdoc_id, expected_name=getattr(a, "expected_name", "") or "",
                                   src_id=getattr(a, "src_id", "") or "", expected_src_name=getattr(a, "expected_src_name", "") or "",
                                   expected_folder_id=getattr(a, "expected_folder_id", "") or "")
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0 if out.get("ok") else 2

# ── I11 (v1.34.18): leftover-sweep từ tl.py (affinity-tốt-nhất) ──


def _corpus_safe_reversible(entries: list) -> dict:
    """Tập AN TOÀN ĐẢO-NGƯỢC cần set corpus=false: infra lẫn corpus (_sweep_report) + dup (dedup_plan ready). Dùng CHUNG
    `corpus-fix --tier safe` và `loop`. Trả {ids, infra, dedup} (giữ breakdown cho output corpus-fix)."""
    infra_ids = [r["drive_id"] for r in _sweep_report(entries)["infra_in_corpus_rows"] if r.get("drive_id")]
    dp = _dedup_plan(entries)
    dup_ids = [d["drive_id"] for it in dp["ready"] for d in it["quarantine"] if d.get("drive_id")]
    return {"ids": list(dict.fromkeys(infra_ids + dup_ids)), "infra": len(infra_ids), "dedup": len(dup_ids)}

def _reassemble_parts(name: str) -> str | None:
    """ĐÃ BỎ cơ chế `_parts/` (chia nhỏ chống mount-cắt-cụt) — Cowork nay bootstrap qua `tl_fetch.sh` tải bản zip
    SẠCH từ Drive (không qua mount nên không cắt cụt) → `_parts` hết tác dụng, đã xoá khỏi skill. Hàm GIỮ chữ ký
    (luôn None) để mọi caller heal degrade an toàn về bản on-disk (strip-NUL nếu cần)."""
    return None

def _compiles(text) -> bool:
    if text is None:
        return False
    try:
        compile(text, "<integrity>", "exec"); return True
    except SyntaxError:
        return False

def _nlm_probe_summary(env=None) -> dict:
    """Canary NLM không mạng: tl dùng absolute path nội bộ, nhưng shell non-interactive có thể không thấy `nlm`."""
    import shutil as _sh
    try:
        nc = _imp("nlm_cli")
        tl_path = nc.nlm_exe() or ""
    except Exception:
        tl_path = ""
    shell_path = _sh.which("nlm") or ""
    try:
        st = _imp("tl_gws")._nlm_install_probe(nlm_path=tl_path or shell_path or None)
    except Exception as e:  # noqa: BLE001
        st = {"next_step": "unknown", "error": f"{type(e).__name__}: {e}", "nlm": tl_path or shell_path}
    return {"tl_nlm_path": tl_path, "shell_nlm_path": shell_path, "probe": st,
            "path_note": ("OK: shell cũng thấy nlm" if shell_path else
                          "shell non-interactive có thể chưa thấy nlm; dùng `tl nlm-*` hoặc export PATH=$HOME/.local/bin:$PATH")}

def _doctor_exporttext_probe_target(entries: list[dict]) -> dict | None:
    """MERGE Codex v1.33.10→v1.33.11: chọn một GDoc nhẹ để `doctor --deep` kiểm riêng GAS exporttext/scope.
    Không dùng file thô vì lỗi raw không nói gì về OAuth scope."""
    cands = [e for e in (entries or []) if _entry_google_doc(e) and _entry_corpus_true(e)]
    if not cands:
        cands = [e for e in (entries or []) if _entry_google_doc(e)]
    cands.sort(key=_entry_score, reverse=True)
    return cands[0] if cands else None

def _canonical_for_query(q: str, refresh: bool=False) -> tuple[dict|None, list[dict]]:
    key = norm_sohieu(q)
    qn = _strip_accents(q).lower()
    # EXACT-SỐ-HIỆU PRIORITY: khi query SUY RA được số hiệu THẬT (vd '45/2019/QH14', '18/VBHN-VPQH') thì khớp số hiệu
    # CHÍNH XÁC LUÔN thắng fuzzy by-name — chống name-collision (1 VBHN/luật khác chỉ trùng cụm tên/dẫn-chiếu thắng nhờ
    # _entry_score cao). KHÔNG đụng VBHN-first redirect (doctrine ở _source_map_one.related_vbhn).
    shkey = norm_sohieu(q.replace("_", "-")) if _looks_like_sohieu_query(q) else ""
    entries = _manifest_entries(refresh=refresh)
    hits, exact = [], []
    for e in entries:
        sh = norm_sohieu(_entry_sohieu(e))
        nm = _strip_accents(_entry_name(e)).lower()
        # Fallback: entry có sohieu RỖNG trong registry nhưng TÊN mang số hiệu (vd '114_2025_QH15_658530').
        # _sohieu_key_entry parse từ tên + .replace('_','-')→norm_sohieu (khớp '114-2025-QH15'); trả '' cho tên Mẫu_/PL_.
        is_exact = bool(shkey) and (sh == shkey or _sohieu_key_entry(e) == shkey)
        if is_exact or (key and sh == key) or (qn and qn in nm) or (key and _sohieu_key_entry(e) == key):
            hits.append(e)
            if is_exact:
                exact.append(e)
    hits.sort(key=_entry_score, reverse=True)
    exact.sort(key=_entry_score, reverse=True)
    # direct exact-sohieu LUÔN ưu tiên hơn by-name fuzzy; trong mỗi nhóm vẫn lấy _entry_score cao nhất.
    canonical = exact[0] if exact else (hits[0] if hits else None)
    return canonical, hits

def _alias_terms(s: str) -> set:
    """Trả tập term chuẩn hóa của s, MỞ RỘNG theo alias 2 chiều (BHXH↔bao hiem xa hoi…)."""
    global _ALIAS_INDEX
    if _ALIAS_INDEX is None:
        _ALIAS_INDEX = {}
        for canon, abbrs in _ALIASES:
            members = set([canon] + abbrs)
            for m in members:
                _ALIAS_INDEX.setdefault(m, set()).update(members)
    plain = _strip_accents(str(s or "")).lower()
    terms = {plain}
    for m, group in _ALIAS_INDEX.items():
        if m and m in plain:
            terms |= group
    return {t for t in terms if t}

def _official_rank(url: str) -> int:
    """G1: hạng UY TÍN nguồn (NHỎ = chính thống hơn). 1=vbpl/congbao, 2=.gov.vn/.chinhphu.vn, 3=luatvietnam,
    4=thuvienphapluat, 5=khác. Dùng xếp nguồn đối chiếu official-first + gate G1."""
    u = (url or "").lower()
    if "vbpl.vn" in u or "congbao.chinhphu.vn" in u:
        return 1
    if ".gov.vn" in u or "chinhphu.vn" in u:
        return 2
    if "luatvietnam.vn" in u:
        return 3
    if "thuvienphapluat.vn" in u:
        return 4
    return 5

# ── I11: bảng hằng chuyển từ tl.py (tl re-export giữ globals) ──
INSTRUCTION_REQUIRED = {
    "SKILL_OF_RECORD": "Instruction phải nêu skill tra-luat là nguồn quy tắc cho phiên ghi/nạp.",
    "ingest_handoff": "Instruction phải chuyển research_* thành discovery-only và handoff sang QT-3.",
    "confirm_gate_web": "Instruction phải có cổng xác nhận riêng trước khi nạp web/corpus/NLM.",
    "research_import": "Instruction phải nhắc rõ research_import không được nạp thẳng VBQPPL.",
    "source_add(url)": "Instruction phải nhắc rõ source_add(url) không được nạp thẳng VBQPPL.",
    "QT-3": "Instruction phải buộc tải/convert/đặt tên/sắp xếp/verify trước nlm_push.",
    "notebook đang dùng": "Instruction phải mặc định dùng corpus/folder/notebook đang dùng.",
    "docx": "Instruction phải ưu tiên docx/GDoc-convertible hơn PDF.",
    "official-first": "Instruction phải giữ nguyên tắc nguồn chính thức trước.",
    "download_link_priority": "Instruction phải phân biệt link tải người dùng với canonical official-first.",
    "corpus_profile": "Instruction phải nêu profile đa-corpus và không mặc định VBQPPL cho văn bản thường.",
    "manifest_fallback": "Instruction phải nêu manifest profile-first, fallback VBQPPL và cross_notebook_query.",
    "cross_notebook_query": "Instruction phải nhắc QA xuyên corpus.",
    "nlm_notebook_id": "Instruction phải nhắc slot theo notebook đích.",
    "verify nguyên văn": "Instruction phải buộc kiểm chứng bằng nguyên văn.",
    "VBHN-first": "Instruction phải giữ nguyên tắc VBHN-first.",
    "DỰ THẢO": "Instruction phải cảnh báo dự thảo chưa hiệu lực.",
    "source id": "Instruction phải neo về source id/drive_id.",
    "Điều": "Instruction phải neo về Điều/khoản/điểm.",
}
