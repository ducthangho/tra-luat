#!/usr/bin/env python3
"""Bo test cua ops/canh_tuoi_audit.py va .github/workflows/canh-tuoi-audit.yml (wp1494, B2). Offline: khong goi GitHub that.

Dung: `python ops/canh_tuoi_audit_test.py` (tat ca) · `--chi-tiet` (in them cap goc/dot bien tung dong) · `--mot-ca TEN GOC MO_DUN`
(tien trinh con cua vong dot bien). Chi `bang()` nem `TinHieuChotCa` mang TEN CA dang chay: con in `DO:<ca>:` va thoat 3; moi
loi khac thoat 4. Dot bien chay tren BAN SAO tam, ten tep rieng, `-B`; chi GIET khi ca dich nem dung lop ay voi dung ten ca.
Ra (bon dong cuoi): `CA: N/N dat` · `DOT BIEN: M/M bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (k dot bien)` · `TONG: DAT`."""
import base64
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
TD, BOT = datetime.timedelta, "github-actions[bot]"
F_BYTE = (ROOT / "ops/specs/wp1460-r1/hop_dong/fixture.json").read_bytes()
NEN = json.loads(F_BYTE)["nen"]
F0 = datetime.datetime(2026, 12, 12, 19, 17)   # khung hien hanh cua moi ca (thu Bay 19:17 UTC)
P0, T0 = F0 - TD(days=7), F0 + TD(hours=5)
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

class Gia:
    """GitHub gia: Issue co than/state/comment that trong bo nho; POST luu comment TRUOC khi quyet dinh phan hoi; ghi nhat ky tung lan
    gui VAT LY (phuong thuc, URL, co Authorization khong, than, timeout, thoi diem don dieu luc bat dau); ton trong `timeout`."""
    def __init__(self):
        self.t, self.nk, self.ngu_nk, self.luot, self.thu_tu, self.goi = 0.0, [], [], {}, [], {}
        self.wf, self.tree, self.master, self.ahead = dict.fromkeys(("a" * 40, "e" * 40), JOB_KV.encode()), dict.fromkeys(("a" * 40, "e" * 40), "b" * 40), "a" * 40, 0
        self.issue, self.id_cm, self.lech_gio, self.T, self.rid = {1520: {"body": "", "state": "open", "cm": []}}, 5000, 0, T0, 7001
        self.sua, self.tre, self.trang, self.so_d2 = [], [], 100, {}

    def dong_ho(self): return self.t

    def ngu(self, giay):
        self.ngu_nk.append(giay)
        self.t += giay

    def them(self, luot):
        self.luot[luot["d1"]["id"]] = luot
        self.thu_tu.append(luot["d1"]["id"])
        self.goi.update(luot["goi"])
        return luot

    def loi(self, mau, *phan_hoi, pt="GET"):
        """Hang doi phan hoi thay the cho cac lan gui khop `mau`: moi phan tu la (ma, than[, header]) hoac mot ngoai le de nem; het hang doi thi di duong thuong."""
        hang = list(phan_hoi)
        self.sua.append((mau, pt, lambda *_: hang.pop(0) if hang else None))

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
        return ma, {k: v for k, v in hd_ra.items() if v is not None}, io.BytesIO(tra if isinstance(tra, bytes) else json.dumps(tra).encode())

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
    g = Gia()
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
def tho(ten, neo, thay, *ca_dich): DB_M.append((ten, "tho", (neo, thay), ca_dich))                 # chuoi neo nguyen van

def giai_db(nguon):
    """Moi muc cua DB_M -> (ten, "M", chuoi neo — DUNG MOT lan trong mo-dun goc, chuoi thay, cac ca dich). Nhan khong duy nhat => neo rong => HONG."""
    ra = []
    for ten, cach, ts, ca_dich in DB_M:
        if cach == "tho":
            ra.append((ten, "M", ts[0], ts[1], ca_dich))
            continue
        nhan = ts if cach == "khong" else ts[0]
        dong = [d for d in nguon.split("\n") if re.search(rf"#.*(?<![\w:.]){re.escape(nhan)}(?![\w:.])", d)]
        neo = dong[0] if len(dong) == 1 else ""
        thay = re.sub(r"^(\s*(?:el)?if ).*?(:\s+# )", r"\1False\2", neo) if cach == "khong" else neo.replace(ts[1], ts[2]) if ts[1] in neo else neo
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
    tho("d01_02_" + _f, f'    "{_f}",  # lk', "", "n1_lien_ket_" + _f)

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
        mong(phep(bc, 20, "T2"), t2, f"TRAN_GOI = kich thuoc goi {them:+d}")

@ca
def n1_j_vuot_tran():
    for them, t1 in ((-1, (KDD, "than_vuot_tran")), (0, ("dat", "dat"))):
        g = gh()
        n = len(json.dumps(g.xu_ly("GET", "/actions/runs/20/artifacts", None)[1]).encode())
        ma, bc, nk = luot_wd(g, tran={"TRAN_GOI": n + them})
        mong(phep(bc, 20, "T1"), t1, f"TRAN_GOI = than D4 {them:+d}")
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
    loi_tk = [f"{ten}: mong {mong}, duoc {h}" for ten, neo, thay, dich, mong in TU_KIEM for h in [chay_dot_bien(ten, "T", neo, thay, (dich,))[0]] if h != mong]
    print("".join(f"[TU KIEM] {x}\n" for x in loi_tk), end="")
    print(f"TU KIEM PHAN HANG: {'DAT' if not loi_tk else 'DO'} ({len(TU_KIEM)} dot bien)")
    ok = dat == len(CA) > 0 and giet == len(DOT_BIEN) > 0 and len({d[0] for d in DOT_BIEN}) == len(DOT_BIEN) and not loi_tk
    print(f"TONG: {'DAT' if ok else 'DO'}")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
