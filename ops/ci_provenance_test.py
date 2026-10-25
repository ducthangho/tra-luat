#!/usr/bin/env python3
"""Phản chứng CHẠY ĐƯỢC cho `ops/ci_provenance.py` — packet #899 (wp899 P-A), đặc tả r2 A1–A8 + r3 A14–A19.

Fixture là log THẬT cắt gọn của run 39342960764 (Linux job 118368717941, Windows job 118368688495, CRLF giữ nguyên), khoá
bằng sha256 (c21). REST giả GIỮ TRẠNG THÁI: trả lời dựng từ run/jobs/log đang giữ, phân trang theo đúng `per_page`/`page`
của URL — không diễn kịch bản. ĐỘT BIẾN sửa BẢN SAO TẠM, ca đích chạy ở tiến trình con (`python -B`,
`PYTHONDONTWRITEBYTECODE=1`), phải XANH trên bản gốc trước. Chỉ `bang()` ném `TinHieuChotCa` (con in `DO:<ca>:`, thoát 3); lỗi vô
can thoát 4 ⇒ TÍN DỤNG GIẢ. `TU_KIEM` kiểm chính bộ phân hạng. r3: workflow giả (`wf_tu`) tiêm qua `wf=`; reader thật đo ở c34.

Ra: `CA: N/N dat` · `DOT BIEN: M/M bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (k dot bien)` · `TONG: DAT`.
"""
import contextlib, hashlib, importlib.util, io, json, os, re, subprocess, sys, tempfile, types, urllib.error, urllib.parse, urllib.request
from pathlib import Path
from unittest import mock

import yaml

sys.dont_write_bytecode = True
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="backslashreplace")

HERE = Path(__file__).resolve().parent
ROOT_THAT = HERE.parent
MA = Path(os.environ.get("CI_PROVENANCE_MA") or HERE / "ci_provenance.py")
CI_DANG_KY = ROOT_THAT / ".claude/dev/ci_dang_ky_test.py"
H = "b27fe85c9e9593ddbb059808fe4347fe1bd267be"
P1, P2, TREE = "5618020a67709ca6f2c93138905df0aa8d9c2df6", "400589368e09ab2ee0e734b7af08b93478035503", "857bc47e6bc5f0024e442b400819ac51286dfc55"
GIT = {H: {"tree": TREE, "parents": [P1, P2]}}
LINUX = r"""2026-10-19T23:40:06.0485589Z ##[group]Runner Image
2026-10-19T23:40:06.0486422Z Image: ubuntu-24.04
2026-10-19T23:40:18.2994760Z [command]/usr/bin/git log -1 --format=%H
2026-10-19T23:40:18.3020458Z b27fe85c9e9593ddbb059808fe4347fe1bd267be
2026-10-19T23:40:18.3206929Z ##[group]Run actions/setup-python@v5
"""
WINDOWS = r"""2026-10-19T23:40:00.8741298Z ##[group]Runner Image
2026-10-19T23:40:00.8742264Z Image: windows-2025-vs2026
2026-10-19T23:40:12.5725422Z [command]"C:\Program Files\Git\bin\git.exe" log -1 --format=%H
2026-10-19T23:40:12.6114260Z b27fe85c9e9593ddbb059808fe4347fe1bd267be
2026-10-19T23:40:12.6655485Z ##[group]Run actions/setup-python@v5
""".replace("\n", "\r\n")
BAM_FIXTURE = {   # sha256 bản cắt: dòng 16,17,729-731 log job 118368717941 (đầy đủ 60ad91c5…) · dòng 16,17,155-157 log
    "LINUX": "65951e153dcf49d4b7bf687c68241678386fb7d55a04e1743b6d6a293eec25af",   # job 118368688495 (đầy đủ f5b64633…),
    "WINDOWS": "d3e4fc7a9d8f37a68cae205811058643b4b4117cb09b3b7137f7440472ff2981"}   # tải bằng REST 24-10-2026
T = "2026-10-19T23:45:04.8553236Z"
DUONG_GIA = "ops/thu_gia_test.py"

class TinHieuChotCa(AssertionError):
    """Chỉ `bang()` ném lớp này ⇒ phân biệt được giết thật (chốt) với chết vì lỗi vô can."""

CA = {}

def bang(dieu_kien, thong_diep):
    if not dieu_kien:
        raise TinHieuChotCa(thong_diep)

def ca(f):
    CA[f.__name__] = f
    return f

def nap():
    spec = importlib.util.spec_from_file_location("ci_provenance_duoi_test", MA)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def buoc(lenh, *ra):
    """Một bước theo đúng dạng log Actions: nhóm mở `##[group]Run` (lệnh vọng lại có mã ANSI) rồi đầu ra."""
    return [f"{T} ##[group]Run {lenh}", f"{T} \x1b[36;1m{lenh}\x1b[0m", f"{T} shell: /usr/bin/bash -e {{0}}",
            f"{T} ##[endgroup]"] + [f"{T} {x}" for x in ra]

def khoi(cac_dong, *ra):
    """Một bước có kịch bản NHIỀU dòng (mỗi dòng vọng lại một lần với mã ANSI)."""
    return [f"{T} ##[group]Run {cac_dong[0]}"] + [f"{T} \x1b[36;1m{x}\x1b[0m" for x in cac_dong] + \
        [f"{T} shell: /usr/bin/bash -e {{0}}", f"{T} ##[endgroup]"] + [f"{T} {x}" for x in ra]

def wf_tu(*kich_ban, buoc_them=None, job_them=None, goc_them=None):   # workflow giả: mỗi kịch bản một bước `run:` của job `j`
    return yaml.safe_dump({"jobs": {"j": {"runs-on": "x", "steps": [{"run": k + "\n"} | (buoc_them or {}) for k in kich_ban]}
                                     | (job_them or {})}} | (goc_them or {}), allow_unicode=True)

def wf_tu_log(*logs):   # mặc định cho ca cũ: mỗi nhóm `##[group]Run` có dòng màu thành một `run:` bằng đúng khối in lại
    kb = [re.findall("\x1b\\[36;1m(.*?)\x1b\\[0m", g) for lg in logs for g in re.split(r"##\[group\]Run ", lg)[1:]]
    return wf_tu(*["\n".join(k) for k in kb if k])

def log_voi(*cac_buoc, nen=LINUX):
    return nen + "".join(d + "\n" for b in cac_buoc for d in b)

def job(i, **kw):
    return {"id": i, "name": f"j{i}", "run_attempt": 1, "runner_id": 7, "runner_name": "GitHub Actions 7",
            "labels": ["ubuntu-latest"], "conclusion": "success", "check_run_url": f"https://api.github.com/repos/o/r/check-runs/{i}",
            "steps": [{"name": "s", "conclusion": "success"}]} | kw

