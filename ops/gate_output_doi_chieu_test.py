#!/usr/bin/env python3
"""Phản chứng CHẠY ĐƯỢC cho `ops/gate_output_doi_chieu.py` — wp1236 đợt A1, đặc tả r7 mục `nghiem_thu` (ca A1–A22, p1127).

Fixture: `F-ok` = provenance THẬT của pr1231 (23 job: 22 J + `chuan-bi`), chỉ thay `log_day_du` bằng băm log giả; workflow đọc từ
commit THẬT `fe84620` trong một clone `--shared` của kho (G05); tệp `gate_output/2` dựng từ bảng dòng mẫu VIẾT TAY (`MAU`), không
gọi module. `F-41397205258` = run `duong_nhanh` thật dựng từ readback REST qua `ci_provenance.moc_gate` (G06).
ĐỘT BIẾN sửa BẢN SAO TẠM của module (neo đúng một lần); ca đích chạy ở tiến trình con và phải XANH trên bản gốc trước. Chỉ `bang()` ném
`TinHieuChotCa` (con in `DO:<ca>:`, thoát 3); lỗi vô can thoát 4 ⇒ TÍN DỤNG GIẢ. Ra: `CA: N/N dat` · `DOT BIEN: M/M bi giet dung ly do` ·
`TU KIEM PHAN HANG: DAT (k dot bien)` · `TONG: DAT`. Thoát 0 chỉ khi đủ cả.
"""
import atexit
import copy
import functools
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import types
from pathlib import Path

import yaml

sys.dont_write_bytecode = True
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="backslashreplace")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MA = Path(os.environ.get("GATE_OUTPUT_DOI_CHIEU_MA") or HERE / "gate_output_doi_chieu.py")
LAND = ROOT / "ops/land"
PR1231 = LAND / "pr1231-wp1105-provenance/ci/provenance.yaml"
NHANH = LAND / "pr1055-wp1052-provenance"
SHA_CK = "fe84620f897913c7f6c2ce5a0c7316a49655e82f"
TIEN_TO = "https://github.com/ducthangho/tra-luat/"
# A20b — CHÉP RIÊNG khoá + miền của sổ luật, đo trên bản đợt A1. Đổi một ký tự trong `LUAT_v1` ⇒ khoá đổi ⇒ A20 ĐỎ.
KY_VONG_SO = {"ee0f2db86fc579ff236ff0417de0658a184a4ed4871468c90a2f0c42417037cc": (1, None)}


class TinHieuChotCa(AssertionError):
    """Chỉ `bang()` ném lớp này ⇒ phân biệt được giết thật (chốt) với chết vì lỗi vô can."""


CA = {}


def bang(dieu_kien, thong_diep):
    if not dieu_kien:
        raise TinHieuChotCa(thong_diep)


def ca(f):
    CA[f.__name__] = f
    return f


@functools.cache
def nap():
    s = importlib.util.spec_from_file_location("gate_output_doi_chieu_duoi_test", MA)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def ban_sao(them):
    """Module nạp từ nguồn của MA + đoạn `them` chạy SAU cùng (sửa sổ luật trên bản sao, không chạm tệp)."""
    m = types.ModuleType("gate_output_ban_sao")
    m.__file__ = str(MA)
    exec(compile(MA.read_text(encoding="utf-8") + "\n" + them, str(MA), "exec"), m.__dict__)
    return m


def git(*a, cwd=None, inp=None):
    return subprocess.run(["git", *a], cwd=cwd, input=inp, capture_output=True, check=True).stdout.decode().strip()


@functools.cache
def goc():
    """G05: clone `--shared` chứa ĐÚNG commit `fe84620` (và `8983e1b`) — không commit `ci.yml` vào một OID khác."""
    d = Path(tempfile.mkdtemp(prefix="go2_goc_"))
    atexit.register(shutil.rmtree, d, True)
    git("clone", "-q", "--shared", "--no-checkout", str(ROOT), str(d / "k"))
    return d / "k"


def commit_ci(van):
    """Commit mới chỉ gồm `.github/workflows/ci.yml` = `van` (biến thể YAML của A14); trả SHA."""
    k = goc()
    b = git("hash-object", "-w", "--stdin", cwd=k, inp=van.encode())
    t = git("mktree", cwd=k, inp=f"100644 blob {b}\tci.yml\n".encode())
    t = git("mktree", cwd=k, inp=f"040000 tree {t}\tworkflows\n".encode())
    t = git("mktree", cwd=k, inp=f"040000 tree {t}\t.github\n".encode())
    return git("-c", "user.name=go2", "-c", "user.email=go2@local", "commit-tree", t, "-m", "bien the", cwd=k)   # runner CI không có danh tính


@functools.cache
def ci_goc():
    return git("show", f"{SHA_CK}:.github/workflows/ci.yml", cwd=ROOT) + "\n"


C, J = "CUOI TỔNG: ĐẠT", 'JSON {"ok": true}'
MAU = {   # tiền tố job → [(tên bước REST, [nội dung BUOC])]: dòng mẫu VIẾT TAY theo log thật của run 42032872356
    "gate (": [("codex credential selftest (packet #300)", [C]), ("idiom-ba-ten selftest", [C]), ("eol-policy selftest", ["30/30 dat"]),
               ("pre-push selftest", ["9/9 dat"]), ("eol-policy survey", [J]), ("bundled-fragment check (topology gói)", [J]),
               ("gen_instructions selftest", ["== gen_instructions selftest 44/44 =="]), ("command-registry unit test (AG-T0-03)", ["OK"]),
               ("tl selftest (co bang chung exact-identity)", ["== tl selftest 1776/1776 ==", '{"ok": true, "status": "pass", "name": '
                '"tl-selftest", "returncode": 0, "duration_seconds": 189.593434, "evidence": '
                '"/home/runner/work/tra-luat/tra-luat/scripts/.tl_state/gate/tl-selftest-Linux.json"}']),
               ("workflow-audit strict", [J]), ("golden-test", [J]), ("doc-claims-check strict", [J]), ("determinism-audit strict", [J]),
               ("ci-phamvi guard (bang phu thuoc khop ma)", ["OK ci_phamvi (ve BAM)"]),
               ("ci-phamvi selftest (phan chung — cong co rang)", ["== ci_phamvi_test 7/7 =="]), ("release-check full", [J]),
               ("release-verify strict (lane LAND — manifest committed)", [J]),
               ("release-bundle x2 cùng SHA-256", ["bundle sha256 = c513ca07aaeb6dc812f54e565fba9185bf3d3d25bad013c95fe605cc1dc2c70b"])],
    "gate-cong-cu (": [("G5 manh ban kinh dot bien (#668)", ["cong_cu_test: 61/61 đạt; tổng=61, bỏ qua=0, tiền kiểm bỏ qua=0",
                                                              "MẢNH {k}/8: 62/62 đột biến bán kính 1 · ghi manh/manh-{k}.txt"])],
    "gate-cong-cu-gop": [("G5 gom manh ban kinh dot bien (#668)", ["SỐ LIỆU GOM: ca=61 · đột biến=490 · lỗi đột biến=0"])],
    "gate-nhanh-manh": [("chạy mảnh nhanh_don_duoc (targeted_mutant_gate)", ["targeted_mutant_gate MANH {k}/8: rc=0 · passed 39/39"])],
    "gate-nhanh-gop": [("gộp mảnh nhanh_don_duoc (targeted_mutant_gate)", [
        "targeted_mutant_gate: DAT — KHONG phai full mutant audit; full_mutant_audit van BAT BUOC truoc merge/land/release"])],
    "gate-ops": [("ci-duong-nhanh selftest (phan loai diff + khoa cau truc if)", ["CUOI TONG: DAT"]),
                 ("bien-nhan v2 selftest", ["bien_nhan_v2_test: 98/98 ca đạt · 153/153 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · "
                                            "135/153 đột biến thường khai đối chứng", C]),
                 ("lease-publish selftest (đo lại setup sau G5)", ["lease_publish: 284/284 đạt; đã chạy=284, bỏ qua=0"]),
                 ("don-nhanh selftest (chốt xoá nhánh)", ["don-nhanh: 21/21 dat"]),
                 ("bo ca gate chay TRONG cgroup duoc uy quyen (Linux)", ["gate lifecycle tests: 28/28 ca QUA (bo qua 0, hong 0)"])],
    "gate-packet-loop": [("packet-loop selftest", [C])],
    "gate-registry": [("test registry (phạm vi + các bộ chưa được nối)", [C, "KHONG 0"])],
}


def dong_job(j, log, mui):
    return (f"JOB {j['job_id']} name={json.dumps(j['name'], ensure_ascii=False)} labels={json.dumps(j['labels'], ensure_ascii=False)} "
            f"conclusion={j['conclusion']} log_sha256={log} -> {mui}")


