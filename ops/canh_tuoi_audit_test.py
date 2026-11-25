#!/usr/bin/env python3
"""Bo test cua ops/canh_tuoi_audit.py va .github/workflows/canh-tuoi-audit.yml (wp1494, B2). Offline: khong goi GitHub that.

Dung: `python ops/canh_tuoi_audit_test.py` (tat ca) · `--chi-tiet` (in them cap goc/dot bien tung dong) · `--mot-ca TEN GOC MO_DUN`
(tien trinh con cua vong dot bien). Chi `bang()` nem `TinHieuChotCa` mang TEN CA dang chay: con in `DO:<ca>:` va thoat 3; moi
loi khac thoat 4. Dot bien chay tren BAN SAO tam, ten tep rieng, `-B`; chi GIET khi ca dich nem dung lop ay voi dung ten ca.
Ra (bon dong cuoi): `CA: N/N dat` · `DOT BIEN: M/M bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (k dot bien)` · `TONG: DAT`."""
import base64
import contextlib
import copy
import datetime
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import warnings
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

sys.dont_write_bytecode = True
for _luong in (sys.stdout, sys.stderr):
    _luong.reconfigure(encoding="utf-8", errors="replace")
TEP_TEST = Path(__file__).resolve()
_CON = sys.argv[1:] if sys.argv[1:2] == ["--mot-ca"] and len(sys.argv) == 5 else None
ROOT = Path(_CON[2]) if _CON else TEP_TEST.parent.parent
TEP_MO_DUN = Path(_CON[3]) if _CON else ROOT / "ops/canh_tuoi_audit.py"
W_TEP = ROOT / ".github/workflows/canh-tuoi-audit.yml"
BAM_FIXTURE = "ce8595739a1ab2f4a86c9c196255e5f91fb19a9f6d3865df6caa2d66f9970e6d"   # GHIM-B1A
BAM_KHOI_MA = "d9c78e708e18a211b7d8c7309638ffd1c73200578cf3128f9f0fc4275430f24e"   # GHIM-B1A

def _nap(duong):
    spec = importlib.util.spec_from_file_location("canh_tuoi_audit_duoi_thu", duong)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

class TinHieuChotCa(AssertionError):
    """Tin hieu RIENG cua mot chot ca, mang TEN CA dang chay; bo phan hang chi tin lop nay voi dung ten ca dich."""
    def __init__(self, ca, thong_diep):
        super().__init__(thong_diep)
        self.ca = ca

CA, _DANG_CHAY = {}, []

def bang(dieu_kien, thong_diep):
    if not dieu_kien:
        raise TinHieuChotCa(_DANG_CHAY[-1], thong_diep)

def ca(f, ten=None):
    ten = ten or f.__name__
    def boc():
        _DANG_CHAY.append(ten)
        try:
            f()
        finally:
            _DANG_CHAY.pop()
    CA[ten] = boc
    return boc

def sha256(byte): return hashlib.sha256(byte).hexdigest()

# ---- Nghiem thu 10: bo kiem hinh workflow (muc 8) — ngu phap danh sach CHO PHEP toi tung buoc ----
BT = "$" + "{{"
J = "jobs.canh-tuoi"
MONG_WF = {"name": "canh-tuoi-audit", "on": {"schedule": [{"cron": "41 */6 * * *"}], "workflow_dispatch": None},
           "permissions": {"actions": "read", "contents": "read", "issues": "write"},
           "concurrency": {"group": "canh-tuoi-audit", "cancel-in-progress": False}}
MONG_BUOC = ({"uses": "actions/checkout@v4", "with": {"persist-credentials": False}},
             {"uses": "actions/setup-python@v5", "with": {"python-version": "3.12"}},
             {"run": "python -m pip install --quiet PyYAML==6.0.3 jsonschema==4.26.0"},
             {"run": "python ops/canh_tuoi_audit.py", "env": {"GH_TOKEN": BT + " github.token }}", "B2_RUN_ID": BT + " github.run_id }}",
                                                               "B2_RUN_ATTEMPT": BT + " github.run_attempt }}"}})

def _lech(co, mong, duong):
    """Duong dan khoa DAU TIEN lech giua `co` va `mong` (bang nhau tuyet doi: kieu + khoa + gia tri), hoac None."""
    if type(co) is not type(mong):
        return duong
    if isinstance(mong, dict):
        for k in sorted(set(co) | set(mong), key=str):
            r = f"{duong}.{k}" if k not in co or k not in mong else _lech(co[k], mong[k], f"{duong}.{k}")
            if r:
                return r
        return None
    if isinstance(mong, list):
        return duong if len(co) != len(mong) else next((r for i, (a, b) in enumerate(zip(co, mong)) for r in [_lech(a, b, f"{duong}[{i}]")] if r), None)
    return None if co == mong else duong

def _khoa(co, mong, duong):
    """Tap khoa DONG: khoa thua, thieu hay lap (danh sach `co`) => duong dan khoa ay."""
    sai = sorted(set(co) ^ set(mong), key=str) or [k for k in co if co.count(k) > 1]
    return f"{duong}.{sai[0]}".lstrip(".") if sai else None

def _gia_tri(buoc, mong, duong):
    """Gia tri cua cac khoa CO MAT trong buoc (tap khoa cua buoc la menh de rieng); `with`/`env` so tron, tap khoa dong."""
    return next((r for k in mong if k in buoc for r in [_lech(buoc[k], mong[k], f"{duong}.{k}")] if r), None)

def kiem_hinh(tho):
    """Tra danh sach duong dan khoa sai cua van ban workflow `tho` (rong <=> dat). Moi menh de mot loi goi `doi`; menh de nem => tu choi."""
    van, loi = yaml.safe_load(tho), []
    def doi(ma, ham):
        try:
            r = ham()
        except Exception as e:
            r = f"{ma}:{type(e).__name__}"
        if r:
            loi.append(r)
    ks = ["on" if k is True else k for k in van]             # PyYAML 1.1 doc khoa tran `on` thanh True; nhan DUNG MOT trong hai
    wf = dict(zip(ks, van.values()))
    job, buoc = (lambda: wf["jobs"]["canh-tuoi"]), (lambda i: wf["jobs"]["canh-tuoi"]["steps"][i])
    doi("m01", lambda: _khoa(ks, [*MONG_WF, "jobs"], "") or _lech(wf["name"], MONG_WF["name"], "name"))
    doi("m02", lambda: _lech(wf["on"], MONG_WF["on"], "on"))
    doi("m03", lambda: _lech(wf["permissions"], MONG_WF["permissions"], "permissions"))
    doi("m04", lambda: _lech(wf["concurrency"], MONG_WF["concurrency"], "concurrency"))
    doi("m05", lambda: _khoa(list(wf["jobs"]), ["canh-tuoi"], "jobs"))
    doi("m06", lambda: _khoa(list(job()), ["runs-on", "timeout-minutes", "steps"], J))
    doi("m07", lambda: _lech(job()["runs-on"], "ubuntu-latest", J + ".runs-on"))
    doi("m08", lambda: _lech(job()["timeout-minutes"], 20, J + ".timeout-minutes"))
    doi("m09", lambda: None if type(job()["steps"]) is list and len(job()["steps"]) == 4 else J + ".steps")
    doi("m10", lambda: _khoa(list(buoc(0)), list(MONG_BUOC[0]), J + ".steps[0]"))
    doi("m11", lambda: _khoa(list(buoc(1)), list(MONG_BUOC[1]), J + ".steps[1]"))
    doi("m12", lambda: _khoa(list(buoc(2)), list(MONG_BUOC[2]), J + ".steps[2]"))
    doi("m13", lambda: _khoa(list(buoc(3)), list(MONG_BUOC[3]), J + ".steps[3]"))
    doi("m14", lambda: _gia_tri(buoc(0), MONG_BUOC[0], J + ".steps[0]"))
    doi("m15", lambda: _gia_tri(buoc(1), MONG_BUOC[1], J + ".steps[1]"))
    doi("m16", lambda: _gia_tri(buoc(2), MONG_BUOC[2], J + ".steps[2]"))
    doi("m17", lambda: _gia_tri(buoc(3), MONG_BUOC[3], J + ".steps[3]"))
    doi("m18", lambda: None if tho.count(BT) == 3 else BT)   # chu thich YAML khong co trong cau truc da phan tich
    return loi

W = W_TEP.read_text(encoding="utf-8")
B1, B2, B3, B4 = ("      - uses: actions/checkout@v4\n", "      - uses: actions/setup-python@v5\n",
                  "      - run: python -m pip install --quiet PyYAML==6.0.3 jsonschema==4.26.0\n", "      - run: python ops/canh_tuoi_audit.py\n")
ENV4, RO = W.partition(B4)[2], "    runs-on: ubuntu-latest\n"
CUOI = "          B2_RUN_ATTEMPT: " + BT + " github.run_attempt }}\n"
KHOA_CAM = (("if", "if", "false"), ("coe", "continue-on-error", "true"), ("name", "name", "x"), ("id", "id", "x"), ("shell", "shell", "bash"),
            ("wd", "working-directory", "."), ("timeout", "timeout-minutes", "5"))
AM_10 = [   # (ten ca, chuoi goc — DUNG MOT lan trong tep that, chuoi thay, duong dan khoa sai phai duoc bao)
    ("n10_khoa_workflow", "permissions:\n", "env:\n  A: b\npermissions:\n", "env"),
    ("n10_khoa_workflow_defaults", "permissions:\n", "defaults:\n  run:\n    shell: bash\npermissions:\n", "defaults"),
    ("n10_hai_khoa_on", "permissions:\n", '"on": {}\npermissions:\n', "on"),
    ("n10_ten", "name: canh-tuoi-audit\n", "name: khac\n", "name"),
    ("n10_on", "  workflow_dispatch:\n", "  workflow_dispatch:\n  push:\n", "on.push"),
    ("n10_on_inputs", "  workflow_dispatch:\n", "  workflow_dispatch:\n    inputs:\n      x:\n        type: string\n", "on.workflow_dispatch"),
    ("n10_on_cron", '"41 */6 * * *"', '"41 */5 * * *"', "on.schedule[0].cron"),
    ("n10_on_hai_schedule", "  workflow_dispatch:\n", '    - cron: "1 1 * * *"\n  workflow_dispatch:\n', "on.schedule"),
    ("n10_quyen", "  issues: write\n", "  issues: write\n  pull-requests: read\n", "permissions.pull-requests"),
    ("n10_quyen_bot", "  actions: read\n", "", "permissions.actions"),
    ("n10_quyen_doi", "  issues: write\n", "  issues: read\n", "permissions.issues"),
    ("n10_concurrency", "cancel-in-progress: false", "cancel-in-progress: true", "concurrency.cancel-in-progress"),
    ("n10_concurrency_bo", "concurrency:\n  group: canh-tuoi-audit\n  cancel-in-progress: false\n", "", "concurrency"),
    ("n10_tap_job", CUOI, CUOI + "  them:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo\n", "jobs.them"),
    ("n10_khoa_job", RO, "    if: false\n" + RO, J + ".if"),
    ("n10_khoa_job_coe", RO, "    continue-on-error: true\n" + RO, J + ".continue-on-error"),
    ("n10_khoa_job_strategy", RO, "    strategy:\n      matrix:\n        a: [1]\n" + RO, J + ".strategy"),
    ("n10_khoa_job_quyen", RO, "    permissions:\n      issues: write\n" + RO, J + ".permissions"),
    ("n10_runs_on", RO, "    runs-on: ubuntu-22.04\n", J + ".runs-on"),
    ("n10_timeout", "timeout-minutes: 20", "timeout-minutes: 30", J + ".timeout-minutes"),
    ("n10_so_buoc", CUOI, CUOI + "      - run: echo\n", J + ".steps"),
    ("n10_thu_tu_buoc", B3 + B4 + ENV4, B4 + ENV4 + B3, J + ".steps[2].env"),
    ("n10_buoc1_gia_tri", "persist-credentials: false", "persist-credentials: true", J + ".steps[0].with.persist-credentials"),
    ("n10_buoc1_vang", "        with:\n          persist-credentials: false\n", "        with: {}\n", J + ".steps[0].with.persist-credentials"),
    ("n10_buoc2_gia_tri", 'python-version: "3.12"', "python-version: 3.12", J + ".steps[1].with.python-version"),
    ("n10_buoc3_gia_tri", "jsonschema==4.26.0", "jsonschema==4.25.0", J + ".steps[2].run"),
    ("n10_buoc4_gia_tri", CUOI, CUOI + "          X: y\n", J + ".steps[3].env.X"),
    ("n10_buoc4_thieu_bien", CUOI, "", J + ".steps[3].env.B2_RUN_ATTEMPT"),
    ("n10_buoc4_doi_bien", "github.run_id", "github.run_number", J + ".steps[3].env.B2_RUN_ID"),
    ("n10_buoc4_chu_thich", B4, "      - run: |\n          # " + BT + " github.sha }}\n          python ops/canh_tuoi_audit.py\n", J + ".steps[3].run"),
    ("n10_dem_bieu_thuc", "name: canh-tuoi-audit\n", "# " + BT + " github.sha }}\nname: canh-tuoi-audit\n", BT),
] + [(f"n10_buoc{k + 1}_{hau}", b, b + f"        {khoa}: {gt}\n", f"{J}.steps[{k}].{khoa}") for k, b in enumerate((B1, B2, B3, B4)) for hau, khoa, gt in KHOA_CAM]

def _ca_am_10(cu, moi, duong):
    def chay():
        bang(W.count(cu) == 1, f"ca phai doi DUNG MOT diem cua tep that (thay {W.count(cu)} cho)")
        loi = kiem_hinh(W.replace(cu, moi))
        bang(duong in loi, f"mong tu choi tai {duong!r}, bo kiem bao {loi}")
    return chay

for _ten, _cu, _moi, _duong in AM_10:
    ca(_ca_am_10(_cu, _moi, _duong), _ten)

@ca
def n10_tep_that():
    bang(kiem_hinh(W) == [], f"tep that tai H phai dat bo kiem hinh: {kiem_hinh(W)}")
    bang(kiem_hinh(W.replace("\non:\n", '\n"on":\n')) == [] and W.count("\non:\n") == 1, "khoa `on` viet co nhay cung phai duoc nhan")

@ca
def n10_i7_dau_bo_qua_ci():   # mau dung tu cac manh chu, khong viet nguyen van (I7)
    m = ("skip", "ci", "no", "actions", "-checks")
    cap = ((m[0], m[1]), (m[1], m[0]), (m[2], m[1]), (m[0], m[3]), (m[3], m[0]))
    mau = re.compile("|".join([rf"\[{a}[ _-]{b}\]" for a, b in cap] + [m[0] + m[4]]), re.I)
    bang(all(mau.search(f"x [{a} {b}] y".upper()) for a, b in cap), "mau phai bat duoc moi bien the")
    for tep in (W_TEP, TEP_MO_DUN, TEP_TEST):
        bang(not mau.search(tep.read_text(encoding="utf-8")), f"{tep.name} chua dau bo-qua-CI")

# ---- Ha tang ca cho ops/canh_tuoi_audit.py: GitHub gia GIU TRANG THAI, dong ho gia, bo dung luot tu fixture GHIM-B1A ----
M = _nap(TEP_MO_DUN)
warnings.filterwarnings("ignore", "Duplicate name")   # ca hai tep cung ten trong mot ZIP la dau vao CO CHU DICH
TD, BOT = datetime.timedelta, "github-actions[bot]"
F_BYTE = (ROOT / "ops/specs/wp1460-r1/hop_dong/fixture.json").read_bytes()
NEN = json.loads(F_BYTE)["nen"]
F0 = datetime.datetime(2026, 12, 12, 19, 17)   # khung hien hanh cua moi ca (thu Bay 19:17 UTC)
P0, T0 = F0 - TD(days=7), F0 + TD(hours=9)
JOB_KV = "jobs:\n  dot-bien-du: {}\n  dot-bien-manh:\n    strategy:\n      fail-fast: false\n      matrix:\n        manh: [0, 1, 2, 3, 4, 5, 6, 7]\n  dot-bien-gop: {}\n  bien-nhan-audit: {}\n"
LUU = "https://luu-tru.example/goi/"
_SO_LUOT = []   # (bao cao, nhat ky, khung_dau) cua moi luot watchdog trong ca dang chay — cho hau kiem sau ca

class LoiTiem(Exception):
    """Lop ngoai le do test dinh nghia (khong thuoc thu vien chuan) de tiem vao nguyen ham."""

def viet(t): return t.strftime("%Y-%m-%dT%H:%M:%SZ")

def zip_cua(tep, nen=zipfile.ZIP_DEFLATED):
    """ZIP tat dinh tu danh sach (ten, byte); ten ket thuc `/` la muc thu muc."""
    bo = io.BytesIO()
    with zipfile.ZipFile(bo, "w", nen) as z:
        for ten, byte in tep:
            z.writestr(zipfile.ZipInfo(ten, (2026, 1, 1, 0, 0, 0)), byte, nen)
    return bo.getvalue()

def dung_luot(rid, khung, att=1, sha="a" * 40, tre=3, sua=None):
    """Mot luot `schedule` HOP LE cua khung `khung`, dung tu nen `xanh` cua fixture: REST + bien nhan + goi bang chung that (digest khop)."""
    tao = viet(khung + TD(hours=tre))
    s = json.dumps([NEN["xanh"], NEN["rest"], NEN["ngoai"]["tai_ve"]]).replace("44000000001", str(rid)).replace("1400000", f"{rid}00")
    bn, rest, tai = json.loads(s.replace("900000000", f"{rid}9000").replace(f"-{rid}-1-", f"-{rid}-{att}-").replace("a" * 40, sha))
    bn["su_kien"] = {"ten": "schedule", "sha": sha, "ref": "refs/heads/master", "cron": "17 19 * * 6", "khung_danh_nghia_utc": viet(M.khung_cron(khung + TD(hours=tre))), "run_created_at": tao}
    bn["luot"]["run_attempt"] = att
    goi = {}
    for d in bn["job"] + bn["manh"]:
        a = d.get("dau_job") or d["artifact"]
        if "dau_job" in d:
            d["run_attempt"] = att
        else:
            d["attempt_ben_san_xuat"] = att
        t = tai[str(a["id"])]["tep"][0]
        if "run_attempt" in t["noi_dung"]:
            t["noi_dung"]["run_attempt"] = att
        nd = json.dumps(t["noi_dung"]).encode()
        goi[a["id"]] = zip_cua([(t["ten"], nd)])
        a["sha256_noi_dung"], a["digest"] = sha256(nd), "sha256:" + sha256(goi[a["id"]])
    for a in rest["artifacts"]:
        a["digest"] = "sha256:" + sha256(goi[a["id"]])
    for j in rest["jobs"]:
        j["run_attempt"] = att
    if sua:
        sua(bn)
    idb = int(f"{rid}000999")
    goi[idb] = zip_cua([("bien_nhan_audit.json", json.dumps(bn).encode())])
    rest["artifacts"].append({"id": idb, "name": f"bien-nhan-audit-{rid}-{att}", "expired": False, "digest": "sha256:" + sha256(goi[idb])})
    d2 = dict(rest["run"], event="schedule", created_at=tao, run_attempt=att, head_branch="master", workflow_id=7, updated_at=tao, status="completed", conclusion="success")
    return {"d1": copy.deepcopy(d2), "d2": d2, "d2_cuoi": None, "jobs": rest["jobs"], "arts": rest["artifacts"], "goi": goi, "bn": bn, "idb": idb}

class LuongGia(io.BytesIO):
    """Luong than cua phan hoi gia: dem lan `read()` KHONG kem kich thuoc (doc het mot lan thay vi theo khuc)."""
    vo_han = 0

    def read(self, n=-1):
        LuongGia.vo_han += n is None or n < 0
        return super().read(n)

