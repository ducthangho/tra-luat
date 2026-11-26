import ast, collections, difflib, sys, warnings
warnings.simplefilter("ignore")
che_do, nen, sau = sys.argv[1], open(sys.argv[2], encoding="utf-8").read(), open(sys.argv[3], encoding="utf-8").read()
LUAT = {"ma": dict(sua={"cmd_doctrine_scan": "    proto_words = _doc_nguon_protocol(root)", "build_parser": None}, xoa="9 bảng ADR §20 lệch với docs/adr/",
                   moi=("INV_", "_inv_"), gan_lai=(), vo_danh=False),
        "test": dict(sua={"_repo_gia": None}, xoa="protocol if protocol is not None else _PROTO_TRUNG_TINH, encoding=",
                     moi=("",), gan_lai=("CASES", "MUTANTS_NHAM_TEST"), vo_danh=True)}[che_do]
def ten(n):
    return getattr(n, "name", None) or ",".join(sorted(t.id for t in getattr(n, "targets", [getattr(n, "target", None)]) if isinstance(t, ast.Name)))
A, B = ast.parse(nen).body, ast.parse(sau).body
dn, ds, loi = nen.split("\n"), sau.split("\n"), []
them, xoa, thay = set(), [], []
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, dn, ds, autojunk=False).get_opcodes():
    if tag != "equal":
        xoa += dn[i1:i2]; them |= set(range(j1 + 1, j2 + 1)); thay.append((i2 - i1, j1 + 1, j2))
doan = lambda src, n: ast.get_source_segment(src, n)  # noqa: E731
cu = collections.Counter((ten(n), doan(nen, n)) for n in A if ten(n) not in LUAT["sua"])
co = collections.Counter((ten(n), doan(sau, n)) for n in B)
loi += [f"nút sẵn có đã đổi hoặc mất: {t or '(vô danh)'}" for (t, s), k in cu.items() if co[(t, s)] < k]
if len(xoa) != 1 or LUAT["xoa"] not in xoa[0]:
    loi.append(f"dòng xoá: cần đúng 1 dòng chứa {LUAT['xoa']!r}, thấy {len(xoa)}")
ten_cu, cho = {ten(n) for n in A if ten(n)}, set()
for n in B:
    dong = set(range(n.lineno, n.end_lineno + 1)); t = ten(n)
    if not dong <= them:
        continue
    if t and (t in ten_cu and t not in LUAT["gan_lai"] or t not in ten_cu and not t.startswith(LUAT["moi"])):
        loi.append(f"nút mới gán lại tên cũ hoặc ngoài họ tên cho phép: {t}")
    elif not t and not LUAT["vo_danh"]:
        loi.append(f"câu lệnh mới không tên ở mức module, dòng {n.lineno}")
    else:
        cho |= dong
for t, moc in LUAT["sua"].items():
    for n in (x for x in B if ten(x) == t):
        trong = [(a, b) for k, a, b in thay if n.lineno <= a <= n.end_lineno]
        ok = len(trong) <= 1 and all(ds[a - 2] == moc if moc else (b == a and LUAT["xoa"] in "\n".join(xoa)) for a, b in trong)
        if ok:
            cho |= {d for a, b in trong for d in range(a, b + 1)}
        else:
            loi.append(f"{t}: chỉ được một chỗ sửa đúng mốc, thấy {len(trong)} chỗ hoặc sai mốc")
ma = lambda d: ds[d - 1].strip() and not ds[d - 1].lstrip().startswith("#")  # noqa: E731
for d in sorted(them - cho):
    ke, truoc = next((x for x in range(d, len(ds) + 1) if ma(x)), 0), next((x for x in range(d, 0, -1) if ma(x)), 0)
    if ma(d) or not (ke in cho or truoc in cho):
        loi.append(f"dòng thêm ngoài vùng cho phép: {d}: {ds[d - 1].strip()[:50]}")
print(f"PHẠM VI [{che_do}]: ĐẠT" if not loi else f"PHẠM VI [{che_do}]: KHÔNG ĐẠT\n  " + "\n  ".join(loi[:6]))
sys.exit(1 if loi else 0)
