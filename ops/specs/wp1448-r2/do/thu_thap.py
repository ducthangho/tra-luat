#!/usr/bin/env python3
"""wp1448 r2 — bo thu v2 (dac ta ops/specs/wp1448-r2/SPEC.md muc 5; r6: ops/specs/wp1448-r6/SPEC.md), CHI DOC. Ke thua hop dong cua bo thu #1434
(`ops/specs/wp1434-r3/do/thu_thap.py`, nap bang duong dan, KHONG sua): anh chup NGOAI kho, ba che do, ba trang thai,
ghi co gioi han, `--tinh` tat dinh, khong mang, KHONG goi git. DO 20-11-2026: `--tinh` cua #1434 tu no phong MOT tien trinh con
(`git check-ignore`, qua `tim()` trong muc §6 cua bao cao); `--tinh` v2 thay muc ay va chan moi lan phong `git` — xem NGUYEN TAC (2).

  --thu --anh-chup <anh chup #1434> --ra <anh chup v2> [--kho <kho git>]
        GitHub REST GET -> them vao MOT thu muc anh chup v2 RIENG (khong ghi vao anh chup #1434): log job gom cong cu, danh
        sach artifact, NOI DUNG bien nhan manh G5 (zip artifact con han) + commit cua head bien nhan, luot + job cua
        `packet-loop-dot-bien.yml`; co `--kho` thi tinh oracle ngu canh moi tu bon OID (git CHI DOC tren kho ay).
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
hoan tat va dau hieu duong; doc cac dong `BONG_CONG_CU`, `BONG_PHAN_LOAI` khi co; thoi gian theo buoc cua `gate` va `gate-ops`;
workflow `packet-loop-dot-bien.yml`; phep quy G4a va G4b (muoi buoc co thu tu, vet can).
Thoi gian G5 (r6, K1): CAT khoi PR1 — khoa `g5_thoi_gian` cua BASELINE_V2.json LUON la `{"ly_do": LY_DO_G5_CAT, "trang_thai":
"khong_do_duoc"}` voi moi dau vao; bo thu KHONG doc, KHONG tai, KHONG tong hop dong `G5_THOI_GIAN` nao (viec cua packet ke nhiem PR1b).

NGUYEN TAC — CHI BANG CHUNG DUONG: mot ket luan "du" / "do duoc" chi co khi TUNG thu no can DA duoc kiem va DAT.
Thu vang, khong doc duoc, khong kiem duoc hay mau thuan KHONG BAO GIO duoc bu bang mot dau hieu khac; buoc xet ca TAP chi co the HA.
  (1) Bien nhan manh — ba tang, moi TEP mot minh: CAU TRUC (`kiem_cau_truc`: khong can kiem ke, khong can tep nao khac) -> HOP DONG tren
      kiem ke cua dung van tay tep khai (`kiem_than`) -> HEAD (`doi_chieu_head`). `du_hoan_tat` chi khi CA tam vi tri deu `hop_le`; dau
      `GOM MẢNH 8/8` cua job gom khong nang cap duoc gi (no chi co the MAU THUAN voi che do da chon). Nguoc lai (r6, WP1448-R5-F8): VANG
      bang chung khong bao gio la giay phep DUA mot luot RA KHOI mau so G4 — chi bang chung duong o buoc 0/1 moi loai duoc.
  (2) `--tinh` khong bao gio phong `git` (`cam_git` tu choi va GHI lai moi lan thu; co lan thu => rc 5, khong ghi ket qua v2). Muc §6 cua
      bao cao #1434 la phep chay tren CAY SONG, khong co trong anh chup: ban tinh lai ghi `khong_do_duoc` cho muc ay (`s6_khong_cay_song`).
  (3) r7: ke hoach ghi kiem TRON truoc khi tao gi (`kiem_ke_hoach_ghi`), moi tep qua `ghi_tep` ke thua; MANIFEST kiem TUNG muc tho truoc khi gom.
"""
import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import types
import warnings
import zipfile

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
# r6 (K1): phan "do day du / do phu thoi gian G5" bi CAT khoi PR1; khoa `g5_thoi_gian` luon mang dung ly do nay (khong phu thuoc dau vao).
LY_DO_G5_CAT = "cat khoi PR1 theo quyet dinh chu kho [E1+E2+E3] issuecomment-7056714807: do day du / do phu thoi gian G5 thuoc packet ke nhiem PR1b - G5 timing collector redesign"


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
    """`a=1 b=2 …` -> dict; phan tu khong co `=` bi bo. Gia tri co the mang `=` (chi tach o dau `=` dau tien). r7 (WP1448-R6-F14, quet moi phep
    gom danh sach -> dict cua dau vao khong tin): khoa LAP voi gia tri KHAC => None (dong mau thuan, KHONG chon ben nao); lap y het van nhan."""
    d = {}
    for k, v in (x.split("=", 1) for x in than.split(" ") if "=" in x):
        if d.setdefault(k, v) != v:
            return None
    return d


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
            if d is None:
                kq["bong_cong_cu" if m.group(1) == "BONG_CONG_CU" else "bong_phan_loai"] = {"quyet_dinh": KHONG_DO_DUOC, "ly_do": "khoa_lap_mau_thuan"}
            elif m.group(1) == "BONG_CONG_CU":
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


def so_lan(x):
    """`run_attempt` -> so nguyen 1..`TRAN_ATTEMPT` | None (chuoi, bool, float, ngoai tran: khong nem, khong doan); vang / null => 1 (nhu #1434)."""
    return 1 if x is None else (x if type(x) is int and 1 <= x <= TRAN_ATTEMPT else None)


def att_dong(d):
    """`run_attempt` cua MOT dong job -> 1..`TRAN_ATTEMPT` | None (r6, WP1448-R5-F9). KHAC `so_lan` cua LUOT: o dong job, vang / null KHONG suy
    ra 1 — dong da chuan hoa (`tinh_luot` cua #1434) luon mang attempt, nen dong thieu no la dong khong xac dinh duoc attempt."""
    x = d.get("run_attempt")
    return None if x is None else so_lan(x)


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
    duoc): CHINH `_phan_manh` cua ma tren bang cua kiem ke ay. Chi dung cho HOP DONG bien nhan (`kiem_bien_nhan`, lop g4-receipt-authority)."""
    kk = chon_kiem_ke([van_tay], cac_kiem_ke) if van_tay else None
    return None if kk is None else nap_cong_cu()[0]["_phan_manh"](k, SO_MANH_G5, [t for t, _ in kk["dot_bien"]])


def dung_luot(run, dong, log=None, artifact=None, bien_nhan=None, cmt=None, kiem_ke=()):
    """Ban ghi CHUAN HOA cua mot luot ci.yml o attempt CUOI, tu: `run` (API), `dong` (dong job: ten, ket_luan, run_attempt,
    head_sha, job_id — moi attempt), `log` ({'chuan_bi': van ban | None, 'gom': van ban | None}), `artifact` (danh sach artifact
    DA DU: ten (chuoi) hoac {name, expired}; None = khong co danh sach), `bien_nhan` ({k: byte tep manh}), `cmt` ({sha: [cha]}) va
    `kiem_ke` (kiem ke them ngoai kiem ke cua cay nay).
    Dong cua attempt cuoi duoc uu tien; job khong chay lai o attempt cuoi lay dong moi nhat cua no (mang sang). CHI dong co attempt HOP LE
    (`att_dong`) va khong lon hon attempt cua luot moi duoc lam dong moi nhat; luot co `run_attempt` khong hop le thi KHONG dong nao."""
    log = log or {}
    so_att = so_lan(run.get("run_attempt"))
    tran = so_att or 0
    moi_nhat = {}
    for d in sorted((d for d in dong if (a := att_dong(d)) is not None and a <= tran), key=lambda d: (att_dong(d) or 0, d.get("job_id") or 0)):
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
    dinh; buoc 10 nhan moi thu con lai. Buoc 0 va 1 dua luot ra NGOAI mau so, nen CHI bang chung DUONG duoc dung o do (r6, WP1448-R5-F8):
    buoc 0 can job `chuan-bi` DA ket thuc `cancelled`/`failure`/`timed_out` (null, vang, `skipped` => o lai mau so, thuong la buoc 2);
    buoc 1 can phan loai cu DO DUOC khac `day_du`."""
    gom, manh, chon = l.get("gom") or {}, l.get("manh") or {}, che_do_chon(l)
    kl_gom, dau = gom.get("ket_luan"), gom.get("dau")
    du_bn = chon in CHE_DO_G5 and du_bien_nhan(l, chon)
    dau_khop = dau in (None, f"gom_manh:{SO_MANH_G5}")             # che do du/dich: dau "KHONG DO" hay so manh khac = mau thuan
    hong = ("cancelled", "failure", "timed_out")
    bi_huy_do = l.get("ket_luan") in hong or kl_gom in hong or any(x in hong for x in manh.get("ket_luan") or ())
    if l.get("chuan_bi") in hong and l.get("lan_cu") is None and l.get("che_do_chay") is None:   # r6 F8: CHI bang chung duong huy/hong
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


def json_mot_nghia(b):
    """`json.loads` ma mot object co khoa LAP => ValueError (khong lang le lay gia tri sau). Cho MANIFEST va kiem ke (dau vao khong tin)."""
    def cap(ds):
        if len({k for k, _ in ds}) != len(ds):
            raise ValueError("object JSON co khoa lap")
        return dict(ds)
    return json.loads(b, object_pairs_hook=cap)


class GhiBiChan(Exception):
    """Ke hoach ghi bi tu choi TRUOC khi tao bat ky thu muc / tep nao (rc 4)."""


def goc_git(p):
    """Thu muc to tien GAN NHAT (ke ca `p`) co `.git` — goc checkout chua `p`, KHONG goi git — hoac None."""
    return next((q for q in (p, *p.parents) if (q / ".git").exists()), None)


def kiem_ke_hoach_ghi(ra, dich, dau_vao=(), nguon=()):
    """r7 (WP1448-R6-F11, lop collector-bounded-output-writes): kiem TOAN BO ke hoach ghi TRUOC khi tao gi, khong tao / sua gi. `ra` da resolve
    (bi danh cua CHINH `ra` duoc phep). Tu choi (GhiBiChan): `ra` trung, nam trong hay CHUA mot dau vao (`dau_vao`: anh chup, kiem ke,
    cohort); `ra` nam trong kho chua bo thu (ROOT) hay cay nguon da chi dinh (`nguon`, ke ca goc checkout `goc_git` cua no); `ra` co ma
    khong phai thu muc; voi moi dich tuong doi (`dich`): BAT KY thanh phan nao da co la symlink, thu muc trung gian khong phai thu muc that,
    la khong phai tep thuong. Tep thuong da co van ghi de duoc (qua `ghi_tep` ke thua: tep tam + os.replace)."""
    for p in (pathlib.Path(x).resolve() for x in dau_vao if x):
        if p == ra or p in ra.parents or ra in p.parents:
            raise GhiBiChan(f"--ra {ra} chong lan dau vao {p}")
    for q in (ROOT, *(pathlib.Path(x).resolve() for x in nguon if x)):
        for r in {q, goc_git(q)} - {None}:
            if r == ra or r in ra.parents or ra in r.parents:      # r8: `--ra` CHUA mot cay nguon (vd checkout ten `nen`) cung bi chan
                raise GhiBiChan(f"--ra {ra} nam trong / chua cay nguon {r}")
    if os.path.lexists(ra) and not ra.is_dir():
        raise GhiBiChan(f"--ra {ra} da co ma khong phai thu muc")
    for rel in dich:
        p, ph = ra, pathlib.PurePosixPath(rel).parts
        for i, x in enumerate(ph):
            p = p / x
            if os.path.islink(p):
                raise GhiBiChan(f"thanh phan dich la symlink: {rel} ({x})")
            if os.path.lexists(p) and not (p.is_file() if i == len(ph) - 1 else p.is_dir()):
                raise GhiBiChan(f"thanh phan dich sai loai: {rel} ({x})")