class Gia:
    """GitHub gia: Issue co than/state/comment that trong bo nho; POST luu comment TRUOC khi quyet dinh phan hoi; ghi nhat ky tung lan
    gui VAT LY (phuong thuc, URL, co Authorization khong, than, timeout, thoi diem don dieu luc bat dau); ton trong `timeout`."""
    def __init__(self):
        self.t, self.nk, self.ngu_nk, self.luot, self.thu_tu, self.goi = 0.0, [], [], {}, [], {}
        self.wf, self.tree, self.master, self.ahead = dict.fromkeys(("a" * 40, "e" * 40), JOB_KV.encode()), dict.fromkeys(("a" * 40, "e" * 40), "b" * 40), "a" * 40, 0
        self.issue, self.id_cm, self.lech_gio, self.T, self.rid = {1520: {"body": "", "state": "open", "cm": []}}, 5000, 0, T0, 7001
        self.sua, self.tre, self.nhay_json, self.trang, self.so_d2 = [], [], [], 100, {}

    def dong_ho(self): return self.t

    def ngu(self, giay):
        self.ngu_nk.append(giay)
        self.t += giay

    def them(self, luot):
        self.luot[luot["d1"]["id"]] = luot
        self.thu_tu.append(luot["d1"]["id"])
        self.goi.update(luot["goi"])
        return luot

    def loi(self, mau, *phan_hoi, pt="GET", tu=1):
        """Hang doi phan hoi thay the cho cac lan gui khop `mau`: moi phan tu la (ma, than[, header]) hoac mot ngoai le de nem; het hang doi thi di duong thuong; `tu` = lan khop dau tien bi thay (dem tu 1)."""
        hang, bo_qua = list(phan_hoi), [tu - 1]
        def ham(*_):
            bo_qua[0] -= 1
            return hang.pop(0) if hang and bo_qua[0] < 0 else None
        self.sua.append((mau, pt, ham))

    def __call__(self, pt, url, hd, than, timeout):
        self.nk.append({"pt": pt, "url": url, "auth": "Authorization" in hd, "than": than, "timeout": timeout, "t": self.t})
        can = next((g for mau, g in self.tre if re.search(mau, url)), 0)
        if timeout is not None and can >= timeout:
            self.t += max(timeout, 0)
            raise TimeoutError("het gio (gia)")
        self.t += can
        kq = next((r for mau, p, ham in self.sua if p == pt and re.search(mau, url) for r in [ham(self, pt, url, than)] if r is not None), None)
        if isinstance(kq, BaseException):
            raise kq
        ma, tra, *hd_them = kq if kq is not None else self.xu_ly(pt, url, than)
        hd_ra = dict({"X-GitHub-Request-Id": "gia"} if "luu-tru.example" not in url else {}, **(hd_them[0] if hd_them else {}))
        return ma, {k: v for k, v in hd_ra.items() if v is not None}, (tra if hasattr(tra, "read") else LuongGia(tra if isinstance(tra, bytes) else json.dumps(tra).encode()))

    def trang_cua(self, url, ds, khoa):
        so = int((re.search(r"[?&]page=(\d+)", url) or [0, 1])[1])
        co = self.trang if khoa in ("workflow_runs", None) else 100   # `trang` chi ap cho D1 va D14
        phan, con = ds[(so - 1) * co:so * co], len(ds) > so * co
        tiep = re.sub(r"[?&]page=\d+", "", url) + f"&page={so + 1}"
        return 200, ({khoa: phan, "total_count": len(ds)} if khoa else phan), ({"Link": f'<{tiep}>; rel="next"'} if con else {})

    def xu_ly(self, pt, url, than):
        m = lambda mau: re.search(mau, url)
        if x := m(r"luu-tru\.example/goi/(\d+)"):
            byte = self.goi[int(x[1])]
            return 200, byte, {"Content-Length": str(len(byte))}
        if m(r"/actions/workflows/ci-dot-bien-du\.yml/runs\?event=schedule"):
            return self.trang_cua(url, [self.luot[i]["d1"] for i in self.thu_tu], "workflow_runs")
        if x := m(r"/actions/runs/(\d+)(/jobs|/artifacts)?"):
            lu = self.luot.get(int(x[1]))
            if lu is None:
                return 404, {"message": "Not Found"}
            if x[2]:
                return self.trang_cua(url, lu["jobs" if x[2] == "/jobs" else "arts"], x[2][1:])
            self.so_d2[int(x[1])] = self.so_d2.get(int(x[1]), 0) + 1
            return 200, lu["d2"] if self.so_d2[int(x[1])] == 1 or lu["d2_cuoi"] is None else lu["d2_cuoi"]
        if x := m(r"/actions/artifacts/(\d+)/zip"):
            return 302, {}, {"Location": LUU + x[1]}
        if x := m(r"/contents/\.github/workflows/ci-dot-bien-du\.yml\?ref=(\w+)"):
            return (200, {"encoding": "base64", "content": base64.encodebytes(self.wf[x[1]]).decode()}) if x[1] in self.wf else (404, {})
        if x := m(r"/git/commits/(\w+)"):
            return (200, {"tree": {"sha": self.tree[x[1]]}}) if x[1] in self.tree else (404, {})
        if m(r"/git/ref/heads/master"):
            return 200, {"object": {"sha": self.master}}
        if m(r"/compare/"):
            return 200, {"status": "ahead", "ahead_by": self.ahead, "behind_by": 0}
        if x := m(r"/issues/comments/(\d+)"):
            cm = [c for i in self.issue.values() for c in i["cm"] if c["id"] == int(x[1])]
            return (200, cm[0]) if cm else (404, {})
        x = m(r"/issues/(\d+)(/comments)?")
        iss = self.issue.get(int(x[1])) if x else None
        if iss is None:
            return 404, {"message": "Not Found"}
        gio_may_chu = viet(self.T + TD(hours=self.lech_gio))
        if x[2] and pt == "POST":
            self.id_cm += 1
            iss["cm"].append({"id": self.id_cm, "body": than["body"], "user": {"login": BOT}, "created_at": gio_may_chu, "updated_at": gio_may_chu})
            return 201, iss["cm"][-1]
        if x[2]:
            tu = re.search(r"since=([^&]+)", url)
            return self.trang_cua(url, [c for c in iss["cm"] if not tu or c["updated_at"] >= tu[1]], None)
        if pt == "PATCH":
            iss.update(body=than["body"], state=than["state"])
        return 200, {"body": iss["body"], "state": iss["state"]}

def luot_wd(g, T=T0, **kw):
    """MOT luot watchdog tren GitHub gia `g`. Tra (ma thoat, bao cao, nhat ky cua RIENG luot nay)."""
    g.T, dau = T, len(g.nk)
    env = kw.pop("env", None) or {"GH_TOKEN": "tok-gia", "B2_RUN_ID": str(g.rid), "B2_RUN_ATTEMPT": "1"}
    g.rid += 1
    kd = kw.pop("khung_dau", viet(P0))
    def boc(goc):   # `nhay_json`: nguyen ham doc_json bi boc de dong ho gia nhay toi `moc` SAU khi phan tich xong phan hoi khop `dk` (moi muc mot lan)
        def f(byte):
            x = goc(byte)
            for muc in [m for m in g.nhay_json if m[0](x)]:
                g.nhay_json.remove(muc)
                g.t = max(g.t, muc[1])
            return x
        return f
    with thay_ten("_tho_json", boc):
        ma, bc = M.chay(env, g, kw.pop("goc", str(ROOT)), T=T, dong_ho=g.dong_ho, ngu=g.ngu, issue=kw.pop("issue", 1520), khung_dau=kd,
                        khung_dong_tay=kw.pop("dong_tay", {}), tran=kw.pop("tran", None))
    _SO_LUOT.append((bc, g.nk[dau:], kd))
    return ma, bc, g.nk[dau:]

def hau_kiem():
    """Sau MOI ca: khu hoi nguoi ghi -> nguoi doc, bat bien moc (nghiem thu 5d), dem vat ly. Vi pham nem AssertionError THUONG (khong phai tin hieu chot)."""
    for bc, nk, kd in _SO_LUOT:
        patch, post = [x for x in nk if x["pt"] == "PATCH"], [x for x in nk if x["pt"] == "POST"]
        assert len(patch) <= 2 and len(post) <= 1, f"dem vat ly: {len(patch)} PATCH, {len(post)} POST"
        for x in patch:
            nt = json.loads(x["than"]["body"].split("\n")[1][len("B2_NHIP_TIM: "):])
            doc = M.doc_nhip_tim(x["than"]["body"], M.gio(nt["luc"]), M.gio(kd))
            assert doc[0] == "moi" and x["than"]["body"].isascii() and x["than"]["body"].count("\n") == 1, f"khu hoi: {doc[:2]}"
        for k in bc.get("khung", {}).values():
            for lu in k.get("luot", []):
                assert lu["phan_quyet"] != "dat" or lu["moc_tuoi"] == lu["khung"], f"bat bien moc: luot {lu['id']} moc {lu['moc_tuoi']} khung {lu['khung']}"

def gh(f="dat", p="dat", **cu):
    """GitHub gia voi luot cua F (id 20), cua P (id 10) va cac khung cu `k<n>` = P - n tuan (id 10 - n). Gia tri: dat · do · kdd · chay · vang."""
    g, LuongGia.vo_han = Gia(), 0
    for khung, rid, kieu in [(P0 - TD(days=7 * int(k[1:])), 10 - int(k[1:]), v) for k, v in sorted(cu.items(), reverse=True)] + [(P0, 10, p), (F0, 20, f)]:
        them(g, rid, khung, kieu)
    return g

def them(g, rid, khung, kieu, **kw):
    if kieu == "vang":
        return None
    lu = g.them(dung_luot(rid, khung, **dict({"sha": ("a" if rid == 20 else "e") * 40}, **kw)))   # luot F mang sha rieng
    if kieu == "do":       # khong co bien nhan => T2 bien_nhan_vang
        lu["arts"].pop()
    elif kieu == "kdd":    # D3 tra 403 co dau => T1 khong_do_duoc
        g.loi(rf"/actions/runs/{rid}/jobs", *[(403, {})] * 9)
    elif kieu == "chay":
        lu["d1"].update(status="in_progress", conclusion=None)
        lu["d2"].update(status="in_progress", conclusion=None)
        lu["arts"].pop()
    return lu

def nt_cu(T=T0, gio_truoc=6, **sua):
    """Nhip tim HOP LE cua mot luot truoc (S `fresh`, `da_bao` mang dung bo `fresh` hien hanh, `cho_bao` null) roi ap `sua`."""
    luc = T - TD(hours=gio_truoc)
    kh = viet(M.khung_cron(luc))
    sk = {"id": "6000-1", "loai": "hoi_phuc", "trang_thai": "fresh", "khung": kh, "ma_ly_do": "khung_xanh", "comment_id": 4000}
    nt = {"schema": "b2_nhip_tim.v1", "luc": viet(luc), "run_id": 6000, "run_attempt": 1, "trang_thai": "fresh", "ma_ly_do": "khung_xanh", "khung": kh,
          "sha_audit": "a" * 40, "sha_master": "a" * 40, "dong_den": viet(P0), "da_bao": sk, "cho_bao": None}
    return dict(nt, **sua)

def dat_than(g, nt, issue=1520):
    g.issue.setdefault(issue, {"body": "", "state": "open", "cm": []})["body"] = M.DONG_1 + "\n" + M.TT_NT + json.dumps(nt, sort_keys=True, separators=(",", ":"))
    return g

def lu_bc(bc, rid):
    return next((lu for k in bc.get("khung", {}).values() for lu in k.get("luot", []) if lu["id"] == rid), {"phep": {}})

def phep(bc, rid, t): return tuple(lu_bc(bc, rid)["phep"].get(t, (None, None)))

def dem(nk, pt, mau=""): return len([x for x in nk if x["pt"] == pt and re.search(mau, x["url"])])

def S(bc): return bc.get("trang_thai"), bc.get("ma_ly_do")

def cm_khop(g, sk, issue=1520):
    return [c for c in g.issue[issue]["cm"] if M.TT_SK + json.dumps(sk, sort_keys=True, separators=(",", ":")) in c["body"].split("\n")]

def nt_tren(g, issue=1520):
    return json.loads(g.issue[issue]["body"].split("\n")[1][len(M.TT_NT):])

@ca
def n0_nen_fresh():   # doi chung chung: nen hop le cho `fresh`, luot dau tren Issue rong
    g = gh()
    ma, bc, nk = luot_wd(g)
    bang(S(bc) == ("fresh", "khung_xanh") and bc["sha_audit"] == "a" * 40, f"nen phai fresh: {S(bc)} {bc.get('ma_chi_tiet')} {lu_bc(bc, 20)}")
    bang(lu_bc(bc, 20)["phan_quyet"] == "dat" and all(v[0] == "dat" for v in lu_bc(bc, 20)["phep"].values()), f"T1-T7 phai dat: {lu_bc(bc, 20)['phep']}")
    bang(ma == 0 and dem(nk, "PATCH") == 2 and dem(nk, "POST") == 1 and bc["nhip_tim_truoc"]["trang_thai"] == "vang", f"luot dau: ma {ma}, ghi {bc['ghi']}")
    bang(nt_tren(g)["da_bao"]["loai"] == "nhip_tim_gian_doan" and nt_tren(g)["dong_den"] == viet(P0), f"nhip tim: {nt_tren(g)}")

# ---- Nghiem thu 3: bang nhau tren fixture CHUNG cua GHIM-B1A ----
def _ap(doc, sua):   # `huong_dan` cua fixture: JSON Pointer RFC 6901, '-' la them cuoi danh sach, `xoa` thi go
    for s in sua or []:
        *cha, cuoi = [x.replace("~1", "/").replace("~0", "~") for x in s["duong"].split("/")[1:]]
        o = doc
        for k in cha:
            o = o[int(k)] if isinstance(o, list) else o[k]
        if isinstance(o, list) and cuoi == "-":
            o.append(s["gia_tri"])
        elif s.get("xoa"):
            del o[int(cuoi) if isinstance(o, list) else cuoi]
        else:
            o[int(cuoi) if isinstance(o, list) else cuoi] = s["gia_tri"]
    return doc

@ca
def n3_fixture_chung():   # hai tep hop_dong/ vang => FileNotFoundError => ca DO (khong bo qua)
    thu = ROOT / "ops/specs/wp1460-r1"
    f_byte = F_BYTE
    ghim = [sha256((ROOT / M.DUONG_SCHEMA).read_bytes()) == M.BAM_SCHEMA, sha256(f_byte) == BAM_FIXTURE]
    if (thu / "SPEC.md").is_file():   # khoi ma "Lenh kiem" chi do duoc khi tep dac ta B1a co trong cay
        d = (thu / "SPEC.md").read_text(encoding="utf-8").split("\n")
        a = d.index("```python", next(i for i, x in enumerate(d) if x.startswith("## Lệnh kiểm")))
        ghim.append(sha256(("\n".join(d[a + 1:d.index("```", a)]) + "\n").encode("utf-8")) == BAM_KHOI_MA)
    bang(all(ghim), f"bam GHIM-B1A lech: {ghim}")
    tt, ma, V = M.t4_hop_dong(str(ROOT))
    bang(tt == "dat", f"T4 phai dat tren checkout nay: {ma}")
    F, hinh, ngu = json.loads(f_byte), 0, 0
    for c in F["ca"]:
        doc = _ap(copy.deepcopy(F["nen"][c["nen"]]), c.get("sua"))
        hop_le = V["dau_job" if c["nen"] == "dau_job" else "bien_nhan"].is_valid(doc)
        bang(hop_le == c["hinh_hop_le"], f"HINH {c['ten']}: {hop_le}")
        hinh += 1
        if c["nen"] == "dau_job":
            continue
        vp, canh, moc = M.tieu_dung(V, doc, _ap(copy.deepcopy(F["nen"]["rest"]), c.get("sua_rest")), _ap(copy.deepcopy(F["nen"]["ngoai"]), c.get("sua_ngoai")))
        bang(set(vp) == set(c["vi_pham"] if hop_le else ["C1"]) and canh == c.get("canh_bao", []) and ("moc_tuoi" not in c or moc == c["moc_tuoi"]),
             f"NGU NGHIA {c['ten']}: vi pham {sorted(vp)} canh bao {canh} moc {moc}")
        ngu += 1
    dong = f"HOP_DONG_B1A: hinh {hinh}/120 · ngu nghia {ngu}/118 · ghim {sum(ghim)}/{len(ghim)}" + ("" if len(ghim) == 3 else " · khoi_ma khong_co_trong_cay")
    bang((hinh, ngu) == (120, 118), dong)
    print(dong)

# ---- Bang dot bien cua mo-dun: giai thanh (chuoi neo, chuoi thay) luc CHAY o tien trinh cha (con doc ban sao da dot bien) ----
DB_M = []   # (ten, cach, tham so, cac ca dich)

def db(ten, nhan, cu, moi, *ca_dich): DB_M.append((ten, "nhan", (nhan, cu, moi), ca_dich))        # doi `cu` -> `moi` tren DONG duy nhat mang `# nhan`
def khong(ten, nhan, *ca_dich): DB_M.append((ten, "khong", nhan, ca_dich))                         # `if X:  # nhan` -> `if False:  # nhan`
def xoa(ten, nhan, *ca_dich): DB_M.append((ten, "xoa", nhan, ca_dich))                             # xoa DONG duy nhat mang `# nhan`
def tho(ten, neo, thay, *ca_dich): DB_M.append((ten, "tho", (neo, thay), ca_dich))                 # chuoi neo nguyen van

def giai_db(nguon):
    """Moi muc cua DB_M -> (ten, "M", chuoi neo — DUNG MOT lan trong mo-dun goc, chuoi thay, cac ca dich). Nhan khong duy nhat => neo rong => HONG."""
    ra = []
    for ten, cach, ts, ca_dich in DB_M:
        if cach == "tho":
            ra.append((ten, "M", ts[0], ts[1], ca_dich))
            continue
        nhan = ts if cach in ("khong", "xoa") else ts[0]
        dong = [d for d in nguon.split("\n") if re.search(rf"#.*(?<![\w:.]){re.escape(nhan)}(?![\w:.])", d)]
        neo = dong[0] if len(dong) == 1 else ""
        thay = "" if cach == "xoa" else re.sub(r"^(\s*(?:el)?if ).*?(:\s+# )", r"\1False\2", neo) if cach == "khong" else neo.replace(ts[1], ts[2]) if ts[1] in neo else neo
        ra.append((ten, "M", neo, thay, ca_dich))
    return ra

# ---- Nghiem thu 1: ba trang thai tung phep con T1-T7, lop J/R/S, thu lai, LIEN KET, U6, bac NEO ----
D1U, KDD = r"/runs\?event=schedule", "khong_do_duoc"

def sua_tra(g, mau, ham, pt="GET"):
    """Sua THAN (va header) phan hoi thuong cua cac lan gui khop `mau`: `ham(than)` sua tai cho hoac tra (than moi, header them)."""
    def h(s, p, url, than):
        ma, tra, *hd = s.xu_ly(p, url, than)
        tra = copy.deepcopy(tra)
        moi = ham(tra)
        return (ma, *moi) if isinstance(moi, tuple) else (ma, tra, *hd)
    g.sua.append((mau, pt, h))

def mot(sua=None, T=T0, f="dat", p="dat", **kw):
    """Nen (mac dinh `fresh`), ap `sua(g, luot F)` roi chay MOT luot watchdog. Tra (g, ma thoat, bao cao, nhat ky)."""
    g = gh(f, p)
    if sua:
        sua(g, g.luot.get(20))
    return (g, *luot_wd(g, T, **kw))

def mong(co, muon, gi=""):
    bang(co == muon, f"{gi}: mong {muon!r}, duoc {co!r}")

def dat_goi(g, lu, tep, nen=zipfile.ZIP_DEFLATED, byte=None):
    """Thay goi bien nhan cua luot bang ZIP cua `tep` (hoac `byte` tho), digest REST khop."""
    g.goi[lu["idb"]] = byte if byte is not None else zip_cua(tep, nen)
    lu["arts"][-1]["digest"] = "sha256:" + sha256(g.goi[lu["idb"]])
    return g.goi[lu["idb"]]

def ca_j(ten, phan_hoi, ma_mong, n=1):
    def chay():
        g, ma, bc, nk = mot(lambda g, lu: g.loi(D1U, *[phan_hoi] * n))
        mong((bc["trang_thai"], bc["ma_chi_tiet"], bc["sha_audit"], ma), (KDD, ma_mong, None, 1), ten)
    ca(chay, ten)

ca_j("n1_j_403_co_dau", (403, {}), "http_github:403")
ca_j("n1_j_403_khong_dau", (403, {}, {"X-GitHub-Request-Id": None}), "khong_dau_github:403")
ca_j("n1_j_404", (404, {}), "http_github:404")
ca_j("n1_j_sai_kieu", (200, {"workflow_runs": "abc", "total_count": 3}), "json_sai_kieu")
ca_j("n1_j_json_hong", (200, b"{"), "json_hong")
ca_j("n1_j_5xx_het_luot", (503, {}), "http_github:503", 3)
db("d121", "d121", "not 200 <= ma < 300", "False", "n1_j_404")
khong("d122", "d122", "n1_j_sai_kieu")

