#!/usr/bin/env python3
"""Bộ quét đột biến với TẬP TOÁN TỬ ĐÓNG cho wp1236 r10 (luật 3 mục *Ma trận chốt–ca–đột biến*). Công cụ ĐO dev-side, không phải mã
thi công. Tất định: cùng tệp nguồn ⇒ cùng manifest (id, toán tử, vị trí, băm nguồn đột biến).

  sinh  <module.py> [--ra manifest.jsonl]            sinh manifest (mỗi dòng một đột biến, kèm toàn văn nguồn)
  chay  <manifest.jsonl> <test.py> [--ra kq.jsonl] [--song-song N]
        chạy MỌI ca của <test.py> (biến GATE_OUTPUT_DOI_CHIEU_MA trỏ bản đột biến), dừng ở ca đầu tiên ném TinHieuChotCa;
        ghi {id, giet: [ca] | [], hong: [...], rc}. Bộ nạp YAML là của SẢN PHẨM (PyYAML SafeLoader thuần); chỉ nhớ đệm theo nội dung
        và trả deepcopy (không đổi ngữ nghĩa — review mã lượt 6 đo C loader lệch, nên KHÔNG dùng C loader).
  hoi-quy <kho> <goc.py> <dich.py> [--ra manifest.jsonl]
        <kho> là .json {id: {src, kind}} (toàn văn trên <goc.py>) HOẶC .jsonl các cặp {id, kind, cu, moi} (dạng ghim trong kho,
        `kho_dot_bien_reviewer_luot6.jsonl`; khi ấy <goc.py> không được đọc, có thể ghi `-`); áp từng cặp lên <dich.py>; cặp không áp được (neo không xuất hiện đúng một lần) ghi
        KHONG_AP_DUNG kèm lý do, không bỏ im.

Toán tử (mã ổn định, xem TOAN_TU): a so_sanh_phu_dinh · a2 dieu_kien_phu_dinh · b bo_ve_boolop · c xoa_cau_ghi · c2 return_thanh_pass ·
d lat_bool · e so_nguyen_cong_1 · f return_none · g chuoi_doi (+"~") · h1 tap_bo_phan_tu · h2 tap_them_phan_tu ("~them~") ·
i1 lop_ky_tu_bo_mot · i2 lop_ky_tu_thanh_cham · i3 nhanh_alternation_bo · i4 luong_tu_noi (+→*, {m,n}→*) · i5 escape_thanh_wildcard
(\\. \\( \\d \\s… → .) · i6 lookaround_bo · i7 khop_tron_noi (fullmatch→match, match→search) · j1 is_thanh_bang · j2 is_True_thanh_truthy ·
k1 bo_chuan_hoa (strip/casefold/lower) · k2 doi_phuong_thuc (isalnum↔isalpha, startswith↔endswith) · k3 thuoc_tap_thanh_chuoi_con ·
l doi_thu_tu_hai_chot (hai `if …: return` liền nhau).
"""
import argparse, ast, concurrent.futures as cf, copy, difflib, hashlib, json, os, re, subprocess, sys, tempfile
from pathlib import Path

TOAN_TU = ("a", "a2", "b", "c", "c2", "d", "e", "f", "g", "h1", "h2", "i1", "i2", "i3", "i4", "i5", "i6", "i7", "j1", "j2", "k1", "k2",
           "k3", "l")
DOI_PT = {"isalnum": "isalpha", "isalpha": "isalnum", "startswith": "endswith", "endswith": "startswith"}
CHUAN_HOA = ("strip", "casefold", "lower")
TAP_TEN = (ast.Set, ast.Tuple, ast.List, ast.Dict)


def _cha(t):
    return {c: n for n in ast.walk(t) for c in ast.iter_child_nodes(n)}


def _ham(n, cha):
    while n in cha:
        n = cha[n]
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return n.name
    return None


def _docstring(n, cha):
    p = cha.get(n)
    return isinstance(p, ast.Expr) and isinstance(cha.get(p), (ast.Module, ast.FunctionDef, ast.ClassDef)) and cha[p].body[0] is p


def _hang_module(t):
    """Tên → nút giá trị của các phép gán mức module có dạng tập/tuple/list/dict/frozenset({…})."""
    kq = {}
    for n in t.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            v = n.value
            if isinstance(v, ast.Call) and isinstance(v.func, ast.Name) and v.func.id in ("frozenset", "set", "tuple") and v.args:
                v = v.args[0]
            if isinstance(v, TAP_TEN):
                kq[n.targets[0].id] = v
    return kq


