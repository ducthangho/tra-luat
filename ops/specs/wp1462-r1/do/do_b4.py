#!/usr/bin/env python3
"""Phép đo của executor cho wp1462 (B4) — KHÔNG phải `*_test.py`, không nằm trong cổng nào. Chạy từ gốc kho, in kết quả ra stdout.

  ab        tiêu chí 1–2: ĐẾM quần thể bằng cách chạy CẢ sổ ca của base với máy đếm ở `_c1106` (không lọc tĩnh), rồi dựng MỖI ca MỘT lần và chạy
            `packet_loop.py` của base (merge-base với origin/master) và của head trên CÙNG fixture, mỗi vế kèm `launcher.py` của chính nó. Tiêu chí 1
            (r9) xếp mỗi ca vào đúng MỘT nhóm: (a) chạm CLI — so từng byte; (b) ĐO được 0 lần chạm CLI ở cả hai vế — so chuỗi ngoại lệ; (c) ca tự
            sửa script — dựng lại phép sửa trên từng vế, so byte sau chuẩn hoá số dòng traceback. Kèm tự kiểm bộ so, phép đếm/nhóm và đột biến bộ so.
  phat-lai  tiêu chí 8: 60 merge của lịch sử thật qua HÀM CHẠY (`_b4_tinh_lai`) so với đường trực tiếp + hồi quy khung dòng LF/CRLF.
  dot-bien  tiêu chí 4: bảng (đột biến · ca · lớp ngoại lệ · phân hạng) cho mọi mục `b4_*` của bảng `MUTANTS`.
`ab` và `dot-bien` nhận thêm lát `i/n` (chạy song song n tiến trình; quần thể = hợp các lát). Thoát 0 = đạt; 1 = có lệch (in từng dòng `ĐỎ`)."""
import contextlib
import hashlib
import importlib.util
import io
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DEV, OID0, BANG = ROOT / ".claude/dev", "0f9aa2a2cc697129e1f5be72feddf60986286865", "aa932267e766cf3f6e242f35febe3692909f3e909cb510177ba83d780bfc849a"
DU, CHUA, K2B, BA_LOAI = "ĐỦ ĐIỀU KIỆN MERGE trên ", "CHƯA ĐỦ ĐIỀU KIỆN MERGE: thiếu ", "K2b làn G5", ("LAN_G5 ", "CONG_TAC ", "HIEU_LUC ")
git = lambda *a, **k: subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, check=True, **k).stdout  # noqa: E731


def nap(ten, tep):
    sys.path.insert(0, str(Path(tep).parent))
    sp = importlib.util.spec_from_file_location(ten, tep)
    m = importlib.util.module_from_spec(sp)
    sys.modules[ten] = m
    sp.loader.exec_module(m)
    return m


# --- tiêu chí 2: bộ so + phép chiếu P -------------------------------------------------------------------------------------------
def xep_lop(b):
    du, tk = [x for x in b[1].decode().splitlines() if x.startswith(DU)], [x for x in b[2].decode().splitlines() if x.startswith(CHUA)]
    return "?" if (du and tk) or len(du) > 1 or len(tk) > 1 else "z" if not du and not tk else "c" if du else "a" if "K2 CI" in tk[0][len(CHUA):].split("; ") else "b"


def so(b, h):
    """(lớp, lỗi | None) của một ca hình dạng CŨ: (z) và (a) trùng byte, không qua P; (b) P(head) = base + đúng một `LAN_G5`, một `THIẾU` K2b; (c) head rc 12,
    stdout đúng một `LAN_G5`, stderr đúng dòng `THIẾU` K2b + tổng kết chỉ nêu K2b."""
    lop, ho, he = xep_lop(b), h[1].decode().splitlines(True), h[2].decode().splitlines(True)
    lan, thieu = [x for x in ho if x.startswith("LAN_G5 ")], [x for x in he if x.lstrip().startswith(f"THIẾU  {K2B}: ")]
    p_o = "".join(x for x in ho if not x.startswith(BA_LOAI))
    p_e = "".join(x.replace("; " + K2B, "").replace(K2B + "; ", "") if x.startswith(CHUA) else x for x in he if x not in thieu)
    if lop == "?":
        return lop, "không xếp được lớp (có cả hai dòng, hoặc dòng lặp)"
    if lop in "za":
        return lop, None if b == h else "phải trùng byte với base, không qua phép chiếu"
    if b[0] != 0 and h[0] == 0:
        return lop, "B-1: base đỏ mà head đạt"
    if lop == "b":
        return lop, None if (h[0] == b[0] and (p_o, p_e) == (b[1].decode(), b[2].decode()) and len(lan) == len(thieu) == 1) else "P(head) ≠ base, rc lệch, hoặc không đúng một LAN_G5 + một THIẾU K2b"
    return lop, None if (h[0] == 12 and ho == lan and len(lan) == 1 and len(he) == 2 and he[:1] == thieu and he[1].strip() == CHUA + K2B) else "lớp (c): head phải rc 12, đúng một LAN_G5, đúng THIẾU K2b + tổng kết chỉ K2b"