@ca
def n1_j_khong_dau():
    g, ma, bc, nk = mot(lambda g, lu: sua_tra(g, D1U, lambda t: (t, {"X-GitHub-Request-Id": None})))
    mong((bc["trang_thai"], bc["ma_chi_tiet"]), (KDD, "khong_dau_github:200"))
khong("d48", "d48", "n1_j_khong_dau")

@ca
def n1_j_het_gio():
    g, ma, bc, nk = mot(lambda g, lu: g.tre.append((D1U, 31)))
    mong((bc["trang_thai"], bc["ma_ly_do"], dem(nk, "GET", D1U), g.ngu_nk), (KDD, "transport_nem", 3, [1, 2]))

@ca
def n1_get_thu_lai():
    g, ma, bc, nk = mot(lambda g, lu: g.loi(D1U, (500, {})))
    mong((S(bc), dem(nk, "GET", D1U)), (("fresh", "khung_xanh"), 2))
    g, ma, bc, nk = mot(lambda g, lu: g.loi(D1U, (404, {})))
    mong((bc["trang_thai"], dem(nk, "GET", D1U)), (KDD, 1), "404 khong thu lai")
db("d49", "d49", 'pt in ("GET",)', "False", "n1_get_thu_lai")

@ca
def n1_get_het_luot():
    g, ma, bc, nk = mot(lambda g, lu: g.loi(D1U, *[(500, {})] * 3))
    mong((bc["trang_thai"], dem(nk, "GET", D1U), g.ngu_nk), (KDD, 3, [1, 2]))
tho("d102", "HAN_GOI, THU_LAI_GET, CHO_THU_LAI = 30, 2, (1, 2)", "HAN_GOI, THU_LAI_GET, CHO_THU_LAI = 30, 3, (1, 2)", "n1_get_het_luot")
tho("d103", "HAN_GOI, THU_LAI_GET, CHO_THU_LAI = 30, 2, (1, 2)", "HAN_GOI, THU_LAI_GET, CHO_THU_LAI = 30, 2, (2, 1)", "n1_get_het_luot")

@ca
def n1_han_goi():
    g, ma, bc, nk = mot()
    mong({x["timeout"] for x in nk}, {30})
db("d101", "d101", "min(HAN_GOI, con)", "None", "n1_han_goi")

@ca
def n1_hai_trang():
    g, ma, bc, nk = mot(lambda g, lu: setattr(g, "trang", 1))
    mong((S(bc), dem(nk, "GET", D1U)), (("fresh", "khung_xanh"), 2))

@ca
def n1_total_count():
    g, ma, bc, nk = mot(lambda g, lu: sua_tra(g, D1U, lambda t: t.update(total_count=3)))
    mong((bc["trang_thai"], bc["ma_chi_tiet"]), (KDD, "tong_lech"))
khong("d08", "d08", "n1_total_count")

@ca
def n1_trung_id():
    g, ma, bc, nk = mot(lambda g, lu: g.thu_tu.append(20))
    mong((bc["trang_thai"], bc["ma_chi_tiet"]), (KDD, "danh_sach_trung_id"))
db("d09", "d09", 'return None, "danh_sach_trung_id"', "ds = list({p['id']: p for p in ds}.values())", "n1_trung_id")

@ca
def n1_id_bool():
    g, ma, bc, nk = mot(lambda g, lu: sua_tra(g, D1U, lambda t: t["workflow_runs"][1].update(id=True)))
    mong((bc["trang_thai"], bc["ma_chi_tiet"]), (KDD, "danh_sach_sai_kieu"))
db("d123", "d123", "type(i) is not int", "not isinstance(i, int)", "n1_id_bool")

def dat_truong(o, duong, gt):
    *cha, cuoi = duong.split(".")
    for k in cha:
        o = o[k]
    o[cuoi] = gt

for _f, _gt in (("path", "x.yml"), ("head_branch", "dev"), ("head_sha", "XYZ"), ("status", 5), ("created_at", "2026-12-12 22:17:00"), ("workflow_id", "7"),
                ("repository.full_name", "a/b"), ("repository.id", 0)):
    def _hinh(f=_f, gt=_gt):
        g, ma, bc, nk = mot(lambda g, lu: [dat_truong(lu[k], f, gt) for k in ("d1", "d2")])
        mong((bc["trang_thai"], bc["ma_chi_tiet"]), (KDD, "khoa_chon_khong_doc_duoc" if f == "created_at" else "danh_sach_la"), f)
    ca(_hinh, "n1_d1_hinh_" + _f)
    tho("d124_" + _f, f'    ("{_f}", lambda r: ', f'    ("{_f}", lambda r: True or ', "n1_d1_hinh_" + _f)

LK = (("id", 999), ("created_at", "2026-12-12T22:17:01Z"), ("event", "workflow_dispatch"), ("path", "x.yml"), ("head_branch", "dev"), ("head_sha", "c" * 40),
      ("workflow_id", 8), ("repository.full_name", "a/b"), ("repository.id", 5))

def lech_d2(lu, f, gt, cuoi=False):
    """Chi ban doc D2 DAU (hoac CUOI) khac D1 o truong `f`; ban con lai bang D1."""
    khac = copy.deepcopy(lu["d2"])
    dat_truong(khac, f, gt)
    lu["d2"], lu["d2_cuoi"] = (lu["d2"], khac) if cuoi else (khac, lu["d2"])

for _f, _gt in LK:
    def _lk(f=_f, gt=_gt):
        g, ma, bc, nk = mot(lambda g, lu: lech_d2(lu, f, gt))
        mong((phep(bc, 20, "T1"), lu_bc(bc, 20).get("ma"), phep(bc, 20, "T7")[0], S(bc)), ((KDD, "lien_ket_lech:" + f), "lien_ket_lech:" + f, "dat", (KDD, "khung_khong_do_duoc")), f)
    ca(_lk, "n1_lien_ket_" + _f)
    tho("d01_02_" + _f, f'    "{_f}",  # lk', "", "n1_lien_ket_" + _f, "n1_lien_ket_cuoi_" + _f)   # mot ham chung cho T1 va T7: chay tren ca cua CA HAI noi goi

@ca
def n1_lien_ket_cuoi():
    g, ma, bc, nk = mot(lambda g, lu: lech_d2(lu, "head_sha", "c" * 40, cuoi=True))
    mong((phep(bc, 20, "T7"), phep(bc, 20, "T1")[0]), ((KDD, "lien_ket_lech:head_sha"), "dat"))
db("d03", "d03", "_lech_lien_ket(d1, cuoi)", "None", "n1_lien_ket_cuoi")

@ca
def n1_lien_ket_doi_chung():   # D1 la anh chup cu hon: chi truong THAY DOI DUOC khac D2 => lien ket dat
    g, ma, bc, nk = mot(lambda g, lu: lu["d1"].update(status="in_progress", conclusion=None, run_attempt=7, updated_at="2026-12-12T22:20:00Z"))
    mong(S(bc), ("fresh", "khung_xanh"))

@ca
def n1_u6():
    g, ma, bc, nk = mot(lambda g, lu: lech_d2(lu, "updated_at", "2026-12-12T23:00:00Z", cuoi=True))
    mong((phep(bc, 20, "T7"), lu_bc(bc, 20)["phan_quyet"]), ((KDD, "luot_doi_giua_chung"), KDD))
khong("d04", "d04", "n1_u6")

@ca
def n1_chua_xong():
    g, ma, bc, nk = mot(f="chay", T=F0 + TD(hours=6))
    mong((lu_bc(bc, 20)["phan_quyet"], S(bc), phep(bc, 20, "T2")[0], ma), ("dang_chay", ("due_in_progress", "khung_dang_cho"), "khong_danh_gia", 0))
    g, ma, bc, nk = mot(lambda g, lu: lech_d2(lu, "status", "completed", cuoi=True), f="chay", T=F0 + TD(hours=6))
    mong((lu_bc(bc, 20)["phan_quyet"], lu_bc(bc, 20)["ma"]), (KDD, "luot_doi_giua_chung"), "vua hoan tat giua hai lan doc")
db("d135", "d135", 'run["status"] != "completed"', "False", "n1_chua_xong")

def _neo(ten, sua_them, phep_am, lech=("created_at", "2026-12-12T22:17:01Z"), ma_neo="lien_ket_lech:created_at"):
    def chay():
        g, ma, bc, nk = mot(lambda g, lu: (sua_them(g, lu), lech_d2(lu, *lech, cuoi=True)))
        mong((lu_bc(bc, 20)["phan_quyet"], lu_bc(bc, 20)["ma"], S(bc), phep(bc, 20, phep_am[0])), (KDD, ma_neo, (KDD, "khung_khong_do_duoc"), phep_am[1:]), ten)
    ca(chay, ten)

_neo("n1_neo_thang_t2", lambda g, lu: lu["arts"].pop(), ("T2", "khong_dat", "bien_nhan_vang"))
_neo("n1_neo_thang_t3", lambda g, lu: g.wf.update({"a" * 40: b"jobs:\n  x:\n    name: y\n"}), ("T3", "khong_dat", "hinh_workflow_la"))
_neo("n1_neo_thang_t6", lambda g, lu: g.tree.update({"a" * 40: "c" * 40}), ("T6", "khong_dat", "luat_C:C5"))
_neo("n1_neo_u6_t2", lambda g, lu: lu["arts"].pop(), ("T2", "khong_dat", "bien_nhan_vang"), ("updated_at", "2026-12-12T23:00:00Z"), "luot_doi_giua_chung")
khong("d83", "d83", "n1_neo_thang_t2")
db("d84", "d84", "pc[t][0] == KHONG_DO_DUOC)", 'pc[t][0] == KHONG_DO_DUOC and pc[t][1] != "luot_doi_giua_chung")', "n1_neo_u6_t2")

@ca
def n1_neo_doi_chung():
    g, ma, bc, nk = mot(f="do")
    mong((lu_bc(bc, 20)["phan_quyet"], lu_bc(bc, 20)["ma"], S(bc), ma), ("khong_dat", "bien_nhan_vang", ("stale_or_missing", "khung_do"), 1))

@ca
def n1_t1_thieu_truong():
    g, ma, bc, nk = mot(lambda g, lu: lu["jobs"][3].pop("conclusion"))
    mong(phep(bc, 20, "T1"), (KDD, "rest_sai_hinh"))
khong("d125", "d125", "n1_t1_thieu_truong")

def ca_t2(ten, sua, mong_t2, **kw):
    def chay():
        g, ma, bc, nk = mot(sua, **kw)
        mong(phep(bc, 20, "T2"), mong_t2, ten)
    ca(chay, ten)

ca_t2("n1_t2_digest", lambda g, lu: lu["arts"][-1].update(digest="sha256:" + "0" * 64), ("khong_dat", "bien_nhan_digest_lech"))
ca_t2("n1_t2_het_han", lambda g, lu: lu["arts"][-1].update(expired=True), ("khong_dat", "bien_nhan_het_han"))
ca_t2("n1_t2_trung", lambda g, lu: (lu["arts"].append(dict(lu["arts"][-1], id=777)), g.goi.update({777: g.goi[lu["idb"]]})), ("khong_dat", "bien_nhan_trung"))
ca_t2("n1_t2_ten_tep", lambda g, lu: dat_goi(g, lu, [("x.json", json.dumps(lu["bn"]).encode())]), ("khong_dat", "bien_nhan_ten_tep"))
ca_t2("n1_r_khong_https", lambda g, lu: g.loi(rf"/artifacts/{lu['idb']}/zip", (302, {}, {"Location": LUU.replace("https", "http") + str(lu["idb"])})), (KDD, "chuyen_huong_khong_https"))
ca_t2("n1_r_qua_3", lambda g, lu: g.loi(rf"/artifacts/{lu['idb']}/zip", *[(302, {}, {"Location": f"{M.API}/actions/artifacts/{lu['idb']}/zip?b={i}"}) for i in range(3)]), (KDD, "chuyen_huong_qua_3"))
ca_t2("n1_r_dung_3", lambda g, lu: g.loi(rf"/artifacts/{lu['idb']}/zip", *[(302, {}, {"Location": f"{M.API}/actions/artifacts/{lu['idb']}/zip?b={i}"}) for i in range(2)]), ("dat", "dat"))
ca_t2("n1_s_ngan", lambda g, lu: g.loi(rf"example/goi/{lu['idb']}", (200, g.goi[lu["idb"]][:-1], {"Content-Length": str(len(g.goi[lu["idb"]]))})), (KDD, "tai_ngan_hon_content_length"))
khong("d41", "d41", "n1_t2_digest")
khong("d117", "d117", "n1_t2_het_han")
khong("d126", "d126", "n1_t2_trung")
khong("d128", "d128", "n1_t2_ten_tep")
khong("d119", "d119", "n1_r_khong_https")
db("d118", "d118", "range(4)", "range(9)", "n1_r_qua_3")
khong("d120", "d120", "n1_s_ngan")

@ca
def n1_s_vuot_tran():   # goi bien nhan luu KHONG nen de no la thu lon nhat tren duong di
    for them, t2 in ((-1, (KDD, "tai_khong_tron:200")), (0, ("dat", "dat"))):
        g = gh()
        n = len(dat_goi(g, g.luot[20], [("bien_nhan_audit.json", json.dumps(g.luot[20]["bn"]).encode())], zipfile.ZIP_STORED))
        ma, bc, nk = luot_wd(g, tran={"TRAN_GOI": n + them})
        mong((phep(bc, 20, "T2"), LuongGia.vo_han), (t2, 0), f"TRAN_GOI = kich thuoc goi {them:+d}; than phai duoc doc THEO KHUC")

@ca
def n1_j_vuot_tran():
    for them, t1 in ((-1, (KDD, "than_vuot_tran")), (0, ("dat", "dat"))):
        g = gh()
        n = len(json.dumps(g.xu_ly("GET", "/actions/runs/20/artifacts", None)[1]).encode())
        ma, bc, nk = luot_wd(g, tran={"TRAN_GOI": n + them})
        mong((phep(bc, 20, "T1"), LuongGia.vo_han), (t1, 0), f"TRAN_GOI = than D4 {them:+d}; than phai duoc doc THEO KHUC")
khong("d107", "d107", "n1_j_vuot_tran", "n1_s_vuot_tran")

@ca
def n1_s_khong_auth():
    g, ma, bc, nk = mot()
    luu = [x for x in nk if "luu-tru.example" in x["url"]]
    mong((len(luu) > 0, sum(x["auth"] for x in luu), all(x["auth"] for x in nk if "api.github.com" in x["url"])), (True, 0, True))
db("d47", "d47", 'urllib.parse.urlsplit(url).hostname == "api.github.com"', "True", "n1_s_khong_auth")

def goc_tam(sua):
    """Checkout gia cho T4: thu muc tam chi co tep schema (da qua `sua`), hoac khong co gi."""
    thu = Path(tempfile.mkdtemp(prefix="cta_goc_"))
    if sua is not None:
        (thu / M.DUONG_SCHEMA).parent.mkdir(parents=True)
        (thu / M.DUONG_SCHEMA).write_bytes(sua((ROOT / M.DUONG_SCHEMA).read_bytes()))
    return str(thu)

@ca
def n1_t4_lech_ghim():
    g, ma, bc, nk = mot(goc=goc_tam(lambda b: b + b" "))
    mong((bc["trang_thai"], bc["ma_chi_tiet"], dem(nk, "GET", D1U), dem(nk, "PATCH") >= 1), (KDD, "hop_dong_lech_ghim", 0, True))
    mong(S(mot(goc=goc_tam(lambda b: b))[2]), ("fresh", "khung_xanh"), "doi chung schema dung bam")
khong("d40", "d40", "n1_t4_lech_ghim")

@ca
def n1_t4_vang():
    g, ma, bc, nk = mot(goc=goc_tam(None))
    mong((bc["trang_thai"], bc["ma_chi_tiet"]), (KDD, "hop_dong_vang"))
khong("d131", "d131", "n1_t4_vang")

@ca
def n1_t3_t5_khong_do_duoc():
    g, ma, bc, nk = mot(lambda g, lu: g.wf.pop("a" * 40))
    mong((phep(bc, 20, "T3"), S(bc)), ((KDD, "http_github:404"), (KDD, "khung_khong_do_duoc")), "D6 404")
    g, ma, bc, nk = mot(lambda g, lu: g.loi(rf"example/goi/{lu['arts'][0]['id']}$", *[(500, b"")] * 3))
    mong((phep(bc, 20, "T5"), phep(bc, 20, "T6")[0], lu_bc(bc, 20)["phan_quyet"]), ((KDD, "tai_khong_tron:500"), "khong_danh_gia", KDD), "goi bang chung tai khong tron")

# ---- Nghiem thu 2: bang ket cuc va bien ngoai le bang BYTE THAT; tran giai nen; ngoai le tiem ----
def bn_byte(lu): return json.dumps(lu["bn"]).encode()

def sk(tt, ma, loai="canh_bao", khung=F0, id="6000-1", cid=4000):
    """Mot su kien (dang `da_bao` khi co `cid`, dang `cho_bao` khi `cid` la None)."""
    o = {"id": id, "loai": loai, "trang_thai": tt, "khung": viet(khung), "ma_ly_do": ma}
    return dict(o, comment_id=cid) if cid else o

def doi_bang_chung(g, lu, i=0, tep=None, byte=None):
    """Thay goi bang chung thu `i` cua luot (artifact `dau-job` cua job thu i); bien nhan va REST khai dung digest moi."""
    a = lu["bn"]["job"][i]["dau_job"]
    g.goi[a["id"]] = byte if byte is not None else zip_cua(tep)
    a["digest"] = lu["arts"][i]["digest"] = "sha256:" + sha256(g.goi[a["id"]])
    if tep:
        a["sha256_noi_dung"] = sha256(tep[0][1])
    dat_goi(g, lu, [("bien_nhan_audit.json", bn_byte(lu))])

def zip_hong(kieu):
    goc = zip_cua([("bien_nhan_audit.json", b'{"a": "' + b"x" * 64 + b'"}')], zipfile.ZIP_STORED)
    if kieu == "crc":
        return goc.replace(b"x" * 64, b"y" + b"x" * 63)
    return bytes(goc[:8]) + b"\x63\x00" + goc[10:goc.index(b"PK\x01\x02") + 10] + b"\x63\x00" + goc[goc.index(b"PK\x01\x02") + 12:]   # kieu nen 99

BYTE_HONG = {"json_hong": b"{", "utf8_sai": b"\xff\xfe{}", "bom": b"\xef\xbb\xbf{}"}
GOI_HONG = {"zip_hong": b"day khong phai ZIP", "crc_sai": zip_hong("crc"), "kieu_nen_la": zip_hong("nen")}

def _ca_byte(ten, qua, sua, mong_phep, mong_s=("stale_or_missing", "khung_do")):
    def chay():
        g, ma, bc, nk = mot(sua)
        mong((*[phep(bc, 20, t) for t in qua], S(bc)), (*mong_phep, mong_s), ten)
    ca(chay, ten)

for _k, _b in BYTE_HONG.items():
    _ca_byte("n2_t2_" + _k, ("T2",), lambda g, lu, b=_b: dat_goi(g, lu, [("bien_nhan_audit.json", b)]), (("khong_dat", "bien_nhan_khong_phai_json"),))
    _ca_byte("n2_t5_" + _k, ("T5", "T6"), lambda g, lu, b=_b: doi_bang_chung(g, lu, tep=[("dau-job.json", b)]), (("dat", "dat"), ("khong_dat", "luat_C:C11")))
for _k, _b in GOI_HONG.items():
    _ca_byte("n2_t2_" + _k, ("T2",), lambda g, lu, b=_b: dat_goi(g, lu, None, byte=b), (("khong_dat", "bien_nhan_goi_hong"),))
    _ca_byte("n2_t5_" + _k, ("T5", "T6"), lambda g, lu, b=_b: doi_bang_chung(g, lu, byte=b), (("dat", "dat"), ("khong_dat", "luat_C:C8")))