def _bien_regex(p):
    """Các phép sửa tất định trên MỘT mẫu regex (chuỗi). Trả [(mã, mô tả, mẫu mới)]."""
    out, n = [], len(p)
    # i1/i2: lớp ký tự
    for m in re.finditer(r"(?<!\\)\[((?:\\.|[^\]\\])+)\]", p):
        tv = re.findall(r"\\.|.-.|.", m[1])
        for k in range(len(tv)):
            if len(tv) > 1:
                out.append(("i1", f"lop@{m.start()} bo {tv[k]!r}", p[:m.start()] + "[" + "".join(tv[:k] + tv[k + 1:]) + "]" + p[m.end():]))
        out.append(("i2", f"lop@{m.start()} thanh .", p[:m.start()] + "." + p[m.end():]))
    # i3: nhánh alternation trong nhóm cấp một (bỏ từng nhánh)
    for m in re.finditer(r"\((?:\?[:=!<][!=]?)?([^()]*\|[^()]*)\)", p):
        nh = m[1].split("|")
        for k in range(len(nh)):
            moi = "|".join(nh[:k] + nh[k + 1:])
            out.append(("i3", f"nhanh@{m.start()} bo {nh[k]!r}", p[:m.start(1)] + moi + p[m.end(1):]))
    # i4: lượng từ
    for m in re.finditer(r"(?<!\\)(\+|\{\d+(?:,\d*)?\})", p):
        out.append(("i4", f"luong_tu@{m.start()} {m[1]}→*", p[:m.start()] + "*" + p[m.end():]))
    # i5: escape thành wildcard
    for m in re.finditer(r"\\([.()\[\]dsw])", p):
        out.append(("i5", f"escape@{m.start()} \\{m[1]}→.", p[:m.start()] + "." + p[m.end():]))
    # i6: lookaround
    for m in re.finditer(r"\(\?(?:<[!=]|[=!])", p):
        sau, sau_i = 1, m.end()
        while sau and sau_i < n:
            c = p[sau_i]
            if c == "\\":
                sau_i += 2
                continue
            sau += (c == "(") - (c == ")")
            sau_i += 1
        out.append(("i6", f"lookaround@{m.start()} bo", p[:m.start()] + p[sau_i:]))
    return out


