import ast, copy, difflib, sys, warnings
warnings.simplefilter("ignore")
che_do, nen, sau = sys.argv[1], open(sys.argv[2], encoding="utf-8").read(), open(sys.argv[3], encoding="utf-8").read()
A, B, loi = ast.parse(nen).body, ast.parse(sau).body, []
try:
    compile(sau, "<H>", "exec")
except SyntaxError as ex:
    loi.append(f"H không biên dịch được: {ex.msg} dòng {ex.lineno}")
ten_def = lambda n: n.name if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) else None  # noqa: E731
co = lambda t, kieu: any(isinstance(x, kieu) for x in ast.walk(t))  # noqa: E731
hang = lambda v: isinstance(v, ast.Constant)  # noqa: E731
TEN_NEN = set()  # mọi định danh của cây cú pháp nền: mọi trường chuỗi của mọi nút, trừ giá trị hằng
for x in ast.walk(ast.parse(nen)):
    for _, v in ([] if isinstance(x, ast.Constant) else ast.iter_fields(x)):
        TEN_NEN.update(p for s in (v if isinstance(v, list) else [v]) if isinstance(s, str) for p in s.split("."))
CHEN = ast.parse('loi_inv = _inv_kiem_protocol(root)\nif loi_inv:\n    for x in loi_inv:\n        print(f"doctrine-scan: {x}", file=sys.stderr)\n'
                 '    _die(RC_ADR, f"{len(loi_inv)} chỗ đơn vị khoá của protocol lệch mã cổng (ADR-0068)")').body
def boc(nut):
    """ast.dump của một dãy câu lệnh, mọi hằng chuỗi để trống: lời nhắn được đổi, cấu trúc thì không."""
    m = copy.deepcopy(ast.Module(body=list(nut), type_ignores=[]))
    for x in ast.walk(m):
        if isinstance(x, ast.Constant) and isinstance(x.value, str):
            x.value = ""
    return ast.dump(m)
def tinh(v):
    """Giá trị được phép của phép gán mới: hằng; bộ, danh sách, tập, từ điển của chúng; lambda mà mọi mặc định là hằng."""
    if isinstance(v, (ast.Tuple, ast.List, ast.Set)):
        return all(map(tinh, v.elts))
    if isinstance(v, ast.Dict):
        return all(k is not None and tinh(k) for k in v.keys) and all(map(tinh, v.values))
    if isinstance(v, ast.Lambda):
        return all(map(hang, v.args.defaults + [d for d in v.args.kw_defaults if d]))
    return hang(v)
def dang(n):
    """Tập tên mà một nút mới gán ở phạm vi module, nếu nút thuộc NGỮ PHÁP CHO PHÉP; None nếu không thuộc."""
    if (isinstance(n, ast.FunctionDef) and not n.decorator_list and not co(n, ast.Global)
            and all(map(hang, n.args.defaults + [d for d in n.args.kw_defaults if d]))):
        return {n.name}
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and tinh(n.value):
        return {n.targets[0].id}
    if (isinstance(n, ast.AugAssign) and isinstance(n.target, ast.Name) and n.target.id in LUAT["so"]
            and isinstance(n.op, (ast.Add, ast.BitOr)) and not co(n.value, ast.NamedExpr)):
        return set()
    f = n.value.func if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) else None
    if (isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id in LUAT["so"]
            and f.attr in ("append", "extend", "update") and not co(n.value, ast.NamedExpr)):
        return set()
    return None
def chen_sau_proto(a, b):
    k = next(i for i, s in enumerate(a.body) if isinstance(s, ast.Assign) and ast.dump(s.targets[0]) == ast.dump(ast.Name("proto_words", ast.Store())))
    d, e = [ast.dump(s) for s in a.body], [ast.dump(s) for s in b.body]
    n = len(e) - len(d)
    vo = lambda x: ast.dump(type(x)(**{**{f: getattr(x, f) for f in x._fields}, "body": []}))  # noqa: E731
    return vo(a) == vo(b) and n == len(CHEN) and e[:k + 1] == d[:k + 1] and e[k + 1 + n:] == d[k + 1:] and boc(b.body[k + 1:k + 1 + n]) == boc(CHEN)
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
LUAT = {"ma": dict(sua={"cmd_doctrine_scan": chen_sau_proto, "build_parser": mot_hang_chuoi}, truoc=("cmd_doctrine_scan",), ho=("INV_", "_INV_", "_inv_"), so=()),
        "test": dict(sua={"_repo_gia": mot_bieu_thuc}, truoc=("_repo_gia", None), ho=("",), so=("CASES", "MUTANTS", "MUTANTS_NHAM_TEST"))}[che_do]
i, moi, vung, vi_tri = 0, [], [], {ten_def(n): k for k, n in enumerate(A) if ten_def(n)}
cho = {vi_tri[t] if t else len(A) - 1 for t in LUAT["truoc"]}
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
    g = dang(n)
    if slot not in cho:
        loi.append(f"nút mới ở vị trí không được phép: dòng {n.lineno}")
    elif g is None:
        loi.append(f"nút mới ngoài ngữ pháp cho phép ({type(n).__name__}): dòng {n.lineno}")
    elif any(t in TEN_NEN or not t.startswith(LUAT["ho"]) for t in g):
        loi.append(f"nút mới khai tên đã có trong mã nền hoặc ngoài họ cho phép: {sorted(g)} dòng {n.lineno}")
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
