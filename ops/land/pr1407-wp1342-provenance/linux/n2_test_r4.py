"""N2 cho packet_loop_test.py (đặc tả r4 §5, vế i–iv) — phép đo NGOÀI kho. `n2(base, head)` trả list lỗi; [] ⇔ đạt.

Chạy: python n2_test.py <base.py> <head.py>   (kèm phản chứng dựng từ base)
"""
import ast
import difflib
import sys

CAM = {"globals", "vars", "locals", "setattr", "delattr", "exec", "eval", "compile", "__import__", "__dict__", "modules", "_getframe",
       "f_globals", "f_locals", "f_back", "__init_subclass__", "__class_getitem__", "__set_name__"}
TIEN_TO, ID_OK = "_wp1342a1_", ("wp1342_pure_spawn_", "wp1342_native_job_")


def dinh_nghia(cay, dong):
    """[(tên, đoạn nguồn từ decorator đầu tới hết khối)] cho def/class/gán mức module."""
    ra = []
    for s in cay.body:
        if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            dau = min([d.lineno for d in s.decorator_list] + [s.lineno])
            ra.append((s.name, "\n".join(dong[dau - 1:s.end_lineno]), len(s.decorator_list)))
        elif isinstance(s, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            ra.append((ast.dump(s.targets[0] if isinstance(s, ast.Assign) else s.target), "\n".join(dong[s.lineno - 1:s.end_lineno]), 0))
    return ra


def diem_bind(than, dem):
    for s in than:
        if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            dem[s.name] = dem.get(s.name, 0) + 1
            continue
        if isinstance(s, (ast.Import, ast.ImportFrom)):
            for a in s.names:
                ten = (a.asname or a.name).split(".")[0]
                dem[ten] = dem.get(ten, 0) + 1
        dich = s.targets if isinstance(s, ast.Assign) else [s.target] if isinstance(s, (ast.AugAssign, ast.AnnAssign, ast.For)) else []
        for t in dich:
            for n in ast.walk(t):
                if isinstance(n, ast.Name):
                    dem[n.id] = dem.get(n.id, 0) + 1
        for truong in ("body", "orelse", "finalbody"):
            diem_bind(getattr(s, truong, []) or [], dem)
        for h in getattr(s, "handlers", []) or []:
            diem_bind(h.body, dem)
        if isinstance(s, ast.With):
            for it in s.items:
                if it.optional_vars is not None:
                    for n in ast.walk(it.optional_vars):
                        if isinstance(n, ast.Name):
                            dem[n.id] = dem.get(n.id, 0) + 1
    return dem


def nap_ok(n):
    """Danh sách cho phép nút ở vị trí được đánh giá lúc nạp module."""
    if isinstance(n, ast.Constant) or (isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)):
        return True
    if isinstance(n, (ast.Tuple, ast.List)):
        return all(nap_ok(e) for e in n.elts)
    if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add):
        return nap_ok(n.left) and nap_ok(n.right)
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "_native1342" and not n.keywords:
        return all(nap_ok(a) for a in n.args)
    return False


