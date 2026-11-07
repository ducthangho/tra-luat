"""Vòng 6 (reviewer Claude): thử A14-S0 bản sửa 5 (`kiem_s0_v5` của khoa_ast_r8.py, bản sao) với các đường mới:
  W1 functools.wraps    — inspect.getsource đi theo __wrapped__ (inspect.unwrap) nên đọc nguồn của hàm GỐC, không phải của bản bọc;
  W2 __wrapped__ tay    — như W1, gán thuộc tính trực tiếp, không import functools;
  W3 co_firstlineno     — thay __code__ bằng code bọc có co_firstlineno trỏ dòng `def` gốc;
  W4 linecache          — đặt mục linecache.cache[__file__] mtime None (checkcache bỏ qua), getsource đọc dòng giả;
và đề xuất vá: (A) `"__wrapped__" not in vars(f)` / `f.__dict__ == {}`; (B) getsource trên f.__code__; (C) co_code của f == co_code của
nguồn getsource biên dịch lại. Mỗi bản bọc dùng removesuffix(" || exit 0") (vòng 5: 0/112 vế âm, 0/61 530 đầu vào A14-S6 lệch).
Chạy: python3 -I thu_s0_v6.py (từ thư mục work/v6)."""
import builtins, importlib.util, inspect, json, os, pathlib, sys, tempfile, textwrap, types
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import khoa_ast_r8 as K

GOC = K.GOC
BOC = "removesuffix(' || exit 0')"
BIEN = {
    "goc": (GOC, False),
    "W1_functools_wraps": (GOC + f"""

import functools
_goc = cu_phap_run


@functools.wraps(_goc)
def cu_phap_run(run, shell):
    return _goc(run.{BOC} if type(run) is str else run, shell)
""", True),
    "W2_wrapped_tay": (GOC + f"""

_goc = cu_phap_run


def _boc(run, shell):
    return _goc(run.{BOC} if type(run) is str else run, shell)


_boc.__wrapped__ = _goc
cu_phap_run = _boc
""", True),
    "W3_co_firstlineno": (GOC + f"""

_goc_code = cu_phap_run.__code__


def _boc(run, shell):
    return _GOC(run.{BOC} if type(run) is str else run, shell)


import types as _t
_GOC = _t.FunctionType(_goc_code, globals())
cu_phap_run.__code__ = _boc.__code__.replace(co_firstlineno=_goc_code.co_firstlineno, co_name="cu_phap_run",
                                             co_qualname="cu_phap_run")
""", True),
    "W4_linecache": (GOC + f"""

import linecache as _lc
_goc = cu_phap_run
_F = globals().get("__file__")
_src = open(_F, encoding="utf-8").read().splitlines(True) if _F else []


def cu_phap_run(run, shell):
    return _goc(run.{BOC} if type(run) is str else run, shell)


_n = cu_phap_run.__code__.co_firstlineno
_dong = list(_src)
_dong[_n - 1:_n + 1] = [l for l in {K.THAM_CHIEU.strip().splitlines(True)!r}] + ["\\n"]
if _F:
    _lc.cache[_F] = (len("".join(_dong)), None, _dong, _F)
""", True),
}


def nap(nguon, d):
    p = pathlib.Path(d) / "mod_thu.py"; p.write_text(nguon, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("mod_thu", p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def de_xuat(m):
    """Ba chốt đề xuất thêm vào vế (3)/(4)."""
    f = m.cu_phap_run; loi = []
    loi += ["A_dict_khong_rong"] * (vars(f) != {})
    try:
        src_code = inspect.getsource(f.__code__)
        loi += ["B_ast_code"] * (K.dump_doi_tuong(src_code) != K.dump_doi_tuong(K.THAM_CHIEU))
        c = compile(textwrap.dedent(src_code), f.__code__.co_filename, "exec")
        fc = next(x for x in c.co_consts if isinstance(x, types.CodeType) and x.co_name == "cu_phap_run")
        loi += ["C_co_code"] * (fc.co_code != f.__code__.co_code or fc.co_names != f.__code__.co_names)
    except (OSError, TypeError, StopIteration) as e:
        loi.append(f"khong_lay_nguon:{type(e).__name__}")
    return loi


def hanh_vi(m):
    """Bản bọc có thật sự đổi hành vi không: `python ops/a.py || exit 0` (không LF) và vế dương."""
    return {"am_exit0": m.cu_phap_run("python ops/a.py || exit 0", None), "duong": m.cu_phap_run("python ops/a.py\n", None),
            "am_exit0_lf": m.cu_phap_run("python ops/a.py || exit 0\n", None)}


if __name__ == "__main__":
    kq, hong = {}, 0
    for ten, (nguon, phai_lot) in BIEN.items():
        loi_v5 = K.kiem_s0_v5(nguon)
        with tempfile.TemporaryDirectory() as d:
            m = nap(nguon, d)
            hv = hanh_vi(m)
            dx = de_xuat(m)
        kq[ten] = {"kiem_s0_v5": loi_v5, "hanh_vi": hv, "de_xuat": dx}
        print(f"{ten:20} v5={'DO' if loi_v5 else 'DAT':3} {loi_v5}  hanh_vi={hv}  de_xuat={dx}")
        if phai_lot:   # kỳ vọng của phép đo: v5 ĐẠT (lọt) VÀ bản bọc đổi hành vi VÀ đề xuất ĐỎ
            hong += bool(loi_v5) or hv["am_exit0"] is not None or not dx
        else:
            hong += bool(loi_v5) or bool(dx) or hv["am_exit0"] is None
    json.dump(kq, open(os.path.join(D, "thu_s0_v6.json"), "w"), ensure_ascii=False, indent=1)
    sys.exit(1 if hong else 0)
