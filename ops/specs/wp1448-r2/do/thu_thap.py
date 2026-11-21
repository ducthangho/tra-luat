#!/usr/bin/env python3
"""wp1448 r2 — bo thu v2 (dac ta ops/specs/wp1448-r2/SPEC.md muc 5), CHI DOC. Ke thua hop dong cua bo thu #1434
(`ops/specs/wp1434-r3/do/thu_thap.py`, nap bang duong dan, KHONG sua): anh chup NGOAI kho, ba che do, ba trang thai,
ghi co gioi han, `--tinh` tat dinh, khong mang, KHONG goi git. DO 20-11-2026: `--tinh` cua #1434 tu no phong MOT tien trinh con
(`git check-ignore`, qua `tim()` trong muc §6 cua bao cao); `--tinh` v2 thay muc ay va chan moi lan phong `git` — xem NGUYEN TAC (3).

  --thu --anh-chup <anh chup #1434> --ra <anh chup v2> [--run-g5 id,id] [--kho <kho git>]
        GitHub REST GET -> them vao MOT thu muc anh chup v2 RIENG (khong ghi vao anh chup #1434): log job gom cong cu, danh
        sach artifact, NOI DUNG bien nhan manh G5 (zip artifact con han) + commit cua head bien nhan, luot + job cua
        `packet-loop-dot-bien.yml`; voi moi luot neu ten o `--run-g5` (MOI su kien; luot ngoai cohort #1434 duoc thu rieng): log manh
        G5 + bien nhan cua CHINH luot ay; co `--kho` thi tinh oracle ngu canh moi tu bon OID (git CHI DOC tren kho ay).
  --tinh --anh-chup <anh chup #1434> --ra <thu muc> [--anh-chup-v2 <anh chup v2>] [--cohort-goc <COHORT.json>] [--kiem-ke <thu muc>]
        thuan offline -> nen/ (BASELINE.json cua bo thu #1434 tren cung anh chup), BASELINE_V2.json, BAO_CAO_V2.md. Moi anh chup
        da chi dinh phai khop MANIFEST tung byte (lech/vang tep => rc 3, truoc moi tinh toan). Hop dong bien nhan la cua CHINH
        `ops/cong_cu_test.py` o cay nay (`kiem_than`); `--kiem-ke` them bang dot bien cua cac phien ban nguon KHAC (xem duoi).
  --xuat-kiem-ke --kho <cay da checkout> --ra <thu muc NGOAI kho>
        ghi `<van tay>.json` = KIEM KE cua CHINH MA o cay ay (bam `ops/cong_cu_test.py` + bang `DOT_BIEN` theo thu tu + ten ca): nap
        module cua cay do (CHAY ma cua no, nhu chay bo ca cua no — chi dung voi cay ban tin). Day la nguon DUY NHAT cua mot kiem ke.
  --tu-kiem
        ca tu kiem tren fixtures/, khong mang, khong git; gom dot bien tren BAN SAO cua chinh tep nay. Nap module that
        `ops/cong_cu_test.py` cua cay nay (phia ghi + phia doc bien nhan), nen can nhung thu module ay import (PyYAML).

Them so voi #1434: ban ghi theo (run_id, attempt, su kien, head) voi che do du dinh, che do thuc chay, ly do bo, trang thai
hoan tat va dau hieu duong; doc cac dong `G5_THOI_GIAN`, `BONG_CONG_CU`, `BONG_PHAN_LOAI` khi co; thoi gian theo buoc cua
`gate` va `gate-ops`; workflow `packet-loop-dot-bien.yml`; phep quy G4a va G4b (muoi buoc co thu tu, vet can).

NGUYEN TAC (lan 4, thiet ke lai) — CHI BANG CHUNG DUONG: mot ket luan "du" / "do duoc" chi co khi TUNG thu no can DA duoc kiem va DAT.
Thu vang, khong doc duoc, khong kiem duoc hay mau thuan KHONG BAO GIO duoc bu bang mot dau hieu khac; buoc xet ca TAP chi co the HA.
  (1) Bien nhan manh — ba tang, moi TEP mot minh: CAU TRUC (`kiem_cau_truc`: khong can kiem ke, khong can tep nao khac) -> HOP DONG tren
      kiem ke cua dung van tay tep khai (`kiem_than`) -> HEAD (`doi_chieu_head`). `du_hoan_tat` chi khi CA tam vi tri deu `hop_le`; dau
      `GOM MẢNH 8/8` cua job gom khong nang cap duoc gi (no chi co the MAU THUAN voi che do da chon).
  (2) Thoi gian G5 — do day du va doi chieu chi khi: DUNG MOT ban ghi cha; moi ban ghi con hop le voi PID DUY NHAT (trong log cua mot job,
      mot attempt); khoang huu han co thu tu; thanh phan huu han, khong am; va co kiem ke mong doi cua CHINH luot (bien nhan cua luot ay,
      thu cho moi luot duoc chon, moi su kien). Khong thi `khong_do_duoc` kem ly do — khong bao gio "thieu 0".
  (3) `--tinh` khong bao gio phong `git` (`cam_git` tu choi va GHI lai moi lan thu; co lan thu => rc 5, khong ghi ket qua v2). Muc §6 cua
      bao cao #1434 la phep chay tren CAY SONG, khong co trong anh chup: ban tinh lai ghi `khong_do_duoc` cho muc ay (`s6_khong_cay_song`).
"""
import argparse
import contextlib
import hashlib
import importlib.util
import json
import math
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import types
import warnings

DAY = pathlib.Path(__file__).resolve().parent
# Ban sao tam cua --tu-kiem (dot bien) khong nam trong kho: tien trinh cha trao goc kho THAT qua bien nay (de nap hop dong that).
ROOT = (pathlib.Path(os.environ["WP1448_GOC_KHO"]) if os.environ.get("WP1448_GOC_KHO")
        else next((p for p in DAY.parents if (p / "ops" / "specs" / "wp1434-r3" / "do").is_dir()), DAY.parent))
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
# wp1448 r2 lan 2 (review F1): BIEN NHAN MANH la NOI DUNG tep `manh-<k>.txt` trong artifact `TEN_ART_MANH`, KHONG phai ket luan
# job. Job `success` hay ten artifact chi la bang chung VANG MAT (job do/huy, artifact vang => thieu), khong bao gio la bang chung CO.
# Lan 4 (review 3, lop g4-receipt-authority, THIET KE LAI): khong con goi `_gom_manh` tren ca bo (ket qua cua no phu thuoc bo co du hay
# khong, nen mot tep hong tung bi che khi bo thieu / khong co kiem ke). Moi TEP duoc kiem mot minh bang chinh hai ham ma `_gom_manh` dung
# cho tung manh (`kiem_than`); bo thu van khong chep luat ban ghi nao. `du` = ca tam vi tri `hop_le`, khong co duong lui nao khac.
TEN_ART_MANH = JOB_MANH + "-manh-ubuntu-latest-"
CHE_DO_G5 = ("du", "dich")
BN_HOP_LE, BN_HONG, BN_THIEU = "hop_le", "khong_hop_le", "thieu"                    # + KHONG_DO_DUOC: ba trang thai + thieu
SU_KIEN_HEAD_LUOT = ("push", "workflow_dispatch", "schedule")                   # su kien ma `github.sha` la CHINH head cua luot
RE_SHA256 = re.compile(r"[0-9a-f]{64}")
TRAN_ATTEMPT = 50                                                               # GitHub cho chay lai mot luot toi da 50 lan: ban ghi attempt CO TRAN


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


def so_do(x):
    """So dung duoc lam PHEP DO: int/float (khong bool), HUU HAN, KHONG AM; khac => False. TOAN PHAN (review 4 F6): so nguyen qua lon => False."""
    try:
        return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x)) and x >= 0
    except OverflowError:
        return False


def so_lan(x):
    """`run_attempt` -> so nguyen 1..`TRAN_ATTEMPT` | None (chuoi, bool, float, ngoai tran: khong nem, khong doan); vang / null => 1 (nhu #1434)."""
    return 1 if x is None else (x if type(x) is int and 1 <= x <= TRAN_ATTEMPT else None)


def khoang_do(b):
    """Ban ghi mang khoang [bat_dau, ket_thuc] HUU HAN va CO THU TU."""
    return so_do(b.get("bat_dau")) and so_do(b.get("ket_thuc")) and b["ket_thuc"] >= b["bat_dau"]


def tap_con(cha, con, mong):
    """Ly do TAP CON cua mot manh KHONG phai bang chung day du, hoac None khi no doi chieu duoc (review 3, F6 — chi bang chung duong):
    DUNG MOT ban ghi cha; so ban ghi con = `so_con` cha khai; MOI ban ghi con hop le (pid nguyen duong, khoang huu han co thu tu,
    `so_dot_bien` nguyen) — mot ban ghi xau KHONG bi lang le bo qua; PID DUY NHAT trong log (mot job, mot attempt: cac con cua mot manh
    song dong thoi nen PID cua chung khac nhau; hai ban ghi cung PID la dinh danh mau thuan, khong bu duoc cho mot con mat); va so dot
    bien TUNG con khai khop PHAN CHIA cua chinh ma tren dinh danh mong doi (`_phong_con`: con thu i nhan `mong[i::so_con]`)."""
    if len(cha) != 1:
        return f"can DUNG MOT ban ghi cha, co {len(cha)}"
    if type(cha[0].get("so_con")) is not int or cha[0]["so_con"] != len(con) or not con:
        return f"so ban ghi con {len(con)} khac so con cha khai ({cha[0].get('so_con')!r})"
    xau = [b for b in con if not (type(b.get("pid")) is int and b["pid"] > 0 and khoang_do(b) and type(b.get("so_dot_bien")) is int)]
    if xau:
        return f"{len(xau)} ban ghi con khong hop le (pid nguyen duong, khoang huu han co thu tu, so_dot_bien nguyen)"
    pid = [b["pid"] for b in con]
    if len(set(pid)) != len(pid):
        return f"dinh danh con (pid) khong duy nhat: {sorted({p for p in pid if pid.count(p) > 1})}"
    khai, chia = sorted(b["so_dot_bien"] for b in con), sorted(len(mong[i::len(con)]) for i in range(len(con)))
    if khai != chia:
        return f"so dot bien tung con khai {khai} khac phan chia mong doi {chia}"
    return None


def tong_hop_g5(ban_ghi, giay_buoc=None, mong=None):
    """Mot manh. `mong` = dinh danh dot bien MONG DOI cua manh (`ten_mong`: phan hoach cua CHINH MA tren kiem ke cua luot); None = khong do duoc.
    DO DAY DU: mau so la `mong`, KHONG phai so dong con sot lai. Mot dinh danh DU khi co DUNG MOT dong mang ten no, dong ay `do_duoc`, khoang
    cua no huu han co thu tu va CA BA thanh phan (dung cay, ca dich, ca khac) huu han khong am. Dinh danh vang dong, co hon mot dong (ke ca
    giong het: `ten_trung`), hay mang thanh phan am / NaN / vo cung la THIEU va duoc NEU TEN. Dong mang ten ngoai `mong` va dong hong dem
    rieng. Khong co `mong` => `khong_do_duoc` (khong bao gio "thieu 0").
    DOI CHIEU thoi gian tuong cua BUOC (`giay_buoc`, tu API; vang thi `tuong_s` cua ban ghi cha duy nhat) voi HOP cac khoang con, phan lech
    la `khong_phan_bo_s` — chi khi `tap_con` doi chieu duoc."""
    cha = [b for b in ban_ghi if b.get("loai") == "cha"]
    con = [b for b in ban_ghi if b.get("loai") == "con"]
    db = [b for b in ban_ghi if b.get("loai") == "dot_bien"]
    theo_ten = {}
    for b in db:
        theo_ten.setdefault(b.get("ten") if isinstance(b.get("ten"), str) else None, []).append(b)
    kq = {"so_con": len(con), "so_dong_dot_bien": len(db),
          "so_dong_hong": len(ban_ghi) - len(cha) - len(con) - len(db) + len(theo_ten.get(None, ()))}
    mau = None if mong is None else list(mong)
    if mau is None:
        kq["do_day_du"] = kdd("khong co kiem ke dinh danh mong doi cua manh")
    else:
        du = [t for t in mau if len(theo_ten.get(t, ())) == 1 and theo_ten[t][0].get("trang_thai") == DO_DUOC and khoang_do(theo_ten[t][0])
              and all(so_do(theo_ten[t][0].get(k)) for k in ("dung_cay_s", "ca_dich_s", "ca_khac_s"))]
        kq["do_day_du"] = {"trang_thai": DO_DUOC, "so_mong": len(mau), "so_du_ba_thanh_phan": len(du), "so_thieu": len(mau) - len(du),
                           "ten_thieu": [t for t in mau if t not in du], "ten_trung": [t for t in mau if len(theo_ten.get(t, ())) > 1],
                           "ten_la": sorted(t for t in theo_ten if t is not None and t not in mau)}
        for khoa in ("dung_cay_s", "ca_dich_s", "ca_khac_s"):
            kq["tong_" + khoa] = round(sum(theo_ten[t][0].get(khoa, 0) for t in du), 3)
    tuong = giay_buoc if so_do(giay_buoc) else (cha[0].get("tuong_s") if len(cha) == 1 else None)
    ly = ("khong co kiem ke: khong doi chieu duoc tap con mong doi" if mau is None else tap_con(cha, con, mau)
          or (None if so_do(tuong) and tuong > 0 else "thieu thoi gian tuong huu han lon hon 0"))
    if ly:
        kq["doi_chieu"] = kdd(ly)
        return kq
    khoang = [(b["bat_dau"], b["ket_thuc"]) for b in con]
    hop = hop_khoang(khoang)
    kq["doi_chieu"] = {"trang_thai": DO_DUOC, "tuong_s": tuong, "hop_con_s": round(hop, 3), "tong_con_s": round(sum(b - a for a, b in khoang), 3),
                       "khong_phan_bo_s": round(tuong - hop, 3), "lech_ti_le": round(abs(tuong - hop) / tuong, 4),
                       "trong_10_phan_tram": abs(tuong - hop) / tuong <= 0.10}
    return kq


def tong_hop_g5_luot(cac_manh):
    """MOT luot: do day du thoi gian tren TOAN BO dinh danh mong doi cua ca 8 manh (nguong 95 % cua nghiem thu 4 doc o day). Thieu mot manh,
    trung manh, hay mot manh khong do duoc do day du => `khong_do_duoc`: manh mat log/dong khong duoc bien mat khoi mau so."""
    do = [m["do_day_du"] for m in cac_manh if m["do_day_du"]["trang_thai"] == DO_DUOC]
    if len(do) != SO_MANH_G5 or sorted(m["manh"] for m in cac_manh) != list(range(SO_MANH_G5)):
        return kdd(f"can du {SO_MANH_G5} manh do duoc do day du, co {len(do)} (manh {sorted(m['manh'] for m in cac_manh)})")
    mong, du = sum(d["so_mong"] for d in do), sum(d["so_du_ba_thanh_phan"] for d in do)
    return {"trang_thai": DO_DUOC, "so_mong": mong, "so_du_ba_thanh_phan": du, "so_thieu": mong - du,
            "ten_thieu": [t for d in do for t in d["ten_thieu"]], "ti_le_du": round(du / mong, 4) if mong else None,
            "dat_95_phan_tram": bool(mong) and du >= 0.95 * mong}


def them_do(bang, khoa, t):
    """Cong MOT phep do {trang_thai, gia_tri} vao bang thong ke `khoa`: do_duoc vao `v`; khong_do_duoc vao `loai` (BI LOAI nhung van duoc
    DEM, thanh `so_loai` cua `thong_ke`); khong_ap_dung vao `kad`. Khong phep do nao bien mat khoi bao cao (cung lop voi review 2, F6)."""
    o = bang.setdefault(khoa, {"v": [], "loai": 0, "kad": 0})
    if t["trang_thai"] == DO_DUOC:
        o["v"].append(t["gia_tri"])
    else:
        o["loai" if t["trang_thai"] == KHONG_DO_DUOC else "kad"] += 1


def chi_so_manh(ten):
    """`gate-cong-cu (ubuntu-latest, 3)` -> 3; ten khac dang -> None."""
    m = re.fullmatch(JOB_MANH + r" \(ubuntu-latest, (\d+)\)", ten or "")
    return int(m.group(1)) if m else None


