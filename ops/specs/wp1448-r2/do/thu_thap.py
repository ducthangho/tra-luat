#!/usr/bin/env python3
"""wp1448 r2 — bo thu v2 (dac ta ops/specs/wp1448-r2/SPEC.md muc 5), CHI DOC. Ke thua hop dong cua bo thu #1434
(`ops/specs/wp1434-r3/do/thu_thap.py`, nap bang duong dan, KHONG sua): anh chup NGOAI kho, ba che do, ba trang thai,
ghi co gioi han, `--tinh` tat dinh va khong goi git.

  --thu --anh-chup <anh chup #1434> --ra <anh chup v2> [--run-g5 id,id] [--kho <kho git>]
        GitHub REST GET -> them vao MOT thu muc anh chup v2 RIENG (khong ghi vao anh chup #1434): log job gom cong cu, danh
        sach artifact, luot + job cua `packet-loop-dot-bien.yml`, log manh G5 cua cac luot neu ten o `--run-g5`; co `--kho`
        thi tinh oracle ngu canh moi tu bon OID (git CHI DOC tren kho ay) va luu vao anh chup v2.
  --tinh --anh-chup <anh chup #1434> --ra <thu muc> [--anh-chup-v2 <anh chup v2>] [--cohort-goc <COHORT.json>]
        thuan offline -> nen/ (BASELINE.json cua bo thu #1434 tren cung anh chup), BASELINE_V2.json, BAO_CAO_V2.md
  --tu-kiem
        ca tu kiem tren fixtures/, khong mang, khong git; gom dot bien tren BAN SAO cua chinh tep nay.

Them so voi #1434: ban ghi theo (run_id, attempt, su kien, head) voi che do du dinh, che do thuc chay, ly do bo, trang thai
hoan tat va dau hieu duong; doc cac dong `G5_THOI_GIAN`, `BONG_CONG_CU`, `BONG_PHAN_LOAI` khi co; thoi gian theo buoc cua
`gate` va `gate-ops`; workflow `packet-loop-dot-bien.yml`; phep quy G4a va G4b (muoi buoc co thu tu, vet can).
"""
import argparse
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

DAY = pathlib.Path(__file__).resolve().parent
ROOT = next((p for p in DAY.parents if (p / "ops" / "specs" / "wp1434-r3" / "do").is_dir()), DAY.parent)   # ban sao tam: khong co kho
TEP_GOC = ROOT / "ops" / "specs" / "wp1434-r3" / "do" / "thu_thap.py"
NEN_GOC = ROOT / "ops" / "specs" / "wp1434-r3" / "do" / "BASELINE.json"
SPEC_SHA256 = "5014de59a48aad517ae22d1b91a6ae8dc1b382fc4650fdddecffe9cc5927c53e"
WF_PL = "packet-loop-dot-bien.yml"
DO_DUOC, KHONG_AP_DUNG, KHONG_DO_DUOC = "do_duoc", "khong_ap_dung", "khong_do_duoc"
DAY_DU, DUONG_NHANH = "day_du", "duong_nhanh"
SO_MANH_G5 = 8
JOB_MANH, JOB_GOM, JOB_CHUAN_BI = "gate-cong-cu", "gate-cong-cu-gop", "chuan-bi"
JOB_BUOC_V2 = ("gate", "gate-ops")                                 # them so voi JOB_BUOC cua #1434
ALLOWLIST = ("ops/land/", "ops/leases/", "ops/reviews/", "ops/specs/")
DUOI_MA_CAP_NONG = (".py", ".sh", ".bash", ".ps1", ".psm1", ".bat", ".cmd", ".js", ".mjs")
MODE_VE_DAY_DU = ("100755", "120000", "160000")
TT = r"^﻿?(?:\S+Z )?"                                           # tien to thoi gian cua log job (co the vang)
RE_CHE_DO = re.compile(TT + r"che_do=(duong_nhanh|day_du)\s*$")
RE_CONG_CU = re.compile(TT + r"cong_cu=(chay|bo_qua)\s*$")          # output THAT cua PR3 (chua co o PR1)
RE_BONG = re.compile(TT + r"(BONG_CONG_CU|BONG_PHAN_LOAI): (.*)$")
RE_G5 = re.compile(TT + r"G5_THOI_GIAN (\{.*\})\s*$")
RE_GOM_DU = re.compile(TT + r"GOM MẢNH (\d+)/(\d+)\s*$")
RE_GOM_KHONG_DO = re.compile(TT + r"GOM: KHÔNG ĐO — (.*)$")
DAU_KHONG_DO = {"duong_nhanh": "=duong_nhanh, 0 mảnh", "bo_moi": "cong_cu=bo_qua"}   # dau RIENG cua tung ly do bo
RE_OID = re.compile(r"[0-9a-f]{40}")
# Cac khoa `[B: …]` ma muc 2 cua ke hoach nguon r3 trich, va hai phep khoa cua [DX-2]: (nhan, duong toi gia tri trong BASELINE).
KHOA_TAI_LAP = (
    ("M2.so_luot", ("M2", "so_luot")),
    ("M2.moi_luot.tat_ca.giay_thuc_thi.tong", ("M2", "moi_luot", "tat_ca", "giay_thuc_thi", "tong")),
    ("M2.moi_luot.tat_ca.giay_thuc_thi.trung_vi", ("M2", "moi_luot", "tat_ca", "giay_thuc_thi", "trung_vi")),
    ("M2.moi_luot.tat_ca.giay_thuc_thi.p90", ("M2", "moi_luot", "tat_ca", "giay_thuc_thi", "p90")),
    ("M2.theo_lan", ("M2", "theo_lan")),
    ("M2.theo_ket_luan", ("M2", "theo_ket_luan")),
    ("M2.theo_buoc.bang[G5 manh].n", ("M2", "theo_buoc", "bang", "gate-cong-cu | ubuntu-latest | day_du | G5 manh ban kinh dot bien (#668)", "n")),
    ("M2.theo_buoc.bang[G5 manh].tong", ("M2", "theo_buoc", "bang", "gate-cong-cu | ubuntu-latest | day_du | G5 manh ban kinh dot bien (#668)", "tong")),
    ("M2.theo_buoc.bang[G5 manh].trung_vi", ("M2", "theo_buoc", "bang", "gate-cong-cu | ubuntu-latest | day_du | G5 manh ban kinh dot bien (#668)", "trung_vi")),
    ("M2.theo_buoc.bang[G5 manh].p90", ("M2", "theo_buoc", "bang", "gate-cong-cu | ubuntu-latest | day_du | G5 manh ban kinh dot bien (#668)", "p90")),
    ("M2.moi_luot.theo_su_kien_va_lan[pull_request | day_du].giay_thuc_thi", ("M2", "moi_luot", "theo_su_kien_va_lan", "pull_request | day_du", "giay_thuc_thi")),
    ("M2b.bang[gate-registry | ubuntu-latest | ops/ci_provenance_test.py].so_ban_ghi", ("M2b", "bang", "gate-registry | ubuntu-latest | ops/ci_provenance_test.py", "so_ban_ghi")),
    ("M3.bang[ops/cong_cu_test.py]", ("M3", "bang", "ops/cong_cu_test.py")),
    ("M3.bang[ops/ci_provenance_test.py]", ("M3", "bang", "ops/ci_provenance_test.py")),
    ("M1.muc_ket_qua_theo_khoa.so_khoa", ("M1", "muc_ket_qua_theo_khoa", "so_khoa")),
    ("[DX-2] top5_giay_thuc_thi[0].so_dong_thuc_thi", ("top5_giay_thuc_thi", 0, "so_dong_thuc_thi")),
    ("[DX-2] top5_giay_thuc_thi[0].tong_giay_thuc_thi", ("top5_giay_thuc_thi", 0, "tong_giay_thuc_thi")),
)
LOAI_G4B = ("huy_truoc_phan_loai", "ngoai_mau_so", "thieu_bang_chung", "duong_nhanh_co_bang_chung", "bo_moi_co_bang_chung",
            "du_hoan_tat", "dich_hoan_tat", "gom_hong", "dang_do")
