#!/usr/bin/env python3
"""Phép đo của executor cho wp1462 (B4) — KHÔNG phải `*_test.py`, không nằm trong cổng nào. Chạy từ gốc kho, in kết quả ra stdout.

  ab        tiêu chí 1–2: ĐẾM quần thể bằng cách chạy CẢ sổ ca của base với máy đếm ở `_c1106` (không lọc tĩnh), rồi với mọi ca đã vào
            bộ dựng: dựng MỘT lần, chạy `packet_loop.py` của base (merge-base với origin/master) và của head trên CÙNG fixture, mỗi vế kèm
            `launcher.py` của chính nó; kèm tự kiểm bộ so và tự kiểm phép đếm. Ca không có lời so được (dừng trước CLI, hoặc chạy script do
            ca tự sửa) được so VẾT + kết cục, không so byte.
  phat-lai  tiêu chí 8: 60 merge của lịch sử thật qua HÀM CHẠY (`_b4_tinh_lai`) so với đường trực tiếp + hồi quy khung dòng LF/CRLF.
  dot-bien  tiêu chí 4: bảng (đột biến · ca · lớp ngoại lệ · phân hạng) cho mọi mục `b4_*` của bảng `MUTANTS`.
`ab` và `dot-bien` nhận thêm lát `i/n` (chạy song song n tiến trình; quần thể = hợp các lát). Thoát 0 = đạt; 1 = có lệch (in từng dòng `ĐỎ`)."""
import contextlib
import hashlib
import importlib.util
import io
import os
import platform
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
def do_ca(T, kich_ban, td, ten_ca):
    """Chạy các ca `ten_ca` của bộ test `T` với MÁY ĐẾM ở `_c1106`, ghi lần VÀO bộ dựng TRƯỚC khi nó chạy. Trả (ghi, vet). `ghi[ca]` = các lời `kiem-merge`
    SO ĐƯỢC (cùng fixture, chạy trên từng script của `kich_ban`). `vet[ca]` = dãy sự kiện: `vao` (vào `_c1106`) · `so` (lời so được) · `la:<rc>` (ca đưa một
    script KHÁC — bản do chính nó sửa — nên chạy ĐÚNG script ấy, không thay) · `nem:<lớp>` (ngoại lệ ra khỏi `_c1106`, kể cả do ca tiêm) · `ca:<dat|lớp>`."""
    ghi, vet, trong, cu = {}, {}, [0, None], (T._c1106, T.run, T._rev_list_loi, T._transition_run1187)

    def boc(goc):
        def chay(script, args, *a, **k):   # CÙNG chữ ký với hàm gốc (`state_dir` tuỳ chọn): bọc sai chữ ký làm ca hỏng trước khi tới bộ dựng
            if not trong[0] or not args or str(args[0]) != "kiem-merge":
                return goc(script, args, *a, **k)
            if Path(script) != Path(kich_ban[-1]):
                r = goc(script, args, *a, **k)
                vet[trong[1]].append(f"la:{r[0]}")
                return r
            ra = [goc(s, args, *((Path(f"{a[0]}-{i}"), *a[1:]) if a and a[0] is not None else a), **k) for i, s in enumerate(kich_ban)]
            ghi.setdefault(trong[1], []).append([(r[0], bytes(r[1]), bytes(r[2])) for r in ra]), vet[trong[1]].append("so")
            return ra[-1]
        return chay

    def c1106(*a, **k):
        trong[0] += 1
        vet[trong[1]].append("vao")
        try:
            return cu[0](*a, **k)
        except BaseException as ex:
            vet[trong[1]].append(f"nem:{type(ex).__name__}")
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
                trong[1], vet[ten], d = ten, [], Path(tempfile.mkdtemp(prefix="ca-", dir=td))
                try:
                    if ten in getattr(T, "WINDOWS_ONLY", ()) and os.name != "nt":
                        raise OSError("chỉ đo trên Windows")
                    fn(T.Ctx(kich_ban[-1], d))
                    vet[ten].append("ca:dat")
                except BaseException as ex:  # noqa: BLE001 — kỳ vọng của ca không phải phép đo ở đây; kết cục được GHI, không bị bỏ
                    if isinstance(ex, KeyboardInterrupt):
                        raise
                    vet[ten].append(f"ca:{type(ex).__name__}")
                shutil.rmtree(d, ignore_errors=True)
    finally:
        T._c1106, T.run, T._rev_list_loi, T._transition_run1187 = cu
    return ghi, vet