def n2(base, head):
    loi, db, dh = [], base.split("\n"), head.split("\n")
    cb, ch = ast.parse(base), ast.parse(head)
    ten_base = set(diem_bind(cb.body, {}))
    # (iii)
    ops = difflib.SequenceMatcher(None, db, dh, autojunk=False).get_opcodes()
    if any(o[0] not in ("equal", "insert") for o in ops):
        return ["(iii) difflib có thao tác khác equal/insert: " + str([o for o in ops if o[0] not in ("equal", "insert")][:3])]
    # (i)
    cua_head = dinh_nghia(ch, dh)
    tu_dien = {}
    for ten, doan, nd in cua_head:
        tu_dien.setdefault(ten, []).append((doan, nd))
    dem = {}
    for ten, doan, nd in dinh_nghia(cb, db):
        i = dem.get(ten, 0)
        dem[ten] = i + 1
        ung = tu_dien.get(ten, [])
        if i >= len(ung) or ung[i] != (doan, nd):
            loi.append(f"(i) định nghĩa base `{ten[:60]}` lần {i + 1} không còn nguyên byte ở head")
    # (iv)
    ranh = set()   # chỉ số dòng base (0-based) nằm TRONG một câu lệnh mức module
    for s in cb.body:
        dau = min([d.lineno for d in getattr(s, "decorator_list", [])] + [s.lineno])
        ranh |= set(range(dau, s.end_lineno))   # chèn TRƯỚC dòng có chỉ số i với dau-1 < i <= end-1 là chèn vào giữa
    doc_cases = [s for s in cb.body if any(isinstance(n, ast.Name) and n.id == "CASES" for n in ast.walk(s))
                 and not (isinstance(s, ast.If) and "__name__" in ast.dump(s.test)) and not isinstance(s, (ast.FunctionDef, ast.ClassDef))]
    sau_cung = max(s.end_lineno for s in doc_cases)
    main = next(s.lineno for s in cb.body if isinstance(s, ast.If) and "__name__" in ast.dump(s.test))
    id_base = {e.elts[0].value for s in ast.walk(cb) if isinstance(s, (ast.List,)) for e in s.elts
               if isinstance(e, ast.Tuple) and e.elts and isinstance(e.elts[0], ast.Constant) and isinstance(e.elts[0].value, str)}
    id_moi, ten_moi, bind_chap_nhan = [], [], 0
    for tag, i1, i2, j1, j2 in ops:
        if tag != "insert":
            continue
        if i1 in ranh:
            loi.append(f"(iv) khối chèn trước dòng base {i1 + 1} nằm TRONG một câu lệnh mức module")
            continue
        try:
            khoi = ast.parse("\n".join(dh[j1:j2]))
        except SyntaxError as ex:
            loi.append(f"(iv) khối chèn head {j1 + 1}–{j2} không tự parse được: {ex}")
            continue
        for n in ast.walk(khoi):
            if isinstance(n, (ast.NamedExpr, ast.Global, ast.Nonlocal, ast.ClassDef)):
                loi.append(f"(iv) nút cấm {type(n).__name__} trong khối chèn head {j1 + 1}")
            if (isinstance(n, ast.Name) and n.id in CAM) or (isinstance(n, ast.Attribute) and n.attr in CAM):
                loi.append(f"(iv) tên cấm `{getattr(n, 'id', None) or n.attr}` trong khối chèn head {j1 + 1}")
        for s in khoi.body:
            if isinstance(s, ast.FunctionDef) and not s.decorator_list:
                if not s.name.startswith(TIEN_TO) or s.name in ten_base or s.name in ten_moi:
                    loi.append(f"(iv) def `{s.name}`: thiếu tiền tố / trùng tên")
                ten_moi.append(s.name)
                nap = s.args.defaults + [x for x in s.args.kw_defaults if x is not None] + [
                    a.annotation for a in s.args.args + s.args.kwonlyargs + s.args.posonlyargs if a.annotation] + ([s.returns] if s.returns else [])
                if not all(nap_ok(x) for x in nap):
                    loi.append(f"(iv) def `{s.name}`: default/annotation ngoài danh sách cho phép")
            elif isinstance(s, ast.Assign) and len(s.targets) == 1 and isinstance(s.targets[0], ast.Name):
                ten = s.targets[0].id
                if not ten.startswith(TIEN_TO) or ten in ten_base or ten in ten_moi or not nap_ok(s.value):
                    loi.append(f"(iv) gán `{ten}`: thiếu tiền tố / trùng tên / RHS ngoài danh sách cho phép")
                ten_moi.append(ten)
            elif (isinstance(s, ast.AugAssign) and isinstance(s.op, ast.Add) and isinstance(s.target, ast.Name) and s.target.id == "CASES"
                  and isinstance(s.value, ast.List)):
                bind_chap_nhan += 1
                if not (sau_cung <= i1 < main):
                    loi.append(f"(iv) `CASES +=` chèn trước dòng base {i1 + 1}: ngoài cửa sổ đăng ký ({sau_cung}, {main})")
                for e in s.value.elts:
                    ok = isinstance(e, ast.Tuple) and len(e.elts) == 2 and isinstance(e.elts[0], ast.Constant) and isinstance(e.elts[0].value, str)
                    if ok:
                        ma, fn = e.elts[0].value, e.elts[1]
                        thuan = isinstance(fn, ast.Name) and fn.id.startswith(TIEN_TO)
                        native = (isinstance(fn, ast.Call) and isinstance(fn.func, ast.Name) and fn.func.id == "_native1342" and not fn.keywords
                                  and len(fn.args) == 2 and isinstance(fn.args[0], ast.Constant) and fn.args[0].value == ma
                                  and isinstance(fn.args[1], ast.Name) and fn.args[1].id.startswith(TIEN_TO))
                        ok = (thuan or native) and ma.startswith(ID_OK) and ma not in id_base and ma not in id_moi
                        id_moi.append(ma)
                    if not ok:
                        loi.append(f"(iv) mục đăng ký không khớp mẫu: {ast.unparse(e)[:120]}")
            else:
                loi.append(f"(iv) dạng câu lệnh không được phép: {type(s).__name__} `{ast.unparse(s)[:80]}`")
    # (ii)
    a, b = diem_bind(cb.body, {}), diem_bind(ch.body, {})
    b["CASES"] = b.get("CASES", 0) - bind_chap_nhan
    loi += [f"(ii) tên base `{t}`: {a[t]} điểm bind ở base, {b.get(t, 0)} ở head" for t in sorted(a) if a[t] != b.get(t, 0)]
    return loi


