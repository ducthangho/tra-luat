#!/usr/bin/env python3
"""Watchdog do tuoi bien nhan full audit (wp1494, B2 cua Mission #1172). Dac ta: ops/specs/wp1494-r1/SPEC.md (nhanh ops/wp1494-r1).

Doc REST cac luot `schedule` cua `.github/workflows/ci-dot-bien-du.yml`, phan bien nhan B1a bang luat C1-C12 voi dau vao doc lap,
xep vao `fresh` · `due_in_progress` · `stale_or_missing` · `khong_do_duoc`, roi ghi nhip tim va thong bao len MOT Issue theo doi.
Khong doc duoc thi khong bao gio la `fresh`. Chi bao cao: khong chan merge, khong chan release. Hang nam trong ma (I3): khong
bien moi truong hay tham so nao doi kho, workflow duoc canh, so Issue, hang thoi gian, ngan sach hay tran."""
import base64
import datetime
import hashlib
import importlib
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

KHO = "ducthangho/tra-luat"
WORKFLOW_CANH = ".github/workflows/ci-dot-bien-du.yml"
API = "https://api.github.com/repos/" + KHO
ISSUE_THEO_DOI = 1520                      # Issue theo doi do dieu phoi tao truoc lease (muc 7); workflow khong tao, khong tim Issue
KHUNG_DAU = "2026-11-28T19:17:00Z"         # khung nho nhat >= thoi diem committer cua commit merge PR B1a (muc 2); khung truoc no khong mang nghia vu
KHUNG_DONG_TAY = {}                        # khung hop le (<= P) -> ly do ASCII; them muc la viec cua mot PR sau co review
KENH_GIAO_TIN_XAC_NHAN = None              # muc 10: chua do; dien URL xac nhan la viec cua mot PR sau
TRE_LICH_TOI_DA = datetime.timedelta(hours=12)
TUOI_TOI_DA = datetime.timedelta(days=8)   # khong co hang 36 h (muc 2): an han hieu dung la 24 h tu tran tuoi nay
LE_DOI_SOAT = datetime.timedelta(hours=24)
HAN_GOI, THU_LAI_GET, CHO_THU_LAI = 30, 2, (1, 2)
NGAN_SACH_DANH_GIA, NGAN_SACH_GHI = 600, 180
TRANG_TOI_DA, SO_KHUNG_SOAT_TOI_DA = 10, 6
TRAN_GOI, TRAN_MUC_ZIP, TRAN_GIAI_NEN, TRAN_GIAI_NEN_TONG = 50 * 2**20, 1000, 64 * 2**20, 256 * 2**20
DUONG_SCHEMA = "ops/specs/wp1460-r1/hop_dong/bien_nhan_audit.v1.schema.json"
BAM_SCHEMA = "844b5218b6f6844945f5c4c9440f09015d238fe09a60d64b3787c440787e4f46"   # GHIM-B1A
DAT, KHONG_DAT, KHONG_DO_DUOC = "dat", "khong_dat", "khong_do_duoc"

# ---- GHIM-B1A: CHEP NGUYEN VAN tu khoi ma "Lenh kiem" cua ops/specs/wp1460-r1/SPEC.md revision 7 (nhanh ops/wp1460-r1, commit
# d1b08c219227d4b8925702029cd20d4e0febed54; sha256 khoi ma d9c78e708e18a211b7d8c7309638ffd1c73200578cf3128f9f0fc4275430f24e):
# dong hang va bon ham `khoa_tu_ten`, `doc_moc`, `khung_cron`, `tieu_dung`. KHONG sua mot ky tu nao trong doan nay; `tieu_dung`
# la dinh nghia chuan tac cua luat C1-C12. Thuoc do: nghiem thu 3 cua ops/canh_tuoi_audit_test.py (fixture chung cua B1a).
JOB_THU, JOB_GOP, TIEN_TO_MANH, CRON_GHIM = "bien-nhan-audit", "dot-bien-gop", "dot-bien-manh", "17 19 * * 6"

def khoa_tu_ten(ten):
    m = re.fullmatch(r"(.+) \((.+)\)", ten)
    return f"{m[1]}-{m[2]}" if m else ten

def doc_moc(v):
    try:
        return datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ")
    except (TypeError, ValueError):
        return None

def khung_cron(tao):
    """Moc `17 19 * * 6` (thu Bay 19:17 UTC) gan nhat <= tao."""
    t = tao.replace(hour=19, minute=17, second=0) - datetime.timedelta(days=(tao.weekday() - 5) % 7)
    return t if t <= tao else t - datetime.timedelta(days=7)