def quan_the(T, manh=(0, 1)):
    """Quần thể ĐẾM = mọi ca BẮT BUỘC của sổ trên nền này (đúng bộ lọc nền của `main()` của bộ test) trừ ca `cong_b4_*` của chính packet, KHÔNG lọc
    tĩnh (lọc theo tên hàm đã sót các ca tới `_c1106` qua `dict(CASES)`)."""
    nen = platform.system()
    ap = getattr(T, "WP1174_REQUIRED", set()) - {"wp1174_windows_claim_rejected"} if nen == "Linux" else getattr(T, "WP1174_BOTH", set()) if nen == "Windows" else set()
    return {t for t, _ in T.CASES[manh[0]::manh[1]] if not t.startswith("cong_b4_") and (not t.startswith("wp1174_") or t in ap)
            and (nen == "Linux" or t not in getattr(T, "_WP1303_LINUX_CASES", ()))}


def tu_kiem_dem(td):
    """Tự kiểm phép đếm trên một sổ ca GIẢ: ca tới `_c1106` qua `dict(CASES)`, ngoại lệ lúc dựng, ngoại lệ ở runner và lượt chạy script do ca tự sửa đều
    phải CÓ trong vết với đúng kết cục; ca không vào bộ dựng thì không có `vao`. Khôi phục bộ lọc tĩnh hay bỏ kết cục ngoại lệ ⇒ lệch ⇒ ĐỎ."""
    G = types.SimpleNamespace(Ctx=lambda script, d: types.SimpleNamespace(script=script), _rev_list_loi=None, _transition_run1187=None)
    G.run = lambda script, args, sd=None: (_ for _ in ()).throw(KeyError("runner")) if "nem" in args else (0, b"", b"")
    G._c1106 = lambda c, kieu="": (_ for _ in ()).throw(OSError("dựng")) if kieu == "dung" else G.run(Path("khac.py") if kieu == "la" else c.script, ["kiem-merge", kieu], *("sd",) * (kieu != "khong_sd"))
    G.CASES = [("thang", lambda c: G._c1106(c)), ("gian_tiep", lambda c: dict(G.CASES)["thang"](c)), ("dung_nem", lambda c: G._c1106(c, "dung")),
               ("runner_nem", lambda c: G._c1106(c, "nem")), ("script_la", lambda c: G._c1106(c, "la")), ("ngoai", lambda c: None), ("khong_sd", lambda c: G._c1106(c, "khong_sd")), ("cong_b4_x", lambda c: G._c1106(c))]
    ghi, vet = do_ca(G, [Path("a.py")], td, quan_the(G))
    mong = {"thang": ["vao", "so", "ca:dat"], "gian_tiep": ["vao", "so", "ca:dat"], "dung_nem": ["vao", "nem:OSError", "ca:OSError"],
            "runner_nem": ["vao", "nem:KeyError", "ca:KeyError"], "script_la": ["vao", "la:0", "ca:dat"], "ngoai": ["ca:dat"],
            "khong_sd": ["vao", "so", "ca:dat"]}
    return [] if vet == mong and sorted(ghi) == ["gian_tiep", "khong_sd", "thang"] else [f"tự kiểm phép đếm: vết {vet} ≠ {mong}"]


