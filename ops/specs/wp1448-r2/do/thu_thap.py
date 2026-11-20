#!/usr/bin/env python3
"""wp1448 r2 — bo thu v2 (dac ta ops/specs/wp1448-r2/SPEC.md muc 5), CHI DOC. Ke thua hop dong cua bo thu #1434
(`ops/specs/wp1434-r3/do/thu_thap.py`, nap bang duong dan, KHONG sua): anh chup NGOAI kho, ba che do, ba trang thai,
ghi co gioi han, `--tinh` tat dinh va khong goi git.

  --thu --anh-chup <anh chup #1434> --ra <anh chup v2> [--run-g5 id,id] [--kho <kho git>]
        GitHub REST GET -> them vao MOT thu muc anh chup v2 RIENG (khong ghi vao anh chup #1434): log job gom cong cu, danh
        sach artifact, NOI DUNG bien nhan manh G5 (zip artifact con han) + commit cua head bien nhan, luot + job cua
        `packet-loop-dot-bien.yml`, log manh G5 cua cac luot neu ten o `--run-g5`; co `--kho` thi tinh oracle ngu canh moi tu
        bon OID (git CHI DOC tren kho ay) va luu vao anh chup v2.
  --tinh --anh-chup <anh chup #1434> --ra <thu muc> [--anh-chup-v2 <anh chup v2>] [--cohort-goc <COHORT.json>]
        thuan offline -> nen/ (BASELINE.json cua bo thu #1434 tren cung anh chup), BASELINE_V2.json, BAO_CAO_V2.md. Moi anh chup
        da chi dinh phai khop MANIFEST tung byte (lech/vang tep => rc 3, truoc moi tinh toan).
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
# wp1448 r2 lan 2 (review F1): BIEN NHAN MANH la NOI DUNG tep `manh-<k>.txt` trong artifact `TEN_ART_MANH` (hop dong
# `_ket_thuc_manh`/`_gom_manh` cua `ops/cong_cu_test.py`), KHONG phai ket luan job. Job `success` hay ten artifact chi la
# bang chung VANG MAT (job do/huy, artifact vang => thieu), khong bao gio la bang chung CO.
TEN_ART_MANH = JOB_MANH + "-manh-ubuntu-latest-"
KHOA_DAU_MANH = frozenset({"phien_ban", "manh", "so_manh", "sha256_test", "head"})   # + `che_do` tuy chon (vang = `du`)
CHE_DO_G5 = ("du", "dich")
BN_HOP_LE, BN_HONG, BN_THIEU = "hop_le", "khong_hop_le", "thieu"                    # + KHONG_DO_DUOC: ba trang thai + thieu
RE_SHA256, RE_HEAD = re.compile(r"[0-9a-f]{64}"), re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")


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
    # review F3: chi dem phan loai DO DUOC. `cu_do` = phan loai dang chay co phai fail-close khong (dong bong ghi); `kiem_moi`
    # khong do duoc nghia la ngu canh moi chua kiem xong. Vang `cu_do` (dong la) cung la khong du du lieu, khong doan.
    cu_do = pl.get("cu_do") == DO_DUOC
    moi_do = pl.get("kiem_moi") != KHONG_DO_DUOC
    loi_ich = int(pl["cu"] != pl["moi"]) if cu_do and moi_do and pl.get("cu") in hop_le and pl.get("moi") in hop_le else None
    ton_du = int(che_do_chay != oracle) if che_do_chay in hop_le and oracle in hop_le and cu_do else None
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


def kiem_bien_nhan(noi_dung, k, so_manh=SO_MANH_G5):
    """MOT tep manh (byte) -> (trang thai, ly do | None, {che_do, head, sha256_test, ten} | None). Ham THUAN, cung hop dong voi
    `_gom_manh` cua bo ca: dong dau `MANH <JSON>` dung bo khoa, kieu so nguyen, phien ban 1, chi so + so manh khop, van tay dung
    mau; than CHI gom dong `BKCON <mang JSON>` mang ten dot bien (chuoi) o vi tri 1, khong rong, khong trung ten."""
    try:
        dong0, _, than = bytes(noi_dung).decode("utf-8").partition("\n")
        if not dong0.startswith("MANH "):
            return BN_HONG, "thieu_dong_MANH", None
        dau = json.loads(dong0[5:])
    except (TypeError, UnicodeDecodeError, ValueError):
        return BN_HONG, "dau_khong_doc_duoc", None
    if not isinstance(dau, dict) or set(dau) - {"che_do"} != KHOA_DAU_MANH:
        return BN_HONG, "khoa_dau_la", None
    if any(type(dau[x]) is not int for x in ("phien_ban", "manh", "so_manh")) or dau["phien_ban"] != 1:
        return BN_HONG, "phien_ban_la", None
    if dau["manh"] != k or dau["so_manh"] != so_manh:
        return BN_HONG, "sai_chi_so_manh", None
    che_do = dau.get("che_do", "du")
    if che_do not in CHE_DO_G5:
        return BN_HONG, "che_do_la", None
    if not (type(dau["sha256_test"]) is str and RE_SHA256.fullmatch(dau["sha256_test"])
            and type(dau["head"]) is str and RE_HEAD.fullmatch(dau["head"])):
        return BN_HONG, "van_tay_la", None
    ten = []
    for d in than.split("\n"):
        if not d:
            continue
        if not d.startswith("BKCON "):
            return BN_HONG, "dong_ngoai_hop_dong", None
        try:
            bg = json.loads(d[6:])
        except ValueError:
            return BN_HONG, "bkcon_hong", None
        if not isinstance(bg, list) or len(bg) < 2 or type(bg[1]) is not str:
            return BN_HONG, "bkcon_hong", None
        ten.append(bg[1])
    if not ten or len(set(ten)) != len(ten):
        return BN_HONG, "ten_rong_hoac_trung", None
    return BN_HOP_LE, None, {"che_do": che_do, "head": dau["head"], "sha256_test": dau["sha256_test"], "ten": ten}


def bien_nhan_luot(manh_job, artifact, noi_dung, head_run, hop=None, cmt=None):
    """Trang thai TUNG bien nhan manh va ket luan cua ca bo. Ham THUAN.

    `manh_job`: {k: dong job} (attempt cuoi, mang sang) · `artifact`: {k: 'co' | 'het_han'} cua danh sach artifact DA DU, hoac
    None = khong co danh sach · `noi_dung`: {k: byte tep manh} (vang = chua lay duoc) · `hop`: merge ref (`github.sha`) tu dong
    bong, hoac None · `cmt`: {sha: [cha...]} cua head bien nhan (REST, --thu). Moi manh dung MOT trang thai:
      hop_le        noi dung dung hop dong VA head doi chieu duoc voi LUOT (= hop, hoac cha hai cua no = head cua luot);
      khong_hop_le  noi dung hong / sai head / sai bo; job mang head khac luot;
      thieu         danh sach artifact da du ma vang tep; hoac khong co danh sach va job khong `success` (khong buoc upload nao chay);
      khong_do_duoc moi truong hop con lai (het han, chua tai, head chua doi chieu) — KHONG suy tu job `success`.
    Tra {trang_thai, ly_do, du_noi_dung, che_do, thieu}: `du_noi_dung` chi khi CA tam manh hop_le, cung head/van tay/che do, ten
    roi nhau va moi manh dung so dong cua phan hoach `i % 8 == k`."""
    tt, ly, gt = [KHONG_DO_DUOC] * SO_MANH_G5, ["-"] * SO_MANH_G5, {}
    for k in range(SO_MANH_G5):
        d, nd = manh_job.get(k), (noi_dung or {}).get(k)
        art = None if artifact is None else artifact.get(k, "vang")
        if d is not None and d.get("head_sha") not in (None, head_run):
            tt[k], ly[k] = BN_HONG, "job_mang_head_khac_luot"
        elif isinstance(nd, (bytes, bytearray)):
            tt[k], ly[k], g = kiem_bien_nhan(nd, k)
            if g is not None:
                cha = (cmt or {}).get(g["head"])
                dinh_danh = (g["head"] == hop) if hop else (len(cha) == 2 and cha[1] == head_run) if isinstance(cha, list) else None
                if dinh_danh is False:
                    tt[k], ly[k] = BN_HONG, "head_bien_nhan_khong_khop_luot"
                elif dinh_danh is None:
                    tt[k], ly[k] = KHONG_DO_DUOC, "head_bien_nhan_chua_doi_chieu_duoc"
                else:
                    gt[k] = g
        elif art == "vang":
            tt[k], ly[k] = BN_THIEU, "artifact_vang"
        elif art is None and (d is None or d.get("ket_luan") != "success"):
            tt[k], ly[k] = BN_THIEU, "job_khong_success"
        else:
            tt[k], ly[k] = KHONG_DO_DUOC, "artifact_het_han" if art == "het_han" else "noi_dung_chua_lay"
    che_do = None
    if len(gt) == SO_MANH_G5:
        ten = [t for k in range(SO_MANH_G5) for t in gt[k]["ten"]]
        bo = {(g["head"], g["sha256_test"], g["che_do"]) for g in gt.values()}
        if len(bo) != 1:
            tt, ly = [BN_HONG] * SO_MANH_G5, ["bo_bien_nhan_lech_head_van_tay_che_do"] * SO_MANH_G5
        elif len(set(ten)) != len(ten) or any(len(gt[k]["ten"]) != len(range(k, len(ten), SO_MANH_G5)) for k in range(SO_MANH_G5)):
            tt, ly = [BN_HONG] * SO_MANH_G5, ["bo_bien_nhan_lech_phan_hoach"] * SO_MANH_G5
        else:
            che_do = bo.pop()[2]
    du = che_do is not None and all(x == BN_HOP_LE for x in tt)
    return {"trang_thai": tt, "ly_do": ly, "du_noi_dung": du, "che_do": che_do if du else None,
            "thieu": any(x in (BN_HONG, BN_THIEU) for x in tt)}


def dung_luot(run, dong, log=None, artifact=None, bien_nhan=None, cmt=None):
    """Ban ghi CHUAN HOA cua mot luot ci.yml o attempt CUOI, tu: `run` (API), `dong` (dong job: ten, ket_luan, run_attempt,
    head_sha, job_id — moi attempt), `log` ({'chuan_bi': van ban | None, 'gom': van ban | None}), `artifact` (danh sach artifact
    DA DU: ten (chuoi) hoac {name, expired}; None = khong co danh sach), `bien_nhan` ({k: byte tep manh}) va `cmt` ({sha: [cha]}).
    Dong cua attempt cuoi duoc uu tien; job khong chay lai o attempt cuoi lay dong moi nhat cua no (mang sang)."""
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
    art = None
    if artifact is not None:
        art = {}
        for a in artifact:
            ten, het = (a, False) if isinstance(a, str) else (a.get("name"), bool(a.get("expired")))
            if isinstance(ten, str) and ten.startswith(TEN_ART_MANH) and ten[len(TEN_ART_MANH):].isdigit():
                k = int(ten[len(TEN_ART_MANH):])
                art[k] = "co" if not het or art.get(k) == "co" else "het_han"
    hop = pl.get("hop") if isinstance(pl.get("hop"), str) and RE_OID.fullmatch(pl.get("hop")) else None
    bn = bien_nhan_luot(manh, art, bien_nhan, head, hop, cmt)
    return {"run_id": run.get("id"), "attempt": so_att, "su_kien": run.get("event"), "head": head, "ket_luan": run.get("conclusion"),
            "chuan_bi": cb.get("ket_luan") if cb else None, "co_log_chuan_bi": isinstance(log.get("chuan_bi"), str),
            "lan_cu": lan_cu, "che_do_chay": tb["che_do_chay"], "cong_cu_that": tb["cong_cu_that"],
            "bong_cong_cu": tb["bong_cong_cu"], "bong_phan_loai": tb["bong_phan_loai"],
            "che_do_g5": "du",                                      # `dich` chi co tu PR6; bien nhan khi ay phai mang truong che do
            "gom": {"ket_luan": gom.get("ket_luan") if gom else None, "dau": trich_gom(log["gom"]) if isinstance(log.get("gom"), str) else None,
                    "co_log": isinstance(log.get("gom"), str)},
            "manh": {"ket_luan": [manh[k].get("ket_luan") if k in manh else None for k in range(SO_MANH_G5)],
                     "bien_nhan": bn["trang_thai"], "ly_do": bn["ly_do"], "du_noi_dung": bn["du_noi_dung"],
                     "che_do_bien_nhan": bn["che_do"], "thieu": bn["thieu"],
                     "nguon_bien_nhan": ("noi_dung" if bien_nhan else "khong_co_noi_dung") + ("+danh_sach_artifact" if art is not None else "")}}


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


def du_bien_nhan(l, che_do):
    """Du 8 bien nhan hop le cua CHE DO `che_do`, co BANG CHUNG DUONG (review F1): (a) noi dung tung tep da kiem (`du_noi_dung`)
    dung che do; hoac (b) che do `du` va job gom `success` in `GOM MẢNH 8/8` — job gom dung lai phan hoach day du va kiem tung
    tep (head, van tay, ban ghi) cua CHINH luot (`_gom_manh`). Mot bien nhan da biet thieu/hong thi KHONG du, ke ca khi gom noi
    8/8 (mau thuan => thieu bang chung). Job `success` hay ten artifact KHONG BAO GIO la bang chung co."""
    gom, manh = l.get("gom") or {}, l.get("manh") or {}
    if manh.get("thieu") is not False:
        return False
    if manh.get("du_noi_dung") is True and manh.get("che_do_bien_nhan") == che_do:
        return True
    return che_do == "du" and gom.get("ket_luan") == "success" and gom.get("dau") == f"gom_manh:{SO_MANH_G5}"


def quy_g4b(l):
    """(loai, buoc) — phep quy G4b CO THU TU va VET CAN cua muc 3 ke hoach nguon r3: xet tu buoc 0, buoc DAU TIEN khop quyet
    dinh; buoc 10 nhan moi thu con lai. Buoc 0 va 1 dua luot ra NGOAI mau so."""
    gom, manh, chon = l.get("gom") or {}, l.get("manh") or {}, che_do_chon(l)
    kl_gom, dau = gom.get("ket_luan"), gom.get("dau")
    du_bn = chon in CHE_DO_G5 and du_bien_nhan(l, chon)
    dau_khop = dau in (None, f"gom_manh:{SO_MANH_G5}")             # che do du/dich: dau "KHONG DO" hay so manh khac = mau thuan
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
    if chon == "du" and du_bn and kl_gom == "success" and dau_khop:
        return "du_hoan_tat", 5
    if chon == "dich" and du_bn and kl_gom == "success" and dau_khop:
        return "dich_hoan_tat", 6
    if kl_gom != "success" and (chon in ("bo_dn", "bo_moi") or du_bn):
        return "gom_hong", 7
    if chon in CHE_DO_G5 and kl_gom != "success" and manh.get("thieu") is True and bi_huy_do:
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


def oracle_moi(kho, goc_su_kien, goc_so, dau, hop, chay=subprocess.run):
    """Phan loai theo NGU CANH MOI, tinh lai DOC LAP tu BON OID (goc su kien, cha thu nhat, head, merge ref `hop`) — khong goi
    `ops/ci_duong_nhanh.py`, khong tin `goc_so` cua dong bong (review F2). Tu dan xuat cha cua `hop`: DUNG hai cha, cha hai =
    `dau`; `goc_so` (khi dong bong ghi) phai bang cha mot; goc su kien phai la to tien cua cha mot; cha mot va `dau` co DUNG mot
    merge-base. Tap ban ghi = ba cham ∪ diff cha mot -> cay merge MO PHONG ∪ diff cha mot -> merge THAT (`hop`). Mot duong dan
    ngoai bon tien to ho so, ma cap nong, mode moi thuc thi/symlink/gitlink, doi mode, hay sua/xoa dac ta da co => `day_du`;
    khong con gi => `duong_nhanh`. Sai mot dieu kien, thieu object, git loi => `khong_do_duoc`. Chi dung o `--thu`."""
    if not all(isinstance(x, str) and RE_OID.fullmatch(x) for x in (goc_su_kien, dau, hop)):
        return KHONG_DO_DUOC
    if goc_so not in (None, "-") and not (isinstance(goc_so, str) and RE_OID.fullmatch(goc_so)):
        return KHONG_DO_DUOC
    try:
        rc, ra = _git(kho, "rev-list", "--parents", "-n", "1", hop, chay=chay)
        k = re.fullmatch(rb"([0-9a-f]{40})((?: [0-9a-f]{40})*)\n", ra) if rc == 0 else None
        if not k or k.group(1).decode("ascii") != hop:
            return KHONG_DO_DUOC
        cha = k.group(2).decode("ascii").split()
        if len(cha) != 2:
            return KHONG_DO_DUOC
        if cha[1] != dau:
            return KHONG_DO_DUOC
        if goc_so not in (None, "-") and goc_so != cha[0]:
            return KHONG_DO_DUOC
        p1 = cha[0]
        if _git(kho, "merge-base", "--is-ancestor", goc_su_kien, p1, chay=chay)[0] != 0:
            return KHONG_DO_DUOC
        rc, mb = _git(kho, "merge-base", "--all", p1, dau, chay=chay)
        if rc != 0 or not re.fullmatch(rb"[0-9a-f]{40}\n", mb):
            return KHONG_DO_DUOC
        rc, cay = _git(kho, "--attr-source=" + p1, "merge-tree", "--write-tree", "--no-messages", p1, dau, chay=chay)
        if rc != 0 or not re.fullmatch(rb"[0-9a-f]{40}\n", cay):
            return KHONG_DO_DUOC
        ban_ghi = []
        for cap in ((f"{p1}...{dau}",), (p1, cay.decode().strip()), (p1, hop)):
            rc, ra = _git(kho, "--attr-source=" + p1, "diff", "--raw", "-z", "--no-renames", "--no-abbrev", *cap, chay=chay)
            muc = ra.decode("utf-8", "surrogateescape").split("\0")
            if rc != 0 or muc[-1] != "" or len(muc) % 2 != 1:
                return KHONG_DO_DUOC
            ban_ghi += list(zip(muc[0:-1:2], muc[1:-1:2]))
    except Exception:  # noqa: BLE001 — git vang/loi/dau ra la: khong do duoc, khong ep ve lan nao
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

class AnhChupHong(Exception):
    """Anh chup DA DUOC CHI DINH ma khong dung duoc: thieu MANIFEST, tep lech/vang so voi MANIFEST, duong dan thoat khoi anh chup."""


def doc_anh_chup(ac):
    """(doc(khoa) -> bytes | None, manifest theo khoa) cua mot anh chup da dong MANIFEST. Kiem TOAN VEN TRUOC khi tra (cung
    hanh vi voi `--tinh` cua #1434, review F5): moi muc co `duong_dan` phai nam TRONG anh chup, ton tai, va sha256 khop MANIFEST;
    muc khong co tep (het han, loi HTTP, het khung) la bang chung VANG MAT hop le, khong bi tu choi. Thieu MANIFEST, lech hay vang
    tep => `AnhChupHong` (anh chup da chi dinh ma hong KHAC voi khong chi dinh anh chup nao)."""
    ac = pathlib.Path(ac).resolve()
    f = ac / "MANIFEST.json"
    if not f.is_file():
        raise AnhChupHong(f"{ac}: khong co MANIFEST.json (anh chup chua dong)")
    try:
        theo_khoa = {m["khoa"]: m for m in json.loads(f.read_bytes())["tep"]}
    except (ValueError, KeyError, TypeError) as e:
        raise AnhChupHong(f"{ac}: MANIFEST.json khong doc duoc ({type(e).__name__})") from e
    hong = []
    for khoa, m in sorted(theo_khoa.items()):
        if not m.get("duong_dan"):
            continue
        p = (ac / m["duong_dan"]).resolve()
        if ac not in p.parents or not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != m.get("sha256"):
            hong.append(khoa)
    if hong:
        raise AnhChupHong(f"{ac}: {len(hong)} muc lech MANIFEST: {hong[:10]}")

    def doc(khoa):
        m = theo_khoa.get(khoa)
        return (ac / m["duong_dan"]).read_bytes() if m and m.get("duong_dan") else None
    return doc, theo_khoa


def tep_manh_tu_zip(b):
    """Byte cua tep `manh-<k>.txt` DUY NHAT trong zip artifact, hoac None (zip hong / khong dung mot tep .txt)."""
    import io
    import zipfile
    try:
        z = zipfile.ZipFile(io.BytesIO(b))
        ten = [n for n in z.namelist() if not n.endswith("/")]
        return z.read(ten[0]) if len(ten) == 1 and ten[0].endswith(".txt") else None
    except (zipfile.BadZipFile, KeyError, ValueError, OSError):
        return None


def lenh_tinh(ns):
    ac, ra = pathlib.Path(ns.anh_chup).resolve(), pathlib.Path(ns.ra).resolve()
    if ROOT == ra or ROOT in ra.parents:
        print("TU CHOI GHI: thu muc --ra phai nam NGOAI kho")
        return 4
    # review F5: anh chup v2 DA CHI DINH thi kiem toan ven TRUOC moi tinh toan (va truoc ca bo thu #1434); vang `--anh-chup-v2`
    # la "khong co v2" hop le, con chi dinh ma hong thi TU CHOI (rc 3, cung ma voi anh chup #1434 lech MANIFEST).
    doc2, theo_khoa2, man2 = None, {}, None
    if ns.anh_chup_v2:
        try:
            doc2, theo_khoa2 = doc_anh_chup(ns.anh_chup_v2)
        except AnhChupHong as e:
            print("ANH CHUP V2 HONG:", e)
            return 3
        man2 = hashlib.sha256((pathlib.Path(ns.anh_chup_v2).resolve() / "MANIFEST.json").read_bytes()).hexdigest()
    g = nap_goc()
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
    try:
        doc, theo_khoa = doc_anh_chup(ac)
    except AnhChupHong as e:
        print("ANH CHUP #1434 HONG:", e)
        return 3
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
        art, bn, cmt = None, {}, {}
        if doc2 and f"arts/{rid}/p1" in theo_khoa2:
            ds_art, du_art, _, _ = g.chon_chuoi_trang(doc2, f"arts/{rid}")
            art = [{"name": a.get("name"), "expired": bool(a.get("expired"))} for a in ds_art] if du_art else None
        for k in range(SO_MANH_G5) if doc2 else ():                # review F1: NOI DUNG bien nhan (zip artifact) + commit cua head
            b = doc2(f"bn/{rid}/{k}")
            nd = tep_manh_tu_zip(b) if b is not None else None
            if nd is not None:
                bn[k] = nd
                h = nd.split(b"\n", 1)[0]
                for sha in set(re.findall(rb'"head": "([0-9a-f]{40})"', h)):
                    bc = doc2(f"cmt/{sha.decode()}")
                    try:
                        cmt[sha.decode()] = [p["sha"] for p in json.loads(bc)["parents"]] if bc is not None else None
                    except (ValueError, KeyError, TypeError):
                        cmt[sha.decode()] = None
        l = dung_luot(r, dong, log, art, bn, {k: v for k, v in cmt.items() if v is not None})
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
                if b and json.loads(b).get("phien_ban_oracle") != 2:   # oracle ba OID cua lan 1 (review F2): khong dung
                    oracle = None
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
                   "cohort_goc": bool(cohort_goc), "co_anh_chup_v2": bool(doc2), "manifest_v2_sha256": man2,
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

def thu_bien_nhan(t, g, cac_rid):
    """Pha thu cua review F1, sau khi da co danh sach artifact (`arts/<rid>`): NOI DUNG bien nhan manh (zip artifact con han; chang
    hai khong mang token — `Thu._goi`), roi commit cua MOI head ma bien nhan khai (REST GET, de doi chieu cha hai = head cua luot khi
    dong bong chua co `hop`). Het han / loi => muc MANIFEST vang tep, de nguyen; khong suy gi."""
    def doc(k):
        return (t.ra / t.muc[k]["duong_dan"]).read_bytes() if k in t.muc and t.muc[k].get("duong_dan") else None
    viec = []
    for rid in cac_rid:
        if f"arts/{rid}/p1" not in t.muc:
            continue
        for a in g.chon_chuoi_trang(doc, f"arts/{rid}")[0]:
            ten = a.get("name") or ""
            if ten.startswith(TEN_ART_MANH) and ten[len(TEN_ART_MANH):].isdigit() and not a.get("expired"):
                viec.append(lambda rid=rid, k=int(ten[len(TEN_ART_MANH):]), aid=a["id"]:
                            t.lay(f"bn/{rid}/{k}", f"actions/artifacts/{aid}/zip", f"bn/{rid}/{k}.zip", "bien_nhan_manh"))
    t.song_song(viec)
    dau_bn = set()
    for rid in cac_rid:
        for k in range(SO_MANH_G5):
            b = doc(f"bn/{rid}/{k}")
            nd = tep_manh_tu_zip(b) if b is not None else None
            dau_bn |= {x.decode() for x in re.findall(rb'"head": "([0-9a-f]{40})"', (nd or b"").split(b"\n", 1)[0])}
    t.song_song([lambda h=h: t.lay(f"cmt/{h}", f"commits/{h}", f"cmt/{h}.json", "commit") for h in sorted(dau_bn)])


def lenh_thu(ns):
    g = nap_goc()
    if not os.environ.get("GITHUB_PAT"):
        raise SystemExit("thieu bien moi truong GITHUB_PAT")
    ac = pathlib.Path(ns.anh_chup).resolve()
    try:
        doc, _ = doc_anh_chup(ac)
    except AnhChupHong as e:
        raise SystemExit(f"anh chup #1434 khong dung duoc: {e}") from e
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
    thu_bien_nhan(t, g, [r["id"] for r in co_ci if r.get("event") == "pull_request"])
    muc_oracle = []
    for rid, pl in oracle:                                   # git CHI DOC tren --kho; khong mang
        kq = oracle_moi(ns.kho, pl.get("goc_su_kien"), pl.get("goc_so"), pl.get("dau"), pl.get("hop"))
        b = xuat_json({"run_id": rid, "oracle": kq, "phien_ban_oracle": 2,
                       "oid": {k: pl.get(k) for k in ("goc_su_kien", "goc_so", "dau", "hop")}})
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


def tao_bien_nhan(head, so_dot_bien=16, che_do=None, sha="ab" * 32, n=SO_MANH_G5):
    """{k: byte tep manh} GIA dung hop dong `_ket_thuc_manh` (dot bien `db<i>` vao manh `i % n`) — chi cho --tu-kiem."""
    kq = {}
    for k in range(n):
        dau = {"phien_ban": 1, "manh": k, "so_manh": n, "sha256_test": sha, "head": head, **({"che_do": che_do} if che_do else {})}
        than = "".join("BKCON " + json.dumps(["do", f"db{i}", "t1", {}]) + "\n" for i in range(k, so_dot_bien, n))
        kq[k] = ("MANH " + json.dumps(dau, sort_keys=True) + "\n" + than).encode("utf-8")
    return kq


def luot_fixture(fx, F=None):
    """Ban ghi luot cua MOT fixture G4b: `bien_nhan` = {"tao": {...}, "sua": {k: chuoi | null}} (GIA) hoac {"tep": <fixture bien nhan
    THAT rut gon>} (kem danh sach artifact va commit cua chinh luot ay)."""
    F = F or DAY / "fixtures"
    spec, bn, cmt, art = fx.get("bien_nhan") or {}, None, fx.get("cmt"), fx.get("artifact")
    if "tao" in spec:
        t = spec["tao"]
        bn = tao_bien_nhan(t["head"], t.get("so_dot_bien", 16), t.get("che_do"))
    if "tep" in spec:
        that = json.loads((F / spec["tep"]).read_text(encoding="utf-8"))
        bn = {int(k): (m["dau_nguyen_van"] + "\n" + "".join("BKCON " + json.dumps(x, ensure_ascii=False) + "\n" for x in m["bkcon_rut_gon"])).encode("utf-8")
              for k, m in that["manh"].items()}
        cmt, art = that["cmt"], art if art is not None else that["artifact"]
    for k, v in (spec.get("sua") or {}).items():
        if v is None:
            bn.pop(int(k), None)
        else:
            bn[int(k)] = v.encode("utf-8")
    l = dung_luot(fx["run"], fx["dong"], fx.get("log"), art, bn, cmt)
    l.update(fx.get("ghi_de") or {})
    return l


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
            l = luot_fixture(fx, F)
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
            l = luot_fixture(fx, F)
            return fx, l, quy_g4b(l)
        fx, l, kq = quy("b08_run_44126854175_tam_manh_cancelled.json")
        bang(fx["run"]["id"] == 44126854175 and l["manh"]["ket_luan"] == ["cancelled"] * 8 and kq[0] != "du_hoan_tat" and kq == ("dang_do", 8),
             f"luot 44126854175 (8 manh cancelled) KHONG duoc ra du_hoan_tat: {kq}")
        fx, l, kq = quy("b03_ca_duong_pr4_mo_phong.json")
        bang(fx["mo_phong"] is True and l["lan_cu"] == DAY_DU and l["che_do_chay"] == DUONG_NHANH and kq == ("duong_nhanh_co_bang_chung", 3)
             and quy_g4a(l) == "duong_nhanh_dang_chay" and quy_g4a(l) != "bo_moi", f"ca duong PR4 phai ra duong_nhanh_co_bang_chung, khong tinh bo moi: {kq}")
        fx, l, kq = quy("b07_run_44443875641_du_bien_nhan_gom_cancelled.json")
        bang(fx["run"]["id"] == 44443875641 and l["manh"]["bien_nhan"] == [BN_HOP_LE] * 8 and l["manh"]["du_noi_dung"] is True
             and l["gom"]["ket_luan"] == "cancelled" and kq == ("gom_hong", 7),
             f"luot 44443875641 (du 8 bien nhan THAT da kiem noi dung, gom cancelled) phai ra gom_hong: {kq} {l['manh']}")
        fx, l, kq = quy("b07_chon_bo_gom_cancelled.json")
        bang(che_do_chon(l) in ("bo_dn", "bo_moi") and l["gom"]["ket_luan"] == "cancelled" and kq == ("gom_hong", 7), f"chon bo + gom cancelled phai ra gom_hong: {kq}")

    @kiem
    def g4_tong_hop_mau_so_va_tran():
        ds = []
        for tep in sorted((F / "g4b").glob("*.json")):
            ds.append(luot_fixture(J(f"g4b/{tep.name}"), F))
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

    @kiem
    def bien_nhan_noi_dung_hai_chieu_ba_trang_thai():
        """review F1: bien nhan la NOI DUNG da kiem; job `success`/ten artifact chi la bang chung VANG MAT."""
        H, P, R = "c" * 40, "d" * 40, "1" * 40
        tot = tao_bien_nhan(H, 20)
        job = {k: {"ket_luan": "success", "head_sha": R} for k in range(SO_MANH_G5)}
        co = {k: "co" for k in range(SO_MANH_G5)}
        kq = bien_nhan_luot(job, co, tot, R, cmt={H: [P, R]})
        bang(kq["du_noi_dung"] is True and kq["che_do"] == "du" and kq["thieu"] is False and kq["trang_thai"] == [BN_HOP_LE] * 8,
             f"doi chung: 8 bien nhan dung, head doi chieu qua commit => du: {kq}")
        bang(bien_nhan_luot(job, co, tot, R, hop=H)["du_noi_dung"] is True, "doi chung: head = merge ref cua dong bong => du")
        dau, _, than = tot[0].decode().partition("\n")
        dj = json.loads(dau[5:])
        m = lambda **s: ("MANH " + json.dumps({**dj, **s}) + "\n" + than).encode()
        hong = {"thieu_dong_MANH": than.encode(), "dau_khong_doc_duoc": b"MANH {", "khoa_dau_la": m(thua=1),
                "phien_ban_la": m(phien_ban=2), "sai_chi_so_manh": m(manh=1), "che_do_la": m(che_do="nhanh"),
                "van_tay_la": m(sha256_test="x"), "dong_ngoai_hop_dong": (dau + "\n" + than + 'G5_THOI_GIAN {"loai": "con"}\n').encode(),
                "bkcon_hong": (dau + "\nBKCON [1, 2]\n").encode(), "ten_rong_hoac_trung": (dau + "\n" + than + than).encode()}
        for ly, nd in hong.items():
            bang(kiem_bien_nhan(nd, 0)[:2] == (BN_HONG, ly), f"tep manh hong ({ly}): {kiem_bien_nhan(nd, 0)[:2]}")
        bang(kiem_bien_nhan(m(so_manh=7), 0)[:2] == (BN_HONG, "sai_chi_so_manh"), "so_manh khac 8 => hong")
        bang(kiem_bien_nhan((dau + "\n").encode(), 0)[:2] == (BN_HONG, "ten_rong_hoac_trung"), "than rong => hong")
        bang(kiem_bien_nhan(m(che_do="dich"), 0)[2]["che_do"] == "dich", "truong che_do doc dung")
        for ten, kq, mong in (
            ("lech van tay", bien_nhan_luot(job, co, {**tot, 3: tao_bien_nhan(H, 20, sha="cd" * 32)[3]}, R, hop=H),
             "bo_bien_nhan_lech_head_van_tay_che_do"),
            ("lech che do", bien_nhan_luot(job, co, {**tot, 3: tao_bien_nhan(H, 20, che_do="dich")[3]}, R, hop=H),
             "bo_bien_nhan_lech_head_van_tay_che_do"),
            ("lech phan hoach", bien_nhan_luot(job, co, {**tot, 7: tao_bien_nhan(H, 24)[7]}, R, hop=H), "bo_bien_nhan_lech_phan_hoach"),
            ("head khac merge ref", bien_nhan_luot(job, co, tot, R, hop=P), "head_bien_nhan_khong_khop_luot"),
            ("cha hai khac head luot", bien_nhan_luot(job, co, tot, R, cmt={H: [R, P]}), "head_bien_nhan_khong_khop_luot"),
            ("job mang head khac", bien_nhan_luot({**job, 2: {"ket_luan": "success", "head_sha": P}}, co, tot, R, hop=H),
             "job_mang_head_khac_luot"),
        ):
            bang(kq["du_noi_dung"] is False and kq["thieu"] is True and mong in kq["ly_do"], f"{ten}: mong khong du + thieu ({mong}): {kq}")
        # ba trang thai khi KHONG co noi dung: khong bao gio suy ra hop_le tu job success
        for ten, kq, mong_tt, thieu in (
            ("chua lay noi dung", bien_nhan_luot(job, co, {}, R, hop=H), "noi_dung_chua_lay", False),
            ("khong danh sach artifact", bien_nhan_luot(job, None, {}, R, hop=H), "noi_dung_chua_lay", False),
            ("artifact het han", bien_nhan_luot(job, {k: "het_han" for k in range(8)}, {}, R), "artifact_het_han", False),
            ("head chua doi chieu duoc", bien_nhan_luot(job, co, tot, R), "head_bien_nhan_chua_doi_chieu_duoc", False),
            ("artifact vang", bien_nhan_luot(job, {}, {}, R), "artifact_vang", True),
            ("job khong success, khong danh sach", bien_nhan_luot({k: {"ket_luan": "cancelled", "head_sha": R} for k in range(8)}, None, {}, R),
             "job_khong_success", True),
        ):
            bang(kq["du_noi_dung"] is False and kq["thieu"] is thieu and kq["ly_do"] == [mong_tt] * 8,
                 f"{ten}: mong khong du, thieu={thieu}, ly do {mong_tt}: {kq}")

    @kiem
    def g4b_khong_suy_hoan_tat_tu_job_success():
        """review F1: buoc 5 can bang chung DUONG (noi dung da kiem, hoac gom in GOM MẢNH 8/8); dau "KHONG DO" trai che do => buoc 9."""
        fx = J("g4b/b05_du_hoan_tat.json")
        for ten, sua, mong in (
            ("chi job success, khong danh sach, khong log gom", {"artifact": None, "log": {**fx["log"], "gom": None}}, ("thieu_bang_chung", 9)),
            ("danh sach artifact du nhung khong log gom", {"log": {**fx["log"], "gom": None}}, ("thieu_bang_chung", 9)),
            ("dau KHONG DO duong nhanh khi chon du", {"log": {**fx["log"], "gom": "GOM: KHÔNG ĐO — x (CONG_CU_TEST_GOP_CHE_DO=duong_nhanh, 0 mảnh)\n"}},
             ("thieu_bang_chung", 9)),
            ("gom in so manh khac 8", {"log": {**fx["log"], "gom": "GOM MẢNH 3/3\n"}}, ("thieu_bang_chung", 9)),
            ("gom in GOM MẢNH 8/8", {}, ("du_hoan_tat", 5)),
            ("noi dung du, khong log gom", {"artifact": None, "log": {**fx["log"], "gom": None}, "bien_nhan": {"tao": {"head": "c" * 40}},
                                            "cmt": {"c" * 40: ["d" * 40, "1" * 40]}}, ("du_hoan_tat", 5)),
        ):
            kq = quy_g4b(luot_fixture({**fx, **sua}, F))
            bang(kq == mong, f"{ten}: mong {mong}, duoc {kq}")

    @kiem
    def anh_chup_v2_kiem_manifest():
        """review F5: anh chup v2 DA CHI DINH phai khop MANIFEST tung byte truoc khi tinh; muc vang tep (het han/loi) van hop le."""
        with tempfile.TemporaryDirectory(prefix="wp1448_ac_") as d:
            goc = pathlib.Path(d)
            ac = goc / "v2"
            (ac / "log").mkdir(parents=True)
            b = "GOM MẢNH 8/8\n".encode("utf-8")
            (ac / "log" / "1.log").write_bytes(b)
            (goc / "ngoai.log").write_bytes(b)

            def man(*muc):
                (ac / "MANIFEST.json").write_text(json.dumps({"tep": list(muc)}), encoding="utf-8")
            tot = {"khoa": "log/1", "duong_dan": "log/1.log", "sha256": hashlib.sha256(b).hexdigest()}
            vang = {"khoa": "arts/2/p1", "duong_dan": None, "http": 410, "loi": "HTTP 410"}
            man(tot, vang)
            doc2, _ = doc_anh_chup(ac)
            bang(doc2("log/1") == b and doc2("arts/2/p1") is None, "doi chung: anh chup dung + muc vang tep hop le")

            def hong(ten):
                try:
                    doc_anh_chup(ac)
                except AnhChupHong:
                    return
                raise TuKiemDo(f"{ten}: anh chup hong ma van doc duoc")
            (ac / "log" / "1.log").write_bytes(b[:-1] + b"X")
            hong("doi mot byte")
            (ac / "log" / "1.log").unlink()
            hong("vang tep")
            (ac / "log" / "1.log").write_bytes(b)
            man(tot, {"khoa": "log/9", "duong_dan": "../ngoai.log", "sha256": hashlib.sha256(b).hexdigest()})
            hong("duong dan thoat khoi anh chup")
            (ac / "MANIFEST.json").unlink()
            hong("khong MANIFEST")
            man({**tot, "sha256": "0" * 64})
            ra = goc / "ra"
            rc = lenh_tinh(argparse.Namespace(anh_chup=str(goc / "khong_co_anh_chup_1434"), ra=str(ra), anh_chup_v2=str(ac), cohort_goc=None))
            bang(rc == 3 and not ra.exists(), f"--tinh voi anh chup v2 lech MANIFEST phai tu choi rc 3 TRUOC moi tinh toan, duoc rc={rc}")

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
    ("g4b_tam_manh_cancelled_thanh_hoan_tat", '    if chon == "du" and du_bn and kl_gom == "success" and dau_khop:\n', '    if chon == "du":\n', "g4b_bon_fixture_bat_buoc_cua_dac_ta"),
    ("g4b_gom_cancelled_van_hoan_tat", '    if chon == "du" and du_bn and kl_gom == "success" and dau_khop:\n', '    if chon == "du" and du_bn and dau_khop:\n',
     "g4b_bon_fixture_bat_buoc_cua_dac_ta"),
    ("g4a_duong_nhanh_tinh_la_bo_moi", '{"bo_dn": "duong_nhanh_dang_chay", "bo_moi": "bo_moi"', '{"bo_dn": "bo_moi", "bo_moi": "bo_moi"', "g4b_bon_fixture_bat_buoc_cua_dac_ta"),
    ("g4_mau_so_gom_buoc_0_1", "    mau = sum(n for b, n in theo_buoc.items() if int(b) >= 2)\n", "    mau = sum(theo_buoc.values())\n", "g4_tong_hop_mau_so_va_tran"),
    ("bong_dem_loi_ich_bang_ton_du", '    return {"loi_ich": loi_ich, "ton_du": ton_du}\n', '    return {"loi_ich": ton_du, "ton_du": ton_du}\n', "bong_hai_bo_dem_tach_rieng"),
    ("bong_ton_du_so_voi_cu", "    ton_du = int(che_do_chay != oracle)", '    ton_du = int(pl.get("cu") != oracle)', "bong_hai_bo_dem_tach_rieng"),
    ("g5_hop_thanh_tong", "        elif b > cuoi:\n            tong, cuoi = tong + (b - cuoi), b\n    return tong\n\n\ndef trich_g5",
     "        else:\n            tong, cuoi = tong + (b - a), max(b, cuoi)\n    return tong\n\n\ndef trich_g5", "g5_hop_khac_tong_va_ba_thanh_phan"),
    ("g5_thieu_thanh_phan_van_du", 'all(so(b.get(k)) for k in ("dung_cay_s", "ca_dich_s", "ca_khac_s"))', 'all(so(b.get(k)) for k in ("dung_cay_s", "ca_khac_s"))',
     "g5_hop_khac_tong_va_ba_thanh_phan"),
    ("gom_dau_la_thanh_duong_nhanh", '            dau = "khong_do:" + (khop[0] if len(khop) == 1 else "la")\n', '            dau = "khong_do:duong_nhanh"\n', "gom_dau_hieu_duong_theo_ly_do"),
    # wp1448 r2 lan 2 — review F1: bien nhan la NOI DUNG da kiem (hoac dau duong cua job gom), khong bao gio la job `success`
    ("g4b_gom_success_la_bien_nhan", '    return che_do == "du" and gom.get("ket_luan") == "success" and gom.get("dau") == f"gom_manh:{SO_MANH_G5}"\n',
     '    return che_do == "du" and gom.get("ket_luan") == "success"\n', "g4b_khong_suy_hoan_tat_tu_job_success"),
    ("g4b_dau_khong_do_van_khop", '    dau_khop = dau in (None, f"gom_manh:{SO_MANH_G5}")', '    dau_khop = True', "g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc"),
    ("bn_thieu_van_du_neu_gom_8_8", '    if manh.get("thieu") is not False:\n        return False\n', '', "g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc"),
    ("bn_che_do_noi_dung_bo_qua", ' and manh.get("che_do_bien_nhan") == che_do', '', "g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc"),
    ("bn_bo_doi_chieu_merge_ref", '(g["head"] == hop) if hop', 'True if hop', "bien_nhan_noi_dung_hai_chieu_ba_trang_thai"),
    ("bn_bo_doi_chieu_cha_hai", '(len(cha) == 2 and cha[1] == head_run)', '(len(cha) == 2)', "bien_nhan_noi_dung_hai_chieu_ba_trang_thai"),
    ("bn_head_chua_doi_chieu_thanh_hop_le", '                elif dinh_danh is None:\n                    tt[k], ly[k] = KHONG_DO_DUOC, "head_bien_nhan_chua_doi_chieu_duoc"\n',
     '', "bien_nhan_noi_dung_hai_chieu_ba_trang_thai"),
    ("bn_bo_kiem_khoa_dau", 'set(dau) - {"che_do"} != KHOA_DAU_MANH', 'not KHOA_DAU_MANH <= set(dau)', "bien_nhan_noi_dung_hai_chieu_ba_trang_thai"),
    ("bn_bo_kiem_phien_ban", ' or dau["phien_ban"] != 1:\n', ':\n', "bien_nhan_noi_dung_hai_chieu_ba_trang_thai"),
    ("bn_bo_kiem_chi_so_manh", '    if dau["manh"] != k or dau["so_manh"] != so_manh:\n', '    if dau["so_manh"] != so_manh:\n', "bien_nhan_noi_dung_hai_chieu_ba_trang_thai"),
    ("bn_bo_kiem_so_manh", '    if dau["manh"] != k or dau["so_manh"] != so_manh:\n', '    if dau["manh"] != k:\n', "bien_nhan_noi_dung_hai_chieu_ba_trang_thai"),
    ("bn_bo_kiem_che_do", '    if che_do not in CHE_DO_G5:\n        return BN_HONG, "che_do_la", None\n', '', "bien_nhan_noi_dung_hai_chieu_ba_trang_thai"),
    ("bn_bo_kiem_van_tay", '        return BN_HONG, "van_tay_la", None\n', '        pass\n', "bien_nhan_noi_dung_hai_chieu_ba_trang_thai"),
    ("bn_nhan_dong_ngoai_hop_dong", '            return BN_HONG, "dong_ngoai_hop_dong", None\n', '            continue\n', "bien_nhan_noi_dung_hai_chieu_ba_trang_thai"),
    ("bn_bo_kiem_ban_ghi_bkcon", '        if not isinstance(bg, list) or len(bg) < 2 or type(bg[1]) is not str:\n            return BN_HONG, "bkcon_hong", None\n', '',
     "bien_nhan_noi_dung_hai_chieu_ba_trang_thai"),
    ("bn_bo_kiem_ten_trung", ' or len(set(ten)) != len(ten)', '', "bien_nhan_noi_dung_hai_chieu_ba_trang_thai"),
    ("bn_bo_kiem_bo_lech", '        if len(bo) != 1:\n', '        if False:\n', "bien_nhan_noi_dung_hai_chieu_ba_trang_thai"),
    ("bn_bo_kiem_phan_hoach", ' or any(len(gt[k]["ten"]) != len(range(k, len(ten), SO_MANH_G5)) for k in range(SO_MANH_G5))', '',
     "bien_nhan_noi_dung_hai_chieu_ba_trang_thai"),
    ("bn_artifact_vang_khong_thieu", '        elif art == "vang":\n            tt[k], ly[k] = BN_THIEU, "artifact_vang"\n', '',
     "bien_nhan_noi_dung_hai_chieu_ba_trang_thai"),
    ("bn_job_do_khong_thieu", '        elif art is None and (d is None or d.get("ket_luan") != "success"):\n            tt[k], ly[k] = BN_THIEU, "job_khong_success"\n', '',
     "g4b_bon_fixture_bat_buoc_cua_dac_ta"),
    ("bn_job_success_la_bien_nhan", '            tt[k], ly[k] = KHONG_DO_DUOC, "artifact_het_han" if art == "het_han" else "noi_dung_chua_lay"\n',
     '            tt[k], ly[k] = BN_HOP_LE, "-"\n', "bien_nhan_noi_dung_hai_chieu_ba_trang_thai"),
    ("bn_job_sai_head_bo_qua", '        if d is not None and d.get("head_sha") not in (None, head_run):\n            tt[k], ly[k] = BN_HONG, "job_mang_head_khac_luot"\n',
     '        if False:\n            pass\n', "bien_nhan_noi_dung_hai_chieu_ba_trang_thai"),
    # review F5: anh chup v2 da chi dinh phai khop MANIFEST
    ("anh_chup_bo_kiem_bam", '    if hong:\n        raise AnhChupHong', '    if False:\n        raise AnhChupHong', "anh_chup_v2_kiem_manifest"),
    ("anh_chup_vang_manifest_im_lang", '        raise AnhChupHong(f"{ac}: khong co MANIFEST.json (anh chup chua dong)")\n', '        return None, {}\n',
     "anh_chup_v2_kiem_manifest"),
    ("anh_chup_duong_dan_thoat_ra_ngoai", '        if ac not in p.parents or not p.is_file()', '        if not p.is_file()', "anh_chup_v2_kiem_manifest"),
    # review F3: phan loai khong do duoc khong vao bo dem
    ("bong_dem_nhan_cu_fail_close", '    cu_do = pl.get("cu_do") == DO_DUOC\n', '    cu_do = True\n', "bong_hai_bo_dem_tach_rieng"),
    ("bong_dem_nhan_kiem_moi_khong_do_duoc", '    moi_do = pl.get("kiem_moi") != KHONG_DO_DUOC\n', '    moi_do = True\n', "bong_hai_bo_dem_tach_rieng"),
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
