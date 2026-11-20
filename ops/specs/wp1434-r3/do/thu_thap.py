#!/usr/bin/env python3
"""wp1434 r3 — do nen mutation testing, CHI DOC (dac ta ops/specs/wp1434-r3/SPEC.md).

Ba che do, khong che do nao chay bo test hay bo dot bien nao:
  --thu --ra <anh chup>                 GitHub REST GET -> thu muc anh chup NGOAI kho (+ META.json, MANIFEST.json)
  --tinh --anh-chup <anh chup> --ra <thu muc>   thuan offline -> COHORT.json, BASELINE.json, BAO_CAO.md
  --tu-kiem                             ca tu kiem tren fixtures/, khong mang

Token chi doc tu bien moi truong GITHUB_PAT, chi gui toi api.github.com; khong in, khong luu token, header xac thuc
hay URL tai co chu ky (log/artifact chuyen huong sang URL co chu ky: chi luu URL API khong chu ky).
"""
import argparse
import datetime
import hashlib
import io
import json
import math
import os
import pathlib
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import threading
import time
import zipfile

DAY = pathlib.Path(__file__).resolve().parent
ROOT = DAY.parents[3]
KHO = "ducthangho/tra-luat"
API = "https://api.github.com/repos/" + KHO + "/"
WF_DU, WF_CI = "ci-dot-bien-du.yml", "ci.yml"
SPEC_SHA256 = "0247845e6dd643388f7219781ebff553b605e59d731481d10a024e80ae8232b4"
DO_DUOC, KHONG_AP_DUNG, KHONG_DO_DUOC = "do_duoc", "khong_ap_dung", "khong_do_duoc"
BO_QUA, MANG_SANG, THUC_THI, KHONG_PHAN_LOAI = "bo_qua", "mang_sang", "thuc_thi", "khong_phan_loai_duoc"
JOB_BUOC = ("gate-cong-cu", "gate-nhanh-", "gate-registry", "gate-packet-loop")   # M2: nhom job phai bao tung buoc
TIEN_TO_BUOC_REGISTRY = "test registry"
NGAY_COHORT = 30


# ───────────────────────── ham thuan (dung chung cho --thu, --tinh, --tu-kiem) ─────────────────────────

def gio(s):
    """ISO-8601 UTC cua API -> datetime; khong doc duoc -> None (KHONG doan)."""
    if not isinstance(s, str) or not s:
        return None
    try:
        d = datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=datetime.timezone.utc)


def iso(d):
    return d.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def gt(v, nguon=None):
    """Gia tri do duoc. 0 la do_duoc voi gia tri 0 (dac ta §5)."""
    r = {"gia_tri": v, "trang_thai": DO_DUOC}
    if nguon is not None:
        r["nguon"] = nguon
    return r


def kdd(ly_do, nguon=None):
    r = {"gia_tri": None, "trang_thai": KHONG_DO_DUOC, "ly_do": ly_do}
    if nguon is not None:
        r["nguon"] = nguon
    return r


def kad(ly_do, nguon=None):
    r = {"gia_tri": None, "trang_thai": KHONG_AP_DUNG, "ly_do": ly_do}
    if nguon is not None:
        r["nguon"] = nguon
    return r


def khoang_giay(bat_dau, ket_thuc, ten=("started_at", "completed_at")):
    """ket_thuc - bat_dau (giay). Thieu moc -> khong_do_duoc; dao -> khong_do_duoc (KHONG kep ve 0); 0 -> do_duoc 0."""
    a, b = gio(bat_dau), gio(ket_thuc)
    if a is None:
        return kdd("thieu_" + ten[0])
    if b is None:
        return kdd("thieu_" + ten[1])
    d = (b - a).total_seconds()
    if d < 0:
        return kdd(f"thoi_gian_dao ({ten[1]} < {ten[0]})")
    return gt(int(d) if d == int(d) else round(d, 3))


def thoi_luong_buoc(buoc):
    """Buoc `skipped` -> khong_ap_dung; con lai theo `khoang_giay`."""
    if buoc.get("conclusion") == "skipped":
        return kad("buoc skipped")
    return khoang_giay(buoc.get("started_at"), buoc.get("completed_at"))


def phan_loai_dong(dong, tao_attempt, job_id_truoc):
    """Dac ta §3, THEO THU TU: (a) skipped -> bo_qua; (b) mang_sang; (c) con lai -> thuc_thi.
    `tao_attempt` = created_at cua attempt chua dong (None neu khong lay duoc); `job_id_truoc` = tap job_id cua cac attempt truoc."""
    if dong.get("conclusion") == "skipped":
        return BO_QUA
    if dong.get("id") in job_id_truoc:
        return MANG_SANG
    bd, ta = gio(dong.get("started_at")), gio(tao_attempt)
    if bd is not None and ta is not None and bd < ta:
        return MANG_SANG
    if ta is None and int(dong.get("run_attempt") or 1) > 1:
        return KHONG_PHAN_LOAI          # attempt > 1 ma khong co created_at cua attempt: khong tach duoc mang_sang
    return THUC_THI


def ten_goc(ten):
    return re.sub(r"\s*\(.*\)\s*$", "", ten or "")


def nen_cua(dong):
    nhan = dong.get("labels") or []
    return "+".join(sorted(str(x) for x in nhan)) if nhan else "khong_ro"


def tinh_luot(run, tao_attempt, dong_job):
    """Mot luot (moi attempt 1..run_attempt). `tao_attempt`: {n: created_at | None}. Tra dict co ba con so §3 + cac dong da phan loai."""
    so_att = int(run.get("run_attempt") or 1)
    theo_att = {}
    for d in dong_job:
        theo_att.setdefault(int(d.get("run_attempt") or 1), []).append(d)
    ngoai = sum(len(v) for n, v in theo_att.items() if n > so_att)          # attempt sinh sau luc chot cohort: khong tinh
    da_thay, dong_ra, dem = set(), [], {BO_QUA: 0, MANG_SANG: 0, THUC_THI: 0, KHONG_PHAN_LOAI: 0}
    tong, loai, hong_truoc = 0, 0, 0
    cuoi_max = None
    for n in range(1, so_att + 1):
        ds = sorted(theo_att.get(n, []), key=lambda d: (d.get("id") or 0))
        for d in ds:
            lo = phan_loai_dong(d, tao_attempt.get(n), da_thay)
            dem[lo] += 1
            muc = {"job_id": d.get("id"), "run_attempt": n, "ten": d.get("name"), "ten_goc": ten_goc(d.get("name")),
                   "nen": nen_cua(d), "ket_luan": d.get("conclusion"), "loai_dong": lo, "_tho": d}
            if lo == THUC_THI:
                muc["giay"] = khoang_giay(d.get("started_at"), d.get("completed_at"))
                muc["giay_cho"] = khoang_giay(d.get("created_at"), d.get("started_at"), ("created_at", "started_at"))
                if muc["giay"]["trang_thai"] == DO_DUOC:
                    tong += muc["giay"]["gia_tri"]
                    if n == so_att:
                        kt = gio(d.get("completed_at"))
                        cuoi_max = kt if cuoi_max is None or kt > cuoi_max else cuoi_max
                else:
                    loai += 1
                if n < so_att and d.get("conclusion") == "failure":
                    hong_truoc += 1
            elif lo == BO_QUA:
                muc["giay"] = kad("job skipped")
                muc["giay_cho"] = kad("job skipped")
            elif lo == MANG_SANG:
                muc["giay"] = kad("mang_sang tu attempt truoc (da tinh o attempt goc)")
                muc["giay_cho"] = kad("mang_sang tu attempt truoc")
            else:
                muc["giay"] = kdd("khong phan loai duoc dong: thieu created_at cua attempt")
                muc["giay_cho"] = kdd("khong phan loai duoc dong: thieu created_at cua attempt")
                loai += 1
            dong_ra.append(muc)
        da_thay |= {d.get("id") for d in ds}
    so_tt_hop_le = dem[THUC_THI] + dem[KHONG_PHAN_LOAI] - loai
    if dem[THUC_THI] + dem[KHONG_PHAN_LOAI] == 0:
        giay_tt = kad("khong co dong thuc_thi nao")
    elif so_tt_hop_le == 0:
        giay_tt = kdd("khong dong thuc_thi nao co thoi luong hop le")
    else:
        giay_tt = gt(tong)
    giay_tt["so_dong_tinh"], giay_tt["so_dong_loai"] = so_tt_hop_le, loai
    tao1 = gio(tao_attempt.get(1))
    if cuoi_max is None:
        dau_cuoi = kdd("attempt cuoi khong co dong thuc_thi hop le")
    elif tao1 is None:
        dau_cuoi = kdd("thieu created_at cua attempt 1")
    elif (cuoi_max - tao1).total_seconds() < 0:
        dau_cuoi = kdd("thoi_gian_dao (max completed_at < created_at attempt 1)")
    else:
        dau_cuoi = gt(int((cuoi_max - tao1).total_seconds()))
    cho = [m["giay_cho"]["gia_tri"] for m in dong_ra if m["loai_dong"] == THUC_THI and m["giay_cho"]["trang_thai"] == DO_DUOC]
    cho_loai = sum(1 for m in dong_ra if m["loai_dong"] == THUC_THI and m["giay_cho"]["trang_thai"] != DO_DUOC)
    return {"run_id": run.get("id"), "so_attempt": so_att, "co_rerun": so_att > 1, "su_kien": run.get("event"),
            "ket_luan": run.get("conclusion"), "head_sha": run.get("head_sha"), "created_at": run.get("created_at"),
            "updated_at_tham_khao": run.get("updated_at"),
            "giay_thuc_thi": giay_tt, "dau_cuoi_suy_ra_tu_job": dau_cuoi,
            "giay_cho": thong_ke(cho, cho_loai), "so_dong": dict(dem), "so_dong_attempt_ngoai_cohort": ngoai,
            "so_job_hong_o_attempt_truoc": hong_truoc, "dong": dong_ra}


def thong_ke(gia_tri, so_loai=0):
    """Chi tinh tren phan do_duoc. trung_vi = statistics.median; p90 = hang gan nhat: sorted[ceil(0.9*n)-1]."""
    v = sorted(gia_tri)
    if not v:
        return {"n": 0, "so_loai": so_loai, "trang_thai": KHONG_DO_DUOC if so_loai else KHONG_AP_DUNG,
                "ly_do": "khong co gia tri do_duoc nao"}
    lam = lambda x: int(x) if float(x) == int(x) else round(float(x), 3)
    return {"n": len(v), "so_loai": so_loai, "trang_thai": DO_DUOC, "tong": lam(sum(v)), "nho_nhat": lam(v[0]),
            "trung_vi": lam(statistics.median(v)), "p90": lam(v[math.ceil(0.9 * len(v)) - 1]), "lon_nhat": lam(v[-1])}


def loc_cohort(ds_run, workflow, t0, t1):
    """Dac ta §2. Tra (trong cohort, bi loai kem ly do). Khoang DONG [t0, t1]; ci-dot-bien-du khong co can duoi."""
    trong, loai = [], []
    a, b = gio(t0), gio(t1)
    for r in ds_run:
        tao = gio(r.get("created_at"))
        if tao is None:
            loai.append((r.get("id"), "thieu_created_at")); continue
        if tao > b:
            loai.append((r.get("id"), "sau_T1")); continue
        if workflow == WF_CI:
            if tao < a:
                loai.append((r.get("id"), "truoc_T0")); continue
            if not (r.get("event") == "pull_request" or (r.get("event") == "push" and r.get("head_branch") == "master")):
                loai.append((r.get("id"), "su_kien_ngoai_pham_vi")); continue
        if r.get("status") != "completed":
            loai.append((r.get("id"), "chua_completed_luc_thu")); continue
        trong.append(r)
    return trong, loai


RE_DK = re.compile(r"^\ufeff?\S+Z CI_DANG_KY_THOI_GIAN (.*)$")
RE_CHE_DO = re.compile(r"^\ufeff?\S+Z che_do=(duong_nhanh|day_du)\s*$")
RE_LUON_DAY_DU = re.compile(r"^\ufeff?\S+Z DUONG_NHANH: khong phan loai - .*luon DAY_DU\s*$")
RE_MO = re.compile(r"^\ufeff?\S+Z (\w+) MANH (\d+)/(\d+): (\d+) muc")
RE_KQ = re.compile(r"^\ufeff?\S+Z KET QUA (\S+): (\w+)(?: \(([0-9]+(?:\.[0-9]+)?)s\))?\s*$")
RE_DONG = re.compile(r"^\ufeff?\S+Z (\w+) MANH (\d+)/(\d+): rc=(-?\d+) · passed (\d+)/(\d+)")


def trich_thoi_gian_dang_ky(van_ban):
    """Ban ghi `CI_DANG_KY_THOI_GIAN` (.claude/dev/ci_dang_ky_test.py). Tra {'trang_thai_log': co|cat_cut|khong_co_ban_ghi, 'bo': [...]}.
    Moi bo: duong_dan, rc, che_do (khong ghi -> 'khong_ghi'), giay ba trang thai (0 la do_duoc; am/thieu -> khong_do_duoc)."""
    dong = [m.group(1) for m in map(RE_DK.match, van_ban.splitlines()) if m]
    if not dong:
        return {"trang_thai_log": "khong_co_ban_ghi", "bo": []}
    try:
        js = json.loads(dong[-1])
        bo_tho = js["bo"]
        if not isinstance(bo_tho, list):
            raise ValueError("bo khong phai list")
    except (ValueError, KeyError, TypeError):
        return {"trang_thai_log": "cat_cut", "bo": []}
    bo = []
    for m in bo_tho:
        g = m.get("giay") if isinstance(m, dict) else None
        if isinstance(g, bool) or not isinstance(g, (int, float)) or not math.isfinite(g):
            giay = kdd("thieu_giay")
        elif g < 0:
            giay = kdd("giay_am")
        else:
            giay = gt(g)
        bo.append({"duong_dan": m.get("duong_dan") if isinstance(m, dict) else None, "rc": m.get("rc") if isinstance(m, dict) else None,
                   "che_do": (m.get("che_do") if isinstance(m, dict) else None) or "khong_ghi", "giay": giay})
    return {"trang_thai_log": "co", "bo": bo, "N": js.get("N"), "so_lop_logic": js.get("so_lop_logic")}


def trich_ket_qua(van_ban):
    """Dong `KET QUA <khoa>: <kq> (<giay>s)` cua job manh (ops/nhanh_don_duoc_test.py). trang_thai_log: co | cat_cut | khong_co_ban_ghi."""
    mo = dong = None
    muc = []
    for l in van_ban.splitlines():
        m = RE_MO.match(l)
        if m and mo is None:
            mo = {"che_do": m.group(1), "manh": int(m.group(2)), "so_manh": int(m.group(3)), "so_muc_khai": int(m.group(4))}
            continue
        m = RE_KQ.match(l)
        if m:
            muc.append({"khoa": m.group(1), "ket_qua": m.group(2),
                        "giay": gt(float(m.group(3))) if m.group(3) is not None else kdd("dong KET QUA khong ghi giay")})
            continue
        m = RE_DONG.match(l)
        if m:
            dong = {"rc": int(m.group(4)), "passed": int(m.group(5)), "tong": int(m.group(6))}
    if mo is None and not muc:
        return {"trang_thai_log": "khong_co_ban_ghi", "muc": []}
    return {"trang_thai_log": "co" if (mo is not None and dong is not None) else "cat_cut", "mo": mo, "dong": dong, "muc": muc}


def trich_lan(van_ban):
    """Lan tu log job chuan-bi: dong `che_do=duong_nhanh|day_du` CUOI CUNG cua buoc phan loai; khong co thi dong
    `DUONG_NHANH: khong phan loai - ... luon DAY_DU` (buoc che do cua workflow truoc 02-11-2026, push/dispatch) -> day_du; con lai -> None."""
    dong = van_ban.splitlines()
    kq = [m.group(1) for m in map(RE_CHE_DO.match, dong) if m]
    if kq:
        return kq[-1]
    return "day_du" if any(RE_LUON_DAY_DU.match(l) for l in dong) else None


def trang_thai_nguon(muc):
    """Muc MANIFEST cua mot log/artifact -> co | het_han | loi | khong_thu."""
    if muc is None:
        return "khong_thu"
    if muc.get("http") == 200 and muc.get("duong_dan"):
        return "co"
    if muc.get("http") == 410:
        return "het_han"
    if muc.get("loi") == "het_khung_thoi_gian":
        return "khong_thu"
    return "loi"


def doc_artifact_manh(du_lieu):
    """Noi dung zip cua mot artifact manh -> so lieu (so muc, rc, moi truong thoi gian co san) hoac cat_cut."""
    try:
        z = zipfile.ZipFile(io.BytesIO(du_lieu))
        ten = sorted(n for n in z.namelist() if n.endswith(".json"))
        d = json.loads(z.read(ten[0]).decode("utf-8"))
        if not isinstance(d, dict):
            raise ValueError
    except (zipfile.BadZipFile, IndexError, ValueError, KeyError, UnicodeDecodeError):
        return {"trang_thai": KHONG_DO_DUOC, "ly_do": "cat_cut (zip/JSON khong doc duoc)"}
    kq = d.get("ket_qua") if isinstance(d.get("ket_qua"), dict) else None
    g = d.get("giay")
    return {"trang_thai": DO_DUOC, "che_do": d.get("che_do"), "manh": d.get("manh"), "so_manh": d.get("so_manh"), "head": d.get("head"),
            "rc": d.get("rc"), "so_muc": len(kq) if kq is not None else None,
            "so_muc_passed": sum(1 for v in kq.values() if v == "passed") if kq is not None else None,
            "bat_dau": d.get("bat_dau"), "ket_thuc": d.get("ket_thuc"),
            "giay": gt(g) if isinstance(g, (int, float)) and not isinstance(g, bool) and g >= 0 else kdd("thieu_giay hoac giay_am"),
            "ram_dinh_mb": d.get("ram_dinh_mb"), "so_lan_chay_lai": d.get("so_lan_chay_lai")}


def can_log(wf, muc):
    """Dong nao phai tai log (dung chung --thu va --tinh). Tra nhan loai log hoac None."""
    if muc["loai_dong"] != THUC_THI:
        return None
    if wf == WF_DU:
        return "manh" if muc["ten_goc"] == "dot-bien-manh" else ("dang_ky_du" if muc["ten_goc"] == "dot-bien-du" else "khac_du")
    if muc["ten_goc"] == "chuan-bi":
        return "chuan_bi"
    if muc["ten_goc"] == "gate-registry":
        for b in muc["_tho"].get("steps") or []:
            if str(b.get("name", "")).startswith(TIEN_TO_BUOC_REGISTRY) and b.get("conclusion") != "skipped":
                return "dang_ky_ci"
    return None


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def xuat_json(o, sau=2, muc=0):
    """JSON tat dinh: in dep toi do sau `sau`, phan con lai mot dong (giu tep doc duoc ma khong phinh)."""
    if muc >= sau or not isinstance(o, (dict, list)) or not o:
        return json.dumps(o, ensure_ascii=False, separators=(",", ":"))
    lui, lui_trong = " " * muc, " " * (muc + 1)
    if isinstance(o, dict):
        ph = [lui_trong + json.dumps(str(k), ensure_ascii=False) + ":" + xuat_json(v, sau, muc + 1) for k, v in o.items()]
        return "{\n" + ",\n".join(ph) + "\n" + lui + "}"
    return "[\n" + ",\n".join(lui_trong + xuat_json(v, sau, muc + 1) for v in o) + "\n" + lui + "]"


# ───────────────────── bo ghi co gioi han (MOI lan ghi cua --thu va --tinh di qua day) ─────────────────────

class GhiBiTuChoi(Exception):
    pass