LOAI_G4A = ("duong_nhanh_dang_chay", "bo_moi", "dich", "du", "khong_phan_loai_duoc")


def nap_goc():
    """Module bo thu #1434, nap bang duong dan (ke thua hop dong, khong chep, khong sua)."""
    spec = importlib.util.spec_from_file_location("thu_thap_wp1434", TEP_GOC)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ───────────────────────── ham thuan ─────────────────────────

def kdd(ly_do):
    return {"trang_thai": KHONG_DO_DUOC, "ly_do": ly_do}


def tach_khoa(than):
    """`a=1 b=2 …` -> dict; phan tu khong co `=` bi bo. Gia tri co the mang `=` (chi tach o dau `=` dau tien)."""
    return dict(x.split("=", 1) for x in than.split(" ") if "=" in x)


def trich_bong(van_ban):
    """Log job chuan-bi -> {che_do_chay, cong_cu_that, bong_cong_cu, bong_phan_loai}. Moi phan: gia tri hoac None (KHONG doan).
    Dong lap lai: lay dong CUOI (cung quy tac voi `trich_lan` cua #1434)."""
    kq = {"che_do_chay": None, "cong_cu_that": None, "bong_cong_cu": None, "bong_phan_loai": None}
    for dong in van_ban.splitlines():
        m = RE_CHE_DO.match(dong)
        if m:
            kq["che_do_chay"] = m.group(1)
            continue
        m = RE_CONG_CU.match(dong)
        if m:
            kq["cong_cu_that"] = m.group(1)
            continue
        m = RE_BONG.match(dong)
        if m:
            than = m.group(2)
            d = tach_khoa(than)
            if m.group(1) == "BONG_CONG_CU":
                d["quyet_dinh"] = than.split(" ", 1)[0]
                kq["bong_cong_cu"] = d if d["quyet_dinh"] in ("chay", "bo_qua", KHONG_DO_DUOC) else {"quyet_dinh": KHONG_DO_DUOC, "ly_do": "dong_la"}
            else:
                kq["bong_phan_loai"] = d
    return kq


def dem_bong(che_do_chay, bong_phan_loai, oracle):
    """Hai bo dem TACH RIENG cua mot luot, moi cai 1 | 0 | None (khong du du lieu):
    LOI ICH       = luat cu khac ngu canh moi (`cu` != `moi` cua dong bong);
    SAI SOT TON DU = phan loai DANG CHAY khac oracle ngu canh moi (tinh lai doc lap tu bon OID)."""
    hop_le = (DAY_DU, DUONG_NHANH)
    pl = bong_phan_loai or {}
    loi_ich = int(pl["cu"] != pl["moi"]) if pl.get("cu") in hop_le and pl.get("moi") in hop_le else None
    ton_du = int(che_do_chay != oracle) if che_do_chay in hop_le and oracle in hop_le else None
    return {"loi_ich": loi_ich, "ton_du": ton_du}


def trich_gom(van_ban):
    """Log job gom cong cu -> dau hieu duong: `gom_manh:<n>` | `khong_do:duong_nhanh` | `khong_do:bo_moi` | `khong_do:la` | None."""
    dau = None
    for dong in van_ban.splitlines():
        m = RE_GOM_DU.match(dong)
        if m and m.group(1) == m.group(2):
            dau = "gom_manh:" + m.group(1)
            continue
        m = RE_GOM_KHONG_DO.match(dong)
        if m:
            khop = [t for t, d in DAU_KHONG_DO.items() if d in m.group(1)]
            dau = "khong_do:" + (khop[0] if len(khop) == 1 else "la")
    return dau


def hop_khoang(khoang):
    """Do dai HOP cua cac khoang [a, b]: con chay chong nhau nen khong cong thang."""
    tong, cuoi = 0.0, None
    for a, b in sorted((float(a), float(b)) for a, b in khoang if b >= a):
        if cuoi is None or a > cuoi:
            tong, cuoi = tong + (b - a), b
        elif b > cuoi:
            tong, cuoi = tong + (b - cuoi), b
    return tong


def trich_g5(van_ban):
    """Cac ban ghi `G5_THOI_GIAN` cua MOT log manh; dong hong -> ban ghi khong_do_duoc."""
    kq = []
    for dong in van_ban.splitlines():
        m = RE_G5.match(dong)
        if not m:
            continue
        try:
            bg = json.loads(m.group(1))
            if not isinstance(bg, dict):
                raise ValueError
        except ValueError:
            bg = {"loai": "hong", "trang_thai": KHONG_DO_DUOC, "ly_do": "dong G5_THOI_GIAN khong doc duoc"}
        kq.append(bg)
    return kq


def tong_hop_g5(ban_ghi, giay_buoc=None):
    """Mot manh: doi chieu thoi gian tuong cua BUOC (`giay_buoc`, tu API; vang thi dung `tuong_s` cua cha) voi HOP cac khoang con;
    phan lech la `khong_phan_bo_s`. Moi dot bien phai du ba thanh phan (dung cay, ca dich, ca khac) hoac `khong_do_duoc`."""
    cha = [b for b in ban_ghi if b.get("loai") == "cha"]
    con = [b for b in ban_ghi if b.get("loai") == "con"]
    db = [b for b in ban_ghi if b.get("loai") == "dot_bien"]
    so = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
    du = [b for b in db if b.get("trang_thai") == DO_DUOC and all(so(b.get(k)) for k in ("dung_cay_s", "ca_dich_s", "ca_khac_s"))]
    kq = {"so_dot_bien": len(db), "so_du_ba_thanh_phan": len(du), "so_thieu": len(db) - len(du),
          "ten_thieu": sorted(str(b.get("ten")) for b in db if b not in du)[:20], "so_con": len(con)}
    khoang = [(b["bat_dau"], b["ket_thuc"]) for b in con if so(b.get("bat_dau")) and so(b.get("ket_thuc"))]
    tuong = giay_buoc if so(giay_buoc) else (cha[-1].get("tuong_s") if cha and so(cha[-1].get("tuong_s")) else None)
    if not khoang or len(khoang) != len(con) or tuong is None or tuong <= 0:
        kq["doi_chieu"] = kdd("thieu khoang con hoac thoi gian tuong")
        return kq
    hop = hop_khoang(khoang)
    kq["doi_chieu"] = {"trang_thai": DO_DUOC, "tuong_s": tuong, "hop_con_s": round(hop, 3), "tong_con_s": round(sum(b - a for a, b in khoang), 3),
                       "khong_phan_bo_s": round(tuong - hop, 3), "lech_ti_le": round(abs(tuong - hop) / tuong, 4),
                       "trong_10_phan_tram": abs(tuong - hop) / tuong <= 0.10}
    for ten, khoa in (("dung_cay_s", "dung_cay_s"), ("ca_dich_s", "ca_dich_s"), ("ca_khac_s", "ca_khac_s")):
        kq["tong_" + ten] = round(sum(b.get(khoa) or 0 for b in du), 3)
    return kq


def chi_so_manh(ten):
    """`gate-cong-cu (ubuntu-latest, 3)` -> 3; ten khac dang -> None."""
    m = re.fullmatch(JOB_MANH + r" \(ubuntu-latest, (\d+)\)", ten or "")
    return int(m.group(1)) if m else None