def van(p, chi_success=False):
    """Tệp `gate_output/2` viết tay cho provenance `p`: JOB mọi job trong T; STEP/BUOC từ `MAU` cho job J."""
    r, ra, nj = p["moc"]["run"], [], 0
    ra.append(f"# gate_output/2 run={r['run_id']} attempt={p['attempt_yeu_cau']} head={r['head_sha']} luat_sha256={next(iter(KY_VONG_SO))}")
    for j in p["moc"]["gate_output"]["jobs"]:
        if j["conclusion"] == "skipped":
            continue
        trong_j = "ubuntu-latest" in (j["labels"] or []) and j["name"] != "chuan-bi"
        ra.append(dong_job(j, p["log_day_du"][j["job_id"]]["sha256"], "passed" if trong_j else
                           "not_measured" if j["name"] == "chuan-bi" else "ngoai_pham_vi_os"))
        nj += trong_j
        k = (re.findall(r", ([0-7])\)$", j["name"]) or ["0"])[0]
        for tien_to, buoc in MAU.items():
            if trong_j and j["name"].startswith(tien_to):
                ok = {b["name"] for b in j["buoc"] if b["conclusion"] == "success"} if type(j["buoc"]) is list else set()
                for ten, nd in buoc:
                    if chi_success and ten not in ok:
                        continue
                    ra.append(f"  STEP name={json.dumps(ten, ensure_ascii=False)} conclusion=success")
                    ra += [f"    BUOC [{ten}] {x.replace('{k}', k)}" for x in nd]
    return "\n".join(ra + [f"MOC_GATE_OUTPUT: passed ({nj}/{nj} job)"]) + "\n"


def gia_log(p):
    for i in p["log_day_du"]:
        p["log_day_du"][i] = {"sha256": hashlib.sha256(f"log gia {i}\n".encode()).hexdigest()}
    return p


@functools.cache
def _f_ok():
    return gia_log(yaml.safe_load(PR1231.read_text(encoding="utf-8")))


def f_ok():
    p = copy.deepcopy(_f_ok())
    return van(p), p


def kq(text, p, g=None):
    return nap().kiem(text, p, g or goc())


def ky(text, p, mong, chua=None, ten=""):
    tt, ly = kq(text, p)
    bang(tt == mong and (chua is None or any(chua in x for x in ly)), f"{ten}: mong {mong}/{chua}, được {tt} {ly[:6]}")


def jb(p, ten):
    return next(j for j in p["moc"]["gate_output"]["jobs"] if j["name"] == ten)


@ca
def a01_duong_f_ok():
    text, p = f_ok()
    ky(text, p, "passed", ten="F-ok")


@ca
def a02_bam_log():
    text, p = f_ok()
    for ten in ("gate (ubuntu-latest)", "chuan-bi"):
        h = p["log_day_du"][jb(p, ten)["job_id"]]["sha256"]
        ky(text.replace(h, ("0" if h[0] != "0" else "1") + h[1:]), p, "not_measured", "bam_log", ten)


def bo_job(p, text, ten):
    j = jb(p, ten)
    p["moc"]["gate_output"]["jobs"].remove(j)
    p["log_day_du"].pop(j["job_id"])
    p["moc"]["checkout"] = [c for c in p["moc"]["checkout"] if c["job_id"] != j["job_id"]]
    return j


@ca
def a03_tap_job():
    text, p = f_ok()
    g = jb(p, "gate (ubuntu-latest)")
    dg = [d for d in text.split("\n") if d.startswith(f"JOB {g['job_id']} ")][0]
    ky(text.replace(dg + "\n", ""), p, "not_measured", "tap_job", "a")
    q = copy.deepcopy(p)
    q["log_day_du"].pop(g["job_id"])
    ky(text, q, "not_measured", "tap_job", "b")
    ky(text.replace(dg + "\n", dg + "\n" + dg + "\n"), p, "not_measured", "tap_job", "c")
    for ten, sua in (("d", lambda q: q["moc"]["gate_output"]["jobs"].clear()),
                     ("e", lambda q: [j.update(conclusion="skipped") for j in q["moc"]["gate_output"]["jobs"]]),
                     ("g", lambda q: [bo_job(q, "", j["name"]) for j in list(q["moc"]["gate_output"]["jobs"]) if j["name"] != "chuan-bi"]),
                     ("h", lambda q: [j.update(labels=["windows-latest"]) for j in q["moc"]["gate_output"]["jobs"]])):
        q = copy.deepcopy(p)
        sua(q)
        q["log_day_du"] = {i: v for i, v in q["log_day_du"].items() if i in {j["job_id"] for j in q["moc"]["gate_output"]["jobs"]
                                                                              if j["conclusion"] != "skipped"}}
        ky(van(q), q, "not_measured", "tap_job_rong", ten)
    q = copy.deepcopy(p)
    jb(q, "gate-ops (ubuntu-latest)")["runner_id"] = 0
    ky(text, q, "not_measured", "job_chua_chay", "f")
    q = copy.deepcopy(p)
    q["moc"]["checkout"] = [c for c in q["moc"]["checkout"] if c["job_id"] != g["job_id"]]
    ky(text, q, "not_measured", "checkout_job_chua_do", "i")
    q = copy.deepcopy(p)   # (j) tám mảnh gate-cong-cu thành MỘT mục bị bỏ cả job, đúng hình `ci_provenance.moc_gate` ghi (G06)
    for k in range(8):
        bo_job(q, "", f"gate-cong-cu (ubuntu-latest, {k})")
    rest = [x for x in json.loads((NHANH / "readback-jobs-41397205258.json").read_text())["jobs"] if x["name"] == "gate-cong-cu"][0]
    q["moc"]["gate_output"]["jobs"].append(nap().cp.moc_gate(rest, [], {}, lambda *a: False))
    q["moc"]["checkout"].append({"job_id": rest["id"], "name": rest["name"], "trang_thai": "skipped"})
    tt, ly = kq(van(q), q)
    bang(tt == "not_measured" and sorted(x for x in ly if x.startswith("thieu_job_bat_buoc")) ==
         [f"thieu_job_bat_buoc:gate-cong-cu (ubuntu-latest, {k})" for k in range(8)], f"j: {tt} {ly[:9]}")
    q = copy.deepcopy(p)   # (j′) hai job `gate (ubuntu-latest)`
    g2 = dict(copy.deepcopy(g), job_id=g["job_id"] + 10**9)
    q["moc"]["gate_output"]["jobs"].append(g2)
    q["log_day_du"][g2["job_id"]] = q["log_day_du"][g["job_id"]]
    q["moc"]["checkout"].append(dict(next(c for c in q["moc"]["checkout"] if c["job_id"] == g["job_id"]), job_id=g2["job_id"]))
    ky(van(q), q, "not_measured", "job_trung_ten:gate (ubuntu-latest)", "j′")
    q = copy.deepcopy(p)   # (j″) job lạ, không sửa module
    g3 = dict(copy.deepcopy(g), job_id=g["job_id"] + 2 * 10**9, name="gate-moi (ubuntu-latest)")
    q["moc"]["gate_output"]["jobs"].append(g3)
    q["log_day_du"][g3["job_id"]] = q["log_day_du"][g["job_id"]]
    q["moc"]["checkout"].append(dict(next(c for c in q["moc"]["checkout"] if c["job_id"] == g["job_id"]), job_id=g3["job_id"]))
    ky(van(q), q, "not_measured", "job_ngoai_luat:gate-moi (ubuntu-latest)", "j″")
    for truoc in (True, False):   # (k) F01: bản ghi trùng `job_id` mang `failure`, đứng trước hoặc sau
        q = copy.deepcopy(p)
        ds = q["moc"]["gate_output"]["jobs"]
        hong = dict(copy.deepcopy(g), conclusion="failure")
        ds.insert(ds.index(jb(q, "gate (ubuntu-latest)")) + (0 if truoc else 1), hong)
        ky(text, q, "not_measured", "job_id_trung_provenance", f"k{truoc}")


@functools.cache
def _f_nhanh():
    """F-41397205258: run `duong_nhanh` thật; job dựng bằng `ci_provenance.moc_gate` trên REST (G06)."""
    r = json.loads((NHANH / "readback-run-41397205258.json").read_text())
    jobs = json.loads((NHANH / "readback-jobs-41397205258.json").read_text())["jobs"]
    gate = [nap().cp.moc_gate(j, [], {}, lambda *a: False) for j in jobs]
    co = [{"job_id": j["id"], "name": j["name"]} | ({"trang_thai": "skipped"} if j["conclusion"] == "skipped" else
                                                   {"trang_thai": "passed", "sha": r["head_sha"]}) for j in jobs]
    p = {"schema": "ci_provenance/1", "attempt_yeu_cau": 1, "log_day_du": {j["id"]: 0 for j in jobs if j["conclusion"] != "skipped"},
         "moc": {"run": {"repo": "ducthangho/tra-luat", "run_id": r["id"], "run_attempt": r["run_attempt"], "event": r["event"],
                         "head_sha": r["head_sha"], "loi_khai_rest_path": r["path"], "trang_thai": "passed"},
                 "checkout": co, "gate_output": {"jobs": gate}}}
    return gia_log(p)