class RestGia:
    """REST giả GIỮ TRẠNG THÁI: mọi trả lời dựng từ run/jobs/log/artifact đang giữ; `loi` = {đoạn đường dẫn: mã HTTP}."""

    def __init__(s, run, jobs, logs, arts=(), loi=None, hong_trang=None, run_id=5):
        s.id, s.run, s.jobs, s.logs, s.arts, s.loi, s.nhat_ky = run_id, run, list(jobs), dict(logs), list(arts), dict(loi or {}), []
        s.hong_trang, s.than_run = dict(hong_trang or {}), None   # {khoá: "rong" | "lap"}: từ trang 2 trả rỗng / lặp lại trang 1

    def __call__(s, url):
        s.nhat_ky.append(url)
        u = urllib.parse.urlsplit(url)
        q, p = dict(urllib.parse.parse_qsl(u.query)), u.path
        if u.netloc != "api.github.com":
            return 404, b""
        for k, ma in s.loi.items():
            if k in p:
                return ma, b'{"message": "gia"}'
        if m := re.fullmatch(r"/repos/o/r/actions/runs/(\d+)", p):
            return (200, s.than_run or json.dumps(s.run).encode()) if int(m[1]) == s.id else (404, b"")
        if (m := re.fullmatch(r"/repos/o/r/actions/runs/(\d+)/attempts/(\d+)/jobs", p)) and int(m[1]) == s.id:
            return s._trang([j for j in s.jobs if j["run_attempt"] == int(m[2])], q, "jobs")
        if (m := re.fullmatch(r"/repos/o/r/actions/runs/(\d+)/artifacts", p)) and int(m[1]) == s.id:
            return s._trang(s.arts, q, "artifacts")
        if m := re.fullmatch(r"/repos/o/r/actions/jobs/(\d+)/logs", p):
            return (200, s.logs[int(m[1])].encode()) if int(m[1]) in s.logs else (404, b"")
        return 404, b""

    def _trang(s, ds, q, khoa):
        n, tr = int(q.get("per_page", 30)), int(q.get("page", 1))
        hong = s.hong_trang.get(khoa)
        tong = len(ds) - (hong == "tong_doi" and tr == 1)   # total đổi giữa các trang, ID cuối vẫn đủ theo total mới
        trang = [] if hong == "rong" and tr > 1 else ds[:n] if hong == "lap" and tr > 1 else ds[(tr - 1) * n:tr * n]
        return 200, json.dumps({"total_count": tong, khoa: trang}).encode()

@contextlib.contextmanager
def moi_tam(them=None):
    """Bản sao TẠM của sổ đăng ký THẬT, nối thêm mục `MOI` lúc chạy — công cụ phải thấy nó qua import, không qua bảng chép."""
    with tempfile.TemporaryDirectory(prefix="cip_moi_") as thu:
        p = Path(thu) / "ci_dang_ky_test.py"
        p.write_text(CI_DANG_KY.read_text(encoding="utf-8") + "".join(f"\nMOI[{k!r}] = {v!r}\n" for k, v in (them or {}).items()),
                     encoding="utf-8")
        yield p

def chay(cap, run=None, attempt=1, git=GIT, loi=None, them=None, sua=None, arts=(), hong_trang=None, than_run=None, wf=None):
    """cap = [(job, log | None)]; wf: None ⇒ `wf_tu_log` · YAML tại (H, ci.yml) · {(sha, path): văn bản}. Trả (rc, stdout, prov, rest)."""
    wf = wf if type(wf) is dict else {(H, ".github/workflows/ci.yml"): wf_tu_log(*[lg for _, lg in cap if lg]) if wf is None else wf}
    run = {"id": 5, "run_attempt": 1, "event": "push", "head_sha": H, "path": ".github/workflows/ci.yml", "check_suite_id": 9} | (run or {})
    run = {k: v for k, v in run.items() if v is not None}
    rest = RestGia(run, [j for j, _ in cap], {j["id"]: lg for j, lg in cap if lg is not None}, arts, loi, hong_trang)
    rest.than_run = than_run
    m = nap()
    if sua:
        sua(m)
    with tempfile.TemporaryDirectory(prefix="cip_out_") as thu, moi_tam({DUONG_GIA: r"^THU: (\d+)/(\d+) dat$"} | (them or {})) as moi:
        o = Path(thu) / "out"
        with contextlib.redirect_stdout(io.StringIO()) as buf:
            rc = m.main(["thu", "--repo", "o/r", "--run", "5", "--attempt", str(attempt), "--out", str(o)], goi=rest,
                        git=git.get, moi_tu=moi, wf=lambda sha, path: wf.get((sha, path)))
        prov = yaml.safe_load((o / "provenance.yaml").read_text(encoding="utf-8")) if (o / "provenance.yaml").exists() else None
    return rc, buf.getvalue(), prov, rest

def co(prov, i=0): return prov["moc"]["checkout"][i]
def gate(prov, i=0): return prov["moc"]["gate_output"]["jobs"][i]

@ca
def c01_cli_du_co():
    r = subprocess.run([sys.executable, "-B", str(MA), "thu", "--help"], capture_output=True, text=True, encoding="utf-8")
    bang(r.returncode == 0 and all(c in r.stdout for c in ("--repo", "--run", "--attempt", "--out")), f"thu --help: {r.returncode}")
    for argv in (["thu", "--repo", "o/r", "--run", "5", "--out", "x"], ["thu", "--repo", "o", "--run", "5", "--attempt", "1",
                                                                         "--out", "x"], []):
        with contextlib.redirect_stdout(io.StringIO()) as buf, contextlib.redirect_stderr(io.StringIO()):
            rc = nap().main(argv, goi=lambda u: (500, b""))
        bang(rc == 2 and buf.getvalue().count("NOT_MEASURED: 4\n") == 1, f"sai đối số {argv} ⇒ rc 2 + đúng một dòng đếm: {rc}")

@ca
def c02_attempt_lech():
    rc, _, p, _ = chay([(job(1), LINUX)], run={"run_attempt": 2})
    bang(rc == 12 and p["moc"]["run"]["trang_thai"] == "failed", f"run_attempt 2 vs --attempt 1 ⇒ failed/rc 12: rc={rc}")
    rc, _, p, _ = chay([(job(1), LINUX)])
    bang(rc == 0 and p["moc"]["run"]["trang_thai"] == "passed" and p["moc"]["run"]["check_suite_id"] == 9, f"khớp ⇒ passed: {rc}")

@ca
def c03_checkout_linux():
    rc, _, p, _ = chay([(job(1), LINUX)])
    c = co(p)
    bang(c["trang_thai"] == "passed" and c["sha"] == H and c["parents"] == [P1, P2] and c["tree"] == TREE, f"Linux: {c}")
    bang(gate(p)["image"] == "ubuntu-24.04" and gate(p)["check_run_id"] == "1", f"Image/check run: {gate(p)}")

@ca
def c04_checkout_windows():
    rc, _, p, _ = chay([(job(1), WINDOWS)])
    bang(co(p)["trang_thai"] == "passed" and co(p)["sha"] == H and gate(p)["image"] == "windows-2025-vs2026", f"Windows: {co(p)}")

@ca
def c05_checkout_khong_sha():
    lg = LINUX.replace(f"Z {H}\n", "Z Done\n")
    rc, out, p, _ = chay([(job(1), lg)])
    bang(co(p)["trang_thai"] == "not_measured" and "sha" not in co(p), f"không dòng SHA ⇒ not_measured: {co(p)}")
    lg = LINUX.replace(f"Z {H}\n", f"Z {H} \n")   # khớp NGUYÊN dòng: đuôi thừa không phải dòng SHA
    bang(co(chay([(job(1), lg)])[2])["trang_thai"] == "not_measured", "dòng SHA có đuôi thừa phải là not_measured")

