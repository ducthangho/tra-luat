#!/usr/bin/env python3
"""Phép đo của executor cho wp1462 (B4) — KHÔNG phải `*_test.py`, không nằm trong cổng nào. Chạy từ gốc kho, in kết quả ra stdout.

  ab        tiêu chí 1–2: mọi ca hiện có đi qua bộ dựng `_c1106`, dựng MỘT lần, chạy `packet_loop.py` của base (merge-base với
            origin/master) và của head trên CÙNG fixture, mỗi vế kèm `launcher.py` của chính nó; kèm tự kiểm bộ so.
  phat-lai  tiêu chí 8: 60 merge của lịch sử thật qua HÀM CHẠY (`_b4_tinh_lai`) so với đường trực tiếp + hồi quy khung dòng LF/CRLF.
  dot-bien  tiêu chí 4: bảng (đột biến · ca · lớp ngoại lệ · phân hạng) cho mọi mục `b4_*` của bảng `MUTANTS`.
Thoát 0 = đạt; 1 = có lệch (in từng dòng `ĐỎ`)."""
import contextlib
import hashlib
import importlib.util
import io
import os
import subprocess
import sys
import tempfile
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
def do_ca(T, kich_ban, td, ten_ca):
    """Chạy các ca `ten_ca` của bộ test `T`, bắt MỌI lời `kiem-merge` đi qua `_c1106`: mỗi lời chạy trên từng script của `kich_ban` (cùng fixture)."""
    ghi, trong, cu = {}, [0], (T._c1106, T.run, T._rev_list_loi, T._transition_run1187)

    def boc(goc):
        def chay(script, args, sd, *a, **k):
            if not trong[0] or not args or str(args[0]) != "kiem-merge":
                return goc(script, args, sd, *a, **k)
            ra = [goc(s, args, Path(f"{sd}-{i}"), *a, **k) for i, s in enumerate(kich_ban)]
            ghi.setdefault(trong[1], []).append([(r[0], bytes(r[1]), bytes(r[2])) for r in ra])
            return ra[-1]
        return chay

    def c1106(*a, **k):
        trong[0] += 1
        try:
            return cu[0](*a, **k)
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
        for ten, fn in T.CASES:
            if ten in ten_ca:
                trong[1:] = [ten]
                d = Path(tempfile.mkdtemp(prefix="ca-", dir=td))
                try:
                    fn(T.Ctx(kich_ban[-1], d))
                except BaseException as ex:  # noqa: BLE001 — kỳ vọng của ca không phải phép đo ở đây; chỉ cần các lời gọi đã ghi
                    if isinstance(ex, KeyboardInterrupt):
                        raise
    finally:
        T._c1106, T.run, T._rev_list_loi, T._transition_run1187 = cu
    return ghi


def cham_c1106(T, f, sau=3):
    """Lọc TĨNH rẻ để khỏi chạy cả sổ ca (phép đếm thật là ĐỘNG, ở `do_ca`): mã của ca, closure của nó và các hàm mức module nó nhắc tên (≤ 3 tầng) có nhắc `_c1106`."""
    co = getattr(f, "__code__", None)
    if co is None or sau < 0:
        return False
    ten = set(co.co_names) | {n for k in co.co_consts if hasattr(k, "co_names") for n in k.co_names}
    o = [c.cell_contents for c in getattr(f, "__closure__", None) or () if c.cell_contents is not f]
    return bool(ten & {"_c1106", "_c1106_ca"}) or any(cham_c1106(T, g, sau - 1) for g in [*o, *(vars(T).get(n) for n in ten)] if callable(g))


