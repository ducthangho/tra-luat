"""Dot bien moi cua reviewer r4: chay tren mot clone, in do= tung dot bien (cung RUN voi ma_tran_r11)."""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
TF, RL = "scripts/tl_core/test_fragments.py", "scripts/tl_core/release.py"
NHAN = tuple(f"V{i}" for i in range(1, 33))
BODY = '        body = header + lines + [")"]\n'
COND = '(len(lines) == 1 and len(groups) > 1)'   # manh mot fragment trong goi nhieu manh
def them(stmt, cond=COND):
    return BODY.replace('[")"]\n', '[")"] + ([%r] if %s else [])\n' % (stmt, cond))
MUT = [
 ("doi_chung", []),
 ("s1_manh_don_trung_SOURCES_sau_rong", [(TF, BODY, them("BUNDLED_FRAGMENT_SOURCES = ()"))]),
 ("s2_manh_don_gan_khong_literal", [(TF, BODY, them("BUNDLED_FRAGMENT_COUNT = len(BUNDLED_FRAGMENT_SOURCES)"))]),
 ("s3_manh_don_annassign_rong", [(TF, BODY, them("X: int"))]),
 ("s4_manh_don_augassign_SOURCES", [(TF, BODY, them("BUNDLED_FRAGMENT_SOURCES += ()"))]),
 ("s5_manh_qua_co_trung_SOURCES", [(TF, BODY, them("BUNDLED_FRAGMENT_SOURCES = ()", '(len(lines) == 1 and len(lines[0].encode("utf-8")) + 1 > _BUNDLED_SHARD_LIMIT)'))]),
 ("s6_phi_ascii_annassign", [(TF, BODY, them("X: int", "any(ord(c) > 127 for l in lines for c in l)"))]),
 ("s7_manh_don_for_loop", [(TF, BODY, them("for BUNDLED_FRAGMENT_N in (): pass"))]),
 ("g1_cong_bo_qua_noi_dong_chu_thich", [(RL, '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n',
     '    if extra or any(a != d and not (a is not None and a.startswith(d) and a[len(d):].startswith(b"#")) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n')]),
 ("g2_missing_bao_stale", [(RL, 'return {**payload, "status": "missing", "error": "BUNDLED_MODULE_MISSING"}', 'return {**payload, "status": "missing", "error": "GENERATED_BUNDLE_STALE"}')]),
 ("g3_extra_chi_khi_khong_lech", [(RL, '    if extra or any(', '    if (extra and len(expected_modules) == 1) or any(')]),
]
RUN = r'''
import sys, json, importlib.util
sys.dont_write_bytecode = True
sys.path.insert(0, "scripts")
import tl
spec = importlib.util.spec_from_file_location("frag", "scripts/test_fragments/wp433_bundled_tach_manh.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
r = m.run(tl)
print("KQ " + json.dumps({"run": r, "kq": m._KQ, "ly_do": m._LY_DO}))
'''
files = subprocess.run(["git", "-C", str(repo), "ls-files"], capture_output=True, text=True, check=True).stdout.splitlines()
chon = set(sys.argv[2:])
for ten, subs in MUT:
    if chon and ten not in chon: continue
    with tempfile.TemporaryDirectory(prefix="rv4_") as t:
        d = Path(t) / "r"
        for rel in files:
            src = repo / rel
            if src.is_file():
                (d / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, d / rel)
        bad = None
        for rel, a, b in subs:
            p = d / rel; s = p.read_text(encoding="utf-8")
            if s.count(a) != 1: bad = (rel, s.count(a)); break
            p.write_text(s.replace(a, b), encoding="utf-8", newline="\n")
        if bad: print("KHONG_AP", ten, bad, flush=True); continue
        pr = subprocess.run([sys.executable, "-B", "-c", RUN], cwd=d, capture_output=True, text=True)
        kq = [l for l in pr.stdout.splitlines() if l.startswith("KQ ")]
        if not kq: print(ten, "VANG", pr.returncode, pr.stderr[-300:], flush=True); continue
        j = json.loads(kq[-1][3:])
        do = [n for n in NHAN if j["kq"].get(n) is not True]
        print(ten, "run=%s" % j["run"], "so_nhan=%d" % len(j["kq"]), "do=" + ",".join(do), "ly_do=" + json.dumps(j["ly_do"], ensure_ascii=False)[:300], flush=True)