def sinh(nguon):
    goc = ast.parse(nguon)
    base = ast.unparse(goc)
    kq, thay = [], set()

    def them(op, ten, cay_or_src, dong):
        s = cay_or_src if isinstance(cay_or_src, str) else ast.unparse(cay_or_src)
        if s == base or s in thay:
            return
        try:
            compile(s, ten, "exec")
        except SyntaxError:
            return
        thay.add(s)
        mid = f"{op}:{ten}"
        mid = mid if mid not in {x["id"] for x in kq} else f"{mid}#{sum(x['id'].startswith(mid) for x in kq)}"
        kq.append({"id": mid, "op": op, "dong": dong, "sha256": hashlib.sha256(s.encode()).hexdigest(), "src": s})

    nut = list(ast.walk(goc))
    for i, n in enumerate(nut):
        cha = _cha(goc)
        h = _ham(n, cha)

        def cay():
            t = copy.deepcopy(goc)
            return t, list(ast.walk(t))[i], _cha(t)

        def thay_nut(t, cu, moi, ct):
            p = ct[cu]
            for f, v in ast.iter_fields(p):
                if v is cu:
                    setattr(p, f, moi)
                    return
                if isinstance(v, list):
                    for k, x in enumerate(v):
                        if x is cu:
                            v[k] = moi
                            return
        dong = getattr(n, "lineno", 0)
        ten = f"{h or 'module'}:{dong}:{getattr(n, 'col_offset', 0)}"
        if h is not None:
            if isinstance(n, ast.Compare):
                t, m, ct = cay(); thay_nut(t, m, ast.UnaryOp(ast.Not(), m), ct); them("a", ten, t, dong)
                if any(isinstance(o, (ast.Is, ast.IsNot)) for o in n.ops):
                    t, m, ct = cay()
                    m.ops = [ast.Eq() if isinstance(o, ast.Is) else ast.NotEq() if isinstance(o, ast.IsNot) else o for o in m.ops]
                    them("j1", ten, t, dong)
                if (len(n.ops) == 1 and isinstance(n.ops[0], ast.Is) and isinstance(n.comparators[0], ast.Constant)
                        and n.comparators[0].value is True):
                    t, m, ct = cay(); thay_nut(t, m, m.left, ct); them("j2", ten, t, dong)
                if (len(n.ops) == 1 and isinstance(n.ops[0], (ast.In, ast.NotIn)) and isinstance(n.comparators[0], ast.Name)
                        and n.comparators[0].id in _hang_module(goc)):
                    t, m, ct = cay()
                    moi = ast.parse(f"any(_p_ in ({ast.unparse(m.left)}) for _p_ in {m.comparators[0].id})", mode="eval").body
                    if isinstance(m.ops[0], ast.NotIn):
                        moi = ast.UnaryOp(ast.Not(), moi)
                    thay_nut(t, m, moi, ct); them("k3", ten, t, dong)
            if isinstance(n, (ast.If, ast.IfExp, ast.While)) and not isinstance(n.test, ast.Compare):
                t, m, ct = cay(); m.test = ast.UnaryOp(ast.Not(), m.test); them("a2", ten, t, dong)
            if isinstance(n, ast.comprehension):
                for k in range(len(n.ifs)):
                    t, m, ct = cay(); m.ifs[k] = ast.UnaryOp(ast.Not(), m.ifs[k]); them("a2", f"{ten}:if{k}", t, dong)
                    t, m, ct = cay(); del m.ifs[k]; them("a2", f"{ten}:bo_if{k}", t, dong)
            if isinstance(n, ast.BoolOp):
                for k in range(len(n.values)):
                    t, m, ct = cay(); vs = [v for j, v in enumerate(m.values) if j != k]
                    thay_nut(t, m, vs[0] if len(vs) == 1 else ast.BoolOp(m.op, vs), ct); them("b", f"{ten}:ve{k}", t, dong)
            if (isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Attribute)
                    and n.value.func.attr in ("append", "extend")) or isinstance(n, ast.AugAssign):
                t, m, ct = cay(); thay_nut(t, m, ast.Pass(), ct); them("c", ten, t, dong)
            if isinstance(n, ast.Return):
                t, m, ct = cay(); thay_nut(t, m, ast.Pass(), ct); them("c2", ten, t, dong)
                if n.value is not None:
                    t, m, ct = cay(); m.value = ast.Constant(None); them("f", ten, t, dong)
            if isinstance(n, ast.Constant) and isinstance(n.value, bool):
                t, m, ct = cay(); m.value = not m.value; them("d", ten, t, dong)
            if isinstance(n, ast.Constant) and type(n.value) is int:
                t, m, ct = cay(); m.value += 1; them("e", ten, t, dong)
            if isinstance(n, ast.Constant) and isinstance(n.value, str) and not _docstring(n, cha) and n.value:
                t, m, ct = cay(); m.value = m.value + "~"; them("g", ten, t, dong)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
                if n.func.attr in CHUAN_HOA and not n.args:
                    t, m, ct = cay(); thay_nut(t, m, m.func.value, ct); them("k1", ten, t, dong)
                if n.func.attr in DOI_PT:
                    t, m, ct = cay(); m.func.attr = DOI_PT[m.func.attr]; them("k2", ten, t, dong)
                if n.func.attr in ("fullmatch", "match"):
                    t, m, ct = cay(); m.func.attr = "match" if m.func.attr == "fullmatch" else "search"; them("i7", ten, t, dong)
        if isinstance(n, (ast.FunctionDef, ast.For, ast.If, ast.With, ast.Try)) and (h is not None or isinstance(n, ast.FunctionDef)):
            for fld in ("body", "orelse"):
                b = getattr(n, fld, None) or []
                for k in range(len(b) - 1):
                    x, y = b[k], b[k + 1]
                    if all(isinstance(z, ast.If) and z.body and isinstance(z.body[-1], ast.Return) for z in (x, y)):
                        t, m, ct = cay(); bb = getattr(m, fld); bb[k], bb[k + 1] = bb[k + 1], bb[k]
                        them("l", f"{ten}:{fld}{k}", t, x.lineno)
    # h1/h2: tập hằng mức module
    for ten, v in _hang_module(goc).items():
        so = len(v.keys) if isinstance(v, ast.Dict) else len(v.elts)
        for k in range(so):
            t = copy.deepcopy(goc); vv = _hang_module(t)[ten]
            if isinstance(vv, ast.Dict):
                del vv.keys[k]; del vv.values[k]
            else:
                del vv.elts[k]
            them("h1", f"{ten}:{k}", t, v.lineno)
        t = copy.deepcopy(goc); vv = _hang_module(t)[ten]
        if isinstance(vv, ast.Dict):
            vv.keys.append(ast.Constant("~them~")); vv.values.append(copy.deepcopy(vv.values[0]) if vv.values else ast.Constant(None))
        else:
            vv.elts.append(ast.Constant("~them~"))
        them("h2", ten, t, v.lineno)
    # i1–i6: regex hằng mức module (re.compile(<chuỗi>))
    for n in goc.body:
        if (isinstance(n, ast.Assign) and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Attribute)
                and n.value.func.attr == "compile" and n.value.args and isinstance(n.value.args[0], ast.Constant)):
            ten = n.targets[0].id
            for op, mo_ta, moi in _bien_regex(n.value.args[0].value):
                try:
                    re.compile(moi)
                except re.error:
                    continue
                t = copy.deepcopy(goc)
                q = next(q for q in t.body if isinstance(q, ast.Assign) and getattr(q.targets[0], "id", None) == ten)
                q.value.args[0].value = moi
                them(op, f"{ten}:{mo_ta}", t, n.lineno)
    return kq


