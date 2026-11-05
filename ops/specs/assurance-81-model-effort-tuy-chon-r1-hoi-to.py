#!/usr/bin/env python3
"""Phân loại hồi tố #1240. Dùng: python3 -I hoi_to.py --root <kho> [--json]. Chỉ ĐỌC."""
import argparse, glob, json, os, re, sys, unicodedata
import yaml

RE_KHOI = re.compile(r"landed_\d{8}")
RE_ME = re.compile(r"model|effort|ho model|họ model", re.I)
RE_KDD = re.compile(r"KHONG_DO_DUOC|khong_do_duoc|KHÔNG_ĐO_ĐƯỢC|not_measured", re.I)
RE_CHUA = re.compile(r"CHUA[ _]DAT|CHƯA[ _]ĐẠT|not_measured|KHONG_DO_DUOC|CHUA NHA|CHUA nha|KHONG DAT", re.I)
RE_81 = re.compile(r"§8\.1|assurance", re.I)


def chuan(v):
    return unicodedata.normalize("NFC", v.strip().upper().replace(" ", "_")) if isinstance(v, str) else None


def landed_a(d):
    tt = d.get("trang_thai_packet")
    return tt.get("landed") if isinstance(tt, dict) and "landed" in tt else d.get("landed")


def khoi_a81(d):
    """(khối chứa reviewer_assurance_81 dùng để xét, đường dẫn). Gốc trước; không có thì khối lồng DUY NHẤT."""
    if isinstance(d.get("assurance_81"), dict):
        return d["assurance_81"], "$.assurance_81"
    tim = []

    def di(o, p):
        if isinstance(o, dict):
            if "reviewer_assurance_81" in o:
                tim.append((o, p))
            for k, v in o.items():
                di(v, f"{p}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                di(v, f"{p}[{i}]")
    di(d, "$")
    return tim[0] if len(tim) == 1 else (None, f"{len(tim)} khoi long")


def chuoi(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from chuoi(v, f"{p}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from chuoi(v, f"{p}[{i}]")
    elif isinstance(o, str):
        yield p, o


def phan_loai(d):
    r24 = d.get("dinh_chinh_r24")
    if isinstance(d.get("assurance_81"), dict) and isinstance(r24, dict):
        return "G3", "co ca assurance_81 goc lan dinh_chinh_r24"
    if isinstance(r24, dict):
        if not (r24.get("landed_truoc") is True and str(r24.get("lo", "")).startswith("A")):
            return "N0", f"dinh_chinh_r24 lo={str(r24.get('lo'))[:20]!r} landed_truoc={r24.get('landed_truoc')!r}"
        tt_p = d.get("trang_thai_packet")
        dk = tt_p.get("landed_dieu_kien") if isinstance(tt_p, dict) else None
        khac = []
        if isinstance(dk, str):
            phan = re.split(r"\((\d+)\)", re.split(r"Mo lai|Mở lại", dk)[0])
            khac = [f"dieu kien ({so}) chua dat" for so, than in zip(phan[1::2], phan[2::2]) if RE_CHUA.search(than) and not RE_81.search(than)]
        return ("G2", "r24 lo A; " + "; ".join(khac)) if khac else ("G1", "r24 lo A (ho model reviewer khong_do_duoc), landed_truoc true, khong dieu kien khac chua dat")
    a, nguon = khoi_a81(d)
    if a is None:
        nghi = [p for p, v in chuoi(d) if re.search(r"(model|effort)(?:(?!sandbox)[^.;]){0,80}?(KHONG_DO_DUOC|khong_do_duoc|not_measured)", v, re.I)]
        if nghi:
            return "G3", f"khong co khoi assurance xet duoc ({nguon}) nhung co {len(nghi)} chuoi model/effort khong do duoc: {nghi[0]}"
        return "N0", f"khong co khoi assurance xet duoc ({nguon})"
    if chuan(a.get("reviewer_assurance_81")) not in ("CHUA_DAT", "CHƯA_ĐẠT"):
        return "N0", f"reviewer_assurance_81={a.get('reviewer_assurance_81')!r}"
    tt = a.get("thuc_thi") if isinstance(a.get("thuc_thi"), dict) else {}
    m_tt = [k for k in ("model", "effort") if isinstance(tt.get(k), str) and (RE_KDD.search(tt[k]) or not tt[k].startswith("measured"))]
    m_ld = [p for p, v in chuoi(a) if not p.startswith(".thuc_thi") and RE_ME.search(v) and RE_KDD.search(v)
            and re.search(r"(model|effort|ho model|họ model)(?:(?!sandbox)[^.;]){0,80}?(KHONG_DO_DUOC|khong_do_duoc|not_measured)", v, re.I)]
    if not (m_tt or m_ld):
        return "N0", "assurance CHUA_DAT nhung khong co tin hieu model/effort KHONG_DO_DUOC"
    khac = []
    sb = tt.get("sandbox_mode")
    if isinstance(a.get("thuc_thi"), dict) and not (isinstance(sb, str) and sb.startswith("measured") and not RE_KDD.search(sb)):
        khac.append(f"sandbox_mode={str(sb)[:30]!r}")
    if "review_exact_sha" in a and not str(a["review_exact_sha"]).startswith("DAT"):
        khac.append("review_exact_sha khac DAT")
    for k in ("snapshot_82",):
        if k in a and RE_KDD.search(str(a[k])):
            khac.append(f"{k} not_measured")
    tt_p = d.get("trang_thai_packet")
    dk = tt_p.get("landed_dieu_kien") if isinstance(tt_p, dict) else None
    if not isinstance(dk, str):
        return ("G2" if khac else "G3"), "; ".join(khac) or "khong co landed_dieu_kien dang chuoi"
    phan = re.split(r"\((\d+)\)", re.split(r"Mo lai|Mở lại", dk)[0])
    muc = list(zip(phan[1::2], phan[2::2]))
    if not muc:
        return ("G2" if khac else "G3"), "; ".join(khac) or "landed_dieu_kien khong tach duoc (n)"
    for so, than in muc:
        if RE_CHUA.search(than) and not RE_81.search(than):
            khac.append(f"dieu kien ({so}) chua dat")
    if khac:
        return "G2", "; ".join(khac) + " | M=" + ",".join(m_tt + m_ld)
    if not any(RE_81.search(t) for _, t in muc):
        return "G3", "khong thay dieu kien §8.1 trong landed_dieu_kien"
    return "G1", "chi thieu model/effort"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    kq = []
    for f in sorted(glob.glob(os.path.join(a.root, "ops/land/*-land-evidence.yaml"))):
        ten = os.path.relpath(f, a.root)
        try:
            d = yaml.safe_load(open(f, encoding="utf-8"))
        except Exception as e:
            kq.append((ten, "G3", f"YAML loi {type(e).__name__}"))
            continue
        if not isinstance(d, dict):
            kq.append((ten, "G3", "goc khong phai mapping"))
            continue
        if landed_a(d) is not False:
            continue
        if any(RE_KHOI.fullmatch(str(k)) and isinstance(v, dict) and v.get("landed") is True for k, v in d.items()):
            continue
        nhom, ly = phan_loai(d)
        kq.append((ten, nhom, ly))
    dem = {n: sum(1 for _, x, _ in kq if x == n) for n in ("G1", "G2", "G3", "N0")}
    if a.json:
        print(json.dumps({"tong_landed_false_chua_mo": len(kq), "dem": dem, "tep": kq}, ensure_ascii=False, indent=1))
    else:
        for t, n, l in kq:
            print(f"{n}\t{t}\t{l}")
        print("DEM", len(kq), dem)
    return 0


if __name__ == "__main__":
    sys.exit(main())