def duong_an_toan(goc, tuong_doi):
    """Dich ghi `tuong_doi` duoi thu muc `goc`. Tu choi: duong tuyet doi, thanh phan `.`/`..`/rong, BAT KY thanh phan nao la symlink,
    dich la symlink hoac khong phai tep thuong, va moi truong hop thu muc cha giai ra NGOAI `goc`. Tao thu muc con con thieu."""
    goc_that = pathlib.Path(os.path.realpath(goc))
    if not goc_that.is_dir():
        raise GhiBiTuChoi(f"thu muc goc khong ton tai: {goc}")
    pp = pathlib.PurePosixPath(str(tuong_doi).replace(os.sep, "/"))
    ph = pp.parts
    if pp.is_absolute() or not ph or any(x in ("", ".", "..") for x in ph):
        raise GhiBiTuChoi(f"duong dan dich khong hop le: {tuong_doi!r}")
    cha = goc_that
    for x in ph[:-1]:
        cha = cha / x
        if cha.is_symlink():
            raise GhiBiTuChoi(f"thanh phan duong dan la symlink: {cha.relative_to(goc_that).as_posix()}")
        if not cha.exists():
            cha.mkdir()
        elif not cha.is_dir():
            raise GhiBiTuChoi(f"thanh phan duong dan khong phai thu muc: {cha.relative_to(goc_that).as_posix()}")
    that = pathlib.Path(os.path.realpath(cha))
    if that != goc_that and goc_that not in that.parents:
        raise GhiBiTuChoi(f"thu muc cha giai ra ngoai goc: {tuong_doi!r}")
    dich = cha / ph[-1]
    if dich.is_symlink():
        raise GhiBiTuChoi(f"dich la symlink: {tuong_doi!r}")
    if dich.exists() and not dich.is_file():
        raise GhiBiTuChoi(f"dich khong phai tep thuong: {tuong_doi!r}")
    return dich


def ghi_tep(goc, tuong_doi, du_lieu):
    """Ghi bytes vao `goc/tuong_doi`: kiem `duong_an_toan`, ghi tep tam CUNG thu muc (ten ngau nhien, O_EXCL), roi os.replace."""
    dich = duong_an_toan(goc, tuong_doi)
    fd, tam = tempfile.mkstemp(dir=str(dich.parent), prefix=".tam-wp1434-")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(du_lieu)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tam, 0o644)
        os.replace(tam, dich)
    except BaseException:
        if os.path.lexists(tam):
            os.unlink(tam)
        raise
    return dich


def mo_noi_them(goc, tuong_doi):
    """Mo tep nhat ky de noi them, qua cung chot `duong_an_toan`; O_NOFOLLOW khi nen co."""
    dich = duong_an_toan(goc, tuong_doi)
    fd = os.open(str(dich), os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o644)
    return os.fdopen(fd, "a", encoding="utf-8")


def bang_md(tieu_de, cac_hang):
    """Bang GFM: moi o duoc thoat `|` va bo xuong dong; hang lech so o voi tieu de -> ValueError (khong sinh bang vo)."""
    o = lambda x: str(x).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")
    ra = ["| " + " | ".join(o(x) for x in tieu_de) + " |", "|" + "---|" * len(tieu_de)]
    for h in cac_hang:
        if len(h) != len(tieu_de):
            raise ValueError(f"hang {len(h)} o, tieu de {len(tieu_de)} o: {h!r}")
        ra.append("| " + " | ".join(o(x) for x in h) + " |")
    return ra


def loi_bang_md(van_ban):
    """Moi hang cua moi bang GFM phai co cung so o voi hang tieu de (dem theo `|` KHONG bi thoat). Tra danh sach loi."""
    loi, so_o = [], None
    for i, l in enumerate(van_ban.splitlines(), 1):
        if not l.startswith("|"):
            so_o = None
            continue
        n = len(re.split(r"(?<!\\)\|", re.sub(r"\\\\", "", l))) - 2
        if so_o is None:
            so_o = n
        elif n != so_o:
            loi.append(f"dong {i}: {n} o, tieu de {so_o} o")
    return loi


# ───────────────────────────────────────────── --thu ─────────────────────────────────────────────

class Thu:
    def __init__(self, ra, han_giay, so_luong):
        import urllib.request
        self.ur = urllib.request
        self.ra = pathlib.Path(ra).resolve()
        if ROOT == self.ra or ROOT in self.ra.parents:
            raise SystemExit("anh chup phai nam NGOAI kho")
        self.ra.mkdir(parents=True, exist_ok=True)
        self.han = time.monotonic() + han_giay
        self.khoa = threading.Lock()
        self.nhip = threading.Lock()
        self.lan_cuoi = 0.0
        self.ngu_den = 0.0
        self.muc = {}
        self.so_luong = so_luong
        self.nk = self.ra / "MANIFEST.partial.jsonl"
        if self.nk.exists():
            for l in self.nk.read_text(encoding="utf-8").splitlines():
                try:
                    m = json.loads(l)
                except ValueError:
                    continue
                if m.get("http") == 200 and m.get("duong_dan") and (self.ra / m["duong_dan"]).exists():
                    self.muc[m["khoa"]] = m
        cu = self.ra / "MANIFEST.json"
        if cu.exists():                                   # tiep tuc mot lan thu da dong MANIFEST: giu moi muc da co tep, thu lai muc loi
            for m in json.loads(cu.read_text(encoding="utf-8"))["tep"]:
                if m.get("http") == 200 and m.get("duong_dan") and (self.ra / m["duong_dan"]).exists():
                    self.muc.setdefault(m["khoa"], m)
        self.f_nk = mo_noi_them(self.ra, "MANIFEST.partial.jsonl")

        class KhongChuyenHuong(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *a, **k):
                return None
        self.mo_api = urllib.request.build_opener(KhongChuyenHuong)

    def _goi(self, duong):
        """Mot GET toi API. Tra (http, bytes | None, loi | None). Token chi di toi api.github.com; chang hai (URL co chu ky) khong mang token."""
        import urllib.error
        loi = None
        for lan in range(5):
            if time.monotonic() > self.han:
                return None, None, "het_khung_thoi_gian"
            with self.nhip:
                cho = max(self.lan_cuoi + 0.09 - time.monotonic(), self.ngu_den - time.monotonic(), 0)
                if cho > 0:
                    time.sleep(min(cho, max(self.han - time.monotonic(), 0) + 1))
                self.lan_cuoi = time.monotonic()
            yc = self.ur.Request(API + duong, headers={"Authorization": "Bearer " + os.environ["GITHUB_PAT"],
                                                       "Accept": "application/vnd.github+json", "User-Agent": "wp1434-thu-thap"})
            try:
                with self.mo_api.open(yc, timeout=120) as p:
                    self._nhin_han_muc(p.headers)
                    return p.status, p.read(), None
            except urllib.error.HTTPError as e:
                h = e.headers
                if e.code in (301, 302, 303, 307, 308):
                    dich = h.get("Location")
                    try:
                        with self.ur.urlopen(self.ur.Request(dich, headers={"User-Agent": "wp1434-thu-thap"}), timeout=300) as p:
                            return 200, p.read(), None
                    except urllib.error.HTTPError as e2:
                        ma2 = e2.code
                        if ma2 in (404, 410):
                            return ma2, None, f"chang hai tra {ma2}"
                        loi = f"chang hai HTTP {ma2}"
                    except Exception as e2:                      # khong in e2: thong diep co the mang URL co chu ky
                        loi = f"chang hai {type(e2).__name__} (co the cat cut khi tai)"
                    time.sleep(2 + lan * 3)
                    continue
                het = h.get("X-RateLimit-Remaining") == "0" or h.get("Retry-After")
                if e.code in (403, 429) and het:
                    doi = float(h.get("Retry-After") or 0) or max(float(h.get("X-RateLimit-Reset") or 0) - time.time(), 5) + 2
                    with self.nhip:
                        self.ngu_den = max(self.ngu_den, time.monotonic() + doi)
                    print(f"  gioi han toc do: cho {int(doi)}s theo header", flush=True)
                    loi = f"HTTP {e.code} gioi han toc do"
                    continue
                if e.code >= 500:
                    loi = f"HTTP {e.code}"
                    time.sleep(2 + lan * 3)
                    continue
                return e.code, None, f"HTTP {e.code}"
            except Exception as e:
                loi = f"{type(e).__name__}"
                time.sleep(2 + lan * 3)
        return None, None, loi

    def _nhin_han_muc(self, h):
        try:
            con = int(h.get("X-RateLimit-Remaining"))
        except (TypeError, ValueError):
            return
        if con < 150:
            doi = max(float(h.get("X-RateLimit-Reset") or 0) - time.time(), 5) + 2
            with self.nhip:
                self.ngu_den = max(self.ngu_den, time.monotonic() + doi)

    def lay(self, khoa, duong_api, tep, loai):
        """Tai mot nguon vao anh chup (bo qua neu da co). Tra muc MANIFEST."""
        with self.khoa:
            if khoa in self.muc and self.muc[khoa].get("http") == 200:
                return self.muc[khoa]
        http, du_lieu, loi = self._goi(duong_api)
        m = {"khoa": khoa, "loai": loai, "url": API + duong_api, "http": http, "duong_dan": None, "sha256": None, "kich_thuoc": None}
        if http == 200 and du_lieu is not None:
            ghi_tep(self.ra, tep, du_lieu)
            m.update(duong_dan=tep, sha256=sha256_bytes(du_lieu), kich_thuoc=len(du_lieu))
        else:
            m["loi"] = loi or f"HTTP {http}"
        with self.khoa:
            self.muc[khoa] = m
            self.f_nk.write(json.dumps(m, ensure_ascii=False) + "\n")
            self.f_nk.flush()
        return m

    def doc(self, m):
        return json.loads((self.ra / m["duong_dan"]).read_bytes()) if m.get("duong_dan") else None

    def song_song(self, viec):
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.so_luong) as ex:
            kq = list(ex.map(lambda v: v(), viec))
        return kq

    def trang(self, khoa_goc, duong, tep_goc, loai, khoa_ds, co=100):
        """Phan trang per_page=100; trang 100 loi (vd. 502 voi phan hoi qua lon) thi thu lai TOAN BO voi per_page=30 duoi khoa `<goc>/c30`.
        Tra (danh sach, tong_dem, du?)."""
        ds, tong, trang, du = [], None, 1, True
        while True:
            m = self.lay(f"{khoa_goc}/p{trang}", f"{duong}{'&' if '?' in duong else '?'}per_page={co}&page={trang}", f"{tep_goc}/p{trang}.json", loai)
            d = self.doc(m)
            if d is None:
                du = False
                break
            tong = d.get("total_count")
            ds += d.get(khoa_ds) or []
            if len(d.get(khoa_ds) or []) < co or (tong is not None and len(ds) >= tong):
                break
            trang += 1
        if not du and co == 100 and m.get("loi") != "het_khung_thoi_gian":
            return self.trang(khoa_goc + "/c30", duong, tep_goc + "/c30", loai, khoa_ds, 30)
        return ds, tong, du