def tieu_dung(V, b, rest, ngoai, bo=None, hop_le=None):
    """Luat C cua ben tieu dung, tung VI TU co ten. Tra (tap luat vi pham, canh bao, moc tinh tuoi). `bo` = ten vi tu bi go (dot bien);
    `hop_le` = ket qua kiem hinh da co cua b (None thi tu kiem)."""
    if not (V["bien_nhan"].is_valid(b) if hop_le is None else hop_le) or b["ok"] is not True:
        return {"C1"}, [], None
    vp, run, lu, sk = set(), rest["run"], b["luot"], b["su_kien"]
    def vt(ten, dk):                           # ten = "<luat>.<vi tu>"
        if ten != bo and not dk: vp.add(ten.split(".")[0])
    E = ngoai["job_ky_vong"]                   # ten job ben tieu dung TU lap tu tep workflow tai H
    moi = {}                                   # ten job -> ban ghi REST co run_attempt lon nhat
    for j in rest["jobs"]:
        if j["name"] not in moi or j["run_attempt"] > moi[j["name"]]["run_attempt"]:
            moi[j["name"]] = j
    cap = [(j["name"], j["run_attempt"]) for j in rest["jobs"]]
    vt("C1.attempt_moi_nhat", lu["run_attempt"] == run["run_attempt"])
    vt("C2.run_completed", run["status"] == "completed")
    vt("C2.run_success", run["conclusion"] == "success")
    vt("C2.moi_job_success", all(j["conclusion"] == "success" for j in moi.values()))
    vt("C3.kho", b["kho"] == run["repository"]["full_name"])
    vt("C3.kho_id", b["kho_id"] == run["repository"]["id"])
    vt("C3.duong_dan", b["workflow"]["duong_dan"] == run["path"])
    vt("C3.run_id", lu["run_id"] == run["id"])
    vt("C3.su_kien_ten", sk["ten"] == run["event"])
    vt("C3.sha_rest", sk["sha"] == run["head_sha"])
    vt("C3.sha_h", sk["sha"] == ngoai["h"])
    hang = {r["ten"]: r for r in b["job"]}
    vt("C4.rest_khong_trung", len(cap) == len(set(cap)))
    vt("C4.rest_du", set(moi) == set(E))
    vt("C4.dong_khong_trung", len(b["job"]) == len(hang))
    vt("C4.tap_ten", set(hang) == set(E))
    vt("C4.ky_vong", b["kiem_ke_job"]["ky_vong"] == sorted(E))
    vt("C4.thuc_co", b["kiem_ke_job"]["thuc_co"] == sorted(E))
    cung = [(r, moi[t]) for t, r in hang.items() if t in moi]
    vt("C4.job_id", all(r["job_id"] == j["id"] for r, j in cung))
    vt("C4.run_attempt", all(r["run_attempt"] == j["run_attempt"] for r, j in cung))
    vt("C4.khoa", all(r["khoa"] == khoa_tu_ten(r["ten"]) for r in b["job"]))
    vt("C4.tu_than", all(r["tu_than"] == (r["ten"] == JOB_THU) for r in b["job"]))
    vt("C4.ten_dau", all(r["dau_job"]["ten"] == f"dau-job-{lu['run_id']}-{j['run_attempt']}-{khoa_tu_ten(r['ten'])}" for r, j in cung))
    vt("C5.job_sha", all(r["checkout_sha"] == sk["sha"] for r in b["job"]))
    vt("C5.manh_head", all(m["head"] == sk["sha"] for m in b["manh"]))
    vt("C5.tree_h", all(r["checkout_tree"] == ngoai["tree_h"] for r in b["job"]))
    ky = {}                                    # khoa job manh -> k, lap tu E (doc lap voi bien nhan va REST)
    for t in E:
        m = re.fullmatch(re.escape(TIEN_TO_MANH) + r" \((0|[1-9][0-9]*)\)", t)
        if m: ky[khoa_tu_ten(t)] = int(m[1])
    ten_theo_khoa = {khoa_tu_ten(t): t for t in E}
    att = lambda khoa: moi.get(ten_theo_khoa.get(khoa), {}).get("run_attempt")   # attempt REST moi nhat cua job mang khoa ay
    co = [m for m in b["manh"] if m["khoa_job"] in ky and att(m["khoa_job"]) is not None]
    vt("C6.manh_khong_trung", len(b["manh"]) == len({m["khoa_job"] for m in b["manh"]}))
    vt("C6.tap_manh", {m["khoa_job"] for m in b["manh"]} == set(ky))
    vt("C6.job_le_luot", all(j["run_attempt"] <= lu["run_attempt"] for j in moi.values()))
    vt("C6.chi_so", all(m["manh"] == ky[m["khoa_job"]] for m in co))
    vt("C6.attempt", all(m["attempt_ben_san_xuat"] == att(m["khoa_job"]) for m in co))
    vt("C6.le_gop", att(JOB_GOP) is not None and all(att(m["khoa_job"]) <= att(JOB_GOP) for m in co))
    vt("C6.ten_artifact", all(m["artifact"]["ten"] == f"{TIEN_TO_MANH}-{lu['run_id']}-{att(m['khoa_job'])}-{ky[m['khoa_job']]}" for m in co))
    vt("C7.job_truoc", b["dau_hieu_duong"]["job_truoc_success"] == f"{len(E) - 1}/{len(E) - 1}")
    vt("C7.manh", b["dau_hieu_duong"]["manh"] == f"{len(ky)}/{len(ky)}")
    kho = {a["id"]: a for a in rest["artifacts"]}
    dau = [(r["dau_job"], "dau-job.json", r) for r in b["job"]]
    mnh = [(m["artifact"], f"manh-{m['manh']}.json", m) for m in b["manh"]]
    cr = [(a, kho[a["id"]]) for a, _, _ in dau + mnh if a["id"] in kho]
    ct = [(a, ten, d, ngoai["tai_ve"][str(a["id"])]) for a, ten, d in dau + mnh if str(a["id"]) in ngoai["tai_ve"]]
    c1 = [x for x in ct if len(x[3]["tep"]) == 1 and x[3]["tep"][0]["ten"] == x[1]]      # dung MOT tep, dung ten
    vt("C8.co_trong_rest", len(cr) == len(dau + mnh))
    vt("C8.ten", all(a["ten"] == r["name"] for a, r in cr))
    vt("C8.digest_rest", all(a["digest"] == r["digest"] for a, r in cr))
    vt("C8.chua_het_han", all(r["expired"] is False for a, r in cr))
    vt("C8.da_tai", len(ct) == len(dau + mnh))
    vt("C8.goi", all(a["digest"] == "sha256:" + t["sha256_goi"] for a, _, _, t in ct))
    vt("C8.mot_tep", len(c1) == len(ct))
    vt("C8.tep_bam", all(a["sha256_noi_dung"] == t["tep"][0]["sha256"] for a, _, _, t in c1))
    nd = [(t["tep"][0]["noi_dung"], d) for a, ten, d, t in c1 if ten == "dau-job.json"]
    nho = V.setdefault("nho", {})                # nho ket qua kiem hinh dau theo noi dung
    def dau_hop_le(n):
        k = json.dumps(n, sort_keys=True)
        if k not in nho: nho[k] = V["dau_job"].is_valid(n)
        return nho[k]
    ok = [(n, d) for n, d in nd if dau_hop_le(n)]
    vt("C11.hinh", len(ok) == len(nd))
    vt("C11.khoa_job", all(n["khoa_job"] == d["khoa"] for n, d in ok))
    vt("C11.run_id", all(n["run_id"] == lu["run_id"] for n, d in ok))
    vt("C11.run_attempt", all(n["run_attempt"] == d["run_attempt"] for n, d in ok))
    vt("C11.su_kien_sha", all(n["su_kien_sha"] == sk["sha"] for n, d in ok))
    vt("C11.checkout_sha", all(n["checkout_sha"] == d["checkout_sha"] for n, d in ok))
    vt("C11.checkout_tree", all(n["checkout_tree"] == d["checkout_tree"] for n, d in ok))
    nm = [(t["tep"][0]["noi_dung"], d) for a, ten, d, t in c1 if ten != "dau-job.json"]
    om = [(n, d) for n, d in nm if isinstance(n, dict)]
    vt("C12.la_object", len(om) == len(nm))
    vt("C12.head", all(n.get("head") == d["head"] for n, d in om))
    vt("C12.manh", all(type(n.get("manh")) is int and n.get("manh") == d["manh"] for n, d in om))
    tao = doc_moc(sk["run_created_at"])
    vt("C9.tao_khop_rest", sk["run_created_at"] == run["created_at"])
    vt("C9.lich_hop_le", tao is not None)
    if sk["ten"] == "schedule":
        vt("C9.cron_ghim", sk["cron"] == CRON_GHIM)
        vt("C9.khung", tao is None or sk["khung_danh_nghia_utc"] == khung_cron(tao).strftime("%Y-%m-%dT%H:%M:%SZ"))
    canh = ["C10"] if bo != "C10.canh_bao" and b["dinh_danh_definition"]["trang_thai"] == "not_measured" else []
    return vp, canh, sk.get("khung_danh_nghia_utc") or sk["run_created_at"]

# ---- het doan GHIM-B1A ----

# ---- Hang phu va ham nho ----
HONG, VUOT, KHONG_BIET = object(), object(), object()   # nguyen ham HONG · khong hoan tat vi tran tai nguyen · da_bao khong biet
W_TT, G_TT = ("stale_or_missing", KHONG_DO_DUOC), ("fresh", "due_in_progress")
TT4 = G_TT + W_TT
MA_SOM = {"fresh": ("khung_xanh",), "due_in_progress": ("khung_dang_cho",),
          "stale_or_missing": ("khung_do", "slot_cu_chua_dong", "khung_vang", "qua_tuoi_8_ngay", "khung_truoc_khong_xanh")}
LOAI = ("canh_bao", "hoi_phuc", "nhip_tim_gian_doan")
KHOA_SK = {"id", "loai", "trang_thai", "khung", "ma_ly_do"}
KHOA_NT = {"schema", "luc", "run_id", "run_attempt", "trang_thai", "ma_ly_do", "khung", "sha_audit", "sha_master", "dong_den", "da_bao", "cho_bao"}
RE_GIO, RE_MA = re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ"), re.compile(r"[a-z0-9_]{1,64}")
RE_SHA, RE_ID_SK = re.compile(r"[0-9a-f]{40}"), re.compile(r"[1-9][0-9]{0,19}-[1-9][0-9]{0,9}")
BAY_NGAY = datetime.timedelta(days=7)
DONG_1 = "B2 watchdog do tuoi full audit (wp1494). Than Issue do workflow ghi de moi luot; dung sua tay."
TT_NT, TT_SK, BOT, DAU = "B2_NHIP_TIM: ", "B2_SU_KIEN: ", "github-actions[bot]", "x-github-request-id"
LIEN_KET = (   # truong BAT BIEN so giua phan tu D1 va moi ban doc D2, theo dung thu tu nay
    "id",  # lk
    "created_at",  # lk
    "event",  # lk
    "path",  # lk
    "head_branch",  # lk
    "head_sha",  # lk
    "workflow_id",  # lk
    "repository.full_name",  # lk
    "repository.id",  # lk
)

