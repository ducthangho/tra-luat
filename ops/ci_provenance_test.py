#!/usr/bin/env python3
"""Phản chứng CHẠY ĐƯỢC cho `ops/ci_provenance.py` — packet #899 (wp899 P-A), đặc tả r2 A1–A8 + r3 A14–A18 + r4 A19–A27.

Fixture là log THẬT cắt gọn của run 39342960764 (Linux job 118368717941, Windows job 118368688495, CRLF giữ nguyên), khoá
bằng sha256 (c21). REST giả GIỮ TRẠNG THÁI: trả lời dựng từ run/jobs/log đang giữ, phân trang theo đúng `per_page`/`page`
của URL — không diễn kịch bản. ĐỘT BIẾN sửa BẢN SAO TẠM, ca đích chạy ở tiến trình con (`python -B`,
`PYTHONDONTWRITEBYTECODE=1`), phải XANH trên bản gốc trước. Chỉ `bang()` ném `TinHieuChotCa` (con in `DO:<ca>:`, thoát 3); lỗi vô
can thoát 4 ⇒ TÍN DỤNG GIẢ. `TU_KIEM` kiểm chính bộ phân hạng. r3: workflow giả (`wf_tu`) tiêm qua `wf=`; reader thật đo ở c34.
r4: REST giả giữ `steps[]` dựng MỘT lần từ log + workflow đang giữ (`buoc_rest`, độc lập với `ten_du_kien`); ca lệch sửa state ấy.

Ra: `CA: N/N dat` · `DOT BIEN: M/M bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (k dot bien)` · `TONG: DAT`.
"""
import ast, collections, contextlib, hashlib, importlib.util, io, json, os, random, re, subprocess, sys, tempfile, types, urllib.error, urllib.parse, urllib.request
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
LINUX_KHONG_SETUP = "".join(LINUX.splitlines(True)[:-1])   # bỏ nhóm `Run actions/setup-python@v5`: workflow không có bước `uses:`
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

def wf_tu(*kich_ban, buoc_them=None, job_them=None, goc_them=None):   # workflow giả: bước `uses:` của nhóm setup-python trong
    return yaml.safe_dump({"jobs": {"j": {"runs-on": "x", "steps": [{"uses": "actions/setup-python@v5"}] + [   # fixture, rồi mỗi
        {"run": k + "\n"} | (buoc_them or {}) for k in kich_ban]}   # kịch bản một bước `run:` của job `j`
                                     | (job_them or {})}} | (goc_them or {}), allow_unicode=True)

def wf_tu_log(*logs):   # mặc định cho ca cũ: mỗi nhóm `##[group]Run` có dòng màu thành một `run:` bằng đúng khối in lại
    kb = [re.findall("\x1b\\[36;1m(.*?)\x1b\\[0m", g) for lg in logs for g in re.split(r"##\[group\]Run ", lg)[1:]]
    return wf_tu(*["\n".join(k) for k in kb if k])

def log_voi(*cac_buoc, nen=LINUX):
    return nen + "".join(d + "\n" for b in cac_buoc for d in b)

def job(i, **kw):   # không khai `steps` ⇒ `chay` sinh bằng `buoc_rest` từ log + workflow đang giữ
    return {"id": i, "name": "j", "run_attempt": 1, "runner_id": 7, "runner_name": "GitHub Actions 7",
            "labels": ["ubuntu-latest"], "conclusion": "success", "check_run_url": f"https://api.github.com/repos/o/r/check-runs/{i}",
            } | kw

def buoc_rest(lg, w, ten="j"):   # REST `steps[]` như GitHub sinh: Set up job · mỗi bước YAML của job (tên `name:` / `Run <dòng đầu>`,
    gio = [d[:19] + "Z" for d in lg.splitlines() if "##[group]Run " in d] or [T[:19] + "Z"]   # giờ = header nhóm cùng vị trí,
    jobs = yaml.safe_load(w)["jobs"]   # cắt về giây) · một bước `Post` · Complete job. Cài ĐỘC LẬP với `ten_du_kien` của công cụ
    ys = jobs.get(str(ten).split(" (")[0], next(iter(jobs.values())))["steps"]
    ds = [("Set up job", gio[0])] + [(y.get("name") or "Run " + (y.get("run") or y["uses"]).split("\n")[0], gio[min(i, len(gio) - 1)])
                                     for i, y in enumerate(ys)] + [("Post Run actions/setup-python@v5", gio[-1]), ("Complete job", gio[-1])]
    return [{"name": t, "number": n, "conclusion": "success", "started_at": g, "completed_at": g} for n, (t, g) in enumerate(ds, 1)]

def _co_jobs(v):
    with contextlib.suppress(Exception):
        return type(yaml.safe_load(v)["jobs"]) is dict

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
    wf = wf if type(wf) is dict else {(H, ".github/workflows/ci.yml"): wf_tu_log(*dict.fromkeys(lg for _, lg in cap if lg)) if wf is None else wf}
    cap = [(j if "steps" in j or lg is None else j | {"steps": buoc_rest(lg, next((v for v in wf.values() if _co_jobs(v)), None)
                                                                          or wf_tu_log(lg), j.get("name"))}, lg) for j, lg in cap]
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
    bang(rc == 12 and gate(p)["trang_thai"] == "failed" and [x["trang_thai"] for x in gate(p)["dau_duong"]] == ["failed"], f"{gate(p)}")
    rc, _, p, _ = chay([(job(1), log_voi(buoc(f"python -B ./{DUONG_GIA}", "THU: 4/4 dat")))])
    bang(rc == 0 and gate(p)["trang_thai"] == "passed" and [x["dong_khop"] for x in gate(p)["dau_duong"]] == [["THU: 4/4 dat"]], f"{gate(p)}")

@ca
def c13_marker_buoc_khac():
    lg = log_voi(buoc(f"python {DUONG_GIA}", "khong co"), buoc("python ops/khac.py", "THU: 4/4 dat"))
    rc, _, p, _ = chay([(job(1), lg)])
    bang(rc == 12 and [x["trang_thai"] for x in gate(p)["dau_duong"]] == ["failed", "not_measured"], f"dòng khớp ở bước KHÁC ⇒ failed: {gate(p)}")

@ca
def c14_ngoai_moi():
    rc, _, p, _ = chay([(job(1), log_voi(buoc("python ops/khong_dang_ky_test.py", "THU: 4/4 dat")))])
    bang(rc == 0 and gate(p)["trang_thai"] == "not_measured" and [x["trang_thai"] for x in gate(p)["dau_duong"]] == ["not_measured"], f"{gate(p)}")
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
        try:
            p = chay([(job(1), log_voi(khoi(kb, "THU: 4/4 dat")))])[2]
        except Exception as e:   # ném ra ngoài CHÍNH LÀ điều ca này đo
            bang(False, f"{kb!r}: công cụ ném {type(e).__name__}")
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
def khong_marker(p, msg, ghep="passed"):   # r4: ca dựng trên job có ghép bước `passed` ⇒ "không marker" là do CHỐT, không do ghép hỏng
    bang(gate(p)["dau_duong"] == [] and kb(p)["buoc_xac_thuc"] == 0 and gate(p)["trang_thai"] != "passed"
         and gate(p)["ghep_buoc"]["trang_thai"] == ghep, f"{msg}: {gate(p)}")

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
                         ("shell lạ", wf_tu(x, buoc_them={"shell": "python {0}"}), x)):
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
             and gate(p)["ghep_buoc"]["trang_thai"] == "not_measured" and (w is not None or kb(p)["ly_do"] == "sha_checkout_chua_do"),
             f"{ten}: rc={rc} {gate(p)}")

def wf_job(**job):   # workflow nhiều job: mỗi khoá một bản sao job `j` của `wf_tu(python <MOI>)`, nối thêm trường mức job / bước
    x, ds = f"python {DUONG_GIA}", {}
    for k, (them_job, them_buoc) in job.items():
        ds[k] = yaml.safe_load(wf_tu(x, buoc_them=them_buoc))["jobs"]["j"] | them_job
    return yaml.safe_dump({"jobs": ds}, allow_unicode=True)

@ca
def c33_trung_chu_khac_job():   # A19: run: giống hệt ở job khác; chặn chế độ CHỈ đọc job/bước đã định danh
    bang(che_do(wf_job(j=({}, None), k=({}, {"env": {"A": "1"}}))) == [("passed", None)], "job khác có env ⇒ job đích vẫn đo được")
    bang(che_do(wf_job(j=({}, {"env": {"A": "1"}}), k=({}, None))) == CHAN, "job đích có env ⇒ chặn")

def g1(w, *cac_buoc, sua=None, ten="j", w_rest=None, nen=LINUX, **kw):   # một job `ten` trên workflow `w`; `sua(steps)` đổi REST steps sinh từ log
    lg = log_voi(*cac_buoc, nen=nen)   # + `w_rest or w` trước khi giữ
    st = buoc_rest(lg, w_rest or w, ten)
    if sua:
        sua(st)
    return chay([(job(1, name=ten, steps=st), lg)], wf=w, **kw)[2]

def ghep(p): return gate(p)["ghep_buoc"].get("ly_do", "passed")
X = f"python {DUONG_GIA}"
NHOM_GIA = [f"##[group]Run {X}", f"\x1b[36;1m{X}\x1b[0m", "shell: /usr/bin/bash -e {0}", "##[endgroup]", "THU: 4/4 dat"]

@ca
def c36_ghep_lech_so():   # A20 (a): (i) output in thêm một nhóm `Run python <MOI>` · (ii) REST thiếu một bước so YAML
    p = g1(wf_tu("python ops/khac.py", X), buoc("python ops/khac.py", *NHOM_GIA), buoc(X, "THU: 3/4 dat"))
    khong_marker(p, "nhóm giả trong output", ghep="not_measured")
    bang(ghep(p) == "a_so_nhom_khac_so_buoc_rest_chay", f"(i) vế a: {ghep(p)}")
    w = yaml.safe_load(wf_tu(X, X))   # bước SAU bị chặn (env): bỏ kiểm số đếm thì nhóm duy nhất rơi vào bước trước
    w["jobs"]["j"]["steps"][2]["env"] = {"A": "1"}
    p = g1(yaml.safe_dump(w), buoc(X, "THU: 4/4 dat"), sua=lambda st: st.pop(3))
    khong_marker(p, "REST thiếu bước", ghep="not_measured")
    bang(ghep(p) == "a_so_buoc_rest_khac_so_buoc_yaml", f"(ii) vế a: {ghep(p)}")
    p = g1(wf_tu(X, X), buoc(X, "THU: 4/4 dat"))   # (iii) log THIẾU một nhóm so với bước REST đã chạy
    bang(ghep(p) == "a_so_nhom_khac_so_buoc_rest_chay" and gate(p)["dau_duong"] == [], f"(iii) vế a: {ghep(p)}")
    p = g1(wf_tu(X), buoc(X, "THU: 4/4 dat"), sua=lambda st: st.append({"name": "Run x", "number": 99, "conclusion": "skipped"}))
    bang(ghep(p) == "a_so_buoc_rest_khac_so_buoc_yaml" and gate(p)["dau_duong"] == [], f"(iv) REST thừa bước: {ghep(p)}")

@ca
def c37_ghep_lech_ten():   # A21 (b): tên REST ≠ tên dự kiến; đối chứng `name:` khác `Run <…>` vẫn khớp
    khong_marker(g1(wf_tu(X), buoc(X, "THU: 4/4 dat"), sua=lambda st: st[2].update(name="Run khac")), "tên lệch", ghep="not_measured")
    p = g1(wf_tu(X, buoc_them={"name": "Kiem tra"}), buoc(X, "THU: 4/4 dat"))
    bang(gate(p)["trang_thai"] == "passed" and ghep(p) == "passed", f"`name:` khớp REST: {gate(p)}")
    ten = lambda t: (lambda st: st[2].update(name=t))  # noqa: E731
    for w, sua, mong, *wr in ((wf_tu(X), list.reverse, "passed"), (wf_tu(X), lambda st: st[2].update(number=2), "steps_rest_sai_dang"),
                              (wf_tu("\n" + X), None, "passed"), (wf_tu(X, buoc_them={"name": "${{ x }}"}), None, "b_ten_buoc_lech"),
                              (wf_tu(X + "  "), None, "passed"), (wf_tu(X, buoc_them={"name": ""}), None, "b_ten_buoc_lech"),
                              (wf_tu(X, buoc_them={"name": "Postgres"}), None, "passed"),
                              (wf_tu(X), lambda st: st[2].update(conclusion="failure"), "passed"),
                              (wf_tu(X, buoc_them={"run": 5}), ten("Run 5"), "b_ten_buoc_lech", wf_tu(X)),
                              (wf_tu(X, buoc_them={"run": 5}), ten(None), "b_ten_buoc_lech", wf_tu(X))):
        bang(ghep(g1(w, buoc(X, "THU: 4/4 dat"), sua=sua, w_rest=(wr or [None])[0])) == mong, f"F10 chốt tên/thứ tự: {w!r} mong {mong}")

@ca
def c38_ghep_lech_gio():   # A22 (c): giờ header ngoài cửa sổ, hoặc started_at/completed_at thiếu/sai dạng ⇒ not_measured, không ném
    for sua in ({"started_at": "2026-10-19T23:45:05Z", "completed_at": "2026-10-19T23:45:06Z"}, {"started_at": None},
                {"completed_at": "2026-10-19T23:45:04.9Z"}, {"started_at": 5}, {"completed_at": "2026-10-19T23:45:03Z"},
                {"started_at": "2026-02-30T00:00:00Z"}, {"completed_at": "2026-13-01T00:00:00Z"}, {"completed_at": "2026-10-19T24:00:00Z"},
                {"completed_at": "2026-10-19T23:99:00Z"}, {"completed_at": "2026-10-19T23:45:99Z"}, {"completed_at": "2026-10-19T23:45:04+00:00"},
                {"completed_at": "2026-10-19T23:45:04Zx"}):
        try:
            p = g1(wf_tu(X), buoc(X, "THU: 4/4 dat"), sua=lambda st, d=sua: st[2].update(d))
        except Exception as e:   # ném ra ngoài CHÍNH LÀ điều ca này đo (vế c phải hỏng êm)
            bang(False, f"giờ {sua}: công cụ ném {type(e).__name__}")
        khong_marker(p, f"giờ {sua}", ghep="not_measured")
    cua_so = {"started_at": "2026-02-28T00:00:00Z", "completed_at": "2026-10-20T00:00:00Z"}   # F09: header thiếu giờ / sai lịch
    for hd in (f"##[group]Run {X}", f"2026-02-30T23:45:04.1Z ##[group]Run {X}"):
        khong_marker(g1(wf_tu(X), [hd] + buoc(X, "THU: 4/4 dat")[1:], sua=lambda st: st[2].update(cua_so)), hd[:12], ghep="not_measured")
    p = g1(wf_tu(X), buoc(X, "THU: 4/4 dat"))   # header 23:45:04.855…Z, cửa sổ [23:45:04Z, 23:45:04Z]: cắt về giây ⇒ trong
    bang(gate(p)["trang_thai"] == "passed", f"đối chứng cắt về giây: {gate(p)['ghep_buoc']}")

@ca
def c39_ghep_job():   # A23 (d): tên job REST khớp 0 / ≥ 2 khoá, `name:` có `${{`, job gọi lại ⇒ not_measured; `k (…)` khớp một ⇒ passed
    for ten, w in (("khac", wf_job(j=({}, None))), ("x (1)", wf_job(x=({}, None), y=({"name": "x"}, None))),
                   ("${{ matrix.n }}", wf_job(j=({"name": "${{ matrix.n }}"}, None))), ("j", wf_job(j=({"uses": "./w.yml"}, None))),
                   ("jx", wf_job(j=({}, None))), ("j x", wf_job(j=({}, None))), (" (1)", wf_job(j=({"name": ""}, None)))):
        try:
            p = g1(w, buoc(X, "THU: 4/4 dat"), ten=ten)
        except Exception as e:   # ném ra ngoài CHÍNH LÀ điều ca này đo
            bang(False, f"job {ten!r}: công cụ ném {type(e).__name__}")
        khong_marker(p, f"job {ten!r}", ghep="not_measured")
        bang(ghep(p) == "d_job_yaml_khong_duy_nhat", f"{ten!r}: {ghep(p)}")
    for ten, w in (("k (ubuntu-latest, 5)", wf_job(k=({}, None), kk=({}, None))), ("j", wf_job(j=({"name": "Build"}, None)))):
        p = g1(w, buoc(X, "THU: 4/4 dat"), ten=ten)   # đối chứng: `k (…)` khớp đúng khoá k; khoá vẫn khớp khi job có `name:`
        bang(gate(p)["trang_thai"] == "passed", f"{ten!r} phải ghép đúng một khoá: {gate(p)['ghep_buoc']}")

@ca
def c40_nhom_long():   # A24 (Q6): nhóm con mở/đóng sau `shell:` rồi dòng màu muộn ⇒ khối không hợp lệ (biểu hiện b r3 lượt 2)
    b = buoc(X, "THU: 4/4 dat")
    khong_marker(g1(wf_tu(X), [*b[:3], f"{T} ##[group]details", b[3], f"{T} \x1b[36;1mecho tail\x1b[0m", b[4]]), "nhóm lồng")

