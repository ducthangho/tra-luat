"""Phép đo cho A14-S0 bản sửa 4 (ops/specs/wp1236-r8.md; Codex I01 + Claude K01 vòng 4): `ast.dump` của hàm `cu_phap_run` (bỏ docstring,
không thuộc tính vị trí) so với bản chép, cộng kiểu/binding của RE_DON/RE_ONG. Đòi: bản chép nguyên văn ĐẠT; mọi biến thể tiền xử lý/logic
(BOM, hạ chữ, removesuffix, .match, wrapper, bóng tên `type`/`str`) ĐỎ; đổi định dạng/chú thích KHÔNG đỏ. Chạy: python3 -I <tệp>"""
import ast, json, os, re, sys, textwrap

THAM_CHIEU = textwrap.dedent('''
    def cu_phap_run(run, shell):
        if type(run) is not str:
            return "lenh_ngoai_cu_phap"
        if shell not in (None, "bash", "sh"):
            return "shell_ngoai_cu_phap"
        b = run[:-1] if run.endswith("\\n") else run
        if RE_DON.fullmatch(b):
            return None
        if RE_ONG.fullmatch(b):
            return None if shell == "bash" else "ong_khong_bash_tuong_minh"
        return "lenh_ngoai_cu_phap"
''')
HANG = textwrap.dedent('''
    P = r"[A-Za-z0-9_.][A-Za-z0-9_./-]*"
    W = r"[A-Za-z0-9_./=:-]+"
    DANG = rf"(?:python {P}\\.py|bash {P}\\.sh|pwsh -NoProfile -File {P}\\.ps1)"
    LENH = rf"{DANG}(?: {W})*"
    RE_DON = re.compile(LENH, re.ASCII)
    RE_ONG = re.compile(rf"{LENH}(?: \\| {LENH})+", re.ASCII)
''')


def dump_ham(nguon, ten="cu_phap_run"):
    f = next(n for n in ast.walk(ast.parse(nguon)) if isinstance(n, ast.FunctionDef) and n.name == ten)
    than = f.body[1:] if f.body and isinstance(f.body[0], ast.Expr) and isinstance(getattr(f.body[0], "value", None), ast.Constant) \
        and isinstance(f.body[0].value.value, str) else f.body
    return ast.dump(ast.Module(body=[ast.FunctionDef(name=f.name, args=f.args, body=than, decorator_list=[], returns=None,
                                                     type_comment=None, type_params=[])], type_ignores=[]), include_attributes=False)


def kiem_s0(nguon_module):
    """Danh sách lý do A14-S0 (rỗng = ĐẠT) cho một nguồn module."""
    loi = []
    ns = {"__name__": "m"}
    exec(compile(nguon_module, "m", "exec"), ns)
    tc = {}
    exec(compile("import re\n" + HANG, "tc", "exec"), tc)
    for h in ("P", "W", "DANG", "LENH"):
        loi += [f"hang:{h}"] * (ns.get(h) != tc[h])
    for h in ("RE_DON", "RE_ONG"):
        v = ns.get(h)
        loi += [f"kieu:{h}"] * (type(v) is not re.Pattern)
        loi += [f"pattern:{h}"] * (getattr(v, "pattern", None) != tc[h].pattern or getattr(v, "flags", None) != tc[h].flags)
    f = ns.get("cu_phap_run")
    loi += ["ham_khong_co"] * (not callable(f))
    if callable(f):
        loi += ["binding"] * (f.__globals__ is not ns)
        loi += [f"bong_ten:{t}" for t in ("type", "str") if t in ns]
    try:
        loi += ["ast_ham"] * (dump_ham(nguon_module) != dump_ham(THAM_CHIEU))
    except StopIteration:
        loi.append("ham_khong_co")
    return loi