def lenh_thu(ns):
    if not os.environ.get("GITHUB_PAT"):
        raise SystemExit("thieu bien moi truong GITHUB_PAT")
    t = Thu(ns.ra, ns.han_giay, ns.so_luong)
    f_meta = t.ra / "META.json"
    if f_meta.exists():
        meta = json.loads(f_meta.read_text(encoding="utf-8"))
        print("tiep tuc lan thu da co, T1 =", meta["T1"])
    else:
        t1 = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        sha = subprocess.run(["git", "rev-parse", "origin/master"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if not re.fullmatch(r"[0-9a-f]{40}", sha):
            raise SystemExit("khong doc duoc SHA origin/master")
        meta = {"kho": KHO, "T0": iso(t1 - datetime.timedelta(days=NGAY_COHORT)), "T1": iso(t1), "sha_master": sha,
                "lenh_sha_master": "git rev-parse origin/master", "spec_sha256": SPEC_SHA256, "khoang_con": []}
        ghi_tep(t.ra, "META.json", (json.dumps(meta, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    t0, t1 = gio(meta["T0"]), gio(meta["T1"])

    # 1) liet ke
    ds_du, tong_du, du_du = t.trang("list/du", f"actions/workflows/{WF_DU}/runs", "list/du", "list", "workflow_runs")
    khoang_con, ds_ci = [], []

    def liet_ke(su_kien, a, b, nhan):
        loc = "event=pull_request" if su_kien == "pull_request" else "event=push&branch=master"
        tu, den = iso(a), iso(b)
        duong = f"actions/workflows/{WF_CI}/runs?{loc}&created={tu}..{den}"
        m = t.lay(f"list/ci/{su_kien}/{nhan}/p1", duong + "&per_page=100&page=1", f"list/ci/{su_kien}/{nhan}/p1.json", "list")
        d = t.doc(m)
        tong = d.get("total_count") if d else None
        if tong is not None and tong >= 1000 and (b - a).total_seconds() >= 2:
            giua = a + datetime.timedelta(seconds=int((b - a).total_seconds() // 2))
            khoang_con.append({"su_kien": su_kien, "tu": tu, "den": den, "tong": tong, "chia_doi": True})
            liet_ke(su_kien, a, giua, nhan + "a")
            liet_ke(su_kien, giua + datetime.timedelta(seconds=1), b, nhan + "b")
            return
        ds, tong, du = t.trang(f"list/ci/{su_kien}/{nhan}", duong, f"list/ci/{su_kien}/{nhan}", "list", "workflow_runs")
        khoang_con.append({"su_kien": su_kien, "tu": tu, "den": den, "tong": tong, "so_lay": len(ds), "du": du, "nhan": nhan})
        ds_ci.extend(ds)

    for su_kien in ("pull_request", "push"):
        a = t0
        i = 0
        while a <= t1:
            b = min(a + datetime.timedelta(days=1) - datetime.timedelta(seconds=1), t1)
            liet_ke(su_kien, a, b, f"{i:02d}")
            a, i = b + datetime.timedelta(seconds=1), i + 1
    meta["khoang_con"] = khoang_con
    meta["liet_ke_du"] = {"tong": tong_du, "so_lay": len(ds_du), "du": du_du}
    ghi_tep(t.ra, "META.json", (json.dumps(meta, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    co_du, _ = loc_cohort(ds_du, WF_DU, meta["T0"], meta["T1"])
    co_ci, _ = loc_cohort(list({r["id"]: r for r in ds_ci}.values()), WF_CI, meta["T0"], meta["T1"])
    print(f"cohort: {WF_DU} {len(co_du)} luot · {WF_CI} {len(co_ci)} luot", flush=True)

    # 2) job + attempt (M1 truoc, roi M2)
    def thu_luot(wf, r):
        rid, n = r["id"], int(r.get("run_attempt") or 1)
        tao = {1: r.get("created_at")} if n == 1 else {}
        if n > 1:
            for k in range(1, n + 1):
                d = t.doc(t.lay(f"att/{rid}/{k}", f"actions/runs/{rid}/attempts/{k}", f"att/{rid}/{k}.json", "attempt"))
                tao[k] = d.get("created_at") if d else None
        dong, _, _ = t.trang(f"jobs/{rid}", f"actions/runs/{rid}/jobs?filter=all", f"jobs/{rid}", "jobs", "jobs")
        return wf, r, tinh_luot(r, tao, dong)

    def thu_log(job_id):
        t.lay(f"log/{job_id}", f"actions/jobs/{job_id}/logs", f"log/{job_id}.log", "log")

    def thu_artifact(r):
        ds, _, _ = t.trang(f"arts/{r['id']}", f"actions/runs/{r['id']}/artifacts", f"arts/{r['id']}", "artifacts", "artifacts")
        for a in ds:
            if str(a.get("name", "")).startswith("dot-bien-manh") and not a.get("expired"):
                t.lay(f"art/{a['id']}", f"actions/artifacts/{a['id']}/zip", f"art/{a['id']}.zip", "artifact")

    def pha(ten, viec):
        bd = time.monotonic()
        t.song_song(viec)
        print(f"pha {ten}: {len(viec)} viec, {int(time.monotonic() - bd)}s", flush=True)

    kq_du = t.song_song([lambda r=r: thu_luot(WF_DU, r) for r in co_du])
    print("M1 job/attempt xong", flush=True)
    pha("M1 artifact", [lambda r=r: thu_artifact(r) for r in co_du])
    pha("M1 log", [lambda j=m["job_id"]: thu_log(j) for _, _, lu in kq_du for m in lu["dong"] if can_log(WF_DU, m)])
    kq_ci = t.song_song([lambda r=r: thu_luot(WF_CI, r) for r in co_ci])
    print("M2 job/attempt xong", flush=True)
    for nhan in ("dang_ky_ci", "chuan_bi"):
        pha("log " + nhan, [lambda j=m["job_id"]: thu_log(j) for _, _, lu in kq_ci for m in lu["dong"] if can_log(WF_CI, m) == nhan])

    # 3) su kien kho (khong mang) + MANIFEST
    t.f_nk.close()
    dong_manifest(t.ra, list(t.muc.values()) + thu_su_kien_kho(t.ra, meta["sha_master"]))
    t.nk.unlink()
    return 0


def dong_manifest(ra, muc):
    b_meta = (ra / "META.json").read_bytes()
    muc = sorted((m for m in muc if m["khoa"] != "META"), key=lambda m: m["khoa"])
    muc.insert(0, {"khoa": "META", "loai": "meta", "url": None, "http": None, "duong_dan": "META.json",
                   "sha256": sha256_bytes(b_meta), "kich_thuoc": len(b_meta)})
    ghi_tep(ra, "MANIFEST.json", (json.dumps({"tep": muc}, ensure_ascii=False, indent=0) + "\n").encode("utf-8"))
    loi = sum(1 for m in muc if m.get("loi"))
    print(f"MANIFEST: {len(muc)} muc, {loi} muc khong co tep (loi/het han/het khung), {sum(1 for m in muc if m['loai'] == 'kho')} muc su kien kho")


def lenh_bo_sung_kho(ns):
    """Buoc RIENG, khong mang: them su kien kho (tep M4, blame, bang M3) vao anh chup DA CO. Khong liet ke lai, khong doi T0/T1/cohort."""
    ra = pathlib.Path(ns.ra).resolve()
    if ROOT == ra or ROOT in ra.parents:
        raise SystemExit("anh chup phai nam NGOAI kho")
    meta = json.loads((ra / "META.json").read_bytes())
    cu = json.loads((ra / "MANIFEST.json").read_bytes())["tep"]
    giu = [m for m in cu if m["loai"] not in ("kho", "meta")]
    print(f"BO SUNG SU KIEN KHO vao anh chup da co: T0 {meta['T0']} · T1 {meta['T1']} · sha_master {meta['sha_master']} (GIU NGUYEN); "
          f"{len(giu)} muc API giu nguyen, {len(cu) - len(giu) - 1} muc kho cu bi thay")
    dong_manifest(ra, giu + thu_su_kien_kho(ra, meta["sha_master"]))
    return 0


# ───────────────────────────────────────────── --tinh ─────────────────────────────────────────────

def git_show(sha, duong):
    r = subprocess.run(["git", "show", f"{sha}:{duong}"], cwd=ROOT, capture_output=True)
    return r.stdout if r.returncode == 0 else None


def git_ds(sha, tien_to):
    r = subprocess.run(["git", "ls-tree", "-r", "--name-only", sha, "--"] + list(tien_to), cwd=ROOT, capture_output=True)
    return sorted(r.stdout.decode("utf-8", errors="replace").splitlines()) if r.returncode == 0 else []


M3_GOC = (".claude/dev/", ".claude/hooks/", ".githooks/", ".github/checks/", "scripts/tl_core/", "ops/")
# Tap mau TUONG MINH cho bang ca/dot bien. Khong tin rieng tap nay: `m3_nghi_bo_sot` bao MOI bang da import co ten chua MUT/DOT_BIEN ma khong duoc
# chon; ten nao bi loai co chu dich phai nam trong M3_LOAI kem ly do, con lai la `nghi_bo_sot` (hien trong BASELINE va BAO_CAO).
M3_RE = re.compile(r"MUTANT|MUTATION|DOT_BIEN|TU_KIEM|CASES|^CA$|CA_DAI")
M3_THEM = {".claude/dev/ci_dang_ky_test.py": ("DANG_KY", "MOI", "NHE", "MOI_WINDOWS", "CACH_LY", "DA_NOI")}
M3_LOAI = {"_WP1393_IMMUTABLE": "ten chua chuoi MUT vi la IMMUTABLE (tap truong bat bien), khong phai bang dot bien"}
M3_RE_CHOT = re.compile(r"^if __name__ == ['\"]__main__['\"]", re.M)
M3_MA = ("import importlib.util,json,sys,os\n"
         "p=sys.argv[1]; sys.path.insert(0,os.path.dirname(os.path.abspath(p)))\n"
         "s=importlib.util.spec_from_file_location('wp1434_m3_doc_bang',p); m=importlib.util.module_from_spec(s)\n"
         "sys.modules['wp1434_m3_doc_bang']=m; s.loader.exec_module(m)\n"
         "def ten(x):\n"
         "    if isinstance(x,str): return x\n"
         "    if isinstance(x,(tuple,list)) and x and isinstance(x[0],str): return x[0]\n"
         "    return getattr(x,'__name__',None) if callable(x) else None\n"
         "b,t,h={},{},{}\n"
         "for n,v in sorted(vars(m).items()):\n"
         "    if not n.isupper(): continue\n"
         "    if isinstance(v,(list,tuple,dict,set,frozenset)):\n"
         "        b[n]=len(v)\n"
         "        ds=[ten(x) for x in v]\n"
         "        if len(ds)<=5000 and all(isinstance(x,str) for x in ds): t[n]=sorted(ds) if isinstance(v,(set,frozenset)) else ds\n"
         "    elif isinstance(v,(int,float)) and not isinstance(v,bool): h[n]=v\n"
         "print('WP1434_M3 '+json.dumps({'bang':b,'ten':t,'hang_so':h}))\n")
M3_HOP = ("tmp", "home", "cwd", "xdg/cache", "xdg/config", "xdg/data", "xdg/state", "xdg/run")
M4_PR = (895,)                      # PR ma loi khai M4 nhac toi: can anh xa PR -> nhanh (tu merge commit first-parent, khong mang)


def la_bo_test_song(tep):
    """Cung dinh nghia 'test song' voi `tim()` cua .claude/dev/ci_dang_ky_test.py (ops chi nhan tep muc dinh, bo ops/reviews)."""
    return (tep.endswith("_test.py") and tep.startswith(M3_GOC) and not tep.startswith("ops/reviews/")
            and not (tep.startswith("ops/") and tep.count("/") != 1))


def chup_thu_muc(d, sau):
    """Anh cua mot thu muc canh gac. `sau`=False: ten cac muc muc dinh; True: de quy (duong dan, kich thuoc, mtime_ns). Khong doc duoc -> None."""
    try:
        if not sau:
            return sorted(os.listdir(d))
        kq = []
        for goc, ds, tep in os.walk(d):
            for x in sorted(ds + tep):
                p = os.path.join(goc, x)
                st = os.lstat(p)
                kq.append((os.path.relpath(p, d), st.st_size, st.st_mtime_ns))
        return sorted(kq)
    except OSError:
        return None


def moi_truong_hop_cat(hop):
    """Bien moi truong ep MOI tac dung phu luc import vao hop cat `hop` (duoi --ra): thu muc tam, HOME, XDG_*."""
    h = str(hop)
    j = lambda x: os.path.join(h, *x.split("/"))
    return {"TMPDIR": j("tmp"), "TMP": j("tmp"), "TEMP": j("tmp"), "HOME": j("home"), "USERPROFILE": j("home"), "APPDATA": j("home"),
            "LOCALAPPDATA": j("home"), "XDG_CACHE_HOME": j("xdg/cache"), "XDG_CONFIG_HOME": j("xdg/config"), "XDG_DATA_HOME": j("xdg/data"),
            "XDG_STATE_HOME": j("xdg/state"), "XDG_RUNTIME_DIR": j("xdg/run"),
            "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}


def xoa_hop_cat(goc, tuong_doi):
    """Don hop cat: chi xoa khi no la thu muc THAT (khong symlink) nam duoi `goc`."""
    goc_that = pathlib.Path(os.path.realpath(goc))
    p = goc_that.joinpath(*tuong_doi.split("/"))
    q = goc_that
    for x in tuong_doi.split("/"):
        q = q / x
        if q.is_symlink():
            raise GhiBiTuChoi(f"hop cat co thanh phan la symlink: {tuong_doi!r}")
    if p.is_dir():
        shutil.rmtree(p)


def doc_bang_import(duong_tep, goc_hop, ten_hop, canh_gac=(), han=180):
    """Doc bang muc module (ten IN HOA) sau khi IMPORT xong tep trong tien trinh con: len() CUOI CUNG, ten phan tu, hang so nguyen/thuc.
    - Module nap duoi ten khac `__main__` => khoi `if __name__ == "__main__"` khong chay; tep thieu chot ay bi tu choi.
    - GIAM GIU: cwd, TMPDIR/TMP/TEMP, HOME, XDG_* cua tien trinh con deu la thu muc moi duoi `goc_hop`/kho/_import_sandbox/<ten_hop>/, xoa sau khi doc.
    - KIEM: chup thu muc tam THAT va HOME THAT cua tien trinh nay (ten muc dinh) + moi thu muc `canh_gac` (de quy) truoc va sau; doi => tu choi
      (fail-closed, thu lai mot lan de loai nhieu cua tien trinh khac).
    Tra (du lieu | None, ly_do | None, so tep con lai trong hop cat truoc khi don)."""
    duong_tep = pathlib.Path(duong_tep)
    try:
        nguon = duong_tep.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return None, f"khong doc duoc tep ({type(e).__name__})", 0
    if not M3_RE_CHOT.search(nguon):
        return None, "tep khong co chot `if __name__ == \"__main__\"` o muc module: khong import (co the chay bo luc import)", 0
    rel = "kho/_import_sandbox/" + re.sub(r"[^A-Za-z0-9_.-]", "_", ten_hop)
    xem = [(os.environ.get("TMPDIR") or tempfile.gettempdir(), False), (os.path.expanduser("~"), False)] + [(str(d), True) for d in canh_gac]
    ly, con_lai = None, 0
    for lan in range(2):
        xoa_hop_cat(goc_hop, rel)
        for sub in M3_HOP:
            duong_an_toan(goc_hop, f"{rel}/{sub}/.giu")              # tao thu muc con qua chot khong-symlink
        hop = pathlib.Path(os.path.realpath(goc_hop)).joinpath(*rel.split("/"))
        truoc = [chup_thu_muc(d, s) for d, s in xem]
        try:
            r = subprocess.run([sys.executable, "-c", M3_MA, str(duong_tep.resolve())], cwd=str(hop / "cwd"), capture_output=True, text=True,
                               timeout=han, stdin=subprocess.DEVNULL, env={**os.environ, **moi_truong_hop_cat(hop)})
        except subprocess.TimeoutExpired:
            r = None
        sau = [chup_thu_muc(d, s) for d, s in xem]
        con_lai = sum(len(tep) for _, _, tep in os.walk(hop))
        xoa_hop_cat(goc_hop, rel)
        doi = [d for (d, _), a, b in zip(xem, truoc, sau) if a is None or a != b]
        if doi:
            ly = "import lam doi thu muc NGOAI hop cat (hoac khong chup duoc): " + ", ".join(doi)
            continue                                                  # fail-closed; thu lai mot lan
        if r is None:
            return None, f"import qua {han}s", con_lai
        dong = [l for l in r.stdout.splitlines() if l.startswith("WP1434_M3 ")]
        if r.returncode != 0 or not dong:
            return None, f"import trong hop cat khong thanh (rc={r.returncode})", con_lai
        try:
            return json.loads(dong[-1][len("WP1434_M3 "):]), None, con_lai
        except ValueError:
            return None, "dau ra import khong phai JSON", con_lai
    return None, ly, con_lai


def m3_chon_bang(tep, bang):
    """Tu moi bang IN HOA da doc, giu bang ve ca/dot bien (M3_RE) + bang so dang ky cua ci_dang_ky_test."""
    return {n: v for n, v in sorted(bang.items()) if M3_RE.search(n) or n in M3_THEM.get(tep, ())}


def m3_nghi_bo_sot(tep, bang):
    """Chot DOC LAP voi M3_RE: moi bang da import co ten chua MUT hoac DOT_BIEN ma KHONG duoc chon. Tra [(ten, so, ly do loai | None)];
    ly do None = nghi bo sot (khong ai giai thich)."""
    chon = m3_chon_bang(tep, bang)
    return [(n, v, M3_LOAI.get(n)) for n, v in sorted(bang.items()) if ("MUT" in n or "DOT_BIEN" in n) and n not in chon]


def thu_su_kien_kho(ra, sha):
    """Su kien KHO ma --tinh can, chup vao anh chup de --tinh khong phu thuoc lich su git cua clone dang chay:
    (1) kho/tep/<duong dan>: noi dung tep pham vi M4 o `sha`; (2) kho/blame.json: commit first-parent + committer-time cua moi dong
    workflow khop regex M4; (3) kho/pr_nhanh.json: nhanh nguon cua cac PR trong M4_PR, doc tu merge commit first-parent;
    (4) kho/m3_import.json: bang cua moi bo test song (import GIAM GIU trong hop cat duoi anh chup, khong chay bo).
    Khong goi mang. Doi kho DAY DU (khong nong) va cay lam viec trung blob voi `sha` o cac tep duoc import."""
    def git(*a):
        return subprocess.run(["git"] + list(a), cwd=ROOT, capture_output=True, text=True)
    if git("rev-parse", "--is-shallow-repository").stdout.strip() != "false":
        raise SystemExit("su kien kho: kho NONG (hoac khong doc duoc) - blame se sai; can clone day du")
    if git("cat-file", "-e", sha + "^{commit}").returncode != 0:
        raise SystemExit(f"su kien kho: khong co commit {sha}")
    muc = []

    def ghi(khoa, du_lieu, nguon):
        ghi_tep(ra, khoa, du_lieu)
        muc.append({"khoa": khoa, "loai": "kho", "url": None, "http": None, "duong_dan": khoa, "sha256": sha256_bytes(du_lieu),
                    "kich_thuoc": len(du_lieu), "nguon": nguon})

    def ghi_json(khoa, o, nguon):
        ghi(khoa, (json.dumps(o, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8"), nguon)

    tep_kho = {}
    for tep in git_ds(sha, M4_TEP):
        if tep.endswith((".yml", ".yaml", ".md")):
            b = git_show(sha, tep)
            if b is None:
                raise SystemExit(f"su kien kho: git show {sha[:12]}:{tep} loi")
            ghi("kho/tep/" + tep, b, f"git show {sha}:{tep}")
            tep_kho[tep] = b.decode("utf-8", errors="replace")
    blame = {}
    for tep, dong, _ in m4_quet(tep_kho):
        if tep.startswith(".github/workflows/"):
            r = git("blame", "--first-parent", "--porcelain", "-L", f"{dong},{dong}", sha, "--", tep)
            m = re.search(r"^committer-time (\d+)$", r.stdout, re.M) if r.returncode == 0 else None
            if not m:
                raise SystemExit(f"su kien kho: git blame {tep}:{dong} loi")
            blame[f"{tep}:{dong}"] = {"commit": r.stdout.split()[0],
                                      "committer_time": iso(datetime.datetime.fromtimestamp(int(m.group(1)), datetime.timezone.utc))}
    ghi_json("kho/blame.json", {"sha": sha, "lenh": "git blame --first-parent --porcelain -L <n>,<n> <sha> -- <tep>", "dong": blame},
             "git blame --first-parent (xem truong lenh)")
    pr = {}
    for so in M4_PR:
        r = git("log", "--first-parent", "--format=%H%x09%s", f"--grep=^Merge pull request #{so} from ", sha)
        m = re.match(rf"([0-9a-f]{{40}})\tMerge pull request #{so} from [^/\s]+/(\S+)$", r.stdout.strip().splitlines()[0]) if r.stdout.strip() else None
        pr[str(so)] = {"commit": m.group(1), "nhanh": m.group(2)} if m and len(r.stdout.strip().splitlines()) == 1 else None
    ghi_json("kho/pr_nhanh.json", {"sha": sha, "lenh": "git log --first-parent --format=%H%x09%s --grep='^Merge pull request #<n> from ' <sha>", "pr": pr},
             "git log --first-parent (xem truong lenh)")
    bo = {}
    for tep in git_ds(sha, M3_GOC):
        if not la_bo_test_song(tep):
            continue
        blob = git("rev-parse", f"{sha}:{tep}").stdout.strip()
        if blob != git("hash-object", "--", tep).stdout.strip():
            bo[tep] = {"blob": blob, "bang": None, "ly_do": "tep tren cay lam viec khac blob o sha_master"}
            continue
        truoc = git("status", "--porcelain", "--ignored").stdout
        dl, ly, con_lai = doc_bang_import(ROOT / tep, ra, tep)
        if git("status", "--porcelain", "--ignored").stdout != truoc:
            dl, ly = None, "import lam doi cay lam viec cua kho (git status --porcelain --ignored khac truoc/sau)"
        bo[tep] = dict(dl or {"bang": None}, blob=blob, ly_do=ly, so_tep_trong_hop_cat=con_lai)
    xoa_hop_cat(ra, "kho/_import_sandbox")
    ghi_json("kho/m3_import.json", {"sha": sha, "bo": bo,
                                    "lenh": "import tep duoi ten khac __main__ trong tien trinh con GIAM GIU (cwd/TMPDIR/HOME/XDG_* duoi <anh chup>/kho/_import_sandbox/, "
                                            "da xoa); doc len(), ten phan tu va hang so cua bien IN HOA"}, "import giam giu (xem truong lenh)")
    print(f"su kien kho: {len(tep_kho)} tep M4, {len(blame)} dong blame, {len(pr)} PR, {len(bo)} bo test "
          f"({sum(1 for x in bo.values() if x['bang'] is None)} khong import duoc; {sum(x.get('so_tep_trong_hop_cat', 0) for x in bo.values())} tep roi vao hop cat)")
    return muc


def m3_tu_anh_chup(du_lieu, sha):
    """M3 tu kho/m3_import.json cua anh chup. Thieu tep -> moi thu khong_do_duoc (KHONG doc cay lam viec thay the)."""
    kq = {"nguon": "kho/m3_import.json cua anh chup (len() cuoi cung sau import giam giu, chup o buoc su kien kho cua --thu)", "bang": {},
          "ten_chua_MUT_hoac_DOT_BIEN_khong_chon": [], "so_bang_nghi_bo_sot": 0}
    if not du_lieu or du_lieu.get("sha") != sha:
        kq["trang_thai"], kq["ly_do"] = KHONG_DO_DUOC, "anh chup thieu kho/m3_import.json (hoac lech sha_master)"
        return kq
    for tep, x in sorted(du_lieu["bo"].items()):
        nguon = f"import {tep}@{sha[:12]} (blob {str(x.get('blob'))[:12]})"
        if x.get("bang") is None:
            kq["bang"][tep] = {"_tep": kdd(x.get("ly_do") or "khong import duoc", nguon)}
            continue
        chon = m3_chon_bang(tep, x["bang"])
        kq["bang"][tep] = {n: gt(v, nguon) for n, v in chon.items()} or {"_tep": kad("khong co bang ca/dot bien nao o muc module", nguon)}
        for n, v, ly in m3_nghi_bo_sot(tep, x["bang"]):
            kq["ten_chua_MUT_hoac_DOT_BIEN_khong_chon"].append({"tep": tep, "bang": n, "so": v, "ly_do_loai": ly,
                                                                "trang_thai": "da_giai_thich" if ly else "nghi_bo_sot"})
            kq["so_bang_nghi_bo_sot"] += 0 if ly else 1
    return kq


M4_TEP = (".github/workflows/", "CLAUDE.md", "docs/", "ops/specs/wp1166")
M4_RG1 = r"(?i)đột biến|dot.bien|mutant|mutation|mảnh"
M4_RG2 = (r"(?i)[0-9]+([.,][0-9]+)? ?(s|giây|giay|phút|phut|h|giờ|gio)\b|~ ?[0-9]|"
          r"[0-9]+ (tự đột biến|mutant|đột biến|dot bien|ca|mảnh|manh|muc|mục)\b|[0-9]+/[0-9]+")
M4_LENH = ("rg -n -i 'đột biến|dot.bien|mutant|mutation|mảnh' .github/workflows CLAUDE.md docs ops/specs/wp1166* | rg -i \"<M4_RG2>\" "
           "(tuong duong: hai regex M4_RG1 roi M4_RG2 trong thu_thap.py, ap tren cac tep kho/tep/* cua anh chup = `git show <sha_master>:<tep>`)")


def doc_ma_tran_manh(van_ban):
    """So phan tu cua `manh: [a, b, ...]` (ma tran workflow) trong noi dung YAML; khong co dung MOT dong nhu the -> None."""
    ds = re.findall(r"^\s*manh:\s*\[([0-9,\s]+)\]\s*$", van_ban or "", re.M)
    return len([x for x in ds[0].split(",") if x.strip()]) if len(ds) == 1 else None


def m4_quet(tep_kho):
    """[(tep, so dong, van ban)] cho moi dong khop CA HAI regex, tren {duong dan: noi dung}."""
    r1, r2 = re.compile(M4_RG1), re.compile(M4_RG2)
    kq = []
    for tep in sorted(tep_kho):
        if not tep.endswith((".yml", ".yaml", ".md")):
            continue
        for i, l in enumerate(tep_kho[tep].splitlines(), 1):
            if r1.search(l) and r2.search(l):
                kq.append((tep, i, l.strip()))
    return kq


def lenh_tinh(ns):
    ac = pathlib.Path(ns.anh_chup).resolve()
    ra = pathlib.Path(ns.ra).resolve()
    b_man = (ac / "MANIFEST.json").read_bytes()
    manifest = json.loads(b_man)["tep"]
    theo_khoa = {m["khoa"]: m for m in manifest}
    meta = json.loads((ac / "META.json").read_bytes())
    sha = meta["sha_master"]
    hong = []
    for m in manifest:                                   # toan ven anh chup truoc khi tinh
        if m.get("duong_dan"):
            p = ac / m["duong_dan"]
            if not p.exists() or sha256_bytes(p.read_bytes()) != m["sha256"]:
                hong.append(m["khoa"])
    if hong:
        print("ANH CHUP LECH MANIFEST:", hong[:10], f"(+{max(len(hong) - 10, 0)})")
        return 3

    def doc(khoa):
        m = theo_khoa.get(khoa)
        return (ac / m["duong_dan"]).read_bytes() if m and m.get("duong_dan") else None

    def doc_trang(goc):
        ds, i, du = [], 1, True
        if doc(f"{goc}/p1") is None and f"{goc}/c30/p1" in theo_khoa:      # trang 100 loi, da thu lai voi per_page=30
            goc += "/c30"
        while f"{goc}/p{i}" in theo_khoa:
            b = doc(f"{goc}/p{i}")
            if b is None:
                du = False
                break
            d = json.loads(b)
            ds += d.get("workflow_runs") or d.get("jobs") or d.get("artifacts") or []
            i += 1
        return ds, du and i > 1

    def url(khoa):
        m = theo_khoa.get(khoa)
        return m["url"] if m else None

    def van_ban(job_id):
        b = doc(f"log/{job_id}")
        return None if b is None else b.decode("utf-8", errors="replace")

    # cohort
    ds_du, _ = doc_trang("list/du")
    ds_ci = []
    for k in meta["khoang_con"]:
        if not k.get("chia_doi"):
            ds_ci += doc_trang(f"list/ci/{k['su_kien']}/{k['nhan']}")[0]
    co_du, loai_du = loc_cohort(ds_du, WF_DU, meta["T0"], meta["T1"])
    co_ci, loai_ci = loc_cohort(sorted({r["id"]: r for r in ds_ci}.values(), key=lambda r: r["id"]), WF_CI, meta["T0"], meta["T1"])
    co_du.sort(key=lambda r: r["id"])

    phu = {k: {"yeu_cau": 0, "co": 0, "het_han": 0, "cat_cut": 0, "loi": 0, "khong_thu": 0, "khong_co_ban_ghi": 0}
           for k in ("jobs", "attempt", "log_manh", "log_dang_ky_du", "log_khac_du", "log_dang_ky_ci", "log_chuan_bi", "artifact_manh")}
    khong_do = []

    def tinh_mot(wf, r):
        rid, n = r["id"], int(r.get("run_attempt") or 1)
        tao = {1: r.get("created_at")} if n == 1 else {}
        if n > 1:
            for k in range(1, n + 1):
                phu["attempt"]["yeu_cau"] += 1
                b = doc(f"att/{rid}/{k}")
                tt = trang_thai_nguon(theo_khoa.get(f"att/{rid}/{k}"))
                phu["attempt"][tt] += 1
                tao[k] = json.loads(b).get("created_at") if b else None
                if b is None:
                    khong_do.append({"doi_tuong": f"attempt {rid}/{k}", "ly_do": tt, "nguon": url(f"att/{rid}/{k}")})
        dong, du = doc_trang(f"jobs/{rid}")
        phu["jobs"]["yeu_cau"] += 1
        if not du:
            tt = trang_thai_nguon(theo_khoa.get(f"jobs/{rid}/p1")) if f"jobs/{rid}/p1" in theo_khoa else "khong_thu"
            phu["jobs"]["loi" if tt == "co" else tt] += 1
            khong_do.append({"doi_tuong": f"jobs cua luot {rid} ({wf})", "ly_do": tt, "nguon": f"{API}actions/runs/{rid}/jobs?filter=all"})
            return None
        phu["jobs"]["co"] += 1
        lu = tinh_luot(r, tao, dong)
        lu["nguon"] = f"{API}actions/runs/{rid}/jobs?filter=all"
        return lu

    def log_cua(wf, m, nhan):
        """Tra (trang thai nguon, van ban | None) va cap nhat do phu."""
        o = phu["log_" + nhan]
        o["yeu_cau"] += 1
        tt = trang_thai_nguon(theo_khoa.get(f"log/{m['job_id']}"))
        if tt != "co":
            o[tt] += 1
            chi_tiet = (theo_khoa.get(f"log/{m['job_id']}") or {}).get("loi")
            khong_do.append({"doi_tuong": f"log job {m['job_id']} ({ten_goc(m['ten'])}, ket luan job {m['ket_luan']})",
                             "ly_do": tt + (f" ({chi_tiet})" if chi_tiet else ""), "nguon": f"{API}actions/jobs/{m['job_id']}/logs"})
            return tt, None
        return tt, van_ban(m["job_id"])

    # ── M1
    m1_luot, muc_kq, top_nhom = [], {}, {}
    dk = {}                      # M2b: (nguon, nen, bo) -> {che_do: [giay]} + rc

    def gom_dk(nguon, nen, tr):
        for b in tr["bo"]:
            o = dk.setdefault((nguon, nen, str(b["duong_dan"])), {"che_do": {}, "rc_khac_0": 0, "giay_loai": 0, "so_ban_ghi": 0})
            o["so_ban_ghi"] += 1
            o["rc_khac_0"] += 1 if b["rc"] != 0 else 0
            if b["giay"]["trang_thai"] == DO_DUOC:
                o["che_do"].setdefault(b["che_do"], []).append(b["giay"]["gia_tri"])
            else:
                o["giay_loai"] += 1
                o["che_do"].setdefault(b["che_do"], [])

    so_manh, job_dai_nhat = {}, {}

    def ghi_them(wf, lu):
        """Su kien phu cho M4: (a) job thuc_thi dai nhat cua moi luot; (b) so job ma tran cua luot success mot attempt MOI NHAT co job ay."""
        hl = [m for m in lu["dong"] if m["loai_dong"] == THUC_THI and m["giay"]["trang_thai"] == DO_DUOC]
        if hl:
            j = max(hl, key=lambda m: (m["giay"]["gia_tri"], m["job_id"] or 0))
            bc = [thoi_luong_buoc(b) for b in j["_tho"].get("steps") or []]
            job_dai_nhat[lu["run_id"]] = {"ten": j["ten"], "giay": j["giay"]["gia_tri"], "nguon": lu["nguon"],
                                          "buoc_dai_nhat": max([x["gia_tri"] for x in bc if x["trang_thai"] == DO_DUOC], default=None)}
        if lu["ket_luan"] == "success" and lu["so_attempt"] == 1:
            dem = {}
            for m in lu["dong"]:
                if m["loai_dong"] == THUC_THI and m["ket_luan"] == "success" and m["nen"] == "ubuntu-latest":
                    dem.setdefault(m["ten_goc"], set()).add(m["ten"])
            for ten, tap in dem.items():
                cu = so_manh.get(f"{wf}|{ten}")
                if cu is None or (lu["created_at"], lu["run_id"]) > (cu["created_at"], cu["run_id"]):
                    so_manh[f"{wf}|{ten}"] = {"so": len(tap), "run_id": lu["run_id"], "created_at": lu["created_at"], "nguon": lu["nguon"]}

    def cong_nhom(wf, lu, lan="_"):
        for m in lu["dong"]:
            if m["loai_dong"] == THUC_THI and m["giay"]["trang_thai"] == DO_DUOC:
                top_nhom.setdefault((wf, m["ten_goc"]), []).append(m["giay"]["gia_tri"])

    for r in co_du:
        lu = tinh_mot(WF_DU, r)
        if lu is None:
            m1_luot.append({"run_id": r["id"], "trang_thai": KHONG_DO_DUOC, "ly_do": "khong co du lieu jobs"})
            continue
        cong_nhom(WF_DU, lu)
        ghi_them(WF_DU, lu)
        ds_job, manh_giay = [], []
        for m in lu["dong"]:
            j = {k: m[k] for k in ("job_id", "run_attempt", "ten", "nen", "ket_luan", "loai_dong", "giay", "giay_cho")}
            nhan = can_log(WF_DU, m)
            if m["ten_goc"] == "dot-bien-manh" and m["loai_dong"] == THUC_THI:
                j["buoc"] = {f"{b.get('number')}:{b.get('name')}": thoi_luong_buoc(b) for b in m["_tho"].get("steps") or []}
                if m["giay"]["trang_thai"] == DO_DUOC and m["ket_luan"] == "success":
                    manh_giay.append(m["giay"]["gia_tri"])
            if nhan:
                tt, van = log_cua(WF_DU, m, nhan)
                if van is not None and nhan == "manh":
                    tr = trich_ket_qua(van)
                    o = phu["log_manh"]
                    o["co" if tr["trang_thai_log"] == "co" else tr["trang_thai_log"]] += 1
                    g = [x["giay"]["gia_tri"] for x in tr["muc"] if x["giay"]["trang_thai"] == DO_DUOC]
                    j["log"] = {"trang_thai_log": tr["trang_thai_log"], "mo": tr.get("mo"), "dong": tr.get("dong"), "so_dong_ket_qua": len(tr["muc"]),
                                "tong_giay_muc": thong_ke(g, len(tr["muc"]) - len(g)).get("tong"), "so_muc_khong_ghi_giay": len(tr["muc"]) - len(g)}
                    if tr["trang_thai_log"] != "co":
                        khong_do.append({"doi_tuong": f"log manh job {m['job_id']} luot {r['id']}", "ly_do": tr["trang_thai_log"],
                                         "nguon": f"{API}actions/jobs/{m['job_id']}/logs"})
                    che = (tr.get("mo") or {}).get("che_do") or "khong_ro"
                    for x in tr["muc"]:
                        o2 = muc_kq.setdefault((che, x["khoa"]), {"giay": [], "loai": 0, "khong_passed": 0})
                        o2["khong_passed"] += 1 if x["ket_qua"] != "passed" else 0
                        if x["giay"]["trang_thai"] == DO_DUOC:
                            o2["giay"].append(x["giay"]["gia_tri"])
                        else:
                            o2["loai"] += 1
                elif van is not None and nhan == "dang_ky_du":
                    tr = trich_thoi_gian_dang_ky(van)
                    phu["log_dang_ky_du"]["co" if tr["trang_thai_log"] == "co" else tr["trang_thai_log"]] += 1
                    j["log"] = {"trang_thai_log": tr["trang_thai_log"], "so_bo": len(tr["bo"])}
                    gom_dk("dot-bien-du", m["nen"], tr)
                    if tr["trang_thai_log"] != "co":
                        khong_do.append({"doi_tuong": f"ban ghi CI_DANG_KY_THOI_GIAN job {m['job_id']} luot {r['id']}", "ly_do": tr["trang_thai_log"],
                                         "nguon": f"{API}actions/jobs/{m['job_id']}/logs"})
                elif van is not None:
                    phu["log_khac_du"]["co"] += 1
                elif nhan in ("manh", "dang_ky_du"):
                    j["log"] = {"trang_thai_log": tt}
            ds_job.append(j)
        arts, du_art = doc_trang(f"arts/{r['id']}")
        ds_art = []
        if f"arts/{r['id']}/p1" not in theo_khoa or doc(f"arts/{r['id']}/p1") is None:
            khong_do.append({"doi_tuong": f"danh sach artifact luot {r['id']}", "ly_do": trang_thai_nguon(theo_khoa.get(f"arts/{r['id']}/p1")),
                             "nguon": f"{API}actions/runs/{r['id']}/artifacts"})
        for a in sorted(arts, key=lambda a: a.get("id") or 0):
            if not str(a.get("name", "")).startswith("dot-bien-manh"):
                continue
            o = phu["artifact_manh"]
            o["yeu_cau"] += 1
            ng = f"{API}actions/artifacts/{a.get('id')}/zip"
            ma = {"id": a.get("id"), "ten": a.get("name"), "kich_thuoc": a.get("size_in_bytes"), "het_han": bool(a.get("expired")), "nguon": ng}
            if a.get("expired"):
                o["het_han"] += 1
                ma["noi_dung"] = {"trang_thai": KHONG_DO_DUOC, "ly_do": "artifact het_han (expired=true)"}
            else:
                tt = trang_thai_nguon(theo_khoa.get(f"art/{a.get('id')}"))
                if tt == "co":
                    ma["noi_dung"] = doc_artifact_manh(doc(f"art/{a.get('id')}"))
                    o["co" if ma["noi_dung"]["trang_thai"] == DO_DUOC else "cat_cut"] += 1
                else:
                    o[tt] += 1
                    ma["noi_dung"] = {"trang_thai": KHONG_DO_DUOC, "ly_do": tt}
            if ma["noi_dung"]["trang_thai"] != DO_DUOC:
                khong_do.append({"doi_tuong": f"artifact {a.get('id')} ({a.get('name')}) luot {r['id']}", "ly_do": ma["noi_dung"]["ly_do"], "nguon": ng})
            ds_art.append(ma)
        so_manh_tc = sum(1 for m in lu["dong"] if m["ten_goc"] == "dot-bien-manh" and m["loai_dong"] == THUC_THI and m["ket_luan"] == "success")
        m1_luot.append({"run_id": r["id"], "nguon": lu["nguon"], "created_at": lu["created_at"], "head_sha": lu["head_sha"], "su_kien": lu["su_kien"],
                        "ket_luan": lu["ket_luan"], "so_attempt": lu["so_attempt"], "updated_at_tham_khao": lu["updated_at_tham_khao"],
                        "giay_thuc_thi": lu["giay_thuc_thi"], "dau_cuoi_suy_ra_tu_job": lu["dau_cuoi_suy_ra_tu_job"], "giay_cho": lu["giay_cho"],
                        "so_dong": lu["so_dong"], "so_job_hong_o_attempt_truoc": lu["so_job_hong_o_attempt_truoc"],
                        "du_8_manh_success": so_manh_tc == 8 and lu["ket_luan"] == "success" and lu["so_attempt"] == 1,
                        "giay_job_manh_success": thong_ke(manh_giay), "job": ds_job, "artifact": ds_art})

    def tk_nhom(luot, khoa):
        g = {}
        for lu in luot:
            for m in lu["job"]:
                if m["loai_dong"] == THUC_THI:
                    o = g.setdefault(khoa(m), {"v": [], "loai": 0})
                    if m["giay"]["trang_thai"] == DO_DUOC:
                        o["v"].append(m["giay"]["gia_tri"])
                    else:
                        o["loai"] += 1
        return {k: thong_ke(o["v"], o["loai"]) for k, o in sorted(g.items())}

    m1_co = [x for x in m1_luot if "job" in x]
    du8 = [x for x in m1_co if x["du_8_manh_success"]]
    moi_nhat = max(du8, key=lambda x: (x["created_at"], x["run_id"])) if du8 else None
    m1 = {"nguon": "tep jobs/*, att/*, arts/*, art/*, log/* cua anh chup (danh sach + sha256 o COHORT.json tep_tho); URL tung luot o M1.luot[].nguon",
          "so_luot": len(co_du), "so_luot_co_rerun": sum(1 for x in m1_co if x["so_attempt"] > 1),
          "so_job_hong_o_attempt_truoc": sum(x["so_job_hong_o_attempt_truoc"] for x in m1_co),
          "theo_ket_luan": dem_theo(m1_co, lambda x: str(x["ket_luan"])),
          "theo_job": tk_nhom(m1_co, lambda m: ten_goc(m["ten"]) + " | " + m["nen"]),
          "luot_du_8_manh_success": {"so_luot": len(du8),
                                     "tong_giay_8_job_manh_moi_luot": thong_ke([x["giay_job_manh_success"]["tong"] for x in du8]),
                                     "giay_mot_job_manh": thong_ke([g for x in du8 for g in
                                                                    [m["giay"]["gia_tri"] for m in x["job"] if ten_goc(m["ten"]) == "dot-bien-manh"
                                                                     and m["loai_dong"] == THUC_THI and m["giay"]["trang_thai"] == DO_DUOC]]),
                                     "moi_nhat": None if moi_nhat is None else {
                                         "run_id": moi_nhat["run_id"], "created_at": moi_nhat["created_at"], "nguon": moi_nhat["nguon"],
                                         "giay_job_manh": moi_nhat["giay_job_manh_success"],
                                         "so_muc_theo_log": sum((m.get("log") or {}).get("so_dong_ket_qua") or 0 for m in moi_nhat["job"]),
                                         "so_muc_theo_artifact": sum((a["noi_dung"].get("so_muc") or 0) for a in moi_nhat["artifact"]
                                                                     if a["noi_dung"]["trang_thai"] == DO_DUOC),
                                         "dau_cuoi_suy_ra_tu_job": moi_nhat["dau_cuoi_suy_ra_tu_job"], "giay_thuc_thi": moi_nhat["giay_thuc_thi"]}},
          "muc_ket_qua_theo_khoa": {"cong_thuc": "moi dong KET QUA <khoa>: <kq> (<giay>s) cua log job manh thuc_thi; gom theo (che_do, khoa)",
                                    "so_khoa": len(muc_kq),
                                    "bang": {f"{c} | {k}": dict(thong_ke(o["giay"], o["loai"]), khong_passed=o["khong_passed"])
                                             for (c, k), o in sorted(muc_kq.items())}},
          "luot": m1_luot}

    # ── M2
    m2_luot, job_g, buoc_g, cc_nhanh, cc_luot = [], {}, {}, {"bo_qua": 0, "thuc_thi": 0, "mang_sang": 0}, []
    nhanh_luot = {}
    for r in co_ci:
        lu = tinh_mot(WF_CI, r)
        if lu is None:
            m2_luot.append({"run_id": r["id"], "trang_thai": KHONG_DO_DUOC, "ly_do": "khong co du lieu jobs"})
            continue
        lan, co_cb = None, False
        for m in lu["dong"]:
            if can_log(WF_CI, m) == "chuan_bi":
                co_cb = True
                tt, van = log_cua(WF_CI, m, "chuan_bi")
                if van is not None:
                    x = trich_lan(van)
                    phu["log_chuan_bi"]["co" if x else "khong_co_ban_ghi"] += 1
                    lan = x or lan
        lan_gt = gt(lan) if lan else kdd("khong co job chuan-bi thuc_thi" if not co_cb else "log chuan-bi thieu/khong co dong che_do=")
        lan_k = lan or "khong_do_duoc"
        cong_nhom(WF_CI, lu)
        ghi_them(WF_CI, lu)
        nhanh_luot.setdefault(str(r.get("head_branch")), []).append({
            "run_id": r["id"], "created_at": lu["created_at"],
            "cc": dem_theo([m for m in lu["dong"] if m["ten_goc"] == "gate-cong-cu" and m["loai_dong"] == THUC_THI and m["nen"] != "khong_ro"],
                           lambda m: str(m["ket_luan"]))})
        if lan == "duong_nhanh":
            co_runner = lambda m: "thuc_thi_khong_runner" if m["loai_dong"] == THUC_THI and m["nen"] == "khong_ro" else m["loai_dong"]
            cc_luot.append({"run_id": r["id"], "created_at": lu["created_at"],
                            "cc": dem_theo([m for m in lu["dong"] if m["ten_goc"] == "gate-cong-cu"], co_runner),
                            "gop": dem_theo([m for m in lu["dong"] if m["ten_goc"] == "gate-cong-cu-gop"],
                                            lambda m: f"{co_runner(m)}:{m['ket_luan']}")})
        for m in lu["dong"]:
            if m["ten_goc"] == "gate-cong-cu" and lan == "duong_nhanh":
                cc_nhanh[m["loai_dong"]] = cc_nhanh.get(m["loai_dong"], 0) + 1
            if not m["ten_goc"].startswith("gate"):
                continue
            kj = (m["ten_goc"], m["nen"] if m["loai_dong"] == THUC_THI else "_", lan_k)
            o = job_g.setdefault(kj, {"v": [], "loai": 0, BO_QUA: 0, MANG_SANG: 0, "ket_luan": {}})
            if m["loai_dong"] == THUC_THI:
                o["ket_luan"][str(m["ket_luan"])] = o["ket_luan"].get(str(m["ket_luan"]), 0) + 1
                if m["giay"]["trang_thai"] == DO_DUOC:
                    o["v"].append(m["giay"]["gia_tri"])
                else:
                    o["loai"] += 1
                    khong_do.append({"doi_tuong": f"thoi luong job {m['job_id']} ({m['ten_goc']}) luot {r['id']}", "ly_do": m["giay"]["ly_do"], "nguon": lu["nguon"]})
                if m["ten_goc"].startswith(JOB_BUOC):
                    for b in m["_tho"].get("steps") or []:
                        ob = buoc_g.setdefault((m["ten_goc"], m["nen"], lan_k, str(b.get("name"))), {"v": [], "loai": 0, "kad": 0})
                        tb = thoi_luong_buoc(b)
                        if tb["trang_thai"] == DO_DUOC:
                            ob["v"].append(tb["gia_tri"])
                        elif tb["trang_thai"] == KHONG_AP_DUNG:
                            ob["kad"] += 1
                        else:
                            ob["loai"] += 1
                if can_log(WF_CI, m) == "dang_ky_ci":
                    tt, van = log_cua(WF_CI, m, "dang_ky_ci")
                    if van is not None:
                        tr = trich_thoi_gian_dang_ky(van)
                        phu["log_dang_ky_ci"]["co" if tr["trang_thai_log"] == "co" else tr["trang_thai_log"]] += 1
                        gom_dk("gate-registry", m["nen"], tr)
                        if tr["trang_thai_log"] != "co":
                            khong_do.append({"doi_tuong": f"ban ghi CI_DANG_KY_THOI_GIAN job {m['job_id']} luot {r['id']} (ket luan job {m['ket_luan']})",
                                             "ly_do": tr["trang_thai_log"], "nguon": f"{API}actions/jobs/{m['job_id']}/logs"})
            elif m["loai_dong"] in (BO_QUA, MANG_SANG):
                o[m["loai_dong"]] += 1
        rec = {"run_id": r["id"], "nguon": lu["nguon"], "created_at": lu["created_at"], "su_kien": lu["su_kien"], "ket_luan": lu["ket_luan"], "so_attempt": lu["so_attempt"],
               "lan": lan_gt, "giay_thuc_thi": lu["giay_thuc_thi"], "dau_cuoi_suy_ra_tu_job": lu["dau_cuoi_suy_ra_tu_job"],
               "giay_cho": {k: lu["giay_cho"].get(k) for k in ("n", "trung_vi", "lon_nhat", "so_loai")},
               "updated_at_tham_khao": lu["updated_at_tham_khao"], "so_dong": lu["so_dong"],
               "so_job_hong_o_attempt_truoc": lu["so_job_hong_o_attempt_truoc"], "co": [k for k in ("cancelled", "failure") if lu["ket_luan"] == k]}
        m2_luot.append(rec)
    m2_co = [x for x in m2_luot if "giay_thuc_thi" in x]

    def tk_luot(ds):
        f = lambda k: thong_ke([x[k]["gia_tri"] for x in ds if x[k]["trang_thai"] == DO_DUOC], sum(1 for x in ds if x[k]["trang_thai"] != DO_DUOC))
        return {"so_luot": len(ds), "giay_thuc_thi": f("giay_thuc_thi"), "dau_cuoi_suy_ra_tu_job": f("dau_cuoi_suy_ra_tu_job"),
                "giay_cho_trung_vi_moi_luot": thong_ke([x["giay_cho"]["trung_vi"] for x in ds if x["giay_cho"].get("trung_vi") is not None])}

    nhom_luot = {}
    for x in m2_co:
        nhom_luot.setdefault(f"{x['su_kien']} | {x['lan']['gia_tri'] or 'khong_do_duoc'}", []).append(x)
    m2 = {"so_luot": len(co_ci), "so_luot_co_rerun": sum(1 for x in m2_co if x["so_attempt"] > 1),
          "so_job_hong_o_attempt_truoc": sum(x["so_job_hong_o_attempt_truoc"] for x in m2_co),
          "theo_ket_luan": dem_theo(m2_co, lambda x: str(x["ket_luan"])),
          "theo_lan": dem_theo(m2_co, lambda x: x["lan"]["gia_tri"] or "khong_do_duoc"),
          "moi_luot": {"tat_ca": tk_luot(m2_co), "theo_su_kien_va_lan": {k: tk_luot(v) for k, v in sorted(nhom_luot.items())}},
          "nguon": "tep jobs/*, att/*, log/* cua anh chup (danh sach + sha256 o COHORT.json tep_tho); URL tung luot o M2.luot[].nguon",
          "theo_job": {"khoa": "job goc | nen | lan", "cong_thuc": "completed_at - started_at cua dong thuc_thi; nen cua dong bo_qua/mang_sang ghi '_'",
                       "bang": {" | ".join(k): dict(thong_ke(o["v"], o["loai"]), so_bo_qua=o[BO_QUA], so_mang_sang=o[MANG_SANG],
                                                    ket_luan=dict(sorted(o["ket_luan"].items()))) for k, o in sorted(job_g.items())}},
          "theo_buoc": {"khoa": "job goc | nen | lan | ten buoc", "cong_thuc": "completed_at - started_at cua buoc trong dong thuc_thi; skipped = khong_ap_dung",
                        "bang": {" | ".join(k): dict(thong_ke(o["v"], o["loai"]), so_khong_ap_dung=o["kad"]) for k, o in sorted(buoc_g.items())}},
          "gate_cong_cu_o_luot_duong_nhanh": cc_nhanh,
          "luot": m2_luot}

    # ── M2b
    m2b = {"cong_thuc": "moi phan tu `bo` cua ban ghi CI_DANG_KY_THOI_GIAN; gom theo (job nguon | nen | bo), tach che_do; chi tinh giay do_duoc",
           "nguon": ".claude/dev/ci_dang_ky_test.py:1335,2982@" + sha[:12] + " + log job trong anh chup",
           "bang": {}}
    for (ng, nen, bo), o in sorted(dk.items()):
        m2b["bang"][f"{ng} | {nen} | {bo}"] = {"so_ban_ghi": o["so_ban_ghi"], "rc_khac_0": o["rc_khac_0"], "giay_bi_loai": o["giay_loai"],
                                              "che_do": {c: thong_ke(v) for c, v in sorted(o["che_do"].items())}}

    # ── M3, M4
    b_m3, b_bl, b_pr = doc("kho/m3_import.json"), doc("kho/blame.json"), doc("kho/pr_nhanh.json")
    tho_m3 = json.loads(b_m3) if b_m3 else None
    m3 = m3_tu_anh_chup(tho_m3, sha)
    bo_m3 = (tho_m3 or {}).get("bo") or {}
    win = [v for (ten, nen, _), o in job_g.items() if ten == "gate-cong-cu" and nen == "windows-latest" for v in o["v"]]
    tep_kho = {k[len("kho/tep/"):]: doc(k).decode("utf-8", errors="replace") for k in sorted(theo_khoa) if k.startswith("kho/tep/") and doc(k) is not None}
    m4 = m4_doi_chieu(m4_quet(tep_kho), {
        "sha": sha, "m3": {t: {n: x["gia_tri"] for n, x in bg.items() if x["trang_thai"] == DO_DUOC} for t, bg in m3["bang"].items()},
        "moi_nhat_du": m1["luot_du_8_manh_success"]["moi_nhat"], "so_manh": so_manh, "luot_nhanh": cc_luot,
        "cc_ca_cohort": m2["gate_cong_cu_o_luot_duong_nhanh"], "blame": json.loads(b_bl) if b_bl else None, "job_dai_nhat": job_dai_nhat,
        "co_tep_kho": bool(tep_kho),
        "m3_ten": {t: x.get("ten") or {} for t, x in bo_m3.items()}, "m3_hang_so": {t: x.get("hang_so") or {} for t, x in bo_m3.items()},
        "pr_nhanh": json.loads(b_pr) if b_pr else None, "nhanh_luot": nhanh_luot,
        "cc_windows": {"so_dong": len(win), "giay_lon_nhat": max(win) if win else None},
        "ma_tran_pldb": doc_ma_tran_manh(tep_kho.get(M4_PLDB))})

    # ── top 5
    top = sorted(({"workflow": wf, "job_goc": ten, "tong_giay_thuc_thi": sum(v), "so_dong_thuc_thi": len(v),
                   "trung_vi_giay": thong_ke(v)["trung_vi"], "trang_thai": DO_DUOC,
                   "nguon": f"tong completed_at - started_at cua moi dong thuc_thi ten goc nay trong cohort (tep jobs/* cua anh chup)"}
                  for (wf, ten), v in top_nhom.items()), key=lambda x: (-x["tong_giay_thuc_thi"], x["workflow"], x["job_goc"]))[:5]

    khong_do.sort(key=lambda x: (x["doi_tuong"], x["ly_do"]))
    kdd_tom = {}
    for x in khong_do:
        nh = re.sub(r"\d{6,}", "<id>", x["doi_tuong"]) + " — " + str(x["ly_do"])
        kdd_tom[nh] = kdd_tom.get(nh, 0) + 1
    base_meta = {"packet": "wp1434", "revision": 3, "spec_sha256": meta["spec_sha256"], "kho": meta["kho"], "T0": meta["T0"], "T1": meta["T1"],
                 "sha_master": sha, "lenh_sha_master": meta.get("lenh_sha_master"), "khoang_con": meta["khoang_con"],
                 "liet_ke_du": meta.get("liet_ke_du"), "manifest_sha256": sha256_bytes(b_man),
                 "cohort": {WF_DU: {"so_luot": len(co_du), "so_cap_run_attempt": sum(int(r.get("run_attempt") or 1) for r in co_du),
                                    "bi_loai": dem_theo(loai_du, lambda x: x[1])},
                            WF_CI: {"so_luot": len(co_ci), "so_cap_run_attempt": sum(int(r.get("run_attempt") or 1) for r in co_ci),
                                    "bi_loai": dem_theo(loai_ci, lambda x: x[1])}},
                 "quy_tac": QUY_TAC}
    baseline = {"meta": base_meta, "do_phu": phu, "M1": m1, "M2": m2, "M2b": m2b, "M3": m3, "M4": m4, "top5_giay_thuc_thi": top,
                "khong_do_duoc": {"so_muc": len(khong_do), "tom_tat": dict(sorted(kdd_tom.items())), "chi_tiet": khong_do}}
    cohort = {"meta": {k: base_meta[k] for k in ("packet", "revision", "spec_sha256", "kho", "T0", "T1", "sha_master", "khoang_con", "manifest_sha256")},
              "cap_run_attempt": {WF_DU: [[r["id"], k] for r in co_du for k in range(1, int(r.get("run_attempt") or 1) + 1)],
                                  WF_CI: [[r["id"], k] for r in co_ci for k in range(1, int(r.get("run_attempt") or 1) + 1)]},
              "bi_loai": {WF_DU: sorted(map(list, loai_du), key=str), WF_CI: sorted(map(list, loai_ci), key=str)},
              "tep_tho": [[m["khoa"], m.get("sha256"), m.get("kich_thuoc"), m.get("http"), m.get("url") or m.get("nguon")] + ([m["loi"]] if m.get("loi") else [])
                          for m in manifest]}
    ra.mkdir(parents=True, exist_ok=True)
    b_base = (xuat_json(baseline, 4) + "\n").encode("utf-8")
    ghi_tep(ra, "BASELINE.json", b_base)
    ghi_tep(ra, "COHORT.json", (xuat_json(cohort, 2) + "\n").encode("utf-8"))
    ghi_tep(ra, "BAO_CAO.md", bao_cao(baseline, cohort).encode("utf-8"))
    print("BASELINE.json sha256", sha256_bytes(b_base))
    return 0


def dem_theo(ds, khoa):
    o = {}
    for x in ds:
        o[khoa(x)] = o.get(khoa(x), 0) + 1
    return dict(sorted(o.items()))


QUY_TAC = {
    "phan_loai_dong": "theo thu tu: (a) conclusion==skipped -> bo_qua (thoi luong khong_ap_dung, chi dem); (b) mang_sang neu job_id da xuat hien o "
                      "attempt truoc HOAC started_at < created_at cua attempt chua dong; (c) con lai -> thuc_thi (gom job hong/huy da chay)",
    "giay_thuc_thi": "tong completed_at - started_at cua dong thuc_thi hop le, moi attempt; dong thieu moc/dao bi loai va dem o so_dong_loai",
    "dau_cuoi_suy_ra_tu_job": "max(completed_at) cua dong thuc_thi hop le o attempt cuoi TRU created_at cua attempt 1; KHONG dung updated_at cua run "
                              "(chi ghi kem updated_at_tham_khao); attempt cuoi khong co dong thuc_thi hop le -> khong_do_duoc",
    "giay_cho": "started_at - created_at cua tung dong thuc_thi",
    "ba_trang_thai": "0 la do_duoc; skipped/khong ton tai -> khong_ap_dung; thieu moc, thoi gian dao, het han, cat cut, loi API -> khong_do_duoc "
                     "(khong thay bang 0, khong kep am ve 0)",
    "thong_ke": "chi tren phan do_duoc; trung_vi = statistics.median; p90 = sorted[ceil(0.9*n)-1]; so_loai = so phan tu bi loai",
    "lan": "doc tu log job chuan-bi thuc_thi: dong `che_do=duong_nhanh|day_du` cuoi cung; khong co thi dong `DUONG_NHANH: khong phan loai - ... luon DAY_DU` "
           "-> day_du; khong co ca hai hoac thieu log -> khong_do_duoc (KHONG suy tu gia tri mac dinh cua workflow)",
    "nen": "nhan runner cua dong job (labels); `khong_ro` = labels rong (job bi huy truoc khi duoc cap runner)",
    "M3": "so phan tu CUOI CUNG cua bang (len() sau khi module import xong, gom .update/gan chi so/append), doc o buoc su kien kho cua --thu trong tien "
          "trinh con KHONG chay bo (ten module khac __main__); --tinh chi doc kho/m3_import.json cua anh chup; khong import duoc -> khong_do_duoc",
    "M4": "moi dong khop hai regex o tep kho/tep/* cua anh chup; loi khai co phep do trong M1-M3 duoc so (khop|lech); khong_do_duoc CHI khi thieu mot "
          "nguon cu the, ghi o ly_do ('nguon thieu: ...'); dong khong phai loi khai ghi rieng o M4.dong_khong_phai_loi_khai",
    "rerun": "so_luot_co_rerun = so luot co run_attempt > 1; so_job_hong_o_attempt_truoc = so dong thuc_thi conclusion==failure o attempt < attempt cuoi "
             "(KHONG goi la flaky)",
}


M4_CI, M4_DU, M4_NHANH = ".github/workflows/ci.yml", ".github/workflows/ci-dot-bien-du.yml", "ops/nhanh_don_duoc_test.py"
# (regex co nhom so, bang cua ops/nhanh_don_duoc_test.py, nhan) — ap cho hai workflow cua cohort
M4_DEM = ((r"(\d+) ca (?:nền|dưới MỖI)", "TU_KIEM", "ca"), (r"(\d+) tự đột biến", "DOT_BIEN_TU_KIEM", "tu dot bien"),
          (r"(\d+) đột biến sản phẩm", "DOT_BIEN", "dot bien san pham"))
# (tep, regex co nhom so manh, workflow, job goc)
M4_MANH = ((M4_DU, r"(\d+) mảnh ≈", WF_DU, "dot-bien-manh"),
           (M4_CI, r"`gate-cong-cu` \((\d+) mảnh\)", WF_CI, "gate-cong-cu"),
           (M4_CI, r"chia (\d+) mảnh chạy song song", WF_CI, "gate-cong-cu"),
           (M4_CI, r"chia (\d+) mảnh cân theo chi phí", WF_CI, "gate-nhanh-manh"),
           (M4_CI, r"(\d+) mảnh chạy \(sổ ca", WF_CI, "gate-packet-loop-manh"))
# (tien to tep, chuoi trong dong | None = moi dong cua tep, NGUON THIEU cu the)
M4_NGUON_THIEU = (
    ("docs/AUDIT_LAUNCHER_", None, "dau ra cua luot chay launcher_test tai thoi diem audit (bien ban co ngay): khong luu trong kho hay anh chup, packet khong chay bo"),
    ("docs/adr/0009-", None, "ket qua thuc nghiem dot bien tay ngay 2026-07-20: khong co log trong kho hay anh chup"),
    ("CLAUDE.md", "**40/40**", "dau ra bo test ops-don-ref tai thoi diem su co (bai hoc lich su): khong luu"),
    ("CLAUDE.md", "`|  | 0/0`", "dau ra chay_dot_bien cua packet #513 (12-09-2026): khong luu"),
    ("CLAUDE.md", "(105 ca;", "so ca cua ops/don_ref_chot_test.sh chi sinh khi CHAY script (khong co bang tinh; packet khong chay)"),
    (M4_CI, "~93 % bước này, ~43 phút", "luot do truoc #668 (28-09-2026) tao truoc T0: khong thuoc cohort"),
    (M4_CI, "111/118 lượt mảnh Windows", "cac luot manh Windows truoc wp879 (#853) tao truoc T0: khong thuoc cohort"),
    (".github/workflows/packet-loop-dot-bien.yml", "(~45 phút)", "thoi luong luot cua packet-loop-dot-bien.yml: workflow khong thuoc cohort (dac ta §2 chi dinh hai workflow)"),
)
# (tien to tep, chuoi trong dong, vi sao KHONG phai loi khai so luong/thoi gian ve dot bien)
M4_KHONG_PHAI = (
    (M4_CI, "- name: G5 manh ban kinh dot bien (#668)", "ten buoc; con so la ma issue"),
    ("CLAUDE.md", "`=duong_nhanh, 0 mảnh`", "trich dau rieng cua mot dong log, khong phai loi khai so luong"),
    ("docs/adr/0062-", "0/1/≥2", "ba trang thai dong khai cua kiem-merge, khong phai so dot bien"),
)
M4_PHAMVI = ".github/checks/ci_phamvi_test.py"
M4_PLDB = ".github/workflows/packet-loop-dot-bien.yml"
M4_RE_BO = re.compile(r"((?:[\w.-]+/)*[\w.-]*\w_test\.py)\b[^\n]*?\b(\d+) đột biến")
M4_RE_RUN = re.compile(r"(\d+)m(\d+)s \(run (\d+)\)")


def m4_doi_chieu(dong, do):
    """dong = [(tep, so dong, van ban)]; do = cac phep do (xem lenh_tinh). Moi loi khai -> khop | lech | khong_do_duoc (kem 'nguon thieu: ...').
    Thu tu: dong khong phai loi khai -> loai rieng; con lai ap MOI quy tac tong quat + bang nguon thieu; khong quy tac nao -> dem `so_dong_chua_anh_xa`."""
    sha12 = do["sha"][:12]
    m3 = do.get("m3") or {}
    mn = do.get("moi_nhat_du")
    blame = (do.get("blame") or {}).get("dong") if do.get("blame") else None
    kq, khong_phai, chua = [], [], 0

    def thieu(nhan, ly):
        return (nhan, None, KHONG_DO_DUOC, "nguon thieu: " + ly)

    def so_sanh(nhan, khai, do_duoc, ghi):
        return (nhan, do_duoc, "khop" if do_duoc == khai else "lech", ghi)

    def moc(tep, so):
        x = (blame or {}).get(f"{tep}:{so}")
        return gio(x["committer_time"]) if x else None

    def c_thoi_gian():
        if not mn:
            return [thieu("~73 800 s noi tiep; ≈ 2,6 h/manh", "khong co luot du 8 manh success trong cohort")]
        t, tb = mn["giay_job_manh"]["tong"], mn["giay_job_manh"]["trung_vi"]
        ng = f"luot {mn['run_id']} (luot du 8 manh success moi nhat cua cohort): {mn['nguon']}"
        gan = lambda khai, v: "khop" if abs(v - khai) <= 0.2 * khai else "lech"
        return [("~73 800 s noi tiep", f"{t} s = tong 8 job manh", gan(73800, t), "khop neu trong ±20% (loi khai dang '~'); " + ng),
                ("≈ 2,6 h/manh (9 360 s)", f"{tb} s = trung vi 8 job manh ({mn['giay_job_manh']['nho_nhat']}–{mn['giay_job_manh']['lon_nhat']} s)",
                 gan(9360, tb), "khop neu trong ±20%; " + ng)]

    def sau_moc(tep, so, nhan):
        m = moc(tep, so)
        if m is None:
            return None, [thieu(nhan, f"kho/blame.json cua anh chup khong co dong {tep}:{so} (khong biet luc dong vao nhanh)")]
        sau = [x for x in do.get("luot_nhanh") or [] if gio(x["created_at"]) is not None and gio(x["created_at"]) > m]
        if not sau:
            return None, [thieu(nhan, f"khong co luot duong_nhanh nao tao sau {iso(m)} trong cohort")]
        return (m, sau), None

    def cong(sau, khoa):
        tong = {}
        for x in sau:
            for k, n in x[khoa].items():
                tong[k] = tong.get(k, 0) + n
        return dict(sorted(tong.items()))

    def c_skip(tep, so):
        nhan = "8 manh skipped (0 phut runner) o duong_nhanh"
        d, loi = sau_moc(tep, so, nhan)
        if loi:
            return loi
        tong = cong(d[1], "cc")
        return [(nhan, f"{len(d[1])} luot duong_nhanh tao sau {iso(d[0])}: dong gate-cong-cu {tong}; ca cohort: {do.get('cc_ca_cohort')}",
                 "khop" if tong.get(THUC_THI, 0) == 0 else "lech",
                 "chi tinh luot tao SAU committer-time first-parent cua dong loi khai (kho/blame.json); khop neu khong dong gate-cong-cu nao la thuc_thi CO "
                 "runner (thuc_thi_khong_runner = bi huy truoc khi duoc cap runner, khong phai skipped); lan doc tu log chuan-bi")]

    def c_gop(tep, so):
        nhan = "gate-cong-cu-gop o duong_nhanh: XANH, khong skipped"
        d, loi = sau_moc(tep, so, nhan)
        if loi:
            return loi
        tong = cong(d[1], "gop")
        la_xau = lambda k: k.startswith(BO_QUA) or k == f"{THUC_THI}:failure"
        xau = sum(n for k, n in tong.items() if la_xau(k))
        luot_xau = sorted(x["run_id"] for x in d[1] if any(la_xau(k) for k in x["gop"]))
        return [(nhan, f"{len(d[1])} luot duong_nhanh tao sau {iso(d[0])}: dong gate-cong-cu-gop theo loai:ket_luan {tong}; luot co dong bo_qua/failure: {luot_xau}",
                 "khop" if xau == 0 else "lech",
                 "chi tinh luot tao SAU committer-time first-parent cua dong loi khai (kho/blame.json); khop neu khong dong nao la bo_qua va khong dong "
                 "thuc_thi co runner nao failure")]

    def c_run(rid, nhan, khai_phut=None, khai_giay=None):
        j = (do.get("job_dai_nhat") or {}).get(rid)
        if j is None:
            return [thieu(nhan, f"jobs cua luot {rid} khong co trong anh chup (luot khong thuoc cohort [T0, T1])")]
        g = j["giay"]
        mo_ta = f"job dai nhat cua luot {rid} ({j['ten']}): {g} s = {g // 3600} gio {g % 3600 // 60} phut {g % 60} giay; buoc dai nhat cua job ay: {j['buoc_dai_nhat']} s"
        if khai_phut is not None:
            return [(nhan, mo_ta, "khop" if khai_phut in (g // 60, round(g / 60)) else "lech",
                     f"khop neu thoi luong JOB cat hoac lam tron ve phut bang {khai_phut} phut; {j['nguon']}")]
        return [(nhan, mo_ta, "khop" if g == khai_giay else "lech", f"khop neu thoi luong job dai nhat bang {khai_giay} s; {j['nguon']}")]

    def c_phamvi():
        nhan = "ci_phamvi_test: 6 dot bien (ca phan chung n*)"
        ten = ((do.get("m3_ten") or {}).get(M4_PHAMVI) or {}).get("CA")
        if ten is None:
            return [thieu(nhan, f"M3 khong co danh sach ten phan tu cua bang CA trong {M4_PHAMVI}")]
        n = sorted(x for x in ten if re.match(r"n\d+_", x))
        return [so_sanh(nhan, 6, len(n), f"so phan tu cua CA trong {M4_PHAMVI}@{sha12} co ten dang n<so>_ (ca dot bien/phan chung; con lai la ca nen "
                                         f"{sorted(set(ten) - set(n))}); doc ten bang import giam giu, khong chay: {n}")]

    def c_pr_895():
        kq1 = "PR #895: CI do 8/8 manh gate-cong-cu"
        thieu_log = "log job gate-cong-cu cua luot do (dac ta §4: voi ci.yml chi thu log gate-registry va chuan-bi)"
        ra2 = []
        x = ((do.get("pr_nhanh") or {}).get("pr") or {}).get("895") if do.get("pr_nhanh") else None
        if not x:
            ra2.append(thieu(kq1, "kho/pr_nhanh.json cua anh chup khong co anh xa PR #895 -> nhanh"))
        else:
            ds = sorted((do.get("nhanh_luot") or {}).get(x["nhanh"]) or [], key=lambda y: (y["created_at"], y["run_id"]))
            if not ds:
                ra2.append(thieu(kq1, f"cohort khong co luot ci.yml nao tren nhanh {x['nhanh']} (nhanh cua PR #895 theo merge commit {x['commit'][:12]})"))
            else:
                do8 = [y["run_id"] for y in ds if y["cc"] == {"failure": 8}]
                ra2.append((kq1, f"nhanh {x['nhanh']} (merge commit {x['commit'][:12]}): {len(ds)} luot trong cohort, dong gate-cong-cu thuc_thi co runner theo ket luan: "
                                 + "; ".join(f"{y['run_id']} ({y['created_at']}) {y['cc']}" for y in ds) + f"; luot 8/8 failure: {do8}",
                            "khop" if do8 else "lech", "khop neu co it nhat mot luot cua nhanh ay co dung 8 dong gate-cong-cu thuc_thi, ca 8 failure; "
                                                       "anh xa PR -> nhanh tu kho/pr_nhanh.json (git log --first-parent)"))
        ra2.append(thieu("26 va 28 loi ban kinh o hai manh doc duoc", thieu_log))
        ra2.append(thieu("13/13 giet dung t52", "dau ra luot dot bien tai cho cua executor packet #892 (23-10-2026): khong luu trong kho hay anh chup"))
        return ra2

    def tham_khao(t, mau):
        if t == "docs/AUDIT_LAUNCHER_":
            b = m3.get(".claude/dev/launcher_test.py") or {}
            return f"; tham khao, KHONG so (bien ban ghi so cua ngay audit): bang hien hanh DOT_BIEN={b.get('DOT_BIEN')}, CA={b.get('CA')} (M3)"
        if mau == "111/118 lượt mảnh Windows":
            return f"; tham khao, KHONG so (mau so 118 luot nam truoc T0): dong gate-cong-cu thuc_thi tren windows-latest trong cohort: {do.get('cc_windows')}"
        return ""

    for tep, so, van in dong:
        vt = f"{tep}:{so}@{sha12}"
        kp = [ly for t, mau, ly in M4_KHONG_PHAI if tep.startswith(t) and mau in van]
        if kp:
            khong_phai.append({"vi_tri": vt, "trich": van[:200], "ly_do": kp[0]})
            continue
        ra = []
        if tep in (M4_CI, M4_DU):
            for mau, bang, nhan in M4_DEM:
                for m in re.finditer(mau, van):
                    v = (m3.get(M4_NHANH) or {}).get(bang)
                    ra.append(thieu(f"{m.group(1)} {nhan}", f"M3 khong co bang {bang} cua {M4_NHANH}") if v is None else
                              so_sanh(f"{m.group(1)} {nhan}", int(m.group(1)), v, f"len({bang}) cuoi cung cua {M4_NHANH}@{sha12} (M3, import)"))
        for m in M4_RE_BO.finditer(van):
            ten, khai = m.group(1), int(m.group(2))
            ung = sorted(t for t in m3 if t == ten or t.endswith("/" + ten))
            nhan = f"{ten}: {khai} dot bien"
            if len(ung) != 1:
                ra.append(thieu(nhan, f"M3 khong co (hoac co {len(ung)}) bo test khop ten {ten!r}"))
                continue
            bang = next((b for b in ("DOT_BIEN", "MUTANTS", "MUTATIONS") if b in m3[ung[0]]), None)
            ra.append(thieu(nhan, f"M3 khong co bang DOT_BIEN/MUTANTS/MUTATIONS cua {ung[0]}") if bang is None else
                      so_sanh(nhan, khai, m3[ung[0]][bang], f"len({bang}) cuoi cung cua {ung[0]}@{sha12} (M3, import)"))
        for t, mau, wf, job in M4_MANH:
            m = re.search(mau, van) if t == tep else None
            if m:
                d = (do.get("so_manh") or {}).get(f"{wf}|{job}")
                nhan = f"{job}: {m.group(1)} manh"
                ra.append(thieu(nhan, f"cohort khong co luot success mot attempt nao co job {job} thuc_thi tren ubuntu-latest") if d is None else
                          so_sanh(nhan, int(m.group(1)), d["so"], f"so job ma tran {job} thuc_thi success (ubuntu-latest) o luot success mot attempt moi nhat "
                                                                  f"co job ay: luot {d['run_id']} ({d['created_at']}); {d['nguon']}"))
        if tep == M4_DU and "73 800 s" in van:
            ra += c_thoi_gian()
        if tep == M4_CI and "8 mảnh `skipped` (0 phút runner)" in van:
            ra += c_skip(tep, so)
        if tep == M4_CI and "0 mảnh nó in \"KHÔNG ĐO\" và XANH, không `skipped`" in van:
            ra += c_gop(tep, so)
        for m in M4_RE_RUN.finditer(van):
            ra += c_run(int(m.group(3)), f"{m.group(1)}m{m.group(2)}s (run {m.group(3)})", khai_giay=int(m.group(1)) * 60 + int(m.group(2)))
        if tep == M4_CI and "đo run 43845962754: một job 2 giờ" in van:
            ra += c_run(43845962754, "run 43845962754: mot job 2 gio 21 phut (loi khai trai hai dong)", khai_phut=141)
        if tep == M4_CI and "6 dot bien tren `git worktree`" in van:
            ra += c_phamvi()
        m = re.search(r"đường găng <= (\d+) s", van) if tep == M4_CI else None
        if m:
            v = ((do.get("m3_hang_so") or {}).get(M4_NHANH) or {}).get("TRAN_DUONG_GANG_GIAY")
            nhan = f"duong gang <= {m.group(1)} s (nguong cua buoc gom)"
            ra.append(thieu(nhan, f"M3 khong co hang so TRAN_DUONG_GANG_GIAY cua {M4_NHANH}") if v is None else
                      so_sanh(nhan, int(m.group(1)), v, f"hang so TRAN_DUONG_GANG_GIAY cua {M4_NHANH}@{sha12} (M3, import): loi khai la NGUONG cua cong, so voi "
                                                        "nguong trong ma; duong gang thuc te cua tung luot nam o bien nhan gate-nhanh (ngoai nguon thu §4)"))
        if tep == "CLAUDE.md" and "8/8 mảnh (26 và 28" in van:
            ra += c_pr_895()
        m = re.search(r"k % (\d+) == j", van) if tep == M4_PLDB else None
        if m:
            v = do.get("ma_tran_pldb")
            nhan = f"packet-loop-dot-bien: {m.group(1)} manh (k % {m.group(1)})"
            ra.append(thieu(nhan, f"anh chup khong co ma tran `manh: [...]` doc duoc trong kho/tep/{M4_PLDB}") if v is None else
                      so_sanh(nhan, int(m.group(1)), v, f"so phan tu cua `matrix.manh` trong kho/tep/{M4_PLDB} (tep workflow o {sha12}; doc tinh, khong can luot chay)"))
        for t, mau, ly in M4_NGUON_THIEU:
            if tep.startswith(t) and (mau is None or mau in van):
                ra.append(thieu(mau or "(ca dong)", ly + tham_khao(t, mau)))
        if not ra:
            chua += 1
            ra.append(thieu("(chua anh xa)", "chua co quy tac anh xa cho dong nay"))
        for nhan, v, kl, ghi in ra:
            kq.append({"vi_tri": vt, "trich": van[:200], "loi_khai": nhan, "so_do": v, "ket_luan": kl, "ly_do": ghi})
    return {"lenh": M4_LENH, "regex_1": M4_RG1, "regex_2": M4_RG2, "trang_thai_nguon": "co" if do.get("co_tep_kho") else "anh chup thieu kho/tep/*",
            "so_dong_khop": len(dong), "so_dong_khong_phai_loi_khai": len(khong_phai), "so_dong_chua_anh_xa": chua,
            "theo_ket_luan": dem_theo(kq, lambda x: x["ket_luan"]), "loi_khai": kq, "dong_khong_phai_loi_khai": khong_phai}


def phan_loai_s6():
    """Dac ta §6: hai bo phan loai tren tap duong dan cua packet (cac tep duoi ops/specs/wp1434-r3/do/). Chi goi ham thuan/doc cay."""
    import importlib.util
    tap = sorted({p.relative_to(ROOT).as_posix() for p in DAY.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
                 | {(DAY / t).relative_to(ROOT).as_posix() for t in ("COHORT.json", "BASELINE.json", "BAO_CAO.md")})
    kq = {"tap_duong_dan": tap}
    try:
        def nap(ten, tep):
            s = importlib.util.spec_from_file_location(ten, ROOT / tep)
            m = importlib.util.module_from_spec(s)
            sys.modules[ten] = m
            goc = sys.dont_write_bytecode
            sys.dont_write_bytecode = True
            try:
                s.loader.exec_module(m)
            finally:
                sys.dont_write_bytecode = goc
            return m
        dn = nap("wp1434_ci_duong_nhanh", "ops/ci_duong_nhanh.py")
        che_do, ly = dn.phan_loai_tu_diff(set(tap))
        kq["phan_loai_tu_diff"] = [che_do, ly]
        kq["ly_do_ve_day_du"] = dn.ly_do_ve_day_du(set(tap), {t: [("000000", "100644", "A")] for t in tap})
        kq["phan_loai_packet_loop"] = list(dn.phan_loai_packet_loop("pull_request", set(tap)))
    except Exception as e:
        kq["ci_duong_nhanh"] = f"khong_do_duoc ({type(e).__name__}: {e})"
    try:
        dk = nap("wp1434_ci_dang_ky", ".claude/dev/ci_dang_ky_test.py")
        song, hien_vat, la = dk.tim(ROOT)
        kq["tim"] = {"so_test_song": len(song), "so_hien_vat": len(hien_vat), "vi_tri_la": sorted(la),
                     "tep_packet_trong_ket_qua": sorted(x for x in (set(song) | set(hien_vat) | set(la)) if x.startswith("ops/specs/wp1434"))}
    except Exception as e:
        kq["tim"] = f"khong_do_duoc ({type(e).__name__}: {e})"
    return kq


def bao_cao(b, cohort):
    meta, m1, m2, L = b["meta"], b["M1"], b["M2"], []
    w = L.append

    def bang(tieu_de, hang):
        L.extend(bang_md(tieu_de, hang))

    def tk(o, don_vi="s"):
        if not o or o.get("trang_thai") != DO_DUOC:
            return "—"
        return (f"n={o['n']} · tổng {o['tong']} · trung vị {o['trung_vi']} · p90 {o['p90']} · max {o['lon_nhat']} {don_vi}"
                + (f" · loại {o['so_loai']}" if o.get("so_loai") else ""))

    def v(o):
        return str(o["gia_tri"]) if o["trang_thai"] == DO_DUOC else f"{o['trang_thai']} ({o.get('ly_do')})"

    tach = lambda k: k.split(" | ")
    w("# wp1434 r3 — Báo cáo đo nền mutation testing (chỉ đọc)\n")
    w(f"Sinh bởi `thu_thap.py --tinh` từ ảnh chụp (MANIFEST sha256 `{meta['manifest_sha256']}`). Đặc tả sha256 `{meta['spec_sha256']}`.")
    w(f"Cohort đóng băng: T0 `{meta['T0']}` · T1 `{meta['T1']}` · master `{meta['sha_master']}` · {len(meta['khoang_con'])} khoảng con liệt kê `ci.yml`.")
    for wf, c in meta["cohort"].items():
        w(f"- `{wf}`: {c['so_luot']} lượt, {c['so_cap_run_attempt']} cặp (run_id, run_attempt); bị loại khỏi cohort: {c['bi_loai'] or 'không'}")
    w("\nKhông có mục khuyến nghị tối ưu (ngoài phạm vi packet). Mọi con số dưới đây đọc từ `BASELINE.json`.\n")
    w("## Quy tắc §3 và ba trạng thái\n")
    for k, x in meta["quy_tac"].items():
        w(f"- **{k}**: {x}")
    w("\n## Độ phủ nguồn\n")
    bang(["nguồn", "yêu cầu", "có", "hết hạn", "cắt cụt", "lỗi", "không thu (hết khung)", "có log, không có bản ghi"],
         [[k, o["yeu_cau"], o["co"], o["het_han"], o["cat_cut"], o["loi"], o["khong_thu"], o["khong_co_ban_ghi"]] for k, o in b["do_phu"].items()])
    w("\n`log_dang_ky_ci` chỉ yêu cầu ở dòng `gate-registry` thực thi có bước registry không `skipped`; `log_chuan_bi` để đọc làn.\n")
    w("## M1 — full audit (`ci-dot-bien-du.yml`)\n")
    w(f"- {m1['so_luot']} lượt · kết luận {m1['theo_ket_luan']} · lượt có rerun {m1['so_luot_co_rerun']} · job hỏng ở attempt trước {m1['so_job_hong_o_attempt_truoc']}")
    d8 = m1["luot_du_8_manh_success"]
    w(f"- Lượt đủ 8 mảnh success, một attempt: {d8['so_luot']}. Tổng giây 8 job mảnh mỗi lượt: {tk(d8['tong_giay_8_job_manh_moi_luot'])}")
    w(f"- Giây một job mảnh (các lượt ấy): {tk(d8['giay_mot_job_manh'])}")
    if d8["moi_nhat"]:
        mn = d8["moi_nhat"]
        w(f"- Lượt đủ mới nhất `{mn['run_id']}` ({mn['created_at']}): job mảnh {tk(mn['giay_job_manh'])}; mục theo log {mn['so_muc_theo_log']}, theo artifact {mn['so_muc_theo_artifact']}; "
          f"giây thực thi {v(mn['giay_thuc_thi'])}; đầu-cuối suy ra từ job {v(mn['dau_cuoi_suy_ra_tu_job'])} s")
    w("")
    bang(["job gốc", "nền", "thống kê giây (dòng thực thi, mọi lượt)"], [tach(k) + [tk(o)] for k, o in m1["theo_job"].items()])
    mk = m1["muc_ket_qua_theo_khoa"]["bang"]
    mk_do = sorted((o["trung_vi"], k) for k, o in mk.items() if o.get("trang_thai") == DO_DUOC)
    w(f"\nDòng `KET QUA` trong log mảnh: {len(mk)} khoá (chế độ | khoá) ở `M1.muc_ket_qua_theo_khoa`; trung vị giây theo khoá từ "
      f"{mk_do[0][0] if mk_do else '—'} đến {mk_do[-1][0] if mk_do else '—'} (lớn nhất: `{mk_do[-1][1] if mk_do else '—'}`).")
    w("\nTừng lượt, từng job, từng bước job mảnh, từng artifact: `BASELINE.json` → `M1.luot`.\n")
    w("## M2 — gate CI (`ci.yml`)\n")
    w(f"- {m2['so_luot']} lượt · kết luận {m2['theo_ket_luan']} · làn {m2['theo_lan']} · lượt có rerun {m2['so_luot_co_rerun']} · job hỏng ở attempt trước {m2['so_job_hong_o_attempt_truoc']}")
    w("")
    bang(["sự kiện", "làn", "lượt", "giây thực thi", "đầu-cuối suy ra từ job"],
         [(tach(k) if " | " in k else [k, "—"]) + [o["so_luot"], tk(o["giay_thuc_thi"]), tk(o["dau_cuoi_suy_ra_tu_job"])]
          for k, o in [("tất cả", m2["moi_luot"]["tat_ca"])] + list(m2["moi_luot"]["theo_su_kien_va_lan"].items())])
    w("\nJob nhóm `gate*` (làn `day_du`, dòng thực thi; đủ mọi làn/nền ở `M2.theo_job`):\n")
    bang(["job gốc", "nền", "làn", "thống kê giây", "bỏ qua", "mang sang", "kết luận"],
         [tach(k) + [tk(o), o["so_bo_qua"], o["so_mang_sang"], o["ket_luan"]] for k, o in m2["theo_job"]["bang"].items()
          if tach(k)[2] == "day_du" and tach(k)[1] != "_"])
    bb = [(k, o) for k, o in m2["theo_buoc"]["bang"].items() if o.get("trang_thai") == DO_DUOC]
    w(f"\nBước của `gate-cong-cu*`, `gate-nhanh-*`, `gate-registry`, `gate-packet-loop*`: {len(m2['theo_buoc']['bang'])} khoá ở `M2.theo_buoc`. 8 khoá có tổng giây lớn nhất:\n")
    bang(["job gốc", "nền", "làn", "bước", "thống kê giây"],
         [k.split(" | ", 3) + [tk(o)] for k, o in sorted(bb, key=lambda x: (-x[1]["tong"], x[0]))[:8]])
    w("\n## M2b — thời gian theo bộ test và chế độ (`CI_DANG_KY_THOI_GIAN`)\n")
    w(f"{len(b['M2b']['bang'])} khoá (job nguồn, nền, bộ). 10 khoá có tổng giây lớn nhất:\n")
    tong_bo = lambda o: sum(c.get("tong", 0) for c in o["che_do"].values())
    bang(["job nguồn", "nền", "bộ", "bản ghi", "rc≠0", "chế độ: n / trung vị / p90 (s)"],
         [k.split(" | ", 2) + [o["so_ban_ghi"], o["rc_khac_0"],
                              "; ".join(f"{c}: {x['n']} / {x.get('trung_vi', '—')} / {x.get('p90', '—')}" for c, x in o["che_do"].items())]
          for k, o in sorted(b["M2b"]["bang"].items(), key=lambda x: (-tong_bo(x[1]), x[0]))[:10]])
    m3 = b["M3"]
    w("\n## M3 — kiểm kê tĩnh (số phần tử CUỐI CÙNG của bảng sau import, không chạy bộ)\n")
    if m3.get("trang_thai") == KHONG_DO_DUOC:
        w(f"- `khong_do_duoc`: {m3['ly_do']}")
    hang = []
    for t, bg in m3["bang"].items():
        if "_tep" in bg:
            hang.append([f"`{t}`", f"{bg['_tep']['trang_thai']} ({bg['_tep'].get('ly_do')})"])
        else:
            hang.append([f"`{t}`", " · ".join(f"{n}={v(x)}" for n, x in bg.items())])
    bang(["bộ", "bảng (len cuối cùng)"], hang)
    kc = m3.get("ten_chua_MUT_hoac_DOT_BIEN_khong_chon") or []
    w(f"\nBảng đã import có tên chứa `MUT`/`DOT_BIEN` nhưng không được chọn: {len(kc)}, trong đó nghi bỏ sót (không có lý do loại): {m3.get('so_bang_nghi_bo_sot')}. "
      + "; ".join(f"`{x['tep']}` {x['bang']}={x['so']} ({x['ly_do_loai'] or 'NGHI BO SOT'})" for x in kc))
    w("\n## 5 điểm tốn thời gian nhất theo giây thực thi (nhóm job, cả cohort)\n")
    bang(["#", "workflow", "job gốc", "tổng giây thực thi", "số dòng thực thi", "trung vị s"],
         [[i, x["workflow"], x["job_goc"], x["tong_giay_thuc_thi"], x["so_dong_thuc_thi"], x["trung_vi_giay"]] for i, x in enumerate(b["top5_giay_thuc_thi"], 1)])
    w("\nNguồn: tổng `completed_at − started_at` của mọi dòng `thuc_thi` cùng tên gốc trong các tệp `jobs/*` của ảnh chụp (URL từng lượt ở `M1.luot[].nguon`, `M2.luot[].nguon`).\n")
    m4 = b["M4"]
    w("## M4 — đối chiếu lời khai\n")
    w(f"Lệnh: `{m4['lenh']}`. {m4['so_dong_khop']} dòng khớp ({m4['so_dong_khong_phai_loi_khai']} dòng không phải lời khai, {m4['so_dong_chua_anh_xa']} dòng chưa ánh xạ); "
      f"{len(m4['loi_khai'])} lời khai, kết luận: {m4['theo_ket_luan']}. Vị trí đọc ở `@{meta['sha_master'][:12]}`.\n")
    ngan = lambda x: x if len(str(x)) <= 230 else str(x)[:227] + "…"
    gom = []                                      # gom cac dong khong_do_duoc LIEN TIEP cung tep, cung nguon thieu thanh mot hang
    for x in m4["loi_khai"]:
        tep, so = x["vi_tri"].split("@")[0].rsplit(":", 1)
        khoa = (tep, x["loi_khai"], x["ket_luan"], x["ly_do"]) if x["ket_luan"] == KHONG_DO_DUOC and x["loi_khai"] == "(ca dong)" else None
        if khoa and gom and gom[-1][0] == khoa:
            gom[-1][1].append(so)
        else:
            gom.append((khoa, [so], x))
    bang(["vị trí", "lời khai", "số đo", "kết luận", "ghi chú / nguồn thiếu"],
         [[f"`{x['vi_tri'].split('@')[0].rsplit(':', 1)[0]}:{','.join(ds)}`", x["loi_khai"], "—" if x["so_do"] is None else ngan(x["so_do"]), x["ket_luan"], ngan(x["ly_do"])]
          for _, ds, x in gom])
    w("\nDòng khớp regex nhưng không phải lời khai: " + ("; ".join(f"`{x['vi_tri']}` ({x['ly_do']})" for x in m4["dong_khong_phai_loi_khai"]) or "không có") + ".")
    w("\n## Lời khai lệch\n")
    lech = [x for x in m4["loi_khai"] if x["ket_luan"] == "lech"]
    for x in lech:
        w(f"- `{x['vi_tri']}` — khai “{x['loi_khai']}”, đo {x['so_do']}. {x['ly_do']}")
    if not lech:
        w("- (không có lời khai nào kết luận `lech`)")
    w("\n## Không đo được\n")
    kd = b["khong_do_duoc"]
    w(f"{kd['so_muc']} mục nguồn (chi tiết + URL ở `BASELINE.json` → `khong_do_duoc.chi_tiet`). Tóm tắt theo dạng:\n")
    for k, n in sorted(kd["tom_tat"].items(), key=lambda x: (-x[1], x[0]))[:10]:
        w(f"- {n} × {k}")
    if len(kd["tom_tat"]) > 10:
        w(f"- … và {len(kd['tom_tat']) - 10} dạng khác (xem `khong_do_duoc.tom_tat`)")
    w(f"- Lời khai M4 `khong_do_duoc`: {m4['theo_ket_luan'].get(KHONG_DO_DUOC, 0)}, mỗi cái ghi nguồn thiếu ở bảng M4.")
    w("- M3: bộ không import được ghi `khong_do_duoc` kèm lý do; packet không chạy bộ để lấy số.")
    w("- Thời điểm workflow hoàn tất: API attempt không trả `completed_at`; chỉ có `dau_cuoi_suy_ra_tu_job`.")
    w("- Workflow đột biến ngoài cohort (vd. `packet-loop-dot-bien.yml`) không được thu: đặc tả §2 chỉ định hai workflow.")
    w("\n## Kết quả hai bộ phân loại §6 (trên tập đường dẫn của packet)\n")
    s6 = phan_loai_s6()
    w("Tập đường dẫn (mọi tệp là `A`, mode `100644`): " + ", ".join(f"`{t}`" for t in s6["tap_duong_dan"]))
    for k in ("phan_loai_tu_diff", "ly_do_ve_day_du", "phan_loai_packet_loop", "ci_duong_nhanh", "tim"):
        if k in s6:
            w(f"- `{k}` ⇒ `{json.dumps(s6[k], ensure_ascii=False)}`")
    w("\nLàn của PR phải được đo lại trên log CI thật trước merge (đặc tả §6); kết quả trên là phép chạy tại chỗ của hai hàm phân loại.")
    van_ban = "\n".join(L) + "\n"
    loi = loi_bang_md(van_ban)
    if loi:
        raise ValueError("BAO_CAO.md co bang lech so o: " + "; ".join(loi[:5]))
    return van_ban


# ───────────────────────────────────────────── --tu-kiem ─────────────────────────────────────────────

def lenh_tu_kiem():
    F = DAY / "fixtures"
    J = lambda t: json.loads((F / t).read_text(encoding="utf-8"))
    T = lambda t: (F / t).read_text(encoding="utf-8")
    ca = []

    def kiem(ten):
        def bo(f):
            ca.append((ten, f))
            return f
        return bo

    def bang(a, b, nhan):
        assert a == b, f"{nhan}: co {a!r}, doi {b!r}"

    @kiem("so_0_do_duoc: buoc started_at == completed_at la do_duoc voi gia tri 0")
    def _():
        b = J("buoc.json")["khong_giay"]
        x = thoi_luong_buoc(b)
        bang((x["trang_thai"], x["gia_tri"]), (DO_DUOC, 0), "buoc 0 giay")
        s = thong_ke([0, 0, 4])
        bang((s["n"], s["tong"], s["trung_vi"], s["nho_nhat"]), (3, 4, 0, 0), "thong ke co so 0")

    @kiem("thieu_started_at: khong_do_duoc, khong thay bang 0, bi loai khoi tong")
    def _():
        d = J("buoc.json")
        x = thoi_luong_buoc(d["thieu_started_at"])
        bang((x["trang_thai"], x["gia_tri"], x.get("ly_do")), (KHONG_DO_DUOC, None, "thieu_started_at"), "buoc thieu started_at")
        lu = tinh_luot(d["luot_thieu"]["run"], {1: d["luot_thieu"]["run"]["created_at"]}, d["luot_thieu"]["jobs"])
        bang((lu["giay_thuc_thi"]["gia_tri"], lu["giay_thuc_thi"]["so_dong_tinh"], lu["giay_thuc_thi"]["so_dong_loai"]), (30, 1, 2), "tong loai dong thieu/dao")

    @kiem("thoi_gian_dao: completed < started la khong_do_duoc, KHONG kep ve 0")
    def _():
        d = J("buoc.json")
        x = thoi_luong_buoc(d["dao"])
        bang((x["trang_thai"], x["gia_tri"]), (KHONG_DO_DUOC, None), "buoc dao")
        assert "thoi_gian_dao" in x["ly_do"], x
        lu = tinh_luot(d["luot_thieu"]["run"], {1: d["luot_thieu"]["run"]["created_at"]}, d["luot_thieu"]["jobs"])
        dao = [m for m in lu["dong"] if m["job_id"] == 903][0]
        bang(dao["giay"]["trang_thai"], KHONG_DO_DUOC, "job dao")
        bang(lu["giay_thuc_thi"]["gia_tri"], 30, "tong khong cong 0 thay cho dong dao")

    @kiem("buoc_skipped: khong_ap_dung")
    def _():
        x = thoi_luong_buoc(J("buoc.json")["skipped"])
        bang((x["trang_thai"], x["gia_tri"]), (KHONG_AP_DUNG, None), "buoc skipped")

    @kiem("bien_cohort: khoang dong [T0, T1], loc su kien va trang thai")
    def _():
        d = J("cohort_bien.json")
        trong, loai = loc_cohort(d["ci"], WF_CI, d["T0"], d["T1"])
        bang(sorted(r["id"] for r in trong), [102, 103, 108], "ci.yml trong cohort")
        bang(dict(loai), {101: "truoc_T0", 104: "sau_T1", 105: "chua_completed_luc_thu", 106: "su_kien_ngoai_pham_vi",
                          107: "su_kien_ngoai_pham_vi"}, "ci.yml bi loai")
        trong, loai = loc_cohort(d["du"], WF_DU, d["T0"], d["T1"])
        bang(sorted(r["id"] for r in trong), [201, 202], "dot-bien-du: khong can duoi, co can tren")
        bang(dict(loai), {203: "sau_T1"}, "dot-bien-du bi loai")

    @kiem("hai_attempt: mang_sang, skipped ca hai attempt, ba con so, khong dung updated_at")
    def _():
        d = J("luot_hai_attempt.json")
        for a in d["attempts"].values():
            assert "completed_at" not in a, "fixture: phan hoi attempt khong duoc co completed_at"
        tao = {int(k): v["created_at"] for k, v in d["attempts"].items()}
        lu = tinh_luot(d["run"], tao, d["jobs"])
        bang(lu["so_dong"], {BO_QUA: 2, MANG_SANG: 1, THUC_THI: 5, KHONG_PHAN_LOAI: 0}, "phan loai dong")
        bang({m["job_id"]: m["loai_dong"] for m in lu["dong"]},
             {1: THUC_THI, 2: THUC_THI, 3: BO_QUA, 4: THUC_THI, 5: MANG_SANG, 6: THUC_THI, 7: BO_QUA, 8: THUC_THI}, "tung dong")
        bang((lu["giay_thuc_thi"]["gia_tri"], lu["giay_thuc_thi"]["so_dong_tinh"], lu["giay_thuc_thi"]["so_dong_loai"]), (1105, 5, 0), "giay_thuc_thi")
        bang(lu["dau_cuoi_suy_ra_tu_job"]["gia_tri"], 3338, "dau_cuoi_suy_ra_tu_job (max completed_at job attempt cuoi - created_at attempt 1)")
        capnhat = int((gio(d["run"]["updated_at"]) - gio(tao[1])).total_seconds())
        assert capnhat != 3338, "fixture: updated_at cua run phai khac max(completed_at) cua job"
        bang(lu["updated_at_tham_khao"], d["run"]["updated_at"], "updated_at chi ghi kem")
        bang(sorted(m["giay_cho"]["gia_tri"] for m in lu["dong"] if m["loai_dong"] == THUC_THI), [1, 2, 2, 2, 20], "giay_cho")
        bang((lu["co_rerun"], lu["so_job_hong_o_attempt_truoc"]), (True, 2), "rerun + job hong attempt truoc")
        bo = [m for m in lu["dong"] if m["loai_dong"] == BO_QUA]
        assert all(m["giay"]["trang_thai"] == KHONG_AP_DUNG for m in bo), "job skipped phai khong_ap_dung"

    @kiem("mang_sang_cung_job_id: job_id da thay o attempt truoc la mang_sang ke ca khi khong so duoc thoi gian")
    def _():
        d = J("mang_sang_cung_job_id.json")
        lu = tinh_luot(d["run"], {int(k): v for k, v in d["tao_attempt"].items()}, d["jobs"])
        bang({(m["run_attempt"], m["job_id"]): m["loai_dong"] for m in lu["dong"]}, {(1, 11): THUC_THI, (2, 11): MANG_SANG, (2, 12): THUC_THI}, "phan loai")
        bang(lu["giay_thuc_thi"]["gia_tri"], 70, "tong khong tinh trung")

    @kiem("attempt_cuoi_khong_co_thuc_thi: dau_cuoi khong_do_duoc")
    def _():
        d = J("attempt_cuoi_rong.json")
        lu = tinh_luot(d["run"], {int(k): v for k, v in d["tao_attempt"].items()}, d["jobs"])
        bang(lu["dau_cuoi_suy_ra_tu_job"]["trang_thai"], KHONG_DO_DUOC, "dau_cuoi")
        bang(lu["giay_thuc_thi"]["gia_tri"], 10, "giay_thuc_thi van tinh attempt 1")

    @kiem("artifact: het han, con han doc duoc, zip hong la cat cut")
    def _():
        d = J("artifacts.json")
        bang([bool(a["expired"]) for a in d["artifacts"]], [True, False], "fixture danh sach")
        bang(trang_thai_nguon({"http": 410, "duong_dan": None, "loi": "HTTP 410"}), "het_han", "410")
        bang(trang_thai_nguon({"http": 404, "duong_dan": None, "loi": "HTTP 404"}), "loi", "404")
        bang(trang_thai_nguon(None), "khong_thu", "khong co trong MANIFEST")
        bang(trang_thai_nguon({"http": 200, "duong_dan": "art/1.zip"}), "co", "200")
        bo = io.BytesIO()
        with zipfile.ZipFile(bo, "w") as z:
            z.writestr("manh-5.json", json.dumps(d["noi_dung_manh"]))
        x = doc_artifact_manh(bo.getvalue())
        bang((x["trang_thai"], x["so_muc"], x["so_muc_passed"], x["rc"], x["giay"]["gia_tri"], x["manh"]), (DO_DUOC, 3, 2, 1, 0, 5), "artifact doc duoc (giay 0 la do_duoc)")
        bang(doc_artifact_manh(bo.getvalue()[:40])["trang_thai"], KHONG_DO_DUOC, "zip cat cut")

    @kiem("log_dang_ky: con / cat cut / thieu cho bo trich CI_DANG_KY_THOI_GIAN")
    def _():
        x = trich_thoi_gian_dang_ky(T("log_dang_ky_con.log"))
        bang(x["trang_thai_log"], "co", "log con")
        bang([(b["duong_dan"], b["rc"], b["che_do"], b["giay"]["trang_thai"], b["giay"]["gia_tri"]) for b in x["bo"]],
             [("ops/a_test.py", 0, "day_du", DO_DUOC, 174.381), ("ops/b_test.py", 0, "nhe", DO_DUOC, 0), ("ops/c_test.py", 1, "khong_ghi", KHONG_DO_DUOC, None),
              ("ops/d_test.py", 0, "day_du", KHONG_DO_DUOC, None)], "ban ghi theo bo (0 la do_duoc; thieu/am la khong_do_duoc)")
        bang(x["bo"][3]["giay"]["ly_do"], "giay_am", "giay am khong kep ve 0")
        bang(trich_thoi_gian_dang_ky(T("log_dang_ky_cat_cut.log"))["trang_thai_log"], "cat_cut", "log cat cut")
        bang(trich_thoi_gian_dang_ky(T("log_dang_ky_thieu.log"))["trang_thai_log"], "khong_co_ban_ghi", "log khong co ban ghi")

    @kiem("log_manh: con / cat cut / thieu cho bo trich dong KET QUA")
    def _():
        x = trich_ket_qua(T("log_manh_con.log"))
        bang((x["trang_thai_log"], x["mo"]["che_do"], x["mo"]["so_muc_khai"], x["dong"]["rc"]), ("co", "full_mutant_audit", 3, 1), "log con")
        bang([(m["khoa"], m["ket_qua"], m["giay"]["trang_thai"], m["giay"]["gia_tri"]) for m in x["muc"]],
             [("tk:a", "passed", DO_DUOC, 47.4), ("db:b", "passed", DO_DUOC, 0.0), ("ca:r546", "failed", KHONG_DO_DUOC, None)], "dong KET QUA")
        y = trich_ket_qua(T("log_manh_cat_cut.log"))
        bang((y["trang_thai_log"], len(y["muc"])), ("cat_cut", 1), "log cat cut")
        bang(trich_ket_qua(T("log_manh_thieu.log"))["trang_thai_log"], "khong_co_ban_ghi", "log khong co ban ghi")

    @kiem("lan: doc che_do tu log buoc phan loai; thieu -> None")
    def _():
        bang(trich_lan(T("log_chuan_bi.log")), "duong_nhanh", "lan")
        bang(trich_lan(T("log_chuan_bi_cu.log")), "day_du", "lan tu dong 'luon DAY_DU' (khong tinh dong echo cua lenh)")
        bang(trich_lan(T("log_chuan_bi_cu.log").splitlines()[1]), None, "dong echo cua lenh khong phai ket qua phan loai")
        bang(trich_lan(T("log_manh_thieu.log")), None, "khong co dong che_do")

    @kiem("can_log: chi dong thuc_thi; gate-registry chi khi buoc registry khong skipped")
    def _():
        d = J("luot_hai_attempt.json")
        lu = tinh_luot(d["run"], {int(k): v["created_at"] for k, v in d["attempts"].items()}, d["jobs"])
        bang({m["job_id"]: can_log(WF_CI, m) for m in lu["dong"]}, {1: "chuan_bi", 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None}, "ke hoach log")
        r = {"loai_dong": THUC_THI, "ten_goc": "gate-registry", "_tho": {"steps": [{"name": "test registry (x)", "conclusion": "skipped"}]}}
        bang(can_log(WF_CI, r), None, "registry skipped")
        r["_tho"]["steps"][0]["conclusion"] = "success"
        bang(can_log(WF_CI, r), "dang_ky_ci", "registry chay")

    @kiem("xuat_json tat dinh + khong bi mat")
    def _():
        o = {"a": [1, {"b": None}], "c": {"d": 0}}
        bang(json.loads(xuat_json(o, 2)), o, "khu hoi")
        bang(xuat_json(o, 2), xuat_json(json.loads(xuat_json(o, 2)), 2), "tat dinh")
        for mau in (r"gh[pousr]_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{20,}", r"X-Amz-Signature|[?&]sig=|[?&]se="):
            for p in sorted(F.iterdir()):
                assert not re.search(mau, p.read_text(encoding="utf-8", errors="replace")), f"dau hieu bi mat trong {p.name}"

    @kiem("m3_bang_cuoi_cung: literal dau + .update + gan chi so + append -> dem so CUOI CUNG, khong dem literal dau")
    def _():
        with tempfile.TemporaryDirectory(prefix="wp1434-tk-") as d:
            ghi_tep(d, "mau_bang.py", T("m3_bang_dien_sau.txt").encode("utf-8"))
            dl, ly, _ = doc_bang_import(pathlib.Path(d) / "mau_bang.py", d, "mau_bang")
            bang(ly, None, "import mau")
            bg = dl["bang"]
            bang((bg.get("MUTANTS"), bg.get("CA"), bg.get("DOT_BIEN"), bg.get("MUTATIONS")), (5, 3, 4, 3), "len cuoi cung (literal dau: 2, 0, 1, 1)")
            bang((dl["ten"]["CA"], dl["ten"]["MUTATIONS"], dl["hang_so"].get("TRAN_GIAY")), (["t1", "t2", "t3"], ["x1", "x2", "x3"], 540), "ten phan tu + hang so")
            assert not [x for x in pathlib.Path(d).rglob("DA_CHAY_BO")], "import khong duoc chay khoi __main__"
            ghi_tep(d, "khong_chot.py", b"MUTANTS = {1: 1}\n")
            bg2, ly2, _ = doc_bang_import(pathlib.Path(d) / "khong_chot.py", d, "khong_chot")
            assert bg2 is None and "chot" in ly2, "tep khong co chot __main__ phai bi tu choi, khong import"
            chon_mau = m3_chon_bang("x/mau.py", bg)
            assert "MUTATIONS" in chon_mau and "IMMUTABLE_TRUONG" not in chon_mau and "THUONG" not in chon_mau, f"chon bang: {sorted(chon_mau)}"
            bang(m3_nghi_bo_sot("x/mau.py", bg), [("IMMUTABLE_TRUONG", 2, None)], "ten chua MUT khong duoc chon phai bi BAO (chua co ly do loai => nghi bo sot)")
        chon = m3_chon_bang(".claude/dev/ci_dang_ky_test.py", {"MUTANTS": 5, "CA": 3, "GOC": 9, "DANG_KY": 29, "DOT_BIEN_HOOK": 2, "CACH_LY": 0})
        bang(chon, {"CA": 3, "CACH_LY": 0, "DANG_KY": 29, "DOT_BIEN_HOOK": 2, "MUTANTS": 5}, "chon bang (giu bang 0 phan tu, bo bang khong lien quan)")
        m3 = m3_tu_anh_chup({"sha": "a" * 40, "bo": {"x/a_test.py": {"blob": "b" * 40, "bang": {"MUTANTS": 5, "GOC": 1}, "ly_do": None},
                                                  "x/b_test.py": {"blob": "c" * 40, "bang": None, "ly_do": "import khong thanh (rc=1)"}}}, "a" * 40)
        bang(m3["bang"]["x/a_test.py"]["MUTANTS"]["gia_tri"], 5, "M3 tu anh chup")
        m3b = m3_tu_anh_chup({"sha": "a" * 40, "bo": {"x/a_test.py": {"blob": "b" * 40, "ly_do": None,
                                                   "bang": {"MUTATIONS": 65, "_WP1393_IMMUTABLE": 14, "BANG_MUTX": 2}}}}, "a" * 40)
        bang(m3b["bang"]["x/a_test.py"]["MUTATIONS"]["gia_tri"], 65, "MUTATIONS song sot qua buoc chon")
        bang([(x["bang"], x["trang_thai"]) for x in m3b["ten_chua_MUT_hoac_DOT_BIEN_khong_chon"]],
             [("BANG_MUTX", "nghi_bo_sot"), ("_WP1393_IMMUTABLE", "da_giai_thich")], "bang khong chon co ten chua MUT duoc bao, tach da giai thich / nghi bo sot")
        bang(m3b["so_bang_nghi_bo_sot"], 1, "dem bang nghi bo sot")
        bang(m3["bang"]["x/b_test.py"]["_tep"]["trang_thai"], KHONG_DO_DUOC, "bo khong import duoc -> khong_do_duoc")
        bang(m3_tu_anh_chup(None, "a" * 40).get("trang_thai"), KHONG_DO_DUOC, "anh chup thieu su kien M3 -> khong_do_duoc")

    @kiem("m4_anh_xa: loi khai do duoc ngoai quy tac cu duoc SO; bien ban lich su o lai khong_do_duoc kem nguon thieu")
    def _():
        d = J("m4_loi_khai.json")
        do = dict(d["do"], job_dai_nhat={int(k): x for k, x in d["do"]["job_dai_nhat"].items()})
        kq = m4_doi_chieu([tuple(x) for x in d["dong"]], do)
        theo = {}
        for x in kq["loi_khai"]:
            theo.setdefault(x["vi_tri"].split("@")[0], []).append((x["loi_khai"], x["so_do"] if not isinstance(x["so_do"], str) else "chuoi", x["ket_luan"]))
        bang(theo["docs/GOI_AGENT_DA_NEN.md:493"], [(".claude/dev/launcher_test.py: 31 dot bien", 572, "lech")], "(a) loi khai launcher ngoai quy tac cu")
        bang(theo["docs/vi_du.md:7"], [("ops/x_test.py: 5 dot bien", 5, "khop")], "(a') cung quy tac, so khop, bang MUTANTS")
        bang(theo[".github/workflows/ci.yml:937"][0], ("52 ca", 56, "lech"), "'52 ca' o dong 937 duoc so voi TU_KIEM")
        bang(theo[".github/workflows/ci.yml:935"], [("10 dot bien san pham", 10, "khop"), ("gate-nhanh-manh: 8 manh", 8, "khop")], "dem + so manh")
        bang(theo["docs/AUDIT_LAUNCHER_VONG_4_POSIX.md:51"], [("(ca dong)", None, KHONG_DO_DUOC)], "(b) bien ban lich su")
        ls = [x for x in kq["loi_khai"] if x["vi_tri"].startswith("docs/AUDIT_")][0]
        assert ls["ly_do"].startswith("nguon thieu: ") and "audit" in ls["ly_do"], "khong_do_duoc phai ghi nguon thieu cu the"
        bang(theo["docs/khac.md:3"], [("khong_co_test.py: 9 dot bien", None, KHONG_DO_DUOC)], "bo khong co trong M3 -> khong_do_duoc")
        bang(theo[".github/workflows/ci.yml:562"], [("45m56s (run 36362558889)", None, KHONG_DO_DUOC)], "luot ngoai cohort")
        bang(theo[".github/workflows/ci.yml:568"][0][2], "khop", "skip: chi tinh luot sau moc blame")
        bang(theo[".github/workflows/ci.yml:1121"][0][2], "lech", "job 8524 s khong phai 141 phut")
        bang((kq["so_dong_khong_phai_loi_khai"], kq["so_dong_chua_anh_xa"]), (1, 1), "dong khong phai loi khai + dong chua anh xa duoc dem rieng")
        assert all(x["ket_luan"] != KHONG_DO_DUOC or x["ly_do"].startswith("nguon thieu: ") for x in kq["loi_khai"]), "moi khong_do_duoc phai co nguon thieu"
        bang(theo["CLAUDE.md:591"], [("PR #895: CI do 8/8 manh gate-cong-cu", "chuoi", "khop"), ("26 va 28 loi ban kinh o hai manh doc duoc", None, KHONG_DO_DUOC),
                                     ("13/13 giet dung t52", None, KHONG_DO_DUOC)], "loi khai TACH: mot ve do duoc, hai ve thieu nguon")
        bang(theo[".github/workflows/ci.yml:413"], [("ci_phamvi_test: 6 dot bien (ca phan chung n*)", 6, "khop")], "6 dot bien doc tu ten phan tu cua CA")
        bang(theo[".github/workflows/ci.yml:937"][1:], [("duong gang <= 540 s (nguong cua buoc gom)", 540, "khop")], "nguong so voi hang so trong ma")
        bang(theo[".github/workflows/packet-loop-dot-bien.yml:5"], [("packet-loop-dot-bien: 16 manh (k % 16)", 16, "khop"), ("(~45 phút)", None, KHONG_DO_DUOC)],
             "loi khai TACH: so manh doc tu ma tran workflow, thoi luong thieu nguon")
        mat_pr = m4_doi_chieu([tuple(x) for x in d["dong"]], dict(do, pr_nhanh=None))
        bang([x["ket_luan"] for x in mat_pr["loi_khai"] if x["vi_tri"].startswith("CLAUDE.md:591")], [KHONG_DO_DUOC] * 3, "thieu anh xa PR -> nhanh thi ve 8/8 khong_do_duoc")
        bang(doc_ma_tran_manh("    strategy:\n      matrix:\n        manh: [0, 1, 2]\n"), 3, "doc ma tran")
        bang(doc_ma_tran_manh("khong co"), None, "khong co ma tran -> None")
        mat = m4_doi_chieu([tuple(x) for x in d["dong"]], dict(do, blame=None))
        bang([x["ket_luan"] for x in mat["loi_khai"] if x["vi_tri"].startswith(".github/workflows/ci.yml:568")], [KHONG_DO_DUOC], "thieu blame trong anh chup -> khong_do_duoc")

    @kiem("ghi_co_gioi_han: tu choi dich la symlink va thu muc con la symlink; tep ngoai khong doi; ghi thuong van duoc")
    def _():
        with tempfile.TemporaryDirectory(prefix="wp1434-tk-") as d:
            goc, ngoai = pathlib.Path(d) / "ra", pathlib.Path(d) / "ngoai"
            goc.mkdir()
            ngoai.mkdir()
            ghi_tep(ngoai, "canh_gac.txt", b"KHONG DUOC DOI")
            bang(ghi_tep(goc, "BASELINE.json", b"{}\n").read_bytes(), b"{}\n", "ghi thuong")
            bang(ghi_tep(goc, "a/b/c.json", b"1").read_bytes(), b"1", "ghi thuong co thu muc con")
            bang(ghi_tep(goc, "BASELINE.json", b"[]\n").read_bytes(), b"[]\n", "ghi de tep thuong")
            if not hasattr(os, "symlink"):
                raise AssertionError("nen khong co os.symlink: KHONG DO DUOC chot symlink")
            os.symlink(ngoai / "canh_gac.txt", goc / "COHORT.json")
            os.symlink(ngoai, goc / "lien_ket")
            os.symlink(goc / "khong_ton_tai", goc / "treo.json")
            os.symlink(goc / "a", goc / "noi_bo")          # symlink tro VAO TRONG goc van bi tu choi: thanh phan la symlink
            for dich in ("COHORT.json", "lien_ket/x.json", "noi_bo/x.json", "lien_ket/sau/y.json", "treo.json", "../ngoai/z.json", "/tmp/wp1434-tuyet-doi.json", "a/../q.json"):
                try:
                    ghi_tep(goc, dich, b"DA BI GHI DE")
                except GhiBiTuChoi:
                    pass
                else:
                    raise AssertionError(f"ghi_tep KHONG tu choi dich {dich!r}")
                try:
                    mo_noi_them(goc, dich).close()
                except GhiBiTuChoi:
                    pass
                else:
                    raise AssertionError(f"mo_noi_them KHONG tu choi dich {dich!r}")
            bang((ngoai / "canh_gac.txt").read_bytes(), b"KHONG DUOC DOI", "tep canh gac ben ngoai")
            bang(sorted(p.name for p in ngoai.iterdir()), ["canh_gac.txt"], "khong tep nao duoc tao ben ngoai")
            assert not [p for p in goc.rglob(".tam-wp1434-*")], "khong de lai tep tam"
            bang(sorted(p.name for p in (goc / "a").iterdir()), ["b"], "khong ghi xuyen qua symlink noi bo")
        nguon = pathlib.Path(__file__).read_text(encoding="utf-8")
        for cam in (".write" + "_text(", ".write" + "_bytes(", "shutil" + ".copy", "os." + "rename("):
            bang(nguon.count(cam), 0, f"moi lan ghi phai qua ghi_tep/mo_noi_them: con {cam!r} trong ma")
        bang(len(re.findall(r"(?<![\w.])open\(", nguon)), 0, "khong goi ham mo tep tran (chi os-level trong mo_noi_them va ghi_tep)")

    @kiem("bang_markdown: o chua dau | duoc thoat; moi hang cung so o voi tieu de; bang vo bi bat")
    def _():
        dong = bang_md(["job gốc", "bước"], [["gate-cong-cu", "a | b"], ["x\\y", "c|d"]])
        bang(loi_bang_md("\n".join(dong)), [], "bang sinh ra hop le")
        assert "a \\| b" in dong[2] and "c\\|d" in dong[3], "dau | trong o phai duoc thoat"
        bang(loi_bang_md("| a | b |\n|---|---|\n| gate | ubuntu | day_du |\n"), ["dong 3: 3 o, tieu de 2 o"], "hang thua o bi bat")
        bang(loi_bang_md("| a | b |\n|---|---|\n| 1 | 2 |\n\nchu thuong a | b | c\n\n| x |\n|---|\n| 1 |\n"), [], "hai bang doc lap + chu thuong co dau |")
        try:
            bang_md(["a", "b"], [["chi mot o"]])
        except ValueError:
            pass
        else:
            raise AssertionError("bang_md phai tu choi hang lech so o")

    @kiem("m3_hop_cat: tac dung phu luc import roi VAO hop cat duoi --ra, thu muc ngoai khong doi; module ghi thang ra ngoai bi TU CHOI")
    def _():
        with tempfile.TemporaryDirectory(prefix="wp1434-tk-") as d:
            d = pathlib.Path(d)
            ra, ngoai = d / "ra", d / "ngoai"
            ra.mkdir()
            ngoai.mkdir()
            ghi_tep(ngoai, "canh_gac.txt", b"KHONG DUOC DOI")
            ghi_tep(d, "mau_ghi.py", T("m3_ghi_tmp.txt").encode("utf-8"))
            mt = moi_truong_hop_cat(ra / "kho" / "_import_sandbox" / "x")
            for k in ("TMPDIR", "TMP", "TEMP", "HOME", "XDG_CACHE_HOME", "XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_STATE_HOME", "XDG_RUNTIME_DIR"):
                assert str(ra) + os.sep in mt.get(k, ""), f"bien {k} cua tien trinh con phai tro vao hop cat duoi --ra"
            cu = {k: os.environ.get(k) for k in ("TMPDIR", "HOME", "WP1434_THOAT")}
            try:
                # Tien trinh nay gia vo co TMPDIR/HOME la thu muc NGOAI: khong giam giu thi module se ghi vao do.
                os.environ["TMPDIR"], os.environ["HOME"] = str(ngoai), str(ngoai)
                os.environ.pop("WP1434_THOAT", None)
                truoc = chup_thu_muc(ngoai, True)
                dl, ly, con_lai = doc_bang_import(d / "mau_ghi.py", ra, "mau_ghi", canh_gac=[ngoai])
                bang(ly, None, "import giam giu")
                bang(dl["bang"].get("DOT_BIEN"), 2, "bang doc duoc sau import giam giu")
                bang(con_lai, 3, "ba tep module ghi luc import (tmp, home, cwd) phai roi vao hop cat duoi --ra")
                bang(chup_thu_muc(ngoai, True), truoc, "thu muc ngoai (TMPDIR/HOME that) khong doi")
                assert not (ra / "kho" / "_import_sandbox" / "mau_ghi").exists(), "hop cat phai duoc don sau khi doc"
                os.environ["WP1434_THOAT"] = str(ngoai)            # phan chung: module ghi THANG ra ngoai bang duong dan tuyet doi
                dl2, ly2, _ = doc_bang_import(d / "mau_ghi.py", ra, "mau_ghi", canh_gac=[ngoai])
                assert dl2 is None and "NGOAI hop cat" in (ly2 or ""), f"ghi ra ngoai phai bi tu choi (fail-closed), co: {dl2!r} / {ly2!r}"
                assert (ngoai / "wp1434_thoat.txt").exists(), "phan chung phai that su ghi ra ngoai (neu khong, ca nay khong do gi)"
            finally:
                for k, v in cu.items():
                    if v is None:
                        os.environ.pop(k, None)
                    else:
                        os.environ[k] = v
            os.symlink(ngoai, ra / "kho" / "_import_sandbox" / "lk") if (ra / "kho" / "_import_sandbox").is_dir() else None
            if (ra / "kho" / "_import_sandbox" / "lk").is_symlink():
                try:
                    doc_bang_import(d / "mau_ghi.py", ra, "lk")
                except GhiBiTuChoi:
                    pass
                else:
                    raise AssertionError("hop cat la symlink phai bi tu choi")
                bang((ngoai / "canh_gac.txt").read_bytes(), b"KHONG DUOC DOI", "canh gac sau hop cat symlink")

    dat = 0
    for ten, f in ca:
        try:
            f()
            dat += 1
            print("DAT ", ten)
        except Exception as e:
            print("DO  ", ten, "—", type(e).__name__, str(e)[:300])
    print(f"TU KIEM: {dat}/{len(ca)}")
    return 0 if dat == len(ca) and ca else 1


def main():
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="backslashreplace")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--thu", action="store_true")
    ap.add_argument("--tinh", action="store_true")
    ap.add_argument("--tu-kiem", action="store_true")
    ap.add_argument("--ra")
    ap.add_argument("--anh-chup")
    ap.add_argument("--han-giay", type=int, default=5400, help="khung thoi gian cua --thu; het khung thi phan con lai la khong_do_duoc")
    ap.add_argument("--so-luong", type=int, default=6)
    ap.add_argument("--chi-su-kien-kho", action="store_true", help="voi --thu: KHONG goi mang; chi them su kien kho vao anh chup da co")
    ns = ap.parse_args()
    if sum((ns.thu, ns.tinh, ns.tu_kiem)) != 1:
        ap.error("chon DUNG MOT trong --thu | --tinh | --tu-kiem")
    if ns.tu_kiem:
        return lenh_tu_kiem()
    if ns.thu:
        if not ns.ra:
            ap.error("--thu can --ra <anh chup>")
        return lenh_bo_sung_kho(ns) if ns.chi_su_kien_kho else lenh_thu(ns)
    if not (ns.anh_chup and ns.ra):
        ap.error("--tinh can --anh-chup <anh chup> --ra <thu muc>")
    return lenh_tinh(ns)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except GhiBiTuChoi as e:
        print("TU CHOI GHI:", e)
        sys.exit(4)
