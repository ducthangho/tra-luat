"""wp685 r28 — tập lệnh bằng chứng cục bộ: A1/A2/W1/W0 cho 54 dòng DOT_BIEN mới (B5) và phép D (B5 (D)).
Dùng: python3.1x -B bang_chung_aw_d.py <thư mục .claude/dev của ứng viên> <thư mục tạm> [aw|d|all]
In mỗi dòng một kết quả; dòng cuối TONG. rc=0 chỉ khi mọi dòng đạt."""
import importlib.util
import json
import sys
from pathlib import Path

DEV = Path(sys.argv[1]).resolve()
TAM = Path(sys.argv[2]).resolve()
CHE_DO = sys.argv[3] if len(sys.argv) > 3 else "all"
TAM.mkdir(parents=True, exist_ok=True)
sys.dont_write_bytecode = True

T156 = "t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan"
T157 = "t157_giet_cay_khi_stat_EACCES_van_tron_ven"
NHAN156 = ["B1", "B2-eacces", "B2-eio", "B2-eperm-hoi", "B2-doc-hong", "B2-tin-hieu", "B2-dem-lan", "B2-exception",
           "B2-thoat-parse", "B2-parse", "B2-dem-doc", "B2-pid-du-phong", "B2-nhanh-cu", "B3-song", "B3-da-wait",
           "B3-zombie"]
TIEU = {  # bảng tiểu nhãn §7 B2 — viết CỨNG, không lấy từ helper
    "B2-doc-hong": ["EACCES", "EIO", "ESRCH", "EPERM"],
    "B2-tin-hieu": ["hoi", "doc", "kill"],
    "B2-exception": ["hoi", "doc", "kill"],
    "B2-thoat-parse": ["hoi-index", "hoi-value", "hoi-decode", "kill-index", "kill-value", "kill-decode"],
    "B2-parse": ["p1", "p2", "p3", "p4"],
    "B2-dem-doc": ["1", "2", "3", "4"],
    "B2-pid-du-phong": ["song", "da-wait", "eperm", "eio"],
    "B2-nhanh-cu": ["song", "EACCES", "EIO", "ESRCH", "EPERM", "p1", "p3", "p4", "utf8-hong-that", "tin-hieu",
                    "exception", "vang", "vang-da-wait", "vang-eperm", "vang-eio", "vang-tin-hieu", "vang-exception",
                    "vang-index", "vang-value", "vang-decode"],
}
DON_VI_156 = [(n, t) for n in NHAN156 for t in (TIEU.get(n) or [None])]
DON_VI_157 = [("B3b-giet-cay", None)]
assert len(DON_VI_156) + len(DON_VI_157) == 57