@ca
def c41_buoc_uses():   # A25 (Q8): bước `uses:` không bao giờ sinh marker; composite in nhóm con ⇒ lệch số đếm (biểu hiện a r3 lượt 2)
    khong_marker(g1(wf_tu(X, buoc_them={"uses": "./a"}), buoc(X, "THU: 4/4 dat")), "bước có uses:")
    c = [f"{T} ##[group]Run ./c", f"{T} ##[endgroup]"]
    for cuoi in ([], [buoc(X, "loi")]):
        w = yaml.safe_load(wf_job(j=({}, None), k=({"if": False}, None)))
        w["jobs"]["j"]["steps"][1:] = [{"uses": "./c"}] + [{"run": X + "\n"}] * len(cuoi)
        khong_marker(g1(yaml.safe_dump(w), c, buoc(X, "THU: 4/4 dat"), *cuoi), f"composite + {len(cuoi)} bước sau", ghep="not_measured")

@ca
def c42_github_env_cung_job():   # A26 (Q7): chỉ `run:` ĐỨNG TRƯỚC trong CÙNG job nhắc GITHUB_ENV/GITHUB_PATH mới chặn
    dd = lambda p: [(x["trang_thai"], x.get("ly_do")) for x in gate(p)["dau_duong"]]  # noqa: E731
    for e in ("echo A=1 >> $GITHUB_ENV", "echo /x >> $GITHUB_PATH"):
        bang(dd(g1(wf_tu(e, X), buoc(e), buoc(X, "THU: 4/4 dat"))) == CHAN, f"{e}: đứng trước, cùng job ⇒ chặn")
        w = yaml.safe_load(wf_job(j=({}, None), k=({}, None)))
        w["jobs"]["k"]["steps"].insert(1, {"run": e + "\n"})
        bang(dd(g1(yaml.safe_dump(w), buoc(X, "THU: 4/4 dat"))) == [("passed", None)], f"{e}: job khác ⇒ đo được")
        bang(dd(g1(wf_tu(X, e), buoc(X, "THU: 4/4 dat"), buoc(e))) == [("passed", None)], f"{e}: đứng sau ⇒ đo được")
    x2 = "python ops/GITHUB_PATH_test.py"
    bang(dd(g1(wf_tu(x2), buoc(x2, "THU: 4/4 dat"), them={x2[7:]: r"^THU: (\d+)/(\d+) dat$"})) == [("passed", None)], "chính bước i")

@ca
def c44_ghep_sai_dang():   # mọi chốt DẠNG của ghép: steps REST / bước YAML / job lạ ⇒ not_measured (job lạ khác: bỏ qua), KHÔNG ném
    w0, sai = wf_tu(X), "steps_rest_sai_dang"
    d, buoc_list = "d_job_yaml_khong_duy_nhat", lambda v: (lambda w: w["jobs"]["j"].update(steps=v))  # noqa: E731
    for sua, them, mong in ((lambda st: st[2].pop("number"), None, sai), (lambda st: st[2].update(number=True), None, sai),
                            (lambda st: st[2].update(number=0), None, sai), (lambda st: st[2].update(number=-1), None, sai),
                            (lambda st: st.append(1), None, sai), (None, lambda w: w["jobs"].update(z="x"), "passed"),
                            (None, lambda w: w["jobs"].update(z={"name": 5}), "passed"),
                            (None, lambda w: w["jobs"]["j"]["steps"].append("chuoi"), d), (None, buoc_list(None), d),
                            (None, buoc_list(3), d), (None, lambda w: w["jobs"]["j"].pop("steps"), d),
                            (lambda st: st[2].update(name="K"), lambda w: w["jobs"]["j"]["steps"][1].update(name="K", run=[X]), "passed"),
                            (lambda st: st[2].update(name="5"), lambda w: w["jobs"]["j"]["steps"][1].update(name=5), "b_ten_buoc_lech")):
        w = yaml.safe_load(w0)
        if them:
            them(w)
        try:
            p = g1(yaml.safe_dump(w), buoc(X, "THU: 4/4 dat"), sua=sua, w_rest=w0)
        except Exception as e:   # ném ra ngoài CHÍNH LÀ điều ca này đo
            bang(False, f"{them or mong}: công cụ ném {type(e).__name__}")
        bang(ghep(p) == mong and (gate(p)["trang_thai"] == "passed") == ("z" in w["jobs"]), f"{mong}: {ghep(p)} {gate(p)['dau_duong']}")

@ca
def c45_buoc_skipped_giua():   # bước `skipped` ĐỨNG TRƯỚC: tên vẫn phải khớp; giờ và vị trí lấy từ bước REST ĐÃ CHẠY cùng thứ tự
    w = yaml.safe_load(wf_tu("echo a", X))
    w["jobs"]["j"]["steps"][1]["if"] = "false"
    bo = lambda st: st[2].update(conclusion="skipped", started_at="2026-10-19T23:00:00Z", completed_at="2026-10-19T23:00:00Z")  # noqa: E731
    p = g1(yaml.safe_dump(w), buoc(X, "THU: 4/4 dat"), sua=bo)
    bang(gate(p)["trang_thai"] == "passed" and [x["trang_thai"] for x in gate(p)["dau_duong"]] == ["passed"], f"skipped trước: {gate(p)}")
    p = g1(yaml.safe_dump(w), buoc(X, "THU: 4/4 dat"), sua=lambda st: (bo(st), st[2].update(name="Run khac")))
    bang(ghep(p) == "b_ten_buoc_lech", f"bước skipped sai tên vẫn phải làm hỏng vế b: {ghep(p)}")

@ca
def c46_mien_che_do():   # miền giá trị của chặn chế độ: mỗi biến thể đổi MỘT trục, có cả chặn lẫn đối chứng cho phép
    x, ok = f"python {DUONG_GIA}", [("passed", None)]
    for ten, w, mong in (("env job []", wf_tu(x, job_them={"env": []}), CHAN), ("env job list", wf_tu(x, job_them={"env": ["A"]}), CHAN),
                         ("env job biểu thức", wf_tu(x, job_them={"env": "${{ x }}"}), CHAN), ("env job {}", wf_tu(x, job_them={"env": {}}), ok), ("env job null (D01)", wf_tu(x, job_them={"env": None}), CHAN),
                         ("env workflow null (D01)", wf_tu(x, goc_them={"env": None}), CHAN),
                         ("env workflow dict", wf_tu(x, goc_them={"env": {"A": "1"}}), ok),
                         ("defaults workflow {}", wf_tu(x, goc_them={"defaults": {}}), CHAN), ("defaults job {}", wf_tu(x, job_them={"defaults": {}}), CHAN),
                         ("shell null", wf_tu(x, buoc_them={"shell": None}), CHAN), ("shell sh", wf_tu(x, buoc_them={"shell": "sh"}), ok),
                         ("shell pwsh", wf_tu(x, buoc_them={"shell": "pwsh"}), ok)) + tuple(
            (f"khoá {k}", wf_tu(x, buoc_them={k: v}), ok) for k, v in (("id", "a"), ("if", "true"), ("timeout-minutes", 5), ("continue-on-error", False))):
        bang(che_do(w) == mong, f"{ten}: {che_do(w)} ≠ {mong}")
    kb = ["A=1 " + x, "python ops/khac.py"]
    p = g1(wf_tu("\n".join(kb)), khoi(kb, "THU: 4/4 dat"))
    bang([x.get("ly_do") for x in gate(p)["dau_duong"]] == ["che_do_khong_xac_dinh", "khong_co_trong_MOI"], f"VAR= một dòng: {gate(p)['dau_duong']}")

@ca
def c47_bien_ghep():   # biên của ghép + xác thực khối: mỗi biến thể một chốt; ca cần marker thì đòi MARKER, không chỉ đòi ghép
    dd = lambda p: [(x["trang_thai"], x.get("ly_do")) for x in gate(p)["dau_duong"]]  # noqa: E731
    ok, e, b = [("passed", None)], "echo A=1 >> $GITHUB_ENV", buoc(X, "THU: 4/4 dat")
    for ten, p, mong in (("number bool", g1(wf_tu(X), b, sua=lambda st: st[0].update(number=True)), "steps_rest_sai_dang"),
                         ("number float", g1(wf_tu(X), b, sua=lambda st: st[2].update(number=2.5)), "steps_rest_sai_dang"),
                         ("alias name:", g1(wf_job(j=({"name": "Build"}, None)), b, ten="Build"), "passed"),
                         ("ma trận rỗng", g1(wf_tu(X), b, ten="j ()"), "passed"),
                         ("ma trận xuống dòng", g1(wf_tu(X), b, ten="j (a\nb)"), "d_job_yaml_khong_duy_nhat"),
                         ("Post ở giữa tên", g1(wf_tu(X, buoc_them={"name": "Chay Post x"}), b), "passed")):
        bang(ghep(p) == mong, f"{ten}: {ghep(p)} ≠ {mong}")
    w0 = yaml.safe_dump({"jobs": {"j": {"runs-on": "x", "steps": [{"run": e + "\n"}, {"run": X + "\n"}]}}})
    for ten, p, mong in (("khoảng trắng cuối run:", g1(wf_tu(X + "  "), buoc(X + "  ", "THU: 4/4 dat")), ok),
                         ("hai dòng trùng", g1(wf_tu(X + "\n" + X), khoi([X, X], "THU: 4/4 dat")), ok),
                         ("GITHUB_ENV ở bước ĐẦU", g1(w0, buoc(e), b, nen=LINUX_KHONG_SETUP), CHAN),
                         ("GITHUB_ENV cách một bước", g1(wf_tu(e, "echo b", X), buoc(e), buoc("echo b"), b), CHAN),
                         ("##[endgroup] có đuôi", g1(wf_tu(X), b[:3] + [f"{T} ##[endgroup]x"] + b[4:]), []),
                         ("shell: thiếu dấu cách", g1(wf_tu(X), b[:2] + [f"{T} shell:/usr/bin/bash"] + b[3:]), [])):
        bang(dd(p) == mong and ghep(p) == "passed", f"{ten}: {dd(p)} ≠ {mong} (ghép {ghep(p)})")
    w = yaml.safe_load(wf_tu(X))
    w["jobs"]["j"]["steps"][1] = {"name": "K", "run": 5}
    try:   # `run:` không phải chuỗi mà khối in lại trùng str(run) ⇒ không marker, KHÔNG ném
        p = g1(yaml.safe_dump(w), buoc("5", "THU: 4/4 dat"), sua=lambda st: st[2].update(name="K"), w_rest=wf_tu(X))
    except Exception as ex:   # ném ra ngoài CHÍNH LÀ điều vế này đo
        bang(False, f"run: 5 ⇒ công cụ ném {type(ex).__name__}")
    bang(dd(p) == [] and ghep(p) == "passed", f"run: 5: {dd(p)}")

def bien_dang(x):   # mọi biến dạng "gần" của một hằng chuỗi: hậu tố, bớt ký tự cuối, hoa/thường, khoảng trắng hai đầu
    return list(dict.fromkeys(v for v in (x + "x", x[:-1], x.upper(), x.lower(), x.swapcase(), " " + x, x + " ") if v != x))

@ca
def c48_nguyen_van_va_mien():   # F10: MỖI hằng chuỗi / tập liệt kê của r4 qua bảng biến dạng; kỳ vọng = định nghĩa NGUYÊN VĂN của spec
    dd = lambda p: [(x["trang_thai"], x.get("ly_do")) for x in gate(p)["dau_duong"]]  # noqa: E731
    ok, b, a_so, d_job, b_ten = [("passed", None)], buoc(X, "THU: 4/4 dat"), "a_so_nhom_khac_so_buoc_rest_chay", "d_job_yaml_khong_duy_nhat", "b_ten_buoc_lech"
    hang = []   # (tên, p, ghép mong, marker mong)
    for t in ["Set up job", "Complete job"] + [v for x in ("Set up job", "Complete job") for v in bien_dang(x)]:
        hang.append((f"bước tên {t!r}", g1(wf_tu(X, buoc_them={"name": t}), b), *((a_so, []) if t in ("Set up job", "Complete job") else ("passed", ok))))
    for t in ("Post x", "Post  x", "Postx", "post x", " Post x", "POST x", "Post"):
        hang.append((f"bước tên {t!r}", g1(wf_tu(X, buoc_them={"name": t}), b), *((a_so, []) if t.startswith("Post ") else ("passed", ok))))
    for t in ["K"] + bien_dang("K k"):
        hang.append((f"name: {t!r} REST lệch", g1(wf_tu(X, buoc_them={"name": "K k"}), b, sua=lambda st, t=t: st[2].update(name=t)),
                     *(("passed", ok) if t == "K k" else (b_ten, []))))
    for t in bien_dang("Run " + X):
        hang.append((f"tên REST {t!r}", g1(wf_tu(X), b, sua=lambda st, t=t: st[2].update(name=t)), b_ten, []))
    for c in ("success", "failure", "neutral", "cancelled", "timed_out", "Skipped", "SKIPPED"):
        hang.append((f"conclusion {c}", g1(wf_tu(X), b, sua=lambda st, c=c: st[2].update(conclusion=c)), "passed", ok))
    hang.append(("skipped mà có nhóm", g1(wf_tu(X), b, sua=lambda st: st[2].update(conclusion="skipped")), a_so, []))
    for ten in ["Build", "B.ild (1)", "Build (1)", "Build ()"] + bien_dang("Build") + ["Build(1)", "Build  (1)", "Build (1) ", "Bxild"]:
        al = "B.ild" if "." in ten or ten == "Bxild" else "Build"
        hang.append((f"job {ten!r} / alias {al!r}", g1(wf_job(j=({"name": al}, None)), b, ten=ten),
                     *(("passed", ok) if re.fullmatch(r"(Build|B\.ild)( \(.*\))?", ten) else (d_job, []))))
    for ten, mong in ((" Build ", ("passed", ok)), ("Build", (d_job, []))):   # alias có khoảng trắng hai đầu: so NGUYÊN VĂN, không strip
        hang.append((f"alias ' Build ' / REST {ten!r}", g1(wf_job(j=({"name": " Build "}, None)), b, ten=ten), *mong))
    for k in ["CI_DANG_KY_", "CI_DANG_KY_X"] + bien_dang("CI_DANG_KY_") + ["XCI_DANG_KY_X"]:
        hang.append((f"env job khoá {k!r}", g1(wf_tu(X, job_them={"env": {k: "1"}}), b), "passed", CHAN if k.startswith("CI_DANG_KY_") else ok))
    for sh in ["bash", "pwsh", "sh", None] + [v for x in ("bash", "pwsh", "sh") for v in bien_dang(x)]:
        hang.append((f"shell {sh!r}", g1(wf_tu(X, buoc_them={"shell": sh}), b), "passed", ok if sh in ("bash", "pwsh", "sh") else CHAN))
    for k, v in (("id", "a"), ("if", "true"), ("timeout-minutes", 5), ("continue-on-error", False), ("env", {}), ("with", {}),
                 ("working-directory", "."), ("Name", "n"), ("ID", "a")):
        hang.append((f"khoá bước {k!r}", g1(wf_tu(X, buoc_them={k: v}), b), "passed", ok if k in ("id", "if", "timeout-minutes", "continue-on-error") else CHAN))
    w = yaml.safe_load(wf_tu("echo A=1 >> $GITHUB_ENV", X))
    w["jobs"]["j"]["steps"][1]["if"] = "false"   # bước nhắc GITHUB_ENV đứng trước mà SKIPPED: Q7 không đòi "đã chạy"
    hang.append(("GITHUB_ENV trước, skipped", g1(yaml.safe_dump(w), b, sua=lambda st: st[2].update(conclusion="skipped")), "passed", CHAN))
    for ten, dong in (("header 2 dấu cách", [f"{T} ##[group]Run  {X}"] + b[1:]), ("shell: đầu có cách", b[:2] + [f"{T}  shell: /usr/bin/bash -e {{0}}"] + b[3:]),
                      ("endgroup đầu có cách", b[:3] + [f"{T}  ##[endgroup]"] + b[4:]), ("shell: hoa", b[:2] + [f"{T} Shell: /usr/bin/bash"] + b[3:])):
        hang.append((ten, g1(wf_tu(X), dong), "passed", []))
    hang.append(("run: dòng đầu rỗng", g1(wf_tu("\n" + X), b), "passed", []))
    e, w1 = "echo A=1 >> ", lambda them: yaml.safe_dump(yaml.safe_load(wf_tu(X)) | them)  # noqa: E731
    for ten, w, dong, sua, g, m in (
            ("dòng đầu có \\r", wf_tu(X, buoc_them={"run": "a\rb\n" + X}), None, None, "passed", []),
            ("defaults: null workflow", w1({"defaults": None}), None, None, "passed", CHAN),
            ("defaults: null job", wf_tu(X, job_them={"defaults": None}), None, None, "passed", CHAN),
            ("github_env chữ thường đứng trước", wf_tu(e + "$github_env", X), [buoc(e + "$github_env"), b], None, "passed", ok),
            ("GITHUB_PATH không có $", wf_tu("echo GITHUB_PATH", X), [buoc("echo GITHUB_PATH"), b], None, "passed", CHAN),
            ("mã màu 36m (không ;1m)", wf_tu(X), [[b[0], f"{T} \x1b[36m{X}\x1b[0m"] + b[2:]], None, "passed", []),
            ("header ##[group]run thường", wf_tu(X), [[f"{T} ##[group]run {X}"] + b[1:]], None, a_so, []),
            ("##[GROUP] hoa sau shell:", wf_tu(X), [b[:3] + [f"{T} ##[GROUP]x"] + b[3:]], None, "passed", ok),
            ("run: có \\r cuối", wf_tu(X, buoc_them={"run": X + "\r"}), None, None, "passed", []),
            ("giờ REST thiếu Z", wf_tu(X), None, lambda st: st[2].update(started_at="2026-10-19T23:45:04"), "c_gio_header_ngoai_cua_so", []),
            ("uses: rỗng ở bước", wf_tu(X, buoc_them={"uses": ""}), None, None, "passed", []),
            ("uses: rỗng ở job", wf_tu(X, job_them={"uses": ""}), None, None, d_job, []),
            ("name: null", wf_tu(X, buoc_them={"name": None}), None, None, b_ten, []),
            ("run: rỗng kèm uses:", wf_tu(X, buoc_them={"run": "", "uses": "./a"}), None, lambda st: st[2].update(name="Run ./a"), b_ten, []),
            ("dấu cách sau dấu nối dòng cuối", wf_tu(X, buoc_them={"run": X + " \\ "}), [khoi([X + " \\ "], "THU: 4/4 dat")], None, "passed", []),
            ("màu không có mã reset", wf_tu(X), [[b[0], f"{T} \x1b[36;1m{X}"] + b[2:]], None, "passed", ok),
            ("run: hai \\n cuối, khối một dòng", wf_tu(X + "\n"), None, None, "passed", ok),
            ("run: hai \\n cuối, khối có dòng màu rỗng", wf_tu(X + "\n"), [khoi([X, ""], "THU: 4/4 dat")], None, "passed", []),
            ("uses: có khoảng trắng hai đầu", yaml.safe_dump({"jobs": {"j": {"runs-on": "x", "steps": [{"uses": "actions/setup-python@v5"},
             {"uses": " ./a "}]}}}), [[f"{T} ##[group]Run  ./a ", f"{T} ##[endgroup]"]], None, "passed", [])):
        hang.append((ten, g1(w, *(dong or [b]), sua=sua), g, m))
    sai = [(ten, ghep(p), dd(p), g, m) for ten, p, g, m in hang if (ghep(p), dd(p)) != (g, m)]
    bang(not sai and len(hang) > 80, f"{len(sai)}/{len(hang)} biến dạng lệch định nghĩa: {sai[:3]}")

