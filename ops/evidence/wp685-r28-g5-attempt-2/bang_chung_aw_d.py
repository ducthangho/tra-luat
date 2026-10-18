"""wp685 r28 g5 attempt 2 — tập lệnh bằng chứng cục bộ: A1/A2/W1/W0 cho 54 dòng DOT_BIEN mới (B5) và phép D (B5 (D)).
Dùng: python3.1x -B bang_chung_aw_d.py <thư mục .claude/dev của ứng viên> <thư mục tạm> [aw|d|all] <đặc tả r28> [<bảng D .json>]
In mỗi dòng một kết quả; dòng cuối KET LUAN. rc=0 chỉ khi mọi dòng đạt.
Attempt 2 (VERDICT lượt 1, lớp D65-control-catalog-not-validated) đổi phần D, phần A/W giữ nguyên từng dòng:
  * danh mục 65 khoá `nhan:<nhãn>` / `tieu:<nhãn>/<tiểu nhãn>` TRÍCH BẰNG MÁY từ đặc tả (đúng sha256) và phải BẰNG
    bảng viết cứng ở đây; bảng control phải có ĐÚNG một dòng cho mỗi khoá — thiếu, thừa hay lặp dòng ⇒ ĐỎ trước khi
    chạy control nào (§7 B5 (D).6);
  * đối chiếu quan sát là phép BẰNG tập: thiếu VÀ thừa đơn vị (kể cả nhãn lạ, tiểu nhãn lạ) đều ĐỎ (§7 B5 (D).3);
    lặp quan sát của CÙNG một đơn vị hợp lệ vẫn được (một đơn vị có nhiều assertion);
  * control đạt khi tập thiếu BẰNG đúng tập kỳ vọng của khoá đó VÀ không có đơn vị thừa;
  * biến môi trường D_PHAN_CHUNG chỉ dùng cho phản chứng (phan_chung_d.py) — bơm lỗi vào bảng control hay vào
    quan sát; mặc định rỗng."""
import hashlib
import importlib.util
import os
import re
import json
import sys
from pathlib import Path

DEV = Path(sys.argv[1]).resolve()
TAM = Path(sys.argv[2]).resolve()
CHE_DO = sys.argv[3] if len(sys.argv) > 3 else "all"
SPEC = Path(sys.argv[4]).resolve() if len(sys.argv) > 4 else None
RA_D = Path(sys.argv[5]).resolve() if len(sys.argv) > 5 else TAM / "bang_D.json"
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


SPEC_SHA = "8007edf4e00aaefc298bf299bf19be9a71c54e73ff6a1610eb676a806773e156"
NHAN17 = NHAN156 + ["B3b-giet-cay"]
KHOA_CUNG = [f"nhan:{n}" for n in NHAN17] + [f"tieu:{n}/{t}" for n, ds in TIEU.items() for t in ds]
CAP_DAO = [("B1", "B2-eacces"), ("B2-thoat-parse", "B2-exception"), ("B2-pid-du-phong", "B3-song"),
           ("B2-dem-doc", "B2-pid-du-phong"), ("B2-eperm-hoi", "B2-doc-hong"), ("B2-pid-du-phong", "B2-nhanh-cu")]
PHAN_CHUNG = os.environ.get("D_PHAN_CHUNG", "")


def khoa_tu_dac_ta(spec):
    """65 khoá trích bằng máy từ 'Bảng tiểu nhãn' của đặc tả: nhãn có tiểu nhãn từ các hàng bảng, nhãn không tiểu nhãn
    từ câu 'Nhãn không liệt kê ở đây (...)'. Trả (tập nhãn, dict tiểu nhãn theo thứ tự)."""
    b = spec.read_bytes()
    if hashlib.sha256(b).hexdigest() != SPEC_SHA:
        raise SystemExit(f"DAC TA SAI BAM {hashlib.sha256(b).hexdigest()}")
    s = b.decode("utf-8")
    i = s.index("**Bảng tiểu nhãn")
    j = s.index("Tổng: 16 nhãn", i)
    doan = s[i:j]
    k = doan.index("Nhãn không liệt kê ở đây (")
    ngoac = doan[k:doan.index(") không có tiểu nhãn", k)]
    khong_tieu = re.findall(r"`([^`]+)`", ngoac)
    khong_tieu = [x for x in khong_tieu if not x.endswith("...")]
    tieu = {}
    for dong in doan.splitlines():
        m = re.match(r"\s*\| `([^`]+)`(?: \(r\d+\))? \| (.+?) \| (\d+) \|\s*$", dong)
        if m:
            ds = re.findall(r"`([^`]+)`", m.group(2))
            assert len(ds) == int(m.group(3)), (m.group(1), len(ds), m.group(3))
            tieu[m.group(1)] = ds
    return khong_tieu, tieu


