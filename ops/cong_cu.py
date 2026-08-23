#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ops/cong_cu.py — G1..G6 packet #290: probe+canary+cổng BA trạng thái (ĐẠT/ĐỎ/
KHÔNG_ĐO_ĐƯỢC, mã riêng) cho `ops/cong_cu.yaml`. `cai-lenh` chỉ TRA CỨU rồi in lệnh cài
(dòng 1) + biến môi trường (dòng sau) — thực thi thuộc `ops/cai_cong_cu.sh`."""
from __future__ import annotations

import argparse, json, os, platform, re, subprocess, sys
from pathlib import Path

import yaml

GOC = Path(__file__).resolve().parent.parent
DAT, DO, KHONG_DO_DUOC = "DAT", "DO", "KHONG_DO_DUOC"
RC = {DAT: 0, DO: 2, KHONG_DO_DUOC: 3}
KY_TU_TOKEN_BAN = re.compile(r"[0-9A-Za-z._+-]")

def doc_ban_ke(duong):
    d = yaml.safe_load(open(duong, encoding="utf-8")) or {}
    if not isinstance(d.get("cong_cu"), dict) or not d["cong_cu"]:
        raise SystemExit(f"ban ke '{duong}' rong hoac thieu khoa 'cong_cu'")
    for ten, dn in d["cong_cu"].items():
        if not isinstance(dn, dict) or not isinstance(dn.get("bat_buoc"), bool):
            raise SystemExit(f"ban ke '{ten}': 'bat_buoc' phai la bool")
        bg = dn.get("ban_ghim")
        if bg is not None and (not isinstance(bg, str) or not bg.strip()):
            raise SystemExit(f"ban ke '{ten}': 'ban_ghim' chi nhan chuoi khac rong hoac null")
        if "canary_bat_buoc" in dn and not isinstance(dn["canary_bat_buoc"], bool):
            raise SystemExit(f"ban ke '{ten}': 'canary_bat_buoc' phai la bool")
        probe = dn.get("probe")
        if not isinstance(probe, list) or not probe:
            raise SystemExit(f"ban ke '{ten}': 'probe' phai la danh sach khac rong")
        for pb in probe:
            erc = pb.get("expected_rc", 0) if isinstance(pb, dict) else None
            erc = [erc] if isinstance(erc, int) and not isinstance(erc, bool) else erc
            if (not isinstance(pb, dict) or not isinstance(pb.get("lenh"), list)
                    or not pb["lenh"] or not all(isinstance(x, str) and x for x in pb["lenh"])
                    or not isinstance(pb.get("regex"), str)
                    or not isinstance(erc, list) or not erc
                    or not all(isinstance(x, int) and not isinstance(x, bool) for x in erc)):
                raise SystemExit(f"ban ke '{ten}': probe/lenh/regex/expected_rc khong hop le")
            try:
                if re.compile(pb["regex"]).groups < 1:
                    raise ValueError
            except (re.error, ValueError):
                raise SystemExit(f"ban ke '{ten}': regex probe phai hop le va co nhom bat")
    return d

def nen_hien_tai():
    t = (os.environ.get("CONG_CU_NEN") or os.environ.get("RUNNER_OS") or platform.system() or "").lower()
    if t.startswith("linux"): return "linux"
    if t in ("macos", "darwin"): return "macos"
    if t.startswith("win") or t in ("mingw", "msys", "cygwin"): return "windows"
    return t or "unknown"

def _chay(argv, timeout=20):
    """Trả (rc, output, lỗi-khởi-chạy); timeout là ĐÃ chạy nhưng hỏng, khác không mở được."""
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or ""), None
    except subprocess.TimeoutExpired as ex:
        ra = (ex.stdout or "") + (ex.stderr or "")
        return None, ra if isinstance(ra, str) else "", "qua_han"
    except OSError as ex:
        return None, "", f"khong_khoi_chay:{type(ex).__name__}"

def _cat_tien_to_token(ra, m):
    """Regex phải bắt trọn token; `1.7.7` trong `1.7.7-rc1` không phải một phiên bản."""
    dau, cuoi = m.start(1), m.end(1)
    return ((dau and KY_TU_TOKEN_BAN.fullmatch(ra[dau - 1]))
            or (cuoi < len(ra) and KY_TU_TOKEN_BAN.fullmatch(ra[cuoi])))

def kiem_tra_1(ten, dn):
    bat_buoc, ban_ghim, ban_thay = dn["bat_buoc"], dn.get("ban_ghim"), {}
    khong_mo, hong = [], []
    for pb in dn.get("probe") or []:
        ten_pb = pb.get("ten", "mac_dinh")
        rc, ra, loi = _chay(pb["lenh"])
        ban_thay[ten_pb] = None
        if loi and loi.startswith("khong_khoi_chay"):
            khong_mo.append(ten_pb)
            continue
        if loi == "qua_han":
            hong.append(f"probe '{ten_pb}' da chay nhung qua han")
            continue
        erc = pb.get("expected_rc", 0)
        erc = [erc] if isinstance(erc, int) else erc
        if rc not in erc:
            hong.append(f"probe '{ten_pb}' da chay nhung rc={rc}, mong {erc}")
            continue
        m = re.search(pb["regex"], ra)
        if not m or not m.group(1) or _cat_tien_to_token(ra, m):
            hong.append(f"probe '{ten_pb}' da chay nhung khong parse tron token phien ban")
            continue
        ban_thay[ten_pb] = m.group(1)
    goc = {"ten": ten, "bat_buoc": bat_buoc, "ban_ghim": ban_ghim, "ban_thay": ban_thay}
    if hong:
        return {**goc, "trang_thai": DO, "chi_tiet": "; ".join(hong)}
    if khong_mo:
        return {**goc, "trang_thai": KHONG_DO_DUOC,
                "chi_tiet": f"khong khoi chay duoc probe {khong_mo} cua '{ten}'"}
    khac_nhau = set(ban_thay.values())
    if len(ban_thay) > 1 and len(khac_nhau) > 1:  # T7, độc lập ban_ghim
        return {**goc, "trang_thai": DO,
                "chi_tiet": f"cac duong goi khac ban: {ban_thay} — co mat khong phai cung ban"}
    if ban_ghim is not None and any(v != ban_ghim for v in ban_thay.values()):
        return {**goc, "trang_thai": DO, "chi_tiet": f"sai ban: mong '{ban_ghim}', thay {ban_thay}"}
    return {**goc, "trang_thai": DAT, "chi_tiet": "dat"}

def kiem_tra_canary(ten_canary, ten_chu, dn, theo_ten, thu_muc_goc):
    chu = theo_ten[ten_chu]
    goc = {"ten": ten_canary, "chu_so_huu": ten_chu,
           "bat_buoc": dn.get("canary_bat_buoc", chu["bat_buoc"])}
    if chu["trang_thai"] != DAT:
        return {**goc, "trang_thai": chu["trang_thai"],
                "chi_tiet": f"tool chu so huu '{ten_chu}' chua DAT"}
    fixture = thu_muc_goc / "ops" / "canary" / f"{ten_canary}.yml"
    if not fixture.is_file():
        return {**goc, "trang_thai": KHONG_DO_DUOC, "chi_tiet": f"thieu fixture '{fixture}'"}
    lenh = [dn["probe"][0]["lenh"][0], str(fixture)]
    rc, ra, loi = _chay(lenh, timeout=30)
    if loi and loi.startswith("khong_khoi_chay"):
        return {**goc, "trang_thai": KHONG_DO_DUOC, "chi_tiet": f"khong goi duoc '{ten_chu}'"}
    if loi == "qua_han":
        return {**goc, "trang_thai": DO, "chi_tiet": f"canary '{ten_canary}' qua han"}
    if "SC1003" in ra:
        return {**goc, "trang_thai": DAT, "chi_tiet": f"canary bat dung SC1003 (rc={rc})"}
    sc_thieu = (theo_ten.get("shellcheck") or {}).get("trang_thai") != DAT
    ly_do = ("SUY_GIAM: thieu shellcheck nen actionlint am tham bo lop luat SC*" if sc_thieu else
             "canary KHONG bat duoc SC1003 du shellcheck co mat — kiem fixture/ban actionlint")
    return {**goc, "trang_thai": DO, "chi_tiet": f"{ly_do} (rc={rc})"}

def tong_hop(ban_ke, thu_muc_goc=None, chi=None):
    cc = ban_ke["cong_cu"]
    theo_ten = {t: kiem_tra_1(t, cc[t]) for t in ([chi] if chi else cc.keys())}
    canary_kq, da_chay = [], set()
    if chi is None:
        for ten, dn in cc.items():
            cn = dn.get("canary")
            if cn and cn not in da_chay:
                da_chay.add(cn)
                canary_kq.append(kiem_tra_canary(cn, ten, dn, theo_ten, thu_muc_goc or GOC))
    tong = DAT
    for kq in list(theo_ten.values()) + canary_kq:
        if kq["trang_thai"] == KHONG_DO_DUOC and kq.get("bat_buoc"):
            tong = KHONG_DO_DUOC
        elif kq["trang_thai"] == DO and tong != KHONG_DO_DUOC:
            tong = DO
    return {"trang_thai_tong": tong, "cong_cu": list(theo_ten.values()), "canary": canary_kq}

def _cai_lenh(ten, ban_ke, nen):
    dn = ban_ke["cong_cu"].get(ten)
    if dn is None: raise SystemExit(f"khong biet cong cu '{ten}'")
    cai = dn.get("cai") or {}
    ct = cai if "lenh" in cai else cai.get(nen)  # {lenh:..} dung chung MOI nen, hoac theo-nen
    if not ct: raise SystemExit(f"'{ten}' chua co cong thuc cai cho nen '{nen}'")
    print(ct["lenh"])
    for k, v in (ct.get("moi_truong") or {}).items():
        print(f"{k}={v}")
    return 0

def main(argv=None):
    ap = argparse.ArgumentParser(prog="cong_cu.py")
    sub = ap.add_subparsers(dest="lenh", required=True)
    p1 = sub.add_parser("kiem-tra")
    p1.add_argument("--chi"); p1.add_argument("--json", action="store_true"); p1.add_argument("--ban-ke")
    p2 = sub.add_parser("cai-lenh")
    p2.add_argument("ten"); p2.add_argument("--nen"); p2.add_argument("--ban-ke")
    a = ap.parse_args(argv)
    duong_ban_ke = Path(a.ban_ke) if a.ban_ke else GOC / "ops" / "cong_cu.yaml"
    ban_ke = doc_ban_ke(duong_ban_ke)
    if a.lenh == "cai-lenh":
        return _cai_lenh(a.ten, ban_ke, a.nen or nen_hien_tai())
    bc = tong_hop(ban_ke, chi=a.chi)  # T8: JSON mang van tay ten+ban_thay cho MOI ban ghi
    print(json.dumps(bc, ensure_ascii=False, indent=2 if a.json else None))
    return RC[bc["trang_thai_tong"]]

if __name__ == "__main__":
    sys.exit(main())