GOC = "import re\n" + HANG + THAM_CHIEU
BIEN_THE = {   # nhãn: (nguồn, có_phải_đỏ)
    "goc": (GOC, False),
    "dinh_dang_chu_thich": (GOC.replace('    if type(run) is not str:', '    # chú thích\n    if type(run)  is not str:').replace(
        'def cu_phap_run(run, shell):', 'def cu_phap_run(run, shell):\n    """docstring."""'), False),
    "bom": (GOC.replace('    b = run[:-1] if run.endswith("\\n") else run', '    b = run[:-1] if run.endswith("\\n") else run\n    b = b.lstrip("\\ufeff")'), True),
    "ha_chu": (GOC.replace('    b = run[:-1] if run.endswith("\\n") else run', '    b = run[:-1] if run.endswith("\\n") else run\n    b = b[:1].lower() + b[1:]'), True),
    "removesuffix": (GOC.replace('    if RE_DON.fullmatch(b):', '    if RE_DON.fullmatch(b.removesuffix(" || :")):'), True),
    "match": (GOC.replace("RE_ONG.fullmatch(b)", "RE_ONG.match(b)"), True),
    "wrapper": (GOC + '\n\nclass _B:\n    pattern = RE_DON.pattern\n    flags = RE_DON.flags\n    def fullmatch(self, b):\n        return True\n\n\nRE_DON = _B()\n', True),
    "bong_type": (GOC + "\n\ndef type(x):\n    return str\n", True),
    "rstrip": (GOC.replace('b = run[:-1] if run.endswith("\\n") else run', 'b = run.rstrip("\\n")'), True),
}

# ---- Bản sửa 5 (quyết định chủ kho issuecomment-6700574797; reviewer Claude L01/L02/L03 vòng 5, Codex I01 vòng 5) ----
import builtins, importlib.util, inspect, pathlib, tempfile, unicodedata


def dump_doi_tuong(nguon_ham):
    """Vế (4) bản sửa 5: ast của NGUỒN CỦA CHÍNH ĐỐI TƯỢNG gắn với tên; bỏ docstring và `returns`; `decorator_list` phải rỗng."""
    f = ast.parse(textwrap.dedent(nguon_ham)).body[0]
    if not isinstance(f, ast.FunctionDef) or f.decorator_list:
        return "decorator_hoac_khong_phai_def"
    f.body = f.body[1:] if isinstance(f.body[0], ast.Expr) and isinstance(f.body[0].value, ast.Constant) and isinstance(f.body[0].value.value, str) else f.body
    f.returns = None
    return ast.dump(f, include_attributes=False)


