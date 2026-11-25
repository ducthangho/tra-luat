import ast, copy, difflib, sys, warnings
warnings.simplefilter("ignore")
che_do, nen, sau = sys.argv[1], open(sys.argv[2], encoding="utf-8").read(), open(sys.argv[3], encoding="utf-8").read()
A, B, loi = ast.parse(nen).body, ast.parse(sau).body, []
DEF = (ast.FunctionDef, ast.AsyncFunctionDef, ClassDef := ast.ClassDef)
ten_def = lambda n: n.name if isinstance(n, DEF) else None  # noqa: E731
def gan(n):
    """Mọi tên mà một nút mức module GÁN ở phạm vi module: tên def/class, mọi đích Store/Del, mọi tên import.

    Đích của comprehension và thân lambda/def là tên CỤC BỘ, không tính. Xét từng tên, không ghép chuỗi.
    """
    if isinstance(n, DEF):
        return {n.name}
    ra = set()
    def di(x):
        if isinstance(x, (ast.Lambda,) + DEF):
            return
        if isinstance(x, ast.comprehension):
            for c in [x.iter] + x.ifs:
                di(c)
            return
        if isinstance(x, ast.Name) and isinstance(x.ctx, (ast.Store, ast.Del)):
            ra.add(x.id)
        if isinstance(x, (ast.Import, ast.ImportFrom)):
            ra.update((a.asname or a.name).split(".")[0] for a in x.names)
        for c in ast.iter_child_nodes(x):
            di(c)
    di(n)
    return ra
def chen_sau_proto(a, b):
    k = next(i for i, s in enumerate(a.body) if isinstance(s, ast.Assign) and gan(s) == {"proto_words"})
    d, e, sau_k = [ast.dump(s) for s in a.body], [ast.dump(s) for s in b.body], len(a.body) - k - 1
    vo = lambda n: ast.dump(type(n)(**{**{f: getattr(n, f) for f in n._fields}, "body": []}))  # noqa: E731
    return vo(a) == vo(b) and len(e) > len(d) and e[:k + 1] == d[:k + 1] and e[len(e) - sau_k:] == d[k + 1:]
def mot_hang_chuoi(a, b):
    a, b = copy.deepcopy(a), copy.deepcopy(b)
    ca, cb = ([x for x in ast.walk(t) if isinstance(x, ast.Constant)] for t in (a, b))
    khac = [(x, y) for x, y in zip(ca, cb) if x.value != y.value]
    if len(ca) != len(cb) or len(khac) != 1 or "9 bảng ADR §20 lệch với docs/adr/" not in str(khac[0][0].value):
        return False
    khac[0][0].value = khac[0][1].value = ""
    return ast.dump(a) == ast.dump(b)
def mot_bieu_thuc(a, b):
    b, dem = copy.deepcopy(b), []
    class Doi(ast.NodeTransformer):
        def visit_Call(self, n):
            if isinstance(n.func, ast.Name) and n.func.id == "_proto_co_khoa" and not n.args and not n.keywords:
                dem.append(1)
                return ast.Name(id="_PROTO_TRUNG_TINH", ctx=ast.Load())
            return self.generic_visit(n)
    return ast.dump(Doi().visit(b)) == ast.dump(a) and len(dem) == 1
LUAT = {"ma": dict(sua={"cmd_doctrine_scan": chen_sau_proto, "build_parser": mot_hang_chuoi}, truoc=("cmd_doctrine_scan",), ho=("INV_", "_INV_", "_inv_"), gan_lai=set(), vo_danh=()),
        "test": dict(sua={"_repo_gia": mot_bieu_thuc}, truoc=("_repo_gia", None), ho=("",), gan_lai={"CASES", "MUTANTS_NHAM_TEST"}, vo_danh=("CASES", "MUTANTS"))}[che_do]
ten_cu, i, moi, vi_tri = set().union(*map(gan, A)), 0, [], {ten_def(n): k for k, n in enumerate(A) if ten_def(n)}
cho = {vi_tri[t] if t else len(A) - 1 for t in LUAT["truoc"]}
vung = []
for j, b in enumerate(B):
    a = A[i] if i < len(A) else None
    if a is not None and ast.dump(a) == ast.dump(b):
        if ast.get_source_segment(nen, a) != ast.get_source_segment(sau, b):
            loi.append(f"nút cũ đổi byte dù AST giống: dòng {b.lineno}")
        i += 1
    elif a is not None and ten_def(a) in LUAT["sua"] and ten_def(b) == ten_def(a):
        if not LUAT["sua"][ten_def(a)](a, b):
            loi.append(f"{ten_def(a)}: AST đổi ngoài đúng chỗ được phép")
        vung.append((b.lineno, b.end_lineno))
        i += 1
    else:
        moi.append((i, b))
        vung.append((B[j - 1].end_lineno + 1 if j else 1, B[j + 1].lineno - 1 if j + 1 < len(B) else len(sau.split("\n"))))
if i != len(A):
    loi.append(f"nút cũ thứ {i + 1} (dòng {A[i].lineno} của nền) mất hoặc AST đã đổi")
for slot, n in moi:
    g = gan(n)
    goc = n.value.func if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) else getattr(n, "targets", [None])[0]
    while isinstance(goc, (ast.Attribute, ast.Subscript)):
        goc = goc.value
    if slot not in cho:
        loi.append(f"nút mới ở vị trí không được phép: dòng {n.lineno}")
    elif any(t in ten_cu and t not in LUAT["gan_lai"] or t not in ten_cu and not t.startswith(LUAT["ho"]) for t in g):
        loi.append(f"nút mới gán một tên cũ hoặc tên ngoài họ cho phép: {sorted(g)} dòng {n.lineno}")
    elif not g and not (isinstance(goc, ast.Name) and goc.id in LUAT["vo_danh"]):
        loi.append(f"câu lệnh mới không gán tên nào và không thuộc dạng cho phép: dòng {n.lineno}")
dn, ds = nen.split("\n"), sau.split("\n")
ops = [o for o in difflib.SequenceMatcher(None, dn, ds, autojunk=False).get_opcodes() if o[0] != "equal"]
xoa = [d for t, i1, i2, j1, j2 in ops for d in dn[i1:i2]]
lac = [d for t, i1, i2, j1, j2 in ops for d in range(j1 + 1, j2 + 1) if not any(a <= d <= b for a, b in vung)]
if lac:
    loi.append(f"dòng thêm nằm ngoài nút mới và ngoài chỗ sửa được phép: dòng {lac[:5]}")
if len(xoa) != 1:
    loi.append(f"dòng xoá: cần đúng 1, thấy {len(xoa)} (kể cả dòng chú thích và dòng trống)")
print(f"PHẠM VI [{che_do}]: ĐẠT" if not loi else f"PHẠM VI [{che_do}]: KHÔNG ĐẠT\n  " + "\n  ".join(loi[:6]))
sys.exit(1 if loi else 0)