@ca
def a03k_run_duong_nhanh_that():
    p = copy.deepcopy(_f_nhanh())
    tt, ly = kq(van(p, chi_success=True), p)
    bang(tt == "not_measured" and sorted(x for x in ly if x.startswith("thieu_job_bat_buoc")) ==
         [f"thieu_job_bat_buoc:gate-cong-cu (ubuntu-latest, {k})" for k in range(8)], f"A3k: {tt} {ly[:12]}")


@ca
def a04_danh_tinh():
    text, p = f_ok()
    ky(text.replace('name="gate-ops (ubuntu-latest)"', 'name="gate-ops (ubuntu-latest) "'), p, "not_measured", "danh_tinh", "a")
    q = copy.deepcopy(p)
    jb(q, "gate-ops (ubuntu-latest)")["conclusion"] = "failure"
    ky(text, q, "failed", "job_khong_success", "b")
    g = jb(p, "gate-ops (ubuntu-latest)")
    ky(text.replace(f'JOB {g["job_id"]} name="gate-ops (ubuntu-latest)" labels=["ubuntu-latest"]',
                    f'JOB {g["job_id"]} name="gate-ops (ubuntu-latest)" labels=["ubuntu-latest", "x"]'), p, "not_measured", "danh_tinh", "c")


@ca
def a05_ca_dong():
    text, p = f_ok()
    ky(text.replace("] 9/9 dat\n", "] 9/9 dat BỎ QUA 74\n"), p, "not_measured", "thieu_dau_hieu")


@ca
def a06_sai_loai():
    text, p = f_ok()
    ky(text.replace("] SỐ LIỆU GOM: ca=61 · đột biến=490 · lỗi đột biến=0\n", "] CUOI TỔNG: ĐẠT\n"), p, "not_measured", "thieu_dau_hieu")


@ca
def a07_n_tren_m():
    text, p = f_ok()   # F04: header theo băm của CHÍNH module đang chạy, để đột biến regex không chết vì đổi băm (A20 canh băm)
    text = re.sub("luat_sha256=[0-9a-f]{64}", "luat_sha256=" + nap().bam(nap().LUAT_v1), text)
    ky(text.replace("passed (22/22 job)", "passed (21/22 job)"), p, "not_measured", "moc_tong", "moc")
    ky(text.replace("gen_instructions selftest 44/44", "gen_instructions selftest 43/44"), p, "not_measured", "thieu_dau_hieu", "N/M")
    ky(text.replace("cong_cu_test: 61/61 đạt; tổng=61", "cong_cu_test: 60/61 đạt; tổng=61"), p, "not_measured", "thieu_dau_hieu", "60/61")


@ca
def a08_neo_run():
    text, p = f_ok()
    r = p["moc"]["run"]
    for cu, moi in ((f"run={r['run_id']}", f"run={r['run_id'] + 1}"), ("attempt=1 ", "attempt=2 ")):
        ky(text.replace(cu, moi, 1), p, "not_measured", "neo_run", cu)
    ky(text.replace(f"head={SHA_CK}", f"head={SHA_CK[:39]}0", 1), p, "not_measured", "neo_run", "head")
    ky(text.replace(f"head={SHA_CK}", f"head={SHA_CK[:8]}", 1), p, "not_measured", "dinh_dang", "head8")
    for k, v, ly in (("trang_thai", "not_measured", "run_chua_passed"), ("repo", "o/r", "sai_kho"), ("event", "pull_request", "su_kien")):
        q = copy.deepcopy(p)
        q["moc"]["run"][k] = v
        ky(text, q, "not_measured", ly, k)


SO_V2 = ("LUAT_v2 = dict(LUAT_v1, ghi_chu='v2')\nLUAT_PHIEN_BAN = {{bam(LUAT_v1): LUAT_v1, bam(LUAT_v2): LUAT_v2}}\n"
         "MIEN_HIEU_LUC = {{bam(LUAT_v1): (1, {r} - 1), bam(LUAT_v2): ({r}, None)}}\n")


@ca
def a09_so_luat_mien():
    text, p = f_ok()
    run = p["moc"]["run"]["run_id"]
    bang(ban_sao(SO_V2.format(r=run + 1)).kiem(text, p, goc())[0] == "passed", "b: run < R với tệp v1 phải passed")
    bang(ban_sao(SO_V2.format(r=run)).kiem(text, p, goc())[0] == "not_measured", "c: run ≥ R với tệp v1 phải not_measured")
    ky(re.sub("luat_sha256=[0-9a-f]{64}", "luat_sha256=" + "a" * 64, text), p, "not_measured", "luat_ngoai_so", "a")


@ca
def a10_cuoi():
    text, p = f_ok()
    ten = "test registry (phạm vi + các bộ chưa được nối)"
    ky(text.replace(f"[{ten}] CUOI TỔNG: ĐẠT\n", f"[{ten}] CUOI TỔNG: ĐẠT\n    BUOC [{ten}] CUOI TỔNG: ĐỎ\n"), p, "not_measured", "cuoi")


@ca
def a11_khong():
    text, p = f_ok()
    ky(text.replace("] KHONG 0\n", "] KHONG 1\n"), p, "not_measured", "khong_khac_0")


@ca
def a12_json():
    text, p = f_ok()
    for x in ('{"ok": false}', '{"x": {"ok": true}}'):
        ky(text.replace('[golden-test] JSON {"ok": true}', f"[golden-test] JSON {x}"), p, "not_measured", "json_khong_ok", x)


@ca
def a13_buoc_rest():
    text, p = f_ok()
    ten = "packet-loop selftest"
    ky(text.replace(f'STEP name="{ten}"', 'STEP name="packet-loop selftest x"'), p, "not_measured", "step_khong_trong_buoc", "a")
    q = copy.deepcopy(p)
    next(b for b in jb(q, "gate-packet-loop (ubuntu-latest)")["buoc"] if b["name"] == ten)["conclusion"] = "failure"
    ky(text, q, "failed", "buoc_khong_success", "b")
    s = f'  STEP name="{ten}" conclusion=success\n    BUOC [{ten}] CUOI TỔNG: ĐẠT\n'
    ky(text.replace(s, s + s), p, "not_measured", "thieu_hoac_lap_buoc", "c")


BLOCK = "      - name: packet-loop selftest\n        if: ${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}\n"


def bien_the_yaml(p, sua_van, sha=None):
    q = copy.deepcopy(p)
    s = sha or commit_ci(sua_van(ci_goc()))
    for c in q["moc"]["checkout"]:
        if c.get("trang_thai") == "passed":
            c["sha"] = s
    return q


def sau(van_, moc, cu, moi):   # thay `cu` LẦN ĐẦU sau mốc `moc`
    i = van_.index(moc)
    return van_[:i] + van_[i:].replace(cu, moi, 1)


@ca
def a14_k7_yaml():
    text, p = f_ok()
    loai = {
        "a": (lambda v: v.replace(BLOCK, BLOCK + "        continue-on-error: true\n"), "continue_on_error"),
        "b": (lambda v: v.replace("run: python .claude/dev/packet_loop_test.py\n", "run: python .claude/dev/packet_loop_test.py | cat\n"),
              "ong_khong_pipefail"),
        "c": (lambda v: v.replace(BLOCK, BLOCK + "        shell: zsh\n"), "shell_la"),
        "e": (lambda v: v.replace(BLOCK, BLOCK + "        env:\n          LA: '1'\n"), "env_buoc_ngoai_tap"),
        "f": (lambda v: sau(v, "  gate-packet-loop:", '      PYTHONUTF8: "1"\n', '      PYTHONUTF8: "1"\n      CONG_CU_TEST_BAN_KINH: x\n'),
              "env_hoac_defaults_job"),
        "f′": (lambda v: v.replace("\njobs:\n", "\nenv:\n  X: '1'\njobs:\n", 1), "env_hoac_defaults_workflow"),
        "g": (lambda v: v.replace(BLOCK, "      - name: ghi env\n        run: echo X=1 >> $GITHUB_ENV\n" + BLOCK), "buoc_truoc_ghi_github_env"),
    }
    for ten, (sua, ly) in loai.items():
        ky(text, bien_the_yaml(p, sua), "not_measured", ly, ten)
    ky(text, bien_the_yaml(p, None, sha="0" * 40), "not_measured", "khong_doc_duoc_workflow", "d")
    q = copy.deepcopy(p)
    q["moc"]["checkout"][3]["sha"] = "1" * 40
    ky(text, q, "not_measured", "khong_xac_dinh_sha_checkout", "h")


@ca
def a14d_k7_yaml_duong():
    text, p = f_ok()
    sua = (lambda v: v.replace(BLOCK + "        run: python .claude/dev/packet_loop_test.py\n",
                               BLOCK + "        shell: bash\n        run: python .claude/dev/packet_loop_test.py | cat\n"))
    ky(text, bien_the_yaml(p, sua), "passed", ten="i")
    bang("CI_DANG_KY_SU_KIEN" in ci_goc() and "conclusion=success\n    BUOC [test registry" in text, "j: bước registry có env thật")
    ky(text, p, "passed", ten="j")


