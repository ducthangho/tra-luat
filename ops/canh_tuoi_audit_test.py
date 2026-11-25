#!/usr/bin/env python3
"""Bo test cua .github/workflows/canh-tuoi-audit.yml va (khi co) ops/canh_tuoi_audit.py (wp1494, B2). Offline: khong goi GitHub that.

Dung: `python ops/canh_tuoi_audit_test.py` (tat ca) · `--chi-tiet` (in them cap goc/dot bien tung dong) · `--mot-ca TEN GOC MO_DUN`
(tien trinh con cua vong dot bien). Chi `bang()` nem `TinHieuChotCa` mang TEN CA dang chay: con in `DO:<ca>:` va thoat 3; moi
loi khac thoat 4. Dot bien chay tren BAN SAO tam, ten tep rieng, `-B`; chi GIET khi ca dich nem dung lop ay voi dung ten ca.
Ra (bon dong cuoi): `CA: N/N dat` · `DOT BIEN: M/M bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (k dot bien)` · `TONG: DAT`."""
import os
import re
import subprocess
import sys
import tempfile
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
    for tep in (W_TEP, TEP_TEST):
        bang(not mau.search(tep.read_text(encoding="utf-8")), f"{tep.name} chua dau bo-qua-CI")

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
    try:
        CA[ten]()
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
    if argv not in ([], ["--chi-tiet"]):
        print("dung: canh_tuoi_audit_test.py [--chi-tiet]", file=sys.stderr)
        return 2
    kq = [chay_ca(ten) for ten in CA]
    print("".join(f"[{dong}]\n" for rc, dong in kq if rc), end="")
    dat = sum(rc == 0 for rc, _ in kq)
    print(f"CA: {dat}/{len(CA)} dat")
    kq_db = [(d[0], *chay_dot_bien(*d)) for d in DOT_BIEN]
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