def tu_kiem_bo_so():
    E = lambda s: s.encode()  # noqa: E731
    lan, th, k4 = "LAN_G5 che_do_thuc_chay=khac buoc=tu_kiem lop=chua_tinh master=- ket_qua=do\n", f"  THIẾU  {K2B}: x\n", "  THIẾU  K4 review offline: y\n"
    z, a, b, c = (2, b"", E("không đọc được --lease: YAML hỏng\n")), (12, b"", E(f"  THIẾU  K2 CI: x\n{CHUA}K2 CI\n")), (12, b"", E(f"{k4}{CHUA}K4 review offline\n")), (0, E(DU + "h\n"), b"")
    hb, hc = (12, E(lan), E(f"{k4}{th}{CHUA}K4 review offline; {K2B}\n")), (12, E(lan), E(f"{th}{CHUA}{K2B}\n"))
    ca = [("nhận (b)", b, hb, True), ("nhận (c)", c, hc, True), ("nhận (z) không đổi", z, z, True), ("nhận (a) không đổi", a, a, True),
          ("từ chối dòng stdout lạ", b, (12, E(lan + "khac\n"), hb[2]), False), ("từ chối hai LAN_G5", b, (12, E(lan * 2), hb[2]), False),
          ("từ chối THIẾU khác đổi một ký tự", b, (12, hb[1], hb[2].replace(b"offline: y", b"offline: z")), False), ("từ chối rc lệch ở (b)", b, (2, hb[1], hb[2]), False),
          ("từ chối (a) có hiện vật K2b", a, (12, E(lan), a[2]), False), ("từ chối (z) có LAN_G5", z, (2, E(lan), z[2]), False),
          ("từ chối (z) có THIẾU K2b", z, (2, b"", E(th) + z[2]), False), ("từ chối lỗi lease (z) đổi một ký tự", z, (2, b"", z[2].replace(b"YAML", b"YAMl")), False),
          ("từ chối base đỏ mà head đạt (B-1)", b, c, False), ("từ chối (c) không có LAN_G5", c, (12, b"", hc[2]), False)]
    return [f"tự kiểm bộ so: {ten}" for ten, x, y, mong in ca if (so(x, y)[1] is None) is not mong]


# --- tiêu chí 1–2 ---------------------------------------------------------------------------------------------------------------
def bien_the(goc, sua, s):
    """Phép sửa mà ca tự làm (`goc` → `sua`, byte), mở ra TRỌN DÒNG, dựng lại trên `s`; đoạn gốc không duy nhất ở `goc` hay `s` ⇒ None (ĐỎ ở bộ gọi)."""
    p = len(os.path.commonprefix([goc, sua]))
    q = min(len(os.path.commonprefix([goc[::-1], sua[::-1]])), len(goc) - p, len(sua) - p)
    a, b = goc.rfind(b"\n", 0, p) + 1, (goc.find(b"\n", len(goc) - q) + 1 or len(goc)) if q else len(goc)
    cu, moi = goc[a:b], sua[a:len(sua) - (len(goc) - b)]
    return s.replace(cu, moi, 1) if goc.count(cu) == s.count(cu) == 1 else None


MON = {"n": 0, "do": False}   # máy đếm CHẠM CLI: vào `main` của một `packet_loop.py` trong tiến trình, hoặc sinh tiến trình nhắc tới `packet_loop.py`


def bat_dem_cli():
    """Bật máy đếm chạm CLI (một lần mỗi tiến trình). Không có `sys.monitoring` ⇒ `MON["do"]` giữ False ⇒ không đo được ⇒ không ca nào vào (b)."""
    mo = getattr(sys, "monitoring", None)
    if MON["do"] or mo is None:
        return

    def vao(code, _):
        if code.co_name != "main" or Path(code.co_filename).name != "packet_loop.py":
            return mo.DISABLE   # tắt sự kiện cho code object ấy: chi phí chỉ ở lần chạy đầu của mỗi hàm
        MON["n"] += 1
    mo.use_tool_id(3, "do_b4"), mo.register_callback(3, mo.events.PY_START, vao), mo.set_events(3, mo.events.PY_START)
    sys.addaudithook(lambda ev, a: MON.__setitem__("n", MON["n"] + 1) if ev.startswith(("subprocess.", "os.exec", "os.posix_spawn", "os.spawn", "os.system"))
                     and "packet_loop.py" in repr(a) else None)
    MON["do"] = True


def chuoi(ex):
    """Chuỗi ngoại lệ: tên lớp ĐẦY ĐỦ (`module.qualname`) và thông điệp của TỪNG tầng, theo `__cause__` rồi `__context__`."""
    ra, thay = [], set()
    while ex is not None and id(ex) not in thay:
        thay.add(id(ex)), ra.append(f"{type(ex).__module__}.{type(ex).__qualname__}({str(ex)!r})")
        ex = ex.__cause__ or ex.__context__
    return " < ".join(ra)