_CONG_CU = {}


def nap_cong_cu(goc=None):
    """(module THAT `ops/cong_cu_test.py` cua cay `goc` — mac dinh cay chua bo thu nay —, KIEM KE cua no). Nap MOT lan moi cay, duoi ten khac
    `__main__` (bo ca khong chay), khong goi git, tra lai `sys.path`/`os.environ` nhu cu. Day la nguon DUY NHAT cua hop dong bien nhan:
    `_gom_manh` (phia doc), `_ket_thuc_manh` (phia ghi), `_phan_manh` va bang `DOT_BIEN`/`CA`; bo thu khong chep lai luat nao cua chung.
    KIEM KE = {sha256_test: bam byte tep test (cong thuc cua `_van_tay`), dot_bien: [[ten, ca dich], …] theo THU TU bang, ca: [ten ca]} —
    bang dot bien CUA CHINH MA, gan voi van tay nguon ma bien nhan khai (bang la ham cua chinh tep test ay)."""
    goc = pathlib.Path(goc or ROOT).resolve()
    if goc not in _CONG_CU:
        duong, env = list(sys.path), dict(os.environ)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")                    # SyntaxWarning cua module ma no import: khong phai viec cua bo thu
                spec = importlib.util.spec_from_file_location("wp1448_cong_cu", goc / "ops" / "cong_cu_test.py")
                m = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(m)
        finally:
            sys.path[:] = duong
            for k in set(os.environ) - set(env):
                del os.environ[k]
            os.environ.update(env)
        mod = vars(m)
        _CONG_CU[goc] = (mod, {"sha256_test": hashlib.sha256(pathlib.Path(mod["TEP_TEST"]).read_bytes()).hexdigest(),
                               "dot_bien": [[t, v[5]] for t, v in mod["DOT_BIEN"].items()], "ca": [f.__name__ for f in mod["CA"]]})
    return _CONG_CU[goc]


@contextlib.contextmanager
def bang_cua(mod, kk):
    """Trong khoi nay cac ham THAT cua `mod` chay tren BANG cua kiem ke `kk` (None = bang cua chinh `mod`): `DOT_BIEN` chi can ten -> ca dich
    (vi tri 5) va `CA` chi can ten ca — dung nhung gi `_gom_manh`, `_phan_manh`, `_ban_ghi_sai`, `_ket_luan_ban_ghi` doc. Luon tra bang cu."""
    cu = mod["DOT_BIEN"], mod["CA"]
    if kk is not None:
        mod["DOT_BIEN"] = {t: (None,) * 5 + (d,) for t, d in kk["dot_bien"]}
        mod["CA"] = [types.SimpleNamespace(__name__=c) for c in kk["ca"]]
    try:
        yield
    finally:
        mod["DOT_BIEN"], mod["CA"] = cu


def chon_kiem_ke(cac_van_tay, cac_kiem_ke=()):
    """Kiem ke DAU TIEN (cua cay nay truoc, roi cac kiem ke `--kiem-ke`) mang mot van tay trong `cac_van_tay`; khong co => None."""
    return next((x for x in (nap_cong_cu()[1], *cac_kiem_ke) if x["sha256_test"] in cac_van_tay), None)


def dau_khai(nd):
    """Dong dau `MANH {…}` ma mot tep manh KHAI -> dict (khong doc duoc => {}). CHI de chon kiem ke / commit doi chieu (`sha256_test`,
    `head`) o `--thu`/`--tinh`; KHONG phai phep kiem (phep kiem dong dau la `kiem_cau_truc`)."""
    try:
        d = json.loads(bytes(nd).split(b"\n", 1)[0][5:].decode("utf-8"))
    except (TypeError, ValueError):
        return {}
    return d if isinstance(d, dict) else {}


def kiem_than(than, kk, cac_ten):
    """Than MOT tep manh (cac dong `BKCON`) doi voi bang `kk` va cac dinh danh `cac_ten` -> ly do SAI | None, bang CHINH hai ham ma
    `_gom_manh` dung cho tung manh: `_nhan_ket_qua_con` (dong khong phan tich duoc, loai/do dai, ten ngoai nhom / lap / thieu, ban ghi sai
    so voi bang) va `_ket_luan_ban_ghi` (dot bien co bi giet dung khong). Bo thu khong chep luat nao cua chung va khong nuot ngoai le nao."""
    mod = nap_cong_cu()[0]
    with bang_cua(mod, kk):
        nhan, ly = mod["_nhan_ket_qua_con"](cac_ten, 0, than, ())
        if nhan is None:
            return str(ly)[:200]
        loi = sum(mod["_ket_luan_ban_ghi"](nhan[t], ())[1] for t in cac_ten)
    return f"{loi} loi dot bien" if loi else None


def kiem_cau_truc(nd, k):
    """TANG 1 — CAU TRUC cua MOT tep manh o vi tri `k`: (dong dau, than) khi dat, (None, ly do) khi HONG DA BIET. Khong nhan kiem ke, khong
    nhan tep nao khac: ket qua cua mot tep KHONG doi theo viec bo co du tam tep hay kiem ke cua nguon co san (review 3, F1).
      dau   UTF-8; dong `MANH {…}` dung bo khoa `_KHOA_DAU_MANH` cua ma, ba so nguyen, `phien_ban` = `_PHIEN_BAN_MANH`; `manh` = vi tri `k`
            cua artifact va `so_manh` = 8 (dinh danh cua vi tri); `sha256_test` 64 hex, `head` la OID;
      than  chi co dong `BKCON ` (nhu `[G-dong-la]`), va `kiem_than` DAT tren BANG TU KHAI cua chinh tep: ten -> ca dich ma dong DAU TIEN
            cua ten ay khai, tap ca = tap ca cua ban ghi `do` dau tien. Bang tu khai la bang THUAN LOI NHAT cho tep: tep dat tren mot bang
            T bat ky thi moi ban ghi mang dung ca dich va tap ca cua T, nen cung dat tren bang tu khai. Vay truot o day (JSON hong, loai /
            do dai, ten lap, trang thai / ly do la, ban ghi `loi`, dich khong bi giet, tap ca lech nhau) la truot voi MOI bang: hong cau
            truc KHONG phu thuoc kiem ke.
    Dat tang nay CHUA phai hop le: ten ngoai bang, thieu ten, ca dich / tap ca khac bang la viec cua tang 2 (`kiem_than` tren kiem ke that)."""
    mod = nap_cong_cu()[0]
    try:
        dong0, _, than = bytes(nd).decode("utf-8").partition("\n")
        dau = json.loads(dong0[5:]) if dong0.startswith("MANH ") else None
    except ValueError:                                              # UnicodeDecodeError / JSONDecodeError: dau khong doc duoc
        dau = None
    if not isinstance(dau, dict) or set(dau) != mod["_KHOA_DAU_MANH"] or any(type(dau[x]) is not int for x in ("phien_ban", "manh", "so_manh")):
        return None, "dau tep khong doc duoc hoac sai bo khoa"
    if dau["phien_ban"] != mod["_PHIEN_BAN_MANH"] or (dau["manh"], dau["so_manh"]) != (k, SO_MANH_G5):
        return None, f"dau khai phien_ban={dau['phien_ban']} manh={dau['manh']}/{dau['so_manh']} o vi tri {k}/{SO_MANH_G5}"
    if not all(isinstance(dau[x], str) and r.fullmatch(dau[x]) for x, r in (("sha256_test", RE_SHA256), ("head", RE_OID))):
        return None, "sha256_test / head sai dang"
    if any(d and not d.startswith("BKCON ") for d in than.split("\n")):
        return None, "co dong ngoai hop dong (khong mo dau `BKCON `)"
    tu, ca = {}, None
    for d in than.split("\n"):
        try:
            bg = json.loads(d[6:])
        except ValueError:
            continue                                                # dong khong doc duoc: chinh `kiem_than` ben duoi tu choi
        if isinstance(bg, list) and len(bg) > 2 and isinstance(bg[1], str):
            tu.setdefault(bg[1], bg[2] if bg[0] == "do" and isinstance(bg[2], str) else None)
            if ca is None and bg[0] == "do" and len(bg) == 4 and isinstance(bg[3], dict):
                ca = list(bg[3])
    loi = kiem_than(than, {"dot_bien": [[t, d] for t, d in tu.items()], "ca": ca or []}, list(tu))
    return (None, "ban ghi: " + loi) if loi else (dau, than)


def doi_chieu_head(h, head_run, su_kien, hop=None, cmt=None):
    """TANG 3 — head bien nhan KHAI co phai commit luot nay da checkout: True | False | None (khong do duoc). Review 4 F1: KHONG nguon nao la
    tham quyen mot minh — MOI bang chung doc lap CO SAN bo mot phieu: `hop` cua dong bong (`github.sha`; `False` = dong bong mau thuan voi luot,
    xem `dung_luot`): h == hop; luot `SU_KIEN_HEAD_LUOT`: h == head luot (khong ep luat cha-merge len push/dispatch); `pull_request` (checkout
    commit MERGE): cha REST cua h DUNG hai, cha hai = head luot. Mot phieu `False` o BAT KY dau => False; khong phieu nao => None; con lai True."""
    co_run = isinstance(head_run, str) and RE_OID.fullmatch(head_run) is not None
    phieu = [] if hop is None else [hop is not False and h == hop]
    if su_kien in SU_KIEN_HEAD_LUOT and co_run:
        phieu.append(h == head_run)
    cha = (cmt or {}).get(h) if su_kien == "pull_request" else None
    if isinstance(cha, list) and (co_run or len(cha) != 2):          # so cha sai la mau thuan ke ca khi chua biet head luot
        phieu.append(len(cha) == 2 and cha[1] == head_run)
    return False if False in phieu else (True if phieu else None)


def kiem_bien_nhan(nd, k, head_run, su_kien, hop=None, cmt=None, cac_kiem_ke=()):
    """MOT tep manh -> (trang thai, ly do, (van tay, head) tep KHAI | None) qua ba tang; khong tang nao nhin tep khac:
      khong_hop_le  HONG DA BIET: truot cau truc; co kiem ke cua van tay tep khai ma truot hop dong; head khai KHONG phai commit cua luot;
      khong_do_duoc cau truc dat, khong co gi sai DA BIET, nhung con thu CHUA kiem duoc: khong kiem ke nao mang van tay ay (ghi kem van
                    tay de biet can `--xuat-kiem-ke` cho nguon nao), hoac head chua doi chieu duoc;
      hop_le        ca ba tang DAT — bang chung duong duy nhat."""
    dau, than = kiem_cau_truc(nd, k)
    if dau is None:
        return BN_HONG, "cau_truc: " + than, None
    khai = (dau["sha256_test"], dau["head"])
    kk = chon_kiem_ke([khai[0]], cac_kiem_ke)
    loi = kiem_than(than, kk, ten_mong(khai[0], k, cac_kiem_ke)) if kk else None
    khop = doi_chieu_head(khai[1], head_run, su_kien, hop, cmt)
    if loi or khop is False:
        return BN_HONG, ("hop_dong: " + loi) if loi else "head_bien_nhan_khong_khop_luot", khai
    if kk is None or khop is None:
        return KHONG_DO_DUOC, ("khong_co_kiem_ke_cua_van_tay_bien_nhan:" + khai[0][:12]) if kk is None else "head_bien_nhan_chua_doi_chieu_duoc", khai
    return BN_HOP_LE, "-", khai


def bien_nhan_luot(manh_job, artifact, noi_dung, head_run, hop=None, cmt=None, cac_kiem_ke=(), su_kien="pull_request"):
    """Trang thai TUNG bien nhan manh va ket luan cua ca bo.

    `manh_job`: {k: dong job} (attempt cuoi, mang sang) · `artifact`: {k: 'co' | 'het_han'} cua danh sach artifact DA DU, hoac
    None = khong co danh sach · `noi_dung`: {k: byte tep manh} (vang = chua lay duoc) · `hop`: merge ref (`github.sha`) tu dong
    bong, hoac None · `cmt`: {sha: [cha...]} cua head bien nhan (REST, --thu) · `cac_kiem_ke`: kiem ke them (`--kiem-ke`) · `su_kien`
    cua luot. Moi vi tri dung MOT trang thai, quyet dinh RIENG cho vi tri ay:
      thieu         danh sach artifact da du ma vang tep; hoac khong co danh sach va job khong `success` (khong buoc upload nao chay);
      khong_do_duoc het han / chua tai — KHONG suy tu job `success`; hoac tep co mat ma con thu chua kiem duoc (`kiem_bien_nhan`);
      khong_hop_le  job mang head khac luot; hoac tep co mat va HONG DA BIET (`kiem_bien_nhan`);
      hop_le        tep co mat va qua ca ba tang.
    Buoc xet TAP chi co the HA: cac tep dat cau truc ma khai (van tay, head) KHAC NHAU thi ca nhom la `khong_hop_le` (mot luot chi co mot
    commit va mot nguon). Tra {trang_thai, ly_do, du_noi_dung, che_do, kiem_ke, thieu}: `du_noi_dung` chi khi CA tam vi tri `hop_le`; `che_do`
    cua bo da duoc nhan la `du` — hop dong HIEN TAI chi co MOT che do va dong dau mang khoa khac bi tu choi o tang cau truc; `dich` chi co tu
    PR6, khi ay nhan che do phai lay tu CHINH hop dong moi, khong doan o day. `kiem_ke` = van tay cua kiem ke ma ca bo da qua."""
    tt, ly, khai = [KHONG_DO_DUOC] * SO_MANH_G5, ["-"] * SO_MANH_G5, {}
    for k in range(SO_MANH_G5):
        d, nd = manh_job.get(k), (noi_dung or {}).get(k)
        art = None if artifact is None else artifact.get(k, "vang")
        if d is not None and head_run is not None and d.get("head_sha") not in (None, head_run):
            tt[k], ly[k] = BN_HONG, "job_mang_head_khac_luot"
        elif isinstance(nd, (bytes, bytearray)):
            tt[k], ly[k], vt = kiem_bien_nhan(nd, k, head_run, su_kien, hop, cmt, cac_kiem_ke)
            if vt:
                khai[k] = vt
        elif art == "vang":
            tt[k], ly[k] = BN_THIEU, "artifact_vang"
        elif art is None and (d is None or d.get("ket_luan") != "success"):
            tt[k], ly[k] = BN_THIEU, "job_khong_success"
        else:
            tt[k], ly[k] = KHONG_DO_DUOC, "artifact_het_han" if art == "het_han" else "noi_dung_chua_lay"
    if len(set(khai.values())) > 1:
        for k in khai:
            tt[k], ly[k] = BN_HONG, "bo_khai_van_tay_hoac_head_khac_nhau"
    du = tt == [BN_HOP_LE] * SO_MANH_G5
    return {"trang_thai": tt, "ly_do": ly, "du_noi_dung": du, "che_do": "du" if du else None, "kiem_ke": khai[0][0] if du else None,
            "thieu": any(x in (BN_HONG, BN_THIEU) for x in tt)}


def ten_mong(van_tay, k, cac_kiem_ke=()):
    """Dinh danh dot bien MONG DOI cua manh `k` theo kiem ke mang van tay `van_tay` (None / khong kiem ke nao mang => None: khong do
    duoc): CHINH `_phan_manh` cua ma tren bang cua kiem ke ay. Day la MAU SO cua do day du thoi gian — khong suy tu cac dong dang xet."""
    kk = chon_kiem_ke([van_tay], cac_kiem_ke) if van_tay else None
    return None if kk is None else nap_cong_cu()[0]["_phan_manh"](k, SO_MANH_G5, [t for t, _ in kk["dot_bien"]])