_ca_byte("n2_zip_muc_thu_muc", ("T2",), lambda g, lu: dat_goi(g, lu, [("thu-muc/", b""), ("bien_nhan_audit.json", bn_byte(lu))]), (("dat", "dat"),), ("fresh", "khung_xanh"))
_ca_byte("n2_t2_hai_tep", ("T2",), lambda g, lu: dat_goi(g, lu, [("bien_nhan_audit.json", bn_byte(lu))] * 2), (("khong_dat", "bien_nhan_so_tep"),))
_ca_byte("n2_doi_chung_hop_le", ("T2", "T5", "T6"), lambda g, lu: None,
         (("dat", "dat"),) * 3, ("fresh", "khung_xanh"))
_ca_byte("n2_t3_yaml_hong", ("T3",), lambda g, lu: g.wf.update({"a" * 40: b"jobs: [\n"}), (("khong_dat", "hinh_workflow_la"),))
db("d42", "d42", "(KHONG_DAT,", "(KHONG_DO_DUOC,", "n2_t2_zip_hong")
db("d43", "d43", "(KHONG_DAT,", "(KHONG_DO_DUOC,", "n2_t2_json_hong")
khong("d44", "d44", "n2_zip_muc_thu_muc")
db("d45", "d45", "tep = []", 'tt = (KHONG_DO_DUOC, "goi_hong")', "n2_t5_zip_hong")
db("d46", "d46", "x = None", 'tt = (KHONG_DO_DUOC, "noi_dung_hong")', "n2_t5_json_hong")
khong("d127", "d127", "n2_t2_hai_tep")
db("d39", "d39", "(KHONG_DAT,", "(KHONG_DO_DUOC,", "n2_t3_yaml_hong")

def d5(nk, aid): return dem(nk, "GET", rf"/actions/artifacts/{aid}/zip")

@ca
def n2_t5_het_han():
    g, ma, bc, nk = mot(lambda g, lu: lu["arts"][0].update(expired=True))
    mong((d5(nk, g.luot[20]["arts"][0]["id"]), d5(nk, g.luot[20]["arts"][1]["id"]), lu_bc(bc, 20)["phan_quyet"]), (0, 1, "khong_dat"))
db("d132", "d132", 'if a["expired"] is False', "if True", "n2_t5_het_han")

@ca
def n2_t5_mot_lan():
    def sua(g, lu):
        lu["bn"]["manh"][0]["artifact"]["id"] = lu["bn"]["job"][0]["dau_job"]["id"]
        dat_goi(g, lu, [("bien_nhan_audit.json", bn_byte(lu))])
    g, ma, bc, nk = mot(sua)
    mong(d5(nk, g.luot[20]["arts"][0]["id"]), 1)
db("d133", "d133", "sorted(set(neu))", "sorted(neu)", "n2_t5_mot_lan")

@ca
def n2_t5_ok_false():   # DO DUOC: schema GHIM-B1A cam `job`/`manh` khi `ok` la false, nen bien nhan DUNG HINH voi ok false khong neu duoc artifact nao
    for ten, doc, t6 in (("dung hinh, ok false", NEN["khong_xanh"], "luat_C:C1"), ("neu artifact, ok false (sai hinh)", None, "luat_C:C1")):
        g = gh()
        lu = g.luot[20]
        lu["bn"] = dict(lu["bn"], ok=False) if doc is None else doc
        dat_goi(g, lu, [("bien_nhan_audit.json", bn_byte(lu))])
        ma, bc, nk = luot_wd(g)
        mong((dem(nk, "GET", r"/actions/artifacts/20\d+/zip"), phep(bc, 20, "T5"), phep(bc, 20, "T6")), (1, ("dat", "dat"), ("khong_dat", t6)), ten)
# Dong 134 (T5 tai khi `ok` khac true): TUONG DUONG THEO SCHEMA, khong tinh vao mau so, khong duoc doi giet — chu kho mien quan sat tai
# https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7157619068. Schema GHIM-B1A cam `job`/`manh` khi `ok` la false, nen quan sat
# "0 -> >= 1 loi goi D5" cua dac ta khong dung duoc; ca n2_t5_ok_false van canh hai dau vao dung duoc.

def _ca_tran(ten, qua, dung, tran_cua):
    """Tran tiem nho, ZIP that nen deflate: duoi va bang tran nhu doi chung hop le; tren tran la KHONG HOAN TAT (`goi_vuot_tran`), khong bao gio `khong_dat`."""
    for hau, them in (("duoi", 1), ("bang", 0), ("tren", -1)):
        def chay(them=them):
            g = gh()
            n = dung(g, g.luot[20])
            ma, bc, nk = luot_wd(g, tran={tran_cua: n + them})
            mong(phep(bc, 20, qua), (KDD, "goi_vuot_tran") if them < 0 else ("dat", "dat"), f"{tran_cua} = {n} {them:+d}")
            mong(S(bc)[0], KDD if them < 0 else "fresh", "S")
        ca(chay, f"{ten}_{hau}")

_ca_tran("n2_muc_t2", "T2", lambda g, lu: len(zipfile.ZipFile(io.BytesIO(dat_goi(g, lu, [("a/", b""), ("b/", b""), ("bien_nhan_audit.json", bn_byte(lu))]))).infolist()), "TRAN_MUC_ZIP")
def bc_goc(g, lu): return zipfile.ZipFile(io.BytesIO(g.goi[lu["arts"][0]["id"]])).read("dau-job.json")
_ca_tran("n2_muc_t5", "T5", lambda g, lu: (doi_bang_chung(g, lu, tep=[("dau-job.json", bc_goc(g, lu)), ("a/", b""), ("b/", b"")]), 3)[1], "TRAN_MUC_ZIP")
_ca_tran("n2_giai_nen_t2", "T2", lambda g, lu: len(bn_byte(lu)), "TRAN_GIAI_NEN")

def _to_bang_chung(g, lu):
    nd = bc_goc(g, lu) + b" " * 20000
    doi_bang_chung(g, lu, tep=[("dau-job.json", nd)])
    return len(nd)
_ca_tran("n2_giai_nen_t5", "T5", _to_bang_chung, "TRAN_GIAI_NEN")
khong("d108", "d108", "n2_muc_t2_tren", "n2_muc_t5_tren")
db("d109", "d109", 'dem > c.tran["TRAN_GIAI_NEN"]', "False", "n2_giai_nen_t2_tren", "n2_giai_nen_t5_tren")
db("d112", "d112", 'dem > c.tran["TRAN_GIAI_NEN"]', 'dem >= c.tran["TRAN_GIAI_NEN"]', "n2_giai_nen_t2_bang")
db("d111", "d111", "return VUOT", 'raise ValueError("vuot tran")', "n2_giai_nen_t2_tren")

@ca
def n2_tong_vuot():
    for them, mong_s in ((-1, (KDD, "het_tai_nguyen_danh_gia", None, 1)), (0, ("fresh", "khung_xanh", "a" * 40, 2))):
        g = dat_than(gh(), nt_cu(da_bao=sk(KDD, "het_tai_nguyen_danh_gia")))
        tong = sum(i.file_size for b in g.goi.values() for i in zipfile.ZipFile(io.BytesIO(b)).infolist())
        ma, bc, nk = luot_wd(g, tran={"TRAN_GIAI_NEN_TONG": tong + them})
        mong((*S(bc), bc["sha_audit"], dem(nk, "PATCH")), mong_s, f"tong {them:+d}")
khong("d110", "d110", "n2_tong_vuot")

class thay_ten:
    """Thay MOT ten trong khong gian ten cua mo-dun trong luc chay (tiem loi vao nguyen ham, I3)."""
    def __init__(self, ten, moi): self.ten, self.moi = ten, moi
    def __enter__(self):
        self.cu = getattr(M, self.ten)
        setattr(M, self.ten, self.moi(self.cu))
    def __exit__(self, *a): setattr(M, self.ten, self.cu)

MA_TIEM = f"{LoiTiem.__module__}.{LoiTiem.__qualname__}"

def nem_khi(dk):
    """Ham boc: nem LoiTiem khi `dk(*doi so)` dung, khong thi goi nguyen ban."""
    def boc(goc):
        def f(*a, **k):
            if dk(*a, **k):
                raise LoiTiem("tiem")
            return goc(*a, **k)
        return f
    return boc

def _ca_tiem(ten, diem, dk, kiem):
    def chay():
        g = gh()
        with thay_ten(diem, nem_khi(lambda *a, **k: dk(g, *a, **k))):
            try:
                ma, bc, nk = luot_wd(g)
            except LoiTiem:
                bang(False, "lop tiem lan khoi ham chinh (bien ngoai le cua nguyen ham bi go)")
        bang(S(bc)[0] != "fresh", "khong bao gio fresh")
        kiem(bc)
    ca(chay, ten)

_ca_tiem("n2_tiem_doc_json", "_tho_json", lambda g, byte: byte == bn_byte(g.luot[20]), lambda bc: mong((phep(bc, 20, "T2"), S(bc)[1]), (("khong_dat", "bien_nhan_khong_phai_json"), "khung_do")))
_ca_tiem("n2_tiem_doc_zip", "_tho_zip", lambda g, c, byte: byte == g.goi[g.luot[20]["idb"]], lambda bc: mong((phep(bc, 20, "T2"), S(bc)[1]), (("khong_dat", "bien_nhan_goi_hong"), "khung_do")))
_ca_tiem("n2_tiem_yaml", "_tho_yaml", lambda g, mo_dun, byte: True, lambda bc: mong((phep(bc, 20, "T3"), S(bc)[1]), (("khong_dat", "hinh_workflow_la"), "khung_do")))
_ca_tiem("n2_tiem_nap_thu_vien", "_tho_nap_thu_vien", lambda g, ten, schema=None: True, lambda bc: mong((bc["ma_chi_tiet"], bc["ma_ly_do"]), ("nap_thu_vien_nem:" + MA_TIEM, "nap_thu_vien_nem")))
_ca_tiem("n2_tiem_tieu_dung", "tieu_dung", lambda g, V, b, rest, ngoai: rest["run"]["id"] == 20, lambda bc: mong((phep(bc, 20, "T6"), S(bc)), ((KDD, "tieu_dung_nem:" + MA_TIEM), (KDD, "khung_khong_do_duoc"))))
db("d52", "bien:doc_json", "except Exception", "except ValueError", "n2_tiem_doc_json")
db("d53", "bien:doc_zip", "except Exception", "except zipfile.BadZipFile", "n2_tiem_doc_zip")
db("d54", "bien:yaml", "except Exception", "except mo_dun.YAMLError", "n2_tiem_yaml")
db("d114", "bien:nap_thu_vien", "except Exception", "except ImportError", "n2_tiem_nap_thu_vien")
db("d55", "bien:tieu_dung", "except Exception", "except ZeroDivisionError", "n2_tiem_tieu_dung")

@ca
def n2_tiem_transport():
    g, ma, bc, nk = mot(lambda g, lu: g.loi(D1U, LoiTiem("a"), LoiTiem("b"), LoiTiem("c")))
    mong((bc["trang_thai"], bc["ma_chi_tiet"], dem(nk, "GET", D1U), g.ngu_nk), (KDD, "transport_nem:" + MA_TIEM, 3, [1, 2]))
db("d113", "bien:transport", "except Exception", "except OSError", "n2_tiem_transport")

@ca
def n2_keyboard_interrupt():
    g = gh()
    g.loi(D1U, KeyboardInterrupt())
    try:
        luot_wd(g)
    except KeyboardInterrupt:
        return
    bang(False, "KeyboardInterrupt tu transport bi nuot")
db("d56", "bien:transport", "except Exception", "except BaseException", "n2_keyboard_interrupt")

def dem_lan(n):
    """Dieu kien dung o DUNG lan goi thu `n` (dem tu 1)."""
    so = [0]
    def dk(*a, **k):
        so[0] += 1
        return so[0] == n
    return dk

@ca
def n2_tiem_kiem_nhip_tim():
    g = dat_than(gh(), nt_cu())
    with thay_ten("kiem_nhip_tim", nem_khi(dem_lan(1))):
        try:
            ma, bc, nk = luot_wd(g)
        except LoiTiem:
            bang(False, "lop tiem lan khoi ham chinh")
    mong((bc["nhip_tim_truoc"], S(bc), dem(nk, "POST"), ma, nt_tren(g)["da_bao"]["loai"]),
         ({"trang_thai": "khong_doc_duoc", "ma": "kiem_nhip_tim_nem:" + MA_TIEM}, ("fresh", "khung_xanh"), 1, 0, "nhip_tim_gian_doan"))
db("d115", "bien:kiem_nhip_tim", "except Exception", "except ZeroDivisionError", "n2_tiem_kiem_nhip_tim")

@ca
def n2_tiem_kiem_nhip_tim_ghi():
    g = dat_than(gh(), nt_cu())
    truoc = g.issue[1520]["body"]
    with thay_ten("kiem_nhip_tim", nem_khi(dem_lan(2))):
        ma, bc, nk = luot_wd(g)
    mong((bc["nhip_tim_truoc"]["trang_thai"], dem(nk, "PATCH"), dem(nk, "POST"), ma, bc["ghi"].get("W2"), g.issue[1520]["body"] == truoc),
         ("moi", 0, 0, 3, "kiem_nhip_tim_nem:" + MA_TIEM, True))

@ca
def n2_luoi_an_toan():
    g = gh()
    with thay_ten("_gop", nem_khi(lambda *a: True)):
        try:
            ma, bc, nk = luot_wd(g)
        except LoiTiem:
            bang(False, "luoi an toan bi go: lop tiem lan khoi ham chinh, pha ghi khong chay")
    mong((S(bc), bc["ma_chi_tiet"], bc["dong_den"] == bc["dong_den_truoc"], dem(nk, "PATCH") >= 1, ma), ((KDD, "danh_gia_nem"), "danh_gia_nem:" + MA_TIEM, True, True, 1))
tho("d57", "except Exception as e:  # luoi an toan", "except ZeroDivisionError as e:  # luoi an toan", "n2_luoi_an_toan")

# ---- Nghiem thu 4: gop khung, nghia vu khung cu, trang thai tong S1-S9 va bien ----
def w(n): return P0 - TD(days=7 * n)   # khung cu thu n truoc P

def tt(f="dat", p="dat", T=T0, nt=None, sua=None, on_dinh=False, **kw):
    """Dung nen theo trang thai tung khung roi chay MOT luot. `on_dinh`: lap lai o thu tu API dao va o HAI TRANG, doi cung S, ma, sha_audit, dong_den."""
    cu = {k: kw.pop(k) for k in list(kw) if re.fullmatch(r"k\d+", k)}
    def dung(dao=False, trang=100):
        g = gh(f, p, **cu)
        if sua:
            sua(g)
        if nt is not None:
            dat_than(g, nt)
        g.thu_tu, g.trang = (g.thu_tu[::-1] if dao else g.thu_tu), trang
        return (g, *luot_wd(g, T, **dict(kw)))
    kq = dung()
    if on_dinh:
        for khac in (dung(dao=True), dung(trang=1)):
            mong(tuple(khac[2].get(k) for k in ("trang_thai", "ma_chi_tiet", "sha_audit", "dong_den")),
                 tuple(kq[2].get(k) for k in ("trang_thai", "ma_chi_tiet", "sha_audit", "dong_den")), "ket qua khong duoc phu thuoc thu tu/trang API")
    return kq

def ca_s(ten, muon, **kw):
    """Mot ca trang thai tong: doi DUNG (trang_thai, ma_ly_do) va moi khoa bao cao khac neu trong `them`."""
    them = kw.pop("them", {})
    kw.setdefault("on_dinh", True)
    def chay():
        g, ma, bc, nk = tt(**kw)
        mong((S(bc), {k: bc.get(k) for k in them}), (muon, them), ten)
    ca(chay, ten)

ST, XANH, CHO = "stale_or_missing", ("fresh", "khung_xanh"), ("due_in_progress", "khung_dang_cho")
ca_s("n4_gop_dat_thang_do", XANH, sua=lambda g: them(g, 21, F0, "do"), on_dinh=True)
ca_s("n4_gop_do_thang_kdd", (ST, "khung_do"), f="do", sua=lambda g: them(g, 21, F0, "kdd"), on_dinh=True)
ca_s("n4_gop_kdd_thang_chay", (KDD, "khung_khong_do_duoc"), f="kdd", sua=lambda g: them(g, 21, F0, "chay"), T=F0 + TD(hours=6), on_dinh=True)
tho("d17", '(DAT, DAT), (KHONG_DAT, "do")', '(KHONG_DAT, "do"), (DAT, DAT)', "n4_gop_dat_thang_do")
tho("d18", '(KHONG_DAT, "do"), (KHONG_DO_DUOC, KHONG_DO_DUOC)', '(KHONG_DO_DUOC, KHONG_DO_DUOC), (KHONG_DAT, "do")', "n4_gop_do_thang_kdd")
tho("d19", '(KHONG_DO_DUOC, KHONG_DO_DUOC), ("dang_chay", "dang_chay")', '("dang_chay", "dang_chay"), (KHONG_DO_DUOC, KHONG_DO_DUOC)', "n4_gop_kdd_thang_chay")
khong("d136", "S2", "n4_gop_do_thang_kdd")
khong("d137", "S5", "n4_gop_dat_thang_do")
khong("d138", "S6", "n4_gop_kdd_thang_chay")

@ca
def n4_s1_khong_tron():   # D1 con rel="next" sau 10 trang, MA phan da thay co luot dat cho F va tong khop
    def sua(g):
        g.thu_tu = [20, 10]
        for i in range(30, 41):
            g.luot[i] = {"d1": dict(g.luot[10]["d1"], id=i, created_at=viet(w(12) + TD(hours=3)))}
            g.thu_tu.append(i)
        sua_tra(g, D1U, lambda t: t.update(total_count=10))
    g = gh()
    sua(g)
    g.trang = 1
    ma, bc, nk = luot_wd(g)
    mong((bc["trang_thai"], bc["ma_chi_tiet"], bc["sha_audit"], dem(nk, "GET", D1U)), (KDD, "khong_tron", None, 10))
db("d07_69", "d07", 'return None, "khong_tron"', "break", "n4_s1_khong_tron", "n8_doi_soat_khong_tron")

ca_s("n4_tran_khung", (KDD, "qua_nhieu_khung_can_soat"), khung_dau=viet(w(6)), **{f"k{i}": "dat" for i in range(1, 7)})
ca_s("n4_tran_khung_doi_chung", XANH, khung_dau=viet(w(5)), them={"dong_den": viet(P0)}, **{f"k{i}": "dat" for i in range(1, 6)})
khong("d25", "d25", "n4_tran_khung")
ca_s("n4_s2_truoc_s3", (ST, "khung_do"), f="do", p="do", them={"nghia_vu": [{"khung": viet(P0), "gop": "do"}]})
tho("d20", '''    if gF == "do":  # S2
        s, ma = "stale_or_missing", "khung_do"
    elif any(gop[k] != KHONG_DO_DUOC for k in O):  # S3
        s, ma = "stale_or_missing", "slot_cu_chua_dong"''', '''    if any(gop[k] != KHONG_DO_DUOC for k in O):  # S3
        s, ma = "stale_or_missing", "slot_cu_chua_dong"
    elif gF == "do":  # S2
        s, ma = "stale_or_missing", "khung_do"''', "n4_s2_truoc_s3")
ca_s("n4_s3_p_vang", (ST, "slot_cu_chua_dong"), p="vang")
khong("d21", "S3", "n4_s3_p_vang")
ca_s("n4_r_khung_cu", (ST, "slot_cu_chua_dong"), k1="do", khung_dau=viet(w(1)), them={"dong_den_truoc": viet(w(2))}, on_dinh=True)
db("d23", "d23", "range(so)", "range(min(so, 1))", "n4_r_khung_cu")

@ca
def n4_dong_den_tien_to():   # khung dong (P) dung SAU khung chan (P - 7 ngay): dong_den khong vuot qua khung chan; chay lai khung chan thi dong duoc
    g, ma, bc, nk = tt(k1="do", khung_dau=viet(w(1)))
    mong((bc["dong_den"], nt_tren(g)["dong_den"]), (viet(w(2)),) * 2)
    g.luot[9]["arts"] = dung_luot(9, w(1), sha="e" * 40)["arts"]
    ma, bc, nk = luot_wd(g, T0 + TD(hours=6), khung_dau=viet(w(1)))
    mong((S(bc), bc["dong_den"], bc["nhip_tim_truoc"]["trang_thai"]), (XANH, viet(P0), "moi"), "sau khi khung chan co bien nhan hop le")
db("d24", "d24", "break", "continue", "n4_dong_den_tien_to")
ca_s("n4_s4_p_kdd", (KDD, "slot_cu_khong_do_duoc"), p="kdd")
khong("d22", "S4", "n4_s4_p_kdd")