@ca
def c06_checkout_hai_sha():
    hai = LINUX + f"{T} [command]/usr/bin/git log -1 --format=%H\n{T} {P1}\n"
    rc, _, p, _ = chay([(job(1), hai)])
    bang(rc == 12 and co(p)["trang_thai"] == "failed", f"hai SHA khác nhau ⇒ failed: rc={rc} {co(p)}")
    lap = LINUX + f"{T} [command]/usr/bin/git log -1 --format=%H\n{T} {H}\n"
    bang(co(chay([(job(1), lap)])[2])["trang_thai"] == "passed", "hai dòng CÙNG SHA vẫn là một SHA")

@ca
def c07_checkout_push_lech():
    rc, _, p, _ = chay([(job(1), LINUX)], run={"head_sha": P1})
    bang(rc == 12 and co(p)["trang_thai"] == "failed" and co(p)["sha"] == H, f"push SHA log ≠ head_sha ⇒ failed: {co(p)}")

@ca
def c08_checkout_pr_parents():
    rc, _, p, _ = chay([(job(1), LINUX)], run={"event": "pull_request", "head_sha": P2})
    bang(rc == 0 and co(p)["trang_thai"] == "passed", f"PR head_sha ∈ parents ⇒ passed: rc={rc} {co(p)}")
    rc, _, p, _ = chay([(job(1), LINUX)], run={"event": "pull_request", "head_sha": P2}, git={})
    c = co(p)
    bang(c["trang_thai"] == "not_measured" and c["parents"] == c["tree"] == "not_measured" and c["sha"] == H,
         f"thiếu object ⇒ parents/tree not_measured, SHA vẫn ghi: {c}")

@ca
def c09_checkout_pr_lech():
    rc, _, p, _ = chay([(job(1), LINUX)], run={"event": "pull_request", "head_sha": "0" * 40})
    bang(rc == 12 and co(p)["trang_thai"] == "failed", f"PR head_sha ∉ parents và ≠ SHA ⇒ failed: {co(p)}")

@ca
def c10_runner_id_0():
    rc, _, p, rest = chay([(job(1, runner_id=0, conclusion="cancelled"), None)])
    bang(gate(p)["trang_thai"] == co(p)["trang_thai"] == "not_run" and not any("/logs" in u for u in rest.nhat_ky),
         f"runner_id 0 ⇒ not_run, không tải log: {gate(p)['trang_thai']}")

@ca
def c11_job_skipped():
    rc, _, p, _ = chay([(job(1, runner_id=0, conclusion="skipped"), None), (job(2, conclusion="skipped"), None)])
    bang(rc == 0 and all(gate(p, i)["trang_thai"] == co(p, i)["trang_thai"] == "skipped" for i in (0, 1)), "job skipped ⇒ skipped")

@ca
def c12_marker_khong_khop():
    rc, _, p, _ = chay([(job(1), log_voi(buoc(f"python {DUONG_GIA}", "THU: 3/4 dat")))])
    bang(rc == 12 and gate(p)["trang_thai"] == "failed" and gate(p)["dau_duong"][0]["trang_thai"] == "failed", f"{gate(p)}")
    rc, _, p, _ = chay([(job(1), log_voi(buoc(f"python -B ./{DUONG_GIA}", "THU: 4/4 dat")))])
    bang(rc == 0 and gate(p)["trang_thai"] == "passed" and gate(p)["dau_duong"][0]["dong_khop"] == ["THU: 4/4 dat"], f"{gate(p)}")

@ca
def c13_marker_buoc_khac():
    lg = log_voi(buoc(f"python {DUONG_GIA}", "khong co"), buoc("python ops/khac.py", "THU: 4/4 dat"))
    rc, _, p, _ = chay([(job(1), lg)])
    bang(rc == 12 and gate(p)["dau_duong"][0]["trang_thai"] == "failed", f"dòng khớp ở bước KHÁC ⇒ failed: {gate(p)}")

@ca
def c14_ngoai_moi():
    rc, _, p, _ = chay([(job(1), log_voi(buoc("python ops/khong_dang_ky_test.py", "THU: 4/4 dat")))])
    bang(rc == 0 and gate(p)["trang_thai"] == "not_measured" and gate(p)["dau_duong"][0]["trang_thai"] == "not_measured", f"{gate(p)}")
    rc, _, p, _ = chay([(job(1, conclusion="failure"), LINUX)])
    bang(rc == 12 and gate(p)["trang_thai"] == "failed", "job conclusion failure ⇒ failed")

@ca
def c15_moi_mot_nguon():
    lg = log_voi(buoc("python ops/them_luc_chay_test.py", "MOI LUC CHAY 2/2"))
    rc, _, p, _ = chay([(job(1), lg)], them={"ops/them_luc_chay_test.py": r"^MOI LUC CHAY (\d+)/(\d+)$"})
    bang(gate(p)["trang_thai"] == "passed", f"mục MOI thêm lúc chạy phải được thấy: {gate(p)}")

@ca
def c16_workflow_def_luon_not_measured():
    rc, _, p, _ = chay([(job(1), LINUX)])
    wd = p["moc"]["workflow_definition"]
    bang(wd["trang_thai"] == "not_measured" and wd["loi_khai_rest_path"] == ".github/workflows/ci.yml", f"{wd}")
    bang(not re.search(r"(?m)^[ -]*path:", yaml.safe_dump(p)), "`path` chỉ được nằm dưới `loi_khai_rest_path`")

@ca
def c17_ghi_nguyen_tu():
    m, dem = nap(), []
    goc_ghi = m.ghi_tep

    def ghi_hong(p, b):
        dem.append(p)
        if len(dem) == 2:
            raise OSError("giữa chừng")
        goc_ghi(p, b)
    for co_cu in (False, True):
        dem.clear()
        with tempfile.TemporaryDirectory() as thu, mock.patch.object(m, "ghi_tep", ghi_hong):
            o = Path(thu) / "out"
            if co_cu:
                o.mkdir()
                (o / "cu.txt").write_text("ban truoc", encoding="utf-8")
            with contextlib.suppress(OSError):
                m.ghi_nguyen_tu(o, {"provenance.yaml": b"a", "jobs/1.trich.txt": b"b", "run.json": b"c"})
            sau = sorted(x.name for x in o.iterdir()) if o.exists() else None
            bang(len(dem) == 2 and sau == (["cu.txt"] if co_cu else None) and len(list(Path(thu).iterdir())) == int(co_cu),
                 f"có bản trước={co_cu}: out sau lỗi {sau}, thư mục cha {sorted(x.name for x in Path(thu).iterdir())}")

@ca
def c18_dem_not_measured():
    rc, out, p, _ = chay([(job(1), log_voi(buoc(f"python {DUONG_GIA}", "THU: 4/4 dat")))])
    bang(rc == 0 and re.search(r"^NOT_MEASURED: 1$", out, re.M), f"chỉ Workflow definition not_measured ⇒ `NOT_MEASURED: 1`: {out}")

