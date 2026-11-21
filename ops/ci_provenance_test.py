#!/usr/bin/env python3
"""Phản chứng CHẠY ĐƯỢC cho `ops/ci_provenance.py` — packet #899 (wp899 P-A), đặc tả r2 A1–A8 + r3 A14–A18 + r4 A19–A27.

Fixture là log THẬT cắt gọn của run 39342960764 (Linux job 118368717941, Windows job 118368688495, CRLF giữ nguyên), khoá
bằng sha256 (c21). REST giả GIỮ TRẠNG THÁI: trả lời dựng từ run/jobs/log đang giữ, phân trang theo đúng `per_page`/`page`
của URL — không diễn kịch bản. ĐỘT BIẾN sửa BẢN SAO TẠM, ca đích chạy ở tiến trình con (`python -B`,
`PYTHONDONTWRITEBYTECODE=1`), phải XANH trên bản gốc trước. Chỉ `bang()` ném `TinHieuChotCa` (con in `DO:<ca>:`, thoát 3); lỗi vô
can thoát 4 ⇒ TÍN DỤNG GIẢ. `TU_KIEM` kiểm chính bộ phân hạng. r3: workflow giả (`wf_tu`) tiêm qua `wf=`; reader thật đo ở c34.
r4: REST giả giữ `steps[]` dựng MỘT lần từ log + workflow đang giữ (`buoc_rest`, độc lập với `ten_du_kien`); ca lệch sửa state ấy.

Ra: `CA: N/N dat` · `DOT BIEN: M/M bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (k dot bien)` · `TONG: DAT`.
#1322: dòng đầu `TIEN TRINH: n`; vòng đột biến chạy `n` luồng (`CI_PROVENANCE_TIEN_TRINH`), kết quả in theo thứ tự `DOT_BIEN`.
"""
import ast, collections, contextlib, warnings, hashlib, importlib.util, io, json, os, platform, random, re, subprocess, sys, tempfile, types, urllib.error, urllib.parse, urllib.request
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