def goi_luot(nk, rid): return dem(nk, "GET", rf"/actions/runs/{rid}(/|$)") + dem(nk, "GET", rf"/artifacts/{rid}0\d+/zip")

@ca
def n4_dong_tay():   # khung dong tay duoc giai TRUOC khi dung tap danh gia: 0 loi goi cho luot cua no; gop `dong_tay`
    kw = {"khung_dau": viet(w(1)), "dong_tay": {viet(w(1)): "lich roi, artifact het han"}}
    for k1 in ("do", "vang"):
        g, ma, bc, nk = tt(k1=k1, **kw)
        mong((goi_luot(nk, 9), S(bc), bc["dong_den"], bc["khung"][viet(w(1))]), (0, XANH, viet(P0), {"gop": "dong_tay", "ly_do": "lich roi, artifact het han"}), k1)
    mong(S(tt(k1="do", khung_dau=viet(w(1)))[2]), (ST, "slot_cu_chua_dong"), "doi chung KHUNG_DONG_TAY rong")
db("d26", "d26", '("dong_tay", DAT)', "(DAT,)", "n4_dong_tay")
db("d85", "d85", " - set(tay)", "", "n4_dong_tay")

@ca
def n4_dong_tay_p():
    g, ma, bc, nk = tt(p="do", dong_tay={viet(P0): "dong tay"})
    mong((goi_luot(nk, 10), S(bc)), (0, XANH))

ca_s("n4_dong_tay_p_cho", (ST, "khung_truoc_khong_xanh"), f="chay", p="do", T=F0 + TD(hours=6), dong_tay={viet(P0): "dong tay"}, them={"sha_audit": None})
db("d86", "d86", '"dong_tay" if k in tay', "DAT if k in tay", "n4_dong_tay_p_cho")
ca_s("n4_dong_tay_f", XANH, dong_tay={viet(F0): "khung hien hanh khong dong tay duoc"})
db("d87", "d87", " and k <= P", "", "n4_dong_tay_f")
ca_s("n4_dat_lai_goc", (ST, "slot_cu_chua_dong"), nt=nt_cu(schema="x"), khung_dau=viet(w(1)), them={"dong_den_truoc": viet(w(2))})
ca_s("n4_dat_lai_goc_doi_chung", XANH, nt=nt_cu(), khung_dau=viet(w(1)), them={"dong_den_truoc": viet(P0)})
db("d27", "d27", "else kd - BAY_NGAY", "else khung_cron(T) - BAY_NGAY * 2", "n4_dat_lai_goc")
ca_s("n4_s6", (KDD, "khung_khong_do_duoc"), f="kdd")
ca_s("n4_s7_bien", CHO, f="vang", T=F0 + TD(hours=12))
ca_s("n4_s7_qua", (ST, "khung_vang"), f="vang", T=F0 + TD(hours=12, seconds=1))
db("d28", "S7", "T > F + TRE_LICH_TOI_DA", "T >= F + TRE_LICH_TOI_DA", "n4_s7_bien")
khong("d29", "S7", "n4_s7_qua")
ca_s("n4_s8_bien", CHO, f="chay", T=P0 + TD(days=8))
ca_s("n4_s8_qua", (ST, "qua_tuoi_8_ngay"), f="chay", T=P0 + TD(days=8, seconds=1))
db("d30", "S8", "T - P > TUOI_TOI_DA", "T - P >= TUOI_TOI_DA", "n4_s8_bien")
khong("d31", "S8", "n4_s8_qua")
ca_s("n4_s9_p_dat", CHO, f="chay", T=F0 + TD(hours=6), them={"sha_audit": "e" * 40})
ca_s("n4_s9_p_kdd", (KDD, "khung_truoc_khong_do_duoc"), f="chay", p="kdd", T=F0 + TD(hours=6), nt=nt_cu(F0 + TD(hours=6), 2), them={"nghia_vu": []})
ca_s("n4_s9_p_vang", (ST, "khung_truoc_khong_xanh"), f="chay", p="vang", T=F0 + TD(hours=6), khung_dau=viet(F0))
ca_s("n4_t_bang_f", CHO, f="vang", T=F0)
khong("d139", "S9a", "n4_s9_p_dat")
db("d32", "S9a", "gP == DAT", "gP in (DAT, KHONG_DO_DUOC)", "n4_s9_p_kdd")
db("d33", "S9a", "gP == DAT", "gP != KHONG_DO_DUOC", "n4_s9_p_vang")

@ca
def n4_u7_jobs():   # ban ghi cung (name, run_attempt): `id` nho success, `id` lon failure, API tra `id` lon truoc
    for kl, muon in ((("success", "failure"), "luat_C:C4"), (("failure", "success"), "luat_C:C2+C4")):
        for dao in (False, True):
            def sua(g, lu):
                lu["jobs"][0]["conclusion"] = kl[0]
                lu["jobs"].insert(0, dict(lu["jobs"][0], id=lu["jobs"][0]["id"] + 500, conclusion=kl[1]))
                lu["jobs"] = lu["jobs"][::-1] if dao else lu["jobs"]
            g, ma, bc, nk = mot(sua)
            mong(lu_bc(bc, 20)["ma"], muon, f"{kl} dao={dao}")
db("d10", "d10", 'sorted(jobs, key=lambda j: j["id"])', "jobs", "n4_u7_jobs")

@ca
def n4_sha_audit_hai_trang():   # hai luot dat cung F, head_sha khac nhau, o HAI trang, `id` lon o trang dau
    def sua(g):
        g.wf["c" * 40], g.tree["c" * 40] = JOB_KV.encode(), "b" * 40
        them(g, 21, F0, "dat", sha="c" * 40)
        g.thu_tu, g.trang = [21, 20, 10], 2
    g = gh()
    sua(g)
    ma, bc, nk = luot_wd(g)
    mong((S(bc), bc["sha_audit"], dem(nk, "GET", D1U)), (XANH, "a" * 40, 2))
db("d16", "d16", "min(dat,", "max(dat,", "n4_sha_audit_hai_trang")

# ---- Nghiem thu 5: chay lai, dispatch, moc ----
@ca
def n5_chay_lai_khong_lam_tuoi():   # luot cua khung P chay lai attempt 2 hom nay: `created_at` giu nguyen nen khung giu nguyen; F vang qua 12 gio
    g = gh(f="vang", p="vang")
    them(g, 10, P0, "dat", att=2, sha="e" * 40)
    ma, bc, nk = luot_wd(g, F0 + TD(hours=13))
    mong((S(bc), lu_bc(bc, 10)["phan_quyet"], lu_bc(bc, 10)["run_attempt"]), ((ST, "khung_vang"), "dat", 2))

@ca
def n5_dispatch():   # luot workflow_dispatch khong bao gio la ung vien; transport gia van tra no trong D1 => danh sach la
    g, ma, bc, nk = mot(lambda g, lu: [lu[k].update(event="workflow_dispatch") for k in ("d1", "d2")])
    mong((bc["trang_thai"], bc["ma_chi_tiet"], goi_luot(nk, 20)), (KDD, "danh_sach_la", 0))
tho("d05", '    ("event", lambda r: ', '    ("event", lambda r: True or ', "n5_dispatch")

@ca
def n5_attempt_thap():   # attempt cao nhat thieu bien nhan: bien nhan cua attempt thap hon khong duoc dung thay
    def sua(g, lu):
        for k in ("d1", "d2"):
            lu[k]["run_attempt"] = 2
    g, ma, bc, nk = mot(sua)
    mong((phep(bc, 20, "T2"), lu_bc(bc, 20)["phan_quyet"]), (("khong_dat", "bien_nhan_vang"), "khong_dat"))
db("d06", "d06", 'if a["name"] == ten]', 'if a["name"] == ten] or [a for a in rest["artifacts"] if a["name"].startswith(f"bien-nhan-audit-{run[\'id\']}-")][:1]', "n5_attempt_thap")

@ca
def n5_lien_ket_created_at():   # luot hop le cua khung P (D2 va bien nhan nguyen ven), chi `created_at` cua phan tu D1 doi +7 ngay vao khung F
    g = dat_than(gh(f="vang"), nt_cu(T=F0 + TD(hours=1), gio_truoc=0))
    g.luot[10]["d1"]["created_at"] = viet(F0 + TD(minutes=30))
    them(g, 9, P0, "dat", sha="e" * 40)
    ma, bc, nk = luot_wd(g, F0 + TD(hours=1))
    mong((lu_bc(bc, 10)["phan_quyet"], lu_bc(bc, 10)["ma"], S(bc)), (KDD, "lien_ket_lech:created_at", (KDD, "khung_khong_do_duoc")))

# ---- Nghiem thu 6: dau vao `ngoai` doc lap voi bien nhan ----
def ca_t3(ten, yaml_byte, muon):
    def chay():
        g, ma, bc, nk = mot(lambda g, lu: g.wf.update({"a" * 40: yaml_byte}))
        mong(phep(bc, 20, "T3"), muon, ten)
    ca(chay, ten)

def kv(doan): return ("jobs:\n  dot-bien-du: {}\n" + doan).encode()

LA = ("khong_dat", "hinh_workflow_la")
ca_t3("n6_x2_name", kv("  dot-bien-gop:\n    name: hien thi\n"), LA)
ca_t3("n6_x2_khong_name", kv("  dot-bien-gop: {}\n"), ("dat", "dat"))
ca_t3("n6_trung_khoa", kv("  dot-bien-manh:\n    strategy:\n      matrix:\n        manh: [0]\n  dot-bien-manh-0: {}\n"), ("khong_dat", "job_ky_vong_trung_khoa"))
ca_t3("n6_trung_ten", kv("  dot-bien-manh:\n    strategy:\n      matrix:\n        manh: [0, 0]\n"), ("khong_dat", "job_ky_vong_trung"))
ca_t3("n6_x2_nhieu_khoa", kv("  m:\n    strategy:\n      matrix:\n        a: [0]\n        b: [1]\n"), LA)
ca_t3("n6_x2_include", kv("  m:\n    strategy:\n      matrix:\n        include: [0, 1]\n"), LA)
ca_t3("n6_x2_kieu", kv("  m:\n    strategy:\n      matrix:\n        a: [0.5, 1.5]\n"), LA)
ca_t3("n6_x2_rong", kv("  m:\n    strategy:\n      matrix:\n        a: []\n"), LA)
ca_t3("n6_x2_khong_matrix", kv("  m:\n    strategy:\n      fail-fast: false\n"), LA)
ca_t3("n6_x2_jobs", b"jobs:\n  - dot-bien-du\n", LA)
khong("d38", "d38", "n6_x2_name")
khong("d37", "d37", "n6_trung_khoa")
khong("d130", "d130", "n6_trung_ten")
for _h in ("nhieu_khoa", "include", "kieu", "rong", "khong_matrix", "jobs"):
    khong("d129_" + _h, "x2:" + _h, "n6_x2_" + _h)

@ca
def n6_job_ky_vong():   # D6 tra workflow co THEM mot job; bien nhan tu nhat quan
    g, ma, bc, nk = mot(lambda g, lu: g.wf.update({"a" * 40: JOB_KV.encode() + b"  them: {}\n"}))
    bang("C4" in str(lu_bc(bc, 20)["ma"]) and lu_bc(bc, 20)["phan_quyet"] == "khong_dat", f"mong khong_dat chua C4, duoc {lu_bc(bc, 20).get('ma')}")
db("d34", "d34", "= ten", '= b["kiem_ke_job"]["ky_vong"]', "n6_job_ky_vong")

@ca
def n6_tree():
    g, ma, bc, nk = mot(lambda g, lu: g.tree.update({"a" * 40: "c" * 40}))
    mong(lu_bc(bc, 20)["ma"], "luat_C:C5")
db("d35", "d35", "= tree_h", '= b["job"][0]["checkout_tree"]', "n6_tree")

@ca
def n6_doc_tai_sha_rest():   # bien nhan khai su_kien.sha = X khac run.head_sha; transport gia chi phuc vu D6/D7 tai run.head_sha
    def sua(g, lu):
        lu["bn"]["su_kien"]["sha"] = "d" * 40
        dat_goi(g, lu, [("bien_nhan_audit.json", bn_byte(lu))])
    g, ma, bc, nk = mot(sua)
    bang(lu_bc(bc, 20)["phan_quyet"] == "khong_dat" and "C3" in lu_bc(bc, 20)["ma"], f"mong khong_dat chua C3, duoc {lu_bc(bc, 20)['phan_quyet']} {lu_bc(bc, 20)['ma']}")
db("d36", "d36", '_t3(c, run["head_sha"])', '_t3(c, b["su_kien"]["sha"] if isinstance(b, dict) else run["head_sha"])', "n6_doc_tai_sha_rest")

# ---- Nghiem thu 7: bao cao va cau ve master ----
C1M, C2M, C3M = "master hiện tại = SHA đã audit ", "master hiện tại KHÁC SHA đã audit: master ", "chưa có SHA đã audit hợp lệ hoặc không đọc được master"

def van_ban(g, bc): return json.dumps(bc, ensure_ascii=False) + g.issue[1520]["body"] + "".join(c["body"] for c in g.issue[1520]["cm"])

@ca
def n7_cau_master():
    g, ma, bc, nk = mot()
    mong((bc["cau_master"], bc["so_sanh"]["ahead_by"]), (C1M + "a" * 40, 0), "hai SHA bang nhau")
    g, ma, bc, nk = mot(lambda g, lu: (setattr(g, "master", "f" * 40), setattr(g, "ahead", 3)))
    mong(bc["cau_master"], f"{C2M}{'f' * 40}, audit {'a' * 40}, master đi trước 3 commit", "hai SHA khac nhau")
    bang(C1M not in van_ban(g, bc) and g.issue[1520]["cm"][0]["body"].split("\n")[2] == bc["cau_master"], "khi hai SHA khac, khong van ban nao duoc chua cau thu nhat")
db("d59", "d59", " and sha_master == sha_audit", "", "n7_cau_master")

@ca
def n7_d9_loi():
    g, ma, bc, nk = mot(lambda g, lu: (setattr(g, "master", "f" * 40), g.loi(r"/compare/", (404, {}))))
    mong((bc["cau_master"], S(bc), bc["so_sanh"], ma), (f"{C2M}{'f' * 40}, audit {'a' * 40}, master đi trước khong_do_duoc commit", XANH, KDD, 0))
db("d60", "d60", "else KHONG_DO_DUOC", 'else (kq.update(trang_thai=KHONG_DO_DUOC, ma="d9_loi") or KHONG_DO_DUOC)', "n7_d9_loi")

@ca
def n7_d8_loi():
    g, ma, bc, nk = mot(lambda g, lu: g.loi(r"/git/ref/heads/master", (404, {})))
    mong((bc["cau_master"], S(bc), bc["sha_master"], ma), (C3M, XANH, KDD, 0))
db("d141", "d141", "else None", 'else kq.update(trang_thai=KHONG_DO_DUOC, ma="d8_loi")', "n7_d8_loi")

@ca
def n7_c10():   # C10 cua bien nhan `not_measured` co mat nguyen van trong bao cao; phan quyet KHONG doi
    def sua(g, lu):
        lu["bn"]["dinh_danh_definition"] = next(s["gia_tri"] for c in json.loads(F_BYTE)["ca"] for s in c.get("sua") or [] if s["duong"] == "/dinh_danh_definition"
                                                and isinstance(s.get("gia_tri"), dict) and s["gia_tri"].get("trang_thai") == "not_measured")
        dat_goi(g, lu, [("bien_nhan_audit.json", bn_byte(lu))])
    g, ma, bc, nk = mot(sua)
    mong((S(bc), lu_bc(bc, 20)["canh_bao"], lu_bc(bc, 20).get("dinh_danh_definition")), (XANH, ["C10"], g.luot[20]["bn"]["dinh_danh_definition"]))
db("d58", "d58", "if vp else", "if vp or r[1] else", "n7_c10")

# ---- Nghiem thu 8: nhip tim, giao tin, doi soat (ca nhieu luot dung CHUNG mot GitHub gia) ----
ISS, CMU, T8 = r"/issues/1520$", r"/issues/\d+/comments$", F0 + TD(hours=30)

def dat_f(g, kieu):
    """Doi trang thai khung F cua nen giua cac luot: dat (`fresh`) · do (`khung_do`) · vang (`khung_vang` khi T > F + 12 h)."""
    lu = g.luot[20]
    lu.setdefault("art_bn", lu["arts"][-1])
    lu["arts"] = [a for a in lu["arts"] if a is not lu["art_bn"]] + ([lu["art_bn"]] if kieu == "dat" else [])
    g.thu_tu = [10] + ([] if kieu == "vang" else [20])
    return g

def luot_n(g, n=0, **kw): return luot_wd(g, T8 + TD(hours=6 * n), **kw)

def post_mat(g, loi=None):
    """POST dau tien: may chu LUU comment roi phan hoi mat (transport nem)."""
    da = []
    g.sua.append((CMU, "POST", lambda s, pt, url, than: None if da else (da.append(s.xu_ly(pt, url, than)), loi or ConnectionError("mat phan hoi"))[1]))

def nen_cho(loai="canh_bao", hong=(500, {})):
    """Luot 0 de lai DUNG MOT su kien dang cho loai `loai` (POST hong, may chu KHONG luu). Tra (g, su kien)."""
    g = gh()
    dat_than(dat_f(g, "do"), nt_cu(T8)) if loai == "canh_bao" else dat_than(g, nt_cu(T8, da_bao=sk(ST, "khung_do")) if loai == "hoi_phuc" else nt_cu(T8, 25))
    truoc = nt_tren(g)["da_bao"]
    g.loi(CMU, hong, pt="POST")
    ma, bc, nk = luot_n(g)
    mong((ma, (nt_tren(g)["cho_bao"] or {}).get("loai"), dem(nk, "POST"), nt_tren(g)["da_bao"]), (3, loai, 1, truoc), "luot 0: su kien nam BEN trong cho_bao, da_bao khong doi, MOT POST")
    return g, nt_tren(g)["cho_bao"]

def chen_cm(g, e, login=BOT, cid=9001, them="", luc=None):
    g.issue[1520]["cm"].append({"id": cid, "body": "x\n" + M.TT_SK + json.dumps(e, sort_keys=True, separators=(",", ":")) + them, "user": {"login": login},
                                "created_at": luc or viet(T8), "updated_at": luc or viet(T8)})

def giao(g, nk, e, so_post=1):
    """Sau mot luot: so POST, va khi su kien `e` da giao thi `da_bao` = `e` + comment_id, `cho_bao` null, dung MOT comment khop."""
    nt = nt_tren(g)
    mong((dem(nk, "POST"), {k: v for k, v in (nt["da_bao"] or {}).items() if k != "comment_id"}, nt["cho_bao"], len(cm_khop(g, e))), (so_post, e, None, 1), "giao su kien")

@ca
def n8_dinh_dang():   # than dung hai dong ASCII dong bang; comment dung nam dong
    g, e = nen_cho()
    ma, bc, nk = luot_n(g, 1)
    than, cm = g.issue[1520]["body"].split("\n"), g.issue[1520]["cm"][0]["body"].split("\n")
    mong((than[0], len(than), than[1] == "B2_NHIP_TIM: " + json.dumps(nt_tren(g), ensure_ascii=True, sort_keys=True, separators=(",", ":"))),
         ("B2 watchdog do tuoi full audit (wp1494). Than Issue do workflow ghi de moi luot; dung sua tay.", 2, True), "than Issue")
    mong((cm[0], cm[1], cm[3], cm[4], len(cm)), ("B2 watchdog: canh_bao: stale_or_missing (khung_do)", "B2_SU_KIEN: " + json.dumps(e, sort_keys=True, separators=(",", ":")),
                                                 "nhip_tim_truoc: moi", f"https://github.com/ducthangho/tra-luat/actions/runs/{g.rid - 1}/attempts/1", 5), "comment")

def doc_truoc(nt=None, than=None, T=T8, **kw):
    g = gh()
    g.issue[1520]["body"] = than if than is not None else dat_than(g, nt).issue[1520]["body"]
    ma, bc, nk = luot_wd(g, T, **kw)
    return (bc["nhip_tim_truoc"]["trang_thai"], bc["nhip_tim_truoc"]["ma"], dem(nk, "POST"))

def ca_doc(ten, muon, **kw):
    ca(lambda: mong(doc_truoc(**kw), muon, ten), ten)