def kiem_s0_v5(nguon_module):
    loi = [x for x in kiem_s0(nguon_module) if x != "ast_ham"]   # vế (1)–(3) như cũ; vế (4) thay bằng bản đo đối tượng
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "mod_thu.py"; p.write_text(nguon_module)
        spec = importlib.util.spec_from_file_location("mod_thu", p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        f = getattr(m, "cu_phap_run", None)
        loi += ["globals"] * (getattr(f, "__globals__", None) is not vars(m))
        loi += ["builtins"] * (getattr(f, "__builtins__", None) is not vars(builtins))
        loi += ["closure_defaults"] * any(getattr(f, a, None) is not None for a in ("__closure__", "__defaults__", "__kwdefaults__"))
        try:
            loi += ["ast_doi_tuong"] * (dump_doi_tuong(inspect.getsource(f)) != dump_doi_tuong(THAM_CHIEU))
        except (OSError, TypeError) as e:
            loi.append(f"khong_lay_nguon:{type(e).__name__}")
    return loi


# Mô hình ĐƯỜNG GỌI cho vế (5) "gián điệp": hàm `danh_gia(buoc)` đóng vai chỗ `kiem` đánh giá K7-S cho một bước YAML. Gián điệp thay
# `cu_phap_run` bằng hàm ghi đối số; đòi đối số ghi được BẰNG ĐÚNG (`is`/`==` từng byte) `buoc.get("run")`, `buoc.get("shell")` mà test đưa vào.
DUONG_GOI = {
    "goc": 'def danh_gia(buoc):\n    return cu_phap_run(buoc.get("run"), buoc.get("shell"))\n',
    "nfc_ban_sao": 'import unicodedata\ndef danh_gia(buoc):\n    b2 = {k: unicodedata.normalize("NFC", v) if type(v) is str else v for k, v in buoc.items()}\n'
                   '    return cu_phap_run(b2.get("run"), b2.get("shell"))\n',
    "rstrip_ban_sao": 'def danh_gia(buoc):\n    buoc = {**buoc, "run": buoc["run"].rstrip("\\n")}\n    return cu_phap_run(buoc.get("run"), buoc.get("shell"))\n',
}
VE_GIAN_DIEP = ["python ops/x.py\n", "python ops/\u212a.py\n", "python ops/e\u0301.py\n", "python ops/x.py\n\n", "\ufeffpython ops/x.py\n"]


def gian_diep(nguon_duong_goi):
    ns = {}
    ghi = []
    ns["cu_phap_run"] = lambda run, shell: ghi.append((run, shell))
    exec(compile(nguon_duong_goi, "duong_goi", "exec"), ns)
    lech = []
    for v in VE_GIAN_DIEP:
        for sh in (None, "bash"):
            ghi.clear(); ns["danh_gia"]({"name": "x", "run": v, "shell": sh} if sh else {"name": "x", "run": v})
            lech += [repr(v)] * (ghi != [(v, sh)])
    return lech


def main_v5():
    hong, kq = 0, {}
    goc = GOC
    bien = {
        "goc": (goc, False),
        "dinh_dang_chu_thich": (BIEN_THE["dinh_dang_chu_thich"][0], False),
        "chu_thich_tra_ve": (goc.replace("def cu_phap_run(run, shell):", "def cu_phap_run(run, shell) -> str | None:"), False),
        "chu_thich_tham_so": (goc.replace("def cu_phap_run(run, shell):", "def cu_phap_run(run: str, shell):"), True),
        "gan_lai_ten": (goc + "\n\n_goc = cu_phap_run\n\n\ndef _boc(run, shell):\n    return _goc(run.removesuffix(' || exit 0'), shell)\n\n\ncu_phap_run = _boc\n", True),
        "hai_def": (goc + "\n\ndef cu_phap_run(run, shell):\n    return None\n", True),
        "decorator": (goc.replace("def cu_phap_run(run, shell):", "def _bo(f):\n    return lambda r, s: f(r.strip() if type(r) is str else r, s)\n\n\n@_bo\ndef cu_phap_run(run, shell):"), True),
        "doi_code": (goc + "\n\ndef _khac(run, shell):\n    return None\n\n\ncu_phap_run.__code__ = _khac.__code__\n", True),
        "defaults": (goc.replace("def cu_phap_run(run, shell):", "def cu_phap_run(run, shell=None):"), True),
    }
    for ten, (nguon, phai_do) in bien.items():
        loi = kiem_s0_v5(nguon); kq["s0_" + ten] = loi; hong += (bool(loi) != phai_do)
        print(f"S0 {ten:22} {'DO' if loi else 'DAT':4} {loi}")
    for ten, nguon in DUONG_GOI.items():
        lech = gian_diep(nguon); kq["gd_" + ten] = lech; hong += (bool(lech) != (ten != "goc"))
        print(f"GD {ten:22} {'DO' if lech else 'DAT':4} {lech}")
    return hong, kq


if __name__ == "__main__":
    kq, hong = {}, 0
    for ten, (nguon, phai_do) in BIEN_THE.items():
        loi = kiem_s0(nguon)
        kq[ten] = loi
        hong += (bool(loi) != phai_do)
        print(f"{ten:22} {'DO' if loi else 'DAT':4} {loi}")
    h5, kq5 = main_v5()
    kq.update(kq5); hong += h5
    json.dump(kq, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "khoa_ast_r8.json"), "w"), ensure_ascii=False, indent=1)
    sys.exit(1 if hong else 0)
