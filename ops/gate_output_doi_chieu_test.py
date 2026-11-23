#!/usr/bin/env python3
"""Phản chứng CHẠY ĐƯỢC cho `ops/gate_output_doi_chieu.py` — packet #1236 đợt A, đặc tả `ops/specs/wp1236-r12.md` mục `nghiem_thu`
(sha256 4589daf1…). Tên ca theo bảng: `a1NN_…` = A1-NN, `a2NN_…` = A2-NN.

Fixture THẬT ở `ops/land/**` (không sửa); biến thể dựng trên BẢN SAO trong thư mục tạm. A1-2, A2-11, A2-13 đọc cây tại một commit
ghim bằng `git archive` (không đọc cây làm việc); không có commit ấy ⇒ ca ĐỎ, không bỏ qua.
ĐỘT BIẾN sửa BẢN SAO TẠM của module (tên tệp riêng từng đột biến, `-B`), ca đích chạy ở tiến trình con và phải XANH trên bản gốc
trước. Chỉ `bang()` ném `TinHieuChotCa` (con in `DO:<ca>:`, thoát 3) ⇒ GIẾT; lỗi vô can thoát 4 ⇒ TÍN DỤNG GIẢ. `TU_KIEM` kiểm
chính bộ phân hạng.

Ra: `CA: N/N dat` · `DOT BIEN: M/M bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (k dot bien)` · `TONG: DAT`.
"""
import ast
import contextlib
import importlib.util
import io
import json
import re
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

import yaml

sys.dont_write_bytecode = True
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="backslashreplace")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MA = Path(os.environ.get("GATE_OUTPUT_DOI_CHIEU_MA") or HERE / "gate_output_doi_chieu.py")
BASE = "8048551a9b1eb886c126d2a1a4df0f95fb285964"   # base soạn đặc tả r9
CHECK_TEN_CHEP_RIENG = ("gate (ubuntu-latest)", "gate-cong-cu-gop (ubuntu-latest)", "gate-ops (ubuntu-latest)",
                        "gate-packet-loop (ubuntu-latest)", "gate-registry (ubuntu-latest)")
L = "ops/land/"
FX = {   # tên: (tệp danh-gia, tệp provenance dùng cho bản sao mini, trạng thái, lý do) — bảng Fixture của đặc tả
    "T-v3-pass": (L + "pr1440-wp1319-provenance/danh-gia-gate-output-44669622916.txt",
                  L + "pr1440-wp1319-provenance/ci-provenance-44669622916/provenance.yaml", "passed", []),
    "T-v2-pass": (L + "pr1453-wp433-provenance/hau-due-66eae51/danh-gia-gate-output-44717155521.txt",
                  L + "pr1453-wp433-provenance/hau-due-66eae51/ci/provenance.yaml", "passed", []),
    "T-v1-pass": (L + "pr1231-wp1105-provenance/danh-gia-gate-output-42032872356.txt",
                  L + "pr1231-wp1105-provenance/ci/provenance.yaml", "passed", []),
    "T-fail": (L + "pr1453-wp433-provenance/danh-gia-gate-output-44711337223.txt",
               L + "pr1453-wp433-provenance/ci/provenance.yaml", "failed", []),
    "T-skip": (L + "pr1344-wp1343-provenance/danh-gia-gate-output-43969906464.txt",
               L + "pr1344-wp1343-provenance/ci/provenance.yaml", "not_measured", ["co_job_skipped"]),
}
THU_MUC_THAT = {"T-v3-pass": "pr1440-wp1319-provenance", "T-v2-pass": "pr1453-wp433-provenance", "T-v1-pass": "pr1231-wp1105-provenance",
                "T-fail": "pr1453-wp433-provenance", "T-skip": "pr1344-wp1343-provenance"}


class TinHieuChotCa(AssertionError):
    """Chỉ `bang()` ném lớp này ⇒ phân biệt được giết thật (chốt) với chết vì lỗi vô can."""


CA = {}


def bang(dieu_kien, thong_diep):
    if not dieu_kien:
        raise TinHieuChotCa(thong_diep)


def ca(f):
    CA[f.__name__] = f
    return f


_M = []


def G():
    if not _M:
        spec = importlib.util.spec_from_file_location("gate_output_doi_chieu_duoi_test", MA)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        _M.append(m)
    return _M[0]


@contextlib.contextmanager
def mini(ten, sua_tep=None, sua_prov=None):
    """Thư mục tạm chỉ chứa `dg.txt` (bản sao tệp đánh giá) và `prov.yaml` (bản sao provenance), sau khi áp hai hàm sửa."""
    tep, prov, _, _ = FX[ten]
    with tempfile.TemporaryDirectory(prefix="godc_") as thu:
        t = Path(thu)
        b = (ROOT / tep).read_bytes()
        y = yaml.safe_load((ROOT / prov).read_bytes().decode("utf-8"))
        if sua_tep:
            b = sua_tep(b.decode("utf-8")).encode("utf-8") if not isinstance(sua_tep, bytes) else sua_tep
        if sua_prov:
            sua_prov(y)
        (t / "dg.txt").write_bytes(b)
        (t / "prov.yaml").write_text(yaml.safe_dump(y, allow_unicode=True, sort_keys=False), encoding="utf-8", newline="")
        yield t / "dg.txt", t


def kt(ten, sua_tep=None, sua_prov=None):
    with mini(ten, sua_tep, sua_prov) as (tep, thu):
        return G().kiem_tep(tep, thu)


def ky(kq, tt, ly, nhan):
    bang(kq == (tt, ly), f"{nhan}: mong {(tt, ly)}, được {kq}")


def dong_job(txt, chi_so):
    """(chỉ số dòng, nội dung) của dòng `JOB … -> …` thứ `chi_so`."""
    ds = [i for i, d in enumerate(txt.split("\n")) if d.startswith("JOB ") and " -> " in d]
    return ds[chi_so]


def sua_dong(txt, i, f):
    d = txt.split("\n")
    d[i] = f(d[i])
    return "\n".join(d)


def doi_tong(txt, moi):
    d = txt.split("\n")
    i = max(k for k, x in enumerate(d) if x.startswith("MOC_GATE_OUTPUT: "))
    d[i] = moi
    return "\n".join(d)


def job_id(dong):
    return int(dong.split()[1])


@contextlib.contextmanager
def cay_tai(commit, *duong):
    """`git archive <commit> <đường dẫn…>` ra thư mục tạm. Không đọc được commit ⇒ ca ĐỎ (không bỏ qua)."""
    with tempfile.TemporaryDirectory(prefix="godc_arc_") as thu:
        r = subprocess.run(["git", "-C", str(ROOT), "archive", "--format=tar", commit, "--", *duong], capture_output=True)
        bang(r.returncode == 0, f"git archive {commit} rc={r.returncode} — CI cần fetch-depth 0: {r.stderr[-200:]!r}")
        with tarfile.open(fileobj=io.BytesIO(r.stdout)) as tf:
            tf.extractall(thu, filter="data")
        yield Path(thu)


# ---------------------------------------------------------------- A1 — tệp đánh giá và provenance
@ca
def a101_sau_fixture_that():
    for ten, (tep, _, tt, ly) in FX.items():
        ky(G().kiem_tep(ROOT / tep, ROOT / L / THU_MUC_THAT[ten]), tt, ly, ten)
    ky(G().kiem_tep(ROOT / L / "pr1130-wp1122-provenance/danh-gia-gate-output-41365578430.txt", ROOT / L / "pr1130-wp1122-provenance"),
       "not_measured", ["provenance_0"], "T-khong-prov")


@ca
def a102_ca_kho_tai_base():
    with cay_tai(BASE, "ops/land") as goc:
        dem, n = {}, 0
        for p in sorted((goc / "ops/land").glob("**/danh-gia-gate-output-*.txt")):
            thu = goc / "ops/land" / p.relative_to(goc / "ops/land").parts[0]
            tt, _ = G().kiem_tep(p, thu)
            dem[tt] = dem.get(tt, 0) + 1
            n += 1
        bang(n == 66 and dem == {"passed": 47, "failed": 10, "not_measured": 9}, f"cả kho tại base: {n} tệp {dem}")


@ca
def a103_bo_phan_tich():
    def them(x):
        return lambda t: t + x
    def lap(t):
        d = t.split("\n")
        i = dong_job(t, 3)
        d.insert(i + 1, d[i])
        return "\n".join(d)

    def cr_tu_do(t):
        return sua_dong(t, dong_job(t, 2), lambda d: d + "\rX")

    def nua_crlf(t):
        d = t.split("\n")
        return "\n".join(x + "\r" if k % 2 == 0 and x else x for k, x in enumerate(d))

    def toan_crlf(t):
        d = t.rstrip("\n").split("\n")
        return "\r\n".join(d) + "\r\n"

    bien = {
        "dong_la": them("dong la o day\n"),
        "moc_lap": them("MOC_GATE_OUTPUT: passed (39/39 job co dau hieu duong)\n"),
        "thieu_moc": lambda t: "\n".join(x for x in t.split("\n") if not x.startswith("MOC_GATE_OUTPUT")),
        "job_lap": lap,
        "dau_tep_sai ": lambda t: t.replace("\n", " thua\n", 1),   # K01 lượt 5: header khớp TRỌN
        "dong_la ": them("MOC_GATE_OUTPUT: passed (39/39 job co dau hieu duong) thua\n"),   # dòng tổng khớp TRỌN
        "dong_la  ": them("JOB 777 x: skipped (khong tinh) thua\n"),   # K02 lượt 5: dòng skipped khớp TRỌN
        "job_lap ": lambda t: doi_tong(t, "") .rstrip("\n") + "\n" + t.split("\n")[dong_job(t, 3)].split(" [")[0] + ": skipped (khong tinh)\n"
        + [x for x in t.split("\n") if x.startswith("MOC_GATE_OUTPUT")][0] + "\n",
        "cr_le": cr_tu_do,
        "xuong_dong_tron": nua_crlf,
        "dau_tep_sai": lambda t: t.replace("sha256 0ea9a5e9b5a663ea6050a934b6116b1d8fcc51b23207510fe9cd056342058faf",
                                          "sha256 0ea9a5e9b5a663ea6050a934b6116b1d8fcc51b23207510fe9cd056342058fa", 1),
    }
    for ly, f in bien.items():
        ky(kt("T-v3-pass", f), "not_measured", [ly.strip()], ly)
    with mini("T-v3-pass") as (tep, thu):
        tep.write_bytes(tep.read_bytes() + b"\xff\xfe")
        ky(G().kiem_tep(tep, thu), "not_measured", ["khong_phai_utf8"], "khong_phai_utf8")
    ky(kt("T-v3-pass", toan_crlf), "passed", [], "doi chung toan CRLF")


@ca
def a104_bo_sinh_la():
    ky(kt("T-v3-pass", lambda t: t.replace("0ea9a5e9b5a663ea6050a934b6116b1d8fcc51b23207510fe9cd056342058faf", "1" * 64, 1)),
       "not_measured", ["bo_sinh_la"], "bo_sinh_la")


@ca
def a105_bam_log():
    def f(t):
        i = dong_job(t, 4)
        d = t.split("\n")[i]
        return sua_dong(t, i, lambda x: x.replace(d.split("log_sha256=")[1][:64], "0" * 64))
    t = (ROOT / FX["T-v3-pass"][0]).read_text(encoding="utf-8")
    k = job_id(t.split("\n")[dong_job(t, 4)])
    ky(kt("T-v3-pass", f), "not_measured", [f"log_sha_lech:{k}"], "log_sha_lech")


@ca
def a106_danh_tinh_job():
    t = (ROOT / FX["T-v3-pass"][0]).read_text(encoding="utf-8")
    i = dong_job(t, 5)
    k = job_id(t.split("\n")[i])
    ky(kt("T-v3-pass", lambda x: sua_dong(x, i, lambda d: d.replace(") [ubuntu-latest]", "x) [ubuntu-latest]", 1)
                                                      if ") [" in d else d.replace(" [ubuntu-latest]", "x [ubuntu-latest]", 1))),
       "not_measured", [f"job_lech:{k}"], "doi name")
    ky(kt("T-v3-pass", lambda x: sua_dong(x, i, lambda d: d.replace("[ubuntu-latest]", "[ubuntu-24.04]", 1))),
       "not_measured", [f"job_lech:{k}"], "doi labels")
    ky(kt("T-v3-pass", lambda x: sua_dong(x, i, lambda d: d.replace(" (", "  (", 1))),
       "not_measured", [f"job_lech:{k}"], "giu khoang trang trong ten")
    tf = (ROOT / FX["T-fail"][0]).read_text(encoding="utf-8")
    jf = [n for n, d in enumerate(tf.split("\n")) if "conclusion=failure" in d][0]
    kf = job_id(tf.split("\n")[jf])
    ky(kt("T-fail", lambda x: sua_dong(x, jf, lambda d: d.replace("conclusion=failure", "conclusion=cancelled"))),
       "not_measured", [f"job_lech:{kf}"], "doi conclusion")


@ca
def a107_tap_job():
    t = (ROOT / FX["T-v3-pass"][0]).read_text(encoding="utf-8")
    i = dong_job(t, 6)
    goc = t.split("\n")[i]
    k = job_id(goc)

    def xoa(x):
        d = x.split("\n")
        del d[i]
        return doi_tong("\n".join(d), "MOC_GATE_OUTPUT: passed (38/38 job co dau hieu duong)")

    def them(x):
        d = x.split("\n")
        d.insert(i, goc.replace(f"JOB {k} ", "JOB 999 ", 1))
        return doi_tong("\n".join(d), "MOC_GATE_OUTPUT: passed (40/40 job co dau hieu duong)")
    ky(kt("T-v3-pass", xoa), "not_measured", ["tap_job_lech"], "xoa dong job")
    ky(kt("T-v3-pass", them), "not_measured", ["tap_job_lech"], "them job la")

    def thanh_skip(x):
        d = x.split("\n")
        d[i] = f"JOB {k} {goc.split(' [')[0].split(' ', 2)[2]}: skipped -> not_measured (khong suy pass)"
        return doi_tong("\n".join(d), "MOC_GATE_OUTPUT: not_measured (38/39 job co dau hieu duong)")
    ky(kt("T-v3-pass", thanh_skip), "not_measured", ["tap_job_lech", "tap_skip_lech"], "doi thanh skipped")


@ca
def a108_neo():
    ky(kt("T-v3-pass", None, lambda y: y.update(attempt_yeu_cau=2)), "not_measured", ["provenance_0"], "(a) attempt")
    with mini("T-v3-pass") as (tep, thu):
        shutil.copy(thu / "prov.yaml", thu / "prov2.yaml")
        ky(G().kiem_tep(tep, thu), "not_measured", ["provenance_nhieu"], "(b) hai ban cung bo ba")
    ky(kt("T-v3-pass", None, lambda y: y["moc"]["run"].update(event="workflow_dispatch")), "not_measured", ["khong_phai_run_land"], "(c)")
    ky(kt("T-v3-pass", None, lambda y: y["moc"]["run"].update(event="push\t")),
       "not_measured", ["khong_phai_run_land"], "(c) event co tab")
    ky(kt("T-v3-pass", None, lambda y: y["moc"]["run"].update(loi_khai_rest_path=".github/workflows/launcher-windows.yml")),
       "not_measured", ["khong_phai_run_land"], "(d) path")
    ky(kt("T-v3-pass", None, lambda y: y["moc"]["run"].update(run_id=float(y["moc"]["run"]["run_id"]))), "not_measured", ["provenance_0"], "(e)")
    ky(kt("T-v3-pass", None, lambda y: y.update(attempt_yeu_cau=True)), "not_measured", ["provenance_0"], "(f) attempt bool")
    ky(kt("T-v3-pass", None, lambda y: y["moc"]["run"].update(head_sha="0" * 40)), "not_measured", ["provenance_0"], "(g) head")
    ky(kt("T-v3-pass", None, lambda y: y.update(schema="ci_provenance/2")), "not_measured", ["provenance_0"], "(h) schema")


def _bo_job(ten_job):
    def ft(x):
        d = [z for z in x.split("\n") if not (z.startswith("JOB ") and f" {ten_job} [" in z)]
        n = sum(1 for z in d if z.startswith("JOB ") and " -> " in z)
        return doi_tong("\n".join(d), f"MOC_GATE_OUTPUT: passed ({n}/{n} job co dau hieu duong)")

    def fp(y):
        ids = [j["job_id"] for j in y["moc"]["gate_output"]["jobs"] if j.get("name") == ten_job]
        y["moc"]["gate_output"]["jobs"] = [j for j in y["moc"]["gate_output"]["jobs"] if j.get("job_id") not in ids]
        y["moc"]["checkout"] = [c for c in y["moc"]["checkout"] if c.get("job_id") not in ids]
        for k in ids:
            y["log_day_du"].pop(k, None)
    return ft, fp