DNT = M.TT_NT + json.dumps(nt_cu(T8), sort_keys=True, separators=(",", ":"))
KDOC = "khong_doc_duoc"
ca_doc("n8_mien_doi_chung", ("moi", "moi", 0), nt=nt_cu(T8))
ca_doc("n8_hai_dong", (KDOC, "nhip_tim_trung", 1), than="\n".join((M.DONG_1, DNT, DNT)))
ca_doc("n8_khong_phai_object", (KDOC, "nhip_tim_khong_phai_object", 1), than=M.DONG_1 + "\n" + M.TT_NT + "[]")
ca_doc("n8_tap_khoa_goc", (KDOC, "nhip_tim_tap_khoa", 1), nt=nt_cu(T8, x=1))
ca_doc("n8_thieu_khoa", (KDOC, "nhip_tim_tap_khoa", 1), nt={k: v for k, v in nt_cu(T8).items() if k != "sha_master"})
ca_doc("n8_luc_tuong_lai", (KDOC, "nhip_tim_tuong_lai", 1), nt=nt_cu(T8, -1))
ca_doc("n8_bien_24h", ("moi", "moi", 0), nt=nt_cu(T8, 24))
ca_doc("n8_qua_24h", ("cu", "cu", 1), nt=nt_cu(T8, 24 + 1 / 3600))
ca_doc("n8_nhip_tim_cu", ("cu", "cu", 1), nt=nt_cu(T8, 25))
khong("d64", "d64", "n8_hai_dong")
khong("d142", "d142", "n8_khong_phai_object")
khong("d116", "d116", "n8_tap_khoa_goc")
khong("d62", "d62", "n8_luc_tuong_lai")
db("d63", "d63", "> datetime.timedelta(hours=24)", ">= datetime.timedelta(hours=24)", "n8_bien_24h")
khong("d74", "(c)", "n8_nhip_tim_cu")

@ca
def n8_json_hong():
    kq = doc_truoc(than=M.DONG_1 + "\n" + M.TT_NT + "{")
    bang(kq[0] == KDOC and kq[1].startswith("nhip_tim_json_hong:doc_json_nem:") and kq[2] == 1, f"duoc {kq}")

CB = sk("fresh", "khung_xanh", "hoi_phuc", cid=None)   # mot `cho_bao` hop le de lam nen cho m27..m33
MIEN = [(1, "schema", {"schema": "x"}), (2, "luc", {"luc": "2026-13-01T00:00:00Z"}), (4, "run_id", {"run_id": True}), (5, "run_id", {"run_id": 0}),
        (6, "run_attempt", {"run_attempt": "1"}), (7, "run_attempt", {"run_attempt": 10**10}), (8, "trang_thai", {"trang_thai": "xanh"}),
        (9, "ma_ly_do", {"ma_ly_do": "x y"}), (10, "ma_ly_do", {"ma_ly_do": "khung_do"}), (11, "khung", {"khung": viet(P0)}), (12, "sha_audit", {"sha_audit": "x"}),
        (13, "sha_audit", {"sha_audit": None}), (14, "sha_master", {"sha_master": "x"}), (15, "dong_den", {"dong_den": "2026-12-05T19:17:01Z"}),
        (16, "dong_den", {"dong_den": viet(w(2))}), (17, "da_bao", {"da_bao": "x"}), (25, "da_bao", {"da_bao": dict(sk("fresh", "khung_xanh"), comment_id=0)}), (26, "cho_bao", {"cho_bao": "x"})]
for _j, (_k, _v) in enumerate((("id", "0-1"), ("loai", "x"), ("trang_thai", "xanh"), ("ma_ly_do", "X"), ("ma_ly_do", "khung_do"), ("khung", "x"), ("khung", viet(F0 + TD(days=7))))):
    MIEN += [(18 + _j, "da_bao", {"da_bao": dict(sk("fresh", "khung_xanh"), **{_k: _v})}), (27 + _j, "cho_bao", {"cho_bao": dict(CB, **{_k: _v})})]
for _i, _mk, _sua in MIEN:
    ca_doc(f"n8_mien_m{_i}", (KDOC, f"nhip_tim_sai_mien:{_mk}:m{_i}", 1), nt=nt_cu(T8, **_sua))
for _i, _mk in [(i, k) for i, k, _ in MIEN if i in (1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 16, 25)]:
    tho(f"d61_m{_i}", f'return SAI("{_mk}", {_i})', "pass", f"n8_mien_m{_i}")
tho("d61_m12_m14", "return SAI(k, i)", "pass", "n8_mien_m12", "n8_mien_m14")
tho("d61_m17_m26", "return SAI(ten, so)", "pass", "n8_mien_m17", "n8_mien_m26")
for _j in range(7):
    tho(f"d61_m{18 + _j}_m{27 + _j}", "return SAI(khoa, i" + (f" + {_j})" if _j else ")"), "pass", f"n8_mien_m{18 + _j}", f"n8_mien_m{27 + _j}")

@ca
def n8_phan_chung_luot_1():   # phan chung cua review luot 1: sai KIEU => khong_doc_duoc, khong bao gio `moi`
    for sua in ({"ma_ly_do": 5}, {"khung": 5}, {"sha_master": 5}, {"run_attempt": 0}, {"dong_den": None}, {"da_bao": []}, {"luc": 5}):
        mong(doc_truoc(nt=nt_cu(T8, **sua))[0], KDOC, str(sua))

@ca
def n8_truoc_khung_dau():   # KHUNG_DAU sau F: khoang `dong_den` van KHAC RONG (ve max cua m16); luot 2 doc `moi`
    for kd in (F0 + TD(days=7), F0, P0):
        g = gh()
        ma, bc, nk = luot_n(g, khung_dau=viet(kd))
        mong((dem(nk, "PATCH") >= 1, ma != 3, bc["ghi"].get("W2")), (True, True, "da_gui"), f"luot 1, KHUNG_DAU {kd}: nguoi ghi phai DAT bo kiem va gui W2")
        mong(nt_tren(g)["dong_den"], viet(max(kd - TD(days=7), P0 if kd <= P0 else kd - TD(days=7))), "dong_den ghi ra")
        ma, bc, nk = luot_n(g, 1, khung_dau=viet(kd))
        mong((bc["nhip_tim_truoc"]["ma"], dem(nk, "POST")), ("moi", 0), f"luot 2, KHUNG_DAU {kd}")
db("d94", "d94", "max(goc, khung_cron(luc) - BAY_NGAY)", "khung_cron(luc) - BAY_NGAY", "n8_truoc_khung_dau")

@ca
def n8_ma_dau_unicode():   # duoi cua ma chi tiet (ten lop Unicode dai 210 ky tu) khong bao gio vao nhip tim
    lop = type("Lỗi" + "ờ" * 207, (Exception,), {})
    g = gh()
    with thay_ten("_gop", lambda goc: lambda *a: (_ for _ in ()).throw(lop("tiem"))):
        ma, bc, nk = luot_n(g)
    mong((dem(nk, "PATCH") >= 1, ma, bc["ghi"].get("W2"), bc["ma_chi_tiet"]), (True, 1, "da_gui", f"danh_gia_nem:{lop.__module__}.{lop.__qualname__}"))
    mong(nt_tren(g)["ma_ly_do"], "danh_gia_nem", "nhip tim chi mang DAU MA")
    mong(luot_n(g, 1)[1]["nhip_tim_truoc"]["ma"], "moi", "luot 2")
db("d95", "d95", '"ma_ly_do": dau_ma(kq["ma"]), "khung"', '"ma_ly_do": kq["ma"], "khung"', "n8_ma_dau_unicode")

@ca
def n8_tu_kiem_truoc_patch():   # nhip tim tu sinh khong qua bo kiem => KHONG PATCH, than giu nguyen byte
    g = dat_than(gh(), nt_cu(T8))
    truoc = g.issue[1520]["body"]
    with thay_ten("dau_ma", lambda goc: lambda ma: "khong hop le"):
        ma, bc, nk = luot_n(g)
    mong((dem(nk, "PATCH"), dem(nk, "POST"), ma, g.issue[1520]["body"] == truoc), (0, 0, 3, True))

@ca
def n8_tu_kiem_truoc_patch2():   # comment mang id 10^20: nhip tim cua W7 vi pham m25 => W7 khong gui
    g = dat_than(dat_f(gh(), "do"), nt_cu(T8))
    g.id_cm = 10**20 - 1
    ma, bc, nk = luot_n(g)
    mong((dem(nk, "POST"), dem(nk, "PATCH"), ma, bc["ghi"].get("W7")), (1, 1, 3, "nhip_tim_sai_mien:da_bao:m25"))
db("d96", "d96", "goi_kiem_nhip_tim(nt, T, khung_dau)", "None", "n8_tu_kiem_truoc_patch", "n8_tu_kiem_truoc_patch2")

def ca_luat(ten, f, da_bao, so_post, loai=None, gio_truoc=6):
    def chay():
        g = dat_than(dat_f(gh(), f), nt_cu(T8, gio_truoc, da_bao=da_bao))
        ma, bc, nk = luot_n(g)
        mong((dem(nk, "POST"), (nt_tren(g)["da_bao"] or {}).get("loai") if so_post else None, ma), (so_post, loai, {"dat": 0}.get(f, 1)), ten)
    ca(chay, ten)

ca_luat("n8_lap_cung_bo", "do", sk(ST, "khung_do"), 0)
ca_luat("n8_doi_ma_ly_do", "do", sk(ST, "khung_vang"), 1, "canh_bao")
ca_luat("n8_hoi_phuc", "dat", sk(ST, "khung_do"), 1, "hoi_phuc")
db("d72", "(a)", " and bo != C", "", "n8_lap_cung_bo")
khong("d73", "(b)", "n8_hoi_phuc")

def ca_doi_issue(ten, f, muon):
    def chay():
        g = dat_than(dat_f(gh(), f), nt_cu(T8, cho_bao=sk(ST, "khung_do", id="5555-1", cid=None)))
        g.issue[1521] = {"body": "", "state": "open", "cm": []}
        ma, bc, nk = luot_n(g, issue=1521)
        cm = g.issue[1521]["cm"]
        e = json.loads(cm[0]["body"].split("\n")[1][len(M.TT_SK):]) if len(cm) == 1 else {}
        mong((len(cm), e.get("loai"), (e.get("trang_thai"), e.get("ma_ly_do")), e.get("id"), dem(nk, "GET", ISS) + dem(nk, "PATCH", ISS), len(g.issue[1520]["cm"])),
             (1, muon[0], muon[1:], f"{g.rid - 1}-1", 0, 0), ten)
    ca(chay, ten)

ca_doi_issue("n8_doi_issue_canh_bao", "vang", ("canh_bao", ST, "khung_vang"))
ca_doi_issue("n8_doi_issue_hoi_phuc", "dat", ("nhip_tim_gian_doan", "fresh", "khung_xanh"))
db("d146", "(a)", "bo != C:", 'bo != C and tt_nt == "moi":', "n8_doi_issue_canh_bao")

def ca_giao_lai(ten, loai, ma_mong):
    def chay():
        g, e = nen_cho(loai, (403, {}))
        ma, bc, nk = luot_n(g, 1)
        giao(g, nk, e)
        mong((ma, e["id"] != f"{g.rid - 1}-1", bc["ghi"].get("W1"), bc["thong_bao_hoan"]), (ma_mong, True, "chua_giao", None), "luot 1: gui lai CUNG su kien, cung id")
        mong(dem(luot_n(g, 2)[2], "POST"), 0, "luot 2 cung S")
    ca(chay, ten)

ca_giao_lai("n8_giao_lai_canh_bao", "canh_bao", 1)
ca_giao_lai("n8_giao_lai_hoi_phuc", "hoi_phuc", 0)
ca_giao_lai("n8_giao_lai_gian_doan", "nhip_tim_gian_doan", 0)
ca_giao_lai("n8_giu_id", "canh_bao", 1)
ca(lambda: nen_cho("canh_bao"), "n8_post_khong_thu_lai")
db("d66", "d66", "None if da_bao1 is KHONG_BIET else da_bao1, cho_bao1)", "(dict(cho_bao1, comment_id=1) if cho_bao1 else None if da_bao1 is KHONG_BIET else da_bao1), cho_bao1)", "n8_giao_lai_canh_bao")
db("d71", "d71", "cho_bao1 = cho_bao0", 'cho_bao1 = dict(cho_bao0, id=f"{rid}-{ratt}")', "n8_giu_id")
db("d88", "d88", "cho_bao1 = cho_bao0", "cho_bao1 = cho_bao0 if can else None", "n8_giao_lai_gian_doan")
db("d50", "d50", 'pt in ("GET",)', 'pt in ("GET", "POST")', "n8_post_khong_thu_lai")

@ca
def n8_cat_truoc_w5():   # luot 0 dung sau W3 (cat truoc W5): su kien da ben trong cho_bao nen luot sau van giao
    g = dat_than(gh(), nt_cu(T8, 25))
    g.loi(CMU, KeyboardInterrupt(), pt="POST")
    try:
        luot_n(g)
    except KeyboardInterrupt:
        pass
    e = nt_tren(g)["cho_bao"]
    giao(g, luot_n(g, 1)[2], e)

for _loai, _hau, _bo in (("canh_bao", "", "dat"), ("hoi_phuc", "_hoi_phuc", "do"), ("nhip_tim_gian_doan", "_gian_doan", "dat")):
    def _khong_bo(loai=_loai, f=_bo):   # luat thong bao KHONG doi gi o luot 1: su kien dang cho van duoc giao, khong bi xoa
        g, e = nen_cho(loai)
        ma, bc, nk = luot_n(dat_f(g, f), 1)
        giao(g, nk, e)
        mong(bc["thong_bao_hoan"], None, "thong_bao_hoan")
    def _khong_thay(loai=_loai):   # luat thong bao doi bo KHAC o luot 1: van gui su kien cu; su kien moi di o luot lanh ke tiep
        g, e = nen_cho(loai)
        ma, bc, nk = luot_n(dat_f(g, "vang"), 1)
        giao(g, nk, e)
        mong(bc["thong_bao_hoan"], {"loai": "canh_bao", "bo": [ST, viet(F0), "khung_vang"]}, "thong_bao_hoan")
        ma, bc, nk = luot_n(g, 2)
        giao(g, nk, sk(ST, "khung_vang", id=f"{g.rid - 1}-1", cid=None))
    ca(_khong_bo, "n8_cho_bao_khong_bi_bo" + _hau)
    ca(_khong_thay, "n8_cho_bao_khong_bi_thay" + _hau)
db("d89", "d89", "cho_bao1 = cho_bao0", "cho_bao1 = cho_bao0 if not can else _su_kien(rid, ratt, can, C)", "n8_cho_bao_khong_bi_thay")
db("d65", "d65", "C, da_bao1, nt[0])", "C, x0 or da_bao1, nt[0])", "n8_cho_bao_khong_bi_thay")

def nen_mat():
    """Luot 0: `fresh` -> `khung_do`, POST duoc may chu LUU roi phan hoi mat. Tra (g, su kien)."""
    g = dat_than(dat_f(gh(), "do"), nt_cu(T8))
    post_mat(g)
    mong((luot_n(g)[0], len(g.issue[1520]["cm"])), (3, 1), "luot 0")
    return g, nt_tren(g)["cho_bao"]

@ca
def n8_phan_hoi_mat():
    g, e = nen_mat()
    ma, bc, nk = luot_n(g, 1)
    giao(g, nk, e, 0)
    mong((bc["ghi"]["W1"], nt_tren(g)["da_bao"]["comment_id"], len(g.issue[1520]["cm"])), ("da_giao", g.issue[1520]["cm"][0]["id"], 1))
khong("d67", "d67", "n8_phan_hoi_mat")

@ca
def n8_doi_soat_roi_cap_moi():   # W1 (a) xac nhan su kien luot 0 da giao, roi cap va gui NGAY su kien moi cua luot 1
    g, e = nen_mat()
    ma, bc, nk = luot_n(dat_f(g, "vang"), 1)
    giao(g, nk, sk(ST, "khung_vang", id=f"{g.rid - 1}-1", cid=None))
    mong(len(cm_khop(g, e)), 1, "comment khop su kien luot 0")
db("d90", "d90", "if can else None", "if can and not da_giao else None", "n8_doi_soat_roi_cap_moi")

def ca_ghi_hong(ten, sua, muon, f="do", sau=None):
    """Luot 0 voi mot loi ghi tiem boi `sua(g)`: doi (ma thoat, so PATCH, so POST); `sau(g)` kiem luot ke tiep."""
    def chay():
        g = dat_than(dat_f(gh(), f), nt_cu(T8))
        sua(g)
        ma, bc, nk = luot_n(g)
        mong((ma, dem(nk, "PATCH"), dem(nk, "POST"), "trang_thai" in bc), (*muon, True), ten)
        if sau:
            g.sua.clear()
            ma, bc, nk = luot_n(g, 1)
            mong((dem(nk, "POST"), (nt_tren(g)["da_bao"] or {}).get("loai"), nt_tren(g)["cho_bao"]), (0, "canh_bao", None), ten + ": luot sau doi soat thay comment, khong gui lai")
    ca(chay, ten)

def lan_doc(n, **doi):
    """Phan hoi GET Issue thu `n` cua luot (W0 = 1, W3 = 2) bi doi: than them mot ky tu, hoac `state` khac."""
    dk = dem_lan(n)
    return lambda s, pt, url, than: (200, dict({"body": s.issue[1520]["body"], "state": s.issue[1520]["state"]}, **{k: v(s) if callable(v) else v for k, v in doi.items()})) if dk() else None

ca_ghi_hong("n8_patch2_loi", lambda g: g.loi(ISS, (500, {}), pt="PATCH", tu=2), (3, 2, 1), sau=True)
ca_ghi_hong("n8_doc_lai_comment_loi", lambda g: sua_tra(g, r"/issues/comments/\d+", lambda t: t.update(body="khac")), (3, 1, 1), sau=True)
ca_ghi_hong("n8_doc_lai_comment_login", lambda g: sua_tra(g, r"/issues/comments/\d+", lambda t: t["user"].update(login="nguoi-khac")), (3, 1, 1))
ca_ghi_hong("n8_patch_loi_khong_post", lambda g: g.loi(ISS, (403, {}), pt="PATCH"), (3, 1, 0))
ca_ghi_hong("n8_patch_khong_thu_lai", lambda g: g.loi(ISS, (500, {}), pt="PATCH"), (3, 1, 0))
ca_ghi_hong("n8_w0_loi", lambda g: g.loi(ISS, *[(500, {})] * 3), (3, 0, 0))
ca_ghi_hong("n8_doc_lai_than", lambda g: g.sua.append((ISS, "GET", lan_doc(2, body=lambda s: s.issue[1520]["body"] + "x"))), (3, 1, 0))
ca_ghi_hong("n8_state", lambda g: g.sua.append((ISS, "GET", lan_doc(2, state="closed"))), (3, 1, 0), f="dat")
ca_ghi_hong("n8_loi_ghi_fresh", lambda g: g.loi(ISS, *[(500, {})] * 3), (3, 0, 0), f="dat")
khong("d77", "d77", "n8_doc_lai_comment_loi")
khong("d145", "d145", "n8_doc_lai_comment_login")
db("d70", "d70", "if ok and cho_bao1", "if cho_bao1", "n8_patch_loi_khong_post")
db("d51", "d51", 'pt in ("GET",)', 'pt in ("GET", "PATCH")', "n8_patch_khong_thu_lai")
khong("d79", "d79", "n8_w0_loi")
khong("d75", "d75", "n8_doc_lai_than")
khong("d76", "d76", "n8_state")
db("d78", "d78", "3 if loi_ghi else", '3 if loi_ghi and kq["trang_thai"] not in G_TT else', "n8_loi_ghi_fresh")

def ca_doi_soat(ten, chen, so_post, sau=None):
    def chay():
        g, e = nen_cho()
        chen(g, e)
        ma, bc, nk = luot_n(g, 1)
        mong((dem(nk, "POST"), ma), (so_post, 1 if so_post in (0, 1) and bc["ghi"]["W1"] != "doi_soat_khong_tron" else 3), ten)
        if sau:
            sau(g, e, bc, nk)
    ca(chay, ten)

def rac(g, n, luc=None, cid=20000):
    g.issue[1520]["cm"] += [{"id": cid + i, "body": "ghi chu", "user": {"login": "nguoi-khac"}, "created_at": luc or viet(T8), "updated_at": luc or viet(T8)} for i in range(n)]