DICH_TINH = ("nen/BASELINE.json", "nen/COHORT.json", "nen/BAO_CAO.md", "BASELINE_V2.json", "BAO_CAO_V2.md")
DICH_THU = ("META.json", "MANIFEST.json", "MANIFEST.partial.jsonl")


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
        tep = json_mot_nghia(f.read_bytes())["tep"]
        if not isinstance(tep, list) or not all(isinstance(m, dict) and isinstance(m.get("khoa"), str) for m in tep):
            raise TypeError("muc MANIFEST khong phai object co `khoa` chuoi")
    except (ValueError, KeyError, TypeError) as e:
        raise AnhChupHong(f"{ac}: MANIFEST.json khong doc duoc ({type(e).__name__})") from e
    # r7 (WP1448-R6-F14, VA HO cua R1-F5): kiem TUNG muc THO truoc moi phep gom theo khoa — mot muc sau cung khoa (hop le hay vang tep)
    # khong bao gio che duoc muc hong truoc no; hai muc cung khoa ma KHAC nhau la mau thuan (lap y het van nhan: chi giu mot).
    hong, theo_khoa = [], {}
    for m in tep:
        dd = m.get("duong_dan")
        if dd:
            p = (ac / dd).resolve() if isinstance(dd, str) else ac
            if ac not in p.parents or not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != m.get("sha256"):
                hong.append(m["khoa"])
        if theo_khoa.setdefault(m["khoa"], m) != m:
            hong.append(m["khoa"] + " (lap mau thuan)")
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
            kk = json_mot_nghia(tep.read_bytes())
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
    ra, g = pathlib.Path(ns.ra).resolve(), nap_goc()
    try:                                                     # r7 F11: --ra NGOAI kho va NGOAI cay nguon --kho, kiem truoc khi nap / tao gi
        kiem_ke_hoach_ghi(ra, (), nguon=(ns.kho,))
        kk = nap_cong_cu(ns.kho)[1]
        kiem_ke_hoach_ghi(ra, (kk["sha256_test"] + ".json",))
        ra.mkdir(parents=True, exist_ok=True)
        g.ghi_tep(ra, kk["sha256_test"] + ".json", xuat_json(kk))
    except (GhiBiChan, g.GhiBiTuChoi) as e:
        print("TU CHOI GHI:", e)
        return 4
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
    """(`tinh_luot` cua #1434 | None, ly do chan doan | None) cho `--tinh` (G4 + thoi gian buoc). Attempt doc duoi khoa `att/<id>/<k>` cua anh chup;
    `run_attempt` sai, dong job sai kieu => (None, ly do NEU TEN), khong nem; ban ghi attempt thieu => (ban ghi, ly do): chi la muc chan doan
    trong `khong_do_duoc`. Khong ket qua nao o day dua luot ra khoi mau so G4 (r6: `_tinh` giu ban ghi chuan hoa cua luot `lu is None`)."""
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
    try:                                                     # r7 F11: TOAN BO ke hoach ghi kiem TRUOC moi viec (ke ca nen/ cua #1434)
        kiem_ke_hoach_ghi(ra, DICH_TINH, (ac, ns.anh_chup_v2, ns.kiem_ke, ns.cohort_goc))
    except GhiBiChan as e:
        print("TU CHOI GHI:", e)
        return 4
    # review F5: anh chup v2 DA CHI DINH thi kiem toan ven TRUOC moi tinh toan (va truoc ca bo thu #1434); vang `--anh-chup-v2`
    # la "khong co v2" hop le, con chi dinh ma hong thi TU CHOI (rc 3, cung ma voi anh chup #1434 lech MANIFEST). r7 F14: anh chup #1434
    # cung qua `doc_anh_chup` (muc tho, lap mau thuan) TRUOC bo thu #1434.
    doc2, theo_khoa2, man2 = None, {}, None
    try:
        cac_kk = doc_kiem_ke(ns.kiem_ke)
        if ns.anh_chup_v2:
            doc2, theo_khoa2 = doc_anh_chup(ns.anh_chup_v2)
            man2 = hashlib.sha256((pathlib.Path(ns.anh_chup_v2).resolve() / "MANIFEST.json").read_bytes()).hexdigest()
        doc, _ = doc_anh_chup(ac)
    except AnhChupHong as e:
        print("ANH CHUP / KIEM KE HONG:", e)
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
    try:
        rc = g.lenh_tinh(argparse.Namespace(anh_chup=str(ac), ra=str(ra / "nen")))
    except g.GhiBiTuChoi as e:
        print("TU CHOI GHI:", e)
        return 4
    if rc != 0:
        print("bo thu #1434 --tinh tra rc =", rc)
        return rc
    nen_moi = json.loads((ra / "nen" / "BASELINE.json").read_bytes())
    nen_goc = json.loads(NEN_GOC.read_bytes())
    meta = json.loads((ac / "META.json").read_bytes())

    def van_ban(khoa, nguon=doc):
        b = nguon(khoa) if nguon else None
        return None if b is None else b.decode("utf-8", errors="replace")

    ds_ci = []
    for k in meta["khoang_con"]:
        if not k.get("chia_doi"):
            ds_ci += g.chon_chuoi_trang(doc, f"list/ci/{k['su_kien']}/{k['nhan']}")[0]
    co_ci, _ = g.loc_cohort(sorted({r["id"]: r for r in ds_ci}.values(), key=lambda r: r["id"]), g.WF_CI, meta["T0"], meta["T1"])
    luot, buoc, khong_do, bo_dem = [], {}, [], {"loi_ich": {"1": 0, "0": 0, "khong_du_du_lieu": 0}, "ton_du": {"1": 0, "0": 0, "khong_du_du_lieu": 0}}
    for r in co_ci:
        rid, (dong_tho, du, _, ly) = r["id"], g.chon_chuoi_trang(doc, f"jobs/{r['id']}")
        lu, ly = phan_loai_luot(g, r, doc, dong_tho) if du else (None, ly or "danh sach job khong du")
        if ly:
            khong_do.append({"doi_tuong": f"luot {rid}", "ly_do": ly})
        if lu is None:                                      # r6 F8: luot DA BIET cua cohort, bang chung vang => ban ghi CHUAN HOA khong do duoc
            l = dung_luot(r, [])                            # (giu run_id / attempt / su kien / head), KHONG bien mat khoi mau so G4
            l["bang_chung_luot"] = kdd(ly)
        else:
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
                    sha = dau_khai(nd).get("head")
                    bc = doc2(f"cmt/{sha}") if isinstance(sha, str) and RE_OID.fullmatch(sha) else None
                    try:
                        cmt[str(sha)] = [p["sha"] for p in json.loads(bc)["parents"]] if bc is not None else None
                    except (ValueError, KeyError, TypeError):
                        cmt[str(sha)] = None
            l = dung_luot(r, dong, log, art, bn, {k: v for k, v in cmt.items() if v is not None}, cac_kk)
            lan = g.trich_lan(log["chuan_bi"]) if log["chuan_bi"] else None
            for m in lu["dong"]:                                  # thoi gian theo buoc cua gate / gate-ops (dong thuc_thi)
                if m["loai_dong"] == g.THUC_THI and m["ten_goc"] in JOB_BUOC_V2:
                    for b in m["_tho"].get("steps") or []:
                        them_do(buoc, f"{m['ten_goc']} | {m['nen']} | {lan or 'khong_do_duoc'} | {b.get('name')}", g.thoi_luong_buoc(b))
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
          "g5_thoi_gian": {"ly_do": LY_DO_G5_CAT, "trang_thai": KHONG_DO_DUOC},
          "packet_loop_dot_bien": pl, "khong_do_duoc": khong_do, "luot": luot}
    if goi:                                                 # ma duoc nap co the da nuot `GitBiCam`: doc DANH SACH, khong doc ngoai le
        print(f"TU CHOI: --tinh da thu goi git {len(goi)} lan (dac ta muc 5), khong ghi ket qua v2: {goi[:3]}")
        return 5
    b = xuat_json(v2)
    try:                                                     # r7 F11: moi tep qua bo ghi co gioi han ke thua (khong theo symlink / hard link)
        g.ghi_tep(ra, "BASELINE_V2.json", b)
        g.ghi_tep(ra, "BAO_CAO_V2.md", bao_cao(v2).encode("utf-8"))
    except g.GhiBiTuChoi as e:
        print("TU CHOI GHI:", e)
        return 4
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
    g5 = v2["g5_thoi_gian"]
    dong.append(f"## G5 — thoi gian (CAT khoi PR1)\n\n{g5['trang_thai']}: {g5['ly_do']}\n")
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


def ke_hoach_thu(su_kien, cac_job, co_kho=False):
    """Viec phai thu cua MOT luot ci.yml (ham THUAN) -> {log: [job id], bien_nhan: bool, oracle: job id chuan-bi | None}. `cac_job`: dong
    job o attempt CUOI theo ten. LOG: CHI job gom da chay (r6, K2: khong thu log manh — thoi gian G5 da cat). BIEN NHAN (danh sach
    artifact + noi dung + commit cua head khai): moi luot `pull_request` (G4)."""
    log = [d["id"] for ten, d in cac_job.items()
           if (ten or "").startswith(JOB_GOM + " (ubuntu-latest") and d.get("conclusion") not in ("skipped", None)]
    cb = cac_job.get(JOB_CHUAN_BI)
    return {"log": log, "bien_nhan": su_kien == "pull_request", "oracle": cb["id"] if co_kho and cb and su_kien == "pull_request" else None}


def lenh_thu(ns, g=None):
    """`g`: module bo thu #1434 (mac dinh nap tu kho); --tu-kiem trao ban co lop `Thu` van chuyen gia (khong mang)."""
    if g is None and not os.environ.get("GITHUB_PAT"):
        raise SystemExit("thieu bien moi truong GITHUB_PAT")
    g = g or nap_goc()
    ac = pathlib.Path(ns.anh_chup).resolve()
    try:                                                     # r7 F11: anh chup v2 RIENG, ngoai kho / --kho, kiem TRUOC khi dung bo ghi
        kiem_ke_hoach_ghi(pathlib.Path(ns.ra).resolve(), DICH_THU, (ac,), (ns.kho,))
    except GhiBiChan as e:
        raise SystemExit(f"TU CHOI GHI: {e}") from e
    try:
        doc, _ = doc_anh_chup(ac)
    except AnhChupHong as e:
        raise SystemExit(f"anh chup #1434 khong dung duoc: {e}") from e
    meta = json.loads((ac / "META.json").read_bytes())
    t = g.Thu(ns.ra, ns.han_giay, ns.so_luong)
    g.ghi_tep(t.ra, "META.json", xuat_json({"packet": "wp1448", "revision": 2, "anh_chup_goc": {k: meta.get(k) for k in ("T0", "T1", "sha_master")}}))
    ds_ci = []
    for k in meta["khoang_con"]:
        if not k.get("chia_doi"):
            ds_ci += g.chon_chuoi_trang(doc, f"list/ci/{k['su_kien']}/{k['nhan']}")[0]
    co_ci, _ = g.loc_cohort(sorted({r["id"]: r for r in ds_ci}.values(), key=lambda r: r["id"]), g.WF_CI, meta["T0"], meta["T1"])
    viec, oracle, co_bn = [], [], []
    for r in co_ci:
        rid = r["id"]
        dong, du, _, _ = g.chon_chuoi_trang(doc, f"jobs/{rid}")
        if not du:
            continue
        cuoi = {}
        for d in sorted(dong, key=lambda d: (so_lan(d.get("run_attempt")) or 0, d.get("id") or 0)):
            cuoi[d.get("name")] = d
        kh = ke_hoach_thu(r.get("event"), cuoi, bool(ns.kho))
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