ENV_MIEN = ("vang", None, {}, {"A": "1"}, {"CI_DANG_KY_X": ""}, {"A": "1", "CI_DANG_KY_": "x", "B": ""}, [], "${{ x }}", 0, False, "")
GHI = ("echo A=1 >> $GITHUB_ENV", "echo /x >> $GITHUB_PATH", 'echo A=1 >> "$GITHUB_ENV"; true', "echo MYGITHUB_PATHX")
SHELL_MIEN = ("vang", "bash", "pwsh", "sh", "zsh", None, " bash", "Bash")

def oracle_chan(wf, job, i):   # đọc THẲNG định nghĩa "Chặn chế độ" của spec r4 (+ D01), không gọi hàm nào của công cụ
    env_xau = lambda d: "env" in d and (not isinstance(d["env"], dict) or any(str(k)[:11] == "CI_DANG_KY_" for k in d["env"]))  # noqa: E731
    s = job["steps"][i]
    return ("defaults" in wf or env_xau(wf) or "defaults" in job or env_xau(job) or any(k not in ("name", "id", "if", "run", "shell",
            "timeout-minutes", "continue-on-error") for k in s) or s.get("shell", "bash") not in ("bash", "pwsh", "sh")
            or any("GITHUB_ENV" in str(t.get("run", "")) or "GITHUB_PATH" in str(t.get("run", "")) for t in job["steps"][:i]))

def oracle_job(ten, wf):   # định nghĩa "Job YAML của job REST" bằng phép so CHUỖI (không regex): đúng một khoá ⇒ khoá, không thì None
    khop = [k for k, j in wf["jobs"].items() if any(isinstance(x, str) and x and "${{" not in x and (ten == x or ten.startswith(x + " (")
            and ten.endswith(")")) for x in (k, j.get("name")))]
    return khop[0] if len(khop) == 1 else None

def kich_ban(rd, so):   # một workflow nhiều job; job đích ở vị trí ngẫu nhiên; mỗi bước một kiểu; trả (wf, tên REST, steps REST, log, them MOI, mong)
    gan = lambda d, k, v: d.update({k: v}) if v != "vang" else None  # noqa: E731
    wf, them, jobs = {}, {}, {}
    for jx in range(rd.randint(1, 3)):
        ds, co_setup = [], rd.random() < 0.7
        if co_setup:
            ds.append({"uses": "actions/setup-python@v5"})
        for bx in range(rd.randint(0 if not co_setup else 1, 9)):
            kieu = rd.choices(("goi", "ghi", "khac", "ghi_list"), (0.68, 0.15, 0.13, 0.04))[0]
            duong = f"ops/g{so}_{jx}_{bx}_test.py"
            run = {"goi": ("A=1 " if rd.random() < 0.1 else "") + f"python {duong}" + (" --x" if rd.random() < 0.1 else ""),
                   "ghi": rd.choice(GHI), "khac": "echo hi", "ghi_list": "echo"}[kieu]
            b = {"name": f"N{bx}", "run": ["echo $GITHUB_ENV"]} if kieu == "ghi_list" else {"run": run + "\n"}   # run: không phải chuỗi
            if rd.random() < 0.15:
                b["if"] = "false"
            if rd.random() < 0.1:
                b["env"] = rd.choice(({}, {"A": "1"}))
            if rd.random() < 0.15:
                gan(b, "shell", rd.choice(SHELL_MIEN))
            if rd.random() < 0.05:
                b["working-directory"] = "."
            ds.append(b)
            them[duong] = r"^THU: (\d+)/(\d+) dat$"
        j = {"runs-on": "x", "steps": ds}
        if rd.random() < 0.2:
            gan(j, "env", rd.choice(ENV_MIEN))
        if rd.random() < 0.05:
            j["defaults"] = rd.choice(({}, None))
        jobs[f"j{jx}"] = j
    for jx, j in enumerate(jobs.values()):   # alias `name:`: thường riêng, đôi khi TRÙNG khoá của job khác (đích không duy nhất)
        if rd.random() < 0.25:
            j["name"] = rd.choice([f"Build {jx}", f"j{rd.randrange(len(jobs))}"])
    wf["jobs"] = jobs
    if rd.random() < 0.15:
        gan(wf, "env", rd.choice(ENV_MIEN))
    if rd.random() < 0.04:
        wf["defaults"] = {}
    k = rd.choice(list(jobs))
    job, lg, st, mong, n = jobs[k], (LINUX if jobs[k]["steps"][:1] == [{"uses": "actions/setup-python@v5"}] else LINUX_KHONG_SETUP), [], [], 1
    st.append({"name": "Set up job", "number": 1, "conclusion": "success", "started_at": "2026-10-19T23:40:00Z", "completed_at": "2026-10-19T23:40:00Z"})
    for i, b in enumerate(job["steps"]):
        n += 1
        ten = b.get("name") or "Run " + (b.get("run") or b["uses"]).split("\n")[0]
        if b.get("if") == "false":
            st.append({"name": ten, "number": n, "conclusion": "skipped", "started_at": "2026-10-19T23:00:00Z", "completed_at": "2026-10-19T23:00:00Z"})
            continue
        if not isinstance(b.get("run", ""), str):   # bước `name:` + `run:` list đã chạy: có nhóm log, không bao giờ xác thực
            gio = f"2026-10-19T23:50:{n:02d}Z"
            lg += "".join(f"{gio[:-1]}.5Z {x}\n" for x in ["##[group]Run echo", "\x1b[36;1mecho\x1b[0m", "shell: /usr/bin/bash -e {0}", "##[endgroup]"])
            st.append({"name": ten, "number": n, "conclusion": "success", "started_at": gio, "completed_at": gio})
            continue
        if "uses" in b:
            gio = "2026-10-19T23:40:18Z"
        else:
            gio, lenh = f"2026-10-19T23:50:{n:02d}Z", b["run"].rstrip("\n")
            ra = rd.choice(("THU: 4/4 dat", "THU: 3/4 dat"))
            lg += "".join(f"{gio[:-1]}.5Z {x}\n" for x in [f"##[group]Run {lenh}", f"\x1b[36;1m{lenh}\x1b[0m", "shell: /usr/bin/bash -e {0}",
                                                            "##[endgroup]", ra])
            g = RE_GOI_ORACLE.fullmatch(lenh)
            if g:
                mong.append(("not_measured", "che_do_khong_xac_dinh") if oracle_chan(wf, job, i) or g[1] else ("passed" if ra[5] == "4" else "failed", None))
        st.append({"name": ten, "number": n, "conclusion": "success", "started_at": gio, "completed_at": gio})
    st.append({"name": "Complete job", "number": n + 1, "conclusion": "success", "started_at": "2026-10-19T23:59:00Z", "completed_at": "2026-10-19T23:59:00Z"})
    ghep, nhieu = "passed", rd.random()
    vi = [x for x in st[1:-1] if x["conclusion"] != "skipped" and x["name"] != "Run actions/setup-python@v5"]
    if nhieu < 0.08 and vi:   # cửa sổ giờ của MỘT bước đã chạy nằm SAU hoặc TRƯỚC header (bất kỳ vị trí nào, không chỉ bước cuối)
        rd.choice(vi).update(rd.choice(({"started_at": "2026-10-19T23:58:00Z", "completed_at": "2026-10-19T23:58:01Z"},
                                        {"started_at": "2026-10-19T23:01:00Z", "completed_at": "2026-10-19T23:01:01Z"})))
        ghep, mong = "c_gio_header_ngoai_cua_so", []
    elif nhieu < 0.16 and len(st) > 2:   # tên REST lệch ở MỘT vị trí bất kỳ (kể cả bước skipped)
        rd.choice(st[1:-1])["name"] = "Run khac_x"
        ghep, mong = "b_ten_buoc_lech", []
    elif nhieu < 0.22:   # `number` float nguyên ⇒ không phải số nguyên REST
        rd.choice(st)["number"] += 0.0
        ghep, mong = "steps_rest_sai_dang", []
    ten = rd.choice([k, f"{k} (ubuntu-latest, {so})", f"{k} ({'x' * 90})"] + ([job["name"]] if "name" in job else []))
    if oracle_job(ten, wf) != k:   # tên REST không định danh DUY NHẤT job đích ⇒ vế d hỏng trước mọi vế khác
        ghep, mong = ("d_job_yaml_khong_duy_nhat", []) if oracle_job(ten, wf) is None else (None, None)
    return yaml.safe_dump(wf, allow_unicode=True), ten, st, lg, them, ghep, mong

RE_GOI_ORACLE = re.compile(r"(A=1 )?python ops/g\d+_\d+_\d+_test\.py")   # lời gọi tối giản của bộ sinh: KHÔNG đối số sau script

@ca
def c49_oracle_nhieu_truc():   # F10 đóng LỚP: 250 kịch bản ngẫu nhiên (hạt giống cố định) qua oracle độc lập; so TRỌN danh sách marker
    rd, sai, phu = random.Random(899), [], collections.Counter()
    for so in range(250):
        w, ten, st, lg, them, ghep_mong, mong = kich_ban(rd, so)
        phu.update([f"ghep:{ghep_mong}"] + [x[0] if x[1] is None else x[1] for x in mong or []] + ["job_dich_khong_dau"] * (list(yaml.safe_load(w)["jobs"]).index(
            ten.split(" (")[0]) > 0 if ten.split(" (")[0] in yaml.safe_load(w)["jobs"] else 0) + ["number>=10"] * (max(x["number"] for x in st) >= 10))
        if ghep_mong is None:   # tên REST trỏ DUY NHẤT một job KHÁC: ngoài phạm vi oracle, bỏ kịch bản (đếm ở dưới)
            continue
        try:
            p = chay([(job(1, name=ten, steps=st), lg)], wf=w, them=them)[2]
        except Exception as e:   # ném ra ngoài CHÍNH LÀ điều ca này đo
            sai.append((so, ten, type(e).__name__))
            continue
        dd = [(x["trang_thai"], x.get("ly_do")) for x in gate(p)["dau_duong"]]
        if (ghep(p), dd) != (ghep_mong, mong):
            sai.append((so, ten, ghep(p), ghep_mong, dd, mong))
    thieu = [k for k in ("passed", "failed", "che_do_khong_xac_dinh", "ghep:passed", "ghep:d_job_yaml_khong_duy_nhat", "ghep:b_ten_buoc_lech",
                         "ghep:c_gio_header_ngoai_cua_so", "ghep:steps_rest_sai_dang", "job_dich_khong_dau", "number>=10") if phu[k] < 5]
    bang(not sai and not thieu, f"{len(sai)}/250 kịch bản lệch oracle; đầu tiên: {sai[:2]}; phân hoạch lấy mẫu < 5: {thieu} {dict(phu)}")

@ca
def c50_mien_luot6():   # F10 lượt 6: miền tên job · hình dạng REST · lịch · nguồn chặn · đầu ra log; mỗi hàng một đầu vào spec ĐỊNH NGHĨA
    dd = lambda p: [(x["trang_thai"], x.get("ly_do")) for x in gate(p)["dau_duong"]]  # noqa: E731
    ok, b, c_gio, b_ten = [("passed", None)], buoc(X, "THU: 4/4 dat"), "c_gio_header_ngoai_cua_so", "b_ten_buoc_lech"
    def gio(tem, sua=None):   # cùng khối, mọi dòng đổi sang timestamp `tem`; REST sinh lại từ log (cửa sổ = header) rồi `sua`
        return g1(wf_tu(X), [d.replace(T, tem) for d in b], sua=(lambda st: st[2].update(sua)) if sua else None)
    w_rong = yaml.safe_dump({"jobs": {"j": {"runs-on": "x", "steps": []}}})
    w_sk = yaml.safe_load(wf_tu("echo bo", X))
    w_sk["jobs"]["j"]["steps"][1]["if"] = "false"
    w_uses = yaml.safe_load(wf_tu(X))
    w_uses["jobs"]["j"]["steps"][0] = {"uses": "./GITHUB_PATH"}
    lg_uses = log_voi(b).replace("Run actions/setup-python@v5", "Run ./GITHUB_PATH")
    w_ten = yaml.safe_dump({"jobs": {"j": {"runs-on": "x", "steps": [{"uses": "actions/setup-python@v5"},
                                                                     {"name": "set GITHUB_ENV", "run": "echo hi\n"}, {"run": X + "\n"}]}}})
    m3 = [f"{T} ##[group]Run {X}", f"{T} \x1b[36;1m{X}\x1b[0m", f"{T} \x1b[36;1m##[endgroup]\x1b[0m", f"{T} shell: /usr/bin/bash -e {{0}}",
          f"{T} ##[endgroup]", f"{T} THU: 4/4 dat"]
    hang = (("job hậu tố Unicode", lambda: g1(wf_tu(X), b, ten="j (Việt Nam)"), "passed", ok),
            ("job hậu tố lồng ngoặc", lambda: g1(wf_tu(X), b, ten="j (ubuntu (64))"), "passed", ok),
            ("alias dài 46 ký tự", lambda: g1(wf_job(j=({"name": "Build " + "a" * 40}, None)), b, ten="Build " + "a" * 40), "passed", ok),
            ("REST steps rỗng, YAML rỗng", lambda: chay([(job(1, steps=[]), LINUX_KHONG_SETUP)], wf=w_rong)[2], "passed", []),
            ("number ≥ 100", lambda: g1(wf_tu(X), b, sua=lambda st: [x.update(number=x["number"] + 100) for x in st]), "passed", ok),
            ("number không bắt đầu từ 1", lambda: g1(wf_tu(X), b, sua=lambda st: [x.update(number=x["number"] + 1) for x in st]), "passed", ok),
            ("bước skipped thiếu giờ", lambda: g1(yaml.safe_dump(w_sk), b, sua=lambda st: st[2].update(conclusion="skipped", started_at=None,
                                                                                                 completed_at=None)), "passed", ok),
            ("cửa sổ qua hai ngày", lambda: gio(T, {"started_at": "2026-10-18T23:45:04Z", "completed_at": "2026-10-20T23:45:04Z"}), "passed", ok),
            ("29/2 năm nhuận", lambda: gio("2024-02-29T23:45:04.8553236Z"), "passed", ok),
            ("năm 1999", lambda: gio("1999-12-31T23:45:04.8553236Z"), "passed", ok),
            ("29/2 năm không nhuận ở REST", lambda: gio("2026-03-01T23:45:04.8553236Z", {"started_at": "2026-02-29T23:45:04Z"}), c_gio, []),
            ("name: null, REST 'None'", lambda: g1(wf_tu(X, buoc_them={"name": None}), b, sua=lambda st: st[2].update(name="None")), b_ten, []),
            ("conclusion null vẫn là đã chạy", lambda: g1(wf_tu(X), b, sua=lambda st: st[2].update(conclusion=None)), "passed", ok),
            ("uses: trước nhắc GITHUB_PATH (không phải run:)", lambda: chay([(job(1, steps=buoc_rest(lg_uses, yaml.safe_dump(w_uses))), lg_uses)],
                                                                    wf=yaml.safe_dump(w_uses))[2], "passed", ok),
            ("name: trước nhắc GITHUB_ENV, run: không", lambda: g1(w_ten, buoc("echo hi"), b), "passed", ok),
            ("marker sau một dòng ghi chú", lambda: g1(wf_tu(X), buoc(X, "ghi chu", "THU: 4/4 dat")), "passed", ok),
            ("marker trước một dòng ghi chú", lambda: g1(wf_tu(X), buoc(X, "THU: 4/4 dat", "ghi chu")), "passed", ok),
            ("marker có khoảng trắng đầu", lambda: g1(wf_tu(X), buoc(X, "  THU: 4/4 dat")), "passed", [("failed", None)]),
            ("MOI nhiều dòng theo thứ tự", lambda: g1(wf_tu(X), buoc(X, "START", "THU: 4/4 dat", "END"),
                                              them={DUONG_GIA: r"^START\nTHU: (\d+)/(\d+) dat\nEND$"}), "passed", ok),
            ("dòng không màu trước shell:", lambda: g1(wf_tu(X), b[:2] + [f"{T}   NOTE: x"] + b[2:]), "passed", []),
            ("dòng không màu sau shell:", lambda: g1(wf_tu(X), b[:3] + [f"{T}   NOTE: x"] + b[3:]), "passed", ok),
            ("##[endgroup] màu trong khối", lambda: g1(wf_tu(X + "\n##[endgroup]"), m3), "passed", []),
            ("shell: rỗng", lambda: g1(wf_tu(X), b[:2] + [f"{T} shell: "] + b[3:]), "passed", ok),
            ("mã màu không ở đầu dòng", lambda: g1(wf_tu(X), [b[0], f"{T} \x1b[0m\x1b[36;1m{X}\x1b[0m"] + b[2:]), "passed", ok),
            ("dòng màu không timestamp", lambda: g1(wf_tu(X), [b[0], f"\x1b[36;1m{X}\x1b[0m"] + b[2:]), "passed", ok),
            ("dòng trống giữa hai lời gọi", lambda: g1(wf_tu(X + "\n\n" + X), khoi([X, "", X], "THU: 4/4 dat")), "passed", ok),
            ("jobs: {} rỗng", lambda: g1("jobs: {}", b, w_rest=wf_tu(X)), "d_job_yaml_khong_duy_nhat", []))
    sai = []
    for ten, f, g, m in hang:
        try:
            p = f()
        except Exception as e:   # ném ra ngoài CHÍNH LÀ điều hàng này đo
            sai.append((ten, type(e).__name__))
            continue
        if (ghep(p), dd(p)) != (g, m) or ten == "##[endgroup] màu trong khối" and kb(p)["buoc_xac_thuc"] != 0:
            sai.append((ten, ghep(p), dd(p), kb(p)["buoc_xac_thuc"], g, m))
    bang(not sai, f"{len(sai)}/{len(hang)} hàng lệch định nghĩa: {sai[:3]}")