@ca
def a15_f_that():
    text, p = f_ok()
    tt, ly = kq(text, p)
    J_ = [j for j in p["moc"]["gate_output"]["jobs"] if j["name"] != "chuan-bi"]
    bang(tt == "passed" and len(J_) == 22 and text.count("  STEP ") == 43, f"F-that: {tt} {ly[:4]} {len(J_)} {text.count('  STEP ')}")


@ca
def a16_dong_la():
    text, p = f_ok()
    ky(text.replace("MOC_GATE_OUTPUT", "DONG LA\nMOC_GATE_OUTPUT"), p, "not_measured", "dinh_dang", "a")
    cb = jb(p, "chuan-bi")
    dc = [d for d in text.split("\n") if d.startswith(f"JOB {cb['job_id']} ")][0]
    ten = next(b["name"] for b in cb["buoc"] if b["conclusion"] == "success" and b["name"].startswith("phan loai"))
    ky(text.replace(dc, dc + f"\n  STEP name={json.dumps(ten, ensure_ascii=False)} conclusion=success"), p, "not_measured", "dinh_dang", "b")
    q = copy.deepcopy(p)
    w = dict(copy.deepcopy(jb(p, "gate-ops (ubuntu-latest)")), job_id=7, name="gate-ops (windows-latest)", labels=["windows-latest"])
    q["moc"]["gate_output"]["jobs"].append(w)
    q["log_day_du"][7] = q["log_day_du"][jb(p, "gate-ops (ubuntu-latest)")["job_id"]]
    t2 = van(q).replace('-> ngoai_pham_vi_os', '-> ngoai_pham_vi_os\n  STEP name="don-nhanh selftest (chốt xoá nhánh)" conclusion=success')
    ky(t2, q, "not_measured", "dinh_dang", "c")


# ---------- lời khai, neo, phạm vi land, owner_waived (cây hồ sơ tạm) ----------
GO2 = "gate-output2-42032872356-a1.txt"


def ho_so(cay_yaml, tep=None, url_hop_le=None, lien_ket=None):
    """Cây tạm `ops/land/pr9001-x-land-evidence.yaml` + `pr9001-x-provenance/` (tep: {đường dẫn: nội dung | None ⇒ không thư mục})."""
    text, p = f_ok()
    tep = {"provenance.yaml": yaml.safe_dump(p, allow_unicode=True), GO2: text} if tep is None else tep
    with tempfile.TemporaryDirectory(prefix="go2_hs_") as d:
        land = Path(d) / "ops/land"
        (land / "pr9001-x-provenance").mkdir(parents=True)
        for k, v in tep.items():
            (land / "pr9001-x-provenance" / k).parent.mkdir(parents=True, exist_ok=True)
            (land / "pr9001-x-provenance" / k).write_text(v, encoding="utf-8")
        if tep == {}:
            (land / "pr9001-x-provenance").rmdir()
        for ten, dich in (lien_ket or {}).items():   # symlink: "" ⇒ chính thư mục provenance
            (land / "pr9001-x-provenance" / ten if ten else land / "pr9001-x-provenance").symlink_to(dich)
        return nap().kiem_ho_so_gate_output(land / "pr9001-x-land-evidence.yaml", cay_yaml, goc(), url_hop_le)


def mot(cay_yaml, **kw):
    r = ho_so(cay_yaml, **kw)
    bang(len(r) == 1, f"đòi đúng một lời khai, được {r}")
    return r[0]


RUN = 42032872356


@ca
def a17_loi_khai():
    cay = {"gate_output": "measured …", "moc_gate_output": "passed", "Gate Output": "Measured x", "GateOutput": "passed",
           "gate_output_nguon": "x", "moc_gate_output_rc_disposition": "x", "a": {"moc_gate_output": {"trang_thai": "passed"}},
           "b": {"moc_gate_output": ["a"]}, "c": {"moc_gate_output": "23/23 job success"}, "d": {"gate_output": f"measured, {GO2}"}}
    r = {x["duong_dan"]: x for x in ho_so(cay)}
    bang(set(r) == {"$.gate_output", "$.moc_gate_output", "$.Gate Output", "$.GateOutput", "$.a.moc_gate_output", "$.b.moc_gate_output",
                    "$.c.moc_gate_output", "$.d.gate_output"}, f"tập lời khai: {sorted(r)}")
    bang(all(not r[k]["hop_le"] and "dinh_dang_loi_khai" in r[k]["ly_do"] for k in ("$.a.moc_gate_output", "$.b.moc_gate_output",
                                                                                         "$.c.moc_gate_output")), "mapping/list/tự do phải ĐỎ")
    bang(r["$.d.gate_output"]["token"] == "measured" and r["$.Gate Output"]["token"] == "measured", "token dương")


def neo_map(**kw):
    return {"run_id": RUN, "run_attempt": 1, "sha": SHA_CK, "gate_output": f"measured — {GO2}"} | kw


@ca
def a18_neo_trich_tep():
    bang(mot(neo_map())["hop_le"], "a: neo cùng mapping khớp")
    for ten, kw in (("b", {"run_id": RUN + 1}), ("c", {"run_attempt": 2}), ("e", {"sha": "1" * 40})):
        bang(not mot(neo_map(**kw))["hop_le"], ten)
    bang(mot({k: v for k, v in neo_map().items() if k != "run_attempt"})["ly_do"] == ["thieu_neo"], "d")
    bang(mot({"run_id": RUN, "run_attempt": 1, "sha": SHA_CK, "con": {"gate_output": f"measured — {GO2}"}})["ly_do"] == ["thieu_neo"], "f")
    moc = {"merge_commit": SHA_CK, "ci_master": {"run_id": RUN, "run_attempt": 1},
           "moc_10_2_2": {"run": "x", "checkout": "x", "workflow_definition": "x", "gate_output": f"measured — {GO2}"}}
    bang(mot(moc)["hop_le"], "g: moc_10_2_2 + ci_master")
    bang(not mot(dict(moc, merge_commit="2" * 40))["hop_le"], "h")
    bang(mot(neo_map(gate_output="measured — kiem-gate-output.txt"))["ly_do"] == ["chi_ket_luan_check_run"], "i")
    bang(mot(neo_map(), tep={})["ly_do"] == ["khong_co_provenance"], "j")
    bang(mot(neo_map(), tep={"x.yaml": "a: 1\n"})["ly_do"] == ["khong_co_provenance"], "k")
    text, p = f_ok()
    tep = {"provenance.yaml": yaml.safe_dump(p, allow_unicode=True), f"../x/{GO2}": text}
    bang(not mot(neo_map(gate_output=f"measured — ../x/{GO2}"), tep=tep)["hop_le"], "l: thoát thư mục provenance")
    for ten in (f"tien-to-{GO2}", "gate-output2-1-a9.txt"):   # (m) F02: tên phải đúng `gate-output2-<run>-a<attempt>.txt` của header
        tep = {"provenance.yaml": yaml.safe_dump(p, allow_unicode=True), ten: text}
        bang(not mot(neo_map(gate_output=f"measured — {ten}"), tep=tep)["hop_le"], f"m: tên {ten}")
    with tempfile.TemporaryDirectory(prefix="go2_sl_") as d:   # (n) symlink ở tệp; (o) symlink ở CHÍNH thư mục provenance
        (Path(d) / GO2).write_text(text, encoding="utf-8")
        (Path(d) / "provenance.yaml").write_text(yaml.safe_dump(p, allow_unicode=True), encoding="utf-8")
        r = ho_so(neo_map(), tep={"provenance.yaml": yaml.safe_dump(p, allow_unicode=True)}, lien_ket={GO2: Path(d) / GO2})
        bang(len(r) == 1 and not r[0]["hop_le"], f"n: symlink tệp {r}")
        r = ho_so(neo_map(), tep={}, lien_ket={"": Path(d)})
        bang(len(r) == 1 and not r[0]["hop_le"], f"o: symlink thư mục provenance {r}")


def url_ok(u):
    return u.startswith(TIEN_TO) and "#issuecomment-" in u


RB_ID = 6635057729
RB = LAND / f"pr1130-wp1122-provenance/readback-duyet-issuecomment-{RB_ID}.json"
URL_RB = f"https://github.com/ducthangho/tra-luat/pull/1130#issuecomment-{RB_ID}"


def waiver(chuoi=None, body=None, **rb):
    rbj = json.loads(RB.read_text(encoding="utf-8"))
    rbj["body"] = (f"Miễn.\nmien_gate_output: {SHA_CK} os=ubuntu-latest ly_do=duong_nhanh han=2026-12-31\n" if body is None else body)
    rbj |= rb
    cay = {"run_id": RUN, "run_attempt": 1, "sha": SHA_CK, "gate_output":
           chuoi if chuoi is not None else f"owner_waived — {URL_RB} {SHA_CK} miễn vì đường nhanh hồ sơ"}
    text, p = f_ok()
    tep = {"provenance.yaml": yaml.safe_dump(p, allow_unicode=True), f"readback-x-issuecomment-{RB_ID}.json": json.dumps(rbj)}
    return mot(cay, tep=tep, url_hop_le=url_ok)


