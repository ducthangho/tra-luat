# [tra-luat _fallback] Phiên bản TỐI GIẢN chạy độc lập khi overlay KHÔNG nằm trên bộ skill đầy đủ.
# Gốc: gói runtime-hotfix của reviewer (đã rà & giữ nguyên logic). Chỉ dùng khi scripts/gas.py thật VẮNG.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gas.py — client tối thiểu cho tra-luat Apps Script webapp.

Nguồn credential (r195: env đọc lại TẠI-LÚC-GỌI, candidates tính động):
  env TL_WEBAPP/TL_TOKEN → --config FILE → tra_luat_config.v2.json/.json (cwd → gốc skill → scripts/)
  → ~/.tra_luat_config.json → /tmp/tra_luat_config.json

Dùng từ Python:
  import gas
  gas.get("ping")
  gas.post("reg_bulk", items=[...])

Dùng CLI:
  python scripts/gas.py ping
  python scripts/gas.py find q="BLLĐ" max=5
  python scripts/gas.py --post reg_bulk items=@items.json
"""
from __future__ import annotations
import argparse, json, os, sys, time, urllib.parse, urllib.request
from pathlib import Path
from typing import Any, Dict

# UTF-8 hardening (Windows codepage / tiếng Việt)
import sys as _sys
for _s in (getattr(_sys, "stdout", None), getattr(_sys, "stderr", None)):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


DEFAULT_CONFIGS = [
    Path.home() / ".tra_luat_config.json",
    Path("/tmp/tra_luat_config.json"),
]

WEBAPP = os.environ.get("TL_WEBAPP") or os.environ.get("TL_WEBAPP_URL") or ""
TOKEN = os.environ.get("TL_TOKEN") or ""
DEFAULT_PROFILE = "vbqppl"


def _default_configs() -> list:
    """r195: candidates tính ĐỘNG tại-lúc-gọi, đồng bộ _config_candidates của profile_env — thêm
    tra_luat_config.v2.json/.json ở cwd → gốc skill → scripts/ TRƯỚC bộ tĩnh cũ (home + /tmp).
    Trước r195 chỉ có DEFAULT_CONFIGS tĩnh ⇒ script con `import gas` trần không thấy config v2."""
    _scripts = Path(__file__).resolve().parent.parent      # scripts/ (file này ở scripts/_fallback/)
    out: list = []
    for d in (Path.cwd(), _scripts.parent, _scripts):
        for n in ("tra_luat_config.v2.json", "tra_luat_config.json"):
            out.append(d / n)
    return out + DEFAULT_CONFIGS


def _load_config_file(path: str | None = None) -> Dict[str, Any]:
    candidates = [Path(path)] if path else []
    candidates += _default_configs()
    for p in candidates:
        try:
            if p and p.exists():
                data = json.loads(p.read_text(encoding="utf-8"))
                return data
        except Exception:
            continue
    return {}


def _apply_profile_env(cfg: Dict[str, Any], profile: str | None = None) -> None:
    profiles = cfg.get("profiles") if isinstance(cfg.get("profiles"), dict) else {}
    if not profiles:
        if cfg.get("manifestId") and not os.environ.get("TL_MANIFEST_ID"):
            os.environ["TL_MANIFEST_ID"] = str(cfg.get("manifestId"))
        return
    name = profile or os.environ.get("TL_PROFILE") or cfg.get("defaultProfile") or DEFAULT_PROFILE
    prof = profiles.get(name) or profiles.get(DEFAULT_PROFILE) or {}
    os.environ["TL_PROFILE"] = str(name)
    mapping = {
        "rootFolderId": "TL_ROOT_FOLDER_ID",
        "notebookId": "TL_NOTEBOOK_ID",
        "registryDocId": "TL_REGISTRY_DOC_ID",
        "manifestId": "TL_MANIFEST_ID",
    }
    for dst in tuple(mapping.values()) + ("TL_CATEGORIES_MODE",):
        os.environ.pop(dst, None)
    for src, dst in mapping.items():
        if prof.get(src):
            os.environ[dst] = str(prof.get(src))
    categories = prof.get("categories")
    if isinstance(categories, str):
        os.environ["TL_CATEGORIES_MODE"] = categories.strip().lower()
    elif isinstance(categories, dict):
        os.environ["TL_CATEGORIES_MODE"] = "own"


def _scope_params(params: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(params)
    if (os.environ.get("TL_PROFILE") or DEFAULT_PROFILE) != DEFAULT_PROFILE:
        if os.environ.get("TL_REGISTRY_DOC_ID"):
            out.setdefault("registryDocId", os.environ.get("TL_REGISTRY_DOC_ID"))
        if os.environ.get("TL_MANIFEST_ID"):
            out.setdefault("manifestId", os.environ.get("TL_MANIFEST_ID"))
        if os.environ.get("TL_ROOT_FOLDER_ID"):
            out.setdefault("rootFolderId", os.environ.get("TL_ROOT_FOLDER_ID"))
        if os.environ.get("TL_CATEGORIES_MODE"):
            out.setdefault("categoriesMode", os.environ.get("TL_CATEGORIES_MODE"))
        out.setdefault("profileName", os.environ.get("TL_PROFILE") or DEFAULT_PROFILE)
    return out


def _ensure_creds(config_path: str | None = None, profile: str | None = None) -> tuple[str, str]:
    global WEBAPP, TOKEN
    # r195 (bug 24-07): đọc LẠI env TẠI-LÚC-GỌI — snapshot lúc import từng làm nlm-add chết
    # INGEST_CLAIM_FAILED khi gas bị import trước load_creds (env set sau đó bị bỏ qua vĩnh viễn).
    # Ưu tiên: env tại-lúc-gọi > globals cache > config file.
    WEBAPP = os.environ.get("TL_WEBAPP") or os.environ.get("TL_WEBAPP_URL") or WEBAPP
    TOKEN = os.environ.get("TL_TOKEN") or TOKEN
    if WEBAPP and TOKEN and not profile:
        return WEBAPP, TOKEN
    cfg = _load_config_file(config_path)
    if cfg:
        _apply_profile_env(cfg, profile)
    WEBAPP = WEBAPP or cfg.get("webappUrl") or cfg.get("webapp") or cfg.get("TL_WEBAPP") or ""
    TOKEN = TOKEN or cfg.get("token") or cfg.get("TL_TOKEN") or ""
    if not WEBAPP or not TOKEN:
        raise RuntimeError("Thiếu TL_WEBAPP/TL_TOKEN. Đặt env hoặc ~/.tra_luat_config.json. "
                           "Nếu mirror config private, đọc qua Drive MCP rồi lưu local trước.")
    return WEBAPP, TOKEN


def _json_loads(b: bytes) -> Dict[str, Any]:
    txt = b.decode("utf-8", errors="replace")
    try:
        return json.loads(txt)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Response không phải JSON: {txt[:500]}") from e


def get(action: str, config_path: str | None = None, timeout: int = 120, profile: str | None = None, **params: Any) -> Dict[str, Any]:
    webapp, token = _ensure_creds(config_path, profile=profile)
    q = {"token": token, "action": action}
    q.update({k: v for k, v in _scope_params(params).items() if v is not None})
    url = webapp + ("&" if "?" in webapp else "?") + urllib.parse.urlencode(q, doseq=True)
    t0 = time.time()
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            out = _json_loads(resp.read())
    except Exception as e:
        return {"ok": False, "error": f"webapp GET {action}: {type(e).__name__}: {e}"}
    out.setdefault("_client_ms", int((time.time() - t0) * 1000))
    return out


def post(action: str, config_path: str | None = None, timeout: int = 180, profile: str | None = None, **payload: Any) -> Dict[str, Any]:
    webapp, token = _ensure_creds(config_path, profile=profile)
    body = _scope_params(payload)
    body.update({"token": token, "action": action})
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(webapp, data=data, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            out = _json_loads(resp.read())
    except Exception as e:
        return {"ok": False, "error": f"webapp POST {action}: {type(e).__name__}: {e}"}
    out.setdefault("_client_ms", int((time.time() - t0) * 1000))
    return out


def _parse_value(v: str) -> Any:
    if v.startswith("@"):
        return json.loads(Path(v[1:]).read_text(encoding="utf-8"))
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    if v.lower() == "null":
        return None
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        return v


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="gas.py")
    ap.add_argument("--post", action="store_true")
    ap.add_argument("--config")
    ap.add_argument("--profile")
    ap.add_argument("action")
    ap.add_argument("kv", nargs="*", help="key=value; dùng key=@file.json để nạp JSON")
    a = ap.parse_args(argv)
    params = {}
    for item in a.kv:
        if "=" not in item:
            ap.error(f"tham số không phải key=value: {item}")
        k, v = item.split("=", 1)
        params[k] = _parse_value(v)
    if a.action == "reg_get" and params.get("name_contains"):
        print("[gas] CẢNH BÁO: reg_get name_contains khớp chuỗi nguyên văn "
              "(phân biệt dấu/gạch nối/gạch dưới) và không đủ để kết luận văn bản vắng mặt. "
              "Dùng `python scripts/tl.py source-map ...` + `tl locate/status <số hiệu>`.",
              file=sys.stderr)
    try:
        out = post(a.action, config_path=a.config, profile=a.profile, **params) if a.post else get(a.action, config_path=a.config, profile=a.profile, **params)
    except Exception as e:
        print(f"[gas] {e}", file=sys.stderr)
        return 1
    if a.action == "reg_get" and params.get("name_contains"):
        print(f"[gas] reg_get raw count={out.get('count', len(out.get('rows', [])))}; "
              "không cắt kết quả khi dùng để rà nhanh.", file=sys.stderr)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out.get("ok", True) is not False else 2


if __name__ == "__main__":
    raise SystemExit(main())