def do_ca(T, kich_ban, td, ten_ca):
    """Chạy các ca `ten_ca` của bộ test `T` với MÁY ĐẾM ở `_c1106`. Trả (ghi, vet, cham). `ghi[ca]` = các lời `kiem-merge`, mỗi lời `(loại, kết cục TỪNG vế)`:
    loại `a` = lời thường, MỌI vế chạy trên CÙNG fixture kể cả khi vế trước ném; loại `c` = ca đưa script do CHÍNH nó sửa: chạy đúng script ấy, rồi dựng lại phép
    sửa trên script của từng vế, chạy ở cùng một chỗ. Kết cục = `(rc, stdout, stderr)`, hoặc chuỗi ngoại lệ (str) khi vế ấy ném. `vet[ca]` = `vao` · `so` ·
    `la:<rc>:so:<dựng lại được>` · `nem:<chuỗi>` (ngoại lệ ra khỏi `_c1106`) · `ca:<dat|lớp>`. `cham[ca]` = số lần chạm CLI đo trong CẢ ca (None: không đo được)."""
    ghi, vet, cham, trong, cu = {}, {}, {}, [0, None], (T._c1106, T.run, T._rev_list_loi, T._transition_run1187)

    def boc(goc):
        def chay(script, args, *a, **k):   # CÙNG chữ ký với hàm gốc (`state_dir` tuỳ chọn): bọc sai chữ ký làm ca hỏng trước khi tới bộ dựng
            if not trong[0] or not args or str(args[0]) != "kiem-merge":
                return goc(script, args, *a, **k)
            sd = lambda i: (Path(f"{a[0]}-{i}"), *a[1:]) if a and a[0] is not None else a  # noqa: E731
            if Path(script) != Path(kich_ban[-1]):
                r, d, ra = goc(script, args, *a, **k), Path(script).parent / "ab-bien-the", []
                d.mkdir(exist_ok=True)
                for i, s in enumerate(kich_ban):
                    bt = bien_the(Path(kich_ban[-1]).read_bytes(), Path(script).read_bytes(), Path(s).read_bytes())
                    (d / "launcher.py").write_bytes((Path(s).parent / "launcher.py").read_bytes()), (d / "packet_loop.py").write_bytes(bt or b"raise SystemExit(99)\n")
                    ra.append(goc(d / "packet_loop.py", args, *sd(f"b{i}"), **k)[:3] + (bt is not None,))
                ghi.setdefault(trong[1], []).append(("c", [(x[0], bytes(x[1]), bytes(x[2])) for x in ra])), vet[trong[1]].append(f"la:{r[0]}:so:{all(x[3] for x in ra)}")
                return r
            ra = []
            for i, s in enumerate(kich_ban):
                try:
                    ra.append(goc(s, args, *sd(i), **k))
                except (Exception, SystemExit) as ex:   # kết cục của từng vế là dữ liệu so; vế sau vẫn chạy
                    ra.append(ex)
            ghi.setdefault(trong[1], []).append(("a", [chuoi(r) if isinstance(r, BaseException) else (r[0], bytes(r[1]), bytes(r[2])) for r in ra])), vet[trong[1]].append("so")
            if isinstance(ra[-1], BaseException):
                raise ra[-1]
            return ra[-1]
        return chay

    def c1106(*a, **k):
        trong[0] += 1
        vet[trong[1]].append("vao")
        try:
            return cu[0](*a, **k)
        except BaseException as ex:
            vet[trong[1]].append(f"nem:{chuoi(ex)}")
            raise
        finally:
            trong[0] -= 1

    def rev_list_loi(script, args, sd, env=None):   # như `_rev_list_loi` của bộ test (rev-list rc -15, stdout đúng) nhưng GIỮ stdout, vì bộ so cần dòng `LAN_G5`
        m, ra, loi = nap("pl_ab", script), io.StringIO(), io.StringIO()
        that, m._git_do = m._git_do, lambda root, *x, **k: (lambda r: (-15, r[1]) if x[0] == "rev-list" else r)(that(root, *x, **k))
        try:
            with contextlib.redirect_stdout(ra), contextlib.redirect_stderr(loi):
                rc = m.main(["--state-dir", str(sd), *map(str, args)])
        except SystemExit as ex:
            rc = ex.code
        return rc, ra.getvalue().encode(), loi.getvalue().encode()
    T._c1106, T.run, T._rev_list_loi, T._transition_run1187 = c1106, boc(cu[1]), boc(rev_list_loi), boc(cu[3])
    try:
        for ten, fn in list(T.CASES):
            if ten in ten_ca:
                trong[1], vet[ten], d, MON["n"] = ten, [], Path(tempfile.mkdtemp(prefix="ca-", dir=td)), 0
                try:
                    if ten in getattr(T, "WINDOWS_ONLY", ()) and os.name != "nt":
                        raise OSError("chỉ đo trên Windows")
                    fn(T.Ctx(kich_ban[-1], d))
                    vet[ten].append("ca:dat")
                except BaseException as ex:  # noqa: BLE001 — kỳ vọng của ca không phải phép đo ở đây; kết cục được GHI, không bị bỏ
                    if isinstance(ex, KeyboardInterrupt):
                        raise
                    vet[ten].append(f"ca:{type(ex).__name__}")
                cham[ten] = MON["n"] if MON["do"] else None
                shutil.rmtree(d, ignore_errors=True)
    finally:
        T._c1106, T.run, T._rev_list_loi, T._transition_run1187 = cu
    return ghi, vet, cham


def quan_the(T, manh=(0, 1)):
    """Quần thể ĐẾM = mọi ca BẮT BUỘC của sổ trên nền này (đúng bộ lọc nền của `main()` của bộ test) trừ ca `cong_b4_*` của chính packet, KHÔNG lọc
    tĩnh (lọc theo tên hàm đã sót các ca tới `_c1106` qua `dict(CASES)`)."""
    nen = platform.system()
    ap = getattr(T, "WP1174_REQUIRED", set()) - {"wp1174_windows_claim_rejected"} if nen == "Linux" else getattr(T, "WP1174_BOTH", set()) if nen == "Windows" else set()
    return {t for t, _ in T.CASES[manh[0]::manh[1]] if not t.startswith("cong_b4_") and (not t.startswith("wp1174_") or t in ap)
            and (nen == "Linux" or t not in getattr(T, "_WP1303_LINUX_CASES", ()))}


