import importlib.util
import json
import os
from pathlib import Path
import sys

OUT = Path(__file__).resolve().parent
path = Path(json.loads((OUT / "rig-3.13.json").read_text())["head"]) / ".claude/dev/launcher_test.py"
spec = importlib.util.spec_from_file_location("properties_head", path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
real_pid, real_ppid = os.getpid, os.getppid
ids = list(range(1, 65)) + [4096, 65535, 99999, 2**31 - 1]
parents = [1, 10, 11, 12, 13, 14, 15, 99999]
trials = regressions = 0
seen = []
helper = m._pid_gia_khac_minh

def checked_helper(n, tu=10):
    result = helper(n, tu)
    assert len(set(result)) == n and result == sorted(result)
    assert os.getpid() not in result and os.getppid() not in result
    seen.append((os.getpid(), os.getppid(), result))
    return result

m._pid_gia_khac_minh = checked_helper
try:
    for parent in parents:
        os.getppid = lambda parent=parent: parent
        for pid in ids:
            with m._co_lap_toan_cuc():
                os.getpid = lambda pid=pid: pid
                m._than_t81()
                trials += 1
        for pid in (1, 10, 11, 12, 13, 14, 15, 99999):
            with m._co_lap_toan_cuc():
                forced = lambda pid=pid: pid
                os.getpid = forced
                m.r766_t81_khong_phu_thuoc_pid_cua_luot_chay()
                assert os.getpid is forced
                regressions += 1
finally:
    os.getpid, os.getppid = real_pid, real_ppid
    m._pid_gia_khac_minh = helper
print(f"CROSS_PRODUCT t81={trials} r766={regressions} allocations_checked={len(seen)} failures=0", flush=True)

# Record both graphs from the actual t81 body with a collision in both exclusions.
graphs = []
loader = m._tai_launcher_thu
def graph_loader():
    launcher = loader()
    snapshot = launcher._chup_cay
    def observe(pid):
        graph = launcher._cac_pid_cha_windows()
        result = snapshot(pid)
        graphs.append({"root": pid, "parents": graph, "result": result})
        return result
    launcher._chup_cay = observe
    return launcher
m._tai_launcher_thu = graph_loader
try:
    with m._co_lap_toan_cuc():
        os.getpid = lambda: 10
        os.getppid = lambda: 11
        m._than_t81()
finally:
    m._tai_launcher_thu = loader
    os.getppid = real_ppid
assert graphs == [{"root": 13, "parents": {13: 12, 14: 13}, "result": None},
                  {"root": 13, "parents": {13: 12, 15: 13, 14: 12},
                   "result": {13: "win:123", 15: "win:456"}}]
print("GRAPHS " + json.dumps(graphs), flush=True)

body = m._than_t81
restoration = []
for cls in (m.TinHieuChotCa, RuntimeError, SystemExit, KeyboardInterrupt):
    calls = []
    def failing_body():
        calls.append(os.getpid())
        if len(calls) == 2:
            raise cls("review sentinel at second iteration")
        body()
    m._than_t81 = failing_body
    try:
        try:
            with m._co_lap_toan_cuc():
                before = os.getpid
                try:
                    m.r766_t81_khong_phu_thuoc_pid_cua_luot_chay()
                finally:
                    assert os.getpid is before
        except cls as error:
            assert len(calls) == 2
            restoration.append({"exception": cls.__name__, "calls": calls, "restored": True,
                                "message": str(error)})
        else:
            raise AssertionError("expected sentinel to escape")
    finally:
        m._than_t81 = body
print("RESTORATION " + json.dumps(restoration), flush=True)

# Exercise the normal harness and the case immediately following a failed r766.
count = [0]
def failed_body():
    count[0] += 1
    if count[0] == 2:
        raise m.TinHieuChotCa("review harness failure")
    body()
def next_case():
    assert os.getpid is real_pid
    assert os.getppid is real_ppid
m._than_t81 = failed_body
try:
    q, b, h = m.chay_bo_ca([m.r766_t81_khong_phu_thuoc_pid_cua_luot_chay, next_case])
    assert (q, b, len(h)) == (1, 0, 1)
finally:
    m._than_t81 = body
print(f"HARNESS_AFTER_FAILURE passed={q} skipped={b} failed={len(h)} next_case=PASS", flush=True)
(OUT / "evidence" / f"properties-{sys.version_info.minor}.json").write_text(json.dumps(
    {"t81": trials, "r766": regressions, "allocations": seen, "graphs": graphs,
     "restoration": restoration}, ensure_ascii=False, indent=2))
