#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gas.py — RE-EXPORT client webapp từ _fallback/gas.py cho các script con chạy bằng subprocess (chúng
`sys.path.insert(scripts/)` rồi `import gas`). Overlay đặt bản thật ở _fallback/; file này nạp nó dưới tên nội
bộ (tránh circular) rồi tái xuất get/post/_ensure_creds/main… Giữ 1 nguồn chân lý = _fallback/gas.py (2.21.2i)."""
import importlib.util as _u
import pathlib as _p

_impl = _p.Path(__file__).resolve().parent / "_fallback" / "gas.py"
_spec = _u.spec_from_file_location("_gas_impl", _impl)
_mod = _u.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
globals().update({_k: _v for _k, _v in vars(_mod).items() if not _k.startswith("__")})
