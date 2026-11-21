"""Phep kiem dong lop F05-F08 (review offline luot 2): cung dot bien / phan chung, chay tren BAN CU (36dc91a) va BAN MOI.
Dung: python -B dong_lop.py <repo> <sha-cu> <sha-moi>. Moi dong: lop | ban | ket qua. Thoat 0 khi: MOI dung o moi dong; moi lop co >=1 dot bien/phan chung CU de lot."""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
repo, CU, MOI = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3]
TF, RL = "scripts/tl_core/test_fragments.py", "scripts/tl_core/release.py"
SO = "    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n"
SH = '            body.append("BUNDLED_FRAGMENT_SHARDS = ("'
BODY = 'body = header + lines + [")"]'
def phu(stmt):   # them mot cau lenh vao MOI manh phu (index >= 2) cua generator
    return [(TF, BODY, BODY + f' + ([{stmt!r}] if index > 1 else [])')]
F05 = {  # F05: moi dang cau lenh loader tu choi o manh chinh va manh phu
 "chinh_gan_nhieu_dich": [(TF, SH, SH.replace("SHARDS = (", "SHARDS = EXTRA = ("))],
 "chinh_dich_tuple": [(TF, BODY, BODY + ' + (["A, B = 0, 0"] if index == 1 and len(groups) > 1 else [])')],
 "chinh_annassign": [(TF, BODY, BODY + ' + (["X: int = 0"] if index == 1 and len(groups) > 1 else [])')],
 "phu_gan_nhieu_dich": phu("X = Y = 0"), "phu_dich_tuple": phu("A, B = 0, 0"), "phu_annassign": phu("X: int = 0"),
 "phu_augassign": phu("X += 0"), "phu_expr": phu("0"), "phu_import": phu("import os"), "phu_if": phu("if 0: pass"),
}
F06 = {
 "one_skip_chap_nhan_mot_manh_stale": [(RL, SO, SO.replace("if extra or any(", "if extra or len(expected_modules) > 1 and any("))],
 "one_red_tu_choi_mot_manh_current": [(RL, SO, SO.replace("if extra or any(", "if extra or len(expected_modules) == 1 or any("))],
 "multi_red_tu_choi_nhieu_manh_current": [(RL, SO, SO.replace("if extra or any(", "if extra or len(expected_modules) > 1 or any("))],
}
RUN = r'''
import sys, json, importlib.util, tempfile
from pathlib import Path
sys.dont_write_bytecode = True; sys.path.insert(0, "scripts")
import tl
from tl_core import test_fragments as tf
spec = importlib.util.spec_from_file_location("frag", "scripts/test_fragments/wp433_bundled_tach_manh.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
r = m.run(tl)
with tempfile.TemporaryDirectory() as t:     # quyet dinh LOADER tren dau ra generator (da dot bien) cua fixture 6 x 40 KiB
    fr = Path(t) / "scripts" / "test_fragments"; fr.mkdir(parents=True)
    for i in range(6):
        (fr / f"wp9001_f{i}.py").write_text(f'TEST_ID = "wp9001_f{i}"\n_PAD = "{"x" * 40960}"\n\n\ndef run(tl_module):\n    return True\n', encoding="utf-8")
    tf._BUNDLED_SHARD_LIMIT = 100 * 1024; tf.write_bundled_modules(fr, fr.parent); tf._BUNDLED_SHARD_LIMIT = 196608
    (Path(t) / "goi").mkdir(); [(Path(t) / "goi" / p.name).write_bytes(p.read_bytes()) for p in fr.parent.glob("tl_test_fragments_bundled*.py")]
    try:
        loader = len(tf.load_runtime_fragment_cases(Path(t) / "goi"))
    except Exception as e:
        loader = getattr(e, "code", type(e).__name__)
print("KQ " + json.dumps({"run": r, "n": len(m._KQ), "do": [k for k, v in m._KQ.items() if v is not True], "loader": loader}))
'''
PROBE7 = r'''
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
    for kieu in ("dut", "tro_dung"):
        goi = t / kieu / "scripts"; goi.mkdir(parents=True); dich = t / f"dich_{kieu}.py"
        if kieu == "tro_dung":
            dich.write_bytes((sc / "tl_test_fragments_bundled.py").read_bytes())
        (goi / "tl_test_fragments_bundled.py").symlink_to(dich)
        try:
            kq[f"runtime_{kieu}"] = len(tf.load_runtime_fragment_cases(goi))
        except Exception as e:
            kq[f"runtime_{kieu}"] = getattr(e, "code", type(e).__name__)
        try:
            kq[f"index_{kieu}"] = len(tf.load_test_id_index(goi.parent).entries if hasattr(tf.load_test_id_index(goi.parent), "entries") else ())
        except Exception as e:
            kq[f"index_{kieu}"] = getattr(e, "code", type(e).__name__)
    (sc / "tl_test_fragments_bundled.py").unlink(); (sc / "tl_test_fragments_bundled.py").symlink_to(t / "khong_co.py")
    kq["cong_ok_manh_1_dut"] = _test_fragments_check(t / "repo").get("ok")
print("KQ " + json.dumps(kq))
'''
PROBE8 = r'''
import sys, json, importlib.util, pathlib
sys.dont_write_bytecode = True; sys.path.insert(0, "scripts")
import tl
def tu_choi(self, *a, **k):
    raise PermissionError(1, "nen tu choi tao symlink (gia lap)")
pathlib.Path.symlink_to = tu_choi
spec = importlib.util.spec_from_file_location("frag", "scripts/test_fragments/wp433_bundled_tach_manh.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
r = m.run(tl)
print("KQ " + json.dumps({"run": r, "n": len(m._KQ), "do": [k for k, v in m._KQ.items() if v is not True], "ly_do": getattr(m, "_LY_DO", "KHONG CO")}))
'''
def cay(sha, subs):
    d = Path(tempfile.mkdtemp(prefix="dl_", dir="/dev/shm")) / "r"
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
    return json.loads(kq[-1][3:]) if kq else {"VANG": pr.stderr[-300:]}