# --- tiêu chí 1 (r9): ba nhóm ca, mỗi ca đúng MỘT nhóm -------------------------------------------------------------------------
CHUAN = lambda b: re.sub(rb'(File "[^"\n]*", line )[0-9]+', rb"\1?", b)  # noqa: E731 — phép chuẩn hoá DUY NHẤT, CHỈ cho lời loại `c` của ca nhóm (c)


def xep_nhom(ds, nem, cham):
    """(c) khi ca có lời script tự sửa; (b) CHỈ khi ĐO được 0 lần chạm CLI ở CẢ lượt base lẫn lượt head, có ngoại lệ ra khỏi bộ dựng ở cả hai lượt và không
    lời nào có vế cho byte; còn lại (a) — kể cả ca chạm CLI rồi ném, hay ca không đo được việc chạm CLI."""
    if any(k == "c" for k, _ in ds):
        return "c"
    return "b" if all(c == 0 for c in cham) and nem[0] and nem[1] and all(isinstance(x, str) for _, xs in ds for x in xs) else "a"


def so_nhom(n, ds, nem=((), ())):
    """Lỗi (str) hoặc None của một ca nhóm `n`. (a): mọi lời, mọi vế cho byte và trùng TỪNG BYTE. (b): mọi vế ném, cùng chuỗi ngoại lệ, và chuỗi ngoại lệ ra khỏi
    `_c1106` ở lượt base bằng ở lượt head. (c): lời loại `c` trùng byte SAU `CHUAN`; lời thường của cùng ca vẫn so từng byte."""
    if n == "b":
        return None if nem[0] and nem[0] == nem[1] and all(isinstance(x, str) and x == xs[0] for _, xs in ds for x in xs) else f"(b): chuỗi ngoại lệ lệch hoặc có vế không ném: {nem} {ds}"
    if not ds:
        return f"({n}): không có lời kiem-merge nào để so"
    for k, xs in ds:
        if any(isinstance(x, str) for x in xs):
            return f"({n}): chạm CLI mà có vế ném thay vì cho byte: {xs}"
        f = CHUAN if n == k == "c" else bytes
        if len({(x[0], f(x[1]), f(x[2])) for x in xs}) != 1:
            return f"({n}) lời {k}: lệch byte{' sau chuẩn hoá số dòng' * (f is CHUAN)}: " + " | ".join(f"rc {x[0]} · {x[2][-160:]!r}" for x in xs)
    return None


def phan_nhom(vao, ghi, vet_b, vet_h, cham_b, cham_h):
    """Xếp MỌI ca của quần thể đếm vào đúng một nhóm rồi so theo nhóm. Trả (nhóm → tên ca, lỗi)."""
    nhom, loi = {"a": [], "b": [], "c": []}, []
    for t in sorted(vao):
        nem = tuple([v for v in vt.get(t, []) if v.startswith("nem:")] for vt in (vet_b, vet_h))
        n = xep_nhom(ghi.get(t, []), nem, (cham_b.get(t), cham_h.get(t)))
        nhom[n].append(t)
        e = so_nhom(n, ghi.get(t, []), nem)
        loi += [f"tiêu chí 1 nhóm ({n}): {t}: {e}"] * bool(e)
        for ve, vet in (("base", vet_b), ("head", vet_h)):
            if any(v.startswith("la:") and v.endswith(":so:False") for v in vet.get(t, [])):
                loi.append(f"tiêu chí 1: {t}: {ve} không dựng lại được bản sửa duy nhất")
    so = sum(map(len, nhom.values()))
    return nhom, loi + [f"tiêu chí 1: phân loại {so} ca ≠ đếm {len(vao)}"] * (so != len(vao))


def ngoai_le_tc2(nhom, cham, xs):
    return nhom == "b" and cham == 0 and bool(xs) and all(isinstance(x, str) and x == xs[0] for x in xs)


def tu_kiem_nhom():
    """Tự kiểm bộ so theo nhóm: chuẩn hoá số dòng CHỈ cứu lời `c` của ca (c); (a) lệch đúng số dòng traceback phải ĐỎ."""
    T_ = lambda e: (1, b"", e.encode())  # noqa: E731
    tb = lambda n, x="E": T_(f'Traceback\n  File "/d/packet_loop.py", line {n}, in f\n{x}\n')  # noqa: E731
    i, j = ["nem:m.E('i')"], ["nem:m.E('j')"]
    ca = [("(a) trùng byte", "a", [("a", [tb(1), tb(1)])], ((), ()), True), ("(a) chỉ lệch số dòng traceback", "a", [("a", [tb(1), tb(2)])], ((), ()), False),
          ("(c) lời tự sửa chỉ lệch số dòng", "c", [("c", [tb(1), tb(2)])], ((), ()), True), ("(c) lời tự sửa lệch byte khác", "c", [("c", [tb(1), tb(2, "F")])], ((), ()), False),
          ("(c) lời thường chỉ lệch số dòng", "c", [("c", [tb(1), tb(1)]), ("a", [tb(1), tb(2)])], ((), ()), False),
          ("(a) có vế ném", "a", [("a", ["m.E('i')", tb(1)])], ((), ()), False), ("(a) không lời nào", "a", [], ((), ()), False),
          ("(b) cùng chuỗi", "b", [("a", ["m.E('i')"] * 2)], (i, i), True), ("(b) thông điệp lệch", "b", [("a", ["m.E('i')", "m.E('j')"])], (i, i), False),
          ("(b) chuỗi ra khỏi bộ dựng lệch", "b", [], (i, j), False), ("(b) không có ngoại lệ", "b", [], ((), ()), False), ("(b) có vế cho byte", "b", [("a", ["m.E('i')", tb(1)])], (i, i), False)]
    loi = [f"tự kiểm nhóm: {ten}" for ten, n, ds, nem, mong in ca if (so_nhom(n, ds, nem) is None) is not mong]
    for n, cham, xs, mong in (("b", 0, [i[0], i[0]], True), ("a", 0, [i[0], i[0]], False),
                               ("b", 1, [i[0], i[0]], False), ("b", None, [i[0], i[0]], False),
                               ("b", 0, [i[0], tb(1)], False), ("b", 0, [i[0], j[0]], False)):
        if ngoai_le_tc2(n, cham, xs) != mong:
            loi.append(f"tự kiểm ngoại lệ tiêu chí 2: {n}, {cham}, {xs}")
    return loi


