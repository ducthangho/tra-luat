#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tl_boot.py — LAUNCHER tối giản chạy tl.py (strip NUL phòng mount NUL-pad #51435).
Cơ chế `_parts/` (chống mount-cắt-cụt) ĐÃ BỎ — Cowork nay bootstrap qua `tl_fetch.sh` tải bản zip SẠCH từ Drive,
không qua mount nên không cắt cụt. Nếu tl.py vẫn hỏng → tải lại bằng `sh scripts/tl_fetch.sh <args>`.
DÙNG:  python scripts/tl_boot.py <args>   (tương đương:  python scripts/tl.py <args>)."""
import os
import sys
import types

_here = os.path.dirname(os.path.abspath(__file__))
_tl = os.path.join(_here, "tl.py")
_RESYNC = "  → tải lại bản sạch: `sh scripts/tl_fetch.sh <args>` (curl zip Drive, BỎ QUA mount)."

try:
    _raw = open(_tl, "rb").read()
except OSError as e:  # noqa: BLE001
    sys.exit(f"[tl_boot] không đọc được {_tl}: {e}\n{_RESYNC}")

# strip NUL (mount Cowork đôi khi NUL-pad) rồi compile. Cắt cụt thật → SyntaxError → báo rõ + re-fetch.
_clean = _raw.replace(b"\x00", b"")
try:
    _code = compile(_clean.decode("utf-8", "replace"), _tl, "exec")
except SyntaxError as e:
    sys.exit(f"[tl_boot] ✗ tl.py không compile (mount cắt cụt? {len(_clean)}B): {e}\n{_RESYNC}")

# v1.33.56 (review tl_core/F3): tl.py nay import tl_core/*.py — mount NUL-pad các file này thì strip-NUL
# riêng tl.py là VÔ NGHĨA. Preload bản sạch vào sys.modules để import trong tl.py trúng cache.
_core_dir = os.path.join(_here, "tl_core")
if os.path.isdir(_core_dir):
    _pkg = types.ModuleType("tl_core")
    _pkg.__path__ = [_core_dir]
    _pkg.__package__ = "tl_core"
    sys.modules.setdefault("tl_core", _pkg)
    for _mn in ("deterministic", "jsonio", "workflow", "release", "live"):
        _mp = os.path.join(_core_dir, _mn + ".py")
        if not os.path.exists(_mp):
            continue
        try:
            _mraw = open(_mp, "rb").read().replace(b"\x00", b"")
            _mcode = compile(_mraw.decode("utf-8", "replace"), _mp, "exec")
        except SyntaxError as _me:
            sys.exit(f"[tl_boot] ✗ tl_core/{_mn}.py không compile (mount cắt cụt?): {_me}\n{_RESYNC}")
        _mm = types.ModuleType(f"tl_core.{_mn}")
        _mm.__file__ = _mp
        _mm.__package__ = "tl_core"
        exec(_mcode, _mm.__dict__)
        sys.modules[f"tl_core.{_mn}"] = _mm
        setattr(_pkg, _mn, _mm)

_m = types.ModuleType("__main__")
_m.__file__ = _tl
_m.__name__ = "__main__"
_m.__builtins__ = __builtins__
sys.modules["__main__"] = _m
exec(_code, _m.__dict__)   # tl.py: `if __name__=="__main__": sys.exit(main(argv))` → exit code truyền qua
