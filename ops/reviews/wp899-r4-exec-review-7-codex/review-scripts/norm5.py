"""Tự đột biến mọi chốt mới của r4: mỗi đột biến chạy TOÀN BỘ ca trên bản sao tạm; báo SỐNG (không ca nào DO đúng chốt)."""
import json, os, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path("/tmp/claude-0/-home-user-tra-luat/eaf2a577-1c02-5642-8186-a4b48145f1ca/scratchpad/r4review7/ws"); SRC = (ROOT / "ops/ci_provenance.py").read_text()
from mau_chuan_hoa import M
def cases(ma):
    code = ("import importlib.util as u,json,sys;s=u.spec_from_file_location('t','/tmp/claude-0/-home-user-tra-luat/eaf2a577-1c02-5642-8186-a4b48145f1ca/scratchpad/r4review7/ws/ops/ci_provenance_test.py');"
            "t=u.module_from_spec(s);s.loader.exec_module(t);print(json.dumps([(c,)+t.chay_ca(c) for c in t.CA]))")
    r = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True,
                       env=dict(os.environ, CI_PROVENANCE_MA=str(ma), PYTHONDONTWRITEBYTECODE="1"), timeout=900)
    return json.loads(r.stdout.strip().splitlines()[-1])
def mot(m):
    ten, cu, moi = m
    if SRC.count(cu) != 1: return ten, "HONG_NEO", SRC.count(cu)
    d = Path(tempfile.mkdtemp(prefix="tdb_", dir='/tmp/claude-0/-home-user-tra-luat/eaf2a577-1c02-5642-8186-a4b48145f1ca/scratchpad/r4review7/ws/.review/tmp')); p = d / f"db_{ten}.py"; p.write_text(SRC.replace(cu, moi))
    kq = cases(p)
    giet = [c for c, rc, o in kq if rc == 3 and o.startswith(f"DO:{c}:")]; vo = [c for c, rc, o in kq if rc not in (0, 3)]
    return ten, "GIET" if giet and not vo else "TIN_DUNG_GIA" if vo else "SONG", (giet[:4], vo[:4])
goc = cases(ROOT / "ops/ci_provenance.py"); assert all(rc == 0 for _, rc, _ in goc), goc
with ThreadPoolExecutor(6) as ex:
    for r in ex.map(mot, M): print(*r, flush=True)