def tu_kiem_dem(td):
    """Tự kiểm phép đếm + phân nhóm trên một sổ ca GIẢ: ca tới `_c1106` qua `dict(CASES)`, ngoại lệ lúc dựng, ngoại lệ ở runner (không chạm CLI), ngoại lệ SAU khi
    chạm CLI (`main` của một `packet_loop.py` có chạy), script do ca tự sửa. Đòi đúng vết, đúng nhóm (ca chạm CLI rồi ném ⇒ (a) và ĐỎ; hai ca không chạm ⇒ (b);
    ca tự sửa ⇒ (c)), số ca phân loại = số ca đếm; vế head in thừa MỘT byte ở ca tự sửa ⇒ ĐỎ."""
    for v, than in (("a", b"x\n1\ny\n"), ("a2", b"x\n1\ny\n"), ("b", b"x\n1\ny\nthua\n"), ("sua", b"")):
        Path(td, v).mkdir(parents=True), Path(td, v, "packet_loop.py").write_bytes(than), Path(td, v, "launcher.py").write_bytes(b"")
    G = types.SimpleNamespace(Ctx=lambda script, d: types.SimpleNamespace(script=script), _rev_list_loi=None, _transition_run1187=None)

    def chay(script, args, sd=None):
        if "cham" in args:   # chạm CLI thật: `main` biên dịch với tên tệp `packet_loop.py`, rồi ném
            exec(compile("def main():\n    pass\n", str(script), "exec"), g := {}), g["main"]()
        if "nem" in args or "cham" in args:
            raise KeyError("runner")
        return 0, b"x" * (b"thua" in Path(script).read_bytes()), b""
    G.run = chay
    la = lambda c: (Path(td, "sua/packet_loop.py").write_bytes(Path(c.script).read_bytes().replace(b"1", b"2")), Path(td, "sua/packet_loop.py"))[1]  # noqa: E731
    G._c1106 = lambda c, kieu="": (_ for _ in ()).throw(OSError("dựng")) if kieu == "dung" else G.run(la(c) if kieu == "la" else c.script, ["kiem-merge", kieu], *("sd",) * (kieu != "khong_sd"))
    G.CASES = [("thang", lambda c: G._c1106(c)), ("gian_tiep", lambda c: dict(G.CASES)["thang"](c)), ("dung_nem", lambda c: G._c1106(c, "dung")),
               ("runner_nem", lambda c: G._c1106(c, "nem")), ("cham_nem", lambda c: G._c1106(c, "cham")), ("script_la", lambda c: G._c1106(c, "la")),
               ("ngoai", lambda c: None), ("khong_sd", lambda c: G._c1106(c, "khong_sd")), ("cong_b4_x", lambda c: G._c1106(c))]
    _, vet, chb = do_ca(G, [Path(td, "a/packet_loop.py")], td, quan_the(G))
    vao = {t for t, v in vet.items() if "vao" in v}
    ghi, vh, chh = do_ca(G, [Path(td, "a/packet_loop.py"), Path(td, "a2/packet_loop.py")], td, vao)
    nhom, loi = phan_nhom(vao, ghi, vet, vh, chb, chh)
    r, k = "nem:builtins.KeyError(\"'runner'\")", ["vao", "so", "ca:dat"]
    mong = {"thang": k, "gian_tiep": k, "khong_sd": k, "dung_nem": ["vao", "nem:builtins.OSError('dựng')", "ca:OSError"], "runner_nem": ["vao", "so", r, "ca:KeyError"],
            "cham_nem": ["vao", "so", r, "ca:KeyError"], "script_la": ["vao", "la:0:so:True", "ca:dat"], "ngoai": ["ca:dat"]}
    nh = {"a": ["cham_nem", "gian_tiep", "khong_sd", "thang"], "b": ["dung_nem", "runner_nem"], "c": ["script_la"]}
    g2 = do_ca(G, [Path(td, "a/packet_loop.py"), Path(td, "b/packet_loop.py")], td, {"script_la"})[0]
    t = "script_la"
    khong_dung_lai = {t: ["vao", "la:99:so:False", "ca:dat"]}
    _, loi_dung_lai = phan_nhom({t}, {t: [("c", [(99, b"", b"")] * 2)]}, khong_dung_lai, khong_dung_lai, {}, {})
    if len(loi_dung_lai) != 2:
        return [f"tự kiểm dựng lại bản sửa: {loi_dung_lai}"]
    ok = (vet, vh, nhom, [x.split(": ")[1] for x in loi], so_nhom("c", g2.get("script_la", [])) is not None) == (mong, {t: mong[t] for t in vao}, nh, ["cham_nem"], True)
    return [] if ok and MON["do"] else [f"tự kiểm phép đếm/nhóm: vết {vet} · nhóm {nhom} · lỗi {loi} (mong {mong} · {nh}); máy đếm CLI bật: {MON['do']}"]