@ca
def a109_check_bat_buoc():
    ft, fp = _bo_job("gate-registry (ubuntu-latest)")
    ky(kt("T-v3-pass", ft, fp), "not_measured", ["check_bat_buoc:gate-registry (ubuntu-latest)"], "bo gate-registry")
    t = (ROOT / FX["T-v3-pass"][0]).read_text(encoding="utf-8")   # K02 lượt 5: job bắt buộc có mặt nhưng not_measured
    i = [n for n, d in enumerate(t.split("\n")) if d.startswith("JOB ") and " gate-registry (ubuntu-latest) [" in d][0]
    ky(kt("T-v3-pass", lambda x: doi_tong(sua_dong(x, i, lambda d: d.split(" -> ")[0] + " -> not_measured: x"),
                                          "MOC_GATE_OUTPUT: not_measured (38/39 job co dau hieu duong)")),
       "not_measured", ["check_bat_buoc:gate-registry (ubuntu-latest)"], "gate-registry not_measured")
    cay = ast.parse((ROOT / ".claude/dev/packet_loop.py").read_text(encoding="utf-8"))
    nut = [n for n in cay.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CHECK_BAT_BUOC" for t in n.targets)]
    bang(len(nut) == 1, f"CHECK_BAT_BUOC: {len(nut)} nút gán")
    gt = eval(compile(ast.Expression(nut[0].value), "packet_loop.py", "eval"), {"__builtins__": {"tuple": tuple}})
    bang(set(G().CHECK_BAT_BUOC_TEN) == {x[1] for x in gt} == set(CHECK_TEN_CHEP_RIENG),
         f"CHECK_BAT_BUOC_TEN {G().CHECK_BAT_BUOC_TEN} vs packet_loop {gt}")


@ca
def a110_dong_tong():
    ky(kt("T-v2-pass", lambda t: doi_tong(t, "MOC_GATE_OUTPUT: passed (38/39 job co dau hieu duong)")), "not_measured", ["moc_lech"], "v2")
    ky(kt("T-fail", lambda t: doi_tong(t, "MOC_GATE_OUTPUT: passed (39/39 job co dau hieu duong)")), "not_measured", ["moc_lech"], "fail")
    for moi in ("passed (39/40", "failed (39/39"):   # H01 lượt 3: đổi ĐÚNG một thành phần của bộ ba
        ky(kt("T-v3-pass", lambda t: doi_tong(t, f"MOC_GATE_OUTPUT: {moi} job co dau hieu duong)")), "not_measured", ["moc_lech"], moi)


def _them_skip(dang, tong):
    """Thêm một job skipped (cả provenance, kèm checkout `skipped`) với dòng `dang` ∈ cu · v3, dòng tổng `tong`."""
    def ft(x):
        dong = ("JOB 777 job-them: skipped (khong tinh)" if dang == "cu" else
                "JOB 777 job-them: skipped -> not_measured (khong suy pass)")
        d = x.split("\n")
        d.insert(dong_job(x, 0), dong)
        return doi_tong("\n".join(d), tong)

    def fp(y):
        y["moc"]["gate_output"]["jobs"].append({"job_id": 777, "name": "job-them", "conclusion": "skipped", "labels": []})
        y["moc"]["checkout"].append({"job_id": 777, "trang_thai": "skipped"})
    return ft, fp


@ca
def a111_skipped_theo_phien_ban():
    ft, fp = _them_skip("cu", "MOC_GATE_OUTPUT: not_measured (39/40 job co dau hieu duong)")
    ky(kt("T-v3-pass", ft, fp), "not_measured", ["dong_skip_sai_phien_ban"], "v3 + dong cu")
    ft, fp = _them_skip("v3", "MOC_GATE_OUTPUT: passed (39/39 job co dau hieu duong)")
    ky(kt("T-v2-pass", ft, fp), "not_measured", ["dong_skip_sai_phien_ban"], "v2 + dong v3")


@ca
def a112_symlink():
    if not hasattr(os, "symlink") or os.name != "posix":
        print("BO QUA a112 (symlink chi do tren POSIX)")
        return
    with mini("T-v3-pass") as (tep, thu), tempfile.TemporaryDirectory(prefix="godc_ngoai_") as ngoai:
        (Path(ngoai) / "p.yaml").write_bytes((thu / "prov.yaml").read_bytes())
        (thu / "prov.yaml").unlink()
        os.symlink(Path(ngoai) / "p.yaml", thu / "lk.yaml")
        ky(G().kiem_tep(tep, thu), "not_measured", ["symlink", "provenance_0"], "symlink tep")


@ca
def a113_ket_luan():
    t = (ROOT / FX["T-fail"][0]).read_text(encoding="utf-8")
    i = [n for n, d in enumerate(t.split("\n")) if "conclusion=failure" in d][0]
    k = job_id(t.split("\n")[i])

    def f(x):
        x = sua_dong(x, i, lambda d: d.split(" -> ")[0] + " -> passed: x")
        return doi_tong(x, "MOC_GATE_OUTPUT: passed (39/39 job co dau hieu duong)")
    ky(kt("T-fail", f), "not_measured", [f"ket_luan_lech:{k}"], "lat failure thanh passed")
    ky(kt("T-fail", lambda x: sua_dong(x, i, lambda d: d.split(" -> ")[0] + " -> not_measured: x")),   # H01 lượt 3: vế thứ hai
       "not_measured", [f"ket_luan_lech:{k}", "moc_lech"], "failure ma not_measured")


@ca
def a114_provenance_tu_khai_du():
    def a(y):
        y["moc"]["run"]["trang_thai"] = "not_measured"

    def b(y):
        y["moc"]["gate_output"]["tap_jobs"]["trang_thai"] = "failed"

    def c(y):
        y["moc"]["checkout"][1]["trang_thai"] = "not_measured"

    def d(y):
        y["moc"]["checkout"] = []

    def e(y):   # J01 lượt 4: checkout `skipped` cho job KHÔNG skipped
        y["moc"]["checkout"][1]["trang_thai"] = "skipped"
    for nhan, f in (("a", a), ("b", b), ("c", c), ("d", d), ("e", e)):
        ky(kt("T-v3-pass", None, f), "not_measured", ["provenance_chua_du"], f"({nhan})")


@ca
def a115_skipped_mat_passed():
    ft, fp = _them_skip("cu", "MOC_GATE_OUTPUT: passed (39/39 job co dau hieu duong)")
    ky(kt("T-v2-pass", ft, fp), "not_measured", ["co_job_skipped"], "v2 them job skipped ngoai CHECK")
    ky(kt("T-v2-pass"), "passed", [], "doi chung")


@ca
def a117_loi_duyet_va_job_trung():   # review lượt 2 G01 (lỗi os.scandir không bị nuốt), G02 (job_id trùng trong provenance)
    from unittest import mock
    goc_scandir = os.scandir
    with mini("T-v3-pass") as (tep, thu):
        (thu / "provenance-copy").mkdir()
        shutil.copy(thu / "prov.yaml", thu / "provenance-copy" / "prov.yaml")
        ky(G().kiem_tep(tep, thu), "not_measured", ["provenance_nhieu"], "doi chung hai provenance")
        loi = lambda p, *a: (_ for _ in ()).throw(PermissionError(p)) if Path(p).name == "provenance-copy" else goc_scandir(p, *a)  # noqa: E731
        with mock.patch.object(os, "scandir", loi):
            ky(G().kiem_tep(tep, thu), "not_measured", ["PermissionError"], "G01 loi duyet")
    ky(kt("T-v3-pass", None, lambda y: y["moc"]["gate_output"]["jobs"].append(dict(y["moc"]["gate_output"]["jobs"][0]))),
       "not_measured", ["job_id_trung_provenance"], "G02 job_id trung")


@ca
def a116_yaml_la_trong_thu_muc():   # review lượt 1 F01/F02: YAML ngoài schema bỏ qua; YAML hỏng và symlink KHÔNG bị nuốt
    with mini("T-v3-pass") as (tep, thu):
        (thu / "x.yaml").write_text("- a\n- b\n", encoding="utf-8")
        ky(G().kiem_tep(tep, thu), "passed", [], "(a) YAML list")
        (thu / "y.yaml").write_text("a: [\n", encoding="utf-8")
        ky(G().kiem_tep(tep, thu), "not_measured", ["ParserError"], "(b) YAML hong")
    if os.name == "posix":
        with mini("T-v3-pass") as (tep, thu), tempfile.TemporaryDirectory(prefix="godc_ng_") as ng:
            (Path(ng) / "z.yaml").write_text("a: 1\n", encoding="utf-8")
            os.symlink(Path(ng) / "z.yaml", thu / "lk.yaml")
            ky(G().kiem_tep(tep, thu), "not_measured", ["symlink"], "(c) symlink canh provenance that")
        with mini("T-v3-pass") as (tep, thu), tempfile.TemporaryDirectory(prefix="godc_ng_") as ng:   # J01 lượt 4
            os.symlink(ng, thu / "lkdir")
            ky(G().kiem_tep(tep, thu), "not_measured", ["symlink"], "(d) symlink thu muc con")
            os.symlink(thu, Path(ng) / "goc")
            ky(G().kiem_tep(tep, Path(ng) / "goc"), "not_measured", ["symlink", "provenance_0"], "(e) thu muc provenance la symlink")


# ---------------------------------------------------------------- A2 — lời khai, miễn, hồ sơ
@ca
def a201_loi_khai():
    doc = {"moc_gate_output": "x", "a": [{"gate_output": "y"}], "b": {"Gate-Output": "z"}, "gate_output_nguon": "w",
           "gate_output_nguon_va_gioi_han": "w", "moc_gate_output_rc_disposition": "w"}   # K01 lượt 5: đủ ba tên phi-lời-khai
    kq = sorted(d for d, _ in G().loi_khai(doc))
    bang(kq == ["$.a[0].gate_output", "$.b.Gate-Output", "$.moc_gate_output"], f"loi_khai: {kq}")


@ca
def a202_token():
    vao = ["measured — x", "  passed", "FAILED: x", "measuredx", "measured1", "passed!", 5, {"a": 1}]
    ra = [khong_nem(lambda: G().token(v)) for v in vao]
    bang(ra == ["measured", "passed", "failed", None, None, None, None, None], f"token: {ra}")


@contextlib.contextmanager
def ho_so_tam(ten="T-v3-pass"):
    """Thư mục provenance tạm = bản sao thư mục thật của fixture (để trích tên tệp thật)."""
    with tempfile.TemporaryDirectory(prefix="godc_hs_") as thu:
        dich = Path(thu) / "pr9001-thu-provenance"
        shutil.copytree(ROOT / L / THU_MUC_THAT[ten], dich, symlinks=True)
        yield dich


def ten_tep(ten):
    return str(Path(FX[ten][0]).relative_to(L + THU_MUC_THAT[ten]))


@ca
def a203_duong_khong_tep():
    with ho_so_tam() as thu:
        vp = G().kiem_ho_so({"moc_gate_output": "measured — kiem-gate-output.txt"}, thu)
        bang(vp == ["$.moc_gate_output: duong_khong_tep_danh_gia"], f"vp: {vp}")
        bang(G().kiem_ho_so({"gate_output": 5}, thu) == ["$.gate_output: dinh_dang_loi_khai"], "dinh dang")


@ca
def a204_duong_dan():
    from unittest.mock import patch

    t = ten_tep("T-v3-pass")
    with ho_so_tam() as thu:
        vp = G().kiem_ho_so({"moc_gate_output": f"measured — ./{t}"}, thu)
        bang(vp == [], f"duong ./ hop le: {vp}")
        (thu / "x").mkdir()
        tham_chieu = [f"x/../{t}", "danh-gia-gate-output-1.txt"]
        if os.name == "posix":
            os.symlink(".", thu / "lk")
            tham_chieu.append(f"lk/{t}")
        for ref in tham_chieu:
            vp = G().kiem_ho_so({"moc_gate_output": f"measured — {ref}"}, thu)
            bang(vp == [f"$.moc_gate_output: tep_danh_gia_khong_hop_le:{ref}"], f"{ref}: {vp}")
        ref = f"/tep-ton-tai/{t}"
        with patch.object(Path, "is_file", return_value=True):
            vp = G().kiem_ho_so({"moc_gate_output": f"measured — {ref}"}, thu)
        bang(vp == [f"$.moc_gate_output: tep_danh_gia_khong_hop_le:{ref}"], f"duong tuyet doi: {vp}")


@ca
def a205_duong_khop():
    with ho_so_tam() as thu:
        vp = G().kiem_ho_so({"moc_gate_output": f"measured — {ten_tep('T-v3-pass')}"}, thu)
        bang(vp == [], f"vp: {vp}")


@ca
def a206_duong_lech():
    with ho_so_tam("T-fail") as thu:
        vp = G().kiem_ho_so({"moc_gate_output": f"measured — {ten_tep('T-fail')}"}, thu)
        bang(len(vp) == 1 and vp[0].startswith("$.moc_gate_output: danh_gia_khong_passed:") and vp[0].endswith(":failed:-"), f"T-fail {vp}")
    with ho_so_tam("T-skip") as thu:
        vp = G().kiem_ho_so({"moc_gate_output": f"passed — {ten_tep('T-skip')}"}, thu)
        bang(len(vp) == 1 and ":not_measured:co_job_skipped" in vp[0], f"T-skip {vp}")


@ca
def a207_hai_tep():
    t = ten_tep("T-v3-pass")
    with ho_so_tam() as thu:
        b = (thu / t).read_text(encoding="utf-8")
        i = dong_job(b, 4)
        d = b.split("\n")[i]
        (thu / "x").mkdir()
        (thu / "x" / "danh-gia-gate-output-44669622916.txt").write_text(
            sua_dong(b, i, lambda z: z.replace(d.split("log_sha256=")[1][:64], "0" * 64)), encoding="utf-8", newline="")
        vp = G().kiem_ho_so({"moc_gate_output": f"measured — {t} x/danh-gia-gate-output-44669622916.txt"}, thu)
        bang(len(vp) == 1 and "danh_gia_khong_passed:x/" in vp[0], f"vp: {vp}")


@ca
def a208_failed_nhat_quan():
    with ho_so_tam("T-fail") as thu:
        bang(G().kiem_ho_so({"moc_gate_output": f"failed — {ten_tep('T-fail')}"}, thu) == [], "failed khop")
        bang(G().kiem_ho_so({"moc_gate_output": "failed — run hong, khong tep"}, thu) == [], "failed khong tep")
    with ho_so_tam() as thu:
        vp = G().kiem_ho_so({"moc_gate_output": f"failed — {ten_tep('T-v3-pass')}"}, thu)
        bang(len(vp) == 1 and "danh_gia_khong_failed:" in vp[0], f"failed tren tep passed: {vp}")


SHA = "d8cf2ab57f9f25a93cefedcebfb315826b6b78fe"
URL = "https://github.com/ducthangho/tra-luat/issues/1236#issuecomment-123"


def rb(body, **k):
    d = {"html_url": URL, "user": {"login": "ducthangho"}, "author_association": "OWNER", "body": body}
    d.update(k)
    return d


DONG = f"mien_gate_output: {SHA} os=ubuntu-latest ly_do=job huy theo chi thi han=2026-12-31"


@ca
def a209_mien():
    bien = {
        "a": (rb(f"Chủ kho miễn.\n{DONG}\n"), f"owner_waived — {URL} {SHA} job bi huy", []),
        "b": (rb(DONG, author_association="MEMBER"), f"owner_waived — {URL} {SHA}", ["tac_gia"]),
        "c": (rb(DONG, user={"login": "ai-khac"}), f"owner_waived — {URL} {SHA}", ["tac_gia"]),
        "d": (rb(f"{DONG}\n{DONG}"), f"owner_waived — {URL} {SHA}", ["dong_mien"]),
        "e": (rb(f"Duyệt merge {SHA}"), f"owner_waived — {URL} {SHA}", ["dong_mien"]),
        "f": (rb(DONG.replace("2026-12-31", "2026-02-30")), f"owner_waived — {URL} {SHA}", ["han"]),
        "g": (rb(DONG.replace("ubuntu-latest", "windows-latest")), f"owner_waived — {URL} {SHA}", ["os"]),
        "h": (rb(DONG, html_url=URL.replace("123", "124")), f"owner_waived — {URL} {SHA}", ["html_url"]),
        "i": (rb(DONG), f"owner_waived — {URL} khong co sha", ["sha"]),
    }
    for nhan, (d, chuoi, mong) in bien.items():
        with tempfile.TemporaryDirectory(prefix="godc_rb_") as thu:
            (Path(thu) / "readback-duyet-issuecomment-123.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            kq = G().kiem_mien(chuoi, Path(thu), None)
            bang(kq == mong, f"({nhan}) mong {mong}, được {kq}")
    with tempfile.TemporaryDirectory(prefix="godc_rb_") as thu:
        (Path(thu) / "readback-duyet-issuecomment-123.json").write_text(json.dumps(rb(DONG)), encoding="utf-8")
        bang(G().kiem_mien(f"owner_waived — {URL}", Path(thu), SHA) == [], "head bang SHA")
        bang(G().kiem_mien(f"owner_waived — {URL}", Path(thu), "0" * 40) == ["sha"], "head khac SHA")
        bang(G().kiem_mien(f"owner_waived — {URL} {URL.replace('123', '9')}", Path(thu), SHA) == ["url"], "hai URL")
        bang(G().kiem_mien(f"owner_waived — {URL} {URL}", Path(thu), SHA) == ["url"], "hai URL giong nhau")
        bang(G().kiem_ho_so({"moc_gate_output": f"owner_waived — {URL} {SHA}"}, Path(thu)) == [], "(j) kiem_ho_so hop le")
        (Path(thu) / "readback-duyet-issuecomment-123.json").write_text(json.dumps(rb(DONG, author_association="MEMBER")), encoding="utf-8")
        vp = G().kiem_ho_so({"moc_gate_output": f"owner_waived — {URL} {SHA}"}, Path(thu))
        bang(vp == ["$.moc_gate_output: waiver_khong_co_can_cu:tac_gia"], f"(j) kiem_ho_so MEMBER: {vp}")
        (Path(thu) / "readback-ban2-issuecomment-123.json").write_text(json.dumps(rb(DONG)), encoding="utf-8")
        bang(G().kiem_mien(f"owner_waived — {URL} {SHA}", Path(thu), None) == ["readback"], "(k) hai readback (G02 luot 2)")
    with tempfile.TemporaryDirectory(prefix="godc_rb_") as thu, tempfile.TemporaryDirectory(prefix="godc_rb2_") as ngoai:
        (Path(ngoai) / "r.json").write_text(json.dumps(rb(DONG)), encoding="utf-8")
        if os.name == "posix":   # J01 lượt 4: readback là symlink
            os.symlink(Path(ngoai) / "r.json", Path(thu) / "readback-duyet-issuecomment-123.json")
            bang(G().kiem_mien(f"owner_waived — {URL} {SHA}", Path(thu), None) == ["readback"], "(l) readback symlink")
            os.unlink(Path(thu) / "readback-duyet-issuecomment-123.json")
        (Path(thu) / "readback-duyet-issuecomment-123.json").write_text("{khong phai json", encoding="utf-8")
        bang(khong_nem(lambda: G().kiem_mien(f"owner_waived — {URL} {SHA}", Path(thu), None)) == ["doc_readback"],
             "(m) JSON hong")


def cli(*a):
    r = subprocess.run([sys.executable, "-B", str(MA), *a], capture_output=True, timeout=300,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    return r.returncode, (r.stdout + r.stderr).decode("utf-8", "replace")


@ca
def a128_cli_stat():
    from contextlib import redirect_stderr
    from io import StringIO
    from unittest.mock import patch

    stderr = StringIO()
    with patch.object(Path, "is_file", side_effect=OSError("stat unavailable")), redirect_stderr(stderr):
        rc = khong_nem(lambda: G().main(["kiem-tep", "danh-gia.txt", "--provenance", "."]))
    bang(rc == 2 and stderr.getvalue().startswith("LỖI THAM SỐ:"), f"stat loi: {rc!r}, {stderr.getvalue()!r}")


@ca
def a210_cli():
    for ten, (tep, _, tt, _) in FX.items():
        rc, ra = cli("kiem-tep", str(ROOT / tep), "--provenance", str(ROOT / L / THU_MUC_THAT[ten]))
        bang(rc == {"passed": 0, "failed": 1}.get(tt, 3) and "Traceback" not in ra, f"kiem-tep {ten}: rc={rc} {ra[-200:]}")
    rc, ra = cli("kiem-tep", "/khong/co.txt", "--provenance", str(ROOT))
    bang(rc == 2 and "Traceback" not in ra, f"kiem-tep vang: {rc}")
    rc, ra = cli("kiem-tep", "/tmp/" + "x" * 300, "--provenance", str(ROOT))   # H02 lượt 3: ENAMETOOLONG
    bang(rc == 2 and "Traceback" not in ra, f"kiem-tep ten qua dai: {rc} {ra[-150:]}")
    with tempfile.TemporaryDirectory(prefix="godc cli ") as thu:
        hs = Path(thu) / "pr9001 thu-land-evidence.yaml"
        hs.write_text("moc_gate_output: 'measured — kiem-gate.txt'\n", encoding="utf-8")
        rc, ra = cli("kiem-ho-so", str(hs))
        bang(rc == 1 and "duong_khong_tep_danh_gia" in ra and "Traceback" not in ra, f"khoang trang: {rc} {ra[-200:]}")
        hong = Path(thu) / "hong-land-evidence.yaml"
        hong.write_text("a: [\n", encoding="utf-8")
        rc, ra = cli("kiem-ho-so", str(hong))
        bang(rc == 2 and "Traceback" not in ra, f"YAML hong: {rc}")
        rc, ra = cli("kiem-ho-so", str(Path(thu) / "vang-land-evidence.yaml"))
        bang(rc == 2 and "Traceback" not in ra, f"vang: {rc}")


@ca
def a211_ho_so_1127():
    for commit in ("bb47274", "7f22121"):
        with cay_tai(commit, "ops/land/pr1127-wp1120-land-evidence.yaml", "ops/land/pr1127-wp1120-provenance") as goc:
            d = yaml.safe_load((goc / "ops/land/pr1127-wp1120-land-evidence.yaml").read_bytes().decode("utf-8"))
            vp = G().kiem_ho_so(d, goc / "ops/land/pr1127-wp1120-provenance")
            bang(any(x.endswith(": duong_khong_tep_danh_gia") for x in vp)
                 and not any("danh_gia_khong_" in x or "tep_danh_gia_khong_hop_le" in x for x in vp), f"#1127 @{commit}: {vp}")


@ca
def a212_landed_khong_loi_khai():
    vx = {"landed_dieu_kien": "Gate output DAT — 0 dong ##[error] tren 23 log"}
    with ho_so_tam() as thu:
        for nhan, d, mong in (
            ("a", {"trang_thai_packet": {"landed": True}, **vx}, ["$: landed_khong_loi_khai_gate_output"]),
            ("b", {"landed": True, **vx}, ["$: landed_khong_loi_khai_gate_output"]),
            ("c", {"trang_thai_packet": {"landed": False}, "landed_20261120": {"landed": True}, **vx}, ["$: landed_khong_loi_khai_gate_output"]),
            ("d", {"trang_thai_packet": {"landed": True}, "moc_gate_output": "measured — kiem-gate-output.txt"},
             ["$.moc_gate_output: duong_khong_tep_danh_gia", "$: landed_khong_loi_khai_gate_output"]),
            ("e", {"trang_thai_packet": {"landed": True}, "moc_gate_output": "not_measured — run khong do", "g": {"gate_output": "skipped — x"},
                   "h": {"gate_output": "not_run — x"}}, ["$: landed_khong_loi_khai_gate_output"]),   # K01 lượt 5: chỉ token âm
            ("doi chung", {"trang_thai_packet": {"landed": False}, **vx}, []),
        ):
            vp = G().kiem_ho_so(d, thu)
            bang(vp == mong, f"({nhan}) mong {mong}, được {vp}")


@ca
def a213_la_landed_khop_kiem_ho_so_land():
    spec = importlib.util.spec_from_file_location("khsl_duoi_test", HERE / "kiem_ho_so_land.py")
    k = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k)
    with cay_tai(BASE, "ops/land") as goc:
        n = landed = lech = 0
        for p in sorted((goc / "ops/land").glob("*-land-evidence.yaml")):
            _, _, la = k._xet_mot_tep(p, yaml)
            n += 1
            landed += la
            lech += la != G().la_landed(yaml.safe_load(p.read_bytes().decode("utf-8")))
        bang((n, landed, lech) == (170, 94, 0), f"la_landed vs kiem_ho_so_land: {n} ho so, {landed} landed, {lech} lech")


@ca
def a214_vong_tham_chieu():   # review lượt 1 F03
    d = yaml.safe_load("a: &x\n  - b: *x\n")
    try:
        loi = G().loi_khai(d) and None
    except Exception as e:   # RecursionError (bỏ chốt vòng) phải ĐỎ ở đây, không thoát ra thành lỗi vô can
        loi = e
    bang(isinstance(loi, ValueError) and str(loi) == "vong_tham_chieu tại $.a[0].b", f"loi_khai tren vong: {loi!r}")
    with tempfile.TemporaryDirectory(prefix="godc_vong_") as thu:
        (Path(thu) / "v-land-evidence.yaml").write_text("a: &x\n  - b: *x\n", encoding="utf-8")
        rc, ra = cli("kiem-ho-so", str(Path(thu) / "v-land-evidence.yaml"))
        bang(rc == 2 and ra.splitlines() == [f"LỖI THAM SỐ: {Path(thu) / 'v-land-evidence.yaml'}: không đọc được (ValueError)"], f"CLI vong: rc={rc} {ra[-200:]}")


def khong_nem(f):   # tính chất ĐANG ĐO là "không ném trên đầu vào dị dạng" ⇒ ngoại lệ là kết quả, không phải lỗi vô can
    try:
        return f()
    except Exception as e:
        return e


@ca
def a118_k1_k2_quet_he_thong():   # lớp chot-thieu-ca: quét đột biến AST 20-11 (#1236 issuecomment-7046799415), K1–K2
    t = (ROOT / FX["T-v3-pass"][0]).read_text(encoding="utf-8")
    k = job_id(t.split("\n")[dong_job(t, 2)])
    ky(kt("T-v3-pass", lambda x: x.replace("\n", "\ndong la ngay sau dau tep\n", 1)), "not_measured", ["dong_la"], "dong 2")
    ky(kt("T-v3-pass", lambda x: x.replace("\n", f"\nJOB {k} x: skipped (khong tinh)\n", 1)), "not_measured", ["job_lap"], "skip roi JOB")
    ky(kt("T-v3-pass", lambda x: x + "JOB 777 x: skipped (khong tinh)\n" * 2), "not_measured", ["job_lap"], "hai dong skip")
    ky(G().kiem_tep(ROOT / FX["T-v3-pass"][0], ROOT / "khong-co-thu-muc"), "not_measured", ["provenance_0"], "thu muc vang")
    with mini("T-v3-pass") as (tep, thu):
        (thu / "z.yaml").write_text("schema: ci_provenance/1\nmoc: {run: [1]}\n", encoding="utf-8")
        ky(G().kiem_tep(tep, thu), "passed", [], "provenance khac co run khong phai mapping")
        if os.name == "posix":
            with tempfile.TemporaryDirectory(prefix="godc_ng_") as ng:
                shutil.copy(thu / "prov.yaml", Path(ng) / "p.yaml")
                os.symlink(ng, thu / "lk")
                ky(G().kiem_tep(tep, thu), "not_measured", ["symlink"], "khong di vao thu muc symlink")


@ca
def a119_k3_k6_du_lieu_di_dang():
    j0 = lambda y: y["moc"]["gate_output"]["jobs"]  # noqa: E731
    ky(kt("T-v3-pass", None, lambda y: j0(y).append("x")), "passed", [], "job provenance khong phai mapping")
    for nhan, f in (("tap_jobs chuoi", lambda y: y["moc"]["gate_output"].update(tap_jobs="passed")),
                    ("checkout so", lambda y: y["moc"].update(checkout=5)), ("checkout chuoi", lambda y: y["moc"]["checkout"].append("x"))):
        ky(kt("T-v3-pass", None, f), "not_measured", ["provenance_chua_du"], nhan)
    y0 = yaml.safe_load((ROOT / FX["T-v3-pass"][1]).read_bytes().decode("utf-8"))
    k = j0(y0)[0]["job_id"]
    ky(kt("T-v3-pass", None, lambda y: j0(y)[0].update(labels=None)), "not_measured", [f"job_lech:{k}"], "labels None")
    def sk(y):
        ids = {q["job_id"] for q in j0(y) if q.get("conclusion") == "skipped"}
        [c.update(trang_thai="failed") for c in y["moc"]["checkout"] if c.get("job_id") in ids]
    ky(kt("T-skip", None, sk), "not_measured", ["provenance_chua_du"], "checkout job skipped ma failed")
    ky(kt("T-v3-pass", lambda x: x.split("\n")[0] + "\nMOC_GATE_OUTPUT: not_measured (0/0 job co dau hieu duong)\n",
          lambda y: y["moc"]["gate_output"].update(jobs=[])), "not_measured", [f"check_bat_buoc:{c}" for c in CHECK_TEN_CHEP_RIENG], "0 job")


@ca
def a215_landed_mien_di_dang():
    bang(khong_nem(lambda: G().la_landed([])) is False, "la_landed tren list")
    bang(khong_nem(lambda: G().la_landed({5: "a", "landed_20261120": "x"})) is False, "la_landed khoa so / khoi khong mapping")
    t = ten_tep("T-v3-pass")
    with ho_so_tam() as thu, tempfile.TemporaryDirectory(prefix="godc_lk_") as ng:
        if os.name == "posix":
            os.symlink(thu, Path(ng) / "lk")
            vp = G().kiem_ho_so({"moc_gate_output": f"measured — {t}"}, Path(ng) / "lk")
            bang(vp == [f"$.moc_gate_output: tep_danh_gia_khong_hop_le:{t}"], f"thu muc ho so la symlink: {vp}")
    mien = f"owner_waived — {URL} {SHA}"
    with tempfile.TemporaryDirectory(prefix="godc_rb_") as thu, tempfile.TemporaryDirectory(prefix="godc_lk_") as ng:
        r = Path(thu) / "readback-duyet-issuecomment-123.json"
        r.mkdir()
        bang(G().kiem_mien(mien, Path(thu), None) == ["readback"], "readback la thu muc")
        r.rmdir()
        for nhan, d, mong in (("list", [rb(DONG)], ["html_url"]), ("user chuoi", rb(DONG, user="ducthangho"), ["tac_gia"])):
            r.write_text(json.dumps(d), encoding="utf-8")
            kq = khong_nem(lambda: G().kiem_mien(mien, Path(thu), None))
            bang(kq == mong, f"readback {nhan}: {kq!r}")
        r.write_text(json.dumps(rb(DONG)), encoding="utf-8")
        if os.name == "posix":
            os.symlink(thu, Path(ng) / "lk")
            bang(G().kiem_mien(mien, Path(ng) / "lk", None) == ["readback"], "thu muc readback la symlink")


@ca
def a216_hop_le_theo_token():
    t = ten_tep("T-v3-pass")
    with ho_so_tam() as thu:
        bang(G().kiem_ho_so({"landed": True, "moc_gate_output": f"measured — {t}"}, thu) == [], "landed + duong hop le")
    with ho_so_tam("T-fail") as thu:
        vp = G().kiem_ho_so({"landed": True, "moc_gate_output": f"failed — {ten_tep('T-fail')}"}, thu)
        bang(vp == ["$: landed_khong_loi_khai_gate_output"], f"landed chi co failed: {vp}")


@ca
def a217_cli_tham_so_va_ma_thoat():
    tep = str(ROOT / FX["T-v3-pass"][0])
    for nhan, a, mong in (("khong doi so", (), 2), ("thieu --provenance", ("kiem-tep", tep), 2), ("--help", ("--help",), 0),
                          ("provenance vang", ("kiem-tep", tep, "--provenance", "/khong/co"), 2)):
        rc, ra = cli(*a)
        bang(rc == mong and "Traceback" not in ra and (mong == 0 or ra.startswith("LỖI THAM SỐ:")), f"{nhan}: rc={rc} {ra[-150:]}")
        if nhan == "--help":
            bang("Đối chiếu gate_output với tệp đánh giá và provenance (wp1236 r10)." in ra.splitlines(), ra)
        elif nhan == "provenance vang":
            bang(ra.splitlines() == ["LỖI THAM SỐ: tệp hoặc thư mục provenance vắng/không đọc được"], ra)
        else:
            bang(ra.splitlines()[0].startswith("LỖI THAM SỐ: the following arguments are required:"), ra)
    rc, ra = cli("kiem-tep", tep, "--provenance", str(ROOT / L / THU_MUC_THAT["T-v3-pass"]))
    bang(rc == 0 and ra.splitlines() == [
        f"passed {tep} -",
        "GIỚI HẠN: không đọc log thật; tệp đánh giá và provenance sửa tay được",
    ], f"dong ket qua: {ra!r}")
    rc, ra = cli("kiem-tep", str(ROOT / FX["T-skip"][0]), "--provenance", str(ROOT / L / THU_MUC_THAT["T-skip"]))
    bang(ra.splitlines()[0].endswith(" co_job_skipped"), f"dong ket qua co ly do: {ra.splitlines()[:1]}")
    with ho_so_tam() as thu:
        tot = thu.parent / "pr9001-thu-land-evidence.yaml"
        tot.write_text(f"landed: true\nmoc_gate_output: 'measured — {ten_tep('T-v3-pass')}'\n", encoding="utf-8")
        xau = thu.parent / "xau-land-evidence.yaml"
        xau.write_text("moc_gate_output: 'measured — khong-tep.txt'\n", encoding="utf-8")
        rc, ra = cli("kiem-ho-so", str(tot))
        bang(rc == 0 and f"DAT {tot} (0 vi phạm)" in ra, f"ho so sach: rc={rc} {ra[-200:]}")
        fallback = tot.with_name("pr9001-thu.yaml")
        shutil.copyfile(tot, fallback)
        rc, ra = cli("kiem-ho-so", str(fallback))
        bang(rc == 0 and f"DAT {fallback} (0 vi phạm)" in ra, f"ten provenance theo stem: {ra!r}")
        rc, ra = cli("kiem-ho-so", str(xau), str(tot))
        bang(rc == 1 and f"DO {xau} (1 vi phạm)" in ra and f"DAT {tot}" in ra, f"xau roi sach: rc={rc} {ra[-300:]}")


def _bang(ten, bien, mong):   # luật 4 r10: mỗi phần tử ma trận nghĩa một dòng — (nhãn, sửa tệp, sửa provenance)
    for nhan, ft, fp in bien:
        ky(kt(ten, ft, fp), *mong(nhan) if callable(mong) else mong, nhan)


@ca
def a120_ngu_phap_dong():   # r10 luật 4: ngữ pháp TỪNG dòng tệp đánh giá (regex khớp trọn; pilot c2d606b i1/i2/i4/i5/i7)
    t = (ROOT / FX["T-v3-pass"][0]).read_text(encoding="utf-8")
    h, i = t.split("\n")[0], dong_job(t, 2)
    hd = re.fullmatch(r"(# Danh gia Gate output run )(\d+)( attempt )(\d+)( head )([0-9a-f]{40})(.*\(danh_gia_gate\.py sha256 )([0-9a-f]{64})(\))", h)
    def dau(k, v):
        g = list(hd.groups()); g[k] = v
        return lambda x: x.replace(h, "".join(g), 1)
    _bang("T-v3-pass", [(f"dau {k} {v!r}", dau(k, v), None) for k, v in (
        (5, "g" * 40), (5, "a" * 39), (7, "g" * 64), (1, ""), (1, "1x"), (3, ""), (3, "x"),
        (6, hd[7].replace("(danh", "Xdanh")), (6, hd[7].replace("gate.py", "gateXpy")), (8, "X"))], ("not_measured", ["dau_tep_sai"]))
    def dj(a, b):
        return lambda x: sua_dong(x, i, lambda d: re.sub(a, b, d, count=1))
    _bang("T-v3-pass", [(f"job {a!r}->{b!r}", dj(a, b), None) for a, b in (
        (r"\[([^\]]*)\]", r"[\1]x]"), (r"log_sha256=[0-9a-f]{64}", "log_sha256=" + "g" * 64), (r"log_sha256=[0-9a-f]", "log_sha256="),
        (r"^JOB \d+", "JOB "), (r"^(JOB \d+ ).+?( \[)", r"\1\2"), (r"conclusion=\w+", "conclusion="), (r"conclusion=\w+", "conclusion=a-b"),
        (r"\] conclusion", "X conclusion"))], ("not_measured", ["dong_la"]))
    sk = [("cu", "JOB 777 job-them: skipped (khong tinh)"), ("v3", "JOB 777 job-them: skipped -> not_measured (khong suy pass)")]
    _bang("T-v3-pass", [(f"skip {dg} {a!r}", (lambda dong: lambda x: x + dong + "\n")(re.sub(a, b, d, count=1) if a else d + " thua"), None)
                        for dg, d in sk for a, b in (("JOB 777", "JOB "), ("job-them", ""), (r"\((khong)", r"X\1"), (r"\)$", "X"), ("", ""))],
          ("not_measured", ["dong_la"]))
    _bang("T-v3-pass", [(f"moc {a!r}", lambda x, a=a, b=b: doi_tong(x, re.sub(a, b, "MOC_GATE_OUTPUT: passed (39/39 job co dau hieu duong)")), None)
                        for a, b in ((r"\(39/", "(/"), (r"/39 ", "/ "), (r"\(39", "(x"), (r"/39 ", "/x "), (r"\(39", "X39"), (r"\)$", "X"))],
          ("not_measured", ["dong_la", "thieu_moc"]))


@ca
def a121_token_tep_khoa_landed():   # r10 luật 4: ngữ pháp token, tên tệp đánh giá, chuẩn hoá khoá, ba dạng landed
    bang([G().token("passed" + c + "x") for c in "—-(,.;: "] == ["passed"] * 8, "token: moi dau phan cach cho phep")
    bang([G().token(v) for v in ("1 passed", "passedx", "x passed", "pass — x")] == [None] * 4, "token: khop tu DAU chuoi, dung tap TOKEN")
    bang(G().kiem_ho_so({"gate_output": "pass — x"}, ROOT) == ["$.gate_output: dinh_dang_loi_khai"], "token ngoai tap la sai dinh dang")
    for v, mong in (("A/B_c.d-1/danh-gia-gate-output-1.txt", ["A/B_c.d-1/danh-gia-gate-output-1.txt"]), ("danh-gia-gate-output-.txt", []),
                    ("danh-gia-gate-output-1xtxt", []), ("danh-gia-gate-output-1a.txt", [])):
        bang(G().tep_danh_gia(v) == mong, f"tep_danh_gia({v!r}) = {G().tep_danh_gia(v)}")
    for doc, mong in (({"gate2output": "x"}, []), ({"gate_output_nguon_x": "y"}, ["$.gate_output_nguon_x"]),
                      ({"gate_output_nguon": {"gate_output": "z"}}, ["$.gate_output_nguon.gate_output"])):
        bang(sorted(d for d, _ in G().loi_khai(doc)) == mong, f"loi_khai({doc})")
    for doc, mong in (({"landed": 1}, False), ({"trang_thai_packet": {"landed": 1}}, False), ({"landed_20261120": {"landed": 1}}, False),
                      ({"landed_202611201": {"landed": True}}, False), ({"landed_123": {"landed": True}}, False),
                      ({"landed_abcdefgh": {"landed": True}}, False), ({"landed_20261120": {"landed": True}}, True)):
        bang(khong_nem(lambda: G().la_landed(doc)) is mong, f"la_landed({doc})")


@ca
def a122_mien_ma_tran():   # r10 luật 4: ngữ pháp dòng miễn, URL, head có/không, THỨ TỰ lý do (hai lỗi đồng thời)
    sai_os, sai_han = DONG.replace("ubuntu-latest", "windows-latest"), DONG.replace("2026-12-31", "2026-02-30")
    ok = f"owner_waived — {URL} {SHA}"
    with tempfile.TemporaryDirectory(prefix="godc_rb_") as thu:
        def f(body, chuoi=ok, head=None, **k):
            (Path(thu) / "readback-duyet-issuecomment-123.json").write_text(json.dumps(rb(body, **k)), encoding="utf-8")
            return khong_nem(lambda: G().kiem_mien(chuoi, Path(thu), head))
        for nhan, kq, mong in (
                ("dau dong co khoang trang", f("  " + DONG), []), ("duoi thua", f(DONG + " thua"), ["dong_mien"]),
                ("nhieu os", f(DONG.replace("os=ubuntu-latest", "os=windows-latest,ubuntu-24.04,ubuntu-latest")), []),
                ("os co cach", f(DONG.replace("os=ubuntu-latest", "os=ubuntu latest")), ["dong_mien"]),
                ("os rong", f(DONG.replace("os=ubuntu-latest", "os=")), ["dong_mien"]),
                ("sha khong hex", f(DONG.replace(SHA, "g" * 40), ok.replace(SHA, "g" * 40)), ["dong_mien"]),
                ("sha 39", f(DONG.replace(SHA, SHA[:39])), ["dong_mien"]),
                ("nam 3 so", f(DONG.replace("2026-", "226-")), ["dong_mien"]), ("thang 1 so", f(DONG.replace("-12-", "-1-")), ["dong_mien"]),
                ("ngay 1 so", f(DONG.replace("-31", "-3")), ["dong_mien"]), ("nam chu", f(DONG.replace("2026-", "abcd-")), ["dong_mien"]),
                ("thang chu", f(DONG.replace("-12-", "-1a-")), ["dong_mien"]), ("ngay chu", f(DONG.replace("-31", "-3a")), ["dong_mien"]),
                ("khong url", f(DONG, f"owner_waived — {SHA}"), ["url"]), ("url khong so", f(DONG, ok.replace("comment-123", "comment-")), ["url"]),
                ("url sai host", f(DONG, ok.replace("github.com", "githubXcom")), ["url"]), ("head rong", f(DONG, ok, ""), ["sha"]),
                ("html_url truoc tac_gia", f(DONG, html_url=URL + "9", author_association="MEMBER"), ["html_url"]),
                ("tac_gia truoc dong", f("khong dong", author_association="MEMBER"), ["tac_gia"]),
                ("han truoc os", f(sai_han.replace("ubuntu-latest", "windows-latest")), ["han"]),
                ("os truoc sha", f(sai_os, f"owner_waived — {URL}"), ["os"])):
            bang(kq == mong, f"mien ({nhan}): mong {mong}, duoc {kq!r}")
        vp = G().kiem_ho_so({"landed": True, "moc_gate_output": f"owner_waived — {SHA}"}, Path(thu))
        bang(vp == ["$.moc_gate_output: waiver_khong_co_can_cu:url", "$: landed_khong_loi_khai_gate_output"], f"ho so khong url: {vp}")


@ca
def a123_thu_tu_va_dinh_dang():   # r10 luật 4: thứ tự chốt K1/K8, labels nhiều phần tử, định dạng lý do nối bằng ","
    ky(kt("T-v3-pass", lambda x: x.replace("# Danh", "#Danh", 1).replace("\n", "\nx\ry\n", 1)), "not_measured", ["cr_le"], "cr_le truoc dau_tep")
    tf = (ROOT / FX["T-fail"][0]).read_text(encoding="utf-8")
    ft, fp = _them_skip("cu", [x for x in tf.split("\n") if x.startswith("MOC_GATE_OUTPUT")][0])
    ky(kt("T-fail", ft, fp), "failed", [], "failed truoc co_job_skipped")
    t = (ROOT / FX["T-v3-pass"][0]).read_text(encoding="utf-8")
    i = dong_job(t, 3)
    k = job_id(t.split("\n")[i])
    def nhan2(y):
        [q.update(labels=["a", "b"]) for q in y["moc"]["gate_output"]["jobs"] if q.get("job_id") == k]
    ky(kt("T-v3-pass", lambda x: sua_dong(x, i, lambda d: re.sub(r"\[[^\]]*\]", "[a,b]", d, count=1)), nhan2), "passed", [], "labels hai phan tu")
    def hai(x):
        d = x.split("\n")[i]
        return doi_tong(sua_dong(x, i, lambda z: z.replace(d.split("log_sha256=")[1][:64], "0" * 64)), "MOC_GATE_OUTPUT: passed (38/39 job co dau hieu duong)")
    with ho_so_tam() as thu:
        tp = thu / ten_tep("T-v3-pass")
        tp.write_text(hai(tp.read_text(encoding="utf-8")), encoding="utf-8", newline="")
        vp = G().kiem_ho_so({"moc_gate_output": f"measured — {ten_tep('T-v3-pass')}"}, thu)
        bang(len(vp) == 1 and vp[0].endswith(f":not_measured:log_sha_lech:{k},moc_lech"), f"ly do noi: {vp}")
        bang(G().kiem_ho_so({"moc_gate_output": "passed — khong tep"}, thu) == ["$.moc_gate_output: duong_khong_tep_danh_gia"], "passed khong tep")
        rc, ra = cli("kiem-tep", str(tp), "--provenance", str(thu))
        bang(rc == 3 and ra.splitlines()[0] == f"not_measured {tp} log_sha_lech:{k},moc_lech", f"cli ly do noi: {ra.splitlines()[:1]}")
        hs = thu.parent / "x-land-evidence.yaml"
        hs.write_text("moc_gate_output: 'measured — khong-tep.txt'\n", encoding="utf-8")
        rc, ra = cli("kiem-ho-so", str(hs))
        bang(ra.splitlines()[:2] == [f"VI_PHAM {hs} $.moc_gate_output: duong_khong_tep_danh_gia", f"DO {hs} (1 vi phạm)"], f"cli VI_PHAM: {ra[:300]}")


@ca
def a124_token_ascii_qua_ho_so():
    """Kiểm tiền tố và dấu phân cách qua token và qua hồ sơ."""
    from unicodedata import category

    ascii_day_du = tuple(map(chr, range(128)))
    dai_dien = _mau_loai_unicode("—")
    khoang_trang = []
    chu_va_so = []
    for ma in range(128, 0x110000):
        ky_tu = chr(ma)
        if ky_tu.isspace():
            khoang_trang.append(ky_tu)
        if category(ky_tu)[0] in "LN":
            chu_va_so.append(ky_tu)

    def kiem(gia_tri, mong, qua_ho_so):
        bang(G().token(gia_tri) == mong, f"token {gia_tri!r}: mong {mong!r}")
        if qua_ho_so:
            vp = G().kiem_ho_so({"gate_output": gia_tri}, ROOT)
            bang(vp == ([] if mong else ["$.gate_output: dinh_dang_loi_khai"]), f"ho so {gia_tri!r}: {vp}")

    for c in (*ascii_day_du, *dai_dien, *khoang_trang, "—"):
        bang_chung = c.isascii() or c in dai_dien or c == "—"
        kiem(c + "skipped", "skipped" if c in " \t" else None, bang_chung)
        kiem("skipped" + c + "x", "skipped" if c in " \t—-:(,.;" else None, bang_chung)

    for c in (*ascii_day_du, *dai_dien, *chu_va_so):
        bang_chung = c.isascii() or c in dai_dien or c in "ſK"
        for i, ky_tu in enumerate("skipped"):
            gia_tri = "skipped"[:i] + c + "skipped"[i + 1:]
            kiem(gia_tri, "skipped" if c.casefold() == ky_tu else None, bang_chung)

    for gia_tri, mong in (("ſkipped", "skipped"), ("skipped\n", "skipped"), ("skipped\u0085", None),
                         ("\u00a0skipped", None), ("skipped\nx", None), ("skipped\u2003x", None)):
        bang(G().token(gia_tri) == mong, f"token {gia_tri!r}: mong {mong!r}")
        vp = G().kiem_ho_so({"gate_output": gia_tri}, ROOT)
        bang(vp == ([] if mong else ["$.gate_output: dinh_dang_loi_khai"]), f"ho so {gia_tri!r}: {vp}")


@ca
def a125_ascii_dong_danh_gia():
    """Chữ số và hex ở từng trường, chữ thường ở kết luận."""
    from string import ascii_lowercase, digits, hexdigits
    hex_thuong = digits + hexdigits[10:16]
    mau = (
        "# Danh gia Gate output run {run} attempt {attempt} head {head} "
        "— (danh_gia_gate.py sha256 {bo_sinh})",
        "JOB {job} ten [nhan] conclusion={conclusion} log_sha256={log} -> passed: x",
        "JOB {skip_cu} x: skipped (khong tinh)",
        "JOB {skip_v3} y: skipped -> not_measured (khong suy pass)",
        "MOC_GATE_OUTPUT: passed ({dat}/{tong} job co dau hieu duong)",
    )
    goc = dict(run="10", attempt="20", head="a" * 40, bo_sinh="a" * 64,
               job="31", conclusion="success", log="a" * 64, skip_cu="42", skip_v3="53", dat="1", tong="2")
    from unicodedata import category

    cac_chu_so = []
    chu_va_so = []
    for ma in range(128, 0x110000):
        ky_tu = chr(ma)
        loai = category(ky_tu)
        if loai == "Nd":
            cac_chu_so.append(ky_tu)
        if loai[0] in "LN":
            chu_va_so.append(ky_tu)

    dai_dien = _mau_loai_unicode("", bo_loai=("Cs",))
    with tempfile.TemporaryDirectory(prefix="godc_danh_gia_") as tam:
        thu = Path(tam)
        tep = thu / "danh-gia-gate-output-10.txt"
        ho_so = {"gate_output": f"measured — {tep.name}"}
        for truong, lop in (
            ("run", digits), ("attempt", digits), ("head", hex_thuong), ("bo_sinh", hex_thuong),
            ("job", digits), ("conclusion", ascii_lowercase + "_"), ("log", hex_thuong),
            ("skip_cu", digits), ("skip_v3", digits), ("dat", digits), ("tong", digits),
        ):
            unicode_am = chu_va_so if truong == "conclusion" else cac_chu_so
            for c in (*map(chr, range(128)), *unicode_am, *dai_dien):
                du_lieu = dict(goc, **{truong: c + goc[truong][1:]})
                byte = "\n".join(dong.format_map(du_lieu) for dong in mau).encode()
                kq, ly_do = G().doc_danh_gia(byte)
                bang((kq is not None) == (c in lop), f"{truong} {c!r}: {ly_do}")
                if c.isascii() or c in dai_dien:
                    tep.write_bytes(byte)
                    ly = ",".join(ly_do or ["bo_sinh_la"])
                    vp = G().kiem_ho_so(ho_so, thu)
                    mong = [f"$.gate_output: danh_gia_khong_passed:{tep.name}:not_measured:{ly}"]
                    bang(vp == mong, f"ho so {truong} {c!r}: {vp}")

    for field in ("skip_cu", "skip_v3"):
        du_lieu = dict(goc, **{field: goc[field] + " café𐐀"})
        kq, ly = G().doc_danh_gia("\n".join(dong.format_map(du_lieu) for dong in mau).encode())
        bang(not ly and int(goc[field]) in kq["skip"], f"{field}: {ly}")


@ca
def a126_mien_ascii_qua_ho_so():
    """Đối chiếu URL, ngày và văn bản tự do với readback qua cả hai tuyến."""
    with tempfile.TemporaryDirectory(prefix="godc_ascii_") as tam:
        thu = Path(tam)
        tep = thu / "readback-duyet-issuecomment-123.json"
        def do(url, dong, ly_do):
            tep.write_text(json.dumps(rb(dong, html_url=url)), encoding="utf-8")
            khai = f"owner_waived — {url} {SHA}"
            bang(G().kiem_mien(khai, thu, None) == ly_do, f"mien {url!r}, {dong!r}")
            vp = G().kiem_ho_so({"gate_output": khai}, thu)
            mong = [f"$.gate_output: waiver_khong_co_can_cu:{x}" for x in ly_do]
            bang(vp == mong, f"ho so mien {url!r}, {dong!r}: {vp}")

        do(URL, DONG, [])
        do(URL, DONG.replace("ubuntu-latest", "ubuntu-latest,win7"), [])
        do(URL.replace("issues/", "issues/é"), DONG, ["url"])
        do(URL.replace("comment-123", "comment-１２３"), DONG, ["url"])
        do(URL, DONG.replace("2026-", "٢٠٢٦-"), ["dong_mien"])
        do(URL, DONG.replace("ubuntu-latest", "ubuntu-latest,ｗindows"), ["dong_mien"])
        do(URL, DONG.replace(SHA, "ａ" + SHA[1:]), ["dong_mien"])
        for ky_tu in " \t\n\r\v\f\x1c\x1d\x1e\x85\u2028\u2029":
            do(URL, DONG.replace("ly_do=", f"ly_do={ky_tu}"), ["dong_mien"])
        do(URL, DONG.split("ly_do=")[0] + "ly_do= han=2026-12-31", ["dong_mien"])
        do(URL, DONG.replace("ly_do=", "ly_do=x han=2025-01-01 "), [])
        for ky_tu in (*_mau_loai_unicode("\n\r\v\f\x1c\x1d\x1e\x85\u2028\u2029 \t"), "\x00", "\u200b"):
            do(URL, DONG.replace("ly_do=", f"ly_do={ky_tu}"), [])


@ca
def a133_lop_dong_mien_qua_ho_so():
    """Kiểm lớp ký tự trong URL và dòng miễn, rồi đối chiếu lý do qua hồ sơ."""
    from datetime import date
    from string import ascii_letters, ascii_lowercase, digits
    from unicodedata import category

    ascii_day_du = tuple(map(chr, range(128)))
    dai_dien = _mau_loai_unicode("")
    so_unicode = []
    chu_so_unicode = []
    for ma in range(128, 0x110000):
        ky_tu = chr(ma)
        loai = category(ky_tu)
        if loai == "Nd":
            so_unicode.append(ky_tu)
        if loai[0] in "LN":
            chu_so_unicode.append(ky_tu)

    with tempfile.TemporaryDirectory(prefix="godc_mien_") as tam:
        thu = Path(tam)
        tep = thu / "readback-duyet-issuecomment-123.json"

        def kiem(url, dong, ly_do):
            tep.write_text(json.dumps(rb(dong, html_url=url)), encoding="utf-8")
            khai = f"owner_waived — {url} {SHA}"
            bang(G().kiem_mien(khai, thu, None) == ly_do, f"mien {url!r}, {dong!r}: {ly_do}")
            vp = G().kiem_ho_so({"gate_output": khai}, thu)
            mong = [f"$.gate_output: waiver_khong_co_can_cu:{x}" for x in ly_do]
            bang(vp == mong, f"ho so mien {url!r}, {dong!r}: {vp}")

        for truong, lop, unicode_am in (
            ("url_path", ascii_letters + digits + "._~/%-", chu_so_unicode),
            ("url_id", digits, so_unicode),
            ("sha", digits + "abcdef", so_unicode),
            ("os", ascii_lowercase + digits + ",.-", chu_so_unicode),
            ("nam", digits, so_unicode),
            ("thang", digits, so_unicode),
            ("ngay", digits, so_unicode),
        ):
            for c in (*ascii_day_du, *dai_dien, *unicode_am):
                url, dong = URL, DONG
                dung_lop = c in lop
                if truong == "url_path":
                    url = URL.replace("/issues/", f"/issu{c}s/")
                elif truong == "url_id":
                    url = URL[:-3] + c + "23"
                elif truong == "sha":
                    dong = DONG.replace(SHA, c + SHA[1:])
                elif truong == "os":
                    dong = DONG.replace("ubuntu-latest", f"ubuntu-latest,{c}x")
                else:
                    ngay = {"nam": f"{c}026-12-31", "thang": f"2026-{c}2-31",
                            "ngay": f"2026-12-{c}1"}[truong]
                    dong = DONG.replace("2026-12-31", ngay)

                la_url = truong in ("url_path", "url_id")
                regex, dau_vao = (G().RE_URL, url) if la_url else (G().RE_MIEN, dong)
                bang(bool(regex.fullmatch(dau_vao)) == dung_lop, f"{truong} {c!r}: mong {dung_lop}")
                if not (c.isascii() or c in dai_dien):
                    continue
                if not dung_lop:
                    ly_do = ["url" if la_url else "dong_mien"]
                elif truong == "url_id" and c != "1":
                    ly_do = ["readback"]
                elif truong == "sha" and c != SHA[0]:
                    ly_do = ["sha"]
                else:
                    ly_do = []
                    if truong in ("nam", "thang", "ngay"):
                        try:
                            date.fromisoformat(ngay)
                        except ValueError:
                            ly_do = ["han"]
                kiem(url, dong, ly_do)


def _mau_loai_unicode(cam, bo_loai=()):
    """Một đại diện của mỗi loại Unicode trên tuyến và một ký tự ngoài BMP."""
    from unicodedata import category
    mau = {}
    for ma in range(128, 0x110000):
        ky_tu = chr(ma)
        loai = category(ky_tu)
        if ky_tu not in cam and loai not in bo_loai:
            mau.setdefault(loai, ky_tu)
    return (*mau.values(), "𐐀")


@ca
def a129_ten_job_lazy_qua_ho_so():
    tep_goc, prov_goc, *_ = FX["T-v3-pass"]
    txt = (ROOT / tep_goc).read_text(encoding="utf-8")
    vi_tri = dong_job(txt, 0)
    dong = txt.split("\n")[vi_tri]
    ma = job_id(dong)
    p = yaml.safe_load((ROOT / prov_goc).read_bytes())
    ten_goc = next(row["name"] for row in p["moc"]["gate_output"]["jobs"] if row["job_id"] == ma)
    tien_to = f"JOB {ma} "
    dau = tien_to + ten_goc
    bang(dong.startswith(dau + " ["), "fixture job khong co ten va hau to mong doi")
    duoi = dong[len(dau):]
    ten_tep_dg = Path(tep_goc).name
    loi_goc = "$.moc_gate_output: danh_gia_khong_passed:" + ten_tep_dg + ":not_measured:"

    def kiem(dong_moi, ten_mong, ly_do=""):
        def sua_prov(doc):
            if ten_mong is not None:
                next(row for row in doc["moc"]["gate_output"]["jobs"] if row["job_id"] == ma)["name"] = ten_mong
        with mini("T-v3-pass", lambda x: sua_dong(x, vi_tri, lambda _: dong_moi), sua_prov) as (tep, thu):
            dich = tep.rename(thu / ten_tep_dg)
            doc, ly = G().doc_danh_gia(dich.read_bytes())
            if ly_do:
                bang(doc is None and ly == [ly_do], f"doc job {dong_moi!r}: {ly}")
            else:
                bang(not ly and doc["jobs"][ma]["name"] == ten_mong, f"ten job lazy {dong_moi!r}: {doc}")
            vp = G().kiem_ho_so({"moc_gate_output": f"measured — {ten_tep_dg}"}, thu)
            bang(vp == ([loi_goc + ly_do] if ly_do else []), f"ho so lazy {dong_moi!r}: {vp}")

    kiem(dong, ten_goc)
    kiem(dau + " [khong khop]" + duoi, ten_goc + " [khong khop]")
    kiem(dong + duoi, ten_goc)
    kiem(tien_to + duoi.lstrip(), None, "dong_la")
    kiem(dau + duoi.replace("]", "]]", 1), None, "dong_la")
    kiem(dong + "\nloi", None, "dong_la")
    for ky_tu in _mau_loai_unicode("\r\n", {"Cs"}):
        kiem(tien_to + ky_tu + ten_goc + duoi + ky_tu, ky_tu + ten_goc)


@ca
def a130_tong_ket_qua_cong_ci():
    """Đo đầu ra main qua consumer CI thật, dùng ca/đột biến thu nhỏ."""
    import io
    import runpy
    from unittest.mock import patch

    cong = runpy.run_path(str(ROOT / ".claude/dev/ci_dang_ky_test.py"))
    path = "ops/gate_output_doi_chieu_test.py"
    mau = {path: cong["MOI"][path]}
    db = (("mot", "x", "y", "a"), ("chi_posix", "x", "z", "a"))
    for nen in ("posix", "nt"):
        windows = nen == "nt"
        for bien, ca_rc, mutant, chi_posix, tong_db in (
            ("dat", 0, "GIET", {"chi_posix"}, db),
            ("ca do", 3, "GIET", {"chi_posix"}, db),
            ("dot bien song", 0, "SONG_SOT", {"chi_posix"}, db),
            ("ten chi POSIX la", 0, "GIET", {"khong_ton_tai"}, db),
            ("mau so 0", 0, "GIET", set(), ()),
        ):
            output = io.StringIO()
            with patch.dict(main.__globals__, {"CA": {"a": None}, "DOT_BIEN": tong_db, "TU_KIEM": (),
                                               "CHI_POSIX": chi_posix,
                                               "chay_ca": lambda _: (ca_rc, "ca thu"),
                                               "chay_dot_bien": lambda *_: (mutant, "")}), \
                    patch.object(os, "name", nen), contextlib.redirect_stdout(output):
                rc = main([])
            text = output.getvalue()
            kiem = io.StringIO()
            with contextlib.redirect_stdout(kiem):
                do = cong["chay_moi"](moi=mau, cach_ly={}, chay_mot=lambda _: (rc, text),
                                     doc_moi_truong=lambda: None, doc_trong_ci=lambda: True,
                                     doc_nen_windows=lambda: windows)
                bang(cong["chay_moi"](moi=mau, cach_ly={}, chay_mot=lambda _: (0, text),
                                     doc_moi_truong=lambda: None, doc_trong_ci=lambda: True,
                                     doc_nen_windows=lambda: windows) == (bien != "dat"),
                     f"{nen}, {bien}: consumer khong nhin dung dau ra khi rc=0")
            bang((rc, do) == ((0, 0) if bien == "dat" else (1, 1)), f"{nen}, {bien}: {rc}, {kiem.getvalue()}")
            if bien == "dat":
                n = 1 if windows else 2
                bang(text.splitlines()[-4:] == ["CA: 1/1 dat", f"DOT BIEN: {n}/{n} bi giet dung ly do",
                                               "TU KIEM PHAN HANG: DAT (0 dot bien)", "TONG: DAT"], repr(text))


@ca
def a132_ascii_khoa_landed_qua_ho_so():
    """Kiểm tám vị trí chữ số trong khoá landed và vi phạm của hồ sơ."""
    ngay = "20261120"
    dai_dien = _mau_loai_unicode("")
    chu_so_unicode = tuple(chr(ma) for ma in range(128, 0x110000) if chr(ma).isdecimal())
    for vi_tri in range(len(ngay)):
        for ky_tu in (*map(chr, range(128)), *dai_dien, *chu_so_unicode):
            khoa = "landed_" + ngay[:vi_tri] + ky_tu + ngay[vi_tri + 1:]
            ho_so = {khoa: {"landed": True}}
            mong = ky_tu in "0123456789"
            bang(G().la_landed(ho_so) is mong, f"khoa {khoa!r}: mong {mong}")
            if ky_tu.isascii() or ky_tu in dai_dien:
                vp = G().kiem_ho_so(ho_so, ROOT)
                bang(vp == (["$: landed_khong_loi_khai_gate_output"] if mong else []), f"khoa {khoa!r}: {vp}")


@ca
def a131_ten_tep_co_Z():
    ten = Path(FX["T-v3-pass"][0]).name
    tham_chieu = f"Z/{ten}"
    with mini("T-v3-pass") as (tep, thu):
        (thu / "Z").mkdir()
        tep.rename(thu / tham_chieu)
        loi_khai = f"measured — {tham_chieu}"
        bang(G().tep_danh_gia(loi_khai) == [tham_chieu], "ten tep can giu Z")
        bang(G().kiem_ho_so({"moc_gate_output": loi_khai}, thu) == [], "ho so co tep trong Z")


@ca
def a134_lop_dong_ten_tep_qua_ho_so():
    from string import ascii_letters, digits
    from unicodedata import category

    dai_dien = _mau_loai_unicode("")
    ten = "danh-gia-gate-output-123.txt"
    with tempfile.TemporaryDirectory(prefix="godc_ten_tep_") as tam:
        for vi_tri in ("thu_muc", "run"):
            for ma in range(0x110000):
                c = chr(ma)
                qua_ho_so = c.isascii() or c in dai_dien
                if not qua_ho_so and not (category(c)[0] in "LN" if vi_tri == "thu_muc" else c.isdecimal()):
                    continue
                if vi_tri == "thu_muc":
                    tham_chieu = f"x{c}x/{ten}"
                    mong = [tham_chieu if c in ascii_letters + digits + "_./-" else f"x/{ten}"]
                else:
                    tham_chieu = ten.replace("123", c + "23")
                    mong = [tham_chieu] if c in digits else []
                khai = f"measured — {tham_chieu}"
                bang(G().tep_danh_gia(khai) == mong, f"tep {tham_chieu!r}: mong {mong!r}")
                if qua_ho_so:
                    vp = G().kiem_ho_so({"gate_output": khai}, Path(tam))
                    ly = f"tep_danh_gia_khong_hop_le:{mong[0]}" if mong else "duong_khong_tep_danh_gia"
                    bang(vp == [f"$.gate_output: {ly}"], f"ho so {tham_chieu!r}: {vp}")


BANG_O_R11 = r"""{
"chieu": {"fixture":"mỗi vi phạm của kiem_ho_so: bỏ tiền tố '$.moc_gate_output: ', thay ':<tên tệp đánh giá>:' bằng ':'","la_fixture":"[trạng thái, danh sách lý do] của kiem_tep","la_mien":"danh sách lý do của kiem_mien (ngoại lệ ⇒ đỏ)","mien":"mỗi vi phạm của kiem_ho_so: phần sau 'waiver_khong_co_can_cu:'"},
"hat_giong": {"fixture":{"T-skip":{"ho_so":{"moc_gate_output":"measured — <tên tệp đánh giá tương đối thư mục>"},"provenance":"ops/land/pr1344-wp1343-provenance/ci/provenance.yaml","provenance_sha256":"30a2bfd3c2f638d5ea2acb6c473f92315641cca260f69269f5d32008280b175a","tep":"ops/land/pr1344-wp1343-provenance/danh-gia-gate-output-43969906464.txt","tep_sha256":"88c23b14e6de89270a42e36db551821b01ba22d5f5386096e020640238e31ecc","thu_muc":"ops/land/pr1344-wp1343-provenance"},"T-v3-pass":{"ho_so":{"moc_gate_output":"measured — <tên tệp đánh giá tương đối thư mục>"},"provenance":"ops/land/pr1440-wp1319-provenance/ci-provenance-44669622916/provenance.yaml","provenance_sha256":"d749903c0613a1120953c781ef295aa16fae2ee5c55e15d8266fb1956062f57e","tep":"ops/land/pr1440-wp1319-provenance/danh-gia-gate-output-44669622916.txt","tep_sha256":"452024d7e9bd5d589f3d65bcef9f3e67a527f234c63dd4aa7f2adcd7173013bf","thu_muc":"ops/land/pr1440-wp1319-provenance"}},"mien":{"dong":"mien_gate_output: d8cf2ab57f9f25a93cefedcebfb315826b6b78fe os=ubuntu-latest ly_do=job huy theo chi thi han=2026-12-31","ho_so":{"gate_output":"<loi_khai>"},"loi_khai":"owner_waived — {url} {sha}","loi_khai_head":"owner_waived — {url}","readback":{"author_association":"OWNER","body":"mien_gate_output: d8cf2ab57f9f25a93cefedcebfb315826b6b78fe os=ubuntu-latest ly_do=job huy theo chi thi han=2026-12-31","html_url":"https://github.com/ducthangho/tra-luat/issues/1236#issuecomment-123","user":{"login":"ducthangho"}},"sha":"d8cf2ab57f9f25a93cefedcebfb315826b6b78fe","ten_readback":"readback-duyet-issuecomment-123.json","url":"https://github.com/ducthangho/tra-luat/issues/1236#issuecomment-123"}},
"o": [
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_0"],"id":"schema:H1","la":["not_measured",["provenance_0"]],"ops":[["prov",["schema"],"CI_PROVENANCE/1"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_0"],"id":"schema:H2","la":["not_measured",["provenance_0"]],"ops":[["prov",["schema"]," ci_provenance/1"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_0"],"id":"schema:H3","la":["not_measured",["provenance_0"]],"ops":[["prov",["schema"],"ci_provenance/1 "]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_0"],"id":"schema:H4","la":["not_measured",["provenance_0"]],"ops":[["prov",["schema"],"ｃi_provenance/1"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_0"],"id":"schema:H6a","la":["not_measured",["provenance_0"]],"ops":[["prov",["schema"],"xci_provenance/1"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_0"],"id":"schema:H6b","la":["not_measured",["provenance_0"]],"ops":[["prov",["schema"],"ci_provenance/1x"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_0"],"id":"run.head_sha:H1","la":["not_measured",["provenance_0"]],"ops":[["prov",["moc","run","head_sha"],"D8CF2AB57F9F25A93CEFEDCEBFB315826B6B78FE"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_0"],"id":"run.head_sha:H2","la":["not_measured",["provenance_0"]],"ops":[["prov",["moc","run","head_sha"]," d8cf2ab57f9f25a93cefedcebfb315826b6b78fe"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_0"],"id":"run.head_sha:H3","la":["not_measured",["provenance_0"]],"ops":[["prov",["moc","run","head_sha"],"d8cf2ab57f9f25a93cefedcebfb315826b6b78fe "]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_0"],"id":"run.head_sha:H4","la":["not_measured",["provenance_0"]],"ops":[["prov",["moc","run","head_sha"],"ｄ8cf2ab57f9f25a93cefedcebfb315826b6b78fe"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_0"],"id":"run.head_sha:H6a","la":["not_measured",["provenance_0"]],"ops":[["prov",["moc","run","head_sha"],"xd8cf2ab57f9f25a93cefedcebfb315826b6b78fe"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_0"],"id":"run.head_sha:H6b","la":["not_measured",["provenance_0"]],"ops":[["prov",["moc","run","head_sha"],"d8cf2ab57f9f25a93cefedcebfb315826b6b78fex"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:khong_phai_run_land"],"id":"run.event:H1","la":["not_measured",["khong_phai_run_land"]],"ops":[["prov",["moc","run","event"],"PUSH"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:khong_phai_run_land"],"id":"run.event:H2","la":["not_measured",["khong_phai_run_land"]],"ops":[["prov",["moc","run","event"]," push"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:khong_phai_run_land"],"id":"run.event:H3","la":["not_measured",["khong_phai_run_land"]],"ops":[["prov",["moc","run","event"],"push "]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:khong_phai_run_land"],"id":"run.event:H4","la":["not_measured",["khong_phai_run_land"]],"ops":[["prov",["moc","run","event"],"ｐush"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:khong_phai_run_land"],"id":"run.event:H6a","la":["not_measured",["khong_phai_run_land"]],"ops":[["prov",["moc","run","event"],"xpush"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:khong_phai_run_land"],"id":"run.event:H6b","la":["not_measured",["khong_phai_run_land"]],"ops":[["prov",["moc","run","event"],"pushx"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:khong_phai_run_land"],"id":"run.loi_khai_rest_path:H1","la":["not_measured",["khong_phai_run_land"]],"ops":[["prov",["moc","run","loi_khai_rest_path"],".GITHUB/WORKFLOWS/CI.YML"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:khong_phai_run_land"],"id":"run.loi_khai_rest_path:H2","la":["not_measured",["khong_phai_run_land"]],"ops":[["prov",["moc","run","loi_khai_rest_path"]," .github/workflows/ci.yml"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:khong_phai_run_land"],"id":"run.loi_khai_rest_path:H3","la":["not_measured",["khong_phai_run_land"]],"ops":[["prov",["moc","run","loi_khai_rest_path"],".github/workflows/ci.yml "]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:khong_phai_run_land"],"id":"run.loi_khai_rest_path:H4","la":["not_measured",["khong_phai_run_land"]],"ops":[["prov",["moc","run","loi_khai_rest_path"],".ｇithub/workflows/ci.yml"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:khong_phai_run_land"],"id":"run.loi_khai_rest_path:H6a","la":["not_measured",["khong_phai_run_land"]],"ops":[["prov",["moc","run","loi_khai_rest_path"],"x.github/workflows/ci.yml"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:khong_phai_run_land"],"id":"run.loi_khai_rest_path:H6b","la":["not_measured",["khong_phai_run_land"]],"ops":[["prov",["moc","run","loi_khai_rest_path"],".github/workflows/ci.ymlx"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"run.trang_thai:H1","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["moc","run","trang_thai"],"PASSED"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"run.trang_thai:H2","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["moc","run","trang_thai"]," passed"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"run.trang_thai:H3","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["moc","run","trang_thai"],"passed "]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"run.trang_thai:H4","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["moc","run","trang_thai"],"ｐassed"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"run.trang_thai:H6a","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["moc","run","trang_thai"],"xpassed"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"run.trang_thai:H6b","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["moc","run","trang_thai"],"passedx"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"tap_jobs.trang_thai:H1","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["moc","gate_output","tap_jobs","trang_thai"],"PASSED"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"tap_jobs.trang_thai:H2","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["moc","gate_output","tap_jobs","trang_thai"]," passed"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"tap_jobs.trang_thai:H3","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["moc","gate_output","tap_jobs","trang_thai"],"passed "]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"tap_jobs.trang_thai:H4","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["moc","gate_output","tap_jobs","trang_thai"],"ｐassed"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"tap_jobs.trang_thai:H6a","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["moc","gate_output","tap_jobs","trang_thai"],"xpassed"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"tap_jobs.trang_thai:H6b","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["moc","gate_output","tap_jobs","trang_thai"],"passedx"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"checkout.passed:H1","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["@checkout",136067289163,"trang_thai"],"PASSED"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"checkout.passed:H2","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["@checkout",136067289163,"trang_thai"]," passed"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"checkout.passed:H3","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["@checkout",136067289163,"trang_thai"],"passed "]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"checkout.passed:H4","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["@checkout",136067289163,"trang_thai"],"ｐassed"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"checkout.passed:H6a","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["@checkout",136067289163,"trang_thai"],"xpassed"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"checkout.passed:H6b","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["@checkout",136067289163,"trang_thai"],"passedx"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.name:H1","la":["not_measured",["job_lech:136067289163"]],"ops":[["prov",["@job",136067289163,"name"],"GATE-CONG-CU (UBUNTU-LATEST, 1)"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.name:H2","la":["not_measured",["job_lech:136067289163"]],"ops":[["prov",["@job",136067289163,"name"]," gate-cong-cu (ubuntu-latest, 1)"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.name:H3","la":["not_measured",["job_lech:136067289163"]],"ops":[["prov",["@job",136067289163,"name"],"gate-cong-cu (ubuntu-latest, 1) "]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.name:H4","la":["not_measured",["job_lech:136067289163"]],"ops":[["prov",["@job",136067289163,"name"],"ｇate-cong-cu (ubuntu-latest, 1)"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.name:H6a","la":["not_measured",["job_lech:136067289163"]],"ops":[["prov",["@job",136067289163,"name"],"xgate-cong-cu (ubuntu-latest, 1)"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.name:H6b","la":["not_measured",["job_lech:136067289163"]],"ops":[["prov",["@job",136067289163,"name"],"gate-cong-cu (ubuntu-latest, 1)x"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.conclusion:H1","la":["not_measured",["job_lech:136067289163"]],"ops":[["prov",["@job",136067289163,"conclusion"],"SUCCESS"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.conclusion:H2","la":["not_measured",["job_lech:136067289163"]],"ops":[["prov",["@job",136067289163,"conclusion"]," success"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.conclusion:H3","la":["not_measured",["job_lech:136067289163"]],"ops":[["prov",["@job",136067289163,"conclusion"],"success "]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.conclusion:H4","la":["not_measured",["job_lech:136067289163"]],"ops":[["prov",["@job",136067289163,"conclusion"],"ｓuccess"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.conclusion:H6a","la":["not_measured",["job_lech:136067289163"]],"ops":[["prov",["@job",136067289163,"conclusion"],"xsuccess"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.conclusion:H6b","la":["not_measured",["job_lech:136067289163"]],"ops":[["prov",["@job",136067289163,"conclusion"],"successx"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.labels_phan_tu:H1","la":["not_measured",["job_lech:136067289163"]],"ops":[["prov",["@job",136067289163,"labels",0],"UBUNTU-LATEST"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.labels_phan_tu:H2","la":["not_measured",["job_lech:136067289163"]],"ops":[["prov",["@job",136067289163,"labels",0]," ubuntu-latest"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.labels_phan_tu:H3","la":["not_measured",["job_lech:136067289163"]],"ops":[["prov",["@job",136067289163,"labels",0],"ubuntu-latest "]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.labels_phan_tu:H4","la":["not_measured",["job_lech:136067289163"]],"ops":[["prov",["@job",136067289163,"labels",0],"ｕbuntu-latest"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.labels_phan_tu:H6a","la":["not_measured",["job_lech:136067289163"]],"ops":[["prov",["@job",136067289163,"labels",0],"xubuntu-latest"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.labels_phan_tu:H6b","la":["not_measured",["job_lech:136067289163"]],"ops":[["prov",["@job",136067289163,"labels",0],"ubuntu-latestx"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:log_sha_lech:136067289163"],"id":"log.sha256:H1","la":["not_measured",["log_sha_lech:136067289163"]],"ops":[["prov",["log_day_du",136067289163,"sha256"],"52230A835CD8D5E546575CB978C3E2E78F2400F5381544BE5E751D8B00EE2466"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:log_sha_lech:136067289163"],"id":"log.sha256:H2","la":["not_measured",["log_sha_lech:136067289163"]],"ops":[["prov",["log_day_du",136067289163,"sha256"]," 52230a835cd8d5e546575cb978c3e2e78f2400f5381544be5e751d8b00ee2466"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:log_sha_lech:136067289163"],"id":"log.sha256:H3","la":["not_measured",["log_sha_lech:136067289163"]],"ops":[["prov",["log_day_du",136067289163,"sha256"],"52230a835cd8d5e546575cb978c3e2e78f2400f5381544be5e751d8b00ee2466 "]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:log_sha_lech:136067289163"],"id":"log.sha256:H4","la":["not_measured",["log_sha_lech:136067289163"]],"ops":[["prov",["log_day_du",136067289163,"sha256"],"５2230a835cd8d5e546575cb978c3e2e78f2400f5381544be5e751d8b00ee2466"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:log_sha_lech:136067289163"],"id":"log.sha256:H6a","la":["not_measured",["log_sha_lech:136067289163"]],"ops":[["prov",["log_day_du",136067289163,"sha256"],"x52230a835cd8d5e546575cb978c3e2e78f2400f5381544be5e751d8b00ee2466"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:log_sha_lech:136067289163"],"id":"log.sha256:H6b","la":["not_measured",["log_sha_lech:136067289163"]],"ops":[["prov",["log_day_du",136067289163,"sha256"],"52230a835cd8d5e546575cb978c3e2e78f2400f5381544be5e751d8b00ee2466x"]]},
{"fx":"T-skip","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"checkout.skipped:H1","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["@checkout",133659160050,"trang_thai"],"SKIPPED"]]},
{"fx":"T-skip","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"checkout.skipped:H2","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["@checkout",133659160050,"trang_thai"]," skipped"]]},
{"fx":"T-skip","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"checkout.skipped:H3","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["@checkout",133659160050,"trang_thai"],"skipped "]]},
{"fx":"T-skip","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"checkout.skipped:H4","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["@checkout",133659160050,"trang_thai"],"ｓkipped"]]},
{"fx":"T-skip","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"checkout.skipped:H6a","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["@checkout",133659160050,"trang_thai"],"xskipped"]]},
{"fx":"T-skip","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du"],"id":"checkout.skipped:H6b","la":["not_measured",["provenance_chua_du"]],"ops":[["prov",["@checkout",133659160050,"trang_thai"],"skippedx"]]},
{"fx":"T-skip","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du,tap_job_lech,tap_skip_lech"],"id":"job.conclusion_skipped:H1","la":["not_measured",["provenance_chua_du","tap_job_lech","tap_skip_lech"]],"ops":[["prov",["@job",133659160050,"conclusion"],"SKIPPED"]]},
{"fx":"T-skip","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du,tap_job_lech,tap_skip_lech"],"id":"job.conclusion_skipped:H2","la":["not_measured",["provenance_chua_du","tap_job_lech","tap_skip_lech"]],"ops":[["prov",["@job",133659160050,"conclusion"]," skipped"]]},
{"fx":"T-skip","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du,tap_job_lech,tap_skip_lech"],"id":"job.conclusion_skipped:H3","la":["not_measured",["provenance_chua_du","tap_job_lech","tap_skip_lech"]],"ops":[["prov",["@job",133659160050,"conclusion"],"skipped "]]},
{"fx":"T-skip","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du,tap_job_lech,tap_skip_lech"],"id":"job.conclusion_skipped:H4","la":["not_measured",["provenance_chua_du","tap_job_lech","tap_skip_lech"]],"ops":[["prov",["@job",133659160050,"conclusion"],"ｓkipped"]]},
{"fx":"T-skip","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du,tap_job_lech,tap_skip_lech"],"id":"job.conclusion_skipped:H6a","la":["not_measured",["provenance_chua_du","tap_job_lech","tap_skip_lech"]],"ops":[["prov",["@job",133659160050,"conclusion"],"xskipped"]]},
{"fx":"T-skip","ho_so":["danh_gia_khong_passed:not_measured:provenance_chua_du,tap_job_lech,tap_skip_lech"],"id":"job.conclusion_skipped:H6b","la":["not_measured",["provenance_chua_du","tap_job_lech","tap_skip_lech"]],"ops":[["prov",["@job",133659160050,"conclusion"],"skippedx"]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:check_bat_buoc:gate-ops (ubuntu-latest)"],"id":"check_bat_buoc.ten:H1","la":["not_measured",["check_bat_buoc:gate-ops (ubuntu-latest)"]],"ops":[["prov",["@job",136067289134,"name"],"GATE-OPS (UBUNTU-LATEST)"],["tep","JOB 136067289134 gate-ops (ubuntu-latest) [","JOB 136067289134 GATE-OPS (UBUNTU-LATEST) ["]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:check_bat_buoc:gate-ops (ubuntu-latest)"],"id":"check_bat_buoc.ten:H2","la":["not_measured",["check_bat_buoc:gate-ops (ubuntu-latest)"]],"ops":[["prov",["@job",136067289134,"name"]," gate-ops (ubuntu-latest)"],["tep","JOB 136067289134 gate-ops (ubuntu-latest) [","JOB 136067289134  gate-ops (ubuntu-latest) ["]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:check_bat_buoc:gate-ops (ubuntu-latest)"],"id":"check_bat_buoc.ten:H3","la":["not_measured",["check_bat_buoc:gate-ops (ubuntu-latest)"]],"ops":[["prov",["@job",136067289134,"name"],"gate-ops (ubuntu-latest) "],["tep","JOB 136067289134 gate-ops (ubuntu-latest) [","JOB 136067289134 gate-ops (ubuntu-latest)  ["]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:check_bat_buoc:gate-ops (ubuntu-latest)"],"id":"check_bat_buoc.ten:H4","la":["not_measured",["check_bat_buoc:gate-ops (ubuntu-latest)"]],"ops":[["prov",["@job",136067289134,"name"],"ｇate-ops (ubuntu-latest)"],["tep","JOB 136067289134 gate-ops (ubuntu-latest) [","JOB 136067289134 ｇate-ops (ubuntu-latest) ["]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:check_bat_buoc:gate-ops (ubuntu-latest)"],"id":"check_bat_buoc.ten:H6a","la":["not_measured",["check_bat_buoc:gate-ops (ubuntu-latest)"]],"ops":[["prov",["@job",136067289134,"name"],"xgate-ops (ubuntu-latest)"],["tep","JOB 136067289134 gate-ops (ubuntu-latest) [","JOB 136067289134 xgate-ops (ubuntu-latest) ["]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:check_bat_buoc:gate-ops (ubuntu-latest)"],"id":"check_bat_buoc.ten:H6b","la":["not_measured",["check_bat_buoc:gate-ops (ubuntu-latest)"]],"ops":[["prov",["@job",136067289134,"name"],"gate-ops (ubuntu-latest)x"],["tep","JOB 136067289134 gate-ops (ubuntu-latest) [","JOB 136067289134 gate-ops (ubuntu-latest)x ["]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.labels_day:thu_tu","la":["not_measured",["job_lech:136067289163"]],"ops":[["tep","JOB 136067289163 gate-cong-cu (ubuntu-latest, 1) [ubuntu-latest]","JOB 136067289163 gate-cong-cu (ubuntu-latest, 1) [a,b]"],["prov",["@job",136067289163,"labels"],["b","a"]]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.labels_day:lap","la":["not_measured",["job_lech:136067289163"]],"ops":[["tep","JOB 136067289163 gate-cong-cu (ubuntu-latest, 1) [ubuntu-latest]","JOB 136067289163 gate-cong-cu (ubuntu-latest, 1) [a,b]"],["prov",["@job",136067289163,"labels"],["a","b","b"]]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.labels_day:thieu","la":["not_measured",["job_lech:136067289163"]],"ops":[["tep","JOB 136067289163 gate-cong-cu (ubuntu-latest, 1) [ubuntu-latest]","JOB 136067289163 gate-cong-cu (ubuntu-latest, 1) [a,b]"],["prov",["@job",136067289163,"labels"],["a"]]]},
{"fx":"T-v3-pass","ho_so":[],"id":"job.labels_day:doi_chung","la":["passed",[]],"ops":[["tep","JOB 136067289163 gate-cong-cu (ubuntu-latest, 1) [ubuntu-latest]","JOB 136067289163 gate-cong-cu (ubuntu-latest, 1) [a,b]"],["prov",["@job",136067289163,"labels"],["a","b"]]]},
{"fx":"T-v3-pass","ho_so":["danh_gia_khong_passed:not_measured:job_lech:136067289163"],"id":"job.name:H5","la":["not_measured",["job_lech:136067289163"]],"ops":[["prov",["@job",136067289163,"name"],"gate-cong-cu (ubuntu-latest, 1)é"],["tep","JOB 136067289163 gate-cong-cu (ubuntu-latest, 1) [","JOB 136067289163 gate-cong-cu (ubuntu-latest, 1)é ["]]},
{"ho_so":["html_url"],"id":"readback.html_url:H1","la":["html_url"],"mien":{"readback":["html_url","HTTPS://GITHUB.COM/DUCTHANGHO/TRA-LUAT/ISSUES/1236#ISSUECOMMENT-123"]}},
{"ho_so":["html_url"],"id":"readback.html_url:H2","la":["html_url"],"mien":{"readback":["html_url"," https://github.com/ducthangho/tra-luat/issues/1236#issuecomment-123"]}},
{"ho_so":["html_url"],"id":"readback.html_url:H3","la":["html_url"],"mien":{"readback":["html_url","https://github.com/ducthangho/tra-luat/issues/1236#issuecomment-123 "]}},
{"ho_so":["html_url"],"id":"readback.html_url:H4","la":["html_url"],"mien":{"readback":["html_url","ｈttps://github.com/ducthangho/tra-luat/issues/1236#issuecomment-123"]}},
{"ho_so":["html_url"],"id":"readback.html_url:H6a","la":["html_url"],"mien":{"readback":["html_url","xhttps://github.com/ducthangho/tra-luat/issues/1236#issuecomment-123"]}},
{"ho_so":["html_url"],"id":"readback.html_url:H6b","la":["html_url"],"mien":{"readback":["html_url","https://github.com/ducthangho/tra-luat/issues/1236#issuecomment-123x"]}},
{"ho_so":["tac_gia"],"id":"readback.login:H1","la":["tac_gia"],"mien":{"readback":["user.login","DUCTHANGHO"]}},
{"ho_so":["tac_gia"],"id":"readback.login:H2","la":["tac_gia"],"mien":{"readback":["user.login"," ducthangho"]}},
{"ho_so":["tac_gia"],"id":"readback.login:H3","la":["tac_gia"],"mien":{"readback":["user.login","ducthangho "]}},
{"ho_so":["tac_gia"],"id":"readback.login:H4","la":["tac_gia"],"mien":{"readback":["user.login","ｄucthangho"]}},
{"ho_so":["tac_gia"],"id":"readback.login:H6a","la":["tac_gia"],"mien":{"readback":["user.login","xducthangho"]}},
{"ho_so":["tac_gia"],"id":"readback.login:H6b","la":["tac_gia"],"mien":{"readback":["user.login","ducthanghox"]}},
{"ho_so":["tac_gia"],"id":"readback.author_association:H1","la":["tac_gia"],"mien":{"readback":["author_association","owner"]}},
{"ho_so":["tac_gia"],"id":"readback.author_association:H2","la":["tac_gia"],"mien":{"readback":["author_association"," OWNER"]}},
{"ho_so":["tac_gia"],"id":"readback.author_association:H3","la":["tac_gia"],"mien":{"readback":["author_association","OWNER "]}},
{"ho_so":["tac_gia"],"id":"readback.author_association:H4","la":["tac_gia"],"mien":{"readback":["author_association","ＯWNER"]}},
{"ho_so":["tac_gia"],"id":"readback.author_association:H6a","la":["tac_gia"],"mien":{"readback":["author_association","xOWNER"]}},
{"ho_so":["tac_gia"],"id":"readback.author_association:H6b","la":["tac_gia"],"mien":{"readback":["author_association","OWNERx"]}},
{"ho_so":["dong_mien"],"id":"mien.os:H1","la":["dong_mien"],"mien":{"dong":["ubuntu-latest","UBUNTU-LATEST"]}},
{"ho_so":["dong_mien"],"id":"mien.os:H2","la":["dong_mien"],"mien":{"dong":["ubuntu-latest"," ubuntu-latest"]}},
{"ho_so":["dong_mien"],"id":"mien.os:H3","la":["dong_mien"],"mien":{"dong":["ubuntu-latest","ubuntu-latest "]}},
{"ho_so":["dong_mien"],"id":"mien.os:H4","la":["dong_mien"],"mien":{"dong":["ubuntu-latest","ｕbuntu-latest"]}},
{"ho_so":["os"],"id":"mien.os:H6a","la":["os"],"mien":{"dong":["ubuntu-latest","xubuntu-latest"]}},
{"ho_so":["os"],"id":"mien.os:H6b","la":["os"],"mien":{"dong":["ubuntu-latest","ubuntu-latestx"]}},
{"ho_so":null,"id":"mien.head:H1","la":["sha"],"mien":{"head":"D8CF2AB57F9F25A93CEFEDCEBFB315826B6B78FE"}},
{"ho_so":["sha"],"id":"mien.sha_loi_khai:H1","la":["sha"],"mien":{"loi_khai_sha":"D8CF2AB57F9F25A93CEFEDCEBFB315826B6B78FE"}},
{"ho_so":null,"id":"mien.head:H2","la":["sha"],"mien":{"head":" d8cf2ab57f9f25a93cefedcebfb315826b6b78fe"}},
{"ho_so":[],"id":"mien.sha_loi_khai:H2","la":[],"mien":{"loi_khai_sha":" d8cf2ab57f9f25a93cefedcebfb315826b6b78fe"}},
{"ho_so":null,"id":"mien.head:H3","la":["sha"],"mien":{"head":"d8cf2ab57f9f25a93cefedcebfb315826b6b78fe "}},
{"ho_so":[],"id":"mien.sha_loi_khai:H3","la":[],"mien":{"loi_khai_sha":"d8cf2ab57f9f25a93cefedcebfb315826b6b78fe "}},
{"ho_so":null,"id":"mien.head:H4","la":["sha"],"mien":{"head":"ｄ8cf2ab57f9f25a93cefedcebfb315826b6b78fe"}},
{"ho_so":["sha"],"id":"mien.sha_loi_khai:H4","la":["sha"],"mien":{"loi_khai_sha":"ｄ8cf2ab57f9f25a93cefedcebfb315826b6b78fe"}},
{"ho_so":null,"id":"mien.head:H6a","la":["sha"],"mien":{"head":"xd8cf2ab57f9f25a93cefedcebfb315826b6b78fe"}},
{"ho_so":[],"id":"mien.sha_loi_khai:H6a","la":[],"mien":{"loi_khai_sha":"xd8cf2ab57f9f25a93cefedcebfb315826b6b78fe"}},
{"ho_so":null,"id":"mien.head:H6b","la":["sha"],"mien":{"head":"d8cf2ab57f9f25a93cefedcebfb315826b6b78fex"}},
{"ho_so":[],"id":"mien.sha_loi_khai:H6b","la":[],"mien":{"loi_khai_sha":"d8cf2ab57f9f25a93cefedcebfb315826b6b78fex"}}
]
}"""


@ca
def a127_bang_o_dong_bang():
    """Chạy 125 ô đặc tả trên hàm lá và đối chiếu hồ sơ."""
    from copy import deepcopy
    from hashlib import sha256

    bang_o = json.loads(BANG_O_R11)
    byte_chuan = json.dumps(bang_o, ensure_ascii=False, sort_keys=True).encode()
    bang(sha256(byte_chuan).hexdigest() == "628e27046ab4ba7a7b3cf31eb65ded9b88c718c5bfd067401d12b60d2c21b857",
         "bang o dong bang lech SHA-256")
    hat_giong = bang_o["hat_giong"]
    fixtures = {}
    for ten, fx in hat_giong["fixture"].items():
        tep, prov = ((ROOT / fx[k]).read_bytes() for k in ("tep", "provenance"))
        for k, b in (("tep", tep), ("provenance", prov)):
            bang(sha256(b).hexdigest() == fx[f"{k}_sha256"], f"{ten}: {k} lech SHA-256")
        fixtures[ten] = (Path(fx["tep"]).name, tep.decode(), yaml.safe_load(prov), fx["ho_so"])

    for o in bang_o["o"]:
        with tempfile.TemporaryDirectory(prefix="godc_o_") as tam:
            thu = Path(tam)
            if "mien" in o:
                la, ho_so = _do_o_mien(hat_giong["mien"], o["mien"], thu)
            else:
                ten, tep, prov, ho_so_goc = fixtures[o["fx"]]
                la, ho_so = _do_o_fixture(ten, tep, deepcopy(prov), ho_so_goc, o["ops"], thu)
            bang(la == o["la"], f"{o['id']}: ham la {la}, mong {o['la']}")
            bang(ho_so == o["ho_so"], f"{o['id']}: ho so {ho_so}, mong {o['ho_so']}")


def _thay_mot(goc, cu, moi):
    bang(goc.count(cu) == 1, f"chuoi o dong bang khong xuat hien dung mot lan: {cu!r}")
    return goc.replace(cu, moi, 1)


def _do_o_fixture(ten, tep, prov, ho_so_goc, ops, thu):
    for loai, vi_tri, gia_tri in ops:
        if loai == "tep":
            tep = _thay_mot(tep, vi_tri, gia_tri)
            continue
        dich = prov
        if vi_tri[0].startswith("@"):
            nhom = prov["moc"]["checkout"] if vi_tri[0] == "@checkout" else prov["moc"]["gate_output"]["jobs"]
            dich, = [job for job in nhom if job["job_id"] == vi_tri[1]]
            vi_tri = vi_tri[2:]
        for khoa in vi_tri[:-1]:
            dich = dich[khoa]
        dich[vi_tri[-1]] = gia_tri
    (thu / "prov.yaml").write_text(yaml.safe_dump(prov), encoding="utf-8")
    (thu / ten).write_bytes(tep.encode())
    tt, ly_do = G().kiem_tep(thu / ten, thu)
    ho_so = {k: _thay_mot(v, "<tên tệp đánh giá tương đối thư mục>", ten) for k, v in ho_so_goc.items()}
    vp = G().kiem_ho_so(ho_so, thu)
    return [tt, ly_do], [v.removeprefix("$.moc_gate_output: ").replace(f":{ten}:", ":") for v in vp]


def _do_o_mien(hat, sua, thu):
    import copy
    readback = copy.deepcopy(hat["readback"])
    if "readback" in sua:
        khoa, gia_tri = sua["readback"]
        if khoa == "user.login":
            readback["user"]["login"] = gia_tri
        else:
            readback[khoa] = gia_tri
    if "dong" in sua:
        readback["body"] = _thay_mot(hat["dong"], *sua["dong"])
    (thu / hat["ten_readback"]).write_text(json.dumps(readback), encoding="utf-8")
    head = sua.get("head")
    if head is not None:
        khai = hat["loi_khai_head"].format(url=hat["url"])
        return G().kiem_mien(khai, thu, head), None
    khai = hat["loi_khai"].format(url=hat["url"], sha=sua.get("loi_khai_sha", hat["sha"]))
    ho_so = {k: _thay_mot(v, "<loi_khai>", khai) for k, v in hat["ho_so"].items()}
    vp = G().kiem_ho_so(ho_so, thu)
    return G().kiem_mien(khai, thu, None), [v.removeprefix("$.gate_output: waiver_khong_co_can_cu:") for v in vp]


# ---------------------------------------------------------------- đột biến
DOT_BIEN = (   # (tên, chuỗi gốc, chuỗi thay, TIỀN TỐ ca đích). Chuỗi gốc phải xuất hiện ĐÚNG MỘT lần.
    ("m1_bo_nhanh_skipped", '    if d["skip"]:\n        return "not_measured", ["co_job_skipped"]\n', "", "a115"),
    ("m2_bo_K6", 'if not (isinstance(lg := ldd.get(k), dict) and str(lg.get("sha256")) == j["sha"]):', "if False:", "a105"),
    ("m3_nhan_dong_la", '            ly.append("dong_la")', "            pass", "a103"),
    ("m4_nhan_tong_thu_hai", '    elif so_moc > 1:\n        ly.append("moc_lap")', "    elif False:\n        pass", "a103"),
    ("m5_bo_job_lap", '            if int(j[1]) in kq["jobs"] or int(j[1]) in kq["skip"]:\n                ly.append("job_lap")\n', "", "a103"),
    ("m6_bo_BO_SINH", '    if d["bo_sinh"] not in BO_SINH:\n        return "not_measured", ["bo_sinh_la"]\n', "", "a104"),
    ("m7_bo_labels", '                or ",".join(q.get("labels") or []) != j["labels"]):', "                ):", "a106"),
    ("m8_bo_conclusion", ' or q.get("conclusion") != j["conclusion"]', "", "a106"),
    ("m9_tap_con", 'if set(d["jobs"]) != set(P) - skip_p:', 'if not set(d["jobs"]) <= set(P) - skip_p:', "a107"),
    ("m10_bo_attempt", ' and y.get("attempt_yeu_cau") == attempt', "", "a108"),
    ("m11_bo_dung_mot", "    if len(khop) != 1:", "    if not khop:", "a108"),
    ("m12_bo_K3", 'if not (r.get("event") == "push" and r.get("loi_khai_rest_path") == ".github/workflows/ci.yml"):', "if False:", "a108"),
    ("m13_so_bang", "    return type(x) is int", "    return isinstance(x, (int, float))", "a108"),
    ("m14_bot_check", '"gate-packet-loop (ubuntu-latest)", "gate-registry (ubuntu-latest)")', '"gate-packet-loop (ubuntu-latest)",)', "a109"),
    ("m15_bo_K7", '    if d["moc"] != (moc_tu, so_pass, n):\n        ly.append("moc_lech")\n', "", "a110"),
    ("m16_skip_moi_dang", '    if any(s["v3"] != v3 for s in d["skip"].values()):', "    if False:", "a111"),
    ("m17_theo_symlink", '            if p.is_symlink():\n                ly.append("symlink")\n                continue\n', "", "a112"),
    ("m18_khong_chuan_hoa", "            c = _chuan(k)", "            c = str(k)", "a201"),
    ("m19_bo_phi_loi_khai", ' and c not in PHI_LOI_KHAI', "", "a201"),
    ("m20_bo_lookahead", r'RE_TOKEN = re.compile(r"[ \t]*([a-z_]+)(?=$|[ \t—\-:(,.;])")', r'RE_TOKEN = re.compile(r"[ \t]*([a-z_]+)")', "a202"),
    ("m21_duong_khong_can_tep", '            if tk in ("passed", "measured") and not teps:\n                vp.append(f"{duong}: duong_khong_tep_danh_gia")\n',
     "", "a203"),
    ("m22_bo_cham_cham", '".." in pp.parts', "False", "a204"),
    ("m23_bo_symlink_thanh_phan", "        p = p / x\n        if p.is_symlink():\n            return None\n", "        p = p / x\n", "a204"),
    ("m24_measured_khong_duong", 'TOKEN = frozenset({"passed", "measured",', 'TOKEN = frozenset({"passed",', "a205"),
    ("m25_nhan_failed_cho_duong", "                if tt != can:", '                if tt not in (can, "failed"):', "a206"),
    ("m26_chi_tep_dau", "            for t in teps:", "            for t in teps[:1]:", "a207"),
    ("m27_bo_failed_khop", '            can = "failed" if tk == "failed" else "passed"\n',
     '            can = "failed" if tk == "failed" else "passed"\n            teps = [] if tk == "failed" else teps\n', "a208"),
    ("m28_bo_html_url", 'if not isinstance(d, dict) or d.get("html_url") != url:', "if not isinstance(d, dict):", "a209"),
    ("m29_bo_association", ' and d.get("author_association") == "OWNER"', "", "a209"),
    ("m30_bo_login", 'd["user"].get("login") == CHU_KHO and ', "", "a209"),
    ("m31_nhan_nhieu_dong", "    if len(dong) != 1:\n        return [\"dong_mien\"]", "    if not dong:\n        return [\"dong_mien\"]", "a209"),
    ("m32_nhan_khong_dong", "    if len(dong) != 1:\n        return [\"dong_mien\"]",
     "    if len(dong) > 1:\n        return [\"dong_mien\"]\n    if not dong:\n        return []", "a209"),
    ("m33_bo_han", "        datetime.date.fromisoformat(m[4])", "        str(m[4])", "a209"),
    ("m34_bo_os", '    if "ubuntu-latest" not in m[2].split(","):\n        return ["os"]\n', "", "a209"),
    ("m35_bo_sha", '    if (m[1] != head) if head is not None else (m[1] not in gia_tri):\n        return ["sha"]\n', "", "a209"),
    ("m36_cli_rc0", '{"passed": 0, "failed": 1}.get(tt, 3)', '{"passed": 0, "failed": 1}.get(tt, 0)', "a210"),
    ("m37_khong_prov_lay_dong_tong", '    if y is None:\n        return "not_measured", ly\n    moc = y["moc"]',
     '    if y is None:\n        return d["moc"][0], []\n    moc = y["moc"]', "a102"),
    ("m38_cam_moi_cr", '    if any(d.endswith("\\r") for d in dong):',
     '    if any("\\r" in d for d in dong):\n        return None, ["cr_le"]\n    if False:', "a103"),
    ("m39_nhan_ten_tom", 'RE_TEP_DG = re.compile(r"[A-Za-z0-9_./-]*danh-gia-gate-output-[0-9]+\\.txt")',
     'RE_TEP_DG = re.compile(r"[A-Za-z0-9_./-]*gate-output-[0-9]+\\.txt")', "a211"),
    ("m40_bo_ket_luan_khop", '            ly.append(f"ket_luan_lech:{k}")', "            pass", "a113"),
    ("m41_bo_ve_a", 'if not (r.get("trang_thai") == "passed" and isinstance(tj, dict)', "if not (isinstance(tj, dict)", "a114"),
    ("m42_bo_ve_b", 'isinstance(tj, dict) and tj.get("trang_thai") == "passed"\n', "isinstance(tj, dict)\n", "a114"),
    ("m43_bo_ve_c", 'and all(isinstance(c, dict) and (c.get("trang_thai") == "passed"\n',
     'and all(isinstance(c, dict) and (True or c.get("trang_thai") == "passed"\n', "a114"),
    ("m44_bo_luat_landed", "    if la_landed(du_lieu) and not hop_le:", "    if False:", "a212"),
    ("m45_bo_cr_le", '    if any("\\r" in d for d in dong):\n        return None, ["cr_le"]\n', "", "a103"),
    ("m46_nhan_tron", '        if not all(d.endswith("\\r") for d in dong):\n            return None, ["xuong_dong_tron"]\n        dong = [d[:-1] for d in dong]',
     '        dong = [d[:-1] if d.endswith("\\r") else d for d in dong]', "a103"),
    ("m47_bo_dang_goc", '        a = du_lieu.get("landed")', "        a = None", "a212"),
    ("m48_bo_dang_khoi", "    return a is True or any(", "    return a is True or False and any(", "a212"),
    ("m49_duong_vi_pham_van_hop_le", '        if tk != "failed" and len(vp) == truoc:', '        if tk != "failed":', "a212"),
    ("m50_cho_checkout_rong", "            and isinstance(co, list) and co\n", "            and isinstance(co, list)\n", "a114"),
    ("m51_bo_head", ' and r.get("head_sha") == head', "", "a108"),
    ("m52_bo_schema", ' and y.get("schema") == "ci_provenance/1"', "", "a108"),
    ("m53_bo_goi_kiem_mien", '            vp += [f"{duong}: waiver_khong_co_can_cu:{x}" for x in kiem_mien(v, thu_muc, None)]', "            pass", "a209"),
    ("m54_yaml_khong_mapping", "if not (isinstance(y, dict) and y.get", "if not (y.get", "a116"),
    ("m55_nuot_yaml_hong", '            y = yaml.safe_load(p.read_bytes().decode())',
     '            try:\n                y = yaml.safe_load(p.read_bytes().decode())\n            except Exception:\n                continue', "a116"),
    ("m56_xoa_ly_do_symlink", '    moc = y["moc"]   # giữ', '    ly, moc = [], y["moc"]   # giữ', "a116"),
    ("m57_bo_chot_vong", '    if id(doc) in _dang:\n        raise ValueError(f"vong_tham_chieu tại {duong}")\n', "", "a214"),
    ("m59_nuot_loi_duyet", "os.walk(thu_muc, followlinks=False, onerror=_nem)", "os.walk(thu_muc, followlinks=False)", "a117"),
    ("m60_bo_job_trung_prov", '        ly += ["job_id_trung_provenance"] if q.get("job_id") in P else []\n', "", "a117"),
    ("m61_nhan_nhieu_readback", "    if len(rb) != 1:\n        return [\"readback\"]", "    if not rb:\n        return [\"readback\"]", "a209"),
    ("m62_bo_so_tong_job", '    if d["moc"] != (moc_tu, so_pass, n):', '    if d["moc"][:2] != (moc_tu, so_pass):', "a110"),
    ("m63_bo_so_trang_thai_tong", '    if d["moc"] != (moc_tu, so_pass, n):', '    if d["moc"][1:] != (so_pass, n):', "a110"),
    ("m64_bo_ve_hai_ket_luan", 'if j["conclusion"] != "success" and j["tt"] != "failed":', 'if j["tt"] == "passed" and j["conclusion"] != "success":', "a113"),
    ("m65_cli_khong_bat_stat", "        except OSError:\n            vang = True\n", "        except KeyError:\n            vang = True\n", "a128"),
    ("m66_bo_utf8", '        return None, ["khong_phai_utf8"]', '        txt = byte.decode("utf-8", "replace")', "a103"),
    ("m67_dau_tep_63_hex", 'sha256 ([0-9a-f]{64})\\)")', 'sha256 ([0-9a-f]{63,64})\\)")', "a103"),
    ("m68_bo_thieu_moc", '    if so_moc == 0:\n        ly.append("thieu_moc")\n', "    if False:\n        pass\n", "a103"),
    ("m69_bo_job_lap_skip", '            ly += ["job_lap"] if int(s[1]) in kq["jobs"] or int(s[1]) in kq["skip"] else []\n', "", "a103"),
    ("m70_bo_ly_do_symlink_thu_muc", '        ly += ["symlink" for t in thu if (Path(goc) / t).is_symlink()]', "        pass", "a116"),
    ("m71_goc_symlink", "    if thu_muc.is_symlink() or not thu_muc.is_dir():\n        return None, (", "    if not thu_muc.is_dir():\n        return None, (", "a116"),
    ("m72_checkout_skip_ngoai_job_skip", ' and c.get("job_id") in skip_p', "", "a114"),
    ("m73_bo_tap_skip", '    if set(d["skip"]) != skip_p:\n        ly.append("tap_skip_lech")\n', "", "a107"),
    ("m74_bo_failed_truoc", '        return "failed", []\n', "        pass\n", "a101"),
    ("m75_nhieu_url", "if isinstance(gia_tri, str) else []) != 1:", "if isinstance(gia_tri, str) else []) < 1:", "a209"),
    ("m76_readback_symlink", '.json") if p.is_file() and not p.is_symlink()]', '.json") if p.is_file()]', "a209"),
    ("m77_readback_hong_thanh_dat", '        return ["doc_readback"]', "        return []", "a209"),
    ("m78_bo_nhanh_head", "    if (m[1] != head) if head is not None else (m[1] not in gia_tri):", "    if m[1] not in gia_tri:", "a209"),
    ("m79_nhan_tuyet_doi", 'if pp.is_absolute() or ".." in pp.parts', 'if ".." in pp.parts', "a204"),
    ("m80_bo_is_file", "    return p if p.is_file() else None", "    return p", "a204"),
    ("m81_bo_dinh_dang", '            vp.append(f"{duong}: dinh_dang_loi_khai")\n            continue', "            continue", "a203"),
    ("m82_token_am_la_hop_le", '        if tk in ("not_measured", "skipped", "not_run"):\n            continue\n',
     '        if tk in ("not_measured", "skipped", "not_run"):\n            hop_le = True\n            continue\n', "a212"),
    ("m83_bo_phi_gioi_han", '"gateoutputnguonvagioihan", ', "", "a201"),
    ("m84_bo_phi_disposition", ', "mocgateoutputrcdisposition"', "", "a201"),
    ("m85_dau_tep_match", "    if not (m := RE_DAU.fullmatch(dong[0])):", "    if not (m := RE_DAU.match(dong[0])):", "a103"),
    ("m86_tong_match", "        elif mm := RE_MOC.fullmatch(d):", "        elif mm := RE_MOC.match(d):", "a103"),
    ("m87_check_khong_loc_passed", ' for j in d["jobs"].values() if j["tt"] == "passed"}', ' for j in d["jobs"].values()}', "a109"),
    ("m88_skip_cu_match", "        elif s := (RE_SKIP_CU.fullmatch(d) or", "        elif s := (RE_SKIP_CU.match(d) or", "a103"),
    ("m89_bo_dong_2", "    for d in dong[1:]:", "    for d in dong[2:]:", "a118"),
    ("m90_job_sau_skip", 'if int(j[1]) in kq["jobs"] or int(j[1]) in kq["skip"]:', 'if int(j[1]) in kq["jobs"]:', "a118"),
    ("m91_hai_skip", 'if int(s[1]) in kq["jobs"] or int(s[1]) in kq["skip"] else []', 'if int(s[1]) in kq["jobs"] else []', "a118"),
    ("m92_prov_vang", "    if thu_muc.is_symlink() or not thu_muc.is_dir():", "    if thu_muc.is_symlink():", "a118"),
    ("m93_theo_symlink_thu_muc", "followlinks=False, onerror", "followlinks=True, onerror", "a118"),
    ("m94_run_khong_mapping", "if (isinstance(r, dict) and _la_so", "if (_la_so", "a118"),
    ("m95_job_khong_mapping", " if isinstance(q, dict)):", "):", "a119"),
    ("m96_tap_jobs_khong_mapping", "and isinstance(tj, dict) and tj.get", "and tj.get", "a119"),
    ("m97_checkout_khong_list", "and isinstance(co, list) and co\n", "and co\n", "a119"),
    ("m98_checkout_khong_mapping", "and all(isinstance(c, dict) and (c.get", "and all((c.get", "a119"),
    ("m99_checkout_skip_moi_trang_thai", '(c.get("trang_thai") == "skipped" and c.get("job_id") in skip_p)', '(c.get("job_id") in skip_p)', "a119"),
    ("m100_labels_none", '",".join(q.get("labels") or [])', '",".join(q.get("labels"))', "a119"),
    ("m101_khong_job_la_passed", 'moc_tu = "passed" if n and so_pass == n', 'moc_tu = "passed" if so_pass == n', "a119"),
    ("m102_landed_khong_mapping", "    if not isinstance(du_lieu, dict):\n        return False", "    if not isinstance(du_lieu, dict):\n        return True", "a215"),
    ("m103_khoa_khong_chuoi", "any(isinstance(k, str) and RE_KHOI_LANDED", "any(RE_KHOI_LANDED", "a215"),
    ("m104_khoi_khong_mapping", "RE_KHOI_LANDED.fullmatch(k) and isinstance(v, dict) and v.get", "RE_KHOI_LANDED.fullmatch(k) and v.get", "a215"),
    ("m105_goc_ho_so_symlink", '".." in pp.parts or p.is_symlink():', '".." in pp.parts:', "a215"),
    ("m106_readback_thu_muc", "if p.is_file() and not p.is_symlink()]", "if not p.is_symlink()]", "a215"),
    ("m107_goc_readback_symlink", "          if not thu_muc.is_symlink() else [])", "          if True else [])", "a215"),
    ("m108_readback_khong_mapping", 'if not isinstance(d, dict) or d.get("html_url")', 'if d.get("html_url")', "a215"),
    ("m109_user_khong_mapping", 'if not (isinstance(d.get("user"), dict) and d["user"]', 'if not (d["user"]', "a215"),
    ("m110_failed_tinh_hop_le", '        if tk != "failed" and len(vp) == truoc:', "        if len(vp) == truoc:", "a216"),
    ("m111_hop_le_nguoc", '        if tk != "failed" and len(vp) == truoc:', '        if tk == "failed" and len(vp) == truoc:', "a216"),
    ("m112_landed_bo_hop_le", "    if la_landed(du_lieu) and not hop_le:", "    if la_landed(du_lieu):", "a216"),
    ("m113_vp_ly_rong", ":{tt}:{','.join(ly) or '-'}\"", ":{tt}:{','.join(ly)}\"", "a206"),
    ("m114_subparser_khong_bat_buoc", "required=True)\n    a1 =", "required=False)\n    a1 =", "a217"),
    ("m115_provenance_khong_bat_buoc", 'a1.add_argument("--provenance", required=True)', 'a1.add_argument("--provenance")', "a217"),
    ("m116_systemexit_rc0", "        return 2 if e.code else 0", "        return 0", "a217"),
    ("m117_help_rc1", "        return 2 if e.code else 0", "        return 2 if e.code else 1", "a217"),
    ("m118_prov_vang_cli", " or not Path(a.provenance).is_dir()", "", "a217"),
    ("m119_in_ly_rong", "{a.tep} {','.join(ly) or '-'}\\n", "{a.tep} {','.join(ly)}\\n", "a217"),
    ("m120_rc_khoi_1", "    rc = 0\n    for hs", "    rc = 1\n    for hs", "a217"),
    ("m121_rc_tep_cuoi", "rc = rc or (1 if vp else 0)", "rc = 1 if vp else 0", "a217"),
    ("m122_ten_ho_so", 'if hs.name.endswith("-land-evidence.yaml") else hs.stem', "if False else hs.stem", "a217"),
    ("m124_in_bo_ly_do", "{a.tep} {','.join(ly) or '-'}\\n", "{a.tep} {'-'}\\n", "a217"),
    ("m123_nhan_do_dat", "{'DO' if vp else 'DAT'}", "{'DAT'}", "a217"),
    ("m125_dau_head_khong_hex", "head ([0-9a-f]{40})", "head (.{40})", "a120"),
    ("m126_job_labels_ngoac", r"\[([^\]]*)\]", r"\[(.*)\]", "a120"),
    ("m127_skip_v3_khop_dau", "RE_SKIP_V3.fullmatch(d)", "RE_SKIP_V3.match(d)", "a120"),
    ("m128_moc_so_rong", r"\(([0-9]+)/([0-9]+) job", r"\(([0-9]*)/([0-9]+) job", "a120"),
    ("m129_token_bo_gach_dai", r"[ \t—\-:(,.;]", r"[ \t\-:(,.;]", "a121"),
    ("m130_token_search", "RE_TOKEN.match(gia_tri.casefold())", "RE_TOKEN.search(gia_tri.casefold())", "a121"),
    ("m131_tep_run_chu", "output-[0-9]+", "output-[a-z0-9]+", "a121"),
    ("m132_khoa_bo_so", "if c.isalnum()", "if c.isalpha()", "a121"),
    ("m133_phi_chuoi_con", "c not in PHI_LOI_KHAI", "not any(p in c for p in PHI_LOI_KHAI)", "a121"),
    ("m134_landed_truthy", "    return a is True or any(", "    return bool(a) or any(", "a121"),
    ("m135_khoi_landed_khop_dau", "RE_KHOI_LANDED.fullmatch(k)", "RE_KHOI_LANDED.match(k)", "a121"),
    ("m136_mien_bo_strip", "RE_MIEN.fullmatch(x.strip())", "RE_MIEN.fullmatch(x)", "a122"),
    ("m137_mien_khop_dau", "RE_MIEN.fullmatch(x.strip())", "RE_MIEN.match(x.strip())", "a122"),
    ("m138_mien_os_bo_so", "os=([a-z0-9,.-]+)", "os=([a-z,.-]+)", "a122"),
    ("m139_url_khong_bat_buoc", '        return ["url"]', '        return ["url"] if urls else []', "a122"),
    ("m140_head_truthy", "if head is not None else", "if head else", "a122"),
    ("m141_doi_os_sha", '    if "ubuntu-latest" not in m[2].split(","):\n        return ["os"]\n    if (m[1] != head) if head is not None else (m[1] not in gia_tri):\n        return ["sha"]\n', '    if (m[1] != head) if head is not None else (m[1] not in gia_tri):\n        return ["sha"]\n    if "ubuntu-latest" not in m[2].split(","):\n        return ["os"]\n', "a122"),
    ("m142_cr_sau_dau_tep", '    if any("\\r" in d for d in dong):\n        return None, ["cr_le"]\n    if not (m := RE_DAU.fullmatch(dong[0])):\n        return None, ["dau_tep_sai"]\n', '    if not (m := RE_DAU.fullmatch(dong[0])):\n        return None, ["dau_tep_sai"]\n    if any("\\r" in d for d in dong):\n        return None, ["cr_le"]\n', "a123"),
    ("m143_skip_truoc_failed", '    if any(j["tt"] == "failed" for j in d["jobs"].values()):                                    # K8\n        return "failed", []\n    if d["skip"]:\n        return "not_measured", ["co_job_skipped"]\n', '    if d["skip"]:\n        return "not_measured", ["co_job_skipped"]\n    if any(j["tt"] == "failed" for j in d["jobs"].values()):\n        return "failed", []\n', "a123"),
    ("m144_labels_noi_sai", '",".join(q.get("labels") or [])', '",~".join(q.get("labels") or [])', "a123"),
    ("m145_ly_do_noi_sai", """{tt}:{','.join(ly) or '-'}\"""", """{tt}:{';'.join(ly) or '-'}\"""", "a123"),
    ("m146_argparse_usage", "    def error(self, message):\n", "    def _error(self, message):\n", "a217"),
    ("m58_cli_chi_bat_OSError", "        except Exception as e:   # gồm vòng", "        except OSError as e:   # gồm vòng", "a214"),
)
DOT_BIEN += (
    ("r12i_head_uppercase", "head ([0-9a-f]{40})", "head ([0-9a-fA-F]{40})", "a125"),
    ("r12i_os_digit7", "os=([a-z0-9,.-]+)", "os=([a-z0-689,.-]+)", "a126"),
    ("r12i_filename_Z", "[A-Za-z0-9_./-]*danh-gia", "[A-Ya-z0-9_./-]*danh-gia", "a131"),
    ("r12i_skip_old_ascii_name", r"(.+?): skipped \(khong tinh\)", r"([\x00-\x7f]+?): skipped \(khong tinh\)", "a125"),
    ("r12i_skip_v3_ascii_name", r"(.+?): skipped ->", r"([\x00-\x7f]+?): skipped ->", "a125"),
    ("r12_job_ten_greedy", r'JOB ([0-9]+) (.+?) \[', r'JOB ([0-9]+) (.+) \[', "a129"),
    ("r12_token_space_unicode", r're.compile(r"[ \t]*([a-z_]+)', r're.compile(r"\s*([a-z_]+)', "a124"),
    ("r12_token_sep_unicode", r"(?=$|[ \t—", r"(?=$|[\s—", "a124"),
    ("r12_run_so_unicode", r"Gate output run ([0-9]+) attempt", r"Gate output run (\d+) attempt", "a125"),
    ("r12_job_conclusion_unicode", r"conclusion=([a-z_]+) log_sha256=", r"conclusion=(\w+) log_sha256=", "a125"),
    ("r12_url_path_unicode", r"tra-luat/[A-Za-z0-9._~/%-]*?#issuecomment-", r"tra-luat/\S*?#issuecomment-", "a126"),
    ("r12_mien_ly_do_unicode", r"ly_do=([^ \t].*?) han=", r"ly_do=(\S.*?) han=", "a126"),
)
CHI_POSIX = frozenset({
    "m17_theo_symlink", "m23_bo_symlink_thanh_phan", "m56_xoa_ly_do_symlink",
    "m70_bo_ly_do_symlink_thu_muc", "m71_goc_symlink", "m76_readback_symlink",
    "m93_theo_symlink_thu_muc", "m105_goc_ho_so_symlink", "m107_goc_readback_symlink",
})
TU_KIEM = (   # (tên, gốc, thay, ca đích, hạng mong đợi)
    ("vo_can_KeyError", "def la_landed(du_lieu):\n", "def la_landed(du_lieu):\n    raise KeyError('vo can')\n", "a212", "TIN_DUNG_GIA"),
    ("chi_them_chu_thich", 'CHU_KHO = "ducthangho"\n', 'CHU_KHO = "ducthangho"  # vo hai\n', "a201", "SONG_SOT"),
)


def chay_con(ten_ca, ma):
    r = subprocess.run([sys.executable, "-B", str(HERE / "gate_output_doi_chieu_test.py"), "--mot-ca", ten_ca], capture_output=True,
                       env=dict(os.environ, GATE_OUTPUT_DOI_CHIEU_MA=str(ma), PYTHONDONTWRITEBYTECODE="1"), timeout=600)
    return r.returncode, (r.stdout + r.stderr).decode("utf-8", "replace")


def phan_hang(rc, ra, ten_ca):
    if rc == 0:
        return "SONG_SOT"
    if rc == 3:
        return "GIET" if f"DO:{ten_ca}:" in ra else "TIN_DUNG_GIA"
    return "TIN_DUNG_GIA" if rc == 4 else "HONG"


_XANH = {}


def chay_dot_bien(ten, cu, moi, tien_to):
    khop = [c for c in CA if c.split("_")[0] == tien_to]
    if len(khop) != 1:
        return "HONG", f"tiền tố ca đích {tien_to!r} phải khớp ĐÚNG MỘT ca, khớp {khop}"
    ten_ca = khop[0]
    goc = (HERE / "gate_output_doi_chieu.py").read_text(encoding="utf-8")
    if goc.count(cu) != 1 or cu == moi:
        return "HONG", f"neo phải xuất hiện đúng 1 lần và đột biến phải đổi mã (thấy {goc.count(cu)})"
    with tempfile.TemporaryDirectory(prefix="godc_db_") as thu:
        ban_goc, ban_db = Path(thu) / "goc.py", Path(thu) / f"db_{ten}.py"
        ban_goc.write_text(goc, encoding="utf-8")
        ban_db.write_text(goc.replace(cu, moi), encoding="utf-8")
        if ten_ca not in _XANH:
            _XANH[ten_ca] = chay_con(ten_ca, ban_goc)
        rc, ra = _XANH[ten_ca]
        if rc != 0:
            return "HONG", f"ca đích không xanh trên bản gốc (rc={rc}): {ra[-200:]}"
        rc, ra = chay_con(ten_ca, ban_db)
        return phan_hang(rc, ra, ten_ca), ra.strip()[-200:]


def chay_ca(ten):
    """(rc, dòng): 0 đạt · 3 `DO:<ca>:` (chỉ `TinHieuChotCa`) · 4 lỗi vô can — KHÔNG đổi lỗi vô can thành tín hiệu chốt."""
    try:
        CA[ten]()
    except TinHieuChotCa as e:
        return 3, f"DO:{ten}:{e}"
    except Exception as e:
        return 4, f"HONG:{ten}:{type(e).__name__}: {e}"
    return 0, ""


def main(argv):
    if len(argv) == 2 and argv[0] == "--mot-ca" and argv[1] in CA:
        rc, dong = chay_ca(argv[1])
        print(dong)
        return rc
    if argv:
        print("dung: gate_output_doi_chieu_test.py [--mot-ca TEN]", file=sys.stderr)
        return 2
    kq = [chay_ca(ten) for ten in CA]
    print("".join(f"[{dong}]\n" for rc, dong in kq if rc), end="")
    dat = sum(rc == 0 for rc, _ in kq)
    danh_sach = {ten for ten, *_ in DOT_BIEN}
    sai_khai_bao = CHI_POSIX - danh_sach
    if sai_khai_bao:
        print(f"[DOT BIEN CHI POSIX KHONG TON TAI] {sorted(sai_khai_bao)}")
    duoc_do = DOT_BIEN
    if os.name != "posix":
        print(f"BO QUA chi-POSIX: {', '.join(sorted(CHI_POSIX))}")
        duoc_do = [db for db in DOT_BIEN if db[0] not in CHI_POSIX]
    xau = [f"{ten}: {h} {ct}" for ten, cu, moi, dich in duoc_do
           for h, ct in [chay_dot_bien(ten, cu, moi, dich)] if h != "GIET"]
    for x in xau:
        print(f"[DOT BIEN KHONG BI GIET DUNG] {x}")
    print(f"CA: {dat}/{len(CA)} dat")
    print(f"DOT BIEN: {len(duoc_do) - len(xau)}/{len(duoc_do)} bi giet dung ly do")
    loi_tk = [f"{ten}: mong {mong}, duoc {h}" for ten, cu, moi, dich, mong in TU_KIEM
              for h in [chay_dot_bien(ten, cu, moi, dich)[0]] if h != mong]
    for x in loi_tk:
        print(f"[TU KIEM] {x}")
    print(f"TU KIEM PHAN HANG: {'DAT' if not loi_tk else 'DO'} ({len(TU_KIEM)} dot bien)")
    ok = dat == len(CA) > 0 and len(duoc_do) > 0 and not xau and not loi_tk and not sai_khai_bao
    print(f"TONG: {'DAT' if ok else 'DO'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