def gio(v):
    """Chuoi `YYYY-MM-DDTHH:MM:SSZ` khop tron va la thoi diem co that -> datetime; khac -> None."""
    return doc_moc(v) if isinstance(v, str) and RE_GIO.fullmatch(v) else None

def viet(t): return t.strftime("%Y-%m-%dT%H:%M:%SZ")

def khung_hop_le(v):
    t = gio(v)
    return t is not None and khung_cron(t) == t

def dau_ma(ma):
    """DAU MA cua mot ma chi tiet `<dau>` hoac `<dau>:<duoi>` — thu duy nhat di vao nhip tim, su kien va comment."""
    return ma.split(":")[0]

def _lay(o, duong):
    for k in duong.split("."):
        o = o.get(k) if isinstance(o, dict) else None
    return o

def _so_nguyen(v): return type(v) is int   # `bool` khong tinh

def _dumps(x): return json.dumps(x, ensure_ascii=True, sort_keys=True, separators=(",", ":"))

def _sha(byte): return hashlib.sha256(byte).hexdigest()

def _ma_nem(diem, e):
    """Ma chi tiet cua mot nguyen ham HONG (muc 3): `<diem>_nem:<module>.<qualname>`."""
    return f"{diem}_nem:{type(e).__module__}.{type(e).__qualname__}"

# ---- Nguyen ham (bien ngoai le, muc 3): moi khoi `try` chi chua dung mot loi goi va phep gan ket qua ----
def _tho_json(byte): return json.loads(byte.decode("utf-8"))

def doc_json(byte):
    try:
        x = _tho_json(byte)
    except Exception as e:  # bien:doc_json
        return HONG, _ma_nem("doc_json", e)
    return x, None

def _tho_zip(c, byte):
    """DOC-ZIP: danh sach (ten, byte) cua moi TEP, hoac VUOT khi vuot tran tai nguyen. Byte giai nen duoc DEM khi doc theo khuc."""
    z = zipfile.ZipFile(io.BytesIO(byte))
    muc, tep, dem = z.infolist(), [], 0
    if len(muc) > c.tran["TRAN_MUC_ZIP"]:  # d108
        return VUOT
    for m in muc:
        if m.filename.endswith("/"):  # d44
            continue
        f, khuc = z.open(m), []
        while True:
            b = f.read(min(2**20, c.tran["TRAN_GIAI_NEN"] + 1 - dem))
            if not b:
                break
            dem, c.giai_nen = dem + len(b), c.giai_nen + len(b)
            if c.giai_nen > c.tran["TRAN_GIAI_NEN_TONG"]:  # d110
                c.can_tn = True
                return VUOT
            if dem > c.tran["TRAN_GIAI_NEN"]:  # d109 d112
                return VUOT  # d111
            khuc.append(b)
        tep.append((m.filename, b"".join(khuc)))
    return tep

def doc_zip(c, byte):
    try:
        r = _tho_zip(c, byte)
    except Exception as e:  # bien:doc_zip
        return HONG, _ma_nem("doc_zip", e)
    return r, None

def _tho_nap_thu_vien(ten, schema=None):
    if ten == "yaml":
        return importlib.import_module("yaml")
    js = importlib.import_module("jsonschema")
    js.Draft202012Validator.check_schema(schema)
    return {"bien_nhan": js.Draft202012Validator(schema),
            "dau_job": js.Draft202012Validator({"$schema": schema["$schema"], "$ref": "#/$defs/dau_job_v1", "$defs": schema["$defs"]})}

def nap_thu_vien(ten, schema=None):
    try:
        r = _tho_nap_thu_vien(ten, schema)
    except Exception as e:  # bien:nap_thu_vien
        return HONG, _ma_nem("nap_thu_vien", e)
    return r, None

def _tho_yaml(mo_dun, byte): return mo_dun.safe_load(byte)

def doc_yaml(mo_dun, byte):
    try:
        r = _tho_yaml(mo_dun, byte)
    except Exception as e:  # bien:yaml
        return HONG, _ma_nem("yaml", e)
    return r, None

def goi_tieu_dung(V, b, rest, ngoai):
    try:
        r = tieu_dung(V, b, rest, ngoai)
    except Exception as e:  # bien:tieu_dung
        return HONG, _ma_nem("tieu_dung", e)
    return r, None

def goi_kiem_nhip_tim(x, T_doc, khung_dau):
    """Bo kiem mien dung chung cho nguoi doc va nguoi ghi. Tra None khi dat, khong thi ma."""
    try:
        r = kiem_nhip_tim(x, T_doc, khung_dau)
    except Exception as e:  # bien:kiem_nhip_tim
        return _ma_nem("kiem_nhip_tim", e)
    return r

# ---- Transport, luat thu lai, han tuyet doi (muc 3) ----
class _NguCanh:
    def __init__(self, transport, dong_ho, ngu, token, tran):
        self.transport, self.dong_ho, self.ngu, self.token = transport, dong_ho, ngu, token
        self.tran = dict({"TRAN_GOI": TRAN_GOI, "TRAN_MUC_ZIP": TRAN_MUC_ZIP, "TRAN_GIAI_NEN": TRAN_GIAI_NEN, "TRAN_GIAI_NEN_TONG": TRAN_GIAI_NEN_TONG}, **(tran or {}))
        self.han, self.pha_dg, self.can_dg, self.can_tn, self.giai_nen, self.nho = 0.0, False, False, False, 0, {}

def _mot_lan(c, pt, url, hd, than, timeout):
    """MOT lan thu vat ly: gui, roi doc than theo khuc va dung o byte thu TRAN_GOI + 1."""
    ma, hd_ra, luong = c.transport(pt, url, hd, than, timeout)
    khuc, n = [], 0
    while True:
        b = luong.read(min(65536, c.tran["TRAN_GOI"] + 1 - n))
        if not b:
            break
        n += len(b)
        if n > c.tran["TRAN_GOI"]:  # d107
            return ma, {k.lower(): v for k, v in hd_ra.items()}, VUOT
        khuc.append(b)
    return ma, {k.lower(): v for k, v in hd_ra.items()}, b"".join(khuc)

def _goi(c, pt, url, than=None):
    """Mot loi goi = cac lan thu VAT LY theo luat cua phuong thuc. Tra (ma HTTP, header, byte | VUOT) hoac (None, ma loi, None)."""
    so_lan = THU_LAI_GET + 1 if pt in ("GET",) else 1  # d49 d50 d51
    for lan in range(so_lan):
        con = c.han - c.dong_ho()
        if con <= 0:  # d105
            c.can_dg = c.can_dg or c.pha_dg
            return None, "het_gio", None
        hd = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        if urllib.parse.urlsplit(url).hostname == "api.github.com":  # d47
            hd["Authorization"] = "Bearer " + c.token
        try:
            kq = _mot_lan(c, pt, url, hd, than, min(HAN_GOI, con))  # d100 d101
        except Exception as e:  # bien:transport
            kq = (None, _ma_nem("transport", e), None)
        if not (kq[0] is None or kq[0] >= 500 or kq[0] == 429) or lan + 1 == so_lan:
            return kq
        cho = CHO_THU_LAI[min(lan, len(CHO_THU_LAI) - 1)]
        if c.dong_ho() + cho >= c.han:  # d104
            c.can_dg = c.can_dg or c.pha_dg
            return kq
        c.ngu(cho)

def _j(c, url, hinh, pt="GET", than=None):
    """Lop J: 2xx co dau GitHub va than la JSON dung hinh. Tra (gia tri, header) hoac (None, ma)."""
    ma, hd, byte = _goi(c, pt, url, than)
    if ma is None:
        return None, hd
    if not 200 <= ma < 300:  # d121
        return None, (f"http_github:{ma}" if DAU in hd else f"khong_dau_github:{ma}")
    if DAU not in hd:  # d48
        return None, f"khong_dau_github:{ma}"
    if byte is VUOT:
        return None, "than_vuot_tran"
    x, _ = doc_json(byte)
    if x is HONG:
        return None, "json_hong"
    if not hinh(x):  # d122
        return None, "json_sai_kieu"
    return x, dict(hd, **{":ma": ma})