# ---------------------------------------------------------------- chạy
_CHAY_CA = r'''
import sys, importlib.util, copy, yaml
_goc, _bo = yaml.safe_load, {}
def _nho(x):
    k = x if isinstance(x, (str, bytes)) else None
    if k is None:
        return _goc(x)
    if k not in _bo:
        _bo[k] = _goc(x)
    return copy.deepcopy(_bo[k])
yaml.safe_load = _nho
spec = importlib.util.spec_from_file_location("godc_test", sys.argv[1])
m = importlib.util.module_from_spec(spec); sys.modules["godc_test"] = m; spec.loader.exec_module(m)
for ten in m.CA:
    rc, dong = m.chay_ca(ten)
    if rc == 3:
        print("GIET", ten); break
    elif rc:
        print("HONG", ten, dong[:200].replace("\n", " "))
'''


def _mot(m, test, thu):
    p = Path(tempfile.mkdtemp(dir=thu)) / "gate_output_doi_chieu.py"   # thư mục riêng từng đột biến: không đụng tên, không đụng .pyc
    p.write_text(m["src"], encoding="utf-8")
    r = subprocess.run([sys.executable, "-B", "-c", _CHAY_CA, str(test)], capture_output=True, timeout=1800,
                       env=dict(os.environ, GATE_OUTPUT_DOI_CHIEU_MA=str(p), PYTHONDONTWRITEBYTECODE="1"))
    ra = r.stdout.decode("utf-8", "replace").splitlines()
    p.unlink()
    return {"id": m["id"], "op": m["op"], "dong": m.get("dong"), "sha256": m.get("sha256"), "rc": r.returncode,
            "giet": [x.split()[1] for x in ra if x.startswith("GIET ")], "hong": [x for x in ra if x.startswith("HONG ")],
            "stderr_cuoi": r.stderr.decode("utf-8", "replace")[-300:] if r.returncode else ""}


def chay(manifest, test, ra, ss):
    ms = [json.loads(x) for x in Path(manifest).read_text(encoding="utf-8").splitlines() if x.strip()]
    ms = [m for m in ms if m.get("src")]
    if len({m["id"] for m in ms}) != len(ms):
        raise SystemExit("id trung trong manifest")
    xong = {json.loads(x)["id"] for x in Path(ra).read_text(encoding="utf-8").splitlines()} if Path(ra).exists() else set()
    ms = [m for m in ms if m["id"] not in xong]
    with tempfile.TemporaryDirectory(prefix="quet_db_") as thu, cf.ThreadPoolExecutor(ss) as ex, open(ra, "a", encoding="utf-8") as f:
        for kq in ex.map(lambda m: _mot(m, Path(test).resolve(), thu), ms):
            f.write(json.dumps(kq, ensure_ascii=False) + "\n")
            f.flush()
    kq = [json.loads(x) for x in Path(ra).read_text(encoding="utf-8").splitlines()]
    song = [k for k in kq if not k["giet"]]
    print(f"TONG {len(kq)} · GIET {len(kq) - len(song)} · SONG_SACH {sum(not k['hong'] for k in song)} · CHI_LOI_VO_CAN "
          f"{sum(bool(k['hong']) for k in song)}")
    for k in song:
        print(f"SONG {k['id']} {'(loi vo can) ' + k['hong'][0][:120] if k['hong'] else ''}")
    return 0