def chay(cap, run=None, attempt=1, git=GIT, loi=None, them=None, sua=None, arts=(), hong_trang=None, than_run=None, wf=None, doi=()):
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
            rc = m.main(["thu", "--repo", "o/r", "--run", "5", "--attempt", str(attempt), "--out", str(o), *doi], goi=rest,
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
def c62_git_commit_khong_utf8():   # F13 (#955 review A) + #978 lượt 1: reader THẬT trên kho tạm, object dựng đúng byte bằng `hash-object`
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
        cho, so_dung = [], []   # r2 (Windows thật, tra-luat-win): ~600 lời gọi `hash-object` lẻ + oracle từng commit đẩy ca này quá timeout 300 s
        def cm(b, lit=()):   # của `chay_con` ⇒ commit hợp lệ GHI MỘT LƯỢT (`--stdin-paths`); OID tính trước, đối chiếu với OID Git trả về
            o = g("hash-object", "-t", "commit", "-w", *lit, "--stdin", i=b) if lit else hashlib.sha1(b"commit %d\0" % len(b) + b).hexdigest()
            cho.extend([] if lit else [b])
            so_dung.append((o, len(b)))   # sổ (OID, cỡ) LÚC DỰNG: chốt tồn tại ở dưới đọc sổ này, không đọc lại `cho`
            return o
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
        # lượt 6 (V3): MA TRẬN parent × dòng mở rộng × thân. Kỳ vọng tính ĐỘC LẬP với sản phẩm: phần đầu (tới LF-LF đầu tiên) có
        # ≠ 1 dòng bắt đầu `tree ` ⇒ None (M1), ngược lại ⇒ Git native (`log --no-walk`, kiểm ở vòng oracle dưới)
        bo_cha = ([], [P1], [P1, P1], [P1, P2, P1], [P1, P1, P1], [P2, P1, "0" * 39 + "1"], [f"{i:040x}" for i in range(1, 258)])   # trùng: AA·ABA·AAA
        pha = (b"", b"x-review start\n \ntree " + oid + b"\n", b"x-review start\n\t\ntree " + oid + b"\n",
               b"x-review start\n \t\ntree " + oid + b"\n", b"tree \n", b"x-review first\n \n tree " + oid + b"\n parent " + P1.encode() + b"\n",
               b"tree\t " + oid + b"\n", b"tree\r\n " + oid + b"\n", b"tree\n\t" + oid + b"\n", b"tree\r\n\t" + oid + b"\n",   # lượt 7: TAB+SP, gập
               b"tree: " + oid + b"\n", b"tree\\\n " + oid + b"\n")   # lượt 8: S01 `tree:` · S02 gập backslash-LF
        than = (None, b"m\n", b"first\n\ntree " + oid + b"\nparent " + P1.encode() + b"\n\nlast\n", b"tree " + oid + b"\n\nlast\n",
                b"\n\ntree " + oid + b"\nparent " + P1.encode() + b"\n")   # None = không có dòng trống, không thân
        for bc in bo_cha:
            for ph in pha:
                for th in than:
                    raw = f"tree {cay}\n".encode() + b"".join(f"parent {x}\n".encode() for x in bc) + ai(b"A") + ph + (b"" if th is None else b"\n" + th)
                    so_tree = sum(x.startswith(b"tree ") for x in raw.split(b"\n\n", 1)[0].split(b"\n"))
                    ca.append((cm(raw), {"tree": cay, "parents": bc} if so_tree == 1 else None))
        # nợ `wp978-git-reader-differential-fuzz`: vi sai NGẪU NHIÊN (seed cố định) — dòng mở rộng ghép từ token bẫy; kỳ vọng như ma trận
        bay = (b"tree", b"parent", b"Tree", "ｔｒｅｅ".encode(), b" ", b"\t", b"\r", b":", b"\\", b"\x0b", b"\x0c", b"\x85", b"\n", b"\n ", b"\r\n",
               oid, P1.encode(), b"x")
        ngau = random.Random(978)
        for _ in range(150):
            raw = dau[:-len(f"parent {P2}\n")] + ai(b"A") + b"".join(ngau.choice(bay) for _ in range(ngau.randint(1, 8))) + b"\n\nm\n"
            so_tree = sum(x.startswith(b"tree ") for x in raw.split(b"\n\n", 1)[0].split(b"\n"))
            ca.append((cm(raw), {"tree": cay, "parents": [P1]} if so_tree == 1 else None))
        hong = [b"tree %s\ntree %s\n" % (cay.encode(), cay.encode()), b"parent %s\n" % P1.encode(), b"tree %s1\n" % cay.encode(),
                b"tree " + b"g" * 40 + b"\n", b"tree " + cay.upper().encode() + b"\n", f"tree {cay}\nparent zz\n".encode(),
                f"tree {cay}\nparent {P1[:20]}".encode() + b"\xff" + P1[20:].encode() + b"\n", f"parent {P1}\ntree {cay}\n".encode(), f"tree {cay}\rparent {P1}\n".encode()]
        ca += [(cm(x + ai(b"A") + b"\nh\n", ("--literally",)), None) for x in hong]
        tep = []
        for i, b in enumerate(cho):
            (Path(thu) / f"c{i}").write_bytes(b)
            tep.append(str(Path(thu) / f"c{i}"))
        ghi = g("hash-object", "-t", "commit", "-w", "--stdin-paths", i="\n".join(tep).encode() + b"\n").split("\n")
        bang(ghi == [hashlib.sha1(b"commit %d\0" % len(b) + b).hexdigest() for b in cho], f"OID tính trước ≠ OID Git ghi ({len(ghi)}/{len(cho)})")
        ton = g("cat-file", "--batch-check", i="".join(f"{o}\n" for o, _ in so_dung).encode()).split("\n")   # lượt 10 P3: MỌI commit dựng, kể cả
        bang(ton == [f"{o} commit {n}" for o, n in so_dung], f"commit dựng thiếu/sai loại/cỡ: {[x for x in ton if not x.endswith(tuple(f' {n}' for _, n in so_dung))][:3]}")   # fixture âm
        ca += [(g("hash-object", "-w", "--stdin", i=v), None) for v in (b"\xff\n", b"tree zz\n", dau + ai(b"A") + b"\nblob\n")]   # blob, kể cả dạng commit
        the = g("hash-object", "-t", "tag", "-w", "--stdin",   # tag annotated dựng đúng byte: `git tag -a` đòi danh tính (runner CI không có)
                i=f"object {hop_le[0]}\ntype commit\ntag the\ntagger A <a@b> 1700000000 +0000\n\nt\n".encode())
        ca += [(cay, None), (the, None), ("0" * 40, None), ("", None), (f"{hop_le[0]}\nHEAD", None), (None, None), ("\udc80", None)]   # tree · tag · thiếu · rỗng · 2 dòng · không str · không mã hoá được
        d2, g2 = kho("sha256", "--object-format=sha256")
        cay2 = g2("mktree", i=f"100644 blob {g2('hash-object', '-w', '--stdin', i=b'x')}\tf\n".encode())
        ba2 = ["f" * 64, "0" * 63 + "1", "a" * 64]
        c2 = g2("hash-object", "-t", "commit", "-w", "--stdin", i=f"tree {cay2}\n".encode() + b"".join(f"parent {x}\n".encode() for x in ba2)
                + ai(b"Jos\xe9") + b"\nm\xe9ssage\n")
        mong = [k for _, k in ca] + [{"tree": cay2, "parents": ba2}]
        kq = []   # #1147 r2: so TỪNG mục ngay khi đọc ⇒ bản đột biến dừng ở mục lệch ĐẦU TIÊN, không đọc hết ~617 commit (Windows)
        for i, (x, d) in enumerate([(x, d1) for x, _ in ca] + [(c2, d2)]):
            kq.append(doc(x, d))
            bang(kq[i] == mong[i], f"git_cuc_bo lệch ở {i}: {kq[i]!r} ≠ {mong[i]!r}")
        bang(len(kq) == len(mong) == len(ca) + 1, f"chỉ so {len(kq)}/{len(mong)} mục")
        hop = [i for i, (_, k) in enumerate(ca) if type(k) is dict]   # oracle Git NATIVE cho mọi commit hợp lệ, MỘT lời gọi mỗi kho
        nat = {}
        for gg, xs in ((g, [ca[i][0] for i in hop]), (g2, [c2])):
            for dong in gg("log", "--no-walk=unsorted", "--stdin", "--format=%H%x00%T%x00%P", i="\n".join(xs).encode() + b"\n").split("\n"):
                h, t, p = dong.split("\0")
                nat[h] = {"tree": t, "parents": p.split()}
        da_so = 0
        for x, a in [(ca[i][0], kq[i]) for i in hop] + [(c2, kq[-1])]:   # `kq` là đầu ra reader đã đo ở trên, không gọi lại
            bang(a == nat.get(x), f"lệch Git native ở {x}: {a} ≠ {nat.get(x)}")
            da_so += 1
        bang(da_so == sum(type(k) is dict for _, k in ca) + 1, f"oracle chỉ so {da_so} mục")   # lượt 10 P3: đếm ĐỘC LẬP từ `ca`, không từ `hop`
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

# ---- CI-PROVENANCE-WD r1 (Issue #1094): `do-wd`, `thu --wd-run`, workflow `ops-do-workflow-definition.yml` ----
import base64, builtins, errno, shutil, zipfile
WD_OID, WD_PATH, XOA = "c" * 40, ".github/workflows/ci.yml", object()
WD_BYTES = b"name: ci\non: push\njobs: {}\n"
WF_WD_TEP = ROOT_THAT / ".github/workflows/ops-do-workflow-definition.yml"
GQL_CAN = ("WorkflowRun", "databaseId", "runNumber", "createdAt", "file", "path", "repositoryFileUrl", "checkSuite", "commit", "oid")
B64 = json.dumps({"encoding": "base64", "content": base64.b64encode(WD_BYTES).decode()}).encode()

def wd_node(**sua):
    return {"databaseId": 7, "runNumber": 3, "createdAt": "2026-11-01T00:00:00Z", "checkSuite": {"commit": {"oid": WD_OID}},
            "file": {"path": WD_PATH, "repositoryFileUrl": f"https://github.com/o/r/blob/{WD_OID}/{WD_PATH}"}} | sua

def do_wd_gia(run=None, gql=None, gql_ma=200, loi=None, node=None, than_run=None, noi=B64):
    run = {k: v for k, v in ({"id": 7, "run_attempt": 1, "event": "push", "head_sha": WD_OID, "path": WD_PATH, "check_suite_id": 1, "node_id": "WFR_x"}
                             | (run or {})).items() if v is not None}
    than = gql if isinstance(gql, bytes) else json.dumps(gql if gql is not None else {"data": {"node": node or wd_node()}}).encode()
    def goi(url):   # trả 404 cho mọi URL ngoài hợp đồng — kể cả contents sai `ref`
        u = urllib.parse.urlsplit(url)
        for k, ma in (loi or {}).items():
            if k in u.path:
                return ma, b""
        if u.path == "/repos/o/r/actions/runs/7" and not u.query:
            return 200, than_run or json.dumps(run).encode()
        if u.path == f"/repos/o/r/contents/{WD_PATH}" and u.query == f"ref={WD_OID}":
            return 200, noi
        return 404, b""
    m = nap()
    with tempfile.TemporaryDirectory(prefix="cip_wd_") as thu:
        o = Path(thu) / "wd.json"
        with contextlib.redirect_stdout(io.StringIO()):
            rc = m.main(["do-wd", "--repo", "o/r", "--run", "7", "--out", str(o)], goi=goi,
                        gql=lambda q, b: (gql_ma, than) if b == {"id": "WFR_x"} and all(re.search(rf"\b{t}\b", q) for t in GQL_CAN) else (500, b""))
        return rc, json.loads(o.read_text(encoding="utf-8"))

@ca
def c53_wd_passed():   # A2
    rc, j = do_wd_gia()
    git = subprocess.run(["git", "hash-object", "--stdin"], input=WD_BYTES, capture_output=True).stdout.decode().strip()
    bang(rc == 0 and j["trang_thai"] == "passed" and j["oid_dinh_nghia"] == WD_OID and j["blob"] == git
         and j["sha256"] == hashlib.sha256(WD_BYTES).hexdigest() and set(j) == nap().KHOA_WD, f"{rc} {j} git {git}")

@ca
def c54_wd_not_measured():   # A3: mỗi dòng not_measured của bảng §2.1 — đúng rc, đúng ly_do; JSON luôn có; dữ liệu hỏng ≠ failed
    loi2 = [{"path": ["node", "file"], "type": "FORBIDDEN", "message": "no ghp_ABCDEFGHIJ1234 " + "x" * 400},
            {"path": ["node", "checkSuite"], "type": "FORBIDDEN", "message": "x"}]
    url_ref = wd_node(file={"path": WD_PATH, "repositoryFileUrl": f"https://github.com/o/r/blob/master/{WD_PATH}"})
    for kw, ly in ((dict(loi={"/actions/runs/7": 404}), "rest_run_404"), (dict(gql_ma=403), "graphql_http_403"),
                   (dict(gql={"data": {"node": wd_node()}, "errors": loi2}), "graphql_errors"), (dict(gql={"data": {"node": None}}), "node_null"),
                   (dict(node=wd_node(file=None)), "file_null"), (dict(node=wd_node(checkSuite=None)), "checksuite_null"),
                   (dict(node=url_ref), "url_khong_oid"), (dict(node=url_ref, run={"event": "pull_request"}), "url_khong_oid"),
                   (dict(loi={"/contents/": 404}), "blob_http_404"), (dict(gql=b"<html>"), "phan_hoi_hong"),
                   (dict(than_run=b"<html>"), "phan_hoi_hong"), (dict(noi=b"<html>"), "phan_hoi_hong"),
                   (dict(noi=json.dumps({"encoding": "base64", "content": "!!!!"}).encode()), "phan_hoi_hong"),
                   (dict(run={"run_attempt": None}), "phan_hoi_hong"), (dict(gql={"data": {"node": wd_node()}, "errors": 1}), "phan_hoi_hong"),
                   (dict(node=wd_node(checkSuite={"commit": "wrong"})), "phan_hoi_hong"), (dict(node=wd_node(databaseId=None)), "phan_hoi_hong"),
                   (dict(node=wd_node(runNumber=None)), "phan_hoi_hong"), (dict(node=wd_node(createdAt=None)), "phan_hoi_hong"),
                   *[(dict(gql={"data": {"node": wd_node()}, "errors": e}), "phan_hoi_hong") for e in (0, False, "", {}, None)],
                   *[(dict(run={"event": ev}, node=wd_node(checkSuite={"commit": {"oid": "not-an-oid"}})), "phan_hoi_hong") for ev in ("push", "pull_request", "pull_request_target")],
                   *[(dict(gql=g), "phan_hoi_hong") for g in ({}, {"data": {}}, *[{"data": {"node": {k: v for k, v in wd_node().items() if k != b}}}
                                                                          for b in ("file", "checkSuite")])]):
        rc, j = do_wd_gia(**kw)
        bang(rc == 3 and j["trang_thai"] == "not_measured" and j["ly_do"] == ly, f"{ly} {kw}: rc={rc} {j}")
        bang(j.get("node_id") == ("WFR_x" if kw.keys() - {"than_run", "run"} and ly != "rest_run_404" else None), f"đường kiểm tường minh: {kw} {j}")
        if ly == "graphql_errors":
            bang([e["path"] for e in j["loi_graphql"]] == [["node", "file"], ["node", "checkSuite"]], f"{j['loi_graphql']}")
            bang("ghp_" not in json.dumps(j) and len(j["loi_graphql"][0]["message"]) == 300, "token lọt / không cắt 300 ký tự")

@ca
def c55_wd_failed():   # A4: mỗi phép so một ca, rc 12, ly_do đúng tên; phép so OID áp cho MỌI sự kiện thuộc SU_KIEN_SO_OID
    url = lambda repo="o/r", oid=WD_OID, path=WD_PATH: f"https://github.com/{repo}/blob/{oid}/{path}"
    for kw, ly in ((dict(node=wd_node(file={"path": WD_PATH, "repositoryFileUrl": url(repo="o/x")})), "repo"),
                   (dict(node=wd_node(file={"path": WD_PATH, "repositoryFileUrl": url(path="x.yml")})), "url_path"),
                   (dict(node=wd_node(file={"path": "x.yml", "repositoryFileUrl": url(path="x.yml")})), "file_path"),
                   (dict(node=wd_node(databaseId=8)), "databaseId"), *[(dict(run={"head_sha": "d" * 40, "event": ev}), "oid_head_sha")
                                                                        for ev in ("push", "workflow_dispatch", "schedule")],
                   (dict(node=wd_node(checkSuite={"commit": {"oid": "e" * 40}})), "oid_check_suite")):
        rc, j = do_wd_gia(**kw)
        bang(rc == 12 and j["trang_thai"] == "failed" and j["ly_do"] == ly, f"{ly} {kw}: rc={rc} {j}")

@ca
def c56_wd_pr():   # A4b: pull_request / pull_request_target — OID định nghĩa khác head/check-suite vẫn passed
    for ev in ("pull_request", "pull_request_target"):
        rc, j = do_wd_gia(run={"event": ev, "head_sha": "d" * 40}, node=wd_node(checkSuite={"commit": {"oid": "e" * 40}}))
        bang(rc == 0 and j["trang_thai"] == "passed" and j["head_sha_rest"] == "d" * 40 and j["check_suite_commit"] == "e" * 40, f"{ev}: {j}")

@ca
def c57_wd_sai_doi_so():   # A5: đích ghi theo ĐÚNG luật parser (`--out=x`, lặp ⇒ cái cuối); JSON tối thiểu nguyên văn
    m, toi_thieu = nap(), {"schema": "wd/1", "trang_thai": "not_measured", "ly_do": "sai_doi_so"}
    with tempfile.TemporaryDirectory(prefix="cip_wd_") as thu:
        a, b = Path(thu) / "a.json", Path(thu) / "b.json"
        for doi in (["--run", "0", "--out", str(b)], ["--run", "abc", f"--out={b}"], ["--run", "9" * 4301, "--out", str(b)], ["--run", "7", "--out", str(a), "--out", str(b)],
                    ["--run", "0", "--out", str(a), f"--out={b}"]):
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                rc = m.main(["do-wd", "--repo", "o r" if "7" in doi else "o/r", *doi], goi=lambda u: (500, b""), gql=lambda q, b: (500, b""))
            bang(rc == 2 and not a.exists() and b.exists() and json.loads(b.read_text()) == toi_thieu, f"{doi}: rc={rc}")
            b.unlink()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc = m.main(["do-wd", "--repo", "o/r", "--run", "7"], goi=lambda u: (500, b""), gql=lambda q, b: (500, b""))
        bang(rc == 2 and not any(Path(thu).iterdir()), "thiếu --out phải rc 2 và không ghi tệp")

def wd_zip(**sua):
    j = {"schema": "wd/1", "repo": "o/r", "run_id": 5, "path": WD_PATH, "trang_thai": "passed", "oid_dinh_nghia": H,
         "blob": hashlib.sha1(b"blob %d\0" % len(WD_BYTES) + WD_BYTES).hexdigest(), "sha256": hashlib.sha256(WD_BYTES).hexdigest(),
         "repository_file_url": f"https://github.com/o/r/blob/{H}/{WD_PATH}", "loi_graphql": [], "nguon": "ops/ci_provenance.py do-wd", "ly_do": None,
         "run_attempt_luc_do": 1, "event": "push", "node_id": "WFR_x", "run_number": 3, "created_at": "2026-11-01T00:00:00Z", "head_sha_rest": H,
         "check_suite_commit": H} | sua
    j = {k: v for k, v in j.items() if v is not XOA}
    with zipfile.ZipFile(b := io.BytesIO(), "w") as z:
        z.writestr(zipfile.ZipInfo("wd.json", (2026, 11, 1, 0, 0, 0)), json.dumps(j))   # dấu giờ GHIM: zip tất định
    return b.getvalue()
def thu_wd(w=None, arts=None, j=None, bo=False, run=None, kho=b'{"default_branch": "master"}', cmp="behind",
           ref={"ref": "refs/heads/master", "object": {"type": "commit", "sha": "b" * 40}}):   # đi qua CLI thật `thu ... --wd-run 77`
    zb = wd_zip(**(j or {}))
    w = {k: v for k, v in ({"path": ".github/workflows/ops-do-workflow-definition.yml", "head_branch": "master", "event": "workflow_dispatch",
         "conclusion": "success", "repository": {"full_name": "o/r"}, "head_sha": "a" * 40} | (w or {})).items() if v is not None}
    arts = arts if arts is not None else [{"id": 9, "name": "workflow-definition-5", "expired": False, "digest": "sha256:" + hashlib.sha256(zb).hexdigest()}]
    dap = {"/repos/o/r": kho, "/repos/o/r/actions/runs/77": json.dumps(w).encode(), "/repos/o/r/actions/artifacts/9/zip": zb,
           "/repos/o/r/actions/runs/77/artifacts": json.dumps({"total_count": len(arts), "artifacts": arts}).encode(),
           "/repos/o/r/git/ref/heads/master": json.dumps(ref).encode(), f"/repos/o/r/compare/{'b' * 40}...{'a' * 40}": json.dumps({"status": cmp}).encode(), f"/repos/o/r/contents/{WD_PATH}?ref={H}": B64, f"/repos/o/r/contents/{WD_PATH}?ref={'f' * 40}": B64}
    def sua(m):
        goc = m.nhap_wd
        m.nhap_wd = lambda goi, *a: goc(lambda url: (lambda u: (200, dap[u]) if u in dap else goi(url))(
            urllib.parse.urlsplit(url).path + ("?" + urllib.parse.urlsplit(url).query if "/contents/" in url else "")), *a)
    return chay([(job(1), LINUX)], run=run, sua=sua, doi=() if bo else ("--wd-run", "77"))[2]["moc"]["workflow_definition"]

@ca
def c58_thu_wd_run():   # A6: bằng chứng chỉ từ artifact của chính lượt workflow trên nhánh mặc định, rồi TÍNH LẠI
    d = thu_wd()
    bang(d["trang_thai"] == "passed" and d["artifact_id"] == 9 and d["wd_run_id"] == 77 and d["oid"] == H
         and d["artifact_sha256"] == hashlib.sha256(wd_zip()).hexdigest(), f"{d}")
    for kw, ly in ((dict(w={"path": ".github/workflows/ci.yml"}), "a:path"), *[(dict(cmp=c), "a:head_sha") for c in ("ahead", "diverged", None)],   # tag `master` ngoài nhánh mặc định ⇒ compare ahead/diverged
                   (dict(w={"head_sha": None}), "a:head_sha"), (dict(kho=b"{}"), "a:head_sha"), (dict(cmp="identical", w={"head_branch": "v1"}), None),
                   *[(dict(ref=r), "a:head_sha") for r in ({"ref": "refs/tags/master", "object": {"type": "commit", "sha": "b" * 40}},
                                                           {"ref": "refs/heads/master", "object": {"type": "tag", "sha": "b" * 40}}, [], {"ref": "refs/heads/master"})], (dict(w={"event": "push"}), "a:event"),
                   (dict(w={"conclusion": "failure"}), "a:conclusion"), (dict(w={"repository": {"full_name": "o/x"}}), "a:repo"),
                   (dict(w={"repository": "o/r"}), "a:repo"), (dict(arts=[]), "b:artifact"),
                   (dict(arts=[{"id": 9, "name": "workflow-definition-5", "expired": False, "digest": "sha256:" + "0" * 64}]), "b:digest"),
                   (dict(j={"schema": "x"}), "c:schema"), (dict(j={"repo": "o/x"}), "c:repo"), (dict(j={"run_id": 6}), "c:run_id"),
                   (dict(j={"path": "x.yml"}), "c:path"), (dict(j={"trang_thai": "failed"}), "c:trang_thai"),
                   *[(dict(j={k: XOA}), "c:khoa") for k in ("loi_graphql", "nguon", "ly_do", "event")], (dict(j={"them": 1}), "c:khoa"),
                   (dict(j={"nguon": "anything"}), "c:khoa"), *[(dict(j={"path": v}), "c:path") for v in (None, "", 1, True)], (dict(j={"path": None}, run={"path": None}), "c:path"), (dict(j={"run_id": 5.0}), "c:run_id"), (dict(j={"run_id": True}), "c:run_id"),
                   *[(dict(j={k: v}), "c:meta") for k, v in (("run_attempt_luc_do", "1"), ("run_number", 0), ("node_id", ""), ("head_sha_rest", "x"))],
                   (dict(j={"blob": "a" * 40}), "d:blob"), (dict(j={"sha256": "b" * 64}), "d:sha256"),
                   (dict(j={"repository_file_url": "https://github.com/o/r/blob/x/y"}), "d:url"),
                   (dict(j={"oid_dinh_nghia": "f" * 40, "repository_file_url": f"https://github.com/o/r/blob/{'f' * 40}/{WD_PATH}"}), "d:oid_head_sha"),
                   (dict(j={"oid_dinh_nghia": "e" * 40, "repository_file_url": f"https://github.com/o/r/blob/{'e' * 40}/{WD_PATH}"}), "d:rest_404")):
        d = thu_wd(**kw)
        bang(d["trang_thai"] == "passed" if ly is None else d["trang_thai"] == "not_measured" and d.get("ly_do") == f"wd_khong_hop_le:{ly}", f"{ly}: {d}")
    a9 = {"id": 9, "name": "workflow-definition-5", "expired": False, "digest": "sha256:" + hashlib.sha256(wd_zip()).hexdigest()}
    for ds in ([a9, a9], [a9, a9 | {"id": 10}], [a9 | {"expired": True}]):   # trùng ID (du=False) · hai artifact · hết hạn — digest ĐÚNG
        bang(thu_wd(arts=ds).get("ly_do") == "wd_khong_hop_le:b:artifact", f"{ds} phải không hợp lệ: {thu_wd(arts=ds)}")
    bang(thu_wd(bo=True)["trang_thai"] == "not_measured" and thu_wd(bo=True)["ly_do"] == "graphql_bi_chan_trong_phien_claude; cho P-B",
         "không --wd-run ⇒ giữ nguyên P-A")
MAU_THAN = "\n".join(("set +e", 'python3 ops/ci_provenance.py do-wd --repo "$REPO" --run "$RUN_ID" --out wd.json', "rc=$?",
                      "if [ ! -f wd.json ]; then",
                      """  printf '{"schema": "wd/1", "trang_thai": "not_measured", "ly_do": "collector_khong_ghi_rc_%s"}\\n' "$rc" > wd.json""",
                      "fi", "cat wd.json", """{ echo '```json'; cat wd.json; echo '```'; } >> "$GITHUB_STEP_SUMMARY\"""", 'exit "$rc"', ""))
def kiem_wf(van):   # A7: DANH SÁCH CHO PHÉP trọn cấu trúc — mọi job/bước/khoá; trả danh sách vi phạm
    d, loi, J = yaml.safe_load(van), [], lambda x: json.dumps(x, sort_keys=True)   # so qua JSON: True ≠ 1, False ≠ 0
    on, jobs = d.get("on", d.get(True)), list(d.get("jobs", {}).values())
    loi += ["on"] if J(on) != J({"workflow_dispatch": {"inputs": {"run_id": {"description": "id workflow run cần đo mốc Workflow definition", "required": True, "type": "string"}}}}) else []
    loi += ["permissions"] if d.get("permissions") != {"contents": "read", "actions": "read"} or set(d) - {"name", "on", True, "permissions", "jobs"} or [k.value for k, _ in yaml.compose(van).value] != ["name", "on", "permissions", "jobs"] else []
    if len(jobs) != 1 or set(jobs[0]) != {"runs-on", "timeout-minutes", "steps"} or (jobs[0]["runs-on"], jobs[0]["timeout-minutes"]) != ("ubuntu-latest", 10):
        return loi + ["job"]
    b = jobs[0]["steps"]
    if len(b) != 4:
        return loi + ["buoc"]
    loi += ["checkout"] if J(b[0]) != J({"uses": "actions/checkout@v4", "with": {"ref": "master", "persist-credentials": False}}) else []
    loi += ["pip"] if set(b[1]) != {"name", "run"} or b[1]["run"] != "python3 -m pip install --quiet PyYAML==6.0.3" else []
    loi += ["env"] if set(b[2]) != {"name", "env", "run"} or b[2]["env"] != {"RUN_ID": "${{ inputs.run_id }}", "REPO": "${{ github.repository }}",
                                                                          "GH_TOKEN": "${{ github.token }}"} else []
    loi += ["collector"] if b[2].get("run") != MAU_THAN else []
    loi += ["upload"] if b[3] != {"uses": "actions/upload-artifact@v4", "if": "always()",
                                  "with": {"name": "workflow-definition-${{ inputs.run_id }}", "path": "wd.json"}} else []
    return loi

@ca
def c59_workflow_tinh():   # A7: tệp thật sạch; MỖI đột biến YAML một vi phạm đúng tên
    bang(kiem_wf(van := WF_WD_TEP.read_text(encoding="utf-8")) == [], f"workflow thật vi phạm: {kiem_wf(van)}")
    for cu, moi, mong in (("    runs-on: ubuntu-latest\n", "    runs-on: ubuntu-latest\n    permissions:\n      pull-requests: write\n", "job"),
                          ("    runs-on: ubuntu-latest\n", "    if: false\n    runs-on: ubuntu-latest\n", "job"),
                          ("runs-on: ubuntu-latest", "runs-on: windows-latest", "job"), ("runs-on: ubuntu-latest", "runs-on: self-hosted", "job"),
                          ("          ref: master\n", "", "checkout"), ("ref: master", "ref: ${{ github.sha }}", "checkout"),
                          ("          persist-credentials: false\n", "", "checkout"), ("persist-credentials: false", "persist-credentials: 0", "checkout"),
                          ("required: true", "required: 1", "on"), ("\non:\n", "\n1:\n", "permissions"), ("\non:\n", '\n"on":\n', None), ("\non:\n", "\ntrue:\n", "permissions"),
                          ("\npermissions:\n", "\n1.0:" + van.split("\non:", 1)[1].split("\npermissions:")[0] + "\npermissions:\n", "permissions"),
                          ("      - name: cài PyYAML\n", "      - uses: actions/checkout@v4\n      - name: cài PyYAML\n", "buoc"),
                          ('          rc=$?\n', '          rc=$?\n          eval "$RUN_ID"\n', "collector"), ('          rc=$?\n', '          rc=$?\n          curl -s x\n', "collector"),
                          ("          python3 ops/ci_provenance.py do-wd", "          # python3 ops/ci_provenance.py do-wd", "collector"),
                          ("          python3 ops/ci_provenance.py do-wd", "          echo python3 ops/ci_provenance.py do-wd", "collector"),
                          ('"$RUN_ID" --out', '${{ inputs.run_id }} --out', "collector"), ("          GH_TOKEN: ${{ github.token }}\n", "", "env"),
                          ("RUN_ID: ${{ inputs.run_id }}", "RUN_ID: '7'", "env"), ("REPO: ${{ github.repository }}", "REPO: o/x", "env"),
                          ("path: wd.json", "path: .", "upload"), ("        if: always()\n", "", "upload"),
                          ("name: workflow-definition-${{ inputs.run_id }}", "name: wd", "upload")):
        bang(van.count(cu) == 1, f"neo YAML {cu!r} phải xuất hiện đúng 1 lần")
        bang(kiem_wf(van.replace(cu, moi)) == [] if mong is None else mong in kiem_wf(van.replace(cu, moi)), f"đột biến {cu!r} -> {moi!r} không bị bắt: {kiem_wf(van.replace(cu, moi))}")
def chay_than(van, ghi=False, rc=3, bash=None):   # A7b: chạy CHÍNH thân `run:` của bước collector với python3 giả
    b = next(b for jb in yaml.safe_load(van)["jobs"].values() for b in jb["steps"] if "do-wd" in b.get("run", ""))
    with tempfile.TemporaryDirectory(prefix="cip_than_") as thu:
        t, gia = Path(thu), Path(thu) / "bin"
        gia.mkdir() or (gia / "python3").write_text("#!/bin/sh\nprintf '%s\\n' \"$@\" > argv.txt\n" + ('printf "{}" > wd.json\n' if ghi else "") + f"exit {rc}\n", newline="\n")
        (gia / "python3").chmod(0o755)
        (t / "than.sh").write_text(b["run"], newline="\n")   # ghim LF: Windows native ghi CRLF ⇒ `set +e\r` gãy (review lượt 9)
        env = dict(os.environ, RUN_ID="1; touch PWNED", REPO="o/r", GH_TOKEN="x", GITHUB_STEP_SUMMARY=str(t / "sum.md"),
                   PATH=f"{gia}{os.pathsep}{os.environ.get('PATH', '')}")
        r = subprocess.run([bash or __import__("bash_nen").tim_bash()[0], "-e", str(t / "than.sh")], cwd=thu, env=env, capture_output=True, timeout=60)
        return r.returncode, *[(t / n).read_text() if (t / n).exists() else None for n in ("argv.txt", "wd.json", "sum.md")], (t / "PWNED").exists()

@ca
def c60_workflow_than_chay():   # A7b: mỗi đột biến một phép kiểm RIÊNG, và collector giả phải ĐÃ CHẠY (lỗi setup không được tính giết)
    if not __import__("bash_nen").tim_bash()[0]:   # bộ giải dùng chung (#570): `bash` trần trên Windows có thể là WSL
        return bang(not (ROOT_THAT / ".git").exists(), "không có bash dùng được trong kho thật: KHÔNG ĐO ĐƯỢC ⇒ đỏ")
    rc, argv, wd, tom, pw = chay_than(van := WF_WD_TEP.read_text(encoding="utf-8"))
    bang(argv is not None and argv.splitlines() == ["ops/ci_provenance.py", "do-wd", "--repo", "o/r", "--run", "1; touch PWNED", "--out", "wd.json"] and not pw, f"argv {argv!r} / PWNED={pw}")
    bang(rc == 3 and wd is not None and "collector_khong_ghi_rc_3" in wd and tom is not None and "collector_khong_ghi_rc_3" in tom, f"rc={rc} wd={wd!r}")
    bang(chay_than(van, ghi=True, rc=12)[:3] == (12, argv, "{}"), "collector đã ghi wd.json thì không được ghi đè")
    for cu, moi, ok in (('--run "$RUN_ID"', "--run $RUN_ID", lambda r, a, w, t: r == 3 and a is not None and "touch" in a.splitlines()),
                        ('          if [ ! -f wd.json ]; then', '          if false; then', lambda r, a, w, t: r == 3 and a == argv and w is None),
                        ('          cat wd.json\n          {', '          exit "$rc"\n          cat wd.json\n          {',
                         lambda r, a, w, t: r == 3 and a == argv and w == wd and t is None)):
        bang(van.count(cu) == 1, f"neo {cu!r}")
        bang(ok(*chay_than(van.replace(cu, moi))[:4]), f"đột biến {cu!r} không bị bắt đúng dấu hiệu")

@ca
def c61_actionlint_bat_yaml_sai():   # A8: actionlint + ShellCheck; tệp thật sạch; `type: number123` ⇒ đỏ; thiếu công cụ trong kho thật ⇒ KHÔNG ĐO ĐỦ ⇒ đỏ
    if not ((al := shutil.which("actionlint")) and shutil.which("shellcheck")):
        return bang(not (ROOT_THAT / ".git").exists(), "thiếu actionlint/shellcheck trong kho thật: KHÔNG ĐO ĐỦ ⇒ đỏ")
    with tempfile.TemporaryDirectory(prefix="cip_al_") as thu:
        for v, mong in (((van := WF_WD_TEP.read_text(encoding="utf-8")), 0), (van.replace("        type: string\n", "        type: number123\n"), 1)):
            (Path(thu) / "w.yml").write_text(v, encoding="utf-8")
            r = subprocess.run([al, str(Path(thu) / "w.yml")], capture_output=True, text=True, timeout=120)
            bang(r.returncode == mong and (mong == 0 or "number123" in r.stdout), f"mong rc {mong}, được {r.returncode}: {r.stdout[-300:]}")

@ca
def c63_ban_goc_mot_lan_moi_ca():   # #997 hậu merge: bản gốc chạy MỘT lần mỗi (ca đích, bản gốc); quá hạn ⇒ HONG có tên, không sập bộ
    goi = []
    def gia(ten_ca, ma):
        goi.append((ten_ca, Path(ma).name))
        return (0, "") if Path(ma).name == "goc.py" else (3, f"DO:{ten_ca}: x")
    nhom = [d for d in DOT_BIEN if d[3] == "c34"][:2]
    bang(len(nhom) == 2, f"cần 2 mục đột biến nhắm c34, có {len(nhom)}")
    with mock.patch.dict(_NEN, clear=True), mock.patch(__name__ + ".chay_con", side_effect=gia):
        hang = [chay_dot_bien(*d)[0] for d in nhom]
    bang(hang == ["GIET", "GIET"] and [x for x in goi if x[1] == "goc.py"] == [("c34_git_blob_that", "goc.py")]
         and sum(x[1] != "goc.py" for x in goi) == 2, f"bản gốc phải chạy đúng 1 lần cho 2 mục: {hang} {goi}")
    with mock.patch.dict(_NEN, clear=True), mock.patch(__name__ + ".chay_con", return_value=(3, "DO:c34_git_blob_that: goc do")) as cc:
        hang = [chay_dot_bien(*d)[0] for d in nhom]
    bang(hang == ["HONG", "HONG"] and cc.call_count == 1, f"bản gốc đỏ ⇒ MỌI mục HONG, chạy gốc 1 lần: {hang} {cc.call_count}")
    with mock.patch.dict(_NEN, clear=True), mock.patch(__name__ + ".chay_con",   # Codex lượt 1 P3: KHOÁ gồm CẢ ca lẫn nội dung bản gốc
                                                       side_effect=lambda t, ma: (0, f"{t}:{Path(ma).read_text(encoding='utf-8')}")) as cc:
        kq = [nen_cua(t, g)[1] for t, g in (("ca_a", "x"), ("ca_a", "y"), ("ca_b", "x"), ("ca_a", "x"), ("ca_b", "x"))]
    bang(kq == ["ca_a:x", "ca_a:y", "ca_b:x", "ca_a:x", "ca_b:x"] and cc.call_count == 3, f"khoá cache (ca, nội dung): {kq} {cc.call_count}")
    with mock.patch.object(subprocess, "run", side_effect=subprocess.TimeoutExpired("python", 300)):
        try:
            rc, ra = chay_con("c34_git_blob_that", HERE / "ci_provenance.py")
        except subprocess.TimeoutExpired:
            rc, ra = None, "TimeoutExpired lọt khỏi chay_con"
    bang(rc == 124 and "QUA_HAN:c34_git_blob_that" in ra and phan_hang(rc, ra, "c34_git_blob_that") == "HONG", f"quá hạn ⇒ 124/HONG: {rc} {ra}")

@ca
def c64_so_tien_trinh_mien():   # #1322 M1/A2: vắng ⇒ min(4, cpu) trên Linux, 1 nơi khác; có biến ⇒ ĐÚNG một chữ số ASCII 1–8
    bang(so_tien_trinh({}, "Linux", 8) == 4 and so_tien_trinh({}, "Linux", 2) == 2 and so_tien_trinh({}, "Linux", 0) == 1,
         "vắng biến trên Linux ⇒ min(4, cpu), cpu 0/None ⇒ 1")
    bang(so_tien_trinh({}, "Windows", 8) == 1 and so_tien_trinh({}, "Darwin", 8) == 1, "vắng biến ngoài Linux ⇒ 1 (#997)")
    bang(all(so_tien_trinh({BIEN_TIEN_TRINH: str(k)}, "Windows", 2) == k for k in range(1, 9)), "1..8 nhận đúng số, mọi nền")
    lot = []
    for x in ("0", "9", "a", "", " 4", "4 ", "04", "4\n", "４", "+4", "4.0", "10"):
        try:
            so_tien_trinh({BIEN_TIEN_TRINH: x}, "Linux", 8)
            lot.append(x)
        except ValueError:
            pass
    bang(not lot, f"giá trị ngoài miền phải ValueError, lọt: {lot!r}")

def _bo_thuc_thi_dieu_khien(tao):   # #1322 review lượt 4 F1: Future THẬT, chỉ hoàn tất SAU KHI bộ gom bắt đầu chờ, theo thứ tự NGƯỢC 5..0
    import concurrent.futures, threading   # ⇒ `map` (chờ `result()` theo thứ tự) vẫn ra đúng thứ tự; `as_completed` (chờ qua `_waiters`) ra NGƯỢC — tất định, không sleep, không lặp
    class _Cond(threading.Condition):
        def __init__(self, bao):
            super().__init__()
            self._bao = bao
        def wait(self, timeout=None):   # `Future.result()` chờ ở đây
            self._bao.set()
            return super().wait(timeout)
    class _Ds(list):
        def __init__(self, bao):
            super().__init__()
            self._bao = bao
        def append(self, x):   # `as_completed` cài waiter ở đây
            self._bao.set()
            super().append(x)
    class TuongLai(concurrent.futures.Future):
        def __init__(self, bao, chi_so):
            super().__init__()
            self._condition, self._waiters, self._bam = _Cond(bao), _Ds(bao), (2, 0, 4, 1, 5, 3)[chi_so]
        def __hash__(self):   # review lượt 4 F1: bộ gom "chờ hết rồi duyệt tập đã xong" đi theo thứ tự BĂM (hoặc ngược nó) ⇒ hoán vị không đơn điệu: cả hai chiều đều KHÁC thứ tự việc
            return self._bam
    class BoThucThi(concurrent.futures.Executor):
        def __init__(self, *a, **k):
            self.viec, self.bao, self.xong, self.qua_han = [], threading.Event(), [], False
            tao.append(self)
            self.luong = threading.Thread(target=self._hoan_tat, daemon=True)
            self.luong.start()
        def submit(self, fn, *a, **k):
            f = TuongLai(self.bao, len(self.viec))
            self.viec.append((f, fn, a, k))
            return f
        def _hoan_tat(self):
            self.qua_han = not self.bao.wait(10)
            for i in reversed(range(len(self.viec))):
                f, fn, a, k = self.viec[i]
                try:
                    f.set_result(fn(*a, **k))
                except BaseException as e:   # noqa: BLE001 — trả về qua Future, người gom tự ném lại
                    f.set_exception(e)
                self.xong.append(i)
        def shutdown(self, wait=True, *, cancel_futures=False):
            if wait:
                self.luong.join(30)
    return BoThucThi

def _thu_tu_tat_dinh():
    import concurrent.futures
    tao = []
    Bo = _bo_thuc_thi_dieu_khien(tao)
    with Bo() as ex:   # đối chứng ÂM trên chính bộ giả: gom theo thứ tự xong PHẢI khác thứ tự việc, nếu không bộ giả hỏng (hạ tầng, không phải chốt)
        fs = [ex.submit(lambda i: i, i) for i in range(6)]
        doi = [f.result() for f in concurrent.futures.as_completed(fs)]
    if sorted(doi) != list(range(6)) or doi == list(range(6)) or tao[0].qua_han:
        raise RuntimeError(f"c65: bộ thực thi điều khiển không tất định: {doi!r}, quá hạn={tao[0].qua_han}")
    with mock.patch("concurrent.futures.ThreadPoolExecutor", Bo):
        r = chay_theo_thu_tu(lambda i: i * 10, range(6), 4)
    if len(tao) > 1 and tao[1].qua_han:
        raise RuntimeError("c65: bộ gom không chờ future nào trong 10 s — bộ giả không điều khiển được thứ tự")
    bang(r == [0, 10, 20, 30, 40, 50], f"bộ thực thi hoàn tất NGƯỢC 5..0: kết quả phải theo thứ tự việc, được {r!r}")

@ca
def c65_chay_theo_thu_tu():   # #1322 M4/A3: thứ tự xong bị ĐẢO ⇒ đầu ra vẫn theo thứ tự việc; n = 1 tuần tự. Đúng phạm vi đặc tả:
    bang(chay_theo_thu_tu(lambda i: i * i, range(5), 1) == [0, 1, 4, 9, 16], "n=1 tuần tự, đúng thứ tự")
    _thu_tu_tat_dinh()   # review lượt 4 F1: bộ thực thi điều khiển hoàn tất NGƯỢC, tất định. Phép đo "chạy chồng" (luồng phụ → Barrier →
    # cấu hình pool, đột biến T4) đã GỠ sau Review Rescue Checkpoint thứ hai: nó nằm NGOÀI M4/A3 và là nơi lớp
    # `loi-luong-nen-bi-tinh-la-giet-dung` tái diễn ở lượt 2–8 (sổ uỷ quyền #1322 comment 7046235668)

@ca
def c66_mien_sai_chan_truoc_moi_ca():   # #1322 A2: giá trị lạ ⇒ rc≠0 TRƯỚC khi chạy ca nào
    with mock.patch.dict(os.environ, {BIEN_TIEN_TRINH: "0"}), mock.patch(__name__ + ".chay_ca", return_value=(0, "")) as cc, \
            mock.patch(__name__ + ".lam_nong_nen"), mock.patch(__name__ + ".chay_dot_bien", return_value=("GIET", "")), \
            mock.patch(__name__ + ".chay_dot_bien_test", return_value=("GIET", "")), \
            contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()) as loi:
        rc = main([])
    bang(rc == 2 and cc.call_count == 0 and BIEN_TIEN_TRINH in loi.getvalue(), f"rc={rc}, số ca đã chạy {cc.call_count}")
    # review lượt 1 F3 + lượt 5 F3b/F3c: kết quả phải khớp KẾ HOẠCH (tên, thứ tự, số lần) — thiếu, lặp, đảo, rỗng ⇒ TONG: DO
    for ten_kq, rc_mong in ((("m1", "m2"), 0), (("m2",), 1), (("m1",), 1), ((), 1), (("m1", "m1"), 1), (("m2", "m1"), 1),
                            (("m1", "m2", "m2"), 1)):
        with mock.patch.dict(os.environ, {BIEN_TIEN_TRINH: "2"}), mock.patch(__name__ + ".chay_ca", return_value=(0, "")), \
                mock.patch(__name__ + ".TU_KIEM", ()), mock.patch(__name__ + ".DOT_BIEN", (("m1",),)), \
                mock.patch(__name__ + ".DOT_BIEN_TEST", (("m2",),)), \
                mock.patch(__name__ + ".chay_vong_dot_bien", return_value=[(t, "GIET", "") for t in ten_kq]), \
                contextlib.redirect_stdout(io.StringIO()) as ra:
            rc = main([])
        bang(rc == rc_mong and ra.getvalue().endswith(f"TONG: {'DO' if rc_mong else 'DAT'}\n"), f"kết quả {ten_kq!r} cho kế hoạch m1,m2: rc={rc}")