def _la_dict(x): return isinstance(x, dict)

def _liet_ke(c, url, khoa):
    """Danh sach TRON (U1) va `id` la khoa duy nhat (U2). Tra (danh sach, None) hoac (None, ma)."""
    ds, tong, trang = [], None, 0
    hinh = (lambda v: isinstance(v, dict) and isinstance(v.get(khoa), list) and _so_nguyen(v.get("total_count"))) if khoa else (lambda v: isinstance(v, list))
    while url:
        if trang == TRANG_TOI_DA:  # d93
            return None, "khong_tron"  # d07 d69
        x, hd = _j(c, url, hinh)
        if x is None:
            return None, hd
        ds, tong, trang = ds + (x[khoa] if khoa else x), (x["total_count"] if khoa else None), trang + 1
        m = re.search(r'<([^>]+)>;\s*rel="next"', hd.get("link", ""))
        url = m[1] if m else None
    if khoa and len(ds) != tong:  # d08
        return None, "tong_lech"
    ids = [p.get("id") if isinstance(p, dict) else None for p in ds]
    if any(type(i) is not int or i < 1 for i in ids):  # d123
        return None, "danh_sach_sai_kieu"
    if len(set(ids)) != len(ids):
        return None, "danh_sach_trung_id"  # d09
    return ds, None

def _tai(c, aid):
    """D5 qua lop R (302 co dau tu api.github.com, Location https, toi da 3 lan) roi lop S (200 tron, khong Authorization)."""
    url = f"{API}/actions/artifacts/{aid}/zip"
    for _ in range(4):  # d118
        ma, hd, byte = _goi(c, "GET", url)
        if ma is None:
            return None, hd
        if urllib.parse.urlsplit(url).hostname == "api.github.com":
            if ma != 302 or DAU not in hd:
                return None, f"chuyen_huong_la:{ma}"
            if not str(hd.get("location", "")).startswith("https://"):  # d119
                return None, "chuyen_huong_khong_https"
            url = hd["location"]
            continue
        if ma != 200 or byte is VUOT:
            return None, f"tai_khong_tron:{ma}"
        if "content-length" in hd and str(hd["content-length"]).strip() != str(len(byte)):  # d120
            return None, "tai_ngan_hon_content_length"
        return byte, None
    return None, "chuyen_huong_qua_3"

# ---- Phan mot luot audit: T1-T7 (muc 4) ----
HINH_D1 = (
    ("event", lambda r: r.get("event") == "schedule"),  # d05
    ("path", lambda r: r.get("path") == WORKFLOW_CANH),  # h:path
    ("head_branch", lambda r: r.get("head_branch") == "master"),  # h:head_branch
    ("head_sha", lambda r: isinstance(r.get("head_sha"), str) and RE_SHA.fullmatch(r["head_sha"])),  # h:head_sha
    ("status", lambda r: isinstance(r.get("status"), str)),  # h:status
    ("created_at", lambda r: gio(r.get("created_at")) is not None),  # h:created_at
    ("workflow_id", lambda r: _so_nguyen(r.get("workflow_id")) and r["workflow_id"] > 0),  # h:workflow_id
    ("repository.full_name", lambda r: _lay(r, "repository.full_name") == KHO),  # h:repository.full_name
    ("repository.id", lambda r: _so_nguyen(_lay(r, "repository.id")) and _lay(r, "repository.id") > 0),  # h:repository.id
)

def _hinh_rest(run, jobs, arts):
    """Truong bat buoc va kieu cua T1 (run, job, artifact)."""
    chuoi = lambda o, *ks: all(isinstance(o.get(k), str) for k in ks)
    return (all(_so_nguyen(run.get(k)) for k in ("id", "run_attempt", "workflow_id")) and "conclusion" in run
            and chuoi(run, "status", "event", "head_sha", "head_branch", "path", "created_at")
            and isinstance(_lay(run, "repository.full_name"), str) and _so_nguyen(_lay(run, "repository.id"))
            and all(chuoi(j, "name", "status") and _so_nguyen(j.get("run_attempt")) and "conclusion" in j for j in jobs)
            and all(chuoi(a, "name") and type(a.get("expired")) is bool and "digest" in a for a in arts))

def _lech_lien_ket(d1, d2):
    return next((f"lien_ket_lech:{t}" for t in LIEN_KET if _lay(d1, t) != _lay(d2, t)), None)

def _t1(c, d1):
    """T1 `doc_rest`. Tra ((trang thai, ma), run ban doc DAU | None, rest | None)."""
    goc = f"{API}/actions/runs/{d1['id']}"
    run, loi = _j(c, goc, _la_dict)
    if run is None:
        return (KHONG_DO_DUOC, loi), None, None
    jobs, loi = _liet_ke(c, goc + "/jobs?filter=all&per_page=100", "jobs")
    arts, loi2 = _liet_ke(c, goc + "/artifacts?per_page=100", "artifacts") if jobs is not None else (None, loi)
    if arts is None:
        return (KHONG_DO_DUOC, loi2), run, None
    if not _hinh_rest(run, jobs, arts):  # d125
        return (KHONG_DO_DUOC, "rest_sai_hinh"), run, None
    lech = _lech_lien_ket(d1, run)
    if lech:
        return (KHONG_DO_DUOC, lech), run, None
    return (DAT, DAT), run, {"run": run, "jobs": sorted(jobs, key=lambda j: j["id"]), "artifacts": arts}  # d10

def _t2(c, rest):
    """T2 `bien_nhan`. Tra ((trang thai, ma), bien nhan | None)."""
    run = rest["run"]
    ten = f"bien-nhan-audit-{run['id']}-{run['run_attempt']}"
    khop = [a for a in rest["artifacts"] if a["name"] == ten]  # d06
    if not khop:
        return (KHONG_DAT, "bien_nhan_vang"), None
    if len(khop) > 1:  # d126
        return (KHONG_DAT, "bien_nhan_trung"), None
    if khop[0]["expired"] is not False:  # d117
        return (KHONG_DAT, "bien_nhan_het_han"), None
    byte, loi = _tai(c, khop[0]["id"])
    if byte is None:
        return (KHONG_DO_DUOC, loi), None
    if "sha256:" + _sha(byte) != khop[0]["digest"]:  # d41
        return (KHONG_DAT, "bien_nhan_digest_lech"), None
    tep, _ = doc_zip(c, byte)
    if tep is VUOT:
        return (KHONG_DO_DUOC, "goi_vuot_tran"), None
    if tep is HONG:
        return (KHONG_DAT, "bien_nhan_goi_hong"), None  # d42
    if len(tep) != 1:  # d127
        return (KHONG_DAT, "bien_nhan_so_tep"), None
    if tep[0][0] != "bien_nhan_audit.json":  # d128
        return (KHONG_DAT, "bien_nhan_ten_tep"), None
    b, _ = doc_json(tep[0][1])
    if b is HONG:
        return (KHONG_DAT, "bien_nhan_khong_phai_json"), None  # d43
    return (DAT, DAT), b

def _job_ky_vong(wf):
    """Luat dat ten X2 cua B1a. Tra (danh sach ten, None) hoac (None, ma)."""
    la = (None, "hinh_workflow_la")
    jobs = wf.get("jobs") if isinstance(wf, dict) else None
    if not isinstance(jobs, dict):  # x2:jobs
        return la
    ten = []
    for k, j in jobs.items():
        if not isinstance(j, dict):
            return la
        if "name" in j:  # d38
            return la
        if "strategy" not in j:
            ten.append(k)
            continue
        mt = j["strategy"].get("matrix") if isinstance(j["strategy"], dict) else None
        if not isinstance(mt, dict):  # x2:khong_matrix
            return la
        if len(mt) != 1:  # x2:nhieu_khoa
            return la
        (mk, gt), = mt.items()
        if mk in ("include", "exclude"):  # x2:include
            return la
        if not isinstance(gt, list) or not gt:  # x2:rong
            return la
        if not all(type(v) in (int, str) for v in gt):  # x2:kieu
            return la
        ten += [f"{k} ({v})" for v in gt]
    if len(set(ten)) != len(ten):  # d130
        return None, "job_ky_vong_trung"
    if len({khoa_tu_ten(t) for t in ten}) != len(ten):  # d37
        return None, "job_ky_vong_trung_khoa"
    return ten, None

