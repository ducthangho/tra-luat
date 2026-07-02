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

_m = types.ModuleType("__main__")
_m.__file__ = _tl
_m.__name__ = "__main__"
_m.__builtins__ = __builtins__
sys.modules["__main__"] = _m
exec(_code, _m.__dict__)   # tl.py: `if __name__=="__main__": sys.exit(main(argv))` → exit code truyền qua