@ca
def c51_mien_luot7():   # F10 lượt 7: Unicode · lịch biên · metadata · env giá trị/khoá · nguồn chặn · NỘI DUNG bằng chứng · cấu trúc log
    dd = lambda p: [(x["trang_thai"], x.get("ly_do")) for x in gate(p)["dau_duong"]]  # noqa: E731
    ok, b, c_gio, M3 = [("passed", None)], buoc(X, "THU: 4/4 dat"), "c_gio_header_ngoai_cua_so", ["START", "THU: 4/4 dat", "END"]
    def gio(tem=T, sua=None):
        return g1(wf_tu(X), [d.replace(T, tem) for d in b], sua=(lambda st: st[2].update(sua)) if sua else None)
    def moi(*ra, mau):   # MOI regex nhiều dòng: đo NỘI DUNG + THỨ TỰ phần log, không chỉ trạng thái
        return g1(wf_tu(X), buoc(X, *ra), them={DUONG_GIA: mau})
    def post_dau(st):   # bước `Post …` mang number NHỎ NHẤT: lọc theo TÊN, không theo vị trí số
        hau = next(x for x in st if x["name"].startswith("Post "))
        for x in st:
            x["number"] += 1
        hau["number"] = 1
    w_tr = yaml.safe_load(wf_tu("echo GITHUB_ENV", X))
    w_tr["jobs"]["j"]["steps"][1]["uses"] = "./a"   # bước trước có CẢ uses: lẫn run: — nguồn chặn là run:
    b_rong, b_shell2, b_ansi = b[:3] + [f"{T} "] + b[3:], b[:3] + [f"{T} shell: /other"] + b[3:], b[:3] + [f"{T} \x1b[31mNOTE\x1b[0m"] + b[3:]
    hang = (("alias job Unicode", lambda: g1(wf_job(j=({"name": "Xây dựng"}, None)), b, ten="Xây dựng"), "passed", ok, None),
            ("name: bước Unicode", lambda: g1(wf_tu(X, buoc_them={"name": "Xây dựng"}), b), "passed", ok, None),
            ("hậu tố ma trận có dấu chấm", lambda: g1(wf_tu(X), b, ten="j (ubuntu-24.04)"), "passed", ok, None),
            ("cửa sổ qua năm", lambda: gio("2026-12-31T23:45:04.8553236Z", {"started_at": "2026-12-30T00:00:00Z",
                                                                          "completed_at": "2027-01-02T00:00:00Z"}), "passed", ok, None),
            ("29/2/2000 (nhuận thế kỷ)", lambda: gio("2000-02-29T23:45:04.8553236Z"), "passed", ok, None),
            ("năm 9999", lambda: gio("9999-12-31T23:45:04.8553236Z"), "passed", ok, None),
            ("năm 0001", lambda: gio("0001-01-01T23:45:04.8553236Z"), "passed", ok, None),
            ("cửa sổ cùng giờ, khác ngày", lambda: gio(sua={"started_at": "2026-10-20T23:45:04Z", "completed_at": "2026-10-21T23:45:04Z"}), c_gio, [], None),
            ("giờ REST có khoảng trắng cuối", lambda: gio(sua={"started_at": "2026-10-19T23:45:04Z "}), c_gio, [], None),
            ("giờ REST chữ số toàn chiều rộng", lambda: gio(sua={"started_at": "２０２６-10-19T23:45:04Z"}), c_gio, [], None),
            ("giờ REST chữ số Ả Rập", lambda: gio(sua={"completed_at": "2026-10-19T23:45:0٤Z"}), c_gio, [], None),
            ("29/2/1900 (không nhuận) ở REST", lambda: gio("1900-03-01T23:45:04.8553236Z", {"started_at": "1900-02-29T23:45:04Z"}), c_gio, [], None),
            ("metadata không có giờ", lambda: g1(wf_tu(X), b, sua=lambda st: [x.update(started_at=None, completed_at=None) for x in st
                                                                         if x["name"] in ("Set up job", "Complete job") or x["name"].startswith("Post ")]), "passed", ok, None),
            ("bước Post có number nhỏ nhất", lambda: g1(wf_tu(X), b, sua=post_dau), "passed", ok, None),
            ("env CI_DANG_KY_X: null", lambda: g1(wf_tu(X, job_them={"env": {"CI_DANG_KY_X": None}}), b), "passed", CHAN, None),
            ("env khoá rỗng", lambda: g1(wf_tu(X, job_them={"env": {"": "abc"}}), b), "passed", ok, None),
            ("env khoá Unicode", lambda: g1(wf_tu(X, job_them={"env": {"VIỆT": "abc"}}), b), "passed", ok, None),
            ("bước trước uses:+run: nhắc GITHUB_ENV", lambda: g1(yaml.safe_dump(w_tr), buoc("echo GITHUB_ENV"), b), "passed", CHAN, None),
            ("dòng khớp nhiều dòng giữ nguyên thứ tự", lambda: moi(*M3, mau=r"^START\nTHU: (\d+)/(\d+) dat\nEND$"), "passed", ok,
             lambda p: [x["dong_khop"] for x in gate(p)["dau_duong"]] == [M3]),
            ("dòng trống trong output", lambda: moi("START", "", "THU: 4/4 dat", "END", mau=r"^START\n\nTHU: (\d+)/(\d+) dat\nEND$"), "passed", ok, None),
            ("output kết thúc bằng LF", lambda: moi("THU: 4/4 dat", mau=r"^THU: (\d+)/(\d+) dat\n\Z"), "passed", ok, None),
            ("dòng output trùng", lambda: moi("START", "START", "THU: 4/4 dat", mau=r"^START\nSTART\nTHU: (\d+)/(\d+) dat$"), "passed", ok, None),
            ("dòng ##[group] trong output", lambda: moi("##[group]details", "THU: 4/4 dat", mau=r"^##\[group\]details\nTHU: (\d+)/(\d+) dat$"), "passed", ok, None),
            ("lenh/duong_dan của đúng bước", lambda: g1(wf_tu(X), b), "passed", ok,
             lambda p: [(x["lenh"], x["duong_dan"]) for x in gate(p)["dau_duong"]] == [(X, DUONG_GIA)]),
            ("hai bước cùng script, hai kết quả", lambda: g1(wf_tu(X, X), b, buoc(X, "THU: 3/4 dat")), "passed", ok + [("failed", None)],
             lambda p: kb(p)["buoc_xac_thuc"] == 2),   # lượt 9 D04: đếm MỌI bước xác thực, không chỉ bước cuối
            ("marker có khoảng trắng cuối", lambda: g1(wf_tu(X), buoc(X, "THU: 4/4 dat  ")), "passed", [("failed", None)], None),
            ("dòng rỗng sau shell:", lambda: g1(wf_tu(X), b_rong), "passed", ok, None),
            ("shell: thứ hai", lambda: g1(wf_tu(X), b_shell2), "passed", ok, None),
            ("metadata có ANSI khác sau shell:", lambda: g1(wf_tu(X), b_ansi), "passed", ok, None),
            ("không có output", lambda: g1(wf_tu(X), buoc(X)), "passed", [("failed", None)], lambda p: kb(p)["buoc_xac_thuc"] == 1),
            ("run: là 'shell: x'", lambda: g1(wf_tu("shell: x"), buoc("shell: x")), "passed", [], lambda p: kb(p)["buoc_xac_thuc"] == 1))
    sai = []
    for ten, f, g, m, them in hang:
        try:
            p = f()
        except Exception as e:   # ném ra ngoài CHÍNH LÀ điều hàng này đo
            sai.append((ten, type(e).__name__))
            continue
        if (ghep(p), dd(p)) != (g, m) or them and not them(p):
            sai.append((ten, ghep(p), dd(p), g, m))
    bang(not sai, f"{len(sai)}/{len(hang)} hàng lệch định nghĩa: {sai[:3]}")

@ca
def c52_tap_dong():   # tập đột biến đóng: HÌNH DẠNG `ghep_buoc` của M4 ({trang_thai, ly_do?, so_buoc}) · `${{` nguyên văn · kiểu lạ
    m, b = nap(), buoc(X, "THU: 4/4 dat")
    def gh(f):   # trọn dict `ghep_buoc` + số nhóm `##[group]Run` đếm ĐỘC LẬP trên log; ném ⇒ tên lớp (chính là điều hàng đo)
        try:
            p = f()
            return gate(p)["ghep_buoc"]
        except Exception as e:   # ném ra ngoài CHÍNH LÀ điều hàng này đo
            return type(e).__name__
    def khong_dat(f):   # True ⇔ KHÔNG có dấu đầu đường `passed` (ném ⇒ False: lỗi lọt ra CHÍNH là điều hàng đo)
        try:
            return all(x["trang_thai"] != "passed" for x in gate(f())["dau_duong"])
        except Exception:
            return False
    w = yaml.safe_load(wf_tu(X, X))
    w["jobs"]["j"]["steps"][2]["env"] = {"A": "1"}
    hang = (("passed", lambda: g1(wf_tu(X), b), {"trang_thai": "passed", "so_buoc": 2}),
            ("a nhóm ≠ REST chạy", lambda: g1(wf_tu(X, X), b), {"trang_thai": "not_measured", "ly_do": "a_so_nhom_khac_so_buoc_rest_chay",
                                                                "so_buoc": 2}),
            ("a REST ≠ YAML", lambda: g1(yaml.safe_dump(w), b, sua=lambda st: st.pop(3)),
             {"trang_thai": "not_measured", "ly_do": "a_so_buoc_rest_khac_so_buoc_yaml", "so_buoc": 2}),
            ("name: job có `${` (không `${{`)", lambda: g1(wf_job(j=({"name": "a${b"}, None)), b, ten="a${b"),
             {"trang_thai": "passed", "so_buoc": 2}),
            ("name: job `${{x}}` không khoảng trắng", lambda: g1(wf_job(j=({"name": "${{x}}"}, None)), b, ten="${{x}}"),
             {"trang_thai": "not_measured", "ly_do": "d_job_yaml_khong_duy_nhat", "so_buoc": 2}),
            ("name: bước có `${` (không `${{`)", lambda: g1(wf_tu(X, buoc_them={"name": "a${b"}), b), {"trang_thai": "passed", "so_buoc": 2}),
            ("name: bước `${{x}}` không khoảng trắng", lambda: g1(wf_tu(X, buoc_them={"name": "${{x}}"}), b),
             {"trang_thai": "not_measured", "ly_do": "b_ten_buoc_lech", "so_buoc": 2}),
            ("lượt 9 D03: name: job có `${{` ở GIỮA", lambda: g1(wf_job(j=({"name": "Build ${{x}}"}, None)), b, ten="Build ${{x}}"),
             {"trang_thai": "not_measured", "ly_do": "d_job_yaml_khong_duy_nhat", "so_buoc": 2}),
            ("lượt 9 D03: name: bước có `${{` ở GIỮA", lambda: g1(wf_tu(X, buoc_them={"name": "Build ${{x}}"}), b),
             {"trang_thai": "not_measured", "ly_do": "b_ten_buoc_lech", "so_buoc": 2}))
    khoi_mau = [(ten, khong_dat(f)) for ten, f in (   # dinh_nghia `hop_le`: in lại = dòng `36;1m` LIỀN sau header; không màu sau `shell: `
        ("SGR 36;10m không phải 36;1m", lambda: g1(wf_tu(X), [b[0], b[1].replace("36;1m", "36;10m")] + b[2:])),
        ("dòng 36;1m SAU shell:", lambda: g1(wf_tu(X + "\n" + X), [b[0], b[1], b[2], b[1]] + b[3:]))) if not khong_dat(f)]
    bang(not khong_dat(lambda: g1(wf_tu(X + "\n" + X), [b[0], b[1], b[1]] + b[2:])), "đối chứng: hai dòng 36;1m TRƯỚC shell: ⇒ passed")
    K, mu = "python ops/khac.py", {"lenh": X, "duong_dan": DUONG_GIA}
    def dd_tron(f):   # TRỌN danh sách `dau_duong` (M4: khoá lenh · duong_dan · trang_thai · ly_do | dong_khop); ném ⇒ tên lớp
        try:
            return gate(f())["dau_duong"]
        except Exception as e:   # ném ra ngoài CHÍNH LÀ điều hàng này đo
            return type(e).__name__
    dd_sai = [(ten, kq) for ten, f, mong in (
        ("passed", lambda: g1(wf_tu(X), b), [mu | {"trang_thai": "passed", "dong_khop": ["THU: 4/4 dat"]}]),
        ("không có trong MOI", lambda: g1(wf_tu(K), buoc(K, "THU: 4/4 dat")),
         [{"lenh": K, "duong_dan": "ops/khac.py", "trang_thai": "not_measured", "ly_do": "khong_co_trong_MOI"}]),
        ("chặn chế độ", lambda: g1(wf_tu(X, job_them={"defaults": {"run": {"shell": "bash"}}}), b),
         [mu | {"trang_thai": "not_measured", "ly_do": "che_do_khong_xac_dinh"}]),
        ("marker không ở dòng đầu phần log (re.M)", lambda: g1(wf_tu(X), buoc(X, "khac", "THU: 4/4 dat")),
         [mu | {"trang_thai": "passed", "dong_khop": ["THU: 4/4 dat"]}]),
        ("dòng cuối `run:` không phải lời gọi", lambda: g1(wf_tu(X + "\nx"), khoi([X, "x"], "THU: 4/4 dat")), []),
        ("dòng `##[groupx` không phải `##[group]` lồng", lambda: g1(wf_tu(X), b[:3] + [f"{T} ##[groupx"] + b[3:]),
         [mu | {"trang_thai": "passed", "dong_khop": ["THU: 4/4 dat"]}])) if (kq := dd_tron(f)) != mong]
    bang(not dd_sai, f"dau_duong lệch M4: {dd_sai[:2]}")
    sai = [(ten, kq, mong) for ten, f, mong in hang if (kq := gh(f)) != mong]
    try:
        kieu = [m.ten_du_kien(s) for s in ({"run": 5}, {"uses": None}, {}, {"run": ["a"]})] + \
            [m.doc_wf(v) for v in ("jobs: [1]\n", "jobs: null\n", "jobs: x\n", "- 1\n", "[" * 5000 + "]" * 5000)] + [   # lồng sâu ⇒ RecursionError
            m.doc_wf(f"name: {v}\njobs: {{j: {{}}}}\n") for v in ("2026-02-30", "2026-01-01T99:00:00Z", "!!int xyz", "!!float abc",
                                                            "!!bool maybe", "!!int ''", "!!float ''", "!!timestamp abc")]   # F12
        for loi in (OverflowError, LookupError, TypeError):   # lượt 10: đo LỚP — `safe_load` ném lớp bất kỳ ⇒ None
            m.yaml = types.SimpleNamespace(safe_load=lambda v, loi=loi: (_ for _ in ()).throw(loi("tiem")), YAMLError=yaml.YAMLError)
            kieu.append(m.doc_wf("jobs: {}\n"))
    except Exception as e:   # ném ra ngoài CHÍNH LÀ điều vế này đo
        kieu = type(e).__name__
    bang(not sai and not khoi_mau and kieu == [None] * 20,
         f"{len(sai)}/{len(hang)} hàng lệch M4/dinh_nghia: {sai[:2]} · khối màu ra marker: {khoi_mau} · kiểu lạ: {kieu}")