@ca
def c19_rest_loi():
    for doan in ("/runs/5", "/attempts/1/jobs", "/jobs/1/logs", "/artifacts"):
        rc, out, p, _ = chay([(job(1), LINUX)], loi={doan: 403})
        bang(rc == 3 and "403" in out and p is None and "NOT_MEASURED: 4\n" in out, f"REST 403 ở {doan} ⇒ rc 3, 403, dòng đếm: {out}")
    for than in (b"[]", b"null", b'"x"'):
        try:
            rc, out, p, _ = chay([(job(1), LINUX)], than_run=than)
        except Exception as e:   # lỗi lọt ra ngoài hợp đồng rc 3 CHÍNH LÀ điều ca này đo
            rc, out, p = type(e).__name__, "", None
        bang(rc == 3 and p is None and out.count("NOT_MEASURED: 4\n") == 1, f"thân run {than!r} ⇒ rc 3 + dòng đếm: rc={rc} {out[-120:]}")
    m, buf = nap(), io.StringIO()
    rest = RestGia({"id": 5, "run_attempt": 1, "event": "push", "head_sha": H, "path": "p", "check_suite_id": 9}, [job(1)], {1: LINUX})
    with moi_tam() as moi, mock.patch.object(m, "ghi_tep", lambda p, b: (_ for _ in ()).throw(OSError("dia day"))), \
            contextlib.redirect_stdout(buf), contextlib.suppress(OSError), tempfile.TemporaryDirectory() as thu:
        m.main(["thu", "--repo", "o/r", "--run", "5", "--attempt", "1", "--out", str(Path(thu) / "o")], goi=rest, git=GIT.get, moi_tu=moi)
    bang(buf.getvalue().count("NOT_MEASURED: 4\n") == 1 and "LOI_GHI" in buf.getvalue(), f"lỗi ghi ⇒ dòng đếm: {buf.getvalue()[-160:]}")
    m, buf = nap(), io.StringIO()
    with moi_tam() as moi, mock.patch.object(m, "moc_gate", lambda *a: {}.vang), contextlib.redirect_stdout(buf), \
            tempfile.TemporaryDirectory() as thu:
        loi = _bat(lambda: m.main(["thu", "--repo", "o/r", "--run", "5", "--attempt", "1", "--out", str(Path(thu) / "o")], goi=rest,
                                  git=GIT.get, moi_tu=moi))
    bang(loi == "AttributeError" and buf.getvalue().count("NOT_MEASURED: 4\n") == 1, f"lỗi thu ngoài hợp đồng: {loi} {buf.getvalue()}")

@ca
def c20_du_trang():
    arts = [{"id": i, "name": f"a{i}", "digest": "sha256:x", "size_in_bytes": 1, "expired": False} for i in (1, 2, 3)]
    for hong in (None, {"jobs": "rong"}, {"jobs": "lap"}, {"jobs": "tong_doi"}, {"artifacts": "rong"}, {"artifacts": "lap"},
                 {"artifacts": "tong_doi"}):
        rc, out, p, rest = chay([(job(i), log_voi(buoc(f"python {DUONG_GIA}", "THU: 4/4 dat"))) for i in range(1, 5)], sua=lambda m: setattr(m, "TRANG", 2), arts=arts, hong_trang=hong)
        bang(rc == 0 and p, f"phân trang {hong}: rc={rc} {out[-200:]}")
        g = p["moc"]["gate_output"]
        tt = {k: g[f"tap_{k}"]["trang_thai"] for k in ("jobs", "artifacts")}
        ids = [x["job_id"] for x in g["jobs"]], [a["id"] for a in g["artifacts"]]
        bang(len(set(ids[0])) == len(ids[0]) and len(set(ids[1])) == len(ids[1]), f"{hong}: ID trùng lọt ra {ids}")
        if hong is None:
            bang(ids == ([1, 2, 3, 4], [1, 2, 3]) and tt == {"jobs": "passed", "artifacts": "passed"}, f"đủ trang: {ids} {tt}")
        else:
            bang(tt[next(iter(hong))] == "not_measured" and re.search(r"^NOT_MEASURED: 2$", out, re.M), f"{hong}: {tt} {out[-80:]}")

@ca
def c22_thieu_dinh_danh_khong_passed():
    lg = log_voi(buoc(f"python {DUONG_GIA}", "THU: 4/4 dat"))
    sai_run = {"id": (None,), "run_attempt": (None, True), "event": (None, "", " "), "head_sha": (None, "bad", H.upper(), H + "\n"),
               "path": (None, ""), "check_suite_id": (None, True, 0, "9")}
    for k, gt in sai_run.items():
        for v in gt:
            rc, _, p, _ = chay([(job(1), lg)], run={k: v} if v is not None else {k: None})
            bang(p and p["moc"]["run"]["trang_thai"] == "not_measured" and k in p["moc"]["run"]["thieu"], f"Run {k}={v!r}: {p and p['moc']['run']}")
            if k in ("event", "head_sha"):
                bang(co(p)["trang_thai"] == "not_measured", f"Checkout khi REST {k}={v!r}: {co(p)}")
    sai_job = {"runner_id": (None, True), "labels": (None, [], [False], [""]), "runner_name": (None, ""), "name": (None, ""),
               "conclusion": (None, "", "unknown", "neutral"), "steps": (None, [], [{}], [{"name": "", "conclusion": "success"}],
                                                                        [{"name": "s", "conclusion": None}], "x", [1]),
               "check_run_url": (None, "", "wrong", "https://x/check-runs/1", "https://api.github.com/repos/o/r/check-runs/1\n", 1, [1])}
    for k, gt in sai_job.items():
        for v in gt:
            try:   # kiểu lạ phải thành not_measured, KHÔNG được làm công cụ ném (F05) — chỉ bắt hai lớp lỗi chiếu dữ liệu
                rc, _, p, _ = chay([(job(1, **{k: v}), lg)])
            except (AttributeError, TypeError) as e:
                bang(False, f"Gate {k}={v!r}: công cụ ném {type(e).__name__}")
            bang(gate(p)["trang_thai"] == "not_measured" and k in gate(p)["thieu"], f"Gate {k}={v!r}: {gate(p)['trang_thai']}")
    art = {"id": 1, "name": "a", "digest": "sha256:x", "size_in_bytes": 1, "expired": False}
    for k, v in (("name", None), ("size_in_bytes", True), ("expired", 0), ("digest", "md5:x")):
        rc, _, p, _ = chay([(job(1), lg)], arts=[art | {k: v}])
        bang(p["moc"]["gate_output"]["tap_artifacts"]["trang_thai"] == "not_measured", f"artifact {k}={v!r}")
    for than in ('{"total_count": true, "jobs": []}', '{"total_count": 1, "jobs": [{"id": true}]}'):
        rest = RestGia({"id": 5}, [], {})
        rest._trang = lambda ds, q, khoa, _t=than: (200, _t.encode())
        bang(_bat(lambda: nap().lay_trang(rest, "https://api.github.com/repos/o/r/actions/runs/5/attempts/1/jobs", "jobs")) == "LoiRest", than)
    rc, _, p, _ = chay([(job(1), lg)])
    bang(rc == 0 and p["moc"]["run"]["trang_thai"] == gate(p)["trang_thai"] == "passed", "đủ trường ⇒ passed")

def _bat(f):
    try:
        f()
    except Exception as e:   # tên lớp ngoại lệ CHÍNH LÀ thứ ca đo
        return type(e).__name__