# Đột biến của CHÍNH bộ so (lượt 4): mỗi cái phải làm tự kiểm ĐỎ. Mỏ neo ghép bằng `+` để chính bảng này không khớp mỏ neo.
DOT_BIEN_AB = {"chuan_hoa_ap_cho_a": ("f = CHUAN if n == k == " + '"c" else bytes', "f = CHUAN"),
               "ca_cham_cli_vao_b": ("all(c == 0 for c in " + "cham) and", "True and"),
               "bo_nhom_b": ("        nhom[n].append(" + "t)\n", "        nhom[n].append(t) if n != 'b' else None\n"),
               "bo_nhom_c": ("        return " + '"c"\n', "        pass\n")}


def tu_kiem_dot_bien(td):
    src, loi = Path(__file__).read_text(encoding="utf-8"), []
    for i, (ten, (tim, thay)) in enumerate(DOT_BIEN_AB.items()):
        m = types.ModuleType(f"do_b4_db{i}")
        m.__file__ = __file__
        exec(compile(src.replace(tim, thay, 1), __file__, "exec"), m.__dict__)
        m.MON = MON
        do = m.tu_kiem_bo_so() + m.tu_kiem_nhom() + m.tu_kiem_dem(Path(td, f"db{i}"))
        loi += [f"tự kiểm đột biến {ten}: mỏ neo khớp {src.count(tim)} chỗ, hoặc đột biến SỐNG"] * (src.count(tim) != 1 or not do)
        print(f"đột biến bộ so {ten}: {'GIẾT' if do else 'SỐNG'} ({len(do)} dòng tự kiểm đỏ)")
    return loi