def khong_nem(f):                     # phep TOAN PHAN: loi doi so / hinh dang -> `TuKiemDo`; CHI boc dung loi goi ma ca kiem tinh toan phan cua no
    try:
        return f()
    except (OverflowError, ValueError, AttributeError, TypeError, IndexError, KeyError) as e:
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

    def ghi_anh_chup(thu_muc, tep):                   # anh chup tu dung: moi khoa -> `<khoa>.json`, MANIFEST dung tung byte
        muc = []
        for khoa, b in tep.items():
            b, p = b if isinstance(b, bytes) else json.dumps(b).encode(), thu_muc / (khoa + ".json")
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b)
            muc.append({"khoa": khoa, "loai": "x", "url": None, "http": 200, "duong_dan": khoa + ".json", "sha256": hashlib.sha256(b).hexdigest(), "kich_thuoc": len(b)})
        (thu_muc / "MANIFEST.json").write_text(json.dumps({"tep": muc}), encoding="utf-8")
        return muc

    def anh_chup_nho(goc, **v2):
        """r7: anh chup #1434 TOI THIEU (khong qua --thu): MOT luot pull_request 501 — `chuan-bi` (dong bong cu=day_du moi=duong_nhanh), `gate`,
        `gate-ops`, MOI job MOT buoc do duoc (60 s, 60 s, 120 s). `v2` (khoa -> noi dung) => anh chup v2 `goc/v2`. Tra (ac, v2 | None)."""
        T, H = "2026-11-01T00:%02d:00Z", "a" * 40
        run = {"id": 501, "run_attempt": 1, "event": "pull_request", "head_sha": H, "head_branch": "f", "status": "completed", "conclusion": "success", "created_at": T % 1}
        job = lambda i, ten, a, b: {"id": 50100 + i, "name": ten, "conclusion": "success", "run_attempt": 1, "head_sha": H, "created_at": T % 1, "started_at": T % 1,
                                    "completed_at": T % 9, "steps": [{"name": "buoc " + ten[:4], "conclusion": "success", "number": 1, "started_at": T % a, "completed_at": T % b}]}
        ghi_anh_chup(goc / "ac", {"META": {"T0": T % 0, "T1": T % 59, "sha_master": H, "kho": "o/r", "spec_sha256": "0" * 64,
                                           "khoang_con": [{"su_kien": "pull_request", "nhan": "x", "tu": T % 0, "den": T % 59}]},
                                  "list/ci/pull_request/x/p1": {"total_count": 1, "workflow_runs": [run]}, "list/du/p1": {"total_count": 0, "workflow_runs": []},
                                  "jobs/501/p1": {"total_count": 3, "jobs": [job(0, JOB_CHUAN_BI, 2, 3), job(1, "gate (ubuntu-latest)", 3, 4), job(2, "gate-ops (ubuntu-latest)", 4, 6)]},
                                  "log/50100": b"che_do=day_du\nBONG_PHAN_LOAI: cu=day_du moi=duong_nhanh cu_do=do_duoc kiem_moi=dat\n"})
        if v2:
            ghi_anh_chup(goc / "v2", {"META": {}, **v2})
        return goc / "ac", (goc / "v2" if v2 else None)

    def tinh_nho(ac, ra, v2=None, **doi):                # -> rc cua `lenh_tinh` THAT (toan phan: loi doi so / hinh dang => TuKiemDo)
        ns = argparse.Namespace(**{"anh_chup": str(ac), "ra": str(ra), "anh_chup_v2": v2 and str(v2), "cohort_goc": None, "kiem_ke": None, **doi})
        with contextlib.redirect_stdout(io.StringIO()):
            return khong_nem(lambda: lenh_tinh(ns))

    def dau_cuoi(goc):
        """`--thu` THAT (lop `Thu` cua #1434, van chuyen GIA — khong mang) tren anh chup #1434 tu dung trong `goc/ac` -> anh chup v2 `goc/v2`.
        Ba luot cua cohort: 101 pull_request (checkout = merge c*40, cha [d*40, a*40]), 102 push, 103 pull_request ma anh chup KHONG co trang
        job (bang chung vang). API phuc vu DAY DU dau vao ma ma `d0ccd1f` chung nhan thoi gian G5 (log manh `G5_THOI_GIAN` du ba thanh phan cho
        moi dinh danh, bien nhan hop le); bo thu sau cat (r6) khong duoc doc log manh. r7: `--kho` RIENG, dong bong cua 101 khong mang OID.
        Tra {g, rc_thu, thu() -> rc, tinh(ra, v2=None) -> rc, ket_qua(ra) -> BASELINE_V2, log_manh}."""
        mod = nap_cong_cu()[0]
        T = "2026-11-01T00:%02d:00Z"
        luot = {101: ("pull_request", "a" * 40, "c" * 40), 102: ("push", "b" * 40, "b" * 40), 103: ("pull_request", "9" * 40, None)}

        def zip_manh(nd, k):
            b = io.BytesIO()
            with zipfile.ZipFile(b, "w") as z:
                z.writestr(f"manh-{k}.txt", nd)
            return b.getvalue()

        def log_manh(k):
            ten = mod["_phan_manh"](k, SO_MANH_G5)
            bg = [{"loai": "dot_bien", "ten": t_, "trang_thai": DO_DUOC, "bat_dau": 1.0, "ket_thuc": 2.0, "dung_cay_s": 0.1, "ca_dich_s": 0.2, "ca_khac_s": 0.3}
                  for t_ in ten] + [{"loai": "con", "pid": 7, "bat_dau": 0.0, "ket_thuc": 9.0, "so_dot_bien": len(ten)}, {"loai": "cha", "so_con": 1, "tuong_s": 9.5}]
            return "".join("G5_THOI_GIAN " + json.dumps(b) + "\n" for b in bg).encode()
        api, tep1, ds, lm = {"commits/" + "c" * 40: json.dumps({"parents": [{"sha": "d" * 40}, {"sha": "a" * 40}]}).encode(),
                             f"actions/workflows/{WF_PL}/runs": b'{"total_count": 0, "workflow_runs": []}'}, {}, {}, {}
        ten = [JOB_CHUAN_BI] + [f"{JOB_MANH} (ubuntu-latest, {k})" for k in range(SO_MANH_G5)] + [JOB_GOM + " (ubuntu-latest)"]
        for rid, (sk, head, checkout) in luot.items():
            ds.setdefault(sk, []).append({"id": rid, "run_attempt": 1, "event": sk, "head_sha": head, "head_branch": "master", "status": "completed",
                                          "conclusion": "success", "created_at": T % 1})
            if checkout is None:
                continue
            tep1[f"jobs/{rid}/p1"] = json.dumps({"total_count": len(ten), "jobs": [
                {"id": rid * 100 + i, "name": t_, "conclusion": "success", "run_attempt": 1, "head_sha": head, "created_at": T % 1, "started_at": T % 2,
                 "completed_at": T % 9, "steps": []} for i, t_ in enumerate(ten)]}).encode()
            tep1[f"log/{rid * 100}"] = (T % 3 + " che_do=day_du\n" + "BONG_PHAN_LOAI: cu=day_du moi=day_du cu_do=do_duoc\n" * (rid == 101)).encode()
            la = [{"id": rid * 10 + 8, "name": "x" * len(TEN_ART_MANH) + "3", "expired": False}, {"id": rid * 10 + 9, "name": TEN_ART_MANH + "4", "expired": True},
                  {"id": rid * 10 + 5000, "name": TEN_ART_MANH + "x", "expired": False}]   # r8: KHONG phai manh / manh HET HAN / duoi khong phai so: bo qua
            api[f"actions/runs/{rid}/artifacts"] = json.dumps({"total_count": SO_MANH_G5 + 3, "artifacts": la + [   # TRUOC manh that: lay nham la thang
                {"id": rid * 10 + k, "name": TEN_ART_MANH + str(k), "expired": False} for k in range(SO_MANH_G5)]}).encode()
            for a, k in ((la[0], 3), (la[1], 4)):               # noi dung GIA (bien nhan khai head khac): lay nham => 101 mat du_hoan_tat
                api[f"actions/artifacts/{a['id']}/zip"] = zip_manh(tao_bien_nhan("0" * 40)[k], k)
            for k, nd in tao_bien_nhan(checkout).items():
                api[f"actions/artifacts/{rid * 10 + k}/zip"] = zip_manh(nd, k)
                lm[rid * 100 + 1 + k] = api[f"actions/jobs/{rid * 100 + 1 + k}/logs"] = log_manh(k)
            api[f"actions/jobs/{rid * 100 + 9}/logs"] = "GOM MẢNH 8/8\n".encode()
        tep1.update({f"list/ci/{sk}/x/p1": json.dumps({"total_count": len(r), "workflow_runs": r}).encode() for sk, r in ds.items()})
        meta = {"T0": T % 0, "T1": T % 59, "sha_master": "f" * 40, "spec_sha256": "0" * 64, "kho": "o/r",
                "khoang_con": [{"su_kien": sk, "nhan": "x", "tu": T % 0, "den": T % 59} for sk in ("pull_request", "push")]}
        ghi_anh_chup(goc / "ac", {"META": meta, **tep1})
        g = nap_goc()

        class ThuGia(g.Thu):
            def _goi(self, duong):
                b = api.get(duong.split("?")[0])
                return (200, b, None) if b is not None else (404, None, "HTTP 404")
        g.Thu = ThuGia
        (goc / "kho" / ".git").mkdir(parents=True)          # --kho RIENG (dong bong 101 khong mang OID: oracle khong do duoc, KHONG goi git)

        def thu():
            with contextlib.redirect_stdout(io.StringIO()):
                return khong_nem(lambda: lenh_thu(argparse.Namespace(anh_chup=str(goc / "ac"), ra=str(goc / "v2"), han_giay=60, so_luong=1, kho=str(goc / "kho")), g))
        rc_thu = thu()

        def tinh(ra, v2=None):                              # -> rc cua `lenh_tinh`; ket qua doc bang `ket_qua(ra)`
            with contextlib.redirect_stdout(io.StringIO()):
                return lenh_tinh(argparse.Namespace(anh_chup=str(goc / "ac"), ra=str(goc / ra), anh_chup_v2=str(v2 or goc / "v2"), cohort_goc=None, kiem_ke=None))
        return {"g": g, "rc_thu": rc_thu, "thu": thu, "tinh": tinh, "ket_qua": lambda ra: json.loads((goc / ra / "BASELINE_V2.json").read_bytes()), "log_manh": lm}

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
        bang([tach_khoa("cu=duong_nhanh moi=day_du cu=day_du"), tach_khoa("cu=day_du cu=day_du moi=x")] == [None, {"cu": "day_du", "moi": "x"}],
             "r7: khoa LAP gia tri KHAC => None (khong chon ben nao); lap y het van nhan")
        tb = khong_nem(lambda: trich_bong("BONG_PHAN_LOAI: cu=duong_nhanh moi=day_du cu_do=do_duoc cu=day_du\nBONG_CONG_CU: chay duong_dan=a duong_dan=b\n"))
        bang(tb["bong_phan_loai"] == tb["bong_cong_cu"] == {"quyet_dinh": KHONG_DO_DUOC, "ly_do": "khoa_lap_mau_thuan"}
             and dem_bong(DAY_DU, tb["bong_phan_loai"], DUONG_NHANH) == {"loi_ich": None, "ton_du": None}, f"r7: dong bong khoa lap mau thuan => khong du du lieu: {tb}")
        ten = {c["ten"]: c for c in fx["ca"]}
        bang(ten["ca duong PR4 o PR1 (tich hop bong that)"]["mong"] == [1, 1] and ten["MO PHONG sau PR4 (phan loai dang chay = moi)"]["mong"] == [1, 0],
             "ca duong PR4: o PR1 loi ich=1/ton du=1; mo phong sau PR4 loi ich=1/ton du=0")

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
        bang([n for n, _ in KHOA_TAI_LAP] == [   # r6 (nghiem thu 5, mien tru): DU 17 nhan, dung thu tu — khong xoa / doi ten hai khoa M3 duoc mien
            "M2.so_luot", "M2.moi_luot.tat_ca.giay_thuc_thi.tong", "M2.moi_luot.tat_ca.giay_thuc_thi.trung_vi", "M2.moi_luot.tat_ca.giay_thuc_thi.p90",
            "M2.theo_lan", "M2.theo_ket_luan", "M2.theo_buoc.bang[G5 manh].n", "M2.theo_buoc.bang[G5 manh].tong", "M2.theo_buoc.bang[G5 manh].trung_vi",
            "M2.theo_buoc.bang[G5 manh].p90", "M2.moi_luot.theo_su_kien_va_lan[pull_request | day_du].giay_thuc_thi",
            "M2b.bang[gate-registry | ubuntu-latest | ops/ci_provenance_test.py].so_ban_ghi", "M3.bang[ops/cong_cu_test.py]",
            "M3.bang[ops/ci_provenance_test.py]", "M1.muc_ket_qua_theo_khoa.so_khoa", "[DX-2] top5_giay_thuc_thi[0].so_dong_thuc_thi",
            "[DX-2] top5_giay_thuc_thi[0].tong_giay_thuc_thi"], f"KHOA_TAI_LAP phai DU 17 nhan dung thu tu: {[n for n, _ in KHOA_TAI_LAP]}")

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
            ("ban ghi khong phai mang (r6)", m0("BKCON 5")),
            ("ban ghi do thieu tap ca (r6)", m0(["do", bg[1], dich])),
        )
        for ten, bn in cau_truc:
            bang(khong_nem(lambda: kiem_cau_truc(bn[0], 0))[0] is None and not that(bn), f"{ten}: tep 0 phai hong cau truc (va `_gom_manh` cung tu choi bo)")
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
                                ("khoa JSON lap (r7)", d, ('{"sha256_test": "' + "ef" * 32 + '", "ca": ["x"], "dot_bien": [["q", "x"]], "ca": ["y"]}').encode()),
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
                  (R, None, None, None), (None, H, {H: [R]}, False), (None, None, {H: [P, R]}, None),
                  (R, H, {H: "khong phai danh sach"}, True), (R, H, {H: 7}, True))), ("issue_comment", R, H, None, True),   # r6: cha REST sai kieu = VANG, khong nem
                ("issue_comment", R, None, None, None), *((sk, r, hop, c, m) for sk in SU_KIEN_HEAD_LUOT for r, hop, c, m in ((H, H, None, True),
                  (H, None, {H: [P]}, True), (H, X, None, False), (H, False, None, False), (H, H, {H: [P, X]}, True), (R, H, {H: [P, R]}, False),
                  (None, H, None, True), (None, None, None, None)))):              # (R, H, ...): hop khop KHONG vuot qua head goc KHAC cua luot
            bang(khong_nem(lambda: doi_chieu_head(H, head, sk, hop, cmt)) is mong, f"{sk} head={head} hop={hop} cmt={cmt}: mong {mong}")
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
    def manifest_moi_muc_tho_truoc_khi_gom():
        """r7, WP1448-R6-F14 (lop snapshot-manifest-integrity, VA HO cua R1-F5): MOI muc THO cua MANIFEST duoc kiem TRUOC khi gom theo khoa. Muc
        sau cung khoa (tot hay vang tep) khong che duoc muc hong truoc no; hai muc cung khoa KHAC nhau, khoa JSON lap, muc sai hinh dang => tu
        choi. Doi chung: lap Y HET, muc vang tep hop le. Dau-cuoi: `--tinh` THAT tren anh chup v2 / #1434 hong => rc 3, KHONG ghi gi."""
        with tempfile.TemporaryDirectory(prefix="wp1448_mf_") as d:
            goc = pathlib.Path(d)
            ac, v2 = anh_chup_nho(goc, **{"oracle/501": {"oracle": DUONG_NHANH, "phien_ban_oracle": 2}})
            con = json.loads((v2 / "MANIFEST.json").read_bytes())["tep"]
            m = next(x for x in con if x["khoa"] == "oracle/501")
            con.remove(m)
            b = (v2 / m["duong_dan"]).read_bytes()
            for ten, nd in (("xau.json", b"XAU"), ("khac.json", b + b" "), ("../ngoai.json", b)):
                (v2 / ten).write_bytes(nd)
            xau, vang = {**m, "duong_dan": "xau.json"}, {"khoa": m["khoa"], "duong_dan": None, "http": 410, "loi": "HTTP 410"}
            khac = {**m, "duong_dan": "khac.json", "sha256": hashlib.sha256(b + b" ").hexdigest()}

            def thu(muc, tho=None):
                (v2 / "MANIFEST.json").write_bytes(tho or json.dumps({"tep": muc}).encode())
                try:
                    return khong_nem(lambda: doc_anh_chup(v2))[0](m["khoa"])
                except AnhChupHong:
                    return None
            sai = (("hong truoc, tot sau", [xau, m]), ("tot truoc, hong sau", [m, xau]), ("hong truoc, vang tep sau", [xau, vang]),
                   ("ngoai anh chup truoc, tot sau", [{**m, "duong_dan": "../ngoai.json"}, m]), ("hai muc hop le KHAC nhau cung khoa", [m, khac]),
                   ("tot va vang tep cung khoa", [m, vang]), ("doi chung khac khoa: muc hong khoa rieng", [m, {**xau, "khoa": "khac"}]),
                   ("muc khong phai object", [m, 5]), ("khoa khong phai chuoi", [m, {**m, "khoa": 7}]), ("duong_dan khong phai chuoi", [{**m, "duong_dan": 7}]))
            for ten, muc in sai:
                bang(thu(con + muc) is None, f"{ten}: MANIFEST phai bi TU CHOI (AnhChupHong), khong nem loi khac")
            tho = json.dumps({"tep": con + [m]})[:-3] + f', "duong_dan": "xau.json", "duong_dan": "{m["duong_dan"]}"}}]}}'
            bang(thu(None, tho.encode()) is None, f"khoa JSON lap trong mot muc: tu choi, khong lang le lay gia tri sau: {tho[-120:]}")
            bang(thu(con + [m, m]) == b and thu(con + [m, {**vang, "khoa": "arts/9/p1"}]) == b and thu(con + [{**m, "duong_dan": None}]) is None,
                 "doi chung: lap Y HET van nhan; muc vang tep (khoa rieng) hop le")
            for i, (ten, muc) in enumerate(sai[:4]):
                thu(con + muc)
                bang(tinh_nho(ac, goc / f"ra{i}", v2) == 3 and not (goc / f"ra{i}").exists(), f"dau-cuoi {ten}: --tinh phai rc 3, KHONG ghi gi")
            thu(con + [m])
            bang(tinh_nho(ac, goc / "ra_tot", v2) == 0, "doi chung dau-cuoi: anh chup v2 dung => rc 0")
            muc1 = json.loads((ac / "MANIFEST.json").read_bytes())["tep"]
            l1 = next(x for x in muc1 if x["khoa"] == "log/50100")
            (ac / "khac.log").write_bytes(b"che_do=duong_nhanh\n")
            (ac / "MANIFEST.json").write_text(json.dumps({"tep": muc1 + [{**l1, "duong_dan": "khac.log", "sha256": hashlib.sha256(b"che_do=duong_nhanh\n").hexdigest()}]}))
            bang(tinh_nho(ac, goc / "ra1434", v2) == 3 and not (goc / "ra1434").exists(),
                 "anh chup #1434 co hai muc HOP LE khac nhau cung khoa: bo thu tu choi rc 3 TRUOC bo thu #1434, KHONG ghi gi")

    @kiem
    def ghi_co_gioi_han_moi_dich_cua_bo_thu():
        """r7, WP1448-R6-F11 (lop collector-bounded-output-writes): MOI dich ghi cua `--tinh`, `--xuat-kiem-ke`, `--thu` duoc kiem TRON truoc khi
        tao gi, roi di qua `ghi_tep` ke thua. Doi chung: ghi lan dau va ghi DE tep thuong da co => rc 0. Am: symlink o la / o `nen` / o
        `nen/...`, la la thu muc, `--ra` la tep, hard link (tep thuong tro inode NGOAI --ra: phai THAY muc, khong ghi xuyen), `--ra` trung /
        trong / chua mot dau vao, trong kho (ROOT) hay trong cay nguon `--kho` (ke ca goc checkout) => rc 4 (`--thu`: SystemExit) TRUOC moi
        byte ngoai va moi muc moi trong cay."""
        cu = b"CANH GAC NGOAI --ra\n"
        with tempfile.TemporaryDirectory(prefix="wp1448_ghi_") as d:
            goc = pathlib.Path(d)
            ac, v2 = anh_chup_nho(goc, **{"oracle/501": {"oracle": DUONG_NHANH, "phien_ban_oracle": 2}})
            ngoai = goc / "ngoai"
            ngoai.mkdir()

            def canh(ten):
                (ngoai / ten).write_bytes(cu)
                return ngoai / ten

            def cay(p):
                return sorted((str(x.relative_to(p)), x.is_symlink() or not x.is_file() or x.read_bytes()) for x in p.rglob("*"))
            ra = goc / "ra"
            bang(tinh_nho(ac, ra, v2) == 0 and tinh_nho(ac, ra, v2) == 0 and (ra / "BASELINE_V2.json").is_file() and (ra / "nen" / "BASELINE.json").is_file(),
                 "doi chung: --tinh ghi lan dau va ghi DE tep thuong da co => rc 0")
            for i, (ten, dung) in enumerate((
                    ("BAO_CAO_V2.md la symlink", lambda r: (r / "BAO_CAO_V2.md").symlink_to(canh("bc"))),
                    ("BASELINE_V2.json la symlink", lambda r: (r / "BASELINE_V2.json").symlink_to(canh("bl"))),
                    ("nen la symlink thu muc", lambda r: (r / "nen").symlink_to(ngoai, target_is_directory=True)),
                    ("nen/BASELINE.json la symlink", lambda r: ((r / "nen").mkdir(), (r / "nen" / "BASELINE.json").symlink_to(canh("nb")))),
                    ("BASELINE_V2.json la thu muc", lambda r: (r / "BASELINE_V2.json").mkdir()))):
                r = goc / f"ra_sl{i}"
                r.mkdir()
                dung(r)
                truoc = cay(goc)
                bang(tinh_nho(ac, r, v2) == 4 and cay(goc) == truoc, f"{ten}: --tinh phai rc 4 TRUOC moi lan ghi (khong byte nao ngoai, khong muc moi)")
            r = goc / "ra_la_tep"
            r.write_bytes(cu)
            try:
                rc = tinh_nho(ac, r, v2)
            except OSError as e:
                rc = f"nem {type(e).__name__}"
            bang(rc == 4 and r.read_bytes() == cu, f"--ra la tep thuong: rc 4, duoc {rc!r}")
            r = goc / "ra_hl"
            r.mkdir()
            for t in ("BASELINE_V2.json", "BAO_CAO_V2.md"):
                os.link(canh("hl_" + t), r / t)
            bang(tinh_nho(ac, r, v2) == 0 and all((ngoai / ("hl_" + t)).read_bytes() == cu and (r / t).read_bytes() != cu for t in ("BASELINE_V2.json", "BAO_CAO_V2.md")),
                 "hard link: tep o --ra duoc THAY (tep tam + os.replace), inode ngoai --ra giu nguyen")
            (goc / "kk_dir").mkdir()
            (goc / "coh").mkdir()
            (goc / "coh" / "c.json").write_text(json.dumps({"cap_run_attempt": {"ci.yml": [[501, 1]]}}))
            for ten, r, doi in (("--ra = anh chup #1434", ac, {}), ("--ra trong anh chup #1434", ac / "con", {}), ("--ra chua anh chup #1434", goc, {}),
                                ("--ra trong anh chup v2", v2 / "con", {}), ("--ra = --kiem-ke", goc / "kk_dir", {"kiem_ke": str(goc / "kk_dir")}),
                                ("--ra chua --cohort-goc", goc / "coh", {"cohort_goc": str(goc / "coh" / "c.json")})):
                truoc = cay(goc)
                bang(tinh_nho(ac, r, v2, **doi) == 4 and cay(goc) == truoc, f"{ten}: --tinh phai rc 4, cay khong doi")
            kk, nap_that, goc_kho = nap_cong_cu()[1], globals()["nap_cong_cu"], globals()["ROOT"]
            la, src = kk["sha256_test"] + ".json", goc / "src"
            (src / ".git").mkdir(parents=True)
            (src / "con").mkdir()

            def xuat(r, kho):
                with contextlib.redirect_stdout(io.StringIO()):
                    return lenh_xuat_kiem_ke(argparse.Namespace(ra=str(r), kho=str(kho)))
            try:
                globals()["nap_cong_cu"] = lambda goc=None: (None, kk)       # khong nap ma cua `src` (cay gia): kiem ke cua cay nay
                bang(xuat(goc / "kk", src) == 0 and xuat(goc / "kk", src) == 0 and (goc / "kk" / la).read_bytes() == xuat_json(kk),
                     "doi chung: --xuat-kiem-ke ghi lan dau va ghi de => rc 0")
                (goc / "kk2").mkdir()
                (goc / "kk2" / la).symlink_to(canh("kk_sl"))
                (goc / "kk3").mkdir()
                os.link(canh("kk_hl"), goc / "kk3" / la)
                bang(xuat(goc / "kk2", src) == 4 and (ngoai / "kk_sl").read_bytes() == cu and (goc / "kk2" / la).is_symlink(), "--xuat-kiem-ke la symlink: rc 4")
                bang(xuat(goc / "kk3", src) == 0 and (ngoai / "kk_hl").read_bytes() == cu and (goc / "kk3" / la).read_bytes() == xuat_json(kk),
                     "--xuat-kiem-ke hard link: thay muc, inode ngoai giu nguyen")
                for ten, r, kho in (("trong --kho", src / "ra", src), ("trong goc checkout cua --kho", src / "ra2", src / "con")):
                    bang(xuat(r, kho) == 4 and not r.exists(), f"--xuat-kiem-ke --ra {ten}: rc 4, khong tao gi")
                globals()["ROOT"] = goc / "kho_gia"
                (goc / "kho_gia").mkdir()
                truoc = cay(goc)
                bang(tinh_nho(ac, goc / "kho_gia" / "ra", v2) == 4 and xuat(goc / "kho_gia" / "kk", src) == 4 and cay(goc) == truoc,
                     "--ra trong kho chua bo thu (ROOT): --tinh va --xuat-kiem-ke rc 4, khong tao gi")
                globals()["ROOT"] = goc / "ngoai_ra" / "nen"                 # r8 (hunt a review 7): --ra NGOAI chua checkout trung ten dich `nen`
                (goc / "ngoai_ra" / "nen" / ".git").mkdir(parents=True)
                (goc / "ngoai_thu" / "log" / ".git").mkdir(parents=True)
                truoc = cay(goc)
                bang(tinh_nho(ac, goc / "ngoai_ra", v2) == 4 and cay(goc) == truoc, "--ra CHUA checkout ten `nen` (ROOT): --tinh rc 4, khong ghi vao checkout")
            finally:
                globals()["nap_cong_cu"], globals()["ROOT"] = nap_that, goc_kho
            g = nap_goc()

            class ThuGia(g.Thu):
                def _goi(self, duong):
                    return 404, None, "HTTP 404"
            g.Thu = ThuGia
            for ten, r, kho in (("--ra = anh chup", ac, None), ("--ra trong anh chup", ac / "con", None), ("--ra trong --kho", src / "v2", src),
                                ("--ra chua --kho ten `log`", goc / "ngoai_thu", goc / "ngoai_thu" / "log")):
                truoc = cay(goc)
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        thoat = lenh_thu(argparse.Namespace(anh_chup=str(ac), ra=str(r), han_giay=1, so_luong=1, kho=kho and str(kho)), g)
                except SystemExit as e:
                    thoat = str(e)
                bang(str(thoat).startswith("TU CHOI GHI") and cay(goc) == truoc, f"--thu {ten}: SystemExit TRUOC khi dung bo ghi, cay khong doi: {thoat!r}")

    @kiem
    def tinh_dau_cuoi_oracle_v2_buoc_gate_artifact_cohort():
        """r7, WP1448-R6-F12 (lop new-guard-mutation-coverage; ranh gioi la base 64fa515 — TOAN BO bo thu moi o PR1): `--tinh` THAT tren anh chup
        TOI THIEU, ky vong DOC LAP (literal). Oracle v2 => ton du DEM duoc, oracle ba OID (phien_ban 1) => khong du du lieu; buoc do duoc cua
        `gate` / `gate-ops` — va CHI hai job ay — vao thoi gian buoc; danh sach artifact het han => ly do tung vi tri; khong v2 => van chay;
        `--cohort-goc` loc luot; khong co muc `khong_do_duoc` vo co."""
        art = {"total_count": 8, "artifacts": [{"id": i, "name": TEN_ART_MANH + str(i), "expired": True} for i in range(SO_MANH_G5)]}
        tk = lambda s: {"lon_nhat": s, "n": 1, "nho_nhat": s, "p90": s, "so_khong_ap_dung": 0, "so_loai": 0, "tong": s, "trang_thai": DO_DUOC, "trung_vi": s}
        dem_ = lambda c, d: {"loi_ich": {"0": 0, "1": 1, "khong_du_du_lieu": 0}, "ton_du": {"0": 0, "1": c, "khong_du_du_lieu": d}}
        kq = {}
        with tempfile.TemporaryDirectory(prefix="wp1448_f12_") as d:
            goc = pathlib.Path(d)
            for ten, pb in (("v2", 2), ("ba_oid", 1), ("khong_v2", None)):
                ac, v2 = anh_chup_nho(goc / ten, **({"oracle/501": {"oracle": DUONG_NHANH, "phien_ban_oracle": pb}, "arts/501/p1": art,
                                                      "list/pl/p1": {"total_count": 0, "workflow_runs": []}} if pb else {}))
                kq[ten] = (tinh_nho(ac, goc / ten / "ra", v2), json.loads((goc / ten / "ra" / "BASELINE_V2.json").read_bytes()))
            (goc / "c.json").write_text(json.dumps({"cap_run_attempt": {"ci.yml": []}}))
            kq["cohort"] = (tinh_nho(ac, goc / "ra_c", cohort_goc=str(goc / "c.json")), json.loads((goc / "ra_c" / "BASELINE_V2.json").read_bytes()))
        bang([kq[k][0] for k in kq] == [0, 0, 0, 0], f"bon lan --tinh phai rc 0: {[(k, kq[k][0]) for k in kq]}")
        o, l = kq["v2"][1], kq["v2"][1]["luot"][0]
        bang(o["bong"]["bo_dem_pull_request"] == dem_(1, 0), f"oracle v2 (phien_ban 2) hop le => ton du DEM: {o['bong']['bo_dem_pull_request']}")
        bang(kq["ba_oid"][1]["bong"]["bo_dem_pull_request"] == dem_(0, 1), f"oracle ba OID (phien_ban 1) KHONG duoc dung: {kq['ba_oid'][1]['bong']['bo_dem_pull_request']}")
        bang(o["thoi_gian_buoc_gate_gate_ops"] == {"gate | khong_ro | khong_do_duoc | buoc gate": tk(60), "gate-ops | khong_ro | khong_do_duoc | buoc gate": tk(120)},
             f"buoc do duoc cua gate (60 s) va gate-ops (120 s), KHONG buoc cua chuan-bi: {o['thoi_gian_buoc_gate_gate_ops']}")
        bang(l["manh"]["ly_do"] == ["artifact_het_han"] * SO_MANH_G5 and l["manh"]["nguon_bien_nhan"] == "khong_co_noi_dung+danh_sach_artifact"
             and o["khong_do_duoc"] == [] and o["packet_loop_dot_bien"]["trang_thai"] == DO_DUOC and o["packet_loop_dot_bien"]["so_luot"] == 0,
             f"danh sach artifact het han, khong noi dung, packet-loop do duoc, khong muc khong_do_duoc vo co: {l['manh']} {o['khong_do_duoc']} {o['packet_loop_dot_bien']}")
        o = kq["khong_v2"][1]
        bang(o["luot"][0]["manh"]["ly_do"] == ["job_khong_success"] * SO_MANH_G5 and o["luot"][0]["manh"]["nguon_bien_nhan"] == "khong_co_noi_dung"
             and o["packet_loop_dot_bien"] == kdd("chua thu (can --thu cua bo thu v2 vao --anh-chup-v2)") and o["bong"]["bo_dem_pull_request"] == dem_(0, 1),
             f"khong anh chup v2: van chay, khong bien nhan / oracle / packet-loop: {o['luot'][0]['manh']} {o['packet_loop_dot_bien']}")
        bang(kq["cohort"][1]["luot"] == [] and kq["cohort"][1]["G4"]["so_luot_pull_request"] == 0, f"--cohort-goc rong => khong luot nao: {kq['cohort'][1]['G4']}")

    @kiem
    def oracle_moi_chot_fail_close_git_gia():
        """r7, WP1448-R6-F12: cac chot cua `oracle_moi` ma ca that t115/t118/t119 cua ops/ci_duong_nhanh_test.py KHONG giet khi go (do bang
        oracle_t119.py, handoff r7), tren git GIA (doi so `chay`, KHONG phong tien trinh): OID sai dang, dong rev-list cua commit KHAC, nhieu
        merge-base, merge-tree hong, diff khong ket thuc NUL / ban ghi la => khong_do_duoc; tep ma cap nong, mode thuc thi, sua dac ta => day_du.
        Doi chung: cung dau vao hop le => duong_nhanh; THEM dac ta moi (A) van duong_nhanh."""
        P1, D, HOP = "b" * 40, "c" * 40, "e" * 40

        def hoi(sua=(), gs="a" * 40):
            tra = {"rev-list": (0, f"{HOP} {P1} {D}\n"), "--is-ancestor": (0, ""), "--all": (0, "f" * 40 + "\n"), "merge-tree": (0, "9" * 40 + "\n"),
                   "diff": (0, ":100644 100644 1 2 M\0ops/land/x.yaml\0"), **dict(sua)}

            def chay(lenh, **k):
                rc, ra = tra[next(x for x in tra if x in lenh)]
                return types.SimpleNamespace(returncode=rc, stdout=ra.encode())
            return khong_nem(lambda: oracle_moi("/kho_gia", gs, None, D, HOP, chay))
        bang(hoi() == hoi([("diff", (0, ":000000 100644 0 2 A\0ops/specs/y.md\0"))]) == DUONG_NHANH, "doi chung: ho so hop le / them dac ta moi => duong_nhanh")
        for ten, sua, mong in (
                ("goc su kien khong phai OID", "x", KHONG_DO_DUOC), ("rev-list tra commit KHAC merge ref", [("rev-list", (0, f"{'d' * 40} {P1} {D}\n"))], KHONG_DO_DUOC),
                ("hai merge-base", [("--all", (0, "f" * 40 + "\n" + "8" * 40 + "\n"))], KHONG_DO_DUOC), ("merge-tree in them dong", [("merge-tree", (0, "9" * 40 + "\nxung dot\n"))], KHONG_DO_DUOC),
                ("diff khong ket thuc NUL", [("diff", (0, ":100644 100644 1 2 M\0ops/land/x.yaml"))], KHONG_DO_DUOC),
                ("ban ghi diff la", [("diff", (0, ":100644 100644 1 2 X\0ops/land/x.yaml\0"))], KHONG_DO_DUOC),
                ("tep ma cap nong trong ho so", [("diff", (0, ":100644 100644 1 2 M\0ops/land/x.py\0"))], DAY_DU),
                ("mode moi thuc thi", [("diff", (0, ":100644 100755 1 2 M\0ops/land/x.yaml\0"))], DAY_DU),
                ("sua dac ta da co", [("diff", (0, ":100644 100644 1 2 M\0ops/specs/x.md\0"))], DAY_DU)):
            kq = hoi(gs=sua) if isinstance(sua, str) else hoi(sua)
            bang(kq == mong, f"oracle_moi {ten}: mong {mong}, duoc {kq}")

    @kiem
    def g4_vang_bang_chung_khong_ra_khoi_mau_so():
        """r6, WP1448-R5-F8 (lop g4-denominator-evidence): VANG bang chung khong bao gio dua mot luot pull_request RA KHOI mau so G4. Buoc 0
        can job `chuan-bi` DA ket thuc huy/hong (bang chung duong); null, vang, `skipped` => o lai, `thieu_bang_chung` buoc 2. Dau-cuoi: luot
        pull_request CUA cohort ma anh chup khong co trang job van la MOT ban ghi chuan hoa (run_id, attempt, su kien, head, ly do) buoc 2."""
        fx = J("g4b/b05_du_hoan_tat.json")
        khong_log = {**fx, "log": {"chuan_bi": None, "gom": fx["log"]["gom"]}}

        def voi_chuan_bi(kl, fx_=khong_log):
            dong = [d for d in fx_["dong"] if d["ten"] != JOB_CHUAN_BI] + ([] if kl == "vang" else
                                                                           [{**next(d for d in fx_["dong"] if d["ten"] == JOB_CHUAN_BI), "ket_luan": kl}])
            return luot_fixture({**fx_, "dong": dong}, F)
        bang(quy_g4b(luot_fixture(fx, F)) == ("du_hoan_tat", 5), "doi chung: luot du bang chung => du_hoan_tat/5")
        for kl in ("success", None, "vang", "skipped", "neutral"):
            l = voi_chuan_bi(kl)
            bang(quy_g4b(l) == ("thieu_bang_chung", 2), f"chuan-bi {kl!r}, khong log phan loai: vang bang chung => o lai mau so buoc 2, duoc {quy_g4b(l)}")
        for kl in ("cancelled", "failure", "timed_out"):
            bang(quy_g4b(voi_chuan_bi(kl)) == ("huy_truoc_phan_loai", 0), f"chuan-bi {kl}: bang chung DUONG huy truoc phan loai => buoc 0")
            bang(quy_g4b(voi_chuan_bi(kl, fx)) == ("du_hoan_tat", 5), f"chuan-bi {kl} nhung log DA in che do: khong phai buoc 0")
        t = tong_hop_g4([voi_chuan_bi(None), voi_chuan_bi("vang"), voi_chuan_bi("cancelled")])
        bang([t["so_luot_pull_request"], t["mau_so"], t["G4b"]["thieu_bang_chung"], t["G4b_theo_buoc"]["0"], t["thieu_bang_chung_ti_le"]] == [3, 2, 2, 1, 1.0],
             f"null/vang o lai mau so (2/2 thieu bang chung), chi luot huy DUONG ra ngoai: {t}")
        with tempfile.TemporaryDirectory(prefix="wp1448_g4v_") as d:
            dc = dau_cuoi(pathlib.Path(d))
            dc["tinh"]("ra")
            v2 = dc["ket_qua"]("ra")
        g4, l3 = v2["G4"], [l for l in v2["luot"] if l["run_id"] == 103]
        bang([g4["so_luot_pull_request"], g4["mau_so"], g4["G4b"]["du_hoan_tat"], g4["G4b_theo_buoc"]["2"], g4["thieu_bang_chung_ti_le"]] == [2, 2, 1, 1, 0.5],
             f"dau-cuoi: luot 103 (pull_request, anh chup vang trang job) VAN trong mau so G4, buoc 2: {g4}")
        bang(len(l3) == 1 and [l3[0][k] for k in ("attempt", "su_kien", "head", "g4b", "g4b_buoc")] == [1, "pull_request", "9" * 40, "thieu_bang_chung", 2]
             and (l3[0].get("bang_chung_luot") or {}).get("trang_thai") == "khong_do_duoc" and "jobs/103/p1" in str(l3[0]["bang_chung_luot"]["ly_do"])
             and {"doi_tuong": "luot 103", "ly_do": l3[0]["bang_chung_luot"]["ly_do"]} in v2["khong_do_duoc"],
             f"ban ghi chuan hoa giu dinh danh luot va LY DO (vang trang job KHAC khong job): {l3}")

    @kiem
    def dung_luot_chi_dong_attempt_hop_le_la_moi_nhat():
        """r6, WP1448-R5-F9 (lop new-guard-mutation-coverage): dong job mang attempt KHONG hop le (chuoi, bool, float, 0, ngoai tran, so qua lon,
        null, vang khoa) hay attempt LON HON attempt cua luot khong bao gio la dong moi nhat; luot co `run_attempt` khong hop le thi khong dong nao.
        Doi chung: dong hop le va dong mang sang (rerun) van dung. Kem so lan attempt (`so_lan`) va phep do khong do duoc van duoc dem."""
        fx = J("g4b/b05_du_hoan_tat.json")
        ten_gom = JOB_GOM + " (ubuntu-latest)"

        def gom_att(x, run_att=1, xoa=False):
            dong = [({k: v for k, v in d.items() if k != "run_attempt"} if xoa else {**d, "run_attempt": x}) if d["ten"] == ten_gom else d for d in fx["dong"]]
            return luot_fixture({**fx, "run": {**fx["run"], "run_attempt": run_att}, "dong": dong}, F)
        bang(quy_g4b(gom_att(1)) == ("du_hoan_tat", 5), "doi chung: gom attempt 1 hop le, success => du_hoan_tat/5")
        bang(quy_g4b(luot_fixture(J("g4b/b05_rerun_mang_sang_gom_lan_hai.json"), F)) == ("du_hoan_tat", 5), "doi chung: rerun + dong mang sang van du_hoan_tat")
        for x in ("bad", "1", True, 1.0, 1.5, 0, -1, TRAN_ATTEMPT + 1, 10 ** 400, float("nan"), None):
            l = gom_att(x)
            bang(l["gom"]["ket_luan"] is None and quy_g4b(l) == ("gom_hong", 7), f"gom run_attempt={x!r} (khong hop le): khong la dong moi nhat => gom_hong/7, duoc {quy_g4b(l)}")
        l = gom_att(None, xoa=True)
        bang(l["gom"]["ket_luan"] is None and quy_g4b(l) == ("gom_hong", 7), f"gom VANG khoa run_attempt: khong suy ra 1 => gom_hong/7, duoc {quy_g4b(l)}")
        l = gom_att(2)
        bang(l["gom"]["ket_luan"] is None and quy_g4b(l) == ("gom_hong", 7), f"gom attempt 2 > attempt 1 cua luot: khong la dong moi nhat, duoc {quy_g4b(l)}")
        bang(quy_g4b(gom_att(2, 2)) == ("du_hoan_tat", 5), "doi chung: luot attempt 2, gom attempt 2 => dong moi nhat hop le")
        l = gom_att(1, "x")
        bang(l["attempt"] is None and l["gom"]["ket_luan"] is None and l["chuan_bi"] is None and quy_g4b(l) == ("gom_hong", 7),
             f"luot run_attempt khong hop le: KHONG dong nao la dong moi nhat: {l['attempt']} {l['gom']} {quy_g4b(l)}")
        bang([so_lan(x) for x in (None, 1, 50, 0, 51, 10 ** 400, True, 1.0, "2", float("nan"))] == [1, 1, 50] + [None] * 7, "so lan attempt: 1..50, khac => None")
        b = {}
        for t in ({"trang_thai": DO_DUOC, "gia_tri": 7}, kdd("thieu moc"), {"trang_thai": KHONG_AP_DUNG}):
            them_do(b, "x", t)
        bang(b == {"x": {"v": [7], "loai": 1, "kad": 1}}, f"phep do khong do duoc van duoc DEM (so_loai), khong bien mat: {b}")

    @kiem
    def g5_thoi_gian_cat_luon_khong_do_duoc():
        """r6 (K4, D1): phan thoi gian G5 da CAT khoi PR1 KHONG BAO GIO bao day du / dung duoc. Dau vao: `--thu` -> `--tinh` THAT tren API mang du
        log manh `G5_THOI_GIAN` (du ba thanh phan cho moi dinh danh) va bien nhan hop le => dau ra F; `--tinh` THAT tren anh chup v2 CU (META
        `run_g5` + log manh day du, MANIFEST dung) => dau ra L. Oracle DOC LAP voi mo-dun: ly do so bang sha256 DONG BANG o dac ta r6, trang thai so
        voi chuoi literal. Thu tu: P-i, P-ii, P-iii tren F, roi tren L, roi P-iv, P-v; moi `bang` mang nhan tinh chat [K4-…]."""
        sha_ly_do = "1e75783f949f1d0a49024d68315dff7bf940298cbc1fa3db2f851966ce2deac2"
        cam = ("dat_95_phan_tram", "ti_le_du", "so_du_ba_thanh_phan", "so_mong", "do_day_du", "doi_chieu", "theo_luot")

        def khoa_cam(o, duong="v2"):
            if isinstance(o, dict):
                return [f"{duong}.{k}" for k in o if k in cam] + [x for k, v in o.items() for x in khoa_cam(v, f"{duong}.{k}")]
            return [x for i, v in enumerate(o) for x in khoa_cam(v, f"{duong}[{i}]")] if isinstance(o, list) else []
        with tempfile.TemporaryDirectory(prefix="wp1448_g5cat_") as d:
            goc = pathlib.Path(d)
            dc = dau_cuoi(goc)
            dc["tinh"]("raF")
            ra = {"F": dc["ket_qua"]("raF")}
            cu, g = goc / "v2cu", dc["g"]
            shutil.copytree(goc / "v2", cu)
            muc = [m for m in json.loads((cu / "MANIFEST.json").read_bytes())["tep"] if m["khoa"] != "META"]
            g.ghi_tep(cu, "META.json", xuat_json({**json.loads((cu / "META.json").read_bytes()), "run_g5": [101]}))
            for j, b in ((j, b) for j, b in dc["log_manh"].items() if j // 100 == 101):     # luot pull_request co du bien nhan: ma d0ccd1f chung nhan 499/499
                g.ghi_tep(cu, f"log/{j}.log", b)
                muc.append({"khoa": f"log/{j}", "loai": "log", "url": None, "http": 200, "duong_dan": f"log/{j}.log", "sha256": g.sha256_bytes(b), "kich_thuoc": len(b)})
            with contextlib.redirect_stdout(io.StringIO()):
                g.dong_manifest(cu, muc)
            dc["tinh"]("raL", cu)
            ra["L"] = dc["ket_qua"]("raL")
            bc = {k: (goc / ("ra" + k) / "BAO_CAO_V2.md").read_text(encoding="utf-8") for k in ra}
        for k in ("F", "L"):
            v2 = ra[k]
            g5 = v2.get("g5_thoi_gian")
            bang(isinstance(g5, dict) and set(g5) == {"ly_do", "trang_thai"}, f"[K4-i] {k}: g5_thoi_gian phai la dict DUNG hai khoa ly_do, trang_thai: {g5}")
            bang(g5["trang_thai"] == "khong_do_duoc", f"[K4-i] {k}: trang_thai phai la khong_do_duoc, duoc {g5['trang_thai']!r}")
            bang(isinstance(g5["ly_do"], str) and hashlib.sha256(g5["ly_do"].encode("utf-8")).hexdigest() == sha_ly_do,
                 f"[K4-i] {k}: ly do khac chuoi K1 dong bang (sha256): {g5['ly_do']!r}")
            bang(khoa_cam(v2) == [], f"[K4-ii] {k}: khoa chung nhan thoi gian G5 o BASELINE_V2.json: {khoa_cam(v2)}")
            muc_g5 = ("\n" + bc[k]).split("\n## G5", 1)[-1].split("\n## ", 1)[0] if "\n## G5" in "\n" + bc[k] else ""
            bang(g5["ly_do"] in muc_g5 and "khong_do_duoc" in muc_g5, f"[K4-iii] {k}: muc G5 cua BAO_CAO_V2.md phai neu ly do va khong_do_duoc: {muc_g5!r}")

        def goi_main(*doi):
            cu_argv, ra_, loi = sys.argv, io.StringIO(), io.StringIO()
            try:
                sys.argv = [str(pathlib.Path(__file__)), *doi]
                with contextlib.redirect_stdout(ra_), contextlib.redirect_stderr(loi):
                    try:
                        ma = main()
                    except SystemExit as e:
                        ma = e.code
            finally:
                sys.argv = cu_argv
            return ma, loi.getvalue()
        doi = ("--tu-kiem", "--mot-ca", "tai_lap_khoa_ba_trang_thai")
        ma0, _ = goi_main(*doi)
        ma, loi = goi_main(*doi, "--run-g5", "1")
        bang(ma0 == 0, f"[K4-iv] doi chung: argv hop le phai ra ma 0, duoc {ma0!r}")
        bang(ma == 2 and "unrecognized arguments: --run-g5 1" in loi, f"[K4-iv] --run-g5 phai bi tu choi VI chinh no (ma 2 + chan doan), duoc {ma!r} {loi[-200:]!r}")
        con = [t for t in ("RE_G5", "hop_khoang", "trich_g5", "so_do", "khoang_do", "tap_con", "tong_hop_g5", "tong_hop_g5_luot") if t in globals()]
        bang(con == [], f"[K4-v] API thoi gian G5 da go van con trong mo-dun: {con}")

    @kiem
    def thu_roi_tinh_khong_goi_git_va_pull_request_du_hoan_tat():
        """review 3 F7 + r6 K4, DAU-CUOI tren ma that: `lenh_thu` (lop `Thu` cua #1434, van chuyen GIA — khong mang) -> anh chup v2 -> `lenh_tinh`
        (gom ca `--tinh` cua #1434). `cam_git` chan va ghi moi lan goi git; `--tinh` goi git => rc 5, khong ghi v2; luot pull_request du tam bien
        nhan THAT => du_hoan_tat; `phan_loai_luot` toan phan. Kem: head cua luot `push` doi chieu theo su kien (goi THANG `dung_luot`)."""
        mod, cay = nap_cong_cu()
        popen = subprocess.Popen
        kh = lambda sk, cb=None: ke_hoach_thu(sk, {JOB_MANH + " (ubuntu-latest, 0)": {"id": 5, "conclusion": "success"},
                                                   JOB_GOM + " (ubuntu-latest)": {"id": 9, "conclusion": "success"}, **({JOB_CHUAN_BI: {"id": 1}} if cb else {})}, cb)
        bang([kh("push"), kh("pull_request"), kh("pull_request", True)] == [{"log": [9], "bien_nhan": False, "oracle": None},
             {"log": [9], "bien_nhan": True, "oracle": None}, {"log": [9], "bien_nhan": True, "oracle": 1}],
             "ke hoach thu: CHI log job gom (khong log manh); bien nhan cho pull_request; oracle chi khi co --kho")
        with cam_git() as goi:
            for lenh in (["git", "--version"], "git --version", ["/usr/bin/git", "status"]):
                try:
                    subprocess.run(lenh, capture_output=True, shell=isinstance(lenh, str))
                except GitBiCam:
                    continue
                raise TuKiemDo(f"cam_git khong chan {lenh!r}")
            try:
                khac = subprocess.run([sys.executable, "-c", "print(7)"], capture_output=True, text=True).stdout.strip()
            except GitBiCam:                            # chan ca tien trinh KHONG phai git: sai, va phai DO (khong HONG)
                khac = None
        bang(len(goi) == 3 and khac == "7" and subprocess.Popen is popen, f"cam_git: chan va GHI moi lan goi git, de yen tien trinh khac, tra Popen nhu cu: {goi} {khac!r}")
        with tempfile.TemporaryDirectory(prefix="wp1448_dc_") as d:
            goc = pathlib.Path(d)
            dc = dau_cuoi(goc)
            g = dc["g"]
            bang(str(khong_nem(lambda: phan_loai_luot(g, {"id": 1, "run_attempt": "x"}, None, []))[1]).startswith("run_attempt khong phai so nguyen")
                 and phan_loai_luot(g, {"id": 1, "run_attempt": 10 ** 400}, None, [])[0] is None    # SAU "x": ban bo chot ay se lap vo han o day
                 and str(khong_nem(lambda: phan_loai_luot(g, {"id": 1, "run_attempt": 1}, None, [{"run_attempt": "x"}]))[1]).startswith("dong job")
                 and str(khong_nem(lambda: phan_loai_luot(g, {"id": 1, "run_attempt": 2}, lambda k: b"[1]", []))[1]).startswith("thieu ban ghi attempt [1, 2]"),
                 "phan loai luot TOAN PHAN: run_attempt sai, dong job sai kieu, ban ghi attempt khong phai object => ly do NEU TEN, khong nem")
            s6_dung = globals()["s6_khong_cay_song"]
            try:
                globals()["s6_khong_cay_song"] = g.phan_loai_s6     # ban GOC cua #1434 (cay song, goi git): `--tinh` phai TU CHOI
                with contextlib.redirect_stdout(io.StringIO()):
                    rc_git = lenh_tinh(argparse.Namespace(anh_chup=str(goc / "ac"), ra=str(goc / "ra2"), anh_chup_v2=str(goc / "v2"), cohort_goc=None, kiem_ke=None))
            finally:
                globals()["s6_khong_cay_song"] = s6_dung
            rc = dc["tinh"]("ra")
            bang((dc["rc_thu"], rc) == (0, 0) and subprocess.Popen is popen, f"--thu roi --tinh phai chay tron (rc 0, 0), duoc {(dc['rc_thu'], rc)}")
            v2 = dc["ket_qua"]("ra")
            khoa_v2 = {m["khoa"] for m in json.loads((goc / "v2" / "MANIFEST.json").read_bytes())["tep"]}
            bang({"arts/101/p1", "log/10109", "log/10209"} <= khoa_v2 and not {k for k in khoa_v2 if k.startswith("arts/102") or k in {f"log/{j}" for j in dc["log_manh"]}}
                 and "run_g5" not in json.loads((goc / "v2" / "META.json").read_bytes()),
                 f"--thu (r6 K2): bien nhan chi cho pull_request, log chi job gom (KHONG log manh), META khong run_g5: {sorted(khoa_v2)}")
            o101 = json.loads((goc / "v2" / "oracle" / "101.json").read_bytes()) if "oracle/101" in khoa_v2 else {}
            bang([o101.get("oracle"), o101.get("phien_ban_oracle")] == [KHONG_DO_DUOC, 2] and "g4b" not in next(l for l in v2["luot"] if l["run_id"] == 102)
                 and sum(v2["bong"]["bo_dem_pull_request"]["loi_ich"].values()) == 2,
                 f"r7: --thu co --kho ghi oracle cho luot pull_request co dong bong; luot push KHONG vao G4 / bo dem: {o101} {v2['bong']['bo_dem_pull_request']}")
            bang(dc["thu"]() == 0 and dc["tinh"]("ra3") == 0 and dc["ket_qua"]("ra3")["G4"] == v2["G4"],
                 "r7: tiep tuc --thu tren anh chup v2 DA dong (ghi de tep thuong) roi --tinh: rc 0, G4 nhu cu")
            pat = os.environ.get("GITHUB_PAT")
            try:
                os.environ.pop("GITHUB_PAT", None)
                lenh_thu(argparse.Namespace(anh_chup=str(goc / "khong_co"), ra=str(goc / "v2x"), han_giay=1, so_luong=1, kho=None))
                thoat = None
            except SystemExit as e:
                thoat = str(e)
            finally:
                if pat is not None:
                    os.environ["GITHUB_PAT"] = pat
            bang(thoat == "thieu bien moi truong GITHUB_PAT", f"--thu that (khong `g`) thieu GITHUB_PAT phai dung NGAY, truoc moi viec: {thoat!r}")
            bang(rc_git == 5 and not (goc / "ra2" / "BASELINE_V2.json").exists(), f"--tinh ma muc §6 goi git thi phai TU CHOI rc 5, khong ghi ket qua v2: rc={rc_git}")
            bang(v2["meta"]["so_lan_thu_goi_git"] == 0 and "khong_do_duoc (--tinh v2" in (goc / "ra" / "nen" / "BAO_CAO.md").read_text(encoding="utf-8"),
                 "--tinh: 0 lan thu goi git; muc §6 cua bao cao nen ghi khong_do_duoc, khong phai du lieu cay song")
            bang([l["run_id"] for l in v2["luot"]] == [101, 102, 103] and v2["G4"]["G4b"]["du_hoan_tat"] == 1
                 and [l["g4b"] for l in v2["luot"] if l["run_id"] == 101] == ["du_hoan_tat"],
                 f"luot pull_request 101 co du tam bien nhan THAT => du_hoan_tat: {v2['G4']}")
        H, P = "e" * 40, "f" * 40
        manh = [{"ten": f"{JOB_MANH} (ubuntu-latest, {k})", "ket_luan": "success", "run_attempt": 1, "job_id": 10 + k, "head_sha": H} for k in range(SO_MANH_G5)]
        for su_kien, head, mong in (("push", H, BN_HOP_LE), ("push", P, BN_HONG)):
            l = dung_luot({"id": 7, "event": su_kien, "head_sha": head, "run_attempt": 1}, manh, None, None, tao_bien_nhan(H))
            bang(l["manh"]["bien_nhan"] == [mong] * SO_MANH_G5, f"{su_kien}: bien nhan khai head {H[:1]}, head luot {head[:1]} => {mong}: {l['manh']['ly_do']}")

    @kiem
    def chia_doi_trang_con_vang_khong_dung_trang_cha():
        """r8, WP1448-R6-F12 (lop new-guard-mutation-coverage): khoang CHIA DOI ma trang cha CON trong anh chup, trang con VANG (con_vang) hay
        chep du trang cha (con_du). `--tinh` (thanh vien luot) va `--thu` (khoa MANIFEST v2) KHONG duoc dung trang cha: ky vong DOC LAP o
        fixture `chia_doi_trang_con.json`; doi chung khong chia = `dau_cuoi` (101, 102, 103)."""
        fx = J("chia_doi_trang_con.json")
        with tempfile.TemporaryDirectory(prefix="wp1448_cd_") as d:
            goc = pathlib.Path(d)
            dc = dau_cuoi(goc)
            bang((dc["rc_thu"], dc["tinh"]("ra"), [l["run_id"] for l in dc["ket_qua"]("ra")["luot"]]) == (0, 0, [101, 102, 103]), "doi chung khong chia")
            goc_tep = {m["khoa"]: (goc / "ac" / m["duong_dan"]).read_bytes() for m in json.loads((goc / "ac" / "MANIFEST.json").read_bytes())["tep"]}
            for ten, bt in fx["bien_the"].items():
                tep, meta = dict(goc_tep), json.loads(goc_tep["META"])
                cha = next(k for k in meta["khoang_con"] if k["su_kien"] == "pull_request")
                cha["chia_doi"] = True
                meta["khoang_con"].append({**cha, **fx["khoang_con_them"]})
                tep["META"] = json.dumps(meta).encode()
                if bt["trang_con"]:
                    tep[f"list/ci/pull_request/{fx['khoang_con_them']['nhan']}/p1"] = tep[f"list/ci/pull_request/{cha['nhan']}/p1"]
                ghi_anh_chup(goc / ("ac_" + ten), tep)
                with contextlib.redirect_stdout(io.StringIO()):
                    rc_t = lenh_tinh(argparse.Namespace(anh_chup=str(goc / ("ac_" + ten)), ra=str(goc / ("t_" + ten)), anh_chup_v2=None, cohort_goc=None, kiem_ke=None))
                    rc_u = lenh_thu(argparse.Namespace(anh_chup=str(goc / ("ac_" + ten)), ra=str(goc / ("v_" + ten)), han_giay=60, so_luong=1,
                                                       kho=str(goc / "kho")), dc["g"])
                v = json.loads((goc / ("t_" + ten) / "BASELINE_V2.json").read_bytes())
                khoa = sorted(m["khoa"] for m in json.loads((goc / ("v_" + ten) / "MANIFEST.json").read_bytes())["tep"])
                bang((rc_t, [l["run_id"] for l in v["luot"]], v["G4"]["so_luot_pull_request"]) == (0, bt["tinh_run_ids"], bt["tinh_so_luot_pull_request"]),
                     f"{ten}: --tinh khong dung trang cha chia doi: rc {rc_t}, luot {[l['run_id'] for l in v['luot']]}, PR {v['G4']['so_luot_pull_request']}")
                bang((rc_u, khoa) == (0, bt["thu_khoa"]), f"{ten}: --thu khong thu bang chung tu trang cha chia doi: rc {rc_u}, khoa {khoa}")

    return ca


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
    for co in ("--ra", "--anh-chup", "--anh-chup-v2", "--cohort-goc", "--kho", "--mot-ca", "--kiem-ke"):
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


# Dot bien tren BAN SAO cua chinh tep nay: (ten, chuoi cu, chuoi moi, ca phai DO). Mot dot bien cho TUNG buoc cua phep quy G4b.
DOT_BIEN_TU_KIEM = (
    ('g4b_bo_buoc_0', '        return "huy_truoc_phan_loai", 0\n', '        pass\n', 'g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc'),
    ('g4b_bo_buoc_1', '        return "ngoai_mau_so", 1\n', '        pass\n', 'g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc'),
    ('g4b_bo_buoc_2', '    if chon is None:\n        return "thieu_bang_chung", 2\n', '', 'g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc'),
    ('g4b_bo_buoc_3', '        return "duong_nhanh_co_bang_chung", 3\n', '        pass\n', 'g4b_bon_fixture_bat_buoc_cua_dac_ta'),
    ('g4b_bo_buoc_4', '        return "bo_moi_co_bang_chung", 4\n', '        pass\n', 'g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc'),
    ('g4b_bo_buoc_5', '        return "du_hoan_tat", 5\n', '        pass\n', 'g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc'),
    ('g4b_bo_buoc_6', '        return "dich_hoan_tat", 6\n', '        pass\n', 'g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc'),
    ('g4b_bo_buoc_7', '        return "gom_hong", 7\n', '        pass\n', 'g4b_bon_fixture_bat_buoc_cua_dac_ta'),
    ('g4b_bo_buoc_8', '        return "dang_do", 8\n', '        pass\n', 'g4b_bon_fixture_bat_buoc_cua_dac_ta'),
    ('g4b_bo_buoc_9', '    if kl_gom == "success":\n        return "thieu_bang_chung", 9\n', '', 'g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc'),
    ('g4b_buoc_10_thanh_hoan_tat', '    return "thieu_bang_chung", 10\n', '    return "du_hoan_tat", 5\n', 'g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc'),
    ('g4b_tam_manh_cancelled_thanh_hoan_tat', '    if chon == "du" and du_bn and kl_gom == "success" and dau_khop:\n', '    if chon == "du":\n', 'g4b_bon_fixture_bat_buoc_cua_dac_ta'),
    ('g4b_gom_cancelled_van_hoan_tat', '    if chon == "du" and du_bn and kl_gom == "success" and dau_khop:\n', '    if chon == "du" and du_bn and dau_khop:\n', 'g4b_bon_fixture_bat_buoc_cua_dac_ta'),
    ('g4a_duong_nhanh_tinh_la_bo_moi', '{"bo_dn": "duong_nhanh_dang_chay", "bo_moi": "bo_moi"', '{"bo_dn": "bo_moi", "bo_moi": "bo_moi"', 'g4b_bon_fixture_bat_buoc_cua_dac_ta'),
    ('g4_mau_so_gom_buoc_0_1', '    mau = sum(n for b, n in theo_buoc.items() if int(b) >= 2)\n', '    mau = sum(theo_buoc.values())\n', 'g4_tong_hop_mau_so_va_tran'),
    ('bong_dem_loi_ich_bang_ton_du', '    return {"loi_ich": loi_ich, "ton_du": ton_du}\n', '    return {"loi_ich": ton_du, "ton_du": ton_du}\n', 'bong_hai_bo_dem_tach_rieng'),
    ('bong_ton_du_so_voi_cu', '    ton_du = int(che_do_chay != oracle)', '    ton_du = int(pl.get("cu") != oracle)', 'bong_hai_bo_dem_tach_rieng'),
    ('phep_do_khong_do_duoc_bien_mat', '        o["loai" if t["trang_thai"] == KHONG_DO_DUOC else "kad"] += 1\n', '        pass\n', 'dung_luot_chi_dong_attempt_hop_le_la_moi_nhat'),
    ('gom_dau_la_thanh_duong_nhanh', '            dau = "khong_do:" + (khop[0] if len(khop) == 1 else "la")\n', '            dau = "khong_do:duong_nhanh"\n', 'gom_dau_hieu_duong_theo_ly_do'),
    ('g4b_dau_khong_do_van_khop', '    dau_khop = dau in (None, f"gom_manh:{SO_MANH_G5}")', '    dau_khop = True', 'g4b_moi_fixture_dung_mot_loai_va_du_muoi_buoc'),
    ('bn_bo_da_kiem_khong_mang_che_do', '"che_do": "du" if du else None,', '"che_do": None,', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_chon_kiem_ke_bat_ke_van_tay', ' if x["sha256_test"] in cac_van_tay), None)\n', '), None)\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_artifact_vang_khong_thieu', '        elif art == "vang":\n            tt[k], ly[k] = BN_THIEU, "artifact_vang"\n', '', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_job_do_khong_thieu', '        elif art is None and (d is None or d.get("ket_luan") != "success"):\n            tt[k], ly[k] = BN_THIEU, "job_khong_success"\n', '', 'g4b_bon_fixture_bat_buoc_cua_dac_ta'),
    ('bn_job_success_la_bien_nhan', '            tt[k], ly[k] = KHONG_DO_DUOC, "artifact_het_han" if art == "het_han" else "noi_dung_chua_lay"\n', '            tt[k], ly[k] = BN_HOP_LE, "-"\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_job_sai_head_bo_qua', '        if d is not None and head_run is not None and d.get("head_sha") not in (None, head_run):\n            tt[k], ly[k] = BN_HONG, "job_mang_head_khac_luot"\n', '        if False:\n            pass\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('kk_bang_cua_cay_cho_dinh_danh_mong_doi', '(k, SO_MANH_G5, [t for t, _ in kk["dot_bien"]])', '(k, SO_MANH_G5)', 'kiem_ke_cua_run_that_khop_bien_nhan_that'),
    ('kk_nhan_kiem_ke_sai_hinh_dang', '                raise ValueError("sai hinh dang kiem ke")\n', '                pass\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('kk_nhan_hai_kiem_ke_cung_van_tay', '                raise ValueError("hai kiem ke cung mot van tay")\n', '                pass\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('kk_thu_muc_vang_im_lang', '        raise AnhChupHong(f"--kiem-ke {thu_muc}: khong phai thu muc")\n', '        return []\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
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
    ('tinh_head_luot_khong_theo_su_kien', 'bien_nhan_luot(manh, art, bien_nhan, head, hop, cmt, kiem_ke, run.get("event"))', 'bien_nhan_luot(manh, art, bien_nhan, head, hop, cmt, kiem_ke)', 'thu_roi_tinh_khong_goi_git_va_pull_request_du_hoan_tat'),
    ('tinh_chay_s6_tren_cay_song', '    g.phan_loai_s6 = s6_khong_cay_song\n', '', 'thu_roi_tinh_khong_goi_git_va_pull_request_du_hoan_tat'),
    ('tinh_khong_cam_git', '    with cam_git() as goi:\n        return _tinh(ns, goi)\n', '    return _tinh(ns, [])\n', 'thu_roi_tinh_khong_goi_git_va_pull_request_du_hoan_tat'),
    ('tinh_bo_qua_danh_sach_goi_git', '    if goi:                                                 # ma duoc nap', '    if False:                                               # ma duoc nap', 'thu_roi_tinh_khong_goi_git_va_pull_request_du_hoan_tat'),
    ('cam_git_ghi_ma_khong_chan', '                raise GitBiCam(f"--tinh khong duoc goi git: {goi[-1][:4]}")\n', '', 'thu_roi_tinh_khong_goi_git_va_pull_request_du_hoan_tat'),
    ('cam_git_khong_tra_popen', '    finally:\n        subprocess.Popen = goc\n', '    finally:\n        pass\n', 'thu_roi_tinh_khong_goi_git_va_pull_request_du_hoan_tat'),
    ('kk_dinh_danh_mong_doi_cua_manh_ke', '["_phan_manh"](k, SO_MANH_G5, [t for t, _ in kk["dot_bien"]])', '["_phan_manh"]((k + 1) % SO_MANH_G5, SO_MANH_G5, [t for t, _ in kk["dot_bien"]])', 'kiem_ke_cua_run_that_khop_bien_nhan_that'),
    ('anh_chup_bo_kiem_bam', '    if hong:\n        raise AnhChupHong', '    if False:\n        raise AnhChupHong', 'anh_chup_v2_kiem_manifest'),
    ('anh_chup_vang_manifest_im_lang', '        raise AnhChupHong(f"{ac}: khong co MANIFEST.json (anh chup chua dong)")\n', '        return None, {}\n', 'anh_chup_v2_kiem_manifest'),
    ('anh_chup_duong_dan_thoat_ra_ngoai', '        if ac not in p.parents or not p.is_file()', '        if not p.is_file()', 'anh_chup_v2_kiem_manifest'),
    ('bong_dem_nhan_cu_fail_close', '    cu_do = pl.get("cu_do") == DO_DUOC\n', '    cu_do = True\n', 'bong_hai_bo_dem_tach_rieng'),
    ('bong_dem_nhan_kiem_moi_khong_do_duoc', '    moi_do = pl.get("kiem_moi") != KHONG_DO_DUOC\n', '    moi_do = True\n', 'bong_hai_bo_dem_tach_rieng'),
    ('bn_hop_som_la_tham_quyen', '    phieu = [] if hop is None else [', '    if hop:\n        return h == hop\n    phieu = [] if hop is None else [', 'head_moi_bang_chung_co_san_phai_khop'),
    ('bn_phieu_dung_thang_phieu_sai', '    return False if False in phieu else (', '    return True if True in phieu else (False if False in phieu else None) or (', 'head_moi_bang_chung_co_san_phai_khop'),
    ('bn_vang_head_luot_la_mau_thuan', ' and RE_OID.fullmatch(head_run) is not None\n', ' or True\n', 'head_moi_bang_chung_co_san_phai_khop'),
    ('bn_job_vang_head_luot_la_mau_thuan', 'd is not None and head_run is not None and d.get', 'd is not None and d.get', 'head_moi_bang_chung_co_san_phai_khop'),
    ('bn_so_cha_sai_bo_qua_khi_vang_head', ' and (co_run or len(cha) != 2):', ' and co_run:', 'head_moi_bang_chung_co_san_phai_khop'),
    ('bn_dong_bong_khai_head_khac_bo_qua', '        hop = False      ', '        hop = hop        ', 'head_moi_bang_chung_co_san_phai_khop'),
    ('so_lan_khong_tran', ' and 1 <= x <= TRAN_ATTEMPT else None)', ' and 1 <= x else None)', 'dung_luot_chi_dong_attempt_hop_le_la_moi_nhat'),
    ('phan_loai_luot_nem_loi_dong_job', '    except (ValueError, TypeError, OverflowError, AttributeError) as e:', '    except ZeroDivisionError as e:', 'thu_roi_tinh_khong_goi_git_va_pull_request_du_hoan_tat'),
    ('g5_cat_bao_do_duoc', '"g5_thoi_gian": {"ly_do": LY_DO_G5_CAT, "trang_thai": KHONG_DO_DUOC}', '"g5_thoi_gian": {"ly_do": LY_DO_G5_CAT, "trang_thai": DO_DUOC}', 'g5_thoi_gian_cat_luon_khong_do_duoc'),
    ('g5_cat_ly_do_khong_neu_pr1b', ' thuoc packet ke nhiem PR1b - G5 timing collector redesign"\n', ' thuoc packet ke nhiem sau"\n', 'g5_thoi_gian_cat_luon_khong_do_duoc'),
    ('g5_cat_them_truong_chung_nhan', '"g5_thoi_gian": {"ly_do": LY_DO_G5_CAT, "trang_thai": KHONG_DO_DUOC}', '"g5_thoi_gian": {"ly_do": LY_DO_G5_CAT, "trang_thai": KHONG_DO_DUOC, "dat_95_phan_tram": True}', 'g5_thoi_gian_cat_luon_khong_do_duoc'),
    ('g5_cat_phu_thuoc_anh_chup_cu', '"g5_thoi_gian": {"ly_do": LY_DO_G5_CAT, "trang_thai": KHONG_DO_DUOC}', '"g5_thoi_gian": {"ly_do": LY_DO_G5_CAT, "trang_thai": DO_DUOC if doc2 and json.loads(doc2("META") or b"{}").get("run_g5") else KHONG_DO_DUOC}', 'g5_thoi_gian_cat_luon_khong_do_duoc'),
    ('g5_cat_chung_nhan_o_goc', '"g5_thoi_gian": {"ly_do": LY_DO_G5_CAT, "trang_thai": KHONG_DO_DUOC},\n', '"g5_thoi_gian": {"ly_do": LY_DO_G5_CAT, "trang_thai": KHONG_DO_DUOC}, "ti_le_du": 1.0,\n', 'g5_thoi_gian_cat_luon_khong_do_duoc'),
    ('g5_cat_chung_nhan_long_sau', '    v2 = {"meta": {"packet": "wp1448",', '    v2 = {"meta": {"do_day_du": {"trang_thai": DO_DUOC}, "packet": "wp1448",', 'g5_thoi_gian_cat_luon_khong_do_duoc'),
    ('g5_cat_bao_cao_bo_ly_do', '\\n\\n{g5[\'trang_thai\']}: {g5[\'ly_do\']}\\n")', '\\n\\n{g5[\'trang_thai\']}\\n")', 'g5_thoi_gian_cat_luon_khong_do_duoc'),
    ('g5_cat_nhan_lai_run_g5', '"--cohort-goc", "--kho", "--mot-ca"', '"--cohort-goc", "--run-g5", "--kho", "--mot-ca"', 'g5_thoi_gian_cat_luon_khong_do_duoc'),
    ('g5_cat_bo_qua_doi_so_la', '    ns = ap.parse_args()\n', '    ns = ap.parse_known_args()[0]\n', 'g5_thoi_gian_cat_luon_khong_do_duoc'),
    ('g5_cat_khoi_phuc_api', '\nLY_DO_G5_CAT = ', '\nRE_G5 = re.compile(TT + r"G5_THOI_GIAN (\\{.*\\})\\s*$")\nLY_DO_G5_CAT = ', 'g5_thoi_gian_cat_luon_khong_do_duoc'),
    ('tai_lap_bo_khoa_m3', '    ("M3.bang[ops/ci_provenance_test.py]", ("M3", "bang", "ops/ci_provenance_test.py")),\n', '', 'tai_lap_khoa_ba_trang_thai'),
    ('g4b_buoc_0_vang_bang_chung_la_huy', '    if l.get("chuan_bi") in hong and l.get("lan_cu")', '    if l.get("chuan_bi") != "success" and l.get("lan_cu")', 'g4_vang_bang_chung_khong_ra_khoi_mau_so'),
    ('tinh_bo_luot_vang_bang_chung', '        if lu is None:                                      # r6 F8', '        if lu is None:\n            continue\n        if lu is None:                                      # r6 F8', 'g4_vang_bang_chung_khong_ra_khoi_mau_so'),
    ('tinh_luot_vang_bang_chung_khong_neu_ly_do', '            l["bang_chung_luot"] = kdd(ly)\n', '', 'g4_vang_bang_chung_khong_ra_khoi_mau_so'),
    ('dung_luot_dong_att_sai_van_nhan', 'if (a := att_dong(d)) is not None and a <= tran)', 'if (a := att_dong(d) or 1) is not None and a <= tran)', 'dung_luot_chi_dong_attempt_hop_le_la_moi_nhat'),
    ('dung_luot_nhan_dong_attempt_sau_luot', 'if (a := att_dong(d)) is not None and a <= tran)', 'if (a := att_dong(d)) is not None)', 'dung_luot_chi_dong_attempt_hop_le_la_moi_nhat'),
    ('dung_luot_luot_att_sai_van_nhan_dong', '    tran = so_att or 0\n', '    tran = so_att or TRAN_ATTEMPT\n', 'dung_luot_chi_dong_attempt_hop_le_la_moi_nhat'),
    ('att_dong_vang_la_1', '    return None if x is None else so_lan(x)\n', '    return so_lan(x)\n', 'dung_luot_chi_dong_attempt_hop_le_la_moi_nhat'),
    ('so_lan_nhan_khong_phai_int', ' (x if type(x) is int and 1 <= x', ' (x if isinstance(x, (int, float)) and 1 <= x', 'dung_luot_chi_dong_attempt_hop_le_la_moi_nhat'),
    ('phan_loai_luot_att_sai_thanh_1', '    n = so_lan(r.get("run_attempt"))\n', '    n = so_lan(r.get("run_attempt")) or 1\n', 'thu_roi_tinh_khong_goi_git_va_pull_request_du_hoan_tat'),
    ('phan_loai_luot_att_khong_phai_object', '        tao[k] = d.get("created_at") if isinstance(d, dict) else None\n', '        tao[k] = d.get("created_at") if d is not None else None\n', 'thu_roi_tinh_khong_goi_git_va_pull_request_du_hoan_tat'),
    ('bn_tu_khai_nhan_ban_ghi_khong_phai_mang', '        if isinstance(bg, list) and len(bg) > 2 and isinstance(bg[1], str):\n', '        if True:\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_tu_khai_ca_khong_kiem_hinh_dang', ' and bg[0] == "do" and len(bg) == 4 and isinstance(bg[3], dict):\n', ' and bg[0] == "do":\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_hop_dong_loi_nhan_thanh_dat', '            return str(ly)[:200]\n', '            return None\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_hong_cau_truc_thanh_khong_do', '        return BN_HONG, "cau_truc: " + than, None\n', '        return KHONG_DO_DUOC, "cau_truc: " + than, None\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bn_cha_khong_phai_danh_sach', '    if isinstance(cha, list) and (co_run or len(cha) != 2):', '    if cha is not None and (co_run or len(cha) != 2):', 'head_moi_bang_chung_co_san_phai_khop'),
    ('cam_git_chan_moi_tien_trinh', '            if dau and pathlib.PurePath(dau[0]).name.lower() in ("git", "git.exe"):\n', '            if dau:\n', 'thu_roi_tinh_khong_goi_git_va_pull_request_du_hoan_tat'),
    ('thu_khong_doi_token', '    if g is None and not os.environ.get("GITHUB_PAT"):\n', '    if False:\n', 'thu_roi_tinh_khong_goi_git_va_pull_request_du_hoan_tat'),
    ('thu_bien_nhan_moi_su_kien', '        if kh["bien_nhan"]:\n', '        if True:\n', 'thu_roi_tinh_khong_goi_git_va_pull_request_du_hoan_tat'),
    ('thu_tai_log_manh', '           if (ten or "").startswith(JOB_GOM + " (ubuntu-latest") and d.get("conclusion") not in ("skipped", None)]\n', '           if ((ten or "").startswith(JOB_GOM + " (ubuntu-latest") or chi_so_manh(ten) is not None) and d.get("conclusion") not in ("skipped", None)]\n', 'thu_roi_tinh_khong_goi_git_va_pull_request_du_hoan_tat'),
    ('ghi_tinh_baseline_v2_ghi_thang', '        g.ghi_tep(ra, "BASELINE_V2.json", b)\n', '        (ra / "BASELINE_V2.json").write_bytes(b)\n', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_tinh_bao_cao_v2_ghi_thang', '        g.ghi_tep(ra, "BAO_CAO_V2.md", bao_cao(v2).encode("utf-8"))\n', '        (ra / "BAO_CAO_V2.md").write_bytes(bao_cao(v2).encode("utf-8"))\n', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_xuat_kiem_ke_ghi_thang', '        g.ghi_tep(ra, kk["sha256_test"] + ".json", xuat_json(kk))\n', '        (ra / (kk["sha256_test"] + ".json")).write_bytes(xuat_json(kk))\n', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_tinh_bo_ke_hoach', '        kiem_ke_hoach_ghi(ra, DICH_TINH, (ac, ns.anh_chup_v2, ns.kiem_ke, ns.cohort_goc))\n', '        pass\n', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_tinh_nhan_nen_symlink', 'DICH_TINH = ("nen/BASELINE.json", "nen/COHORT.json", "nen/BAO_CAO.md", ', 'DICH_TINH = (', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_ke_hoach_bo_kiem_symlink', '            if os.path.islink(p):\n', '            if False:\n', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_ke_hoach_chi_kiem_la', '        p, ph = ra, pathlib.PurePosixPath(rel).parts\n', '        p, ph = ra / pathlib.PurePosixPath(rel).parent, (pathlib.PurePosixPath(rel).name,)\n', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_ke_hoach_bo_kiem_sai_loai', '            if os.path.lexists(p) and not (p.is_file() if i == len(ph) - 1 else p.is_dir()):\n', '            if False:\n', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_ra_la_tep_van_nhan', '    if os.path.lexists(ra) and not ra.is_dir():\n', '    if False:\n', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_bo_chong_lan_dau_vao', '        if p == ra or p in ra.parents or ra in p.parents:\n', '        if False:\n', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_chong_lan_bo_chieu_ra_chua_dau_vao', ' or p in ra.parents or ra in p.parents:\n', ' or p in ra.parents:\n', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_chong_lan_bo_chieu_ra_trong_dau_vao', '        if p == ra or p in ra.parents or ra', '        if p == ra or ra', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_bo_kiem_root', '    for q in (ROOT, *(', '    for q in (*(), *(', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_bo_goc_git_cua_nguon', '        for r in {q, goc_git(q)} - {None}:\n', '        for r in {q}:\n', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_xuat_kiem_ke_bo_nguon_kho', '        kiem_ke_hoach_ghi(ra, (), nguon=(ns.kho,))\n', '        kiem_ke_hoach_ghi(ra, ())\n', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_thu_kiem_sau_khi_dung_writer', '    try:                                                     # r7 F11: anh chup v2 RIENG, ngoai kho / --kho, kiem TRUOC khi dung bo ghi\n        kiem_ke_hoach_ghi(pathlib.Path(ns.ra).resolve(), DICH_THU, (ac,), (ns.kho,))\n    except GhiBiChan as e:\n        raise SystemExit(f"TU CHOI GHI: {e}") from e\n    try:\n        doc, _ = doc_anh_chup(ac)\n    except AnhChupHong as e:\n        raise SystemExit(f"anh chup #1434 khong dung duoc: {e}") from e\n    meta = json.loads((ac / "META.json").read_bytes())\n    t = g.Thu(ns.ra, ns.han_giay, ns.so_luong)\n', '    try:\n        doc, _ = doc_anh_chup(ac)\n    except AnhChupHong as e:\n        raise SystemExit(f"anh chup #1434 khong dung duoc: {e}") from e\n    meta = json.loads((ac / "META.json").read_bytes())\n    t = g.Thu(ns.ra, ns.han_giay, ns.so_luong)\n    try:                                                     # r7 F11: anh chup v2 RIENG, ngoai kho / --kho, kiem TRUOC khi dung bo ghi\n        kiem_ke_hoach_ghi(pathlib.Path(ns.ra).resolve(), DICH_THU, (ac,), (ns.kho,))\n    except GhiBiChan as e:\n        raise SystemExit(f"TU CHOI GHI: {e}") from e\n', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_thu_bo_nguon_kho', ' DICH_THU, (ac,), (ns.kho,))\n', ' DICH_THU, (ac,), ())\n', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_thu_bo_dau_vao_anh_chup', ' DICH_THU, (ac,), (ns.kho,))\n', ' DICH_THU, (), (ns.kho,))\n', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_tinh_bo_dau_vao_v2', '(ac, ns.anh_chup_v2, ns.kiem_ke, ns.cohort_goc)', '(ac, ns.kiem_ke, ns.cohort_goc)', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_tinh_bo_dau_vao_kiem_ke', '(ac, ns.anh_chup_v2, ns.kiem_ke, ns.cohort_goc)', '(ac, ns.anh_chup_v2, ns.cohort_goc)', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('ghi_tinh_bo_dau_vao_cohort', '(ac, ns.anh_chup_v2, ns.kiem_ke, ns.cohort_goc)', '(ac, ns.anh_chup_v2, ns.kiem_ke)', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    ('manifest_gom_truoc_khi_kiem', '    for m in tep:\n        dd = m.get("duong_dan")\n', '    for m in {x["khoa"]: x for x in tep}.values():\n        dd = m.get("duong_dan")\n', 'manifest_moi_muc_tho_truoc_khi_gom'),
    ('manifest_lap_mau_thuan_lay_sau', '        if theo_khoa.setdefault(m["khoa"], m) != m:\n            hong.append(m["khoa"] + " (lap mau thuan)")\n', '        theo_khoa[m["khoa"]] = m\n', 'manifest_moi_muc_tho_truoc_khi_gom'),
    ('manifest_khoa_json_lap_im_lang', '        tep = json_mot_nghia(f.read_bytes())["tep"]\n', '        tep = json.loads(f.read_bytes())["tep"]\n', 'manifest_moi_muc_tho_truoc_khi_gom'),
    ('json_mot_nghia_nhan_khoa_lap', '            raise ValueError("object JSON co khoa lap")\n', '            pass\n', 'manifest_moi_muc_tho_truoc_khi_gom'),
    ('manifest_bo_kiem_hinh_dang_muc', '        if not isinstance(tep, list) or not all(isinstance(m, dict) and isinstance(m.get("khoa"), str) for m in tep):\n', '        if False:\n', 'manifest_moi_muc_tho_truoc_khi_gom'),
    ('manifest_duong_dan_khong_kiem_kieu', '            p = (ac / dd).resolve() if isinstance(dd, str) else ac\n', '            p = (ac / dd).resolve()\n', 'manifest_moi_muc_tho_truoc_khi_gom'),
    ('tinh_anh_chup_1434_gom_khong_kiem', '        doc, _ = doc_anh_chup(ac)\n    except AnhChupHong as e:\n        print("ANH CHUP / KIEM KE HONG:"', '        doc = lambda k, _m={x["khoa"]: x for x in json.loads((ac / "MANIFEST.json").read_bytes())["tep"]}: (ac / _m[k]["duong_dan"]).read_bytes() if k in _m and _m[k].get("duong_dan") else None\n    except AnhChupHong as e:\n        print("ANH CHUP / KIEM KE HONG:"', 'manifest_moi_muc_tho_truoc_khi_gom'),
    ('kk_khoa_json_lap_im_lang', '            kk = json_mot_nghia(tep.read_bytes())\n', '            kk = json.loads(tep.read_bytes())\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('bong_khoa_lap_lay_sau', '        if d.setdefault(k, v) != v:\n            return None\n', '        d[k] = v\n', 'bong_hai_bo_dem_tach_rieng'),
    ('bong_khoa_lap_van_doc', '            if d is None:\n                kq[', '            if False:\n                kq[', 'bong_hai_bo_dem_tach_rieng'),
    ('bn_khai_moi_tep_ke_ca_hong', '            if vt:\n', '            if True:\n', 'bien_nhan_ba_tang_moi_tep_mot_minh'),
    ('tinh_oracle_ba_oid_duoc_dung', '                if b and json.loads(b).get("phien_ban_oracle") != 2:', '                if False:', 'tinh_dau_cuoi_oracle_v2_buoc_gate_artifact_cohort'),
    ('tinh_oracle_v2_bi_bo', '                if b and json.loads(b).get("phien_ban_oracle") != 2:', '                if True:', 'tinh_dau_cuoi_oracle_v2_buoc_gate_artifact_cohort'),
    ('tinh_bo_oracle_khi_co_v2', '            if doc2:\n', '            if False:\n', 'tinh_dau_cuoi_oracle_v2_buoc_gate_artifact_cohort'),
    ('tinh_doc_oracle_khi_khong_v2', '            if doc2:\n', '            if True:\n', 'tinh_dau_cuoi_oracle_v2_buoc_gate_artifact_cohort'),
    ('tinh_bo_buoc_gate', '                if m["loai_dong"] == g.THUC_THI and m["ten_goc"] in JOB_BUOC_V2:\n', '                if False:\n', 'tinh_dau_cuoi_oracle_v2_buoc_gate_artifact_cohort'),
    ('tinh_buoc_moi_job', '                if m["loai_dong"] == g.THUC_THI and m["ten_goc"] in JOB_BUOC_V2:\n', '                if True:\n', 'tinh_dau_cuoi_oracle_v2_buoc_gate_artifact_cohort'),
    ('tinh_bo_cohort_goc', '    if ns.cohort_goc:\n', '    if False:\n', 'tinh_dau_cuoi_oracle_v2_buoc_gate_artifact_cohort'),
    ('tinh_khong_do_khong_ly_do', '        if ly:\n            khong_do.append(', '        if True:\n            khong_do.append(', 'tinh_dau_cuoi_oracle_v2_buoc_gate_artifact_cohort'),
    ('tinh_bo_danh_sach_artifact', '            if doc2 and f"arts/{rid}/p1" in theo_khoa2:\n', '            if False:\n', 'tinh_dau_cuoi_oracle_v2_buoc_gate_artifact_cohort'),
    ('tinh_bien_nhan_vang_van_ghi', '                if nd is not None:\n                    bn[k] = nd\n', '                if True:\n                    bn[k] = nd\n', 'tinh_dau_cuoi_oracle_v2_buoc_gate_artifact_cohort'),
    ('tinh_g4_moi_su_kien', '        if l["su_kien"] == "pull_request":\n            oracle = None\n', '        if True:\n            oracle = None\n', 'thu_roi_tinh_khong_goi_git_va_pull_request_du_hoan_tat'),
    ('tinh_bo_packet_loop', '    if doc2 and "list/pl/p1" in theo_khoa2:\n', '    if False:\n', 'tinh_dau_cuoi_oracle_v2_buoc_gate_artifact_cohort'),
    ('tinh_packet_loop_khong_v2', '    if doc2 and "list/pl/p1" in theo_khoa2:\n', '    if True:\n', 'tinh_dau_cuoi_oracle_v2_buoc_gate_artifact_cohort'),
    ('tinh_v2_vang_van_doc', '        if ns.anh_chup_v2:\n', '        if True:\n', 'tinh_dau_cuoi_oracle_v2_buoc_gate_artifact_cohort'),
    ('luot_bo_danh_sach_artifact', '    if artifact is not None:\n', '    if False:\n', 'tinh_dau_cuoi_oracle_v2_buoc_gate_artifact_cohort'),
    ('luot_ten_artifact_khong_doc', '            if isinstance(ten, str) and ten.startswith(TEN_ART_MANH) and ten[len(TEN_ART_MANH):].isdigit():\n', '            if False:\n', 'tinh_dau_cuoi_oracle_v2_buoc_gate_artifact_cohort'),
    ('thu_bo_oracle_khi_co_kho', '        if pl:\n            oracle.append(', '        if False:\n            oracle.append(', 'thu_roi_tinh_khong_goi_git_va_pull_request_du_hoan_tat'),
    ('oracle_bo_kiem_dang_oid', '    if not all(isinstance(x, str) and RE_OID.fullmatch(x) for x in (goc_su_kien, dau, hop)):\n', '    if False:\n', 'oracle_moi_chot_fail_close_git_gia'),
    ('oracle_rev_list_khong_doi_chieu_hop', '        if not k or k.group(1).decode("ascii") != hop:\n', '        if not k:\n', 'oracle_moi_chot_fail_close_git_gia'),
    ('oracle_nhan_nhieu_merge_base', '        if rc != 0 or not re.fullmatch(rb"[0-9a-f]{40}\\n", mb):\n', '        if rc != 0:\n', 'oracle_moi_chot_fail_close_git_gia'),
    ('oracle_nhan_merge_tree_hong', '        if rc != 0 or not re.fullmatch(rb"[0-9a-f]{40}\\n", cay):\n', '        if rc != 0:\n', 'oracle_moi_chot_fail_close_git_gia'),
    ('oracle_nhan_diff_khong_nul', '            if rc != 0 or muc[-1] != "" or len(muc) % 2 != 1:\n', '            if rc != 0:\n', 'oracle_moi_chot_fail_close_git_gia'),
    ('oracle_nhan_ban_ghi_la', '        if not m:\n            return KHONG_DO_DUOC\n        cu, moi, tt', '        if False:\n            return KHONG_DO_DUOC\n        cu, moi, tt', 'oracle_moi_chot_fail_close_git_gia'),
    ('oracle_bo_ma_cap_nong', '        if len(tp) == 3 and tp[2].lower().endswith(DUOI_MA_CAP_NONG):\n', '        if False:\n', 'oracle_moi_chot_fail_close_git_gia'),
    ('oracle_bo_mode_thuc_thi', '        if moi in MODE_VE_DAY_DU or (cu != "000000" and moi != "000000" and cu != moi):\n', '        if False:\n', 'oracle_moi_chot_fail_close_git_gia'),
    ('oracle_bo_sua_dac_ta', '        if duong.startswith("ops/specs/") and tt in ("M", "D", "T"):\n', '        if False:\n', 'oracle_moi_chot_fail_close_git_gia'),
    # r8 (WP1448-R6-F12): HAI chot chia doi (dong `if` giong het nhau -> neo kem dong dung truoc de MOI dot bien sua DUNG MOT cho)
    ('tinh_dung_trang_cha_chia_doi', 'errors="replace")\n\n    ds_ci = []\n    for k in meta["khoang_con"]:\n        if not k.get("chia_doi"):\n',
     'errors="replace")\n\n    ds_ci = []\n    for k in meta["khoang_con"]:\n        if True:\n', 'chia_doi_trang_con_vang_khong_dung_trang_cha'),
    ('thu_dung_trang_cha_chia_doi', '"sha_master")}}))\n    ds_ci = []\n    for k in meta["khoang_con"]:\n        if not k.get("chia_doi"):\n',
     '"sha_master")}}))\n    ds_ci = []\n    for k in meta["khoang_con"]:\n        if True:\n', 'chia_doi_trang_con_vang_khong_dung_trang_cha'),
    ('ghi_nguon_bo_ra_chua_cay_nguon', ' or ra in r.parents:      # r8:', ':      # r8:', 'ghi_co_gioi_han_moi_dich_cua_bo_thu'),
    # r8: ba ve cua chot chon artifact o lenh_thu (truoc la "tuong duong" khong fixture) + chot bo qua luot jobs khong du
    ('thu_artifact_bo_kiem_ten', '            if ten.startswith(TEN_ART_MANH) and ten[len(', '            if ten[len(', 'thu_roi_tinh_khong_goi_git_va_pull_request_du_hoan_tat'),
    ('thu_artifact_lay_het_han', ' and not a.get("expired"):\n                viec.append(', ':\n                viec.append(', 'thu_roi_tinh_khong_goi_git_va_pull_request_du_hoan_tat'),
    ('thu_artifact_duoi_khong_so', ' and ten[len(TEN_ART_MANH):].isdigit() and not a.get("expired"):\n', ' and not a.get("expired"):\n',
     'thu_roi_tinh_khong_goi_git_va_pull_request_du_hoan_tat'),
    ('thu_lay_bang_chung_khi_jobs_khong_du', '        dong, du, _, _ = g.chon_chuoi_trang(doc, f"jobs/{rid}")\n        if not du:\n            continue\n',
     '        dong, du, _, _ = g.chon_chuoi_trang(doc, f"jobs/{rid}")\n', 'chia_doi_trang_con_vang_khong_dung_trang_cha'),
)


if __name__ == "__main__":
    sys.exit(main())