def dung_luot(run, dong, log=None, artifact=None, bien_nhan=None, cmt=None, kiem_ke=()):
    """Ban ghi CHUAN HOA cua mot luot ci.yml o attempt CUOI, tu: `run` (API), `dong` (dong job: ten, ket_luan, run_attempt,
    head_sha, job_id — moi attempt), `log` ({'chuan_bi': van ban | None, 'gom': van ban | None}), `artifact` (danh sach artifact
    DA DU: ten (chuoi) hoac {name, expired}; None = khong co danh sach), `bien_nhan` ({k: byte tep manh}), `cmt` ({sha: [cha]}) va
    `kiem_ke` (kiem ke them ngoai kiem ke cua cay nay).
    Dong cua attempt cuoi duoc uu tien; job khong chay lai o attempt cuoi lay dong moi nhat cua no (mang sang)."""
    log = log or {}
    so_att = so_lan(run.get("run_attempt"))
    moi_nhat = {}
    for d in sorted(dong, key=lambda d: (so_lan(d.get("run_attempt")) or 0, d.get("job_id") or 0)):
        if so_att and (so_lan(d.get("run_attempt")) or so_att + 1) <= so_att:      # attempt khong hop le: khong bao gio la dong moi nhat
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
    if RE_OID.fullmatch(str(pl.get("dau"))) and RE_OID.fullmatch(str(head)) and pl["dau"] != head:
        hop = False                                         # review 4 F1: dong bong khai head KHAC luot => mau thuan DA BIET, phu quyet
    bn = bien_nhan_luot(manh, art, bien_nhan, head, hop, cmt, kiem_ke, run.get("event"))
    return {"run_id": run.get("id"), "attempt": so_att, "su_kien": run.get("event"), "head": head, "ket_luan": run.get("conclusion"),
            "chuan_bi": cb.get("ket_luan") if cb else None, "co_log_chuan_bi": isinstance(log.get("chuan_bi"), str),
            "lan_cu": lan_cu, "che_do_chay": tb["che_do_chay"], "cong_cu_that": tb["cong_cu_that"],
            "bong_cong_cu": tb["bong_cong_cu"], "bong_phan_loai": tb["bong_phan_loai"],
            "che_do_g5": "du",                                      # `dich` chi co tu PR6; bien nhan khi ay phai mang truong che do
            "gom": {"ket_luan": gom.get("ket_luan") if gom else None, "dau": trich_gom(log["gom"]) if isinstance(log.get("gom"), str) else None,
                    "co_log": isinstance(log.get("gom"), str)},
            "manh": {"ket_luan": [manh[k].get("ket_luan") if k in manh else None for k in range(SO_MANH_G5)],
                     "bien_nhan": bn["trang_thai"], "ly_do": bn["ly_do"], "du_noi_dung": bn["du_noi_dung"],
                     "che_do_bien_nhan": bn["che_do"], "kiem_ke": bn["kiem_ke"], "thieu": bn["thieu"],
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
    """Du 8 bien nhan hop le cua CHE DO `che_do` — CHI bang chung duong (review 3, F1): CA tam vi tri `hop_le` (moi tep co mat, dat cau
    truc, dat hop dong tren kiem ke cua no, head doi chieu duoc) va bo mang dung che do. KHONG co duong lui: job `success`, ten artifact
    hay dau `GOM MẢNH 8/8` cua job gom khong bao gio thay duoc mot bien nhan vang, het han, khong kiem duoc hay hong."""
    manh = l.get("manh") or {}
    return manh.get("bien_nhan") == [BN_HOP_LE] * SO_MANH_G5 and manh.get("che_do_bien_nhan") == che_do


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


def doc_kiem_ke(thu_muc):
    """[kiem ke] cua moi tep `*.json` trong thu muc `--kiem-ke` (None => []). Thu muc vang, tep sai hinh dang hay hai tep cung mot van tay
    => `AnhChupHong` (dau vao DA CHI DINH ma hong: tu choi, khong lang le bo qua). Mot kiem ke chi co hieu luc voi bien nhan khai DUNG
    `sha256_test` cua no; no la LOI KHAI cua nguoi cap (do `--xuat-kiem-ke` xuat tu ma) — `--tinh` ghi bam noi dung cua tung kiem ke vao meta."""
    if thu_muc and not pathlib.Path(thu_muc).is_dir():
        raise AnhChupHong(f"--kiem-ke {thu_muc}: khong phai thu muc")
    kq = []
    for tep in sorted(pathlib.Path(thu_muc).glob("*.json")) if thu_muc else ():
        try:
            kk = json.loads(tep.read_bytes())
            ten = [t for t, _ in kk["dot_bien"]]
            if not (RE_SHA256.fullmatch(kk["sha256_test"]) and ten and len(set(ten)) == len(ten) and len(set(kk["ca"])) == len(kk["ca"])
                    and all(isinstance(x, str) for x in ten + kk["ca"] + [d for _, d in kk["dot_bien"]])):
                raise ValueError("sai hinh dang kiem ke")
            if kk["sha256_test"] in [x["sha256_test"] for x in kq]:
                raise ValueError("hai kiem ke cung mot van tay")
        except (OSError, ValueError, KeyError, TypeError) as e:
            raise AnhChupHong(f"kiem ke {tep.name} khong dung duoc ({type(e).__name__}: {e})") from e
        kq.append(kk)
    return kq


def lenh_xuat_kiem_ke(ns):
    ra = pathlib.Path(ns.ra).resolve()
    if ROOT == ra or ROOT in ra.parents:
        print("TU CHOI GHI: thu muc --ra phai nam NGOAI kho")
        return 4
    kk = nap_cong_cu(ns.kho)[1]
    ra.mkdir(parents=True, exist_ok=True)
    (ra / (kk["sha256_test"] + ".json")).write_bytes(xuat_json(kk))
    print(f"KIEM KE {kk['sha256_test']}: {len(kk['dot_bien'])} dot bien, {len(kk['ca'])} ca (ma cua {pathlib.Path(ns.kho).resolve()})")
    return 0


class GitBiCam(RuntimeError):
    """`--tinh` da thu phong `git` (dac ta muc 5 cam): lan thu bi tu choi TRUOC khi phong va duoc ghi lai."""


@contextlib.contextmanager
def cam_git():
    """Trong khoi nay moi lan phong tien trinh `git` qua `subprocess` (ke ca tu module duoc nap: `run`/`check_output`/`call` deu qua
    `Popen`) bi TU CHOI truoc khi phong (`GitBiCam`) va duoc GHI vao danh sach tra ve — nguoi goi doc DANH SACH, vi ma duoc nap co the
    nuot ngoai le. Tien trinh khac khong bi dung toi. Luon tra `subprocess.Popen` nhu cu (review 3, F7)."""
    goc, goi = subprocess.Popen, []

    class Chan(goc):
        def __init__(self, *a, **k):
            lenh = a[0] if a else k.get("args")
            dau = os.fsdecode(lenh).split()[:1] if isinstance(lenh, (str, bytes, os.PathLike)) else [os.fsdecode(x) for x in list(lenh)[:1]]
            if dau and pathlib.PurePath(dau[0]).name.lower() in ("git", "git.exe"):
                goi.append([os.fsdecode(x) for x in ([lenh] if isinstance(lenh, (str, bytes, os.PathLike)) else lenh)])
                raise GitBiCam(f"--tinh khong duoc goi git: {goi[-1][:4]}")
            super().__init__(*a, **k)
    subprocess.Popen = Chan
    try:
        yield goi
    finally:
        subprocess.Popen = goc


def s6_khong_cay_song():
    """Thay `phan_loai_s6` cua bo thu #1434 trong `--tinh` v2. Ban goc chay hai bo phan loai tren CAY SONG cua kho (`tim()` cua
    `.claude/dev/ci_dang_ky_test.py` phong `git check-ignore`): do khong phai du lieu cua anh chup va trai "tinh lai khong goi git". Anh chup
    khong mang muc §6, nen ban tinh lai ghi THANG la khong do duoc — khong lay du lieu cay song de lap cho trong. BASELINE.json khong doc muc nay."""
    ly = "khong_do_duoc (--tinh v2: muc §6 la phep chay tren cay song, khong co trong anh chup; ban da do: ops/specs/wp1434-r3/do/BAO_CAO.md)"
    return {"tap_duong_dan": [], "ci_duong_nhanh": ly, "tim": ly}


def phan_loai_luot(g, r, nguon, dong_tho):
    """(`tinh_luot` cua #1434 | None, ly do thoi gian G5 cua CA luot khong do duoc | None) — chung cho `--thu` (chon log manh) va `--tinh` (review 4
    F6). Attempt doc duoi CHINH khoa `att/<id>/<k>` ma `--thu` ghi; `run_attempt` sai, attempt thieu, dong job sai kieu => ly do NEU TEN, khong nem."""
    n = so_lan(r.get("run_attempt"))
    if n is None:
        return None, f"run_attempt khong phai so nguyen 1..{TRAN_ATTEMPT}: {r.get('run_attempt')!r}"
    tao = {1: r.get("created_at")}
    for k in range(1, n + 1) if n > 1 else ():
        d = json.loads(nguon(f"att/{r['id']}/{k}") or b"null")
        tao[k] = d.get("created_at") if isinstance(d, dict) else None
    try:
        lu = g.tinh_luot(r, tao, dong_tho)
    except (ValueError, TypeError, OverflowError, AttributeError) as e:
        return None, f"dong job cua luot khong phan loai duoc ({type(e).__name__})"
    return lu, (f"thieu ban ghi attempt {thieu} cua luot: khong tach duoc dong thuc thi / mang sang"
                if (thieu := [k for k, v in tao.items() if v is None and n > 1]) else None)


def lenh_tinh(ns):
    with cam_git() as goi:
        return _tinh(ns, goi)


def _tinh(ns, goi):
    ac, ra = pathlib.Path(ns.anh_chup).resolve(), pathlib.Path(ns.ra).resolve()
    if ROOT == ra or ROOT in ra.parents:
        print("TU CHOI GHI: thu muc --ra phai nam NGOAI kho")
        return 4
    # review F5: anh chup v2 DA CHI DINH thi kiem toan ven TRUOC moi tinh toan (va truoc ca bo thu #1434); vang `--anh-chup-v2`
    # la "khong co v2" hop le, con chi dinh ma hong thi TU CHOI (rc 3, cung ma voi anh chup #1434 lech MANIFEST).
    doc2, theo_khoa2, man2 = None, {}, None
    try:
        cac_kk = doc_kiem_ke(ns.kiem_ke)
        if ns.anh_chup_v2:
            doc2, theo_khoa2 = doc_anh_chup(ns.anh_chup_v2)
            man2 = hashlib.sha256((pathlib.Path(ns.anh_chup_v2).resolve() / "MANIFEST.json").read_bytes()).hexdigest()
    except AnhChupHong as e:
        print("ANH CHUP V2 / KIEM KE HONG:", e)
        return 3
    g = nap_goc()
    g.phan_loai_s6 = s6_khong_cay_song
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
    luot, buoc, khong_do, bo_dem, g5 = [], {}, [], {"loi_ich": {"1": 0, "0": 0, "khong_du_du_lieu": 0}, "ton_du": {"1": 0, "0": 0, "khong_du_du_lieu": 0}}, {}
    # Luot DUOC CHON (`--run-g5`, ghi o META cua anh chup v2) ma NGOAI cohort cua anh chup #1434 (no chi liet ke pull_request + push master):
    # `--thu` da thu rieng `run/<id>` + `jobs/<id>` vao anh chup v2. Chung CHI vao phan thoi gian G5, khong vao G4 / bong / thoi gian buoc.
    chon = [x for x in (json.loads(doc2("META") or b"{}").get("run_g5") or [] if doc2 else []) if type(x) is int]
    ngoai = [json.loads(doc2(f"run/{x}")) for x in chon if x not in {r["id"] for r in co_ci} and doc2(f"run/{x}")]
    ly_luot = {}                                            # rid -> ly do thoi gian G5 cua CA luot khong do duoc (review 4 F6)
    for r, nguon in [(r, doc) for r in co_ci] + [(r, doc2) for r in ngoai]:
        rid, (dong_tho, du, _, ly) = r["id"], g.chon_chuoi_trang(nguon, f"jobs/{r['id']}")
        lu, ly = phan_loai_luot(g, r, nguon, dong_tho) if du else (None, ly or "danh sach job khong du")
        if ly:
            ly_luot[rid] = ly
            khong_do.append({"doi_tuong": f"luot {rid}", "ly_do": ly})
        if lu is None:
            continue
        dong = [{"ten": m["ten"], "ket_luan": m["ket_luan"], "run_attempt": m["run_attempt"], "job_id": m["job_id"],
                 "head_sha": m["_tho"].get("head_sha")} for m in lu["dong"]]
        cb = [m for m in lu["dong"] if m["ten_goc"] == JOB_CHUAN_BI]
        gom = [m for m in lu["dong"] if m["ten_goc"] == JOB_GOM]
        log = {"chuan_bi": van_ban(f"log/{cb[-1]['job_id']}", nguon) if cb else None,
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
                sha = dau_khai(nd).get("head")
                bc = doc2(f"cmt/{sha}") if isinstance(sha, str) and RE_OID.fullmatch(sha) else None
                try:
                    cmt[str(sha)] = [p["sha"] for p in json.loads(bc)["parents"]] if bc is not None else None
                except (ValueError, KeyError, TypeError):
                    cmt[str(sha)] = None
        l = dung_luot(r, dong, log, art, bn, {k: v for k, v in cmt.items() if v is not None}, cac_kk)
        lan = g.trich_lan(log["chuan_bi"]) if log["chuan_bi"] else None
        for m in lu["dong"]:                                  # thoi gian theo buoc cua gate / gate-ops (dong thuc_thi)
            if nguon is doc and m["loai_dong"] == g.THUC_THI and m["ten_goc"] in JOB_BUOC_V2:
                for b in m["_tho"].get("steps") or []:
                    them_do(buoc, f"{m['ten_goc']} | {m['nen']} | {lan or 'khong_do_duoc'} | {b.get('name')}", g.thoi_luong_buoc(b))
            k = chi_so_manh(m["ten"])
            # MOI manh co log DA THU (`--run-g5`) deu vao bao cao — ke ca log khong con dong `G5_THOI_GIAN` nao hay log khong lay duoc;
            # attempt MOI NHAT cua tung manh. Mau so = dinh danh mong doi theo kiem ke cua CHINH luot (bo bien nhan `hop_le` cua no, moi
            # su kien); luot chua co kiem ke thi manh `khong_do_duoc` va `ly_do_kiem_ke` neu trang thai tung bien nhan.
            if (doc2 and m["loai_dong"] == g.THUC_THI and k is not None and f"log/{m['job_id']}" in theo_khoa2 and rid not in ly_luot
                    and (m["run_attempt"], m["job_id"]) >= g5.get((rid, k), {}).get("_moi", (0, 0))):
                vb = van_ban(f"log/{m['job_id']}", doc2)
                b_g5 = next((g.thoi_luong_buoc(b) for b in m["_tho"].get("steps") or [] if str(b.get("name", "")).startswith("G5 manh")), None)
                g5[(rid, k)] = {"run_id": rid, "job_id": m["job_id"], "manh": k, "ket_luan": m["ket_luan"], "co_log": vb is not None,
                                "_moi": (m["run_attempt"], m["job_id"]), "su_kien": l["su_kien"], "kiem_ke": l["manh"]["kiem_ke"],
                                "ly_do_kiem_ke": None if l["manh"]["kiem_ke"] else sorted(set(l["manh"]["ly_do"])),
                                **tong_hop_g5(trich_g5(vb or ""), b_g5["gia_tri"] if b_g5 and b_g5["trang_thai"] == DO_DUOC else None,
                                              ten_mong(l["manh"]["kiem_ke"], k, cac_kk) if vb is not None else None)}
        if nguon is not doc:
            continue
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
        tg, thieu_jobs = {}, 0
        for r in ds_pl if du_pl else []:
            dong_tho, du, _, _ = g.chon_chuoi_trang(doc2, f"jobs/{r['id']}")
            thieu_jobs += 0 if du else 1
            for d in (dong_tho if du else []):
                them_do(tg, "job", g.kad("job skipped") if d.get("conclusion") == "skipped" else g.khoang_giay(d.get("started_at"), d.get("completed_at")))
        tg = tg.get("job", {"v": [], "loai": 0, "kad": 0})
        pl = ({"trang_thai": DO_DUOC if not thieu_jobs else KHONG_DO_DUOC, "so_luot": len(ds_pl), "so_luot_thieu_jobs": thieu_jobs,
               "so_job_khong_do_duoc": tg["loai"], "giay_job": g.thong_ke(tg["v"], thieu_jobs + tg["loai"])} if du_pl else kdd(ly))
    v2 = {"meta": {"packet": "wp1448", "revision": 2, "spec_sha256": SPEC_SHA256, "anh_chup": {k: meta.get(k) for k in ("T0", "T1", "sha_master")},
                   "manifest_sha256": hashlib.sha256((ac / "MANIFEST.json").read_bytes()).hexdigest(),
                   "cohort_goc": bool(cohort_goc), "co_anh_chup_v2": bool(doc2), "manifest_v2_sha256": man2, "so_lan_thu_goi_git": len(goi),
                   "kiem_ke": {"cua_cay": next((kk["sha256_test"] for _, kk in _CONG_CU.values()), None),
                               "them": {kk["sha256_test"]: hashlib.sha256(xuat_json(kk)).hexdigest() for kk in cac_kk}},
                   "nen_sha256": hashlib.sha256((ra / "nen" / "BASELINE.json").read_bytes()).hexdigest(),
                   "BASELINE_goc_sha256": hashlib.sha256(NEN_GOC.read_bytes()).hexdigest()},
          "tai_lap_khoa": doi_chieu_khoa(nen_moi, nen_goc),
          "G4": tong_hop_g4([l for l in luot if l["su_kien"] == "pull_request"]),
          "bong": {"so_luot_co_dong_BONG_CONG_CU": sum(1 for l in luot if l["bong_cong_cu"]),
                   "so_luot_co_dong_BONG_PHAN_LOAI": sum(1 for l in luot if l["bong_phan_loai"]),
                   "BONG_CONG_CU_theo_quyet_dinh": dem([l["bong_cong_cu"]["quyet_dinh"] for l in luot if l["bong_cong_cu"]]),
                   "BONG_CONG_CU_theo_duong_dan": dem([l["bong_cong_cu"].get("duong_dan") for l in luot if l["bong_cong_cu"]]),
                   "bo_dem_pull_request": bo_dem},
          "thoi_gian_buoc_gate_gate_ops": {k: dict(g.thong_ke(o["v"], o["loai"]), so_khong_ap_dung=o["kad"]) for k, o in sorted(buoc.items())},
          "g5_thoi_gian": ({"so_manh_co_log": len(g5), "manh": [{k: v for k, v in g5[x].items() if k != "_moi"} for x in sorted(g5)],
                            "theo_luot": {str(rid): (kdd(ly_luot[rid]) if rid in ly_luot else tong_hop_g5_luot([m for (r_, _), m in sorted(g5.items()) if r_ == rid])
                                                     if rid in {x[0] for x in g5} else kdd("luot duoc chon (--run-g5) nhung anh chup v2 khong co log manh nao cua no"))
                                          for rid in sorted({x[0] for x in g5} | set(chon))}}
                           if doc2 else kdd("chua thu log manh G5 (--thu --run-g5 …)")),
          "packet_loop_dot_bien": pl, "khong_do_duoc": khong_do, "luot": luot}
    if goi:                                                 # ma duoc nap co the da nuot `GitBiCam`: doc DANH SACH, khong doc ngoai le
        print(f"TU CHOI: --tinh da thu goi git {len(goi)} lan (dac ta muc 5), khong ghi ket qua v2: {goi[:3]}")
        return 5
    b = xuat_json(v2)
    (ra / "BASELINE_V2.json").write_bytes(b)
    (ra / "BAO_CAO_V2.md").write_bytes(bao_cao(v2).encode("utf-8"))
    print("BASELINE_V2.json sha256", hashlib.sha256(b).hexdigest())
    for d in v2["tai_lap_khoa"]:
        print(f"  {d['ket_luan']:14} {d['khoa']}")
    return 0


def dem(ds):
    s = [str(x) for x in ds]
    return {k: s.count(k) for k in sorted(set(s))}


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
    dong.append("## G5 — do day du thoi gian theo luot (mau so = dinh danh mong doi cua ca 8 manh)\n\n"
                + json.dumps(v2["g5_thoi_gian"].get("theo_luot", v2["g5_thoi_gian"]), ensure_ascii=False) + "\n")
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
            dau_bn |= {h for h in [dau_khai(nd or b"").get("head")] if isinstance(h, str) and RE_OID.fullmatch(h)}
    t.song_song([lambda h=h: t.lay(f"cmt/{h}", f"commits/{h}", f"cmt/{h}.json", "commit") for h in sorted(dau_bn)])


def ke_hoach_thu(su_kien, cac_job, duoc_chon, co_kho=False):
    """Viec phai thu cua MOT luot ci.yml (ham THUAN) -> {log: [job id], bien_nhan: bool, oracle: job id chuan-bi | None}. `cac_job`: dong
    job o attempt CUOI theo ten; `duoc_chon`: luot co ten o `--run-g5`. LOG: job gom da chay; va moi manh da chay cua luot duoc chon.
    BIEN NHAN (danh sach artifact + noi dung + commit cua head khai): moi luot `pull_request` (G4) VA moi luot duoc chon BAT KE su kien
    (review 3, F6) — kiem ke mong doi cua thoi gian G5 la cua CHINH luot ay; khong thu bien nhan thi do day du cua no khong bao gio do duoc."""
    log = [d["id"] for ten, d in cac_job.items()
           if ((ten or "").startswith(JOB_GOM + " (ubuntu-latest") and d.get("conclusion") not in ("skipped", None))
           or (duoc_chon and chi_so_manh(ten) is not None and d.get("conclusion") != "skipped")]
    cb = cac_job.get(JOB_CHUAN_BI)
    return {"log": log, "bien_nhan": su_kien == "pull_request" or duoc_chon, "oracle": cb["id"] if co_kho and cb and su_kien == "pull_request" else None}


def lenh_thu(ns, g=None):
    """`g`: module bo thu #1434 (mac dinh nap tu kho); --tu-kiem trao ban co lop `Thu` van chuyen gia (khong mang)."""
    if g is None and not os.environ.get("GITHUB_PAT"):
        raise SystemExit("thieu bien moi truong GITHUB_PAT")
    g = g or nap_goc()
    ac = pathlib.Path(ns.anh_chup).resolve()
    try:
        doc, _ = doc_anh_chup(ac)
    except AnhChupHong as e:
        raise SystemExit(f"anh chup #1434 khong dung duoc: {e}") from e
    meta = json.loads((ac / "META.json").read_bytes())
    t = g.Thu(ns.ra, ns.han_giay, ns.so_luong)
    if t.ra == ac or ac in t.ra.parents:
        raise SystemExit("anh chup v2 phai la thu muc RIENG, khong nam trong anh chup #1434")
    run_g5 = sorted({int(x) for x in (ns.run_g5 or "").split(",") if x.strip().isdecimal()})
    g.ghi_tep(t.ra, "META.json", xuat_json({"packet": "wp1448", "revision": 2, "run_g5": run_g5,
                                            "anh_chup_goc": {k: meta.get(k) for k in ("T0", "T1", "sha_master")}}))
    ds_ci = []
    for k in meta["khoang_con"]:
        if not k.get("chia_doi"):
            ds_ci += g.chon_chuoi_trang(doc, f"list/ci/{k['su_kien']}/{k['nhan']}")[0]
    co_ci, _ = g.loc_cohort(sorted({r["id"]: r for r in ds_ci}.values(), key=lambda r: r["id"]), g.WF_CI, meta["T0"], meta["T1"])

    def doc_t(k):
        return (t.ra / t.muc[k]["duong_dan"]).read_bytes() if k in t.muc and t.muc[k].get("duong_dan") else None
    ngoai = [x for x in run_g5 if x not in {r["id"] for r in co_ci}]      # duoc chon ma ngoai cohort #1434 (vd workflow_dispatch): thu chinh luot ay
    for x in ngoai:
        d = t.doc(t.lay(f"run/{x}", f"actions/runs/{x}", f"run/{x}.json", "run"))
        t.trang(f"jobs/{x}", f"actions/runs/{x}/jobs?filter=all", f"jobs/{x}", "jobs", "jobs")
        n = so_lan(d.get("run_attempt")) if isinstance(d, dict) else None    # review 4 F6: ban ghi attempt ma `--tinh` can, co tran
        for k in range(1, n + 1) if n and n > 1 else ():
            t.lay(f"att/{x}/{k}", f"actions/runs/{x}/attempts/{k}", f"att/{x}/{k}.json", "attempt")
    viec, oracle, co_bn = [], [], []
    for r, nguon in [(r, doc) for r in co_ci] + [(json.loads(doc_t(f"run/{x}")), doc_t) for x in ngoai if doc_t(f"run/{x}")]:
        rid = r["id"]
        dong, du, _, _ = g.chon_chuoi_trang(nguon, f"jobs/{rid}")
        if not du:
            continue
        cuoi = {}
        for d in sorted(dong, key=lambda d: (so_lan(d.get("run_attempt")) or 0, d.get("id") or 0)):
            cuoi[d.get("name")] = d
        # review 4 F6: log manh = dong THUC_THI MOI NHAT theo CHINH phep phan loai `--tinh` doc (ban mang sang co id moi, khong mang log that)
        lu = phan_loai_luot(g, r, nguon, dong)[0] if rid in run_g5 else None
        cuoi.update({m["ten"]: m["_tho"] for m in (lu or {}).get("dong", ()) if m["loai_dong"] == g.THUC_THI and chi_so_manh(m["ten"]) is not None})
        kh = ke_hoach_thu(r.get("event"), cuoi, rid in run_g5, bool(ns.kho) and nguon is doc)
        viec += [lambda j=j: t.lay(f"log/{j}", f"actions/jobs/{j}/logs", f"log/{j}.log", "log") for j in kh["log"]]
        b = doc(f"log/{kh['oracle']}") if kh["oracle"] else None
        pl = trich_bong(b.decode("utf-8", errors="replace"))["bong_phan_loai"] if b else None
        if pl:
            oracle.append((rid, pl))
        if kh["bien_nhan"]:
            co_bn.append(rid)
            viec.append(lambda rid=rid: t.trang(f"arts/{rid}", f"actions/runs/{rid}/artifacts", f"arts/{rid}", "artifacts", "artifacts"))
    ds_pl, _, _ = t.trang("list/pl", f"actions/workflows/{WF_PL}/runs?created={meta['T0']}..{meta['T1']}", "list/pl", "list", "workflow_runs")
    viec += [lambda rid=r["id"]: t.trang(f"jobs/{rid}", f"actions/runs/{rid}/jobs?filter=all", f"jobs/{rid}", "jobs", "jobs") for r in ds_pl]
    t.song_song(viec)
    thu_bien_nhan(t, g, co_bn)
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


def khong_nem(f):                                    # phep TOAN PHAN (review 4 F6): DUNG hai loi doi so khong an toan -> `TuKiemDo`
    try:
        return f()
    except (OverflowError, ValueError) as e:
        raise TuKiemDo(f"nem {type(e).__name__} thay vi tra trang thai khong do duoc / thieu: {e}") from e


def tao_bien_nhan(head, kk=None, so_manh=SO_MANH_G5, **sua):
    """{k: byte tep manh} do CHINH phia ghi cua ma dung (`_ket_thuc_manh` + `_ban_ghi_du_gia`, tren bang cua kiem ke `kk` hoac cua cay nay) —
    --tu-kiem khong con ban ghi tu che. `sua`: khoa de len dong dau cua MOI tep SAU khi ghi (vd `che_do` — hop dong gom HIEN TAI khong co
    khoa nay —, hay `sha256_test` cua mot nguon khong kiem ke nao mang)."""
    mod, cay = nap_cong_cu()
    kq = {}
    with tempfile.TemporaryDirectory(prefix="wp1448_bn_") as d, bang_cua(mod, kk):
        for k in range(so_manh):
            cac, tep = mod["_phan_manh"](k, so_manh), pathlib.Path(d) / f"manh-{k}.txt"
            mod["_ket_thuc_manh"](k, so_manh, str(tep), cac, {t: mod["_ban_ghi_du_gia"](t) for t in cac}, None,
                                  {"sha256_test": (kk or cay)["sha256_test"], "head": head})
            kq[k] = tep.read_bytes()
    return {k: sua_dau(nd, **sua) for k, nd in kq.items()} if sua else kq


def sua_dau(nd, **sua):
    """Tep manh voi dong dau `MANH {…}` da sua vai khoa (chi cho --tu-kiem)."""
    dau, _, than = nd.partition(b"\n")
    return ("MANH " + json.dumps({**json.loads(dau[5:]), **sua}, sort_keys=True)).encode("utf-8") + b"\n" + than


def luot_fixture(fx, F=None):
    """Ban ghi luot cua MOT fixture G4b: `bien_nhan` = {"tao": {head, <khoa dong dau de len>…}, "sua": {k: chuoi | null}} (phia ghi THAT, bang cua cay nay)
    hoac {"tep": <fixture luot THAT>} (dong dau, danh sach artifact, commit va KIEM KE cua chinh luot ay; bang phan quyet tung ca do phia ghi
    that dung lai). `ghi_de` de len ban ghi (khoa `manh` de tung truong) — chi cho fixture MO PHONG."""
    F = F or DAY / "fixtures"
    spec, bn, cmt, art, kk = fx.get("bien_nhan") or {}, None, fx.get("cmt"), fx.get("artifact"), ()
    if "tao" in spec:
        bn = tao_bien_nhan(**spec["tao"])
    if "tep" in spec:
        that = json.loads((F / spec["tep"]).read_text(encoding="utf-8"))
        kk, cmt, art = (that["kiem_ke"],), that["cmt"], art if art is not None else that["artifact"]
        bn = tao_bien_nhan(dau_khai(that["manh"]["0"]["dau_nguyen_van"].encode())["head"], that["kiem_ke"])
    for k, v in (spec.get("sua") or {}).items():
        if v is None:
            bn.pop(int(k), None)
        else:
            bn[int(k)] = v.encode("utf-8")
    l = dung_luot(fx["run"], fx["dong"], fx.get("log"), art, bn, cmt, kk)
    gd = dict(fx.get("ghi_de") or {})
    l["manh"].update(gd.pop("manh", {}))
    l.update(gd)
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
             f"luot 44443875641 (du 8 bien nhan hop_le tren kiem ke cua chinh luot, gom cancelled) phai ra gom_hong: {kq} {l['manh']}")
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
        bg, M = trich_g5(vb), ["db_a", "db_b", "db_thieu"]
        t = tong_hop_g5(bg, 40, M)
        dd = t["do_day_du"]
        bang(len(bg) == 7 and dd["so_mong"] == 3 and dd["so_du_ba_thanh_phan"] == 2 and dd["so_thieu"] == 1 and dd["ten_thieu"] == ["db_thieu"],
             f"ba dot bien mong doi, mot thieu thanh phan: {t}")
        co_khoang = tong_hop_g5([{**b, "bat_dau": 1.0, "ket_thuc": 2.0} if b.get("ten") == "db_thieu" else b for b in bg], 40, M)["do_day_du"]
        bang(co_khoang["so_du_ba_thanh_phan"] == 2 and co_khoang["ten_thieu"] == ["db_thieu"], f"co khoang nhung thieu thanh phan ca dich van la thieu: {co_khoang}")
        dc = t["doi_chieu"]
        bang(dc["trang_thai"] == DO_DUOC and dc["hop_con_s"] == 20.0 and dc["tong_con_s"] == 25.0 and dc["khong_phan_bo_s"] == 20.0
             and dc["trong_10_phan_tram"] is False, f"doi chieu bang HOP (con chong nhau van hop le), phan lech la khong phan bo: {dc}")
        gan = tong_hop_g5(bg, 21, M)["doi_chieu"]
        bang(gan["trong_10_phan_tram"] is True and gan["khong_phan_bo_s"] == 1.0, f"lech duoi 10 % thi dat: {gan}")
        bang(tong_hop_g5([b for b in bg if b.get("loai") != "con"], 40, M)["doi_chieu"]["trang_thai"] == KHONG_DO_DUOC, "khong co khoang con => khong_do_duoc")
        bang(trich_g5("G5_THOI_GIAN {hong}\n")[0]["trang_thai"] == KHONG_DO_DUOC, "dong hong => ban ghi khong_do_duoc")

    @kiem
    def g5_mau_so_la_dinh_danh_mong_doi():
        """review 2 (F6): do day du thoi gian tinh tren dinh danh MONG DOI; dong mat, hong, trung hay con mat khong duoc lam mau so co lai."""
        bg = trich_g5((F / "log_manh_g5.log").read_text(encoding="utf-8"))
        db = [b for b in bg if b.get("loai") == "dot_bien"]
        con = [b for b in bg if b.get("loai") == "con"]
        cha = [b for b in bg if b.get("loai") == "cha"]
        M = ["db_a", "db_b", "db_thieu", "db_vang"]
        dd = tong_hop_g5(bg, 40, M)["do_day_du"]
        bang([dd["so_mong"], dd["so_du_ba_thanh_phan"], dd["so_thieu"], dd["ten_thieu"]] == [4, 2, 2, ["db_thieu", "db_vang"]],
             f"dinh danh mong doi VANG dong la thieu, co ten (khong phai 2/3): {dd}")
        mat = tong_hop_g5([b for b in bg if b.get("ten") != "db_a"] + [{"loai": "hong", "trang_thai": KHONG_DO_DUOC}], 40, M[:3])
        bang(mat["do_day_du"]["so_du_ba_thanh_phan"] == 1 and mat["do_day_du"]["ten_thieu"] == ["db_a", "db_thieu"] and mat["so_dong_hong"] == 1,
             f"dong mat / dong hong: van 3 mong doi, 2 thieu co ten: {mat}")
        for ten, them in (("giong het", [dict(db[1])] * 3), ("mau thuan", [{**db[1], "ca_dich_s": 9.0}])):
            trung = tong_hop_g5(bg + them, 40, M)["do_day_du"]
            bang([trung["so_du_ba_thanh_phan"], trung["so_thieu"], trung["ten_trung"]] == [1, 3, ["db_b"]] and "db_b" in trung["ten_thieu"],
                 f"dinh danh co hon MOT dong ({ten}) khong phai bang chung day du: la thieu, co neu ten (khong phai 2/4, 5/4): {trung}")
        la = tong_hop_g5(bg + [{**db[0], "ten": "db_la"}], 40, M[:3])["do_day_du"]
        bang(la["ten_la"] == ["db_la"] and la["so_du_ba_thanh_phan"] == 2, f"dinh danh ngoai mong doi dem rieng, khong vao tu so: {la}")
        kk = tong_hop_g5(bg, 40)
        bang(kk["do_day_du"]["trang_thai"] == KHONG_DO_DUOC and "so_thieu" not in kk["do_day_du"] and kk["doi_chieu"]["trang_thai"] == KHONG_DO_DUOC
             and kk["so_dong_dot_bien"] == 3, f"khong co kiem ke => khong_do_duoc, khong bao gio 'thieu 0': {kk}")
        bang(tong_hop_g5(trich_g5("khong co dong nao\n"), 40, M[:3])["do_day_du"]["so_thieu"] == 3, "log khong con dong nao: ca manh la thieu")
        # tap con: (i) mat mot ban ghi con ma cha van khai 3 (cac con con lai van khai du 3 dot bien); (ii) cha va con khop nhau nhung
        # tong dot bien cac con khai it hon mong doi (mot con chet truoc khi cha thu duoc dong cua no)
        mat_con = db + [{**con[0], "so_dot_bien": 2}, con[1]] + cha
        bang(tong_hop_g5(mat_con, 40, M[:3])["doi_chieu"]["trang_thai"] == KHONG_DO_DUOC, "mat mot ban ghi con => khong doi chieu duoc")
        con_chet = db + con[:2] + [{**cha[0], "so_con": 2}]
        bang(tong_hop_g5(con_chet, 40, M[:3])["doi_chieu"]["trang_thai"] == KHONG_DO_DUOC, "con khai thieu dot bien => khong doi chieu duoc")
        bang(tong_hop_g5(db + con + [{k: v for k, v in cha[0].items() if k != "so_con"}], 40, M[:3])["doi_chieu"]["trang_thai"] == KHONG_DO_DUOC,
             "cha khong khai so con => khong doi chieu duoc")
        # ca luot: du 8 manh do duoc moi co ti le; mat mot manh, trung manh hay mot manh khong do duoc => khong_do_duoc
        manh = lambda k, mong=M[:3]: {"manh": k, **tong_hop_g5(bg, 40, mong)}
        du8 = tong_hop_g5_luot([manh(k) for k in range(8)])
        bang([du8["trang_thai"], du8["so_mong"], du8["so_du_ba_thanh_phan"], du8["ti_le_du"], du8["dat_95_phan_tram"]] == [DO_DUOC, 24, 16, 0.6667, False]
             and du8["ten_thieu"] == ["db_thieu"] * 8, f"doi chung ca luot: 16/24 dinh danh mong doi: {du8}")
        for ten, ds in (("mat mot manh", [manh(k) for k in range(7)]), ("trung manh", [manh(k) for k in (0, 1, 2, 3, 3, 5, 6, 7)]),
                        ("mot manh khong co kiem ke", [manh(k) for k in range(7)] + [manh(7, None)])):
            bang(tong_hop_g5_luot(ds)["trang_thai"] == KHONG_DO_DUOC, f"{ten}: ca luot phai khong_do_duoc: {tong_hop_g5_luot(ds)}")
        b = {}
        for t in ({"trang_thai": DO_DUOC, "gia_tri": 7}, kdd("thieu moc"), {"trang_thai": KHONG_AP_DUNG}):
            them_do(b, "x", t)
        bang(b == {"x": {"v": [7], "loai": 1, "kad": 1}}, f"phep do khong do duoc van duoc DEM (so_loai), khong bien mat: {b}")

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
    def bien_nhan_ba_tang_moi_tep_mot_minh():
        """review 3 F1 (lop g4-receipt-authority, lan 4): TUNG tep duoc kiem MOT MINH qua ba tang. Hong cau truc la hong DA BIET bat ke bo co
        du hay kiem ke co san; thu chua kiem duoc la khong_do_duoc; chi `hop_le` la bang chung. Tren bo DU co kiem ke, ket luan duoc doi
        chieu voi `_gom_manh` goi TRUC TIEP: bo thu khong de hon, khong khat khe hon."""
        H, P, R = "c" * 40, "d" * 40, "1" * 40
        mod, cay = nap_cong_cu()
        tot = tao_bien_nhan(H)
        job = {k: {"ket_luan": "success", "head_sha": R} for k in range(SO_MANH_G5)}
        co = {k: "co" for k in range(SO_MANH_G5)}
        art7 = {**co, 7: "het_han"}
        la = lambda bn, tu=1: {k: sua_dau(nd, sha256_test="0" * 64) if k >= tu else nd for k, nd in bn.items()}   # van tay KHONG kiem ke nao mang
        kq = bien_nhan_luot(job, co, tot, R, cmt={H: [P, R]})
        bang(kq["trang_thai"] == [BN_HOP_LE] * 8 and kq["du_noi_dung"] is True and kq["che_do"] == "du" and kq["thieu"] is False
             and kq["kiem_ke"] == cay["sha256_test"], f"doi chung: 8 bien nhan do phia ghi THAT dung, head doi chieu qua commit => du: {kq}")
        dong = [tot[k].decode().split("\n") for k in range(SO_MANH_G5)]
        bg = json.loads(dong[0][1][6:])
        dich = bg[2]
        khac = next(c for c in bg[3] if c != dich)

        def m0(*ban_ghi, them=()):                       # manh 0 voi dong BKCON dau thay bang `ban_ghi` (chuoi = dong NGUYEN VAN) + dong `them`
            return {**tot, 0: "\n".join([dong[0][0]] + [b if isinstance(b, str) else "BKCON " + json.dumps(b) for b in ban_ghi] + dong[0][2:-1]
                                        + list(them) + [""]).encode()}

        def that(bn):                                    # `_gom_manh` goi TRUC TIEP tren cung cac byte: dat = ("GOM MẢNH 8/8", 0)
            with tempfile.TemporaryDirectory(prefix="wp1448_dc_") as d:
                for k, nd in bn.items():
                    (pathlib.Path(d) / f"manh-{k}.txt").write_bytes(nd)
                dg, loi = mod["_gom_manh"](d, {"sha256_test": cay["sha256_test"], "head": H})
            return (dg[0], loi) == ("GOM MẢNH 8/8", 0)
        bang(that(tot), "doi chung: chinh `_gom_manh` nhan bo dung")
        # TANG 1 — tep 0 hong CAU TRUC: `kiem_cau_truc` khong nhan kiem ke hay tep khac, va ket luan khong doi theo ba dieu kien cua bo
        cau_truc = (
            ("dong BKCON khong phai JSON", m0("BKCON [")),
            ("loai/do dai ban ghi", m0(["loi", bg[1]])),
            ("ban ghi loi", m0(["loi", bg[1], "x"])),
            ("trang thai ca la", m0([*bg[:3], {**bg[3], khac: ["chet", None]}])),
            ("ly do khong phai chuoi", m0([*bg[:3], {**bg[3], khac: ["qua", 7]}])),
            ("tap ca lech nhau giua cac ban ghi", m0([*bg[:3], {c: v for c, v in bg[3].items() if c != khac}])),
            ("ca dich khong phai chuoi", m0([bg[0], bg[1], [dich], bg[3]])),
            ("ten trung", m0(bg, bg)),
            ("dot bien khong bi giet", m0([*bg[:3], {**bg[3], dich: ["qua", None]}])),
            ("dong ngoai hop dong", m0(bg, them=['G5_THOI_GIAN {"loai": "con"}'])),
            ("dau cat cut", {**tot, 0: b'MANH {"head": '}),
            ("khong phai UTF-8", {**tot, 0: b"\xff\xfe\n"}),
            ("dau mang khoa che_do", {**tot, 0: sua_dau(tot[0], che_do="dich")}),
            ("phien ban la", {**tot, 0: sua_dau(tot[0], phien_ban=2)}),
            ("so manh lech", {**tot, 0: sua_dau(tot[0], so_manh=7)}),
            ("manh khac vi tri", {**tot, 0: tot[1]}),
            ("van tay sai dang", {**tot, 0: sua_dau(tot[0], sha256_test="zz")}),
        )
        for ten, bn in cau_truc:
            bang(kiem_cau_truc(bn[0], 0)[0] is None and not that(bn), f"{ten}: tep 0 phai hong cau truc (va `_gom_manh` cung tu choi bo)")
            for dk, kq, duoi in (("bo du, co kiem ke", bien_nhan_luot(job, co, bn, R, hop=H), [BN_HOP_LE] * 7),
                                 ("bo thieu manh 7 (het han)", bien_nhan_luot(job, art7, {k: v for k, v in bn.items() if k != 7}, R, hop=H),
                                  [BN_HOP_LE] * 6 + [KHONG_DO_DUOC]),
                                 ("khong kiem ke nao mang van tay", bien_nhan_luot(job, co, la(bn), R, hop=H), [KHONG_DO_DUOC] * 7)):
                bang(kq["trang_thai"] == [BN_HONG] + duoi and kq["ly_do"][0].startswith("cau_truc: ") and kq["thieu"] is True
                     and kq["du_noi_dung"] is False and kq["kiem_ke"] is None,
                     f"{ten} / {dk}: tep 0 hong DA BIET o moi dieu kien, cac tep khac giu trang thai RIENG: {kq['trang_thai']} {kq['ly_do'][0]}")
        # TANG 2 — dat cau truc, sai HOP DONG: co kiem ke => hong (chi tep ay); khong kiem ke => khong_do_duoc (khong hong, khong hop_le)
        doi = [bg[0], bg[1], khac, {**bg[3], dich: ["qua", None], khac: ["giet_that", "x"]}]
        for ten, bn in (("ca dich khac bang (ban ghi tu nhat quan)", m0(doi)),
                        ("ten ngoai bang", m0([bg[0], "khong_co_trong_bang", *bg[2:]])),
                        ("cat con mot dong", {**tot, 0: "\n".join(dong[0][:2] + [""]).encode()}),
                        ("mat mot dong", {**tot, 0: "\n".join([dong[0][0]] + dong[0][2:]).encode()})):
            a, b = bien_nhan_luot(job, co, bn, R, hop=H), bien_nhan_luot(job, co, la(bn, 0), R, hop=H)
            bang(kiem_cau_truc(bn[0], 0)[0] is not None and a["trang_thai"] == [BN_HONG] + [BN_HOP_LE] * 7 and a["ly_do"][0].startswith("hop_dong: ")
                 and a["du_noi_dung"] is False and not that(bn), f"{ten}: dat cau truc, co kiem ke => hong hop dong (nhu `_gom_manh`), chi tep 0: {a}")
            bang(b["trang_thai"] == [KHONG_DO_DUOC] * 8 and b["thieu"] is False and b["du_noi_dung"] is False and b["kiem_ke"] is None
                 and b["ly_do"] == ["khong_co_kiem_ke_cua_van_tay_bien_nhan:" + "0" * 12] * 8, f"{ten}: khong kiem ke => khong_do_duoc, khong bao gio du: {b}")
        # TANG 3 — head, theo su kien (push / workflow_dispatch checkout chinh head cua luot: khong ep luat cha-merge cua PR)
        ko = "head_bien_nhan_khong_khop_luot"
        for ten, kq, mong in (
            ("merge ref cua dong bong", bien_nhan_luot(job, co, tot, R, hop=H), [BN_HOP_LE, "-"]),
            ("head khac merge ref", bien_nhan_luot(job, co, tot, R, hop=P), [BN_HONG, ko]),
            ("cha hai khac head luot", bien_nhan_luot(job, co, tot, R, cmt={H: [R, P]}), [BN_HONG, ko]),
            ("pull_request chua co commit de doi chieu", bien_nhan_luot(job, co, tot, R), [KHONG_DO_DUOC, "head_bien_nhan_chua_doi_chieu_duoc"]),
            ("push: head khai = head luot", bien_nhan_luot({}, co, tot, H, su_kien="push"), [BN_HOP_LE, "-"]),
            ("workflow_dispatch: head khai = head luot", bien_nhan_luot({}, co, tot, H, su_kien="workflow_dispatch"), [BN_HOP_LE, "-"]),
            ("push: head khai khac head luot du cha hai khop", bien_nhan_luot({}, co, tot, R, cmt={H: [P, R]}, su_kien="push"), [BN_HONG, ko]),
            ("push: commit thuong MOT cha, khong ep luat cha-merge", bien_nhan_luot({}, co, tot, H, cmt={H: [P]}, su_kien="push"), [BN_HOP_LE, "-"]),
            ("su kien la", bien_nhan_luot({}, co, tot, H, su_kien="issue_comment"), [KHONG_DO_DUOC, "head_bien_nhan_chua_doi_chieu_duoc"]),
        ):
            bang(kq["trang_thai"] == [mong[0]] * 8 and kq["ly_do"] == [mong[1]] * 8 and kq["du_noi_dung"] is (mong[0] == BN_HOP_LE), f"{ten}: mong {mong}: {kq}")
        mot = bien_nhan_luot({**job, 2: {"ket_luan": "success", "head_sha": P}}, co, tot, R, hop=H)
        bang(mot["trang_thai"] == [BN_HOP_LE] * 2 + [BN_HONG] + [BN_HOP_LE] * 5 and mot["ly_do"][2] == "job_mang_head_khac_luot" and mot["du_noi_dung"] is False,
             f"job mang head khac luot: chi vi tri ay hong: {mot}")
        lan = {**tot, 3: sua_dau(tot[3], sha256_test="0" * 64)}
        kq = bien_nhan_luot(job, co, lan, R, hop=H)
        bang(kq["trang_thai"] == [BN_HONG] * 8 and kq["ly_do"] == ["bo_khai_van_tay_hoac_head_khac_nhau"] * 8 and not that(lan),
             f"buoc TAP chi HA: cac tep khai van tay khac nhau => ca nhom hong (nhu `[G-van-tay]`): {kq}")
        # VI TRI khong co tep: thieu (vang DA BIET) khac khong_do_duoc (chua lay / het han); job `success` khong bao gio la bang chung co
        for ten, kq, tt_, ly_ in (
            ("chua lay noi dung", bien_nhan_luot(job, co, {}, R, hop=H), KHONG_DO_DUOC, "noi_dung_chua_lay"),
            ("khong danh sach artifact", bien_nhan_luot(job, None, {}, R, hop=H), KHONG_DO_DUOC, "noi_dung_chua_lay"),
            ("artifact het han", bien_nhan_luot(job, {k: "het_han" for k in range(8)}, {}, R), KHONG_DO_DUOC, "artifact_het_han"),
            ("artifact vang", bien_nhan_luot(job, {}, {}, R), BN_THIEU, "artifact_vang"),
            ("job khong success, khong danh sach", bien_nhan_luot({k: {"ket_luan": "cancelled", "head_sha": R} for k in range(8)}, None, {}, R),
             BN_THIEU, "job_khong_success"),
        ):
            bang(kq["trang_thai"] == [tt_] * 8 and kq["ly_do"] == [ly_] * 8 and kq["du_noi_dung"] is False and kq["thieu"] is (tt_ == BN_THIEU),
                 f"{ten}: mong {tt_} / {ly_}, khong du: {kq}")
        dang_do = bien_nhan_luot(job, art7, {k: tot[k] for k in range(7)}, R, hop=H)
        bang(dang_do["trang_thai"] == [BN_HOP_LE] * 7 + [KHONG_DO_DUOC] and dang_do["ly_do"][7] == "artifact_het_han" and dang_do["thieu"] is False
             and dang_do["du_noi_dung"] is False and dang_do["kiem_ke"] is None, f"bay tep dung van duoc kiem mot minh; bo thieu mot vi tri KHONG du: {dang_do}")
        # kiem ke cua phien ban nguon KHAC (`--kiem-ke`): bang cua kiem ke ay, khong phai bang cua cay nay
        kk2 = {"sha256_test": "ab" * 32, "ca": ["ca_a", "ca_b", "ca_c"], "dot_bien": [[f"db{i}", "ca_" + "abc"[i % 3]] for i in range(20)]}
        bn2 = tao_bien_nhan(H, kk2)
        kq = bien_nhan_luot(job, co, bn2, R, hop=H)
        bang(kq["trang_thai"] == [KHONG_DO_DUOC] * 8 and kq["ly_do"] == ["khong_co_kiem_ke_cua_van_tay_bien_nhan:" + "ab" * 6] * 8,
             f"kiem ke khac chua duoc cap => khong_do_duoc, ly do neu van tay can cap: {kq}")
        kq = bien_nhan_luot(job, co, bn2, R, hop=H, cac_kiem_ke=[kk2])
        bang(kq["du_noi_dung"] is True and kq["kiem_ke"] == kk2["sha256_test"], f"doi chung: bien nhan cua van tay khac + dung kiem ke => du: {kq}")
        lech = bien_nhan_luot(job, co, bn2, R, hop=H, cac_kiem_ke=[{**kk2, "dot_bien": kk2["dot_bien"][:-1]}])
        bang(lech["trang_thai"] == [BN_HOP_LE] * 3 + [BN_HONG] + [BN_HOP_LE] * 4 and lech["ly_do"][3].startswith("hop_dong: "),
             f"kiem ke thieu mot dinh danh so voi bien nhan => tep mang dinh danh ay hong: {lech}")
        bang(ten_mong(kk2["sha256_test"], 3, [kk2]) == ["db3", "db11", "db19"] and ten_mong(kk2["sha256_test"], 3) is None and ten_mong(None, 3) is None
             and ten_mong(cay["sha256_test"], 5) == mod["_phan_manh"](5, SO_MANH_G5), "dinh danh mong doi = `_phan_manh` tren bang cua DUNG kiem ke")
        with tempfile.TemporaryDirectory(prefix="wp1448_kk_") as d:
            (pathlib.Path(d) / "a.json").write_bytes(xuat_json(kk2))
            bang(doc_kiem_ke(d) == [kk2] and doc_kiem_ke(None) == [], "doi chung: thu muc --kiem-ke doc duoc")
            for ten, xau, b in (("hai tep cung mot van tay", d, xuat_json({**kk2, "ca": ["ca_a", "ca_b", "ca_c", "ca_d"]})),
                                ("ten dot bien trung", d, xuat_json({**kk2, "sha256_test": "cd" * 32, "dot_bien": kk2["dot_bien"] + [["db0", "ca_a"]]})),
                                ("thu muc vang", str(pathlib.Path(d) / "khong_co"), b"")):
                (pathlib.Path(d) / "b.json").write_bytes(b)
                try:
                    doc_kiem_ke(xau)
                except AnhChupHong:
                    continue
                raise TuKiemDo(f"{ten}: kiem ke hong ma van doc duoc")

    @kiem
    def head_moi_bang_chung_co_san_phai_khop():
        """review 4 F1 (g4-receipt-authority): `hop` KHONG con la tham quyen som; mau thuan DA BIET o bat ky dau phu quyet; vang KHAC sai."""
        H, R, P, X = "c" * 40, "1" * 40, "d" * 40, "e" * 40
        for sk, head, hop, cmt, mong in (
                *(("pull_request", r, hop, c, m) for r, hop, c, m in ((R, H, {H: [P, R]}, True), (R, H, None, True), (R, None, {H: [P, R]}, True),
                  (R, H, {H: [P, X]}, False), (R, H, {H: [R]}, False), (R, X, {H: [P, R]}, False), (R, False, {H: [P, R]}, False),
                  (R, None, None, None), (None, H, {H: [R]}, False), (None, None, {H: [P, R]}, None))), ("issue_comment", R, H, None, True),
                ("issue_comment", R, None, None, None), *((sk, r, hop, c, m) for sk in SU_KIEN_HEAD_LUOT for r, hop, c, m in ((H, H, None, True),
                  (H, None, {H: [P]}, True), (H, X, None, False), (H, False, None, False), (H, H, {H: [P, X]}, True), (R, H, {H: [P, R]}, False),
                  (None, H, None, True), (None, None, None, None)))):              # (R, H, ...): hop khop KHONG vuot qua head goc KHAC cua luot
            bang(doi_chieu_head(H, head, sk, hop, cmt) is mong, f"{sk} head={head} hop={hop} cmt={cmt}: mong {mong}")
        kq = bien_nhan_luot({k: {"ket_luan": "success", "head_sha": R} for k in range(8)}, {k: "co" for k in range(8)}, tao_bien_nhan(H), None, hop=H, su_kien="push")
        bang(kq["trang_thai"] == [BN_HOP_LE] * 8, f"head luot VANG: head cua job khong phai mau thuan, `hop` van la bang chung duong: {kq['ly_do']}")
        fx, bong = J("g4b/b05_du_hoan_tat.json"), "BONG_PHAN_LOAI: cu=day_du moi=day_du goc_su_kien={0} goc_so={0} dau={1} hop={2} ly_do=- cu_do=do_duoc kiem_moi=- run=9005/1\n"
        for dau, cmt, mong in ((R, {H: [P, R]}, 5), (R, None, 5), (R, {H: [P, X]}, 9), (R, {H: [R]}, 9), (X, {H: [P, R]}, 9), (X, None, 9)):
            l = luot_fixture({**fx, "log": {**fx["log"], "chuan_bi": fx["log"]["chuan_bi"] + bong.format(P, dau, H)}, "cmt": cmt})
            bang(quy_g4b(l)[1] == mong and (l["manh"]["bien_nhan"] == [BN_HOP_LE] * 8) is (mong == 5), f"dau={dau[:1]} cmt={cmt}: mong buoc {mong}: {l['manh']}")

    @kiem
    def kiem_ke_cua_run_that_khop_bien_nhan_that():
        """Kiem ke cua van tay 2d798df0… (ma tai 64fa515, do `--xuat-kiem-ke` xuat) doi chieu voi 8 bien nhan THAT cua run 44443875641: phia ghi
        that dung lai dong dau trung NGUYEN VAN dong dau that; moi manh dung so dong va dung DAY TEN (bam) cua tep that."""
        that = J("bien_nhan_44443875641.json")
        kk = that["kiem_ke"]
        bn = tao_bien_nhan(dau_khai(that["manh"]["0"]["dau_nguyen_van"].encode())["head"], kk)
        for k in range(SO_MANH_G5):
            m, dong = that["manh"][str(k)], bn[k].decode().split("\n")
            ten = [json.loads(d[6:])[1] for d in dong[1:] if d]
            bang(dong[0] == m["dau_nguyen_van"] and len(ten) == m["so_dong_bkcon_goc"] and ten == ten_mong(kk["sha256_test"], k, [kk])
                 and hashlib.sha256("\n".join(ten).encode()).hexdigest() == m["sha256_ten_goc"], f"manh {k}: kiem ke khong khop bien nhan that")

    @kiem
    def g4b_hoan_tat_chi_tu_tam_bien_nhan_hop_le():
        """review 1-3 F1: buoc 5 can DU tam bien nhan `hop_le` va job gom `success`. Job `success`, ten artifact hay dau `GOM MẢNH 8/8` khong
        bao gio bu duoc mot bien nhan vang, het han, khong kiem duoc hay hong — ke ca moi to hop cua vong 3 (bo thieu / van tay la + than hong)."""
        fx = J("g4b/b05_du_hoan_tat.json")
        C, khong_gom = "c" * 40, {**fx["log"], "gom": None}
        hong0 = (tao_bien_nhan(C)[0].split(b"\n")[0] + b"\nBKCON [\n").decode()
        het7 = [{"name": TEN_ART_MANH + str(k), "expired": k == 7} for k in range(SO_MANH_G5)]
        la = {"tao": {"head": C, "sha256_test": "0" * 64}}
        thieu9 = ("thieu_bang_chung", 9)
        for ten, sua, mong in (
            ("doi chung: tam bien nhan hop le + gom in GOM MẢNH 8/8", {}, ("du_hoan_tat", 5)),
            ("doi chung: tam bien nhan hop le, khong log gom (job gom success)", {"artifact": None, "log": khong_gom}, ("du_hoan_tat", 5)),
            ("chi job success: khong noi dung, khong danh sach, khong log gom", {"bien_nhan": None, "artifact": None, "log": khong_gom}, thieu9),
            ("khong noi dung + GOM MẢNH 8/8: dau gom KHONG nang cap", {"bien_nhan": None}, thieu9),
            ("bo thieu manh 7 (het han), bay tep dung + GOM MẢNH 8/8", {"bien_nhan": {"tao": {"head": C}, "sua": {"7": None}}, "artifact": het7}, thieu9),
            ("vong 3: than manh 0 hong + manh 7 het han + GOM MẢNH 8/8", {"bien_nhan": {"tao": {"head": C}, "sua": {"7": None, "0": hong0}}, "artifact": het7}, thieu9),
            ("vong 3: ca tam van tay la + than manh 0 hong + GOM MẢNH 8/8", {"bien_nhan": {**la, "sua": {"0": sua_dau(hong0.encode(), sha256_test="0" * 64).decode()}}}, thieu9),
            ("van tay khong kiem ke nao mang (than dung) + GOM MẢNH 8/8", {"bien_nhan": la}, thieu9),
            ("than manh 0 hong, bo du, co kiem ke + GOM MẢNH 8/8", {"bien_nhan": {"tao": {"head": C}, "sua": {"0": hong0}}}, thieu9),
            ("dau KHONG DO duong nhanh khi chon du", {"log": {**fx["log"], "gom": "GOM: KHÔNG ĐO — x (CONG_CU_TEST_GOP_CHE_DO=duong_nhanh, 0 mảnh)\n"}}, thieu9),
            ("gom in so manh khac 8", {"log": {**fx["log"], "gom": "GOM MẢNH 3/3\n"}}, thieu9),
            ("bien nhan mang khoa che_do (hong cau truc) + GOM MẢNH 8/8", {"bien_nhan": {"tao": {"head": C, "che_do": "dich"}}}, thieu9),
            ("MO PHONG: bo da kiem mang che do dich, luot chon du", {"ghi_de": {"manh": {"che_do_bien_nhan": "dich"}}}, thieu9),
        ):
            l = luot_fixture({**fx, **sua}, F)
            bang(quy_g4b(l) == mong, f"{ten}: mong {mong}, duoc {quy_g4b(l)} {l['manh']['bien_nhan']} {l['manh']['ly_do'][0]}")

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
            rc = lenh_tinh(argparse.Namespace(anh_chup=str(goc / "khong_co_anh_chup_1434"), ra=str(ra), anh_chup_v2=str(ac), cohort_goc=None, kiem_ke=None))
            bang(rc == 3 and not ra.exists(), f"--tinh voi anh chup v2 lech MANIFEST phai tu choi rc 3 TRUOC moi tinh toan, duoc rc={rc}")

    @kiem
    def g5_tap_con_duy_nhat_va_so_do_huu_han():
        """review 3 F6: bang chung thoi gian chi "day du" khi tap con co PID hop le va DUY NHAT, khoang huu han co thu tu, DUNG MOT ban ghi cha;
        thanh phan am / NaN / vo cung / khong phai so khong vao tu so."""
        bg = trich_g5((F / "log_manh_g5.log").read_text(encoding="utf-8"))
        db, con, cha = ([b for b in bg if b.get("loai") == x] for x in ("dot_bien", "con", "cha"))
        M = ["db_a", "db_b", "db_thieu"]
        dc = lambda ds, giay=40: tong_hop_g5(ds, giay, M)["doi_chieu"]
        thay_con = lambda **sua: db + [{**con[0], **sua}] + con[1:] + cha
        bang(dc(bg)["trang_thai"] == DO_DUOC and dc(db + con[::-1] + cha)["trang_thai"] == DO_DUOC, "doi chung: ba con, ba PID khac nhau => doi chieu duoc")
        for ten, ds in (
            ("con mat duoc thay bang BAN SAO cua con khac (cung so_dot_bien)", db + [con[0], dict(con[0]), con[2]] + cha),
            ("pid la bool", thay_con(pid=True)),
            ("pid khong duong", thay_con(pid=0)),
            ("pid vang", db + [{k: v for k, v in con[0].items() if k != "pid"}] + con[1:] + cha),
            ("khoang con dao nguoc", thay_con(bat_dau=con[0]["ket_thuc"] + 1)),
            ("khoang con NaN", thay_con(ket_thuc=float("nan"))),
            ("khoang con vo cung", thay_con(ket_thuc=float("inf"))),
            ("khoang con la so nguyen qua lon de doi ra float (review 4 F6)", thay_con(ket_thuc=10 ** 400)),
            ("so_dot_bien cua con la bool", thay_con(so_dot_bien=True)),
            ("tong dung nhung phan chia sai (mot con khai 0, con khac khai 2)", db + [{**con[0], "so_dot_bien": 0}, {**con[1], "so_dot_bien": 2}, con[2]] + cha),
            ("hai ban ghi cha", db + con + cha * 2),
        ):
            bang(khong_nem(lambda: dc(ds))["trang_thai"] == KHONG_DO_DUOC, f"{ten}: tap con khong phai bang chung day du => khong_do_duoc, duoc {dc(ds)}")
        tuong_xau = db + con + [{**cha[0], "tuong_s": float("nan")}]
        bang(dc(tuong_xau, None)["trang_thai"] == KHONG_DO_DUOC and dc(tuong_xau)["trang_thai"] == DO_DUOC and dc(bg, float("inf"))["trang_thai"] == DO_DUOC,
             "thoi gian tuong: so do cua API truoc, khong co thi `tuong_s` cua cha; ca hai khong huu han => khong_do_duoc")
        bang([so_lan(x) for x in (None, 1, 50, 0, 51, 10 ** 400, True, 1.0, "2", float("nan"))] == [1, 1, 50] + [None] * 7, "so lan attempt: 1..50, khac => None")
        for khoa in ("dung_cay_s", "ca_dich_s", "ca_khac_s", "bat_dau", "ket_thuc"):
            for xau in (-1, float("nan"), float("inf"), True, "1.0", 10 ** 400):
                dd = khong_nem(lambda: tong_hop_g5([{**b, khoa: xau} if b.get("ten") == "db_a" else b for b in bg], 40, M)["do_day_du"])
                bang(dd["so_du_ba_thanh_phan"] == 1 and dd["ten_thieu"] == ["db_a", "db_thieu"], f"{khoa}={xau!r} khong phai so do: dinh danh ay la thieu: {dd}")
        dao = tong_hop_g5([{**b, "ket_thuc": b["bat_dau"] - 1} if b.get("ten") == "db_a" else b for b in bg], 40, M)["do_day_du"]
        bang(dao["so_du_ba_thanh_phan"] == 1 and "db_a" in dao["ten_thieu"], f"khoang cua dot bien dao nguoc: thieu: {dao}")
        nan = trich_g5('G5_THOI_GIAN {"loai": "dot_bien", "ten": "db_a", "trang_thai": "do_duoc", "bat_dau": 1, "ket_thuc": 2, "dung_cay_s": NaN, "ca_dich_s": 1, "ca_khac_s": 1}\n')
        bang(tong_hop_g5(nan, 40, ["db_a"])["do_day_du"]["so_du_ba_thanh_phan"] == 0, "NaN di qua dong log that (JSON cua Python doc duoc NaN) van bi loai")

    @kiem
    def thu_roi_tinh_moi_luot_duoc_chon_va_khong_goi_git():
        """review 3 F6 + F7, DAU-CUOI tren ma that: `lenh_thu` (lop `Thu` cua #1434, van chuyen GIA — khong mang) -> anh chup v2 -> `lenh_tinh`
        (gom ca `--tinh` cua #1434) cho cac luot DUOC CHON: pull_request, push (trong cohort), workflow_dispatch (ngoai cohort) va mot luot
        khong thu duoc. Cung log va bien nhan dung => cung mau so mong doi o ca ba su kien; `--tinh` khong phong `git` lan nao."""
        import io
        import zipfile
        mod, cay = nap_cong_cu()
        T, popen = "2026-11-01T00:%02d:00Z", subprocess.Popen
        luot = {101: ("pull_request", "a" * 40, "c" * 40, 1), 102: ("push", "b" * 40, "b" * 40, 1), 103: ("workflow_dispatch", "e" * 40, "e" * 40, 1),
                104: ("workflow_dispatch", "e" * 40, "e" * 40, 2), 105: ("workflow_dispatch", "e" * 40, "e" * 40, 2)}   # review 4 F6: attempt 2
        kh = lambda sk, chon: ke_hoach_thu(sk, {JOB_MANH + " (ubuntu-latest, 0)": {"id": 5, "conclusion": "success"}}, chon)
        bang([kh("push", True), kh("push", False), kh("pull_request", False)] == [{"log": [5], "bien_nhan": True, "oracle": None},
             {"log": [], "bien_nhan": False, "oracle": None}, {"log": [], "bien_nhan": True, "oracle": None}],
             "ke hoach thu: luot DUOC CHON thu bien nhan o moi su kien; push khong duoc chon thi khong; pull_request luon thu (G4)")

        def log_manh(k, lon=False):                       # `lon`: dong dau mang so nguyen JSON 401 chu so (review 4 F6)
            ten = mod["_phan_manh"](k, SO_MANH_G5)
            bg = [{"loai": "dot_bien", "ten": t_, "trang_thai": DO_DUOC, "bat_dau": 1.0, "ket_thuc": 2.0, "dung_cay_s": 10 ** 400 if lon and t_ == ten[0] else 0.1, "ca_dich_s": 0.2, "ca_khac_s": 0.3} for t_ in ten]
            bg += [{"loai": "con", "pid": 7, "bat_dau": 0.0, "ket_thuc": 9.0, "so_dot_bien": len(ten)}, {"loai": "cha", "so_con": 1, "tuong_s": 9.5}]
            return "".join("G5_THOI_GIAN " + json.dumps(b) + "\n" for b in bg).encode()

        def zip_manh(nd, k):
            b = io.BytesIO()
            with zipfile.ZipFile(b, "w") as z:
                z.writestr(f"manh-{k}.txt", nd)
            return b.getvalue()
        api, tep1 = {"commits/" + "c" * 40: json.dumps({"parents": [{"sha": "d" * 40}, {"sha": "a" * 40}]}).encode(),
                     f"actions/workflows/{WF_PL}/runs": b'{"total_count": 0, "workflow_runs": []}'}, {}
        for rid, (sk, head, checkout, n) in luot.items():
            run = {"id": rid, "run_attempt": n, "event": sk, "head_sha": head, "head_branch": "master", "status": "completed", "conclusion": "success", "created_at": T % 1}
            ten = [JOB_CHUAN_BI] + [f"{JOB_MANH} (ubuntu-latest, {k})" for k in range(SO_MANH_G5)] + [JOB_GOM + " (ubuntu-latest)"]
            jobs = [(rid * 100 + i, t_, 1, 2, 9) for i, t_ in enumerate(ten)] + [    # attempt 2: manh 0-3 + gom CHAY LAI; con lai la MANG SANG
                (rid * 100 + 20 + i, t_, 2, *((21, 29) if 1 <= i <= 4 or i == 9 else (2, 9))) for i, t_ in enumerate(ten) if n == 2]
            trang = json.dumps({"total_count": len(jobs), "jobs": [{"id": j, "name": t_, "conclusion": "success", "run_attempt": a, "head_sha": head,
                                "created_at": T % 1, "started_at": T % s, "completed_at": T % e, "steps": []} for j, t_, a, s, e in jobs]}).encode()
            if rid == 104:                               # 105: cung cac dong ay nhung API khong tra ban ghi attempt
                api.update({f"actions/runs/{rid}/attempts/{a}": json.dumps({"created_at": T % c}).encode() for a, c in ((1, 1), (2, 20))})
            if sk == "workflow_dispatch":                # ngoai cohort cua #1434: `--thu` phai tu lay luot + job cua no
                api[f"actions/runs/{rid}"], api[f"actions/runs/{rid}/jobs"] = json.dumps(run).encode(), trang
            else:
                tep1.update({f"list/ci/{sk}/x/p1": json.dumps({"total_count": 1, "workflow_runs": [run]}).encode(), f"jobs/{rid}/p1": trang,
                             f"log/{rid * 100}": (T % 3 + " che_do=day_du\n").encode()})
            api[f"actions/runs/{rid}/artifacts"] = json.dumps({"total_count": SO_MANH_G5, "artifacts": [
                {"id": rid * 10 + k, "name": TEN_ART_MANH + str(k), "expired": False} for k in range(SO_MANH_G5)]}).encode()
            for k, nd in tao_bien_nhan(checkout).items():
                api[f"actions/artifacts/{rid * 10 + k}/zip"] = zip_manh(nd, k)
                api.update({f"actions/jobs/{rid * 100 + d + k}/logs": log_manh(k, rid == 102 and k == 0) for d in (1, 21)})
            api.update({f"actions/jobs/{rid * 100 + j}/logs": "GOM MẢNH 8/8\n".encode() for j in (9, 29)})
        with cam_git() as goi:
            for lenh in (["git", "--version"], "git --version", ["/usr/bin/git", "status"]):
                try:
                    subprocess.run(lenh, capture_output=True, shell=isinstance(lenh, str))
                except GitBiCam:
                    continue
                raise TuKiemDo(f"cam_git khong chan {lenh!r}")
            khac = subprocess.run([sys.executable, "-c", "print(7)"], capture_output=True, text=True).stdout.strip()
        bang(len(goi) == 3 and khac == "7" and subprocess.Popen is popen, f"cam_git: chan va GHI moi lan goi git, de yen tien trinh khac, tra Popen nhu cu: {goi} {khac!r}")
        with tempfile.TemporaryDirectory(prefix="wp1448_dc_") as d:
            goc = pathlib.Path(d)
            meta = {"T0": T % 0, "T1": T % 59, "sha_master": "f" * 40, "spec_sha256": "0" * 64, "kho": "o/r",
                    "khoang_con": [{"su_kien": sk, "nhan": "x", "tu": T % 0, "den": T % 59} for sk in ("pull_request", "push")]}
            muc = []
            for khoa, b in {"META": json.dumps(meta).encode(), **tep1}.items():
                p = goc / "ac" / (khoa + ".json")
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(b)
                muc.append({"khoa": khoa, "loai": "x", "url": None, "http": 200, "duong_dan": khoa + ".json", "sha256": hashlib.sha256(b).hexdigest(), "kich_thuoc": len(b)})
            (goc / "ac" / "MANIFEST.json").write_text(json.dumps({"tep": muc}), encoding="utf-8")
            g = nap_goc()

            class ThuGia(g.Thu):
                def _goi(self, duong):
                    b = api.get(duong.split("?")[0])
                    return (200, b, None) if b is not None else (404, None, "HTTP 404")
            g.Thu = ThuGia
            bang(phan_loai_luot(g, {"id": 1, "run_attempt": 10 ** 400}, None, [])[0] is None and str(khong_nem(lambda: phan_loai_luot(g, {"id": 1, "run_attempt": 1}, None, [{"run_attempt": "x"}]))[1]).startswith("dong job"), "phan loai luot TOAN PHAN")
            tinh = lambda ra: lenh_tinh(argparse.Namespace(anh_chup=str(goc / "ac"), ra=str(goc / ra), anh_chup_v2=str(goc / "v2"), cohort_goc=None, kiem_ke=None))
            s6_dung = globals()["s6_khong_cay_song"]
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    rc_thu = lenh_thu(argparse.Namespace(anh_chup=str(goc / "ac"), ra=str(goc / "v2"), han_giay=60, so_luong=1, run_g5="101,102,103,104,105,999", kho=None), g)
                    rc = tinh("ra")
                    globals()["s6_khong_cay_song"] = g.phan_loai_s6     # ban GOC cua #1434 (cay song, goi git): `--tinh` phai TU CHOI
                    rc_git = tinh("ra2")
            finally:
                globals()["s6_khong_cay_song"] = s6_dung
            bang((rc_thu, rc) == (0, 0) and subprocess.Popen is popen, f"--thu roi --tinh phai chay tron (rc 0, 0), duoc {(rc_thu, rc)}")
            bang(rc_git == 5 and not (goc / "ra2" / "BASELINE_V2.json").exists(), f"--tinh ma muc §6 goi git thi phai TU CHOI rc 5, khong ghi ket qua v2: rc={rc_git}")
            v2 = json.loads((goc / "ra" / "BASELINE_V2.json").read_bytes())
            tl, n = v2["g5_thoi_gian"]["theo_luot"], len(cay["dot_bien"])
            bang(v2["meta"]["so_lan_thu_goi_git"] == 0 and "khong_do_duoc (--tinh v2" in (goc / "ra" / "nen" / "BAO_CAO.md").read_text(encoding="utf-8"),
                 "--tinh: 0 lan thu goi git; muc §6 cua bao cao nen ghi khong_do_duoc, khong phai du lieu cay song")
            dung = lambda r, du=n: tl[str(r)]["trang_thai"] == DO_DUOC and [tl[str(r)]["so_mong"], tl[str(r)]["so_du_ba_thanh_phan"]] == [n, du]
            bang(all(dung(r) for r in (101, 103, 104)) and dung(102, n - 1) and tl["102"]["ten_thieu"] == mod["_phan_manh"](0, SO_MANH_G5)[:1],
                 f"cung log + bien nhan dung: pull_request, push, dispatch attempt 1 VA 2 (co ban mang sang) {n}/{n}; so qua lon chi mat dinh danh ay: {tl}")
            bang(tl.get("105", {}).get("trang_thai") == KHONG_DO_DUOC and "thieu ban ghi attempt [1, 2]" in tl["105"]["ly_do"], f"vang ban ghi attempt => NEU TEN: {tl.get('105')}")
            bang(tl.get("999", {}).get("trang_thai") == KHONG_DO_DUOC and len(v2["g5_thoi_gian"]["manh"]) == 32
                 and all(m["doi_chieu"]["trang_thai"] == DO_DUOC and m["kiem_ke"] == cay["sha256_test"] for m in v2["g5_thoi_gian"]["manh"]),
                 f"luot duoc chon ma khong thu duoc phai hien dien la khong_do_duoc; 32 manh doi chieu duoc: {tl.get('999')}")
            bang([l["run_id"] for l in v2["luot"]] == [101, 102] and v2["G4"]["so_luot_pull_request"] == 1 and v2["G4"]["G4b"]["du_hoan_tat"] == 1,
                 f"luot ngoai cohort chi vao phan thoi gian G5; luot pull_request co du tam bien nhan that => du_hoan_tat: {v2['G4']}")

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
    ("g5_thieu_thanh_phan_van_du", 'for k in ("dung_cay_s", "ca_dich_s", "ca_khac_s"))]', 'for k in ("dung_cay_s", "ca_khac_s"))]', "g5_hop_khac_tong_va_ba_thanh_phan"),
    # review 2 (F6, lop g5-collector-expected-id-accounting): mau so la dinh danh MONG DOI, khong phai so dong con sot lai
    ("g5_mau_so_la_dong_con_sot", "    mau = None if mong is None else list(mong)\n", "    mau = None if mong is None else [t for t in mong if t in theo_ten]\n",
     "g5_mau_so_la_dinh_danh_mong_doi"),
    ("g5_khong_kiem_ke_lay_ten_tu_dong", "    mau = None if mong is None else list(mong)\n",
     "    mau = sorted(t for t in theo_ten if t) if mong is None else list(mong)\n", "g5_mau_so_la_dinh_danh_mong_doi"),
    ("g5_luot_manh_khong_do_van_tinh", "    if len(do) != SO_MANH_G5 or sorted(", "    if sorted(", "g5_mau_so_la_dinh_danh_mong_doi"),
    ("g5_luot_khong_kiem_tap_manh", " or sorted(m[\"manh\"] for m in cac_manh) != list(range(SO_MANH_G5)):\n", ":\n", "g5_mau_so_la_dinh_danh_mong_doi"),
    ("phep_do_khong_do_duoc_bien_mat", '        o["loai" if t["trang_thai"] == KHONG_DO_DUOC else "kad"] += 1\n', '        pass\n', "g5_mau_so_la_dinh_danh_mong_doi"),
    ("gom_dau_la_thanh_duong_nhanh", '            dau = "khong_do:" + (khop[0] if len(khop) == 1 else "la")\n', '            dau = "khong_do:duong_nhanh"\n', "gom_dau_hieu_duong_theo_ly_do"),
    # review F1: bien nhan la NOI DUNG da kiem (hoac dau duong cua job gom), khong bao gio la job `success`
    ("g4b_dau_khong_do_van_khop", '    dau_khop = dau in (None, f"gom_manh:{SO_MANH_G5}")', '    dau_khop = True', "g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc"),
    # review 2 (F1, lop g4-receipt-authority): bang dot bien la cua MA (kiem ke), khong suy tu bien nhan
    ("bn_bo_da_kiem_khong_mang_che_do", '"che_do": "du" if du else None,', '"che_do": None,', "bien_nhan_ba_tang_moi_tep_mot_minh"),
    ("bn_chon_kiem_ke_bat_ke_van_tay", ' if x["sha256_test"] in cac_van_tay), None)\n', '), None)\n', "bien_nhan_ba_tang_moi_tep_mot_minh"),
    ("bn_artifact_vang_khong_thieu", '        elif art == "vang":\n            tt[k], ly[k] = BN_THIEU, "artifact_vang"\n', '',
     "bien_nhan_ba_tang_moi_tep_mot_minh"),
    ("bn_job_do_khong_thieu", '        elif art is None and (d is None or d.get("ket_luan") != "success"):\n            tt[k], ly[k] = BN_THIEU, "job_khong_success"\n', '',
     "g4b_bon_fixture_bat_buoc_cua_dac_ta"),
    ("bn_job_success_la_bien_nhan", '            tt[k], ly[k] = KHONG_DO_DUOC, "artifact_het_han" if art == "het_han" else "noi_dung_chua_lay"\n',
     '            tt[k], ly[k] = BN_HOP_LE, "-"\n', "bien_nhan_ba_tang_moi_tep_mot_minh"),
    ("bn_job_sai_head_bo_qua", '        if d is not None and head_run is not None and d.get("head_sha") not in (None, head_run):\n            tt[k], ly[k] = BN_HONG, "job_mang_head_khac_luot"\n',
     '        if False:\n            pass\n', "bien_nhan_ba_tang_moi_tep_mot_minh"),
    ("kk_bang_cua_cay_cho_dinh_danh_mong_doi", '(k, SO_MANH_G5, [t for t, _ in kk["dot_bien"]])', '(k, SO_MANH_G5)', "kiem_ke_cua_run_that_khop_bien_nhan_that"),
    ("kk_nhan_kiem_ke_sai_hinh_dang", '                raise ValueError("sai hinh dang kiem ke")\n', '                pass\n', "bien_nhan_ba_tang_moi_tep_mot_minh"),
    ("kk_nhan_hai_kiem_ke_cung_van_tay", '                raise ValueError("hai kiem ke cung mot van tay")\n', '                pass\n',
     "bien_nhan_ba_tang_moi_tep_mot_minh"),
    ("kk_thu_muc_vang_im_lang", '        raise AnhChupHong(f"--kiem-ke {thu_muc}: khong phai thu muc")\n', '        return []\n', "bien_nhan_ba_tang_moi_tep_mot_minh"),
    # lan 4 (thiet ke lai theo review 3): moi luat mot dot bien rieng, bi bat boi `TuKiemDo` cua dung ca
    ('bn_dau_gom_nang_cap_bo_khong_du', '    return manh.get("bien_nhan") == [BN_HOP_LE] * SO_MANH_G5 and manh.get("che_do_bien_nhan") == che_do\n', '    return (manh.get("bien_nhan") == [BN_HOP_LE] * SO_MANH_G5 and manh.get("che_do_bien_nhan") == che_do) or (\n        che_do == "du" and (l.get("gom") or {}).get("dau") == f"gom_manh:{SO_MANH_G5}")\n', 'g4b_hoan_tat_chi_tu_tam_bien_nhan_hop_le'),
    ('bn_du_la_khong_con_hong_da_biet', '    du = tt == [BN_HOP_LE] * SO_MANH_G5\n', '    du = not any(x in (BN_HONG, BN_THIEU) for x in tt)\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_bo_than_co_mat_khi_bo_thieu', '        elif isinstance(nd, (bytes, bytearray)):\n', '        elif isinstance(nd, (bytes, bytearray)) and len(noi_dung) == SO_MANH_G5:\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_bo_tang_cau_truc_cua_ban_ghi', '    return (None, "ban ghi: " + loi) if loi else (dau, than)\n', '    return dau, than\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_bo_kiem_dong_ngoai_hop_dong', '    if any(d and not d.startswith("BKCON ") for d in than.split("\\n")):\n', '    if False:\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_bo_kiem_bo_khoa_dau', ' or set(dau) != mod["_KHOA_DAU_MANH"] or any(', ' or any(', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_bo_kiem_phien_ban', '    if dau["phien_ban"] != mod["_PHIEN_BAN_MANH"] or (dau["manh"]', '    if (dau["manh"]', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_bo_kiem_vi_tri_manh', ' or (dau["manh"], dau["so_manh"]) != (k, SO_MANH_G5):\n', ':\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_bo_kiem_dang_van_tay', '    if not all(isinstance(dau[x], str) and r.fullmatch(dau[x]) for x, r in (("sha256_test", RE_SHA256), ("head", RE_OID))):\n', '    if False:\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_bo_tang_hop_dong', '    loi = kiem_than(than, kk, ten_mong(khai[0], k, cac_kiem_ke)) if kk else None\n', '    loi = None\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_bo_loi_dot_bien_cua_hop_dong', '    return f"{loi} loi dot bien" if loi else None\n', '    return None\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_khong_kiem_ke_van_hop_le', '    if kk is None or khop is None:\n', '    if khop is None:\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_head_chua_doi_chieu_thanh_hop_le', '    if kk is None or khop is None:\n', '    if kk is None:\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_head_sai_khong_hong', '    if loi or khop is False:\n', '    if loi:\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_bo_doi_chieu_merge_ref', '[hop is not False and h == hop]', '[hop is not False]', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_bo_doi_chieu_cha_hai', 'phieu.append(len(cha) == 2 and cha[1] == head_run)', 'phieu.append(len(cha) == 2)', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_push_bi_ep_luat_cha_merge', ' if su_kien == "pull_request" else None\n', ' if True else None\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_su_kien_la_duoc_tin_head', '    if su_kien in SU_KIEN_HEAD_LUOT and co_run:\n', '    if co_run:\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_bo_buoc_tap', '    if len(set(khai.values())) > 1:\n', '    if False:\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('g5_nhan_dinh_danh_nhieu_dong', ' if len(theo_ten.get(t, ())) == 1 and theo_ten[t][0].get("trang_thai")', ' if theo_ten.get(t) and theo_ten[t][0].get("trang_thai")', 'g5_mau_so_la_dinh_danh_mong_doi'),
    ('g5_bo_doi_chieu_so_con', '    if type(cha[0].get("so_con")) is not int or cha[0]["so_con"] != len(con) or not con:\n', '    if False:\n', 'g5_mau_so_la_dinh_danh_mong_doi'),
    ('g5_bo_doi_chieu_dot_bien_cua_con', '    if khai != chia:\n', '    if False:\n', 'g5_mau_so_la_dinh_danh_mong_doi'),
    ('g5_doi_chieu_tong_thay_phan_chia', '    if khai != chia:\n', '    if sum(khai) != sum(chia):\n', 'g5_tap_con_duy_nhat_va_so_do_huu_han'),
    ('g5_bo_pid_duy_nhat', '    if len(set(pid)) != len(pid):\n', '    if False:\n', 'g5_tap_con_duy_nhat_va_so_do_huu_han'),
    ('g5_bo_kiem_pid_hop_le', 'if not (type(b.get("pid")) is int and b["pid"] > 0 and khoang_do(b)', 'if not (khoang_do(b)', 'g5_tap_con_duy_nhat_va_so_do_huu_han'),
    ('g5_bo_kiem_khoang_con', ' and b["pid"] > 0 and khoang_do(b) and type(', ' and b["pid"] > 0 and type(', 'g5_tap_con_duy_nhat_va_so_do_huu_han'),
    ('g5_bo_kiem_so_dot_bien_cua_con', ' and type(b.get("so_dot_bien")) is int)]\n', ')]\n', 'g5_tap_con_duy_nhat_va_so_do_huu_han'),
    ('g5_nhan_nhieu_ban_ghi_cha', '    if len(cha) != 1:\n        return f"can DUNG MOT ban ghi cha, co {len(cha)}"\n', '', 'g5_tap_con_duy_nhat_va_so_do_huu_han'),
    ('g5_so_do_khong_can_huu_han', ' and math.isfinite(float(x)) and x >= 0\n', ' and x >= 0\n', 'g5_tap_con_duy_nhat_va_so_do_huu_han'),
    ('g5_so_do_nhan_so_am', ' and math.isfinite(float(x)) and x >= 0\n', ' and math.isfinite(float(x))\n', 'g5_tap_con_duy_nhat_va_so_do_huu_han'),
    ('g5_so_do_nhan_bool', ' and not isinstance(x, bool) and math.isfinite(float(x))', ' and math.isfinite(float(x))', 'g5_tap_con_duy_nhat_va_so_do_huu_han'),
    ('g5_dot_bien_khong_can_khoang', ' == DO_DUOC and khoang_do(theo_ten[t][0])\n', ' == DO_DUOC\n', 'g5_tap_con_duy_nhat_va_so_do_huu_han'),
    ('g5_khoang_khong_can_thu_tu', ' and b["ket_thuc"] >= b["bat_dau"]\n', '\n', 'g5_tap_con_duy_nhat_va_so_do_huu_han'),
    ('g5_tuong_khong_can_so_do', '(None if so_do(tuong) and tuong > 0 else ', '(None if tuong else ', 'g5_tap_con_duy_nhat_va_so_do_huu_han'),
    ('thu_bien_nhan_chi_cho_pull_request', '"bien_nhan": su_kien == "pull_request" or duoc_chon,', '"bien_nhan": su_kien == "pull_request",', 'thu_roi_tinh_moi_luot_duoc_chon_va_khong_goi_git'),
    ('thu_bo_luot_duoc_chon_ngoai_cohort', '    ngoai = [x for x in run_g5 if x not in {r["id"] for r in co_ci}]', '    ngoai = []', 'thu_roi_tinh_moi_luot_duoc_chon_va_khong_goi_git'),
    ('tinh_luot_duoc_chon_vang_bien_mat', ' for rid in sorted({x[0] for x in g5} | set(chon))}}\n', ' for rid in sorted({x[0] for x in g5})}}\n', 'thu_roi_tinh_moi_luot_duoc_chon_va_khong_goi_git'),
    ('tinh_luot_ngoai_cohort_vao_g4', '        if nguon is not doc:\n            continue\n', '', 'thu_roi_tinh_moi_luot_duoc_chon_va_khong_goi_git'),
    ('tinh_head_luot_khong_theo_su_kien', 'bien_nhan_luot(manh, art, bien_nhan, head, hop, cmt, kiem_ke, run.get("event"))', 'bien_nhan_luot(manh, art, bien_nhan, head, hop, cmt, kiem_ke)', 'thu_roi_tinh_moi_luot_duoc_chon_va_khong_goi_git'),
    ('tinh_chay_s6_tren_cay_song', '    g.phan_loai_s6 = s6_khong_cay_song\n', '', 'thu_roi_tinh_moi_luot_duoc_chon_va_khong_goi_git'),
    ('tinh_khong_cam_git', '    with cam_git() as goi:\n        return _tinh(ns, goi)\n', '    return _tinh(ns, [])\n', 'thu_roi_tinh_moi_luot_duoc_chon_va_khong_goi_git'),
    ('tinh_bo_qua_danh_sach_goi_git', '    if goi:                                                 # ma duoc nap', '    if False:                                               # ma duoc nap', 'thu_roi_tinh_moi_luot_duoc_chon_va_khong_goi_git'),
    ('cam_git_ghi_ma_khong_chan', '                raise GitBiCam(f"--tinh khong duoc goi git: {goi[-1][:4]}")\n', '', 'thu_roi_tinh_moi_luot_duoc_chon_va_khong_goi_git'),
    ('cam_git_khong_tra_popen', '    finally:\n        subprocess.Popen = goc\n', '    finally:\n        pass\n', 'thu_roi_tinh_moi_luot_duoc_chon_va_khong_goi_git'),
    ('g5_luot_mau_so_la_so_da_du', '    mong, du = sum(d["so_mong"] for d in do), sum(d["so_du_ba_thanh_phan"] for d in do)\n', '    mong = du = sum(d["so_du_ba_thanh_phan"] for d in do)\n', 'g5_mau_so_la_dinh_danh_mong_doi'),
    ('kk_dinh_danh_mong_doi_cua_manh_ke', '["_phan_manh"](k, SO_MANH_G5, [t for t, _ in kk["dot_bien"]])', '["_phan_manh"]((k + 1) % SO_MANH_G5, SO_MANH_G5, [t for t, _ in kk["dot_bien"]])', 'kiem_ke_cua_run_that_khop_bien_nhan_that'),
    # review F5: anh chup v2 da chi dinh phai khop MANIFEST
    ("anh_chup_bo_kiem_bam", '    if hong:\n        raise AnhChupHong', '    if False:\n        raise AnhChupHong', "anh_chup_v2_kiem_manifest"),
    ("anh_chup_vang_manifest_im_lang", '        raise AnhChupHong(f"{ac}: khong co MANIFEST.json (anh chup chua dong)")\n', '        return None, {}\n',
     "anh_chup_v2_kiem_manifest"),
    ("anh_chup_duong_dan_thoat_ra_ngoai", '        if ac not in p.parents or not p.is_file()', '        if not p.is_file()', "anh_chup_v2_kiem_manifest"),
    # review F3: phan loai khong do duoc khong vao bo dem
    ("bong_dem_nhan_cu_fail_close", '    cu_do = pl.get("cu_do") == DO_DUOC\n', '    cu_do = True\n', "bong_hai_bo_dem_tach_rieng"),
    ("bong_dem_nhan_kiem_moi_khong_do_duoc", '    moi_do = pl.get("kiem_moi") != KHONG_DO_DUOC\n', '    moi_do = True\n', "bong_hai_bo_dem_tach_rieng"),
    ("bn_hop_som_la_tham_quyen", "    phieu = [] if hop is None else [", "    if hop:\n        return h == hop\n    phieu = [] if hop is None else [", "head_moi_bang_chung_co_san_phai_khop"),
    ("bn_phieu_dung_thang_phieu_sai", "    return False if False in phieu else (", "    return True if True in phieu else (False if False in phieu else None) or (", "head_moi_bang_chung_co_san_phai_khop"),
    ("bn_vang_head_luot_la_mau_thuan", " and RE_OID.fullmatch(head_run) is not None\n", " or True\n", "head_moi_bang_chung_co_san_phai_khop"),
    ("bn_job_vang_head_luot_la_mau_thuan", "d is not None and head_run is not None and d.get", "d is not None and d.get", "head_moi_bang_chung_co_san_phai_khop"),
    ("bn_so_cha_sai_bo_qua_khi_vang_head", " and (co_run or len(cha) != 2):", " and co_run:", "head_moi_bang_chung_co_san_phai_khop"),
    ("bn_dong_bong_khai_head_khac_bo_qua", "        hop = False      ", "        hop = hop        ", "head_moi_bang_chung_co_san_phai_khop"),
    ("so_do_doi_float_nem", "    except OverflowError:\n        return False\n", "    except ZeroDivisionError:\n        return False\n", "g5_tap_con_duy_nhat_va_so_do_huu_han"),
    ("so_lan_khong_tran", " and 1 <= x <= TRAN_ATTEMPT else None)", " and 1 <= x else None)", "g5_tap_con_duy_nhat_va_so_do_huu_han"),
    ("phan_loai_luot_nem_loi_dong_job", "    except (ValueError, TypeError, OverflowError, AttributeError) as e:", "    except ZeroDivisionError as e:", "thu_roi_tinh_moi_luot_duoc_chon_va_khong_goi_git"),
    ("thu_bo_ban_ghi_attempt_ngoai_cohort", '            t.lay(f"att/{x}/{k}", ', '            0 and t.lay(f"att/{x}/{k}", ', "thu_roi_tinh_moi_luot_duoc_chon_va_khong_goi_git"),
    ("thu_log_manh_theo_dong_moi_nhat_theo_ten", "[0] if rid in run_g5 else None\n", "[0] if False else None\n", "thu_roi_tinh_moi_luot_duoc_chon_va_khong_goi_git"),
    ("tinh_attempt_thieu_khong_neu_ten", "(kdd(ly_luot[rid]) if rid in ly_luot else ", "(", "thu_roi_tinh_moi_luot_duoc_chon_va_khong_goi_git"),
    ("tinh_g5_nhan_manh_cua_luot_thieu_attempt", " in theo_khoa2 and rid not in ly_luot", " in theo_khoa2", "thu_roi_tinh_moi_luot_duoc_chon_va_khong_goi_git"),
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
            r = subprocess.run([sys.executable, "-B", str(ban / "thu_thap.py"), "--tu-kiem", "--mot-ca", dich], capture_output=True, text=True, timeout=120,
                               env={**os.environ, "WP1448_GOC_KHO": str(ROOT)})
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
    for co in ("--thu", "--tinh", "--tu-kiem", "--xuat-kiem-ke"):
        ap.add_argument(co, action="store_true")
    for co in ("--ra", "--anh-chup", "--anh-chup-v2", "--cohort-goc", "--run-g5", "--kho", "--mot-ca", "--kiem-ke"):
        ap.add_argument(co)
    ap.add_argument("--han-giay", type=int, default=3600)
    ap.add_argument("--so-luong", type=int, default=6)
    ns = ap.parse_args()
    if sum((ns.thu, ns.tinh, ns.tu_kiem, ns.xuat_kiem_ke)) != 1:
        ap.error("chon DUNG MOT trong --thu | --tinh | --tu-kiem | --xuat-kiem-ke")
    if ns.tu_kiem:
        return lenh_tu_kiem(ns)
    if ns.xuat_kiem_ke:
        if not (ns.kho and ns.ra):
            ap.error("--xuat-kiem-ke can --kho <cay da checkout> --ra <thu muc>")
        return lenh_xuat_kiem_ke(ns)
    if not (ns.anh_chup and ns.ra):
        ap.error("--thu va --tinh can --anh-chup <anh chup #1434> --ra <thu muc>")
    return lenh_thu(ns) if ns.thu else lenh_tinh(ns)


if __name__ == "__main__":
    sys.exit(main())