def lenh_ab(manh=(0, 1)):
    base = git("merge-base", "HEAD", "refs/remotes/origin/master").decode().strip()
    bat_dem_cli()
    loi = tu_kiem_bo_so() + tu_kiem_nhom()
    with tempfile.TemporaryDirectory(prefix="b4ab-") as td:
        td = Path(td)
        loi += tu_kiem_dem(td / "dem") + tu_kiem_dot_bien(td / "db")
        for ve, lay in (("base", lambda p: git("show", f"{base}:.claude/dev/{p}")), ("head", lambda p: (DEV / p).read_bytes())):
            (td / ve).mkdir()
            for p in ("packet_loop.py", "launcher.py", "packet_loop_test.py"):
                (td / ve / p).write_bytes(lay(p))
        # Hai bộ test nạp NỐI TIẾP dưới CÙNG tên mô-đun: tên lớp ngoại lệ đầy đủ của hai vế so được. Fixture canonical đọc từ kho thật (như vòng đột biến của bộ test).
        Tb = nap("packet_loop_test", td / "base/packet_loop_test.py")
        Tb.HERE, Tb.ROOT = DEV, ROOT
        nen, vet, chb = do_ca(Tb, [td / "base/packet_loop.py"], td, quan_the(Tb, manh))   # ĐẾM: cả sổ ca của base (lát `manh`), không lọc trước
        vao = {t for t, v in vet.items() if "vao" in v}
        Th = nap("packet_loop_test", td / "head/packet_loop_test.py")
        Th.HERE, Th.ROOT = DEV, ROOT
        ghi, vh, chh = {}, {}, {}
        for hinh, sua in (("moi", None), ("cu", lambda h, *a, **k: [])):
            goc = Th._b4_manh
            Th._b4_manh = sua or goc
            try:
                ghi[hinh], vh[hinh], chh[hinh] = do_ca(Th, [td / "base/packet_loop.py", td / "head/packet_loop.py"], td, vao)
            finally:
                Th._b4_manh = goc
    bo = lambda v: [x for x in v if not x.startswith("ca:")]  # noqa: E731
    loi += [f"quần thể: {t} vết head (hình dạng mới) {vh['moi'].get(t)} ≠ vết base {vet[t]}" for t in sorted(vao) if vh["moi"].get(t) != vet[t]]
    loi += [f"quần thể: {t} vết head (hình dạng cũ) {vh['cu'].get(t)} ≠ vết base {vet[t]} (không kể kết cục ca)" for t in sorted(vao) if bo(vh["cu"].get(t, [])) != bo(vet[t])]
    loi += [f"tiêu chí 1: {t} head ({h}) có {len(ghi[h].get(t, []))} lời kiem-merge, base có {len(nen[t])}" for h in ghi for t in nen if len(ghi[h].get(t, [])) != len(nen[t])]
    nhom, e = phan_nhom(vao, ghi["moi"], vet, vh["moi"], chb, chh["moi"])
    loi += e
    lop, bo_qua = {}, []
    for t, ds in ghi["cu"].items():   # tiêu chí 2: lời có vế ném (nhóm b) không có byte để xếp lớp ⇒ liệt kê; lời `c` so sau CHUAN (cùng phép của tiêu chí 1)
        if any(v.startswith("la:") and v.endswith(":so:False") for v in vh["cu"].get(t, [])):
            loi.append(f"tiêu chí 2: {t}: không dựng lại được bản sửa duy nhất")
        for i, (k, xs) in enumerate(ds):
            if any(isinstance(x, str) for x in xs):
                if ngoai_le_tc2("b" if t in nhom["b"] else "a", chh["cu"].get(t), xs):
                    bo_qua.append(t)
                else:
                    loi.append(f"tiêu chí 2: {t} lời {i}: ngoại lệ thiếu bằng chứng nhóm (b), 0 lần chạm CLI hoặc bằng nhau: {xs}")
                continue
            b, h = ((x[0], CHUAN(x[1]), CHUAN(x[2])) for x in xs) if k == "c" else xs
            lp, er = so(b, h)
            lop.setdefault(lp, []).append(t)
            loi += [f"tiêu chí 2: {t} lời {i} lớp ({lp}): {er}"] * bool(er)
    z = sorted(set(lop.get("z", [])))
    loi += [f"tiêu chí 2: ca {t} phải thuộc lớp (z)" for t in ("cong_c_k1_anchor", "cong_c_k1_yaml_hong", "cong_c_k1_khoa_trung", "cong_c_k1_tag_hong") if t not in z and (manh[1] == 1 or t in vao)]
    kc = {}
    for v in vet.values():
        kc[v[-1]] = kc.get(v[-1], 0) + 1
    print(f"base {base} · lát {manh[0]}/{manh[1]} · máy đếm CLI: {'sys.monitoring + audit hook' if MON['do'] else 'KHÔNG ĐO ĐƯỢC'}\nsổ ca base đã chạy: {len(vet)} · kết cục {dict(sorted(kc.items()))}"
          f"\nca base kết cục không phải đạt/BoQua: {sorted((t, ' '.join(v)) for t, v in vet.items() if v[-1] not in ('ca:dat', 'ca:BoQua'))}")
    print(f"tiêu chí 1: đếm {len(vao)} · phân loại {sum(map(len, nhom.values()))} = (a) {len(nhom['a'])} + (b) {len(nhom['b'])} + (c) {len(nhom['c'])}"
          f" · lời kiem-merge base {sum(map(len, nen.values()))}")
    for n in "abc":
        print(f"nhóm ({n}): " + " ".join(nhom[n]))
    for t in nhom["b"] + nhom["c"]:
        print(f"  bằng chứng {t}: chạm CLI base {chb.get(t)} · head {chh['moi'].get(t)} · vết base {' '.join(vet[t])} · lời head {[(k, [x if isinstance(x, str) else x[0] for x in xs]) for k, xs in ghi['moi'].get(t, [])]}")
    print("tiêu chí 2 — số lời theo lớp: " + " · ".join(f"({k}) {len(v)}" for k, v in sorted(lop.items())) + f" · lời không có byte (nhóm b): {len(bo_qua)}\nlớp (z): {z}")
    return loi