@ca
def c23_chi_loi_goi_that():
    for kb in ([f"printf 'python {DUONG_GIA}'"], [f"echo x # python {DUONG_GIA}"], [f"python {DUONG_GIA}.bak"], [f"python -m {DUONG_GIA}"],
               [f"echo 'a; python {DUONG_GIA}; b'"], [f"echo ';' python {DUONG_GIA}"], [f"python -W ignore -c 1 {DUONG_GIA}"],
               [f"python -X dev {DUONG_GIA}"], [f"true && python {DUONG_GIA}"], [f"python {DUONG_GIA} | tee x"], [f"python {DUONG_GIA} --x"],
               ["python .\\ops\\thu_gia_test.py"], ["printf a \\", f"  python {DUONG_GIA}"], ["if false; then", f"  python {DUONG_GIA}", "fi"],
               ["f() {", f"  python {DUONG_GIA}", "}"], ["cat <<EOF", f"python {DUONG_GIA}", "EOF"], ['echo "a', f"python {DUONG_GIA}", 'b"'],
               ["# python ops/khac.py", f"python {DUONG_GIA}"]):
        p = chay([(job(1), log_voi(khoi(kb, "THU: 4/4 dat")))])[2]
        bang(gate(p)["dau_duong"] == [] and gate(p)["trang_thai"] == "not_measured", f"{kb!r} không sinh bằng chứng: {gate(p)['dau_duong']}")
    rc, _, p, _ = chay([(job(1), log_voi(buoc(f"/usr/bin/python3.13 -B ./{DUONG_GIA}", "THU: 4/4 dat")))])
    bang(gate(p)["trang_thai"] == "passed" and [x["duong_dan"] for x in gate(p)["dau_duong"]] == [DUONG_GIA], f"{gate(p)['dau_duong']}")
    m = nap()
    bang([g and g[2] for g in map(m.RE_LOI_GOI.fullmatch, m.dong_logic(["python \\", f"  {DUONG_GIA}"]))] == [DUONG_GIA], "dòng nối")

@ca
def c24_goi_that_loi_va_chuyen_huong():
    m = nap()
    h302 = lambda: urllib.error.HTTPError("u", 302, "Found", {"Location": "https://blob.example/x"}, None)  # noqa: E731
    for dau, sau, mong in ((urllib.error.URLError("x"), None, "loi"), (h302(), urllib.error.URLError("x"), "loi"),
                           (h302(), OSError("x"), "loi"), (h302(), contextlib.nullcontext(types.SimpleNamespace(status=200, read=lambda: b"ok")), (200, b"ok"))):
        mo, mo2 = mock.Mock(side_effect=dau), mock.Mock(side_effect=sau if isinstance(sau, Exception) else None, return_value=sau)
        with mock.patch.object(urllib.request, "build_opener", lambda *a: types.SimpleNamespace(open=mo)), \
                mock.patch.object(urllib.request, "urlopen", mo2), mock.patch.dict(os.environ, {"GITHUB_PAT": "gia"}):
            try:
                kq = m.goi_that("https://api.github.com/x")
            except m.LoiRest:
                kq = "loi"
            except Exception as e:   # lỗi lọt ra ngoài hợp đồng LoiRest CHÍNH LÀ điều ca này đo
                kq = type(e).__name__
        bang(kq == mong, f"{type(dau).__name__} → {type(sau).__name__}: được {kq!r}, mong {mong!r}")
        bang(sau is None or isinstance(mo2.call_args.args[0], str), "lượt chuyển hướng không được mang Request có token")

def kb(p): return gate(p)["kich_ban"]
def khong_marker(p, msg): bang(gate(p)["dau_duong"] == [] and kb(p)["buoc_xac_thuc"] == 0 and gate(p)["trang_thai"] != "passed", f"{msg}: {gate(p)}")

@ca
def c25_f02_env_mang_mau():   # A14: dòng metadata mang màu nhắc đường dẫn MOI ⇒ khối ≠ run: ⇒ không xác thực
    lg = log_voi([f"{T} ##[group]Run python ops/khac.py", f"{T} \x1b[36;1mpython ops/khac.py\x1b[0m", f"{T} env:",
                  f"{T} \x1b[36;1mpython {DUONG_GIA}\x1b[0m", f"{T} ##[endgroup]", f"{T} THU: 4/4 dat"])
    khong_marker(chay([(job(1), lg)], wf=wf_tu("python ops/khac.py"))[2], "env mang màu")
    lg = log_voi(buoc(f"python {DUONG_GIA}", "THU: 4/4 dat"))   # khối ĐÚNG cấu trúc mà không ứng viên nào bằng ⇒ vẫn không xác thực
    khong_marker(chay([(job(1), lg)], wf=wf_tu("python ops/khac.py"))[2], "khối không bằng run: nào")

@ca
def c26_f02_dong_khong_mau():   # A15: chỉ dòng python mang màu, run: có if/fi ⇒ khối ≠ run: ⇒ không xác thực
    lg = log_voi([f"{T} ##[group]Run if false; then", f"{T} if false; then", f"{T} \x1b[36;1mpython {DUONG_GIA}\x1b[0m", f"{T} fi",
                  f"{T} ##[endgroup]", f"{T} THU: 4/4 dat"])
    khong_marker(chay([(job(1), lg)], wf=wf_tu(f"if false; then\npython {DUONG_GIA}\nfi"))[2], "dòng không màu")
    lg = log_voi(buoc(f"python {DUONG_GIA}", "THU: 4/4 dat"))   # khối đúng cấu trúc là TẬP CON của run: ⇒ không xác thực
    khong_marker(chay([(job(1), lg)], wf=wf_tu(f"if false; then\npython {DUONG_GIA}\nfi"))[2], "khối ⊂ run:")

@ca
def c27_f02_yaml_khong_toi_gian():   # A16: bằng nguyên văn nhưng một dòng ngoài allowlist ⇒ xác thực, không marker
    p = chay([(job(1), log_voi(khoi([f"python {DUONG_GIA}", "echo xong"], "THU: 4/4 dat")))])[2]
    bang(gate(p)["dau_duong"] == [] and kb(p) == {"buoc_xac_thuc": 1, "trang_thai": "passed", "nguon": "run_tai_sha_checkout"}, f"{gate(p)}")
    p = chay([(job(1), log_voi(khoi([f"python {DUONG_GIA}", "python ops/khac.py"], "THU: 4/4 dat")))])[2]
    bang(gate(p)["trang_thai"] == "passed" and [(x["duong_dan"], x["trang_thai"]) for x in gate(p)["dau_duong"]] == [(DUONG_GIA, "passed"),
         ("ops/khac.py", "not_measured")], f"khối TOÀN lời gọi tối giản đo được từng lời gọi: {gate(p)}")

def che_do(wf, lenh=f"python {DUONG_GIA}"):
    p = chay([(job(1), log_voi(buoc(lenh, "THU: 4/4 dat")))], wf=wf)[2]
    return [(x["trang_thai"], x.get("ly_do")) for x in gate(p)["dau_duong"]]
CHAN = [("not_measured", "che_do_khong_xac_dinh")]

@ca
def c28_che_do_env_buoc():   # A17 (i) + đối chứng
    bang(che_do(wf_tu(f"python {DUONG_GIA}")) == [("passed", None)], "đối chứng: không env, không đối số ⇒ đo được")
    bang(che_do(wf_tu(f"python {DUONG_GIA}", buoc_them={"env": {"A": "1"}})) == CHAN, "env mức bước ⇒ chặn")

@ca
def c29_che_do_env_job():   # A17 (ii)
    bang(che_do(wf_tu(f"python {DUONG_GIA}", job_them={"env": {"CI_DANG_KY_X": "1", "PYTHONUTF8": "1"}})) == CHAN, "job CI_DANG_KY_* ⇒ chặn")
    bang(che_do(wf_tu(f"python {DUONG_GIA}", job_them={"env": {"PYTHONUTF8": "1"}})) == [("passed", None)], "job env khác ⇒ đo được")

