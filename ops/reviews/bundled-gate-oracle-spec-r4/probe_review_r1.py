"""python -B probe.py <tree> <mutant>... : moi dot bien chay tren BAN SAO tree, tien trinh moi."""
import json, shutil, subprocess, sys, tempfile, datetime
from pathlib import Path
TF, RL, FR = "scripts/tl_core/test_fragments.py", "scripts/tl_core/release.py", "scripts/test_fragments/wp433_bundled_tach_manh.py"
SO = "    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n"
SH = 'for k in range(2, len(groups) + 1)).rstrip() + ")")\n'
MUT = {
 "doi_chung": [],
 "size-only": [(RL, SO, SO.replace("a != d", "len(a or b'') != len(d)"))],
 "size-only-raw": [(RL, SO, SO.replace("a != d", "len(a) != len(d)"))],
 "one-stale-ok": [(RL, '            "status": "stale",\n', '            "status": "stale",\n            "ok": len(expected_modules) == 1,\n')],
 "ann-empty": [(TF, SH, SH + '            body.append("X: int")\n')],
 "duplicate": [(TF, SH, SH + '            body.append("BUNDLED_FRAGMENT_SOURCES = ()")\n')],
 "missing-ok-narrow": [(RL, 'return {**payload, "status": "missing", "error": "BUNDLED_MODULE_MISSING"}', 'return {**payload, "ok": not bundled_path.is_symlink(), "status": "missing", "error": "BUNDLED_MODULE_MISSING"}')],
 "flip-mid-only-miss": [(RL, SO, SO.replace("a != d", "(a is None or a[:-1] != d[:-1] or len(a) != len(d))"))],
 # --- quet ca lop bundle-gate-fixture-oracle ---
 "missing-ok": [(RL, 'return {**payload, "status": "missing", "error": "BUNDLED_MODULE_MISSING"}', 'return {**payload, "ok": True, "status": "missing", "error": "BUNDLED_MODULE_MISSING"}')],
 "missing-status": [(RL, 'return {**payload, "status": "missing", "error": "BUNDLED_MODULE_MISSING"}', 'return {**payload, "status": "stale", "error": "BUNDLED_MODULE_MISSING"}')],
 "stale-rc1": [(RL, '    return 0 if payload.get("ok") else 2\n\n\ndef cmd_release_check', '    return 0 if payload.get("ok") else 1\n\n\ndef cmd_release_check')],
 "stale-status-current": [(RL, '            "status": "stale",\n', '            "status": "current",\n')],
 "extra-ok": [(RL, '            "status": "stale",\n', '            "status": "stale",\n            "ok": bool(extra) and len(extra) == 1,\n')],
 "absent-ok": [(RL, '            "status": "stale",\n', '            "status": "stale",\n            "ok": all(a is not None for _, a in actual_modules) is False,\n')],
 "absent-status": [(RL, '            "status": "stale",\n', '            "status": "stale" if all(a is not None for _, a in actual_modules) else "current",\n')],
 "extra-status": [(RL, '            "status": "stale",\n', '            "status": "current" if extra else "stale",\n')],
 "stale-sha-swap": [(RL, '            "actual_sha256": actual_sha256,\n            "expected_bytes": len(expected),\n            "actual_bytes": len(actual),\n            "extra_shards": extra,', '            "actual_sha256": expected_sha256,\n            "expected_bytes": len(expected),\n            "actual_bytes": len(actual),\n            "extra_shards": extra,')],
 "stale-flip-only-firstbyte": [(RL, SO, SO.replace("a != d", "(a is None or a[:1] != d[:1] or len(a) != len(d))"))],
 "stale-ignore-lastbyte-region": [(RL, SO, SO.replace("a != d", "(a is None or a[:-1] != d[:-1] or len(a) != len(d))"))],
 "stale-head-only": [(RL, SO, SO.replace("a != d", "(a is None or a[:64] != d[:64] or len(a) != len(d))"))],
 "stale-tail-only": [(RL, SO, SO.replace("a != d", "(a is None or a[-64:] != d[-64:] or len(a) != len(d))"))],
 "stale-sha-len-cmp": [(RL, SO, SO.replace("a != d", "(a is None or (len(a), a.count(b'#')) != (len(d), d.count(b'#')))"))],
}
# go ban va (A7)
HONG_C = '''        def sua(s):
            d = bytearray((s / t).read_bytes())
            d[0] ^= 1
            (s / t).write_bytes(bytes(d))
        _, _, rc, j = cong(nhom, sua)
        return (rc, j.get("ok"), j.get("status"), j.get("error"))
'''
MUT["A7-hong-cu"] = [(FR, HONG_C, '        return cong(nhom, lambda s: (s / t).write_bytes((s / t).read_bytes() + b"# sua\\n"))[3].get("error")\n'),
                     (FR, '_HONG = (2, False, "stale", "GENERATED_BUNDLE_STALE")\n', '_HONG = "GENERATED_BUNDLE_STALE"\n')]
GAN_C = '''    gan = {}                                           # DỮ LIỆU: chỉ phép gán chuẩn một đích Name, lấy lần ĐẦU
    for n in body:
        if type(n) is ast.Assign and [type(t) for t in n.targets] == [ast.Name] and n.targets[0].id in (_SRC, _SHA):
            gan.setdefault(n.targets[0].id, ast.literal_eval(n.value))
'''
MUT["A7-gan-cu"] = [(FR, GAN_C, '''    gan = {t.id: ast.literal_eval(n.value) for n in body for t in getattr(n, "targets", [getattr(n, "target", None)])
           if isinstance(t, ast.Name)}
''')]
RUN = r'''
import sys, json, importlib.util
sys.dont_write_bytecode = True
sys.path.insert(0, "scripts")
import tl
spec = importlib.util.spec_from_file_location("frag", "scripts/test_fragments/wp433_bundled_tach_manh.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
r = m.run(tl)
print("KQ " + json.dumps({"run": r, "kq": m._KQ, "ly_do": m._LY_DO}, ensure_ascii=False))
'''
tree = Path(sys.argv[1]).resolve()
args = sys.argv[2:]
compose = [a.split("+") for a in args]
for parts in compose:
    with tempfile.TemporaryDirectory(prefix="pr_") as t:
        d = Path(t) / "r"
        shutil.copytree(tree, d)
        ok = True
        for name in parts:
            for rel, a, b in MUT[name]:
                p = d / rel; s = p.read_text(encoding="utf-8")
                if s.count(a) != 1:
                    print("+".join(parts), "KHONG_AP_DUOC", name, s.count(a)); ok = False; break
                p.write_text(s.replace(a, b), encoding="utf-8", newline="\n")
        if not ok: continue
        t0 = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%SZ")
        pr = subprocess.run([sys.executable, "-B", "-c", RUN], cwd=d, capture_output=True, text=True)
        kq = [l for l in pr.stdout.splitlines() if l.startswith("KQ ")]
        if pr.returncode != 0 or not kq:
            print("+".join(parts), "VANG rc=%d" % pr.returncode, pr.stderr[-300:]); continue
        j = json.loads(kq[-1][3:])
        do = [k for k, v in j["kq"].items() if v is not True]
        print(t0, "+".join(parts), "rc=0 run=%s n=%d do={%s}" % (j["run"], len(j["kq"]), ",".join(do)), "ly_do=" + json.dumps(j["ly_do"], ensure_ascii=False)[:200])