def dung_luot(run, dong, log=None, artifact=None):
    """Ban ghi CHUAN HOA cua mot luot ci.yml o attempt CUOI, tu: `run` (API), `dong` (dong job: ten, ket_luan, run_attempt,
    head_sha, job_id — moi attempt), `log` ({'chuan_bi': van ban | None, 'gom': van ban | None}) va `artifact` (danh sach ten
    artifact con han, hoac None = khong thu). Dong cua attempt cuoi duoc uu tien; job khong chay lai o attempt cuoi lay dong moi
    nhat cua no (mang sang)."""
    log = log or {}
    so_att = int(run.get("run_attempt") or 1)
    moi_nhat = {}
    for d in sorted(dong, key=lambda d: (int(d.get("run_attempt") or 1), d.get("job_id") or 0)):
        if int(d.get("run_attempt") or 1) <= so_att:
            moi_nhat[d.get("ten")] = d
    cb = next((d for t, d in moi_nhat.items() if t == JOB_CHUAN_BI), None)
    gom = next((d for t, d in moi_nhat.items() if (t or "").startswith(JOB_GOM + " (ubuntu-latest")), None)
    tb = trich_bong(log["chuan_bi"]) if isinstance(log.get("chuan_bi"), str) else trich_bong("")
    pl = tb["bong_phan_loai"] or {}
    # luat CU: truoc PR4 phan loai dang chay CHINH la luat cu; tu PR1 dong bong ghi rieng `cu`
    lan_cu = pl.get("cu") if pl.get("cu") in (DAY_DU, DUONG_NHANH) else tb["che_do_chay"]
    head = run.get("head_sha")
    manh = {}
    for t, d in moi_nhat.items():
        k = chi_so_manh(t)
        if k is not None:
            manh[k] = d
    co_art = None if artifact is None else {k for k in range(SO_MANH_G5) if f"{JOB_MANH}-manh-ubuntu-latest-{k}" in set(artifact)}
    hop_le, sai = 0, 0
    for k in range(SO_MANH_G5):
        d = manh.get(k)
        if d is None or d.get("ket_luan") != "success":
            continue
        if d.get("head_sha") != head or (co_art is not None and k not in co_art):
            sai += 1
        else:
            hop_le += 1
    return {"run_id": run.get("id"), "attempt": so_att, "su_kien": run.get("event"), "head": head, "ket_luan": run.get("conclusion"),
            "chuan_bi": cb.get("ket_luan") if cb else None, "co_log_chuan_bi": isinstance(log.get("chuan_bi"), str),
            "lan_cu": lan_cu, "che_do_chay": tb["che_do_chay"], "cong_cu_that": tb["cong_cu_that"],
            "bong_cong_cu": tb["bong_cong_cu"], "bong_phan_loai": tb["bong_phan_loai"],
            "che_do_g5": "du",                                      # `dich` chi co tu PR6; bien nhan khi ay phai mang truong che do
            "gom": {"ket_luan": gom.get("ket_luan") if gom else None, "dau": trich_gom(log["gom"]) if isinstance(log.get("gom"), str) else None,
                    "co_log": isinstance(log.get("gom"), str)},
            "manh": {"ket_luan": [manh[k].get("ket_luan") if k in manh else None for k in range(SO_MANH_G5)],
                     "bien_nhan_hop_le": hop_le, "bien_nhan_sai": sai,
                     "nguon_bien_nhan": "job+artifact" if co_art is not None else "job (khong co danh sach artifact)"}}


def che_do_chon(l):
    """Che do G5 DUOC CHON cua mot luot: `bo_dn` | `bo_moi` | `du` | `dich` | None (khong doc duoc che do dang chay)."""
    if l.get("che_do_chay") == DUONG_NHANH:
        return "bo_dn"
    if l.get("che_do_chay") != DAY_DU:
        return None
    if l.get("cong_cu_that") == "bo_qua":
        return "bo_moi"
    return l.get("che_do_g5") if l.get("che_do_g5") in ("du", "dich") else None


def quy_g4a(l):
    """Che do DUOC CHON, mot loai cho moi luot cua mau so."""
    return {"bo_dn": "duong_nhanh_dang_chay", "bo_moi": "bo_moi", "du": "du", "dich": "dich"}.get(che_do_chon(l), "khong_phan_loai_duoc")


def quy_g4b(l):
    """(loai, buoc) — phep quy G4b CO THU TU va VET CAN cua muc 3 ke hoach nguon r3: xet tu buoc 0, buoc DAU TIEN khop quyet
    dinh; buoc 10 nhan moi thu con lai. Buoc 0 va 1 dua luot ra NGOAI mau so."""
    gom, manh, chon = l.get("gom") or {}, l.get("manh") or {}, che_do_chon(l)
    kl_gom, dau = gom.get("ket_luan"), gom.get("dau")
    du_bien_nhan = manh.get("bien_nhan_hop_le") == SO_MANH_G5 and not manh.get("bien_nhan_sai")
    hong = ("cancelled", "failure", "timed_out")
    bi_huy_do = l.get("ket_luan") in hong or kl_gom in hong or any(x in hong for x in manh.get("ket_luan") or ())
    if l.get("chuan_bi") != "success" and l.get("lan_cu") is None and l.get("che_do_chay") is None:
        return "huy_truoc_phan_loai", 0
    if l.get("lan_cu") is not None and l.get("lan_cu") != DAY_DU:
        return "ngoai_mau_so", 1
    if chon is None:
        return "thieu_bang_chung", 2
    if chon == "bo_dn" and kl_gom == "success" and dau == "khong_do:duong_nhanh":
        return "duong_nhanh_co_bang_chung", 3
    if chon == "bo_moi" and kl_gom == "success" and dau == "khong_do:bo_moi":
        return "bo_moi_co_bang_chung", 4
    if chon == "du" and du_bien_nhan and kl_gom == "success":
        return "du_hoan_tat", 5
    if chon == "dich" and du_bien_nhan and kl_gom == "success":
        return "dich_hoan_tat", 6
    if kl_gom != "success" and (chon in ("bo_dn", "bo_moi") or du_bien_nhan):
        return "gom_hong", 7
    if chon in ("du", "dich") and kl_gom != "success" and not du_bien_nhan and bi_huy_do:
        return "dang_do", 8
    if kl_gom == "success":
        return "thieu_bang_chung", 9
    return "thieu_bang_chung", 10


def tong_hop_g4(cac_luot):
    """G4a + G4b tren cac luot pull_request (attempt cuoi). Mau so: buoc >= 2. Tran: thieu_bang_chung <= 2 % mau so."""
    g4b = {t: 0 for t in LOAI_G4B}
    theo_buoc = {str(i): 0 for i in range(11)}
    g4a = {t: 0 for t in LOAI_G4A}
    for l in cac_luot:
        loai, buoc = quy_g4b(l)
        g4b[loai] += 1
        theo_buoc[str(buoc)] += 1
        if buoc >= 2:
            g4a[quy_g4a(l)] += 1
    mau = sum(n for b, n in theo_buoc.items() if int(b) >= 2)
    thieu = sum(theo_buoc[b] for b in ("2", "9", "10"))
    return {"so_luot_pull_request": len(cac_luot), "mau_so": mau, "G4a": g4a, "G4b": g4b, "G4b_theo_buoc": theo_buoc,
            "thieu_bang_chung_ti_le": round(thieu / mau, 4) if mau else None,
            "phu_hoan_tat": g4b["du_hoan_tat"] + g4b["dich_hoan_tat"],
            "bo_moi_ti_le": round(g4a["bo_moi"] / mau, 4) if mau else None}


def _git(kho, *doi, chay=subprocess.run):
    r = chay(["git", "-C", str(kho), *doi], capture_output=True, timeout=120)
    if r.returncode not in (0, 1):
        raise RuntimeError(f"git {doi[0]} rc={r.returncode}")
    return r.returncode, r.stdout