@ca
def c67_lam_nong_truoc_vong_dot_bien():   # #1322 M2, review lượt 1 F2: bản gốc của MỌI ca đích (cả `DOT_BIEN_TEST`) xong TRƯỚC đột biến đầu tiên, mỗi khoá một lần
    import threading
    nhom = tuple([d for d in DOT_BIEN if d[3] == "c34"][:2] + [d for d in DOT_BIEN if d[3] == "c58"][:1])
    dich = {[c for c in CA if c.split("_")[0] == p][0] for p in ("c34", "c58", DOT_BIEN_TEST[0][3])}
    for n in (1, 4):
        nhat_ky, khoa = [], threading.Lock()
        def con(ten_ca, loai):
            with khoa:
                nhat_ky.append((loai, ten_ca))
            return (0, "") if loai == "goc" else (3, f"DO:{ten_ca}: x")
        with mock.patch.dict(_NEN, clear=True), mock.patch(__name__ + ".DOT_BIEN", nhom), mock.patch(__name__ + ".TU_KIEM", ()), \
                mock.patch(__name__ + ".DOT_BIEN_TEST", DOT_BIEN_TEST[:1]), \
                mock.patch(__name__ + ".chay_con", side_effect=lambda t, ma: con(t, "goc" if Path(ma).name == "goc.py" else "db")), \
                mock.patch(__name__ + ".chay_con_ban_test", side_effect=lambda t, ban: con(t, "db")):
            viec = [(co_ten(chay_dot_bien), d) for d in nhom] + [(co_ten(chay_dot_bien_test), d) for d in DOT_BIEN_TEST[:1]]
            kq = chay_vong_dot_bien(n, viec)
        goc = [t for loai, t in nhat_ky if loai == "goc"]
        dau = [loai for loai, _ in nhat_ky].index("db")
        bang(sorted(goc) == sorted(dich), f"n={n}: mỗi ca đích chạy bản gốc ĐÚNG một lần: {goc}")
        bang({loai for loai, _ in nhat_ky[:dau]} == {"goc"} and "goc" not in {loai for loai, _ in nhat_ky[dau:]},
             f"n={n}: mọi bản gốc phải xong TRƯỚC đột biến đầu tiên: {nhat_ky}")
        bang([(t, h) for t, h, _ in kq] == [(d[0], "GIET") for _, d in viec] and len(viec) == 4, f"n={n}: mỗi việc đúng một kết quả, đúng tên: {kq}")

@ca
def c68_moi_viec_dung_ket_qua_cua_no():   # #1322 review lượt 6 F3d: runner THẬT, mỗi việc một kết quả RIÊNG (có SONG_SOT) — gắn tên đúng mà chạy nhầm việc ⇒ đỏ
    def gia(ten, *_):
        return ("SONG_SOT" if ten == "v5" else "GIET", f"chi tiet {ten}")
    ke_hoach = [(co_ten(gia), (f"v{i}", "neo", "thay", "c00")) for i in range(6)]
    mong = [(f"v{i}", "SONG_SOT" if i == 5 else "GIET", f"chi tiet v{i}") for i in range(6)]
    for n in (1, 4):
        with mock.patch(__name__ + ".lam_nong_nen"):
            kq = chay_vong_dot_bien(n, list(ke_hoach))
        bang(kq == mong, f"n={n}: mỗi việc phải mang ĐÚNG kết quả của chính nó, được {kq!r}")

CU_BYTE, MOI_BYTE = {"cu.txt": b"ban truoc"}, {"provenance.yaml": b"a", "run.json": b"c"}

def _doc_cay(d):   # đọc ĐỆ QUY (review lượt 3 F2.f: cây lồng): đường dẫn tương đối dạng `a/x` → byte
    return {x.relative_to(d).as_posix(): x.read_bytes() for x in sorted(d.rglob("*")) if x.is_file()} if d.is_dir() else None

class _StderrHong(io.StringIO):
    def __init__(self, loi=None):
        super().__init__()
        self.loi = loi

    def write(self, s):
        raise self.loi if self.loi is not None else OSError(28, "stderr đầy (giả)")

def _ghi_voi_doi_ten_gia(ke_hoach, *, windows=True, co_cu=False, xoa=None, onexc=None, stderr_hong=False, moi=None, cu_cay=None, lien_ket=None, bat_moi=False, ngat_ngu=None, ngat_ghi=None):
    """#1475: chạy `ghi_nguyen_tu` với `_thay_the`/`_xoa_cay`/`ngu_thu_lai` giả. `ke_hoach[cho]` (cho ∈ a cất bản trước ·
    b đưa tạm vào chỗ · c hoàn tác) là hàm nhận số thứ tự lời gọi ở chỗ ấy, trả ngoại lệ để ném hay None để đổi tên THẬT.
    `xoa[cho]` (cho ∈ tam · cu) nhận số thứ tự lần dọn, trả None (rmtree THẬT) hoặc {"unlink"|"rmdir": [lỗi…]}: rmtree THẬT
    chạy với `os.unlink`/`os.rmdir` ném lần lượt các lỗi ấy (None = gọi thật) — giữ nguyên chuỗi callback của stdlib, kể cả
    ENOTEMPTY thứ cấp (review lượt 2 F2.d); hoặc {"theo_ten": {tên tệp: hàm(số thứ tự lần dọn) → lỗi | None}} tiêm theo TÊN,
    không phụ thuộc thứ tự duyệt thư mục (lượt 3 F2.f). `onexc` ép nhánh `_DUNG_ONEXC`; `stderr_hong` là True (OSError) hay một
    ngoại lệ để stream ném; `moi`/`cu_cay` là cây mới/cây bản trước (mặc định MOI_BYTE/CU_BYTE, khoá dạng `a/x`). Trả một dict."""
    m, goi, ngu, goi_xoa = nap(), [], [], []

    def gia(nguon, dich):
        n, d = Path(nguon).name, Path(dich).name
        cho = "c" if n.endswith(".cu") else ("a" if d.endswith(".cu") else "b")
        goi.append(cho)
        loi = ke_hoach.get(cho, lambda i: None)(goi.count(cho) - 1)
        if loi is not None:
            raise loi
        os.replace(nguon, dich)

    def tiem(that, ds):
        def f(*a, **kw):
            loi = ds.pop(0) if ds else None
            if loi is not None:
                raise loi
            return that(*a, **kw)
        return f

    def xoa_gia(duong, **kw):
        cho = "cu" if Path(duong).name.endswith(".cu") else "tam"
        goi_xoa.append(cho)
        kh = (xoa or {}).get(cho, lambda i: None)(goi_xoa.count(cho) - 1)
        if isinstance(kh, BaseException):   # ngắt ngay trong lần dọn (review lượt 12 F2.v)
            raise kh
        if kh is None:
            return shutil.rmtree(duong, **kw)
        lan, theo_ten = goi_xoa.count(cho) - 1, kh.get("theo_ten")

        def theo(that, tien_to):   # tiêm theo TÊN nút: "x" cho unlink tệp/link tên x, "@d" cho rmdir thư mục tên d
            def f(ten, *a, **k):
                loi = theo_ten.get(tien_to + os.path.basename(os.fspath(ten).rstrip("/\\")), lambda i: None)(lan)
                if loi is not None:
                    raise loi
                return that(ten, *a, **k)
            return f
        with mock.patch.object(os, "unlink", theo(os.unlink, "") if theo_ten else tiem(os.unlink, list(kh.get("unlink", [])))), \
                mock.patch.object(os, "rmdir", theo(os.rmdir, "@") if theo_ten else tiem(os.rmdir, list(kh.get("rmdir", [])))), \
                warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            return shutil.rmtree(duong, **kw)
    def ngu_gia(s):   # `ngat_ngu=(n, e)`: ném e ở lần ngủ thứ n (đã ghi lần ngủ ấy)
        ngu.append(s)
        if ngat_ngu is not None and len(ngu) - 1 == ngat_ngu[0]:
            raise ngat_ngu[1]
    ghi_that = m.ghi_tep

    def ghi_gia(*a, **k):   # `ngat_ghi=e`: ném e ở lần ghi tệp ĐẦU TIÊN
        if ngat_ghi is not None and not getattr(ghi_gia, "da", False):
            ghi_gia.da = True
            raise ngat_ghi
        return ghi_that(*a, **k)
    with tempfile.TemporaryDirectory() as thu, mock.patch.object(m, "_thay_the", gia), mock.patch.object(m, "_xoa_cay", xoa_gia), \
            mock.patch.object(m, "ngu_thu_lai", ngu_gia), mock.patch.object(m, "ghi_tep", ghi_gia), mock.patch.object(m, "LA_WINDOWS", windows), \
            mock.patch.object(m, "_DUNG_ONEXC", m._DUNG_ONEXC if onexc is None else onexc), contextlib.redirect_stderr(_StderrHong(None if stderr_hong is True else stderr_hong) if stderr_hong else io.StringIO()) as err:
        o = Path(thu) / "out"
        if co_cu:
            o.mkdir()   # bản trước có thể là thư mục RỖNG (review lượt 4 F2.l)
            for ten, b in (CU_BYTE if cu_cay is None else cu_cay).items():
                (o / ten).parent.mkdir(parents=True, exist_ok=True)
                (o / ten).write_bytes(b)
        for ten, dich in (lien_ket or {}).items():   # symlink NỘI CÂY (review lượt 4 F2.m): tạo trong bản trước, trỏ vào chính cây ấy
            os.symlink(dich, o / ten)
        try:
            m.ghi_nguyen_tu(o, dict(MOI_BYTE if moi is None else moi))
            loi = None
        except (BaseException if bat_moi else OSError) as e:   # `bat_moi`: bắt cả ngắt (KeyboardInterrupt/SystemExit) để đo hậu điều
            loi = e
        sot = {x.name: _doc_cay(x) for x in Path(thu).iterdir() if x.name != "out"}
        return {"loi": loi, "goi": goi, "ngu": ngu, "out": _doc_cay(o), "sot": sot, "xoa": goi_xoa,
                "err": "" if stderr_hong else err.getvalue()}