sai = 0
lot = {}
def dong(lop, ten, cu, moi, dat):
    global sai
    sai += not dat
    print(("DAT " if dat else "SAI ") + f"{lop} {ten} | CU {CU[:7]} {json.dumps(cu, ensure_ascii=False)} | MOI {MOI[:7]} {json.dumps(moi, ensure_ascii=False)}")
for lop, bang, dich in (("F05", F05, ["V8"]), ("F06", F06, None)):
    for ten, subs in bang.items():
        cu, moi = chay(cay(CU, subs), RUN), chay(cay(MOI, subs), RUN)
        d = dich or (["V28"] if ten.startswith("multi") else ["V27"])
        ok = moi.get("run") is False and moi.get("n") == 32 and moi.get("do") == d   # MOI: do DUNG tap dich, khong vang
        if lop == "F05":
            ok = ok and cu.get("loader") == moi.get("loader") == "BUNDLED_MODULE_CONTRACT"   # loader tu choi dang nay
        lot.setdefault(lop, []).append(cu.get("run") is True)   # CU de lot dot bien nay?
        dong(lop, ten + (" [CU LOT]" if cu.get("run") is True else " [CU da bat]"), cu, moi, ok)
    sai += not any(lot[lop])   # lop dong that khi co >=1 dot bien CU lot ma MOI bat
cu, moi = chay(cay(CU, []), PROBE7), chay(cay(MOI, []), PROBE7)
dong("F07", "symlink_tai_ten_manh_1", cu, moi, cu.get("runtime_dut") == 0
     and all(moi.get(k) == "BUNDLED_MODULE_CONTRACT" for k in ("runtime_dut", "runtime_tro_dung")) and moi.get("cong_ok_manh_1_dut") is False)
cu, moi = chay(cay(CU, []), PROBE8), chay(cay(MOI, []), PROBE8)
dong("F08", "nen_tu_choi_symlink", cu, moi, cu.get("ly_do") == "KHONG CO" and moi.get("do") == ["V32"] and "PermissionError" in moi.get("ly_do", {}).get("V32", ""))
print("TONG: sai=%d" % sai)
sys.exit(1 if sai else 0)