# dòng → (ca đích, nhãn, tiểu nhãn hay None, loại hay None) — B5 (a)–(m); loại chỉ khi dòng nêu
DICH = {
    "a": [(T156, "B1", None, None)], "b": [(T156, "B2-eacces", None, None)],
    "c": [(T156, "B3-zombie", None, None), (T157, "B3b-giet-cay", None, None)],
    "d1": [(T156, "B2-eio", None, None)], "d2": [(T156, "B2-doc-hong", "EIO", None)],
    "e1": [(T156, "B2-tin-hieu", "hoi", None)], "e2": [(T156, "B2-tin-hieu", "doc", None)],
    "f": [(T156, "B2-dem-lan", None, None)],
    "g1": [(T156, "B2-doc-hong", "EACCES", None)], "g2": [(T156, "B2-doc-hong", "ESRCH", None)],
    "h1": [(T156, "B2-exception", "hoi", None)], "h2": [(T156, "B2-exception", "doc", None)],
    "i": [(T156, "B2-parse", "p1", None)],
    "j1": [(T156, "B2-dem-doc", "1", None)], "j2": [(T156, "B2-dem-doc", "3", None)],
    "k1": [(T156, "B2-pid-du-phong", "song", None)], "k2": [(T156, "B2-pid-du-phong", "da-wait", None)],
    "k3": [(T156, "B2-pid-du-phong", "eperm", None)], "k4": [(T156, "B2-pid-du-phong", "eio", None)],
    "k5": [(T156, "B2-pid-du-phong", "song", "kill count")],
    "l1": [(T156, "B2-eacces", None, "seam escaped")], "l2": [(T156, "B1", None, "result True")],
    "l3": [(T156, "B2-eio", None, "result False")], "l4": [(T156, "B2-eperm-hoi", None, "seam escaped")],
    "l5": [(T156, "B2-eperm-hoi", None, "result False")],
    "l6": [(T156, "B2-thoat-parse", "hoi-index", "sentinel identity")],
    "l7": [(T156, "B2-thoat-parse", "hoi-value", "sentinel identity")],
    "l8": [(T156, "B2-thoat-parse", "hoi-decode", "sentinel identity")],
    "l9": [(T156, "B2-exception", "hoi", "seam wrapped")],
    "l10": [(T156, "B2-doc-hong", "EACCES", "seam escaped")], "l11": [(T156, "B2-doc-hong", "ESRCH", "seam escaped")],
    "l12": [(T156, "B2-doc-hong", "EPERM", "seam escaped")], "l13": [(T156, "B2-doc-hong", "EPERM", "result False")],
    "l14": [(T156, "B2-doc-hong", "EIO", "result False")],
    "l15": [(T156, "B2-parse", "p1", "parse error escaped")], "l16": [(T156, "B2-parse", "p2", "parse error escaped")],
    "l17": [(T156, "B2-parse", "p3", "parse error escaped")], "l18": [(T156, "B2-parse", "p3", "result False")],
    "l19": [(T156, "B2-parse", "p4", "seam escaped")], "l20": [(T156, "B2-parse", "p4", "result False")],
    "l21": [(T156, "B2-parse", "p1", "parse error wrapped")],
    "l22": [(T156, "B2-pid-du-phong", "da-wait", "seam escaped")],
    "l23": [(T156, "B2-pid-du-phong", "eperm", "seam escaped")],
    "l24": [(T156, "B2-pid-du-phong", "eio", "seam escaped")],
    "l25": [(T156, "B2-tin-hieu", "kill", "sentinel identity")],
    "l26": [(T156, "B2-exception", "kill", "sentinel identity")],
    "l27": [(T156, "B2-thoat-parse", "kill-index", "sentinel identity")],
    "l28": [(T156, "B2-thoat-parse", "kill-value", "sentinel identity")],
    "l29": [(T156, "B2-thoat-parse", "kill-decode", "sentinel identity")],
    "m1": [(T156, "B2-nhanh-cu", "EACCES", "result True")],
    "m2": [(T156, "B2-nhanh-cu", "tin-hieu", "sentinel identity")],
    "m3": [(T156, "B2-nhanh-cu", "vang", "result False")], "m4": [(T156, "B1", None, "stat count")],
    "m5": [(T156, "B3-zombie", None, "result True")],
}
assert len(DICH) == 54 and sum(len(v) for v in DICH.values()) == 55
_dem = [0]


def nap(launcher_path=None, test_src=None):
    _dem[0] += 1
    tp = TAM / f"lt_{_dem[0]:04d}.py"
    tp.write_text(test_src or (DEV / "launcher_test.py").read_text(encoding="utf-8"), encoding="utf-8")
    # tệp test tra LAUNCHER theo thư mục của chính nó: trỏ thẳng biến toàn cục sau khi nạp
    sp = importlib.util.spec_from_file_location(f"lt_{_dem[0]}", tp)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    m.LAUNCHER_DANG_DUNG = Path(launcher_path or (DEV / "launcher.py"))
    return m


def tach(msg):
    for n in sorted(NHAN156 + ["B3b-giet-cay"], key=len, reverse=True):
        if msg == n or msg.startswith(n + " "):
            con = msg[len(n):].strip()
            t = None
            if n in TIEU:
                for x in sorted(TIEU[n], key=len, reverse=True):
                    if con == x or con.startswith(x + " "):
                        t, con = x, con[len(x):].strip()
                        break
            return n, t, con
    return None, None, msg