ca_doi_soat("n8_gia_danh", lambda g, e: chen_cm(g, e, "nguoi-khac"), 1)
ca_doi_soat("n8_gia_danh_doi_chung", lambda g, e: chen_cm(g, e), 0)
ca_doi_soat("n8_hai_dong_su_kien", lambda g, e: chen_cm(g, e, them="\n" + M.TT_SK + "{}"), 1)
ca_doi_soat("n8_hai_comment_khop", lambda g, e: (chen_cm(g, e, cid=9002), chen_cm(g, e, cid=9001)), 0, lambda g, e, bc, nk: mong(nt_tren(g)["da_bao"]["comment_id"], 9001, "comment_id nho nhat"))
ca_doi_soat("n8_doi_soat_khong_tron", lambda g, e: (rac(g, 11), setattr(g, "trang", 1)), 0,
            lambda g, e, bc, nk: mong((bc["ghi"]["W1"], nt_tren(g)["cho_bao"], dem(nk, "GET", r"/comments\?since")), ("doi_soat_khong_tron", e, 10), "khoa gui"))
ca_doi_soat("n8_doi_soat_cua_so", lambda g, e: (rac(g, 1500, "2026-12-01T00:00:00Z"), chen_cm(g, e)), 0,
            lambda g, e, bc, nk: mong(([x["url"] for x in nk if "/comments?" in x["url"]], nt_tren(g)["da_bao"]["comment_id"]),
                                      ([f"{M.API}/issues/1520/comments?since={viet(F0 - TD(hours=24))}&per_page=100"], 9001), "D14 mot trang trong cua so cua su kien"))
ca_doi_soat("n8_doi_soat_bien", lambda g, e: rac(g, 1000), 1, lambda g, e, bc, nk: mong(dem(nk, "GET", r"/comments\?since"), 10, "dung 1000 comment trong cua so: tron"))
khong("d68", "d68", "n8_gia_danh")
db("d143", "d143", "len(dong) != 1", "not dong", "n8_hai_dong_su_kien")
db("d144", "d144", "min(khop)", "max(khop)", "n8_hai_comment_khop")
db("d91", "d91", "?since={cua_so}&per_page=100", "?per_page=100", "n8_doi_soat_cua_so")

@ca
def n8_doi_soat_bien_tren():   # 1 001 comment trong cua so: khoa gui; bot 2 comment thi khoa tu go, gui lai CUNG id
    g, e = nen_cho()
    rac(g, 1001)
    ma, bc, nk = luot_n(g, 1)
    mong((dem(nk, "POST"), ma, bc["ghi"]["W1"], nt_tren(g)["cho_bao"]), (0, 3, "doi_soat_khong_tron", e))
    del g.issue[1520]["cm"][:2]
    giao(g, luot_n(g, 2)[2], e)
khong("d93", "d93", "n8_doi_soat_bien_tren", "n4_s1_khong_tron")   # bo phan trang dung chung: ca D14 lan D1

@ca
def n8_doi_soat_lech_dong_ho():   # may chu dong dau som hon dong ho runner 3 gio: comment van nam sau cua_so = khung - 24 h
    g = gh(f="vang")
    g.lech_gio = -3
    post_mat(g)
    luot_wd(g, F0)
    e = nt_tren(g)["cho_bao"]
    ma, bc, nk = luot_wd(g, F0 + TD(hours=6))
    giao(g, nk, e, 0)
    mong((e["khung"], g.issue[1520]["cm"][0]["updated_at"]), (viet(F0), viet(F0 - TD(hours=3))))
db("d92", "d92", " - LE_DOI_SOAT", "", "n8_doi_soat_lech_dong_ho")

@ca
def n10_i7_van_ban_sinh_ra():   # I7 tren moi van ban do watchdog SINH RA (bao cao, than Issue, comment); mau dung tu cac manh chu
    m = ("skip", "ci", "no", "actions", "-checks")
    mau = re.compile("|".join([rf"\[{a}[ _-]{b}\]" for a, b in ((m[0], m[1]), (m[1], m[0]), (m[2], m[1]), (m[0], m[3]), (m[3], m[0]))] + [m[0] + m[4]]), re.I)
    for f in ("dat", "do", "vang"):
        g = dat_f(gh(), f)
        ma, bc, nk = luot_n(g)
        bang(len(g.issue[1520]["cm"]) == 1 and not mau.search(van_ban(g, bc)), f"van ban sinh ra ({f}) chua dau bo-qua-CI hoac thieu comment")

# ---- Nghiem thu 9: ma thoat va cau hinh ----
def cau_hinh(env=None, **kw):
    g = gh()
    ma, bc, nk = luot_wd(g, env=dict({"GH_TOKEN": "tok-gia", "B2_RUN_ID": "77", "B2_RUN_ATTEMPT": "1"}, **(env or {})), **kw)
    return ma, len(nk), g

def ca_ma_2(ten, **kw):
    ca(lambda: mong(cau_hinh(**kw)[:2], (2, 0), ten), ten)

ca_ma_2("n9_token_rong", env={"GH_TOKEN": ""})
ca_ma_2("n9_issue", issue=0)
ca_ma_2("n9_issue_none", issue=None)
ca_ma_2("n9_issue_am", issue=-5)
ca_ma_2("n9_issue_bool", issue=True)
ca_ma_2("n9_run_id_so_0", env={"B2_RUN_ID": "0123"})
ca_ma_2("n9_run_id_khong_phai_so", env={"B2_RUN_ID": "abc"})
khong("d80", "d80", "n9_token_rong")
khong("d147", "d147", "n9_issue")
db("d148", "d148", '"[1-9][0-9]*"', '"[0-9]+"', "n9_run_id_so_0")

@ca
def n9_run_id_bien():
    mong((cau_hinh(env={"B2_RUN_ID": str(10**20)})[:2], cau_hinh(env={"B2_RUN_ATTEMPT": str(10**10)})[:2]), ((2, 0), (2, 0)), "ngoai mien")
    ma, n, g = cau_hinh(env={"B2_RUN_ID": str(10**20 - 1), "B2_RUN_ATTEMPT": str(10**10 - 1)})
    mong((ma, nt_tren(g)["da_bao"]["id"], bool(M.RE_ID_SK.fullmatch(nt_tren(g)["da_bao"]["id"]))), (0, f"{10**20 - 1}-{10**10 - 1}", True), "bien tren cua mien")
db("d97", "d97", "10**20 - 1", "10**30", "n9_run_id_bien")
db("d98", "d98", "10**10 - 1", "10**30", "n9_run_id_bien")

@ca
def n9_ma_thoat():
    mong([mot(f=f)[1] for f in ("dat", "do")] + [mot(lambda g, lu: g.loi(ISS, *[(500, {})] * 3))[1], cau_hinh(issue=0)[0]], [0, 1, 3, 2])

@ca
def n9_i3():   # khong bien moi truong nao doi kho, so Issue hay KHUNG_DAU
    g = gh()
    ma, bc, nk = luot_wd(g, env={"GH_TOKEN": "tok-gia", "B2_RUN_ID": "77", "B2_RUN_ATTEMPT": "1", "GITHUB_API_URL": "https://evil.example", "GITHUB_REPOSITORY": "a/b",
                                 "GH_REPO": "a/b", "B2_ISSUE": "1521", "B2_KHUNG_DAU": "2020-01-04T19:17:00Z"})
    mong((S(bc), [x["url"] for x in nk if not x["url"].startswith((M.API + "/", LUU))], dem(nk, "GET", r"/issues/1521")), (XANH, [], 0))
db("d81", "d81", 'or ""', 'or ""; issue = int(moi_truong.get("B2_ISSUE", issue))', "n9_i3")

# ---- Nghiem thu 15: ngan sach va thu tu ----
DG = r"/actions/|/contents/|/git/commits/|luu-tru"

@ca
def n15_thu_tu_goi():   # cung mot D1 o hai thu tu API va o hai trang, bang chung liet ke o hai thu tu => CHUOI loi goi giong het
    def chuoi(dao, trang):
        g = gh()
        them(g, 21, F0, "dat", sha="a" * 40)
        if dao:
            g.thu_tu, g.luot[20]["arts"] = g.thu_tu[::-1], g.luot[20]["arts"][::-1]
            g.luot[20]["bn"]["job"].reverse()
            g.luot[20]["bn"]["manh"].reverse()
            g.goi[g.luot[20]["idb"]] = zip_cua([("bien_nhan_audit.json", bn_byte(g.luot[20]))])
            next(a for a in g.luot[20]["arts"] if a["id"] == g.luot[20]["idb"])["digest"] = "sha256:" + sha256(g.goi[g.luot[20]["idb"]])
        g.trang = trang
        return [x["url"] for x in luot_wd(g)[2] if re.search(DG, x["url"]) and not re.search(D1U, x["url"])]
    goc = chuoi(False, 100)
    bang(len(goc) > 100 and goc == chuoi(True, 100) == chuoi(True, 2), "chuoi loi goi phai khong phu thuoc thu tu API")
db("d11", "d11", 'sorted((r for r in d1 if kc[r["id"]] in xet), key=lambda r: r["id"])', '[r for r in d1 if kc[r["id"]] in xet]', "n15_thu_tu_goi")
db("d12", "d12", "sorted(set(neu))", "list(dict.fromkeys(neu))", "n15_thu_tu_goi")

def nen_can(dao=False, cham=29, **nt):
    """F co luot dat id 20 (nhanh) va luot dat id 21 ma moi GET tieu `cham` giay: TONG vuot NGAN_SACH_DANH_GIA. Khong su kien nao can gui."""
    g = dat_than(gh(), nt_cu(T0, da_bao=sk(KDD, "het_ngan_sach_danh_gia"), **nt))
    them(g, 21, F0, "dat", sha="a" * 40)
    g.tre.append((r"/runs/21|/artifacts/2100\d+|goi/2100\d+", cham))
    g.thu_tu = g.thu_tu[::-1] if dao else g.thu_tu
    return g

@ca
def n15_can_ngan_sach():
    for dao in (False, True):
        g = nen_can(dao)
        ma, bc, nk = luot_wd(g)
        mong((S(bc), bc["sha_audit"], bc["dong_den"] == bc["dong_den_truoc"], dem(nk, "PATCH")), ((KDD, "het_ngan_sach_danh_gia"), None, True, 1), f"dao={dao}")
    mong(S(luot_wd(nen_can(cham=0))[1]), XANH, "doi chung ngan sach du")
db("d13", "d13", '_phan_luot(c, r, V, kc[r["id"]])', '(_phan_luot(c, r, V, kc[r["id"]]) if not any(luot[x]["phan_quyet"] == DAT and kc[x] == kc[r["id"]] for x in luot) else {"id": r["id"], "phan_quyet": "dang_chay", "ma": "bo_qua", "phep": {}, "head_sha": r["head_sha"], "khung": "", "moc_tuoi": None})', "n15_can_ngan_sach")
khong("d14", "d14", "n15_can_ngan_sach")

@ca
def n15_ngan_sach_ghi():   # can ngan sach danh gia khong lam mat W2: ngan sach ghi rieng
    ma, bc, nk = luot_wd(nen_can())
    mong((bc["ma_ly_do"], dem(nk, "PATCH"), bc["ghi"]["W3"]), ("het_ngan_sach_danh_gia", 1, "dat"))
db("d15", "d15", "c.dong_ho() + NGAN_SACH_GHI - w0_dung", "c.han", "n15_ngan_sach_ghi")

@ca
def n15_can_ngan_sach_dong_den():   # luot dat cua P (id nho nhat) da danh gia xong truoc khi can: dong_den van KHONG tien
    g = nen_can(dong_den=viet(w(1)))
    ma, bc, nk = luot_wd(g)
    mong((bc["ma_ly_do"], bc["dong_den"], nt_tren(g)["dong_den"], lu_bc(bc, 10).get("phan_quyet")), ("het_ngan_sach_danh_gia", viet(w(1)), viet(w(1)), "dat"))
db("d140", "d140", "dong_den=viet(dong_den0), ", "", "n15_can_ngan_sach_dong_den")

@ca
def n15_khong_goi_sau_han():
    ma, bc, nk = luot_wd(nen_can())
    mong(([x["t"] for x in nk if re.search(DG, x["url"]) and x["t"] >= 600], bc["ma_ly_do"]), ([], "het_ngan_sach_danh_gia"))
khong("d105", "d105", "n15_khong_goi_sau_han")

def nen_han(can, moc=599.0, ma_t7=None):
    """F co luot A (id 20) dat va luot B (id 21, khong bien nhan). Dong ho nhay toi `moc` ngay truoc T7 cua B (luc phan tich xong D4 cua B); D2 cua B can `can` giay."""
    g = dat_than(gh(), nt_cu(T0))
    them(g, 21, F0, "do", sha="a" * 40)
    g.tre.append((r"/actions/runs/21$", can))
    g.nhay_json.append((lambda x: isinstance(x, dict) and any("-21-" in a["name"] for a in x.get("artifacts") or []), moc))   # sau khi doc xong D4 cua B
    if ma_t7:
        g.loi(r"/actions/runs/21$", (ma_t7, {}), tu=2)
    return g

@ca
def n15_han_cuoi_danh_gia():   # T7 cua B bat dau o 599 s: can 2 s => timeout kep 1, het gio o 600 s => S1; 0,5 s => fresh; dung 1 s => S1
    for can, muon in ((2, (KDD, "het_ngan_sach_danh_gia")), (0.5, XANH), (1, (KDD, "het_ngan_sach_danh_gia"))):
        g = nen_han(can)
        ma, bc, nk = luot_wd(g)
        mong((S(bc), [x["timeout"] for x in nk if re.search(r"/runs/21$", x["url"])][-1], bc["sha_audit"]), (muon, 1.0, "a" * 40 if muon == XANH else None), f"may chu can {can} s")

@ca
def n15_phan_tich_qua_han():   # phep phan tich CUOI cua pha danh gia vuot han, sau no khong con lan thu hay lan cho nao => chi kiem luc HOAN TAT bat duoc
    g = nen_han(0.5)
    dk = dem_lan(2)
    def boc(goc):
        def f(byte):
            x = goc(byte)
            if isinstance(x, dict) and x.get("id") == 21 and "run_attempt" in x and dk():
                g.t = 601.0
            return x
        return f
    with thay_ten("_tho_json", boc):
        ma, bc, nk = luot_wd(g)
    mong((S(bc), bc["sha_audit"], max(x["t"] for x in nk if re.search(DG, x["url"])) < 600), ((KDD, "het_ngan_sach_danh_gia"), None, True))
khong("d99", "d99", "n15_phan_tich_qua_han", "n15_tinh_cuoi_qua_han")

@ca
def n15_kep_timeout():
    ma, bc, nk = luot_wd(nen_han(0.5, moc=595.0))
    mong([x["timeout"] for x in nk if re.search(r"/runs/21$", x["url"])], [30, 5.0])
db("d100", "d100", "min(HAN_GOI, con)", "HAN_GOI", "n15_kep_timeout")

@ca
def n15_cho_qua_han():   # GET 500 khi con 0,5 s: khong cho, khong thu lai, ham ngu khong duoc goi
    g = nen_han(0, moc=599.5, ma_t7=500)
    ma, bc, nk = luot_wd(g)
    mong((g.ngu_nk, dem(nk, "GET", r"/runs/21$"), S(bc)), ([], 2, (KDD, "het_ngan_sach_danh_gia")))
khong("d104", "d104", "n15_cho_qua_han")

def nen_w8(can):
    """S `khung_do` can `canh_bao`, giao xong; W8 (GET Issue thu ba) bat dau khi HAN_GHI con 1 s; moi GET Issue can `can` giay."""
    g = dat_than(dat_f(gh(), "do"), nt_cu(T8))
    g.tre.append((ISS, can))
    dk = dem_lan(4)   # than Issue duoc phan tich lan thu tu = phan hoi PATCH cua W7
    g.nhay_json.append((lambda x: isinstance(x, dict) and set(x) == {"body", "state"} and dk(), 179.0))
    return g

@ca
def n15_han_cuoi_ghi():   # W8 thanh cong ve transport (xong o 179,5 s) nhung phep phan tich sau no vuot HAN_GHI => chi kiem luc hoan tat bat duoc
    for nhay, ma_mong in ((True, 3), (False, 1)):
        g, dk = nen_w8(0.5), dem_lan(5)   # than Issue duoc phan tich nam lan: W0, W2 (PATCH), W3, W7 (PATCH), W8
        def boc(goc):
            def f(byte):
                x = goc(byte)
                if isinstance(x, dict) and set(x) == {"body", "state"} and dk() and nhay:
                    g.t = 181.0
                return x
            return f
        with thay_ten("_tho_json", boc):
            ma, bc, nk = luot_n(g)
        mong((ma, dem(nk, "PATCH"), dem(nk, "POST"), [x["t"] for x in nk if x["pt"] == "GET" and re.search(ISS, x["url"])][-1]), (ma_mong, 2, 1, 179.0), f"nhay={nhay}")
        mong((dem(luot_n(g, 1)[2], "POST"), nt_tren(g)["da_bao"]["loai"]), (0, "canh_bao"), "luot sau doc nhip tim co da_bao = su kien")
khong("d106", "d106", "n15_han_cuoi_ghi")

@ca
def n15_han_cuoi_ghi_het_gio():   # W8 bat dau khi con 1 s, may chu can 2 s => timeout 1, W8 het gio => ma 3
    g = nen_w8(2)
    ma, bc, nk = luot_n(g)
    mong((ma, [x["timeout"] for x in nk if x["pt"] == "GET" and re.search(ISS, x["url"])][-1], bc["ghi"]["W8"]), (3, 1.0, "doc_lai_loi:het_gio"))

# ---- Sau review ma luot 1. F01 `rest-response-domain-incomplete`: MOT bo kiem mien o bien cho moi hinh REST duoc tieu dung ----
def ca_t1_mien(ten, sua, muon=(KDD, "rest_sai_hinh")):
    def chay():
        g, ma, bc, nk = mot(lambda g, lu: sua(lu))
        mong((phep(bc, 20, "T1"), S(bc)[0] == "fresh"), (muon, muon[0] == "dat"), ten)
    ca(chay, ten)

def art_thua(lu, **kw): lu["arts"].append(dict({"id": 90909090, "name": "khong-duoc-chon", "expired": False, "digest": None}, **kw))

K1 = (("run_so", lambda lu: lu["d2"].update(workflow_id="7")), ("run_attempt", lambda lu: lu["d2"].update(run_attempt=0)), ("run_conclusion", lambda lu: lu["d2"].update(conclusion=1)),
      ("run_chuoi", lambda lu: lu["d2"].update(status=5)), ("job_attempt", lambda lu: lu["jobs"][0].update(run_attempt=0)), ("job_conclusion", lambda lu: lu["jobs"][0].update(conclusion=1)),
      ("job_chuoi", lambda lu: lu["jobs"][0].update(name=5)), ("art_digest", lambda lu: art_thua(lu, digest=7)), ("art_khac", lambda lu: art_thua(lu, expired="no")))
for _t, _s in K1:
    ca_t1_mien("n1_t1_mien_" + _t, _s)
    xoa("f01_k1_" + _t, "k1:" + _t, "n1_t1_mien_" + _t)
ca_t1_mien("n1_t1_mien_job_attempt_am", lambda lu: lu["jobs"][2].update(run_attempt=-1))
ca_t1_mien("n1_t1_mien_run_attempt_bool", lambda lu: lu["d2"].update(run_attempt=True))
ca_t1_mien("n1_t1_mien_doi_chung", lambda lu: art_thua(lu), ("dat", "dat"))   # `digest: null` duoc K1 cho phep; `conclusion: null` cua luot dang chay: n1_chua_xong

def ca_thieu_body(ten, lan, muon):
    def chay():   # Issue THIEU khoa `body` (khac `body: null`) o lan doc thu `lan` cua luot: loi doc Issue vao luong loi ghi, van co bao cao
        g = dat_than(dat_f(gh(), "do"), nt_cu(T8))
        g.loi(ISS, (200, {"state": "open"}), tu=lan)
        try:
            ma, bc, nk = luot_n(g)
        except KeyError as e:
            bang(False, f"KeyError {e} lan khoi ham chinh, khong co bao cao")
        mong((ma, dem(nk, "PATCH"), dem(nk, "POST"), bc["trang_thai"]), (3, *muon, ST), ten)
    ca(chay, ten)