@ca
def c43_khoi_khac_buoc():   # A27 (Q6): khối của nhóm i bằng `run:` của bước KHÁC (bước sau, skipped) ⇒ không marker
    w = yaml.safe_load(wf_tu("echo a", X))
    w["jobs"]["j"]["steps"][2]["if"] = "false"
    khong_marker(g1(yaml.safe_dump(w), buoc(X, "THU: 4/4 dat"), sua=lambda st: st[3].update(conclusion="skipped")), "khối ≠ run: bước i")

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
def c53_git_commit_khong_utf8():   # F13 (#955 review A) + #978 lượt 1: reader THẬT trên kho tạm, object dựng đúng byte bằng `hash-object`
    m = nap()   # (`--literally` cho object cố ý hỏng). Hợp đồng `git_cuc_bo`: dict hoặc None, KHÔNG ném (main không bắt) ⇒ ném là sai
    def doc(sha, goc):   # chỉ lỗi NỔI TỪ khung `git_cuc_bo` mới thành giá trị `NEM:` (vi phạm hợp đồng không-ném); lỗi khác ném tiếp = vô can
        try:
            return m.git_cuc_bo(sha, goc=goc)
        except Exception as e:   # noqa: BLE001
            tb = e.__traceback__
            while tb and tb.tb_frame.f_code is not m.git_cuc_bo.__code__:
                tb = tb.tb_next
            if tb is None:
                raise
            return f"NEM:{type(e).__name__}"
    with tempfile.TemporaryDirectory(prefix="cip_f13_") as thu:
        def kho(ten, *co):
            d = str(Path(thu) / ten)
            subprocess.run(["git", "init", "-q", *co, d], capture_output=True, check=True)
            g = lambda *a, i=None: subprocess.run(["git", "-C", d, *a], input=i, capture_output=True, check=True).stdout.decode().strip()  # noqa: E731
            return d, g
        d1, g = kho("sha1")
        cay = g("mktree", i=f"100644 blob {g('hash-object', '-w', '--stdin', i=b'x')}\tf\n".encode())
        dau = f"tree {cay}\nparent {P1}\nparent {P2}\n".encode()
        ai = lambda ten: b"author " + ten + b" <a@b> 1700000000 +0000\ncommitter " + ten + b" <a@b> 1700000000 +0000\n"  # noqa: E731
        cm = lambda b, lit=(): g("hash-object", "-t", "commit", "-w", *lit, "--stdin", i=b)  # noqa: E731
        dung, goc = {"tree": cay, "parents": [P1, P2]}, {"tree": cay, "parents": []}
        hop_le = [cm(dau + x) for x in (ai("Nguyễn".encode()) + "\nthông điệp UTF-8\n".encode(), ai(b"A") + b"encoding ISO-8859-1\n\nm\xe9ssage\n",
                                         ai(b"Jos\xe9") + b"encoding ISO-8859-1\n\nm\xe9ssage\n",
                                         ai(b"A") + f"\ntree {P1}\nparent {P1}\n".encode())]   # body giống header: chỉ đọc PHẦN ĐẦU
        ba = [P2, P1, "0" * 39 + "1"]   # 3 parent, thứ tự KHÔNG sắp xếp
        ca = [(x, dung) for x in hop_le] + [(cm(f"tree {cay}\n".encode() + ai(b"A") + b"\ngoc\n"), goc),   # commit gốc
              (cm(f"tree {cay}\n".encode() + ai(f"A\rparent {P1}\r".encode()) + b"\ncr\n"), goc),   # CR trong author ≠ dòng mới
              (cm(f"tree {cay}\n".encode() + b"".join(f"parent {x}\n".encode() for x in ba) + ai(b"A") + b"\nba\n"), {"tree": cay, "parents": ba})]
        ca += [(cm(f"tree {cay}\n".encode() + ai(b"A") + x + b"\nmo rong\n"), goc)   # `parent` SAU committer / sau header mở rộng ≠ cha
               for x in (f"parent {P1}\n".encode(), f"x-review v\nparent {P1}\n".encode())]
        tag = f"object {P1}\ntype commit\ntag v1\ntagger A <a@b> 1700000000 +0000\n\ntree {P2}\nparent {P2}\n".encode()   # header nhiều dòng:
        ca += [(cm(dau + ai(b"A") + b"mergetag " + tag.replace(b"\n", b"\n ").rstrip(b" ") + b"\nnoi\n"), dung)]   # dòng tiếp nối GIỮ dấu cách
        oid = cay.encode()   # lượt 5 (V3, cả lớp "chuẩn hoá dòng header"): `tree <oid>` ngụy trang — Git đọc là NỘI DUNG, không phải trường
        ca += [(cm(dau + ai(b"A" + k + b"tree " + oid + k + b"B") + b"\nsep\n"), dung)   # phân cách lạ trong author
               for k in (b"\x0b", b"\x0c", b"\x1c", b"\x1d", b"\x1e", b"\x85", "\u2028".encode(), "\u2029".encode(), "\u0085".encode())]
        ca += [(cm(dau + ai(b"A") + x + b"\n\nmo rong\n"), dung) for x in (   # dòng sau committer: TAB/CR đầu, TAB giữa, hoa, gập, NFKC
            b"\ttree " + oid, b"\rtree " + oid, b"tree\t" + oid, b"Tree " + oid, b"tree\n " + oid, "ｔｒｅｅ ".encode() + oid)]
        ca += [(cm(dau + ai(b"A") + x + b"\n\nm1\n"), None) for x in (b"tree ", b"x-review v\r\n\r\ntree " + oid)]   # M1: >1 dòng `tree `
        hong = [b"tree %s\ntree %s\n" % (cay.encode(), cay.encode()), b"parent %s\n" % P1.encode(), b"tree %s1\n" % cay.encode(),
                b"tree " + b"g" * 40 + b"\n", b"tree " + cay.upper().encode() + b"\n", f"tree {cay}\nparent zz\n".encode(),
                f"tree {cay}\nparent {P1[:20]}".encode() + b"\xff" + P1[20:].encode() + b"\n", f"parent {P1}\ntree {cay}\n".encode(), f"tree {cay}\rparent {P1}\n".encode()]
        ca += [(cm(x + ai(b"A") + b"\nh\n", ("--literally",)), None) for x in hong]
        ca += [(g("hash-object", "-w", "--stdin", i=v), None) for v in (b"\xff\n", b"tree zz\n", dau + ai(b"A") + b"\nblob\n")]   # blob, kể cả dạng commit
        g("tag", "-a", "-m", "t", "the", hop_le[0])
        ca += [(cay, None), (g("rev-parse", "the"), None), ("0" * 40, None), ("", None), (f"{hop_le[0]}\nHEAD", None), (None, None), ("\udc80", None)]   # tree · tag · thiếu · rỗng · 2 dòng · không str · không mã hoá được
        d2, g2 = kho("sha256", "--object-format=sha256")
        cay2 = g2("mktree", i=f"100644 blob {g2('hash-object', '-w', '--stdin', i=b'x')}\tf\n".encode())
        ba2 = ["f" * 64, "0" * 63 + "1", "a" * 64]
        c2 = g2("hash-object", "-t", "commit", "-w", "--stdin", i=f"tree {cay2}\n".encode() + b"".join(f"parent {x}\n".encode() for x in ba2)
                + ai(b"Jos\xe9") + b"\nm\xe9ssage\n")
        kq = [doc(x, d1) for x, _ in ca] + [doc(c2, d2)]
        mong = [k for _, k in ca] + [{"tree": cay2, "parents": ba2}]
        bang(kq == mong, f"git_cuc_bo lệch ở {[(i, a) for i, (a, b) in enumerate(zip(kq, mong)) if a != b]}")
        for x, d, gg in [(x, d1, g) for x, k in ca if type(k) is dict] + [(c2, d2, g2)]:   # oracle Git NATIVE cho mọi commit hợp lệ
            t, _, p = gg("log", "-1", "--no-walk", "--format=%T%n%P", x).partition("\n")
            bang(doc(x, d) == {"tree": t, "parents": p.split()}, f"lệch Git native ở {x}: {doc(x, d)} ≠ {t} {p.split()}")
        with mock.patch.dict(os.environ, {"PATH": thu}):
            bang(doc(hop_le[0], d1) is None, "không có git trên PATH ⇒ None")
        ra_that = subprocess.run(["git", "-C", d1, "cat-file", "--batch"], input=hop_le[0].encode() + b"\n", capture_output=True, check=True).stdout
        with mock.patch.object(m.subprocess, "run", return_value=subprocess.CompletedProcess([], 128, ra_that, b"")):   # git chết SAU khi in
            bang(doc(hop_le[0], d1) is None, "git rc ≠ 0 dù stdout trông như commit ⇒ None")
        for gia in (b"x commit zz\n\n", b"", ra_that.replace(b"\n", b" y\n", 1), ra_that[:-2], subprocess.TimeoutExpired("git", 60)):   # đầu ra/lỗi git TIÊM:
            tiem = {"side_effect": gia} if isinstance(gia, Exception) else {"return_value": subprocess.CompletedProcess([], 0, gia, b"")}
            with mock.patch.object(m.subprocess, "run", **tiem):   # kích thước không số · rỗng · thừa trường · thân cụt · quá hạn
                bang(doc(hop_le[0], d1) is None, f"đầu ra git tiêm {gia!r:.40} ⇒ None, không ném")
        tt = types.SimpleNamespace(get=lambda sha: m.git_cuc_bo(sha, goc=d1))
        rc, ra, prov, _ = chay([(job(1), LINUX.replace(H, hop_le[1]))], run={"event": "pull_request", "head_sha": P2}, git=tt,
                               wf={(hop_le[1], ".github/workflows/ci.yml"): wf_tu_log(LINUX)})
    bang(rc == 0 and prov and co(prov) == {"job_id": 1, "name": "j", "dong_sha": [hop_le[1]], "sha": hop_le[1], "parents": [P1, P2], "tree": cay,
                                            "trang_thai": "passed", "doi_chieu": "head_sha_trong_parents_merge_tong_hop"},
         f"main trên commit ISO-8859-1: rc={rc} {prov and co(prov)} {ra[-300:]}")