@ca
def a19_owner_waived():
    bang(waiver()["hop_le"], f"a: hợp lệ {waiver()['ly_do']}")
    url = URL_RB
    sai = {"b": dict(chuoi=f"owner_waived — {url} {url[:-1]}1 {SHA_CK} miễn vì đường nhanh hồ sơ"),
           "c": dict(chuoi=f"owner_waived — {url} {'3' * 40} miễn vì đường nhanh hồ sơ"),
           "d": dict(chuoi=f"owner_waived — {url} {SHA_CK}"),
           "f": dict(html_url=url + "0"), "g": dict(author_association="COLLABORATOR"), "h": dict(body="duyệt merge, không miễn"),
           "i": dict(body=json.loads(RB.read_text(encoding="utf-8"))["body"] + f"\nSHA {SHA_CK}"),
           "j": dict(body=f"mien_gate_output: {'4' * 40} os=ubuntu-latest ly_do=x han=2026-12-31"),
           "k": dict(body=f"mien_gate_output: {SHA_CK} os=windows-latest ly_do=x han=2026-12-31"),
           "l": dict(body=f"mien_gate_output: {SHA_CK} os=ubuntu-latest ly_do=x han=2026-02-30"),
           "m": dict(body=f"mien_gate_output: {SHA_CK} os=ubuntu-latest ly_do=x han=2026-12-31\n" * 2),
           "n": dict(body=f"xem mien_gate_output: {SHA_CK} os=ubuntu-latest ly_do=x han=2026-12-31")}
    for ten, kw in sai.items():
        r = waiver(**kw)
        bang(not r["hop_le"] and "waiver_khong_co_can_cu" in r["ly_do"], f"{ten}: {r['ly_do']}")
    text, p = f_ok()   # (e) không có readback
    r = mot({"run_id": RUN, "run_attempt": 1, "sha": SHA_CK, "gate_output": f"owner_waived — {url} {SHA_CK} miễn vì đường nhanh"},
            tep={"provenance.yaml": yaml.safe_dump(p, allow_unicode=True)}, url_hop_le=url_ok)
    bang(not r["hop_le"], f"e: {r['ly_do']}")


@ca
def a20_so_luat():
    m = nap()
    bang(all(k == m.bam(v) for k, v in m.LUAT_PHIEN_BAN.items()) and not m.kiem_so_luat(), "a: khoá = băm, sổ lành")
    bang(m.MIEN_HIEU_LUC == KY_VONG_SO and set(m.LUAT_PHIEN_BAN) == set(KY_VONG_SO), f"b: bản chép riêng {m.MIEN_HIEU_LUC}")
    tinh = "LUAT_PHIEN_BAN = {bam(LUAT_v1): LUAT_v1}\nMIEN_HIEU_LUC = {bam(LUAT_v1): (1, None)}\n"
    for ten, them, ly in (
            ("c", "LUAT_PHIEN_BAN = {'0' * 64: LUAT_v1}\nMIEN_HIEU_LUC = {'0' * 64: (1, None)}\n", "khoa_khac_bam"),
            ("d", SO_V2.format(r=1).replace("(1, 1 - 1)", "(1, 5)"), "mien_chong"),
            ("e", SO_V2.format(r=10).replace("(1, 10 - 1)", "(1, None)").replace("(10, None)", "(20, None)"), "mien_mo_khac_1"),
            ("f", "LUAT_v1['JOB_BAT_BUOC'].append('gate (ubuntu-latest)')\n" + tinh, "job_bat_buoc_trung"),
            ("g", "LUAT_v1['JOB_BAT_BUOC'].remove('gate-ops (ubuntu-latest)')\n" + tinh, "mien_mo_thieu_check_bat_buoc"),
            ("h", "LUAT_v1['JOB_BAT_BUOC'].append('khac (ubuntu-latest)')\n" + tinh, "job_khong_dung_mot_muc"),
            ("i", "LUAT_v1['JOB_BAT_BUOC'].pop()\n", "khoa_khac_bam"),
            ("j", "MIEN_HIEU_LUC = {}\n", "khoa_thieu_mien")):
        loi = ban_sao(them).kiem_so_luat()
        bang(any(x.startswith(ly) for x in loi), f"{ten}: mong {ly}, được {loi}")
        text, p = f_ok()
        bang(ban_sao(them).kiem(text, p, goc())[1][:1] == ["so_luat_hong"], f"{ten}: kiem phải so_luat_hong")
    g = ban_sao("LUAT_v1['JOB_BAT_BUOC'].remove('gate-ops (ubuntu-latest)')\nLUAT_PHIEN_BAN = {bam(LUAT_v1): LUAT_v1}\n"
                "MIEN_HIEU_LUC = {bam(LUAT_v1): (1, 5)}\nLUAT_v2 = dict(LUAT_v1, JOB_BAT_BUOC=LUAT_v1['JOB_BAT_BUOC'] + ['gate-ops "
                "(ubuntu-latest)'], ghi_chu='v2')\nLUAT_PHIEN_BAN[bam(LUAT_v2)] = LUAT_v2\nMIEN_HIEU_LUC[bam(LUAT_v2)] = (6, None)\n")
    bang(not g.kiem_so_luat(), f"G03: miền ĐÓNG thiếu CHECK_BAT_BUOC không làm sổ hỏng: {g.kiem_so_luat()}")
    dong = re.search(r"^CHECK_BAT_BUOC = .*$", (ROOT / ".claude/dev/packet_loop.py").read_text(encoding="utf-8"), re.M)[0]
    bang(tuple(f"{j} (ubuntu-latest)" for j in re.findall(r'"([\w-]+)"', dong.split(" for j in ")[1])) == m.CHECK_BAT_BUOC,
         f"bản chép CHECK_BAT_BUOC lệch packet_loop.py: {dong[:90]}")


@ca
def a21_pham_vi_land():
    text, p = f_ok()

    def land(sua_p=None, cay=None, prov=True):
        q = copy.deepcopy(p)
        (sua_p or (lambda q: None))(q)
        tep = {"provenance.yaml": yaml.safe_dump(q, allow_unicode=True), GO2: text} if prov else {GO2: text, "x.yaml": "schema: khac\n"}
        return [x["la_land"] for x in ho_so(cay or {"merge_commit": SHA_CK, "pmc": neo_map()}, tep=tep)]
    bang(land() == [True], "a: ci.yml push, head ∈ H")
    bang(land(lambda q: q["moc"]["run"].update(loi_khai_rest_path=".github/workflows/launcher-windows.yml")) == [False], "b")
    bang(land(prov=False) == [True], "c: không có provenance cho run ⇒ land (fail-closed)")
    bang(nap().tap_head_land({"prs": [{"merge_commit": "a" * 40}, {"merge_commit": "b" * 40}]}) == {"a" * 40, "b" * 40}, "d")
    bang(land(lambda q: q["moc"]["run"].update(event="workflow_dispatch")) == [False], "e: dispatch cùng head")
    am = {"merge_commit": SHA_CK, "pmc": neo_map(gate_output="not_measured — chưa đo")}   # (f) lời khai land âm ⇒ KHÔNG hợp lệ (Q8)
    r = ho_so(am)
    bang(len(r) == 1 and r[0]["la_land"] and not r[0]["hop_le"], f"f: {r}")
    q = copy.deepcopy(p)
    q["moc"]["run"]["event"] = "workflow_dispatch"
    r = ho_so(am, tep={"provenance.yaml": yaml.safe_dump(q, allow_unicode=True)})
    bang(len(r) == 1 and not r[0]["la_land"] and r[0]["hop_le"], f"g: lời khai PHỤ được not_measured {r}")