def _ten_sot(r):
    return sorted("cu" if k.endswith(".cu") else "tam" for k in r["sot"])

PE = lambda nhan="giả": PermissionError(13, nhan)  # noqa: E731

@ca
def c69_doi_ten_thu_lai_windows():   # #1475 A1–A5: thử lại có giới hạn, CHỈ PermissionError, CHỈ Windows, cho CẢ BA lời gọi đổi tên
    cho = [0.05 * 2 ** j for j in range(5)]
    for k in (1, 5):   # A1 (b): hỏng k lần rồi được; đọc BYTE (review lượt 1 F2.b)
        r = _ghi_voi_doi_ten_gia({"b": lambda i, k=k: PE() if i < k else None})
        bang(r["loi"] is None and r["goi"] == ["b"] * (k + 1) and r["ngu"] == cho[:k] and r["out"] == MOI_BYTE and r["sot"] == {},
             f"(b) hỏng {k} lần: {r}")
    for k in (1, 5):   # A1 (a)
        r = _ghi_voi_doi_ten_gia({"a": lambda i, k=k: PE() if i < k else None}, co_cu=True)
        bang(r["loi"] is None and r["goi"] == ["a"] * (k + 1) + ["b"] and r["ngu"] == cho[:k] and r["out"] == MOI_BYTE and r["sot"] == {},
             f"(a) hỏng {k} lần: {r}")
    hong = OSError(5, "EIO giả")   # A1 (c): (b) hỏng hẳn bằng lỗi KHÔNG thử lại, (c) hỏng k lần rồi trả được bản trước ĐÚNG BYTE
    for k in (1, 5):
        r = _ghi_voi_doi_ten_gia({"b": lambda i: hong, "c": lambda i, k=k: PE() if i < k else None}, co_cu=True)
        bang(r["loi"] is hong and r["goi"] == ["a", "b"] + ["c"] * (k + 1) and r["ngu"] == cho[:k] and r["out"] == CU_BYTE and r["sot"] == {},
             f"(c) hoàn tác hỏng {k} lần: {r}")
    for cho_hong, co_cu in (("b", False), ("b", True), ("a", True)):   # A2 + A3: hỏng mãi ⇒ 6 lời gọi, ném CHÍNH lỗi cuối, out vắng/giữ bản trước
        da_nem = []
        r = _ghi_voi_doi_ten_gia({cho_hong: lambda i: da_nem.append(PE(f"lần {i}")) or da_nem[-1]}, co_cu=co_cu)
        mong_goi = (["a"] if cho_hong == "b" and co_cu else []) + [cho_hong] * 6 + (["c"] if cho_hong == "b" and co_cu else [])
        bang(r["loi"] is da_nem[-1] and len(da_nem) == 6 and r["goi"] == mong_goi and r["ngu"] == cho
             and r["out"] == (CU_BYTE if co_cu else None) and r["sot"] == {},
             f"({cho_hong}) hỏng mãi, bản trước={co_cu}: {r} · ném {len(da_nem)}")
    da_nem = []   # (c) hết lượt (review lượt 1 F1.a + F2.c): ném lỗi cuối của (c), BẢN TRƯỚC giữ nguyên ở `.cu`, thư mục tạm ĐÃ dọn
    r = _ghi_voi_doi_ten_gia({"b": lambda i: hong, "c": lambda i: da_nem.append(PE(f"c {i}")) or da_nem[-1]}, co_cu=True)
    bang(r["loi"] is da_nem[-1] and len(da_nem) == 6 and r["goi"] == ["a", "b"] + ["c"] * 6 and r["ngu"] == cho and r["out"] is None
         and _ten_sot(r) == ["cu"] and list(r["sot"].values()) == [CU_BYTE], f"(c) hết lượt: {r}")
    for cho_hong, ke in (("b", {"b": lambda i: hong}), ("a", {"a": lambda i: hong})):   # A4: OSError khác ⇒ ném ngay, ở cả (a)
        r = _ghi_voi_doi_ten_gia(ke, co_cu=cho_hong == "a")
        bang(r["loi"] is hong and r["goi"] == [cho_hong] and r["ngu"] == [] and r["sot"] == {}, f"OSError khác ở ({cho_hong}): {r}")
    hong_c = OSError(5, "EIO giả ở (c)")   # A4 ở (c) (review lượt 2 F2.e): hoàn tác gặp lỗi khác ⇒ ném ngay, giữ bản trước ở `.cu`
    r = _ghi_voi_doi_ten_gia({"b": lambda i: hong, "c": lambda i: hong_c}, co_cu=True)
    bang(r["loi"] is hong_c and r["loi"].__context__ is hong and r["goi"] == ["a", "b", "c"] and r["ngu"] == [] and r["out"] is None
         and _ten_sot(r) == ["cu"] and list(r["sot"].values()) == [CU_BYTE], f"OSError khác ở (c): {r}")
    for ke, co_cu, mong in (({"b": lambda i: PE()}, False, ["b"]), ({"a": lambda i: PE()}, True, ["a"]),   # A5: không phải Windows
                            ({"b": lambda i: hong, "c": lambda i: PE()}, True, ["a", "b", "c"])):
        r = _ghi_voi_doi_ten_gia(ke, windows=False, co_cu=co_cu)
        bang(isinstance(r["loi"], OSError) and r["goi"] == mong and r["ngu"] == [], f"nền khác Windows {mong}: {r}")

@ca
def c70_mac_dinh_doi_ten_thu_lai():   # #1475 review lượt 1 F2.a: giá trị MẶC ĐỊNH (không tiêm đè); nền nạp qua `os` RIÊNG của mô-đun
    that = os

    class OsGia(types.ModuleType):
        def __getattr__(self, k):
            return getattr(that, k)
    for ten in ("nt", "posix"):
        gia = OsGia("os")
        gia.name = ten
        with mock.patch.dict(sys.modules, {"os": gia}):
            m = nap()
        bang(m.LA_WINDOWS is (ten == "nt"), f"os.name={ten!r} ⇒ LA_WINDOWS phải là {ten == 'nt'}, được {m.LA_WINDOWS!r}")
        import time as _time
        bang(m._thay_the is that.replace and m._xoa_cay is shutil.rmtree and m.ngu_thu_lai is _time.sleep
             and (m.SO_LAN_THU_LAI, m.CHO_GOC) == (5, 0.05),
             f"mặc định: _thay_the={m._thay_the!r} _xoa_cay={m._xoa_cay!r} ngu={m.ngu_thu_lai!r} {(m.SO_LAN_THU_LAI, m.CHO_GOC)}")

@ca
def c71_don_thu_muc_thu_lai():   # #1475 review lượt 1 F1.b/c + lượt 2 F1/F2.d/F3: dọn bằng rmtree THẬT, lỗi tiêm ở syscall
    cho, hong = [0.05 * 2 ** j for j in range(5)], OSError(5, "EIO giả")
    for onexc in sorted({False, sys.version_info >= (3, 12)}):   # cả hai nhánh callback của stdlib chạy được ở runtime này
        u1 = lambda i: {"unlink": [PE()]} if i < 1 else None  # noqa: E731 — unlink một tệp hỏng 1 lần ⇒ PermissionError + ENOTEMPTY
        r = _ghi_voi_doi_ten_gia({"b": lambda i: hong}, xoa={"tam": u1}, onexc=onexc)   # dọn tạm
        bang(r["loi"] is hong and r["xoa"] == ["tam", "tam"] and r["ngu"] == cho[:1] and r["sot"] == {} and "KHONG_DON_DUOC" not in r["err"],
             f"onexc={onexc} dọn tạm, unlink hỏng 1 lần: {r}")
        r = _ghi_voi_doi_ten_gia({}, co_cu=True, xoa={"cu": u1}, onexc=onexc)   # dọn bản trước sau commit
        bang(r["loi"] is None and r["out"] == MOI_BYTE and r["xoa"] == ["cu", "cu"] and r["ngu"] == cho[:1] and r["sot"] == {}
             and "KHONG_DON_DUOC" not in r["err"], f"onexc={onexc} dọn bản trước, unlink hỏng 1 lần: {r}")
        r = _ghi_voi_doi_ten_gia({}, co_cu=True, xoa={"cu": lambda i: {"rmdir": [PE()]} if i < 1 else None}, onexc=onexc)   # rmdir hỏng 1 lần
        bang(r["loi"] is None and r["out"] == MOI_BYTE and r["xoa"] == ["cu", "cu"] and r["ngu"] == cho[:1] and r["sot"] == {},
             f"onexc={onexc} dọn bản trước, rmdir hỏng 1 lần: {r}")
        r = _ghi_voi_doi_ten_gia({}, co_cu=True, xoa={"cu": lambda i: {"unlink": [PE()]}}, onexc=onexc)   # hỏng mãi: KHÔNG ném, BÁO
        bang(r["loi"] is None and r["out"] == MOI_BYTE and r["xoa"] == ["cu"] * 6 and r["ngu"] == cho and _ten_sot(r) == ["cu"]
             and "KHONG_DON_DUOC" in r["err"], f"onexc={onexc} dọn bản trước hỏng mãi: {r}")
        for ten, kh, kw in (("lỗi khác", {"unlink": [hong]}, {}), ("nền khác", {"unlink": [PE()]}, {"windows": False}),
                            ("PermissionError + EIO độc lập", {"unlink": [PE(), hong]}, {})):   # không thử lại, vẫn BÁO, giữ lỗi gốc
            r = _ghi_voi_doi_ten_gia({"b": lambda i: hong}, xoa={"tam": lambda i, kh=kh: kh if i < 1 else None}, onexc=onexc, **kw)
            bang(r["loi"] is hong and r["xoa"] == ["tam"] and r["ngu"] == [] and _ten_sot(r) == ["tam"] and "KHONG_DON_DUOC" in r["err"],
                 f"onexc={onexc} dọn tạm, {ten}: {r}")
    hong_c = []   # F3: stderr hỏng KHÔNG đổi kết quả ghi, KHÔNG thay lỗi đang ném (đúng đối tượng) ở cả ba đường
    for ten, ke, xoa, co_cu, mong_loi, mong_out in (
            ("thành công", {}, {"cu": lambda i: {"unlink": [PE()]}}, True, lambda: None, MOI_BYTE),
            ("(b) hỏng, (c) trả lại", {"b": lambda i: hong}, {"tam": lambda i: {"unlink": [hong]}}, True, lambda: hong, CU_BYTE),
            ("(c) hết lượt", {"b": lambda i: hong, "c": lambda i: hong_c.append(PE(f"c {i}")) or hong_c[-1]},
             {"tam": lambda i: {"unlink": [hong]}}, True, lambda: hong_c[-1], None)):
        r = _ghi_voi_doi_ten_gia(ke, xoa=xoa, co_cu=co_cu, stderr_hong=True)
        bang(r["loi"] is mong_loi() and r["out"] == mong_out, f"stderr hỏng, {ten}: {r}")

_CAY_C72 = {"phang": ("x", "y"), "long1": ("d/x", "y"), "long2": ("a/x", "b/y"), "sau": ("a/b/x", "c/y"),
            "trung_ten": ("a/x", "b/x"), "ba_tep": ("a/x", "b/y", "c/z"), "rong": ()}
_PE6 = ("PE",) * 6
_LOI_C72 = ({}, {"x": ("PE",)}, {"x": _PE6}, {"x": ("EIO",)}, {"x": ("PE",), "y": ("PE",)}, {"x": ("PE",), "y": ("EIO",)},
            {"x": _PE6, "y": ("PE",)}, {"x": ("PE", "EIO")}, {"x": ("PE", "PE"), "y": ("PE", "EIO")}, {"x": ("PE",), "y": ("PE",), "z": ("PE",)},
            {"@d": ("PE",)}, {"@a": ("PE",)}, {"@a": _PE6})

def _mong_don_c72(tep, ke, windows):
    """Hậu điều dọn dẹp TÍNH TỪ ĐẶC TẢ (mô phỏng từng lần dọn, không đọc mã): mỗi lần, mỗi nút còn lại có kế hoạch ở lần ấy thì
    hỏng với LOẠI ấy, còn lại bị xoá. Thử lại ⇔ Windows, lần ấy có PE và không có lỗi khác (ENOTEMPTY của thư mục cha không phải lỗi
    khác), tối đa 6 lần. Trả (số lần dọn, dãy ngủ, tệp còn sót, có thư mục sót)."""
    nut = {k: k.rsplit("/", 1)[-1] for k in tep} | {f"@{d}": "@" + d.rsplit("/", 1)[-1] for k in tep for d in
                                                     ["/".join(k.split("/")[:i]) for i in range(1, k.count("/") + 1)]}
    con, ngu = set(nut), []
    for i in range(6):
        hong = {n: ke[nut[n]][i] for n in con if nut[n] in ke and i < len(ke[nut[n]])}
        con = set(hong) | {n for n in con if n.startswith("@") and any(h.startswith(n[1:] + "/") for h in hong)}
        if not hong:
            return i + 1, ngu, set(), False
        if not windows or "EIO" in hong.values() or i == 5:
            return i + 1, ngu, {n for n in hong if not n.startswith("@")}, True
        ngu.append(0.05 * 2 ** i)

@ca
def c72_ma_tran_don_dep():   # #1475 sổ uỷ quyền 7059117700 + lần xét lại thứ hai: ma trận hậu điều, luật chỉ đọc LOẠI lỗi
    hong = OSError(5, "EIO giả")
    loai = {"PE": lambda: PE(), "EIO": lambda: OSError(5, "EIO tệp")}
    so_o, nhanh = 0, sorted({False, sys.version_info >= (3, 12)})
    for onexc in nhanh:
        for ten_cay, tep in _CAY_C72.items():
            cay = {k: k.encode() for k in tep}
            for ke in _LOI_C72:
                for windows in (True, False):
                    n, ngu, sot_tep, co_sot = _mong_don_c72(tep, ke, windows)
                    theo_ten = {"theo_ten": {k: (lambda i, v=v: loai[v[i]]() if i < len(v) else None) for k, v in ke.items()}}
                    for cho in ("tam", "cu"):
                        if cho == "tam":   # dọn thư mục tạm sau (b) hỏng
                            r = _ghi_voi_doi_ten_gia({"b": lambda i: hong}, windows=windows, onexc=onexc, moi=cay,
                                                     xoa={"tam": lambda i, x=theo_ten: x})
                            dung_ket_qua = r["loi"] is hong and r["out"] is None
                        else:   # dọn bản trước sau commit
                            r = _ghi_voi_doi_ten_gia({}, windows=windows, onexc=onexc, co_cu=True, cu_cay=cay,
                                                     xoa={"cu": lambda i, x=theo_ten: x})
                            dung_ket_qua = r["loi"] is None and r["out"] == MOI_BYTE
                        con = {k: v for d in r["sot"].values() for k, v in d.items()}
                        bang(dung_ket_qua and r["xoa"] == [cho] * n and r["ngu"] == ngu
                             and _ten_sot(r) == ([cho] if co_sot else []) and con == {k: cay[k] for k in sot_tep}
                             and ("KHONG_DON_DUOC" in r["err"]) == co_sot,
                             f"onexc={onexc} cây={ten_cay} lỗi={ke} windows={windows} dọn={cho}: mong {n} lần, ngủ {ngu}, "
                             f"sót {sorted(sot_tep)}/{co_sot}; được {r}")
                        so_o += 1
    bang(so_o == len(_CAY_C72) * len(_LOI_C72) * 4 * len(nhanh), f"số ô ma trận: {so_o}")
    with tempfile.TemporaryDirectory() as thu:   # Windows không có quyền tạo symlink (không Developer Mode) ⇒ KHÔNG ĐO ĐƯỢC phần này
        try:
            os.symlink(thu, Path(thu) / "thu")
            co_symlink = True
        except OSError:
            co_symlink = False
    bang(co_symlink or os.name == "nt", "nền không phải Windows mà không tạo được symlink: không được bỏ qua phần symlink")
    if not co_symlink:
        print("BO QUA c72 symlink noi cay: Windows khong co quyen tao symlink — KHONG DO DUOC", file=sys.stderr)
    for windows in ((True, False) if co_symlink else ()):   # symlink NỘI CÂY (F2.m): unlink link hỏng 1 lần — link là một nút như tệp
        r = _ghi_voi_doi_ten_gia({}, windows=windows, co_cu=True, cu_cay={"dich/k": b"k"}, lien_ket={"lk": "dich"},
                                 xoa={"cu": lambda i: {"theo_ten": {"lk": lambda j: PE() if j < 1 else None}}})
        bang(r["loi"] is None and r["out"] == MOI_BYTE and r["xoa"] == ["cu"] * (2 if windows else 1)
             and _ten_sot(r) == ([] if windows else ["cu"]), f"symlink nội cây windows={windows}: {r}")
    for loi in (OSError(28, "giả"), ValueError("giả"), KeyboardInterrupt(), SystemExit(7)):   # ranh giới báo cáo (lượt 3 F2.g)
        bat = None
        try:
            r = _ghi_voi_doi_ten_gia({}, co_cu=True, xoa={"cu": lambda i: {"unlink": [PE()]}}, stderr_hong=loi)
        except BaseException as e:
            bat = e
        if isinstance(loi, Exception):
            bang(bat is None and r["loi"] is None and r["out"] == MOI_BYTE, f"stream ném {loi!r}: phải cô lập, được bat={bat!r}")
        else:
            bang(bat is loi, f"stream ném {loi!r}: BaseException phải đi qua đúng đối tượng, được {bat!r}")

