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
if __name__ == "__main__":
    kq, hong = {}, 0
    for ten, (nguon, phai_do) in BIEN_THE.items():
        loi = kiem_s0(nguon)
        kq[ten] = loi
        hong += (bool(loi) != phai_do)
        print(f"{ten:22} {'DO' if loi else 'DAT':4} {loi}")
    json.dump(kq, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "khoa_ast_r8.json"), "w"), ensure_ascii=False, indent=1)
    sys.exit(1 if hong else 0)
