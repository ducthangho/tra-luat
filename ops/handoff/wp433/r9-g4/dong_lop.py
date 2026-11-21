"""Phep kiem dong lop F01-F04: cung mot dot bien / phan chung, chay tren BAN CU (4e74fe1) va BAN MOI.
Dung: python -B dong_lop.py <repo> <sha-cu> <sha-moi>. In mot dong cho moi (lop, ban)."""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
repo, CU, MOI = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3]
TF, RL = "scripts/tl_core/test_fragments.py", "scripts/tl_core/release.py"
SO = "    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n"
MUT = {
 "F01 shard-size-byte-oracle: dem ky tu thay vi byte": [(TF, 'size = len(line.encode("utf-8")) + 1', 'size = len(line) + 1')],
 "F02 shard-ast-shape-oracle: manh 1 them bieu thuc": [(TF, 'for k in range(2, len(groups) + 1)).rstrip() + ")")\n', 'for k in range(2, len(groups) + 1)).rstrip() + ")")\n            body.append("0")\n')],
 "F03 bundle-gate-fixture-oracle: cong bo so manh chinh": [(RL, SO, "    if extra or any((a != d) if i > 0 else (a is None) for i, ((_, d), (_, a)) in enumerate(zip(expected_modules, actual_modules))):\n")],
}
RUN = r'''
import sys, json, importlib.util
sys.dont_write_bytecode = True; sys.path.insert(0, "scripts")
import tl
spec = importlib.util.spec_from_file_location("frag", "scripts/test_fragments/wp433_bundled_tach_manh.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
r = m.run(tl); print("KQ " + json.dumps({"run": r, "n": len(m._KQ), "do": [k for k, v in m._KQ.items() if v is not True]}))
'''
PROBE = r'''
import sys, json, tempfile
from pathlib import Path
sys.dont_write_bytecode = True; sys.path.insert(0, "scripts")
import tl
from tl_core import test_fragments as tf
from tl_core.release import _test_fragments_check
kq = {}
with tempfile.TemporaryDirectory() as t:
    t = Path(t); fr = t / "repo" / "scripts" / "test_fragments"; fr.mkdir(parents=True); sc = fr.parent
    (fr / "wp9001_a.py").write_text('TEST_ID = "wp9001_a"\n\n\ndef run(tl_module):\n    return True\n', encoding="utf-8")
    tf.write_bundled_modules(fr, sc)
    that = t / "ngoai.py"; that.write_bytes((sc / "tl_test_fragments_bundled.py").read_bytes())
    (sc / "tl_test_fragments_bundled.py").unlink(); (sc / "tl_test_fragments_bundled.py").symlink_to(that)
    kq["cong_ok_khi_manh_1_la_symlink"] = _test_fragments_check(t / "repo").get("ok")
    goi = t / "goi" / "scripts"; goi.mkdir(parents=True); (goi / "tl_test_fragments_bundled.py").symlink_to(that)
    try:
        kq["loader"] = [c.test_id for c in tf.load_runtime_fragment_cases(goi)]
    except Exception as e:
        kq["loader"] = getattr(e, "code", type(e).__name__)
    that.write_bytes(b"giu nguyen\n")
    try:
        tf.write_bundled_modules(fr, sc); kq["writer"] = "khong loi"
    except Exception as e:
        kq["writer"] = getattr(e, "code", type(e).__name__)
    kq["dich_symlink_sau_writer"] = that.read_bytes().decode()[:20]
print("KQ " + json.dumps(kq))
'''
def cay(sha, subs):
    d = Path(tempfile.mkdtemp(prefix="dl_")) / "r"
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", str(repo), str(d)], check=True)
    subprocess.run(["git", "-C", str(d), "checkout", "-q", "--detach", sha], check=True)
    for rel, a, b in subs:
        p = d / rel; s = p.read_text(encoding="utf-8"); assert s.count(a) == 1, (rel, a)
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
for nhan, sha in (("CU ", CU), ("MOI", MOI)):
    print("F04 shard-symlink-follow: phan chung symlink tai ten manh 1 |", nhan, sha[:7], "|", chay(cay(sha, []), PROBE))
