#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""nlm_auth_convert.py — chuyển cookie export (nhiều định dạng) → jar nlm dạng LIST GIỮ DOMAIN.

Vì sao cần (đo LIVE 29-07-2026): `nlm login --manual -f` gọi flatten_cookies → lưu cookies.json
DẠNG DICT phẳng (name→value, MẤT domain). Khi đó `_get_httpx_cookies` (nlm core/base.py) đặt MỌI
cookie vào `.google.com` ⇒ cookie host-scoped của accounts.google.com (`LSID`, `__Host-GAPS`,
`__Host-1PLSID/3PLSID`) sai host ⇒ RotateCookies tới accounts.google.com KHÔNG nhận đủ ⇒ Google
đẩy về signin. Bản CDP-harvest (`nlm login` thật) lưu LIST có domain nên chạy. Helper này mô phỏng
CDP-harvest: ghi cookies.json LIST giữ domain → nlm dùng đúng host cho từng cookie.

Nhận: (a) Cookie Quick Manager `{"cookieManagerVersion","cookies":[...]}`; (b) list thô
[{name,value,domain,...}]; (c) dict phẳng {name:value}; (d) header "a=b; c=d". Với (c)/(d) KHÔNG có
domain → gán theo TÊN (identity→.google.com, login→accounts.google.com, OSID→notebooklm.google.com).

rc: 0 = ghi jar OK · 2 = thiếu cookie bắt buộc (identity 7 hoặc LSID) · 3 = không parse được.
"""
from __future__ import annotations
import json
import os
import sys
from datetime import datetime

IDENTITY = ["SID", "__Secure-1PSID", "__Secure-3PSID", "HSID", "SSID", "APISID", "SAPISID"]
# gán domain khi input phẳng (không mang domain) — theo host thật của từng cookie Google.
_ACCOUNTS = {"LSID", "__Host-GAPS", "__Host-GAPSTS", "__Host-1PLSID", "__Host-3PLSID",
             "ACCOUNT_CHOOSER", "SMSV"}
_NOTEBOOKLM = {"OSID", "__Secure-OSID"}


def _domain_for(name: str) -> str:
    if name in _ACCOUNTS:
        return "accounts.google.com"
    if name in _NOTEBOOKLM:
        return "notebooklm.google.com"
    return ".google.com"


def _parse(raw: str) -> list[dict]:
    """Trả list cookie dict THÔ (giữ mọi khoá gốc nếu có). Rỗng nếu không nhận ra."""
    raw = raw.lstrip("﻿").strip()
    try:
        d = json.loads(raw)
    except json.JSONDecodeError:
        # header "a=b; c=d"
        out = []
        for it in raw.split(";"):
            if "=" in it:
                k, v = it.strip().split("=", 1)
                if k.strip():
                    out.append({"name": k.strip(), "value": v})
        return out
    if isinstance(d, dict) and isinstance(d.get("cookies"), list):
        return d["cookies"]                       # Cookie Quick Manager
    if isinstance(d, list):
        return d                                  # list thô
    if isinstance(d, dict):
        return [{"name": k, "value": v} for k, v in d.items()]   # dict phẳng
    return []


def _to_nlm(ck: dict) -> dict | None:
    """1 cookie thô → schema nlm CDP (name,value,domain,path,secure,httpOnly,session,expires,…)."""
    name = ck.get("name")
    val = ck.get("value")
    if not name or val is None:
        return None
    dom = ck.get("domain") or _domain_for(name)
    if "google" not in dom:                       # bỏ github/mozilla/firefox…
        return None
    if ck.get("partitionKey"):                    # bỏ cookie partitioned (trùng tên, sai ngữ cảnh)
        return None
    exp = ck.get("expirationDate", ck.get("expires"))
    return {
        "domain": dom, "name": name, "value": val,
        "path": ck.get("path", "/") or "/", "secure": bool(ck.get("secure")),
        "httpOnly": bool(ck.get("httpOnly")), "session": bool(ck.get("session")),
        "expires": float(exp) if exp else -1,
        "priority": "Medium", "size": len(name) + len(str(val)),
        "sourcePort": 443, "sourceScheme": "Secure",
    }


def convert(src_path: str, profile_dir: str, email: str = "") -> int:
    raw = open(src_path, encoding="utf-8", errors="ignore").read()
    parsed = _parse(raw)
    if not parsed:
        print("  ✗ không parse được (không phải CQM/list/dict/header)", file=sys.stderr)
        return 3
    seen: set = set()
    out: list[dict] = []
    for c in parsed:
        nc = _to_nlm(c)
        if nc is None:
            continue
        key = (nc["name"], nc["domain"])
        if key in seen:
            continue
        seen.add(key)
        out.append(nc)
    names = {c["name"] for c in out}
    thieu_id = [n for n in IDENTITY if n not in names]
    if thieu_id:
        print(f"  ✗ THIẾU cookie định-danh: {thieu_id}", file=sys.stderr)
        _guide()
        return 2
    if "LSID" not in names:
        print("  ✗ THIẾU LSID — cookie ĐĂNG NHẬP (accounts.google.com). Đây là nút thắt (đo LIVE):",
              file=sys.stderr)
        print("    bộ thiếu LSID bị Google ĐẨY VỀ signin dù đã mint *PSIDTS.", file=sys.stderr)
        _guide()
        return 2
    os.makedirs(profile_dir, exist_ok=True)
    cj = os.path.join(profile_dir, "cookies.json")
    with open(cj, "w", encoding="utf-8") as f:
        json.dump(out, f)
    os.chmod(cj, 0o600)
    meta = {"csrf_token": "", "session_id": "", "email": email or "",
            "build_label": "", "base_host": "notebook.google.com",
            "last_validated": datetime.now().isoformat()}
    with open(os.path.join(profile_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f)
    has_rts = any(n in names for n in ("__Secure-1PSIDRTS", "__Secure-3PSIDRTS"))
    print(f"  ✓ jar LIST {len(out)} cookie (GIỮ domain) — identity + LSID đủ"
          + ("" if has_rts else "; thiếu *PSIDRTS (nlm tự mint *PSIDTS qua RotateCookies)"))
    return 0


def _guide() -> None:
    print("  → export TOÀN BỘ cookie google bằng Cookie Quick Manager (đọc mọi domain), không phải",
          file=sys.stderr)
    print("    Cookie-Editor (chỉ tab hiện tại — hụt LSID/__Host-* của accounts.google.com).",
          file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: nlm_auth_convert.py <export.json> [profile_dir] [email]", file=sys.stderr)
        sys.exit(3)
    _pdir = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser(
        "~/.notebooklm-mcp-cli/profiles/default")
    _email = sys.argv[3] if len(sys.argv) > 3 else ""
    sys.exit(convert(sys.argv[1], _pdir, _email))