def _b64(s):
    try:
        return base64.b64decode(s)
    except Exception:
        return None

def _t3(c, sha):
    """T3 `dau_vao_doc_lap`: D6 + D7 tai `sha`, MOT lan moi sha. Tra ((trang thai, ma), job_ky_vong | None, tree_h | None)."""
    if sha in c.nho:
        return c.nho[sha]
    def doc():
        x, loi = _j(c, f"{API}/contents/{WORKFLOW_CANH}?ref={sha}", lambda v: isinstance(v, dict) and v.get("encoding") == "base64"
                    and isinstance(v.get("content"), str) and _b64(v["content"]) is not None)
        if x is None:
            return (KHONG_DO_DUOC, loi), None, None
        cm, loi = _j(c, f"{API}/git/commits/{sha}", lambda v: isinstance(_lay(v, "tree.sha"), str))
        if cm is None:
            return (KHONG_DO_DUOC, loi), None, None
        mo_dun, loi = nap_thu_vien("yaml")
        if mo_dun is HONG:
            return (KHONG_DO_DUOC, loi), None, None
        wf, _ = doc_yaml(mo_dun, _b64(x["content"]))
        if wf is HONG:
            return (KHONG_DAT, "hinh_workflow_la"), None, None  # d39
        ten, loi = _job_ky_vong(wf)
        return ((KHONG_DAT, loi), None, None) if ten is None else ((DAT, DAT), ten, cm["tree"]["sha"])
    c.nho[sha] = doc()
    return c.nho[sha]

def _t5(c, rest, b, V):
    """T5 `tai_goi`. Tra ((trang thai, ma), tai_ve)."""
    if not (V["bien_nhan"].is_valid(b) and b["ok"] is True):  # d134
        return (DAT, DAT), {}
    co = {a["id"] for a in rest["artifacts"] if a["expired"] is False}  # d132
    neu = [r["dau_job"]["id"] for r in b["job"]] + [m["artifact"]["id"] for m in b["manh"]]
    tt, tai_ve = (DAT, DAT), {}
    for aid in sorted(set(neu)):  # d12 d133
        if aid not in co:
            continue
        byte, loi = _tai(c, aid)
        if byte is None:
            tt = (KHONG_DO_DUOC, loi) if tt[0] == DAT else tt
            continue
        tep, _ = doc_zip(c, byte)
        if tep is VUOT:
            tt = (KHONG_DO_DUOC, "goi_vuot_tran") if tt[0] == DAT else tt
            continue
        if tep is HONG:
            tep = []  # d45
        ds = []
        for ten, nd in sorted(tep):
            x, _ = doc_json(nd)
            if x is HONG:
                x = None  # d46
            ds.append({"ten": ten, "sha256": _sha(nd), "noi_dung": x})
        tai_ve[str(aid)] = {"sha256_goi": _sha(byte), "tep": ds}
    return tt, tai_ve

def _t7(c, d1, run):
    """T7 `anh_chup`: D2 CUOI, LIEN KET roi U6."""
    cuoi, loi = _j(c, f"{API}/actions/runs/{d1['id']}", _la_dict)
    if cuoi is None:
        return (KHONG_DO_DUOC, loi)
    lech = _lech_lien_ket(d1, cuoi)  # d03
    if lech:
        return (KHONG_DO_DUOC, lech)
    if any(run.get(k) != cuoi.get(k) for k in ("run_attempt", "status", "conclusion", "updated_at")):  # d04
        return (KHONG_DO_DUOC, "luot_doi_giua_chung")
    return (DAT, DAT)

def _phan_luot(c, d1, V, khung):
    """Phan quyet MOT luot: bac 1 (NEO: T1/T7) thang moi ket qua khac; bac 2 la phep VA tren T2-T6 da danh gia."""
    pc = dict.fromkeys(("T1", "T2", "T3", "T5", "T6", "T7"), ("khong_danh_gia", None))
    pc["T4"] = (DAT, DAT)
    ra = {"id": d1["id"], "head_sha": d1["head_sha"], "khung": viet(khung), "run_attempt": None, "canh_bao": [], "moc_tuoi": None}
    pc["T1"], run, rest = _t1(c, d1)
    chua_xong = False
    if rest is not None:
        ra["run_attempt"] = run["run_attempt"]
        chua_xong = run["status"] != "completed"  # d135
        if not chua_xong:
            pc["T2"], b = _t2(c, rest)
            pc["T3"], ten, tree_h = _t3(c, run["head_sha"])  # d36
            if pc["T2"][0] == DAT:
                pc["T5"], tai_ve = _t5(c, rest, b, V)
                if pc["T3"][0] == DAT and pc["T5"][0] == DAT:
                    ngoai = {"h": run["head_sha"], "tai_ve": tai_ve}
                    ngoai["job_ky_vong"] = ten  # d34
                    ngoai["tree_h"] = tree_h  # d35
                    r, loi = goi_tieu_dung(V, b, rest, ngoai)
                    if r is HONG:
                        pc["T6"] = (KHONG_DO_DUOC, loi)
                    else:
                        vp, ra["canh_bao"], ra["moc_tuoi"] = r[0], list(r[1]), r[2]
                        if "C10" in ra["canh_bao"]:
                            ra["dinh_danh_definition"] = b.get("dinh_danh_definition")
                        pc["T6"] = (KHONG_DAT, "luat_C:" + "+".join(sorted(vp, key=lambda s: int(s[1:])))) if vp else (DAT, DAT)  # d58
    if run is not None:
        pc["T7"] = _t7(c, d1, run)
    neo = next((pc[t][1] for t in ("T1", "T7") if pc[t][0] == KHONG_DO_DUOC), None)  # d84
    if neo is not None:  # d83
        ra["phan_quyet"], ra["ma"] = KHONG_DO_DUOC, neo
    elif chua_xong:
        ra["phan_quyet"], ra["ma"] = "dang_chay", "dang_chay"
    else:
        da = [pc[t] for t in ("T2", "T3", "T5", "T6") if pc[t][0] != "khong_danh_gia"]
        pq = next((x for x in (KHONG_DAT, KHONG_DO_DUOC) if any(p[0] == x for p in da)), DAT)
        ra["phan_quyet"], ra["ma"] = pq, next(p[1] for p in da if p[0] == pq)
    ra["phep"] = {t: list(v) for t, v in sorted(pc.items())}
    return ra

# ---- Gop khung, nghia vu khung cu, trang thai tong (muc 5) ----
UU_TIEN = ((DAT, DAT), (KHONG_DAT, "do"), (KHONG_DO_DUOC, KHONG_DO_DUOC), ("dang_chay", "dang_chay"))

def _gop(phan_quyet):
    return next((ten for x, ten in UU_TIEN if x in phan_quyet), "vang")

def _da_dong(gop): return gop in ("dong_tay", DAT)  # d26

def t4_hop_dong(goc):
    """T4 `hop_dong`: schema trong CHECKOUT cua chinh watchdog phai dung bam GHIM-B1A va nap duoc. Tra (trang thai, ma, V)."""
    duong = os.path.join(goc, DUONG_SCHEMA)
    if not os.path.isfile(duong):  # d131
        return KHONG_DO_DUOC, "hop_dong_vang", None
    with open(duong, "rb") as f:
        byte = f.read()
    if _sha(byte) != BAM_SCHEMA:  # d40
        return KHONG_DO_DUOC, "hop_dong_lech_ghim", None
    schema, _ = doc_json(byte)
    V, loi = nap_thu_vien("jsonschema", schema)
    return (KHONG_DO_DUOC, loi, None) if V is HONG else (DAT, DAT, V)

