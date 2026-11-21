"""Phep kiem dong lop luot 2 (F05-F08): cung dot bien / phan chung, chay tren BAN CU va BAN MOI.
Dung: python -B dong_lop2.py <repo> <sha-cu> <sha-moi>. Moi dong mot clone moi va mot tien trinh moi."""
import shutil, subprocess, sys, tempfile
from pathlib import Path
repo, CU, MOI = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3]
TF, RL = "scripts/tl_core/test_fragments.py", "scripts/tl_core/release.py"
SO = "    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n"
MUT = {
 "F05 shard-ast-shape-oracle: manh 1 gan nhieu dich": [(TF, 'body.append("BUNDLED_FRAGMENT_SHARDS = ("', 'body.append("BUNDLED_FRAGMENT_SHARDS = EXTRA = ("')],
 "F05 shard-ast-shape-oracle: manh phu them AnnAssign": [(TF, 'body = header + lines + [")"]', 'body = header + lines + [")"] + (["X: int = 0"] if index > 1 else [])')],
 "F06 bundle-gate-fixture-oracle: one_skip (mot manh stale duoc nhan)": [(RL, SO, SO.replace("    if extra or any(", "    if len(expected_modules) > 1 and (extra or any(").replace("actual_modules)):", "actual_modules))):"))],
 "F06 bundle-gate-fixture-oracle: one_red (mot manh current bi tu choi)": [(RL, SO, SO.replace("    if extra or any(", "    if len(expected_modules) == 1 or extra or any("))],
}
DAU = r"""
import sys, json, importlib.util
sys.dont_write_bytecode = True; sys.path.insert(0, "scripts")
import tl
spec = importlib.util.spec_from_file_location("frag", "scripts/test_fragments/wp433_bundled_tach_manh.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
"""
RUN = DAU + r"""
r = m.run(tl); print("KQ " + json.dumps({"run": r, "n": len(m._KQ), "do": [k for k, v in m._KQ.items() if v is not True]}))
"""
TUCHOI = DAU + r"""
from pathlib import Path
def tu_choi(self, *a, **k):
    raise PermissionError("nen tu choi tao symlink (gia lap)")
Path.symlink_to = tu_choi
r = m.run(tl); print("KQ " + json.dumps({"run": r, "n": len(m._KQ), "do": [k for k, v in m._KQ.items() if v is not True], "ly_do": getattr(m, "_LY_DO", "KHONG CO _LY_DO")}))
"""
DUT = r"""
import sys, json, tempfile
from pathlib import Path
sys.dont_write_bytecode = True; sys.path.insert(0, "scripts")
from tl_core import test_fragments as tf
kq = {}
with tempfile.TemporaryDirectory() as t:
    sc = Path(t) / "goi" / "scripts"; sc.mkdir(parents=True)
    (sc / "tl_test_fragments_bundled.py").symlink_to(Path(t) / "khong-ton-tai.py")
    for ten, fn in (("runtime", lambda: [c.test_id for c in tf.load_runtime_fragment_cases(sc)]),
                    ("index", lambda: len(tf.load_test_id_index(Path(t) / "goi").entries))):
        try:
            kq[ten] = fn()
        except Exception as e:
            kq[ten] = getattr(e, "code", type(e).__name__)
print("KQ " + json.dumps(kq))
"""
def cay(sha, subs):
    d = Path(tempfile.mkdtemp(prefix="dl_")) / "r"
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", str(repo), str(d)], check=True)
    subprocess.run(["git", "-C", str(d), "checkout", "-q", "--detach", sha], check=True)
    for rel, a, b in subs:
        p = d / rel; s = p.read_text(encoding="utf-8"); assert s.count(a) == 1 and a != b, (rel, a)
        p.write_text(s.replace(a, b), encoding="utf-8", newline="\n")
    return d
def chay(d, code):
    pr = subprocess.run([sys.executable, "-B", "-c", code], cwd=d, capture_output=True, text=True)
    kq = [l for l in pr.stdout.splitlines() if l.startswith("KQ ")]
    shutil.rmtree(d.parent, ignore_errors=True)
    return "rc=%d %s" % (pr.returncode, kq[-1][3:] if kq else "KHONG CO KQ " + pr.stderr[-300:])
for ten, subs in MUT.items():
    for nhan, sha in (("CU ", CU), ("MOI", MOI)):
        print(ten, "|", nhan, sha[:7], "|", chay(cay(sha, subs), RUN))
for ten, code in (("F07 shard-symlink-follow: manh 1 la symlink DUT tren duong runtime", DUT),
                  ("F08 v32-symlink-denial-diagnostic: nen tu choi tao symlink", TUCHOI)):
    for nhan, sha in (("CU ", CU), ("MOI", MOI)):
        print(ten, "|", nhan, sha[:7], "|", chay(cay(sha, []), code))
