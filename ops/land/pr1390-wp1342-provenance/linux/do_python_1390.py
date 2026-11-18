"""Do _additive1342r2/_wired1342 va MUTANTS cho #1342 r3 (chay trong clone o merge). Dung: python -X utf8 -B do_python_1390.py <B> <H> <P> <M> <thu_muc_tam>"""
import hashlib, importlib.util, pathlib, subprocess, sys, warnings
warnings.simplefilter("ignore", SyntaxWarning)
B, H, P, M, TAM = sys.argv[1:6]; TAM = pathlib.Path(TAM); TAM.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, ".claude/dev")
import packet_loop_test as T
g = lambda r, f=".claude/dev/packet_loop.py": subprocess.run(["git", "show", f"{r}:{f}"], capture_output=True, check=True).stdout
print(f"_additive1342r2(base {B[:7]}, head {H[:7]}) =", T._additive1342r2(g(B), g(H)))
print(f"_additive1342r2(cha1 {P[:7]}, merge {M[:7]}) =", T._additive1342r2(g(P), g(M)))
print(f"_wired1342(merge {M[:7]}) =", T._wired1342(g(M)))
for r in (B, H, P, M):
    d = TAM / r[:7]; d.mkdir(exist_ok=True)
    (d / "packet_loop.py").write_bytes(g(r)); f = d / "packet_loop_test.py"; f.write_bytes(g(r, ".claude/dev/packet_loop_test.py"))
    for k in [k for k in sys.modules if k == "packet_loop"]: del sys.modules[k]
    sys.path.insert(0, str(d))
    sp = importlib.util.spec_from_file_location(f"plt_{r[:7]}", f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    sys.path.remove(str(d))
    mu = m.MUTANTS
    it = sorted((str(k), repr(v)) for k, v in (mu.items() if isinstance(mu, dict) else enumerate(mu)))
    print(r[:7], "MUTANTS", len(mu), "sha256(repr sap xep)", hashlib.sha256(repr(it).encode()).hexdigest()[:16],
          "CASES", len(m.CASES), "WP1174_REQUIRED", len(m.WP1174_REQUIRED), "WP1174_BOTH", len(m.WP1174_BOTH))