@ca
def a22_mot_chieu_phu_thuoc():
    """Danh sách CHO PHÉP (G02 vòng 6): mọi `.py`/`.pyc` dưới gốc cây được mở phải thuộc module + `ci_provenance` (cả `.pyc`)."""
    with tempfile.TemporaryDirectory(prefix="go2_a22_") as d:
        ops = Path(d) / "ops"
        ops.mkdir()
        for t in ("ci_provenance.py", "kiem_ho_so_land.py", "land_evidence_nguon.py"):
            shutil.copy(ROOT / "ops" / t, ops / t)
        doi = {"duong": "", "1": f"import sys as _s\n_s.path.insert(0, {d!r})\nimport ops.kiem_ho_so_land\n",
               "2": "import importlib.util as _u\n_x = _u.spec_from_file_location('x', Path(__file__).with_name('kiem_ho_so_land.py'))\n"
                    "_x.loader.exec_module(_u.module_from_spec(_x))\n",
               "3": "import runpy\nrunpy.run_path(str(Path(__file__).with_name('kiem_ho_so_land.py')))\n",
               "4": "_p = Path(__file__).with_name('kiem_ho_so_land.py')\nexec(compile(open(_p).read(), str(_p), 'exec'), {})\n",
               "5": "import runpy, importlib.util as _u\nrunpy.run_path(_u.cache_from_source(str(Path(__file__).with_name('kiem_ho_so_land.py'))))\n",
               "6": "import sys as _s\n_s.path.insert(0, str(Path(__file__).parent))\nimport kiem_ho_so_land\n"}
        text, p = f_ok()
        hs = Path(d) / "hs"   # F05: tiến trình con gọi CẢ `kiem_ho_so_gate_output` trên cây hồ sơ dương (tệp `.yaml`/`.txt`, ngoài tập đo)
        (hs / "pr9001-x-provenance").mkdir(parents=True)
        (hs / "pr9001-x-provenance/provenance.yaml").write_text(yaml.safe_dump(p, allow_unicode=True), encoding="utf-8")
        (hs / "pr9001-x-provenance" / GO2).write_text(text, encoding="utf-8")
        (Path(d) / "vao.json").write_text(json.dumps({"text": text, "p": p, "goc": str(goc()), "hs": str(hs), "cay": neo_map()}),
                                          encoding="utf-8")
        kq_ = {}
        for ten, them in doi.items():
            (ops / "gate_output_doi_chieu.py").write_text(MA.read_text(encoding="utf-8") + "\n" + them, encoding="utf-8")
            for f in ops.rglob("*.pyc"):
                f.unlink()
            subprocess.run([sys.executable, "-m", "compileall", "-q", str(ops)], check=True, capture_output=True)
            env = {k: v for k, v in os.environ.items() if k not in ("PYTHONDONTWRITEBYTECODE", "PYTHONPYCACHEPREFIX")}
            r = subprocess.run([sys.executable, "-c", CON_A22, d], capture_output=True, env=env, timeout=120)
            kq_[ten] = json.loads(r.stdout or b"{}")
        bang(kq_["duong"].get("cho_phep") == [] and kq_["duong"].get("ok"), f"dương phải sạch: {kq_['duong']}")
        bang(all(kq_[k].get("cho_phep") for k in "123456"), f"mọi đối chứng phải bị danh sách cho phép bắt: {kq_}")
        bang(not all(kq_[k].get("cam_py") for k in "123456"), f"đối chứng phải có ca danh sách cấm `.py` (r6) lọt: {kq_}")


CON_A22 = r"""
import json, sys, os
from pathlib import Path
goc = Path(sys.argv[1]).resolve()
ops = goc / "ops"
cho = {str(ops / t) for t in ("gate_output_doi_chieu.py", "ci_provenance.py")}
mo = []
def ghi(x):   # chỉ `.py`/`.pyc` DƯỚI gốc cây được đo (cả ba lớp dùng chung)
    try:
        q = Path(os.fsdecode(x)).resolve()
    except (OSError, ValueError, TypeError):
        return
    if q.is_relative_to(goc) and q.suffix in (".py", ".pyc"):
        mo.append(str(q))
def hook(ev, a):
    if ev == "open" and isinstance(a[0], (str, bytes, os.PathLike)):
        ghi(a[0])
sys.addaudithook(hook)
import importlib.machinery, importlib.util
_em, _sf = importlib.machinery.SourceFileLoader.exec_module, importlib.util.spec_from_file_location
def em(self, mod):   # lớp 1–2: ghi mọi đường dẫn nguồn được thực thi / được tạo spec
    ghi(self.path); return _em(self, mod)
def sf(name, loc=None, *a, **k):
    if loc is not None: ghi(loc)
    return _sf(name, loc, *a, **k)
importlib.machinery.SourceFileLoader.exec_module, importlib.util.spec_from_file_location = em, sf
mo.clear()
ok = True
try:
    s = importlib.util.spec_from_file_location("gate_output_doi_chieu", ops / "gate_output_doi_chieu.py")
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    v = json.loads((goc / "vao.json").read_text(encoding="utf-8"))
    p = v["p"]; p["log_day_du"] = {int(k): x for k, x in p["log_day_du"].items()}
    ok = m.kiem(v["text"], p, v["goc"])[0] == "passed"
    r = m.kiem_ho_so_gate_output(Path(v["hs"]) / "pr9001-x-land-evidence.yaml", v["cay"], v["goc"], lambda u: True)
    ok = ok and len(r) == 1 and r[0]["hop_le"]
except Exception:
    ok = False
def duoc(q):
    q = Path(q)
    return str(q) in cho or (q.parent.name == "__pycache__" and q.parent.parent == ops and q.name.split(".")[0] in
                             ("gate_output_doi_chieu", "ci_provenance"))
f = [str(Path(x.__file__).resolve()) for x in list(sys.modules.values()) if getattr(x, "__file__", None)]
f = [x for x in f if Path(x).is_relative_to(goc)]
cam = {str(ops / "kiem_ho_so_land.py"), str(ops / "land_evidence_nguon.py")}
print(json.dumps({"ok": ok, "cho_phep": sorted({q for q in mo + f if not duoc(q)}), "cam_py": sorted({q for q in mo + f if q in cam})}))
"""


@ca
def p1127_phan_chung():
    """Ba trạng thái hồ sơ #1127 (commit bb47274, 936744e, 7f22121) ⇒ ĐỎ; bản sửa của 7f22121 với provenance F-ok ⇒ ĐẠT (đo LUẬT)."""
    for c in ("bb47274", "936744e", "7f22121"):
        cay = yaml.safe_load(git("show", f"{c}:ops/land/pr1127-wp1120-land-evidence.yaml", cwd=ROOT))
        with tempfile.TemporaryDirectory(prefix="go2_1127_") as d:
            tar = subprocess.run(["git", "-C", str(ROOT), "archive", c, "ops/land/pr1127-wp1120-provenance"], capture_output=True, check=True)
            subprocess.run(["tar", "-x", "-C", d], input=tar.stdout, check=True)
            land = Path(d) / "ops/land"
            r = nap().kiem_ho_so_gate_output(land / "pr1127-wp1120-land-evidence.yaml", cay, goc(), url_ok)
        bang(r and not all(x["hop_le"] for x in r), f"{c}: phải ĐỎ, được {r}")
    cay = yaml.safe_load(git("show", "7f22121:ops/land/pr1127-wp1120-land-evidence.yaml", cwd=ROOT))
    cay["merge_commit"] = SHA_CK
    cay["post_merge_checks"][0].update(run_id=RUN, run_attempt=1, sha=SHA_CK, moc_gate_output=f"measured — {GO2}")
    r = ho_so(cay)
    bang(r and all(x["hop_le"] for x in r), f"vế dương: {r}")


@ca
def a23_cli():
    text, p = f_ok()
    with tempfile.TemporaryDirectory(prefix="go2_cli_") as d:
        (Path(d) / "p.yaml").write_text(yaml.safe_dump(p, allow_unicode=True), encoding="utf-8")
        (Path(d) / GO2).write_text(text, encoding="utf-8")
        r = subprocess.run([sys.executable, "-B", str(MA), "kiem", "--provenance", str(Path(d) / "p.yaml"), "--goc", str(goc()),
                            str(Path(d) / GO2)], capture_output=True)
        r2 = subprocess.run([sys.executable, "-B", str(MA), "sai"], capture_output=True)
        (Path(d) / "hong.yaml").write_text("schema: ci_provenance/1\nmoc: x\n", encoding="utf-8")   # F06: dữ liệu hỏng ⇒ rc 2
        r3 = subprocess.run([sys.executable, "-B", str(MA), "kiem", "--provenance", str(Path(d) / "hong.yaml"), "--goc", str(goc()),
                             str(Path(d) / GO2)], capture_output=True)
        land = Path(d) / "ops/land"   # F03: owner_waived qua CLI (không có url_hop_le) ⇒ KHÔNG ĐO ĐƯỢC, rc 2
        (land / "pr9001-x-provenance").mkdir(parents=True)
        (land / "pr9001-x-land-evidence.yaml").write_text(yaml.safe_dump(
            neo_map(gate_output=f"owner_waived — {URL_RB} {SHA_CK} miễn vì đường nhanh hồ sơ")), encoding="utf-8")
        r4 = subprocess.run([sys.executable, "-B", str(MA), "kiem-ho-so", "--root", str(goc()), str(land / "pr9001-x-land-evidence.yaml")],
                            capture_output=True)
    bang(r.returncode == 0 and b"GATE_OUTPUT: passed" in r.stdout and r2.returncode == 2, f"CLI: {r.returncode} {r.stdout[-200:]}")
    bang(r3.returncode == 2 and b"Traceback" not in r3.stderr, f"CLI dữ liệu hỏng: {r3.returncode} {r3.stdout[-120:]} {r3.stderr[-200:]}")
    bang(r4.returncode == 2 and "KHÔNG ĐO ĐƯỢC".encode() in r4.stdout, f"CLI waiver: {r4.returncode} {r4.stdout[-200:]}")


