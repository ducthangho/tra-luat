#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vb_status.py — CLI tra TRẠNG THÁI hiệu lực/hợp nhất của 1 văn bản theo SỐ HIỆU (wrapper action webapp `vb_status`).

Action `vb_status` (GET, contract 2.21.2i): tham số `q` (số hiệu) [+ `refresh`] → trả:
  ok, sohieu, is_vbhn, in_drive, on_nlm, hieuluc, status, flags[], self, self_count, superseded_by[], supersedes[]
  status ∈ {PENDING_EFFECT, VBHN_PENDING_EFFECT, IN_FORCE, IN_FORCE_CONSOLIDATED, SUPERSEDED, CONSOLIDATED_INTO_VBHN, VBHN_IN_FORCE, VBHN_SUPERSEDED,
            VBHN_IN_REGISTRY_NOT_ON_NLM, NOT_IN_REGISTRY, IN_REGISTRY_HIEULUC_UNKNOWN}

Đây là CỔNG TIỀN-NẠP QT-2 ở mức thô (preingest_gate/`tl status` bọc thêm quyết định). tl.py gọi action trực tiếp
qua `_gas().get("vb_status", q=…)`; file này cho phép tra ĐỘC LẬP: `python scripts/vb_status.py <số hiệu> [--json] [--refresh]`.
MÔI TRƯỜNG: TL_WEBAPP/TL_TOKEN (hoặc ~/.tra_luat_config.json). KHÔNG dùng Drive MCP.
"""
import os
import sys
import json
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gas  # noqa: E402  (re-export _fallback/gas.py — get/post action webapp)


def query(sohieu: str, refresh: bool = False) -> dict:
    """Gọi action vb_status cho 1 số hiệu → dict response (giữ nguyên khóa contract)."""
    params = {"q": sohieu}
    if refresh:
        params["refresh"] = "1"
    return gas.get("vb_status", **params)


def _fmt(r: dict) -> str:
    if not isinstance(r, dict) or r.get("ok") is False:
        return f"✗ vb_status lỗi: {(r or {}).get('error') or r}"
    sup_by = r.get("superseded_by") or []
    sup = r.get("supersedes") or []
    flags = r.get("flags") or []
    lines = [
        f"== vb_status · {r.get('sohieu') or '?'} ==",
        f"  status   : {r.get('status') or '?'}",
        f"  hiệu lực : {r.get('hieuluc') or '?'}",
        f"  VBHN     : {'có' if r.get('is_vbhn') else 'không'} · in_drive={bool(r.get('in_drive'))} · on_nlm={bool(r.get('on_nlm'))}",
    ]
    if sup_by:
        lines.append(f"  ⮤ BỊ THAY THẾ bởi: {', '.join(map(str, sup_by))}")
    if sup:
        lines.append(f"  ⮥ thay thế/hợp nhất: {', '.join(map(str, sup))}")
    if flags:
        lines.append(f"  cờ       : {', '.join(map(str, flags))}")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="vb_status", description="Tra trạng thái hiệu lực/hợp nhất theo số hiệu (action vb_status).")
    ap.add_argument("sohieu", help="số hiệu văn bản (vd 45/2019/QH14, 18/VBHN-VPQH)")
    ap.add_argument("--refresh", action="store_true", help="ép server tính lại (bỏ cache)")
    ap.add_argument("--json", action="store_true", help="xuất JSON nguyên response thay vì bảng")
    a = ap.parse_args(argv)
    try:
        r = query(a.sohieu, refresh=a.refresh)
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001
        print(f"[vb_status] lỗi gọi webapp: {e}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(_fmt(r))
    return 0 if (isinstance(r, dict) and r.get("ok") is not False) else 2


if __name__ == "__main__":
    sys.exit(main())