def oracle_moi(kho, goc_su_kien, goc_so, dau, chay=subprocess.run):
    """Phan loai theo NGU CANH MOI, tinh lai DOC LAP tu OID (khong goi `ops/ci_duong_nhanh.py`): goc su kien phai la to tien
    cua `goc_so`; `goc_so` va `dau` co DUNG mot merge-base; tap duong dan = ba cham ∪ diff `goc_so` -> cay merge mo phong. Mot
    duong dan ngoai bon tien to ho so, ma cap nong, mode moi thuc thi/symlink/gitlink, doi mode, hay sua/xoa dac ta da co =>
    `day_du`; khong con gi => `duong_nhanh`. Thieu OID, thieu object, git loi => `khong_do_duoc`. Chi dung o `--thu`."""
    if not all(isinstance(x, str) and RE_OID.fullmatch(x) for x in (goc_su_kien, goc_so, dau)):
        return KHONG_DO_DUOC
    try:
        if _git(kho, "merge-base", "--is-ancestor", goc_su_kien, goc_so, chay=chay)[0] != 0:
            return KHONG_DO_DUOC
        rc, mb = _git(kho, "merge-base", "--all", goc_so, dau, chay=chay)
        if rc != 0 or not re.fullmatch(rb"[0-9a-f]{40}\n", mb):
            return KHONG_DO_DUOC
        rc, cay = _git(kho, "--attr-source=" + goc_so, "merge-tree", "--write-tree", "--no-messages", goc_so, dau, chay=chay)
        if rc != 0 or not re.fullmatch(rb"[0-9a-f]{40}\n", cay):
            return KHONG_DO_DUOC
        ban_ghi = []
        for cap in ((f"{goc_so}...{dau}",), (goc_so, cay.decode().strip())):
            rc, ra = _git(kho, "--attr-source=" + goc_so, "diff", "--raw", "-z", "--no-renames", "--no-abbrev", *cap, chay=chay)
            muc = ra.decode("utf-8", "surrogateescape").split("\0")
            if rc != 0 or muc[-1] != "" or len(muc) % 2 != 1:
                return KHONG_DO_DUOC
            ban_ghi += list(zip(muc[0:-1:2], muc[1:-1:2]))
    except (RuntimeError, OSError, subprocess.SubprocessError):
        return KHONG_DO_DUOC
    for dau_ghi, duong in ban_ghi:
        m = re.fullmatch(r":([0-7]{6}) ([0-7]{6}) [0-9a-f]+ [0-9a-f]+ ([AMDT])", dau_ghi)
        if not m:
            return KHONG_DO_DUOC
        cu, moi, tt = m.groups()
        tp = duong.split("/")
        if not duong.startswith(ALLOWLIST) or any(t in ("", ".", "..") for t in tp) or "\\" in duong or any(ord(c) < 32 or ord(c) == 127 for c in duong):
            return DAY_DU
        if len(tp) == 3 and tp[2].lower().endswith(DUOI_MA_CAP_NONG):
            return DAY_DU
        if moi in MODE_VE_DAY_DU or (cu != "000000" and moi != "000000" and cu != moi):
            return DAY_DU
        if duong.startswith("ops/specs/") and tt in ("M", "D", "T"):
            return DAY_DU
    return DUONG_NHANH


def lay_duong(d, duong):
    for k in duong:
        try:
            d = d[k]
        except (KeyError, IndexError, TypeError):
            return KHONG_DO_DUOC
    return d


def doi_chieu_khoa(nen_moi, nen_goc):
    """Tung khoa cua `KHOA_TAI_LAP`: `khop` | `lech` | `khong_do_duoc` (mot ben khong co khoa)."""
    kq = []
    for nhan, duong in KHOA_TAI_LAP:
        a, b = lay_duong(nen_moi, duong), lay_duong(nen_goc, duong)
        nguon_hong = [x.get("_tep") for x in (a, b) if isinstance(x, dict) and isinstance(x.get("_tep"), dict)
                      and x["_tep"].get("trang_thai") == KHONG_DO_DUOC]   # bang M3 ma chinh NGUON trong anh chup khong do duoc
        kl = KHONG_DO_DUOC if (KHONG_DO_DUOC in (a, b) or nguon_hong) else ("khop" if a == b else "lech")
        kq.append({"khoa": nhan, "ket_luan": kl, "gia_tri_tinh_lai": a, "gia_tri_BASELINE": b,
                   **({"ly_do": str(nguon_hong[0].get("ly_do"))[:200]} if nguon_hong else {})})
    return kq