@ca
def c35_f02_khoi_khong_tron_ven():   # F02 r3: khối thiếu/lẫn màu không được thành tập con khớp run: của bước KHÁC
    x, hd, sh = f"python {DUONG_GIA}", f"{T} ##[group]Run python {DUONG_GIA}", f"{T} shell: /usr/bin/bash -e {{0}}"
    mau, ra = f"{T} \x1b[36;1mpython {DUONG_GIA}\x1b[0m", [f"{T} ##[endgroup]", f"{T} THU: 4/4 dat"]
    for ten, lg, w in (("dòng sau khối màu không phải shell:", [hd, mau, f"{T} echo xong", sh] + ra, wf_tu(x)),
                       ("thiếu shell:", [hd, mau] + ra, wf_tu(x)), ("header ≠ dòng màu đầu", [f"{T} ##[group]Run echo a", mau, sh] + ra, wf_tu(x)),
                       ("thiếu ##[endgroup]", [hd, mau, sh, f"{T} THU: 4/4 dat"], wf_tu(x)), ("màu sau shell:",
                        [f"{T} ##[group]Run python ops/khac.py", f"{T} \x1b[36;1mpython ops/khac.py\x1b[0m", sh, mau] + ra,
                        wf_tu("python ops/khac.py"))):
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
    ("A4d_regex_ca_log_job", "dau, so = do_dau_duong(buoc, moi, xanh, wf, ghep)",
     'dau, so = do_dau_duong([b | {"phan": [than(d) for d in dong]} for b in buoc], moi, xanh, wf, ghep)', "c13"),
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
    ("A14_kich_ban_tu_dong_mau", 'if not (type(run) is str and b["hop_le"] and run.rstrip("\\n") == "\\n".join(b["in_lai"])):',
     'run = "\\n".join(b["in_lai"])\n        if not run:', "c25"),
    ("A15_khoi_la_tap_con", 'run.rstrip("\\n") == "\\n".join(b["in_lai"])', 'set(b["in_lai"]) <= set(run.split("\\n"))', "c26"),
    ("A16_bo_luat_toan_khoi", "[g[2] for g in goi] if goi and all(goi) else []", "[g[2] for g in goi if g]", "c27"),
    ("A16_bo_khop_nguyen_van", 'run.rstrip("\\n") == "\\n".join(b["in_lai"])', 'True', "c25"),
    ("A17i_cho_env_buoc", '"timeout-minutes", "continue-on-error"}', '"timeout-minutes", "continue-on-error", "env"}', "c28"),
    ("A17ii_bo_env_job", ' or _env_chan(j)', '', "c29"),
    ("A17iii_cho_doi_so", r'\.py)$")', r'\.py)(?:\s+\S+)*$")', "c30"),
    ("che_do_bo_tien_to_VAR", " or any(g and g[1] for g in goi)", "", "c31"),
    ("che_do_bo_env_workflow", ' or _env_chan(wf)', "", "c31"),
    ("che_do_bo_defaults_workflow", 'return bool("defaults" in wf or', "return bool(", "c31"),
    ("che_do_bo_defaults_job", ' or "defaults" in j', "", "c31"),
    ("che_do_moi_shell", ' not in ("bash", "pwsh", "sh")', " is None", "c31"),
    ("A26_bo_GITHUB_ENV", 'or any(re.search("GITHUB_(ENV|PATH)", str(t.get("run", ""))) for t in j["steps"][:i]))', "or False)", "c42"),
    ("F11_bo_GITHUB_PATH", 're.search("GITHUB_(ENV|PATH)",', 're.search("GITHUB_ENV",', "c42"),
    ("A26_tinh_ca_buoc_i", 'for t in j["steps"][:i]))', 'for t in j["steps"][:i + 1]))', "c42"),
    ("A26_GITHUB_ENV_toan_workflow", 'for t in j["steps"][:i]))', 'for jj in wf["jobs"].values() for t in jj["steps"]))', "c42"),
    ("F08_git_bo_sha", 'f"{sha}:{path}"', 'f"HEAD:{path}"', "c34"),
    ("F13_giai_ma_toan_stdout", 'dau, _, than = r.stdout.partition(b"\\n")', 'dau, _, than = r.stdout.decode("utf-8").encode().partition(b"\\n")', "c53"),
    ("F13_giai_ma_ca_phan_dau", '.split(b"\\n\\n", 1)[0].split(b"\\n")', '.split(b"\\n\\n", 1)[0].decode("utf-8").encode().split(b"\\n")', "c53"),
    ("F13_bo_kiem_oid", " or not all(RE_OID_B.fullmatch(x) for x in tree + cha):", ":", "c53"),
    ("F13_cha_quet_ca_dau", "            break\n        cha.append(x[7:])", "            continue\n        cha.append(x[7:])", "c53"),
    ("F13_bo_tree_dong_dau", ' or not dong[0].startswith(b"tree ")', "", "c53"),
    ("F13_cha_chi_hai", '"parents": [x.decode("ascii") for x in cha]}', '"parents": [x.decode("ascii") for x in cha[:2]]}', "c53"),
    ("F13_cha_chi_40", "fullmatch(x) for x in tree + cha)", 'fullmatch(x) for x in tree) and all(re.fullmatch(rb"[0-9a-f]{40}", x) for x in cha)', "c53"),
    ("F13_bo_kiem_loai", ' or loai[1] != b"commit"', "", "c53"),
    ("F13_tach_splitlines", '.split(b"\\n\\n", 1)[0].split(b"\\n")', '.split(b"\\n\\n", 1)[0].splitlines()', "c53"),
    ("F13_oid_khoang", 're.compile(rb"[0-9a-f]{40}|[0-9a-f]{64}")', 're.compile(rb"[0-9a-f]{40,64}")', "c53"),
    ("F13_oid_chu_so", 're.compile(rb"[0-9a-f]{40}|[0-9a-f]{64}")', 're.compile(rb"[0-9a-z]{40}|[0-9a-z]{64}")', "c53"),
    ("F13_nhieu_tree", "if len(tree) != 1 or", "if not tree or", "c53"),
    ("F13_chi_kiem_tree", "fullmatch(x) for x in tree + cha)", "fullmatch(x) for x in tree)", "c53"),
    ("F13_bo_tach_dau_than", '.split(b"\\n\\n", 1)[0].split(b"\\n")', '.split(b"\\n")', "c53"),
    ("F13_dao_cha", '"parents": [x.decode("ascii") for x in cha]}', '"parents": [x.decode("ascii") for x in cha][::-1]}', "c53"),
    ("F13_bo_oserror", "except (OSError, subprocess.SubprocessError, UnicodeEncodeError):", "except (subprocess.SubprocessError, UnicodeEncodeError):", "c53"),
    ("F13_bo_kiem_kieu", "    if type(sha) is not str:", "    if False:", "c53"),
    ("F13_bo_kiem_rc", "if r.returncode != 0 or len(loai) != 3", "if len(loai) != 3", "c53"),
    ("F13_bo_isdigit", " or not loai[2].isdigit()", "", "c53"),
    ("F13_bo_kiem_kich_thuoc", " or len(than) != int(loai[2]) + 1", "", "c53"),
    ("F13_bo_dem_truong_dau", "if r.returncode != 0 or len(loai) != 3 or", "if r.returncode != 0 or", "c53"),
    ("F13_nhan_truong_thua", "or len(loai) != 3 or", "or len(loai) < 3 or", "c53"),
    ("F13_nhan_than_cut", "len(than) != int(loai[2]) + 1", "len(than) > int(loai[2]) + 1", "c53"),
    ("F13_bo_unicodeencode", "except (OSError, subprocess.SubprocessError, UnicodeEncodeError):", "except (OSError, subprocess.SubprocessError):", "c53"),
    ("F13_bo_subprocesserror", "except (OSError, subprocess.SubprocessError, UnicodeEncodeError):", "except (OSError, UnicodeEncodeError):", "c53"),
    ("F13_lstrip_dau_dong", '.split(b"\\n\\n", 1)[0].split(b"\\n")\n', '.split(b"\\n\\n", 1)[0].split(b"\\n")\n    dong = [x.lstrip() for x in dong]\n', "c53"),
    *[(f"F13_bien_doi_{ten}", '.split(b"\\n\\n", 1)[0].split(b"\\n")\n', '.split(b"\\n\\n", 1)[0].split(b"\\n")\n    dong = ' + bd + "\n", "c53") for ten, bd in (
        ("lstrip_tab", '[x.lstrip(b"\\t") for x in dong]'), ("tab_thanh_sp", '[x.replace(b"\\t", b" ") for x in dong]'),
        ("ha_ten", '[x[:4].lower() + x[4:] for x in dong]'), ("rstrip", '[x.rstrip() for x in dong]'),
        ("xoa_cr", '[x.replace(b"\\r", b"") for x in dong]'), ("xoa_dieu_khien", '[bytes(c for c in x if c >= 32) for x in dong]'),
        ("gap_dong", 'b"\\n".join(dong).replace(b"\\n ", b" ").split(b"\\n")'),
        ("nfkc", '[__import__("unicodedata").normalize("NFKC", x.decode("utf-8", "replace")).encode() for x in dong]'),
        ("tach_unicode", '[y.encode() for x in dong for y in x.decode("utf-8", "replace").splitlines()]'),
        *[(f"tach_{h:02x}", f'[y for x in dong for y in x.split(bytes([{h}]))]') for h in (0x0b, 0x0c, 0x1c, 0x1d, 0x1e, 0x85)])],
    ("F13_crlf_truoc_tach", "dong = than[:int(loai[2])].split(", 'dong = than[:int(loai[2])].replace(b"\\r\\n", b"\\n").split(', "c53"),
    ("F13_oid_chi_40", 're.compile(rb"[0-9a-f]{40}|[0-9a-f]{64}")', 're.compile(rb"[0-9a-f]{40}")', "c53"),
    ("F08_git_luon_vang", 'return r.stdout.decode("utf-8") if r.returncode == 0 else None', "return None", "c34"),
    ("F02_bo_doi_dong", 'not b["mo"] and b["ok"]', 'b["ok"]', "c35"),
    ("F02_bo_doi_shell", 'not b["tien_to"] or t.startswith("shell: ")', "True", "c35"),
    ("F02_cho_mau_sau", 'b["ok"] and not mau and', 'b["ok"] and', "c35"),
    ("F02_bo_het_tien_to", ' and not b["tien_to"] and b["in_lai"][:1]', " and b[\"in_lai\"][:1]", "c35"),
    ("F02_bo_doi_header", ' and b["in_lai"][:1] == [b["lenh"]]}', "}", "c35"),
    ("A18_head_sha_thay_sha_checkout", 'sha = co[-1].get("sha") if co[-1]["trang_thai"] == "passed" else None', 'sha = r.get("head_sha")', "c32"),
    ("L9_D03_job_chi_tien_to", 'and "${{" not in x and', 'and not x.startswith("${{") and', "c52"),
    ("L9_D03_buoc_chi_tien_to", 'and "${{" not in s["name"] else', 'and not s["name"].startswith("${{") else', "c52"),
    ("L9_D04_dem_mot_buoc", "        so += 1\n", "        so = 1\n", "c51"),
    ("A18_yaml_hong_nem", "    except Exception:   # r4 lượt 8–10", "    except RecursionError:   # r4 lượt 8–10", "c32"),
    ("L10_bat_lai_tuple_luot9", "    except Exception:   # r4 lượt 8–10",
     "    except (yaml.YAMLError, RecursionError, ValueError, KeyError, IndexError, AttributeError):   # r4 lượt 8–10", "c52"),
    ("A19_moi_ung_vien_trung_chu", "chan = chan_buoc(wf, k, i) or", 'chan = any(chan_buoc(wf, kk, ii) for kk, jj in wf["jobs"].items() '
     'for ii, t in enumerate(jj["steps"]) if t.get("run") == run) or', "c33"),
    ("A19_chan_doc_job_khac", "chan = chan_buoc(wf, k, i) or", 'chan = chan_buoc(wf, next(kk for kk in wf["jobs"] if kk != k), i) or', "c33"),
    ("A20i_zip_bo_dem_nhom", "    if len(buoc) != len(chay):\n", "    if False:\n", "c36"),
    ("A20ii_zip_bo_dem_yaml", "    if len(ung) != len(sy):\n", "    if False:\n", "c36"),
    ("A21_bo_kiem_ten", "if any(not _chuoi(s.get(\"name\")) or", "if False and any(not _chuoi(s.get(\"name\")) or", "c37"),
    ("ten_none_bang_none", 'any(not _chuoi(s.get("name")) or s.get("name")', 'any(s.get("name")', "c37"),
    ("ten_chi_buoc_chay", "for s, y in zip(ung, sy)):", "for s, y in [(ung[i], sy[i]) for i in chay]):", "c45"),
    ("ten_name_khong_chuoi", 'return s["name"] if _chuoi(s["name"]) and', 'return s["name"] if', "c44"),
    ("ten_name_rong_bo_qua", '    if "name" in s:\n', '    if s.get("name"):\n', "c37"),
    ("ten_v_khong_chuoi", 'return "Run " + v.split("\\n")[0] if _chuoi(v) else None', 'return "Run " + str(v).split("\\n")[0]', "c37"),
    ("ten_rstrip", 'return "Run " + v.split("\\n")[0] if', 'return "Run " + v.split("\\n")[0].rstrip() if', "c37"),
    ("loc_post_khong_cach", 'startswith("Post ")', 'startswith("Post")', "c37"),
    ("chay_chi_success", 'if s.get("conclusion") != "skipped"]', 'if s.get("conclusion") == "success"]', "c37"),
    ("dem_chi_khi_thua_nhom", "    if len(buoc) != len(chay):\n", "    if len(buoc) > len(chay):\n", "c36"),
    ("dem_chi_khi_thieu_rest", "    if len(ung) != len(sy):\n", "    if len(ung) < len(sy):\n", "c36"),
    ("gio_theo_thu_tu_tho", "for b, i in zip(buoc, chay)):", "for b, i in zip(buoc, range(len(buoc)))):", "c45"),
    ("vi_tri_theo_thu_tu_tho", "[(k, i) for i in chay]", "[(k, i) for i in range(len(chay))]", "c45"),
    ("wf_none_khai_passed", "    if wf is None:\n        return hong(ly_do_wf)\n", '    if wf is None:\n        return {"trang_thai": "passed", "so_buoc": 0}, None\n', "c32"),
    ("gio_match_thay_fullmatch", "RE_GIO.fullmatch(v)", "RE_GIO.match(v)", "c38"),
    ("job_hau_to_bat_ky", r'r"(?: \(.*\))?"', r'r"(?:.*)?"', "c39"),
    ("job_hau_to_khong_ngoac", r'r"(?: \(.*\))?"', r'r"(?: .*)?"', "c39"),
    ("job_cho_x_rong", 'type(x) is str and x and "${{"', 'type(x) is str and "${{"', "c39"),
    ("gio_bo_kiem_str", 'if type(v) is str and RE_GIO.fullmatch(v) else None', 'if RE_GIO.fullmatch(v) else None', "c38"),
    ("gio_bo_bat_ValueError", "    except ValueError:\n        return None", "    except KeyError:\n        return None", "c38"),
    ("job_chi_name_khi_co_name", 'for x in (k, j.get("name"))', 'for x in (j.get("name") or k,)', "c39"),
    ("L3_number_bool", '_so(s.get("number"), 1)', '(isinstance(s.get("number"), int) and s["number"] >= 1)', "c47"),
    ("L3_number_float", '_so(s.get("number"), 1)', '(isinstance(s.get("number"), (int, float)) and not isinstance(s.get("number"), bool) and s["number"] >= 1)', "c47"),
    ("L3_alias_name_bo", 'type(x) is str and x and "${{" not in x and re.fullmatch', 'type(x) is str and x and ten != j.get("name") and "${{" not in x and re.fullmatch', "c47"),
    ("L3_ma_tran_khac_rong", r'r"(?: \(.*\))?"', r'r"(?: \(.+\))?"', "c47"),
    ("L3_ma_tran_dotall", r'r"(?: \(.*\))?", ten)', r'r"(?: \(.*\))?", ten, re.S)', "c47"),
    ("L3_post_o_giua", 'str(s.get("name")).startswith("Post ")', '("Post " in str(s.get("name")))', "c47"),
    ("L3_run_rstrip_het", 'run.rstrip("\\n") == "\\n".join(b["in_lai"])', 'run.rstrip() == "\\n".join(b["in_lai"])', "c47"),
    ("L3_run_ep_chuoi", 'type(run) is str and b["hop_le"] and run.rstrip', 'b["hop_le"] and str(run).rstrip', "c47"),
    ("L3_bo_dedupe", "for duong in dict.fromkeys([g[2] for g in goi] if goi and all(goi) else []):", "for duong in ([g[2] for g in goi] if goi and all(goi) else []):", "c47"),
    ("L3_endgroup_startswith", 'if t == "##[endgroup]":', 'if t.startswith("##[endgroup]"):', "c47"),
    ("L3_shell_khong_cach", 't.startswith("shell: ")', 't.startswith("shell:")', "c47"),
    ("L3_truoc_bo_buoc_dau", 'for t in j["steps"][:i]))', 'for t in j["steps"][1:i]))', "c47"),
    ("L3_truoc_chi_lien_ke", 'for t in j["steps"][:i]))', 'for t in j["steps"][max(i - 1, 0):i]))', "c47"),
    ("L3_env_bo_dang", 'type(d["env"]) is not dict or any(str(k)', "False or any(str(k)", "c46"),
    ("L3_env_truthy", 'return "env" in d and (', 'return bool(d.get("env")) and (', "c46"),
    ("L3_env_chi_chuoi", 'type(d["env"]) is not dict or any(str(k)', 'type(d["env"]) is str or any(str(k)', "c46"),
    ("L3_env_wf_co_mat", '_env_chan(wf) or', '("env" in wf) or', "c46"),
    ("L3_defaults_wf_truthy", 'return bool("defaults" in wf or', 'return bool(bool(wf.get("defaults")) or', "c46"),
    ("L3_defaults_job_truthy", ' or "defaults" in j or', ' or bool(j.get("defaults")) or', "c46"),
    ("L3_shell_bo_pwsh", '("bash", "pwsh", "sh")', '("bash", "sh")', "c46"),
    ("L3_shell_bo_sh", '("bash", "pwsh", "sh")', '("bash", "pwsh")', "c46"),
    ("L3_shell_null_mac_dinh", 's.get("shell", "bash")', '(s.get("shell") or "bash")', "c46"),
    ("L3_khoa_bo_id", '{"name", "id", "if", "run", "shell",', '{"name", "if", "run", "shell",', "c46"),
    ("L3_khoa_bo_if", '{"name", "id", "if", "run", "shell",', '{"name", "id", "run", "shell",', "c46"),
    ("L3_khoa_bo_timeout", '"timeout-minutes", "continue-on-error"}', '"continue-on-error"}', "c46"),
    ("L3_khoa_bo_coe", '"timeout-minutes", "continue-on-error"}', '"timeout-minutes"}', "c46"),
    ("O_job_none_and", 'if k is None or "uses" in wf["jobs"][k] or', 'if k is None and "uses" in wf["jobs"][k] or', "c39"),
    ("O_var_mot_dong_all", "chan = chan_buoc(wf, k, i) or any(g and g[1] for g in goi)", "chan = chan_buoc(wf, k, i) or all(g and g[1] for g in goi)", "c46"),
    ("O_goi_or", "if goi and all(goi) else []):", "if goi or all(goi) else []):", "c23"),
    ("O_goi_any", "if goi and all(goi) else []):", "if goi and any(goi) else []):", "c23"),
    ('N_ten_strip', 'if type(ten) is str and type(j) is dict and any(', 'if type(ten) is str and (ten := ten.strip()) is not None and type(j) is dict and any(', 'c48'),
    ('N_ten_lower', 're.fullmatch(re.escape(x) + r"(?: \\(.*\\))?", ten)', 're.fullmatch(re.escape(x.lower()) + r"(?: \\(.*\\))?", ten.lower())', 'c48'),
    ('N_job_match', 're.fullmatch(re.escape(x)', 're.match(re.escape(x)', 'c48'),
    ('N_job_khoang_trang_ngoac', 'r"(?: \\(.*\\))?"', 'r"(?:\\s*\\(.*\\))?"', 'c48'),
    ('N_ten_run_strip', '"Run " + v.split("\\n")[0]', '"Run " + v.strip().split("\\n")[0]', 'c48'),
    ('N_ten_splitlines', 'v.split("\\n")[0]', '(v.splitlines() or [""])[0]', 'c48'),
    ('N_ten_name_lower', 'return s["name"] if _chuoi(s["name"])', 'return s["name"].lower() if _chuoi(s["name"])', 'c48'),
    ('N_rest_ten_lower', 's.get("name") != ten_du_kien(y)', 'str(s.get("name")).lower() != str(ten_du_kien(y)).lower()', 'c48'),
    ('N_meta_lower', 's.get("name") not in ("Set up job", "Complete job")', 'str(s.get("name")).lower() not in ("set up job", "complete job")', 'c48'),
    ('N_post_lower', 'str(s.get("name")).startswith("Post ")', 'str(s.get("name")).lower().startswith("post ")', 'c48'),
    ('N_post_strip', 'str(s.get("name")).startswith("Post ")', 'str(s.get("name")).strip().startswith("Post ")', 'c48'),
    ('N_concl_lower', 's.get("conclusion") != "skipped"]', 'str(s.get("conclusion")).lower() != "skipped"]', 'c48'),
    ('N_concl_timed_out', 's.get("conclusion") != "skipped"]', 's.get("conclusion") not in ("skipped", "timed_out")]', 'c48'),
    ('N_env_strip', 'str(k).startswith("CI_DANG_KY_")', 'str(k).strip().startswith("CI_DANG_KY_")', 'c48'),
    ('D01_null_coi_nhu_vang', 'return "env" in d and (', 'return d.get("env") is not None and (', 'c46'),
    ('N_defaults_none', 'return bool("defaults" in wf or', 'return bool(wf.get("defaults") is not None or', 'c48'),
    ('N_github_re_I', 're.search("GITHUB_(ENV|PATH)",', 're.search("(?i)GITHUB_(ENV|PATH)",', 'c48'),
    ('N_github_dollar', 're.search("GITHUB_(ENV|PATH)",', 're.search(r"\\$GITHUB_(ENV|PATH)",', 'c48'),
    ('N_mau_rong', 'mau = "\\x1b[36;1m" in d', 'mau = "\\x1b[36" in d', 'c48'),
    ('N_header_strip', '"lenh": t[len("##[group]Run "):]', '"lenh": t[len("##[group]Run "):].strip()', 'c48'),
    ('N_in_lai_strip', 'b["in_lai"].append(t)', 'b["in_lai"].append(t.strip())', 'c47'),
    ('N_in_lai_rstrip', 'b["in_lai"].append(t)', 'b["in_lai"].append(t.rstrip())', 'c47'),
    ('N_group_lower', 'if t.startswith("##[group]Run "):', 'if t.lower().startswith("##[group]run "):', 'c48'),
    ('N_long_lower', 'and not t.startswith("##[group]") and (', 'and not t.lower().startswith("##[group]") and (', 'c48'),
    ('N_shell_lower', 'not b["tien_to"] or t.startswith("shell: ")', 'not b["tien_to"] or t.lower().startswith("shell: ")', 'c48'),
    ('N_endgroup_strip', 'if t == "##[endgroup]":', 'if t.strip() == "##[endgroup]":', 'c48'),
    ('N_run_join_rstrip', 'run.rstrip("\\n") == "\\n".join(b["in_lai"])', 'run.rstrip("\\n") == "\\n".join(b["in_lai"]).rstrip()', 'c47'),
    ('N_run_cr', 'run.rstrip("\\n") == "\\n".join(b["in_lai"])', 'run.replace("\\r", "").rstrip("\\n") == "\\n".join(b["in_lai"])', 'c48'),
    ('N_gio_Z_tuy_chon', '[0-9]{2}:[0-9]{2}:[0-9]{2}Z")', '[0-9]{2}:[0-9]{2}:[0-9]{2}Z?")', 'c48'),
    ('N_khoa_lower', 'or set(s) - KHOA_BUOC', 'or {str(x).lower() for x in s} - KHOA_BUOC', 'c48'),
    ('N_uses_rong', 'run = s.get("run") if "uses" not in s else None', 'run = s.get("run") if not s.get("uses") else None', 'c48'),
    ('N_uses_job_rong', 'if k is None or "uses" in wf["jobs"][k] or', 'if k is None or bool(wf["jobs"][k].get("uses")) or', 'c48'),
    ('N_name_present_none', '    if "name" in s:\n', '    if s.get("name") is not None:\n', 'c48'),
    ('N_run_truoc_uses', 'v = s.get("run", s.get("uses"))', 'v = s.get("run") or s.get("uses")', 'c48'),
    ('L4_job_escape_alias', 're.escape(x)', 'x', 'c48'),
    ('L4_job_alias_strip', 're.escape(x)', 're.escape(x.strip())', 'c48'),
    ('L4_job_casefold', 'ten) for x in (k, j.get("name"))', 'ten, re.I) for x in (k, j.get("name"))', 'c48'),
    ('L4_name_explicit_strip', 'return s["name"] if _chuoi(s["name"])', 'return s["name"].strip() if _chuoi(s["name"])', 'c48'),
    ('L4_name_explicit_casefold', 'return s["name"] if _chuoi(s["name"])', 'return s["name"].casefold() if _chuoi(s["name"])', 'c48'),
    ('L4_metadata_setup_prefix', 's.get("name") not in ("Set up job", "Complete job")', 'not str(s.get("name")).startswith("Set up job") and s.get("name") != "Complete job"', 'c48'),
    ('L4_metadata_complete_prefix', 's.get("name") not in ("Set up job", "Complete job")', 's.get("name") != "Set up job" and not str(s.get("name")).startswith("Complete job")', 'c48'),
    ('L4_metadata_post_suffix', 'str(s.get("name")).startswith("Post ")', 'str(s.get("name")).endswith("Post ")', 'c48'),
    ('L4_ran_neutral_excluded', 's.get("conclusion") != "skipped"]', 's.get("conclusion") not in ("skipped", "neutral")]', 'c48'),
    ('L4_ran_cancelled_excluded', 's.get("conclusion") != "skipped"]', 's.get("conclusion") not in ("skipped", "cancelled")]', 'c48'),
    ('L4_env_prefix_empty_suffix', 'str(k).startswith("CI_DANG_KY_")', '(str(k).startswith("CI_DANG_KY_") and len(str(k)) > len("CI_DANG_KY_"))', 'c48'),
    ('L4_env_prefix_casefold', 'str(k).startswith("CI_DANG_KY_")', 'str(k).upper().startswith("CI_DANG_KY_")', 'c48'),
    ('L4_mode_step_key_truthy', 'set(s) - KHOA_BUOC', '{key for key in s if s[key]} - KHOA_BUOC', 'c48'),
    ('L4_mode_shell_strip', 's.get("shell", "bash") not in', 'str(s.get("shell", "bash")).strip() not in', 'c48'),
    ('L4_mode_shell_casefold', 's.get("shell", "bash") not in', 'str(s.get("shell", "bash")).lower() not in', 'c48'),
    ('L4_mode_prior_requires_ran', 'for t in j["steps"][:i]))', 'for t in j["steps"][:i] if t.get("if") != "false"))', 'c48'),
    ('L4_run_compare_strip_newlines', 'run.rstrip("\\n") == "\\n".join(b["in_lai"])', 'run.strip("\\n") == "\\n".join(b["in_lai"])', 'c48'),
    ('L4_header_lstrip', 'b["in_lai"][:1] == [b["lenh"]]', 'b["in_lai"][:1] == [b["lenh"].lstrip()]', 'c48'),
    ('L4_shell_lstrip', 't.startswith("shell: ")', 't.lstrip().startswith("shell: ")', 'c48'),
    ('L4_number_contiguous', 'and len({s["number"] for s in st}) == len(st)', 'and {s["number"] for s in st} == set(range(1, len(st) + 1))', 'c36'),
    ('L5_wf_env_dict_only', '_env_chan(wf) or', '(type(wf.get("env")) is dict and _env_chan(wf)) or', 'c49'),
    ('L5_wf_env_nonempty_only', '_env_chan(wf) or', '(bool(wf.get("env")) and _env_chan(wf)) or', 'c49'),
    ('L5_env_chi_khoa_dau', 'for k in d["env"]))', 'for k in list(d["env"])[:1]))', 'c49'),
    ('L5_env_chi_khoa_cuoi', 'for k in d["env"]))', 'for k in list(d["env"])[-1:]))', 'c29'),
    ('L5_env_false_cho_qua', 'return "env" in d and (', 'return "env" in d and d["env"] is not False and (', 'c49'),
    ('L5_env_int_cho_qua', 'return "env" in d and (', 'return "env" in d and type(d["env"]) is not int and (', 'c49'),
    ('L5_env_chuoi_rong_cho_qua', 'return "env" in d and (', 'return "env" in d and d["env"] != "" and (', 'c49'),
    ('L5_env_gia_tri_rong_cho_qua', 'str(k).startswith("CI_DANG_KY_") for k in', '(str(k).startswith("CI_DANG_KY_") and bool(d["env"][k])) for k in', 'c49'),
    ('L5_che_do_buoc_run_dau', 'j, s = wf["jobs"][k], wf["jobs"][k]["steps"][i]', 'j, s = wf["jobs"][k], wf["jobs"][k]["steps"][min(1, len(wf["jobs"][k]["steps"]) - 1)]', 'c49'),
    ('L5_dd_job_dau', '        s = wf["jobs"][k]["steps"][i]\n', '        s = (next(iter(wf["jobs"].values()))["steps"] + [{}] * 99)[i]\n', 'c49'),
    ('L5_job_uu_tien_khop_dung', 'return khop[0] if len(khop) == 1 else None', 'return ten if ten in khop else khop[0] if len(khop) == 1 else None', 'c49'),
    ('L5_job_ten_dai_bo_hau_to', 'for x in (k, j.get("name")))]', 'for x in (k, j.get("name")) if ten == x or len(ten) < 80)]', 'c49'),
    ('L5_gio_completed_cua_buoc_cuoi', '(z := _gio(ung[i].get("completed_at")))', '(z := _gio(ung[chay[-1]].get("completed_at")))', 'c49'),
    ('L5_truoc_chi_run_chuoi', 'str(t.get("run", ""))', '(t.get("run", "") if type(t.get("run", "")) is str else "")', 'c49'),
    ('L5_github_cuoi_chuoi', 're.search("GITHUB_(ENV|PATH)",', 're.search("GITHUB_(ENV|PATH)$",', 'c49'),
    ('L5_github_ranh_gioi_tu', 're.search("GITHUB_(ENV|PATH)",', 're.search(r"\\bGITHUB_(ENV|PATH)\\b",', 'c49'),
    ('L5_mau_doi_reset', 'mau = "\\x1b[36;1m" in d', 'mau = bool(re.search(r"\\x1b\\[36;1m.*\\x1b\\[0m$", d))', 'c48'),
    ('L5_khoi_rstrip_ca_khoi', 'run.rstrip("\\n") == "\\n".join(b["in_lai"])', 'run.rstrip("\\n") == "\\n".join(b["in_lai"]).rstrip("\\n")', 'c48'),
    ('L5_run_bo_mot_lf', 'run.rstrip("\\n") == "\\n".join(b["in_lai"])', 'run.removesuffix("\\n") == "\\n".join(b["in_lai"])', 'c48'),
    ('L5_uses_strip', 'v = s.get("run", s.get("uses"))', 'v = s.get("run", str(s.get("uses")).strip())', 'c48'),
    ('L5_goi_strip_toan_run', 'dong_logic(run.rstrip("\\n").split("\\n"))', 'dong_logic(run.strip().split("\\n"))', 'c48'),
    ('L5_D01_null_la_vang', 'return "env" in d and (', 'return d.get("env") is not None and (', 'c49'),
    ('L6_job_ascii_suffix', 're.escape(x) + r"(?: \\(.*\\))?", ten)', 're.escape(x) + r"(?: \\([ -~]*\\))?", ten)', 'c50'),
    ('L6_job_alias_truncate', 'for x in (k, j.get("name"))', 'for x in (k, str(j.get("name"))[:20])', 'c50'),
    ('L6_job_nonempty_rest_required', 'type(st) is list and all(', 'type(st) is list and bool(st) and all(', 'c50'),
    ('L6_rest_number_under_100', '_so(s.get("number"), 1)', '(_so(s.get("number"), 1) and s["number"] < 100)', 'c50'),
    ('L6_rest_skipped_time_required', 'if not all((a := _gio(', 'if any(not _gio(s.get("started_at")) for s in ung) or not all((a := _gio(', 'c50'),
    ('L6_time_require_same_day', 'a <= h <= z', 'a <= h <= z and a.date() == h.date() == z.date()', 'c50'),
    ('L6_time_reject_year_before_2000', 'type(v) is str and RE_GIO.fullmatch(v)', 'type(v) is str and RE_GIO.fullmatch(v) and v[:4] >= "2000"', 'c50'),
    ('L6_time_accept_invalid_leap_day', 'except ValueError:\n        return None', 'except ValueError:\n        return datetime.datetime(2026, 2, 28) if type(v) is str and v[:10] == "2026-02-29" else None', 'c50'),
    ('L6_names_compare_as_strings', 's.get("name") != ten_du_kien(y)', 'str(s.get("name")) != str(ten_du_kien(y))', 'c50'),
    ('L6_prior_entire_step_instead_run', 'str(t.get("run", ""))', 'str(t)', 'c50'),
    ('L6_prior_uses_preferred', 'str(t.get("run", ""))', 'str(t.get("uses", t.get("run", "")))', 'c50'),
    ('L6_log_first_output_line', '"\\n".join(b["phan"]) + "\\n"', '"\\n".join(b["phan"][:1]) + "\\n"', 'c50'),
    ('L6_log_last_output_line', '"\\n".join(b["phan"]) + "\\n"', '"\\n".join(b["phan"][-1:]) + "\\n"', 'c50'),
    ('L6_log_output_strip', '"\\n".join(b["phan"]) + "\\n"', '"\\n".join(b["phan"]).strip() + "\\n"', 'c50'),
    ('L6_log_reverse_output', '"\\n".join(b["phan"]) + "\\n"', '"\\n".join(reversed(b["phan"])) + "\\n"', 'c50'),
    ('L6_log_endgroup_need_shell_first', 'if t == "##[endgroup]":', 'if t == "##[endgroup]" and not b["tien_to"]:', 'c50'),
    ('L6_log_uncolored_metadata_add_to_echo', 'elif mau and b["tien_to"]:', 'elif mau and b["tien_to"] or t.startswith("  NOTE:"):', 'c50'),
    ('L6_log_shell_nonempty', 't.startswith("shell: ")', 't.startswith("shell: ") and len(t)>7', 'c50'),
    ('L6_log_color_prefix_only', 'mau = "\\x1b[36;1m" in d', 'mau = d.split(" ", 1)[-1].startswith("\\x1b[36;1m")', 'c50'),
    ('L6_log_color_without_timestamp', 'mau = "\\x1b[36;1m" in d', 'mau = "\\x1b[36;1m" in d and bool(RE_DONG.match(d))', 'c50'),
    ('L6_run_blank_lines_disallowed', 'for d in dong_logic(run.rstrip("\\n").split("\\n")) if d]', 'for d in dong_logic(run.rstrip("\\n").split("\\n"))]', 'c50'),
    ('L6_rest_also_skip_null', 's.get("conclusion") != "skipped"]', 's.get("conclusion") not in (None, "skipped")]', 'c50'),
    ('L6_yaml_empty_workflow_reject', 'type(wf.get("jobs")) is dict', 'type(wf.get("jobs")) is dict and bool(wf["jobs"])', 'c50'),
    ('L6_rest_number_order_contiguous', 'len({s["number"] for s in st}) == len(st)', 'len({s["number"] for s in st}) == len(st) and min(s["number"] for s in st) == 1', 'c50'),
    ('A_gio_chu_so_unicode', '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z', '\\d{4}-\\d\\d-\\d\\dT\\d\\d:\\d\\d:\\d\\dZ', 'c51'),
    ('L7_job_alias_unicode_reject', 'type(x) is str and x and "${{"', 'type(x) is str and x.isascii() and x and "${{"', 'c51'),
    ('L7_name_explicit_unicode_reject', '_chuoi(s["name"]) and "${{"', '_chuoi(s["name"]) and s["name"].isascii() and "${{"', 'c51'),
    ('L7_time_same_year', 'a <= h <= z', 'a <= h <= z and a.year == h.year == z.year', 'c51'),
    ('L7_time_same_month', 'a <= h <= z', 'a <= h <= z and a.month == h.month == z.month', 'c51'),
    ('L7_time_century_leap_reject', 'type(v) is str and RE_GIO.fullmatch(v)', 'type(v) is str and RE_GIO.fullmatch(v) and not (v[5:10] == "02-29" and int(v[:4]) % 100 == 0)', 'c51'),
    ('L7_time_year_9999_reject', 'type(v) is str and RE_GIO.fullmatch(v)', 'type(v) is str and RE_GIO.fullmatch(v) and v[:4] != "9999"', 'c51'),
    ('L7_time_year_0001_reject', 'type(v) is str and RE_GIO.fullmatch(v)', 'type(v) is str and RE_GIO.fullmatch(v) and v[:4] != "0001"', 'c51'),
    ('L7_time_clock_only_compare', 'a <= h <= z', 'a.time() <= h.time() <= z.time()', 'c51'),
    ('L7_time_whitespace_strip', 'RE_GIO.fullmatch(v)', 'RE_GIO.fullmatch(v.strip())', 'c51'),
    ('L7_time_invalid_century_accept', 'except ValueError:\n        return None', 'except ValueError:\n        return datetime.datetime(1900, 2, 28) if type(v) is str and v[:10] == "1900-02-29" else None', 'c51'),
    ('L7_rest_metadata_time_required', 'if not all((a := _gio(', 'if any(not _gio(s.get("started_at")) or not _gio(s.get("completed_at")) for s in st if s.get("name") in ("Set up job", "Complete job") or str(s.get("name")).startswith("Post ")) or not all((a := _gio(', 'c51'),
    ('L7_rest_filter_post_number_order', 'and not str(s.get("name")).startswith("Post ")]', 'and not (str(s.get("name")).startswith("Post ") and s["number"] > 1)]', 'c51'),
    ('L7_mode_env_present_values_only', 'any(str(k).startswith("CI_DANG_KY_") for k in d["env"])', 'any(str(k).startswith("CI_DANG_KY_") and d["env"][k] is not None for k in d["env"])', 'c51'),
    ('L7_mode_env_empty_key_reject', '_env_chan(j) or', '(_env_chan(j) or (type(j.get("env")) is dict and "" in j["env"])) or', 'c51'),
    ('L7_mode_env_unicode_key_reject', '_env_chan(j) or', '(_env_chan(j) or (type(j.get("env")) is dict and any(not str(k).isascii() for k in j["env"]))) or', 'c51'),
    ('L7_mode_prior_skip_uses', 'for t in j["steps"][:i]))', 'for t in j["steps"][:i] if "uses" not in t))', 'c51'),
    ('L7_dd_first_match_lines_only', 'k.group(0).splitlines() if k else []', 'k.group(0).splitlines()[:1] if k else []', 'c51'),
    ('L7_dd_last_match_lines_only', 'k.group(0).splitlines() if k else []', 'k.group(0).splitlines()[-1:] if k else []', 'c51'),
    ('L7_dd_blank_output_lines_remove', '"\\n".join(b["phan"]) + "\\n"', '"\\n".join(x for x in b["phan"] if x) + "\\n"', 'c51'),
    ('L7_dd_no_output_final_newline', '"\\n".join(b["phan"]) + "\\n"', '"\\n".join(b["phan"])', 'c51'),
    ('L7_dd_dedup_output_lines', '"\\n".join(b["phan"]) + "\\n"', '"\\n".join(dict.fromkeys(b["phan"])) + "\\n"', 'c51'),
    ('L7_dd_sort_match_lines', 'k.group(0).splitlines() if k else []', 'sorted(k.group(0).splitlines()) if k else []', 'c51'),
    ('L7_dd_wrong_lenh_first_call', '"lenh": b["lenh"], "duong_dan": duong', '"lenh": next(iter(moi)), "duong_dan": duong', 'c51'),
    ('L7_dd_step_dedup_paths', 'for b, (k, i) in zip(buoc, ghep or []):', 'for b, (k, i) in zip(buoc, ghep or []):\n        if any(x["lenh"] == b["lenh"] for x in kq): continue', 'c51'),
    ('L7_log_output_ignore_indented_blank', 'buoc[-1]["phan"].append(t)', 'buoc[-1]["phan"].append(t.rstrip())', 'c51'),
    ('L7_log_empty_metadata_reject', 'not b["tien_to"] or t.startswith("shell: ")', '(not b["tien_to"] and bool(t)) or t.startswith("shell: ")', 'c51'),
    ('L7_log_second_shell_reject', 'not b["tien_to"] or t.startswith("shell: ")', '(not b["tien_to"] and not t.startswith("shell: ")) or (b["tien_to"] and t.startswith("shell: "))', 'c51'),
    ('L7_log_output_drop_group_lines', 'buoc[-1]["phan"].append(t)', 'buoc[-1]["phan"].extend([t] if not t.startswith("##[group]") else [])', 'c51'),
    ('L7_log_require_output_nonempty', 'not b["mo"] and b["ok"]', 'not b["mo"] and bool(b["phan"]) and b["ok"]', 'c51'),
    ('L7_log_require_metadata_no_ansi', 'b["ok"] and not mau', 'b["ok"] and not mau and "\\x1b[" not in d', 'c51'),
    ('L7_log_color_run_not_contains_shell', 'elif mau and b["tien_to"]:', 'elif mau and b["tien_to"] and not t.startswith("shell: "):', 'c51'),
    ('L7_job_suffix_no_dot_pure', 'r"(?: \\(.*\\))?"', 'r"(?: \\([^.\\n]*\\))?"', 'c51'),
    ("job_bo_x_str", 'type(x) is str and x and "${{"', 'x and "${{"', "c44"),
    ("so_number_0", '_so(s.get("number"), 1)', '_so(s.get("number"), 0)', "c44"),
    ("so_number_am", '_so(s.get("number"), 1)', '(type(s.get("number")) is int)', "c44"),
    ("sy_khong_list", " or type(sy) is not list or", " or", "c44"),
    ("dd_run_khong_chuoi", "if not (type(run) is str and b[\"hop_le\"]", "if not (run and b[\"hop_le\"]", "c44"),
    ("A22_bo_kiem_gio", "    if not all((a := _gio(", "    if False and all((a := _gio(", "c38"),
    ("A22_khong_cat_giay", '"gio": d[:19] + "Z"})', '"gio": d.split(" ", 1)[0]})', "c38"),
    ("F09_bo_kiem_lich", 'datetime.datetime.strptime(v[:19], "%Y-%m-%dT%H:%M:%S")', "v[:19]", "c38"),
    ("F09_nhan_offset", r'[0-9]{2}:[0-9]{2}:[0-9]{2}Z")', r'[0-9]{2}:[0-9]{2}:[0-9]{2}(?:Z|[+-][0-9]{2}:[0-9]{2})")', "c38"),
    ("F09_header_thieu_dung_rest", '(h := _gio(b["gio"]))', '(h := _gio(b["gio"]) or a)', "c38"),
    ("F10_bo_sort", 'sorted(st, key=lambda s: s["number"])', "st", "c37"),
    ("F10_bo_number_trung", '\n            and len({s["number"] for s in st}) == len(st)', "", "c37"),
    ("F10_ten_lstrip", '"Run " + v.split("\\n")[0]', '"Run " + v.lstrip().split("\\n")[0]', "c37"),
    ("F10_name_bieu_thuc", '_chuoi(s["name"]) and "${{" not in s["name"]', '_chuoi(s["name"])', "c37"),
    ("dang_bo_number", 'type(s) is dict and _so(s.get("number"), 1) for s in st', "type(s) is dict for s in st", "c44"),
    ("dang_buoc_rest_khong_dict", 'all(type(s) is dict and _so(s.get("number"), 1)', 'all(_so(s.get("number"), 1)', "c44"),
    ("dang_buoc_yaml_khong_dict", "or not all(type(s) is dict for s in sy):", "or False:", "c44"),
    ("dang_job_khong_dict", "if type(ten) is str and type(j) is dict and any(", "if type(ten) is str and any(", "c44"),
    ("A23_lay_khoa_dau", "return khop[0] if len(khop) == 1 else None", "return khop[0] if khop else None", "c39"),
    ("A23_nhan_job_goi_lai", 'if k is None or "uses" in wf["jobs"][k] or', "if k is None or", "c39"),
    ("A23_nhan_bieu_thuc", 'x and "${{" not in x and re.fullmatch', "x and re.fullmatch", "c39"),
    ("A24_bo_luat_nhom_long", ' and not t.startswith("##[group]")', "", "c40"),
    ("A25i_uses_sinh_marker", 'run = s.get("run") if "uses" not in s else None', 'run = s.get("run")', "c41"),
    ("A25ii_zip_bo_dem_nhom", "    if len(buoc) != len(chay):\n", "    if False:\n", "c41"),
    ("A27_khoi_bang_buoc_khac", 'run = s.get("run") if "uses" not in s else None', 'run = next((t["run"] for t in wf["jobs"][k]["steps"] if '
     'type(t.get("run")) is str and t["run"].rstrip("\\n") == "\\n".join(b["in_lai"])), None)', "c43"),
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