# ---------------------------------------------------------------- hồi quy kho cũ
def hoi_quy(kho, goc, dich, ra):
    d = Path(dich).read_text(encoding="utf-8")
    out = []
    if str(kho).endswith(".jsonl"):
        for x in (json.loads(y) for y in Path(kho).read_text(encoding="utf-8").splitlines() if y.strip()):
            if d.count(x["cu"]) != 1:
                out.append({"id": f"kho:{x['id']}", "op": "kho", "trang_thai": "KHONG_AP_DUNG", "ly_do": f"neo xuat hien {d.count(x['cu'])} lan"})
                continue
            s = d.replace(x["cu"], x["moi"])
            out.append({"id": f"kho:{x['id']}", "op": "kho", "kind": x.get("kind"), "cu": x["cu"], "moi": x["moi"],
                        "sha256": hashlib.sha256(s.encode()).hexdigest(), "src": s})
        Path(ra).write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in out), encoding="utf-8")
        print(f"HOI_QUY {len(out)} · AP_DUNG {sum('src' in x for x in out)} · KHONG_AP_DUNG {sum('src' not in x for x in out)}")
        return 0
    g = Path(goc).read_text(encoding="utf-8")
    for mid, v in sorted(json.loads(Path(kho).read_text(encoding="utf-8")).items()):
        a, b = g.splitlines(keepends=True), v["src"].splitlines(keepends=True)
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
        if not ops:
            out.append({"id": f"kho:{mid}", "op": "kho", "trang_thai": "KHONG_AP_DUNG", "ly_do": "trung goc"})
            continue
        i1, i2, j1, j2 = ops[0][1], ops[-1][2], ops[0][3], ops[-1][4]
        cu, moi = "".join(a[i1:i2]), "".join(b[j1:j2])
        k = 0
        while d.count(cu) != 1 and (i1 - k > 0 or i2 + k < len(a)):   # nới ngữ cảnh tới khi neo duy nhất
            k += 1
            cu = "".join(a[max(0, i1 - k):min(len(a), i2 + k)])
            moi = "".join(a[max(0, i1 - k):i1]) + "".join(b[j1:j2]) + "".join(a[i2:min(len(a), i2 + k)])
        if d.count(cu) != 1:
            out.append({"id": f"kho:{mid}", "op": "kho", "trang_thai": "KHONG_AP_DUNG", "ly_do": f"neo xuat hien {d.count(cu)} lan"})
            continue
        s = d.replace(cu, moi)
        out.append({"id": f"kho:{mid}", "op": "kho", "kind": v.get("kind"), "cu": cu, "moi": moi,
                    "sha256": hashlib.sha256(s.encode()).hexdigest(), "src": s})
    Path(ra).write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in out), encoding="utf-8")
    print(f"HOI_QUY {len(out)} · AP_DUNG {sum('src' in x for x in out)} · KHONG_AP_DUNG {sum('src' not in x for x in out)}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="lenh", required=True)
    a = sp.add_parser("sinh"); a.add_argument("module"); a.add_argument("--ra", default="manifest.jsonl")
    b = sp.add_parser("chay"); b.add_argument("manifest"); b.add_argument("test"); b.add_argument("--ra", default="kq.jsonl")
    b.add_argument("--song-song", type=int, default=4)
    c = sp.add_parser("hoi-quy"); c.add_argument("kho"); c.add_argument("goc"); c.add_argument("dich")
    c.add_argument("--ra", default="hoi_quy.jsonl")
    x = ap.parse_args(argv)
    if x.lenh == "sinh":
        ms = sinh(Path(x.module).read_text(encoding="utf-8"))
        Path(x.ra).write_text("".join(json.dumps(m, ensure_ascii=False) + "\n" for m in ms), encoding="utf-8")
        dem = {}
        for m in ms:
            dem[m["op"]] = dem.get(m["op"], 0) + 1
        print(f"SINH {len(ms)} " + " ".join(f"{k}={dem.get(k, 0)}" for k in TOAN_TU))
        return 0
    if x.lenh == "chay":
        return chay(x.manifest, x.test, x.ra, x.song_song)
    return hoi_quy(x.kho, x.goc, x.dich, x.ra)


if __name__ == "__main__":
    sys.exit(main())
