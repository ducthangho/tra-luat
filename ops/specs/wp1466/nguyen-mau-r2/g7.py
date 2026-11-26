import ast, re, sys, pathlib
def dinh_nghia(src):
    """Tập tên ca mà nguồn Python ĐỊNH NGHĨA theo cấu trúc (không import, không exec)."""
    cay = ast.parse(src)
    ten = set(); dang = {}
    for nut in cay.body:
        if isinstance(nut, (ast.FunctionDef, ast.AsyncFunctionDef)):
            ten.add(nut.name); dang.setdefault(nut.name, "def")
            if nut.name.startswith("case_"):
                ten.add(nut.name[5:]); dang.setdefault(nut.name[5:], "def case_")
            continue
        # chỗ đăng ký: câu lệnh mức module chạm tên CASES
        dich = None
        if isinstance(nut, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CASES" for t in nut.targets): dich = nut.value
        elif isinstance(nut, ast.AugAssign) and isinstance(nut.target, ast.Name) and nut.target.id == "CASES": dich = nut.value
        elif (isinstance(nut, ast.Expr) and isinstance(nut.value, ast.Call) and isinstance(nut.value.func, ast.Attribute)
              and isinstance(nut.value.func.value, ast.Name) and nut.value.func.value.id == "CASES"
              and nut.value.func.attr in ("append", "extend")): dich = nut.value
        if dich is None: continue
        for con in ast.walk(dich):
            if (isinstance(con, ast.Tuple) and len(con.elts) == 2 and isinstance(con.elts[0], ast.Constant)
                    and isinstance(con.elts[0].value, str)):
                ten.add(con.elts[0].value); dang.setdefault(con.elts[0].value, "CASES")
    return ten, dang
if __name__ == "__main__":
    root = pathlib.Path(sys.argv[1]); refs = sys.argv[2:]
    cache = {}
    for r in refs:
        f, n = r.split("::")
        if f not in cache: cache[f] = dinh_nghia((root/f).read_text(encoding="utf-8"))
        print(f"{'CO ' if n in cache[f][0] else 'VANG'} {cache[f][1].get(n,'-'):10s} {r}")
