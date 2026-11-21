# -*- coding: utf-8 -*-
"""Rig N4 (SECRETS-SET-BUNDLE-KIEU r5 §4): mỗi mục của ma trận chạy trong một TIẾN TRÌNH MỚI trên nguồn đã áp đột biến (trong bộ nhớ;
cây không bị sửa). Tiến trình con gọi `run(tl, nguon)` của fragment với `WP433_SS_BAN_DO` trỏ tệp riêng; cha chỉ đọc bản đồ đó.
  python rig_n4.py <cay_ung_vien> <ma-tran-n4.json> <thu_muc_ra> <tl_gws_base.py>
Phân hạng: HONG (neo ≠ 1 lần) · TIN_DUNG_GIA (văng / con rc≠0 / thiếu-thừa khoá / run() không khớp bản đồ / sai cơ chế) ·
SONG_SOT (mọi khoá True) · LECH_TAP (tập False ≠ tập khai) · GIET."""
import json, os, pathlib, subprocess, sys, time, types
FRAG = "scripts/test_fragments/wp433_secrets_set_bundle.py"
def ap(src, cap):
    for neo, thay in cap:
        if src.count(neo) != 1 or neo == thay:
            return None
        src = src.replace(neo, thay)
    return src
def con(cay, ma_tran, ten, ra, base):
    e = next(x for x in json.load(open(ma_tran, encoding="utf-8"))["dot_bien"] if x["ten"] == ten)
    out = pathlib.Path(ra) / (ten + ".ket_qua.json")
    sys.path.insert(0, os.path.join(cay, "scripts"))
    import tl
    fsrc = ap(pathlib.Path(cay, FRAG).read_text(encoding="utf-8"), e["cap_fragment"])
    goc = tl._imp("tl_gws"); goc.bind(tl)  # noqa: E702
    gsrc = pathlib.Path(base if e["nguon"] == "base" else goc.__file__).read_text(encoding="utf-8")
    gsrc = ap(gsrc, e["cap"])
    if fsrc is None or gsrc is None:
        out.write_text(json.dumps({"hong": True}), encoding="utf-8"); return  # noqa: E702
    f = types.ModuleType("wp433ss_frag"); f.__file__ = os.path.join(cay, FRAG)  # noqa: E702
    exec(compile(fsrc, f.__file__, "exec"), f.__dict__)
    os.environ["WP433_SS_BAN_DO"] = str(pathlib.Path(ra) / (ten + ".ban_do.json"))
    kq = {"hong": False, "run": None, "ngoai_le": None, "co_che": None, "danh_muc": sorted(f._DANH_MUC), "pid": os.getpid(),
          "tl_gws_file": goc.__file__}
    try:
        kq["run"] = f.run(tl, gsrc)
    except BaseException as x:  # noqa: BLE001
        kq["ngoai_le"] = type(x).__name__
    if e["co_che_luot"]:
        try:
            store = tl._imp("gws_cred_store"); m = f._nap(gsrc, tl, goc, store)  # noqa: E702
            _c, kt, ct = e["co_che_luot"].split(".")
            kq["co_che"] = f._dung_co_che(f._Rig(m, store, {}).luot(e["co_che_luot"], dict(f._KIEU)[kt], f._CO[ct]))
        except BaseException as x:  # noqa: BLE001
            kq["co_che"], kq["co_che_ngoai_le"] = False, type(x).__name__
    out.write_text(json.dumps(kq, ensure_ascii=False), encoding="utf-8")
