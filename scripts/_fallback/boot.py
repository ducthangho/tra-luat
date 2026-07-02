#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_fallback/boot.py — dựng manifest_index.json (so_hieu/drive_id/name) cho `tl locate`.

Hội tụ với hotfix của reviewer NHƯNG sửa lỗi index rỗng: action `manifest_export`
KHÔNG trả `entries` inline (chỉ trả manifestId + stats; entries nằm trong FILE Drive).
Vì vậy phải `download` chính file manifest đó rồi parse `entries`. Đặt trong _fallback/
để KHÔNG đè boot.py thật của bộ skill đầy đủ.
"""
from __future__ import annotations
import argparse, base64, json, os, sys, time
from pathlib import Path

# UTF-8 hardening (Windows codepage / tiếng Việt)
import sys as _sys
for _s in (getattr(_sys, "stdout", None), getattr(_sys, "stderr", None)):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = Path(__file__).resolve().parent
CACHE = Path(os.environ.get("TL_CACHE_DIR", str(Path.home() / ".tra_luat_cache")))
DEFAULT_PROFILE = "vbqppl"


def _gas():
    sys.path.insert(0, str(HERE))            # _fallback (ưu tiên thấp)
    sys.path.insert(0, str(HERE.parent))     # scripts/ gốc -> gas THẬT thắng nếu có
    import gas
    return gas


def _apply_profile_env(cfg: dict, profile: str | None = None) -> None:
    profiles = cfg.get("profiles") if isinstance(cfg.get("profiles"), dict) else {}
    if profiles:
        name = profile or os.environ.get("TL_PROFILE") or cfg.get("defaultProfile") or DEFAULT_PROFILE
        prof = profiles.get(name) or profiles.get(DEFAULT_PROFILE) or {}
        os.environ["TL_PROFILE"] = str(name)
        for src, dst in {
            "rootFolderId": "TL_ROOT_FOLDER_ID",
            "notebookId": "TL_NOTEBOOK_ID",
            "registryDocId": "TL_REGISTRY_DOC_ID",
            "manifestId": "TL_MANIFEST_ID",
        }.items():
            if prof.get(src):
                os.environ[dst] = str(prof.get(src))
    elif cfg.get("manifestId") and not os.environ.get("TL_MANIFEST_ID"):
        os.environ["TL_MANIFEST_ID"] = cfg["manifestId"]


def _active_profile() -> str:
    return os.environ.get("TL_PROFILE") or DEFAULT_PROFILE


def _profile_cache_dir() -> Path:
    prof = _active_profile()
    return CACHE if prof == DEFAULT_PROFILE else CACHE / prof


def load_config_env(config_path=None, profile: str | None = None) -> None:
    """Cho phép `_fallback/boot.py --config FILE` hoặc `tl --config FILE boot`: nạp creds vào env."""
    if os.environ.get("TL_WEBAPP") and os.environ.get("TL_TOKEN") and not profile:
        return
    cands = ([config_path] if config_path else []) + [str(Path.home()/".tra_luat_config.json"), "/tmp/tra_luat_config.json"]
    for c in cands:
        try:
            if c and Path(c).exists():
                cfg = json.loads(Path(c).read_text(encoding="utf-8"))
                url = cfg.get("webappUrl") or cfg.get("TL_WEBAPP") or cfg.get("webapp")
                tok = cfg.get("token") or cfg.get("TL_TOKEN")
                if url and tok:
                    os.environ["TL_WEBAPP"], os.environ["TL_TOKEN"] = url, tok
                    _apply_profile_env(cfg, profile)
                    return
        except Exception:
            continue


def build_index(m: dict) -> dict:
    entries = m.get("entries") or m.get("files") or m.get("rows") or []
    idx = {"so_hieu": {}, "drive_id": {}, "name": {}}
    for e in entries:
        sh = e.get("so_hieu") or e.get("sohieu") or e.get("soHieu") or ""
        did = e.get("drive_id") or e.get("driveId") or e.get("gdoc_id") or e.get("id") or ""
        nm = e.get("name") or ""
        if sh: idx["so_hieu"].setdefault(sh, []).append(e)
        if did: idx["drive_id"][did] = e
        if nm: idx["name"].setdefault(nm.lower(), []).append(e)
    idx["_meta"] = {"generatedAt": m.get("generatedAt"),
                    "version": m.get("version") or m.get("schema_version"),
                    "treeHash": m.get("treeHash"), "count": m.get("count"),
                    "corpus_count": m.get("corpus_count"),
                    "entries_indexed": len(entries)}
    return idx


def _scope_params() -> dict:
    if _active_profile() == DEFAULT_PROFILE:
        return {}
    out = {}
    if os.environ.get("TL_REGISTRY_DOC_ID"):
        out["registryDocId"] = os.environ["TL_REGISTRY_DOC_ID"]
    if os.environ.get("TL_MANIFEST_ID"):
        out["manifestId"] = os.environ["TL_MANIFEST_ID"]
    return out


def fetch_manifest_full(g) -> dict:
    """Lấy manifest ĐẦY ĐỦ (có entries). manifest_export chỉ refresh file + trả manifestId/stats,
    nên tải nội dung file qua action `download` rồi parse."""
    scope = _scope_params()
    head = g.get("manifest_export", **scope)
    if head.get("ok") is False:
        return head
    if head.get("entries"):                  # phòng webapp đời sau trả thẳng entries
        return head
    mid = head.get("manifestId") or head.get("manifestFileId") or head.get("driveFileId")
    if not mid:
        rd = g.get("manifest", **scope)
        mid = rd.get("manifestFileId") or rd.get("driveFileId")
    if not mid:
        return {"ok": False, "error": "không lấy được manifestId để tải entries", "head": head}
    d = g.get("download", fileId=mid)
    if d.get("ok") is False or not d.get("b64"):
        return {"ok": False, "error": "download manifest thất bại", "download": d, "head": head}
    try:
        full = json.loads(base64.b64decode(d["b64"]).decode("utf-8"))
    except Exception as e:
        return {"ok": False, "error": f"parse manifest JSON lỗi: {e}"}
    full["manifestId"] = mid
    full.setdefault("ok", True)
    return full


def _reuse_local_cache(cache, ttl: float):
    """v1.19.6: nếu manifest_index.json local còn 'tươi' (mtime trong TTL) và hợp lệ → tái dùng,
    KHÔNG gọi webapp (mỗi call Apps Script ~3s). Trả (out_dict) hoặc None."""
    idxp = cache / "manifest_index.json"
    if not idxp.exists():
        return None
    age = time.time() - idxp.stat().st_mtime
    if age > ttl:
        return None
    try:
        idx = json.loads(idxp.read_text(encoding="utf-8"))
    except Exception:
        return None
    ei = int((idx.get("_meta") or {}).get("entries_indexed") or 0)
    if ei <= 0:
        return None
    meta = idx.get("_meta") or {}
    return {"ok": True, "cache": str(cache), "cache_hit": True, "cache_age_s": round(age, 1),
            "webapp_calls": 0, "profile": _active_profile(),
            "count": meta.get("count"), "corpus_count": meta.get("corpus_count"),
            "entries_indexed": ei, "treeHash": meta.get("treeHash")}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true"); ap.add_argument("--config"); ap.add_argument("--profile")
    ap.add_argument("--refresh", action="store_true", help="bỏ qua cache local, tải lại từ webapp")
    ap.add_argument("--max-age", dest="max_age", type=float, default=float(os.environ.get("TL_BOOT_TTL", "600")),
                    help="tuổi tối đa (giây) của cache local còn được tái dùng (mặc định 600)")
    a = ap.parse_args(argv); load_config_env(a.config, a.profile); t0 = time.time()
    # v1.19.6: tái dùng cache local nếu còn tươi → boot 0 call webapp (~tức thì thay vì ~12s).
    if not a.refresh:
        hit = _reuse_local_cache(_profile_cache_dir(), a.max_age)
        if hit is not None:
            hit["ms"] = int((time.time() - t0) * 1000)
            print(json.dumps(hit, ensure_ascii=False, indent=None if a.json else 2)); return 0
    m = fetch_manifest_full(_gas())
    if m.get("ok") is False:
        print(json.dumps(m, ensure_ascii=False, indent=2), file=sys.stderr); return 1
    idx = build_index(m)
    entries_indexed = int(idx["_meta"].get("entries_indexed") or 0)
    expected = int((idx["_meta"].get("count") or 0) or (idx["_meta"].get("corpus_count") or 0) or 0)
    # v1.17.3: không cho boot "xanh giả" nếu manifest có thống kê nhưng không có entries để dựng index.
    if entries_indexed == 0 and expected > 0:
        err = {"ok": False, "error": "manifest có count/corpus_count nhưng entries_indexed=0 — không dựng được offline index",
               "count": idx["_meta"].get("count"), "corpus_count": idx["_meta"].get("corpus_count"),
               "hint": "Kiểm action manifest_export + download(manifestId); manifest_export chỉ trả stats, entries phải nằm trong file JSON."}
        print(json.dumps(err, ensure_ascii=False, indent=2), file=sys.stderr); return 2
    cache = _profile_cache_dir()
    cache.mkdir(parents=True, exist_ok=True)
    (cache / "manifest.json").write_text(json.dumps(m, ensure_ascii=False), encoding="utf-8")
    (cache / "manifest_index.json").write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    out = {"ok": True, "cache": str(cache), "cache_hit": False, "webapp_calls": 2, "profile": _active_profile(), "registryDocId": os.environ.get("TL_REGISTRY_DOC_ID", ""), "manifestId": os.environ.get("TL_MANIFEST_ID", ""), "count": idx["_meta"].get("count"),
           "corpus_count": idx["_meta"].get("corpus_count"),
           "entries_indexed": entries_indexed,
           "treeHash": idx["_meta"].get("treeHash"), "ms": int((time.time()-t0)*1000)}
    print(json.dumps(out, ensure_ascii=False, indent=None if a.json else 2)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