def kiem_danh_muc(spec, bang_ctrl_khoa):
    """Lỗi danh mục (list chuỗi). Rỗng ⇔ hard-code = đặc tả VÀ bảng control có đúng một dòng mỗi khoá."""
    loi = []
    khong_tieu, tieu = khoa_tu_dac_ta(spec)
    if tieu != TIEU:
        loi.append(f"TIEU viet cung lech dac ta: {tieu}")
    if sorted(khong_tieu + list(tieu)) != sorted(NHAN17):
        loi.append(f"17 nhan lech dac ta: khong_tieu={khong_tieu} co_tieu={list(tieu)}")
    khoa_dt = [f"nhan:{n}" for n in NHAN17] + [f"tieu:{n}/{t}" for n, ds in tieu.items() for t in ds]
    if len(khoa_dt) != 65 or len(set(khoa_dt)) != 65 or khoa_dt != KHOA_CUNG:
        loi.append(f"65 khoa dac ta lech viet cung: {len(khoa_dt)}/{len(set(khoa_dt))}")
    don_vi = DON_VI_156 + DON_VI_157
    if len(don_vi) != 57 or len(set(don_vi)) != 57:
        loi.append("57 don vi khong duy nhat")
    dem = {}
    for k in bang_ctrl_khoa:
        dem[k] = dem.get(k, 0) + 1
    lap = sorted(k for k, c in dem.items() if c > 1)
    thieu = sorted(set(khoa_dt) - set(dem))
    thua = sorted(set(dem) - set(khoa_dt))
    if lap or thieu or thua or len(bang_ctrl_khoa) != 65:
        loi.append(f"BANG CONTROL: so dong={len(bang_ctrl_khoa)} so khoa={len(dem)} lap={lap} thieu={thieu} thua={thua}")
    return loi


def tach_khoa(khoa):
    """Khoá ⇒ (đổi, nhãn, tiểu nhãn). Phép đổi DẪN XUẤT từ khoá, nên khoá và thứ bị đổi không lệch nhau được."""
    if khoa.startswith("nhan:"):
        return "noi", khoa[5:], None
    if khoa.startswith("tieu:"):
        n, _, t = khoa[5:].partition("/")
        return "bo", n, t
    raise ValueError(khoa)


def quan_sat(m):
    ghi = {T156: [], T157: []}
    cur = [None]
    g = m.bang
    da_bom = [False]

    def bang_ghi(dk, td):
        n, t, _lo = tach(td)
        ghi[cur[0]].append((n, t) if n is not None else ("?", td[:60]))
        if PHAN_CHUNG.startswith("quan_sat") and not da_bom[0]:
            da_bom[0] = True  # phản chứng: MỘT lời gọi bang ĐÚNG thêm, ngoài 57 đơn vị, đi qua chính observer
            m.bang(True, {"quan_sat_tieu_la": "B2-parse p9 ngoai spec", "quan_sat_nhan_la": "B9-la ngoai spec",
                          "quan_sat_tieu_thieu": "B2-doc-hong"}[PHAN_CHUNG])
        return g(dk, td)
    m.bang = bang_ghi
    loi = {}
    try:
        for ca in (T156, T157):
            cur[0] = ca
            r = chay(getattr(m, ca))
            if r[0] != "song":
                loi[ca] = r
    finally:
        m.bang = g
    return ghi, loi


def doi_chieu(ghi):
    """(thiếu, thừa, sai thứ tự). Tập đơn vị quan sát (khử lặp, giữ lần đầu) phải BẰNG tập kỳ vọng của từng ca."""
    thieu, thua, sai_thu_tu = [], [], False
    for ca, ky in ((T156, DON_VI_156), (T157, DON_VI_157)):
        dau = []
        for x in ghi[ca]:
            if x not in dau:
                dau.append(x)
        thieu += [x for x in ky if x not in dau]
        thua += [x for x in dau if x not in ky]
        if [x for x in dau if x in ky] != [x for x in ky if x in dau]:
            sai_thu_tu = True
    return thieu, thua, sai_thu_tu