@ca
def c30_che_do_doi_so():   # A17 (iii): có đối số sau script ⇒ không phải lời gọi tối giản ⇒ không marker
    bang(che_do(wf_tu(lenh := f"python {DUONG_GIA} --gop-dich manh"), lenh) == [], "có đối số ⇒ không marker")

@ca
def c31_che_do_duong_khac():   # đường đổi môi trường ngoài (i)–(iii): mỗi đường một chốt, mỗi chốt một đột biến
    x = f"python {DUONG_GIA}"
    for ten, w, lenh in (("VAR=", wf_tu("A=1 " + x), "A=1 " + x), ("env workflow", wf_tu(x, goc_them={"env": {"CI_DANG_KY_X": "1"}}), x),
                         ("defaults workflow", wf_tu(x, goc_them={"defaults": {"run": {"shell": "bash"}}}), x),
                         ("defaults job", wf_tu(x, job_them={"defaults": {"run": {"shell": "bash"}}}), x),
                         ("working-directory", wf_tu(x, buoc_them={"working-directory": "d"}), x),
                         ("shell lạ", wf_tu(x, buoc_them={"shell": "python {0}"}), x), ("GITHUB_ENV", wf_tu(x, "echo A=1 >> $GITHUB_ENV"), x),
                         ("job gọi lại", wf_tu(x, goc_them={"jobs": {"j": {"runs-on": "x", "steps": [{"run": x + "\n"}]}, "k": {"uses": "./w.yml"}}}), x)):
        bang(che_do(w, lenh) == CHAN, f"{ten} ⇒ chặn: {che_do(w, lenh)}")
    bang(che_do(wf_tu(x, buoc_them={"shell": "bash", "name": "n"})) == [("passed", None)], "shell bash + name ⇒ đo được")

@ca
def c32_workflow_khong_doc_duoc():   # A18
    lg = log_voi(buoc(f"python {DUONG_GIA}", "THU: 4/4 dat"))
    for ten, w, l in (("thiếu object", {}, lg), ("sai path", {(H, "khac.yml"): wf_tu_log(lg)}, lg), ("YAML hỏng", "jobs: [", lg),
                      ("YAML không phải dict", "- a", lg), ("SHA checkout chưa đo", None, lg.replace(f"Z {H}\n", "Z Done\n"))):
        try:
            rc, _, p, _ = chay([(job(1), l)], wf=w)
        except Exception as e:   # ném ra ngoài CHÍNH LÀ điều ca này đo
            bang(False, f"{ten}: công cụ ném {type(e).__name__}")
        bang(rc in (0, 12) and kb(p)["trang_thai"] == "not_measured" and gate(p)["dau_duong"] == [] and gate(p)["trang_thai"] != "passed"
             and (w is not None or kb(p)["ly_do"] == "sha_checkout_chua_do"), f"{ten}: rc={rc} {gate(p)}")

@ca
def c33_nhieu_ung_vien():   # A19: khối khớp hai ứng viên, ứng viên SAU có env ⇒ chặn (vế chặt nhất)
    w = yaml.safe_load(wf_tu(f"python {DUONG_GIA}"))
    w["jobs"]["k"] = {"runs-on": "x", "env": {"CI_DANG_KY_X": "1"}, "steps": [{"run": f"python {DUONG_GIA}\n"}]}
    bang(che_do(yaml.safe_dump(w)) == CHAN, "hai ứng viên, một bị chặn ⇒ chặn")

@ca
def c34_git_blob_that():   # F08: reader THẬT trên kho tạm; đối tượng là tree (không commit nên không cần ký), HEAD chưa sinh
    m = nap()
    with tempfile.TemporaryDirectory(prefix="cip_git_") as thu:
        g = lambda *a, i=None: subprocess.run(["git", "-C", thu, *a], input=i, capture_output=True, check=True).stdout.decode().strip()  # noqa: E731
        g("init", "-q")
        cay = [g("mktree", i=f"100644 blob {g('hash-object', '-w', '--stdin', i=v)}\twf.yml\n".encode()) for v in (b"jobs: {}\n", b"\xff\n")]
        kq = [m.git_blob(cay[0], "wf.yml", goc=thu), m.git_blob(cay[0], "khac.yml", goc=thu), m.git_blob(cay[1], "wf.yml", goc=thu)]
    bang(kq == ["jobs: {}\n", None, None], f"git_blob: đúng byte tại object; thiếu path / không UTF-8 ⇒ None: {kq}")

@ca
def c35_f02_khoi_khong_tron_ven():   # F02 r3: khối thiếu/lẫn màu không được thành tập con khớp run: của bước KHÁC
    x, hd, sh = f"python {DUONG_GIA}", f"{T} ##[group]Run python {DUONG_GIA}", f"{T} shell: /usr/bin/bash -e {{0}}"
    mau, ra = f"{T} \x1b[36;1mpython {DUONG_GIA}\x1b[0m", [f"{T} ##[endgroup]", f"{T} THU: 4/4 dat"]
    for ten, lg, w in (("dòng sau khối màu không phải shell:", [hd, mau, f"{T} echo xong", sh] + ra, wf_tu(x + "\necho xong", x)),
                       ("thiếu shell:", [hd, mau] + ra, wf_tu(x)), ("header ≠ dòng màu đầu", [f"{T} ##[group]Run echo a", mau, sh] + ra, wf_tu(x)),
                       ("thiếu ##[endgroup]", [hd, mau, sh, f"{T} THU: 4/4 dat"], wf_tu(x)), ("màu sau shell:",
                        [f"{T} ##[group]Run python ops/khac.py", f"{T} \x1b[36;1mpython ops/khac.py\x1b[0m", sh, mau] + ra,
                        wf_tu("python ops/khac.py", "python ops/khac.py\n" + x))):
        khong_marker(chay([(job(1), log_voi(lg))], wf=w)[2], ten)

@ca
def c21_fixture_bam():
    bam = {k: hashlib.sha256(v.encode()).hexdigest() for k, v in (("LINUX", LINUX), ("WINDOWS", WINDOWS))}
    bang(bam == BAM_FIXTURE, f"fixture lệch bản cắt đã băm: {bam}")

