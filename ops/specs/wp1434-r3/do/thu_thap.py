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
import statistics
import subprocess
import sys
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
        self.f_nk = open(self.nk, "a", encoding="utf-8")

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
            p = self.ra / tep
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(du_lieu)
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
        f_meta.write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
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
    f_meta.write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
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

    # 3) MANIFEST
    t.f_nk.close()
    b_meta = f_meta.read_bytes()
    muc = sorted(t.muc.values(), key=lambda m: m["khoa"])
    muc.insert(0, {"khoa": "META", "loai": "meta", "url": None, "http": None, "duong_dan": "META.json",
                   "sha256": sha256_bytes(b_meta), "kich_thuoc": len(b_meta)})
    (t.ra / "MANIFEST.json").write_text(json.dumps({"tep": muc}, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
    t.nk.unlink()
    loi = sum(1 for m in muc if m.get("loi"))
    print(f"MANIFEST: {len(muc)} muc, {loi} muc khong co tep (loi/het han/het khung)")
    return 0


# ───────────────────────────────────────────── --tinh ─────────────────────────────────────────────

def git_show(sha, duong):
    r = subprocess.run(["git", "show", f"{sha}:{duong}"], cwd=ROOT, capture_output=True)
    return r.stdout.decode("utf-8", errors="replace") if r.returncode == 0 else None


def git_ds(sha, tien_to):
    r = subprocess.run(["git", "ls-tree", "-r", "--name-only", sha, "--"] + list(tien_to), cwd=ROOT, capture_output=True)
    return sorted(r.stdout.decode("utf-8", errors="replace").splitlines()) if r.returncode == 0 else []


M3_BANG = {".claude/dev/ci_dang_ky_test.py": ("DANG_KY", "MOI", "NHE", "MOI_WINDOWS", "CACH_LY", "DA_NOI"),
           "ops/nhanh_don_duoc_test.py": ("CA", "TU_KIEM", "DOT_BIEN", "DOT_BIEN_TU_KIEM")}
M3_TEN_TINH = ("DOT_BIEN", "DOT_BIEN_TU_KIEM", "TU_KIEM", "CA", "MUTANTS", "MUTANT", "CA_DAI")
M3_MA = ("import importlib.util,json,sys,os\n"
         "p=sys.argv[1]; sys.path.insert(0,os.path.dirname(os.path.abspath(p)))\n"
         "s=importlib.util.spec_from_file_location('wp1434_m3_doc_bang',p); m=importlib.util.module_from_spec(s)\n"
         "sys.modules['wp1434_m3_doc_bang']=m; s.loader.exec_module(m)\n"
         "o={}\n"
         "for n in sys.argv[2:]:\n"
         "    v=getattr(m,n,None)\n"
         "    o[n]=len(v) if hasattr(v,'__len__') else None\n"
         "print('WP1434_M3 '+json.dumps(o))\n")


def m3_kiem_ke(sha):
    """Kiem ke tinh. (1) hai module neu ten trong dac ta: IMPORT trong tien trinh con, chi doc len() cua bang hang (khong goi ham chay ca).
    (2) moi bo trong DANG_KY: dem phan tu literal bang ast tren `git show <sha>:<tep>`; khong phai literal -> khong_do_duoc."""
    import ast
    import warnings
    kq = {"import": {}, "tinh_ast": {}}
    for tep, ten in M3_BANG.items():
        a = subprocess.run(["git", "rev-parse", f"{sha}:{tep}"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        b = subprocess.run(["git", "hash-object", tep], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        nguon = f"{tep}@{sha[:12]} (import, len() cua bang)"
        if not a or a != b:
            kq["import"][tep] = {n: kdd("tep tren cay lam viec khac blob o SHA meta", nguon) for n in ten}
            continue
        try:
            r = subprocess.run([sys.executable, "-c", M3_MA, tep] + list(ten), cwd=ROOT, capture_output=True, text=True, timeout=180,
                               env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"})
            dong = [l for l in r.stdout.splitlines() if l.startswith("WP1434_M3 ")]
            o = json.loads(dong[-1][len("WP1434_M3 "):])
            kq["import"][tep] = {n: (gt(o[n], nguon) if isinstance(o.get(n), int) else kdd("bang khong ton tai hoac khong co len()", nguon))
                                 for n in ten}
        except Exception as e:
            kq["import"][tep] = {n: kdd(f"import khong thanh ({type(e).__name__})", nguon) for n in ten}
    goc = (".claude/dev/", ".claude/hooks/", ".githooks/", ".github/checks/", "scripts/tl_core/", "ops/")
    for tep in git_ds(sha, goc):
        if not tep.endswith("_test.py") or tep.startswith("ops/reviews/") or (tep.startswith("ops/") and tep.count("/") != 1):
            continue
        van = git_show(sha, tep)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                cay = ast.parse(van or "")
        except SyntaxError:
            kq["tinh_ast"][tep] = {"_tep": kdd("khong phan tich duoc cu phap")}
            continue
        muc = {}
        for nut in cay.body:
            dich = nut.targets[0] if isinstance(nut, ast.Assign) and len(nut.targets) == 1 else (nut.target if isinstance(nut, ast.AnnAssign) else None)
            if not isinstance(dich, ast.Name) or dich.id not in M3_TEN_TINH or getattr(nut, "value", None) is None:
                continue
            nguon = f"{tep}:{nut.lineno}@{sha[:12]}"
            v = nut.value
            if isinstance(v, (ast.List, ast.Tuple, ast.Set)) and not any(isinstance(e, ast.Starred) for e in v.elts):
                so = len(v.elts)
            elif isinstance(v, ast.Dict) and all(k is not None for k in v.keys):
                so = len(v.keys)
            else:
                muc[dich.id] = kdd("khong phai literal tinh (chi sinh khi chay/import)", nguon)
                continue
            muc[dich.id] = gt(so, nguon) if so else kdd("literal RONG luc dinh nghia: bang duoc dien khi chay (decorator/append)", nguon)
        kq["tinh_ast"][tep] = muc or {"_tep": kad("khong co bang ten DOT_BIEN/TU_KIEM/CA/MUTANT* o muc module")}
    return kq


M4_TEP = (".github/workflows/", "CLAUDE.md", "docs/", "ops/specs/wp1166")
M4_RG1 = r"(?i)đột biến|dot.bien|mutant|mutation|mảnh"
M4_RG2 = (r"(?i)[0-9]+([.,][0-9]+)? ?(s|giây|giay|phút|phut|h|giờ|gio)\b|~ ?[0-9]|"
          r"[0-9]+ (tự đột biến|mutant|đột biến|dot bien|ca|mảnh|manh|muc|mục)\b|[0-9]+/[0-9]+")
M4_LENH = ("rg -n -i 'đột biến|dot.bien|mutant|mutation|mảnh' .github/workflows CLAUDE.md docs ops/specs/wp1166* | rg -i \"<M4_RG2>\" "
           "(tuong duong: hai regex M4_RG1 roi M4_RG2 trong thu_thap.py, ap tren `git show <sha_master>:<tep>`)")


def m4_quet(sha):
    r1, r2 = re.compile(M4_RG1), re.compile(M4_RG2)
    kq = []
    for tep in git_ds(sha, M4_TEP):
        if not (tep.endswith((".yml", ".yaml", ".md"))):
            continue
        for i, l in enumerate((git_show(sha, tep) or "").splitlines(), 1):
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
    run_theo_id = {}
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
        if lan == "duong_nhanh":
            cc_luot.append({"run_id": r["id"], "created_at": lu["created_at"],
                            "dem": dem_theo([m for m in lu["dong"] if m["ten_goc"] == "gate-cong-cu"],
                                            lambda m: "thuc_thi_khong_runner" if m["loai_dong"] == THUC_THI and m["nen"] == "khong_ro" else m["loai_dong"])})
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
        run_theo_id[r["id"]] = lu
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
    m3 = m3_kiem_ke(sha)
    m4 = m4_doi_chieu(sha, m1, m2, m3, run_theo_id, cc_luot)

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
              "tep_tho": [[m["khoa"], m.get("sha256"), m.get("kich_thuoc"), m.get("http"), m.get("url")] + ([m["loi"]] if m.get("loi") else [])
                          for m in manifest]}
    ra.mkdir(parents=True, exist_ok=True)
    (ra / "BASELINE.json").write_text(xuat_json(baseline, 4) + "\n", encoding="utf-8", newline="\n")
    (ra / "COHORT.json").write_text(xuat_json(cohort, 2) + "\n", encoding="utf-8", newline="\n")
    (ra / "BAO_CAO.md").write_text(bao_cao(baseline, cohort), encoding="utf-8", newline="\n")
    print("BASELINE.json sha256", sha256_bytes((ra / "BASELINE.json").read_bytes()))
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
    "rerun": "so_luot_co_rerun = so luot co run_attempt > 1; so_job_hong_o_attempt_truoc = so dong thuc_thi conclusion==failure o attempt < attempt cuoi "
             "(KHONG goi la flaky)",
}


def git_blame_gio(sha, tep, dong):
    """committer-time (UTC) cua commit TREN DUONG first-parent cua `sha` da dua dong `tep:dong` vao (tuc luc dong ay vao nhanh, khong phai
    luc tac gia commit tren nhanh PR); khong doc duoc -> None."""
    nong = subprocess.run(["git", "rev-parse", "--is-shallow-repository"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    if nong != "false":                                   # kho nong: blame dung o bien cat va tra commit SAI
        return None
    r = subprocess.run(["git", "blame", "--first-parent", "--porcelain", "-L", f"{dong},{dong}", sha, "--", tep], cwd=ROOT, capture_output=True, text=True)
    m = re.search(r"^committer-time (\d+)$", r.stdout, re.M) if r.returncode == 0 else None
    return datetime.datetime.fromtimestamp(int(m.group(1)), datetime.timezone.utc) if m else None


def m4_doi_chieu(sha, m1, m2, m3, run_theo_id, cc_luot):
    """Moi dong khop hai regex M4 la mot loi khai. Loi khai co phep do tuong ung trong M1-M3 duoc so; con lai khong_do_duoc kem ly do."""
    mn = m1["luot_du_8_manh_success"]["moi_nhat"]
    imp = m3["import"].get("ops/nhanh_don_duoc_test.py", {})

    def so(ten):
        x = imp.get(ten) or {}
        return x.get("gia_tri") if x.get("trang_thai") == DO_DUOC else None

    def gan(khai, do, sai_so):
        return "khop" if abs(do - khai) <= sai_so * khai else "lech"

    def c_73800():
        if not mn:
            return [("~73 800 s noi tiep", None, KHONG_DO_DUOC, "khong co luot du 8 manh success trong cohort")]
        t = mn["giay_job_manh"]["tong"]
        tb = mn["giay_job_manh"]["trung_vi"]
        ng = f"luot {mn['run_id']} (luot du 8 manh success moi nhat cua cohort): {mn['nguon']}"
        return [("~73 800 s noi tiep", f"{t} s = tong 8 job manh", gan(73800, t, 0.2), "khop neu trong ±20% (loi khai dang '~'); " + ng),
                ("8 manh ≈ 2,6 h/manh (9 360 s)", f"{tb} s = trung vi 8 job manh ({mn['giay_job_manh']['nho_nhat']}–{mn['giay_job_manh']['lon_nhat']} s)",
                 gan(9360, tb, 0.2), "khop neu trong ±20%; " + ng)]

    def c_dem(vi_tri):
        ca, tk, db = so("TU_KIEM"), so("DOT_BIEN_TU_KIEM"), so("DOT_BIEN")
        ng = ("anh xa: '52 ca' <-> len(TU_KIEM), '239 tu dot bien' <-> len(DOT_BIEN_TU_KIEM), '10 dot bien san pham' <-> len(DOT_BIEN); "
              "import ops/nhanh_don_duoc_test.py@" + sha[:12]
              + (f"; doi chieu phu: luot du moi nhat {mn['run_id']} co {mn['so_muc_theo_log']} muc theo log, {mn['so_muc_theo_artifact']} theo artifact"
                 if mn else ""))
        kq = []
        for nhan, khai, do in (("52 ca", 52, ca), ("239 tu dot bien", 239, tk), ("10 dot bien san pham", 10, db)):
            kq.append((nhan, do, KHONG_DO_DUOC if do is None else ("khop" if do == khai else "lech"), ng))
        return kq

    def c_skip(tep, dong):
        nhan = "8 manh skipped (0 phut runner) o duong_nhanh"
        moc = git_blame_gio(sha, tep, dong)
        if moc is None:
            return [(nhan, None, KHONG_DO_DUOC, "git blame khong tra committer-time cho dong loi khai")]
        sau = [x for x in cc_luot if gio(x["created_at"]) is not None and gio(x["created_at"]) > moc]
        if not sau:
            return [(nhan, None, KHONG_DO_DUOC, f"khong co luot duong_nhanh nao tao sau {iso(moc)} trong cohort")]
        tong = {}
        for x in sau:
            for k, n in x["dem"].items():
                tong[k] = tong.get(k, 0) + n
        return [(nhan, f"{len(sau)} luot duong_nhanh tao sau {iso(moc)}: dong gate-cong-cu {tong}; ca cohort ({len(cc_luot)} luot duong_nhanh): "
                       f"{m2['gate_cong_cu_o_luot_duong_nhanh']}",
                 "khop" if tong.get(THUC_THI, 0) == 0 else "lech",   # thuc_thi o day = dong co nhan runner
                 f"chi tinh luot tao SAU committer-time cua dong loi khai (git blame --first-parent --porcelain -L {dong},{dong} {sha[:12]} -- {tep}); "
                 "khop neu khong dong gate-cong-cu nao la thuc_thi CO runner (thuc_thi_khong_runner = dong bi huy truoc khi duoc cap runner: "
                 "labels rong, khong buoc nao, khong phai skipped); lan doc tu log chuan-bi")]

    def c_run(rid, khai_phut, nhan):
        lu = run_theo_id.get(rid)
        if lu is None:
            return [(nhan, None, KHONG_DO_DUOC, f"luot {rid} khong thuoc cohort / khong co du lieu jobs trong anh chup")]
        ds = [m for m in lu["dong"] if m["loai_dong"] == THUC_THI and m["giay"]["trang_thai"] == DO_DUOC and m["ten_goc"].startswith("gate-packet-loop")]
        if not ds:
            return [(nhan, None, KHONG_DO_DUOC, f"luot {rid} khong co dong thuc_thi gate-packet-loop* hop le")]
        j = max(ds, key=lambda m: (m["giay"]["gia_tri"], m["job_id"]))
        g = j["giay"]["gia_tri"]
        bc = [thoi_luong_buoc(b) for b in j["_tho"].get("steps") or []]
        bmax = max([x["gia_tri"] for x in bc if x["trang_thai"] == DO_DUOC], default=None)
        return [(nhan, f"job {j['ten']} dai nhat cua luot: {g} s = {g // 3600} gio {g % 3600 // 60} phut {g % 60} giay; buoc dai nhat cua job ay: {bmax} s",
                 "khop" if khai_phut in (g // 60, round(g / 60)) else "lech",
                 f"khop neu thoi luong JOB cat hoac lam tron ve phut bang {khai_phut} phut; {lu['nguon']}")]

    luat = [
        (".github/workflows/ci-dot-bien-du.yml", "73 800 s", lambda t, d: c_73800()),
        (".github/workflows/ci-dot-bien-du.yml", "52 ca dưới MỖI 239", lambda t, d: c_dem("du")),
        (".github/workflows/ci.yml", "52 ca nền + 239 tự đột biến", lambda t, d: c_dem("ci")),
        (".github/workflows/ci.yml", "8 mảnh `skipped` (0 phút runner)", c_skip),
        (".github/workflows/ci.yml", "đo run 43845962754: một job 2 giờ", lambda t, d: c_run(43845962754, 141, "run 43845962754: mot job 2 gio 21 phut")),
    ]
    ly_do_mac_dinh = ("khong co phep do tuong ung trong cohort M1-M3: loi khai ve bo/workflow/moc thoi gian ngoai hai workflow cua cohort, "
                      "hoac la bien ban lich su co ngay, hoac con so chi sinh khi CHAY bo (packet khong chay)")
    kq = []
    for tep, dong, van in m4_quet(sha):
        ham = [h for t, mau, h in luat if t == tep and mau in van]
        ng = f"{tep}:{dong}@{sha[:12]}"
        if not ham:
            kq.append({"vi_tri": ng, "trich": van[:200], "loi_khai": None, "so_do": None, "ket_luan": KHONG_DO_DUOC, "ly_do": ly_do_mac_dinh})
            continue
        for h in ham:
            for nhan, do, kl, ghi in h(tep, dong):
                kq.append({"vi_tri": ng, "trich": van[:200], "loi_khai": nhan, "so_do": do, "ket_luan": kl, "ly_do": ghi})
    return {"lenh": M4_LENH, "regex_1": M4_RG1, "regex_2": M4_RG2, "so_dong_khop": len({x["vi_tri"] for x in kq}),
            "theo_ket_luan": dem_theo(kq, lambda x: x["ket_luan"]), "loi_khai": kq}


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
    def tk(o, don_vi="s"):
        return "—" if not o or o.get("trang_thai") != DO_DUOC else f"n={o['n']} · tổng {o['tong']} · trung vị {o['trung_vi']} · p90 {o['p90']} · max {o['lon_nhat']} {don_vi}" + (f" · loại {o['so_loai']}" if o.get("so_loai") else "")
    def v(o):
        return str(o["gia_tri"]) if o["trang_thai"] == DO_DUOC else f"{o['trang_thai']} ({o.get('ly_do')})"
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
    w("| nguồn | yêu cầu | có | hết hạn | cắt cụt | lỗi | không thu (hết khung) | có log, không có bản ghi |")
    w("|---|---|---|---|---|---|---|---|")
    for k, o in b["do_phu"].items():
        w(f"| {k} | {o['yeu_cau']} | {o['co']} | {o['het_han']} | {o['cat_cut']} | {o['loi']} | {o['khong_thu']} | {o['khong_co_ban_ghi']} |")
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
    w("\n| job gốc \\| nền | thống kê giây (dòng thực thi, mọi lượt) |\n|---|---|")
    for k, o in m1["theo_job"].items():
        w(f"| {k} | {tk(o)} |")
    mk = m1["muc_ket_qua_theo_khoa"]["bang"]
    w(f"\nDòng `KET QUA` trong log mảnh: {len(mk)} khoá (chế độ | khoá). 10 khoá có trung vị giây lớn nhất:\n")
    w("| chế độ \\| khoá | n | trung vị s | p90 s | max s |\n|---|---|---|---|---|")
    for k, o in sorted(((k, o) for k, o in mk.items() if o.get("trang_thai") == DO_DUOC), key=lambda x: (-x[1]["trung_vi"], x[0]))[:10]:
        w(f"| {k} | {o['n']} | {o['trung_vi']} | {o['p90']} | {o['lon_nhat']} |")
    w("\nTừng lượt, từng job, từng bước job mảnh, từng artifact: `BASELINE.json` → `M1.luot`.\n")
    w("## M2 — gate CI (`ci.yml`)\n")
    w(f"- {m2['so_luot']} lượt · kết luận {m2['theo_ket_luan']} · làn {m2['theo_lan']} · lượt có rerun {m2['so_luot_co_rerun']} · job hỏng ở attempt trước {m2['so_job_hong_o_attempt_truoc']}")
    w("\n| sự kiện \\| làn | lượt | giây thực thi | đầu-cuối suy ra từ job |\n|---|---|---|---|")
    for k, o in [("tất cả", m2["moi_luot"]["tat_ca"])] + list(m2["moi_luot"]["theo_su_kien_va_lan"].items()):
        w(f"| {k} | {o['so_luot']} | {tk(o['giay_thuc_thi'])} | {tk(o['dau_cuoi_suy_ra_tu_job'])} |")
    w("\nJob nhóm `gate*` (làn `day_du`, dòng thực thi; đủ mọi làn/nền ở `M2.theo_job`):\n")
    w("| job gốc \\| nền \\| làn | thống kê giây | bỏ qua | mang sang | kết luận |\n|---|---|---|---|---|")
    for k, o in m2["theo_job"]["bang"].items():
        if k.endswith("| day_du") and " | _ | " not in k:
            w(f"| {k} | {tk(o)} | {o['so_bo_qua']} | {o['so_mang_sang']} | {o['ket_luan']} |")
    bb = [(k, o) for k, o in m2["theo_buoc"]["bang"].items() if o.get("trang_thai") == DO_DUOC]
    w(f"\nBước của `gate-cong-cu*`, `gate-nhanh-*`, `gate-registry`, `gate-packet-loop*`: {len(m2['theo_buoc']['bang'])} khoá ở `M2.theo_buoc`. 12 khoá có tổng giây lớn nhất:\n")
    w("| job gốc \\| nền \\| làn \\| bước | thống kê giây |\n|---|---|")
    for k, o in sorted(bb, key=lambda x: (-x[1]["tong"], x[0]))[:12]:
        w(f"| {k} | {tk(o)} |")
    w("\n## M2b — thời gian theo bộ test và chế độ (`CI_DANG_KY_THOI_GIAN`)\n")
    w(f"{len(b['M2b']['bang'])} khoá (job nguồn | nền | bộ). 15 khoá có tổng giây lớn nhất:\n")
    w("| job nguồn \\| nền \\| bộ | bản ghi | rc≠0 | chế độ: n / trung vị / p90 (s) |\n|---|---|---|---|")
    def tong_bo(o):
        return sum(c.get("tong", 0) for c in o["che_do"].values())
    for k, o in sorted(b["M2b"]["bang"].items(), key=lambda x: (-tong_bo(x[1]), x[0]))[:15]:
        cd = "; ".join(f"{c}: {s['n']} / {s.get('trung_vi', '—')} / {s.get('p90', '—')}" for c, s in o["che_do"].items())
        w(f"| {k} | {o['so_ban_ghi']} | {o['rc_khac_0']} | {cd} |")
    w("\n## M3 — kiểm kê tĩnh\n")
    for tep, bang in b["M3"]["import"].items():
        w(f"- `{tep}` (import, `len()`): " + " · ".join(f"{n}={v(x)}" for n, x in bang.items()))
    ast_do = [(t, n, x) for t, bg in b["M3"]["tinh_ast"].items() for n, x in bg.items()]
    w(f"- Đếm literal bằng `ast` trên {len(b['M3']['tinh_ast'])} bộ `*_test.py` ở SHA meta: {sum(1 for _, _, x in ast_do if x['trang_thai'] == DO_DUOC)} bảng đo được, "
      f"{sum(1 for _, _, x in ast_do if x['trang_thai'] == KHONG_DO_DUOC)} `khong_do_duoc` (chỉ sinh khi chạy/import), "
      f"{sum(1 for _, _, x in ast_do if x['trang_thai'] == KHONG_AP_DUNG)} bộ không có bảng tên chuẩn.")
    w("\n| bộ | bảng đo được bằng ast |\n|---|---|")
    for t, bg in b["M3"]["tinh_ast"].items():
        co = [f"{n}={x['gia_tri']}" for n, x in bg.items() if x["trang_thai"] == DO_DUOC]
        if co:
            w(f"| `{t}` | {' · '.join(co)} |")
    w("\n## 5 điểm tốn thời gian nhất theo giây thực thi (nhóm job, cả cohort)\n")
    w("| # | workflow | job gốc | tổng giây thực thi | số dòng thực thi | trung vị s |\n|---|---|---|---|---|---|")
    for i, x in enumerate(b["top5_giay_thuc_thi"], 1):
        w(f"| {i} | {x['workflow']} | {x['job_goc']} | {x['tong_giay_thuc_thi']} | {x['so_dong_thuc_thi']} | {x['trung_vi_giay']} |")
    w("\nNguồn: tổng `completed_at − started_at` của mọi dòng `thuc_thi` cùng tên gốc trong các tệp `jobs/*` của ảnh chụp (URL từng lượt ở `M1.luot[].nguon`, `actions/runs/<id>/jobs?filter=all`).\n")
    m4 = b["M4"]
    w("## M4 — đối chiếu lời khai\n")
    w(f"Lệnh: `{m4['lenh']}`. {m4['so_dong_khop']} dòng khớp; kết luận: {m4['theo_ket_luan']}.\n")
    w("| vị trí | lời khai | số đo | kết luận | ghi chú |\n|---|---|---|---|---|")
    for x in m4["loi_khai"]:
        if x["loi_khai"]:
            w(f"| `{x['vi_tri']}` | {x['loi_khai']} | {x['so_do']} | **{x['ket_luan']}** | {x['ly_do']} |")
    w("\n## Lời khai lệch\n")
    lech = [x for x in m4["loi_khai"] if x["ket_luan"] == "lech"]
    for x in lech:
        w(f"- `{x['vi_tri']}` — khai “{x['loi_khai']}”, đo {x['so_do']}. {x['ly_do']}")
    if not lech:
        w("- (không có lời khai nào kết luận `lech`)")
    w("\n## Không đo được\n")
    kd = b["khong_do_duoc"]
    w(f"{kd['so_muc']} mục nguồn (chi tiết + URL ở `BASELINE.json` → `khong_do_duoc.chi_tiet`). Tóm tắt theo dạng:\n")
    for k, n in sorted(kd["tom_tat"].items(), key=lambda x: (-x[1], x[0]))[:14]:
        w(f"- {n} × {k}")
    if len(kd["tom_tat"]) > 14:
        w(f"- … và {len(kd['tom_tat']) - 14} dạng khác (xem `khong_do_duoc.tom_tat`)")
    w(f"- Lời khai M4 không có phép đo tương ứng: {m4['theo_ket_luan'].get(KHONG_DO_DUOC, 0)} (danh sách ở `M4.loi_khai`).")
    w("- M3: bảng không phải literal tĩnh hoặc literal rỗng được điền khi chạy — ghi `khong_do_duoc`, không chạy bộ để lấy số.")
    w("- Thời điểm workflow hoàn tất: API attempt không trả `completed_at`; chỉ có `dau_cuoi_suy_ra_tu_job`.")
    w("- Workflow đột biến ngoài cohort (vd. `packet-loop-dot-bien.yml`) không được thu: đặc tả §2 chỉ định hai workflow.")
    w("\n## Kết quả hai bộ phân loại §6 (trên tập đường dẫn của packet)\n")
    s6 = phan_loai_s6()
    w("Tập đường dẫn (mọi tệp là `A`, mode `100644`): " + ", ".join(f"`{t}`" for t in s6["tap_duong_dan"]))
    for k in ("phan_loai_tu_diff", "ly_do_ve_day_du", "phan_loai_packet_loop", "ci_duong_nhanh", "tim"):
        if k in s6:
            w(f"- `{k}` ⇒ `{json.dumps(s6[k], ensure_ascii=False)}`")
    w("\nLàn của PR phải được đo lại trên log CI thật trước merge (đặc tả §6); kết quả trên là phép chạy tại chỗ của hai hàm phân loại.")
    return "\n".join(L) + "\n"


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
    ns = ap.parse_args()
    if sum((ns.thu, ns.tinh, ns.tu_kiem)) != 1:
        ap.error("chon DUNG MOT trong --thu | --tinh | --tu-kiem")
    if ns.tu_kiem:
        return lenh_tu_kiem()
    if ns.thu:
        if not ns.ra:
            ap.error("--thu can --ra <anh chup>")
        return lenh_thu(ns)
    if not (ns.anh_chup and ns.ra):
        ap.error("--tinh can --anh-chup <anh chup> --ra <thu muc>")
    return lenh_tinh(ns)


if __name__ == "__main__":
    sys.exit(main())