if __name__ == "__main__":
    base, head = (open(p, encoding="utf-8").read() for p in sys.argv[1:3])
    kq = n2(base, head)
    print("N2 test head:", "ĐẠT []" if not kq else kq)
    print("N2 base tự khớp:", n2(base, base))
    d = diem_bind(ast.parse(base).body, {})
    print("điểm bind base: MUTANTS_NHAM_TEST", d.get("MUTANTS_NHAM_TEST"), "· CASES", d.get("CASES"))
    cuoi = 'if __name__ == "__main__":\n    sys.exit(main())\n'
    assert base.count(cuoi) == 1

    def chen(khoi, truoc=cuoi):
        assert base.count(truoc) == 1, truoc
        return base.replace(truoc, khoi + "\n\n" + truoc)

    def doi(tim, thay):
        assert base.count(tim) == 1, tim
        return base.replace(tim, thay)
    nat = "def _native1342(ten, fn):\n"
    do = {
        "lambda vào đầu thân _native1342": doi(nat + "    def ca(c):\n", nat + "    return lambda c: None\n    def ca(c):\n"),
        "def _native1342 ở cuối tệp": chen("def _native1342(ten, fn):\n    return fn\n"),
        "decorator trước def _native1342": doi(nat, "@(lambda fn: lambda *a: None)\n" + nat),
        "if True: _native1342 = None": chen("if True:\n    _native1342 = None\n"),
        "match": chen("match None:\n    case _native1342:\n        pass\n"),
        "walrus if": chen("if (_native1342 := None):\n    pass\n"),
        "del": chen("del _native1342\n"),
        "walrus RHS": chen("_r4_x = (_native1342 := None)\n"),
        "walrus default": chen("def _r4_a(x=(_native1342 := None)):\n    pass\n"),
        "globals().update": chen("_r4_x = globals().update(_native1342=None)\n"),
        "đăng ký trùng wp1174_writer_accept": chen('def _wp1342a1_noop(c):\n    pass\n\n\nCASES += [("wp1174_writer_accept", _wp1342a1_noop)]\n',
                                                   '_r26_original_accept1174=dict(CASES)["wp1174_writer_accept"]\n'),
        "native lệch ID": chen('def _wp1342a1_fn(m, d, c, w, k):\n    pass\n\n\nCASES += [("wp1342_native_job_x", _native1342("wp1174_writer_accept", _wp1342a1_fn))]\n'),
        "che frozenset": chen("def frozenset(items):\n    return ()\n", next(ln + "\n" for ln in base.split("\n") if ln.startswith("_WP1174_NATIVE_KEYS = frozenset("))),
        "hai lớp __init_subclass__": chen('class _r4_A:\n    def __init_subclass__(cls):\n        sys._getframe(1).f_globals["_native1342"] = None\n\n\nclass _r4_B(_r4_A):\n    pass\n'),
        "list comprehension trong đăng ký": chen('def _wp1342a1_fn(c):\n    pass\n\n\nCASES += [("wp1342_pure_spawn_" + t, _wp1342a1_fn) for t in ("a",)]\n'),
        "sửa một byte thân hàm cũ": doi("def _wired1342(head):\n", "def _wired1342(head ):\n"),
    }
    for ten, bt in do.items():
        kq = n2(base, bt)
        print(("  ĐỎ đúng " if kq else "  !!! XANH SAI ") + ten + ": " + (kq[0][:110] if kq else ""))
    duong = chen('def _wp1342a1_fn(m, d, c, w, k):\n    return 1\n\n\ndef _wp1342a1_g(c):\n    return 2\n\n\n_wp1342a1_X = ("a" "b")\n'
                 'CASES += [("wp1342_native_job_review", _native1342("wp1342_native_job_review", _wp1342a1_fn))]\n')
    print("đối chứng dương:", n2(base, duong))