_TAP_LOAI = [frozenset(t for t, b in zip(("PE", "ENOTEMPTY", "khac"), (i & 1, i & 2, i & 4)) if b) for i in range(8)]

def _mong_c73(lich, windows):
    """Hậu điều TÍNH TỪ LUẬT ĐÃ DUYỆT (sổ 7060197691), không đọc mã: lần k có tập loại S; S rỗng ⇒ sạch; thử lại ⇔ Windows ∧ PE ∈ S
    ∧ khac ∉ S, tối đa 6 lần. Trả (số lần dọn, dãy ngủ, sạch?)."""
    ngu = []
    for k in range(6):
        s = lich[k] if k < len(lich) else frozenset()
        if not s:
            return k + 1, ngu, True
        if not (windows and "PE" in s and "khac" not in s) or k == 5:
            return k + 1, ngu, False
        ngu.append(0.05 * 2 ** k)

@ca
def c73_bang_chan_tri_loai_loi():   # #1475 review lượt 5 F2.n: TOÀN BỘ bảng chân trị của luật tập loại (miền hữu hạn), không lấy mẫu
    m = nap()
    dai_dien = {"PE": (lambda: OSError(errno.EACCES, "PE giả"), lambda: OSError(errno.EPERM, "PE giả")),
                "ENOTEMPTY": (lambda: OSError(errno.ENOTEMPTY, "ENOTEMPTY giả"),),
                "khac": (lambda: OSError(errno.EIO, "EIO giả"), lambda: OSError(errno.ENOSPC, "ENOSPC giả"))}
    lich_ds = ([(s,) for s in _TAP_LOAI] + [(s,) * 6 for s in _TAP_LOAI]
               + [(s0, s1) for s0 in _TAP_LOAI for s1 in _TAP_LOAI])   # một lần · kéo dài · mọi chuyển tiếp hai bước
    so_o, nhanh = 0, sorted({False, sys.version_info >= (3, 12)})
    for lich in lich_ds:
        for windows in (True, False):
            n, ngu_mong, sach = _mong_c73(lich, windows)
            for bien in range(2):   # đại diện thứ `bien` của mỗi loại (EACCES/EPERM · EIO/ENOSPC)
                for onexc in nhanh:
                    goi, ngu = [], []

                    def xoa_gia(p, onexc=None, onerror=None):
                        k = len(goi)
                        goi.append(k)
                        s = lich[k] if k < len(lich) else frozenset()
                        for t in sorted(s):
                            e = dai_dien[t][bien % len(dai_dien[t])]()
                            if onexc is not None:
                                onexc(os.unlink, f"{p}/{t}", e)
                            else:
                                onerror(os.unlink, f"{p}/{t}", (type(e), e, None))
                        if not s:
                            shutil.rmtree(p)
                    with tempfile.TemporaryDirectory() as thu, mock.patch.object(m, "_xoa_cay", xoa_gia), \
                            mock.patch.object(m, "ngu_thu_lai", ngu.append), mock.patch.object(m, "LA_WINDOWS", windows), \
                            mock.patch.object(m, "_DUNG_ONEXC", onexc), contextlib.redirect_stderr(io.StringIO()) as err:
                        p = Path(thu) / "d"
                        p.mkdir()
                        kq = m.don_thu_muc(p)
                        bang(kq is sach and len(goi) == n and ngu == ngu_mong and p.exists() is not sach
                             and ("KHONG_DON_DUOC" in err.getvalue()) is not sach,
                             f"lịch={[sorted(s) for s in lich]} windows={windows} biến={bien} onexc={onexc}: mong ({n}, {ngu_mong}, "
                             f"{sach}); được ({kq}, {len(goi)}, {ngu}, còn={p.exists()})")
                    so_o += 1
    bang(so_o == len(lich_ds) * 2 * 2 * len(nhanh), f"số ô bảng chân trị: {so_o}")
    for onexc in nhanh:   # cầu nối rmtree THẬT: tập loại sinh bởi stdlib khớp mô hình callback ở hai tập review lượt 5 tìm ra
        r = _ghi_voi_doi_ten_gia({}, windows=True, onexc=onexc, co_cu=True, cu_cay={"d/x": b"x"},   # chỉ ENOTEMPTY, không PE
                                 xoa={"cu": lambda i: {"theo_ten": {"@d": lambda j: OSError(errno.ENOTEMPTY, "giả") if j < 1 else None}}})
        bang(r["loi"] is None and r["out"] == MOI_BYTE and r["xoa"] == ["cu"] and r["ngu"] == [] and _ten_sot(r) == ["cu"],
             f"onexc={onexc} rmdir chỉ ENOTEMPTY: phải dừng sau 1 lần, không ngủ; được {r}")
        r = _ghi_voi_doi_ten_gia({}, windows=True, onexc=onexc, co_cu=True, cu_cay={"x": b"x", "y": b"y"},   # PE + ENOSPC
                                 xoa={"cu": lambda i: {"theo_ten": {"x": lambda j: PE() if j < 1 else None,
                                                                    "y": lambda j: OSError(errno.ENOSPC, "giả") if j < 1 else None}}})
        con = {k: v for d in r["sot"].values() for k, v in d.items()}
        bang(r["loi"] is None and r["xoa"] == ["cu"] and r["ngu"] == [] and con == {"x": b"x", "y": b"y"},
             f"onexc={onexc} PE + ENOSPC: ENOSPC là lỗi khác, phải dừng sau 1 lần; được {r}")

class _PEcon(PermissionError):
    pass

class _OSErrorCon(OSError):
    pass

class _KhacCoErrno(ValueError):
    def __init__(self, so):
        super().__init__("không phải OSError, có errno")
        self.errno = so

def _loi_kieu_errno(cls, so):
    """Đối tượng đúng KIỂU `cls` (không để OSError tự đổi kiểu theo errno) mang errno `so` (None = không errno)."""
    e = cls("giả")
    if so is not None:
        e.errno = so
    return e

_KIEU_C76 = (("PermissionError", PermissionError), ("lớp con PermissionError", _PEcon),
             ("lớp con OSError", _OSErrorCon), ("OSError", OSError))
_ERRNO_C76 = (("không errno", None), ("EACCES", errno.EACCES), ("EPERM", errno.EPERM), ("ENOTEMPTY", errno.ENOTEMPTY), ("EIO", errno.EIO))
_NHAN_DON_C76 = """\
PermissionError         | không errno PE | EACCES PE   | EPERM PE   | ENOTEMPTY PE        | EIO PE
lớp con PermissionError | không errno PE | EACCES PE   | EPERM PE   | ENOTEMPTY PE        | EIO PE
lớp con OSError         | không errno khac | EACCES khac | EPERM khac | ENOTEMPTY ENOTEMPTY | EIO khac
OSError                 | không errno khac | EACCES khac | EPERM khac | ENOTEMPTY ENOTEMPTY | EIO khac
"""   # nhãn DỌN viết tay theo luật đã duyệt: kiểu PE ⇒ PE (mọi errno); không phải PE mà errno ENOTEMPTY ⇒ ENOTEMPTY; còn lại khac
_NHAN_DOI_TEN_C76 = {"PermissionError": "PE", "lớp con PermissionError": "PE", "lớp con OSError": "khac", "OSError": "khac"}   # SPEC M1/M2: theo KIỂU

def _bang_c76(nhan_cua):
    """Tích ĐỦ kiểu × errno (review lượt 8 F2.r): mọi giao kiểu/errno đều có một dòng, nhãn lấy từ bảng viết tay `nhan_cua`."""
    return tuple((f"{tk} errno={te}", (lambda c=c, s=s: _loi_kieu_errno(c, s)), nhan_cua(tk, te)) for tk, c in _KIEU_C76 for te, s in _ERRNO_C76)

def _nhan_don_c76(tk, te):
    dong = {d.split("|")[0].strip(): d.split("|")[1:] for d in _NHAN_DON_C76.splitlines()}[tk]
    o = [x.strip() for x in dong if x.strip().startswith(te + " ")]
    assert len(o) == 1, (tk, te)
    return o[0].rsplit(" ", 1)[1]

def _kieu_oserror_du():
    """MỌI lớp con OSError dựng sẵn của runtime (duyệt `__subclasses__`, không liệt kê tay) + OSError + hai lớp con tự định nghĩa
    (review lượt 9 F2.s: danh mục âm phải là TOÀN BỘ, không phải vài đại diện)."""
    def con(c):
        for s in c.__subclasses__():
            yield s
            yield from con(s)
    dung_san = {c.__name__: c for c in con(OSError) if getattr(builtins, c.__name__, None) is c}
    return [("OSError", OSError)] + sorted(dung_san.items()) + [("_PEcon", _PEcon), ("_OSErrorCon", _OSErrorCon)]

_KIEU_PE_DU = frozenset({"PermissionError", "_PEcon"})   # viết tay: CHỈ hai kiểu này là PermissionError (SPEC M1)

def _bang_du():
    """Tích TOÀN BỘ kiểu × (không errno + MỌI errno của runtime). Nhãn: đổi tên theo KIỂU (`_KIEU_PE_DU`); dọn theo luật đã duyệt
    (kiểu PE ⇒ PE; không phải PE mà errno ENOTEMPTY ⇒ ENOTEMPTY; còn lại khac)."""
    for tk, c in _kieu_oserror_du():
        for so in [None] + sorted(errno.errorcode):
            dt = "PE" if tk in _KIEU_PE_DU else "khac"
            dd = "PE" if tk in _KIEU_PE_DU else ("ENOTEMPTY" if so == errno.ENOTEMPTY else "khac")
            yield f"{tk} errno={so}", (lambda c=c, so=so: _loi_kieu_errno(c, so)), dt, dd

_PHAN_LOAI_C74 = (   # (đối tượng lỗi, NHÃN KỲ VỌNG viết tay — không suy bằng isinstance/getattr của bộ phân loại)
    ("PermissionError(EACCES)", lambda: OSError(errno.EACCES, "giả"), "PE"),
    ("lớp con PermissionError", lambda: _PEcon(errno.EACCES, "giả"), "PE"),
    ("PermissionError không errno", lambda: PermissionError("giả"), "PE"),
    ("PermissionError errno ENOTEMPTY", lambda: PermissionError(errno.ENOTEMPTY, "giả"), "PE"),
    ("OSError(ENOTEMPTY)", lambda: OSError(errno.ENOTEMPTY, "giả"), "ENOTEMPTY"),
    ("lớp con OSError ENOTEMPTY", lambda: _OSErrorCon(errno.ENOTEMPTY, "giả"), "ENOTEMPTY"),
    ("lớp con OSError EACCES (không phải PE)", lambda: _OSErrorCon(errno.EACCES, "giả"), "khac"),
    ("OSError(EIO)", lambda: OSError(errno.EIO, "giả"), "khac"),
    ("FileNotFoundError", lambda: FileNotFoundError(errno.ENOENT, "giả"), "khac"),
    ("ValueError", lambda: ValueError("giả"), "khac"),
    ("không phải OSError, errno ENOTEMPTY", lambda: _KhacCoErrno(errno.ENOTEMPTY), "khac"),
    ("không phải OSError, errno EACCES", lambda: _KhacCoErrno(errno.EACCES), "khac"),
)

@ca
def c74_phan_loai_doi_tuong_loi():   # #1475 review lượt 6 F2.o: ranh giới kiểu/lớp con/errno của bước ánh xạ lỗi → loại
    m = nap()
    nhanh, so_o = sorted({False, sys.version_info >= (3, 12)}), 0
    for ten, tao, nhan in _PHAN_LOAI_C74 + _bang_c76(_nhan_don_c76):
        for kem_pe in (False, True):   # một mình: chỉ PE mới thử lại · kèm PE: PE/ENOTEMPTY thử lại, khac dừng
            s = frozenset({nhan, "PE"} if kem_pe else {nhan})
            for windows in (True, False):
                n, ngu_mong, sach = _mong_c73((s,), windows)
                for onexc in nhanh:
                    goi, ngu = [], []

                    def xoa_gia(p, onexc=None, onerror=None):
                        goi.append(1)
                        if len(goi) > 1:
                            return shutil.rmtree(p)
                        for e in ([tao()] + ([OSError(errno.EACCES, "PE kèm")] if kem_pe else [])):
                            if onexc is not None:
                                onexc(os.unlink, f"{p}/x", e)
                            else:
                                onerror(os.unlink, f"{p}/x", (type(e), e, None))
                    with tempfile.TemporaryDirectory() as thu, mock.patch.object(m, "_xoa_cay", xoa_gia), \
                            mock.patch.object(m, "ngu_thu_lai", ngu.append), mock.patch.object(m, "LA_WINDOWS", windows), \
                            mock.patch.object(m, "_DUNG_ONEXC", onexc), contextlib.redirect_stderr(io.StringIO()) as err:
                        p = Path(thu) / "d"
                        p.mkdir()
                        kq = m.don_thu_muc(p)
                        bang(kq is sach and len(goi) == n and ngu == ngu_mong and ("KHONG_DON_DUOC" in err.getvalue()) is not sach,
                             f"{ten} (nhãn {nhan}) kèm_PE={kem_pe} windows={windows} onexc={onexc}: mong ({n}, {ngu_mong}, {sach}); "
                             f"được ({kq}, {len(goi)}, {ngu})")
                    so_o += 1
    bang(so_o == (len(_PHAN_LOAI_C74) + 20) * 2 * 2 * len(nhanh), f"số ô: {so_o}")
    ten_kieu = [tk for tk, _ in _kieu_oserror_du()]   # danh mục TOÀN BỘ: chỉ chạy ở cấu hình phân biệt được (Windows tiêm)
    bang(len(ten_kieu) >= 17 and {"InterruptedError", "BlockingIOError", "PermissionError", "FileNotFoundError"} <= set(ten_kieu),
         f"danh mục kiểu OSError dựng sẵn thiếu: {ten_kieu}")
    so_du, trang = 0, {}   # danh mục ĐỦ ở MỌI vị trí retry (review lượt 10 F2.t): j lần {PE} rồi lỗi đang xét, j = 0..5
    def xoa_du(p, onexc=None, onerror=None):
        k = trang["k"]
        trang["k"] += 1
        loi = [OSError(errno.EACCES, "PE trước")] if k < trang["j"] else (trang["loi"] if k == trang["j"] else None)
        if loi is None:
            return os.rmdir(p)
        for e in loi:
            (onexc(os.unlink, f"{p}/x", e) if onexc is not None else onerror(os.unlink, f"{p}/x", (type(e), e, None)))
    ngu = []
    with tempfile.TemporaryDirectory() as thu, mock.patch.object(m, "_xoa_cay", xoa_du), mock.patch.object(m, "ngu_thu_lai", ngu.append), \
            mock.patch.object(m, "LA_WINDOWS", True), contextlib.redirect_stderr(io.StringIO()):
        p = Path(thu) / "d"
        for ten, tao, _, nhan in _bang_du():
            for j in range(6):
                for kem_pe in (False, True):
                    lich = (frozenset({"PE"}),) * j + (frozenset({nhan, "PE"} if kem_pe else {nhan}),)
                    n, ngu_mong, sach = _mong_c73(lich, True)
                    if p.exists():
                        os.rmdir(p)
                    p.mkdir()
                    trang.update(k=0, j=j, loi=[tao()] + ([OSError(errno.EACCES, "PE kèm")] if kem_pe else []))
                    del ngu[:]
                    kq = m.don_thu_muc(p)
                    bang(kq is sach and trang["k"] == n and ngu == ngu_mong,
                         f"danh mục đủ: {ten} (nhãn dọn {nhan}) sau {j} lần PE, kèm_PE={kem_pe}: mong ({n}, {ngu_mong}, {sach}); "
                         f"được ({kq}, {trang['k']}, {ngu})")
                    so_du += 1
    bang(so_du == len(ten_kieu) * (len(errno.errorcode) + 1) * 6 * 2, f"số ô danh mục đủ: {so_du}")
    cau = ((lambda: {"x": lambda j: _PEcon(errno.EACCES, "giả") if j < 1 else None}, 2),   # cầu nối rmtree THẬT
           (lambda: {"x": lambda j: _OSErrorCon(errno.EACCES, "giả") if j < 1 else None}, 1),
           (lambda: {"x": lambda j: PE() if j < 1 else None, "@d": lambda j: _OSErrorCon(errno.ENOTEMPTY, "giả") if j < 1 else None}, 2))
    for onexc in nhanh:
        for i, (kh, n) in enumerate(cau):
            r = _ghi_voi_doi_ten_gia({}, windows=True, onexc=onexc, co_cu=True, cu_cay={"d/x": b"x"},
                                     xoa={"cu": lambda j, kh=kh: {"theo_ten": kh()}})
            con = {k: v for d in r["sot"].values() for k, v in d.items()}
            bang(r["loi"] is None and r["out"] == MOI_BYTE and r["xoa"] == ["cu"] * n and r["ngu"] == [0.05] * (n - 1)
                 and con == ({} if n == 2 else {"d/x": b"x"}), f"cầu nối {i} onexc={onexc}: mong {n} lần; được {r}")

_DOI_TEN_C75 = (   # (đối tượng lỗi của os.replace, NHÃN viết tay: chỉ PermissionError — mọi lớp con, mọi errno — mới thử lại)
    ("PermissionError(EACCES)", lambda: OSError(errno.EACCES, "giả"), "PE"),
    ("PermissionError(EPERM)", lambda: OSError(errno.EPERM, "giả"), "PE"),
    ("lớp con PermissionError", lambda: _PEcon(errno.EACCES, "giả"), "PE"),
    ("PermissionError không errno", lambda: PermissionError("giả"), "PE"),
    ("lớp con OSError EACCES (không phải PE)", lambda: _OSErrorCon(errno.EACCES, "giả"), "khac"),
    ("OSError(EIO)", lambda: OSError(errno.EIO, "giả"), "khac"),
    ("OSError(ENOTEMPTY)", lambda: OSError(errno.ENOTEMPTY, "giả"), "khac"),
    ("FileNotFoundError", lambda: FileNotFoundError(errno.ENOENT, "giả"), "khac"),
)