@ca
def a24_du_lieu_sai_kieu():
    """F06: mapping lồng sai kiểu ⇒ `not_measured` có lý do, không ném ngoại lệ (API)."""
    text, p = f_ok()
    for ten, sua in (("moc", lambda q: q.update(moc="x")), ("run", lambda q: q["moc"].update(run="x")),
                     ("gate_output", lambda q: q["moc"].update(gate_output="x")), ("jobs", lambda q: q["moc"]["gate_output"].update(jobs="x")),
                     ("log", lambda q: q["log_day_du"].update({k: "x" for k in q["log_day_du"]})),
                     ("labels", lambda q: jb(q, "gate (ubuntu-latest)").update(labels="ubuntu-latest")),
                     ("checkout", lambda q: q["moc"].update(checkout="x"))):
        q = copy.deepcopy(p)
        sua(q)
        try:
            tt = kq(text, q)[0]
            r = ho_so(neo_map(), tep={"provenance.yaml": yaml.safe_dump(q, allow_unicode=True), GO2: text})
        except Exception as e:   # ngoại lệ ở đây CHÍNH là lỗi đang canh ⇒ tín hiệu chốt, không phải lỗi vô can
            bang(False, f"{ten}: ném {type(e).__name__}: {e}")
        bang(tt == "not_measured" and len(r) == 1 and not r[0]["hop_le"], f"{ten}: {tt} {r}")
    bang(kq(text, ["x"])[0] == "not_measured" and kq(None, p)[0] == "not_measured", "provenance/tệp không phải dict/chuỗi")