def lenh_ab(manh=(0, 1)):
    base = git("merge-base", "HEAD", "refs/remotes/origin/master").decode().strip()
    loi = tu_kiem_bo_so()
    with tempfile.TemporaryDirectory(prefix="b4ab-") as td:
        td = Path(td)
        loi += tu_kiem_dem(td)
        for ve, lay in (("base", lambda p: git("show", f"{base}:.claude/dev/{p}")), ("head", lambda p: (DEV / p).read_bytes())):
            (td / ve).mkdir()
            for p in ("packet_loop.py", "launcher.py", "packet_loop_test.py"):
                (td / ve / p).write_bytes(lay(p))
        Tb, Th = nap("plt_base", td / "base/packet_loop_test.py"), nap("plt_head", td / "head/packet_loop_test.py")
        for T in (Tb, Th):   # như vòng đột biến của chính bộ test: fixture canonical đọc từ kho thật, `__file__` vẫn là bản sao
            T.HERE, T.ROOT = DEV, ROOT
        nen, vet = do_ca(Tb, [td / "base/packet_loop.py"], td, quan_the(Tb, manh))   # ĐẾM: cả sổ ca của base (lát `manh`), không lọc trước
        vao = {t for t, v in vet.items() if "vao" in v}
        ghi, vh = {}, {}
        for hinh, sua in (("moi", None), ("cu", lambda h, *a, **k: [])):
            goc = Th._b4_manh
            Th._b4_manh = sua or goc
            try:
                ghi[hinh], vh[hinh] = do_ca(Th, [td / "base/packet_loop.py", td / "head/packet_loop.py"], td, vao)
            finally:
                Th._b4_manh = goc
    bo = lambda v: [x for x in v if not x.startswith("ca:")]  # noqa: E731
    loi += [f"quần thể: {t} vết head (hình dạng mới) {vh['moi'].get(t)} ≠ vết base {vet[t]}" for t in sorted(vao) if vh["moi"].get(t) != vet[t]]
    loi += [f"quần thể: {t} vết head (hình dạng cũ) {vh['cu'].get(t)} ≠ vết base {vet[t]} (không kể kết cục ca)" for t in sorted(vao) if bo(vh["cu"].get(t, [])) != bo(vet[t])]
    loi += [f"tiêu chí 1: thiếu ca {t} (base có {len(nen[t])} lời kiem-merge)" for h in ghi for t in nen if len(ghi[h].get(t, [])) != len(nen[t])]
    loi += [f"tiêu chí 1 (hình dạng mới, B-2): {t} lời {i} lệch byte: rc {b[0]}/{h[0]}" for t, ds in ghi["moi"].items() for i, (b, h) in enumerate(ds) if b != h]
    lop = {}
    for t, ds in ghi["cu"].items():
        for i, (b, h) in enumerate(ds):
            k, e = so(b, h)
            lop.setdefault(k, []).append(t)
            loi += [f"tiêu chí 2: {t} lời {i} lớp ({k}): {e}"] * bool(e)
    z = sorted(set(lop.get("z", [])))
    loi += [f"tiêu chí 2: ca {t} phải thuộc lớp (z)" for t in ("cong_c_k1_anchor", "cong_c_k1_yaml_hong", "cong_c_k1_khoa_trung", "cong_c_k1_tag_hong") if t not in z and (manh[1] == 1 or t in vao)]
    rieng = {t: vet[t] for t in sorted(vao) if set(vet[t]) - {"vao", "so", "ca:dat"}}   # ca có lần vào KHÔNG cho lời so được, hoặc kết cục không phải đạt
    kc = {}
    for v in vet.values():
        kc[v[-1]] = kc.get(v[-1], 0) + 1
    print(f"base {base} · lát {manh[0]}/{manh[1]}\nsổ ca của base đã chạy có máy đếm: {len(vet)} · kết cục: {dict(sorted(kc.items()))}"
          f"\nca base kết cục không phải đạt/BoQua (vết): {sorted((t, ' '.join(v)) for t, v in vet.items() if v[-1] not in ('ca:dat', 'ca:BoQua'))}")
    print(f"ca VÀO _c1106 tại base: {len(vao)} = {len(vao) - len(rieng)} ca thường (mọi lần vào đều cho lời so được, ca đạt) + {len(rieng)} ca riêng · lần vào: {sum(v.count('vao') for v in vet.values())}"
          f" · lời kiem-merge so được: {sum(map(len, nen.values()))} · ở head: moi {len(ghi['moi'])} ca · cu {len(ghi['cu'])} ca")
    print("ca riêng (vết tại base; head hình dạng mới phải trùng vết):\n" + "\n".join(f"  {t}: {' '.join(v)}" for t, v in rieng.items()))
    print("tiêu chí 2 — số lời theo lớp: " + " · ".join(f"({k}) {len(v)}" for k, v in sorted(lop.items())) + f"\nlớp (z): {z}\ntên ca vào _c1106: {sorted(vao)}")
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