def chay(fn):
    """('song', None) | ('TH', msg) | ('VO_CAN', 'Kieu: msg')."""
    try:
        fn()
        return ("song", "")
    except BaseException as e:  # noqa: BLE001
        if type(e).__name__ == "TinHieuChotCa":
            return ("TH", str(e))
        return ("VO_CAN", f"{type(e).__name__}: {str(e)[:120]}")


def aw():
    goc = (DEV / "launcher.py").read_text(encoding="utf-8")
    m0 = nap()
    muc = [x for x in m0.DOT_BIEN if x[0].startswith("wp685_")]
    assert len(muc) == 54, len(muc)
    hong = 0
    for i, (ten, cap, dich) in enumerate(muc):
        dong = ten.split("_")[1]
        old, new = cap
        lp = TAM / f"launcher_mut_{i:02d}.py"
        lp.write_text(goc.replace(old, new, 1), encoding="utf-8")
        for ca_dich, nhan, tieu, loai in DICH[dong]:
            assert ca_dich in dich
            m = nap(lp)
            ham = getattr(m, ca_dich)
            helper = m._cs_chay_t156 if ca_dich == T156 else m._cs_chay_t157
            thu_tu = NHAN156 if ca_dich == T156 else ["B3b-giet-cay"]
            a1 = chay(ham)
            a2 = chay(lambda: helper(m._tai_launcher_thu(), noi=[nhan]))
            w1 = chay(lambda: helper(m._tai_launcher_thu(), chay=[nhan]))
            tong_cham = [0]
            g_exit = m._CsSeam.__exit__

            def dem_exit(self, *a, _g=g_exit):
                tong_cham[0] += self.n_stat + self.n_exists + self.n_doc + self.n_kill
                return _g(self, *a)
            m._CsSeam.__exit__ = dem_exit
            w0 = chay(lambda: helper(m._tai_launcher_thu(), chay=[nhan], noi=[nhan]))
            m._CsSeam.__exit__ = g_exit
            ly_do = []
            # A1
            if a1[0] != "TH":
                ly_do.append(f"A1 {a1[0]}")
            else:
                n, t, lo = tach(a1[1])
                if n is None or thu_tu.index(n) > thu_tu.index(nhan):
                    ly_do.append("A1 nhan sau nhan dich")
                elif n == nhan:
                    if tieu and t != tieu:
                        ly_do.append(f"A1 tieu nhan {t}")
                    if loai and not lo.startswith(loai):
                        ly_do.append(f"A1 loai {lo[:30]}")
            # W1
            if w1[0] != "TH":
                ly_do.append(f"W1 {w1[0]}")
            else:
                n, t, lo = tach(w1[1])
                if n != nhan or (tieu and t != tieu) or (loai and not lo.startswith(loai)):
                    ly_do.append(f"W1 lech {n}/{t}/{lo[:30]}")
            hang = "DAT"
            if w0[0] != "song" or tong_cham[0] < 1:
                hang = "CHUA CO CHOT NGUOC" if not ly_do else "DO"
            if ly_do:
                hang = "DO"
            if hang != "DAT":
                hong += 1
            print(json.dumps({"dong": dong, "ten": ten, "ca": ca_dich, "dich": [nhan, tieu, loai], "hang": hang,
                              "A1": a1, "A2": a2, "W1": w1, "W0": w0, "W0_cham": tong_cham[0], "ly_do": ly_do},
                             ensure_ascii=False), flush=True)
    print(f"TONG A/W: {55 - hong}/55 cap dat")
    return hong


def quan_sat(m):
    ghi = {T156: [], T157: []}
    cur = [None]
    g = m.bang

    def bang_ghi(dk, td):
        n, t, _lo = tach(td)
        ghi[cur[0]].append((n, t))
        return g(dk, td)
    m.bang = bang_ghi
    loi = {}
    for ca in (T156, T157):
        cur[0] = ca
        r = chay(getattr(m, ca))
        if r[0] != "song":
            loi[ca] = r
    m.bang = g
    return ghi, loi