DOT_BIEN = (   # (tên, chuỗi gốc, chuỗi thay, TIỀN TỐ ca đích). Chuỗi gốc phải xuất hiện ĐÚNG MỘT lần.
    ("A1_xoa_co_attempt", 't.add_argument("--attempt", required=True, type=int, help="run_attempt phải đo")', 't.add_argument("--attempt", type=int, default=1, help=argparse.SUPPRESS)', "c01"),
    ("A2_bo_so_attempt", 'if k not in thieu and r.get(k) != v]', "if False]", "c02"),
    ("A3d_lay_sha_dau_tien", "if len(set(sha_ds)) > 1:", "if False:", "c06"),
    ("A3c_thieu_la_do_duoc", '{"trang_thai": "not_measured", "ly_do": "khong_co_dong_sha_checkout"}', '{"trang_thai": "passed", "ly_do": "khong_co_dong_sha_checkout"}', "c05"),
    ("A3e_lay_head_sha_rest", "sha = sha_ds[0]", "sha = head", "c07"),
    ("A3b_chi_nhan_linux", 'if t.startswith("[command]") and', 'if t.startswith("[command]/usr/bin/git") and', "c04"),
    ("A3g_pr_nhan_moi_sha", 'if head in obj["parents"]:', "if True:", "c09"),
    ("A3_sha_khong_nguyen_dong", "k = RE_SHA.fullmatch(dong[i + 1])", 'k = re.match(rf"^{TS} ([0-9a-f]{{40}})", dong[i + 1])', "c05"),
    ("A4d_regex_ca_log_job", "dau, so = do_dau_duong(tach_buoc(dong), moi, xanh, uv or [])",
     'dau, so = do_dau_duong([b | {"phan": [than(d) for d in dong]} for b in tach_buoc(dong)], moi, xanh, uv or [])', "c13"),
    ("A4b_skipped_la_passed", 'return r | {"trang_thai": "skipped"}', 'return r | {"trang_thai": "passed"}', "c11"),
    ("A4a_runner_0_la_passed", 'return r | {"trang_thai": "not_run"}', 'return r | {"trang_thai": "passed"}', "c10"),
    ("A4c_khong_khop_la_not_measured", '"passed" if ok else "failed"', '"passed" if ok else "not_measured"', "c12"),
    ("A4_chep_cung_MOI", "return dict(m.MOI), m.bang_chung_xanh", 'return {"ops/thu_gia_test.py": r"^THU: (\\d+)/(\\d+) dat$"}, m.bang_chung_xanh', "c15"),
    ("A4_job_failure_bo_qua", 'if job.get("conclusion") in LOI_JOB or "failed" in tt:', 'if "failed" in tt:', "c14"),
    ("A5_passed_khi_co_path", '"workflow_definition": {"trang_thai": "not_measured"', '"workflow_definition": {"trang_thai": "passed" if r.get("path") else "not_measured"', "c16"),
    ("A6_ghi_thang_vao_out", 'tam = Path(tempfile.mkdtemp(prefix=f".{out.name}.tam-", dir=out.parent))', "tam = out\n    out.mkdir(exist_ok=True)", "c17"),
    ("A7_bo_dong_dem", "    print(f\"NOT_MEASURED: {tt.count('not_measured')}\")\n", "", "c18"),
    ("A7_gop_rest_vao_12", "        return 3\n", "        return 12\n", "c19"),
    ("M1_chi_doc_trang_dau", "if len(d[khoa]) < TRANG or trang >= TRANG_TOI_DA:", "if True:", "c20"),
    ("F03_dung_khi_du_total", "if len(d[khoa]) < TRANG or trang >= TRANG_TOI_DA:", "if len(ids) >= tong or trang >= TRANG_TOI_DA:", "c20"),
    ("F03_tap_luon_du", '"du": du and len(ids) == tong and len(d[khoa]) < TRANG}', '"du": True}', "c20"),
    ("F03_trung_id_van_them", "                if x[\"id\"] not in ids:\n", "                if True:\n", "c20"),
    ("F04_jobs_run_khac", 'f"{goc}/runs/{run}/attempts/{attempt}/jobs"', 'f"{goc}/runs/{run + 1}/attempts/{attempt}/jobs"', "c20"),
    ("F04_artifacts_run_khac", 'f"{goc}/runs/{run}/artifacts"', 'f"{goc}/runs/{run + 1}/artifacts"', "c20"),
    ("F01_run_thieu_van_passed", '"not_measured" if thieu else "passed"}', '"passed"}', "c22"),
    ("F01_gate_thieu_van_passed", '"not_measured" if thieu or "passed" not in tt', '"not_measured" if "passed" not in tt', "c22"),
    ("F01_checkout_head_thieu", 'return r | {"trang_thai": "not_measured", "ly_do": "REST_thieu_event_hoac_head_sha"}', 'pass', "c22"),
    ("F02_search_thay_match", "goi = [RE_LOI_GOI.fullmatch(d)", "goi = [RE_LOI_GOI.search(d.split(None, 1)[-1])", "c23"),
    ("A14_kich_ban_tu_dong_mau", '(khop := [(r, c) for r, c in uv if b["hop_le"] and r == "\\n".join(b["in_lai"])])', '(khop := [("\\n".join(b["in_lai"]), False)] if b["in_lai"] else [])', "c25"),
    ("A15_khoi_la_tap_con", 'r == "\\n".join(b["in_lai"])]', 'set(b["in_lai"]) <= set(r.split("\\n"))]', "c26"),
    ("A16_bo_luat_toan_khoi", "[g[2] for g in goi] if goi and all(goi) else []", "[g[2] for g in goi if g]", "c27"),
    ("A16_bo_khop_nguyen_van", 'r == "\\n".join(b["in_lai"])]', 'True]', "c25"),
    ("A17i_cho_env_buoc", '"timeout-minutes", "continue-on-error"}', '"timeout-minutes", "continue-on-error", "env"}', "c28"),
    ("A17ii_bo_env_job", ' or _env_chan(j.get("env"))', '', "c29"),
    ("A17iii_cho_doi_so", r'\.py)$")', r'\.py)(?:\s+\S+)*$")', "c30"),
    ("che_do_bo_tien_to_VAR", " or any(g and g[1] for g in goi)", "", "c31"),
    ("che_do_bo_env_workflow", ' or _env_chan(wf.get("env"))', "", "c31"),
    ("che_do_bo_defaults_workflow", 'chan_wf = ("defaults" in wf or', "chan_wf = (", "c31"),
    ("che_do_bo_job_goi_lai", ' or any(type(j) is dict and "uses" in j for j in wf["jobs"].values())', "", "c31"),
    ("che_do_bo_defaults_job", ' or "defaults" in j', "", "c31"),
    ("che_do_moi_shell", ' not in ("bash", "pwsh", "sh")', " is None", "c31"),
    ("che_do_bo_GITHUB_ENV", 'or any(re.search("GITHUB_(ENV|PATH)", b["run"]) for _, b in ds))', "or False)", "c31"),
    ("F08_git_bo_sha", 'f"{sha}:{path}"', 'f"HEAD:{path}"', "c34"),
    ("F08_git_luon_vang", 'return r.stdout.decode("utf-8") if r.returncode == 0 else None', "return None", "c34"),
    ("F02_bo_doi_dong", 'not b["mo"] and b["ok"]', 'b["ok"]', "c35"),
    ("F02_bo_doi_shell", '(not b["tien_to"] or t.startswith("shell: "))', "True", "c35"),
    ("F02_cho_mau_sau", 'b["ok"] and not mau and', 'b["ok"] and', "c35"),
    ("F02_bo_het_tien_to", ' and not b["tien_to"] and b["in_lai"][:1]', " and b[\"in_lai\"][:1]", "c35"),
    ("F02_bo_doi_header", ' and b["in_lai"][:1] == [b["lenh"]]}', "}", "c35"),
    ("A18_head_sha_thay_sha_checkout", 'sha = co[-1].get("sha") if co[-1]["trang_thai"] == "passed" else None', 'sha = r.get("head_sha")', "c32"),
    ("A18_yaml_hong_nem", "    except (yaml.YAMLError, RecursionError):\n        return None\n", "    except RecursionError:\n        return None\n", "c32"),
    ("A19_lay_ung_vien_dau", "chan = any(c for _, c in khop)", "chan = khop[0][1]", "c33"),
    ("F01_steps_chi_la_list", '"steps": lambda v: type(v) is list and bool(v)\n', '"steps": lambda v: type(v) is list or bool(v)\n', "c22"),
    ("F05_chieu_khong_an_toan", 'job["check_run_url"].rsplit("/", 1)[-1] if hop["check_run_url"]', '(job.get("check_run_url") or "").rsplit("/", 1)[-1] if True', "c22"),
    ("F05_luoi_cuoi", "    except Exception:   # lưới cuối M7", "    except ZeroDivisionError:   # lưới cuối M7", "c19"),
    ("F02_khong_noi_dong", 'noi += d[:-1] + " " if d.endswith("\\\\") else d', "noi += d", "c23"),
    ("F02_cho_moi_co", r'(?:\s+-[BuIsSEOqb]+)*', r'(?:\s+-\S+)*', "c23"),
    ("F01_bool_la_int", "return type(v) is int and v >= nho", "return isinstance(v, int) and v >= nho", "c22"),
    ("F01_chuoi_rong", 'return type(v) is str and v.strip() != ""', "return type(v) is str", "c22"),
    ("F01_conclusion_bat_ky", '"conclusion": lambda v: v == "success",', '"conclusion": _chuoi,', "c22"),
    ("F01_labels_rong", "lambda v: type(v) is list and bool(v) and all(_chuoi(x) for x in v)", "lambda v: type(v) is list", "c22"),
    ("F01_check_run_bat_ky", '"check_run_url": lambda v: _chuoi(v) and bool(RE_CHECK_RUN.fullmatch(v))', '"check_run_url": _chuoi', "c22"),
    ("F01_head_sha_bat_ky", '"head_sha": lambda v: _chuoi(v) and bool(RE_HEX40.fullmatch(v))', '"head_sha": _chuoi', "c22"),
    ("F01_head_sha_nhan_newline", "bool(RE_HEX40.fullmatch(v))", "bool(RE_HEX40.match(v))", "c22"),
    ("F01_check_run_nhan_newline", "bool(RE_CHECK_RUN.fullmatch(v))", "bool(RE_CHECK_RUN.match(v))", "c22"),
    ("F01_artifact_khong_kiem", 'tap(arts, "artifacts", ART_BAT_BUOC)', 'tap(arts, "artifacts")', "c22"),
    ("F01_phong_bi_khong_kiem", "            if not (_so(d[\"total_count\"]) and", "            if False and (_so(d[\"total_count\"]) and", "c22"),
    ("F03_bo_kiem_total_doi", 'du, tong = du and tong in (None, d["total_count"]), d["total_count"]', 'du, tong = du, d["total_count"]', "c20"),
    ("F05_than_run_sai_dang", "    if type(r) is not dict:\n", "    if False:\n", "c19"),
    ("F05_loi_ghi_mat_dong_dem", 'print(f"LOI_GHI: {e}\\n{KHONG_SINH}")', 'print(f"LOI_GHI: {e}")', "c19"),
    ("F05_sai_doi_so_mat_dong_dem", "        print(KHONG_SINH)\n        return 2\n", "        return 2\n", "c01"),
    ("F05_rest_mat_dong_dem", 'print(f"REST_LOI: HTTP {e.ma} {e.url}\\n{KHONG_SINH}")', 'print(f"REST_LOI: HTTP {e.ma} {e.url}")', "c19"),
    ("F06_redirect_lot_loi", "        except (urllib.error.URLError, OSError) as e:\n", "        except ZeroDivisionError as e:\n", "c24"),
    ("F06_redirect_mang_token", "yeu_cau, mo = loc, urllib.request.urlopen", "yeu_cau, mo = urllib.request.Request(loc, headers=hd), urllib.request.urlopen", "c24"),
)
TU_KIEM = (   # (tên, gốc, thay, ca đích, hạng mong đợi)
    ("vo_can_AttributeError_qua_except_doi_kieu", "def than(dong):\n",
     "def than(dong):\n    try:\n        raise AttributeError('vo can')\n    except Exception as e:\n"
     "        raise AssertionError(f'doi kieu {type(e).__name__}')\n", "c03", "TIN_DUNG_GIA"),
    ("chi_them_chu_thich", "TRANG = 100\n", "TRANG = 100  # vo hai\n", "c20", "SONG_SOT"),
)