HAM_DONG = ("_env_chan", "doc_wf", "ghep_job", "ten_du_kien", "_gio", "ghep_buoc", "chan_buoc", "tach_buoc", "do_dau_duong")
DOI_SO_SANH = {ast.Eq: [ast.NotEq], ast.NotEq: [ast.Eq], ast.Lt: [ast.LtE, ast.Gt], ast.LtE: [ast.Lt, ast.GtE], ast.Gt: [ast.GtE, ast.Lt],
               ast.GtE: [ast.Gt, ast.LtE], ast.In: [ast.NotIn], ast.NotIn: [ast.In], ast.Is: [ast.IsNot], ast.IsNot: [ast.Is]}
TUONG_DUONG = {   # mã đột biến tập đóng → chứng minh vì sao KHÔNG đầu vào nào phân biệt được (bị giết ⇒ lời khai SAI ⇒ ĐỎ)
    "ghep_job#24:-1": "`khop[-1]` thay `khop[0]` chỉ được tính khi `len(khop) == 1`, mà danh sách một phần tử có [0] và [-1] là cùng một phần tử",
    "chan_buoc#103:bo_doi_so1": "`str(t.get('run'))` thay `str(t.get('run', ''))` chỉ khác ở bước KHÔNG có `run:`: chuỗi tìm là 'None' thay vì '' — "
                                "cả hai đều không chứa `GITHUB_ENV`/`GITHUB_PATH`, nên `re.search` cùng trả None",
    **{f"tach_buoc#173:chuoi{k}": "chuỗi chỉ đứng trong `len('##[group]Run ')`: biến dạng hoa/thường/đảo hoa giữ NGUYÊN độ dài 13 nên lát "
       "cắt `lenh` không đổi (biến dạng đổi độ dài — hậu tố, bớt ký tự, khoảng trắng, rỗng — bị giết)" for k in (2, 3, 4)},
    "do_dau_duong#127:bo_ve0": "bỏ vế `goi and`: khi `goi` rỗng thì `all(goi)` là True nhưng `[g[2] for g in goi]` cũng rỗng ⇒ vòng lặp "
                               "không chạy lần nào, y như nhánh `else []`",
    **{f"do_dau_duong#306:chuoi{k}": "`run.rstrip('')` (cả hai mã cùng một nguồn đột biến) chỉ để lại các `\\n` cuối ⇒ `split` sinh thêm "
       "đoạn RỖNG ở đuôi; `dong_logic` biến đoạn rỗng thành '' (hoặc nối vào dòng `\\` đang dở rồi `strip()` ra cùng chuỗi), và "
       "`if d` bỏ ''. Phép so khối `run.rstrip(\"\\n\") == …` đứng TRƯỚC không đổi" for k in (1, 4)},
}

