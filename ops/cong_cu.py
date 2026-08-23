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

def doc_ban_ke(duong):
    d = yaml.safe_load(open(duong, encoding="utf-8")) or {}
    if not isinstance(d.get("cong_cu"), dict) or not d["cong_cu"]:
        raise SystemExit(f"ban ke '{duong}' rong hoac thieu khoa 'cong_cu'")
    return d

def nen_hien_tai():
    t = (os.environ.get("CONG_CU_NEN") or os.environ.get("RUNNER_OS") or platform.system() or "").lower()
    if t.startswith("linux"): return "linux"
    if t in ("macos", "darwin"): return "macos"
    if t.startswith("win") or t in ("mingw", "msys", "cygwin"): return "windows"
    return t or "unknown"

def _chay(argv, timeout=20):
    """rc=None: khong khoi chay duoc. Doc CA stdout+stderr (vd `shellcheck --version` in
    ra stderr, khong phai stdout)."""
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None, ""

def kiem_tra_1(ten, dn):
    bat_buoc, ban_ghim, ban_thay = bool(dn.get("bat_buoc")), dn.get("ban_ghim"), {}
    for pb in dn.get("probe") or []:
        rc, ra = _chay(pb["lenh"])
        if rc is None:
            continue
        m = re.search(pb["regex"], ra) if pb.get("regex") else None
        ban_thay[pb.get("ten", "mac_dinh")] = m.group(1) if m else None
    goc = {"ten": ten, "bat_buoc": bat_buoc, "ban_ghim": ban_ghim, "ban_thay": ban_thay}
    if not ban_thay:
        return {**goc, "trang_thai": KHONG_DO_DUOC,
                "chi_tiet": f"khong tim thay '{ten}' — moi probe deu khong khoi chay duoc"}
    # T7: >=2 duong probe, cac ban THAY (bo None) khac nhau => DO, DOC LAP voi ban_ghim.
    khac_nhau = {v for v in ban_thay.values() if v is not None}
    if len(ban_thay) > 1 and len(khac_nhau) > 1:
        return {**goc, "trang_thai": DO,
                "chi_tiet": f"cac duong goi khac ban: {ban_thay} — co mat khong phai cung ban"}
    if ban_ghim and not any(v == ban_ghim for v in ban_thay.values()):
        return {**goc, "trang_thai": DO, "chi_tiet": f"sai ban: mong '{ban_ghim}', thay {ban_thay}"}
    return {**goc, "trang_thai": DAT, "chi_tiet": "dat"}

def kiem_tra_canary(ten_canary, theo_ten, thu_muc_goc):
    al = theo_ten.get("actionlint")
    if al is None or al["trang_thai"] == KHONG_DO_DUOC:
        return {"ten": ten_canary, "trang_thai": KHONG_DO_DUOC, "chi_tiet": "khong co actionlint"}
    fixture = thu_muc_goc / "ops" / "canary" / f"{ten_canary}.yml"
    if not fixture.is_file():
        return {"ten": ten_canary, "trang_thai": KHONG_DO_DUOC, "chi_tiet": f"thieu fixture '{fixture}'"}
    rc, ra = _chay(["actionlint", str(fixture)], timeout=30)
    if rc is None:
        return {"ten": ten_canary, "trang_thai": KHONG_DO_DUOC, "chi_tiet": "khong goi duoc actionlint"}
    if "SC1003" in ra:
        return {"ten": ten_canary, "trang_thai": DAT, "chi_tiet": "canary bat dung SC1003"}
    sc_thieu = (theo_ten.get("shellcheck") or {}).get("trang_thai") != DAT
    ly_do = ("SUY_GIAM: thieu shellcheck nen actionlint am tham bo lop luat SC*" if sc_thieu else
             "canary KHONG bat duoc SC1003 du shellcheck co mat — kiem fixture/ban actionlint")
    return {"ten": ten_canary, "trang_thai": DO, "chi_tiet": ly_do}

def tong_hop(ban_ke, thu_muc_goc=None, chi=None):
    cc = ban_ke["cong_cu"]
    theo_ten = {t: kiem_tra_1(t, cc[t]) for t in ([chi] if chi else cc.keys())}
    canary_kq, da_chay = [], set()
    if chi is None:
        for dn in cc.values():
            cn = dn.get("canary")
            if cn and cn not in da_chay:
                da_chay.add(cn)
                canary_kq.append(kiem_tra_canary(cn, theo_ten, thu_muc_goc or GOC))
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