def _mong_doi_ten(nhan, windows):
    """Hậu điều đổi tên TÍNH TỪ SPEC M1/M2: lần k mang nhãn nhan[k] (None = thành công). PE trên Windows ⇒ ngủ rồi thử lại, tối đa
    6 lời gọi; khác ⇒ ném ngay đúng lỗi lần ấy. Trả (số lời gọi, dãy ngủ, chỉ số lỗi bị ném hay None)."""
    ngu = []
    for k in range(6):
        if k >= len(nhan) or nhan[k] is None:
            return k + 1, ngu, None
        if not (windows and nhan[k] == "PE") or k == 5:
            return k + 1, ngu, k
        ngu.append(0.05 * 2 ** k)

@ca
def c75_doi_ten_va_ngat():   # #1475 review lượt 7: F2.p phân hoạch/chuyển tiếp lỗi ĐỔI TÊN · F2.q dọn tạm khi bị ngắt (BaseException)
    pe0 = _DOI_TEN_C75[0]
    so_o = 0
    for ten, tao, nhan in _DOI_TEN_C75 + _bang_c76(lambda tk, te: _NHAN_DOI_TEN_C76[tk]):
        for kieu, lich in (("một lần", ((ten, tao, nhan),)), ("kéo dài", ((ten, tao, nhan),) * 6), ("PE rồi lỗi này", (pe0, (ten, tao, nhan)))):
            for windows in (True, False):
                n, ngu, k_nem = _mong_doi_ten([x[2] for x in lich], windows)
                for cho in ("a", "b", "c"):
                    da_tao, hong_b = [], OSError(errno.EIO, "b hỏng hẳn")

                    def ke(i, lich=lich, da_tao=da_tao):
                        if i >= len(lich):
                            return None
                        e = lich[i][1]()
                        da_tao.append(e)
                        return e
                    kh = {cho: ke} if cho != "c" else {"b": lambda i: hong_b, "c": ke}
                    r = _ghi_voi_doi_ten_gia(kh, windows=windows, co_cu=True)
                    mo_ta = f"{ten} [{kieu}] windows={windows} chỗ={cho}: mong {n} lời gọi, ngủ {ngu}, ném #{k_nem}; được {r}"
                    bang(r["goi"].count(cho) == n and r["ngu"] == ngu, mo_ta)
                    if cho == "c":   # (b) hỏng hẳn ⇒ hoàn tác (c): thành công ⇒ ném lỗi (b), bản trước về chỗ; hỏng ⇒ ném lỗi (c), giữ .cu
                        mong_loi = hong_b if k_nem is None else da_tao[k_nem]
                        bang(r["loi"] is mong_loi and r["out"] == (CU_BYTE if k_nem is None else None)
                             and _ten_sot(r) == ([] if k_nem is None else ["cu"]), mo_ta)
                    else:
                        mong_loi = None if k_nem is None else da_tao[k_nem]
                        bang(r["loi"] is mong_loi and r["out"] == (MOI_BYTE if k_nem is None else CU_BYTE) and _ten_sot(r) == [], mo_ta)
                    so_o += 1
    bang(so_o == (len(_DOI_TEN_C75) + 20) * 3 * 2 * 3, f"số ô đổi tên: {so_o}")
    so_du = 0   # TÍCH HỢP qua ghi_nguyen_tu: canh rollback + dọn tạm cho MỌI kiểu lỗi (review lượt 11 F2.u — không được bỏ khối này)
    for ten, tao, nhan, _ in _bang_du():   # danh mục TOÀN BỘ ở (b), Windows tiêm, lỗi một lần rồi thành công (review lượt 9 F2.s)
        da = []
        r = _ghi_voi_doi_ten_gia({"b": lambda i, da=da, tao=tao: (da.append(tao()) or da[-1]) if i == 0 else None}, windows=True, co_cu=True)
        if nhan == "PE":
            ok = r["goi"].count("b") == 2 and r["ngu"] == [0.05] and r["loi"] is None and r["out"] == MOI_BYTE
        else:
            ok = r["goi"].count("b") == 1 and r["ngu"] == [] and r["loi"] is da[0] and r["out"] == CU_BYTE
        bang(ok and _ten_sot(r) == [], f"danh mục đủ đổi tên: {ten} (nhãn {nhan}): được {r}")
        so_du += 1
    bang(so_du == len(_kieu_oserror_du()) * (len(errno.errorcode) + 1), f"số ô danh mục đủ đổi tên (tích hợp): {so_du}")
    m, so_du, trang, ngu = nap(), 0, {}, []   # danh mục ĐỦ ở MỌI vị trí retry (review lượt 10 F2.t): j lần PE rồi lỗi đang xét

    def thay(nguon, dich):
        k = trang["k"]
        trang["k"] += 1
        if k < trang["j"] or k == trang["j"]:
            e = OSError(errno.EACCES, "PE trước") if k < trang["j"] else trang["tao"]()
            trang["da"].append(e)
            raise e
    with mock.patch.object(m, "_thay_the", thay), mock.patch.object(m, "ngu_thu_lai", ngu.append), mock.patch.object(m, "LA_WINDOWS", True):
        for ten, tao, nhan, _ in _bang_du():
            for j in range(6):
                n, ngu_mong, k_nem = _mong_doi_ten(["PE"] * j + [nhan], True)
                trang.update(k=0, j=j, tao=tao, da=[])
                del ngu[:]
                try:
                    m.doi_ten_thu_lai("nguon", "dich")
                    loi = None
                except OSError as e:
                    loi = e
                bang(trang["k"] == n and ngu == ngu_mong and (loi is None if k_nem is None else loi is trang["da"][k_nem]),
                     f"danh mục đủ đổi tên: {ten} (nhãn {nhan}) sau {j} lần PE: mong ({n}, {ngu_mong}, ném #{k_nem}); "
                     f"được ({trang['k']}, {ngu}, {loi!r})")
                so_du += 1
    bang(so_du == len(_kieu_oserror_du()) * (len(errno.errorcode) + 1) * 6, f"số ô danh mục đủ đổi tên: {so_du}")
    for ngat in (lambda: KeyboardInterrupt(), lambda: SystemExit(7)):   # F2.q: ngắt giữa (a)/(b) ⇒ ném lại ĐÚNG đối tượng, dọn tạm
        for cho, co_cu in (("a", True), ("b", True), ("b", False)):
            for windows in (True, False):
                e = ngat()
                r = _ghi_voi_doi_ten_gia({cho: lambda i, e=e: e if i == 0 else None}, windows=windows, co_cu=co_cu, bat_moi=True)
                bang(r["loi"] is e and r["goi"].count(cho) == 1 and r["ngu"] == []
                     and r["out"] == (CU_BYTE if co_cu else None) and _ten_sot(r) == [],
                     f"ngắt {e!r} ở ({cho}) co_cu={co_cu} windows={windows}: phải ném lại đúng đối tượng, giữ bản trước, dọn tạm; được {r}")
    m = nap()   # tiêu chí "sạch" là CÂY ĐÃ VẮNG, không phải "không có callback lỗi" (review lượt 7 U9): lỗi báo về mà cây vẫn mất ⇒ sạch
    for onexc in sorted({False, sys.version_info >= (3, 12)}):
        goi, ngu = [], []

        def xoa_mat(p, onexc=None, onerror=None):
            goi.append(1)
            e = OSError(errno.EACCES, "giả")
            (onexc(os.unlink, f"{p}/x", e) if onexc is not None else onerror(os.unlink, f"{p}/x", (type(e), e, None)))
            shutil.rmtree(p, ignore_errors=True)   # lần gọi sau (nếu đột biến thử lại) gặp cây đã vắng
        with tempfile.TemporaryDirectory() as thu, mock.patch.object(m, "_xoa_cay", xoa_mat), mock.patch.object(m, "ngu_thu_lai", ngu.append), \
                mock.patch.object(m, "LA_WINDOWS", True), mock.patch.object(m, "_DUNG_ONEXC", onexc), contextlib.redirect_stderr(io.StringIO()) as err:
            (Path(thu) / "d").mkdir()
            kq = m.don_thu_muc(Path(thu) / "d")
            bang(kq is True and len(goi) == 1 and ngu == [] and "KHONG_DON_DUOC" not in err.getvalue(),
                 f"onexc={onexc} có callback lỗi nhưng cây đã vắng: mong (True, 1 lần, không ngủ, không báo); được ({kq}, {len(goi)}, {ngu})")