def _thay(x, y):   # đổi nút x thành nút y tại chỗ
    x.__class__ = y.__class__
    x.__dict__.clear()
    x.__dict__.update(y.__dict__)

def _toan_tu(n):   # bảng toán tử CỐ ĐỊNH của tập đóng: (tên, hàm sửa nút tại chỗ trên bản sao)
    if isinstance(n, ast.Compare):
        for k, op in enumerate(n.ops):
            for moi in DOI_SO_SANH.get(type(op), []):
                yield f"so{k}->{moi.__name__}", lambda x, k=k, moi=moi: x.ops.__setitem__(k, moi())
    elif isinstance(n, ast.BoolOp):
        yield "and<->or", lambda x: setattr(x, "op", ast.Or() if isinstance(x.op, ast.And) else ast.And())
        for k in range(len(n.values)):
            yield f"bo_ve{k}", lambda x, k=k: x.values.pop(k) if len(x.values) > 2 else _thay(x, x.values[1 - k])
    elif isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not):
        yield "bo_not", lambda x: _thay(x, x.operand)
    elif isinstance(n, ast.Constant) and type(n.value) is bool:
        yield "bool", lambda x: setattr(x, "value", not x.value)
    elif isinstance(n, ast.Constant) and type(n.value) is int:
        yield "+1", lambda x: setattr(x, "value", x.value + 1)
        yield "-1", lambda x: setattr(x, "value", x.value - 1)
    elif isinstance(n, ast.Constant) and type(n.value) is str and n.value:
        for k, w in enumerate(bien_dang(n.value) + [""]):
            yield f"chuoi{k}", lambda x, w=w: setattr(x, "value", w)
    elif isinstance(n, ast.IfExp):
        yield "ifexp_than", lambda x: _thay(x, x.body)
        yield "ifexp_khac", lambda x: _thay(x, x.orelse)
    elif isinstance(n, ast.If):
        yield "if_dung", lambda x: setattr(x, "test", ast.Constant(True))
        yield "if_sai", lambda x: setattr(x, "test", ast.Constant(False))
    elif isinstance(n, ast.comprehension):
        for k in range(len(n.ifs)):
            yield f"bo_loc{k}", lambda x, k=k: x.ifs.pop(k)
    elif isinstance(n, ast.Call) and len(n.args) > 1:
        for k in range(len(n.args)):
            yield f"bo_doi_so{k}", lambda x, k=k: x.args.pop(k)
    elif isinstance(n, ast.Return) and n.value is not None:
        yield "tra_None", lambda x: setattr(x, "value", ast.Constant(None))
    elif isinstance(n, ast.ExceptHandler) and isinstance(n.type, ast.Tuple):   # lượt 8 P2: bỏ TỪNG lớp ngoại lệ được bắt
        for k in range(len(n.type.elts)):
            yield f"bo_ngoai_le{k}", lambda x, k=k: x.type.elts.pop(k)

def sinh_dot_bien_dong(src):
    """TẬP ĐÓNG (quyết định chủ kho #899 sau lượt 7): MỌI đột biến bậc một của MỌI nút trong `HAM_DONG` theo `_toan_tu`, trừ
    docstring. Trả [(mã, nguồn)]; mã = `<hàm>#<thứ tự nút trong ast.walk>:<toán tử>` — ổn định khi mã NGOÀI hàm đổi."""
    goc, ra = ast.parse(src), {}
    for ham in [n for n in goc.body if isinstance(n, ast.FunctionDef) and n.name in HAM_DONG]:
        doc = {id(x.value) for x in ast.walk(ham) if isinstance(x, ast.Expr) and isinstance(x.value, ast.Constant)}
        for j, n in enumerate(list(ast.walk(ham))[1:]):
            if id(n) in doc:
                continue
            for ten, sua in _toan_tu(n):
                cay = ast.parse(src)
                dich = list(ast.walk(next(h for h in cay.body if isinstance(h, ast.FunctionDef) and h.name == ham.name)))[1:][j]
                sua(dich)
                try:
                    moi = ast.unparse(ast.fix_missing_locations(cay))
                    compile(moi, "<db>", "exec")
                except (SyntaxError, ValueError, TypeError, IndexError):
                    continue
                if moi != ast.unparse(goc):
                    ra[f"{ham.name}#{j}:{ten}"] = moi
    return list(ra.items())

def _tat_ca_ca(ma):   # chạy MỌI ca trên bản `ma` trong một tiến trình con: [(ca, rc, dòng)]
    r = subprocess.run([sys.executable, "-B", str(HERE / "ci_provenance_test.py"), "--tat-ca-ca"], capture_output=True, timeout=1800,
                       env=dict(os.environ, CI_PROVENANCE_MA=str(ma), PYTHONDONTWRITEBYTECODE="1"))
    try:
        return json.loads(r.stdout.decode("utf-8", "replace").strip().splitlines()[-1])
    except (ValueError, IndexError):
        return [("nap", 4, r.stderr.decode("utf-8", "replace")[-300:])]

def chay_dot_bien_dong(song_song):
    """Hạng mỗi đột biến: GIET (≥ 1 ca chết bởi `TinHieuChotCa` của CHÍNH nó) · SONG · TIN_DUNG_GIA (chỉ chết vì lỗi vô can).
    Đạt ⇔ 0 SONG ngoài `TUONG_DUONG`, 0 TIN_DUNG_GIA, và KHÔNG mục `TUONG_DUONG` nào bị giết (giết ⇒ chứng minh sai)."""
    from concurrent.futures import ThreadPoolExecutor
    goc = (HERE / "ci_provenance.py").read_text(encoding="utf-8")
    dsach = sinh_dot_bien_dong(goc)
    with tempfile.TemporaryDirectory(prefix="cip_dong_") as thu:
        nen = Path(thu) / "goc.py"
        nen.write_text(goc, encoding="utf-8")
        bad = [x for x in _tat_ca_ca(nen) if x[1] != 0]
        if bad:
            print(f"DOT BIEN DONG: KHONG DO DUOC — ca khong xanh tren ban goc: {bad[:2]}")
            return 1
        def mot(m):
            ma, src = m
            p = Path(thu) / f"db_{len(ma)}_{abs(hash(ma))}.py"
            p.write_text(src, encoding="utf-8")
            kq = _tat_ca_ca(p)
            giet = [c for c, rc, d in kq if rc == 3 and d.startswith(f"DO:{c}:")]
            return ma, "GIET" if giet else "TIN_DUNG_GIA" if any(rc for _, rc, _ in kq) else "SONG", giet[:2]
        tiep = {}   # `CIP_DONG_TIEP=<tệp stdout lượt trước>`: dùng lại hạng đã đo cho CÙNG mã + CÙNG băm nguồn đột biến
        for d in Path(os.environ["CIP_DONG_TIEP"]).read_text(encoding="utf-8").splitlines() if os.environ.get("CIP_DONG_TIEP") else []:
            if d.startswith("[KQ] "):
                ma, bam, h = d[5:].rsplit(" ", 2)
                tiep[(ma, bam)] = h
        def mot_co_ghi(m):
            bam = hashlib.sha256(m[1].encode()).hexdigest()[:16]
            r = (m[0], tiep[(m[0], bam)], []) if (m[0], bam) in tiep else mot(m)
            print(f"[KQ] {r[0]} {bam} {r[1]}", flush=True)
            return r
        with ThreadPoolExecutor(song_song) as ex:
            kq = list(ex.map(mot_co_ghi, dsach))
    hang = collections.Counter(h for _, h, _ in kq)
    song = [ma for ma, h, _ in kq if h == "SONG" and ma not in TUONG_DUONG]
    tdg = [ma for ma, h, _ in kq if h == "TIN_DUNG_GIA"]
    sai_td = [ma for ma, h, _ in kq if h == "GIET" and ma in TUONG_DUONG] + [ma for ma in TUONG_DUONG if ma not in dict((m, 1) for m, _ in dsach)]
    for ma in song + tdg + sai_td:
        print(f"[DOT BIEN DONG] {ma}: {dict((m, h) for m, h, _ in kq).get(ma, 'KHONG_CON_TRONG_TAP')}")
    print(f"DOT BIEN DONG: {hang['GIET']}/{len(kq)} giet · {len(TUONG_DUONG)} tuong duong co chung minh · {len(song)} song · {len(tdg)} tin dung gia"
          f" · {len(sai_td)} chung minh tuong duong sai")
    ok = len(kq) > 0 and not song and not tdg and not sai_td
    print(f"TONG DONG: {'DAT' if ok else 'DO'}")
    return 0 if ok else 1

def main(argv):
    if len(argv) == 2 and argv[0] == "--mot-ca" and argv[1] in CA:
        rc, dong = chay_ca(argv[1])
        print(dong)
        return rc
    if argv == ["--tat-ca-ca"]:   # ca nhẹ trước, ca bảng/oracle sau; dừng ở ca ĐẦU TIÊN chết bởi `TinHieuChotCa` (đã đủ để xếp GIET)
        kq = []
        for c in sorted(CA, key=lambda c: c.split("_")[0] in ("c22", "c46", "c48", "c49")):
            kq.append((c, *chay_ca(c)))
            if kq[-1][1] == 3:
                break
        print(json.dumps(kq, ensure_ascii=False))
        return 0
    if argv[:1] == ["--dot-bien-dong"] and len(argv) <= 2:
        return chay_dot_bien_dong(int(argv[1]) if len(argv) == 2 else 8)
    if argv:
        print("dung: ci_provenance_test.py [--mot-ca TEN | --dot-bien-dong [SONG_SONG]]", file=sys.stderr)
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