# --- tiêu chí 8 -----------------------------------------------------------------------------------------------------------------
def lenh_phat_lai():
    m, dem, loi = nap("pl_head", DEV / "packet_loop.py"), [0], []
    m._rest_get = lambda *a, **k: (dem.__setitem__(0, dem[0] + 1), (_ for _ in ()).throw(m._B4Loi("phát lại không được đọc công tắc")))[1]
    merges = [x.split() for x in git("log", "--first-parent", "--merges", "-60", "--format=%H %P", OID0).decode().splitlines()]
    with tempfile.TemporaryDirectory(prefix="b4pl-") as td:
        # Bản sao RIÊNG của kho (bare, không hardlink): phép "không thêm ref / worktree / object" đo trên nó, không trên kho dùng chung với phiên khác.
        kho = Path(td, "kho.git")
        subprocess.run(["git", "clone", "-q", "--bare", "--no-hardlinks", str(ROOT), str(kho)], check=True, capture_output=True)
        anh = lambda: [subprocess.run(["git", "-C", str(kho), *x], capture_output=True, check=True).stdout for x in (("for-each-ref",), ("worktree", "list"))] + sorted(  # noqa: E731
            str(p) for p in (kho / "objects").rglob("*"))
        truoc, gd = anh(), str(kho)
        env = {**{k: v for k, v in os.environ.items() if k in m.B4_BIEN_MT}, "GIT_DIR": gd, "GIT_WORK_TREE": td + "/cay", "GIT_INDEX_FILE": td + "/idx",
               "GIT_OBJECT_DIRECTORY": td + "/obj", "GIT_ALTERNATE_OBJECT_DIRECTORIES": gd + "/objects", "CI_DUONG_NHANH_SU_KIEN": "pull_request"}
        os.makedirs(td + "/cay"), os.makedirs(td + "/obj")
        for lenh in (("read-tree", OID0), ("checkout-index", "-a")):
            subprocess.run(["git", *lenh], env=env, cwd=td + "/cay", check=True, capture_output=True)
        crlf = "import io, runpy, sys\nsys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', newline='\\r\\n')\nsys.argv = sys.argv[1:]\nrunpy.run_path(sys.argv[0], run_name='__main__')\n"
        truc_tiep = lambda c, p1, p2, *lenh: subprocess.run([sys.executable, "-I", *lenh, td + "/cay/ops/ci_duong_nhanh.py"], cwd=td + "/cay", capture_output=True, env={  # noqa: E731
            **env, "CI_DUONG_NHANH_GOC": p1, "CI_DUONG_NHANH_DAU": p2, "CI_DUONG_NHANH_MERGE": c})
        bang, dem_lop = "", {}
        for c, p1, p2 in merges:
            lf, rn = truc_tiep(c, p1, p2), truc_tiep(c, p1, p2, "-c", crlf)
            cd = [x[7:] for x in lf.stdout.decode().splitlines() if x.startswith("che_do=")]
            bang += f"{c} {cd[0] if len(cd) == 1 and lf.returncode == 0 else '?'}\n"
            mong, lop = {"duong_nhanh": "duong_nhanh", "day_du": "khong_giam"}.get(cd[0] if cd else ""), m._b4_tinh_lai(kho, OID0, p1, p2)
            dem_lop[lop] = dem_lop.get(lop, 0) + 1
            loi += [f"phát lại {c}: hàm chạy trả {lop!r}, đường trực tiếp {mong!r}"] * (lop != mong)
            a, b = m._b4_doc_lop(lf.returncode, lf.stdout), m._b4_doc_lop(rn.returncode, rn.stdout)
            co_crlf = b"\r\n" in rn.stdout and b"\r\r" not in rn.stdout   # lớp dịch mô phỏng có sinh CRLF thật, và không sinh CR kép
            loi += [f"khung dòng {c}: LF ⇒ {a!r}, CRLF ⇒ {b!r} (CRLF có thật: {co_crlf})"] * (a != b or a != mong or not co_crlf)
        hong = lf.stdout.replace(b"che_do=d", b"che_do=d\r", 1)
        loi += [f"đối chứng hỏng: CR giữa giá trị phải ra 'la', được {m._b4_doc_lop(0, hong)!r}"] * (hong == lf.stdout or m._b4_doc_lop(0, hong) != "la")
        sach = anh() == truoc
    bam = hashlib.sha256(bang.encode()).hexdigest()
    loi += [f"bảng kỳ vọng 60 dòng: sha256 {bam} ≠ {BANG}"] * (bam != BANG) + [f"số lớp {dem_lop} ≠ 18 duong_nhanh + 42 khong_giam"] * (dem_lop != {"duong_nhanh": 18, "khong_giam": 42})
    loi += [f"{dem[0]} yêu cầu REST (đòi 0)"] * bool(dem[0]) + ["kho có thêm ref / worktree / object sau phát lại"] * (not sach)
    print(f"phát lại: {len(merges)} merge · bảng sha256 {bam} · lớp {dem_lop} · REST {dem[0]} · kho (bản sao riêng) sạch: {sach}")
    return loi


# --- tiêu chí 4 -----------------------------------------------------------------------------------------------------------------
def lenh_dot_bien(manh=(0, 1)):
    T, loi = nap("packet_loop_test", DEV / "packet_loop_test.py"), []
    goc = T.CANONICAL.read_text(encoding="utf-8")
    print("| đột biến | ca đích | lớp ngoại lệ | phân hạng |\n|---|---|---|---|")
    with tempfile.TemporaryDirectory(prefix="b4db-") as td:
        for i, (ten, (tim, thay, dich)) in enumerate([(k, v) for k, v in T.MUTANTS.items() if k.startswith("b4_")][manh[0]::manh[1]]):
            than, d = goc, Path(td, f"m{i}")
            d.mkdir()
            for t, th in T._cap_thay_the(tim, thay):
                loi += [f"{ten}: mỏ neo khớp {than.count(t)} chỗ"] * (than.count(t) != 1)
                than = than.replace(t, th, 1)
            (d / "packet_loop.py").write_text(than, encoding="utf-8", newline="\n"), (d / "launcher.py").write_bytes((DEV / "launcher.py").read_bytes())
            dc = T._doi_chung_khac_ho(dich)
            ket = T.chay_suite(d / "packet_loop.py", d, chi_chay=set(dich) | set(dc))
            for t in dich:
                hang = T._b4_hang(ket[t]) if ket.get(t) is not None else "SONG"
                print(f"| {ten} | {t} | {'-' if ket.get(t) is None else str(ket[t]).split(':')[0]} | {hang} |")
                loi += [f"{ten} · {t}: {hang}: {str(ket.get(t))[:300]}"] * (hang != "GIET")
            loi += [f"{ten}: đối chứng khác họ đỏ {t}" for t in dc if ket.get(t) is not None]
    return loi


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="backslashreplace") if isinstance(s, io.TextIOWrapper) else None
    lenh = {"ab": lenh_ab, "phat-lai": lenh_phat_lai, "dot-bien": lenh_dot_bien}.get(sys.argv[1] if len(sys.argv) in (2, 3) else "")
    if not lenh or (len(sys.argv) == 3 and lenh is lenh_phat_lai):
        sys.exit(__doc__)
    ds = lenh(*([tuple(map(int, sys.argv[2].split("/")))] if len(sys.argv) == 3 else []))
    print("\n".join(f"ĐỎ  {x}" for x in ds) or "không lệch")
    print(f"KẾT QUẢ {sys.argv[1]}: {'ĐẠT' if not ds else str(len(ds)) + ' lỗi'}")
    sys.exit(int(bool(ds)))