def doi_chieu(ghi):
    thieu, sai_thu_tu = [], False
    for ca, ky in ((T156, DON_VI_156), (T157, DON_VI_157)):
        dau = []
        for x in ghi[ca]:
            if x not in dau:
                dau.append(x)
        thieu += [x for x in ky if x not in dau]
        if [x for x in dau if x in ky] != [x for x in ky if x in dau]:
            sai_thu_tu = True
    return thieu, sai_thu_tu


def d():
    hong = 0
    m = nap()
    ghi, loi = quan_sat(m)
    thieu, sai = doi_chieu(ghi)
    ok = not thieu and not sai and not loi
    print(f"D ban dung: {'XANH' if ok else 'DO'} thieu={thieu} order_sai={sai} loi={loi}")
    hong += not ok
    controls = []
    for n in NHAN156 + ["B3b-giet-cay"]:
        controls.append((f"noi_mac_dinh:{n}", "noi", n, None))
    for n, ds in TIEU.items():
        for t in ds:
            controls.append((f"bo_tieu_nhan:{n} {t}", "bo", n, t))
    controls[-1] = controls[0]  # reviewer: one duplicate key, one missing control; count stays 65
    assert len(controls) == 65
    bang_ctrl = []
    for khoa, loai, n, t in controls:
        m = nap()
        if loai == "noi":
            if n == "B3b-giet-cay":
                m._cs_chay_t157.__defaults__ = (None, (n,))
            else:
                m._cs_chay_t156.__defaults__ = (None, (n,))
            ky_vong = [(x, y) for (x, y) in DON_VI_156 + DON_VI_157 if x == n]
        else:
            g_kiem = m._CsNhan.kiem

            def kiem_bo(self, dk, tieu, lo, _g=g_kiem, _n=n, _t=t):
                if self.nhan == _n and tieu == _t:
                    return None
                return _g(self, dk, tieu, lo)
            m._CsNhan.kiem = kiem_bo
            ky_vong = [(n, t)]
        ghi, loi = quan_sat(m)
        thieu, sai = doi_chieu(ghi)
        dat = bool(thieu) and sorted(map(str, thieu)) == sorted(map(str, ky_vong))
        hong += not dat
        bang_ctrl.append({"khoa": khoa, "doi": loai, "thieu_ky_vong": ky_vong, "thieu_do": thieu, "dat": dat})
        print(json.dumps(bang_ctrl[-1], ensure_ascii=False), flush=True)
    for a, b in (("B1", "B2-eacces"), ("B2-thoat-parse", "B2-exception"), ("B2-pid-du-phong", "B3-song"),
                 ("B2-dem-doc", "B2-pid-du-phong"), ("B2-eperm-hoi", "B2-doc-hong"), ("B2-pid-du-phong", "B2-nhanh-cu")):
        m = nap()
        t = list(m.CS_NHAN_T156)
        i, j = t.index(a), t.index(b)
        t[i], t[j] = t[j], t[i]
        m.CS_NHAN_T156 = tuple(t)
        ghi, loi = quan_sat(m)
        thieu, sai = doi_chieu(ghi)
        dat = sai and not thieu
        hong += not dat
        print(f"DAO {a}<->{b}: missing={thieu} order={not sai} {'DO dung' if dat else 'KHONG DO'}", flush=True)
    print(f"TONG D: control {sum(c['dat'] for c in bang_ctrl)}/65 do dung; hong={hong}")
    return hong


if __name__ == "__main__":
    h = 0
    if CHE_DO in ("d", "all"):
        h += d()
    if CHE_DO in ("aw", "all"):
        h += aw()
    print(f"KET LUAN: {'DAT' if h == 0 else 'DO'} hong={h}")
    sys.exit(1 if h else 0)