def lenh_ab():
    base = git("merge-base", "HEAD", "refs/remotes/origin/master").decode().strip()
    loi = tu_kiem_bo_so()
    with tempfile.TemporaryDirectory(prefix="b4ab-") as td:
        td = Path(td)
        for ve, lay in (("base", lambda p: git("show", f"{base}:.claude/dev/{p}")), ("head", lambda p: (DEV / p).read_bytes())):
            (td / ve).mkdir()
            for p in ("packet_loop.py", "launcher.py", "packet_loop_test.py"):
                (td / ve / p).write_bytes(lay(p))
        Tb, Th = nap("plt_base", td / "base/packet_loop_test.py"), nap("plt_head", td / "head/packet_loop_test.py")
        for T in (Tb, Th):   # như vòng đột biến của chính bộ test: fixture canonical đọc từ kho thật, `__file__` vẫn là bản sao
            T.HERE, T.ROOT = DEV, ROOT
        ung = lambda T: {t for t, f in T.CASES if not t.startswith("cong_b4_") and cham_c1106(T, f)}  # noqa: E731
        nen = do_ca(Tb, [td / "base/packet_loop.py"], td, ung(Tb))
        ghi = {}
        for hinh, sua in (("moi", None), ("cu", lambda h, *a, **k: [])):
            goc = Th._b4_manh
            Th._b4_manh = sua or goc
            try:
                ghi[hinh] = do_ca(Th, [td / "base/packet_loop.py", td / "head/packet_loop.py"], td, ung(Th))
            finally:
                Th._b4_manh = goc
    loi += [f"tiêu chí 1: thiếu ca {t} (base có {len(nen[t])} lời kiem-merge)" for h in ghi for t in nen if len(ghi[h].get(t, [])) != len(nen[t])]
    loi += [f"tiêu chí 1 (hình dạng mới, B-2): {t} lời {i} lệch byte: rc {b[0]}/{h[0]}" for t, ds in ghi["moi"].items() for i, (b, h) in enumerate(ds) if b != h]
    lop = {}
    for t, ds in ghi["cu"].items():
        for i, (b, h) in enumerate(ds):
            k, e = so(b, h)
            lop.setdefault(k, []).append(t)
            loi += [f"tiêu chí 2: {t} lời {i} lớp ({k}): {e}"] * bool(e)
    z = sorted(set(lop.get("z", [])))
    loi += [f"tiêu chí 2: ca {t} phải thuộc lớp (z)" for t in ("cong_c_k1_anchor", "cong_c_k1_yaml_hong", "cong_c_k1_khoa_trung", "cong_c_k1_tag_hong") if t not in z]
    print(f"base {base}\nca đi qua _c1106 tại base: {len(nen)} · tại head (so được): moi {len(ghi['moi'])} · cu {len(ghi['cu'])} · lời kiem-merge: {sum(map(len, nen.values()))}")
    print("tiêu chí 2 — số lời theo lớp: " + " · ".join(f"({k}) {len(v)}" for k, v in sorted(lop.items())) + f"\nlớp (z): {z}\ntên ca: {sorted(nen)}")
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
def lenh_dot_bien():
    T, loi = nap("packet_loop_test", DEV / "packet_loop_test.py"), []
    goc = T.CANONICAL.read_text(encoding="utf-8")
    print("| đột biến | ca đích | lớp ngoại lệ | phân hạng |\n|---|---|---|---|")
    with tempfile.TemporaryDirectory(prefix="b4db-") as td:
        for i, (ten, (tim, thay, dich)) in enumerate((k, v) for k, v in T.MUTANTS.items() if k.startswith("b4_")):
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
    lenh = {"ab": lenh_ab, "phat-lai": lenh_phat_lai, "dot-bien": lenh_dot_bien}.get(sys.argv[1] if len(sys.argv) == 2 else "")
    if not lenh:
        sys.exit(__doc__)
    ds = lenh()
    print("\n".join(f"ĐỎ  {x}" for x in ds) or "không lệch")
    print(f"KẾT QUẢ {sys.argv[1]}: {'ĐẠT' if not ds else str(len(ds)) + ' lỗi'}")
    sys.exit(int(bool(ds)))
