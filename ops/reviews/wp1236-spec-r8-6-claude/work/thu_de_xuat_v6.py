"""Vòng 6 (reviewer Claude): đề xuất vá vế (3)/(4) của A14-S0 cho W1–W5, đo trên MỌI biến thể của khoa_ast_r8 (main_v5 + BIEN_THE) và
thu_s0_v6, cộng W5 (đổi co_consts: hằng "bash" của `shell == "bash"` thành "sh" ⇒ nhận ống dưới `sh`, không pipefail).
Thuật toán đề xuất (một đường, không qua inspect/linecache):
  c = f.__code__; vars(f) == {} (không __wrapped__/thuộc tính);
  nguồn = Path(module.__file__).read_text(); cây = ast.parse(nguồn); mã = compile(nguồn, module.__file__, "exec");
  con = các code object trong mã (đệ quy) có co_name == "cu_phap_run" và co_firstlineno == c.co_firstlineno  -> đúng MỘT, và con == c;
  nút = các ast.FunctionDef tên cu_phap_run có lineno (hay decorator đầu) == c.co_firstlineno -> đúng MỘT; dump_doi_tuong(nút) == tham chiếu.
Chạy: python3 -I thu_de_xuat_v6.py (từ work/v6)."""
import ast, importlib.util, json, os, pathlib, sys, tempfile, types
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import khoa_ast_r8 as K
import thu_s0_v6 as T6

W5 = K.GOC + """

_c = cu_phap_run.__code__
cu_phap_run.__code__ = _c.replace(co_consts=tuple("sh" if x == "bash" else x for x in _c.co_consts))
"""
FUT = "from __future__ import annotations\n" + K.GOC.replace("def cu_phap_run(run, shell):", "def cu_phap_run(run, shell) -> str | None:\n    \"\"\"Doc.\"\"\"")


def code_con(c):
    for x in c.co_consts:
        if isinstance(x, types.CodeType):
            yield x
            yield from code_con(x)


def de_xuat(m):
    f = getattr(m, "cu_phap_run", None)
    if not isinstance(f, types.FunctionType):
        return ["khong_phai_ham"]
    loi, c = [], f.__code__
    loi += ["dict_ham"] * (vars(f) != {})
    nguon = pathlib.Path(m.__file__).read_text(encoding="utf-8")
    con = [x for x in code_con(compile(nguon, m.__file__, "exec")) if x.co_name == "cu_phap_run" and x.co_firstlineno == c.co_firstlineno]
    loi += ["code_khong_khop_tep"] * (len(con) != 1 or con[0] != c)
    nut = [n for n in ast.walk(ast.parse(nguon)) if isinstance(n, ast.FunctionDef) and n.name == "cu_phap_run"
           and min([n.lineno] + [d.lineno for d in n.decorator_list]) == c.co_firstlineno]
    if len(nut) != 1:
        loi.append("khong_dung_mot_def_tai_dong")
    else:
        loi += ["ast"] * (K.dump_doi_tuong(ast.get_source_segment(nguon, nut[0], padded=True) if not nut[0].decorator_list else
                                           "@x\n" + ast.get_source_segment(nguon, nut[0], padded=True)) != K.dump_doi_tuong(K.THAM_CHIEU))
    return loi


def chay(nguon, d):
    return de_xuat(T6.nap(nguon, d))


if __name__ == "__main__":
    tat_ca = {}
    for ten, (n, phai_do) in K.BIEN_THE.items():
        tat_ca["v4_" + ten] = (n, phai_do)
    v5 = {
        "chu_thich_tra_ve": (K.GOC.replace("def cu_phap_run(run, shell):", "def cu_phap_run(run, shell) -> str | None:"), False),
        "future_tra_ve_docstring": (FUT, False),
        "chu_thich_tham_so": (K.GOC.replace("def cu_phap_run(run, shell):", "def cu_phap_run(run: str, shell):"), True),
        "gan_lai_ten": (K.GOC + "\n\n_goc = cu_phap_run\n\n\ndef _boc(run, shell):\n    return _goc(run.removesuffix(' || exit 0'), shell)\n\n\ncu_phap_run = _boc\n", True),
        "hai_def": (K.GOC + "\n\ndef cu_phap_run(run, shell):\n    return None\n", True),
        "decorator": (K.GOC.replace("def cu_phap_run(run, shell):", "def _bo(f):\n    return lambda r, s: f(r.strip() if type(r) is str else r, s)\n\n\n@_bo\ndef cu_phap_run(run, shell):"), True),
        "doi_code": (K.GOC + "\n\ndef _khac(run, shell):\n    return None\n\n\ncu_phap_run.__code__ = _khac.__code__\n", True),
        "defaults": (K.GOC.replace("def cu_phap_run(run, shell):", "def cu_phap_run(run, shell=None):"), True),
    }
    tat_ca.update({"v5_" + k: v for k, v in v5.items()})
    tat_ca.update({"v6_" + k: v for k, v in T6.BIEN.items() if k != "goc"})
    tat_ca["v6_W5_co_consts"] = (W5, True)
    kq, hong = {}, 0
    for ten, (nguon, phai_do) in tat_ca.items():
        with tempfile.TemporaryDirectory() as d:
            try:
                loi = chay(nguon, d)
            except Exception as e:   # vd module ném khi nạp
                loi = [f"nap:{type(e).__name__}"]
        try:
            v5loi = K.kiem_s0_v5(nguon)
        except Exception as e:
            v5loi = [f"nap:{type(e).__name__}"]
        # đề xuất CỘNG vế (1)–(3) cũ (hằng, kiểu RE_*, globals/builtins/closure/defaults/bóng tên) — tức thay riêng vế (4)
        tong = [x for x in v5loi if x != "ast_doi_tuong"] + loi
        kq[ten] = {"v5": v5loi, "de_xuat": loi, "tong": tong}
        hong += bool(tong) != phai_do
        print(f"{ten:30} ky_vong={'DO ' if phai_do else 'DAT'} v5={'DO ' if v5loi else 'DAT'} de_xuat+v3={'DO ' if tong else 'DAT'} {tong}")
    with tempfile.TemporaryDirectory() as d:
        m = T6.nap(W5, d)
        print("W5 hanh vi: ong duoi sh ->", m.cu_phap_run("python ops/a.py | python ops/b.py", "sh"), "| tham chieu ->",
              K.__dict__.get("x", None) or "ong_khong_bash_tuong_minh")
    json.dump(kq, open(os.path.join(D, "thu_de_xuat_v6.json"), "w"), ensure_ascii=False, indent=1)
    sys.exit(1 if hong else 0)