ca_thieu_body("n8_issue_thieu_body_w0", 1, (0, 0))
ca_thieu_body("n8_issue_thieu_body_w3", 2, (1, 0))
ca_thieu_body("n8_issue_thieu_body_w8", 3, (2, 1))
db("f01_issue_body", "f01:body", '"body" in v and isinstance(v["body"]', 'isinstance(v.get("body")', "n8_issue_thieu_body_w0", "n8_issue_thieu_body_w3", "n8_issue_thieu_body_w8")

@ca
def n8_issue_body_null():   # doi chung: `body: null` la Issue rong hop le => nhip tim `vang`, luot van ghi
    g = gh()
    g.issue[1520]["body"] = None
    ma, bc, nk = luot_n(g)
    mong((bc["nhip_tim_truoc"]["trang_thai"], ma, dem(nk, "PATCH")), ("vang", 0, 2))

# ---- F02 `bounded-evaluation-order-dependent`: han tuyet doi phu MOI duong ket thuc pha ----
def nhay(g, moc=None, them=0.0, lan=1):
    """Ham boc: o lan goi thu `lan`, dong ho gia nhay toi `moc` (hoac tien `them` giay) roi moi goi nguyen ban."""
    dk = dem_lan(lan)
    def boc(goc):
        def f(*a, **k):
            if dk():
                g.t = max(g.t, moc) if moc is not None else g.t + them
            return goc(*a, **k)
        return f
    return boc

@ca
def n15_tinh_cuoi_qua_han():   # phep tinh CUOI cua pha danh gia (nghia vu O) hoan tat o 599,5 / 600 / 600,5 s: bang han la da het
    for moc, muon in ((599.5, (XANH, "a" * 40)), (600.0, ((KDD, "het_ngan_sach_danh_gia"), None)), (600.5, ((KDD, "het_ngan_sach_danh_gia"), None))):
        g = gh()
        with thay_ten("_da_dong", nhay(g, moc)):
            ma, bc, nk = luot_wd(g)
        mong((S(bc), bc["sha_audit"], bc["dong_den"] == bc["dong_den_truoc"] or muon[0] == XANH), (*muon, True), f"phep tinh cuoi xong o {moc} s")

@ca
def n15_w0_phan_tich_qua_han():   # TOAN BO W0 (ca phan tich va kiem mien nhip tim) tinh vao HAN_W0
    for them, muon in ((181.0, ("d10_loi:het_gio", 0, 3)), (100.0, ("moi", 1, 0))):
        g = dat_than(gh(), nt_cu(T0))
        with thay_ten("kiem_nhip_tim", nhay(g, them=them)):
            ma, bc, nk = luot_wd(g)
        mong((bc["nhip_tim_truoc"]["ma"], dem(nk, "PATCH"), ma), muon, f"kiem mien nhip tim tieu {them} s")
khong("f02_w0_tron_ven", "w0:tron_ven", "n15_w0_phan_tich_qua_han")

@ca
def n15_w0_tinh_ca_phan_tich():   # thoi gian phan tich o W0 bi TRU khoi ngan sach ghi con lai: W0 dung 170 s => lan gui dau cua pha ghi con 10 s
    g = dat_than(gh(), nt_cu(T0))
    with thay_ten("kiem_nhip_tim", nhay(g, them=170.0)):
        ma, bc, nk = luot_wd(g)
    mong(([x["timeout"] for x in nk if "/git/ref/heads/master" in x["url"]], ma), ([10.0], 0))
db("f02_w0_dung", "w0:dung", "c.dong_ho() - t0", "0.0", "n15_w0_tinh_ca_phan_tich")

class LuongCham:
    """Luong than ma MOI lan `read` tieu `giay` giay don dieu (moi lan deu duoi timeout cua socket)."""
    def __init__(self, g, byte, giay): self.g, self.khuc, self.giay = g, [byte[:10], byte[10:20], byte[20:], b""], giay
    def read(self, n=-1):
        self.g.t += self.giay
        return self.khuc.pop(0) if self.khuc else b""

@ca
def n15_vong_doc_qua_han():   # ba khuc x 20 s: tung lan doc duoi 30 s nhung TONG vuot han cua lan thu => lan thu khong hoan tat
    for giay, muon in ((20, (KDD, "transport_nem:builtins.TimeoutError", 3)), (5, ("fresh", "khung_xanh", 1))):
        g = gh()
        g.sua.append((D1U, "GET", lambda s, pt, url, than: (200, LuongCham(s, json.dumps(s.xu_ly(pt, url, than)[1]).encode(), giay))))
        ma, bc, nk = luot_wd(g)
        mong((bc["trang_thai"], bc["ma_chi_tiet"], dem(nk, "GET", D1U)), muon, f"moi lan doc {giay} s")
khong("f02_vong_doc", "f02:vong_doc", "n15_vong_doc_qua_han")

@ca
def n15_d14_khop_qua_han():   # D14: kiem luc hoan tat dung SAU phep khop comment
    g, e = nen_cho()
    chen_cm(g, e)
    with thay_ten("_khop", nhay(g, them=500.0)):
        ma, bc, nk = luot_n(g, 1)
    mong((dem(nk, "POST"), ma, bc["ghi"]["W1"], nt_tren(g)["cho_bao"]), (0, 3, "doi_soat_loi:het_gio", e))
khong("f02_d14", "f02:d14", "n15_d14_khop_qua_han")

# ---- F03 `mutant-oracles-non-discriminating`: tung truong D2/U6 rieng; adapter that va main ----
for _f, _gt in LK:
    def _lk_cuoi(f=_f, gt=_gt):
        g, ma, bc, nk = mot(lambda g, lu: lech_d2(lu, f, gt, cuoi=True))
        mong((phep(bc, 20, "T7"), phep(bc, 20, "T1")[0], lu_bc(bc, 20)["ma"]), ((KDD, "lien_ket_lech:" + f), "dat", "lien_ket_lech:" + f), f)
    ca(_lk_cuoi, "n1_lien_ket_cuoi_" + _f)
tho("r27_t7_bo_event", "lech = _lech_lien_ket(d1, cuoi)  # d03",
    'lech = next((f"lien_ket_lech:{f}" for f in LIEN_KET if f != "event" and _lay(d1, f) != _lay(cuoi, f)), None)  # d03', "n1_lien_ket_cuoi_event")
U6 = '("run_attempt", "status", "conclusion", "updated_at"))'
for _f, _gt in (("run_attempt", 2), ("status", "queued"), ("conclusion", "failure"), ("updated_at", "2026-12-12T23:00:00Z")):
    def _u6(f=_f, gt=_gt):
        g, ma, bc, nk = mot(lambda g, lu: lech_d2(lu, f, gt, cuoi=True))
        mong((phep(bc, 20, "T7"), lu_bc(bc, 20)["phan_quyet"]), ((KDD, "luot_doi_giua_chung"), KDD), f)
    ca(_u6, "n1_u6_" + _f)
    tho("r28_u6_bo_" + _f, U6, U6.replace(f'"{_f}", ', "").replace(f', "{_f}"', ""), "n1_u6_" + _f)

@ca
def n1_j_doc_theo_khuc():   # than vo tan: phai dung o byte thu TRAN_GOI + 1, khong bao gio goi `read()` khong kich thuoc
    class VoTan:
        da, vo_han = 0, False
        def read(self, n=-1):
            VoTan.vo_han |= n is None or n < 0
            VoTan.da += max(n or 0, 0) if n and n > 0 else 10**6
            return b"x" * (n if n and n > 0 else 10**6)
    g = gh()
    g.sua.append((D1U, "GET", lambda *a: (200, VoTan())))
    ma, bc, nk = luot_wd(g, tran={"TRAN_GOI": 1000})
    mong((VoTan.vo_han, VoTan.da <= 1001, bc["ma_chi_tiet"]), (False, True, "than_vuot_tran"))
tho("r22_doc_khong_theo_khuc", 'b = luong.read(min(65536, c.tran["TRAN_GOI"] + 1 - n))', "b = luong.read()", "n1_j_doc_theo_khuc", "n1_j_vuot_tran", "n1_s_vuot_tran")

class PhanHoiGia:
    def __init__(self, ma, hd, byte): self.status, self.headers, self.than = ma, hd, io.BytesIO(byte)
    def read(self, n=-1): return self.than.read(n)

@ca
def n16_transport_that():   # adapter urllib THAT qua lop mo gia (khong mang): timeout di toi `open`, KHONG tu theo chuyen huong, HTTPError thanh phan hoi
    goi = []
    def mo_gia(*lop):
        class Mo:
            def open(self, req, timeout=None):
                goi.append((req.get_method(), req.full_url, dict(req.header_items()), req.data, timeout))
                if "chuyen" in req.full_url:   # nhu urllib: handler chuyen huong tra None => HTTPError 302; tra Request => tu theo
                    theo = [h().redirect_request(req, None, 302, "Found", {}, "https://luu-tru.example/dich") for h in lop] or [object()]
                    if all(x is None for x in theo):
                        raise urllib.error.HTTPError(req.full_url, 302, "Found", {"Location": "https://luu-tru.example/dich", "X-GitHub-Request-Id": "g"}, io.BytesIO(b""))
                    return PhanHoiGia(200, {}, b"da tu theo chuyen huong")
                if "khong-co" in req.full_url:
                    raise urllib.error.HTTPError(req.full_url, 404, "Not Found", {"X-GitHub-Request-Id": "g"}, io.BytesIO(b'{"message": "Not Found"}'))
                return PhanHoiGia(200, {"X-GitHub-Request-Id": "g"}, b'{"ok": true}')
        return Mo()
    cu, urllib.request.build_opener = urllib.request.build_opener, mo_gia
    try:
        ma, hd, luong = M.transport_that("PATCH", "https://api.github.com/x", {"Authorization": "Bearer t"}, {"body": "b"}, 7)
        mong((ma, hd, luong.read(4), goi[0][0], goi[0][3], goi[0][4], goi[0][2].get("Authorization")), (200, {"X-GitHub-Request-Id": "g"}, b'{"ok', "PATCH", b'{"body": "b"}', 7, "Bearer t"), "200")
        ma, hd, luong = M.transport_that("GET", "https://api.github.com/chuyen", {}, None, 3.5)
        mong((ma, hd.get("Location"), goi[1][3], goi[1][4]), (302, "https://luu-tru.example/dich", None, 3.5), "302 khong duoc tu theo")
        ma, hd, luong = M.transport_that("GET", "https://api.github.com/khong-co", {}, None, 30)
        mong((ma, luong.read(), goi[2][4]), (404, b'{"message": "Not Found"}', 30), "HTTPError thanh phan hoi")
    finally:
        urllib.request.build_opener = cu
tho("r23_tu_theo_chuyen_huong", "def redirect_request(self, *a, **k):\n        return None", "def redirect_request(self, *a, **k):\n        return super().redirect_request(*a, **k)", "n16_transport_that")
tho("r25_bo_timeout_adapter", ".open(req, timeout=timeout)", ".open(req, timeout=None)", "n16_transport_that")

@ca
def n9_main_ma_thoat():   # main(): ma thoat cua muc 9 di nguyen ven ra tien trinh; bao cao MOT dong JSON ASCII sort_keys; tom tat khi co GITHUB_STEP_SUMMARY
    tom_tat = Path(tempfile.mkdtemp(prefix="cta_tt_")) / "tom_tat.md"
    cu = os.environ.get("GITHUB_STEP_SUMMARY")
    os.environ["GITHUB_STEP_SUMMARY"] = str(tom_tat)
    try:
        for ma_mong in (0, 1, 2, 3):
            bc = {"loi": "gh_token_rong"} if ma_mong == 2 else {"trang_thai": "fresh", "ma_chi_tiet": "khung_xanh", "cau_master": "câu về master", "ghi": {"W0": "moi"}}
            nhan, ra = [], io.StringIO()
            with thay_ten("chay", lambda goc: lambda *a, **k: (nhan.append((a, k)), (ma_mong, bc))[1]), contextlib.redirect_stdout(ra):
                ma = M.main()
            mong((ma, ra.getvalue(), nhan[0][0][0] is os.environ, nhan[0][0][1] is M.transport_that, nhan[0][0][2], nhan[0][1]),
                 (ma_mong, json.dumps(bc, ensure_ascii=True, sort_keys=True) + "\n", True, True, os.path.dirname(os.path.dirname(os.path.abspath(M.__file__))), {}), f"ma {ma_mong}")
        mong(tom_tat.read_text(encoding="utf-8").count("câu về master"), 3, "tom tat ghi cho ba luot co trang_thai, bo qua luot cau hinh sai")
    finally:
        os.environ.pop("GITHUB_STEP_SUMMARY") if cu is None else os.environ.update(GITHUB_STEP_SUMMARY=cu)
tho("r24_main_luon_0", "    return ma\n\nif __name__", "    return 0\n\nif __name__", "n9_main_ma_thoat")

# ---- Nghiem thu 11: bon ca tu kiem bo phan hang (doi tuong thu la `_TK`) ----
_TK = {"nguong": 3, "ten": "abc"}

@ca
def tk_chot():
    bang(_TK["nguong"] == 3, "nguong phai la 3")

@ca
def tk_doi_kieu():   # mot `except` doi kieu DUNG LEN AssertionError: khong duoc tinh la tin hieu chot
    try:
        _TK["ten"].upper()
    except Exception as e:
        raise AssertionError(f"doi kieu tu {type(e).__name__}")

@ca
def tk_ca_khac():
    CA["tk_chot"]()

HONG_M = "(lambda *a: None)"
DOT_BIEN = [   # (ten, tep: T = tep test nay · M = mo-dun, chuoi neo — DUNG MOT lan trong tep goc, chuoi thay, cac ca dich). Dong 82 (x18):
    (f"d82_{i:02d}_{dich}", "T", f'doi("m{i:02d}",', f'{HONG_M}("m{i:02d}",', (dich,)) for i, dich in enumerate((
        "n10_khoa_workflow", "n10_on", "n10_quyen", "n10_concurrency", "n10_tap_job", "n10_khoa_job", "n10_runs_on", "n10_timeout", "n10_so_buoc",
        "n10_buoc1_if", "n10_buoc2_if", "n10_buoc3_if", "n10_buoc4_if", "n10_buoc1_gia_tri", "n10_buoc2_gia_tri", "n10_buoc3_gia_tri",
        "n10_buoc4_gia_tri", "n10_dem_bieu_thuc"), 1)] + [   # hai ve con cua menh de (1) ma dong 82 khong tach rieng (executor them):
    ("d82_01b_gia_tri_name", "T", ' or _lech(wf["name"]' + ', MONG_WF["name"], "name")', "", ("n10_ten",)),
    ("d82_01c_hai_khoa_on", "T", " or [k for k in co" + " if co.count(k) > 1]", "", ("n10_hai_khoa_on",))]
TU_KIEM = (   # (ten, chuoi neo, chuoi thay, ca dich, hang MONG)
    ("tk_giet_that", '"nguong"' + ": 3", '"nguong"' + ": 4", "tk_chot", "GIET"),
    ("tk_attribute_error_qua_except", '"ten"' + ': "abc"', '"ten"' + ": None", "tk_doi_kieu", "TIN_DUNG_GIA"),
    ("tk_assertion_cua_ca_khac", '"nguong"' + ": 3", '"nguong"' + ": 4", "tk_ca_khac", "TIN_DUNG_GIA"),
    ("tk_song", '"ten"' + ': "abc"', '"ten"' + ': "abd"', "tk_chot", "SONG"),
    # tu kiem thu nam: dot bien TUONG DUONG (viii) da khai cua dac ta (bo ve KHUNG_DAU - 7 ngay khoi can duoi cua R) phai ra SONG
    ("tk_tuong_duong_viii", "max(dong_den0, khung_dau" + " - BAY_NGAY)", "dong_den0", "n4_r_khung_cu", "SONG", "M"),
)

def chay_ca(ten):
    """(rc, dong): 0 dat · 3 `DO:<ca>:` (chi `TinHieuChotCa` mang DUNG ten ca nay) · 4 loi vo can hoac tin hieu cua ca KHAC."""
    _SO_LUOT.clear()
    try:
        CA[ten]()
        hau_kiem()
    except TinHieuChotCa as e:
        return (3, f"DO:{ten}:{e}") if e.ca == ten else (4, f"HONG:{ten}:tin hieu chot cua ca khac {e.ca}: {e}")
    except Exception as e:
        return 4, f"HONG:{ten}:{type(e).__name__}: {e}"
    return 0, ""

def chay_con(tep_test, ten_ca, mo_dun):
    r = subprocess.run([sys.executable, "-B", str(tep_test), "--mot-ca", ten_ca, str(ROOT), str(mo_dun)], capture_output=True, timeout=300,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    return r.returncode, (r.stdout + r.stderr).decode("utf-8", "replace").strip()

def phan_hang(rc, ra, ten_ca):
    return "SONG" if rc == 0 else "GIET" if rc == 3 and f"DO:{ten_ca}:" in ra else "TIN_DUNG_GIA"

_NEN = {}

def chay_dot_bien(ten, tep, neo, thay, cac_ca):
    """(hang, chi tiet). GIET <=> ca dich DAT tren goc va MOI ca dich chet boi `TinHieuChotCa` cua chinh no tren ban sao dot bien."""
    nguon = TEP_TEST if tep == "T" else TEP_MO_DUN
    goc = nguon.read_text(encoding="utf-8")
    if goc.count(neo) != 1 or neo == thay or not set(cac_ca) <= set(CA) or not cac_ca:
        return "HONG", f"neo phai xuat hien DUNG MOT lan (thay {goc.count(neo)}), dot bien phai doi ma, ca dich phai co that"
    hang, chi_tiet = [], []
    with tempfile.TemporaryDirectory(prefix="cta_db_") as thu:
        ban = Path(thu) / f"db_{ten}.py"
        ban.write_text(goc.replace(neo, thay), encoding="utf-8")
        for c in cac_ca:
            if c not in _NEN:
                _NEN[c] = chay_con(TEP_TEST, c, TEP_MO_DUN)
            if _NEN[c][0] != 0:
                return "HONG", f"ca dich {c} khong DAT tren ban goc: {_NEN[c][1][-200:]}"
            rc, ra = chay_con(ban if tep == "T" else TEP_TEST, c, ban if tep == "M" else TEP_MO_DUN)
            hang.append(phan_hang(rc, ra, c))
            chi_tiet.append(f"{c}: goc DAT -> dot bien {hang[-1]} rc={rc} {ra[-160:]}")
    return next((h for h in hang if h != "GIET"), "GIET"), " | ".join(chi_tiet)

def main(argv):
    if _CON:
        rc, dong = chay_ca(_CON[1]) if _CON[1] in CA else (4, f"HONG:{_CON[1]}:khong co ca nay")
        print(dong)
        return rc
    if argv not in ([], ["--chi-tiet"], ["--ca"]):
        print("dung: canh_tuoi_audit_test.py [--chi-tiet]", file=sys.stderr)
        return 2
    DOT_BIEN.extend(giai_db(TEP_MO_DUN.read_text(encoding="utf-8")))
    kq = [chay_ca(ten) for ten in CA]
    print("".join(f"[{dong}]\n" for rc, dong in kq if rc), end="")
    dat = sum(rc == 0 for rc, _ in kq)
    print(f"CA: {dat}/{len(CA)} dat")
    if argv == ["--ca"]:
        return 0 if dat == len(CA) else 1
    with ThreadPoolExecutor(min(8, os.cpu_count() or 1)) as bo:
        kq_db = list(bo.map(lambda d: (d[0], *chay_dot_bien(*d)), DOT_BIEN))
    for ten, h, ct in kq_db:
        if h != "GIET" or argv:
            print(f"[DOT BIEN {h}] {ten}: {ct}")
    giet = sum(h == "GIET" for _, h, _ in kq_db)
    print(f"DOT BIEN: {giet}/{len(DOT_BIEN)} bi giet dung ly do")
    loi_tk = [f"{ten}: mong {mong}, duoc {h}" for ten, neo, thay, dich, mong, *tep in TU_KIEM for h in [chay_dot_bien(ten, (tep or ["T"])[0], neo, thay, (dich,))[0]] if h != mong]
    print("".join(f"[TU KIEM] {x}\n" for x in loi_tk), end="")
    print(f"TU KIEM PHAN HANG: {'DAT' if not loi_tk else 'DO'} ({len(TU_KIEM)} dot bien)")
    ok = dat == len(CA) > 0 and giet == len(DOT_BIEN) > 0 and len({d[0] for d in DOT_BIEN}) == len(DOT_BIEN) and not loi_tk
    print(f"TONG: {'DAT' if ok else 'DO'}")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