def d():
    hong = 0
    bang_ctrl = [{"khoa": k} for k in KHOA_CUNG]
    if PHAN_CHUNG == "lap":
        bang_ctrl[-1] = dict(bang_ctrl[0])  # phản chứng reviewer: 65 dòng, 64 khoá
    elif PHAN_CHUNG == "thua":
        bang_ctrl.append({"khoa": "tieu:B2-parse/p9"})
    elif PHAN_CHUNG == "thua_trung":
        bang_ctrl.append(dict(bang_ctrl[0]))
    elif PHAN_CHUNG == "thieu":
        bang_ctrl.pop()
    elif PHAN_CHUNG == "khoa_cu":
        bang_ctrl = [{"khoa": ("noi_mac_dinh:" + k[5:]) if k.startswith("nhan:") else k} for k in KHOA_CUNG]
    loi_dm = kiem_danh_muc(SPEC, [r["khoa"] for r in bang_ctrl])
    ket = {"spec_sha256": SPEC_SHA, "phan_chung": PHAN_CHUNG, "khoa_65": KHOA_CUNG,
           "don_vi_57": [list(x) for x in DON_VI_156 + DON_VI_157], "cap_dao_6": [list(x) for x in CAP_DAO],
           "loi_danh_muc": loi_dm}
    if loi_dm:
        for x in loi_dm:
            print(f"D DANH MUC DO: {x}", flush=True)
        ket["ket_luan"] = "DO"
        RA_D.write_text(json.dumps(ket, ensure_ascii=False, indent=1), encoding="utf-8")
        print("TONG D: DANH MUC DO — khong chay control nao", flush=True)
        return 1
    print(f"D danh muc: 65 khoa = dac ta (trich bang may) = viet cung; bang control 65 dong / 65 khoa, 0 lap/thieu/thua",
          flush=True)
    m = nap()
    ghi, loi = quan_sat(m)
    thieu, thua, sai = doi_chieu(ghi)
    ok = not thieu and not thua and not sai and not loi
    so_156 = len({x for x in ghi[T156]})
    so_157 = len({x for x in ghi[T157]})
    print(f"D ban dung: {'XANH' if ok else 'DO'} t156={so_156} don vi t157={so_157} thieu={thieu} thua={thua} "
          f"order_sai={sai} loi={loi}", flush=True)
    ket["ban_dung"] = {"xanh": ok, "t156": so_156, "t157": so_157, "thieu": thieu, "thua": thua, "order_sai": sai,
                       "loi": {k: list(v) for k, v in loi.items()}}
    hong += not ok
    ket["controls"] = []
    for r in bang_ctrl:
        loai, n, t = tach_khoa(r["khoa"])
        m = nap()
        if loai == "noi":
            if n == "B3b-giet-cay":
                m._cs_chay_t157.__defaults__ = (None, (n,))
            else:
                m._cs_chay_t156.__defaults__ = (None, (n,))
            ky_vong = [(x, y) for (x, y) in DON_VI_156 + DON_VI_157 if x == n]
            doi = f"them nhan {n} vao tap NOI mac dinh cua helper"
        else:
            g_kiem = m._CsNhan.kiem

            def kiem_bo(self, dk, tieu, lo, _g=g_kiem, _n=n, _t=t):
                if self.nhan == _n and tieu == _t:
                    return None
                return _g(self, dk, tieu, lo)
            m._CsNhan.kiem = kiem_bo
            ky_vong = [(n, t)]
            doi = f"bo assertion cua dau vao {n} {t} (giu cac dau vao khac cung nhan)"
        ghi, loi = quan_sat(m)
        thieu, thua, sai = doi_chieu(ghi)
        dat = bool(thieu) and sorted(map(str, thieu)) == sorted(map(str, ky_vong)) and not thua
        hong += not dat
        dong = {"khoa": r["khoa"], "doi": doi, "thieu_ky_vong": ky_vong, "thieu_do": thieu, "thua_do": thua,
                "dat": dat}
        ket["controls"].append(dong)
        print(json.dumps(dong, ensure_ascii=False), flush=True)
    ket["dao"] = []
    for a, b in CAP_DAO:
        m = nap()
        t = list(m.CS_NHAN_T156)
        i, j = t.index(a), t.index(b)
        t[i], t[j] = t[j], t[i]
        m.CS_NHAN_T156 = tuple(t)
        ghi, loi = quan_sat(m)
        thieu, thua, sai = doi_chieu(ghi)
        dat = sai and not thieu and not thua
        hong += not dat
        ket["dao"].append({"cap": [a, b], "missing": thieu, "thua": thua, "order_dung": not sai, "dat": dat})
        print(f"DAO {a}<->{b}: missing={thieu} thua={thua} order={not sai} {'DO dung' if dat else 'KHONG DO'}",
              flush=True)
    n_dat = sum(c["dat"] for c in ket["controls"])
    ket["ket_luan"] = "DAT" if hong == 0 else "DO"
    RA_D.write_text(json.dumps(ket, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"TONG D: control {n_dat}/65 do dung; dao {sum(x['dat'] for x in ket['dao'])}/6; hong={hong}; bang={RA_D}",
          flush=True)
    return hong


if __name__ == "__main__":
    h = 0
    if CHE_DO in ("d", "all"):
        if SPEC is None:
            raise SystemExit("D can duong dan dac ta r28 (doi so 4)")
        h += d()
    if CHE_DO in ("aw", "all"):
        h += aw()
    print(f"KET LUAN: {'DAT' if h == 0 else 'DO'} hong={h}")
    sys.exit(1 if h else 0)