def hang(e, kq, bd, danh_muc):
    if kq is None:
        return "TIN_DUNG_GIA", "con không ghi kết quả"
    if kq.get("hong"):
        return "HONG", "neo không khớp đúng một lần"
    if kq["ngoai_le"]:
        return "TIN_DUNG_GIA", "văng " + kq["ngoai_le"]
    if set(kq["danh_muc"]) != danh_muc:
        return "TIN_DUNG_GIA", "danh mục fragment ≠ danh mục ma trận"
    if bd is None or set(bd) != danh_muc:
        return "TIN_DUNG_GIA", "bản đồ thiếu/thừa khoá: thiếu %d thừa %d" % (len(danh_muc - set(bd or {})), len(set(bd or {}) - danh_muc))
    sai = {k for k, v in bd.items() if v is not True}
    if kq["run"] is not (not sai):
        return "TIN_DUNG_GIA", "run() = %r không khớp bản đồ (%d khoá False)" % (kq["run"], len(sai))
    if not sai:
        return "SONG_SOT", "mọi khoá True"
    if sai != set(e["dich"]):
        return "LECH_TAP", "False ngoài khai %d, khai mà True %d" % (len(sai - set(e["dich"])), len(set(e["dich"]) - sai))
    if e["co_che_luot"] and kq["co_che"] is not True:
        return "TIN_DUNG_GIA", "sai cơ chế ở " + e["co_che_luot"]
    return "GIET", "%d khoá False == tập khai" % len(sai)
def cha(cay, ma_tran, ra, base):
    mt = json.load(open(ma_tran, encoding="utf-8"))
    danh_muc, ket, phu, pids = set(mt["danh_muc"]), [], set(), set()
    pathlib.Path(ra).mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    env.pop("WP433_SS_BAN_DO", None)
    for e in mt["dot_bien"]:
        t0 = time.time()
        p = subprocess.run([sys.executable, "-B", __file__, "--con", cay, ma_tran, e["ten"], ra, base], env=env, capture_output=True, text=True,
                           timeout=900)
        fk, fb = pathlib.Path(ra) / (e["ten"] + ".ket_qua.json"), pathlib.Path(ra) / (e["ten"] + ".ban_do.json")
        kq = json.loads(fk.read_text(encoding="utf-8")) if fk.exists() else None
        bd = json.loads(fb.read_text(encoding="utf-8")) if fb.exists() else None
        h, ly = hang(e, kq, bd, danh_muc) if p.returncode == 0 else ("TIN_DUNG_GIA", "con rc %d" % p.returncode)
        (pathlib.Path(ra) / (e["ten"] + ".stderr.txt")).write_text(p.stderr, encoding="utf-8")
        dat = h == e["mong"]
        if e["nhom"] == "dot_bien" and dat:
            phu |= set(e["dich"])
        pids.add((kq or {}).get("pid"))
        ket.append(dict(ten=e["ten"], nhom=e["nhom"], pid=(kq or {}).get("pid"), rc_con=p.returncode, hang=h, mong=e["mong"], dat=dat, ly=ly,
                        so_dich=len(e["dich"]), giay=round(time.time() - t0, 2)))
        print("%-28s %-9s %-13s mong %-13s %s  (%s)" % (e["ten"], e["nhom"], h, e["mong"], "ĐẠT" if dat else "ĐỎ", ly), flush=True)
    chua_phu = sorted(danh_muc - phu)
    ok = all(x["dat"] for x in ket) and not chua_phu and len(danh_muc) == 346 and len(pids - {None}) == len(ket)
    tong = dict(ok=ok, so_muc=len(ket), so_dat=sum(x["dat"] for x in ket), danh_muc=len(danh_muc), so_tien_trinh=len(pids - {None}),
                khoa_chua_phu=chua_phu, ket=ket)
    pathlib.Path(ra, "ket-qua-n4.json").write_text(json.dumps(tong, ensure_ascii=False, indent=1), encoding="utf-8")
    print("N4: ok=%s · mục đạt %d/%d · tiến trình riêng %d · khoá chưa phủ %d/%d" % (ok, tong["so_dat"], len(ket), tong["so_tien_trinh"],
                                                                                     len(chua_phu), len(danh_muc)))
    return 0 if ok else 1
if __name__ == "__main__":
    if sys.argv[1] == "--con":
        con(*sys.argv[2:7])
    else:
        sys.exit(cha(*sys.argv[1:5]))