DOT_BIEN = (   # (tên, chuỗi gốc, chuỗi thay, TIỀN TỐ ca đích). Chuỗi gốc phải xuất hiện ĐÚNG MỘT lần trong module.
    ("m-A1_kiem_luon_not_measured", '    if loi := kiem_so_luat():\n        return "not_measured", ["so_luat_hong", *loi]',
     '    return "not_measured", ["db"]', "a01"),
    ("m-A2_bo_K4", '            nm.append(f"bam_log:{j[\'id\']}")', "            pass", "a02"),
    ("m-A3a_bo_so_tap", "if len(ids) != len(set(ids)) or set(ids) != set(tp) or set(tp) != set(log):", "if False:", "a03"),
    ("m-A3b_bo_J_khac_rong", "    if not jj:\n", "    if False:\n", "a03"),
    ("m-A3c_bo_checkout_tung_job", 'if not any(c.get("job_id") == j["id"] and c.get("sha") in sha for c in co):', "if False:", "a03"),
    ("m-A3d_go_chot_du_job", 'for t in luat["JOB_BAT_BUOC"] if ten_j.count(t) == 0]', 'for t in [] if ten_j.count(t) == 0]', "a03"),
    ("m-A3e_chi_nam_ten_check", 'for t in luat["JOB_BAT_BUOC"] if ten_j.count(t) == 0]', 'for t in CHECK_BAT_BUOC if ten_j.count(t) == 0]',
     "a03"),
    ("m-A3f_nhan_ten_trung", "if ten_j.count(t) > 1]", "if False]", "a03"),
    ("m-A3g_bo_job_ngoai_luat", 'if t not in luat["JOB_BAT_BUOC"]]', "if False]", "a03"),
    ("m-A3k_chot_du_job_chi_khi_chua_co_ly_do", 'for t in luat["JOB_BAT_BUOC"] if ten_j.count(t) == 0]',
     'for t in luat["JOB_BAT_BUOC"] if ten_j.count(t) == 0 and not nm]', "a03k"),
    ("m-A3h_bo_chot_id_trung", '    if len({j.get("job_id") for j in ds}) != len(ds):', "    if False:", "a03"),
    ("m-A4a_bo_so_name", '(j["name"], j["labels"], j["conclusion"]) != (p.get("name"), p.get("labels"), p.get("conclusion"))',
     '(j["labels"], j["conclusion"]) != (p.get("labels"), p.get("conclusion"))', "a04"),
    ("m-A4b_conclusion_tu_tep", '        if p.get("conclusion") != "success":', '        if j["conclusion"] != "success":', "a04"),
    ("m-A4c_bo_so_labels", '(j["name"], j["labels"], j["conclusion"]) != (p.get("name"), p.get("labels"), p.get("conclusion"))',
     '(j["name"], j["conclusion"]) != (p.get("name"), p.get("conclusion"))', "a04"),
    ("m-A5_fullmatch_thanh_search", 'not any(re.fullmatch(r, x) for x in thuong)', "not any(re.search(r, x) for x in thuong)", "a05"),
    ("m-A6_mot_dau_hieu_bat_ky", '    loi, thuong = [], [nd for lo, nd in buoc if lo == ""]',
     '    if buoc:\n        return []\n    loi, thuong = [], [nd for lo, nd in buoc if lo == ""]', "a06"),
    ("m-A7_bo_backreference", r'r"== gen_instructions selftest (\d+)/\1 =="', r'r"== gen_instructions selftest (\d+)/\d+ =="', "a07"),
    ("m-A8a_bo_so_neo_run", 'if (int(dau[1]), int(dau[2]), dau[3]) != (run.get("run_id"), pv.get("attempt_yeu_cau"), run.get("head_sha")):',
     "if False:", "a08"),
    ("m-A8b_bo_trang_thai_repo", 'if run.get("trang_thai") != "passed" or run.get("repo") != "ducthangho/tra-luat":', "if False:", "a08"),
    ("m-A8c_nhan_pull_request", 'not in ("push", "workflow_dispatch"):', 'not in ("push", "workflow_dispatch", "pull_request"):', "a08"),
    ("m-A9a_chi_mien_mo", 'not (a <= run["run_id"] and (z is None or run["run_id"] <= z))', "z is not None", "a09"),
    ("m-A9b_bo_kiem_mien", 'not (a <= run["run_id"] and (z is None or run["run_id"] <= z))', "False", "a09"),
    ("m-A10_xet_dong_dau", "re.fullmatch(r, cu[-1])", "re.fullmatch(r, cu[0])", "a10"),
    ("m-A11_bo_KHONG", 'elif loai == "KHONG" and [nd for lo, nd in buoc if lo == "KHONG"] != ["0"]:', "elif False:", "a11"),
    ("m-A12_ok_moi_do_sau", 'v.get("ok") is True', "'\"ok\": true' in js[0]", "a12"),
    ("m-A13a_bo_so_step_buoc", '            nm.append(f"step_khong_trong_buoc:{s[\'name\'][:30]}")', "            pass", "a13"),
    ("m-A13b_bo_conclusion_buoc", 'elif rb[0].get("conclusion") != "success":', "elif False:", "a13"),
    ("m-A13c_nhan_nhieu_step", "        if len(st) != 1:\n            nm.append(f\"thieu_hoac_lap_buoc", "        if not st:\n            nm.append(f\"thieu_hoac_lap_buoc",
     "a13"),
    ("m-A14a_bo_coe", '    if s.get("continue-on-error", False) is not False:', "    if False:", "a14"),
    ("m-A14b_bo_pipefail", "and RE_ONG.search(_bo_nhay(str(y.get(\"run\", \"\"))))", "and False", "a14"),
    ("m-A14c_bo_shell", '    if s.get("shell", "bash") not in ("bash", "pwsh", "sh"):', "    if False:", "a14"),
    ("m-A14d_bo_wf_khong_doc", '        nm += [] if wf else ["khong_doc_duoc_workflow"]', "        pass", "a14"),
    ("m-A14e_bo_env_buoc", 'not set(s["env"]) <= set(env_buoc)', "False", "a14"),
    ("m-A14f_bo_env_job_workflow", ' or not set(d.get("env") or {}) <= set(env_job):', ":", "a14"),
    ("m-A14g_bo_github_env", 'if any(re.search("GITHUB_(ENV|PATH)", str(t.get("run", ""))) for t in jb["steps"][:i]):', "if False:", "a14"),
    ("m-A14h_nhan_nhieu_sha", "    if len(sha) != 1:\n", "    if not sha:\n", "a14"),
    ("m-A14i_bash_khong_pipefail", 'y.get("shell") in (None, "sh")', 'y.get("shell") in (None, "sh", "bash")', "a14d"),
    ("m-A14j_goi_chan_buoc", 'chan_k7(wf, k, sy[0], lb["env"] if lb else [], luat["ENV_JOB_CHO_PHEP"])',
     '("chan_buoc" if cp.chan_buoc(wf, k, sy[0]) else None)', "a14d"),
    ("m-A15a_so_Run_lenh", 'cp.ten_du_kien(y) == s["name"]', '"Run " + str(y.get("run", "")).split("\\n")[0] == s["name"]', "a15"),
    ("m-A16_bo_K9", '            raise ValueError("dong_la")', "            continue", "a16"),
    ("m-A16b_nhan_step_ngoai_J", '            if j["steps"] or j["mui"] != mui:', '            if j["mui"] != mui:', "a16"),
    ("m-A17a_bo_bo_ky_tu", "if c.isalnum())", "if c.isalnum() or c == ' ')", "a17"),
    ("m-A17b_cho_mapping_list", '        if tok is None:\n            loi.append("dinh_dang_loi_khai")',
     '        if tok is None and type(gt) is str:\n            loi.append("dinh_dang_loi_khai")', "a17"),
    ("m-A18a_bo_so_run_id", "(int(d[1]), int(d[2]), d[3]) != neo", "(int(d[2]), d[3]) != neo[1:]", "a18"),
    ("m-A18b_bo_so_run_attempt", "(int(d[1]), int(d[2]), d[3]) != neo", "(int(d[1]), d[3]) != (neo[0], neo[2])", "a18"),
    ("m-A18c_bo_so_head", "(int(d[1]), int(d[2]), d[3]) != neo", "(int(d[1]), int(d[2])) != neo[:2]", "a18"),
    ("m-A18d_cho_thua_ke", 'yield f"{duong}.{k}", x, _neo(v, cha)', 'yield f"{duong}.{k}", x, _neo(v, cha) or (type(cha) is dict and _neo(cha, None)) or None',
     "a18"),
    ("m-A18e_bo_nhanh_moc", "if MOC_10_2_2 <= set(m) and", "if False and", "a18"),
    ("m-A18f_provenance_vang_la_dat", '            elif not prov:\n                loi.append("khong_co_provenance")',
     '            elif not prov:\n                pass', "a18"),
    ("m-A18h_bo_symlink_thu_muc", "for q in [p, *p.parents][:n + 1])", "for q in [p, *p.parents][:n])", "a18"),
    ("m-A18i_bo_kiem_ten_tep", '        if p.name != f"gate-output2-{d[1]}-a{d[2]}.txt":', "        if False:", "a18"),
    ("m-A18j_bo_symlink_moi_thanh_phan", "and not any(q.is_symlink() for q in [p, *p.parents][:n + 1])", "", "a18"),
    ("m-A18g_cho_thoat_thu_muc", 'not ten.startswith("/") and ".." not in Path(ten).parts and ', "", "a18"),
    ("m-A19a_bo_url", '    if len(url) != 1 or url_hop_le is None or not url_hop_le(url[0][0]):\n        loi.append("url")',
     '    if False:\n        loi.append("url")', "a19"),
    ("m-A19c_bo_sha", '    if head not in RE_SHA.findall(chuoi):', "    if False:", "a19"),
    ("m-A19d_bo_ly_do", "    if len(con.strip(\" \\t—-:;,.()\")) < 10:", "    if False:", "a19"),
    ("m-A19f_bo_html_url", '    if not url or rb.get("html_url") != url[0][0]:', "    if False:", "a19"),
    ("m-A19g_bo_chu_kho", 'if (rb.get("user") or {}).get("login") != "ducthangho" or rb.get("author_association") != "OWNER":', "if False:", "a19"),
    ("m-A19h_bo_dong_may_doc", '    if len(dong) != 1:\n        loi.append("khong_dung_mot_dong_mien_gate_output")\n    elif',
     '    if len(dong) > 1:\n        loi.append("khong_dung_mot_dong_mien_gate_output")\n    elif not dong:\n        pass\n    elif', "a19"),
    ("m-A19j_bo_so_sha_dong", "(m := RE_MIEN.fullmatch(d.strip())) and m[1] == head]", "(m := RE_MIEN.fullmatch(d.strip()))]", "a19"),
    ("m-A19k_bo_os", 'elif not set(LUAT_v1["OS_BAT_BUOC"]) <= set(dong[0][2].split(",")):', "elif False:", "a19"),
    ("m-A19l_han_regex", "datetime.date.fromisoformat(dong[0][4])", 'assert re.fullmatch(r"\\d{4}-\\d{2}-\\d{2}", dong[0][4])', "a19"),
    ("m-A19m_nhan_nhieu_dong", '    if len(dong) != 1:\n        loi.append("khong_dung', '    if not dong:\n        loi.append("khong_dung', "a19"),
    ("m-A19n_search", "(m := RE_MIEN.fullmatch(d.strip()))", "(m := RE_MIEN.search(d))", "a19"),
    ("m-A20a_sua_regex_LUAT", '_d("OK")', '_d("OK|ok")', "a20"),
    ("m-A20b_bo_kiem_so_luat", '    if loi := kiem_so_luat():\n        return "not_measured", ["so_luat_hong", *loi]', "", "a20"),
    ("m-A20c_bo_kiem_chong_mien", '    loi += ["mien_chong"] * any(', '    loi += [] * any(', "a20"),
    ("m-A20f_bo_kiem_trung", '        loi += ["job_bat_buoc_trung"] * (len(ds) != len(set(ds)))', "", "a20"),
    ("m-A20g_bo_kiem_check_bat_buoc", '            loi.append("mien_mo_thieu_check_bat_buoc")', "            pass", "a20"),
    ("m-A20g2_check_cho_moi_mien", 'if MIEN_HIEU_LUC.get(k, (0, 0))[1] is None and not', "if not", "a20"),
    ("m-A20j_bo_kiem_khoa_thieu_mien", '    loi += ["khoa_thieu_mien"] * (set(LUAT_PHIEN_BAN) != set(MIEN_HIEU_LUC))', "", "a20"),
    ("m-A20h_bo_kiem_mot_muc", '        loi += [f"job_khong_dung_mot_muc:{t}" for t in ds if len(_muc(v, t)) != 1]', "", "a20"),
    ("m-A20i_JOB_BAT_BUOC_ngoai_bam", "json.dumps(luat, ensure_ascii",
     'json.dumps({k: v for k, v in luat.items() if k != "JOB_BAT_BUOC"}, ensure_ascii', "a20"),
    ("m-A21a_chi_merge_commit_goc", ', *(_h40(p.get("merge_commit")) for p in prs if type(p) is dict)]', "]", "a21"),
    ("m-A21b_khong_provenance_khong_land", "(not pv or any(la_run_land(p) for p in pv))", "any(la_run_land(p) for p in pv)", "a21"),
    ("m-A21c_bo_event_push", ' and r.get("event") == "push"', "", "a21"),
    ("m-A21d_nhan_loi_khai_land_am", "        elif land:\n            loi.append(", "        elif False:\n            loi.append(", "a21"),
    ("m-A22_ho_so_nem_loi", '    """Mỗi lời khai: {duong_dan, token, neo, la_land, hop_le, ly_do}. L8 và L-7 tự rút kết luận."""',
     '    raise RuntimeError("db")', "a22"),
    ("m-A23a_cli_waiver_la_do", "            return 1 if do else 2 if mien else 0", "            return 1 if do or mien else 0", "a23"),
    ("m-A24_bo_kiem_kieu_mapping", "    return v if type(v) is dict else {}", "    return v or {}", "a24"),
    ("m-p1127_khong_trich_tep_la_dat", 'return ["chi_ket_luan_check_run" if re.search(r"kiem-gate|check-runs", gt) else "khong_trich_tep_gate_output"]',
     "return []", "p1127"),
)
TU_KIEM = (   # (tên, gốc, thay, ca đích, hạng mong đợi): kiểm chính bộ phân hạng
    ("vo_can_KeyError", "def kiem_so_luat():\n", "def kiem_so_luat():\n    raise KeyError('vo can')\n", "a01", "TIN_DUNG_GIA"),
    ("chi_them_chu_thich", "def la_run_land(provenance):\n", "def la_run_land(provenance):   # vo hai\n", "a21", "SONG_SOT"),
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


def chay_dot_bien(ten, cu, moi, tien_to):
    khop = [c for c in CA if c.split("_")[0] == tien_to]
    if len(khop) != 1:
        return "HONG", f"tiền tố ca đích {tien_to!r} phải khớp ĐÚNG MỘT ca, khớp {khop}"
    goc_ = (HERE / "gate_output_doi_chieu.py").read_text(encoding="utf-8")
    if goc_.count(cu) != 1 or cu == moi:
        return "HONG", f"neo phải xuất hiện đúng 1 lần và đột biến phải đổi mã (thấy {goc_.count(cu)})"
    with tempfile.TemporaryDirectory(prefix="go2_db_") as thu:
        for t in ("ci_provenance.py",):
            shutil.copy(HERE / t, Path(thu) / t)
        ban = Path(thu) / "gate_output_doi_chieu.py"
        ban.write_text(goc_, encoding="utf-8")
        rc, ra = chay_con(khop[0], ban)
        if rc != 0:
            return "HONG", f"ca đích không xanh trên bản gốc (rc={rc}): {ra[-200:]}"
        ban.write_text(goc_.replace(cu, moi), encoding="utf-8")
        rc, ra = chay_con(khop[0], ban)
        return phan_hang(rc, ra, khop[0]), ra.strip()[-200:]


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
    kq_ = [chay_ca(ten) for ten in CA]
    print("".join(f"[{dong}]\n" for rc, dong in kq_ if rc), end="")
    dat = sum(rc == 0 for rc, _ in kq_)
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