def xuat_json(o):
    return (json.dumps(o, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8")


# ───────────────────────── --tinh ─────────────────────────

def doc_anh_chup(ac):
    """(doc(khoa) -> bytes | None, manifest theo khoa) cua mot anh chup da dong MANIFEST; None neu khong co MANIFEST."""
    f = ac / "MANIFEST.json"
    if not f.exists():
        return None, {}
    theo_khoa = {m["khoa"]: m for m in json.loads(f.read_bytes())["tep"]}

    def doc(khoa):
        m = theo_khoa.get(khoa)
        return (ac / m["duong_dan"]).read_bytes() if m and m.get("duong_dan") else None
    return doc, theo_khoa


def lenh_tinh(ns):
    g = nap_goc()
    ac, ra = pathlib.Path(ns.anh_chup).resolve(), pathlib.Path(ns.ra).resolve()
    if ROOT == ra or ROOT in ra.parents:
        print("TU CHOI GHI: thu muc --ra phai nam NGOAI kho")
        return 4
    ra.mkdir(parents=True, exist_ok=True)
    cohort_goc = None
    if ns.cohort_goc:
        cohort_goc = {int(r) for wf in json.loads(pathlib.Path(ns.cohort_goc).read_bytes())["cap_run_attempt"].values() for r, _ in wf}
        loc_cu = g.loc_cohort

        def loc_theo_cohort_goc(ds_run, workflow, t0, t1):
            trong, loai = loc_cu(ds_run, workflow, t0, t1)
            return ([r for r in trong if r.get("id") in cohort_goc],
                    loai + [(r.get("id"), "ngoai_cohort_goc") for r in trong if r.get("id") not in cohort_goc])
        g.loc_cohort = loc_theo_cohort_goc
    rc = g.lenh_tinh(argparse.Namespace(anh_chup=str(ac), ra=str(ra / "nen")))
    if rc != 0:
        print("bo thu #1434 --tinh tra rc =", rc)
        return rc
    nen_moi = json.loads((ra / "nen" / "BASELINE.json").read_bytes())
    nen_goc = json.loads(NEN_GOC.read_bytes())
    doc, theo_khoa = doc_anh_chup(ac)
    doc2, theo_khoa2 = doc_anh_chup(pathlib.Path(ns.anh_chup_v2).resolve()) if ns.anh_chup_v2 else (None, {})
    meta = json.loads((ac / "META.json").read_bytes())

    def van_ban(khoa, nguon=doc):
        b = nguon(khoa) if nguon else None
        return None if b is None else b.decode("utf-8", errors="replace")

    ds_ci = []
    for k in meta["khoang_con"]:
        if not k.get("chia_doi"):
            ds_ci += g.chon_chuoi_trang(doc, f"list/ci/{k['su_kien']}/{k['nhan']}")[0]
    co_ci, _ = g.loc_cohort(sorted({r["id"]: r for r in ds_ci}.values(), key=lambda r: r["id"]), g.WF_CI, meta["T0"], meta["T1"])
    luot, buoc, khong_do, bo_dem, g5 = [], {}, [], {"loi_ich": {"1": 0, "0": 0, "khong_du_du_lieu": 0}, "ton_du": {"1": 0, "0": 0, "khong_du_du_lieu": 0}}, []
    for r in co_ci:
        rid, n = r["id"], int(r.get("run_attempt") or 1)
        dong_tho, du, _, ly = g.chon_chuoi_trang(doc, f"jobs/{rid}")
        if not du:
            khong_do.append({"doi_tuong": f"jobs cua luot {rid}", "ly_do": ly})
            continue
        tao = {1: r.get("created_at")} if n == 1 else {}
        for k in range(1, n + 1) if n > 1 else ():
            b = doc(f"att/{rid}/{k}")
            tao[k] = json.loads(b).get("created_at") if b else None
        lu = g.tinh_luot(r, tao, dong_tho)
        dong = [{"ten": m["ten"], "ket_luan": m["ket_luan"], "run_attempt": m["run_attempt"], "job_id": m["job_id"],
                 "head_sha": m["_tho"].get("head_sha")} for m in lu["dong"]]
        cb = [m for m in lu["dong"] if m["ten_goc"] == JOB_CHUAN_BI]
        gom = [m for m in lu["dong"] if m["ten_goc"] == JOB_GOM]
        log = {"chuan_bi": van_ban(f"log/{cb[-1]['job_id']}") if cb else None,
               "gom": van_ban(f"log/{gom[-1]['job_id']}", doc2) if gom else None}
        art = None
        if doc2 and f"arts/{rid}/p1" in theo_khoa2:
            ds_art, du_art, _, _ = g.chon_chuoi_trang(doc2, f"arts/{rid}")
            art = [a.get("name") for a in ds_art if not a.get("expired")] if du_art else None
        l = dung_luot(r, dong, log, art)
        lan = g.trich_lan(log["chuan_bi"]) if log["chuan_bi"] else None
        for m in lu["dong"]:                                  # thoi gian theo buoc cua gate / gate-ops (dong thuc_thi)
            if m["loai_dong"] == g.THUC_THI and m["ten_goc"] in JOB_BUOC_V2:
                for b in m["_tho"].get("steps") or []:
                    t = g.thoi_luong_buoc(b)
                    if t["trang_thai"] == DO_DUOC:
                        buoc.setdefault(f"{m['ten_goc']} | {m['nen']} | {lan or 'khong_do_duoc'} | {b.get('name')}", []).append(t["gia_tri"])
            if doc2 and m["loai_dong"] == g.THUC_THI and chi_so_manh(m["ten"]) is not None:
                vb = van_ban(f"log/{m['job_id']}", doc2)
                if vb is not None and "G5_THOI_GIAN " in vb:
                    b_g5 = next((g.thoi_luong_buoc(b) for b in m["_tho"].get("steps") or [] if str(b.get("name", "")).startswith("G5 manh")), None)
                    g5.append({"run_id": rid, "job_id": m["job_id"], "manh": chi_so_manh(m["ten"]), "ket_luan": m["ket_luan"],
                               **tong_hop_g5(trich_g5(vb), b_g5["gia_tri"] if b_g5 and b_g5["trang_thai"] == DO_DUOC else None)})
        if l["su_kien"] == "pull_request":
            oracle = None
            if doc2:
                b = doc2(f"oracle/{rid}")
                oracle = json.loads(b).get("oracle") if b else None
            d = dem_bong(l["che_do_chay"], l["bong_phan_loai"], oracle)
            for ten in ("loi_ich", "ton_du"):
                bo_dem[ten]["khong_du_du_lieu" if d[ten] is None else str(d[ten])] += 1
            l["g4a"], (l["g4b"], l["g4b_buoc"]) = quy_g4a(l), quy_g4b(l)
            l["bo_dem"] = d
        luot.append(l)
    pl = {"trang_thai": KHONG_DO_DUOC, "ly_do": "chua thu (can --thu cua bo thu v2 vao --anh-chup-v2)"}
    if doc2 and "list/pl/p1" in theo_khoa2:
        ds_pl, du_pl, _, ly = g.chon_chuoi_trang(doc2, "list/pl")
        tg, thieu_jobs = [], 0
        for r in ds_pl if du_pl else []:
            dong_tho, du, _, _ = g.chon_chuoi_trang(doc2, f"jobs/{r['id']}")
            thieu_jobs += 0 if du else 1
            tg += [x["gia_tri"] for x in (g.khoang_giay(d.get("started_at"), d.get("completed_at")) for d in (dong_tho if du else [])
                                         if d.get("conclusion") != "skipped") if x["trang_thai"] == DO_DUOC]
        pl = ({"trang_thai": DO_DUOC if not thieu_jobs else KHONG_DO_DUOC, "so_luot": len(ds_pl), "so_luot_thieu_jobs": thieu_jobs,
               "giay_job": g.thong_ke(tg, thieu_jobs)} if du_pl else kdd(ly))
    v2 = {"meta": {"packet": "wp1448", "revision": 2, "spec_sha256": SPEC_SHA256, "anh_chup": {k: meta.get(k) for k in ("T0", "T1", "sha_master")},
                   "manifest_sha256": hashlib.sha256((ac / "MANIFEST.json").read_bytes()).hexdigest(),
                   "cohort_goc": bool(cohort_goc), "co_anh_chup_v2": bool(doc2),
                   "nen_sha256": hashlib.sha256((ra / "nen" / "BASELINE.json").read_bytes()).hexdigest(),
                   "BASELINE_goc_sha256": hashlib.sha256(NEN_GOC.read_bytes()).hexdigest()},
          "tai_lap_khoa": doi_chieu_khoa(nen_moi, nen_goc),
          "G4": tong_hop_g4([l for l in luot if l["su_kien"] == "pull_request"]),
          "bong": {"so_luot_co_dong_BONG_CONG_CU": sum(1 for l in luot if l["bong_cong_cu"]),
                   "so_luot_co_dong_BONG_PHAN_LOAI": sum(1 for l in luot if l["bong_phan_loai"]),
                   "BONG_CONG_CU_theo_quyet_dinh": dem([l["bong_cong_cu"]["quyet_dinh"] for l in luot if l["bong_cong_cu"]]),
                   "BONG_CONG_CU_theo_duong_dan": dem([l["bong_cong_cu"].get("duong_dan") for l in luot if l["bong_cong_cu"]]),
                   "bo_dem_pull_request": bo_dem},
          "thoi_gian_buoc_gate_gate_ops": {k: g.thong_ke(v) for k, v in sorted(buoc.items())},
          "g5_thoi_gian": {"so_manh_co_dong": len(g5), "manh": g5} if doc2 else kdd("chua thu log manh G5 (--thu --run-g5 …)"),
          "packet_loop_dot_bien": pl, "khong_do_duoc": khong_do, "luot": luot}
    b = xuat_json(v2)
    (ra / "BASELINE_V2.json").write_bytes(b)
    (ra / "BAO_CAO_V2.md").write_bytes(bao_cao(v2).encode("utf-8"))
    print("BASELINE_V2.json sha256", hashlib.sha256(b).hexdigest())
    for d in v2["tai_lap_khoa"]:
        print(f"  {d['ket_luan']:14} {d['khoa']}")
    return 0


def dem(ds):
    kq = {}
    for x in ds:
        kq[str(x)] = kq.get(str(x), 0) + 1
    return dict(sorted(kq.items()))


def bao_cao(v2):
    g4, dong = v2["G4"], ["# wp1448 r2 — bo thu v2: bao cao tinh lai\n"]
    dong.append(f"Anh chup: T0 {v2['meta']['anh_chup']['T0']} · T1 {v2['meta']['anh_chup']['T1']} · cohort goc: {v2['meta']['cohort_goc']} · "
                f"anh chup v2: {v2['meta']['co_anh_chup_v2']}\n")
    dong.append("## Tai lap khoa cua BASELINE #1434\n\n| khoa | ket luan | tinh lai | BASELINE |\n|---|---|---|---|")
    for d in v2["tai_lap_khoa"]:
        dong.append(f"| `{d['khoa']}` | {d['ket_luan']} | {json.dumps(d['gia_tri_tinh_lai'], ensure_ascii=False)[:80]} | "
                    f"{json.dumps(d['gia_tri_BASELINE'], ensure_ascii=False)[:80]} |")
    dong.append(f"\n## G4 (luot pull_request, attempt cuoi)\n\nSo luot: {g4['so_luot_pull_request']} · mau so: {g4['mau_so']} · "
                f"phu hoan tat: {g4['phu_hoan_tat']} · ti le thieu bang chung: {g4['thieu_bang_chung_ti_le']}\n")
    dong.append("G4a: " + json.dumps(g4["G4a"], ensure_ascii=False) + "\n\nG4b: " + json.dumps(g4["G4b"], ensure_ascii=False)
                + "\n\nG4b theo buoc: " + json.dumps(g4["G4b_theo_buoc"], ensure_ascii=False) + "\n")
    dong.append("## Bong\n\n" + json.dumps(v2["bong"], ensure_ascii=False) + "\n")
    return "\n".join(dong) + "\n"


# ───────────────────────── --thu ─────────────────────────

def lenh_thu(ns):
    g = nap_goc()
    if not os.environ.get("GITHUB_PAT"):
        raise SystemExit("thieu bien moi truong GITHUB_PAT")
    ac = pathlib.Path(ns.anh_chup).resolve()
    doc, _ = doc_anh_chup(ac)
    if doc is None:
        raise SystemExit("anh chup #1434 chua dong MANIFEST")
    meta = json.loads((ac / "META.json").read_bytes())
    t = g.Thu(ns.ra, ns.han_giay, ns.so_luong)
    if t.ra == ac or ac in t.ra.parents:
        raise SystemExit("anh chup v2 phai la thu muc RIENG, khong nam trong anh chup #1434")
    g.ghi_tep(t.ra, "META.json", xuat_json({"packet": "wp1448", "revision": 2, "anh_chup_goc": {k: meta.get(k) for k in ("T0", "T1", "sha_master")}}))
    run_g5 = {int(x) for x in (ns.run_g5 or "").split(",") if x.strip().isdigit()}
    ds_ci = []
    for k in meta["khoang_con"]:
        if not k.get("chia_doi"):
            ds_ci += g.chon_chuoi_trang(doc, f"list/ci/{k['su_kien']}/{k['nhan']}")[0]
    co_ci, _ = g.loc_cohort(sorted({r["id"]: r for r in ds_ci}.values(), key=lambda r: r["id"]), g.WF_CI, meta["T0"], meta["T1"])
    viec, oracle = [], []
    for r in co_ci:
        rid = r["id"]
        dong, du, _, _ = g.chon_chuoi_trang(doc, f"jobs/{rid}")
        if not du:
            continue
        cuoi = {}
        for d in sorted(dong, key=lambda d: (int(d.get("run_attempt") or 1), d.get("id") or 0)):
            cuoi[d.get("name")] = d
        for ten, d in cuoi.items():
            la_gom = (ten or "").startswith(JOB_GOM + " (ubuntu-latest") and d.get("conclusion") not in ("skipped", None)
            la_manh = rid in run_g5 and chi_so_manh(ten) is not None and d.get("conclusion") != "skipped"
            if la_gom or la_manh:
                viec.append(lambda j=d["id"]: t.lay(f"log/{j}", f"actions/jobs/{j}/logs", f"log/{j}.log", "log"))
            if ns.kho and ten == JOB_CHUAN_BI and r.get("event") == "pull_request":
                b = doc(f"log/{d['id']}")
                pl = trich_bong(b.decode("utf-8", errors="replace"))["bong_phan_loai"] if b else None
                if pl:
                    oracle.append((rid, pl))
        if r.get("event") == "pull_request":
            viec.append(lambda rid=rid: t.trang(f"arts/{rid}", f"actions/runs/{rid}/artifacts", f"arts/{rid}", "artifacts", "artifacts"))
    ds_pl, _, _ = t.trang("list/pl", f"actions/workflows/{WF_PL}/runs?created={meta['T0']}..{meta['T1']}", "list/pl", "list", "workflow_runs")
    viec += [lambda rid=r["id"]: t.trang(f"jobs/{rid}", f"actions/runs/{rid}/jobs?filter=all", f"jobs/{rid}", "jobs", "jobs") for r in ds_pl]
    t.song_song(viec)
    muc_oracle = []
    for rid, pl in oracle:                                   # git CHI DOC tren --kho; khong mang
        kq = oracle_moi(ns.kho, pl.get("goc_su_kien"), pl.get("goc_so"), pl.get("dau"))
        b = xuat_json({"run_id": rid, "oracle": kq, "oid": {k: pl.get(k) for k in ("goc_su_kien", "goc_so", "dau", "hop")}})
        g.ghi_tep(t.ra, f"oracle/{rid}.json", b)
        muc_oracle.append({"khoa": f"oracle/{rid}", "loai": "oracle", "url": None, "http": None, "duong_dan": f"oracle/{rid}.json",
                           "sha256": g.sha256_bytes(b), "kich_thuoc": len(b)})
    t.f_nk.close()
    g.dong_manifest(t.ra, list(t.muc.values()) + muc_oracle)
    t.nk.unlink()
    return 0


# ───────────────────────── --tu-kiem ─────────────────────────

class TuKiemDo(AssertionError):
    """Chi `bang()` cua --tu-kiem nem lop nay: loi vo can trong ma bi dot bien di ra duoi TEN THAT (khong tinh la bat duoc)."""


def bang(dieu_kien, nhan):
    if not dieu_kien:
        raise TuKiemDo(nhan)


def cac_ca_tu_kiem():
    F = DAY / "fixtures"
    J = lambda t: json.loads((F / t).read_text(encoding="utf-8"))
    ca = []

    def kiem(f):
        ca.append(f)
        return f

    @kiem
    def g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc():
        thay = set()
        for tep in sorted((F / "g4b").glob("*.json")):
            fx = J(f"g4b/{tep.name}")
            l = dung_luot(fx["run"], fx["dong"], fx.get("log"), fx.get("artifact"))
            l.update(fx.get("ghi_de") or {})
            loai, buoc = quy_g4b(l)
            bang([loai, buoc] == fx["mong"]["g4b"], f"{tep.name}: G4b mong {fx['mong']['g4b']}, duoc {[loai, buoc]}")
            bang(quy_g4a(l) == fx["mong"]["g4a"] or buoc < 2, f"{tep.name}: G4a mong {fx['mong']['g4a']}, duoc {quy_g4a(l)}")
            bang(buoc == int(tep.name[1:3]), f"{tep.name}: ten tep khai buoc {tep.name[1:3]}, quy ra buoc {buoc}")
            thay.add(buoc)
        bang(thay == set(range(11)), f"fixture phai phu DU muoi buoc 0..10 cua phep quy, thay {sorted(thay)}")

    @kiem
    def g4b_bon_fixture_bat_buoc_cua_dac_ta():
        def quy(ten):
            fx = J(f"g4b/{ten}")
            l = dung_luot(fx["run"], fx["dong"], fx.get("log"), fx.get("artifact"))
            l.update(fx.get("ghi_de") or {})
            return fx, l, quy_g4b(l)
        fx, l, kq = quy("b08_run_44126854175_tam_manh_cancelled.json")
        bang(fx["run"]["id"] == 44126854175 and l["manh"]["ket_luan"] == ["cancelled"] * 8 and kq[0] != "du_hoan_tat" and kq == ("dang_do", 8),
             f"luot 44126854175 (8 manh cancelled) KHONG duoc ra du_hoan_tat: {kq}")
        fx, l, kq = quy("b03_ca_duong_pr4_mo_phong.json")
        bang(fx["mo_phong"] is True and l["lan_cu"] == DAY_DU and l["che_do_chay"] == DUONG_NHANH and kq == ("duong_nhanh_co_bang_chung", 3)
             and quy_g4a(l) == "duong_nhanh_dang_chay" and quy_g4a(l) != "bo_moi", f"ca duong PR4 phai ra duong_nhanh_co_bang_chung, khong tinh bo moi: {kq}")
        fx, l, kq = quy("b07_run_44443875641_du_bien_nhan_gom_cancelled.json")
        bang(fx["run"]["id"] == 44443875641 and l["manh"]["bien_nhan_hop_le"] == 8 and l["gom"]["ket_luan"] == "cancelled" and kq == ("gom_hong", 7),
             f"luot 44443875641 (du 8 bien nhan, gom cancelled) phai ra gom_hong: {kq}")
        fx, l, kq = quy("b07_chon_bo_gom_cancelled.json")
        bang(che_do_chon(l) in ("bo_dn", "bo_moi") and l["gom"]["ket_luan"] == "cancelled" and kq == ("gom_hong", 7), f"chon bo + gom cancelled phai ra gom_hong: {kq}")

    @kiem
    def g4_tong_hop_mau_so_va_tran():
        ds = []
        for tep in sorted((F / "g4b").glob("*.json")):
            fx = J(f"g4b/{tep.name}")
            l = dung_luot(fx["run"], fx["dong"], fx.get("log"), fx.get("artifact"))
            l.update(fx.get("ghi_de") or {})
            ds.append(l)
        t = tong_hop_g4(ds)
        ngoai = t["G4b_theo_buoc"]["0"] + t["G4b_theo_buoc"]["1"]
        bang(t["mau_so"] == len(ds) - ngoai and ngoai >= 2 and sum(t["G4b"].values()) == len(ds) and sum(t["G4a"].values()) == t["mau_so"],
             f"moi luot dung mot loai; buoc 0-1 ngoai mau so: {t}")
        thieu = sum(t["G4b_theo_buoc"][b] for b in ("2", "9", "10"))
        bang(t["G4b"]["thieu_bang_chung"] == thieu and t["thieu_bang_chung_ti_le"] == round(thieu / t["mau_so"], 4), f"tran tinh tren buoc 2, 9, 10: {t}")
        bang(t["phu_hoan_tat"] == t["G4b_theo_buoc"]["5"] + t["G4b_theo_buoc"]["6"], "chi buoc 5 va 6 la phu hoan tat")
        bang(t["G4a"]["bo_moi"] == sum(1 for l in ds if quy_g4b(l)[1] >= 2 and che_do_chon(l) == "bo_moi") and t["G4a"]["duong_nhanh_dang_chay"] >= 1,
             "bo moi chi dem luot day_du co cong_cu=bo_qua; duong nhanh dang chay dem rieng")

    @kiem
    def bong_hai_bo_dem_tach_rieng():
        fx = J("bong.json")
        for ca_ in fx["ca"]:
            tb = trich_bong(ca_["log"])
            d = dem_bong(tb["che_do_chay"], tb["bong_phan_loai"], ca_["oracle"])
            bang([d["loi_ich"], d["ton_du"]] == ca_["mong"], f"{ca_['ten']}: mong [loi ich, ton du] = {ca_['mong']}, duoc {[d['loi_ich'], d['ton_du']]}")
            bang((tb["bong_cong_cu"] or {}).get("quyet_dinh") == ca_.get("cong_cu"), f"{ca_['ten']}: quyet dinh BONG_CONG_CU doc sai: {tb['bong_cong_cu']}")
        ten = {c["ten"]: c for c in fx["ca"]}
        bang(ten["ca duong PR4 o PR1 (tich hop bong that)"]["mong"] == [1, 1] and ten["MO PHONG sau PR4 (phan loai dang chay = moi)"]["mong"] == [1, 0],
             "ca duong PR4: o PR1 loi ich=1/ton du=1; mo phong sau PR4 loi ich=1/ton du=0")

    @kiem
    def g5_hop_khac_tong_va_ba_thanh_phan():
        bang(hop_khoang([(0, 10), (5, 15), (20, 25)]) == 20.0 and hop_khoang([]) == 0.0, "hop cua cac khoang chong nhau khong phai tong")
        vb = (F / "log_manh_g5.log").read_text(encoding="utf-8")
        bg = trich_g5(vb)
        t = tong_hop_g5(bg, 40)
        bang(len(bg) == 7 and t["so_dot_bien"] == 3 and t["so_du_ba_thanh_phan"] == 2 and t["so_thieu"] == 1 and t["ten_thieu"] == ["db_thieu"],
             f"ba dot bien, mot thieu thanh phan: {t}")
        dc = t["doi_chieu"]
        bang(dc["trang_thai"] == DO_DUOC and dc["hop_con_s"] == 20.0 and dc["tong_con_s"] == 25.0 and dc["khong_phan_bo_s"] == 20.0
             and dc["trong_10_phan_tram"] is False, f"doi chieu bang HOP, phan lech la khong phan bo: {dc}")
        gan = tong_hop_g5(bg, 21)["doi_chieu"]
        bang(gan["trong_10_phan_tram"] is True and gan["khong_phan_bo_s"] == 1.0, f"lech duoi 10 % thi dat: {gan}")
        bang(tong_hop_g5([b for b in bg if b.get("loai") != "con"], 40)["doi_chieu"]["trang_thai"] == KHONG_DO_DUOC, "khong co khoang con => khong_do_duoc")
        bang(trich_g5("G5_THOI_GIAN {hong}\n")[0]["trang_thai"] == KHONG_DO_DUOC, "dong hong => ban ghi khong_do_duoc")

    @kiem
    def gom_dau_hieu_duong_theo_ly_do():
        bang(trich_gom("2026-11-01T00:00:00.0Z GOM MẢNH 8/8\n") == "gom_manh:8", "gom that")
        bang(trich_gom("GOM: KHÔNG ĐO — PR chỉ đổi hồ sơ (CONG_CU_TEST_GOP_CHE_DO=duong_nhanh, 0 mảnh); 490 đột biến\n") == "khong_do:duong_nhanh", "dau duong nhanh")
        bang(trich_gom("GOM: KHÔNG ĐO — diff ngoài bao đóng (cong_cu=bo_qua)\n") == "khong_do:bo_moi", "dau bo moi")
        bang(trich_gom("GOM: KHÔNG ĐO — ly do khac\n") == "khong_do:la" and trich_gom("khong co gi\n") is None, "dau la / vang")

    @kiem
    def tai_lap_khoa_ba_trang_thai():
        a = {"M2": {"so_luot": 5, "theo_lan": {"day_du": 3}}, "top5_giay_thuc_thi": [{"so_dong_thuc_thi": 7, "tong_giay_thuc_thi": 9}]}
        b = json.loads(json.dumps(a))
        b["M2"]["so_luot"] = 6
        kq = {d["khoa"]: d["ket_luan"] for d in doi_chieu_khoa(a, b)}
        bang(kq["M2.so_luot"] == "lech" and kq["M2.theo_lan"] == "khop" and kq["[DX-2] top5_giay_thuc_thi[0].so_dong_thuc_thi"] == "khop"
             and kq["M1.muc_ket_qua_theo_khoa.so_khoa"] == KHONG_DO_DUOC, f"khop / lech / khong_do_duoc: {kq}")
        a["M3"] = {"bang": {"ops/cong_cu_test.py": {"_tep": {"trang_thai": KHONG_DO_DUOC, "ly_do": "nguon hong"}}}}
        b["M3"] = {"bang": {"ops/cong_cu_test.py": {"CA": 61}}}
        kq = {d["khoa"]: d["ket_luan"] for d in doi_chieu_khoa(a, b)}
        bang(kq["M3.bang[ops/cong_cu_test.py]"] == KHONG_DO_DUOC, f"nguon cua bang khong do duoc thi KHONG goi la lech: {kq}")

    return ca


# Dot bien tren BAN SAO cua chinh tep nay: (ten, chuoi cu, chuoi moi, ca phai DO). Mot dot bien cho TUNG buoc cua phep quy G4b.
DOT_BIEN_TU_KIEM = (
    ("g4b_bo_buoc_0", '        return "huy_truoc_phan_loai", 0\n', '        pass\n', "g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc"),
    ("g4b_bo_buoc_1", '        return "ngoai_mau_so", 1\n', '        pass\n', "g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc"),
    ("g4b_bo_buoc_2", '    if chon is None:\n        return "thieu_bang_chung", 2\n', '', "g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc"),
    ("g4b_bo_buoc_3", '        return "duong_nhanh_co_bang_chung", 3\n', '        pass\n', "g4b_bon_fixture_bat_buoc_cua_dac_ta"),
    ("g4b_bo_buoc_4", '        return "bo_moi_co_bang_chung", 4\n', '        pass\n', "g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc"),
    ("g4b_bo_buoc_5", '        return "du_hoan_tat", 5\n', '        pass\n', "g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc"),
    ("g4b_bo_buoc_6", '        return "dich_hoan_tat", 6\n', '        pass\n', "g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc"),
    ("g4b_bo_buoc_7", '        return "gom_hong", 7\n', '        pass\n', "g4b_bon_fixture_bat_buoc_cua_dac_ta"),
    ("g4b_bo_buoc_8", '        return "dang_do", 8\n', '        pass\n', "g4b_bon_fixture_bat_buoc_cua_dac_ta"),
    ("g4b_bo_buoc_9", '    if kl_gom == "success":\n        return "thieu_bang_chung", 9\n', '', "g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc"),
    ("g4b_buoc_10_thanh_hoan_tat", '    return "thieu_bang_chung", 10\n', '    return "du_hoan_tat", 5\n', "g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc"),
    ("g4b_tam_manh_cancelled_thanh_hoan_tat", '    if chon == "du" and du_bien_nhan and kl_gom == "success":\n', '    if chon == "du":\n', "g4b_bon_fixture_bat_buoc_cua_dac_ta"),
    ("g4b_gom_cancelled_van_hoan_tat", '    if chon == "du" and du_bien_nhan and kl_gom == "success":\n', '    if chon == "du" and du_bien_nhan:\n', "g4b_bon_fixture_bat_buoc_cua_dac_ta"),
    ("g4a_duong_nhanh_tinh_la_bo_moi", '{"bo_dn": "duong_nhanh_dang_chay", "bo_moi": "bo_moi"', '{"bo_dn": "bo_moi", "bo_moi": "bo_moi"', "g4b_bon_fixture_bat_buoc_cua_dac_ta"),
    ("g4_mau_so_gom_buoc_0_1", "    mau = sum(n for b, n in theo_buoc.items() if int(b) >= 2)\n", "    mau = sum(theo_buoc.values())\n", "g4_tong_hop_mau_so_va_tran"),
    ("bong_dem_loi_ich_bang_ton_du", '    return {"loi_ich": loi_ich, "ton_du": ton_du}\n', '    return {"loi_ich": ton_du, "ton_du": ton_du}\n', "bong_hai_bo_dem_tach_rieng"),
    ("bong_ton_du_so_voi_cu", "    ton_du = int(che_do_chay != oracle)", '    ton_du = int(pl.get("cu") != oracle)', "bong_hai_bo_dem_tach_rieng"),
    ("g5_hop_thanh_tong", "        elif b > cuoi:\n            tong, cuoi = tong + (b - cuoi), b\n    return tong\n\n\ndef trich_g5",
     "        else:\n            tong, cuoi = tong + (b - a), max(b, cuoi)\n    return tong\n\n\ndef trich_g5", "g5_hop_khac_tong_va_ba_thanh_phan"),
    ("g5_thieu_thanh_phan_van_du", 'all(so(b.get(k)) for k in ("dung_cay_s", "ca_dich_s", "ca_khac_s"))', 'all(so(b.get(k)) for k in ("dung_cay_s", "ca_khac_s"))',
     "g5_hop_khac_tong_va_ba_thanh_phan"),
    ("gom_dau_la_thanh_duong_nhanh", '            dau = "khong_do:" + (khop[0] if len(khop) == 1 else "la")\n', '            dau = "khong_do:duong_nhanh"\n', "gom_dau_hieu_duong_theo_ly_do"),
)


def chay_ca(ten=None):
    """[(ten ca, 'DAT' | 'DO' | 'HONG', chi tiet)]."""
    kq = []
    for f in cac_ca_tu_kiem():
        if ten and f.__name__ != ten:
            continue
        try:
            f()
            kq.append((f.__name__, "DAT", ""))
        except TuKiemDo as e:
            kq.append((f.__name__, "DO", str(e)))
        except Exception as e:  # noqa: BLE001
            kq.append((f.__name__, "HONG", f"{type(e).__name__}: {e}"))
    return kq


def lenh_tu_kiem(ns):
    if ns.mot_ca:                                            # cua tien trinh con cua dot bien: rc 3 = DO dung ca, 4 = loi vo can
        kq = chay_ca(ns.mot_ca)
        if len(kq) != 1:
            print("HONG: khong co ca", ns.mot_ca)
            return 4
        print(f"{kq[0][1]}:{kq[0][0]}:{kq[0][2]}")
        return {"DAT": 0, "DO": 3}.get(kq[0][1], 4)
    kq = chay_ca()
    for ten, tt, ct in kq:
        if tt != "DAT":
            print(f"  {tt} {ten}: {ct}")
    dat = sum(1 for _, tt, _ in kq if tt == "DAT")
    print(f"CA: {dat}/{len(kq)} dat")
    nguon = pathlib.Path(__file__).read_text(encoding="utf-8")
    ma = nguon.split("\n# Dot bien tren BAN SAO cua chinh tep nay", 1)[0]     # neo chi tinh trong MA, khong tinh trong chinh bang nay
    giet, xau = 0, []
    for ten, cu, moi, dich in DOT_BIEN_TU_KIEM:
        if ma.count(cu) != 1 or cu == moi:
            xau.append(f"{ten}: neo phai xuat hien DUNG MOT lan trong ma (thay {ma.count(cu)})")
            continue
        with tempfile.TemporaryDirectory(prefix="wp1448_tk_") as d:
            ban = pathlib.Path(d) / "do"
            shutil.copytree(DAY, ban, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            (ban / "thu_thap.py").write_text(nguon.replace(cu, moi, 1), encoding="utf-8", newline="\n")
            r = subprocess.run([sys.executable, "-B", str(ban / "thu_thap.py"), "--tu-kiem", "--mot-ca", dich], capture_output=True, text=True, timeout=120)
        if r.returncode == 3 and f"DO:{dich}:" in r.stdout:
            giet += 1
        else:
            xau.append(f"{ten}: {'SONG SOT' if r.returncode == 0 else 'TIN DUNG GIA (rc=%d)' % r.returncode}: {(r.stdout + r.stderr).strip()[-200:]}")
    for x in xau:
        print("  XAU", x)
    print(f"DOT BIEN (tren ban sao): {giet}/{len(DOT_BIEN_TU_KIEM)} bi bat dung ca")
    tot = bool(kq) and dat == len(kq) and giet == len(DOT_BIEN_TU_KIEM) > 0
    print("TONG:", "DAT" if tot else "DO")
    return 0 if tot else 1


def main():
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="backslashreplace")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    for co in ("--thu", "--tinh", "--tu-kiem"):
        ap.add_argument(co, action="store_true")
    for co in ("--ra", "--anh-chup", "--anh-chup-v2", "--cohort-goc", "--run-g5", "--kho", "--mot-ca"):
        ap.add_argument(co)
    ap.add_argument("--han-giay", type=int, default=3600)
    ap.add_argument("--so-luong", type=int, default=6)
    ns = ap.parse_args()
    if sum((ns.thu, ns.tinh, ns.tu_kiem)) != 1:
        ap.error("chon DUNG MOT trong --thu | --tinh | --tu-kiem")
    if ns.tu_kiem:
        return lenh_tu_kiem(ns)
    if not (ns.anh_chup and ns.ra):
        ap.error("--thu va --tinh can --anh-chup <anh chup #1434> --ra <thu muc>")
    return lenh_thu(ns) if ns.thu else lenh_tinh(ns)


if __name__ == "__main__":
    sys.exit(main())