@ca
def c76_ngat_moi_diem():   # #1475 review lượt 12 F2.v: ngoại lệ không phải OSError (ngắt, GeneratorExit, ValueError) ở MỌI điểm của ghi_nguyen_tu
    """Mỗi điểm ngắt: ném lại ĐÚNG đối tượng ngắt; `out` và phần sót đúng như bảng dưới (viết tay theo M3, không suy từ mã):
    ghi tệp / (a) / ngủ ở (a) ⇒ out giữ bản trước (hoặc vắng), không sót · (b) / ngủ ở (b) ⇒ hoàn tác, out giữ bản trước (hoặc vắng),
    không sót · (c) / ngủ ở (c) (khi (b) hỏng hẳn) ⇒ out vắng, GIỮ .cu, tam đã dọn · dọn tạm bị ngắt ⇒ ngắt thay lỗi (b), out đã hoàn
    tác, sót tam · dọn bản trước bị ngắt / ngủ trong lúc dọn bản trước ⇒ out mới, sót .cu."""
    eio, so_o = (lambda: OSError(errno.EIO, "b hỏng hẳn")), 0
    for ngat in (lambda: KeyboardInterrupt(), lambda: SystemExit(7), lambda: GeneratorExit(), lambda: ValueError("vd: tên tệp có NUL")):
        for windows in (True, False):
            dsj = (0, 1, 5) if windows else (0,)
            ca_ds = []
            for co_cu in (True, False):
                ca_ds.append(("ghi tệp", co_cu, lambda e: dict(ngat_ghi=e), [], [], CU_BYTE if co_cu else None, []))
            for j in dsj:
                ca_ds.append((f"(a) sau {j} PE", True, lambda e, j=j: dict(ke_hoach={"a": lambda i: PE() if i < j else (e if i == j else None)}),
                              ["a"] * (j + 1), [0.05 * 2 ** k for k in range(j)], CU_BYTE, []))
                for co_cu in (True, False):
                    ca_ds.append((f"(b) sau {j} PE", co_cu, lambda e, j=j: dict(ke_hoach={"b": lambda i: PE() if i < j else (e if i == j else None)}),
                                  None, [0.05 * 2 ** k for k in range(j)], CU_BYTE if co_cu else None, []))
                ca_ds.append((f"(c) sau {j} PE", True, lambda e, j=j: dict(ke_hoach={"b": lambda i: eio(), "c": lambda i: PE() if i < j else (e if i == j else None)}),
                              None, [0.05 * 2 ** k for k in range(j)], None, ["cu"]))
            if windows:
                ca_ds.append(("ngủ ở (a)", True, lambda e: dict(ke_hoach={"a": lambda i: PE() if i == 0 else None}, ngat_ngu=(0, e)),
                              ["a"], [0.05], CU_BYTE, []))
                for co_cu in (True, False):
                    ca_ds.append(("ngủ ở (b)", co_cu, lambda e: dict(ke_hoach={"b": lambda i: PE() if i == 0 else None}, ngat_ngu=(0, e)),
                                  None, [0.05], CU_BYTE if co_cu else None, []))
                ca_ds.append(("ngủ ở (c)", True, lambda e: dict(ke_hoach={"b": lambda i: eio(), "c": lambda i: PE() if i == 0 else None}, ngat_ngu=(0, e)),
                              None, [0.05], None, ["cu"]))
                ca_ds.append(("ngủ khi dọn bản trước", True, lambda e: dict(ke_hoach={}, xoa={"cu": lambda i: {"unlink": [PE()]}}, ngat_ngu=(0, e)),
                              None, [0.05], MOI_BYTE, ["cu"]))
            for co_cu in (True, False):
                ca_ds.append(("dọn tạm", co_cu, lambda e: dict(ke_hoach={"b": lambda i: eio()}, xoa={"tam": lambda i: e}),
                              None, [], CU_BYTE if co_cu else None, ["tam"]))
            ca_ds.append(("dọn bản trước", True, lambda e: dict(ke_hoach={}, xoa={"cu": lambda i: e}), None, [], MOI_BYTE, ["cu"]))
            for ten, co_cu, cau_hinh, goi_mong, ngu_mong, out_mong, sot_mong in ca_ds:
                e = ngat()
                kw = cau_hinh(e)
                r = _ghi_voi_doi_ten_gia(kw.pop("ke_hoach", {}), windows=windows, co_cu=co_cu, bat_moi=True, **kw)
                bang(r["loi"] is e and r["ngu"] == ngu_mong and r["out"] == out_mong and _ten_sot(r) == sot_mong
                     and (goi_mong is None or r["goi"] == goi_mong),
                     f"ngắt {e!r} ở [{ten}] co_cu={co_cu} windows={windows}: mong loi=đúng đối tượng, ngủ {ngu_mong}, out {out_mong}, "
                     f"sót {sot_mong}; được {r}")
                so_o += 1
    bang(so_o == 4 * ((2 + 3 * 4 + 2 + 1) + (2 + 1 * 4 + 2 + 1) + (1 + 2 + 1 + 1)), f"số ô ngắt: {so_o}")

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
    ("F13_giai_ma_toan_stdout", 'dau, _, than = r.stdout.partition(b"\\n")', 'dau, _, than = r.stdout.decode("utf-8").encode().partition(b"\\n")', "c62"),
    ("F13_giai_ma_ca_phan_dau", '.split(b"\\n\\n", 1)[0].split(b"\\n")', '.split(b"\\n\\n", 1)[0].decode("utf-8").encode().split(b"\\n")', "c62"),
    ("F13_bo_kiem_oid", " or not all(RE_OID_B.fullmatch(x) for x in tree + cha):", ":", "c62"),
    ("F13_cha_quet_ca_dau", "            break\n        cha.append(x[7:])", "            continue\n        cha.append(x[7:])", "c62"),
    ("F13_bo_tree_dong_dau", ' or not dong[0].startswith(b"tree ")', "", "c62"),
    ("F13_cha_chi_hai", '"parents": [x.decode("ascii") for x in cha]}', '"parents": [x.decode("ascii") for x in cha[:2]]}', "c62"),
    ("F13_cha_chi_40", "fullmatch(x) for x in tree + cha)", 'fullmatch(x) for x in tree) and all(re.fullmatch(rb"[0-9a-f]{40}", x) for x in cha)', "c62"),
    ("F13_bo_kiem_loai", ' or loai[1] != b"commit"', "", "c62"),
    ("F13_tach_splitlines", '.split(b"\\n\\n", 1)[0].split(b"\\n")', '.split(b"\\n\\n", 1)[0].splitlines()', "c62"),
    ("F13_oid_khoang", 're.compile(rb"[0-9a-f]{40}|[0-9a-f]{64}")', 're.compile(rb"[0-9a-f]{40,64}")', "c62"),
    ("F13_oid_chu_so", 're.compile(rb"[0-9a-f]{40}|[0-9a-f]{64}")', 're.compile(rb"[0-9a-z]{40}|[0-9a-z]{64}")', "c62"),
    ("F13_nhieu_tree", "if len(tree) != 1 or", "if not tree or", "c62"),
    ("F13_chi_kiem_tree", "fullmatch(x) for x in tree + cha)", "fullmatch(x) for x in tree)", "c62"),
    ("F13_bo_tach_dau_than", '.split(b"\\n\\n", 1)[0].split(b"\\n")', '.split(b"\\n")', "c62"),
    ("F13_dao_cha", '"parents": [x.decode("ascii") for x in cha]}', '"parents": [x.decode("ascii") for x in cha][::-1]}', "c62"),
    ("F13_bo_oserror", "except (OSError, subprocess.SubprocessError, UnicodeEncodeError):", "except (subprocess.SubprocessError, UnicodeEncodeError):", "c62"),
    ("F13_bo_kiem_kieu", "    if type(sha) is not str:", "    if False:", "c62"),
    ("F13_bo_kiem_rc", "if r.returncode != 0 or len(loai) != 3", "if len(loai) != 3", "c62"),
    ("F13_bo_isdigit", " or not loai[2].isdigit()", "", "c62"),
    ("F13_bo_kiem_kich_thuoc", " or len(than) != int(loai[2]) + 1", "", "c62"),
    ("F13_bo_dem_truong_dau", "if r.returncode != 0 or len(loai) != 3 or", "if r.returncode != 0 or", "c62"),
    ("F13_nhan_truong_thua", "or len(loai) != 3 or", "or len(loai) < 3 or", "c62"),
    ("F13_nhan_than_cut", "len(than) != int(loai[2]) + 1", "len(than) > int(loai[2]) + 1", "c62"),
    ("F13_bo_unicodeencode", "except (OSError, subprocess.SubprocessError, UnicodeEncodeError):", "except (OSError, subprocess.SubprocessError):", "c62"),
    ("F13_bo_subprocesserror", "except (OSError, subprocess.SubprocessError, UnicodeEncodeError):", "except (OSError, UnicodeEncodeError):", "c62"),
    ("F13_lstrip_dau_dong", '.split(b"\\n\\n", 1)[0].split(b"\\n")\n', '.split(b"\\n\\n", 1)[0].split(b"\\n")\n    dong = [x.lstrip() for x in dong]\n', "c62"),
    *[(f"F13_bien_doi_{ten}", '.split(b"\\n\\n", 1)[0].split(b"\\n")\n', '.split(b"\\n\\n", 1)[0].split(b"\\n")\n    dong = ' + bd + "\n", "c62") for ten, bd in (
        ("lstrip_tab", '[x.lstrip(b"\\t") for x in dong]'), ("tab_thanh_sp", '[x.replace(b"\\t", b" ") for x in dong]'),
        ("ha_ten", '[x[:4].lower() + x[4:] for x in dong]'), ("rstrip", '[x.rstrip() for x in dong]'),
        ("xoa_cr", '[x.replace(b"\\r", b"") for x in dong]'), ("xoa_dieu_khien", '[bytes(c for c in x if c >= 32) for x in dong]'),
        ("gap_dong", 'b"\\n".join(dong).replace(b"\\n ", b" ").split(b"\\n")'),
        ("nfkc", '[__import__("unicodedata").normalize("NFKC", x.decode("utf-8", "replace")).encode() for x in dong]'),
        ("tach_unicode", '[y.encode() for x in dong for y in x.decode("utf-8", "replace").splitlines()]'),
        *[(f"tach_{h:02x}", f'[y for x in dong for y in x.split(bytes([{h}]))]') for h in (0x0b, 0x0c, 0x1c, 0x1d, 0x1e, 0x85)])],
    ("F13_crlf_truoc_tach", "dong = than[:int(loai[2])].split(", 'dong = than[:int(loai[2])].replace(b"\\r\\n", b"\\n").split(', "c62"),
    ("F13_tach_dau_cuoi", '.split(b"\\n\\n", 1)[0].split(b"\\n")\n', '.rsplit(b"\\n\\n", 1)[0].split(b"\\n")\n', "c62"),
    ("F13_dong_trang_la_ranh_gioi", "dong = than[:int(loai[2])].split(b", 'dong = re.split(rb"\\n[ \\t]*\\n", than[:int(loai[2])], maxsplit=1)[0].split(b"\\n")  # ', "c62"),
    ("F13_strip_payload", "dong = than[:int(loai[2])].split(", "dong = than[:int(loai[2])].strip().split(", "c62"),
    ("F13_gop_cha_trung", '"parents": [x.decode("ascii") for x in cha]}', '"parents": list(dict.fromkeys(x.decode("ascii") for x in cha))}', "c62"),
    ("F13_cha_toi_da_256", '"parents": [x.decode("ascii") for x in cha]}', '"parents": [x.decode("ascii") for x in cha[:256]]}', "c62"),
    *[(f"F13_gap_{ten}", '.split(b"\\n\\n", 1)[0].split(b"\\n")\n', '.split(b"\\n\\n", 1)[0].split(b"\\n")\n    dong = b"\\n".join(dong).replace(' + gap + ', b" ").split(b"\\n")\n', "c62")
      for ten, gap in (("crlf_sp", 'b"\\r\\n "'), ("lf_tab", 'b"\\n\\t"'), ("crlf_tab", 'b"\\r\\n\\t"'))],
    ("F13_gop_cha_lech_mot", "        cha.append(x[7:])\n", "        if x[7:] not in cha[:-1]:\n            cha.append(x[7:])\n", "c62"),
    ("F13_rstrip_ten_truong", '.split(b"\\n\\n", 1)[0].split(b"\\n")\n', '.split(b"\\n\\n", 1)[0].split(b"\\n")\n    dong = [x.split(b" ", 1)[0].rstrip() + b" " + x.split(b" ", 1)[1] if b" " in x else x for x in dong]\n', "c62"),
    ("F13_bo_hai_cham_ten", '.split(b"\\n\\n", 1)[0].split(b"\\n")\n', '.split(b"\\n\\n", 1)[0].split(b"\\n")\n    dong = [x.split(b" ", 1)[0].rstrip(b":") + b" " + x.split(b" ", 1)[1] if b" " in x else x for x in dong]\n', "c62"),
    ("F13_gap_backslash", "dong = than[:int(loai[2])].split(", 'dong = than[:int(loai[2])].replace(b"\\\\\\n", b"").split(', "c62"),
    ("F13_oid_chi_40", 're.compile(rb"[0-9a-f]{40}|[0-9a-f]{64}")', 're.compile(rb"[0-9a-f]{40}")', "c62"),
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
    ("B2_blob_sha1_thuan", 'return hashlib.sha1(b"blob %d\\0" % len(b) + b).hexdigest()', "return hashlib.sha1(b).hexdigest()", "c53"),
    ("B2_sha256_sai", "kq.update(blob=blob_cua(b), sha256=hashlib.sha256(b).hexdigest())", "kq.update(blob=blob_cua(b), sha256=hashlib.sha256(b[:-1]).hexdigest())", "c53"),
    ("B3_url_ref_hop_le", "/blob/([0-9a-f]{40})/(.+)$", "/blob/([0-9a-z]+)/(.+)$", "c54"),
    ("B3_bo_errors", 'if d.get("errors"):', "if False:", "c54"),
    ("B3_gop_loi", '{"path": e.get("path"), "type"', '{"path": None, "type"', "c54"),
    ("B4b_so_moi_event", 'if r["event"] in SU_KIEN_SO_OID:\n        so +=', "if True:\n        so +=", "c56"),
    ("B5_chap_nhan_run_0", "and int(a.run) > 0", "and int(a.run) >= 0", "c57"),
    ("B5_bo_ghi_khi_sai", "    if out:\n        Path(out)", "    if out and ok:\n        Path(out)", "c57"),
    ("B6_bo_tinh_lai", '("blob", blob_cua(b) == j["blob"]), ("sha256", hashlib.sha256(b).hexdigest() == j["sha256"])', '("blob", True), ("sha256", True)', "c58"),
    ("B6_bo_du", 'if not ds["du"] or len(arts) != 1', "if len(arts) != 1", "c58"),
    ("B6_bo_digest", 'if arts[0].get("digest") != f"sha256:{sz}":', "if False:", "c58"),
    ("B6_bo_wd_run", "    if wd_run is not None:\n        prov", "    if False:\n        prov", "c58"),
    ("B3_bo_run_attempt", 'for k in ("id", "run_attempt", "path", "head_sha", "event")', 'for k in ("id", "path", "head_sha", "event")', "c54"),
    ("B3_commit_kieu", 'cso = cm.get("oid") if type(cm) is dict else None', 'cso = cm.get("oid")', "c54"),
    ("B3_base64_long", 'validate=True)', "validate=False)", "c54"),
    ("B3_run_than_hong", '"phan_hoi_hong" if e.ma == "than_khong_phai_json" else f"rest_run_{e.ma}"', 'f"rest_run_{e.ma}"', "c54"),
    ("B3_blob_than_hong", '"phan_hoi_hong" if e.ma == "than_khong_phai_json" else f"blob_http_{e.ma}"', 'f"blob_http_{e.ma}"', "c54"),
    ("B2_ref_contents", '?ref={oid}"', '?ref=master"', "c53"),
    ("B4b_chi_push", 'SU_KIEN_SO_OID = ("push", "workflow_dispatch", "schedule")', 'SU_KIEN_SO_OID = ("push",)', "c55"),
    ("B5_out_tu_tim", "out = po.parse_known_args(argv)[0].out", 'out = argv[argv.index("--out") + 1] if "--out" in argv else None', "c57"),
    ("B5_json_toi_thieu", '{"schema": "wd/1", "trang_thai": "not_measured", "ly_do": "sai_doi_so"}, 2', '{"schema": "x", "trang_thai": "passed", "ly_do": "sai_doi_so"}, 2', "c57"),
    ("B6_cli_bo_wd_run", "moi_tu, wf, a.wd_run)", "moi_tu, wf, None)", "c58"),
    *[(f"B4_bo_so{i}", a, a.split(",")[0] + ", True)", "c55") for i, a in enumerate((
        '("repo", m[1] == repo)', '("url_path", m[3] == fp)', '("file_path", fp == r["path"])',
        '("databaseId", n.get("databaseId") == run)', '("oid_head_sha", oid == r["head_sha"])', '("oid_check_suite", cso == oid)',
    ))],
    *[(f"B6_bo_so{i}", a, a.split(",")[0] + ", True)", "c58") for i, a in enumerate((
        '("schema", j.get("schema") == "wd/1")', '("conclusion", w.get("conclusion") == "success")', '("repo", j.get("repo") == repo)',
        '("run_id", _so(j.get("run_id"), 1) and j.get("run_id") == run)', '("path", _chuoi(j.get("path")) and j.get("path") == r.get("path"))',
        '("trang_thai", j.get("trang_thai") == "passed")',
    ))],
    *[(f"B3_bo_dk{i}", a, "", "c54") for i, a in enumerate((
        ' and _so(n.get("databaseId"), 1)', ' and _so(n.get("runNumber"), 1)', ' and _chuoi(n.get("createdAt"))', '[:300]',
    ))],
    *[(f"B2_bo_chon{i}", a, "", "c53") for i, a in enumerate(("runNumber createdAt ", "file { path repositoryFileUrl } ", "checkSuite { commit { oid } } "))],
    ("B3_errors_kieu_ngoai", 'if type(d.get("errors", [])) is not list:', "if False:", "c54"),
    ("B3_thieu_bang_null", 'n.get(khoa, ...)) is None:', "n.get(khoa)) is None:", "c54"),
    ("B6_ref_khong_heads", 'ref.get("ref") == f"refs/heads/{kho.get(\'default_branch\')}"', "True", "c58"), ("B6_ref_khong_commit", 'o.get("type") == "commit"', "True", "c58"),
    ("B6_bo_to_tien", 'so.get("status") in ("identical", "behind")', 'so.get("status") is not None', "c58"),
    ("B6_bo_meta", '("meta", all(', '("meta", True or all(', "c58"),
    ("B6_bo_khoa", '("khoa", set(j) == KHOA_WD and', '("khoa", True or', "c58"),
    ("B3_cso_khong_hex", 'type(cso) is str and bool(RE_HEX40.fullmatch(cso)) and', "_chuoi(cso) and", "c54"),
    ("B6_run_id_kieu", '_so(j.get("run_id"), 1) and j.get("run_id") == run', 'j.get("run_id") == run', "c58"), ("B6_nguon_tuy_y", 'j.get("nguon") == "ops/ci_provenance.py do-wd"', '_chuoi(j.get("nguon"))', "c58"),
    ("W1_khong_thu_lai", "            if k == SO_LAN_THU_LAI:   # hết lượt: ném chính lỗi cuối", "            if True:", "c69"),   # #1475
    ("W2_bo_dieu_kien_nen", "            if not LA_WINDOWS:   # chỉ Windows", "            if False:", "c69"),
    ("W3_bat_OSError", "        except PermissionError:\n            if not LA_WINDOWS", "        except OSError:\n            if not LA_WINDOWS", "c69"),
    ("W4_nang_gioi_han", "SO_LAN_THU_LAI = 5            # tối đa", "SO_LAN_THU_LAI = 6            # tối đa", "c69"),   # range(+2) là đột biến TƯƠNG ĐƯƠNG (k == giới hạn vẫn ném ở lần 6)
    ("W5_nuot_loi_het_luot", "# hết lượt: ném chính lỗi cuối\n                raise", "# hết lượt: ném chính lỗi cuối\n                return", "c69"),
    ("W6_doi_he_so_cho", "            ngu_thu_lai(CHO_GOC * 2 ** k)", "            ngu_thu_lai(CHO_GOC * (k + 1))", "c69"),
    ("W7_bo_ngu", "            ngu_thu_lai(CHO_GOC * 2 ** k)", "            pass", "c69"),
    ("W8_a_goi_thang", "            doi_ten_thu_lai(out, cu)", "            os.replace(out, cu)", "c69"),
    ("W9_b_goi_thang", "        doi_ten_thu_lai(tam, out)", "        os.replace(tam, out)", "c69"),
    ("W10_c_goi_thang", "            doi_ten_thu_lai(cu, out)", "            os.replace(cu, out)", "c69"),
    ("W11_nem_loi_moi", "# hết lượt: ném chính lỗi cuối\n                raise", "# hết lượt: ném chính lỗi cuối\n                raise PermissionError(13, 'het luot')", "c69"),
    ("R1_la_windows_luon_sai", 'LA_WINDOWS = os.name == "nt"', "LA_WINDOWS = False", "c70"),   # #1475 review lượt 1 F2.a
    ("R2_la_windows_luon_dung", 'LA_WINDOWS = os.name == "nt"', "LA_WINDOWS = True", "c70"),
    ("R3_ngu_rong", "ngu_thu_lai = time.sleep", "ngu_thu_lai = lambda s: None", "c70"),
    ("R4_thay_the_rong", "_thay_the = os.replace", "_thay_the = lambda a, b: None", "c70"),
    ("R4b_xoa_cay_rong", "_xoa_cay = shutil.rmtree", "_xoa_cay = lambda p, **kw: None", "c70"),
    ("R5_ghi_rong", "ghi_tep(tam / ten, byte)", 'ghi_tep(tam / ten, b"")', "c69"),   # F2.b
    ("R11_nuot_het_luot_a", "        if out.exists():\n            doi_ten_thu_lai(out, cu)\n", "        if out.exists():\n            try:\n                doi_ten_thu_lai(out, cu)\n            except PermissionError:\n                pass\n", "c69"),   # F2.c
    ("R12_nuot_het_luot_c", "                doi_ten_thu_lai(cu, out)\n", "                try:\n                    doi_ten_thu_lai(cu, out)\n                except PermissionError:\n                    pass\n", "c69"),
    ("X1_bo_don_khi_hoan_tac_nem", "        try:\n            if cu.exists() and not out.exists():\n                doi_ten_thu_lai(cu, out)\n        finally:   # dọn thư mục tạm KỂ CẢ khi hoàn tác ném\n", "        if True:\n            if cu.exists() and not out.exists():\n                doi_ten_thu_lai(cu, out)\n        if True:\n", "c69"),   # F1.a
    ("X2_don_khong_thu_lai", "        if k == SO_LAN_THU_LAI:   # dọn: hết lượt", "        if True:", "c71"),   # F1.b/c
    ("X5_don_khong_bao", 'print(f"KHONG_DON_DUOC {p}', 'print(f"x {p}', "c71"),
    ("X6_don_nuot_cam", "_xoa_cay(p, onexc=lambda ham, duong, e: loi.append((duong, e)))", "_xoa_cay(p, ignore_errors=True)", "c71"),
    ("X7_bo_don_ban_truoc", "    if os.path.lexists(cu):\n        don_thu_muc(cu)", "    if False:\n        don_thu_muc(cu)", "c71"),
    ("X8_don_khong_ngu", "\n        ngu_thu_lai(CHO_GOC * 2 ** k)\n    try:", "\n        pass\n    try:", "c71"),
    ("N1_thu_lai_moi_loi_o_c", "                doi_ten_thu_lai(cu, out)\n", "                for _k in range(6):\n                    try:\n                        doi_ten_thu_lai(cu, out)\n                        break\n                    except OSError:\n                        ngu_thu_lai(0.01)\n                        if _k == 5:\n                            raise\n", "c69"),   # #1475 review lượt 2 F2.e
    ("N3_onerror_nuot_cam", "_xoa_cay(p, onerror=lambda ham, duong, tt: loi.append((duong, tt[1])))", "_xoa_cay(p, ignore_errors=True)", "c71"),
    ("Y1_bao_khong_co_lap", "    except Exception:\n        pass\n    return False", "    except ZeroDivisionError:\n        pass\n    return False", "c71"),   # F3
    ("B1_khong_phan_loai_lai", '"khac" not in loai):   # dọn', '("khac" not in loai or k > 0)):   # dọn', "c72"),   # #1475 lượt 4 F2.i (luật chỉ đọc LOẠI lỗi)
    ("B2_rong_coi_la_sach", "    for k in range(SO_LAN_THU_LAI + 1):\n        loi = []", "    if not any(Path(p).iterdir()):\n        return True\n    for k in range(SO_LAN_THU_LAI + 1):\n        loi = []", "c72"),   # F2.l
    ("B3_ENOTEMPTY_la_loi_khac", "isinstance(e, OSError) and e.errno == errno.ENOTEMPTY", "False", "c72"),
    ("B4_thu_lai_ca_loi_khac", '"khac" not in loai):   # dọn', 'True):   # dọn', "c72"),   # thay X3/N2
    ("B5_bo_dieu_kien_nen_khi_don", 'if not (LA_WINDOWS and "PE" in loai and', 'if not ("PE" in loai and', "c72"),   # thay X4; F2.h
    ("B6_chi_PE_moi_thu_lai", 'if not (LA_WINDOWS and "PE" in loai and "khac" not in loai):', 'if not (LA_WINDOWS and loai == {"PE"}):', "c72"),
    ("Z1_bao_nuot_BaseException", "    except Exception:\n        pass\n    return False", "    except BaseException:\n        pass\n    return False", "c72"),   # #1475 lượt 3 F2.g
    ("T1_bo_dieu_kien_co_PE", 'LA_WINDOWS and "PE" in loai and "khac"', 'LA_WINDOWS and "khac"', "c73"),   # #1475 lượt 5 F2.n
    ("T2_ENOTEMPTY_la_PE", '"PE" if isinstance(e, PermissionError) else', '"PE" if isinstance(e, PermissionError) or getattr(e, "errno", None) == errno.ENOTEMPTY else', "c73"),
    ("T3_ENOSPC_la_thu_cap", "isinstance(e, OSError) and e.errno == errno.ENOTEMPTY", "isinstance(e, OSError) and e.errno in (errno.ENOTEMPTY, errno.ENOSPC)", "c73"),
    ("T4_khac_can_ENOTEMPTY", 'and "khac" not in loai):', 'and ("khac" not in loai or "ENOTEMPTY" not in loai)):', "c73"),
    ('S1_PE_dung_kieu', 'loai = {"PE" if isinstance(e, PermissionError) else', 'loai = {"PE" if type(e) is PermissionError else', "c74"),   # #1475 lượt 6 F2.o
    ('S2_PE_theo_errno', 'loai = {"PE" if isinstance(e, PermissionError) else', 'loai = {"PE" if getattr(e, "errno", None) in (errno.EACCES, errno.EPERM) else', "c74"),
    ('S3_ENOTEMPTY_dung_kieu', 'isinstance(e, OSError) and e.errno == errno.ENOTEMPTY', 'type(e) is OSError and e.errno == errno.ENOTEMPTY', "c74"),
    ('S4_ENOTEMPTY_theo_errno', 'isinstance(e, OSError) and e.errno == errno.ENOTEMPTY', 'getattr(e, "errno", None) == errno.ENOTEMPTY', "c74"),
    ('S5_bo_loi_khong_OSError', 'else "khac" for _, e in loi}', 'else "khac" for _, e in loi if isinstance(e, OSError)}', "c74"),
    ('S6_khong_OSError_thu_cap', 'isinstance(e, OSError) and e.errno == errno.ENOTEMPTY', '(not isinstance(e, OSError) or e.errno == errno.ENOTEMPTY)', "c74"),
    ('U1_doi_ten_dung_kieu_PE', '        except PermissionError:\n', '        except PermissionError as e:\n            if type(e) is not PermissionError:\n                raise\n', "c75"),   # #1475 lượt 7 F2.p/F2.q
    ('U2_doi_ten_chi_EACCES', '        except PermissionError:\n', '        except PermissionError as e:\n            if e.errno != errno.EACCES:\n                raise\n', "c75"),
    ('U3_doi_ten_PE_theo_errno', '        except PermissionError:\n', '        except OSError as e:\n            if e.errno not in (errno.EACCES, errno.EPERM):\n                raise\n', "c75"),
    ('U4_doi_ten_loi_khac_sau_PE', '        except PermissionError:\n', '        except OSError as e:\n            if k == 0 and not isinstance(e, PermissionError):\n                raise\n', "c75"),
    ('U13_ngat_khong_don_tam', '    except BaseException:\n        try:\n', '    except Exception:\n        try:\n', "c75"),
    ('U9_sach_theo_callback', '        if not os.path.lexists(p):\n            return True', '        if not loi:\n            return True', "c75"),
    ('V1_doi_ten_PE_errno_cho_phep', '        except PermissionError:\n', '        except PermissionError as e:\n            if e.errno not in (None, errno.EACCES, errno.EPERM):\n                raise\n', 'c75'),   # #1475 lượt 8 F2.r: tích kiểu × errno
    ('V2_doi_ten_OSError_EPERM_la_PE', '        except PermissionError:\n', '        except OSError as e:\n            if not isinstance(e, PermissionError) and e.errno != errno.EPERM:\n                raise\n', 'c75'),
    ('V3_don_PE_errno_cho_phep', 'loai = {"PE" if isinstance(e, PermissionError) else', 'loai = {"PE" if isinstance(e, PermissionError) and getattr(e, "errno", None) in (None, errno.EACCES, errno.EPERM) else', 'c74'),
    ('V4_don_OSError_EPERM_la_PE', 'loai = {"PE" if isinstance(e, PermissionError) else', 'loai = {"PE" if isinstance(e, PermissionError) or getattr(e, "errno", None) == errno.EPERM else', 'c74'),
    ('J1_doi_ten_thu_lai_EINTR', '        except PermissionError:\n', '        except (PermissionError, InterruptedError):\n', 'c75'),   # #1475 lượt 9 F2.s: danh mục OSError toàn bộ
    ('J2_doi_ten_thu_lai_EAGAIN', '        except PermissionError:\n', '        except (PermissionError, BlockingIOError):\n', 'c75'),
    ('J3_don_EINTR_thu_cap', 'isinstance(e, OSError) and e.errno == errno.ENOTEMPTY', 'isinstance(e, OSError) and e.errno in (errno.ENOTEMPTY, errno.EINTR)', 'c74'),
    ('J4_don_EAGAIN_thu_cap', 'isinstance(e, OSError) and e.errno == errno.ENOTEMPTY', 'isinstance(e, OSError) and e.errno in (errno.ENOTEMPTY, errno.EAGAIN)', 'c74'),
    ('K1_doi_ten_EINTR_sau_PE', '        except PermissionError:\n', '        except (PermissionError, InterruptedError) as e:\n            if k == 0 and not isinstance(e, PermissionError):\n                raise\n', 'c75'),   # #1475 lượt 10 F2.t: danh mục đủ ở mọi vị trí retry
    ('K2_doi_ten_EAGAIN_sau_PE', '        except PermissionError:\n', '        except (PermissionError, BlockingIOError) as e:\n            if k == 0 and not isinstance(e, PermissionError):\n                raise\n', 'c75'),
    ('K3_don_EINTR_sau_PE', 'isinstance(e, OSError) and e.errno == errno.ENOTEMPTY', 'isinstance(e, OSError) and (e.errno == errno.ENOTEMPTY or (k > 0 and e.errno == errno.EINTR))', 'c74'),
    ('K4_don_EAGAIN_sau_PE', 'isinstance(e, OSError) and e.errno == errno.ENOTEMPTY', 'isinstance(e, OSError) and (e.errno == errno.ENOTEMPTY or (k > 0 and e.errno == errno.EAGAIN))', 'c74'),
    ('L1_ghi_bo_khoi_phuc_InterruptedError', '    except BaseException:\n        try:\n', '    except InterruptedError:\n        raise\n    except BaseException:\n        try:\n', 'c75'),   # #1475 lượt 11 F2.u: tích hợp danh mục đủ qua ghi_nguyen_tu
    ('L2_ghi_bo_khoi_phuc_BlockingIOError', '    except BaseException:\n        try:\n', '    except BlockingIOError:\n        raise\n    except BaseException:\n        try:\n', 'c75'),
    ('L3_ghi_bo_khoi_phuc_TimeoutError', '    except BaseException:\n        try:\n', '    except TimeoutError:\n        raise\n    except BaseException:\n        try:\n', 'c75'),
    ('M1_finally_thanh_except_Exception', '        finally:   # dọn thư mục tạm KỂ CẢ khi hoàn tác ném\n', '        except Exception:\n            if os.path.lexists(tam):\n                don_thu_muc(tam)\n            raise\n        else:   # đột biến\n', 'c76'),   # #1475 lượt 12 F2.v: ngắt ở mọi điểm của ghi_nguyen_tu
    ('M2_nuot_ngat_o_c', '                doi_ten_thu_lai(cu, out)', '                try:\n                    doi_ten_thu_lai(cu, out)\n                except (KeyboardInterrupt, SystemExit):\n                    pass', 'c76'),
    ('M3_nuot_ngat_khi_ngu_doi_ten', '            ngu_thu_lai(CHO_GOC * 2 ** k)\n\n_DUNG_ONEXC', '            try:\n                ngu_thu_lai(CHO_GOC * 2 ** k)\n            except BaseException:\n                pass\n\n_DUNG_ONEXC', 'c76'),
    ('M4_nuot_ngat_khi_ngu_don', '        ngu_thu_lai(CHO_GOC * 2 ** k)\n    try:', '        try:\n            ngu_thu_lai(CHO_GOC * 2 ** k)\n        except BaseException:\n            pass\n    try:', 'c76'),
    ('M5_nuot_ngat_khi_don_ban_truoc', '    if os.path.lexists(cu):\n        don_thu_muc(cu)\n', '    if os.path.lexists(cu):\n        try:\n            don_thu_muc(cu)\n        except BaseException:\n            pass\n', 'c76'),
    ('M6_GeneratorExit_tra_ve_som', '    except BaseException:\n        try:\n', '    except GeneratorExit:\n        return\n    except BaseException:\n        try:\n', 'c76'),
    ('M7_ValueError_tra_ve_som', '    except BaseException:\n        try:\n', '    except ValueError:\n        return\n    except BaseException:\n        try:\n', 'c76'),
)
TU_KIEM = (   # (tên, gốc, thay, ca đích, hạng mong đợi)
    ("vo_can_AttributeError_qua_except_doi_kieu", "def than(dong):\n",
     "def than(dong):\n    try:\n        raise AttributeError('vo can')\n    except Exception as e:\n"
     "        raise AssertionError(f'doi kieu {type(e).__name__}')\n", "c03", "TIN_DUNG_GIA"),
    ("chi_them_chu_thich", "TRANG = 100\n", "TRANG = 100  # vo hai\n", "c20", "SONG_SOT"),
)
_XD = chr(10)   # xuống dòng dựng bằng mã: neo nhiều dòng của `DOT_BIEN_TEST` không được tự xuất hiện lần thứ hai trong tệp này
DOT_BIEN_TEST = (   # #1322 M4: (tên, gốc, thay, TIỀN TỐ ca đích) — sửa CHÍNH tệp này để đo răng của bộ máy song song. Neo một dòng ghép
                    # từ hai mảnh vì cùng lý do; `chay_dot_bien_test` vẫn đòi neo xuất hiện ĐÚNG MỘT lần.
    ("T1_mien_nhan_khoang_trang", 're.fullmatch(r"[1-' + '8]", raw)', 're.fullmatch(r" *[0-9]+ *", raw)', "c64"),
    ("T2_mac_dinh_ngoai_linux", '!= "Linux":' + _XD + '            return 1', '!= "Linux" and False:' + _XD + '            return 1', "c64"),
    ("T3_gom_theo_thu_tu_xong", 'return list(ex.' + 'map(ham, viec))',
     'return [f.result() for f in __import__("concurrent.futures").futures.as_completed([ex.submit(ham, x) for x in viec])]', "c65"),
    ("T5_kiem_mien_sau_ca", 'file=sys.stderr)' + _XD + '        return 2' + _XD + '    print(f"TIEN TRINH',
     'file=sys.stderr)' + _XD + '        n = 1' + _XD + '    print(f"TIEN TRINH', "c66"),
    ("T6_bo_lam_nong", '    lam_nong_nen(n)' + _XD + '    return chay_theo_thu_tu(', '    pass' + _XD + '    return chay_theo_thu_tu(', "c67"),
    ("T7_lam_nong_bo_sot_dot_bien_test", 'DOT_BIEN + TU_KIEM + ' + 'DOT_BIEN_TEST:', 'DOT_BIEN + TU_KIEM:', "c67"),
    ("T8_bo_kiem_du_ket_qua", 'len(DOT_BIEN) > 0 and ' + 'du and', 'len(DOT_BIEN) > 0 and', "c66"),
    ("T18_du_chi_dem_so_luong", '[t for t, _, _ in kq_db] == ' + 'ten_kh', 'len(kq_db) == len(ten_kh)', "c66"),   # review lượt 5 F3c
    ("T19_ke_hoach_tu_ket_qua", 'ten_kh = [d[0] for _, d in ' + 'viec]', 'ten_kh = [d[0] for _, d in ' + 'viec][:0]', "c66"),
    ("T20_chay_nham_viec_gan_dung_ten", 'chay_theo_thu_tu(lambda v: v[0](' + '*v[1]), viec, n)', 'chay_theo_thu_tu(lambda v: viec[0][0](*viec[0][1]), viec, n)', "c68"),   # review lượt 6 F3d
    ("T21_ten_tu_runner_khong_tu_doi_so", '        return (ten, ' + '*ham(ten, *con_lai))', '        return (ten, *ham("v0", *con_lai))', "c68"),
)

