"""Phan chung cho danh_gia_gate.py v3 (connector P2 r4629096903, PR #1419): run gia lap gom `chuan-bi` success (che_do=day_du) va
`gate (ubuntu-latest)` SKIPPED phai ra MOC_GATE_OUTPUT not_measured, khong duoc passed. Khong goi mang: thay `raw` bang du lieu gia."""
import importlib.util, io, json, os, sys, tempfile, contextlib
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "danh_gia_gate.py")
spec = importlib.util.spec_from_file_location("dgg", p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
LOG = ("2026-11-19T10:00:00.0000000Z ##[group]Run python ops/ci_duong_nhanh.py\n"
       "2026-11-19T10:00:00.0000000Z \x1b[36;1mpython ops/ci_duong_nhanh.py\x1b[0m\n"
       "2026-11-19T10:00:00.0000000Z shell: /usr/bin/bash -e {0}\n"
       "2026-11-19T10:00:00.0000000Z ##[endgroup]\n"
       "2026-11-19T10:00:01.0000000Z che_do=day_du\n").encode()
def tra(u, skipped):
    if u.endswith("/jobs?per_page=100"):
        return json.dumps({"jobs": [
            {"id": 1, "name": "chuan-bi", "conclusion": "success", "labels": ["ubuntu-latest"]},
            {"id": 2, "name": "gate (ubuntu-latest)", "conclusion": "skipped" if skipped else "success", "labels": ["ubuntu-latest"]}]}).encode()
    if u.startswith("actions/runs/"):
        return json.dumps({"run_attempt": 1, "head_sha": "0" * 40}).encode()
    if u == "actions/jobs/1/logs":
        return LOG
    raise AssertionError("khong mong doi " + u)
kq = {}
for skipped in (True,):
    m.raw = lambda u, s=skipped: tra(u, s)
    with tempfile.TemporaryDirectory() as d:
        sys.argv = ["danh_gia_gate.py", "999", os.path.join(d, "o.txt")]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            m.main()
        kq[skipped] = buf.getvalue().strip()
print("skipped:", kq[True])
ok = kq[True].startswith("MOC_GATE_OUTPUT: not_measured")
print("KET_QUA:", "DAT" if ok else "DO")
sys.exit(0 if ok else 1)