def _danh_gia(c, T, goc, dong_den0, khung_dau, dong_tay):
    """Pha danh gia (muc 3-5). Tra dict ket qua; moi duong S1 giu `dong_den` = `dong_den0` va `sha_audit` = None."""
    F = khung_cron(T)
    P = F - BAY_NGAY
    kq = {"F": viet(F), "P": viet(P), "khung": {}, "dong_den": viet(dong_den0), "nghia_vu": [], "sha_audit": None}
    def s1(ma):
        kq.update(trang_thai=KHONG_DO_DUOC, ma=ma)
        return kq
    tt4, ma4, V = t4_hop_dong(goc)
    if tt4 != DAT:
        return s1(ma4)
    d1, loi = _liet_ke(c, f"{API}/actions/workflows/ci-dot-bien-du.yml/runs?event=schedule&per_page=100", "workflow_runs")
    if d1 is None:
        return s1(loi)
    for r in d1:
        sai = next((ten for ten, dung in HINH_D1 if not dung(r)), None)
        if sai:
            return s1("khoa_chon_khong_doc_duoc" if sai == "created_at" else "danh_sach_la")
    kc = {r["id"]: khung_cron(gio(r["created_at"])) for r in d1}
    so = max(0, (P - max(dong_den0, khung_dau - BAY_NGAY)) // BAY_NGAY)
    R = [P - BAY_NGAY * i for i in range(so)][::-1]  # d23
    tay = {k: ly_do for k, ly_do in ((gio(x), y) for x, y in dong_tay.items()) if k is not None and k <= P}  # d87
    if len([k for k in R if k not in tay]) > SO_KHUNG_SOAT_TOI_DA:  # d25
        return s1("qua_nhieu_khung_can_soat")
    xet = ({F, P} | set(R)) - set(tay)  # d85
    E = sorted((r for r in d1 if kc[r["id"]] in xet), key=lambda r: r["id"])  # d11
    luot = {}
    for r in E:
        luot[r["id"]] = _phan_luot(c, r, V, kc[r["id"]])  # d13
    gop = {}
    for k in sorted({F, P} | set(R)):
        ds = [luot[r["id"]] for r in E if kc[r["id"]] == k]
        gop[k] = "dong_tay" if k in tay else _gop([x["phan_quyet"] for x in ds])  # d86
        kq["khung"][viet(k)] = {"gop": gop[k], "ly_do": tay[k]} if k in tay else {"gop": gop[k], "luot": ds}
    if c.dong_ho() >= c.han:  # d99
        c.can_dg = True
    if c.can_tn:
        return s1("het_tai_nguyen_danh_gia")
    if c.can_dg:  # d14
        return s1("het_ngan_sach_danh_gia")  # d140
    O = [k for k in R if not _da_dong(gop[k])]
    dong_den = dong_den0
    for k in R:
        if not _da_dong(gop[k]):
            break  # d24
        dong_den = k
    kq["dong_den"], kq["nghia_vu"] = viet(dong_den), [{"khung": viet(k), "gop": gop[k]} for k in O]
    gF, gP = gop[F], gop[P]
    if gF == "do":  # S2
        s, ma = "stale_or_missing", "khung_do"
    elif any(gop[k] != KHONG_DO_DUOC for k in O):  # S3
        s, ma = "stale_or_missing", "slot_cu_chua_dong"
    elif O:  # S4
        s, ma = KHONG_DO_DUOC, "slot_cu_khong_do_duoc"
    elif gF == DAT:  # S5
        s, ma = "fresh", "khung_xanh"
    elif gF == KHONG_DO_DUOC:  # S6
        s, ma = KHONG_DO_DUOC, "khung_khong_do_duoc"
    elif gF == "vang" and T > F + TRE_LICH_TOI_DA:  # S7
        s, ma = "stale_or_missing", "khung_vang"
    elif T - P > TUOI_TOI_DA:  # S8
        s, ma = "stale_or_missing", "qua_tuoi_8_ngay"
    elif gP == DAT:  # S9a
        s, ma = "due_in_progress", "khung_dang_cho"
    elif gP == KHONG_DO_DUOC:
        s, ma = KHONG_DO_DUOC, "khung_truoc_khong_do_duoc"
    else:
        s, ma = "stale_or_missing", "khung_truoc_khong_xanh"
    if s in G_TT:
        dat = [x for x in kq["khung"][viet(F if s == "fresh" else P)].get("luot", []) if x["phan_quyet"] == DAT]
        kq["sha_audit"] = min(dat, key=lambda x: x["id"])["head_sha"] if dat else None  # d16
    kq.update(trang_thai=s, ma=ma)
    return kq

# ---- Nhip tim (muc 7) ----
def SAI(khoa, i): return f"nhip_tim_sai_mien:{khoa}:m{i}"

def _hop_ma(tt, ma):
    return ma in MA_SOM[tt] if tt in MA_SOM else all(ma not in v for v in MA_SOM.values())

def _kiem_su_kien(o, khoa, i, khung_nt):
    """m18..m24 (`da_bao`, i = 18) va m27..m33 (`cho_bao`, i = 27) cho chinh object."""
    if not (isinstance(o["id"], str) and RE_ID_SK.fullmatch(o["id"])):
        return SAI(khoa, i)
    if o["loai"] not in LOAI:
        return SAI(khoa, i + 1)
    if o["trang_thai"] not in TT4:
        return SAI(khoa, i + 2)
    if not (isinstance(o["ma_ly_do"], str) and RE_MA.fullmatch(o["ma_ly_do"])):
        return SAI(khoa, i + 3)
    if not _hop_ma(o["trang_thai"], o["ma_ly_do"]):
        return SAI(khoa, i + 4)
    if not khung_hop_le(o["khung"]):
        return SAI(khoa, i + 5)
    if not o["khung"] <= khung_nt:
        return SAI(khoa, i + 6)
    return None

def kiem_nhip_tim(x, T_doc, khung_dau):
    """Dinh nghia chuan tac cua mien `b2_nhip_tim.v1`: dieu kien DAU TIEN sai cho ma; None khi dat. `khung_dau` la datetime."""
    if set(x) != KHOA_NT:  # d116
        return "nhip_tim_tap_khoa"
    if x["schema"] != "b2_nhip_tim.v1":
        return SAI("schema", 1)
    luc = gio(x["luc"])
    if luc is None:
        return SAI("luc", 2)
    if luc > T_doc:  # d62
        return "nhip_tim_tuong_lai"
    if type(x["run_id"]) is not int:
        return SAI("run_id", 4)
    if not 1 <= x["run_id"] <= 10**20 - 1:
        return SAI("run_id", 5)
    if type(x["run_attempt"]) is not int:
        return SAI("run_attempt", 6)
    if not 1 <= x["run_attempt"] <= 10**10 - 1:
        return SAI("run_attempt", 7)
    if x["trang_thai"] not in TT4:
        return SAI("trang_thai", 8)
    if not (isinstance(x["ma_ly_do"], str) and RE_MA.fullmatch(x["ma_ly_do"])):
        return SAI("ma_ly_do", 9)
    if not _hop_ma(x["trang_thai"], x["ma_ly_do"]):
        return SAI("ma_ly_do", 10)
    if x["khung"] != viet(khung_cron(luc)):
        return SAI("khung", 11)
    for k, i in (("sha_audit", 12), ("sha_master", 14)):
        if not (x[k] is None or isinstance(x[k], str) and RE_SHA.fullmatch(x[k])):
            return SAI(k, i)
        if k == "sha_audit" and (x[k] is not None) != (x["trang_thai"] in G_TT):
            return SAI("sha_audit", 13)
    if not khung_hop_le(x["dong_den"]):
        return SAI("dong_den", 15)
    goc = khung_dau - BAY_NGAY
    if not goc <= gio(x["dong_den"]) <= max(goc, khung_cron(luc) - BAY_NGAY):  # d94
        return SAI("dong_den", 16)
    for ten, so, them in (("da_bao", 17, {"comment_id"}), ("cho_bao", 26, set())):
        o = x[ten]
        if o is None:
            continue
        if not (isinstance(o, dict) and set(o) == KHOA_SK | them):
            return SAI(ten, so)
        ma = _kiem_su_kien(o, ten, so + 1, x["khung"])
        if ma:
            return ma
        if them and not (type(o["comment_id"]) is int and 1 <= o["comment_id"] <= 10**20 - 1):
            return SAI("da_bao", 25)
    return None

def doc_nhip_tim(than, T, khung_dau):
    """Luat doc nhip tim. Tra (`moi` | `cu` | `vang` | `khong_doc_duoc`, ma day du, nhip tim | None)."""
    dong = [d for d in (than or "").split("\n") if d.startswith(TT_NT)]
    if not dong:
        return "vang", "vang", None
    if len(dong) > 1:  # d64
        return "khong_doc_duoc", "nhip_tim_trung", None
    x, loi = doc_json(dong[0][len(TT_NT):].encode("utf-8"))
    if x is HONG:
        return "khong_doc_duoc", "nhip_tim_json_hong:" + loi, None
    if not isinstance(x, dict):  # d142
        return "khong_doc_duoc", "nhip_tim_khong_phai_object", None
    ma = goi_kiem_nhip_tim(x, T, khung_dau)
    if ma:
        return "khong_doc_duoc", ma, None
    tt = "cu" if T - gio(x["luc"]) > datetime.timedelta(hours=24) else "moi"  # d63
    return tt, tt, x

# ---- Giao thuc giao tin W0-W8 (muc 7) va bao cao (muc 6) ----
def cau_master(sha_master, sha_audit, so_sanh):
    """Dung MOT trong ba cau; khong bao gio noi master da audit khi hai SHA khac nhau."""
    if sha_master and sha_audit and sha_master == sha_audit:  # d59
        return f"master hiện tại = SHA đã audit {sha_audit}"
    if sha_master and sha_audit:
        truoc = so_sanh["ahead_by"] if isinstance(so_sanh, dict) else KHONG_DO_DUOC
        return f"master hiện tại KHÁC SHA đã audit: master {sha_master}, audit {sha_audit}, master đi trước {truoc} commit"
    return "chưa có SHA đã audit hợp lệ hoặc không đọc được master"

def _thong_bao_can(S, C, da_bao, tt_nt):
    """Luat thong bao: loai su kien CAN cap (so voi su kien DA GIAO gan nhat), hoac None."""
    bo = (da_bao["trang_thai"], da_bao["khung"], da_bao["ma_ly_do"]) if isinstance(da_bao, dict) else None
    if S in W_TT and bo != C:  # (a)
        return "canh_bao"
    if S in G_TT and bo is not None and bo[0] in W_TT:  # (b)
        return "hoi_phuc"
    if tt_nt in ("cu", "vang", "khong_doc_duoc"):  # (c)
        return "nhip_tim_gian_doan"
    return None

def _su_kien(rid, ratt, loai, C):
    return {"id": f"{rid}-{ratt}", "loai": loai, "trang_thai": C[0], "khung": C[1], "ma_ly_do": C[2]}

def _khop(cm, sk):
    """Comment KHOP su kien: cua github-actions[bot], DUNG MOT dong `B2_SU_KIEN: `, JSON sau tien to bang su kien."""
    dong = [d for d in str(cm.get("body") or "").split("\n") if d.startswith(TT_SK)]
    if _lay(cm, "user.login") != BOT:  # d68
        return False
    if len(dong) != 1:  # d143
        return False
    x, _ = doc_json(dong[0][len(TT_SK):].encode("utf-8"))
    return x is not HONG and x == sk

def _buoc_ghi(c, url, hinh, pt="GET", than=None):
    """Mot buoc cua pha ghi; buoc HOAN TAT o hay sau han thi ket qua khong duoc dung."""
    x, hd = _j(c, url, hinh, pt, than)
    if c.dong_ho() >= c.han:  # d106
        return None, "het_gio"
    return x, hd

def _hinh_issue(v): return isinstance(v, dict) and isinstance(v.get("body"), (str, type(None))) and isinstance(v.get("state"), str)

def _ghi_than(c, issue, nt, T, khung_dau, ghi, a, b):
    """Tu kiem -> PATCH (MOT lan gui) -> doc lai. True <=> than doc lai bang tung ky tu va `state` la `open`."""
    ma = goi_kiem_nhip_tim(nt, T, khung_dau)  # d96
    if ma:
        ghi[a] = ma
        return False
    than = DONG_1 + "\n" + TT_NT + _dumps(nt)
    x, loi = _buoc_ghi(c, f"{API}/issues/{issue}", _la_dict, "PATCH", {"body": than, "state": "open"})
    ghi[a] = "da_gui" if x is not None else "chua_xac_nhan:" + loi
    x, loi = _buoc_ghi(c, f"{API}/issues/{issue}", _hinh_issue)
    if x is None:
        ghi[b] = "doc_lai_loi:" + loi
    elif x["body"] != than:  # d75
        ghi[b] = "than_lech"
    elif x["state"] != "open":  # d76
        ghi[b] = "state_lech"
    else:
        ghi[b] = DAT
    return ghi[b] == DAT

def _so_context(v, tran):
    return int(v) if isinstance(v, str) and re.fullmatch(r"[1-9][0-9]*", v) and int(v) <= tran else None  # d148

def chay(moi_truong, transport, goc=".", *, T=None, dong_ho=time.monotonic, ngu=time.sleep, issue=ISSUE_THEO_DOI, khung_dau=KHUNG_DAU,
         khung_dong_tay=KHUNG_DONG_TAY, tran=None):
    """MOT luot watchdog. Tra (ma thoat, bao cao). Dong ho, ham ngu, transport, so Issue, KHUNG_DAU, KHUNG_DONG_TAY va tran chi tiem
    bang tham so ham (I3); `moi_truong` chi duoc doc GH_TOKEN, B2_RUN_ID, B2_RUN_ATTEMPT."""
    token = moi_truong.get("GH_TOKEN") or ""  # d81
    if type(issue) is not int or issue < 1:  # d147
        return 2, {"loi": "issue_theo_doi_sai"}
    if not token:  # d80
        return 2, {"loi": "gh_token_rong"}
    rid = _so_context(moi_truong.get("B2_RUN_ID"), 10**20 - 1)  # d97
    ratt = _so_context(moi_truong.get("B2_RUN_ATTEMPT"), 10**10 - 1)  # d98
    if rid is None or ratt is None:
        return 2, {"loi": "context_b2_run_sai"}
    T = T or datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None, microsecond=0)
    kd, c = gio(khung_dau), _NguCanh(transport, dong_ho, ngu, token, tran)
    ghi, loi_ghi = {}, False
    # W0 — doc truoc (D10), TRUOC pha danh gia
    t0 = c.dong_ho()
    c.han = t0 + NGAN_SACH_GHI
    iss, loi = _buoc_ghi(c, f"{API}/issues/{issue}", _hinh_issue)
    w0_dung = c.dong_ho() - t0
    nt = ("khong_doc_duoc", "d10_loi:" + loi, None) if iss is None else doc_nhip_tim(iss["body"], T, kd)
    x0 = nt[2]
    dong_den0 = gio(x0["dong_den"]) if x0 else kd - BAY_NGAY  # d27
    da_bao0, cho_bao0 = (x0["da_bao"], x0["cho_bao"]) if x0 else (KHONG_BIET, None)
    # Pha danh gia, trong luoi an toan; pha ghi KHONG nam trong luoi
    c.pha_dg, c.han = True, c.dong_ho() + NGAN_SACH_DANH_GIA
    try:
        kq = _danh_gia(c, T, goc, dong_den0, kd, khung_dong_tay)
    except Exception as e:  # luoi an toan
        F = khung_cron(T)
        kq = {"F": viet(F), "P": viet(F - BAY_NGAY), "khung": {}, "dong_den": viet(dong_den0), "nghia_vu": [], "sha_audit": None,
              "trang_thai": KHONG_DO_DUOC, "ma": _ma_nem("danh_gia", e)}
    c.pha_dg = False
    c.han = c.dong_ho() + NGAN_SACH_GHI - w0_dung  # d15
    # D8, D9 — thong tin cho bao cao, khong doi S
    x, _ = _buoc_ghi(c, f"{API}/git/ref/heads/master", lambda v: isinstance(_lay(v, "object.sha"), str) and RE_SHA.fullmatch(v["object"]["sha"]))
    sha_master = x["object"]["sha"] if x is not None else None  # d141
    so_sanh = "khong_ap_dung"
    if sha_master and kq["sha_audit"]:
        x, _ = _buoc_ghi(c, f"{API}/compare/{kq['sha_audit']}...{sha_master}", lambda v: isinstance(v, dict) and isinstance(v.get("status"), str)
                         and _so_nguyen(v.get("ahead_by")) and _so_nguyen(v.get("behind_by")))
        so_sanh = {k: x[k] for k in ("status", "ahead_by", "behind_by")} if x is not None else KHONG_DO_DUOC  # d60
    cau = cau_master(sha_master, kq["sha_audit"], so_sanh)
    C = (kq["trang_thai"], kq["F"], dau_ma(kq["ma"]))
    def nhip(da_bao, cho_bao):
        return {"schema": "b2_nhip_tim.v1", "luc": viet(T), "run_id": rid, "run_attempt": ratt, "trang_thai": kq["trang_thai"],
                "ma_ly_do": dau_ma(kq["ma"]), "khung": kq["F"], "sha_audit": kq["sha_audit"], "sha_master": sha_master,  # d95
                "dong_den": kq["dong_den"], "da_bao": da_bao, "cho_bao": cho_bao}
    da_bao1, cho_bao1, hoan = da_bao0, cho_bao0, None
    if iss is None:  # d79
        ghi["W0"], loi_ghi = nt[1], True
    else:
        ghi["W0"], khoa_gui, da_giao = nt[0], False, False
        if cho_bao0 is not None:  # W1 d67
            cua_so = viet(gio(cho_bao0["khung"]) - LE_DOI_SOAT)  # d92
            ds, loi = _liet_ke(c, f"{API}/issues/{issue}/comments?since={cua_so}&per_page=100", None)  # d91
            if ds is not None and c.dong_ho() >= c.han:
                ds, loi = None, "het_gio"
            if ds is None:
                khoa_gui, loi_ghi, ghi["W1"] = True, True, "doi_soat_khong_tron" if loi == "khong_tron" else "doi_soat_loi:" + loi
            else:
                khop = [cm["id"] for cm in ds if _khop(cm, cho_bao0)]
                if khop:
                    da_bao1, da_giao = dict(cho_bao0, comment_id=min(khop)), True  # d144
                ghi["W1"] = "da_giao" if khop else "chua_giao"
        if not khoa_gui:   # Cap su kien
            can = _thong_bao_can(kq["trang_thai"], C, da_bao1, nt[0])  # d65
            if cho_bao0 is not None and not da_giao:
                cho_bao1 = cho_bao0  # d71 d88 d89
                khac = (can, C) != (cho_bao0["loai"], (cho_bao0["trang_thai"], cho_bao0["khung"], cho_bao0["ma_ly_do"]))
                hoan = {"loai": can, "bo": list(C)} if can and khac else None   # su kien KHAC bi hoan; cung loai cung bo thi chinh la su kien dang cho
            else:
                cho_bao1 = _su_kien(rid, ratt, can, C) if can else None  # d90
        ok = _ghi_than(c, issue, nhip(None if da_bao1 is KHONG_BIET else da_bao1, cho_bao1), T, kd, ghi, "W2", "W3")  # d66
        if not ok:
            loi_ghi = True
        if ok and cho_bao1 is not None and not khoa_gui:  # W4 d70
            than_cm = "\n".join((f"B2 watchdog: {cho_bao1['loai']}: {cho_bao1['trang_thai']} ({cho_bao1['ma_ly_do']})", TT_SK + _dumps(cho_bao1), cau,
                                 f"nhip_tim_truoc: {nt[0]}", f"https://github.com/{KHO}/actions/runs/{rid}/attempts/{ratt}"))
            cm, hd = _buoc_ghi(c, f"{API}/issues/{issue}/comments", lambda v: isinstance(v, dict) and _so_nguyen(v.get("id")) and v["id"] > 0, "POST", {"body": than_cm})
            if cm is None or hd[":ma"] != 201:
                ghi["W5"], loi_ghi = "chua_xac_nhan", True
            else:
                ghi["W5"] = "da_gui"
                doc, _ = _buoc_ghi(c, f"{API}/issues/comments/{cm['id']}", _la_dict)
                if doc is None or doc.get("body") != than_cm:  # d77
                    ghi["W6"], loi_ghi = "doc_lai_lech", True
                elif _lay(doc, "user.login") != BOT:  # d145
                    ghi["W6"], loi_ghi = "doc_lai_login_lech", True
                else:
                    ghi["W6"] = DAT
                    da_bao1, cho_bao1 = dict(cho_bao1, comment_id=cm["id"]), None
                    if not _ghi_than(c, issue, nhip(da_bao1, None), T, kd, ghi, "W7", "W8"):
                        loi_ghi = True
    bc = {"schema": "b2_bao_cao.v1", "T": viet(T), "F": kq["F"], "P": kq["P"], "trang_thai": kq["trang_thai"], "ma_ly_do": dau_ma(kq["ma"]),
          "ma_chi_tiet": kq["ma"], "khung": kq["khung"], "dong_den_truoc": viet(dong_den0), "dong_den": kq["dong_den"], "nghia_vu": kq["nghia_vu"],
          "sha_audit": kq["sha_audit"], "sha_master": sha_master or KHONG_DO_DUOC, "so_sanh": so_sanh, "cau_master": cau,
          "nhip_tim_truoc": {"trang_thai": nt[0], "ma": nt[1]}, "ghi": ghi, "thong_bao_hoan": hoan, "kenh_giao_tin": KENH_GIAO_TIN_XAC_NHAN or "chua_do",
          "su_kien": {"da_giao": None if da_bao1 is KHONG_BIET else da_bao1, "dang_cho": cho_bao1}}
    return (3 if loi_ghi else 0 if kq["trang_thai"] in G_TT else 1), bc  # d78

class _KhongChuyenHuong(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None

def transport_that(pt, url, hd, than, timeout):
    """Transport HTTP that: MOT lan gui, khong tu theo chuyen huong (lop R tu xu ly), tra (ma, header, luong doc duoc)."""
    req = urllib.request.Request(url, data=None if than is None else json.dumps(than).encode("utf-8"), headers=hd, method=pt)
    try:
        r = urllib.request.build_opener(_KhongChuyenHuong).open(req, timeout=timeout)
    except urllib.error.HTTPError as e:
        r = e
    return r.status, dict(r.headers.items()), r

def main():
    ma, bc = chay(os.environ, transport_that, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(json.dumps(bc, ensure_ascii=True, sort_keys=True))
    tom_tat = os.environ.get("GITHUB_STEP_SUMMARY")
    if tom_tat and "trang_thai" in bc:
        with open(tom_tat, "a", encoding="utf-8") as f:
            f.write(f"## canh-tuoi-audit: {bc['trang_thai']} ({bc['ma_chi_tiet']})\n\n{bc['cau_master']}\n\nma thoat {ma}; ghi: {_dumps(bc['ghi'])}\n")
    return ma

if __name__ == "__main__":
    sys.exit(main())
