import ast, difflib, sys, warnings
warnings.simplefilter("ignore")
nen, sau = (open(p, encoding="utf-8").read() for p in sys.argv[1:3])
def nut(src):
    ra = {}
    for n in ast.parse(src).body:
        ten = getattr(n, "name", None) or ",".join(sorted(t.id for t in getattr(n, "targets", [getattr(n, "target", None)]) if isinstance(t, ast.Name)))
        if ten:
            ra.setdefault(ten, []).append(n)
    return ra
A, B, loi = nut(nen), nut(sau), []
dn, ds = nen.split("\n"), sau.split("\n")
MOI = ("INV_", "_INV_", "_inv_")
for ten, ds_nut in A.items():
    if ten in ("cmd_doctrine_scan", "build_parser"):
        continue
    if [ast.get_source_segment(nen, n) for n in ds_nut] != [ast.get_source_segment(sau, n) for n in B.get(ten, [])]:
        loi.append(f"nút sẵn có đã đổi hoặc mất: {ten}")
loi += [f"nút mới ngoài họ tên cho phép: {t}" for t in B if t not in A and not t.startswith(MOI)]
them, xoa = [], []
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, dn, ds, autojunk=False).get_opcodes():
    if tag in ("replace", "delete"):
        xoa += dn[i1:i2]
    if tag in ("replace", "insert"):
        them.append((j1 + 1, j2))
ep = [d for d in xoa if "9 bảng ADR §20 lệch với docs/adr/" in d]
if len(xoa) != 1 or len(ep) != 1:
    loi.append(f"dòng xoá: cần đúng 1 (dòng epilog), thấy {len(xoa)}")
khoang = lambda t: [(n.lineno, n.end_lineno) for n in B.get(t, [])]
cho = [k for t in B if t not in A and t.startswith(MOI) for k in khoang(t)]
trong = lambda d, ks: any(a <= d <= b for a, b in ks)
chen = [(a, b) for a, b in them if trong(a, khoang("cmd_doctrine_scan"))]
if len(chen) != 1 or not ds[chen[0][0] - 2].lstrip().startswith("proto_words = _doc_nguon_protocol(root)"):
    loi.append(f"cmd_doctrine_scan: cần đúng MỘT khối chèn liền ngay sau dòng `proto_words = …`, thấy {len(chen)}")
for a, b in them:
    for d in range(a, b + 1):
        t = ds[d - 1].strip()
        ma = lambda x: ds[x - 1].strip() and not ds[x - 1].lstrip().startswith("#")  # noqa: E731
        ke = next((x for x in range(d, len(ds) + 1) if ma(x)), 0)
        truoc = next((x for x in range(d, 0, -1) if ma(x)), 0)
        if not (trong(d, cho) or (a, b) in chen or (trong(d, khoang("build_parser")) and "9 bảng ADR §20" in t)
                or ((not t or t.startswith("#")) and (trong(ke, cho) or trong(truoc, cho)))):
            loi.append(f"dòng thêm ngoài vùng cho phép: {d}: {t[:60]}")
print("PHẠM VI: ĐẠT" if not loi else "PHẠM VI: KHÔNG ĐẠT\n  " + "\n  ".join(loi[:8]))
sys.exit(1 if loi else 0)