def chay_con(ten_ca, ma):
    try:
        r = subprocess.run([sys.executable, "-B", str(HERE / "ci_provenance_test.py"), "--mot-ca", ten_ca], capture_output=True,
                           env=dict(os.environ, CI_PROVENANCE_MA=str(ma), PYTHONDONTWRITEBYTECODE="1"), timeout=300)
    except subprocess.TimeoutExpired:   # Windows that (#997): ca nang qua han ⇒ HONG co ten, khong lam sap ca bo
        return 124, f"QUA_HAN:{ten_ca}: tien trinh con qua 300 s"
    return r.returncode, (r.stdout + r.stderr).decode("utf-8", "replace")

_NEN = {}   # (ca đích, sha256 bản gốc) -> (rc, ra): bản gốc chạy MỘT lần mỗi ca, không phải mỗi mục đột biến

def nen_cua(ten_ca, goc):
    khoa = (ten_ca, hashlib.sha256(goc.encode("utf-8")).hexdigest())
    if khoa not in _NEN:
        with tempfile.TemporaryDirectory(prefix="cip_nen_") as thu:
            ban_goc = Path(thu) / "goc.py"
            ban_goc.write_text(goc, encoding="utf-8")
            _NEN[khoa] = chay_con(ten_ca, ban_goc)
    return _NEN[khoa]

BIEN_TIEN_TRINH = "CI_PROVENANCE_TIEN_TRINH"

def so_tien_trinh(env=None, he=None, cpu=None):
    """#1322 M1: số luồng của vòng đột biến. Vắng biến ⇒ `min(4, cpu)` trên Linux, 1 ở nền khác (Windows giữ tuần tự, #997).
    Có biến ⇒ ĐÚNG một chữ số ASCII 1–8; còn lại (rỗng, khoảng trắng, `04`, xuống dòng cuối, chữ số Unicode mà `int()` vẫn
    nhận) ⇒ ValueError. Khớp TOÀN chuỗi với lớp ký tự liệt kê, không dùng neo cuối dòng hay lớp chữ số Unicode."""
    raw = (os.environ if env is None else env).get(BIEN_TIEN_TRINH)
    if raw is None:
        if (platform.system() if he is None else he) != "Linux":
            return 1
        return min(4, (os.cpu_count() if cpu is None else cpu) or 1)
    if not isinstance(raw, str) or not re.fullmatch(r"[1-8]", raw):
        raise ValueError(f"{BIEN_TIEN_TRINH}={raw!r} ngoài miền 1–8")
    return int(raw)

def chay_theo_thu_tu(ham, viec, n):
    """#1322 M2: `ham` trên từng phần tử của `viec` bằng `n` luồng (việc thật nằm ở tiến trình con nên luồng là đủ).
    Kết quả trả theo THỨ TỰ `viec`, không theo thứ tự xong."""
    viec = list(viec)
    if n <= 1:
        return [ham(x) for x in viec]
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(n) as ex:
        return list(ex.map(ham, viec))

def lam_nong_nen(n):
    """#1322 M2: lượt bản gốc của mọi ca đích chạy TRƯỚC vòng đột biến, mỗi (ca, bản gốc) một lần, để các luồng đột biến chỉ
    ĐỌC `_NEN` — không có hai luồng cùng tính và cùng ghi một khoá. Bản gốc đọc Ở ĐÂY (cùng cách `chay_dot_bien` đọc), không
    truyền từ `main`: đối số tính trước lời gọi nên sẽ chạy cả khi hàm bị thay (c66)."""
    goc = (HERE / "ci_provenance.py").read_text(encoding="utf-8")
    dich = set()
    for muc in DOT_BIEN + TU_KIEM + DOT_BIEN_TEST:
        khop = [c for c in CA if c.split("_")[0] == muc[3]]
        if len(khop) == 1:
            dich.add(khop[0])
    chay_theo_thu_tu(lambda ten_ca: nen_cua(ten_ca, goc), sorted(dich), n)

def co_ten(ham):   # #1322 review lượt 6 F3d: tên trong kết quả lấy từ ĐỐI SỐ việc THẬT SỰ nhận, không do runner gắn
    def boc(ten, *con_lai):
        return (ten, *ham(ten, *con_lai))
    return boc

def chay_vong_dot_bien(n, viec):
    """#1322 M2: làm nóng `_NEN` rồi chạy `viec` bằng `n` luồng. `viec` do NGƯỜI GỌI sở hữu (review lượt 5 F3b/F3c: kế hoạch
    phải độc lập với hàm bị kiểm). Trả mỗi việc một bộ `(tên, hạng, chi tiết)` theo thứ tự việc — tên để người gọi đối chiếu."""
    lam_nong_nen(n)
    return chay_theo_thu_tu(lambda v: v[0](*v[1]), viec, n)

def chay_con_ban_test(ten_ca, ban_test):
    """#1322 M4: chạy MỘT ca trên bản sao (đã đột biến) của CHÍNH tệp test; mã sản phẩm là bản thật."""
    try:
        r = subprocess.run([sys.executable, "-B", str(ban_test), "--mot-ca", ten_ca], capture_output=True,
                           env=dict(os.environ, CI_PROVENANCE_MA=str(HERE / "ci_provenance.py"), PYTHONDONTWRITEBYTECODE="1"),
                           timeout=300)
    except subprocess.TimeoutExpired:
        return 124, f"QUA_HAN:{ten_ca}: tien trinh con qua 300 s"
    return r.returncode, (r.stdout + r.stderr).decode("utf-8", "replace")

def chay_dot_bien_test(ten, cu, moi, tien_to):
    """Như `chay_dot_bien`, nhưng đột biến sửa `ci_provenance_test.py`; cùng phân hạng `phan_hang`, cùng đòi bản gốc XANH."""
    khop = [c for c in CA if c.split("_")[0] == tien_to]
    if len(khop) != 1:
        return "HONG", f"tiền tố ca đích {tien_to!r} phải khớp ĐÚNG MỘT ca, khớp {khop}"
    ten_ca = khop[0]
    goc_test = (HERE / "ci_provenance_test.py").read_text(encoding="utf-8")
    if goc_test.count(cu) != 1 or cu == moi:
        return "HONG", f"neo phải xuất hiện đúng 1 lần trong tệp test và đột biến phải đổi mã (thấy {goc_test.count(cu)})"
    rc, ra = nen_cua(ten_ca, (HERE / "ci_provenance.py").read_text(encoding="utf-8"))
    if rc != 0:
        return "HONG", f"ca đích không xanh trên bản gốc (rc={rc}): {ra[-200:]}"
    with tempfile.TemporaryDirectory(prefix="cip_dbt_") as thu:   # bản sao test ĐỨNG CẠNH mã sản phẩm thật: ca nào đọc `HERE` cũng thấy nó
        ban = Path(thu) / "ci_provenance_test.py"
        ban.write_text(goc_test.replace(cu, moi), encoding="utf-8")
        (Path(thu) / "ci_provenance.py").write_bytes((HERE / "ci_provenance.py").read_bytes())
        rc, ra = chay_con_ban_test(ten_ca, ban)
        return phan_hang(rc, ra, ten_ca), ra.strip()[-200:]

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
    rc, ra = nen_cua(ten_ca, goc)
    if rc != 0:
        return "HONG", f"ca đích không xanh trên bản gốc (rc={rc}): {ra[-200:]}"
    with tempfile.TemporaryDirectory(prefix="cip_db_") as thu:
        ban_db = Path(thu) / f"db_{ten}.py"
        ban_db.write_text(goc.replace(cu, moi), encoding="utf-8")
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
    try:   # #1322 M1: miền sai ⇒ dừng TRƯỚC ca nào; dòng TIEN TRINH đứng đầu để bốn dòng cuối của sổ `MOI` liền nhau (M3)
        n = so_tien_trinh()
    except ValueError as e:
        print(f"CI_PROVENANCE: {e}", file=sys.stderr)
        return 2
    print(f"TIEN TRINH: {n}")
    kq = [chay_ca(ten) for ten in CA]
    print("".join(f"[{dong}]\n" for rc, dong in kq if rc), end="")
    dat = sum(rc == 0 for rc, _ in kq)
    print(f"CA: {dat}/{len(CA)} dat")
    viec = [(co_ten(chay_dot_bien), d) for d in DOT_BIEN] + [(co_ten(chay_dot_bien_test), d) for d in DOT_BIEN_TEST]   # kế hoạch ĐỘC LẬP (review lượt 5 F3b/F3c)
    ten_kh = [d[0] for _, d in viec]
    kq_db = chay_vong_dot_bien(n, list(viec))   # bản sao: hàm bị kiểm không đổi được kế hoạch của người gọi
    du = len(set(ten_kh)) == len(ten_kh) and [t for t, _, _ in kq_db] == ten_kh   # đúng tên, đúng thứ tự, đúng số lần — không chỉ đếm
    if not du:
        print(f"[DOT BIEN THIEU/LAP/DAO VIEC] ke hoach {len(ten_kh)} viec, ket qua {len(kq_db)}")
    xau = [f"{t}: {h} {ct}" for t, h, ct in kq_db if h != "GIET"]
    for x in xau:
        print(f"[DOT BIEN KHONG BI GIET DUNG] {x}")
    print(f"DOT BIEN: {sum(h == 'GIET' for _, h, _ in kq_db)}/{len(ten_kh)} bi giet dung ly do")   # tử số từ KẾT QUẢ thật (F3), mẫu số từ KẾ HOẠCH
    loi_tk = [f"{ten}: mong {mong}, duoc {h}" for ten, cu, moi, dich, mong in TU_KIEM
              for h in [chay_dot_bien(ten, cu, moi, dich)[0]] if h != mong]
    for x in loi_tk:
        print(f"[TU KIEM] {x}")
    print(f"TU KIEM PHAN HANG: {'DAT' if not loi_tk else 'DO'} ({len(TU_KIEM)} dot bien)")
    ok = dat == len(CA) > 0 and len(DOT_BIEN) > 0 and du and not xau and not loi_tk
    print(f"TONG: {'DAT' if ok else 'DO'}")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