def chay_con(ten_ca, ma):
    r = subprocess.run([sys.executable, "-B", str(HERE / "ci_provenance_test.py"), "--mot-ca", ten_ca], capture_output=True,
                       env=dict(os.environ, CI_PROVENANCE_MA=str(ma), PYTHONDONTWRITEBYTECODE="1"), timeout=300)
    return r.returncode, (r.stdout + r.stderr).decode("utf-8", "replace")

def phan_hang(rc, ra, ten_ca):
    if rc == 0:
        return "SONG_SOT"
    if rc == 3:
        return "GIET" if f"DO:{ten_ca}:" in ra else "TIN_DUNG_GIA"
    return "TIN_DUNG_GIA" if rc == 4 else "HONG"

def chay_dot_bien(ten, cu, moi, tien_to):
    khop = [c for c in CA if c.split("_")[0] == tien_to]
    if len(khop) != 1:
        return "HONG", f"tiền tố ca đích {tien_to!r} phải khớp ĐÚNG MỘT ca, khớp {khop}"
    ten_ca = khop[0]
    goc = (HERE / "ci_provenance.py").read_text(encoding="utf-8")
    if goc.count(cu) != 1 or cu == moi:
        return "HONG", f"neo phải xuất hiện đúng 1 lần và đột biến phải đổi mã (thấy {goc.count(cu)})"
    with tempfile.TemporaryDirectory(prefix="cip_db_") as thu:
        ban_goc, ban_db = Path(thu) / "goc.py", Path(thu) / f"db_{ten}.py"
        ban_goc.write_text(goc, encoding="utf-8")
        ban_db.write_text(goc.replace(cu, moi), encoding="utf-8")
        rc, ra = chay_con(ten_ca, ban_goc)
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
        print("dung: ci_provenance_test.py [--mot-ca TEN]", file=sys.stderr)
        return 2
    kq = [chay_ca(ten) for ten in CA]
    print("".join(f"[{dong}]\n" for rc, dong in kq if rc), end="")
    dat = sum(rc == 0 for rc, _ in kq)
    print(f"CA: {dat}/{len(CA)} dat")
    xau = [f"{ten}: {h} {ct}" for ten, cu, moi, dich in DOT_BIEN for h, ct in [chay_dot_bien(ten, cu, moi, dich)] if h != "GIET"]
    for x in xau:
        print(f"[DOT BIEN KHONG BI GIET DUNG] {x}")
    print(f"DOT BIEN: {len(DOT_BIEN) - len(xau)}/{len(DOT_BIEN)} bi giet dung ly do")
    loi_tk = [f"{ten}: mong {mong}, duoc {h}" for ten, cu, moi, dich, mong in TU_KIEM
              for h in [chay_dot_bien(ten, cu, moi, dich)[0]] if h != mong]
    for x in loi_tk:
        print(f"[TU KIEM] {x}")
    print(f"TU KIEM PHAN HANG: {'DAT' if not loi_tk else 'DO'} ({len(TU_KIEM)} dot bien)")
    ok = dat == len(CA) > 0 and len(DOT_BIEN) > 0 and not xau and not loi_tk
    print(f"TONG: {'DAT' if ok else 'DO'}")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
